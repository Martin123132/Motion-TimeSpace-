# 295 - Arrow Semigroup Parent-Time Attempt

Private derivation checkpoint. This is not a public cosmology, local-GR, CMB, or parent-field-theory claim.

## Purpose

Checkpoint 294 gave the endpoint integers a clean meaning:

```text
n_early=Tr(P_axis)=3
n_today=Tr(P_iso)=1
Delta n=2
```

but left the real problem:

```text
why 3 -> 1?
```

This checkpoint asks:

```text
can the endpoint arrow be derived from a parent time/coarse-graining/Ward trace law?
```

Short answer:

```text
yes, conditionally, as a semigroup/H-theorem.
```

But:

```text
the parent theory has not yet derived physical time as that semigroup.
```

## Axis-Load Projectors

Work on the resolved diagonal axis-load sector:

```text
A = span{E_11,E_22,E_33}.
```

The early resolved endpoint is:

```text
P_axis = I_A.
```

The late scalar trace endpoint is:

```text
P_iso = (1/3) 11^T.
```

The anisotropic residual projector is:

```text
R_aniso = I_A - P_iso.
```

These obey:

```text
P_iso^2=P_iso
R_aniso^2=R_aniso
P_iso R_aniso=0
P_iso + R_aniso = I_A.
```

The trace defect is:

```text
Tr(R_aniso)=Tr(P_axis)-Tr(P_iso)=3-1=2.
```

So the endpoint gap remains:

```text
Delta n=2.
```

## Semigroup Arrow

Define a coarse-graining semigroup:

```text
Phi_tau = P_iso + exp(-gamma tau) R_aniso.
```

Equivalently:

```text
dq/dtau = -gamma R_aniso q.
```

If:

```text
gamma > 0,
```

then:

```text
Phi_0 = I_A = P_axis,
Phi_infinity = P_iso.
```

The anisotropic residual decays as:

```text
||R_aniso Phi_tau q||^2
= exp(-2 gamma tau) ||R_aniso q||^2.
```

That is an honest mathematical arrow:

```text
resolved axis load -> scalar trace load.
```

In endpoint language:

```text
3 -> 1.
```

## H-Theorem Form

If the axis weights are positive and normalized, the same flow can be written:

```text
q(tau) = pi + exp(-gamma tau)(q(0)-pi),
pi=(1/3,1/3,1/3).
```

The Shannon entropy obeys:

```text
dH/dtau
= gamma sum_i (q_i-1/3) log(q_i/(1/3))
>= 0.
```

So the arrow is not just aesthetic.

It is the direction of:

```text
loss of resolved axis information,
decay of anisotropic residual,
increase of scalar coarse-grained entropy.
```

This is the cleanest arrow theorem route found so far.

## Parent-Theory Catch

The semigroup proves:

```text
if physical parent time is positive coarse-graining time,
then P_axis -> P_iso.
```

It does not prove:

```text
physical parent time is positive coarse-graining time.
```

That is a serious distinction.

An ordinary reversible local action does not normally produce irreversible projection by itself.

To parent-own this arrow, the theory needs one of:

```text
1. an entropy/gradient-flow principle,
2. an open-system or influence-functional derivation,
3. a boundary/domain measure that orients time,
4. a Ward/anomaly cancellation that forces gamma >= 0,
5. a parent observer map where time is exactly loss of unresolved orientation data.
```

Without one of those:

```text
the arrow is a closure law.
```

## Relation To 2/27

The conditional chain is now:

```text
B3 relative index -> k=9
SO(3) trace projection -> factor 1/3
projector rank defect -> Delta n=2
positive semigroup arrow -> 3 -> 1
```

Then:

```text
B_mem = Delta n/(3*k)
      = 2/(3*9)
      = 2/27.
```

This is significantly better than where the branch started.

But every arrow in that chain still has a condition attached.

So:

```text
B_mem=2/27 remains a locked empirical closure/theorem target,
not a finished parent derivation.
```

## Gates

| Gate | Result | Meaning |
|---|---|---|
| source paths exist | pass | audit traceable |
| semigroup constructed | pass | exact carrier for the arrow |
| monotone `3 -> 1` arrow | conditional pass | follows for `gamma>0` |
| entropy H-theorem | conditional pass | follows for positive normalized axis weights |
| parent time derived | fail | physical time not yet identified with this semigroup |
| positive `gamma` parent-owned | fail | irreversibility not action-derived |
| `B_mem` derived | fail | conditional chain only |
| local GR promoted | fail | no `q_loc`/PPN result |

## Decision

Decision:

```text
arrow_semigroup_conditionally_derives_3_to_1_parent_time_not_owned
```

Meaning:

```text
the missing endpoint arrow now has a precise conditional theorem:
positive SO(3)-equivariant coarse-graining sends P_axis to P_iso.
```

What improved:

```text
3 -> 1 is no longer merely asserted.
```

It follows from:

```text
Phi_tau=P_iso+exp(-gamma tau)(I-P_iso),
gamma>0.
```

What did not improve:

```text
the parent action has not yet derived gamma>0
or identified physical time with this coarse-graining parameter.
```

Boxing-score version:

```text
We found the punch trajectory.
It is clean: resolved axes decay into scalar trace.
But we still have to prove the bell rings in that direction.
No bell, no official stoppage.
```

## Machine Artifacts

Script:

```text
scripts/arrow_semigroup_parent_time_attempt.py
```

Run:

```text
runs/20260601-000118-arrow-semigroup-parent-time-attempt
```

Output files:

```text
runs/20260601-000118-arrow-semigroup-parent-time-attempt/results/source_register.csv
runs/20260601-000118-arrow-semigroup-parent-time-attempt/results/semigroup_algebra.csv
runs/20260601-000118-arrow-semigroup-parent-time-attempt/results/monotonicity_checks.csv
runs/20260601-000118-arrow-semigroup-parent-time-attempt/results/parent_contract.csv
runs/20260601-000118-arrow-semigroup-parent-time-attempt/results/route_status.csv
runs/20260601-000118-arrow-semigroup-parent-time-attempt/results/gate_results.csv
runs/20260601-000118-arrow-semigroup-parent-time-attempt/results/decision.csv
```

## Next Step

The next exact target is:

```text
derive positive coarse-graining time from the parent action.
```

The contract is:

```text
produce gamma >= 0 and Phi_tau as physical time evolution,
not merely as an observer projection.
```

If that cannot be done:

```text
the 2/27 chain should be explicitly classified as an elegant empirical closure,
with the derivation stack kept as a theorem target rather than a claim.
```
