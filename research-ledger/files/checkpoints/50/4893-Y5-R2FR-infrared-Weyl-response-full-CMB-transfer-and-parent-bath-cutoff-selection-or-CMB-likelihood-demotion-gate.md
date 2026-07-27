# 4893 — Infrared Weyl response, UV CMB envelope, and parent bath-cutoff gate

Marker: `MTS_IR_CMB_UV_BATH_CUTOFF_GATE_4893`

## Decision

Checkpoint 4893 closes the missing infrared calculation, attempts the high-`k`
parent solve in two independent formulations, completes a bounded linear
lensing projection over the unresolved UV weight, and replaces the 4892
top-hat FDT smoke with the exact linear-system adjoint filter.

The outcome is mixed but decisive:

- the infrared Weyl response and low-multipole line of sight close without
  extrapolation;
- the local high-`k` parent does not supply a constraint-certified point
  response, but the two branches bound its Weyl ambiguity below `1.22e-4`;
- that ambiguity only widens the full-`k` lensing shift by at most `3.66e-5`;
- the exact FDT filter rejects the 4892 `(Lambda,Theta)=(0.3,0.1)` state at the
  one-percent metric gate;
- no existing parent damping, memory, or carrier scale selects the smaller
  allowed cutoff.

No CMB likelihood or cosmological promotion follows. The next derivation must
put the full nonlocal retarded bath kernel into the parent perturbation system.
If that does not close the high-`k` constraints and FDT covariance together,
the cosmological source route must be demoted.

## 1. Direct infrared solve

The 4890 finite-`k` parent and its matched-GR control were integrated at

```text
k = 0, 1e-5, 3e-5, 1e-4, 3e-4, 5e-4, 7e-4 h/Mpc.
```

The solved `k=1e-5` response differs from the exact `k=0` response by at most

```text
1.51790e-7
```

over the ten sampled redshifts. The worst infrared momentum-constraint
residual is

```text
2.85268e-6.
```

CAMB's minimum transfer mode is `1.0487e-5 h/Mpc`, so the new response grid
now reaches the engine's actual infrared floor. No `R_W=1` padding remains in
the low-`ell` calculation.

## 2. Infrared-complete non-Limber transfer

The exact 4892 source identities are retained,

\[
\delta S_T^{\rm ISW}
=2e^{-\tau}k^{-2}\partial_\eta[(R_W-1)W_{\rm CAMB}],
\qquad
\delta S_\phi=(R_W-1)S_\phi^{\rm CAMB},
\]

and projected with the newly solved infrared response. The low-multipole TT
power coverage now exceeds `99.999%`.

| `ell` | IR-complete `Delta TT/TT` | `Delta C_phi-phi/C_phi-phi` | `Delta C_T-phi/C_T-phi` |
|---:|---:|---:|---:|
| 2 | `+1.08105%` | `-1.29616%` | `+1.79995%` |
| 3 | `+1.18972%` | `-1.33898%` | `+2.43862%` |
| 4 | `+1.21888%` | `-1.35069%` | `+2.99258%` |
| 5 | `+1.19675%` | `-1.34662%` | `+3.46667%` |
| 10 | `+0.82903%` | `-1.24723%` | `+4.94142%` |

The infrared completion changes the checkpoint-4892 `ell=2` TT shift by only
`5.67e-4` in absolute fractional power, but it removes the previous `28%`
coverage caveat. Resolution halving remains within the declared numerical
gate.

## 3. High-k point branch rejected

Direct full-system modes were attempted at `0.1`, `0.2`, and `0.3 h/Mpc`.
The raw integration preserves the clock-potential evolution equation but its
relative momentum residual becomes ill-conditioned and can reach order unity.

An independent differential-algebraic branch eliminates the clock potential
and enforces the momentum constraint algebraically. It gives

```text
max momentum residual = 1.11e-16,
max clock-equation residual = 2.7699%,
RMS clock-equation residual = 0.8798%.
```

