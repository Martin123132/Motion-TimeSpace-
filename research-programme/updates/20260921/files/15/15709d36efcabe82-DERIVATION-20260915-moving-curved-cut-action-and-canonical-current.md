# Moving curved cut-cell action and its canonical gravity current

Private derivation and controlled numerical tests, 2026-09-15. No GitHub action. All work stays in post-checkpoint-work. Ancestry: `DERIVATION-20260914-consistent-moving-trace-and-live-wave-gravity.md` and its immutable `source-intake/navier-stokes/20260914/annular-fixed-trace-final-integrity.json`.

## 1. What changed, and what has actually been achieved

The previous static reference cut-cell correction and full-factor MTS interface lift now belong to a **single moving, time-transported curved action**. Its source momentum, velocity inversion, lapse/mass variations and shift current are derived below. Independent finite-action variations verify the current; a moving-interface term in the conservation identity is necessary in both branches.

The repaired matter/source dynamics also evolve successfully on prescribed Schwarzschild and flat backgrounds with common boundary-compatible initial data. These are not live self-gravity evolutions. The older live-gravity trajectory belongs to the different, force-inaccurate interpolated-trace action and is not relabelled as evidence for this repair.

Current result: 129 checks in the current canonical, transport, metric, background-evolution and interface-limit runs pass. The earlier 27-check qualification with a complex-storage warning and the failed first background run are retained separately, not hidden or counted as additional independent physics results.

Remaining immediate gap: solve the repaired finite-width radial constraints together with the newly derived canonical velocity inversion, then evolve their geometry and compare its mass rate with the independent current. No full GR limit, angular Einstein-tensor closure, observational pass or unique microscopic parent boundary law is claimed here.

## 2. Physical horizontal leaves rather than a simultaneous-time shortcut

Keep the inherited physical metric and canonical chart, in c=1 units:
\[
 ds^2=-N^2dt^2+(dR+\beta dt)^2/U^2+R^2d\Omega^2,
 \quad U^2=1-2\mu/R,\quad\beta=\kappa NU^3P,
\]
\[
 c=\frac{\beta}{N^2U^2-\beta^2},\qquad
 C=\frac{R^2(N^2U^2-\beta^2)}{NU}.
\]
The physical reference scalar density can be written exactly as
\[
 \frac{R^2}{2NU}(\chi_t-\beta\chi_R)^2-\frac{R^2NU}{2}\chi_R^2
 =\frac{R^4}{2C}\chi_t^2-\frac C2(\chi_R+c\chi_t)^2.
\]
The areal factor R squared is included; this is not the planar static action with the same labels attached.

Use source coordinate time s as a leaf label and V=db/ds. Solve
\[
 T_R=c(T,R),\qquad T(s,b(s))=s.
\]
Differentiation at fixed target radius gives
\[
 J(s,R)=T_s=(1-c_bV)\exp\!\left(\int_b^R c_t(T(\rho),\rho)d\rho\right).
\]
Thus J is not the fixed-anchor expression with initial value one. Work locally where N,U,C,J and 1-c_bV are positive and each leaf intersects the source once.

Define transported nodal values and coefficient densities
\[
 q_i^\sharp(s)=q_i(T(s,R_i)),\quad
 \bar C(s,R)=J(s,R)C(T(s,R),R).
\]
Their rates are dq_i^sharp/ds=J_i*q_i,t(T_i). Construct Q(s,R) by piecewise linear interpolation on the fixed radial nodes with an additional, exact zero at R=b(s). This replaces the previous interpolated zero-trace constraint; there is **no old trace multiplier**.

For a time relabelling t_old=H(t_new,R), c_new=(c_old(H)-H_R)/H_t and C_new=H_t*C_old(H). If J_source=dt_old,source/dt_new,source, then the transported nodal values are scalars, their rates and V acquire J_source, and bar(C)_new=J_source*bar(C)_old. Source proper time acquires the same density factor. The action in section3 is therefore time-coordinate covariant off shell on the stated regular chart. This does not prove arbitrary spatial-diffeomorphism invariance of a finite radial grid.

