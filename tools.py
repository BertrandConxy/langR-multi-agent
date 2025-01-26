from langchain_community.tools import WikipediaQueryRun, ArxivQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper

from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings

from dotenv import load_dotenv
load_dotenv()
    
def wikipedia_search():
    """Retrieve information from Wikipedia"""
    wikipediaRunner = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    return wikipediaRunner


def arxiv_search():
    """Retrieve information from Arxiv"""
    arxivRunner = ArxivQueryRun(api_wrapper=ArxivAPIWrapper())
    return arxivRunner

def retriever_tool():
    """Retrieve information from Rwanda Tax Law documents"""
    loader = WebBaseLoader('https://www.rra.gov.rw/fileadmin/user_upload/law_no_0162018.pdf')
    documents = loader.load()
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=1000,chunk_overlap=200).split_documents(documents)
    vector_store = FAISS.from_documents(
        chunks, embedding=OpenAIEmbeddings()
    )
    retriever = vector_store.as_retriever()
    retriever_tool = create_retriever_tool(
        retriever, "Rwanda_Tax_Law_Retriever",
        """For any questions related related or has context of Rwanda Tax Law,
            Search and retrieve information from Rwanda Tax Law documents db."""
    )
    return retriever_tool