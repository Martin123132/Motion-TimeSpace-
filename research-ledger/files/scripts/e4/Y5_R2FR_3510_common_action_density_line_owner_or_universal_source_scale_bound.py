from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3510-Y5-R2FR-common-action-density-line-owner-or-universal-source-scale-bound.md"
CANONICAL_COMMON_SCALE = OUT / "P8_EM_common_action_density_line_universal_source_scale.csv"

SOURCES: dict[str, dict[str, Any]] = {
    "script_3510": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3509": {
        "path": ROOT / "3509-Y5-R2FR-no-source-only-matter-functor-signature-or-zg-bound.md",
        "role": "3509 source-slot theorem handoff",
    },
    "residual_3509": {
        "path": OUT / "P8_EM_no_source_only_matter_functor_residual.csv",
        "role": "3509 no-source-only residual vector",
    },
    "theorem_3509": {
        "path": OUT / "P8_Y5_R2FR_3509_NO_SOURCE_ONLY_MATTER_FUNCTOR_THEOREM.csv",
        "role": "3509 source-slot theorem stack",
    },
    "minimal_parent_line_3378": {
        "path": OUT / "P8_Y5_R2FR_3378_MINIMAL_PARENT_ACTION_LINE.csv",
        "role": "minimal parent action line candidate",
    },
    "minimal_line_candidate_3395": {
        "path": OUT / "P8_Y5_R2FR_3395_MINIMAL_PARENT_ACTION_LINE_CANDIDATE.csv",
        "role": "minimal parent action line source/current contract",
    },
    "parent_density_3424": {
        "path": OUT / "P8_Y5_R2FR_3424_PARENT_ACTION_DENSITY.csv",
        "role": "parent action density candidate",
    },
    "density_line_owner_3252": {
        "path": OUT / "P8_Y5_R2FR_3252_PARENT_ACTION_DENSITY_LINE_OWNER_ATTEMPT.csv",
        "role": "parent action density line owner attempt",
    },
    "action_scale_1888": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1888_ACTION_SCALE_OWNER_PROOF_ATTEMPT.csv",
        "role": "action scale owner proof attempt",
    },
    "action_scale_measure_2676": {
        "path": OUT / "P8_Y5_R2FR_2676_ACTION_SCALE_MEASURE_OWNER_PROOF_AUDIT.csv",
        "role": "action scale/measure owner proof audit",
    },
    "action_current_lock_1418": {
        "path": OUT / "P8_Y5_R10_1418_ACTION_SCALE_CURRENT_OWNER_LOCK_ATTEMPT.csv",
        "role": "action scale/current owner lock attempt",
    },
    "action_scale_1230": {
        "path": OUT / "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv",
        "role": "universal action-scale owner theorem attempt",
    },
    "ppn_gdot_map_708": {
        "path": OUT / "P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv",
        "role": "PPN/Gdot/WEP map",
    },
    "newton_contract_868": {
        "path": OUT / "P8_Y5_R10_868_NEWTON_SOURCE_NORMALIZATION_CONTRACT.csv",
        "role": "Newton source normalization contract",
    },
    "newton_chain_3382": {
        "path": OUT / "P8_Y5_R2FR_3382_NEWTON_SOURCE_NORMALIZATION_CHAIN.csv",
        "role": "Newton source normalization chain",
    },
    "clock_bound_1052": {
        "path": OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
        "role": "clock alpha product bound ledger",
    },
}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(metadata["path"]),
            "exists": bool_text(Path(metadata["path"]).exists()),
            "role": metadata["role"],
            "valid_for_claim": "False",
        }
        for source_id, metadata in SOURCES.items()
    ]


