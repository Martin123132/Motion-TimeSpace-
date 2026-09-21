# Derive the remaining wave/source reaction from the actual action

## Question and inherited experiment

The preceding source-acceleration calculation is `DERIVATION-20260921-physical-source-acceleration.md`, sealed by `source-intake/navier-stokes/20260914/annular-candidate-source-acceleration-v3-final-integrity.json`. Its wider-probe endpoint comparisons find that the independently derived moving-anchor traction matches the raw non-dust reaction within1.2-2.1percent. This calculation attempts to explain that remaining vector difference, rather than fit a correction.

Keep the same reference, MTS primary and MTS alternative states, all16,425 canonical components, source mass, moving zero-field anchor and live radial geometry. Use initial states and the wider-probe endpoints; the original narrow-endpoint failures remain in the inherited record. No new trajectory, spatial mesh, coupling or physical boundary condition is introduced. Initial reactions are small and differentiation-sensitive, so they are controls rather than presumed physical signals.

## 1. Local moving-coordinate identity

For each material label write the physical radius as r=chi(x,b), with J=chi_x and d=chi_b. On each affine mesh cell d_x=J_b and J_x=0. Let u(t,x)=phi(t,chi(x,b(t))), V=b_dot and

    g=u_x/J, W=d*V, T=u_t-W*g,
    alpha=r^2/(N*sqrt(F)), beta=r^2*N*sqrt(F),
    L_ref=J*(alpha*T^2-beta*g^2)/2.

Here T is the physical fixed-radius field time derivative. The bulk density and its source/field derivatives are those implemented in `scripts/annular_candidate_midpoint_20260921.py` and `scripts/annular_candidate_coordinate_covectors_20260921.py`; this derivation does not substitute a different continuum action for the saved candidate. The field momentum, reference flux and source momentum density are

    pi=J*alpha*T,
    H=partial L_ref / partial u_x=-alpha*T*W-beta*g,
    eta=-d*g,
    p_b=eta*pi.

The source coordinate derivative holds the metric profile fixed exactly as in the inherited candidate action; its subsequent time derivative includes the live geometry response. Differentiating the same density gives the off-shell identity

    partial L_ref / partial b - d(p_b)/dt
      = partial_x B + eta*E_u,
    E_u=-partial_t pi-partial_x H,
    B=d*(L_ref/J-g*H)
     =d*[alpha*u_t^2+(beta-alpha*W^2)*g^2]/2.

No field equation, free-geodesic axiom or zero boundary force is used to derive this equality. The accompanying symbolic test treats the local time and space jets independently and checks the identity exactly. The numerical calculation evaluates both sides separately on the actual saved states.

## 2. Do not discard the internal cell faces

Integrating cell by cell, the bulk source reaction is the sum of the B jumps and the volume integral of eta*E_u. At the moving anchor u=0 at every time, so u_t=0, d=1 and W=V. Its jump is precisely the previously derived traction

    T_anchor=(beta-alpha*V^2)*(g_left^2-g_right^2)/2.

At an ordinary P2 cell face u_t is continuous but g need not be. The other jumps are therefore not automatically zero. They are retained as a separate vector contribution, not identified with new physical walls. Exterior contributions are also evaluated; the source mesh displacement vanishes at the fixed outer endpoints.

The Gram action has no explicit velocity dependence in this candidate. Its source force is evaluated directly from the existing factor/sampling matrices, not inferred by subtracting the desired result:

    F_Gram,b = -1/2 sum_k [sampling(gradient_source)]_k * [factor(u)]_k^2.

After the same material projection as the canonical equations, the target balance is

    R_non-dust = T_anchor + J_internal + B_exterior
                 + integral eta*E_u dx + F_Gram,b.

The finite-element field equation is weak, whereas eta can jump at cell faces. Here the volume term means the sum of ordinary cell-interior integrals; it is not an undefined product of a discontinuous eta with a distributional flux delta at a face. Consequently weak field stationarity alone does not justify dropping the volume term or its compensating internal jumps. This calculation retains both, including their cancellation.

## 3. Reconstruct the measured derivatives and test the identity

Rebuild the radial primitive representation from each saved radial state and its actual q,v-dependent loads. Verify the original radial grid, residual, sampled metric/clock/gradients, and base full force/momentum before using the replay. No new root or gravity solution is selected. Save the reconstructed radial primitive arrays for reuse.

