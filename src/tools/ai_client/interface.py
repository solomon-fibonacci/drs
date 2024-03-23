from typing import Any


class AiClient:
    name: str
    system_msg: Any

    async def send_json_chat(self, prompt: Any, sys_prompt: str) -> str:
        raise NotImplementedError

    async def generate_code(self, prompt: str) -> str:
        raise NotImplementedError

    async def log_req_res_to_file(self, prompt: str, response: str):
        log_file = f"{self.name}_log.txt"
        with open(log_file, 'a') as file:
            file.write(f"Prompt: {prompt}\n\n====\n\nResponse: {response}\n\n")
        print(f"Request and response logged to {log_file}")