Neither branch closes both equations, so neither is promoted as the physical
UV point response. Their largest difference in `R_W` is

```text
1.21574e-4.
```

That measured split is retained as a private UV response envelope. A fitted
quasi-static form

\[
R_W(k,N)=R_\infty(N)+\frac{A_2(N)}{k^2}+O(k^{-4})
\]

extends the envelope beyond `0.3 h/Mpc`; it is not treated as a point
prediction.

## 4. Full-k linear lensing envelope

CAMB's linear Weyl power was rerun to `k=2.1 Mpc^-1`. The certified response,
finite-UV envelope, and asymptotic envelope were then projected through the
full Limber kernel.

| `L` | central shift | lower envelope | upper envelope | envelope width |
|---:|---:|---:|---:|---:|
| 10 | `-1.25185%` | `-1.25188%` | `-1.25182%` | `5.45e-7` |
| 40 | `-0.78897%` | `-0.78906%` | `-0.78889%` | `1.67e-6` |
| 100 | `-0.51598%` | `-0.51629%` | `-0.51573%` | `5.59e-6` |
| 200 | `-0.39858%` | `-0.39958%` | `-0.39770%` | `1.88e-5` |
| 400 | `-0.30640%` | `-0.30832%` | `-0.30466%` | `3.65e-5` |

Every envelope remains suppressive. The UV point failure therefore changes
the precision label, not the sign or approximate magnitude of this linear
lensing result. This remains a fixed-background, linear, Limber bound rather
than an official lensing likelihood.

## 5. Exact FDT adjoint filter

Write the linear parent perturbation system as

\[
y_N=A(N,k)y+B(N)\xi.
\]

For a metric output at `N_f`, the adjoint obeys

\[
-\lambda_N=A^T\lambda,
\qquad
\lambda(N_f)=e_\Phi,
\qquad
g(N_f,N)=\lambda^T(N)B(N).
\]

The colored-noise metric variance is then

\[
\operatorname{Var}\Phi(N_f)
=\frac1\pi\int_0^\infty d\omega\,
N(\omega)|\widetilde g(N_f,\omega)|^2.
\]

This adjoint kernel reproduces all four 4890 forward impulse responses with a
worst relative residual `8.69e-6`.

For the 4892 super-Drude KMS family at `Theta=0.1`, the present one-percent
metric-power gate requires

```text
Lambda <= 0.2517166 per e-fold.
```

The explicit 4892 point `Lambda=0.3` produces

```text
Var(Phi)/budget = 1.72066,
```

and is rejected. Natural parent scale identifications are worse:

```text
Lambda=gamma/H=1       -> 27.80 times budget,
Lambda=m_eff/H~15      -> 1148.4 times budget,
largest carrier floor  -> 9.99e15 H0.
```

The positive KMS family still exists mathematically at a smaller cutoff, but
the current parent action does not select that cutoff. The exact calculation
therefore demotes the 4892 parameter point and leaves bath-state ownership
open. It also covers final-time metric covariance, not yet the complete
two-time line-of-sight noise covariance.

## Arbitration

Closed in 4893:

- direct infrared parent response through the CAMB minimum mode;
- infrared-complete low-`ell` non-Limber temperature projection;
- a measured high-`k` response envelope after rejecting both point branches;
- a full-`k` linear lensing envelope;
- the exact adjoint FDT filter;
- rejection of the 4892 bath parameter point.

Open:

- a high-`k` parent branch satisfying momentum and clock equations together;
- parent selection of the bath cutoff and state;
- a self-consistent nonlocal parent Einstein–Boltzmann solve;
- an official likelihood.

The local stationary EH/Newton/PPN/Maxwell correspondence is unchanged. The
failure found here belongs to the local-in-time cosmological bath truncation,
not to the previously derived stationary metric-only correspondence.

## Next target

`4894-Y5-R2FR-parent-nonlocal-bath-kernel-self-consistent-Einstein-Boltzmann-or-cosmology-source-demotion-gate.md`

