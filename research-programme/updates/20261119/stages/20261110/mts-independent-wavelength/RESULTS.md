# Independent wavelength: same couplings, paired numerical pass

2026-11-10. **Verified progress:** the retained coupled equations pass the specified baseline/MTS control at k=1/Mpc, in addition to the preceding k=5/Mpc test. No mass, G, coupling, background fraction, seed prescription or tolerance is fitted to make this happen. The full research goal remains unfinished.

## What was actually changed

The comoving wavelength input changes from k=5 to1/Mpc. The saved backgrounds and thermodynamics, z=10 start, Delta ln(a)=0.01 interval,64-node positive momentum distribution, action and all four heavy canonical coordinates are retained. The starting state is recomputed from the same controlled physical seed and live metric constraints; fast coordinates are not copied from the old mode.

The selected mode exists in the retained family and heavy matching table. Seventeen actual native captures per case keep the supported late hierarchy signature; the native routine rejects a signature change within that capture. Thermal consistency is within9.830e-14. The new wrapper reproduces complete k=5matrices and the checked source rows exactly at initial/middle/final positions. The heavy preparation solve has condition1.01117455 and normalized residual1.412e-16; its16/32stencil difference is1.574e-26. Cold preparation is unchanged by the stencil.

Sources: `preflight-result.json`, `prepare-result.json` and the corresponding immutable packets. These checks establish the implementation's connection to the retained model, not universal validity of its approximation regimes.

## Completed coupled evolution

For each case a256-step asymptotic-boundary bootstrap supplies the initial metric iterate. Its physical accuracy is **not promoted**. The derived characteristic F17 then supplies the boundary at1060actual evaluation times. The entire coupled system is evolved at128and256steps with that same bank. Boundary time-quadrature controls are below1.840e-16. Final tests reconstruct the neutrino moments and F17 from the **new final metric**, rather than relying on the bootstrap.

One explicit coupled boundary iteration passes those final-history checks in both cases. No second iteration or512-step run is needed for this accepted control. All six forward runs are complete and retain32-step checkpoint packets.

| Final control | Cold baseline | MTS heavy |
|---|---:|---:|
| Normalized128/256state difference | 1.13431672e-8 | 1.13432819e-8 |
| Largest physical-readout step difference | 6.66399e-15 | 1.04227605e-5 |
| Independent normalized metric residual | 5.83118e-9 | 5.83144e-9 |
| Algebraic identity residual | 1.45605e-16 | 9.29867e-17 |
| Neutrino energy-row conservation residual | 4.42335e-16 | 5.76524e-16 |
| Neutrino current-row conservation residual | 1.20539e-16 | 1.20539e-16 |
| Final characteristic low-moment discrepancy | <=5.04976e-15 | <=8.86009e-13 |
| Final paired acceptance | PASS | PASS |

The unchanged gates are2e-5numerical and1e-10algebra. Source comparisons use each field's peak over nine common-scale-factor probes; full states use the frozen coordinate normalization. These are not observational percentages. F17from the final metric matches the supplied boundary at all257saved boundaries to zero in the saved floating-point subtraction, not as an exact-arithmetic identity. Streaming-phase discrepancy is5.330e-14; passive64/128momentum checks are below1.126e-14. The passive test is not a separate128-node coupled background.

**Tightest margin:** the heavy pressure response has peak1.10152725e-21Mpc^-2 in the retained gravity-scaled conformal source convention. Its coarse/fine difference is1.14809547e-26Mpc^-2, or1.04227605e-5of that peak. It passes the fixed gate but is not a high-margin or thirteen-digit pressure measurement. Other MTS physical readout step differences are at most2.850e-13. The small absolute pressure is not a reason to delete its relative check.

Authoritative evidence: `cold-i1-analysis-result.json`, `heavy-i1-analysis-result.json`, their analysis packets, `cold-i1-s128.npz`, `cold-i1-s256.npz`, and the corresponding heavy trajectories. `validation-i1.json` passes191implementation/provenance/reproduction checks and separately recomputes both physical acceptances. Check counts are not independent physical discoveries.

