import os
from datetime import datetime


class AiClient:
    name: str
    system_msg: str

    async def send_json_chat(self, prompt: str, sys_prompt: str) -> str:
        raise NotImplementedError

    async def generate_code(self, prompt: str) -> str:
        raise NotImplementedError

    async def log_req_res_to_file(self, prompt: str, response: str):
        log_dir = f"ai_logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file = f"{log_dir}/{self.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(log_file, 'a') as file:
            try:
                file.write(
                    f"Request:\n{prompt}\n\n<<<<<>>>>>\n\nResponse:\n{response}\n\n"
                )
            except FileNotFoundError as e:
                print(f"Failed to log request and response to file: {e}")

        print(f"Request and response logged to {log_file}")
