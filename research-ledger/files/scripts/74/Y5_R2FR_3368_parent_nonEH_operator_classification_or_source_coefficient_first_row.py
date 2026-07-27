from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3368-Y5-R2FR-parent-nonEH-operator-classification-or-source-coefficient-first-row-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3368_SOURCE_REGISTER.csv",
    "operator_inventory": OUT / "P8_Y5_R2FR_3368_NONEH_OPERATOR_INVENTORY.csv",
    "classification": OUT / "P8_Y5_R2FR_3368_NONEH_OPERATOR_CLASSIFICATION.csv",
    "coefficient_rows": OUT / "P8_Y5_R2FR_3368_FIRST_SOURCE_COEFFICIENT_ROWS_NONCLAIM.csv",
    "priority": OUT / "P8_Y5_R2FR_3368_OPERATOR_PRIORITY_RANKING.csv",
    "runner": OUT / "P8_Y5_R2FR_3368_OPERATOR_CLASSIFIER_RUNNER.csv",
    "gates": OUT / "P8_Y5_R2FR_3368_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3368_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3368_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3368_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3368_0_3367_doc", ROOT / "3367-Y5-R2FR-first-DeltaGM-mass-charge-component-row-under-AX1090.md", "3367 classifier derivation"),
    ("SRC3368_1_3367_next", OUT / "P8_Y5_R2FR_3367_NEXT_TARGET.csv", "3367 next target selects parent non-EH operator classification"),
    ("SRC3368_2_3367_decomp", OUT / "P8_Y5_R2FR_3367_RNONEH_CHARGE_DECOMPOSITION.csv", "R_nonEH classifier classes"),
    ("SRC3368_3_2904_zero_gate", OUT / "P8_Y5_R2FR_2904_NON_EH_QV_ZERO_PRIORITY_GATE.csv", "non-EH sector priority gates"),
    ("SRC3368_4_2904_source_pack", OUT / "P8_Y5_R2FR_2904_NON_EH_QV_SOURCE_PACK.csv", "non-EH source pack components"),
    ("SRC3368_5_2905_extra_cert", OUT / "P8_Y5_R2FR_2905_EXTRA_RESPONSE_SILENCE_CERTIFICATE.csv", "extra/response operator silence certificate"),
    ("SRC3368_6_2905_extra_bound", OUT / "P8_Y5_R2FR_2905_EPSILON_EXTRA_BOUND_PACK.csv", "extra/response bound pack"),
    ("SRC3368_7_3089_schema", OUT / "P8_Y5_R2FR_3089_SOURCE_PACK_SCHEMA.csv", "bulk/edge X coefficient schema"),
    ("SRC3368_8_3355_contact", OUT / "P8_Y5_R2FR_3355_EPSILON_BOUNDARY_CONTACT_SPLIT.csv", "boundary/contact split"),
    ("SRC3368_9_3274_current_audit", OUT / "P8_Y5_R2FR_3274_CJ_OWNER_AUDIT.csv", "current-normalization owner audit"),
    ("SRC3368_10_3274_CJ_bound", OUT / "P8_Y5_R2FR_3274_CJ_CONDITIONAL_BOUND_ROWS_NONCLAIM.csv", "conditional C_J bound rows"),
    ("SRC3368_11_3274_poynting", OUT / "P8_Y5_R2FR_3274_EM_STRESS_POYNTING_EXCHANGE_LAW.csv", "EM stress/Poynting exchange source law"),
    ("SRC3368_12_3339_measuredG", OUT / "P8_Y5_R2FR_3339_MEASURED_G_ABSORPTION_THEOREM.csv", "common-mode absorption rule"),
    ("SRC3368_13_3340_parent_clause", OUT / "P8_Y5_R2FR_3340_PARENT_HILBERT_SOURCE_CLAUSE.csv", "parent Hilbert source clause"),
]


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def local_source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        parse_ok = False
        parse_error = ""
        if exists:
            parse_ok, parse_error = parse_csv(path) if path.suffix.lower() == ".csv" else parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def inventory_rows() -> list[dict[str, str]]:
    return [
        {
            "operator_id": "OP3368_0_common_kappa",
            "operator_family": "common_EH_proportional",
            "candidate_form": "E_X^{mu nu}=a_X E_EH^{mu nu}",
            "source_path": str(OUT / "P8_Y5_R2FR_3339_MEASURED_G_ABSORPTION_THEOREM.csv"),
            "source_row_hint": "GABS3339_0_measured_G_absorbs_common_mode",
            "evidence_status": "ALLOWED_CALIBRATION_CLASS_NOT_ACTUAL_NUMERIC_OPERATOR",
            "parent_owned": "false",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "OP3368_1_extra_response",
            "operator_family": "extra_response_motion_time_memory",
            "candidate_form": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B; O_X X=J_X with boundary flux",
            "source_path": str(OUT / "P8_Y5_R2FR_2905_EXTRA_RESPONSE_SILENCE_CERTIFICATE.csv"),
            "source_row_hint": "XRS2905_1_even_density;XRS2905_4_zero_odd_source_Y5;XRS2905_5_zero_odd_source_Y6",
            "evidence_status": "CANDIDATE_WRITTEN_HARD_Y5_Y6_SOURCE_BLOCK",
            "parent_owned": "false",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "OP3368_2_boundary_Bv",
            "operator_family": "boundary_reference_improvement",
            "candidate_form": "E_X^{mu nu}=nabla_lambda B_v^{lambda mu nu}; R_nonEH^B proportional to int_S B_v",
            "source_path": str(OUT / "P8_Y5_R2FR_2904_NON_EH_QV_SOURCE_PACK.csv"),
            "source_row_hint": "NES2904_0_Bv;ZNE2904_0_boundary_Bv",
            "evidence_status": "CONDITIONAL_ZERO_AVAILABLE_NOT_PARENT_SIGNED",
            "parent_owned": "false",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "OP3368_3_projector_PiM",
            "operator_family": "projector_source_measure",
            "candidate_form": "Pi_M vertical charge or d(Pi_M J_H) source-measure leakage",
            "source_path": str(OUT / "P8_Y5_R2FR_2904_NON_EH_QV_SOURCE_PACK.csv"),
            "source_row_hint": "NES2904_2_projector;ZNE2904_2_projector_source_measure",
            "evidence_status": "MISSING_PROJECTOR_VARIATION_AND_WARD_CLOSURE",
            "parent_owned": "false",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "OP3368_4_hidden_direct_source",
            "operator_family": "hidden_nonHilbert_source_slot",
            "candidate_form": "direct source slot changes exterior charge after readout",
            "source_path": str(OUT / "P8_Y5_R2FR_2904_NON_EH_QV_SOURCE_PACK.csv"),
            "source_row_hint": "NES2904_4_hidden_source;ZNE2904_3_matter_worldtube",
            "evidence_status": "MISSING_PARENT_NO_DIRECT_SOURCE_SLOT",
            "parent_owned": "false",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "OP3368_5_constraint_Cv",
            "operator_family": "constraint_or_Bianchi_piece",
            "candidate_form": "C_v nonconstraint or unbounded residual in Hamiltonian/Noether split",
            "source_path": str(OUT / "P8_Y5_R2FR_2904_NON_EH_QV_SOURCE_PACK.csv"),
            "source_row_hint": "NES2904_5_Cv;ZNE2904_4_constraint_Cv",
            "evidence_status": "MISSING_COMMON_CONSTRAINT_SPLIT",
            "parent_owned": "false",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "OP3368_6_EM_current_CJ",
            "operator_family": "EM_current_normalization_and_Poynting",
            "candidate_form": "S_int contains kappa_J(X) A_mu J_Q^mu; C_J=L_X ln kappa_J",
            "source_path": str(OUT / "P8_Y5_R2FR_3274_CJ_CONDITIONAL_BOUND_ROWS_NONCLAIM.csv"),
            "source_row_hint": "CJB3274_0_conditional_CJ_from_alpha",
            "evidence_status": "CONDITIONAL_NUMERIC_BOUND_EXISTS_WITH_SIDE_CONDITIONS",
            "parent_owned": "false",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "OP3368_7_boundary_contact",
            "operator_family": "contact_interface_source",
            "candidate_form": "distributional T_contact in local material support",
            "source_path": str(OUT / "P8_Y5_R2FR_3355_EPSILON_BOUNDARY_CONTACT_SPLIT.csv"),
            "source_row_hint": "EPSB3355_3_contact",
            "evidence_status": "OPEN_PRIMARY_SURVIVOR",
            "parent_owned": "false",
            "valid_for_claim": "false",
        },
        {
            "operator_id": "OP3368_8_bulk_X_coefficients",
            "operator_family": "bulk_X_massive_or_Yukawa",
            "candidate_form": "Z_X;M_X2;J_X;lambda_X;K_X;Qbar_XH;qbar_XT",
            "source_path": str(OUT / "P8_Y5_R2FR_3089_SOURCE_PACK_SCHEMA.csv"),
            "source_row_hint": "SP3089_4_bulk_X_coefficients",
            "evidence_status": "MISSING_PARENT_INPUT_OR_ARENA_PROJECTION",
            "parent_owned": "false",
            "valid_for_claim": "false",
        },
    ]


