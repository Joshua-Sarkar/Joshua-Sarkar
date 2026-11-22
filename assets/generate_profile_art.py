from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os
import subprocess

OUT = os.environ.get("OUTPUT_DIR", "assets/generated")
os.makedirs(OUT, exist_ok=True)


def resolve_font(pattern, fallback):
    """Resolve installed font files by family/style; avoid tiny PIL bitmap fallback."""
    try:
        path = subprocess.check_output(
            ["fc-match", "-f", "%{file}", pattern],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        if path and os.path.isfile(path):
            return path
    except (OSError, subprocess.CalledProcessError):
        pass
    return fallback


SERIF = resolve_font(
    "EB Garamond:style=Bold",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
)
SANS = resolve_font(
    "DejaVu Sans:style=Book",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
)
SANS_BOLD = resolve_font(
    "DejaVu Sans:style=Bold",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
)
ITALIC = resolve_font(
    "EB Garamond:style=Italic",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
)

PURPLE = (179, 120, 255)
CYAN = (85, 220, 255)
GOLD = (245, 208, 139)
PINK = (255, 112, 190)
RED = (255, 78, 105)


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        fallback = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        return ImageFont.truetype(fallback, size)


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
    img = background(1400, 520, phase)
    glass_panel(img, (64, 24, 1336, 496), 42, GOLD, (10, 13, 38, 178), phase)
    d = ImageDraw.Draw(img)
    draw_tentacle(d, 86, 435, 1.65, phase, (164, 117, 244, 150))
    draw_crown(d, 700, 78, 1.15)

    d.rounded_rectangle((1210, 68, 1300, 140), radius=11,
                        fill=(38, 9, 28, 220), outline=(255, 93, 113, 220), width=2)
    d.text((1255, 94), "AM//", font=font(SANS_BOLD, 20),
           fill=(255, 117, 132, 255), anchor="mm")
    d.line((1228, 119, 1240, 119, 1248, 109, 1256, 128, 1264, 113, 1282, 113),
           fill=(255, 85, 110, 230), width=2)

    shimmer = (245, 208, 139) if frame % 12 < 6 else (103, 232, 249)
    draw_glow_text(img, (700, 205), "JOSHUA SARKAR", font(SERIF, 112),
                   (255, 239, 205, 255), shimmer, blur=17)
    d = ImageDraw.Draw(img)
    sweep_x = int(270 + 860 * (frame / 11))
    d.line((sweep_x, 262, min(1320, sweep_x + 95), 262),
           fill=(*shimmer, 225), width=3)

    center_text(d, (700, 314), "20  ·  B.TECH CSE  ·  AI/ML",
                font(SANS_BOLD, 29), (244, 239, 255, 255))
    center_text(d, (700, 369), "GRAPHIC ERA UNIVERSITY  ·  DEHRADUN, INDIA",
                font(SANS_BOLD, 22), (191, 224, 255, 255))
    center_text(d, (700, 430), "PRODUCTION SOFTWARE  ·  COMPUTER VISION  ·  CREATIVE WRITING",
                font(SANS_BOLD, 18), (139, 221, 248, 255))
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
    d.text((1139, 34), "AM//", font=font(SANS_BOLD, 18),
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
        center_text(d, (x+175, 214), title, font(SERIF, 35), (255, 238, 211, 255))
        center_text(d, (x+175, 258), kicker, font(SANS_BOLD, 16), (*colour, 255))
        center_text(d, (x+175, 291), sub, font(SANS, 17), (230, 225, 249, 250))
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
                   font(SERIF, 39), (255, 231, 194, 255), GOLD, blur=8)
    d = ImageDraw.Draw(img)
    center_text(d, (600, 169), "COSMIC HORROR, MACHINE MINDS & QUESTIONS THAT LINGER",
                font(SANS_BOLD, 15), (211, 222, 255, 250))
    center_text(d, (600, 207), "Strange stories. Unsettling machines. Questions that linger.",
                font(ITALIC, 20), (234, 206, 231, 255))
    return img.convert("RGB")


def render_typing(frame, total):
    w, h = 1000, 94
    phase = 2*math.pi*frame/max(1, total)
    img = background(w, h, phase, variant=3)
    glass_panel(img, (10, 8, w-10, h-8), 23, GOLD, (11, 13, 37, 194), phase)
    message = "AI/ML  ·  PRODUCTION SOFTWARE  ·  CREATIVE WRITING"
    reveal = min(len(message), max(0, frame*2))
    visible = message[:reveal]
    d = ImageDraw.Draw(img)
    f = font(SANS_BOLD, 27)
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



def render_divider(frame):
    phase = 2*math.pi*frame/12
    img = background(1200, 110, phase, variant=3)
    glass_panel(img, (8, 7, 1192, 103), 22, GOLD, (12, 13, 39, 150), phase, border=1)
    d = ImageDraw.Draw(img)
    draw_tentacle(d, 12, 98, .72, phase, (178, 120, 255, 125))
    # An understated astrolabe-like orbit in the centre.
    cx, cy = 600, 55
    for radius, colour, width in [(27, (245, 208, 139, 160), 1), (19, (103, 232, 249, 135), 1)]:
        d.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline=colour, width=width)
    angle = phase
    px = int(cx + 27*math.cos(angle))
    py = int(cy + 27*math.sin(angle))
    d.ellipse((px-3, py-3, px+3, py+3), fill=(255, 225, 170, 245))
    d.line((95, 55, 490, 55), fill=(179, 120, 255, 145), width=1)
    d.line((710, 55, 1105, 55), fill=(85, 220, 255, 145), width=1)
    d.rounded_rectangle((1130, 27, 1170, 76), radius=8,
                        fill=(35, 8, 30, 165), outline=(255, 91, 112, 145), width=1)
    d.text((1150, 51), "AM", font=font(SANS_BOLD, 11), fill=(255, 117, 132, 235), anchor="mm")
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




