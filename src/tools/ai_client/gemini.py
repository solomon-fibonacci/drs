import logging
from typing import Any

import vertexai
from vertexai.preview.generative_models import GenerativeModel
from tools.ai_client.interface import AiClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiAiClient(AiClient):

    def __init__(self):
        self.name = "gemini"
        vertexai.init(
            project="projectameoba",
            location="us-central1",
        )
        self.ai_client = GenerativeModel("gemini-pro-vision")

    async def send_json_chat(self, prompt: Any, sys_propmt: Any) -> str:
        chat_msg = f"\n**system_prompt**\n {sys_propmt} \n**user_prompt**\n {prompt}\n\n make sure response is a single valid string"
        response = await self.ai_client.generate_content_async(
            chat_msg,
            generation_config={
                "max_output_tokens": 2048,
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 32,
            },
        )
        res_string = str(response.text)  # type: ignore
        json_string = ""
        try:
            json_start = res_string.index("{")
            json_end = res_string.rindex("}") + 1
            json_string = res_string[json_start:json_end]
            if not json_string:
                raise Exception("Failed to extract json string")
        except Exception as e:
            logger.error(f"Failed to extract json string from {res_string}")
            raise Exception("Failed to extract json string")

        await self.log_req_res_to_file(chat_msg, json_string)
        return json_string

    async def generate_code(self, prompt: str) -> str:
        _res = await self.ai_client.generate_content_async(
            prompt,
            generation_config={
                "max_output_tokens": 2048,
                "temperature": 0.9,
                "top_p": 1,
                "top_k": 32,
            },
        )
        res = str(_res.text)
        await self.log_req_res_to_file(prompt, res)
        return res
