# Coupled current hyperbolicity, constraint propagation and evolution

Private continuation, 2026-09-09. The preceding goal turn is verified as
progress: its scalar evolution outputs and source-completion records exist
and pass their stated checks. This turn connects the ordinary scalar current
to the mass/lapse equations instead of treating the metric as prescribed.

The substantive new result is a full five-field principal symmetrizer for the
ordinary constraint-reduced parent, with an exact constraint-propagation law.
The numerical experiment evolves the ordinary LINEARIZED coupled correction
around the saved approximate parent. It is not a finite-u, fully nonlinear,
calibrated MTS solution. The higher-curvature and physical-coupling tasks stay open.

## 1. Why simply attaching metric evolution is insufficient

Keep t=v-sigma(r-4), R=r, q=chi_t, w=chi_R, E=exp(delta),
F=1-2mu/r-Lambda*r^2/3, p=q/E, s=w-sigma*q, X=2p*s+F*s^2.
For the saved ordinary scalar polynomial,

    P=1-4b2*X-6b3*X^2, Q=P+2X*P_X,
    h=pi/r^2=P*[sigma*(2-sigma*E*F)*q-(1-sigma*E*F)*w],
    f=I/r^2=E*P*(p+F*s),
    alpha=h_q, B=f_q=-h_w, c=f_w, B^2+alpha*c=P*Q.

All alpha,B,c in this note are density-divided. Define the ordinary parent
metric sources and its tilted mass constraint by

    D0=kappa*r*P*s^2,
    C0=kappa*r^2*p*f,
    R0=kappa*r^2*[P*F*s^2/2+V+b2*X^2+2b3*X^3],
    G0=R0+sigma*C0, J=mu_R-G0, V=m_chi^2*chi^2/2.

The naive free-current evolution would be

    chi_t=q, w_t=q_R,
    h_t=f_R+2f/r-E*V_chi,
    mu_t=C0, delta_t=(delta_R-D0)/sigma.

Its scalar block is healthy when alpha>0 and P*Q>0. That does NOT automatically
make the full five-field principal matrix uniformly diagonalizable. A canonical
frozen-coefficient counterexample at F=0, E=1, sigma=1/20 has the (w,h,mu,delta)
principal matrix

    [[10,10, s/r, 0],
     [10,10,-s/r, 0],
     [ 0, 0,   0, 0],
     [ 0, 0,   0,20]].

For s!=0 the zero eigenvalue has algebraic multiplicity two but only one
eigenvector. A constraint-violating mass perturbation couples to the zero-speed
scalar characteristic, giving a Jordan chain. The exact checker uses r=2,
s=1/50: nullity(M)=1 while nullity(M^2)=2.

This concerns the unconstrained evolution formulation, not a physical
singularity of GR at a regular horizon. It disappears in vacuum s=0, and it
does not establish that earlier EXTERIOR curvature failures were caused by this
horizon issue. It does explain why the earlier scalar-only norm was insufficient
as a general coupled-gravity argument.

## 2. The constraint reduction is derived, not an assumed zero

The saved physical parent evolves p,s after substituting the mass/lapse
constraint equations. In current coordinates its exact ordinary reduction is

    h_t=f_R+2f/r-E*V_chi-f_mu*J,
    f_mu=-2E*[P_X*s^2*(p+F*s)+P*s]/r,

with the other four equations as above. No coefficient is fitted to a test:
f_mu is the current's derivative with respect to mass at fixed chi,q,w,delta,r.
The term -f_mu*J is kept when J is nonzero. Dropping it would change the
off-constraint reduction; setting J=0 by hand would conceal the discrepancy.

At the canonical horizon the reduction changes the second-row mass entry from
-s/r to +s/r. The double zero then has two eigenvectors. More generally the
following exact five-field change of variables proves a stronger statement.

Let z=(chi,p,s,mu,delta) and y=(chi,w,h,mu,delta). Their perturbation map T is

    dchi_y=dchi_z,
    dw=sigma*E*dp+ds+sigma*q*ddelta,
    dh=E*(alpha-sigma*B)*dp-B*ds+h_mu*dmu
       +[q*(alpha-sigma*B)+h_delta]*ddelta,
    dmu_y=dmu_z, ddelta_y=ddelta_z.

