from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4619"
CLAIM_ID = "L-461"
BRANCH_ID = "MTS_R2FR_Y5_F2_MEMORY_COEFFICIENT_OWNER_4619"
MARKER = "PPC4161_F2_MEMORY_COEFFICIENT_OWNER_OR_ZMEM_M2MEM_SOURCE_ROW_4619"
PACKET_MARKER = "PPC4161_PACKET_F2_MEMORY_COEFFICIENT_OWNER_4619"
DECISION = "F2_MEMORY_COEFFICIENT_OWNER_TEST_DERIVED_MIXED_OPERATOR_COUNTERMODEL_AND_SOURCE_ROWS_READY_NONCLAIM"
NEXT_TARGET = "4620-Y5-R2FR-kappa-memF2-owner-zero-or-first-numeric-coefficient-row.md"

DOC_PATH = POST / "4619-Y5-R2FR-F2-memory-coefficient-owner-or-Zmem-M2mem-source-row.md"
FORMAL_PATH = FORMAL / "635-PPC4161-F2-memory-coefficient-owner-or-Zmem-M2mem-source-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4619_SOURCE_REGISTER.csv"
OWNER_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4619_F2_MEMORY_OWNER_THEOREM.csv"
OWNER_CLASS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4619_F2_MEMORY_OWNER_CLASSIFICATION.csv"
SOURCE_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4619_KAPPA_MEMF2_ZMEM_M2MEM_SOURCE_ROWS_NONCLAIM.csv"
CMEMORY_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4619_CMEMORY_F2_UPDATE_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4619_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4619_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4619_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4619_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4619_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4619_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4619_VALIDATION.csv"

CSV_4618_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4618_NEXT_TARGET.csv"
CSV_4618_VALUE = SOURCE_DIR / "P8_Y5_R2FR_4618_CMEMORY_F2_VALUE_ROW_NONCLAIM.csv"
CSV_4618_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4618_MEMORY_CLASS_SCALAR_NOHAIR_THEOREM.csv"
CSV_4616_PROOF = SOURCE_DIR / "P8_Y5_R2FR_4616_VISIBLE_IMAGE_PROOF_ATTEMPT.csv"
CSV_1108_THEOREM = SOURCE_DIR / "P8_Y5_R10_1108_EM_F2_IMAGE_THEOREM_ATTEMPT.csv"
CSV_1099_THEOREM = SOURCE_DIR / "P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv"
CSV_1099_EXCLUSION = SOURCE_DIR / "P8_Y5_R10_1099_NO_EXTRA_F2_EXCLUSION_AUDIT.csv"
CSV_1099_COUNTER = SOURCE_DIR / "P8_Y5_R10_1099_COUNTEREXAMPLE_LEDGER.csv"
CSV_1109_THEOREM = SOURCE_DIR / "P8_Y5_R10_1109_LAMBDA_F2_THEOREM_ATTEMPT.csv"
CSV_1109_FINITE = SOURCE_DIR / "P8_Y5_R10_1109_FINITE_ALPHA_ROWS_NONCLAIM.csv"
CSV_4437_DERIVATION = SOURCE_DIR / "P8_Y5_R2FR_4437_DERIVATION_ROWS.csv"
CSV_4437_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4437_EM_COUPLING_ZERO_ROWS.csv"
CSV_4437_SURVIVOR = SOURCE_DIR / "P8_Y5_R2FR_4437_EM_COUPLING_SURVIVOR_ROWS.csv"
CSV_4506_OPERATOR = SOURCE_DIR / "P8_Y5_R2FR_4506_MEMORY_OPERATOR_SIGNATURE.csv"
CSV_4506_BODY = SOURCE_DIR / "P8_Y5_R2FR_4506_BODY_CHARGE_INPUT_ROW.csv"

