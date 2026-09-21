# Endpoint Hamiltonian and the retained boundary energy

Private continuation of `DERIVATION-20260921-first-coupled-canonical-midpoint.md`.

Status: COMPLETE endpoint inverse and short-run energy smoke test; all 170 implementation checks pass. The energy drift and its temporal refinement are below the diagnostic numerical floor, so no resolved energy-convergence or conservation claim is made. The algebra below concerns the inherited annular polar, zero-shift candidate. It is not a full-GR theorem or a derivation of Newton's constant.

## 1. A derived energy, not an extra conservation assumption

Write F=1-2 mu/r, N=exp(ell), s=sqrt(N^2-V^2/F). The chart requires F>0 and s>0. A denotes the material average of the squared transported field time derivative; B denotes the material average of the squared physical radial gradient; g is the existing Gram density; sigma is source density; V is source coordinate velocity. All use the same inherited candidate and material maps as the coupled pilot. The reference branch has g=0.

The reduced Lagrangian, with its retained outer-boundary normalization, is

    L_total = L_matter + integral N mu_r/(kappa sqrt(F)) dr - mu_out/kappa.

The inner mass mu_c is fixed; the outer lapse obeys N_out=sqrt(F_out), as in the inherited exterior-time normalization. Neither kappa nor the boundary normalization is newly fitted here. The radial action and inherited boundary conditions are retained, not replaced by an energy chosen after seeing the trajectory. Source definitions are in `scripts/annular_candidate_radial_constraint_20260920.py` and `scripts/annular_candidate_canonical_response_20260920.py`.

At fixed metric, the wave kinetic term is homogeneous quadratic in the joint field/source rates: the material transport term is included. Thus the complete canonical pairing of those rates is twice the wave kinetic term. The velocity-independent spatial and Gram terms change sign in the Legendre transform. For the proper-clock source,

    L_dust = -m_s sigma s,
    p_V V - L_dust = m_s sigma N^2/s.

Consequently the matter Hamiltonian density is

    h_matter = r^2 A/(2 N sqrt(F))
               + N sqrt(F) r^2 (B/2+g)
               + m_s sigma N^2/s.

The already-used mass constraint is

    mu_r = kappa r^2 F [A/(2 N^2 F)+B/2+g]
           + kappa m_s sigma sqrt(F) N/s.

Multiplication by N/(kappa sqrt(F)) gives EXACTLY h_matter. Hence, on this continuum candidate constraint,

    H_total = integral [h_matter-N mu_r/(kappa sqrt(F))] dr + mu_out/kappa
            = mu_out/kappa,
    H_shifted = H_total-mu_c/kappa = (mu_out-mu_c)/kappa.

This identity applies to the reference and both MTS branches because the same wave/Gram/dust action supplies their matter and radial constraint terms. It does not require suppressing the MTS term. Symbolic verification is in `scripts/annular_candidate_hamiltonian_20260921.py`.

The continuum identity is conditional on this action, its stationary radial fields and its inherited boundary conditions. Our separate radial and reference/material quadratures do not turn that continuum cancellation into an exact finite-dimensional variational theorem. At finite radius this is the energy of the adopted boundary-normalized candidate, not a newly proved identification with general asymptotically flat ADM energy.

## 2. A limited Newtonian connection

Define beta=V/(N sqrt(F)). The dust contribution to mu_r/kappa is

    m_s sigma sqrt(F)/sqrt(1-beta^2).

For |mu/r| and beta^2 small, its dimensionless rest-energy factor is

    1 + beta^2/2 - mu/r + O((mu/r)^2, beta^4, (mu/r) beta^2).

This exhibits the familiar rest-plus-kinetic-minus-gravitational-potential energy form in the inherited c=1 normalization. It is a check of compatibility of this dust energy term, not a derivation of G, the complete Newtonian equations of motion, the full MTS matter coupling, or the full GR limit. No SI energy or duration is assigned by this calculation.

