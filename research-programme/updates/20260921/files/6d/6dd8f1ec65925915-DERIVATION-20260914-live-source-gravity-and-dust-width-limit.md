# Live source gravity, the dust-width limit, and the remaining moving scalar assembly

Private local checkpoint, 2026-09-14 UTC (completed after midnight UK time).
No GitHub action. This is a conditional spherical action calculation, not the full MTS-to-GR limit or an observational claim.

## 1. Result and scope

We have now evolved the proposed minimally embedded source with **live self-gravity**, not a prescribed force. With the scalar field exactly zero, the reference and MTS/Gram scalar terms vanish identically and share this same matter/gravity control.

The source trajectories and clocks agree with independent GR dust solutions at numerical precision. A separate calculation exposes a real restriction: independently moving pressureless layers cannot be squeezed to zero thickness while maintaining a uniformly ordered classical source for a fixed nonzero duration. We derive the crossing-time law, check it against GR, and stop at the first crossing.

We also derive and test the **nonzero-scalar curved radial constraints, scalar canonical equations and total source embedding covector**. This supplies the equations for the next coupled calculation; it is not falsely labelled a completed scalar-plus-gravity evolution.

Retained assumptions: the inherited Einstein spherical gravity sector, the declared minimal proper-time matter embedding, ideal reflecting endpoint, positive source energy S, and the existing full factor matrices. S=0.003, kappa=0.1, central geometric mass0.8 and radii near6 are normalized test inputs, not parent-derived dimensional predictions. The restriction of a model to an already specified Einstein sector is not a derivation of Einstein gravity from the complete MTS parent.

Ancestry:
- `DERIVATION-20260914-moving-finite-collar-source-action.md`
- `DERIVATION-20260914-coupled-moving-source-GR-control.md`
- `DERIVATION-20260913-proper-clock-source-action-and-live-initial-backreaction.md`
- `DERIVATION-20260912-nonlinear-history-Euler-equations.md`

## 2. Source and live gravity equations

Use the previous metric convention
\[
 ds^2=-N^2dt^2+(dR+\beta dt)^2/U^2+R^2d\Omega^2,\qquad
 U^2=F=1-2\mu/R.
\]
Vary the parent shift dependence before setting the canonical gravity momentum P=0 and beta=0. Denote source labels by z in [-1/2,1/2], normalized positive interior weight w(z), radius b(z,t), and particle momentum per unit label weight p_s. This is not the total source momentum once the scalar is active.

The unforced clock Routh reduction already gave
\[
 L_s=-S\sqrt{N^2-(V+\beta)^2/U^2},\qquad
 H_s=N E_s-\beta p_s,\quad E_s=\sqrt{S^2+U^2p_s^2}.
\]
For ordered layers J=b_z>0, lapse and radial-metric variations of this source and the inherited gravity action give
\[
 \mu_z=\kappa w U E_s,\qquad
 (\log N)_z=J\frac{\mu}{b^2F}
       +\frac{\kappa w U p_s^2}{bE_s}.                         \tag{1}
\]
Boundary conditions are mu(-1/2)=0.8 and N(1/2)=U(1/2): the clock is normalized to the vacuum exterior's Schwarzschild time at infinity. This is not the old held-source clock normalization copied unchanged.

Hamilton's source equations are
\[
 \dot b=\frac{NFp_s}{E_s},\qquad
 \dot\theta=\frac{NS}{E_s},\qquad
 \dot p_s=-E_sN_R-NUU_Rp_s^2/E_s.                            \tag{2}
\]
Here the derivatives are physical areal-radius derivatives of the live metric. Substituting (1) makes the terms proportional to w/J cancel:
\[
 \boxed{\dot p_s=-\frac{N\mu}{b^2}
          \left(\frac{E_s}{F}+\frac{p_s^2}{E_s}\right).}       \tag{3}
\]
The checker compares the unsimplified gradients and (3); this cancellation was not used to erase a missing force.

The source shift variation gives the independent temporal mass equation
\[
 (\partial_t\mu)_R=-\kappa NU^3p_s\,w/J=-\dot b\,\mu_R.       \tag{4}
\]
Thus enclosed material mass should be constant. It is **not imposed** by the numerical evolution: (1) is solved anew at every right-hand-side evaluation.

