# 🔗 PostgreSQL LangGraph Agent

A PostgreSQL SQL agent with memory built using LangGraph and LangChain.

## 🚀 Setup

### Prerequisites

-   Python 3.11 - 3.13 (as specified in `pyproject.toml`)
-   [uv](https://docs.astral.sh/uv/) package manager or [pip](https://pypi.org/project/pip/)
-   [Docker](https://www.docker.com/) and Docker Compose (for default database)
-   **Model Provider** (choose one):
    -   OpenAI API key (default)
    -   AWS Bedrock credentials (optional)

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

**Option 1: Use OpenAI (Default)**

```bash
# Add OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here
```

**Option 2: Use AWS Bedrock**

```bash
# Set model provider explicitly (optional, auto-detected if AWS credentials exist)
MODEL_PROVIDER=bedrock

# AWS credentials (use either credentials OR profile, not both)
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=us-east-1  # Optional, defaults to us-east-1

# OR use AWS profile instead:
# AWS_PROFILE=your_aws_profile_name

# Optional: Custom Bedrock model (defaults to Claude Haiku)
# BEDROCK_MODEL_ID=anthropic.claude-haiku-4-5-20251001-v1:0
```

**Optional: LangSmith tracing**

```bash
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=pg-langgraph-agent
```

**Model Provider Selection:**

-   If `MODEL_PROVIDER=bedrock` is set → uses AWS Bedrock
-   If `MODEL_PROVIDER=openai` is set → uses OpenAI
-   If `MODEL_PROVIDER` not set but AWS credentials exist → auto-detects Bedrock
-   Otherwise → defaults to OpenAI

Create virtual environment and install dependencies

```bash
# Create virtual environment and install dependencies
uv sync
```

### Database Setup

The agent needs a PostgreSQL database to connect to. You have two options:

#### Option 1: Use Default Database (Recommended for Quick Start)

The project includes a Docker setup with a sample database. This is the easiest way to get started:

```bash
# Start the default PostgreSQL database with sample data
docker compose up -d

# Check if it's running
docker compose ps
```

The default database will be available at:

-   **Connection**: `postgresql://postgres:postgres@localhost:5432/sample_db`
-   **Sample data**: Includes customers, products, orders, and order_items tables

**No configuration needed** - the agent will automatically use this database if `POSTGRES_URI` is not set in your `.env` file.

#### Option 2: Use Your Own Database

If you have your own PostgreSQL database (local, AWS RDS, Neon, etc.), set the connection string in your `.env` file:

```bash
# Add to your .env file
POSTGRES_URI=postgresql://user:password@host:port/database
```

**Examples:**

-   Local database: `POSTGRES_URI=postgresql://user:pass@localhost:5432/mydb`
-   AWS RDS: `POSTGRES_URI=postgresql://user:pass@your-rds-endpoint:5432/mydb`
-   Neon: `POSTGRES_URI=postgresql://user:pass@your-neon-endpoint/dbname`

**Note**: If `POSTGRES_URI` is set, it will override the default database.

### Running the Agent

Start the interactive chat:

```bash
# Run with uv
uv run python main.py chat

# Or activate the virtual environment if preferred
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python main.py chat
```

The agent will connect to your configured database and you can ask questions about the schema and data!

### Getting Started with LangSmith (Optional)

-   Create a [LangSmith](https://smith.langchain.com/) account
-   Create a LangSmith API key
-   Add it to your `.env` file as shown above
