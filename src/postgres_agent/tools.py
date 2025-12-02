"""SQL execution tool for any SQL database."""

from langchain_core.tools import tool
from langgraph.runtime import get_runtime

from .context import RuntimeContext


@tool
def execute_sql(query: str) -> str:
    """
    Execute a SQL SELECT query and return results.

    This tool is read-only and only allows SELECT queries.
    Works with any SQL database (PostgreSQL, SQLite, MySQL, etc.).
    No INSERT/UPDATE/DELETE/ALTER/DROP/CREATE/REPLACE/TRUNCATE commands are allowed.
    """
    runtime = get_runtime(RuntimeContext)
    db = runtime.context.db

    # Basic read-only enforcement
    query_upper = query.strip().upper()
    forbidden_keywords = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "ALTER",
        "DROP",
        "CREATE",
        "REPLACE",
        "TRUNCATE",
        "GRANT",
        "REVOKE",
    ]
    for keyword in forbidden_keywords:
        if keyword in query_upper:
            return f"Error: {keyword} operations are not allowed. This tool is read-only."

    try:
        return db.run(query)
    except Exception as e:
        return f"Error: {e}"

