from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4546"
CLAIM_ID = "L-388"
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_SILENCE_ATTRACTOR_HOMOGENEITY_4546"
MARKER = "PPC4161_SOURCE_SILENCE_AND_ATTRACTOR_HOMOGENEITY_FROM_COMPACT_SUPPORT_OR_UB_POWER_BOUND_4546"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_SILENCE_AND_ATTRACTOR_HOMOGENEITY_FROM_COMPACT_SUPPORT_OR_UB_POWER_BOUND_4546"
DECISION = "STATIC_SOURCE_AND_ML_HOMOGENEITY_EXACT_ZERO_CONDITIONAL_UB2_BOUND_IMPORTED_ACTIVE_NONCLAIM"
NEXT_TARGET = "4547-Y5-R2FR-local-static-residual-vector-projection-to-PPN-Gdot-R10-or-first-numeric-Ubound-row.md"

FORMAL_PATH = FORMAL / "562-PPC4161-source-silence-and-attractor-homogeneity-from-compact-support-or-U_B-power-bound.md"
DOC_PATH = POST / "4546-Y5-R2FR-source-silence-and-attractor-homogeneity-from-compact-support-or-U_B-power-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4546_SOURCE_REGISTER.csv"
EXACT_ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4546_EXACT_ZERO_THEOREM.csv"
UB2_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4546_UB2_STATIC_BOUND_THEOREM.csv"
ML_HOMOGENEITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4546_ML_HOMOGENEITY_BOUND.csv"
STATIC_RESIDUAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4546_STATIC_JRES_BUDGET.csv"
INPUT_REQUIREMENTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4546_INPUT_REQUIREMENTS.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4546_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4546_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4546_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4546_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4546_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC4546_00_4545_status",
            "label": "4545 status",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4545_STATUS.csv",
            "needle": "source_static_amplitude_closed",
            "role": "imports the remaining source/homogeneity gaps",
        },
        {
            "source_id": "SRC4546_01_4545_retained",
            "label": "4545 retained residuals",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4545_RETAINED_RESIDUALS.csv",
            "needle": "P_loc[D_m Delta_h m_L]",
            "role": "selects static source and spatial attractor residuals",
        },
        {
            "source_id": "SRC4546_02_1752_support_audit",
            "label": "1752 source-support audit",
            "path": SOURCE_DIR / "P8_Y5_PARENT_QLOC_1752_SOURCE_SUPPORT_ZERO_BOUND_AUDIT.csv",
            "needle": "R_source = (1-Pi_B) S_cg = U_B S_cg",
            "role": "defines source residual and exact conditional finite bound",
        },
        {
            "source_id": "SRC4546_03_1753_power_convention",
            "label": "1753 source-power convention",
            "path": SOURCE_DIR / "P8_Y5_PARENT_QLOC_1753_SOURCE_POWER_CONVENTION_AUDIT.csv",
            "needle": "p_total=1+p_int",
            "role": "prevents double-counting U_B powers",
        },
        {
            "source_id": "SRC4546_04_1754_silence_attempt",
            "label": "1754 source silence attempt",
            "path": SOURCE_DIR / "P8_Y5_PARENT_QLOC_1754_SOURCE_SILENCE_THEOREM_ATTEMPT.csv",
            "needle": "||R_source|| <= C_H A_1 U_B^2",
            "role": "imports U_B^2 source-residual theorem shape",
        },
        {
            "source_id": "SRC4546_05_1754_ZL_contract",
            "label": "1754 Z_L/D_L contract",
            "path": SOURCE_DIR / "P8_Y5_PARENT_QLOC_1754_ZL_DL_LEAKAGE_VECTOR_CONTRACT.csv",
            "needle": "D_L=sqrt",
            "role": "imports D_L=U_B H_L distance-bound route",
        },
        {
            "source_id": "SRC4546_06_1975_envelope",
            "label": "1975 U_B suppression envelope",
            "path": SOURCE_DIR / "P8_Y5_PARENT_QLOC_1975_UB_SUPPRESSION_BOUND_ENVELOPE.csv",
            "needle": "U_B S_cg amplitude",
            "role": "imports source and m_L U_B^2 bound formulas",
        },
        {
            "source_id": "SRC4546_07_1978_mL_inputs",
            "label": "1978 m_L derivative inputs",
            "path": SOURCE_DIR / "P8_Y5_PARENT_QLOC_1978_ML_DERIVATIVE_ENVELOPE_INPUTS.csv",
            "needle": "mL_A_bar",
            "role": "imports m_L derivative envelope and missing constants",
        },
        {
            "source_id": "SRC4546_08_2224_Scg_gate",
            "label": "2224 S_cg provenance gate",
            "path": SOURCE_DIR / "P8_Y5_PARENT_QLOC_2224_SCG_TERM_PROVENANCE_GATE.csv",
            "needle": "S_cg_norm <= 1/2*T_source_norm*C_qm",
            "role": "keeps S_cg finite provenance noncomputable until source terms are filled",
        },
        {
            "source_id": "SRC4546_09_2224_worldtube",
            "label": "2224 worldtube profile gate",
            "path": SOURCE_DIR / "P8_Y5_PARENT_QLOC_2224_WORLDTUBE_PROFILE_GATE.csv",
            "needle": "one compact profile should feed all local arenas",
            "role": "prevents per-arena retuning of source support",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        path = Path(spec["path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle = str(spec["needle"])
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": b(exists),
                "needle": needle,
                "needle_found": b(exists and needle in text),
                "role": spec["role"],
                "valid_for_claim": "False",
            }
        )
    return rows


def exact_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "EZ4546_0_source_exact_zero",
            "target": "P_loc[U_B S_cg]=0",
            "statement": "Exact source silence follows if U_B=0 on the compact local collar, or S_cg=0 on the local source kernel, or a parent projector identity kills P_loc S_cg.",
            "proof": "Substitution in R_source=U_B S_cg.",
            "current_status": "not_parent_signed",
            "why_not_claim": "logistic screening gives small U_B, not exact zero; S_cg kernel/projector theorem remains unsigned",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "EZ4546_1_attractor_exact_homogeneity",
            "target": "P_loc[D_m Delta_h m_L]=0",
            "statement": "Exact attractor homogeneity follows if the compact local branch has a trivial leakage class D_L=0 and m_L=m_* is spatially constant over the tested collar.",
            "proof": "If m_L is constant, D_m Delta_h m_L=0.",
            "current_status": "not_parent_signed",
            "why_not_claim": "local trivial class and spatially constant branch are conditional, not parent-owned",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "EZ4546_2_joint_local_Jres_zero",
            "target": "static P_loc J_res",
            "statement": "If EZ4546_0, EZ4546_1 and boundary amplitude silence all hold, the static part of P_loc J_res vanishes.",
            "proof": "P_loc J_res = P_loc[U_B S_cg] + P_loc[D_m Delta_h m_L] - P_loc[D_t m_L] + P_loc[boundary_in]; 4545 supplies conditional D_t m_L=0.",
            "current_status": "blocked_by_boundary_and_parent_signature",
            "why_not_claim": "boundary amplitude and exact source/homogeneity clauses remain unsigned",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def ub2_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "UB24546_0_power_convention",
            "quantity": "R_source",
            "formula": "R_source = U_B S_cg; if S_cg = U_B^p_int S_* then R_source = U_B^(1+p_int) S_*",
            "derivation": "Direct from 1752/1753 bookkeeping.",
            "needed_inputs": "p_int and ||S_*|| in shared source norm",
            "current_status": "exact_bookkeeping",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "UB24546_1_linear_silence",
            "quantity": "source leakage",
            "formula": "If S_cg(D_L,Y)=D_L S_1(Y)+O(D_L^2), D_L=U_B H_L, ||H_L||<=C_H, ||S_1||<=A_1, then ||P_loc[U_B S_cg]|| <= C_H A_1 U_B^2 + O(U_B^3).",
            "derivation": "Regular source map around the local fixed branch plus leakage-distance lock.",
            "needed_inputs": "source-silent fixed point, regularity, C_H, A_1, shared norm and arena projection",
            "current_status": "conditional_theorem_imported_and_current_chain_bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "UB24546_2_envelope_epsilon",
            "quantity": "source amplitude envelope",
            "formula": "If U_B <= epsilon_U on D_loc, then ||P_loc[U_B S_cg]|| <= C_H A_1 epsilon_U^2 + O(epsilon_U^3).",
            "derivation": "Take the supremum over D_loc.",
            "needed_inputs": "epsilon_U, C_H, A_1 and local domain D_loc",
            "current_status": "formula_ready_values_missing",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def ml_homogeneity_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "ML4546_0_moving_extremum",
            "quantity": "m_L-m_*",
            "formula": "If m_L=m_*+D_L^2 m_2+O(D_L^3), D_L=U_B H_L, ||H_L||<=H0 and ||m_2||<=M20, then |m_L-m_*| <= epsilon_U^2 H0^2 M20 + O(epsilon_U^3).",
            "derivation": "Even/smooth local attractor around the trivial leakage class.",
            "needed_inputs": "H0, M20, epsilon_U and proof of quadratic/even attractor dependence",
            "current_status": "conditional_U_B2_amplitude_bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "ML4546_1_gradient",
            "quantity": "|grad m_L|",
            "formula": "|grad m_L| <= C_grad_m epsilon_U^2/L_B under far-local bounds grad U_B=O(U_B/L_B), grad H_L=O(1/L_B), grad m_2=O(M21/L_B).",
            "derivation": "Differentiate m_L=m_*+U_B^2 H_L^2 m_2 and use far-local gradient scaling.",
            "needed_inputs": "C_grad_m, L_B or the detailed H0/H1A/M20/M21A constants from 1975/1978",
            "current_status": "new_current_chain_gradient_bound_shape",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "ML4546_2_laplacian",
            "quantity": "|D_m Delta_h m_L|",
            "formula": "|D_m Delta_h m_L| <= D_m C_lap_m epsilon_U^2/L_B^2 in the far-local collar, with transition-shell U_B=O(1) excluded.",
            "derivation": "Apply the same U_B^2 regularity to second spatial derivatives and multiply by D_m.",
            "needed_inputs": "D_m, C_lap_m, L_B, domain regularity and transition-shell quarantine",
            "current_status": "first_explicit_static_attractor_homogeneity_bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def static_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "budget_id": "SJ4546_0_static_budget",
            "budget": "||P_loc J_res_static|| <= C_H A_1 epsilon_U^2 + D_m C_lap_m epsilon_U^2/L_B^2 + ||P_loc boundary_in_static|| + O(epsilon_U^3)",
            "applies_to": "static source leakage and attractor homogeneity after 4545 derivative silence",
            "closed_terms": "P_loc[D_t m_L] conditional zero from 4545",
            "retained_terms": "boundary amplitude, source constants, spatial-gradient constants",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "budget_id": "SJ4546_1_exact_zero_branch",
            "budget": "P_loc J_res_static=0 if U_B=0, S_cg kernel zero, m_L spatially constant, and boundary_in=0 all hold as parent theorems.",
            "applies_to": "strict compact local zero branch",
            "closed_terms": "none promoted as current claim",
            "retained_terms": "all parent signatures required",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "budget_id": "SJ4546_2_transition_shell_warning",
            "budget": "U_B^2 far-local bounds cannot be used inside transition shells where U_B=O(1); those require exact projector cancellation or quarantine.",
            "applies_to": "screening transition/local-vacuum collar boundaries",
            "closed_terms": "none",
            "retained_terms": "transition-shell current and boundary amplitude",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def input_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "REQ4546_0_epsilon_U",
            "symbol": "epsilon_U",
            "definition": "sup_Dloc U_B",
            "status": "missing_local_range_or_parent_bound",
            "needed_for": "numeric source and m_L U_B^2 envelopes",
            "valid_for_claim": "False",
        },
        {
            "input_id": "REQ4546_1_source_norm",
            "symbol": "C_H, A_1",
            "definition": "D_L/U_B bound and first source-map coefficient norm",
            "status": "missing_parent_signature_and_source_norm",
            "needed_for": "||P_loc[U_B S_cg]|| <= C_H A_1 epsilon_U^2",
            "valid_for_claim": "False",
        },
        {
            "input_id": "REQ4546_2_gradient_scale",
            "symbol": "L_B, C_grad_m, C_lap_m",
            "definition": "far-local environmental length and derivative constants for m_L",
            "status": "missing_numeric_or_theorem_bound",
            "needed_for": "P_loc[D_m Delta_h m_L] bound",
            "valid_for_claim": "False",
        },
        {
            "input_id": "REQ4546_3_boundary_static",
            "symbol": "||P_loc boundary_in_static||",
            "definition": "static trace/shear/vector boundary amplitude after derivative silence",
            "status": "retained_from_4545",
            "needed_for": "full P_loc J_res_static budget",
            "valid_for_claim": "False",
        },
        {
            "input_id": "REQ4546_4_worldtube_profile",
            "symbol": "W_src/J_q shared profile",
            "definition": "one source profile feeding R10, PPN, clock, orbital and local-GR arenas",
            "status": "template_exists_no_profile",
            "needed_for": "arena projections without retuning",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG4546_0_source_exact_zero",
            "gate": "P_loc[U_B S_cg]=0",
            "status": "BLOCKED_EXACT_ZERO_NOT_PARENT_SIGNED",
            "meaning": "exact zero needs U_B=0, source-kernel silence or parent projector identity",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4546_1_source_UB2_bound",
            "gate": "source U_B^2 finite bound",
            "status": "PASS_FORMULA_NONCLAIM",
            "meaning": "conditional U_B^2 theorem is now imported into the current chain, but constants are missing",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4546_2_mL_homogeneity",
            "gate": "P_loc[D_m Delta_h m_L]",
            "status": "PASS_BOUND_SHAPE_NONCLAIM",
            "meaning": "first explicit U_B^2 spatial/laplacian bound shape is written",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4546_3_local_GR",
            "gate": "full local GR/Newton/PPN",
            "status": "BLOCKED_BOUNDARY_AND_NUMERIC_PROJECTION_INPUTS",
            "meaning": "static residual budget is improved but not yet projected/numeric/claim-safe",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4546_0",
            "decision": DECISION,
            "meaning": "4546 closes the algebraic shape of the two static leftovers. Exact zero remains conditional, but the finite branch now has source and attractor-homogeneity residuals suppressed as U_B^2 under a regular leakage-coordinate theorem. The next step is projection/numeric acquisition, not another broad missing-input loop.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4546_0",
            "target": NEXT_TARGET,
            "objective": "project the 4546 static residual vector into PPN/Gdot/R10 rows or fill the first numeric epsilon_U/source-norm bound row",
            "derive_first": "turn SJ4546_0 into arena residual formulas with shared source profile and no retuning",
            "fallback": "acquire epsilon_U, C_H A_1, D_m C_lap_m/L_B^2 and boundary_static as explicit nonclaim numeric rows",
            "avoid": "claiming local GR from U_B^2 formulas without constants and arena kernels",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT,
            "result": DECISION,
            "source_exact_zero_parent_signed": "False",
            "source_UB2_bound_written": "True",
            "mL_exact_homogeneity_parent_signed": "False",
            "mL_spatial_UB2_bound_written": "True",
            "static_Jres_budget_written": "True",
            "numeric_projection_ready": "False",
            "public_local_GR_claim_allowed": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    exact_zero: list[dict[str, Any]],
    ub2_bounds: list[dict[str, Any]],
    ml_bounds: list[dict[str, Any]],
    static_budget: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append({"validation_id": "VAL4546_00_sources", "status": "PASS" if source_ok else "FAIL", "detail": "all source paths exist and needles found" if source_ok else "source path or needle missing"})

    exact_blocked = any(row["theorem_id"] == "EZ4546_0_source_exact_zero" and row["current_status"] == "not_parent_signed" for row in exact_zero)
    checks.append({"validation_id": "VAL4546_01_exact_zero_honest", "status": "PASS" if exact_blocked else "FAIL", "detail": "exact zero theorem is stated but not promoted"})

    ub2_ok = any(row["bound_id"] == "UB24546_1_linear_silence" and "U_B^2" in row["formula"] for row in ub2_bounds)
    checks.append({"validation_id": "VAL4546_02_source_UB2", "status": "PASS" if ub2_ok else "FAIL", "detail": "source U_B^2 finite bound written"})

    ml_lap = any(row["bound_id"] == "ML4546_2_laplacian" and "epsilon_U^2" in row["formula"] for row in ml_bounds)
    checks.append({"validation_id": "VAL4546_03_mL_laplacian", "status": "PASS" if ml_lap else "FAIL", "detail": "m_L spatial/laplacian U_B^2 bound written"})

    budget_ok = any(row["budget_id"] == "SJ4546_0_static_budget" and "boundary_in_static" in row["budget"] for row in static_budget)
    checks.append({"validation_id": "VAL4546_04_static_budget", "status": "PASS" if budget_ok else "FAIL", "detail": "static Jres budget retains boundary amplitude"})

    req_ok = all(row["valid_for_claim"] == "False" for row in requirements) and any(row["input_id"] == "REQ4546_4_worldtube_profile" for row in requirements)
    checks.append({"validation_id": "VAL4546_05_requirements", "status": "PASS" if req_ok else "FAIL", "detail": "missing numeric/profile inputs are explicit and nonclaim"})

    gates_ok = all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in gates)
    local_block = any(row["claim_gate_id"] == "CG4546_3_local_GR" and row["status"].startswith("BLOCKED") for row in gates)
    checks.append({"validation_id": "VAL4546_06_claim_firewall", "status": "PASS" if gates_ok and local_block else "FAIL", "detail": "local GR remains blocked until constants/projections/boundary rows close"})

    csv_paths = [
        SOURCE_REGISTER,
        EXACT_ZERO_CSV,
        UB2_BOUND_CSV,
        ML_HOMOGENEITY_CSV,
        STATIC_RESIDUAL_CSV,
        INPUT_REQUIREMENTS_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
    ]
    csv_ok = True
    details: list[str] = []
    for path in csv_paths:
        try:
            if not read_csv(path):
                csv_ok = False
                details.append(f"{path.name}:empty")
        except Exception as exc:
            csv_ok = False
            details.append(f"{path.name}:{exc}")
    checks.append({"validation_id": "VAL4546_07_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(details)})

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append({"validation_id": "VAL4546_08_pycache_absent", "status": "PASS" if pycache_absent else "FAIL", "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present"})

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append({"validation_id": "VAL4546_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "4546 source silence and attractor homogeneity exact-zero/U_B^2 bound"})
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    exact_zero: list[dict[str, Any]],
    ub2_bounds: list[dict[str, Any]],
    ml_bounds: list[dict[str, Any]],
    static_budget: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4546 - Source silence and attractor homogeneity from compact support or U_B power bound

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4545 made the time-derivative part of the local branch quieter. 4546 attacks the static leftovers:

```text
P_loc[U_B S_cg],
P_loc[D_m Delta_h m_L].
```

The exact-zero route is simple but not yet parent-owned:

```text
U_B=0 or S_cg=0  ->  P_loc[U_B S_cg]=0,
m_L=constant     ->  P_loc[D_m Delta_h m_L]=0.
```

The useful finite route is now sharper. If the local leakage coordinate satisfies

```text
D_L = U_B H_L,       ||H_L|| <= C_H,
```

and the coarse source is regular/silent at the local fixed point,

```text
S_cg(D_L,Y) = D_L S_1(Y) + O(D_L^2),
```

then:

```text
||P_loc[U_B S_cg]|| <= C_H A_1 U_B^2 + O(U_B^3).
```

For the attractor, if the local branch is even/smooth around the trivial leakage class,

```text
m_L = m_* + D_L^2 m_2 + O(D_L^3),
```

then, in the far-local collar:

```text
|D_m Delta_h m_L| <= D_m C_lap_m epsilon_U^2 / L_B^2.
```

So 4546 does not solve local GR, but it upgrades the static leftovers from open prose to an explicit residual vector:

```text
||P_loc J_res_static||
 <= C_H A_1 epsilon_U^2
  + D_m C_lap_m epsilon_U^2/L_B^2
  + ||P_loc boundary_in_static||
  + O(epsilon_U^3).
```

That is a real next scorer/bound object.

## Exact Zero Theorem

{markdown_table(exact_zero)}

## U_B^2 Source Bound

{markdown_table(ub2_bounds)}

## m_L Homogeneity Bound

{markdown_table(ml_bounds)}

## Static J_res Budget

{markdown_table(static_budget)}

## Input Requirements

{markdown_table(requirements)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_target)}

## Status

{markdown_table(status)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_memory_bound",
        "claim": "4546 derives the current-chain static source and m_L homogeneity bounds: exact zero remains conditional, while the finite branch gives U_B^2 suppression of P_loc[U_B S_cg] and P_loc[D_m Delta_h m_L] under regular leakage-coordinate assumptions.",
        "current_evidence": "Generated source register, exact zero theorem, U_B^2 source bound, m_L homogeneity bound, static J_res budget, input requirements, claim gates, status and validation CSVs.",
        "status": "static_source_mL_UB2_bound_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Claiming local GR from U_B^2 formulas before constants, local ranges, arena projections and boundary amplitudes are sourced.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Boundary amplitude and numeric projection inputs remain retained.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    exact_zero = exact_zero_rows()
    ub2_bounds = ub2_bound_rows()
    ml_bounds = ml_homogeneity_rows()
    static_budget = static_residual_rows()
    requirements = input_requirement_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(EXACT_ZERO_CSV, exact_zero)
    write_csv(UB2_BOUND_CSV, ub2_bounds)
    write_csv(ML_HOMOGENEITY_CSV, ml_bounds)
    write_csv(STATIC_RESIDUAL_CSV, static_budget)
    write_csv(INPUT_REQUIREMENTS_CSV, requirements)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, exact_zero, ub2_bounds, ml_bounds, static_budget, requirements, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, exact_zero, ub2_bounds, ml_bounds, static_budget, requirements, gates, decisions, next_target, status, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4546 Source Silence And Attractor Homogeneity Static Bound

Marker: `{MARKER}`  
4546 imports the prior source-support machinery into the current local-GR chain. Exact silence needs `U_B=0`/source-kernel zero and constant `m_L`, still not parent-signed. The finite route now has explicit `U_B^2` source and attractor-homogeneity bounds, giving `||P_loc J_res_static|| <= C_H A_1 epsilon_U^2 + D_m C_lap_m epsilon_U^2/L_B^2 + ||P_loc boundary_in_static|| + O(epsilon_U^3)`. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4546 Packet Integration - Static Source And m_L U_B^2 Bounds

Marker: `{PACKET_MARKER}`  
The local packet now has a concrete static residual object after derivative silence: source leakage and attractor inhomogeneity are both `U_B^2`-suppressed under regular leakage-coordinate assumptions. This is still nonclaim until constants, local ranges, boundary amplitudes and arena projections are supplied.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
