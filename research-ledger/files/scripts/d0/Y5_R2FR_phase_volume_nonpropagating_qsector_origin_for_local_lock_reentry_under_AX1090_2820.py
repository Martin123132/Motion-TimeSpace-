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
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2820-Y5-R2FR-phase-volume-nonpropagating-qsector-origin-for-local-lock-reentry-under-AX1090.md"

SRC_2819_NEXT = RESIDUALS / "P8_Y5_R2FR_2819_NEXT_TARGET.csv"
SRC_2819_ANSATZ = RESIDUALS / "P8_Y5_R2FR_2819_MINIMAL_QSECTOR_ANSATZ_REENTRY_AUDIT.csv"
SRC_2819_EXTRACTION = RESIDUALS / "P8_Y5_R2FR_2819_EQ_JQ_DQVM_EXTRACTION_STATUS.csv"
SRC_2819_REENTRY = RESIDUALS / "P8_Y5_R2FR_2819_LOCAL_LOCK_REENTRY_IMPACT.csv"
SRC_2742_ORIGIN = RESIDUALS / "P8_Y5_R2FR_2742_PHASE_VOLUME_ORIGIN_AUDIT.csv"
SRC_2742_MAPPING = RESIDUALS / "P8_Y5_R2FR_2742_QSECTOR_MAPPING_NONCLAIM.csv"
SRC_2742_OBSTRUCTIONS = RESIDUALS / "P8_Y5_R2FR_2742_ORIGIN_OBSTRUCTION_LEDGER.csv"
SRC_2742_RUNNER = RESIDUALS / "P8_Y5_R2FR_2742_ORIGIN_RUNNER_NONCLAIM.csv"
SRC_2742_DECISION = RESIDUALS / "P8_Y5_R2FR_2742_DECISION_LEDGER.csv"
SRC_2743_GAUGE = RESIDUALS / "P8_Y5_R2FR_2743_GAUGE_NOETHER_ROUTE_AUDIT.csv"
SRC_2743_RUNNER = RESIDUALS / "P8_Y5_R2FR_2743_ZERO_CHARGE_RUNNER_NONCLAIM.csv"
SRC_2743_DECISION = RESIDUALS / "P8_Y5_R2FR_2743_DECISION_LEDGER.csv"
SRC_2744_DECISION = RESIDUALS / "P8_Y5_R2FR_2744_DECISION_LEDGER.csv"
SRC_2745_DECISION = RESIDUALS / "P8_Y5_R2FR_2745_DECISION_LEDGER.csv"
SRC_2262_NONPROP = RESIDUALS / "P8_Y5_PARENT_QLOC_2262_NONPROPAGATING_CONSTRAINT_AUDIT.csv"
SRC_2268_TESTS = RESIDUALS / "P8_Y5_PARENT_QLOC_2268_PHASE_VOLUME_PSI_ORIGIN_TESTS.csv"
SRC_1554_ORIGIN = RESIDUALS / "P8_Y5_PARENT_QLOC_1554_PHASE_VOLUME_ORIGIN_AUDIT.csv"
SRC_2227_ORIGIN = RESIDUALS / "P8_Y5_PARENT_QLOC_2227_PHASE_VOLUME_ORIGIN_AUDIT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2820_SOURCE_REGISTER.csv",
    "origin_reentry": RESIDUALS / "P8_Y5_R2FR_2820_PHASE_VOLUME_ORIGIN_REENTRY_AUDIT.csv",
    "mapping": RESIDUALS / "P8_Y5_R2FR_2820_QSECTOR_ORIGIN_MAPPING_STATUS.csv",
    "extraction": RESIDUALS / "P8_Y5_R2FR_2820_EQ_MU_GAB_EXTRACTION_STATUS.csv",
    "reentry_gate": RESIDUALS / "P8_Y5_R2FR_2820_LOCAL_LOCK_REENTRY_GATE.csv",
    "filters": RESIDUALS / "P8_Y5_R2FR_2820_PHASE_VOLUME_FAILURE_FILTERS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2820_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2820_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2820_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2820_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2820_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "origin_weight": SOURCE_WEIGHT / "phase_volume_qsector_local_lock_reentry_2820_NONCLAIM.csv",
    "local_gate": LOCAL_BOUNDS / "local_lock_qsector_reentry_gate_2820_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2820_PARENT_COUPLING_SOURCE_CURRENT_NEXT.csv",
}

