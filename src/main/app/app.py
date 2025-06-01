from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_qdrant import QdrantVectorStore
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from pathlib import Path
import qdrant_client
import shutil
import tempfile

from qdrant_client.http.models import VectorParams, Distance

app = FastAPI()
COLLECTION_NAME = "rag_documents"

qdrant_client = qdrant_client.QdrantClient(
    url="http://localhost:6333",
)

# Embeddings
embedding = OllamaEmbeddings(model="nomic-embed-text")

embedding_dim = 768

if not qdrant_client.collection_exists(COLLECTION_NAME):
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=embedding_dim,
            distance=Distance.COSINE
        ),
    )

vectorstore = QdrantVectorStore(
    client=qdrant_client,
    collection_name=COLLECTION_NAME,
    embedding=embedding
)

llm = OllamaLLM(model="mistral")

retriever = vectorstore.as_retriever()

qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)


# When splitting docs, add source metadata (inside parse_file)
def parse_file(file_path: Path) -> list[Document]:
    if file_path.suffix.lower() in [".md", ".puml"]:
        loader = TextLoader(str(file_path), encoding="utf-8")
        docs = loader.load()
        split_docs = splitter.split_documents(docs)
        # Add file name to each document's metadata
        for d in split_docs:
            d.metadata["source"] = file_path.name
        return split_docs
    else:
        raise ValueError(f"Unsupported file type: {file_path.suffix}")


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload .md or .puml file and index its content."""
    if not file.filename.endswith((".md", ".puml")):
        raise HTTPException(status_code=400, detail="Only .md and .puml files are supported.")

    with tempfile.TemporaryDirectory() as tmpdir:
        temp_file_path = Path(tmpdir) / file.filename
        with open(temp_file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        try:
            docs = parse_file(temp_file_path)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        vectorstore.add_documents(docs)

    return JSONResponse(content={"status": "ok", "indexed_docs": len(docs)})


# Modify /query to get documents with answer
@app.get("/query")
async def query(q: str):
    if not q:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # Use call method to get docs + answer
    chain_response = qa.invoke({"query": q})

    # Extract answer and source docs
    answer = chain_response["result"]
    docs = chain_response.get("source_documents", [])  # This key depends on chain implementation

    # Get unique filenames from docs
    sources = list({doc.metadata.get("source", "unknown") for doc in docs})

    return JSONResponse(content={
        "response": answer,
        "sources": sources,
    })
