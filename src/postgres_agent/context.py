"""Runtime context for the PostgreSQL agent."""

from dataclasses import dataclass

from langchain_community.utilities import SQLDatabase


@dataclass
class RuntimeContext:
    """Runtime context providing database access to the agent and tools."""

    db: SQLDatabase

