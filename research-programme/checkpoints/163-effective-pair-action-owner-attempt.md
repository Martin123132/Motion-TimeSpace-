# 163 - Effective Pair Action Owner Attempt

Private owner-mechanism checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 162 said the ruler route needs:

```text
a connected bilocal pair kernel with zero one-point marginal.
```

That was a condition. This checkpoint asks:

```text
can we construct the zero marginal rather than merely demand it?
```

Short answer:

```text
yes, at the effective/coarse-grained level:
use a connected compensated pair kernel.
```

But:

```text
this is not yet a fundamental parent action.
```

## 2. Machine Artifact

Script:

```text
scripts/effective_pair_action_owner_attempt.py
```

Run:

```text
runs/20260531-235959-effective-pair-action-owner-attempt
```

Generated:

```text
source_register.csv
compensated_kernel_proof.csv
action_candidate_ledger.csv
response_proof_matrix.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
connected_compensated_pair_action_constructed_not_fundamental_parent_derived
```

Claim ceiling:

```text
effective_pair_action_owner_attempt_no_bridge_promotion
```

## 3. Compensated Kernel Construction

Start with the raw finite-pair kernel from 160/161:

```text
K_raw^A_B(x,y)=T_D h^A_B+S_D(n^A n_B-h^A_B/3).
```

Define the marginals:

```text
K_x^A_B(x)=integral dmu_y W(x,y) K_raw^A_B(x,y)
K_y^A_B(y)=integral dmu_x W(x,y) K_raw^A_B(x,y)
K_bar^A_B=integral dmu_x dmu_y W(x,y) K_raw^A_B(x,y).
```

Then define:

```text
K_c = K_raw - K_x - K_y + K_bar.
```

For normalized domain measure:

```text
integral dmu_y W K_c = 0
integral dmu_x W K_c = 0.
```

So the zero marginal is now constructed algebraically.

## 4. Effective Pair Action

The best current effective owner is:

```text
S_pair ~ 1/2 integral dmu_x dmu_y
         :delta_g(x)delta_g(y):
         ell_A K_c^A_B ell^B.
```

The normal ordering / connected-pair structure means:

```text
one-point contractions are removed.
```

The compensated kernel means:

```text
one-point marginal response vanishes.
```

The finite connected kernel means:

```text
BAO pair response remains nonzero.
```

That is the cleanest effective-action version of the ruler-only move so far.

## 5. What This Proves

At leading order, this gives:

```text
delta O_1 proportional to marginal(K_c) = 0
delta O_2 proportional to K_c(x,y) != 0.
```

So:

```text
SN/H(z)/background one-point response can be null;
BAO pair response can be nonzero.
```

This is no longer just:

```text
please exempt SN.
```

It is:

```text
use a connected compensated pair action.
```

## 6. What Still Fails

The route is still not a full parent theory because:

```text
K_c is constructed as an effective/coarse-grained object;
T_D and S_D from checkpoint 161 are inserted, not varied from an action;
the local parent action that produces this connected pair sector is missing;
lensing/growth/two-point observables may inherit the operator;
CMB r_d safety still requires a late-ruler or Boltzmann proof.
```

So this is a real improvement, but not a promotion.

## 7. Candidate Ledger

| candidate | status | reason |
|---|---|---|
| raw bilocal pair action | incomplete | can leak into one-point marginals |
| connected compensated pair action | best effective owner | owns zero marginal and finite pair response |
| conserved pair current action | open theorem target | pair current not constructed |
| local parent action direct | missing | no derivation from local parent fields |
| BAO likelihood patch | rejected | not theory |

The current winner is only:

```text
best effective owner.
```

Not:

```text
fundamental parent action.
```

## 8. Gates

| gate | status | readout |
|---|---|---|
| source paths | pass | all required sources exist |
| compensated kernel identity | pass algebraic | `K_c=K_raw-K_x-K_y+K_bar` has zero marginals |
| effective pair action | conditional pass | normal-ordered connected pair action can own finite-pair response |
| fundamental parent action | fail open | still effective/coarse-grained |
| source-law insertion | fail open | `T_D`, `S_D` inserted rather than action-varied |
| SN/H(z) null | conditional pass | leading order only, if no metric/clock/geodesic coupling |
| lensing/growth | open mandatory | two-point observables may change |
| promotion | fail | no bridge/local-GR/CMB claim |

## 9. Decision

Current fair status:

```text
connected_compensated_pair_action_constructed_not_fundamental_parent_derived
```

Meaning:

```text
the zero-marginal condition is no longer a naked assertion;
it can be owned by a connected compensated effective pair action;
but this still does not derive the branch from a fundamental local parent
action, and it still inserts the 161 source laws.
```

Boxing-card readout:

```text
This is the cleanest defensive move so far.
We are not ducking SN by pretending it is not in the ring.
We are saying the punch is a connected pair punch, and its one-point follow-up
is subtracted by construction.
```

## 10. Next Target

Create:

```text
164-fixed-pair-ruler-branch-smoke.md
```

Task:

```text
run a fixed trace/quadrupole pair-ruler branch against SN+BAO/H(z), with no
fitted BAO projection knobs.
```

Pass condition:

```text
the fixed 161 laws improve or remain competitive on BAO without damaging SN/H(z)
under the null-response policy.
```

Fail condition:

```text
the fixed pair-ruler law performs worse than no-clock MTS or only works after
introducing fitted projection amplitudes.
```
