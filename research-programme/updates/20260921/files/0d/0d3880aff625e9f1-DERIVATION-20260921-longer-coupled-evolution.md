# Longer coupled evolution with complete energy accounting

Private continuation of `DERIVATION-20260921-endpoint-Hamiltonian-and-boundary-energy.md`.

Status: COMPLETE comparison at both horizons. The 10x pilot passes its declared acceptance gates. The 100x runs complete across all branches, pass energy, finer-quadrature and reversal checks, but fail four declared field time-refinement ratio gates. Those failures remain explicit and determine the next calculation.

## Aim and fixed comparison

Move from the inherited interval 1e-7 to 1e-6, then 1e-5 if the first stage passes. These are inherited coordinate-time units, not assigned seconds. This changes the actual evolved state, rather than rechecking static initial data. Reference, primary MTS and alternative MTS receive identical horizons and one/two/four-step comparisons. The larger horizon also receives finer action quadrature and an independently perturbed-seed reversal.

All 16,425 coordinates and momenta remain active. The common-space field is not projected onto the native mesh. Gravity is re-solved at each nonlinear trial. The fixed saved mass is a preconditioner, not the physical evolution law. No coupling, initial state, force definition or scientific tolerance is fitted to make this longer test succeed.

## Equations and numerical gates

At a trial velocity v, q_mid=q_initial+h*v/2 and

    R(v) = P(q_mid,v) - p_initial - h F(q_mid,v)/2.

The accepted step updates q_final=q_initial+h*v and p_final=p_initial+h*F. P and F come from the same reference/material action with current solved radial gravity. Endpoint velocity is recovered separately from P(q_final,v_final)=p_final; midpoint velocity is not substituted into the endpoint energy.

The full velocity Jacobian, including the implicit solved-metric dependence in its partial derivatives, is

    dR/dv = P_v + (h/2)(P_q-F_v) - (h^2/4) F_q.

For the special linear mechanical example P=Mv and F=-Kq, this becomes M+h^2*K/4. A mass-only fixed-point iteration then has error map -h^2*M^(-1)*K/4. This explains why an implicit time-discretization can remain well defined while a simple mass-preconditioned iteration ceases to converge at larger steps: solver convergence is a separate question from physical instability. This special-example identity is not a measurement of the actual nonlinear spectrum.

Unchanged nonlinear acceptance gates are relative momentum residual <5e-12, maximum preconditioned rate correction <2e-12, radial residual <2e-12, F>0 and a timelike source clock. Position/momentum increments retain the preceding Decimal implementation and prepared common-state derivative atoms; metric solves remain binary64.

For each field/source coordinate/momentum block, the finer step difference must be below 0.002 times its measured change plus the inherited diagnostic floor. It must also be no greater than 0.4 times the coarser difference plus twice that floor. An apparent order below the floor is not labelled resolved.

The complete energy is computed as p dot v minus the matter action and gravitational bulk, plus the retained outer boundary increment. Both the direct Legendre calculation and the boundary-mass identity remain visible. Energy acceptance uses the preceding 1e-9 relative smoke gate; numerical resolution and temporal convergence are reported separately. Finer quadrature preserves initial physical positions/rates while recalculating momenta, so comparisons use impulses rather than unequal initial canonical momenta.

## Results

### Numerical solver repair at the larger step

The T=1e-6 experiment completed across all branches with 21 accepted steps, 9 endpoint inverses and 97 evaluations. All 74 implementation checks and the equal-branch temporal/energy gates passed.

The first T=1e-5 attempt stopped before accepting its reference step: successive relative residuals were 3.741e-4, 5.149e-8 and 4.293e-7. The third trial grew by a factor of about 8.34, so the inherited noncontracting-iteration guard fired. This is an observed root-finder failure, not an accepted divergent physical trajectory. Its executed script, status and last-trial state remain in `source-intake/navier-stokes/20260914/annular-candidate-longer-1e-5-attempt01/status.json`.

The replacement retains the same nonlinear residual and both stopping gates, but uses residual-minimizing history acceleration. At each trial let z=M_saved^(-1) R and g=v-z. Coefficients minimize the weighted residual combination R_current+sum alpha_i(R_i-R_current), using weights from the same preconditioner scaling. The next trial is g_current+sum alpha_i(g_i-g_current). At most 12 past trial vectors enter this small least-squares problem. Removing numerically redundant HISTORY directions is not removing physical field modes: the candidate state and every acceptance residual still contain all 16,425 components.

History least squares uses relative singular-value cutoff 1e-12. A coefficient 1-norm above 1e6 triggers an explicitly recorded damped proposal; nonfinite proposals or residual growth beyond the declared large safety bound stop the solve. At most 40 full trials are allowed. This permits intermediate residual growth while still requiring the original final residual/correction criteria. No physical coefficient, force term, state component, integration step or scientific tolerance changes.

