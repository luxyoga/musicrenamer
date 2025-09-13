#!/usr/bin/env python3
import os, re, argparse, unicodedata
from pathlib import Path

INVALID_FS_CHARS = r'\/:*?"<>|'

def clean_text(s: str) -> str:
    # Normalize, collapse spaces, strip bracketed bits ((), [], {})
    s = unicodedata.normalize("NFKC", s)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*[\(\[\{].*?[\)\]\}]\s*", " ", s)  # remove bracketed
    s = re.sub(r"\s+-\s+-\s*", " - ", s)
    s = s.strip(" -._").strip()
    return s

def strip_leading_tracknum(stem: str) -> str:
    # Remove patterns like "01 - ", "1. ", "A1_", "(01) "
    return re.sub(r"^\s*[\(\[]?\s*[A-Za-z]?\s*\d{1,3}\s*[\)\]]?\s*[-._)]?\s*", "", stem).strip()

def sanitize_for_fs(s: str) -> str:
    for ch in INVALID_FS_CHARS:
        s = s.replace(ch, " ")
    return re.sub(r"\s+", " ", s).strip()

def parse_from_filename(stem: str):
    stem = strip_leading_tracknum(stem)
    parts = [p.strip() for p in re.split(r"\s+-\s+", stem, maxsplit=1)]
    if len(parts) == 2:
        artist, title = parts
    else:
        # Try another common pattern "Artist_Title"
        parts = [p.strip() for p in re.split(r"[_–—-]{1,2}", stem, maxsplit=1)]
        artist, title = (parts + [""])[:2] if len(parts) == 2 else ("", stem)
    artist = clean_text(artist) or "Unknown Artist"
    title = clean_text(title) or "Unknown Title"
    return artist, title

def read_tags(p: Path):
    try:
        from mutagen import File as MutaFile
        mf = MutaFile(p)
        if not mf: return None, None
        artist, title = None, None
        # Try common tag keys across formats
        for key in ("artist", "TPE1"):
            if key in mf.tags:
                v = mf.tags.get(key)
                artist = str(v[0]) if isinstance(v, list) else str(v)
                break
        for key in ("title", "TIT2"):
            if key in mf.tags:
                v = mf.tags.get(key)
                title = str(v[0]) if isinstance(v, list) else str(v)
                break
        return artist, title
    except Exception:
        return None, None

def unique_path(dst: Path) -> Path:
    if not dst.exists():
        return dst
    stem, ext = dst.stem, dst.suffix
    i = 1
    while True:
        candidate = dst.with_name(f"{stem} ({i}){ext}")
        if not candidate.exists():
            return candidate
        i += 1

def rename_folder(folder: Path, recursive: bool, use_tags: bool, apply: bool, exts):
    files = []
    for ext in exts:
        files.extend(folder.rglob(f"*{ext}") if recursive else folder.glob(f"*{ext}"))
    files = [f for f in files if f.is_file()]

    changes = []
    for f in files:
        ext = f.suffix
        stem = f.stem
        artist, title = (None, None)

        if use_tags:
            a, t = read_tags(f)
            if a: artist = a
            if t: title = t

        if not artist or not title:
            a2, t2 = parse_from_filename(stem)
            artist = artist or a2
            title  = title  or t2

        artist = sanitize_for_fs(clean_text(artist))
        title  = sanitize_for_fs(clean_text(title))
        if not artist or not title:
            continue

        new_name = f"{artist} - {title}{ext.lower()}"
        dst = unique_path(f.with_name(new_name))
        if f.name != dst.name:
            changes.append((f, dst))

    # Show summary
    if not changes:
        print("No files to rename.")
        return

    print(f"Found {len(changes)} file(s) to rename:\n")
    for src, dst in changes:
        print(f"- {src.name}  ->  {dst.name}")

    if apply:
        print("\nRenaming...")
        for src, dst in changes:
            src.rename(dst)
        print("Done.")
    else:
        print("\n(DRY RUN) No files were changed. Add --apply to perform the rename.")

def main():
    parser = argparse.ArgumentParser(description="Rename music files to 'Artist - Song.ext'")
    parser.add_argument("folder", help="Folder containing your music")
    parser.add_argument("--recursive", action="store_true", help="Process subfolders")
    parser.add_argument("--use-tags", action="store_true",
                        help="Prefer ID3/metadata tags when available (install 'mutagen')")
    parser.add_argument("--apply", action="store_true",
                        help="Actually rename files (otherwise dry run)")
    parser.add_argument("--exts", default=".mp3,.m4a,.flac,.wav",
                        help="Comma-separated extensions to include")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    if not folder.exists():
        print("Folder not found:", folder)
        return

    exts = tuple([e if e.startswith(".") else f".{e}" for e in args.exts.split(",")])
    rename_folder(folder, args.recursive, args.use_tags, args.apply, exts)

if __name__ == "__main__":
    main()
