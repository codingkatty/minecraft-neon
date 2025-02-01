import time
import board
import displayio
import framebufferio
import rgbmatrix
import requests
import terminalio
from adafruit_display_text import label

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)

group = displayio.Group()
display.root_group = group

bitmap = displayio.Bitmap(10, 10, 4)
minecraft = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
    [0, 0, 1, 2, 0, 0, 2, 1, 0, 0],
    [0, 0, 0, 0, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 2, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 3, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

minecraft_palette = displayio.Palette(4)
minecraft_palette[0] = 0x0001B53C
minecraft_palette[1] = 0x000123F28
minecraft_palette[2] = 0x000000
minecraft_palette[3] = 0x00044C062

minecraft_tilegrid = displayio.TileGrid(
    bitmap,
    pixel_shader=minecraft_palette,
    x=5,
    y=5
)
group.append(minecraft_tilegrid)

for y in range(10):
    for x in range(10):
        bitmap[x, y] = minecraft[y][x]

playernum = label.Label(terminalio.FONT, text="0", color=0xFFFFFF, x=20, y=9)
group.append(playernum)

onlinetxt = label.Label(terminalio.FONT, text="loadyloady", color=0xFFFFFF, x=3, y=22)
group.append(onlinetxt)

def serverstat():
    response = requests.get("https://api.mcstatus.io/v2/status/java/kayppn.aternos.me")
    data = response.json()

    if data["version"]["name_clean"] != "● Offline":
        onlinetxt.color = 0x00FF00
        onlinetxt.text = "Online :D"
    else:
        onlinetxt.color = 0xFF0000
        onlinetxt.text = "Offline :("

    playernum.text = f"{data['players']['online']}/{data['players']['max']}"

while True:
    serverstat()
    time.sleep(30)
