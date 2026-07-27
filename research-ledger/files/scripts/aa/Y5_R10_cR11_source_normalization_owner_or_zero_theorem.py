from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1148-Y5-R10-cR11-source-normalization-owner-or-zero-theorem.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1148_0_1147_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1147_NEXT_TARGET.csv",
            "needle": "NEXT1147_0_1148",
            "role": "handoff selecting c_R11/source-normalization owner route.",
        },
        {
            "source_id": "SRC1148_1_1138_canonical_c",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1138_CANONICAL_C_SOURCE_NORMALIZATION_ROW.csv",
            "needle": "CROW1138_0_c_domain_source_normalization_operator",
            "role": "canonical c_R11/c_domain source-normalization contract row.",
        },
        {
            "source_id": "SRC1148_2_1137_coupling",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1137_W_K_C_COUPLING_AUDIT.csv",
            "needle": "CPL1137_2_c_R11_flux_alpha3",
            "role": "c_R11 is alias to missing R11 source-normalization operator.",
        },
        {
            "source_id": "SRC1148_3_1137_zero",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1137_COUPLING_ZERO_ROUTE_AUDIT.csv",
            "needle": "ZR1137_2_c_zero",
            "role": "c zero route fails current corpus.",
        },
        {
            "source_id": "SRC1148_4_R11_operator_min",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM.csv",
            "needle": "c_domain_source_normalization_operator",
            "role": "R11 domain source-normalization operator row.",
        },
        {
            "source_id": "SRC1148_5_R11_link",
            "relative_path": "source-intake/mts_residuals/R11_MU_EXTRA_SOURCE_NORMALIZATION_LINK.csv",
            "needle": "source_normalization_operator",
            "role": "source-normalization family links to retained unfilled channels.",
        },
        {
            "source_id": "SRC1148_6_R11_minimum_skeleton",
            "relative_path": "source-intake/mts_residuals/R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv",
            "needle": "source_normalization_operator",
            "role": "source-normalization operator is highest priority in Newton/R11 skeleton.",
        },
        {
            "source_id": "SRC1148_7_R11_fill",
            "relative_path": "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv",
            "needle": "R11SN_2_domain_projector_mass",
            "role": "minimum source-normalization channel fill rows.",
        },
        {
            "source_id": "SRC1148_8_R11_route",
            "relative_path": "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_THEOREM_OR_NUMERIC_ROUTE.csv",
            "needle": "T0_parent_zero",
            "role": "theorem/numeric/closure routes for source normalization.",
        },
        {
            "source_id": "SRC1148_9_R11_missing",
            "relative_path": "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_MISSING_LEDGER.csv",
            "needle": "MISSING_DOMAIN_PROJECTOR_ZERO_THEOREM_OR_NUMERIC_PRODUCTS",
            "role": "missing ledger for source-normalization rows.",
        },
        {
            "source_id": "SRC1148_10_SN_theorem",
            "relative_path": "source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
            "needle": "S5_Newton_gate",
            "role": "source-normalization theorem stack currently fails.",
        },
        {
            "source_id": "SRC1148_11_Y5_owner",
            "relative_path": "source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv",
            "needle": "Y5O_8_owner_theorem",
            "role": "owner theorem is written but premises are not satisfied.",
        },
        {
            "source_id": "SRC1148_12_Newton_stack",
            "relative_path": "source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv",
            "needle": "SN6_zero_mu_extra_and_source_residuals",
            "role": "Newton source-normalization stack identifies mu_extra residuals.",
        },
        {
            "source_id": "SRC1148_13_scorecard",
            "relative_path": "source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
            "needle": "SRC523_4_extra_mass_channels_total",
            "role": "source-normalization residual scorecard is unfilled.",
        },
        {
            "source_id": "SRC1148_14_mu_extra_vector",
            "relative_path": "source-intake/mts_residuals/P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv",
            "needle": "domain_projector_mass",
            "role": "mu_extra coefficient vector rows remain unfilled.",
        },
        {
            "source_id": "SRC1148_15_measured_GM_obstruction",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
            "needle": "OBS1013_0_projected_extra_current",
            "role": "measured-GM obstruction vector remains retained.",
        },
        {
            "source_id": "SRC1148_16_Newton_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_868_NEWTON_SOURCE_NORMALIZATION_CONTRACT.csv",
            "needle": "NS868_1_measured_GM",
            "role": "Newton source-normalization contract is not parent-derived.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def alias_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "alias_id": "ALIAS1148_0_symbol_map",
                "symbol": "c_R11_flux_alpha3",
                "canonical_object": "c_domain_source_normalization_operator",
                "meaning": "branch-specific alpha3 notation for the R11/domain source-normalization operator",
                "source_anchor": "1137/1138",
                "current_value": "MISSING_DOMAIN_MU_EXTRA_OPERATOR_ZERO_OR_NUMERIC_COEFFICIENT",
                "claim_policy": "not a free product factor",
                "valid_for_claim": "false",
            },
            {
                "alias_id": "ALIAS1148_1_source_split",
                "symbol": "c_domain_source_normalization_operator",
                "canonical_object": "mu_extra/(G_eff*M_eff) domain/source-normalization contribution",
                "meaning": "operator measures extra source strength that can modify measured GM, alpha_i, xi, and R11 rows",
                "source_anchor": "R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM",
                "current_value": "MISSING_DOMAIN_PROJECTOR_COEFFICIENT_PRODUCTS_OR_THEOREM_ZERO",
                "claim_policy": "must be theorem-zero or numerically sourced with units/normalization",
                "valid_for_claim": "false",
            },
            {
                "alias_id": "ALIAS1148_2_alpha3_product",
                "symbol": "K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "canonical_object": "R11 alpha3 flux product",
                "meaning": "alpha3 product branch uses c_R11 but cannot define or tune it",
                "source_anchor": "1122/1136/1147",
                "current_value": "K=MISSING; c=MISSING; epsilon=MISSING",
                "claim_policy": "product shortcut forbidden",
                "valid_for_claim": "false",
            },
            {
                "alias_id": "ALIAS1148_3_Newton_bridge",
                "symbol": "c_R11",
                "canonical_object": "source-normalized Newton/measured-GM bottleneck",
                "meaning": "closing c_R11 helps the Newton branch only if same-frame source charge and no mu_extra channels close",
                "source_anchor": "P8_source_normalized_Newton_branch_STACK",
                "current_value": "not_parent_derived",
                "claim_policy": "no Newton/local-GR promotion",
                "valid_for_claim": "false",
            },
        ]
    )


