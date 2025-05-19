import requests
import fitz
import io

from google.adk.agents import BaseAgent
from google.adk.events import Event
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator

class FetchPaperDetailsAgent(BaseAgent):
    def __init__(self, name:str = "fetch_paper_details_agent"):
        super().__init__(name=name)

    async def _run_async_impl(self, ctx:InvocationContext)-> AsyncGenerator[Event, None]:
        pdf_url = ctx.session.state.get("selected_paper_pdf_url")

        if not pdf_url:
            yield Event(author=self.name, content="No PDF URL found")
            return
        
        try:
            response=requests.get(pdf_url)
            response.raise_for_status()

            doc = fitz.open(stream=io.BytesIO(response.content), filetype="pdf")
            full_text=""

            for page in doc:
                full_text += page.get_text()

            if not full_text.strip():
                yield Event(author=self.name, content="Failed to extract any text from PDF")
                return
            
            #extracted text
            ctx.session.state["paper_text"]=full_text
            #yield Event(author=self.name, content=f"Successfully extracted paper content of ({len(full_text)} characters")

            from google.genai.types import Content, Part

            yield Event(
                author=self.name,
                content=Content(role="agent", parts=[Part(text=f"Successfully extracted paper content of ({len(full_text)} characters")])
            )


        except Exception as e:
            yield Event(author=self.name, content=f"Error downloading or parsing PDF: {str(e)}")