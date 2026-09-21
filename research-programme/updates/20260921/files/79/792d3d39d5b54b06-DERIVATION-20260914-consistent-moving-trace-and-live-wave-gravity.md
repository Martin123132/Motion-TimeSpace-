# A consistent moving trace: nonzero scalar, source and live gravity

Private local derivation and numerical checkpoint, started2026-09-14 UTC and continued2026-09-15. No GitHub action or changes to the protected workbench.

## 1. The advance, and the change of route

The straightforward affine moving-grid assembly failed an independent local Einstein-equation test in **both** reference and MTS branches. Its source-only GR and flat wave/source controls still passed, and its exterior mass was conserved. Those facts did not cure the local failure.

Instead of adjusting the failed current or declaring it good enough, we constructed a separate action: keep the scalar sampling grid fixed in physical radius, and let the source move through a **covariantly transported reflecting trace**. The scalar and particle forces come from that action and its constraint multiplier. This is a change of finite coupling, not a numerical correction applied to the old action.

The new model passes its nonzero-velocity local-current qualification, proper-clock/added-action covariance checks, and independent radial/energy controls. Paired live evolutions are recorded below.

Passing those identities is **not sufficient to certify its source force**. The static source-versus-grid-position audit below is a separate acceptance gate; no accurate boundary-force claim follows from conservation alone.

Important scope:
- This is a conditional spherical Einstein-scalar/source sector with the existing complete reference/MTS factor matrices. It is not a derivation of the full Einstein action from the entire MTS parent.
- The pilot is a **two-sided** scalar field with a moving internal zero-trace source. Equivalence to the earlier one-sided moving endpoint is not proved.
- Positive source massS=0.003, initial width0.001, central geometric mass0.8, kappa=0.1, grid interval[3,7] and source centre6.03 are declared normalized inputs, not observations or newly derived constants.
- Initial width is held fixed across numerical resolutions; subsequent source thickness evolves freely. No rigid lock, pressure, cohesion, or energy-conservation projection is inserted.
- The earlier dust caustic restriction remains relevant. The present calculation does not remove it.
- The independent gravity checks here concern the sourced radial/lapse equations and temporal mass current. An unrestricted angular-stress/Einstein-tensor or PPN qualification does not follow automatically.

Ancestry: `DERIVATION-20260914-live-source-gravity-and-dust-width-limit.md` and `DERIVATION-20260914-moving-finite-collar-source-action.md`.

## 2. Why the first coupled assembly did not qualify

The implementation of the previous action's P=0 radial, scalar and total embedding equations was first compared with independent old controls. The dust-force and flat-action comparisons passed. Nevertheless, differentiating the live radial mass constraint along its computed state derivative disagreed with the current obtained from varying P:

| Initial33-node qualification | Reference | MTS |
|---|---:|---:|
| Maximum local mass-current discrepancy | 6.38878e-5 | 6.64413e-5 |
| Gate, unchanged | 2e-7 | 2e-7 |
| Relative to largest sampled current | 0.9900% | 1.0296% |
| Exterior mass rate magnitude | 7.71e-17 | 7.85e-17 |

The failed evidence remains `source-intake/navier-stokes/20260914/annular-moving-live-gravity-qualification-attempt01/status.json`. Nothing there is relabelled a pass.

### A transport obstruction, not just insufficient quadrature

