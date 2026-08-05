import weaviate
from weaviate.classes.config import Configure, Property, DataType

from app.config.settings import settings


class WeaviateStore:

    def __init__(self):

        self.client = weaviate.connect_to_local(
            host=settings.WEAVIATE_HOST,
            port=settings.WEAVIATE_HTTP_PORT,
            grpc_port=settings.WEAVIATE_GRPC_PORT,
        )

    def create_collection(self):

        if self.client.collections.exists(
            settings.WEAVIATE_COLLECTION,
        ):
            return

        self.client.collections.create(
            name=settings.WEAVIATE_COLLECTION,

            vector_config=Configure.Vectors.self_provided(),

            properties=[
                Property(
                    name="document_id",
                    data_type=DataType.UUID,
                ),
                Property(
                    name="owner_id",
                    data_type=DataType.UUID,
                ),
                Property(
                    name="chunk_index",
                    data_type=DataType.INT,
                ),
                Property(
                    name="content",
                    data_type=DataType.TEXT,
                ),
                Property(
                    name="original_filename",
                    data_type=DataType.TEXT,
                ),
                Property(
                    name="content_type",
                    data_type=DataType.TEXT,
                ),
            ],
        )

        collection = self.client.collections.get(
            settings.WEAVIATE_COLLECTION,
            )
        print(collection.config.get())


    def close(self) -> None:
        self.client.close()