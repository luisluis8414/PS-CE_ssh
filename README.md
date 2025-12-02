# PS-CE_ssh

https://www.jfranken.de/homepages/johannes/vortraege/ssh3.de.html

Themen:

1. SSH
   1. Keygen
   2. Logins im Vergleich
      -> Passwort, Key, Key with passphrase, ssh agent
   3. Tunnel
   4. Fingerprint --> SHA1 MD5 Collisions, storing, usage
2. SCP
   1. SCP vs FTP
   2. SFTP

Fokus auf Verwendung von SSH, Fingerprint Yes/no --> Keygen Bildchen und Keyaustausch

Advanced: Package Typing analysis, Zeit zwischen Paket senden und Eingabe

## Restart (fresh setup from 0)

```
docker compose down && docker compose up -d
```

## Rebuild (when change in Dockerfile)

```
docker compose down && docker compose up -d --build
```

## Connect to client or server

```
# For the server container
docker exec -it ssh-server bash -l

# For the client container
docker exec -it ssh-client bash -l
```
## Questions: 

- ps not installed in the base image of rocky linux? Fine to install such things?
- should create default users or keep image minimal?

