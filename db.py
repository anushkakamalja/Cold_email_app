import chromadb

client = chromadb.Client()

collection = client.create_collection("my_collection")

collection.add(
    ids=["1", "2", "3"],
    documents=["DocA", "DocB", "DocC"],
)

# all_docs = collection.get()

results = collection.query(
    query_texts=["First letter"],
    n_results=3,
)

print(results)