## 3. One action containing the repaired boundary

Let G and S_fi be the complete inherited Gram factor and coefficient-sampling matrices. No rows or weights are discarded. For the source cell define
\[
 L=b-R_l,\quad D=R_r-b,\quad
 j_b^Tq=q_l/L+q_r/D,\quad\rho_{b,i}=(R_i-b)_+,
\]
\[
 G_b=G(I-\rho_bj_b^T),\quad A_f=(G_bq^\sharp)_f,\quad
 \bar C_f=\sum_i S_{fi}\bar C(s,R_i).
\]
The action is
\[
 \boxed{I=\int ds\left\{
 \int dR\left[\frac{R^4}{2\bar C}Q_s^2-\frac{\bar C}{2}Q_R^2\right]
 -\frac1{2h}\sum_f\bar C_f A_f^2
 -S_0\sqrt{N_b^2-(V+\beta_b)^2/U_b^2}\right\}.}       \tag{1}
\]
S_0 is source rest mass, distinct from the sampling matrix. Reference means omit only the Gram sum. The reference integral now uses the split trial field and its consistent kinetic integral, not the older lumped moving-trace kinetic rule.

At a flat planar static source this recovers the already proved split-cell pressure correction and the full-factor static lift. Away from the interface it retains the bulk factors. It is an explicitly chosen boundary extension, not a proof that the unchanged parent uniquely prescribes this material interface. The geometry sector itself remains the inherited Einstein/canonical sector; (1) is not a derivation of that whole sector from first principles.

## 4. Canonical source inertia and a unique velocity inversion

At P=0, J=1 and C=R^2NU. Write Q=a(R,b)^Tq,
\[
 W=Q_t=a^Tu+B V,\quad B=(\partial_ba)^Tq,\quad H=Q_R.
\]
The partial derivative with respect to b is at fixed physical R. In the cut cell it gives the convection terms found in the planar derivation; it is not a derivative following a quadrature point.

Define
\[
 M=\int\frac{R^4}{C}aa^T dR,\quad
 d=\int\frac{R^4}{C}aB\,dR,\quad
 I_b=\int\frac{R^4}{C}B^2dR.
\]
Then the canonical momenta are
\[
 \pi=Mu+dV,\qquad
 P_b=p_s+\zeta,
 \quad p_s=\frac{S_0V}{U_b^2\ell_b},\quad
 \zeta=d^Tu+I_bV,\quad\ell_b=\sqrt{N_b^2-V^2/U_b^2}.      \tag{2}
\]
The Gram term changes the coordinate force through G_b and its full b derivative, but does not add instantaneous P=0 kinetic inertia. Its transported P variation must still be retained.

The field kinetic Hessian is a Gram integral of the features (a,B), so M is positive definite for a nondegenerate mesh and
\(\mathcal I=I_b-d^TM^{-1}d\ge0\).
Eliminate u to obtain a scalar inversion:
\[
 \boxed{P_b-d^TM^{-1}\pi
 =\frac{S_0V}{U_b^2\sqrt{N_b^2-V^2/U_b^2}}+\mathcal I V.} \tag{3}
\]
The derivative of its right side is
\[
 \frac{S_0N_b^2}{U_b^2\ell_b^3}+\mathcal I>0.
\]
It tends to opposite infinities as V approaches the two timelike endpoints. Thus at fixed regular metric, source position and scalar configuration there is exactly one velocity for any finite canonical target. This supplies an actual inversion for the next live radial solver, rather than an unsigned momentum relation. The numerical implementation brackets inside the timelike interval and fails rather than silently accepting an unbracketed extreme target.

The Euler equations are the full mass-matrix equations
\[
 \mathbb M\dot v=L_x-(\partial_xL_v)v-\partial_tL_v,
 \qquad x=(q,b),\ v=(u,V).
\]
All source-length, physical metric-gradient and Gram-lift derivatives are included. There is no prescribed continuum recoil force or energy projection.

## 5. Lapse/mass sources and the live finite-width system

