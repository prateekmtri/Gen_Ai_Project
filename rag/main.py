from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from utils.pdf_parser import extract_text_from_pdf
from utils.embedding_helper import get_embedding_model
import os

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

embedding = get_embedding_model()
VECTOR_DIR = "vector_db"

if not os.path.exists(VECTOR_DIR):
    os.makedirs(VECTOR_DIR)

# Upload and process file
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(await file.read())
    else:
        text = (await file.read()).decode("utf-8")

    doc = Document(page_content=text)
    vectorstore = Chroma.from_documents([doc], embedding=embedding, persist_directory=VECTOR_DIR)
    vectorstore.persist()
    return {"message": "✅ Document uploaded and processed"}

# Search endpoint
@app.post("/search")
async def search_question(question: str = Form(...)):
    vectorstore = Chroma(persist_directory=VECTOR_DIR, embedding_function=embedding)
    results = vectorstore.similarity_search_with_score(question, k=3)
    response = [{"score": float(score), "content": doc.page_content} for doc, score in results]
    return {"results": response}
