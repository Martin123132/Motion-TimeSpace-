> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# Why the two gravity routes launch different photons at 89.1485038031 conformal Mpc

The difference of the entry impulses is predictable from the saved preparations. On both gravity grids the complex amplitude error is below 1e-8 percent, including both subdivisions, without reading the outgoing curvature or photon impulse when constructing the forecast. This is a conditional constraint calculation on the same initial data, not an independent cosmological measurement. The unexpected result is which input survives the cancellation: **the heavy energy forcing was evaluated two different ways at the same off-grid switch**.

| Four subdivisions, primary photon transfer | p16 | p32 |
|---|---:|---:|
| Entry contribution / original small correction, joint % | 1.336890 | 1.336904 |
| Full physical route discrepancy, joint % | 1.567398 | 1.567329 |
| Residual after subtracting the predicted entry, energy / current % | 0.261257 / 0.264277 | 0.261202 / 0.264223 |
| Residual after subtraction, joint % | 0.261935 | 0.261880 |
| Change just to the matched wave's own mean current, hold smooth history fixed: resulting joint % | 1.570797 | 1.570729 |

The 0.5% tolerance, sign conventions, two gravity clocks, source grid, scattering bank and launch scale did not change. The residual passes as **attribution**. The saved physical trajectory still gives 1.5673%; no term was subtracted in a new evolution. The alternative current estimate converges to 0.00276% of its difference from the original at both quadrature/time refinements; it does not improve the answer.

## What was predicted

For each route K is the matched potential minus the corresponding resolved potential immediately after the switch. Compute D = K_density − K_momentum. At the matched momentum curvature P let R_f be the *fluid* energy constraint residual, dD_h the physical heavy-density replacement at fixed P, dJ_h the instantaneous current replacement, j_c the normalized complementary current from the previously frozen pressure/exchange integral, B the wave energy-constraint denominator, and A = 3H/(2k²). The initial complementary density is zero under this saved preparation. Then

    D = −[R_f + dD_h/2 + A(dJ_h + rho*j_c)]/B − (Phi_density,resolved − Phi_momentum,resolved).

The resolved density potential here is independently calculated from its own initial state, 77-bin stress and source terms. The matched and resolved momentum impulses, density impulses, their small complex difference, and the no-companion control were all predicted. The separate backwards integration of the launched wave computed its own mean and terminal current from the supplied incoming metric, using 48/96 phase nodes and two step bounds. This does not solve a new pre-switch metric. [Frozen components](evidence-001.zip) (archive member: `forecast.json`) · [physical and counterfactual comparisons](evidence-001.zip) (archive member: `comparison.json`). All photon comparisons used the previously frozen unit impulse and signed energy/current histories; comparisons across the three scattering settings and both subdivisions are retained.

## Where it came from

On the fine grid, about **93.1165%** of the signed entry difference along its own complex direction comes from just the difference in henergy between the incoming inversion and the outgoing evolution; the corresponding end-current hJ mapping contributes **7.1344%** before the other current terms. These are projections, not positive probabilities. Net current accounts for 6.8832%; the change of metric in the explicit volume term contributes less than 0.00001% along the discrepancy. Ordinary matter, the resolved residual and the other normalization terms were retained. [Independent energy-coefficient breakdown](evidence-001.zip) (archive member: `energy-origin.json`).

Same stored table and quintic order, different supports: the incoming inversion extrapolates from the left; the outgoing operator interpolates using the bracketing samples. The switch is about 76.06% from 89.14375 to 89.15000 Mpc; there is no direct table entry there. In a predeclared leave-one-knot-out diagnostic, **the bracketed estimate beat the incoming-only estimate at all 16 nearby knots, for both energy and current**. Errors were normalized to the *difference between interpolants at the switch*, not the large total source. Left/right energy RMS errors: 109%/125% (prefix) versus 2.54%/2.43% (bracketed); current: 458%/456% versus 6.82%/6.94%. The held knots are one full step past the previous sample and share the same bank; they do not measure the off-grid switch or authorize future data in a prospective launch. [Blind knot protocol and predictions](evidence-001.zip) (archive member: `bank-forecast.json`) · [release](evidence-001.zip) (archive member: `bank-check.json`).

**Best next physical test:** obtain henergy and hJ directly from the microscopic source at the actual switch, or obtain a refined incoming-only estimate with a measured error there. Use one agreed source representation in both the preparation and joint evolution; derive a new launch, then propagate it, including the smooth response and photons, without imposing an impulse subtraction. The existing result points to a source-evaluation mismatch, not evidence that gravity requires a new coupling.

Replay in a fresh sibling with the three earlier sealed stages and the other pinned parents: entry.py, compare.py, energy_origin.py, bank_witness.py forecast then score (Python 3.13, -B, single numerical thread). Earlier archives remain unchanged.