Let the wave coefficient covector be the distribution
\[
 Z(R)= -\tfrac12[R^4W^2/C^2+H^2]
       -\sum_i\delta(R-R_i)\frac1{2h}\sum_fS_{fi}A_f^2.   \tag{4}
\]
At P=0 the field contributions are
\[
 G_N^{wave}=R^2UZ,\qquad G_\mu^{wave}=-RNZ/U.
\]
The source adds
\[
 G_N^{src}=-\frac{S_0N_b}{\ell_b}\delta_b=-E_s\delta_b,
 \qquad G_\mu^{src}=\frac{S_0V^2}{bU_b^4\ell_b}\delta_b,
 \quad E_s=\sqrt{S_0^2+U_b^2p_s^2}.
\]
Independent metric perturbations verify these covectors both at fixed velocities and, after (3), at fixed canonical momenta, where delta(H)=-delta(L).

For live self-gravity do not multiply unsmoothed shell distributions by discontinuous self-fields. Retain the inherited positive finite-width material average over z, with fixed scalar nodes R_i(z), ordered source b(z), and weight w(z). Let Z_total be the averaged wave covector and average the source delta functions before solving the nonlinear radial constraints:
\[
 \mu_R=-\kappa R^2U^2 Z_{total}
       +\kappa U\int w(z)E_s(z)\delta(R-b(z))dz,
\]
\[
 (\log N)_R=\frac{\mu}{R^2U^2}-\kappa RZ_{total}
       +\frac{\kappa U}{R}\int w(z)\frac{p_s(z)^2}{E_s(z)}\delta(R-b(z))dz. \tag{5}
\]
The layer momenta in (2) are per positive layer weight, as before. Equations (2)-(5) must be solved together: M,d and the wave density depend on the live lapse and mass. This coupled solve is **not yet implemented here**. The source-width/dust-crossing restrictions of earlier work remain; this action does not derive a rigid or zero-width material body.

## 6. Shift current, moving-anchor term and constraint compatibility

At P=0, a shift variation gives
\[
 \delta c=\delta\beta/(N^2U^2),\quad \delta C|_P=0,
 \quad I_R=\delta T_R=\int_b^R\delta c(t,\rho)d\rho,
\]
\[
 \delta J_R=\partial_tI_R
 =\int_b^R\partial_t\delta c\,d\rho-V\delta c_b.          \tag{6}
\]
The last term is essential. Vary transported nodal values, their rates, every pulled coefficient density and the source proper clock before setting P=0.

Define E_i=dot(pi_i)-L_qi and E_b^wave=dot(zeta)-L_b^wave. With compact temporal variations, integration by parts gives the connection current
\[
 \boxed{\mathcal K(r)=-\sum_i E_i u_i\,\mathcal I_{bR_i}(r)
 -\int C(R)\partial_tZ(R)\,\mathcal I_{bR}(r)dR,}        \tag{7}
\]
where \(\mathcal I_{ab}(r)=\operatorname{sgn}(b-a)1_{\min(a,b)<r<\max(a,b)}\).
The unintegrated first variation is checked independently against (7). For noncompact time variations retain the endpoint work
\([\sum_i\pi_i u_i I_i+\int CZ I_R dR]_{t_0}^{t_1}\).

In the inherited canonical variables,
\[
 G_P=\frac{\kappa U}{N}\mathcal K+\kappa NU^3p_s\delta_b,
 \qquad\mu_t=(H_{gravity})_P-G_P.                        \tag{8}
\]
The source term has this sign because delta(L_src)=+p_s*delta(beta_b). In the inherited polar P=0 branch the gravity-only contribution vanishes. Equations (7)-(8) are not an assertion that the matter current vanishes.

### The interface distribution cannot be dropped

Z is piecewise smooth in the cut cell. Its time derivative at fixed radius includes
\[
 \partial_t Z=(\partial_t Z)_{regular}
       +V(Z_- - Z_+)\delta_b
\]
as well as the time derivatives of the fixed-node Gram atoms. Although the interface atom pairs with I_bb=0 in (7), it is required in the integrated off-shell identity
\[
 \boxed{\sum_iE_i u_i+VE_b^{wave}+\int C\partial_tZ\,dR=0.} \tag{9}
\]
Independent manufactured histories give errors below6.08e-17. Dropping the moving-interface contribution instead produces errors up to0.002902 in **both** branches.

