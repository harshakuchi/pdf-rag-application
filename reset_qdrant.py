from qdrant_client import QdrantClient

client = QdrantClient("http://localhost:6333")

if client.collection_exists("docs"):
    client.delete_collection("docs")
    print("Deleted old docs collection")

print("Done")