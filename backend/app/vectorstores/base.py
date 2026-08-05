from abc import ABC, abstractmethod


class VectorStore(ABC):

    @abstractmethod
    def index_chunks(
        self,
        chunks: list[dict],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query: str,
        limit: int = 5,
    ):
        raise NotImplementedError

    @abstractmethod
    def create_collection(self) -> None:
        pass