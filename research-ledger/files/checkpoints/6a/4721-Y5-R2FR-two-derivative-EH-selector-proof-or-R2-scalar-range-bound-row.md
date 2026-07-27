# 4721 - Two-Derivative EH Selector Proof or R2 Scalar Range Bound Row

Generated: `2026-07-07T21:46:40+00:00`

## Purpose

4720 sharpened the local left-hand problem to an EH-selector fork. 4721 tries the proof first and refuses the cheap version:

- covariance alone does not derive EH;
- the strict two-derivative/no-extra-slot IR selector does force EH;
- if that selector is not parent-signed, the first fallback is an `R2/f(R)` scalar finite-range row.

## Proof Result

The conditional proof works:

If the parent local geometry object language has one observed metric/coframe, local covariant parity-even bulk terms, a two-derivative IR selector, algebraic/silent torsion/nonmetricity, and no scalar/vector/disformal/memory/source coefficient targets, the bulk principal operator is EH plus `Lambda`, topological and boundary terms.

The unconditional proof fails:

Diffeomorphism covariance by itself allows `R^2`, `R_mu_nu R^mu_nu`, `C^2`, scalar-tensor terms, vector selectors, torsion/nonmetricity, nonlocal/memory kernels and source-boundary terms.

So the exact route is not dead, but it must be signed as a parent object-language theorem.

## Proof Rows

- `TDEH4721_0_object_language`: Assume the local visible geometry object language contains exactly one observed coframe/metric, a compatible connection that is algebraic or Levi-Civita in the compact spinless branch, the volume form, constants, and fixed boundary/topological data. Result: `operator_domain_restricted`.
- `TDEH4721_1_two_derivative_count`: At two bulk derivatives, the only parity-even scalar density built from the metric/coframe and compatible connection that contributes to second-order metric equations is sqrt(-g)R, plus a zeroth-order Lambda density and fixed boundary/topological terms. Result: `EH_principal_block_forced_if_two_derivative_selector_signed`.
- `TDEH4721_2_Palatini_to_EH`: The first-order EC/Palatini form collapses to the EH metric equation when the connection equation is algebraic and torsion/nonmetricity vanish or are separately bounded. Result: `Palatini_selector_reduces_to_EH_conditionally`.
- `TDEH4721_3_covariance_alone_rejected`: Diffeomorphism covariance alone does not prove EH. Result: `exact_EH_not_derived_from_covariance_alone`.
- `TDEH4721_4_verdict`: The two-derivative EH selector is proved as a sufficient theorem, but the existing parent action has not yet signed every premise. Result: `conditional_proof_plus_R2_fallback`.

## Failure Modes

- `FAIL4721_0_R2_fR`: four-derivative curvature scalar allowed -> R2/f(R) scalar finite-range mode -> `R2_scalar_row`.
- `FAIL4721_1_Ricci_Weyl`: quadratic spin-2/tidal curvature operators allowed -> gamma/xi/wave-sector residual -> `Ricci_Weyl_matrix_row`.
- `FAIL4721_2_torsion_Q`: connection has independent propagating torsion/nonmetricity -> preferred-frame/clock/WEP residual -> `torsion_nonmetricity_row`.
- `FAIL4721_3_scalar_vector_slot`: parent admits independent scalar/vector selector -> R10/Gdot/alpha_i/xi residual -> `scalar_vector_rows`.
- `FAIL4721_4_disformal_metric`: matter/source sees second metric or disformal slot -> WEP/gamma/clock residual -> `c_D_bdis_row`.
- `FAIL4721_5_memory_nonlocal`: local collar admits Gamma/memory/nonlocal kernel -> range/local leakage residual -> `c_Gamma_row`.
- `FAIL4721_6_boundary_source`: boundary/corner data creates source-dependent bulk charge -> source normalization/orbital/alpha3 residual -> `c_bdy_row`.

## R2 / f(R) Scalar Fallback

- `R2F4721_0_scalaron_contract`: `Phi(r)=-G_eff M/r [1 + alpha_R exp(-r/lambda_R)]`; R10: `for every lambda_R row: abs(alpha_R_predicted(lambda_R)) <= alpha_bound(lambda_R), using full source-backed bound curve, not anchor-only.`.

