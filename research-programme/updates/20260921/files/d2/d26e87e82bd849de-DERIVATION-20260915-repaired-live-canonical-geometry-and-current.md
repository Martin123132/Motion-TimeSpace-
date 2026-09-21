# Repaired moving source: live canonical geometry and independent current

Private derivation/implementation checkpoint. This extends the repaired action in `DERIVATION-20260915-moving-curved-cut-action-and-canonical-current.md`; it does not reuse the force-inaccurate interpolated-trace trajectories. All quantities below are normalized controls, not fitted or observed physical parameters. Derivation and numerical tests are complete; see the separate final integrity seal for preservation checks.

## 1. The actual new problem

The previous repaired action had a canonical inverse and independently derived metric/current covectors, but its numerical trajectories used prescribed geometry. Here both scalar/source motion and radial geometry are solved together. The matter action is the positive continuous layer average

\[
 I_{\rm matter}=\int_{-1/2}^{1/2}w(z)I_z\,dz,
 \qquad w(z)=6(z+1/2)(1/2-z),\qquad\int w\,dz=1.
\]

Each layer retains the same full reference or MTS cut-cell action. Fixed scalar nodes are \(R_i(z)=R_i^{\rm base}+\epsilon z\); the reflecting source \(b(z,t)\) evolves independently. No rigid source lock is applied. A common live \(\mu(t,R),N(t,R)\) is used by all layers. The canonical momentum *density* is \(w(z)\pi(z)\), not \(\pi(z)\); because the weight is fixed in time, its interior Euler equations divide by the same positive weight. The zero-weight label endpoints are treated by continuous extension, not by division by zero.

The numerical label method is Chebyshev collocation. It is **not** claimed to be an exact finite-label Galerkin action: interpolated equations away from the collocation labels need separate residual and refinement tests. This qualification matters particularly for a local spatial current.

## 2. Average before the nonlinear radial solve

Let \(W_z=Q_{z,t}\), \(H_z=Q_{z,R}\), \(U^2=1-2\mu/R\), and \(C=R^2NU\). Define continuous fixed-radius averages

\[
 A(R)=\int wW_z^2\,dz,\qquad B(R)=\int wH_z^2\,dz,
\]

\[
 g(R)=\sum_i{w(z_i)\over\epsilon}\,
 {1\over2h}\sum_f S_{fi}(G_{b(z_i)}q(z_i))_f^2,
 \quad z_i=(R-R_i^{\rm base})/\epsilon,
\]

where only labels in the material interval contribute. Thus the full coefficient covector, including the continuously spread original Gram atoms, is

\[
 Z(R)=-\frac12\left({A\over N^2U^2}+B\right)-g(R).
 \tag{1}
\]

If \(b_z>0\), let \(z_b=b^{-1}(R)\), \(d_b=w(z_b)/b_z(z_b)\), \(V_b=b_t(z_b)\), and \(\ell_b=\sqrt{N^2-V_b^2/U^2}\) on its support; source terms vanish outside it. Variation of the inherited proper-time source action and the repaired wave action gives

\[
 \mu_R=-\kappa R^2U^2Z+\kappa US_0{N\over\ell_b}d_b,
 \tag{2}
\]

\[
 (\log N)_R={\mu\over R^2U^2}-\kappa RZ
 +{\kappa S_0V_b^2\over RN U^3\ell_b}d_b.
 \tag{3}
\]

These equations use the *already averaged* continuous densities. No delta source is multiplied by an unsmoothed self-field and no label-density Jacobian is discarded. Node and source bands may overlap: the label quadrature is split at every relevant node crossing and the inverse source label, not restricted to disjoint bands.

The boundary conditions are fixed inner mass and \(N_{\rm out}=U_{\rm out}\). With velocities supplied, the loading in (1)-(3) itself depends on the lapse. Therefore solving at an arbitrary lapse and rescaling it afterward would be wrong. The implementation solves both integral radial equations simultaneously and includes the outer normalization inside every iteration.

Piecewise Chebyshev radial integration is split at all node-band and moving source-band endpoints. Independent interior quadrature points test the differential equations, rather than only retesting their collocation equations. Fixed-metric action variations provide a second, differently assembled check of the density formulas.

## 3. Canonical coupling, not a prescribed force

For each layer the previously derived strictly monotone momentum inversion is used:

\[
 \pi=Mu+dV,\qquad
 P_b-d^TM^{-1}\pi={S_0V\over U_b^2\ell_b}
 +(I-d^TM^{-1}d)V.
 \tag{4}
\]

