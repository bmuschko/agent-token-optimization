# Installation

Everything below should be done **before** the session, ideally a day ahead.
Total time is about fifteen minutes on a normal network.

Run [`make verify`](Makefile) when you are finished. It prints a green check
when the repo, Python, and the test suite are all working.

## Contents

- [Prerequisites](#prerequisites)
- [The repository](#the-repository)
- [An AI coding agent](#an-ai-coding-agent)
- [Headroom, the measuring proxy](#headroom-the-measuring-proxy)
- [Usage analyzers](#usage-analyzers)
- [Verify everything](#verify-everything)
- [Working offline](#working-offline)

## Prerequisites

| Tool | Version | Why |
|---|---|---|
| Git | any recent | cloning this repo |
| Python | 3.10 or later | the sample project and Headroom |
| Node.js | 20 or later | `npx ccusage` |

```bash
git --version
python3 --version
node --version
```

Node is only needed for `ccusage`. If you would rather not install it, the
exercises still work; you lose one of the two analyzers.

## The repository

```bash
git clone https://github.com/bmuschko/agent-token-optimization
cd agent-token-optimization
```

Create a virtual environment and install the project with its test
dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Confirm the suite is green before you go any further:

```bash
make test
```

## An AI coding agent

You need **one** of these. All exercises work with any of them.

### Claude Code

Native install, which is the recommended path:

```bash
# macOS, Linux, WSL
curl -fsSL https://claude.ai/install.sh | bash
```

```powershell
# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
```

Homebrew and npm also work:

```bash
brew install --cask claude-code
npm install -g @anthropic-ai/claude-code      # needs Node.js 22+
```

Verify, then check the installation in more detail:

```bash
claude --version
claude doctor
```

Claude Code requires a Pro, Max, Team, Enterprise, or Console account. The free
claude.ai plan does not include it. Full details:
[Claude Code setup](https://code.claude.com/docs/en/setup).

### Cursor

Download from [cursor.com](https://cursor.com) and sign in. For the session,
know where your usage dashboard is and which model your Auto setting resolves
to: [Models and pricing](https://cursor.com/docs/models-and-pricing).

### GitHub Copilot

Either the VS Code extension or the CLI. If you use the CLI, note that the
per-interaction token view lives only in the **VS Code Chat Debug View**, so
install the extension too if you want to see per-request numbers. Billing
reference:
[Usage-based billing for individuals](https://docs.github.com/copilot/concepts/billing/usage-based-billing-for-individuals).

## Headroom, the measuring proxy

[Headroom](https://github.com/chopratejas/headroom) is the local proxy every
exercise routes through. It measures tokens and, in Section 5, compresses tool
output. It runs entirely on your machine.

```bash
pip install "headroom-ai[all]"
```

There is also a Node package if you prefer it:

```bash
npm install headroom-ai
```

Requires Python 3.10 or later. The `[all]` extra pulls in the proxy, MCP server
and evaluation support; granular extras such as `[proxy]` and `[mcp]` exist if
you want a smaller install.

Wrap your agent in one command:

```bash
headroom wrap claude        # also: codex, copilot, cursor, aider, opencode
```

`headroom wrap cursor` prints a configuration to paste into Cursor rather than
launching it.

Or run the proxy standalone and point your agent at it:

```bash
headroom proxy --port 8787
export ANTHROPIC_BASE_URL=http://127.0.0.1:8787
```

Check routing and savings:

```bash
headroom doctor      # confirms traffic is actually going through the proxy
headroom stats       # token counts
headroom dashboard   # live view, proxy must be running
```

**Pin the version** noted in [requirements.txt](requirements.txt) so the whole
room is on the same build.

## Usage analyzers

Two tools, two different questions. Both are optional but Exercise 2 is much
better with them.

### ccusage, how much did I spend

No installation needed:

```bash
npx ccusage@latest            # daily report
npx ccusage@latest session    # by session
npx ccusage@latest daily --breakdown   # per model
```

Repository: [ryoppippi/ccusage](https://github.com/ryoppippi/ccusage).

### claude-usage-analyzer, why did I spend it

Ranks your projects and names the controllable token sinks.

```bash
# macOS
brew install SingggggYee/tap/claude-usage-analyzer

# any platform with Rust
cargo install claude-usage-analyzer
```

Prebuilt binaries are also published:

```bash
# Linux x86_64
curl -L https://github.com/SingggggYee/claude-usage-analyzer/releases/latest/download/claude-usage-analyzer-linux-x86_64.tar.gz | tar xz

# macOS Apple Silicon
curl -L https://github.com/SingggggYee/claude-usage-analyzer/releases/latest/download/claude-usage-analyzer-macos-aarch64.tar.gz | tar xz
```

Then:

```bash
claude-usage-analyzer                  # full report, last 30 days
claude-usage-analyzer sessions         # top sessions by cost
```

Repository:
[SingggggYee/claude-usage-analyzer](https://github.com/SingggggYee/claude-usage-analyzer).

**Both analyzers read Claude Code session files** from `~/.claude/projects/`.
Cursor and Copilot users should use their own dashboards instead; the exercises
say where.

## Credentials

Whatever your agent already uses. An Anthropic account for Claude Code, your
Cursor subscription, or your Copilot subscription. Nothing extra is needed for
this course.

Budget roughly **$3** of token usage for the full session.

## Verify everything

```bash
make verify
```

This checks your Python version, that the package imports, that the regression
suite passes, and that the optional tools are on your PATH. It prints a green
check when the required pieces are in place and a note for anything optional
that is missing.

Then confirm the proxy separately:

```bash
headroom doctor
```

Both should be green before the session starts.

## Working offline

If you cannot run your agent live, or your network blocks the proxy:

```bash
export REPLAY_MODE=true
```

Every exercise then works against the recorded sessions in
[replays/](replays/). See [replays/README.md](replays/README.md).

## If something goes wrong

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md). The most common problem by a wide
margin is an SSL-inspecting corporate proxy blocking a download, which is why
this page asks you to install a day ahead.
