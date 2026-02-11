from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter  # Fixed import
from langchain_ollama import ChatOllama, OllamaEmbeddings  # Fixed import
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Initialize
embeddings = OllamaEmbeddings(model="mistral")  # Fixed - no warning
llm = ChatOllama(model="mistral")

# Load documents from a directory
# First, create a 'documents' folder and add some .txt files
loader = DirectoryLoader('./documents', glob="**/*.txt", loader_cls=TextLoader)
documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(documents)

# Create embeddings and store
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./chroma_db",  # Persist to disk
    collection_name="my_documents"
)

print(f"✅ Loaded {len(documents)} documents, split into {len(splits)} chunks")

# Query the loaded documents
query = input("\nAsk a question about your documents: ")
relevant_docs = vectorstore.similarity_search(query, k=3)

print(f"\n📚 Found {len(relevant_docs)} relevant chunks:\n")
for i, doc in enumerate(relevant_docs):
    print(f"Chunk {i+1}:")
    print(doc.page_content[:200] + "...\n")  # Show first 200 chars

# Ask LLM with context
context = "\n".join([doc.page_content for doc in relevant_docs])
messages = [
    SystemMessage(content=f"Use this context to answer: {context}"),
    HumanMessage(content=query)
]

print("🤖 Jarvis: ", end="", flush=True)
for chunk in llm.stream(messages):
    print(chunk.content, end="", flush=True)
print("\n")