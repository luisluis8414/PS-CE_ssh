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

**2. Accept the servers host key:**

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

## Exercise 2: Securing Your SSH Setup

In Exercise 1, we used password authentication, which is simple but less secure. Passwords can be guessed, brute forced, or stolen. In this exercise, we will implement several security best practices:

1. Change the SSH port from the default (22) to a non standard port
2. Set up public key authentication
3. Disable password authentication entirely

### Step 1: Generate an SSH Key Pair on the Client

In the **client terminal**, generate a new SSH key pair:

```bash
ssh-keygen -t ed25519 -C "student@ssh-client"
```

You will be prompted for:

1. **File location**: Press Enter to accept the default (`~/.ssh/id_ed25519`)
2. **Passphrase**: Enter a secure passphrase (e.g., `MySecurePass123!`)

```
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/student/.ssh/id_ed25519):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
```

#### What is a Passphrase?

A passphrase adds an extra layer of security to your private key. Even if someone steals your private key file, they cannot use it without knowing the passphrase [^8]. Think of it as a password that protects your key.

#### Understanding the Key Pair

This command creates two files [^8]:

| File                    | Description                                                 |
| ----------------------- | ----------------------------------------------------------- |
| `~/.ssh/id_ed25519`     | Your **private key** - keep this secret and never share it! |
| `~/.ssh/id_ed25519.pub` | Your **public key** - this can be shared freely             |

You can view your public key with:

```bash
cat ~/.ssh/id_ed25519.pub
```

### Step 2: Copy the Public Key to the Server

Now we need to install your public key on the server. The `ssh-copy-id` command automates this process:

```bash
ssh-copy-id admin@ssh-server
```

Enter the password (`admin123`) when prompted. This command copies your public key to the server's `~/.ssh/authorized_keys` file.

You should see output like:

```
Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'admin@ssh-server'"
and check to make sure that only the key(s) you wanted were added.
```

### Step 3: Test Key Authentication

Try connecting to the server again:

```bash
ssh admin@ssh-server
```

This time, instead of asking for the server password, SSH will ask for your **key passphrase**:

```
Enter passphrase for key '/home/student/.ssh/id_ed25519':
```

Enter the passphrase you created earlier. You should now be logged in!

Exit the session:

```bash
exit
```

### Step 4: Change the SSH Port

Using the default port 22 makes your server an easy target for automated attacks. Changing to a non standard port reduces this risk [^3].

In the **server terminal**:

**1. Edit the SSH daemon configuration:**

```bash
sudo nano /etc/ssh/sshd_config
```

**2. Find the line `#Port 22` and change it to:**

```
Port 1234
```

(Remove the `#` to uncomment the line)

**3. Save the file** (Ctrl+O, Enter, Ctrl+X)

**4. Restart the SSH daemon:**

First, stop the current daemon:

```bash
sudo pkill sshd
```

Then start it again:

```bash
sudo /usr/sbin/sshd
```

### Step 5: Connect Using the New Port

In the **client terminal**, try connecting without specifying the port:

```bash
ssh admin@ssh-server
```

This will fail because SSH still tries port 22 by default.

Now connect using the `-p` flag to specify the new port:

```bash
ssh -p 1234 admin@ssh-server
```

Enter your passphrase when prompted. You should be connected!

Exit the session:

```bash
exit
```

### Step 6: Disable Password Authentication

Now that key authentication works, we can disable password authentication entirely. This means only users with a valid key can connect.

In the **server terminal**:

**1. Edit the SSH daemon configuration:**

```bash
sudo nano /etc/ssh/sshd_config
```

**2. Find and modify these lines:**

```
PasswordAuthentication no
PubkeyAuthentication yes
```

**3. Save the file** (Ctrl+O, Enter, Ctrl+X)

**4. Restart the SSH daemon:**

```bash
sudo pkill sshd
sudo /usr/sbin/sshd
```

### Step 7: Verify Password Authentication is Disabled

In the **client terminal**, let's verify that password authentication no longer works.

First, try connecting with a forced password authentication:

```bash
ssh -p 1234 -o PubkeyAuthentication=no admin@ssh-server
```

This should fail with:

```
admin@ssh-server: Permission denied (publickey).
```

Now connect normally with your key:

```bash
ssh -p 1234 admin@ssh-server
```

Enter your passphrase and you should be connected!

---

**Congratulations!** You have successfully:

- Generated an SSH key pair with a passphrase
- Installed your public key on the server using `ssh-copy-id`
- Changed the SSH port to a non-standard port
- Disabled password authentication
- Verified that only key authentication works

---

### Security Summary

| Before                   | After                            |
| ------------------------ | -------------------------------- |
| Port 22 (default)        | Port 1234 (non-standard)         |
| Password authentication  | Public key authentication        |
| No passphrase protection | Passphrase-protected private key |

These changes significantly improve your SSH security by:

1. **Reducing automated attacks** - Most bots scan only port 22
2. **Eliminating password guessing** - No password means no brute force attacks
3. **Adding defense in depth** - Even if your private key is stolen, the attacker still needs your passphrase

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
