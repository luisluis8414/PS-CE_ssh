# SSH and SCP: Secure Remote Access and File Transfer

## What is SSH?

**SSH** (Secure Shell) is a cryptographic network protocol that enables users to log into remote machines and execute commands securely. It uses cryptography to authenticate and encrypt connections between devices, ensuring that sensitive data cannot be intercepted during transmission [^3][^7].

Beyond simple remote access, SSH also enables tunneling (also known as port forwarding), which allows data packets to traverse networks they would not otherwise be able to cross. Common use cases for SSH include controlling servers remotely, managing infrastructure, and transferring files securely [^7].

### Why SSH?

Traditional tools like Telnet transmit data in clear, unencrypted form. Anyone monitoring network traffic could intercept usernames, passwords, and all transmitted data. SSH solves this by encrypting all communications between the client and server [^2].

## How does SSH work?

SSH operates on a client-server architecture [^2]:

1. **The SSH Server (sshd)**: A daemon running on the remote machine that listens for incoming connections (default port 22) [^1]
2. **The SSH Client (ssh)**: A program on the host machine that initiates connections to the server [^1]

When you connect via SSH:

1. The client contacts the server and they negotiate encryption algorithms
2. The server sends its public host key for verification
3. A secure encrypted channel is established
4. User authentication occurs (password or public key)
5. The user gains access to the remote shell

### SSH vs OpenSSH

**SSH** is the protocol - a set of rules that define how secure communication should work between two systems.

**OpenSSH** is the most widely used implementation of that protocol. It is a free, open source software suite developed by the OpenBSD project [^1]. When you use commands like `ssh`, `scp`, or `sshd` on Linux, macOS, or Windows, you are almost always using OpenSSH.

### OpenSSH Tools

Beyond the core `ssh` client and `sshd` server, OpenSSH provides additional tools [^1]:

| Tool          | Description                                                   |
| ------------- | ------------------------------------------------------------- |
| `ssh_config`  | The client configuration file                                 |
| `sshd_config` | The daemon configuration file                                 |
| `ssh-keygen`  | Key generation tool for creating authentication keys          |
| `ssh-copy-id` | Tool to install your public key on a remote server            |
| `ssh-agent`   | An authentication agent that can store private keys           |
| `ssh-add`     | Tool which adds keys to the ssh-agent                         |
| `scp`         | File copy program for secure file transfer                    |
| `sftp`        | FTP-like program that works over SSH protocol                 |
| `sftp-server` | SFTP server subsystem (started automatically by sshd)         |
| `ssh-keyscan` | Utility for gathering public host keys from a number of hosts |
| `ssh-keysign` | Helper program for host-based authentication                  |

In this tutorial, we will focus on `ssh`, `sshd`, `ssh-keygen`, and `scp`.

## Exercise 1: Your First SSH Connection

Now let's put this into practice! You will configure the SSH server for password authentication and connect to it from a client.

### Lab Credentials

These are the users and passwords you will use in each container:

| Container  | User    | Password   |
| ---------- | ------- | ---------- |
| ssh-server | admin   | admin123   |
| ssh-client | student | student123 |

### Step 1: Configure the SSH Server

In the **server terminal**, perform the following steps:

**1. Generate SSH host keys:**

Every SSH server needs its own unique cryptographic keys, called host keys, to identify itself to clients. These host keys serve two purposes:

- They prove the server's identity (so clients know they're connecting to the real server, not an imposter)
- They help establish the encrypted connection

`ssh-keygen` is used to generate these host keys [^8]. Generate the host keys by running:

```bash
sudo ssh-keygen -A
```

The `-A` flag "generates host keys of all default key types (rsa, ecdsa, and ed25519) if they do not already exist" [^8]. Without these keys, the SSH daemon cannot start.

However most of the time this will already have happened automatically and you won't have to do this yourself.

**2. Start the SSH daemon:**

```bash
sudo /usr/sbin/sshd
```

**3. Verify the SSH server is running:**

```bash
ps aux | grep sshd
```

You should see the sshd process running.

