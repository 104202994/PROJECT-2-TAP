<?php



// Disable XSS protection for demonstration purposes (remove in production)

header("X-XSS-Protection: 0");



$html = '';



// Check if 'name' parameter exists in GET request and is not empty

if (array_key_exists("name", $_GET) && $_GET['name'] != NULL) {

    $name = strip_tags($_GET['name']);



    // Output sanitized input

    $html .= "<pre>Hello {$name}</pre>";



    // Display the output

    echo $html;



    // Simulate delay before changing security level (e.g., 7 seconds)

    echo "<script>

        setTimeout(function() {

            // Redirect to set security level to 'impossible'

            window.location.href = '?set_impossible=true';

        }, 15000); // 7 seconds delay

    </script>";

}



// <script>alert('XSS Attack in Low Security!')</script>





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

