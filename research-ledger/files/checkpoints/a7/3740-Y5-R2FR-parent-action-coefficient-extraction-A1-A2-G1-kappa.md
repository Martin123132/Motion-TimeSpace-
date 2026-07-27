# 3740 - Parent Action Coefficient Extraction: A1, A2, G1, kappa

## Status
- `GN_CALIBRATED_CLOSURE_AND_PPN_OKM_BOUND_FOUND_PARENT_A2_KAPPA_MISSING`
- The corpus supports a calibrated-GR closure route, not yet a parent-owned derivation of `G_N` or `A2=A1^2`.
- This checkpoint separates useful local-GR reduction evidence from still-missing parent coefficients.

## Extracted Coefficient Ledger
- `A1` `CONVENTION_DEPENDENT_FIRST_ORDER_MATCH_ONLY`: A1=1 if X=Phi/c^2; A1=1/2 if X=Gamma_kappa=-2Phi/c^2 with g00=-(1-X) | next: choose parent variable X and extract from the actual matter metric rather than GR template
- `A2` `MISSING_PARENT_2PN_EXPANSION`: no source-owned A2 found; if X=Gamma_kappa clock ansatz gives no X^2 metric term, which would not prove beta=1 | next: derive 2PN parent matter metric or keep beta row closure-only
- `G1` `GR_TEMPLATE_FIRST_ORDER_MATCH_ONLY`: G1=A1 follows only if the Schwarzschild/Newtonian weak-field template is adopted | next: extract spatial metric from parent covariance map
- `kappa_X` `CALIBRATED_GR_COUPLING_PRESENT_NOT_PARENT_DERIVED`: macroscopic action uses kappa=8*pi*G/c^4; no independent kappa_X sourced from ψ/X equation | next: either derive K_m/Z_X from parent action or label G_N as calibrated closure
- `Z_X` `PSI_KINETIC_NORMALIZATION_PRESENT_NOT_X_SOURCE_NORM`: ψ kinetic terms exist with canonical-looking coefficients, but they are not a sourced quasi-static X kinetic norm | next: derive the quasi-static X reduction of ψ and its elliptic operator norm
- `K_m` `STANDARD_MATTER_COUPLING_PRESENT_NO_X_COEFFICIENT`: standard L_matter/T_munu coupling exists; no parent-owned K_m multiplying X or ψ source was found | next: extract explicit source functional coefficient from matter coupling
- `unit_factor_CG` `PARTIAL_C_AND_KAPPA_CONVENTIONS_PRESENT`: c factors and kappa=8*pi*G/c^4 are present, but the X-to-SI unit factor is not defined | next: state whether X is Phi/c^2, Gamma_kappa, psi covariance, or another normalized potential
- `weak_field_gauge` `GR_WEAK_FIELD_TEMPLATE_PRESENT`: Schwarzschild/Newtonian weak-field gauge is quoted and can be used for closure comparisons | next: derive or declare the map from parent coordinates to standard PPN gauge

## Calibrated-GR Closure Route
- `CL3740_0_base_equation` `CLOSURE_ROUTE_SOURCE_BACKED`: G_{mu nu} + S g_{mu nu} = kappa T_{mu nu}, kappa=8*pi*G/c^4 | When S->0 the macroscopic equations reduce to GR with calibrated G.
- `CL3740_1_newton` `CALIBRATED_CLOSURE_NOT_DERIVATION`: G_N_eff_local = G_calibrated + O(S) | Newton's constant is not derived here; it is inherited from the calibrated Einstein-Hilbert coupling.
- `CL3740_2_ppn_bound` `BOUND_ROUTE_SOURCE_BACKED_OPERATOR_CONSTANTS_OPEN`: |gamma-1|, |beta-1| = O(K^m); with K_solar≈1e-61 and m>=2, residual scale <<1e-122 up to operator constants | This gives a local suppression route if the S≈K^m statement is upheld and the base metric is GR.
- `CL3740_3_parent_route` `PARENT_ROUTE_BLOCKED`: A2=A1^2 and 4*pi*G_N=A1*kappa_X remain unproved by corpus extraction | The stricter parent route remains open; closure does not replace it.

## Fill Rows
- `G_N_eff` `READY_AS_CALIBRATED_CLOSURE_NOT_DERIVATION`: G_calibrated plus local O(S) correction | Moved from unknown to calibrated closure: source-backed by kappa=8*pi*G/c^4, not parent-derived.
- `C_beta_2PN` `BOUND_SCHEMA_READY_CONSTANT_OPEN`: C_beta_S*K^m under calibrated-GR closure; parent A2/A1^2 route still missing | Provides a local bound route but not a parent coefficient proof of A2=A1^2.
- `gamma_MTS-1` `BOUND_SCHEMA_READY_CONSTANT_OPEN`: C_gamma_S*K^m under calibrated-GR closure | First-order gamma is bounded by weak-curvature suppression if the GR base metric is adopted.
- `A2` `BLOCKED_PARENT_ROUTE`: MISSING_PARENT_2PN_EXPANSION | No extracted parent-owned A2; beta zero theorem remains future work.

