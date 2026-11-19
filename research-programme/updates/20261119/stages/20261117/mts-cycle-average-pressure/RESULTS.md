# Complete-cycle pressure test and a matched auxiliary density

Private local calculation, 17 November 2026. Uses the accepted3038..3039 coupled
histories only. No native evolution, mass/coupling fit, altered bank/grid/tolerance,
publication or galaxy fit.

## What was frozen before testing

The first and last positive-going zeros of the coherent homogeneous heavy field
select tau=89.93623115134311 to90.48754073353619, three complete background cycles.
No perturbation, pressure or fit score selected the endpoints. Both original and
coherent MTS branches use the identical window. Baseline support includes it.
The original full89.88473904123015..90.54488392761013 interval is retained as control.

All six32/64-step, stride1/2/4 background reconstructions give the same crossing
topology. Maximum endpoint spreads are5.7294e-10 and2.02515e-9 in retained conformal
time units. These are numerical comparisons, not rigorous continuum root bounds.
The exact window, source hashes and pre-test UTC are in window-frozen.json.

## Derived law, including the term an averaged closure omits

With mu2=a^2 m^2, D=Vg+mu2 Phi f, P=Vg-mu2 Phi f and J=Vf+Phi g,

    c_v = k^2/(4a^2m^2+k^2), s=1-c_v,
    P = c_v D + s[J'+2HJ+k Phi V z-Gf-Fg]/2.

The coefficient follows algebraically from the retained field equations. It is
not fitted; the remainder is not presumed negligible. DERIVATION.md gives the
weighted integral and a separate unforced constant-coefficient analytic control.

The leading k^2/(4a^2m^2) and free-carrier k^2/(sqrt(a^2m^2+k^2)+am)^2 laws were
also frozen before evaluation. The latter assumes an unforced constant-coefficient
carrier projection and is not silently applied as an exact cosmological law.

## Independent saved-work comparison

Reference is I=integral H beta P dt, beta=a/rho0, reconstructed from the separately
integrated saved pressure-work accumulator, -Delta(work_pressure)/3. At new phase
endpoints only, the reference uses saved-work Hermite interpolation with derivatives
from the field equations. Its interpolation variation is explicitly included.

The exact resummed identity passes the unchanged2e-5 numerical gate against the
original934 heavy density-source norm0.04756215632133064. Maximum prefix residual
plus quadrature, interpolation,32/64-step, endpoint-root and rounding estimates:

| Branch | Full original interval | Three-cycle interval |
|---|---:|---:|
| Original MTS representation |3.72046e-7|3.80301e-7|
| Coherent MTS background |3.98839e-7|4.07791e-7|

These estimates include coarsening the endpoint/current and independent-work
representations; they are not directly the same uncertainty budget as the preceding
stage's original-node identity. Sampling differences shrink under refinement.
Direct primitive-pressure quadrature independently passes against saved work too.
All working estimates remain conditional numerical evidence, not rigorous ODE error
enclosures. The earlier independent-native discrepancy has not been eliminated by
this paired-history calculation.

Coherent three-cycle final pressure-work accounting, in retained normalized units:

| Contribution | Integral |
|---|---:|
| Independently saved pressure work | -4.10140674215e-6 |
| Derived density/gradient coefficient | -1.60101964698e-6 |
| Retained endpoint difference | -2.59848190607e-6 |
| Expansion and changing coefficient | +9.76537603831e-8 |
| Metric forcing | +4.42491222613e-10 |
| Representation contacts |0|
| Sum of derived terms | -4.10140530145e-6 |

The tiny difference between the last and first rows is covered by the retained
working numerical budget. The coefficient term accounts for roughly39% of the
signed integral; the endpoint is about63%, partly offset by expansion. Those are
shares of this finite perturbation-work calculation, not cosmological energy
fractions or an observational equation of state.

## What the complete cycles settle

Completing three homogeneous cycles does not make the perturbation state return.
The coherent field Phi is zero at both frozen endpoints, but J changes from
1.44911916819e-6 to1.40210764099e-6. Accordingly H beta s J/2 changes from
8.42185800904e-5 to8.16200981843e-5. Dropping that difference is not justified.

Final-window approximation residual plus allowance, divided by the SAME density norm:

| Approximation | Original MTS | Coherent MTS | Gate2e-5 |
|---|---:|---:|---|
| Zero pressure |8.62677e-5|8.62680e-5|FAIL|
| Leading gradient only |5.24259e-5|5.24267e-5|FAIL|
| Resummed coefficient only |5.26059e-5|5.26067e-5|FAIL|
| Free-carrier coefficient only |5.27830e-5|5.27838e-5|FAIL|

These final-window tests are distinct from prefix tests, since a partial prefix is
not a complete cycle. All outcomes are retained in science-score.json. Density
exchange contains -3I, so a pressure-work omission creates three times its residual
in that contribution; do not quote these I-based tests as a relaxed density gate.
The full non-cycle interval rejects those omissions as well. This is a failure
of an uncorrected averaging approximation, not a failed fitted MTS sky prediction.

H/(am) is approximately3.7e-4 and k/(am) approximately0.146 in this window.
Slow expansion alone therefore does not license discarding finite-window phase
information. The coefficient varies around0.0053; no sound speed was estimated
from the signed final P/D ratio.

Omission budgets for metric forcing are borderline at some prefixes once numerical
allowances are included. That is a failure to certify the omission, not a robust
measurement of a separately resolved metric signal. Keep the exact term.

## Constructive next variable, not an imposed closure

MATCHED-DENSITY.md derives d_star=d+3B, where d=beta D and B=H beta s J/2.
It carries the pressure's total-derivative piece without discarding it. Its equation
follows from the existing exchange identity with all expansion/metric/contact
terms retained. Initial d_star must include3B(initial); recover physical d by
subtracting3B(final). The phase/current still has to evolve: this is not a new
one-variable fluid law. Algebra and saved-quadrature replay are checked separately;
no live evolution of this transformed system is claimed here.

## Shared controls and retained limitations

Both baseline and MTS primitive pressures, currents, Hubble derivatives and endpoint
field equations are rechecked at32/64 settings. The baseline's owned cold component
has exactly zero pressure; it has no heavy oscillator to cycle-average.

The four preceding slow-scalar self-normalized cancellation failures remain
failures. Their separately derived conditional whole-span stress bounds cover this
subinterval (baseline<=3.05e-29 and MTS<=1.47e-28 of their separately frozen ORIGINAL934
system-density norms). These are not substituted passing norms for those failures,
and say nothing about the slow scalar at much later epochs.

185 main technical checks and77 additional matching/replay checks pass; the latter
are retained in matching-verification.json. The checks do not promote the rejected approximate
closures. Original histories, previous stage seals and frozen inputs are unchanged.
See cleanup.json and closeout.json for process exit receipts and artifact hashes.
