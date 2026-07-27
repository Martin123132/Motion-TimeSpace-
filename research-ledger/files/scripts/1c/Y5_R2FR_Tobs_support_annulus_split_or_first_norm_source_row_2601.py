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

BRANCH_ID = "MTS_R2FR_TOBS_SUPPORT_ANNULUS_REBASE_2601"
CHECKPOINT_ID = "2601"

DOC = ROOT / "2601-Y5-R2FR-Tobs-support-annulus-split-or-first-norm-source-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_TOBS_ANNULUS_REBASE_2601_SOURCE_REGISTER.csv",
    "lineage_ledger": OUT / "P8_Y5_TOBS_ANNULUS_REBASE_2601_LINEAGE_LEDGER.csv",
    "annulus_retest": OUT / "P8_Y5_TOBS_ANNULUS_REBASE_2601_ANNULUS_RETEST.csv",
    "bridge_rows": OUT / "P8_Y5_TOBS_ANNULUS_REBASE_2601_CURRENT_OWNER_BRIDGE_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_TOBS_ANNULUS_REBASE_2601_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_TOBS_ANNULUS_REBASE_2601_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_TOBS_ANNULUS_REBASE_2601_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_TOBS_ANNULUS_REBASE_2601_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_TOBS_ANNULUS_REBASE_2601_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2601_VALIDATION.csv",
}

