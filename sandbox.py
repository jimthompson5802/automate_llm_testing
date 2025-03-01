from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader

# Load and chunk documents
loader = TextLoader("document.txt")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)

# Create embeddings and store in vector database
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = FAISS.from_documents(chunks, embeddings)

# Retrieve chunks based on a prompt
query = "What are the considerations for extraterrestrial travel?"
relevant_chunks = vectorstore.similarity_search(query, k=3)

# Print retrieved chunks
print(f"query: {query}, related materail")
for i, chunk in enumerate(relevant_chunks):
    print(f"\n\n>>>chunk {i+1}: '{chunk.page_content}'")


# To list all chunks in the vectorstore
all_docs = list(vectorstore.docstore._dict)

# Print the number of documents
print("Number of documents:", len(all_docs))


# Print all chunks
print("\nAll chunks in vectorstore:")
for doc in vectorstore.get_by_ids(all_docs):
    print(f"\n>>>chunk {doc.id}: '{doc.page_content}'")