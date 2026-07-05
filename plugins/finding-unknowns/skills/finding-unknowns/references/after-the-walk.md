# After the Walk

The map lives on past planning. Four moves for the phases that follow.

- **Implementation notes** (during the build) — keep a running log; every
  time the code forces a deviation from the plan, record what the plan said,
  what the code revealed, and the conservative call made, then keep going.
  Tag entries that need the user's judgment. Each deviation is an unknown
  unknown that escaped the walk — fold it back into the map for attempt #2.
- **The buy-in doc** (before shipping) — other people inherit your unknowns;
  package prototype, spec, and notes into one skimmable pitch that leads with
  a demo, pre-answers each reviewer's objections with evidence, and names who
  signs off on what.
- **Quiz before merge** (before merging someone else's or a long diff) — a
  merge-readiness report — mental model, non-obvious behaviors introduced,
  what to watch after deploy — ending in a quiz the user must pass; wrong
  answers point back to the section they skimmed.
- **The handoff** (at a session boundary) — when the work outlives this
  context, write the map's successor for a fresh agent. State, not
  instructions: "X is implemented; Y is not started" — the next agent decides
  actions. Every decision with its why and the approaches rejected; the traps
  and dead ends already stepped on (the least recoverable knowledge there
  is); pointers to artifacts, never re-embedded copies that go stale. Frame
  everything as claims for the next agent to verify against the territory,
  not facts to trust.
