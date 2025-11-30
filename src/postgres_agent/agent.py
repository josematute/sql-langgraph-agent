"""Agent creation with memory for PostgreSQL queries."""

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from .config import get_database
from .context import RuntimeContext
from .tools import execute_sql

SYSTEM_PROMPT = """You are a careful PostgreSQL analyst.

Rules:
- Think step-by-step.
- When you need data, call the tool `execute_sql` with ONE SELECT query.
- Read-only only; no INSERT/UPDATE/DELETE/ALTER/DROP/CREATE/REPLACE/TRUNCATE.
- Limit to 5 rows unless the user explicitly asks otherwise.
- If the tool returns 'Error:', revise the SQL and try again.
- Prefer explicit column lists; avoid SELECT *.
- PostgreSQL uses double quotes for identifiers if needed.
- Use proper PostgreSQL syntax (e.g., LIMIT not TOP).
"""


def create_sql_agent(model: str = "openai:gpt-4o-mini"):
    """
    Create agent with memory for PostgreSQL queries.

    Args:
        model: Model identifier (default: "openai:gpt-4o-mini")

    Returns:
        Agent with memory checkpointing enabled
    """
    return create_agent(
        model=model,
        tools=[execute_sql],
        system_prompt=SYSTEM_PROMPT,
        context_schema=RuntimeContext,
        checkpointer=InMemorySaver(),
    )


def get_agent_context() -> RuntimeContext:
    """
    Get runtime context with database connection.

    Returns:
        RuntimeContext instance with database
    """
    return RuntimeContext(db=get_database())

