## Git Over SSH: You Don't Need GitHub

Most developers assume they need GitHub, GitLab, or some other hosted service to collaborate on code. But here's a secret: if you have an SSH server, you already have a Git server. This is actually how GitHub works under the hood.

In this exercise, you will set up your own Git server using nothing but SSH and bare repositories.

### What is a Bare Repository?

A normal Git repository has two parts:

1. Your working files (the actual code you edit)
2. The `.git` folder (Git's internal database)

A **bare repository** contains only the `.git` folder contents - no working files. This is exactly what you want for a remote server, because:

- No one edits files directly on the server
- It only exists to receive pushes and serve clones
- It takes up less space

You can recognize a bare repo by its contents - it looks like the inside of a `.git` folder:

```
HEAD
config
hooks/
objects/
refs/
```

### How GitHub Actually Works

Here's something interesting: GitHub is just an SSH server with bare repos. Try this yourself:

```bash
ssh git@github.com
```

You'll see:

```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

It's an SSH server - just without shell access. When you clone from GitHub using SSH:

```
git@github.com:username/repo.git
```

This is an SSH URL pointing to a bare repository on GitHub's servers. You can do the exact same thing with your own SSH server.

---

## Exercise 5: Setting Up Your Own Git Server

In this exercise, you will create a bare repository on the server and use it as a remote Git server.

### Prerequisites

Make sure you have completed the previous exercises and have:

- SSH key authentication set up
- SSH running on port 1234

### Step 1: Create a Bare Repository on the Server

In the **server terminal**, create a bare repository:

```bash
cd ~
git init --bare myproject.git
```

You should see:

```
Initialized empty Git repository in /home/admin/myproject.git/
```

Explore the bare repository structure:

```bash
ls myproject.git/
```

You'll see:

```
HEAD  branches  config  description  hooks  info  objects  refs
```

This is identical to what you'd find inside a `.git` folder.

### Step 2: Clone the Repository to the Client

In the **client terminal**, clone the bare repository using an SSH URL:

```bash
cd ~
git clone ssh://admin@ssh-server:1234/home/admin/myproject.git
```

Let's break down this SSH URL:

- `ssh://` - The protocol
- `admin@ssh-server` - User and hostname
- `:1234` - The SSH port
- `/home/admin/myproject.git` - Absolute path to the bare repo

Enter your key passphrase when prompted. You should see:

```
Cloning into 'myproject'...
warning: You appear to have cloned an empty repository.
```

The warning is expected - we haven't added any files yet.

### Step 3: Add Files and Push

In the **client terminal**, create a simple project:

```bash
cd myproject
```

Create a Hello World program:

```bash
cat > hello.c << 'EOF'
#include <stdio.h>

int main() {
    printf("Hello World!\n");
    return 0;
}
EOF
```

Now add, commit, and push:

```bash
git add hello.c
git commit -m "Add Hello World"
git push
```

Enter your passphrase when prompted. You should see:

```
Enumerating objects: 3, done.
Counting objects: 100% (3/3), done.
Writing objects: 100% (3/3), 254 bytes | 254.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
To ssh://ssh-server:1234/home/admin/myproject.git
 * [new branch]      master -> master
```

### Step 4: Verify on the Server

In the **server terminal**, verify the commit was received:

```bash
cd ~/myproject.git
git log --oneline
```

You should see:

```
abc1234 Add Hello World
```

The bare repository received your push. Anyone with SSH access can now clone this repository.

### Step 5: Simulate a Second Developer

Let's simulate another developer cloning and contributing to the project. In the **server terminal**, clone the repo to a different location:

```bash
cd /tmp
git clone /home/admin/myproject.git myproject-copy
cd myproject-copy
```

Make a change:

```bash
cat > README.md << 'EOF'
# My Project

A simple Hello World program.
EOF

git add README.md
git commit -m "Add README"
git push
```

### Step 6: Pull the Changes on the Client

Back in the **client terminal**, pull the changes:

```bash
cd ~/myproject
git pull
```

You should see:

```
remote: Enumerating objects: 4, done.
remote: Counting objects: 100% (4/4), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (3/3), done.
From ssh://ssh-server:1234/home/admin/myproject.git
   abc1234..def5678  master     -> origin/master
Updating abc1234..def5678
Fast-forward
 README.md | 3 +++
 1 file changed, 3 insertions(+)
 create mode 100644 README.md
```

Verify the file is there:

```bash
cat README.md
```

---

**Congratulations!** You have successfully:

- Created a bare Git repository on a remote server
- Cloned it using an SSH URL
- Pushed and pulled changes through SSH
- Simulated collaboration between multiple developers

---

## Understanding SSH URLs for Git

Git supports several SSH URL formats:

| Format | Example |
| ------ | ------- |
| SCP-style | `admin@ssh-server:myproject.git` |
| SSH protocol with port | `ssh://admin@ssh-server:1234/path/to/repo.git` |
| SSH protocol default port | `ssh://admin@ssh-server/path/to/repo.git` |

The SCP-style format (`user@host:path`) is shorter but doesn't support custom ports. Use the full `ssh://` URL when you need to specify a port.

## Access Control

One major advantage of Git over SSH: access control comes for free.

- **Read/write access**: Anyone in the server's `~/.ssh/authorized_keys` can clone and push
- **No access**: Anyone not in `authorized_keys` cannot access the repos

For more granular control (e.g., read-only access for some users), you can:

- Use separate system users with different permissions
- Look into tools like Gitolite that manage Git access control over SSH

## When to Use GitHub vs Your Own Server

| Use Your Own SSH Server | Use GitHub/GitLab |
| ----------------------- | ----------------- |
| Private projects | Open source projects |
| Full control needed | Need issue tracking, PRs, CI/CD |
| Simple collaboration | Large team collaboration |
| Learning/experimentation | Public visibility desired |

---

## Additional Resources

- Pro Git Book, Chapter 4: "Git on the Server" - https://git-scm.com/book/en/v2/Git-on-the-Server-The-Protocols
- Gitolite (Git access control): https://gitolite.com/
