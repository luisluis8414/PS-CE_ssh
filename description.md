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

Every SSH server needs its own unique cryptographic keys, called host keys, to identify itself to clients.

`ssh-keygen` is used to generate these host keys [^8]. Generate the host keys by running:

```bash
sudo ssh-keygen -A
```

The `-A` flag generates host keys of all default key types (rsa, ecdsa, and ed25519) if they do not already exist [^8]. Multiple key types are generated to ensure compatibility with different SSH clients. Older clients may only support RSA, while modern clients prefer Ed25519. Without these keys, the SSH daemon cannot start.

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

Then when prompted enter the admins user password.

You should now be connected to the server!

You can type `exit` to close the connection.

### Step 2.5: Understanding Host Key Verification in Practice

Now that you have connected once and accepted the server's host key, let's see what happens when a server's key changes unexpectedly.

**1. First, exit the SSH session if you're still connected:**

```bash
exit
```

**2. On the server terminal, delete the existing host keys and generate new ones:**

```bash
sudo rm /etc/ssh/ssh_host_*
sudo ssh-keygen -A
```

**3. Restart the ssh server:**

```bash
sudo pkill sshd
sudo /usr/sbin/sshd
```

**4. On the client terminal, try to connect again:**

```bash
ssh admin@ssh-server
```

You will see a warning message like this:

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ED25519 key sent by the remote host is
SHA256:xxxxxxxxxxxxxxxxxxxxx.
Please contact your system administrator.
Add correct host key in /home/student/.ssh/known_hosts to get rid of this message.
Offending key in /home/student/.ssh/known_hosts:1
Host key for ssh-server has changed and you have requested strict checking.
Host key verification failed.
```

#### What just happened?

SSH detected that the server's host key is different from the one stored in your `~/.ssh/known_hosts` file. This is exactly what SSH is designed to do: protect you from connecting to a server that might not be who it claims to be.

#### Why can't an attacker just copy the fingerprint?

You might wonder, if the fingerprint is derived from the public key, and public keys are meant to be shared, why can't an attacker simply copy the server's public key and pretend to be the server?

The answer lies in how SSH verifies the server's identity. During the connection, SSH doesn't just check if the server _has_ the public key, it verifies that the server _owns_ the corresponding private key. This is done through a cryptographic challenge. The client sends a challenge that can only be correctly answered by someone who possesses the private key to the public key used for the identification.

An attacker can copy the public key and fingerprint, but without the private key (which never leaves the server), they cannot prove ownership. This is why protecting the server's private key is critical - if an attacker obtains both the public and private key, they can fully impersonate the server.

In a real scenario, this warning could mean:

- **Legitimate cause**: The server was reinstalled, or the administrator regenerated the host keys
- **Security threat**: An attacker is impersonating the server (man-in-the-middle attack)

#### Resolving the warning

Since we know we intentionally changed the server's keys, we can safely remove the old key from our known_hosts file:

```bash
ssh-keygen -R ssh-server
```

You should see:

```
# Host ssh-server found: line 1
/home/student/.ssh/known_hosts updated.
Original contents retained as /home/student/.ssh/known_hosts.old
```

Now connect again:

```bash
ssh admin@ssh-server
```

You will be prompted to verify the new fingerprint, just like the first time. Type `yes` to accept it.

---

**Key takeaway**: Never blindly remove a host key warning in a production environment. Always verify with your system administrator that the key change was intentional before proceeding.

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
2. **Passphrase**: Enter a secure passphrase

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
(You can search in nano using ctrl + f)

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
3. **Securing your key** - Even if your private key is stolen, the attacker still needs your passphrase

---

## What is SCP?

**SCP** (Secure Copy Protocol) is a command-line tool that uses SSH to securely transfer files between a local and a remote host, or between two remote hosts [^5][^6]. It provides the same level of encryption and authentication as SSH itself.

### Basic SCP Syntax

```bash
scp [options] source destination
```

Where source and destination can be:

- A local path: `/path/to/file`
- A remote path: `user@host:/path/to/file`

Common options include:

| Option | Description                            |
| ------ | -------------------------------------- |
| `-P`   | Specify the SSH port (uppercase P!)    |
| `-r`   | Recursively copy entire directories    |
| `-p`   | Preserve modification times and modes  |
| `-q`   | Quiet mode, suppresses progress output |

---

## What is SFTP?

**SFTP** (SSH File Transfer Protocol) is an interactive file transfer program that works over SSH [^1]. Unlike SCP, which is designed for simple file copies, SFTP provides an interactive session where you can navigate directories, list files, and perform multiple operations.

### SCP vs SFTP

| Feature           | SCP                        | SFTP                          |
| ----------------- | -------------------------- | ----------------------------- |
| Mode              | Non-interactive            | Interactive                   |
| Use case          | Single file/directory copy | Multiple operations, browsing |
| Resume transfers  | No                         | Yes                           |
| Directory listing | No                         | Yes                           |

---

## Exercise 3: Transferring Files with SCP and SFTP

In this exercise, you will transfer a simple Python web server from the client to the server using both SCP and SFTP.

### Step 1: Examine the Web Server

In the **client terminal**, there is already a simple Python web server file. Take a look at it:

```bash
cat server.py
```

You should see:

```python
from http.server import HTTPServer, BaseHTTPRequestHandler

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'''
<!DOCTYPE html>
<html>
<head><title>SSH Tutorial</title></head>
<body style="font-family: monospace; text-align: center; padding: 50px;">
    <h1>Hello from the server!</h1>
</body>
</html>
''')

    def log_message(self, format, *args):
        print(f"Request received: {args[0]}")

