# 5338 - D4 E0025 targeted support-exit depth-4 refinement

Date: `2026-08-10`

Marker: `MTS_5338_D4_E0025_TARGETED_SUPPORT_EXIT_DEPTH4_REFINEMENT`.

## Executive result

Checkpoint 5338 changes no threshold and recomputes no previously accepted
node.  It proves exact cache identity for all `432/432` checkpoint-5334 D4
outer nodes, raises only the adaptive-depth contract from three to four, and
evaluates the `24` new Q4/Q8 nodes belonging to

```text
P12S02LLLL
P12S02LLLR.
```

All `456/456` encountered nodes complete and pass their inner-energy,
pole-subtraction and exact-Jacobian contracts.  The right child passes its
local outer gate by a wide margin,

```text
P12S02LLLR: Q4/Q8 relative change = 2.065234424805188e-6.
```

The event-adjacent left child improves but remains above the unchanged `0.5%`
local gate,

```text
P12S02LLLL: Q4/Q8 relative change = 0.006405449614157091
local limit:                              0.005
```

so the finite `E0025` rung is **not accepted**.  Its global conservative error
is already below one percent,

```text
total relative conservative error = 0.0029782291055883764,
```

but a global cancellation is not used to excuse an unresolved local endpoint.
The correct decision is

```text
D4_E0025_TARGETED_DEPTH4_BLOCKED__DERIVE_SUPPORT_EXIT_ASYMPTOTIC.
```

This is a sharply localized numerical obstruction, not an inner-integral
failure and not evidence against the parent field-theory construction.

## 1. Exact computation performed

The pre-depth-4 state is copied into

```text
source-intake/functional_rg/5338/pre-depth4/.
```

The old plan hash is

```text
39fd506f4652d549bb524b0751c937ab5c14a3449955292c0cbae0a66ef858b0,
```

and the depth-4 plan hash is

```text
05943068f6c1a1db11e2b91126a1d5eb4764f5157839fd79cfcde0895baa057c.
```

The initial event-aligned geometry is byte-identical.  For every old shard the
wrapper verifies

```text
outer coordinate identity;
mapped weight identity;
physical result identity after deleting only node_plan_sha256;
geometric-pole CSV identity;
pole-fit CSV identity;
classification CSV identity;
cell-integral CSV identity.
```

Only after all `432` rows pass is the cache retagged to the depth-4 plan.  The
new run therefore adds exactly `24` physical evaluations rather than silently
repeating the full D4 calculation.

## 2. Numerical result

The complete depth-4 diagnostic is

```text
fixed-decay integral real       = 5.720158199277302
fixed-decay integral imaginary  = 6.48799772604819
fixed-decay integral magnitude  = 8.649527404313245

outer error absolute            = 0.02476335647911239
inner error absolute            = 0.0009969177859975975
total error absolute            = 0.025760274265109986
total error relative            = 0.0029782291055883764
```

Relative to the completed depth-3 diagnostic, the central value moves by only
about `5.3e-4` in magnitude and the conservative relative error decreases from
`0.0032478938188009996` to `0.0029782291055883764`.  Those improvements are
reported as diagnostics only because one local leaf remains unresolved.

The complete target chain is

```text
panel         depth   Q4/Q8 relative change   outcome
P12S02          0     3.4168353673841974e-2   refined
P12S02L         1     6.7880243342193110e-1   refined
P12S02LL        2     2.2277705911554840e-2   refined
P12S02LLL       3     9.9243023029843490e-3   refined
P12S02LLLL      4     6.4054496141570910e-3   blocked
P12S02LLLR      4     2.0652344248051880e-6   pass
```

The failure has therefore collapsed onto the single half-panel touching the
source-derived support-exit coordinate

```text
x0 = 0.8708639328146937.
```

## 3. Why another blind bisection is not the next step

The parent energy integrator already gives the exact material-simple-pole
piece for each energy cell:

```text
I_p(x)
 = mu R(x) [Log(E_U(x)-p(x)) - Log(E_L(x)-p(x))].
```

At event `E08`, the real pole crosses the lower support boundary.  With

```text
delta = x-x0,
m(x)  = Re[p(x)]-E_L(x),
kappa = m'(x0) = -35.08998477990699,
gamma = Im[p(x0)] approximately 1.3718247328621853e-4,
```

