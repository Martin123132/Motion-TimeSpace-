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

CHECKPOINT = "4834"
CLAIM_ID = "L-676"
MARKER = "PPC4161_PARENT_THETA_OMEGA_DC_OPERATOR_OR_SOURCE_COUPLING_BOUND_ROW_4834"
PACKET_MARKER = "PPC4161_PACKET_PARENT_THETA_OMEGA_DC_OPERATOR_OR_SOURCE_COUPLING_BOUND_ROW_4834"
DECISION = "PARENT_THETA_OMEGA_DC_UNSIGNED_SOURCE_COUPLING_BOUND_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4835-Y5-R2FR-matter-quotient-constant-sector-or-first-qbarXT-source-row.md"

DOC_PATH = POST / "4834-Y5-R2FR-parent-theta-omega-DC-operator-or-source-coupling-bound-row.md"
FORMAL_PATH = FORMAL / "850-PPC4161-parent-theta-omega-DC-operator-or-source-coupling-bound-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "parent_theta_omega_DC_operator_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4834_SOURCE_REGISTER.csv"
OWNER_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4834_THETA_OMEGA_DC_OWNER_AUDIT.csv"
COUPLING_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4834_SOURCE_COUPLING_BOUND_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4834_THETA_OMEGA_DC_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4834_THETA_OMEGA_DC_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4834_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4834_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4834_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4834_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4834_VALIDATION.csv"