print("Server running on port 8080...")
print("Press Ctrl+C to stop")
HTTPServer(('127.0.0.1', 8080), MyHandler).serve_forever()
```

This is a minimal HTTP server that:

- Listens only on `127.0.0.1` (localhost), making it inaccessible from outside the server
- Returns a custom HTML page with a success message
- Runs on port 8080

### Step 2: Transfer the File Using SCP

Now let's copy the file to the server using SCP:

```bash
scp -P 1234 server.py admin@ssh-server:~/
```

Let's break down this command:

- `-P 1234`: Connect to SSH on port 1234 (note: uppercase P for SCP, lowercase p for SSH)
- `server.py`: The local file to copy
- `admin@ssh-server:~/`: The destination - the admin user's home directory on ssh-server

Enter your key passphrase when prompted. You should see output like:

```
server.py                                     100%  195    50.0KB/s   00:00
```

### Step 3: Verify the Transfer

Connect to the server and verify the file exists:

```bash
ssh -p 1234 admin@ssh-server
```

```bash
ls -la server.py
cat server.py
```

The file should be present with the same content. Exit the session:

```bash
exit
```

### Step 4: Transfer Files Using SFTP

Now let's explore SFTP's interactive mode. First, remove the file from the server so we can transfer it again:

```bash
ssh -p 1234 admin@ssh-server "rm server.py"
```

Start an SFTP session:

```bash
sftp -P 1234 admin@ssh-server
```

You will see an interactive prompt:

```
sftp>
```

#### Exploring SFTP Commands

Try these commands to explore the SFTP interface:

```sftp
pwd           # Print remote working directory
lpwd          # Print local working directory
ls            # List remote files
lls           # List local files
```

Notice the pattern: commands prefixed with `l` operate on the **l**ocal machine.

#### Uploading the File

Upload the server file:

```sftp
put server.py
```

Verify it was uploaded:

```sftp
ls -la
```

You should see `server.py` in the listing.

#### Other Useful SFTP Commands

| Command         | Description                 |
| --------------- | --------------------------- |
| `get filename`  | Download a file from server |
| `put filename`  | Upload a file to server     |
| `mget *.txt`    | Download multiple files     |
| `mput *.txt`    | Upload multiple files       |
| `mkdir dirname` | Create remote directory     |
| `rm filename`   | Delete remote file          |
| `cd dirname`    | Change remote directory     |
| `lcd dirname`   | Change local directory      |
| `help`          | Show all available commands |

Exit the SFTP session:

```sftp
bye
```

---

**Congratulations!** You have successfully:

- Created a simple Python web server
- Transferred files using SCP
- Used SFTP interactively to upload files and navigate directories

---

## What is SSH Port Forwarding?

**SSH Port Forwarding** (also called SSH tunneling) allows you to securely forward network traffic through an encrypted SSH connection [^3][^7]. This is useful for:

- Accessing services that are only available on localhost
- Bypassing firewalls securely
- Encrypting traffic for protocols that don't have built-in encryption

### Types of Port Forwarding

| Type                    | Flag | Description                                     |
| ----------------------- | ---- | ----------------------------------------------- |
| Local Port Forwarding   | `-L` | Forward a local port to a remote destination    |
| Remote Port Forwarding  | `-R` | Forward a remote port to a local destination    |
| Dynamic Port Forwarding | `-D` | Create a SOCKS proxy through the SSH connection |

In this exercise, we will focus on **Local Port Forwarding**.

### Local Port Forwarding Syntax

```bash
ssh -L [local_address:]local_port:destination_address:destination_port user@ssh_server
```

For example:

```bash
ssh -L 9000:127.0.0.1:8080 admin@server
```

This forwards `localhost:9000` on your machine to `127.0.0.1:8080` on the server.

---

## Exercise 4: SSH Port Forwarding

In this exercise, you will start the web server on the remote machine and use SSH port forwarding to access it from the client.

### The Scenario

The web server we transferred binds to `127.0.0.1:8080`. This means:

- It only accepts connections from the server itself (localhost)
- It cannot be accessed directly from the client or any other machine

SSH port forwarding allows us to securely access this localhost-only service from our client machine.

### Step 1: Start the Web Server on the Server

In the **server terminal**, start the Python web server:

```bash
cd ~
python3 server.py &
```

The `&` runs the server in the background. You should see:

```
Server running on port 8080...
Press Ctrl+C to stop
```

Press Enter to get your prompt back.

Verify the server is running:

```bash
curl http://127.0.0.1:8080
```

You should see the HTML response:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>SSH Tutorial</title>
  </head>
  <body style="font-family: monospace; text-align: center; padding: 50px;">
    <h1>Hello from the server!</h1>
  </body>
</html>
```

