import logging
from typing import Any

from openai import AsyncOpenAI as OpenAI
from openai.types.chat import ChatCompletionMessageParam

from tools.ai_client.interface import AiClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GPTAiClient(AiClient):

    def __init__(self, openai_api_key: str):
        self.ai_client = OpenAI(api_key=openai_api_key)
        self.model = "gpt-4-0125-preview"

    async def send_json_chat(self, prompt: Any, sys_propmt: Any) -> str:
        msg: ChatCompletionMessageParam = {"role": "user", "content": prompt}
        messages = [msg]
        completion = await self.ai_client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.9,
        )
        json_string = completion.choices[0].message.content
        if not json_string:
            logger.error(f"Prompt: {prompt}")
            raise Exception("Failed to generate response")
        return json_string

    async def generate_code(self, prompt: str) -> str:
        completion = await self.ai_client.completions.create(
            model=self.model,
            prompt=prompt,
            temperature=0.9,
        )
        return completion.choices[0].text
