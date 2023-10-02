import subprocess


def test_newsletter_cli(monkeypatch):
    result = subprocess.run(
        ["python", "-m", "src.cli", "newsletter"], capture_output=True, text=True
    )

    # Check the return code to see if the command ran successfully
    assert result.returncode == 1
