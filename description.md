# SSH

**ssh** (SSH client) is a program for logging into a remote machine and for executing commands on a remote machine. It is intended to provide secure encrypted communications between two untrusted hosts over an insecure network. 

**ssh**  connects and logs into the specified destination, which may be specified as either `[user@]hostname` or a URI of the form `ssh://[user@]hostname[:port]`. The user must prove their identity to the remote machine using one of several methods (e.g password, key...).

If a command is specified, it will be executed on the remote host instead of a login shell. A complete command line may be specified as command, or it may have additional arguments. If supplied, the arguments will be appended to the command, separated by spaces, before it is sent to the server to be executed. [[1]](https://man.openbsd.org/ssh)

## Sources

https://www.openssh.org/manual.html

ssh(1) — The basic rlogin/rsh-like client program
sshd(8) — The daemon that permits you to log in
ssh_config(5) — The client configuration file
sshd_config(5) — The daemon configuration file
ssh-agent(1) — An authentication agent that can store private keys
ssh-add(1) — Tool which adds keys to in the above agent
sftp(1) — FTP-like program that works over SSH1 and SSH2 protocol
scp(1) — File copy program that acts like rcp
ssh-keygen(1) — Key generation tool
sftp-server(8) — SFTP server subsystem (started automatically by sshd)
ssh-keyscan(1) — Utility for gathering public host keys from a number of hosts
ssh-keysign(8) — Helper program for host-based authentication