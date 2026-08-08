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
DOC = ROOT / "1524-Y5-parent-Khat-DeltaK-scalar-channel-profile-or-Green-normalization.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1523_doc": ROOT / "1523-Y5-parent-P_loc-Pi_gamma-scalar-projector-and-units-ledger.md",
    "1523_next": OUT / "P8_Y5_PARENT_QLOC_1523_NEXT_TARGET.csv",
    "1523_units": OUT / "P8_Y5_PARENT_QLOC_1523_UNITS_LEDGER.csv",
    "1523_pigamma": OUT / "P8_Y5_PARENT_QLOC_1523_PIGAMMA_PROJECTOR_LEDGER.csv",
    "1523_validation": OUT / "P8_Y5_BRR545_1523_VALIDATION.csv",
    "1522_gauss": OUT / "P8_Y5_PARENT_QLOC_1522_GAUSS_GREEN_CONTRACT.csv",
    "1522_profile": OUT / "P8_Y5_PARENT_QLOC_1522_SCALAR_SOURCE_PROFILE_DERIVATION.csv",
    "1287_khat": OUT / "P8_Y5_R10_1287_FIRST_KHAT_COMPONENT_ROW_NONCLAIM.csv",
    "1287_kmetric_volume": OUT / "P8_Y5_R10_1287_FIRST_KMETRIC_VOLUME_ROW_NONCLAIM.csv",
    "1287_deltak_status": OUT / "P8_Y5_R10_1287_DELTAK_COMPONENT_STATUS_LEDGER.csv",
    "1289_delta": OUT / "P8_Y5_R10_1289_DELTAK00_COMPARISON_TEMPLATE.csv",
    "1289_kernel": OUT / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
    "1367_kernel": OUT / "P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv",
    "776_kgamma": OUT / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
    "798_gamma": OUT / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
    "1010_doc": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
    "1240_qr_map": OUT / "P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1524_SOURCE_REGISTER.csv"
KHAT_DELTAK_PROFILE = OUT / "P8_Y5_PARENT_QLOC_1524_KHAT_DELTAK_SCALAR_PROFILE.csv"
GREEN_NORMALIZATION = OUT / "P8_Y5_PARENT_QLOC_1524_GREEN_NORMALIZATION_CONTRACT.csv"
QLOC_HAT_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1524_QLOC_HAT_RUNNER_ROW.csv"
RETAINED_GAPS = OUT / "P8_Y5_PARENT_QLOC_1524_RETAINED_GAP_LEDGER.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1524_REJECTION_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1524_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1524_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_QLOC_1524_LOCAL_GR_NEWTON_STATUS.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1524_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1524_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1524"
QUAR_PROFILE = QUARANTINE / "KHAT_DELTAK_SCALAR_PROFILE_NONCLAIM.csv"
QUAR_GREEN = QUARANTINE / "GREEN_NORMALIZATION_CONTRACT_NONCLAIM.csv"
QUAR_RUNNER = QUARANTINE / "QLOC_HAT_RUNNER_ROW_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "QLOC_DECISION_NONCLAIM.csv"
BRANCH_PROFILE = BRANCH_RESIDUALS / "khat_deltak_scalar_profile_nonclaim_1524.csv"
BRANCH_GREEN = BRANCH_RESIDUALS / "green_normalization_contract_nonclaim_1524.csv"
BRANCH_RUNNER = BRANCH_RESIDUALS / "q_loc_hat_runner_row_nonclaim_1524.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "q_loc_decision_nonclaim_1524.csv"


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
                "source_id": f"SRC1524_{source_id}_{key}",
                "source_path": rel(path),
                "exists": path.exists(),
                "purpose": "input evidence for Khat/DeltaK scalar profile and Green normalization",
                **flags(),
            }
        )
    return rows


