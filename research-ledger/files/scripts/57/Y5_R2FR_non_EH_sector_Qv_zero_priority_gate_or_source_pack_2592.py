from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_NON_EH_QV_ZERO_GATE_2592"
CHECKPOINT_ID = "2592"

DOC = ROOT / "2592-Y5-R2FR-non-EH-sector-Qv-zero-priority-gate-or-source-pack.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NON_EH_QV_2592_SOURCE_REGISTER.csv",
    "zero_priority_gate": OUT / "P8_Y5_NON_EH_QV_2592_ZERO_PRIORITY_GATE.csv",
    "source_pack": OUT / "P8_Y5_NON_EH_QV_2592_SOURCE_PACK.csv",
    "runner_refusal": OUT / "P8_Y5_NON_EH_QV_2592_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_NON_EH_QV_2592_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NON_EH_QV_2592_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NON_EH_QV_2592_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NON_EH_QV_2592_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2592_VALIDATION.csv",
}

COPY_TARGETS = {
    "zero_priority_gate": QUEUE / "JR2592_NON_EH_QV_ZERO_PRIORITY_GATE_NONCLAIM.csv",
    "source_pack": LOCAL_BOUNDS / "Non_EH_Qv_source_pack_2592_NONCLAIM.csv",
    "next_target": QUEUE / "JR2592_EXTRA_RESPONSE_QV_ZERO_ODD_SOURCE_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:  # pragma: no cover - validation reports the error.
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    source_specs = [
        {
            "source_id": "SRC2592_00_2591_handoff",
            "source_path": ROOT / "2591-Y5-R2FR-vertical-sector-variation-ledger-or-Qv-piece-leak-rows.md",
            "needles": ["NEXT2591_0_selected", "VSL2591_2_extra_response", "VAL2591_OVERALL"],
            "role": "active handoff selecting non-EH Qv zero/source-pack gate",
        },
        {
            "source_id": "SRC2592_01_2591_next_queue",
            "source_path": QUEUE / "JR2591_NON_EH_QV_SECTOR_ZERO_OR_SOURCE_PACK_NEXT.csv",
            "needles": ["NEXT2591_0_selected", "2592-Y5-R2FR-non-EH-sector-Qv-zero-priority-gate-or-source-pack.md"],
            "role": "machine-readable 2592 task and guardrails",
        },
        {
            "source_id": "SRC2592_02_1009_sector_contract",
            "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "needles": ["PCS1009_3_boundary_reference", "PCS1009_7_memory_response_doublet", "PCS1009_9_total_parent_contract"],
            "role": "parent current-chain sector contract and guardrails",
        },
        {
            "source_id": "SRC2592_03_extra_response",
            "source_path": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            "needles": ["RD516_1_even_scalar_density", "RD516_4_zero_odd_source", "RD516_6_boundary_no_flux"],
            "role": "extra/response local-silence clauses",
        },
        {
            "source_id": "SRC2592_04_projector_contract",
            "source_path": OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
            "needles": ["PM5_projector_variation_owned", "PM6_flux_closure_requires_Ward_or_Euler"],
            "role": "projector variation and Ward/Euler closure gaps",
        },
        {
            "source_id": "SRC2592_05_worldtube_glue",
            "source_path": OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
            "needles": ["W504_4_worldtube_source_measure_glue", "W504_5_calibration_and_limits"],
            "role": "worldtube/source-measure glue and Newton calibration clauses",
        },
        {
            "source_id": "SRC2592_06_matter_descent",
            "source_path": ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
            "needles": ["MWD1760_1_conditional_theorem", "PRE1760_8_verdict", "VAL1760_OVERALL"],
            "role": "matter descent exact conditional theorem and remaining premises",
        },
        {
            "source_id": "SRC2592_07_hidden_source",
            "source_path": ROOT / "1756-Y5-R2FR-two-slot-source-free-owner-or-hidden-source-counterexample-ledger.md",
            "needles": ["HSC1756_9_verdict", "HSR1756_9_total", "VAL1756_OVERALL"],
            "role": "hidden-source/direct-slot obstruction ledger",
        },
        {
            "source_id": "SRC2592_08_noether_chain",
            "source_path": OUT / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
            "needles": ["D505_3_exterior_derivative", "D505_4_zero_premises"],
            "role": "C-term/constraint closure chain",
        },
    ]
    rows: list[dict[str, Any]] = []
    for source in source_specs:
        source_path = source["source_path"]
        missing_needles = path_has_needles(source_path, source["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": source_path,
                    "exists": source_path.exists(),
                    "missing_needles": missing_needles,
                    "source_pass": source_path.exists() and not missing_needles,
                    "role": source["role"],
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def zero_priority_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "ZNE2592_0_boundary_Bv",
            "sector": "boundary/reference",
            "zero_condition": "B_v and reference subtraction are fixed before readout, and int_S delta B_v=0 on compact linked local surfaces",
            "current_status": "MISSING_FIXED_BV_AND_ZERO_COMPACT_FLUX",
            "why_priority": "boundary terms can fake a zero total charge or absorb a residual",
            "if_not_zero": "epsilon_Bv_ambiguity remains in the local Qv budget",
            "primary_source": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        },
        {
            "gate_id": "ZNE2592_1_extra_response",
            "sector": "extra/response motion-time-memory",
            "zero_condition": "extra response is even at the local branch, has positive self-adjoint operator, zero odd local source, PPN lock and no boundary flux",
            "current_status": "MISSING_ZERO_ODD_SOURCE_AND_FULL_VARIATION",
            "why_priority": "this is the MTS novelty channel most likely to become local charge hair",
            "if_not_zero": "epsilon_Qv_extra_piece must be bounded or the local-GR route fails",
            "primary_source": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
        },
        {
            "gate_id": "ZNE2592_2_projector_source_measure",
            "sector": "projector/source-measure Pi_M",
            "zero_condition": "Pi_M is parent-symplectic, delta Pi_M is owned, and d(Pi_M J_H)=0 follows from Ward/Euler closure rather than algebra alone",
            "current_status": "MISSING_PROJECTOR_VARIATION_AND_WARD_CLOSURE",
            "why_priority": "projector algebra can look like a mass theorem while hiding source-normalization drift",
            "if_not_zero": "epsilon_Qv_projector_piece and epsilon_Cv_constraint_missing remain live",
            "primary_source": OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        },
        {
            "gate_id": "ZNE2592_3_matter_worldtube",
            "sector": "matter/source/worldtube",
            "zero_condition": "ordinary matter descends through q/e_obs, no direct source slot exists, and worldtube source measure equals exterior Noether charge before fitting",
            "current_status": "MISSING_MATTER_DESCENT_STACK_AND_WORLDTUBE_GLUE",
            "why_priority": "even a silent geometry sector fails if source mass and exterior charge are not the same object",
            "if_not_zero": "epsilon_Qv_matter_source_piece, epsilon_matter_kernel and epsilon_hidden_source_slot remain live",
            "primary_source": ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
        },
        {
            "gate_id": "ZNE2592_4_constraint_Cv",
            "sector": "constraint total",
            "zero_condition": "C_v pieces are parent EOM/proper constraints in the same branch or are source-bounded in one declared norm",
            "current_status": "MISSING_COMMON_CONSTRAINT_SPLIT",
            "why_priority": "Noether identity is not the same as zero residual current",
            "if_not_zero": "epsilon_Cv_constraint_missing remains live",
            "primary_source": OUT / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
        },
        {
            "gate_id": "ZNE2592_5_same_branch",
            "sector": "same parent branch compatibility",
            "zero_condition": "boundary, extra, projector, matter/worldtube and constraint clauses hold simultaneously with one q/e_obs/tau/M_H_ref branch",
            "current_status": "MISSING_SAME_BRANCH_COMPATIBILITY_PROOF",
            "why_priority": "sector-by-sector zeroes do not help if they require different branches or normalizations",
            "if_not_zero": "epsilon_non_EH_branch_mismatch remains live",
            "primary_source": ROOT / "2591-Y5-R2FR-vertical-sector-variation-ledger-or-Qv-piece-leak-rows.md",
        },
        {
            "gate_id": "ZNE2592_6_verdict",
            "sector": "non-EH total",
            "zero_condition": "all non-EH sectors above are theorem-zero, fixed-before-readout, constraint-proportional or source-bounded in one branch",
            "current_status": "NON_EH_LOCAL_SILENCE_NOT_PROVED_CURRENT_CORPUS",
            "why_priority": "this is the present local-GR bottleneck",
            "if_not_zero": "Delta_non_EH_Qv_total_over_MH remains nonclaim",
            "primary_source": DOC,
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "source_path_exists": Path(row["primary_source"]).exists() if row["primary_source"] != DOC else True,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def source_pack_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "NES2592_0_Bv",
            "symbol": "epsilon_Bv_ambiguity",
            "definition": "abs(int_S delta B_v_unfixed)/M_H_ref",
            "units": "dimensionless boundary-improvement ambiguity",
            "current_value": "MISSING_FIXED_BV_CONVENTION;MISSING_ZERO_BOUNDARY_FLUX;MISSING_M_H_REF",
            "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "observable_link": "boundary;clock;orbital;PPN",
        },
        {
            "row_id": "NES2592_1_extra",
            "symbol": "epsilon_Qv_extra_piece",
            "definition": "abs(int_S(Q_v^extra + C_v^extra - i_v Theta_extra))/M_H_ref",
            "units": "dimensionless extra-sector vertical charge",
            "current_value": "MISSING_EXTRA_SECTOR_VARIATION;MISSING_ZERO_ODD_SOURCE;MISSING_PPN_LOCK;MISSING_BOUNDARY_NO_FLUX;MISSING_M_H_REF",
            "source_path": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            "observable_link": "PPN;R10;clock;cosmology_branching",
        },
        {
            "row_id": "NES2592_2_projector",
            "symbol": "epsilon_Qv_projector_piece",
            "definition": "abs(int_S(Q_v^projector + C_v^projector - i_v Theta_projector))/M_H_ref",
            "units": "dimensionless projector/source-measure vertical charge",
            "current_value": "MISSING_PROJECTOR_VARIATION_OWNER;MISSING_WARD_OR_EULER_CLOSURE;MISSING_M_H_REF",
            "source_path": OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
            "observable_link": "source_mass;Newton;orbital;PPN",
        },
        {
            "row_id": "NES2592_3_matter_source",
            "symbol": "epsilon_Qv_matter_source_piece",
            "definition": "abs(int_S(Q_v^matter/source + C_v^matter - i_v Theta_matter/source))/M_H_ref",
            "units": "dimensionless matter/source vertical charge",
            "current_value": "MISSING_MATTER_DESCENT;MISSING_WORLDTUBE_GLUE;MISSING_NO_DIRECT_SOURCE_SLOT;MISSING_M_H_REF",
            "source_path": ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
            "observable_link": "WEP;source_mass;orbital;Newton",
        },
        {
            "row_id": "NES2592_4_Cv",
            "symbol": "epsilon_Cv_constraint_missing",
            "definition": "abs(int_S C_v_nonconstraint_or_unbounded)/M_H_ref",
            "units": "dimensionless constraint leakage",
            "current_value": "MISSING_COMMON_CONSTRAINT_SPLIT;MISSING_PARENT_EOM_SOURCE;MISSING_M_H_REF",
            "source_path": OUT / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
            "observable_link": "Bianchi;conservation;source_current",
        },
        {
            "row_id": "NES2592_5_branch",
            "symbol": "epsilon_non_EH_branch_mismatch",
            "definition": "1 if non-EH zero conditions require incompatible q/e_obs/tau/M_H_ref branches else 0",
            "units": "boolean branch-compatibility guard",
            "current_value": "MISSING_SAME_BRANCH_COMPATIBILITY_PROOF",
            "source_path": ROOT / "2591-Y5-R2FR-vertical-sector-variation-ledger-or-Qv-piece-leak-rows.md",
            "observable_link": "q_owner;same_frame;local_GR",
        },
        {
            "row_id": "NES2592_TOTAL",
            "symbol": "Delta_non_EH_Qv_total_over_MH",
            "definition": "epsilon_Bv_ambiguity + epsilon_Qv_extra_piece + epsilon_Qv_projector_piece + epsilon_Qv_matter_source_piece + epsilon_Cv_constraint_missing + epsilon_non_EH_branch_mismatch",
            "units": "dimensionless after M_H_ref",
            "current_value": "COMPONENTS_MISSING",
            "source_path": DOC,
            "observable_link": "q_owner;Newton;local_GR;PPN;R10;clock;orbital",
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "source_path_exists": Path(row["source_path"]).exists() if row["source_path"] != DOC else True,
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def runner_refusal_rows(source_pack: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in source_pack:
        reasons = ["VALID_FOR_CLAIM_FALSE", "MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE"]
        if not row["source_path_exists"]:
            reasons.append("MISSING_SOURCE_PATH")
        if row["symbol"] == "epsilon_Qv_extra_piece":
            reasons.append("MTS_NOVELTY_LOCAL_SILENCE_NOT_PROVED")
        if row["row_id"] == "NES2592_TOTAL":
            reasons.append("NON_EH_COMPONENTS_NOT_SCORE_READY")
        rows.append(
            with_stamp(
                {
                    "runner_id": f"NER2592_{row['row_id']}",
                    "target_id": row["row_id"],
                    "symbol": row["symbol"],
                    "verdict": "REFUSED_NONCLAIM_NON_EH_QV_ROW",
                    "failure_reasons": reasons,
                    "score_ready": False,
                    "claim_allowed": False,
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "CG2592_0_priority_gate_shape",
            "claim": "non-EH local silence priority gate is explicit",
            "gate_status": "PASS_NONCLAIM_STRUCTURE_ONLY",
            "reason": "boundary, extra, projector, matter/worldtube, constraint and branch-compatibility tests are separated",
            "gate_pass": True,
        },
        {
            "gate_id": "CG2592_1_non_EH_zero",
            "claim": "all non-EH vertical Q_v pieces vanish locally",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "zero conditions are written but not parent-signed",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2592_2_extra_response_zero",
            "claim": "MTS novelty channel is locally silent",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "extra/response full variation, zero odd source, PPN lock and boundary no-flux are missing",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2592_3_projector_matter_source",
            "claim": "projector and matter/source sectors carry no vertical charge",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "projector Ward/Euler closure and matter/worldtube glue are unsigned",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2592_4_same_branch",
            "claim": "all zeroes hold in one q/e_obs/tau/M_H_ref branch",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "same-branch compatibility is not proved",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2592_5_local_GR_Newton",
            "claim": "local GR/Newton follows from the non-EH gate",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "the gate identifies missing local-silence conditions; it does not close them",
            "gate_pass": False,
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2592_0_non_EH_priority_gate_accepted",
            "decision": "NON_EH_LOCAL_SILENCE_IS_THE_CURRENT_GR_BOTTLENECK",
            "reason": "EH reference behavior cannot carry MTS to local GR unless the novelty sectors are silent or bounded",
            "effect": "the project now targets non-EH Qv zero conditions rather than total-charge rhetoric",
        },
        {
            "decision_id": "DEC2592_1_no_silence_claim",
            "decision": "NON_EH_QV_ZERO_NOT_CLAIMED",
            "reason": "boundary, extra, projector, matter/worldtube, constraint and same-branch clauses remain unsigned",
            "effect": "Delta_non_EH_Qv_total_over_MH remains nonclaim",
        },
        {
            "decision_id": "DEC2592_2_next",
            "decision": "EXTRA_RESPONSE_ZERO_ODD_SOURCE_SELECTED_NEXT",
            "reason": "the distinctive MTS sector is the highest-leverage local-GR risk: if it is not locally silent, the branch is not GR-like",
            "effect": "2593 should attack the extra/response Qv zero theorem or source-pack epsilon_Qv_extra_piece",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2592_0_selected",
            "selection_status": "selected",
            "target_file": "2593-Y5-R2FR-extra-response-Qv-zero-odd-source-or-extra-piece-bound.md",
            "target_script": "scripts/Y5_R2FR_extra_response_Qv_zero_odd_source_or_extra_piece_bound_2593.py",
            "task": "try to prove the extra/response sector has even local density, positive self-adjoint operator, zero odd source, PPN lock and zero boundary flux so Q_v^extra vanishes",
            "success_condition": "epsilon_Qv_extra_piece is theorem-zero in the same local branch",
            "fallback_condition": "source-pack epsilon_Qv_extra_piece with action/variation/operator/source/boundary rows and valid_for_claim=false",
            "guardrails": "no local-GR claim; no total-zero switch; no EH-only import; no hidden source cancellation; no fitted M_H_ref; no GitHub; no formalization-workbench edits",
            "valid_for_claim": False,
        }
    ]
    return [with_stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target_path in COPY_TARGETS.items():
        source_path = OUTPUTS[copy_id]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2592_{copy_id}",
                    "source_path": source_path,
                    "target_path": target_path,
                    "source_exists": source_path.exists(),
                    "target_exists": target_path.exists(),
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(data: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in data.values():
        for row in rows:
            if row.get("valid_for_claim") is True or row.get("claim_allowed") is True:
                return False
    return True


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(
            with_stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if condition else "FAIL",
                    "notes": notes,
                    "detail": detail,
                    "valid_for_claim": False,
                }
            )
        )

    add("VAL2592_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    required_gate_sectors = {"boundary/reference", "extra/response motion-time-memory", "projector/source-measure Pi_M", "matter/source/worldtube", "constraint total", "same parent branch compatibility", "non-EH total"}
    present_gate_sectors = {row["sector"] for row in data["zero_priority_gate"]}
    add("VAL2592_01_priority_gate_complete", required_gate_sectors.issubset(present_gate_sectors), "priority gate covers all non-EH local-silence sectors")
    add("VAL2592_02_gate_source_paths_exist", all(row["source_path_exists"] is True for row in data["zero_priority_gate"]), "all priority-gate rows have existing source paths")
    required_symbols = {"epsilon_Bv_ambiguity", "epsilon_Qv_extra_piece", "epsilon_Qv_projector_piece", "epsilon_Qv_matter_source_piece", "epsilon_Cv_constraint_missing", "epsilon_non_EH_branch_mismatch", "Delta_non_EH_Qv_total_over_MH"}
    present_symbols = {row["symbol"] for row in data["source_pack"]}
    add("VAL2592_03_source_pack_symbols_present", required_symbols.issubset(present_symbols), "all non-EH source-pack symbols are present")
    add("VAL2592_04_source_pack_paths_exist", all(row["source_path_exists"] is True for row in data["source_pack"]), "source-pack rows point to existing local evidence")
    add(
        "VAL2592_05_rows_nonclaim",
        all(row["score_ready"] is False and row["valid_for_claim"] is False for row in data["source_pack"]),
        "non-EH source-pack rows remain non-score-ready and nonclaim",
    )
    add(
        "VAL2592_06_runner_refuses",
        all(row["score_ready"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]),
        "runner refuses all unfilled non-EH Qv rows",
    )
    add(
        "VAL2592_07_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"])
        and any(row["gate_id"] == "CG2592_2_extra_response_zero" and row["gate_pass"] is False for row in data["claim_gates"]),
        "non-EH zero, local-GR and Newton claims remain blocked",
    )
    add("VAL2592_08_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row sets valid_for_claim=true or claim_allowed=true")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2592-Y5-R2FR-non-EH*",
            "*Y5_R2FR_non_EH_sector_Qv*",
            "*P8_Y5_NON_EH_QV_2592*",
            "*JR2592*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2592_09_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2592 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )
    add(
        "VAL2592_10_next_selected",
        any(row["route_id"] == "NEXT2592_0_selected" and "2593-Y5-R2FR-extra-response-Qv-zero" in row["target_file"] for row in data["next"]),
        "2593 extra/response Qv zero target selected next",
    )
    add(
        "VAL2592_11_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2592_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2592_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2592_OVERALL",
        overall,
        "2592 installs the non-EH Qv local-silence priority gate, keeps source-pack rows nonclaim, and selects extra/response zero-odd-source as the next derivation target",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [row_value(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2592 Y5 R2FR non-EH sector Qv zero priority gate or source pack",
        "",
        "**Status:** private nonclaim derivation checkpoint. The non-EH local-silence gate is explicit, but current MTS has not proved boundary, extra/response, projector/source-measure, matter/worldtube and constraint pieces vanish or are harmless in one parent branch.",
        "",
        "**Main result:** the local-GR route now has a sharper bottleneck: prove MTS novelty is locally silent, not just that the EH reference sector behaves. The highest-leverage next target is the extra/response sector because it is the distinctive motion/time/memory channel most likely to carry local vertical charge.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Zero Priority Gate",
        markdown_table(data["zero_priority_gate"], ["gate_id", "sector", "zero_condition", "current_status", "why_priority", "if_not_zero", "primary_source", "source_path_exists", "valid_for_claim", "claim_allowed"]),
        "",
        "## Source Pack",
        markdown_table(data["source_pack"], ["row_id", "symbol", "definition", "units", "current_value", "source_path", "source_path_exists", "observable_link", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Runner Refusal",
        markdown_table(data["runner_refusal"], ["runner_id", "target_id", "symbol", "verdict", "failure_reasons", "score_ready", "claim_allowed", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
        "## Practical Status",
        "",
        "This checkpoint does not win local GR. It does something more useful: it tells us the next fair fight. If the extra/response sector can be made even, positive, source-odd-silent and boundary-silent, the MTS novelty can plausibly coexist with local GR. If it cannot, the theory has to own a finite local residual instead of hiding behind the EH reference.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    source_pack = source_pack_rows()
    data = {
        "sources": source_register_rows(),
        "zero_priority_gate": zero_priority_gate_rows(),
        "source_pack": source_pack,
        "runner_refusal": runner_refusal_rows(source_pack),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["zero_priority_gate"], data["zero_priority_gate"])
    write_csv(OUTPUTS["source_pack"], data["source_pack"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2592_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
