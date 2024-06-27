function checkReloadFlag() {
    fetch('/dvwa/config/reload_flag.txt')
        .then(response => {
            if (response.ok) {
                return response.text();
            } else {
                throw new Error('No reload required');
            }
        })
        .then(text => {
            if (text.includes('XSS attack detected')) {
                alert('XSS attack has been detected and prevented.');
                // Reload the page
                window.location.reload(true);
                // Clear the flag file after reloading
                fetch('/dvwa/config/reload_flag.txt', {
                    method: 'DELETE'
                }).then(() => {
                    console.log('Flag file cleared after reload.');
                }).catch(error => {
                    console.error('Failed to clear flag file after reload:', error);
                });
            }
        })
        .catch(error => {
            console.log('No reload required yet.');
        });
}

// Check for the flag every 5 seconds
setInterval(checkReloadFlag, 5000);
