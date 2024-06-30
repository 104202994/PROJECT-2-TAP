<h1>Structure of Log entries</h1>
<pre>&lt;IP Address> - - [&lt;Date and Time>] "&lt;HTTP Method> &lt;Request URL> &lt;HTTP Version>" &lt;HTTP Status Code> &ltResponse Size></pre>
<b>Sample Log for Brute Force:</b>
<pre>192.168.3 - - [30/Jun/2024:10:41:54 +1000] "GET /DVWA/vulnerabilities/brute/?username=admin&password=letmein&Login=Login HTTP/1.0" 200 4292</pre>

<b>Sample Log for Dos Attack:</b>
<pre>192.168.3 - - [30/Jun/2024:10:26:15 +1000] "GET /DVWA HTTP/1.1" 408 1011</pre>
