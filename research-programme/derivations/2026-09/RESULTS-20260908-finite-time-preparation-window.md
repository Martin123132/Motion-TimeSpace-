# Finite-time local preparation: executed result and limits

Private, 2026-09-08. This is a quantitative advance in the linear preparation
problem, not a claim of full local GR or an observational test result.

## What is now derived and executed

The retained quadratic motion operator is compared with the flat massless
wave equation without replacing the parent operator. Its curvature, mass and
kinetic-coupling residual produces a finite-time energy bound. The proof is
`DERIVATION-20260908-finite-time-causal-escape-and-forcing.md`.

For compact initial data and observation inside stellar areal radius R,
the unforced low-angular-band result has the form

```text
E_motion,obs(t) / E_motion,initial
    <= min(1, C_obs C_init expm1(J_L(t))^2),
t > S_initial + S_observation.
```

The constants come from analytic TOV-Lambda geometry envelopes and the
retained K=1+2u C^2 operator. Neither a fitted damping parameter nor a
reflecting outer wall was introduced. The exterior participates in the
causal evolution.

The comparison uses the standard flat 3D Kirchhoff/Huygens property, not an
assumed Huygens property for the curved parent. The primary reference and its
precise scope are recorded in the proof and result provenance.

## Numerical reference results

The gamma=3/2 material EOS is retained. The independent-variable scaling in
the new TOV-Lambda solver permits a weak star without a long raw-radius solve.
All lengths below use R=1; time is the fixed static-coordinate time in R/c,
not a universal statement about the readings of all local clocks.

Weak reference: GM/(Rc^2)=1.66167958e-6, mR=1e-6. Positive-Lambda control:
H^2 R^2=5.68423725e-13. These are declared reference inputs, not sourced solar
measurements or signed physical MTS coefficients.

At t=2.00201682 R/c the positive-Lambda energy-fraction upper bounds are:

| Retained angular band | u/R^4=0 bound |
| --- | ---: |
| ell <= 0 | 3.73727012e-8 |
| ell <= 1 | 3.00127663e-7 |
| ell <= 2 | 1.58068724e-6 |
| ell <= 4 | 1.40187995e-5 |

For the monopole with u/R^4=+0.005 or -0.005 the conservative bound is
3.79555975e-8. The signed envelopes agree because their analytic estimate
uses |u|; this is NOT a theorem that the actual signed dynamics agree.
The corresponding Lambda=0 monopole controls are 3.73726852e-8 (u=0) and
3.79555808e-8 (either nonzero sign).

For each of these weak bands the illustrative target energy fraction 1e-4
holds on the available interval from about 2.00202 to 2.99999 R/c. Its
energy-time integral is bounded by 9.97975e-5 E_initial R/c. This is the factor
that can enter the existing smoothly smeared Hilbert-source bound; 1e-4 is
not an experimental tolerance.

**Baseline fairness:** u=0 is the same curved-background calculation with a
minimally coupled massive spectator scalar. It also passes the weak-reference
bound. Thus the escape mechanism is not evidence that MTS outperforms GR;
it demonstrates a possible preparation mechanism for the extra sector on
the selected MTS branch. Pure GR has no corresponding extra scalar to clear.

## The stronger reference remains unresolved by this estimate

At GM/(Rc^2)=0.04028665 and mR=0.49644238, the u=0 upper bound clips at energy
conservation (fraction 1). For u/R^4=+/-0.005, the coarse initial norm
conversion is unavailable. Both outcomes are preserved for Lambda=0 and
positive Lambda. Neither is evidence of physical growth or a failed theory;
this particular sufficient estimate supplies no useful suppression there.

## Validation actually performed

- Main companion: in-memory compile; 111/111 checks, 2.758 seconds of reported
  numerical runtime. Four stellar references, 48 band/coupling rows, tighter
  ODE comparisons and the frozen Lambda=0 TOV baseline are included.
- Nonzero compact manufactured forcing remains nonzero after free-wave
  clearing and is bounded by the supplied force budget. Omitting the force
  fails the control. Angular-tail and coherent spatial-remainder checks
  prevent silently replacing arbitrary data with compact radial vacuum data.
- Independent companion: in-memory compile; 79/79 checks, 2.980 seconds of
  reported numerical runtime. It reintegrates the TOV-Lambda equations in
  direct areal-radius/enthalpy variables, rather than calling the first
  solver or reusing its computed potential. It computes the Weyl moment and
  harmonic-mean cancellation stably, checks analytic center limits, and
  compares sampled V0, angular residual, beta and metric/kinetic coefficients
  against the analytic envelopes.
- Those 79 comprise 20 profile checks, 56 checks on eight exported monopole
  envelopes, and three integrity checks. Four stronger signed envelopes are
  explicitly skipped because the first runner exported no informative norm
  conversion; they are not counted as validated envelopes.

The independent sampling does not certify a continuous supremum. The proof
of the analytic envelopes is still necessary. Neither background solve uses
directed interval arithmetic, so these numerical references are not
interval-certified stellar models. A count of passing checks is not a count
of independent physical predictions.

## What this does not establish

The result requires a static regular background, positive retained kinetic
coefficient, the stated smooth surface, a finite causal region and specified
initial/support/angular budgets. A general finite-energy spatial remainder
is carried with its coherent cross term, not assumed to vanish. Continued
forcing has an explicit nonzero budget. Arbitrary extended quantum states
have not been shown to supply the required budgets.

This is a finite window, not a permanent settling rate. Nonlinear derivative
interactions, metric/fluid backreaction, and preparation of rho_local=rho_0
are not proved by the linear calculation. Locally escaped energy also has
not ceased to gravitate: exterior stress and metric constraints must be
included before assigning clock, orbital or PPN residuals. The complete
higher-operator correction and the common galaxy/cosmology dynamics remain
open. No physical-claim flag is promoted.

## Reproducibility and frozen evidence

- Runner: `scripts/parent_finite_time_escape_20260908.py`.
- Result: `source-intake/local-preparation/20260908/finite-time-initial/result.json`.
- Independent runner: `scripts/finite_time_escape_profile_verify_20260908.py`.
- Independent result: `source-intake/local-preparation/20260908/finite-time-initial/profile-verification-initial/result.json`.

Each output retains an executed script, source hashes and completion marker.
Do not silently edit their pinned scripts or proof; any refinement requires
versioned evidence. The untouched 8760-file formalization-workbench metadata
SHA is 5d2a482310acd9ba509985c584515bfd8525b721a5d5629c900ab055445acf38.
No scripts bytecode cache; no GitHub operation; one numerical worker at a time.

Next physics priority is to derive a usable nonlinear/incoming-source budget
from the retained parent, rather than setting the forcing to zero by closure.
Real-star background and observable-response inputs are then needed to turn
the sufficient inequality into a physical local-gravity test.
