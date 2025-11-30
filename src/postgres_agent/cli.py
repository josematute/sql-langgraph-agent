"""Interactive CLI for PostgreSQL agent."""

import sys
import threading
import time

import click

from .agent import create_sql_agent, get_agent_context


@click.group()
def cli():
    """PostgreSQL LangGraph Agent CLI"""


class Spinner:
    """Simple spinner for loading indicators."""

    def __init__(self, message="Loading"):
        self.message = message
        self.spinner_chars = "|/-\\"
        self.spinner_index = 0
        self.running = False
        self.thread = None

    def _spin(self):
        while self.running:
            char = self.spinner_chars[self.spinner_index % len(self.spinner_chars)]
            print(f"\r{self.message} {char}", end="", flush=True)
            self.spinner_index += 1
            time.sleep(0.1)

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        print("\r" + " " * (len(self.message) + 3) + "\r", end="", flush=True)


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

    # Create agent and get context with loading indicator
    spinner = Spinner("Initializing agent and connecting to database")
    spinner.start()
    try:
        agent = create_sql_agent()
        context = get_agent_context()
    finally:
        spinner.stop()
    print("✅ Ready!\n")

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
            print("\nAgent: ", end="", flush=True)
            spinner = Spinner("Thinking")
            spinner.start()
            try:
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
                
                spinner.stop()
                
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
                    print("\n" + "─" * 50)
                    for i, query in enumerate(sql_queries, 1):
                        print(f"[SQL QUERY {i}]:")
                        print(query)
                        print("─" * 50)
                    print()
                
                # Print the final AI response
                if final_message and hasattr(final_message, "content"):
                    print(final_message.content)
                print()  # New line after response
            except Exception as e:
                spinner.stop()
                print(f"\nError: {e}\n")
                continue

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)


if __name__ == "__main__":
    cli()