At leading weak backreaction, write the scalar nodal energy as e_i=k_i+v_i, with kinetic and potential loadings k_i,v_i, and let W_i be the velocity of its sampling point. In distribution notation the lapse constraint contains
\[
 \mu_R/\kappa-\sum_i e_i\delta(R-R_i(t)).
\]
Its time derivative contains the advective density-derivative term
\(\sum_i e_iW_i\delta'(R-R_i)\).
But the derived affine action's direct nodal P-current gives
\[
 \mu_t/\kappa\supset-2\sum_i v_iW_i\delta(R-R_i).
\]
The linked factor currents have indicator-function support at this order; their radial derivatives supply endpoint deltas, not the missing delta derivatives. The uncancelled transport coefficient is therefore
\[
 \boxed{(k_i-v_i)W_i\,\delta'(R-R_i).}
\]
Generic moving wave data do not make it vanish. Smooth layer averaging regularizes these distributions but does not automatically enforce the missing identity. The accompanying finite-width diagnostic checks the defect's quadrature stability and inverse-width leading behaviour.

In contrast, the dust source's derivative coefficient cancels: in this weak-gravity notation E_s V=p_s. In the exact curved formula it is E_s V=NU^2p_s. This explains why the source-only control passed. At zero gravitational coupling there is no local Einstein mass equation to fail, so the old flat-action conservation test also remains valid.

This diagnoses the **proposed all-time P=0 affine branch**, not every conceivable nonzero-P history of that action or the full MTS programme. A time-coordinate transformation acting differently at different radii does not preserve a prescribed affine motion of all interior nodes with one endpoint coordinate. The previous manufactured action variations were correct variations of that restricted action; they did not prove the missing moving-grid gauge identity.

Evidence: `source-intake/navier-stokes/20260914/annular-affine-moving-current-obstruction-attempt01/status.json`.

## 3. The alternative action

Retain the old physical metric and parent relation
\[
 ds^2=-N^2dt^2+(dR+\beta dt)^2/U^2+R^2d\Omega^2,\quad
 U^2=1-2\mu/R,\quad \beta=\kappa NU^3P.
\]
Keep the full fixed-node covariant scalar action, including all MTS Gram rows. Each scalar grid is fixed at R_i(z)=R_i^{base}+epsilon*z; only its source b(z,t) moves.

For source position between adjacent nodes, let f_i(b) be the two nonnegative linear interpolation weights, summing to one. They are a declared finite approximation to the trace, not a fitted source profile.

At nonzero P the trace is **not** an interpolation of simultaneous coordinate-time samples. Transport each scalar history along the inherited horizontal connection:
\[
 c=\frac{\beta}{N^2U^2-\beta^2},\quad
 \partial_R T=c(T,R),\qquad T(t,b(t))=t,
\]
\[
 \Phi_h(t,z)=\sum_i f_i(b(t,z))q_i(T_i(t,z),z).
\]
Add the source and trace action
\[
 \boxed{I_{\rm src}=\int dt\,dz\,w(z)
     \left[-S\ell+\Lambda\Phi_h\right],\qquad
 \ell=\sqrt{N_b^2-(V+\beta_b)^2/U_b^2}.}                    \tag{1}
\]
Here Lambda is a source-time density multiplier, not a cosmological constant or fitted force. Equivalently Lambda=ell*lambda with a scalar proper-time multiplier; the constrained Euler equations agree. Vary the action before imposing Phi_h=0.

### Added-action time-coordinate covariance

For an admissible physical time relabelling t_old=H(t_new,R), the source transforms implicitly as
\[
 b_{\rm new}(t)=b_{\rm old}(H(t,b_{\rm new}(t))),\quad
 V_{\rm new}=\frac{V_{\rm old}H_t}{1-V_{\rm old}H_R}.
\]
The source clock factor is J_b=H_t+H_R V_new. The horizontal connection transforms as c_new=(c_old(H)-H_R)/H_t. Its transported endpoint satisfies the conjugacy relation
\[
 H(T_i^{new},R_i)=T_i^{old}(H(t,b),R_i).
\]
Thus Phi_h is a scalar at the source event, ell_new=J_b*ell_old and Lambda_new=J_b*Lambda_old. The action density in (1) transforms by J_b, with the same physical endpoint events.

An independent manufactured calculation integrates these links in the transformed curved metric. It verifies the proper clock, scalar trace, action density and integrated action over corresponding source events. Replacing the linked trace with naive simultaneous interpolation demonstrably fails. This proves/tests the stated added-action time relabelling, not arbitrary spatial-diffeomorphism invariance of a finite lattice.

## 4. Instantaneous P=0 equations: the source force is derived

At P=0 the links are simultaneous, but their P variations must still be retained. Use scalar canonical momenta pi_i including positive nodal quadrature Omega_i, full factor amplitudes A_f=(Bq)_f, coefficient sampling matrix S_fi, and fixed radial spacing h:
\[
 e_i=\frac{\pi_i^2}{2\Omega_iR_i^2}
       +\frac{R_i^2}{2h}\sum_f S_{fi}A_f^2,\qquad
 E_s=\sqrt{S^2+U_b^2p_s^2}.
\]
S_fi is the coefficient-sampling matrix, distinct from source massS. Phi=sum_i f_i q_i and g_b=sum_i f_{i,b}q_i.

The scalar and source equations from (1) are
\[
 \dot q_i=\frac{N_iU_i}{\Omega_iR_i^2}\pi_i,
\]
\[
 \dot\pi_i=-\frac1h[B^T(A\,(S(R^2NU)))]_i+\Lambda f_i,
\]
\[
 \dot b=V=\frac{N_bU_b^2p_s}{E_s},\qquad
 \dot p_s=-E_sN_{R,b}-N_bU_bU_{R,b}p_s^2/E_s+\Lambda g_b,
\]
\[
 \dot\theta=N_bS/E_s,\qquad \Phi=0.                         \tag{2}
\]
There is no freely prescribed recoil force. The previous endpoint half-cell inertia is not copied into this **different** coupling: the constrained fixed-grid field remains in the canonical system rather than being eliminated as a moving endpoint.

On the constraint surface the multiplier term contributes neither lapse nor mass density. Its variations still contribute scalar force, source force and transported current. Dropping it because Phi=0 before variation would lose the coupling.

The live radial equations remain
\[
 \mu_R=\kappa\left[U^2 e_h
       +U\int wE_s\delta(R-b)\,dz\right],
\]
\[
 \frac{N_R}{N}=\frac{\mu}{R^2U^2}+\frac{\kappa e_h}{R}
       +\frac{\kappa U}{R}\int w\frac{p_s^2}{E_s}\delta(R-b)\,dz,
 \quad e_h=\int w\sum_i e_i\delta(R-R_i)\,dz.                \tag{3}
\]
Overlapping scalar/source bands are summed before solving these constraints. The outer clock is normalized by N_outer=U_outer in the exterior vacuum; inner mass is fixed. Geometry is recomputed from the current state, not forced to retain its initial mass.

### How Lambda is determined

Differentiate the reflecting constraint:
\[
 \dot\Phi=f\cdot\dot q+Vg_b=0.
\]
For X=(q,pi,b,p_s,theta), write the state equation as Xdot=F0(X)+B_Lambda(X)Lambda. Then solve
\[
 [D_X\dot\Phi\,B_\Lambda]\Lambda=-D_X\dot\Phi\,F_0.           \tag{4}
\]
The differentiation includes the implicit live mass and lapse response. The implementation differentiates the radial solution and solves the small coupled layer matrix. It does not project the positions, fields or energy back onto a target after each step.

In flat spacetime, the layer matrix is diagonal with positive entry
\[
 \sum_i\frac{f_i^2}{\Omega_iR_i^2}
       +\frac{S^2g_b^2}{E_s^3}>0.
\]
The exact flat matrix is checked independently. The live-gravity matrix is not declared positive for all states; its conditioning is checked in the pilot.

The energy exchange of the constraint force is
\[
 {\cal P}_{wave}+{\cal P}_{src}
 =\Lambda(f\cdot\dot q+Vg_b)=\Lambda\dot\Phi=0.              \tag{5}
\]
This is a derived exchange law, not an energy correction added to the evolution.

## 5. The missing source-to-grid current is retained

The moving-anchor shift variation at P=0 gives
\[
 \delta T_i=\int_b^{R_i}\frac{\delta\beta}{N^2U^2}\,dR,\qquad
 \delta I_{\rm trace}=\int dt\,dz\,w\Lambda
              \sum_i f_i\dot q_i\,\delta T_i .
\]
Let I_ab(R)=sgn(b-a)*1_{min(a,b)<R<max(a,b)}. The trace current is
\[
 {\cal K}_{trace}(R)=\int dz\,w\Lambda
                      \sum_i f_i\dot q_i\,I_{bR_i}(R).
\]
With the unchanged full scalar factor current K_scalar,
\[
 \boxed{\mu_t=-\frac{\kappa U}{N}({\cal K}_{scalar}+{\cal K}_{trace})
       -\kappa NU^3\int w p_s\delta(R-b)\,dz.}              \tag{6}
\]
There is no affine moving-grid direct term, because the scalar nodes do not move. The source still does.

The integration includes oriented links, all factor rows and all physical layer weights. The action proof matches physical source-time endpoints. For the interior Euler equation in (6), shift variations have compact temporal support; temporal boundary terms are not reinterpreted as bulk sources.

This equation is tested **independently** against the time derivative of the solution of (3) along (2)-(4). Neither side is used to overwrite the other.

## 6. Controls before interpreting the evolution

- Nonzero-velocity trace qualification: local-current error<1.53e-13 in both branches against the unchanged2e-7 gate. Constraint position/rate and exterior mass-rate checks also pass.
-12 added-action/clock/flat-multiplier checks pass, including a deliberately wrong unlinked interpolation control.
-15 independent controls pass. A separate adaptive radial ODE agrees with the collocation geometry to2.34e-15 in mass and8.89e-16 in log lapse.
- Width0.16 explicitly exercises **three overlapping bands**; this is an implementation control, not a change of width in the physical refinement series. Its local-current test and real five-point time derivatives pass.
- Empty-wave dynamics agrees with the separate self-gravitating dust implementation. The flat field-plus-particle energy derivative vanishes without conservation projection.

Evidence:
- `source-intake/navier-stokes/20260914/annular-fixed-grid-moving-trace-qualification-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-fixed-trace-action-and-clock-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-fixed-trace-independent-controls-attempt01/status.json`

## 7. Coupled evolution results

Both paired series finish all eight cases: reference/MTS at 33, 65 and 129 nodes, followed by each 33-node half-step control. All reach normalized exterior time0.2 without an interpolation-cell event or a source-layer crossing. The 100 evolution checks pass, but the independent force gate in section8 still prevents promotion of these trajectories to accurate physical-source evidence.

| Common-smooth-data series | Final central source radius | Final proper clock | Maximum local mass-current error |
|---|---:|---:|---:|
| Reference33 | 6.025724584845 | 0.171323050714 | 3.25e-13 |
| MTS33 | 6.025853063589 | 0.171326666685 | 2.93e-13 |
| Reference65 | 6.025727304223 | 0.171321963398 | 3.46e-13 |
| MTS65 | 6.025716457985 | 0.171321388348 | 3.10e-13 |
| Reference129 | 6.025909623039 | 0.171328348207 | 3.53e-13 |
| MTS129 | 6.025878266859 | 0.171327184045 | 3.36e-13 |

Across both series, maximum relative active-energy drift is2.70e-12 and the largest whole-state half-step difference is2.28e-13. Active energy excludes the fixed central mass; a large background mass is not used to dilute this error. The minimum sampled metric factor F is0.466578. The finest final source maps remain ordered, with exactly minimized layer-polynomial Jacobians0.000898399 and0.000898489.

Independent final checks on49 off-grid source labels give trace/rate errors below8.57e-15. Raising the layer order4 to8 and radial order18 to24 changes the final right-hand side by at most5.44e-13. These12 comparison checks pass.

Wave self-refinement improves, but does not yet certify continuum accuracy:

| Maximum relative scalar L2 difference | 33 versus65 | 65 versus129 |
|---|---:|---:|
| Reference | 9.538% | 2.834% |
| MTS | 7.313% | 2.146% |

At129 nodes the reference/MTS wave difference is0.2701%, but two approximations agreeing with each other is not independent continuum truth. Source-position and clock refinement differences do not decrease monotonically. In particular, their displayed digits must not be read as equally precise continuum predictions. The subsequent static force counterexample supplies a reason to repair the boundary rather than keep refining this uncorrected coupling indefinitely.

Evidence:
- `source-intake/navier-stokes/20260914/annular-fixed-grid-moving-trace-evolution-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-fixed-grid-moving-trace-smooth-evolution-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-fixed-trace-evolution-comparison-attempt01/status.json`

The initial scalar displacement is smooth, two-sided and linear in a neighbourhood of the source. A first-derivative constraint preparation adjusts scalar momenta on the interpolation stencil so that the chosen nonzero source velocity satisfies dot(Phi)=0. It is applied **only to initial data**, not as a drift or energy projection. It is the same preparation rule for both branches.

That stencil-supported adjustment changes with grid resolution. We therefore also run a separate common-smooth-data series: qdot_i=-V_b*g(R_i), where g is the analytic gradient of the common initial scalar profile. The momenta pi_i=Omega_i*R_i^2*qdot_i/(N_i*U_i) are iterated with the live geometry and source velocity over the whole field support, not patched only on a stencil. The linear source neighbourhood makes Phi=dot(Phi)=0. This improves initial-data discipline, not by itself continuum accuracy or boundary stress.

All actual trajectories stop at exterior time0.2 or at the first source interpolation-cell event. The cell-event safeguard is part of the tested domain. An event-transfer law across a stencil change has not been derived here. Source layer order and positive F are independently monitored; regularity is not inferred from total energy alone.

## 8. Source-force accuracy is an independent gate

Take a planar unit interval with q(0)=1,q(1)=0 and an internal zero-trace barrier at b. The continuum minimum has E=1/(2b), zero exterior field, and outward force F=1/(2b^2). Put b inside a uniform grid cell of width h at fraction theta. For the reference derivative,
\[
 G_h(b,b)=b(1-b)-h\theta(1-\theta),\qquad
 E_h=\tfrac12+\frac{(1-b)^2}{2G_h(b,b)}.
\]
Differentiate with the grid fixed, so dtheta/db=1/h. Despite energy convergence,
\[
 \boxed{F_h/F_{continuum}\longrightarrow2\theta.}
\]
An order-h energy error can have an order-one source shape derivative. This is already a reference-model artifact, not an MTS-only failure. Possible force averaging over cell crossings is not a uniform pointwise force law.

There is a derived reference remedy: enrich the cut cell so the actual field vanishes at b while the neighbouring nodal values remain independent. Its exact gradient energy is
\[
 \frac{q_l^2}{2h\theta}+\frac{q_r^2}{2h(1-\theta)}
 =\frac{(q_r-q_l)^2}{2h}
 +\frac{[(1-\theta)q_l+\theta q_r]^2}{2h\theta(1-\theta)}.
\]
This **replaces** the old interpolated-trace constraint; adding the correction while retaining that constraint would do nothing. Its source shape derivative is the pressure difference
\[
 F_b=\frac{q_l^2}{2(h\theta)^2}-\frac{q_r^2}{2(h(1-\theta))^2}.
\]
The static audit tests both reference and all unchanged MTS Gram factors before and after this reference correction. It does not silently discard cross-interface Gram rows or identify a reference fix with a completed MTS boundary derivation.

The 48 static cases confirm that this is a real force problem, not a roundoff or time-step issue. At 257 nodes:

| Boundary construction | Force / exact force at cell fractions 0.2, 0.5, 0.8 | Worst relative error |
|---|---|---:|
| Reference interpolated trace | 0.398960, 1.003267, 1.605224 | 60.52% |
| Full MTS interpolated trace | 0.550167, 1.003609, 1.455289 | 45.53% |
| Reference split-cell energy | 1.000000, 1.000000, 1.000000 | 7.54e-14 |
| MTS with reference-only split correction | 1.151374, 1.000339, 0.849893 | 15.14% |

Thus both interpolated-trace models fail the same 0.5% pressure gate. The exact reference correction passes, but simply retaining the unchanged cross-interface MTS Gram action on top of that correction does not. Thirty-eight completed algebra/diagnostic checks record these verdicts; they are not 38 physical passes for the failed force laws.

Evidence: `source-intake/navier-stokes/20260914/annular-trace-static-force-phase-audit-attempt01/status.json`.

The moving cut-cell kinetic action, time-link current and complete MTS boundary lift do not follow from this static identity alone. The failed force gates mean the preceding coupled trace runs remain conservation/solver evidence, not accurate-source-force evidence. The following subsections construct separate partial repairs without relabelling those runs.

### 8.1 Derived moving kinetic terms for the reference split cell

This part is an exact restriction of the flat planar reference scalar action to a split linear trial field in c=1 units, not an assertion of a complete curved discretization. Write L=b-R_left, D=R_right-b and V=dot(b). The two pieces are
\[
 q_-(R)=q_l(b-R)/L,\qquad q_+(R)=q_r(R-b)/D.
\]
Their derivatives must be taken at fixed physical radius before integration. The result is
\[
 T_{cut}=\frac16\left[L\dot q_l^2+D\dot q_r^2
       +V(q_l\dot q_l-q_r\dot q_r)
       +V^2(q_l^2/L+q_r^2/D)\right],
\]
\[
 I_{cut}=\int dt\,[T_{cut}-q_l^2/(2L)-q_r^2/(2D)-S\sqrt{1-V^2}].
\]
The source canonical momentum is therefore
\[
 P_b=\frac{SV}{\sqrt{1-V^2}}+
       \frac{q_l\dot q_l-q_r\dot q_r}{6}
       +\frac V3(q_l^2/L+q_r^2/D).
\]
It is not just the material momentum. The velocity Hessian has positive field block diag(L/3,D/3), and its source Schur complement is exactly
\[
 \frac{S}{(1-V^2)^{3/2}}+\frac14(q_l^2/L+q_r^2/D)>0
\]
for S,L,D>0 and |V|<1. The finite flat kinetic system is therefore locally Legendre-regular under these conditions. Its autonomous energy is T_cut+E_cut+S/sqrt(1-V^2). No conservation projection is required.

Sixteen checks pass, including independent physical-coordinate quadrature and first variations at five source locations. Largest action-gradient error is 9.44e-12; an independent real-difference energy rate along the derived Euler equations is below 9.14e-12. This is not a global wave-evolution, source-cell-crossing or curved-current qualification.

Evidence: `source-intake/navier-stokes/20260914/annular-reference-cut-cell-kinetics-attempt01/status.json`.

### 8.2 A constructive MTS static interface lift, not a fitted force

The 15% residual identifies a specific issue: an unchanged third-difference Gram penalty sees the permitted slope jump of the reflecting field as a bulk defect. We can construct a boundary-adapted candidate without dropping Gram rows or fitting a force coefficient.

Let G be the entire inherited Gram factor matrix with its unchanged weights. For the split-cell field define
\[
 J=q_R(b^+)-q_R(b^-)=q_l/L+q_r/D=j_b^Tq,\qquad
 \rho_b(R_i)=(R_i-b)_+.
\]
In distribution notation, differentiating the hinge three times gives delta-prime. Thus subtracting J*rho_b removes the slope-jump contribution from the bulk third derivative. This motivates the explicitly declared **broken-bulk interpretation** of the Gram energy:
\[
 \boxed{G_b=G(I-\rho_bj_b^T),\qquad
 E_{candidate}=E_{reference,cut}+\|G_bq\|^2/(2h).}
\]
This changes the old boundary action. It is not an algebraic identity equating the old and new theories, nor a proof that the parent uniquely selects this boundary rule. Every old factor and weight remains, but the argument of factors that see the interface changes. Rows entirely away from the interface remain unchanged because G annihilates affine functions there. On a continuous-slope source trace, J=0 and the original Gram action is recovered.

There is a simple static proof. With arbitrary fixed endpoint values, the exact continuum minimizer is linear on each side of b. Subtracting its slope-jump hinge makes it globally affine, so G_bq_exact=0. The reference split-cell energy already attains its unique minimum there. Adding a nonnegative term that vanishes there preserves that minimum, its energy, and its full source shape derivative. Consequently the static pressure law is exact for every interior cell fraction, not merely at a specially selected mesh position.

The force implementation includes the derivative of the complete lifted factor,
\[
 F_G=-\frac1h(G_bq)^T(\partial_bG_b\,q),\quad
 \partial_bG_b=-G[(\partial_b\rho_b)j_b^T+\rho_b(\partial_bj_b)^T].
\]
It does not replace the computed recoil by the desired continuum answer after solving.

The static lift passes all 24 cases across 33/65/129/257 nodes, three cell fractions and two independent endpoint preparations. Largest relative force error is 4.06e-12 and profile error 2.40e-13. Forty algebra/implementation checks pass, including three independent full shape-derivative controls on non-equilibrium fields. This closes the static pressure defect **for this new boundary candidate**; the original 15.14% failure is preserved unchanged.

Evidence: `source-intake/navier-stokes/20260914/annular-Gram-interface-lift-static-attempt01/status.json`.

Limits are important: removing the first-derivative jump does not yet specify how to handle an arbitrary second-derivative jump, the complete time-transported curved action, or independent one-sided dynamics. Those are next derivations, not silently satisfied clauses. The new static candidate has not been used to relabel the preceding uncorrected coupled trajectories.

## 9. What remains

The next useful work is **not another search for a coupling coefficient**. We have a concrete covariant trace coupling with live energy transfer, a proved force defect in that finite approximation, and a separately derived static boundary candidate that fixes it. Those are three distinct results: the repaired candidate has not yet inherited the live evolution's conservation qualification.

Next:
1. Extend the derived split-cell kinetic terms and static Gram lift to one moving, time-transported curved action. Derive the remaining interface-jump terms and source canonical momentum, then recheck the independent temporal mass current. Do not keep the old trace multiplier or assume the old conservation test transfers to this changed action.
2. Derive and test the treatment of interpolation-cell crossings; do not conceal a change of active stencil inside an otherwise smooth proof.
   Include a source-versus-grid-position test: convergent field values alone would not exclude a spurious grid-dependent force or an incorrect limiting boundary stress.
3. Establish or reject the relation between this two-sided trace construction and the earlier one-sided reflecting source, including exterior-field and boundary-stress behaviour.
4. Extend the interval only while source ordering survives; a material mechanism or different weak-limit construction is still needed if a zero-width collective source is sought.
5. Keep the parent-origin questions distinct: source mass, reflectivity/material law, microscopic coupling ownership, unrestricted GR/Newton limits and the wider MTS sectors are not settled by this spherical pilot.

Nothing here is an observational local-GR pass, a black-hole solution or a complete unified field theory. The improvement is a coupled local-conservation test plus an identified boundary artifact and a constructive, tested static remedy. The remaining gap is the moving curved completion of that remedy, not whether any candidate force can be written at all.

## 10. Local implementation

- `scripts/annular_moving_live_gravity_20260914.py` and `scripts/qualify_annular_moving_live_gravity_20260914.py`: preserved affine trial and failed qualification.
- `scripts/diagnose_annular_affine_current_20260914.py`: obstruction diagnostic.
- `scripts/annular_fixed_grid_moving_trace_20260914.py`: separate fixed-grid/source-trace candidate.
- `scripts/qualify_annular_fixed_grid_moving_trace_20260914.py`: nonzero-velocity qualification.
- `scripts/verify_annular_fixed_trace_action_20260914.py`: proper-clock/action and multiplier tests.
- `scripts/verify_annular_fixed_trace_controls_20260914.py`: independent radial, overlap, dust, flat-energy and real-difference checks.
- `scripts/run_annular_fixed_grid_moving_trace_20260914.py`: paired live evolution and time-step checks.
- `scripts/annular_smooth_trace_preparation_20260914.py` and `scripts/run_annular_fixed_trace_smooth_20260914.py`: common smooth initial velocity and a separate paired series.
- `scripts/compare_annular_fixed_trace_evolution_20260914.py`: cross-resolution, off-grid and layer-resolution diagnostics.
- `scripts/audit_annular_trace_static_force_20260914.py`: static pressure, grid-phase and cut-cell audit in both branches.
- `scripts/derive_annular_reference_cut_cell_kinetics_20260915.py`: exact flat split-cell kinetic action, momentum and positive inertia.
- `scripts/derive_annular_Gram_interface_lift_20260915.py`: positive full-factor static boundary candidate, exact pressure and shape variations.

Executed files and evidence are immutable. Raw completed states are saved before analysis. At most two own one-core BelowNormal workers run at once; no subagents or unrelated process changes.
