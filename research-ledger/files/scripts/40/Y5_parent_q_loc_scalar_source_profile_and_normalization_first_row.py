from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1522-Y5-parent-q_loc-scalar-source-profile-and-normalization-first-row.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1521_doc": ROOT / "1521-Y5-parent-q_loc-to-qR-bridge-or-weak-field-operator-source-profile.md",
    "1521_next": OUT / "P8_Y5_PARENT_QLOC_1521_NEXT_TARGET.csv",
    "1521_bridge": OUT / "P8_Y5_PARENT_QLOC_1521_QLOC_TO_QR_BRIDGE_AUDIT.csv",
    "1521_operator": OUT / "P8_Y5_PARENT_QLOC_1521_WEAK_FIELD_OPERATOR_SOURCE_PROFILE.csv",
    "1521_runner": OUT / "P8_Y5_PARENT_QLOC_1521_QLOC_GAMMA_RUNNER_UPDATE.csv",
    "1521_validation": OUT / "P8_Y5_BRR545_1521_VALIDATION.csv",
    "1365_qbound": OUT / "P8_Y5_R10_1365_QLOC_BOUND_SOURCE_ROW.csv",
    "1366_envelope": OUT / "P8_Y5_R10_1366_QLOC_ENVELOPE_INTAKE_ROWS.csv",
    "798_gamma": OUT / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
    "1289_kernel": OUT / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
    "1367_kernel": OUT / "P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv",
    "1368_projection": OUT / "P8_Y5_R10_1368_QLOC_TO_PPN_GAMMA_PROJECTION_REQUIREMENTS.csv",
    "1369_runner": OUT / "P8_Y5_R10_1369_QLOC_GAMMA_RUNNER_SCHEMA.csv",
    "1240_qr_map": OUT / "P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv",
    "1244_policy": OUT / "P8_Y5_R10_1244_RUNNER_POLICY_FEED.csv",
    "1181_ppn": OUT / "P8_Y5_R10_1181_EXTERNAL_PPN_SOURCE_REGISTER.csv",
    "776_kgamma": OUT / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1522_SOURCE_REGISTER.csv"
SCALAR_PROFILE_DERIVATION = OUT / "P8_Y5_PARENT_QLOC_1522_SCALAR_SOURCE_PROFILE_DERIVATION.csv"
NORMALIZATION_FIRST_ROW = OUT / "P8_Y5_PARENT_QLOC_1522_NORMALIZATION_FIRST_ROW_SCHEMA.csv"
GAUSS_GREEN_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1522_GAUSS_GREEN_CONTRACT.csv"
RUNNER_ROW = OUT / "P8_Y5_PARENT_QLOC_1522_QLOC_PROFILE_RUNNER_ROW.csv"
RETAINED_GAPS = OUT / "P8_Y5_PARENT_QLOC_1522_RETAINED_GAP_LEDGER.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1522_REJECTION_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1522_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1522_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_QLOC_1522_LOCAL_GR_NEWTON_STATUS.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1522_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1522_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1522"
QUAR_PROFILE = QUARANTINE / "QLOC_SCALAR_SOURCE_PROFILE_DERIVATION_NONCLAIM.csv"
QUAR_NORM = QUARANTINE / "QLOC_NORMALIZATION_FIRST_ROW_SCHEMA_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "QLOC_PROFILE_RUNNER_ROW_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "QLOC_DECISION_NONCLAIM.csv"
BRANCH_PROFILE = BRANCH_RESIDUALS / "q_loc_scalar_source_profile_derivation_nonclaim_1522.csv"
BRANCH_NORM = BRANCH_RESIDUALS / "q_loc_normalization_first_row_schema_nonclaim_1522.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "q_loc_profile_runner_row_nonclaim_1522.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "q_loc_decision_nonclaim_1522.csv"


def flags() -> dict[str, bool]:
    return {
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source_id, (key, path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1522_{source_id}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "purpose": "input evidence for q_loc scalar source profile and normalization first row",
                **flags(),
            }
        )
    return rows


