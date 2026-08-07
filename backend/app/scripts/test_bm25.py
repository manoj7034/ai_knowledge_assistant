from app.vectorstores.weaviate_store import WeaviateStore

store = WeaviateStore()

results = store.keyword_search(
    query="Python FastAPI",
    owner_id="b6e95f4b-10de-4eda-9286-47ace0fa5b39",
)

for result in results:
    print("-" * 80)
    print(result["filename"])
    print(result["score"])
    print(result["content"][:250])

store.close()