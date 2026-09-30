from functions.get_file_content import get_file_content


def print_output(working_dir: str, file: str) -> None:
    result = get_file_content(working_dir, file)
    print(result)
    if not "Error: " == result[:7]:
        print(f"{file} length: {len(result)}")
        print(f"{file} truncated: {'truncated' in result}")


print_output("calculator", "lorem.txt")

print_output("calculator", "main.py")

print_output("calculator", "pkg/calculator.py")

print_output("calculator", "/bin/cat")

print_output("calculator", "pkg/does_not_exist.py")
