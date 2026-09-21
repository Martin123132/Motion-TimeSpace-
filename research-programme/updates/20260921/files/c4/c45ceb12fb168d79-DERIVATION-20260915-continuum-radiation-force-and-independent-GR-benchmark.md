# Continuum radiation force and an independent moving-source GR benchmark

Private continuation of `DERIVATION-20260915-repaired-live-canonical-geometry-and-current.md`. This checkpoint derives the radiation force rather than assigning it, qualifies the repaired finite action's moving-force limit, and tests it against an independently discretized continuum problem. All numerical parameters are normalized controls, not observations or fitted physical constants.

## 1. Vary the moving boundary, including time transport

On the polar spherical chart

\[
 ds^2=-N^2dt^2+U^{-2}dR^2+R^2d\Omega^2,\qquad
 U^2=1-2\mu/R,
\]

the continuum scalar action on either side of a source \(R=b(t)\) is

\[
 I_{\phi}=\int dt\int dR\,\frac12(AW^2-CH^2),\qquad
 A=\frac{R^2}{NU}=\frac{R^4}{C},\quad C=R^2NU,
 \quad W=\phi_t,\ H=\phi_R.
\]

The material action is \(-S_0\int\ell\,dt\), with \(V=\dot b\), \(\ell=\sqrt{N_b^2-V^2/U_b^2}>0\). The two sides satisfy the moving zero trace, hence \(W_\pm+VH_\pm=0\) at the source.

For the left domain, integration by parts yields the boundary covector \(-CH-VAW\) multiplying the Eulerian field variation. The second term comes from the moving endpoint during integration in time; omitting it changes the result. Since \(\delta\phi_b=-H\delta b\), the left force contribution is

\[
 \mathcal L_b-(-CH-VAW)H
 =\frac12(C-AV^2)H_-^2.
\]

The right contribution has the opposite orientation. Thus

\[
 \boxed{\mathcal F_{\phi}=\frac12(C_b-A_bV^2)(H_-^2-H_+^2).}
 \tag{1}
\]

This is a two-sided reflecting scalar/material model. It does not establish that the boundary/material law is uniquely selected by the full MTS parent, or that every physical matter field has this coupling.

## 2. Rest-frame meaning and the exact material equation

The source velocity and outward unit normal in the two-dimensional radial chart are

\[
 u^a=(1,V)/\ell,\qquad n^a=(V/(NU),NU)/\ell.
\]

They satisfy \(u^au_a=-1\), \(n^an_a=1\), \(u^an_a=0\). The scalar pressure in the source rest frame is

\[
 \Pi_\pm=\tfrac12(n^a\partial_a\phi_\pm)^2
 =\tfrac12U_b^2\left(1-\frac{V^2}{N_b^2U_b^2}\right)H_\pm^2.
\]

Equation(1) becomes \(\mathcal F_\phi=b^2N_b\Delta\Pi/U_b\). The material canonical momentum and force equation are

\[
 p_s=\frac{S_0V}{U_b^2\ell},\qquad
 \dot p_s=-\frac{S_0}{\ell}
 \left(N_bN_{R,b}+\frac{V^2U_{R,b}}{U_b^3}\right)
 +\frac{b^2N_b}{U_b}\Delta\Pi.
 \tag{2}
\]

Equivalently, the normal proper acceleration satisfies \(S_0a_an^a=b^2\Delta\Pi\). The speed factor is a Lorentz/rest-frame pressure effect, not a free suppression coefficient. Its omission is tested at non-negligible source speed, not only where the correction happens to be tiny.

## 3. Combine with live continuum Einstein-scalar constraints

Keep the previous positive continuous material average \(\langle\cdot\rangle=\int w(z)(\cdot)dz\), fixed nonzero material width and ordered \(b_z>0\). At the location of a particular layer let \(d_b=w/b_z\), \(E_s=\sqrt{S_0^2+U^2p_s^2}\), and

\[
 \bar\rho=\left\langle\tfrac12(W^2/N^2+U^2H^2)\right\rangle,
 \qquad \overline{WH}=\langle WH\rangle.
\]

The continuum radial and temporal constraints are

\[
 \mu_R=\kappa R^2\bar\rho+\kappa UE_s d_b,\quad
 (\log N)_R=\frac{\mu}{R^2U^2}+\frac{\kappa R\bar\rho}{U^2}
 +\frac{\kappa U p_s^2}{R E_s}d_b,
\]

\[
 \mu_t=\kappa R^2U^2\overline{WH}-\kappa NU^3p_s d_b.
 \tag{3}
\]

Substitution into the radial Christoffel terms gives cancellation of all *explicit local* material-density terms. Their coefficient is

\[
 -N^2U^3p_s^2/E_s+2NUp_sV-E_sV^2/U=0
\]

because \(V=NU^2p_s/E_s\). This does **not** remove the source's gravity: the integrated mass \(\mu\) still includes it.

For each scalar field, the source-frame energy density is the nonnegative expression

\[
 \rho_\phi^{(u)}=
 \frac{(W+VH)^2+(NUH+VW/(NU))^2}{2\ell^2}.
\]

