# Independent local Ward-source prediction of the mass-current defect

Private derivation, September21,2026. Numerical run complete; independent validation status is recorded by the final integrity seal. This follows `DERIVATION-20260921-Gram-energy-and-radial-mass-current.md`, using the same action, modes, normalized constants, saved states and metric solutions.

## 1. Observable to predict, not an input to reconstruct the source

Let I=N/sqrt(F), a=kappa/I, and R=mu_t+J_total. The established radial constraints give

    (I R)_r = -kappa I r^2 H,  H=div_mu T^mu_t.

With constant central mass and no incoming current below the support, the inner R is zero. Therefore

    R_predicted(R_cut) = -a(R_cut) integral_(below support)^R_cut I r^2 H dr.

All terms on the right must come from the action and independent Euler-Lagrange quantities. We must not define H by differentiating the measured R. The saved measured R is used only for final comparison and for explicitly disclosed diagnostic radius selection. Existing archive tangent probes supply time derivatives; this is not a new evolution experiment.

## 2. Wave cells and moving faces

Inside each affine reference cell set T=phi_t=u_t-Wg, g=phi_r=u_x/J, W=chi_b V, alpha=r^2/(N sqrtF), beta=r^2 N sqrtF. Then

    pi=J alpha T,
    H_xflux = -alpha T W-beta g,
    E_u=-partial_t pi-partial_x H_xflux,
    integral I r^2 H_wave dr = integral T E_u dx,

with the last equality only for the cell-interior contribution. Internal P2 faces cannot be dropped. Define [f]=f_right-f_left and e=(alpha T^2+beta g^2)/2, j=-beta T g. Their weighted stress-defect power is

    Q_face = -[j-W e]
           = T_average (beta-alpha W^2)[g].

The second equality uses continuity of the reference field rate and [T]=-W[g], with continuous physical coefficients and mesh velocity. It avoids multiplying a delta by an arbitrary one-sided time trace. At the moving pinned anchor, u_t=0 and Q_anchor=V*traction, with the previously derived traction sign. Ordinary faces are accounted separately. Exterior stress jumps are also retained explicitly rather than silently set to zero. Endpoint field values are near numerical zero (~1e-53), but no unsupported exact exterior field equation is inferred from that observation.

## 3. Dust work from the actual proper-time action

For L_d=-m*s, s=sqrt(N^2-V^2/F), define p_d=mV/(F*s) and E_d=partial_b L_d-d_t p_d. The weighted temporal stress-divergence measure is

    I r^2 H_dust = V E_d delta(r-b).

This follows from dH_d/dt=-V E_d-partial_t L_d, retaining metric exchange. E_d is evaluated from the archived time-dependent lapse/metric and recovered velocities, not set to zero because geodesic motion is desired. Material weights are included at the final z integration.

## 4. Gram work: reduce the temporal defect rather than assert it vanishes

The same action has h_i=gamma_i l_i, l_i=(S^T y^2/2)_i, y=D u, gamma_i=beta(r_i)/J_i. Its already derived physical energy density and flux are h=sum h_i delta(r-r_i) and j_G=graph cut current+moving-node advection. Their balance is

    h_t+(j_G)_r=sum_i[-v_i F_G,i+gamma_dot_i l_i]delta(r-r_i),
    gamma_dot_i=gamma_b,i V+gamma_i(N_t/N+F_t/(2F))_i.

The existing polar diagonal metric variations of this potential correspond to rho_G=p_G=h/(I r^2). For the candidate mixed component J_G=a*j_G, the weighted temporal stress defect consequently satisfies

    I r^2 H_G = -h_t-(j_G)_r+h(N_t/N+F_t/(2F))
              = sum_i[v_i F_G,i - V gamma_b,i l_i]delta(r-r_i).

This is an off-shell temporal-defect identity, not a proof that the defect is zero or a unique general shift completion. It strengthens the previous candidate-current diagnostic by deriving the action work that it must supply. The distributed source-work term is located at the Gram nodes; relocating it to b would change the local identity. No redshift bond exchange is discarded: differentiating J_G=a*j_G together with the integrating factor cancels the spatial a derivative in this temporal component.

## 5. Complete independently computable prediction

At each material label, for a physical cut R_cut, compute

    Q_wave_cell = integral_(chi(x)<R_cut) T E_u dx,
    Q_wave_face = sum_(faces<R_cut) Q_face,
    Q_dust = V E_d * 1_(b<R_cut),
    Q_Gram = sum_(r_i<R_cut) [v_i F_G,i - V gamma_b,i l_i].

Then R_predicted=-a(R_cut)*integral w(z)*(Q_wave_cell+Q_wave_face+Q_dust+Q_Gram)dz. Separate ordinary faces, pinned-anchor face, exterior faces, Gram field and Gram source work in the outputs. No term is chosen from the measured residual and no numerical multiplier is fitted.

## 6. Fixed experiment and acceptance gates

- Use the qualified wider endpoint only: reference, MTS primary and MTS alternative, all16,425 components,21 archived base/probe phase/geometry pairs. Initial states were derivative-floor-sensitive in the prior calculation.
- Select up tofive common physical radii from the prior reference grid: both extremes, its largest defect, and strongest wave current outside the source on each side. These are diagnostic targets, not held-out predictions. All cuts must avoid the dust support.
- Split spatial integration at the actual physical cuts, every P2 edge and every radial metric interval. Split material-label integration at each relevant node/cut crossing. Do not mask an unsplit Gauss rule across a moving discontinuity.
- Pair reference/material orders8/12; retain two Richardson estimates from the three saved probe sizes. Prediction tolerance5e-12+0.05*max|R_observed| per branch, paired quadrature tolerance1e-12. Failures are retained with unchanged tolerances.
- Store separate cell space/time work, all six probe work integrals, face traces and powers, dust momenta, nodal Gram powers and cut masks. Keep one full quadrature spot per branch/order for independent pointwise reconstruction; avoid duplicating gigabytes of archived states.
- A close reconstruction identifies the measured defect's mechanism, not a new observational accuracy bound or automatic vanishing of the local Ward source. Numerical differentiation, quadrature and the finite-element weak-versus-pointwise distinction remain separately visible.

