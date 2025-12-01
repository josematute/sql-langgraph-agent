# 🔗 PostgreSQL LangGraph Agent

A PostgreSQL SQL agent with memory built using LangGraph and LangChain.

## 📑 Table of Contents

-   [Setup](#-setup)
    -   [Prerequisites](#prerequisites)
    -   [Installation](#installation)
    -   [Database Setup](#database-setup)
    -   [Running the Agent](#running-the-agent)
-   [Example Questions](#-example-questions)
-   [Getting Started with LangSmith (Optional)](#getting-started-with-langsmith-optional)
-   [Acknowledgments](#acknowledgments)

## 🚀 Setup

### Prerequisites

-   Python 3.11 - 3.13 (as specified in `pyproject.toml`)
-   [uv](https://docs.astral.sh/uv/) package manager
-   [Docker](https://www.docker.com/) and Docker Compose (for default database)
-   **Model Provider** (choose one):
    -   OpenAI API key (default)
    -   AWS Bedrock credentials (optional)

### Installation

Clone this repository and navigate to the project directory

```bash
git clone https://github.com/josematute/pg-langgraph-agent.git
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

**Recommended: Use AWS Profile (Preferred)**

If you have an AWS profile configured in `~/.aws/credentials`, you only need to set:

```bash
# Set model provider explicitly (optional, auto-detected if AWS credentials exist)
MODEL_PROVIDER=bedrock

# Use AWS profile (only these two lines needed if you have a profile)
AWS_PROFILE=your_aws_profile_name
AWS_REGION=us-east-1  # Optional, defaults to us-east-1
```

**Alternative: Direct Credentials**

If you don't have an AWS profile set up, you can use direct credentials instead:

```bash
# Set model provider explicitly (optional, auto-detected if AWS credentials exist)
MODEL_PROVIDER=bedrock

# Direct AWS credentials (use this if you don't have a profile)
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=us-east-1  # Optional, defaults to us-east-1
```

**Note**: The code checks for `AWS_PROFILE` first. If set, it uses the profile (you only need `AWS_PROFILE` and optionally `AWS_REGION`). Otherwise, it falls back to direct credentials.

**Optional Configuration:**

```bash
# Custom Bedrock model (defaults to Claude Haiku)
BEDROCK_MODEL_ID=anthropic.claude-haiku-4-5-20251001-v1:0
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

## 💡 Example Questions

Once the agent is running, you can ask questions about your database schema and data. The example questions below apply to the **default local Docker Compose PostgreSQL database** (with customers, products, orders, and order_items tables).

**Schema Exploration:**

-   "What tables are in this database?"
-   "Show me the schema for the customers table"
-   "What columns does the orders table have?"

**Data Queries:**

-   "Show me all customers"
-   "List all products with their prices"
-   "How many orders do we have?"
-   "Show me all customer orders with order items and product names"
-   "What are the top 5 products by sales?"

**Analytical Questions:**

-   "Which customer has the most orders?"
-   "What's the total revenue from all orders?"
-   "Show me orders from the last month"
-   "Which products are in the most orders?"

**Follow-up Questions (Memory):**

-   "Show me more details about that first customer"
-   "What products are in those orders?"
-   "How much did that customer spend in total?"

The agent maintains conversation context, so you can ask follow-up questions naturally without repeating information from previous queries.

## Getting Started with LangSmith (Optional)

LangSmith provides tracing, debugging, and monitoring for your agent. It's completely optional but can be helpful for development and debugging.

**To enable LangSmith:**

1.  Create a [LangSmith](https://smith.langchain.com/) account (free tier available)
2.  Create a LangSmith API key from your [LangSmith settings](https://smith.langchain.com/settings)
3.  Uncomment and fill in the LangSmith configuration in your `.env` file:

```bash
# In your .env file, uncomment and set:
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=pg-langgraph-agent
```

**Note:** The LangSmith configuration is commented out by default in `example.env`. You need to uncomment these lines and add your API key to enable tracing.

**To view traces:**

1.  Go to [https://smith.langchain.com/](https://smith.langchain.com/) and sign in
2.  Select your project: Use the project selector (top left) and choose `pg-langgraph-agent` (or whatever you set in `LANGSMITH_PROJECT`)
3.  View traces: After running the agent, traces will appear in the project. You'll see:
    -   Each agent run as a trace
    -   Tool calls (e.g., SQL queries executed)
    -   LLM requests and responses
    -   Token usage and timing
    -   The full conversation flow
4.  Click on any trace to see:
    -   The full conversation
    -   Each step the agent took
    -   SQL queries executed
    -   LLM prompts and responses
    -   Timing and costs

Traces appear automatically once `LANGSMITH_TRACING=true` is set and you run the agent. They show up in real-time as you use the CLI.

## Acknowledgments

This project is based on the [LangChain Essentials - Python](https://academy.langchain.com/courses/langchain-essentials-python) course from LangChain Academy. The agent implementation follows patterns and examples from the course materials, particularly:

-   **Lesson 1: Create Agent** - SQL agent implementation
-   **Lesson 6: Memory** - Conversation memory with `InMemorySaver`

The original course materials and examples can be found in the [LangChain Essentials GitHub repository](https://github.com/langchain-ai/lca-langchainV1-essentials/tree/main/python).
