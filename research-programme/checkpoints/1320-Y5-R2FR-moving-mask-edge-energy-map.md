# 5304 — Moving mask-edge fold topology and energy map

## Exact topology

At fixed `|d|=0.338281138367`, the 5272 surface

`F_{+1,-0.3}(sqrt(1-E),-|s|,-|d|)=0`

has exactly one physical `q=sqrt(1-E)` root for each
`0 <= |s| <= 0.995`. Implicit differentiation gives

`dE/d|s| = 2 q (partial F/partial |s|)/(partial F/partial q)`.

The derivative vanishes once. This is a nondegenerate minimum of `E(|s|)`,
so the inverse map has two coordinates between the fold and angular-cutoff
energies: an `INNER` branch and a short `OUTER` branch. Above the cutoff
event only the `INNER` branch remains. This fold was hidden by the earlier
tensor grid and invalidates the preliminary global-monotonicity assumption.

## Result

- fold: `E=0.0776215638880362` at `|s|=0.947685460798158`;
- fold second derivative: `0.731637683770714`;
- angular-cutoff crossing: `E=0.0795445844332201`;
- zero-coordinate crossing: `E=0.223867086613646`;
- energy width: `0.14624552272561`;
- two-branch width: `0.0019230205451839`;
- branch samples: `513`;
- inverse energy nodes: `35`;
- inverse energy-map rows: `38`;
- maximum equation residual: `5.79980508064e-13`;
- smallest nonfold transverse derivative magnitude: `0.0176247304356`;
- witness coordinate: `0.426511684066408`;
- witness reproduction change: `1.99840144433e-15`.

Decision: **MOVING_EDGE_FOLD_AND_TWO_BRANCH_TOPOLOGY_DERIVED__SELECT_TOPOLOGY_SAFE_REGULATOR_LADDERS**.

Validation: **PASS**.

## Claim boundary

This derives the fold and both branches of one exact hard-mask surface at one
fixed decay angle. It does not yet integrate the five-regulator residue along
those branches, integrate over the decay angle, establish the full
phase-space coefficient, or imply local GR or the full MTS theory.
