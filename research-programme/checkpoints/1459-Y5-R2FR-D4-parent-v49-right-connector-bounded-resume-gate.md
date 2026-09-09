# 5443: parent v49 right-connector bounded-resume gate

## Decision

**PARENT V49 CONTINUES TO ADVANCE WITHOUT REPAIRED-FAILURE REGRESSION.**

Two source-identical v49 production resumes were run from checkpoint 5442. Both stopped only at their runtime budgets and remained resume-safe.

## Combined progress

- Accepted boxes: 529 -> 564 (`+35`).
- Live stack: 7 -> 9.
- Second-resume stack contraction: 12 -> 9.
- Collision-Jacobian failures: 5 -> 5.
- External01 c0 failures: 23 -> 23.
- External01 c1 failures: 262 -> 293.

## Stack interpretation

The combined live-stack count is not a completion percentage: after finishing the left subtree the depth-first runner opened the broad right subtree, temporarily increasing the stack. During the second resume that stack contracted from 12 to 9 while 18 boxes were accepted. Every newly accepted row has positive amplitude and collision-Jacobian lower bounds.

## Claim boundary

Nine right-connector boxes remain on the live depth-first stack. This is real certified progress, not right-connector completion; no regular-away W3, UV, local-GR, or full-MTS claim is made.
