from pathlib import Path
from src.generators.config_gen import render_acl_from_file
from src.generators.policies import no_any_any_permit
from src.adapters.mock_cli import MockCLI
from src.pipeline.plan import diff

def test_acl_end_to_end():
    candidate = render_acl_from_file("data/changes/change_002_acl.yml").strip()
    golden = Path("tests/integration/golden/change_002_acl.expected").read_text().strip()
    assert candidate == golden

    # policy check
    assert no_any_any_permit(candidate) is True

    # plan + apply
    cli = MockCLI()
    running = cli.show_running_config()
    d = diff(running, candidate)
    assert "access-list" in d
    assert cli.send_config(candidate) == "OK"
