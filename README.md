# Photo Color Inverter (resume project)

A small learning project: upload a photo → the app inverts its colors → save the result.

## Highlights
- **Component-based design** (split into classes):
  - `ImageLoader` — loads an image
  - `ImageInverter` — inverts colors
  - `ImageSaver` — saves an image
  - `InvertPipeline` — orchestration (load → invert → save)
- **GUI** using Tkinter (built into Python)
- **CLI** for quick terminal usage

## Requirements
- Python **3.10+** (3.11/3.12 recommended)
- Pillow library

## Run (GUI)
1. Unzip the archive.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   python -m app
   ```
4. Usage:
   - `1) Open photo` → select a file
   - `2) Invert colors` → see the result on the right
   - `3) Save as...` → choose where to save

## Run (CLI)
```bash
pip install -r requirements.txt
python -m app.cli input.jpg output.png
```

## Project structure
```
photo-inverter-project-en/
  app/
    __init__.py
    __main__.py      # runs GUI
    components.py    # component classes
    gui.py           # GUI
    cli.py           # CLI
  requirements.txt
  README.md
```

## Ideas to improve it (to look even better on a resume)
- Add tests (`pytest`) for `ImageInverter`
- Add batch processing for a whole folder
- Add extra filters (grayscale/blur/contrast) as separate components