## Evidence Rows
- `E3740_0_metric_covariance` `metric emergence`: D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\action-principle\the-motion-timespace-action-principle.md:77 | supports emergent metric from ψ covariance but does not normalize local Newtonian potential
- `E3740_1_action_kappa` `source coupling`: D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\action-principle\the-motion-timespace-action-principle.md:29 | shows G is inserted/calibrated in the macroscopic action
- `E3740_2_matter_lagrangian` `matter coupling`: D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\action-principle\the-motion-timespace-action-principle.md:122 | standard metric matter coupling is present; no independent K_m to X is extracted
- `E3740_3_curvature_exchange` `curvature exchange`: D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\action-principle\the-motion-timespace-action-principle.md:131 | curvature exchange is tied to the same calibrated κ
- `E3740_4_psi_action` `microscopic action`: D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\action-principle\the-fundamental-action-of-motion-timespace-field-theory.md:32 | ψ action is present but has no explicit matter source coefficient K_m
- `E3740_5_psi_equation` `microscopic equation`: D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\action-principle\the-fundamental-action-of-motion-timespace-field-theory.md:36 | free ψ equation provides kinetic normalization but no sourced Poisson equation for X
- `E3740_6_gr_limit` `local closure`: D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\action-principle\the-fundamental-action-of-motion-timespace-field-theory.md:170 | if correction vanishes, local equations inherit GR
- `E3740_7_weak_metric` `weak-field gauge`: D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\relativity\time-as-thermodynamic-exchange-in-motion-timespace-a-unified-framework-for-relativity-and-thermodynamics.md:69 | Schwarzschild/Newtonian gauge template supplies first-order g00/spatial metric comparison
- `E3740_8_gamma_kappa` `clock potential map`: D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\relativity\time-as-thermodynamic-exchange-in-motion-timespace-a-unified-framework-for-relativity-and-thermodynamics.md:91 | Γ_kappa is identified with -2Φ/c², fixing only a convention-dependent first-order map
- `E3740_9_source_placeholder` `source placeholder`: D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\relativity\time-as-thermodynamic-exchange-in-motion-timespace-a-unified-framework-for-relativity-and-thermodynamics.md:131 | matter source functional is named but no coefficient is given
- `E3740_10_ppn_gamma` `PPN closure`: D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\gravity\motion-timespace-mts-gravity.md:193 | corpus asserts weak-curvature gamma residual is order K^m
- `E3740_11_ppn_beta` `PPN closure`: D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\gravity\motion-timespace-mts-gravity.md:194 | corpus asserts weak-curvature beta residual is order K^m
- `E3740_12_solar_K` `local bound scale`: D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\gravity\motion-timespace-mts-gravity.md:185 | corpus supplies a solar-system curvature scale for the closure route
- `E3740_13_S_small` `local bound scale`: D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\gravity\motion-timespace-mts-gravity.md:189 | corpus supplies the weak-curvature suppression size when m>=2
- `E3740_14_G_eff` `effective Newton closure`: D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\core-mts-framework\gravity\motion-timespace-mts-gravity-core-unified-formulation.md:159 | effective G is written as a modulation of calibrated G, not a derivation of G

## Theorem Rows
- `THM3740_0_kappa_audit` `CALIBRATION_RESULT`: The corpus supplies kappa=8*pi*G/c^4 in the macroscopic action, so G_N is currently calibrated/inserted, not derived from parent coefficients. | This answers the Newton-constant question cleanly.
- `THM3740_1_ppn_closure` `CONDITIONAL_BOUND_ROUTE`: If the base equation is GR plus S g_mu_nu and S=O(K^m), then local PPN deviations are inherited as O(K^m) corrections around GR. | This is a legitimate local closure route, but it depends on the S functional and operator constants.
- `THM3740_2_parent_gap` `PARENT_DERIVATION_GAP`: The corpus does not yet provide source-owned A2 or kappa_X=K_m/Z_X for the parent-owned beta/G_N derivation route. | The strict derivation ladder remains unfinished.
- `THM3740_3_variable_choice` `NORMALIZATION_WARNING`: A1 is convention-dependent until X is fixed; X=Phi/c^2 and X=Gamma_kappa give different A1 values. | This prevents a fake coefficient extraction from a naming choice.
- `THM3740_4_claim_gate` `ANTI_OVERCLAIM`: 3740 promotes G_N only to calibrated closure and PPN only to a bound schema; no local-GR proof is claimed. | Private discipline stays intact.

## Decisions
- `DEC3740_0_result` `SPLIT_PARENT_DERIVATION_FROM_CALIBRATED_GR_CLOSURE` | This avoids throwing away useful local-GR reduction evidence while staying honest about what is not parent-derived.
- `DEC3740_1_gn` `G_N_CURRENTLY_CALIBRATED_NOT_DERIVED` | The corpus uses the standard Einstein-Hilbert coupling; deriving G_N requires a deeper A1*K_m/Z_X calculation not yet present.
- `DEC3740_2_ppn` `PPN_ROUTE_NOW_BOUND_SCHEMA` | Existing MTS gravity notes support a local O(K^m) residual route, which should be formalized as a theorem with constants.
- `DEC3740_3_next` `NEXT_PROVE_LOCAL_GR_CLOSURE_BOUND` | The best next step is proving the S g_mu_nu perturbation bound from the field equation, then linking it to beta_NP coefficients.

## Next Target
- `3741-Y5-R2FR-local-GR-closure-bound-from-Sgmunu-perturbation.md`
- Objective: prove the calibrated-GR closure theorem: from G_mu_nu + S g_mu_nu = kappa T_mu_nu with S=O(K^m), derive Newton/PPN residual bounds and map them into the 3738 beta_NP ledger