def khat_deltak_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KDS1524_0_Khat_candidate",
            "K_hat candidate",
            "K_L^{mu nu}=2 nabla^mu nabla^nu phi - (1/2)g^{mu nu}Box phi",
            "FORMAL_COMPONENT_EXISTS_NONCLAIM",
            "parent origin for phi/current MTS K_hat match is missing",
            source_list("1287_khat", "1287_deltak_status"),
        ),
        (
            "KDS1524_1_Kmetric_structure",
            "K_metric[Gamma_eff]",
            "Kmetric = Kmetric_volume + Kmetric_chain + K_conn + K_domain + K_boundary",
            "PARTIAL_STRUCTURE_NOT_COMPUTABLE",
            "C_sign, M_m, M_L, K_conn, K_domain, K_boundary, units, and boundary terms are missing",
            source_list("1287_kmetric_volume", "1289_delta", "1367_kernel"),
        ),
        (
            "KDS1524_2_DeltaK_definition",
            "Delta_K^{mu nu}",
            "Delta_K^{mu nu}:=K_hat^{mu nu}-K_metric^{mu nu}[Gamma_eff]",
            "DEFINITION_TEMPLATE_EXISTS",
            "current K_hat match and full K_metric are missing",
            source_list("1289_delta", "776_kgamma"),
        ),
        (
            "KDS1524_3_scalar_DeltaK_channel",
            "S_Delta",
            "S_Delta := -Pi_gamma[P_loc nabla_mu Delta_K^{mu nu}]",
            "SCALAR_CHANNEL_SCHEMA_WRITTEN",
            "Pi_gamma/P_loc not live, Delta_K components not computable, response coefficients missing",
            source_list("1523_pigamma", "1289_delta", "1367_kernel"),
        ),
        (
            "KDS1524_4_total_scalar_source",
            "S_total",
            "S_total := S_Gamma + S_Delta + S_boundary + S_source, with no cancellation assumption",
            "BUDGET_SCHEMA_WRITTEN",
            "each retained channel needs zero theorem or independent bound",
            source_list("1522_profile", "1010_doc", "1523_units"),
        ),
        (
            "KDS1524_5_verdict",
            "current scalar-channel K_hat/DeltaK profile",
            "source-backed S_Delta(r,x) or theorem-zero certificate",
            "MISSING_SCALAR_PROFILE",
            "K_hat/DeltaK remains retained and cannot be dropped from S_q",
            source_list("1287_deltak_status", "1367_kernel"),
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


def green_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "GRN1524_0_operator_equation",
            "static scalar operator",
            "nabla^2 R_AB = C_op S_total",
            "CONDITIONAL_OPERATOR_FORM",
            "L_PPN scalar reduction, sign, gauge, boundary, and C_op are not parent-signed",
        ),
        (
            "GRN1524_1_green_solution",
            "Green solution",
            "R_AB(x) = -C_op/(4*pi) int S_total(x')/|x-x'| d^3x' for R_AB(infinity)=0",
            "DERIVED_CONDITIONAL_GREEN_FORM",
            "depends on flat/static exterior scalar operator and sign convention",
        ),
        (
            "GRN1524_2_exterior_charge",
            "Q_loc",
            "for compact support, R_AB(r) = -Q_loc/r with Q_loc=(C_op/4*pi) int S_total d^3x",
            "DERIVED_CONDITIONAL_NORMALIZATION",
            "requires sourced S_total and C_op",
        ),
        (
            "GRN1524_3_dimensionless_amplitude",
            "q_loc_hat",
            "q_loc_hat = Q_loc c^2/(G M_source)",
            "CONDITIONAL_DIMENSIONLESS_MAP",
            "requires measured GM/source row and Q_loc",
        ),
        (
            "GRN1524_4_qR_bridge",
            "q_loc_hat equals q_R_hat",
            "only if Q_loc=Q_R with same sign, source, GM convention, and no retained channels outside S_total",
            "BRIDGE_CONDITION_ONLY",
            "q_R import remains forbidden without this proof",
        ),
        (
            "GRN1524_5_verdict",
            "current C_op/Q_loc/q_loc_hat",
            "finite Green-normalized q_loc amplitude",
            "NOT_SCORE_READY",
            "C_op and S_total integral are missing",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "green_id": green_id,
            "quantity": quantity,
            "formula_or_requirement": formula,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("1522_gauss", "1523_units", "1240_qr_map"),
            **flags(),
        }
        for green_id, quantity, formula, status, missing in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1524_0_green_blocked",
            "branch": "q_loc_hat_from_scalar_source",
            "S_Gamma": "MISSING_SOURCE_PROFILE",
            "S_Delta": "MISSING_KHAT_DELTAK_SCALAR_PROFILE",
            "S_boundary": "MISSING_BOUNDARY_PROFILE_OR_ZERO",
            "C_op": "MISSING_OPERATOR_CONSTANT",
            "Q_loc_formula": "Q_loc=(C_op/4*pi)*int(S_total)d^3x",
            "Q_loc_value": "MISSING",
            "q_loc_hat": "MISSING",
            "result": "BLOCKED_MISSING_STOTAL_OR_COP",
            "source_paths": source_list("1523_units", "1522_gauss", "1289_delta"),
            **flags(),
        }
    ]


