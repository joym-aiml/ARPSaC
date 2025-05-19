from google.adk.agents import SequentialAgent
from google.adk.agents.invocation_context import InvocationContext


# Import agents
from .fetch_papers import FetchPapersAgent
from .selection import SelectionAgent
from .fetch_paper_details import FetchPaperDetailsAgent
from .summarize import SummarizeAgent
from .classify import ClassifyAgent
from .critique import CritiqueAgent

# Initialize agents
fetch_agent = FetchPapersAgent()
selection_agent = SelectionAgent()
detail_agent = FetchPaperDetailsAgent()
summarizer = SummarizeAgent()
classifier = ClassifyAgent()
critiquer = CritiqueAgent()

# Define the orchestrated pipeline
orchestrated_pipeline = SequentialAgent(
    name="arpsac_pipeline",
    sub_agents=[
        fetch_agent,
        selection_agent,
        detail_agent,
        summarizer,
        classifier,
        critiquer
    ]
)
