import os
from typing import Optional
from tools.ai_client.interface import AiClient
from tools.ai_client.gpt import GPTAiClient
from tools.ai_client.gemini import GeminiAiClient


class AiClientFactory:
    """
    Factory class to create instances of different AI clients based on the client name.
    """

    @staticmethod
    def create_ai_client(self, client_name: Optional[str]) -> AiClient:
        """
        Creates an instance of the specified AI client based on the client name.

        :param client_name: The name of the AI client to create.
        :return: An instance of the specified AI client.
        """
        if not client_name:
            open_api_key = os.getenv("OPENAI_API_KEY")
            google_app_cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
            if open_api_key:
                return GPTAiClient(open_api_key)
            elif google_app_cred_path:
                return GeminiAiClient(google_app_cred_path)
            else:
                raise ValueError(
                    "No API key or credentials found for AI client.")
        if client_name.lower() == "gpt":
            return GPTAiClient()
        elif client_name.lower() == "gemini":
            return GeminiAiClient()
        else:
            raise ValueError(f"Unsupported AI client: {client_name}")