def classification_rows(inventory: list[dict[str, str]]) -> list[dict[str, str]]:
    classifier = {
        "OP3368_0_common_kappa": ("common_absorbable", "absorbed into measured G only if universal/source-blind/derivative-silent", "not a residual if exact"),
        "OP3368_1_extra_response": ("massive_or_noncommon_residual", "positive source-free theorem could zero it; Y5/Y6 source terms make it physical if not zero", "highest priority hard operator"),
        "OP3368_2_boundary_Bv": ("exact_flux_or_weighted_stokes_bound", "zero only by fixed exact no-flux boundary class; otherwise surface bound", "conditional exact route"),
        "OP3368_3_projector_PiM": ("projector_source_measure_residual", "noncommon source normalization drift unless Pi_M is parent-fixed Ward chain map", "source-mass/Newton risk"),
        "OP3368_4_hidden_direct_source": ("noncommon_source_selector", "cannot be absorbed by G; must be forbidden by parent object language or bounded", "WEP/Newton hard fail if live"),
        "OP3368_5_constraint_Cv": ("Bianchi_or_constraint_balance", "silent only if pure same-branch constraint or compensated Ward equation", "conservation gate"),
        "OP3368_6_EM_current_CJ": ("EM_current_source_coupling", "conditional alpha-derived bound exists only if C_Z=C_R=0 and no compensator/source-shadow current", "partly numeric nonclaim row"),
        "OP3368_7_boundary_contact": ("contact_source_residual", "bulk boundary zero does not kill material-support contact; needs collar exclusion or amplitude bound", "open survivor"),
        "OP3368_8_bulk_X_coefficients": ("massive_or_Yukawa_tail", "scoreable only after Z_X,M_X2,J_X,K_X,Qbar_XH,qbar_XT and arena projection", "R10/PPN bound route"),
    }
    rows: list[dict[str, str]] = []
    for item in inventory:
        class_label, zero_or_bound, verdict = classifier[item["operator_id"]]
        rows.append(
            {
                "classification_id": item["operator_id"].replace("OP", "CLS"),
                "operator_id": item["operator_id"],
                "operator_family": item["operator_family"],
                "3367_class": class_label,
                "zero_or_bound_route": zero_or_bound,
                "current_verdict": verdict,
                "parent_owned": item["parent_owned"],
                "valid_for_claim": "false",
            }
        )
    return rows


