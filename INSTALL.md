# Interstellar Node — Installation Guide

## Requirements

- Windows 10 or 11
- Python 3.11 from python.org (NOT Microsoft Store version)

## Step 1 — Install dependencies

```cmd
pip install pystray
pip install pillow pyinstaller dnslib
Step 2 — Download the node
curl -o node.py https://raw.githubusercontent.com/nardaxxx/interstellar-node/main/node.py
Step 3 — Add your GitHub token
Open node.py in Notepad and replace:
GITHUB_TOKEN = "YOUR_TOKEN_HERE"
with your real token from github.com/settings/tokens (scope: public_repo)
Also set:
PEERS_FILE = "peers.json"
Step 4 — Test before compiling
py node.py
If it starts and shows a green icon in the tray — it works.
Step 5 — Compile to EXE
py -m PyInstaller --clean --onefile --noconsole --collect-all pystray node.py
EXE will be in: dist\node.exe
Peer registry
github.com/nardaxxx/dpnn_peers
Known issues
Use py not python if multiple Python versions are installed
Microsoft Store Python does NOT work
pystray requires --collect-all pystray flag, not --hidden-import
