from durations.__main__ import main


def test_parses_to_seconds(capsys):
    assert main(["1h", "30m"]) == 0
    assert capsys.readouterr().out == "5400\n"


def test_formats_seconds(capsys):
    assert main(["--format", "5400"]) == 0
    assert capsys.readouterr().out == "1h 30m\n"


def test_reports_bad_input_on_stderr(capsys):
    assert main(["soon"]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("durations: ")
