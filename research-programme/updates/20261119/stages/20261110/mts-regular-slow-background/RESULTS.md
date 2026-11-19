# Regular slow background repaired; native metric residual isolated

Private continuation of the retained MTS action,2026-11-10. This extends
the preceding local repair from the actual original a=1e-9 seed through
a=1; no scalar mass, amplitude, abundance, coupling, likelihood fit or
acceptance tolerance was changed. Original sources and failures are retained.

## What was derived and tested

The integrating factor J=a^2 b' and stable j=J/a^5 yield
delta_b,N=a^3*j/H and j,N=-5j-m_s^2*b/(aH). Evolve the tiny offset and
momentum separately, including their new energy in Friedmann on the saved
non-slow density history. Six symbolic checks pass. A conditional finite-start
regular-seed bound is1.776e-6 relative in j for both retained branches;
DERIVATION.md states the radiation/positive-matter assumptions. This is not
a derivation of primordial amplitude or galactic occupation.

Both cold control and MTS complete six background runs on their original
14001/59873-node tables. Worst step-refinement change is1.006e-12;
source-interpolation change<=2.534e-8, with held-out density error<=5.067e-8.
Independent integrating-factor quadratures agree within7.54e-13.
Present expansion normalization remains within1.72e-12 without refitting.
The MTS slow velocity near matching changes25.1041% from the old numerical
table, while the full background H changes<=5.19e-13. These statements concern
a very small early slow component, not a25% change in the expansion rate.

The accepted background products are cold-candidate-background.npz and
heavy-candidate-background.npz. Retain the stable j/offset run packets too:
the early field increment is not recoverable by subtracting rounded phi.
Native/background acceptance are separate flags, not interchangeable.

## Actual native comparison

The retained native library evolves its full species hierarchy from its
regular perturbation seed for k=1 Mpc^-1 and4253 original requested scales,
using old and candidate tables separately for both models. A pre-existing
double-precision observer avoids the older float32 metric transfer outputs.
No native rebuild, averaging event, new matching selector or state fitting.

Independent canonical replays use the original299-interval matching window,
316 guarded/160 coarse samples and two/four RK4 substeps. They are driven by
the native metric history; they are not independent full-hierarchy solves.
The unchanged componentwise acceptance gate is2e-5.

| Table/readout | Worst canonical replay error | Outcome |
| --- | ---: | --- |
| Cold, old table, double observer |1.163684e-6|pass|
| Cold, repaired table |1.163684e-6|pass|
| MTS, old table |0.195384402|fail retained|
| MTS, repaired table |6.020945e-5|field/current still above gate|

The repaired MTS field error itself is5.948650e-5; only its slow field/current
fail. The other slow readouts and the heavy-field checks pass in this window.
The older float32-driven baseline failure is preserved in the preceding
stage: these new double-precision observations are a separate comparison.

## Remaining discrepancy: tested, not patched

The already derived off-shell gauge ports predict the residual without new
coefficients. The metric-only diagnostic brings the repaired MTS slow-field
disagreement down to3.973e-7; including the background ports gives1.039e-10.
This diagnoses inconsistent supplied histories; adding these diagnostic
ports as extra physical forces is NOT the accepted solution.

Using exact native metric slopes in Hermite interpolation does not shrink
the discrepancy. Native slope identities themselves agree at~1e-14 or better.
Halving and quartering native integration tolerance also leave the MTS
field/current error near6.02e-5, with paired baseline controls. Numerical
quadrature or simple native step refinement has not explained it away.

An integral check, without differentiating noisy histories, gives:

| Identity on saved matching window | Cold relative residual | MTS relative residual |
| --- | ---: | ---: |
| H(t)-H(t0)=integral[-(R+3Pbar)/6]dt |6.739e-16|2.781169e-8|
| alpha(t)-alpha(t0)=integral[Psi-H*alpha]dt |8.850078e-10|6.819628e-8|
| dstar_c(t)-dstar_c(t0)=-integral alpha dt |2.027e-15|6.022e-14|

Four/eight-point quadrature changes<=1.35e-16. The observer/requested clocks
are identical. Small metric-history defects are magnified by cancellation
in the tiny slow-field perturbation. The heavy branch's metric background
also differs from the tabulated H by<=4.019e-8 locally. These are measured
diagnostics, not yet a unique attribution to one native source component.

## Runtime failures and interface boundary

An initial IntTolBoost6->12 attempt failed; the loop stopped before other
planned attempts. Source inspection showed this requests exp(15) tighter
tolerance, not a factor2. The failed receipt remains. Subsequent properly
defined factor2/4 refinements use6+ln(factor)/2.5 and complete. The heavy
factor4 native call reports a Romberg nonconvergence warning despite code0;
it is diagnostic-only and cannot certify full internal numerical convergence.
See ACCURACY-FAILURE-AND-REVISION.md and RUNTIME-NOTES.md.

The existing late full-state capture explicitly rejects tight coupling.
Do not remove that protection to pretend an early restart exists. The
readouts here are physical outputs, not a saved complete native restart.
Full thermal/species initial data and the tight-coupling cache remain the
next interface requirement when an independently recoupled test is attempted.

## Next scientific step

Close the joint background/metric conservation interface on this SAME
short window. Attribute the H/Raychaudhuri defect component by component
using saved cold/heavy histories and native source equations; then repair
the identified representation at its owner, not by adding defect forces.
See NEXT.md for the frozen test. No galaxy population law follows from
this numerical repair. Galaxy Lab's conditional measured baryonic force
remains a separate source input, not a selected MTS halo occupation.
