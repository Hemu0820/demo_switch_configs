from pathlib import Path
from src.generators.config_gen import render_ntp_from_file
from src.adapters.mock_cli import MockCLI
from src.pipeline.plan import diff

def test_ntp_end_to_end():
    candidate = render_ntp_from_file("data/changes/change_001_ntp.yml").strip()
    golden = Path("tests/integration/golden/change_001_ntp.expected").read_text().strip()
    assert candidate == golden

    cli = MockCLI()
    running = cli.show_running_config()
    d = diff(running, candidate)
    assert "ntp server" in d  # something changes
    assert cli.send_config(candidate) == "OK"
