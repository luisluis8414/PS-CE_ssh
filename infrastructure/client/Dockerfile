# Als Basis-Image Rocky-Linux 10.0 (oder alternativ 9.4) 
FROM docker.io/rockylinux/rockylinux:10.0 
 
# openssh-clients: Enthält ssh, scp, sftp, ssh-keygen
# nano: Zum Schreiben von Dateien
RUN dnf install -y epel-release && \
    dnf install -y openssh-clients nano sl procps-ng && \
    dnf clean all

RUN useradd -m student && \
    echo "student:student123" | chpasswd

RUN mkdir -p /home/student/.ssh && \
    chmod 700 /home/student/.ssh

COPY src/server.py /home/student/server.py
COPY config /home/student/.ssh/config

RUN chown -R student:student /home/student && \
    chmod 600 /home/student/.ssh/config

# Als student user starten
USER student
WORKDIR /home/student

# Container offen halten
CMD ["tail", "-f", "/dev/null"]