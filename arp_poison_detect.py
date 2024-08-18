from scapy.all import *
import time

def detect_arp_poison(pkt):
    if ARP in pkt and pkt[ARP].op == 2:  # ARP reply is op=2
        real_mac = getmacbyip(pkt[ARP].psrc)
        response_mac = pkt[ARP].hwsrc
        if real_mac and real_mac != response_mac:
            alert_msg = f"ARP Poisoning detected: REAL-MAC {real_mac}, FAKE-MAC {response_mac} for IP {pkt[ARP].psrc}"
            print(alert_msg)
            log_arp_poison(alert_msg, pkt[ARP].psrc)

def log_arp_poison(message, ip):
    log_line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - ARP_POISON {ip} - {message}\n"
    with open("/var/log/arp_poison.log", "a") as log_file:
        log_file.write(log_line)

if __name__ == "__main__":
    print("Starting ARP poisoning detection...")
    sniff(store=False, prn=detect_arp_poison, iface="enp0s1")
