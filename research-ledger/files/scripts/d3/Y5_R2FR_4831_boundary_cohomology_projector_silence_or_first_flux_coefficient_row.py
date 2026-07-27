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

CHECKPOINT = "4831"
CLAIM_ID = "L-673"
MARKER = "PPC4161_BOUNDARY_COHOMOLOGY_PROJECTOR_SILENCE_OR_FIRST_FLUX_COEFFICIENT_ROW_4831"
PACKET_MARKER = "PPC4161_PACKET_BOUNDARY_COHOMOLOGY_PROJECTOR_SILENCE_OR_FIRST_FLUX_COEFFICIENT_ROW_4831"
DECISION = "BOUNDARY_PROJECTOR_ZERO_UNSIGNED_FIRST_FLUX_COEFFICIENT_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4832-Y5-R2FR-BX-primitive-cocycle-zero-or-first-edge-source-row.md"

DOC_PATH = POST / "4831-Y5-R2FR-boundary-cohomology-projector-silence-or-first-flux-coefficient-row.md"
FORMAL_PATH = FORMAL / "847-PPC4161-boundary-cohomology-projector-silence-or-first-flux-coefficient-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "boundary_projector_flux_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4831_SOURCE_REGISTER.csv"
ZERO_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4831_BOUNDARY_PROJECTOR_ZERO_AUDIT.csv"
BOUND_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4831_FLUX_COEFFICIENT_BOUND_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4831_FLUX_COEFFICIENT_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4831_FLUX_COEFFICIENT_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4831_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4831_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4831_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4831_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4831_VALIDATION.csv"

