<h1>Structure of Log entries</h1>
<pre>&lt;IP Address> - - [&lt;Date and Time>] "&lt;HTTP Method> &lt;Request URL> &lt;HTTP Version>" &lt;HTTP Status Code> &ltResponse Size></pre>
<b>Sample Log for Brute Force:</b>
<pre>192.168.3 - - [30/Jun/2024:10:41:54 +1000] "GET /DVWA/vulnerabilities/brute/?username=admin&password=letmein&Login=Login HTTP/1.0" 200 4292</pre>

<b>Sample Log for Dos Attack:</b>
<pre>192.168.3 - - [30/Jun/2024:10:26:15 +1000] "GET /DVWA HTTP/1.1" 408 1011</pre>

<b>Sample Log for Directory Traversal:</b>
<pre>192.168.8.103 - - [18/Aug/2024:20:16:13 +1000] "GET /DVWA/vulnerabilities/fi/?page=../../../../../../../../../../etc/passwd HTTP/1.1" 200 22</pre>

<b>Sample Log for File Inclusion:</b>
<pre>192.168.8.103 - - [18/Aug/2024:19:25:27 +1000] "GET /DVWA/vulnerabilities/fi/?page=file4.php HTTP/1.1" 200 3565</pre>
<pre>192.168.8.103 - - [18/Aug/2024:19:13:01 +1000] "GET /DVWA/vulnerabilities/fi/?page=https://google.com HTTP/1.1" 200 3237</pre>