PUBLIC_STAGE = Path("D:/Users/ollet/Desktop/Motion-TimeSpace-public-stage")
BACKUP_REPO = Path("D:/Users/ollet/Desktop/laptop-back-up-")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


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
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
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
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines)


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for number, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return number
    return 0


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    suffix = "\n" if text.endswith("\n") or not text else "\n\n"
    write_text(path, text + suffix + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not path.exists() or not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--porcelain"], text=True, capture_output=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4619_00_4618_next", CSV_4618_NEXT, "4619-Y5-R2FR-F2-memory-coefficient-owner-or-Zmem-M2mem-source-row.md", "4618 selected coefficient owner or Zmem/M2mem row."),
        ("SRC4619_01_4618_value", CSV_4618_VALUE, "CMF4618_0_first_value_contract", "4618 C_memory_F2 value contract."),
        ("SRC4619_02_4618_theorem", CSV_4618_THEOREM, "MCS4618_2_no_target_zero", "4618 no-target route."),
        ("SRC4619_03_4616_countermodel", CSV_4616_PROOF, "VIP4616_2_scalar_functional_countermodel", "4616 scalar F2 countermodel."),
        ("SRC4619_04_1108_image", CSV_1108_THEOREM, "EMF1108_3_no_hidden_f", "1108 hidden F2 target obstruction."),
        ("SRC4619_05_1099_owner", CSV_1099_THEOREM, "UEM1099_2_counterterm", "1099 scalar gauge-kinetic counterterm."),
        ("SRC4619_06_1099_exclusion", CSV_1099_EXCLUSION, "EXC1099_1_U1_gauge", "1099 U1/covariance exclusion audit."),
        ("SRC4619_07_1099_counter", CSV_1099_COUNTER, "CX1099_1_fX", "1099 hidden fX F2 counterexample."),
        ("SRC4619_08_1109_lambda", CSV_1109_THEOREM, "LFA1109_5_hidden_or_running_lambda", "1109 finite lambda/F2 branch."),
        ("SRC4619_09_1109_finite", CSV_1109_FINITE, "FAL1109_1_lambda_vertical", "1109 finite alpha coefficient row."),
        ("SRC4619_10_4437_identity", CSV_4437_DERIVATION, "SOC4437_0_same_owner_identity", "4437 same-owner identity."),
        ("SRC4619_11_4437_branch_zero", CSV_4437_ZERO, "ZERO4437_0_C_XF2", "4437 branch C_XF2 zero."),
        ("SRC4619_12_4437_survivor", CSV_4437_SURVIVOR, "SURV4437_1_global_unique_F2", "4437 global F2 survivor."),
        ("SRC4619_13_4506_operator", CSV_4506_OPERATOR, "MOP4506_0_quadratic_action", "4506 memory operator row."),
        ("SRC4619_14_4506_body", CSV_4506_BODY, "BCIN4506_0_memory_density", "4506 memory body-charge row."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": needle in text,
            "line": line_of(path, needle),
            "role": role,
            "valid_for_claim": False,
            "timestamp_utc": now,
        })
    return rows