BRANCH_ID = "MTS_R2FR_LOCAL_LOCK_QSECTOR_REENTRY_2820"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    anchor_list = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in anchor_list if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2820_0_2819_next", SRC_2819_NEXT, "NEXT2819_0_2820", "handoff selecting phase-volume q-sector origin for local-lock reentry"),
        ("SRC2820_1_2819_ansatz", SRC_2819_ANSATZ, "ASR2819_4_phase_volume;ASR2819_5_verdict", "2819 ansatz status and phase-volume route"),
        ("SRC2820_2_2819_extraction", SRC_2819_EXTRACTION, "EXT2819_0_Eq;EXT2819_1_Jq;EXT2819_2_Dqvm", "missing Eq/Jq/Dqvm blockers"),
        ("SRC2820_3_2819_reentry", SRC_2819_REENTRY, "LLR2819_2_qnorm_blocker;LLR2819_5_claim_ceiling", "2818 local-lock reentry blocker"),
        ("SRC2820_4_2742_origin", SRC_2742_ORIGIN, "ORG2742_0_radial_cell_rule;ORG2742_6_current_verdict", "phase-volume origin audit"),
        ("SRC2820_5_2742_mapping", SRC_2742_MAPPING, "MAP2742_3_auxiliary_norm_candidate;MAP2742_4_source_current;MAP2742_5_same_norm_Cqm", "q-sector mapping blockers"),
        ("SRC2820_6_2742_obstructions", SRC_2742_OBSTRUCTIONS, "OBS2742_3_positive_norm;OBS2742_4_matter_source;OBS2742_5_no_charge", "open phase-volume obstructions"),
        ("SRC2820_7_2742_runner", SRC_2742_RUNNER, "RUN2742_4_auxiliary_norm;RUN2742_6_source_norm;RUN2742_7_score_status", "nonclaim runner status"),
        ("SRC2820_8_2742_decision", SRC_2742_DECISION, "DEC2742_0_result;DEC2742_2_best_next;DEC2742_3_no_claim", "phase-volume decision"),
        ("SRC2820_9_2743_gauge", SRC_2743_GAUGE, "GAUGE2743_5_first_class_constraint;GAUGE2743_7_current_verdict", "gauge/Noether no-charge attempt"),
        ("SRC2820_10_2743_runner", SRC_2743_RUNNER, "RUN2743_5_first_class;RUN2743_7_score_status", "zero-charge runner refusal"),
        ("SRC2820_11_2743_decision", SRC_2743_DECISION, "DEC2743_0_result;DEC2743_3_reentry", "zero-charge decision and reentry contract"),
        ("SRC2820_12_2744_decision", SRC_2744_DECISION, "DEC2744_1_missing", "closure benchmark missing gates"),
        ("SRC2820_13_2745_decision", SRC_2745_DECISION, "DEC2745_0_verdict;DEC2745_3_next", "local deviation budget and coefficient-source next route"),
        ("SRC2820_14_2262_nonprop", SRC_2262_NONPROP, "NPR2262_0_algebraic_lock;NPR2262_1_no_hair;NPR2262_3_best_derivation_route", "nonpropagating constraint prior"),
        ("SRC2820_15_2268_tests", SRC_2268_TESTS, "OT2268_0_phase_cell_parent;OT2268_2_psi_covariance", "phase-cell and psi-map origin tests"),
        ("SRC2820_16_1554_origin", SRC_1554_ORIGIN, "ORG1554_0_radial_cell_rule;ORG1554_5_current_verdict", "older phase-volume audit"),
        ("SRC2820_17_2227_origin", SRC_2227_ORIGIN, "ORG2227_0_radial_cell_rule;ORG2227_5_current_verdict", "repeat phase-volume audit"),
    ]
    return [source_row(*spec) for spec in specs]


