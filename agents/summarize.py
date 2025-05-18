from google.adk.agents import BaseAgent
from google.adk.events import Event
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator
from transformers import T5Tokenizer, T5ForConditionalGeneration

class SummarizeAgent(BaseAgent):
    def __init__(self, name:str="summarize_agent"):
        super().__init__(name=name)

        self.tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
        self.model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small") 

    async def _run_async_impl(self, ctx:InvocationContext)-> AsyncGenerator[Event, None]:
        input_text = ctx.session.state.get("paper_text", "")
        if not input_text:
            yield Event(author=self.name, content="No input text provided")
            return
        
        input_ids = self.tokenizer("summary: "+input_text, retuen_tensors="pt").input_ids
        output_ids = self.model.generate(
            input_ids,
            max_length=150,
            min_length=30,
            do_sample=True, #makes the output deterministic
            early_stopping=True #avoids unnecessary generation
        )

        summary = self.tokenizer.decode(output_ids[0], skip_special_tokens=True) #converting model output into human readable text
        ctx.session.state["summary"] = summary #adk workflow chain agents. so writing in session will make it usable by other agents

        yield Event(author=self.name, content=summary)

    
