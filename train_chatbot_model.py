import os
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# Step 1: Define the knowledge base (This is your hospital's data)
# We will simulate a text file containing the hospital's information.
# In a real-world scenario, this could be a PDF, website, or other documents.
hospital_knowledge_base = """
Vardhman Mahaveer Health Care is a premier multi-specialty hospital located in Patiala, Punjab.
Address: S.C.O-34, Urban Estate, Phase-2, Rajpura Road, Patiala, Punjab, 147002.
Phone: 0175-5051234
Email: info@vardhmanhealthcare.com
OPD Timings: Monday to Saturday, 10:30 AM to 3:00 PM.
Services: Cardiology, Orthopedics, Obstetrics & Gynaecology, Dentistry, General Surgery, Neurology.
Insurance: We accept all major insurance providers. Please contact our billing department for more details.
"""

# Save the knowledge base to a temporary file
with open("hospital_info.txt", "w") as f:
    f.write(hospital_knowledge_base)

# Step 2: Load and process the knowledge base
loader = TextLoader("hospital_info.txt")
documents = loader.load()

# Split the documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# Step 3: Create a Vector Store (The "Retrieval" part of RAG)
# This converts the text chunks into numerical vectors for efficient search.
# We will use Ollama for local embeddings, but in production, you might use a cloud-based service.
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = Chroma.from_documents(docs, embeddings)

# Step 4: Set up the LLM (The "Generation" part of RAG)
# We will use the Ollama-based Llama 3 model. You need to have Ollama installed and have pulled the Llama 3 model locally.
# Example command: 'ollama pull llama3'
llm = Ollama(model="llama3")

# Step 5: Combine LLM and Vector Store into a RAG Pipeline
# This chain will retrieve relevant documents and pass them to the LLM for a final response.
retriever = vector_store.as_retriever()

# Create a conversation memory to remember chat history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Define the RAG chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm,
    retriever,
    memory=memory
)

# Step 6: Test the pipeline with a user query
def get_rag_response(query):
    result = qa_chain({"question": query})
    return result["answer"]

# Let's test a few queries
print(f"User: 'What are your services?'")
print(f"Bot: {get_rag_response('What are your services?')}\n")

print(f"User: 'Tell me about the heart doctors?'")
print(f"Bot: {get_rag_response('Tell me about the heart doctors?')}\n") # The bot will infer from "heart doctors" to "Cardiology"

print(f"User: 'I have an emergency, what do I do?'")
print(f"Bot: {get_rag_response('I have an emergency, what do I do?')}\n")