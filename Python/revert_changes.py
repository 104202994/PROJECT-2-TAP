import os
import subprocess

def revert_security(folder_name):
    """Revert changes in index.php files to use {$vulnerabilityFile}."""
    file_path = f'/opt/lampp/htdocs/DVWA/vulnerabilities/{folder_name}/index.php'
    
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return
    
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        with open(file_path, 'w') as file:
            for line in lines:
                if "require_once DVWA_WEB_PAGE_TO_ROOT . 'vulnerabilities/{folder_name}/source/impossible.php';" in line:
                    line = line.replace("impossible.php", "{$vulnerabilityFile}")
                file.write(line)
        
        print(f"Reverted {file_path} to use {{$vulnerabilityFile}}")
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

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
