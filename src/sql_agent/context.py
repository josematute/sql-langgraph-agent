"""Runtime context for the SQL agent."""

from dataclasses import dataclass

from langchain_community.utilities import SQLDatabase


@dataclass
class RuntimeContext:
    """Runtime context providing database access to the agent and tools.
    
    Works with any SQL database (PostgreSQL, SQLite, MySQL, etc.).
    """

    db: SQLDatabase

