#use llamaindex to load pdfs and embed them
import voyageai
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from dotenv import load_dotenv
import os

load_dotenv()

client = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))

EMBED_MODEL = "voyage-4-lite"
EMBED_DIM = 1024

splitter = SentenceSplitter(chunk_size=1000, chunk_overlap=200)

def load_and_chunk_pdf(path: str):
    docs = PDFReader().load_data(file=path)
    texts = [d.text for d in docs if getattr(d, "text", None)] #extract text from the doc, if it has some text
    chunks = []
    for t in texts:
        chunks.extend(splitter.split_text(t))
    return chunks

def embed_texts(texts: list[str]) -> list[list[float]]:
    response = client.embed(
        texts,
        model=EMBED_MODEL,
        input_type="document"
    )
    return response.embeddings
    