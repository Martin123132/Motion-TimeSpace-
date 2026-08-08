# 3138 - Qobs, Obs_e, and Rep(Qobs) Construction under AX1090

Private checkpoint. This follows 3137 by taking Door A:

```text
construct q -> Obs_e -> Rep(Q_obs)
```

instead of merely saying that quotient ownership is missing.

## Result

3138 builds the typed local readout chain:

```text
Phi_parent --q--> Q_obs --Obs_e--> e_obs
                     |
                     v
                  Rep(Q_obs)
```

with:

```text
Q_obs = (
  M,
  e_obs mod local Lorentz,
  omega_obs if owned,
  [C]_PD,
  Orbit_27(h),
  [J_rel]_local,
  boundary_class,
  Rep_labels
)
```

and:

```text
Obs_e(Q_obs) = e_obs up to local Lorentz gauge.
```

This gives 3137 a real home for the statement:

```text
theta_A in Rep(Q_obs).
```

The construction is coherent. It is not yet parent-owned. No local-GR, Newton, PPN, clock, source-coupling, or EM claim is made.

## What Actually Moves Forward

The previous chain had the right theorem target:

```text
theta_A fixed as quotient representation labels
=> Lie_v theta_A = 0
```

but the object carrying those labels had not been made explicit. 3138 now writes the actual candidate:

| object | role |
|---|---|
| `Phi_parent` | parent configuration before quotient |
| `q: Phi_parent -> Q_obs` | candidate map that forgets representative/internal data |
| `Q_obs` | typed observable quotient object |
| `Obs_e: Q_obs -> Coframe/Lorentz` | observed coframe readout |
| `Rep(Q_obs)` | ordinary matter representation category over the quotient |
| `S_matter over Rep(Q_obs)` | matter action descent target |
| `F_src over Q_obs` | source-current readout target |

This is useful because it turns a vague closure demand into a specific mathematical contract:

```text
ordinary clocks, masses, charge labels, and source weights must live over Rep(Q_obs),
not over the hidden representative fibre.
```

## Clock/Flow Interpretation

This checkpoint keeps the important distinction from 3135-3137:

```text
internal flow time != observed material clock time
```

An internal motion/time variable is allowed to have a non-GR-looking sign or monotonicity until it leaks into:

```text
e_obs,
g_obs,
clock transition constants,
mass standards,
alpha_EM,
source weights,
or measured redshift/PPN observables.
```

So a branch is not rejected merely because the hidden flow variable behaves oddly. It is rejected only if the readout chain cannot recover the observed GR/SR clock functional.

## What Still Fails For Claim

The 3138 certificate deliberately fails the claim gate. The missing parent signatures are:

| certificate | current status |
|---|---|
| `ker(Dq)` presymplectic-null | `failed_current_corpus` |
| `e_obs` not just inserted by hand | `open_guard_active` |
| unique matter-visible coframe functor | `conditional_not_signed` |
| `theta_A` fixed as representation labels | `conditional_not_signed` |
| ordinary matter action descends to `Rep(Q_obs)` | `conditional_not_signed` |
| source functor forgets species labels | `conditional_countermodel_retained` |
| vertical variations have no boundary/source tail | `not_signed` |
| total parent ownership | `not_claim_ready` |

The central trap remains:

```text
putting e_obs inside Q_obs is not a derivation.
```

To become a derivation, the parent action must show that the hidden representative directions are physically null or gauge-like for matter and sources.

## Residual Fallback Rows

If the parent proof does not close, the following finite residual rows stay active:

| residual | meaning |
|---|---|
| `c_g/b_g` | representative Weyl/common-frame leakage |
| `b_dis` | representative disformal matter-frame leakage |
| `b_clock` | material clock transition derivative |
| `b_alpha` | alpha_EM derivative if EM-lock fails |
| `Delta_kappa_AB` | relative species source-weight difference |
| `q_nonH` | non-Hilbert or boundary source projection |
| `Delta_W_support` | source support shift under observed frame choices |

No cancellation between these rows is allowed without a parent theorem or a sourced bound.

## Claim Gate

| gate | status |
|---|---|
| typed construction | `typed_candidate_written` |
| parent ownership | `fail_for_claim` |
| residual fallback | `active_nonclaim` |
| local GR/Newton/clock/source readout | `not_claim_ready` |

## Why This Matters

3138 is not another missing-list checkpoint. It is the skeleton of the readout map:

```text
hidden MTS parent variables
-> quotient observable object
-> observed coframe/metric
-> matter representations
-> clocks, masses, charge labels, sources
```

That is exactly the place where a deeper motion/time structure can be allowed to exist without instantly contradicting GR. The observed theory only has to match GR after the `Obs_e` and `Rep(Q_obs)` readout.

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3138_QOBS_REP_INPUTS.csv` |
| typed construction | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3138_TYPED_QOBS_CONSTRUCTION.csv` |
| certificate matrix | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3138_REP_QOBS_CERTIFICATE_MATRIX.csv` |
| fallback rows | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3138_QOBS_REP_FALLBACK_ROWS.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3138_GATE.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3138_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3138_qobs_representations_construction.py` |

## Next Target

The best next target is:

```text
3139:
try to prove the kernel-null clause for the typed Q_obs construction,
or reduce it to a smaller owned variational identity.
```

That is the route which most directly helps local GR/Newton, because if:

```text
v in ker(Dq)
```

is parent-null for the action, symplectic form, boundary flux, matter functor, and source readout, then the hidden representative direction becomes a genuine gauge/quotient direction rather than an extra force.

If that route stalls, the best narrower attack is the EM/Poynting door:

```text
unique Maxwell F^2 + charge lattice inheritance + stress/source current owner.
```

That would directly target `b_alpha`, Poynting-vector readout, and EM stress consistency.
