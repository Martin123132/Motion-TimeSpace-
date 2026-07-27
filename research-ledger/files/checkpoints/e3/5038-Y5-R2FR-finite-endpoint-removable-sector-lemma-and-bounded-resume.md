# 5038 - finite-endpoint removable-sector lemma and bounded resume

**Status: COMPLETE AS A LOCAL NUMERICAL-GEOMETRY CHECKPOINT; the 5037 production matrix remains in progress.**

## Problem

The only failed 5037 job was

```text
E040__S503403_N0000__A14__primary24, z=9+0.04 i.
```

Its topology was valid, but adaptive relative quadrature approached the finite
collision `direct:g1:minus_u/direct:g1:minus_v`. Fixed ownership then rejected
the nearly coincident global roots because the two inherited sectors own
opposite members.

The diagnostic in
`scripts/Y5_R2FR_5037_A14_ownership_pinch_diagnostic.py` located the first
failure at

```text
y = 0.288076208166133 - 0.0000528214011765 i,
sector parameter = O(1e-13).
```

The global roots were still mathematically distinct. Their separation had
only fallen inside the numerical grouping tolerance. Sampling ordinary
chamber interiors produced no mixed-ownership failure.

## Conditional sector lemma

Let `x_+(y)` and `x_-(y)` collide at a transported chamber endpoint `y_*`,
and let `G_L(y)` and `G_R(y)` denote the global-cycle values with ownership
inherited from the adjacent relative sectors. Define the local two-torus
coefficient

```text
R_* = Res_(y=y_*) [dy/y sum_(a in I_+)
      Res_(x=x_a(y)) (dx/x) F(x,y)].
```

If

```text
R_* = 0,
lim_(y->y_* from L) G_L(y) = lim_(y->y_* from R) G_R(y) = G_*,
```

then the apparent endpoint pinch is removable for the iterated contour. There
is no logarithmic principal part. A boundary detour of radius `rho` contributes
`O(rho G_*)`, which vanishes as `rho -> 0`. Thus the two inherited sectors plus
their shrinking detour reproduce the unsplit off-pinch contour, with no
half-residue or imposed winding.

This lemma is exact. Checkpoint 5038 supplies a numerical certificate for the
specific A14 event; it does not claim a symbolic all-event theorem.

## A14 certificate

All four transported endpoints were checked from both sides:

```text
endpoint sides checked                    = 8
maximum local double-residue magnitude   = 3.5695e-15
maximum one-sided limit residual         = 9.2838e-9
maximum adjacent-limit mismatch          = 7.0210e-9
declared numerical-zero threshold        = 1e-7
declared limit tolerance                 = 2e-8
```

The implementation in
`scripts/Y5_R2FR_5037_endpoint_sector_repair.py` changes no off-pinch value.
It catches only the pre-existing mixed-ownership exception inside the certified
endpoint tube and evaluates the common quadratic sector extension. Five such
evaluations were required. Their largest recorded absolute error bound is
`2.25e-6` at the integrand level.

Primary and audit extension floors `1e-9` and `2e-9` give exactly the same
stored kernel:

```text
D/G^3 = 833.9779876731545 + 261.7261506446660 i
highest-order residual = 3.6128138543e-5
primary/audit relative difference = 0.
```

The original failed job, topology, scripts, certificates, extension calls,
and repaired job/kernel are hash-linked under
`source-intake/functional_rg/5037/repairs/finite_endpoint_sector_v1`.

## Bounded resume

The immutable 5037 runner then attempted eight additional `epsilon=0.02`,
seed-503403 kernels. Six converged directly. A01 and A13 reached the already
classified stereographic chart-origin degeneracy and were rerun through the
unchanged v5 gate; both converged without changing their direct values:

```text
A01: D/G^3 = 1766.4494060358 - 198.5877290198 i, residual=2.56283e-5
A13: D/G^3 =   62.8195622720 +  39.6763634832 i, residual=4.60994e-5
```

Current immutable matrix state (`139/189` numeric):

```text
expected               = 189
terminal numeric       = 139
exact imports          = 117
new converged kernels  = 22
failed                 = 0
unconverged            = 0
remaining              = 50
```

The complete paired population still contains only two scrambles. No
four-scramble precision statistic, fixed-target verdict, epsilon-zero limit,
production `hhh`, local-GR result, or full-MTS claim follows yet.

## Next calculation

Resume the same immutable matrix in bounded batches. Apply chart-origin or
finite-endpoint logic only when its existing certificate clauses are met. If a
new finite endpoint needs the continuous extension, require a fresh local
double-residue and two-sided-limit certificate; do not assume A14 universality.
After all 189 jobs are numeric, evaluate the four-scramble precision,
reflection, and untouched fixed-target gates.

No GitHub action was taken.

Marker: `MTS_5038_FINITE_ENDPOINT_REMOVABLE_SECTOR_AND_BOUNDED_RESUME`.
