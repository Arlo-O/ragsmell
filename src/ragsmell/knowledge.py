"""Declarative domain vocabulary used by the detectors."""

from __future__ import annotations

import re

PROVIDER_SDKS = frozenset({"openai", "anthropic", "cohere", "google.generativeai", "mistralai", "groq", "ollama"})
LLM_CLASSES = frozenset({"ChatOpenAI", "OpenAI", "AzureChatOpenAI", "ChatAnthropic", "Anthropic", "ChatGoogleGenerativeAI", "ChatOllama", "ChatMistralAI", "HuggingFaceHub"})
GENERATION_CALLS = frozenset({"invoke", "ainvoke", "stream", "astream", "predict", "generate", "chat.completions.create", "messages.create", "completions.create", "complete", "chat", "generate_content"})
RETRIEVAL_CALLS = frozenset({"similarity_search", "similarity_search_with_score", "get_relevant_documents", "as_retriever", "retrieve", "query_engine.query"})
VECTOR_TYPES = frozenset({"Chroma", "Qdrant", "Pinecone", "Weaviate", "FAISS", "Milvus"})
WEB_FRAMEWORKS = frozenset({"FastAPI", "Flask", "Streamlit", "Gradio", "Django"})
PROMPT_TYPES = frozenset({"PromptTemplate", "ChatPromptTemplate", "SystemMessage", "HumanMessage"})
PROMPT_HINTS = frozenset({"prompt", "template", "system", "instruction"})
MODEL_NAME_REGEX = re.compile(r"(?:gpt|claude|gemini|mistral|llama|mixtral|command|o[1-9])[-_a-zA-Z0-9.]*", re.IGNORECASE)


def is_generation_call(name: str) -> bool:
    """Recognize calls from the curated list, including dotted suffixes."""
    return name in GENERATION_CALLS or any(name.endswith(f".{item}") for item in GENERATION_CALLS if "." not in item)


def is_retrieval_call(name: str) -> bool:
    """Recognize retrieval calls without treating generic query/search as critical."""
    return name in RETRIEVAL_CALLS or any(name.endswith(f".{item}") for item in RETRIEVAL_CALLS)