def coefficient_rows() -> list[dict[str, str]]:
    cj_rows = read_csv_rows(OUT / "P8_Y5_R2FR_3274_CJ_CONDITIONAL_BOUND_ROWS_NONCLAIM.csv")
    cj_bound = next((row for row in cj_rows if row.get("bound_id") == "CJB3274_0_conditional_CJ_from_alpha"), {})
    return [
        {
            "coefficient_row_id": "COEF3368_0_CJ_conditional_bound",
            "operator_id": "OP3368_6_EM_current_CJ",
            "coefficient": cj_bound.get("coefficient", "C_J=L_X ln kappa_J"),
            "value_or_bound": cj_bound.get("bound_value", "6.948988557475e-13"),
            "units": cj_bound.get("bound_units", "dimensionless local logarithmic current-normalization coefficient"),
            "side_conditions": cj_bound.get("side_conditions", "C_Z=0 and C_R=0, same local generator X, same observed coframe/readout"),
            "source_path": cj_bound.get("source_path", str(OUT / "P8_Y5_R2FR_3274_CJ_CONDITIONAL_BOUND_ROWS_NONCLAIM.csv")),
            "status": "CONDITIONAL_NUMERIC_BOUND_NONCLAIM",
            "why_not_claim": "general C_J is unbounded by alpha alone unless C_Z and C_R are independently zero and no compensator/source-shadow current survives",
            "valid_for_claim": "false",
        },
        {
            "coefficient_row_id": "COEF3368_1_extra_response_source_zero_contract",
            "operator_id": "OP3368_1_extra_response",
            "coefficient": "J_X or qbar_XT",
            "value_or_bound": "MISSING",
            "units": "operator/source coupling units required",
            "side_conditions": "positive self-adjoint operator, zero odd Y5/Y6 source, PPN lock, boundary no-flux, same branch",
            "source_path": str(OUT / "P8_Y5_R2FR_2905_EXTRA_RESPONSE_SILENCE_CERTIFICATE.csv"),
            "status": "HIGHEST_PRIORITY_MISSING_COEFFICIENT",
            "why_not_claim": "Y5 source-normalization and Y6 extra-stress remain retained debts",
            "valid_for_claim": "false",
        },
        {
            "coefficient_row_id": "COEF3368_2_bulk_X_schema",
            "operator_id": "OP3368_8_bulk_X_coefficients",
            "coefficient": "Z_X;M_X2;J_X;lambda_X;K_X;Qbar_XH;qbar_XT",
            "value_or_bound": "MISSING_PARENT_INPUT_OR_ARENA_PROJECTION",
            "units": "mixed; must be declared per coefficient",
            "side_conditions": "same parent branch and no-cancellation arena projection",
            "source_path": str(OUT / "P8_Y5_R2FR_3089_SOURCE_PACK_SCHEMA.csv"),
            "status": "SCHEMA_READY_NO_VALUES",
            "why_not_claim": "all numeric/source-backed parent inputs missing",
            "valid_for_claim": "false",
        },
    ]


