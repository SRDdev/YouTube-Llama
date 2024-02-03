from flask import Flask, request, jsonify
import os
from utils.ingest import create_vector_db
from utils.Services import Services
from langchain.prompts import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import LlamaCpp
from langchain.chains import RetrievalQA
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import datetime

app = Flask(__name__)

# Constants
DB_FAISS_PATH = 'vectorstore/db_faiss'
current_time = datetime.datetime.now()
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
    prompt = PromptTemplate(template=template, input_variables=['context', 'question'])
    return prompt

def retrieval_qa_chain(llm, prompt, db):
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                           chain_type='stuff',
                                           retriever=db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.3, "k": 4}),
                                           return_source_documents=True,
                                           chain_type_kwargs={'prompt': prompt},
                                           )
    return qa_chain
    
def delete_junk_files(folder_path, junk_extension):
    [os.remove(os.path.join(folder_path, file)) for file in os.listdir(folder_path) if file.endswith(junk_extension)]

def initialize_llama_model(selected_model):
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
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})

    db = FAISS.load_local(DB_FAISS_PATH, embeddings)
    llm = initialize_llama_model(selected_model)
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)
    return qa

# Flask route for the home page
@app.route('/')
def home():
    return "Welcome to the Horizon Server!"

# Flask route to handle the user input
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    selected_model = data['model']
    if "user_input" in data:
        prompt = data["user_input"]
        messages = [{"role": "user", "content": prompt}]
        qa_result = qa_bot(selected_model)
        
        response = qa_result({'query': prompt})
        helpful_answer = response['result']

        if 'source_documents' in response and response['source_documents']:
            document = response['source_documents'][0]
            metadata = document.metadata
            file = metadata['source'].split("\\")[-1]
            source = os.path.splitext(file)[0]
            assistant_answer = f"{helpful_answer} \n\n Source : {source} Video"
        else:
            source = "Llama"
            assistant_answer = f"{helpful_answer} \n\n Source : {source} Model"
        
        messages.append({"role": "assistant", "content": helpful_answer})
        response_data = {"Horizon Answer": assistant_answer}
        return jsonify(response_data)
    else:
        return jsonify({"error": "Invalid request format"}), 400

if __name__ == '__main__':
    app.run(debug=True)
