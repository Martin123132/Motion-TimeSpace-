from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4570"
CLAIM_ID = "L-412"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_ML_ATTRACTOR_ALAP_4570"
MARKER = "PPC4161_PARENT_ML_ATTRACTOR_EQUATION_OR_ALAP_SOURCE_ROW_4570"
PACKET_MARKER = "PPC4161_PACKET_PARENT_ML_ATTRACTOR_ALAP_ZERO_SOURCE_ROW_4570"
DECISION = "A_LAP_HOMOGENEOUS_ATTRACTOR_ZERO_CONDITIONAL_INVARIANT_RESIDUAL_ROW_RETAINED_NONCLAIM"
NEXT_TARGET = "4571-Y5-R2FR-static-boundary-nohair-or-B_boundary-profile-kernel-row.md"

FORMAL_PATH = FORMAL / "586-PPC4161-parent-mL-attractor-equation-or-A-lap-source-row.md"
DOC_PATH = POST / "4570-Y5-R2FR-parent-mL-attractor-equation-or-A_lap-source-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4569 = FORMAL / "585-PPC4161-parent-source-current-covariance-or-A-src-zero-source-norm-row.md"
CSV_4569_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4569_AJ_REDUCTION_AFTER_ASRC.csv"
CSV_4569_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4569_STATUS.csv"
CSV_4569_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4569_NEXT_TARGET.csv"
CSV_4568_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4568_AJ_COEFFICIENT_OWNER_LAW.csv"
CSV_4568_ZERO_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4568_AJ_ZERO_ROUTE_AUDIT.csv"
CSV_4546_ML = SOURCE_DIR / "P8_Y5_R2FR_4546_ML_HOMOGENEITY_BOUND.csv"
CSV_4546_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4546_EXACT_ZERO_THEOREM.csv"
CSV_4546_BUDGET = SOURCE_DIR / "P8_Y5_R2FR_4546_STATIC_JRES_BUDGET.csv"
CSV_4545_ATTRACTOR = SOURCE_DIR / "P8_Y5_R2FR_4545_ATTRACTOR_STATIONARITY_MAP.csv"
CSV_4545_WARD = SOURCE_DIR / "P8_Y5_R2FR_4545_WARD_HAMILTONIAN_DERIVATION.csv"
CSV_4545_RETAINED = SOURCE_DIR / "P8_Y5_R2FR_4545_RETAINED_RESIDUALS.csv"
CSV_1751_VARIATION = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1751_VARIATION_THEOREM.csv"
CSV_1751_RESIDUAL = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1751_FINITE_RESIDUAL_VECTOR.csv"
CSV_1751_CONTRACT = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1751_ELLIPTIC_FUNCTIONAL_OWNERSHIP_CONTRACT.csv"
CSV_1978_ML_ENVELOPE = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1978_ML_DERIVATIVE_ENVELOPE_INPUTS.csv"
CSV_1978_ACQ = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1978_ACQUISITION_REQUIREMENTS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4570_SOURCE_REGISTER.csv"
ATTRACTOR_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4570_ML_ATTRACTOR_ZERO_THEOREM.csv"
ALAP_BRANCH_CSV = SOURCE_DIR / "P8_Y5_R2FR_4570_ALAP_BRANCH_VERDICT.csv"
INVARIANT_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4570_INVARIANT_LAPLACIAN_RESIDUAL_ROW.csv"
ALAP_SOURCE_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4570_ALAP_SOURCE_ROW.csv"
STATIC_REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4570_STATIC_REDUCTION_AFTER_ALAP.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4570_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4570_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4570_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4570_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4570_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
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
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4570_00_4569_doc", "4569 formal A_J reduction", DOC_4569, "A_J_eff^std = A_lap"),
        ("SRC4570_01_4569_reduction", "4569 reduction CSV", CSV_4569_REDUCTION, "AJ4569_0_standard_reduction"),
        ("SRC4570_02_4569_status", "4569 A_J status", CSV_4569_STATUS, "REDUCED_TO_A_lap_ON_STANDARD_BRANCH"),
        ("SRC4570_03_4569_next", "4569 selected next target", CSV_4569_NEXT, "parent-mL-attractor-equation"),
        ("SRC4570_04_4568_owner", "4568 A_lap owner", CSV_4568_OWNER, "OWN4568_1_A_lap"),
        ("SRC4570_05_4568_zero_audit", "4568 A_lap zero route", CSV_4568_ZERO_AUDIT, "ZR4568_1_attractor_homogeneity"),
        ("SRC4570_06_4546_mL_bound", "4546 m_L homogeneity bound", CSV_4546_ML, "ML4546_2_laplacian"),
        ("SRC4570_07_4546_exact_zero", "4546 exact homogeneity zero", CSV_4546_ZERO, "EZ4546_1_attractor_exact_homogeneity"),
        ("SRC4570_08_4546_static_budget", "4546 static Jres budget", CSV_4546_BUDGET, "SJ4546_0_static_budget"),
        ("SRC4570_09_4545_attractor", "4545 attractor stationarity map", CSV_4545_ATTRACTOR, "PZ4545_3_attractor_stationarity"),
        ("SRC4570_10_4545_ward", "4545 Hamiltonian chain rule", CSV_4545_WARD, "WH4545_2_attractor_chain_rule"),
        ("SRC4570_11_4545_retained", "4545 retained spatial amplitude", CSV_4545_RETAINED, "RR4545_1_attractor_homogeneity"),
        ("SRC4570_12_1751_variation", "1751 elliptic nohair theorem", CSV_1751_VARIATION, "VAR1751_4_nohair_branch"),
        ("SRC4570_13_1751_residual", "1751 m_L drift residual", CSV_1751_RESIDUAL, "RV1751_1_mL_drift"),
        ("SRC4570_14_1751_contract", "1751 elliptic functional contract", CSV_1751_CONTRACT, "EFO1751_0_functional_candidate"),
        ("SRC4570_15_1978_mL_envelope", "1978 m_L derivative envelope", CSV_1978_ML_ENVELOPE, "MLE1978_5_mL_derivative"),
        ("SRC4570_16_1978_acquisition", "1978 m_L envelope acquisition", CSV_1978_ACQ, "REQ1978_3_mL_envelope"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in specs:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needle": needle,
                "needle_found": b(needle in text),
                "role": "4570 A_lap attractor/homogeneity derivation chain",
                "valid_for_claim": "False",
            }
        )
    return rows


