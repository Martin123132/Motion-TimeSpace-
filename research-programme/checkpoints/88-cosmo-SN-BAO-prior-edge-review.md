# 88 - Cosmology SN+BAO Prior-Edge Review

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 87 found:

```text
MTS_fixed_p3_u3quarter converges without its own edge;
CPL hits a prior edge;
stable_evidence_allowed = false.
```

This checkpoint tests whether the blocking edge is a one-off prior accident or a persistent flexible-baseline degeneracy.

## 2. Short Verdict

```text
prior_edge_review_status =
baseline_degeneracy_persists
```

```text
MTS_branch_status =
numerically_stable_but_not_promoted
```

```text
stable_evidence_allowed =
false
```

Plain English:

```text
The MTS fixed branch is not the one misbehaving here; the flexible CPL baseline keeps trying to sit on an edge or boundary-like corner. That makes the result interesting, but still not claimable.
```

## 3. Runner Changes

Extended:

```text
research-programme\scripts\cosmo_SN_BAO_closure_runner.py
```

with:

- `--cpl-wa-lower` and `--cpl-wa-upper` to widen or narrow the CPL `wa` prior without changing the MTS branch;
- `--include-mts-ablations` to score `MTS_fitted_p` and `MTS_fitted_u3` under the same data and nuisance rules;
- `prior_config`, `include_mts_ablations`, and `scored_models` written into `run_config.json`.

## 4. Runs

Default short smoke:

```text
research-programme\runs\20260531-124544-cosmo-SN-BAO-short-smoke
```

Narrow CPL `wa` prior:

```text
wa in [-1, 1]
```

```text
research-programme\runs\20260531-125058-cosmo-SN-BAO-short-smoke
```

Wide CPL `wa` prior:

```text
wa in [-6, 4]
```

```text
research-programme\runs\20260531-125112-cosmo-SN-BAO-short-smoke
```

MTS ablation run:

```text
research-programme\runs\20260531-125144-cosmo-SN-BAO-short-smoke
```

All runs use:

```text
SN rows = 250
BAO rows = 13
max_iter = 80
same SN nuisance = analytic offset
same BAO nuisance = analytic scale
```

## 5. CPL Edge Behavior

| CPL prior | CPL chi2 | CPL AIC | CPL BIC | Edge parameter | Edge readout |
|---|---:|---:|---:|---|---|
| `wa in [-2, 2]` | 126.017145 | 136.017145 | 153.877915 | `wa = -2.0` | lower edge |
| `wa in [-1, 1]` | 127.113223 | 137.113223 | 154.973993 | `wa = -1.0` | lower edge |
| `wa in [-6, 4]` | 125.819813 | 135.819813 | 153.680583 | `w0 = -0.2` | upper edge |

The failure mode moves rather than disappears. Narrowing `wa` pins `wa` to the new lower edge. Widening `wa` lets `wa` move inward but pushes `w0` to its upper edge.

## 6. Fixed-MTS Stability

Across the default, narrow, and wide CPL-prior runs:

| Quantity | Value |
|---|---:|
| `MTS_fixed_p3_u3quarter` chi2 | 127.662755 |
| `MTS_fixed_p3_u3quarter` AIC | 135.662755 |
| `MTS_fixed_p3_u3quarter` BIC | 149.951372 |
| `Omega_m` | 0.309710 |
| `B_mem` | 0.138740 |
| `B_mem` edge flag | no |

This stability is good pipeline behavior. It is not yet theory promotion.

## 7. Ablation Readout

| Model | chi2 | AIC | BIC | Edge flag | Readout |
|---|---:|---:|---:|---:|---|
| `MTS_fixed_p3_u3quarter` | 127.662755 | 135.662755 | 149.951372 | no | primary closure |
| `MTS_fitted_p` | 127.646523 | 137.646523 | 155.507293 | no | tiny chi2 gain, AIC/BIC worse |
| `MTS_fitted_u3` | 127.415906 | 137.415906 | 155.276677 | no | modest chi2 gain, AIC/BIC worse |

Best-fit ablation parameters:

| Branch | Fitted parameter | Best fit | Edge flag |
|---|---|---:|---:|
| `MTS_fitted_p` | `p` | 2.465580 | no |
| `MTS_fitted_u3` | `u3` | 0.130500 | no |

The fixed `p=3`, `u3=1/4` branch is not obviously overfitting this short smoke. Fitting either parameter does not buy enough improvement to pay the information-criterion penalty.

## 8. Interpretation Gate

Allowed statement:

```text
The short-smoke signal survives basic CPL prior perturbation in the sense that the fixed-MTS branch remains stable and non-edge, but the baseline sector is still degenerate.
```

Forbidden statement:

```text
MTS beats CPL.
```

Reason:

```text
CPL remains boundary-seeking under multiple prior choices, and the run still uses a short sampled SN subset without full covariance.
```

## 9. What This Means

This is not a grim failure.

It says:

```text
The MTS closure branch is behaving sanely enough to deserve a better test.
```

But it also says:

```text
The current short-smoke SN+BAO setup is too compressed to settle preference against flexible dark-energy baselines.
```

The right next move is not more victory language. The right next move is better likelihood discipline.

## 10. Next Target

Create:

```text
89-cosmo-SN-BAO-full-covariance-and-data-split-gate.md
```

with the next implementation focused on:

1. full Pantheon+ covariance or a clearly labeled diagonal-only limitation;
2. explicit no-SH0ES/no-local-calibration branch;
3. DESI DR1 vs DR2 split;
4. full SN sample run if runtime remains acceptable;
5. same edge-review matrix for `LCDM`, `wCDM`, `CPL`, and fixed/ablated MTS.

Acceptance:

```text
No cosmology-preference language unless the baseline sector stops boundary-running under the same data, priors, nuisance, and covariance rules.
```
