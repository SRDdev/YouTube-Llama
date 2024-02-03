# Imports
import os
import streamlit as st
from utils.ingest import create_vector_db
from utils.Services import Services
from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import LlamaCpp
from langchain.chains import RetrievalQA
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import datetime
# Constants
DB_FAISS_PATH = 'vectorstore/db_faiss'
current_time = datetime.datetime.now()
# Updated Prompt Template
template = f"""Use the following pieces of information to answer the user's question.
If you don't know the answer or if the data might be outdated, just say that you don't know or acknowledge the potential time lapse, don't try to make up an answer.

Current Time : {current_time}
Context: {{context}}
Question: {{question}}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

# Functions

def set_custom_prompt():     
    """
    Creates a custom prompt template for the QA model.

    Returns:
        PromptTemplate: The configured prompt template.
    """
    prompt = PromptTemplate(template=template, input_variables=['context', 'question'])
    return prompt

def retrieval_qa_chain(llm, prompt, db):
    """
    Configures and returns a RetrievalQA chain.

    Args:
        llm (LlamaCpp): The LlamaCpp language model.
        prompt (PromptTemplate): The prompt template for the QA model.
        db (FAISS): The FAISS vector store.

    Returns:
        RetrievalQA: Configured RetrievalQA chain.
    """
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                           chain_type='stuff',
                                           retriever=db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.3, "k": 4}),
                                           return_source_documents=True,
                                           chain_type_kwargs={'prompt': prompt},
                                           )
    return qa_chain
    
def delete_junk_files(folder_path, junk_extension):
    """
    Deletes files with a specific extension in a given folder.

    Args:
        folder_path (str): Path to the folder.
        junk_extension (str): Extension of the files to be deleted.
    """
    [os.remove(os.path.join(folder_path, file)) for file in os.listdir(folder_path) if file.endswith(junk_extension)]

def initialize_llama_model(selected_model):
    """
    Initializes and returns the LlamaCpp language model.

    Args:
        selected_model (str): The selected Llama model.

    Returns:
        LlamaCpp: Initialized LlamaCpp language model.
    """
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    model_path = f"models/{selected_model}.gguf"
    llm = LlamaCpp(
        model_path=model_path,
        n_gpu_layers=256,
        n_batch=512,
        max_tokens=2000,
        temperature=0.4,
        callback_manager=callback_manager,
        verbose=True,
    )

    return llm

def qa_bot(selected_model):
    """
    Configures and returns the QA bot.

    Args:
        selected_model (str): The selected Llama model.

    Returns:
        RetrievalQA: Configured RetrievalQA chain for the QA bot.
    """
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})

    db = FAISS.load_local(DB_FAISS_PATH, embeddings)
    llm = initialize_llama_model(selected_model)
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)
    return qa

# Streamlit UI code

# Title and Sidebar
st.title("🦙YouTube Llama")
st.markdown("Your own youtube video assistant. Ask question about anything, understand everything.")
st.caption("Created : Shreyas Dixit")
st.sidebar.title("HyperParameters")
selected_model = st.sidebar.radio("Llama Models", ["mistral-7b-instruct-v0.2.Q3_K_S","llama-2-7b-chat.Q2_K", "llama-2-7b-chat.Q4_K_M"])

# Custom Youtube Video
st.sidebar.markdown("#")
st.sidebar.markdown("#")
st.sidebar.subheader("Youtube Video Link")
url = st.sidebar.text_input('Enter Youtube Video Link')

# Understand Video Button
if st.sidebar.button("Understand Video"):
    st.video(url, format='video/mp4')
    with st.spinner("Learning, please wait for 2 mins..."):
        text_path = Services(url)
        create_vector_db()
        start_index = text_path.find("\\") + 1
        end_index = text_path.rfind(".")
        desired_substring = text_path[start_index:end_index]
    st.sidebar.markdown(f'**Watched "{desired_substring}" video!**')

# Chat History Initialization
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": f"What's on your mind ?"}]

# Display Chat History
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Sidebar Options
st.sidebar.markdown("#")
st.sidebar.markdown("#")
st.sidebar.subheader("Clear Chats")

# Clear Chats Button
if st.sidebar.button("Chats"):
    st.session_state.messages = []

# Delete Store Button
if st.sidebar.button('Delete Store'):
    delete_junk_files('data','.txt')

# User Input Handling
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with st.spinner("Thinking..."):
        qa_result = qa_bot(selected_model)
        response = qa_result({'query': prompt})
        helpful_answer = response['result']
        
        # Display Source Information
        if 'source_documents' in response and response['source_documents']:
            document = response['source_documents'][0]
            metadata = document.metadata
            file = metadata['source'].split("\\")[-1]
            source = os.path.splitext(file)[0]
            assistant_answer = f"{helpful_answer} \n\n Source : {source} Video"
        else:
            source = "Llama"
            assistant_answer = f"{helpful_answer} \n\n Source : {source} Model"
        
        # Update Chat History
        st.session_state.messages.append({"role": "assistant", "content": helpful_answer})
        st.chat_message("assistant").write(assistant_answer)
