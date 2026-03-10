#!/usr/bin/env python3

"""mvbook CLI

Example:
  mvbook book1.epub book2.mobi
"""

from pathlib import Path
import argparse
import sys
import json
from urllib import parse, request, error

API_SEARCH = "https://openlibrary.org/search.json"


def format_filename(metadata, orig_path: Path):
    """Format: Author.Title.Year.ISBN.ext

    Assumes metadata has keys: author_name (list), title, first_publish_year, isbn (list)
    """
    author = metadata.get("author_name", ["Unknown"])[0].split(' ')[-1].replace(" ", ".")
    title = metadata.get("title", "Unknown").replace(" ", ".")
    year = str(metadata.get("first_publish_year", ""))
    isbn = metadata.get("isbn", [""])[0]
    ext = orig_path.suffix.lstrip(".")
    parts = [author, title]
    if year:
        parts.append(year)
    if isbn:
        parts.append(isbn)
    return ".".join(parts) + f".{ext}"


def lookup_by_title(title):
    query = parse.urlencode({"q": title})
    url = f"{API_SEARCH}?{query}"
    try:
        with request.urlopen(url, timeout=10) as resp:
            if resp.status != 200:
                raise error.HTTPError(url, resp.status, resp.reason, resp.headers, None)
            data = json.load(resp)
    except Exception:
        raise
    docs = data.get("docs", [])
    if not docs:
        return None
    return docs[0]


def main(argv=None):
    parser = argparse.ArgumentParser(prog="mvbook")
    parser.add_argument("files", nargs="+")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    for f in args.files:
        p = Path(f)
        title_guess = p.stem
        meta = lookup_by_title(title_guess)
        if not meta:
            print(f"No metadata found for {f}", file=sys.stderr)
            continue
        newname = format_filename(meta, p)
        if args.dry_run:
            print(f"{f} -> {newname}")
        else:
            p.rename(p.with_name(newname))
            print(f"Renamed {f} -> {newname}")


if __name__ == "__main__":
    main()
