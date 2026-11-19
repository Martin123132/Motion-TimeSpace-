# Formation starting-state packet: results, 2026-11-10

## What advances

The saved cosmological histories now supply an explicit, paired starting-state
interface, rather than only a request for an unspecified galactic occupation.
No new cosmological evolution, galaxy fit, mass adjustment or coupling was used.
This does not choose the realized formation history or the population of a named
galaxy: the preceding transport functional still has to be evolved with that history.

- Early real-field stage: 1197 heavy rows (399 modes at three epochs), plus the
  existing 12 early cold comparison rows. Canonical field/momentum, physical
  density/pressure/current and normal/anomalous classical covariance are preserved.
- Later averaged stage: 1995 rows for each model (399 modes at five epochs),
  plus a paired comparison packet. This later cold bank is complete over the
  same main band; it is not limited to the older four-mode example.
- All 5199 physical rows reproduce their original saved raw observations.
  The paired and volume packets are transformations of these rows, not more data.
- Added the hypersurface-volume correction to coordinate-number preparation:
  delta_number,coordinate=delta_N-3Phi. It applies to both MTS and cold.
  Read VOLUME-MEASURE.md; the original flat-measure phase coordinate is preserved
  separately, not silently relabelled as a fully canonical wave.

The exact early canonical map includes the spatial-volume term in momentum.
Its inverse remains regular when the homogeneous field or velocity crosses zero.
Native scalar source reconstruction is accurate to 7.54e-16 in the independent
60-digit check, normalized by the declared source scale.

## Which slice can support the next controlled comparison?

The frozen overlap diagnostics are the exact local leading-frequency truncation
and the dimensional subhorizon estimate, each below 2e-5. They are screens, not
a theorem controlling accumulated evolution or all relativistic corrections.

| Scale factor | Modes per model | Common scale-screen modes | k range, inverse Mpc | Screened heavy pressure-relative checks <=2e-5 |
|---|---:|---:|---|---:|
| .0003 | 399 | 0 | none | 0/0, unavailable |
| .0005 | 399 | 0 | none | 0/0, unavailable |
| .001 | 399 | 5 | 1.03663--1.28640 | 0/5 |
| .003 | 399 | 38 | .572549--3.99542 | 16/38 |
| .01 | 399 | 99 | .2925--5 | 45/99 |

The cold screen uses the same comparison band and reference mass; it does not
assign a scalar mass or quantum-pressure dispersion to classical cold matter.
All other main-band modes are retained as cosmological context, not deleted.

At the predeclared a=.01 (z=99) slice, the largest leading-frequency diagnostic
is 2.78161e-6. The leading NR pressure differs from the retained pressure by at
most 1.63072e-11 relative to the declared density/current source scale. Its
pressure-relative difference in the screened band nevertheless reaches
5.57692e-5, so the stricter relative-pressure comparison does NOT pass all99.
This is precisely why merely matching density and current is not sufficient
to replace the retained stress by an unqualified flat-space wave model.

## Phase and abundance

A trapezoidal diagnostic over the existing finite k band gives density rms
.0243307 and spatial-phase rms59.0481 at a=.01. This is not a converged continuum
variance or a selected realization. The large phase rules out assuming that
1+iS accurately approximates exp(iS) over the whole saved band. It does not
alone imply large velocity or breakdown of weak density perturbations: the
phase gradient and local phase differences, not an overall phase, determine flow.

The retained homogeneous benchmark gives comoving number density
8.164615214198274e32 per cubic metre in coordinates with a_today=1, using the
specified heavy mass and current SI constants. This is a conditional global
normalization, NOT a measured halo number, a parent-derived primordial spectrum,
or an occupation fitted to a rotation curve. The retained A_s=2.1e-9,
n_s=.9653 and positive heavy density constant remain declared inputs.

## Validation and preserved failures

Nine symbolic identities pass. validation-02.json records68209 scalar, row,
hash and coverage checks (not68209 independent experiments). The spatial-measure
sidecar adds5985 inverse/covariance checks, maximum error2.18e-16.
All inputs recorded in result.json retain their hashes.

The original worker stopped on a real numerical conditioning problem in the
exporter, not on a newly failed physical evolution. Evaluating
delta_N+3H u_N/k separately destroys precision for some very long wavelengths.
The identical gauge-invariant combination delta_S+3H u_S/k avoids the
cancellation. All1995 pressure rows then match the saved native pressure to
4.45e-16 with the unchanged1e-10 algebra threshold. No source bank was modified.

A first validator completed its checks but failed while serializing a numpy
integer. Its failed receipt, partial validation.json and original source remain
as failure evidence. Only validation-02.json is an accepted validation artifact.
See REPAIRS.md; no failed attempt is advertised as a successful run.

## Scope and next physical step

The averaged packets intentionally lack exact late fast carrier phase. Their
density/current/pressure do not determine a unique exact relativistic field
microstate. The42 observed columns also omit parts of the native radiation,
polarization and massive-neutrino hierarchy. These exports therefore are not
complete all-species nonlinear restart files.

Next: derive and test a metric-measure- and stress-consistent formation
initialization and short paired evolution on this already declared slice,
preserving phase through an exponential and accounting for the retained
pressure/metric terms. Freeze any realization and environment before examining
galaxy scores. Then the retained population-transport equation can determine
capture for that specified history, rather than importing a Vobs-fitted mass.

No GitHub action, galaxy-file edit, new observational fit or communication loop.