Differentiating (7) distributionally and using (9) gives
\[
 \partial_R\mathcal K=C\partial_t Z+
       \sum_iE_i u_i\delta_i+VE_b^{wave}\delta_b.
\]
In smooth bulk regions on the scalar Euler equations, K_R=C*Z_t. Combining the bulk radial constraints in (5) gives
\[
 (\log(U/N))_R=2\kappa RZ,
\]
and hence the R derivative of (8) equals the time derivative of the bulk mass constraint:
\[
 (\mu_t)_R=2\kappa RZ\mu_t-\kappa R^2U^2Z_t
          =\partial_t[-\kappa R^2U^2Z].                  \tag{10}
\]
This is a derived conditional compatibility identity, not a numerical measurement of a live repaired spacetime. Source distribution terms must be combined with the proper-time source equation and finite-width averaging; the standard advective equality U*E_s*V=N*U^3*p_s fixes their delta-prime normalization. No independent angular equation or unrestricted GR theorem is inferred from this bulk result.

## 7. What the independent tests say

- Canonical qualification:29 checks pass, including the positive full velocity Hessian, independent coordinate/rate action variations and (9). A prior run's complex-Hessian storage warning is preserved. A minimal dtype-only wrapper removes it; the second run treats such warnings as errors and verifies unchanged numerical results. No physics equation or gate was changed.
- Time transport/current:18 checks pass. Full action covariance error<1.05e-16 and proper-clock error<1.12e-16 under a radius-dependent time relabelling with nonzero shift. Omitting transported coefficient Jacobians produces errors up to2.15e-4.
- Independent finite nonzero-shift action differences agree with the derived integrated current to1.48e-14 (reference) and1.21e-14 (MTS). Raw and integrated-by-parts variations agree below2.04e-19. Freezing the source-anchor contribution fails by8.33e-6 and9.54e-6.
- Metric/canonical inversion:18 checks pass. Velocity round-trip error<1.39e-17; independent lapse/mass action and fixed-momentum Hamiltonian variations agree to1.79e-13. This checks usable radial source covectors, not a completed solution of (5).

Evidence:
- `source-intake/navier-stokes/20260914/annular-covariant-cut-canonical-qualification-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-covariant-cut-canonical-qualification-attempt02/status.json`
- `source-intake/navier-stokes/20260914/annular-cut-transport-and-current-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-cut-metric-and-canonical-inversion-attempt01/status.json`

## 8. Actual moving tests on prescribed curved backgrounds

The evolution tests use the Schwarzschild background N=U=sqrt(1-2*0.7/R), and separate flat controls N=U=1. Scalar/source stress does **not** feed back into these backgrounds. They test the repaired matter action and source dynamics, not (5) or a self-consistent Einstein-scalar spacetime.

Declared normalized inputs: R in[5.2,6.8], initial b=6.03, V=0.03, source rest mass S_0=0.03. This is a new controlled test setup, not the previous mass0.8/source0.003 live-gravity trajectory continued under another name. Both branches receive the same setup and gates.

The first attempt incorrectly reused the arbitrary off-shell manufactured field as refinement initial data. That smooth field has a nonzero value at the requested zero-trace source. Enforcing a zero inside progressively smaller cells injects gradient energy proportional to
\[
 \frac{C_b\,q(b)^2}{2h\theta(1-\theta)}.
\]
Consequently it is not a common finite-energy continuum preparation. Its65-node MTS independent trajectory-Euler check failed at3.01338e-7 against the unchanged2e-7 gate; all raw completed/event data remain saved. This is not called an MTS physical failure or silently labelled repaired.

The separate second attempt keeps the action, duration and gates, but uses one common smooth compact field, linear around the source, with q(b)=0 and q_t+V*q_R=0 initially. No compatibility, field or energy projection is applied during evolution.

