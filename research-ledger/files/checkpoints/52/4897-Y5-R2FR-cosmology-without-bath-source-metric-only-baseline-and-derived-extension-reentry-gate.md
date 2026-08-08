# 4897 - Metric-only cosmology baseline and derived-extension re-entry gate

Marker: `MTS_METRIC_ONLY_BASELINE_REENTRY_GATE_4897`

## Decision

Checkpoint 4896 retired the selected bath cosmology. This checkpoint prevents
that result from leaving the programme in an ambiguous halfway state.

The active fundamental baseline is now the metric-only integrated-`H` branch:

\[
\boxed{
\Gamma_{\rm base}
=\int d^4x\sqrt{-g}\,
\frac{M_R^2}{2}(R-2\Lambda_{\rm cal})
+S_{\rm matter}[g]
+S_{\rm EM}[g]
+\Gamma_{\rm EFT,residual}.
}
\]

It gives ordinary GR/ΛCDM background evolution, Newtonian mechanics,
`gamma_PPN=beta_PPN=1`, and standard Maxwell/Hilbert/Poynting sourcing in the
domains already certified by checkpoints 4875, 4879, and 4880.

This is a required known limit, not a novel MTS cosmological prediction.
`Lambda_cal` is one frozen renormalized matching condition, and `G_N` remains
a measured calibration of `M_R` until the microscopic spectrum, nonminimal
coupling, and cutoff are independently derived.

All bath-source cosmology outputs from claims `L-729` through `L-738` are now
explicitly quarantined from current parent-cosmology claims. Their numerical
pipelines and mathematical methods remain reusable.

Future cosmological extensions must pass ten simultaneous derivation and
evidence clauses. No weighted score or good likelihood can compensate for a
failed parent, conservation, local-GR, or early-gravity clause.

The project now leaves cosmology fitting and returns to the highest-value
unification gap: whether the Planck stiffness and Newton constant are
microscopically predicted or only calibrated.

## 1. Active metric-only baseline

The selected integrated principal-density parent supplies the public metric,
positive massless spin-2 pole, Diff/BRST Ward identity, and universal soft
coupling. After the explicit vacuum matching condition of checkpoint 4877,
the baseline equations are

\[
G_{\mu\nu}+\Lambda_{\rm cal}g_{\mu\nu}
=M_R^{-2}
(T^{\rm matter}_{\mu\nu}+T^{\rm EM}_{\mu\nu})
+E^{\rm EFT}_{\mu\nu},
\]

with

\[
G_N=\frac1{8\pi M_R^2}.
\]

At the homogeneous two-derivative baseline,

\[
\boxed{
E^2(a)=\Omega_r a^{-4}+\Omega_m a^{-3}+\Omega_\Lambda,
\qquad Q^\nu=0.
}
\]

For the retained calibration row,

```text
H0                  = 67.4 km s^-1 Mpc^-1;
Omega_r             = 9e-5;
Omega_m             = 0.315;
Omega_Lambda        = 0.68491;
Lambda_cal          = 1.09077e-52 m^-2.
```

The baseline calculation verifies `E(0)=1`, separate matter conservation,
and unit Friedmann fraction closure at nine redshifts from zero to `1e6`.

### Local consequences

Within the previously stated strict-EFT domains,

\[
\nabla^2U=4\pi G_N\rho,
\qquad
\gamma_{\rm PPN}=\beta_{\rm PPN}=1.
\]

Maxwell remains

\[
S_{\rm EM}=-\frac14\int\sqrt{-g}\,F_{\mu\nu}F^{\mu\nu}
+\int\sqrt{-g}\,A_\mu J^\mu,
\]

\[
T^{\rm EM}_{\mu\nu}
=F_{\mu\alpha}F_\nu{}^\alpha
-\frac14g_{\mu\nu}F_{\alpha\beta}F^{\alpha\beta},
\]

including Poynting momentum. This is the calibrated source-coupling baseline
against which any future extension must be tested.

## 2. What is and is not claimed

The metric-only baseline establishes:

- a coherent GR/ΛCDM known limit;
- one common public metric and Hilbert source;
- Newton, PPN, clocks, rods, Maxwell, and Poynting correspondence;
- a clean place for bounded strict-EFT residuals.

It does not establish:

- a new explanation of cosmic acceleration;
- a prediction of `Lambda_cal`;
- a prediction of `G_N` from independent microscopic MTS data;
- a new CMB, BAO, SN, or growth likelihood preference;
- completion of strong matter, particle, or gauge-normalization sectors.

This distinction prevents the fallback baseline from being advertised as a
victory over ΛCDM merely because it reproduces ΛCDM.

## 3. Cosmology quarantine ledger

Claims `L-729` through `L-735` contain historical fixed-background,
backreacted, growth, CMB, and FDT diagnostics. They are superseded as parent
predictions by the 4896 full-stress retirement.

`L-736` remains the valid demotion step. `L-737` retains its positive spectral
matrix, FDT, and stationary-local decoupling theorems, but its cosmological
application is retired. `L-738` is the authoritative branch decision.

The machine-readable rule is

```text
eligible for current MTS parent cosmology claim = false;
eligible for method/pipeline reuse              = true.
```

This applies to all ten rows. It does not delete results or conceal failed
routes; it fixes their evidential role.

## 4. Ten-clause extension re-entry contract

A future cosmological extension may re-enter only if every clause closes.

1. **Parent operator predeclared:** the covariant operator and coefficients
   are derived before inspecting cosmological residuals.
2. **Same-parent stress:** response and Hilbert/SK stress come from the same
   action or kernel.
3. **Ward and constraints:** Friedmann, momentum, clock, and finite-`k`
   identities close together.
4. **Stationary local decoupling:** Newton, PPN, clocks, Maxwell, and source
   coupling remain inside their certified limits.
5. **Early gravity:** fixed physical radiation and locally calibrated `G_N`
   give an acceptable early expansion.
6. **No arena reset:** neither `G_N` nor the one `Lambda_cal` condition is
   independently recalibrated for cosmology.
7. **Derived activation:** amplitude and history follow from parent inputs,
   not a fit-only redshift switch.
8. **State/FDT ownership:** any dissipative response and stochastic
   covariance share one physical state.
9. **Finite-`k` species completion:** metric, matter, photon-baryon, and
   neutrino perturbations use one constraint system.
10. **Fair empirical score:** a frozen prediction is compared with refitted
    GR, `wCDM`, and CPL baselines and predeclared data splits.

The gate is

\[
\boxed{
Z_{\rm reentry}=\bigwedge_{i=1}^{10}Z_i.
}
\]

There is no average score. The retired bath branch closes six clauses and
fails four: early gravity, derived activation, finite-`k` completion, and a
valid final empirical score. Its re-entry flag remains false.

## 5. Priority redirect

The current high-value unresolved targets rank as follows.

| rank | target | reason |
|---:|---|---|
| 1 | microscopic Planck stiffness and `G_N` owner | directly separates a Newton prediction from calibration |
| 2 | primitive matter/EM normalization | universal Hilbert coupling exists, but `U(1)` normalization and `alpha` are not predicted |
| 3 | vacuum relevant-coupling selection | `Lambda_cal` is honest but not derived |
| 4 | strong matter and curvature-cubed owner | extends the certified EFT domain |
| 5 | new cosmological extension | no active derived candidate currently passes re-entry |

The key Newton relation is already known:

\[
\boxed{
G_N=\frac{12\pi}
{N_s(1-6\xi)\Lambda_{\rm UV}^2}.
}
\]

What is missing is not another algebraic rearrangement. The next checkpoint
must determine whether `N_s`, `xi`, and `Lambda_UV` have independent MTS
owners or whether the equation is only a one-parameter calibration surface.

## 6. Arbitration

```text
METRIC-ONLY COSMOLOGY
    -> ACTIVE KNOWN-LIMIT BASELINE
    -> NOT A NOVEL MTS COSMOLOGY PREDICTION

RETIRED BATH-SOURCE OUTPUTS
    -> QUARANTINED FROM CURRENT PARENT CLAIMS
    -> METHODS AND FAILURE EVIDENCE RETAINED

LOCAL GR / NEWTON / MAXWELL
    -> 4875 / 4879 / 4880 CONDITIONAL CERTIFICATES RETAINED

NEXT FUNDAMENTAL TARGET
    -> MICROSCOPIC PLANCK STIFFNESS AND G_N OWNERSHIP
```

No GitHub action or new public cosmology claim follows from this checkpoint.

## Next target

`4898-Y5-R2FR-microscopic-Planck-stiffness-owner-and-GN-calibration-versus-prediction-gate.md`