Consequently (2)-(3) imply the compact proper-clock law

\[
 \boxed{\frac{d^2b}{d\tau^2}=-\frac{\mu_b}{b^2}
 -\kappa b\langle\rho_\phi^{(u)}\rangle_b
 +\frac{b^2\sqrt{U_b^2+(db/d\tau)^2}}{S_0}\Delta\Pi.}
 \tag{4}
\]

The terms are enclosed-mass attraction, gravitational focusing by scalar energy measured in the source frame, and the two-sided radiation-pressure force. Setting the scalar to zero gives the prior GR dust law \(b_{\tau\tau}=-\mu/b^2\); its weak-field, slow-motion limit has the Newtonian inverse-square form. Neither Newton's constant nor the full MTS matter sector has thereby been derived. Equation(4) is conditional on the continuum scalar/source action and constraints(3), not a completed proof that every finite MTS solution converges to them.

## 4. A small momentum can have a non-small derivative

The repaired finite action has source momentum \(P_b=p_s+\zeta_h\), so its physical wave force is

\[
 \mathcal F_h=L_b^{\rm wave}-\dot\zeta_h,
 \tag{5}
\]

not \(L_b^{\rm wave}\) alone. With left/right cut lengths \(L,D\), bounded smooth one-sided data and a fixed cell-phase margin,

\[
 \zeta_h=\tfrac12A_bV(H_-^2L+H_+^2D)+O(h^2)=O(h).
\]

But \(\dot L=V\), \(\dot D=-V\), so

\[
 \dot\zeta_h=\tfrac12A_bV^2(H_-^2-H_+^2)+O(h),\qquad
 L_b^{\rm wave}=\tfrac12C_b(H_-^2-H_+^2)+O(h).
 \tag{6}
\]

Their difference has exactly the timelike pressure factor in (1). It is incorrect to discard \(\dot\zeta_h\) merely because \(\zeta_h\to0\). At a fixed moving-source phase, differentiation and the mesh limit need not commute separately; the physical combination must be formed first.

Taylor expansion of the split reference kinetic/spatial integrals then gives \(\mathcal F_h-\mathcal F_\phi=O(h)\) under bounded one-sided spatial/time jets, smooth positive metric, a uniform timelike margin and fixed positive cell-phase margin. The retained lifted Gram term has \(G_bq=O(h^2)\) on its interface rows and shape derivative \(O(1)\), giving an additional \(O(h)\) force for the bounded finite-stencil coefficients. No Gram row is removed. This is local force consistency, not uniform solution stability or a cell-crossing theorem.

The manufactured curved, time-dependent-metric test uses84 cases, grids17..1025, three phases and two velocities in each branch. Worst final force errors are0.2062% reference/0.1428% MTS with measured orders1.00017/0.99983. At speed .25, the finite \(\dot\zeta_h\) term agrees with (6) within0.371% at the finest grid; its omission is not a harmless fine-grid approximation. These are controlled numerical consistency results, not an observational advantage of one theory.

## 5. Independent continuum benchmark, with its scope kept explicit

The first independent orbit benchmark sets **backreaction coupling to zero**, retaining a prescribed Schwarzschild mass .7. This isolates the derived moving-source force from the shared radial solver. It is the middle-layer zero-backreaction control of the fixed-width family, not an independently evolved live finite-width geometry. The older one-sided Israel thin-shell solver is not silently reused for this different two-sided source problem.

For \(F(R)=1-2M/R\), introduce \(f_\pm=W\pm FH\). Directly from the continuum scalar equation,

\[
 (f_+)_t=F(f_+)_R+\frac F R(f_+-f_-),\qquad
 (f_-)_t=-F(f_-)_R+\frac F R(f_+-f_-).
\]

The two subdomains follow the source through separate smooth coordinate maps. At the source, the incoming characteristic is eliminated using

\[
 f_+^{\rm left}=-\frac{F-V}{F+V}f_-^{\rm left},\qquad
 f_-^{\rm right}=-\frac{F+V}{F-V}f_+^{\rm right}.
\]

This is an analytic boundary condition, not an energy/position projection. The outer boundaries use the same zero normal gradient as the finite action. The continuum solver uses Chebyshev characteristics and the rest-pressure version of(2), while the repaired reference/MTS solver uses the original action, its full Gram factors and the derived velocity Hessian. Sparse assembly is separately checked against the original dense action/Hessian/acceleration; no force is copied from the oracle into finite evolution.

Both receive the same new compact smooth two-sided initial field, unequal source slopes .012/.006, source mass .03, initial radius6.03, speed .03 and duration .02. Initial curvature is chosen to satisfy second trace compatibility using the derived source law; this is a declared preparation, not an evolving fitted force. Under static geometry, continuum boundary energy loss is exactly \(-V\mathcal F_\phi\), balancing material energy gain. Proper clocks are also evolved and compared.

Field errors are measured in the physical energy norm at the same physical radii. Quadrature is split at **both** source positions so a small displacement does not hide a sliver containing the gradient jump. This avoids comparing only equal computational grid labels.

## 6. Recorded outcomes