For an autonomous, stationary reduced action with time-independent boundary data, the formal identity dH/dt = v dot (p_dot-L_q)-L_t gives conservation on exact Euler-Lagrange solutions. A driven boundary or changing inner mass would add work/flux terms; the present calculation does not cover those cases. Symbolic Noether algebra and a short numerical pilot are not a global existence or stability proof.

## 3. Actual endpoint velocities and independent energy channels

An implicit-midpoint step stores midpoint velocities, not endpoint velocities. At each saved q,p we therefore solve the full relation P(q,v)=p for all 16,425 rates, re-solving radial gravity at every trial. The saved full mass is only a preconditioner. No native-subspace projection, mode removal or frozen-gravity substitution is used. The reference and both MTS branches receive identical checks.

The first implementation attempted to reuse the midpoint map at zero step. Its initial exact state-preservation check correctly failed: even adding Decimal zero under a 64-digit context rounds initial binary64-exact momentum strings with longer decimal expansions. This is a representational failure, not an observed physical drift. The failed execution is preserved in `source-intake/navier-stokes/20260914/annular-candidate-endpoint-energy-attempt01/status.json`. The replacement `scripts/annular_endpoint_legendre_inverse_20260921.py` performs a genuine fixed-q,p inverse with no state arithmetic at all. It does not relax the exact-state gate.

Independent reproduction found 14,926 initial momentum components rounded by at most 5e-70; no coordinate changed. This explains why a physically negligible rounding event still fails an exact state-preservation check.

The v2 run completed all six reference endpoint cases, then failed to serialize a Numpy Boolean in its new refinement diagnostics; its error handler encountered the same issue. Its last status says "running" but its process exited with code 1. No completed result is claimed from it. The fresh v3 runner fixes native scalar serialization without changing scientific gates. Both failed executions are recorded in `source-intake/navier-stokes/20260914/annular-candidate-endpoint-energy-failure-ledger.json` and retained unchanged.

The final runner is `scripts/derive_annular_candidate_endpoint_energy_v3_20260921.py`. It processes, per branch, the initial state and the one/two/four-step endpoints at T=1e-7 inherited coordinate-time units, plus the matched-physical-state initial/final pair from the finer quadrature pilot. This stage adds no new trajectory or longer time interval.

We evaluate the complete shifted Legendre energy independently as

    H_shifted = p_target dot v - L_matter(reference/material)
                - integral N mu_r/(kappa sqrt(F)) dr + B_integral,
    B_integral = integral mu_r dr/kappa,
    B_endpoint = (mu_out-mu_c)/kappa.

B_endpoint independently checks the integrated boundary increment, but subtracting the central mass in binary64 is less accurate for this small increment. Both channels are retained. The full energy, without-boundary energy and without-gravity-bulk energy are recorded separately; omitting either necessary term must be detected. Relative drifts use the shifted energy, never the larger constant central mass to dilute the discrepancy.

The computed-vs-target momentum mismatch contributes (p_target-P_computed) dot v. It is checked against the weighted Cauchy bound ||delta p/s_mass||_2 ||s_mass v||_2, where s_mass is the saved preconditioner scaling. The direct Legendre cancellation defect also measures disagreement between the reference/material and radial quadratures. None of these tests are silently replaced by the symbolic on-shell identity.

## 4. Numerical results and their resolution

All 18 endpoint inverses completed, with 42 joint momentum/force/gravity evaluations. Known initial rates converge in one evaluation; evolved endpoints require three. The final run took 832.86 seconds (13.9 minutes), using one single-core BelowNormal worker. Both earlier implementation failures remain in the evidence trail.

| Check across all branches/endpoints | Observed value |
| --- | ---: |
| Maximum endpoint momentum relative residual | 5.307e-14 |
| Maximum preconditioned velocity correction | 6.492e-15 |
| Maximum radial constraint residual | 5.595e-17 |
| Minimum F | 0.7302515 |
| Maximum local source speed ratio | 0.03911584 |
| Maximum pointwise matter/gravity density relative defect | 4.502e-16 |
| Maximum full Legendre/boundary relative difference | 5.446e-15 |
| Maximum inverse-energy Cauchy bound | 2.502e-18 |
| Largest absolute mixed-quadrature Legendre defect | 1.522e-16 |