def scalar_profile_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SP1522_0_qloc_definition",
            "q_loc^nu",
            "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "DEFINITION_INHERITED",
            "P_loc, units, K_hat, and scalar projection are still missing",
            source_list("1365_qbound", "1366_envelope"),
        ),
        (
            "SP1522_1_scalar_projection",
            "S_q",
            "S_q := Pi_gamma[ q_loc ] := R_scalar P_obs P_loc(nabla Gamma_eff - div K_hat)",
            "PROFILE_SCHEMA_WRITTEN",
            "Pi_gamma/R_scalar/P_obs are not yet sourced or gauge-fixed",
            source_list("1521_operator", "1368_projection"),
        ),
        (
            "SP1522_2_Gamma_gradient_seed",
            "nabla Gamma_eff",
            "nabla Gamma_eff = L_cg^-2 F'(m)nabla m - 2 L_cg^-3 F(m)nabla L_cg",
            "SOURCE_BACKED_FORMULA_SHAPE_NONCLAIM",
            "needs m profile, L_cg profile/silence, units, support powers, and boundary behavior",
            source_list("798_gamma", "1366_envelope"),
        ),
        (
            "SP1522_3_locked_quadratic_branch",
            "local locked branch",
            "if L_cg=L_* and F'(m_*)=0, the m-gradient channel starts quadratically in delta m",
            "CONDITIONAL_SUPPRESSION_ONLY",
            "parent m_* lock, F' zero theorem, source powers pS/pL/pT, and transition width are unsigned",
            source_list("798_gamma", "1289_kernel"),
        ),
        (
            "SP1522_4_Khat_subtraction",
            "div K_hat",
            "S_q needs the same scalar projection of div K_hat or DeltaK=K_hat-K_metric[Gamma_eff]",
            "MISSING_KHAT_SCALAR_PROFILE",
            "K_hat components, K_metric kernels, DeltaK units, and boundary terms are missing",
            source_list("1289_kernel", "1367_kernel", "776_kgamma"),
        ),
        (
            "SP1522_5_source_profile_verdict",
            "current S_q(r,x)",
            "finite scalar-channel source profile for weak-field operator or q_R bridge",
            "MISSING_SOURCE_PROFILE",
            "no scoreable S_q row exists; first row remains schema-only",
            source_list("1521_operator", "1365_qbound", "1366_envelope"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "profile_id": profile_id,
            "quantity": quantity,
            "formula_or_requirement": formula,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": sources,
            **flags(),
        }
        for profile_id, quantity, formula, status, missing, sources in rows
    ]


def normalization_rows() -> list[dict[str, Any]]:
    rows = [
        ("NORM1522_0_system", "system_id", "local source/test body identifier", "MISSING_SYSTEM_ID", "must match PPN/GM source convention"),
        ("NORM1522_1_source_body", "source_body", "Sun or explicitly named central source for PPN comparator", "MISSING_SOURCE_BODY", "cannot borrow generic GM"),
        ("NORM1522_2_GM", "G M_source", "measured GM in the same convention used by the comparator", "MISSING_GM_SOURCE_VALUE", "do not infer GM from MTS fit"),
        ("NORM1522_3_coordinate", "coordinate_convention", "areal-radial weak-field convention or explicit correction", "MISSING_COORDINATE_CONVENTION", "must match QMAP1240/Cassini map"),
        ("NORM1522_4_operator", "L_PPN and R_gamma", "linearized operator and readout used to convert S_q into gamma_minus_1", "MISSING_OPERATOR_READOUT", "no response coefficient without this"),
        ("NORM1522_5_scalar_source", "S_q profile", "source-backed scalar-channel q_loc profile with units/support/domain", "MISSING_S_Q_PROFILE", "main missing row"),
        ("NORM1522_6_integral", "Q_loc functional", "Q_loc = G_ext[S_q] under fixed sign and boundary convention", "MISSING_GREEN_FUNCTION_CONSTANT", "must prove relation to exterior Q_R/r if using q_R bridge"),
        ("NORM1522_7_dimensionless", "q_loc_hat", "q_loc_hat = Q_loc c^2/(G M_source) or direct dimensionless source-backed value", "MISSING_QLOC_HAT", "cannot use Cassini without finite q_loc_hat"),
        ("NORM1522_8_retained_channels", "DeltaK/boundary/source channel bounds", "zero-derived or independently bounded retained channels", "MISSING_CHANNEL_BOUNDS", "no cancellation"),
        ("NORM1522_9_acceptance", "first-row acceptance", "all fields source-backed, units compatible, no MISSING markers", "CLAIM_BLOCKED", "runner cannot score"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "row_id": row_id,
            "field": field,
            "required_value": required,
            "current_value": current,
            "guard": guard,
            "source_paths": source_list("1244_policy", "1521_operator", "1521_bridge"),
            **flags(),
        }
        for row_id, field, required, current, guard in rows
    ]


