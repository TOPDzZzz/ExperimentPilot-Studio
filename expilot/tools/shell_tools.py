import subprocess
import shlex
from pathlib import Path
from typing import List

WORKSPACE = Path("workspace").resolve()

DANGEROUS_KEYWORDS: List[str] = [
    "rm -rf",
    "del /s",
    "format",
    "shutdown",
    "reboot",
    ":(){",
    "mkfs",
]


def _is_safe_command(command: str) -> bool:
    """Check if command is safe to execute (no shell injection, no dangerous ops)."""
    lowered = command.lower()
    for keyword in DANGEROUS_KEYWORDS:
        if keyword in lowered:
            return False

    # Block shell metacharacters that enable injection
    dangerous_chars = set("|;&`$(){}[]!#~")
    if any(c in command for c in dangerous_chars):
        return False

    return True


def run_shell(command: str, timeout: int = 20) -> str:
    """Run a shell command safely within workspace sandbox."""
    if not _is_safe_command(command):
        return f"Blocked unsafe command: {command}"

    try:
        args = shlex.split(command)
    except ValueError:
        return f"Failed to parse command: {command}"

    if not args:
        return "Empty command."

    # For commands with path arguments, validate they stay in workspace
    for arg in args:
        if arg.startswith("/") or arg.startswith("C:\\") or arg.startswith("D:\\"):
            resolved = Path(arg).resolve()
            if not str(resolved).startswith(str(WORKSPACE)):
                return f"Path outside workspace blocked: {arg}"

    try:
        result = subprocess.run(
            args,
            shell=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(WORKSPACE),
        )
        output = result.stdout.strip()
        error = result.stderr.strip()

        if result.returncode != 0:
            return f"Command failed with code {result.returncode}\nSTDOUT:\n{output}\nSTDERR:\n{error}"

        return output or "Command executed successfully with no output."
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout} seconds."
    except Exception as e:
        return f"Command error: {e}"
