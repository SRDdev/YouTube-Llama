# Horizon Chat API

Welcome to the Horizon Chat API! This API is designed to provide conversational responses to user queries using the Horizon language model and retrieval-based question-answering mechanisms. The system incorporates various components, such as the LlamaCpp language model, Faiss vector store, and Hugging Face embeddings.

## Getting Started

Follow these instructions to set up and use the Horizon Chat API on your local machine.

### Prerequisites

- Python 3.6 or later
- Flask (install via `pip install flask`)
- Faiss (install via `pip install faiss-cpu`)
- Other required Python packages (install via `pip install -r requirements.txt`)

### Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/horizon-chat-api.git
    ```

2. Navigate to the project directory:

    ```bash
    cd horizon-chat-api
    ```

3. Run the API:

    ```bash
    python app.py
    ```

   The API will be accessible at `http://127.0.0.1:5000/`.

### API Endpoint

- **Home:** `http://127.0.0.1:5000/`

- **Chat Endpoint:** `http://127.0.0.1:5000/chat`

    - **Method:** POST
    - **Input JSON Format:**
    
        ```json
        {
            "model": "llama-2-7b-chat.Q2_K",
            "user_input": "What is Productivity?"
        }
        ```

    - **Output JSON Format:**
    
        ```json
        {
            "Horizon Answer": "The helpful answer to the user's question."
        }
        ```

### Customization

- **Llama Model:**
  
  You can choose a specific Llama model by adjusting the `selected_model` parameter in the `chat()` function.

- **Vector Store:**

  The Faiss vector store is initialized with a specific path (`DB_FAISS_PATH`). Update this path or customize the initialization in the `qa_bot` function.

- **Embeddings:**

  The Hugging Face embeddings are set to use the "sentence-transformers/all-MiniLM-L6-v2" model. You can customize the model by adjusting the `model_name` parameter in the `HuggingFaceEmbeddings` instantiation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This API leverages various open-source libraries, including Flask, Faiss, and Hugging Face Transformers.
- Special thanks to the developers and contributors of the underlying language models and components.

Feel free to explore, experiment, and integrate this API into your applications!