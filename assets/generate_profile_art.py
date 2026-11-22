from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os

OUT = os.environ.get("OUTPUT_DIR", "assets/generated")
os.makedirs(OUT, exist_ok=True)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
ITALIC = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"

PURPLE = (179, 120, 255)
CYAN = (85, 220, 255)
GOLD = (245, 208, 139)
PINK = (255, 112, 190)
RED = (255, 78, 105)


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def center_text(draw, xy, text, fnt, fill, anchor="mm"):
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def draw_glow_text(img, xy, text, fnt, fill, glow, anchor="mm", blur=9):
    glow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)
    gd.text(xy, text, font=fnt, fill=(*glow, 190), anchor=anchor,
            stroke_width=2, stroke_fill=(*glow, 110))
    img.alpha_composite(glow_layer.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(img).text(xy, text, font=fnt, fill=fill, anchor=anchor,
                             stroke_width=1, stroke_fill=(17, 12, 37, 180))


def background(w, h, phase=0.0, variant=0):
    img = Image.new("RGBA", (w, h), (9, 9, 28, 255))
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    pools = [
        (int(w * (.18 + .05 * math.sin(phase))), int(h * .25), int(h * .9), (107, 45, 193, 115)),
        (int(w * (.78 + .04 * math.cos(phase * .8))), int(h * .7), int(h * .95), (0, 133, 182, 105)),
        (int(w * (.52 + .035 * math.sin(phase * 1.3))), int(h * .35), int(h * .55), (178, 55, 139, 65)),
    ]
    for x, y, r, colour in pools:
        gd.ellipse((x-r, y-r, x+r, y+r), fill=colour)
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(max(20, h // 5))))

    lines = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lines)
    colours = [(*PURPLE, 105), (*CYAN, 100), (*GOLD, 92), (*PINK, 90)]
    for j in range(22):
        pts = []
        base = h * (.12 + j * .037)
        for x in range(-10, w + 20, 12):
            y = base + 16 * math.sin(x / 105 + phase * 1.1 + j * .31) + 8 * math.cos(x / 62 - phase * .8 + j * .22)
            pts.append((x, int(y)))
        ld.line(pts, fill=colours[(j + variant) % len(colours)], width=1)
    for j in range(8):
        pts = []
        base = h * (.35 + j * .055)
        for x in range(-10, w + 20, 16):
            y = base + 24 * math.sin(x / 170 - phase * .7 + j * .48)
            pts.append((x, int(y)))
        ld.line(pts, fill=(126, 112, 255, 48), width=1)
    img.alpha_composite(lines.filter(ImageFilter.GaussianBlur(.35)))

    d = ImageDraw.Draw(img)
    for i in range(42):
        x = (i * 173 + 39) % w
        y = (i * 79 + 23) % h
        pulse = .55 + .45 * math.sin(phase * 1.7 + i * 1.91)
        r = 1 if i % 4 else 2
        a = int(75 + 150 * pulse)
        colour = (245, 220, 173, a) if i % 3 else (132, 222, 255, a)
        d.ellipse((x-r, y-r, x+r, y+r), fill=colour)
    return img


def glass_panel(img, box, radius=28, accent=(245, 208, 139), fill=(12, 16, 43, 155), phase=0.0, border=2):
    x1, y1, x2, y2 = box
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rounded_rectangle((x1-3, y1-3, x2+3, y2+3), radius=radius+4,
                         outline=(*accent, 170), width=5)
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(13)))
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle(box, radius=radius, fill=fill,
                         outline=(226, 235, 255, 120), width=border)
    od.rounded_rectangle((x1+5, y1+5, x2-5, y2-5), radius=max(8, radius-6),
                         outline=(255, 255, 255, 34), width=1)
    shine_x = int(x1 + 20 + (x2-x1-40) * (.5 + .5 * math.sin(phase * 1.2)))
    od.line((shine_x, y1+9, shine_x+75, y1+9), fill=(*accent, 190), width=3)
    od.line((x1+24, y1+12, x2-24, y1+12), fill=(255, 255, 255, 35), width=1)
    img.alpha_composite(overlay)


def draw_crown(draw, cx, cy, scale=1.0, colour=(245, 208, 139, 245)):
    pts = [
        (cx-26*scale, cy+12*scale), (cx-22*scale, cy-8*scale),
        (cx-9*scale, cy+1*scale), (cx, cy-16*scale),
        (cx+10*scale, cy+1*scale), (cx+23*scale, cy-8*scale),
        (cx+27*scale, cy+12*scale), (cx-26*scale, cy+12*scale),
    ]
    draw.line(pts, fill=colour, width=max(1, int(2*scale)), joint="curve")
    draw.line((cx-24*scale, cy+17*scale, cx+25*scale, cy+17*scale),
              fill=colour, width=max(1, int(2*scale)))
    for x, y in [pts[1], pts[3], pts[5]]:
        r = 2*scale
        draw.ellipse((x-r, y-r, x+r, y+r), fill=colour)


