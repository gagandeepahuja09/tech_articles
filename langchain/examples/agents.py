from pathlib import Path
from dotenv import load_dotenv

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

llm = OpenAI(temperature=0)

tools = load_tools(llm=llm, tool_names=["serpapi", "llm-math"])

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

print(agent.run("What was the high temperature in SF yesterday in Fahrenheit? What is that number raised to the .023 power?"))
# Result in the form of Observation, Thought, Action.