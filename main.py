# main.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
from google.adk.sessions import Session
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import uuid

# Import orchestrated pipeline and agents
from agents.pipeline_orchestrator import orchestrated_pipeline
from agents.fetch_papers import FetchPapersAgent
from agents.selection import SelectionAgent
from agents.fetch_paper_details import FetchPaperDetailsAgent
from agents.summarize import SummarizeAgent
from agents.classify import ClassifyAgent
from agents.critique import CritiqueAgent

app = FastAPI(title="ARPSaC API", description="REST API for Research Paper Intelligence Agents")

# Initialize session service
session_service = InMemorySessionService()

# Helper to create session
def create_adk_session(query: str, selected_index: int = 0):
    session_id = str(uuid.uuid4())
    session = session_service.create_session(
        app_name="arpsac",
        user_id="demo-user",
        session_id=session_id,
        state={"query": query, "selected_index": selected_index}
    )
    return session_id, session

# Request and Response Models
class QueryRequest(BaseModel):
    query: str
    selected_index: int = 0

class AgentResponse(BaseModel):
    events: List[Dict[str, Any]]
    final_state: Dict[str, Any]

# Generic agent runner
async def run_agent(agent, session_id, content_text=None):
    runner = Runner(agent=agent, app_name="arpsac", session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=content_text)]) if content_text else None
    events = []
    async for event in runner.run_async(user_id="demo-user", session_id=session_id, new_message=content):
        events.append({"author": event.author, "content": event.content})
    session = session_service.get_session("arpsac", "demo-user", session_id)
    return {"events": events, "final_state": session.state}

# Endpoint per agent
@app.post("/run/fetch_papers", response_model=AgentResponse)
async def fetch_papers(request: QueryRequest):
    session_id, _ = create_adk_session(request.query)
    return await run_agent(FetchPapersAgent(), session_id)

@app.post("/run/selection", response_model=AgentResponse)
async def select_paper(request: QueryRequest):
    session_id, _ = create_adk_session(request.query, request.selected_index)
    return await run_agent(SelectionAgent(selected_index=request.selected_index), session_id)

@app.post("/run/fetch_details", response_model=AgentResponse)
async def fetch_details(request: QueryRequest):
    session_id, _ = create_adk_session(request.query, request.selected_index)
    return await run_agent(FetchPaperDetailsAgent(), session_id)

@app.post("/run/summarize", response_model=AgentResponse)
async def summarize_paper(request: QueryRequest):
    session_id, _ = create_adk_session(request.query, request.selected_index)
    return await run_agent(SummarizeAgent(), session_id)

@app.post("/run/classify", response_model=AgentResponse)
async def classify_paper(request: QueryRequest):
    session_id, _ = create_adk_session(request.query, request.selected_index)
    return await run_agent(ClassifyAgent(), session_id)

@app.post("/run/critique", response_model=AgentResponse)
async def critique_paper(request: QueryRequest):
    session_id, _ = create_adk_session(request.query, request.selected_index)
    return await run_agent(CritiqueAgent(), session_id)

# Endpoint to run entire orchestrated pipeline
@app.post("/run/full_pipeline", response_model=AgentResponse)
async def run_full_pipeline(request: QueryRequest):
    session_id, _ = create_adk_session(request.query, request.selected_index)
    return await run_agent(orchestrated_pipeline, session_id, content_text=request.query)
