# Exercise 5: Shrink a Tool Result

**Section 5 · 10 minutes · work alone**

## Objective

Measure what one tool call adds to your window, cut it at the source two different ways, and find out which cut holds without you remembering it.

## Before you start

Nothing new to install, and leave the proxy for Exercise 6; it is introduced after this exercise and is not needed here.

One leftover from Exercise 2: if your context view showed a large MCP tools share there, disable the servers you have not used in a month now (Claude Code: `/mcp`; Cursor: the toggle under Customize; Copilot: the tools picker or the server config). Claude Code, Codex and Copilot CLI defer tool definitions by default, so most people have nothing to do here.

Every run below is a **fresh session**, started the way Exercise 3 started them:

```bash
claude                      # Claude Code; or: codex | copilot
```

Cursor and Copilot in VS Code: a new chat. The delta must start from the same near-empty window each time, and Claude Code reads the rules file only at session start.

## The measurement

The instrument is the context view you used in Exercise 2: `/context` in Claude Code and Copilot CLI, the context ring in Cursor, the context window control in Copilot for VS Code. Read its **messages** figure before and after one tool call and take the difference. That delta is what the result added to the window, and it is what every later request in the session carries.

`tokscale` reports per session and cannot see one call; the proxy sees the wire but not the window. For this exercise the agent's own view is the only instrument that answers the question.

## Steps

1. **The before.** Fresh session, then in the session:

   ```
   /context
   ```

   Note the messages figure. Then ask, the way you normally would:

   > Run the acceptance tests in `tests/tasks` and tell me which tasks still fail.

   The agent runs something like `uv run pytest tests/tasks -v`. When it answers, write down which tasks it said still fail, then:

   ```
   /context
   /exit
   ```

   The difference between the two messages figures is the test log, tracebacks included, now in the window for the rest of that session. That is your **before**.

2. **Cut 1, automated.** Pick the one your agent supports.

   **Claude Code: the hook.** It rewrites any test command before it runs, so the agent only ever sees the failures. Save the script from the cost docs and register it in the repo's local settings, which git ignores:

   ```bash
   mkdir -p ~/.claude/hooks .claude
   cat > ~/.claude/hooks/filter-test-output.sh <<'EOF'
   #!/bin/bash
   input=$(cat)
   cmd=$(echo "$input" | jq -r '.tool_input.command')

   # If running tests, filter to show only failures
   pattern='^(npm test|pytest|go test|uv run pytest|make test|make task)( [^;&|<>`$#\\[:cntrl:]]*)?$'
   if [[ "$cmd" =~ $pattern ]]; then
     filtered_cmd="$cmd 2>&1 | grep -A 5 -E '(FAIL|ERROR|error:)' | head -100"
     echo "$input" | jq --arg filtered "$filtered_cmd" \
       '{hookSpecificOutput: {hookEventName: "PreToolUse", updatedInput: (.tool_input + {command: $filtered})}}'
   else
     echo "{}"
   fi
   EOF
   chmod +x ~/.claude/hooks/filter-test-output.sh
   cat > .claude/settings.local.json <<'EOF'
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Bash",
           "hooks": [
             { "type": "command", "command": "~/.claude/hooks/filter-test-output.sh" }
           ]
         }
       ]
     }
   }
   EOF
   ```

   The pattern is the docs' version with `uv run pytest`, `make test` and `make task` added, because that is what the agent runs in this repo. Fresh session, then:

   ```
   /hooks
   ```

   It must list the hook under `PreToolUse`. Then `/context`, the same prompt as step 1 word for word, `/context`, `/exit`.

   **Any agent: the rules line.** Append one line to the rules file your agent reads:

   ```bash
   printf '\n- When running tests, pipe the output through `grep -E "^(FAILED|ERROR)|passed|failed"` and report only that.\n' >> CLAUDE.md
   ```

   Claude Code reads `CLAUDE.md`; Codex reads `AGENTS.md`; Cursor reads `AGENTS.md` or a file under `.cursor/rules/`; Copilot reads `.github/copilot-instructions.md` or `AGENTS.md`. Fresh session, `/context`, the same prompt as step 1, `/context`, `/exit`. Check the transcript: did the agent actually pipe the command?

   Either way, write the delta down as **cut 1**, with the agent's answer.

3. **Cut 2, by hand.** Take the automation out first:

   ```bash
   rm .claude/settings.local.json       # the hook
   git checkout -- CLAUDE.md            # the rules line; or AGENTS.md, .github/copilot-instructions.md
   ```

   Fresh session, `/context`, then ask for the filtering in the prompt itself:

   > Run the acceptance tests in `tests/tasks` and show me only the failing test names and the summary line.

   `/context`, `/exit`. Write the delta down as **cut 2**, with the agent's answer.

4. **Compare the three.**

   ```
   before   = messages after step 1 - messages before step 1
   cut 1    = the same for step 2         # hook or rules line
   cut 2    = the same for step 3         # the prompt
   held?    = did the filter actually run, and did the answer name the same failing tasks
   ```

   The hook does it every time; the rules line is a request the model may or may not honour; the prompt works only when you remember to write it.

5. **Post in chat** as `before N, cut 1 N (hook|rules), cut 2 N, same answer yes|no, keeping: <hook|rules line|prompt>`.

## Done when

- Three deltas for the same question, one unfiltered and two filtered
- The agent named the same failing tasks every time
- One sentence naming the cut you are keeping, and where it lives

A smaller delta with a different answer is a failed exercise. The filter kept the wrong lines; widen it.

## Expect

On a fresh clone the verbose acceptance run is about 12 KB, roughly 3,000 tokens; through the hook it is about 800, summary lines only about 300. A four to ten times cut on a small repo. Your acceptance suite is partly green by now, so your before is smaller than this; the ratio is what transfers to the repo where the same log is 50 KB.

The rules line is the cut that fails most often: agents follow it on the first run after a fresh start and drift later. If your rules-line delta did not move, check the transcript before blaming the measurement.

## If you get stuck

- **The context view does not show a messages figure.** Read the total before and after instead; the delta is the same.
- **`/hooks` does not list the hook.** You started the session outside the repo root, or the JSON did not parse. `cd` to the root and `cat .claude/settings.local.json | jq .` to check it.
- **The hook is listed but the log still came through whole.** The agent ran a command the pattern does not match. Read the transcript for the exact command and add it to the pattern.
- **The agent ignored the rules line.** That is a result; note it and move to step 3.
- **Every acceptance test already passes.** Use the regression suite instead: ask for `make test` in the prompts. It is smaller, about 450 tokens unfiltered, so expect a smaller cut.
- **`jq` is missing.** The hook needs it: `brew install jq` or your package manager, or use the rules line instead.

The reference answers are in [solution/solution.md](solution/solution.md).
