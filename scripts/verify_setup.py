#!/usr/bin/env python3
"""Check this machine is ready for the course.

Run: make verify
"""
import importlib.util
import shutil
import subprocess
import sys

GREEN, RED, YELLOW, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[0m"
required_failures = 0


def ok(message):
    print(f"{GREEN}  ok{RESET}  {message}")


def fail(message, fix):
    global required_failures
    required_failures += 1
    print(f"{RED}fail{RESET}  {message}")
    print(f"        fix: {fix}")


def warn(message, fix):
    print(f"{YELLOW}note{RESET}  {message}")
    print(f"        {fix}")


def check_uv():
    """uv provides the interpreter and the test tooling."""
    uv = shutil.which("uv")
    if uv is None:
        fail("uv not found on PATH", "see INSTALL.md, 'Prerequisites'")
        return
    version = subprocess.run([uv, "--version"], capture_output=True, text=True)
    ok(version.stdout.strip() or "uv")


def check_python():
    """Python 3.10 or later is required."""
    version = sys.version_info
    label = f"Python {version.major}.{version.minor}.{version.micro}"
    if version >= (3, 10):
        ok(label)
    else:
        fail(f"{label} is too old", "install Python 3.10 or later")


def check_package():
    """The sample project must be importable."""
    sys.path.insert(0, "src")
    if importlib.util.find_spec("orderly") is None:
        fail("orderly package not importable",
             "run this from the repository root")
        return
    ok("orderly package imports")


def check_pytest():
    """The regression suite must be green on a fresh clone."""
    if importlib.util.find_spec("pytest") is None:
        fail("pytest is not installed", "run: uv sync")
        return
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--no-header", "-p", "no:cacheprovider"],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        summary = next((l for l in reversed(result.stdout.splitlines())
                        if "passed" in l), "").strip()
        ok(f"regression suite green ({summary})")
    else:
        fail("regression suite is not green",
             "see TROUBLESHOOTING.md, 'make test fails on a fresh clone'")


def check_tasks_are_red():
    """The acceptance tests should be failing before you start."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--no-header", "-p", "no:cacheprovider",
         "tests/tasks"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        ok("acceptance tests are red, as they should be on a fresh clone")
    else:
        warn("acceptance tests already pass",
             "someone has done the tasks already; git stash or re-clone")


def check_optional(command, label, fix):
    """Report on a tool that is useful but not required."""
    if shutil.which(command):
        ok(f"{label} found")
    else:
        warn(f"{label} not found", fix)


def main():
    print("\nChecking your setup\n")
    check_uv()
    check_python()
    check_package()
    check_pytest()
    check_tasks_are_red()

    print("\nAgents and tooling\n")
    check_optional("headroom", "headroom",
                   'uv tool install "headroom-ai[all]==0.40.0", then run: headroom doctor')
    check_optional("node", "node", "needed only for npx ccusage")
    found_agent = any(shutil.which(c) for c in ("claude", "cursor", "copilot"))
    if found_agent:
        ok("a coding agent is on your PATH")
    else:
        warn("no coding agent found on PATH",
             "install one; see INSTALL.md. A GUI-only install is fine.")

    print()
    if required_failures:
        print(f"{RED}{required_failures} required check(s) failed.{RESET} "
              "See TROUBLESHOOTING.md.\n")
        return 1
    print(f"{GREEN}Required checks passed.{RESET} "
          "Run 'headroom doctor' to confirm proxy routing.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
