import os

def upgrade_security(folder_name):
    # Construct the file path
    file_path = f"/opt/lampp/htdocs/DVWA/vulnerabilities/{folder_name}/index.php"
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # The line to search for, with {folder_name} replaced
    search_line = f'require_once DVWA_WEB_PAGE_TO_ROOT . "vulnerabilities/{folder_name}/source/{{$vulnerabilityFile}}";'
    replacement_line = f'require_once DVWA_WEB_PAGE_TO_ROOT . "vulnerabilities/{folder_name}/source/impossible.php";'
    
    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Flag to check if the line was found and replaced
    found = False

    # Iterate over each line to find and replace the matching line
    for i, line in enumerate(lines):
        if search_line in line:
            lines[i] = line.replace('{$vulnerabilityFile}', 'impossible.php')
            found = True
            print(f"Line found and replaced in {file_path} at line {i+1}")
            break

    # If the line was found and replaced, write back the modified content to the file
    if found:
        with open(file_path, 'w') as file:
            file.writelines(lines)
    else:
        print(f"Line not found in {file_path}")

