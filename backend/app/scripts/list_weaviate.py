from app.config.settings import settings
from app.vectorstores.weaviate_store import WeaviateStore

store = WeaviateStore()

collection = store.client.collections.get(
    settings.WEAVIATE_COLLECTION,
)

print("=" * 80)

for obj in collection.iterator():
    print(obj.properties)

print("=" * 80)

store.close()