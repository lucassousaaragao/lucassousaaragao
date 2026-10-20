#!/usr/bin/env python3
"""Build responsive, self-contained stack panels from the bundled brand SVGs.

Run: python scripts/generate_stack.py
Requires fontTools. No network, browser, scripts, or external resources in output.
Original brand files remain unchanged; nested IDs and classes are scoped on import.
Technology labels describe tools in the ecosystem, not proficiency or live status.
"""

from __future__ import annotations

import html
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
BRANDS = ASSETS / "stack"
FONT = ASSETS / "fonts" / "Sora.ttf"
SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", XLINK)
SOURCE_META = {row["name"]: row for row in json.loads((BRANDS / "SOURCES.json").read_text())["sources"]}

# This is the complete public inventory used to generate the panel and text table.
CATEGORIES = [
    ("Linguagens", [
        ("TypeScript", "typescript"), ("JavaScript", "javascript"),
        ("Python", "python"), ("PHP", "php"),
    ]),
    ("Interfaces e desktop", [
        ("React", "react"), ("SolidJS", "solidjs"), ("Electron", "electron"),
        ("Vite", "vite"), ("Tailwind CSS", "tailwindcss"), ("shadcn/ui", "shadcnui"),
        ("Radix UI", "radixui"), ("TanStack", "tanstack"), ("Three.js", "threejs"),
        ("Motion", "framermotion"), ("Livewire", "livewire"), ("Alpine.js", "alpinejs"),
        ("Tiptap", "tiptap"), ("React Flow", "reactflow"), ("Sass", "sass"),
        ("React Hook Form", "reacthookform"),
    ]),
    ("Backend e dados", [
        ("Node.js", "nodejs"), ("Bun", "bun"), ("Deno", "deno"),
        ("Laravel", "laravel"), ("Supabase", "supabase"), ("PostgreSQL", "postgresql"),
        ("MySQL", "mysql"), ("MongoDB", "mongodb"), ("Redis", "redis"),
        ("Drizzle ORM", "drizzle"), ("Effect", "effect"), ("Pydantic", "pydantic"),
        ("Zod", "zod"),
    ]),
    ("Cloud e entrega", [
        ("Docker", "docker"), ("Cloudflare", "cloudflare"), ("Google Cloud", "googlecloud"),
        ("GitHub Actions", "githubactions"), ("Git", "git"), ("GitHub", "github"),
        ("npm", "npm"), ("pnpm", "pnpm"),
    ]),
    ("IA e integrações", [
        ("OpenAI", "openai"), ("Claude", "anthropic"), ("Gemini", "gemini"),
        ("DeepSeek", "deepseek"), ("OpenCode", "opencode"), ("MCP", "modelcontextprotocol"),
        ("Codex", "openai"), ("Claude Code", "anthropic"),
        ("ElevenLabs", "elevenlabs"), ("LiveKit", "livekit"),
    ]),
    ("Qualidade", [
        ("Playwright", "playwright"), ("Vitest", "vitest"),
        ("PHPUnit", "phpunit"), ("ESLint", "eslint"),
    ]),
]


def n(value):
    return f"{value:.3f}".rstrip("0").rstrip(".") or "0"


class Typography:
    """Outline Sora once per glyph, then reuse the shapes for smaller SVGs."""

    def __init__(self):
        self.fonts = {}
        self.definitions = {}

    def font(self, weight):
        if weight not in self.fonts:
            self.fonts[weight] = instantiateVariableFont(TTFont(FONT), {"wght": weight}, inplace=True)
        return self.fonts[weight]

    def width(self, text, size, weight=500):
        font = self.font(weight)
        glyphs = font.getGlyphSet()
        cmap = font.getBestCmap()
        return sum(glyphs[cmap[ord(char)]].width for char in text) * size / font["head"].unitsPerEm

    def text(self, text, x, y, size, color, weight=500, center=False):
        font = self.font(weight)
        glyphs, cmap = font.getGlyphSet(), font.getBestCmap()
        scale = size / font["head"].unitsPerEm
        if center:
            x -= self.width(text, size, weight) / 2
        parts, advance = [], 0
        for char in text:
            name = cmap.get(ord(char))
            if not name:
                raise ValueError(f"Missing Sora glyph: {char}")
            key = f"sora-{weight}-{ord(char):x}"
            glyph = glyphs[name]
            if key not in self.definitions:
                pen = SVGPathPen(glyphs, ntos=n)
                glyph.draw(pen)
                self.definitions[key] = f'<path id="{key}" d="{pen.getCommands()}"/>'
            parts.append(f'<use xlink:href="#{key}" x="{n(advance)}"/>')
            advance += glyph.width
        return (f'<g aria-label="{html.escape(text, quote=True)}" fill="{color}" '
                f'transform="translate({n(x)} {n(y)}) scale({n(scale)} {-scale})">'
                + "".join(parts) + "</g>")

    def wrap(self, value, size, maximum):
        lines = [""]
        for word in value.split():
            candidate = (lines[-1] + " " + word).strip()
            if lines[-1] and self.width(candidate, size) > maximum:
                lines.append(word)
            else:
                lines[-1] = candidate
        if any(self.width(line, size) > maximum for line in lines):
            raise ValueError(f"Label too wide: {value} at {size}px; maximum {maximum}")
        if len(lines) > 2:
            # Keep the established three-word brand name readable on two lines.
            if value == "React Hook Form":
                lines = ["React Hook", "Form"]
            else:
                raise ValueError(f"Label needs more than two lines: {value}")
        return lines


