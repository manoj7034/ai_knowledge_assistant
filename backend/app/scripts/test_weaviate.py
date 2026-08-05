from app.vectorstores.weaviate_store import WeaviateStore

store = WeaviateStore()

store.create_collection()

print("Connected successfully!")

store.close()