def origin_reentry_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PVR2820_0_exact_cell_equivalence",
            "radial t-r cell rule",
            "J_tr = T sqrt(S) = 1 <=> T^2 S = 1 <=> q=R_AB=0",
            "exactly selects the scalar p=1 / GR-lane benchmark",
            "PASS_ALGEBRAIC_NONCLAIM",
            "algebraic equivalence is useful, but it is not a parent theorem",
            SRC_2742_ORIGIN,
            "ORG2742_0_radial_cell_rule",
        ),
        (
            "PVR2820_1_generic_phase_volume",
            "generic Liouville/canonical volume",
            "J_q J_p = 1 for the canonical pair",
            "preserves full phase volume for every p",
            "REJECTED_TOO_WEAK",
            "cannot select p=1 or force q=0",
            SRC_2742_ORIGIN,
            "ORG2742_1_generic_phase_volume",
        ),
        (
            "PVR2820_2_nonpropagating_constraint",
            "hard algebraic closure",
            "S_lambda = int lambda_R q dV",
            "would impose q=0 without exterior gradient hair",
            "CLOSURE_ONLY_NOT_PARENT_DERIVED",
            "lambda origin and variational descent are still unsigned",
            SRC_2262_NONPROP,
            "NPR2262_0_algebraic_lock",
        ),
        (
            "PVR2820_3_auxiliary_positive_norm",
            "auxiliary q norm",
            "S_aux = 1/2 int mu_q^2 q^A G_AB q^B dV",
            "would supply E_q and avoid kinetic hair",
            "REFUSED_MISSING_COEFFICIENT_ORIGIN",
            "phase-volume does not derive mu_q^2 or G_AB",
            SRC_2742_MAPPING,
            "MAP2742_3_auxiliary_norm_candidate",
        ),
        (
            "PVR2820_4_matter_source",
            "matter q-current",
            "J_q = delta S_matter / delta q",
            "needed for T_source_norm and N_pair",
            "REFUSED_MISSING_PARENT_COUPLING",
            "no matter/readout map varies with q in the parent action",
            SRC_2742_MAPPING,
            "MAP2742_4_source_current",
        ),
        (
            "PVR2820_5_same_norm_response",
            "same-norm response coefficient",
            "C_qm = ||Dq[v_m]||_E",
            "needed to feed 2818 local-lock amplitude law",
            "REFUSED_MISSING_PARENT_NORM",
            "Dq[v_m] cannot be normed before E_q exists",
            SRC_2742_MAPPING,
            "MAP2742_5_same_norm_Cqm",
        ),
        (
            "PVR2820_6_zero_charge_guard",
            "no exterior reciprocal charge",
            "W partial_r R_AB = Q_R with required Q_R=0",
            "would prevent reciprocal hair",
            "REFUSED_NO_CHARGE_THEOREM",
            "2743 found no accepted first-class/no-charge origin",
            SRC_2743_DECISION,
            "DEC2743_0_result",
        ),
        (
            "PVR2820_7_reentry_verdict",
            "2818 local-lock reentry",
            "Delta_m <= C_emb N_lock with N_lock needing q-sector norm/source data",
            "cannot be reopened as a sourced result",
            "REENTRY_BLOCKED_PHASE_VOLUME_NOT_ENOUGH",
            "q closure remains a benchmark/closure route, not a derived local-GR route",
            SRC_2819_REENTRY,
            "LLR2819_5_claim_ceiling",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "audit_id": audit_id,
                "candidate": candidate,
                "mathematical_form": form,
                "what_it_would_supply": supply,
                "status": status,
                "reason": reason,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "accepted_parent_origin": False,
                "feeds_2818_reentry": False,
            }
        )
        for audit_id, candidate, form, supply, status, reason, source_path, anchor in specs
    ]


