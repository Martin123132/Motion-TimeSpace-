# 125 - BAO Shape Theorem Target or Non-CMB Stress Route

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 124 localized the hard joint BAO penalty:

```text
dominant observable = DH_over_rs
dominant redshift group = z ~= 0.934
```

The penalty is not just a distance-ladder scale issue. It is mostly radial:

```text
D_H(z) / r_s = c / (H(z) r_s).
```

So this checkpoint asks:

```text
Should we chase an immediate BAO-shape theorem, or first run an independent
non-CMB H(z)-style stress test?
```

## 2. Machine Artifact

Script:

```text
research-programme\scripts\Hz_radial_stress_route_gate.py
```

Run:

```text
research-programme\runs\20260531-174600-Hz-radial-stress-route-gate
```

Generated:

```text
source_register.csv
data_option_audit.csv
covariance_diagnostics.csv
model_test_contract.csv
acceptance_gates.csv
decision.csv
status.json
```

Status:

```text
Hz_radial_stress_route_ready
```

Claim ceiling:

```text
route_gate_not_likelihood_evidence
```

## 3. Available H(z) Data

Local data already exist.

Full 32-row cosmic-chronometer table:

```text
[local-formalization-workbench]\data\cosmology\cosmic_chronometers\Hz.csv
```

Source:

```text
https://cluster.difa.unibo.it/astro/CC_data/data_CC.dat
```

Caveat:

```text
diagonal-error sanity check only; source metadata says no full covariance is
provided for the full 32-row table.
```

Prepared 15-row covariance branch:

```text
[local-formalization-workbench]\data\cosmology\cosmic_chronometers\covariance_branch\Hz_CC_Moresco15_BC03.csv
```

Recipe source:

```text
https://gitlab.com/mmoresco/CCcovariance
```

Decision:

```text
primary H(z) smoke = 15-row covariance branch
full 32-row table = diagonal sensitivity only
```

## 4. Covariance Preflight

All local 15-row covariance variants are symmetric and positive definite:

| Covariance | Rows | Min eigenvalue | Condition number | Status |
|---|---:|---:|---:|---|
| `diagonal_total_error` | 15 | `14.4926870922` | `169.61495024086986` | usable |
| `suggested` | 15 | `17.247664047203184` | `143.82310314996894` | usable |
| `conservative` | 15 | `17.64448252932561` | `153.15656871002747` | usable |
| `extra_conservative` | 15 | `18.17506235613284` | `165.38906560123263` | usable |
| `nonstat_systematic_only` | 15 | `0.30501299592797904` | `7741.084540309214` | usable but ill-conditioned |

Primary score should use:

```text
covariance_suggested.csv
```

Sensitivity branches:

```text
diagonal_total_error
conservative
extra_conservative
full32 diagonal-only
```

The nonstat-only matrix is invertible but highly conditioned, so it should be
diagnostic only.

## 5. Fair Model Contract

The next likelihood smoke must score:

```text
LCDM
wCDM
CPL
MTS_locked_2over27
MTS_Bmem_zero
```

with the same H(z) rows and covariance.

Model rule:

```text
H(z) = 100 h E(z).
```

MTS locked branch:

```text
B_mem = 2/27
p = 3
u3 = 1/4
```

Forbidden:

```text
no MTS-only radial correction
no fitted Omega map
no local-H0 prior in the primary branch
```

This is a radial-expansion stress test, not a rescue term.

## 6. Acceptance Gates

Before any H(z) result can be used even internally:

1. Source paths, row counts, and covariance dimensions must pass.

2. Primary branch uses:

```text
15-row suggested covariance.
```

3. Full 32-row diagonal branch is reported only as sensitivity.

4. Every model gets identical rows and covariance.

5. `MTS_Bmem_zero` must reproduce the LCDM background result.

6. Edge flags must be reported.

7. No model with edge-hitting is treated as stable evidence.

8. AIC/BIC must be reported against LCDM, wCDM, and CPL.

9. The result must be interpreted as:

```text
radial consistency stress only.
```

## 7. Decision

The next empirical move is:

```text
run an H(z) radial-expansion smoke test.
```

Why:

```text
BAO DH/rs pressure points at H(z), and local cosmic-chronometer data already
exist with a usable covariance branch.
```

The next theory move is not to invent a correction. It is to ask:

```text
Does the independent H(z) data prefer the same upward-radial behaviour that
the joint BAO/CMB compromise wants?
```

Possible outcomes:

| Outcome | Interpretation |
|---|---|
| MTS locked improves H(z) without edges | radial route gets stronger |
| MTS locked draws baselines | still alive; no promotion |
| MTS locked loses badly | BAO radial pressure may be DESI/compressed-bridge-specific |
| all models unstable | data/covariance branch is not decisive |

## 8. Boxing Readout

124 told us the punch was mostly radial.

125 says:

```text
Do not throw a wild theorem haymaker yet.
Make the opponent show the same weakness in an independent H(z) round.
```

This is the Mayweather route: clean footwork, same rules for both corners,
no secret glove weights.

## 9. Next Target

Next checkpoint:

```text
126-Hz-radial-expansion-smoke.md
```

Script:

```text
scripts\Hz_radial_expansion_smoke.py
```

Task:

```text
Fit H(z)=100 h E(z) on the 15-row covariance cosmic-chronometer branch for
LCDM, wCDM, CPL, MTS_locked_2over27, and MTS_Bmem_zero; then run covariance
and full32 diagonal sensitivities.
```

Claim ceiling:

```text
radial-expansion stress only; no CMB claim; no BAO-shape correction claim.
```

