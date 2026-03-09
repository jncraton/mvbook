import pytest
from pathlib import Path
import mvbook.cli as cli


@pytest.mark.parametrize("initial_name, expected_author, expected_title_word", [
    ("The Two Towers.epub", "Tolkien", "Two"),
    ("Pride and Prejudice.epub", "Austen", "Pride"),
    ("The Hobbit.epub", "Tolkien", "Hobbit"),
])
def test_end_to_end_real_network(tmp_path, capsys, initial_name, expected_author, expected_title_word):
    # create file
    f = tmp_path / initial_name
    f.write_text('dummy')

    # run CLI in dry-run mode using real network lookup
    cli.main(["--dry-run", str(f)])

    captured = capsys.readouterr()
    assert '->' in captured.out
    # new filename part is after ->
    newname = captured.out.split('->', 1)[1].strip()
    # ensure extension preserved
    assert newname.endswith(f'.{f.suffix.lstrip(".")}')
    # ensure expected author and title word appear in the generated name
    assert expected_author in newname
    assert expected_title_word in newname


def test_end_to_end_no_metadata(tmp_path, capsys):
    f = tmp_path / "SomeVeryUnlikelyTitleThatDoesNotExist12345.pdf"
    f.write_text('dummy')

    cli.main(["--dry-run", str(f)])

    captured = capsys.readouterr()
    assert 'No metadata found' in captured.err
