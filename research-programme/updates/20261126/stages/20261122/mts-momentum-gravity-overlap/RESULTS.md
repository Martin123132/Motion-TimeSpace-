> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# What slow neutrinos change — and which background differences survive

**We can carry the distribution forward instead of assigning the same speed to every particle or inserting a late gravitational compensation.** From the frozen regular material state, we propagated both the incident and quadratic collisionless fields with their actual momentum-dependent speeds. We returned their energy, current, anisotropic stress and pressure trace to the other matter and gravity equations. Neither the source strength nor the primordial amplitude was fitted. The parent bank, canonical couplings and numerical tolerance remain unchanged.

## Size of the correction

On the five retained Fourier modes from conformal time 0.00625 to 6.4 Mpc, the largest endpoint change in the forced **quadratic lapse** against the previous thermal-weight/common-speed control is **0.0000222% cold and 0.0000232% heavy MTS**. The underlying particle changes are not uniformly tiny: the softest primary node ends at about 0.0245c, and its angular perturbation can differ by hundreds of times the corresponding unit-speed shape. Its small phase-space weight matters. No data scored a flow direction or selected a cosmology here.

| Precision question, both models and curvature controls | Worst result |
|---|---:|
| Replaying either of the 1.6→6.4 and 3.2→6.4 overlaps from the actual accumulated state: stress change relative to its own peak | 0.000016% |
| Replacing that accumulated mass lag by zero at 3.2: worst error in the correction relative to its own peak | about 70% |
| Independent energy/current balance, error relative to the **correction**, not the universe's total | 0.00767% |
| Derived one-channel law vs 77-node transport, largest error in any of the four stress histories, in peak norm | 0.07544% |
| Same law vs exact **gravitational increment** (curvature, lapse, Weyl, scaled momentum metric), in peak norm | 0.00507% |
| Same law vs the nonzero final gravitational increments, largest pointwise endpoint error | 0.01144% |

Three feedback passes converge on both backgrounds; the third makes no resolvable change to the saved metric at native precision. The coarsest log-momentum grid missed the 0.5% endpoint test on one stress component on each background (up to 1.38%). The 39→77-node comparison resolves this: largest stress endpoint change below 0.000005%; both the earlier failure and the final comparisons are retained. The microscopic log-momentum derivative agrees with independent symmetric perturbations to within 0.00086% on the checked modes/momenta. The zero-mass driver control goes back to the thermal shape at roundoff. Independent native first-order energy/normal-flux vector comparisons across 782 modes are within 0.00034% on the sampled surfaces. These are different controls; no individual-bin accuracy is inferred from an integrated stress check.

**Why the analytical shortcut works.** For a regular thermal occupation the leading velocity correction is proportional to ((am/q)^2). The thermal weight of the correction has mean spectral derivative **−2**, not the massless brightness mean **−4**. One propagated response at −2, the squared-temperature shape and the analytic thermal integral π²/6 give all four stresses, without a free coefficient. It fails as a bin-by-bin expansion near zero momentum; the quoted accuracy is for the thermally integrated histories on this interval, not a promise at 87 Mpc. [Derivation](DERIVATION.md) · cold (not bundled here) and heavy (not bundled here) exact comparisons.

**Why two gravity calculations initially disagreed on the tiny increment.** The material constraints and an independent spatial-trace evolution agreed closely on total gravity but gave subtractions that differed by up to **231% of the increment's peak**. The old control used finite-mass thermal weights with a unit-speed transport law. It does not obey the massive energy and momentum equations exactly. We derived the two divergence terms of that comparison directly from the transported distribution, not by fitting either potential. Including them in the independent trace *comparison* predicts the material-constraint correction to **0.00284% of the increment's peak** (worst endpoint 0.00334%). No corrective term was installed in the physical action. Omitting the streaming mismatch or the quadratic driving fails the independent balance test by order unity. [Cold](evidence-001.zip) (archive member: `ward-check-cold-s2-dense.csv`) · [heavy](evidence-001.zip) (archive member: `ward-check-heavy-s2-dense.csv`) · negative controls (not bundled here).

