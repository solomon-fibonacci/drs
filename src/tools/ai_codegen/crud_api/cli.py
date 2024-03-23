import argparse
import asyncio
import os
import zipfile
from tools.ai_codegen.crud_api.generator import CrudApiCodeGen

DEFAULT_PROJECT_NAME = "MyAPIProject"
DEFAULT_SPEC = "A simple CRUD API for an event management system."


def write_to_file(folder_path: str, filename: str, content: str):
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
    parser = argparse.ArgumentParser(
        description="Generate API code based on a specification.")
    parser.add_argument(
        "--project_name",
        type=str,
        default=DEFAULT_PROJECT_NAME,
        help=f"The name of the project (default: {DEFAULT_PROJECT_NAME})")
    parser.add_argument(
        "--spec",
        type=str,
        default=DEFAULT_SPEC,
        help=
        f"The specification of the API in natural language (default: {DEFAULT_SPEC})"
    )
    args = parser.parse_args()

    project_name = args.project_name
    spec = args.spec

    # Generate code
    code_gen = CrudApiCodeGen(spec)
    generated_components = await code_gen.generate_all()

    # Create project folder
    project_folder = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_folder, exist_ok=True)

    # Write generated code to files
    write_to_file(project_folder, "datamodels.py",
                  generated_components["datamodels"])
    write_to_file(project_folder, "router.py", generated_components["router"])
    write_to_file(project_folder, "service.py",
                  generated_components["service"])
    write_to_file(project_folder, "main.py",
                  generated_components["main"])  # New: Write the main file

    # Zip the project folder
    zip_path = zip_project_folder(project_folder)

    # Output the path to the zip file
    print(f"Project zipped at: {zip_path}")


if __name__ == "__main__":
    asyncio.run(main())
