"""Interactive CLI for SQL agent."""

import sys

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.rule import Rule
from rich.status import Status
from rich.syntax import Syntax

from .agent import create_sql_agent, get_agent_context

console = Console()


@click.group()
def cli():
    """SQL LangGraph Agent CLI - Works with any SQL database"""


@cli.command()
@click.option(
    "--thread-id",
    default="default",
    help="Conversation thread ID for maintaining context",
)
def chat(thread_id: str):
    """
    Interactive chat mode with the SQL agent.

    Ask questions about your database schema and data.
    Works with any SQL database (PostgreSQL, SQLite, MySQL, etc.).
    The agent maintains conversation context, so follow-up questions work naturally.

    Exit with Ctrl+C or type 'exit'/'quit'.
    """
    console.print("\n[bold cyan]SQL Agent[/bold cyan] - Interactive Chat Mode")
    console.print(Rule(style="cyan"))
    console.print(f"[dim]Thread ID:[/dim] {thread_id}")
    console.print("[dim]Type 'exit', 'quit' or 'q' to end the conversation[/dim]")
    console.print(Rule(style="cyan"))
    console.print()

    # Create agent and get context with loading indicator
    with Status("Initializing agent and connecting to database", console=console):
        agent = create_sql_agent()
        context = get_agent_context()
    console.print("✅ Ready!\n", style="green")

    try:
        while True:
            # Get user input
            try:
                question = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n\nGoodbye!")
                sys.exit(0)

            if not question:
                continue

            # Check for exit commands
            if question.lower() in ("exit", "quit", "q"):
                print("\nGoodbye!")
                break

            # Stream agent response with loading indicator
            console.print("\n[bold blue]Agent:[/bold blue] ", end="")
            try:
                with Status("Thinking", console=console):
                    all_messages = []
                    final_message = None
                    messages_before = None
                    
                    # Get message count before this turn (to filter only new messages)
                    # We'll check the first step to see how many messages existed before
                    first_step = True
                    
                    for step in agent.stream(
                        {"messages": [{"role": "user", "content": question}]},
                        {"configurable": {"thread_id": thread_id}},
                        context=context,
                        stream_mode="values",
                    ):
                        # Get all messages from each step
                        if "messages" in step and step["messages"]:
                            all_messages = step["messages"]
                            final_message = step["messages"][-1]
                            
                            # On first step, capture the message count before our new user message
                            if first_step:
                                # The user message we just added is at the end, so count before it
                                messages_before = len(all_messages) - 1
                                first_step = False
                
                # Extract and display SQL queries only from the current interaction
                # (skip messages from previous conversations due to memory)
                sql_queries = []
                seen_queries = set()
                
                # Only process messages from the current turn (after messages_before)
                # This excludes previous conversation history
                current_turn_messages = all_messages[messages_before:] if messages_before else all_messages
                
                for msg in current_turn_messages:
                    # Check if this is an AIMessage with tool calls
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tool_call in msg.tool_calls:
                            # Handle both dict and object formats
                            if isinstance(tool_call, dict):
                                name = tool_call.get("name")
                                args = tool_call.get("args", {})
                            else:
                                name = getattr(tool_call, "name", None)
                                args = getattr(tool_call, "args", {})
                            
                            if name == "execute_sql" and isinstance(args, dict):
                                query = args.get("query")
                                if query and query not in seen_queries:
                                    sql_queries.append(query)
                                    seen_queries.add(query)
                
                # Display SQL queries if any
                if sql_queries:
                    console.print()
                    for i, query in enumerate(sql_queries, 1):
                        # Syntax highlight SQL queries
                        sql_syntax = Syntax(
                            query,
                            "sql",
                            theme="monokai",
                            line_numbers=False,
                            word_wrap=True,
                        )
                        console.print(
                            Panel(
                                sql_syntax,
                                title=f"[bold yellow]SQL Query {i}[/bold yellow]",
                                border_style="yellow",
                                expand=False,
                            )
                        )
                    console.print()
                
                # Print the final AI response
                if final_message and hasattr(final_message, "content"):
                    content = final_message.content
                    # Always render as markdown - Rich handles both markdown and plain text gracefully
                    try:
                        console.print(Markdown(content))
                    except Exception:
                        # Fallback to plain text if markdown parsing fails
                        console.print(content)
                
                # Add separator between conversation turns
                console.print()
                console.print(Rule(style="dim"))
                console.print()
            except Exception as e:
                console.print(f"\n[bold red]Error:[/bold red] {e}\n")
                console.print(Rule(style="dim"))
                console.print()
                continue

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)


if __name__ == "__main__":
    cli()

