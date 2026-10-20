#!/usr/bin/env python3
"""Generate the self-contained, accessible SVG mastheads for Lucas Sousa.

Typography is outlined from the bundled OFL Space Grotesk variable font.
Artwork is a precisely defined 3D trefoil ribbon projected into two dimensions.
No remote resources, raster assets, JavaScript, or generated imagery are used.
Run: python scripts/generate_hero.py
Requires fontTools. Output is deterministic.
"""

from __future__ import annotations

import html
import math
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONT_PATH = ASSETS / "fonts" / "SpaceGrotesk.ttf"
PALETTE = ("#7B24FF", "#BF18FF", "#F421A6", "#FF733D", "#FFBE24")
TAU = 2 * math.pi
FONT_CACHE = {}


def number(value: float) -> str:
    return f"{value:.2f}".rstrip("0").rstrip(".") or "0"


def font_at(weight: int):
    if weight not in FONT_CACHE:
        font = TTFont(FONT_PATH)
        if "fvar" in font:
            font = instantiateVariableFont(font, {"wght": weight}, inplace=True)
        FONT_CACHE[weight] = font
    return FONT_CACHE[weight]


def outlined_text(text, x, baseline, size, weight, fill, tracking=-0.025):
    font = font_at(weight)
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = size / font["head"].unitsPerEm
    cursor = x
    paths = []
    bounds = []
    for char in text:
        name = cmap.get(ord(char))
        if name is None:
            raise ValueError(f"Missing glyph: {char!r}")
        glyph = glyph_set[name]
        transform = (scale, 0, 0, -scale, cursor, baseline)
        pen = SVGPathPen(glyph_set, ntos=number)
        glyph.draw(TransformPen(pen, transform))
        paths.append(pen.getCommands())
        bound_pen = BoundsPen(glyph_set)
        glyph.draw(TransformPen(bound_pen, transform))
        if bound_pen.bounds:
            bounds.append(bound_pen.bounds)
        cursor += glyph.width * scale + size * tracking
    box = (
        min(b[0] for b in bounds), min(b[1] for b in bounds),
        max(b[2] for b in bounds), max(b[3] for b in bounds),
    )
    return f'<path fill="{fill}" d="{"".join(paths)}"/>', box


def unit(v):
    length = math.sqrt(sum(n * n for n in v))
    return tuple(n / length for n in v)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def curve(t):
    radius = 1.66 + 0.66 * math.cos(3 * t)
    return (radius * math.cos(2 * t), radius * math.sin(2 * t),
            0.90 * math.sin(3 * t))


def ribbon_point(t, lateral):
    p = curve(t)
    before, after = curve(t - 0.002), curve(t + 0.002)
    tangent = unit(tuple(b - a for a, b in zip(before, after)))
    normal = unit(tuple(b + a - 2 * c for a, b, c in zip(before, after, p)))
    binormal = unit(cross(tangent, normal))
    twist = t + 0.54
    offset = tuple(math.cos(twist) * a + math.sin(twist) * b
                   for a, b in zip(normal, binormal))
    point = tuple(a + lateral * b for a, b in zip(p, offset))
    return rotate(point)


def rotate(point):
    x, y, z = point
    a, b, c = map(math.radians, (52, -28, -24))
    y, z = y * math.cos(a) - z * math.sin(a), y * math.sin(a) + z * math.cos(a)
    x, z = x * math.cos(b) + z * math.sin(b), -x * math.sin(b) + z * math.cos(b)
    x, y = x * math.cos(c) - y * math.sin(c), x * math.sin(c) + y * math.cos(c)
    return x, y, z


def lerp_color(position):
    index = min(int(position * (len(PALETTE) - 1)), len(PALETTE) - 2)
    part = position * (len(PALETTE) - 1) - index
    a, b = PALETTE[index], PALETTE[index + 1]
    rgb = [round(int(a[i:i + 2], 16) * (1 - part) + int(b[i:i + 2], 16) * part)
           for i in (1, 3, 5)]
    return "#" + "".join(f"{n:02X}" for n in rgb)