def import_icon(slug, prefix, x, y, size, height=None):
    """Contain the unchanged brand geometry and scope all references."""
    root = ET.fromstring((BRANDS / f"{slug}.svg").read_text())
    forbidden = {"script", "foreignObject", "image", "iframe"}
    ids = {node.attrib["id"]: f"{prefix}-{node.attrib['id']}" for node in root.iter() if "id" in node.attrib}
    classes = {word for node in root.iter() for word in node.attrib.get("class", "").split()}
    for node in root.iter():
        if node.tag.rsplit("}", 1)[-1] in forbidden:
            raise ValueError(f"Unexpected active or linked content in {slug}")
        for attr, value in list(node.attrib.items()):
            if attr.rsplit("}", 1)[-1] == "href" and not value.startswith("#"):
                raise ValueError(f"External SVG dependency in {slug}")
            if attr == "id":
                node.set(attr, ids[value])
            elif attr == "class":
                node.set(attr, " ".join(f"{prefix}-{word}" for word in value.split()))
            else:
                for old, new in ids.items():
                    value = value.replace(f"url(#{old})", f"url(#{new})")
                    if value == f"#{old}":
                        value = f"#{new}"
                node.set(attr, value)
        if node.tag.rsplit("}", 1)[-1] == "style" and node.text:
            css = node.text
            for cls in classes:
                css = re.sub(r"\." + re.escape(cls) + r"(?![\w-])", f".{prefix}-{cls}", css)
            for old, new in ids.items():
                css = css.replace(f"#{old}", f"#{new}")
            node.text = css
    for attr in ("id", "class", "width", "height", "x", "y", "role", "aria-labelledby"):
        root.attrib.pop(attr, None)
    root.set("x", n(x))
    root.set("y", n(y))
    root.set("width", n(size))
    root.set("height", n(size if height is None else height))
    root.set("preserveAspectRatio", "xMidYMid meet")
    # Source monocolor marks intentionally stay black on a light plate.
    root.set("color", "#000000")
    if "fill" not in root.attrib:
        root.set("fill", "#000000")
    return ET.tostring(root, encoding="unicode")


