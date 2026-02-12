#!/usr/bin/env python3
"""Convert GEDCOM files encoded in ANSEL to UTF-8.

Usage:
    python3 gedcom_ansel_to_utf8.py [--inplace] [-o OUT] file1 [file2 ...]

Behavior:
- Tries to detect "ANSEL" in the GEDCOM header (line starting with "1 CHAR").
- If ANSEL is detected (or with --force-ansel), attempts to convert using system iconv.
- If iconv is not available or fails, it exits with a helpful message.
- Rewrites the header ("1 CHAR ANSEL") to "1 CHAR UTF-8" in the converted output (default). Use `--char` to select a different label.

Notes:
- This tool prefers system iconv (common on Linux). If you prefer a pure-python
  implementation, we could add a fallback mapping.
"""

from __future__ import annotations
import argparse
import subprocess
from pathlib import Path
import sys
import shutil


def detect_charset(path: Path) -> str | None:
    try:
        with path.open('rb') as f:
            for _ in range(120):  # read a few header lines
                line = f.readline()
                if not line:
                    break
                try:
                    t = line.decode('ascii', errors='ignore')
                except Exception:
                    continue
                t = t.strip()
                if t.upper().startswith('1 CHAR'):
                    parts = t.split()
                    if len(parts) >= 3:
                        return parts[2].upper()
                    return None
    except Exception:
        return None
    return None


def convert_with_iconv(infile: Path, outfile: Path, char_value: str = 'UTF-8') -> bool:
    iconv = shutil.which('iconv')
    if iconv is not None:
        # try system iconv first
        cmd = [iconv, '-f', 'ANSEL', '-t', 'UTF-8', str(infile)]
        try:
            p = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data = p.stdout
            try:
                text = data.decode('utf-8')
            except Exception:
                text = data.decode('utf-8', errors='replace')
            lines = text.splitlines(True)
            for i, line in enumerate(lines[:200]):
                if line.upper().startswith('1 CHAR'):
                    lines[i] = f'1 CHAR {char_value}' + ('\r\n' if line.endswith('\r\n') else '\n')
                    break
            new = ''.join(lines)
            outfile.write_text(new, encoding='utf-8')
            return True
        except subprocess.CalledProcessError as e:
            print(f"⚠️  iconv failed: {e.stderr.decode(errors='replace')}", file=sys.stderr)
            # fall through to Python fallback
    else:
        print('⚠️  `iconv` not found on PATH. Falling back to built-in ANSEL decoder.', file=sys.stderr)

    # Fallback: use python package 'ansel' (must be installed)
    try:
        import ansel as _ansel
        _ansel.register()
    except Exception as e:
        print('❌  ANSEL fallback not available (install package `ansel` via pip):', e, file=sys.stderr)
        return False

    try:
        raw = infile.read_bytes()
        text = raw.decode('ansel')
    except Exception as e:
        print('❌  Failed to decode file with ANSEL codec:', e, file=sys.stderr)
        return False

    # update header to UTF-8
    lines = text.splitlines(True)
    for i, line in enumerate(lines[:200]):
        if line.upper().startswith('1 CHAR'):
            lines[i] = f'1 CHAR {char_value}' + ('\r\n' if line.endswith('\r\n') else '\n')
            break
    new = ''.join(lines)
    outfile.write_text(new, encoding='utf-8')
    return True


def process_file(inpath: Path, outpath: Path | None, force: bool = False, inplace: bool = False, char_value: str = 'UTF-8') -> int:
    cs = detect_charset(inpath)
    if cs is None and not force:
        print(f"ℹ️  No charset detected in header of {inpath.name}. Use --force-ansel to force ANSEL conversion or -e to set encoding.")
        return 1
    if cs and cs != 'ANSEL' and not force:
        print(f"ℹ️  Charset for {inpath.name} is '{cs}', not ANSEL. Use --force-ansel to force conversion anyway.")
        return 1

    if outpath is None:
        if inplace:
            outpath = inpath.with_suffix(inpath.suffix + '.utf8')
        else:
            outpath = inpath.with_name(inpath.stem + '_utf8' + inpath.suffix)

    success = convert_with_iconv(inpath, outpath, char_value)
    if success:
        print(f"✅  Converted: {inpath} → {outpath}")
        if inplace:
            # replace original
            backup = inpath.with_suffix(inpath.suffix + '.bak')
            inpath.replace(backup)
            outpath.replace(inpath)
            print(f"🔁  Original moved to {backup}")
        return 0
    else:
        print(f"❌  Failed to convert {inpath}")
        return 2


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description='Convert GEDCOM ANSEL -> UTF-8')
    p.add_argument('files', nargs='+', help='GEDCOM file(s) to convert')
    p.add_argument('--inplace', action='store_true', help='Replace original file (writes a .bak)')
    p.add_argument('-o', '--out', help='Output filename (only valid for single input)')
    p.add_argument('--force-ansel', action='store_true', help='Force conversion even if header does not say ANSEL')
    p.add_argument('--char', default='UTF-8', help='Value to write in the header after "1 CHAR" (default: %(default)s)')
    args = p.parse_args(argv)

    if args.out and len(args.files) != 1:
        print('Specify -o/--out only when converting a single file', file=sys.stderr)
        return 3

    exit_codes = []
    for f in args.files:
        inpath = Path(f)
        if not inpath.exists():
            print(f"File not found: {f}", file=sys.stderr)
            exit_codes.append(4)
            continue
        outpath = Path(args.out) if args.out else None
        rc = process_file(inpath, outpath, force=args.force_ansel, inplace=args.inplace, char_value=args.char)
        exit_codes.append(rc)

    return max(exit_codes) if exit_codes else 0


if __name__ == '__main__':
    raise SystemExit(main())