## 7. Local sources

- `scripts/annular_candidate_Ward_source_20260921.py`
- `scripts/run_annular_candidate_Ward_source_20260921.py`
- `source-intake/navier-stokes/20260914/annular-candidate-energy-current-final-integrity.json`
- `source-intake/navier-stokes/20260914/annular-candidate-reaction-balance-attempt02/status.json`
- `source-intake/navier-stokes/20260914/annular-candidate-energy-current-attempt01/status.json`

## 8. Constructive next mechanism: the missing kinetic current

There is a concrete variational construction to test after the decomposition, not merely another missing-input label. In a fixed spatial ansatz with quadratic field action L=(v^T M v-u^T K u)/2, let M,K be symmetric, M positive/invertible and coefficients allowed to depend explicitly on time. Let M_R,K_R be obtained by integrating the SAME physical energy only up to a cut, not by inventing nodal energy weights. With E=-M*a-Mdot*v-K*u, define

    J_R = v^T(M_R M^(-1) K-K_R)u
        + v^T(M_R M^(-1) Mdot-M_Rdot)v.

Direct differentiation of E_R=(v^T M_R v+u^T K_R u)/2 yields

    dE_R/dt + J_R
      = -1/2 v^T M_Rdot v + 1/2 u^T K_Rdot u
        - v^T M_R M^(-1) E.

For a whole-domain cut, M_R=M and K_R=K, hence J_R=0. For a partial cut the mass-matrix terms transfer kinetic energy and cannot in general be replaced by a continuum pointwise flux evaluated on an approximate FE solution. This formula is fixed by the quadratic action and chosen physical energy allocation; it contains no fitted multiplier. The finite-dimensional identity is independently symbolically checked in the sealer.

This is a controlled linear/fixed-spatial-ansatz lemma. The actual source moves, and its full mass matrix depends on field/source coordinates, so substituting this formula unchanged into the MTS candidate would omit connection, cross-velocity and moving-cut terms. The next construction must derive those terms from its actual action and compare the resulting current with metric/shift variation. That is the proposed route from today's localized Ward defect to a consistent derived current.

## 9. Completed numerical result

The single-core run completes in1269.09seconds (about21minutes), with82 implementation checks and all15 predeclared scientific comparisons passing. There are six branch/order cases,3,840 segmented material samples and30 cut predictions. The actual targets are5.21,5.61734375,6.2221875,6.444375 and6.79 in the inherited coordinate units. No dynamics, fit coefficients or modes were changed.

| Branch | Maximum observed defect | Maximum action-source prediction | Maximum absolute mismatch, order12 |
| --- | ---: | ---: | ---: |
| Reference | 1.3749768e-11 | 1.5176071e-11 | 1.4263029e-12 |
| MTS primary | 3.6665802e-11 | 3.8078414e-11 | 1.4233263e-12 |
| MTS alternative | 3.6665802e-11 | 3.8078426e-11 | 1.4233384e-12 |

The action-derived source therefore predicts the small residual with no added multiplier. It does not reproduce every digit of the finite-differenced mass profile. The remaining~1.4e-12 discrepancy is similar in the reference and both MTS branches. Its post-source near-common-offset pattern suggests checking accumulated mass-derivative error, rather than immediately attributing it to new physical coupling. That diagnosis remains a hypothesis until checked against a direct constraint tangent or another independent time-derivative calculation.

Changing both quadrature orders8->12 changes the predictions by at most2.36e-18; switching between the two archived Richardson estimates changes them by at most2.27e-17. The earlier mass-profile derivative sensitivity outside the source was~1.38e-12, much larger than these new action-source sensitivities. These are observed differences, not rigorous numerical-error bounds.

The source terms are individually larger than their sum. At r=6.2221875 in primary MTS, order8 contributions to R are approximately: wave cells+1.33025e-9, ordinary faces-1.26530e-9, anchor+3.74670e-11, dust-3.67428e-11, Gram field-2.75301e-11 and Gram distributed source-6.42235e-14. Their sum is3.80784e-11. The reference has the same important cell/face and anchor/dust cancellations without the Gram contributions. This is why dropping finite-element faces or assuming the dust follows an unforced geodesic gives the wrong local balance.

The independent checker reconstructs the segmented integrations, individual cut masks, pointwise spots, source momenta from original metric archives, representative Gram/face values from parent action data, and every scientific gate. It also records omission/sign controls and an integrating-factor difference diagnostic using the outer cut. The latter is explicitly post-run: it compares differences of R/a to test a common-offset pattern, not a fitted physical boundary condition.

The principal advance is a source-based reconstruction of the previously unexplained mass-current residual, alongside a constructive kinetic-current formula for the simpler fixed-spatial-ansatz case. Next: extend that current derivation to the actual moving-source action, keeping coordinate-dependent inertia, cross-velocity, moving-cut and metric-exchange terms. Use a direct radial-constraint tangent to separate any remaining mass-differencing offset if it limits that comparison.