Before retrying the actual model, an independent four-component stiff linear mechanical control checks the accelerated solver against a direct analytic inverse, quadratic midpoint energy and an independently seeded reversal. The old iteration rejects that stiff control, while all four accelerated-control checks pass. Source: `scripts/check_annular_anderson_midpoint_20260921.py`; evidence: `source-intake/navier-stokes/20260914/annular-candidate-accelerated-midpoint-control-attempt01/status.json`. The direct rate error is 1.25e-15, energy error 4.00e-14 and reversal error 4.17e-14; forward/reverse each take five trials. This test qualifies the numerical mechanism; the actual nonlinear model must still meet all its own gates.

The 12-vector implementation then accepted all seven reference forward steps, all their endpoint energies, and the finer-quadrature forward step. The coarsest and fine-quadrature steps each took 33 trials. The strongly perturbed reverse did not meet both stopping gates in its 40-trial allowance, ending at residual 2.665e-10 and rate correction 4.242e-9. Its accepted work and failed reverse remain intact in `source-intake/navier-stokes/20260914/annular-candidate-longer-1e-5-attempt02/status.json`.

The next version expands history to 40 vectors and the allowance to 96 trials; all tolerances, perturbations and equations remain unchanged. The independent linear control is repeated in `source-intake/navier-stokes/20260914/annular-candidate-accelerated-midpoint-control-attempt02/status.json`. A hash-checked resume reuses the eight accepted steps and four endpoint inverses, verifying their exact starting states, instead of wasting them. The reverse restarts from its saved failed trial, retaining the original independent seed and earlier iteration history as source evidence. Restart iterations are counted separately, not mislabelled as a fresh unperturbed reverse. Subsequent branches use the expanded-history solver.

That run reached its declared 7,400-second safe wall boundary during the last alternative reverse, with all 26 preceding steps and all 12 endpoint energies saved. The last recorded reverse trial had residual 1.522e-12 and correction 1.331e-11; it was not accepted on the residual alone. A final same-solver continuation hash-reuses those 26 steps and 12 energies and resumes only this unfinished control. The wall stop is preserved in `source-intake/navier-stokes/20260914/annular-candidate-longer-1e-5-attempt03/status.json`; it is a resource-boundary exit, not an observed physical instability or a relaxed gate.

### Forward and energy comparisons

At T=1e-6, all 12 state-refinement acceptance checks pass. The largest finer-grid difference is 4.002e-8 of its measured block increment; the largest relative energy drift is 6.010e-16. The formal order diagnostic is floor-limited, so passing this pilot's acceptance bounds is not a resolved order measurement.

At T=1e-5 all nine forward endpoint energies and all three finer-quadrature endpoint energies pass the same smoke gate. Maximum relative drift is 4.054e-16. Energy differences and energy step-refinement comparisons remain below the paired diagnostic scale of about 1.191e-15 absolute; ratios formed from those tiny differences do not rank the branches' conservation properties.

The larger-horizon field refinement is a different result:

| Branch | Field position ratio | Field momentum ratio | Declared field ratio gate |
| --- | ---: | ---: | --- |
| Reference | 0.51460 | 0.60784 | Both fail |
| MTS primary | 0.38965 | 0.68123 | Position passes; momentum fails |
| MTS alternative | 0.38674 | 0.69060 | Position passes; momentum fails |

The ratios compare the two-to-four-step difference with the one-to-two-step difference. These field differences are above the declared diagnostic floors. Four of the six field ratio checks fail the unchanged 0.4-plus-floor gate, although all absolute/signal-relative error bounds pass. The largest finer-grid difference is only 1.847e-6 of the measured block increment. All six source-block acceptance checks pass, but their order estimates remain floor-limited. We therefore retain `trajectories_qualified=false` for the larger-horizon convergence test; an overall energy pass must not overwrite these field results. The reference is subjected to exactly the same rejection rule as MTS.

### Completed controls and saved results

All 12 finer-quadrature comparisons and all 12 independently seeded reversal comparisons pass at T=1e-5. The largest quadrature-induced increment difference is 3.257e-7 of its measured increment. The largest reversal error is 6.796e-18 in the respective inherited state-coordinate units; this is not a claim of a common SI physical error across position and momentum channels.

The two horizons contain 48 distinct accepted steps and 21 endpoint-energy evaluations. Maximum accepted midpoint relative residual is 2.254e-12, maximum preconditioned rate correction 1.890e-12, and radial residual 5.638e-17. Maximum endpoint inverse relative residual is 2.680e-12 with correction 3.284e-13. Throughout these accepted states, F>=0.7302515 and the local source speed ratio is below 0.03911580. Every physical component remains present.

