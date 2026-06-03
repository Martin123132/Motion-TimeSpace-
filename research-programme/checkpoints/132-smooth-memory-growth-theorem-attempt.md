# 132 - Smooth Memory Growth Theorem Attempt

Private theorem attempt. This is not a public claim.

## 1. Trigger

Checkpoint 131 set the next target:

```text
Try to prove the smooth memory theorem.
```

Target statement:

```text
For linear late-time matter perturbations on SDSS/eBOSS scales, the memory
sector that produces B_mem A(a) contributes to the homogeneous background but
does not introduce an independent clustering scalar at leading order.
```

This checkpoint asks whether that can be derived, not assumed.

## 2. Machine Artifact

Script:

```text
research-programme\scripts\smooth_memory_growth_theorem_attempt.py
```

Run:

```text
research-programme\runs\20260531-184700-smooth-memory-growth-theorem-attempt
```

Generated:

```text
source_register.csv
locked_effective_fluid.csv
linear_smoothness_conditions.csv
growth_proxy_terms.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
smooth_memory_theorem_conditional_not_derived
```

Claim ceiling:

```text
smooth_memory_theorem_attempt_conditional_only
```

## 3. Background Being Tested

The locked background is:

```text
E^2(a) = Omega_m0 a^-3 + 1 - Omega_m0 + B_mem A(a)
```

with:

```text
B_mem = 2/27
p = 3
u3 = 1/4
A(a) = 1 - exp[-((-ln a)/u3)^3]
```

The checkpoint-130 DR2 no-CMB primary background gives:

```text
Omega_m0 = 0.3042725199400447
H0 = 67.50994528839665
BAO alpha = 30.034792746095537
inferred r_d = 147.85237578643267
```

## 4. Effective Smooth Fluid Readout

If the memory background is treated as a separately conserved smooth effective sector:

```text
rho_mem / rho_crit0 = 1 - Omega_m0 + B_mem A(N)
N = ln(1+z)
```

then:

```text
w_mem(N) = -1 + B_mem A_N / [3 rho_mem]
```

Key values:

| z | A_mem | dA/dN | w_mem |
|---:|---:|---:|---:|
| `0.0` | `0.0` | `0.0` | `-1.0` |
| `0.15` | `0.16030929561082197` | `3.1491868522733713` | `-0.8901110039715496` |
| `0.38` | `0.8821547019831165` | `2.347201853032448` | `-0.9238500686781729` |
| `0.51` | `0.9886596073561769` | `0.3697897681206578` | `-0.9881260488517351` |
| `0.698` | `0.9999250398772931` | `0.004034439502822785` | `-0.9998705945107994` |
| `1.48` | `1.0` | `2.367813192861715e-19` | `-1.0` |

Interpretation:

```text
the memory sector behaves like a smooth transient dark-energy-like background,
with w close to -1 except around the activation transition.
```

This is not enough by itself.

A smooth background is not automatically a non-clustering perturbation sector.

## 5. The Useful Cancellation

The best result is a real first-order cancellation in the coherence invariant.

Prior checkpoints use:

```text
C_coh =
<theta>_D^2 /
(<theta^2>_D + <sigma^2>_D + <omega^2>_D + eps_D)
```

For an FLRW background:

```text
theta = theta0
sigma = 0
omega = 0
eps_D = 0 or negligible
C_coh = 1
```

Now perturb:

```text
theta = theta0 + epsilon delta theta
sigma = O(epsilon)
omega = O(epsilon)
```

Then:

```text
<theta>_D^2
= theta0^2 + 2 epsilon theta0 <delta theta>_D + O(epsilon^2)
```

and:

```text
<theta^2>_D
= theta0^2 + 2 epsilon theta0 <delta theta>_D + O(epsilon^2)
```

while:

```text
<sigma^2>_D = O(epsilon^2)
<omega^2>_D = O(epsilon^2)
```

Therefore:

```text
C_coh = 1 + O(epsilon^2)
```

and:

```text
delta C_coh^(1) = 0
```

This is stronger than needing the perturbation average to vanish.

The same linear term appears in numerator and denominator and cancels.

## 6. Conditional Smooth Memory Lemma

The conditional lemma is:

```text
If chi_D is an auxiliary constrained selector with chi_D = C_coh,
and if the memory exposure I_M is a coherent-domain/global invariant rather
than a local propagating scalar,
then FLRW linear perturbations do not source an independent local memory
clustering scalar through C_coh at first order.
```

Symbolically:

```text
delta chi_D^(1) = delta C_coh^(1) = 0
```