def mapping_rows() -> list[dict[str, Any]]:
    specs = [
        ("MAP2820_0_scalar_q", "q := R_AB = ln(T^2 S)", "scalar closure variable", "CONDITIONAL_SYMBOLIC_MAP", "not a full q^A family and not tracefree/PPN complete", SRC_2742_MAPPING, "MAP2742_0_scalar_q"),
        ("MAP2820_1_phase_cell_equivalence", "T sqrt(S)=1 <=> q=0", "connects phase-cell clue to closure", "EXACT_EQUIVALENCE_NONCLAIM", "equivalence is not the variational origin", SRC_2742_MAPPING, "MAP2742_1_radial_cell_equivalence"),
        ("MAP2820_2_multiplier", "lambda_q q", "nonpropagating closure", "CLOSURE_ONLY", "lambda_q is not parent-sourced", SRC_2742_MAPPING, "MAP2742_2_multiplier_closure"),
        ("MAP2820_3_GAB", "G_AB", "positive q-sector metric", "MISSING_PARENT_FORM", "no phase-volume theorem fixes the positive bilinear form", SRC_2742_OBSTRUCTIONS, "OBS2742_3_positive_norm"),
        ("MAP2820_4_muq", "mu_q^2", "algebraic stiffness/coefficient", "MISSING_PARENT_COEFFICIENT", "would be a hand penalty unless derived from parent capacity law", SRC_2742_RUNNER, "RUN2742_4_auxiliary_norm"),
        ("MAP2820_5_Jq", "J_q", "matter source current", "MISSING_PARENT_COUPLING", "matter variation with respect to q is absent", SRC_2742_OBSTRUCTIONS, "OBS2742_4_matter_source"),
        ("MAP2820_6_Dqvm", "Dq[v_m]", "local vertical/memory generator response", "MISSING_SAME_NORM_RESPONSE", "no accepted E_q exists in which to measure it", SRC_2819_EXTRACTION, "EXT2819_2_Dqvm"),
        ("MAP2820_7_boundary", "boundary/domain terms", "no-hair / domain guard", "CONDITIONAL_ONLY", "no exterior hair follows only after the nonpropagating route is parent-signed", SRC_2262_NONPROP, "NPR2262_1_no_hair"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "map_id": map_id,
                "qsector_object": obj,
                "role": role,
                "status": status,
                "blocker": blocker,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "accepted_for_claim": False,
                "feeds_2818_reentry": False,
            }
        )
        for map_id, obj, role, status, blocker, source_path, anchor in specs
    ]


def extraction_rows() -> list[dict[str, Any]]:
    specs = [
        ("EXT2820_0_q", "q", "local closure scalar", "CONDITIONAL_SYMBOLIC_ONLY", "q=R_AB is mapped, but parent q^A field family is not signed", "NO"),
        ("EXT2820_1_GAB", "G_AB", "positive q-sector metric", "MISSING", "needed for E_q and same-norm C_qm", "NO"),
        ("EXT2820_2_muq", "mu_q^2", "algebraic phase/capacity stiffness", "MISSING", "phase-volume does not provide the coefficient", "NO"),
        ("EXT2820_3_Eq", "E_q", "positive parent q norm", "REFUSED", "requires G_AB and mu_q^2 from a parent origin", "NO"),
        ("EXT2820_4_Jq", "J_q", "source current", "REFUSED", "requires explicit S_matter[q] or matter descent", "NO"),
        ("EXT2820_5_Dqvm", "Dq[v_m]", "same-norm vertical response", "REFUSED", "cannot be evaluated without E_q and q-map differential", "NO"),
        ("EXT2820_6_boundary", "B_q", "boundary/domain contribution", "UNSIGNED", "no exterior hair is conditional on nonpropagating parent route", "NO"),
        ("EXT2820_7_Tsource_Cqm", "T_source_norm*C_qm", "2818 local-lock input", "REFUSED", "same-norm holder product cannot be sourced", "NO"),
        ("EXT2820_8_Nlock", "N_lock", "local-lock amplitude driver", "CLOSURE_ONLY", "remains the 2818 staged bound, not a source-backed prediction", "NO"),
    ]
    return [
        nonclaim(
            {
                "extraction_id": extraction_id,
                "quantity": quantity,
                "required_role": role,
                "status": status,
                "blocker": blocker,
                "feeds_2818_reentry": feeds,
                "source_path": str(SRC_2819_EXTRACTION),
                "source_anchor": "EXT2819_0_Eq;EXT2819_1_Jq;EXT2819_2_Dqvm",
                "accepted_parent_input": False,
            }
        )
        for extraction_id, quantity, role, status, blocker, feeds in specs
    ]


