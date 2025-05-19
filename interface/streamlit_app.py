import streamlit as st
import asyncio
import sys
import os
import uuid

from google.adk.sessions import Session
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# Path setup
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.pipeline_orchestrator import orchestrated_pipeline

# UI setup
st.set_page_config(page_title="ARPSaC Interface", layout="centered")
st.title("ARPSaC — Research Paper Intelligence")

query = st.text_input("Enter your research query:", "")
run_button = st.button("Search and Analyze")

if run_button and query:
    st.info("Running ARPSaC agent pipeline...")

    # Prepare session + service
    session_id = str(uuid.uuid4())
    session_service = InMemorySessionService()
    session = session_service.create_session(
        app_name="arpsac",
        user_id="demo-user",
        session_id=session_id,
        state={
            "query": query,
            "selected_index": 0
        }
    )

    runner = Runner(
        agent=orchestrated_pipeline,
        app_name="arpsac",
        session_service=session_service
    )

    logs = []

    async def run_pipeline():
        content = types.Content(role="user", parts=[types.Part(text=query)])
        async for event in runner.run_async(user_id="demo-user", session_id=session_id, new_message=content):
            logs.append((event.author, event.content))
            st.write(f"**[{event.author}]**: {event.content}")

    asyncio.run(run_pipeline())

    st.success("✅ Pipeline complete.")

    st.subheader("📄 Final Summary")
    st.write(session.state.get("summary", "No summary generated."))

    st.subheader("🏷️ Classification")
    st.write(", ".join(session.state.get("classification", [])) or "No classification available.")

    st.subheader("🧠 Critique")
    st.write(session.state.get("critique", "No critique generated."))
