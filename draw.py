from __future__ import division

# dicongwo chomut

import gizeh
import random
from math import *
from imgurpython import ImgurClient
import os

with open("draw_corpus", "w") as f:
    f.write(str(os.getpid()))

IMAGE_SIZE = 400
IMAGE_BORDER = 100
CURVE_CHANCE = 2

client_id = '05c4e4c8869eb82'
client_secret =  '711339dbcc785ad5d2da165e9bf6b22f0f4b8136'
imgurclient = ImgurClient(client_id, client_secret)

with open("target", "r") as f:
    query = f.read()
os.remove(os.getcwd()+"/target")

surface = gizeh.Surface(width=IMAGE_SIZE+IMAGE_BORDER*2, height=IMAGE_SIZE+IMAGE_BORDER*2, bg_color=(1, 1, 1))

g = gizeh.Group([])
line = []
size = random.randint(10, 25)
for i in range(2, size):
    x = random.randint(1, int(sqrt(i-1)))*IMAGE_SIZE/int(sqrt(i)+1)
    y = random.randint(1, int(sqrt(i-1)))*IMAGE_SIZE/int(sqrt(i)+1)

    # If now is the time for an arc
    if random.randint(1, CURVE_CHANCE) == 2 and i>2 and not (old_x == x and old_y == y):
        # Finish the previous linegroup
        prevline = gizeh.polyline(line, stroke_width=5)
        line = []

        vx, vy = x-old_x, y-old_y
        distance = hypot(vx, vy)
        radius = distance*(random.random()/2 + 0.5)
        mid_x, mid_y = old_x+vx/2, old_y+vy/2
        sgn = random.choice([1, -1])
        # 90 degrees rotated, direction random
        hvx, hvy = -vy*sgn, vx*sgn
        hlength = sqrt(radius**2 - (distance/2)**2)
        f = hlength/distance
        center_x, center_y = mid_x+f*hvx, mid_y+f*hvy

        arc = gizeh.arc(radius, atan2(old_y-center_y, old_x-center_x), atan2(y-center_y, x-center_x), xy=[center_x+IMAGE_BORDER, center_y+IMAGE_BORDER], stroke_width=5)
        g = gizeh.Group([g, prevline, arc])
        
    line.append([x+IMAGE_BORDER, y+IMAGE_BORDER])
    old_x, old_y = x, y

p = gizeh.polyline(line, stroke_width=5)
g = gizeh.Group([g, p])

g.draw(surface)

surface.write_to_png("sigil.png")

upload = imgurclient.upload_from_path(os.getcwd()+"/sigil.png")
os.remove(os.getcwd()+"/sigil.png")

with open("sigil", "w") as f:
    f.write(upload['link'])
