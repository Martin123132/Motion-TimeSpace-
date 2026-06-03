# 162 - Pair Ruler Operator Null Response Contract

Private null-response checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 161 found candidate source laws:

```text
T_D = (B_mem/4) F_D(N,u_3=1/4)(1 - 2e^{-N})
S_D = (B_mem/6)(1 - e^{-2N})
```

Those can populate the tensor:

```text
R^A_B = delta^A_B + T_D h^A_B + S_D(n^A n_B - h^A_B/3).
```

But the dangerous question remained:

```text
why does this move BAO pair separations without moving SN/H(z)?
```

Short answer:

```text
there is a conditional mathematical route:
a connected bilocal pair kernel with zero one-point marginal.
```

But there is still no parent action deriving that kernel.

## 2. Machine Artifact

Script:

```text
scripts/pair_ruler_operator_null_response_contract.py
```

Run:

```text
runs/20260531-235959-pair-ruler-operator-null-response-contract
```

Generated:

```text
source_register.csv
operator_condition_contract.csv
route_null_response_audit.csv
observable_response_matrix.csv
theorem_chain.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
pair_ruler_null_response_contract_conditional_bilocal_operator_not_parent_derived
```

Claim ceiling:

```text
pair_ruler_operator_null_response_contract_no_bridge_promotion
```

## 3. Conditional Null Theorem

Define a pair separation:

```text
ell^A(x,y).
```

Let the ruler operator act only on finite pair separations:

```text
delta ell^A(x,y) = K^A_B[D](x,y) ell^B(x,y).
```

Use the 160/161 tensor form:

```text
K^A_B = T_D h^A_B + S_D(n^A n_B - h^A_B/3).
```

Now impose the key null condition:

```text
integral_D dmu_y W_D(x,y) K^A_B(x,y) = 0.
```

Then a one-point observable has linear response:

```text
delta O_1(x) proportional to integral_D K(x,y)dmu_y = 0.
```

But a two-point BAO ruler has response:

```text
delta O_2(x,y) proportional to K(x,y) != 0.
```

That is the cleanest mathematical way to say:

```text
BAO pair separations can move while one-point SN/H(z) observables remain null.
```

However, this is only conditional unless the parent theory derives the kernel and its zero marginal.

## 4. Non-Negotiable Conditions

The operator must satisfy:

| condition | formula | status |
|---|---|---|
| bilocal connected operator | `delta ell^A(x,y)=K^A_B ell^B` | required |
| zero one-point marginal | `integral_D W_D K = 0` | conditional null theorem |
| non-metric/non-clock | `delta g=delta z=delta u=0` | mandatory |
| trace/quadrupole eigenstructure | `K=T h + S(n n-h/3)` | candidate from 160/161 |
| zero memory/local silence | `B_mem,F_D,X_D -> 0 implies K -> 0` | conditional |
| CMB `r_d` safety | `delta r_d=0` unless Boltzmann-derived | open mandatory |
| parent variational owner | `K` from action/effective action/current | missing |

This is the no-low-blow version:

```text
SN/H(z) are not exempt by decree.
They are null only if the one-point marginal vanishes and no metric/clock
deformation is present.
```

## 5. Route Audit

| route | BAO response | SN/H(z) null? | status |
|---|---|---|---|
| metric deformation | yes | no | rejected for ruler-only |
| global clock/redshift map | yes | no | demoted |
| one-point coframe strain | yes | no | rejected for null branch |
| connected bilocal pair kernel | yes | conditional yes | best live effective route |
| late-time BAO ruler calibration | yes | conditional yes | live high risk |
| ad hoc BAO likelihood shift | yes | by declaration | rejected |

So the only live clean route is:

```text
connected bilocal pair kernel with zero one-point marginal.
```

## 6. Observable Response Matrix

| observable | response | condition |
|---|---|---|
| BAO pair separation | nonzero | finite-pair `K(x,y)` |
| SN luminosity distance | zero at linear order | zero marginal and no metric/geodesic deformation |
| cosmic chronometer `H(z)` | zero at linear order | no clock/lapse/background deformation |
| local rods/clocks/PPN | zero if bound-domain silent | `K -> 0` in bound domains |
| lensing/growth/correlation observables | open | two-point statistics may inherit the operator |
| CMB sound horizon `r_d` | zero only if late-ruler transport | early-time safety still required |

Important:

```text
lensing and growth are not automatically null.
```

If this is a two-point matter/ruler operator, other two-point observables may see it. That is a testing opportunity, not a bug to hide.

## 7. What Was Derived

This checkpoint derives a conditional algebraic fact:

```text
zero one-point marginal implies zero leading one-point response;
finite pair kernel implies nonzero BAO pair response.
```

That is enough to keep the route logically alive.

It is not enough to promote the route, because the parent theory has not derived:

```text
the bilocal kernel,
the zero marginal,
the coarse-grained effective action,
the CMB/lensing/growth safety conditions.
```

The fair interpretation is:

```text
we have a clean contract for how SN/H(z) immunity could be real;
we do not yet have the parent owner that makes it real.
```

## 8. Gates

| gate | status | readout |
|---|---|---|
| source paths | pass | all required sources exist |
| conditional null algebra | pass conditional | `delta O_1=0`, `delta O_2!=0` if zero marginal holds |
| metric/clock exclusion | mandatory condition written | `delta g=delta z=delta u=0` |
| BAO pair operator | conditional pass | only live route preserving SN/H(z) null |
| parent action owner | fail open | no action/effective action derives `K` |
| locality | open risk | bilocality must be derived coarse-grained, not arbitrary |
| lensing/growth safety | open | two-point observables must be tested |
| CMB `r_d` safety | open mandatory | late-ruler or Boltzmann derivation required |
| promotion | fail | no bridge/local-GR/CMB claim |

## 9. Decision

Current fair status:

```text
pair_ruler_null_response_contract_conditional_bilocal_operator_not_parent_derived
```

Meaning:

```text
the trace/quadrupole ruler route survives the null-response logic gate only as
a conditional bilocal effective operator;
metric, clock, and one-point coframe routes are rejected for this branch;
the parent derivation is now the main blocker.
```

Boxing-card readout:

```text
We found the legal punch.
It has to be a connected pair shot with no one-point follow-through.
If it turns into a metric or clock punch, SN gets hit and the round is lost.
```

## 10. Next Target

Create:

```text
163-effective-pair-action-owner-attempt.md
```

Task:

```text
try to derive K^A_B and the zero one-point marginal from a coarse-grained
effective action, connected cumulant, or conserved pair current.
```

Pass condition:

```text
the bilocal pair kernel emerges from parent variables with a zero marginal,
source laws from checkpoint 161, zero-memory/local-silence limits, and no
metric/clock deformation.
```

Fail condition:

```text
K^A_B can only be inserted as a BAO-only effective likelihood correction.
```
