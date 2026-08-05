from app.config.settings import settings
from app.vectorstores.weaviate_store import WeaviateStore

store = WeaviateStore()

collection = store.client.collections.get(
    settings.WEAVIATE_COLLECTION,
)

result = collection.aggregate.over_all(
    total_count=True,
)

print(result)

store.close()