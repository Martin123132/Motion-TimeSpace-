from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2934"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2934-Y5-R2FR-dotG-to-kappa-projection-theorem-or-ellJ-owner-source-current-normalization-under-AX1090.md"

SRC_2933_DOC = ROOT / "2933-Y5-R2FR-kappa-drift-range-source-bound-first-value-or-ellJ-owner-under-AX1090.md"
SRC_2933_NEXT = RESIDUALS / "P8_Y5_R2FR_2933_NEXT_TARGET.csv"
SRC_2933_PROJECTION = RESIDUALS / "P8_Y5_R2FR_2933_DOTG_KAPPA_PROJECTION_GATE.csv"
SRC_2933_BOUND = RESIDUALS / "P8_Y5_R2FR_2933_COUPLING_BOUND_SOURCE_ACQUISITION.csv"
SRC_2933_FIRST_VALUE = RESIDUALS / "P8_Y5_R2FR_2933_FIRST_VALUE_STATUS.csv"
SRC_2933_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2933_VALIDATION.csv"

SRC_2932_BOUND_LEDGER = RESIDUALS / "P8_Y5_R2FR_2932_COUPLING_FIRST_BOUND_ACQUISITION_LEDGER.csv"
SRC_2932_CONSTANT_AUDIT = RESIDUALS / "P8_Y5_R2FR_2932_KAPPA_ELLJ_CONSTANT_PROOF_AUDIT.csv"
SRC_2931_RESIDUAL = RESIDUALS / "P8_Y5_R2FR_2931_MTS_COEFFICIENT_RESIDUAL_DECOMPOSITION.csv"
SRC_2928_COUPLING = RESIDUALS / "P8_Y5_R2FR_2928_KAPPA_ELLJ_COUPLING_BASELINE_ROWS.csv"
SRC_2578_LEDGER = RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_RESIDUAL_INPUT_LEDGER.csv"
SRC_2925_DOC = ROOT / "2925-Y5-R2FR-MTS-to-EH-reduction-morphism-or-extra-sector-silence-proof-under-AX1090.md"
SRC_2924_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2924_MTS_TO_EH_REDUCTION_CONTRACT.csv"
SRC_2924_EH = RESIDUALS / "P8_Y5_R2FR_2924_EH_ANCHOR_COEFFICIENT_MAP.csv"

