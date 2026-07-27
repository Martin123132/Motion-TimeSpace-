from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3556-Y5-R2FR-source-normalization-even-scalar-owner-or-q_loc-R11-coefficient-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_SOURCE_NORMALIZATION_RENORMALIZED_G_3556"
CHECKPOINT_ID = "3556"


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_paths() -> dict[str, Path]:
    return {
        "handoff_3555": RESIDUALS / "P8_Y5_R2FR_3555_NEXT_TARGET.csv",
        "hard_rows_3555": RESIDUALS / "P8_Y5_R2FR_3555_Y5_Y6_HARD_ROW_AUDIT.csv",
        "hard_rows_parent": RESIDUALS / "P8_EXCHANGE_COMPONENT_HARD_ROWS.csv",
        "map_score": RESIDUALS / "P8_EXCHANGE_COMPONENT_MAP_SCORE.csv",
        "coefficient_branch": RESIDUALS / "P8_EXCHANGE_COMPONENT_COEFFICIENT_BRANCH.csv",
        "yloc_euler": RESIDUALS / "P8_YLOC_EULER_SYSTEM.csv",
        "owner_theorem_518": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv",
        "even_scalar_gate_518": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_EVEN_SCALAR_GATE.csv",
        "bound_runner_518": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv",
        "scorecard_523": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
        "r11_minimum_fill": RESIDUALS / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv",
        "r11_acceptance": RESIDUALS / "P8_R11_SOURCE_NORMALIZATION_ACCEPTANCE_GATES.csv",
        "source_norm_2594_stack": RESIDUALS / "P8_Y5_SOURCE_NORM_2594_THEOREM_STACK.csv",
        "source_norm_2594_channels": RESIDUALS / "P8_Y5_SOURCE_NORM_2594_CHANNEL_VECTOR.csv",
        "source_pref_2632_rollforward": RESIDUALS / "P8_Y5_SOURCE_PREF_GR_ROLLFORWARD_2632_SOURCE_COUPLING_ROLLFORWARD.csv",
        "source_pref_2632_residuals": RESIDUALS / "P8_Y5_SOURCE_PREF_GR_ROLLFORWARD_2632_RESIDUAL_OWNER_LEDGER.csv",
    }


def build_source_register(sources: dict[str, Path]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, path in sources.items():
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "role": {
                    "handoff_3555": "declares 3556 target and Y5 success gate",
                    "hard_rows_3555": "states Y5 measured-GM hard row inherited from 3555",
                    "hard_rows_parent": "root hard-row source for exchange-even measured GM",
                    "map_score": "records why exchange oddness cannot erase Y5",
                    "coefficient_branch": "maps Y5 to R11/source-normalization coefficient branch",
                    "yloc_euler": "defines Y5 Euler residual L_mu Delta_mu=J_mu",
                    "owner_theorem_518": "older theorem stack for source-normalization ownership",
                    "even_scalar_gate_518": "records even-scalar guard and bound trigger",
                    "bound_runner_518": "lists source-normalization bound channels",
                    "scorecard_523": "residual scorecard for measured-GM/source channels",
                    "r11_minimum_fill": "minimum R11 coefficient vector",
                    "r11_acceptance": "claim gates preventing fake Newton pass",
                    "source_norm_2594_stack": "latest theorem stack for Y5/source normalization",
                    "source_norm_2594_channels": "latest channel vector for Y5/source normalization",
                    "source_pref_2632_rollforward": "source-coupling rollforward and Hilbert source status",
                    "source_pref_2632_residuals": "residual owner ledger for EH/kappa/R11/coframe leaks",
                }[source_id],
                "valid_for_claim": False,
            }
        )
    return rows


