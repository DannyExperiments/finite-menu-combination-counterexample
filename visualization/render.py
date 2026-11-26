#!/usr/bin/env python3
"""Render the expectation plane E = c − p and selected exact cross-pairs."""
from math import cos, pi, sin, tau
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 664, 434
COLORS = ["#0d1723", "#162638", "#31495e", "#f0f6fa", "#b4c8d9", "#83e2ce", "#ffc179", "#789aae"]


def font(size, bold=False):
    names = ("Arial Bold.ttf", "DejaVuSans-Bold.ttf") if bold else ("Arial.ttf", "DejaVuSans.ttf")
    for name in names:
        for base in (Path("/System/Library/Fonts/Supplemental"), Path("/usr/share/fonts/truetype/dejavu")):
            path = base / name
            if path.is_file():
                return ImageFont.truetype(str(path), size)
    raise RuntimeError("Arial or DejaVu Sans is required")


FONTS = [font(32, True), font(19), font(22, True), font(18), font(19, True)]


def project(c, p, angle):
    x, y, z = (c-.5)*1.3, .76*(c-p), (p-.5)*1.3
    x, z = x*cos(angle)+z*sin(angle), -x*sin(angle)+z*cos(angle)
    y, z = y*cos(.44)-z*sin(.44), y*sin(.44)+z*cos(.44)
    scale = 89*5/(5-z)
    return 186+x*scale, 212-y*scale


def frame(angle, n):
    image = Image.new("RGB", (W,H), COLORS[0])
    d = ImageDraw.Draw(image)
    d.text((24, 18), "The conflicting gamble moves", font=FONTS[0], fill=COLORS[3])
    d.text((24, 59), "Two outcomes  ·  Exact expectation crossing", font=FONTS[1], fill=COLORS[4])
    d.rounded_rectangle((24, 102, 353, 353), radius=18, fill=COLORS[1], outline=COLORS[2])
    d.rounded_rectangle((365, 102, 640, 353), radius=18, fill=COLORS[1], outline=COLORS[2])
    for i in range(5):
        r = i/4
        for a,b in (((0,r),(1,r)),((r,0),(r,1))):
            d.line((*project(*a,angle),*project(*b,angle)),fill=COLORS[2],width=2)
    d.line((*project(0,0,angle),*project(1,1,angle)),fill=COLORS[7],width=2)
    c = 1/(2*n)
    a,b = project(c,0,angle),project(c,1/n,angle)
    d.line((*a,*b),fill=COLORS[3],width=3)
    for i,(x,y) in enumerate((a,b)):
        color = COLORS[5 if i == 0 else 6]
        d.ellipse((x-6,y-6,x+6,y+6),fill=color,outline=COLORS[0],width=1)
    d.text((39, 329), "Expectation plane  E = c − p", font=FONTS[3], fill=COLORS[4])
    d.text((385, 121), f"Cone pair at n = {n}", font=FONTS[2], fill=COLORS[3])
    d.text((385, 167), f"E at p = 1/2:  +1/{8*n}", font=FONTS[2], fill=COLORS[5])
    d.text((385, 205), f"E at p = p(n):  −1/{8*n}", font=FONTS[2], fill=COLORS[6])
    d.text((385, 257), "L accepts the moving gamble.", font=FONTS[3], fill=COLORS[3])
    d.text((385, 288), "D(n) accepts its negative.", font=FONTS[3], fill=COLORS[3])
    chosen = "D(n) hits the fixed menu." if n < 8 else "D(n) misses the fixed menu."
    d.text((24, 371), chosen, font=FONTS[4], fill=COLORS[3])
    d.text((24, 401), "The fixed menu misses L and misses every D(n) from n = 8.", font=FONTS[3], fill=COLORS[4])
    return image


def main():
    palette = Image.new("P", (1, 1))
    palette.putpalette([int(c[i:i+2],16) for c in COLORS for i in (1,3,5)] + [0,0,0]*(256-len(COLORS)))
    frames = [frame(tau*i/48+pi/6,(1,2,4,8)[i//12]).quantize(palette=palette,dither=Image.Dither.NONE) for i in range(48)]
    frames[0].save(Path(__file__).with_name("expectation-crossing.gif"),save_all=True,append_images=frames[1:],
                   loop=0,duration=135,optimize=True,disposal=1)


if __name__ == "__main__":
    main()