def owner_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "FMO4619_0_no_Hom_zero",
            "claim_piece": "no memory-to-F2 coefficient owner",
            "formal_statement": "If the parent visible EM coefficient algebra is the image of Gen_EM=C_P N_Q <F_Q,F_Q> only, and m_mem is not an argument of that image, then Hom_parent(m_mem,Coeff(F_Q^2)) is absent and partial_m lambda_F2=0.",
            "derivation": "A memory dependence of the Maxwell kinetic normalization requires a target coefficient object. If the target object is absent or exhausted by fixed parent norm data, differentiating with respect to m_mem is ill-typed.",
            "result": "EXACT_CONDITIONAL_NO_TARGET_THEOREM",
            "current_status": "PARENT_IMAGE_AND_NO_HOM_UNSIGNED",
            "source_refs": "MCS4618_2_no_target_zero;EMF1108_3_no_hidden_f;VIP4616_0_exact_image_zero_theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "FMO4619_1_fixed_branch_import",
            "claim_piece": "fixed q-basic standard branch zero",
            "formal_statement": "Inside the fixed q-basic standard visible branch, lambda_A and g_J are fixed before variation, no independent F2 slot is present, and memory is not a visible EM coefficient argument; hence C_memory_F2=0 branch-conditionally.",
            "derivation": "4437 proves C_XF2=0 and d lambda_A=0 inside the fixed q-basic standard branch. 4619 specializes that branch zero to the memory/class scalar coefficient.",
            "result": "BRANCH_ZERO_IMPORTED_NOT_GLOBAL",
            "current_status": "PRIVATE_BRANCH_ONLY",
            "source_refs": "ZERO4437_0_C_XF2;SOC4437_1_fixed_qbasic_branch_zero",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "FMO4619_2_mixed_operator_countermodel",
            "claim_piece": "memory-F2 mixed operator",
            "formal_statement": "If m_mem is a scalar and Coeff(F_Q^2) is a legal target, DeltaS_memF2=-(1/4) int mu_obs kappa_memF2 m_mem F_Q^2 is diffeomorphism and U1 gauge invariant.",
            "derivation": "F_Q^2 is a visible gauge-invariant scalar density and m_mem is scalar. Ordinary symmetry therefore does not forbid a mixed memory-F2 coefficient.",
            "result": "COUNTERMODEL_RETAINED",
            "current_status": "MIXED_COEFFICIENT_ROW_REQUIRED_IF_NO_TARGET_FAILS",
            "source_refs": "EXC1099_1_U1_gauge;CX1099_1_fX;VIP4616_2_scalar_functional_countermodel",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "FMO4619_3_finite_derivative_law",
            "claim_piece": "finite C_memory_F2 law",
            "formal_statement": "For Z_Q_eff=Z_Q0+kappa_memF2 delta_m+O(delta_m^2), C_memory_F2=|kappa_memF2/Z_Q_eff| Delta_v m_mem at first order.",
            "derivation": "C_memory_F2=|partial_m ln lambda_F2| Delta_v m_mem and partial_m ln Z_Q_eff=kappa_memF2/Z_Q_eff at the selected branch.",
            "result": "EXACT_FINITE_BRANCH_IDENTITY",
            "current_status": "VALUES_MISSING",
            "source_refs": "CMF4618_0_first_value_contract;SOC4437_0_same_owner_identity;FAL1109_1_lambda_vertical",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "FMO4619_4_nohair_source_law",
            "claim_piece": "Delta_v m_mem source bound",
            "formal_statement": "If the mixed coefficient survives, Delta_v m_mem is bounded by the memory positive-operator/body-charge row using Z_mem, M2_mem, B_mem, C_mem, J_mem, Q_boundary_mem and the body profile.",
            "derivation": "4618 and 4506 give the amplitude law for delta_m; 4619 attaches it to the EM coefficient derivative rather than leaving it as a generic memory residual.",
            "result": "SOURCE_ROW_CONTRACT_READY",
            "current_status": "ZMEM_M2MEM_KAPPA_VALUES_MISSING",
            "source_refs": "BCIN4506_0_memory_density;MOP4506_0_quadratic_action;CMF4618_0_first_value_contract",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def owner_class_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "class_id": "OWN4619_0_absent",
            "case": "no memory Hom into Coeff(F_Q^2)",
            "normal_form": "Hom_parent(m_mem,Coeff(F_Q^2))=empty",
            "effect": "partial_m lambda_F2=0 and C_memory_F2=0",
            "status": "EXACT_IF_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "class_id": "OWN4619_1_fixed_branch",
            "case": "fixed q-basic standard visible branch",
            "normal_form": "lambda_A, g_J, charge labels and readout fixed before variation",
            "effect": "C_memory_F2=0 only inside the private fixed branch",
            "status": "BRANCH_ZERO_NOT_GLOBAL",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "class_id": "OWN4619_2_linear_mixed",
            "case": "linear memory-F2 mixed coefficient",
            "normal_form": "DeltaS=-(1/4) int mu_obs kappa_memF2 delta_m F_Q^2",
            "effect": "C_memory_F2=|kappa_memF2/Z_Q_eff| Delta_v m_mem",
            "status": "FINITE_BRANCH_RETAINED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "class_id": "OWN4619_3_extremum",
            "case": "branch extremum/double-zero",
            "normal_form": "Z_Q_eff=Z_Q0+1/2 lambda2 delta_m^2+...",
            "effect": "first-order C_memory_F2=0; quadratic/profile residual remains",
            "status": "EXTREMUM_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "class_id": "OWN4619_4_readout_rad",
            "case": "readout/radiative memory re-entry",
            "normal_form": "delta lambda_eff(mu,readout,m_mem) F_Q^2",
            "effect": "C_readout_F2 or C_rad_F2 remains in H_XF2",
            "status": "RADIOUT_CLOSURE_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def source_value_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "KMF4619_0_kappa_memF2",
            "symbol": "kappa_memF2",
            "definition": "linear memory/class scalar coefficient in the Maxwell kinetic normalization",
            "normal_form": "DeltaS_memF2=-(1/4) int mu_obs kappa_memF2 delta_m F_Q^2",
            "value": "MISSING_NUMERIC_OR_DERIVED_ZERO",
            "units": "Maxwell coefficient per memory-field unit",
            "required_source": "parent action term, no-target theorem, or explicit coefficient derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "KMF4619_1_ZQeff_lower",
            "symbol": "Z_Q_eff_min",
            "definition": "positive lower bound on effective Maxwell kinetic normalization",
            "normal_form": "Z_Q_eff=C_P N_Q+lambda_A+delta_lambda",
            "value": "MISSING_POSITIVE_DENOMINATOR_BOUND",
            "units": "dimensionless Maxwell coefficient",
            "required_source": "parent norm/calibrated normalization branch and no zero-crossing bound",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "KMF4619_2_Zmem",
            "symbol": "Z_mem",
            "definition": "memory scalar kinetic coefficient in the positive operator",
            "normal_form": "L_mem=-nabla_i Z_mem nabla^i + M2_mem",
            "value": "MISSING_SOURCE_BACKED_VALUE",
            "units": "memory kinetic units",
            "required_source": "parent memory action/Hessian with units and sign",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "KMF4619_3_M2mem",
            "symbol": "M2_mem",
            "definition": "positive memory scalar mass/gap term",
            "normal_form": "lambda_mem=sqrt(Z_mem/M2_mem)",
            "value": "MISSING_SOURCE_BACKED_VALUE",
            "units": "memory mass-squared units",
            "required_source": "parent memory Hessian, zero-mode removal and branch sign",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "KMF4619_4_rhomem",
            "symbol": "rho_mem",
            "definition": "memory source density driving delta_m",
            "normal_form": "rho_mem=B_mem R_obs + C_mem T + J_mem",
            "value": "MISSING_SOURCE_OR_ZERO_PROOF",
            "units": "memory source density units",
            "required_source": "B_mem, C_mem, J_mem, body profile and source paths",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "KMF4619_5_Qboundary",
            "symbol": "Q_boundary_mem",
            "definition": "boundary charge/flux contribution to memory amplitude",
            "normal_form": "Delta_v m_mem includes |Q_boundary_mem|/(4*pi |Z_mem|)",
            "value": "MISSING_BOUNDARY_ZERO_OR_VALUE",
            "units": "memory boundary charge units",
            "required_source": "boundary no-flux theorem or source-backed boundary row",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def cmemory_update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": "CMU4619_0_first_order_identity",
            "quantity": "C_memory_F2",
            "formula": "C_memory_F2=|kappa_memF2/Z_Q_eff| Delta_v m_mem",
            "status": "FINITE_IDENTITY_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "update_id": "CMU4619_1_nohair_amplitude",
            "quantity": "Delta_v m_mem",
            "formula": "Delta_v m_mem <= [exp(R_body/lambda_mem) int_body |rho_mem| dV + |Q_boundary_mem|]/(4*pi |Z_mem|)",
            "status": "AMPLITUDE_BOUND_IMPORTED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "update_id": "CMU4619_2_zero_switch",
            "quantity": "C_memory_F2",
            "formula": "C_memory_F2=0 if kappa_memF2=0 or Delta_v m_mem=0 on the same branch",
            "status": "ZERO_SWITCH_EXACT_PARENT_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4619_0_no_symmetry_ban",
            "rule": "Do not use diffeomorphism covariance or visible U1 gauge invariance to forbid m_mem F_Q^2.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4619_1_no_branch_globalization",
            "rule": "Fixed q-basic standard-branch C_XF2=0 cannot be promoted to a global dynamic memory-F2 zero.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4619_2_no_bound_inversion",
            "rule": "Do not infer kappa_memF2, Z_mem, M2_mem, or rho_mem by fitting local-test bounds backward.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4619_0_no_Hom_signature",
            "claim_blocked": "partial_m lambda_F2=0",
            "missing_signature": "parent says memory/class scalar has no Hom into Coeff(F_Q^2)",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4619_1_kappa_value",
            "claim_blocked": "finite C_memory_F2 scoring",
            "missing_signature": "kappa_memF2 or theorem-zero coefficient owner",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4619_2_operator_values",
            "claim_blocked": "Delta_v m_mem amplitude bound",
            "missing_signature": "Z_mem, M2_mem, rho_mem, Q_boundary_mem and body profile with source paths",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4619_0_zero_branch",
            "requirement": "no memory Hom into Coeff(F_Q^2), or same-branch kappa_memF2=0 plus readout/radiative closure",
            "current_status": "BLOCKED_PARENT_SIGNATURE_UNSIGNED",
            "sources_valid": sources_ok,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4619_1_finite_branch",
            "requirement": "source-backed kappa_memF2, Z_Q_eff_min, Z_mem, M2_mem, rho_mem, Q_boundary_mem, body profile and arena K/tau projections",
            "current_status": "BLOCKED_VALUE_ROWS_MISSING",
            "sources_valid": sources_ok,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4619_0",
            "decision": DECISION,
            "what_changed": "The memory-F2 coupling now has an owner test and a first-order coefficient law; it is no longer a generic alpha/memory caveat.",
            "claim_status": "NONCLAIM_PRIVATE_DERIVATION_STAGE",
            "exact_path": "prove Hom_parent(m_mem,Coeff(F_Q^2)) is absent or kappa_memF2=0 on the same branch",
            "fallback_path": "source kappa_memF2 plus Zmem/M2mem/rho/boundary values for C_memory_F2",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "status": "PRIVATE_NONCLAIM_DERIVATION_ADVANCE",
            "summary": "F2 memory coefficient owner test and mixed-operator finite law are written; next is kappa_memF2 zero/value or Zmem/M2mem source row.",
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": now,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "timestamp_utc": now,
            "next_target": NEXT_TARGET,
            "why": "4619 isolates the first missing coefficient as kappa_memF2 unless no-Hom/no-target closes.",
            "derive_path": "prove kappa_memF2=0 by parent operator-domain/no-Hom or branch extremum",
            "fallback_path": "fill a source-backed kappa_memF2 row or the Z_mem/M2_mem/rho_mem amplitude inputs",
            "claim_allowed": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4619 - F2 Memory Coefficient Owner Or Zmem/M2mem Source Row