The first continuum oracle attempt failed the unchanged field-resolution gate: degree96-to192 differed by2.28e-5, above2e-6. Extending only the spatial resolution to384 reduced the difference to2.29e-7 and passed the original gate; energy drift is4.98e-15. The original failed attempt remains intact.

The first finite-action benchmark also failed the common waveform gate: both1025-node runs gave0.54227%, just above the original0.5% limit, despite excellent force and source trajectories. It is not relabeled as passed. A1505-node refinement completes with unchanged equations, initial data, duration and gates; this grid is chosen geometrically to stay away from an unimplemented cell-crossing event, not to tune a force result. Its source-cell margin stays at least .2.

| Finest paired test against the qualified continuum oracle | Reference | Full-factor MTS |
| --- | --- | --- |
| Maximum physical energy-norm field error | 0.369213% | 0.369213% |
| Final physical energy-norm field error | 0.335129% | 0.335129% |
| Maximum relative radiation-force error | 0.00004161% | 0.013742% |
| Maximum source position error | 1.59e-12 | 2.94e-12 |
| Maximum coordinate velocity error | 1.85e-10 | 9.65e-10 |
| Maximum proper-clock error | 7.05e-14 | 1.31e-13 |
| Conserved total energy drift | 6.94e-18 | 1.05e-17 |
| Saved129-node whole-trajectory half-step difference | 2.54e-15 | 3.58e-15 |

The equal worst field errors occur at the common initial finite-element interpolation; they do not mean the two evolved fields are identical. Source and force errors are measured throughout the trajectory separately. These numbers qualify a short normalized control, not astrophysical accuracy or a numerical superiority claim for MTS.

The sparse optimization retains all original factors and agrees with the dense implementation through65 nodes: maximum tested acceleration difference1.42e-13. Its inherited sparse-factor helper emits a SciPy future dtype-conversion warning; the original helper remains unchanged and the explicit equivalence tests pass. This is not a mathematical failure or a warning-free build claim.

All current numerical jobs are finished. The seven completed suites contain64 mathematical/numerical/diagnostic checks: force algebra11, sparse equivalence18, manufactured force limit6, momentum cancellation5, characteristic/work algebra7, refined oracle4 and refined finite benchmark13. The two failed under-resolved suites and their raw data are retained separately, not counted as successful suites. A separate final seal verifies inherited/current files and the protected workspace.

## 7. What this establishes, and the next calculation

This gives an explicit derived continuum radiation force, a compact conditional live GR acceleration law, the previously essential finite-momentum cancellation, and an independently implemented two-sided characteristic reference. It does not establish unrestricted GR, a unique parent material coupling, angular Einstein completion, an observational fit or a zero-width limit.

The next calculation is to put (1)-(4) into an independent **finite-width, common-live-geometry** characteristic solver and compare it with the existing repaired live canonical evolution at the same source width and preparation. Cell crossing needs its own variational transfer rule before arbitrary further mesh refinement or longer fixed-grid runs. An instantaneous \(O(h)\) force result on a noncrossing cell cannot alone prove a fixed-time, all-mesh convergence theorem for a source that keeps moving.

## Source/evidence paths

- `scripts/derive_annular_continuum_radiation_force_20260915.py`.
- `scripts/annular_sparse_repaired_cut_20260915.py`.
- `scripts/verify_annular_sparse_repaired_cut_20260915.py`.
- `scripts/verify_annular_continuum_moving_force_20260915.py`.
- `scripts/derive_annular_moving_momentum_cancellation_20260915.py`.
- `scripts/derive_annular_characteristic_work_balance_20260915.py`.
- `scripts/annular_radiation_benchmark_preparation_20260915.py`.
- `scripts/annular_two_sided_GR_characteristics_20260915.py`.
- `scripts/run_annular_two_sided_GR_oracle_20260915.py`.
- `scripts/run_annular_two_sided_GR_oracle_refined_20260915.py`.
- `scripts/run_annular_repaired_GR_force_benchmark_20260915.py`.
- `scripts/run_annular_repaired_GR_force_refined_20260915.py`.
- `source-intake/navier-stokes/20260914/annular-continuum-radiation-force-algebra-attempt01/status.json`.
- `source-intake/navier-stokes/20260914/annular-sparse-repaired-cut-equivalence-attempt01/status.json`.
- `source-intake/navier-stokes/20260914/annular-continuum-moving-force-limit-attempt01/status.json`.
- `source-intake/navier-stokes/20260914/annular-moving-momentum-cancellation-attempt01/status.json`.
- `source-intake/navier-stokes/20260914/annular-characteristic-work-balance-attempt01/status.json`.
- `source-intake/navier-stokes/20260914/annular-two-sided-GR-oracle-attempt01/status.json` (failed, retained).
- `source-intake/navier-stokes/20260914/annular-two-sided-GR-oracle-attempt02/status.json`.
- `source-intake/navier-stokes/20260914/annular-repaired-GR-force-benchmark-attempt01/status.json` (failed, retained).
- `source-intake/navier-stokes/20260914/annular-repaired-GR-force-benchmark-attempt02/status.json`.
