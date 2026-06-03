# 150 - Boltzmann Interface Contract

Private CMB / perturbation-interface checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 149 gave the late-time growth proxy a defensible effective limit:

```text
smooth/high-sound-speed memory makes subhorizon growth corrections tiny.
```

The next question is harder:

```text
Can the same memory branch be wired honestly into a Boltzmann/CMB calculation?
```

Short answer:

```text
Yes as an interface contract / future kill-screen.
No as a CMB support claim.
```

The primary plasma era is background-safe because the memory fraction is tiny at recombination. The promotion blockers are still parent perturbations, late ISW/lensing spectra, and the absolute calibration bridge.

## 2. Machine Artifact

Script:

```text
research-programme\scripts\boltzmann_interface_contract.py
```

Run:

```text
research-programme\runs\20260531-235900-Boltzmann-interface-contract
```

Generated:

```text
source_register.csv
interface_modes.csv
Boltzmann_variable_contract.csv
CMB_background_interface.csv
CMB_safety_table.csv
calibration_bridge_table.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
Boltzmann_interface_defined_primary_CMB_background_safe_support_claim_blocked
```

Claim ceiling:

```text
Boltzmann_interface_contract_only_no_CMB_support_claim
```

## 3. Background Interface

The locked branch supplies:

```text
rho_mem(a) = 1 - Omega_m0 + B_mem A(N)
N = ln(1+z)
A(N) = 1 - exp[-(N/u3)^p]
B_mem = 2/27
p = 3
u3 = 1/4
```

Background conservation gives:

```text
1 + w_mem = B_mem A_N / [3 rho_mem]
```

The CMB interface tabulates:

```text
rho_mem(a)
w_mem(a)
dw_mem/dln(a)
c_a^2 diagnostic
Omega_mem(a) with approximate radiation included
```

Important implementation warning:

```text
1+w_mem -> 0 at early times and today,
so a naive dark-fluid implementation can hit denominator problems.
```

Future CLASS/CAMB-style work should use either:

1. exact frozen auxiliary memory; or
2. scalar/PPF-style high-sound-speed closure.

## 4. Interface Modes

| Mode | Perturbation rule | Status |
|---|---|---|
| exact auxiliary smooth memory | `delta_mem^GI = theta_mem = delta_p_mem^GI = pi_mem = 0` | clean if parent constraint is derived |
| high-sound-speed effective scalar | `c_s_eff^2 = 1`, `sigma_mem = 0` | implementable kill-screen, not parent support |
| controlled modified growth | derive `mu`, slip, `Sigma`, `F_fric`, `S_mem` | not ready |

So the best future CMB implementation is not a random new fitting function. It is a predeclared kill-screen using one of the two smooth-memory closures already fenced by checkpoints 149 and 150.

## 5. Primary CMB Safety

Using the primary late-to-CMB transfer reference row:

```text
Omega_m_late = 0.3032827426766658
h_profiled = 0.6842175693081872
z_star = 1091.7904498991018
```

The radiation-inclusive memory fractions are:

| Redshift | `Omega_mem` with radiation | `1+w_mem` | Readout |
|---:|---:|---:|---|
| `1059.0` | `1.6266370173279974e-09` | `0.0` | primary CMB memory background negligible |
| `1091.7904498991018` | `1.4737224055894007e-09` | `0.0` | primary CMB memory background negligible |
| `10000.0` | `6.444990236810129e-13` | `0.0` | primary CMB memory background negligible |

This is good news, but narrow good news.

It says:

```text
the memory sector is not obviously injecting a large primary-plasma perturbation source.
```

It does not say:

```text
MTS passes TT/TE/EE/lensing.
```

The real spectra danger is later: ISW, lensing kernels, distance calibration, and the shared parameter map.

## 6. Calibration Blocker

The old CMB bridge problem remains alive.

Primary strict late-to-CMB transfer:

```text
Delta chi2 vs CMB-only = 28.710799376348643
Delta Omega_m late-minus-CMB = -0.026291272002077426
```

Joint calibration red-team:

```text
hard failure count = 1
failing margin = 0.5157605947599677
BAO fraction of failing late penalty = 0.7429816457469559
```

So the interface does not erase the CMB issue. It splits it:

```text
primary-era memory fraction: safe-looking
perturbation implementation: conditional
late ISW/lensing spectra: not run
absolute calibration bridge: still not promoted
```

## 7. Gates

| Gate | Status | Meaning |
|---|---|---|
| background functions defined | pass | `rho_mem`, `w_mem`, derivatives, and radiation-inclusive fraction tabulated |
| primary CMB early fraction | pass background safety | max recombination-era `Omega_mem ~ 1.6e-09` |
| perturbation closure modes | conditional | exact auxiliary and high-c_s modes specified, not parent-derived |
| naive fluid stability | warning | `1+w -> 0`; use scalar/PPF/frozen-constraint handling |
| late ISW/lensing prediction | not run | interface only; no spectra likelihood |
| calibration bridge | fail not promoted | simple transfer fails, joint calibration remains mixed |
| CMB support claim | fail | no official spectra pass |

## 8. Decision

The CMB route is not dead, but the claim is still blocked.

Current fair status:

```text
MTS has a Boltzmann-interface contract suitable for a future CMB kill-screen.
It does not have a CMB support result.
```

Next target:

```text
151-CMB-kill-screen-runner-contract.md
```

That should define the future run without wasting tokens watching it:

```text
fixed locked branch,
exact auxiliary or high-c_s effective closure,
TT/TE/EE/lensing outputs,
late ISW/lensing diagnostics,
calibration bridge logged separately,
and no public claim unless the spectra survive.
```

In boxing terms: we have now checked that MTS is not walking into the CMB round with its gloves untied. But we still have to actually step into the ring.
