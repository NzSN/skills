---
name: implementation-to-formal-semantics
description: Explain source code by reconstructing its invariants, minimal abstract machine, and formal semantics. Use when the user wants a source-grounded semantic analysis of an implementation, operational rules, or a comparison of representable and semantically valid states.
---

# Implementation-to-Formal-Semantics Code Explanation

Reconstruct the semantic structure implicit in an implementation:

$$
\text{Implementation} \rightarrow \text{Invariants}
\rightarrow \text{Abstract Machine} \rightarrow \text{Formal Semantics}.
$$

The concrete implementation is the ground truth. Begin with source, derive the model from it, and explicitly state what is preserved and erased at every transition. Distinguish observations ("the implementation stores X") from modeling choices ("we model X as Y"). The model supports understanding; it does not replace the implementation.

Apply this method across implementation languages, compiler IRs, bytecode, and runtimes. It fits parsers, lexers, resolvers, type checkers, interpreters, compilers, optimizers, VMs, collectors, object and module systems, concurrency and memory-management systems, standard libraries, and protocols.

## 1. Inspect the concrete implementation

Identify the requested code and behavior under investigation. Follow relevant callers, callees, constructors, allocation sites, and dependencies until the module boundary and important contracts are supported by source evidence. If the source or target is missing, request it before inventing behavior. Cite files, symbols, and line locations for consequential claims and transitions. Distinguish source inspection from behavior actually executed.

Complete this analysis before constructing the abstract machine:

- **Boundary:** files, major types, public and private operations, callers, callees, dependencies, responsibility, and what the module owns versus delegates.
- **State:** fields and types, initialization and mutation, valid and sentinel values, optional states, caches, derived state, synchronization state, and ownership relationships. Separate semantic state from representation state, such as a string's content versus its cached hash.
- **Ownership, aliasing, lifetime:** values, borrows, references, pointers, GC references, reference counting, arenas, regions, shared ownership, immutable sharing, and mutable aliasing as relevant. Establish relationships through allocation, constructors, APIs, destruction, type guarantees, and call structure, not syntax alone. Define notation such as `owns(A, B)`, `borrows(A, B)`, `aliases(A, B)`, and lifetime containment before using it.
- **Effects:** mutation, allocation/deallocation, I/O, exceptions, diagnostics, logging, synchronization, blocking, local/global/environment/cache changes, continuations, and control transfer. Distinguish semantic effects from implementation effects. A memoization write may leave logical meaning unchanged.
- **Control flow:** entry points, loops, recursion, dispatch, callbacks, continuations, early exits, exceptional paths, state-dependent branches, indirect calls, and asynchronous transitions. Explain state transformations instead of paraphrasing every line.
- **Failure:** invalid input, missing values, errors, exceptions, panics, sentinels, retries, recovery, timeouts, partial results, fatal errors, and undefined-behavior assumptions. Account for state left behind on failure.
- **Concurrency, when relevant:** threads/tasks, shared state, atomics, locks and lock ordering, happens-before, ownership transfer, race prevention, and messages. Preserve concurrency whenever it changes observable behavior.

Adapt the inspection to the language:

| Implementation | Representation concerns |
| --- | --- |
| C / C++ | Pointers, aliasing, unions, casts, lifetime, RAII, undefined behavior, manual allocation, templates, virtual dispatch |
| Rust | Ownership, borrowing, lifetimes, interior mutability, unsafe code, Rc/Arc, RefCell/Cell, pinning, trait objects |
| Java / Kotlin | References, nullability, inheritance, interfaces, GC, exceptions, synchronization, class initialization |
| Go | Interfaces, slices, maps, pointers, goroutines, channels, escape behavior, synchronization |
| OCaml / Haskell | Algebraic types, matching, closures, laziness, monadic effects, mutable references, persistent structures |
| JavaScript / TypeScript | Objects, prototypes, closures, promises, dynamic lookup, coercions, event loop, static types versus runtime behavior |
| Swift, other languages, IRs, bytecode | Corresponding ownership, representation, dispatch, memory, and execution mechanisms visible in the source |

