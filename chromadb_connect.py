import chromadb
import importlib.metadata

print("ChromaDB version:", importlib.metadata.version("chromadb"))

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="personal_collection")

print("Client:", chroma_client)
print("Collection:", collection.name)