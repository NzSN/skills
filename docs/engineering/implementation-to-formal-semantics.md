## What it does

Reconstructs source code's semantics through concrete state, invariants, a minimal abstract machine, and formal rules. The implementation remains authoritative, and every abstraction states what it preserves and what it forgets.

The resulting explanation connects mathematical properties back to the code that establishes, checks, or assumes them. It distinguishes an observed guarantee from an assumption that still needs evidence.

## When to reach for it

Type `/implementation-to-formal-semantics`, or the agent reaches for it automatically when a task fits.

- Understand a parser, runtime, compiler pass, library, or protocol through its states and transitions.
- Derive operational rules from an existing implementation.
- Investigate the gap between states the representation permits and states valid execution should reach.

For choosing a module interface or improving its shape, use [codebase-design](https://aihero.dev/skills-codebase-design).

## Prerequisites

Provide the source code or an accessible checkout and identify the module or behavior to explain.

## Explicit abstraction boundaries

An abstract machine can forget a cache or object layout while retaining binding identity, failure states, and observable effects. Each boundary explains that choice so a simpler model cannot silently conceal behavior that matters. Concurrency and recovery stay visible when they affect the result.

## Common questions

**Does this prove the implementation correct?**

No. It distinguishes source evidence, modeling assumptions, and open proof questions. Progress, preservation, and determinism are claimed as theorems only when actually established.

**Is this limited to interpreters or one programming language?**

No. The same method applies to stateful libraries and protocols across languages. Syntax, binding, and typing rules appear only where they have a meaningful role.

## It's working if

- You can trace a formal transition to the source operations that realize it.
- You can tell which invariants are checked and which depend on callers.
- The explanation includes failures and says what state remains afterward.
- You can identify what the model forgets and which assumptions remain unverified.

## Where it fits

A reach-for-it-anytime standalone for understanding existing implementations. Use [codebase-design](https://aihero.dev/skills-codebase-design) when that understanding leads to an interface design question. [ask-matt](https://aihero.dev/skills-ask-matt) maps the wider skill set.
