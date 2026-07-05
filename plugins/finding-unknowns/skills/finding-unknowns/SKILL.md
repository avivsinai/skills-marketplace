---
name: finding-unknowns
description: Find and resolve the user's unknowns before, during, and after implementation. Use when starting ambiguous or unfamiliar work, when the user asks for a blindspot pass or mentions unknown unknowns / "what am I missing / what should I be asking", when planning under uncertainty, when they want several directions to react to, when implementation deviates from plan or they want a deviations log kept, or when they want an explainer and quiz to understand a change before merging. Classifies known knowns, known unknowns, unknown knowns, and unknown unknowns, then routes each to the cheapest discovery technique.
---

The map is not the territory. The map is the prompt, spec, and context the user gives you; the territory is the codebase and the real world. **Unknowns** are the gap between them, and the quality of long-horizon work is bottlenecked by clarifying them — too-specific instructions block a needed pivot, too-vague ones invite best-practice guesses that don't fit. This skill runs one loop: locate the user's unknowns, run the cheapest technique that converts them into knowns, repeat until the map matches the territory.

Every explainer, brainstorm, interview, prototype, and reference is a cheap way to find out what the user didn't know **before** it gets expensive to fix.

**Scope**: when the user asks for one slice ("do a blindspot pass", "quiz me on this change"), run that technique, recommend the next cheapest move, and stop — do not force the whole loop.

## Step 1 — Build the unknowns inventory

First learn where the user stands: their experience with this domain and this part of the codebase; where they are in their thought process (vague itch, rough idea, firm spec); what they could already write down but haven't (constraints, taste, invariants, prior art they like). Work as a thought partner, not an order-taker — infer from the conversation and ask only for what's missing.

Then write a compact **unknowns inventory**: for each unknown — its quadrant, the evidence for it, the risk if it resolves wrong, the cheapest discovery move, and whether to ask the user now or inspect artifacts first. Completion: every quadrant below holds at least one entry or is explicitly declared empty — no quadrant unexamined.

## Step 2 — Route each unknown

| Quadrant | Signal | Technique |
|---|---|---|
| **Known knowns** | Already stated in the prompt/spec | None — restate scope back in one paragraph so drift is visible |
| **Known unknowns** | User can name the question but not the answer | **Interview** — or **Reference hunt** when the answer lives in code or docs, not in the user's head |
| **Unknown knowns** | Tacit knowledge — taste, house style, invariants, "I'd recognize it if I saw it" | **Directions & prototypes** for reactable domains; **Reference hunt** or concrete examples to compare when pointing beats reacting |
| **Unknown unknowns** | Unfamiliar territory; user can't yet name the questions | **Blind-spot pass** |

Route by cost: run the technique for the unknown that is most expensive to discover late (usually architecture-changing answers first, visual taste last). Techniques compose — a blind-spot pass typically surfaces known unknowns that then feed an interview. Completion: the user confirms no remaining unknown blocks planning; then move to **Plan**, and carry the tolerated unknowns into the **Deviations log**.

## Techniques

### Blind-spot pass

Given who the user is and what they know (Step 1), explore the territory — codebase, history, docs, the web — and come back with the unknown unknowns *they* couldn't have asked about: what good looks like here, prior art and past attempts, potholes and load-bearing constraints, how good this can get. Teach, don't dump: explain each finding so the user can prompt better, and end by proposing the questions they should now be asking. Completion: the user can restate their new known unknowns in their own words.

### Interview

Interview the user **one question at a time**; prioritize questions whose answer would change the architecture, and give your recommended answer with each question. If a question can be answered by exploring the codebase, explore instead of asking. Completion: no ambiguity remains whose resolution would change the plan.

### Directions & prototypes

For taste-shaped unknowns, produce **several wildly different directions** as cheap disposable artifacts the user can react to — an HTML page of design directions, a mocked toolbar with fake data, a throwaway script — before touching the real app. Never wire prototypes into real state or backends; their whole value is being cheap to discard. When the user reacts ("this one, but..."), have them verbalize *why* — that sentence is the recovered unknown known; record it in the spec. Completion: the user has picked a direction and the "why" is written down.

### Reference hunt

When the user can't describe what they want but can point at it, treat source code as the highest-fidelity reference — richer than screenshots or prose. Read the referenced implementation (a vendored library, a module on a site they like, code in another language) and extract the semantics to reimplement, not the syntax. Diagrams, docs, and pictures work as references too; prefer code when it exists. Completion: you can state the desired behavior precisely enough that the reference is no longer needed.

### Plan (change-led)

Write the implementation plan **led by the decisions the user is most likely to tweak** — data-model changes, new type interfaces, anything user-facing — and bury mechanical refactoring at the bottom. The plan's job is to surface what the user might need to alter, not to prove thoroughness. Completion: the user has explicitly approved or amended each likely-to-change decision, not just skimmed the plan.

## During implementation — Deviations log

However good the plan, unknowns lurk in the territory. Keep an `implementation-notes.md` in the workspace. When an edge case forces a deviation from the plan: pick the conservative option, log it under **Deviations** (what was found, what was chosen, why), and keep going — do not stop to renegotiate each one. Also log decisions made on unknowns the plan tolerated.

Closeout: the log is temporary. When the work ships, either delete it, fold the durable lessons into the right permanent home (repo doc, skill, test), or explicitly hand it off as a handoff artifact — never leave it to rot. Completion: every deviation from the approved plan appears in the log, and the log has been closed out one of those three ways.

## After implementation — Explainer & quiz gate

Two artifacts close the loop:

- **Explainer / pitch** — package the prototype, spec, and implementation notes into a single artifact a reviewer can absorb cold. Lead with the demo; answer the unknowns you started with, because reviewers start with those same unknowns and approvers look for the failure points they'd have anticipated.
- **Quiz gate** — the user may understand less of the change than they think, since behavior hides in existing code paths a diff doesn't show. Produce a report of what changed — context, intuition, what was done — ending with a quiz that tests understanding of *behavior* (what happens when X), not trivia (what is line 42). Grade honestly: this gates the *user's understanding*, not CI. Completion: the user passes fully, or every unresolved misunderstanding is recorded and re-taught before they merge or ship.