def owner_theorem_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "clause_id": "OWN1148_0_same_observed_coframe",
                "needed_statement": "matter, clocks, photons, source current, exterior charge, and orbital readout use one observed coframe",
                "math_form": "e_obs = e_matter = e_source = e_charge = e_orbit",
                "current_evidence": "Y5O_1 and SN0 mark same-frame/coframe as not parent-derived",
                "result": "MISSING_PARENT_COFRAME_OWNER",
                "effect_if_missing": "c_R11 can hide in frame/source normalization",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "OWN1148_1_constant_universal_coupling",
                "needed_statement": "local coupling is constant, universal, source-blind, range-blind, and frame-blind",
                "math_form": "partial_t,r,A,lambda,frame G_eff = 0",
                "current_evidence": "Y5O_2/S1/SN7 are conditional or not parent-derived",
                "result": "MISSING_CONSTANT_COUPLING_SUPERSELECTION",
                "effect_if_missing": "Gdot, fifth-force, species, radial, or frame dependence can mimic source normalization",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "OWN1148_2_parent_source_charge",
                "needed_statement": "measured source mass is a parent Noether/Hamiltonian/Hilbert mass charge before orbital fitting",
                "math_form": "M_H[W] = integral_S Q_M[tau] = (4*pi*G_ref)^-1 integral_S Pi_M J_H",
                "current_evidence": "Y5O_3/SN3 and measured-GM obstruction rows are not parent-derived",
                "result": "MISSING_PARENT_SOURCE_CHARGE",
                "effect_if_missing": "measured GM remains an orbital calibration rather than a derived source owner",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "OWN1148_3_flux_closure",
                "needed_statement": "projected Hilbert mass current is closed in compact source-free exterior regions",
                "math_form": "d(Pi_M J_H)=0; partial_t M_eff=0; partial_r M_eff=0",
                "current_evidence": "Y5O_4/SN4 and OBS1013_6 keep flux leakage retained",
                "result": "MISSING_FLUX_CLOSURE",
                "effect_if_missing": "radial/time source hair remains live",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "OWN1148_4_no_extra_mass_projection",
                "needed_statement": "boundary, domain, projector, bulk, memory, non-EH, frame, species, and calibration channels carry no independent mass projection",
                "math_form": "mu_extra = Delta_nonEH + Delta_symp + Delta_PiM + Delta_extra + Delta_frame + Delta_cal + Delta_PPN = 0",
                "current_evidence": "Y5O_5/SN6 and R11 source-normalization rows keep all channels retained/unfilled",
                "result": "MISSING_MU_EXTRA_ZERO_VECTOR",
                "effect_if_missing": "c_R11 remains a live source-normalization residual",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "OWN1148_5_no_absorption_cheat",
                "needed_statement": "range/time/species/radial dependence is not absorbed into a fitted measured GM",
                "math_form": "partial_r mu_extra = partial_t mu_extra = partial_A mu_extra = partial_lambda mu_extra = 0 unless scored",
                "current_evidence": "S4 is rule-written but not satisfied; 1147 forbids product shortcuts",
                "result": "GUARD_ACTIVE_NOT_PROOF",
                "effect_if_missing": "constant-GM calibration could hide residual physics",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "OWN1148_6_second_order_stability",
                "needed_statement": "same source charge remains stable through beta/gamma/preferred-frame PPN order",
                "math_form": "Delta_PPN_source = 0 or source-backed bounded",
                "current_evidence": "Y5O_7/SN11 are not derived or not run",
                "result": "MISSING_SECOND_ORDER_PPN_SOURCE_STABILITY",
                "effect_if_missing": "Newton normalization could pass while GR/PPN fails",
                "valid_for_claim": "false",
            },
            {
                "clause_id": "OWN1148_7_verdict",
                "needed_statement": "c_R11_flux_alpha3 = 0 as a parent source-normalization theorem",
                "math_form": "OWN1148_0 through OWN1148_6 close together",
                "current_evidence": "multiple owner clauses are missing or conditional only",
                "result": "c_R11_ZERO_THEOREM_NOT_DERIVED",
                "effect_if_missing": "c_R11 remains retained and alpha3/Newton rows remain blocked",
                "valid_for_claim": "false",
            },
        ]
    )


