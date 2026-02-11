from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Fixed import
from langchain_core.documents import Document

# Initialize Ollama LLM and Embeddings
llm = ChatOllama(model="mistral")
embeddings = OllamaEmbeddings(model="mistral")  # Using Mistral for embeddings

# Sample documents (your knowledge base)
documents = [
    Document(page_content="Pramod is an experienced developer who worked with PHP, Node.js, and NestJS before learning Python.", metadata={"source": "bio"}),
    Document(page_content="Jarvis is Pramod's AI assistant built with LangChain and Mistral AI.", metadata={"source": "assistant_info"}),
    Document(page_content="Python uses indentation for code blocks instead of curly braces like PHP and JavaScript.", metadata={"source": "python_basics"}),
    Document(page_content="LangChain is a framework for developing applications powered by language models.", metadata={"source": "langchain_info"}),
]

# Split documents into chunks (important for large texts)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
splits = text_splitter.split_documents(documents)

# Create ChromaDB vector store
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    collection_name="pramod_knowledge_base"
)

print("✅ Vector store created with", len(splits), "document chunks\n")

# Query the knowledge base
query = "Who is Pramod?"
docs = vectorstore.similarity_search(query, k=2)  # Get top 2 relevant docs

print(f"📚 Retrieved {len(docs)} relevant documents for: '{query}'\n")
for i, doc in enumerate(docs):
    print(f"Doc {i+1}: {doc.page_content}\n")

# Use retrieved context in conversation
context = "\n".join([doc.page_content for doc in docs])

messages = [
    SystemMessage(content=f"You are Jarvis. Use this context to answer: {context}"),
    HumanMessage(content=query)
]

response = llm.invoke(messages)
print("🤖 Jarvis:", response.content)