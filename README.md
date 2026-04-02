# interstellar-node
P2P network of DNS nodes bypassing CGNAT
# Interstellar Node

P2P network of DNS nodes that communicate directly, bypassing CGNAT.

## What it does

Each user who installs the program becomes a network node. The node:
- Discovers its public IP automatically
- Registers on the shared peer list
- Connects directly to other nodes through CGNAT via UDP hole punching
- Acts as a local DNS resolver for the host device
- Shares and updates the peer list directly with other nodes

## How it works

1. Node starts → discovers public IP via ipify
2. Downloads peer list from GitHub registry
3. Registers itself on the list
4. Connects directly to known peers
5. Resolves DNS queries locally

The GitHub registry is only the bootstrap entry point. Once connected, the network is fully autonomous. If the list is deleted, connected nodes regenerate it from their local copies.

## Current status

- Public IP discovery ✅
- GitHub peer registration ✅
- CGNAT bypass ✅
- Local DNS resolver ✅
- Direct peer exchange — in development
- Windows EXE — in development

## Installation (Linux)

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
mkdir -p ~/interstellar-node
cd ~/interstellar-node
python3 -m venv venv
source venv/bin/activate
pip install dnslib pystray pillow
nano node.py
```

Paste the node code inside, save with CTRL+O then CTRL+X, then run:

```bash
python3 node.py
```

## Restart after reboot

```bash
cd ~/interstellar-node
source venv/bin/activate
python3 node.py
```

## Configuration

Edit node.py and set your GitHub token:

```python
GITHUB_TOKEN = "your_token_here"
```

## Peer registry

github.com/nardaxxx/dpnn_peers

## License

All rights reserved — © Giovanni Nardacci