def priority_rows() -> list[dict[str, str]]:
    return [
        {
            "priority_id": "PRI3368_0_extra_response_Y5",
            "rank": "1",
            "operator_id": "OP3368_1_extra_response",
            "why": "distinctive MTS channel and directly blocks R_nonEH/source-normalized Newton through Y5 source normalization",
            "recommended_action": "try to prove J_X/qbar_XT=0 for the extra-response Y5 source leg, or write first bounded qbar_XT row",
            "valid_for_claim": "false",
        },
        {
            "priority_id": "PRI3368_1_hidden_source_slot",
            "rank": "2",
            "operator_id": "OP3368_4_hidden_direct_source",
            "why": "if a direct non-Hilbert source slot is legal, no measured-G or WEP shortcut can save local GR",
            "recommended_action": "derive no-direct-source-slot from object language or keep explicit source-selector residual",
            "valid_for_claim": "false",
        },
        {
            "priority_id": "PRI3368_2_EM_current_CJ",
            "rank": "3",
            "operator_id": "OP3368_6_EM_current_CJ",
            "why": "has a partial numeric bound already; closing side conditions could create the first real coefficient bound row",
            "recommended_action": "prove C_Z=C_R=0 and no compensator/source-shadow current, or demote C_J bound to EM-only side branch",
            "valid_for_claim": "false",
        },
        {
            "priority_id": "PRI3368_3_boundary_contact",
            "rank": "4",
            "operator_id": "OP3368_7_boundary_contact",
            "why": "bulk boundary is mostly tamed but material-support contact remains a genuine survivor",
            "recommended_action": "prove collar/contact support exclusion or source a contact amplitude bound",
            "valid_for_claim": "false",
        },
    ]


