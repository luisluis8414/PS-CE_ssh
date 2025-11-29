FROM docker.io/rockylinux/rockylinux:10.0

RUN dnf install -y tcpdump python3 python3-pip iproute iputils procps-ng \
    && pip3 install scapy numpy

WORKDIR /root
