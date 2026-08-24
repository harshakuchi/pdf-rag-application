#to connect to qdrant and search in vectorDB
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

class QdrantStorage:
    def __init__(self, url="http://localhost:6333", collection="docs", dim=1024): # dim = no of values we have inside a vector
        self.client = QdrantClient(url=url, timeout=30)
        self.collection = collection
        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )

    def upsert(self, ids, vectors, payloads): #ids list, vectors = vectorized version of dimensions = 3027 and payloads is real data which represents the info which we vectorized
        points = [PointStruct(id=ids[i], vector=vectors[i], payload=payloads[i]) for i in range(len(ids))] #this point structure is what required for qdrant
        self.client.upsert(self.collection, points=points)

    def search(self, query_vector, top_k: int = 5):
        results = self.client.query_points(
            collection_name=self.collection,
            query=query_vector,
            with_payload=True,
            limit=top_k
        )
        contexts = [] #info
        sources = set() #documents which we pulled the info from

        for r in results.points:
            payload = getattr(r, "payload", None) or {}
            text = payload.get("text", "")
            source = payload.get("source", "")
            if text:
                contexts.append(text)
                sources.add(source)

        return {"contexts": contexts, "sources": list(sources)}
      
         