Initial shifted energies in inherited units are approximately 0.02794194175036349 (reference) and 0.02794194180154711 (both MTS variants at the displayed precision). These are candidate numerical quantities, not measured physical energies or claims of 17-digit physical accuracy. Primary and alternative agree initially here; this does not make their evolution algebraically identical.

| Branch | One-step absolute energy drift | Largest relative drift over all four comparisons |
| --- | ---: | ---: |
| Reference | 9.410e-18 | 3.368e-16 |
| MTS primary | 3.006e-18 | 3.567e-16 |
| MTS alternative | 3.008e-18 | 3.567e-16 |

All 12 comparisons pass the declared 1e-9 relative smoke gate. However, the paired diagnostic resolution scale is about 1.191e-15 in absolute shifted-energy units, larger than every measured drift. The one/two/four-step energy-difference ratios are 0.5514, 0.1037 and 0.1019 respectively. None qualifies as a resolved temporal order because both numerator and denominator are below the diagnostic floor. The smaller MTS ratios are not evidence that MTS conserves energy better than the reference.

Increasing reference/material quadrature from (10,32) to (16,48), with the same initial physical state and separately recalculated canonical momenta, shifts initial energy by about -9.035e-17. It changes measured drift by -1.273e-20 (reference) and about 6.960e-18 (each MTS variant), also below the floor. Thus these data support a smoke-level consistency result, not resolved spatial/quadrature convergence.

The omission controls expose why the full accounting matters: leaving out the boundary gives an initial energy around -6.2e-17 instead of 0.02794; leaving out the gravitational bulk gives about 0.055875. A near-zero, near-flat result without the boundary would be the wrong Hamiltonian. Endpoint mass subtraction and integrated mass loading agree within approximately 2.1e-16 absolute. On this Windows runtime, both float and long-double epsilon equal 2.220446049250313e-16; long-double is not an independent precision upgrade.

The diagnostic resolution scale is the maximum of 32 binary64 eps times the sum of absolute energy terms, the mixed-quadrature Legendre defect, the endpoint-minus-integral boundary difference and the inverse-energy Cauchy bound. It is a practical diagnostic, NOT a certified bound on all discretization error. A temporal energy difference must exceed four times the comparison scale before its order is described as resolved. The smoke gate is relative drift below 1e-9; passing it alone is not an energy-conservation proof. Accumulating binary64 samples in 64-digit Decimal avoids additional summation cancellation but does not improve the metric's underlying precision. The actual float and long-double machine epsilons are recorded.

## 5. Evidence and next step

Run evidence: `source-intake/navier-stokes/20260914/annular-candidate-endpoint-energy-attempt03/status.json`.
Independent reconstruction and integrity checker: `scripts/seal_annular_candidate_endpoint_energy_20260921.py`.
Final seal: `source-intake/navier-stokes/20260914/annular-candidate-endpoint-energy-final-integrity.json`.

The next substantive calculation is a longer, bounded, checkpointed coupled evolution with equal reference/MTS controls and this complete endpoint-energy accounting. Its interval should be increased cautiously, with step refinement and tighter quadrature if the energy signal remains dominated by numerical resolution. Do not repeat energy audits indefinitely instead of evolving the system; use the audit as an acceptance test on the next actual trajectory.

Still open: physical-force and spatial convergence (including the old 12.5718% impulse, 13.5770% fine/continuum and 32.5535% coarse/fine discrepancies), general shift/current, exact finite-label variational stationarity, long-time/global stability, and the full GR limit. No black-hole crossing, public physics claim or GitHub update is made. All original and executed evidence remains intact; only post-checkpoint work is written.
