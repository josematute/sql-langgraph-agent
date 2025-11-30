# 🔗 PostgreSQL LangGraph Agent

A PostgreSQL SQL agent with memory built using LangGraph and LangChain.

## 🚀 Setup

### Prerequisites

-   Python 3.11 - 3.13 (as specified in `pyproject.toml`)
-   [uv](https://docs.astral.sh/uv/) package manager or [pip](https://pypi.org/project/pip/)
-   [Docker](https://www.docker.com/) and Docker Compose (for default database)
-   OpenAI API key

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

### Database Setup

The agent uses a default PostgreSQL database (simple e-commerce sample database) running in Docker.

**Option 1: Use Default Database (Recommended for Quick Start)**

Start the default PostgreSQL database with Docker:

```bash
# Start the database container (creates sample database automatically)
docker-compose up -d

# Check if it's running
docker-compose ps
```

The database will be available at `postgresql://postgres:postgres@localhost:5432/sample_db`

The sample database includes:

-   **customers** table (5 sample customers)
-   **products** table (8 sample products)
-   **orders** table (5 sample orders)
-   **order_items** table (order details)
-   **Views**: `customer_orders` and `product_sales`

**Option 2: Use Your Own Database**

Set your own PostgreSQL connection string in `.env`:

```bash
# Add to .env file
POSTGRES_URI=postgresql://user:password@host:5432/dbname
```

For example, to use a Neon database or AWS RDS instance, just set the `POSTGRES_URI` environment variable.

**Stop the default database:**

```bash
docker-compose down
```

### Running the Agent

Start the interactive chat:

```bash
# Run with uv
uv run python main.py chat

# Or activate the virtual environment if preferred
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python main.py chat
```

The agent will connect to your database and you can ask questions about the schema and data!

## 📚 Project Status

This project is currently in development. See `docs/plan.md` for the full implementation plan.

### Getting Started with LangSmith (Optional)

-   Create a [LangSmith](https://smith.langchain.com/) account
-   Create a LangSmith API key
-   Add it to your `.env` file as shown above

---

**Note**: LangSmith Studio integration - TBD
