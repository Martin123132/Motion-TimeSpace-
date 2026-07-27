# 5051 - phase-covariant complex-control gate

Marker: `MTS_5051_PHASE_COVARIANT_COMPLEX_CONTROL_GATE`.

**Cost correction:** the estimator and candidate verdict remain valid, but the
wall-time projection in this checkpoint used two-event pair variances with
one-event runtimes. Checkpoint 5055 repairs that unit mismatch. Use 5055 for all
execution times.

## Exact estimator contract

For any matrix `B` fixed independently of future samples,

```text
mu_hat = mean_H(H - B L) + B mean_L(L)
```

is exactly unbiased for `E[H]`. Here

```text
H = 2 R(E020) - R(E040),
L = R(E040).
```

The parameter-free choice `B=1` therefore gives the exact Richardson
correction `H-L=2[R(E020)-R(E040)]`. This is algebra, not a fitted correlation.

## Candidate result

| candidate | score ratio | worst correction SD ratio | eligible |
|---|---:|---:|---|
| unit coefficient, all channels | 0.666 | 16.051 | no |
| unit coefficient, real only | 0.666 | 1.000 | yes |
| fitted scalar, all channels | 0.681 | 1.581 | no |
| complex coefficient per angle | 0.667 | 15.559 | no |
| shared complex coefficient | 0.665 | 16.153 | no |
| fitted scalar, real only | 0.681 | 1.000 | yes |

Complex phase mixing is decisively rejected: it transfers the large real
fluctuations into the small imaginary channels. The selected control is instead

```text
B = diag(1,1,1,1,1,0,0,0,0,0).
```

It improves all five real corrections without fitting any coefficient and
leaves every imaginary correction unchanged. Its equal-cost score ratio is
`0.6663`. The five fitted real coefficients, independently found in 5049, lie
between `0.994` and `1.049` in the full fit and support the exact unit choice.

## Boundary

At the optimal retrospective allocation the inactive imaginary channels cost
about `2.08` times more per unit precision because low-only samples do not help
them. The joint target-normalized score still improves because the real channel
is the dominant precision bottleneck. The former 32-hour estimate is withdrawn.
Under unit-consistent accounting the paired minimum-efficiency design is
`27.69 h`, while the conservative one-event design is `14.88 h`; neither is
within the 10-hour cap.

## Evidence

- Result: `source-intake/functional_rg/5051/phase_covariant_complex_control_gate.json`
- Candidates: `source-intake/functional_rg/5051/phase_control_candidate_comparison.csv`
- Components: `source-intake/functional_rg/5051/selected_phase_control_components.csv`
- Lock: `source-intake/functional_rg/5051/locked_phase_control_pilot_contract.json`
- Generator: `scripts/Y5_R2FR_5051_phase_covariant_complex_control_gate.py`
- Validation: `source-intake/mts_residuals/P8_Y5_BRR545_5051_VALIDATION.csv`

This is an estimator derivation and retrospective gate, not production `hhh` or
MTS physics evidence.
