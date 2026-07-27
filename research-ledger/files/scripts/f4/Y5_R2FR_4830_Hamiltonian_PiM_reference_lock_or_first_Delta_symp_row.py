from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"

CHECKPOINT = "4830"
CLAIM_ID = "L-672"
MARKER = "PPC4161_HAMILTONIAN_PIM_REFERENCE_LOCK_OR_FIRST_DELTA_SYMP_ROW_4830"
PACKET_MARKER = "PPC4161_PACKET_HAMILTONIAN_PIM_REFERENCE_LOCK_OR_FIRST_DELTA_SYMP_ROW_4830"
DECISION = "HAMILTONIAN_PIM_REFERENCE_LOCK_UNSIGNED_FIRST_DELTA_SYMP_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4831-Y5-R2FR-boundary-cohomology-projector-silence-or-first-flux-coefficient-row.md"

DOC_PATH = POST / "4830-Y5-R2FR-Hamiltonian-PiM-reference-lock-or-first-Delta-symp-row.md"
FORMAL_PATH = FORMAL / "846-PPC4161-Hamiltonian-PiM-reference-lock-or-first-Delta-symp-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "Hamiltonian_PiM_reference_Delta_symp_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4830_SOURCE_REGISTER.csv"
ZERO_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4830_REFERENCE_LOCK_ZERO_AUDIT.csv"
BOUND_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4830_DELTA_SYMP_BOUND_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4830_DELTA_SYMP_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4830_DELTA_SYMP_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4830_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4830_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4830_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4830_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4830_VALIDATION.csv"

