#!/usr/bin/env python3
"""Build the code-led profile hero and original-brand project directory.

Run: python scripts/generate_profile.py
Dependencies: fontTools, Pillow. Fonts and source logos are bundled locally.
SVG typography is outlined and reused through glyph definitions. No network,
scripts, external image references, simulated terminal status, or metrics.
"""

from __future__ import annotations

import base64
import hashlib
import html
import io
import json
import os
import re
from pathlib import Path

from PIL import Image, ImageChops
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONT_CACHE = {}
COLORS = ("#7B24FF", "#BF18FF", "#F421A6", "#FF733D", "#FFBE24")
THEMES = {
    "dark": dict(bg="#080C16", surface="#0D1422", fg="#F4F7FC", muted="#A6B5CA",
                 line="#243047", code="#C6D1E4", keyword="#DCAAFF", string="#FFBA86", punctuation="#8FA4C3"),
    "light": dict(bg="#F4F6FC", surface="#EAF0F9", fg="#121A2B", muted="#51617A",
                  line="#D4DCEA", code="#243C60", keyword="#7125B9", string="#99400C", punctuation="#566B89"),
}


def n(value):
    return f"{value:.2f}".rstrip("0").rstrip(".") or "0"


def font_at(family, weight):
    key = (family, weight)
    if key not in FONT_CACHE:
        face = TTFont(ASSETS / "fonts" / f"{family}.ttf")
        if "fvar" in face:
            face = instantiateVariableFont(face, {"wght": weight}, inplace=True)
        FONT_CACHE[key] = face
    return FONT_CACHE[key]


class Canvas:
    def __init__(self, width, height, title, description, theme):
        self.width, self.height = width, height
        self.title, self.description, self.theme = title, description, THEMES[theme]
        self.defs, self.body, self.boxes = {}, [], []
        stops = "".join(f'<stop offset="{i/4:g}" stop-color="{c}"/>' for i, c in enumerate(COLORS))
        self.defs["aurora"] = f'<linearGradient id="aurora" x1="0" y1="0" x2="1" y2=".4">{stops}</linearGradient>'

    def add(self, value):
        self.body.append(value)

    def text_width(self, value, size, family="Sora", weight=500, tracking=-.012):
        f = font_at(family, weight)
        glyphs, cmap = f.getGlyphSet(), f.getBestCmap()
        return sum(glyphs[cmap[ord(c)]].width * size / f["head"].unitsPerEm + size * tracking for c in value)

    def text(self, value, x, y, size, color=None, weight=500, family="Sora", tracking=-.012, anchor="start"):
        f = font_at(family, weight)
        glyphs, cmap = f.getGlyphSet(), f.getBestCmap()
        units = f["head"].unitsPerEm
        width = self.text_width(value, size, family, weight, tracking)
        if anchor == "middle":
            x -= width / 2
        elif anchor == "end":
            x -= width
        cursor, uses = 0, []
        for char in value:
            name = cmap.get(ord(char))
            if name is None:
                raise ValueError(f"Missing glyph {char!r} in {family}")
            glyph = glyphs[name]
            ident = f"g-{family}-{weight}-{ord(char):x}"
            if ident not in self.defs:
                pen = SVGPathPen(glyphs, ntos=n)
                glyph.draw(pen)
                self.defs[ident] = f'<path id="{ident}" d="{pen.getCommands()}"/>'
            if char != " ":
                uses.append(f'<use xlink:href="#{ident}" x="{n(cursor)}"/>')
            cursor += glyph.width + tracking * units
        label = html.escape(value, quote=True)
        scale = size / units
        self.add(f'<g aria-label="{label}" fill="{color or self.theme["fg"]}" transform="translate({n(x)} {n(y)}) scale({n(scale*1000000)}e-6 {-scale:g})">{"".join(uses)}</g>')
        self.boxes.append(dict(text=value, x=round(x, 2), right=round(x + width, 2), baseline=y, size=size))
        if x < 0 or x + width > self.width + .5 or y > self.height:
            raise ValueError(f"Text outside canvas: {value} {x=} {width=} {self.width=}")
        return width

    def wrap(self, text, x, y, max_width, size, color=None, weight=400, leading=1.4):
        line = ""
        for word in text.split():
            proposed = (line + " " + word).strip()
            if line and self.text_width(proposed, size, weight=weight) > max_width:
                self.text(line, x, y, size, color, weight)
                y += size * leading
                line = word
            else:
                line = proposed
        if line:
            self.text(line, x, y, size, color, weight)
        return y

    def image(self, filename, x, y, width, height, label):
        payload = Path(filename).read_bytes()
        Image.open(io.BytesIO(payload)).verify()
        data = base64.b64encode(payload).decode("ascii")
        self.add(f'<image x="{x}" y="{y}" width="{width}" height="{height}" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/png;base64,{data}" aria-label="{html.escape(label, quote=True)}"/>')

    def save(self, filename, style=""):
        output = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" role="img" aria-labelledby="title desc">'
                  f'<title id="title">{html.escape(self.title)}</title><desc id="desc">{html.escape(self.description)}</desc>'
                  f'<defs>{"".join(self.defs.values())}</defs>' + (f'<style>{style}</style>' if style else "") + "".join(self.body) + '</svg>\n')
        target = ASSETS / filename
        target.write_text(output)
        print(filename, target.stat().st_size)
        return dict(file=filename, width=self.width, height=self.height, bytes=target.stat().st_size, text_bounds=self.boxes)


