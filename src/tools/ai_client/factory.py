import os
from typing import Optional
from tools.ai_client.interface import AiClient
from tools.ai_client.gpt import GPTAiClient
from tools.ai_client.gemini import GeminiAiClient


def get_ai_client(client_name: Optional[str] = None) -> AiClient:
    """
    Factory function to create and return an AI client based on the client name provided.
    Args:
        client_name (Optional[str]): The name of the AI client to create.
    Returns:
        AiClient: An instance of the AI client.
    Raises:
        ValueError: If the client name is not supported or no API key or credentials are found.
    """

    if not client_name:
        open_api_key = os.getenv("OPENAI_API_KEY")
        google_app_cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if google_app_cred_path:
            print("Using Gemini AI client with Google credentials: ",
                  google_app_cred_path)
            return GeminiAiClient()
        elif open_api_key:
            return GPTAiClient(open_api_key)
        else:
            raise ValueError("No API key or credentials found for AI client.")
    if client_name.lower() == "gpt":
        return GPTAiClient()
    elif client_name.lower() == "gemini":
        return GeminiAiClient()
    else:
        raise ValueError(f"Unsupported AI client: {client_name}")
