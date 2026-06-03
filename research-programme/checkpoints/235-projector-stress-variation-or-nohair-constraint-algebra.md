# 235 - Projector Stress Variation or Nohair Constraint Algebra

Private local-derivation checkpoint. This is not a public local-GR, PPN,
clock, WEP, or field-theory completion claim.

## 1. Trigger

Checkpoint 234 fenced the stress problem:

```text
no projector without projector stress.
```

The next target was:

```text
either compute/structure delta P_mem / delta g_mu_nu,
or attack the X/J_rel/V_def no-hair constraint algebra.
```

This checkpoint does both at condition level.

## 2. Machine Artifact

Script:

```text
scripts/projector_stress_variation_or_nohair_constraint_algebra.py
```

Run:

```text
runs/20260601-000052-projector-stress-variation-or-nohair-constraint-algebra
```

Command:

```text
python scripts/projector_stress_variation_or_nohair_constraint_algebra.py --timestamp 20260601-000052
```

Status:

```text
projector_variation_safe_branch_conditions_written_X_nohair_rank_test_not_derived_no_promotion
```

Claim ceiling:

```text
projector_stress_variation_conditions_no_nohair_or_PPN_promotion
```

## 3. Projector Variation

For the candidate boundary metric:

```text
S_proj = (1/2)<J, P_mem J>_B.
```

Metric variation gives:

```text
delta_g S_proj =
(1/2)<J, delta_g B P_mem J>
+ (1/2)<J, B delta_g P_mem J>
+ source variations.
```

The projector split is:

```text
P_mem = 1 - Pi_M - Pi_TF - Pi_matter.
```

Therefore:

```text
delta P_mem =
- delta Pi_M
- delta Pi_TF
- delta Pi_matter.
```

So projector stress is safe only if every removed block has an owned
destination.

## 4. Safe Branch Conditions

The safe local branch now requires:

| condition | requirement | protects |
|---|---|---|
| `C1` | `M_eff` is conserved monopole, not radial memory hair | `G_eff`, `beta` |
| `C2` | `Pi_TF` vanishes by scalar boundary symmetry | `gamma`, `Phi-Psi` |
| `C3` | `Pi_matter` absent by universal metric coupling | clocks, WEP |
| `C4` | relative memory current exact with pure-gauge boundary primitive | `q_loc` |
| `C5` | `X/J_rel/V_def` carry no exterior propagating hair | beta, fifth-force safety |
| `C6` | all projector metric variations are included or vanish by `C1-C5` | Bianchi |

This is stricter than before.

It says:

```text
P_mem is allowed only if its stress is either explicitly carried
or killed by the same theorem conditions that define the projector.
```

## 5. Nohair Constraint Algebra

The no-hair route is now:

```text
pi_X^nu ~= 0
```

as a primary constraint, and:

```text
C_X^nu =
-nabla_mu P[Y]^{mu nu}
+ S_L^nu
+ d_rel(P_mem J_rel)^nu
~= 0
```

as the secondary constraint.

The necessary tests are:

```text
rank Hessian(dot X,dot X) = 0,
{C_X^nu(x), C_X^rho(y)} closes on parent constraints,
B_X^nu = n_mu P^{mu nu},
A_rel|boundary = pure gauge,
P[Y] and P_mem are parent-owned composites.
```

If these hold, `X` is a multiplier rather than a fifth-force field.

But the bracket closure is not computed because the parent symplectic
structure is still missing.

## 6. What Improved

Before this checkpoint:

```text
T_projector was listed as required.
```

After this checkpoint:

```text
T_projector has explicit vanishing/cancellation conditions:
delta Pi_M -> M_eff,
delta Pi_TF -> zero or explicit anisotropic stress,
delta Pi_matter -> forbidden direct coupling,
delta relative Hodge -> boundary/relative cancellation.
```

That is a genuine tightening.

It is not yet a parent variation.

## 7. Gate Results

| gate | result |
|---|---|
| all cited local sources exist | pass |
| `delta P_mem` variation split written | pass |
| safe branch conditions listed | pass |
| `X` no-hair rank/bracket tests written | pass |
| beta gate sharpened | pass |
| `T_projector` derived or shown to vanish | fail |
| `X/J_rel/V_def` no-hair derived | fail |
| local GR or PPN promoted | fail |

The pass rows are footwork.

The fail rows are the judges not awarding the round yet.

## 8. Decision

Decision:

```text
projector_variation_safe_branch_conditions_written_X_nohair_rank_test_not_derived_no_promotion
```

Meaning:

```text
the projector-stress problem is now structured. delta P_mem splits into mass,
trace-free, matter-coupling, and relative-memory variations, each with a named
safe condition. The X no-hair route is also reduced to primary/secondary
constraints, bracket closure, boundary primitive, and rank-count tests.
```

Main gain:

```text
hidden projector stress has explicit vanishing/cancellation conditions.
```

Main failure:

```text
the parent variation and X/J_rel/V_def no-hair proof are still missing.
```

## 9. Next Target

Create:

```text
236-local-EH-operator-or-constraint-algebra-decision.md
```

Purpose:

```text
decide whether to attack the local Einstein-Hilbert exterior operator next,
or continue trying to compute the X/P_mem constraint algebra.
```

Pass condition:

```text
metric-only two-derivative exterior action reduces to Einstein-Hilbert,
```

or:

```text
the X/P_mem constraint algebra closes without exterior hair.
```

Fail condition:

```text
the local branch is treated as GR because the stress conditions are named.
```
