## What it does

`formal-semantics` explains a piece of source code by reconstructing its semantics in four layers: the concrete implementation, the invariants it depends on, a minimal **abstract machine**, and a formal semantics (syntax, judgments, statics, dynamics, in the style of programming-language theory). Every move between layers is an explicit **abstraction boundary** that declares what the model kept and what it erased.

The source code stays the ground truth throughout. The skill never starts from a tidy mathematical model and bends the code to fit: every claimed invariant must point at the code that establishes, checks, or assumes it, and every formal rule maps back to the functions that realize it. A summary tells you what the code does; this reconstructs what the code *is*: its states, its legal transitions, and the gap between the states the representation permits and the states execution can actually reach.

## When to reach for it

Type `/formal-semantics`, or the agent reaches for it automatically when a task fits.

Reach for it when the question is "how does this code really work" and a prose walkthrough won't carry the weight. It is most at home on language machinery and runtimes (parsers, lexers, type checkers, interpreters, compilers, VMs, garbage collectors, concurrency runtimes, protocol state machines), but the method is language-agnostic and works on any module with interesting state.

Several skills sit close to it. Which one you want depends on what you actually need:

| The situation | The skill |
|---|---|
| Understand how an implementation works, down to its states and transitions | `formal-semantics` |
| Change the shape of the code: seams, interfaces, depth | [codebase-design](https://aihero.dev/skills-codebase-design) |
| The code is broken and you need the bug found | [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) |
| The question needs external reading, not code reading | [research](https://aihero.dev/skills-research) |
| You want to learn a concept over multiple sessions | [teach](https://aihero.dev/skills-teach) |

## The method

The skill climbs four levels, and each crossing is declared:

1. **Concrete implementation.** Module boundary, semantic state versus representation state, ownership, effects, control flow, error paths. Ends with a behavioral summary of the significant operations as transformations.
2. **Invariants.** Representation, structural, semantic, typestate, cross-object, and temporal invariants, each classified by how it is enforced: type system, construction, runtime check, debug-only, caller discipline, convention, or not visibly enforced.
3. **Minimal abstract machine.** The smallest state machine that reproduces the behavior: state as a tuple, operations as transitions, reachability, and at least one trace through the real code.
4. **Formal semantics.** Abstract syntax, judgment forms, statics, and dynamics, chosen to fit the implementation rather than forced through a fixed template.

The analysis always closes with **model-versus-implementation**: the concrete states the formal model excludes. Temporary, half-initialized, or unreachable-but-representable states are where hidden assumptions and bugs live, so the gap is the finding, not a footnote.

## Common questions

**Isn't this overkill for a small function?**

Usually, yes, and the skill says so itself: prefer minimal abstractions, don't transcribe the implementation into notation. On a small function each level collapses to a sentence or two. The full ladder earns its keep on machinery with real state: interpreters, allocators, schedulers, protocol handlers.

**Does it run or modify the code?**

It is a reading discipline, not a driver. It may run the code to confirm a trace, but the output is an explanation; it never edits the implementation to make the model cleaner.

**How is this different from just asking the agent to explain the code?**

A plain explanation summarizes behavior in prose and quietly swaps implementation details for whatever abstraction reads well. This method makes those swaps explicit: three declared abstraction boundaries, invariants tied to their enforcement, and a final accounting of the states the implementation permits that the semantics excludes. That last gap is where the surprising findings are.

**Do I need programming-language theory to read the output?**

No. The formal layer is the last of four, and the skill forbids inventing judgments just to fill the template. The concrete analysis, invariants, and abstract machine stand on their own; the judgments and rules are there when you want precision.

## It's working if

- The explanation opens with the module boundary: what the code owns and what it delegates.
- Every claimed invariant names where it is established, checked, or assumed, and how it is enforced.
- There is at least one execution trace through the real source, with each transition naming the code that realizes it.
- The abstract machine is smaller than the implementation, and the list of what was erased to get there is stated out loud.
- Judgments are declared with their meaning before any rules use them.
- The write-up ends with the model-versus-implementation gap: states the representation allows that execution never produces, flagged as possible bugs, unsafe assumptions, or design complexity.

## Where it fits

`formal-semantics` is a **reach-for-it-anytime standalone**: it explains code and changes nothing, so it sits off the main idea-to-ship flow. Its closest neighbour is [codebase-design](https://aihero.dev/skills-codebase-design): once the explanation has exposed a module's real state and invariants, that is the vocabulary for judging whether the module is deep and whether the seam is in the right place. [research](https://aihero.dev/skills-research) is the other neighbour, for when the question needs external [primary sources](https://www.aihero.dev/ai-coding-dictionary/primary-source) rather than the code in front of you. When you're unsure which skill or flow fits, [ask-matt](https://aihero.dev/skills-ask-matt) routes you.