The field Schur complement is nonnegative and the material term has positive derivative on the timelike interval at fixed regular geometry. Alternating (4) with (2)-(3) constructs the shared numerical fixed point. Observed iteration convergence is not a global uniqueness theorem for the combined nonlinear geometry problem.

The evolved equations are

\[
 \dot q=u,\quad \dot b=V,\quad
 \dot\pi=L_q\big|_{\mu,N},\quad
 \dot P_b=L_b\big|_{\mu,N}.
 \tag{5}
\]

The coordinate covectors hold the metric field fixed during matter variation while retaining its spatial gradients at moving source/quadrature positions. The metric is then re-solved from the updated canonical state at every evolution evaluation. No background-only acceleration formula is transplanted, no force is fitted, and no mass/current/position is projected onto a desired conserved value.

## 4. Independent temporal test

The action-derived shift covector from the previous checkpoint is retained:

\[
 K_z(r)=-\sum_i E_i(z)u_i(z)\mathcal I_{b(z),R_i(z)}(r)
 -\int C(R)\dot Z_z(R)\mathcal I_{b(z),R}(r)\,dR,
\]

\[
 \mu_t^{\rm current}(r)=-{\kappa U\over N}\int wK_z(r)dz
 -\kappa NU^3p_s(z_b)d_b,
 \qquad p_s={S_0V_b\over U^2\ell_b}.
 \tag{6}
\]

The inherited gravity-only term vanishes on this polar \(P=0\) branch. It is not being dropped from a general nonzero-shift field equation. The sign and normalization in (6) follow the prior nonzero-shift action variation, not the new radial solver.

For a target above its layer's source, the regular integral in \(K_z\) is minus the tail beyond that target; below the source it is plus the integral up to the target. Fixed-node Gram covector rates are included. The moving-source delta in \(\dot Z_z\) has zero oriented interval at its own anchor, but is essential in the whole-layer Noether check:

\[
 \sum_iE_i u_i+VE_b^{\rm wave}
 +\int C\dot Z_{\rm regular}\,dR
 +\sum_iC_i\dot Z_i
 +VC_b(Z_- - Z_+)=0.
 \tag{7}
\]

The test perturbs the actual canonical state in the direction (5), separately re-solves its neighboring geometries, and differentiates their mass profiles at fixed physical radius. This \(\mu_t^{\rm radial}\) is compared with (6); it is **not** used to define the current. Neighboring velocity solutions provide acceleration for differentiating the action quantities. A fourth-order centered time-direction difference is used for the geometry, while exact first-order complex differentiation handles the split field basis away from its discontinuities. The known interface jump is included explicitly rather than being sampled through a moving discontinuity.

Two current versions are recorded: the full off-shell expression with measured field Euler residuals, and the on-shell expression with those residual terms omitted. Their difference measures one material-collocation effect rather than hiding it inside a conservation correction. The implementation also tests a nonaffine ordered source map with unequal one-sided gradients, so the interface term is not only checked on data where it happens to vanish.

## 5. Initial controls and acceptance

- Central mass .7, source action mass .03, coupling .1, base radial interval [5.2,6.8], material width .02, initial middle source 6.03 and coordinate speed .03.
- Common smooth compact field preparation from `scripts/annular_cut_initial_data_20260915.py`, with matching source-trace rate. This is the repaired preparation, not the failed off-shell initial history.
- Reference and all retained MTS Gram factors receive identical criteria. Width stays fixed while scalar, material, radial and time resolution are varied separately.
- Short duration .02 is an implementation/conservation pilot, not a long-time waveform or stability claim. Source cells must not cross and material ordering must remain positive.
- The zero-wave sector must coincide in both branches. Its source proper clocks are integrated and compared with independently evolved \(d^2R/d\tau^2=-\mu(z)/R^2\), using the initial mass label, not the live computed acceleration.
- The zero-backreaction control sets coupling to zero but retains central Schwarzschild mass .7; it is not mislabeled as flat space.
- Radial/current/canonical diagnostics must pass their original gates. Failed attempts are retained; later corrections or refinements get new files/attempts.

## 6. Results and scope

**The repaired action now has an actual live, nonzero-wave spherical evolution, not only a prescribed-background trajectory.** Sixteen trajectories complete across both branches, scalar grids17/33/65, time-step, layer, radial-resolution, dust and zero-backreaction controls. The middle source moves, all material layers stay ordered and source cell margins stay above .22 in the principal runs. Interior mass changes by about1.18e-4 while the exterior mass remains conserved without projection.

