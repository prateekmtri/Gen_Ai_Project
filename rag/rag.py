from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

# 1. Load API Key from .env
load_dotenv()
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# 2. Create documents
docs = [
    Document(page_content="APJ Abdul Kalam was the 11th President of India."),
    Document(page_content="He was known as the Missile Man of India."),
    Document(page_content="He worked at DRDO and ISRO."),
    Document(page_content="He also wrote books like Wings of Fire."),
]

# 3. Load HF Embeddings (new way)
embedding = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
)

# 4. Create vector DB
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embedding,
    persist_directory="vector_db_cloud"
)

# 5. Save
vectorstore.persist()
print("✅ Vector DB created successfully using latest HuggingFace embeddings.")




# Load the same vector DB
vectorstore = Chroma(
    persist_directory="vector_db_cloud",
    embedding_function=embedding
)

# Ask a query
query = "Missile Man of India kaun hai?"

# Perform similarity search with scores
results = vectorstore.similarity_search_with_score(query, k=3)

# Print answers with similarity scores
for i, (doc, score) in enumerate(results):
    print(f"\n📄 Result {i+1}:")
    print(f"🔢 Score: {score:.4f}")
    print(f"📄 Content: {doc.page_content}")






# query = "Missile Man of India kaun hai?"

# # Get embedding vector of the query
# query_vector = embedding.embed_query(query)

# # Print the embedding vector
# print("\n🔢 Query Embedding Vector:\n")
# print(query_vector)
# print(f"\n🧮 Vector Length: {len(query_vector)}")











docs_texts = [doc.page_content for doc in docs]

# Get embedding vectors for all documents
doc_vectors = embedding.embed_documents(docs_texts)

# Print all document vectors
for i, vec in enumerate(doc_vectors):
    print(f"\n📄 Document {i+1} Embedding Vector (length {len(vec)}):\n")
    print(vec)