def prepare_brands():
    """Create small web copies; preserve each supplied original unchanged.

    Transparent/blank page margins are trimmed; no mark is redrawn or recolored.
    Images are reduced proportionally with a lossless PNG container.
    """
    destination = ASSETS / "projects" / "web"
    destination.mkdir(exist_ok=True)
    records = []
    for slug in ("luwei", "flow", "dev", "zenit", "horora", "union", "cuidarpro", "eaudit", "pericia"):
        source = ASSETS / "projects" / f"{slug}.png"
        im = Image.open(source).convert("RGBA")
        original_size = im.size
        if slug in ("eaudit", "cuidarpro"):
            # These supplied logos sit on a white page; detect only page margins.
            rgb = im.convert("RGB")
            minimum = ImageChops.darker(ImageChops.darker(rgb.getchannel("R"), rgb.getchannel("G")), rgb.getchannel("B"))
            ink = minimum.point(lambda p: 255 if p < 185 else 0)
            bounds = ink.getbbox()
        elif slug not in ("dev", "pericia"):
            bounds = im.getchannel("A").getbbox()
        else:
            bounds = (0, 0, im.width, im.height)
        x0, y0, x1, y1 = bounds
        bounds = (max(0, x0 - 8), max(0, y0 - 8), min(im.width, x1 + 8), min(im.height, y1 + 8))
        im = im.crop(bounds)
        im.thumbnail((420, 270), Image.Resampling.LANCZOS)
        target = destination / source.name
        buffer = io.BytesIO()
        im.save(buffer, format="PNG", optimize=True)
        payload = buffer.getvalue()
        Image.open(io.BytesIO(payload)).verify()
        temporary = target.with_suffix(".png.tmp")
        with temporary.open("wb") as output:
            output.write(payload)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, target)
        if target.read_bytes() != payload:
            raise OSError(f"Incomplete write: {target.name}")
        records.append(dict(name=slug, source=f"projects/{source.name}", web_copy=f"projects/web/{source.name}",
                            source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(), source_size=list(original_size),
                            crop=list(bounds), output_size=list(im.size), sha256=hashlib.sha256(target.read_bytes()).hexdigest(),
                            operation="Only empty margin trim and proportional downscale; original retained."))
    (ASSETS / "projects" / "SOURCES.json").write_text(json.dumps({"origin":"Original logos supplied by the owner for this README", "marks":"All rights remain with their respective owners.", "assets":records}, indent=2, ensure_ascii=False)+"\n")


def draw_code(c, x, y, size, line_height, number_x):
    lines = (ROOT / "profile.ts").read_text().strip().splitlines()
    token = re.compile(r'"[^"\\]*(?:\\.[^"\\]*)*"|\b(?:export|const|as)\b|\b\w+\b|\s+|.')
    for index, line in enumerate(lines):
        baseline = y + index * line_height
        c.text(str(index + 1), number_x, baseline, size - 2, c.theme["muted"], 400, "JetBrainsMono", 0, "end")
        cursor = x
        for match in token.finditer(line):
            value = match.group(0)
            color = c.theme["string"] if value.startswith('"') else c.theme["keyword"] if value in ("export", "const", "as") else c.theme["punctuation"] if value in "[]{}:,;" else c.theme["code"]
            cursor += c.text(value, cursor, baseline, size, color, 400, "JetBrainsMono", 0)


