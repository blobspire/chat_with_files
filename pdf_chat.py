import os
import shutil
import tempfile
import streamlit as st
from embedchain import App

# create a new temp directory and return the path
def create_temp_dir():
    return tempfile.mkdtemp()

# get a temp directory to store the provided pdf
db_path = create_temp_dir()
print(db_path)

# create embedchain app with given configuration.
# this app will create vector embeddings of the provided pdf and store them in the vector database so 
# that the llm can use them for the queries it recieves
def create_embedchain_app(dir_path):
    # define the configuration for the embedchain app.
    # use llama3 for the llm and chroma for the vector database
    embedchain_config = {
        "llm": {
            "provider": "ollama",
            "config": {
                "model": "llama3",
                "max_tokens": 250,
                "temperature": 0.5,
                "stream": True,
                "base_url": 'http://localhost:11434'
            }
        },
        "vectordb": {
            "provider": "chroma",
            "config": {
                "dir": dir_path
            }
        },
        "embedder": {
            "provider": "ollama",
            "config": {
                "model": "llama3",
                "base_url": 'http://localhost:11434'
            }
        }
    } # ollama hosts on port 11434
    return App.from_config(config = embedchain_config)

# create an instance of the embdedchain app
app = create_embedchain_app(dir_path=db_path)

# add title and description to gui
st.title("Chat with a PDF")
st.caption("Upload a PDF and ask it questions.")

# upload pdf
pdf_file = st.file_uploader("Upload a PDF", type="pdf")

# if a pdf file is uploaded, add its contents to the vector database
if pdf_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f: 
        # create a temp file named f
        f.write(pdf_file.getvalue()) # writes the pdf contents to temp file
        app.add(f.name, data_type="pdf_file") # f.name is the temp file path
        # add the temp file contents to the app. this vectorizes the content and stores in the vector db
    os.remove(f.name) # delete the temp file (its contents was added to the db so it's no longer needed)
    st.success(f"Successfully uploaded {pdf_file.name}!") # display success message on gui

# initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# display chat feed in box on gui
with st.expander("Chat History", expanded=True):
    for query, response in st.session_state.chat_history:
        st.write(f"**You:** {query}")
        st.write(f"**LLM:** {response}")

# initialize prompt within session state
if "prompt" not in st.session_state:
    st.session_state.prompt = ""

# ask a question using the pdf and display answer
def submit_prompt():
    prompt = st.session_state.prompt
    if prompt:
        answer = app.chat(prompt) # send prompt to app and recieve answer
        st.session_state.chat_history.append((prompt, answer)) # store query and response into chat history
        st.session_state.prompt = "" # reset the prompt after it and answer are added to chat history

prompt = st.text_input("What would you like to ask the PDF?", key="prompt", on_change=submit_prompt)

# add button to clear knowledge base
if st.button("Clear Knowledge Base"):
    try:
        if os.path.exists(db_path):
            shutil.rmtree(db_path) # delete temp dir
            db_path = create_temp_dir() # get new temp dir
            app = create_embedchain_app(dir_path=db_path) # create new app that will use the new temp dir
            app.reset() # clear the rag data
            st.session_state.chat_history = [] # clear the chat history
            st.success("Successfully cleared Knowledge Base.")
            st.rerun() # update the display
    except Exception as e:
        st.error(f"An error occurred while clearing the Knowledge Base: {e}")