## Can a different primordial amplitude hide the cold/MTS distinction?

We allowed each background its **own arbitrary complex quadratic adiabatic growing-mode amplitude at each k**. We did not choose an amplitude for the theory. A linear projection gives the *smallest possible* model difference after optimizing these nuisance directions. The comparison uses the fixed, signed long–short input phases and background parameters, a common scale factor at each epoch, and equal weights on the selected complex perturbations. This is not an observed noise model.

| Compared on each mode | Fraction of forced cold–MTS difference that cannot be absorbed | Residual as fraction of the cold quadratic signal norm |
|---|---:|---:|
| Both potentials at one endpoint, two free amplitudes | zero within roundoff | zero within roundoff |
| Weyl potential alone at three epochs | 35.09–65.20% | 0.097–0.766% |
| Both potentials at three epochs | **57.72–78.88%** | **0.166–0.757%** |

The single-epoch failure is real. With only the endpoint pair and the two independent growing modes, a rotation of the initial amplitudes can reproduce those two complex numbers. Across three epochs **the time dependence** is different. The three physical epochs correspond to the smaller scale factors reached by the two backgrounds at conformal times 1.6, 3.2 and 6.4 Mpc. The transfer columns are nearly parallel (condition numbers about 230–3393); independent native linear transfers, the independent gravity route and the finer momentum grid reproduce the surviving fraction. A mixed lower-angular/second-order time solver changed the small residual vector by up to 0.83%, above the unchanged comparison gate. Keeping integrator and cadence matched reduces the angular-only test to below 0.000016%; the failed mixed check remains in the record.

This residual is a fraction of the **quadratic scalar perturbation on this prescribed panel**, not of total gravitational power. It does not rule out different input phases, isocurvature, other primordial modes, distances, survey projection or noise masking it. Nor is it evidence in favor of either background. It identifies which future tests can, in principle, carry information: a temporal or projected shape, not just a single amplitude. [All nuisance choices and clocks](evidence-001.zip) (archive member: `primordial-contrast.csv`) · coefficients and singular values (not bundled here) · [sensitivity](evidence-001.zip) (archive member: `contrast-sensitivity.csv`) · [matched angular test](evidence-001.zip) (archive member: `contrast-matched-angular.csv`).

## Reaching the old window without artificial reflections

We tested an independent line-of-sight calculation: a particle of speed v(q, η) travels comoving distance ∫v dη; Legendre projecting its angular phase gives the exact free-streaming propagator for each input multipole. We integrate the saved driving terms along that path. On the driven 3.2→6.4 overlap its first three moments match the evolved distributions to **0.00521% in vector norm**, worst individual moment below 0.0092%, for four widely separated momenta, all probes and both initial-curvature choices. Cold (not bundled here) · heavy (not bundled here).

The old window starts at 87.62048/87.62054 Mpc. A **force-free numerical control only** propagates the actual saved massless angular endpoint over that missing distance. Closing the hierarchy at order 18 reflects radiation back into the low moments: one mode's error is about 99 times its true remaining low-moment norm. To date, no driven second-order history through the missing gap is claimed here. Use the tested streaming propagator or a validated increasing angular cutoff, not an untested long order-18 flight.

**Next physical stage:** propagate the complete state *forward*, initially 6.4→12.8 Mpc, acquiring the new native first-order sources and their incident angular history. Keep the freely specified growing mode separate, use matched-scale-factor output, test the leading law with full momentum bins where it is most sensitive, and prevent a reflecting hierarchy tail. Continue toward the old 87.62-Mpc window to predict its gravity **before** comparing with the old compensated result. The eventual observational question is which line-of-sight transfer retains the surviving time dependence. No simulations were published or left running.
