# Dimensional clarification to the frozen derivation

The first paragraph of DERIVATION.md incorrectly assigns Mpc^-1 to z and sigma. Correct conventions are:

- Conformal time tau: Mpc in the retained c=1 convention; scale factor: dimensionless.
- k, H and eta_k: Mpc^-1.
- z=h'/(2k) and sigma: dimensionless.
- B, P, D, T, Q and Pi: Mpc^-2, with the retained gravitational normalization absorbed.
- E_B, E_D and E_Q: Mpc^-3.
- E_eta, C00 and F: respectively Mpc^-2, Mpc^-1 and Mpc^-2.
- R_trace and R_shear: Mpc^-1.

This corrects prose only. All equations, numerical arrays, kernels and gates use the original native definitions and are unchanged. The frozen DERIVATION.md remains byte-preserved because completed numerical workers recorded its hash; read it together with this clarification. check_dimensions.py checks every addition in the constraint, trace/shear and contact identities using powers of length.