def gauss_green_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "GG1522_0_static_scalar_operator",
            "static scalar reduction",
            "if L_PPN scalar channel reduces to nabla^2 R_AB = C_op S_q in the exterior-matched gauge",
            "CONDITIONAL_OPERATOR_TEMPLATE",
            "C_op, sign, gauge, and boundary conditions missing",
        ),
        (
            "GG1522_1_exterior_solution",
            "compact source exterior",
            "for compact S_q and R_AB(infinity)=0, exterior R_AB(r) = -Q_loc/r under the Q_R sign convention",
            "CONDITIONAL_GAUSS_LAW",
            "only after operator normalization fixes Q_loc = G_ext[S_q]",
        ),
        (
            "GG1522_2_qR_bridge",
            "q_loc_hat to q_R_hat",
            "q_loc_hat = q_R_hat only if Q_loc equals Q_R with same GM/source/sign convention and retained channels vanish",
            "BRIDGE_CONDITION_WRITTEN",
            "current corpus has no Q_loc integral or channel bounds",
        ),
        (
            "GG1522_3_claim_status",
            "current q_loc scalar source law",
            "current MTS supplies a source-backed S_q and Q_loc",
            "NOT_CLAIMED",
            "schema is useful but not scoreable",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "piece": piece,
            "conditional_law": law,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("1240_qr_map", "1521_bridge", "1521_operator"),
            **flags(),
        }
        for contract_id, piece, law, status, missing in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1522_0_profile_blocked",
            "branch": "q_loc_scalar_profile_first_row",
            "S_q_profile": "MISSING_S_Q_PROFILE",
            "Q_loc": "MISSING_QLOC_INTEGRAL",
            "q_loc_hat": "MISSING_QLOC_HAT",
            "operator_readout": "MISSING_L_PPN_AND_R_GAMMA",
            "C_qgamma": "MISSING_WEAK_FIELD_RESPONSE",
            "sigma_gamma": "2.3e-05",
            "q_R_guardrail": "4.6e-05_COMPARATOR_ONLY",
            "result": "BLOCKED_MISSING_PROFILE_NORMALIZATION_OPERATOR",
            "source_paths": source_list("1521_runner", "1244_policy", "1369_runner"),
            **flags(),
        }
    ]


def retained_gap_rows() -> list[dict[str, Any]]:
    rows = [
        ("GAP1522_0_Ploc", "P_loc definition", "MISSING", "cannot decide what part of q_loc is local physical scalar channel"),
        ("GAP1522_1_Pigamma", "Pi_gamma/R_scalar weak-field projector", "MISSING", "cannot map q_loc to gamma slip"),
        ("GAP1522_2_units", "q_loc/S_q units", "MISSING", "cannot normalize q_loc_hat"),
        ("GAP1522_3_m_profile", "m profile and support powers", "MISSING", "Gamma gradient seed not numerical/source-backed"),
        ("GAP1522_4_Lcg_profile", "L_cg silence/profile", "CONDITIONAL_ONLY", "L_cg fixed route not parent-signed"),
        ("GAP1522_5_Khat", "K_hat/DeltaK scalar profile", "MISSING", "stress-divergence subtraction remains open"),
        ("GAP1522_6_boundary", "boundary/source/no-flux profile", "MISSING", "exterior hair sign and retained-channel silence not proved"),
        ("GAP1522_7_acceptance", "gap closure", "CLAIM_BLOCKED", "all gaps must be filled or theorem-zeroed"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gap_id": gap_id,
            "missing_piece": piece,
            "status": status,
            "why_it_matters": why,
            "source_paths": source_list("1365_qbound", "1366_envelope", "1521_operator"),
            **flags(),
        }
        for gap_id, piece, status, why in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1522_0_raw_qloc", "treat raw q_loc vector as scalar PPN source", "REJECTED", "needs Pi_gamma scalar projection and gauge/readout"),
        ("REJ1522_1_gamma_only", "use Gamma_eff gradient without K_hat subtraction", "REJECTED", "q_loc definition includes div K_hat and DeltaK gap"),
        ("REJ1522_2_qR_guardrail", "use q_R guardrail before q_loc_hat exists", "REJECTED", "normalization and bridge are missing"),
        ("REJ1522_3_screening_words", "claim profile suppression from screening language only", "REJECTED", "needs m/Lcg profiles, support powers, transition width, and boundary row"),
        ("REJ1522_4_cancellation", "let DeltaK/boundary/source channels cancel S_q", "REJECTED", "independent zero/bounds required"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "shortcut": shortcut,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for rejection_id, shortcut, status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1522_0_qloc_formula", "base q_loc formula exists", "PASS_NONCLAIM", "P_loc(nabla Gamma_eff - div Khat) is inherited", False),
        ("GATE1522_1_scalar_profile", "S_q profile is source-backed", "BLOCKED", "Pi_gamma, units, m/Lcg profile, Khat, and support are missing", False),
        ("GATE1522_2_normalization", "q_loc_hat is finite and normalized", "BLOCKED", "Q_loc integral, GM convention, and operator constant are missing", False),
        ("GATE1522_3_qR_bridge", "q_loc_hat equals q_R_hat", "BLOCKED", "exterior source integral and retained-channel silence are missing", False),
        ("GATE1522_4_runner_score", "PPN/Cassini q_loc runner can score", "BLOCKED", "profile/normalization/operator rows missing", False),
        ("GATE1522_5_local_GR", "local GR/Newton claim can be made", "BLOCKED_NO_CLAIM", "q_loc response and M_H_ref/source normalization remain open", False),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "gate_pass": gate_pass,
            **flags(),
        }
        for gate_id, claim, status, reason, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC1522_0_profile_schema", "Promote S_q from vague target to explicit first-row schema.", "SCHEMA_WRITTEN_NONCLAIM", "we now know what must be sourced before weak-field scoring."),
        ("DEC1522_1_gauss_contract", "Retain the static Gauss/Green bridge as conditional law.", "CONDITIONAL_CONTRACT_ONLY", "it explains how a scalar source would become exterior Q_R hair without claiming it happens."),
        ("DEC1522_2_next", "Next target is the P_loc/Pi_gamma scalar projector and units ledger.", "NEXT_1523_PROJECTOR_UNITS", "without the scalar projector and units, S_q cannot be promoted or normalized."),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in rows
    ]


