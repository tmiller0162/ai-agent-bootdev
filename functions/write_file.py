import os

from .get_files_info import check_if_valid


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        valid = check_if_valid(working_directory, file_path)
        if not valid[1]:
            return valid[0]
        target_path = valid[0]
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes to a file, creating a new file and any necessary parent directories or overwriting an existing file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to the file to write, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the given file",
                },
            },
        },
    },
}
