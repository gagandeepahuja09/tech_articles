from langchain.memory import ConversationBufferMemory
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool, tool

from pathlib import Path
from dotenv import load_dotenv

@tool
def update_website_details(url: str) -> str:
    """when the customer wants to update their website details"""
    return f"Status: website updated to {url}"

@tool
def upload_file(fileName: str) -> str:
    """when the customer wants to upload a file"""
    return f"Status: file successfully uploaded {fileName}"


dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

llm = ChatOpenAI(temperature=0)

tools = [
    Tool(
        name = "Update website details",
        func=update_website_details.run,
        description="when the customer wants to update their website details"
    ),
    Tool(
        name="Upload file",
        func=upload_file.run,
        description="when the customer wants to upload a file",
    )
]

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

agent_chain = initialize_agent(tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

print(agent_chain.run("Make my website as gagan.com and then upload the file ./abc/xzy.pdf"))
# Result in the form of Observation, Thought, Action.