def draw_tentacle(draw, x0, y0, scale=1.0, phase=0.0, colour=(178, 120, 255, 170)):
    for k in range(3):
        pts = []
        for n in range(26):
            t = n / 25
            x = x0 + scale * (70*t + 10*math.sin(t*8 + phase + k*.6))
            y = y0 + scale * (-42*t + 34*math.sin(t*5 + phase + k*.6))
            pts.append((int(x), int(y)))
        draw.line(pts, fill=colour, width=max(2, int(3*scale)))
        ex, ey = pts[-1]
        for q in range(4):
            r = 1.5*scale
            draw.ellipse((ex-q*4*r-r, ey-q*2*r-r, ex-q*4*r+r, ey-q*2*r+r),
                         fill=(245, 208, 139, 125))


def render_hero(frame):
    phase = 2*math.pi*frame/12
    img = background(1200, 430, phase)
    glass_panel(img, (70, 42, 1130, 388), 38, GOLD, (10, 13, 38, 166), phase)
    d = ImageDraw.Draw(img)
    draw_tentacle(d, 92, 310, 1.45, phase, (164, 117, 244, 130))
    draw_crown(d, 600, 104, .95)
    d.rounded_rectangle((1010, 84, 1086, 143), radius=9,
                        fill=(38, 9, 28, 200), outline=(255, 93, 113, 190), width=2)
    d.text((1048, 103), "AM//", font=font(SANS_BOLD, 16),
           fill=(255, 117, 132, 245), anchor="mm")
    d.line((1024, 124, 1034, 124, 1040, 117, 1048, 131, 1055, 121, 1073, 121),
           fill=(255, 85, 110, 210), width=2)
    draw_glow_text(img, (600, 197), "JOSHUA SARKAR", font(SERIF, 68),
                   (255, 236, 198, 255), GOLD, blur=11)
    d = ImageDraw.Draw(img)
    center_text(d, (600, 253), "B.TECH STUDENT  ·  3RD YEAR",
                font(SANS_BOLD, 22), (230, 222, 255, 255))
    center_text(d, (600, 308), "Curious. Thoughtful. Interested in building things.",
                font(ITALIC, 24), (255, 225, 205, 255))
    center_text(d, (600, 349), "AI  ·  COMPUTER VISION  ·  SOFTWARE  ·  SYSTEMS",
                font(SANS_BOLD, 14), (139, 221, 248, 245))
    return img.convert("RGB")


def project_icon(draw, cx, cy, kind, colour):
    if kind == "shield":
        pts = [
            (cx, cy-24), (cx+22, cy-15), (cx+18, cy+10),
            (cx, cy+27), (cx-18, cy+10), (cx-22, cy-15), (cx, cy-24),
        ]
        draw.line(pts, fill=(*colour, 245), width=3, joint="curve")
        draw.line((cx-9, cy, cx-2, cy+8, cx+12, cy-9), fill=(*colour, 240), width=3)
    elif kind == "people":
        for x, y, r in [(cx-14, cy-11, 7), (cx+14, cy-11, 7), (cx, cy-17, 8)]:
            draw.ellipse((x-r, y-r, x+r, y+r), outline=(*colour, 245), width=2)
        draw.arc((cx-34, cy-3, cx+34, cy+34), 180, 360, fill=(*colour, 245), width=3)
        draw.arc((cx-24, cy-6, cx+24, cy+34), 180, 360, fill=(*colour, 245), width=3)
    else:
        draw.line((cx-2, cy+24, cx+4, cy-19), fill=(*colour, 245), width=3)
        draw.arc((cx-26, cy-24, cx+4, cy+5), 180, 300, fill=(*colour, 245), width=3)
        draw.arc((cx+2, cy-11, cx+30, cy+18), 210, 340, fill=(*colour, 245), width=3)
        draw.arc((cx-15, cy-2, cx+21, cy+27), 205, 335, fill=(*colour, 245), width=3)


