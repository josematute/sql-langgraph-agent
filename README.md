# 🔗 PostgreSQL LangGraph Agent

A PostgreSQL SQL agent with memory built using LangGraph and LangChain.

## 🚀 Setup

### Prerequisites

- Python 3.11 - 3.13 (as specified in `pyproject.toml`)
- [uv](https://docs.astral.sh/uv/) package manager or [pip](https://pypi.org/project/pip/)
- OpenAI API key

### Installation

Clone this repository and navigate to the project directory

```bash
git clone <your-repo-url>
cd pg-langgraph-agent
```

Make a copy of `example.env`

```bash
# Create .env file
cp example.env .env
```

Insert API keys directly into `.env` file

```bash
# Add OpenAI API key (required)
OPENAI_API_KEY=your_openai_api_key_here

# Optional: For LangSmith tracing
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=pg-langgraph-agent
```

Create virtual environment and install dependencies

```bash
# Create virtual environment and install dependencies
uv sync
```

### Running the Agent

Run the simple agent example

```bash
# Run with uv
uv run python main.py

# Or activate the virtual environment if preferred
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python main.py
```

## 📚 Project Status

This project is currently in development. See `docs/plan.md` for the full implementation plan.

### Getting Started with LangSmith (Optional)

- Create a [LangSmith](https://smith.langchain.com/) account
- Create a LangSmith API key
- Add it to your `.env` file as shown above

---

**Note**: LangSmith Studio integration - TBD

