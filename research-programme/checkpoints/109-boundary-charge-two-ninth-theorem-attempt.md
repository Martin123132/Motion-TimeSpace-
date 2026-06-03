# 109 - Boundary-Charge Two-Ninth Theorem Attempt

Private checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 108 found:

```text
DeltaR = 2/9
B_mem = 2/27
```

survives the current SN+BAO robustness matrix as a locked no-fit amplitude. That makes `2/9` worth trying to derive.

This checkpoint asks:

```text
Can DeltaR = 2/9 be derived from normalized boundary charge, observer-cell trace split, or relative cohomology current?
```

## 2. Short Verdict

```text
two_ninth_theorem_status =
not_derived_but_target_sharpened
```

```text
promotion_allowed =
false
```

Plain English:

```text
We do not yet have a parent-action derivation of 2/9.
```

But the failed attempt is useful: it tells us exactly what must be proved next.

Boxing-score version:

```text
The counterpunch landed empirically in T7. The theorem punch did not land yet. But now we know the exact angle: derive the normalized boundary charge, not another floating amplitude corridor.
```

## 3. Machine Artifact

Script:

```text
research-programme\scripts\boundary_charge_two_ninth_theorem_attempt.py
```

Run:

```text
research-programme\runs\20260531-150236-boundary-charge-two-ninth-theorem-attempt
```

Generated:

```text
source_register.csv
route_attempts.csv
theorem_contract.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
two_ninth_theorem_not_derived_but_target_sharpened
```

## 4. Attempted Routes

| Route | Candidate chain | Result | Why it fails or remains conditional |
|---|---|---|---|
| relative form degree count | `(boundary 2-form / bulk 3-form) x spatial trace projection = (2/3)(1/3)=2/9` | fail as derivation | form degree is bookkeeping unless the action turns it into a charge measure |
| relative boundary pair pairing | `J_rel=(j_3,b_2)` gives a 2-to-3 boundary/bulk pairing, then trace gives `1/3` | conditional schema only | closure can be imposed, but representative and coefficient selection are not derived |
| nine-component deformation charge | `Q^i_j` has nine slots and two boundary-transverse slots carry relaxed charge | fail as default | FLRW coherent expansion is trace/isotropic, not automatically a two-transverse-slot channel |
| normalized boundary charge | `R=Q_boundary/Q_*`, with endpoint equations giving `(Q_early-Q_today)/Q_*=2/9` | best contract, not theorem | endpoint values are not predicted before data |
| empirical locked branch | `DeltaR=2/9`, `B_mem=2/27` survives T7 | empirical motivation pass | robustness motivates theory work but does not derive the number |

The tempting product:

```text
(2/3)(1/3) = 2/9
```

is not enough. Counting form degrees or components is not physics unless a parent variational measure says those counts are the normalized charge weights.

## 5. What Is Actually Needed

The theorem must prove:

```text
R = Q_boundary / Q_*
```

and:

```text
DeltaR = (Q_early - Q_today) / Q_* = 2/9
```

before fitting SN+BAO.

The exact contract is:

| Clause | Requirement | Status |
|---|---|---|
| T0 | define dimensionless `Q_boundary` and fixed unit `Q_*` from the parent action | missing |
| T1 | prove this `R` is the same `R` entering `Gamma_eff` and relaxation | missing |
| T2 | derive endpoint equations for `Q_early` and `Q_today` before data | missing |
| T3 | show `(Q_early-Q_today)/Q_*=2/9` from topology, cell geometry, or Ward identity | missing |
| T4 | preserve `eta=1`, `a_F=1`, `p=3`, `u3=1/4`, local GR/PPN silence, and conservation | open guard |
| T5 | freeze `B_mem=2/27` in future tests without refitting amplitude | passed for T7 SN+BAO scout |

So the theory problem is now beautifully narrow:

```text
derive Q_* and the endpoint charge split.
```

## 6. Gate Results

| Gate | Result | Reason |
|---|---|---|
| `two_ninth_empirical_target_exists` | pass | T7 locked amplitude matrix survived all six SN+BAO branches |
| `relative_boundary_language_exists` | pass | `J_rel=(j_3,b_2)` and `H^3(D,boundary D)` give a clean object to target |
| `boundary_charge_unit_defined` | fail | `Q_*` is not derived from the parent action |
| `two_over_three_factor_derived` | fail | `2/3` is motivated by boundary/bulk degree counting, not made into a charge ratio |
| `one_over_three_trace_factor_derived` | partial | spatial trace projection is natural, but Ward-fixed coupling to `R` is missing |
| `product_two_over_nine_derived` | fail | multiplying plausible factors is not a theorem |
| `post_fit_circularity_removed` | fail | `2/9` was noticed after the fitted primary amplitude |
| `theorem_target_live` | pass | the locked branch performs well enough that deriving or rejecting `2/9` is high value |
| `support_claim_allowed` | fail | no parent derivation yet |

## 7. Current Standing

Before checkpoint 107:

```text
B_mem was a fitted amplitude.
```

After checkpoints 107-108:

```text
B_mem = 2/27 is a strong locked empirical scout.
```

After this checkpoint:

```text
B_mem = 2/27 is not derived, but the derivation target is exact.
```

That is a real improvement. It moves the programme from:

```text
fit an amplitude corridor
```

to:

```text
derive or reject one exact normalized boundary-charge contrast.
```

## 8. Claim Ceiling

Allowed statement:

```text
The locked branch B_mem=2/27 is robust enough on current SN+BAO tests to deserve a focused parent-theory derivation attempt.
```

Forbidden statement:

```text
MTS derives DeltaR=2/9.
```

Reason:

```text
Q_*, endpoint equations, and Ward-fixed trace coupling are still missing.
```

## 9. Decision

Decision:

```text
two_ninth_status =
robust_empirical_theorem_target_not_prediction
```

Decision:

```text
best_live_theory_route =
normalized_boundary_charge_with_endpoint_equations
```

Decision:

```text
failed_shortcut =
degree_counting_2_over_3_times_trace_1_over_3
```

Decision:

```text
locked_empirical_branch =
B_mem=2/27 remains predeclared scout branch
```

## 10. Next Target

There are two honest next moves:

```text
Route A - theory:
derive endpoint charge equations for Q_boundary and Q_*.
```

or:

```text
Route B - empirical:
freeze B_mem=2/27 as a predeclared branch for external holdouts:
CMB distance/growth, BAO-only variations, and future non-SN data.
```

Recommendation:

```text
Route A first, then Route B.
```

Reason:

```text
T7 made 2/27 worth theory time. If Route A fails cleanly, Route B still gives a disciplined fixed-amplitude empirical pillar.
```
