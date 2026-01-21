from __future__ import annotations

import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

from PIL import ImageTk, Image

from .components import InvertPipeline


class PhotoInverterGUI(tk.Tk):
    """Simple Tkinter GUI with component-based core pipeline."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Photo Color Inverter")
        self.geometry("980x620")
        self.minsize(900, 560)

        self.pipeline = InvertPipeline()

        self.input_path: Path | None = None
        self.original_img: Image.Image | None = None
        self.inverted_img: Image.Image | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        # Top controls
        top = tk.Frame(self, padx=12, pady=10)
        top.pack(fill=tk.X)

        self.btn_open = tk.Button(top, text="1) Open photo", command=self.open_file)
        self.btn_open.pack(side=tk.LEFT)

        self.btn_invert = tk.Button(top, text="2) Invert colors", command=self.invert_current, state=tk.DISABLED)
        self.btn_invert.pack(side=tk.LEFT, padx=(10, 0))

        self.btn_save = tk.Button(top, text="3) Save as...", command=self.save_inverted, state=tk.DISABLED)
        self.btn_save.pack(side=tk.LEFT, padx=(10, 0))

        self.status = tk.Label(top, text="Ready", anchor="w")
        self.status.pack(side=tk.LEFT, padx=(16, 0), fill=tk.X, expand=True)

        # Image panels
        body = tk.Frame(self, padx=12, pady=10)
        body.pack(fill=tk.BOTH, expand=True)

        left = tk.LabelFrame(body, text="Original", padx=8, pady=8)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        right = tk.LabelFrame(body, text="Inverted", padx=8, pady=8)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.lbl_original = tk.Label(left)
        self.lbl_original.pack(fill=tk.BOTH, expand=True)

        self.lbl_inverted = tk.Label(right)
        self.lbl_inverted.pack(fill=tk.BOTH, expand=True)

        # Footer hint
        footer = tk.Label(self, text="Supported: PNG/JPG/BMP/TIFF/WEBP (via Pillow).", padx=12, pady=6, anchor="w")
        footer.pack(fill=tk.X)

    def _set_status(self, text: str) -> None:
        self.status.config(text=text)
        self.update_idletasks()

    def open_file(self) -> None:
        path = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return
        try:
            self.input_path = Path(path)
            self.original_img = self.pipeline.loader.load(self.input_path)
            self.inverted_img = None

            self._render_image(self.original_img, self.lbl_original)
            self.lbl_inverted.config(image="")
            self.lbl_inverted.image = None

            self.btn_invert.config(state=tk.NORMAL)
            self.btn_save.config(state=tk.DISABLED)
            self._set_status(f"Opened: {self.input_path.name}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def invert_current(self) -> None:
        if self.original_img is None:
            return
        try:
            self._set_status("Inverting...")
            self.inverted_img = self.pipeline.inverter.invert(self.original_img)
            self._render_image(self.inverted_img, self.lbl_inverted)
            self.btn_save.config(state=tk.NORMAL)
            self._set_status("Ready: inversion completed")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self._set_status("Inversion error")

    def save_inverted(self) -> None:
        if self.inverted_img is None:
            return
        default_name = (self.input_path.stem + "_inverted.png") if self.input_path else "inverted.png"
        path = filedialog.asksaveasfilename(
            title="Save inverted image",
            defaultextension=".png",
            initialfile=default_name,
            filetypes=[
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("WEBP", "*.webp"),
                ("BMP", "*.bmp"),
                ("TIFF", "*.tiff"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return
        try:
            out_path = Path(path)
            self.pipeline.saver.save(self.inverted_img, out_path)
            self._set_status(f"Saved: {out_path.name}")
            messagebox.showinfo("Saved", f"File saved:\n{out_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _render_image(self, img: Image.Image, label: tk.Label) -> None:
        # Fit image to the current label size
        label.update_idletasks()
        w = max(label.winfo_width(), 300)
        h = max(label.winfo_height(), 300)

        copy = img.copy()
        copy.thumbnail((w, h))
        tk_img = ImageTk.PhotoImage(copy)
        label.config(image=tk_img)
        label.image = tk_img  # keep reference


def main() -> None:
    app = PhotoInverterGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
