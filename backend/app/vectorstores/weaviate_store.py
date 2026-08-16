import weaviate
from uuid import UUID

from weaviate.classes.config import Configure, Property, DataType
from weaviate.classes.data import DataObject
from weaviate.classes.query import Filter, MetadataQuery
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

    # ---------------------------------------------------------
    # Metadata Filter
    # ---------------------------------------------------------

    def _build_filter(
        self,
        *,
        owner_id: str,
        document_id: UUID | None = None,
        content_type: str | None = None,
        filename: str | None = None,
    ):
        """
        Build a Weaviate filter.
        owner_id is mandatory and always comes from the authenticated user.
        Additional filters are optional.
        """

        filters = [
            Filter.by_property(
                "owner_id"
            ).equal(UUID(owner_id))
        ]

        if document_id is not None:

            filters.append(
                Filter.by_property(
                    "document_id"
                ).equal(document_id)
            )

        if content_type is not None:

            filters.append(
                Filter.by_property(
                    "content_type"
                ).equal(content_type)
            )

        if filename is not None:

            filters.append(
                Filter.by_property(
                    "original_filename"
                ).equal(filename)
            )

        combined_filter = filters[0]

        for current_filter in filters[1:]:

            combined_filter = (
                combined_filter & current_filter
            )

        return combined_filter

    # ---------------------------------------------------------
    # Semantic Search
    # ---------------------------------------------------------

    def semantic_search(
        self,
        *,
        query_vector: list[float],
        owner_id: str,
        limit: int = 5,
        document_id: UUID | None = None,
        content_type: str | None = None,
        filename: str | None = None,
        
    ) -> list[dict[str, Any]]:

        # print("\n========== SEMANTIC DEBUG ==========")

        # print(
        #     "Query vector dimension:",
        #     len(query_vector),
        # )

        # print(
        #     "First 5 vector values:",
        #     query_vector[:5],
        # )

        # print(
        #     "Owner ID:",
        #     owner_id,
        # )

        # self.debug_owner_ids()

        collection = self.client.collections.get(
            settings.WEAVIATE_COLLECTION,
        )

        filters = self._build_filter(
            owner_id=owner_id,
            document_id=document_id,
            content_type=content_type,
            filename=filename,
        )

        response = collection.query.near_vector(
            near_vector=query_vector,
            limit=limit,
            filters=filters,
            return_metadata=["distance"],
        )

        results: list[dict[str, Any]] = []

        for obj in response.objects:

            distance = obj.metadata.distance

            if distance is None:
                score = 0.0
            else:
                score = round(
                    1.0 - distance,
                    4,
                )

            results.append(
                {
                    "chunk_id": str(obj.uuid),
                    "document_id": obj.properties["document_id"],
                    "filename": obj.properties[
                        "original_filename"
                    ],
                    "content": obj.properties["content"],
                    "chunk_index": obj.properties[
                        "chunk_index"
                    ],
                    "content_type": obj.properties[
                        "content_type"
                    ],
                    "score": score,
                }
            )

        return results


    # def debug_owner_ids(self) -> None:

    #     collection = self.client.collections.get(
    #         settings.WEAVIATE_COLLECTION,
    #     )

    #     response = collection.query.fetch_objects(
    #         limit=20,
    #     )

    #     print("\n========== OWNER ID DEBUG ==========")

    #     for obj in response.objects:

    #         print(
    #             "UUID:",
    #             obj.uuid,
    #         )

    #         print(
    #             "Owner ID:",
    #             obj.properties.get("owner_id"),
    #         )

    #         print(
    #             "Owner ID type:",
    #             type(obj.properties.get("owner_id")),
    #         )

    #         print("------------------------------------")

    # ---------------------------------------------------------
    # BM25 Keyword Search
    # ---------------------------------------------------------

    def keyword_search(
        self,
        *,
        query: str,
        owner_id: str,
        limit: int = 5,
        document_id: UUID | None = None,
        content_type: str | None = None,
        filename: str | None = None,
    ) -> list[dict[str, Any]]:

        collection = self.client.collections.get(
            settings.WEAVIATE_COLLECTION,
        )

        filters = self._build_filter(
            owner_id=owner_id,
            document_id=document_id,
            content_type=content_type,
            filename=filename,
        )

        response = collection.query.bm25(
            query=query,
            query_properties=["content"],
            filters=filters,
            limit=limit,
            return_metadata=MetadataQuery(
                score=True,
            ),
        )

        return [
            {
                "chunk_id": str(obj.uuid),
                "document_id": obj.properties[
                    "document_id"
                ],
                "filename": obj.properties[
                    "original_filename"
                ],
                "content": obj.properties[
                    "content"
                ],
                "chunk_index": obj.properties[
                    "chunk_index"
                ],
                "content_type": obj.properties[
                    "content_type"
                ],
                "score": float(
                    obj.metadata.score or 0
                ),
            }
            for obj in response.objects
        ]

    def close(self) -> None:
        self.client.close()

