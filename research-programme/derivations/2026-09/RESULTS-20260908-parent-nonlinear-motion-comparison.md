# Nonlinear parent comparison: executed result

Private, 2026-09-08. The retained nonlinear interaction now has an explicit
energy-error bound with source-owned coefficients. This is not yet a full
inhomogeneous or backreacted preparation theorem.

## The mathematical advance

Starting with the selected action -K X/2-m^2 chi^2/2+Q(X), the derivation
constructs its principal tensor, common time-slice condition, conservative
characteristic cone, nonlinear energy comparison, additional Hilbert stress
and exact metric/connection source terms.

The useful comparison is with the physical quadratic evolution having the
same initial data and background. The difference obeys a forced linear
equation whose positive energy bounds every newly generated angular mode.
It is not necessary to pretend that the nonlinear field remains radial or
bandlimited. With the stated uniform gradient and regularity budgets,

```text
sqrt(E_local / E_initial) <= sqrt(epsilon_linear) + C_Q B_H,
B_H = integral ||Hess chi||_L2 / sqrt(2 E_quadratic) dt.
```

The parent equation also eliminates the second time derivative from B_H in
favor of spatial/velocity derivatives and controlled lower-order terms.
Small first gradients are NOT silently substituted for this higher-derivative
budget. A compact high-frequency negative control demonstrates the distinction.

Proof: `DERIVATION-20260908-parent-nonlinear-motion-comparison.md`.

## Actual coefficient input, not a fitted damping term

The runner reads the source-locked 4958 N=6 and N=8 trajectory endpoints in
both regulator schemes. The CSV still matches its historical 5209 lock.
At the stored g approximately 1e-10 endpoint, x=U_star/k^4=0.1, k0=N_max=1:

| N8 quantity | Dynamic scheme | Reference scheme |
| --- | ---: | ---: |
| Principal perturbation bound eta | 1.94202129e-18 | 1.92167565e-18 |
| Energy-comparison bound theta | 1.61835108e-18 | 1.60139638e-18 |
| Nonlinear error amplitude per B_H, C_Q | 2.58936172e-18 | 2.56223420e-18 |

The source coefficient is not set to zero just because binary64 arithmetic
would round 1+eta to 1. The runner retains 80-digit Decimal evaluation and
reports the nonzero characteristic-cone correction separately. These digits
preserve a tiny correction; they do not improve the accuracy of the original
stored trajectory coefficients or make the envelopes interval-certified.

Transferring the sufficient bound to the declared weak linear reference,
even the illustrative B_H=1e6 case changes its monopole fraction only from
3.73727012448e-8 to at most 3.73727022460e-8 in the dynamic scheme. A target
fraction 1e-4 permits B_H up to about 3.78730e15 under the same hypotheses.

Those are conditional budget examples, not a claim that a real star has
B_H=1e6 or that all dimensional inputs have been jointly matched. The stored
finite-polynomial endpoint does not certify arbitrary RG scales, uncomputed
operators, or an unrestricted ultraviolet characteristic/front velocity.

## Checks against actual nonlinear evolution

The primary companion compiled and passed 199/199 checks in 4.062 seconds
of reported numerical runtime. This includes exact action differentiation,
both-sign signature/cone/energy controls, nearly null gradients, the
acceleration-elimination estimate, connection terms, invalid-input controls
and 24 source-owned coefficient-envelope cases. These checks are not 199
independent empirical predictions.

A second companion integrates a homogeneous nonlinear oscillator, rather
than only evaluating the analytic formulas. It includes the free baseline,
both quartic signs, and two mixed quartic/sextic controls, at two tolerances.
The deliberately amplified coefficients expose effects that would disappear
into floating-point error with the tiny physical-reference coefficients;
they are validation controls, not alternative MTS fits.

The oscillator is defined in a unit spatial volume and has no spatial
escape. It tests the physical difference-energy and source-budget identities,
not the stellar clearing theorem. All 118/118 checks pass, with 3.050 seconds
of reported runtime. Maximum relative conserved-energy drift is 1.11e-11.
The four nonlinear controls have nonzero deviation from their free baseline;
omitting the source fails to bound that deviation. Source-inclusive bounds
hold at the sampled times, with numerical tolerances explicitly in the code.

## A closed regularity example, with its boundary made explicit

For these homogeneous controls, the derivative budget can actually be bounded
from initial data rather than supplied independently. Here K=N=m=1,
chi(0)=0.2 and dot(chi)(0)=0, so E0=0.02. For U_star=0.1,

```text
E_total >= (1-theta) dot(chi)^2/2 + m^2 chi^2/2,
dot(chi)^2 <= 2E0/(1-theta) < U_star.
```

At a hypothetical first exit from the gradient domain, conservation would
contradict this strict inequality. Thus the homogeneous gradient condition
closes by continuity. The principal-time coefficient stays above 1-eta;
solving the oscillator acceleration equation and using the same energy gives

```text
B_H(T) <= m T sqrt(1+theta)/(1-eta).
```

At T=4pi, measured B_H is between 7.95 and 8.05; the derived nonlinear upper
bounds are below 13.25. The solution stays in a bounded, nonsingular ODE
domain. This is a genuine closed homogeneous control, not an inference that
spatial PDE gradients cannot concentrate or that metric work vanishes.

## What remains and the next derivation

The next step is to extend this initial-data control to the inhomogeneous
stellar equation, retaining its physical interface conditions. Global energy
alone does not bound a pointwise gradient or its spatial derivatives in three
dimensions. A propagated higher-regularity estimate is needed; it cannot be
replaced by the homogeneous example.

For the full coupled problem, metric work, incoming data, the state functional
and remaining higher/nonlocal operators must also be controlled. The exact
metric-source identity is now available, but its coefficients have not been
bounded by solving the coupled constraints. No R10, PPN, all-operator local-GR
or complete-MTS flag is promoted. No claim of observational superiority over
the baseline follows from these tests.

## Reproducible evidence

- `scripts/parent_nonlinear_motion_comparison_20260908.py`.
- `source-intake/local-preparation/20260908/nonlinear-parent-initial/result.json`.
- `scripts/nonlinear_motion_ode_controls_20260908.py`.
- `source-intake/local-preparation/20260908/nonlinear-parent-initial/ode-controls-reference1/result.json`.

Each executed script and its sources are hashed and retained. Do not edit the
pinned proof/scripts silently. The 8760-file formalization-workbench metadata
remains unchanged. Everything stays local and private.