def hero(mobile, theme):
    width, height = (600, 800) if mobile else (1200, 620)
    c = Canvas(width, height, "Lucas Sousa — Engenheiro de Software", "Fundador da Luwei Software House. Software, automação e inteligência artificial. O código mostrado vem do arquivo profile.ts deste repositório. Uma linha aurora acompanha a estrutura do código durante 4,8 segundos e depois para. Movimento reduzido é respeitado.", theme)
    t = c.theme
    c.add(f'<rect width="{width}" height="{height}" fill="{t["bg"]}"/>')
    # Open architectural frame, with one chamfer derived from the code bracket.
    c.add(f'<path d="M1 39 V1 H{width-40} L{width-1} 40 V{height-1} H1 V{height-42}" fill="none" stroke="{t["line"]}"/>')
    if mobile:
        c.image(ASSETS / "projects/web/luwei.png", 433, 29, 128, 124, "Logo original da Luwei Software House")
        c.text("Lucas", 37, 128, 79, weight=650, tracking=-.032)
        c.text("Sousa.", 37, 211, 79, weight=650, tracking=-.032)
        c.text("Engenheiro de Software", 40, 266, 30, weight=550)
        c.text("Fundador da Luwei Software House", 41, 306, 23, t["muted"], 400)
        c.text("Software, automação e IA.", 41, 349, 25, t["fg"], 400)
        code_x, code_y, code_size, line_height, num_x = 84, 451, 23, 32, 62
        c.text("profile.ts", 83, 401, 23, t["muted"], 400, "JetBrainsMono", 0)
        c.add(f'<path d="M40 420 H559 M72 430 V687" fill="none" stroke="{t["line"]}"/>')
        trace = "M40 373 H533 L560 400 V691 L535 716 H81 L41 755"
        c.text("Ideias em código.", 83, 754, 25, weight=500)
    else:
        c.image(ASSETS / "projects/web/luwei.png", 997, 27, 137, 133, "Logo original da Luwei Software House")
        c.text("Lucas", 64, 178, 105, weight=650, tracking=-.032)
        c.text("Sousa.", 64, 288, 105, weight=650, tracking=-.032)
        c.text("Engenheiro de Software", 69, 348, 30, weight=550)
        c.text("Fundador da Luwei", 70, 393, 23, t["muted"], 400)
        c.text("Software House", 70, 424, 23, t["muted"], 400)
        c.text("Ideias em código.", 70, 490, 29, weight=500)
        c.text("Código em produto.", 70, 528, 29, weight=500)
        c.add(f'<path d="M564 84 V534" stroke="{t["line"]}"/>')
        code_x, code_y, code_size, line_height, num_x = 677, 251, 21, 35, 645
        c.text("profile.ts", 677, 192, 22, t["muted"], 400, "JetBrainsMono", 0)
        c.add(f'<path d="M623 211 H1134 M660 225 V515" fill="none" stroke="{t["line"]}"/>')
        trace = "M515 567 H588 L618 537 V197 L645 170 H946 L974 142"
        c.text("Software, automação e inteligência artificial.", 70, 588, 20, t["muted"], 400)
    draw_code(c, code_x, code_y, code_size, line_height, num_x)
    # The full line exists at time zero; only a short highlight traverses it.
    c.add(f'<path d="{trace}" fill="none" stroke="url(#aurora)" stroke-width="1.5" stroke-linecap="round"/>')
    c.add(f'<path class="trace" pathLength="1" d="{trace}" fill="none" stroke="{t["fg"]}" stroke-width="2" stroke-linecap="round"/>')
    # Bracket syntax becomes the signature linework; it never obscures code.
    if not mobile:
        c.add(f'<path d="M1161 259 H1152 V315 Q1152 331 1138 331 Q1152 331 1152 347 V463 H1161" fill="none" stroke="url(#aurora)" stroke-width="2"/>')
    style = '.trace{stroke-dasharray:.045 .955;stroke-dashoffset:0;opacity:0;animation:trace 4.8s cubic-bezier(.16,1,.3,1) 1 both}@keyframes trace{0%{stroke-dashoffset:1;opacity:0}8%{opacity:.9}85%{opacity:.9}100%{stroke-dashoffset:0;opacity:0}}@media(prefers-reduced-motion:reduce){.trace{animation:none;opacity:0}}'
    filename = "hero-" + ("mobile-" if mobile else "") + theme + ".svg"
    return c.save(filename, style)


