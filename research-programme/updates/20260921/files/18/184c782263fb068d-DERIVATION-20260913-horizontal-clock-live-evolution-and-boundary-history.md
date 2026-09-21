# Horizontal-clock live evolution and the inner boundary-history test

Private continuation, 2026-09-13. A conditional regular-annulus calculation with a declared closed exterior extension; not a physical GR-limit, black-hole or global well-posedness claim.

## 1. What changed

The preceding result constructed and checked common inner mass two-jets but did not evolve them. This step finds an exact local clock reduction of the candidate transported action, checks that reduction against the saved first and second derivatives, and integrates the coupled scalar, source and constrained geometry over a nonzero interval. The geometry is recalculated from the evolving fields at every evaluation. Neither a frozen oscillator nor a Taylor polynomial stands in for that evolution.

Both the GR-control and MTS metric-Gram branches complete the tested interval with conserved total enclosed mass and positive apparatus energy. The deliberately affine inner mass history, however, does **not** persist exactly in either branch. That is retained as a failed boundary-history test, not laundered into a pass because the live equations solve.

Predecessor: `DERIVATION-20260913-common-source-two-jet-and-exterior-preparation.md`.

## 2. Derive a common clock instead of freezing the transport

For the sourced ADM variables write

```text
F=1-2 mu/R,  beta=kappa N F^(3/2) P,
d=1-kappa^2 F^2 P^2,
ds^2=-N^2 dt^2+F^(-1)(dR+beta dt)^2.
```

On the regular chart F>0, N>0, d>0, use t=T(tau,R) with

```text
T_R=c(T,R),   c=kappa sqrt(F) P/(N d),
T(tau,R_outer)=tau,   a=T_tau>0.
```

This is the same horizontal transport already present in the scalar action, now used as the common time chart on the annulus. Smooth local transport with positive a is assumed; a global horizon-crossing chart is not obtained. Direct substitution into the metric gives

```text
g_tau,R=0,
F_bar=F d,
N_bar=a N sqrt(d),
P_bar=0,
M=R(1-F_bar)/2=mu+kappa^2 R F^3 P^2/2.
```

The diagonal mass M is not generally the old mu treated as a scalar. Its shift-square correction is essential when transforming second derivatives. At the initial zero-P slice M=mu and their first physical-time derivatives agree, but their second derivatives differ wherever P_1 is nonzero.

For the full scalar coefficient C=R^2 N sqrt(F)d, C_bar=a C. The auxiliary scalar momentum transforms as a scalar, p_bar=p(T,R), while the scalar histories transform as chi_bar=chi(T,R). Consequently every transported factor becomes an equal-tau factor with J_bar=1. This is a coordinate reduction of the whole scalar action, not the old incorrect operation of setting J=1 in the original time chart while leaving the lapse unchanged.

The apparatus clock factor ell=N sqrt(d) similarly obeys ell_bar=a ell=N_bar, so its proper-clock action retains its original form. The bulk equations are derived **before** imposing P_bar=0; otherwise the missing P variation would discard the mass-evolution equation. Radial and temporal boundary conditions must still be specified separately.

Action and transformation owners: `DERIVATION-20260912-covariant-full-scalar-action-and-initial-constraint.md` and `DERIVATION-20260912-nonlinear-history-Euler-equations.md`.

## 3. Check that this is the same saved initial jet

Let g and b be the existing initial transport primitives, g_R=c_t and b_R=c_tt exp(g), and let the reference cut be the old outer physical cut. At tau=0,

```text
a(R)=exp(g(R)-g_ref),
T_tautau(R)=exp(g(R)-2g_ref)[b(R)-b_ref].

N_bar=a N,
M_tau=a mu_1,
M_tautau=a^2[mu_2+kappa^2 R U^6 P_1^2]+T_tautau mu_1,
N_bar,tau/N_bar=a L+T_tautau/a,
chi_bar,tau=a chi_1,  p_bar,tau=a p_1.
```

These are checked against derivatives of the **new live equations**, including a complex-step directional derivative of the complete metric reconstruction and source response. The old initial state is not refitted. Maximum initial metric disagreement in the matrix is 5.56e-15, mass-rate disagreement 2.02e-17, mass-acceleration disagreement 7.40e-15 and scalar-rate disagreement 2.53e-13.

This explicitly includes the shift-square contribution and the nonconstant time map. At the physical cuts P_1=0, so the previous proper inner acceleration remains zero to the inherited accuracy. The initial inner lapse remains branch-dependent. A common old coordinate rate is not relabelled as an identical proper first rate.

## 4. The live radial constraints and the retained mass equation

Suppress bars in this section; M is the diagonal mass and U=sqrt(1-2M/R). The conditional diagonal-gauge system is

```text
M_R=kappa(U^2 epsilon+U sigma),
(ln N)_R=M/(R^2 U^2)+kappa epsilon/R,
chi_i,tau=N_i U_i p_i/R_i^2,
omega_i p_i,tau=G_chi,i+rho_i,
M_tau=-kappa U K/N.
```