## A physical consistency signal in the retained dispersion

After inspecting the completed modes, we derived and recorded a **post-test mechanistic diagnostic**, not an additional frozen prediction. In the locally frozen scalar equation the slow envelope beat is

    omega_s = k^2/(sqrt(mu^2+k^2)+mu),  mu=a*m.

Its square tends to k^4/(4a^2m^2). This is the same gradient-pressure mechanism in the inherited weak-field Schrodinger-Poisson limit; the actual runs retain expansion corrections and fast coordinates. Under a common short-time source response, a density departure proportional to k^4 gives an absolute metric-potential departure proportional to k^2. No coefficient is fitted to the two results.

At the final saved epoch the MTS-minus-cold potential shifts are1.47761030e-19at k=1and3.69403308e-18at k=5. Their ratio is25.00004963, close to the leading k^2expectation25. The fractional shifts are1.85806189e-7and1.16227237e-4, with ratio625.529417rather than exactly625. Much of this distinction is the baseline's own small wavelength-dependent transfer, which is retained explicitly.

The absolute-ratio departure is1.98524e-6relative to25. The summed saved time-step-difference proxy is1.03642e-6relative: the discrepancy is of comparable order but is **not claimed to lie inside a certified error bound**. It also includes unbounded physical approximation effects. At the three sampled positions k/mu<=3.66921e-4; the W2beat differs from the frozen exact scalar beat by at most1.999e-15in the evaluated arithmetic. Six dispersion polynomial checks pass. Two post-inspection modes do not establish a universal scaling law or empirical preference.

See `DISPERSION-CONSISTENCY.md`, `dispersion-consistency-result.json`, and `wavelength-comparison-i1.csv`. This connects the observed numerical response to an existing field-gradient term rather than introducing a new fitted galaxy force. It does not select the heavy-field population or eliminate the fast branch by assertion.

## Remaining physical qualifications

The baseline slow scalar source remains tiny (peak4.03972e-22Mpc^-2) but not uniformly slow: rate/(k*peak density) is0.988855, and pressure/peak density0.999613. The heavy combined custom source peaks at8.18183e-13Mpc^-2, with corresponding ratios0.00106553and1.77876e-9. These diagnose source ordering; they do not bound every omitted radiation term. The leading-radiation and W2/late-heavy approximations keep their documented scope. A lower metric residual cannot alone certify an approximation outside that scope.

The seed is still the explicitly prescribed late thermal/density disturbance, not a recovered primordial spectrum. Current readouts are controlled solutions, not galaxy rotation curves or data-fit improvements. The original historical full-span archive qualification is not resolved by this new mode.

The retained heavy projection table does cover k=1exactly, over modes1e-5to10/Mpc. Its matching scale is0.00022501566262210325, matching-density coefficient2.479342985570997e-8in its native convention, and retained heavy fraction0.5. Those inputs were reused, not derived anew or refitted. `matching-input-map-i1.json` records paths/hashes for the next initial-state bridge. The cold table has no heavy matching layer; missing heavy entries are not fabricated.

## Preservation and next action

All inherited artifacts are hash-checked. `closeout.json` and `CLEANUP-VERIFIED.json` record the final seal and exact exited worker identities. No production action/library/bank, Galaxy file, other chat or shared service is changed. No GitHub, new browser, timer, relay, subagent or source download. The Galaxy09force handoff is retained with attribution in `GALAXY-UPDATE-09-RECEIPT.md` and is not independently reproduced here.

**Next: derive the early-to-late physical state projection from the retained action and original matching history.** Identify what the saved two fluid moments retain, what phase information they lose, and recover that information from retained early field evolution rather than imposing the D0preparation as a physical law. Apply the same initial-data standard to the baseline. Do not spend the next stage on another arbitrary wavelength or more refinement of these passing points; see `NEXT.md`.