def attractor_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "ML4570_0_owner_import",
            "statement": "Import 4568 owner row A_lap := D_m C_lap_m/L_B^2 for |D_m Delta_h m_L| after U_B^2 factoring.",
            "derivation": "4546 supplies |D_m Delta_h m_L| <= D_m C_lap_m epsilon_U^2/L_B^2; 4568 defines A_lap as the coefficient multiplying epsilon_U^2.",
            "status": "OWNER_FORMULA_IMPORTED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "ML4570_1_constant_invariant_chain",
            "statement": "If m_L=m_*(I_A,Q_B), nabla_i I_A=0, nabla_i Q_B=0 and m_* has no explicit x-dependence on the local collar, then nabla_i m_L=0 and Delta_h m_L=0.",
            "derivation": "Chain rule: nabla_i m_L = m_{*,A} nabla_i I_A + m_{*,Q} nabla_i Q_B. Every term vanishes under collar-constant invariants; therefore the Laplacian also vanishes.",
            "status": "CONDITIONAL_HOMOGENEOUS_ATTRACTOR_ZERO",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "ML4570_2_gapped_attractor_nohair",
            "statement": "If eta_L:=m_L-m_*^0 obeys (-D_m Delta_h + mu_L) eta_L = J_L with D_m>0, mu_L>=mu_min>0, J_L=0, fixed zero mode and no boundary flux, then eta_L=0 and Delta_h m_L=0.",
            "derivation": "Multiply the elliptic equation by eta_L and integrate: int D_m|grad eta_L|^2 + int mu_L eta_L^2 = boundary_flux + int J_L eta_L. With zero right-hand side, positivity forces eta_L=0.",
            "status": "EXACT_CONDITIONAL_ENERGY_IDENTITY_ZERO",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "ML4570_3_Alap_standard_zero",
            "statement": "A_lap^std=0 on the homogeneous/gapped m_L-attractor branch.",
            "derivation": "A_lap is the coefficient of D_m Delta_h m_L after U_B^2 factoring; ML4570_1 or ML4570_2 sets Delta_h m_L=0 on the same collar.",
            "status": "CLOSED_CONDITIONAL_STANDARD_ATTRACTOR_BRANCH",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "ML4570_4_no_smuggling_variable_coefficients",
            "statement": "If D_m varies, the full variational residual is R_mL_full = D_m Delta_h m_L + grad D_m dot grad m_L; A_lap=0 alone does not silence R_mL_full.",
            "derivation": "1751 variable-coefficient variation gives -nabla_i(D_m nabla^i delta_m), which expands to -D_m Delta_h delta_m - grad D_m dot grad delta_m.",
            "status": "VARIABLE_COEFFICIENT_FIREWALL",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def branch_verdict_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "verdict_id": "BV4570_0_homogeneous_attractor",
            "branch_scope": "compact stationary standard Dq/Hperp branch plus homogeneous or gapped m_L attractor collar",
            "A_lap_status": "CLOSED_CONDITIONAL_STANDARD_ATTRACTOR_BRANCH",
            "formula": "A_lap^std=0",
            "reason": "constant-invariant chain or gapped elliptic nohair sets Delta_h m_L=0.",
            "firewall": "Do not use this zero if local invariants, D_m, target m_* or boundary flux vary across the tested collar.",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "verdict_id": "BV4570_1_inhomogeneous_attractor",
            "branch_scope": "environmental-gradient, transition-shell, variable-coefficient or open-boundary branch",
            "A_lap_status": "INVARIANT_RESIDUAL_ROW_RETAINED",
            "formula": "A_lap^inhom <= D_m C_lap_m/L_B^2 or sharper invariant-chain residual",
            "reason": "4546 gives the U_B^2/L_B^2 envelope; 1751 prevents hiding m_L drift or grad D_m residuals.",
            "firewall": "This row is not numeric until D_m, C_lap_m, L_B and invariant-gradient constants are sourced.",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "verdict_id": "BV4570_2_public_claim",
            "branch_scope": "public local-GR/Newton/PPN/R10 claim",
            "A_lap_status": "PUBLIC_CLAIM_BLOCKED",
            "formula": "bulk A_J can be zero only on a private branch; boundary, higher-order and arena kernels remain",
            "reason": "4569 removed A_src and 4570 conditionally removes A_lap, but B_boundary_static and K_a are still retained.",
            "firewall": "No local-GR, WEP, PPN, clock, orbital or R10 pass may be inferred from 4570 alone.",
            "valid_for_claim": "False",
        },
    ]


