"""Interactive CLI for PostgreSQL agent."""

import sys

import click

from .agent import create_sql_agent, get_agent_context


@click.group()
def cli():
    """PostgreSQL LangGraph Agent CLI"""


@cli.command()
@click.option(
    "--thread-id",
    default="default",
    help="Conversation thread ID for maintaining context",
)
def chat(thread_id: str):
    """
    Interactive chat mode with the PostgreSQL agent.

    Ask questions about your database schema and data.
    The agent maintains conversation context, so follow-up questions work naturally.

    Exit with Ctrl+C or type 'exit'/'quit'.
    """
    print("PostgreSQL SQL Agent - Interactive Chat Mode")
    print("=" * 50)
    print(f"Thread ID: {thread_id}")
    print("Type 'exit' or 'quit' to end the conversation")
    print("=" * 50)
    print()

    # Create agent and get context
    agent = create_sql_agent()
    context = get_agent_context()

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

            # Stream agent response
            print("\nAgent: ", end="", flush=True)
            try:
                final_message = None
                for step in agent.stream(
                    {"messages": [{"role": "user", "content": question}]},
                    {"configurable": {"thread_id": thread_id}},
                    context=context,
                    stream_mode="values",
                ):
                    # Get the last message from each step
                    if "messages" in step and step["messages"]:
                        final_message = step["messages"][-1]
                
                # Print the final AI response
                if final_message and hasattr(final_message, "content"):
                    print(final_message.content)
                print()  # New line after response
            except Exception as e:
                print(f"\nError: {e}\n")
                continue

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)


if __name__ == "__main__":
    cli()