def reentry_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("LLG2820_0_2818_chain", "2818 Delta_m amplitude law", "AVAILABLE_CONDITIONAL", "Delta_m <= C_emb N_lock already exists", True, False),
        ("LLG2820_1_qnorm", "positive q norm E_q", "BLOCKED", "G_AB and mu_q^2 not parent-derived", False, False),
        ("LLG2820_2_source", "matter source J_q", "BLOCKED", "no S_matter[q] or q-readout map", False, False),
        ("LLG2820_3_response", "same-norm Dq[v_m]", "BLOCKED", "no accepted norm for the vertical generator", False, False),
        ("LLG2820_4_no_hair", "nonpropagating/no exterior hair guard", "CONDITIONAL_ONLY", "works if the closure is imposed, not as a parent theorem", True, False),
        ("LLG2820_5_zero_charge", "Q_R=0 no-charge theorem", "BLOCKED", "2743 found no accepted zero-charge origin", False, False),
        ("LLG2820_6_local_reentry", "2818 local-lock reentry", "REFUSED", "required q-sector inputs remain absent", False, False),
        ("LLG2820_7_claim_ceiling", "local GR/Newton/PPN/R10 claims", "BLOCKED_NO_CLAIM", "closure-only data cannot be scored as derived physics", False, False),
    ]
    return [
        nonclaim(
            {
                "gate_id": gate_id,
                "object": obj,
                "status": status,
                "reason": reason,
                "conditional_piece_available": conditional_piece,
                "reentry_allowed": reentry_allowed,
                "source_path": str(SRC_2819_REENTRY),
            }
        )
        for gate_id, obj, status, reason, conditional_piece, reentry_allowed in specs
    ]


def filter_rows() -> list[dict[str, Any]]:
    specs = [
        ("FLT2820_0_no_hand_penalty", "do not insert mu_q^2 by hand", "PASS_BLOCKS_PROMOTION", "auxiliary norm remains private unless coefficient is parent-derived"),
        ("FLT2820_1_no_generic_phase_volume", "do not use generic Liouville volume as p=1 proof", "PASS_BLOCKS_PROMOTION", "generic canonical volume is p-blind"),
        ("FLT2820_2_no_GR_import", "do not import Schwarzschild AB=1", "PASS_BLOCKS_PROMOTION", "would make the local-GR reduction circular"),
        ("FLT2820_3_no_boundary_deletion", "do not delete Q_R or boundary charge by hand", "PASS_BLOCKS_PROMOTION", "zero-charge theorem must be parent-signed"),
        ("FLT2820_4_no_mixed_norm", "do not pair source and response in different norms", "PASS_BLOCKS_REENTRY", "T_source_norm*C_qm is legal only in one E_q norm"),
        ("FLT2820_5_no_local_claim", "do not score closure rows as predictions", "PASS_BLOCKS_CLAIM", "R_AB=0 remains a benchmark closure"),
    ]
    return [
        nonclaim(
            {
                "filter_id": filter_id,
                "filter": filter_text,
                "status": status,
                "reason": reason,
                "active": True,
            }
        )
        for filter_id, filter_text, status, reason in specs
    ]


