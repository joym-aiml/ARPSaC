from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator

from transformers import pipeline
from utils.chunking import chunk_text


class ClassifyAgent(BaseAgent):
    def __init__(self, name="classify_agent"):
        super().__init__(name=name)

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        text = ctx.session.state.get("paper_text", "")
        if not text:
            yield Event(author=self.name, content="No paper text found for classification.")
            return

        # Move config and model inside the method
        max_tokens = 400
        overlap = 100
        classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")
        labels = ["research", "methodology", "results", "review", "theoretical", "survey", "application"]

        chunks = chunk_text(text, max_tokens=max_tokens, overlap=overlap)
        chunk_labels = []

        for i, chunk in enumerate(chunks):
            result = classifier(chunk, candidate_labels=labels, multi_label=True)
            top_labels = [label for label, score in zip(result["labels"], result["scores"]) if score >= 0.5]
            chunk_labels.append(top_labels)

            yield Event(author=self.name, content=f"Classified chunk {i+1}/{len(chunks)}")

        # Aggregate labels
        label_counts = {}
        for label_list in chunk_labels:
            for label in label_list:
                label_counts[label] = label_counts.get(label, 0) + 1

        top_labels = sorted(label_counts, key=label_counts.get, reverse=True)

        ctx.session.state["classification"] = top_labels
        ctx.session.state["chunk_labels"] = chunk_labels

        #yield Event(author=self.name, content=f"Final classification: {', '.join(top_labels)}")

        from google.genai.types import Content, Part

        yield Event(
            author=self.name,
            content=Content(role="agent", parts=[Part(text=f"Final classification: {', '.join(top_labels)}")])
        )