DOTG_BOUND_PER_YEAR = 4.0e-14
TARGET_2932_PER_YEAR = 9.6e-15

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2934_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_2934_DOTG_TO_KAPPA_PROJECTION_THEOREM_ATTEMPT.csv",
    "residual": RESIDUALS / "P8_Y5_R2FR_2934_LOG_DERIVATIVE_RESIDUAL_VECTOR.csv",
    "ellj": RESIDUALS / "P8_Y5_R2FR_2934_ELLJ_OWNER_SOURCE_CURRENT_AUDIT.csv",
    "transfer": RESIDUALS / "P8_Y5_R2FR_2934_DOTG_BOUND_TRANSFER_SCORECARD.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2934_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2934_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2934_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2934_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2934_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_copy": PARENT_ACTION / "DotG_to_kappa_projection_theorem_attempt_2934_NONCLAIM.csv",
    "transfer_copy": LOCAL_BOUNDS / "DotG_kappa_residual_transfer_scorecard_2934_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2934_R10_ALPHA_CURVE_OR_ELLJ_OWNER_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2934_00_2933_doc", SRC_2933_DOC, "NEXT2933_0_2934;G_eff=C_source*kappa_MTS;Validation overall: `True`", "2933 selected dotG-to-kappa projection theorem"),
        ("SRC2934_01_2933_next", SRC_2933_NEXT, "NEXT2933_0_2934;G_eff=C_source*kappa_MTS", "machine-readable 2934 target"),
        ("SRC2934_02_2933_projection", SRC_2933_PROJECTION, "PG2933_1_weak_field_map;PG2933_2_log_derivative;PG2933_5_verdict", "projection gate inherited from 2933"),
        ("SRC2934_03_2933_bound", SRC_2933_BOUND, "BND2933_0_dotG_over_G_messenger;10.1038/s41467-017-02558-1", "finite dotG/G comparator"),
        ("SRC2934_04_2933_first_value", SRC_2933_FIRST_VALUE, "FVS2933_0_first_value;FIRST_SOURCE_BACKED_COMPARATOR", "first value status"),
        ("SRC2934_05_2933_validation", SRC_2933_VALIDATION, "VAL2933_OVERALL;True", "2933 validation summary"),
        ("SRC2934_06_2932_bound", SRC_2932_BOUND_LEDGER, "CBL2932_0_dln_Geff_dt;CBL2932_7_delta_ellJ;CBL2932_8_total", "coupling acquisition rows"),
        ("SRC2934_07_2932_constant", SRC_2932_CONSTANT_AUDIT, "KLC2932_0_kappa_route;KLC2932_3_ellJ_owner;KLC2932_5_coupling_total", "kappa/ellJ theorem status"),
        ("SRC2934_08_2931_residual", SRC_2931_RESIDUAL, "CRD2931_5_coupling;Delta_coupling_source_abs", "coupling residual in source coefficient decomposition"),
        ("SRC2934_09_2928_coupling", SRC_2928_COUPLING, "CB2928_0_kappa_alpha3;CB2928_1_ellJ_alpha3;CB2928_3_coupling_total", "coupling baseline products"),
        ("SRC2934_10_2578_ledger", SRC_2578_LEDGER, "RES2578_7_delta_kappa;RES2578_8_delta_ellJ;RES2578_9_total", "PiM/Hamiltonian residual ledger"),
        ("SRC2934_11_2925_doc", SRC_2925_DOC, "RTL2925_0_statement;RV2925_TOTAL;Validation overall", "conditional local reduction theorem and residual vector"),
        ("SRC2934_12_2924_contract", SRC_2924_CONTRACT, "RED2924_1_constant_kappa;RED2924_3_universal_matter_descent;RED2924_7_integrable_Htau", "MTS-to-EH reduction contract"),
        ("SRC2934_13_2924_EH", SRC_2924_EH, "EHA2924_4_EH_weak_field;G0=kappa0", "EH weak-field target anchor"),
    ]
    rows = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    specs = [
        ("DTP2934_0_EH_reference", "EH weak-field reference", "linearized EH plus universal matter gives nabla^2 Phi=4*pi*G0*rho_H and G0=kappa0*c^4/(8*pi)", "REFERENCE_SIGNED_NOT_MTS", True, False, "2924 supplies the target reference"),
        ("DTP2934_1_MTS_metric_readout", "MTS observed metric readout", "g_readout=g_obs+O(Phi^2), no first-order Weyl/disformal/source slot", "UNSIGNED", False, True, "RED2924_0 remains missing"),
        ("DTP2934_2_EH_core_coefficient", "EH core coefficient inheritance", "local metric sector coefficient is kappa_MTS^-1 with no hidden H_core denominator", "UNSIGNED", False, True, "2924/2931 reject EH import as total MTS parent action"),
        ("DTP2934_3_source_current_descent", "source current normalization", "rho_source is the same parent J_H/M_H source current that appears in H_tau and matter descent", "UNSIGNED", False, True, "worldtube/source mass glue remains open"),
        ("DTP2934_4_ellJ_owner", "ell_J source-current scale owner", "ell_J is fixed before readout or p_J*D_t ln ell_J=0", "UNSIGNED", False, True, "2932 identified ell_J owner as open"),
        ("DTP2934_5_reference_frame", "reference/frame absorption silence", "D_t ln R_frame=0 and measured GM is not absorbing kappa/source drift", "UNSIGNED", False, True, "2933 still blocks arena transfer"),
        ("DTP2934_6_conditional_map", "conditional weak-field map", "If DTP2934_1..5 hold, G_eff=C_source*kappa_MTS*ell_J^p_J*R_frame and dotG/G=D_t ln G_eff", "CONDITIONAL_THEOREM_ONLY", True, True, "mathematically clean, current MTS clauses unsigned"),
        ("DTP2934_7_verdict", "dotG/G to D_t ln kappa_MTS projection", "dotG/G = D_t ln kappa_MTS", "NOT_DERIVED_CURRENT_MTS", False, True, "requires D_t ln C_source=p_J D_t ln ell_J=D_t ln R_frame=0"),
    ]
    return [
        add_common(
            {
                "theorem_id": theorem_id,
                "clause": clause,
                "required_identity": required_identity,
                "status": status,
                "mathematical_step_valid": mathematical_step_valid,
                "blocks_projection_claim": blocks_projection_claim,
                "reason": reason,
                "source_paths": ";".join(str(path) for path in [SRC_2924_CONTRACT, SRC_2924_EH, SRC_2925_DOC, SRC_2933_PROJECTION]),
            }
        )
        for theorem_id, clause, required_identity, status, mathematical_step_valid, blocks_projection_claim, reason in specs
    ]


