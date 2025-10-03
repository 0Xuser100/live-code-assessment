from langchain_community.document_loaders import JSONLoader
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.vectorstores import FAISS


def metadata_func(record: dict, metadata: dict) -> dict:
    author = record.get("author", {}) or {}
    metadata["author"] = author
    metadata["author_name"] = author.get("name")
    metadata["author_email"] = author.get("email")
    return metadata


docs_loader = JSONLoader(
    file_path="data/tweets.json",
    jq_schema=".[]",
    content_key="tweet",
    metadata_func=metadata_func,
)

tweets = docs_loader.load()

embeddings = FakeEmbeddings(size=768)

retriever = FAISS.from_documents(tweets, embeddings)
