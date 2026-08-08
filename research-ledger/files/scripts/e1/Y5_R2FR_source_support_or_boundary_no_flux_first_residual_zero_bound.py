from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1752"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1752 - Source Support Or Boundary No-Flux First Residual Zero Bound"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1752_0_1751_doc",
        "source_key": "1751_handoff",
        "source_path": ROOT / "1751-Y5-R2FR-parent-elliptic-functional-ownership-or-finite-residual-vector.md",
        "needles": ["RV1751_0_source_leak", "RV1751_3_boundary_flux"],
    },
    {
        "source_id": "SRC1752_1_1751_residual_vector",
        "source_key": "1751_finite_residual_vector",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1751_FINITE_RESIDUAL_VECTOR.csv",
        "needles": ["RV1751_0_source_leak", "MISSING_BOUNDARY_NOFLUX_OR_AMBIENT_MATCH"],
    },
    {
        "source_id": "SRC1752_2_71_source_boundary_law",
        "source_key": "71_source_support_boundary_law",
        "source_path": FORMALIZATION / "71-source-support-boundary-law.md",
        "needles": ["S_cg,local = U_B^pS S_*", "M_src ="],
    },
    {
        "source_id": "SRC1752_3_72_source_boundary_results",
        "source_key": "72_source_support_results",
        "source_path": FORMALIZATION / "72-source-support-boundary-first-results.md",
        "needles": ["complete_source_support_boundary_law_conditional_open", "open_source_support_not_derived"],
    },
    {
        "source_id": "SRC1752_4_77_sigma_silence",
        "source_key": "77_sigma_L_source_silence",
        "source_path": FORMALIZATION / "77-sigma-L-source-silence-theorem.md",
        "needles": ["sigma_L_source_silence_theorem_conditional_not_parent_derived", "S_cg = O(U_B)"],
    },
    {
        "source_id": "SRC1752_5_78_sigma_results",
        "source_key": "78_sigma_L_source_silence_results",
        "source_path": FORMALIZATION / "78-sigma-L-source-silence-first-results.md",
        "needles": ["complete_sigma_L_source_silence_conditional_not_parent_derived", "1.4413864308717837e-13"],
    },
    {
        "source_id": "SRC1752_6_143_boundary_gate",
        "source_key": "143_boundary_topological_backup",
        "source_path": FORMALIZATION / "143-boundary-topological-backup-gate.md",
        "needles": ["boundary_topological_backup_fails_transition_branch_demoted_closure_only", "4.212667126774669e-17"],
    },
    {
        "source_id": "SRC1752_7_boundary_scalar_owner",
        "source_key": "boundary_scalar_action_owner_attempt",
        "source_path": RESIDUALS / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv",
        "needles": ["O1_homogeneous_scalar_action", "O7_parent_owner_verdict"],
    },
    {
        "source_id": "SRC1752_8_boundary_alpha3_noflux",
        "source_key": "boundary_alpha3_noflux_theorem_attempt",
        "source_path": RESIDUALS / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv",
        "needles": ["T1_scalar_boundary_action", "T7_conclusion"],
    },
    {
        "source_id": "SRC1752_9_1041_noflux_route",
        "source_key": "1041_noflux_theorem_zero_route",
        "source_path": RESIDUALS / "P8_Y5_R10_1041_NOFLUX_THEOREM_ZERO_ROUTE.csv",
        "needles": ["NFR1041_0_positive_energy", "PROMISING_NOT_PARENT_SIGNED"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1752_SOURCE_REGISTER.csv",
    "source_support_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1752_SOURCE_SUPPORT_ZERO_BOUND_AUDIT.csv",
    "boundary_noflux_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1752_BOUNDARY_NOFLUX_ZERO_BOUND_AUDIT.csv",
    "first_residual_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1752_FIRST_RESIDUAL_ROWS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1752_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1752_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1752_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1752_VALIDATION.csv",
}


COPY_MAP = {
    "source_support_audit": "R2FR_1752_SOURCE_SUPPORT_ZERO_BOUND_AUDIT.csv",
    "boundary_noflux_audit": "R2FR_1752_BOUNDARY_NOFLUX_ZERO_BOUND_AUDIT.csv",
    "first_residual_rows": "R2FR_1752_FIRST_RESIDUAL_ROWS.csv",
    "decision": "R2FR_1752_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1752_CLAIM_GATE.csv",
    "next_target": "R2FR_1752_NEXT_TARGET.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        needles_present = all(needle in text for needle in needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles": "; ".join(needles),
                "needles_present": yesno(needles_present),
                "used_for": "1752 first residual source-support/no-flux audit",
                "timestamp_utc": UTC,
            }
        )
    return rows