def residual_rows() -> list[dict[str, Any]]:
    b = DOTG_BOUND_PER_YEAR
    t = TARGET_2932_PER_YEAR
    specs = [
        ("LDR2934_0_observed", "D_t ln G_eff", "external comparator", "|D_t ln G_eff| <= B_dotG", b, "yr^-1", "source_backed_bound", True),
        ("LDR2934_1_kappa", "D_t ln kappa_MTS", "desired MTS coupling residual", "D_t ln kappa_MTS", "", "yr^-1", "projection_target", False),
        ("LDR2934_2_ellJ", "p_J D_t ln ell_J", "source-current scale residual", "p_J D_t ln ell_J", "", "yr^-1", "missing_owner_or_bound", False),
        ("LDR2934_3_source", "D_t ln C_source", "source normalization residual", "D_t ln C_source", "", "yr^-1", "missing_source_current_theorem", False),
        ("LDR2934_4_frame", "D_t ln R_frame", "reference/frame/domain residual", "D_t ln R_frame", "", "yr^-1", "missing_reference_frame_silence", False),
        ("LDR2934_5_identity", "Delta_dotG_projection", "exact projection residual identity", "D_t ln G_eff - D_t ln kappa_MTS = p_J D_t ln ell_J + D_t ln C_source + D_t ln R_frame", "", "yr^-1", "exact_identity_nonclaim", True),
        ("LDR2934_6_bound_formula", "bound_on_Dln_kappa", "triangle bound formula", "|D_t ln kappa_MTS| <= B_dotG + |p_J D_t ln ell_J| + |D_t ln C_source| + |D_t ln R_frame|", b, "yr^-1_plus_missing_terms", "conditional_bound_only", True),
        ("LDR2934_7_target_comparison", "target_gap", "MESSENGER bound versus 2932 target", "B_dotG / target_2932 = 4.166666666666667", b / t, "dimensionless", "source_bound_weaker_than_target", True),
    ]
    return [
        add_common(
            {
                "residual_id": residual_id,
                "symbol": symbol,
                "role": role,
                "expression": expression,
                "known_value": known_value,
                "units": units,
                "status": status,
                "mathematically_exact": mathematically_exact,
                "source_paths": ";".join(str(path) for path in [SRC_2933_BOUND, SRC_2933_PROJECTION, SRC_2932_BOUND_LEDGER]),
            }
        )
        for residual_id, symbol, role, expression, known_value, units, status, mathematically_exact in specs
    ]


