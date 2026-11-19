# Direct metric-source derivation and background-flow diagnosis

Completed locally2026-11-09. No new physical history, field action, physical grid, parameter, bank or tolerance. The previous accepted source remains untouched.

## What is derived and tested

1. Derived the massless monopole source independently from the retained GR/Poisson-spatial stress equations, using exact finite-background product/quotient rules.
2. Froze18saved points first; native rates/backgrounds replay bitwise and independent90-digit checks passed. Reused those probes while evaluating the remaining2024EXISTING source nodes.
3. All4084branch cases pass the independent full-grid source algebra. Maximum individual-rate discrepancy8.059e-16; independent finite increments agree after rounding. Both models receive identical checks.
4. Projected the candidate pair through the original adjoints and quadratic weights. Independent forward-map and weighted-integration checks pass.
5. Derived the explicit scalar energy/momentum divergence from background-flow defects, then independently checked16336scalar cases and its observable-source decomposition.

Authoritative derivations: DERIVATION.md for the metric equations, with its metadata wording corrected by STRESS-BALANCE-DERIVATION.md; the latter contains the new source-coupling identities and verified background provenance.

## Numerical outcome

Arithmetic-only replacement does NOT close the MTS quadrature flags. Original -> candidate signed refinement magnitudes (same original budget):
- GR/Pi:4.30990089e-5 ->4.30988757e-5.
- GR/delta_massless:4.60594613e-5 ->4.60596397e-5.
- Poisson-spatial/Pi:2.67808599e-5 ->2.67807767e-5.
- Poisson-spatial/delta_massless:2.72271902e-5 ->2.72275793e-5.

The candidate changes the MTS final integral by at most1.988e-18 of its saved observable scale. Baseline changes reach7.496e-18 of its scale, despite larger relative changes in its tiny source difference. No candidate full-source budget or20-case pass count is claimed; previous16/20MTS and0/20baseline accuracy status remains authoritative.

## The useful diagnosis

The heavy-field background-flow defect accounts for essentially all the troublesome Phi_dot0 refinement contribution. We have an explicit algebraic mapping from that defect into density, momentum and metric source—not merely a correlation with a failed flag.

Normalized heavy reference-background defects reach~6.8e-9; the retained instantaneous background is at rounding scale. Although tiny compared with the main background, their variation matters to this weak source contribution. The saved MTS interval crosses158dense-polynomial segments, whereas the baseline interval crosses2.

Next is a focused segment-aware integration/weak-form test of this DERIVED defect source, retaining the saved path and boundary terms. Do not delete the defect, overwrite the background derivative, loosen tolerances or double the entire grid blindly.

## Evidence and scope

- balanced/freeze.json; probe-audit/result.json.
- balanced/full-freeze.json; balanced/stress-full-01/result.json.
- balanced/metric-projection-01/result.json; full-audit/result.json.
- balanced/stress-balance-01/result.json; balance-audit/result.json.
- DENSE-SEGMENT-INVENTORY.json; STRESS-BALANCE-DERIVATION.md.
- closeout.json/CLEANUP.json once sealed.

All new work remains private/local. No GitHub, compiler, subagent or other-chat intervention.

