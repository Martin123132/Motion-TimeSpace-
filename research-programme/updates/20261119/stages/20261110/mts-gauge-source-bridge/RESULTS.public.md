> Public reading copy. Machine-specific or private operational passages are omitted; original and public SHA-256 values are recorded separately.

# Live mixed-gauge scalar source bridge — 10 November 2026

## What changed physically and what did not

The canonical heavy scalar now evolves as four independent real coordinates
alongside the retained 91 other hierarchy coordinates. Its current density
and momentum determine the metric and feed the other species, rather than
being driven by supplied future perturbation histories. The freely evolving
fast component is retained. This is a 95-state conditional short-window
calculation, not merely a modified averaged-fluid pressure coefficient.

The synchronous-rest / Newtonian-heavy clock transformation was derived
first and checked with a native-equivalent two-coordinate heavy control.
Only heavy enthalpy enters the mixed-gauge denominator; using total enthalpy
with untransformed synchronous rest sources would double-count their gauge
response. Seven exact identities pass. See DERIVATION.md and proof.json.

Original equations, matching parameters, background, physical frequency,
source bank, grids and tolerance remain fixed. The window is the retained
z=10, Delta ln a=.001, k=5/Mpc test. Original late radiation-streaming
approximations remain in force. No new observational data or galaxy state
selection enters this calculation.

## Numerical controls and independent evolution

The gate remains 2e-5 in the saved component-scaled state norm; values below
are not percentage errors on every observable or observational fit scores.

| Calculation | Internal steps | Difference from saved native fine DOP853 state |
| --- | ---: | ---: |
| Native-equivalent heavy bridge | 32 | 1.6307009553e-6 |
| Native-equivalent heavy bridge | 64 | 8.6965350425e-7 |
| Unchanged cold control | 32 | 1.6593248428e-6 |
| Unchanged cold control | 64 | 1.0350693989e-7 |

Heavy/cold 64-versus-32 differences are 1.5291746355e-6 and
1.5558179029e-6. All five sampled all-state transformed-RHS comparisons
pass 1e-10; their largest normalized residual is 2.7394864072e-16.

The new unrestricted canonical calculation used 64, 128 and 256 internal
commutator-free exponential steps. Its successive 95-state differences are
4.9397349357e-6 and 1.9744038577e-7: the finer check passes the unchanged
gate and shrinks. No measured universal convergence order is inferred from
this oscillatory test. Source/state snapshots are in canonical-*.npz;
final_sources are [physical density/Rh, Newtonian current/Rh, pressure/Rh,
Phi, Psi]. Normalizations are frozen from the initial state and initial
operator, not chosen from the final differences.

The final reconstructed 93-state difference from the retained fluid is
8.6958774666e-7. This is a model-comparison difference, not an estimate of
canonical integration error. It is also comparable to the native-equivalent
bridge's numerical discrepancy, so it is not a resolved physical signal or
evidence of superiority. Cold remains the unchanged paired numerical
control, not a newly assigned scalar model.

## Preparation and background qualifications

Initial physical density/current and all rest states are retained. The
extra scalar coordinates use conditional D0 preparation with the *initial*
native metric derivative; subsequent metric and species perturbations are
live. It is not a derived galactic formation state. The higher-order D01
preparation has not yet been tested in this new coupled system.

The W2 ensemble energy is normalized to the retained cosmological weight
on the initial slice. At 898 evaluated coefficient points, the largest
absolute discrepancies from the native background are 6.662e-16 in H,
9.993e-16 in carried energy and 1.333e-15 in enthalpy. These are sampled
floating-point diagnostics, not exact equalities or uniform bounds. The
carrier/sideband residuals are nonzero, about -2.03e-24 in inverse-Mpc
squared, and must enter the existing constraint-defect accounting.

Future metric interpolation tables were emptied in the canonical object;
the coefficients use only retained homogeneous-background data and its
equations. The current RHS forms the metric from current coupled states.
The saved historical future native state is read only for comparison after
evolution, not as forcing.

## Failures, preservation and handoff

The initial 8/16/32-step equivalent test was not accepted. Its coarse
integration differences failed the original gate. INTEGRATOR-REFINEMENT.md
retains this record; that first attempt did not save arrays before raising.
The refined checker saves progress before acceptance. No tolerance or
physical law was changed to pass. The previous stage's full-span historical
archive mismatch also remains unresolved; its accepted short-window scope
has not been expanded here.

Validation passes 55 implementation/provenance/packet/process checks,
including all 745 inherited hashes, independently recomputed stored error
metrics and unchanged initial physical sources. These counts are not 55
physical discoveries. All numerical workers have ended; final cleanup is
recorded separately after sealing. No GitHub or Galaxy files changed.

[Operational or machine-specific passage omitted from public reading copy.]

Next: use this live system to derive its own initial forced preparation
and evaluate the already-derived conservation/metric-defect law; see NEXT.md.
