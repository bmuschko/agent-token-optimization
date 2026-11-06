# Solution: Tool Output Compression

## What the numbers usually look like

| Turn | Forwarded | Saved |
|---|---|---|
| The acceptance-test question, log arriving unfiltered | the system prompt, rules file, conversation and the compressed log | most of the log: Headroom's own example takes a 10,144-token log dump to 1,260, with the failure line kept |
| An ordinary turn, no tool result | the same prefix plus a short answer | close to zero |

Two things to read off that table. The saving lives in one place, the repetitive tool result; the proxy does not touch the prefix or the model's own text, which is why the share over the whole request is far below the share on the log alone. And the saving on a turn without noisy output is nothing, which is the honest version of the headline number.

Headroom's own figures: 60 to 95% on JSON-heavy payloads, about 20% on coding-agent traffic, 21% on a hundred-result code search and 57% on an SRE incident log in its seeded benchmark. All true, each for its workload. Yours is the one you just measured.

## Did the answer survive

It usually does, because the log compressor keeps the failure lines and the summary, which is all the model needs to name the failing tasks. When it does not, the usual cause is a traceback that lost the line that mattered. That is not an argument against compression; it is the argument for step 4. The token counter cannot tell you the answer changed. Only the comparison can, and in your own work the test suite plays that role.

## Where this sits in the order

1. **Narrow the request.** The specific prompt, the summary flag. Free, and cannot lose what you chose to keep.
2. **Automate the narrowing.** The hook or the rules line from Exercise 5. Free, and nobody has to remember.
3. **Route the noisy step to a subagent.** The log lives in its window and only the summary comes back.
4. **Compress what is left.** This exercise. For the output you do not control: JSON from an API you did not write, a log you cannot reshape, a tool that returns a document when you wanted two fields.

Exercise 5 and this one measured the same log twice. The hook removed the noise before the agent saw it, for free, and the answer was never at risk. Compression removed it on the wire, with a proxy to run, and the answer had to be checked. Prefer the first; keep the second for what the first cannot reach.

## Where it does not help

- **Prose and already-dense output.** Headroom says so itself; the step 5 turn shows it.
- **Small results.** A 400-token answer gains nothing and costs a hop.
- **Cursor.** Its requests go through Cursor's servers; no local proxy sees them.

## The method that fails most often

An unrouted agent. `headroom wrap` started the proxy, but the agent was launched from another terminal or another directory and went straight to the API, and the ledger reads zero. `headroom doctor` from the `wrap` directory is the check; a zero counter is never a result.
