FROM rockylinux:9

RUN dnf install -y openssh-server passwd && \
    mkdir -p /var/run/sshd && \
    useradd demo && echo "demo:demo123" | chpasswd

COPY sshd_config /etc/ssh/sshd_config

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
