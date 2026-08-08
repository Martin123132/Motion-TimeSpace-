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

CHECKPOINT = "4833"
CLAIM_ID = "L-675"
MARKER = "PPC4161_PARENT_LTHETAQ_BOUNDARY_MOMENTUM_OR_FIRST_BX_NORM_ROW_4833"
PACKET_MARKER = "PPC4161_PACKET_PARENT_LTHETAQ_BOUNDARY_MOMENTUM_OR_FIRST_BX_NORM_ROW_4833"
DECISION = "PARENT_LTHETAQ_BOUNDARY_MOMENTUM_UNSIGNED_FIRST_BX_NORM_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4834-Y5-R2FR-parent-theta-omega-DC-operator-or-source-coupling-bound-row.md"

DOC_PATH = POST / "4833-Y5-R2FR-parent-LThetaQ-boundary-momentum-or-first-bX-norm-row.md"
FORMAL_PATH = FORMAL / "849-PPC4161-parent-LThetaQ-boundary-momentum-or-first-bX-norm-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "parent_LThetaQ_boundary_momentum_runner.py"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4833_SOURCE_REGISTER.csv"
FORMULA_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4833_PARENT_LTHETAQ_FORMULA_AUDIT.csv"
NORM_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4833_BX_NORM_BOUND_CONTRACT.csv"
RUNNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4833_PARENT_BOUNDARY_RUNNER_INPUT.csv"
RUNNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4833_PARENT_BOUNDARY_RUNNER_OUTPUT.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4833_DECISION_LEDGER.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4833_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4833_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4833_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4833_VALIDATION.csv"