def gate_rows(sources: list[dict[str, Any]], origin: list[dict[str, Any]], mapping: list[dict[str, Any]], extraction: list[dict[str, Any]], reentry: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_pass = all(row["path_exists"] and row["anchors_found"] for row in sources)
    phase_origin_proved = any(row["accepted_parent_origin"] for row in origin)
    q_inputs_extracted = all(
        any(row["quantity"] == quantity and row["accepted_parent_input"] for row in extraction)
        for quantity in ["E_q", "J_q", "Dq[v_m]"]
    )
    reentry_allowed = any(row["reentry_allowed"] for row in reentry if row["object"] == "2818 local-lock reentry")
    specs = [
        ("CG2820_0_sources_anchored", "2820 sources and anchors are present", source_pass, "source register resolves all imported ledgers"),
        ("CG2820_1_phase_origin_parent_proved", "phase-volume parent origin proved", phase_origin_proved, "phase-volume remains motivated-not-derived"),
        ("CG2820_2_positive_qnorm", "G_AB/mu_q/E_q extracted", q_inputs_extracted, "positive same-norm q norm is not supplied"),
        ("CG2820_3_matter_source", "J_q matter source extracted", q_inputs_extracted, "matter q-coupling is absent"),
        ("CG2820_4_same_norm_response", "Dq[v_m] extracted in E_q", q_inputs_extracted, "same-norm response is absent"),
        ("CG2820_5_local_lock_reentry", "2818 local-lock reentry allowed", reentry_allowed, "N_lock remains closure-only"),
        ("CG2820_6_local_claim", "local GR/Newton/PPN/R10 claim allowed", False, "no sourced local branch exists"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": passed,
                "status": "PASS_NONCLAIM" if passed else "BLOCKED",
                "reason": reason,
            }
        )
        for gate_id, claim, passed, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2820_0_verdict",
            "Phase-volume/nonpropagating origin does not reopen local-lock reentry.",
            "NO_PARENT_ORIGIN_NO_REENTRY",
            "the exact radial-cell algebra survives, but G_AB, mu_q, E_q, J_q, Dq[v_m], and zero-charge remain unsigned",
            "keep closure benchmark quarantined",
        ),
        (
            "DEC2820_1_keep_clue",
            "Keep J_tr=T sqrt(S)=1 as a strong private clue.",
            "RETAIN_ALGEBRAIC_GR_LANE",
            "it selects p=1 exactly, so it remains useful as a target structure",
            "do not treat it as a derivation",
        ),
        (
            "DEC2820_2_no_cycle",
            "Do not loop back into phase-volume or gauge/no-charge as if they were new.",
            "ROUTE_ALREADY_TESTED",
            "2742 and 2743 already performed those attempts and blocked claims",
            "attack the coupling/source-current map next",
        ),
        (
            "DEC2820_3_next",
            "Next target is parent coupling/source-current and same-norm map.",
            "NEXT_2821_PARENT_COUPLING_MAP",
            "without J_q and Dq[v_m] in the same E_q norm the 2818 local-lock branch cannot become test-ready",
            "derive or reject the coupling rather than adding a coefficient",
        ),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, result, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2820_0_2821",
                "status": "selected_primary",
                "target_doc": "2821-Y5-R2FR-parent-coupling-source-current-and-same-norm-map-for-local-lock-reentry-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_parent_coupling_source_current_and_same_norm_map_for_local_lock_reentry_under_AX1090_2821.py",
                "mission": "derive or reject the parent matter/readout coupling that supplies J_q and Dq[v_m] in the same E_q norm, so the 2818 local-lock amplitude route can either reenter or be demoted to closure-only testing",
                "acceptance": "produce parent-signed q/matter map with G_AB or an accepted norm, J_q, Dq[v_m], boundary terms, and no mixed-norm leakage; otherwise write explicit closure-only test rows with valid_for_claim=false",
                "forbidden": "do not hand-insert coupling coefficients; do not use phase-volume or AB=1 as a proof; do not claim local GR/Newton/PPN/R10; do not edit formalization-workbench",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copy_specs = [
        ("BR2820_0_origin_weight", OUTPUTS["origin_reentry"], BRANCH_OUTPUTS["origin_weight"], "source-weight copy of phase-volume local-lock reentry audit"),
        ("BR2820_1_local_gate", OUTPUTS["reentry_gate"], BRANCH_OUTPUTS["local_gate"], "local-bound copy of reentry gate"),
        ("BR2820_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue for parent coupling/source-current next target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in copy_specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            nonclaim(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "source_paths", "copy_path", "source_table"}
    found: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if value is None:
                    continue
                for token in str(value).split(";"):
                    item = token.strip()
                    if not item or item.startswith("http"):
                        continue
                    path = Path(item)
                    if not path.is_absolute():
                        path = ROOT / item
                    found.append(path)
    return found


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start_stamp = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            try:
                if path.stat().st_mtime >= start_stamp:
                    return False
            except OSError:
                return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            for key in ("valid_for_claim", "claim_allowed", "score_ready", "valid_prediction_row"):
                if str(row.get(key, "")).lower() == "true":
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values())
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2820_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2820_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2820_2_phase_origin_unclaimed", not any(row["accepted_parent_origin"] for row in rows_by_name["origin_reentry"]), "phase-volume origin remains unaccepted"),
        ("VAL2820_3_q_inputs_blocked", not any(row["accepted_parent_input"] for row in rows_by_name["extraction"]), "no Eq/Jq/Dqvm parent inputs were accepted"),
        ("VAL2820_4_reentry_blocked", not any(row["reentry_allowed"] for row in rows_by_name["reentry_gate"]), "local-lock reentry remains blocked"),
        ("VAL2820_5_next_target_2821", any(row["next_id"] == "NEXT2820_0_2821" and row["selected"] for row in rows_by_name["next"]), "parent coupling/source-current map selected next"),
        ("VAL2820_6_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2820_7_outputs_exist", all(path.exists() for path in output_paths if path != OUTPUTS["validation"]), "all generated output paths exist before validation write"),
        ("VAL2820_8_csv_parse", all(csv_parses(path) for path in output_paths if path.exists() and path != OUTPUTS["validation"]), "all generated CSV outputs parse"),
        ("VAL2820_9_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2820_10_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim, or claim_allowed flag is true"),
        ("VAL2820_11_generated_under_post_checkpoint", all(str(path).startswith(str(ROOT)) for path in output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2820_12_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2820_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2820_OVERALL",
            "passed": overall,
            "detail": "2820 blocks phase-volume/nonpropagating q-sector origin as a parent derivation for local-lock reentry, preserves the exact radial-cell clue as nonclaim, and selects parent coupling/source-current mapping next.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2820 - Y5 R2FR Phase-Volume Nonpropagating Qsector Origin For Local Lock Reentry Under AX1090

Status: `Y5_R2FR_2820_phase_volume_origin_blocks_local_lock_reentry_parent_coupling_selected_next`

## Private Verdict

2820 gives the phase-volume/nonpropagating q-sector route its local-lock reentry test. It does not pass as a parent derivation.

The good piece survives: `J_tr = T sqrt(S) = 1 <=> T^2 S = 1 <=> q=R_AB=0`. That is still an exact and useful GR-lane target. The failure is not the algebra; the failure is the missing parent origin and coupling.

For 2818 reentry we still need `G_AB`, `mu_q`, `E_q`, `J_q`, `Dq[v_m]`, boundary/domain control, and a zero-charge/no-hair guard in one parent-signed construction. Phase-volume motivates the closure but does not supply those objects. Therefore local-lock reentry remains blocked and local GR/Newton/PPN/R10 claims remain forbidden.

The anti-circling move is to stop re-running phase-volume as proof. The next best target is the coupling/source-current map: either derive `J_q` and `Dq[v_m]` in the same norm, or demote this branch to explicit closure-only testing.

## Source Register

{markdown_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Phase-Volume Origin Reentry Audit

{markdown_table(rows_by_name["origin_reentry"], ["audit_id", "candidate", "status", "reason", "accepted_parent_origin", "feeds_2818_reentry", "valid_for_claim"])}

## Qsector Origin Mapping Status

{markdown_table(rows_by_name["mapping"], ["map_id", "qsector_object", "status", "blocker", "accepted_for_claim", "feeds_2818_reentry", "valid_for_claim"])}

## Eq Mu GAB Extraction Status

{markdown_table(rows_by_name["extraction"], ["extraction_id", "quantity", "status", "blocker", "feeds_2818_reentry", "accepted_parent_input", "valid_for_claim"])}

## Local Lock Reentry Gate

{markdown_table(rows_by_name["reentry_gate"], ["gate_id", "object", "status", "reason", "conditional_piece_available", "reentry_allowed", "valid_for_claim"])}

## Failure Filters

{markdown_table(rows_by_name["filters"], ["filter_id", "filter", "status", "reason", "active", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows_by_name["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "claim_allowed", "reason"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"], ["decision_id", "decision", "result", "because", "next_action", "valid_for_claim"])}

## Next Target

{markdown_table(rows_by_name["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows_by_name["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name: dict[str, list[dict[str, Any]]] = {}
    rows_by_name["sources"] = source_rows()
    rows_by_name["origin_reentry"] = origin_reentry_rows()
    rows_by_name["mapping"] = mapping_rows()
    rows_by_name["extraction"] = extraction_rows()
    rows_by_name["reentry_gate"] = reentry_gate_rows()
    rows_by_name["filters"] = filter_rows()
    rows_by_name["gates"] = gate_rows(
        rows_by_name["sources"],
        rows_by_name["origin_reentry"],
        rows_by_name["mapping"],
        rows_by_name["extraction"],
        rows_by_name["reentry_gate"],
    )
    rows_by_name["decision"] = decision_rows()
    rows_by_name["next"] = next_rows()

    for key in ["sources", "origin_reentry", "mapping", "extraction", "reentry_gate", "filters", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows_by_name[key])

    rows_by_name["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows_by_name["branches"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)

    overall = next(row for row in rows_by_name["validation"] if row["validation_id"] == "VAL2820_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2820_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
