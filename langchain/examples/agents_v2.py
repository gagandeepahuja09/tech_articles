from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

llm = OpenAI(temperature=0)

tools = load_tools(llm=llm, tool_names=["serpapi", "hiConverter"])

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

print(agent.run("Who is the president of the US? Say hi to him."))
# Result in the form of Observation, Thought, Action.


def hiConverter(input_string):
    return input_string + " hello hello hello"