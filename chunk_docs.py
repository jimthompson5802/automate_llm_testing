from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import SQLiteVec
from langchain_community.document_loaders import DirectoryLoader
import sqlite3



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

# Initialize SQLite database
conn = sqlite3.connect(vector_db_fp)
conn.enable_load_extension(True)
conn.load_extension("./venv/lib/python3.12/site-packages/sqlite_vec/vec0")  # Make sure the SQLite vector extension is installed

# Create vector store
vector_store = SQLiteVec(
    "documents",
    embedding=embeddings,
    connection=conn,
)

# vectorstore = SQLiteVec.from_documents(
#     documents=chunks,
#     embedding=embeddings,
#     connection=conn,
#     table_name="documents",
#     db_file=vector_db_fp,
# )

# Store chunks in the vectorstore
vector_store.from_documents(chunks, embeddings)

conn.close()


# Connect to the database
# Initialize SQLite database
conn = sqlite3.connect(vector_db_fp)
conn.enable_load_extension(True)
conn.load_extension("./venv/lib/python3.12/site-packages/sqlite_vec/vec0")  # Make sure the SQLite vector extension is installed

vectorstore = SQLiteVec(
    "documents",
    embedding=embeddings,
    connection=conn,
)

cursor = conn.cursor()
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
print("\nTables in database:")
for table in tables:
    print(f"- {table[0]}")
    schema = cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table[0]}'").fetchone()
    print(f"Schema: {schema[0]}\n")

# Retrieve chunks based on a prompt
query = "What are the considerations for extraterrestrial travel?"
relevant_chunks = vectorstore.similarity_search(query, k=3)

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

conn.close()
