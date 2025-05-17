# 🧠 ARPSaC: Agentic AI for Automated Research Paper Summarization and Critique

**ARPSaC** is an end-to-end, autonomous, agentic AI system designed to ingest, analyze, and summarize newly published academic research papers. Built with NLP, deep learning, and orchestrated using Google ADK, the system automatically classifies papers, summarizes content, generates critical insights, and stores structured intelligence for interactive retrieval.

> 📚 Think of ARPSaC as your intelligent research assistant—reading, analyzing, and distilling insights so you can focus on what truly matters: knowledge.

---

## 🚀 Key Features

- 🤖 **Autonomous Agent Pipeline** using Google ADK
- 📝 **Summarization** of abstracts, introductions, and conclusions using T5/BART
- 🧠 **Critique Generation** (strengths, weaknesses, novelty detection)
- 🧩 **Domain Classification** of papers via fine-tuned BERT
- 🔍 **Semantic Search** using Sentence-BERT embeddings & FAISS
- 🔄 **Real-Time Knowledge Base** using Firebase Firestore
- 💬 **Conversational Interface** for querying and exploration

---

## 🧱 System Architecture
```text
           ┌──────────────┐
           │  Paper Fetch │◄────┐
           └────┬─────────┘     │
                ▼               │
       ┌────────────────┐       │
       │  Domain Class. │       │
       └────┬───────────┘       │
            ▼                   │  Scheduled
     ┌──────────────┐           │  Agentic
     │ Summarizer   │           │  Pipeline
     └────┬─────────┘           │
          ▼                    │
  ┌─────────────────────┐      │
  │ Critique Generation │──────┘
  └────┬────────────────┘
       ▼
 ┌──────────────┐
 │ Vector Store │◄─ Search
 └────┬─────────┘
      ▼
┌──────────────────────┐
│ Firestore Knowledge  │
└────────┬─────────────┘
         ▼
┌──────────────────────┐
│ Conversational Agent │
└──────────────────────┘
```

---

## 🛠️ Tech Stack & Tools Used

| Category             | Technology / Tool                            |
|----------------------|----------------------------------------------|
| **Language**         | Python 3.12+                                 |
| **NLP Models**       | T5, BART, BERT, Sentence-BERT                |
| **Deep Learning**    | HuggingFace Transformers, PyTorch            |
| **Agent Orchestration** | Google AI Developer Kit (ADK)            |
| **Storage**          | Firebase Firestore                           |
| **Embeddings**       | FAISS, Pinecone (optional alternative)       |
| **Frontend (Optional)** | Streamlit or React                        |
| **PDF Parsing**      | PyMuPDF, pdfminer.six (optional extension)   |
| **Deployment**       | Docker (optional), GitHub Actions (CI/CD)    |

---

## 🧠 Skills Demonstrated

| Skill Domain         | Demonstrated Capabilities                                       |
|----------------------|-----------------------------------------------------------------|
| **NLP**              | Summarization, classification, generation, embedding            |
| **Deep Learning**    | Fine-tuning, transformer architectures, model evaluation        |
| **Agentic AI**       | Autonomous multi-step pipelines, stateful agents via Google ADK |
| **Cloud/Serverless** | Firestore integration, ADK-managed workflows                    |
| **Data Engineering** | Parsing PDFs, handling unstructured text, storing embeddings    |
| **Search**           | Semantic vector search via FAISS                                |
| **MLOps**            | Reproducible pipelines, modular design                          |
| **Product Thinking** | Practical tool for academic research automation                 |
| **Communication**    | Query interface, dynamic summarization-based conversations      |

---

## 🔍 Use Cases

- 🧠 **Research Assistants**: Automatically summarize and critique latest papers.
- 🔬 **Trend Monitoring**: Detect emerging areas in scientific domains.
- 📊 **Knowledge Base Generation**: Create searchable corpora of structured academic content.
- 💬 **Conversational AI**: Ask domain-specific questions like:
  - *"What are the newest approaches in transformer efficiency?"*
  - *"Summarize recent papers in few-shot learning."*

---

## 📦 Folder Structure

```text
arpsac-agentic-ai/
│
├── experiments/                  # All experimental notebooks and prototype scripts
│   ├── summarization/
│   │   ├── t5_baseline.ipynb
│   │   ├── t5_finetuned.ipynb
│   │   └── eval_results.md
│   ├── critique_generation/
│   ├── classification/
│   └── pipeline_simulations/
│
├── evaluations/                  # Centralized evaluation results and benchmarking
│   ├── rouge_bleu_scores.csv
│   ├── agent_timing_stats.md
│   └── critique_quality_analysis.md
│
├── logs/                         # Personal logs and detailed notes
│   ├── dev_logs/
│   │   ├── 2025-05-17.md
│   │   ├── 2025-05-18.md
│   │   └── ...
│   ├── decisions/
│   │   ├── model_selection.md
│   │   ├── critique_scoring_strategy.md
│   │   └── prompting_versions.md
│   └── progress_tracker.md
│
├── agents/                       # Finalized agent modules
│   ├── fetch_papers.py
│   ├── summarize.py
│   ├── critique.py
│   ├── classify.py
│   └── pipeline_orchestrator.py
│
├── models/                       # Trained models or export paths
│   ├── summarizer/
│   └── classifier/
│
├── storage/                      # Storage logic for firestore/vector DB
│   ├── firestore_interface.py
│   └── vector_indexer.py
│
├── interface/                    # UI or API interface
│   └── streamlit_app.py
│
├── adk_config/                   # Google ADK pipeline definitions
│   └── pipelines.json
│
├── utils/                        # General helper functions
│   ├── arxiv_parser.py
│   └── text_cleaner.py
│
├── requirements.txt
├── main.py
├── README.md
└── CONTRIBUTING.md
```
---

## 🛠️ Setup & Run Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/joy-aiml/arpsac-agentic-ai.git
   cd arpsac-agentic-ai
   ```

2. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Firebase & Google ADK**
   - Add your Firebase credentials under config/
   - Set ADK task flow via adk_config/pipelines.json
  

4. **Run the Agent Pipeline**
   ```bash
   python main.py
   ```

5. **Launch the Conversational UI(optional**
   ```bash
   streamlit run interface/streamlit_app.py
   ```

 ## 📒 Development Journey

This repository is structured to reflect the full research + engineering lifecycle. Each module was designed, tested, and validated through documented experimentation before being finalized into agent components.

You can explore:
- `experiments/`: early ideas, alternatives, performance tests
- `logs/`: personal dev diary and architectural decision logs
- `evaluations/`: quantitative benchmarks of model components