All10 cases complete to normalized time0.05: both branches at17/33/65 nodes, both17-node half-step controls, and both17-node flat controls. No source changes interpolation cell.46 checks pass; largest relative energy drift4.97e-16, independent trajectory-Euler residual2.67e-13, and half-step whole-state difference3.56e-15. Inertia stays positive.

| Finest Schwarzschild case | Final b | Final V | Proper clock |
|---|---:|---:|---:|
| Reference65 | 6.031480844651 | 0.029220573344 | 0.043781095842 |
| MTS65 | 6.031480841560 | 0.029220217402 | 0.043781095977 |

The close source trajectories are a diagnostic, not independent continuum truth or observational precision. No waveform-accuracy gate or general moving stability theorem has been established from this short interval.

Evidence:
- `source-intake/navier-stokes/20260914/annular-cut-curved-background-evolution-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-cut-curved-background-evolution-attempt02/status.json`

## 9. Unequal one-sided curvatures: a bound instead of another guessed correction

The split linear trial field has zero second derivative on either immediate side of the source. For a smooth continuum target with unequal one-sided second derivatives, the slope-jump lift does not remove every distributional third-derivative term exactly. That does not automatically create another order-one force defect.

Take theta in[eta,1-eta], eta>0 fixed, bounded one-sided C2 norms and bounded finite-stencil Gram weights. Taylor expansion gives the nodal target as an affine part plus its slope-jump hinge and an O(h^2) remainder near the interface. The inferred slope jump differs from the exact jump by O(h). Since G*rho=O(h),
\[
 G_bq=O(h^2)
\]
on the fixed number of interface rows. At fixed nodal values, partial_b(G_bq)=O(1): j_b*q=O(1), partial_b(j_b^Tq)=O(1/h), G*rho=O(h), and G*partial_b(rho)=O(1). Positive bounded coefficient sampling then gives
\[
 \boxed{E_{Gram,interface}=O(h^3),\qquad
          \partial_bE_{Gram,interface}=O(h).}             \tag{11}
\]
This is a local interface bound, not a global C2 bulk truncation bound or an exact cancellation of the curvature jump. It requires the positive phase margin; it does not extend uniformly through a cell crossing.

Fifteen piecewise-quadratic cases with unequal curvatures across17..257 nodes and three phases verify the mechanism. Worst-phase measured orders are3.00159 for energy and1.00289 for the full source shape force.18 checks pass including the incompatible-initial-trace energy identity. No Gram rows were deleted and no numerical force was replaced by a target.

Evidence: `source-intake/navier-stokes/20260914/annular-cut-interface-regular-limit-attempt01/status.json`.

## 10. Next implementation and remaining limits

The next step is concrete: use (3) inside a finite-width solver for (5), with actual overlapping source/Gram supports and fixed physical width during refinement. Evolve the canonical variables, recompute the metric, and independently compare the resulting mu_t with (7)-(8). Do not impose the current as an energy correction or transfer the older action's live-gravity pass.

Keep source-cell events terminal until a transfer law is derived. Keep source layers ordered; earlier dust focusing remains relevant. Parent ownership of source mass/reflectivity, uniqueness of the boundary extension, one-sided decoupling, angular Einstein equations, PPN and the broader unified-theory sectors remain distinct questions.

## 11. Reproducibility

Executed files and attempts remain immutable. New current implementation:
- `scripts/annular_covariant_cut_action_20260915.py`
- `scripts/annular_covariant_cut_action_v2_20260915.py`
- `scripts/qualify_annular_covariant_cut_20260915.py`
- `scripts/qualify_annular_covariant_cut_v2_20260915.py`
- `scripts/verify_annular_cut_transport_current_20260915.py`
- `scripts/verify_annular_cut_metric_and_inversion_20260915.py`
- `scripts/run_annular_cut_curved_background_20260915.py`
- `scripts/annular_cut_initial_data_20260915.py`
- `scripts/run_annular_cut_curved_background_v2_20260915.py`
- `scripts/verify_annular_cut_interface_regular_limit_20260915.py`

At most two own one-core BelowNormal workers; no subagents or unrelated process changes. The background jobs completed and no long calculation remains running.
