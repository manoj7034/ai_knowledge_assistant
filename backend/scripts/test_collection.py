from app.embeddings.service import EmbeddingService

service = EmbeddingService()

vector = service.generate_embeddings(
    ["Hello World"]
)

print(len(vector[0]))