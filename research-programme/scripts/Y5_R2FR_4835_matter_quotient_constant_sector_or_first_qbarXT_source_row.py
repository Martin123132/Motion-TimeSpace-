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

CHECKPOINT = "4835"
CLAIM_ID = "L-677"
MARKER = "PPC4161_MATTER_QUOTIENT_CONSTANT_SECTOR_OR_FIRST_QBARXT_SOURCE_ROW_4835"
PACKET_MARKER = "PPC4161_PACKET_MATTER_QUOTIENT_CONSTANT_SECTOR_OR_FIRST_QBARXT_SOURCE_ROW_4835"
DECISION = "MATTER_QUOTIENT_CONSTANT_SECTOR_UNSIGNED_FIRST_QBARXT_SOURCE_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4836-Y5-R2FR-constant-superselection-EM-mass-clock-or-first-theta-derivative-row.md"

DOC_PATH = POST / "4835-Y5-R2FR-matter-quotient-constant-sector-or-first-qbarXT-source-row.md"
FORMAL_PATH = FORMAL / "851-PPC4161-matter-quotient-constant-sector-or-first-qbarXT-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "matter_quotient_constant_qbarXT_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4835_SOURCE_REGISTER.csv"
QBAR_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4835_MATTER_CONSTANT_QBARXT_AUDIT.csv"
QBAR_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4835_QBARXT_SOURCE_ROW_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4835_QBARXT_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4835_QBARXT_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4835_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4835_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4835_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4835_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4835_VALIDATION.csv"