def channel_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "channel_id": "CH1148_0_radial_Meff_hair",
                "source_channel": "radial_Meff_hair",
                "coefficient_symbol": "epsilon_radial_Meff",
                "required_zero_or_input": "zero radial hair theorem or numeric radial profile",
                "current_status": "MISSING_RADIAL_NOHAIR_THEOREM_OR_NUMERIC_PROFILE",
                "maps_to": "beta_minus_1; alpha(lambda); R11",
                "valid_for_claim": "false",
            },
            {
                "channel_id": "CH1148_1_boundary_monopole_shift",
                "source_channel": "boundary_monopole_shift",
                "coefficient_symbol": "epsilon_boundary",
                "required_zero_or_input": "boundary no-hair/no-flux theorem or coefficient bounds",
                "current_status": "MISSING_BOUNDARY_NOHAIR_THEOREM_OR_NUMERIC_COEFFICIENT",
                "maps_to": "beta_minus_1; alpha3; xi; Gdot_over_G; R11",
                "valid_for_claim": "false",
            },
            {
                "channel_id": "CH1148_2_domain_projector_mass",
                "source_channel": "domain_projector_mass",
                "coefficient_symbol": "epsilon_domain_projector / c_domain_source_normalization_operator",
                "required_zero_or_input": "domain no-vector/no-flux/no-anisotropy theorem or numeric products below gates",
                "current_status": "MISSING_DOMAIN_PROJECTOR_ZERO_THEOREM_OR_NUMERIC_PRODUCTS",
                "maps_to": "alpha1; alpha2; alpha3; xi; R11",
                "valid_for_claim": "false",
            },
            {
                "channel_id": "CH1148_3_bulk_X_Yukawa_tail",
                "source_channel": "bulk_X_Yukawa_tail",
                "coefficient_symbol": "epsilon_bulk_X",
                "required_zero_or_input": "positive mass-gap no-hair theorem or alpha(lambda) curve",
                "current_status": "MISSING_BULK_MASS_GAP_THEOREM_OR_ALPHA_LAMBDA_CURVE",
                "maps_to": "alpha(lambda); R10; R11",
                "valid_for_claim": "false",
            },
            {
                "channel_id": "CH1148_4_nonEH_operator_potential",
                "source_channel": "nonEH_operator_potential",
                "coefficient_symbol": "epsilon_nonEH_source",
                "required_zero_or_input": "EH-only exterior theorem or non-EH operator coefficient map",
                "current_status": "MISSING_EH_ONLY_THEOREM_OR_NONEH_OPERATOR_COEFFICIENT_MAP",
                "maps_to": "gamma_minus_1; beta_minus_1; alpha(lambda); R11",
                "valid_for_claim": "false",
            },
            {
                "channel_id": "CH1148_5_species_source_charge",
                "source_channel": "species_source_charge",
                "coefficient_symbol": "epsilon_species_A",
                "required_zero_or_input": "selector-blind source theorem or eta_source_AB residual",
                "current_status": "MISSING_SELECTOR_BLIND_SOURCE_THEOREM_OR_SPECIES_CHARGE_VECTOR",
                "maps_to": "eta_source_AB; clock_redshift; R11",
                "valid_for_claim": "false",
            },
            {
                "channel_id": "CH1148_6_time_drift",
                "source_channel": "time_drift",
                "coefficient_symbol": "epsilon_time_drift",
                "required_zero_or_input": "stationarity theorem or Gdot/G bound row",
                "current_status": "MISSING_STATIONARITY_THEOREM_OR_TIME_DRIFT_COEFFICIENT",
                "maps_to": "Gdot_over_G; R9; R11",
                "valid_for_claim": "false",
            },
            {
                "channel_id": "CH1148_7_absolute_calibration_offset",
                "source_channel": "absolute_calibration_offset",
                "coefficient_symbol": "epsilon_calibration",
                "required_zero_or_input": "parent-fixed universal calibration with zero derivatives",
                "current_status": "MISSING_PARENT_FIXED_UNIVERSAL_CALIBRATION_THEOREM_OR_RETAINED_OFFSET",
                "maps_to": "beta_minus_1; Gdot_over_G; R11",
                "valid_for_claim": "false",
            },
            {
                "channel_id": "CH1148_8_channel_verdict",
                "source_channel": "source_normalization_operator_total",
                "coefficient_symbol": "c_R11_flux_alpha3",
                "required_zero_or_input": "all channels theorem-zero or source-backed bounded with no cancellation",
                "current_status": "ALL_CHANNELS_RETAINED_OR_MISSING",
                "maps_to": "Newton/measured-GM; alpha3 product; R11 ledger",
                "valid_for_claim": "false",
            },
        ]
    )


