#!/usr/bin/env python3
"""Refresh site/data for the X$ Board landing page.

1) Optionally rebuild Hot Tips via ../regenerate_hot_tips.py (if present)
2) Copy ../hot_tips.json      → site/data/hot_tips.json
3) Copy ../free_teaser.json   → site/data/free_teaser.json  (Pro board)
4) Rewrite embedded JSON blobs in site/index.html (file:// fallback)
5) Rebuild paid unlock JSON (real handles + last-10 from calls.json) under
   site/<paid_path>/ from stripe_config.json — never onto the free landing page

Usage:
  python site/sync_data.py
  python site/sync_data.py --no-regen   # copy + embed only
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


HOT_EMBED_RE = re.compile(
    r'(<script type="application/json" id="hot-tips-data">).*?(</script>)',
    re.DOTALL,
)
PRO_EMBED_RE = re.compile(
    r'(<script type="application/json" id="pro-board-data">).*?(</script>)',
    re.DOTALL,
)


def rewrite_embeds(index_html: Path, hot: dict, pro: dict) -> None:
    """Replace inline JSON script bodies used as file:// fetch fallbacks."""
    text = index_html.read_text(encoding="utf-8")
    hot_json = json.dumps(hot, ensure_ascii=False, separators=(",", ":"))
    pro_json = json.dumps(pro, ensure_ascii=False, separators=(",", ":"))

    if not HOT_EMBED_RE.search(text) or not PRO_EMBED_RE.search(text):
        raise SystemExit(
            f"ERROR: missing hot-tips-data / pro-board-data embeds in {index_html}"
        )

    # Callable repl avoids re.sub backslash mangling inside JSON payloads.
    text = HOT_EMBED_RE.sub(lambda m: m.group(1) + hot_json + m.group(2), text, count=1)
    text = PRO_EMBED_RE.sub(lambda m: m.group(1) + pro_json + m.group(2), text, count=1)
    index_html.write_text(text, encoding="utf-8")
    print(
        f"Rewrote embeds in {index_html.name} "
        f"(hot={len(hot_json)} chars, pro={len(pro_json)} chars)"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-regen", action="store_true", help="Skip regenerate_hot_tips.py")
    args = parser.parse_args()

    site_dir = Path(__file__).resolve().parent
    root = site_dir.parent
    data_dir = site_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    index_html = site_dir / "index.html"

    regen = root / "regenerate_hot_tips.py"
    if not args.no_regen and regen.is_file():
        print(f"Running {regen.name} …")
        subprocess.check_call([sys.executable, str(regen)], cwd=str(root))

    payloads = {}
    copied = 0
    for name in ("hot_tips.json", "free_teaser.json"):
        src = root / name
        if not src.is_file():
            print(f"ERROR: missing {src}", file=sys.stderr)
            return 1
        dst = data_dir / name
        shutil.copy2(src, dst)
        print(f"Synced {name} → {dst} ({dst.stat().st_size} bytes)")
        payloads[name] = json.loads(src.read_text(encoding="utf-8"))
        copied += 1

    if index_html.is_file():
        rewrite_embeds(index_html, payloads["hot_tips.json"], payloads["free_teaser.json"])
    else:
        print(f"WARN: {index_html} missing — skipped embed rewrite", file=sys.stderr)

    print(f"Done ({copied} files). Hot Tips = default landing view; free_teaser = Pro board tab.")

    # Paid path only: last-10 + real handles. Do not copy paid_board.json into site/data/.
    sys.path.insert(0, str(root))
    from paid_board_build import write_paid_site
    write_paid_site(root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