def generate(mobile, dark):
    # Three mobile columns retain full brand names at 24px. Four columns caused
    # neighboring long names to appear joined at a real phone viewport width.
    width, columns, margin = (600, 3, 28) if mobile else (1200, 8, 44)
    cell = (width - 2 * margin) / columns
    row_height, header_height, gap = (128, 72, 12) if mobile else (118, 64, 10)
    symbol = 52 if mobile else 50
    label_size = 24 if mobile else 21
    title_size = 32
    foreground = "#F4F7FC" if dark else "#121A2B"
    background = "#080C16" if dark else "#F4F6FC"
    border = "#243047" if dark else "#D4DCEA"
    height = 22 + sum(header_height + math.ceil(len(items) / columns) * row_height + gap for _, items in CATEGORIES)
    typeface = Typography()
    body = [f'<rect width="{width}" height="{height}" fill="{background}"/>']
    y = 26
    for category_index, (category, items) in enumerate(CATEGORIES):
        label_bounds = []
        body.append(typeface.text(category, margin, y + 32, title_size, foreground, 600))
        rule_y = y + 51
        body.append(f'<path d="M{margin} {rule_y}H{width-margin}" stroke="{border}"/>')
        body.append(f'<path d="M{margin} {rule_y}h96" stroke="url(#aurora-rule)" stroke-width="2"/>')
        grid_y = y + header_height
        for index, (name, slug) in enumerate(items):
            col, row = index % columns, index // columns
            center_x = margin + cell * (col + 0.5)
            top = grid_y + row * row_height
            if slug:
                icon_size = symbol
                plate = SOURCE_META[slug].get("plate") == "light" and slug not in {"phpunit", "reactflow"}
                # Alpine and MySQL have dark outlines whose actual colors need a light field.
                if slug in {"alpinejs", "mysql"}:
                    plate = True
                if plate:
                    edge = symbol + 16
                    plate_width = 116 if slug == "tiptap" else edge
                    body.append(f'<rect x="{n(center_x-plate_width/2)}" y="{n(top-8)}" width="{plate_width}" height="{edge}" rx="12" fill="#F4F6FC"/>')
                    icon_size = symbol - 10
                # The official OpenAI file contains clear space around its central symbol.
                # Scale the containing viewport, keeping all geometry and clear space intact.
                if slug == "openai":
                    icon_size = 100
                # PHPUnit's official wordmark is wide; preserve its original aspect ratio.
                if slug == "phpunit":
                    icon_size = 72
                # Tiptap's official horizontal mark needs a wide viewport.
                # Its 84:20 ratio is contained without cropping or distortion.
                if slug == "tiptap":
                    icon_size = 100
                icon_y = top + (symbol - icon_size) / 2
                icon_height = symbol if slug == "tiptap" else icon_size
                if slug == "tiptap":
                    icon_y = top
                body.append(import_icon(slug, f"logo-{category_index}-{index}", center_x-icon_size/2, icon_y, icon_size, icon_height))
                lines = typeface.wrap(name, label_size, cell - 8)
                for line_index, line in enumerate(lines):
                    body.append(typeface.text(line, center_x, top + symbol + 32 + line_index * (label_size + 4), label_size, foreground, center=True))
                longest = max(typeface.width(line, label_size) for line in lines)
                label_bounds.append((row, col, center_x-longest/2, center_x+longest/2))
            else:
                # Text-only brands are explicit labels; no invented surrogate logos.
                lines = typeface.wrap(name, 26 if mobile else 25, cell - 4)
                for line_index, line in enumerate(lines):
                    baseline = top + 42 + (line_index - (len(lines)-1)/2) * 31
                    body.append(typeface.text(line, center_x, baseline, 26 if mobile else 25, foreground, 500, center=True))
        for left, right in zip(label_bounds, label_bounds[1:]):
            if left[0] == right[0]:
                assert right[2] - left[3] >= 8, (category, left, right)
        y = grid_y + math.ceil(len(items) / columns) * row_height + gap
    description = "; ".join(f"{category}: {', '.join(name for name, _ in items)}" for category, items in CATEGORIES)
    defs = (f'<linearGradient id="aurora-rule" gradientUnits="userSpaceOnUse" x1="{margin}" y1="0" x2="{margin+96}" y2="0">'
            '<stop offset="0" stop-color="#7B24FF"/><stop offset=".48" stop-color="#F421A6"/>'
            '<stop offset="1" stop-color="#FFBE24"/></linearGradient>' + "".join(typeface.definitions.values()))
    output = (f'<svg xmlns="{SVG}" xmlns:xlink="{XLINK}" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="stack-title stack-desc">'
              '<title id="stack-title">Stack de engenharia de Lucas Sousa</title>'
              f'<desc id="stack-desc">{html.escape(description)}</desc><defs>{defs}</defs>'
              + "".join(body) + "</svg>\n")
    # Structural verification catches unresolved logos or malformed generated SVGs.
    tree = ET.fromstring(output)
    ids = [node.get("id") for node in tree.iter() if node.get("id")]
    assert len(ids) == len(set(ids)), "Duplicate SVG IDs"
    assert y <= height + 4, (y, height)
    filename = "stack-" + ("mobile-" if mobile else "") + ("dark" if dark else "light") + ".svg"
    path = ASSETS / filename
    path.write_text(output, encoding="utf-8")
    print(f"{filename}: {width}×{height}, {len(output.encode('utf-8')):,} bytes, {len(typeface.definitions)} glyphs")


if __name__ == "__main__":
    assert sum(len(items) for _, items in CATEGORIES) == 55
    assert len({slug for _, items in CATEGORIES for _, slug in items}) == 53
    for mobile_variant in (False, True):
        for dark_variant in (True, False):
            generate(mobile_variant, dark_variant)
    manifest = [{"category": category, "technologies": [{"name": name, "logo": f"assets/stack/{slug}.svg" if slug else None} for name, slug in items]} for category, items in CATEGORIES]
    (ROOT / "scripts" / "stack.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
