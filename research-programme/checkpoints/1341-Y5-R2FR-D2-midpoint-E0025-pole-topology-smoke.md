# 5325 - D2 midpoint E0025 pole-topology smoke

## Purpose

This is the first new numerical decay-angle node after the inherited
D4-inner calculation.  It rebuilds the 44-cell, 11-panel contract at
`|d|=0.5744635178436776` and evaluates E0025 without
assuming that the old panel-nine material-pole topology transfers.

## Result

- completed nodes: `66` / `66`;
- all inner nodes pass: `True`;
- geometric poles: `185`;
- material simple poles: `62`;
- failed outer panels: `[1, 7, 8, 10, 11]`;
- fixed-decay value: `39.30076472295721` `+6.30243323813 i`;
- coarse fixed-decay acceptance: `False`;
- decision: **D2_E0025_POLE_TOPOLOGY_LOCALIZED__BUILD_EVENT_ALIGNED_REFINEMENT**;
- validation: **PASS**.

## Claim boundary

A pass is evidence for at most one E0025 fixed-decay value at D2_MID.
The regulator-zero limit, GL2/GL4 decay-angle integral, endpoint cap,
full phase space, UV coefficient, local GR, and full MTS remain separate.
