# 4896 - Full-matrix FLRW stress, reshoot, and bath-cosmology retirement gate

Marker: `MTS_FULL_MATRIX_FLRW_STRESS_RETIREMENT_GATE_4896`

## Decision

Checkpoint 4895 constructed a positive reciprocal bath but left its
nonstationary stress and cosmological constraints open. This checkpoint
derives that stress from the same closed spectral continuum, solves the
resulting FLRW system, and applies the promised retirement gate.

The mathematics closes. The cosmology does not.

The physical bath fraction and `E(0)=1` can be reshot, and the differentiated
Friedmann equation agrees with Raychaudhuri below `8.89e-16`. However:

1. the reshot memory fraction is only `9.28670e-7`, a factor `1076.81` below
   the predeclared `1e-3` branch;
2. a 24-point positive-`kappa`, positive-clock scan contains no joint memory
   and bath closure;
3. more decisively, the diagonal clock counterterm changes the early
   cosmological Einstein coefficient for every FDT-allowed cutoff.

At the least damaging allowed cutoff,

\[
\frac{M_{\rm Pl,early}^2}{M_{\rm Pl,local}^2}=2.07263466,
\qquad
\frac{H_{\rm early}}{H_{\rm GR}}=0.69460615
\]

at the same physical radiation density. This destroys the defining
late-activation property of the proposed bath source.

The `gamma=1`, `sigma=0.3`, FDT-compatible, diagonally subtracted bath
cosmology is therefore retired as the active fundamental MTS cosmology
source. The stationary local-GR theorem is unaffected because its exact
branch has `theta=phi=0`. The metric-only cosmology remains the baseline while
a different derived extension is sought.

## 1. Closed covariant parent and spectral measure

Use the fixed-norm clock `U`, `u_mu=-nabla_mu U`, and the positive continuum

\[
S_\chi=\overline M_{\rm Pl}^2\int\!d^4x\sqrt{-g}
\int_0^\infty\!d\Omega\left[
-\frac12(\nabla\chi_\Omega)^2
-\frac12\Omega^2\chi_\Omega^2
+g_\Omega\chi_\Omega\phi
+qg_\Omega\nabla_\mu\chi_\Omega\nabla^\mu U
\right].
\]

The coupling density is fixed by the 4895 spectrum:

\[
\boxed{
g_\Omega^2=
\frac{2\gamma\Omega^2}
{\pi[1+(\Omega/\Lambda)^2]^2}
}
\]

so that

\[
\int_0^\infty\!d\Omega\frac{g_\Omega^2}{\Omega^2}
=C_{\phi\phi},
\qquad
\operatorname{Im}K_R=J_{\phi\phi}.
\]

The diagonal subtraction is

\[
S_{ct}=-\frac{\overline M_{\rm Pl}^2}{2}
\int\sqrt{-g}\left[
C_{\phi\phi}\phi^2+C_{\theta\theta}(\Box U)^2
\right].
\]

Introduce an algebraic clock-counterterm auxiliary,

\[
-\frac12C_{\theta\theta}\theta^2
=\frac{b^2}{2C_{\theta\theta}}+b\theta,
\qquad
b=-C_{\theta\theta}\theta.
\]

This turns the homogeneous clock sector into a first-order variational
system rather than treating the counterterm stress by analogy.

## 2. Clock current and exact stress

Clock-shift invariance gives

\[
\boxed{
D=\varrho-q\int d\Omega\,g_\Omega\dot\chi_\Omega-\dot b,
\qquad
\dot D+3HD=0.
}
\]

Lapse variation gives the complete bath-clock density

\[
\boxed{
\frac{\rho_B}{\overline M_{\rm Pl}^2}
=D+\int d\Omega\left[
\frac12\dot\chi_\Omega^2
+\frac12\Omega^2\chi_\Omega^2
-g_\Omega\chi_\Omega\phi
\right]
+\frac12C_{\phi\phi}\phi^2
-\frac12C_{\theta\theta}\theta^2.
}
\]

Scale-factor variation gives

\[
\boxed{
\frac{\rho_B+p_B}{\overline M_{\rm Pl}^2}
=D+\int d\Omega\,\dot\chi_\Omega^2
-q\int d\Omega\,g_\Omega\dot\chi_\Omega
-\dot b.
}
\]

These are not response-only auxiliary proxies. They are Hilbert sources from
the same closed continuum whose retarded kernel and FDT matrix were used in
4895.

## 3. Full reciprocal FLRW equations

Define

\[
Y=\int d\Omega\,g_\Omega\chi_\Omega,
\quad
Y_N=\int d\Omega\,g_\Omega\chi_{\Omega,N},
\quad
I_N=\int d\Omega\,\chi_{\Omega,N}^2,
\quad
I_m=\int d\Omega\,\Omega^2\chi_\Omega^2,
\]

and `d=D/(3 Mbar_Pl^2 H0^2)`. The exact Friedmann and Raychaudhuri equations
are

\[
\boxed{
E^2=\frac{
x_r+x_o+x_\Lambda+d+I_m/6-\phi Y/3
+C_{\phi\phi}\phi^2/6+\bar\kappa\phi^4/12
}{
1+3C_{\theta\theta}/2-\phi_N^2/6-I_N/6
}.
}
\]

\[
\boxed{
h=\frac{
-2x_r/E^2-3x_o/(2E^2)-3d/(2E^2)
-\phi_N^2/2-I_N/2+qY_N/(2E)
}{1+3C_{\theta\theta}/2}.
}
\]

The fields obey

\[
\phi_{NN}+(3+h)\phi_N+rac{\bar\kappa\phi^3}{E^2}
=\frac{Y-C_{\phi\phi}\phi}{E^2},
\]

