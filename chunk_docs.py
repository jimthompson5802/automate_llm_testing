from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.document_loaders import DirectoryLoader
import faiss



# Set the directory path
docs_dir = "raw_documents"  # Create this folder in your project directory
vector_db_fp = "vector_dbs/vector_store_openai.db"

# Load all text documents from the directory
loader = DirectoryLoader(docs_dir, glob="**/*.txt")  # Loads all .txt files recursively
documents = loader.load()

# Print number of documents loaded
print(f"Loaded {len(documents)} documents from {docs_dir}/")

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)

# Create embeddings and store in vector database
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# setup vector store
vector_length = len(embeddings.embed_query("hello world"))   # compute size for embedding vector with a sample query
faiss_index = faiss.IndexFlatL2(vector_length) 
vector_store = FAISS(
    embedding_function=embeddings,
    index=faiss_index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

#
# Store chunks in the vectorstore
vector_store = FAISS.from_documents(chunks, embeddings)


vector_store.save_local(vector_db_fp)

del vector_store


vector_store = FAISS.load_local(
    vector_db_fp, embeddings, allow_dangerous_deserialization=True
)
# Retrieve chunks based on a prompt
query = "What are the considerations for extraterrestrial travel?"
relevant_chunks = vector_store.similarity_search(query, k=3)

# Print retrieved chunks
print(f"query: {query}, related material")
for i, chunk in enumerate(relevant_chunks):
    print(f"\n>>>chunk {i+1} from {chunk.metadata.get('source', 'unknown')}:")
    print(f"'{chunk.page_content}'")



# # To list all chunks in the vectorstore
# all_docs = vectorstore.get()

# # Print the number of documents
# print("Number of documents:", len(all_docs))

# # Print all chunks
# print("\nAll chunks in vectorstore:")
# for i, doc in enumerate(all_docs):
#     print(f"\n>>>chunk {i+1}: '{doc.page_content}'")


