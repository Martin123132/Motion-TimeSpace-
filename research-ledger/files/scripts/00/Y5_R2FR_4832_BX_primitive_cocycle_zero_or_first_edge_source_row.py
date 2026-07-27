from __future__ import annotations

import csv
import math
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

CHECKPOINT = "4832"
CLAIM_ID = "L-674"
MARKER = "PPC4161_BX_PRIMITIVE_COCYCLE_ZERO_OR_FIRST_EDGE_SOURCE_ROW_4832"
PACKET_MARKER = "PPC4161_PACKET_BX_PRIMITIVE_COCYCLE_ZERO_OR_FIRST_EDGE_SOURCE_ROW_4832"
DECISION = "BX_PRIMITIVE_COCYCLE_ZERO_UNSIGNED_FIRST_EDGE_SOURCE_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4833-Y5-R2FR-parent-LThetaQ-boundary-momentum-or-first-bX-norm-row.md"

DOC_PATH = POST / "4832-Y5-R2FR-BX-primitive-cocycle-zero-or-first-edge-source-row.md"
FORMAL_PATH = FORMAL / "848-PPC4161-BX-primitive-cocycle-zero-or-first-edge-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "BX_primitive_cocycle_edge_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4832_SOURCE_REGISTER.csv"
ZERO_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4832_BX_PRIMITIVE_COCYCLE_ZERO_AUDIT.csv"
EDGE_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4832_EDGE_BOUND_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4832_EDGE_SOURCE_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4832_EDGE_SOURCE_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4832_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4832_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4832_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4832_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4832_VALIDATION.csv"