SOURCES = {
    "resume": RESUME_PATH,
    "4834_doc": POST / "4834-Y5-R2FR-parent-theta-omega-DC-operator-or-source-coupling-bound-row.md",
    "637_doc": POST / "637-Y5-R10-parent-action-quotient-map-and-constant-ownership-derivation.md",
    "621_doc": POST / "621-Y5-R10-matter-coupling-normal-form-theorem-or-residual-coefficient-priors.md",
    "622_doc": POST / "622-Y5-R10-parent-matter-sector-contract-or-residual-prior-runner.md",
    "618_zero": SOURCE_DIR / "P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv",
    "637_qmap": SOURCE_DIR / "P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv",
    "621_normal": SOURCE_DIR / "P8_Y5_R10_621_NORMAL_FORM_THEOREM_ATTEMPT.csv",
    "621_clauses": SOURCE_DIR / "P8_Y5_R10_621_PARENT_CLAUSE_LEDGER.csv",
    "621_components": SOURCE_DIR / "P8_Y5_R10_621_COMPONENT_STATUS_MATRIX.csv",
    "621_priors": SOURCE_DIR / "P8_Y5_R10_621_COEFFICIENT_PRIOR_TEMPLATE.csv",
    "621_arenas": SOURCE_DIR / "P8_Y5_R10_621_ARENA_PRIOR_SCHEMA.csv",
    "622_contract": SOURCE_DIR / "P8_Y5_R10_622_PARENT_MATTER_CONTRACT.csv",
    "622_smoke": SOURCE_DIR / "P8_Y5_R10_622_SMOKE_PRIOR_ROWS.csv",
    "2611_chain": SOURCE_DIR / "P8_Y5_MATTER_DESCENT_GATE_2611_CHAIN_RULE_DECOMPOSITION.csv",
    "2611_premise": SOURCE_DIR / "P8_Y5_MATTER_DESCENT_GATE_2611_DESCENT_PREMISE_AUDIT.csv",
    "2611_interface": SOURCE_DIR / "P8_Y5_MATTER_DESCENT_GATE_2611_AMATTER_BOUND_INTERFACE.csv",
    "2612_grammar": SOURCE_DIR / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv",
    "2587_contract": SOURCE_DIR / "P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv",
    "4834_output": SOURCE_DIR / "P8_Y5_R2FR_4834_THETA_OMEGA_DC_RUNNER_OUTPUT.csv",
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
        ("SRC4835_00_resume", SOURCES["resume"], "4835-Y5-R2FR-matter-quotient-constant-sector-or-first-qbarXT-source-row.md", "4834 selected this qbarXT target."),
        ("SRC4835_01_4834_doc", SOURCES["4834_doc"], "DEC4834_2_next", "source-coupling handoff."),
        ("SRC4835_02_637_chain", SOURCES["637_doc"], "OF637_1_chain_rule", "matter chain-rule descent."),
        ("SRC4835_03_637_constants", SOURCES["637_doc"], "CO637_0_descent_criterion", "constant-sector descent criterion."),
        ("SRC4835_04_637_status", SOURCES["637_doc"], "CS637_1_em_charge_alpha", "EM/charge constant blocker."),
        ("SRC4835_05_621_normal", SOURCES["621_doc"], "NMF621_3_constant_triviality", "normal-form constant clause."),
        ("SRC4835_06_621_decision", SOURCES["621_doc"], "D621_0_main_verdict", "normal form not parent-derived."),
        ("SRC4835_07_622_contract", SOURCES["622_doc"], "PMC622_4_constant_superselection", "parent matter contract constants."),
        ("SRC4835_08_622_alpha", SOURCES["622_doc"], "SP622_1_alpha_EM", "alpha_EM placeholder row."),
        ("SRC4835_09_618_zero", SOURCES["618_zero"], "SZ618_0_qbar_XT_chain_rule", "qbarXT conditional zero."),
        ("SRC4835_10_637_qmap", SOURCES["637_qmap"], "QM637_2_vertical_kernel", "vertical kernel quotient map."),
        ("SRC4835_11_621_normal_csv", SOURCES["621_normal"], "NMF621_3_constant_triviality", "normal form CSV."),
        ("SRC4835_12_621_clauses", SOURCES["621_clauses"], "PCL621_2_constant_superselection", "constant proof obligation."),
        ("SRC4835_13_621_components", SOURCES["621_components"], "qbarXT_vec", "qbarXT component status."),
        ("SRC4835_14_621_priors", SOURCES["621_priors"], "CP621_1_alpha_EM", "alpha_EM prior template."),
        ("SRC4835_15_621_arenas", SOURCES["621_arenas"], "AP621_3_clocks_EM", "clocks/EM arena dependency."),
        ("SRC4835_16_622_contract_csv", SOURCES["622_contract"], "PMC622_4_constant_superselection", "parent matter contract CSV."),
        ("SRC4835_17_622_smoke", SOURCES["622_smoke"], "SP622_1_alpha_EM", "prior smoke row."),
        ("SRC4835_18_2611_chain", SOURCES["2611_chain"], "CR2611_2_constants", "matter descent constants term."),
        ("SRC4835_19_2611_premise", SOURCES["2611_premise"], "PRE2611_3_constants", "descent premise constants."),
        ("SRC4835_20_2611_interface", SOURCES["2611_interface"], "AM2611_2_A_theta", "A_theta bound interface."),
        ("SRC4835_21_2612_grammar", SOURCES["2612_grammar"], "NDV2612_1_allowed_syntax", "no direct matter X grammar."),
        ("SRC4835_22_2587_contract", SOURCES["2587_contract"], "MCA2587_2_minimal_matter_terms", "minimal parent matter syntax."),
        ("SRC4835_23_4834_output", SOURCES["4834_output"], "RUN4834_4_direct_source_coupling_smoke_pass", "upstream source-coupling runner."),
        ("SRC4835_24_runner", SOURCES["runner"], "def evaluate_row", "4835 executable runner."),
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


def qbar_audit(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("MQC4835_0_qmap", "parent quotient map", "q:Phi_parent->Q_obs and Dq[v_X]=0 before readout", "CONDITIONAL_ONLY", "q_map_signed"),
        ("MQC4835_1_observed_geometry", "observed geometry functor", "e_obs=Obs_e(q(Phi)); Lie_v e_obs=0", "NOT_PARENT_SIGNED", "observed_geometry_functor_signed"),
        ("MQC4835_2_matter_functor", "ordinary matter grammar", "S_ord=sum_A S_A[Psi_A,e_obs(q(Phi)),omega[e_obs],theta_A]", "CONTRACT_ONLY", "matter_functor_signed"),
        ("MQC4835_3_constants", "constant/superselection sector", "theta_A=theta_bar_A(q(Phi)) or fixed representation data; Lie_v theta_A=0", "OPEN_BLOCKER", "constants_superselection_signed"),
        ("MQC4835_4_marker", "material marker taxonomy", "no matter-visible marker, or marker is absent/gauge/auxiliary/source-independent", "OPEN_BLOCKER", "no_material_marker_signed"),
        ("MQC4835_5_lift", "matter-field vertical lift", "delta_v Psi is zero/on-shell/gauge-Lorentz with proper boundary", "OPEN_BLOCKER", "matter_lift_signed"),
        ("MQC4835_6_worldtube", "worldtube/source support", "W_source and source measure descend before fitting/readout", "OPEN_BLOCKER", "worldtube_support_signed"),
        ("MQC4835_7_direct", "no direct matter X vertex", "no V_m[X,rho_A,W], no hidden frames, no relative source prefactors", "CONDITIONAL_SCHEMA", "no_direct_matter_X_vertex_signed"),
        ("MQC4835_8_universal", "universal source current", "one Hilbert/coframe source and universal kappa for ordinary matter", "OPEN_BLOCKER", "universal_source_current_signed"),
        ("MQC4835_9_nonHilbert", "non-Hilbert currents", "spin/torsion/topological/edge currents absent, exact, zero-flux or separately retained", "OPEN_BLOCKER", "nonHilbert_current_zero_signed"),
        ("MQC4835_10_guard", "no qbar shortcut", "qbarXT=0 only by signed descent/superselection; otherwise first source row stays live", "GUARD_ACTIVE", "no_cancellation_guard"),
    ]
    return [
        {
            "clause_id": clause_id,
            "object": obj,
            "formula": formula,
            "current_result": result,
            "needed_signature_or_input": needed,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for clause_id, obj, formula, result, needed in rows
    ]


def qbar_contract(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("QBC4835_0_zero", "qbar_XT=0", "all matter quotient, constant, marker, source and current clauses signed", "conditional_only"),
        ("QBC4835_1_direct_bound", "qbar_XT_bound", "A_geom+A_theta+A_lift+A_marker+A_direct+A_worldtube+A_boundary+A_source_weight+A_nonHilbert", "runner_ready_values_missing"),
        ("QBC4835_2_component_bound", "qbarXT_vec", "P_A*(b_g+b_theta_alpha+b_theta_mass+b_m+b_kappa+b_NH+b_direct+b_worldtube+b_boundary)", "runner_ready_values_missing"),
        ("QBC4835_3_alpha", "alpha_source", "K_source*Qbar_source_XH_bound*qbar_XT_bound", "runner_ready_values_missing"),
        ("QBC4835_4_next", "theta derivative row", "d_ln_alpha_EM_dXhat and d_ln_mass_ratio_dXhat are the next constant-sector knife edge", "next_target"),
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
        "q_map_signed": "true",
        "observed_geometry_functor_signed": "true",
        "matter_functor_signed": "true",
        "constants_superselection_signed": "true",
        "no_material_marker_signed": "true",
        "matter_lift_signed": "true",
        "worldtube_support_signed": "true",
        "boundary_no_flux_signed": "true",
        "no_direct_matter_X_vertex_signed": "true",
        "universal_source_current_signed": "true",
        "nonHilbert_current_zero_signed": "true",
        "no_post_readout_EFT_signed": "true",
        "no_physical_charge_removed_signed": "true",
        "no_measured_GM_absorption_signed": "true",
    }
    direct = {
        "A_geom_matter_abs": "0.001",
        "A_theta_matter_abs": "0.002",
        "A_lift_matter_abs": "0.001",
        "A_marker_matter_abs": "0.001",
        "A_direct_matter_abs": "0.001",
        "A_worldtube_matter_abs": "0.001",
        "A_boundary_matter_abs": "0.001",
        "A_source_weight_abs": "0.0005",
        "A_nonHilbert_abs": "0.0005",
        "Qbar_source_XH_bound_abs": "0.01475",
        "K_source_abs": "1.5",
        "tau_BY5_qbar_abs": "2.0",
    }
    component = {
        "common_frame_log_derivative_abs": "0.001",
        "d_ln_alpha_EM_dXhat_abs": "0.0015",
        "d_ln_mass_ratio_dXhat_abs": "0.0005",
        "marker_coupling_projection_abs": "0.001",
        "species_source_weight_splitting_abs": "0.001",
        "nonHilbert_current_projection_abs": "0.001",
        "direct_vertex_projection_abs": "0.001",
        "worldtube_support_projection_abs": "0.001",
        "boundary_tail_projection_abs": "0.001",
        "P_A_qbarXT_vec_abs": "1.0",
        "Qbar_source_XH_bound_abs": "0.01475",
        "K_source_abs": "1.5",
        "tau_BY5_qbar_abs": "2.0",
    }
    doc_637 = str(SOURCES["637_doc"])
    doc_622 = str(SOURCES["622_doc"])
    source_618 = str(SOURCES["618_zero"])
    chain_2611 = str(SOURCES["2611_chain"])
    grammar_2612 = str(SOURCES["2612_grammar"])
    return [
        {
            "row_id": "RUN4835_0_live_qbarXT_zero_missing",
            "route_type": "qbarXT_zero",
            "route": "live matter quotient constant-sector zero audit",
            "source_path": doc_637,
            "equation_ref": "OF637_1_chain_rule;CO637_0_descent_criterion",
            "notes": "current MTS lacks parent q-map, observed geometry functor, constants superselection, marker taxonomy, source universality and no-direct-vertex signatures",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4835_1_conditional_qbarXT_zero_pass",
            "route_type": "qbarXT_zero",
            "route": "conditional parent signed matter quotient and constants zero",
            "source_path": source_618,
            "equation_ref": "SZ618_0_qbar_XT_chain_rule",
            "notes": "nonclaim theorem-shape smoke row",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4835_2_forbidden_constants_silent_assertion",
            "route_type": "qbarXT_zero",
            "route": "forbidden constants silent by assertion",
            "source_path": doc_637,
            "equation_ref": "CO637_0_descent_criterion",
            "notes": "CONSTANTS_SILENT_BY_ASSERTION cannot close theta_A",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4835_3_live_qbarXT_bound_missing",
            "route_type": "direct_qbarXT_bound",
            "route": "live first qbarXT source row missing",
            "source_path": chain_2611,
            "equation_ref": "CR2611_0_variation_identity;CR2611_2_constants",
            "notes": "matter descent/source row schema exists but no source-backed coefficients are filled",
            **base,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4835_4_direct_qbarXT_smoke_pass",
            "route_type": "direct_qbarXT_bound",
            "route": "direct finite qbarXT bound smoke",
            "source_path": chain_2611,
            "equation_ref": "CR2611_0_variation_identity",
            "notes": "nonclaim arithmetic smoke for matter descent plus constants/marker residuals",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4835_5_component_qbarXT_smoke_pass",
            "route_type": "component_qbarXT_bound",
            "route": "component finite qbarXT vector smoke",
            "source_path": doc_622,
            "equation_ref": "SP622_1_alpha_EM;SP622_2_mass_ratio",
            "notes": "nonclaim arithmetic smoke using 621/622 normal-form component basis",
            **base,
            **component,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4835_6_forbidden_closure_only_quotient",
            "route_type": "qbarXT_zero",
            "route": "forbidden closure-only quotient",
            "source_path": doc_637,
            "equation_ref": "QM637_2_vertical_kernel",
            "notes": "CLOSURE_ONLY_QUOTIENT cannot close matter constants or markers",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4835_7_forbidden_hidden_frame_ignored",
            "route_type": "direct_qbarXT_bound",
            "route": "forbidden hidden frame ignored",
            "source_path": doc_637,
            "equation_ref": "OF637_2_counterexample_filter",
            "notes": "HIDDEN_FRAME_IGNORED cannot zero common-frame coupling",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4835_8_forbidden_marker_ignored",
            "route_type": "direct_qbarXT_bound",
            "route": "forbidden marker ignored",
            "source_path": doc_622,
            "equation_ref": "PMC622_3_marker_taxonomy",
            "notes": "MARKER_IGNORED cannot close material marker coupling",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4835_9_forbidden_direct_vertex_dropped",
            "route_type": "direct_qbarXT_bound",
            "route": "forbidden direct matter vertex dropped",
            "source_path": grammar_2612,
            "equation_ref": "NDV2612_4_current_verdict",
            "notes": "DIRECT_VERTEX_DROPPED cannot replace the parent grammar theorem",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4835_10_forbidden_qbar_policy_only",
            "route_type": "component_qbarXT_bound",
            "route": "forbidden qbar zero by policy only",
            "source_path": doc_622,
            "equation_ref": "RU622_0_allowed",
            "notes": "QBAR_ZERO_BY_POLICY_ONLY cannot promote the parent matter contract",
            **base,
            **component,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4835_11_forbidden_measured_GM_source",
            "route_type": "component_qbarXT_bound",
            "route": "forbidden measured GM source",
            "source_path": doc_622,
            "equation_ref": "AR622_0_R10",
            "notes": "MEASURED_GM_AS_SOURCE cannot normalize qbarXT",
            **base,
            **component,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4835_12_forbidden_cancellation",
            "route_type": "component_qbarXT_bound",
            "route": "forbidden cancellation of unknown qbar components",
            "source_path": doc_622,
            "equation_ref": "qbarXT_vec_zero_promoted",
            "notes": "CANCEL_UNKNOWN_COMPONENTS cannot make qbarXT small",
            **base,
            **component,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4835_13_forbidden_GR_import",
            "route_type": "qbarXT_zero",
            "route": "forbidden GR import of matter quotient",
            "source_path": doc_622,
            "equation_ref": "PMC622_8_contract_verdict",
            "notes": "GR_IMPORT cannot replace parent MTS matter grammar",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
    ]


def decisions(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DEC4835_0_zero", "Matter quotient and constant-sector qbarXT zero is still unsigned for live MTS.", "The quotient chain-rule is clean, but observed geometry, constants, markers, matter lift, worldtube support and source-current clauses are not all parent-owned.", "keep qbarXT zero nonclaim", False),
        ("DEC4835_1_bound", "The first qbarXT source row is now executable.", "If descent fails, qbarXT is the absolute sum of matter, constants, marker, direct, support, boundary, source-weight and non-Hilbert residuals.", "source or theorem-zero each qbar component", False),
        ("DEC4835_2_next", "The next target should attack constant superselection first.", "The geometry leg is conditional and the constants leg hits EM, masses, clocks and WEP, making it the cleanest next knife-edge.", NEXT_TARGET, False),
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
        ("CG4835_0_runner_installed", "matter/constant qbarXT gate is executable", True, "runner computes qbar-zero, direct qbar bound and component qbar vector routes", False),
        ("CG4835_1_zero_unsigned", "qbarXT is theorem-zero for live MTS", False, "live matter quotient, constants, marker and source-current clauses are unsigned", False),
        ("CG4835_2_bound_ready", "finite qbarXT source row is staged", True, "smoke rows compute qbar, alpha and BY5 from retained components", False),
        ("CG4835_3_no_shortcuts", "asserted constants, closure quotient, hidden frame, ignored marker, dropped vertex, policy-only qbar, measured GM, cancellation and GR import fail closed", True, "forbidden rows return FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", False),
        ("CG4835_4_no_local_claim", "local GR/Newton/R10/WEP/PPN claims remain blocked", True, "no live row allows a claim", False),
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
            "objective": "derive constant superselection for EM/masses/clocks or stage first theta-derivative source row",
            "include": "alpha_EM, mass ratios, clock transitions, representation labels, material constants, d_ln theta/dXhat bounds, source paths, units",
            "exclude": "constants silent by assertion, unit rescaling that changes dimensionless observables, measured GM denominator, cancellation, GR import",
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
        "RUN4835_0_live_qbarXT_zero_missing": "BLOCKED_QBARXT_ZERO_CLAUSES",
        "RUN4835_1_conditional_qbarXT_zero_pass": "QBARXT_ZERO_PASS_NONCLAIM",
        "RUN4835_2_forbidden_constants_silent_assertion": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4835_3_live_qbarXT_bound_missing": "BLOCKED_DIRECT_QBARXT_BOUND_INPUTS",
        "RUN4835_4_direct_qbarXT_smoke_pass": "DIRECT_QBARXT_BOUND_PASS_NONCLAIM",
        "RUN4835_5_component_qbarXT_smoke_pass": "COMPONENT_QBARXT_BOUND_PASS_NONCLAIM",
        "RUN4835_6_forbidden_closure_only_quotient": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4835_7_forbidden_hidden_frame_ignored": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4835_8_forbidden_marker_ignored": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4835_9_forbidden_direct_vertex_dropped": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4835_10_forbidden_qbar_policy_only": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4835_11_forbidden_measured_GM_source": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4835_12_forbidden_cancellation": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4835_13_forbidden_GR_import": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
    }
    direct = by_id.get("RUN4835_4_direct_qbarXT_smoke_pass", {})
    component = by_id.get("RUN4835_5_component_qbarXT_smoke_pass", {})
    forbidden_ids = [
        "RUN4835_2_forbidden_constants_silent_assertion",
        "RUN4835_6_forbidden_closure_only_quotient",
        "RUN4835_7_forbidden_hidden_frame_ignored",
        "RUN4835_8_forbidden_marker_ignored",
        "RUN4835_9_forbidden_direct_vertex_dropped",
        "RUN4835_10_forbidden_qbar_policy_only",
        "RUN4835_11_forbidden_measured_GM_source",
        "RUN4835_12_forbidden_cancellation",
        "RUN4835_13_forbidden_GR_import",
    ]
    checks = [
        ("VAL4835_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        ("VAL4835_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ("VAL4835_02_output_count", len(outputs) == len(expected), "all runner rows emitted"),
        ("VAL4835_03_expected_statuses", all(by_id.get(row_id, {}).get("runner_status") == status for row_id, status in expected.items()), "runner statuses match expected pass/block/fail modes"),
        ("VAL4835_04_live_zero_blocked", by_id["RUN4835_0_live_qbarXT_zero_missing"]["runner_status"] == "BLOCKED_QBARXT_ZERO_CLAUSES", "live qbarXT zero remains blocked"),
        ("VAL4835_05_live_bound_blocked", by_id["RUN4835_3_live_qbarXT_bound_missing"]["runner_status"] == "BLOCKED_DIRECT_QBARXT_BOUND_INPUTS", "live first qbarXT row remains missing"),
        ("VAL4835_06_direct_smoke_pass", close_to(direct.get("matter_descent_residual_abs"), 0.006) and close_to(direct.get("constant_marker_residual_abs"), 0.003) and close_to(direct.get("qbar_XT_bound_abs"), 0.009) and close_to(direct.get("alpha_source_abs"), 0.000199125) and close_to(direct.get("BY5_qbar_feed_abs"), 0.018), "direct qbarXT smoke computes matter/constant split and alpha"),
        ("VAL4835_07_component_smoke_pass", close_to(component.get("matter_descent_residual_abs"), 0.006) and close_to(component.get("constant_marker_residual_abs"), 0.003) and close_to(component.get("qbar_XT_bound_abs"), 0.009), "component qbarXT smoke matches direct envelope"),
        ("VAL4835_08_forbidden_routes_fail", all(by_id[row_id]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE" for row_id in forbidden_ids), "forbidden shortcuts fail closed"),
        ("VAL4835_09_no_claim_allowed", not any(str(row.get("claim_allowed", "")).lower() == "true" for row in outputs), "no runner row allows a claim"),
        ("VAL4835_10_runner_compiles", True, "runner compiled before execution"),
        ("VAL4835_11_next_target_written", NEXT_TARGET_CSV.exists(), "next target CSV written"),
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
    doc = f"""# 4835 Y5 R2FR matter quotient constant sector or first qbarXT source row

**Status:** 4835 makes the test-body coupling leg executable. The quotient chain-rule can kill geometry coupling, but `qbar_XT=0` still needs parent-signed observed geometry, matter grammar, constants, markers, source support, source-current and non-Hilbert current clauses. Otherwise the first `qbar_XT` source row is retained.

**Decision:** `{DECISION}`.

**Claim ceiling:** no local-GR, Newtonian, R10, WEP, PPN, clock, EM, source-charge, qbar-zero, or matter-quotient claim is allowed from 4835.

## Core derivation

```text
S_matter = Sbar_m[Obs(q(Phi)), Psi, theta_A]
Dq[v_X] = 0

delta_v S_matter =
  (delta Sbar_m/dE_obs) DObs(Dq[v_X])
  + (partial Sbar_m/partial theta_A) delta_v theta_A
  + marker/lift/worldtube/boundary/direct-current terms

qbar_XT_bound =
  A_geom + A_theta + A_lift + A_marker + A_direct
  + A_worldtube + A_boundary + A_source_weight + A_nonHilbert

alpha_source = K_source Qbar_source_XH_bound qbar_XT_bound
```

## Source register

{md_table(sources, ["source_id", "exists", "needle_found", "role"])}

## qbarXT zero audit

{md_table(audit, ["clause_id", "object", "current_result", "needed_signature_or_input"])}

## qbarXT source-row contract

{md_table(contract, ["contract_id", "quantity", "definition", "status"])}

## Runner output

{md_table(outputs, ["row_id", "runner_status", "matter_descent_residual_abs", "constant_marker_residual_abs", "qbar_XT_bound_abs", "alpha_source_abs", "BY5_qbar_feed_abs", "missing_for_claim"])}

## Decision ledger

{md_table(decision_rows, ["decision_id", "decision", "because", "next_action"])}

## Validation

{md_table(validation, ["validation_id", "result", "detail"])}

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    formal = f"""# 851 PPC4161 matter quotient constant sector or first qbarXT source row

Checkpoint: `{DOC_PATH}`

4835 turns the test-body source leg into an owner-or-bound gate. If matter descends through observed quotient geometry and constants/markers/source currents are parent-superselected, `qbar_XT=0` conditionally follows. If not, `qbar_XT_bound` is the absolute sum of retained matter and constant/source residuals.

Decision: `{DECISION}`

Runner: `{RUNNER}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_claims(timestamp: str) -> None:
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "matter_quotient_constant_sector_or_first_qbarXT_source_row",
        "current_evidence": "4835 turns matter quotient and constant-sector descent into an executable qbarXT zero-or-source-row runner; live qbarXT zero and live source-backed qbar rows remain missing.",
        "status": "matter_constant_qbarXT_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "observed geometry functor, constants, markers, source support, direct matter vertex, source universality and non-Hilbert current clauses remain unsigned",
        "sector": "local_gr_Newton_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smoke rows pass but live qbarXT inputs are not source-backed",
        "title": "Matter quotient constant sector or first qbarXT source row",
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
        f"""## PPC4161 4835 matter quotient/constant qbarXT gate

`{MARKER}`. The test-body source leg is now explicit: quotient geometry can kill the geometric matter term, but constants, markers, source support, source weighting, direct matter vertices, boundary tails and non-Hilbert currents must be parent-signed or retained in `qbar_XT_bound`. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4835 matter quotient constant sector or first qbarXT source row

`{MARKER}` blocks qbar-by-slogan. Conditional zero needs parent-signed observed geometry, matter grammar, constants, marker taxonomy, support, source current, non-Hilbert current and no-direct-vertex clauses. If not, `qbar_XT_bound` feeds `alpha_source`. Next: `{NEXT_TARGET}`.""",
    )


def update_resume(timestamp: str) -> None:
    text = f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4835-Y5-R2FR-matter-quotient-constant-sector-or-first-qbarXT-source-row.md`
Marker: `{MARKER}`

## Where we are

4835 made the test-body coupling leg executable:

```text
S_matter = Sbar_m[Obs(q(Phi)), Psi, theta_A]
Dq[v_X]=0
delta_v S_matter = geometry pullback term + theta/constant term + marker/lift/worldtube/boundary/direct-current terms
qbar_XT_bound = A_geom + A_theta + A_lift + A_marker + A_direct + A_worldtube + A_boundary + A_source_weight + A_nonHilbert
alpha_source = K_source Qbar_source_XH_bound qbar_XT_bound
```

## Live blockers

- Observed geometry functor, matter grammar, constants, markers, matter lift, worldtube support, boundary tails, direct matter vertices, source universality and non-Hilbert current clauses are not signed together.
- `qbar_XT=0` remains conditional only; no local-GR/R10/WEP/PPN claim follows.
- Live coefficient rows for `A_theta`, `d_ln_alpha_EM_dXhat`, mass-ratio derivatives, marker/source weights and non-Hilbert currents remain missing.
- Constants silent by assertion, closure-only quotient, hidden-frame ignoring, marker ignoring, dropped matter vertex, policy-only qbar zero, measured/orbital `GM`, cancellation and GR import are forbidden.

## Next target

`{NEXT_TARGET}`
"""
    write_text(RESUME_PATH, text)


def main() -> int:
    timestamp = now()
    py_compile.compile(str(RUNNER), doraise=True)
    sources = source_register(timestamp)
    audit = qbar_audit(timestamp)
    contract = qbar_contract(timestamp)
    inputs = runner_inputs(timestamp)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(QBAR_AUDIT, audit)
    write_csv(QBAR_CONTRACT, contract)
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
        print(f"4835 validation failed: {failed}", file=sys.stderr)
        return 1
    print(f"{MARKER} complete")
    print(f"doc={DOC_PATH}")
    print(f"runner_output={RUNNER_OUTPUT}")
    print(f"validation={VALIDATION_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
