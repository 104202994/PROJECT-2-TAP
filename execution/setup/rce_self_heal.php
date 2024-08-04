<?php

// Paths to the flag file and the email script
$flagFile = 'execution_flag.txt';
$emailScript = 'send_email_script.sh';

// Function to check if the execution flag is set
function isFlagSet($filePath) {
    if (file_exists($filePath)) {
        $content = trim(file_get_contents($filePath));
        return $content === 'EXECUTION DETECTED';
    }
    return false;
}

// Function to clear the execution flag
function clearFlag($filePath) {
    if (file_exists($filePath)) {
        file_put_contents($filePath, '');
    }
}

// Function to execute the email script
function executeEmailScript($scriptPath) {
    if (file_exists($scriptPath)) {
        shell_exec($scriptPath);
    }
}

// Function to handle attack detection
function handleAttackDetection() {
    global $emailScript, $flagFile;
    // Simulate delay before changing security level (e.g., 15 seconds)
    echo "<pre>Command executed. Redirecting to set security level to 'impossible' in 15 seconds...</pre>";
    echo "<script>
            setTimeout(function() {
                window.location.href = '?set_impossible=true';
            }, 15000); // 15 seconds delay
          </script>";

    // Execute the email script
    executeEmailScript($emailScript);

    // Clear the execution flag
    clearFlag($flagFile);
}

if (isset($_POST['Submit'])) {
    // Get input
    $target = $_REQUEST['ip'];

    // Determine OS and execute the ping command
    if (stristr(php_uname('s'), 'Windows NT')) {
        // Windows
        $cmd = shell_exec('ping ' . $target);
    } else {
        // *nix
        $cmd = shell_exec('ping -c 4 ' . $target);
    }

    // Feedback for the end user
    $html .= "<pre>{$cmd}</pre>";

    // Check for the execution flag and handle attack if detected
    if (isFlagSet($flagFile)) {
        handleAttackDetection();
    } else {
        // Provide feedback and redirect without setting security level
        echo "<pre>Command executed.</pre>";
    }
}

// Check if the page is reloaded to set security level
if (isset($_GET['set_impossible']) && $_GET['set_impossible'] === 'true') {
    // Include necessary files or define constants if required
    define('DVWA_WEB_PAGE_TO_ROOT', '../../');
    require_once DVWA_WEB_PAGE_TO_ROOT . 'dvwa/includes/dvwaPage.inc.php';

    dvwaSecurityLevelSet('impossible');
    dvwa_start_session();

    // Redirect to the appropriate page
    header('Location: ../../vulnerabilities/exec/'); // Adjust the path as needed
    exit();
}

?>