PROJECTS = [
    dict(slug="flow", name="Luwei Flow", copy="Projetos, tarefas, finanças e reuniões.", url="https://luweiflow.com.br/", plate="dark"),
    dict(slug="dev", name="LuweiDev", copy="Desenvolvimento assistido por IA.", url="https://luweidev.com.br/", plate="dark"),
    dict(slug="zenit", name="Zênit", copy="Gestão de SST e medicina do trabalho.", url="https://softzenit.com.br/", plate="light"),
    dict(slug="horora", name="Horora", copy="Sua empresa é a plataforma.", url=None, plate="light"),
    dict(slug="cuidarpro", name="CuidarPro", copy="Saúde mental ocupacional e riscos psicossociais.", url="https://cuidarpro.com.br/", plate="light"),
    dict(slug="eaudit", name="eAudit", copy="", url=None, plate="light"),
    dict(slug="pericia", name="Projeto Perícia Paraíba", copy="Perícias e exames admissionais.", url="https://periciaparaiba.com.br/", plate="dark"),
    dict(slug="union", name="Union", copy="", url=None, plate="light"),
]


def projects(mobile, theme):
    width, height, row_h = (600, 1640, 200) if mobile else (1200, 980, 232)
    c = Canvas(width, height, "Projetos no ecossistema Luwei", "Logos originais: Luwei Flow, LuweiDev, Zênit, Horora, CuidarPro, eAudit, Projeto Perícia Paraíba e Union. Os links públicos disponíveis estão em texto logo após esta imagem.", theme)
    t = c.theme
    c.add(f'<rect width="{width}" height="{height}" fill="{t["bg"]}"/>')
    if not mobile:
        c.add(f'<path d="M600 24 V956" stroke="{t["line"]}"/>')
    for i, project in enumerate(PROJECTS):
        row, col = (i, 0) if mobile else (i // 2, i % 2)
        x, y = col * 600, 28 + row * row_h
        if row:
            c.add(f'<path d="M{x+26} {y-10} H{x+574}" stroke="{t["line"]}"/>')
        logo_x, logo_y = x + 27, y + 22
        logo_w, logo_h = (186, 136) if mobile else (207, 154)
        if project["plate"] == "light":
            c.add(f'<rect x="{logo_x}" y="{logo_y}" width="{logo_w}" height="{logo_h}" rx="8" fill="#FFFFFF"/>')
        elif project["slug"] == "dev":
            c.add(f'<rect x="{logo_x}" y="{logo_y}" width="{logo_w}" height="{logo_h}" rx="8" fill="#060611"/>')
        elif theme == "light":
            c.add(f'<rect x="{logo_x}" y="{logo_y}" width="{logo_w}" height="{logo_h}" rx="8" fill="#080C16"/>')
        c.image(ASSETS / f'projects/web/{project["slug"]}.png', logo_x + 10, logo_y + 10, logo_w - 20, logo_h - 20, f'Logo original de {project["name"]}')
        tx, title_y = x + (240 if mobile else 262), y + 64
        title_size = 29 if mobile else 31
        if project["slug"] == "pericia":
            c.text("Projeto Perícia", tx, title_y - 7, 27, weight=600)
            c.text("Paraíba", tx, title_y + 28, 27, weight=600)
            copy_y = title_y + 68
        else:
            c.text(project["name"], tx, title_y, title_size, weight=600)
            copy_y = title_y + 41
        if project["copy"]:
            c.wrap(project["copy"], tx, copy_y, 327 if mobile else 300, 23 if mobile else 21, t["muted"])
    return c.save("projects-" + ("mobile-" if mobile else "") + theme + ".svg")


if __name__ == "__main__":
    prepare_brands()
    report = []
    for mobile in (False, True):
        for theme in ("dark", "light"):
            report.extend((hero(mobile, theme), projects(mobile, theme)))
    review = ROOT / ".impeccable/review"
    review.mkdir(parents=True, exist_ok=True)
    (review / "profile-geometry.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