## 2. Reconstruct invariants and contracts

Classify important invariants as representation, structural, semantic, typestate, cross-object, or temporal. Examples include bounds, capacity versus size, parent-child consistency, resolved binding identity, initialization phases, membership consistency, and initialize-before-execute-before-destroy ordering.

For each invariant record:

- Where it is established, checked, and assumed.
- Which operations preserve it and why.
- Whether violations are representable and whether they appear reachable.
- Enforcement: **Type-system enforced**, **Construction enforced**, **Runtime checked**, **Debug-only checked**, **Caller enforced**, **Convention enforced**, or **Not visibly enforced**.

Infer important preconditions and postconditions, including exceptional outcomes and partial mutation. For a successful state transformation, express the intended contract as:

$$
Pre(f,\sigma) \land f(\sigma)=\sigma' \implies Post(f,\sigma').
$$

Separate a documented or inferred requirement from an established guarantee. Say when an invariant appears required, depends on callers, or cannot be established from available code. Do not invent implementation invariants to simplify the model.

Summarize concrete behavior with derived signatures. Pure operations may have type $A \to B$; stateful operations may have type $A \times \Sigma \to (B + Error) \times \Sigma$. Use a relation when nondeterminism, divergence, blocking, or multiple outcomes make a total function misleading.

Trace representative behavior through the real source, including an important failure or recovery path when applicable.

## 3. Construct the minimal abstract machine

Declare the **first abstraction boundary**: list preserved information and erased information before introducing the machine. Justify losses relative to the behavior under investigation. Layout, addresses, caches, logging, counters, and optimizations may disappear only when their effects are irrelevant to that scope.

Define the smallest state capable of reproducing that behavior:

$$
\Sigma = \langle s_1,\ldots,s_n\rangle.
$$

Explain each component. Possible starting shapes, to adapt only after inspecting source:

| Subsystem | Possible components |
| --- | --- |
| Interpreter | expression, environment, store, continuation |
| Parser | tokens, position, stack, result, error |
| VM | program counter, stack, locals, heap |
| Type checker | context, constraints, worklist |

Use semantic structure rather than copying object fields. Several fields may implement one component; one flags field may encode several concepts. Algebraic states such as `Uninitialized | Initialized | Completed(Result)` can exclude impossible combinations, but retain and explain any concrete states thereby excluded.

Define principal abstract operations and labeled transitions:

$$
\Sigma \xrightarrow{op\,/\,\alpha} \Sigma'.
$$

Define labels and observables, including relevant outputs, messages, allocation, and exceptions. An operation may correspond to one function, several functions, a loop, dispatch, or a protocol across modules.

Identify initial, intermediate, terminal, error, invalid, and unreachable states. Distinguish representability from reachability: $Reachable \subseteq States$. Give at least one meaningful trace $\Sigma_0 \to \cdots \to \Sigma_n$, mapping important transitions to the implementation and connecting it to the concrete trace.

At the **second abstraction boundary**, inventory what the machine has erased, what remains observable, and what additional simplification the formal semantics will introduce.

## 4. Express formal semantics

Organize the formalization as **Syntax + Judgments + Statics + Dynamics**, in the style of PFPL and related programming-language semantics. Include only meaningful categories and rules. For an inapplicable part, state why it is inapplicable instead of fabricating typing or syntax.

