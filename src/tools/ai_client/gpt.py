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
        await self.log_req_res_to_file(prompt, json_string)
        return json_string

    async def generate_code(self, prompt: str) -> str:
        completion = await self.ai_client.chat.completions.create(
            model=self.model,
            messages=[{
                "role": "user",
                "content": prompt
            }],
            temperature=0.9,
        )
        res = completion.choices[0].message.content
        await self.log_req_res_to_file(prompt, res)
        return res
