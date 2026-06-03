# 152 - Calibration Bridge No-Go and Owner Contract

Private theory-promotion checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 151 said the future CMB spectra kill-screen is blocked by missing engine/wrapper, but the deeper live problem was already visible:

```text
the late SN+BAO branch and CMB bridge want different effective Omega_m0 values.
```

This checkpoint asks:

```text
Can the shared calibration bridge be derived under conservative assumptions,
or do we need a new parent-owned mechanism?
```

Short answer:

```text
Under conservative assumptions, the bridge is a no-go.
The alpha/r_d scalar calibration is not the repair.
The only live routes are a parent-owned BAO-shape correction, a screened Q^nu map, or a full Boltzmann inference map.
```

## 2. Machine Artifact

Script:

```text
research-programme\scripts\calibration_bridge_no_go_owner_contract.py
```

Run:

```text
research-programme\runs\20260531-235955-calibration-bridge-no-go-owner-contract
```

Generated:

```text
source_register.csv
no_go_assumptions.csv
calibration_evidence_table.csv
owner_candidate_matrix.csv
theorem_contract.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
calibration_bridge_no_go_under_conservative_assumptions_owner_contract_written
```

Claim ceiling:

```text
calibration_bridge_no_go_owner_contract_no_CMB_promotion
```

## 3. No-Go Assumptions

The conservative assumptions are:

| Assumption | Consequence |
|---|---|
| single metric background | CMB, BAO, and SN use one distance map once parameters are fixed |
| separately conserved ordinary matter | `rho_m(a)=rho_m0 a^-3`, so `Omega_m0^early = Omega_m0^late` |
| standard BAO ruler relation | `alpha_BAO = c/(100 h r_d)` is the scalar absolute-calibration relation |
| negligible memory at recombination | primary-era memory background cannot directly generate a percent-level matter shift |
| no private MTS rescue knobs | every nontrivial map must reduce to the baseline identity when `B_mem -> 0` |

Under these assumptions, the only derived bridge is the identity map:

```text
Omega_m0^early = Omega_m0^late.
```

That map is clean, but empirically it is exactly the problem.

## 4. Evidence

The late-only locked target remains:

```text
Omega_m0 = 0.3032827426766658
alpha_BAO = 30.012562164133616
```

The failed bridge does not come from the scalar alpha/r_d tape:

```text
same-shape xi_alpha mean = 1.000000039490485
same-shape tied-alpha BAO penalty mean = 3.3278224620403307e-10
```

The real remaining cost is shape/Omega driven:

```text
mean free-alpha BAO shape penalty = 3.1697527095124576
failing-gate shape penalty = 4.841090529899786
joint mean Omega_m0 shift = 0.01647749874764233
failing-gate Omega_m0 shift = 0.020762192385866185
```

So the tape is fine. The stance is wrong: CMB pushes the branch toward a higher `Omega_m0` than late SN+BAO wants.

## 5. The Strong Clue

There is still a real clue:

```text
B_mem * (2/9) = 0.016460905349794237
joint mean shift needed = 0.01647749874764233
joint mean residual after B_mem*(2/9) = 1.659339784811087e-05
```

That is not nothing. It is far too neat to ignore.

But it is not a theorem yet:

```text
worst joint residual = 0.004301287036071966
best CMB-only residual after B_mem*(2/9) = 0.009830345482600256
```

So `B_mem*(2/9)` is a strong closure clue, not a parent-derived bridge.

## 6. CMB Background Limit

Checkpoint 150 now makes one repair route less plausible:

```text
max recombination Omega_mem = 1.6266370173279974e-09
max |1+w_mem| at recombination = 0.0
```

The required bridge shift is about:

```text
joint shift / recombination memory fraction = 10129794.522141865
failing shift / recombination memory fraction = 12763875.507992124
```

So under the current smooth-memory picture, the bridge is not naturally a direct primary-era memory-density effect. It must be:

1. an inference/spectra effect;
2. a late-time BAO-shape/ruler projection;
3. a screened matter-memory exchange;
4. or a closure coincidence.

## 7. Owner Candidates

| Candidate | Status | Readout |
|---|---|---|
| identity map | derived under conservative assumptions | clean but fails target |
| alpha/r_d scalar calibration | rejected as primary repair | same-shape `xi` is already `1+O(1e-8)` |
| `B_mem*(2/9)` closure | useful empirical coincidence | centers joint rows, not full CMB transfer |
| `Q^nu` memory-matter exchange | possible only if parent-derived | threatens local GR unless screened |
| BAO-shape correction | live theorem target | must be parent-owned, not an ad hoc residual patch |
| full Boltzmann inference map | not run | needs the CMB kill-screen runner |

## 8. Promotion Contract

Any successful bridge must satisfy:

```text
B_mem -> 0  implies  Omega_m0^late = Omega_m0^early
```

and:

```text
no hidden B_mem refit,
no private MTS-only ruler rescue,
local/PPN silence preserved,
growth suppression preserved,
late branch preserved,
and CMB spectra kill-screen survived.
```

The bridge is not promoted until it supplies an owner for one of:

```text
Q^nu,
delta F_BAO(z),
or full Boltzmann inference response.
```

## 9. Decision

Current fair status:

```text
calibration bridge no-go under conservative assumptions.
```

This is not a death blow. It is a useful narrowing.

The target is no longer:

```text
fix alpha_BAO.
```

The target is:

```text
derive a BAO-shape/ruler correction,
derive a screened Q^nu early-late map,
or run a full Boltzmann inference kill-screen.
```

Next checkpoint:

```text
153-BAO-shape-or-Qnu-bridge-owner.md
```

My current preference is to try the BAO-shape owner first, because `Q^nu` risks stepping straight onto the local-GR landmine.
