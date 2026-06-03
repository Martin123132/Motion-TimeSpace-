# 194 - Half-Memory Clock Map Derivation Attempt

Private theory checkpoint. This is not a public CMB claim.

## 1. Trigger

Checkpoint 193 found that the late-reference H0 and same-density CMB-profile
H0 are almost connected by:

```text
H_CMB = H_late exp(-B_mem/2).
```

This checkpoint asks whether the factor `1/2` can be derived rather than
inserted.

## 2. Machine Artifact

Script:

```text
scripts/half_memory_clock_map_derivation_attempt.py
```

Run:

```text
runs/20260601-000011-half-memory-clock-map-derivation-attempt
```

Command:

```text
python scripts/half_memory_clock_map_derivation_attempt.py --timestamp 20260601-000011
```

Status:

```text
half_memory_clock_map_metric_sqrt_candidate_domain_rule_missing
```

Claim ceiling:

```text
metric_clock_map_candidate_only_no_parent_action_no_CMB_claim
```

## 3. Derivation Attempt

Introduce a matter-observer metric:

```text
tilde_g_munu = exp(C) g_munu.
```

For a comoving observer:

```text
d tilde_tau = exp(C/2) d tau.
```

So the factor `1/2` is not arbitrary. It follows from the square root of the
metric conformal factor.

For a pure FLRW conformal map:

```text
tilde_a = exp(C/2) a.
```

The measured expansion rate is then:

```text
tilde_H = (1/tilde_a) d(tilde_a)/d tilde_tau
        = exp(-C/2) (H + dot_C/2).
```

If `C` is saturated or slowly varying at readout:

```text
tilde_H ~= H exp(-C/2).
```

Setting the saturated memory jump to:

```text
C = B_mem
```

gives:

```text
H_CMB = H_late exp(-B_mem/2).
```

This is a genuine derivation foothold:

```text
the half comes from metric geometry, not from curve-fitting.
```

But it only derives the algebraic form. It does not yet derive the parent
field `C`, the amplitude `B_mem`, or the late/CMB domain rule.

## 4. Numerical Check

| quantity | value |
|---|---:|
| late-reference H0 | `68.42175693081872` |
| same-density CMB-profile H0 | `65.92050790786743` |
| `H_late exp(-B_mem/2)` | `65.93397224868876` |
| error | `0.013464340821329301` |
| inferred `C=-2 ln(H_CMB/H_late)` | `0.07448253469982279` |
| locked `B_mem` | `0.07407407407407407` |
| `C-B_mem` | `0.0004084606257487161` |

If the tiny remaining mismatch is interpreted as the `dot_C` term:

```text
tilde_H/H = exp(-C/2) (1 + dot_C/(2H)),
```

then the required residual is:

```text
dot_C/H = -0.0004084189185673548.
```

So the clean bridge is already close; the leftover can be treated as a very
small derivative/calibration budget, but that budget is not yet derived.

## 5. Domain Rule Problem

The conformal clock map is dangerous if used lazily.

If it applies as a universal constant rescaling to every observable, it risks
moving the late SN/BAO/H(z) calibration too, which would erase the useful H0
split.

The viable route is narrower:

```text
CMB inference compares an early ruler to a late clock across an endpoint
memory jump, while late local calibrators absorb common local clock/ruler
scaling.
```

That is plausible, but it must be derived. Otherwise it is branch switching by
hand.

## 6. Parent Contract

To promote the clock map, the parent theory must provide:

| contract | required derivation | current status |
|---|---|---|
| matter metric coupling | `S_matter[psi, exp(C) g_munu]` or equivalent | candidate form written |
| memory identification | saturated `Delta C = B_mem = 2/27` | missing |
| slow/saturated readout | `dot_C/H` zero or bounded near H0 readout | bounded, not derived |
| late/CMB domain rule | CMB sees endpoint memory while late local ladders absorb common scaling | missing |
| local GR silence | local fixed point suppresses gradients and clock drift of `C` | missing |
| perturbation consistency | `C` perturbations do not break CMB/growth fits | missing |

## 7. Claim Gates

| gate | result |
|---|---|
| all cited sources exist | pass |
| factor `1/2` derived | pass |
| half-memory H0 bridge remains close | pass |
| residual derivative budget small | pass |
| `Delta C = B_mem` parent-derived | fail |
| late/CMB domain rule derived | fail |
| support claim allowed | fail |

## 8. Decision

Decision:

```text
half_memory_clock_map_metric_sqrt_candidate_domain_rule_missing
```

Meaning:

```text
The half-memory H0 bridge now has a concrete geometric origin: a conformal
matter-clock map. This is a much better position than a fitted calibration
factor. But it is still not a parent derivation.
```

Current theory status:

```text
keep the bridge as the lead theorem target;
do not claim CMB support;
next derive or reject the late/CMB domain rule and local silence condition.
```

Next target:

```text
195-late-CMB-domain-rule-and-local-silence-gate.md
```
