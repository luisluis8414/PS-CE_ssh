# Als Basis-Image Rocky-Linux 10.0 (oder alternativ 9.4) 
FROM docker.io/rockylinux/rockylinux:10.0 

# 1. openssh-server: Der Daemon
# 2. nano: Damit die User configs bearbeiten können
RUN dnf install -y openssh-server nano

# Nötige Vorbereitungen für den SSHD-Start:
# - Host Keys generieren
# - Verzeichnis für Privilege Separation anlegen
RUN ssh-keygen -A \
    && mkdir -p /run/sshd

# Minimaler User "user" mit Passwort "123" 
# Root-Passwort setzen 
RUN useradd user && echo 'user:123' | chpasswd \
    && echo 'root:root123' | chpasswd

EXPOSE 22

# ssh starten & Container offen halten
CMD ["/bin/bash", "-c", "/usr/sbin/sshd && tail -f /dev/null"]