REPOSITORIES = [
    {
        "slug": "sentinel-cam-enterprise", "title": "SENTINEL-CAM",
        "subtitle": "AI CCTV  ·  OBJECT DETECTION  ·  FACE RECOGNITION  ·  SECURITY EVENTS",
        "steps": ["CAMERA FEED", "OPENCV", "YOLO TASK", "EVENT LOG", "ALERT"],
        "accent": (255, 86, 112), "secondary": (70, 205, 255),
        "note": "Django + OpenCV + Ultralytics",
    },
    {
        "slug": "ams-v1", "title": "AMS-V1  /  WORKFORCE LEDGER",
        "subtitle": "LIVE WORKFORCE OPERATIONS  ·  ATTENDANCE  ·  LEAVE  ·  PAYROLL",
        "steps": ["AUTH + ROLES", "WORKFORCE", "ATTENDANCE", "LEAVE LEDGER", "PAYROLL"],
        "accent": (197, 151, 87), "secondary": (233, 210, 170),
        "note": "Laravel 12  ·  MySQL  ·  Blade",
    },
    {
        "slug": "plantdoc", "title": "PLANTDOC",
        "subtitle": "PLANT DISEASE ANALYSIS  ·  38 CLASSES  ·  GRAD-CAM  ·  IOT CONTEXT",
        "steps": ["LEAF IMAGE", "TFLITE", "38 CLASSES", "GRAD-CAM", "IOT CONTEXT"],
        "accent": (94, 212, 133), "secondary": (72, 216, 211),
        "note": "TensorFlow Lite  ·  FastAPI  ·  React",
    },
    {
        "slug": "pharmalock", "title": "PHARMALOCK",
        "subtitle": "PHARMACY INVENTORY  ·  TRANSACTIONS  ·  LOCKING  ·  RECOVERY",
        "steps": ["REQUEST", "LOCK MANAGER", "WAL", "BUFFER POOL", "COMMIT / UNDO"],
        "accent": (57, 212, 160), "secondary": (246, 183, 91),
        "note": "Operating Systems meet Database Systems",
    },
    {
        "slug": "wacrm-fusion", "title": "WACRM-FUSION",
        "subtitle": "WHATSAPP CRM  ·  SHARED INBOX  ·  AUTOMATIONS  ·  SALES PIPELINES",
        "steps": ["WHATSAPP", "WEBHOOK", "INBOX / FLOWS", "AUTOMATIONS", "TEAM CRM"],
        "accent": (44, 211, 146), "secondary": (82, 222, 211),
        "note": "Next.js 16  ·  PostgreSQL  ·  Prisma",
    },
    {
        "slug": "scout-lead-intelligence", "title": "SCOUT  /  LEAD INTELLIGENCE",
        "subtitle": "LOCAL DISCOVERY  ·  QUALIFICATION  ·  WEBSITE RESEARCH  ·  OUTREACH",
        "steps": ["OSM SEARCH", "BOUNDARY FILTER", "CLASSIFY", "RESEARCH", "DRAFT + SYNC"],
        "accent": (249, 151, 77), "secondary": (125, 215, 129),
        "note": "Client-aware research pipeline",
    },
    {
        "slug": "ehr-deidentification-blockchain", "title": "MEDICAL DATA  /  PROVENANCE",
        "subtitle": "TEXT DE-IDENTIFICATION  ·  HASH FINGERPRINTS  ·  BLOCKCHAIN AUDIT",
        "steps": ["MEDICAL TEXT", "SPACY NER", "REDACT", "SHA-256", "GANACHE LOG"],
        "accent": (88, 176, 255), "secondary": (173, 130, 255),
        "note": "Flask  ·  spaCy  ·  Web3.py",
    },
    {
        "slug": "blood-circulation-simulation", "title": "VASCULAR FLOW SIMULATOR",
        "subtitle": "GRAPH NETWORK  ·  BLOOD-CELL QUEUES  ·  TEMPORARY BLOCKAGES",
        "steps": ["VESSEL GRAPH", "CELL QUEUE", "SIM TICK", "BLOCKAGE", "STATE API"],
        "accent": (255, 94, 115), "secondary": (72, 210, 240),
        "note": "C  ·  libmicrohttpd  ·  JavaScript",
    },
    {
        "slug": "aerodaa-airline-pricing", "title": "AERODAA  /  AIRLINE PRICING",
        "subtitle": "FLIGHT SEARCH  ·  GREEDY FARES  ·  QUICK SORT  ·  BOOKINGS",
        "steps": ["ROUTE SEARCH", "GREEDY FARE", "DP CACHE", "QUICK SORT", "BOOKING"],
        "accent": (246, 190, 85), "secondary": (91, 174, 255),
        "note": "C++  ·  CSV persistence  ·  Web visualiser",
    },
    {
        "slug": "ams-golden-frozen-master", "title": "AMS  /  GOLDEN FROZEN MASTER",
        "subtitle": "PRESERVED RELEASE BASELINE  ·  WORKFORCE LEDGER",
        "steps": ["FROZEN BASE", "AUTH + ROLES", "ATTENDANCE", "LEAVE LEDGER", "PAYROLL"],
        "accent": (226, 177, 91), "secondary": (236, 216, 174),
        "note": "Private release snapshot",
    },
    {
        "slug": "future-corridor-ams", "title": "FUTURE CORRIDOR  /  AMS",
        "subtitle": "CLIENT EDITION  ·  LIQUID GLASS  ·  ROYAL LAVENDER DESIGN SYSTEM",
        "steps": ["CLIENT SHELL", "WORKFORCE", "ATTENDANCE", "GOVERNANCE", "OPERATIONS"],
        "accent": (115, 119, 255), "secondary": (90, 199, 255),
        "note": "Private client deployment variant",
    },
    {
        "slug": "dwheelz-ams", "title": "DWHEELZ  /  AMS",
        "subtitle": "CLIENT-BRANDED WORKFORCE MANAGEMENT DEPLOYMENT",
        "steps": ["CLIENT BRAND", "AUTH + ROLES", "WORKFORCE", "ATTENDANCE", "LEAVE + PAYROLL"],
        "accent": (244, 143, 75), "secondary": (87, 204, 221),
        "note": "Private client deployment variant",
    },
]


