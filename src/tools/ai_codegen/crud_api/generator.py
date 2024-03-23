import asyncio
from tools.ai_client.factory import get_ai_client
from tools.ai_codegen.crud_api.templates.service import template as service_template
from tools.ai_codegen.crud_api.templates.router import template as router_template
from tools.ai_codegen.crud_api.templates.datamodels import template as datamodels_template
from tools.ai_codegen.crud_api.templates.main import template as main_template


class CrudApiCodeGen:

    def __init__(self, spec: str):
        """
        Initializes the CRUD API code generator with a specific set of specifications.
        
        :param spec: A string containing a natural language description of the entire API.
        """
        self.spec = f"""{spec}. Make sure to only include source code in your response. 
        The string from your response will be written to a file for execution, 
        so you must not include any additional comments or instructions.
        Also ensure to not include any formatting or markdown syntax (such as ```python) in your response.
        The outputted string should be valid Python code that is executable as is.
        """
        self._datamodel = ""
        self._service = ""
        self.ai_client = get_ai_client()

    async def generate_datamodels(self) -> str:
        """
        Generates the content for the datamodels.py file based on a natural language spec,
        combining detailed instructions with a template for code generation.
        """
        prompt = f"""
        # Specification:
        {self.spec}

        # Template:
        {datamodels_template}

        # Instructions:
        Generate Python code for data models using Pydantic. The code should include necessary imports. 
        Define enums and models based on the specification above, using the following template as a guideline.
        """
        # Additional template and example details would be included here.
        generated_code = await self._send_prompt(prompt)
        self._datamodel = generated_code
        return generated_code

    async def generate_router(self) -> str:
        """
        Generates the content for the router.py file based on a natural language spec,
        combining detailed instructions with a template for code generation.
        """
        prompt = f"""
        # Specification:
        {self.spec}

        # Template:
        {router_template}

        # Data Models:
        {self._datamodel}

        # Instructions:
        Generate Python code for FastAPI router including necessary imports and route decorators. 
        """
        # Additional template and example details would be included here.
        generated_code = await self._send_prompt(prompt)
        return generated_code

    async def generate_service(self) -> str:
        """
        Generates the content for the service.py file based on a natural language spec,
        combining detailed instructions with a template for code generation.
        """
        prompt = f"""
        # Specification:
        {self.spec}

        # Template:
        {service_template}
        
        # Data Models:
        {self._datamodel}


        # Instructions:
        Generate Python code for the service layer, including necessary functions and business logic. 
        The service layer interacts with the database or external services to perform CRUD operations, 
        including retrieving a specific item by ID.


        # Your code should replace the YourService class methods with specifics from the specification,
        # including details for the method to get an item by ID.
        """
        # Additional template and example details would be included here.
        generated_code = await self._send_prompt(prompt)
        return generated_code

    async def generate_main(self) -> str:
        """
        Generates the content for the api.py file based on a natural language spec,
        combining detailed instructions with a template for code generation.
        """
        prompt = f"""
        # Specification:
        {self.spec}

        # Template:
        {main_template}

        # Instructions:
        Generate Python code for the main API file, including the FastAPI app setup, 
        importing routers and defining the main entry point for the API.
        """
        # Additional template and example details would be included here.
        generated_code = await self._send_prompt(prompt)
        return generated_code

    async def generate_all(self) -> dict:
        """
        Generates all the code components for the CRUD API based on the natural language spec.
        """
        datamodels_code = await self.generate_datamodels()
        router_code_gen_task = self.generate_router()
        service_code_gen_task = self.generate_service()
        main_code_gen_task = self.generate_main()

        router_code, service_code, main_code = await asyncio.gather(
            router_code_gen_task, service_code_gen_task, main_code_gen_task)
        return {
            "datamodels": datamodels_code,
            "router": router_code,
            "service": service_code,
            "main": main_code
        }

    async def _send_prompt(self, prompt: str) -> str:
        """
        Sends a prompt to the AI model to generate code based on the given prompt.
        
        :param prompt: The prompt for generating code.
        :return: The generated code.
        """
        prompt = f"""
        {prompt}. 
        Make sure that all methods are implemented and do not contain "pass", 
        blank space or placeholder comments.
        """
        return await self.ai_client.generate_code(prompt)
