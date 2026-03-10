import pytest
from pathlib import Path
import re
import mvbook.cli as cli


@pytest.mark.parametrize(
    "initial_name, expected_author, expected_title_word",
    [
        ("The Two Towers.epub", "Tolkien", "Two"),
        ("Pride and Prejudice.epub", "Austen", "Pride"),
        ("The Hobbit.epub", "Tolkien", "Hobbit"),
        ("Kandinsky Point Line Plane 2012.epub", "Kandinsky", "Point"),
    ],
)
def test_end_to_end_real_network(
    tmp_path, capsys, initial_name, expected_author, expected_title_word
):
    # create file
    f = tmp_path / initial_name
    f.write_text("dummy")

    # run CLI in dry-run mode using real network lookup
    cli.main(["--dry-run", str(f)])

    captured = capsys.readouterr()
    assert "->" in captured.out
    # new filename part is after ->
    newname = captured.out.split("->", 1)[1].strip()
    # ensure extension preserved
    assert newname.endswith(f'.{f.suffix.lstrip(".")}')
    # ensure expected author and title word appear in the generated name
    assert expected_author in newname
    assert expected_title_word in newname


def test_end_to_end_no_metadata(tmp_path, capsys):
    f = tmp_path / "SomeVeryUnlikelyTitleThatDoesNotExist12345.pdf"
    f.write_text("dummy")

    cli.main(["--dry-run", str(f)])

    captured = capsys.readouterr()
    assert "No metadata found" in captured.err


def test_end_to_end_isbn_appended(tmp_path, capsys):
    # create file with a real title likely to have ISBN in OpenLibrary
    f = tmp_path / "The Hobbit.epub"
    f.write_text("dummy")

    # probe API first to ensure an ISBN is available; skip if not
    title_guess = "The Hobbit"
    meta = cli.lookup_by_title(title_guess)
    if not meta or not meta.get("isbn"):
        pytest.skip(f"OpenLibrary returned no ISBN for title: {title_guess}")

    expected_isbn = meta.get("isbn", [None])[0]

    # run CLI using real network lookup
    cli.main(["--dry-run", str(f)])

    captured = capsys.readouterr()
    assert "->" in captured.out
    newname = captured.out.split("->", 1)[1].strip()
    # ensure the specific ISBN returned by the API appears in the generated name
    assert expected_isbn in newname
    # ensure extension preserved
    assert newname.endswith('.epub')
