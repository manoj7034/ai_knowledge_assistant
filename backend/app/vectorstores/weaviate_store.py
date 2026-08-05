import weaviate

from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.data import DataObject
from weaviate.classes.query import Filter
from typing import Any

from app.config.settings import settings
from app.models.document import Document
from app.models.document_chunk import DocumentChunk


class WeaviateStore:

    def __init__(self):
        self.client = weaviate.connect_to_local(
            host=settings.WEAVIATE_HOST,
            port=settings.WEAVIATE_HTTP_PORT,
            grpc_port=settings.WEAVIATE_GRPC_PORT,
        )

    def create_collection(self) -> None:

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

    def index_chunks(
        self,
        *,
        document: Document,
        chunks: list[DocumentChunk],
        vectors: list[list[float]],
    ) -> None:

        if not chunks:
            return

        if len(chunks) != len(vectors):
            raise ValueError(
                "Number of chunks and vectors must match."
            )

        collection = self.client.collections.get(
            settings.WEAVIATE_COLLECTION,
        )

        objects = []

        for chunk, vector in zip(chunks, vectors):

            objects.append(
                DataObject(
                    uuid=str(chunk.id),

                    properties={
                        "document_id": str(document.id),
                        "owner_id": str(document.owner_id),
                        "chunk_index": chunk.chunk_index,
                        "content": chunk.content,
                        "original_filename": document.original_filename,
                        "content_type": document.content_type,
                    },

                    vector=vector,
                )
            )

        collection.data.insert_many(objects)


    def search(
            self, 
            *, 
            query_vector: list[float], 
            owner_id: str, 
            limit: int = 5,
            ) -> list[dict[str, Any]]:

        collection = self.client.collections.get(
        settings.WEAVIATE_COLLECTION,
    )

        response = collection.query.near_vector(
            near_vector=query_vector,
            limit=limit,
            filters=Filter.by_property("owner_id").equal(owner_id),
            return_metadata=["distance"],
        )

        return [
            {
                "id": str(obj.uuid),
                "distance": obj.metadata.distance,
                "properties": obj.properties,
            }
            for obj in response.objects
        ]


    def close(self) -> None:
        self.client.close()