def fit_font(text, path, max_width, size, minimum=22):
    """Shrink a heading just enough to fit; always use a scalable font."""
    draw = ImageDraw.Draw(Image.new("RGB", (2, 2)))
    while size > minimum:
        f = font(path, size)
        if draw.textbbox((0, 0), text, font=f)[2] <= max_width:
            return f
        size -= 2
    return font(path, minimum)


def render_repo_hero(config, frame, index):
    phase = 2 * math.pi * frame / 10
    img = background(1400, 360, phase, variant=index % 4)
    accent = config["accent"]
    secondary = config["secondary"]
    glass_panel(img, (36, 24, 1364, 336), 34, accent, (9, 13, 37, 186), phase)
    d = ImageDraw.Draw(img)

    # Project-specific orbital marks, nodes and circuit traces.
    for ring in (28, 44, 62):
        x = 92 + ring // 4 * math.sin(phase)
        d.ellipse((x-ring, 180-ring, x+ring, 180+ring),
                  outline=(*secondary, 80 + ring), width=1)
    for i in range(7):
        x = 190 + i * 168
        y = 70 + int(10 * math.sin(phase + i * .7))
        d.line((x, y, x+54, y), fill=(*accent, 100), width=2)
        d.ellipse((x+51, y-3, x+57, y+3), fill=(*secondary, 200))

    title_size = 68 if len(config["title"]) < 22 else 56
    draw_glow_text(
        img, (700, 148), config["title"],
        fit_font(config["title"], SANS_BOLD, 1180, title_size),
        (246, 243, 255, 255), accent, blur=14,
    )
    d = ImageDraw.Draw(img)
    center_text(d, (700, 220), config["subtitle"],
                fit_font(config["subtitle"], SANS_BOLD, 1180, 22, 15),
                (198, 221, 255, 255))
    center_text(d, (700, 278), config["note"],
                fit_font(config["note"], ITALIC, 1180, 24, 17),
                (255, 221, 187, 255))

    # A moving highlight runs around the frosted panel.
    sweep = int(60 + 1280 * frame / 9)
    d.line((sweep, 30, min(1340, sweep+85), 30),
           fill=(*secondary, 230), width=3)
    d.rounded_rectangle((1262, 50, 1322, 92), radius=9,
                        fill=(28, 10, 32, 190), outline=(*accent, 190), width=2)
    d.text((1292, 71), "BUILD", font=font(SANS_BOLD, 13),
           fill=(255, 240, 220, 245), anchor="mm")
    return img.convert("RGB")