\[
\chi_{\Omega,NN}+(3+h)\chi_{\Omega,N}
+\frac{\Omega^2}{E^2}\chi_\Omega
=\frac{g_\Omega}{E^2}(\phi+3qE).
\]

Differentiating the boxed Friedmann equation and substituting these field
equations reproduces the boxed Raychaudhuri equation algebraically. The
40-mode numerical realization gives

```text
maximum Friedmann-derivative residual = 8.882e-16;
maximum Raychaudhuri identity residual = 4.441e-16;
minimum Friedmann denominator          = 2.06700.
```

Thus the failed phenomenology cannot be blamed on a broken conservation
pipeline.

## 4. Exact early-time obstruction

For frequencies large compared with the bath cutoff,

\[
K_R(\omega)\longrightarrow0,
\qquad
K^{ren}_{\theta\theta}\longrightarrow-C_{\theta\theta}.
\]

On FLRW, `theta=3H`, so the diagonal counterterm changes the Einstein kinetic
coefficient:

\[
\boxed{
\frac{M_{\rm Pl,early}^2}{M_{\rm Pl,local}^2}
=1+\frac32C_{\theta\theta}
=1+\frac{3\sigma^2}{\gamma\Lambda}.
}
\]

For all FDT-allowed cutoffs `Lambda<=0.251716646`,

\[
C_{\theta\theta}\ge0.715089776,
\]

\[
\boxed{
M_{\rm Pl,early}^2/M_{\rm Pl,local}^2\ge2.072634663,
\qquad
H_{\rm early}/H_{\rm GR}\le0.694606146.
}
\]

Even the deliberately loose internal requirement
`|H_early/H_GR-1|<0.1` would need

```text
C_theta_theta < 0.156379;
Lambda/H0     > 1.151053.
```

The required cutoff is `4.57281` times above the exact FDT ceiling. Smaller
allowed cutoffs make the obstruction worse. This is an analytic branch
no-go, not a failed optimizer.

## 5. Full background reshoot

The positive spectral continuum was discretized with Gauss-Legendre modes
and renormalized to reproduce `C_phi_phi` exactly. Starting from the same
zero retarded history at `N=-14`, the clock normalization and cosmological
constant were reshot while retaining the inherited positive `kappa`.

```text
kappa/H0^2             = 4.801332e5;
clock-current scale    = 22.7109545;
Omega_Lambda           = 0.684909071;
Omega_bath,0           = 0.049000000;
E(0)                   = 1.000000000;
Omega_memory,0         = 9.286703e-7;
target Omega_memory,0  = 1.000000e-3;
memory shortfall       = 1076.808.
```

The present bath fraction closes through a large cancellation:

```text
clock-current fraction = +1.112837;
induced-mode fraction  = +0.008798;
theta counterterm      = -1.072635;
net bath fraction      = +0.049000.
```

The counterterm fraction is exactly `-3 C_theta_theta/2` at every FLRW time.
Consequently the source is not late-only:

| redshift | `H/H_matched_GR` | bath-clock fraction |
|---:|---:|---:|
| `1e6` | `0.69869` | `-1.04739` |
| `1100` | `1.31225` | `0.48800` |
| `100` | `1.43744` | `0.58920` |
| `10` | `1.45058` | `0.59833` |
| `1` | `1.32827` | `0.50250` |
| `0` | `1.00000` | `0.04900` |

The multiplier remains positive on all sampled rows, so this is not a hidden
negative-clock branch.

## 6. Scan and convergence controls

A predeclared 24-point smoke grid covered

```text
kappa/H0^2 = 1e-3 ... 1e12;
clock scale = 1e-3 ... 100;
positive kappa and zero retarded history only.
```

Results:

```text
maximum memory fraction on any row       = 1.78486e-5;
maximum on bath-close rows               = 9.13159e-7;
rows closing both targets within 10%     = 0.
```

This grid is not advertised as a global fit. The route decision does not rely
on it; the exact early-time coefficient theorem already rejects the selected
architecture.

Increasing the quadrature from 16 to 56 modes changes the derived memory
fraction by at most `1.467%`. Moving the zero-history start from `N=-12` to
`N=-16` changes it by only `2.58e-8` fractionally. The shortfall is not a
quadrature or start-time artefact.

## 7. Arbitration

Derived and closed:

- one covariant closed owner for response, noise, clock current, and stress;
- exact bath-clock density and enthalpy;
- the full reciprocal FLRW field equations;
- Friedmann, Raychaudhuri, and clock-current consistency;
- a bath-density and `E(0)` reshoot;
- quadrature and initial-history convergence.

Rejected:

- the `1e-3` late memory activation;
- an early GR-like expansion for any FDT-allowed cutoff;
- reuse of the previous bath-source CMB, growth, SN, or BAO outputs as parent
  predictions.

Decision:

```text
GAMMA=1, SIGMA=0.3 FDT-COMPATIBLE DIAGONAL BATH COSMOLOGY
    -> RETIRED AS THE ACTIVE FUNDAMENTAL COSMOLOGY SOURCE

STATIONARY LOCAL GR/NEWTON/PPN/MAXWELL
    -> UNCHANGED; THE 4895 EXACT DECOUPLING THEOREM REMAINS

METRIC-ONLY COSMOLOGY
    -> RETAINED AS THE FUNDAMENTAL BASELINE
```

This retires one derived extension, not MTS, the local-GR bridge, or the
galaxy empirical programme. Re-entry requires a genuinely different parent
spectral/counterterm architecture that removes the UV `theta^2` Planck shift
without restoring the forbidden static diagonals, and then rederives FDT,
stress, and constraints from that same parent.

## Next target

`4897-Y5-R2FR-cosmology-without-bath-source-metric-only-baseline-and-derived-extension-reentry-gate.md`

