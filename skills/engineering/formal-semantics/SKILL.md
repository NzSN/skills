---
name: formal-semantics
description: Explain source code by progressively reconstructing its formal semantics. Climbs four levels, from the concrete implementation, through its invariants and a minimal abstract machine, to PFPL-style syntax, judgments, statics, and dynamics, with every abstraction boundary declaring what it preserved and what it erased. Use when the user asks to explain, understand, or formalize how an implementation really works, especially parsers, lexers, type checkers, name resolvers, interpreters, compilers, IRs, optimizers, VMs, garbage collectors, object systems, module systems, concurrency runtimes, memory-management systems, standard libraries, or protocol state machines, or asks for invariants, an abstract machine, or operational semantics rather than a summary.
---

# Formal Semantics

## Purpose

Use this skill to explain source code by progressively reconstructing its semantics.

The method is applicable to implementations written in any programming language, including:

* C
* C++
* Rust
* Java
* Go
* Swift
* Kotlin
* OCaml
* Haskell
* JavaScript
* TypeScript
* Python
* compiler IRs
* bytecode interpreters
* virtual machines
* language runtimes

It is particularly useful when studying:

* parsers;
* lexers;
* type checkers;
* name resolvers;
* interpreters;
* compilers;
* intermediate representations;
* optimizers;
* virtual machines;
* garbage collectors;
* object systems;
* module systems;
* concurrency runtimes;
* memory-management systems;
* standard-library implementations;
* protocol/state-machine implementations.

The objective is not simply to summarize code.

The objective is to reconstruct:

$$
\boxed{
\text{Implementation}
\rightarrow
\text{Invariants}
\rightarrow
\text{Abstract Machine}
\rightarrow
\text{Formal Semantics}
}
$$

The concrete implementation remains the ground truth.

The formal model is a tool for understanding the implementation, not a replacement for it.

## 1. Core Principle

Analyze the program at four distinct levels:

$$
\text{Concrete Representation}
$$

$$
\downarrow
$$

$$
\text{Representation and Semantic Invariants}
$$

$$
\downarrow
$$

$$
\text{Abstract Machine}
$$

$$
\downarrow
$$

$$
\text{Formal Semantics}
$$

At every transition between levels, explicitly state what information has been preserved and what information has been erased.

Never silently replace implementation details with an abstraction.

## 2. Layer I: Concrete Implementation

Begin with the actual source code.

Do not begin with a mathematical model.

Determine what the implementation really represents and how it behaves.

### 2.1 Identify the Module Boundary

Determine:

* files involved;
* major data types;
* classes, structs, records, enums, traits, interfaces, or modules;
* exported/public operations;
* internal/private operations;
* callers;
* callees;
* external dependencies.

State the responsibility of the module.

For example:

```text
This module performs lexical analysis.

This module resolves identifiers to bindings.

This module transforms IR from representation A to representation B.

This module implements a garbage-collector worklist.

This module evaluates bytecode instructions.
```

Separate:

$$
\text{what the module owns}
$$

from:

$$
\text{what it delegates}.
$$

## 3. Concrete State

Identify all semantically relevant state.

For every important object or data structure determine:

* fields;
* field types;
* initialization;
* mutation;
* valid values;
* sentinel values;
* optional states;
* cached state;
* derived state;
* synchronization state;
* ownership relationships.

Distinguish between:

$$
\text{semantic state}
$$

and

$$
\text{representation state}.
$$

For example, an implementation may maintain:

```text
cached_hash
```

even though the abstract object only represents:

$$
String(content).
$$

The cache belongs to the implementation but may disappear from the semantic model.

## 4. Ownership, Aliasing, and Lifetime

Determine how objects relate to one another.

Depending on the implementation language, inspect:

* value ownership;
* borrowing;
* references;
* pointers;
* garbage-collected references;
* reference counting;
* arena allocation;
* region allocation;
* shared ownership;
* immutable sharing;
* mutable aliasing.

Useful abstract relations include:

$$
A \owns B
$$

$$
A \borrows B
$$

$$
A \aliases B
$$

and:

$$
lifetime(B) \subseteq lifetime(A).
$$

Do not infer these relationships solely from syntax.

Use constructors, allocation sites, APIs, destruction behavior, type-system guarantees, comments, and call structure.

