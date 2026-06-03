# 159 - Ruler-Only Projection Theorem Contract

Private theorem-contract checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 158 made the key split:

```text
global/universal clock coupling is demoted;
ruler-only BAO projection remains live.
```

But that creates a dangerous loophole:

```text
if BAO sees a projection but SN does not,
why is that physics rather than a BAO-only patch?
```

This checkpoint writes the exact no-smuggling contract.

Short answer:

```text
ruler-only projection is allowed only if it is a two-point BAO ruler-transport
operator, not a universal metric/clock/geodesic deformation.
```

If it is metric/geodesic, SN, H(z), lensing, and local clocks must see it too. That route already failed enough to demote the global clock branch.

## 2. Machine Artifact

Script:

```text
scripts/ruler_only_projection_theorem_contract.py
```

Run:

```text
runs/20260531-235959-ruler-only-projection-theorem-contract
```

Generated:

```text
source_register.csv
evidence_summary.csv
theorem_object_contract.csv
candidate_route_ledger.csv
no_smuggling_gates.csv
formula_contract.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
ruler_only_projection_contract_written_parent_theorem_missing
```

Claim ceiling:

```text
ruler_only_projection_contract_no_bridge_promotion
```

## 3. Evidence From 158

The empirical motivation is real but not sufficient:

| branch | result |
|---|---|
| ruler-only `u3=1/4` | ΔBIC vs LCDM = -3.868328116780731 |
| ruler-only `u3=1/4` | ΔBIC vs no-clock MTS = +1.3856129363377931 |
| ruler-only `u3=1/4` | ΔBIC vs global clock = -4.964039023763462 |

Meaning:

```text
ruler-only projection is better than global clock and better than LCDM;
but no-clock MTS remains stronger than the projection variant.
```

So this is not a new lead claim. It is a subroute that deserves a parent-theory attempt.

## 4. Core Distinction

The contract turns on one distinction:

```text
BAO is a two-point standard-ruler observable.
SN luminosity distance is a one-point standard-candle/photon-flux observable.
```

A ruler-only route must act on:

```text
galaxy-pair separation / ruler inference.
```

It must not act on:

```text
the universal metric,
photon geodesics,
source redshift,
SN luminosity distance,
local rods/clocks.
```

If it acts on those, it is no longer ruler-only. It becomes the global clock/metric route, and checkpoint 157/158 already says that route is not the bridge winner.

## 5. Required Objects

The parent theory must define:

| object | symbol | required meaning | current status |
|---|---|---|---|
| BAO pair separation | `ell_BAO^A` | two-point spatial/radial separation vector from clustering | conceptual target |
| ruler projection tensor | `R^A_B[D,Q]` | maps FLRW standard ruler to observed radial/transverse BAO channels | missing |
| screen projector | `P_perp^A_B` | transverse observer-screen projection | standard piece |
| radial projector | `n^A n_B` | line-of-sight projection | standard piece |
| coherent scalar load | `X_D` | coherent-domain load with local silence | conditional |
| projection amplitude | `Xi_D` | fixed scalar from memory/coframe invariants | candidate, not derived |
| SN immunity condition | `delta D_L_SN=0` | one-point luminosity distance does not inherit BAO projection | required, not derived |
| metric/equivalence safety | `not delta g_mu_nu` | not a universal metric/geodesic deformation | mandatory |

The dangerous item is:

```text
SN immunity.
```

We are not allowed to simply say:

```text
BAO gets it and SN does not.
```

The parent theory must derive why.

## 6. Formula Contract

The minimum mathematical skeleton is:

```text
ell_obs^A = R^A_B[D,Q] ell_FLRW^B.
```

Then:

```text
R^A_B = delta^A_B + Pi_perp P_perp^A_B + Pi_parallel n^A n_B.
```

where:

```text
Pi_AB = Pi_AB[X_D, F_D, boundary/coframe invariants].
```

If derived, the BAO observables may transform as:

```text
D_M^BAO/r_d -> (1 + Pi_perp) D_M/r_d
D_H^BAO/r_d -> (1 + Pi_parallel) D_H/r_d
```

But SN and chronometer null predictions must also be derived:

```text
D_L^SN = D_L^no-clock + O(Pi^2 or explicitly derived coupling)
H_CC(z) = H_no-clock(z) + O(Pi^2 or explicitly derived coupling).
```

That is the no-smuggling line.

## 7. Candidate Route Ledger

| route | status | reason |
|---|---|---|
| metric projection | rejected for ruler-only | SN/H(z)/lensing/local clocks must see it |
| universal clock map | demoted | strict SN and SN+BAO penalize it |
| two-point ruler transport | best live route | matches 158 failure split |
| late-time ruler calibration | live, high risk | may protect CMB `r_d`, but can become a patch |
| galaxy-bias/selection projection | deferred | too survey/systematics-like unless parent-derived |
| ad hoc BAO-only patch | rejected | not field theory |

The cleanest live route is:

```text
two-point ruler transport.
```

The hardest live route is:

```text
late-time ruler calibration that leaves CMB r_d untouched.
```

Both require a parent object.

## 8. No-Smuggling Gates

Machine gate summary:

| gate | status | failure if missing |
|---|---|---|
| two-point vs one-point distinction | open_mandatory | BAO-only exemption by hand |
| not metric deformation | open_mandatory | SN/H(z)/lensing inherit it |
| single tensor integrability | open_mandatory | row-wise BAO patch |
| zero-memory limit | conditional | projection not tied to MTS memory |
| local silence | conditional | local GR threatened |
| CMB `r_d` safety | open_mandatory | uncontrolled CMB bridge |
| SN/H(z) null prediction | empirically motivated, not theorem | diagnostic loses physics status |
| pre-data shape lock | open_mandatory | tuned DESI repair |

Overall:

```text
open mandatory gates = 5.
```

So this is not promoted. It is a strict work order.

## 9. Decision

Current fair status:

```text
ruler_only_projection_contract_written_parent_theorem_missing
```

Meaning:

```text
global clock is demoted;
ruler-only projection remains live;
the live route is two-point BAO ruler transport or late-time ruler calibration;
the projection must not be a metric/geodesic deformation;
the parent tensor R^A_B[D,Q] is missing;
no bridge, CMB, or local-GR promotion is allowed.
```

The exact no-smuggling requirement is:

```text
derive R^A_B[D,Q] before data-fitting,
derive why it acts on BAO pair separations,
derive why it does not globally remap SN clocks,
and derive Pi_perp/Pi_parallel from one tensor.
```

If any of those fail:

```text
the route demotes to closure-only.
```

## 10. Next Target

Next checkpoint:

```text
160-ruler-projection-parent-tensor-attempt.md
```

Task:

```text
construct or reject R^A_B[D,Q] from observer coframe / coherent-domain boundary physics.
```

Pass condition:

```text
one parent tensor gives radial and transverse BAO projection,
zero-memory/local-silence limits,
and SN/H(z) null response without being asserted by hand.
```

Fail condition:

```text
we can only write Pi_perp and Pi_parallel after looking at DESI rows.
```

Boxing-card version:

```text
The ruler feint stays on the card,
but the referee is watching the gloves now.
If it is a metric punch, SN gets hit too.
If SN does not get hit, the theory must prove this was a ruler move,
not a hidden low blow.
```
