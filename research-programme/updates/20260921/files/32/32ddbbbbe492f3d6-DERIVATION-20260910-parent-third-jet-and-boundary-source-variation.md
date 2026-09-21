# Parent third time jet and exact boundary-source variation law

Private continuation, 2026-09-10 (Europe/London). No GitHub action.

## 1. Result and limits

The required third time jet is now sourced by differentiating the ORIGINAL
canonical parent constraints, including the actual metric-link shift current.
Both the old boundary-source trace and its time derivative are reconstructed.
An equivalent source decomposition removes the second-spatial-derivative trace
from the new endpoint coefficient WITHOUT dropping its weak compatibility
defect: that defect is retained in a remainder with a derived energy bound.

This gives an explicit conditional pointwise rate bound and hence a conditional
total-variation inequality for the REPACKED endpoint source. It does not yet
certify total variation on the actual time interval. The new third-jet solve is
finite-dimensional; no mesh-uniform parent inverse or time-persistence theorem
has been proved. The original trace's mesh-uniform BV bound remains open.

Validation: 633/633 checks on the SAME 18 saved states, at three times on
N=16,32,64 in both GR and metric-Gram branches. No new trajectory or physical
fit. These are algebraic/numerical checks, not 633 independent physics tests,
an interval-arithmetic certificate, a continuum existence proof, or local-GR /
black-hole closure. The largest checked third free-constraint residual is
1.029e-13 in the inherited dimensionless coordinates.

## 2. Hypotheses and source ownership

Keep the canonical Lambda=m_chi=b2=b3=0 annulus, positive lapse N and
F=1-2mu/R, the actual Gauss4 quadrature, C1 cubic Hermite scalar reconstruction,
and metric-Gram action when enabled. Endpoint scalar VALUES are prescribed;
all scalar slopes remain free. Use the original quadratic endpoint histories
and affine outer-clock history. This note does not cover arbitrary boundary
histories without adding their higher derivatives.

Let y denote the packed parent unknowns (mass, lapse, nodal scalar velocity,
slope velocity), x the scalar configuration, pi its canonical momenta, and
F_parent(y,x,pi,clock)=0 the free parent constraints. Subscript I denotes free
scalar tests; subscript f below denotes free PARENT unknowns, a different set.

    c=N sqrt(F), m=R^2/c, p=R^2 c, theta=c_t/c,
    M=(.,.)_(Qm), K=a_bulk+a_Gram, L=M^-1 K, U=L^-1.

M and K without a full subscript are restricted to free scalar variables.
Pi is the actual weighted quadrature projection and B=Pi ell_map the inherited
two-endpoint affine lift. All norms and numbers retain the saved dimensionless
conventions, not inferred SI units.

Implementation and immediate mathematical dependencies:

- `scripts/annular_boundary_source_variation_20260910.py`
- `scripts/derive_annular_boundary_source_variation_20260910.py`
- `scripts/annular_metric_flux_jets_20260909.py`
- `scripts/annular_released_hermite_action_20260909.py`
- `scripts/annular_H1_clock_energy_20260909.py`
- `scripts/annular_uniform_energy_bounds_20260909.py`
- `DERIVATION-20260910-mesh-independent-regular-transport-with-clock-jumps.md`
- `DERIVATION-20260910-released-slope-feedback-and-boundary-normal-form.md`
- `DERIVATION-20260910-paired-variational-work-and-graph-energy-correction.md`

The hash ledger includes the original state, first/second jets, parent action,
source reconstruction, and inherited theorem files. No parent coefficient or
source history is fitted or replaced here.

## 3. Third differentiated parent equation

From the saved y,y1,y2, the configuration jets are

    x1=velocity(y), x2=velocity(y1), x3=velocity(y2).

Differentiating the canonical momentum law gives

    pi1=-K_full x,
    pi2=-K_full,t x-K_full x1,
    pi3=-K_full,tt x-2K_full,t x1-K_full x2.

As in the original parent, the two prescribed nodal endpoint momentum rates
are held zero; every slope momentum equation is retained. M_full, K_full and
their first and second rates are evaluated with the existing SecondJet
algebra, including the sampled Gram coefficient and its time rates.

Let J be the actual packed Hessian/Jacobian returned by the parent evaluator.
At any saved state the differentiated third constraint is

    F_parent^(3)=J y3+k3.

k3 is evaluated with y3=0 and the above x/pi jets. It is not an extra closure.
Computationally, differentiate the existing second-jet expression by complex
step: replace each zeroth/first/second input jet by itself plus i epsilon times
its next jet. This calculates the third chain rule of the original expression;
it does not differentiate rounded saved time differences.

