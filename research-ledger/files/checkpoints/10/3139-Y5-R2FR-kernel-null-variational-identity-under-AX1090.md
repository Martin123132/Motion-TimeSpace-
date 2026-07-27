# 3139 - Kernel-Null Variational Identity under AX1090

Private checkpoint. This follows 3138 by attacking the hardest clause directly:

```text
if v in ker(Dq), why should v be physically null rather than a hidden force?
```

## Result

3139 derives the exact conditional identity needed for the local-GR route:

```text
basic parent action
+ descending presymplectic potential
+ silent local boundary charge
+ matter/source descent
=> ker(Dq) is null for local readouts.
```

In more explicit form, for a parent Lagrangian n-form:

```text
delta L_parent = E_i delta Phi^i + d Theta_parent(delta Phi)
```

if:

```text
L_parent = q^* Lbar(Q_obs) + dB
Theta_parent(delta Phi) = q^* Thetabar(Dq delta Phi) + d beta(delta Phi)
v in ker(Dq)
```

then:

```text
Theta_parent(v) = d beta(v)
omega_parent(v,delta) = d Xi_v(delta)
Omega_Sigma(v,delta) = int_boundarySigma Xi_v(delta).
```

So if the compact local boundary term vanishes:

```text
int_boundarySigma Xi_v(delta) = 0
```

then:

```text
Omega_Sigma(v,delta) = 0.
```

That is the clean kernel-null theorem shape.

## What Actually Closes

The following mathematical reduction is now exact:

| step | result |
|---|---|
| `Dq[v]=0` | quotient-owned bulk terms do not vary along `v` |
| `L_parent=q^*Lbar+dB` | bulk parent action is basic over `Q_obs` |
| `Theta=q^*Thetabar+d beta` | presymplectic pairing with `v` is boundary-exact |
| compact boundary silence | local charge of `v` vanishes |
| matter descent through `Rep(Q_obs)` | clocks/masses/alpha do not see `v` |
| source descent through `Range(Dq)^*` | source current does not pair with `v` |

So the work is no longer saying:

```text
maybe the hidden direction is gauge.
```

It is saying:

```text
the hidden direction is gauge/null if and only if these concrete variational descent clauses are parent-owned.
```

That is a real derivation ladder.

## What Still Does Not Close

The current corpus does not yet parent-sign the premises:

| premise | current status |
|---|---|
| parent-owned `q: Phi_parent -> Q_obs` | `candidate_written_not_parent_signed` |
| basic action `L_parent=q^*Lbar+dB` | `conditional_identity_not_parent_signed` |
| presymplectic potential descent | `not_parent_signed` |
| compact boundary/no-edge silence | `conditional_for_proper_variations_not_measured_edges` |
| ordinary matter descent to `Rep(Q_obs)` | `conditional_theorem_not_parent_signed` |
| source descent and label forgetting | `conditional_countermodel_retained` |
| no Weyl/disformal frame transfer | `not_parent_signed` |
| total kernel-null ownership | `not_claim_ready` |

Therefore:

```text
local GR/Newton/PPN reduction is still not claimed.
```

But the blocker has been sharpened. The core missing object is now:

```text
Theta_parent(delta Phi) = q^* Thetabar(Dq delta Phi) + d beta(delta Phi)
```

plus local boundary silence.

## Countermodels Still Alive

The following branches still break kernel-null if the parent allows them:

| countermodel | effect |
|---|---|
| `A(X) R[e_obs]` | hidden representative changes the EH prefactor |
| boundary charge `int_boundary Q_v` | representative direction has a measured edge/source charge |
| `theta_A=theta_A(marker,X)` | clock/mass/alpha constants vary along the hidden direction |
| disformal matter frame | matter sees a frame different from `e_obs` |
| species-labelled source functor | source coupling keeps labels not erased by `q` |
| non-Hilbert current | source current pairs directly with the hidden direction |

These are not philosophical objections; they are the exact ways the theorem can fail.

## Clock/Time Readout Consequence

This is why the earlier internal-time thought is not automatically fatal:

```text
internal flow/time may behave unlike observed GR clock time
```

provided:

```text
the internal direction lies in ker(Dq),
the presymplectic/matter/source pairings vanish,
and observed clocks are read through e_obs and Rep(Q_obs).
```

So the sign/readout fork is now technical, not emotional:

```text
does the parent action make the internal direction variationally null?
```

If yes, the odd internal variable is gauge/readout scaffolding. If no, it becomes a physical residual and must be bounded.

## Claim Gate

| gate | status |
|---|---|
| formal variational identity | `pass_conditional_theorem_shape` |
| all kernel premises parent-signed | `fail_for_claim` |
| countermodels closed | `fail_for_claim` |
| local GR/Newton/PPN kernel claim | `not_claim_ready` |

## Why This Matters

This is one of the cleaner steps toward GR reduction so far.

Before 3139, the kernel-null demand was broad:

```text
prove ker(Dq) is null.
```

After 3139, the demand is local and attackable:

```text
prove presymplectic-potential descent and boundary silence for the typed Q_obs quotient.
```

That is exactly the Grossmann-style job: not declaring victory, but finding the right geometric condition that would make the victory legitimate.

## Runner Artifacts

| artifact | path |
|---|---|
| inputs | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3139_INPUTS.csv` |
| variational identity | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3139_KERNEL_NULL_VARIATIONAL_IDENTITY.csv` |
| premise audit | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3139_PREMISE_OWNERSHIP_AUDIT.csv` |
| countermodel stress test | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3139_COUNTERMODEL_STRESS_TEST.csv` |
| decision ledger | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3139_REDUCTION_DECISION.csv` |
| gate | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3139_GATE.csv` |
| validation | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_3139_VALIDATION.csv` |
| runner | `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\scripts\Y5_R2FR_3139_kernel_null_variational_identity.py` |

## Next Target

The best next route is:

```text
3140:
try to derive presymplectic-potential descent for the typed Q_obs construction.
```

Specifically, try to show:

```text
Theta_parent(delta Phi) - q^* Thetabar(Dq delta Phi) = d beta(delta Phi)
```

from the topological/projector quotient machinery.

If that fails, do not keep circling the same broad local-GR gate. Switch to the narrower EM/Poynting route:

```text
unique Maxwell F^2 + charge lattice inheritance + Hilbert stress/source owner.
```

That narrower route would directly attack `b_alpha`, EM stress, Poynting-vector readout, and one piece of the coupling problem.
