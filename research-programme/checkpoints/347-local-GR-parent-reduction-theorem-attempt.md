# 347 - Local GR Parent-Reduction Theorem Attempt

Private derivation checkpoint. This is not a public local-GR, PPN, WEP, Cassini, clock, CMB, cosmology, or unified-field claim.

## Purpose

Checkpoint 346 pinned the real target:

```text
connect MTS to GR from the parent action,
and derive as much as possible rather than fitting or assuming it.
```

This checkpoint attempts the local-GR reduction directly.

The pass/fail rule is:

```text
derive the local Einstein-Hilbert exterior and PPN residual vector from the parent action,
or isolate the exact missing axiom/closure that blocks the derivation.
```

Short answer:

```text
we get a real conditional GR-reduction theorem,
but not a parent-derived GR theorem yet.
```

The sharp blocker is still:

```text
N5_projector_stress_Bianchi_safe.
```

## Machine Artifact

Script:

```text
scripts/local_GR_parent_reduction_theorem_attempt.py
```

Run:

```text
runs/20260601-220000-local-GR-parent-reduction-theorem-attempt
```

Key outputs:

```text
results/source_register.csv
results/theorem_statement.csv
results/local_N_gate_status.csv
results/ppn_residual_vector_map.csv
results/closure_or_axiom_ledger.csv
results/gate_results.csv
results/decision.csv
status.json
DONE.txt
```

Status:

```text
local_GR_parent_reduction_conditional_theorem_written_N5_parent_action_blockers_remain_no_PPN_promotion
```

Claim ceiling:

```text
conditional_GR_reduction_only_no_local_GR_or_PPN_claim
```

Source paths missing:

```text
0
```

## The Attempt

Start with the parent-action contract:

```text
S_parent
= (1/2 kappa) int sqrt(-g) (R - 2 Lambda)
  + S_matter[g, psi]
  + S_MTS[g, X, P_mem, projectors, boundary/domain variables].
```

Metric variation must give:

```text
G_munu + Lambda g_munu
= kappa T_matter_munu + E_MTS_munu.
```

The MTS correction is legitimate only if:

```text
E_MTS_munu = -2/sqrt(-g) delta S_MTS / delta g^munu.
```

Then diffeomorphism invariance gives the Bianchi ledger:

```text
nabla_mu (T_matter^munu + kappa^-1 E_MTS^munu) = 0.
```

If matter is minimally coupled to the same physical metric/coframe and has ordinary local conservation, then the local burden is:

```text
nabla_mu E_MTS^munu = 0,
```

with no hidden projector force being silently dropped.

## Conditional Local-GR Theorem

The conditional theorem is:

```text
If the parent action has one physical metric/coframe,
and the local exterior action is Einstein-Hilbert,
and the MTS sector has no conserved bulk exterior support,
and relative memory is exact/pure-gauge,
and projector stress is zero, boundary-only, or retained in a conserved stress ledger,
then the local exterior field equations reduce to GR.
```

In equation form:

```text
E_MTS_munu -> 0
```

or boundary-only with no local bulk force implies:

```text
G_munu + Lambda g_munu = kappa T_matter_munu.
```

For local vacuum exterior:

```text
T_matter_munu = 0
```

so:

```text
G_munu + Lambda g_munu = 0.
```

In the weak-field Solar-System limit this gives:

```text
gamma = 1,
beta = 1,
preferred-frame residuals = 0,
clock/WEP fifth-force residuals = 0,
```

provided the no-hair/screening and metric-only exterior assumptions hold through the required post-Newtonian order.

That is real progress: local GR is now a finite premise stack, not a vibe.

## Why This Still Does Not Promote

The theorem is conditional because these premises are not parent-derived yet:

| Gate | Current status | Why it blocks promotion |
|---|---|---|
| `N0` unique metric/coframe | specified contract, not fully derived | local observables need one geometry |
| `N2` no trace-free/shear stress | conditional | otherwise `gamma-1` can be nonzero |
| `N3` no local scalar/vector hair | conditional | otherwise fifth-force, clock, preferred-frame residuals can appear |
| `N4` exact relative memory | conditional pass | useful only if paired with Bianchi-safe stress |
| `N5` projector stress | open hard blocker | cannot drop hidden metric-dependent stress |
| `N6` metric-only EH exterior | blocked by `N5` and parent ownership | needed for GR field equations |

The sharpest failure is not vague.

It is:

```text
If the projector depends on the metric or boundary metric,
then varying it produces T_projector.

If T_projector is ignored,
conservation is fake.
```

So the local-GR branch does not fail because the idea is incoherent.

It fails to promote because:

```text
T_projector = 0
```

or:

```text
T_projector = boundary-only / conserved retained stress
```

has not been derived from the parent action.

## PPN Residual Vector Map

This checkpoint writes the symbolic residual owners.

| Residual | Symbolic owner | Zero condition |
|---|---|---|
| `delta_gamma` | trace-free spatial residual / anisotropic projector stress | `N2` and `N5` remove bulk trace-free stress |
| `delta_beta` | second-order scalar residual plus nonlinear stress/no-hair terms | `N3`, `N5`, `N6` give EH exterior through PN order |
| `alpha1`, `alpha2` | vector residual `E_MTS_0i` / domain-frame hair | single coframe and no local vector hair |
| clock drift | direct clock coupling or scalar gradients | matter sees only `g/e`, local gradients vanish/screen |
| WEP/fifth force | composition-dependent coupling or MTS force | universal metric coupling and no species-dependent force |

This is not a numerical PPN pass.

It is the map of what must be killed.

The next local theorem has to turn those symbolic owners into:

```text
zero by theorem,
```

or:

```text
bounded residuals with explicit coefficients.
```

## Gate Results

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | all cited source files exist |
| conditional EH reduction theorem written | pass | if `E_MTS` has no conserved bulk exterior support, local EH/PPN GR follows conditionally |
| metric variation owned by parent | fail | `S_MTS` variation is still a contract |
| `N5` projector stress cleared | fail | `T_projector` not shown zero/boundary/conserved |
| metric-only EH exterior derived | fail | blocked by `N5` and parent action ownership |
| PPN residual vector calculated | fail | symbolic owner map written, not closed residual formulae |
| local GR promoted | fail | promotion blocked |
| branch declared dead | fail | coherent conditional theorem remains live |
| claim ceiling enforced | pass | no local-GR/PPN claim |

The fail rows are not embarrassing.

They are the exact shopping list.

## Decision

Decision:

```text
local_GR_parent_reduction_conditional_theorem_written_N5_parent_action_blockers_remain_no_PPN_promotion
```

Meaning:

```text
A conditional GR-reduction theorem is now explicit.
If MTS supplies one physical metric/coframe, a Bianchi-safe stress ledger,
no bulk local MTS exterior support, and a metric-only EH exterior,
then local GR/PPN follows.
```

But:

```text
those premises are not all parent-derived,
so MTS does not yet derive GR.
```

## Next Target

The next target should be narrower than "derive GR".

It should attack the blocker:

```text
348 - N5 Projector-Stress Conservation Theorem
```

Pass condition:

```text
derive T_projector = 0 in the local exterior,
or derive that T_projector is boundary-only and has no bulk PPN support,
or retain T_projector in a conserved stress equation and compute its PPN residual vector.
```

Fail condition:

```text
drop projector stress because the GR limit needs it gone.
```

That route would be cheating, and it is now explicitly forbidden.

## Bottom Line

This is movement in the right direction.

We did not get:

```text
MTS -> GR
```

as a completed proof.

We did get:

```text
MTS -> GR if and only if the local exterior MTS stress is owned and silenced.
```

That is the right kind of narrowing.

The next real derivation fight is not cosmology.

It is:

```text
own projector stress,
or the local GR branch remains closure-only.
```