the fast lower-end factor is

```text
E_L(x)-p(x)
 = |kappa| delta - i gamma + O(delta^2).
```

Hence the source-owned local normal form is logarithmic:

```text
I_fast(delta) = -C0 Log(|kappa| delta-i gamma),
C0            = mu R(x0).
```

It has the exact outer primitive

```text
z(delta) = |kappa| delta-i gamma,

Integral_0^h I_fast(delta) ddelta
 = -C0/|kappa|
   {z(h)[Log z(h)-1]-z(0)[Log z(0)-1]}.
```

No phenomenological endpoint profile has been inserted: this form follows
directly from the logarithm already used by the parent pole-subtracted energy
integrator.

The regulator boundary-layer scale derived from the measured event slope and
pole imaginary part is

```text
delta_bl = gamma/|kappa| = 3.909448070344308e-6,
t_bl     = sqrt(delta_bl) = 0.001977232426990896.
```

For the depth-4 event-adjacent child,

```text
h       = 0.005362309606006255,
t_max   = sqrt(h) = 0.07322779257909018,
t_max/t_bl = 37.035500520560376.
```

Under the existing squared endpoint map, the closest Q4 node lies at
`2.5714431021226996 t_bl`, while the closest Q8 node lies at
`0.735342520178513 t_bl`.  Q8 samples the regulator core but Q4 does not.  The
remaining Q4/Q8 mismatch therefore has a concrete scale explanation.  Blind
bisection until Q4 first enters the core would require approximately depth
seven and could make both rules miss the same structure at other regulators.
That is not accepted as a derivation.

## 4. Required endpoint subtraction

The next implementation must evaluate the parent-owned endpoint coefficients
at `x0` and decompose the complete outer integrand as

```text
F(delta) = I_fast(delta) + F_regular(delta).
```

It must then

```text
1. integrate I_fast analytically with the primitive above;
2. apply Q4/Q8 only to F_regular;
3. bound variation of R, gamma, kappa and the energy boundaries across the
   endpoint collar;
4. show the subtracted remainder is continuous and numerically convergent;
5. compare the reconstructed panel value with the unmodified depth-4 value;
6. retain the same 0.5% local and 1% global gates.
```

The nearest completed node already independently confirms the relevant pole
identity (`MC04_SM_DM`, `direct:shared:s13`), pole-subtraction residual,
masked identity and simple-pole suppression.  It does not by itself license
using its residue as the exact endpoint coefficient; `C0` must be evaluated or
bounded at the source-derived event.

## 5. Claim boundary

Checkpoint 5338 validates only the execution and localization statements.  It
does **not** validate

```text
the D4 E0025 fixed-decay integral;
the D4 regulator-zero limit;
the decay-angle integral;
full angular convergence;
the full phase-space coefficient;
a numeric UV claim;
local GR;
the full MTS theory.
```

All corresponding claim flags remain false.  The result is private and no
GitHub action is taken.

## 6. Validation artifacts

The main artifacts are

```text
scripts/Y5_R2FR_5338_D4_E0025_targeted_support_exit_depth4_refinement.py
source-intake/functional_rg/5338/D4_E0025_depth4_preflight.csv
source-intake/functional_rg/5338/D4_E0025_depth4_prepare_validation.csv
source-intake/functional_rg/5338/D4_E0025_pre_depth4_shard_inventory.csv
source-intake/functional_rg/5338/D4_E0025_depth4_shard_migration.csv
source-intake/functional_rg/5338/D4_E0025_depth4_leaf_audit.csv
source-intake/functional_rg/5338/D4_E0025_targeted_depth4_result.json
source-intake/mts_residuals/P8_Y5_BRR545_5338_VALIDATION.csv
```

The final validation intentionally records `9/13` passing checkpoint gates.
The four failed rows are the direct logical consequences of the one local
leaf failure: child acceptance, all-leaf acceptance, parent acceptance and
narrow-claim promotion.  All source, cache, node, inner, global-budget,
provenance and protected-workbench gates pass.  The
`formalization-workbench` modified-file count remains zero.

## 7. Next action

Build checkpoint 5339 as a source-owned `E08` support-exit logarithm
subtraction and regular-remainder gate.  Do not raise the adaptive depth and
do not relax either numerical threshold before that derivation is tested.