and conditionally:

```text
delta I_M^(1) = 0
```

for non-boundary coherent-domain perturbations.

This gives a non-cheating route to:

```text
delta rho_mem = 0
delta p_mem = 0
theta_mem = 0
pi_mem = 0
```

at leading quasi-static order.

But this final stress statement is still conditional because `S_stress` has not been varied.

## 7. Growth Proxy Implication

Checkpoint 130 used:

```text
F_fric = 0
mu = 1
S_mem = 0
eta_slip = 1
```

The smooth-memory route can conditionally justify these:

| Term | Conditional reason | Status |
|---|---|---|
| `F_fric = 0` | no independent memory momentum perturbation; matter remains separately conserved | conditionally allowed |
| `mu = 1` | no memory density perturbation enters subhorizon Poisson equation | conditionally allowed |
| `S_mem = 0` | memory perturbation is constrained away or second-order in `C_coh` | conditionally allowed |
| `eta_slip = 1` | no memory anisotropic stress | open, not derived |

So:

```text
checkpoint 130 is no longer a random proxy.
```

It is now a conditional theorem target with a real first-order cancellation behind it.

But:

```text
it is still not promoted to a derived perturbation theory.
```

## 8. Gates

Gate results:

| Gate | Status | Evidence |
|---|---|---|
| `linear_Ccoh_cancellation` | pass conditional | `dCcoh/depsilon` vanishes at FLRW linear order when `eps_D` is not a first-order source |
| `auxiliary_nonpropagating_selector` | pass contract | prior checkpoints allow `chi_D` as auxiliary/constrained, not propagating |
| `memory_density_perturbation_removed` | open conditional | requires `S_stress` and gauge-invariant stress perturbation derivation |
| `Bianchi_conservation` | fail not derived | boundary exchange/current and total stress owner remain open |
| `GR_growth_proxy_promoted` | fail | smooth memory theorem is conditional, not action-derived |
| `support_claim_allowed` | fail | conditional theorem target only |

## 9. Why This Is Better Than a Plateau Axiom

The old bad move would be:

```text
assume memory does not cluster because we need growth to work.
```

This checkpoint does something sharper:

```text
the specific coherence invariant already used for local/FLRW gating has no
linear perturbation around the FLRW bulk branch.
```

That means smoothness is not pure wishful thinking.

It follows from the structure:

```text
C_coh = <theta>^2 / <theta^2 + shear^2 + vorticity^2>
```

because scalar expansion perturbations enter the numerator and denominator in the same way at first order.

Boxing-score version:

```text
We did not land the knockout theorem.
But we found a real defensive slip: the first-order coherence perturbation
throws a punch and hits air.
```

## 10. Remaining Blockers

The theorem is not promoted because these are still missing:

```text
S_stress perturbation variation
gauge-invariant statement of delta rho_mem = 0
total Bianchi identity
boundary exchange current
Q_coh parent field derivation
relative-current representative selection
```

The most important subtlety is gauge:

```text
a homogeneous time-dependent memory density can look perturbed under a time
slicing change.
```

So the final theorem must specify either:

```text
memory-comoving/unitary gauge with no physical scalar mode
```

or a gauge-invariant variable proving:

```text
delta rho_mem^GI = 0 or subhorizon-suppressed.
```

Without that, `delta rho_mem = 0` is not a complete perturbation statement.

## 11. Decision

Decision:

```text
smooth_memory_theorem_status =
conditional_not_derived
```

Meaning:

```text
the smooth-memory route is now a strong theorem target;
the checkpoint-130 growth proxy is conditionally supported;
the missing step is the memory stress/gauge/Bianchi owner.
```

Do not demote the growth branch.

Do not promote it as derived.

Use the result as:

```text
evidence that the growth route deserves a proper parent perturbation attempt.
```

## 12. Next Target

Create:

```text
133-memory-stress-perturbation-owner-attempt.md
```

Purpose:

```text
vary the missing memory stress owner and decide whether the conditional smooth
lemma becomes a real theorem or collapses into closure-only.
```

Pass condition:

```text
derive a stress tensor whose linear scalar perturbations vanish, or are
subhorizon-suppressed, while its background reproduces B_mem A(a).
```

Fail condition:

```text
the memory stress necessarily carries a clustering scalar, anisotropic stress,
or uncontrolled exchange current.
```

If it fails, the next fork is:

```text
derive controlled modified growth terms F_fric, mu, or S_mem;
otherwise demote growth to empirical closure-only.
```
