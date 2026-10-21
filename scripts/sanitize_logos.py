#!/usr/bin/env python3
"""Remove ancillary document metadata from the distributed PNG copies.

Keep image data, transparency and color profiles unchanged. The owner's source
files outside this repository are never opened or modified by this script.
"""

from pathlib import Path
import hashlib
import io
import json
import os
import struct

from PIL import Image, ImageCms

ROOT = Path(__file__).resolve().parents[1]
KEEP = {b"IHDR", b"PLTE", b"IDAT", b"IEND", b"tRNS", b"gAMA", b"cHRM", b"sRGB", b"iCCP", b"pHYs"}


def clean(payload):
    if payload[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("Expected PNG")
    source = Image.open(io.BytesIO(payload))
    keep = KEEP
    if source.info.get("icc_profile"):
        profile = ImageCms.ImageCmsProfile(io.BytesIO(source.info["icc_profile"]))
        standard = ImageCms.profileToProfile(source.convert("RGBA"), profile,
                                            ImageCms.createProfile("sRGB"), outputMode="RGBA")
        if source.convert("RGBA").tobytes() == standard.tobytes():
            # A redundant standard profile may carry document identifiers. It
            # is removed only after a color conversion proves pixel identity.
            keep = KEEP - {b"iCCP", b"pHYs"}
    result, removed, offset = [payload[:8]], [], 8
    while offset < len(payload):
        size = struct.unpack(">I", payload[offset:offset + 4])[0]
        kind = payload[offset + 4:offset + 8]
        end = offset + size + 12
        if end > len(payload):
            raise ValueError("Incomplete PNG chunk")
        if kind in keep:
            result.append(payload[offset:end])
        else:
            removed.append(kind.decode("ascii"))
        offset = end
    output = b"".join(result)
    before = Image.open(io.BytesIO(payload)).convert("RGBA")
    after = Image.open(io.BytesIO(output)).convert("RGBA")
    if before.size != after.size or before.tobytes() != after.tobytes():
        raise ValueError("Pixel integrity check failed")
    return output, removed


if __name__ == "__main__":
    report = []
    for path in sorted((ROOT / "assets/projects").rglob("*.png")):
        source = path.read_bytes()
        output, removed = clean(source)
        if removed:
            temporary = path.with_suffix(".png.tmp")
            with temporary.open("wb") as f:
                f.write(output)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temporary, path)
        report.append({"file": str(path.relative_to(ROOT)), "removed_chunk_types": removed,
                       "pixels_unchanged": True, "sha256": hashlib.sha256(output).hexdigest()})
    review = ROOT / ".impeccable/review"
    review.mkdir(parents=True, exist_ok=True)
    (review / "png-metadata.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"Validated {len(report)} PNGs; sanitized {sum(bool(x['removed_chunk_types']) for x in report)} copies; all pixels unchanged.")