### Step 2: Connect from the Client

In the **client terminal**, perform the following steps:

**1. Connect to the SSH server:**

```bash
ssh admin@ssh-server
```

**2. When prompted, type `yes` to accept the server's host key:**

When you connect, you will see a message like this:

```
The authenticity of host 'ssh-server (172.x.x.x)' can't be established.
ED25519 key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxxx.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
```

#### What is a Fingerprint?

Remember the host keys we generated earlier on the server? This is where they come into play. A fingerprint is a short, unique identifier derived from the server's public host key using a hash function (like SHA256). Since public keys are very long, fingerprints provide a shorter way to verify a key's identity [^9][^4].

#### Why does this matter?

This verification step protects you against **server spoofing** or **man-in-the-middle attacks**. Without it, an attacker could intercept your connection and pretend to be the server, capturing your password or data. By verifying the fingerprint, you ensure you're connecting to the real server [^9][^3].

#### How to verify a fingerprint

In a secure environment, you would obtain the server's fingerprint through a trusted channel [^9] (e.g., from the system administrator in person, via a secure channel, or from documentation) and compare it to what SSH displays. If they match, you can safely type `yes`.

Once you accept the fingerprint, SSH stores the host key in your `~/.ssh/known_hosts` (or `/etc/ssh/ssh_known_hosts` if the user is root) file. On future connections, SSH automatically compares the server's key against this stored copy. If the key has changed unexpectedly, SSH will warn you and disables pasword authentication [^3]. This could indicate an attack or simply that the server was reinstalled.

For this tutorial, type `yes` to continue.

**3. Enter the password when prompted:**

```
admin@ssh-server's password: admin123
```

**4. You are now connected!** You should see a new prompt like:

```
[admin@ssh-server ~]$
```

### Step 3: Explore Your Connection

Try some commands on the remote server:

```bash
whoami
hostname
pwd
ls -la
```

### Step 4: Exit the SSH Session

To disconnect from the server, type:

```bash
exit
```

You will return to the client's shell.

---

**Congratulations!** You have successfully:

- Configured an SSH server with password authentication
- Connected to a remote machine using SSH
- Executed commands on a remote system
- Safely disconnected from the session

---

## Exercise 2: Make it more secure

---

## Additional Resources

- OpenSSH Official Website: https://www.openssh.com/
- OpenSSH Manual Pages: https://www.openssh.org/manual.html
- OpenBSD SSH Manual: https://man.openbsd.org/ssh
- Linux SSH Manual: https://man7.org/linux/man-pages/man1/ssh.1.html

https://learn.microsoft.com/en-us/azure/devops/repos/git/use-ssh-keys-to-authenticate?view=azure-devops

https://datatracker.ietf.org/doc/html/rfc4251#section-4.1

## References

[^1]: OpenSSH. "OpenSSH Official Website." https://www.openssh.org/
[^2]: Red Hat Documentation. "Chapter 12. OpenSSH | System Administrator's Guide." https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/system_administrators_guide/ch-openssh
[^3]: OpenBSD. "ssh(1) - OpenSSH remote login client." https://man.openbsd.org/ssh
[^4]: Linux Manual Pages. "ssh(1) - OpenSSH remote login client." https://man7.org/linux/man-pages/man1/ssh.1.html
[^5]: Linux Manual Pages. "scp(1) - OpenSSH secure file copy." https://man7.org/linux/man-pages/man1/scp.1.html
[^6]: OpenBSD. "scp(1) - OpenSSH secure file copy." https://man.openbsd.org/scp.1
[^7]: Cloudflare. "What is SSH?" https://www.cloudflare.com/learning/access-management/what-is-ssh/
[^8]: OpenBSD. "ssh-keygen(1) - OpenSSH authentication key utility." https://man.openbsd.org/ssh-keygen
[^9]: Ylonen, T., & Lonvick, C. _"RFC 4251 – The Secure Shell (SSH) Protocol Architecture."_ Internet Engineering Task Force (IETF). https://datatracker.ietf.org/doc/html/rfc4251
