# Moving P2 current and short live evolution

Private local checkpoint, 2026-09-18. This follows `DERIVATION-20260918-coupled-live-P2-canonical-inverse.md` and retains the complete source-fitted P2 action, every Gram factor, the live radial solve and the actual finite canonical inverse. Normalized test parameters are not observational fits or parent-derived physical constants.

## 1. What must be derived, not transplanted

The older current in `DERIVATION-20260915-moving-curved-cut-action-and-canonical-current.md` used fixed field nodes. The present physical nodes and element edges move:

    R(r,z,t) = r + k(r)[b(z,t)-b_star] + [1-k(r)] epsilon z,
    J = partial_r R,      v(r,z,t) = k(r) V(z,t),
    partial_z R = [1-k(r)] epsilon + k(r) b_z.

Ignoring the last two facts loses transport of both piecewise P2 energy and Gram atoms. Source ordering and J>0, U>0, N>0 and timelike source speed are assumed throughout. The inherited Einstein/polar geometry is being coupled consistently to this specified matter action; the entire Einstein action is not being derived from the MTS corpus here.

## 2. Explicit horizontal extension and its scope

Keep the preceding source-anchored horizontal connection prescription:

    beta = kappa N U^3 P,
    c = beta / (N^2 U^2-beta^2),
    C = R^2 (N^2 U^2-beta^2)/(N U),
    T_R = c(T,R),     T(s,b(s)) = s.

Write J_T=partial_s T at FIXED physical R. The moving source anchor gives

    J_T(s,R) = [1-c_b V] exp(integral_b^R c_t(T,rho) d rho).

An off-diagonal extension is needed to talk about a shift variation at all. We specify it explicitly rather than assert that the diagonal P=0 action uniquely determines it: construct the source-fitted mesh on the horizontal leaf, retaining its positions R_i(s); transport the nodal histories by a_i^sharp(s)=a_i(T(s,R_i(s))) and the Eulerian coefficient density by Cbar(s,R)=J_T C(T,R). Evaluate the same finite P2 kinetic, gradient and full Gram terms on this leaf, with the proper-time source term using V+beta_b.

Crucially,

    d_s a_i^sharp = a_i,t(T_i) [J_T(s,R_i) + c(T_i,R_i) v_i].

The extra c v_i is absent for a fixed grid. The spatial map Jacobian J and leaf-time Jacobian J_T are different quantities. We do not replace one with the other.

This is an explicit extension of the inherited clock rule to this moving-mesh representation. It reduces EXACTLY to the retained action at P=0, and its finite nonzero-shift variation is tested below. Neither uniqueness from the parent nor arbitrary spatial/time-coordinate covariance of this finite representation is proved by that test. Other off-diagonal extensions are not excluded merely by agreement at P=0.

The nonuniqueness is elementary: a putative added term integral P F ds dR vanishes at P=0 but changes the P derivative there. Additional symmetry/parent requirements would have to exclude such terms. Thus the present result constructs and checks the declared horizontal extension; it does not infer a unique off-diagonal action from diagonal data alone.

## 3. First variation before invoking gravity

At P=0 define I(s,R)=integral_b^R delta c(s,rho) d rho. Then

    delta Cbar = C_t I + C I_t,
    I_t|_R = integral_b^R delta c_t d rho - V delta c_b,
    delta a_i = u_i I_i,
    delta u_i = a_i,tt I_i + u_i [I_t|_(R_i) + v_i delta c_i].

The source-coordinate history is held fixed in this variation; I_b=0. This is not a variation in which all mesh nodes are artificially frozen in the subsequent time integration by parts.

Let pi_i=L_(u_i), E_i=dot(pi_i)-L_(a_i), zeta=L_wave,V and E_b^wave=dot(zeta)-L_wave,b. Define the distributional coefficient covector at fixed physical radius:

    Z(R) = Z_reg(R) + sum_i z_atom,i delta(R-R_i),
    Z_reg = -1/2 [R^4 W^2/C^2 + H^2],
    z_atom,i = -gamma_i/J_i,
    gamma_i = sum_f S_(fi) (L a)_f^2/(2 h_G).

All field/source coordinate covectors hold the Eulerian metric fixed, but retain its spatial gradients. For temporally compact variations, integrating the raw action variation by parts gives

    delta I_wave = - integral ds [sum_i E_i u_i I_i
                                  + integral C partial_t Z I dR].

The corresponding endpoint work for noncompact variations is

    [sum_i pi_i u_i I_i + integral C Z I dR]_(s0)^(s1).

The coefficient distribution must be differentiated at fixed PHYSICAL radius. This is why the expression still includes the motion of edges and atoms although the displayed current resembles the fixed-node expression.

## 4. Moving edges and moving atoms