Generated UTC: `{now}`

Marker: `{MARKER}`

## Result

4619 isolates the owner of the first memory/F2 coefficient:

```text
DeltaS_memF2 = -1/4 int mu_obs kappa_memF2 delta_m F_Q^2
C_memory_F2 = |kappa_memF2/Z_Q_eff| Delta_v m_mem
```

The exact zero route is:

```text
Hom_parent(m_mem, Coeff(F_Q^2)) = empty
or kappa_memF2 = 0 on the same parent branch.
```

The finite route is now a real source row, not a vibe:

```text
Delta_v m_mem <= [exp(R_body/lambda_mem) int_body |rho_mem| dV + |Q_boundary_mem|]/(4*pi |Z_mem|)
rho_mem = B_mem R_obs + C_mem T + J_mem.
```

No local-GR, Maxwell, clock, R10, PPN, WEP or Newton claim fires.

## Source Register

{markdown_table(tables["sources"])}

## F2 Memory Owner Theorem

{markdown_table(tables["owner_theorem"])}

## F2 Memory Owner Classification

{markdown_table(tables["owner_class"])}

## Kappa/Zmem/M2mem Source Rows Nonclaim

{markdown_table(tables["source_rows"])}

## C_memory_F2 Update Rows

{markdown_table(tables["cmemory_update"])}

