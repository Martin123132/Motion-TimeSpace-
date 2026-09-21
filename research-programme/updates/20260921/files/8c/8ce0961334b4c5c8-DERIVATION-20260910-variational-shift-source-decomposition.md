# Variational shift source: independent decomposition and a boundary repair test

10 September 2026. Private finite-model derivation. Final attempt01:
**365/365 checks on 18 states**, with matched GR-plus-canonical-scalar and
metric-Gram branches at 16, 32 and 64 radial intervals and saved times
0, 0.005 and 0.01. These are separate initial-root neighborhoods, not a
certificate that all saved states lie on one exact trajectory.

**Result:** the original action and static root data independently predict
the previously certified shift defect. A necessary law for the two scalar
endpoint accelerations is derived and tested, not merely requested.
It cannot close the remaining interior equations in any of the 18 cases
when the other data and reduced rules are held fixed. This is neither a
continuum GR no-go nor a rejection of MTS.

Predecessor: `DERIVATION-20260910-implicit-parent-jets-and-full-shift-defect.md`.
The earlier exact free-root, local reduced residence and implicit-jet
certificates are preserved. This note does not promote them to a solution
of every retained equation or transplant them onto altered boundary histories.

## 1. Build the source without using the observed defect

Let the packed variables be y=(mu,N,v), including face mass, nodal lapse,
scalar velocities and released scalar-slope velocities. Write the original
constraints as Fcal(y;x,pi,C)=0, with Jacobian J=Fcal_y, scalar coordinates x,
momenta pi and outer clock C. At a background free root, the original action
gives x_dot=v and pi_dot=f. Endpoint nodal momentum rates remain zero;
the scalar slope equations are retained.

The full shift equation and its previously measured defect are

    P u_mu = b,       b = j_Gram - j_matter,
    R_shift = P (mu_dot - u_mu).

Now prescribe a TRIAL mass rate u_mu at every face, not the measured
mu_dot. Initially set lapse and free scalar-velocity rates to zero.
Supply the original clock rate and the two endpoint accelerations a.
The resulting first derivative of the original constraint vector is

    k = J[:,mu] u_mu + Fcal_x v - E_pi f
        - (C_dot/kappa) e_outermass + J[:,vend] a,

where Fcal_pi=-E_pi is the canonical momentum insertion map and kappa=1/10.
Thus k is calculable from the background root and original action alone.
No measured mass tangent, shift residual or fitted counterterm defines it.

The helper receives only system/background fields, the existing exact
free-root enclosure, clock data and endpoint accelerations. The runner
loads the previous tangent/residual archive AFTER calling this helper,
solely to check the independent prediction.

## 2. Six explicit additive sources

Split the shift solve into bulk and Gram loads, u_mu=u_B+u_G, using the
same P. At the SAME candidate background, decompose k into:

| Channel | Definition before elimination |
| --- | --- |
| bulk_transport | Differentiate bulk constraints with mu_dot=u_B, x_dot=v, pi_dot=f_B; other trial rates zero. |
| Gram_link_current | J_B[:,mu] u_G from the Gram contribution to the original shift current. |
| Gram_action_variation | Differentiate Gram metric covectors with mu_dot=u_B+u_G and x_dot=v, and include -E_pi f_G. |
| outer_clock_rate | -(C_dot/kappa) e_outermass. |
| left_endpoint_acceleration | J[:,vend_left] a_left. |
| right_endpoint_acceleration | J[:,vend_right] a_right. |

All responses below use the full background J, not a different operator
for each channel. This specifies a useful linear partition, not a unique
causal attribution or a counterfactual GR model at different fields.
In the GR control both Gram input and response columns are exactly absent.

For clarity, the canonical Gram action variation is differentiated directly.
Let B_G be the stored difference factor, S_G the stored sampling map,
q_chi the nodal scalar velocity, and F_n=1-2 mu_n/R. Then

    rho_G = S_G^T (B_G chi)^2 / (2h),
    rho_G,t = S_G^T ((B_G chi)(B_G q_chi)) / h,
    g_mu,t = face_to_node^T [R N rho_G,t F_n^(-1/2)
                           + N rho_G mu_n,t F_n^(-3/2)],
    g_N,t = -R^2 rho_G,t sqrt(F_n)
            + R rho_G mu_n,t / sqrt(F_n).

Together with -E_pi f_G these are the third channel. The lapse rate is
zero in this raw forcing calculation; its later response is handled by J.
Both Gram-current and Gram-action variations are retained. Dropping either
because their responses nearly cancel would change the problem.

## 3. Eliminate the free velocities and expose compatibility