def local_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("LOCAL1522_0_profile", "q_loc scalar profile", "SCHEMA_ONLY", "S_q row exists but is not source-backed"),
        ("LOCAL1522_1_qR", "q_loc to q_R bridge", "NOT_PROVED", "Q_loc integral and q_loc_hat missing"),
        ("LOCAL1522_2_PPN", "Cassini/PPN scoring", "NOT_CLAIMED", "runner blocks missing profile/operator/normalization"),
        ("LOCAL1522_3_GR", "derived local GR", "NOT_CLAIMED", "q_loc response and source denominator remain open"),
        ("LOCAL1522_4_next", "next repair", "PROJECTOR_UNITS_TARGET", "derive P_loc/Pi_gamma and units before profile scoring"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "claim": claim,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for status_id, claim, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1522_0_1523",
            "next_target": "1523-Y5-parent-P_loc-Pi_gamma-scalar-projector-and-units-ledger.md",
            "script": "scripts/Y5_parent_P_loc_Pi_gamma_scalar_projector_and_units_ledger.py",
            "objective": "derive or source the local projector P_loc, scalar weak-field projector Pi_gamma/R_scalar, and q_loc/S_q units needed to promote the 1522 source-profile schema",
            "do_not": "do not score PPN/Cassini, do not import q_R, do not ignore K_hat/DeltaK/boundary channels, and do not claim local GR",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (SCALAR_PROFILE_DERIVATION, QUAR_PROFILE),
        (NORMALIZATION_FIRST_ROW, QUAR_NORM),
        (RUNNER_ROW, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (SCALAR_PROFILE_DERIVATION, BRANCH_PROFILE),
        (NORMALIZATION_FIRST_ROW, BRANCH_NORM),
        (RUNNER_ROW, BRANCH_RUNNER),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    profile = read_csv(SCALAR_PROFILE_DERIVATION)
    norm = read_csv(NORMALIZATION_FIRST_ROW)
    gauss = read_csv(GAUSS_GREEN_CONTRACT)
    runner = read_csv(RUNNER_ROW)
    gaps = read_csv(RETAINED_GAPS)
    rejections = read_csv(REJECTION_LEDGER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1522_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1522 input source paths exist"),
        ("VAL1522_1_profile_schema_written", any(row["profile_id"] == "SP1522_1_scalar_projection" and row["status"] == "PROFILE_SCHEMA_WRITTEN" for row in profile), "S_q scalar projection schema is written"),
        ("VAL1522_2_profile_not_promoted", any(row["profile_id"] == "SP1522_5_source_profile_verdict" and row["status"] == "MISSING_SOURCE_PROFILE" for row in profile), "source-backed S_q profile remains missing"),
        ("VAL1522_3_normalization_missing", any(row["field"] == "q_loc_hat" and "MISSING" in row["current_value"] for row in norm), "q_loc_hat normalization remains missing"),
        ("VAL1522_4_gauss_conditional", any(row["contract_id"] == "GG1522_1_exterior_solution" and row["status"] == "CONDITIONAL_GAUSS_LAW" for row in gauss), "Gauss/Green exterior law is conditional only"),
        ("VAL1522_5_runner_blocked", any(row["runner_id"] == "RUN1522_0_profile_blocked" and row["result"] == "BLOCKED_MISSING_PROFILE_NORMALIZATION_OPERATOR" for row in runner), "runner refuses missing profile/normalization/operator inputs"),
        ("VAL1522_6_gaps_complete", len(gaps) >= 8 and any(row["gap_id"] == "GAP1522_7_acceptance" and row["status"] == "CLAIM_BLOCKED" for row in gaps), "gap ledger blocks promotion"),
        ("VAL1522_7_rejections_guardrails", len(rejections) >= 5 and all(row["status"] == "REJECTED" for row in rejections), "raw qloc, gamma-only, qR guardrail, screening-word, and cancellation shortcuts rejected"),
        ("VAL1522_8_claim_gates_block_claim", any(row["gate_id"] == "GATE1522_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1522_9_decision_next", any(row["result"] == "NEXT_1523_PROJECTOR_UNITS" for row in decisions), "decision selects P_loc/Pi_gamma projector and units target"),
        ("VAL1522_10_next_target", any("1523-Y5-parent-P_loc-Pi_gamma" in row["next_target"] for row in next_rows), "next target is scalar projector and units ledger"),
        ("VAL1522_11_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1522 CSVs parse cleanly"),
        ("VAL1522_12_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1522_13_branch_copies", all(path.exists() for path in [QUAR_PROFILE, QUAR_NORM, QUAR_RUNNER, QUAR_DECISION, BRANCH_PROFILE, BRANCH_NORM, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1522_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1522_15_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1522_16_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1522 writes the q_loc scalar source-profile and normalization first-row schema, keeps it nonclaim, and selects P_loc/Pi_gamma/projector units next"
            if overall
            else "1522 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
            + " |"
        )
    return "\n".join(output)


def write_doc(
    sources: list[dict[str, Any]],
    profile: list[dict[str, Any]],
    norm: list[dict[str, Any]],
    gauss: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    local_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1522 - Parent q_loc Scalar Source Profile and Normalization First Row",
                "",
                "## Verdict",
                "- `q_loc` now has an explicit scalar-channel source-profile schema: `S_q := Pi_gamma[q_loc]`, not raw vector `q_loc`.",
                "- The inherited seed is real: `q_loc^nu=P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})` with `Gamma_eff=L_cg^-2 F(m)` and the product-rule gradient.",
                "- The first-row profile is still not claimable because `P_loc`, `Pi_gamma`, units, `m/L_cg` profiles, `K_hat/DeltaK`, and boundary/source support are missing.",
                "- A conditional Gauss/Green bridge is written: a compact scalar source can produce exterior `Q_loc/r`, but only after the operator normalization, sign, and boundary convention are fixed.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Scalar Source Profile Derivation",
                md_table(profile, ["profile_id", "quantity", "formula_or_requirement", "status", "missing_to_promote"]),
                "",
                "## Normalization First Row Schema",
                md_table(norm, ["row_id", "field", "required_value", "current_value", "guard"]),
                "",
                "## Gauss / Green Contract",
                md_table(gauss, ["contract_id", "piece", "conditional_law", "status", "missing_to_promote"]),
                "",
                "## q_loc Profile Runner Row",
                md_table(runner, ["runner_id", "branch", "S_q_profile", "Q_loc", "q_loc_hat", "operator_readout", "result"]),
                "",
                "## Retained Gap Ledger",
                md_table(gaps, ["gap_id", "missing_piece", "status", "why_it_matters"]),
                "",
                "## Rejection Ledger",
                md_table(rejections, ["rejection_id", "shortcut", "status", "reason"]),
                "",
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Local GR / Newton Status",
                md_table(local_rows, ["status_id", "claim", "current_status", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    profile = scalar_profile_rows()
    norm = normalization_rows()
    gauss = gauss_green_rows()
    runner = runner_rows()
    gaps = retained_gap_rows()
    rejections = rejection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(SCALAR_PROFILE_DERIVATION, profile)
    write_csv(NORMALIZATION_FIRST_ROW, norm)
    write_csv(GAUSS_GREEN_CONTRACT, gauss)
    write_csv(RUNNER_ROW, runner)
    write_csv(RETAINED_GAPS, gaps)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        SCALAR_PROFILE_DERIVATION,
        NORMALIZATION_FIRST_ROW,
        GAUSS_GREEN_CONTRACT,
        RUNNER_ROW,
        RETAINED_GAPS,
        REJECTION_LEDGER,
        CLAIM_GATE,
        DECISION,
        LOCAL_STATUS,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, profile, norm, gauss, runner, gaps, rejections, gates, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()