Every P2 element boundary can have unequal one-sided derivatives. With edge speed v_e and jump [Z]_e=Z_left-Z_right,

    partial_t Z = (partial_t Z_reg)_regular
                  + sum_edges v_e [Z]_e delta_(R_e)
                  + sum_i [dot(z_atom,i) delta_(R_i) - z_atom,i v_i delta'_(R_i)].

Use one-sided spatial Jacobians at the source when evaluating these jumps. The source edge alone is not sufficient; all P2 edges contribute. The exterior regular density is zero. The physical end boundaries have k=0, hence zero speed in these tests.

In particular,

    integral C partial_t Z I dR
      = integral C (partial_t Z_reg)_regular I dR
        + sum_edges C_e v_e [Z]_e I_e
        + sum_i [(C_i dot(z_atom,i) + C'_i z_atom,i v_i) I_i
                 + C_i z_atom,i v_i delta c_i].

The C'_i term and the final local atom term come from delta-prime transport. They are not optional corrections fitted to a computed mass rate.

The whole-layer off-shell Noether identity provides an independent sign/accounting check:

    sum_i E_i u_i + V E_b^wave + integral C partial_t Z dR = 0.

To derive it, note that the full wave field/source Legendre energy obeys E_wave=-integral C Z dR, including the Gram energy and source field momentum. Differentiate this identity and the ordinary Legendre energy identity; cancel the explicit coefficient work integral Z C_t. No gravitational mass equation is used in this argument.

## 5. Connection current and finite-width pushforward

Let I_(a,b)(r)=sign(b-a) 1_(min(a,b)<r<max(a,b)). The shift covector is

    K(r) = -sum_i E_i u_i I_(b,R_i)(r)
           -integral C(R) partial_t Z(R) I_(b,R)(r) dR.

The regular terms can be evaluated as a left primitive below the source or minus a right tail above it. In addition there is the LOCAL moving-atom term

    K_local(r) = -sum_i C_i z_atom,i v_i delta(r-R_i).

It is easy to miss this term by integrating only selected atoms in the left/right tails. Its continuous label average uses the ACTUAL inverse-map Jacobian:

    <K_local>(r) = -sum_i [w C_i z_atom,i v_i / partial_z R_i]_(z=xi_i),
    R_i(xi_i)=r,     -1/2 < xi_i < 1/2.

Here xi_i is the inverse material label, not the atom coefficient z_atom,i.

The inherited polar canonical relation, whose gravity-only contribution vanishes on P=0, is

    m_t^current(r) = -kappa U/N <K>(r)
                    -kappa N U^3 p_material(z_b) w(z_b)/b_z(z_b),
    p_material = S0 V/(U^2 ell),   ell^2=N^2-V^2/U^2,
    b(z_b)=r.

It contains the MATERIAL momentum here, not the full canonical source momentum. The latter includes field inertia and was retained in the coupled inversion and evolution. Both roles must be kept distinct.

## 6. What the numerical comparison does and does not establish

`scripts/annular_live_P2_current_20260918.py` implements the moving distributions above. It takes the actual canonical force direction, re-solves neighboring canonical/radial states and obtains a centered fourth-order tangent of the metric and velocities. Regular covector rates and the finite momenta are differentiated at first order by complex differentiation, with explicit interface/atom distributions.

The current is NOT set equal to a finite difference of reconstructed mass. Its formula is derived from the separate action variation and tested by finite nonzero-shift action differences in `scripts/qualify_annular_P2_shift_variation_20260918.py`. Nevertheless, it contains the tangent metric inside partial_t Z. Comparing it with the mass tangent is therefore an IMPLICIT temporal-equation residual test, not a wholly independent spacetime solver or an angular Einstein equation test.

`scripts/qualify_annular_live_P2_current_20260918.py` tests both branches on affine and deformed moving-source states. It records full off-shell current, on-shell current with scalar Euler terms omitted, frozen-mesh negative control, Noether residuals and off-grid radial equations separately. Chebyshev material collocation is not an exact finite-label Galerkin action. A small scalar-work/current residual does not imply that every off-label Euler-vector component is equally small; `scripts/qualify_annular_P2_current_tangent_resolution_20260918.py` checks that distinction explicitly.

The pilot `scripts/run_annular_live_P2_current_evolution_20260918.py` evolves the unprojected canonical equations from the actual retained action, re-solving gravity at every right-hand side. It compares both branches, half time step, increased material resolution and zero-wave controls. Time horizon0.004 is a deliberately short normalized pilot, not a physical time prediction or long-time test. No force, source coordinate, mass, current or energy is projected onto a desired answer.

### Why the current cannot certify the entire Euler vector

Since |I_(b,R_i)(r)|<=1, the difference between the full off-shell and scalar-on-shell current obeys

    |delta m_t(r)| <= kappa |U(r)/N(r)| integral w(z) sum_i |E_i(z) u_i(z)| dz.

This follows directly from the action-derived current, not from a measured mass residual. A small velocity-weighted Euler work can coexist with a larger individual E_i. The label-resolution diagnosis records both quantities and tests the inequality using the same positive integration measure; its numerical check is not a quadrature-certified continuum supremum bound.

The initial degree6-to10 diagnostic missed its predeclared factor-two scalar-residual reduction: the reference ratio was0.5257788755. Its nodal equations, Noether checks and time-difference control passed, but the resolution expectation failed. That executed run is preserved without changing its gate. The separate `scripts/diagnose_annular_P2_current_label_resolution_20260918.py` checks both branches at6,10,18 with unchanged equations; a wider refinement check is explicitly different from passing the original6-to10 test. There is no universal spectral convergence rate claim.

## 7. Results

97 successful implementation checks:12 finite shift/current variations,20 live initial-current checks,21 label-resolution/weighted-current diagnostics,44 short-evolution/control checks. These are implementation checks, not97 independent physical validations. One failed resolution-expectation attempt remains preserved; the accumulated retained failed-attempt count is33. All4 older full-horizon flat-force failures remain unchanged.

| Diagnostic | Observed result |
| --- | --- |
| Finite nonzero-shift action derivative versus raw variation, both branches | error<=3.63e-15 |
| Raw versus integrated-by-parts current variation | error<=1.36e-20 |
| Manufactured whole-layer moving Noether identity | error<=3.91e-18 |
| Omitting moving-node clock from that variation | error2.25e-8 |
| Omitting moving transport from the Noether identity | error up to9.46e-6 |
| Initial affine/deformed current versus re-solved mass tangent | error<=1.48e-11 |
| Frozen-mesh current used on those same states | error up to1.46e-6 |
| Eight trajectories: both branches, principal/half-step/label-refined/zero-wave | all finish t=0.004 |
| Maximum exterior-mass drift across all8 trajectories, no projection | 6.59e-14 |
| Actual interior mass change | about2.33e-5 |
| Principal source displacement, reference / MTS | 0.00011987588534 /0.00011991339361 |
| Evolved independent-current residual, reference / MTS | 1.10e-11 /2.08e-11 |
| Evolved scalar-on-shell current residual, reference / MTS | 1.10e-11 /1.64e-11 |
| Reference half-step whole-state / velocity difference | 2.25e-14 /7.80e-13 |
| MTS half-step whole-state / velocity difference | 9.68e-10 /1.32e-8 |
| Degree6-to8 trajectory label refinement: worst whole-state / velocity difference | 8.87e-10 /1.61e-8 |
| Largest evolved off-grid radial mass / log-lapse equation residual | 1.34e-7 /2.55e-8 |
| Reference versus MTS zero-wave trajectory, velocity and metric arrays | identical |

The exterior-mass precision MUST NOT be advertised as fourteen-digit trajectory, local-equation or continuum accuracy. The velocity refinement controls are of order1e-8 against a2e-8 gate; the evolved radial mass derivative is of order1e-7 against a2e-7 gate. These pass the declared pilot criteria but are not wide safety margins for a longer run. The MTS principal trajectory needed134 right-hand-side evaluations versus62 for reference at the same solver tolerances; this is a computational difference, not by itself a proof of instability or physical significance.

### Retained material-resolution miss

On the deformed source, both branches miss the original degree6-to10 factor-two reduction expectation: reference0.5257788755, MTS0.5402456944. The first executed diagnostic stopped at the reference miss; the follow-up deliberately measured both rather than applying a tougher rule only to MTS.

At degree18 the corresponding ratios to degree6 are0.0761746031 and0.0786812630. The sampled scalar Euler residuals fall from1.39e-6/1.35e-6 to1.058e-7/1.064e-7. These are still nonzero off-label residuals, not an exact finite-label variational solution or a uniform-in-label theorem. Nodal scalar Euler residuals stay below6e-14 and nodal source residuals below1.73e-10. Halving the tangent difference step in the retained reference diagnostic changes the acceleration by2.35e-12, so that particular off-label defect is not removed by shrinking the time difference.

The velocity-weighted Euler-work bound falls from about3.32e-11 to1.11e-12 under degree6-to18 refinement. The corresponding sampled gravitational-current bounds are about3.32e-12 to1.11e-13. This quantifies why the good current result does not erase the separately recorded Euler-vector defect. No equation, Gram factor, force or current acceptance gate was changed for this diagnosis.

All owned numerical workers finished. Final preservation checks are recorded separately in `source-intake/navier-stokes/20260914/annular-live-P2-current-final-integrity.json`; require its state to be complete before treating the note as sealed.

## 8. Remaining scientific step

Before lengthening the run, tighten and separate the radial, material-label and time error budgets at the saved evolved states. The next physics-facing qualification is spatial waveform and source-force accuracy against an independently implemented continuum spherical matter/gravity reference at fixed physical source width, with the same preparation and boundary assumptions. Time conservation alone cannot establish that accuracy: the four preserved older flat full-horizon force failures are not being relabelled as passed. Do not repeat the already-completed current derivation as a new advance.

Keep the chosen horizontal/boundary extension, finite-label approximation, source ordering interval, nonzero width, positive/untrapped metric, inherited Einstein sector and missing unrestricted angular/parent completion explicit. This is not a full MTS-to-GR or observational validation.

## 9. Evidence

- `source-intake/navier-stokes/20260914/annular-P2-moving-shift-variation-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-live-P2-independent-current-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-P2-current-tangent-resolution-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-P2-current-label-diagnosis-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-live-P2-current-evolution-attempt01/status.json`

No GitHub action or subagents. Executed sources/evidence remain immutable, including any failed run. This derivation note becomes immutable after its final integrity seal.
