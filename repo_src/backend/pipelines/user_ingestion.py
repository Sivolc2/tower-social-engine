"""
Ingestion & Processing Core (Component A)
Parses raw text files and extracts structured user profile data using LLM
"""
import json
import os
from typing import Dict, Any
from pathlib import Path

from repo_src.backend.llm_chat.llm_interface import ask_llm


EXTRACTION_SYSTEM_MESSAGE = """You are a data extraction assistant for a user profile system.
Your task is to analyze interview transcripts or user profile documents and extract structured information.

You must return ONLY a valid JSON object with the following schema:
{
    "user_id": "a stable, machine-readable identifier (e.g., lowercase name with underscores)",
    "name": "the person's full name",
    "bio": "a concise one-line summary of who they are (50-100 characters)",
    "wiki_content": "a comprehensive markdown-formatted document containing all descriptive information about the person including: background, skills, interests, projects, experiences, personality traits, goals, and any other relevant details. This should be well-organized with headers and bullet points where appropriate."
}

IMPORTANT GUIDELINES:
1. The wiki_content field is the most important - consolidate ALL descriptive text here
2. Format wiki_content as clean Markdown with headers (##, ###) and bullet points
3. Be thorough - include everything that would help understand this person
4. The user_id should be stable and machine-readable (e.g., "jane_doe", "john_smith")
5. Keep the bio very concise - it's just a tagline
6. Return ONLY valid JSON, no additional text or explanation"""


EXTRACTION_PROMPT_TEMPLATE = """Please analyze the following text and extract user profile information according to the schema:

TEXT TO ANALYZE:
{file_content}

Return the extracted information as a JSON object."""


async def process_file(file_path: str) -> Dict[str, Any]:
    """
    Process a text file and extract user profile information using LLM.

    Args:
        file_path: Path to the text file to process

    Returns:
        Dictionary containing extracted user profile data

    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the LLM response is not valid JSON
    """
    # Read the file
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path_obj, 'r', encoding='utf-8') as f:
        file_content = f.read()

    # Use LLM to extract information
    prompt = EXTRACTION_PROMPT_TEMPLATE.format(file_content=file_content)

    llm_response = await ask_llm(
        prompt_text=prompt,
        system_message=EXTRACTION_SYSTEM_MESSAGE,
        model_override=None,  # Use default model
        max_tokens=4096,  # More tokens for comprehensive wiki_content
        temperature=0.3  # Lower temperature for more consistent extraction
    )

    # Parse the JSON response
    try:
        # Clean up the response in case there's any wrapper text
        response_text = llm_response.strip()

        # Try to extract JSON if it's wrapped in markdown code blocks
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            response_text = response_text[start:end].strip()
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            response_text = response_text[start:end].strip()

        user_data = json.loads(response_text)

        # Validate required fields
        required_fields = ["user_id", "name"]
        for field in required_fields:
            if field not in user_data:
                raise ValueError(f"Missing required field in LLM response: {field}")

        return user_data

    except json.JSONDecodeError as e:
        print(f"Error parsing LLM response as JSON: {e}")
        print(f"LLM Response was: {llm_response}")
        raise ValueError(f"LLM did not return valid JSON. Response: {llm_response[:200]}...")


def process_file_sync(file_path: str) -> Dict[str, Any]:
    """
    Synchronous wrapper for process_file for easier CLI usage.

    Args:
        file_path: Path to the text file to process

    Returns:
        Dictionary containing extracted user profile data
    """
    import asyncio
    return asyncio.run(process_file(file_path))
