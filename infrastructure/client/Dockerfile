# Als Basis-Image Rocky-Linux 10.0 (oder alternativ 9.4) 
FROM docker.io/rockylinux/rockylinux:10.0 
 
# openssh-clients: Enthält ssh, scp, sftp, ssh-keygen
# nano: Zum Schreiben von Dateien
RUN dnf install -y openssh-clients nano && \
    dnf clean all

# Benutzer erstellen
RUN useradd -m student && \
    echo "student:student123" | chpasswd

# Als student starten
USER student
WORKDIR /home/student

# Container offen halten
CMD ["tail", "-f", "/dev/null"]