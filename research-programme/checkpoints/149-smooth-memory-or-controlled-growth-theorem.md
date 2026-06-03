# 149 - Smooth Memory or Controlled Growth Theorem

Private theorem / promotion checkpoint. This is not a public claim.

## 1. Trigger

Checkpoint 148 made the promotion blocker explicit:

```text
the late-time empirical branch is alive,
but growth is still using a GR-proxy perturbation equation.
```

This checkpoint asks the exact next question:

```text
Can that GR-proxy be derived as a smooth-memory / high-sound-speed limit,
or must MTS derive explicit controlled modified-growth terms?
```

Short answer:

```text
The smooth/high-sound-speed route now has a real effective suppression law.
It is strong enough for the current source-locked late-time growth rows.
It is still not a parent-action promotion.
```

## 2. Machine Artifact

Script:

```text
research-programme\scripts\smooth_memory_or_controlled_growth_theorem.py
```

Run:

```text
research-programme\runs\20260531-235500-smooth-memory-or-controlled-growth-theorem
```

Generated:

```text
source_register.csv
theorem_contract.csv
background_memory_functions.csv
source_locked_growth_suppression_bounds.csv
suppression_summary_by_branch.csv
gate_results.csv
decision.csv
status.json
```

Status:

```text
smooth_memory_effective_suppression_law_derived_parent_promotion_still_blocked
```

Claim ceiling:

```text
smooth_memory_suppression_law_effective_not_parent_promotion
```

## 3. The Derived Suppression Law

Use the locked background:

```text
E^2(a) = Omega_m0 a^-3 + rho_mem(a)
rho_mem(a) = 1 - Omega_m0 + B_mem A(N)
N = ln(1+z) = -ln a
B_mem = 2/27
A(N) = 1 - exp[-(N/u3)^p]
p = 3
u3 = 1/4
```

The memory equation of state implied by background conservation is:

```text
1 + w_mem = B_mem A_N / [3 rho_mem]
```

For a high-sound-speed memory owner with effective sound speed near unity, the pressure-gradient operator dominates on subhorizon growth scales. With:

```text
epsilon_k = aH / (c k)
```

the memory clustering amplitude is bounded by:

```text
|delta_mem / delta_m| <= C_QS |1+w_mem| epsilon_k^2 / c_s_eff^2
```

and the fractional Poisson-source correction is:

```text
|mu(a,k)-1| <= (Omega_mem/Omega_m) |delta_mem/delta_m|
```

So the GR-proxy growth limit is not magic. It follows as the leading subhorizon limit if the memory owner is either:

1. an exact non-propagating auxiliary/geometric constraint; or
2. a high-sound-speed effective stress sector with negligible anisotropic stress.

## 4. Route Split

| Route | Result | Promotion status |
|---|---|---|
| exact auxiliary smooth memory | `delta_rho_mem^GI = delta_p_mem^GI = theta_mem = pi_mem = 0` | theorem target, not parent-derived |
| high-sound-speed effective memory | `|mu-1|` suppressed by `(aH/ck)^2` | effective derivation passes the late-time bound |
| controlled modified growth | derive `F_fric`, `mu`, slip/Sigma, and `S_mem` explicitly | fallback if smooth/high-c_s route fails |

For the exact auxiliary route:

```text
F_fric = 0
mu = 1
eta_slip = 1
S_mem = 0
```

But that only becomes a theorem if the parent action supplies the gauge-invariant constraint and Bianchi identity.

For the high-sound-speed route, `mu` is not exactly 1, but the correction is bounded and tiny on the tested late-time growth scales.

## 5. Numerical Bound on Source-Locked Growth Rows

The script reuses the source-locked SDSS/eBOSS growth covariance holdout from checkpoint 146.

Worst branch at the deliberately conservative `10x nominal` stress setting and largest correction scale `k = 0.02 h/Mpc`:

| Branch | Max `|delta_mem/delta_m|` | Max `|mu-1|` | Sum chi2 impact bound |
|---|---:|---:|---:|
| DR1 primary BAO+growth | `0.0004040668951340738` | `0.0006244429628406536` | `1.1236283330865509e-05` |
| DR2 primary BAO+growth | `0.00040575965563180997` | `0.0006204428893598783` | `1.120208903953035e-05` |
| DR1 full-shape-only | `0.0002590133222485161` | `0.00024909083790307124` | `6.9179050197016465e-06` |
| DR2 full-shape-only | `0.00026039153292939414` | `0.0002478293671903285` | `6.899037645415543e-06` |

Gate results:

| Gate | Status | Evidence |
|---|---|---|
| exact auxiliary route | pass if parent constraint derived | linear source bound is zero by construction |
| high-sound-speed nominal bound | pass | worst chi2 impact `1.12363e-07` |
| high-sound-speed conservative bound | pass | worst chi2 impact `4.49451e-07` |
| high-sound-speed 10x stress bound | pass | worst chi2 impact `1.12363e-05` |
| GR-proxy growth justification | pass effective, not parent | correction far below current source-locked growth errors |
| field-theory promotion | fail parent derivation missing | no parent stress/constraint, no CMB/local promotion |

## 6. What This Actually Buys Us

This is a meaningful improvement over the previous wording.

Before this checkpoint:

```text
growth success used a GR-proxy and smooth memory was mostly a desired closure.
```

After this checkpoint:

```text
the GR-proxy has an explicit asymptotic law and a source-locked numerical bound.
```

That means the current growth success is not obviously cheating. If the memory sector has a high-sound-speed or auxiliary/geometric owner, the missing clustering correction is far too small to change the present SDSS/eBOSS source-locked growth readout.

## 7. What This Does Not Buy Us

This does not prove:

```text
MTS has a parent perturbation action.
MTS passes CMB.
MTS derives local GR.
MTS derives B_mem=2/27.
MTS derives the domain selector D.
```

The dangerous unsolved piece is that the high-sound-speed owner is still reconstructed/effective. The exact auxiliary route is cleaner, but it still needs a parent Bianchi/constraint mechanism.

## 8. Decision

The growth branch should not be demoted right now.

Current fair status:

```text
GR-proxy growth is justified as a late-time effective limit,
provided smooth/high-sound-speed memory survives the parent-action programme.
```

The controlled-growth fallback remains on the board, but it is not forced by current late-time growth data.

Next target:

```text
150-Boltzmann-interface-contract.md
```

Reason:

```text
The subhorizon late-time growth round now has a defensible effective derivation.
The next serious promotion blocker is whether this memory owner can be propagated through CMB perturbations.
```

If the CMB interface rejects the smooth/high-sound-speed owner, then we return to the controlled-growth branch and derive `F_fric`, `mu`, slip/Sigma, and `S_mem` explicitly instead of pretending the GR-proxy is exact.
