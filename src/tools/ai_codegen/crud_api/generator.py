from tools.ai_client.factory import AiClientFactory


class CrudApiCodeGen:

    def __init__(self, spec: str):
        """
        Initializes the CRUD API code generator with a specific set of specifications.
        
        :param spec: A string containing a natural language description of the entire API.
        """
        self.spec = spec
        self.ai_client = AiClientFactory.create_ai_client()

    async def generate_datamodels(self) -> str:
        """
        Generates the content for the datamodels.py file based on a natural language spec,
        combining detailed instructions with a template for code generation.
        """
        prompt = f"""
        # Specification:
        {self.spec}

        # Instructions:
        Generate Python code for data models using Pydantic. The code should include necessary imports. 
        Define enums and models based on the specification above, using the following template as a guideline.
        """
        # Additional template and example details would be included here.
        generated_code = self.ai_client.generate_code(prompt)
        return generated_code

    async def generate_router(self) -> str:
        """
        Generates the content for the router.py file based on a natural language spec,
        combining detailed instructions with a template for code generation.
        """
        prompt = f"""
        # Specification:
        {self.spec}

        # Instructions:
        Generate Python code for FastAPI router including necessary imports and route decorators. 
        """
        # Additional template and example details would be included here.
        generated_code = self.ai_client.generate_code(prompt)
        return generated_code

    async def generate_service(self) -> str:
        """
        Generates the content for the service.py file based on a natural language spec,
        combining detailed instructions with a template for code generation.
        """
        prompt = f"""
        # Specification:
        {self.spec}

        # Instructions:
        Generate Python code for the service layer, including necessary functions and business logic. 
        The service layer interacts with the database or external services to perform CRUD operations, 
        including retrieving a specific item by ID.
        """
        # Additional template and example details would be included here.
        generated_code = self.ai_client.generate_code(prompt)
        return generated_code
