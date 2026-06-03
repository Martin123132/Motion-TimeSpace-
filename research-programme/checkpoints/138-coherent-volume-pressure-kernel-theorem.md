# 138 - Coherent Volume Pressure Kernel Theorem

Private theorem checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 137 isolated the exact missing pressure kernel:

```text
p_M + rho_M = B_mem A_N / 3.
```

It said:

```text
the auxiliary action can remove the propagating memory mode,
but it still has to derive the activation pressure.
```

This checkpoint tests the best opening:

```text
if N is a coherent-domain volume variable, does the pressure kernel follow
from spatial metric variation?
```

Short answer:

```text
yes, conditionally.
```

This is a real upgrade over checkpoint 137, but it is not the full parent theory.

## 2. Machine Artifact

Script:

```text
research-programme\scripts\coherent_volume_pressure_kernel_theorem.py
```

Run:

```text
research-programme\runs\20260531-201500-coherent-volume-pressure-kernel-theorem
```

Generated:

```text
source_register.csv
volume_variation_derivation.csv
pressure_kernel_check.csv
theorem_conditions.csv
summary.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
volume_pressure_kernel_derived_conditionally_constants_not_derived
```

Claim ceiling:

```text
conditional_volume_pressure_kernel_not_full_parent_theory
```

## 3. The Derivation

Let the coherent-domain spatial volume be:

```text
V_D = integral_D sqrt(h) d^3x.
```

Define:

```text
N_D = (1/3) ln(V_D0 / V_D).
```

For FLRW:

```text
V_D proportional to a^3
```

so:

```text
N_D = -ln(a) = ln(1+z).
```

Now vary the spatial metric:

```text
delta ln V_D = (1/2)<h^ij delta h_ij>_D
```

therefore:

```text
delta N_D = -(1/6)<h^ij delta h_ij>_D.
```

Take the memory density action:

```text
S_M = - integral sqrt(-g) rho_M(N_D).
```

Then:

```text
delta S_M =
1/2 integral sqrt(-g)
[-rho_M + (1/3) rho_M,N] h^ij delta h_ij.
```

So the isotropic pressure is:

```text
p_M = -rho_M + (1/3) d rho_M / dN_D.
```

For:

```text
rho_M = rho_Lambda + B_mem A(N_D)
```

this gives:

```text
p_M + rho_M = B_mem A_N / 3.
```

That is exactly the kernel checkpoint 137 identified.

## 4. Numerical Check

The audit compared the volume-variation pressure against the checkpoint-137 required kernel.

| Check | Value |
|---|---:|
| rows checked | `701` |
| max pressure error | `0.0` |
| max `p+rho` error | `0.0` |
| peak volume pressure lift | `0.1160898276990483` |
| peak redshift | `z ~= 0.243396` |
| endpoint pressure lift zero | `True` |

This means:

```text
the pressure term is not hand-inserted if N_D is genuinely a coherent
volume variable.
```

## 5. What This Fixes

Checkpoint 137 had:

```text
activation pressure kernel identified = pass
activation pressure kernel derived = fail
```

This checkpoint upgrades that to:

```text
activation pressure kernel derived = pass conditional.
```

The condition is important:

```text
N_D must be a real coherent-domain volume variable,
not a fitted redshift label.
```

If that condition holds, then the memory pressure comes from metric variation:

```text
no separate pressure postulate needed.
```

This also explains why the endpoint is safe:

```text
A_N(0) = 0
```

so:

```text
p+rho -> 0
```

at the local/frozen endpoint.

## 6. What Still Fails

This does not derive the whole branch.

Still missing:

```text
the parent domain selector D;
safe boundary variation / J_rel;
the density law rho_M(N_D);
B_mem = 2/27;
p = 3;
u3 = 1/4;
local N_D = 0 and delta N_D = 0 theorem;
full perturbation theory for CMB/growth/lensing.
```

So the win is specific:

```text
pressure kernel derived conditionally.
```

Not:

```text
MTS field theory complete.
```

## 7. Conditions Ledger

| Condition | Status | Why It Matters |
|---|---|---|
| coherent domain selected | open | avoids arbitrary smoothing |
| `N_D=(1/3)ln(V_D0/V_D)` | pass conditional | gives the `1/3` pressure factor |
| boundary terms owned by `J_rel` | open | avoids wall stress / PPN hair |
| density law from parent | fail | still importing locked branch |
| cubic endpoint regularity | pass conditional | gives `A_N(0)=0` |
| full perturbation action | not done | no CMB/growth promotion |

## 8. Gates

| Gate | Status | Evidence |
|---|---|---|
| source paths exist | pass | source register checked |
| volume variable recovers FLRW `N` | pass conditional | `V_D proportional to a^3` |
| pressure kernel from metric variation | pass conditional | max pressure/lift error `0` |
| endpoint pressure lift zero | pass | cubic activation gives `A_N(0)=0` |
| boundary variation owned | open | `J_rel` must absorb moving-domain terms |
| density law derived | fail | `rho_Lambda + B_mem A(N_D)` still supplied |
| `B_mem,p,u3` derived | fail | constants not derived here |
| local PPN promoted | fail | local `N_D=0` not proven |
| growth/CMB promoted | fail | background pressure theorem only |

## 9. Decision

Decision:

```text
volume_pressure_kernel_derived_conditionally_constants_not_derived
```

Meaning:

```text
the activation pressure problem is no longer a free pressure insertion if
N_D is a coherent volume variable.
```

Boxing-score version:

```text
That was a clean counterpunch.
Not a knockout, but it scored.
The pressure term now has a recognizable mechanical origin.
```

## 10. Next Target

The live bottleneck moves.

Before this checkpoint:

```text
derive the pressure kernel.
```

After this checkpoint:

```text
derive the density law and domain owner.
```

Next exact target:

```text
derive or reject rho_M(N_D) = rho_Lambda + B_mem[1-exp(-(N_D/u3)^3)]
from the coherent cell determinant / hazard law,
without inserting B_mem, p=3, or u3=1/4 by hand.
```

If that fails:

```text
locked memory remains a strong empirical EFT closure branch,
with one more piece of its stress mechanics understood,
but still not a complete parent field theory.
```

