from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from dotenv import load_dotenv
import json
from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain import PromptTemplate, LLMChain
from langchain.llms import HuggingFaceHub
from huggingface_hub import hf_hub_download #load from huggingfaces
from constants import *
from langchain.llms import CerebriumAI
# import chainlit as cl
from core.settings import get_ai_credentials


# Path to the FAISS database vECTORE store
DB_FAISS_PATH

# Load environment variables from a .env file
load_dotenv()
settings = get_ai_credentials()
settings["CEREBRIUMAI_API_KEY"]

# Custom prompt template for QA retrieval
custom_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

def set_custom_prompt():
    """
    Set the custom prompt template for QA retrieval.
    Returns:
        PromptTemplate: The configured prompt template.
    """
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context', 'question'])
    return prompt

# Retrieval QA Chain
def retrieval_qa_chain(llm, prompt, db):
    """
    Create a RetrievalQA chain for question answering.

    Args:
        llm (CTransformers): The LLM model.
        prompt (PromptTemplate): The prompt template for QA retrieval.
        db (FAISS): The FAISS database for retrieval.

    Returns:
        RetrievalQA: The configured QA chain.
    """
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                           chain_type='stuff',
                                           retriever=db.as_retriever(search_kwargs={'k': 2}),
                                           return_source_documents=True,
                                           chain_type_kwargs={'prompt': prompt}
                                           )
    return qa_chain

# Get the LLM model path
def get_llm_model_path():
    """
    Get the path to the LLM model.

    Returns:
        str: The path to the LLM model.
    """
    # Load from Hugging Face model hub
    model_path = hf_hub_download(repo_id="TheBloke/Llama-2-7B-Chat-GGML", filename="llama-2-7b-chat.ggmlv3.q2_K.bin")
    return model_path




# Define a global variable to store the LLM model
global_llm = None

# Load the LLM model
def load_llm():
    """
    Load the LLM (Language Model) if not already loaded.

    Returns:
        CTransformers: The loaded LLM model.
    """
    global global_llm
    if global_llm is None:
        global_llm = CTransformers(
            model=get_llm_model_path(),
            model_type="llama",
            max_new_tokens=512,
            temperature=0.5
        )
    return global_llm

# QA Bot function
def qa_bot(llm_model):
    """
    Create a QA bot for question answering.

    Args:
        llm_model (CTransformers): The LLM model.

    Returns:
        RetrievalQA: The configured QA chain.
    """
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(DB_FAISS_PATH, embeddings)
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm_model, qa_prompt, db)

    return qa

# Final result function
def final_result(query):
    """
    Get the final result by querying the QA bot with a user's query.

    Args:
        query (str): The user's query.

    Returns:
        dict: The response from the QA bot.
    """
    global global_llm  # Use the global LLM model
    if global_llm is None:
        raise ValueError("LLM model not loaded")
    qa_result = qa_bot(global_llm)
    response = qa_result({'query': query})
    return response
