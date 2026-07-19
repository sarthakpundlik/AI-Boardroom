"""
AI Boardroom — Context Builder
Formats retrieved chunks into agent context blocks.
"""

from __future__ import annotations


def build_agent_context(retrieved_docs: list[dict]) -> str:
    """Format documents into a single context string for LLM prompts."""
    if not retrieved_docs:
        return "No relevant documents found."
        
    context_parts = []
    for i, doc in enumerate(retrieved_docs, 1):
        filename = doc["metadata"].get("filename", "Unknown File")
        content = doc["content"]
        
        part = f"--- Document {i}: {filename} ---\n{content}\n"
        context_parts.append(part)
        
    return "\n".join(context_parts)
