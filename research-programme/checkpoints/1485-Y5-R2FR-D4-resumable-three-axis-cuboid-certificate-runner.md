# 5469: D4 resumable three-axis cuboid certificate runner

## Derived repair

Checkpoint 5468 proved a lossless 21,065-cuboid cover, but its largest all-at-once hull spent thirty minutes in x/t-only adaptive refinement without committing a witness. That interruption is non-evidential. This runner evaluates one exact subcuboid at a time, splits epsilon first whenever coalescence made it broader than its source-fiber scale, then selects x or t from source-width ratios. Every completed node is written atomically before the next node starts. A depth limit can be extended only explicitly; the recorded terminal witness is retained and split once by the same source-ratio rule without being reevaluated or erased.

Every split is an exact interval identity. Source boundaries nearest the midpoint are preferred; a numerical midpoint is used only when no interior source boundary exists. An interrupted run retains its unchanged pending node and all prior accepted certificates.

## Current state

Certified cuboids: `1/21065`, covering `810/606990` source leaves. Partial resumable cuboids: `1`. Depth-limit cuboids: `0`.

Accepted three-axis subcuboids: `146`. Pending subcuboids: `22`. Total node evaluations: `187`.

## Decision

**THREE_AXIS_CUBOID_CERTIFICATION_PARTIAL__RESUME**

## Claim boundary

Partial states and interrupted hulls are not failures. Full outer enclosure requires every cuboid to be certified or losslessly split to certified descendants. Event-local W3, the regulator limit, local GR and full MTS remain unclaimed.
