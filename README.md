# Chat With Files


## Overview
 
This project allows you to locally upload PDF's and interact with their contents via a Large Language Model. It uses `Streamlit` to build the user interface and `embedchain` to create embeddings and handle queries. The `embedchain` app uses `llama3` as the LLM and `chroma` as the vector database.


## Features

* Upload PDF files, vectorize their contents, and store the embeddings in a local vector database.
* Ask the LLM questions based on the PDF contents.
* Clear the knowledge base to remove all uploaded content and the chat history.


## Requirements

* Python 3.9 or later
* Streamlit
* embedchain
* ollama (assumed to be running on localhost:11434)


## Installation

1.	Clone the repository:
```
git clone https://github.com/blobspire/chat_with_files.git
cd chat_with_files
```

2.	Create a virtual environment and activate it:
```
python -m venv .venv
source .venv/bin/activate
```

3.	Install the required packages:
```
pip install -r requirements.txt
```


## Usage

1.	Run the Streamlit app:
```
streamlit run pdf_chat.py
```

2. Upload a PDF file using the "Browse files" button.
3. Ask questions using the input box.
4. Click the "Clear Knowledge Base" button to remove all uploaded content, embeddings, and chat history.