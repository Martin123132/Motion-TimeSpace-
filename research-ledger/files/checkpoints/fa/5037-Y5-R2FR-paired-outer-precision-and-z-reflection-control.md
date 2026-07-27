# 5037 — paired outer precision and z-reflection control

**Status: COMPLETE AS A FOUR-SCRAMBLE NUMERICAL SMOKE - all `189/189` jobs are numeric and converged; production precision and an epsilon-zero claim remain open.**

## Purpose

Checkpoint 5036 established a contracting two-scramble regulator ladder but
could not distinguish a fixed-target mismatch from one-point outer variance.
This checkpoint extends the exact same eventwise estimator to four independent
scrambles:

```text
seeds   = (503401,503402,503403,503404)
epsilon = (0.08,0.04,0.02)
C(z)    = D(z)+(t/s)^3 D(z_t)+(u/s)^3 D(z_u).
```

The local projection `a=(phi dot C)/(phi dot phi)`, `phi=1-z^2`, still occurs
event by event before either reflection diagnostics or the fixed 5018 target.
No `z<->-z` symmetry is imposed.

## Locked run

The restartable run is
`source-intake/functional_rg/5037/runs/paired_outer_precision_s4_v1`, with
config digest
`86e46b1d2663217182a1bd246c1367e6dfd1eca61694ec86c388d3182e502c49`.

The strict dry run found

```text
expected jobs          = 189
exact source imports   = 117
new kernels required   = 72
```

The imports comprise all 99 locked 5036 jobs plus 18 exact central jobs for
the two new scrambles from 5035. The first bounded production invocation ran
for `9046.2 s`, below the four-hour turn limit, and attempted 14 new kernels.

## Current state

After the endpoint-sector repair, bounded resume, and second chart-origin repair:

```text
terminal jobs          = 189/189
source-locked imports  = 117
new converged kernels  = 72
failed                 = 0
unconverged            = 0
not yet attempted      = 0
numeric jobs           = 189/189
```

All four paired vectors are complete. This closes the predeclared minimum
four-scramble precision smoke, but it does not satisfy the separate production
precision or epsilon-zero gates.

## Derived chart-origin repair

Two finite kernels initially failed only their residue-stability gate:

```text
E040__S503403_N0000__A01__primary24
E040__S503403_N0000__A13__primary24.
```

In both cases the sole gate-failing row was the same-source pair
`direct:g1:minus_u/direct:g1:plus_u` at relative root
`2.20758747145128`. Direct evaluation of the two global factor roots at that
point gives maximum modulus below `3.8e-15`. Thus both poles coalesce at the
stereographic chart origin; neither is a tracked homotopy crossing. This is a
coordinate degeneration, not a nonzero propagator pinch.

The v5 repair filters only a same-source `{plus_u,minus_u}` or
`{plus_v,minus_v}` collision when all represented global roots vanish below
`1e-7` **and** the root is not required by the transported homotopy. It does
not filter any finite collision, impose a contour winding, or alter the direct
integral. Both jobs then converge with their original direct values and
relative residuals:

```text
A01 : D/G^3 = 1752.6961738576 - 376.2771391565 i, residual=3.45817e-5
A13 : D/G^3 =   62.3284327493 +  40.8385816555 i, residual=3.83084e-5.
```

Each repaired kernel records 12 chamber-level chart rows: four distinct
same-source `{plus_u,minus_u}` or `{plus_v,minus_v}` origin coalescences, each
encountered in three chambers. All represented global roots are below
`3.8e-15`; none carries a transported winding. The repair records zero
remaining radius adjustments and a hash-linked copy of its pre-repair
job/kernel.

## Resolved finite endpoint sector

The chart-origin filter correctly did **not** repair

```text
E040__S503403_N0000__A14__primary24, z=9+0.04i.
```

That job reaches the finite pair
`direct:g1:minus_u/direct:g1:minus_v`. Its transported roots include

```text
3.47130355799 + 0.00063649518 i,
0.288076208166 - 0.00005282140 i,
```

and the coincident global factor values are finite and nonzero. The topology
already identifies this as an endpoint ownership boundary. Treating it as a
chart artefact would therefore have been a false repair.

The follow-up diagnostic localized the failure to adaptive quadrature only:
one global-cycle evaluation approached the endpoint to relative-sector
parameter `1.61e-13`, where the numerical root-coincidence tolerance merged two
mathematically distinct poles with opposite inherited ownership. Ordinary
chamber interiors remained valid.

For all four transported endpoints and both inherited sides, the local
two-torus double residue is below `3.57e-15`. Quadratic one-sided limits have
maximum relative refinement residual `9.29e-9`; adjacent-sector limits agree
to `7.03e-9`. Therefore the local principal part vanishes, the two sectors
share a finite continuous endpoint value, and the shrinking boundary detour
contributes zero. Only five evaluations inside the numerical coincidence tube
use that continuous extension; every off-pinch evaluation is unchanged.

Independent extension floors `1e-9` and `2e-9` produce the identical result

```text
D/G^3 = 833.9779876731545 + 261.7261506446660 i
relative residual = 3.6128138543e-5.
```

The repair is hash-linked in
`source-intake/functional_rg/5037/repairs/finite_endpoint_sector_v1`.

The remaining canonical kernels were then completed. Six further chart-origin
rows closed under the unchanged v5 criterion across the full run. The finite
A14 endpoint at `epsilon=0.02` and `0.08` received fresh, independent
zero-residue and two-sided-limit certificates rather than inheriting the
`epsilon=0.04` result. All three primary/audit floor pairs agree exactly.

## Completed four-scramble diagnostics

The complete mean regulator ladder contracts in the full-vector and local
coefficient norms:

```text
full-vector steps       : 14.0466 -> 11.1743, p_eff=0.3300
local-coefficient steps :  4.2014 ->  2.5591, p_eff=0.7152
```

Three of five nonlocal component mean steps contract; components at physical
cosines `-0.6` and `+0.3` do not. Checkpoint 5039 therefore performs an
uncertainty-aware paired audit rather than treating those two noisy sample
means as automatic theory failures.

The linear diagnostic gives

```text
local coefficient = -26.4934 + 0.8654 i
real standard error = 76.4951
nonlocal fixed-target RMS difference = 47.5256.
```

Every component's fixed-target residual is below `1.29` current standard
errors, but the errors are much too broad for a match claim. Reflection was
measured, never imposed.

## Boundary

Checkpoint 5037 now closes its exact matrix and numerical-geometry remit:
`189/189`, 117 exact imports, 72 computed-converged kernels, and no failed or
unconverged rows. The four-scramble smoke passes, while uncertainty-aware
target, epsilon-zero, production `hhh`, local GR and full MTS claims remain
open. No GitHub action was taken.

Marker: `MTS_5037_PAIRED_OUTER_PRECISION_REFLECTION_CONTROL_IN_PROGRESS`.
