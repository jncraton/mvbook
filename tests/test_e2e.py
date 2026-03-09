import os
from pathlib import Path
import pytest
import mvbook.cli as cli


def fake_lookup(title):
    # Return metadata for known titles based on simple matching
    mapping = {
        'The Two Towers': {'author_name': ['J R R Tolkien'], 'title': 'The Two Towers', 'first_publish_year': 1999, 'isbn': ['9780618002238']},
        'tolkien_two_towers': {'author_name': ['J R R Tolkien'], 'title': 'The Two Towers', 'first_publish_year': 1954, 'isbn': ['9780000000001']},
        'tolkien-the-two-towers': {'author_name': ['J R R Tolkien'], 'title': 'The Two Towers', 'first_publish_year': 1954, 'isbn': ['9780000000002']},
        'UnknownTitle': None,
    }
    return mapping.get(title, mapping.get(title.replace('-', '_'), None))


@pytest.mark.parametrize("initial_name, expected_parts", [
    ("The Two Towers.epub", ("J.R.R.Tolkien", "The.Two.Towers", "1999", "9780618002238")),
    ("tolkien_two_towers.mobi", ("J.R.R.Tolkien", "The.Two.Towers", "1954", "9780000000001")),
    ("tolkien-the-two-towers.azw3", ("J.R.R.Tolkien", "The.Two.Towers", "1954", "9780000000002")),
])
def test_end_to_end_dry_run(tmp_path, monkeypatch, capsys, initial_name, expected_parts):
    # create file
    f = tmp_path / initial_name
    f.write_text('dummy')

    # monkeypatch lookup to avoid network
    monkeypatch.setattr(cli, 'lookup_by_title', lambda title: fake_lookup(title))

    # run CLI in dry-run mode
    cli.main(["--dry-run", str(f)])

    captured = capsys.readouterr()
    assert '->' in captured.out
    # Check expected pieces in output new filename
    for part in expected_parts:
        assert part in captured.out


def test_end_to_end_no_metadata(tmp_path, monkeypatch, capsys):
    f = tmp_path / "UnknownTitle.pdf"
    f.write_text('dummy')

    monkeypatch.setattr(cli, 'lookup_by_title', lambda title: fake_lookup(title))

    cli.main(["--dry-run", str(f)])

    captured = capsys.readouterr()
    assert 'No metadata found' in captured.err
