# Paired early transport completed — 2026-11-08

## Scientific outcome
The original perturbation has now been evolved in the derived mean system over the first approximately0.01 e-fold and compared with the saved original full-equation solution at five original epochs. Both baseline/MTS and GR/spatial-Poisson controls were run at allthree retained wavelengths. No new observational fit, amplitude, bank, hierarchy or tolerance was introduced.

**Baseline:** allten observable channels pass at every retained wavelength and both gravity branches; the worst relative discrepancy is2.879444e-11.

**MTS frozen-density mean approximation:** misses the unchanged2e-5 observable gate. Its largest discrepancy is about3.2e-4 (0.032%), not a failed empirical comparison with observations. This rejects this uncorrected averaged approximation at the requested accuracy, not the underlying saved equations.

| Wavelength | MTS GR maximum | MTS spatial-Poisson maximum |
|---|---:|---:|
| half | 3.206432299384e-4 | 3.206432299386e-4 |
| balanced | 3.197714908594e-4 | 3.197714908590e-4 |
| double | 3.195734806670e-4 | 3.195555817813e-4 |

The largest D discrepancy occurs at probe0 for allsix MTS branches. The mean-background preparation preserves the original encoded perturbation but changes the physical background used to evaluate its stress. Thus the dominant initial density discrepancy exists BEFORE the new evolution; smaller integration steps cannot remove it. The separately propagated initial coordinate mismatch does not remove the entire physical readout discrepancy and was not subtracted to manufacture a pass.

## Numerical repair and checks
A frozen held-out source check first rejected interpolation of the whole matrix. Fine/coarse absolute errors0.1332181/0.2001795 were localized to the retained photon-baryon scattering term. The rest was within2.192e-11/3.291e-11. That failed attempt is preserved.

Derived exact repair:

    Abar = Abar_without_collision + (opacity/H)*<R_phys C_unit>,
    C_unit*S_phys = C_unit.

The opacity comes directly from the ORIGINAL thermal cubic at every solver evaluation. The small induced heavy-row collision term remains. No source smoothing or bank alteration. The identical repair applies to the baseline.

Completed checks:
- 102 even source nodes and96 frozen held-out nodes across both models/three wavelengths; original256 phase nodes retained.
- Maximum repaired source interpolation absolute discrepancy6.005177e-10.
- Propagated source-interpolant refinement <=1.479190e-14 relative; time-step refinement <=6.920047e-12.
- Physical phase step refinement <=1.243450e-13 radians.
- 48 independent closed-collision coefficient identities; maximum absolute residual9.094948e-13.
- Full G192, both initial-state and linear initial-mismatch responses; original rtol2e-12/atol2e-14.
- Five physical output epochs, ten channels and two gravity branches for each model/wavelength; predictions saved before reference comparisons.
- ALGEBRA1e-10/GATE2e-5 unchanged. Numerical validation PASS is kept separate from the MTS approximation verdict above.

## A derived constructive next step
DENSITY-RECONSTRUCTION.md uses the already retained phase invariant to derive

    ln(rho_rec) = ln(rho_bar) + g1(rho_rec,theta) + g2(rho_rec,theta).

The invariant drift Delta_I is not declared zero in the theory; it stays a bounded remainder. The new exact logarithmic derivative is

    partial_ln_rho(g1+g2)
      = (3/4)f*u sin(2theta)
        -(9/8)f*u² cos(2theta)
        -(9/32)f*u² cos(4theta),

with u=H/(a*m_h), f=rho_h/(3H²). Five symbolic identities pass. Positivity plus the saved initial u<0.001 establishes a conservative self-mapping log-density box. The contraction bound is approximately0.0007589723 (safely <0.000759), so there is one positive reconstruction on that box.

Its physical phase-law Lipschitz bound is approximately4.504550832 (safely <4.504551) per e-fold—not of order the rapid frequency mu. The inherited full-background invariant drift bound3.174313e-6 fits the existence box and yields an invariant-only log-density sensitivity bound below3.176725e-6. Slow-state, phase, averaging and solver errors remain separate. Displayed decimals approximate the saved interval calculation; the strict rounded-up caps are given above.

This establishes a constructive mathematical route, not a newly tested corrected transport. The next calculation should freeze the slow invariant, reconstruct rho(theta), and include its density/phase correlation in the source mean and both endpoint maps. Reusing the old frozen-rho primitive unchanged would mix two different coordinate constructions.

## Accepted evidence and reuse
- build_source.py: eachlabel/source-even-01, original source/phase histories and five endpoint primitives.
- split_collision.py: eachlabel/collision-split-01, exact-source decomposition.
- validate_sources_v2.py: eachlabel/source-heldout-02, frozen predictions and independent source checks.
- evolve_mean_v2.py: eachlabel/evolution-02, matched trajectory plus linear initial-mismatch trajectory and refinements.
- predict_outputs_v2.py and compare_reference.py: eachlabel/predictions-01 and comparison-01.
- validate_collision_identity.py: collision-identity/result.json.
- derive_density_reconstruction.py: density-reconstruction-proof/result.json.
- audit_transport_v2.py: audit/result.json, including per-channel maximum-error epoch diagnostics.

Original failed heldout-half-01 code/logs/predictions and its diagnosis remain intact. Original unused draft variants are retained but not accepted evidence. The previous matching stage and all reused parent source seals remain unchanged.

Local-only work completed around03:45Z, well before07:00Z cutoff. All23 task-owned sequential numerical workers exited (22success,1preserved gate failure); no compiler, subagent, app/server, process kill or GitHub action. Final process and artifact receipts are CLEANUP.json and closeout.json.