For pure metric `R+a_R2 R^2`, use the scalaron contract:

`m_R^2 = 1/(6 a_R2)`, `lambda_R = hbar/(m_R c)`, and `Phi(r)=-G_eff M/r [1+alpha_R exp(-r/lambda_R)]`.

For the pure universal case `alpha_R=1/3`; for a general parent source normalization, keep `alpha_R=(1/3) zeta_R^2` until `zeta_R` is derived or bounded.

## Projection Contracts

- `R2P4721_0_R10_curve` / `R10_fifth_force`: abs(alpha_R)<=alpha_bound(lambda_R) Blocker: full digitized/source-backed curve required; no anchor-only claim.
- `R2P4721_1_gamma_slip` / `gamma_minus_1`: abs(gamma-1) below gamma bound in same PPN convention Blocker: screening/range/profile must be stated, not assumed.
- `R2P4721_2_beta_nonlinear` / `beta_minus_1`: abs(beta-1) below beta bound Blocker: separate second-order source-normalized row required.
- `R2P4721_3_Poisson_source` / `epsilon_N_density`: fractional source residual below Newton/Poisson tolerance Blocker: density-region normalization and boundary terms required.
- `R2P4721_4_orbital_range` / `orbital_precession_or_inverse_square`: range-dependent acceleration residual below orbital bound Blocker: finite-size/shell profile required.

## Gates

- `GATE4721_0_parent_selector_signed`: passed=False; blocker=`PARENT_SELECTOR_UNSIGNED`.
- `GATE4721_1_covariance_not_enough`: passed=False; blocker=`COVARIANCE_ONLY_REJECTED`.
- `GATE4721_2_R2_row_filled`: passed=False; blocker=`R2_NUMERIC_OR_ZERO_MISSING`.
- `GATE4721_3_R10_curve_available`: passed=False; blocker=`R10_FULL_CURVE_REQUIRED`.
- `GATE4721_4_gamma_beta_same_convention`: passed=False; blocker=`PPN_CONVENTION_UNFILLED`.

## Source Register

- `SRC4721_0`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4720_EH_SELECTOR_THEOREM_ROWS.csv`; exists=True; needle_found=True; role=4720 conditional EH selector theorem to sharpen.
- `SRC4721_1`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4720_PARENT_EH_SIGNATURE_CLAUSES.csv`; exists=True; needle_found=True; role=Two-derivative IR clause whose proof/rejection is the target.
- `SRC4721_2`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4720_NONEH_OPERATOR_COEFFICIENT_MATRIX.csv`; exists=True; needle_found=True; role=R2/f(R) fallback row selected if two-derivative selector is unsigned.
- `SRC4721_3`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4720_NONEH_PROJECTION_KERNEL_ROWS.csv`; exists=True; needle_found=True; role=R10 projection contract for range-dependent scalar fallback.
- `SRC4721_4`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4719_PPN_RESIDUAL_VECTOR_ROWS.csv`; exists=True; needle_found=True; role=Gamma PPN residual row that R2 scalar feeds.
- `SRC4721_5`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4719_PPN_RESIDUAL_VECTOR_ROWS.csv`; exists=True; needle_found=True; role=Beta PPN residual row that R2 scalar can feed at nonlinear order.
- `SRC4721_6`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_Y5_R2FR_4719_POISSON_RESIDUAL_BOUND_ROWS.csv`; exists=True; needle_found=True; role=Poisson residual bound that non-EH scalar source modifies.
- `SRC4721_7`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\R11_nonEH_operator_vector_executable.csv`; exists=True; needle_found=True; role=Existing skeleton row for R2/f(R) scalar coefficient, currently nonclaim.
- `SRC4721_8`: `D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work\source-intake\mts_residuals\P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv`; exists=True; needle_found=True; role=Scorecard rows showing non-EH potential feeds gamma/beta/R10/R11.

## Decision

`TWO_DERIVATIVE_EH_SELECTOR_PROVED_CONDITIONAL_COVARIANCE_ALONE_REJECTED_R2_ROW_STAGED_NONCLAIM`

## Next Target

`4722-Y5-R2FR-parent-two-derivative-signature-insertion-or-R2-alpha-lambda-runner.md`
