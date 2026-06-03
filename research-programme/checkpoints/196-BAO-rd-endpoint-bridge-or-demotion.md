# 196 - BAO r_d Endpoint Bridge or Demotion

Private theory checkpoint. This is not a public BAO claim.

## 1. Trigger

Checkpoint 195 partially derived an endpoint-memory rule:

```text
1 + tilde_z = exp[(C_obs - C_emit)/2] (1 + z_g).
```

That made the CMB/late split less ad hoc, but it exposed BAO as the next
hazard because BAO uses:

```text
D_M/r_d, D_H/r_d, D_V/r_d.
```

The drag ruler `r_d` is an early-universe object measured by late surveys.
So the key question is:

```text
does the endpoint clock map cancel in BAO ratios, or does it rescale them?
```

## 2. Machine Artifact

Script:

```text
scripts/BAO_rd_endpoint_bridge_or_demotion.py
```

Run:

```text
runs/20260601-000013-BAO-rd-endpoint-bridge-or-demotion
```

Command:

```text
python scripts/BAO_rd_endpoint_bridge_or_demotion.py --timestamp 20260601-000013
```

Status:

```text
BAO_rd_common_mode_rule_required_half_memory_ratio_shift_rejected
```

Claim ceiling:

```text
BAO_endpoint_policy_internal_gate_only_no_parent_rd_claim
```

## 3. Data Shape

The gate loaded the DESI DR2 primary BAO vector:

| check | result |
|---|---:|
| BAO rows | `13` |
| covariance shape | `13 x 13` |
| quantities | `DM_over_rs`, `DH_over_rs`, `DV_over_rs` |

This is not a new cosmology fit. It is a scale-mode stress test:

```text
if the endpoint rule forced a global fractional shift in D_X/r_d,
how badly would DESI DR2 punish it?
```

## 4. Endpoint Policy Test

The locked amplitude is:

```text
B_mem = 2/27.
```

The dangerous half-memory ratio factor is:

```text
exp(-B_mem/2) = 0.9636404443012863.
```

That is a `-3.635955569871374%` shift in every BAO ratio if applied naked.

The policy table is:

| policy | ratio factor | DR2 scale-mode chi2 penalty | status |
|---|---:|---:|---|
| common-mode `D_X/r_d` cancellation | `1.0` | `0.0` | viable theorem target |
| `r_d` denominator only gets half-memory | `0.9636404443012863` | `172.3159081737169` | rejected without alpha rescue |
| distance numerator only gets half-memory | `1.0377314546247354` | `185.5646876400574` | rejected without alpha rescue |
| linearized denominator-only sidecar | `0.962962962962963` | `178.7971984722909` | rejected without alpha rescue |

This is a hard guardrail:

```text
BAO cannot tolerate a naked half-memory rescaling of D_X/r_d.
```

## 5. Row-Level Hazard

For the denominator-only half-memory shift, the largest row hazards include:

| z | observable | diagonal sigma shift |
|---:|---|---:|
| `0.934` | `DM_over_rs` | `-4.849010862385111` |
| `0.706` | `DM_over_rs` | `-3.5061364615828563` |
| `0.934` | `DH_over_rs` | `-3.1905418933426576` |
| `2.33` | `DH_over_rs` | `-3.1053982612921034` |
| `1.321` | `DM_over_rs` | `-3.092086579584712` |
| `0.295` | `DV_over_rs` | `-3.794826848216947` |

So this is not one rogue point. A global half-memory ratio shift would move
many DESI rows by several sigma.

## 6. r_d Microphysics Check

The CAMB same-density smoke already showed that the early sound horizon barely
moved:

| branch | `rdrag` | fractional shift vs LCDM |
|---|---:|---:|
| LCDM baseline | `147.10139220381296` | `0.0` |
| MTS high-cs fluid | `147.10122955697344` | `-0.0000011056784513767072` |
| MTS high-cs PPF | `147.10122955697344` | `-0.0000011056784513767072` |

So the BAO danger is not early sound-horizon microphysics in this smoke.
The danger is the observer/calibration endpoint policy.

## 7. Theory Contract

BAO survival now requires one of these:

| route | verdict |
|---|---|
| `D_X` and `r_d` share the same endpoint conformal unit, so `D_X/r_d` is invariant | best theorem target |
| a global BAO `alpha` absorbs the endpoint scale and is parent-derived | allowed only if derived |
| a naked half-memory factor shifts BAO ratios | rejected |

The previous BAO-only result remains useful:

```text
locked 2/27 survived BAO-only DR1/DR2 empirically.
```

But this checkpoint clarifies the theory burden:

```text
the parent theory must explain why BAO ratios are common-mode or why alpha/r_d
is parent-owned.
```

Otherwise BAO becomes a closure-only fit.

## 8. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| DESI DR2 BAO shape valid | pass |
| common-mode BAO endpoint policy safe | pass |
| naked half-memory BAO ratio shift allowed | fail |
| BAO alpha parent-owned | fail |
| BAO support claim allowed | fail |

## 9. Decision

Decision:

```text
BAO_rd_common_mode_rule_required_half_memory_ratio_shift_rejected
```

Meaning:

```text
BAO can survive the endpoint-clock route only if D_X and r_d share a common
conformal endpoint unit, or if a parent-owned BAO calibration alpha is derived.
A naked half-memory shift of D_X/r_d is strongly rejected by DESI DR2 covariance.
```

Current theory status:

```text
do not apply exp(-B_mem/2) directly to BAO ratios;
keep BAO as empirically promising but theory-gated;
derive the common-mode BAO ratio theorem next.
```

Next target:

```text
197-BAO-common-mode-ratio-theorem-attempt.md
```
