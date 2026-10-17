# Phase 1 and 2: measure, then name the patterns

## Role

Be a meter, not a critic. Phase 1 records what is there. Phase 2 records what repeats. Both avoid interpretation; interpretation belongs to Phase 3.

## Visual primacy

Study the screenshot before reading any markup. When the two disagree, trust what a human sees. Rules of thumb:

- A color under about 5% of visible surface area is an accent incident, not a palette color.
- A shadow at 3% opacity is a rendering artifact, not a design decision.
- White space the DOM reports as 10px may read as 80px of breathing room. Measure the gap the eye sees.
- Dividers that are invisible in the screenshot do not exist, regardless of borders in the CSS.

## Collect, with roles attached

1. **Color roles**: background, surface, ink, secondary ink, hairline, accent, accent-soft. Hex for each. Note which is the single saturated moment, if any.
2. **Neutral tinting**: are the grays pure (`#888`, `#CCC`) or pulled toward a hue? State the hue and the approximate offset.
3. **Type families and weights**: every family, every weight, where each is used. A three-weight single-family system is a different decision from a display/body pairing.
4. **Type scale**: every distinct size, largest to smallest, with its job (display, heading, body, caption).
5. **Letterform treatment**: tracking, casing, line-height ratio, optical alignment at edges.
6. **Radii**: every distinct value, and what consumes it. Note whether nested radii are concentric.
7. **Shadow recipes**: offset, blur, spread, color, layer count, and whether the color is neutral black or tinted.
8. **Spacing steps**: the base unit and the observed multiples. Note consistent rhythm versus arbitrary gaps.
9. **Layout grid**: columns, gutters, max width, and the alignment strategy per region.
10. **Image and card ratios**: aspect ratios of hero, thumbnails, and card-like blocks.
11. **Line weight and stroke**: for illustration or icon-heavy work, the stroke width in px, its cap and join style, and whether it stays constant across shapes of different size.
12. **Density map**: where the composition is busy and where it is deliberately empty, in relative proportions of the frame.

## Then name the patterns

Group the measurements into devices that repeat at least three times. Typical shapes:

- an outline system: one stroke weight, one ink color, used on every shape
- an accent budget: how many saturated elements are allowed per screen
- a spacing rhythm: the actual step sequence and where it doubles
- a shape grammar: radii, blob softness, how curves meet
- a texture layer: grain, paper, noise, and its strength

For each pattern write one line: **name, the measurements that prove it repeats, and what it excludes**. The exclusion matters, because it is the raw material for Phase 3.

Put one-off devices under a separate heading called Incidents. Do not promote an incident to a pattern to make the brief look richer.

## Output shape

```
## Design Map
- Background: #... (role)
- Ink: #... (role)
- Accent: #... used on X only, covering ~N% of the frame
- Type: family / weights / sizes and jobs
- Stroke: Npx, round caps, constant across shapes
- Spacing: base N, steps ...
- Density: busy top third, empty lower two thirds

## Patterns
- <Name>: repeats at X, Y, Z. Excludes <what it does not do>.

## Incidents
- <one-off device, with measurement>
```
