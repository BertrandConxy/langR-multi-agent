from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from tools import wikipedia_search, arxiv_search
from dotenv import load_dotenv

load_dotenv()

# Initialize model with a system message
model = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind(
    messages=[SystemMessage(content="You are a professional reporter agent who uses provided tools to make research on given topic and craft report.")]
)

# Define tools
tools = [wikipedia_search(), arxiv_search()]

# Initialize memory
memory = MemorySaver()

# Create agent without state_modifier
graph = create_react_agent(
    model,
    tools=tools,
    checkpointer=memory
)

 # Interface with the agent
def main():
    print("Chat with the AI Agent! Type 'exit' to quit.\n")
    config = {"configurable": {"thread_id": "1"}}

    while True:
        user_input = input("ME: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        inputs = [HumanMessage(content=user_input)]
        try:
            response = graph.invoke({"messages": inputs}, config)
            response_message = response["messages"][-1]
            print(f"Agent: {response_message.content}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()