SOURCES = {
    "resume": RESUME_PATH,
    "4830_doc": POST / "4830-Y5-R2FR-Hamiltonian-PiM-reference-lock-or-first-Delta-symp-row.md",
    "549_doc": POST / "549-Y5-boundary-cohomology-nohair-certificate-or-boundary-flux-bound-fill.md",
    "550_doc": POST / "550-Y5-projector-symplectic-silence-certificate-or-commutator-bound-fill.md",
    "1019_doc": POST / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
    "bct549": SOURCE_DIR / "P8_Y5_BRR545_BOUNDARY_COHOMOLOGY_NOHAIR_THEOREM_ATTEMPT.csv",
    "fb549": SOURCE_DIR / "P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv",
    "pst550": SOURCE_DIR / "P8_Y5_BRR545_PROJECTOR_SYMPLECTIC_SILENCE_THEOREM_ATTEMPT.csv",
    "fb550": SOURCE_DIR / "P8_Y5_BRR545_COMMUTATOR_PROJECTOR_BOUND_FILL_ROW.csv",
    "be1019": SOURCE_DIR / "P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv",
    "po1019": SOURCE_DIR / "P8_Y5_R10_1019_PROJECTOR_ORTHOGONALITY_CLAUSES.csv",
    "sp1019": SOURCE_DIR / "P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv",
    "delta_symp_output": SOURCE_DIR / "P8_Y5_R2FR_4830_DELTA_SYMP_RUNNER_OUTPUT.csv",
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
        ("SRC4831_00_resume", SOURCES["resume"], "4831-Y5-R2FR-boundary-cohomology-projector-silence-or-first-flux-coefficient-row.md", "4830 selected this boundary/projector target."),
        ("SRC4831_01_4830_doc", SOURCES["4830_doc"], "DEC4830_2_next", "current Delta_symp handoff."),
        ("SRC4831_02_549_doc", SOURCES["549_doc"], "BCT549_6_certificate_verdict", "boundary cohomology/no-hair attempt."),
        ("SRC4831_03_550_doc", SOURCES["550_doc"], "PST550_7_certificate_verdict", "projector symplectic silence attempt."),
        ("SRC4831_04_1019_doc", SOURCES["1019_doc"], "RVT1019_1_projector_orthogonality", "boundary/projector route verdict."),
        ("SRC4831_05_bct549", SOURCES["bct549"], "BCT549_4_volume_no_flux_not_alpha3_no_flux", "boundary no-hair obstruction."),
        ("SRC4831_06_fb549", SOURCES["fb549"], "FB549_0_boundary_flux_bound", "boundary flux fallback row."),
        ("SRC4831_07_pst550", SOURCES["pst550"], "PST550_4_variation_stress", "projector variation/stress obstruction."),
        ("SRC4831_08_fb550", SOURCES["fb550"], "FB550_0_commutator_projector_bound", "commutator/projector fallback row."),
        ("SRC4831_09_be1019", SOURCES["be1019"], "BE1019_1_BX_exact", "boundary exactness clauses."),
        ("SRC4831_10_po1019", SOURCES["po1019"], "PO1019_1_edge_mass_independence", "projector orthogonality clauses."),
        ("SRC4831_11_sp1019", SOURCES["sp1019"], "SP1019_6_projector_zero_or_bound", "source-pack schema."),
        ("SRC4831_12_4830_output", SOURCES["delta_symp_output"], "RUN4830_5_component_FB5540_smoke_pass", "upstream Delta_symp runner feed."),
        ("SRC4831_13_runner", SOURCES["runner"], "def evaluate_row", "4831 executable runner."),
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
        ("BPZ4831_0_domain", "compact corner-free boundary domain", "partial Sigma closed, corner terms absent, edge cohomology controlled", "NOT_PARENT_SIGNED", "Delta_domain_boundary row"),
        ("BPZ4831_1_relative_class", "relative boundary class is trivial or separately projected", "[B_imp]=0 in allowed relative cohomology before readout", "CONDITIONAL_ONLY", "B_zero_flux row"),
        ("BPZ4831_2_Bprimitive", "boundary momentum/improvement has a parent primitive", "B_imp=d_boundary b_X with fixed reference/counterterm", "NOT_DERIVED", "B_X primitive/source row"),
        ("BPZ4831_3_kernel", "range/kernel derivative does not reintroduce edge flux", "d_boundary(F_lambda epsilon)=0 or retained kernel derivative term", "FAIL_OPEN", "kernel_derivative_flux row"),
        ("BPZ4831_4_nohair", "boundary has no vector/tensor/shear/marker hair", "T_B^TF=T_B^vector=n_mu P_loc_nu T_B^{mu nu}=0", "FAIL_OPEN", "boundary_vector/tensor/marker rows"),
        ("BPZ4831_5_projector_definition", "Pi_M^H is defined at fixed observed source frame", "Pi_M^H[f]=partial f/partial M_H_ref at fixed tau, surface, reference and boundary class", "FORMAL_ONLY", "projector definition certificate"),
        ("BPZ4831_6_edge_mass_independence", "edge charge is mass/source independent", "partial Q_edge/partial M_H_ref=0", "NOT_DERIVED", "PiM_Q_edge row"),
        ("BPZ4831_7_symplectic_block", "source and edge sectors are symplectically orthogonal", "Omega(delta_M Phi,delta_edge Phi)=0", "NOT_DERIVED", "projector_boundary_flux row"),
        ("BPZ4831_8_no_double_count", "bulk, edge, FB5540 and R11 components are non-overlapping", "absolute envelope until projectors/source split are signed", "GUARD_WRITTEN", "component no-cancellation pack"),
        ("BPZ4831_9_anti_circularity", "no symbolic edge zero, closure-only quotient, measured GM or cancellation", "edge/projector terms vanish only by theorem-zero or source-backed coefficients", "POLICY_GUARD", "forbidden-source guard"),
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
        ("BPC4831_0_zero", "epsilon_boundary_projector=0", "boundary exactness/no-hair plus projector orthogonality signed in one branch", "conditional_only"),
        ("BPC4831_1_direct_flux", "sum first boundary/projector flux coefficients/M_H_ref", "B_zero + vector/tensor + kernel derivative + projector boundary + PiM_Q_edge + K_boundary", "runner_ready_values_missing"),
        ("BPC4831_2_component_pack", "full boundary/projector no-cancellation envelope/M_H_ref", "direct flux plus shear, marker, counterterm, commutator, projector variation, domain motion", "runner_ready_values_missing"),
        ("BPC4831_3_observable", "C_i epsilon_boundary_projector and tau_BY5 epsilon_boundary_projector", "maps retained flux to beta/gamma/alpha3/xi and BY5/source-normalization", "runner_ready_values_missing"),
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
    doc_1019 = str(SOURCES["1019_doc"])
    fb549 = str(SOURCES["fb549"])
    fb550 = str(SOURCES["fb550"])
    base = {
        "source_signed": "true",
        "units_signed": "true",
        "same_branch_signed": "true",
        "no_cancellation_guard": "true",
    }
    zero = {
        "compact_corner_free_domain_signed": "true",
        "relative_cohomology_trivial_signed": "true",
        "B_imp_exact_primitive_signed": "true",
        "kernel_derivative_zero_signed": "true",
        "no_vector_tensor_boundary_hair_signed": "true",
        "boundary_reference_silent_signed": "true",
        "projector_definition_signed": "true",
        "edge_mass_independence_signed": "true",
        "source_edge_symplectic_orthogonal_signed": "true",
        "PiM_reference_silence_signed": "true",
        "no_double_count_split_signed": "true",
        "M_H_ref_positive_signed": "true",
        "no_readout_mask_signed": "true",
        "no_measured_GM_absorption_signed": "true",
    }
    direct = {
        "M_H_ref_abs": "2.0",
        "B_zero_flux_abs": "0.02",
        "boundary_vector_flux_abs": "0.01",
        "boundary_tensor_flux_abs": "0.01",
        "kernel_derivative_flux_abs": "0.005",
        "projector_boundary_flux_abs": "0.03",
        "PiM_Q_edge_abs": "0.02",
        "K_boundary_abs": "0.01",
        "C_beta_flux_abs": "1.2",
        "C_gamma_flux_abs": "1.1",
        "C_alpha3_flux_abs": "0.5",
        "C_xi_flux_abs": "0.4",
        "tau_BY5_boundary_abs": "2.0",
    }
    component = {
        **direct,
        "boundary_shear_flux_abs": "0.005",
        "boundary_marker_flux_abs": "0.005",
        "boundary_counterterm_flux_abs": "0.005",
        "projector_commutator_abs": "0.02",
        "projector_variation_abs": "0.02",
        "Delta_domain_boundary_abs": "0.01",
    }
    return [
        {
            "row_id": "RUN4831_0_live_boundary_projector_zero_missing",
            "route_type": "boundary_projector_zero",
            "route": "live boundary/projector zero audit",
            "source_path": doc_1019,
            "equation_ref": "RVT1019_4_verdict",
            "notes": "current MTS lacks signed boundary domain, B primitive, no-hair, projector orthogonality and no-double-count clauses",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4831_1_conditional_boundary_projector_zero_pass",
            "route_type": "boundary_projector_zero",
            "route": "conditional parent-signed boundary/projector zero",
            "source_path": doc_1019,
            "equation_ref": "BE1019_6_verdict;PO1019_5_verdict",
            "notes": "nonclaim theorem-shape smoke row",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4831_2_forbidden_symbolic_edge_zero",
            "route_type": "boundary_projector_zero",
            "route": "forbidden symbolic edge zero",
            "source_path": doc_1019,
            "equation_ref": "CG1019_7_guardrail",
            "notes": "SYMBOLIC_EDGE_ZERO cannot replace boundary exactness and projector orthogonality",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4831_3_live_flux_coefficients_missing",
            "route_type": "direct_flux_coefficients",
            "route": "live first boundary/projector flux coefficients missing",
            "source_path": fb549,
            "equation_ref": "FB549_0_boundary_flux_bound",
            "notes": "schema exists but no source-backed B_zero/projector/Q_edge/K_boundary values",
            **base,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4831_4_direct_flux_smoke_pass",
            "route_type": "direct_flux_coefficients",
            "route": "direct finite boundary/projector flux smoke",
            "source_path": fb549,
            "equation_ref": "FB549_0_boundary_flux_bound",
            "notes": "nonclaim arithmetic smoke for first flux coefficient row",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4831_5_component_flux_pack_smoke_pass",
            "route_type": "component_flux_pack",
            "route": "component finite boundary/projector flux pack smoke",
            "source_path": fb550,
            "equation_ref": "FB550_0_commutator_projector_bound",
            "notes": "nonclaim arithmetic smoke for full retained boundary/projector envelope",
            **base,
            **component,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4831_6_forbidden_closure_only_quotient",
            "route_type": "boundary_projector_zero",
            "route": "forbidden closure-only quotient",
            "source_path": doc_1019,
            "equation_ref": "RVT1019_0_boundary_exactness",
            "notes": "CLOSURE_ONLY_QUOTIENT cannot erase edge/boundary coefficients",
            **base,
            **zero,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4831_7_forbidden_measured_GM_source",
            "route_type": "component_flux_pack",
            "route": "forbidden measured GM denominator",
            "source_path": doc_1019,
            "equation_ref": "DC1019_2_decision",
            "notes": "MEASURED_GM_AS_SOURCE cannot normalize the flux theorem",
            **base,
            **component,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4831_8_forbidden_cancellation",
            "route_type": "component_flux_pack",
            "route": "forbidden cancellation of unknown boundary/projector terms",
            "source_path": doc_1019,
            "equation_ref": "DC1019_1_no_cancellation_total",
            "notes": "CANCEL_UNKNOWN_COMPONENTS cannot prove a boundary/projector zero",
            **base,
            **component,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4831_9_forbidden_drop_projector_stress",
            "route_type": "direct_flux_coefficients",
            "route": "forbidden dropped projector stress",
            "source_path": str(SOURCES["pst550"]),
            "equation_ref": "PST550_4_variation_stress",
            "notes": "DROP_PROJECTOR_STRESS cannot close PiM boundary flux",
            **base,
            **direct,
            "timestamp_utc": timestamp,
        },
    ]


def decisions(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DEC4831_0_zero", "Boundary/projector zero is still unsigned for current MTS.", "The route needs parent-owned boundary domain, B primitive, no-hair, projector definition, edge mass-independence and source-edge symplectic orthogonality.", "keep Delta_symp/local-GR promotion blocked", False),
        ("DEC4831_1_flux", "The first flux coefficient envelope is now executable.", "If boundary/projector silence fails, B_zero, vector/tensor/shear/marker, kernel, commutator, projector variation, Q_edge and K_boundary must be retained absolutely.", "source or theorem-zero each flux coefficient before local tests", False),
        ("DEC4831_2_next", "The next hard target is the B_X primitive/cocycle row.", "BE1019_1 and BE1019_5 are the earliest clauses that can collapse the edge flux without data fitting.", NEXT_TARGET, False),
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
        ("CG4831_0_runner_installed", "boundary/projector gate is executable", True, "runner computes exact-zero, direct flux, and full component-pack routes", False),
        ("CG4831_1_boundary_zero", "boundary exactness/no-hair is theorem-zero", False, "relative class, primitive, kernel and no-hair clauses remain unsigned", False),
        ("CG4831_2_projector_zero", "projector orthogonality is theorem-zero", False, "PiM definition, edge mass independence, symplectic block and reference silence remain unsigned", False),
        ("CG4831_3_flux_row_ready", "finite flux coefficient route is staged", True, "smoke rows compute epsilon and observable feeds without cancellation", False),
        ("CG4831_4_no_shortcuts", "symbolic edge zero, closure-only quotient, measured GM, cancellation and dropped projector stress fail closed", True, "forbidden rows return FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", False),
        ("CG4831_5_no_local_GR_claim", "local GR/Newton/R10/PPN claims remain blocked", True, "no runner row allows a claim", False),
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
            "objective": "derive B_X primitive/cocycle zero or stage first source-backed edge flux row",
            "include": "B_X=d b_X primitive, allowed boundary domain, kernel derivative term, local counterterm, K_boundary cocycle, Q_edge, source paths, units, no-cancellation validation",
            "exclude": "symbolic edge zero, closure-only quotient, measured GM denominator, dropped projector stress, cancellation, local-GR/Newton/R10/PPN claim",
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
        "RUN4831_0_live_boundary_projector_zero_missing": "BLOCKED_BOUNDARY_PROJECTOR_ZERO_CLAUSES",
        "RUN4831_1_conditional_boundary_projector_zero_pass": "BOUNDARY_PROJECTOR_ZERO_PASS_NONCLAIM",
        "RUN4831_2_forbidden_symbolic_edge_zero": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4831_3_live_flux_coefficients_missing": "BLOCKED_DIRECT_BOUNDARY_PROJECTOR_FLUX_INPUTS",
        "RUN4831_4_direct_flux_smoke_pass": "DIRECT_BOUNDARY_PROJECTOR_FLUX_PASS_NONCLAIM",
        "RUN4831_5_component_flux_pack_smoke_pass": "COMPONENT_BOUNDARY_PROJECTOR_FLUX_PASS_NONCLAIM",
        "RUN4831_6_forbidden_closure_only_quotient": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4831_7_forbidden_measured_GM_source": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4831_8_forbidden_cancellation": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4831_9_forbidden_drop_projector_stress": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
    }
    direct = by_id.get("RUN4831_4_direct_flux_smoke_pass", {})
    component = by_id.get("RUN4831_5_component_flux_pack_smoke_pass", {})
    checks = [
        ("VAL4831_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        ("VAL4831_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ("VAL4831_02_output_count", len(outputs) == len(expected), "all runner rows emitted"),
        ("VAL4831_03_expected_statuses", all(by_id.get(row_id, {}).get("runner_status") == status for row_id, status in expected.items()), "runner statuses match expected pass/block/fail modes"),
        ("VAL4831_04_live_zero_blocked", by_id["RUN4831_0_live_boundary_projector_zero_missing"]["runner_status"] == "BLOCKED_BOUNDARY_PROJECTOR_ZERO_CLAUSES", "live boundary/projector zero remains blocked"),
        ("VAL4831_05_live_flux_blocked", by_id["RUN4831_3_live_flux_coefficients_missing"]["runner_status"] == "BLOCKED_DIRECT_BOUNDARY_PROJECTOR_FLUX_INPUTS", "live flux coefficient row remains missing"),
        ("VAL4831_06_direct_smoke_pass", close_to(direct.get("epsilon_boundary_projector_abs"), 0.0525) and close_to(direct.get("BY5_boundary_projector_feed_abs"), 0.105), "direct flux smoke computes first coefficient envelope"),
        ("VAL4831_07_component_smoke_pass", close_to(component.get("epsilon_boundary_projector_abs"), 0.085) and close_to(component.get("BY5_boundary_projector_feed_abs"), 0.17), "component flux pack smoke computes full retained envelope"),
        ("VAL4831_08_forbidden_routes_fail", all(by_id[row_id]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE" for row_id in ("RUN4831_2_forbidden_symbolic_edge_zero", "RUN4831_6_forbidden_closure_only_quotient", "RUN4831_7_forbidden_measured_GM_source", "RUN4831_8_forbidden_cancellation", "RUN4831_9_forbidden_drop_projector_stress")), "forbidden shortcuts fail closed"),
        ("VAL4831_09_no_claim_allowed", not any(str(row.get("claim_allowed", "")).lower() == "true" for row in outputs), "no runner row allows a claim"),
        ("VAL4831_10_runner_compiles", True, "runner compiled before execution"),
        ("VAL4831_11_next_target_written", NEXT_TARGET_CSV.exists(), "next target CSV written"),
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
    doc = f"""# 4831 Y5 R2FR boundary cohomology projector silence or first flux coefficient row

**Status:** 4831 makes the boundary/projector silence route executable. The exact path needs a parent-signed compact boundary domain, trivial relative cohomology or a primitive `B_imp=d b_X`, no vector/tensor/shear/marker boundary hair, and a Hamiltonian projector that is orthogonal to edge/source motion. Current MTS has not signed those clauses.

**Decision:** `{DECISION}`.

**Claim ceiling:** no local-GR, Newtonian, R10, R11, PPN, source-charge, boundary-zero, projector-zero, or `Delta_symp` claim is allowed from 4831.

## Core equations

```text
B_imp = d_boundary b_X + B_pure
Q_edge^H(lambda) = int_boundary F_lambda epsilon B_X
epsilon_boundary_projector =
    (|B_zero_flux|+|boundary_vector_flux|+|boundary_tensor_flux|
     +|kernel_derivative_flux|+|projector_boundary_flux|
     +|Pi_M^H Q_edge|+|K_boundary|+...)/M_H_ref
```

## Source register

{md_table(sources, ["source_id", "exists", "needle_found", "role"])}

## Boundary/projector zero audit

{md_table(audit, ["clause_id", "claim_piece", "current_result", "finite_fallback"])}

## Flux coefficient contract

{md_table(contract, ["contract_id", "quantity", "definition", "status"])}

## Runner output

{md_table(outputs, ["row_id", "runner_status", "B_zero_flux_over_MH_abs", "projector_boundary_flux_over_MH_abs", "Q_edge_over_MH_abs", "epsilon_boundary_projector_abs", "BY5_boundary_projector_feed_abs", "missing_for_claim"])}

## Decision ledger

{md_table(decision_rows, ["decision_id", "decision", "because", "next_action"])}

## Validation

{md_table(validation, ["validation_id", "result", "detail"])}

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    formal = f"""# 847 PPC4161 boundary cohomology projector silence or first flux coefficient row

Checkpoint: `{DOC_PATH}`

4831 turns boundary exactness, no-hair, and projector orthogonality into a visible zero-or-flux gate. The live branch remains nonclaim because the boundary primitive/domain and projector-orthogonality clauses are not parent-signed for current MTS.

Decision: `{DECISION}`

Runner: `{RUNNER}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_claims(timestamp: str) -> None:
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "boundary_cohomology_projector_silence_or_first_flux_coefficient_row",
        "current_evidence": "4831 converts boundary cohomology/no-hair and projector orthogonality into an executable zero-or-finite flux coefficient runner; live zero and source-backed flux values remain missing.",
        "status": "boundary_projector_flux_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "boundary domain, B_X primitive, kernel derivative, vector/tensor boundary hair, projector definition, edge mass-independence, symplectic block and source pack remain unsigned or missing",
        "sector": "local_gr_Newton_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smoke rows pass but live boundary/projector flux rows are not source-backed",
        "title": "Boundary cohomology projector silence or first flux coefficient row",
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
        f"""## PPC4161 4831 boundary/projector flux runner

`{MARKER}`. The `Delta_symp` chain now has a boundary/projector gate: either boundary exactness/no-hair and Hamiltonian projector orthogonality are parent-signed, or `B_zero_flux`, boundary hair, kernel derivative flux, projector boundary leakage, `Pi_M^H Q_edge`, and `K_boundary` are retained in `epsilon_boundary_projector`. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4831 boundary cohomology/projector silence or first flux row

`{MARKER}` stops symbolic boundary/edge silence. Conditional zero requires parent-owned boundary domain, primitive, no-hair and projector orthogonality; finite rows compute `epsilon_boundary_projector`, observable PPN equivalents and BY5 feed. Symbolic edge zero, closure-only quotient, measured GM, dropped projector stress and cancellation fail closed. Next: `{NEXT_TARGET}`.""",
    )


def update_resume(timestamp: str) -> None:
    text = f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4831-Y5-R2FR-boundary-cohomology-projector-silence-or-first-flux-coefficient-row.md`
Marker: `{MARKER}`

## Where we are

4831 made the boundary/projector silence gate executable:

```text
B_imp = d_boundary b_X + B_pure
Q_edge^H(lambda) = int_boundary F_lambda epsilon B_X
epsilon_boundary_projector = sum(|boundary/projector/edge flux residuals|)/M_H_ref
```

## Live blockers

- Boundary domain/cohomology, `B_X` primitive, kernel derivative silence, and boundary no-hair are not parent-signed.
- Hamiltonian projector definition, edge mass-independence, source-edge symplectic orthogonality, and reference silence are not parent-signed.
- No source-backed live rows exist for `B_zero_flux`, boundary vector/tensor/shear/marker flux, projector commutator/variation, `Pi_M^H Q_edge`, or `K_boundary`.
- Symbolic edge zero, closure-only quotient, measured/orbital `GM`, dropped projector stress, and cancellation-only routes are explicitly forbidden.

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
        print(f"4831 validation failed: {failed}", file=sys.stderr)
        return 1
    print(f"{MARKER} complete")
    print(f"doc={DOC_PATH}")
    print(f"runner_output={RUNNER_OUTPUT}")
    print(f"validation={VALIDATION_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
