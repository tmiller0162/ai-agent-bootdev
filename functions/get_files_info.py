import os
from os.path import isdir


class FileNode:
    def __init__(self, file: str):
        self.name = os.path.basename(file)
        self.size = os.path.getsize(file)
        self.is_dir = os.path.isdir(file)


def check_if_valid(working_directory: str, directory: str = ".") -> tuple[str, bool]:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return (
                f'Error: Cannot list "{directory}" as it is outside the permitted working directory',
                False,
            )
        return target_dir, True
    except Exception as e:
        return f"Error: {e}", False


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        check = check_if_valid(working_directory, directory)
        if check[1] == False:
            return check[0]
        target_dir = check[0]
        if not isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        # DO NOT TRUST UNCONDITIONALLY: WILL ALLOW SYMLINKS
        # DO NOT ALLOW WRITES, ONLY READS ON TRUSTED DIR
        # OTHERWISE, USE A PROPER SANDBOX INSTEAD
        final_lst = ["\n"]
        for file in os.listdir(target_dir):
            file = os.path.join(target_dir, file)
            file_node = FileNode(file)
            final_lst.append(
                f"  - {file_node.name}: file_size={file_node.size} bytes, is_dir={file_node.is_dir}"
            )
        return "\n".join(final_lst)
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