def render_repo_flow(config, frame, index):
    phase = 2 * math.pi * frame / 10
    img = background(1400, 245, phase, variant=(index+2) % 4)
    accent = config["accent"]
    secondary = config["secondary"]
    glass_panel(img, (22, 14, 1378, 231), 28, secondary, (9, 13, 37, 178), phase, border=1)
    d = ImageDraw.Draw(img)
    center_text(d, (700, 48), "HOW THE SYSTEM MOVES",
                font(SANS_BOLD, 22), (235, 233, 255, 250))
    labels = config["steps"]
    left, gap, width = 46, 24, 236
    active = frame % len(labels)
    for i, label in enumerate(labels):
        x = left + i * (width + gap)
        y = 94
        chosen = i == active
        border = accent if chosen else secondary
        fill = (35, 24, 66, 225) if chosen else (12, 23, 48, 220)
        d.rounded_rectangle((x, y, x+width, y+91), radius=17,
                            fill=fill, outline=(*border, 235 if chosen else 120),
                            width=3 if chosen else 1)
        if chosen:
            glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
            gd = ImageDraw.Draw(glow)
            gd.rounded_rectangle((x-2, y-2, x+width+2, y+93), radius=18,
                                 outline=(*accent, 190), width=4)
            img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10)))
            d = ImageDraw.Draw(img)
        center_text(d, (x+width//2, y+43), label,
                    fit_font(label, SANS_BOLD, width-24, 19, 13),
                    (255, 246, 225, 255) if chosen else (198, 221, 255, 235))
        if i < len(labels)-1:
            x1 = x+width+4
            d.line((x1, y+45, x1+gap-7, y+45), fill=(*secondary, 220), width=2)
            d.polygon([(x1+gap-7, y+39), (x1+gap-1, y+45), (x1+gap-7, y+51)],
                      fill=(*secondary, 220))
    return img.convert("RGB")


def save_to_path(frames, path, duration=190):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    palette_frames = [
        im.convert("P", palette=Image.Palette.ADAPTIVE, colors=192)
        for im in frames
    ]
    palette_frames[0].save(
        path, save_all=True, append_images=palette_frames[1:],
        duration=duration, loop=0, optimize=True, disposal=2,
    )
    print(f"created {path} ({os.path.getsize(path)} bytes)")


def generate_repository_art():
    for index, config in enumerate(REPOSITORIES):
        folder = os.path.join(OUT, "repositories", config["slug"])
        save_to_path(
            [render_repo_hero(config, frame, index) for frame in range(10)],
            os.path.join(folder, "hero.gif"), 190,
        )
        save_to_path(
            [render_repo_flow(config, frame, index) for frame in range(10)],
            os.path.join(folder, "flow.gif"), 210,
        )



save_loop([render_hero(i) for i in range(12)], "hero.gif", 230)
save_loop([render_projects(i) for i in range(12)], "projects-glass.gif", 230)
save_loop([render_lore(i) for i in range(12)], "lovecraft-am.gif", 230)
save_loop([render_typing(i, 32) for i in range(32)], "tagline.gif", 130)
save_loop([render_divider(i) for i in range(12)], "divider.gif", 230)
generate_repository_art()