Here h_mu=-2h_F/r and h_delta=E*h_E. In z variables the principal matrix A_z
is block diagonal: zero chi and mass blocks, the lapse block 1/sigma, and

    A_ps = [[-(2b-sigma*c0)/A_t, -c0/(E*A_t)],
            [E+sigma*E*(2b-sigma*c0)/A_t, sigma*c0/A_t]],

where b=r^2*B+sigma*c0, c0=r^2*c, A_t=-r^2*alpha are the prior density
coefficients. In particular no mass or lapse spatial derivative enters this
physical scalar principal block. Direct symbolic calculation proves

    A_y*T=T*A_z, det(T)=-E*alpha.

Let T_s be the two-by-two dp,ds to dw,dh block of T. Then

    H_ps=T_s^T*diag(P*Q,1)*T_s,
    det(H_ps)=E^2*alpha^2*P*Q,
    H_z=diag(1,H_ps,1,1), H_y=T^(-T)*H_z*T^(-1).

H_z*A_z and H_y*A_y are symmetric, and H_y is positive if E>0,
alpha!=0 and P*Q>0. The tested time-oriented branch further uses alpha>0,
P>0,Q>0. This is an exact ordinary PRINCIPAL symmetrizer, including the metric
variables, not just a sampled scalar norm. It remains meaningful at a regular
horizon when these coefficients and their inverses stay bounded.

Uniform energy estimates also need bounds on coefficients, their derivatives,
the inverse transformation, lower-order terms and boundary/source operators.
The arbitrary positive unit weights for chi,mu,delta specify a mathematical
norm, not new physical constants or a positive gravitational Hamiltonian.
No full nonlinear initial-boundary-value theorem or higher-curvature principal
symbol is claimed here.

## 3. Exact constraint propagation supplies the consistency argument

The current-coordinate differential of G0 is

    dG0=kappa*r^2*V_chi*dchi+kappa*r^2*P*(p+F*s)*dw
        +beta*dh-D0*dmu-sigma*C0*ddelta,
    beta=kappa*r^2*p.

Using C0=kappa*r^2*p*f and p_R=(q_R-q*delta_R)/E, every term in the
unreduced constraint time derivative cancels:

    J_t = (C0)_R-kappa*r^2*V_chi*q
          -kappa*r^2*P*(p+F*s)*q_R
          -beta*(f_R+2f/r-E*V_chi)
          +D0*C0+sigma*C0*(delta_R-D0)/sigma = 0.

The reduction changes this to

    J_t=rho_J*J, rho_J=beta*f_mu.

Thus J=0 initial data remain constrained in the smooth continuum system without
a plateau assumption. More generally, at fixed R,

    J(t,R)=J(0,R)*exp(integral_0^t rho_J(a,R) da),
    ||J(t)||_infinity <= ||J(0)||_infinity
                       *exp(integral_0^t ||rho_J(a)||_infinity da).

This is conditional on a smooth solution and bounded coefficients; rho_J need
not be negative. It is not automatic damping. For additive numerical sources,
the exact extra term is

    (D_R+D0)S_mu-beta*S_h-kappa*r^2*P*(p+F*s)*S_w
      -kappa*r^2*V_chi*S_chi+sigma*C0*S_delta.

That is precisely the previously derived source-completion expression.
Its finite-grid cancellation does not cancel background drift, time-dependent
linearization terms or SBP product-rule defects. Those remain measurable.
The initial discrete w-D_R chi defect is also retained and recorded.

## 4. Coupled boundary data require the lapse perturbation

For an ordinary perturbation e, write dq as the full local Legendre variation.
The fixed-metric scalar variations appropriate to the p,s principal block are

    dq_g=dq-q*e_delta, dw_g=e_w-sigma*q*e_delta,
    df_g=B*dq_g+c*dw_g, z_ac=sqrt(P*Q).

An incoming condition df_g +/- z_ac*dq_g=0 is equivalently

    e_w-k*dq+(k-sigma)*q*e_delta=0,
    k=-(B +/- z_ac)/c.

The flux form need not divide by c; the slope form here is used only on the
exterior test domain with nonzero c. The term involving e_delta is required
by the full physical-variable transformation. The runner saves both this
coupled boundary error and the earlier legacy e_w-k*dq error; changing the
condition is not reported as passing the old first-u boundary test.