The fixed third jet is determined as in the original first/second jet route:
inner mass third rate is the second derivative of the actual shift-projected
mass velocity; fixed endpoint scalar-velocity third rates are zero for these
quadratic histories. Consequently

    y3_fixed=(v_shift,tt(inner),0,0),
    y3_f=-J_ff^-1 (k3+J y3_fixed)_f.

Here y3_fixed in the second line is embedded as zero on free entries. This
requires nonsingular J_ff at the state being evaluated. It does not establish
nonsingularity in a neighborhood or over the evolution interval.

The original shift projection is differentiated explicitly. Write

    P v_shift = G_link - matter = r_shift.

Then

    v_shift,t=P^-1(r_shift,t-P_t v_shift),
    v_shift,tt=P^-1(r_shift,tt-P_tt v_shift-2P_t v_shift,t).

P is the original face mass pairing with weight 1/(kappa N F^(3/2)). The
matter term, nonlocal metric-link matrix and Gram link current are all
differentiated. The LOCAL canonical Gram coefficient derivative with respect
to shift is exactly zero in this branch, checked against the original
coefficient evaluator; this does NOT make the nonlocal Gram link current zero.

Only the prescribed INNER mass row uses that fixed shift rate. We do not
replace all interior mass jets by shift jets. The complete interior difference
y3_mass-v_shift,tt is saved as physical_shift_second_mismatch, not asserted
zero or hidden by the new constraint solve.

For each saved state the finite-coordinate estimate is

    ||y3||inf <= max(||y3_fixed||inf,
                    ||J_ff^-1||inf ||(k3+J y3_fixed)_f||inf).

The inequality is algebraic; its displayed numerical value uses ordinary
floating-point solves, not outward-rounded certification. This mixed vector
includes high scalar-velocity derivatives. Its norm is not a metric-only
bound or a coordinate-independent physical instability diagnostic.

Independent controls preserve the old first/second jets, check matrix second
rates and shift rates by a separate complex-step calculation, and evaluate
the second constraint rate along consistent cubic paths at +/-2e-5 and +/-1e-5.
The latter third-derivative errors decrease by approximately four on halving
the displacement, as expected for a centered second-order check.

## 4. Original complete source and elliptic identity

Let ell be the ORIGINAL spatially affine lift of the quadratic endpoint
history. In particular ell_RR=ell_tRR=0 and ell_ttt=0. Define

    F_b=-(M_full ell_tt+M_full,t ell_t+K_full ell)_I,
    F_b,t=-(2M_full,t ell_tt+M_full,tt ell_t
                         +K_full,t ell+K_full ell_t)_I,
    psi=K^-1 F_b, with zero endpoint values,
    b=M^-1(K_t psi-F_b,t).

Differentiating K psi=F_b proves the useful exact identity

    psi_t=-U b.

Let w_potential=psi+ell. This is NOT the velocity normal-form variable from
the previous note. Its weak equation, on every free test, is

    (K_full w_potential)_I=Q[m xi (test)],
    xi=-ell_tt+theta ell_t.

xi need not lie in the finite-element space. No strong pointwise equation is
being imposed at either boundary.

Put

    a=p_R/m=2c^2/R+c c_R, d=c^2 theta_R, D=a theta+d.

The earlier trace is retained as beta_old:

    beta_old=-D w_potential,R-c^2 theta psi_RR-a ell_tR
                         -2theta ell_tt+(theta^2-theta_t)ell_t.

Define a different, simpler endpoint coefficient by the bulk formula

    beta_red=-d w_potential,R-a ell_tR-3theta ell_tt
                                      +(2theta^2-theta_t)ell_t.

These two traces are not identical. With
r_w=-a w_potential,R-c^2 w_potential,RR their difference is

    beta_old-beta_red=theta(r_w-xi).

The weak compatibility defect r_w-xi is NOT set to zero. Instead it is included
in the exact repacking below, which is why this operation is legitimate.

## 5. Exact repacking and retained energy remainder

Define

    E_w=M^-1(K_full,t w_potential)_I
                       -Pi(theta xi-d w_potential,R),
    Q_ell_t=M^-1(K_full ell_t)_I+Pi(a ell_tR).

Using M_t=-Pi(theta .) in bilinear form and
M_full,tt=Q[m(theta^2-theta_t) (trial)(test)] gives EXACTLY

    b=Pi beta_red+E_w+Q_ell_t
     =B beta_red,end+b_red,reg,
    b_red,reg=Pi(beta_red-ell_map beta_red,end)+E_w+Q_ell_t.

The full vector b and its signed source-energy work are unchanged. Old traces,
old derivatives and the new vectors are saved separately. Q_ell_t, including
the actual affine quadrature remainder, is retained; it is not declared zero.

