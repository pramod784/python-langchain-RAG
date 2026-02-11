from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

# Initialize
llm = ChatOllama(model="mistral")
embeddings = OllamaEmbeddings(model="mistral")

# Check if vector store exists
persist_dir = "./chroma_storage"
if os.path.exists(persist_dir):
    print("📂 Loading existing knowledge base...")
    vectorstore = Chroma(
        collection_name="jarvis_docs",
        embedding_function=embeddings,
        persist_directory=persist_dir
    )
    print("✅ Knowledge base loaded!\n")
else:
    print("📚 Creating new knowledge base from documents...")
    
    # Load documents
    loader = DirectoryLoader('./documents', glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()
    
    # Split
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    
    # Create and persist
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name="jarvis_docs"
    )
    print(f"✅ Created knowledge base with {len(splits)} chunks!\n")

# Conversational RAG
print("🤖 Jarvis with RAG: Ready! (type 'exit' to quit, 'add' to add more docs)\n")

messages = [SystemMessage(content="You are Jarvis, Pramod's AI assistant.")]

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("🤖 Jarvis: Goodbye!")
        break
    
    if user_input.lower() == 'add':
        new_text = input("Enter text to add to knowledge base: ")
        vectorstore.add_texts([new_text])
        print("✅ Added to knowledge base!\n")
        continue
    
    if not user_input:
        continue
    
    # Retrieve relevant context
    relevant_docs = vectorstore.similarity_search(user_input, k=3)
    context = "\n".join([doc.page_content for doc in relevant_docs])
    
    # Build message with context
    current_query = f"Context: {context}\n\nQuestion: {user_input}"
    messages.append(HumanMessage(content=current_query))
    
    # Stream response
    print("🤖 Jarvis: ", end="", flush=True)
    full_response = ""
    for chunk in llm.stream(messages):
        print(chunk.content, end="", flush=True)
        full_response += chunk.content
    print("\n")
    
    # Save to history
    messages[-1] = HumanMessage(content=user_input)
    messages.append(AIMessage(content=full_response))