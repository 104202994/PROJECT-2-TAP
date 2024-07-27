import subprocess
import sys

def unblock_ip(ip):
    try:
        subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        print(f"Unblocked IP: {ip}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to unblock IP {ip}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python unblock_ip.py <ip_address>")
        sys.exit(1)
    
    ip = sys.argv[1]
    unblock_ip(ip)

