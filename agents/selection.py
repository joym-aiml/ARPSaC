from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator


class SelectionAgent(BaseAgent):
    def __init__(self, name="selection_agent"):
        super().__init__(name=name)

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        search_results = ctx.session.state.get("search_results", [])
        selected_index = ctx.session.state.get("selected_index", 0)  # dynamic and safe

        if not search_results:
            yield Event(author=self.name, content="No search results found. Make sure FetchPaperAgent ran successfully.")
            return

        if selected_index >= len(search_results):
            yield Event(author=self.name, content=f"Invalid selection index: {selected_index}")
            return

        selected_paper = search_results[selected_index]

        ctx.session.state["selected_paper_id"] = selected_paper["id"]
        ctx.session.state["selected_paper_title"] = selected_paper["title"]
        ctx.session.state["selected_paper_summary"] = selected_paper["summary"]
        ctx.session.state["selected_paper_pdf_url"] = selected_paper.get("pdf_url")

        message = f"Selected paper #{selected_index + 1}: {selected_paper['title']}"
        
        from google.genai.types import Content, Part

        yield Event(
            author=self.name,
            content=Content(role="agent", parts=[Part(text=message)])
        )
