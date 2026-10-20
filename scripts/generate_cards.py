#!/usr/bin/env python3
"""Generate self-contained SVG product cards; no remote fonts or services."""
from pathlib import Path
from html import escape
from math import sin, cos, pi
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parents[1]
BASE = TTFont(ROOT / 'assets/fonts/SpaceGrotesk.ttf')
FONTS = {w: instantiateVariableFont(BASE, {'wght': w}, inplace=False) for w in (400, 500, 600, 700)}
COLORS = ['#7B24FF', '#BF18FF', '#F421A6', '#FF733D', '#FFBE24']

def label(value, x, y, size, color, weight=500):
    font = FONTS[weight]
    glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
    scale, advance = size / font['head'].unitsPerEm, 0
    pen = SVGPathPen(glyphs, ntos=lambda v: str(round(v, 2)))
    for char in value:
        glyph = glyphs[cmap[ord(char)]]
        glyph.draw(TransformPen(pen, (scale, 0, 0, -scale, x + advance, y)))
        advance += glyph.width * scale
    return f'<path fill="{color}" aria-label="{escape(value, quote=True)}" d="{pen.getCommands()}"/>'

def geometry(kind, x, y, mobile):
    s = .70 if mobile else 1
    lines = []
    if kind == 'flow':
        for k in range(15):
            dy = (k - 7) * 4.5
            color = COLORS[min(4, k // 3)]
            lines.append(f'<path d="M0 {dy} C65 {dy},55 {-85+dy},130 {-85+dy} S195 {70+dy},270 {70+dy} S345 {dy},390 {dy}" fill="none" stroke="{color}" stroke-width="1.25" opacity=".65"/>')
    else:
        for k in range(32):
            theta = k / 32 * 2*pi
            cx, cy = cos(theta)*100, sin(theta)*24
            color = COLORS[min(4, k // 7)]
            lines.append(f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="94" ry="48" transform="rotate({k*5.625:.2f} {cx:.2f} {cy:.2f})" fill="none" stroke="{color}" stroke-width="1.1" opacity=".7"/>')
    return f'<g transform="translate({x} {y}) scale({s})">'+''.join(lines)+'</g>'

def card(kind, dark, mobile):
    w, h = (680, 360) if mobile else (1200, 240)
    bg = '#101019' if dark else '#F8F6FC'
    fg = '#F6F2FC' if dark else '#171322'
    muted = '#C2BACE' if dark else '#544C60'
    line = '#30283D' if dark else '#DED7E7'
    name = 'Luwei Flow' if kind == 'flow' else 'LuweiDev'
    detail = 'Gestão integrada. Trabalho conectado.' if kind == 'flow' else 'Engenharia e inteligência artificial.'
    action = 'Conhecer o produto' if kind == 'flow' else 'Acessar a central'
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">', f'<title id="title">{name}</title>', f'<desc id="desc">{detail} {action}.</desc>', f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="{bg}" stroke="{line}"/>']
    if mobile:
        out.append(label(name, 40, 76, 46, fg, 700))
        words = ('Gestão integrada.', 'Trabalho conectado.') if kind == 'flow' else ('Engenharia e', 'inteligência artificial.')
        out.append(label(words[0], 40, 126, 30, muted))
        out.append(label(words[1], 40, 164, 30, muted))
        out.append(geometry(kind, 350 if kind == 'flow' else 513, 247, True))
        out.append(label(action, 40, 290, 26, fg, 600))
        ax, ay = 297 if kind == 'flow' else 262, 279
    else:
        out.append(label(name, 46, 83, 47, fg, 700))
        out.append(label(detail, 46, 130, 27, muted))
        out.append(label(action, 46, 196, 21, fg, 600))
        out.append(geometry(kind, 740 if kind == 'flow' else 932, 130, False))
        ax, ay = 259 if kind == 'flow' else 231, 186
    out.append(f'<path d="M{ax} {ay+8} l14 -14 m-14 0 h14 v14" fill="none" stroke="{fg}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
    out.append('</svg>')
    filename = kind + ('-mobile' if mobile else '') + ('-dark' if dark else '-light') + '.svg'
    (ROOT / 'assets' / filename).write_text('\n'.join(out)+'\n')
    print(filename)

if __name__ == '__main__':
    for kind in ('flow', 'dev'):
        for dark in (False, True):
            for mobile in (False, True):
                card(kind, dark, mobile)
