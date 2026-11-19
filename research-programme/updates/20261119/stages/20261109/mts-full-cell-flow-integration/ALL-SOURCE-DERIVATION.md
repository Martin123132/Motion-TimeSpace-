# Complete-source reuse and integration measure

The expensive source evaluation already saves the entire10-output source, both current columns, three terminal adjoint controls and the coarse-phase/current cross term at every new node. Therefore the full-cell continuation need not stop at a two-channel heavy-flow diagnostic or pay for another native bank.

After independent point validation, all_source_projection.py directly integrates the SAVED full source for every output and both branches on the same frozen segment rules. It computes signed integrals, positive-weight squared integrals/Cauchy scales, current, phase, cross, combined current-and-phase, adjoint interpolation and adjoint-step comparisons. The original acceptance rule is retained: each diagnostic below2e-5, correct volume, and the discrete Cauchy check. Extra triangle indicators are recorded separately, not substituted for that rule.

For any completed union of segments D with N-length |D|:
```
I_D = sum_segments Q_segment[g(N)]
B_D = sqrt(|D| sum_segments Q_segment[g(N)^2])
Delta_current = Q[lambda E delta_x]
Delta_phase = Q[lambda delta_E x]
Delta_cross = Q[lambda delta_E delta_x].
```
Here g is already a source per unit N from the existing equations. In the older phase-coordinate quadrature, dN=dtheta/(dtheta/dN). In direct N integration the measure is dN, not dN times another saved phase Jacobian. The physical phase evolution, clock-dependent source, current histories and coarse-phase comparison remain unchanged. An obsolete phase-coordinate quadrature-measure error is not a physical clock contribution.

This direct full-source calculation can ultimately be checked against the derived composite identity Q_old(S-heavy_flow)+Q_segment(heavy_flow). It avoids a new native computation solely to recover old component controls. Neither method may promote a partial union of MTS segments to a full-cell result. The exact baseline whole-cell source is projected using its existing66saved nodes, without inventing a heavy baseline field or erasing its cancellation flags.

The10outputs are Phi,Psi,D,Q,Pi,theta_c,delta_c,delta_b,delta_gamma,delta_massless. Their actual source coupling is retained; correcting only the displayed Pi/delta_massless channels would be incomplete. Independent compensated adjoint contractions check all saved source/control values;90-digit summation checks the segment integral. These are numerical consistency tests, not new observational fits or continuum certificates.