| Independent diagnostic | Observed result |
| --- | --- |
| Live fixed-point momentum round trip | below1.74e-17 |
| Initial off-grid momentum error after label4-to8 refinement | about3.90e-11 to1.19e-16 |
| Temporal mass-current disagreement in evolved principal/dust runs | below1.95e-11 |
| Exterior mass drift across all16 trajectories | below4.45e-16 |
| Whole canonical/clock state half-step difference | below2.67e-15 |
| Whole-state radial6-to10 difference | below1.80e-13 |
| Common-label4-to8 endpoint difference | below1.10e-16 |
| Independent proper-clock GR dust radius / speed errors | below8.89e-16 /1.37e-15 |
| Reference versus MTS zero-wave trajectories | identical in the saved arrays |
| Independent velocity-form background recovery at zero coupling | coordinates below1.78e-15; final velocity below3.46e-16 |
| Integrated action variation versus independently averaged metric covectors, including nonaffine/overlapping support cases | below2.01e-17 |
| Nonaffine moving Noether identity | below2.94e-19; omitting interface term leaves2.26e-6 |

**One diagnostic hypothesis failed and is preserved.** `annular-repaired-live-method-attempt01` incorrectly anticipated that the deformed source's roughly4.91e-10 current error would shrink under *material-label* refinement. Degree8-to12 and a time-difference change did not remove it. A separate radial refinement, with no equation, coupling, force or acceptance-gate change, identified the cause: degree10 had a1.53e-8 off-grid radial mass residual in the nonaffine source band. Increasing the radial degree to14 reduced the current discrepancy to2.98e-12 reference/1.76e-12 MTS. Degree18 and the smaller time-difference control remain below9.82e-12. Both branches show the same numerical mechanism; the original failed attribution is not relabeled as passed.

There are141 checks in the five completed current mathematical/numerical/diagnostic suites: snapshot15, initial current8, trajectory81, averaged-action/nonaffine controls20, radial-transport diagnosis17. The failed method-attribution suite is recorded separately, not added to that successful total. These are **not141 independent physics validations** and do not establish a continuum waveform theorem. All own numerical jobs finished before sealing.

The next scientific qualification after this solver step is to derive the continuum moving-boundary radiation/source-force equations directly, then compare the nonzero-wave trajectories with an independently implemented continuum GR matter/source problem at the same fixed physical width. Near-roundoff conservation alone is not evidence of correct continuum force or waveform, as the preserved older interpolated-trace failure already demonstrated. Cell-crossing transfer, uniform long-time convergence, unique parent boundary/material selection, angular Einstein completion and the unrestricted GR/PPN limit remain separate questions.

## Local implementation/evidence

- `scripts/annular_repaired_live_geometry_20260915.py`: continuous layer densities, coupled radial boundary-value and canonical inverse, unprojected canonical equations.
- `scripts/annular_repaired_live_current_20260915.py`: independent shift/current and moving-interface Noether comparison.
- `scripts/qualify_annular_repaired_live_geometry_20260915.py`: paired shared snapshot and off-grid checks.
- `scripts/qualify_annular_repaired_live_current_20260915.py`: paired initial current tests.
- `scripts/run_annular_repaired_live_evolution_20260915.py`: paired short evolution and dust/proper-clock controls.
- `scripts/verify_annular_repaired_live_controls_20260915.py`: nonaffine map, overlap and averaged-action variation controls.
- `scripts/verify_annular_repaired_live_method_20260915.py`: preserved failed material-error attribution; its later background controls were not reached.
- `scripts/verify_annular_repaired_radial_transport_20260915.py`: separate radial/time error diagnosis, independent prescribed-background solver and actual interior geometry-change controls.
- `source-intake/navier-stokes/20260914/annular-repaired-live-geometry-attempt01/status.json`.
- `source-intake/navier-stokes/20260914/annular-repaired-live-current-attempt01/status.json`.
- `source-intake/navier-stokes/20260914/annular-repaired-live-evolution-attempt01/status.json`.
- `source-intake/navier-stokes/20260914/annular-repaired-live-controls-attempt01/status.json`.
- `source-intake/navier-stokes/20260914/annular-repaired-live-method-attempt01/status.json` (failed, retained).
- `source-intake/navier-stokes/20260914/annular-repaired-radial-transport-attempt01/status.json`.