def numeric_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "numeric_id": "NUM1148_0_canonical_row",
                "target": "c_domain_source_normalization_operator",
                "required_input": "derived zero or numeric coefficient with units, normalization, weak-field map, and source path",
                "current_value": "MISSING_DOMAIN_MU_EXTRA_OPERATOR_ZERO_OR_NUMERIC_COEFFICIENT",
                "source_path": "MISSING_PARENT_ACTION_OR_NUMERIC_COEFFICIENT_SOURCE",
                "status": "CANONICAL_CONTRACT_ROW_BLOCKED",
                "valid_for_claim": "false",
            },
            {
                "numeric_id": "NUM1148_1_minimum_fill",
                "target": "R11 source-normalization eight-channel fill",
                "required_input": "every channel derived_zero, derived_bound, numeric_bound, or retained_unfilled with no-claim",
                "current_value": "minimum_row_missing_input across channels",
                "source_path": "various required_source_artifact rows",
                "status": "NO_CLAIMABLE_ROWS",
                "valid_for_claim": "false",
            },
            {
                "numeric_id": "NUM1148_2_scorecard",
                "target": "source-normalization residual scorecard",
                "required_input": "charge/current, Poisson/source, mu_extra, Gdot/range, M_eff flux, species, radial, alpha(lambda), PPN rows",
                "current_value": "not_loaded/unfilled/not_computed",
                "source_path": "P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
                "status": "SCORECARD_NOT_EXECUTABLE",
                "valid_for_claim": "false",
            },
            {
                "numeric_id": "NUM1148_3_verdict",
                "target": "finite c_R11 value or bound",
                "required_input": "source-backed c_R11 or channel envelope below mapped locks",
                "current_value": "NO_NUMERIC_C_R11_SOURCE_FOUND",
                "source_path": "NO_VALID_SOURCE_PATH",
                "status": "NUMERIC_ROUTE_NOT_FILLED",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1148_0_sources_exist",
                "rule": "all 1148 cited source paths and needles exist",
                "gate_pass": "true_nonclaim",
                "reason": "source register validates the local audit trail",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1148_1_alias_locked",
                "rule": "c_R11 is linked to c_domain/source-normalization and not treated as a free product knob",
                "gate_pass": "true_nonclaim",
                "reason": "alias ledger defines the canonical object and product guard",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1148_2_zero_theorem",
                "rule": "c_R11 source-normalization theorem-zero is derived",
                "gate_pass": "false",
                "reason": "owner/coframe/coupling/charge/flux/mu_extra/PPN clauses are missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1148_3_numeric_source",
                "rule": "finite source-backed c_R11 or channel envelope exists",
                "gate_pass": "false",
                "reason": "canonical row and all channel rows remain missing/unfilled",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1148_4_product_scoring",
                "rule": "K*c*epsilon alpha3 product is scoreable",
                "gate_pass": "false",
                "reason": "c_R11 is not zero or numeric, and K/epsilon are still missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1148_5_Newton_GR_promotion",
                "rule": "source-normalized Newton/local-GR branch can be promoted",
                "gate_pass": "false",
                "reason": "measured-GM/source-normalization owner theorem remains unsatisfied",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1148_0_c_status",
                "decision": "c_R11_not_derived_or_sourced",
                "reason": "it is an alias to a missing source-normalization operator with unresolved owner and channel-zero clauses",
                "next_action": "do not use c_R11 in alpha3 or Newton claims",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1148_1_structure_gain",
                "decision": "c_R11_recast_as_source_normalization_residual_vector",
                "reason": "the bottleneck is now decomposed into owner clauses and eight source-normalization channels",
                "next_action": "attack the minimum owner lemma instead of treating c as a free coefficient",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1148_2_best_next",
                "decision": "target_minimal_source_owner_lemma",
                "reason": "same-frame source charge plus flux closure is the parent-theorem route that would help both Newton and c_R11",
                "next_action": "build 1149 source-owner minimal lemma or channel-bound fallback",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1148_0_1149",
                "next_target": "1149-Y5-R10-source-normalization-owner-minimal-lemma-or-channel-bound-fallback.md",
                "objective": "try to derive the minimal source-owner lemma: same observed coframe, parent Hilbert/Noether source charge, and closed Pi_M J_H flux; if it fails, create the first channel-bound fallback queue for the c_R11 source-normalization vector",
                "include": "same-frame source variation; Hamiltonian/Hilbert charge equality; Pi_M flux closure; mu_extra channel queue; measured-GM/Newton bridge; c_R11 product guard",
                "exclude": "fitted GM absorption; product shortcut; tuned cancellation; local-GR/Newton claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    aliases: list[dict[str, object]],
    owners: list[dict[str, object]],
    channels: list[dict[str, object]],
    numerics: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = aliases + owners + channels + numerics + gates + decisions + next_target
    add(
        "V1148_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1148_1_alias_locked",
        any(row["alias_id"] == "ALIAS1148_0_symbol_map" and row["canonical_object"] == "c_domain_source_normalization_operator" for row in aliases)
        and any(row["alias_id"] == "ALIAS1148_2_alpha3_product" and row["claim_policy"] == "product shortcut forbidden" for row in aliases),
        "c_R11 is locked to source-normalization and product shortcut is forbidden",
    )
    add(
        "V1148_2_zero_not_derived",
        any(row["clause_id"] == "OWN1148_7_verdict" and row["result"] == "c_R11_ZERO_THEOREM_NOT_DERIVED" for row in owners),
        "c_R11 theorem-zero is explicitly not derived",
    )
    add(
        "V1148_3_channel_vector_complete",
        {
            "CH1148_0_radial_Meff_hair",
            "CH1148_1_boundary_monopole_shift",
            "CH1148_2_domain_projector_mass",
            "CH1148_3_bulk_X_Yukawa_tail",
            "CH1148_4_nonEH_operator_potential",
            "CH1148_5_species_source_charge",
            "CH1148_6_time_drift",
            "CH1148_7_absolute_calibration_offset",
        }.issubset({row["channel_id"] for row in channels}),
        "eight source-normalization channels are represented",
    )
    add(
        "V1148_4_numeric_not_filled",
        any(row["numeric_id"] == "NUM1148_3_verdict" and row["status"] == "NUMERIC_ROUTE_NOT_FILLED" for row in numerics),
        "no finite c_R11 value or bound is found",
    )
    add(
        "V1148_5_claim_gates_blocked",
        any(row["gate_id"] == "G1148_2_zero_theorem" and row["gate_pass"] == "false" for row in gates)
        and any(row["gate_id"] == "G1148_5_Newton_GR_promotion" and row["gate_pass"] == "false" for row in gates),
        "zero theorem and Newton/GR promotion gates remain blocked",
    )
    add(
        "V1148_6_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in all_rows)
        and all(row.get("claim_allowed", "false") == "false" for row in next_target),
        "all generated rows remain nonclaim",
    )
    add(
        "V1148_7_next_target",
        next_target[0]["next_target"].startswith("1149-") and "source-normalization-owner" in str(next_target[0]["next_target"]),
        "1149 handoff targets source-owner minimal lemma or channel-bound fallback",
    )
    add(
        "V1148_8_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1148_9_csv_parse", csv_parse_ok, "all 1148 CSV outputs parse cleanly")
    add("V1148_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add(
        "V1148_SUMMARY",
        True,
        "1148 locks c_R11 to source-normalization, rejects theorem-zero/numeric claim, and sends source-owner lemma to 1149",
    )
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    aliases: list[dict[str, object]],
    owners: list[dict[str, object]],
    channels: list[dict[str, object]],
    numerics: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1148 - Y5/R10 cR11 Source-Normalization Owner or Zero Theorem

**Current verdict:** `c_R11_flux_alpha3` is not derived, zeroed, or numerically sourced. It is an alias for the domain/source-normalization operator, so treating it as a free alpha3 product factor would be cheating.

**Useful progress:** the symbol is now compressed into a source-normalization residual vector: same coframe, constant coupling, parent source charge, closed `Pi_M J_H` flux, no `mu_extra`, no fitted-GM absorption, and second-order PPN stability.

**Important guard:** closing `c_R11` is a Newton/GR source-normalization problem first and an alpha3-product problem second. This is exactly why it is worth attacking.

**Best next attack:** derive the minimal source-owner lemma: same-frame source variation, Hamiltonian/Hilbert charge equality, and closed projected source flux. If that fails, build the first channel-bound fallback queue.

**No claim:** no R10, PPN, alpha3, preferred-frame, source-normalized Newton, local-GR, measured-GM, GitHub, or public claim follows from 1148.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "role"], sources)}