The numerical penalty is assembled in coordinate q/lapse sources. The existing
interior q-source projection preserves their endpoint values and supplies a
constraint-compatible mass source with S_mu at the outer endpoint zero.
Only THEN is it transformed to h:

    S_h=alpha*S_q+h_mu*S_mu+h_delta*S_delta, S_w=S_chi=0.

Consequently the induced mass source cannot silently change the specified
q penalty. Holding endpoint S_h instead would not have this property. The
completed source still lacks a full nonpositive-work theorem; all-row source
compatibility is a different assertion from energy dissipation.

## 5. Actual coupled correction experiment

The new evolution is e_t=D F_reduced[y_bar] e-residual[y_bar]+S_num for
e=(e_chi,e_w,e_h,e_mu,e_delta). Both mass and lapse corrections are evolved,
not prescribed. The potential, mass response and lapse response are present
in the linearized RHS. In particular the current equation includes BOTH

    -f_mu*delta J-(delta f_mu)*J_bar.

The second term is not discarded merely because the reference is approximate.
The stable residual provider transforms the prior exact-jet parent defects;
an independent evaluation of y_bar_t-F_reduced[y_bar] agrees. Defects are of
order 1e-9 to 2e-8 in these normalized fixtures, not zero. Background mass
constraints reach roughly 5e-11. This is not the manufactured forcing used
in the preceding scalar method test.

The same degree-64 continuum initial-data lift is used for canonical and
nonlinear fixtures, with epsilon=.1, sigma=.05, R in [4,8], T=.3 and outputs
at .1,.3. Its current momentum component is transformed at t=0. The lift is
an existing approximate constraint construction, not a new exact-data claim.

The spatial current uses r^-2*D_R(r^2*delta f), retaining the spherical weight.
Background coefficients use six-point time interpolation and independent
holdouts. RK4 has CFL=.15 with a 5% speed buffer and finest-grid time halving.
All boundary points remain included. Every output saves the RHS, numerical
sources, background residual, full mass constraint and both boundary errors.

The first launch exposed a batched-array shape error before evolution. It is
preserved as failed. A broadcast-safe zero fixes the array shape; the previous
module snapshot is preserved and scalar/batched identities were rerun.

## 6. Numerical outcome

The unfiltered N64/128/256 experiment is FAILED 124/127, with three spatial
refinement failures. The unfiltered N128/256/512 experiment is FAILED 126/127:
only canonical T=.1 q refinement remains failed. Its coarse and fine mesh
differences are 1.4850e-12 and 1.9121e-12, while time halving changes q by
9.87e-18. This is not explained by the time step. Boundary, lapse, mass and
source-compatibility gates pass in both models on the finest grids.

The comparison uses the previously declared third-difference Gram filter,
strength 1/64, rather than fitting a new physical coefficient. Before source
completion its q/lapse source is -d*(Delta3^T Delta3)u/W_u, with
W_q=SBP_weight*r^2*alpha and W_delta=SBP_weight. Hence its declared weighted
source work is -d*||Delta3 u||^2. For smooth fields this vanishes under mesh
refinement (including the boundary rows); the projected/full coupled work
need not have that sign. Filtered and unfiltered owners stay distinct and
all acceptance thresholds are unchanged.

The filter does NOT repair the remaining gate: its owner is also FAILED
126/127, completed 06:10:58 UTC. Canonical T=.1 q mesh differences become
1.3339e-12 and 1.8770e-12, so they still do not show the required reduction.
No further filter-strength tuning is selected. Both models' finest boundary,
lapse, mass and temporal checks pass; the nonlinear case passes all four
spatial/temporal output comparisons. This does not certify an MTS solution or
establish a physical preference over GR.

Unfiltered N512, half time step, all-row residual and boundary results:

| Case | T | Full mass constraint | Coupled scalar boundary error | Outer lapse error |
| --- | ---: | ---: | ---: | ---: |
| Canonical | .1 | 3.04e-15 | 3.97e-12 | 4.18e-19 |
| Canonical | .3 | 2.55e-14 | 3.05e-12 | 1.17e-17 |
| Nonlinear | .1 | 9.40e-15 | 1.63e-11 | 2.63e-18 |
| Nonlinear | .3 | 1.64e-13 | 1.63e-11 | 6.61e-17 |

