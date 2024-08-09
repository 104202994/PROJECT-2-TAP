import os

def upgrade_security(folder_name):
    # Define the path to the index.php file
    file_path = f'/opt/lampp/htdocs/DVWA/vulnerabilities/{folder_name}/index.php'
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return
    
    # Read the file content
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        for line in lines:
            # Replace the specific line if it matches the pattern
            if "require_once DVWA_WEB_PAGE_TO_ROOT . 'vulnerabilities/{folder_name}/source/{$vulnerabilityFile}';" in line:
                line = line.replace("{$vulnerabilityFile}", "impossible.php")
            file.write(line)
    
    print(f"Updated {file_path} to use impossible.php")

