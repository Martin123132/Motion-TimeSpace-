# Third-cell refinement and localized next calculation

Completed locally2026-11-09. Parent histories and1022old samples are reused;1020new odd samples give1025MTS and1017baseline source points. Original bank, physical histories/grids, G192,256-angle primitive, preparation, algebra1e-10 and numerical gate2e-5 remain unchanged.

## Results

MTS passes16/20 controls, versus18/20 before refinement. Pi and delta_massless fail source-quadrature/conditional-budget controls in BOTH GR and Poisson-spatial branches. All phase, current, mapping, clock and adjoint controls pass. Baseline remains0/20 on the same relative controls.

Largest cumulative three-cell contribution:8.308366803403354e-7 of the saved observable scale (0.830836680ppm); conditional budget8.312254409271687e-7. Baseline contribution1.15459223925657e-13; conditional budget1.2141499423961528e-13. These are ONE background-source term, not total errors or fit scores.

Accumulation uses the SECOND-CELL two-cell total plus the refined third cell, without reset or double counting. New coarse/coarser integrals reproduce old fine/coarse bitwise. The primary independent audit verifies4history controls,40cell and40cumulative cases,1022reused and1020new samples, and2042phase controls.

## Derived localization

Final subtraction/dot-product repair does not cure the MTS flags: compensated integrals change by at most1.372e-16 of their conditional source budgets. Massless monopole/quadrupole native coordinates92/94 dominate the unresolved refinement change.

The exact sum law from the inherited native fluid equations is now derived and checked at every saved point for both models. It separates monopole transfer from clock damping. The MTS discrepancy overwhelmingly follows the former; clock damping and the tested rate representation residual are far smaller. See MASSLESS-SOURCE-DERIVATION.md.

This localization does not promote any failed accuracy flag to a pass. It gives a specific direct metric-source calculation rather than another blind grid refinement.

## Evidence

- audit/result.json: primary continuation/integration audit, completed BEFORE the supplemental attribution.
- balanced/quadrature-diagnosis-01/result.json: integration flags and no-blind-doubling decision.
- balanced/source-attribution-01/result.json: saved-node attribution and40exact contraction spot checks.
- balanced/massless-identity-02/result.json: source-derived identity plus independent weight/attribution checks.
- IDENTITY-ADAPTER-REPAIR.md: first supplemental verifier wrongly assumed trapezoidal weights; it failed before physics testing. The failed attempt is preserved; version2 checks the correct original quadratic weights without relaxing gates.
- closeout.json and CLEANUP.json: final artifact-integrity and exact process-exit records, once sealed.

No new physical evolution, source replacement, fit, GitHub action, compiler or subagent. Previous stages remain intact.

