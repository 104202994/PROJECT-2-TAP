<?php

// Disable XSS protection for demonstration purposes (remove in production)
header("X-XSS-Protection: 0");

$html = '';

// Function to check the injection flag and clear it
function isInjectionDetected() {
    $flagFile = 'injection_flag.txt'; // Adjust the path as needed
    if (file_exists($flagFile)) {
        $flagContent = file_get_contents($flagFile);
        if (strpos($flagContent, 'INJECTION DETECTED') !== false) {
            // Clear the flag file
            file_put_contents($flagFile, '');
            return true;
        }
    }
    return false;
}

// Check if 'name' parameter exists in GET request and is not empty
if (array_key_exists("name", $_GET) && $_GET['name'] != NULL) {
    $name = strip_tags($_GET['name']);

    // Output sanitized input
    $html .= "<pre>Hello {$name}</pre>";

    // Display the output
    echo $html;

    // Check for injection flag and set security level if detected
    if (isInjectionDetected()) {
        // Simulate delay before changing security level (e.g., 15 seconds)
        echo "<pre>ATTACK DETECTED, MITIGATING IN 15 SECONDS..</pre>";
        echo "<script>
            setTimeout(function() {
                // Redirect to set security level to 'impossible'
                window.location.href = '?set_impossible=true';
            }, 15000); // 15 seconds delay
        </script>";
    }
}

// Check if the page is reloaded to set security level
if (isset($_GET['set_impossible']) && $_GET['set_impossible'] === 'true') {
    define('DVWA_WEB_PAGE_TO_ROOT', '../../');
    require_once DVWA_WEB_PAGE_TO_ROOT . 'dvwa/includes/dvwaPage.inc.php';

    dvwaSecurityLevelSet('impossible');
    dvwa_start_session();
    header('Location: ../../vulnerabilities/xss_r/'); // Adjust the path as needed
    exit();
}

?>

<script>
    // JavaScript function to keep checking the flag file every 15 seconds
    function checkInjectionFlag() {
        fetch('path/to/injection_flag.txt') // Adjust the path as needed
            .then(response => response.text())
            .then(text => {
                if (text.includes('INJECTION DETECTED')) {
                    location.href = '?set_impossible=true';
                } else {
                    setTimeout(checkInjectionFlag, 15000); // Check again in 15 seconds
                }
            })
            .catch(error => console.error('Error:', error));
    }

    // Start checking the flag file when the page loads
    window.onload = checkInjectionFlag;
</script>
