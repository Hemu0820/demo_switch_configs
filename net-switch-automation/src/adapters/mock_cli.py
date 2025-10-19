import time, random

class MockCLI:
    def __init__(self, latency_ms=20, fail_rate=0.0):
        self.latency_ms = latency_ms
        self.fail_rate = fail_rate
        # a minimal 'running config' snapshot
        self._running = """ntp server 1.1.1.1 prefer
snmp-server community public RO
"""

    def show_running_config(self) -> str:
        return self._running

    def send_config(self, config: str) -> str:
        time.sleep(self.latency_ms/1000)
        if random.random() < self.fail_rate:
            raise RuntimeError("apply failed")
        # pretend to merge; for demo we replace
        self._running = config
        return "OK"
