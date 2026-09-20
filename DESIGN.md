# Design system: editorial enterprise assurance

## Visual theme

The portal should feel like a well-edited risk memo presented in an architecture studio: calm, exact, and easy to inspect. Density is low to moderate. Composition is asymmetric. Thin rules, type scale, and space carry the hierarchy. There are no generic SaaS card grids, neon security motifs, fake terminals, or decorative dashboards.

## Color roles

Light theme:

- Architectural paper `#F3F0E8`: canvas.
- Forest ink `#18362C`: primary text.
- Graphite sage `#5D675F`: secondary text.
- Warm rule `#C8C5BB`: separators.
- Oxide copper `#B95F43`: the single accent.

Dark theme:

- Rich graphite `#101210`: canvas.
- Warm ivory `#ECE9DF`: primary text.
- Stone `#A6A79F`: secondary text.
- Mineral rule `#34372F`: separators.
- Champagne copper `#C79B72`: the single accent.

## Typography

- Display: Instrument Serif where available, then a readable serif fallback. Maximum display size is `8.5rem`, with tracking no tighter than `-0.04em`.
- Body and controls: the platform sans stack. Body measure stays under 75 characters.
- Monospace appears only in code, identifiers, and machine output.
- Headings use sentence case. UI copy uses plain verbs and concrete nouns.

## Layout

- A 12-column desktop grid collapses to one column below 768px.
- Section spacing uses `clamp()` and remains generous without forcing every section to fill a viewport.
- Lists and thin dividers replace boxy cards.
- Touch targets are at least 44 CSS pixels where controls appear on mobile.
- No horizontal overflow at 320px or above.

## Motion

- Motion explains navigation or state. It does not decorate every section.
- CSS transitions use `cubic-bezier(.16,1,.3,1)` and target named properties.
- No layout-property animation, parallax, cursor replacement, scroll hijacking, or bounce.
- `prefers-reduced-motion` removes spatial movement and smooth scrolling.

## Interaction states

- Focus rings use the theme accent and remain visible on both canvases.
- Loading text states what is loading.
- Errors state the failed source and the recovery action.
- Empty data is distinct from a failed collector.
- The light/dark choice persists in local storage and falls back to the operating-system preference.

## Asset treatment

The technical portal uses no decorative stock imagery. Diagrams are semantic, data is labeled, and illustrative metrics are explicitly marked. The future personal portfolio may add editorial photography or generated campaign assets after its repository and final content are available.