COPY_TARGETS = {
    "annulus_retest": LOCAL_BOUNDS / "Tobs_support_annulus_retest_2601_NONCLAIM.csv",
    "bridge_rows": LOCAL_BOUNDS / "Tobs_annulus_to_current_owner_bridge_2601_NONCLAIM.csv",
    "next_target": QUEUE / "JR2601_CURRENT_DESCENT_DQ_TAU_PROJECTABILITY_NEXT.csv",
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
    if isinstance(value, (list, tuple, set)):
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
    except Exception as exc:
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC2601_00_2600_handoff",
            "source_path": ROOT / "2600-Y5-R2FR-Tobs-delta-tau-norm-owner-or-boundary-clock-action-clause.md",
            "needles": ["CNR2600_3_vacuum_annulus_zero_candidate", "NEXT2600_0_selected", "VAL2600_OVERALL"],
            "role": "current branch handoff selecting T_obs support-annulus split",
        },
        {
            "source_id": "SRC2601_01_2600_rows",
            "source_path": OUT / "P8_Y5_TOBS_DTAU_2600_CTOBS_SOURCE_ROWS.csv",
            "needles": ["CNR2600_2_Tobs_envelope", "CNR2600_3_vacuum_annulus_zero_candidate"],
            "role": "current branch C_Tobs_tau rows",
        },
        {
            "source_id": "SRC2601_02_1730_doc",
            "source_path": ROOT / "1730-Y5-R2FR-Tobs-support-annulus-split-or-first-norm-source-row.md",
            "needles": ["ASA1730_7_verdict", "TNS1730_0_Z_Tobs_Aext_candidate", "NEXT1730_0_primary", "VAL1730_OVERALL"],
            "role": "prior support-annulus proof attempt",
        },
        {
            "source_id": "SRC2601_03_1730_norm_rows",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1730_TOBS_NORM_SOURCE_ROWS.csv",
            "needles": ["TNS1730_0_Z_Tobs_Aext_candidate", "TNS1730_1_sup_A_Tobs_op", "TNS1730_3_boundary_flux_guard"],
            "role": "prior annulus zero and first stress-envelope source rows",
        },
        {
            "source_id": "SRC2601_04_1731_doc",
            "source_path": ROOT / "1731-Y5-R2FR-Aext-surface-pair-support-certificate-or-boundary-flux-row.md",
            "needles": ["AEX1731_7_verdict", "BFH1731_5_handoff_acceptance", "NEXT1731_0_primary", "VAL1731_OVERALL"],
            "role": "prior A_ext geometry/support and boundary-handoff certificate attempt",
        },
        {
            "source_id": "SRC2601_05_1731_geometry_rows",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1731_AEXT_GEOMETRY_SUPPORT_ROWS.csv",
            "needles": ["AGS1731_0_W_source", "AGS1731_4_support_exclusion"],
            "role": "A_ext geometry/support checklist",
        },
        {
            "source_id": "SRC2601_06_1731_handoff_rows",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1731_BOUNDARY_FLUX_HANDOFF_ROWS.csv",
            "needles": ["BFH1731_0_M_H_ref", "BFH1731_4_PiM_chain_map"],
            "role": "boundary/Hamiltonian handoff source rows",
        },
        {
            "source_id": "SRC2601_07_1732_doc",
            "source_path": ROOT / "1732-Y5-R2FR-boundary-flux-handoff-to-Htau-or-MHref-source-row.md",
            "needles": ["BHA1732_8_verdict", "HMS1732_0_M_H_ref", "NEXT1732_0_primary", "VAL1732_OVERALL"],
            "role": "prior boundary/Hamiltonian handoff attempt",
        },
        {
            "source_id": "SRC2601_08_1732_htau_rows",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1732_HTAU_MHREF_SOURCE_ROWS.csv",
            "needles": ["HMS1732_0_M_H_ref", "HMS1732_2_PiM_H_chain_map"],
            "role": "H_tau and M_H_ref source rows",
        },
        {
            "source_id": "SRC2601_09_1733_doc",
            "source_path": ROOT / "1733-Y5-R2FR-parent-theta-Qtau-current-owner-or-Htau-first-row.md",
            "needles": ["COA1733_7_owner_verdict", "DCL1733_7_verdict", "NEXT1733_0_primary", "VAL1733_OVERALL"],
            "role": "prior Theta_total/Q_tau current-owner attempt",
        },
        {
            "source_id": "SRC2601_10_1733_descent_lemma",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1733_DESCENT_CURRENT_LEMMA.csv",
            "needles": ["DCL1733_0_contract", "DCL1733_7_verdict"],
            "role": "descent-current lemma contract",
        },
        {
            "source_id": "SRC2601_11_1733_theta_rows",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_COMPONENT_ROWS.csv",
            "needles": ["TQC1733_1_X_extra", "TQC1733_6_total_Qtau"],
            "role": "Theta/Q_tau component source rows",
        },
        {
            "source_id": "SRC2601_12_1733_next",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_1733_NEXT_TARGET.csv",
            "needles": ["NEXT1733_0_primary", "current-descent-lemma-Dq-tau-projectability"],
            "role": "prior selected Dq/tau-projectability target",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        missing_needles = path_has_needles(spec["source_path"], spec["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": spec["source_id"],
                    "source_path": spec["source_path"],
                    "exists": spec["source_path"].exists(),
                    "missing_needles": missing_needles,
                    "source_pass": spec["source_path"].exists() and not missing_needles,
                    "role": spec["role"],
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def lineage_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "LIN2601_0_2600",
            "checkpoint": "2600",
            "question": "Can C_Tobs_tau be owned or zeroed?",
            "result": "exact operator law retained; coefficient owner unsigned",
            "status": "HANDOFF_REBASED",
            "next_dependency": "support-annulus zero or first stress norm row",
        },
        {
            "step_id": "LIN2601_1_1730",
            "checkpoint": "1730",
            "question": "Can a vacuum exterior annulus make bulk T_obs vanish?",
            "result": "conditional theorem written; not signed because worldtube, surfaces, support split, boundary flux and units are missing",
            "status": "CONDITIONAL_ROUTE_NOT_CLAIM",
            "next_dependency": "A_ext surface-pair/support certificate",
        },
        {
            "step_id": "LIN2601_2_1731",
            "checkpoint": "1731",
            "question": "Can W_source, S1, S2 and A_ext cap W_source be certified?",
            "result": "geometry/support rows staged; boundary/Hamiltonian handoff becomes the priority",
            "status": "CERTIFICATE_NOT_SIGNED",
            "next_dependency": "boundary/Hamiltonian handoff",
        },
        {
            "step_id": "LIN2601_3_1732",
            "checkpoint": "1732",
            "question": "Can source mass leave bulk stress and reappear as H_tau/M_H_ref boundary charge?",
            "result": "clean GR-like handoff contract written; missing Theta_total, Q_tau, integrability, M_H_ref and PiM chain map",
            "status": "HANDOFF_NOT_SIGNED",
            "next_dependency": "parent Theta_total/Q_tau current owner",
        },
        {
            "step_id": "LIN2601_4_1733",
            "checkpoint": "1733",
            "question": "Can the parent action own Theta_total and Q_tau?",
            "result": "descent-current lemma contract written; q/Dq, tau projectability, vertical silence, boundary/reference and matter descent remain unsigned",
            "status": "CURRENT_OWNER_NOT_SIGNED",
            "next_dependency": "Dq/tau projectability or theta leak row",
        },
        {
            "step_id": "LIN2601_5_current_selection",
            "checkpoint": "2601",
            "question": "What should the current 2600 branch target next?",
            "result": "do not repeat 1730; continue at the sharper Dq/tau-projectability gate",
            "status": "NEXT_ROUTE_SELECTED",
            "next_dependency": "2602 current descent lemma",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def annulus_retest_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "test_id": "ART2601_0_conditional_zero_law",
            "object": "bulk T_obs vacuum-annulus zero",
            "condition": "W_source=closure(supp J_H[tau_obs]); A_ext between fixed S1/S2; A_ext cap W_source empty; T_obs support follows W_source; boundary flux retained elsewhere",
            "current_verdict": "VALID_CONDITIONAL_THEOREM",
            "blocking_gap": "antecedents not parent-signed",
            "zero_claim_allowed": False,
        },
        {
            "test_id": "ART2601_1_no_mass_erasure",
            "object": "boundary/Hamiltonian handoff guard",
            "condition": "mass information excluded from bulk annulus is carried by H_tau, M_H_ref, PiM chain map, B_zero_flux/Delta_symp/R_glue or explicit residuals",
            "current_verdict": "HANDOFF_REQUIRED_NOT_FILLED",
            "blocking_gap": "Theta_total/Q_tau owner and M_H_ref source rows are nonclaim",
            "zero_claim_allowed": False,
        },
        {
            "test_id": "ART2601_2_first_norm_row",
            "object": "sup_A_norm_Tobs_op",
            "condition": "if zero theorem fails, source a finite observed stress envelope with A_ext, norm, Hodge factor and units",
            "current_verdict": "SCHEMA_AVAILABLE_NOT_SCORE_READY",
            "blocking_gap": "A_ext, stress bound, norm pair, observed metric/coframe and units are missing",
            "zero_claim_allowed": False,
        },
        {
            "test_id": "ART2601_3_current_branch_verdict",
            "object": "C_Tobs_tau",
            "condition": "C_Tobs_tau is either theorem-zero on A_ext or finite source-backed with units",
            "current_verdict": "NOT_CLAIM_VALID",
            "blocking_gap": "support-annulus route reduces the problem to q/Dq and tau-projectable current ownership",
            "zero_claim_allowed": False,
        },
    ]
    return [with_stamp({**row, "score_ready": False, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def bridge_rows() -> list[dict[str, Any]]:
    source_paths = [
        OUT / "P8_Y5_TOBS_DTAU_2600_CTOBS_SOURCE_ROWS.csv",
        OUT / "P8_Y5_PARENT_QLOC_1730_TOBS_NORM_SOURCE_ROWS.csv",
        OUT / "P8_Y5_PARENT_QLOC_1731_BOUNDARY_FLUX_HANDOFF_ROWS.csv",
        OUT / "P8_Y5_PARENT_QLOC_1732_HTAU_MHREF_SOURCE_ROWS.csv",
        OUT / "P8_Y5_PARENT_QLOC_1733_DESCENT_CURRENT_LEMMA.csv",
        OUT / "P8_Y5_PARENT_QLOC_1733_THETA_QTAU_COMPONENT_ROWS.csv",
    ]
    rows = [
        {
            "row_id": "BR2601_0_Z_Tobs_Aext_bulk",
            "symbol": "Z_Tobs_Aext_bulk",
            "definition": "theorem-zero flag for ordinary observed stress on the compact exterior annulus",
            "current_status": "CONDITIONAL_ONLY",
            "missing_inputs": "MISSING_PARENT_WORLDTUBE_SELECTOR;MISSING_S1_S2;MISSING_AEXT_SUPPORT_EXCLUSION;MISSING_BOUNDARY_HANDOFF",
            "next_owner": "Dq/tau projectability plus boundary/Hamiltonian current owner",
        },
        {
            "row_id": "BR2601_1_C_Tobs_tau",
            "symbol": "C_Tobs_tau",
            "definition": "moving-tau source-current coefficient inherited from either zero annulus or finite stress envelope",
            "current_status": "LAW_DERIVED_VALUE_OR_ZERO_MISSING",
            "missing_inputs": "MISSING_Z_TOBS_AEXT_OR_SUP_A_TOBS;MISSING_NORM_PAIR;MISSING_HODGE_FACTOR;MISSING_UNITS",
            "next_owner": "annulus/current descent branch",
        },
        {
            "row_id": "BR2601_2_epsilon_boundary_handoff_abs",
            "symbol": "epsilon_boundary_handoff_abs",
            "definition": "absolute residual proving excluded bulk matter stress is carried by boundary/Hamiltonian/source-normalization ledger",
            "current_status": "COMPONENTS_MISSING",
            "missing_inputs": "MISSING_M_H_REF;MISSING_B_ZERO_FLUX;MISSING_DELTA_SYMP;MISSING_R_GLUE;MISSING_PIM_H_CHAIN_MAP",
            "next_owner": "Theta_total/Q_tau current owner",
        },
        {
            "row_id": "BR2601_3_Q_tau_total",
            "symbol": "Q_tau_MTS_total",
            "definition": "parent observed-time Noether charge needed for H_tau and M_H_ref",
            "current_status": "DESCENT_CONTRACT_ONLY",
            "missing_inputs": "MISSING_Q_DQ;MISSING_TAU_PROJECTABILITY;MISSING_VERTICAL_SYMPLECTIC_SILENCE;MISSING_BOUNDARY_REFERENCE;MISSING_MATTER_DESCENT",
            "next_owner": "2602 Dq/tau projectability",
        },
        {
            "row_id": "BR2601_4_theta_Qtau_leak",
            "symbol": "theta_Qtau_leak_vector",
            "definition": "fallback finite residual vector if parent current descent does not close",
            "current_status": "SOURCE_ROW_TO_BUILD_NEXT",
            "missing_inputs": "MISSING_SECTOR_LX_THETAX_QX;MISSING_PROJECTOR_CURRENT;MISSING_BOUNDARY_REFERENCE;MISSING_COUPLING_DESCENT;MISSING_UNITS",
            "next_owner": "2602 theta leak row fallback",
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "source_paths": source_paths,
                "source_paths_exist": all(path.exists() for path in source_paths),
                "numeric_or_theorem_value": "MISSING",
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "runner_id": "RUN2601_0_annulus_zero",
            "target": "Z_Tobs_Aext_bulk=True",
            "verdict": "REFUSE_CLAIM",
            "failure_reasons": "MISSING_W_SOURCE;MISSING_S1_S2;MISSING_AEXT_SUPPORT_EXCLUSION;MISSING_BOUNDARY_HANDOFF",
        },
        {
            "runner_id": "RUN2601_1_stress_envelope",
            "target": "sup_A_norm_Tobs_op scoring row",
            "verdict": "ACCEPT_SCHEMA_REFUSE_SCORING",
            "failure_reasons": "MISSING_A_EXT;MISSING_NORM_TYPE;MISSING_STRESS_BOUND;MISSING_HODGE_FACTOR;MISSING_UNITS",
        },
        {
            "runner_id": "RUN2601_2_boundary_handoff",
            "target": "bulk vacuum preserves source mass through H_tau/M_H_ref",
            "verdict": "BLOCKED_NO_CLAIM",
            "failure_reasons": "MISSING_THETA_TOTAL;MISSING_Q_TAU;MISSING_M_H_REF;MISSING_PIM_CHAIN_MAP;MISSING_BOUNDARY_RESIDUALS",
        },
        {
            "runner_id": "RUN2601_3_current_descent",
            "target": "Theta_total/Q_tau descends through q",
            "verdict": "NEXT_REQUIRED",
            "failure_reasons": "MISSING_Q_DQ;MISSING_TAU_PROJECTABILITY;MISSING_VERTICAL_SYMPLECTIC_SILENCE;MISSING_BOUNDARY_REFERENCE;MISSING_MATTER_DESCENT",
        },
        {
            "runner_id": "RUN2601_4_local_GR_Newton",
            "target": "local GR/Newton recovery",
            "verdict": "BLOCKED_NO_CLAIM",
            "failure_reasons": "NO_BULK_ZERO_OR_STRESS_VALUE;NO_BOUNDARY_HANDOFF;NO_QTAU_OWNER;NO_MHREF;PPN_VECTOR_UNCLEARED",
        },
    ]
    return [with_stamp({**row, "accepted_for_scoring": False, "claim_allowed": False, "valid_for_claim": False}) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "CG2601_0_annulus_route",
            "claim": "vacuum exterior annulus is the clean route",
            "gate_status": "PASS_CONDITIONAL_ONLY",
            "reason": "1730/1731 show the theorem shape is legal if support and boundary handoff are parent-owned",
            "gate_pass": True,
        },
        {
            "gate_id": "CG2601_1_bulk_zero_claim",
            "claim": "T_obs|A_ext=0 for current MTS",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "A_ext support certificate is missing",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2601_2_mass_handoff_claim",
            "claim": "source mass is carried by boundary/Hamiltonian charge",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "Theta_total/Q_tau, M_H_ref and PiM chain map are unsigned",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2601_3_current_owner_claim",
            "claim": "parent current descends through q with projectable tau",
            "gate_status": "NEXT_GATE_REQUIRED",
            "reason": "1733 selected q/Dq and tau projectability as the next real bottleneck",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2601_4_local_GR_claim",
            "claim": "local GR/Newton reduction is derived",
            "gate_status": "BLOCKED_NO_CLAIM",
            "reason": "support, handoff, current descent, M_H_ref and PPN residual vector remain open",
            "gate_pass": False,
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2601_0_no_duplicate_1730",
            "decision": "do not repeat the support-annulus attempt",
            "reason": "1730 already wrote the conditional theorem and the first norm-row fallback",
            "effect": "2601 rebases the result into the current 2600 chain",
        },
        {
            "decision_id": "DEC2601_1_route_alive",
            "decision": "keep vacuum-annulus route alive",
            "reason": "it is the clean GR-like way to have exterior bulk T_obs=0 without erasing source mass",
            "effect": "bulk zero remains conditional rather than rejected",
        },
        {
            "decision_id": "DEC2601_2_real_bottleneck",
            "decision": "move to current descent",
            "reason": "1732/1733 show boundary handoff requires parent Theta_total/Q_tau, which requires q/Dq and tau projectability",
            "effect": "next derivation target is Dq/tau projectability or theta leak row",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2601_0_selected",
            "selection_status": "selected",
            "target_file": "2602-Y5-R2FR-current-descent-lemma-Dq-tau-projectability-or-theta-leak-row.md",
            "target_script": "scripts/Y5_R2FR_current_descent_lemma_Dq_tau_projectability_or_theta_leak_row_2602.py",
            "task": "prove q/Dq and tau projectability clauses needed by the descent-current lemma, or stage nonclaim theta/Qtau leak rows",
            "success_condition": "parent current descent becomes theorem-backed enough to reopen H_tau/M_H_ref handoff without inserting a charge by hand",
            "fallback_condition": "theta_Qtau_leak_vector rows remain finite nonclaim residuals with sector owners, units and source paths",
            "guardrails": "no inserted Q_tau; no EH-only charge shortcut; no clock-product tau owner; no mass erasure from vacuum annulus; no local-GR claim; no GitHub; no formalization-workbench edits",
        }
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target_path in COPY_TARGETS.items():
        source_path = OUTPUTS[copy_id]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2601_{copy_id}",
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
            if row.get("score_ready") is True:
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

    add("VAL2601_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    lineage_steps = {row["step_id"] for row in data["lineage"]}
    add("VAL2601_01_lineage_complete", all(f"LIN2601_{idx}_" in step for idx, step in enumerate(sorted(lineage_steps))), "lineage ledger covers 2600, 1730, 1731, 1732, 1733 and current selection")
    add("VAL2601_02_annulus_retest_complete", len(data["annulus_retest"]) == 4 and all(row["zero_claim_allowed"] is False for row in data["annulus_retest"]), "annulus retest covers conditional zero, mass guard, first norm row and verdict")
    required_bridge_symbols = {"Z_Tobs_Aext_bulk", "C_Tobs_tau", "epsilon_boundary_handoff_abs", "Q_tau_MTS_total", "theta_Qtau_leak_vector"}
    add("VAL2601_03_bridge_rows_complete", required_bridge_symbols.issubset({row["symbol"] for row in data["bridge_rows"]}), "bridge rows connect annulus, handoff, current owner and fallback leak")
    add("VAL2601_04_bridge_sources_exist", all(row["source_paths_exist"] is True for row in data["bridge_rows"]), "bridge rows cite existing local source paths")
    add("VAL2601_05_runner_refuses_claims", all(row["accepted_for_scoring"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]), "runner refuses annulus zero, scoring, boundary handoff and local-GR claims")
    add("VAL2601_06_claim_gates_safe", all(row["claim_allowed"] is False for row in data["claim_gates"]) and any(row["gate_id"] == "CG2601_4_local_GR_claim" and row["gate_status"] == "BLOCKED_NO_CLAIM" for row in data["claim_gates"]), "claim gates block local-GR/Newton promotion")
    add("VAL2601_07_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated rows promote score or claim flags")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2601-Y5-R2FR-Tobs-support-annulus*",
            "*Y5_R2FR_Tobs_support_annulus*2601*",
            "*P8_Y5_TOBS_ANNULUS_REBASE_2601*",
            "*JR2601*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2601_08_no_formalization_artifacts", not formalization_artifacts, "no 2601 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))
    add("VAL2601_09_next_selected", any(row["route_id"] == "NEXT2601_0_selected" and "2602-Y5-R2FR-current-descent-lemma-Dq-tau-projectability" in row["target_file"] for row in data["next"]), "2602 current descent Dq/tau projectability target selected")
    add("VAL2601_10_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2601_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2601_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2601_OVERALL",
        overall,
        "2601 rebases the 1730-1733 support-annulus chain into the current 2600 branch, keeps annulus zero nonclaim, and selects Dq/tau projectability or theta leak row next",
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
        "# 2601 Y5 R2FR Tobs support annulus split or first norm source row",
        "",
        "**Status:** private nonclaim rebase checkpoint. The support-annulus target selected by 2600 was already attempted in the older 1730-1733 chain, so 2601 preserves that evidence instead of rerunning the same gate.",
        "",
        "**Main result:** the clean route is alive but not closed. A source-free exterior annulus would set the bulk `T_obs` piece of `C_Tobs_tau` to zero, but only if `W_source`, `S1/S2`, `A_ext cap W_source`, same-frame `T_obs`, and boundary/Hamiltonian mass handoff are parent-owned. Prior checkpoints show the bottleneck has moved downstream: boundary handoff requires `Theta_total/Q_tau`, and that requires `q/Dq` plus projectable `tau`. No local-GR/Newton claim is made.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Lineage Ledger",
        markdown_table(data["lineage"], ["step_id", "checkpoint", "question", "result", "status", "next_dependency", "valid_for_claim", "claim_allowed"]),
        "",
        "## Annulus Retest",
        markdown_table(data["annulus_retest"], ["test_id", "object", "condition", "current_verdict", "blocking_gap", "zero_claim_allowed", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Current Owner Bridge Rows",
        markdown_table(data["bridge_rows"], ["row_id", "symbol", "definition", "current_status", "missing_inputs", "next_owner", "source_paths", "source_paths_exist", "numeric_or_theorem_value", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Runner Refusal",
        markdown_table(data["runner_refusal"], ["runner_id", "target", "verdict", "failure_reasons", "accepted_for_scoring", "claim_allowed", "valid_for_claim"]),
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
        "This is the useful leap-forward check. The annulus idea is not dead; it is just no longer the deepest unsolved thing. The next real door is whether the parent action lets the observed-time current descend through `q` without smuggling in an EH-only charge. If yes, the boundary handoff can reopen. If not, the honest object is a finite `theta_Qtau_leak_vector`.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_register_rows(),
        "lineage": lineage_ledger_rows(),
        "annulus_retest": annulus_retest_rows(),
        "bridge_rows": bridge_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["lineage_ledger"], data["lineage"])
    write_csv(OUTPUTS["annulus_retest"], data["annulus_retest"])
    write_csv(OUTPUTS["bridge_rows"], data["bridge_rows"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2601_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
