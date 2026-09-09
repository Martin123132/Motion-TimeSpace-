# 5467: D4 all-outer-leaf epsilon-fiber transplant runner

## Exact transplant identity

For a fixed geometry rectangle `(x,t)`, consecutive closed regulator subboxes with matching imaginary interval have an exact union equal to their interval hull. The unchanged parent-v51 interval evaluator run once on that hull therefore encloses every source leaf in the fiber. Geometry ownership is not inferred from a representative margin: every member leaf is already source-certified outer by checkpoint 5451, and the source-partition minimum gap is retained.

```text
union_j [epsilon_j^-,epsilon_j^+] = [epsilon_a^-,epsilon_b^+]
fixed (x^-,x^+,t^-,t^+) and consecutive j=a,...,b
parent interval certificate on the hull => certificate for all member leaves
```

A failed hull is an interval-compression failure, not a failed source leaf. It must be split back along its recorded regulator partition or routed through the existing finite projective cover; no representative denominator is transferred.

## Current state

Source outer leaves: `606990`. Exact contiguous fibers: `99522`. Compression factor: `6.09905347561`. Maximum source leaves in one fiber: `64`.

Certified fibers: `1/99522` covering `64/606990` source leaves. Failed hull attempts: `0`. Remaining fibers: `99521`.

## Decision

**EPSILON_FIBER_TRANSPLANT_PARTIAL__RESUME**

## Claim boundary

The 77/77 representative smoke is complete, but full outer-leaf enclosure becomes true only when every exact fiber is certified or losslessly split to certified children. Event-local W3, the regulator limit, local GR and full MTS remain unclaimed.
