import requests
import xml.etree.ElementTree as ET   #data returned in Atom XML format

from google.adk.agents import BaseAgent
from google.adk.events import Event
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator

class FetchPapersAgent(BaseAgent):
    def __init__(self, name:str="fetch_papers_agent", max_results=5):
        super().__init__(name=name)
        self.max_results = max_results
        self.arxiv_url = "http://export.arxiv.org/api/query"

    async def _run_async_impl(self, ctx:InvocationContext)-> AsyncGenerator[Event, None]:
        query = ctx.session.state.get("query","").strip()
        if not query:
            yield Event(author=self.name, content="No input query provided by user")
            return
        
        params={
            "search_query": f"all:{query}",
            "start": 0,
            "max_results":self.max_results,
            "sortBy":"relevance",
            "sortOrder":"descending"
        }

        response= requests.get(self.arxiv_url, params=params)
        if response.status_code != 200:
            yield Event(author=self.name, content="Failed to fetch papers from arXiv")
            return
        
        root = ET.fromstring(response.text)
        namespace = {"arxiv": "http://www.w3.org/2005/Atom"}
        entries = root.findall("arxiv:entry", namespace)

        results=[]
        for entry in entries:
            title= entry.find("arxiv:title", namespace).text.strip()
            paper_id=entry.findall("arxiv:id", namespace).text().strip()
            summary = entry.findall("arxiv:summary", namespace).text.strip()
            results.append({
                "id":paper_id,
                "title":title,
                "summary": summary
            })

        ctx.session.state["search_results"] = results