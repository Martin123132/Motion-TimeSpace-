# Retained phase action and a derived first-adiabatic parent connection

2026-11-10. This extends the sealed formation-state packet, without replacing
the retained cosmology or galaxy solver.

## Main result

We now have both:
1. A quadratic Hamiltonian generating the retained averaged density/current/
   pressure equations in the supplied Newtonian metric.
2. A microscopic real-field derivation of the first expansion-dependent
   normalization connection in the unforced homogeneous-FLRW limit.

The second step goes beyond reconstructing an action from the equations:
the flat real-field symplectic pullback fixes W=1+r rather than leaving
occupation normalization arbitrary. Expanding the actual field derivative,
stress and current then supplies

    Pi = r delta - (3H r+g) S/mu + higher-adiabatic terms,
    g = H(w-1)/w^2 = -W'/W,
    w=sqrt(1+k^2/mu^2), mu=am.

There is no fitted damping coefficient. The same g independently supplies
the symplectic connection that the naive instantaneous state map required.
The exact action of the stated minimal completion uses canonical momentum
P=W S. Read FIRST-ADIABATIC-CONNECTION.md: its first-order terms are derived;
its particular second-order products are not the entire higher-order parent.

## Retained metric-forced probe

All399 saved modes from EACH model at a=.01 were propagated over Delta ln a=.001.
H, Phi and Psi were held at each row's saved initial value while a evolves.
This is a controlled supplied-background probe, not a new native cosmological
history or a prediction of a self-consistent metric.

| Check | Heavy MTS | Classical cold |
|---|---:|---:|
| Independent fluid/Hamilton discrepancy | 4.69e-16 | 4.42e-16 |
| Source work/energy discrepancy | 3.69e-16 | 3.43e-16 |
| 8-step midpoint error | 1.256e-10 | 3.038e-12 |
| 16-step midpoint error | 3.139e-11 | 7.603e-13 |
| 32-step midpoint error | 7.847e-12 | 1.903e-13 |
| 64-step midpoint error | 1.962e-12 | 4.918e-14 |

Errors use the fixed component/source scales recorded by the scripts.
Midpoint discrepancies shrink approximately by4. Both DOP853 tolerance runs
used14 evaluations and returned the same values: that equality alone is NOT
independent resolution evidence. Midpoint refinement and the separate analytic
cold solution provide independent controls.

The frozen-source Hamiltonian is stable as a matter subsystem for r>0.
This does not establish gravitational collapse stability after metric feedback.

## Parent normalization and real-field comparison

At the saved a=.01 slice:
- maximum W-1 is2.781609665e-6;
- maximum g/H is5.563172907e-6;
- naive instantaneous parent-weight drift over the short probe is5.557613503e-9.

The first adiabatic derivation follows from canonical field and stress
projection, not from inserting a trace-cancelling term. It agrees with an
independent expansion of the full projected WKB source-map generator through
first order. Flat sideband density, pressure, symplectic form and excitation
energy were independently checked at all1995saved heavy mode/epoch pairs.

A separate unforced probe compares the original and derived-completion
equations against the full projected WKB template:

| Quantity at retained H | Maximum normalized discrepancy |
|---|---:|
| Original retained equations versus template | 3.644e-10 |
| First-order completion versus template | 5.677e-9 |
| Original versus first-order completion | 5.481e-9 |

**The new term alone does not improve numerical agreement at the retained
background.** Both discrepancies are small compared with the unchanged2e-5
gate, but that does not authorize calling the new completion a better physical
model or overwriting the retained native closure.

We investigated rather than concealed this ordering. Holding the starting
physical variables and e-fold interval fixed while reducing H by factors
1,1/2,1/4,1/8,1/16 gives completion/template discrepancies

    5.676e-9, 2.840e-9, 1.422e-9, 7.126e-10, 3.574e-10.

The approximately linear decrease is consistent with the omitted
second-adiabatic-order generator integrated over an interval proportional to
1/H. The original comparison is closer at the retained H but does not follow
this decrease. This is a diagnostic family, not a fit or held-out observation.
The post-diagnosis ratio check is a consistency assertion, not a new
predeclared empirical acceptance threshold. Cold analytic controls pass under
all the same H changes, below4.76e-16.

The WKB template itself has a nonzero KG residual: at the actual starting
background its maximum fractional oscillator residual is5.661e-13. This
local residual is NOT an accumulated-error bound. Its omitted frequency/
curvature terms belong to the same higher order being diagnosed.

## Validation and reproducibility

-19 original action/gauge/flat-parent identities;
-10 microscopic first-adiabatic identities;
-6 independently constructed source-map expansion identities.
-All35 identities reduce to zero.
-24747 independent scalar checks cover flat stress/normalization, finite beat
  evolution, exact cold evolution, symplectic maps and detection of the
  uncorrected weighted defect. These are numerical controls, not independent
  experiments.
-Original1e-10 algebra and2e-5 numerical gates remain unchanged.
-Both original and corrected outputs are retained. No failed physical check
  is reclassified as observational success.

run_action_probe.py creates the original probe; validate_parent_action.py is
its independent validator. derive_connection.py creates the separate
first-order branch; validate_connection.py verifies its source-map expansion
and the matched cold controls. diagnose_adiabatic_scaling.py records the
exploratory order-scaling investigation, not a new cosmology.

## Next physical target

Derive the next adiabatic correction from the KG action, including the
frequency-curvature/negative-frequency contribution, rather than only keeping
the convenient O(H^2) terms generated by inserting first-order pressure into
conservation equations. Then include metric perturbation forcing with the
same source/canonical normalization. Compare all versions on the fixed saved
background before promoting any correction to the retained implementation.

This progresses toward a calibrated formation state and its galactic
occupation. It does not infer a named halo mass or replace missing baryonic
geometry with a tuned boundary. No current galaxy files, original banks,
grids, tolerances, local coupling or live cosmology were changed. No GitHub or
communications action was performed.
