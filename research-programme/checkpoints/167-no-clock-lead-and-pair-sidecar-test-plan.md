# 167 - No-Clock Lead and Pair Sidecar Test Plan

Private governance checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 166 ended with:

```text
half_kernel_repair_improves_draw_but_no_clock_remains_lead
```

That result matters because the pair-ruler branch did not fail. It tightened up.
But it also did not beat the no-clock control.

So the next risk is not physics failure. The next risk is branch drift:

```text
using a sidecar theorem target as if it were the lead empirical branch.
```

This checkpoint locks the lanes.

## 2. Machine Artifact

Script:

```text
scripts/no_clock_lead_and_pair_sidecar_test_plan.py
```

Run:

```text
runs/20260531-235959-no-clock-lead-and-pair-sidecar-test-plan
```

Generated:

```text
source_register.csv
branch_lane_assignment.csv
lead_empirical_evidence_table.csv
claim_boundary_matrix.csv
sidecar_test_queue.csv
shared_baseline_fairness_rules.csv
promotion_gate_queue.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
no_clock_lead_pair_sidecar_governance_locked
```

Claim ceiling:

```text
lead_sidecar_governance_no_CMB_local_GR_or_parent_action_promotion
```

## 3. Lane Assignments

| branch | lane | status |
|---|---|---|
| `MTS_2over27_no_clock_u3quarter` | lead empirical lane | late-time empirical lead; theory promotion blocked |
| `MTS_pair_ruler_half_kernel` | sidecar theorem/test lane | best structural pair repair, still draw behind no-clock |
| `MTS_pair_ruler_base_161` | superseded sidecar baseline | survives but not lead |
| `MTS_global_clock` | demoted control lane | historical diagnostic only |
| `LCDM/wCDM/CPL` | baseline fairness lane | active fair baselines; same tests required |

The lead branch is:

```text
B_mem = 2/27
u3 = 1/4
no global clock
no pair-ruler projection amplitude
```

The sidecar branch is:

```text
T_D = (B_mem/8) F_D (1 - 2e^-N)
S_D = (B_mem/12)(1 - e^-2N)
```

This sidecar is allowed only if the effective pair action owns the `1/2`
factor before data scoring.

## 4. Why No-Clock Leads

The current lead is not chosen because it is perfect. It is chosen because it
has the broadest disciplined support and the fewest extra moving parts.

| arena | readout | metric |
|---|---|---|
| SN+BAO full covariance | preferred vs fitted LCDM | `DeltaBIC_vs_LCDM=-5.259466877748764` |
| BAO-only release holdout | DR2 preferred; DR1 draw | DR2 `DeltaBIC=-2.108368627321081`; DR1 `DeltaBIC=-0.8483738675035859` |
| BAO+H(z), no CMB | stable draw/preference | 10/10 draw; `DeltaBIC` range `[-1.9014668577456,-0.5803932783513801]` |
| fresh cosmic-chronometer H(z) | competitive draw vs LCDM | primary `DeltaBIC=+0.33256956910347313` |
| source-locked growth covariance | preferred/draw under GR-proxy growth | all rows `DeltaChi2=-2.30357028036`; jackknife failures `0` |
| ELG grid likelihood | draw | non-Gaussian ELG branch does not reverse scorecard |
| CMB bridge | unresolved/mixed | compressed draw only; transfer fails; joint bridge mixed |

So the fair status is:

```text
late-time no-clock MTS is competitive enough to keep testing seriously.
```

Not:

```text
MTS passes CMB.
MTS derives local GR.
MTS derives B_mem = 2/27.
```

## 5. Pair-Ruler Sidecar Rules

The pair-ruler result is useful because it probes whether the theory has a
genuine two-point/ruler sector. But it cannot be the lead branch right now.

Checkpoint 166 found:

```text
pair-action half kernel:
DeltaBIC_vs_no_clock = +0.5114297958095904
DeltaBIC_vs_base_161 = -0.990582113224491
DeltaBIC_vs_LCDM     = -4.742511257309843
```

