#!/usr/bin/env python3
import json, os, base64, random, socket, urllib.request
from dnslib.server import DNSServer, BaseResolver
from dnslib import DNSRecord
import pystray
from PIL import Image, ImageDraw

LISTEN_PORT = 5353
UPSTREAM_RESOLVERS = ["9.9.9.9", "208.67.222.222"]
PEERS_FILE = os.path.expanduser("~/interstellar-node/peers.json")
GITHUB_PEERS_URL = "https://raw.githubusercontent.com/nardaxxx/dpnn_peers/main/peers.json"
GITHUB_API_URL = "https://api.github.com/repos/nardaxxx/dpnn_peers/contents/peers.json"
GITHUB_TOKEN = "YOUR_TOKEN_HERE"
peers = []

def load_peers():
    global peers
    if os.path.exists(PEERS_FILE):
        with open(PEERS_FILE) as f:
            peers = json.load(f)

def save_peers():
    with open(PEERS_FILE, "w") as f:
        json.dump(peers, f)

def fetch_peers_from_github():
    try:
        with urllib.request.urlopen(GITHUB_PEERS_URL, timeout=5) as r:
            return json.loads(r.read().decode())
    except:
        return []

def get_public_ip():
    try:
with urllib.request.urlopen("https://api.ipify.org?format=json", timeout=5) as r:
            data = json.loads(r.read().decode())
            return data["ip"], 5353
    except:
        return None, None

def update_github_peers(ip, port):
    try:
        req = urllib.request.Request(GITHUB_API_URL, headers={"Authorization": f"token {GITHUB_TOKEN}"})
        with urllib.request.urlopen(req) as r:
            data = json.loads(r.read().decode())
            sha = data["sha"]
            current = json.loads(base64.b64decode(data["content"]).decode())
        entry = {"ip": ip, "port": port}
        if entry not in current:
            current.append(entry)
        content = base64.b64encode(json.dumps(current).encode()).decode()
        payload = json.dumps({"message": "node join", "content": content, "sha": sha}).encode()
        req = urllib.request.Request(
            GITHUB_API_URL,
            data=payload,
            headers={"Authorization": f"token {GITHUB_TOKEN}", "Content-Type": "application/json"},
            method="PUT"
        )
        urllib.request.urlopen(req)
        print(f"Registered on GitHub: {ip}:{port}")
    except Exception as e:
        print(f"GitHub update failed: {e}")

class DPNNResolver(BaseResolver):
    def resolve(self, request, handler):
        upstream = random.choice(UPSTREAM_RESOLVERS)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(3)
            sock.sendto(request.pack(), (upstream, 53))
            data, _ = sock.recvfrom(4096)
            sock.close()
            return DNSRecord.parse(data)
        except:
            return request.reply()

def create_icon():
    img = Image.new("RGB", (64, 64), color=(30, 30, 30))
    d = ImageDraw.Draw(img)
    d.ellipse([16, 16, 48, 48], fill=(0, 200, 100))
    return img

def run_tray(server):
    def on_quit(icon, item):
        server.stop()
        icon.stop()
    menu = pystray.Menu(
        pystray.MenuItem(f"Interstellar Node — peers: {len(peers)}", lambda i, it: None),
        pystray.MenuItem("Quit", on_quit)
    )
    icon = pystray.Icon("IN", create_icon(), "Interstellar Node", menu)
    icon.run()

if __name__ == "__main__":
    print("Interstellar Node starting...")
    github_peers = fetch_peers_from_github()
    peers.extend(github_peers)
    load_peers()
    save_peers()
    print(f"Peers from GitHub: {len(github_peers)}")
    public_ip, public_port = get_public_ip()
    if public_ip:
        print(f"Public IP: {public_ip}:{public_port}")
        update_github_peers(public_ip, public_port)
    else:
        print("Could not determine public IP")
    resolver = DPNNResolver()
    server = DNSServer(resolver, port=LISTEN_PORT, address="0.0.0.0")
    server.start_thread()
    print(f"Interstellar Node listening on port {LISTEN_PORT}")
    print(f"Upstream resolvers: {UPSTREAM_RESOLVERS}")
    run_tray(server)