def ellj_rows() -> list[dict[str, Any]]:
    specs = [
        ("EJO2934_0_definition", "definition", "ell_J is a parent source-current normalization scale, not a fitted post-readout knob", "NAMED_NOT_OWNED", False, "2932/2933 name it but do not derive owner"),
        ("EJO2934_1_matter_descent", "matter descent", "S_matter descends to ordinary universal matter with same J_H in H_tau and stress tensor", "UNSIGNED", False, "RED2924_3 remains open"),
        ("EJO2934_2_ward_identity", "Ward/source identity", "nabla_mu T^{mu nu}=0 same source current after quotient and boundary projection", "UNSIGNED", False, "needed to stop source-current scale drift"),
        ("EJO2934_3_unit_policy", "unit/reference policy", "ell_J is fixed by units/reference before observational fitting", "UNSIGNED", False, "otherwise measured GM can absorb it"),
        ("EJO2934_4_log_zero", "log derivative zero", "D_t ln ell_J=0 and D_A ln ell_J=0 on local branch", "NOT_DERIVED", False, "no parent owner theorem yet"),
        ("EJO2934_5_verdict", "ellJ owner theorem", "p_J D_t ln ell_J=0 in dotG projection", "OWNER_THEOREM_NOT_DERIVED", False, "must remain an active residual head"),
    ]
    return [
        add_common(
            {
                "ellj_id": ellj_id,
                "clause": clause,
                "required_identity": required_identity,
                "status": status,
                "condition_passed": condition_passed,
                "reason": reason,
                "source_paths": ";".join(str(path) for path in [SRC_2932_CONSTANT_AUDIT, SRC_2924_CONTRACT, SRC_2578_LEDGER]),
            }
        )
        for ellj_id, clause, required_identity, status, condition_passed, reason in specs
    ]


