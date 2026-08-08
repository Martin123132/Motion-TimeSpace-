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

CHECKPOINT = "4828"
CLAIM_ID = "L-670"
MARKER = "PPC4161_TOPOLOGICAL_HILBERT_EQUALITY_OR_FIRST_REQ_BZERO_ROW_4828"
PACKET_MARKER = "PPC4161_PACKET_TOPOLOGICAL_HILBERT_EQUALITY_OR_FIRST_REQ_BZERO_ROW_4828"
DECISION = "TOPOLOGICAL_HILBERT_EQUALITY_UNSIGNED_FIRST_REQ_BZERO_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4829-Y5-R2FR-parent-worldtube-source-measure-selector-or-first-MHref-row.md"

DOC_PATH = POST / "4828-Y5-R2FR-topological-Hilbert-equality-or-first-Req-Bzero-row.md"
FORMAL_PATH = FORMAL / "844-PPC4161-topological-Hilbert-equality-or-first-Req-Bzero-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "topological_Hilbert_Req_Bzero_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4828_SOURCE_REGISTER.csv"
ZERO_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4828_TOPO_HILBERT_EQUALITY_ZERO_AUDIT.csv"
BOUND_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4828_REQ_BZERO_BOUND_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4828_REQ_BZERO_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4828_REQ_BZERO_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4828_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4828_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4828_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4828_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4828_VALIDATION.csv"

