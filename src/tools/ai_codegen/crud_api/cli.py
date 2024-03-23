import argparse
import asyncio
import os
import zipfile
from tools.ai_codegen.crud_api.generator import CrudApiCodeGen


def write_to_file(folder_path, filename, content):
    with open(os.path.join(folder_path, filename), 'w') as file:
        file.write(content)


def zip_project_folder(folder_path):
    zip_filename = f"{folder_path}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                zipf.write(
                    os.path.join(root, file),
                    os.path.relpath(os.path.join(root, file),
                                    os.path.join(folder_path, '..')))
    return zip_filename


async def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Generate API code based on a specification.")
    parser.add_argument("--project_name",
                        type=str,
                        default="MyAPIProject",
                        help="The name of the project (default: MyAPIProject)")
    parser.add_argument(
        "--spec",
        type=str,
        default="A simple CRUD API for managing resources.",
        help=
        "The specification of the API in natural language (default: A simple CRUD API for managing resources.)"
    )
    args = parser.parse_args()

    # If arguments not provided, prompt the user
    project_name = args.project_name if args.project_name else input(
        "Enter the project name: ")
    spec = args.spec if args.spec else input("Enter the API specification: ")

    # Generate code
    code_gen = CrudApiCodeGen(spec)
    datamodels_code = await code_gen.generate_datamodels()
    router_code = await code_gen.generate_router()
    service_code = await code_gen.generate_service()

    # Create project folder
    project_folder = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_folder, exist_ok=True)

    # Write generated code to files
    write_to_file(project_folder, "datamodels.py", datamodels_code)
    write_to_file(project_folder, "router.py", router_code)
    write_to_file(project_folder, "service.py", service_code)

    # Zip the project folder
    zip_path = zip_project_folder(project_folder)

    # Output the path to the zip file
    print(f"Project zipped at: {zip_path}")


if __name__ == "__main__":
    asyncio.run(main())