At fixed reference quadrature points, differentiate pi and p_b with the six saved plus/minus probes and the two Richardson combinations. Initial steps are1e-5,5e-6,2.5e-6; endpoint steps are1e-4,5e-5,2.5e-5. This is a canonical directional derivative, not a longer physical trajectory. Compute H_x analytically from the piecewise polynomial field and radial metric derivatives. Evaluate B on each cell face using the correct one-sided affine Jacobian at the source anchor.

Compare independently:

- The pointwise algebraic identity before integration.
- Integrated B_x versus the sum of all cell-face contributions.
- The product-rule derivative eta*pi_dot+eta_dot*pi versus direct differentiation of p_b.
- The sum of volume, face and Gram contributions versus the previously measured non-dust source reaction.
- Both Richardson estimates and reference quadrature orders16/32, retaining material order48.

For the projected force comparisons, predeclare an absolute tolerance1e-13 plus1e-3 times the raw reaction norm, in inherited units. This targets substantially less than the previous1.2-2.1percent remainder. Failed scientific comparisons remain recorded rather than aborting other branches or changing tolerances. Numerical differences are diagnostics, not rigorous continuum error enclosures. The differentiated inverse-root residual remains separately visible from the preceding record.

Packed evidence retains per-point momentum probes, momentum/flux/force/boundary channels, integration measures, material interpolation and face jumps, allowing a separate checker to reconstruct the projected comparisons without invoking the runner's balance routine.

## 4. Results

The completed run passes149 implementation checks and all66 predeclared scientific comparisons. It replays42 archived gravity/phase states across six physical phase points, evaluates both quadrature orders in all branches, and takes1238.40seconds on one restrained worker. The first serialization failure is preserved separately and did not change any mathematical formula or tolerance.

At the wider-probe endpoints, using reference order32:

| Branch | Boundary-only remainder / reaction | Full derived remainder / reaction | Full remainder in inherited force units |
| --- | ---: | ---: | ---: |
| Reference | 0.0125395 | 4.29109e-7 | 1.95208e-15 |
| MTS primary | 0.0208247 | 9.62971e-7 | 4.10739e-15 |
| MTS alternative | 0.0119346 | 8.56868e-7 | 3.66228e-15 |

Thus including the independently evaluated internal jumps, cell field EL and Gram force accounts for the previous1.2-2.1percent discrepancy to below one part per million of the small additional reaction at all three tested endpoints. This is the residual of a finite-grid force identity, not a one-part-per-million error bar on the entire theory or an assertion that the reaction itself vanishes.

The internal-jump and cell-EL vector norms are each approximately1.4e-8, so both are larger than the small remainder and largely cancel. At the endpoints their combination with the Gram source has cancellation ratios approximately512(reference),325(primary) and565(alternative). The explicit MTS Gram source norm is7.72114e-12, while it is zero in the reference. The explanation is therefore not simply that the entire missing force was Gram: the matched cell/field balance is essential. Norms of contributions must not be added as though they were signed scalar forces.

Initial-state full remainders are4.89e-14,5.12e-14 and5.25e-14, corresponding to0.0127percent,0.0323percent and0.0332percent of their much smaller raw reactions. These also pass the unchanged gate, but their underlying acceleration/force signals remain inverse-derivative-sensitive as established in the preceding checkpoint.

Across the complete experiment the largest16/32 quadrature change is1.022e-17, largest integrated cell-identity defect1.721e-18, largest source-momentum product-rule discrepancy6.587e-16 and largest Richardson-estimate change2.813e-15. Both orders and all branches are retained. The remaining force mismatch is dominated by the comparison of fixed-reference differentiated integrals with the original moving-quadrature momentum samples, not an unexplained percent-sized force channel.

Exact tables, independent packed-array reconstruction, and the force-to-acceleration projection diagnostics are recorded in `source-intake/navier-stokes/20260914/annular-candidate-reaction-balance-computed-results.md` and `source-intake/navier-stokes/20260914/annular-candidate-reaction-balance-final-integrity.json`.

## 5. Toward geodesic source motion

The dust identity from the preceding stage turns the right-hand side into the material projection of (m*s/F)*(A_tau-A_geo). Therefore a derived zero of the FULL reaction gives projected geodesic motion, with the same evolving geometry and clock. Separately vanishing boundary traction is not sufficient while internal, field or Gram contributions remain. Conversely, the additional force should not be called a gravity failure merely because a coupled moving interface is not a free test particle.

Use the measured decomposition to decide which term to derive or control next. In a smooth continuum limit internal flux jumps disappear, but the field EL and Gram terms must be treated together using their actual equations. Pointwise geodesic recovery also requires more than cancellation of fifteen material projections. The parent physical interpretation of the imposed moving zero-field anchor remains explicit rather than assumed.