This confirms the server is working locally.

### Step 2: Verify the Server is Not Accessible from the Client

In the **client terminal**, try to access the server directly:

```bash
curl http://ssh-server:8080
```

This will fail with a connection refused error because the server only listens on `127.0.0.1`, not on the network interface.

### Step 3: Set Up Local Port Forwarding

Now let's create an SSH tunnel to access the server. In the **client terminal**:

```bash
ssh -p 1234 -L 9000:127.0.0.1:8080 -f -N admin@ssh-server
```

Let's break down this command:

- `-p 1234`: Connect to SSH on port 1234
- `-L 9000:127.0.0.1:8080`: Forward local port 9000 to 127.0.0.1:8080 on the server
- `-f`: Run SSH in the background after authentication
- `-N`: Don't execute a remote command (just forward ports)
- `admin@ssh-server`: The SSH server to connect through

Enter your key passphrase. The tunnel is now running in the background.

You can verify the tunnel is running:

```bash
ps aux | grep ssh
```

### Step 4: Access the Server Through the Tunnel

Now access the forwarded port:

```bash
curl http://127.0.0.1:9000
```

You should see the HTML response:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>SSH Tutorial</title>
  </head>
  <body style="font-family: monospace; text-align: center; padding: 50px;">
    <h1>Hello from the server!</h1>
  </body>
</html>
```

The same output we saw on the server! The traffic flows like this:

```
Client (curl) → localhost:9000 → [SSH Tunnel] → ssh-server:22 → 127.0.0.1:8080 (Python server)
```

### Step 5: Understanding the Traffic Flow

Here's what happens when you access `localhost:9000`:

1. Your curl request connects to `localhost:9000` on the client
2. SSH intercepts this connection and encrypts it
3. The encrypted traffic travels through the SSH connection to the server
4. On the server, SSH decrypts the traffic and forwards it to `127.0.0.1:8080`
5. The Python server responds, and the response travels back through the tunnel

All traffic is encrypted, and the server remains inaccessible from the network.

### Step 6: Clean Up

Stop the SSH tunnel by killing the background SSH process:

```bash
pkill -f "ssh -p 1234 -L"
```

In the **server terminal**, stop the Python server:

```bash
pkill python3
```

---

**Congratulations!** You have successfully:

- Started a localhost-only web server
- Created an SSH tunnel using local port forwarding
- Accessed a remote localhost service securely through the tunnel
- Understood how SSH port forwarding protects and enables access to internal services

---

## Port Forwarding Summary

| What we did                    | Command                                                  |
| ------------------------------ | -------------------------------------------------------- |
| Start server (server)          | `python3 server.py &`                                    |
| Create tunnel (client)         | `ssh -p 1234 -L 9000:127.0.0.1:8080 -N admin@ssh-server` |
| Access through tunnel (client) | `curl http://127.0.0.1:9000`                             |

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
