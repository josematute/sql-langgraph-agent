from langchain.agents import create_agent
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    """Simple agent example that prints to console."""
    # Create a simple agent
    agent = create_agent(
        model="openai:gpt-4o-mini",
        system_prompt="You are a helpful assistant. Be concise and friendly.",
    )
    
    # Invoke with a simple message
    result = agent.invoke({"messages": "Hello! Can you tell me a short joke?"})
    
    # Print the response
    print("\n" + "="*50)
    print("Agent Response:")
    print("="*50)
    print(result["messages"][-1].content)
    print("="*50 + "\n")
    
    # Show message history
    print("Message History:")
    for msg in result["messages"]:
        print(f"{msg.type}: {msg.content}\n")


if __name__ == "__main__":
    main()
