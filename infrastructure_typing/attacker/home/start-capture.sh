#!/bin/bash
echo "[INFO] Starte passiven SSH-Traffic-Mitschnitt..."
tcpdump -i eth0 -w ssh.pcap 'tcp port 22'