The earlier weak-commutator proof extends to E_w without imposing homogeneous
endpoint values on w_potential. For a free test v set
e_v=theta v-W_theta v, with the same nodal-value/physical-slope multiplier
W_theta as before. The test still has zero endpoint values. Its weak equation
gives

    (v,E_w)_M=Q[p w_potential,R e_v,R]-Q[m xi e_v]
               +a_Gram,t(w_potential,v)-a_Gram(w_potential,W_theta v).

The runner reconstructs E_w independently from this identity. The proof from
the previous note uses continuity of p w_potential,R and cell-endpoint zeros
of e_v, not zeros of w_potential. The Gram factor annihilates affine nodal
data, so its H2 estimate also applies to w_potential. Thus, writing

    W1=||w_potential,R||L2 upper bound,
    W2=||w_potential,RR||L2 upper bound,
    Winf=||w_potential,R||inf upper bound,
    Xi=||xi||Q upper bound,
    Ltheta=||theta_R||inf, Qtheta=||theta_RR||broken,
    Cw=30Ltheta(Lp W1+pmax W2)+104pmax Winf Qtheta
                              +3mmax Ltheta Xi
                              +I_Gram 128pmax Ltheta W2,

the exact same multiplication/quadrature/Gram estimates give

    ||E_w||M <=h Cw/sqrt(mmin),
    ||E_w||K <=16sqrt((pmax+G0)/mmin) Cw/sqrt(mmin),
    G0=2pmax in Gram, zero in GR.

This is a mesh-independent conditional energy bound, not a deletion of a
troublesome endpoint curvature term. For xi the proof uses its quadrature
norm; the implementation safely bounds it by sqrt(length) times its analytic
supremum. The remaining zero-endpoint volume projection still has internal
VALUE jumps. Complete regular-source and affine-quadrature energy control
must retain these; this note does not prove that entire bound merely from
the small measured norm of b_red,reg.

## 6. Exact source time derivatives

For the quadratic histories,

    a_t=2theta a+d,
    d_t=c^2(2theta theta_R+theta_tR),
    D_t=a(2theta^2+theta_t)+3c^2 theta theta_R+c^2 theta_tR.

Differentiate the original trace without removing its curvature terms:

    beta_old,t=-D_t w_potential,R-D w_potential,tR
               -c^2(2theta^2+theta_t)psi_RR-c^2 theta psi_tRR
               -a_t ell_tR-a ell_ttR
               +(theta^2-3theta_t)ell_tt
               +(2theta theta_t-theta_tt)ell_t.

The equivalent repacked source has the simpler law

    beta_red,t=-d_t w_potential,R-d w_potential,tR
               -a_t ell_tR-a ell_ttR
               +(2theta^2-4theta_t)ell_tt
               +(4theta theta_t-theta_tt)ell_t.

There is no second-spatial-derivative trace in this last expression. For
nonquadratic endpoint histories it additionally contains -3theta ell_ttt;
the force derivative in section 4 must then also include M_full ell_ttt.

The necessary theta_tt is now obtained from the third parent jet. With
Dden=R-2mu,

    theta_tt=N3/N-3N1 N2/N^2+2(N1/N)^3
             -mu3/Dden-6mu1 mu2/Dden^2-8(mu1/Dden)^3.

theta_tR uses the first spatial derivatives of the original piecewise-linear
mass/lapse and their first/second time jets. Only one-sided endpoint traces
are used; no unsupported global smoothness across knots is assumed.

Both beta derivatives and theta_tt are checked against a separate complex-step
reconstruction of the full matrices, loads, elliptic solve and source traces.
This checks derivatives of the old as well as the new source, not just the
rearranged expression against itself.

## 7. Conditional pointwise bound and BV implication

Let Fstar bound ||F_b||M-dual, Ftstar bound ||F_b,t||M-dual, and Cstar bound
||M^-1 K_t U||M-to-M, all from the existing analytic coefficient envelopes.
Let Dinf be the inherited elliptic derivative-supremum constant. Then

    bMstar=Cstar Fstar+Ftstar,
    Winf=Dinf Fstar+|ell_R|,
    Wtinf=Dinf bMstar+|ell_tR|.

The second line follows from psi_t=-U b, not an endpoint inverse inequality.
For the remainder estimate one may take

    W1=D1 Fstar+sqrt(length)|ell_R|, W2=D2 Fstar,
    Xi=sqrt(length)(sup|ell_tt|+sup|theta| sup|ell_t|).

At each endpoint e a sourced triangle bound is

    Value_e=|d|Winf+|a||ell_tR|+3|theta||ell_tt|
                                   +(2theta^2+|theta_t|)|ell_t|,
    Rate_e=|d_t|Winf+|d|Wtinf+|a_t||ell_tR|+|a||ell_ttR|
                 +(2theta^2+4|theta_t|)|ell_tt|
                 +(4|theta theta_t|+|theta_tt|)|ell_t|.

