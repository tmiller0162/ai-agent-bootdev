from functions.get_files_info import get_files_info

str_prefix = "Result for current directory:"

print(str_prefix, get_files_info("calculator", "."))
print(str_prefix, get_files_info("calculator", "pkg"))
print(str_prefix, get_files_info("calculator", "/bin"))
print(str_prefix, get_files_info("calculator", "../"))
print(str_prefix, get_files_info("calculator", "main.py"))