def invariant_residual_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "IR4570_0_chain_rule_laplacian",
            "quantity": "Delta_h m_L",
            "law": "Delta_h m_L = m_A Delta_h I_A + m_Q Delta_h Q_B + m_AB grad I_A.grad I_B + 2 m_AQ grad I_A.grad Q_B + m_QQ |grad Q_B|^2",
            "meaning": "If the attractor target is not spatially constant, the surviving A_lap is controlled by invariant Laplacians and gradient-squared terms.",
            "required_inputs": "bounds on m_A,m_Q,m_AB,m_AQ,m_QQ and local invariant gradient/Laplacian norms",
            "status": "DERIVED_SYMBOLIC_RESIDUAL_ROW",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "IR4570_1_envelope_bound",
            "quantity": "A_lap^inhom",
            "law": "A_lap^inhom <= D_m C_lap_m/L_B^2",
            "meaning": "4546's far-local U_B^2 regularity remains the compact fallback coefficient after A_src is removed.",
            "required_inputs": "D_m; C_lap_m; L_B; domain regularity; transition-shell quarantine",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "IR4570_2_variable_Dm_firewall",
            "quantity": "R_mL_full",
            "law": "R_mL_full = D_m Delta_h m_L + grad D_m dot grad m_L",
            "meaning": "A full variational local residual must include coefficient-gradient drift if D_m is not constant on the collar.",
            "required_inputs": "grad D_m bound or parent proof D_m=constant in the tested collar",
            "status": "NO_SMUGGLING_FIREWALL",
            "valid_for_claim": "False",
        },
    ]


