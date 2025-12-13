# Als Basis-Image Rocky-Linux 10.0 (oder alternativ 9.4) 
FROM docker.io/rockylinux/rockylinux:10.0 

# 1. openssh-server: Der Daemon
# 2. nano: Damit die User configs bearbeiten können
RUN dnf install -y openssh-server nano procps-ng sudo python3 && \
    dnf clean all

# user erstellen
RUN useradd -m admin && \
    echo "admin:admin123" | chpasswd && \
    usermod -aG wheel admin
    
USER admin
WORKDIR /home/admin

# Container offen halten
CMD ["tail", "-f", "/dev/null"]