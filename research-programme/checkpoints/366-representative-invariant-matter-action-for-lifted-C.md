# 366 - Representative-Invariant Matter Action For Lifted C

Private derivation checkpoint. This is not a public WEP, clock, PPN, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 365 improved the lifted `C` route:

```text
local boundary primitive silence follows inside fixed relative-class variations.
```

The next GR-facing question is the matter one:

```text
does matter see only the lifted class observable C_D / P_D C,
or can it see representative data such as B_perp, b_2, scalar Cperp, or j_3?
```

Answer:

```text
representative invariance conditionally forces matter to ignore local representative data
and depend only on class observables.
```

But:

```text
species universality, physical class selection, normalization, and EH reduction are still not derived.
```

So this is a real theorem-shape improvement.

It is not a WEP/PPN/local-GR pass.

## 2. Machine Artifact

Script:

```text
scripts/representative_invariant_matter_action_for_lifted_C.py
```

Run:

```text
runs/20260601-211000-representative-invariant-matter-action-for-lifted-C
```

Outputs:

```text
results/source_register.csv
results/symmetry_contract.csv
results/matter_action_candidates.csv
results/selector_derivation.csv
results/exponential_composition.csv
results/residual_impact.csv
results/failure_modes.csv
results/gate_results.csv
results/decision.csv
results/next_queue.csv
status.json
DONE.txt
```

Status:

```text
representative_invariance_conditionally_selects_class_metric_direct_Cperp_vertices_forbidden_universality_and_class_selection_open
```

Claim ceiling:

```text
conditional_matter_selector_theorem_only_no_WEP_clock_PPN_EH_or_local_GR_promotion
```

Source paths missing:

```text
0
```

## 3. Symmetry Contract

The lifted `C` representative shift is:

```text
delta j_3 = dB_perp
delta b_2 = B_perp + d_boundary gamma_1
delta Q_rel[D] = 0
```

inside a fixed relative class.

The class scalar is:

```text
C_D[D] = N_D^-1 int_D J_C
```

and within the fixed-class sector:

```text
delta_B C_D = 0.
```

Therefore, if representative shifts are gauge/admissible symmetries of the parent theory, matter must obey:

```text
delta_B S_matter = 0.
```

That forbids matter from depending directly on:

```text
B_perp,
b_2,
scalar Cperp,
or local j_3 representative data.
```

Matter may depend on:

```text
C_D,
P_D C,
or an observed coframe built from that class observable.
```

This is the clean matter-selector theorem shape.

## 4. Matter Action Readout

| Candidate | Representative invariant? | Verdict |
|---|---|---|
| `S_m[psi, exp(C)g]` | no | reject as lead; raw scalar `Cperp` is matter-sourced |
| `S_m[psi, exp(C_D)g]` | conditional yes | best theorem target |
| `S_m[psi, exp(F(C_D))g]` | yes | allowed but underselects normalization |
| `S_A[psi_A, exp(F_A(C_D))g]` | yes but not universal | reject for WEP route |
| `S_m + int_boundary b_2 O_matter` | no unless constrained topological zero | reject for local-GR route |
| `sum_A S_A[psi_A, ehat, omega[ehat], constants_A]` | conditional yes | universal-coupling contract |

This is the important split:

```text
representative invariance kills local representative vertices.
```

But it does not, by itself, force:

```text
all species to use the same F(C_D).
```

So WEP is improved but not passed.

## 5. Selector Derivation

The derivation chain is:

```text
1. lifted C representative shifts are fixed-class gauge/admissible variations
2. physical matter observables must be invariant under them
3. direct dependence on representative data violates that invariance
4. matter dependence descends to the quotient/class observable
5. universal observed coframe kills direct WEP/clock vertices
```

In equations:

```text
delta_B S_matter = 0
```

requires:

```text
delta S_matter / delta B_perp = 0,
delta S_matter / delta Cperp = 0
```

for representative directions.

Thus:

```text
S_matter = S_matter[psi, ehat(C_D,g)].
```

This is exactly what we wanted from the lifted route.

But there is a caveat:

```text
this assumes representative invariance is a parent symmetry,
not just a branch rule.
```

That parent symmetry is now sharpened, but not globally completed.

## 6. Why The Exponential Is Natural But Not Fully Fixed

Representative invariance permits:

```text
ghat_mn = exp(F(C_D)) g_mn.
```

To get the exponential form, use class composition.

If independent class contributions add:

```text
C_12 = C_1 + C_2,
```

and metric scale factors compose:

```text
A(C_1 + C_2) = A(C_1) A(C_2),
A(0)=1,
```

then continuity gives:

```text
A(C) = exp(lambda C).
```

So:

```text
ghat_mn = exp(lambda C_D) g_mn.
```

Choosing:

```text
lambda = 1
```

is either a definition of the normalization of `C_D`, or it needs a parent amplitude/unit theorem.

Therefore:

```text
the exponential form is conditionally derived,
but its normalization is still open.
```

This is good enough to keep `exp(P_D C)g` as the best theorem target.

It is not enough to claim a completed matter metric.

## 7. Residual Impact

If this theorem is completed:

| Residual | Impact | Still open |
|---|---|---|
| `eta_WEP` | direct representative/species vertices forbidden | species universality and hidden `F_A(C_D)` exclusion |
| `alpha_clock_redshift` | direct `Cperp` clock vertex absent | common-mode `C_D/P_D C` drift or gradient |
| `gamma_minus_1` | matter/photon representative mismatch removed if they share `ehat` | EH exterior/operator residuals |
| `delta_G_or_fifth_force` | direct scalar/boundary representative force forbidden | class-changing events, bulk/radial/domain forces |

So the result is:

```text
direct representative hazards can be killed by symmetry.
```

But:

```text
common-mode local gradients and EH/PPN gates remain.
```

## 8. What Still Fails

Still not derived:

| Missing piece | Why it matters |
|---|---|
| species universality | representative invariance allows species-specific `F_A(C_D)` unless forbidden |
| physical class selection | local `Q_rel=0` and FLRW nonzero class are not parent-selected |
| normalization `lambda` | exponential scale can absorb a free coefficient |
| common-mode local silence | even class metric can produce clock/redshift drift if `C_D` varies locally |
| EH exterior operator | local GR needs metric-only second-order exterior dynamics |

This is not a failure.

It is a much sharper list of remaining debts.

## 9. Decision

Decision:

```text
representative_invariance_conditionally_selects_class_metric_direct_Cperp_vertices_forbidden_universality_and_class_selection_open
```

Meaning:

```text
if lifted-C representative shifts are parent gauge/admissible symmetries,
matter cannot couple to B_perp, b_2, scalar Cperp, or local representative data.
```

Matter must descend to:

```text
C_D / P_D C
```

or a coframe built from it.

But:

```text
species universality,
physical class selection,
normalization,
common-mode clock silence,
and EH exterior reduction
remain open.
```

No promotion:

```text
WEP/clock/PPN not passed,
projected metric not fully parent-derived,
Einstein-Hilbert exterior not derived,
local GR not derived.
```

## 10. Next Target

Next:

```text
367 - Topological Class Selection Or Local GR Closure Ledger
```

Aim:

```text
try the last clean derivation route for physical class selection:
local Q_rel = 0,
FLRW Q_rel != 0,
without a smooth arbitrary polarization function or smoothing scale.
```

If it works, the local-GR route gets much stronger.

If it fails, this branch should be ledgered as a disciplined effective closure and pushed into residual-bound testing.
