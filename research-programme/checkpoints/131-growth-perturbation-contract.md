# 131 - Growth Perturbation Contract

Private theorem-target contract. This is not a public claim.

## 1. Trigger

Checkpoint 130 gave a useful empirical fact:

```text
The locked B_mem = 2/27 background survives the first SDSS/eBOSS growth gate.
```

But it also exposed the real bottleneck:

```text
The growth equation used in checkpoint 130 was the GR background-growth proxy,
not a derived MTS perturbation sector.
```

So the next job is not to celebrate the score.

The next job is to define the exact contract a parent perturbation theory must satisfy.

## 2. Required Background Limit

The perturbation sector must reduce to the locked background already being tested:

```text
E^2(a) = Omega_m0 a^-3 + 1 - Omega_m0 + B_mem A(a)
```

with:

```text
B_mem = 2/27
p = 3
u3 = 1/4
A(a) = 1 - exp[-((-ln a)/u3)^p]
```

where:

```text
a = 1 / (1 + z)
```

This is the current locked empirical branch.

The contract does not allow a different growth background unless it first reproduces the SN+BAO, BAO-only, BAO+H(z), and growth gate scores already obtained.

## 3. Minimum Field Content

A future parent perturbation action must name the fields that own the background term.

Minimal acceptable field ledger:

| Object | Role | Status Required |
|---|---|---|
| `g_mu_nu` | spacetime metric | fundamental |
| `T_m^{mu nu}` | ordinary matter stress tensor | separately conserved or explicitly exchange-coupled |
| `U_mem` or equivalent | memory/background sector | owner of `B_mem A(a)` |
| `delta U_mem` or constrained absence thereof | perturbation of memory sector | derived, not guessed |
| `Phi`, `Psi` | scalar metric potentials | gauge-fixed perturbation variables |
| `delta_m`, `theta_m` | matter density and velocity perturbations | observable growth variables |

The key fork:

```text
Either the memory sector has perturbations, or it is proven non-clustering.
```

Both are allowed as theorem routes.

Neither may be assumed without derivation.

## 4. Conservation Contract

The parent equations must satisfy:

```text
nabla_mu [T_m^{mu nu} + T_mem^{mu nu}] = 0
```

Then one of these must be selected:

### Route A: Separately Conserved Matter

```text
nabla_mu T_m^{mu nu} = 0
nabla_mu T_mem^{mu nu} = 0
```

This is the safest local-GR route.

It preserves standard matter geodesic motion and keeps the growth equation close to GR unless the memory stress clusters gravitationally.

### Route B: Controlled Exchange

```text
nabla_mu T_m^{mu nu} = Q^nu
nabla_mu T_mem^{mu nu} = -Q^nu
```

This route is allowed only if:

```text
Q^nu -> 0 in local/PPN regimes
Q^nu has a covariant parent expression
Q^nu does not introduce a fitted growth fudge
Q^nu preserves background results already tested
```

If `Q^nu` is introduced only to fix growth data, the route fails.

## 5. Perturbation Equation Target

In the quasi-static scalar sector, the derived matter growth equation should take the form:

```text
D'' + [2 + d ln H / d ln a + F_fric(a,k)] D'
    - (3/2) mu(a,k) Omega_m(a) D = S_mem(a,k)
```

where prime means:

```text
d / d ln a
```

GR is recovered when:

```text
F_fric(a,k) -> 0
mu(a,k) -> 1
S_mem(a,k) -> 0
```

The checkpoint-130 proxy corresponds to:

```text
F_fric = 0
mu = 1
S_mem = 0
```

on the locked MTS background.

The theorem task is to derive whether that proxy is actually justified.

## 6. Acceptable Theorem Outcomes

There are three acceptable outcomes.

### Outcome 1: Smooth Memory Theorem

Prove:

```text
delta U_mem = 0 or negligible for SDSS/eBOSS linear growth modes
```

Then the checkpoint-130 GR-growth proxy becomes a derived first approximation.

Required proof ingredients:

```text
memory sector has no propagating scalar mode in the relevant regime
or memory perturbations have a large effective mass
or memory perturbations are constrained algebraically to remain smooth
```

This is the cleanest route if it works.

### Outcome 2: Controlled Modified Growth

Derive nonzero:

```text
F_fric(a,k)
mu(a,k)
S_mem(a,k)
```

