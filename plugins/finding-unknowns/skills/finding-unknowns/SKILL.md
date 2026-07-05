---
name: finding-unknowns
description: Guide the user through a quadrant walk that maps the unknowns of a task — open by listing the known knowns, then work through known unknowns, unknown knowns, and unknown unknowns one stage at a time, ending with a complete four-quadrant map in the user's hands. Use when the user explicitly asks for a blindspot pass, unknown unknowns, "what am I missing / what should I be asking", a one-question-at-a-time interview, or several directions to react to; when ambiguity or unfamiliarity is high enough that building now would likely cause rework; when a reference implementation must be understood before porting; or for a named after-walk slice — implementation notes / deviations log, a buy-in doc, a quiz gate before merge, or a session handoff (run only that slice). Do not invoke for ordinary implementation of a sufficiently specified task.
---

<!-- Based on explore-unknowns from dzhng/skills (MIT, Copyright (c) David Zhang),
     itself codifying Thariq Shihipar's "A Field Guide to Fable: Finding Your Unknowns".
     Extended with patterns from Addy Osmani's agent-skills and davidondrej/skills. -->

# Finding Unknowns

The map is not the territory. The prompt, the plan, and the context window are
the map; the codebase, the domain, and the user's actual intent are the
territory. The gap between them is the unknowns — and an unknown found before
code is written costs minutes, while the same unknown found three PRs later
costs the three PRs.

This skill is a guided conversation: the **quadrant walk**. Together with the
user you fill in a four-quadrant map of the task, one quadrant per stage, and
the user walks away holding the completed map. The map is the deliverable;
implementation is a different task that starts only after the map is handed
over.

Two moves apply at every stage:

- **Reacting beats imagining — for tacit unknowns.** When the unknown is
  taste, shape, vocabulary, or "I'll know it when I see it", never ask the
  user to describe what they want when you can hand them something concrete
  to react to — a rendered option, a clickable mock, a decisions table.
  Reacting extracts knowledge the user has but cannot articulate unprompted.
  When the unknown is a factual constraint or an architectural decision, ask
  the highest-blast-radius question directly, with a recommendation.
- **Every artifact assembles the reply.** End each artifact with the user's
  next message pre-drafted: steal/skip chips, resonate checkboxes, a
  decisions table, a copyable sharpened prompt — so their reaction becomes
  their next message with near-zero typing.

## The Quadrant Walk

Five stages, walked in order, one at a time. **When you enter a stage, read
its reference file and follow it.** Name the current quadrant as you go — the
user should always know where they stand on the map — and finish the stage in
front of you before opening the next.

1. **[Known knowns](references/stage-1-known-knowns.md)** — scan the
   territory, then open with the settled ground.
2. **[Known unknowns](references/stage-2-known-unknowns.md)** — the questions
   you can name; resolve them one at a time.
3. **[Unknown knowns](references/stage-3-unknown-knowns.md)** — extract the
   taste and tacit context nobody has put into words.
4. **[Unknown unknowns](references/stage-4-unknown-unknowns.md)** — sweep the
   territory for landmines.
5. **[Hand over the map](references/stage-5-hand-over-the-map.md)** — the
   completed four-quadrant map, the walk's only done-condition.

When the user moves on to build, review, merge, or hand off what the walk
mapped — or asks for implementation notes, a buy-in doc, a quiz gate, or a
session handoff — read [after the walk](references/after-the-walk.md): the
map lives on past planning.

**Scope:** the full walk is for a full task. When the user asks for one slice
("do a blindspot pass", "quiz me on this change", "write the handoff"), run
that stage or move alone, recommend the next cheapest one, and stop — never
force the whole walk onto a request that named its slice.

## Rules

- For a full walk, walk the quadrants in order, one stage at a time, naming
  the current quadrant; the walk ends with the map in the user's hands — no
  map, not done. For a named slice, the Scope rule overrides quadrant order:
  run only that stage or move, then stop.
- Stages order the walk; they never embargo information. A finding that
  materially bears on a decision in flight is disclosed the moment you have
  it, then filed on the map under its quadrant — never held back for its
  stage's scheduled turn.
- Nothing closes off-screen. Any question or judgment call the map records as
  closed must have been shown to the user first — including ones the
  territory answered.
- An unknown closes only on evidence — a cited file, the user's explicit
  word, or observed output. "Seems right" keeps it OPEN.
- A conflict between two sources of truth — spec vs code, the user's words vs
  the territory — stops the walk at that point: name it, show both sides, let
  the user rule. Never silently pick one. A disclosed conflict takes the
  floor as the current question — asked alone, in the slot any other question
  would have taken, and like any question it carries your recommended answer:
  recommending is not deciding. When several conflicts surface at once, ask
  the highest-blast-radius one; file the rest as queued OPEN conflicts, one
  per turn.
- Agreement is not a deliverable. When the user's chosen direction carries a
  concrete cost, put the cost in front of them — quantified where possible —
  before walking on. The walk exists to find problems while they are cheap.
- Claims about the territory cite real files actually read; invented data is
  labeled as such. A fabricated specific destroys the map's authority.
- Start the map file at the end of stage 1 whenever the walk will span more
  than one sitting, produce artifacts, or end in a handoff, and update it as
  each stage closes; a short single-sitting walk may assemble the map at
  hand-over. Never let a context reset eat the walk. Map files, mocks, and
  notes live in a scratch or repo-ignored path unless the user asks to
  commit them.
- HTML artifacts are self-contained single files: inline CSS/JS, no external
  requests, plausible fake data over lorem ipsum.
- Stop at every stage boundary that needs the user's reaction. Never barrel
  into implementation on unconfirmed guesses — implementing is a separate
  task that begins after the map is delivered.