### A derived force-to-acceleration bound, not division by a bare mass

Define kappa(z)=m*s(z)/F(z)>0 on the timelike chart and the material matrix

    G_ab=integral w*kappa*L_a*L_b dz.

Positive quadrature weights and a full-rank cardinal basis make G positive definite. If r=A_tau-A_geo and R_a=integral w*kappa*L_a*r dz, its weighted least-squares material projection is

    Pi r = sum_a L_a*(G^(-1)R)_a,
    ||Pi r||_(w*kappa)^2=R^T G^(-1)R.

An error delta_R in the reaction therefore has the precise projected-acceleration norm

    ||delta(Pi r)||_(w*kappa)=sqrt(delta_R^T G^(-1)delta_R)
      <= ||delta_R||_2/sqrt(lambda_min(G)).

Also ||r||^2=||Pi r||^2+||r-Pi r||^2 in the same weighted norm. Thus driving the derived reaction to zero AND controlling the unresolved material projection recovers the acceleration comparator; a zero source covector alone need not imply a zero pointwise profile. Uniform limits require control of coercivity rather than silently extrapolating through a singular clock/metric chart.

The independent checker evaluates G from the actual saved mass, clock and F, checks positivity, orthogonality and the norm identity, and compares the reconstructed acceleration profile with the preceding measured profile. It retains the inverse-root correction explicitly: R_decomposed+e_dot is compared with the dust/geodesic covector, while the raw force balance remains compared with R_raw. This finite-quadrature linear-algebra bound does not turn a numerical residual into a certified continuum error bar.

As a separate analytic control, a constant-coefficient wave phi=a_side*(r-V*t) on either side of a prescribed constant-speed pinned interface solves the bulk wave equation. Its force is exactly(beta-alpha*V^2)*(a_left^2-a_right^2)/2: equal squared gradients give zero force, unequal gradients give the correctly signed pressure. This tests the mechanism without pretending that constant coefficients are the evolving spherical MTS solution or that an unbalanced force allows a free source to keep constant speed.

## 6. The next conservation calculation already has a starting identity

For the bulk wave in physical radial coordinates define

    e=(alpha*phi_t^2+beta*phi_r^2)/2,
    j=-beta*phi_t*phi_r,
    E=-partial_t(alpha*phi_t)+partial_r(beta*phi_r).

Direct differentiation gives the exact off-shell identity

    partial_t e + partial_r j
      = -phi_t*E - alpha_t*phi_t^2/2 + beta_t*phi_r^2/2.

The last two terms are exchange with the explicitly changing geometry. They must not be dropped by demanding separately constant wave energy. At a moving pinned boundary phi_t=-V*phi_r, the flux relative to that boundary obeys

    j - V*e = V*T,
    T=(beta-alpha*V^2)*phi_r^2/2.

Thus the boundary force derived in this checkpoint has exactly the corresponding mechanical power transfer. The independent checker verifies both identities symbolically and records the projected source-work rates. They do not by themselves supply the Gram energy current or the metric mass equation.

**Next concrete target:** derive the Gram contribution to the same-action energy flux, combine it with this wave/interface exchange and the dust source, then compare the resulting radial mass current with the evolving saved metric. Keep the full reaction balance and weighted acceleration bound as established inputs rather than repeatedly auditing the same1.2-2.1percent discrepancy.

## 7. Reproduction and scope

- `scripts/annular_candidate_reaction_balance_20260921.py`
- `scripts/run_annular_candidate_reaction_balance_20260921.py`
- `source-intake/navier-stokes/20260914/annular-candidate-reaction-balance-attempt01/status.json`
- `scripts/run_annular_candidate_reaction_balance_v2_20260921.py`
- `source-intake/navier-stokes/20260914/annular-candidate-reaction-balance-attempt02/status.json`
- `scripts/seal_annular_candidate_reaction_balance_20260921.py`
- `source-intake/navier-stokes/20260914/annular-candidate-reaction-balance-final-integrity.json`

Attempt01 stops at output serialization because a pointwise force channel and the full canonical force vector used the same NPZ key. Its preceding five scientific comparisons pass. It is preserved; attempt02 changes only those archive key names and the run destination, leaving equations, data and tolerances unchanged.

Private work only in post-checkpoint-work. No GitHub action, subagents or sibling edits. One BelowNormal worker, single-core affinity and one BLAS thread. Turn baseline2026-09-21T16:47:30Z; check-in by20:47UTC. The numerical script has a7200-second safe boundary, leaving validation time. Executed scripts and completed or failed numerical evidence remain immutable; the current resume file stays mutable with sealed snapshots.