Use m for free mass coordinates (inner mass excluded), N for all lapse
coordinates and z for free scalar velocities (two nodal endpoints excluded).
If there are n nodes, there are n free mass and n lapse coordinates and
2n-2 free scalar velocity coordinates. Define M=J_zz and

    S_ab = J_ab - J_az M^(-1) J_zb,       a,b in {m,N},
    kbar_a = k_a - J_az M^(-1) k_z.

For a trial satisfying every mass shift rate, the mass-constraint tangency
equations determine the lapse rate:

    S_mN N_dot_trial = -kbar_m.

The remaining lapse-constraint tangency obstruction is

    W = kbar_N + S_NN N_dot_trial.

This is an independently sourced obstruction, rather than R_shift used
as its own explanation. All these operations are linear in k at fixed
background. To recover the actual reduced free-root tangent, allow a
free-mass correction delta_m. The two block equations imply

    T_m = S_Nm - S_NN S_mN^(-1) S_mm,
    T_m delta_m = -W,
    R_shift = P[:,m] delta_m.

The inner mass correction is zero by the reduced rule. This does NOT make
the inner row of the covector P delta_mu zero. No covector row is discarded.
The checked inverses of P, M, S_mN and T_m make these equivalences valid
on the archived root boxes. The new source prediction and previous
implicit-jet prediction overlap componentwise in all 18 cases; the largest
midpoint difference is 4.430e-19. Interval overlap is a numerical check of
the algebra above, not by itself a proof of an algebraic identity.

## 4. Isolate one genuine kinetic-projection term

At the stored quadrature nodes, let Wq be the positive diagonal weight
with entries w_q R_q^2/(N_q sqrt(F_q)), V the free scalar-velocity map,
Nmap the lapse reconstruction and q_q the scalar velocity reconstruction.
Set U=diag(q_q/N_q) Nmap and define the weighted projection

    Pi U = V (V^T Wq V)^(-1) V^T Wq U.

The canonical kinetic Hessian gives

    S_NN = (U-Pi U)^T Wq (U-Pi U) >= 0.

The canonical Gram potential contributes no extra lapse-lapse or velocity
Hessian at this slice. The helper independently encloses this Gram formula
and intersects it with the ordinary Schur enclosure of S_NN.
This derives the sign and structure; it does not assume S_NN=0.

Now separate W_direct=kbar_N and W_projection=S_NN N_dot_trial.
Across these 18 states, the archived upper bound for ||W_projection||_inf
divided by the lower bound for ||W_direct||_inf is at most 3.368e-4.
The isolated kinetic-projection contribution therefore cannot cancel the
direct obstruction on these states. The corresponding shift responses
are also archived separately; different response conditioning is retained.

**Important limitation:** W_direct still contains scalar Galerkin and
weak-to-strong compatibility effects. This result does not eliminate all
projection errors, identify quadrature as the cause, or prove convergence.
It is an exact finite-algebra partition, not yet the full radial source H
decomposition requested by the predecessor's continuum reconstruction identity.

## 5. Derive and test a boundary-acceleration law

Instead of assuming that boundary data explain the defect, keep all fields,
clock rate and other reduced rules fixed and treat a=(a_left,a_right) as
unknown. The source is affine in these two accelerations:

    W(a) = W_other + E a.

E contains the two unit-acceleration obstruction columns. Let B select the
first and last lapse equations. A full solution W(a)=0 must satisfy

    a_star = -(B E)^(-1) B W_other.

The 2-by-2 inverse is verified over every existing initial root box. Thus
any acceleration-only repair MUST use this unique a_star there. Substituting
it into the other lapse rows leaves a strictly nonzero enclosed interior
obstruction in every case. Consequently **no choice of these two endpoint
accelerations alone closes the full shift/constraint tangency system** at
these 18 fixed backgrounds with the other rules unchanged.

For example, the final N64 metric-Gram state has original accelerations
approximately (-0.139171051, 0.0557737204). Necessary boundary values lie in

    a_left  in [-0.147932613, -0.147932553],
    a_right in [ 0.061897185,  0.061897225].

Yet the remaining interior obstruction has norm in
[5.39168e-7,5.39180e-7]. The two boundary entries may be set exactly to zero
when predicting this hypothetical trial's shift response because their
defining linear system has been solved. The other entries are never zeroed.

This trial reduces the shift norm in 17/18 cases but worsens it for N16
metric-Gram at saved time zero (about 2.049e-7 to 2.656e-7). There is no
universal improvement claim. More importantly, reduction is not closure.
No boundary history was changed or evolved. Previous residence estimates
are not certificates for these alternative histories. Changing clock
rate, other boundary data, trial spaces or reduction remains outside this test.

