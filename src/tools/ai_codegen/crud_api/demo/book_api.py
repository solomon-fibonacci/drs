# Assuming the CrudApiCodeGen and AiClient are defined in crud_api_code_gen.py
from tools.ai_codegen.crud_api.generator import CrudApiCodeGen

# Unified specification for the Book Management System
specification = """
A Book Management System to catalog books. Each book has a title, author, publication year, and ISBN.
Functionality needed includes:
- Adding a new book
- Listing all books
- Retrieving a book by its ISBN
- Updating book details
- Deleting a book by ISBN
The system should use a RESTful API design, with a service layer interacting with a mock database.
"""


def test_crud_api_codegen():
    # Create an instance of the CrudApiCodeGen with the unified specification
    code_generator = CrudApiCodeGen(specification)

    # Generate code based on the provided specification
    datamodels_code = code_generator.generate_datamodels()
    router_code = code_generator.generate_router()
    service_code = code_generator.generate_service()

    # Output the generated code for review
    print("=== Data Models Code ===")
    print(datamodels_code, "\n")
    print("=== Router Code ===")
    print(router_code, "\n")
    print("=== Service Code ===")
    print(service_code, "\n")


if __name__ == "__main__":
    test_crud_api_codegen()