def common_action_line_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "UAS3510_0_single_density_line_target",
            "claim_piece": "single ordinary-matter action-density line",
            "statement": "Ordinary matter uses one parent action-density line and one common action/phase normalization before variation and readout.",
            "mathematical_form": "S_ord = int dmu_parent L_ord(Psi_A,e_obs,A_Q,theta_A; constants), not sum_A w_A(X) S_A with independent density lines",
            "derivation": "If species sectors are fields/representations inside one density line, a new common source scalar must be an automorphism of that line rather than an independent species source charge.",
            "payoff": "keeps 3509's connected-naturality collapse meaningful and stops species-dependent WEP source weights",
            "gap": "parent has candidate action lines but not a derived unique line from MTS primitives",
            "status": "TARGET_SHARP_NOT_PARENT_SIGNED",
            "source_path": str(SOURCES["density_line_owner_3252"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "UAS3510_1_common_scale_identity",
            "claim_piece": "universal common source scale identity",
            "statement": "A common scalar w_common multiplying all ordinary matter is not composition-dependent, but it rescales the active Hilbert source relative to the gravitational coupling.",
            "mathematical_form": "E_mu nu = kappa_ref w_common T_H, so G_eff = G_ref w_common if the EH coefficient is held fixed",
            "derivation": "Varying w_common S_matter gives w_common T_H. The field equation only sees the product kappa_ref w_common unless the parent action line fixes w_common=1 or D_X ln w_common=0.",
            "payoff": "moves the residual from WEP/R10 composition into universal G/source calibration",
            "gap": "D_X ln w_common is not proved zero",
            "status": "EXACT_ALGEBRAIC_RECLASSIFICATION",
            "source_path": str(SOURCES["newton_chain_3382"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "UAS3510_2_common_mode_not_harmless",
            "claim_piece": "common scalar guard",
            "statement": "A common scalar is harmless only for composition tests after one calibration; it is not harmless for time/radius/frame drift, Newton source normalization, clocks, or absolute source calibration.",
            "mathematical_form": "D_X ln(G_eff M_H) = D_X ln G_ref + D_X ln w_common + D_X ln M_H + retained extra-source terms",
            "derivation": "The measured Newtonian source is the product of coupling and Hilbert mass. A common rescaling cannot be seen as WEP composition charge, but it still shifts the absolute monopole unless fixed or calibrated once.",
            "payoff": "prevents hiding source coupling inside G_N/GM backfill",
            "gap": "need fixed kappa/G_ref and closed M_H projector before a zero claim",
            "status": "ANTI_BACKFILL_IDENTITY",
            "source_path": str(SOURCES["minimal_line_candidate_3395"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "UAS3510_3_fixed_action_phase_measure",
            "claim_piece": "hbar/measure/action phase owner",
            "statement": "A single parent hbar/action phase and species-blind measure would remove independent common-source normalization drift from ordinary matter.",
            "mathematical_form": "D_X ln hbar_parent = 0, D_X ln dmu_parent has no ordinary-matter source component, D_X ln w_common = 0",
            "derivation": "If the parent fixes the action phase and measure, w_common cannot vary as a physical source multiplier without adding an extra action-line automorphism.",
            "payoff": "would close the matter-side universal source scale",
            "gap": "hbar/measure owner remains a contract, not parent-derived",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "source_path": str(SOURCES["action_scale_1888"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "UAS3510_4_Newton_Poisson_payoff",
            "claim_piece": "Newtonian coefficient recovery",
            "statement": "If kappa_ref and w_common are fixed and the Hilbert source is the same object used by the Hamiltonian mass projector, the weak-field 00 equation gives the Poisson coefficient without orbital GM backfill.",
            "mathematical_form": "G_00^(1)=2 nabla^2 Phi_N/c^2, T_00=w_common rho_H c^2 => nabla^2 Phi_N=4 pi G_ref w_common rho_H",
            "derivation": "With w_common=1 or fixed once into G_ref, the same source normalization enters the field equation, Hamiltonian charge, and Newtonian potential.",
            "payoff": "turns local Newton recovery from fitted amplitude into conditional algebra",
            "gap": "extra K_MTS_IR_00 and boundary/reference locks remain separate gates",
            "status": "EXACT_CONDITIONAL_NEWTON_CHAIN",
            "source_path": str(SOURCES["newton_chain_3382"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "UAS3510_5_verdict",
            "claim_piece": "3510 verdict",
            "statement": "The common action-density line route is viable and sharper than a generic source-coupling gap: it either fixes w_common or maps it to universal G/source calibration.",
            "mathematical_form": "D_X ln w_common = 0 if parent line/phase/measure signed; otherwise zeta_common := D_X ln w_common is a universal residual",
            "derivation": "Combine the 3509 common-scalar reclassification with the minimal action-line and Newton source-normalization chains.",
            "payoff": "source coupling frontier is now universal-scale/kappa ownership, not WEP species poisoning",
            "gap": "no live local-GR/Newton claim until fixed kappa/G_ref/source projector owners also close",
            "status": "THEOREM_STACK_CONSTRUCTED_NOT_PARENT_SIGNED",
            "source_path": str(SOURCES["minimal_parent_line_3378"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "UCSR3510_0_zeta_w_common",
            "residual": "zeta_w_common",
            "definition": "D_X ln w_common",
            "3510_result": "universal source-scale residual, not composition source charge",
            "zero_condition": "single fixed parent action-density line, action phase and measure",
            "maps_to": "G_eff/source calibration drift",
            "observable_links": "Gdot; Newton_G; clock/action normalization; source_calibration",
            "claim_allowed": "False",
        },
        {
            "row_id": "UCSR3510_1_delta_w_species",
            "residual": "delta_w_species",
            "definition": "D_X ln w_A - D_X ln w_B",
            "3510_result": "inherits 3509 conditional zero under connected density-line naturality",
            "zero_condition": "connected ordinary matter category and one action-density line",
            "maps_to": "WEP/composition only if connectedness fails",
            "observable_links": "WEP; composition_source; beta_source_alpha",
            "claim_allowed": "False",
        },
        {
            "row_id": "UCSR3510_2_Geff_common_scale",
            "residual": "Geff_common_scale",
            "definition": "D_X ln(G_ref w_common)",
            "3510_result": "effective gravitational coupling drift from common matter scale and EH coefficient",
            "zero_condition": "D_X ln G_ref + D_X ln w_common = 0 by parent identity, not tuning",
            "maps_to": "Gdot/G and Newton source normalization",
            "observable_links": "Gdot_over_G; ephemerides; binary/orbital GM; Newton_limit",
            "claim_allowed": "False",
        },
        {
            "row_id": "UCSR3510_3_mu_obs_common_scale",
            "residual": "mu_obs_common_scale",
            "definition": "D_X ln mu_obs from common source scale",
            "3510_result": "absolute measured GM can absorb one constant calibration but not drift or radius/source dependence",
            "zero_condition": "closed M_H projector plus fixed common scale",
            "maps_to": "radial/time GM drift and source calibration",
            "observable_links": "orbital_GM; Gdot; radial_source_hair",
            "claim_allowed": "False",
        },
        {
            "row_id": "UCSR3510_4_clock_action_scale",
            "residual": "clock_action_scale",
            "definition": "common action/phase normalization entering clock/readout constants",
            "3510_result": "retained if hbar/action phase/readout owner unsigned",
            "zero_condition": "fixed hbar_parent and readout-stable action phase",
            "maps_to": "clock drift and alpha/mass product bounds",
            "observable_links": "clock; spectroscopy; alpha_mass_clock",
            "claim_allowed": "False",
        },
        {
            "row_id": "UCSR3510_5_extra_metric_source",
            "residual": "extra_metric_source",
            "definition": "K_MTS_IR_00 or non-Hilbert source term not absorbed by common scale",
            "3510_result": "parallel retained gate outside ordinary common action scale",
            "zero_condition": "local residual sector has no linear source vertex or is bounded",
            "maps_to": "PPN gamma/beta/R10/source residual",
            "observable_links": "PPN; R10; Newton_limit",
            "claim_allowed": "False",
        },
    ]


def bound_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "UCBIN3510_0_Gdot",
            "arena": "Gdot/time drift",
            "residual": "Geff_common_scale",
            "predicted_value": "MISSING_DX_LN_GREF_PLUS_WCOMMON",
            "predicted_units": "yr^-1_or_declared_time_scale",
            "bound_value": "MISSING_GDOT_BOUND",
            "bound_units": "yr^-1",
            "source_path": str(SOURCES["ppn_gdot_map_708"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "UCBIN3510_1_Newton_GM",
            "arena": "Newton/source calibration",
            "residual": "mu_obs_common_scale",
            "predicted_value": "MISSING_DX_LN_MU_OBS_COMMON",
            "predicted_units": "dimensionless_or_declared_scale",
            "bound_value": "MISSING_NEWTON_GM_BOUND",
            "bound_units": "same_as_prediction",
            "source_path": str(SOURCES["newton_contract_868"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "UCBIN3510_2_clock_action",
            "arena": "clock/action normalization",
            "residual": "clock_action_scale",
            "predicted_value": "MISSING_ACTION_CLOCK_PROJECTION",
            "predicted_units": "yr^-1_or_declared_clock_scale",
            "bound_value": "MISSING_CLOCK_BOUND",
            "bound_units": "yr^-1",
            "source_path": str(SOURCES["clock_bound_1052"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "UCBIN3510_3_delta_w_species",
            "arena": "WEP/composition fallback",
            "residual": "delta_w_species",
            "predicted_value": "MISSING_DELTA_W_SPECIES_IF_CONNECTEDNESS_FAILS",
            "predicted_units": "dimensionless",
            "bound_value": "MISSING_WEP_BOUND",
            "bound_units": "dimensionless",
            "source_path": str(SOURCES["residual_3509"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "UCBIN3510_4_extra_metric_source",
            "arena": "PPN/R10/Newton residual",
            "residual": "extra_metric_source",
            "predicted_value": "MISSING_K_MTS_IR_00_OR_SOURCE_VERTEX",
            "predicted_units": "dimensionless_or_potential_units",
            "bound_value": "MISSING_PPN_R10_BOUND",
            "bound_units": "same_as_prediction",
            "source_path": str(SOURCES["parent_density_3424"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def parse_float(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def run_bound_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for row in rows:
        predicted = parse_float(str(row["predicted_value"]))
        bound = parse_float(str(row["bound_value"]))
        if row["valid_for_claim"] != "True":
            verdict = "BLOCKED_INPUT_NOT_VALID_FOR_CLAIM"
            passes = "False"
        elif predicted is None or bound is None or bound <= 0:
            verdict = "BLOCKED_MISSING_NUMERIC_PREDICTION_OR_BOUND"
            passes = "False"
        else:
            passes = bool_text(abs(predicted) <= bound)
            verdict = "PASS_NUMERIC_COMMON_SCALE_BOUND" if passes == "True" else "FAIL_NUMERIC_COMMON_SCALE_BOUND"
        results.append(
            {
                "row_id": row["row_id"].replace("UCBIN", "UCRUN"),
                "arena": row["arena"],
                "residual": row["residual"],
                "predicted_value": row["predicted_value"],
                "bound_value": row["bound_value"],
                "pass_condition": "abs(predicted_value) <= bound_value with sourced numeric rows",
                "runner_verdict": verdict,
                "passes_bound": passes,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return results


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3510_0_common_scalar_reclassified",
            "decision": "The common matter scale is no longer a WEP/source-composition problem; it is a universal G/source/action calibration problem.",
            "rationale": "A common scalar multiplies every Hilbert source equally, so it cannot distinguish materials but it can drift the absolute coupling.",
            "effect": "The next derivation should target fixed kappa/G_ref/action line ownership, not repeat species-weight arguments.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3510_1_no_harmless_common_mode",
            "decision": "Do not declare w_common harmless unless it is constant or absorbed once into a fixed parent coupling.",
            "rationale": "A drifting common scalar maps directly to Gdot/Newton GM/source calibration and possibly clock/action normalization.",
            "effect": "All common-scale rows remain non-claim until D_X ln w_common or D_X ln(G_ref w_common) is derived/bounded.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3510_2_best_next_target",
            "decision": "Attack the fixed kappa/G_ref and action-line lock next.",
            "rationale": "If the EH coefficient and common matter action scale share a parent owner, Newton's coefficient can be recovered without orbital-GM backfill.",
            "effect": "Next step should derive D_X ln(G_ref w_common)=0 or create executable Gdot/Newton/clock bound rows.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3511-Y5-R2FR-fixed-kappa-Gref-action-line-lock-or-Gdot-Newton-bound.md",
            "next_script": "scripts/Y5_R2FR_3511_fixed_kappa_Gref_action_line_lock_or_Gdot_Newton_bound.py",
            "objective": "Derive whether the EH coefficient kappa/G_ref and the common ordinary-matter action scale are locked by one parent constant/topological owner; if not, produce executable non-claim Gdot/Newton/clock common-scale bound rows.",
            "success_gate": "Either D_X ln(G_ref w_common)=0 is parent-signed, or the common-scale residual is numerically mapped to Gdot, Newton GM/source calibration, and clock/action rows.",
            "forbidden_shortcuts": "Do not use measured orbital GM to define the theorem coefficient; do not absorb a drifting common scalar by convention.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    bound_inputs: list[dict[str, Any]],
    runner_results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    theorem_ids = {row["theorem_id"] for row in theorem_rows}
    residual_names = {row["residual"] for row in residuals}
    all_claim_false = all(
        row.get("valid_for_claim") == "False"
        for table in [sources, theorem_rows, bound_inputs, runner_results, decisions, next_rows]
        for row in table
    ) and all(row.get("claim_allowed") == "False" for row in residuals)
    all_blocked = all("BLOCKED" in row["runner_verdict"] for row in runner_results)
    validation = [
        {
            "check_id": "VAL3510_0_sources_exist",
            "passed": bool_text(all(row["exists"] == "True" for row in sources)),
            "detail": "all cited local source paths exist",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3510_1_theorem_stack_present",
            "passed": bool_text({"UAS3510_0_single_density_line_target", "UAS3510_1_common_scale_identity", "UAS3510_2_common_mode_not_harmless"}.issubset(theorem_ids)),
            "detail": "density-line, common-scale, and anti-backfill identities written",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3510_2_common_scale_residuals_present",
            "passed": bool_text({"zeta_w_common", "Geff_common_scale", "mu_obs_common_scale", "clock_action_scale"}.issubset(residual_names)),
            "detail": "universal common-scale residual vector complete",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3510_3_not_composition_claim",
            "passed": bool_text(any(row["residual"] == "zeta_w_common" and "universal" in row["3510_result"] for row in residuals)),
            "detail": "w_common classified as universal, not species-composition source charge",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3510_4_bound_runner_blocks_placeholders",
            "passed": bool_text(all_blocked),
            "detail": "all common-scale bound rows remain blocked until numeric sourced inputs exist",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3510_5_no_claim_flags",
            "passed": bool_text(all_claim_false),
            "detail": "no 3510 output row is valid_for_claim=True or claim_allowed=True",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3510_6_next_target_kappa_Gref_lock",
            "passed": bool_text(next_rows[0]["next_doc"].startswith("3511") and "G_ref" in next_rows[0]["objective"]),
            "detail": "fixed kappa/G_ref/action-line lock selected next",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL3510_7_formalization_workbench_not_targeted",
            "passed": bool_text(FORMALIZATION.exists() and str(DOC).startswith(str(ROOT))),
            "detail": str(FORMALIZATION),
            "valid_for_claim": "False",
        },
    ]
    validation.append(
        {
            "check_id": "VAL3510_SUMMARY",
            "passed": bool_text(all(row["passed"] == "True" for row in validation)),
            "detail": "PASS" if all(row["passed"] == "True" for row in validation) else "FAIL",
            "valid_for_claim": "False",
        }
    )
    return validation


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(
    theorem_rows: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    bound_inputs: list[dict[str, Any]],
    runner_results: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3510 - Common Action-Density Line Owner Or Universal Source-Scale Bound",
                "",
                "## Summary",
                "- **Derived gain:** `w_common` is not a WEP/composition source charge; it is a universal action/source/G calibration scalar.",
                "- **Exact identity:** if `S_matter -> w_common S_matter`, then the field equation sees `G_eff = G_ref w_common` unless the parent action line fixes `w_common`.",
                "- **Hard guard:** a common scalar can be calibrated once, but drift/radius/frame dependence still maps to `Gdot`, Newton `GM`, clocks, and source calibration.",
                "- **Next best move:** derive the fixed `kappa/G_ref` plus action-line lock, or run non-claim common-scale bounds.",
                "",
                "## Common Action-Line Theorem Stack",
                markdown_table(
                    theorem_rows,
                    ["theorem_id", "claim_piece", "statement", "mathematical_form", "payoff", "gap", "status"],
                ),
                "",
                "## Universal Common-Scale Residual Vector",
                markdown_table(
                    residuals,
                    ["row_id", "residual", "definition", "3510_result", "zero_condition", "maps_to", "claim_allowed"],
                ),
                "",
                "## Bound Input Template",
                markdown_table(
                    bound_inputs,
                    ["row_id", "arena", "residual", "predicted_value", "bound_value", "source_path", "valid_for_claim"],
                ),
                "",
                "## Runner Results",
                markdown_table(
                    runner_results,
                    ["row_id", "arena", "residual", "pass_condition", "runner_verdict", "passes_bound", "claim_allowed"],
                ),
                "",
                "## Decisions",
                markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"]),
                "",
                "## Next Target",
                markdown_table(
                    next_rows,
                    ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed"],
                ),
                "",
                "## Validation",
                markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"]),
                "",
                f"Generated: {now_utc()}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    sources = source_register_rows()
    theorem_rows = common_action_line_rows()
    residuals = residual_rows()
    bound_inputs = bound_input_rows()
    runner_results = run_bound_rows(bound_inputs)
    decisions = decision_rows()
    next_rows = next_target_rows()
    validation_rows = validate(sources, theorem_rows, residuals, bound_inputs, runner_results, decisions, next_rows)

    write_csv(OUT / "P8_Y5_R2FR_3510_SOURCE_REGISTER.csv", sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(
        OUT / "P8_Y5_R2FR_3510_COMMON_ACTION_DENSITY_LINE_THEOREM.csv",
        theorem_rows,
        ["theorem_id", "claim_piece", "statement", "mathematical_form", "derivation", "payoff", "gap", "status", "source_path", "valid_for_claim"],
    )
    residual_fields = [
        "row_id",
        "residual",
        "definition",
        "3510_result",
        "zero_condition",
        "maps_to",
        "observable_links",
        "claim_allowed",
    ]
    write_csv(OUT / "P8_Y5_R2FR_3510_UNIVERSAL_COMMON_SCALE_RESIDUAL.csv", residuals, residual_fields)
    write_csv(CANONICAL_COMMON_SCALE, residuals, residual_fields)
    write_csv(
        OUT / "P8_Y5_R2FR_3510_COMMON_SCALE_BOUND_INPUT_TEMPLATE.csv",
        bound_inputs,
        ["row_id", "arena", "residual", "predicted_value", "predicted_units", "bound_value", "bound_units", "source_path", "valid_for_claim"],
    )
    runner_fields = [
        "row_id",
        "arena",
        "residual",
        "predicted_value",
        "bound_value",
        "pass_condition",
        "runner_verdict",
        "passes_bound",
        "claim_allowed",
        "valid_for_claim",
    ]
    write_csv(OUT / "P8_Y5_R2FR_3510_COMMON_SCALE_BOUND_RUNNER_RESULTS.csv", runner_results, runner_fields)
    write_csv(OUT / "P8_EM_common_scale_bound_runner_results.csv", runner_results, runner_fields)
    write_csv(
        OUT / "P8_Y5_R2FR_3510_DECISION_LEDGER.csv",
        decisions,
        ["decision_id", "decision", "rationale", "effect", "claim_allowed", "valid_for_claim"],
    )
    write_csv(
        OUT / "P8_Y5_R2FR_3510_NEXT_TARGET.csv",
        next_rows,
        ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"],
    )
    write_csv(OUT / "P8_Y5_BRR545_3510_VALIDATION.csv", validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(theorem_rows, residuals, bound_inputs, runner_results, decisions, next_rows, validation_rows)


if __name__ == "__main__":
    main()
