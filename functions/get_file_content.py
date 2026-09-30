import os

from config import FILE_READ_CHAR_LIMIT

from .get_files_info import check_if_valid


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        check = check_if_valid(working_directory, file_path)
        if check[1] == False:
            return check[0]
        target_file = check[0]
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_file, "r") as f:
            text_content = f.read(FILE_READ_CHAR_LIMIT)
            if f.read(1):
                text_content += f'[...File "{file_path}" truncated at {FILE_READ_CHAR_LIMIT} characters]'
        return text_content
    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Retrieves the contents of a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to the file to read, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