Consequently, PROVIDED these sourced functions are integrably bounded along
the actual solution and the stated differentiability/positivity persists,

    TV(beta_red,end;[0,T]) <= integral_0^T ||Rate(s)||R2 ds.

This is the conditional estimate needed by the inherited boundary-memory
formula, with beta_red replacing beta_old and with b_red,reg retained. We
have NOT bounded the right side over the actual time interval. Three saved
times per trajectory do not certify the supremum or the integral; no sampled
trapezoidal sum is relabeled an upper bound. The previous normal-form source
bridge and F_B remain unchanged because B is unchanged.

For a completely parent-solve-based pointwise estimate, substitute the section
3 finite-coordinate upper bound for N3 and mu3 in section 6, using the owned
positive Nmin and Dden_min. This is implemented as a second, much more
conservative upper. No cancellation or unsupported smaller measured value is
substituted into that full-parent upper.

## 8. Numerical results and what they do not show

Final saved time t=.01; rate bounds are dimensionless R2 norms. The first
bound uses the sourced endpoint theta_tt, the second bounds it through the
whole packed inverse estimate. Neither is an actual interval-TV certificate.

| Cells | Branch | Endpoint-based rate upper | Whole-parent rate upper | ||J_ff^-1||inf |
| --- | --- | ---: | ---: | ---: |
| 16 | GR | .295719 | 355.035 | 403.588 |
| 16 | metric-Gram | .389234 | 514.779 | 403.587 |
| 32 | GR | .264446 | 1277.132 | 808.106 |
| 32 | metric-Gram | .354739 | 1961.535 | 808.106 |
| 64 | GR | .221951 | 2272.027 | 1617.142 |
| 64 | metric-Gram | .362525 | 2509.240 | 1617.142 |

At N64 the repacked endpoints and their derivatives are

    GR beta_red=(-.02031333595,-.01985293453),
       beta_red,t=(-.14709848968,-.14264126128);
    Gram beta_red=(-.02031200922,-.01985467272),
         beta_red,t=(-.14680788599,-.14186042532).

The measured E_w energy norms are 2.72e-10 GR and 8.34e-8 Gram, while the
analytic upper bounds are approximately 91.65 and 1030. The complete repacked
regular-source norms are .0044331 and .0044424. These are deliberately reported
alongside the loose bounds, not used to replace them. The original complete
source remains unchanged, including its large endpoint-projection contribution.

The increasing raw inverse infinity norm does not prove failure: it depends
on the mixed-coordinate norm, includes scalar velocity/slope blocks, and is
not the particular endpoint metric response needed by theta_tt. It does show
that this whole-system estimate has not delivered a useful uniform bound.
Conversely, the moderate endpoint-based rates at three meshes do not prove
uniform boundedness or persistence.

## 9. Best next derivation

Target the PARTICULAR metric response in theta_tt rather than repeatedly
bounding every component of y3 by one maximum. Write its linear third-jet part
as endpoint functionals of y3: N3/N-mu3/(R-2mu), plus known lower-jet terms.
Construct the actual free-parent adjoint/Schur-complement representation of
those functionals, retaining fixed-row forcing and Gram current. Then try to
bound that response with the parent constraint structure and appropriate
weighted norms, before paying for another higher global derivative norm.

The outstanding steps remain substantive: make that estimate uniform and
propagate it in time; control the repacked regular source including jumps and
affine quadrature; and close the positive-annulus/parent persistence argument.
The work here supplies the missing derivative equation and a tractable source
law, not a claim that those steps are already complete.

## 10. Reproducibility and integrity

The derive runner is additive and refuses to overwrite its output directory.
The successful run stores old/new traces, both derivatives, third parent jets,
all third residuals, interior shift mismatch, complete b and its retained
regular/remainder vectors. It used one single-core BelowNormal Python worker
and launches no evolution or other agent.

- `source-intake/navier-stokes/20260910/annular-boundary-source-variation-derived/status.json`
- `source-intake/navier-stokes/20260910/annular-regular-transport-bound-final-integrity.json`
- `source-intake/navier-stokes/20260910/annular-boundary-source-variation-final-integrity.json`

The final seal rechecks inherited and new SHA256 evidence and cited local
paths, records a resume snapshot, and requires no scripts bytecode cache.
The protected formalization-workbench check is a modification-time scan since
2026-09-10T02:07:00Z, not a full pre-turn content-hash baseline. No frozen
workbench, galaxy project, public repository or prior completed artifact was
intentionally edited. Final seal status, rather than this prose, records the
outcome of the post-write verification.
