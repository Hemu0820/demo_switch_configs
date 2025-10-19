import difflib

def diff(before: str, after: str) -> str:
    return "\n".join(difflib.unified_diff(
        before.splitlines(), after.splitlines(),
        fromfile="running", tofile="candidate", lineterm=""
    ))
