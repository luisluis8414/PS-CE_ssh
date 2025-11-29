from scapy.all import rdpcap, TCP
import numpy as np
import os

PCAP_FILE = os.path.expanduser("~/ssh.pcap")

print("[ANALYSE] Lade PCAP:", PCAP_FILE)

if not os.path.exists(PCAP_FILE):
    print("[ERROR] PCAP Datei nicht gefunden!")
    exit(1)

packets = rdpcap(PCAP_FILE)

times = [p.time for p in packets if p.haslayer(TCP)]
if len(times) < 2:
    print("[ANALYSE] Nicht genug SSH-Pakete gefunden.")
    exit(0)

deltas = np.diff(times)

print("[ANALYSE] Inter-Keystroke Timings (ms):")
for d in deltas:
    print(f"{d * 1000:.2f}")

print(f"\n[ANALYSE] Pakete: {len(times)}")
