# Horizontal metric response of the retained moving-source candidate

Private/post-checkpoint work. The diagonal action, all16,425 coefficients, source clock, material measure, common-space Gram operators and archived states are unchanged. This extends the previous energy-current result through the already documented off-diagonal action prescription, rather than introducing a fitted flux.

## The derivation

The source-anchored horizontal-clock extension already specified on September18 has now been applied to the current common-space/material-Galerkin action. Its metric variation produces a current calculated directly from regular coefficient derivatives, moving P2 faces, moving Gram atoms, nodal Euler work and source-anchored left/right tails. The local atom delta-prime term is retained.

The exact relationship to the previous localized energy current is

    J_horizontal-J_Legendre=P_R-C_R.

Here P_R is the previous Hessian-projected action residual, while C_R is the directly evaluated nodally localized per-layer Euler work. The latter is not set to zero just because the finite Galerkin equations hold. At a source-free cut, exact Galerkin orthogonality implies that unresolved label work can survive only at nodes whose material extent crosses the cut. Nodes wholly on one side still have admissible polynomial test functions.

The current is not calculated by subtracting a measured mass residual. Its independently derived coefficient-current formula is tested against the saved energy-current calculation only afterward.

## Actual nonzero-shift test

For c=epsilon*h(r), use the exact source-anchored leaf

    T=s+epsilon*(H(r)-H(b(s))), H'=h,
    J_T=1-epsilon*h(b)*V,
    beta=2*c*N^2*F/(1+sqrt(1+4*c^2*N^2*F)).

The nodal time derivative includes J_T+c*W_i. This is the moving-node clock term, not a tunable coefficient. Actual finite nonzero-shift action evaluations are compared with raw first variations separately for wave, Gram and dust contributions, using3 material labels and3 spatial profiles in each of the3 branches. The field histories and background are local jets through the archived states and tangents. This checks a functional derivative, not a new time evolution.

The zero-shift limit is checked against the unchanged action. Reference and both MTS candidates receive identical checks. The Gram derivative is checked separately so its much smaller scale is not hidden by dust or wave work.

## Matched numerical result

The direct shift current and the separately saved localized energy current agree on all three branches. At order12:

| Branch | Maximum current difference, archived tangent | Maximum current difference, action tangent | Horizontal mass-current residual |
| --- | ---: | ---: | ---: |
| Reference | 3.27294e-18 | 3.36103e-18 | 1.42327883e-12 |
| MTS primary | 1.91091e-18 | 1.30104e-18 | 1.42033044e-12 |
| MTS alternative | 2.56820e-18 | 2.87314e-18 | 1.42033039e-12 |

These are the inherited internal energy/current units, not SI error bars or observational prediction accuracy. Across all cases, the independent current/projection identity differs by at most2.711e-19; the per-layer Noether check differs by at most1.091e-18; the order8/12 current change is below4.337e-19. All27 current/Noether/quadrature comparisons pass. The unchanged mass-current offset is the same approximately1.4e-12 offset isolated earlier, not a new fitted subtraction.

For the fixed-background action acceleration, localized cut Euler work is at most3.357e-18. For the archived tangent it is about3.02e-14, but the Hessian-projected residual P_R matches it closely. Thus their difference, not an unsupported assumption that both vanish, explains the current agreement. The source-free cut restriction and the archived-background nature of these tests remain explicit.

### The failed coarse probe and its resolution

The main run has102/108 passing comparisons, not108/108. Its six failures are the separately checked MTS Gram derivative at the constant-connection profile, at the coarse step pair .001/.0005. The original failing results are preserved unchanged.

The fresh refinement run uses the same action, states and raw first variation, halving the step down to .00003125. In every failing MTS case, the first two successive Richardson-error ratios lie between15.999956 and15.999992, matching the derived fourth-order truncation term. The finest Gram error is at most1.189e-19, versus coarse errors up to7.768e-15, and passes the ORIGINAL tolerance. Its39/39 checks pass:27 finest sector checks plus12 convergence-ratio checks. The reference is included unchanged and has identically zero Gram contribution.