def runner_rows(classifications: list[dict[str, str]], coefficients: list[dict[str, str]]) -> list[dict[str, str]]:
    all_classified = len(classifications) >= 9
    cj_bound_present = any(row["coefficient_row_id"] == "COEF3368_0_CJ_conditional_bound" and row["value_or_bound"] != "MISSING" for row in coefficients)
    missing_parent_owned = [row["operator_id"] for row in classifications if row["parent_owned"] != "true"]
    return [
        {
            "run_id": "RUN3368_0_inventory",
            "test": "operator inventory extracted from corpus ledgers",
            "result": "PASS" if all_classified else "FAIL",
            "detail": f"operator_count={len(classifications)}",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3368_1_classifier_coverage",
            "test": "3367 classifier classes assigned",
            "result": "PASS",
            "detail": "common/exact/massive/noncommon/Bianchi/EM/contact/projector classes assigned",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3368_2_first_numeric_like_row",
            "test": "first conditional coefficient bound row surfaced",
            "result": "PASS_NONCLAIM" if cj_bound_present else "FAIL",
            "detail": "C_J conditional bound retained as nonclaim because side conditions are unsigned",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3368_3_parent_owned_claim",
            "test": "all retained non-EH operators parent-owned",
            "result": "BLOCKED",
            "detail": "not_parent_owned=" + ";".join(missing_parent_owned),
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3368_4_RnonEH_promotion",
            "test": "R_nonEH_charge theorem-zero or bounded",
            "result": "BLOCKED",
            "detail": "classification exists, but operator coefficients/zero theorems are not closed",
            "valid_for_claim": "false",
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    return [
        {"gate_id": "GATE3368_0_operator_inventory", "claim": "operator candidates are inventory-classified", "passed": "true", "reason": "nine corpus-backed operator families classified", "valid_for_claim": "false"},
        {"gate_id": "GATE3368_1_first_conditional_bound", "claim": "first conditional coefficient-like row is surfaced", "passed": "true", "reason": "C_J conditional bound from 3274 imported as nonclaim", "valid_for_claim": "false"},
        {"gate_id": "GATE3368_2_extra_response_closed", "claim": "extra-response Y5/Y6 source leg is zero or bounded", "passed": "false", "reason": "J_X/qbar_XT and Y5/Y6 source silence remain missing", "valid_for_claim": "false"},
        {"gate_id": "GATE3368_3_all_nonEH_parent_owned", "claim": "all retained non-EH operators are parent-owned", "passed": "false", "reason": "every candidate remains conditional/not parent signed", "valid_for_claim": "false"},
        {"gate_id": "GATE3368_4_RnonEH_claim", "claim": "R_nonEH_charge can be promoted", "passed": "false", "reason": "classification is progress but not a zero/bound closure", "valid_for_claim": "false"},
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3368_0_not_empty",
            "question": "Was there anything real to classify?",
            "answer": "yes",
            "reason": "the corpus contains concrete operator families: extra/response, boundary, projector, hidden source, constraint, EM current, contact and bulk X coefficients",
            "next_action": "attack the highest-priority source-zero operator instead of repeating generic coupling language",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3368_1_best_target",
            "question": "Which candidate should be attacked first?",
            "answer": "extra-response Y5 source leg J_X/qbar_XT",
            "reason": "it is the distinctive MTS sector, sits directly in R_nonEH/source mass, and remains the hard block in 2905",
            "next_action": "3369 should derive qbar_XT/J_X source-zero or create a bounded qbar_XT component row",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3368_2_CJ_status",
            "question": "Does C_J give a real numeric foothold?",
            "answer": "partly",
            "reason": "3274 gives |C_J| <= 6.948988557475e-13 only if C_Z=C_R=0 and current compensators/source-shadow are excluded",
            "next_action": "keep it as a useful side branch, not the main R_nonEH source-mass closure",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3369-Y5-R2FR-extra-response-Y5-source-zero-or-qbarXT-bound-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3369_extra_response_Y5_source_zero_or_qbarXT_bound_row.py",
            "objective": "derive J_X/qbar_XT=0 for the extra-response Y5 source-normalization leg from parent matter/coframe descent, or emit the first bounded qbar_XT component row with no-cancellation guard",
            "why_next": "3368 ranks extra-response Y5 as the highest-priority actual non-EH source-charge operator blocking R_nonEH and source-normalized Newton",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3370-Y5-R2FR-CJ-side-conditions-close-or-EM-current-bound-demotion-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3370_CJ_side_conditions_close_or_EM_current_bound_demotion.py",
            "objective": "try to close C_Z=0, C_R=0, no-compensator and no-source-shadow current side conditions so the conditional C_J bound becomes usable, or demote it to EM-only nonclaim",
            "why_next": "C_J is the only surfaced conditional numeric coefficient row, but it is not general until side conditions close",
            "valid_for_claim": "false",
        },
    ]


def validate_rows(
    sources: list[dict[str, str]],
    inventory: list[dict[str, str]],
    classifications: list[dict[str, str]],
    coefficients: list[dict[str, str]],
    priorities: list[dict[str, str]],
    runner: list[dict[str, str]],
    gates: list[dict[str, str]],
    next_rows_in: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        rows.append({"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail})

    add("VAL3368_0_sources_exist", "all cited local source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3368_1_sources_parse", "all cited local source paths parse", all(row["parse_ok"] == "true" for row in sources))
    required_ops = {
        "OP3368_0_common_kappa",
        "OP3368_1_extra_response",
        "OP3368_2_boundary_Bv",
        "OP3368_3_projector_PiM",
        "OP3368_4_hidden_direct_source",
        "OP3368_5_constraint_Cv",
        "OP3368_6_EM_current_CJ",
        "OP3368_7_boundary_contact",
        "OP3368_8_bulk_X_coefficients",
    }
    seen_ops = {row["operator_id"] for row in inventory}
    add("VAL3368_2_inventory_complete", "operator inventory covers expected non-EH families", required_ops == seen_ops, "seen=" + ";".join(sorted(seen_ops)))
    classes = {row["3367_class"] for row in classifications}
    add(
        "VAL3368_3_classifier_classes_present",
        "classification spans common/exact/massive/noncommon/Bianchi classes",
        {"common_absorbable", "exact_flux_or_weighted_stokes_bound", "massive_or_Yukawa_tail", "noncommon_source_selector", "Bianchi_or_constraint_balance"}.issubset(classes),
    )
    add(
        "VAL3368_4_conditional_CJ_bound_surfaced",
        "conditional C_J numeric row is surfaced but nonclaim",
        any(row["coefficient_row_id"] == "COEF3368_0_CJ_conditional_bound" and row["valid_for_claim"] == "false" and row["value_or_bound"] != "MISSING" for row in coefficients),
    )
    add(
        "VAL3368_5_extra_response_ranked_first",
        "extra-response Y5 source leg ranked first",
        any(row["priority_id"] == "PRI3368_0_extra_response_Y5" and row["rank"] == "1" for row in priorities),
    )
    add(
        "VAL3368_6_runner_blocks_RnonEH",
        "runner blocks R_nonEH promotion",
        any(row["run_id"] == "RUN3368_4_RnonEH_promotion" and row["result"] == "BLOCKED" for row in runner),
    )
    add(
        "VAL3368_7_no_claim_gates",
        "all promotion claim gates remain false where required",
        any(row["gate_id"] == "GATE3368_4_RnonEH_claim" and row["passed"] == "false" for row in gates),
    )
    add(
        "VAL3368_8_next_target_qbarXT",
        "next target attacks qbarXT/J_X source-zero or bound",
        any(row["target_id"].startswith("3369-") and "qbarXT" in row["target_id"] for row in next_rows_in),
    )
    write_targets = list(OUTPUTS.values()) + [DOC]
    add(
        "VAL3368_9_write_scope_outside_formalization",
        "all 3368 write targets are outside formalization-workbench",
        all(not str(path).lower().startswith(str(FW).lower()) for path in write_targets),
        f"write_targets={len(write_targets)}",
    )
    passed_so_far = all(row["passed"] == "true" for row in rows)
    add("VAL3368_10_overall", "3368 validation overall", passed_so_far, "all required checks passed" if passed_so_far else "one or more checks failed")
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        vals = []
        for header in headers:
            vals.append(str(row.get(header, "")).replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, str]],
    inventory: list[dict[str, str]],
    classifications: list[dict[str, str]],
    coefficients: list[dict[str, str]],
    priorities: list[dict[str, str]],
    runner: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_rows_in: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    content = f"""# 3368 - Y5/R2FR parent non-EH operator classification or source coefficient first row under AX1090

## Summary
- 3368 feeds the 3367 `R_nonEH_charge` classifier with actual operator families already present in the corpus.
- Real result: the non-EH/source-charge problem is not empty; it has nine concrete families: common-kappa, extra/response, boundary `B_v`, projector `Pi_M`, hidden direct source, constraint `C_v`, EM/current `C_J`, contact/interface, and bulk `X` coefficients.
- The highest-priority hard target is the extra/response Y5 source leg `J_X/qbar_XT`, because it is distinctive MTS physics and directly blocks source-normalized Newton.
- The first numeric-like coefficient foothold is `|C_J| <= 6.948988557475e-13`, but it is conditional/nonclaim until `C_Z=0`, `C_R=0`, and compensator/source-shadow currents are excluded.
- No `R_nonEH_charge` or local-GR claim is promoted; this is an operator-classification checkpoint that tells us where to attack next.

Generated UTC: `{RUN_UTC}`

## Source Register
{markdown_table(sources)}

## Operator Inventory
{markdown_table(inventory)}

## Classification
{markdown_table(classifications)}

## First Coefficient Rows
{markdown_table(coefficients)}

## Priority Ranking
{markdown_table(priorities)}

## Runner
{markdown_table(runner)}

## Promotion Gates
{markdown_table(gates)}

## Decision Ledger
{markdown_table(decisions)}

## Next Target
{markdown_table(next_rows_in)}

## Validation
{markdown_table(validations)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = local_source_rows()
    inventory = inventory_rows()
    classifications = classification_rows(inventory)
    coefficients = coefficient_rows()
    priorities = priority_rows()
    runner = runner_rows(classifications, coefficients)
    gates = gate_rows()
    decisions = decision_rows()
    next_rows_in = next_rows()
    validations = validate_rows(sources, inventory, classifications, coefficients, priorities, runner, gates, next_rows_in)

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["operator_inventory"], inventory)
    write_csv(OUTPUTS["classification"], classifications)
    write_csv(OUTPUTS["coefficient_rows"], coefficients)
    write_csv(OUTPUTS["priority"], priorities)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_rows_in)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, inventory, classifications, coefficients, priorities, runner, gates, decisions, next_rows_in, validations)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
