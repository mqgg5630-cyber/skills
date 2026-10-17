---
name: taste
description: Reverse-engineer the design taste of a reference (live URL, screenshots, or app images) into explicit tokens plus the trade-offs behind them, then apply that taste to something new. Use when the user wants to extract a design system, study a competitor's look, match an app's aesthetic, asks "what makes X look like that", or wants design guidance that reads like a senior designer explaining choices instead of "clean and modern".
---

# Taste

Adapted from Sen Lin's MIT-licensed `taste` skill (https://github.com/senlindesign/taste-skill). This version drops the Playwright-only entry point: a URL, a set of screenshots, or a handful of app images all work as input, and the output is a design brief you can execute against.

## What you produce

Two things, in this order:

1. **`{name}.taste.md`**, the design DNA. Two sections:
   - **Design Map**: concrete tokens (color roles with hex, type scale, weights, radii, shadow recipes, spacing steps, layout grid, alignment strategy).
   - **Taste DNA**: four principles, each written as Trigger, Decision, Reason, Evidence. At least one must be a restraint (something the design deliberately did not do).
2. **The applied result**, if the user asked for a new asset or screen. Build it, then re-measure it against the Design Map.

A token list is not taste. A token list plus the decisions it implies is taste.

## Phase 0: name the source

Pick one:

- **Live URL**: capture with Playwright MCP (`browser_resize` to 1440x900, then `browser_navigate`, wait 3s, screenshot, evaluate a DOM extraction snippet). If Playwright is unavailable, ask for screenshots instead of guessing.
- **Screenshots or images**: ask what platform and state they show. Note the resolution, because a 1280px export and a 390px phone shot carry different precision.
- **A design the user already built**: capture two or three representative states (empty, populated, error) before deciding anything.

Write the source type at the top of the brief. Every measurement in the brief inherits its precision.

## Phase 1: measure, do not interpret

Read [references/measure.md](references/measure.md). Produce exact values (hex, px, ratio, weight) with roles attached. No adjectives. If a value cannot be measured, say so instead of inventing it.

Success criterion: a Design Map where every line could be typed into code without another decision.

## Phase 2: name the patterns

Still in [references/measure.md](references/measure.md). Group the measurements into recurring devices (the outline system, the accent budget, the spacing rhythm). A pattern is only real if it repeats at least three times in the reference. One-off flourishes get listed separately as incidents.

Success criterion: each pattern cites the measurements that prove it repeats.

## Phase 3: extract the taste

Read [references/taste.md](references/taste.md). Turn patterns into trade-offs: what did this designer choose, and what plausible alternative did they reject? Each principle needs a human reason (what the viewer feels) and evidence from Phase 1 or 2.

Success criterion: four principles, at least one restraint, zero banned adjectives.

## Phase 4: apply

Read [references/apply.md](references/apply.md). Implement against the Design Map, then verify: re-measure the output, diff it against the tokens, and check that each Taste DNA principle is visibly honored. Fix drift rather than rationalizing it.

## Rules

- The screenshot is the ground truth. DOM values that cover less than roughly 5% of the visible surface are decoration, not palette.
- Never report a color that appears only in markup, a hover state, or a single icon as a brand color.
- Banned words in the output: clean, modern, sleek, elegant, minimal, intuitive, seamless, polished, delightful, stunning, premium. If one appears, replace it with the actual decision.
- Every principle needs a rejected alternative. "Chose readable text over unreadable text" is not a trade-off.
- Keep the brief short enough that a person will actually read it. Four principles, not fourteen.
- When the reference and the user's request collide, say so: for example, a reference with near-zero contrast between text and ground cannot survive being used as a chat background behind bubbles, so the background version must lift contrast while keeping the palette.