For each retained translated copy,

```text
A_f=sum_i B_fi chi_i,
C_i=R_i^2 N_i U_i,
D_f=sum_i S_fi C_i,
G_chi,i=-sum_f B_fi A_f D_f/h,
I_fi=A_f[S_fi C_i A_f,tau-B_fi chi_i,tau D_f]/h.
```

K is the layer-integrated oriented crossing current over the same whole factors and retained exterior bands. The factor matrices, spacing, layer width, layer weight and matched exterior amplitudes are unchanged. Epsilon includes the full canonical scalar kinetic and factor-potential energy; sigma is the apparatus energy density.

The radial solves alone do not establish M_tau. Differentiate the mass constraint:

```text
(M_tau)_R+kappa[2 epsilon/R+sigma/(R U)] M_tau
   =kappa(U^2 epsilon_tau+U sigma_tau).
```

The scalar/source Ward identity in this chart is

```text
K_R+N U epsilon_tau+N sigma_tau=0.
```

Together with the derived lapse equation, it implies that -kappa U K/N satisfies the same linear radial tangent equation. A matching lower boundary value therefore propagates the full mass equation. The verifier checks this identity symbolically; the computation also differentiates the actual constrained reconstruction and tests M_tau=-kappa U K/N on live states, not just at the initial slice.

This is a local-in-time finite radial model conditional on the declared source/support/gauge choices. It is not a proof that every original history-boundary problem admits a causal solution, or that the fixed radial regulator restores all continuum diffeomorphism properties.

## 5. Keep the original apparatus and its energy budget

The retained right-layer source is

```text
S_app=integral w(z) d tau [E theta_tau-N E+N lambda(chi-D_z(theta))],
D_z(theta)=D0(z)+V0(z) theta+(a_proper/2)theta^2.
```

D0, V0 and a_proper come from the saved source preparation; E0=0.001. The source constraint and proper-clock equation can be eliminated algebraically without fitting a force:

```text
theta_tau=N,
chi_right=D_z(theta),
V=D'_z(theta),
p_right=R^2 V/U,
p_right,tau=R^2 a_proper N/U+R V M_tau/U^3,
rho=omega_right p_right,tau-G_chi,right,
E_tau=-rho V.
```

Thus M_tau determines part of the source reaction, and the reaction changes the source energy which in turn changes the radial metric constraint. This feedback is included at every time evaluation. The right momentum is not independently stepped in violation of its source constraint. The source is still an ideal candidate apparatus: its microscopic realization, a lower-bounded apparatus Hamiltonian and the stresses holding its radius fixed have not been derived.

## 6. State the changed boundary problem openly

To obtain a genuine interval test without introducing a new inner actuator, the calculation adopts a **closed enlarged-support extension**:

- The old physical cuts remain where they were, but the retained exterior half-bands are now part of the evolved domain.
- At the lower end of all retained support, K=0; the already prepared lower mass seed stays constant. Its value is not changed during evolution.
- At the upper end of all retained support, K=0 likewise. The total enclosed mass should remain constant even while energy transfers between source, scalar and geometry.
- The old outer physical cut fixes the clock normalization N/U=C0+C1 tau. It is the clock reference, not a new truncation of the crossing factors.
- The right proper-clock apparatus drives its full retained layer with the saved D_z(theta), not with a newly fitted coordinate-time force.

The mass at the old inner physical cut is now an **output** of those retained exterior dynamics. We compare that output with the trial affine proper history, but do not enforce the history by changing exterior amplitudes at later times. This extension is a different interval boundary problem from prescribing that inner history exactly. The initial physical two-jet is shared through the checked time transformation; that alone does not make the complete boundary problems identical.

## 7. An actual interval integration, with numerical controls

The interval is 0<=tau<=0.004 in the inherited pilot normalization, not calibrated seconds. Each layer half has Chebyshev degrees 12 or 16, respecting the initial C3 join at z=0. The radial constraints use degrees 32 or 40; gaps between scalar bands have the exact vacuum radial solution. Currents are integrated across the whole crossing factors using separate layer-half interpolants.

The source-constrained states have 851 or 1123 evolving components: free scalar values/momenta, source clocks and energies, plus an inner proper-clock readout. Radial mass and lapse are dependent variables re-solved from those evolving components. DOP853 runs use both a looser/two-step-limit and a tighter/four-step-limit setting, followed by the higher spatial resolution. There is no new physical parameter fit.

All six live runs and 48 main checks complete, following a two-branch pilot with 10 checks. Across the main runs:

- Maximum tested full mass-equation discrepancy is below 4.58e-17.
- Total enclosed mass changes by at most 4.67e-15 over sampled times.
- The positive chart stays above F=0.65934 on the tested support.
- Minimum source energy at the final time is approximately 0.000950907 (GR) and 0.000951496 (MTS), versus the initial 0.001.

The separate integrity verification compares the saved solutions with an independent fixed-step RK4 replay and reconstructs the final radial constraints with adaptive radial integration instead of the main collocation solver. Temporal and layer-refinement differences are compared without retuning. Completion of that verification is owned by its final record, not inferred from the main solver's success.