SOURCES = {
    "resume": RESUME_PATH,
    "4831_doc": POST / "4831-Y5-R2FR-boundary-cohomology-projector-silence-or-first-flux-coefficient-row.md",
    "1019_doc": POST / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
    "1020_doc": POST / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
    "be1019": SOURCE_DIR / "P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv",
    "sp1019": SOURCE_DIR / "P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv",
    "weighted1020": SOURCE_DIR / "P8_Y5_R10_1020_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv",
    "bx1020": SOURCE_DIR / "P8_Y5_R10_1020_BX_PRIMITIVE_AUDIT.csv",
    "edgebound1020": SOURCE_DIR / "P8_Y5_R10_1020_SOURCE_PACK_FIRST_BOUND_ROW.csv",
    "bx1021": SOURCE_DIR / "P8_Y5_R10_1021_BX_PRIMITIVE_GATES.csv",
    "bx677": SOURCE_DIR / "P8_Y5_R10_677_BX_EXACTNESS_OR_SOURCE_ROW.csv",
    "bx678": SOURCE_DIR / "P8_Y5_R10_678_BX_SOURCE_ROW_GATE.csv",
    "edge671": SOURCE_DIR / "P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv",
    "gate671": SOURCE_DIR / "P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv",
    "kboundary2428": SOURCE_DIR / "P8_Y5_PARENT_QLOC_2428_KBOUNDARY_COCYCLE_CONTRACT.csv",
    "bx4813": SOURCE_DIR / "P8_Y5_R2FR_4813_BX_PRIMITIVE_GATES_OUTPUT.csv",
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


def as_float(value: Any) -> float:
    try:
        return float(str(value))
    except (TypeError, ValueError):
        return math.nan


def close_to(value: Any, target: float, tolerance: float = 1e-14) -> bool:
    number = as_float(value)
    return math.isfinite(number) and abs(number - target) <= tolerance


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4832_00_resume", SOURCES["resume"], "4832-Y5-R2FR-BX-primitive-cocycle-zero-or-first-edge-source-row.md", "4831 selected this primitive/cocycle target."),
        ("SRC4832_01_4831_doc", SOURCES["4831_doc"], "DEC4831_2_next", "boundary/projector handoff."),
        ("SRC4832_02_1019_doc", SOURCES["1019_doc"], "BE1019_5_cocycle_zero", "boundary exactness and cocycle clauses."),
        ("SRC4832_03_1020_doc", SOURCES["1020_doc"], "ETB1020_3_residual_bound", "weighted-Stokes fallback bound."),
        ("SRC4832_04_1020_doc_BX", SOURCES["1020_doc"], "BXP1020_2_exact_primitive", "explicit primitive gap."),
        ("SRC4832_05_1020_doc_bound", SOURCES["1020_doc"], "EDGEBOUND1020_0_formal_bound_row", "first bound-row schema."),
        ("SRC4832_06_be1019", SOURCES["be1019"], "BE1019_1_BX_exact", "B_X exactness clause."),
        ("SRC4832_07_sp1019", SOURCES["sp1019"], "SP1019_4_edge_coefficients", "edge coefficient schema."),
        ("SRC4832_08_weighted1020", SOURCES["weighted1020"], "ETB1020_3_residual_bound", "weighted-Stokes theorem CSV."),
        ("SRC4832_09_bx1020", SOURCES["bx1020"], "BXP1020_2_exact_primitive", "B_X primitive audit."),
        ("SRC4832_10_edgebound1020", SOURCES["edgebound1020"], "EDGEBOUND1020_0_formal_bound_row", "edge source-pack first row."),
        ("SRC4832_11_bx1021", SOURCES["bx1021"], "BXG1021_2_exact_surface_pullback", "primitive gate carry-forward."),
        ("SRC4832_12_bx677", SOURCES["bx677"], "BX677_0_candidate_formula", "earlier B_X candidate formula."),
        ("SRC4832_13_bx678", SOURCES["bx678"], "BXG678_3_best_empirical_fallback", "Qbar edge empirical fallback."),
        ("SRC4832_14_edge671", SOURCES["edge671"], "ERV671_5_K_boundary", "edge residual vector."),
        ("SRC4832_15_gate671", SOURCES["gate671"], "BCG671_5_boundary_cocycle", "boundary charge owner gate."),
        ("SRC4832_16_kboundary2428", SOURCES["kboundary2428"], "KBC2428_0_contract", "cocycle formula contract."),
        ("SRC4832_17_bx4813", SOURCES["bx4813"], "physical_BX_primitive_missing", "newer primitive gate output."),
        ("SRC4832_18_runner", SOURCES["runner"], "def evaluate_row", "4832 executable runner."),
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
        ("BXZ4832_0_parent_origin", "B_X is derived from one parent variation", "delta L_X = E_X delta X + d Theta_X and B_X=i_epsilon Theta_X-dQ_X+B_ct", "UNSIGNED", "parent_LThetaQ_boundary_momentum_signed"),
        ("BXZ4832_1_counterterm", "counterterm/reference is fixed before readout", "B_ct chosen by differentiability/reference principle, not by R10 fit", "UNSIGNED", "boundary_counterterm_owner_signed"),
        ("BXZ4832_2_primitive", "surface pullback is exact after harmonic split", "i_S^*B_X-h_X=d_S b_X with chart-overlap compatibility", "NOT_DERIVED", "BX_exact_primitive_signed"),
        ("BXZ4832_3_harmonic", "harmonic edge mode vanishes or is bounded", "Pi_Hedge[B_X]=0 or retained as harmonic_edge_abs", "UNSIGNED", "harmonic_edge_zero_signed"),
        ("BXZ4832_4_kernel", "weighted-Stokes kernel is closed or bounded", "d_S(F_lambda epsilon_X)=0 or norm_dS_Feps*norm_bX retained", "UNSIGNED", "kernel_weight_closed_signed"),
        ("BXZ4832_5_cocycle", "boundary generator algebra has no central edge term", "K_boundary[epsilon,eta]=0 from parent Omega and differentiable G_X", "UNCOMPUTED", "K_boundary_cocycle_zero_signed"),
        ("BXZ4832_6_projector", "Pi_M and M_H_ref normalize the retained edge charge", "Qbar_edge_XH <= ||Pi_M^H|| Q_edge_bound/M_H_ref_min", "CONDITIONAL_ONLY", "PiM_projector_bound_signed;M_H_ref_min_signed"),
        ("BXZ4832_7_guard", "no symbolic zero, measured-GM source, closure quotient or cancellation", "edge term can die only by theorem-zero or bounded source row", "GUARD_ACTIVE", "no_cancellation_guard"),
    ]
    return [
        {
            "clause_id": clause_id,
            "claim_piece": claim_piece,
            "math_form": math_form,
            "current_result": current_result,
            "needed_signature": needed_signature,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for clause_id, claim_piece, math_form, current_result, needed_signature in rows
    ]


def edge_contract(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("BEC4832_0_exact_zero", "Q_edge=Qbar_edge_XH=alpha_edge=0", "parent B_X primitive, closed weighted kernel, no harmonic/residual/corner, K_boundary=0, Pi_M/M_H_ref signed", "conditional_only"),
        ("BEC4832_1_direct_bound", "Q_edge_bound", "C_corner + norm_dS_Feps*norm_bX + harmonic_edge_abs + residual_edge_abs + K_boundary_abs", "runner_ready_values_missing"),
        ("BEC4832_2_projection", "Qbar_edge_XH_bound", "PiM_norm*Q_edge_bound/M_H_ref_min", "runner_ready_values_missing"),
        ("BEC4832_3_alpha_edge", "alpha_edge(lambda)", "K_edge*Qbar_edge_XH_bound*qbar_XT", "runner_ready_values_missing"),
        ("BEC4832_4_BY5_feed", "BY5_edge_feed", "tau_BY5_edge*Qbar_edge_XH_bound", "runner_ready_values_missing"),
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
    base = {
        "source_signed": "true",
        "units_signed": "true",
        "same_branch_signed": "true",
        "no_cancellation_guard": "true",
    }
    zero = {
        "parent_LThetaQ_boundary_momentum_signed": "true",
        "boundary_counterterm_owner_signed": "true",
        "compact_corner_free_domain_signed": "true",
        "BX_exact_primitive_signed": "true",
        "overlap_compatibility_signed": "true",
        "pure_gauge_part_zero_signed": "true",
        "harmonic_edge_zero_signed": "true",
        "residual_edge_zero_signed": "true",
        "kernel_weight_closed_signed": "true",
        "K_boundary_cocycle_zero_signed": "true",
        "PiM_projector_bound_signed": "true",
        "M_H_ref_min_signed": "true",
        "no_physical_charge_removed_signed": "true",
        "no_measured_GM_absorption_signed": "true",
    }
    direct = {
        "M_H_ref_min_abs": "2.0",
        "PiM_norm_abs": "0.5",
        "C_corner_abs": "0.01",
        "norm_dS_Feps_abs": "0.02",
        "norm_bX_abs": "3.0",
        "harmonic_edge_abs": "0.02",
        "residual_edge_abs": "0.01",
        "K_boundary_abs": "0.005",
        "K_edge_abs": "1.5",
        "qbar_XT_abs": "0.2",
        "tau_BY5_edge_abs": "2.0",
        "lambda_edge_abs": "0.1",
    }
    component = {
        "M_H_ref_min_abs": "2.0",
        "projector_norm_abs": "0.5",
        "corner_outer_abs": "0.006",
        "corner_inner_abs": "0.004",
        "kernel_weight_derivative_abs": "0.02",
        "bX_norm_abs": "3.0",
        "harmonic_mode_abs": "0.02",
        "residual_mode_abs": "0.01",
        "counterterm_mismatch_abs": "0.015",
        "cocycle_abs": "0.005",
        "K_edge_abs": "1.5",
        "qbar_XT_abs": "0.2",
        "tau_BY5_edge_abs": "2.0",
        "lambda_edge_abs": "0.1",
    }
    doc_1019 = str(SOURCES["1019_doc"])
    doc_1020 = str(SOURCES["1020_doc"])
    edge_671 = str(SOURCES["edge671"])
    gate_671 = str(SOURCES["gate671"])
    kboundary = str(SOURCES["kboundary2428"])
    return [
        {
            "row_id": "RUN4832_0_live_BX_cocycle_zero_missing",
            "route_type": "BX_cocycle_zero",
            "route": "live B_X primitive/cocycle zero audit",
            "source_path": doc_1020,
            "equation_ref": "ETB1020_2_zero_conditions;BXP1020_2_exact_primitive",
            "notes": "current MTS lacks parent LThetaQ, B_ct owner, primitive, harmonic/kernel/cocycle signatures",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4832_1_conditional_BX_cocycle_zero_pass",
            "route_type": "BX_cocycle_zero",
            "route": "conditional parent-signed B_X primitive and cocycle zero",
            "source_path": doc_1019,
            "equation_ref": "BE1019_6_verdict",
            "notes": "nonclaim theorem-shape smoke row",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4832_2_forbidden_symbolic_BX_exact",
            "route_type": "BX_cocycle_zero",
            "route": "forbidden symbolic B_X exactness",
            "source_path": doc_1019,
            "equation_ref": "BE1019_1_BX_exact",
            "notes": "SYMBOLIC_BX_EXACTNESS cannot replace a parent primitive and overlap proof",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4832_3_live_edge_bound_missing",
            "route_type": "direct_edge_bound",
            "route": "live first edge source bound missing",
            "source_path": edge_671,
            "equation_ref": "ERV671_2_Qbar_edge_XH;ERV671_4_BX_boundary_momentum",
            "notes": "schema exists but source-backed C_corner, bX norm, harmonic/residual/cocycle and projector factors are missing",
            **base,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4832_4_direct_edge_bound_smoke_pass",
            "route_type": "direct_edge_bound",
            "route": "direct finite edge bound smoke",
            "source_path": edge_671,
            "equation_ref": "ERV671_2_Qbar_edge_XH",
            "notes": "nonclaim arithmetic smoke for weighted-Stokes edge bound",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4832_5_component_edge_pack_smoke_pass",
            "route_type": "component_edge_pack",
            "route": "component finite edge pack smoke",
            "source_path": kboundary,
            "equation_ref": "KBC2428_0_contract;KBC2428_3_R10_edge",
            "notes": "nonclaim arithmetic smoke for decomposed corner/kernel/harmonic/residual/cocycle envelope",
            **base,
            **component,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4832_6_forbidden_open_weight_stokes",
            "route_type": "BX_cocycle_zero",
            "route": "forbidden Stokes zero with open weight",
            "source_path": doc_1020,
            "equation_ref": "ETB1020_1_weighted_Stokes_identity",
            "notes": "STOKES_ZERO_WITH_OPEN_WEIGHT cannot erase the kernel derivative term",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4832_7_forbidden_harmonic_silence",
            "route_type": "direct_edge_bound",
            "route": "forbidden harmonic silence by assumption",
            "source_path": gate_671,
            "equation_ref": "BCG671_2_exact_boundary_form",
            "notes": "HARMONIC_SILENCE_BY_ASSUMPTION cannot replace a cohomology projection",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4832_8_forbidden_closure_only_quotient",
            "route_type": "BX_cocycle_zero",
            "route": "forbidden closure-only quotient",
            "source_path": doc_1019,
            "equation_ref": "BE1019_3_proper_gauge",
            "notes": "CLOSURE_ONLY_QUOTIENT cannot delete physical edge charges",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4832_9_forbidden_measured_GM_source",
            "route_type": "component_edge_pack",
            "route": "forbidden measured GM source",
            "source_path": edge_671,
            "equation_ref": "ERV671_2_Qbar_edge_XH",
            "notes": "MEASURED_GM_AS_SOURCE cannot normalize an edge-source coefficient",
            **base,
            **component,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4832_10_forbidden_cancellation",
            "route_type": "component_edge_pack",
            "route": "forbidden cancellation of unknown edge components",
            "source_path": edge_671,
            "equation_ref": "ERV671_6_bulk_edge_split",
            "notes": "CANCEL_UNKNOWN_COMPONENTS cannot prove Q_edge or alpha_edge small",
            **base,
            **component,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4832_11_forbidden_GR_import",
            "route_type": "BX_cocycle_zero",
            "route": "forbidden GR import of boundary silence",
            "source_path": doc_1019,
            "equation_ref": "BE1019_6_verdict",
            "notes": "GR_IMPORT cannot replace an MTS parent-action boundary theorem",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
    ]


def decisions(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DEC4832_0_zero", "B_X primitive/cocycle zero is still unsigned for current MTS.", "The route needs one parent-owned LThetaQ boundary momentum, counterterm owner, primitive, cohomology/kernel and cocycle signatures.", "keep local-GR/Newton/R10 promotion blocked", False),
        ("DEC4832_1_bound", "The first edge-source bound is now executable.", "If the primitive/cocycle zero fails, Q_edge_bound, Qbar_edge_XH_bound, alpha_edge and BY5 feed are retained absolutely.", "source or theorem-zero each bound input", False),
        ("DEC4832_2_next", "The next derivation target should hit the parent boundary momentum itself.", "B_X cannot be derived or bounded honestly until L_X, Theta_X, Q_X, B_ct and b_X norm are fixed from the same parent branch.", NEXT_TARGET, False),
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
        ("CG4832_0_runner_installed", "B_X primitive/cocycle edge gate is executable", True, "runner computes exact-zero, direct edge-bound and component edge-pack routes", False),
        ("CG4832_1_zero_unsigned", "B_X primitive and K_boundary cocycle are theorem-zero", False, "parent LThetaQ, counterterm, primitive, harmonic/kernel and cocycle clauses remain unsigned", False),
        ("CG4832_2_edge_bound_ready", "finite edge source row is staged", True, "smoke rows compute Q_edge_bound, Qbar_edge_XH, alpha_edge and BY5 feed without cancellation", False),
        ("CG4832_3_no_shortcuts", "symbolic exactness, open-weight Stokes, harmonic assumption, closure quotient, measured GM, cancellation and GR import fail closed", True, "forbidden rows return FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", False),
        ("CG4832_4_no_local_claim", "local GR/Newton/R10/PPN claims remain blocked", True, "no live row allows a claim", False),
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
            "objective": "derive the parent LThetaQ boundary momentum and first b_X norm row, or keep the edge branch explicitly bounded",
            "include": "L_X, Theta_X, Q_X, B_ct, B_X pullback, b_X norm, harmonic projector, kernel norm, source paths, units, no-cancellation validation",
            "exclude": "symbolic exactness, closure-only quotient, GR import, measured GM denominator, cancellation, local-GR/Newton/R10/PPN claim",
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
        "RUN4832_0_live_BX_cocycle_zero_missing": "BLOCKED_BX_PRIMITIVE_COCYCLE_ZERO_CLAUSES",
        "RUN4832_1_conditional_BX_cocycle_zero_pass": "BX_PRIMITIVE_COCYCLE_ZERO_PASS_NONCLAIM",
        "RUN4832_2_forbidden_symbolic_BX_exact": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4832_3_live_edge_bound_missing": "BLOCKED_DIRECT_EDGE_BOUND_INPUTS",
        "RUN4832_4_direct_edge_bound_smoke_pass": "DIRECT_EDGE_BOUND_PASS_NONCLAIM",
        "RUN4832_5_component_edge_pack_smoke_pass": "COMPONENT_EDGE_PACK_PASS_NONCLAIM",
        "RUN4832_6_forbidden_open_weight_stokes": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4832_7_forbidden_harmonic_silence": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4832_8_forbidden_closure_only_quotient": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4832_9_forbidden_measured_GM_source": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4832_10_forbidden_cancellation": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4832_11_forbidden_GR_import": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
    }
    direct = by_id.get("RUN4832_4_direct_edge_bound_smoke_pass", {})
    component = by_id.get("RUN4832_5_component_edge_pack_smoke_pass", {})
    forbidden_ids = [
        "RUN4832_2_forbidden_symbolic_BX_exact",
        "RUN4832_6_forbidden_open_weight_stokes",
        "RUN4832_7_forbidden_harmonic_silence",
        "RUN4832_8_forbidden_closure_only_quotient",
        "RUN4832_9_forbidden_measured_GM_source",
        "RUN4832_10_forbidden_cancellation",
        "RUN4832_11_forbidden_GR_import",
    ]
    checks = [
        ("VAL4832_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        ("VAL4832_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ("VAL4832_02_output_count", len(outputs) == len(expected), "all runner rows emitted"),
        ("VAL4832_03_expected_statuses", all(by_id.get(row_id, {}).get("runner_status") == status for row_id, status in expected.items()), "runner statuses match expected pass/block/fail modes"),
        ("VAL4832_04_live_zero_blocked", by_id["RUN4832_0_live_BX_cocycle_zero_missing"]["runner_status"] == "BLOCKED_BX_PRIMITIVE_COCYCLE_ZERO_CLAUSES", "live B_X/cocycle zero remains blocked"),
        ("VAL4832_05_live_bound_blocked", by_id["RUN4832_3_live_edge_bound_missing"]["runner_status"] == "BLOCKED_DIRECT_EDGE_BOUND_INPUTS", "live first edge bound row remains missing"),
        ("VAL4832_06_direct_smoke_pass", close_to(direct.get("Q_edge_bound_abs"), 0.105) and close_to(direct.get("Qbar_edge_XH_bound_abs"), 0.02625) and close_to(direct.get("alpha_edge_abs"), 0.007875) and close_to(direct.get("BY5_edge_feed_abs"), 0.0525), "direct edge smoke computes Q, Qbar, alpha and BY5"),
        ("VAL4832_07_component_smoke_pass", close_to(component.get("Q_edge_bound_abs"), 0.12) and close_to(component.get("Qbar_edge_XH_bound_abs"), 0.03) and close_to(component.get("alpha_edge_abs"), 0.009) and close_to(component.get("BY5_edge_feed_abs"), 0.06), "component edge pack smoke computes retained envelope"),
        ("VAL4832_08_forbidden_routes_fail", all(by_id[row_id]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE" for row_id in forbidden_ids), "forbidden shortcuts fail closed"),
        ("VAL4832_09_no_claim_allowed", not any(str(row.get("claim_allowed", "")).lower() == "true" for row in outputs), "no runner row allows a claim"),
        ("VAL4832_10_runner_compiles", True, "runner compiled before execution"),
        ("VAL4832_11_next_target_written", NEXT_TARGET_CSV.exists(), "next target CSV written"),
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
    doc = f"""# 4832 Y5 R2FR B_X primitive cocycle zero or first edge source row

**Status:** 4832 turns the `B_X` primitive and `K_boundary` cocycle gap into an executable zero-or-bound gate. The exact edge-zero route is still unsigned for current MTS, but the finite fallback is now arithmetic rather than rhetorical.

**Decision:** `{DECISION}`.

**Claim ceiling:** no local-GR, Newtonian, R10, R11, PPN, source-charge, boundary-zero, cocycle-zero, or edge-alpha claim is allowed from 4832.

## Core equations

```text
B_X = d_S b_X + h_X + r_X
Q_edge_bound(lambda) =
    C_corner + ||d_S(F_lambda epsilon_X)||_* ||b_X||_*
    + |int_S F_lambda epsilon_X h_X|
    + |int_S F_lambda epsilon_X r_X|
    + |K_boundary|

Qbar_edge_XH_bound(lambda) <= ||Pi_M^H|| Q_edge_bound(lambda)/M_H_ref_min
alpha_edge(lambda) = K_edge(lambda) Qbar_edge_XH_bound(lambda) qbar_XT(lambda)
```

## Source register

{md_table(sources, ["source_id", "exists", "needle_found", "role"])}

## Primitive/cocycle zero audit

{md_table(audit, ["clause_id", "claim_piece", "current_result", "needed_signature"])}

## Edge-source contract

{md_table(contract, ["contract_id", "quantity", "definition", "status"])}

## Runner output

{md_table(outputs, ["row_id", "runner_status", "Q_edge_bound_abs", "Qbar_edge_XH_bound_abs", "alpha_edge_abs", "BY5_edge_feed_abs", "missing_for_claim"])}

## Decision ledger

{md_table(decision_rows, ["decision_id", "decision", "because", "next_action"])}

## Validation

{md_table(validation, ["validation_id", "result", "detail"])}

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    formal = f"""# 848 PPC4161 B_X primitive cocycle zero or first edge source row

Checkpoint: `{DOC_PATH}`

4832 keeps the local-GR path honest by forcing the boundary edge branch through either a parent-signed primitive/cocycle zero or an explicit finite source row. The live route remains nonclaim because `B_X`, `b_X`, `h_X`, `r_X`, `K_boundary`, `Pi_M^H`, and `M_H_ref_min` are not yet parent-owned numeric/theorem inputs.

Decision: `{DECISION}`

Runner: `{RUNNER}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_claims(timestamp: str) -> None:
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "BX_primitive_cocycle_zero_or_first_edge_source_row",
        "current_evidence": "4832 converts the B_X primitive and K_boundary cocycle gap into an executable zero-or-finite edge-source runner; live zero and live source-backed bound rows remain missing.",
        "status": "BX_edge_source_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "parent LThetaQ boundary momentum, counterterm owner, b_X primitive/norm, harmonic/residual/kernel bounds, K_boundary cocycle, Pi_M norm and M_H_ref_min remain unsigned or missing",
        "sector": "local_gr_Newton_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smoke rows pass but live edge-source inputs are not source-backed",
        "title": "B_X primitive cocycle zero or first edge source row",
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
        f"""## PPC4161 4832 B_X primitive/cocycle edge-source gate

`{MARKER}`. The boundary edge branch now has an executable contract: either `B_X=d_S b_X+h_X+r_X` collapses by parent-signed exactness, zero harmonic/residual, closed kernel and `K_boundary=0`, or `Q_edge_bound`, `Qbar_edge_XH_bound`, `alpha_edge` and BY5 feed are retained in a finite source envelope. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4832 B_X primitive/cocycle zero or first edge-source row

`{MARKER}` makes the missing edge coupling computable. The exact zero route is not promoted; the retained route computes `Q_edge_bound`, `Qbar_edge_XH_bound`, `alpha_edge` and BY5 feed without cancellations. Symbolic exactness, open-weight Stokes zero, harmonic silence by assumption, closure quotient, measured GM, cancellation and GR import fail closed. Next: `{NEXT_TARGET}`.""",
    )


def update_resume(timestamp: str) -> None:
    text = f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4832-Y5-R2FR-BX-primitive-cocycle-zero-or-first-edge-source-row.md`
Marker: `{MARKER}`

## Where we are

4832 made the `B_X` primitive/cocycle branch executable:

```text
B_X = d_S b_X + h_X + r_X
Q_edge_bound = C_corner + norm_dS_Feps*norm_bX + harmonic_edge_abs + residual_edge_abs + K_boundary_abs
Qbar_edge_XH_bound <= PiM_norm*Q_edge_bound/M_H_ref_min
alpha_edge = K_edge*Qbar_edge_XH_bound*qbar_XT
```

## Live blockers

- `B_X` is not yet derived from one parent `L_X`, `Theta_X`, `Q_X`, `Omega_X` branch.
- The local boundary counterterm/reference owner is not signed before readout.
- No explicit `b_X` primitive, overlap-compatibility proof, harmonic projection, or kernel norm row is source-backed.
- `K_boundary`, `Pi_M^H`, `M_H_ref_min`, `K_edge`, and `qbar_XT` remain nonclaim unless sourced or theorem-zeroed.
- Symbolic exactness, open-weight Stokes zero, harmonic silence by assumption, closure-only quotient, measured/orbital `GM`, GR import and cancellation routes are explicitly forbidden.

## Next target

`{NEXT_TARGET}`
"""
    write_text(RESUME_PATH, text)


def main() -> int:
    timestamp = now()
    py_compile.compile(str(RUNNER), doraise=True)
    sources = source_register(timestamp)
    audit = zero_audit(timestamp)
    contract = edge_contract(timestamp)
    inputs = runner_inputs(timestamp)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_AUDIT, audit)
    write_csv(EDGE_CONTRACT, contract)
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
        print(f"4832 validation failed: {failed}", file=sys.stderr)
        return 1
    print(f"{MARKER} complete")
    print(f"doc={DOC_PATH}")
    print(f"runner_output={RUNNER_OUTPUT}")
    print(f"validation={VALIDATION_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
