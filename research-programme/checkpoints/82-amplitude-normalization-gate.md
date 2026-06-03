# 82 - Amplitude Normalization Gate

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 81 selected:

```text
post_local_route_pivot =
pivot_to_amplitude_normalization_first_then_empirical_closure_tests
```

and set the gate:

```text
Every amplitude/normalization factor must be classified as derived, bounded, fitted, phenomenological, or rejected.
```

This checkpoint performs that classification.

## 2. Short Verdict

```text
amplitude_gate_status =
no_amplitude_fully_parent_derived
```

That sounds grim, but it is actually useful.

The amplitude sector is now honest:

```text
p=3 and u3=1/4 are bounded structural closures;
B_mem/b_mem remains fitted or calibrated;
C_coh local amplitude is diagnostic only;
local A_loc/q_loc suppression is not derived.
```

So:

```text
amplitude agreement cannot be used as evidence of a fundamental field theory yet.
```

## 3. Classification Register

| Factor | Status | Allowed use | Must not claim |
|---|---|---|---|
| `p = 3` | bounded structural closure, not parent-derived | fixed regularized activation exponent | parent action theorem |
| `u_3 = 1/4` | bounded structural candidate, not parent-derived | fixed less-free transition-scale closure | cell/domain theorem |
| `B_mem` / `b_mem` | fitted or calibrated closure parameter | explicit fit/calibration with priors | derived memory charge |
| `C_coh` amplitude | diagnostic closure selector | empirical selector tests only | derived local GR suppression |
| `F(N)=1-exp[-(N/u_3)^3]` | regularized closure shape | internal closure benchmark | fundamental scalar potential |
| scalar proxy normalization | reverse-engineered proxy | diagnostic reconstruction | fundamental MTS scalar action |
| `A_loc` / `q_loc` suppression | rejected as derived in current route | local bound target only | local vacuum plateau theorem |

## 4. Gate Results

| Gate | Result |
|---|---|
| `p=3` parent-derived | fail |
| `u3=1/4` parent-derived | fail |
| `B_mem` derived | fail |
| `C_coh` amplitude derived | fail |
| closure use allowed | pass |
| public claim allowed | fail |

This is the cleanest status:

```text
usable closures, no fake derivation.
```

## 5. What Improved

Before this gate, a good data fit could hide too much:

```text
Was the result from theory, or from amplitude freedom?
```

Now the rules are explicit:

- `p=3` can be fixed and compared against fitted `p`;
- `u3=1/4` can be fixed and compared against fitted `u3`;
- `B_mem/b_mem` must be fitted/calibrated openly;
- `C_coh` cannot be used as derived local suppression;
- local residual amplitudes are constraints, not victories.

That is a proper empirical spine.

## 6. Highest-Risk Factor

The most dangerous normalization is:

```text
B_mem / b_mem
```

Reason:

```text
It is the least structurally constrained amplitude and most able to absorb disagreement.
```

Therefore all future tests must report:

```text
B_mem prior range;
B_mem best fit;
B_mem prior-edge behavior;
B_mem sensitivity across data splits;
delta AIC/BIC against fair baselines.
```

If `B_mem` only works at prior edges or flips under splits, it is not evidence.

## 7. Empirical Handling Rules

| Factor | Handling in tests |
|---|---|
| `p=3` | fixed in primary tests; fitted-`p` run as ablation |
| `u3=1/4` | fixed in primary tests; fitted-`u3` run as ablation |
| `B_mem/b_mem` | fitted or calibrated with explicit priors |
| `C_coh` | diagnostic selector only |
| `A_loc/q_loc` | bound as local residual, not fitted as derived mechanism |

This protects the work from accidental overclaiming.

## 8. Next Obligations

| Obligation | Question |
|---|---|
| `B_mem` origin | can amplitude be tied to a conserved memory charge or normalization integral? |
| `u3` cell origin | can `1/4` come from a cell/domain theorem without the failed selector route? |
| `p3` regularity origin | can cubic onset be derived from smooth source onset or extremality? |
| local amplitude suppression | can residual local amplitude be bounded without a plateau theorem? |
| fair empirical matrix | which factors are fixed, fitted, or ablated in each test? |

The next immediate step is not another derivation tunnel.

It is:

```text
empirical closure manifest with fixed/fitted/ablated columns.
```

## 9. Claim Status

Allowed:

```text
MTS has disciplined regularized closure candidates worth testing.
```

Not allowed:

```text
MTS has derived its amplitude normalization from a parent field theory.
```

Not allowed:

```text
MTS has derived local GR through C_coh suppression.
```

This keeps the programme alive and serious.

## 10. Run Artifact

Script:

```text
research-programme\scripts\amplitude_normalization_gate.py
```

Run directory:

```text
research-programme\runs\20260531-121227-amplitude-normalization-gate
```

Generated tables:

```text
source_checkpoint_register.csv
amplitude_register.csv
gate_results.csv
empirical_handling.csv
next_obligations.csv
decision.csv
```

Status readout:

```text
amplitudes_classified_none_fully_parent_derived
```

## 11. Next Target

Create:

```text
83-empirical-closure-test-manifest.md
```

Acceptance:

```text
Every future empirical test must say which factors are fixed, fitted, ablated, bounded, or diagnostic.
Baselines must be tested fairly where comparable.
No closure result is treated as field-theory proof.
```
