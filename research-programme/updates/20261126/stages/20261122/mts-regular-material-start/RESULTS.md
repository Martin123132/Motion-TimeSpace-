> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Where the early gravitational state comes from

**The same prepared matter now predicts the same later gravity from three early starts, without supplying a compensating fluid.** We derived a regular adiabatic initial state, with neutrino shear, dust, photons and the canonical scalar field(s), and integrated the coupled material and gravity equations through horizon entry on the retained cold and heavy-MTS backgrounds. This answers the previous stage's initial-surface question on a finite interval; it is not an observational fit. We did not adjust any gravitational coupling, incoming amplitude or clock to recover the old compensated snapshot.

The initial linear curvature phases and backgrounds are inputs. The forced comparison sets the *independent quadratic* primordial curvature to zero, **not** the initially induced metric or matter contrast. Adding a unit squared-curvature seed is a separate control. Linear theory, GR constraints and minimally coupled kinetics are borrowed framework, not MTS discoveries. The numerical result is which states and metric differences the retained MTS/common-metric system generates from these inputs.

## Where the comparison is strongest

All five signed mixed Fourier modes, all three starts at conformal times 0.00625, 0.0125 and 0.025 Mpc, common endpoint 6.4 Mpc. The 782 incoming wavenumbers have maximum kη=0.015 at the earliest start, 15.35 at the end. The MTS scalar fraction of the background is 2.118% at the end. Below are **largest** relative differences, not averages over favorable modes. A local small nonzero signal is its own denominator. The numerical gate remains 0.5%, not a confidence interval.

| Comparison | Cold | Heavy MTS |
|---|---:|---:|
| Moving the start from earliest to latest: worst curvature, lapse or Weyl at shared endpoint | 0.001752% | 0.001774% |
| Same start change, worst at any common saved output | 0.11671% | 0.11527% |
| Propagate independent spatial trace vs solving the two matter constraints at each step, worst of 81 saved outputs | 0.000753% | 0.000773% |
| Halve the adopted Radau step, worst of those outputs | 0.003401% | 0.002896% |
| Change photon/neutrino angular cutoffs together (4/12 against 6/18), same SDIRK method | 0.001970% | 0.001853% |
| Added primordial control minus forced run vs exact-wavelength native linear transfers, 7 material/metric fields | 0.17582% | 0.01023% |
| Same linear control: just the two metric potentials, all times | 0.004893% | 0.003012% |

At the endpoint the **lapse difference between the cold and heavy backgrounds**, divided by the cold lapse, ranges from 0.63% to 6.38% in complex magnitude across the five modes (1.29% on the first mode). This is a model-to-model difference on the same seeded panel, not an observed preference. More importantly, project the forced two-potential vector (curvature and lapse, equal component weight) onto the *best possible complex multiple* of the independent adiabatic linear transfer at the same k and time. The component that cannot be reproduced is **4.38–35.24% cold; 5.26–34.74% heavy** of the forced vector norm. Thus this two-potential signal is not just a resized primordial growing mode. That distinction does not fix the primordial amplitude, exclude other primordial degrees of freedom, or establish a specifically MTS-only effect: the cold control shows it too.

## Two traps the checks actually caught

1. The first leading-order slip formula used the wrong sign for a projected Hessian. Its internal slip and momentum identities passed at machine precision, yet its actual material-constraint lapse at launch differed by up to **52.42%**. Restoring the minus from two Fourier derivatives reduces the worst finite-start lapse discrepancy to below 0.0043%, without changing the source bank or tolerances. Bare `origin-{model}` and `flight-{model}` outputs are rejected controls, not starts for later evolution.
2. The second-order time solver looked satisfactory on the forced metric, but missed the native small neutrino shear by up to **6.45% cold / 1.48% heavy**, pointwise. Its results and failures remain. A third-order stiff integrator, separately step-halved, passes the unchanged test. On the accepted route all 155 per-model grouped checks pass. They include independent native material transfer and scalar clock checks are documented separately; 155 is not the number of independent experiments.

## What is actually saved for continuation

- The endpoint for every signed mode, all three starts and both free-curvature settings includes the canonical variables, dust, photon and polarization moments, gravity and integrated neutrino hierarchy. Column order: earliest forced/free, middle forced/free, latest forced/free. Exact reconstruction of all 12 saved observables from these restart fields is checked. Cold restart (not bundled here) · heavy restart (not bundled here).
- A particle distribution at different momenta cannot in general be restarted by copying the integrated brightness to every thermal momentum. For initial thermal collisionless rays we derived its missing spectral shape from the squared incident temperature field and independently transported it. Full 19-moment vectors agree to **0.132% or better**. The 48-node momentum integral returns the saved brightness to a relative vector error below **3.0e-12**; the 12- and 24-node controls did not reach the separate 1e-8 replay threshold. The shape coefficient itself has a norm 6–45% of the forced brightness norm depending on the mode; **it is not a 6–45% correction to gravity**. At fixed endpoint state its massive thermal weighting changes either metric potential by under **0.0000049%**. Cold distribution (not bundled here) · heavy distribution (not bundled here).
- The common-speed neutrino propagation is an early relativistic approximation (final mass/thermal temperature 0.00498); evaluating finite-mass thermal stress on that state is not the same as evolving momentum-dependent particle speeds. Incident photon high multipoles use a tight-coupling recurrence. Both the interval and the five-mode scalar long–short truncation matter. No late-time potential, CMB spectrum, galaxy sign or local GR measurement is inferred from these numbers.

**Next:** use the saved distributions rather than installing a new late-time density or incoming compensation. First propagate the first- and second-order massive neutrino distributions with their true momentum-dependent velocities on a short overlap ending at 6.4, checking both gravity constraints and small momentum bins against the relativistic control. Then extend the complete species state toward the archived η≈87 Mpc window. Predict its two potentials before comparing with the old compensated and material-start variants; include the accrued truncation/transfer error. Do not extrapolate the 6.4-Mpc differences to that window. The separate Pal 5 observational decision is unchanged.

[Derivation and assumptions](DERIVATION.md) · [cold mode/time checks](evidence-001.zip) (archive member: `checks-cold.csv`) · [heavy mode/time checks](evidence-001.zip) (archive member: `checks-heavy.csv`) · cold forced endpoint test (not bundled here) · heavy forced endpoint test (not bundled here) · [kinetic check](evidence-001.zip) (archive member: `spectral-check-heavy.csv`) · [replay instructions](REPLAY.md).
