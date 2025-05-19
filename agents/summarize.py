from google.adk.agents import BaseAgent
from google.adk.events import Event
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator
from transformers import T5Tokenizer, T5ForConditionalGeneration
from utils.chunking import chunk_text

class SummarizeAgent(BaseAgent):
    def __init__(self, name:str="summarize_agent"):
        super().__init__(name=name)

    async def _run_async_impl(self, ctx:InvocationContext)-> AsyncGenerator[Event, None]:
        input_text = ctx.session.state.get("paper_text", "")
        if not input_text:
            yield Event(author=self.name, content="No input text provided")
            return
        
        tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
        model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

        chunks = chunk_text(input_text, max_tokens=400, overlap=100)
        chunk_summaries = []

        # Step 2: Summarize each chunk
        for i, chunk in enumerate(chunks):
            input_text = "summarize: " + chunk
            input_ids = tokenizer(input_text, return_tensors="pt").input_ids
            output_ids = model.generate(
                input_ids,
                max_length=150,
                min_length=30,
                do_sample=False,
                early_stopping=True
            )
            summary = tokenizer.decode(output_ids[0], skip_special_tokens=True)
            chunk_summaries.append(summary)

            #yield Event(author=self.name, content=f"Summarized chunk {i+1}/{len(chunks)}")

            from google.genai.types import Content, Part

            yield Event(
                author=self.name,
                content=Content(role="agent", parts=[Part(text=f"Summarized chunk {i+1}/{len(chunks)}")])
            )


        # Step 3: Save summaries to session
        ctx.session.state["chunk_summaries"] = chunk_summaries
        final_summary = "\n".join(chunk_summaries)
        ctx.session.state["summary"] = final_summary

        #yield Event(author=self.name, content="All chunks summarized and merged.")
        

    