but with:

```text
mu -> 1 when B_mem -> 0
mu -> 1 on local/PPN scales
no arbitrary fitted amplitude
no arbitrary fitted transition scale
```

This route can improve the theory, but it is dangerous because it can easily become a phenomenological patch.

### Outcome 3: Closure-Only Demotion

If neither smooth memory nor controlled modified growth can be derived, then the growth result remains:

```text
conditional empirical closure only
```

That is still useful, but it cannot be promoted as fundamental field theory.

## 7. No-Fudge Rules

Forbidden moves:

```text
fit a free mu_0 growth amplitude after seeing f_sigma8
fit a free Sigma_0 lensing amplitude after seeing data
fit a free k_screen to save one dataset
give MTS a different sigma8 freedom from LCDM/wCDM/CPL
use CMB priors while calling the result no-CMB
interpret BAO+FS geometry improvement as pure growth proof
ignore the RSD-only draw
```

Allowed moves:

```text
derive a memory sound speed from the action
derive an effective mass from the action
derive a constraint equation that removes delta U_mem
use one shared sigma8_0 nuisance exactly as in checkpoint 130
test the derived equation on the same SDSS/eBOSS files
```

## 8. Local-GR and PPN Locks

The perturbation route must not damage the local branch.

Required local limits:

```text
Phi = Psi + negligible slip
G_eff / G -> 1
Q^nu -> 0 if exchange exists
memory perturbation force -> 0
```

in:

```text
Solar-System / local weak-field systems
orbital systems
laboratory clock/EM regimes
```

This means any scale-dependent growth modification must satisfy:

```text
lim_{local/high-density/PPN} mu(a,k) = 1
lim_{local/high-density/PPN} eta_slip(a,k) = 1
```

without inserting a plateau axiom by hand.

## 9. Observable Contract

The theory must predict:

```text
f_sigma8(z) = sigma8_0 f(z) D(z)
```

with:

```text
D(a=1) = 1
f = d ln D / d ln a
```

The interpretation must keep these branches separate:

| Branch | Meaning |
|---|---|
| BAO+FS all rows | geometry plus growth stress |
| RSD-only rows | growth-amplitude stress |
| full-shape transfer | robustness after sigma8_0 is fitted elsewhere |

Checkpoint 130 found:

```text
BAO+FS all rows: locked MTS preferred vs LCDM
RSD-only: competitive draw
full-shape transfer: competitive draw
```

Therefore:

```text
Do not claim pure growth evidence from the BAO+FS all-row result.
Do claim that growth does not currently kill the locked branch.
```

## 10. CMB Boundary

This contract does not solve CMB.

A CMB perturbation claim needs a separate Boltzmann-level contract:

```text
early-time limit
radiation perturbations
baryon-photon coupling
lensing potential
ISW contribution
sound horizon consistency
matter power spectrum transfer function
```

Until then:

```text
compressed CMB priors remain stress tests only
checkpoint-130 growth is late-time only
```

## 11. Acceptance Gates

A candidate perturbation derivation passes the first gate only if:

```text
1. It reproduces the locked background.
2. It derives matter conservation or controlled exchange.
3. It reduces to GR when B_mem -> 0.
4. It keeps local-GR / PPN limits intact.
5. It gives f_sigma8(z) without extra MTS-only nuisance freedom.
6. It reruns checkpoint-130 data with no worse-than-LCDM penalty greater than 2.
7. It reports BAO+FS, RSD-only, and full-shape-transfer branches separately.
8. It keeps MTS_Bmem_zero = LCDM as a negative control.
```

Promotion rule:

```text
Only after these gates pass can the growth sector be called a serious derived
piece of the field theory.
```

## 12. Next Work Order

Recommended next file:

```text
132-smooth-memory-growth-theorem-attempt.md
```

First theorem attempt:

```text
Try to prove the smooth memory theorem.
```

Target statement:

```text
For linear late-time matter perturbations on SDSS/eBOSS scales, the memory
sector that produces B_mem A(a) contributes to the homogeneous background but
does not introduce an independent clustering scalar at leading order.
```

If this works:

```text
checkpoint 130 becomes more than a proxy; it becomes the first derived
late-time growth approximation.
```

If it fails:

```text
derive a controlled mu(a,k), friction, or source term;
otherwise demote growth to empirical closure-only.
```
