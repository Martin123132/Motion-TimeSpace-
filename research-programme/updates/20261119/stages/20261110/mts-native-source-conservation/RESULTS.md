# Equation-derived source interpolation closes the paired canonical replay

Private retained-MTS continuation,2026-11-10. No action replacement, parameter
fit, abundance choice, source-grid change or relaxed acceptance threshold.

## Derived source accounting

Differentiating the retained flat Einstein constraints gives

    E_alpha=E_D/(2k^2 H)+3E_Q/(2k^3)-z*E_H/(kH),
    E_H=E_R/(6H).

For each canonical scalar, E_R=vE_b+mu^2*bE_f,
E_D=wE_b+mu^2*uE_f, E_Q=k*uE_b, where E_b and E_f are the actual
background equation defects. Four symbolic identities verify these ports;
two further identities check Friedmann propagation and baryon/photon drag.
The existing baryon pressure approximation contributes separately. No
defect force has been inserted into the action or native evolution.

The first unsplit quadratures were not accurate enough for the tiny
component residual and remain recorded as failed attribution comparisons.
Splitting at the ORIGINAL source knots resolves the cancellation. The heavy
scalar explains the background/Friedmann residual to1.88e-8 of that residual
after separately accounting for scale interpolation. It also predicts the
dominant shear discrepancy, leaving~1.3% unassigned. The baseline shear
residual remains a distinct control, not something blamed on MTS or set zero.

## Source repair, not residual fitting

The old native interface independently interpolated field and velocity
with cubics. The replacement uses endpoint quintics whose first and second
derivatives are fixed by the same Klein-Gordon/Friedmann equations. All45873
heavy field nodes and their stored values remain unchanged. Clock data come
from the native standard-species density and retained scalar stress; the
massive-neutrino pressure used for endpoint slopes is obtained by differentiating
its saved log-density representation. It is a numerical representation,
not a new empirical equation of state. See QUINTIC-REPAIR-CONTRACT.md.

On the same knot-split probe, heavy field/velocity equation defects fall
from~5.8e-6 to~5.1e-9 of their component scales. The energy-equation defect
falls from7.995e-3 to7.318e-6. Changes in field/velocity are<=1.703e-7;
H changes<=4.028e-8. No residual was used to choose coefficients.

## Actual native paired test

An isolated library was compiled with bounds checks. Only MTSTwoField.f90
and its Python method declaration differ from the copied sources. The new
clock/interpolation is opt-in; disabled cold and MTS arrays reproduce the
previous library BYTE-FOR-BYTE. Baseline is unchanged when enabled because
it has no heavy field. Full native species evolution uses the original4253
requested scales, k=1Mpc^-1, parameters and solver settings. No averaging or
matching event occurs in this early branch.

The independent canonical replay uses the original299-interval window,
316 guarded/160 coarse histories and two/four RK4 substeps. Source recovery
uses the actual candidate interpolation, independently implemented in Python.
All recovery identities meet1e-10; numerical gates remain2e-5.

| Case | Worst fine4 canonical error | Result including refinements |
| --- | ---: | --- |
| Cold, original/disabled |1.163684e-6|pass|
| Cold, candidate |1.163684e-6|pass; unchanged|
| MTS, original/disabled cubic |6.020945e-5|fail retained|
| MTS, equation-derived quintic |8.115376e-6|pass|

The MTS slow-field error is8.073997e-6; all targeted field, momentum, density,
pressure, current and canonical stress readouts pass. The test includes step
and driving-history refinement, not only one favourable saved trajectory.
This is a forced canonical replay against a freshly evolved coupled native
history; an independent full-hierarchy recoupling/full-state restart is not
what this particular gate tests. Earlier scalar/background and library
failures remain authoritative records of the old implementations.

## Conservation diagnostic after repair

In the same window the MTS integrated H/Raychaudhuri residual falls from
~2.78e-8 to5.772e-11 relative to H; the shear-history residual falls from
~6.82e-8 to9.186e-9 relative to alpha. The cold H residual is7.081e-16 and
its shear residual8.850e-10. These measured residuals are not claimed zero.
The remaining shear component attribution is incomplete; keep it separate
from the passing canonical numerical gate. Massive-neutrino perturbative
pressure/approximation effects were not invented to close that remainder.

## Preserved execution failures and cleanup

The first enabled native adapter aliased params.DarkEnergy then reassigned
the same allocatable owner. It failed with an access violation. A checker
launched prematurely then failed on the absent candidate result; its three
completed control replays were saved and reused. Both failed receipts remain.
The corrected adapter uses the documented .copy() ownership API and a new
-owned label; it completes. This is a code-ownership fix, not a physical
retune or an identical failed-run retry. See NATIVE-OWNERSHIP-REPAIR.md.

The build compiles39 units serially;137 tracked compiler/helper identities
exit and its temporary drive mapping is removed. No prior/native source,
Galaxy work, public repository or shared service was changed. Build cleanup
was subsequently hardened so a deadline/hold cannot prevent owned-drive
removal; that defensive cleanup path did not alter the completed binary.
Final receipts verify the remaining workers and all saved files.

## Next physical use

Carry the corrected source into the source-complete early-state/matching
interface and test constraint propagation across the handoff, keeping the
coherent state rather than choosing a population to fit galaxies. First use
the already saved neighbouring phase window as a transfer control; do not
repeat these completed runs. The early full-state interface must preserve
the tight-coupling state/cache instead of bypassing the existing guard.