## 6. Representative enclosed results

At saved time 0.01, the following display intervals are rounded outward
from the archive. All quantities are finite covector/source norms in the
existing code normalization, not SI observational errors. Changing mesh
also changes the basis and covector coordinates: this is not a convergence proof.

| Intervals | Branch | Original source-predicted shift norm | Necessary-boundary trial shift norm | Remaining interior W norm |
| --- | --- | --- | --- | --- |
| 16 | GR | [7.18329e-7,7.18333e-7] | [7.71011e-8,7.71040e-8] | [5.15387e-6,5.15389e-6] |
| 16 | metric-Gram | [1.91599e-6,1.91600e-6] | [1.96617e-7,1.96619e-7] | [8.48440e-6,8.48442e-6] |
| 32 | GR | [3.01796e-8,3.01820e-8] | [6.49456e-9,6.49710e-9] | [7.80438e-7,7.80445e-7] |
| 32 | metric-Gram | [6.33058e-8,6.33114e-8] | [1.35282e-8,1.35323e-8] | [1.83491e-6,1.83493e-6] |
| 64 | GR | [8.86837e-10,8.89208e-10] | [5.40800e-10,5.43881e-10] | [2.10994e-7,2.11001e-7] |
| 64 | metric-Gram | [1.23691e-8,1.23697e-8] | [3.11991e-9,3.12006e-9] | [5.39168e-7,5.39180e-7] |

For the final N64 metric-Gram state the approximate individual shift-response
norms are: bulk 2.412e-7, Gram link 3.122e-8, Gram action 3.434e-8,
clock 4.72e-12, left endpoint 2.269e-7 and right endpoint 1.253e-8.
The actual summed vector has norm about 1.237e-8. Individual norms do NOT
add as signed scalars: these vectors have substantial cancellation.

## 7. Validation and evidence boundary

The run checks actual archived basis, Gram, link and assembly maps;
positive metric/lapse charts; eight inverse applications per state;
independent first-Taylor source assembly; old/new mass and shift prediction
agreement; direct-plus-projection response; Gram symmetry; necessary
boundary equations; exactly absent GR Gram channels; and exact archive
roundtrips. Multiple-right-hand-side and singular-matrix controls are included.

Each solve uses a floating preconditioner R only as a chosen exact matrix.
Outward arithmetic bounds Bmat >= abs(I-R A), verifies ||Bmat||_inf<1,
and verifies a componentwise radius d satisfying

    Bmat d + abs(R (load-A center)) <= d.

This proves the inverse/solution enclosure under the inherited IEEE
outward-arithmetic assumptions, not by trusting a floating inverse norm.
The arithmetic applies to the exact real interpretation of the realized
binary maps/weights, with rational kappa=1/10. It is not a proof that those
maps reproduce ideal continuum integrals or every desired boundary identity.
No automatic proof-assistant or independent implementation review is claimed.

Authoritative outputs:
- `scripts/annular_shift_source_schur_20260910.py`
- `scripts/derive_annular_shift_source_schur_20260910.py`
- `source-intake/navier-stokes/20260910/annular-shift-source-schur-attempt01/status.json`
- `source-intake/navier-stokes/20260910/annular-shift-source-schur-attempt01/canonical_N64_metric_Gram_sample64.npz`
- `source-intake/navier-stokes/20260910/annular-shift-source-schur-final-integrity.json`

Attempt01 contains all 18 array archives and executed source snapshots.
Earlier probe01/probe02 directories are retained as development evidence,
not substituted for the final 18-state result. The final seal validates
inherited hashes, cited paths and a resume snapshot. The protected-workbench
check is an mtime scan since this turn's start, not a full pre-turn hash baseline.

## 8. Next derivation, without restarting the same audit

The free-root existence and actual first/second jets are no longer missing.
The finite shift mismatch now has an independently evaluated action source.
The acceleration-only remedy has been constructed and found insufficient.

Next derive the remaining direct bulk scalar/metric compatibility source
from the weak equations: retain integration-by-parts endpoint reactions,
internal traces, test-space projection commutators and quadrature remainders,
with the Gram link/action pair kept together. First isolate a term whose
cancellation follows from the original action or whose error can be bounded;
then test an action-consistent repair on the same GR and candidate states.
Do not infer that quadrature is responsible merely because other terms are small.
Do not define a correction from the observed residual and call it a derivation.

Full shift closure, continuum convergence, a horizon theorem and local-GR
recovery remain unproved. No new numerical evolution, GitHub action,
galaxy-work edit or frozen-workbench edit is part of this checkpoint.
