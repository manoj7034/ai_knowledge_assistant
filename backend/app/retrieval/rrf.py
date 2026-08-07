from collections.abc import Iterable
from typing import Any


class ReciprocalRankFusion:
    """
    Implements Reciprocal Rank Fusion (RRF).

    Reference:
    https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf

    RRF Score = Σ (1 / (k + rank))

    where:
        k = 60 (recommended default)
        rank starts from 1
    """

    def __init__(
        self,
        k: int = 60,
    ) -> None:
        self.k = k

    def fuse(
        self,
        *result_lists: Iterable[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Fuse multiple ranked result lists into one.

        Parameters
        ----------
        result_lists:
            One or more ranked search result lists.

        Returns
        -------
        list[dict]
            Results sorted by fused RRF score.
        """

        scores: dict[str, float] = {}
        objects: dict[str, dict[str, Any]] = {}

        for results in result_lists:

            for rank, result in enumerate(results, start=1):

                chunk_id = result["chunk_id"]

                score = 1.0 / (self.k + rank)

                scores[chunk_id] = (
                    scores.get(chunk_id, 0.0) + score
                )

                # Keep the first copy of the object.
                if chunk_id not in objects:
                    objects[chunk_id] = result.copy()

        fused_results: list[dict[str, Any]] = []

        for chunk_id, result in objects.items():

            item = result.copy()

            item["rrf_score"] = scores[chunk_id]

            fused_results.append(item)

        fused_results.sort(
            key=lambda x: x["rrf_score"],
            reverse=True,
        )

        return fused_results