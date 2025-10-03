from typing import Any, Dict

from retriever import retriever

PROMPT = """
Find recent tweets about {topic} from {location} written in {language}.
"""


class FakeAI:
    def __init__(self):
        print("Initializing FakeAI...")

    async def __retrieve(self, query: str) -> Dict[str, Any]:
        results = retriever.similarity_search(query, k=1)
        if not results:
            return {"tweet": None, "author": None}

        top_result = results[0]
        metadata = top_result.metadata or {}
        author = metadata.get("author")
        if isinstance(author, dict):
            name = author.get("name")
            email = author.get("email")
        else:
            name = metadata.get("author_name")
            email = metadata.get("author_email")

        author_info = {"name": (name or ""), "email": (email or "")}
        tweet_text = top_result.page_content or ""
        return {"tweet": tweet_text, "author": author_info}

    async def generate_response(self, context: Dict[str, Any]) -> Dict[str, Any]:
        query = PROMPT.format(
            topic=context["topic"],
            location=context["location"],
            language=context["language"],
        )
        return await self.__retrieve(query)