SOURCES = {
    "resume": RESUME_PATH,
    "4832_doc": POST / "4832-Y5-R2FR-BX-primitive-cocycle-zero-or-first-edge-source-row.md",
    "1021_doc": POST / "1021-Y5-R10-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md",
    "667_variation": SOURCE_DIR / "P8_Y5_R10_667_VARIATION_LEDGER.csv",
    "667_action": SOURCE_DIR / "P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv",
    "667_fallback": SOURCE_DIR / "P8_Y5_R10_667_RESIDUAL_FALLBACK_ROWS.csv",
    "669_theta": SOURCE_DIR / "P8_Y5_R10_669_THETA_QX_VARIATION_LEDGER.csv",
    "669_candidates": SOURCE_DIR / "P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv",
    "583_contract": SOURCE_DIR / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv",
    "583_owner": SOURCE_DIR / "P8_Y5_R10_583_PARENT_MOMENTUM_MAP_OWNER_ATTEMPT.csv",
    "591_dc": SOURCE_DIR / "P8_Y5_R10_591_DC_OPERATOR_FORMULA.csv",
    "591_dagger": SOURCE_DIR / "P8_Y5_R10_591_DCDAGGER_FORMULA.csv",
    "591_compare": SOURCE_DIR / "P8_Y5_R10_591_OMEGA_DCDAGGER_COMPARISON.csv",
    "1020_bound": SOURCE_DIR / "P8_Y5_R10_1020_SOURCE_PACK_FIRST_BOUND_ROW.csv",
    "4832_output": SOURCE_DIR / "P8_Y5_R2FR_4832_EDGE_SOURCE_RUNNER_OUTPUT.csv",
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
        ("SRC4833_00_resume", SOURCES["resume"], "4833-Y5-R2FR-parent-LThetaQ-boundary-momentum-or-first-bX-norm-row.md", "4832 selected the parent LThetaQ target."),
        ("SRC4833_01_4832_doc", SOURCES["4832_doc"], "DEC4832_2_next", "B_X/cocycle handoff."),
        ("SRC4833_02_1021_parent", SOURCES["1021_doc"], "PVT1021_0_parent_first_variation", "parent variation map."),
        ("SRC4833_03_1021_BX", SOURCES["1021_doc"], "PVT1021_3_BX_definition", "B_X definition."),
        ("SRC4833_04_1021_norm", SOURCES["1021_doc"], "EBF1021_0_norm_bX", "first b_X norm gap."),
        ("SRC4833_05_667_variation", SOURCES["667_variation"], "VL667_0_total_variation", "parent variation ledger."),
        ("SRC4833_06_667_hamiltonian", SOURCES["667_variation"], "VL667_3_Hamiltonian_variation", "Hamiltonian boundary variation."),
        ("SRC4833_07_667_action", SOURCES["667_action"], "PBA667_1_bulk_action", "parent action ansatz."),
        ("SRC4833_08_667_charge", SOURCES["667_action"], "PBA667_3_charge_definition", "Noether charge definition."),
        ("SRC4833_09_667_fallback", SOURCES["667_fallback"], "RF667_0_LX_theta_Qtau_owner", "missing owner fallback."),
        ("SRC4833_10_669_theta", SOURCES["669_theta"], "V669_0_variation", "Theta_X ledger."),
        ("SRC4833_11_669_charge", SOURCES["669_theta"], "V669_2_charge", "Q_X ledger."),
        ("SRC4833_12_669_candidates", SOURCES["669_candidates"], "LX669_1_vertical_constraint", "vertical constraint route."),
        ("SRC4833_13_583_contract", SOURCES["583_contract"], "NMC583_0_symplectic_potential", "Noether momentum-map contract."),
        ("SRC4833_14_583_boundary", SOURCES["583_contract"], "NMC583_5_boundary_zero", "boundary zero contract."),
        ("SRC4833_15_583_owner", SOURCES["583_owner"], "OMA583_1_noether_current_owner", "Noether owner attempt."),
        ("SRC4833_16_591_dc", SOURCES["591_dc"], "DC591_4_boundary_pairing", "DC boundary pairing."),
        ("SRC4833_17_591_dagger", SOURCES["591_dagger"], "DCA591_3_boundary_adjoint", "boundary adjoint."),
        ("SRC4833_18_591_compare", SOURCES["591_compare"], "CMP591_4_boundary", "Omega/DC boundary comparison."),
        ("SRC4833_19_1020_bound", SOURCES["1020_bound"], "EDGEBOUND1020_0_formal_bound_row", "edge bound schema."),
        ("SRC4833_20_4832_output", SOURCES["4832_output"], "RUN4832_4_direct_edge_bound_smoke_pass", "upstream edge bound runner."),
        ("SRC4833_21_runner", SOURCES["runner"], "def evaluate_row", "4833 executable runner."),
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


def formula_audit(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("PLT4833_0_first_variation", "parent sector first variation", "delta L_X=E_X delta X + d Theta_X(delta X)", "formula_written_not_owned", "parent_LX_signed;theta_X_signed"),
        ("PLT4833_1_Noether_current", "Noether current", "J_epsilon^X=Theta_X(delta_epsilon X)-mu_epsilon", "template_only", "vertical_generator_signed;theta_X_signed"),
        ("PLT4833_2_charge_decomposition", "surface charge and constraints", "J_epsilon^X=dQ_epsilon^X+epsilon C_X", "formula_written_not_owned", "Q_X_signed;DC_operator_signed"),
        ("PLT4833_3_boundary_covector", "Hamiltonian boundary covector", "delta H_epsilon^X|_S=int_S(delta Q_epsilon^X-i_epsilon Theta_X+delta B_ct)", "boundary_pairing_known_not_cancelled", "Bct_reference_owner_signed;boundary_condition_lock_signed"),
        ("PLT4833_4_BX_pullback", "edge boundary momentum", "B_X=i_S^*(delta Q_epsilon^X-i_epsilon Theta_X+delta B_ct)", "definition_sharpened", "same_branch_signed;hodge_domain_signed"),
        ("PLT4833_5_Hodge_bound", "first b_X norm law", "if B_exact=d_S b_X and delta_S b_X=0 then ||b_X||_2 <= C_H ||B_exact||_2/sqrt(lambda_1)", "derived_bound_law", "spectral_gap_lambda1_abs;B_exact_norm_abs"),
        ("PLT4833_6_edge_feed", "kernel edge feed", "Q_edge <= C_corner+||d_S(F epsilon)||_*||b_X||_*+harmonic+residual+K_boundary", "bound_law_executable", "norm_dS_Feps_abs;harmonic_edge_abs;residual_edge_abs;K_boundary_abs"),
        ("PLT4833_7_guard", "no circular source normalization", "B_X and b_X are parent/Hodge objects, not orbital GM or post-readout masks", "guard_active", "no_cancellation_guard;no_measured_GM_absorption_signed"),
    ]
    return [
        {
            "clause_id": clause_id,
            "object": obj,
            "formula": formula,
            "current_result": current_result,
            "needed_signature_or_input": needed,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for clause_id, obj, formula, current_result, needed in rows
    ]


def norm_contract(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("BNC4833_0_parent_formula", "B_X parent formula", "B_X=i_S^*(delta Q_X-i_epsilon Theta_X+delta B_ct)", "conditional formula; unsigned for live branch"),
        ("BNC4833_1_hodge_norm", "norm_bX_bound", "C_hodge*B_exact_norm/sqrt(lambda1_edge)", "finite bound requires spectral gap and exact/harmonic split"),
        ("BNC4833_2_kernel_feed", "Q_edge_kernel_feed", "norm_dS_Feps*norm_bX_bound", "feeds 4832 edge bound"),
        ("BNC4833_3_projected_edge", "Qbar_edge_XH_bound", "PiM_norm*(corner+kernel_feed+harmonic+residual+K_boundary)/M_H_ref_min", "projection still nonclaim until PiM/MHref owned"),
        ("BNC4833_4_alpha", "alpha_edge(lambda)", "K_edge*Qbar_edge_XH_bound*qbar_XT", "observable edge channel remains nonclaim"),
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
    parent_signed = {
        "parent_LX_signed": "true",
        "theta_X_signed": "true",
        "Q_X_signed": "true",
        "omega_X_signed": "true",
        "vertical_generator_signed": "true",
        "DC_operator_signed": "true",
        "Bct_reference_owner_signed": "true",
        "boundary_condition_lock_signed": "true",
        "hodge_domain_signed": "true",
        "no_physical_charge_removed_signed": "true",
        "no_measured_GM_absorption_signed": "true",
    }
    hodge_smoke = {
        "C_hodge_abs": "1.0",
        "spectral_gap_lambda1_abs": "4.0",
        "B_exact_norm_abs": "0.3",
        "norm_dS_Feps_abs": "0.02",
        "corner_abs": "0.01",
        "harmonic_edge_abs": "0.02",
        "residual_edge_abs": "0.01",
        "K_boundary_abs": "0.005",
        "M_H_ref_min_abs": "2.0",
        "PiM_norm_abs": "0.5",
        "K_edge_abs": "1.5",
        "qbar_XT_abs": "0.2",
        "tau_BY5_edge_abs": "2.0",
    }
    component_smoke = {
        "C_hodge_abs": "1.0",
        "spectral_gap_lambda1_abs": "4.0",
        "B_parent_pullback_norm_abs": "0.2",
        "Bct_norm_abs": "0.05",
        "DC_boundary_covector_norm_abs": "0.03",
        "reference_mismatch_norm_abs": "0.02",
        "norm_dS_Feps_abs": "0.02",
        "corner_abs": "0.01",
        "harmonic_edge_abs": "0.02",
        "residual_edge_abs": "0.01",
        "K_boundary_abs": "0.005",
        "M_H_ref_min_abs": "2.0",
        "PiM_norm_abs": "0.5",
        "K_edge_abs": "1.5",
        "qbar_XT_abs": "0.2",
        "tau_BY5_edge_abs": "2.0",
    }
    doc_1021 = str(SOURCES["1021_doc"])
    theta_669 = str(SOURCES["669_theta"])
    bound_1020 = str(SOURCES["1020_bound"])
    dagger_591 = str(SOURCES["591_dagger"])
    return [
        {
            "row_id": "RUN4833_0_live_parent_LThetaQ_missing",
            "route_type": "parent_LThetaQ_formula",
            "route": "live parent LThetaQ boundary momentum audit",
            "source_path": doc_1021,
            "equation_ref": "PVT1021_0_parent_first_variation;PVT1021_3_BX_definition",
            "notes": "current MTS has the covariant formula but not signed L_X, Theta_X, Q_X, Omega_X, DC_X or B_ct owner",
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4833_1_conditional_parent_LThetaQ_formula_pass",
            "route_type": "parent_LThetaQ_formula",
            "route": "conditional parent signed LThetaQ boundary momentum",
            "source_path": doc_1021,
            "equation_ref": "PVT1021_5_verdict",
            "notes": "nonclaim theorem-shape smoke row for the parent boundary formula",
            **base,
            **parent_signed,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4833_2_forbidden_formula_only_LThetaQ",
            "route_type": "parent_LThetaQ_formula",
            "route": "forbidden formula-only parent boundary momentum",
            "source_path": theta_669,
            "equation_ref": "V669_0_variation",
            "notes": "FORMULA_ONLY_LTHETAQ cannot replace a signed sector variation",
            **base,
            **parent_signed,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4833_3_live_bX_norm_missing",
            "route_type": "hodge_bX_norm_bound",
            "route": "live first b_X norm bound missing",
            "source_path": bound_1020,
            "equation_ref": "EDGEBOUND1020_0_formal_bound_row",
            "notes": "norm_bX requires explicit primitive or spectral/Hodge bound inputs",
            **base,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4833_4_hodge_bX_norm_smoke_pass",
            "route_type": "hodge_bX_norm_bound",
            "route": "finite Hodge b_X norm smoke",
            "source_path": bound_1020,
            "equation_ref": "EDGEBOUND1020_0_formal_bound_row",
            "notes": "nonclaim arithmetic smoke for C_hodge*B_exact/sqrt(lambda1)",
            **base,
            **hodge_smoke,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4833_5_component_bX_norm_smoke_pass",
            "route_type": "component_bX_norm_bound",
            "route": "component finite b_X norm smoke",
            "source_path": dagger_591,
            "equation_ref": "DCA591_3_boundary_adjoint",
            "notes": "nonclaim arithmetic smoke from parent pullback, counterterm, DC boundary covector and reference mismatch",
            **base,
            **component_smoke,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4833_6_forbidden_symbolic_bX_norm",
            "route_type": "hodge_bX_norm_bound",
            "route": "forbidden symbolic b_X norm",
            "source_path": bound_1020,
            "equation_ref": "EDGEBOUND1020_0_formal_bound_row",
            "notes": "SYMBOLIC_BX_NORM cannot fill EDGEBOUND1020",
            **base,
            **hodge_smoke,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4833_7_forbidden_no_spectral_gap",
            "route_type": "hodge_bX_norm_bound",
            "route": "forbidden Poincare without spectral gap",
            "source_path": bound_1020,
            "equation_ref": "EDGEBOUND1020_0_formal_bound_row",
            "notes": "POINCARE_WITHOUT_SPECTRAL_GAP cannot bound b_X",
            **base,
            **hodge_smoke,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4833_8_forbidden_uncontrolled_harmonic",
            "route_type": "component_bX_norm_bound",
            "route": "forbidden Hodge with uncontrolled harmonic part",
            "source_path": doc_1021,
            "equation_ref": "BXG1021_3_harmonic_zero",
            "notes": "HODGE_WITH_UNCONTROLLED_HARMONIC cannot erase h_X",
            **base,
            **component_smoke,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4833_9_forbidden_measured_GM_source",
            "route_type": "component_bX_norm_bound",
            "route": "forbidden measured GM source",
            "source_path": doc_1021,
            "equation_ref": "PVT1021_5_verdict",
            "notes": "MEASURED_GM_AS_SOURCE cannot normalize parent boundary momentum",
            **base,
            **component_smoke,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4833_10_forbidden_cancellation",
            "route_type": "component_bX_norm_bound",
            "route": "forbidden cancellation of unknown boundary pieces",
            "source_path": doc_1021,
            "equation_ref": "R1021_2_edge_bound_fill",
            "notes": "CANCEL_UNKNOWN_COMPONENTS cannot prove b_X or Q_edge small",
            **base,
            **component_smoke,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "RUN4833_11_forbidden_GR_import",
            "route_type": "parent_LThetaQ_formula",
            "route": "forbidden GR import of LThetaQ owner",
            "source_path": doc_1021,
            "equation_ref": "PVT1021_0_parent_first_variation",
            "notes": "GR_IMPORT cannot replace MTS parent Theta_X and Q_X",
            **base,
            **parent_signed,
            "timestamp_utc": timestamp,
        },
    ]


def decisions(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DEC4833_0_parent_formula", "The parent Noether boundary formula is sharpened but not signed for live MTS.", "L_X, Theta_X, Q_X, Omega_X, DC_X, vertical action and B_ct owner still have to come from one parent branch.", "keep B_X derivation nonclaim", False),
        ("DEC4833_1_bX_norm", "The first b_X norm law is now executable.", "A spectral/Hodge bound turns norm_bX into C_hodge*B_exact/sqrt(lambda1), then feeds Q_edge and alpha_edge absolutely.", "source spectral gap, B_exact norm, harmonic/residual and kernel inputs", False),
        ("DEC4833_2_next", "The next derivation target should fill parent theta/Omega/DC or demote to source-coupling bounds.", "That is the remaining object that decides whether the local branch is a theorem-zero route or a bounded residual route.", NEXT_TARGET, False),
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
        ("CG4833_0_runner_installed", "parent LThetaQ and b_X norm gate is executable", True, "runner computes parent formula, Hodge b_X norm, and component b_X norm routes", False),
        ("CG4833_1_parent_formula_unsigned", "parent LThetaQ boundary formula is claim-owned", False, "signed L_X/Theta_X/Q_X/Omega_X/DC_X/B_ct branch is still absent", False),
        ("CG4833_2_bX_norm_ready", "first b_X norm law is staged", True, "smoke rows compute norm_bX, Q_edge feed, Qbar, alpha and BY5", False),
        ("CG4833_3_no_shortcuts", "formula-only LThetaQ, symbolic b_X, no spectral gap, uncontrolled harmonic, measured GM, cancellation and GR import fail closed", True, "forbidden rows return FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE", False),
        ("CG4833_4_no_local_claim", "local GR/Newton/R10/PPN claims remain blocked", True, "no live row allows a claim", False),
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
            "objective": "fill parent theta/Omega/DC operator enough to own B_X, or stage source-coupling bound rows if the owner route fails",
            "include": "Theta_X, Omega_X, DC_X, vertical generator, boundary adjoint, B_ct, spectral gap, B_exact norm, harmonic/residual inputs, units, source paths",
            "exclude": "formula-only LThetaQ, symbolic b_X norm, Poincare without spectral gap, uncontrolled harmonic erasure, measured GM denominator, cancellation, GR import",
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
        "RUN4833_0_live_parent_LThetaQ_missing": "BLOCKED_PARENT_LTHETAQ_BOUNDARY_MOMENTUM_CLAUSES",
        "RUN4833_1_conditional_parent_LThetaQ_formula_pass": "PARENT_LTHETAQ_BOUNDARY_MOMENTUM_SIGNED_NONCLAIM",
        "RUN4833_2_forbidden_formula_only_LThetaQ": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4833_3_live_bX_norm_missing": "BLOCKED_HODGE_BX_NORM_BOUND_INPUTS",
        "RUN4833_4_hodge_bX_norm_smoke_pass": "HODGE_BX_NORM_BOUND_PASS_NONCLAIM",
        "RUN4833_5_component_bX_norm_smoke_pass": "COMPONENT_BX_NORM_BOUND_PASS_NONCLAIM",
        "RUN4833_6_forbidden_symbolic_bX_norm": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4833_7_forbidden_no_spectral_gap": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4833_8_forbidden_uncontrolled_harmonic": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4833_9_forbidden_measured_GM_source": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4833_10_forbidden_cancellation": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
        "RUN4833_11_forbidden_GR_import": "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
    }
    hodge = by_id.get("RUN4833_4_hodge_bX_norm_smoke_pass", {})
    component = by_id.get("RUN4833_5_component_bX_norm_smoke_pass", {})
    forbidden_ids = [
        "RUN4833_2_forbidden_formula_only_LThetaQ",
        "RUN4833_6_forbidden_symbolic_bX_norm",
        "RUN4833_7_forbidden_no_spectral_gap",
        "RUN4833_8_forbidden_uncontrolled_harmonic",
        "RUN4833_9_forbidden_measured_GM_source",
        "RUN4833_10_forbidden_cancellation",
        "RUN4833_11_forbidden_GR_import",
    ]
    checks = [
        ("VAL4833_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        ("VAL4833_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ("VAL4833_02_output_count", len(outputs) == len(expected), "all runner rows emitted"),
        ("VAL4833_03_expected_statuses", all(by_id.get(row_id, {}).get("runner_status") == status for row_id, status in expected.items()), "runner statuses match expected pass/block/fail modes"),
        ("VAL4833_04_live_parent_blocked", by_id["RUN4833_0_live_parent_LThetaQ_missing"]["runner_status"] == "BLOCKED_PARENT_LTHETAQ_BOUNDARY_MOMENTUM_CLAUSES", "live parent LThetaQ formula remains blocked"),
        ("VAL4833_05_live_norm_blocked", by_id["RUN4833_3_live_bX_norm_missing"]["runner_status"] == "BLOCKED_HODGE_BX_NORM_BOUND_INPUTS", "live first b_X norm row remains missing"),
        ("VAL4833_06_hodge_smoke_pass", close_to(hodge.get("norm_bX_bound_abs"), 0.15) and close_to(hodge.get("Q_edge_kernel_feed_abs"), 0.003) and close_to(hodge.get("Q_edge_bound_abs"), 0.048) and close_to(hodge.get("Qbar_edge_XH_bound_abs"), 0.012) and close_to(hodge.get("alpha_edge_abs"), 0.0036) and close_to(hodge.get("BY5_edge_feed_abs"), 0.024), "Hodge b_X smoke computes norm and edge feed"),
        ("VAL4833_07_component_smoke_pass", close_to(component.get("B_X_pullback_norm_abs"), 0.3) and close_to(component.get("norm_bX_bound_abs"), 0.15) and close_to(component.get("Q_edge_bound_abs"), 0.048), "component b_X smoke computes same envelope"),
        ("VAL4833_08_forbidden_routes_fail", all(by_id[row_id]["runner_status"] == "FAILED_FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE" for row_id in forbidden_ids), "forbidden shortcuts fail closed"),
        ("VAL4833_09_no_claim_allowed", not any(str(row.get("claim_allowed", "")).lower() == "true" for row in outputs), "no runner row allows a claim"),
        ("VAL4833_10_runner_compiles", True, "runner compiled before execution"),
        ("VAL4833_11_next_target_written", NEXT_TARGET_CSV.exists(), "next target CSV written"),
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
    doc = f"""# 4833 Y5 R2FR parent LThetaQ boundary momentum or first b_X norm row

**Status:** 4833 derives the exact contract a parent action must satisfy before `B_X` is owned, and adds the first executable `b_X` norm bound. The live MTS branch still lacks signed parent `L_X/Theta_X/Q_X/Omega_X/DC_X/B_ct`, but `norm_bX` is no longer an empty placeholder.

**Decision:** `{DECISION}`.

**Claim ceiling:** no local-GR, Newtonian, R10, R11, PPN, source-charge, `B_X` primitive, `b_X` norm, or edge-alpha claim is allowed from 4833.

## Core derivation

```text
delta L_X = E_X delta X + d Theta_X(delta X)
J_epsilon^X = Theta_X(delta_epsilon X) - mu_epsilon
J_epsilon^X = d Q_epsilon^X + epsilon C_X
delta H_epsilon^X|_S = int_S(delta Q_epsilon^X - i_epsilon Theta_X + delta B_ct)
B_X = i_S^*(delta Q_epsilon^X - i_epsilon Theta_X + delta B_ct)

B_X = d_S b_X + h_X + r_X
||b_X||_2 <= C_H(S) ||B_exact||_2 / sqrt(lambda_1(S))
Q_edge <= C_corner + ||d_S(F epsilon)||_* ||b_X||_* + h_X + r_X + K_boundary
```

## Source register

{md_table(sources, ["source_id", "exists", "needle_found", "role"])}

## Parent formula audit

{md_table(audit, ["clause_id", "object", "current_result", "needed_signature_or_input"])}

## b_X norm contract

{md_table(contract, ["contract_id", "quantity", "definition", "status"])}

## Runner output

{md_table(outputs, ["row_id", "runner_status", "B_X_pullback_norm_abs", "norm_bX_bound_abs", "Q_edge_kernel_feed_abs", "Q_edge_bound_abs", "Qbar_edge_XH_bound_abs", "alpha_edge_abs", "missing_for_claim"])}

## Decision ledger

{md_table(decision_rows, ["decision_id", "decision", "because", "next_action"])}

## Validation

{md_table(validation, ["validation_id", "result", "detail"])}

## Next target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)
    formal = f"""# 849 PPC4161 parent LThetaQ boundary momentum or first b_X norm row

Checkpoint: `{DOC_PATH}`

4833 writes the parent Noether/Hamiltonian contract for `B_X` and turns `norm_bX` into a spectral/Hodge bound rather than a symbolic gap. The live branch remains nonclaim because parent `L_X`, `Theta_X`, `Q_X`, `Omega_X`, `DC_X`, vertical generator, boundary counterterm, spectral gap and source-bound inputs are not yet owned together.

Decision: `{DECISION}`

Runner: `{RUNNER}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_claims(timestamp: str) -> None:
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "parent_LThetaQ_boundary_momentum_or_first_bX_norm_row",
        "current_evidence": "4833 derives the parent Noether boundary formula for B_X and stages a spectral/Hodge b_X norm bound runner; live parent owner and live numeric/source rows remain missing.",
        "status": "parent_LThetaQ_bX_norm_runner_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "signed parent L_X/Theta_X/Q_X/Omega_X/DC_X/B_ct, spectral gap, exact pullback norm, harmonic/residual inputs and source-coupling normalization remain missing",
        "sector": "local_gr_Newton_source_coupling",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "smoke rows pass but live parent and b_X norm rows are not source-backed",
        "title": "Parent LThetaQ boundary momentum or first b_X norm row",
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
        f"""## PPC4161 4833 parent LThetaQ boundary momentum and b_X norm gate

`{MARKER}`. The local edge/source bridge now has a parent-action contract: `B_X=i_S^*(delta Q_X-i_epsilon Theta_X+delta B_ct)`, followed by the Hodge/spectral bound `||b_X|| <= C_H ||B_exact||/sqrt(lambda_1)`. This makes the missing coupling attackable as parent `Theta/Omega/DC` ownership or as explicit source-bound rows. Decision: `{DECISION}`.""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## 4833 parent LThetaQ boundary momentum or first b_X norm row

`{MARKER}` stops `b_X` from being a magic object. Conditional parent ownership requires signed `L_X`, `Theta_X`, `Q_X`, `Omega_X`, `DC_X`, vertical generator and `B_ct`. If that fails, the finite route now needs spectral gap, exact pullback norm, harmonic/residual and kernel rows. Formula-only LThetaQ, symbolic `b_X`, no spectral gap, uncontrolled harmonic erasure, measured GM, cancellation and GR import fail closed. Next: `{NEXT_TARGET}`.""",
    )


def update_resume(timestamp: str) -> None:
    text = f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4833-Y5-R2FR-parent-LThetaQ-boundary-momentum-or-first-bX-norm-row.md`
Marker: `{MARKER}`

## Where we are

4833 sharpened the parent boundary-momentum route:

```text
delta L_X = E_X delta X + d Theta_X
J_epsilon^X = Theta_X(delta_epsilon X)-mu_epsilon = dQ_epsilon^X + epsilon C_X
B_X = i_S^*(delta Q_epsilon^X - i_epsilon Theta_X + delta B_ct)
||b_X|| <= C_H ||B_exact|| / sqrt(lambda_1)
Q_edge <= C_corner + norm_dS_Feps*norm_bX + harmonic + residual + K_boundary
```

## Live blockers

- Parent `L_X`, `Theta_X`, `Q_X`, `Omega_X`, `DC_X`, vertical generator and `B_ct` are not signed together.
- The first live `b_X` norm row still needs `lambda_1`, `C_H`, `B_exact_norm`, harmonic/residual bounds, kernel norm and units/source paths.
- `Qbar_edge_XH`, `K_edge`, `qbar_XT`, and `M_H_ref_min` remain nonclaim unless derived or source-backed.
- Formula-only LThetaQ, symbolic `b_X`, Poincare without spectral gap, uncontrolled harmonic erasure, measured/orbital `GM`, GR import and cancellation routes are explicitly forbidden.

## Next target

`{NEXT_TARGET}`
"""
    write_text(RESUME_PATH, text)


def main() -> int:
    timestamp = now()
    py_compile.compile(str(RUNNER), doraise=True)
    sources = source_register(timestamp)
    audit = formula_audit(timestamp)
    contract = norm_contract(timestamp)
    inputs = runner_inputs(timestamp)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(FORMULA_AUDIT, audit)
    write_csv(NORM_CONTRACT, contract)
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
        print(f"4833 validation failed: {failed}", file=sys.stderr)
        return 1
    print(f"{MARKER} complete")
    print(f"doc={DOC_PATH}")
    print(f"runner_output={RUNNER_OUTPUT}")
    print(f"validation={VALIDATION_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