- **Syntax:** define relevant syntactic classes and metavariables, for example $x \in Var$, $e \in Exp$, and $\tau \in Type$.
- **Binding:** when syntax binds names, identify binders, binding occurrences, bound/free occurrences, scope, shadowing, alpha-equivalence, and substitution as relevant. Preserve binding identity rather than equating names by spelling.
- **Judgments:** declare each form and its meaning before rules, for example typing $\Gamma \vdash e:\tau$, well-formedness, resolution, evaluation $e\Downarrow v$, transition $\Sigma\to\Sigma'$, subtyping, or constraint satisfaction.
- **Statics:** express meaningful typing, scope, declaration, well-formedness, capability, effect, ownership, or protocol-legality rules. Translate invariants into static judgments only where justified.
- **Dynamics:** choose small-step when intermediate computation matters, big-step when final results suffice, or machine/labeled transitions for stateful systems. State evaluation order; evaluation contexts can factor deterministic order when useful. Keep divergence or blocking distinctions if observable.
- **Environment and store:** distinguish binding from mutable storage when needed, for example $\rho:Var\rightharpoonup Location$ and $\mu:Location\rightharpoonup Value$. Collapse them only with justification.
- **Errors:** formalize outcomes such as `Value(v) | Error(e)`, exceptional transitions, state on failure, and recovery. Recoverable errors need recovery rules, not an invented terminal state.
- **Nondeterminism:** allow multiple legal successors when scheduling, GC, search, or protocols permit them. Do not impose determinism for convenience.

Map formal concepts and rules to abstract operations and concrete files/symbols in a correspondence table. Label exact correspondence versus conceptual correspondence, and identify rules jointly realized by multiple implementation operations.

At the **final abstraction boundary**, explicitly list remaining losses and introduced assumptions, such as collapsing lazy initialization into an atomic transition. Explain why each assumption is acceptable or what it leaves unmodeled.

## 5. Compare model and implementation

This comparison is required. Concrete and abstract state spaces usually contain different kinds of objects, so define an abstraction map $\alpha:C\rightharpoonup A$ or a correspondence relation $R\subseteq C\times A$ before comparing them. Use a literal subset comparison only if both spaces share a justified common representation.

Investigate concrete states excluded, merged, or left unmapped: temporary states, optimization states, errors, partial initialization, invalid representations, and potential defects. Distinguish representable states from reachable ones and model assumptions from source-established facts. Check whether concrete transitions correspond to abstract steps, multiple steps, or unobservable stuttering.

For important operations, examine preservation:

$$
Invariant(\sigma) \land Pre(op,\sigma)
\implies Invariant(op(\sigma)).
$$

Adapt this formula to each outcome or relational successor where necessary. Explain dependence on caller discipline, checks, typing, ownership, synchronization, or hidden global state, and identify missing evidence.

Keep representation and semantic type separate: a runtime tag, enum, header, vtable, union discriminant, type ID, generic, or pointer metadata implements a semantic property only under the relevant invariants.

Where appropriate, investigate progress (every valid nonterminal state has a successor), preservation (steps maintain validity), and determinism (successors agree). Account for external inputs and scheduling assumptions. Treat these as analytical questions; claim a theorem only with an actual proof. Report possible defects as hypotheses with evidence, not as confirmed bugs merely because the abstraction excludes a state.

## Required output order

Use these sections in order. Keep inapplicable sections brief and explain why they do not apply.

1. **Purpose and module boundary**
2. **Concrete implementation**: structures, functions, ownership, mutation, effects, control flow, errors, dependencies
3. **Concrete invariants**: classified invariants, contracts, evidence, enforcement
4. **Representative execution**: trace through source
5. **First abstraction boundary**: preserved and erased information
6. **Minimal abstract machine**: state and every component
7. **Abstract operations**: significant transformations
8. **Reachability and invariants**: legal, illegal, initial, terminal, error states
9. **Abstract execution trace**: transitions tied to source
10. **Second abstraction boundary**
11. **Abstract syntax**
12. **Binding structure**
13. **Judgment forms**
14. **Statics**
15. **Dynamics**
16. **Error behavior**
17. **Implementation correspondence**
18. **Final abstraction boundary**
19. **Model-versus-implementation analysis**: excess representations, implicit invariants, invalid states, mismatches, assumptions, preservation, possible defects

The explanation is complete when the reader can move from source to semantic model and back from a semantic property to its implementation mechanism, with evidence and explicit abstraction losses in both directions.
