# from pathlib import Path
# from dotenv import load_dotenv

# dotenv_path = Path('./.env')
# load_dotenv(dotenv_path=dotenv_path)

from langchain.document_loaders import PlaywrightURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import ElasticVectorSearch

urls = [
    "https://razorpay.com/docs/payments/easy-create-account",
    "https://razorpay.com/docs/payments/easy-submit-kyc"
]

loader = PlaywrightURLLoader(urls=urls, remove_selectors=["header", "footer"])

documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embedding = OpenAIEmbeddings()
db = ElasticVectorSearch.from_documents(documents=documents, 
        embedding=embedding, 
        elasticsearch_url="http://localhost:9200")

query = "What all APIs are supported in dispute?"
docs = db.similarity_search(query)

print(docs[0].page_content)