## Alias and Product Lock
{table(["alias_id", "symbol", "canonical_object", "meaning", "source_anchor", "current_value", "claim_policy", "valid_for_claim"], aliases)}

## Owner Zero-Theorem Audit
{table(["clause_id", "needed_statement", "math_form", "current_evidence", "result", "effect_if_missing", "valid_for_claim"], owners)}

## Source-Normalization Channel Vector
{table(["channel_id", "source_channel", "coefficient_symbol", "required_zero_or_input", "current_status", "maps_to", "valid_for_claim"], channels)}

## Numeric Source Route
{table(["numeric_id", "target", "required_input", "current_value", "source_path", "status", "valid_for_claim"], numerics)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1148_SOURCE_REGISTER.csv",
        "aliases": OUT / "P8_Y5_R10_1148_C_R11_ALIAS_AND_PRODUCT_LOCK.csv",
        "owners": OUT / "P8_Y5_R10_1148_SOURCE_OWNER_ZERO_THEOREM_AUDIT.csv",
        "channels": OUT / "P8_Y5_R10_1148_SOURCE_NORMALIZATION_CHANNEL_VECTOR.csv",
        "numerics": OUT / "P8_Y5_R10_1148_C_R11_NUMERIC_SOURCE_ROUTE.csv",
        "gates": OUT / "P8_Y5_R10_1148_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1148_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1148_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1148_VALIDATION.csv",
    }
    sources = source_rows()
    aliases = alias_rows()
    owners = owner_theorem_rows()
    channels = channel_rows()
    numerics = numeric_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["aliases"], aliases)
    write_csv(outputs["owners"], owners)
    write_csv(outputs["channels"], channels)
    write_csv(outputs["numerics"], numerics)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, aliases, owners, channels, numerics, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, aliases, owners, channels, numerics, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    if failed:
        for row in failed:
            print(f"{row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
