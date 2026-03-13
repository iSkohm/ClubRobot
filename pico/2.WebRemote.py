

## class robot.py

from machine import Pin, PWM
import time

class Servo:
    STOP    = 4915  # ~1.5ms
    CW_MAX  = 3276  # ~1.0ms
    CCW_MAX = 6553  # ~2.0ms

    def __init__(self, pin, reversed=False):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)
        self.reversed = reversed
        self.stop()

    def _duty(self, val):
        self.pwm.duty_u16(self.CCW_MAX if (val and not self.reversed) or (not val and self.reversed) else self.CW_MAX)

    def forward(self):  self._duty(True)
    def backward(self): self._duty(False)
    def stop(self):     self.pwm.duty_u16(self.STOP)


class Robot:
    def __init__(self, pin_left, pin_right):
        self.left  = Servo(pin_left,  reversed=False)
        self.right = Servo(pin_right, reversed=True)  # mirrored mounting

    def avance(self, t=2):
        self.left.forward();  self.right.forward()
        time.sleep(t);        self.stop()

    def recule(self, t=2):
        self.left.backward(); self.right.backward()
        time.sleep(t);        self.stop()

    def tourne_gauche(self, t=1):
        self.left.backward(); self.right.forward()
        time.sleep(t);        self.stop()

    def tourne_droite(self, t=1):
        self.left.forward();  self.right.backward()
        time.sleep(t);        self.stop()

    def stop(self):
        self.left.stop(); self.right.stop()





###

# main.py

import network, socket, asyncio
from machine import Pin
from robot import Robot

led = Pin("LED", Pin.OUT)
robot = Robot(pin_left=16, pin_right=15)
SSID     = "SSID_ICI"
PASSWORD = "MOT_DE_PASS_WIFI"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    pass
ip = wlan.ifconfig()[0]
print(f"Open http://{ip}")

HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; height: 100vh;
    background: #0a0a0a; font-family: monospace;
    touch-action: none; user-select: none;
  }
  h1 { color: #00ff88; letter-spacing: 4px; font-size: 14px;
       text-transform: uppercase; margin-bottom: 40px; }
  .grid {
    display: grid;
    grid-template-columns: repeat(3, 90px);
    grid-template-rows: repeat(3, 90px);
    gap: 10px;
  }
  .btn {
    display: flex; align-items: center; justify-content: center;
    font-size: 28px; border: 2px solid #333; border-radius: 12px;
    background: #1a1a1a; color: #fff; cursor: pointer;
    transition: background 0.1s, border-color 0.1s, transform 0.1s;
  }
  .btn:active, .btn.active {
    background: #00ff8833;
    border-color: #00ff88;
    transform: scale(0.94);
  }
  .empty { visibility: hidden; }
  #status {
    margin-top: 30px; font-size: 11px; letter-spacing: 2px;
    color: #444; text-transform: uppercase;
  }
  #status.on { color: #00ff88; }
</style>
</head>
<body>
<h1>⬡ Pico Robot</h1>
<div class="grid">
  <div class="empty"></div>
  <div class="btn" id="F">▲</div>
  <div class="empty"></div>
  <div class="btn" id="L">◀</div>
  <div class="btn" id="S">■</div>
  <div class="btn" id="R">▶</div>
  <div class="empty"></div>
  <div class="btn" id="B">▼</div>
  <div class="empty"></div>
</div>
<div id="status">disconnected</div>

<script>
  const status = document.getElementById('status');
  let ws, active = null;

  function connect() {
    ws = new WebSocket(`ws://${location.host}/ws`);
    ws.onopen  = () => { status.textContent = 'connected'; status.className = 'on'; };
    ws.onclose = () => { status.textContent = 'reconnecting...'; status.className = '';
                         setTimeout(connect, 2000); };
  }

  function send(cmd) {
    if (ws && ws.readyState === 1) ws.send(cmd);
  }

  function press(id) {
    if (active && active !== id) release();
    active = id;
    document.getElementById(id).classList.add('active');
    send(id);
  }

  function release() {
    if (active) {
      document.getElementById(active).classList.remove('active');
      active = null;
      send('S');
    }
  }

  ['F','B','L','R','S'].forEach(id => {
    const btn = document.getElementById(id);
    btn.addEventListener('pointerdown', e => { e.preventDefault(); press(id); });
  });

  document.addEventListener('pointerup',    release);
  document.addEventListener('pointercancel', release);

  document.addEventListener('keydown', e => {
    const map = { ArrowUp:'F', ArrowDown:'B', ArrowLeft:'L', ArrowRight:'R', ' ':'S' };
    if (map[e.key]) { e.preventDefault(); press(map[e.key]); }
  });
  document.addEventListener('keyup', e => {
    if (['ArrowUp','ArrowDown','ArrowLeft','ArrowRight',' '].includes(e.key)) {
      e.preventDefault(); release();
    }
  });

  connect();
</script>
</body>
</html>
"""

def ws_handshake(req):
    import ubinascii, hashlib
    key = ""
    for line in req.split("\r\n"):
        if "Sec-WebSocket-Key" in line:
            key = line.split(": ")[1].strip()
    combined = key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    accept = ubinascii.b2a_base64(hashlib.sha1(combined.encode()).digest()).strip()
    return (
        "HTTP/1.1 101 Switching Protocols\r\n"
        "Upgrade: websocket\r\n"
        "Connection: Upgrade\r\n"
        f"Sec-WebSocket-Accept: {accept.decode()}\r\n\r\n"
    )

async def recv_ws_frame(reader):
    """Properly decode a WebSocket frame."""
    header = await reader.readexactly(2)
    opcode = header[0] & 0x0f
    masked  = (header[1] & 0x80) != 0
    length  = header[1] & 0x7f

    if length == 126:
        ext = await reader.readexactly(2)
        length = int.from_bytes(ext, 'big')
    elif length == 127:
        ext = await reader.readexactly(8)
        length = int.from_bytes(ext, 'big')

    mask_key = await reader.readexactly(4) if masked else b''
    data     = await reader.readexactly(length)

    if masked:
        data = bytes(data[i] ^ mask_key[i % 4] for i in range(length))

    return opcode, data

def handle_command(cmd):
    print(f"CMD: {cmd}")
    if   cmd == "F": robot.left.forward();  robot.right.forward()
    elif cmd == "B": robot.left.backward(); robot.right.backward()
    elif cmd == "L": robot.left.backward(); robot.right.forward()
    elif cmd == "R": robot.left.forward();  robot.right.backward()
    elif cmd == "S": robot.stop()
    led.toggle()

async def handle_client(reader, writer):
    try:
        req = await asyncio.wait_for(reader.read(1024), timeout=5)
        req = req.decode()

        if "Upgrade: websocket" in req:
            writer.write(ws_handshake(req).encode())
            await writer.drain()

            while True:
                opcode, data = await recv_ws_frame(reader)
                if opcode == 8:   # close frame
                    break
                elif opcode == 1: # text frame
                    cmd = data.decode().strip()
                    if cmd:
                        handle_command(cmd)
        else:
            writer.write(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
            writer.write(HTML.encode())
            await writer.drain()
    except Exception as e:
        print("Client error:", e)
    finally:
        writer.close()

async def main():
    server = await asyncio.start_server(handle_client, "0.0.0.0", 80)
    print("Server running")
    while True:
        await asyncio.sleep(1)

asyncio.run(main())
