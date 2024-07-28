import subprocess
from concurrent.futures import ThreadPoolExecutor

def run_script(script_name):
    """Function to run a script and print its output in real-time."""
    try:
        process = subprocess.Popen(
            ['sudo', 'python3', script_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1,
            universal_newlines=True,
            env={"PYTHONUNBUFFERED": "1"}
        )
        
        # Continuously read output from the process
        while True:
            # Read a line from stdout
            output = process.stdout.readline()
            if output:
                print(f'{script_name}: {output.strip()}')
            
            # Read a line from stderr
            err = process.stderr.readline()
            if err:
                print(f'{script_name} (stderr): {err.strip()}')
            
            # If the process is done and no more output
            if output == '' and err == '' and process.poll() is not None:
                break
    except FileNotFoundError as e:
        print(f'File not found: {e}')
    except Exception as e:
        print(f'Unexpected error: {e}')

if __name__ == '__main__':
    scripts = ['detectDos.py', 'detectFileInclusion.py', 'detectDirectoryTraversal.py', 'detectBruteForce.py']
    
    # Create a ThreadPoolExecutor to run scripts concurrently
    with ThreadPoolExecutor(max_workers=len(scripts)) as executor:
        futures = [executor.submit(run_script, script) for script in scripts]
        
        for future in futures:
            try:
                future.result()  # Wait for all futures to complete
            except Exception as e:
                print(f'Unexpected error: {e}')