def transfer_rows() -> list[dict[str, Any]]:
    missing_envelope = "MISSING: |p_J D_t ln ell_J| + |D_t ln C_source| + |D_t ln R_frame|"
    return [
        add_common(
            {
                "transfer_id": "DTS2934_0_external_bound",
                "quantity": "|D_t ln G_eff|",
                "value": DOTG_BOUND_PER_YEAR,
                "units": "yr^-1",
                "source_backed": True,
                "formula": "|dotG/G| <= 4.0e-14 yr^-1",
                "target_2932": TARGET_2932_PER_YEAR,
                "target_pass": DOTG_BOUND_PER_YEAR <= TARGET_2932_PER_YEAR,
                "projection_ready": False,
                "verdict": "FINITE_COMPARATOR_ONLY",
            }
        ),
        add_common(
            {
                "transfer_id": "DTS2934_1_kappa_bound_formula",
                "quantity": "|D_t ln kappa_MTS|",
                "value": f"4.0e-14 + {missing_envelope}",
                "units": "yr^-1",
                "source_backed": False,
                "formula": "|Dln kappa| <= B_dotG + |ellJ term| + |source term| + |frame term|",
                "target_2932": TARGET_2932_PER_YEAR,
                "target_pass": False,
                "projection_ready": False,
                "verdict": "BOUND_FORMULA_DERIVED_VALUES_MISSING",
            }
        ),
        add_common(
            {
                "transfer_id": "DTS2934_2_zero_route",
                "quantity": "projection residual",
                "value": "0 only if D_t ln C_source=p_J D_t ln ell_J=D_t ln R_frame=0",
                "units": "yr^-1",
                "source_backed": False,
                "formula": "Delta_dotG_projection=0",
                "target_2932": 0,
                "target_pass": False,
                "projection_ready": False,
                "verdict": "ZERO_ROUTE_UNSIGNED",
            }
        ),
        add_common(
            {
                "transfer_id": "DTS2934_3_decision",
                "quantity": "next_useful_test",
                "value": "R10 alpha(lambda) real curve or ellJ/source owner theorem",
                "units": "route",
                "source_backed": True,
                "formula": "if dotG bound is weaker than target and projection unsigned, attack independent local range/source test",
                "target_2932": "",
                "target_pass": False,
                "projection_ready": False,
                "verdict": "MOVE_TO_R10_ALPHA_CURVE_OR_ELLJ_OWNER",
            }
        ),
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2934_0_conditional_theorem", "conditional dotG-to-kappa projection theorem shape exists", "PASS_CONDITIONAL_NONCLAIM", "the exact residual identity and required clauses are now explicit", True),
        ("CG2934_1_current_projection", "current MTS proves dotG/G=D_t ln kappa_MTS", "BLOCKED_NONCLAIM", "C_source, ell_J and R_frame clauses are unsigned", False),
        ("CG2934_2_kappa_bound", "MESSENGER bound constrains D_t ln kappa_MTS for MTS", "BLOCKED_NONCLAIM", "only valid after projection residual heads are zero or bounded", False),
        ("CG2934_3_ellJ_owner", "ell_J source-current normalization owner is derived", "BLOCKED_NONCLAIM", "owner theorem remains open", False),
        ("CG2934_4_local_GR", "local GR/Newton recovery follows", "BLOCKED_NONCLAIM", "coupling/source map not closed", False),
        ("CG2934_5_no_public_claim", "any empirical/public claim is promoted", "NO_PROMOTION_ALLOWED", "2934 is private theorem gate work", False),
    ]
    return [
        add_common(
            {
                "claim_id": claim_id,
                "claim": claim,
                "status": status,
                "reason": reason,
                "condition_passed": condition_passed,
            }
        )
        for claim_id, claim, status, reason, condition_passed in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2934_0_gain", "keep the exact projection residual identity", "it prevents false wins and gives the precise terms that must vanish", "use as gate for all future dotG/local-coupling claims"),
        ("DEC2934_1_bound", "do not use MESSENGER as a kappa pass", "the source bound is weaker than the 2932 target and projection is unsigned", "retain comparator only"),
        ("DEC2934_2_ellJ", "ell_J remains the live coupling gap", "without an owner theorem it can mimic or absorb source drift", "attack source-current normalization or independently bound ell_J"),
        ("DEC2934_3_next", "move to R10 alpha(lambda) real curve or ellJ owner theorem", "dotG path cannot score until projection residuals close", "2935 should acquire a real alpha(lambda) curve or derive source-current owner"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "action": action,
            }
        )
        for decision_id, decision, reason, action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2934_0_2935",
                "selection": "selected_primary",
                "target_doc": "2935-Y5-R2FR-R10-alpha-lambda-real-curve-or-ellJ-source-current-owner-theorem-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_R10_alpha_lambda_real_curve_or_ellJ_source_current_owner_theorem_under_AX1090_2935.py",
                "objective": "either acquire a real source-backed R10 alpha(lambda) curve/anchor set for kappa range dependence, or derive the ell_J source-current owner theorem needed by the dotG projection",
                "acceptance_gate": "no local-GR/R10 claim unless rows are numeric, sourced, projection-ready, and all valid_for_claim gates remain false until parent clauses close",
                "fallback": "if full R10 curve extraction is unavailable, create source-backed anchor-only nonclaim rows and keep the theorem route open",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("theorem_copy", OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_copy"]),
        ("transfer_copy", OUTPUTS["transfer"], BRANCH_OUTPUTS["transfer_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows = []
    for copy_id, source_path, destination_path in specs:
        shutil.copyfile(source_path, destination_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source_path),
                    "destination_path": str(destination_path),
                    "source_exists": source_path.exists(),
                    "destination_exists": destination_path.exists(),
                    "destination_parses": csv_parses(destination_path),
                }
            )
        )
    return rows


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values())
    branch_paths = list(BRANCH_OUTPUTS.values())
    theorem_ids = {row["theorem_id"] for row in rows_by_name["theorem"]}
    residual_ids = {row["residual_id"] for row in rows_by_name["residual"]}
    ellj_ids = {row["ellj_id"] for row in rows_by_name["ellj"]}
    no_claims = all(not as_bool(row.get("valid_for_claim")) and not as_bool(row.get("claim_allowed")) for rows in rows_by_name.values() for row in rows)
    no_predictions = all(not as_bool(row.get("score_ready")) and not as_bool(row.get("valid_prediction_row")) for rows in rows_by_name.values() for row in rows)
    local_sources_ok = all(as_bool(row["path_exists"]) and as_bool(row["anchors_found"]) for row in rows_by_name["sources"])
    transfer_bound_row = next(row for row in rows_by_name["transfer"] if row["transfer_id"] == "DTS2934_0_external_bound")
    formalization_output_count = sum(1 for path in output_paths + branch_paths + [DOC] if is_under(path, FORMALIZATION))
    checks = [
        ("VAL2934_0_sources_exist_and_anchored", local_sources_ok, "all local sources exist and anchors are found"),
        ("VAL2934_1_theorem_clauses_complete", {"DTP2934_0_EH_reference", "DTP2934_7_verdict"}.issubset(theorem_ids), "projection theorem attempt includes reference and verdict"),
        ("VAL2934_2_residual_identity_present", "LDR2934_5_identity" in residual_ids and "LDR2934_6_bound_formula" in residual_ids, "exact log residual identity and bound formula present"),
        ("VAL2934_3_ellJ_owner_audited", "EJO2934_5_verdict" in ellj_ids, "ellJ owner verdict audited"),
        ("VAL2934_4_transfer_bound_positive", float(transfer_bound_row["value"]) > 0 and transfer_bound_row["units"] == "yr^-1", "dotG transfer bound positive numeric with units"),
        ("VAL2934_5_transfer_not_promoted", not as_bool(transfer_bound_row["projection_ready"]) and not as_bool(transfer_bound_row["target_pass"]), "dotG comparator is not promoted to kappa pass"),
        ("VAL2934_6_no_claims_promoted", no_claims, "no 2934 row is valid_for_claim"),
        ("VAL2934_7_no_prediction_rows", no_predictions, "no score-ready prediction rows emitted"),
        ("VAL2934_8_outputs_parse", all(csv_parses(path) for path in output_paths), "all 2934 output CSVs parse"),
        ("VAL2934_9_branch_copies_parse", all(csv_parses(path) for path in branch_paths), "all branch copy CSVs parse"),
        ("VAL2934_10_doc_exists", DOC.exists(), "2934 markdown doc exists"),
        ("VAL2934_11_next_target_selected", rows_by_name["next"][0]["target_doc"].startswith("2935-"), "2935 target selected"),
        ("VAL2934_12_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in output_paths + branch_paths + [DOC]), "all outputs remain under post-checkpoint-work"),
        ("VAL2934_13_sources_not_formalization", not any(is_under(Path(row["source_path"]), FORMALIZATION) for row in rows_by_name["sources"]), "no formalization-workbench source dependency"),
        ("VAL2934_14_no_formalization_2934_outputs", formalization_output_count == 0, "no formalization-workbench 2934 outputs"),
    ]
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": True,
            }
        )
        for validation_id, passed, check in checks
    ]
    rows.append(
        add_common(
            {
                "validation_id": "VAL2934_OVERALL",
                "passed": all(as_bool(row["passed"]) for row in rows),
                "check": "2934 validation overall",
                "required": True,
            }
        )
    )
    return rows


