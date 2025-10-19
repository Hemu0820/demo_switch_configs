from ..adapters.mock_cli import MockCLI

def apply_config(candidate_cfg: str) -> str:
    cli = MockCLI()
    return cli.send_config(candidate_cfg)
