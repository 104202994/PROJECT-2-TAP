<?php



if( isset( $_POST[ 'Submit' ] ) ) {

	// Get input

	$target = $_REQUEST[ 'ip' ];



	// Determine OS and execute the ping command.

	if( stristr( php_uname( 's' ), 'Windows NT' ) ) {

		// Windows

		$cmd = shell_exec( 'ping ' . $target );

	}

	else {

		// *nix

		$cmd = shell_exec( 'ping -c 4 ' . $target );

	}



	// Feedback for the end user

	$html .= "<pre>{$cmd}</pre>";



	// Simulate delay before changing security level (e.g., 15 seconds)

	echo "<pre>Command executed. Redirecting to set security level to 'impossible' in 15 seconds...</pre>";

	echo "<script>

			setTimeout(function() {

				window.location.href = '?set_impossible=true';

			}, 15000); // 15 seconds delay

		  </script>";

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