## Controls

{markdown_table(tables["controls"])}

## Claim Blockers

{markdown_table(tables["blockers"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Decision

{markdown_table(tables["decision"])}

## Status

{markdown_table(tables["status"])}

## Next Target

`{NEXT_TARGET}`
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 Formal Addendum 635 - F2 Memory Coefficient Owner Or Zmem/M2mem Source Row

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

## Owner Test

The memory contribution to the EM kinetic Hom row is zero if

```text
Hom_parent(m_mem, Coeff(F_Q^2)) = empty
```

or if the same parent branch gives `kappa_memF2=0`.

## Mixed Operator Countermodel

If `m_mem` is a scalar and `Coeff(F_Q^2)` is a legal target,

```text
DeltaS_memF2 = -1/4 int mu_obs kappa_memF2 delta_m F_Q^2
```

is covariant and visible-U1 gauge invariant. Therefore ordinary symmetry cannot kill it.

## Finite Law

At first order,

```text
C_memory_F2 = |kappa_memF2/Z_Q_eff| Delta_v m_mem.
```

The next target is `{NEXT_TARGET}`.
"""


def append_claim_once() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "sector": "local_gr_empirical_interface",
        "claim": "4619 derives the memory-F2 coefficient owner test and the first-order finite law C_memory_F2=|kappa_memF2/Z_Q_eff| Delta_v m_mem, while retaining source rows as nonclaim.",
        "evidence": "Generated owner theorem rows, owner classification, kappa/Zmem/M2mem source rows, C_memory updates, controls, blockers, promotion gates, decision, status, next target and validation.",
        "status": "F2_memory_owner_test_and_kappa_source_rows_nonclaim",
        "next_action": NEXT_TARGET,
        "risk": "Banning m_mem F_Q^2 by ordinary symmetry, globalizing a fixed-branch zero, or fitting coefficient rows backward from empirical bounds.",
        "owner": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "No b_alpha, Maxwell, WEP, clock, R10, Newton or local-GR pass until kappa_memF2 is parent-zero/source-backed and Zmem/M2mem/source/boundary rows are real.",
    }
    existing = read_text(CLAIMS_PATH)
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not existing.endswith("\n"):
            handle.write("\n")
        writer.writerow(row)


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        })

    missing_sources = [row["source_id"] for row in tables["sources"] if not row["path_exists"] or not row["needle_found"]]
    add("VAL4619_00_sources_exist_and_needles_found", not missing_sources, "missing: " + ",".join(missing_sources) if missing_sources else "all cited paths/needles found")

    csv_paths = [
        SOURCE_REGISTER, OWNER_THEOREM_CSV, OWNER_CLASS_CSV, SOURCE_ROW_CSV, CMEMORY_UPDATE_CSV,
        CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV,
    ]
    csv_ok = True
    details: list[str] = []
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4619_01_csv_parse", csv_ok, ";".join(details))

    theorem_text = "\n".join(str(row) for row in tables["owner_theorem"])
    class_text = "\n".join(str(row) for row in tables["owner_class"])
    source_text = "\n".join(str(row) for row in tables["source_rows"])
    update_text = "\n".join(str(row) for row in tables["cmemory_update"])
    add("VAL4619_02_no_Hom_theorem", "Hom_parent(m_mem,Coeff(F_Q^2)) is absent" in theorem_text and "partial_m lambda_F2=0" in theorem_text, "no-Hom theorem present")
    add("VAL4619_03_countermodel", "kappa_memF2 m_mem F_Q^2" in theorem_text and "COUNTERMODEL_RETAINED" in theorem_text, "mixed operator countermodel present")
    add("VAL4619_04_finite_identity", "kappa_memF2/Z_Q_eff" in theorem_text and "C_memory_F2" in update_text, "finite derivative identity present")
    add("VAL4619_05_classification", "linear memory-F2 mixed coefficient" in class_text and "readout/radiative memory re-entry" in class_text, "owner classification present")
    add("VAL4619_06_source_rows", "kappa_memF2" in source_text and "Z_mem" in source_text and "M2_mem" in source_text and "Q_boundary_mem" in source_text, "source rows present")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "claim_pass", "empirical_pass_claimed", "score_ready"} and value is True:
                    all_false = False
    add("VAL4619_07_no_claim_true", all_false, "no generated row promotes a claim")
    add("VAL4619_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4619_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4619_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4619_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4619_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4619_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4619_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4619_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4619_OVERALL", all(row["status"] == "PASS" for row in rows), "4619 F2 memory coefficient owner checkpoint")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "owner_theorem": owner_theorem_rows(now),
        "owner_class": owner_class_rows(now),
        "source_rows": source_value_rows(now),
        "cmemory_update": cmemory_update_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(OWNER_THEOREM_CSV, tables["owner_theorem"])
    write_csv(OWNER_CLASS_CSV, tables["owner_class"])
    write_csv(SOURCE_ROW_CSV, tables["source_rows"])
    write_csv(CMEMORY_UPDATE_CSV, tables["cmemory_update"])
    write_csv(CONTROL_CSV, tables["controls"])
    write_csv(BLOCKERS_CSV, tables["blockers"])
    write_csv(PROMOTION_CSV, tables["promotion"])
    write_csv(DECISION_CSV, tables["decision"])
    write_csv(STATUS_CSV, tables["status"])
    write_csv(NEXT_CSV, tables["next"])
    write_text(DOC_PATH, build_doc(now, tables))
    write_text(FORMAL_PATH, build_formal(now))
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## PPC4161 Local Addendum - F2 Memory Coefficient Owner Or Zmem/M2mem Source Row

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

4619 isolates the first memory/F2 owner test. `C_memory_F2=0` follows if `Hom_parent(m_mem,Coeff(F_Q^2))=empty` or the same branch gives `kappa_memF2=0`. Otherwise the finite law is `C_memory_F2=|kappa_memF2/Z_Q_eff| Delta_v m_mem`, with `Delta_v m_mem` bounded by the `Z_mem/M2_mem/rho_mem/Q_boundary_mem` body-charge row. Ordinary covariance and visible U1 do not forbid the mixed scalar operator.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - F2 Memory Coefficient Owner Or Zmem/M2mem Source Row

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The packet now has a named first coefficient: `kappa_memF2`. The next move is to prove the parent operator-domain/no-Hom zero for that coefficient or fill the first source-backed coefficient/operator row.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4619 validation failed: {failed}")
    print(f"4619 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
