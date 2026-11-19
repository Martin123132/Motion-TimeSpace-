# Frozen integrated-defect experiment

One manual stage; goal paused. Original background/scattering bank, prepared 902 signed nodes, physical grids, nine reporting epochs, parameters and tolerances (numerical2e-5/algebra1e-10) stay fixed. No fits, new observations, handover or publication. New quadrature nodes integrate the existing interpolants; they do not change the field or source grids.

Obtain the exact retained thermo interpolation coefficients and background constants by a private read-only export, preserving original mode order and preparation parity. Reconstruct a,r,r',H,H' from those coefficients and existing slow/heavy natural-cubic tables. No substitution of r=H or independent approximated background conservation is permitted.

Primary prediction: keep the derived initial algebraic remainder R0, but integrate C_b E_b'+C_v E_v' by parts over the actual saved background defects. Use a quadratic time expansion for C from initial equation-owned values/derivatives; linear C is a frozen approximation control. Do not remove E or fit it. Test direct E' quadrature against the integration-by-parts form; split quadrature at exact background and thermo interpolation knots, using orders8/16. Keep original histories and physical grids unchanged.

The assumption R=R0 needs a control: estimate the initial variation of the already defect-subtracted R using fixed6/8-knot past-only differentiation. Do NOT differentiate the noisy original full source rates again. Save the resulting cubic response contributions as diagnostics, not a new fitted coefficient. Include their maximum magnitude as a working allowance on the frozen-R prediction, and report their refinement discrepancy separately. This finite control is not a rigorous bound on all future remainder variation. If the diagnostic itself is unstable at the source gate, retain that failure explicitly rather than silently certifying the prediction.

Freeze all candidates and controls before loading the checked target readout. Compare both cold and MTS. Cold has no heavy defect correction: retain its equation-owned quadratic control and evaluate its remainder-variation diagnostic too. Preserve old first-order and failed quadratic results. All data were previously exposed; this is numerical validation, not observational holdout evidence.

One below-normal worker at a time, one numerical thread, CPU4, guarded900s workers. No changes to other agents or services. All writes confined to this new stage and an additive resume bookmark. Verify exact process exits and old source hashes before the final reply.