SOURCES = {
    "resume": RESUME_PATH,
    "4829_doc": POST / "4829-Y5-R2FR-parent-worldtube-source-measure-selector-or-first-MHref-row.md",
    "1017_doc": POST / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
    "1018_doc": POST / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
    "hci554": SOURCE_DIR / "P8_Y5_HAMILTONIAN_CHARGE_INTEGRABILITY_REFERENCE_ATTEMPT.csv",
    "hci_fill": SOURCE_DIR / "P8_Y5_HAMILTONIAN_INTEGRABILITY_SOURCE_EQUALITY_FILL_ROWS.csv",
    "parent_lock_666": SOURCE_DIR / "P8_Y5_R10_666_PARENT_LOCK_ATTEMPT.csv",
    "source_hunt_666": SOURCE_DIR / "P8_Y5_R10_666_FB5540_SOURCE_VALUE_HUNT_LEDGER.csv",
    "term_map_667": SOURCE_DIR / "P8_Y5_R10_667_FB5540_TERM_MAP.csv",
    "flux_residual": SOURCE_DIR / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
    "worldtube_runner": SOURCE_DIR / "P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv",
    "mhref_output": SOURCE_DIR / "P8_Y5_R2FR_4829_MHREF_RUNNER_OUTPUT.csv",
    "runner": RUNNER,
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_safe(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_safe(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker not in existing:
        write_text(path, existing.rstrip() + "\n\n" + text.strip() + "\n")


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4830_00_resume", SOURCES["resume"], "4830-Y5-R2FR-Hamiltonian-PiM-reference-lock-or-first-Delta-symp-row.md", "4829 selected this reference-lock target."),
        ("SRC4830_01_4829_doc", SOURCES["4829_doc"], "DEC4829_2_next", "current denominator handoff."),
        ("SRC4830_02_1017_lock", SOURCES["1017_doc"], "HRL1017_3_boundary_flux_zero", "reference-lock law."),
        ("SRC4830_03_1017_schema", SOURCES["1017_doc"], "MHR1017_3_symplectic_boundary_flux", "symplectic boundary row schema."),
        ("SRC4830_04_1018_boundary", SOURCES["1018_doc"], "FSR1018_3_boundary_flux", "sector-owner boundary row."),
        ("SRC4830_05_hci554", SOURCES["hci554"], "HCI554_5_symplectic_boundary_flux", "Hamiltonian integrability obstruction."),
        ("SRC4830_06_hci_fill", SOURCES["hci_fill"], "FB554_0_HPiM_integrability_reference_bound", "FB5540 fill row."),
        ("SRC4830_07_parent_lock_666", SOURCES["parent_lock_666"], "PLA666_3_boundary_class", "parent boundary/reference lock attempt."),
        ("SRC4830_08_source_hunt_666", SOURCES["source_hunt_666"], "SVH666_6_Delta_symp", "Delta_symp source hunt."),
        ("SRC4830_09_term_map_667", SOURCES["term_map_667"], "TM667_2_symplectic_boundary_flux", "FB5540 term map."),
        ("SRC4830_10_flux_residual", SOURCES["flux_residual"], "SMR509_2_Delta_symp", "source-measure residual map."),
        ("SRC4830_11_worldtube_runner", SOURCES["worldtube_runner"], "MR510_2_symplectic_boundary", "worldtube residual runner."),
        ("SRC4830_12_4829_output", SOURCES["mhref_output"], "RUN4829_5_component_selector_smoke_pass", "upstream MHref selector feed."),
        ("SRC4830_13_runner", SOURCES["runner"], "def evaluate_row", "4830 executable runner."),
    ]


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def zero_audit(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("REFZ4830_0_parent_variation", "MTS owns L, Theta, Q_tau and constraints", "delta L = E delta Phi + dTheta; J_tau = Theta(L_tau Phi)-i_tau L; J_tau=dQ_tau+C_tau", "CONTRACT_ONLY", "delta_H_tau_nonintegrable row"),
        ("REFZ4830_1_covariant_phase_space", "Hamiltonian variation has zero curl", "delta H_tau = int_S(delta Q_tau-i_tau Theta)-delta H_ref and delta_1 delta_2 H_tau-delta_2 delta_1 H_tau=0", "NOT_DERIVED", "integrability_curl row"),
        ("REFZ4830_2_reference_lock", "H_ref is branch-selected and derivative-silent", "partial_source,r,t,frame,lambda H_ref = 0 after parent reference selection", "FAIL_OPEN", "H_ref_shift/Delta_ref row"),
        ("REFZ4830_3_boundary_class", "exact/improvement boundary flux is fixed or zero", "int_boundary(delta Q_extra-i_tau Theta_extra)+delta B_class=0", "FAIL_OPEN", "B_zero/symplectic_boundary row"),
        ("REFZ4830_4_Delta_symp", "reference plus symplectic/projector transfer obstruction vanishes", "Delta_symp=0 only if reference lock and projector/boundary silence are parent-owned", "KEY_BLOCKER", "Delta_symp row"),
        ("REFZ4830_5_projector_silence", "Pi_M^H is not carrying hidden boundary/symplectic hair", "delta(Pi_M J_H)=Pi_M delta J_H and projector/domain flux is zero or retained", "NOT_PARENT_SIGNED", "projector_boundary_flux row"),
        ("REFZ4830_6_tau_lock", "same observed time generator is used", "tau_source=tau_charge=tau_clock=tau_readout and delta tau=0", "NOT_PARENT_SIGNED", "tau_mismatch row"),
        ("REFZ4830_7_denominator_guard", "M_H_ref is positive and source-backed", "M_H_ref cannot be bare mass, reference-only one, or orbital GM", "GUARD_PASS_NO_VALUE", "M_H_ref source row"),
        ("REFZ4830_8_anti_circularity", "no GR import, measured GM, reference-only zero, or cancellation", "conditional EH route is a guide, not a proof for MTS", "POLICY_GUARD", "forbidden-source guard"),
    ]
    return [
        {
            "clause_id": clause_id,
            "claim_piece": claim_piece,
            "math_form": math_form,
            "current_result": current_result,
            "finite_fallback": finite_fallback,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for clause_id, claim_piece, math_form, current_result, finite_fallback in rows
    ]


def bound_contract(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("REFC4830_0_zero", "epsilon_HPiM_integrability=0", "all Hamiltonian/reference/boundary/projector/tau clauses parent-signed in one branch", "conditional_only"),
        ("REFC4830_1_direct_Delta_symp", "(Delta_symp+H_ref_shift+B_zero+symplectic_boundary_flux)/M_H_ref", "first reference/boundary source row before promoting M_H_ref", "runner_ready_values_missing"),
        ("REFC4830_2_component_FB5540", "sum FB5540 reference-lock components/M_H_ref", "integrability curl + reference curl + boundary flux + projector + tau + nonEH envelope", "runner_ready_values_missing"),
        ("REFC4830_3_BY5", "BY5_reference_lock_feed=tau_BY5_ref epsilon_HPiM_integrability", "feeds reference-lock leakage into BY5/source-normalization branch", "runner_ready_values_missing"),
    ]
    return [
        {
            "contract_id": contract_id,
            "quantity": quantity,
            "definition": definition,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for contract_id, quantity, definition, status in rows
    ]


def runner_inputs(timestamp: str) -> list[dict[str, Any]]:
    doc_1017 = str(SOURCES["1017_doc"])
    source_hunt = str(SOURCES["source_hunt_666"])
    base = {
        "source_signed": "true",
        "units_signed": "true",
        "same_branch_signed": "true",
        "no_cancellation_guard": "true",
    }
    zero = {
        "parent_L_theta_Q_signed": "true",
        "covariant_phase_space_identity_signed": "true",
        "Hamiltonian_PiM_map_signed": "true",
        "integrability_curl_zero_signed": "true",
        "reference_superselection_signed": "true",
        "H_ref_derivative_silent_signed": "true",
        "boundary_class_exact_signed": "true",
        "symplectic_boundary_flux_zero_signed": "true",
        "projector_silence_signed": "true",
        "tau_lock_signed": "true",
        "M_H_ref_positive_signed": "true",
        "no_readout_mask_signed": "true",
        "no_measured_GM_absorption_signed": "true",
    }
    direct = {
        "M_H_ref_abs": "2.0",
        "tau_BY5_ref_abs": "2.0",
        "Delta_symp_abs": "0.03",
        "H_ref_shift_abs": "0.01",
        "B_zero_flux_abs": "0.02",
        "symplectic_boundary_flux_abs": "0.04",
    }
    component = {
        **direct,
        "delta_H_tau_nonintegrable_abs": "0.02",
        "reference_curl_abs": "0.01",
        "projector_boundary_flux_abs": "0.02",
        "tau_mismatch_abs": "0.02",
        "Delta_PiM_abs": "0.01",
        "Delta_nonEH_abs": "0.02",
    }
    return [
        {
            "row_id": "RUN4830_0_live_reference_zero_missing",
            "route_type": "reference_zero",
            "route": "live Hamiltonian/PiM reference-lock zero audit",
            "source_path": doc_1017,
            "equation_ref": "HPT1017_5_verdict",
            "notes": "current MTS has unsigned L/Theta/Q, reference, boundary, projector, tau, and denominator clauses",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4830_1_conditional_reference_zero_pass",
            "route_type": "reference_zero",
            "route": "conditional parent-signed reference-lock zero",
            "source_path": doc_1017,
            "equation_ref": "HRL1017_6_FB5540_zero_law",
            "notes": "nonclaim theorem-shape smoke row",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4830_2_forbidden_GR_import",
            "route_type": "reference_zero",
            "route": "forbidden GR import as MTS proof",
            "source_path": doc_1017,
            "equation_ref": "HPT1017_0_EH_reference",
            "notes": "GR_IMPORT cannot replace the missing MTS symplectic charge derivation",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4830_3_live_Delta_symp_missing",
            "route_type": "direct_Delta_symp",
            "route": "live Delta_symp/H_ref boundary row missing",
            "source_path": source_hunt,
            "equation_ref": "SVH666_6_Delta_symp",
            "notes": "schema exists but no source-backed Delta_symp/H_ref/B_zero/symplectic values",
            **base,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4830_4_direct_Delta_symp_smoke_pass",
            "route_type": "direct_Delta_symp",
            "route": "direct finite Delta_symp/H_ref smoke",
            "source_path": source_hunt,
            "equation_ref": "SVH666_6_Delta_symp",
            "notes": "nonclaim arithmetic smoke for first reference-boundary row",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4830_5_component_FB5540_smoke_pass",
            "route_type": "component_FB5540",
            "route": "component finite FB5540 reference-lock smoke",
            "source_path": str(SOURCES["term_map_667"]),
            "equation_ref": "TM667_2_symplectic_boundary_flux",
            "notes": "nonclaim arithmetic smoke for full retained Hamiltonian/PiM reference-lock envelope",
            **base,
            **component,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4830_6_forbidden_reference_only_zero",
            "route_type": "direct_Delta_symp",
            "route": "forbidden reference-only zero",
            "source_path": doc_1017,
            "equation_ref": "HPT1017_2_reference_superselection",
            "notes": "REFERENCE_ONLY_ZERO cannot close Delta_ref or Delta_symp",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4830_7_forbidden_measured_GM_source",
            "route_type": "component_FB5540",
            "route": "forbidden measured GM denominator",
            "source_path": doc_1017,
            "equation_ref": "DEC1017_1_no_MHref_shortcut",
            "notes": "MEASURED_GM_AS_SOURCE cannot normalize the source-charge theorem",
            **base,
            **component,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4830_8_forbidden_cancellation",
            "route_type": "component_FB5540",
            "route": "forbidden cancellation of unknown reference terms",
            "source_path": doc_1017,
            "equation_ref": "MHR1017_5_FB5540_total",
            "notes": "CANCEL_UNKNOWN_COMPONENTS cannot prove reference-lock zero",
            **base,
            **component,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4830_9_forbidden_bare_mass_denominator",
            "route_type": "component_FB5540",
            "route": "forbidden bare mass denominator",
            "source_path": doc_1017,
            "equation_ref": "HPT1017_4_denominator_guard",
            "notes": "BARE_MASS_DENOMINATOR cannot replace M_H_ref",
            **base,
            **component,
            "timestamp_utc": timestamp,
        },
    ]


def decisions(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DEC4830_0_reference_lock", "Hamiltonian/PiM reference lock is still unsigned for current MTS.", "The EH route is a valid template, but MTS still needs its own L/Theta/Q, fixed H_ref, boundary class, projector silence and tau lock.", "keep M_H_ref and local-GR promotion blocked", False),
        ("DEC4830_1_Delta_symp", "Delta_symp is now a first-class source-normalization residual, not a note in the margin.", "Reference shift, exact boundary flux, symplectic leakage and projector boundary hair can all move the source charge.", "source or zero each numerator before scoring local tests", False),
        ("DEC4830_2_next", "The next hard target is boundary cohomology/projector silence.", "Delta_symp cannot close until boundary exactness/no-hair and PiM boundary orthogonality are parent-owned or bounded.", NEXT_TARGET, False),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "because": because,
            "next_action": next_action,
            "valid_for_claim": valid_for_claim,
            "timestamp_utc": timestamp,
        }
        for decision_id, decision, because, next_action, valid_for_claim in rows
    ]


def claim_gates(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CG4830_0_runner_installed", "Hamiltonian/PiM reference-lock gate is executable", True, "runner computes exact-zero, direct Delta_symp, and component FB5540 routes", False),
        ("CG4830_1_reference_zero", "reference-lock components are theorem-zero", False, "live parent variation/reference/boundary/projector/tau clauses remain unsigned", False),
        ("CG4830_2_delta_symp_claim", "Delta_symp/H_ref/B_zero row is source-backed for current MTS", False, "no live numeric/theorem-zero row with M_H_ref, units, and source path exists", False),
        ("CG4830_3_residual_route", "finite reference-lock residual route is staged", True, "smoke rows compute epsilon_ref_boundary and epsilon_HPiM without cancellation", False),
        ("CG4830_4_no_shortcuts", "GR import, reference-only zero, measured GM, bare mass and cancellation fail closed", True, "forbidden rows return FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", False),
        ("CG4830_5_no_local_GR_claim", "local GR/Newton/R10/PPN claims remain blocked", True, "no runner row allows a claim", False),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "claim_allowed": claim_allowed,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, claim, gate_pass, reason, claim_allowed in rows
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "decision": DECISION,
            "claim_id": CLAIM_ID,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "derive boundary cohomology/projector silence or stage first source-backed flux coefficients for Delta_symp",
            "include": "B_class exactness, B_zero_flux, no vector/tensor boundary hair, projector boundary orthogonality, PiM silence, source paths, units, no-cancellation validation",
            "exclude": "GR import, reference-only zero, measured GM denominator, bare mass denominator, cancellation, local-GR/Newton/R10/PPN claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def run_runner() -> list[dict[str, str]]:
    subprocess.run([sys.executable, str(RUNNER), str(RUNNER_INPUT), str(RUNNER_OUTPUT)], check=True)
    return read_csv(RUNNER_OUTPUT)


def validate(timestamp: str, outputs: list[dict[str, str]], sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {row["row_id"]: row for row in outputs}
    expected = {
        "RUN4830_0_live_reference_zero_missing": "BLOCKED_REFERENCE_LOCK_ZERO_CLAUSES",
        "RUN4830_1_conditional_reference_zero_pass": "REFERENCE_LOCK_ZERO_PASS_NONCLAIM",
        "RUN4830_2_forbidden_GR_import": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4830_3_live_Delta_symp_missing": "BLOCKED_DIRECT_DELTA_SYMP_INPUTS",
        "RUN4830_4_direct_Delta_symp_smoke_pass": "DIRECT_DELTA_SYMP_ROW_PASS_NONCLAIM",
        "RUN4830_5_component_FB5540_smoke_pass": "COMPONENT_FB5540_ROW_PASS_NONCLAIM",
        "RUN4830_6_forbidden_reference_only_zero": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4830_7_forbidden_measured_GM_source": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4830_8_forbidden_cancellation": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4830_9_forbidden_bare_mass_denominator": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
    }
    direct = by_id.get("RUN4830_4_direct_Delta_symp_smoke_pass", {})
    component = by_id.get("RUN4830_5_component_FB5540_smoke_pass", {})
    checks = [
        ("VAL4830_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        ("VAL4830_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ("VAL4830_02_output_count", len(outputs) == len(expected), "all runner rows emitted"),
        ("VAL4830_03_expected_statuses", all(by_id.get(row_id, {}).get("runner_status") == status for row_id, status in expected.items()), "runner statuses match expected pass/block/fail modes"),
        ("VAL4830_04_live_zero_blocked", by_id["RUN4830_0_live_reference_zero_missing"]["runner_status"] == "BLOCKED_REFERENCE_LOCK_ZERO_CLAUSES", "live reference-lock zero remains blocked"),
        ("VAL4830_05_live_delta_symp_blocked", by_id["RUN4830_3_live_Delta_symp_missing"]["runner_status"] == "BLOCKED_DIRECT_DELTA_SYMP_INPUTS", "live Delta_symp row remains missing"),
        ("VAL4830_06_direct_smoke_pass", direct.get("epsilon_ref_boundary_abs") == "5.000000000000000e-02" and direct.get("BY5_reference_lock_feed_abs") == "1.000000000000000e-01", "direct Delta_symp smoke computes reference-boundary residual"),
        ("VAL4830_07_component_smoke_pass", component.get("epsilon_HPiM_integrability_abs") == "1.000000000000000e-01" and component.get("BY5_reference_lock_feed_abs") == "2.000000000000000e-01", "component FB5540 smoke computes full retained residual"),
        ("VAL4830_08_forbidden_routes_fail", all(by_id[row_id]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE" for row_id in ("RUN4830_2_forbidden_GR_import", "RUN4830_6_forbidden_reference_only_zero", "RUN4830_7_forbidden_measured_GM_source", "RUN4830_8_forbidden_cancellation", "RUN4830_9_forbidden_bare_mass_denominator")), "forbidden shortcuts fail closed"),
        ("VAL4830_09_no_claim_allowed", not any(str(row.get("claim_allowed", "")).lower() == "true" for row in outputs), "no runner row allows a claim"),
        ("VAL4830_10_runner_compiles", True, "runner compiled before execution"),
        ("VAL4830_11_next_target_written", NEXT_TARGET_CSV.exists(), "next target CSV written"),
    ]
    return [
        {
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for validation_id, passed, detail in checks
    ]


def write_docs(timestamp: str, sources: list[dict[str, Any]], audit: list[dict[str, Any]], contract: list[dict[str, Any]], outputs: list[dict[str, str]], decision_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    doc = f"""# 4830 Y5 R2FR Hamiltonian PiM reference lock or first Delta symp row

**Status:** 4830 makes the Hamiltonian/PiM reference lock executable. The exact path needs parent-owned `L/Theta/Q_tau`, an integrable `H_tau`, derivative-silent `H_ref`, zero or retained boundary/symplectic/projector flux, one time generator, and a positive source-backed `M_H_ref`. Current MTS has not signed those clauses.

**Decision:** `{DECISION}`.

**Claim ceiling:** no local-GR, Newtonian, R10, PPN, stable `M_H_ref`, source-charge, measured-GM, or reference-lock claim is allowed from 4830.

## Core equations

```text
delta H_tau[S] = int_S(delta Q_tau - i_tau Theta_total) - delta H_ref[S]
epsilon_ref_boundary = (|Delta_symp|+|H_ref_shift|+|B_zero_flux|+|symplectic_boundary_flux|)/M_H_ref
epsilon_HPiM_integrability = (|delta_H_tau_nonintegrable|+|reference_curl|+|H_ref_shift|
                              +|B_zero_flux|+|Delta_symp|+|symplectic_boundary_flux|
                              +|projector_boundary_flux|+|tau_mismatch|+|Delta_PiM|
                              +|Delta_nonEH|)/M_H_ref
BY5_reference_lock_feed = tau_BY5_ref epsilon_HPiM_integrability
```

## Source register

{md_table(sources, ["source_id", "exists", "needle_found", "role"])}

## Reference-lock zero audit

{md_table(audit, ["clause_id", "claim_piece", "current_result", "finite_fallback"])}

## Delta-symp contract

{md_table(contract, ["contract_id", "quantity", "definition", "status"])}

## Runner output

{md_table(outputs, ["row_id", "runner_status", "Delta_symp_over_MH_abs", "Delta_ref_over_MH_abs", "epsilon_ref_boundary_abs", "epsilon_HPiM_integrability_abs", "BY5_reference_lock_feed_abs", "missing_for_claim"])}

## Decision ledger

{md_table(decision_rows, ["decision_id", "decision", "because", "next_action"])}

## Validation

{md_table(validation, ["validation_id", "result", "detail"])}

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    formal = f"""# 846 PPC4161 Hamiltonian PiM reference lock or first Delta symp row

Checkpoint: `{DOC_PATH}`

4830 turns `Delta_symp`, `H_ref_shift`, `B_zero_flux`, and symplectic boundary leakage into a visible source-normalization gate. The live branch remains nonclaim because the parent Hamiltonian/PiM reference-lock clauses are not signed for current MTS.

Decision: `{DECISION}`

Runner: `{RUNNER}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_claims(timestamp: str) -> None:
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "Hamiltonian_PiM_reference_lock_or_first_Delta_symp_row",
        "current_evidence": "4830 converts the Hamiltonian/PiM reference-lock bottleneck into an executable zero-or-finite Delta_symp/H_ref/B_zero/symplectic-boundary runner; live zero and source-backed values remain missing.",
        "status": "Hamiltonian_PiM_reference_Delta_symp_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "MTS L/Theta/Q, H_tau integrability, H_ref derivative silence, boundary class, projector silence, tau lock, and M_H_ref remain unsigned or missing",
        "sector": "local_gr_Newton_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smoke rows pass but live Delta_symp/reference-lock rows are not source-backed",
        "title": "Hamiltonian PiM reference lock or first Delta symp row",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    if CLAIMS_PATH.exists():
        rows = read_csv(CLAIMS_PATH)
        if any(existing.get("claim_id") == CLAIM_ID for existing in rows):
            return
        fields = list(rows[0].keys()) if rows else list(row.keys())
        for key in row:
            if key not in fields:
                fields.append(key)
        rows.append(row)
        with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(rows)
    else:
        write_csv(CLAIMS_PATH, [row])


def update_spine_and_packet(timestamp: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""## PPC4161 4830 Hamiltonian/PiM reference-lock runner

`{MARKER}`. The source-coupling chain now has a visible reference/boundary lock: either the parent action signs `L/Theta/Q_tau`, integrable `H_tau`, fixed `H_ref`, boundary/projector silence and tau lock, or `Delta_symp`, `H_ref_shift`, `B_zero_flux` and symplectic boundary leakage are retained as `epsilon_HPiM_integrability`. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4830 Hamiltonian/PiM reference-lock or first Delta-symp row

`{MARKER}` prevents the `M_H_ref` denominator from borrowing a quiet reference or boundary flux. Conditional zero requires parent-owned Hamiltonian charge and boundary/reference locks; finite rows compute `epsilon_ref_boundary`, `epsilon_HPiM_integrability`, and `BY5` feed. GR import, reference-only zero, measured GM, bare mass and cancellation fail closed. Next: `{NEXT_TARGET}`.""",
    )


def update_resume(timestamp: str) -> None:
    text = f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4830-Y5-R2FR-Hamiltonian-PiM-reference-lock-or-first-Delta-symp-row.md`
Marker: `{MARKER}`

## Where we are

4830 made the Hamiltonian/PiM reference-lock gate executable:

```text
delta H_tau[S] = int_S(delta Q_tau - i_tau Theta_total) - delta H_ref[S]
epsilon_ref_boundary = (|Delta_symp|+|H_ref_shift|+|B_zero_flux|+|symplectic_boundary_flux|)/M_H_ref
epsilon_HPiM_integrability = sum(|reference-lock/source-charge residuals|)/M_H_ref
```

## Live blockers

- `L_MTS`, `Theta_MTS`, `Q_tau`, and the Hamiltonian integrability curl are not parent-signed for all retained sectors.
- `H_ref` is not yet branch-selected and derivative-silent.
- `Delta_symp`, `B_zero_flux`, symplectic boundary flux, projector boundary flux, and tau mismatch have no source-backed live rows.
- GR import, measured/orbital `GM`, bare mass, reference-only zero, and cancellation-only routes are explicitly forbidden.

## Next target

`{NEXT_TARGET}`
"""
    write_text(RESUME_PATH, text)


def main() -> int:
    timestamp = now()
    py_compile.compile(str(RUNNER), doraise=True)
    sources = source_register(timestamp)
    audit = zero_audit(timestamp)
    contract = bound_contract(timestamp)
    inputs = runner_inputs(timestamp)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_AUDIT, audit)
    write_csv(BOUND_CONTRACT, contract)
    write_csv(RUNNER_INPUT, inputs)
    outputs = run_runner()
    decision_rows = decisions(timestamp)
    gate_rows = claim_gates(timestamp)
    write_csv(DECISION_CSV, decision_rows)
    write_csv(CLAIM_GATES, gate_rows)
    write_csv(STATUS_CSV, status_rows(timestamp))
    write_csv(NEXT_TARGET_CSV, next_target_rows(timestamp))
    validation = validate(timestamp, outputs, sources)
    write_csv(VALIDATION_CSV, validation)
    write_docs(timestamp, sources, audit, contract, outputs, decision_rows, validation)
    update_claims(timestamp)
    update_spine_and_packet(timestamp)
    update_resume(timestamp)
    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        print(f"4830 validation failed: {failed}", file=sys.stderr)
        return 1
    print(f"{MARKER} complete")
    print(f"doc={DOC_PATH}")
    print(f"runner_output={RUNNER_OUTPUT}")
    print(f"validation={VALIDATION_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
