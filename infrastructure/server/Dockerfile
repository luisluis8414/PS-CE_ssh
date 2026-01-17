# Als Basis-Image Rocky-Linux 10.0 (oder alternativ 9.4) 
FROM docker.io/rockylinux/rockylinux:10.0 

RUN dnf install -y epel-release && \
    dnf install -y openssh-server nano sl procps-ng sudo python3 && \
    dnf clean all

# user erstellen
RUN useradd -m admin && \
    echo 'admin:4j6$9*BAof78' | chpasswd && \
    usermod -aG wheel admin
    
USER admin
WORKDIR /home/admin

# Container offen halten
CMD ["tail", "-f", "/dev/null"]