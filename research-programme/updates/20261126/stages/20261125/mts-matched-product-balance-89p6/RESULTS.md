> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The matter equations reproduce the matched photon discrepancy

**25 November 2026 · frozen-U/original-Q/Fq mean-current control · 89.148503803–89.6 conformal Mpc · photon launch.** Independently predicting the potential change from the matter equations gives the same stable matched discrepancy as the saved endpoints. On the fine gravity step the predicted and saved complex photon vectors differ by **0.00000730% of the matched discrepancy**. The mismatch with the momentum constraint therefore survives a solver that never uses the measured right-hand potential as a target or input.

| Joint visibility-weighted result (% of original small momentum-route correction) | Coarse gravity | Fine gravity |
|---|---:|---:|
| Matched discrepancy from saved increments and within-cell history | 0.53899358 | 0.53899555 |
| Matched discrepancy predicted from the matter equations and momentum constraint | 0.53899226 | 0.53899554 |
| Predicted matched minus unchanged explicit wave | 0.82686216 | 0.60661516 |
| Saved matched minus unchanged explicit wave | 0.82686361 | 0.60661517 |

The last two rows subtract complex histories before taking the norm. On the fine step the independent energy and current gaps are **0.606848% and 0.605804%**. Neither passes the unchanged 0.5% comparison. Both total correction routes at both gravity steps remain below **0.163% of the original joint launch**. Photon time and angular controls pass; the matched result is stable across the two gravity steps, whereas the difference including the reference is not. This is a consistency test on the retained simulation, not a comparison with new observations. [Photon comparisons](evidence-001.zip) (archive member: `prediction-tests.csv`) · [original acceptance tests](evidence-001.zip) (archive member: `branch-gates.csv`) · [refinements](evidence-001.zip) (archive member: `refinements.csv`).

## How the independent prediction works

We reconstructed the saved trajectory from the original entry preparation and the saved 77-bin stress, rather than recomputing the scattering bank. The archived potential, lapse, heavy energy/current and complete final matter state reproduced exactly on both clocks. For each of 1,156 coarse or 2,312 fine cells we initialized **only from its left matter state**, then integrated 12 energy- and momentum-carrying variables from the retained evolution equations with independent fourth-order Runge–Kutta steps. Both potentials inside a step are computed algebraically from the trial matter state, the shear and the prescribed sources. The saved right-hand values are used only for scoring or as the **next** cell's initial condition. This is a local prediction conditional on the saved background, higher quadrupoles I₂ and N₂, 77-bin stress, external work/drive and switch preparation, not an independent forecast of those inputs or a continuous free-running trajectory. The cold history and explicit reference were reused, not re-evolved.

Write DΦ=N, with N=U−E/2−3HJ/(2k²). For each sector write N_g=C_g·x+S_g, where S_g is its explicit numerator input. With predicted matter change δx and arithmetic endpoint means, the exact finite-step rule is

    δN_g = mean(C_g)·δx + δC_g·(x_left+δx/2) + δS_g
    δΦ_g = [δN_g − (N_g,left/D_left) δD] / D_right.

We computed the longitudinal rate independently inside the step, P=J/(2k²)−HΨ+Fq, accumulating its impulse together with the matter solution. The signed residual is ΣδΦ_g−∫P. No observed ΔΦ or measured sector derivative enters the right-hand side. First we kept the archived ∫P as a control, then used the independently evaluated impulse. Explicit numerator work, work driving the states, changing background coefficients and the changing denominator are not interchangeable.

The maximum rate error of the independent potential increment relative to the peak observed potential-increment rate was **0.0000998% coarse / 0.00000140% fine**. Against the much smaller *peak discrepancy rate*, the error of the independently predicted balance was **0.0238% / 0.00339%**. These are peak-normalized comparisons, not claims about percentage error at a zero crossing. The photon projection also resolved each gravity cell in halves and quarters without resetting the intermediate matter state; source corners were split explicitly. Cell means were integrated with the original two photon-stage weights and the changing visibility, not equal endpoint weights. [Coarse cell diagnostics](evidence-001.zip) (archive member: `local-check-p16.json`) · [fine cell diagnostics](evidence-001.zip) (archive member: `local-check-p32.json`) · [independent matter equations](evidence-001.zip) (archive member: `matter_product.py`) · [within-cell checks](evidence-001.zip) (archive member: `interior_product.py`).

## What the source split rules out

The signed source ledger closes, but several terms are larger than the net and cancel. On the fine step the signed projections along the net matched vector are +1.961 geometry, +13.479 photon, −2.831 collisionless, +9.573 cold, −28.926 baryon, negligible slow field and +7.744 heavy: the unrounded sum is one. These are **not** fractions of observed energy or evidence that the baryons are faulty. The numerator-work split is recorded separately from this sector split. [Full signed ledger](evidence-001.zip) (archive member: `signed-terms.csv`).

There is a useful exact cancellation before any projection: with r=e_b/e_γ, b_t=(W−B)/(r+4/3) and j_γ=B+4b_t/3, the photon–baryon state current is e_γ j_γ+e_b b_t=e_γ W. The internal slip B also cancels in the combined density-state rate and the equation for W. At fixed background the latter still contains external momentum work proportional to opacity times (C_b−C_ph); the former still receives the retained heat term. All three identities hold on both saved histories and after independently perturbing B at fixed W, with worst peak-relative difference below 6.2×10⁻¹⁶. This excludes **explicit internal slip as an extra net exchange term**; it does not exclude indirect effects through the evolved states, photon quadrupole, or external work. [Pair checks](evidence-001.zip) (archive member: `paired-matter.csv`).

**Next:** test the total energy and longitudinal-momentum balance with photon and baryon exchange combined analytically. Derive the change in the frozen geometric source U required by those balances, then compare it with the independently saved U change, cell by cell and with the photon weights. Keep both values separate: replacing U with the value inferred from the discrepancy would fit the gap by construction. No new interval or fit is needed.

[Fixed protocol](PROTOCOL.md) · [state reconstruction](evidence-001.zip) (archive member: `inputs_product.py`) · [photon projection](evidence-001.zip) (archive member: `photon_product.py`) · [verification](evidence-001.zip) (archive member: `verify_product.py`).
