# Music Renamer — `Artist - Title.ext`

Batch-rename audio files to a clean format like `Artist - Song Name.mp3`.  
Drops leading track numbers (e.g., `01 -`), trims bracketed suffixes like `(Radio Edit)` by default, and optionally reads proper tags with `mutagen`.

![Demo](docs/demo.png) <!-- optional: add later or remove this line -->

## Why?
DJ/label packs often come as `01 - Artist - Song (Extended Mix).mp3`. This tool:
- Removes leading numbering (`01 -`, `(01)`, `A1_`, etc.)
- Cleans punctuation/spacing
- Keeps `Artist - Title` (falls back to filename if tags are missing)
- Avoids overwriting by appending `(1)`, `(2)`, etc.

## Features
- **Dry run by default** — preview before any changes.
- **Tag-aware** (optional `--use-tags`) via `mutagen`.
- **Recursive mode** with `--recursive`.
- Supports `.mp3, .m4a, .flac, .wav` (configurable with `--exts`).

## Example

<p float="left" align="center">
  <div style="display:inline-block; margin-right:20px; text-align:center;">
    <strong>Before</strong><br/>
    <img src="Musicrenamer_Before.png" width="400"/>
  </div>
  
  <div style="display:inline-block; text-align:center;">
    <strong>After</strong><br/>
    <img src="Musicrenamer_After.png" width="400"/>
  </div>
</p>

## Install

```bash
# Clone
git clone https://github.com/<your-username>/music-renamer.git
cd music-renamer
```

### (Optional) create a venv
```
python3 -m venv .venv && source .venv/bin/activate
```

### Install tag support (optional but recommended)
```
pip install -r requirements.txt
```


## Usage

### 1. Clone the repo
```
git clone https://github.com/luxyoga/musicrenamer.git
cd musicrenamer
```

### 2. (Optional) Create a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows (PowerShell)
```

### 3. Install dependencies
```
pip install -r requirements.txt
```

### 4. Run the script
```
# Preview changes (no files renamed)
python3 rename_music.py "/path/to/your/music/folder"

# Use tags if available (requires mutagen, already included in requirements)
python3 rename_music.py "/path/to/your/music/folder" --use-tags

# Apply the changes
python3 rename_music.py "/path/to/your/music/folder" --use-tags --apply
```

### 5. Optional: Install as CLI command
If you’d like to call it directly as music-renamer, install it in editable mode:
```
pip install -e .
```
Then you can run:
```
music-renamer "/path/to/your/music/folder" --use-tags --apply
```
