import pytest
from mvbook.cli import format_filename
from pathlib import Path


def test_format_filename_minimal():
    meta = {
        "author_name": ["J R R Tolkien"],
        "title": "The Two Towers",
        "first_publish_year": 1999,
        "isbn": ["9780618002238"],
    }
    p = Path("dummy.epub")
    res = format_filename(meta, p)
    assert res == "J.R.R.Tolkien.The.Two.Towers.1999.9780618002238.epub"
