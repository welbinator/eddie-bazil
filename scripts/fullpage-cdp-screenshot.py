#!/usr/bin/env python3
"""Full-page screenshot of a LOCAL build via headless Chrome + CDP.

Why: browser_exec/new_tab refuse localhost ("Blocked: URL targets a private or internal
address"), and `google-chrome --screenshot` only captures the viewport. This uses
Page.captureScreenshot with captureBeyondViewport:true for a true full-page PNG.

Usage:
  1. Build + serve:  npm run build && (npx --yes serve dist -l 4321 &)
  2. Start Chrome (terminal background=true, NOT trailing &):
       google-chrome --headless=new --disable-gpu --no-sandbox \
         --remote-debugging-port=9333 --user-data-dir=/tmp/cdp-x about:blank
  3. python3 fullpage-cdp-screenshot.py   # edit PORT/PAGE_URL/OUT below
  4. Cleanup: pkill -f "remote-debugging-port=9333"; pkill -f "serve dist"
"""
import json, urllib.request, socket, base64, struct, os, time

PORT = 9333
PAGE_URL = "http://localhost:4321/"
OUT = "/tmp/fullpage.png"
SETTLE_S = 4.5  # wait for fonts + scroll-reveal before capturing

def http(path, method="GET"):
    r = urllib.request.Request(f"http://127.0.0.1:{PORT}{path}", method=method)
    return json.load(urllib.request.urlopen(r))

# Newer Chrome requires PUT on /json/new (GET -> 405)
tab = http(f"/json/new?{PAGE_URL}", "PUT")
ws = tab["webSocketDebuggerUrl"]
path = ws.split(str(PORT), 1)[1]
s = socket.create_connection(("127.0.0.1", PORT))
key = base64.b64encode(os.urandom(16)).decode()
s.sendall((f"GET {path} HTTP/1.1\r\nHost:127.0.0.1:{PORT}\r\nUpgrade:websocket\r\n"
           f"Connection:Upgrade\r\nSec-WebSocket-Key:{key}\r\nSec-WebSocket-Version:13\r\n\r\n").encode())
s.recv(4096)
mid = 0
def send(method, params=None):
    global mid; mid += 1
    msg = json.dumps({"id": mid, "method": method, "params": params or {}}).encode()
    hdr = bytearray([0x81]); l = len(msg); m = os.urandom(4)
    if l < 126: hdr.append(0x80 | l)
    elif l < 65536: hdr.append(0x80 | 126); hdr += struct.pack(">H", l)
    else: hdr.append(0x80 | 127); hdr += struct.pack(">Q", l)
    hdr += m; hdr += bytes(b ^ m[i % 4] for i, b in enumerate(msg))
    s.sendall(hdr); return mid
def recv():
    b = s.recv(2); l = b[1] & 0x7f
    if l == 126: l = struct.unpack(">H", s.recv(2))[0]
    elif l == 127: l = struct.unpack(">Q", s.recv(8))[0]
    data = b""
    while len(data) < l: data += s.recv(l - len(data))
    return json.loads(data)
def wait(i):
    while True:
        msg = recv()
        if msg.get("id") == i: return msg

send("Page.enable"); recv()
time.sleep(SETTLE_S)
r = wait(send("Page.captureScreenshot",
              {"format": "png", "captureBeyondViewport": True, "fromSurface": True}))
open(OUT, "wb").write(base64.b64decode(r["result"]["data"]))
print("OK", OUT, os.path.getsize(OUT))