Interpretation:

```text
better than the base pair-ruler branch;
competitive against LCDM;
still not better than the no-clock lead.
```

Allowed:

```text
growth/RSD sidecar response;
lensing/slip response;
CMB-ruler safety;
parent-action ownership of the half-kernel factor;
BAO row-pressure diagnostics with fixed formulas.
```

Forbidden:

```text
lead cosmology branch;
row-wise BAO repair;
continuous fitted projection amplitude;
public bridge/CMB/local-GR claim.
```

## 6. Baseline Fairness

The rule going forward:

```text
if MTS gets punched, LCDM/wCDM/CPL get punched too.
```

That means every future empirical runner should enforce:

| rule | requirement |
|---|---|
| same data vectors | identical rows, redshift cuts, source manifests, and covariance blocks |
| same nuisance profile | offsets/calibrations profiled or frozen symmetrically |
| same jackknife punches | every split applied to MTS and baselines |
| same edge flags | prior-edge/convergence dependence marked for every branch |
| draw honesty | `|DeltaBIC| < 2` is a draw unless context proves otherwise |
| claim ceiling | late-time empirical score cannot be reworded as parent-action/CMB/local-GR proof |

This is the boxing-card rule:

```text
close rounds are close rounds.
If the baseline also wobbles under the same punch, that punch is not a clean
knockdown of MTS.
```

## 7. Promotion Gates

The title-belt gates remain:

| gate | status | needed artifact |
|---|---|---|
| no-clock parent action | open | variation gives memory stress and conservation law |
| `B_mem=2/27` derivation | open | normalization/boundary-charge theorem |
| `u3=1/4` derivation | open | cell/transition theorem |
| perturbation owner | open | `mu(a,k)`, slip/Sigma, friction/source terms |
| local GR / PPN branch | open | derive `q_loc^nu -> 0`, `G_eff/G -> 1`, `Phi=Psi` |
| pair sidecar two-point safety | open | growth/RSD, lensing/slip, CMB-ruler tests |

These gates are not optional if the aim is a serious field theory rather than
another phenomenological dark-sector fit.

## 8. Sidecar Test Queue

| priority | target | branch | output |
|---:|---|---|---|
| 1 | half-kernel parent ownership | pair-ruler half-kernel | `168-pair-half-kernel-parent-ownership-gate.md` |
| 2 | growth/RSD sidecar response | pair-ruler half-kernel | `169-pair-sidecar-growth-rsd-safety.md` |
| 3 | lensing/slip safety | pair-ruler half-kernel | `170-pair-sidecar-lensing-slip-safety.md` |
| 4 | CMB-ruler safety | pair-ruler half-kernel | `171-pair-sidecar-CMB-ruler-safety.md` |
| 5 | official likelihood refresh | no-clock lead | `172-no-clock-official-likelihood-refresh.md` |

This ordering keeps the sidecar honest before it gets used as a bridge.

## 9. Decision

Decision:

```text
no_clock_lead_pair_sidecar_governance_locked
```

Meaning:

```text
No-clock MTS remains the empirical lead.
Pair-ruler half-kernel remains a fixed sidecar theorem/test branch.
Global clock remains demoted.
LCDM/wCDM/CPL remain active baselines and must face the same tests.
No CMB, local-GR, perturbation, or parent-action promotion is made here.
```

Boxing-card readout:

```text
No-clock is still ahead on the cards.
The pair-ruler half-kernel has better footwork than the base pair branch, but
it is not wearing the belt.
Now we use it as a sparring partner for the two-point machinery instead of
trying to force it into the main event.
```

## 10. Next Target

Create:

```text
168-pair-half-kernel-parent-ownership-gate.md
```

Task:

```text
Either derive the half-kernel factor from the effective pair action before
data scoring, or keep the pair-ruler route frozen as closure-only.
```

Pass condition:

```text
the 1/2 factor is owned by the action/operator normalization independently of
the BAO residual score.
```

Fail condition:

```text
the half factor is only an empirical repair knob.
```
