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

CHECKPOINT = "4829"
CLAIM_ID = "L-671"
MARKER = "PPC4161_PARENT_WORLDTUBE_SOURCE_MEASURE_SELECTOR_OR_FIRST_MHREF_ROW_4829"
PACKET_MARKER = "PPC4161_PACKET_PARENT_WORLDTUBE_SOURCE_MEASURE_SELECTOR_OR_FIRST_MHREF_ROW_4829"
DECISION = "PARENT_WORLDTUBE_SOURCE_MEASURE_UNSIGNED_FIRST_MHREF_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4830-Y5-R2FR-Hamiltonian-PiM-reference-lock-or-first-Delta-symp-row.md"

DOC_PATH = POST / "4829-Y5-R2FR-parent-worldtube-source-measure-selector-or-first-MHref-row.md"
FORMAL_PATH = FORMAL / "845-PPC4161-parent-worldtube-source-measure-selector-or-first-MHref-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "parent_worldtube_MHref_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4829_SOURCE_REGISTER.csv"
SELECTOR_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4829_SELECTOR_ZERO_AUDIT.csv"
MHREF_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4829_MHREF_BOUND_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4829_MHREF_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4829_MHREF_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4829_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4829_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4829_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4829_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4829_VALIDATION.csv"

SOURCES = {
    "resume": RESUME_PATH,
    "4828_doc": POST / "4828-Y5-R2FR-topological-Hilbert-equality-or-first-Req-Bzero-row.md",
    "1016_doc": POST / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
    "1017_doc": POST / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
    "worldtube_glue": SOURCE_DIR / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
    "worldtube_measure": SOURCE_DIR / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
    "flux_residual": SOURCE_DIR / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
    "worldtube_runner": SOURCE_DIR / "P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv",
    "req_bzero_output": SOURCE_DIR / "P8_Y5_R2FR_4828_REQ_BZERO_RUNNER_OUTPUT.csv",
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
        ("SRC4829_00_resume", SOURCES["resume"], "4829-Y5-R2FR-parent-worldtube-source-measure-selector-or-first-MHref-row.md", "4828 selected this source-measure target."),
        ("SRC4829_01_4828_doc", SOURCES["4828_doc"], "Next target: `4829-Y5-R2FR-parent-worldtube-source-measure-selector-or-first-MHref-row.md`", "current same-object handoff."),
        ("SRC4829_02_1016_selector", SOURCES["1016_doc"], "PSC1016_5_dressed_source_charge", "selector/source-measure clause."),
        ("SRC4829_03_1016_first_input", SOURCES["1016_doc"], "FIS1016_0_M_H_ref", "first M_H_ref input schema."),
        ("SRC4829_04_1017_denominator", SOURCES["1017_doc"], "MHR1017_0_M_H_ref_denominator", "denominator row schema."),
        ("SRC4829_05_1017_guard", SOURCES["1017_doc"], "HPT1017_4_denominator_guard", "no bare/orbital mass guard."),
        ("SRC4829_06_worldtube_glue", SOURCES["worldtube_glue"], "W504_4_worldtube_source_measure_glue", "worldtube/exterior charge glue."),
        ("SRC4829_07_worldtube_measure", SOURCES["worldtube_measure"], "T510_1_worldtube_source_measure", "dressed source measure correction."),
        ("SRC4829_08_flux_residual", SOURCES["flux_residual"], "SMR509_2_Delta_symp", "symplectic/reference residual."),
        ("SRC4829_09_worldtube_runner", SOURCES["worldtube_runner"], "MR510_2_symplectic_boundary", "worldtube residual runner."),
        ("SRC4829_10_4828_output", SOURCES["req_bzero_output"], "RUN4828_4_direct_Req_Bzero_smoke_pass", "upstream equality runner feed."),
        ("SRC4829_11_runner", SOURCES["runner"], "def evaluate_row", "4829 executable runner."),
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


def selector_audit(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("MHZ4829_0_parent_action", "parent action owns the source current and observed time flow", "delta L gives J_H[tau], theta, Q_tau, and the same tau before readout", "CONTRACT_WRITTEN_NOT_PARENT_SIGNED", "parent action covariant source row"),
        ("MHZ4829_1_worldtube_selector", "compact source worldtube is selected by Hilbert support", "W_source := closure(supp J_H[tau]) with S_outer linking W_source", "FORMAL_SELECTOR_ONLY", "Delta_worldtube_domain row"),
        ("MHZ4829_2_same_frame_measure", "source, charge, clock, and readout share one observed frame", "tau_source=tau_charge=tau_clock=tau_readout and e_obs is fixed once", "FAIL_OPEN", "Delta_frame_source row"),
        ("MHZ4829_3_Htau_integrable", "Hamiltonian variation is integrable on the selected branch", "delta H_tau = integral_S(delta Q_tau - i_tau theta) has zero field-space curl", "NOT_DERIVED", "delta_H_tau_nonintegrable row"),
        ("MHZ4829_4_Href_lock", "reference subtraction cannot absorb source calibration", "H_ref is branch-selected and derivative-silent", "NOT_DERIVED", "H_ref_shift row"),
        ("MHZ4829_5_MHref_denominator", "positive source denominator is parent-owned", "M_H_ref := H_tau[S_outer] - H_ref > 0, not bare mass or orbital GM", "KEY_BLOCKER", "first M_H_ref row"),
        ("MHZ4829_6_PiM_Hamiltonian_map", "Pi_M is the Hamiltonian mass-charge map", "Pi_M J_H matches the same Q_tau source channel", "NOT_PARENT_SIGNED", "PiM/Hamiltonian map certificate"),
        ("MHZ4829_7_boundary_reference_lock", "exact/boundary/symplectic terms are zero or retained", "B_zero_flux, Delta_symp and H_ref_shift are owned before residual scoring", "FAIL_OPEN", "boundary/reference residual rows"),
        ("MHZ4829_8_coupling_descent", "matter coupling descends without hidden readout coefficients", "S_matter = Sbar[q(Phi), Psi, theta] with no representative leakage", "NOT_SIGNED", "coupling_residual row"),
        ("MHZ4829_9_anti_circularity", "no bare mass, measured GM, reference-only zero, or cancellation", "denominator and numerator must be source-backed before claims", "POLICY_GUARD", "forbidden-source guard"),
    ]
    return [
        {
            "clause_id": clause_id,
            "claim_piece": claim_piece,
            "math_form": math_form,
            "current_result": current_result,
            "finite_fallback": fallback,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for clause_id, claim_piece, math_form, current_result, fallback in rows
    ]


def mhref_contract(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("MHC4829_0_selector_zero", "epsilon_selector_Meff=0", "all selector, integrability, reference, frame, coupling and PiM clauses parent-signed in one branch", "conditional_only"),
        ("MHC4829_1_direct_MHref", "M_H_ref=H_tau[S_outer]-H_ref", "first source-backed denominator row with units, reference rule and source path", "runner_ready_values_missing"),
        ("MHC4829_2_component_selector", "epsilon_selector_Meff=sum retained source-selector residuals/M_H_ref", "B_zero+Delta_symp+H_ref+worldtube+frame+coupling+R_eq+I_commutator+T_PiM+A_parent envelope", "runner_ready_values_missing"),
        ("MHC4829_3_BY5", "BY5_selector_feed=tau_BY5_MHref epsilon_selector_Meff", "feeds source-measure leakage into the same BY5/source-normalization branch", "runner_ready_values_missing"),
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
    doc_1016 = str(SOURCES["1016_doc"])
    doc_1017 = str(SOURCES["1017_doc"])
    base = {
        "source_signed": "true",
        "units_signed": "true",
        "same_branch_signed": "true",
        "no_cancellation_guard": "true",
    }
    zero = {
        "parent_action_covariant_signed": "true",
        "observed_tau_signed": "true",
        "same_frame_source_measure_signed": "true",
        "compact_worldtube_support_signed": "true",
        "linking_surfaces_fixed_signed": "true",
        "Htau_integrability_signed": "true",
        "H_ref_fixed_signed": "true",
        "M_H_ref_positive_signed": "true",
        "PiM_Hamiltonian_map_signed": "true",
        "boundary_reference_lock_signed": "true",
        "coupling_descent_silence_signed": "true",
        "no_readout_mask_signed": "true",
        "no_measured_GM_absorption_signed": "true",
    }
    component_values = {
        "M_H_ref_abs": "2.0",
        "tau_BY5_MHref_abs": "2.0",
        "B_zero_flux_abs": "0.02",
        "Delta_symp_abs": "0.03",
        "H_ref_shift_abs": "0.01",
        "Delta_worldtube_domain_abs": "0.02",
        "Delta_frame_source_abs": "0.01",
        "coupling_residual_abs": "0.01",
        "R_eq_integral_abs": "0.02",
        "I_commutator_abs": "0.03",
        "T_PiM_norm_abs": "0.02",
        "A_parent_abs": "0.01",
    }
    return [
        {
            "row_id": "RUN4829_0_live_selector_zero_missing",
            "route_type": "selector_zero",
            "route": "live parent selector/MHref zero audit",
            "source_path": doc_1016,
            "equation_ref": "PSC1016_9_verdict",
            "notes": "current MTS has unsigned parent action, tau, worldtube, integrability, reference, PiM and coupling clauses",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4829_1_conditional_selector_zero_pass",
            "route_type": "selector_zero",
            "route": "conditional parent-signed selector zero",
            "source_path": doc_1016,
            "equation_ref": "PST1016_1_source_measure_lemma",
            "notes": "nonclaim theorem-shape smoke row",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4829_2_forbidden_bare_mass_shortcut",
            "route_type": "selector_zero",
            "route": "forbidden bare mass denominator",
            "source_path": doc_1017,
            "equation_ref": "HPT1017_4_denominator_guard",
            "notes": "BARE_MASS_SHORTCUT cannot replace the parent Hamiltonian source charge",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4829_3_live_MHref_missing",
            "route_type": "direct_MHref",
            "route": "live M_H_ref denominator row missing",
            "source_path": doc_1017,
            "equation_ref": "MHR1017_0_M_H_ref_denominator",
            "notes": "schema exists but no source-backed H_tau/H_ref/M_H_ref values",
            **base,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4829_4_direct_MHref_smoke_pass",
            "route_type": "direct_MHref",
            "route": "direct finite M_H_ref smoke",
            "source_path": doc_1017,
            "equation_ref": "MHR1017_0_M_H_ref_denominator",
            "H_tau_outer_abs": "3.0",
            "H_ref_abs": "1.0",
            "M_H_ref_abs": "2.0",
            "reference_tolerance_abs": "1e-12",
            "notes": "nonclaim arithmetic smoke for denominator consistency",
            **base,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4829_5_component_selector_smoke_pass",
            "route_type": "component_selector",
            "route": "component finite selector residual smoke",
            "source_path": doc_1017,
            "equation_ref": "MHR1017_5_FB5540_total",
            "notes": "nonclaim arithmetic smoke for retained source-selector residuals",
            **base,
            **component_values,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4829_6_forbidden_reference_only_zero",
            "route_type": "direct_MHref",
            "route": "forbidden reference-only zero",
            "source_path": doc_1017,
            "equation_ref": "HPT1017_2_reference_superselection",
            "H_tau_outer_abs": "1.0",
            "H_ref_abs": "0.0",
            "M_H_ref_abs": "1.0",
            "reference_tolerance_abs": "1e-12",
            "notes": "REFERENCE_ONLY_ZERO cannot close the source denominator",
            **base,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4829_7_forbidden_measured_GM_source",
            "route_type": "component_selector",
            "route": "forbidden measured GM as source",
            "source_path": doc_1017,
            "equation_ref": "DEC1017_1_no_MHref_shortcut",
            "notes": "MEASURED_GM_AS_SOURCE cannot normalize the theorem it is supposed to derive",
            **base,
            **component_values,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4829_8_forbidden_cancellation",
            "route_type": "component_selector",
            "route": "forbidden cancellation of unknown selector components",
            "source_path": doc_1017,
            "equation_ref": "MHR1017_5_FB5540_total",
            "notes": "CANCEL_UNKNOWN_COMPONENTS cannot prove a selector zero",
            **base,
            **component_values,
            "timestamp_utc": timestamp,
        },
    ]


def decisions(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DEC4829_0_selector", "The parent worldtube/source-measure selector is still unsigned.", "The exact route is mathematically well-formed but needs parent ownership of J_H, tau, H_tau, H_ref, Pi_M^H and coupling descent.", "keep local-GR/Newton claims blocked until signed or bounded", False),
        ("DEC4829_1_MHref", "M_H_ref is now the required denominator row, not a hidden normalization.", "R_eq/B_zero/I_commutator/T_PiM rows cannot be scored against measured GM, bare mass, or reference-only one.", "source H_tau/H_ref/M_H_ref or carry selector residuals", False),
        ("DEC4829_2_next", "The next hard target is Hamiltonian PiM reference/boundary lock.", "M_H_ref depends on integrability, reference subtraction, and Delta_symp/B_zero boundary ownership.", NEXT_TARGET, False),
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
        ("CG4829_0_runner_installed", "parent worldtube/MHref gate is executable", True, "runner computes selector zero, direct denominator, and component residual routes", False),
        ("CG4829_1_selector_zero", "parent selector and source measure are theorem-zero", False, "live parent action/integrability/reference/frame/coupling clauses remain unsigned", False),
        ("CG4829_2_MHref_claim", "M_H_ref is source-backed for current MTS", False, "no live H_tau/H_ref/M_H_ref row with source path and units exists", False),
        ("CG4829_3_residual_route", "finite selector residual route is staged", True, "component smoke computes epsilon_selector_Meff and BY5 feed without cancellation", False),
        ("CG4829_4_no_shortcuts", "bare mass, measured GM, reference-only zero and cancellation fail closed", True, "forbidden rows return FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", False),
        ("CG4829_5_no_local_GR_claim", "local GR/Newton/R10/PPN claims remain blocked", True, "no runner row allows a claim", False),
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
            "objective": "derive Hamiltonian/PiM reference lock or stage first Delta_symp/H_ref boundary row before promoting M_H_ref",
            "include": "delta_H_tau curl, H_ref shift, B_zero_flux, Delta_symp, tau lock, M_H_ref source path, no-cancellation validation",
            "exclude": "bare mass denominator, orbital GM source, reference-only zero, cancellation, local-GR/Newton/R10/PPN claim",
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
        "RUN4829_0_live_selector_zero_missing": "BLOCKED_PARENT_SELECTOR_MHREF_ZERO_CLAUSES",
        "RUN4829_1_conditional_selector_zero_pass": "PARENT_SELECTOR_MHREF_ZERO_PASS_NONCLAIM",
        "RUN4829_2_forbidden_bare_mass_shortcut": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4829_3_live_MHref_missing": "BLOCKED_DIRECT_MHREF_INPUTS",
        "RUN4829_4_direct_MHref_smoke_pass": "DIRECT_MHREF_ROW_PASS_NONCLAIM",
        "RUN4829_5_component_selector_smoke_pass": "COMPONENT_SELECTOR_ROW_PASS_NONCLAIM",
        "RUN4829_6_forbidden_reference_only_zero": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4829_7_forbidden_measured_GM_source": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4829_8_forbidden_cancellation": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
    }
    component = by_id.get("RUN4829_5_component_selector_smoke_pass", {})
    checks = [
        ("VAL4829_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        ("VAL4829_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ("VAL4829_02_output_count", len(outputs) == len(expected), "all runner rows emitted"),
        ("VAL4829_03_expected_statuses", all(by_id.get(row_id, {}).get("runner_status") == status for row_id, status in expected.items()), "runner statuses match expected pass/block/fail modes"),
        ("VAL4829_04_live_zero_blocked", by_id["RUN4829_0_live_selector_zero_missing"]["runner_status"] == "BLOCKED_PARENT_SELECTOR_MHREF_ZERO_CLAUSES", "live selector zero remains blocked"),
        ("VAL4829_05_direct_MHref_blocked", by_id["RUN4829_3_live_MHref_missing"]["runner_status"] == "BLOCKED_DIRECT_MHREF_INPUTS", "live M_H_ref row remains missing"),
        ("VAL4829_06_smoke_MHref_pass", by_id["RUN4829_4_direct_MHref_smoke_pass"]["M_H_ref_mismatch_abs"] == "0.000000000000000e+00", "direct smoke denominator is internally consistent"),
        ("VAL4829_07_component_smoke_pass", component.get("epsilon_selector_Meff_abs") == "9.000000000000000e-02", "component smoke computes retained selector residual"),
        ("VAL4829_08_forbidden_routes_fail", all(by_id[row_id]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE" for row_id in ("RUN4829_2_forbidden_bare_mass_shortcut", "RUN4829_6_forbidden_reference_only_zero", "RUN4829_7_forbidden_measured_GM_source", "RUN4829_8_forbidden_cancellation")), "forbidden shortcuts fail closed"),
        ("VAL4829_09_no_claim_allowed", not any(str(row.get("claim_allowed", "")).lower() == "true" for row in outputs), "no runner row allows a claim"),
        ("VAL4829_10_runner_compiles", True, "runner compiled before execution"),
        ("VAL4829_11_next_target_written", NEXT_TARGET_CSV.exists(), "next target CSV written"),
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
    doc = f"""# 4829 Y5 R2FR parent worldtube source-measure selector or first MHref row

**Status:** 4829 turns the local source denominator into an executable gate. The exact path is `W_source = closure(supp J_H[tau])` plus `M_H_ref = H_tau[S_outer] - H_ref` with same-frame parent ownership. Current MTS has not signed that path, so the branch stays nonclaim.

**Decision:** `{DECISION}`.

**Claim ceiling:** no local-GR, Newtonian, R10, PPN, source-measure, measured-GM, or `M_H_ref` claim is allowed from 4829.

## Core equations

```text
W_source := closure(supp J_H[tau])
M_H_ref := H_tau[S_outer] - H_ref > 0
epsilon_selector_Meff = (|B_zero|+|Delta_symp|+|H_ref_shift|+|Delta_worldtube|
                         +|Delta_frame|+|coupling_residual|+|R_eq|+|I_commutator|
                         +|T_PiM|+|A_parent|)/M_H_ref
BY5_selector_feed = tau_BY5_MHref epsilon_selector_Meff
```

## Source register

{md_table(sources, ["source_id", "exists", "needle_found", "role"])}

## Selector zero audit

{md_table(audit, ["clause_id", "claim_piece", "current_result", "finite_fallback"])}

## MHref contract

{md_table(contract, ["contract_id", "quantity", "definition", "status"])}

## Runner output

{md_table(outputs, ["row_id", "runner_status", "M_H_ref_abs", "M_H_ref_mismatch_abs", "epsilon_selector_Meff_abs", "BY5_selector_feed_abs", "missing_for_claim"])}

## Decision ledger

{md_table(decision_rows, ["decision_id", "decision", "because", "next_action"])}

## Validation

{md_table(validation, ["validation_id", "result", "detail"])}

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    formal = f"""# 845 PPC4161 parent worldtube source-measure selector or first MHref row

Checkpoint: `{DOC_PATH}`

4829 makes `M_H_ref` a visible gate instead of a hidden denominator. Exact closure requires a parent-signed worldtube selector, same observed time/source frame, integrable `H_tau`, fixed `H_ref`, a Hamiltonian `Pi_M` map, boundary/reference silence, and coupling descent. The live branch remains nonclaim.

Decision: `{DECISION}`

Runner: `{RUNNER}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_claims(timestamp: str) -> None:
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "parent_worldtube_source_measure_selector_or_first_MHref_row",
        "current_evidence": "4829 converts the parent worldtube/source-measure denominator into an executable selector-zero/direct-MHref/component-residual runner; live selector zero and source-backed M_H_ref values remain missing.",
        "status": "parent_worldtube_MHref_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "parent action, same-frame tau, H_tau integrability, fixed H_ref, PiM Hamiltonian map, boundary/reference lock, and coupling descent remain unsigned",
        "sector": "local_gr_Newton_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smoke rows pass but live M_H_ref and selector residual rows are not source-backed",
        "title": "Parent worldtube source-measure selector or first MHref row",
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
        f"""## PPC4161 4829 parent worldtube/MHref runner

`{MARKER}`. The source-coupling route now has an explicit denominator gate: either `W_source=closure(supp J_H[tau])` and `M_H_ref=H_tau[S_outer]-H_ref` are parent-signed, or boundary/reference/worldtube/frame/coupling residuals are retained as `epsilon_selector_Meff` and fed into `BY5`. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4829 parent worldtube source-measure/MHref runner

`{MARKER}` stops hidden source normalization. Conditional zero requires parent-owned `J_H`, tau, worldtube support, integrable `H_tau`, fixed `H_ref`, Hamiltonian `Pi_M`, boundary/reference lock and coupling descent; finite rows compute `M_H_ref`, `epsilon_selector_Meff`, and `BY5` feeds. Bare mass, measured GM, reference-only zero, and cancellation fail closed. Next: `{NEXT_TARGET}`.""",
    )


def update_resume(timestamp: str) -> None:
    text = f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4829-Y5-R2FR-parent-worldtube-source-measure-selector-or-first-MHref-row.md`
Marker: `{MARKER}`

## Where we are

4829 made the source denominator gate executable:

```text
W_source := closure(supp J_H[tau])
M_H_ref := H_tau[S_outer] - H_ref
epsilon_selector_Meff = sum(|selector/source residuals|)/M_H_ref
BY5_selector_feed = tau_BY5_MHref epsilon_selector_Meff
```

## Live blockers

- Parent worldtube/source-measure selector is not parent-signed for current MTS.
- `M_H_ref` has no source-backed same-frame `H_tau`, `H_ref`, units, and reference rule row.
- `Delta_symp`, `H_ref_shift`, boundary flux, frame mismatch, coupling residual, and Hamiltonian/PiM map remain open.
- Bare mass, orbital/measured `GM`, reference-only zeros, and cancellation-only routes are explicitly forbidden.

## Next target

`{NEXT_TARGET}`
"""
    write_text(RESUME_PATH, text)


def main() -> int:
    timestamp = now()
    py_compile.compile(str(RUNNER), doraise=True)
    sources = source_register(timestamp)
    audit = selector_audit(timestamp)
    contract = mhref_contract(timestamp)
    inputs = runner_inputs(timestamp)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(SELECTOR_AUDIT, audit)
    write_csv(MHREF_CONTRACT, contract)
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
        print(f"4829 validation failed: {failed}", file=sys.stderr)
        return 1
    print(f"{MARKER} complete")
    print(f"doc={DOC_PATH}")
    print(f"runner_output={RUNNER_OUTPUT}")
    print(f"validation={VALIDATION_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