def alap_source_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "source_row_id": "AL4570_0_standard_zero",
            "coefficient": "A_lap^std",
            "value_or_bound": "0",
            "units": "same as D_m Delta_h m_L coefficient after epsilon_U^2 factoring",
            "source_authority": "ML4570_1 or ML4570_2 plus 4568 owner law",
            "status": "THEOREM_ZERO_CONDITIONAL_PRIVATE_BRANCH",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "source_row_id": "AL4570_1_inhomogeneous_bound",
            "coefficient": "A_lap^inhom",
            "value_or_bound": "D_m C_lap_m/L_B^2",
            "units": "same as D_m Delta_h m_L coefficient after epsilon_U^2 factoring",
            "source_authority": str(CSV_4546_ML),
            "status": "SYMBOLIC_NONCLAIM_VALUES_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "source_row_id": "AL4570_2_full_variational_residual",
            "coefficient": "R_mL_full",
            "value_or_bound": "D_m C_lap_m/L_B^2 + C_gradD C_gradm/L_B^2",
            "units": "full local residual units",
            "source_authority": str(CSV_1751_VARIATION),
            "status": "SYMBOLIC_FIREWALL_VALUES_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def static_reduction_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "reduction_id": "SR4570_0_bulk_zero_branch",
            "before": "A_J_eff^std = A_lap after 4569",
            "after": "A_J_eff^bulk-zero = 0",
            "condition": "4569 standard A_src zero plus 4570 homogeneous/gapped A_lap zero on the same collar",
            "status": "BULK_STATIC_TOOTH_REMOVED_CONDITIONALLY",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "reduction_id": "SR4570_1_static_bound",
            "before": "||P_loc J_res_static|| <= epsilon_U^2 A_lap + B_boundary_static + O(epsilon_U^3)",
            "after": "||P_loc J_res_static|| <= B_boundary_static + O(epsilon_U^3)",
            "condition": "bulk-zero branch only; boundary profile is not absorbed into A_lap",
            "status": "STATIC_BOUND_SHARPENED_CONDITIONALLY",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "reduction_id": "SR4570_2_inhomogeneous_branch",
            "before": "A_lap left as vague C_lap_m",
            "after": "A_lap controlled by invariant Laplacian/gradient row plus D_m C_lap_m/L_B^2 fallback",
            "condition": "environmental-gradient or variable-coefficient branch",
            "status": "FINITE_BRANCH_SHARPENED",
            "valid_for_claim": "False",
        },
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4570_0_same_branch",
            "requirement": "A_src^std=0 and A_lap^std=0 must hold on the same local collar and branch selector",
            "current_status": "PASS_PRIVATE_BRANCH_ONLY",
            "failure_mode": "combining zeros from incompatible branch assumptions",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4570_1_Dm_constancy",
            "requirement": "prove D_m constant or include grad D_m dot grad m_L in the residual",
            "current_status": "FIREWALL_WRITTEN",
            "failure_mode": "using a simplified D_m Delta_h operator while coefficients vary",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4570_2_boundary",
            "requirement": "derive or source B_boundary_static and arena kernels K_a",
            "current_status": "OPEN_NEXT_TARGET",
            "failure_mode": "claiming local GR after bulk teeth vanish while boundary and projection channels remain",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4570_3_public_tests",
            "requirement": "PPN/R10/clock/orbital scoring needs boundary, higher-order and projection rows even if A_J bulk is zero",
            "current_status": "BLOCKED_FOR_PUBLIC_CLAIM",
            "failure_mode": "turning private bulk-zero theorem into empirical pass evidence",
            "valid_for_claim": "False",
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "decision_id": "DEC4570_0_Alap_zero",
            "reason": "The parent m_L attractor route can close A_lap on a homogeneous/gapped collar: constant invariants or elliptic nohair force Delta_h m_L=0.",
            "next_action": "use A_lap^std=0 only in the private same-branch bulk-zero packet",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "decision_id": "DEC4570_1_inhomogeneous_retained",
            "reason": "If local invariants, target m_* or coefficients vary, the chain-rule Laplacian and grad D_m residual survive.",
            "next_action": "retain invariant-gradient and D_m C_lap_m/L_B^2 rows as nonclaim finite branch",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "decision_id": "DEC4570_2_next",
            "reason": "With A_src and A_lap conditionally removed from the same private branch, the live static obstruction is boundary/nohair plus arena kernels.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4570_0",
            "next_target": NEXT_TARGET,
            "objective": "try to prove static boundary nohair or derive source-backed B_boundary_static and K_a profile rows",
            "derive_first": "show boundary_in_static is zero/routed-silent for the same compact stationary standard collar",
            "fallback": "keep B_boundary,a and K_a as finite nonclaim rows per PPN/R10/clock/orbital arena",
            "avoid": "using bulk A_J zero to erase boundary, higher-order, transition-shell or projection-kernel residuals",
            "valid_for_claim": "False",
            "generated_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "status_id": "STAT4570_0_A_lap",
            "item": "A_lap",
            "status": "CLOSED_CONDITIONAL_STANDARD_ATTRACTOR_BRANCH",
            "note": "A_lap^std=0 follows if m_L is homogeneous by constant invariants or gapped nohair on the same local collar.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "status_id": "STAT4570_1_A_J_eff",
            "item": "A_J_eff",
            "status": "BULK_ZERO_ON_PRIVATE_SAME_BRANCH",
            "note": "4569 A_src^std=0 plus 4570 A_lap^std=0 gives A_J_eff^bulk-zero=0, but boundary remains.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "status_id": "STAT4570_2_public_claim",
            "item": "local_GR_public_claim",
            "status": "BLOCKED",
            "note": "Boundary profiles, projection kernels, higher-order terms and parent branch selector remain required.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    branch_verdict: list[dict[str, Any]],
    invariant_rows: list[dict[str, Any]],
    source_rows_out: list[dict[str, Any]],
    static_reduction: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_paths = [
        SOURCE_REGISTER,
        ATTRACTOR_THEOREM_CSV,
        ALAP_BRANCH_CSV,
        INVARIANT_ROW_CSV,
        ALAP_SOURCE_ROW_CSV,
        STATIC_REDUCTION_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        FORMAL_PATH,
        DOC_PATH,
    ]
    csv_paths = [
        SOURCE_REGISTER,
        ATTRACTOR_THEOREM_CSV,
        ALAP_BRANCH_CSV,
        INVARIANT_ROW_CSV,
        ALAP_SOURCE_ROW_CSV,
        STATIC_REDUCTION_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
    ]
    text_blob = "\n".join(str(row) for row in theorem + branch_verdict + invariant_rows + source_rows_out + static_reduction + promotion + decisions + next_target + status)
    source_paths_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    theorem_tokens_ok = all(
        token in text_blob
        for token in [
            "A_lap^std=0",
            "Delta_h m_L=0",
            "A_J_eff^bulk-zero = 0",
            "R_mL_full",
            "grad D_m dot grad m_L",
        ]
    )
    branch_tokens_ok = all(
        token in text_blob
        for token in [
            "CLOSED_CONDITIONAL_STANDARD_ATTRACTOR_BRANCH",
            "INVARIANT_RESIDUAL_ROW_RETAINED",
            "PUBLIC_CLAIM_BLOCKED",
        ]
    )
    generated_paths_ok = all(path.exists() for path in generated_paths)
    csv_parse_ok = True
    csv_parse_detail: list[str] = []
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            ok = bool(parsed)
            csv_parse_ok = csv_parse_ok and ok
            csv_parse_detail.append(f"{path.name}:{len(parsed)}")
        except Exception as exc:  # pragma: no cover - validation report only
            csv_parse_ok = False
            csv_parse_detail.append(f"{path.name}:ERROR:{exc}")
    all_new_rows = sources + theorem + branch_verdict + invariant_rows + source_rows_out + static_reduction + promotion + decisions + next_target + status
    nonclaim_ok = all(str(row.get("valid_for_claim", "False")) == "False" for row in all_new_rows)
    next_ok = bool(next_target) and next_target[0].get("next_target") == NEXT_TARGET
    pycache_absent = not (POST / "scripts" / "__pycache__").exists()
    rows = [
        {
            "check_id": "VAL4570_0_source_paths",
            "status": "PASS" if source_paths_ok else "FAIL",
            "detail": "all cited source paths exist and needles were found",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4570_1_generated_paths",
            "status": "PASS" if generated_paths_ok else "FAIL",
            "detail": "; ".join(str(path) for path in generated_paths),
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4570_2_csv_parse",
            "status": "PASS" if csv_parse_ok else "FAIL",
            "detail": "; ".join(csv_parse_detail),
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4570_3_theorem_tokens",
            "status": "PASS" if theorem_tokens_ok else "FAIL",
            "detail": "required A_lap zero, bulk-zero and variable-coefficient firewall tokens present",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4570_4_branch_verdict",
            "status": "PASS" if branch_tokens_ok else "FAIL",
            "detail": "standard A_lap closed, inhomogeneous retained and public blocked statuses present",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4570_5_nonclaim_firewall",
            "status": "PASS" if nonclaim_ok else "FAIL",
            "detail": "all generated rows keep valid_for_claim=false",
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4570_6_next_target",
            "status": "PASS" if next_ok else "FAIL",
            "detail": NEXT_TARGET,
            "valid_for_claim": "False",
        },
        {
            "check_id": "VAL4570_7_pycache_absent",
            "status": "PASS" if pycache_absent else "FAIL",
            "detail": str(POST / "scripts" / "__pycache__"),
            "valid_for_claim": "False",
        },
    ]
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL4570_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": "False",
        }
    )
    return rows


