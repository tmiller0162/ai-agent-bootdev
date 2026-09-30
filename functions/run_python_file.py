import os
import subprocess

from .get_files_info import check_if_valid


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        valid = check_if_valid(working_directory, file_path)
        if not valid[1]:
            return valid[0].replace("list", "execute")
        target = valid[0]
        if not os.path.isfile(target):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target[-3:] == ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = [
            "python",
            target,
        ]
        if args:
            command.extend(args)
        process = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output_str = ""
        if process.returncode != 0:
            output_str += f"Process exited with code {process.returncode}"
        if not process.stderr and not process.stdout:
            output_str += "No output produced"
        else:
            output_str += f"STDOUT: {process.stdout}"
            output_str += f"STDERR: {process.stderr}"
        return output_str
    except Exception as e:
        return f"Error: executing python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a python file with the given optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to the python executable, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array",
                    "items": "string",
                    "description": "Optional parameter to provide arguments to the python executable",
                },
            },
        },
    },
}
