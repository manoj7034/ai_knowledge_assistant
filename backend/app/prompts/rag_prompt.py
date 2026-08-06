SYSTEM_PROMPT = """
You are an Enterprise AI Knowledge Assistant.

Answer ONLY from the supplied context.

If the answer cannot be found inside the context,
reply exactly:

"I couldn't find that information in the uploaded documents."

Never make up facts.

Always answer professionally.

At the end of your answer include:

Sources:
- filename
"""


def build_rag_prompt(question: str, contexts: list[dict],) -> str:

    context_text = ""

    for index, item in enumerate(contexts, start=1):

        context_text += (
            f"""Context {index} 
            Filename: 
            {item["filename"]}
            Content:
            {item["content"]}
            -------------------------
            """
        )

    return f"""
{SYSTEM_PROMPT}

Context

{context_text}

Question

{question}

Answer:
"""