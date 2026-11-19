# Phase-aware density actually evolved

Private local stage,17 November2026. Previous goal turn and this turn make verified
progress; the full parent-framework objective remains unfinished. This stage
finishes the preceding matched-density target rather than starting a new theory.

## Derivation and regularity

The retained scalar admits an exact two-variable representation:

    d_star=beta[D+(3Hs/2)J],
    w=beta mu(Vf-Phi g),
    mu=am, s=4mu^2/(4mu^2+k^2), J=Vf+Phi g.

Using J alone as the second variable would introduce singularities at kinetic/
potential equality. The Wronskian difference avoids that: the inverse denominator
is Delta=V^2+mu^2 Phi^2+3Hs Phi V. It remains positive if |3Hs/(2mu)|<1,
with a derived sufficient bound3|H|/(2|k|)<1. Eight symbolic controls verify the
equations, inverse, determinant and positive-square bound. No division by Phi, V,
pressure or density is used, so individual field zero crossings remain regular.

The saved domain has maximum |3Hs/(2mu)| approximately0.000558835. Its sampled
Delta/(V^2+mu^2 Phi^2) remains at least0.999442735; the maximum balanced matrix
condition number is approximately1.000559. The validity condition is checked
throughout RHS evaluations, not merely assumed from the initial point.

DERIVATION.md provides the exact two first-order equations. They retain the
phase-dependent endpoint, expansion, metric forcing and representation contacts.
They are an equivalent representation of the existing two field perturbation
degrees of freedom, not an extra free fluid law or new coupling.

## Actual short evolution

Eight heavy-field integrations cover the original3038..3039 saved interval:
original/coherent backgrounds,32/64 maximum-step controls, and separate1/2/4
source interpolation comparisons. Each integrates the matched variables,
independent primitive f/g, a deliberately mismatched initial state, and the
physical exchange integrals.420 unchanged diagnostic cells provide bounded
checkpoint saves. The previous three-cycle endpoints are additional already-frozen
diagnostic evaluations, not replacement report epochs or fitted windows.

The background and z histories, INCLUDING FUTURE VALUES, are supplied from saved
work. This is a CONDITIONAL REPLAY. It tests the new evolution representation and
matching, not independent prediction of the cosmology or the metric. No native
owner/full-hierarchy integration was launched. A mutation test verifies that
changing future scalar-array entries cannot directly change the replay forcing;
it does NOT remove scalar information already present in the supplied metric.

## Results at unchanged tolerances

Largest physical-source discrepancy plus paired-step, larger interpolation
difference and rounding allowance, relative to the original934 component norm:

| Quantity | Original MTS | Coherent MTS | Gate |
|---|---:|---:|---:|
| Density |3.15963e-8|1.16452e-5|2e-5|
| Current |1.71628e-9|1.08010e-5|2e-5|
| Pressure |3.13854e-9|1.21738e-5|2e-5|
| Independently saved pressure-work integral |6.69382e-12|1.53072e-8|2e-5|
| Reconstructed physical density exchange |2.02316e-13|1.47269e-13|2e-5|

All pass. Physical fields f/g also pass their retained native-unit checks.
Against an independently integrated primitive KG solution with identical forcing,
coordinate-equivalence residuals are at most4.87e-11 of the frozen density norm
in the original branch and3.17e-13 in the coherent branch. The independent matrix
T'+TL calculation agrees with the explicitly implemented matched equations; the
coherent fine run's maximum relative algebra discrepancy is2.70e-16.

The coherent budget is dominated by reconstructing the SAVED background, not by
new-variable integration: interpolation differences shrink under1/2/4 refinement,
but the conservative maximum is retained. Original-branch interpolation differences
are smaller and non-monotonic. Do not claim demonstrated asymptotic convergence
there; the larger observed difference is used. All these are working estimates,
not rigorous global bounds or a replacement for the earlier independent-native
accuracy control. Full-output success does not certify the much smaller coherent-
minus-original repair signal to the same relative precision.

Coherent phase-aware pressure work over the frozen three-cycle window is
-4.10140450479e-6 versus the earlier independent saved-work reference
-4.10140674215e-6, difference2.23736e-12. This retains, rather than hides, the
endpoint contribution that defeated the preceding coefficient-only closures.

## Initial matching is necessary

The coherent initial matched coordinates are approximately
(-0.0449308573361,0.453396990512). Deliberately replacing the first entry by the
undressed density -0.0446852554366 changes the physical initial state. Its errors
then fail the unchanged gate: density0.00521638, current0.000308876 and
pressure0.000520174 in their original component norms. The original branch gives
the same conclusion. No initial condition was tuned after looking at the answer.

## Baseline, contacts and retained boundaries

Twelve cold-CDM replays use its OWN saved metric, both backgrounds and32/64,
stride1/2/4 comparisons. The exact represented-metric antiderivative solves
d'=-k n_c z. Density budget7.81898e-14 passes; owned pressure/current are exactly
zero as required by that retained component. This is an active baseline evolution
control, not a fictional heavy oscillator substituted into the baseline.

The coherent continuous reconstruction is not itself an exact background ODE
solution between stored knots. The code differentiates its actual Hermite
representation and retains F,G,r-H as INTERPOLATION CONTACTS. These are not newly
added parent interactions. Original-background contacts keep their earlier role.
The four prior tiny slow-scalar self-normalized failures and their separate
conditional bounded influence remain unchanged. No late-time slow-sector deletion
or galactic occupation follows from this early-window test.

The older metric documentation mislabeled z and sigma as Mpc^-1. The retained
constraints require them to be dimensionless; eta_k has Mpc^-1. This wording
correction is documented in UNIT-CONVENTION-CLARIFICATION.md without modifying
sealed history or any numerical equation.

## Verification and next physical step

129 technical/replay checks pass, including symbolic replay, exact score replay,
bounded checkpoint consistency, native primitive controls, coordinate equivalence
and direct future-scalar isolation. All actual source/work/exchange budgets pass.
The deliberately unmatched negative controls fail, as recorded, and the previous
coefficient-only pressure approximations remain rejected.

Next connect the phase-aware state to the LIVE common-metric/surrounding equations,
starting at the complete saved3039 state. Do not continue polishing this passing
conditional window. A self-consistent new-epoch test must not read future z or
surrounding sources. Maintain the direct original formulation as an independent
implementation control and preserve separate tiny-correction precision tests.

All work is local.1358 frozen/inherited inputs unchanged; no parameter/bank/grid/
tolerance change, native rebuild, publication, subagent, browser/server, or action
on another chat's processes. Process exits and artifact hashes are in cleanup.json
and closeout.json.