def retained_gap_rows() -> list[dict[str, Any]]:
    rows = [
        ("GAP1524_0_current_Khat", "current MTS K_hat tensor", "MISSING_CURRENT_KHAT_MATCH", "formal K_L component is not live K_hat"),
        ("GAP1524_1_full_Kmetric", "full K_metric[Gamma_eff]", "MISSING_FULL_KMETRIC", "volume piece exists but chain/connection/domain/boundary kernels missing"),
        ("GAP1524_2_DeltaK_components", "Delta_K^{mu nu}", "NOT_COMPUTABLE", "cannot build S_Delta without Khat-Kmetric components"),
        ("GAP1524_3_Pi_gamma_live", "Pi_gamma/P_loc", "SCHEMA_ONLY", "scalar channel projector not parent/operator signed"),
        ("GAP1524_4_Cop", "Green/operator constant", "MISSING_OPERATOR_CONSTANT", "cannot turn S_total into Q_loc"),
        ("GAP1524_5_boundary_sign", "boundary/sign convention", "MISSING_BOUNDARY_SIGN", "exterior -Q/r sign not fixed for q_loc"),
        ("GAP1524_6_channel_bounds", "independent retained-channel bounds", "MISSING", "no cancellation between S_Gamma, S_Delta, boundary/source"),
        ("GAP1524_7_acceptance", "profile/normalization acceptance", "CLAIM_BLOCKED", "no scoring until all gaps are closed or bounded"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gap_id": gap_id,
            "missing_piece": piece,
            "status": status,
            "why_it_matters": why,
            "source_paths": source_list("1287_deltak_status", "1367_kernel", "1523_units"),
            **flags(),
        }
        for gap_id, piece, status, why in rows
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1524_0_drop_Khat", "score S_q using Gamma gradient only", "REJECTED", "q_loc definition contains div K_hat and DeltaK can source gamma"),
        ("REJ1524_1_formal_KL_live", "treat formal K_L row as current MTS K_hat", "REJECTED", "parent origin/current-symbol match is missing"),
        ("REJ1524_2_volume_only_Kmetric", "use only Kmetric volume term", "REJECTED", "chain, connection, domain, and boundary terms remain open"),
        ("REJ1524_3_Cop_one", "set C_op=1 by convention", "REJECTED", "operator normalization carries units and sign"),
        ("REJ1524_4_qR_import", "use q_R exterior formula before Q_loc is derived", "REJECTED", "requires Q_loc=Q_R bridge and channel silence"),
        ("REJ1524_5_cancellation", "allow S_Delta to cancel S_Gamma without proof", "REJECTED", "retained channels need independent zero/bounds"),
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
        ("GATE1524_0_DeltaK_schema", "S_Delta schema exists", "PASS_NONCLAIM", "scalar-channel DeltaK formula is written", False),
        ("GATE1524_1_live_DeltaK", "S_Delta is source-backed or theorem-zero", "BLOCKED", "current Khat/full Kmetric/components missing", False),
        ("GATE1524_2_Green_formula", "Green normalization formula exists", "PASS_CONDITIONAL", "Q_loc=(C_op/4pi) integral S_total is derived under static scalar assumptions", False),
        ("GATE1524_3_Cop_live", "C_op is source-backed", "BLOCKED", "operator normalization/sign/gauge missing", False),
        ("GATE1524_4_qloch_score", "q_loc_hat can be computed", "BLOCKED", "S_total, C_op, Q_loc, GM missing", False),
        ("GATE1524_5_local_GR", "local GR/PPN claim can be made", "BLOCKED_NO_CLAIM", "q_loc scalar channel remains nonclaim", False),
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
        ("DEC1524_0_DeltaK_retained", "Keep K_hat/DeltaK as explicit scalar-channel source, not an optional correction.", "SDELTA_SCHEMA_WRITTEN", "dropping K_hat would fake the q_loc source profile."),
        ("DEC1524_1_Green_gain", "Adopt the conditional Green normalization formula.", "QLOC_FORMULA_DERIVED_CONDITIONAL", "this is real progress: it identifies C_op and the S_total integral as the normalization bottleneck."),
        ("DEC1524_2_next", "Next target is Khat parent-origin or Kmetric derivative/domain/boundary kernels.", "NEXT_1525_KHAT_OR_KMETRIC", "without live Khat/full Kmetric, DeltaK cannot be zeroed or bounded."),
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
        ("LOCAL1524_0_Khat", "K_hat/DeltaK scalar channel", "SCHEMA_ONLY", "S_Delta defined but components missing"),
        ("LOCAL1524_1_Green", "Green normalization", "CONDITIONAL_FORMULA_ONLY", "Q_loc formula exists but C_op/S_total missing"),
        ("LOCAL1524_2_qloch", "q_loc_hat", "NOT_COMPUTABLE", "Q_loc and GM/source row missing"),
        ("LOCAL1524_3_PPN", "Cassini/PPN scoring", "NOT_CLAIMED", "no q_loc_hat or live C_qgamma"),
        ("LOCAL1524_4_GR", "derived local GR/Newton", "NOT_CLAIMED", "q_loc and M_H_ref bottlenecks remain"),
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
            "next_id": "NEXT1524_0_1525",
            "next_target": "1525-Y5-parent-Khat-origin-or-Kmetric-derivative-domain-boundary-kernels.md",
            "script": "scripts/Y5_parent_Khat_origin_or_Kmetric_derivative_domain_boundary_kernels.py",
            "objective": "try to parent-sign the K_hat candidate as current MTS K_hat, or compute/source the missing Kmetric derivative, domain, boundary, and sign kernels needed for DeltaK",
            "do_not": "do not drop K_hat, do not use volume-only Kmetric, do not score PPN/Cassini, and do not claim local GR",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (KHAT_DELTAK_PROFILE, QUAR_PROFILE),
        (GREEN_NORMALIZATION, QUAR_GREEN),
        (QLOC_HAT_RUNNER, QUAR_RUNNER),
        (DECISION, QUAR_DECISION),
        (KHAT_DELTAK_PROFILE, BRANCH_PROFILE),
        (GREEN_NORMALIZATION, BRANCH_GREEN),
        (QLOC_HAT_RUNNER, BRANCH_RUNNER),
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
    profile = read_csv(KHAT_DELTAK_PROFILE)
    green = read_csv(GREEN_NORMALIZATION)
    runner = read_csv(QLOC_HAT_RUNNER)
    gaps = read_csv(RETAINED_GAPS)
    rejections = read_csv(REJECTION_LEDGER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1524_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1524 input source paths exist"),
        ("VAL1524_1_SDelta_schema", any(row["profile_id"] == "KDS1524_3_scalar_DeltaK_channel" and row["status"] == "SCALAR_CHANNEL_SCHEMA_WRITTEN" for row in profile), "S_Delta scalar-channel schema is written"),
        ("VAL1524_2_DeltaK_not_promoted", any(row["profile_id"] == "KDS1524_5_verdict" and row["status"] == "MISSING_SCALAR_PROFILE" for row in profile), "Khat/DeltaK scalar profile remains missing"),
        ("VAL1524_3_Green_formula", any(row["green_id"] == "GRN1524_2_exterior_charge" and row["status"] == "DERIVED_CONDITIONAL_NORMALIZATION" for row in green), "Q_loc Green normalization formula is written"),
        ("VAL1524_4_Cop_missing", any(row["green_id"] == "GRN1524_5_verdict" and row["status"] == "NOT_SCORE_READY" for row in green), "C_op/S_total remain missing"),
        ("VAL1524_5_runner_blocked", any(row["runner_id"] == "RUN1524_0_green_blocked" and row["result"] == "BLOCKED_MISSING_STOTAL_OR_COP" for row in runner), "runner refuses missing S_total/C_op"),
        ("VAL1524_6_gaps_complete", len(gaps) >= 8 and any(row["gap_id"] == "GAP1524_7_acceptance" and row["status"] == "CLAIM_BLOCKED" for row in gaps), "gap ledger blocks promotion"),
        ("VAL1524_7_rejections_guardrails", len(rejections) >= 6 and all(row["status"] == "REJECTED" for row in rejections), "Khat/Cop/qR/cancellation shortcuts rejected"),
        ("VAL1524_8_claim_gates_block_claim", any(row["gate_id"] == "GATE1524_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1524_9_decision_next", any(row["result"] == "NEXT_1525_KHAT_OR_KMETRIC" for row in decisions), "decision selects Khat origin or Kmetric kernels next"),
        ("VAL1524_10_next_target", any("1525-Y5-parent-Khat-origin" in row["next_target"] for row in next_rows), "next target is Khat origin or Kmetric derivative/domain/boundary kernels"),
        ("VAL1524_11_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1524 CSVs parse cleanly"),
        ("VAL1524_12_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1524_13_branch_copies", all(path.exists() for path in [QUAR_PROFILE, QUAR_GREEN, QUAR_RUNNER, QUAR_DECISION, BRANCH_PROFILE, BRANCH_GREEN, BRANCH_RUNNER, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1524_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1524_15_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
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
            "check_id": "VAL1524_16_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1524 writes S_Delta and conditional Green normalization, keeps them nonclaim, and selects Khat origin or Kmetric kernels next"
            if overall
            else "1524 validation failed; inspect failed rows before continuing",
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
    green: list[dict[str, Any]],
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
                "# 1524 - Parent Khat/DeltaK Scalar-Channel Profile or Green Normalization",
                "",
                "## Verdict",
                "- The retained `K_hat/DeltaK` correction is now explicitly part of the scalar source budget: `S_Delta := -Pi_gamma[P_loc nabla_mu Delta_K^{mu nu}]`.",
                "- The total scalar source must be `S_total = S_Gamma + S_Delta + S_boundary + S_source`; cancellation between these pieces is not allowed unless proven.",
                "- The Green normalization is conditionally derived: if `nabla^2 R_AB = C_op S_total`, then `Q_loc=(C_op/4*pi) int S_total d^3x` and `R_AB=-Q_loc/r` outside compact support.",
                "- Nothing is scoreable yet because current `K_hat`, full `K_metric`, `DeltaK`, `C_op`, and the source integral are still missing.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Khat / DeltaK Scalar Profile",
                md_table(profile, ["profile_id", "quantity", "formula_or_requirement", "status", "missing_to_promote"]),
                "",
                "## Green Normalization Contract",
                md_table(green, ["green_id", "quantity", "formula_or_requirement", "status", "missing_to_promote"]),
                "",
                "## q_loc Hat Runner Row",
                md_table(runner, ["runner_id", "branch", "S_Gamma", "S_Delta", "C_op", "Q_loc_formula", "result"]),
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
    profile = khat_deltak_rows()
    green = green_rows()
    runner = runner_rows()
    gaps = retained_gap_rows()
    rejections = rejection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(KHAT_DELTAK_PROFILE, profile)
    write_csv(GREEN_NORMALIZATION, green)
    write_csv(QLOC_HAT_RUNNER, runner)
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
        KHAT_DELTAK_PROFILE,
        GREEN_NORMALIZATION,
        QLOC_HAT_RUNNER,
        RETAINED_GAPS,
        REJECTION_LEDGER,
        CLAIM_GATE,
        DECISION,
        LOCAL_STATUS,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, profile, green, runner, gaps, rejections, gates, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()