def formal_markdown(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    branch_verdict: list[dict[str, Any]],
    invariant_rows: list[dict[str, Any]],
    source_rows_out: list[dict[str, Any]],
    static_reduction: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 586 - PPC4161 Parent m_L Attractor Equation Or A_lap Source Row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4569 reduced the standard-branch c_Gamma static bulk problem to:

```text
A_J_eff^std = A_lap.
```

4570 derives the exact condition under which this remaining bulk tooth vanishes. If the same local collar has either a constant-invariant attractor

```text
m_L=m_*(I_A,Q_B),
nabla_i I_A=0,
nabla_i Q_B=0,
```

or a gapped elliptic no-hair equation

```text
(-D_m Delta_h + mu_L)(m_L-m_*^0)=0
```

with positive gap, fixed zero mode and no boundary flux, then:

```text
Delta_h m_L=0,
A_lap^std=0,
A_J_eff^bulk-zero = 0.
```

This is not a public local-GR claim. It is a private same-branch bulk-zero theorem. Boundary amplitude, higher-order terms, transition-shells and arena kernels still remain.

## Inhomogeneous Branch

If local invariants or coefficients vary, the survivor is no longer vague:

```text
Delta_h m_L = m_A Delta_h I_A + m_Q Delta_h Q_B
            + m_AB grad I_A.grad I_B
            + 2 m_AQ grad I_A.grad Q_B
            + m_QQ |grad Q_B|^2.
```

And if `D_m` varies, the full residual is:

```text
R_mL_full = D_m Delta_h m_L + grad D_m dot grad m_L.
```

So the fallback is an invariant-gradient source row, plus the compact 4546 envelope `A_lap^inhom <= D_m C_lap_m/L_B^2`, not a hidden closure axiom.

## Source Register

{markdown_table(sources)}

## m_L Attractor Zero Theorem

{markdown_table(theorem)}

## A_lap Branch Verdict

{markdown_table(branch_verdict)}

## Invariant Laplacian Residual Rows

{markdown_table(invariant_rows)}

## A_lap Source Rows

{markdown_table(source_rows_out)}

## Static Reduction After A_lap

{markdown_table(static_reduction)}

## Promotion Gates

{markdown_table(promotion)}

## Decisions

{markdown_table(decisions)}

## Next Target

{markdown_table(next_target)}

## Status

{markdown_table(status)}

## Validation

{markdown_table(validation)}
"""


def post_markdown(
    theorem: list[dict[str, Any]],
    branch_verdict: list[dict[str, Any]],
    invariant_rows: list[dict[str, Any]],
    source_rows_out: list[dict[str, Any]],
    static_reduction: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4570 - Parent m_L Attractor Equation Or A_lap Source Row

Marker: `{MARKER}`

Decision: `{DECISION}`

## What Changed

The remaining bulk tooth after 4569 was:

```text
A_J_eff^std = A_lap.
```

4570 derives the clean local condition:

```text
Delta_h m_L=0 => A_lap^std=0 => A_J_eff^bulk-zero = 0.
```

This is valid only on the same private compact stationary standard branch when `m_L` is homogeneous by constant invariants or by a gapped no-flux attractor equation. If the collar is inhomogeneous, the branch keeps:

```text
A_lap^inhom <= D_m C_lap_m/L_B^2,
R_mL_full = D_m Delta_h m_L + grad D_m dot grad m_L.
```

## m_L Attractor Theorem

{markdown_table(theorem)}

## Branch Verdict

{markdown_table(branch_verdict)}

## Invariant Residual Rows

{markdown_table(invariant_rows)}

## A_lap Source Rows

{markdown_table(source_rows_out)}

## Static Reduction

{markdown_table(static_reduction)}

## Decisions

{markdown_table(decisions)}

## Validation

{markdown_table(validation)}

## Files Written

- `{FORMAL_PATH}`
- `{SOURCE_REGISTER}`
- `{ATTRACTOR_THEOREM_CSV}`
- `{ALAP_BRANCH_CSV}`
- `{INVARIANT_ROW_CSV}`
- `{ALAP_SOURCE_ROW_CSV}`
- `{STATIC_REDUCTION_CSV}`
- `{PROMOTION_CSV}`
- `{DECISION_CSV}`
- `{NEXT_CSV}`
- `{STATUS_CSV}`
- `{VALIDATION_PATH}`

## Next Target

`{NEXT_TARGET}`
"""


def append_section_once(path: Path, marker: str, section: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        if text and not text.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + section.strip() + "\n")


def append_claim_once() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else [
        "claim_id",
        "domain",
        "claim",
        "current_evidence",
        "status",
        "next_test",
        "key_risk",
        "sector",
        "evidence",
        "next_action",
        "risk",
    ]
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4570 derives the conditional m_L attractor/homogeneity route that sets A_lap^std=0 on a homogeneous/gapped local collar, while retaining invariant-gradient and variable-D_m residual rows for inhomogeneous branches.",
        "current_evidence": "Generated source register, m_L attractor theorem, A_lap branch verdict, invariant residual rows, A_lap source rows, static reduction rows, promotion gates, status and validation CSVs.",
        "status": "A_lap_homogeneous_attractor_zero_conditional_invariant_residual_retained_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Combining A_src and A_lap zeros from different branches, or treating bulk-zero A_J as full c_Gamma/local-GR closure while boundary and projection kernels remain open.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "This is private same-branch bulk progress only; public PPN/R10/clock/orbital/local-GR claims still need boundary and arena kernel closure.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writerow(claim_row)


def main() -> None:
    now = utc_now()
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    sources = source_rows()
    theorem = attractor_theorem_rows(now)
    branch_verdict = branch_verdict_rows(now)
    invariant_rows = invariant_residual_rows(now)
    source_rows_out = alap_source_rows(now)
    static_reduction = static_reduction_rows(now)
    promotion = promotion_rows(now)
    decisions = decision_rows(now)
    next_target = next_rows(now)
    status = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ATTRACTOR_THEOREM_CSV, theorem)
    write_csv(ALAP_BRANCH_CSV, branch_verdict)
    write_csv(INVARIANT_ROW_CSV, invariant_rows)
    write_csv(ALAP_SOURCE_ROW_CSV, source_rows_out)
    write_csv(STATIC_REDUCTION_CSV, static_reduction)
    write_csv(PROMOTION_CSV, promotion)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    validation = validation_rows(
        sources,
        theorem,
        branch_verdict,
        invariant_rows,
        source_rows_out,
        static_reduction,
        promotion,
        decisions,
        next_target,
        status,
    )
    write_csv(VALIDATION_PATH, validation)

    FORMAL_PATH.write_text(
        formal_markdown(
            sources,
            theorem,
            branch_verdict,
            invariant_rows,
            source_rows_out,
            static_reduction,
            promotion,
            decisions,
            next_target,
            status,
            validation,
        ),
        encoding="utf-8",
        newline="\n",
    )
    DOC_PATH.write_text(
        post_markdown(theorem, branch_verdict, invariant_rows, source_rows_out, static_reduction, decisions, validation),
        encoding="utf-8",
        newline="\n",
    )

    validation = validation_rows(
        sources,
        theorem,
        branch_verdict,
        invariant_rows,
        source_rows_out,
        static_reduction,
        promotion,
        decisions,
        next_target,
        status,
    )
    write_csv(VALIDATION_PATH, validation)
    FORMAL_PATH.write_text(
        formal_markdown(
            sources,
            theorem,
            branch_verdict,
            invariant_rows,
            source_rows_out,
            static_reduction,
            promotion,
            decisions,
            next_target,
            status,
            validation,
        ),
        encoding="utf-8",
        newline="\n",
    )
    DOC_PATH.write_text(
        post_markdown(theorem, branch_verdict, invariant_rows, source_rows_out, static_reduction, decisions, validation),
        encoding="utf-8",
        newline="\n",
    )

    append_section_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4570 Parent m_L Attractor / A_lap Branch Verdict

