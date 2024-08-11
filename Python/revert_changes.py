import os
import subprocess

def revert_security(folder_name):
    """Revert changes in index.php files to use {$vulnerabilityFile}."""
    # Construct the file path
    file_path = f"/opt/lampp/htdocs/DVWA/vulnerabilities/{folder_name}/index.php"
    
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # The line to search for with "impossible.php"
    search_line = f'require_once DVWA_WEB_PAGE_TO_ROOT . "vulnerabilities/{folder_name}/source/impossible.php";'
    replacement_line = f'require_once DVWA_WEB_PAGE_TO_ROOT . "vulnerabilities/{folder_name}/source/{{$vulnerabilityFile}}";'
    
    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Flag to check if the line was found and replaced
    found = False

    # Iterate over each line to find and replace the matching line
    for i, line in enumerate(lines):
        if search_line in line:
            lines[i] = line.replace('impossible.php', '{$vulnerabilityFile}')
            found = True
            print(f"Line found and reverted in {file_path} at line {i+1}")
            break

    # If the line was found and replaced, write back the modified content to the file
    if found:
        with open(file_path, 'w') as file:
            file.writelines(lines)
    else:
        print(f"Line not found in {file_path}")

def update_php_ini():
    """Update php.ini to set allow_url_include to On."""
    php_ini_path = '/opt/lampp/etc/php.ini'
    
    if not os.path.isfile(php_ini_path):
        print(f"File not found: {php_ini_path}")
        return
    
    try:
        with open(php_ini_path, 'r') as file:
            lines = file.readlines()
        
        with open(php_ini_path, 'w') as file:
            for line in lines:
                if 'allow_url_include=' in line:
                    file.write('allow_url_include=On\n')
                else:
                    file.write(line)
        
        print(f"Updated {php_ini_path} to set allow_url_include to On")
    
    except Exception as e:
        print(f"Error updating {php_ini_path}: {e}")

def restart_apache():
    """Restart the Apache server in XAMPP."""
    try:
        subprocess.run(['/opt/lampp/lampp', 'restart'], check=True)
        print("Apache server has been restarted.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart Apache server: {e}")

# List of folders to process
folders = ['brute', 'fi']

# Process each folder
for folder in folders:
    revert_security(folder)

# Update php.ini
update_php_ini()

# Restart Apache
restart_apache()