def line_path(points):
    # Smooth closed Catmull-Rom spline expressed as cubic Beziers.
    pieces = [f"M{number(points[0][0])} {number(points[0][1])}"]
    n = len(points)
    for i in range(n):
        p0, p1 = points[(i - 1) % n], points[i]
        p2, p3 = points[(i + 1) % n], points[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        pieces.append("C" + " ".join(number(v) for p in (c1, c2, p2) for v in p))
    return "".join(pieces) + "Z"


def artwork(mobile, dark):
    center_x, center_y = (361, 564) if mobile else (922, 282)
    target_w, target_h = (466, 324) if mobile else (470, 432)
    samples, strands = 72, 44
    raw = [[ribbon_point(TAU * i / samples, (j / (strands - 1) - 0.5) * 0.90)
            for i in range(samples)] for j in range(strands)]
    min_x = min(p[0] for strand in raw for p in strand)
    max_x = max(p[0] for strand in raw for p in strand)
    min_y = min(p[1] for strand in raw for p in strand)
    max_y = max(p[1] for strand in raw for p in strand)
    scale = min(target_w / (max_x - min_x), target_h / (max_y - min_y))
    mid_x, mid_y = (min_x + max_x) / 2, (min_y + max_y) / 2
    projected = [[(center_x + (p[0] - mid_x) * scale,
                   center_y + (p[1] - mid_y) * scale) for p in strand]
                 for strand in raw]
    output = []
    # A quiet structural silhouette gives the ribbon weight; it is not a glow.
    centerline = projected[strands // 2]
    output.append(f'<path d="{line_path(centerline)}" fill="none" '
                  f'stroke="{"#191524" if dark else "#E2DCEB"}" stroke-width="28" '
                  'stroke-linecap="round" opacity="0.62"/>')
    for j, points in enumerate(projected):
        position = j / (strands - 1)
        color = lerp_color(position)
        # Keep the entire colored ribbon visible even if a renderer freezes at
        # animation time zero. Only the extra edge highlight reveals itself.
        output.append(f'<path d="{line_path(points)}" '
                      f'fill="none" stroke="{color}" stroke-width="{1.65 if mobile else 1.55}" '
                      'stroke-linecap="round" stroke-linejoin="round"/>')
    # An extra light catches the edge, just as the colored ribbon closes.
    output.append(f'<path class="trace" pathLength="1" d="{line_path(projected[-1])}" '
                  f'fill="none" stroke="{"#FFE3A0" if dark else "#C87718"}" '
                  'stroke-width="0.65" opacity="0.9"/>')
    bounds = (center_x + (min_x - mid_x) * scale, center_y + (min_y - mid_y) * scale,
              center_x + (max_x - mid_x) * scale, center_y + (max_y - mid_y) * scale)
    return f'<g class="ribbon" transform-origin="{center_x}px {center_y}px">{"".join(output)}</g>', bounds


def generate(mobile=False, dark=True):
    width, height = (680, 760) if mobile else (1200, 560)
    background = "#0D0E16" if dark else "#F8F6FA"
    foreground = "#F8F5FF" if dark else "#16101F"
    secondary = "#BEB5D0" if dark else "#665B72"
    title = "Lucas Sousa. Construo o próximo."
    description = ("Software, automação e inteligência artificial. "
                   "Uma fita orbital nas cores violeta, magenta, rosa, laranja e amarelo "
                   "permanece inteira desde o primeiro instante. Sua borda luminosa se revela "
                   "durante uma rotação suave; o conjunto fica estático após 4,8 segundos. "
                   "A animação respeita a preferência por movimento reduzido.")
    body = [f'<rect width="{width}" height="{height}" fill="{background}"/>']
    bboxes = {}
    if mobile:
        text_specs = [
            ("Lucas Sousa", 48, 91, 48, 600, foreground),
            ("Construo o", 46, 190, 76, 600, foreground),
            ("próximo.", 46, 272, 76, 600, foreground),
            ("Software, automação e", 50, 329, 25, 400, secondary),
            ("inteligência artificial.", 50, 363, 25, 400, secondary),
        ]
        line_y, line_x, line_width = 109, 50, 72
    else:
        text_specs = [
            ("Lucas Sousa", 64, 116, 49, 600, foreground),
            ("Construo o", 60, 249, 88, 600, foreground),
            ("próximo.", 60, 344, 88, 600, foreground),
            ("Software, automação e", 65, 411, 26, 400, secondary),
            ("inteligência artificial.", 65, 447, 26, 400, secondary),
        ]
        line_y, line_x, line_width = 144, 65, 82
    # The name is a first-class part of the composition, not a small eyebrow.
    for i, spec in enumerate(text_specs):
        path, bounds = outlined_text(*spec)
        body.append(path)
        bboxes[f"text_{i}"] = [round(v, 2) for v in bounds]
    for i, color in enumerate(PALETTE):
        body.append(f'<path d="M{number(line_x + i * line_width / 5)} {line_y}'
                    f'h{number(line_width / 5)}" stroke="{color}" stroke-width="2"/>')
    art, bounds = artwork(mobile, dark)
    body.append(art)
    bboxes["art"] = [round(v, 2) for v in bounds]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
           f'width="{width}" height="{height}" role="img" aria-labelledby="hero-title hero-desc">'
           f'<title id="hero-title">{html.escape(title)}</title>'
           f'<desc id="hero-desc">{html.escape(description)}</desc>'
           '<style>'
           '.trace{stroke-dasharray:1;stroke-dashoffset:0;animation:reveal 4.8s cubic-bezier(.16,1,.3,1) 1 both}'
           '.ribbon{animation:turn 4.8s cubic-bezier(.16,1,.3,1) 1 both}'
           '@keyframes reveal{0%{stroke-dashoffset:.82;opacity:.35}65%{opacity:1}100%{stroke-dashoffset:0;opacity:1}}'
           '@keyframes turn{0%{transform:rotate(-9deg)}100%{transform:rotate(0deg)}}'
           '@media(prefers-reduced-motion:reduce){.trace,.ribbon{animation:none}}'
           '</style>' + "".join(body) + '</svg>\n')
    name = 'hero-' + ('mobile-' if mobile else '') + ('dark' if dark else 'light') + '.svg'
    path = ASSETS / name
    path.write_text(svg, encoding='utf-8')
    print(name, f'{path.stat().st_size:,} bytes', bboxes)


if __name__ == '__main__':
    for mobile_variant in (False, True):
        for dark_variant in (True, False):
            generate(mobile_variant, dark_variant)