def render_projects(frame):
    phase = 2*math.pi*frame/12
    img = background(1200, 390, phase, variant=1)
    d = ImageDraw.Draw(img)
    draw_tentacle(d, 4, 368, .95, phase, (164, 117, 244, 105))
    d.rounded_rectangle((1102, 12, 1176, 58), radius=8, fill=(35, 8, 30, 170),
                        outline=(255, 91, 112, 160), width=2)
    d.text((1139, 34), "AM//", font=font(SANS_BOLD, 15),
           fill=(255, 117, 132, 235), anchor="mm")
    center_text(d, (600, 37), "A FEW THINGS I BUILD",
                font(SERIF, 31), (255, 230, 187, 250))
    cards = [
        ("SENTINEL-CAM", "AI CCTV  ·  YOLOv8", "Face recognition & alerts", "shield", CYAN),
        ("AMS-V1", "ATTENDANCE  ·  WORKFORCE", "Employees, leave & roles", "people", PURPLE),
        ("PLANTDOC", "PLANT HEALTH  ·  AI + IoT", "38 diseases & Grad-CAM", "leaf", GOLD),
    ]
    xs = [45, 425, 805]
    for idx, (title, kicker, sub, icon, colour) in enumerate(cards):
        x = xs[idx]
        glass_panel(img, (x, 82, x+350, 344), 30, colour, (13, 15, 43, 178), phase+idx*.7)
        d = ImageDraw.Draw(img)
        project_icon(d, x+175, 146, icon, colour)
        center_text(d, (x+175, 214), title, font(SERIF, 29), (255, 238, 211, 255))
        center_text(d, (x+175, 258), kicker, font(SANS_BOLD, 14), (*colour, 255))
        center_text(d, (x+175, 291), sub, font(SANS, 14), (230, 225, 249, 250))
        gx = int(x + 20 + 310*(.5 + .5*math.sin(phase+idx)))
        d.line((gx, 335, gx+45, 335), fill=(*colour, 235), width=3)
    return img.convert("RGB")


def render_lore(frame):
    phase = 2*math.pi*frame/12
    img = background(1200, 285, phase, variant=2)
    glass_panel(img, (190, 42, 1010, 244), 31, GOLD, (12, 12, 39, 177), phase)
    d = ImageDraw.Draw(img)
    draw_tentacle(d, 26, 220, 1.3, phase, (178, 117, 255, 210))
    d.rounded_rectangle((1036, 53, 1169, 215), radius=16,
                        fill=(21, 8, 25, 220), outline=(255, 91, 112, 210), width=3)
    d.rounded_rectangle((1048, 65, 1157, 169), radius=10,
                        fill=(56, 9, 30, 220), outline=(255, 130, 140, 125), width=1)
    d.text((1102, 91), "AM//", font=font(SANS_BOLD, 26),
           fill=(255, 102, 119, 255), anchor="mm")
    wave = []
    for x in range(1057, 1149, 4):
        y = 131 + 8*math.sin(x/10 + phase*2) + 4*math.cos(x/6-phase)
        wave.append((x, int(y)))
    d.line(wave, fill=(255, 93, 120, 235), width=2)
    d.text((1102, 188), "SIGNAL", font=font(SANS_BOLD, 10),
           fill=(249, 173, 182, 220), anchor="mm")
    draw_glow_text(img, (600, 111), "A LITTLE LOVECRAFT. A LITTLE AM.",
                   font(SERIF, 36), (255, 231, 194, 255), GOLD, blur=8)
    d = ImageDraw.Draw(img)
    center_text(d, (600, 169), "COSMIC HORROR, MACHINE MINDS & QUESTIONS THAT LINGER",
                font(SANS_BOLD, 15), (211, 222, 255, 250))
    center_text(d, (600, 207), "Strange stories. Unsettling machines. Questions that linger.",
                font(ITALIC, 17), (234, 206, 231, 255))
    return img.convert("RGB")


def render_typing(frame, total):
    w, h = 1000, 94
    phase = 2*math.pi*frame/max(1, total)
    img = background(w, h, phase, variant=3)
    glass_panel(img, (10, 8, w-10, h-8), 23, GOLD, (11, 13, 37, 194), phase)
    message = "Curious. Thoughtful. Interested in building things."
    reveal = min(len(message), max(0, frame*2))
    visible = message[:reveal]
    d = ImageDraw.Draw(img)
    f = font(ITALIC, 29)
    x, y = 45, 48
    d.text((x, y), visible, font=f, fill=(255, 233, 204, 255), anchor="lm")
    bbox = d.textbbox((x, y), visible, font=f, anchor="lm")
    cursor_x = bbox[2] + 5
    if frame % 4 < 2:
        d.rounded_rectangle((cursor_x, y-17, cursor_x+3, y+17),
                            radius=2, fill=(103, 232, 249, 255))
    a = int(130 + 100*(.5 + .5*math.sin(phase*2)))
    d.ellipse((w-63, 32, w-53, 42), fill=(245, 208, 139, a))
    return img.convert("RGB")


def save_loop(frames, name, duration=220):
    path = os.path.join(OUT, name)
    palette_frames = [
        im.convert("P", palette=Image.Palette.ADAPTIVE, colors=192)
        for im in frames
    ]
    palette_frames[0].save(
        path, save_all=True, append_images=palette_frames[1:],
        duration=duration, loop=0, optimize=True, disposal=2,
    )
    print(f"created {path} ({os.path.getsize(path)} bytes)")


save_loop([render_hero(i) for i in range(12)], "hero.gif", 230)
save_loop([render_projects(i) for i in range(12)], "projects-glass.gif", 230)
save_loop([render_lore(i) for i in range(12)], "lovecraft-am.gif", 230)
save_loop([render_typing(i, 32) for i in range(32)], "tagline.gif", 130)
