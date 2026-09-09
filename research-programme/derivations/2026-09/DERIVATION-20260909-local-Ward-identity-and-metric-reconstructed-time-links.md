# Local Ward identity and metric-reconstructed time links

2026-09-09. Private continuation. Numerical formulation progress, not an
empirical MTS confirmation, black-hole result or complete local-GR proof.

## 1. Outcome

The nonzero mass-flow residual now has an explicit action-derived identity.
It is accounted for by finite reconstruction/product defects, scalar lifting
work and boundary reactions. Every shift direction is tested; no bad mode
or equation is projected out. The identity also holds on off-shell probes.

That derivation suggested a concrete change to the finite action: reconstruct
the ADM metric first, then calculate and integrate its time connection.
The earlier action instead interpolated nodal samples of the connection.
The new first variation is independently checked against nonlinear metric
time-flow integration. No compensating source or fitted coefficient is added.

On six matched patches the change reduces the candidate mass-rate mismatch
by factors 3.48-6.13. On N64 it is comparable to the GR discretization error.
Both remain nonzero. Initial constraints, phase data, boundary data, the
scalar lifting and the GR control are unchanged. The old action and its
results remain available as an explicit comparison, not overwritten.

## 2. The continuum identity and its finite counterpart

Use the existing areal ADM variables, F=1-2mu/R-Lambda R^2/3, L=F^(-1/2),
gamma=N^2 F, q=chi_t, w=chi_R, and V=V_t=0 AFTER variation of the full action.
For an infinitesimal active time generator f(t,R), the slice transformations
are

    delta chi=f q,    delta mu=f mu_t,
    delta N=f N_t+N f_t,    delta V=-gamma f_R.

The scalar radial and temporal jets obey delta w=f w_t+q f_R and
delta q=f q_t+q f_t. Direct density differentiation proves that the
coefficients of f_R and f_t in delta L-d_t(f L) vanish before spatial
projection. The coefficient of f cancels by the ordinary chain rule.
For the Gram principal density a, the corresponding exact identities are

    q a_w = gamma a_V,       q a_q + N a_N = a.

Write E for the action Euler covectors. The continuum Noether combination
at this slice has the form

    q E_chi + mu_t E_mu - N d_t E_N + d_R(gamma E_V)=0,

with boundary and any additional externally prescribed fields treated
explicitly. This is NOT assumed to be an exact symmetry of a fixed finite
interpolation space.

For the actual mixed discretization w=D chi+I, the required lifting generator
for a time-independent spatial test f is

    L_f = f (Dq+I_t) + q f_R - D(fq).

Its derivative uses q_t and I_tt. I has not been set to zero or freely tuned.
Let S_f=-gamma_face f_R(face), and use reconstructed f at the mass faces,
nodal values for scalar/lapse variations, and independent Hermite nodal
values AND slopes for the test function. The exact finite identity is

    S_f^T E_V = D_bulk[f] - D_Gram[f] - L_f^T E_I
                -(f_node q)^T E_chi -(f_face mu_t)^T E_mu
                +(f_node N)^T d_t E_N.

E_I=L_I-d_t L_(I_t). The last three terms retain endpoint reactions and
any residual free Euler rows. Nonzero boundary terms are essential even
when the free constraints and their tangents have been solved.

## 3. The right-hand side is explicit, not a renamed residual

For the bulk action, form the difference between the reconstructed nodal/
face variations and the pointwise continuum transformations at the shared
quadrature. The amplitude defects are in mu, mu_R, N, chi, q, w and V.
Contract each with its own density derivative. The f_t coefficient has
two product defects, in lapse and scalar velocity. Then

    D_bulk = sum(amplitude defects) - d_t sum(f_t coefficient defects).

All nine vectors are saved separately. Complex-step time derivatives are
checked against two finite-difference steps, and the reconstructed bulk
variation is checked against the original shift-unfixed ADM action.

For each Gram factor ell, z=T chi, a_bar=S a, rho=S^T(z^2)/(2h), and

    j_li = a_i S_li z_l (Tq)_l/h - q_i T_li a_bar_l z_l/h.

For its linear time displacement Y_li, define

    e_li = Y_li + f_i - f_anchor(l),
    Delta a_i = a_mu,i [P_face(f_face mu_t)-f_i P_face(mu_t)]_i
                +a_V,i [P_face(S_f)+gamma_i f_R,i].

The complete reduced Gram remainder is

    D_Gram[f] = rho^T Delta a - sum_li j_li e_li.

This follows by subtracting the derivative of the linear time-boundary
term from the raw link variation. Coefficient-time and Y_t terms cancel;
they are not neglected. The identity sum_i j_li=0 eliminates arbitrary
factor-anchor constants. The source retains both coefficient and connection
reconstruction contributions.

Thus the measured E_V is now tied to identifiable interpolation and boundary
work. This algebra does not imply those remainders vanish or are harmless
under arbitrary evolution. Off-shell tests deliberately retain nonzero
scalar and lapse Euler rows and still obey the same identity.

## 4. No hidden shift directions

The enriched test generator has 2n parameters for n+1 shift faces. It has
full row rank on these patches. More strongly, an explicit right inverse
can be constructed without SVD truncation or a least-squares solve.

There is one interior face in each scalar cell. Let its fractional position
be theta in (0,1). Cubic Hermite interpolation gives

    f_R(face) = 6 theta(1-theta)(f_right-f_left)/h
                +(3theta^2-4theta+1)d_left +(3theta^2-2theta)d_right.