The explanation follows the analytic expansion, not a tolerance adjustment:

    D_h=s_1+s_3*h^2+s_5*h^4+O(h^6),
    Richardson(D_h,D_(h/2))=s_1-s_5*h^4/4+O(h^6).

This resolves the finite-difference derivative at the finer steps while leaving the original coarse gate false. The finite raw-variation tests that already passed are not replaced or omitted. See `DERIVATION-20260921-horizontal-shift-step-size-refinement.md` and the separate refinement evidence.

## Scope and why this is useful

Agreement here establishes compatibility between the energy-current construction and the metric response of this specific inherited horizontal extension on the tested candidate states. The extension was explicitly chosen earlier; a diagonal action alone does not uniquely determine it. Finite quadrature agreement is not a proof of uniqueness, arbitrary-coordinate covariance or an entire family of trajectories.

Nevertheless, this is a concrete step beyond naming an energy-conserving current: the relevant metric deformation now has an actual action, an explicit first variation and a finite nonzero-deformation test. There is no newly fitted current or boundary adjustment.

## The next equation toward the spherical GR system

The next distinct task is the radial stress/force balance, not another repetition of the temporal-current comparison. Restore enough radial/areal-radius metric variation to derive the transverse pressure from the action, then test its radial Ward equation, including the source region and moving interfaces.

For the polar metric ds^2=-N^2 dt^2+dr^2/F+r^2 dOmega^2, let T^t_t=-rho, T^r_r=p_r, T^theta_theta=p_perp and K=T^t_r. Symmetry gives T^r_t=-N^2*F*K. Direct Christoffel contraction yields

    D_r = nabla_mu T^mu_r
        = K_t+(N_t/N-F_t/(2F))*K
          +(p_r)_r+(rho+p_r)*N_r/N+2*(p_r-p_perp)/r.

This expression is independently checked symbolically in the sealer. If S^mu_nu=G^mu_nu-g_E*T^mu_nu has only its equal angular components A left, then nabla_mu S^mu_r=-2*A/r. The contracted Bianchi identity therefore gives

    A=(g_E*r/2)*D_r.

In the inherited normalization mu_r=kappa*r^2*rho, g_E=2*kappa, so A=kappa*r*D_r. This is a conditional angular-closure implication once the other Einstein components hold, not a definition of p_perp. Deriving p_perp independently and checking D_r is the constructive next test; assigning p_perp to force D_r=0 would be circular.

## Evidence

- `DERIVATION-20260921-candidate-horizontal-shift-and-localized-current.md`
- `DERIVATION-20260918-moving-P2-current-and-live-evolution.md`
- `scripts/annular_candidate_horizontal_shift_20260921.py`
- `scripts/run_annular_candidate_horizontal_shift_20260921.py`
- `scripts/seal_annular_candidate_horizontal_shift_20260921.py`
- `source-intake/navier-stokes/20260914/annular-candidate-horizontal-shift-attempt01/status.json`
- `source-intake/navier-stokes/20260914/annular-horizontal-shift-step-scan-attempt01/status.json`
- `scripts/annular_horizontal_shift_step_scan_20260921.py`
- `scripts/run_annular_horizontal_shift_step_scan_20260921.py`
- Parent: `source-intake/navier-stokes/20260914/annular-moving-Legendre-current-final-integrity.json`

Main numerical run:1835.772seconds,104 implementation checks, six completed branch/order cases,3,840 material samples. Step scan:35.720seconds,65 implementation checks. Both workers exited successfully. The independent seal `source-intake/navier-stokes/20260914/annular-candidate-horizontal-shift-final-integrity.json`, once COMPLETE, is authoritative for its validation count, rehashed lineage, CSV tables and the protected-workbench check. Its original `comparisons_passed` flag remains false to preserve the six coarse failures; current agreement and refined derivative qualification have separate flags.

Only this private workbench branch is touched. No GitHub, subagents, discarded modes or changes to the protected formalization-workbench. Executed scripts and completed evidence remain immutable; the live resume is the mutable bookmark.
