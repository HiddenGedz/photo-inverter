from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from PIL import Image, ImageOps


class ImageLoader:
    """Responsible for loading images from disk."""

    def load(self, path: str | Path) -> Image.Image:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"File not found: {p}")
        # Use Image.open lazily but convert to RGB/RGBA to normalize downstream processing
        img = Image.open(p)
        # Preserve alpha if present
        if img.mode in ("RGBA", "LA"):
            return img.convert("RGBA")
        return img.convert("RGB")


class ImageInverter:
    """Applies color inversion to a PIL Image."""

    def invert(self, img: Image.Image) -> Image.Image:
        # If image has alpha, invert only RGB channels and keep alpha as-is
        if img.mode == "RGBA":
            r, g, b, a = img.split()
            rgb = Image.merge("RGB", (r, g, b))
            inv_rgb = ImageOps.invert(rgb)
            r2, g2, b2 = inv_rgb.split()
            return Image.merge("RGBA", (r2, g2, b2, a))
        if img.mode == "RGB":
            return ImageOps.invert(img)
        # Fallback: convert then invert
        return ImageOps.invert(img.convert("RGB"))


class ImageSaver:
    """Responsible for saving images to disk."""

    def save(self, img: Image.Image, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        # Infer format from suffix; default to PNG
        suffix = p.suffix.lower()
        fmt = {
            ".jpg": "JPEG",
            ".jpeg": "JPEG",
            ".png": "PNG",
            ".bmp": "BMP",
            ".tiff": "TIFF",
            ".webp": "WEBP",
        }.get(suffix, "PNG")
        img.save(p, format=fmt)


@dataclass
class ProcessResult:
    input_path: Path
    output_path: Path


class InvertPipeline:
    """High-level orchestration: load -> invert -> save."""

    def __init__(self, loader: Optional[ImageLoader] = None,
                 inverter: Optional[ImageInverter] = None,
                 saver: Optional[ImageSaver] = None) -> None:
        self.loader = loader or ImageLoader()
        self.inverter = inverter or ImageInverter()
        self.saver = saver or ImageSaver()

    def run(self, input_path: str | Path, output_path: str | Path) -> ProcessResult:
        inp = Path(input_path)
        out = Path(output_path)
        img = self.loader.load(inp)
        inv = self.inverter.invert(img)
        self.saver.save(inv, out)
        return ProcessResult(input_path=inp, output_path=out)
