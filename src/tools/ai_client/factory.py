from tools.ai_client.interface import AiClient
from tools.ai_client.gpt import GPTAiClient
from tools.ai_client.gemini import GeminiAiClient

DEFAULT_LLM = "gpt"


class AiClientFactory:
    """
    Factory class to create instances of different AI clients based on the client name.
    """

    @staticmethod
    def create_ai_client(self, client_name: str = DEFAULT_LLM) -> AiClient:
        """
        Creates an instance of the specified AI client based on the client name.

        :param client_name: The name of the AI client to create.
        :return: An instance of the specified AI client.
        """

        if client_name.lower() == "gpt":
            return GPTAiClient()
        elif client_name.lower() == "gemini":
            return GeminiAiClient()
        else:
            raise ValueError(f"Unsupported AI client: {client_name}")