For any desired shift vector u, set the desired face derivative to
-u/gamma_face. Fix the two endpoint slopes to their desired derivatives,
set the remaining slopes to zero, choose f_leftmost=0, and solve the written
formula successively for each next nodal value. The positive coefficient
6theta(1-theta)/h guarantees the construction. If R is this map and G maps
generator parameters to shift variations, G R=identity on ALL shift faces.

Consequently E_V=R^T times the independently derived Ward right-hand side.
This is a verification/remainder bound, not a correction applied to E_V.
The final integrity calculation checks this explicit reconstruction for all
18 old/new action samples. SVD norms are also diagnostic finite-state bounds,
not uniform or interval-certified continuum estimates.

## 5. A correction obtained from the metric, not from fitting the residual

The old finite action used A_i=-V_i/(N_i^2 F_i-V_i^2) and then piecewise
linear interpolation of these nodal A samples. The alternative is

    A_h(t,R) = -V_h(t,R)/(N_h(t,R)^2 F_h(t,R)-V_h(t,R)^2),

where V_h and mu_h use the already declared face basis and N_h the nodal
basis. Integrate phi_R=-A_h(phi,R) and J_R=-(A_h)_t J as before. The Gram
factor density and its scalar/coefficient sampling are otherwise unchanged.
This is a different finite action away from V=0, explicitly retained as a
new computational candidate, not silently relabelled as the old action.

Its first displacement matrix at V=0 is

    H_(li),j = integral_anchor^node Q_face,j(R)/(N_h^2 F_h) dR,
    Y = H delta V.

The reduced first shift variation becomes

    (U_Gram)_V = P_face^T(rho a_V) - H^T j.

Positive-branch metric link integrals agree under 4- and 8-point quadrature
on the split mesh. Independent nonlinear characteristic integrations of
the new action at two perturbation sizes verify this variation, including
its time-boundary term. The full Ward identity also holds for the new H.

At V=0 the initial potential, gradient and Hessian in (mu,N,q) are unchanged.
The GR branch is bit-for-bit unchanged in the comparison. Only the derived
Gram shift current changes, so the flux-derived inner mass rate and the
resulting constraint tangent are recomputed. No initial root is refitted.

## 6. Matched numerical results

Maximum |mu_dot_constraint-mu_dot_flux| in the existing fixture normalization:

| fixture | grid | GR control | old Gram links | metric-reconstructed links |
|---|---:|---:|---:|---:|
| canonical | 16 | 9.139e-7 | 1.640e-5 | 2.674e-6 |
| canonical | 32 | 6.493e-7 | 3.836e-6 | 8.548e-7 |
| canonical | 64 | 2.237e-7 | 9.129e-7 | 2.363e-7 |
| nonlinear | 16 | 1.156e-6 | 1.637e-5 | 3.114e-6 |
| nonlinear | 32 | 8.576e-7 | 3.837e-6 | 9.722e-7 |
| nonlinear | 64 | 2.807e-7 | 9.259e-7 | 2.659e-7 |

On N64 the new/GR ratios are 1.057 and 0.947: comparable numerical errors,
not a physical competition won or a claim of exact GR recovery. The new
weak shift residuals remain 1.90e-8 and 2.23e-8. Every branch still has
all_shift_rows_closed=false. These finite fixtures do not establish a
uniform error bound, complete constraint algebra or causal evolution.

The old action Ward validator finishes 120/120; the new metric-link action
comparison finishes 50/50. Identity errors are below 1e-17 in these tests.
They validate the specified formulas and finite calculations, not the
entire fundamental framework.

## 7. Exact next task

Use the metric-reconstructed-link action as the next computational branch,
with the old action and GR saved as controls. Re-derive its local quadratic
reduction and metric first-order/constraint blocks using the new H and its
metric derivatives; do not inherit the old finite-action stability gates.
Then attempt a short matched time-evolution smoke on the owned local patch,
recording actual constraint drift against GR. Keep the present nonzero
remainder and its explicit Ward identity as the diagnostic.

No further hunt for the current, initial roots or a missing cancellation
coefficient is needed at this point. No arbitrary I_t, boundary adjustment,
filtered shift row or mass-flux counterterm is allowed as a shortcut.

## 8. Sources and preserved attempts

Local paths are relative to post-checkpoint-work:

- `DERIVATION-20260909-constrained-initial-slice-solve-and-mass-flux-tangent.md`.
- `scripts/annular_local_ward_identity_20260909.py`.
- `scripts/derive_annular_local_ward_identity_20260909.py`.
- `scripts/annular_metric_time_links_20260909.py`.
- `scripts/derive_annular_metric_time_links_20260909.py`.
- `scripts/finalize_annular_local_ward_20260909.py`.
- `source-intake/navier-stokes/20260909/annular-local-Ward-identity-derived-validated/status.json`.
- `source-intake/navier-stokes/20260909/annular-metric-time-links-derived/status.json`.
- `source-intake/navier-stokes/20260909/annular-local-Ward-final-integrity.json`.

One generic unfactored symbolic simplification was stopped after more than
five CPU minutes, before numerical work. Its executed source and status
remain in `source-intake/navier-stokes/20260909/annular-local-Ward-identity-derived/status.json`.
A subsequent bookkeeping attempt failed because that interrupted status had
not yet saved its own script hash. The failure is preserved in
`source-intake/navier-stokes/20260909/annular-local-Ward-identity-derived-factored/status.json`.
The final run uses equivalent generator-coefficient identities in F coordinates
and records the saved source snapshots directly. No numerical tolerance or
physics result was changed to resolve either issue.

All final workers exited. Private/local only; no subagents, GitHub actions,
shared-process shutdowns, frozen-workbench or galaxy modifications.
