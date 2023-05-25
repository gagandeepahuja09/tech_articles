from pathlib import Path
from dotenv import load_dotenv

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

dotenv_path = Path('./.env')
load_dotenv(dotenv_path=dotenv_path)

llm = OpenAI(temperature=0.9)
prompt = PromptTemplate(
    input_variables=["product"],
    template="What would be a good company name for a company that makes {product}?"
)

chain = LLMChain(llm=llm, prompt=prompt)

print(chain.run("colorful socks"))