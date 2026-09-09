# 5425: left first-soft invariant subcover gate

## Decision

**PASS FOR THE EXACT `(1,3)` INVARIANT AND CONTINUED V44 PRODUCTION ONLY.**

The recurring left/right hard-1--soft denominator is not a physical zero. It is an interval-dependency artefact caused by separately enclosing two chiral brackets. V44 now switches to the exact Lorentz invariant whenever either direct bracket loses zero separation.

## Exact reduction

With recoil `r`, soft cosine `x`, decay cosine `c`, regulator coordinate `q`, and the two parent factors `F_+` and `F_-`, the parent relative coordinate gives

`s_13 = 2(1-r^2)(1-C) = 4 r (q+1)(1-r^2) P / (F_+ F_-)`,

where `P` is the explicit polynomial implemented in the v44 parent. Symbolic elimination using `u^2=1-x^2` and `d^2=1-c^2` leaves exactly zero. Because `C` depends on `R+R^{-1}`, the same invariant serves the representative and reciprocal charts.

## Certified cover

The complete active right-connector regulator slab is covered by `320` closed boxes. Every leaf is nonzero and their single rectangular hull has real lower bound `0.0020680171376112493` and absolute lower bound `0.0020680171376112493`.

Across `150` direct momentum checks, the largest formula error is `7.043622102694415e-17`. Both targeted production boxes advance past `edge_2_1_3:stable_edge`.

## Consequence

This is an analytic repair, not another depth-only workaround: the old `(1,3)` obstruction is removed in both KLT copies. The targeted historical box now reaches the already-known external `(0,1)` obstruction instead.

## Claim boundary

The right connector is still incomplete. Regular-away W3, event-local W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain false.
