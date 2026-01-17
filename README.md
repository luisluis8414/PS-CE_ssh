# PS-CE_ssh

An SSH tutorial environment using Docker containers.

## Quick Start

### 1. Setup

```bash
cd infrastructure
docker compose up -d
```

### 2. Connect to Containers

```bash
# Server container
docker exec -it ssh-server bash -l

# Client container
docker exec -it ssh-client bash -l
```

## Maintenance

| Action                             | Command                                               |
| ---------------------------------- | ----------------------------------------------------- |
| Restart (fresh setup)              | `docker compose down && docker compose up -d`         |
| Rebuild (after Dockerfile changes) | `docker compose down && docker compose up -d --build` |
| Stop containers                    | `docker compose down`                                 |

## Fun

```bash
ssh starwarstel.net
```
