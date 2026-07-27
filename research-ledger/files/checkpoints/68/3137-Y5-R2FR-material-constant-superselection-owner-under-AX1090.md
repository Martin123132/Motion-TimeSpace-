# 3137 - Material Constant Superselection Owner under AX1090

Private checkpoint. This follows 3136 by attacking the next missing clause:

```text
why should material clock constants, masses, and alpha_EM be silent under the internal/representative direction?
```

## Result

The clean zero route is now exact:

```text
theta_A in Rep(Q_obs)
v in ker(Dq)
theta_A not a parent field and not marker-indexed
=> Lie_v theta_A = 0.
```

If the parent action signs that ordinary material constants are fixed representation/superselection labels of the quotient matter bundle, then:

```text
b_clock = 0
b_mass  = 0
```

and if EM-lock also signs charge lattice, unique Maxwell `F^2`, current owner, and readout descent:

```text
b_alpha = 0.
```

This is not a claim yet. It is the sharp theorem route.

## What Actually Closes

The formal chain is valid:

```text
S_matter = Sbar_matter[q(Phi), Psi_A, theta_A]
Dq[v] = 0
Lie_v theta_A = 0
```

implies:

```text
Lie_v S_matter = 0.
```

For clocks:

```text
nu_A = nu_A(theta_A, e_obs local tetrad)
Lie_v nu_A = 0
```

if:

```text
Lie_v theta_A = 0
Lie_v e_obs = 0.
```

So 3136’s clock theorem becomes much stronger if 3137’s representation-label clause is parent-signed.

## What Still Fails For Claim

The current corpus still does not parent-sign:

```text
Rep(Q_obs) construction,
no marker-indexed representation choice,
constant-sector universality,
charge lattice / unique Maxwell F2,
source-domain label forgetting,
one parent branch containing all of the above.
```

The active countermodels are still legal:

```text
theta_A = theta_A(marker, Xhat)
m_A = m_A(marker, Xhat)
alpha_EM = alpha_EM(Xhat)
F_src({(T_A,A)}) = sum_A kappa_A T_A.
```

Metric/coframe descent alone does not kill those. That is the key no-cheat lesson.

## Residual Fallback

If the zero route does not close, the retained rows are:

| residual | meaning |
|---|---|
| `b_clock` | material clock transition derivative |
| `b_mass` | mass-standard derivative |
| `b_alpha` | fine-structure/EM-coupling derivative |
| `beta_source_alpha` | WEP alpha/Coulomb source-force normalization |
| `kappa_alpha_tau_clock_time` | alpha-sensitive clock product |
| `Delta_kappa_AB` | relative species source weight if labels survive |

These are not allowed to cancel each other unless a parent theorem or sourced bound says so.

## Claim Gate

| gate | status |
|---|---|
| `b_clock,b_mass` zero | `formal_pass_conditional_not_parent_signed` |
| `b_alpha` zero | `conditional_exact_but_EM_lock_unsigned` |
| no relative source weights | `conditional_theorem_countermodel_retained` |
| clock constants parent ownership | `not_claim_ready` |

## Why This Matters

This narrows the local-GR clock route. We no longer have the vague statement:

```text
constants must not vary.
```

We have the actual mathematical demand:

```text
ordinary material constants must be fixed representation labels of the quotient observed matter category.
```

That is a much more respectable field-theory target. It is also harder to smuggle, because if a material label survives as source-functor data, the countermodel immediately reopens WEP/clock/source residuals.

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3137_CONSTANT_STANDARD_INPUTS.csv` |
| theorem | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3137_MATERIAL_STANDARD_SUPERSELECTION_THEOREM.csv` |
| reduction | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3137_REPRESENTATION_LABEL_REDUCTION.csv` |
| fallback rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3137_CONSTANT_STANDARD_RESIDUAL_FALLBACK.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3137_GATE.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3137_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3137_material_constant_superselection_owner.py` |

## Next Target

3138 should attack one of two doors:

```text
Door A:
construct q -> Obs_e -> Rep(Q_obs) explicitly enough that theta_A are fixed quotient representation labels.
```

or:

```text
Door B:
attack unique Maxwell F2 / charge lattice inheritance, because that is the cleanest b_alpha zero route.
```

Door A is broader and helps clocks, WEP, and source normalization. Door B is narrower but directly helps EM/Poynting and alpha.