def render_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    status = "Y5_R2FR_2934_conditional_dotG_projection_theorem_written_current_MTS_projection_blocked_R10_or_ellJ_2935_next"
    claim_ceiling = "conditional_projection_theorem_yes_current_kappa_bound_no_ellJ_owner_no_local_GR_no_Newton_no_R10_no_GitHub_claim"
    return "\n\n".join(
        [
            "# 2934 — Y5 R2FR: dotG-to-kappa projection theorem or ellJ owner/source-current normalization under AX1090",
            f"Status: `{status}`",
            f"Claim ceiling: `{claim_ceiling}`",
            "## Summary",
            (
                "2934 derives the exact projection shape but does not promote it. "
                "The conditional theorem is clean: if the local weak-field branch has universal metric readout, EH-core coefficient inheritance, "
                "same-source matter descent, fixed `ell_J`, and no reference/frame absorption, then "
                "`dotG/G = D_t ln G_eff` and the residual against kappa is explicit."
            ),
            (
                "The exact residual identity is:\n\n"
                "`D_t ln G_eff - D_t ln kappa_MTS = p_J D_t ln ell_J + D_t ln C_source + D_t ln R_frame`.\n\n"
                "So the MESSENGER bound only becomes a `kappa_MTS` bound after the right-hand side is theorem-zero or independently bounded."
            ),
            "## Source Register",
            md_table(rows_by_name["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"]),
            "## Projection Theorem Attempt",
            md_table(rows_by_name["theorem"], ["theorem_id", "clause", "required_identity", "status", "mathematical_step_valid", "blocks_projection_claim", "reason"]),
            "## Log-Derivative Residual Vector",
            md_table(rows_by_name["residual"], ["residual_id", "symbol", "role", "expression", "known_value", "units", "status", "mathematically_exact"]),
            "## ellJ Owner Audit",
            md_table(rows_by_name["ellj"], ["ellj_id", "clause", "required_identity", "status", "condition_passed", "reason"]),
            "## dotG Bound Transfer Scorecard",
            md_table(rows_by_name["transfer"], ["transfer_id", "quantity", "value", "units", "source_backed", "formula", "target_2932", "target_pass", "projection_ready", "verdict"]),
            "## Claim Gates",
            md_table(rows_by_name["claims"], ["claim_id", "claim", "status", "condition_passed", "reason"]),
            "## Decisions",
            md_table(rows_by_name["decision"], ["decision_id", "decision", "reason", "action"]),
            "## Next Target",
            md_table(rows_by_name["next"], ["next_id", "selection", "target_doc", "target_script", "objective", "acceptance_gate", "fallback"]),
            "## Branch Copies",
            md_table(rows_by_name["branches"], ["copy_id", "source_path", "destination_path", "source_exists", "destination_exists", "destination_parses"]),
            "## Validation",
            md_table(rows_by_name["validation"], ["validation_id", "passed", "check", "required"]),
            f"Validation overall: `{rows_by_name['validation'][-1]['passed']}`.",
            "## Bottom Line",
            (
                "This is a real derivation gain but not a theory pass. We now know the exact equation that must close before local `dotG/G` data can constrain "
                "`kappa_MTS`. The unresolved pieces are no longer vague: `ell_J` ownership, `C_source` source normalization, and `R_frame` reference/domain silence. "
                "Since the existing MESSENGER bound is also weaker than the 2932 target by a factor of 4.1667, the best next move is either a real R10 `alpha(lambda)` curve "
                "or the `ell_J` owner theorem."
            ),
            "## Non-Claims",
            "- no `dotG/G = D_t ln kappa_MTS` claim is made;\n- no `ell_J` source-current owner theorem is claimed;\n- no local-GR/Newton/R10 pass is claimed;\n- no GitHub/public claim is made.",
        ]
    ) + "\n"


def main() -> None:
    rows_by_name: dict[str, list[dict[str, Any]]] = {}
    rows_by_name["sources"] = source_register_rows()
    rows_by_name["theorem"] = theorem_rows()
    rows_by_name["residual"] = residual_rows()
    rows_by_name["ellj"] = ellj_rows()
    rows_by_name["transfer"] = transfer_rows()
    rows_by_name["claims"] = claim_rows()
    rows_by_name["decision"] = decision_rows()
    rows_by_name["next"] = next_rows()

    for key in ["sources", "theorem", "residual", "ellj", "transfer", "claims", "decision", "next"]:
        write_csv(OUTPUTS[key], rows_by_name[key])

    rows_by_name["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows_by_name["branches"])

    DOC.write_text("# 2934 — validation pending\n", encoding="utf-8")
    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    DOC.write_text(render_doc(rows_by_name), encoding="utf-8")

    print(f"wrote {DOC}")
    print(f"validation overall: {rows_by_name['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()