SOURCES = {
    "resume": RESUME_PATH,
    "4833_doc": POST / "4833-Y5-R2FR-parent-LThetaQ-boundary-momentum-or-first-bX-norm-row.md",
    "590_doc": POST / "590-Y5-R10-map-DCdagger-to-vertical-generator-or-fill-edge-row-source.md",
    "637_doc": POST / "637-Y5-R10-parent-action-quotient-map-and-constant-ownership-derivation.md",
    "669_doc": POST / "669-Y5-R10-minimal-LX-sector-operator-owner-or-retained-residual-vector.md",
    "591_dc": SOURCE_DIR / "P8_Y5_R10_591_DC_OPERATOR_FORMULA.csv",
    "591_dagger": SOURCE_DIR / "P8_Y5_R10_591_DCDAGGER_FORMULA.csv",
    "591_compare": SOURCE_DIR / "P8_Y5_R10_591_OMEGA_DCDAGGER_COMPARISON.csv",
    "590_fields": SOURCE_DIR / "P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv",
    "670_vertical": SOURCE_DIR / "P8_Y5_R10_670_VERTICAL_GENERATOR_CERTIFICATE.csv",
    "618_source_zero": SOURCE_DIR / "P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv",
    "637_qmap": SOURCE_DIR / "P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv",
    "669_theta": SOURCE_DIR / "P8_Y5_R10_669_THETA_QX_VARIATION_LEDGER.csv",
    "4833_output": SOURCE_DIR / "P8_Y5_R2FR_4833_PARENT_BOUNDARY_RUNNER_OUTPUT.csv",
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
        ("SRC4834_00_resume", SOURCES["resume"], "4834-Y5-R2FR-parent-theta-omega-DC-operator-or-source-coupling-bound-row.md", "4833 selected this Theta/Omega/DC target."),
        ("SRC4834_01_4833_doc", SOURCES["4833_doc"], "DEC4833_2_next", "parent LThetaQ handoff."),
        ("SRC4834_02_590_precise_map", SOURCES["590_doc"], "DVM590_3_precise_map", "DCdagger maps to Omega-flat, not directly to a vector."),
        ("SRC4834_03_590_omega_gate", SOURCES["590_doc"], "MCG590_0_parent_Omega", "parent Omega gate."),
        ("SRC4834_04_637_doc", SOURCES["637_doc"], "CO637_0_descent_criterion", "constant-sector descent criterion."),
        ("SRC4834_05_669_doc", SOURCES["669_doc"], "V669_6_yukawa_projection", "source-coupling coefficient route."),
        ("SRC4834_06_591_dc", SOURCES["591_dc"], "DC591_1_linearization_tensor_convention", "linearized DC operator."),
        ("SRC4834_07_591_boundary", SOURCES["591_dc"], "DC591_4_boundary_pairing", "DC boundary covector."),
        ("SRC4834_08_591_dagger", SOURCES["591_dagger"], "DCA591_4_compare_to_Omega_flat", "DCdagger/Omega-flat comparison."),
        ("SRC4834_09_591_compare", SOURCES["591_compare"], "CMP591_3_current_MTS_Omega", "Omega missing row."),
        ("SRC4834_10_591_verdict", SOURCES["591_compare"], "CMP591_5_verdict", "formal progress/no certificate verdict."),
        ("SRC4834_11_590_fields", SOURCES["590_fields"], "matter_readout", "field-by-field vertical action map."),
        ("SRC4834_12_670_omega", SOURCES["670_vertical"], "VGC670_0_parent_Omega", "vertical generator certificate."),
        ("SRC4834_13_670_matter", SOURCES["670_vertical"], "VGC670_6_matter_quotient", "matter quotient blocker."),
        ("SRC4834_14_618_source_zero", SOURCES["618_source_zero"], "SZ618_0_qbar_XT_chain_rule", "qbar_XT chain-rule theorem."),
        ("SRC4834_15_637_qmap", SOURCES["637_qmap"], "QM637_2_vertical_kernel", "vertical kernel quotient map."),
        ("SRC4834_16_669_theta", SOURCES["669_theta"], "V669_0_variation", "Theta_X variation ledger."),
        ("SRC4834_17_669_yukawa", SOURCES["669_theta"], "V669_6_yukawa_projection", "finite source coupling projection."),
        ("SRC4834_18_4833_output", SOURCES["4833_output"], "RUN4833_4_hodge_bX_norm_smoke_pass", "upstream b_X norm runner."),
        ("SRC4834_19_runner", SOURCES["runner"], "def evaluate_row", "4834 executable runner."),
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


def owner_audit(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("TOD4834_0_theta", "parent symplectic potential", "delta L_parent=E_A deltaY^A+d theta_Y(deltaY)", "UNSIGNED", "theta_Y_signed"),
        ("TOD4834_1_omega", "parent presymplectic form", "Omega_Y=delta theta_Y with controlled boundary terms", "UNSIGNED", "omega_Y_signed"),
        ("TOD4834_2_DC", "linearized constraint operator", "DC_X[deltaY] from C_X=-nabla P+J_eff including connection/volume terms", "FORMULA_ONLY", "DC_X_operator_signed"),
        ("TOD4834_3_DCadjoint", "adjoint covector", "<eta,DC_X[deltaY]>=<DC_X^dagger eta,deltaY>+B_DC", "FORMULA_ONLY", "DCdagger_formula_signed"),
        ("TOD4834_4_match", "Hamiltonian generator identity", "DC_X^dagger eta=Omega_Y^flat(v_eta) field-by-field", "NOT_CLOSED", "omega_flat_match_signed"),
        ("TOD4834_5_vertical", "vertical action on every field", "v_eta[g,Pi,Gamma,Khat,q_loc,memory,matter,boundary] declared and quotient-compatible", "PARTIAL", "vertical_action_all_fields_signed"),
        ("TOD4834_6_boundary", "differentiable boundary generator", "delta Q_X + delta B_ct cancels B_DC and leaves zero/proper/exact boundary charge", "NOT_DERIVED", "boundary_differentiability_signed;Bct_cancels_boundary_covector_signed"),
        ("TOD4834_7_matter", "ordinary matter/source descent", "delta_v S_matter=0 and delta_v theta_A=0, else qbar_XT is retained", "CONDITIONAL_ONLY", "matter_quotient_signed;constant_sector_descends_signed"),
        ("TOD4834_8_guard", "no category/circular shortcut", "DCdagger is a covector, measured GM is not a source, constants cannot be silent by assertion", "GUARD_ACTIVE", "no_cancellation_guard"),
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


def coupling_contract(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("SCC4834_0_owner_zero", "source_coupling_residual=0", "theta/Omega/DC owner plus matter and constant descent signs all local source legs to zero", "conditional_only"),
        ("SCC4834_1_direct_bound", "source_coupling_residual", "|Omega-DCdagger|+|unmapped v|+|B_DC|+|Bct mismatch|+|degeneracy|+|matter quotient|+|constant marker|", "runner_ready_values_missing"),
        ("SCC4834_2_qbarXT", "qbar_XT_bound", "|matter quotient residual|+|constant marker residual|", "runner_ready_values_missing"),
        ("SCC4834_3_Qbar", "Qbar_source_XH_bound", "PiM_norm*source_coupling_residual/M_H_ref_min", "runner_ready_values_missing"),
        ("SCC4834_4_alpha", "alpha_source", "K_source*Qbar_source_XH_bound*qbar_XT_bound", "runner_ready_values_missing"),
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
    owner = {
        "theta_Y_signed": "true",
        "omega_Y_signed": "true",
        "DC_X_operator_signed": "true",
        "DCdagger_formula_signed": "true",
        "omega_flat_match_signed": "true",
        "vertical_action_all_fields_signed": "true",
        "boundary_differentiability_signed": "true",
        "Bct_cancels_boundary_covector_signed": "true",
        "reduced_nondegeneracy_signed": "true",
        "matter_quotient_signed": "true",
        "constant_sector_descends_signed": "true",
        "no_physical_charge_removed_signed": "true",
        "no_measured_GM_absorption_signed": "true",
    }
    direct = {
        "omega_DC_mismatch_abs": "0.02",
        "unmapped_vertical_action_abs": "0.015",
        "boundary_covector_abs": "0.01",
        "Bct_mismatch_abs": "0.003",
        "reduced_degeneracy_residual_abs": "0.002",
        "matter_quotient_residual_abs": "0.005",
        "constant_marker_residual_abs": "0.004",
        "M_H_ref_min_abs": "2.0",
        "PiM_norm_abs": "0.5",
        "K_source_abs": "1.5",
        "tau_BY5_source_abs": "2.0",
    }
    component = {
        "theta_gap_abs": "0.006",
        "omega_gap_abs": "0.006",
        "DC_operator_gap_abs": "0.006",
        "DCdagger_gap_abs": "0.006",
        "omega_flat_match_gap_abs": "0.006",
        "vertical_map_gap_abs": "0.006",
        "boundary_differentiability_gap_abs": "0.006",
        "Bct_mismatch_abs": "0.008",
        "matter_descent_gap_abs": "0.005",
        "constant_descent_gap_abs": "0.004",
        "M_H_ref_min_abs": "2.0",
        "PiM_norm_abs": "0.5",
        "K_source_abs": "1.5",
        "tau_BY5_source_abs": "2.0",
    }
    doc_590 = str(SOURCES["590_doc"])
    compare_591 = str(SOURCES["591_compare"])
    source_618 = str(SOURCES["618_source_zero"])
    dc_591 = str(SOURCES["591_dc"])
    return [
        {
            "row_id": "RUN4834_0_live_theta_omega_DC_owner_missing",
            "route_type": "theta_omega_DC_owner",
            "route": "live parent theta/Omega/DC owner audit",
            "source_path": doc_590,
            "equation_ref": "MCG590_0_parent_Omega;MCG590_1_DCX_operator",
            "notes": "current MTS lacks signed theta, Omega, DC_X, vertical action, boundary differentiability, matter quotient and constants descent",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4834_1_conditional_theta_omega_DC_owner_pass",
            "route_type": "theta_omega_DC_owner",
            "route": "conditional parent signed theta/Omega/DC owner",
            "source_path": doc_590,
            "equation_ref": "DVM590_3_precise_map",
            "notes": "nonclaim theorem-shape smoke row",
            **base,
            **owner,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4834_2_forbidden_formula_only_theta",
            "route_type": "theta_omega_DC_owner",
            "route": "forbidden formula-only theta owner",
            "source_path": compare_591,
            "equation_ref": "CMP591_3_current_MTS_Omega",
            "notes": "FORMULA_ONLY_THETA cannot replace parent symplectic ownership",
            **base,
            **owner,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4834_3_live_source_coupling_missing",
            "route_type": "direct_source_coupling_bound",
            "route": "live first source-coupling residual bound missing",
            "source_path": source_618,
            "equation_ref": "SZ618_0_qbar_XT_chain_rule;SZ618_5_full_source_zero_certificate",
            "notes": "qbar_XT/Qbar/K_source rows remain missing or theorem-unsigned",
            **base,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4834_4_direct_source_coupling_smoke_pass",
            "route_type": "direct_source_coupling_bound",
            "route": "direct finite source-coupling smoke",
            "source_path": source_618,
            "equation_ref": "SZ618_0_qbar_XT_chain_rule",
            "notes": "nonclaim arithmetic smoke for retained source-coupling residual",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4834_5_component_source_coupling_smoke_pass",
            "route_type": "component_source_coupling_bound",
            "route": "component finite source-coupling smoke",
            "source_path": dc_591,
            "equation_ref": "DC591_4_boundary_pairing",
            "notes": "nonclaim arithmetic smoke for decomposed theta/Omega/DC/matter/constant residuals",
            **base,
            **component,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4834_6_forbidden_DCdagger_equals_vector",
            "route_type": "theta_omega_DC_owner",
            "route": "forbidden DCdagger equals vector shortcut",
            "source_path": doc_590,
            "equation_ref": "DVM590_3_precise_map",
            "notes": "DC_DAGGER_EQUALS_VECTOR is the category error 590 repaired",
            **base,
            **owner,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4834_7_forbidden_omega_by_analogy",
            "route_type": "theta_omega_DC_owner",
            "route": "forbidden Omega by GR analogy",
            "source_path": doc_590,
            "equation_ref": "GRA590_1_covariant_phase_space",
            "notes": "OMEGA_BY_ANALOGY cannot replace parent MTS Omega",
            **base,
            **owner,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4834_8_forbidden_DC_operator_inserted",
            "route_type": "direct_source_coupling_bound",
            "route": "forbidden inserted DC operator",
            "source_path": dc_591,
            "equation_ref": "DC591_3_parent_field_expansion",
            "notes": "DC_OPERATOR_INSERTED cannot replace P,J parent-field expansion",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4834_9_forbidden_constants_silent",
            "route_type": "direct_source_coupling_bound",
            "route": "forbidden constants silent by assertion",
            "source_path": source_618,
            "equation_ref": "SZ618_0_qbar_XT_chain_rule",
            "notes": "CONSTANTS_SILENT_BY_ASSERTION cannot close qbar_XT",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4834_10_forbidden_measured_GM_source",
            "route_type": "component_source_coupling_bound",
            "route": "forbidden measured GM source",
            "source_path": source_618,
            "equation_ref": "SZ618_5_full_source_zero_certificate",
            "notes": "MEASURED_GM_AS_SOURCE cannot normalize source coupling",
            **base,
            **component,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4834_11_forbidden_cancellation",
            "route_type": "component_source_coupling_bound",
            "route": "forbidden cancellation of unknown coupling pieces",
            "source_path": source_618,
            "equation_ref": "SZ618_5_full_source_zero_certificate",
            "notes": "CANCEL_UNKNOWN_COMPONENTS cannot prove source coupling small",
            **base,
            **component,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4834_12_forbidden_GR_import",
            "route_type": "theta_omega_DC_owner",
            "route": "forbidden GR import of theta/Omega/DC",
            "source_path": doc_590,
            "equation_ref": "GRA590_2_current_MTS_CX",
            "notes": "GR_IMPORT cannot replace parent MTS theta/Omega/DC",
            **base,
            **owner,
            "timestamp_utc": timestamp,
        },
    ]


def decisions(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DEC4834_0_owner", "Theta/Omega/DC ownership is still unsigned for live MTS.", "The category-correct identity is known, but theta, Omega, DC_X, vertical action, boundary differentiability, matter quotient and constants descent are not signed together.", "keep theorem-zero source coupling blocked", False),
        ("DEC4834_1_bound", "The first source-coupling residual bound is now executable.", "If owner descent fails, matter/constant coupling becomes qbar_XT_bound and source coupling is retained absolutely.", "source or theorem-zero qbar_XT/Qbar/K_source inputs", False),
        ("DEC4834_2_next", "The next derivation target should attack matter quotient plus constants.", "The test-body leg qbar_XT is now the cleanest coupling knife-edge after theta/Omega/DC.", NEXT_TARGET, False),
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
        ("CG4834_0_runner_installed", "theta/Omega/DC source-coupling gate is executable", True, "runner computes owner-zero, direct source-bound, and component source-bound routes", False),
        ("CG4834_1_owner_unsigned", "parent theta/Omega/DC owner is claim-ready", False, "live branch lacks signed theta/Omega/DC/vertical/boundary/matter/constant clauses", False),
        ("CG4834_2_source_bound_ready", "finite source-coupling row is staged", True, "smoke rows compute residual, qbar, Qbar, alpha and BY5", False),
        ("CG4834_3_no_shortcuts", "formula-only theta, Omega analogy, inserted DC, DCdagger-vector category error, asserted constants, measured GM, cancellation and GR import fail closed", True, "forbidden rows return FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", False),
        ("CG4834_4_no_local_claim", "local GR/Newton/R10/PPN claims remain blocked", True, "no live row allows a claim", False),
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
            "objective": "derive matter quotient and constant-sector silence, or stage first qbar_XT source row",
            "include": "matter action descent, observed geometry functor, alpha_EM/mass/clock constants, material labels, qbar_XT, Qbar_XH, K_source, source paths, units",
            "exclude": "constants silent by assertion, measured GM denominator, closure-only quotient, cancellation, GR import, local-GR/Newton/R10/PPN claim",
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
        "RUN4834_0_live_theta_omega_DC_owner_missing": "BLOCKED_THETA_OMEGA_DC_OWNER_CLAUSES",
        "RUN4834_1_conditional_theta_omega_DC_owner_pass": "THETA_OMEGA_DC_OWNER_PASS_NONCLAIM",
        "RUN4834_2_forbidden_formula_only_theta": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4834_3_live_source_coupling_missing": "BLOCKED_DIRECT_SOURCE_COUPLING_BOUND_INPUTS",
        "RUN4834_4_direct_source_coupling_smoke_pass": "DIRECT_SOURCE_COUPLING_BOUND_PASS_NONCLAIM",
        "RUN4834_5_component_source_coupling_smoke_pass": "COMPONENT_SOURCE_COUPLING_BOUND_PASS_NONCLAIM",
        "RUN4834_6_forbidden_DCdagger_equals_vector": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4834_7_forbidden_omega_by_analogy": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4834_8_forbidden_DC_operator_inserted": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4834_9_forbidden_constants_silent": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4834_10_forbidden_measured_GM_source": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4834_11_forbidden_cancellation": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4834_12_forbidden_GR_import": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
    }
    direct = by_id.get("RUN4834_4_direct_source_coupling_smoke_pass", {})
    component = by_id.get("RUN4834_5_component_source_coupling_smoke_pass", {})
    forbidden_ids = [
        "RUN4834_2_forbidden_formula_only_theta",
        "RUN4834_6_forbidden_DCdagger_equals_vector",
        "RUN4834_7_forbidden_omega_by_analogy",
        "RUN4834_8_forbidden_DC_operator_inserted",
        "RUN4834_9_forbidden_constants_silent",
        "RUN4834_10_forbidden_measured_GM_source",
        "RUN4834_11_forbidden_cancellation",
        "RUN4834_12_forbidden_GR_import",
    ]
    checks = [
        ("VAL4834_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        ("VAL4834_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ("VAL4834_02_output_count", len(outputs) == len(expected), "all runner rows emitted"),
        ("VAL4834_03_expected_statuses", all(by_id.get(row_id, {}).get("runner_status") == status for row_id, status in expected.items()), "runner statuses match expected pass/block/fail modes"),
        ("VAL4834_04_live_owner_blocked", by_id["RUN4834_0_live_theta_omega_DC_owner_missing"]["runner_status"] == "BLOCKED_THETA_OMEGA_DC_OWNER_CLAUSES", "live theta/Omega/DC owner remains blocked"),
        ("VAL4834_05_live_bound_blocked", by_id["RUN4834_3_live_source_coupling_missing"]["runner_status"] == "BLOCKED_DIRECT_SOURCE_COUPLING_BOUND_INPUTS", "live source-coupling bound row remains missing"),
        ("VAL4834_06_direct_smoke_pass", close_to(direct.get("source_coupling_residual_abs"), 0.059) and close_to(direct.get("qbar_XT_bound_abs"), 0.009) and close_to(direct.get("Qbar_source_XH_bound_abs"), 0.01475) and close_to(direct.get("alpha_source_abs"), 0.000199125) and close_to(direct.get("BY5_source_feed_abs"), 0.0295), "direct source-coupling smoke computes residual/qbar/Qbar/alpha/BY5"),
        ("VAL4834_07_component_smoke_pass", close_to(component.get("source_coupling_residual_abs"), 0.059) and close_to(component.get("qbar_XT_bound_abs"), 0.009) and close_to(component.get("Qbar_source_XH_bound_abs"), 0.01475), "component source-coupling smoke matches direct envelope"),
        ("VAL4834_08_forbidden_routes_fail", all(by_id[row_id]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE" for row_id in forbidden_ids), "forbidden shortcuts fail closed"),
        ("VAL4834_09_no_claim_allowed", not any(str(row.get("claim_allowed", "")).lower() == "true" for row in outputs), "no runner row allows a claim"),
        ("VAL4834_10_runner_compiles", True, "runner compiled before execution"),
        ("VAL4834_11_next_target_written", NEXT_TARGET_CSV.exists(), "next target CSV written"),
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
    doc = f"""# 4834 Y5 R2FR parent theta omega DC operator or source coupling bound row

**Status:** 4834 makes the actual coupling hinge executable. The category-correct owner identity is `DC_X^dagger eta = Omega_Y^flat(v_eta)`. Current MTS has not signed the parent `theta/Omega/DC/vertical/matter/constants` chain, so the fallback is an explicit source-coupling residual bound.

**Decision:** `{DECISION}`.

**Claim ceiling:** no local-GR, Newtonian, R10, R11, PPN, source-charge, source-coupling-zero, or qbar/theta/Omega/DC claim is allowed from 4834.

## Core derivation

```text
delta L_parent = E_A deltaY^A + d theta_Y(deltaY)
Omega_Y = delta theta_Y
delta G_eta[deltaY] = <eta, DC_X[deltaY]> + delta Q_X
                    = <DC_X^dagger eta, deltaY> + B_DC[eta,deltaY]
Hamiltonian owner condition:
    DC_X^dagger eta = Omega_Y^flat(v_eta)

source_coupling_residual =
    |Omega-DCdagger| + |unmapped v| + |B_DC| + |B_ct mismatch|
    + |reduced degeneracy| + |delta_v S_matter| + |delta_v theta_A|

qbar_XT_bound = |delta_v S_matter| + |delta_v theta_A|
Qbar_source_XH_bound <= PiM_norm source_coupling_residual/M_H_ref_min
alpha_source = K_source Qbar_source_XH_bound qbar_XT_bound
```

## Source register

{md_table(sources, ["source_id", "exists", "needle_found", "role"])}

## Theta/Omega/DC owner audit

{md_table(audit, ["clause_id", "object", "current_result", "needed_signature_or_input"])}

## Source-coupling contract

{md_table(contract, ["contract_id", "quantity", "definition", "status"])}

## Runner output

{md_table(outputs, ["row_id", "runner_status", "source_coupling_residual_abs", "Qbar_source_XH_bound_abs", "qbar_XT_bound_abs", "alpha_source_abs", "BY5_source_feed_abs", "missing_for_claim"])}

## Decision ledger

{md_table(decision_rows, ["decision_id", "decision", "because", "next_action"])}

## Validation

{md_table(validation, ["validation_id", "result", "detail"])}

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    formal = f"""# 850 PPC4161 parent theta omega DC operator or source coupling bound row

Checkpoint: `{DOC_PATH}`

4834 makes the coupling hinge explicit: `DC_X^dagger eta = Omega_Y^flat(v_eta)` is the parent owner identity. If that chain and matter/constants descent are not signed, the retained branch stores `source_coupling_residual`, `qbar_XT_bound`, `Qbar_source_XH_bound`, and `alpha_source`.

Decision: `{DECISION}`

Runner: `{RUNNER}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_claims(timestamp: str) -> None:
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "parent_theta_omega_DC_operator_or_source_coupling_bound_row",
        "current_evidence": "4834 turns the theta/Omega/DC parent owner identity and matter/constants source coupling into an executable zero-or-bound runner; live owner and live source-coupling rows remain missing.",
        "status": "theta_omega_DC_source_coupling_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "parent theta/Omega/DC/vertical boundary identity plus matter quotient and constant-sector descent remain unsigned",
        "sector": "local_gr_Newton_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smoke rows pass but live source-coupling inputs are not source-backed",
        "title": "Parent theta omega DC operator or source coupling bound row",
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
        f"""## PPC4161 4834 parent theta/Omega/DC source-coupling gate

`{MARKER}`. The local coupling hinge is now the category-correct identity `DC_X^dagger eta = Omega_Y^flat(v_eta)`. If parent `theta/Omega/DC`, vertical action, boundary differentiability, matter quotient, and constant descent are signed, the local source leg can theorem-zero; otherwise the source-coupling residual is retained as an explicit bound feeding `qbar_XT`, `Qbar_source_XH`, and `alpha_source`. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4834 parent theta/Omega/DC or source-coupling bound row

`{MARKER}` puts the coupling under a hard owner-or-bound gate. Formula-only theta, Omega by analogy, inserted DC, DCdagger-as-vector, constants-silent-by-assertion, measured GM, cancellation and GR import fail closed. Next: `{NEXT_TARGET}`.""",
    )


def update_resume(timestamp: str) -> None:
    text = f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4834-Y5-R2FR-parent-theta-omega-DC-operator-or-source-coupling-bound-row.md`
Marker: `{MARKER}`

## Where we are

4834 made the actual source-coupling hinge executable:

```text
delta L = E deltaY + d theta_Y
Omega_Y = delta theta_Y
delta G_eta = <eta,DC_X[deltaY]> + delta Q_X
DC_X^dagger eta = Omega_Y^flat(v_eta)
source_coupling_residual = |Omega-DCdagger| + |unmapped v| + |B_DC/B_ct| + |matter quotient| + |constant marker|
qbar_XT_bound = matter_quotient_residual + constant_marker_residual
alpha_source = K_source Qbar_source_XH_bound qbar_XT_bound
```

## Live blockers

- Parent `theta_Y`, `Omega_Y`, `DC_X`, `DC_X^dagger`, vertical action, reduced nondegeneracy, and boundary differentiability are not signed together.
- Matter quotient descent and constant-sector descent remain conditional, so `qbar_XT` is not theorem-zero.
- Live `K_source`, `Qbar_source_XH`, `qbar_XT`, `M_H_ref_min`, and units/source paths remain missing.
- Formula-only theta, Omega by analogy, inserted DC, DCdagger-as-vector, constants silent by assertion, measured/orbital `GM`, GR import and cancellation routes are explicitly forbidden.

## Next target

`{NEXT_TARGET}`
"""
    write_text(RESUME_PATH, text)


def main() -> int:
    timestamp = now()
    py_compile.compile(str(RUNNER), doraise=True)
    sources = source_register(timestamp)
    audit = owner_audit(timestamp)
    contract = coupling_contract(timestamp)
    inputs = runner_inputs(timestamp)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(OWNER_AUDIT, audit)
    write_csv(COUPLING_CONTRACT, contract)
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
        print(f"4834 validation failed: {failed}", file=sys.stderr)
        return 1
    print(f"{MARKER} complete")
    print(f"doc={DOC_PATH}")
    print(f"runner_output={RUNNER_OUTPUT}")
    print(f"validation={VALIDATION_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
