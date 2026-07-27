from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
MTS = WORK / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
DOC = WORK / "2819-Y5-R2FR-parent-qsector-action-norm-extraction-for-local-lock-reentry-under-AX1090.md"

SRC_2818_NEXT = MTS / "P8_Y5_R2FR_2818_NEXT_TARGET.csv"
SRC_2818_AMPLITUDE = MTS / "P8_Y5_R2FR_2818_LOCAL_LOCK_AMPLITUDE_LAW.csv"
SRC_2818_FIRST_PAIR = MTS / "P8_Y5_R2FR_2818_FIRST_NLOCK_INPUT_INTERFACE.csv"
SRC_2818_CHAIN = MTS / "P8_Y5_R2FR_2818_CHAIN_BOUND_UPDATE_WITH_NLOCK.csv"
SRC_2739_HUNT = MTS / "P8_Y5_R2FR_2739_PARENT_QNORM_SOURCE_HUNT.csv"
SRC_2739_DUAL = MTS / "P8_Y5_R2FR_2739_DUAL_PAIRING_STATUS.csv"
SRC_2739_DEMOTION = MTS / "P8_Y5_R2FR_2739_LOCAL_CLOSURE_DEMOTION_GATE.csv"
SRC_2740_SLOTS = MTS / "P8_Y5_R2FR_2740_PARENT_QSECTOR_ACTION_SLOTS.csv"
SRC_2740_ALGO = MTS / "P8_Y5_R2FR_2740_QNORM_EXTRACTION_ALGORITHM.csv"
SRC_2740_FILTERS = MTS / "P8_Y5_R2FR_2740_ACTION_FAILURE_FILTERS.csv"
SRC_2740_RUNNER = MTS / "P8_Y5_R2FR_2740_REENTRY_RUNNER_NONCLAIM.csv"
SRC_2740_NEXT = MTS / "P8_Y5_R2FR_2740_NEXT_TARGET.csv"
SRC_2741_ANSATZ = MTS / "P8_Y5_R2FR_2741_MINIMAL_QSECTOR_ANSATZ_AUDIT.csv"
SRC_2741_SMOKE = MTS / "P8_Y5_R2FR_2741_QNORM_EXTRACTION_SMOKE.csv"
SRC_2741_FILTER = MTS / "P8_Y5_R2FR_2741_ANSATZ_FILTER_RUNNER.csv"
SRC_2741_REJECT = MTS / "P8_Y5_R2FR_2741_REJECTION_LEDGER.csv"
SRC_2741_NEXT = MTS / "P8_Y5_R2FR_2741_NEXT_TARGET.csv"
SRC_1551_REENTRY = MTS / "P8_Y5_PARENT_QLOC_1551_QNORM_REENTRY_CONDITIONS.csv"
SRC_1552_TEMPLATE = MTS / "P8_Y5_PARENT_QLOC_1552_PARENT_QSECTOR_ACTION_TEMPLATE.csv"
SRC_1552_ALGO = MTS / "P8_Y5_PARENT_QLOC_1552_QNORM_EXTRACTION_ALGORITHM.csv"
SRC_1552_RUNNER = MTS / "P8_Y5_PARENT_QLOC_1552_REENTRY_RUNNER_NONCLAIM.csv"
SRC_1552_FILTERS = MTS / "P8_Y5_PARENT_QLOC_1552_ACTION_FAILURE_FILTERS.csv"
SRC_1553_SMOKE = MTS / "P8_Y5_PARENT_QLOC_1553_QNORM_EXTRACTION_SMOKE_NONCLAIM.csv"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2819_SOURCE_REGISTER.csv",
    "contract_import": MTS / "P8_Y5_R2FR_2819_QSECTOR_CONTRACT_IMPORT.csv",
    "extraction_status": MTS / "P8_Y5_R2FR_2819_EQ_JQ_DQVM_EXTRACTION_STATUS.csv",
    "ansatz_status": MTS / "P8_Y5_R2FR_2819_MINIMAL_QSECTOR_ANSATZ_REENTRY_AUDIT.csv",
    "local_lock_reentry": MTS / "P8_Y5_R2FR_2819_LOCAL_LOCK_REENTRY_IMPACT.csv",
    "gates": MTS / "P8_Y5_R2FR_2819_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2819_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2819_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2819_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2819_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "contract_queue": RAB_QUEUE / "JR2819_QSECTOR_CONTRACT_IMPORT_NONCLAIM.csv",
    "status_queue": RAB_QUEUE / "JR2819_EQ_JQ_DQVM_EXTRACTION_STATUS_NONCLAIM.csv",
    "ansatz_queue": RAB_QUEUE / "JR2819_MINIMAL_QSECTOR_ANSATZ_REENTRY_AUDIT_NONCLAIM.csv",
    "reentry_queue": RAB_QUEUE / "JR2819_LOCAL_LOCK_REENTRY_IMPACT_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2819_NEXT_PHASE_VOLUME_QSECTOR_ORIGIN.csv",
    "beta_doc": BETA_DOCS / "PARENT_QSECTOR_LOCAL_LOCK_REENTRY_2819_NONCLAIM.csv",
    "local_bound_copy": LOCAL_BOUNDS / "Parent_qsector_reentry_2819_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_parent_qsector_reentry_2819_nonclaim.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sp(path: Path) -> str:
    return str(path)