def build_theorem_rows(sources: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "RG3556_0_measured_source_split",
            "name": "measured source split",
            "statement": "The observed weak-field source strength can be decomposed as mu_obs=G0 M_H[Pi_M J_H](1+epsilon_abs+sum_i epsilon_i), with epsilon_i carrying radial, time, range, species, frame, boundary, domain, non-EH, and q_loc source-normalization channels.",
            "derivation": "Start from the weak static Gauss law r^2 Phi'(r)=G0 times the enclosed Hilbert charge plus every non-EH/source-normalization monopole contribution. Divide by G0 M_H to define dimensionless epsilon channels rather than hiding them inside fitted GM.",
            "what_this_closes": "turns the even-scalar Y5 blocker into a concrete residual vector instead of an undefined objection",
            "required_parent_premises": "same observed coframe, parent Hilbert charge Pi_M J_H, compact source exterior, and channel decomposition",
            "status": "EXACT_DECOMPOSITION_CONDITIONAL_ON_CHANNEL_BASIS",
            "source_path": str(sources["owner_theorem_518"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "RG3556_1_constant_G_renormalization",
            "name": "constant universal offset is not a local-GR failure",
            "statement": "If epsilon_abs is constant, universal, positive, source-blind, range-blind, species-blind, frame-blind, and derivative-free, then define G_N=G0(1+epsilon_abs). First-order Newton and source-normalized local GR tests are unchanged by this absolute offset.",
            "derivation": "In the acceleration law a_r=-mu_obs/r^2, a constant universal factor multiplying all sources is operationally the empirical Newton coupling. Local tests constrain derivatives, species/range dependence, preferred-frame pieces, and higher-order operator residues, not the bare numerical value of G0.",
            "what_this_closes": "removes the false requirement that MTS must derive the numerical value of Newton's constant before reducing to GR/Newton",
            "required_parent_premises": "epsilon_abs has no t, r, lambda, species, frame, or branch dependence and uses the same matter/orbit coframe",
            "status": "EXACT_CONDITIONAL_RENORMALIZATION_THEOREM",
            "source_path": str(sources["r11_acceptance"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "RG3556_2_derivative_hair_law",
            "name": "source-normalization derivative hair law",
            "statement": "For any probe derivative D in {partial_t, partial_r, partial_lambda, partial_species, partial_frame}, D ln(mu_obs)=D ln(G0)+D ln(M_H)+D ln(1+epsilon_abs+sum_i epsilon_i). A constant epsilon_abs drops out; all nonconstant epsilon_i remain testable.",
            "derivation": "Take the logarithmic derivative of the measured source split. The first-order residual is D ln(mu_obs)=D ln(G0 M_H)+sum_i D epsilon_i+O(epsilon^2), so derivative hair cannot be absorbed into one fitted GM value.",
            "what_this_closes": "converts Y5 from all-or-nothing source normalization into observable derivative/range/species tests",
            "required_parent_premises": "small residual expansion or exact log derivative; no tuned cancellation between independent channels",
            "status": "EXACT_DIFFERENTIAL_IDENTITY",
            "source_path": str(sources["scorecard_523"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "RG3556_3_Gauss_nohair_condition",
            "name": "Gauss/no-hair exterior condition",
            "statement": "A clean inverse-square Newton branch follows if the exterior projected source current is closed and all finite-range/non-EH source tails vanish outside compact support; otherwise radial or range hair enters R10/R11.",
            "derivation": "Integrate the exterior weak-field equation over nested spheres. If d(Pi_M J_H)=0 and no exterior extra density/operator tail is present, the enclosed charge is radius-independent and Phi'=G_N M/r^2. Any nonzero exterior tail produces partial_r ln(mu_obs) or alpha(lambda).",
            "what_this_closes": "identifies the exact route to first-order Newton without demanding epsilon_abs=0",
            "required_parent_premises": "closed Hilbert flux, compact support, no bulk Yukawa/nonlocal tail, and same-frame orbital readout",
            "status": "EXACT_CONDITIONAL_GAUSS_THEOREM",
            "source_path": str(sources["source_norm_2594_stack"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "RG3556_4_PPN_not_first_order",
            "name": "Newton pass is not full local-GR pass",
            "statement": "Even after G_N renormalization and first-order Gauss closure, local GR still requires non-EH operator residues, beta/gamma source residues, preferred-frame pieces, q_loc projection, and T_extra stress to vanish or be bounded.",
            "derivation": "The constant coupling theorem only controls the monopole coefficient in the 1/r potential. PPN terms depend on U^2, vector potentials, anisotropic stress, time variation, and operator response coefficients that are independent of an absolute GM calibration.",
            "what_this_closes": "prevents upgrading a Newton-source fix into a GR claim",
            "required_parent_premises": "second-order weak-field expansion, PPN readout map, q_loc projection, and retained stress ledger",
            "status": "CLAIM_GUARD_EXACT",
            "source_path": str(sources["hard_rows_3555"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def build_channel_rows(sources: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "channel_id": "CH3556_0_absolute_constant",
            "channel": "absolute_calibration_offset",
            "symbol": "epsilon_abs",
            "definition": "constant universal multiplicative offset between bare parent coupling G0 and measured Newton coupling G_N",
            "danger_class": "SAFE_ONLY_IF_UNIVERSAL_CONSTANT",
            "zero_or_pass_condition": "partial_t,r,lambda,A,frame epsilon_abs=0 and same e_obs/q/tau branch",
            "observable_links": "none for local differential tests once absorbed into G_N; still blocks claim to derive numerical G",
            "current_value_or_theorem": "ABSORBABLE_CONSTANT_ONLY_IF_PARENT_UNIVERSAL_NOT_NUMERIC_G_CLAIM",
            "source_path": str(sources["r11_minimum_fill"]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "channel_id": "CH3556_1_radial",
            "channel": "radial_Meff_hair",
            "symbol": "epsilon_radial_Meff",
            "definition": "radius-dependent source strength outside compact support",
            "danger_class": "TESTABLE_HAIR",
            "zero_or_pass_condition": "Gauss/no-hair exterior theorem or profile envelope with radius units",
            "observable_links": "inverse-square Newton; R10; beta source residue; R11",
            "current_value_or_theorem": "MISSING_RADIAL_NOHAIR_THEOREM_OR_NUMERIC_PROFILE",
            "source_path": str(sources["source_norm_2594_channels"]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "channel_id": "CH3556_2_time",
            "channel": "time_drift",
            "symbol": "epsilon_time_drift",
            "definition": "time variation in G_N M_H or source-normalization channels",
            "danger_class": "TESTABLE_HAIR",
            "zero_or_pass_condition": "stationarity/global coupling theorem or Gdot coefficient",
            "observable_links": "Gdot/G; clock/orbital ephemeris drift; R9; R11",
            "current_value_or_theorem": "MISSING_STATIONARITY_THEOREM_OR_TIME_DRIFT_COEFFICIENT",
            "source_path": str(sources["bound_runner_518"]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "channel_id": "CH3556_3_species",
            "channel": "species_source_charge",
            "symbol": "epsilon_species_A",
            "definition": "composition/species dependence of active gravitational source charge",
            "danger_class": "TESTABLE_HAIR",
            "zero_or_pass_condition": "selector-blind source theorem or source-charge vector bound",
            "observable_links": "WEP/source charge; clocks; R1/R2/R11",
            "current_value_or_theorem": "MISSING_SELECTOR_BLIND_SOURCE_THEOREM_OR_SPECIES_CHARGE_VECTOR",
            "source_path": str(sources["source_pref_2632_rollforward"]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "channel_id": "CH3556_4_range",
            "channel": "bulk_X_Yukawa_tail",
            "symbol": "epsilon_bulk_X; alpha(lambda)",
            "definition": "finite-range or nonlocal tail in active source strength",
            "danger_class": "TESTABLE_HAIR",
            "zero_or_pass_condition": "bulk mass-gap/no-pole theorem or sourced alpha(lambda) curve",
            "observable_links": "R10 fifth force; R11; short-range gravity",
            "current_value_or_theorem": "MISSING_BULK_MASS_GAP_THEOREM_OR_ALPHA_LAMBDA_CURVE",
            "source_path": str(sources["r11_minimum_fill"]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "channel_id": "CH3556_5_frame",
            "channel": "frame_calibration_split",
            "symbol": "delta_frame_source",
            "definition": "difference between matter-frame source calibration and gravity/orbital readout frame",
            "danger_class": "TESTABLE_HAIR",
            "zero_or_pass_condition": "same parent pullback for source variation, clocks, photons, and orbital readout",
            "observable_links": "same-frame Newton; clocks; alpha_i; R11",
            "current_value_or_theorem": "MISSING_SAME_FRAME_SOURCE_VARIATION_THEOREM_OR_FRAME_RESIDUAL_BOUND",
            "source_path": str(sources["owner_theorem_518"]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "channel_id": "CH3556_6_domain_boundary",
            "channel": "boundary_domain_projector_mass",
            "symbol": "epsilon_boundary; c_domain_source_normalization_operator",
            "definition": "boundary/domain/projector mass contribution to measured GM",
            "danger_class": "TESTABLE_OR_TOPOLOGICAL_HAIR",
            "zero_or_pass_condition": "no-flux/topological invisible theorem or source-ready coefficient products",
            "observable_links": "alpha1; alpha2; alpha3; xi; beta; Gdot; R11",
            "current_value_or_theorem": "MISSING_BOUNDARY_DOMAIN_PROJECTOR_ZERO_THEOREM_OR_NUMERIC_PRODUCTS",
            "source_path": str(sources["coefficient_branch"]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "channel_id": "CH3556_7_nonEH_q_loc",
            "channel": "nonEH_operator_and_q_loc_source_projection",
            "symbol": "epsilon_nonEH_source; C_qmu q_loc",
            "definition": "non-EH weak-field operator or q_loc stress-divergence projection into source normalization",
            "danger_class": "PPN_AND_OPERATOR_HAIR",
            "zero_or_pass_condition": "EH-only theorem plus q_loc source projection zero, or coefficient vector",
            "observable_links": "gamma; beta; R10; R11; local PPN residual vector",
            "current_value_or_theorem": "MISSING_EH_ONLY_THEOREM_QLOC_PROJECTION_OR_NONEH_OPERATOR_COEFFICIENT_MAP",
            "source_path": str(sources["bound_runner_518"]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def build_coefficient_rows(sources: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": "R11C3556_0_epsilon_abs",
            "r11_family": "source_normalization_operator",
            "channel": "absolute_calibration_offset",
            "coefficient_symbol": "epsilon_abs",
            "coefficient_value_or_theorem": "CONSTANT_RENORMALIZABLE_ONLY_IF_PARENT_UNIVERSAL",
            "units": "dimensionless",
            "normalization": "G_N=G0*(1+epsilon_abs); not a derived numerical G claim",
            "observable_projection": "no local differential projection if all derivative/species/range/frame tests are zero",
            "missing_for_claim": "MISSING_PARENT_FIXED_UNIVERSAL_CALIBRATION_THEOREM",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": "R11C3556_1_radial",
            "r11_family": "source_normalization_operator",
            "channel": "radial_Meff_hair",
            "coefficient_symbol": "epsilon_radial_Meff(r)",
            "coefficient_value_or_theorem": "MISSING_RADIAL_NOHAIR_THEOREM_OR_NUMERIC_PROFILE",
            "units": "dimensionless_profile_with_radius_units",
            "normalization": "epsilon_radial_Meff=Delta_mu_radial/(G_N*M_H)",
            "observable_projection": "partial_r ln(mu_obs); R10 alpha(lambda) if tail has finite range",
            "missing_for_claim": "MISSING_PROFILE_SOURCE_PATH_AND_RADIUS_DOMAIN",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": "R11C3556_2_time",
            "r11_family": "source_normalization_operator",
            "channel": "time_drift",
            "coefficient_symbol": "epsilon_time_drift(t)",
            "coefficient_value_or_theorem": "MISSING_STATIONARITY_THEOREM_OR_TIME_DRIFT_COEFFICIENT",
            "units": "dimensionless_or_per_time_after_projection",
            "normalization": "d ln(mu_obs)/dt = d ln(G_N M_H)/dt + d epsilon_time/dt",
            "observable_projection": "Gdot/G; clock/orbital drift",
            "missing_for_claim": "MISSING_C_GDOT_SOURCE_NORMALIZATION_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": "R11C3556_3_species",
            "r11_family": "source_normalization_operator",
            "channel": "species_source_charge",
            "coefficient_symbol": "epsilon_species_A",
            "coefficient_value_or_theorem": "MISSING_SELECTOR_BLIND_SOURCE_THEOREM_OR_SPECIES_CHARGE_VECTOR",
            "units": "dimensionless_by_species_pair",
            "normalization": "epsilon_species_A=Delta_A mu_obs/(G_N*M_H)",
            "observable_projection": "WEP/source charge and clock composition channels",
            "missing_for_claim": "MISSING_MATERIAL_SOURCE_CHARGE_VECTOR",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": "R11C3556_4_range",
            "r11_family": "source_normalization_operator",
            "channel": "bulk_X_Yukawa_tail",
            "coefficient_symbol": "alpha_X(lambda_X)",
            "coefficient_value_or_theorem": "MISSING_BULK_MASS_GAP_THEOREM_OR_ALPHA_LAMBDA_CURVE",
            "units": "dimensionless_plus_length_scale",
            "normalization": "Delta Phi/Phi_N = alpha_X exp(-r/lambda_X) or declared non-Yukawa kernel",
            "observable_projection": "R10 fifth-force bound curve and source-normalization R11",
            "missing_for_claim": "MISSING_ALPHA_LAMBDA_SOURCE_CURVE_OR_NO_POLE_THEOREM",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": "R11C3556_5_domain_boundary",
            "r11_family": "source_normalization_operator",
            "channel": "boundary_domain_projector_mass",
            "coefficient_symbol": "epsilon_boundary; c_domain_source_normalization_operator",
            "coefficient_value_or_theorem": "MISSING_BOUNDARY_DOMAIN_PROJECTOR_ZERO_THEOREM_OR_NUMERIC_PRODUCTS",
            "units": "dimensionless_or_operator_units_declared",
            "normalization": "epsilon_channel=mu_channel/(G_N*M_H)",
            "observable_projection": "alpha1; alpha2; alpha3; xi; beta; Gdot; R11",
            "missing_for_claim": "MISSING_NO_FLUX_TOPOLOGICAL_INVISIBLE_THEOREM_OR_PRODUCTS",
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": "R11C3556_6_nonEH_q_loc",
            "r11_family": "source_normalization_operator",
            "channel": "nonEH_operator_and_q_loc_source_projection",
            "coefficient_symbol": "epsilon_nonEH_source; C_qmu",
            "coefficient_value_or_theorem": "MISSING_EH_ONLY_THEOREM_QLOC_PROJECTION_OR_NONEH_OPERATOR_COEFFICIENT_MAP",
            "units": "operator_units_declared_by_projection",
            "normalization": "Delta operator/source term divided by 4*pi*G_N*rho_H or PPN source coefficient",
            "observable_projection": "gamma; beta; R10; R11; full q_loc PPN vector",
            "missing_for_claim": "MISSING_PARENT_EH_UNIQUENESS_AND_QLOC_SOURCE_KERNEL",
            "valid_for_claim": False,
        },
    ]


def build_gate_rows(sources: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "G3556_0_G_value",
            "gate": "numerical G is empirical coupling",
            "before_3556": "Y5 appeared to require epsilon_mu=0 including absolute calibration",
            "after_3556": "epsilon_abs may be absorbed into G_N if it is universal constant; MTS still cannot claim to derive G's numerical value",
            "claim_effect": "narrows Y5 from absolute-offset proof to universality/derivative/no-hair proof",
            "status": "IMPROVED_THEOREM_GATE",
            "source_path": str(sources["r11_acceptance"]),
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "G3556_1_Newton_first_order",
            "gate": "source-normalized Newton",
            "before_3556": "measured GM could be an orbital fit",
            "after_3556": "Newton requires same-frame Hilbert/worldtube charge plus no radial/time/range/species/frame hair after G_N renormalization",
            "claim_effect": "first-order inverse-square branch has explicit pass/fail residual vector",
            "status": "CONDITIONAL_NOT_LIVE",
            "source_path": str(sources["source_norm_2594_stack"]),
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "G3556_2_R10_R11",
            "gate": "range/operator source leakage",
            "before_3556": "R10/R11 blocked by generic source-normalization missing row",
            "after_3556": "R10/R11 block is specifically alpha(lambda), non-EH operator coefficient map, and q_loc source projection",
            "claim_effect": "turns one blocker into concrete coefficient targets",
            "status": "COEFFICIENT_TARGETS_READY_NONCLAIM",
            "source_path": str(sources["r11_minimum_fill"]),
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "G3556_3_local_GR",
            "gate": "do not promote Newton to GR",
            "before_3556": "source normalization and PPN source stability were mixed",
            "after_3556": "constant G_N and first-order Gauss closure are only Newton-level; beta/gamma/preferred-frame/q_loc/T_extra remain separate gates",
            "claim_effect": "prevents overclaim while allowing a real Newton route to advance",
            "status": "CLAIM_GUARD_ACTIVE",
            "source_path": str(sources["hard_rows_3555"]),
            "valid_for_claim": False,
        },
    ]


def build_decision_rows(sources: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3556_0",
            "decision": "Do not require MTS to derive the numerical value of G for local GR/Newton reduction.",
            "reason": "GR uses an empirical coupling constant; the real derivation requirement is universality, same-frame coupling, and absence/boundedness of source-normalization hair.",
            "effect": "absolute constant calibration becomes a renormalized-G premise, not an automatic failure",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3556_1",
            "decision": "Y5 is not closed.",
            "reason": "No parent theorem yet proves epsilon_abs universal constant, no radial/range/species/time/frame hair, EH-only operator dominance, q_loc source silence, or second-order PPN stability.",
            "effect": "local GR/Newton source-normalization claim remains disabled",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3556_2",
            "decision": "The next useful derivation is a derivative-hair/no-hair theorem, not another absolute-G audit.",
            "reason": "Once constant G_N is allowed, the observable failure modes are radial, time, range, species, frame, non-EH, and q_loc source projections.",
            "effect": "route moves to 3557 derivative-hair no-hair or executable coefficient bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def build_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STAT3556_0",
            "area": "source-normalization",
            "status": "PARTIALLY_ADVANCED_NOT_CLOSED",
            "summary": "Absolute universal calibration can be absorbed into empirical G_N; nonconstant source-normalization hair remains live and testable.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STAT3556_1",
            "area": "Newton",
            "status": "CONDITIONAL_ROUTE_SHARPENED",
            "summary": "First-order Newton route now requires same-frame Hilbert/worldtube Gauss charge and no derivative/range/species/frame source hair after G_N renormalization.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STAT3556_2",
            "area": "local_GR",
            "status": "STILL_BLOCKED_BY_PPN_QLOC_TEXTRA",
            "summary": "Full local GR still needs beta/gamma/preferred-frame/q_loc/T_extra gates, not just first-order source normalization.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def build_next_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": timestamp(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3556_0",
            "target_doc": "3557-Y5-R2FR-source-normalization-derivative-hair-nohair-or-bound-runner.md",
            "target_script": "scripts/Y5_R2FR_3557_source_normalization_derivative_hair_nohair_or_bound_runner.py",
            "objective": "derive D epsilon_i=0 for radial/time/range/species/frame source-normalization hair from parent Gauss/Noether/same-frame structure; if not, build executable bound rows for Gdot, R10 alpha(lambda), WEP/source-charge, radial profile, and frame residuals",
            "success_gate": "constant G_N is allowed but all nonconstant source-normalization channels are theorem-zero or have source-ready coefficients",
            "reason": "3556 narrows Y5 to derivative/source-hair channels; 3557 must try to kill or score those channels directly",
            "valid_for_claim": False,
        }
    ]


def build_validation_rows(
    sources: dict[str, Path],
    outputs: dict[str, Path],
    theorem_rows: list[dict[str, object]],
    channel_rows: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    missing_sources = [str(path) for path in sources.values() if not path.exists()]
    validation.append(
        {
            "validation_id": "VAL3556_0_sources_exist",
            "passes": not missing_sources,
            "status": "PASS" if not missing_sources else "FAIL",
            "detail": f"{len(sources) - len(missing_sources)}/{len(sources)} cited source paths exist"
            if not missing_sources
            else "; ".join(missing_sources),
        }
    )

    parse_failures: list[str] = []
    for path in outputs.values():
        if path.suffix.lower() == ".csv":
            try:
                read_csv(path)
            except Exception as exc:  # pragma: no cover - explicit validation output
                parse_failures.append(f"{path}: {exc}")
    validation.append(
        {
            "validation_id": "VAL3556_1_generated_csvs_parse",
            "passes": not parse_failures,
            "status": "PASS" if not parse_failures else "FAIL",
            "detail": f"{sum(1 for p in outputs.values() if p.suffix.lower() == '.csv')} generated CSV files parse with DictReader"
            if not parse_failures
            else "; ".join(parse_failures),
        }
    )

    has_g_theorem = any(row["theorem_id"] == "RG3556_1_constant_G_renormalization" for row in theorem_rows)
    validation.append(
        {
            "validation_id": "VAL3556_2_constant_G_theorem_present",
            "passes": has_g_theorem,
            "status": "PASS" if has_g_theorem else "FAIL",
            "detail": "renormalized-G theorem is present and scoped as conditional",
        }
    )

    has_derivative_law = any(row["theorem_id"] == "RG3556_2_derivative_hair_law" for row in theorem_rows)
    validation.append(
        {
            "validation_id": "VAL3556_3_derivative_hair_law_present",
            "passes": has_derivative_law,
            "status": "PASS" if has_derivative_law else "FAIL",
            "detail": "D ln(mu_obs) residual law is present",
        }
    )

    required_channels = {
        "absolute_calibration_offset",
        "radial_Meff_hair",
        "time_drift",
        "species_source_charge",
        "bulk_X_Yukawa_tail",
        "frame_calibration_split",
        "boundary_domain_projector_mass",
        "nonEH_operator_and_q_loc_source_projection",
    }
    present_channels = {str(row["channel"]) for row in channel_rows}
    missing_channels = sorted(required_channels - present_channels)
    validation.append(
        {
            "validation_id": "VAL3556_4_channel_vector_complete",
            "passes": not missing_channels,
            "status": "PASS" if not missing_channels else "FAIL",
            "detail": "source-normalization channels include constant, radial, time, species, range, frame, boundary/domain, and q_loc/non-EH"
            if not missing_channels
            else "; ".join(missing_channels),
        }
    )

    unsafe_claim_rows = [
        row["coefficient_id"]
        for row in coefficient_rows
        if str(row.get("valid_for_claim", "")).lower() == "true"
        or (
            "MISSING_" in str(row.get("coefficient_value_or_theorem", ""))
            and str(row.get("valid_for_claim", "")).lower() != "false"
        )
    ]
    validation.append(
        {
            "validation_id": "VAL3556_5_missing_rows_nonclaim",
            "passes": not unsafe_claim_rows,
            "status": "PASS" if not unsafe_claim_rows else "FAIL",
            "detail": "all coefficient rows remain nonclaim while theorem/numeric inputs are missing or conditional"
            if not unsafe_claim_rows
            else "; ".join(map(str, unsafe_claim_rows)),
        }
    )

    g_gate = next((row for row in gate_rows if row["gate_id"] == "G3556_0_G_value"), None)
    validation.append(
        {
            "validation_id": "VAL3556_6_no_numerical_G_overclaim",
            "passes": bool(g_gate) and "cannot claim to derive G" in str(g_gate["after_3556"]),
            "status": "PASS" if bool(g_gate) and "cannot claim to derive G" in str(g_gate["after_3556"]) else "FAIL",
            "detail": "constant calibration is separated from a claim to derive Newton's constant",
        }
    )

    formalization_touched = False
    if FORMALIZATION.exists():
        new_outputs_under_formalization = [
            str(path)
            for path in outputs.values()
            if FORMALIZATION in path.parents or path == FORMALIZATION
        ]
        formalization_touched = bool(new_outputs_under_formalization)
    validation.append(
        {
            "validation_id": "VAL3556_7_formalization_workbench_untouched",
            "passes": not formalization_touched,
            "status": "PASS" if not formalization_touched else "FAIL",
            "detail": "3556 generated outputs only inside post-checkpoint-work",
        }
    )

    return validation


def write_doc(
    sources: dict[str, Path],
    outputs: dict[str, Path],
    theorem_rows: list[dict[str, object]],
    channel_rows: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> None:
    lines = [
        "# 3556 - Source-normalization even-scalar owner or q_loc/R11 coefficient fill",
        "",
        "## Verdict",
        "3556 makes a real forward move on the coupling problem: MTS does not need to derive the numerical value of Newton's constant to reduce to GR/Newton. The exact requirement is weaker and sharper: the parent theory must supply a universal constant coupling on the local branch, with no radial, time, species, range, frame, non-EH, q_loc, boundary, or domain source-normalization hair.",
        "",
        "The new conditional theorem is: if the only source-normalization offset is a constant universal scalar `epsilon_abs`, then `G_N = G0(1 + epsilon_abs)` is just the empirical Newton coupling. That is not a local-GR failure. The failure modes are the derivatives and operator projections of the remaining `epsilon_i` channels.",
        "",
        "This does not close Y5. It narrows Y5 from a vague measured-GM blocker into a derivative/source-hair theorem or bound-runner problem.",
        "",
        "## Derived spine",
        "- Source split: `mu_obs = G0 M_H[Pi_M J_H] (1 + epsilon_abs + sum_i epsilon_i)`.",
        "- Constant-G renormalization: if `D epsilon_abs = 0` for time, radius, range, species, frame, and branch derivatives, define `G_N = G0(1 + epsilon_abs)`.",
        "- Derivative hair law: `D ln(mu_obs) = D ln(G0 M_H) + D ln(1 + epsilon_abs + sum_i epsilon_i)`; a constant offset drops out but nonconstant channels remain observable.",
        "- Gauss/no-hair condition: closed exterior Hilbert flux plus no finite-range/non-EH tail gives inverse-square Newton after `G_N` calibration.",
        "- PPN guard: first-order Newton source normalization does not imply beta/gamma/preferred-frame/q_loc/T_extra closure.",
        "",
        "## What improved",
        "- We stop treating `derive the numerical value of G` as a required local-GR reduction condition.",
        "- The absolute calibration row is now separated from observable source hair.",
        "- Y5 now has a cleaner next target: prove or bound `D epsilon_i = 0` for the nonconstant channels.",
        "- R10/R11 are tied to specific range/operator coefficients instead of a generic source-normalization complaint.",
        "",
        "## What remains open",
        "- Parent proof that `epsilon_abs` is genuinely universal and constant.",
        "- Parent proof of same observed coframe for matter, source variation, clocks, photons, and orbits.",
        "- Gauss/no-hair proof for radial exterior source strength.",
        "- No-pole or sourced `alpha(lambda)` curve for finite-range tails.",
        "- Species/source-charge blindness, time stationarity, frame silence, non-EH operator dominance, and q_loc source projection.",
        "- PPN beta/gamma/preferred-frame and retained `T_extra` stress gates.",
        "",
        "## Generated outputs",
    ]
    for key, path in outputs.items():
        lines.append(f"- `{key}`: `{rel(path)}`")
    lines.extend(
        [
            "",
            "## Key theorem rows",
        ]
    )
    for row in theorem_rows:
        lines.append(f"- `{row['theorem_id']}`: {row['statement']}")
    lines.extend(
        [
            "",
            "## Channel triage",
        ]
    )
    for row in channel_rows:
        lines.append(f"- `{row['channel_id']}` `{row['symbol']}`: {row['danger_class']} -> {row['current_value_or_theorem']}")
    lines.extend(
        [
            "",
            "## Decision ledger",
        ]
    )
    for row in decision_rows:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} {row['reason']}")
    lines.extend(
        [
            "",
            "## Next target",
            f"- `{next_rows[0]['target_doc']}`",
            f"- Objective: {next_rows[0]['objective']}",
            "",
            "## Source paths",
        ]
    )
    for source_id, path in sources.items():
        lines.append(f"- `{source_id}`: `{path}`")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_paths()
    source_rows = build_source_register(sources)
    theorem_rows = build_theorem_rows(sources)
    channel_rows = build_channel_rows(sources)
    coefficient_rows = build_coefficient_rows(sources)
    gate_rows = build_gate_rows(sources)
    decision_rows = build_decision_rows(sources)
    status_rows = build_status_rows()
    next_rows = build_next_rows()

    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3556_SOURCE_REGISTER.csv",
        "renormalized_G_theorem": RESIDUALS / "P8_Y5_R2FR_3556_RENORMALIZED_G_THEOREM.csv",
        "channel_triage": RESIDUALS / "P8_Y5_R2FR_3556_CHANNEL_TRIAGE.csv",
        "r11_coefficient_targets": RESIDUALS / "P8_Y5_R2FR_3556_R11_COEFFICIENT_TARGETS.csv",
        "gate_update": RESIDUALS / "P8_Y5_R2FR_3556_Y5_GATE_UPDATE.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3556_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3556_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3556_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_source_normalization_renormalized_G_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3556_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["renormalized_G_theorem"], theorem_rows)
    write_csv(outputs["channel_triage"], channel_rows)
    write_csv(outputs["r11_coefficient_targets"], coefficient_rows)
    write_csv(outputs["gate_update"], gate_rows)
    write_csv(outputs["decision_ledger"], decision_rows)
    write_csv(outputs["status"], status_rows)
    write_csv(outputs["next_target"], next_rows)
    write_csv(
        outputs["canonical_status"],
        [
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "canonical_status": "Y5_SOURCE_NORMALIZATION_RENAMED_AS_RENORMALIZED_G_PLUS_DERIVATIVE_HAIR_VECTOR",
                "what_changed": "constant universal source calibration is absorbable into G_N; nonconstant source hair remains the real local-GR/Newton test",
                "claim_allowed": False,
                "valid_for_claim": False,
                "next_target": next_rows[0]["target_doc"],
            }
        ],
    )

    validation_rows = build_validation_rows(
        sources=sources,
        outputs={key: path for key, path in outputs.items() if key != "validation"},
        theorem_rows=theorem_rows,
        channel_rows=channel_rows,
        coefficient_rows=coefficient_rows,
        gate_rows=gate_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        sources=sources,
        outputs=outputs,
        theorem_rows=theorem_rows,
        channel_rows=channel_rows,
        coefficient_rows=coefficient_rows,
        gate_rows=gate_rows,
        decision_rows=decision_rows,
        next_rows=next_rows,
    )

    for path in [DOC, *outputs.values()]:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
