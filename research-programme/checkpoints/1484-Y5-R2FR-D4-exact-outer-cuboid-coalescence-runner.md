# 5468: D4 exact outer-cuboid coalescence runner

## Derivation

Two closed axis-aligned boxes with identical semantic ownership and identical intervals on two axes have union equal to their interval hull when their intervals on the third axis touch or overlap. Repeating this identity over epsilon, x and t to a fixed point produces a lossless cuboid cover; no representative margin and no untested gap region is imported.

```text
B1 = I1 x J x K, B2 = I2 x J x K, inf(I2) <= sup(I1)
B1 union B2 = hull(I1 union I2) x J x K
repeat over epsilon, x, t until no exact merge remains
```

A failed cuboid is a compression failure only. It must be split through its recorded source-fiber membership; it is not evidence that any constituent checkpoint-5451 leaf fails.

## Current state

Input fibers: `99522` covering `606990` source leaves. Fixed-point cuboids: `21065`. Fiber-to-cuboid compression: `4.72451934488`. Total leaf-to-cuboid compression: `28.815096131`.

Certified cuboids: `1/21065` covering `810/606990` source leaves. Failed cuboids: `0`. Remaining cuboids: `21064`.

## Decision

**EXACT_OUTER_CUBOID_TRANSPLANT_PARTIAL__RESUME**

## Claim boundary

Full outer enclosure becomes true only when every exact cuboid is certified or every failed cuboid is losslessly split to certified descendants. Event-local W3, the regulator limit, local GR and full MTS remain unclaimed.