Numerical gates are explicitly scoped: initial metric/flux recovery uses 1e-9, first/second derivative and live mass-equation controls use 1e-8, and total mass, clock and temporal-work controls use 1e-9. These are distinct diagnostics from the old six weak C2 rows and do not retrospectively change the old 1e-10 gate. The observed errors are much smaller than these gates; none is an interval-certified bound.

## 8. Temporal work is retained, not discarded

At fixed diagonal metric, arbitrary scalar and apparatus-clock variations give the on-shell temporal boundary term

```text
[integral w(z) dz (sum_i omega_i p_i delta chi_i+E delta theta)]_0^T.
```

The full scalar/source raw variation, including rho delta chi-rho V delta theta, is integrated and compared with this nonzero endpoint work. Gauss time orders 8 and 12 agree to roundoff. Maximum tested difference is 4.34e-19; omitting the clock work produces an error about 1.91e-5. This is a scalar/source variation check at fixed metric. It does not claim a proof of all gravitational corner terms under arbitrary moving-boundary metric variations, nor a full covariant physical support action.

## 9. The affine inner-history test fails in both branches

Let theta_inner,tau=N_inner and retain

```text
gamma=old mu_1,inner/old N_inner,
M_trial(theta_inner)=M0+gamma theta_inner.
```

This extends the previous zero proper acceleration as a deliberately affine trial history. The actual freely evolved retained exterior does not maintain it:

| tau | GR: M-M_trial | MTS: M-M_trial |
| ---: | ---: | ---: |
| 0.0005 | -1.003e-11 | -1.499e-11 |
| 0.001 | -7.912e-11 | -1.185e-10 |
| 0.002 | -6.154e-10 | -9.242e-10 |
| 0.004 | -4.655e-9 | -7.021e-9 |

These departures persist under the main temporal and layer refinements. They grow approximately cubically near the initial slice, consistent with matching through order two rather than the entire history. They are small compared with the mass but resolved compared with numerical variation; small is not identical to zero. The independent replay is required before the final integrity record marks that conclusion verified.

This is **not an MTS-only failure**, a demonstrated conservation failure, or an instability of the live solver. GR shows the same type of departure. It shows that an arbitrary higher-time boundary protocol is not generated merely by matching its initial two-jet.

## 10. Derive the precise condition needed for that prescribed history

From the full mass equation, the necessary current for the affine proper protocol is

```text
K_required=-gamma N_inner^2/(kappa U_inner).
```

For the history error Delta=M-M_trial,

```text
Delta_tau=-kappa U_inner/N_inner (K_actual-K_required).
```

The verifier records these actual and required currents at the final time. This identifies a current-response condition, not a license to insert an arbitrary cancellation force. With the previous orientation convention, the gravitational boundary-work trace is n N M_tau/(kappa U)=-n K. Any actuator used to enforce a different K must therefore own its corresponding work and backreaction.

There are two scientifically distinct uses of the new evolution. If the exterior is a closed physical subsystem, its generated inner history is a prediction, and the arbitrary affine probe should not be promoted to a law. If an externally prescribed affine boundary really is required, it needs an action-owned source response rather than a third fitted initial amplitude.

## 11. Next substantive target

Derive the retained exterior's boundary response from this **live, backreacting system**, including its initial-state contribution and source energy. This replaces the earlier frozen-geometry response as the next object to test. Determine explicitly which trace is the input and which current/history is the output; replay its work balance and the same GR control. Do not keep fitting one more exterior mode for each additional Taylor coefficient of an otherwise arbitrary boundary history.

The shared-clock construction is restricted to the regular radial chart. Horizon approach, global evolution, physical parent-selected coefficients, apparatus support stresses, regulator ownership and a complete GR/Newton reduction remain unresolved. The current result is a substantive conditional evolution construction, not a finished fundamental theory.

## 12. Evidence and preservation

- Starting seal: `source-intake/navier-stokes/20260913/annular-common-source-history-final-integrity.json`.
- Live equations and radial/current reconstruction: `scripts/annular_horizontal_clock_evolution_20260913.py`.
- Executed matrix: `scripts/derive_annular_horizontal_clock_evolution_20260913.py`.
- Initial pullback pilot: `source-intake/navier-stokes/20260913/annular-horizontal-clock-pilot-attempt01/status.json`.
- Saved actual trajectories: `source-intake/navier-stokes/20260913/annular-horizontal-clock-evolve-attempt01/status.json`.
- Independent replay and radial verification: `scripts/verify_annular_horizontal_clock_evolution_20260913.py`.
- Completion authority: `source-intake/navier-stokes/20260913/annular-horizontal-clock-final-integrity.json`.

All previous executed evidence is preserved. No GitHub, subagents or protected-workbench edits. One below-normal-priority single-core worker at a time. The protected check uses file mtimes since 2026-09-13T20:19:03Z, not a pre-turn content-hash comparison. The immutable resume snapshot precedes any later completion line.
