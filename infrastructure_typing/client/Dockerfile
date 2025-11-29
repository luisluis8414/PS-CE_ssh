FROM docker.io/rockylinux/rockylinux:10.0

RUN dnf install -y nano man \
    && dnf install -y epel-release \
    && dnf install -y openssh-clients iproute iputils procps-ng

CMD ["/bin/bash"]
