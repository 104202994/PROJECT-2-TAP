<?php

function checkSessionFlag() {
    $flagFilePath = '/path/to/session_flag.txt'; // Update with the actual path to the flag file

    // Check if the flag file exists
    if (file_exists($flagFilePath)) {
        // Read the content of the flag file
        $flagContent = file_get_contents($flagFilePath);

        // Check if the flag is set to "SESSION_FLAG"
        if (strpos($flagContent, 'SESSION_FLAG') !== false) {
            // Clear the flag file
            file_put_contents($flagFilePath, '');

            // Perform the logout and redirect actions
            dvwaLogout();
            dvwaRedirect('../../login.php');

            // Return true to indicate that the flag was detected and actions were taken
            return true;
        }
    }

    // Return false if the flag was not detected
    return false;
}

if (isset($_GET['Login'])) {
    // Check for the session flag before proceeding
    if (checkSessionFlag()) {
        // If the flag was detected and actions were taken, exit the script
        exit();
    }

    // Get username
    $user = $_GET['username'];

    // Get password
    $pass = $_GET['password'];
    $pass = md5($pass);

    // Check the database
    $query = "SELECT * FROM `users` WHERE user = '$user' AND password = '$pass';";
    $result = mysqli_query($GLOBALS["___mysqli_ston"], $query) or die('<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>');

    if ($result && mysqli_num_rows($result) == 1) {
        // Get user's details
        $row = mysqli_fetch_assoc($result);
        $avatar = $row["avatar"];

        // Login successful
        $html .= "<p>Welcome to the password protected area {$user}</p>";
        $html .= "<img src=\"{$avatar}\" />";
    } else {
        // Login failed
        $html .= "<pre><br />Username and/or password incorrect.</pre>";
    }

    ((is_null($___mysqli_res = mysqli_close($GLOBALS["___mysqli_ston"]))) ? false : $___mysqli_res);
}
?>