For an analytic consistency argument, differentiate the Volterra equation
\(\mu=\mu_{\rm inner}+\int\kappa w UE_s\,dz\).
At fixed mu, the derivative of UE_s along (2)-(3) vanishes. Therefore the actual material mass derivative obeys a homogeneous linear Volterra equation. Its unique regular solution is zero. This avoids assuming mass conservation in order to prove it.

Consequently
\[
 v=\frac{db}{d\theta}=\frac{Fp_s}{S},\qquad
 \frac{dv}{d\theta}=-\frac{\mu}{b^2},\qquad
 {\cal E}=\frac{UE_s}{S}=\sqrt{F+v^2}=\text{constant}.        \tag{5}
\]
The Newton-looking proper acceleration is the spherical GR dust equation in these variables; it is not the complete Newtonian limit of MTS.

## 3. Independent GR comparison, including clocks

For initially resting dust, radius b0 and enclosed mass mu, use the exact cycloid
\[
 b=\frac{b_0}{2}(1+\cos\eta),\quad
 \theta=\sqrt{\frac{b_0^3}{8\mu}}(\eta+\sin\eta),\quad
 v=-\sqrt{\frac{2\mu}{b_0}}\tan(\eta/2).                     \tag{6}
\]
Each numerical layer is compared at **its own integrated proper clock**, not at an incorrectly shared coordinate time.

The initially orthogonal dust proper-time slicing also supplies a separate clock/label check. If b_z|theta is the derivative of (6) at fixed proper time,
\[
 \theta_z|_t=-vJ/F,\qquad
 J=\frac{F}{{\cal E}^2}\,b_z|_\theta.                        \tag{7}
\]
Both identities are tested before crossing. They prevent a match to the single-particle acceleration from hiding a wrong relation between the common metric and the source clocks.

At fixed width0.001, with b0=6+width*z, the live calculation runs to exterior time1.6. Degree8,12,16,24 source-label collocations and an independent halved time step pass the same gates.

| Source-only result | Value |
|---|---:|
| Largest radius discrepancy over the five runs | 9.77e-15 |
| Largest proper-speed discrepancy | 6.48e-16 |
| Halved-step whole-state difference | 1.51e-14 |
| Largest binding-integral discrepancy | 3.34e-16 |
| Smallest layer Jacobian | 0.00099564108698 |
| Smallest F | 0.73233703 |
| Degree24 final central radius | 5.979133256342817 |
| Degree24 final central proper clock | 1.3694992441881642 |

Enclosed/exterior mass changes are zero at floating-point resolution; complex-step material mass-rate checks are below5.23e-23. These are error diagnostics in one normalized preparation, not exact numerical proofs or measured precision. Errors already at roundoff do not establish a spectral convergence rate. An independent zero-gravity inertial control also passes.

Evidence: `source-intake/navier-stokes/20260914/annular-source-gravity-algebra-attempt01/status.json` (12 checks), `source-intake/navier-stokes/20260914/annular-source-gravity-evolution-attempt01/status.json` (24 checks).

## 4. Derived limitation: freely moving dust layers focus

At rest, b0=B+epsilon*z, J0=epsilon and p_s0=0. Equations (1)-(3) give
\[
 b_{tt}(0,z)=-N_0^2\mu_0/b_0^2,
\]
\[
 J_{tt}(0,z)=-\frac{N_0^2\mu_{0,z}}{b_0^2}
 +2N_0^2\epsilon
 \left(\frac{\mu_0}{b_0^3}-\frac{\mu_0^2}{b_0^4F_0}\right).
                                                                    \tag{8}
\]
The negative self-loading term remains finite as epsilon shrinks; the positive central tidal stretching is only order epsilon. The scalar field is zero, so a Gram correction cannot remove this common dust effect.

### A conditional local asymptotic result, not just a quadratic guess

