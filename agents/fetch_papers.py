import requests
import xml.etree.ElementTree as ET

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator


class FetchPapersAgent(BaseAgent):
    def __init__(self, name: str = "fetch_papers_agent"):
        super().__init__(name=name)

    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        query = ctx.session.state.get("query", "").strip()
        if not query:
            yield Event(author=self.name, content="No input query provided by user.")
            return

        # define as local variables
        max_results = 5
        arxiv_url = "http://export.arxiv.org/api/query"

        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
            "sortBy": "relevance",
            "sortOrder": "descending"
        }

        response = requests.get(arxiv_url, params=params)
        if response.status_code != 200:
            yield Event(author=self.name, content="Failed to fetch papers from arXiv.")
            return

        root = ET.fromstring(response.text)
        namespace = {"arxiv": "http://www.w3.org/2005/Atom"}
        entries = root.findall("arxiv:entry", namespace)

        results = []
        for entry in entries:
            title = entry.find("arxiv:title", namespace).text.strip()
            paper_id = entry.find("arxiv:id", namespace).text.strip()
            summary = entry.find("arxiv:summary", namespace).text.strip()

            pdf_url = None
            for link in entry.findall("arxiv:link", namespace):
                if link.attrib.get("title") == "pdf":
                    pdf_url = link.attrib["href"]
                    break

            results.append({
                "id": paper_id,
                "title": title,
                "summary": summary,
                "pdf_url": pdf_url
            })

        ctx.session.state["search_results"] = results

        paper_titles = "\n".join([f"{i+1}. {r['title']}" for i, r in enumerate(results)])
        message = f"Top {len(results)} papers found for query: '{query}'\n\n{paper_titles}"
        
        from google.genai.types import Content, Part

        yield Event(
            author=self.name,
            content=Content(role="agent", parts=[Part(text=message)])
        )
