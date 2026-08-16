class RAGPromptBuilder:
    """
    Builds a grounded RAG prompt using the user's
    question and retrieved context.
    """

    def build(
        self,
        *,
        query: str,
        context: str,
    ) -> str:

        return f"""
You are an enterprise knowledge assistant.

Answer the user's question using ONLY the information
provided in the context below.

Rules:
1. Do not invent or assume information.
2. If the context does not contain enough information
   to answer the question, say that you do not have
   enough information.
3. Give a concise and direct answer.
4. Use the source information provided in the context
   when relevant.

Context:
--------------------
{context}
--------------------

User Question:
{query}

Answer:
""".strip()