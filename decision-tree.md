# The Decision Tree

One page. Print it, or keep it open.

```
  measure and attribute (Section 2)
        |
        +-- one task type dominating?
        |        |
        |        +-- exploration or bugs  ->  context discipline (Section 3)
        |        +-- no, it is uniform    ->  check your default model (Section 4)
        |
        +-- high fixed overhead before you type?
        |        -> defer tool loading, or remove the servers (Section 5)
        |
        +-- tool outputs huge?
        |        -> filter at the source, then compress the rest (Section 5)
        |
        v
  after every change: run the tests
```

## The metric

```
cost per completed task = total spend / tasks that pass their tests
```

Not cost per token. A cheap model that fails twice and then succeeds cost you
three runs for one result.

## The order that pays

| Lever | Effort | Section |
|---|---|---|
| Context discipline and caching | low | 3 |
| Model and effort routing | low | 4 |
| Tool definition loading | medium | 5 |
| Tool output compression | medium | 5 |
| Session and history hygiene | low | 5 |

Start at the top. Most people never need to reach the bottom.

## The four dials on every bill

| Dial | Who controls it |
|---|---|
| Input tokens | you, via what enters context |
| Cache read | you, via prefix stability |
| Cache write | you, via how often the prefix changes |
| Output tokens | mostly the model and the task |

## Habits that bust your prefix cache

- Editing the rules file mid-session
- Toggling an MCP server between turns
- Switching models mid-conversation
- Anything dynamic near the top: timestamps, git status, branch names
- Reordering what you attach

Each one turns a 0.1x cache read into a 1.25x cache write.

## The one rule

**Never trade a cheaper bill for broken code.** A 60% token cut that fails the
tests is a 100% waste.
