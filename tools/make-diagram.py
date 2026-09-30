#!/usr/bin/env python3
"""Zeichnet das Architekturbild des Berichts (docs/zwischenbericht-2026-09/assets/architektur.png)."""
import pathlib

from PIL import Image, ImageDraw, ImageFont

OUT = pathlib.Path(__file__).resolve().parents[1] / "docs/zwischenbericht-2026-09/assets/architektur.png"
FONTS = "/usr/share/fonts/truetype/liberation/"
BOLD = ImageFont.truetype(FONTS + "LiberationSans-Bold.ttf", 44)
REG = ImageFont.truetype(FONTS + "LiberationSans-Regular.ttf", 34)
SMALL = ImageFont.truetype(FONTS + "LiberationSans-Italic.ttf", 32)

NAVY, BLUE, GREEN, OLIVE = (39, 80, 110), (52, 103, 140), (92, 126, 76), (110, 140, 44)
INK, MUTED, LINE = (27, 44, 57), (90, 107, 118), (201, 215, 226)
W, H = 2700, 1780
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

X0, BW, BH, GAP = 170, 1120, 150, 70
layers = [
    ("Mitarbeitende im Browser", "Anmeldung mit persönlichem Konto", (238, 243, 248), NAVY, INK),
    ("Nginx", "Einziger öffentlicher Zugang · Verschlüsselung (HTTPS)", NAVY, None, "white"),
    ("Open WebUI", "Konten, Rechte, Modellprofile, Wissenssammlungen", BLUE, None, "white"),
    ("Auth-Proxy", "Prüft Zugangsschlüssel · gibt nur freigegebene Modelle weiter", GREEN, None, "white"),
    ("Ollama", "Betreibt die Sprachmodelle und das Embedding-Modell", OLIVE, None, "white"),
    ("GPU-Server Hetzner GEX44", "NVIDIA RTX 4000 SFF Ada, 20 GB Grafikspeicher", (238, 243, 248), NAVY, INK),
]
ys = []
y = 60
for title, sub, fill, outline, color in layers:
    d.rounded_rectangle([X0, y, X0 + BW, y + BH], radius=28, fill=fill,
                        outline=outline or fill, width=4)
    d.text((X0 + 50, y + 26), title, font=BOLD, fill=color)
    d.text((X0 + 50, y + 90), sub, font=REG, fill=color if color != INK else MUTED)
    ys.append(y)
    y += BH + GAP + (60 if len(ys) == 1 else 0)


def arrow(x1, y1, x2, y2, color=MUTED, width=6):
    d.line([x1, y1, x2, y2], fill=color, width=width)
    if y2 > y1:
        d.polygon([(x2 - 18, y2 - 26), (x2 + 18, y2 - 26), (x2, y2)], fill=color)
    else:
        d.polygon([(x2, y2 - 18), (x2, y2 + 18), (x2 - 28, y2)], fill=color)


cx = X0 + BW // 2
for i in range(len(ys) - 1):
    arrow(cx, ys[i] + BH, cx, ys[i + 1])

# Beschriftung des öffentlichen Übergangs
d.text((cx + 30, ys[0] + BH + 14), "HTTPS über das Internet", font=SMALL, fill=MUTED)

# Rahmen: eigene, vertraglich abgesicherte Infrastruktur
fy0, fy1 = ys[1] - 30, ys[-1] + BH + 30
d.rounded_rectangle([X0 - 50, fy0, X0 + BW + 50, fy1], radius=36, outline=GREEN, width=5)
d.text((X0 - 40, fy1 + 14), "Eigene, per Auftragsverarbeitungsvertrag abgesicherte Infrastruktur – "
       "Daten verlassen sie nicht", font=SMALL, fill=GREEN)

# Fachanwendungen rechts: zwei Zugangswege
AX0, AW, AH = X0 + BW + 440, 720, BH + 20


def app_box(y, title, sub, target_y, label, color):
    d.rounded_rectangle([AX0, y, AX0 + AW, y + AH], radius=28, fill=(245, 248, 240),
                        outline=color, width=4)
    d.text((AX0 + 40, y + 26), title, font=BOLD, fill=INK)
    d.text((AX0 + 40, y + 90), sub, font=REG, fill=MUTED)
    arrow(AX0, y + AH // 2, X0 + BW + 55, target_y, color=color)
    d.text((X0 + BW + 80, y + AH // 2 - 50), label, font=SMALL, fill=color)


# mit Wissen: über HTTPS zu Nginx und weiter an Open WebUI (Dienstkonto + API-Schlüssel)
app_box(ys[1] - 10, "Anwendungen mit Wissen", "eigenes Dienstkonto in Open WebUI",
        ys[1] - 10 + AH // 2, "HTTPS + API-Schlüssel", BLUE)
# ohne Wissen: über VPN direkt zum Auth-Proxy
app_box(ys[3] - 10, "Anwendungen ohne Wissen", "direkter Zugriff auf das Modell",
        ys[3] - 10 + AH // 2, "VPN + Schlüssel", OLIVE)

img = img.crop((0, 0, AX0 + AW + 70, fy1 + 80))
dpi = round(img.size[0] / 6.5)  # Breite in Word: rund 16,5 cm
img.save(OUT, dpi=(dpi, dpi))
print(f"erstellt: {OUT} ({img.size[0]}×{img.size[1]})")
