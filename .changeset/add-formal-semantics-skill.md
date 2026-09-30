---
"mattpocock-skills": patch
---

Add the `formal-semantics` skill (engineering bucket, model-invoked). It explains source code by progressively reconstructing its semantics across four levels: the concrete implementation, the invariants the code depends on (each classified by how it is enforced), a minimal abstract machine with explicit state and transitions, and a PFPL-style formal semantics of syntax, judgments, statics, and dynamics. Every move between levels is an explicit abstraction boundary that declares what was preserved and what was erased, and the analysis closes with a model-versus-implementation gap check, where the states the representation permits but execution never reaches are where bugs and hidden assumptions surface. Ships with the docs page, both README entries, the plugin manifest entry, and the `ask-matt` router update a promoted skill requires.