An exact alternative to the lapse equation eliminates label derivatives:
\[
 N(z)=U(z)\exp\left[-\int_z^{1/2}
 \frac{\kappa w(S^2+2Fp_s^2)}{bUE_s}\,dz'\right].             \tag{9}
\]
The mass constraint is a nonlinear Volterra equation. In material variables these equations and the source flow have a regular local extension through J=0 when b, F and S stay strictly positive. Such an extension is useful for the asymptotic calculation, **not** a physical single-stream solution after crossing.

For a fixed smooth weight and fixed positive kappa,S, take the limit epsilon=0 in this regular material system. Let W(z)=integral[-1/2,z]w. Initially,
\[
 U_0(z)=U_{\rm in}-\frac{\kappa S}{B}W(z),\qquad
 N_0(z)=U_{\rm out}=U_{\rm in}-\frac{\kappa S}{B}.
\]
Define
\[
 C_0(z)=\frac{U_{\rm out}^2\kappa S\,w(z)U_0(z)}{B^2},
 \qquad C_{\max}=\max C_0>0.
\]
On a uniform regular material neighbourhood, time reversal makes b even in t. Its uniform C1 Taylor remainder gives
\[
 J(t,z)=\epsilon-\tfrac12 C_0(z)t^2
          +O(\epsilon t^2+t^4).
\]
With t=sqrt(epsilon)*s this becomes
\[
 J/\epsilon=1-\tfrac12C_0(z)s^2+O(\epsilon).
\]
Uniform convergence and positivity before the first zero imply
\[
 \boxed{t_{\rm cross}/\sqrt{\epsilon}\longrightarrow
           \sqrt{2/C_{\max}}.}                              \tag{10}
\]
This conclusion is restricted to the specified initially resting independent dust family and the regular material extension. It does not assert global well-posedness, absence of other singularities for arbitrary data, or failure of a weak/multistream or interacting-matter limit.

For w=6(z+1/2)(1/2-z), B=6, kappa=0.1, S=0.003 and mu_inner=0.8:
C_max=7.84871857758e-6 and sqrt(2/C_max)=504.795667857.

| Initial width | First crossing time | Time/sqrt(width) |
|---|---:|---:|
| 1e-4 | 5.192384626 | 519.238463 |
| 1e-5 | 1.600677034 | 506.178523 |
| 1e-6 | 0.504933350 | 504.933350 |
| 1e-7 | 0.159634735 | 504.809356 |

Seven widths plus degree/time-step controls were run. The narrow-width fitted exponent is0.500224516, consistent with the derived1/2. The independent GR clock/label formula agrees within2.18e-12. The event uses minima of the finite interpolating polynomial, with a degree check; it is not a certified interval enclosure of a continuum event.

F remains above0.723 in these runs: these events are not horizon crossings. **That does not make the spacetime smooth at crossing**: the nonzero matter loading divided by J produces a divergent single-stream density. Physical interpretation stops there. No particle sorting, artificial pressure, rigid layer lock, or post-crossing negative-density continuation is used.

Turning off source self-loading while retaining the central Schwarzschild geometry removes the early crossing in the1e-7 control through time1.6. This isolates the cause rather than blaming the integrator or MTS.

Evidence: `source-intake/navier-stokes/20260914/annular-source-gravity-focusing-attempt01/status.json` (39 checks), `source-intake/navier-stokes/20260914/annular-source-gravity-limit-algebra-attempt01/status.json` (9 checks).

For literature context, [Hellaby and Lake, *Shell Crossings and the Tolman Model*, ApJ290 (1985),381-387](https://adsabs.harvard.edu/pdf/1985ApJ...290..381H) analyse shell crossings in GR dust and distinguish breakdown of its single-stream description from other collapse singularities. Our coefficient, scaling calculation and numerical tests above are local derivations, not results attributed to that paper.

### Why the previous thin initial-data check remains valid

The zero-width initial mass profile integrates exactly to
\[
 \mu_{\rm out}-\mu_{\rm in}
 =\kappa S U_{\rm in}-\frac{(\kappa S)^2}{2B}.
\]
This is the resting Israel-shell mass jump. Matching this **initial** jump does not prove that a family of independent dust layers evolves as a single collective Israel surface on a uniform fixed time interval. The latter requires additional dynamics or a different limiting construction. The earlier static matching evidence is retained, not retracted or promoted beyond its scope.

## 5. Nonzero-scalar radial and embedding assembly

We do not stop at the dust obstruction. The following remaining covectors are derived directly from the moving full-factor action and tested on nonconstant curved metric slices in **both** branches.

For one source layer, let R_i=a+H*xi_i, H=b-a, fixed inner anchor a, physical factor spacing DeltaR=H*delta_xi, and nodal quadrature Omega_i=H*omega_i. Endpoint Omega_b=DeltaR/2 must not be confused with DeltaR. Let T=diag(xi)D_xi/H, q_b=dot(q_b)=0, r=dot(q)-V*Tq, and
\[
 M_i=\frac{\Omega_i R_i^2}{N_iU_i},\quad
 A_f=(Bq)_f,\quad d_f=\frac{\sum_i S_{fi}R_i^2N_iU_i}{\Delta R}.
\]
B and S here denote the full derivative and coefficient-sampling matrices, not source mass. At P=0, lapse/mass variations do not change the zero connection, but P variations still require the previous transported current.

Include the endpoint kinetic term before eliminating its trace:
\[
 L_h=\tfrac12\sum_i M_i r_i^2-\tfrac12\sum_f d_f A_f^2
          -S\sqrt{N_b^2-V^2/U_b^2}.                          \tag{11}
\]
Free scalar canonical momenta are pi_i=M_i*r_i. The endpoint momentum is dependent:
\[
 \pi_b=-\frac{\Omega_b b^2U_bp_s}{E_s}(Tq)_b .
\]
Define nodal energy loading
\[
 v_i=\frac{R_i^2}{2\Delta R}\sum_f S_{fi}A_f^2,\qquad
 e_i=\frac{\pi_i^2}{2\Omega_iR_i^2}+v_i.                    \tag{12}
\]
The metric covectors at fixed velocities and embedding are
\[
 \frac{\partial L_h}{\partial N_i}
       =-U_ie_i-\delta_{ib}E_s,\qquad
 \frac{\partial L_h}{\partial\mu_i}
       =\frac{N_ie_i}{R_iU_i}
          +\delta_{ib}\frac{N_bp_s^2}{bE_s}.                 \tag{13}
\]
Do not differentiate a substituted Hamiltonian holding p_s fixed when the actual total source momentum is fixed.

Pushing each node/layer covector to physical areal radius, define e_h(R)=integral dz*w*sum_i e_i*delta(R-R_i(z)); retain the individual source p_s,E_s values inside analogous integrals. If rho_s is shorthand for the source pushforward, the radial equations read
\[
 \mu_R=\kappa(F e_h+U E_s\rho_s),\qquad
 \frac{N_R}{N}=\frac{\mu}{R^2F}+\frac{\kappa e_h}{R}
                    +\frac{\kappa U p_s^2}{RE_s}\rho_s.    \tag{14}
\]
Products with rho_s mean that weighted pushforward, not an averaged momentum incorrectly multiplied by an averaged density. Evaluating smooth densities requires ordered maps at every active node, not merely at the outer source.

### The correct source canonical variable has a unique local inversion

Let a_h=M_b*(Tq)_b^2 and eta=a_h*V. The source coordinate's full canonical momentum is
\[
 P_B=p_s+\eta-\pi_{\rm free}^T(Tq)_{\rm free},\qquad
 \eta=\frac{\Omega_b b^2U_bp_s}{E_s}(Tq)_b^2.               \tag{15}
\]
Given geometry and the scalar state, the required equation is
\[
 p_s+\eta(p_s)=P_B+\pi_{\rm free}^T(Tq)_{\rm free}.
\]
Its derivative is
\[
 1+\frac{\Omega_b b^2U_b S^2(Tq)_b^2}{E_s^3}>0.
\]
It is onto the real line and strictly monotone for positive S,U,Omega. Thus the particle momentum is uniquely recovered **at fixed geometry**, and the lapse cancels from this inversion. This does not establish uniqueness of the entire coupled nonlinear metric solve.

For the actual embedding force use dot(P_B)=partial_b L_h. At fixed q,dot(q),V and physical metric histories,
\[
 M_{i,b}=M_i[H^{-1}+2\xi_i/R_i-\xi_i(\log NU)_R],
\]
\[
 d_{f,b}=\frac{\sum_iS_{fi}\xi_i[2R_iN_iU_i+
                 R_i^2(NU)_{R,i}]}{\Delta R}-d_f/H,
\]
\[
 a_{h,b}=a_h[2/b-H^{-1}-(\log NU)_{R,b}],
\]
\[
 \boxed{
 \dot P_B=\tfrac12\sum_{\rm free}M_{i,b}r_i^2
 +\frac{V}{H}\pi_{\rm free}^T(Tq)_{\rm free}
 +\tfrac12a_{h,b}V^2-\tfrac12\sum_f d_{f,b}A_f^2
 -E_sN_{R,b}-N_bU_bU_{R,b}p_s^2/E_s.}                     \tag{16}
\]
The scalar equations are
\[
 \dot q=M_{\rm free}^{-1}\pi+V(Tq)_{\rm free},\qquad
 \dot\pi=-B_{\rm free}^T(dA)-VT_{\rm free}^T\pi
                      +\tfrac12V^2\partial_{q_{\rm free}}a_h. \tag{17}
\]
These include endpoint inertia and metric evaluation at the moving radius. They are not the old flat acceleration formula with a gravitational force added afterwards.

Substituting (14) into just the last two, purely gravitational, terms in (16) yields
\[
 -\frac{N\mu}{b^2}(E_s/F+p_s^2/E_s)
 -\frac{\kappa NS^2e_h(b)}{bE_s}.
\]
Own-source density terms again cancel. The scalar embedding terms in (16) remain; this last expression alone is **not** the complete reflecting-source radiation force.

At17/33 nodes, both full reference and MTS matrices pass complex-step action derivatives for N,mu,b,V,q,dot(q), independent five-point b variations, and canonical inversion. Maximum derivative mismatch is1.12e-16; the independent embedding differences are below3.01e-15. Omitting endpoint inertia is detectably wrong in every case. These are manufactured-slice action checks, not a live evolution or a finite moving Ward theorem.

Evidence: `source-intake/navier-stokes/20260914/annular-moving-curved-radial-assembly-attempt01/status.json` (39 checks).

## 6. What to do next, without hiding the dust issue

The source-only GR gate is now passed for its declared regular finite-width interval. The necessary nonzero-scalar radial and embedding equations are no longer missing.

Next implementation:
1. Evolve q,pi,b,P_B with (14)-(17), using a fixed, declared finite physical source width during numerical refinement. The present width0.001 is only a control preparation, not a derived material length.
2. Reconstruct shared geometry on the actual moving nodal maps, including overlapping layer bands if they occur. The old disjoint static-band solver cannot simply be reused once width and scalar spacing are independent.
3. Retain the full previous P-current, including transported-factor, moving-node and temporal boundary terms. Check mu_t independently against the time derivative of the radial solution; do not enforce both and call the residual a test.
4. Run the same small nonzero pulse in reference/MTS, refine scalar and layer resolution separately, compare with a matching **finite-width** continuum source model, and stop if any active map loses order.
5. Treat a zero-width collective Israel source as a separate derivation problem. Do not silently impose rigidity or claim the old single-shell continuum control is the exact finite-width target.

No physical pressure, cohesion, reflectivity law or width has been newly derived. No wave-plus-live-gravity evolution from this finite action has yet been run. No unrestricted GR limit, local observational pass, black-hole resolution, or unique complete parent matter action is claimed.

## 7. Reproducibility

New scripts:
- `scripts/annular_source_gravity_collar_20260914.py`
- `scripts/derive_annular_source_gravity_20260914.py`
- `scripts/run_annular_source_gravity_20260914.py`
- `scripts/run_annular_source_gravity_focusing_20260914.py`
- `scripts/derive_annular_source_gravity_limit_20260914.py`
- `scripts/derive_annular_moving_curved_radial_assembly_20260914.py`

All123 current mathematical/numerical/implementation checks passed. Raw evolution states and executed sources are saved before analysis. Existing evidence is immutable; reruns need new attempt names rather than overwriting completed directories. One BelowNormal single-core numerical worker was used at a time, with no subagents or unrelated process changes.