def source_support_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SSA1752_0_residual_definition",
            "clause": "first residual source leak",
            "derived_or_checked_statement": "R_source = (1-Pi_B) S_cg = U_B S_cg",
            "status": "INHERITED_FROM_1751",
            "blocker": "none for definition; blocker is source-support ownership",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SSA1752_1_support_power_law",
            "clause": "source support power",
            "derived_or_checked_statement": "If S_cg,local = U_B^pS S_* then R_source = U_B^(1+pS) S_*",
            "status": "EXACT_CONDITIONAL_ALGEBRA",
            "blocker": "current corpus records this as conditional/open, not parent-derived",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SSA1752_2_source_bound_law",
            "clause": "finite source bound",
            "derived_or_checked_statement": "If |S_*| <= A_src then |R_source| <= U_B^(1+pS) A_src",
            "status": "CONDITIONAL_BOUND_THEOREM",
            "blocker": "A_src and parent support law are not source-backed prediction inputs",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SSA1752_3_exact_zero_test",
            "clause": "exact source zero",
            "derived_or_checked_statement": "R_source=0 requires U_B=0, S_*=0, or an exact parent projector identity killing S_cg",
            "status": "EXACT_ZERO_NOT_PROVED",
            "blocker": "finite-margin route gives small U_B, not exact U_B=0; no parent source-kernel theorem is signed",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SSA1752_4_strong_margin_smoke",
            "clause": "strong finite margin check",
            "derived_or_checked_statement": "For U_B=3.7965595357794454e-7 and pS=1, U_B^(1+pS)=1.4413864308717837e-13",
            "status": "SOURCE_BACKED_NUMERIC_SMOKE_NONCLAIM",
            "blocker": "multiplies unknown A_src and still depends on conditional support power",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SSA1752_5_weak_margin_edge",
            "clause": "weak finite margin check",
            "derived_or_checked_statement": "For U_B=1e-4 and pS=1, U_B^(1+pS)=1e-8 before A_src",
            "status": "EDGE_OF_BUDGET_NONCLAIM",
            "blocker": "generic linear m_L/trace failures show that powers and amplitudes cannot be hand-waved",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SSA1752_6_verdict",
            "clause": "source support verdict",
            "derived_or_checked_statement": "1752 upgrades R_source from vague missing row to an exact conditional finite bound row, but does not close it claim-grade",
            "status": "BOUND_FORM_DERIVED_PARENT_OWNERSHIP_MISSING",
            "blocker": "MISSING_PARENT_SUPPORT_INVARIANT; MISSING_A_src; MISSING_ARENA_PROJECTION_NORMS",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def boundary_noflux_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BNA1752_0_energy_identity",
            "clause": "no-hair energy identity",
            "derived_or_checked_statement": "positive bulk norm plus zero source plus zero boundary flux forces the local screened field residual to vanish",
            "status": "EXACT_CONDITIONAL_FROM_1751",
            "blocker": "source and boundary zero premises are not parent-owned",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BNA1752_1_scalar_boundary_zero",
            "clause": "scalar homogeneous boundary action",
            "derived_or_checked_statement": "scalar-only homogeneous stationary boundary action has no tangential vector/preferred-frame alpha3 channel",
            "status": "CONDITIONAL_ZERO_LEMMA",
            "blocker": "boundary scalar action owner audit fails parent ownership",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BNA1752_2_ward_flux",
            "clause": "normal momentum/no-flux condition",
            "derived_or_checked_statement": "n_mu B_boundary^{mu i}=0 or exact cancellation would remove boundary force flux",
            "status": "CONDITIONAL_IDENTITY_ONLY",
            "blocker": "current corpus has Ward ownership/force channels but not absence of flux",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BNA1752_3_full_local_warning",
            "clause": "alpha3-zero is not full local-GR zero",
            "derived_or_checked_statement": "even if the alpha3 vector channel is killed, beta, xi, Gdot, shell, stress, and orbital rows can remain active",
            "status": "DO_NOT_OVERPROMOTE",
            "blocker": "alpha3-specific boundary lemma is narrower than full PPN/local-GR closure",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BNA1752_4_finite_boundary_requirement",
            "clause": "finite boundary response budget",
            "derived_or_checked_statement": "|boundary/local PPN response| <= 4.212667126774669e-17 is required if exact zero is not parent-proved",
            "status": "FINITE_BOUND_REQUIREMENT_RETAINED",
            "blocker": "no source-backed boundary response coefficient or projection norm row",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "BNA1752_5_verdict",
            "clause": "boundary no-flux verdict",
            "derived_or_checked_statement": "boundary no-flux remains a conditional theorem and closure-only fallback, not a parent-owned local residual zero",
            "status": "NOFLUX_ZERO_NOT_CLAIMED",
            "blocker": "MISSING_PARENT_BOUNDARY_ACTION; MISSING_FLUX_ZERO; MISSING_BOUNDARY_RESPONSE_COEFFICIENT",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def first_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RV1752_0_source_leak_bound",
            "parent_residual_id": "RV1751_0_source_leak",
            "quantity": "R_source",
            "formula_or_description": "R_source = U_B S_cg; if S_cg=U_B^pS S_* then |R_source| <= U_B^(1+pS) A_src",
            "current_status": "CONDITIONAL_BOUND_FORM_DERIVED_NOT_PARENT_OWNED",
            "arena_links": "PPN/R10/WEP/clock/orbital/local_GR",
            "source_path": str(FORMALIZATION / "71-source-support-boundary-law.md"),
            "missing_to_promote": "MISSING_PARENT_SUPPORT_INVARIANT; MISSING_A_src; MISSING_ARENA_PROJECTION_NORMS",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RV1752_1_source_exact_zero",
            "parent_residual_id": "RV1751_0_source_leak",
            "quantity": "R_source_zero",
            "formula_or_description": "R_source=0 only if U_B=0 or S_cg is parent-kernel-zero",
            "current_status": "EXACT_ZERO_BLOCKED",
            "arena_links": "all_local_arenas",
            "source_path": str(FORMALIZATION / "77-sigma-L-source-silence-theorem.md"),
            "missing_to_promote": "MISSING_EXACT_PROJECTOR_ZERO_OR_SOURCE_KERNEL_THEOREM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RV1752_2_boundary_flux_zero",
            "parent_residual_id": "RV1751_3_boundary_flux",
            "quantity": "R_boundary",
            "formula_or_description": "R_boundary=0 if source-free positive operator and parent-owned no-flux boundary theorem hold",
            "current_status": "CONDITIONAL_ZERO_LEMMA_NOT_PARENT_OWNED",
            "arena_links": "PPN/local_GR/orbital",
            "source_path": str(RESIDUALS / "P8_Y5_R10_1041_NOFLUX_THEOREM_ZERO_ROUTE.csv"),
            "missing_to_promote": "MISSING_PARENT_BOUNDARY_ACTION; MISSING_FLUX_ZERO",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RV1752_3_boundary_finite_bound",
            "parent_residual_id": "RV1751_3_boundary_flux",
            "quantity": "R_boundary_bound",
            "formula_or_description": "if not exactly zero, require |boundary/local PPN response| <= 4.212667126774669e-17 or an arena-specific tighter map",
            "current_status": "FINITE_BOUND_INPUT_REQUIRED",
            "arena_links": "PPN/local_GR/orbital",
            "source_path": str(FORMALIZATION / "143-boundary-topological-backup-gate.md"),
            "missing_to_promote": "MISSING_BOUNDARY_RESPONSE_COEFFICIENT; MISSING_PROJECTION_NORM",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "RV1752_4_verdict",
            "parent_residual_id": "RV1751_10_verdict",
            "quantity": "first residual pair",
            "formula_or_description": "source-support bound and boundary no-flux theorem are now sharply separated: source is finite-bound promising; boundary is closure-only until parent signed",
            "current_status": "FIRST_RESIDUAL_PAIR_ACTIVE_NONCLAIM",
            "arena_links": "all_local_arenas",
            "source_path": str(ROOT / "1752-Y5-R2FR-source-support-or-boundary-no-flux-first-residual-zero-bound.md"),
            "missing_to_promote": "MISSING_PARENT_SUPPORT_INVARIANT_OR_PARENT_BOUNDARY_NOFLUX",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1752_0_source_result",
            "decision": "SOURCE_SUPPORT_BOUND_FORM_DERIVED",
            "reason": "R_source=U_B S_cg combines with S_cg=U_B^pS S_* to give an exact conditional U_B^(1+pS) suppression law",
            "next_action": "try to parent-derive the support invariant and source amplitude A_src",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1752_1_source_zero_result",
            "decision": "SOURCE_EXACT_ZERO_NOT_PROVED",
            "reason": "finite U_B margins are small but not exact zero, and no source-kernel theorem signs S_cg=0",
            "next_action": "keep source residual as finite bound row unless exact projector theorem appears",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1752_2_boundary_result",
            "decision": "BOUNDARY_NOFLUX_REMAINS_CLOSURE_ONLY",
            "reason": "scalar/no-flux lemmas exist, but current audits explicitly fail parent ownership and only kill narrow channels conditionally",
            "next_action": "do not use boundary no-flux to claim local GR; source a finite boundary coefficient if needed",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1752_3_best_next",
            "decision": "TARGET_SOURCE_SUPPORT_PARENT_INVARIANT_OR_A_SRC_ROW",
            "reason": "source route produced the cleanest derivable algebra; closing its parent invariant would shrink several local residuals without smuggling in a plateau",
            "next_action": "build 1753 source-support parent invariant or A_src coefficient row checkpoint",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1752_0_source_bound",
            "claim": "R_source finite bound can score",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_SUPPORT_INVARIANT_AND_A_SRC",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1752_1_source_zero",
            "claim": "R_source=0 exact local source silence",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_NO_EXACT_U_B_ZERO_OR_SOURCE_KERNEL_THEOREM",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1752_2_boundary_zero",
            "claim": "R_boundary=0 no-flux theorem is parent-owned",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_PARENT_BOUNDARY_ACTION_AND_FLUX_ZERO",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1752_3_boundary_bound",
            "claim": "finite boundary residual satisfies local PPN/orbital limits",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_BOUNDARY_RESPONSE_COEFFICIENT_AND_PROJECTION_NORM",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1752_4_local_reentry",
            "claim": "local GR/Newton/PPN/R10/WEP branch can claim",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_FIRST_RESIDUAL_PAIR_ACTIVE_NONCLAIM",
            "claim_allowed": no(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1752_0_primary",
            "next_target": "1753-Y5-R2FR-source-support-parent-invariant-or-A-src-coefficient-row.md",
            "script": "scripts/Y5_R2FR_source_support_parent_invariant_or_A_src_coefficient_row.py",
            "objective": "try to parent-derive S_cg=U_B^pS S_* and source amplitude A_src, or create explicit finite nonclaim source coefficient rows",
            "success_condition": "source residual becomes parent-signed exact-zero or source-backed finite-bound row without opening local claims",
            "selection_status": "selected",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1752_1_fallback",
            "next_target": "1753b-Y5-R2FR-boundary-response-coefficient-or-no-flux-parent-owner.md",
            "script": "scripts/Y5_R2FR_boundary_response_coefficient_or_noflux_parent_owner.py",
            "objective": "try to parent-own the scalar/no-flux boundary lemma or source a finite boundary response coefficient below local bounds",
            "success_condition": "boundary residual is zero by parent theorem or retained as a sourced finite nonclaim bound row",
            "selection_status": "held_fallback",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "source_support_audit": source_support_audit_rows(),
        "boundary_noflux_audit": boundary_noflux_audit_rows(),
        "first_residual_rows": first_residual_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1752_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1752_{key.upper()}.csv")


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if row.get(field) == "True":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values())
            if "MISSING_" in text:
                for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                    if row.get(field) == "True":
                        return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1752_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1752_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1752*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def source_bound_present(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["source_support_audit"]
    return any(
        row["audit_id"] == "SSA1752_2_source_bound_law"
        and row["status"] == "CONDITIONAL_BOUND_THEOREM"
        and "U_B^(1+pS)" in row["derived_or_checked_statement"]
        for row in rows
    )


def source_exact_zero_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["source_support_audit"]
    return any(row["audit_id"] == "SSA1752_3_exact_zero_test" and row["status"] == "EXACT_ZERO_NOT_PROVED" for row in rows)


def boundary_zero_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["boundary_noflux_audit"]
    return any(row["audit_id"] == "BNA1752_5_verdict" and row["status"] == "NOFLUX_ZERO_NOT_CLAIMED" for row in rows)


def finite_rows_active_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["first_residual_rows"]
    return any(row["residual_id"] == "RV1752_4_verdict" and row["current_status"] == "FIRST_RESIDUAL_PAIR_ACTIVE_NONCLAIM" for row in rows) and all(
        row["score_ready"] == "False" and row["claim_allowed"] == "False" for row in rows
    )


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    sources = rows_map["source_register"]
    claims = rows_map["claim_gate"]
    next_rows = rows_map["next_target"]
    source_rows = rows_map["source_support_audit"]
    boundary_rows = rows_map["boundary_noflux_audit"]

    validation = [
        check("VAL1752_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1752_1_needles_present", all(row["needles_present"] == "True" for row in sources), "required source needles are present", "one or more source needles missing"),
        check("VAL1752_2_source_bound_present", source_bound_present(rows_map), "source-support finite bound law is written", "source-support finite bound law missing"),
        check("VAL1752_3_source_exact_zero_blocked", source_exact_zero_blocked(rows_map), "exact source zero remains blocked", "exact source zero was accidentally promoted"),
        check("VAL1752_4_strong_margin_nonclaim", any(row["audit_id"] == "SSA1752_4_strong_margin_smoke" and row["valid_for_claim"] == "False" for row in source_rows), "strong margin smoke row remains nonclaim", "strong margin smoke row missing or promoted"),
        check("VAL1752_5_boundary_zero_blocked", boundary_zero_blocked(rows_map), "boundary no-flux exact zero remains blocked", "boundary no-flux was accidentally promoted"),
        check("VAL1752_6_boundary_bound_required", any(row["audit_id"] == "BNA1752_4_finite_boundary_requirement" and "4.212667126774669e-17" in row["derived_or_checked_statement"] for row in boundary_rows), "finite boundary response requirement retained", "finite boundary requirement missing"),
        check("VAL1752_7_first_residual_active", finite_rows_active_nonclaim(rows_map), "first residual pair remains active and nonclaim", "first residual rows missing or claim-enabled"),
        check("VAL1752_8_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claims), "all claim gates remain blocked", "one or more claim gates opened"),
        check("VAL1752_9_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check("VAL1752_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check("VAL1752_11_decision_next", any(row["decision_id"] == "DEC1752_3_best_next" and row["decision"] == "TARGET_SOURCE_SUPPORT_PARENT_INVARIANT_OR_A_SRC_ROW" for row in rows_map["decision"]), "decision selects source-support parent invariant/A_src target", "best-next decision missing"),
        check("VAL1752_12_next_selected", any(row["route_id"] == "NEXT1752_0_primary" and row["selection_status"] == "selected" for row in next_rows), "next target selected", "next target missing"),
        check("VAL1752_13_csv_parse", parsed_ok, "all generated 1752 CSVs parse", "one or more generated 1752 CSVs failed to parse"),
        check("VAL1752_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1752_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1752_16_formalization_untouched", formalization_untouched(), "no 1752 outputs found under formalization-workbench", "1752 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1752_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1752 source-support/no-flux first residual zero-bound checkpoint" if overall else "one or more 1752 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1752 gets a real derivation win, but not a claim win: the source residual now has an exact conditional bound form.",
        "- The algebra is clean: `R_source = U_B S_cg`, and if `S_cg = U_B^pS S_*`, then `|R_source| <= U_B^(1+pS) A_src`.",
        "- Strong finite-margin numbers are encouraging as smoke checks, but they still multiply unknown `A_src` and depend on a support law the parent theory has not signed.",
        "- Boundary no-flux remains a conditional closure theorem: useful, but not owned enough to erase `R_boundary` or claim local GR/Newton/PPN safety.",
        "- No local-GR, Newton, PPN, WEP, clock, orbital, R10, `q_loc=0`, or public claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Source Support Zero/Bound Audit",
        markdown_table(rows_map["source_support_audit"], ["audit_id", "clause", "derived_or_checked_statement", "status", "blocker"]),
        "",
        "## Boundary No-Flux Zero/Bound Audit",
        markdown_table(rows_map["boundary_noflux_audit"], ["audit_id", "clause", "derived_or_checked_statement", "status", "blocker"]),
        "",
        "## First Residual Rows",
        markdown_table(rows_map["first_residual_rows"], ["residual_id", "quantity", "formula_or_description", "current_status", "missing_to_promote"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "This checkpoint narrows the local problem in the good way. The source route is now the better attack than the boundary route: it has exact algebra and a plausible suppression hierarchy, while the boundary route still smells like a closure unless a parent boundary action appears. The next move is to hunt the parent reason why `S_cg` must carry `U_B` powers, or to admit a finite `A_src` coefficient row and test it honestly.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1752-Y5-R2FR-source-support-or-boundary-no-flux-first-residual-zero-bound.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1752_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1752 validation FAIL")
    print("1752 validation PASS")


if __name__ == "__main__":
    main()