SOURCES = {
    "resume": RESUME_PATH,
    "4827_doc": POST / "4827-Y5-R2FR-projector-stress-zero-or-first-TPiM-bound-row.md",
    "1015_doc": POST / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
    "1014_doc": POST / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
    "1013_doc": POST / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
    "top_conditions": SOURCE_DIR / "P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv",
    "top_parent": SOURCE_DIR / "P8_TOPOLOGICAL_PIM_PARENT_CLAUSE_ATTEMPT.csv",
    "top_failure": SOURCE_DIR / "P8_TOPOLOGICAL_PIM_FAILURE_ANALYSIS.csv",
    "top_certificate": SOURCE_DIR / "P8_Y5_PIM_TOPO_EQUALITY_CERTIFICATE.csv",
    "top_gates": SOURCE_DIR / "P8_Y5_PIM_TOPO_EQUALITY_ACCEPTANCE_GATES.csv",
    "radial_input": SOURCE_DIR / "P8_Y5_PIM_RADIAL_BOUND_INPUT.csv",
    "fill_template": SOURCE_DIR / "P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv",
    "obstruction_vector": SOURCE_DIR / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
    "worldtube_glue": SOURCE_DIR / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
    "worldtube_measure": SOURCE_DIR / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
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
        ("SRC4828_00_resume", SOURCES["resume"], "4828-Y5-R2FR-topological-Hilbert-equality-or-first-Req-Bzero-row.md", "4827 selected this target."),
        ("SRC4828_01_4827_doc", SOURCES["4827_doc"], "Next target: `4828-Y5-R2FR-topological-Hilbert-equality-or-first-Req-Bzero-row.md`", "current packet handoff."),
        ("SRC4828_02_1015_sol", SOURCES["1015_doc"], "SOL1015_3_de_rham_equality", "old equality lemma."),
        ("SRC4828_03_1015_reb", SOURCES["1015_doc"], "REB1015_0_R_eq_integral", "old residual row."),
        ("SRC4828_04_1014_req", SOURCES["1014_doc"], "PCC1014_0_R_eq_integral", "commutator checkpoint residual."),
        ("SRC4828_05_1014_bzero", SOURCES["1014_doc"], "PCC1014_2_B_zero_flux", "boundary exact term residual."),
        ("SRC4828_06_1013_req", SOURCES["1013_doc"], "OBS1013_3_topological_equality_residual", "measured-GM obstruction vector."),
        ("SRC4828_07_1013_bzero", SOURCES["1013_doc"], "OBS1013_4_boundary_zero_flux", "boundary flux obstruction."),
        ("SRC4828_08_top_condition", SOURCES["top_conditions"], "TC500_3_Hilbert_equality", "topological route condition."),
        ("SRC4828_09_top_parent", SOURCES["top_parent"], "TP500_3_Hilbert_equality_gate", "parent clause attempt."),
        ("SRC4828_10_top_failure", SOURCES["top_failure"], "F500_0_conserved_wrong_object", "wrong conserved object failure."),
        ("SRC4828_11_top_certificate", SOURCES["top_certificate"], "PTEC534_4_topological_Hilbert_equality", "topological equality certificate."),
        ("SRC4828_12_top_gates", SOURCES["top_gates"], "AG534_1_no_wrong_conserved_object", "acceptance gate."),
        ("SRC4828_13_radial", SOURCES["radial_input"], "PI521_3_topological_equality_residual", "radial source-hair input."),
        ("SRC4828_14_fill", SOURCES["fill_template"], "PIF537_0_R_eq_integral", "R_eq fill template."),
        ("SRC4828_15_bzero_fill", SOURCES["fill_template"], "PIF537_2_B_zero_flux", "B_zero fill template."),
        ("SRC4828_16_worldtube_glue", SOURCES["worldtube_glue"], "W504_4_worldtube_source_measure_glue", "worldtube glue blocker."),
        ("SRC4828_17_worldtube_measure", SOURCES["worldtube_measure"], "T510_1_worldtube_source_measure", "source-measure theorem."),
        ("SRC4828_18_runner", SOURCES["runner"], "def evaluate_row", "4828 executable runner."),
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
        ("REQZ4828_0_worldtube", "same compact Hilbert source worldtube", "W_source and linking S2 class are fixed by parent source support before readout", "NOT_PARENT_SIGNED", "Delta_worldtube_domain row"),
        ("REQZ4828_1_source_measure", "same observed Hilbert/Noether source measure", "Q_M is defined from the same dressed source charge as Pi_M J_H", "NOT_LOCKED", "M_H_ref/source-measure row"),
        ("REQZ4828_2_topological_PD", "J_M_top is Poincare dual of that worldtube", "J_M_top=Q_M omega_M_top with d omega_M_top=0 and integral_link omega=1", "CONDITIONAL_SHAPE_ONLY", "R_eq row"),
        ("REQZ4828_3_same_class", "same de Rham compact-support class", "Pi_M J_H-J_M_top=dB_zero+R_eq with R_eq=0 only if same-class premise is parent-signed", "KEY_BLOCKER", "R_eq_integral row"),
        ("REQZ4828_4_boundary_zero", "exact term has zero compact boundary flux", "integral_boundary dB_zero=0 with reference fixed once", "FAIL_OPEN", "B_zero_flux row"),
        ("REQZ4828_5_commutator_stress", "commutator and projector stress already controlled", "[d,Pi_M]J_H=0 and T_PiM=0/bounded in same branch", "PARTIAL_SMOKE_ONLY", "4826/4827 feeds"),
        ("REQZ4828_6_no_extra_exchange", "extra projected source channels silent", "Pi_M dJ_extra=0 for boundary/domain/bulk/nonEH/kappa/frame/species", "NOT_PARENT_DERIVED", "Delta_extra_vector row"),
        ("REQZ4828_7_calibration_PPN", "same charge controls Newton/PPN readout", "source charge controls inverse-square coefficient and second-order PPN vector", "NOT_REACHED", "Delta_cal/Delta_PPN row"),
        ("REQZ4828_8_anti_circularity", "no late equality multiplier or measured-GM source", "reference-only zero/readout mask/fitted GM cannot prove equality", "POLICY_GUARD", "forbidden-source guard"),
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


def bound_contract(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("REQC4828_0_zero", "R_eq=B_zero=0", "all same-object and boundary-zero clauses parent-signed in one branch", "conditional_only"),
        ("REQC4828_1_direct", "(|R_eq|+|B_zero|)/M_H_ref", "first direct equality/boundary residual envelope", "runner_ready_values_missing"),
        ("REQC4828_2_component", "sum residual components / M_H_ref", "R_eq+B_zero+I_commutator+domain+extra+T_PiM+A_parent envelope", "runner_ready_values_missing"),
        ("REQC4828_3_BY5", "BY5_equality_feed=tau_BY5_Req epsilon_eq_Meff", "feeds same-object failure into BY5/source-normalization branch", "runner_ready_values_missing"),
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
    doc_1015 = str(SOURCES["1015_doc"])
    fill = str(SOURCES["fill_template"])
    base = {
        "source_signed": "true",
        "units_signed": "true",
        "same_branch_signed": "true",
        "no_cancellation_guard": "true",
    }
    zero = {
        "worldtube_fixed_signed": "true",
        "source_measure_owned_signed": "true",
        "topological_representative_PD_signed": "true",
        "same_deRham_class_signed": "true",
        "Hilbert_to_PiM_charge_map_signed": "true",
        "boundary_zero_flux_signed": "true",
        "commutator_zero_signed": "true",
        "projector_stress_silence_signed": "true",
        "no_extra_exchange_signed": "true",
        "calibration_PPN_stable_signed": "true",
        "no_readout_mask_signed": "true",
        "no_measured_GM_absorption_signed": "true",
    }
    return [
        {
            "row_id": "RUN4828_0_live_zero_missing",
            "route_type": "equality_zero",
            "route": "live same-object zero audit",
            "source_path": doc_1015,
            "equation_ref": "SOL1015_6_verdict",
            "notes": "current MTS has unsigned worldtube/source/class/boundary clauses",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4828_1_conditional_zero_pass",
            "route_type": "equality_zero",
            "route": "conditional parent-signed same-object zero",
            "source_path": doc_1015,
            "equation_ref": "SOL1015_3_de_rham_equality",
            "notes": "nonclaim theorem-shape smoke row",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4828_2_forbidden_late_multiplier",
            "route_type": "equality_zero",
            "route": "forbidden late equality multiplier",
            "source_path": doc_1015,
            "equation_ref": "late equality multiplier",
            "notes": "LATE_EQUALITY_MULTIPLIER cannot derive source equality",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4828_3_live_direct_bound_missing",
            "route_type": "direct_bound",
            "route": "live R_eq/B_zero rows missing",
            "source_path": str(SOURCES["radial_input"]),
            "equation_ref": "PI521_3_topological_equality_residual",
            "R_eq_integral_abs": "MISSING_R_EQ_INTEGRAL",
            "B_zero_flux_abs": "MISSING_B_ZERO_FLUX",
            "M_H_ref_abs": "MISSING_M_H_REF",
            "tau_BY5_Req_abs": "MISSING_tau",
            "notes": "no physical source-backed equality row yet",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4828_4_direct_Req_Bzero_smoke_pass",
            "route_type": "direct_bound",
            "route": "direct finite R_eq/B_zero smoke",
            "source_path": fill,
            "equation_ref": "PIF537_0_R_eq_integral;PIF537_2_B_zero_flux",
            "R_eq_integral_abs": "0.03",
            "B_zero_flux_abs": "0.02",
            "M_H_ref_abs": "2.0",
            "tau_BY5_Req_abs": "1.5",
            "notes": "nonclaim direct equality smoke row",
            **base,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4828_5_component_Req_Bzero_smoke_pass",
            "route_type": "component_bound",
            "route": "component finite equality smoke",
            "source_path": doc_1015,
            "equation_ref": "REB1015_7_epsilon_eq_Meff",
            "R_eq_integral_abs": "0.02",
            "B_zero_flux_abs": "0.01",
            "I_commutator_abs": "0.03",
            "Delta_worldtube_domain_abs": "0.02",
            "Delta_extra_vector_abs": "0.01",
            "projector_stress_beta_equiv_abs": "0.01",
            "A_parent_abs": "0.02",
            "M_H_ref_abs": "2.0",
            "tau_BY5_Req_abs": "2.0",
            "notes": "nonclaim component equality smoke row",
            **base,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4828_6_forbidden_reference_zero",
            "route_type": "direct_bound",
            "route": "forbidden reference-only zero",
            "source_path": doc_1015,
            "equation_ref": "reference row sets equality zero",
            "R_eq_integral_abs": "0.0",
            "B_zero_flux_abs": "0.0",
            "M_H_ref_abs": "1.0",
            "tau_BY5_Req_abs": "1.0",
            "notes": "REFERENCE_ONLY_ZERO cannot prove same-object equality",
            **base,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4828_7_forbidden_measured_GM_source",
            "route_type": "component_bound",
            "route": "forbidden measured GM source",
            "source_path": doc_1015,
            "equation_ref": "measured GM readout",
            "R_eq_integral_abs": "0.0",
            "B_zero_flux_abs": "0.0",
            "I_commutator_abs": "0.0",
            "Delta_worldtube_domain_abs": "0.0",
            "Delta_extra_vector_abs": "0.0",
            "projector_stress_beta_equiv_abs": "0.0",
            "A_parent_abs": "0.0",
            "M_H_ref_abs": "1.0",
            "tau_BY5_Req_abs": "1.0",
            "notes": "MEASURED_GM_AS_SOURCE cannot source equality",
            **base,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4828_8_forbidden_cancellation",
            "route_type": "component_bound",
            "route": "forbidden cancellation",
            "source_path": doc_1015,
            "equation_ref": "component cancellation",
            "R_eq_integral_abs": "0.01",
            "B_zero_flux_abs": "0.01",
            "I_commutator_abs": "0.01",
            "Delta_worldtube_domain_abs": "0.01",
            "Delta_extra_vector_abs": "0.01",
            "projector_stress_beta_equiv_abs": "0.01",
            "A_parent_abs": "0.01",
            "M_H_ref_abs": "1.0",
            "tau_BY5_Req_abs": "1.0",
            "notes": "CANCEL_UNKNOWN_COMPONENTS is not a source equality theorem",
            **base,
            "timestamp_utc": timestamp,
        },
    ]


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), str(RUNNER_INPUT), str(RUNNER_OUTPUT)], check=True)


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4828_0",
            "decision": DECISION,
            "basis": "same-object equality remains unsigned; R_eq/B_zero and component residual smoke rows execute; forbidden equality shortcuts fail closed",
            "zero_claim": False,
            "finite_bound_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def claim_gates(timestamp: str, outputs: list[dict[str, str]]) -> list[dict[str, Any]]:
    by_id = {row["row_id"]: row for row in outputs}
    return [
        {
            "gate_id": "CG4828_0_equality_zero",
            "claim": "Pi_M J_H = J_M_top + dB_zero with zero compact boundary flux",
            "passed": by_id["RUN4828_0_live_zero_missing"]["runner_status"] == "REQ_BZERO_EQUALITY_ZERO_PASS_NONCLAIM",
            "claim_allowed": False,
            "reason": "live worldtube/source/class/boundary/calibration clauses remain unsigned",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CG4828_1_bound_ready",
            "claim": "source-backed R_eq/B_zero/M_H_ref row exists",
            "passed": by_id["RUN4828_3_live_direct_bound_missing"]["runner_status"] == "REQ_BZERO_DIRECT_BOUND_PASS_NONCLAIM",
            "claim_allowed": False,
            "reason": "live R_eq/B_zero rows remain missing; smoke rows only check arithmetic",
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CG4828_2_anti_circularity",
            "claim": "no late multiplier/reference/measured-GM/cancellation shortcut is used",
            "passed": by_id["RUN4828_2_forbidden_late_multiplier"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE"
            and by_id["RUN4828_6_forbidden_reference_zero"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE"
            and by_id["RUN4828_7_forbidden_measured_GM_source"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
            "claim_allowed": False,
            "reason": "forbidden routes fail closed",
            "timestamp_utc": timestamp,
        },
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "decision": DECISION,
            "claim_allowed": False,
            "physics_status": "topological-Hilbert same-object equality remains unsigned; R_eq/B_zero/M_H_ref finite contract is executable but nonclaim",
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "reason": "R_eq/B_zero cannot become physical without the parent-owned compact source worldtube, same-frame Hilbert source measure, and normalization M_H_ref",
            "success_condition": "derive parent worldtube/source-measure selector and M_H_ref normalization, or produce first source-backed M_H_ref/domain selector rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def validate(timestamp: str, outputs: list[dict[str, str]], sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {row["row_id"]: row for row in outputs}
    checks = [
        ("VAL4828_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        ("VAL4828_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ("VAL4828_02_live_zero_blocked", by_id["RUN4828_0_live_zero_missing"]["runner_status"] == "BLOCKED_REQ_BZERO_EQUALITY_ZERO_CLAUSES", "live same-object zero remains blocked"),
        ("VAL4828_03_conditional_zero_pass", by_id["RUN4828_1_conditional_zero_pass"]["runner_status"] == "REQ_BZERO_EQUALITY_ZERO_PASS_NONCLAIM", "conditional equality zero computes"),
        ("VAL4828_04_late_multiplier_fails", by_id["RUN4828_2_forbidden_late_multiplier"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "late equality multiplier fails closed"),
        ("VAL4828_05_live_bound_blocked", by_id["RUN4828_3_live_direct_bound_missing"]["runner_status"] == "BLOCKED_REQ_BZERO_DIRECT_BOUND_INPUTS", "live R_eq/B_zero row missing"),
        ("VAL4828_06_direct_smoke_pass", by_id["RUN4828_4_direct_Req_Bzero_smoke_pass"]["runner_status"] == "REQ_BZERO_DIRECT_BOUND_PASS_NONCLAIM", "direct R_eq/B_zero smoke passes"),
        ("VAL4828_07_component_smoke_pass", by_id["RUN4828_5_component_Req_Bzero_smoke_pass"]["runner_status"] == "REQ_BZERO_COMPONENT_BOUND_PASS_NONCLAIM", "component equality smoke passes"),
        ("VAL4828_08_reference_zero_fails", by_id["RUN4828_6_forbidden_reference_zero"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "reference-only zero fails closed"),
        ("VAL4828_09_measured_GM_fails", by_id["RUN4828_7_forbidden_measured_GM_source"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "measured-GM shortcut fails closed"),
        ("VAL4828_10_cancellation_fails", by_id["RUN4828_8_forbidden_cancellation"]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", "cancellation shortcut fails closed"),
        ("VAL4828_11_no_claim_allowed", all(str(row.get("claim_allowed", "")).lower() == "false" for row in outputs), "no runner row allows a claim"),
    ]
    return [
        {
            "validation_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "details": details,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, details in checks
    ]


def build_docs(timestamp: str, sources: list[dict[str, Any]], audit: list[dict[str, Any]], contract: list[dict[str, Any]], outputs: list[dict[str, str]], validations: list[dict[str, Any]]) -> None:
    doc = f"""# 4828 - Topological Hilbert Equality Or First Req Bzero Row

Marker: `{MARKER}`

## Summary

4828 attacks the conserved-wrong-object problem:

```text
Pi_M J_H - J_M_top = dB_zero + R_eq
epsilon_eq_Meff = (|R_eq|+|B_zero|+other retained equality residuals)/M_H_ref
BY5_equality_feed = tau_BY5_Req epsilon_eq_Meff
```

The mathematical route is clean: if `Pi_M J_H` and `J_M_top` are representatives of the same compact Hilbert source-worldtube class, their difference is exact plus a residual, and the residual vanishes when the same-class and zero-boundary premises are parent-signed. The current MTS branch does not yet sign those premises. The finite route is now executable: `R_eq`, `B_zero`, and component equality residuals can feed the source-normalization chain without using a late equality multiplier, reference-only zero, measured `GM`, or cancellation.

## Source register

{md_table(sources, ['source_id', 'exists', 'needle_found', 'role'])}

## Zero audit

{md_table(audit, ['clause_id', 'claim_piece', 'current_result', 'finite_fallback'])}

## Bound contract

{md_table(contract, ['contract_id', 'quantity', 'definition', 'status'])}

## Runner output

{md_table(outputs, ['row_id', 'runner_status', 'R_eq_norm_abs', 'B_zero_norm_abs', 'epsilon_eq_Meff_abs', 'BY5_equality_feed_abs', 'missing_for_claim'])}

## Decision

`{DECISION}`

Next target: `{NEXT_TARGET}`

## Validation

{md_table(validations, ['validation_id', 'result', 'details'])}
"""
    formal = f"""# 844 - PPC4161 topological-Hilbert equality or first Req/Bzero row

Marker: `{MARKER}`

4828 makes the same-object problem explicit. A closed `J_M_top` only helps local GR/Newton if it is the same observed Hilbert source current:

```text
Pi_M J_H - J_M_top = dB_zero + R_eq
epsilon_eq_Meff = (|R_eq|+|B_zero|+...)/M_H_ref
BY5_equality_feed = tau_BY5_Req epsilon_eq_Meff
```

The live branch does not prove this equality. Direct and component smoke rows compute the fallback envelope, and forbidden shortcuts fail closed. No local-GR/Newton/source-normalization claim is allowed from this checkpoint.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    write_text(FORMAL_PATH, formal)


def update_claims(timestamp: str) -> None:
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "topological_Hilbert_equality_or_first_Req_Bzero_row",
        "current_evidence": "4828 converts the same-object problem into an executable R_eq/B_zero/M_H_ref zero-or-finite runner; live equality and source-backed residual values remain missing.",
        "status": "topological_Hilbert_Req_Bzero_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "parent worldtube, same-frame source measure, same de Rham class, boundary zero flux, M_H_ref normalization, and calibration/PPN stability remain missing",
        "sector": "local_gr_Newton_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smoke rows pass but live R_eq/B_zero rows are not source-backed",
        "title": "Topological-Hilbert equality or first Req/Bzero row",
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
        f"""## PPC4161 4828 topological-Hilbert equality runner

`{MARKER}`. The same-object problem is now an explicit source-coupling gate: either `Pi_M J_H = J_M_top + dB_zero` is parent-signed with zero compact boundary flux, or `R_eq/B_zero` are retained and normalized by `M_H_ref` into `epsilon_eq_Meff` and `BY5`. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4828 topological-Hilbert equality zero-or-bound runner

`{MARKER}` prevents a closed wrong current from being promoted as Newtonian mass. Conditional zero requires parent-signed worldtube/source/class/boundary/calibration clauses; finite direct/component rows compute `R_eq/B_zero` and `BY5` feeds; late multipliers, reference zeros, measured-GM and cancellation shortcuts fail closed. Next: `{NEXT_TARGET}`.""",
    )


def update_resume(timestamp: str) -> None:
    text = f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4828-Y5-R2FR-topological-Hilbert-equality-or-first-Req-Bzero-row.md`
Marker: `{MARKER}`

## Where we are

4828 made the same-object equality gate executable:

```text
Pi_M J_H - J_M_top = dB_zero + R_eq
epsilon_eq_Meff = (|R_eq|+|B_zero|+other retained equality residuals)/M_H_ref
BY5_equality_feed = tau_BY5_Req epsilon_eq_Meff
```

## Live blockers

- `Pi_M J_H = J_M_top + dB_zero` is not parent-signed.
- Parent compact worldtube, same-frame source measure, same de Rham class, zero compact boundary flux, and `M_H_ref` normalization remain open.
- No source-backed physical `R_eq`/`B_zero` row exists yet.
- Late equality multipliers, reference-only zeros, measured `GM`, and cancellation-only routes are explicitly forbidden.

## Next target

`{NEXT_TARGET}`
"""
    write_text(RESUME_PATH, text)


def main() -> int:
    timestamp = now()
    py_compile.compile(str(RUNNER), doraise=True)
    py_compile.compile(__file__, doraise=True)

    sources = source_register(timestamp)
    audit = zero_audit(timestamp)
    contract = bound_contract(timestamp)
    inputs = runner_inputs(timestamp)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_AUDIT, audit)
    write_csv(BOUND_CONTRACT, contract)
    write_csv(RUNNER_INPUT, inputs)

    run_runner()
    outputs = read_csv(RUNNER_OUTPUT)
    decisions = decision_rows(timestamp)
    gates = claim_gates(timestamp, outputs)
    status = status_rows(timestamp)
    next_target_rows = next_rows(timestamp)
    validations = validate(timestamp, outputs, sources)

    write_csv(DECISION_CSV, decisions)
    write_csv(CLAIM_GATES, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_target_rows)
    write_csv(VALIDATION_CSV, validations)

    build_docs(timestamp, sources, audit, contract, outputs, validations)
    update_claims(timestamp)
    update_spine_and_packet(timestamp)
    update_resume(timestamp)

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validations if row["result"] != "PASS"]
    if failed:
        raise RuntimeError(f"4828 validation failed: {failed}")
    print(f"{MARKER} complete")
    print(f"doc={DOC_PATH}")
    print(f"validation={VALIDATION_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