## 5. Mutation and Effects

Treat important functions as state transformers.

A pure operation may be modeled as:

$$
f : A \rightarrow B
$$

while a stateful operation may be:

$$
f :
\Sigma
\rightarrow
B \times \Sigma'.
$$

Identify effects such as:

* mutation;
* allocation;
* deallocation;
* I/O;
* exceptions;
* diagnostics;
* logging;
* synchronization;
* blocking;
* thread-local mutation;
* global-state modification;
* cache modification;
* environment modification;
* continuation changes;
* control transfer.

Distinguish:

$$
\text{semantic effects}
$$

from:

$$
\text{implementation effects}.
$$

For example, memoization may mutate memory without changing the logical meaning of the computation.

## 6. Control Flow

Explain the significant control-flow structure.

Identify:

* entry points;
* loops;
* recursive calls;
* dispatch;
* callbacks;
* continuations;
* exception paths;
* early exits;
* state-dependent branches;
* indirect calls;
* asynchronous transitions.

When useful, express control flow as a transition relation:

$$
s \rightarrow s'.
$$

Avoid merely paraphrasing functions line by line.

Instead identify the state transformation performed by each important path.

## 7. Invariants

Before formalizing behavior, reconstruct the invariants assumed by the implementation.

Classify them.

### Representation invariants

Examples:

$$
0 \le i < length
$$

$$
ptr \neq null
$$

$$
capacity \ge size.
$$

### Structural invariants

Examples:

$$
parent(child)=node
$$

or:

$$
graph\ is\ acyclic.
$$

### Semantic invariants

Examples:

$$
Resolved(x)
\implies
binding(x)\neq None.
$$

### Typestate invariants

Example:

$$
Created
\rightarrow
Initialized
\rightarrow
Running
\rightarrow
Finished.
$$

### Cross-object invariants

Example:

$$
x.owner = o
\implies
x \in members(o).
$$

### Temporal invariants

Example:

$$
Initialize
\prec
Execute
\prec
Destroy.
$$

For each important invariant determine:

* where it is established;
* where it is checked;
* where it is assumed;
* which operations preserve it;
* whether violating it is representable.

## 8. Preconditions and Postconditions

For important functions infer:

$$
Pre(f)
$$

and:

$$
Post(f).
$$

Express the intended contract:

$$
Pre(f,\sigma)
\land
f(\sigma)=\sigma'
\implies
Post(f,\sigma').
$$

Also determine whether these conditions are:

* enforced by the type system;
* runtime checked;
* asserted only in debug builds;
* documented;
* implicit;
* enforced only by callers.

This distinction is crucial.

## 9. Error and Exceptional Behavior

Do not model only the successful path.

Identify:

* invalid inputs;
* parsing failures;
* type errors;
* null/missing values;
* exceptions;
* panics;
* error values;
* sentinel values;
* retries;
* recovery states;
* timeout behavior;
* partial results;
* undefined behavior assumptions;
* fatal errors.

A function that conceptually looks like:

$$
f : A \rightarrow B
$$

may actually be better modeled as:

$$
f : A \rightarrow B + Error.
$$

Or, if state is involved:

$$
f :
\Sigma
\rightarrow
(B+\text{Error})\times\Sigma'.
$$

## 10. Concurrency When Relevant

If the module is concurrent, determine:

* threads or tasks involved;
* shared mutable state;
* atomic operations;
* synchronization;
* lock ordering;
* happens-before relationships;
* ownership transfer;
* data races prevented by design;
* message-passing behavior.

Possible relations include:

$$
a \prec_{hb} b
$$

for happens-before.

Do not remove concurrency from the model if concurrency affects observable semantics.

## 11. Concrete Behavioral Summary

After examining the implementation, summarize the significant operations as transformations.

For example:

$$
parse :
TokenStream
\rightarrow
AST + ParseError
$$

$$
resolve :
Environment \times Name
\rightarrow
Binding + Unresolved
$$

$$
step :
VMState
\rightarrow
VMState
$$

$$
infer :
Context \times Expression
\rightarrow
Type + TypeError.
$$

These descriptions must be derived from the code rather than imposed beforehand.

## 12. Abstraction Boundary I

Before building the abstract machine, explicitly list what will be retained.

Example:

```text
Preserved:
- logical program state
- scope nesting
- binding identities
- instruction position
- error state
```

Then list what will be removed.

Example:

```text
Erased:
- concrete object layout
- source-language helper methods
- memory addresses
- cache fields
- tracing infrastructure
- performance counters
- inline optimization details
```

Every abstraction must declare its losses.

## 13. Layer II: Minimal Abstract Machine

Construct the smallest state machine capable of reproducing the behavior under investigation.

Represent machine state as:

$$
\Sigma =
\langle
s_1,\ldots,s_n
\rangle.
$$

For an interpreter:

$$
\Sigma =
\langle
e,\rho,\mu,k
\rangle
$$

where:

* \(e\) is the current expression;
* \(\rho\) is the environment;
* \(\mu\) is the store;
* \(k\) is the continuation.

For a parser:

$$
\Sigma =
\langle
tokens,pos,stack,result,error
\rangle.
$$

For a VM:

$$
\Sigma =
\langle
pc,stack,locals,heap
\rangle.
$$

For a type checker:

$$
\Sigma =
\langle
\Gamma,constraints,worklist
\rangle.
$$

The precise representation must be derived from the implementation.

## 14. Do Not Copy the Implementation Structure

The abstract machine is not a mathematical transcription of object fields.

Several implementation fields may correspond to one semantic component.

Conversely, one implementation field may encode several semantic concepts.

For example:

```text
implementation:
    state_flags: uint32
```

may semantically represent:

$$
State =
Parsed
+
Resolved
+
Compiled.
$$

Prefer semantic structure over storage structure.

## 15. Algebraic Representation of States

Use algebraic data types when they make illegal states unrepresentable.

Instead of:

$$
initialized : Bool
$$

$$
result : Option(Result)
$$

use:

$$
State ::=
Uninitialized
\mid
Initialized
\mid
Completed(Result).
$$

This often reveals implementation states that exist only because the representation is more permissive than the semantics.

## 16. Abstract Operations

Define the principal operations of the machine.

For example:

$$
step :
\Sigma \rightarrow \Sigma
$$

$$
lookup :
Environment \times Name
\rightarrow Binding + Failure
$$

$$
allocate :
Store \times Value
\rightarrow Location \times Store
$$

$$
unify :
Constraints
\rightarrow
Constraints + TypeError.
$$

An abstract operation may correspond to:

* one implementation function;
* several functions;
* a loop;
* a dispatch chain;
* a distributed protocol across modules.

Do not assume a one-to-one mapping.

## 17. Reachability

Determine which states are actually reachable.

Let:

$$
States
$$

denote representable states and:

$$
Reachable \subseteq States.
$$

The distinction matters because implementation representations often admit states that valid execution never creates.

Identify:

* initial states;
* intermediate states;
* terminal states;
* error states;
* unreachable states.

## 18. Transition System

Describe execution using transitions:

$$
\Sigma
\rightarrow
\Sigma'.
$$

For named operations use:

$$
\Sigma
\xrightarrow{op}
\Sigma'.
$$

If actions produce observable effects:

$$
\Sigma
\xrightarrow{\alpha}
\Sigma'
$$

where \(\alpha\) may be an output, event, allocation, exception, or message.

## 19. Example Trace

Provide at least one meaningful trace:

$$
\Sigma_0
\rightarrow
\Sigma_1
\rightarrow
\Sigma_2
\rightarrow
\cdots
\rightarrow
\Sigma_n.
$$

For each important transition, indicate which implementation code realizes it.

The trace serves as the bridge between source code and formal semantics.

## 20. Abstraction Boundary II

State what the abstract machine removed.

Possible erased details:

* source-level helper functions;
* pointer identities;
* object layout;
* allocation strategy;
* implementation-language type machinery;
* concrete collection representations;
* caches;
* debugging infrastructure;
* performance optimization.

Also state what remains observable in the model.

## 21. Layer III: Formal Semantics

Formalize the abstract machine using programming-language semantics.

The preferred organization is:

$$
\boxed{
\text{Syntax}
+
\text{Judgments}
+
\text{Statics}
+
\text{Dynamics}
}
$$

This follows the style used in PFPL and related programming-language literature.

Not every subsystem requires all four parts.

Do not invent meaningless typing or static judgments merely to fill the template.

## 22. Abstract Syntax

Define relevant syntactic classes.

For example:

$$
Exp\ e ::=
x
\mid
n
\mid
e_1+e_2
\mid
let(x,e_1,e_2)
$$

or:

$$
Instr\ i ::=
load(x)
\mid
store(x)
\mid
add
\mid
jump(l).
$$

State metavariable conventions explicitly:

$$
x \in Var
$$

$$
e \in Exp
$$

$$
\tau \in Type.
$$

## 23. Binding Structure

If the implementation manipulates programming-language syntax, explicitly describe binding.

For example:

$$
\lambda x.e
$$

introduces the binding \(x\) whose scope is \(e\).

Distinguish:

* binder;
* binding occurrence;
* bound occurrence;
* free occurrence;
* scope;
* shadowing;
* alpha-equivalence;
* substitution.

Do not identify variables merely by their textual spelling when binding identity matters.

## 24. Judgment Forms

Declare judgments before defining rules.

Examples include:

### Typing

$$
\Gamma \vdash e : \tau
$$

meaning:

> Under context \(\Gamma\), expression \(e\) has type \(\tau\).

### Well-formedness

$$
\Gamma \vdash e\ ok
$$

### Name resolution

$$
\Gamma \vdash x \Downarrow b
$$

### Evaluation

$$
e \Downarrow v
$$

### Small-step transition

$$
e \rightarrow e'
$$

### Machine transition

$$
\Sigma \rightarrow \Sigma'
$$

### Subtyping

$$
\tau_1 <: \tau_2
$$

### Constraint satisfaction

$$
C \models \phi.
$$

Explain the intended meaning of every judgment.

## 25. Statics

Describe rules governing valid programs or states.

These may include:

* typing;
* well-formedness;
* declaration rules;
* scope rules;
* capability requirements;
* effect restrictions;
* ownership constraints;
* protocol legality.

Example:

$$
\frac{
\Gamma(x)=\tau
}{
\Gamma \vdash x:\tau
}
$$

or:

$$
\frac{
\Gamma\vdash e_1:\tau_1
\qquad
\Gamma,x:\tau_1\vdash e_2:\tau_2
}{
\Gamma\vdash let(x,e_1,e_2):\tau_2
}
$$

Translate implementation invariants into static judgments only when the relationship is meaningful.

## 26. Dynamics

Represent runtime behavior with operational semantics.

### Small-step semantics

Use:

$$
e \rightarrow e'
$$

when intermediate computational states matter.

Example:

$$
\frac{
e_1\rightarrow e_1'
}{
e_1+e_2
\rightarrow
e_1'+e_2
}
$$

### Big-step semantics

Use:

$$
e\Downarrow v
$$

when only the final result matters.

### Machine semantics

Use:

$$
\langle control,state\rangle
\rightarrow
\langle control',state'\rangle
$$

for interpreters, VMs, protocols, and stateful systems.

Choose the semantic style that best corresponds to the implementation.

## 27. Evaluation Contexts When Useful

If the implementation has deterministic evaluation order, consider evaluation contexts.

Example:

$$
E ::= [\,]
\mid E+e
\mid v+E.
$$

Then:

$$
e\rightarrow e'
\implies
E[e]\rightarrow E[e'].
$$

This can greatly simplify formalization of evaluators and interpreters.

## 28. Store and Environment Semantics

When the implementation manipulates mutable state, distinguish environments from stores.

Use:

$$
\rho : Var \rightharpoonup Location
$$

for environments and:

$$
\mu : Location \rightharpoonup Value
$$

for memory/store.

Then configurations may take the form:

$$
\langle e,\rho,\mu\rangle.
$$

Do not collapse name binding and storage unless the implementation semantics justify doing so.

## 29. Error Semantics

Represent errors explicitly.

For example:

$$
Result ::= Value(v) \mid Error(e).
$$

Or:

$$
\Sigma
\xrightarrow{error(e)}
Error(e).
$$

If execution recovers, model recovery rather than treating errors as terminal.

## 30. Nondeterminism

If the implementation permits multiple legal transitions, use:

$$
\Sigma \rightarrow \Sigma_1
$$

and:

$$
\Sigma \rightarrow \Sigma_2.
$$

Do not falsely impose determinism.

This is especially relevant to:

* concurrency;
* scheduling;
* garbage collection;
* search procedures;
* distributed systems;
* specification-level semantics.

## 31. Correspondence With Implementation

Map formal constructs back to source code.

For example:

| Formal concept        | Abstract operation | Implementation                |
| --------------------- | ------------------ | ----------------------------- |
| environment lookup    | `lookup`           | map lookup + parent traversal |
| small-step transition | `step`             | evaluator dispatch            |
| allocation            | `alloc`            | allocator routine             |
| type judgment         | `check`            | type-checker visitor          |

Distinguish:

$$
\text{exact implementation correspondence}
$$

from:

$$
\text{conceptual correspondence}.
$$

Say explicitly when several implementation operations jointly realize one formal rule.

## 32. Abstraction Boundary III

After formalization, state exactly what has disappeared.

For example:

```text
Erased by the formal semantics:

- source-language implementation types
- physical object layout
- cache state
- logging
- profiling
- allocator internals
- helper-function decomposition
- debug assertions
- concrete instruction encodings
```

Also list assumptions introduced by the model.

For example:

```text
The model assumes lookup is deterministic.

The implementation supports lazy initialization,
which the formal system collapses into an atomic transition.
```

## 33. Model-versus-Implementation Analysis

This is a required part of the explanation.

Compare:

$$
ConcreteStates
$$

with:

$$
AbstractStates.
$$

Ask whether:

$$
AbstractStates
\subset
ConcreteStates.
$$

If so, investigate the concrete states excluded from the abstract model.

They may represent:

* temporary states;
* optimization states;
* error states;
* partially initialized objects;
* invalid representations;
* bugs.

## 34. Invariant Preservation

For every important operation \(op\), consider:

$$
Invariant(\sigma)
\land
Precondition(op,\sigma)
\implies
Invariant(op(\sigma)).
$$

If this cannot be established from the implementation, explain why.

Determine whether preservation depends upon:

* caller discipline;
* runtime checks;
* static typing;
* ownership;
* synchronization;
* hidden global state.

## 35. Representation Versus Semantic Type

Do not confuse implementation representation with semantic type.

For example:

$$
\Gamma \vdash v : \tau
$$

states a semantic property.

An implementation may encode this using:

* runtime tags;
* enums;
* object headers;
* vtables;
* union discriminants;
* type IDs;
* pattern-matching variants;
* generics;
* pointer metadata.

Always ask separately:

$$
representation(v)
\models
semantic\_type(v)?
$$

This principle applies across implementation languages.

## 36. Static Versus Dynamic Enforcement

Classify each important invariant according to how it is enforced.

Use categories such as:

```text
Type-system enforced
Construction enforced
Runtime checked
Debug-only checked
Caller enforced
Convention enforced
Not visibly enforced
```

This classification is often more informative than the invariant alone.

## 37. Language-Specific Representation Details

Adapt the implementation analysis to the language being studied.

### C / C++

Inspect:

* pointers;
* aliasing;
* unions;
* casts;
* object lifetime;
* RAII;
* undefined behavior;
* manual allocation;
* templates;
* virtual dispatch.

### Rust

Inspect:

* ownership;
* borrowing;
* lifetimes;
* interior mutability;
* `unsafe`;
* `Rc`;
* `Arc`;
* `RefCell`;
* `Cell`;
* pinning;
* trait-object dispatch.

### Java / Kotlin

Inspect:

* object references;
* nullability;
* inheritance;
* interfaces;
* garbage collection;
* exceptions;
* synchronization;
* class initialization.

### Go

Inspect:

* interfaces;
* slices;
* maps;
* pointers;
* goroutines;
* channels;
* escape behavior;
* synchronization.

### OCaml / Haskell

Inspect:

* algebraic data types;
* pattern matching;
* closures;
* laziness;
* monadic effects;
* mutable references;
* persistent structures.

### JavaScript / TypeScript

Inspect:

* objects;
* prototypes;
* closures;
* promises;
* dynamic property lookup;
* coercions;
* event-loop behavior;
* TypeScript's static model versus JavaScript runtime behavior.

These are implementation concerns, not changes to the semantic methodology.

## 38. Proof-Oriented Questions

Where appropriate, ask whether the implementation appears to satisfy properties resembling standard metatheoretic results.

Examples:

### Progress-like question

Can every valid nonterminal state make progress?

$$
Valid(\sigma)
\land
\neg Terminal(\sigma)
\implies
\exists\sigma'.\;
\sigma\rightarrow\sigma'
$$

### Preservation-like question

Does execution preserve validity?

$$
Valid(\sigma)
\land
\sigma\rightarrow\sigma'
\implies
Valid(\sigma').
$$

### Determinism

$$
\sigma\rightarrow\sigma_1
\land
\sigma\rightarrow\sigma_2
\implies
\sigma_1=\sigma_2.
$$

Do not claim these properties as theorems unless they have actually been established.

Use them as analytical questions.

## 39. Required Output Structure

Produce analyses in this order.

### 1. Purpose and module boundary

Explain what the code is responsible for.

### 2. Concrete implementation

Describe:

* data structures;
* functions;
* ownership;
* mutation;
* effects;
* control flow;
* error handling;
* dependencies.

### 3. Concrete invariants

Identify representation, state, structural, and temporal invariants.

### 4. Representative execution

Trace important behavior through the real source code.

### 5. First abstraction boundary

State what will be preserved and erased.

### 6. Minimal abstract machine

Define:

$$
\Sigma.
$$

Explain every state component.

### 7. Abstract operations

Define significant state transformations.

### 8. Reachability and invariants

Identify legal, illegal, initial, terminal, and error states.

### 9. Abstract execution trace

Show at least one meaningful transition sequence.

### 10. Second abstraction boundary

State what has been erased.

### 11. Abstract syntax

Define relevant syntactic categories.

### 12. Binding structure

Explain bindings and scopes when applicable.

### 13. Judgment forms

Define each judgment and its meaning.

### 14. Statics

Formalize well-formedness, typing, scope, or legality when applicable.

### 15. Dynamics

Formalize execution using small-step, big-step, machine, or labeled-transition semantics.

### 16. Error behavior

Formalize relevant errors and recovery.

### 17. Implementation correspondence

Map formal rules back to concrete code.

### 18. Final abstraction boundary

State what the formal model ignores.

### 19. Model-versus-implementation analysis

Analyze:

* excess representational states;
* implicit invariants;
* invalid states;
* abstraction mismatches;
* hidden assumptions;
* possible implementation defects.

## 40. Rules for the Analyzer

### Treat source code as authoritative

Never modify the interpretation merely to produce cleaner mathematics.

### Separate observation from modeling

Always distinguish statements of the form:

```text
The implementation stores X.
```

from:

```text
We model X as Y.
```

### Do not invent invariants

Every claimed implementation invariant should have observable justification.

### Prefer minimal abstractions

Do not reproduce the complete implementation in mathematical notation.

### Preserve uncertainty

Use formulations such as:

```text
The code appears to require this invariant.

This property is enforced by callers rather than locally.

This state seems unreachable, but the representation permits it.
```

when evidence is incomplete.

### Formalize behavior, not syntax alone

A useful formal model should explain:

$$
\text{what states exist}
$$

$$
\text{what operations are allowed}
$$

and:

$$
\text{how states evolve}.
$$

### Keep abstraction losses explicit

Every model should answer:

> What did we intentionally forget?

## 41. Desired Outcome

A successful analysis lets the reader move in both directions:

$$
\text{source code}
\Rightarrow
\text{semantic model}
$$

and:

$$
\text{semantic property}
\Rightarrow
\text{implementation mechanism}.
$$

At the end, the reader should be able to answer:

* What does this code represent?
* What is its state?
* Which states are legal?
* Which states are reachable?
* What operations transform the state?
* What effects occur?
* What invariants must hold?
* How are those invariants enforced?
* What are the failure states?
* What implementation details are semantically irrelevant?
* What is the smallest abstract machine explaining the behavior?
* How can that machine be expressed using formal judgments and operational semantics?
* Where does the implementation permit more states than the semantic model?
* Where might those gaps indicate bugs, unsafe assumptions, or design complexity?

The purpose of the formalization is not mathematical decoration.

Its purpose is to expose the semantic structure already implicit in the program.
