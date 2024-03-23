from typing import Any


class AiClient:
    name: str
    system_msg: Any

    async def send_json_chat(self, prompt: Any, sys_prompt: str) -> str:
        raise NotImplementedError

    async def generate_code(self, prompt: str) -> str:
        raise NotImplementedError
