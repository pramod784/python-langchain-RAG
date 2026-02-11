from langchain_ollama import ChatOllama, OllamaEmbeddings  # Fixed import
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.documents import Document

# Initialize
llm = ChatOllama(model="mistral")
embeddings = OllamaEmbeddings(model="mistral")  # Fixed - no warning

# Your knowledge base
documents = [
    Document(page_content="Pramod is learning Python after years of PHP and Node.js development."),
    Document(page_content="Jarvis can answer questions using RAG (Retrieval-Augmented Generation)."),
    Document(page_content="ChromaDB is a vector database for storing embeddings."),
    Document(page_content="LangChain helps build LLM applications with chains and agents."),
    Document(page_content="Ollama allows you to run LLMs locally without API costs."),
    Document(page_content="Vector embeddings convert text into numerical representations that capture semantic meaning."),
]

# Create vector store
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="jarvis_knowledge"
)

print("🤖 Jarvis with RAG: Ready! (type 'exit' to quit)\n")

messages = [
    SystemMessage(content="Your name is Jarvis. You are Pramod's assistant. Use the provided context to answer questions accurately.")
]

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() in ['exit', 'quit', 'bye']:
        print("🤖 Jarvis: Goodbye!")
        break
    
    if not user_input:
        continue
    
    # RAG: Retrieve relevant documents
    relevant_docs = vectorstore.similarity_search(user_input, k=2)
    context = "\n".join([doc.page_content for doc in relevant_docs])
    
    # Create message with context
    current_query = f"Context: {context}\n\nQuestion: {user_input}"
    messages.append(HumanMessage(content=current_query))
    
    # Stream response
    print("🤖 Jarvis: ", end="", flush=True)
    full_response = ""
    for chunk in llm.stream(messages):
        print(chunk.content, end="", flush=True)
        full_response += chunk.content
    print("\n")
    
    # Add only the original question and response to history (not the context)
    messages[-1] = HumanMessage(content=user_input)  # Replace with original question
    messages.append(AIMessage(content=full_response))