Marker: `{MARKER}`

The 4569 reduction `A_J_eff^std=A_lap` now has a conditional attractor closure. On the same compact stationary standard collar, if `m_L=m_*(I_A,Q_B)` with spatially constant invariants, or if `eta_L=m_L-m_*^0` obeys a positive gapped no-flux elliptic equation, then:

```text
Delta_h m_L=0,
A_lap^std=0,
A_J_eff^bulk-zero=0.
```

The inhomogeneous branch is retained as an invariant-gradient row, and variable `D_m` adds `grad D_m dot grad m_L`. Boundary amplitude and arena kernels remain the next live obstruction. Next target: `{NEXT_TARGET}`.
""",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4570 Packet Integration - A_lap Homogeneous Attractor Zero

Marker: `{PACKET_MARKER}`

Packet rule: inside the private same-branch compact stationary standard collar, `A_lap^std=0` if the parent m_L attractor is homogeneous by constant invariants or by a gapped no-flux elliptic nohair equation. Combined with 4569, this gives `A_J_eff^bulk-zero=0`, but only for the bulk static coefficient. Inhomogeneous collars retain `A_lap^inhom <= D_m C_lap_m/L_B^2` plus invariant-gradient and variable-`D_m` residual rows. Next target: `{NEXT_TARGET}`.
""",
    )
    append_claim_once()

    if pycache.exists():
        shutil.rmtree(pycache)

    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