The last continuation completes in 183.33 seconds, with nine new reverse trials; it reuses 26 prior steps and all 12 larger-horizon endpoint energies. Total independent reverse evaluation chains are 40+14 for reference, 54 for primary, and 53+9 for alternative, including reevaluation of resumed last-trial states. The last continuation's nine evaluations must not be presented as the computational cost of the whole larger-horizon experiment. The smaller-horizon run has 74 implementation checks; the final resume has 142 checks, including input hashes and exact state-reuse checks. Earlier numerical runs remain separately recorded.

Three interrupted numerical executions are retained: mass-only noncontraction, the first accelerated reverse's iteration cap, and the later safe wall boundary. No accepted work is deleted. The first postflight reconstructed all 48 steps and 21 energies and passed its 195 checks, then failed exporting a scalar energy column because its CSV formatter expected a nested energy dictionary. A fresh v2 sealer distinguishes scalar and nested energy records, preserves that failed export and its existing tables, and reruns the independent checks. The final trail therefore retains 61 failed/interrupted executions, including the inherited 57. This CSV export repair changes no numerical result or scientific gate.

## Why energy and trajectory refinement can disagree

For a linear conservative oscillator, write y_dot=A*y, with A^T*G+G*A=0 for the positive energy metric G. The implicit-midpoint map is C=(I-h*A/2)^(-1)(I+h*A/2). Multiplying out the two sides of A^T*G+G*A=0 gives C^T*G*C=G: the quadratic energy is preserved. But for an eigenvalue i*omega,

    C_eigenvalue = (1+i*omega*h/2)/(1-i*omega*h/2),
    omega_numerical = (2/h)*arctan(omega*h/2)
                    = omega - omega^3*h^2/12 + O(h^4).

Thus exact oscillator energy is compatible with phase error. The usual quartering of temporal error under step halving requires reaching the small-omega*h regime; it is not guaranteed for a coarse step across a stiff component. This is an exact diagnostic example, not a fitted frequency estimate or a proof that phase dispersion is the sole cause of the measured field ratios. It motivates holding the full physical horizon fixed and adding smaller time steps, rather than altering the theory to cure a numerical ratio.

## Reproduction and integrity

Runner: `scripts/run_annular_candidate_longer_evolution_20260921.py`.
Larger-step retry: `scripts/run_annular_candidate_longer_evolution_v2_20260921.py`, with `scripts/annular_candidate_anderson_midpoint_20260921.py`.
Resumed run: `scripts/run_annular_candidate_longer_evolution_v3_20260921.py`, with `scripts/annular_candidate_anderson_midpoint_v2_20260921.py`.
Final wall-boundary continuation: `scripts/run_annular_candidate_longer_evolution_v4_20260921.py`.
Independent state/energy reconstruction and integrity seal: `scripts/seal_annular_candidate_longer_evolution_20260921.py`.
Corrected final exporter/sealer: `scripts/seal_annular_candidate_longer_evolution_v2_20260921.py`.

Completed smaller-horizon evidence: `source-intake/navier-stokes/20260914/annular-candidate-longer-1e-6-attempt01/status.json`.
Completed larger-horizon evidence: `source-intake/navier-stokes/20260914/annular-candidate-longer-1e-5-attempt04/status.json`.
Final integrity manifest: `source-intake/navier-stokes/20260914/annular-candidate-longer-evolution-v2-final-integrity.json`.

Every accepted step and recovered endpoint is saved. The postflight reconstructs full discrete updates, midpoint and endpoint momentum residuals, energy sums, temporal refinement, finer-quadrature impulses and reversal errors from those saved arrays. Previous source hashes and all failed executions are retained. Work stays private in post-checkpoint-work; no GitHub or sibling-workbench changes.

## Decision

The substantive gain is actual coupled source/field/gravity evolution at 10x and 100x the original interval, with explicit solver stiffness isolated and complete energy retained. The next target is the remaining temporal field-resolution gap, not a new physical assumption or a looser acceptance threshold.

Keep T=1e-5 and add eight- and sixteen-step grids for all three branches, reusing the already saved two/four-step endpoints. Evaluate the two/four/eight and four/eight/sixteen ratios, with the same endpoint-energy accounting and a finer-quadrature comparison at the newly selected fine grid. This tests whether the observed field ratios approach their asymptotic regime and whether quadrature becomes the dominant error instead. Do not infer a phase-only explanation until these comparisons support it. Keep the inherited annular/zero-shift scope and original physical-force/spatial discrepancies separate from this numerical evolution advance.
