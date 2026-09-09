# D4 general proof-carrying adaptive-cover theorem draft

## Purpose

The current frontier repeatedly encounters an interval-hull zero in the same
`edge_2_1_3:stable_edge` factor. Checkpoints 5425, 5474, 5478 and 5496 already
show that this class can disappear under exact finite source subdivision while
the complete parent amplitude remains unchanged. The next parent revision
should therefore generalize the proved *operation*, not copy any previously
accepted numerical value or bind a repair to one coordinate box.

This draft states the exact contract for that generalization. It changes no
action, field, contour, chart, selector, residue, threshold or physical claim.

## Certified leaf evaluator

Let

\[
D=E\times X\times T
\]

be one closed epsilon/x/path-parameter box and let `P(D)` be the unchanged
parent-v58 evaluator. A successful call returns a complete-amplitude enclosure
with

\[
\int_T |A_D(t)|\,dt\le I_D,
\qquad d_D\le\inf_D |\Delta_A|,
\qquad r_D\le\inf_D |R|,
\qquad g_D\le\inf_D |J|,
\]

where `I_D` is finite and every required lower bound is strictly positive.
A failed call supplies an exception class and exact factor identity; it does
not supply a physical zero.

## Adaptive operator

Define `A_N(D)` recursively with a finite depth budget `N`:

1. Evaluate `P(D)` unchanged. If it passes, return that result exactly.
2. If it fails for anything except the precise connector
   `edge_2_1_3:stable_edge` interval singularity, propagate the failure.
3. If it has the precise failure and `N=0`, return unresolved; never accept.
4. Otherwise split t or x at the inherited source-grid boundary nearest the
   midpoint, falling back to the exact rational midpoint only when no interior
   source boundary exists. Select between t and x by the inherited normalized
   source-width rule. Epsilon remains an outer-frontier axis because it is not
   integrated by the path-amplitude aggregation rule.
5. Recursively evaluate both children. Return a parent enclosure only when
   every terminal child passes and the exact-cover checks below pass.

No terminal value may be interpolated, copied from a different sibling or
inferred from point sampling. A terminal call may be memoized only by replaying
an immutable result previously produced by the complete unchanged parent on
the *identical* argument binding, parent revision and source hashes.

## Finite-cover theorem

Let the recursion terminate in leaves `D_i`, with pairwise-disjoint interiors,
and let exact rational endpoint arithmetic prove

\[
D=\bigcup_{i=1}^{n}D_i,
\qquad
\sum_i \operatorname{vol}(D_i)=\operatorname{vol}(D).
\]

If every unchanged complete-amplitude leaf evaluation passes, then the parent
is certified by

\[
I_D=\sum_i I_{D_i},\qquad
d_D=\min_i d_{D_i},\qquad
r_D=\min_i r_{D_i},\qquad
g_D=\min_i g_{D_i}.
\]

All other certified lower-bound fields aggregate by minimum, all certified
upper-bound fields by the parent-declared maximum or sum rule, and active
material-branch identifiers by exact set union.

### Proof

For one split, the two closed children cover the parent and overlap only on a
measure-zero boundary. Additivity of the nonnegative path-integral upper bound
gives `I_D <= I_D0 + I_D1`. Every point of the parent lies in at least one
child, so each global absolute lower bound is at least the minimum of the two
child lower bounds. The exact branch set is their union. Induction over the
finite binary subdivision tree gives the stated formulas for all leaves.
Exact rational volume equality and pairwise interior-disjointness independently
exclude gaps and positive-measure double counting.

This proof establishes soundness **conditional on finite termination and
successful leaf certificates**. It does not assume or claim termination on
every outer cuboid.

## Control identity

If `P(D)` passes at the root, `A_N(D)` must return the unmodified parent result
before constructing a child. Consequently the control result, serialized
metric fields, branch set and audit counts must be exactly equal. This is the
required no-effect theorem away from the trigger; numerical closeness is not
enough.

## No-smuggling contract

A general parent revision is admissible only if all of the following are true:

- the trigger matches the exact exception type, connector segment and
  `edge_2_1_3:stable_edge` factor;
- every child calls the complete unchanged parent-v58 amplitude or resolves an
  immutable exact-binding certificate produced by that same parent revision;
- source-grid or midpoint endpoints are represented and checked with exact
  rational arithmetic;
- terminal leaves form a gap-free, pairwise interior-disjoint parent cover;
- all terminal denominator/root/Jacobian lowers are finite and positive;
- the integral upper is the sum of leaf uppers, never a fit or average;
- non-trigger failures and depth exhaustion propagate as failure/unresolved;
- an untriggered control is field-for-field identical to parent v58;
- the audit records the complete subdivision tree and source hashes;
- all local-GR and full-MTS claim flags remain false until the whole required
  operator/domain chain is independently complete.

These clauses make the operation proof carrying. The rule cannot turn a failed
leaf into a pass merely because neighboring leaves pass.

## Relation to existing revisions

- Parent v53 proves exact t-leaf aggregation for the stable-edge class.
- Parent v55 proves exact x/t-leaf aggregation of complete amplitudes.
- Parent v58 applies a verified adaptive T2 aggregate only at one exact
  hash-bound target.
- The proposed next revision would execute the same finite-cover proof for any
  exact matching trigger and return only newly evaluated leaf evidence. It
  would not reuse the checkpoint-5496 aggregate outside its binding.

Thus this is a generalization of a proved enclosure theorem, not a new
phenomenological closure and not a modification of MTS dynamics.

## Post-5504 integration gate

1. Preserve checkpoint 5504's atomic result regardless of outcome.
2. Use the failed checkpoint-5503 broad x sibling as the triggered target.
3. Use its actual descendant certificates as the adaptive leaves; continue
   subdivision until every leaf passes or one reaches a declared depth limit.
4. Re-evaluate an already passing, non-triggered parent-v58 box as the control
   and require exact result equality with zero adaptive applications.
5. Compare the adaptive target aggregate against an independently assembled
   union of the same leaves.
6. Promote the general rule only if the target, control, exact cover, source
   hashes and broad-claim guards all pass.

If checkpoint 5504 refines again, its children extend the same proof tree; that
is not a failure of this theorem. If any child remains unresolved, parent-v59
promotion remains blocked and the outer source frontier stays authoritative.

## Claim boundary

This draft derives a sound, domain-independent numerical enclosure-composition
rule. It does not prove that the present D4 outer cuboid terminates, does not
complete regular-away/event-local/combined `W3`, and does not by itself derive
local GR, Newton, Maxwell stress, calibrated source coupling or full MTS.
