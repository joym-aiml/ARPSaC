from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator

from transformers import T5Tokenizer, T5ForConditionalGeneration


class CritiqueAgent(BaseAgent):
    def __init__(self, name="critique_agent"):
        super().__init__(name=name)

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        summary = ctx.session.state.get("summary", "").strip()
        if not summary:
            yield Event(author=self.name, content="No summary found for critique.")
            return

        # Moved inside the method
        tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
        model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

        prompt = (
            "Critique the following academic paper summary. Focus on strengths, novelty, and any weaknesses:\n\n"
            + summary
        )

        input_ids = tokenizer(prompt, return_tensors="pt").input_ids
        output_ids = model.generate(
            input_ids,
            max_length=200,
            min_length=50,
            do_sample=False,
            early_stopping=True
        )

        critique = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        ctx.session.state["critique"] = critique

        #yield Event(author=self.name, content="Critique generated.")

        from google.genai.types import Content, Part

        yield Event(
            author=self.name,
            content=Content(role="agent", parts=[Part(text=critique)])
        )

        #yield Event(author=self.name, content=critique)
