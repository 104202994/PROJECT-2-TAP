<?php



// Include necessary files or define constants if required

define('DVWA_WEB_PAGE_TO_ROOT', '../../');

require_once DVWA_WEB_PAGE_TO_ROOT . 'dvwa/includes/dvwaPage.inc.php';



dvwaPageStartup(array('authenticated'));



// Handle guestbook form submission

if (isset($_POST['btnSign'])) {

    // Get input

    $message = trim($_POST['mtxMessage']);

    $name = trim($_POST['txtName']);



    // Sanitize inputs

    $message = stripslashes($message);

    $message = mysqli_real_escape_string($GLOBALS["___mysqli_ston"], $message);

    $name = mysqli_real_escape_string($GLOBALS["___mysqli_ston"], $name);



    // Insert into database

    $query = "INSERT INTO guestbook (comment, name) VALUES ('$message', '$name')";

    $result = mysqli_query($GLOBALS["___mysqli_ston"], $query)

        or die('<pre>' . mysqli_error($GLOBALS["___mysqli_ston"]) . '</pre>');



    // Simulate delay before changing security level (e.g., 15 seconds)

    echo "<pre>ATTACK DETECTED, MITIGATING IN 15 SECONDS..</pre>";

    echo "<script>

            setTimeout(function() {

                window.location.href = '?set_impossible=true';

            }, 10000); // 15 seconds delay

          </script>";

}



// Check if the page is reloaded to set security level

if (isset($_GET['set_impossible']) && $_GET['set_impossible'] === 'true') {

    // Set security level to 'impossible'

    dvwaSecurityLevelSet('impossible');

    $query  = "TRUNCATE guestbook;";

    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    // Redirect to appropriate page

    header('Location: ../../vulnerabilities/xss_s/'); // Adjust the path as needed

    exit();

}



?>