def ensure_dirs() -> None:
    directories = {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def anchor_found(path: Path, anchor: str) -> bool:
    return anchor in read_text(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def local_path_tokens(value: Any) -> list[Path]:
    if value is None:
        return []
    paths: list[Path] = []
    for token in str(value).split(";"):
        item = token.strip()
        if not item or item == "MISSING" or item.startswith("http"):
            continue
        candidate = Path(item)
        if not candidate.is_absolute():
            candidate = WORK / item
        if candidate.suffix or candidate.drive:
            paths.append(candidate)
    return paths


def build_sources() -> list[dict[str, Any]]:
    entries = [
        ("SRC2819_0_2818_next", SRC_2818_NEXT, "NEXT2818_0_2819", "2819 handoff"),
        ("SRC2819_1_2818_amplitude", SRC_2818_AMPLITUDE, "ALA2818_4_chain_insert", "local-lock amplitude bridge"),
        ("SRC2819_2_2818_first_pair", SRC_2818_FIRST_PAIR, "FPI2818_4_qnorm_blocker", "q-norm blocker in first-pair input"),
        ("SRC2819_3_2818_chain", SRC_2818_CHAIN, "CBU2818_3_qnorm_status", "local-lock reentry blocker"),
        ("SRC2819_4_2739_hunt", SRC_2739_HUNT, "HUNT2739_5_verdict", "no accepted q norm"),
        ("SRC2819_5_2739_dual", SRC_2739_DUAL, "DUAL2739_3_holder", "same-norm dual-pairing theorem"),
        ("SRC2819_6_2739_demotion", SRC_2739_DEMOTION, "DEM2739_4_reentry", "future reentry condition"),
        ("SRC2819_7_2740_slots", SRC_2740_SLOTS, "QS2740_8_verdict", "q-sector action slots"),
        ("SRC2819_8_2740_algorithm", SRC_2740_ALGO, "ALG2740_5_compute_Cqm", "q-norm extraction algorithm"),
        ("SRC2819_9_2740_filters", SRC_2740_FILTERS, "FAIL2740_1_mixed_norm", "failure filters"),
        ("SRC2819_10_2740_runner", SRC_2740_RUNNER, "RUN2740_6_reentry", "reentry runner refusal"),
        ("SRC2819_11_2740_next", SRC_2740_NEXT, "NEXT2740_0_2741", "minimal ansatz target"),
        ("SRC2819_12_2741_ansatz", SRC_2741_ANSATZ, "ANS2741_6_current_verdict", "minimal ansatz verdict"),
        ("SRC2819_13_2741_smoke", SRC_2741_SMOKE, "SMOKE2741_5_phase_volume_E", "phase-volume route"),
        ("SRC2819_14_2741_filter", SRC_2741_FILTER, "FR2741_6_verdict", "ansatz filter verdict"),
        ("SRC2819_15_2741_reject", SRC_2741_REJECT, "REJ2741_2_best_origin", "best origin route"),
        ("SRC2819_16_2741_next", SRC_2741_NEXT, "NEXT2741_0_2742", "phase-volume next target"),
        ("SRC2819_17_1551_reentry", SRC_1551_REENTRY, "RE1551_8_claim_policy", "original reentry conditions"),
        ("SRC2819_18_1552_template", SRC_1552_TEMPLATE, "ACT1552_6_parent_action_verdict", "original action template"),
        ("SRC2819_19_1552_algo", SRC_1552_ALGO, "ALG1552_4_compute_Cqm", "original algorithm"),
        ("SRC2819_20_1552_runner", SRC_1552_RUNNER, "RUN1552_6_reentry_status", "original runner refusal"),
        ("SRC2819_21_1552_filters", SRC_1552_FILTERS, "FAIL1552_1_mixed_norm", "original filters"),
        ("SRC2819_22_1553_smoke", SRC_1553_SMOKE, "SMOKE1553_0_auxiliary_E", "original qnorm smoke"),
    ]
    return [
        {
            "source_id": source_id,
            "path_or_url": sp(path),
            "anchor": anchor,
            "role": role,
            "path_exists": path.exists(),
            "anchor_found": anchor_found(path, anchor),
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for source_id, path, anchor, role in entries
    ]


def build_contract_import_rows() -> list[dict[str, Any]]:
    rows = [
        ("QCI2819_0_q_field", "q^A or q^A(Phi)", "required parent q field / q_loc map", "REQUIRED_NOT_SUPPLIED", SRC_2740_SLOTS, "QS2740_0_q_field"),
        ("QCI2819_1_positive_form", "E_q from G_AB/Hessian/regulator", "required positive same-norm quadratic form", "REQUIRED_NOT_SUPPLIED", SRC_2740_SLOTS, "QS2740_1_positive_quadratic_form"),
        ("QCI2819_2_Jq", "J_q=delta S_matter/delta q", "required parent source current", "REQUIRED_NOT_SUPPLIED", SRC_2740_SLOTS, "QS2740_4_matter_coupling"),
        ("QCI2819_3_Cqm", "C_qm=||Dq[v_m]||_E", "required same-norm response coefficient", "REQUIRED_NOT_SUPPLIED", SRC_2740_SLOTS, "QS2740_5_Cqm"),
        ("QCI2819_4_boundary", "boundary/domain terms", "must be zero-proved or included in finite rows", "REQUIRED_NOT_SUPPLIED", SRC_2740_SLOTS, "QS2740_6_boundary"),
        ("QCI2819_5_verdict", "accepted q-sector action", "no q-sector action data is supplied in current branch", "NOT_SUPPLIED_CURRENTLY", SRC_2740_SLOTS, "QS2740_8_verdict"),
    ]
    return [
        {
            "import_id": import_id,
            "object": obj,
            "role": role,
            "current_status": status,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": anchor_found(source_path, anchor),
            "reentry_required": True,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for import_id, obj, role, status, source_path, anchor in rows
    ]


def build_extraction_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("EXT2819_0_Eq", "E_q", "positive parent q norm", "REFUSED_MISSING_PARENT_NORM", "no G_AB/Hessian/regulator supplied", SRC_2740_RUNNER, "RUN2740_2_Eq"),
        ("EXT2819_1_Jq", "J_q", "source current in same variation space", "REFUSED_MISSING_PARENT_SOURCE", "no explicit S_matter[q] or coupling projector", SRC_2740_RUNNER, "RUN2740_3_Jq"),
        ("EXT2819_2_Dqvm", "Dq[v_m]", "vertical/local memory generator response in E_q", "REFUSED_MISSING_DQVM_NORM", "C_qm is not norm-evaluated", SRC_2740_RUNNER, "RUN2740_4_Cqm"),
        ("EXT2819_3_holder", "T_source_norm*C_qm", "same-norm Holder product", "DERIVED_CONDITIONAL_ONLY", "legal only after E_q,J_q,Dq[v_m] exist in one norm", SRC_2739_DUAL, "DUAL2739_3_holder"),
        ("EXT2819_4_no_mixed_norm", "mixed norm guard", "reject source/Cqm norm switching", "PASS_GUARD_NONCLAIM", "guard remains active and blocks norm-cheating", SRC_2740_FILTERS, "FAIL2740_1_mixed_norm"),
        ("EXT2819_5_reentry", "2818 local-lock reentry", "N_pair/Nlock may reopen only after Eq/Jq/Dqvm are supplied", "REENTRY_REFUSED_NOT_READY", "template and ansatz smoke do not supply parent data", SRC_2740_RUNNER, "RUN2740_6_reentry"),
    ]
    return [
        {
            "status_id": status_id,
            "quantity": quantity,
            "definition": definition,
            "current_status": status,
            "reason": reason,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": anchor_found(source_path, anchor),
            "source_backed": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for status_id, quantity, definition, status, reason, source_path, anchor in rows
    ]


def build_ansatz_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("ASR2819_0_auxiliary", "nonpropagating auxiliary q-sector", "S_q=1/2 int mu_q^2(q-Q)^A G_AB(q-Q)^B dV_e", "BEST_FORMAL_CANDIDATE_NOT_ACCEPTED", "least hair-prone if parent-sourced; Q,G,mu,Jq missing", SRC_2741_ANSATZ, "ANS2741_0_auxiliary_algebraic_positive_norm"),
        ("ASR2819_1_constraint", "pure constraint q-sector", "S_q=int lambda(q-Q)", "REJECTED_AS_NORM_SOURCE", "no positive E_q for T_source_norm*C_qm", SRC_2741_ANSATZ, "ANS2741_2_pure_constraint_q"),
        ("ASR2819_2_kinetic", "massive kinetic q-sector", "Z_AB nabla q nabla q + M_AB^2 q^2", "REJECTED_FOR_LOCAL_GR_ROUTE", "finite-range/exterior hair risk without stronger no-hair theorem", SRC_2741_ANSATZ, "ANS2741_1_massive_kinetic_q"),
        ("ASR2819_3_quotient", "quotient-reduced parent norm", "pullback of reduced Hessian", "CONDITIONAL_FUTURE_ROUTE_ONLY", "q/v_X/action/matter/boundary certificate currently failed", SRC_2741_ANSATZ, "ANS2741_4_reduced_quotient_norm"),
        ("ASR2819_4_phase_volume", "phase-volume/nonpropagating origin", "q norm arises from local capacity/phase-volume balance", "BEST_NEXT_ORIGIN_ROUTE", "could justify auxiliary norm without hand penalty, but origin theorem missing", SRC_2741_ANSATZ, "ANS2741_5_phase_volume_nonpropagating_origin"),
        ("ASR2819_5_verdict", "accepted q-sector action", "none", "NO_ACCEPTED_PARENT_ACTION", "all candidates lack parent source, norm, coupling, or pass/fail filters", SRC_2741_ANSATZ, "ANS2741_6_current_verdict"),
    ]
    return [
        {
            "ansatz_id": ansatz_id,
            "candidate": candidate,
            "formula_or_origin": formula,
            "status": status,
            "reason": reason,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": anchor_found(source_path, anchor),
            "accepted_parent_action": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for ansatz_id, candidate, formula, status, reason, source_path, anchor in rows
    ]


def build_local_lock_reentry_rows() -> list[dict[str, Any]]:
    rows = [
        ("LLR2819_0_amplitude_law", "Delta_m <= C_emb N_lock", "already staged in 2818", "WAITING_ON_NLOCK_INPUTS", SRC_2818_AMPLITUDE, "ALA2818_2_Delta_m"),
        ("LLR2819_1_Npair", "N_pair <= U_B,max S_cg,total_norm + C_inner||Q_m^H|| + domain/zero-mode terms", "first N_lock input interface", "CLOSURE_ONLY_UNTIL_EQ", SRC_2818_FIRST_PAIR, "FPI2818_2_Npair"),
        ("LLR2819_2_qnorm_blocker", "E_q/J_q/Dq[v_m]", "needed to make T_source_norm, C_qm and S_cg,total source-backed", "MISSING_PARENT_QSECTOR", SRC_2818_FIRST_PAIR, "FPI2818_4_qnorm_blocker"),
        ("LLR2819_3_contract_effect", "2740 contract", "reentry requirements are explicit but not supplied", "CONTRACT_ONLY_NO_REENTRY", SRC_2740_RUNNER, "RUN2740_0_contract_written"),
        ("LLR2819_4_ansatz_effect", "2741 ansatz audit", "auxiliary norm is private guide only; phase-volume origin is the next theorem target", "NO_REENTRY_FROM_ANSATZ", SRC_2741_REJECT, "REJ2741_2_best_origin"),
        ("LLR2819_5_claim_ceiling", "local GR/Newton/PPN/R10", "no local or arena claim can reopen from closure-only q norm", "CLAIMS_BLOCKED", SRC_2739_DEMOTION, "DEM2739_3_GR_Newton"),
    ]
    return [
        {
            "reentry_id": reentry_id,
            "object": obj,
            "effect": effect,
            "status": status,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": anchor_found(source_path, anchor),
            "reentry_allowed": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for reentry_id, obj, effect, status, source_path, anchor in rows
    ]


def build_gate_rows(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    contract_imported = all(row["anchor_found"] for row in sections["contract_import"])
    extracted = all(row["source_backed"] for row in sections["extraction_status"])
    phase_next = any(row["ansatz_id"] == "ASR2819_4_phase_volume" and row["status"] == "BEST_NEXT_ORIGIN_ROUTE" for row in sections["ansatz_status"])
    rows = [
        ("CG2819_0_sources_anchored", "2819 source anchors are present", all(row["anchor_found"] for row in sections["sources"]), "all source anchors were found"),
        ("CG2819_1_contract_imported", "q-sector extraction contract is imported", contract_imported, "2740 slots and algorithm are present"),
        ("CG2819_2_Eq_Jq_Dqvm_extracted", "E_q, J_q and Dq[v_m] are parent-extracted", extracted, "all remain missing or conditional"),
        ("CG2819_3_ansatz_accepted", "minimal q-sector ansatz can be accepted", False, "2741 rejects promotion of every ansatz"),
        ("CG2819_4_next_route_selected", "phase-volume origin is selected next", phase_next, "least-cheaty route to auxiliary q norm"),
        ("CG2819_5_local_lock_reentry", "2818 N_pair/Nlock route can reenter scoring", False, "q-sector norm data is absent"),
        ("CG2819_6_local_claim", "local-GR/Newton/PPN/R10 claim can be made", False, "closure-only branch cannot support claims"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": passed,
            "reason": reason,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for gate_id, claim, passed, reason in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2819_0_import_contract", "Import 2740 as the active q-sector extraction contract.", "It names every action/norm/source/boundary slot required for local-lock reentry.", "use it as the gate before any N_pair/Nlock scoring"),
        ("DEC2819_1_no_reentry", "Do not reopen the 2818 local-lock route yet.", "E_q, J_q, and Dq[v_m] remain missing; 2741 supplies no accepted parent action.", "keep N_pair/Nlock closure-only"),
        ("DEC2819_2_retain_auxiliary", "Retain the auxiliary algebraic q norm as a private guide.", "It avoids exterior gradient hair but is not parent-derived.", "derive its phase-volume/capacity origin or reject it"),
        ("DEC2819_3_next", "Attack phase-volume/nonpropagating q-sector origin next.", "It is the least-cheaty way to get a positive local norm without hand-inserting a penalty coefficient.", "2820 should derive or reject the origin theorem"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "because": because,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for decision_id, decision, because, next_action in rows
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2819_0_2820",
            "next_target": "2820-Y5-R2FR-phase-volume-nonpropagating-qsector-origin-for-local-lock-reentry-under-AX1090.md",
            "script": "scripts/Y5_R2FR_phase_volume_nonpropagating_qsector_origin_for_local_lock_reentry_under_AX1090_2820.py",
            "objective": "derive or reject a phase-volume/nonpropagating origin for the auxiliary q-sector norm, supplying or blocking q field, G_AB, mu_q, J_q, Dq[v_m], boundary terms, and no-exterior-hair guards needed for 2818 local-lock reentry",
            "include": "capacity/phase-volume balance; nonpropagating constraint origin; positive algebraic norm; matter coupling; same-norm C_qm; boundary/domain terms; failure filters",
            "exclude": "hand-inserted penalty coefficient; exterior kinetic hair; arena-fit norm; local-GR/Newton/PPN/R10 claim; GitHub; formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["contract_import"], BRANCH_OUTPUTS["contract_queue"], "contract_queue"),
        (OUTPUTS["extraction_status"], BRANCH_OUTPUTS["status_queue"], "status_queue"),
        (OUTPUTS["ansatz_status"], BRANCH_OUTPUTS["ansatz_queue"], "ansatz_queue"),
        (OUTPUTS["local_lock_reentry"], BRANCH_OUTPUTS["reentry_queue"], "reentry_queue"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
        (OUTPUTS["local_lock_reentry"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["local_lock_reentry"], BRANCH_OUTPUTS["local_bound_copy"], "local_bound_copy"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2819_{label}",
                "source": sp(source),
                "destination": sp(destination),
                "exists": destination.exists(),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def claim_flags_true(sections: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in sections.items():
        if key == "validation":
            continue
        for row in rows:
            if str(row.get("valid_for_claim", "false")).lower() == "true":
                return True
            if str(row.get("claim_allowed", "false")).lower() == "true":
                return True
    return False


def cited_paths_exist(sections: dict[str, list[dict[str, Any]]]) -> bool:
    paths: list[Path] = []
    for rows in sections.values():
        for row in rows:
            for key in ("source_path", "source_paths", "source", "destination", "path_or_url"):
                paths.extend(local_path_tokens(row.get(key)))
    return all(path.exists() for path in paths)


def formalization_untouched_since_run() -> bool:
    if not FORMALIZATION.exists():
        return True
    threshold = RUN_STARTED_UTC.timestamp()
    return not any(path.is_file() and path.stat().st_mtime >= threshold for path in FORMALIZATION.rglob("*"))


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2819_0_sources_exist", all(row["path_exists"] for row in sections["sources"]), "all source-register local paths exist"),
        ("VAL2819_1_source_anchors", all(row["anchor_found"] for row in sections["sources"]), "all source-register anchors were found"),
        ("VAL2819_2_contract_import_anchored", all(row["anchor_found"] for row in sections["contract_import"]), "q-sector contract import rows anchored"),
        ("VAL2819_3_extraction_not_claimed", all(not row["source_backed"] for row in sections["extraction_status"]), "E_q/J_q/Dqvm extraction remains unclaimed"),
        ("VAL2819_4_no_ansatz_accepted", all(not row["accepted_parent_action"] for row in sections["ansatz_status"]), "no minimal ansatz accepted as parent action"),
        ("VAL2819_5_phase_route_selected", any(row["ansatz_id"] == "ASR2819_4_phase_volume" for row in sections["ansatz_status"]), "phase-volume origin route retained"),
        ("VAL2819_6_reentry_blocked", all(not row["reentry_allowed"] for row in sections["local_lock_reentry"]), "local-lock reentry remains blocked"),
        ("VAL2819_7_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2819_8_next_target_2820", any(row["next_id"] == "NEXT2819_0_2820" for row in sections["next"]), "next target is 2820"),
        ("VAL2819_9_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2819_10_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2819_11_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2819_12_cited_paths_exist", cited_paths_exist(sections), "all cited local file/copy paths in generated rows exist"),
        ("VAL2819_13_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2819_14_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2819_15_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2819_16_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2819_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2819 imports the parent q-sector extraction contract into the 2818 local-lock route, refuses reentry because E_q/J_q/Dq[v_m] are absent, and selects phase-volume/nonpropagating q-sector origin as the next derivation target.",
            "generated_utc": utc_now(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
        + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2819 - Y5 R2FR Parent Qsector Action Norm Extraction For Local Lock Reentry Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2819 imports the 2740 q-sector action/norm extraction contract back into the 2818 local-lock amplitude route. The contract is useful and explicit, but it does not supply parent data.",
        "",
        "`E_q`, `J_q`, and `Dq[v_m]` are still absent. Therefore `T_source_norm`, `C_qm`, `S_cg,total_norm`, `N_pair`, `N_lock`, and the 2818 `Delta_m` bound remain closure-only rather than source-backed.",
        "",
        "2741 gives the current ansatz status: no q-sector action is accepted. The auxiliary algebraic norm is the best private candidate, but it needs a phase-volume/nonpropagating origin before it can be more than an inserted penalty.",
        "",
        "## Qsector Contract Import",
        markdown_table(sections["contract_import"], ["import_id", "object", "current_status", "reentry_required"]),
        "",
        "## Eq Jq Dqvm Extraction Status",
        markdown_table(sections["extraction_status"], ["status_id", "quantity", "current_status", "reason"]),
        "",
        "## Minimal Qsector Ansatz Reentry Audit",
        markdown_table(sections["ansatz_status"], ["ansatz_id", "candidate", "status", "accepted_parent_action"]),
        "",
        "## Local Lock Reentry Impact",
        markdown_table(sections["local_lock_reentry"], ["reentry_id", "object", "status", "effect"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "claim", "gate_pass", "claim_allowed", "reason"]),
        "",
        "## Decision Ledger",
        markdown_table(sections["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Validation",
        markdown_table(sections["validation"], ["validation_id", "passed", "detail"]),
        "",
        "## Next Target",
        markdown_table(sections["next"], ["next_id", "next_target", "objective", "include", "exclude"]),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    if (SCRIPTS / "__pycache__").exists():
        shutil.rmtree(SCRIPTS / "__pycache__")

    sections: dict[str, list[dict[str, Any]]] = {
        "sources": build_sources(),
        "contract_import": build_contract_import_rows(),
        "extraction_status": build_extraction_status_rows(),
        "ansatz_status": build_ansatz_status_rows(),
        "local_lock_reentry": build_local_lock_reentry_rows(),
    }
    sections["gates"] = build_gate_rows(sections)
    sections["decision"] = build_decision_rows()
    sections["next"] = build_next_rows()

    for key, rows in sections.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)
    sections["branches"] = copy_branches()
    write_csv(OUTPUTS["branches"], sections["branches"])
    sections["validation"] = build_validation(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])
    DOC.write_text(build_doc(sections), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation overall: {sections['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()