These are normalized fixture values, not physical bounds. The mass residuals
are approximately 9.1e-5,1.25e-3,3.02e-4,3.36e-3 of their respective background
mass residual scales, below the declared 5% gate. The scalar boundary gate is
1% of the saved incoming-data scale. A small residual does not replace the
remaining refinement or continuum-error requirement.

The stubborn q difference peaks at R=4.015625, just inside the inner boundary,
with alternating neighboring signs. It is 1.9121e-12 without the filter and
1.8770e-12 with it, about 0.0535% and 0.0526% of the corresponding finest q
correction norm. In the unfiltered run the q source at this interior point
is ENTIRELY the Noether compatibility projection: 8.46e-12 at N256 versus
-9.21e-12 at the common N512 point. The raw penalty acts only at endpoints.
That makes the boundary/source discretization the next concrete target;
these saved-time samples do not yet prove it is the sole accumulated cause.

Derivation owners: broadcast-safe reduction 26/26 at 05:55:44 UTC; exact full
principal/boundary identities 6/6 at 05:57:50 UTC. Independent validation is
121/121 at 06:11:20 UTC, including the nonlinear zero-order AND gradient
linearization against an independent complex-step continuum RHS, exact
constraint propagation, saved-output metrics and source hashes. The validator
explicitly records all three failed evolution states; its own success does
not promote them. Executed runner snapshots preserve the pre-filter versions.

### Next derivation, not more blind refinement

The full nodal source derivative equations together with an exact outer mass
source impose an extra discrete compatibility condition. The current repair
adjusts interior q through an adjoint projection; its oscillatory interior
source must now be addressed explicitly. Derive and compare a boundary-compatible
mass-source integration/operator that either satisfies the same condition or
retains a rigorously bounded all-row residual in the constraint error budget.
Do not delete the outer row, set that residual to zero, or call an unbounded
source change physical. Use the canonical T=.1 case as the first diagnostic
and keep the nonlinear control matched. After that, transfer the corrected
derivative jets back to the actual-curvature and first-u calculations.

## 7. Source map and scope boundary

Paths below are relative to this post-checkpoint-work directory.

- `scripts/annular_coupled_current_operator_20260909.py`
- `scripts/derive_annular_coupled_current_reduction_20260909.py`
- `scripts/derive_annular_full_principal_identity_20260909.py`
- `scripts/run_annular_coupled_current_correction_20260909.py`
- `scripts/validate_annular_coupled_current_20260909.py`
- `scripts/annular_evolution_operator_20260909.py`
- `scripts/annular_coordinate_evolution_operator_20260909.py`
- `scripts/annular_continuum_initial_data_20260909.py`
- `scripts/annular_boundary_preserving_completion_20260909.py`
- `source-intake/navier-stokes/20260909/annular-constraint-correction-initial/canonical.json`
- `source-intake/navier-stokes/20260909/annular-constraint-correction-initial/nonlinear_modulated.json`
- `source-intake/navier-stokes/20260909/annular-coupled-current-reduction-derived/status.json`
- `source-intake/navier-stokes/20260909/annular-coupled-current-reduction-derived/current-operator-snapshot.py`
- `source-intake/navier-stokes/20260909/annular-coupled-current-reduction-broadcast/status.json`
- `source-intake/navier-stokes/20260909/annular-full-principal-identity-derived/status.json`
- `source-intake/navier-stokes/20260909/annular-coupled-current-correction-initial/status.json`
- `source-intake/navier-stokes/20260909/annular-coupled-current-correction-broadcast/status.json`
- `source-intake/navier-stokes/20260909/annular-coupled-current-correction-refined/status.json`
- `source-intake/navier-stokes/20260909/annular-coupled-current-correction-gram-filter/status.json`
- `source-intake/navier-stokes/20260909/annular-coupled-current-independent-validation/status.json`
- `DERIVATION-20260909-conservative-evolution-and-momentum-mass-completion.md`

No preceding first-u or actual-curvature failure is promoted by these new
ordinary experiments. No physical kappa/u calibration, Maxwell/source match,
full MTS-to-GR limit, central-singularity cure, or empirical preference follows
from these numerical checks. The full goal remains active. Work is private;
no GitHub action, frozen workbench or galaxy edits, subagents or stopped shared
processes. Jobs are single-core BelowNormal and at most two run concurrently.
