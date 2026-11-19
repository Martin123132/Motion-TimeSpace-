# Follow-through: source energy/momentum balance

The full-grid direct metric-source projection leaves the MTS refinement discrepancy essentially unchanged; its Phi_dot0 term dominates. Do not pursue an arithmetic-only source repair.

Inspection of the retained stress getter reveals a physically specific distinction: the reference side differentiates the scalar background interpolants, whereas the instantaneous retained side uses canonical energy/momentum equations. Next derive the explicit background-flow defect in the scalar stress divergence and test it using ONLY the already-captured primitives. Keep the defect, native baryon approximation and quadrature enthalpy visible rather than assuming conservation or forcing it to hold.

Documentation correction: DERIVATION.md's phrase describing metadata_3 as a scalar enthalpy contribution is incorrect. The actual zero-based metadata[3] is the massive-neutrino quadrature enthalpy integral (4/3 sum weight/velocity). The code has always used the correct table entry and formula. All scalar background data are at zero-based metadata[4:11] and [14:21]. This correction changes no calculation or gate.

