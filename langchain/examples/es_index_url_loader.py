import os
import time

os.environ['OPENAI_API_KEY'] = ""

from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import ElasticVectorSearch
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

urls = [
    "https://razorpay.com/docs/payments/easy-create-account",
    "https://razorpay.com/docs/payments/easy-submit-kyc",
    "https://razorpay.com/docs/payments/business-types-kyc-documents",
    "https://razorpay.com/docs/payments/account-activation-support",
    "https://razorpay.com/docs/payments/faqs",
    "https://razorpay.com/docs/payments/dashboard",
    "https://razorpay.com/docs/payments/dashboard/home",
    "https://razorpay.com/docs/payments/disputes",
    "https://razorpay.com/docs/payments/payments/apis",
    "https://razorpay.com/docs/payments/payments/faqs"
]

loader = UnstructuredURLLoader(urls=urls)

documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

embedding = OpenAIEmbeddings()
db = ElasticVectorSearch.from_documents(documents=documents, 
        embedding=embedding, 
        elasticsearch_url="http://localhost:9200")

queries = [
    "what all steps are involved in signup?",
    "what can I do after after my kyc is complete?",
    "can you tell about business type llp?",
    "what is gst certificate?",
    "I have created an account. Can I change my business type?",
    "what all actions are supported for settlement",
    "how can i know number of payments i received in last 30 days?",
    "what are the different phase of disputes?",
    "what are the different payment APIs supported by Razorpay?",
    "how much does razorpay charge per transaction",
]

retriever = db.as_retriever(search_type="similarity", search_kwargs={"k":2})
qa = RetrievalQA.from_chain_type(
    llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=False)

for query in queries:
    result = qa({"query": query})
    answer = result['result']
    time.sleep(2)
    print("Query: ", query, "\n Answer:", answer, "\n\n")