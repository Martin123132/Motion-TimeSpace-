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

CHECKPOINT = "4601"
CLAIM_ID = "L-443"
BRANCH_ID = "MTS_R2FR_Y5_BODY_CHARGE_SCORE_INPUT_INTERFACE_4601"
MARKER = "PPC4161_CX_JX_BX_BODY_CHARGE_VECTOR_TO_EMPIRICAL_SCORE_INPUTS_4601"
PACKET_MARKER = "PPC4161_PACKET_BODY_CHARGE_SCORE_INPUT_INTERFACE_4601"
DECISION = "BODY_CHARGE_SCORE_INPUT_INTERFACE_READY_NONCLAIM"
NEXT_TARGET = "4602-Y5-R2FR-ZX-MX2-lambdaX-range-owner-or-body-charge-score-first-fill.md"

DOC_PATH = POST / "4601-Y5-R2FR-CX-JX-BX-body-charge-vector-to-empirical-score-inputs.md"
FORMAL_PATH = FORMAL / "617-PPC4161-CX-JX-BX-body-charge-vector-to-empirical-score-inputs.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4601_SOURCE_REGISTER.csv"
SCORE_VECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4601_BODY_CHARGE_SCORE_VECTOR.csv"
OPERATOR_INPUTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4601_FIELD_OPERATOR_INPUTS.csv"
ARENA_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4601_ARENA_SCORE_MATRIX.csv"
MISSING_INPUTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4601_MISSING_INPUT_LEDGER.csv"
RUNNER_SCHEMA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4601_NONCLAIM_RUNNER_SCHEMA.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4601_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4601_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4601_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4601_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4601_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4601_VALIDATION.csv"

DOC_4600 = POST / "4600-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md"
FORMAL_616 = FORMAL / "616-PPC4161-boundary-nonHilbert-zero-or-final-CXlive-norm.md"
CSV_4600_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4600_NEXT_TARGET.csv"
CSV_4600_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4600_STATUS.csv"
CSV_4600_BODY = SOURCE_DIR / "P8_Y5_R2FR_4600_BODY_CHARGE_ENVELOPE_FINAL_CX_UPDATE.csv"
CSV_4600_INTERFACE = SOURCE_DIR / "P8_Y5_R2FR_4600_EMPIRICAL_SCORE_INPUT_INTERFACE.csv"
CSV_4600_FINAL_CX = SOURCE_DIR / "P8_Y5_R2FR_4600_FINAL_CXLIVE_NORM.csv"
CSV_4595_SCHEMA = SOURCE_DIR / "P8_Y5_R2FR_4595_FINITE_INPUT_SCHEMA.csv"
CSV_4595_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4595_OWNER_ZERO_SWITCH.csv"
CSV_4595_MEM = SOURCE_DIR / "P8_Y5_R2FR_4595_MEMORY_BODY_CHARGE_BOUND.csv"
CSV_4595_FIB = SOURCE_DIR / "P8_Y5_R2FR_4595_FIBRE_BODY_CHARGE_BOUND.csv"
CSV_4595_BMEM = SOURCE_DIR / "P8_Y5_R2FR_4595_BMEM_EFF_INSERTION.csv"
CSV_4596_J = SOURCE_DIR / "P8_Y5_R2FR_4596_JMEM_JH_REDUCED_RESIDUAL_VECTOR.csv"
CSV_4596_COEFF = SOURCE_DIR / "P8_Y5_R2FR_4596_FIRST_BODY_CHARGE_COEFFICIENT_ROWS.csv"
CSV_4597_CX = SOURCE_DIR / "P8_Y5_R2FR_4597_CX_LIVE_COEFFICIENT_ROWS.csv"
CSV_4506_BODY = SOURCE_DIR / "P8_Y5_R2FR_4506_BODY_CHARGE_INPUT_ROW.csv"
CSV_4505_GREEN = SOURCE_DIR / "P8_Y5_R2FR_4505_BODY_CHARGE_GREEN_FUNCTION_LAW.csv"
CSV_4514_INSERT = SOURCE_DIR / "P8_Y5_R2FR_4514_BODY_CHARGE_INSERTION_BOUND.csv"
CSV_4514_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4514_BMEM_EFFECTIVE_COMPONENT_VECTOR.csv"
CSV_4515_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4515_SOURCE_COUPLING_BOUND.csv"
CSV_4523_ALPHA_INPUTS = SOURCE_DIR / "P8_Y5_R2FR_4523_FIRST_ALPHA_RUNNER_INPUTS.csv"
CSV_4524_ALPHA_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4524_RESIDUAL_ALPHA_INPUT_CONTRACT.csv"
CSV_4524_ALPHA_LAW = SOURCE_DIR / "P8_Y5_R2FR_4524_FINITE_RESIDUAL_ALPHA_LAW.csv"
CSV_4594_R10 = SOURCE_DIR / "P8_Y5_R2FR_4594_R10_ORBITAL_BOUND_INTERFACE.csv"
CSV_4592_PPN = SOURCE_DIR / "P8_Y5_R2FR_4592_PPN_VECTOR_IMPACT_ROWS.csv"
CSV_4447_PPN = SOURCE_DIR / "P8_Y5_R2FR_4447_PPN_SOURCE_RESIDUAL_OUTPUT.csv"
CSV_4530_POYNTING = SOURCE_DIR / "P8_Y5_R2FR_4530_BOUNDARY_POYNTING_SPLIT.csv"
CSV_4583_EM = SOURCE_DIR / "P8_Y5_R2FR_4583_CHARGE_CURRENT_EM_READOUT_OWNER_THEOREM.csv"
CSV_4486_M2 = SOURCE_DIR / "P8_Y5_R2FR_4486_FIRST_M2K2_INPUT_ROW.csv"
CSV_4475_LAMBDA = SOURCE_DIR / "P8_Y5_R2FR_4475_LAMBDAM_SOURCE_ROW.csv"
CSV_4476_PROJECTION = SOURCE_DIR / "P8_Y5_R2FR_4476_LAMBDAM_PROJECTION_MAP.csv"

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


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for number, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return number
    return 0


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
        lines.append("| " + " | ".join(str(row.get(key, "")).replace("\n", " ").replace("|", "\\|") for key in headers) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    write_text(path, text.rstrip() + "\n\n" + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--short"], capture_output=True, text=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


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
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4601 converts the memory/fibre body-charge ledger into a concrete nonclaim empirical score-input vector: operator/range inputs, B/C/J/Q source amplitudes, arena transfer kernels, calibration rows and missing-input blockers are now separated by sector and test arena.",
        "current_evidence": "Generated body-charge score vector rows, field-operator rows, arena score matrix, runner schema, missing-input ledger, controls and validation.",
        "status": "body_charge_score_input_interface_ready_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Mistaking a schema-ready score vector for a prediction, or filling R10/PPN/clock/orbital rows from placeholders rather than parent-owned coefficients and source-backed arena kernels.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/R10/PPN claim until Z_X, M_X^2, lambda_X, B_X, C_X, J_X, Q_boundary_X, source/test charges, calibration and arena kernels are theorem-zero or numeric with source paths.",
    }
    rows.append({key: row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4601_00_4600_doc", DOC_4600, "C_X^final_live", "4600 final C_X handoff."),
        ("SRC4601_01_616_formal", FORMAL_616, "C_X^final_live", "formal 4600 final C_X statement."),
        ("SRC4601_02_4600_next", CSV_4600_NEXT, "4601-Y5-R2FR-CX-JX-BX-body-charge-vector-to-empirical-score-inputs.md", "machine-readable 4600 next target."),
        ("SRC4601_03_4600_status", CSV_4600_STATUS, "B_X/J_X/Q_boundary/Z_X/M_X^2 arena scoring", "4600 names missing body-charge scoring."),
        ("SRC4601_04_4600_body", CSV_4600_BODY, "BU4600_1_memory", "final C_X in A_mem."),
        ("SRC4601_05_4600_interface", CSV_4600_INTERFACE, "E4600_0_R10", "arena interface handoff."),
        ("SRC4601_06_4600_final_cx", CSV_4600_FINAL_CX, "C4600_4_final", "final C_X norm row."),
        ("SRC4601_07_4595_schema", CSV_4595_SCHEMA, "schema4595_0_memory_Z", "finite input schema."),
        ("SRC4601_08_4595_owner", CSV_4595_OWNER, "ZS4595_0_common_operator", "common zero switch."),
        ("SRC4601_09_4595_mem", CSV_4595_MEM, "MEM4595_2_amplitude", "memory amplitude law."),
        ("SRC4601_10_4595_fib", CSV_4595_FIB, "FIB4595_2_amplitude", "fibre amplitude law."),
        ("SRC4601_11_4595_bmem", CSV_4595_BMEM, "BM4595_5_combined", "B_mem_eff source vector."),
        ("SRC4601_12_4596_jlive", CSV_4596_J, "J4596_5_live_total", "J_X live vector."),
        ("SRC4601_13_4596_coeff", CSV_4596_COEFF, "CO4596_6_Qboundary", "first body-charge coefficient rows."),
        ("SRC4601_14_4597_cx", CSV_4597_CX, "CX4597_7_live_total", "C_X live vector ancestry."),
        ("SRC4601_15_4506_body", CSV_4506_BODY, "BCIN4506_2_zero_switch", "body-charge input row."),
        ("SRC4601_16_4505_green", CSV_4505_GREEN, "BC4505_2_absolute_bound", "Green-function amplitude bound."),
        ("SRC4601_17_4514_insert", CSV_4514_INSERT, "BCB4514_5_arena", "arena projection missing."),
        ("SRC4601_18_4514_vector", CSV_4514_VECTOR, "BMV4514_6_combined", "B_mem effective component vector."),
        ("SRC4601_19_4515_bound", CSV_4515_BOUND, "SB4515_2_amplitude", "source-coupling amplitude bound."),
        ("SRC4601_20_4523_alpha_inputs", CSV_4523_ALPHA_INPUTS, "AIR4523_0_Z", "alpha runner input blockers."),
        ("SRC4601_21_4524_alpha_contract", CSV_4524_ALPHA_CONTRACT, "RAI4524_4_mass_range", "residual alpha contract."),
        ("SRC4601_22_4524_alpha_law", CSV_4524_ALPHA_LAW, "FRA4524_4_finite_range_mode", "finite range alpha law."),
        ("SRC4601_23_4594_R10", CSV_4594_R10, "B4594_0_R10_curve", "R10 bound interface."),
        ("SRC4601_24_4592_PPN", CSV_4592_PPN, "PPN4592_7_R10_clock_WEP_orbital", "PPN side arena survivors."),
        ("SRC4601_25_4447_PPN", CSV_4447_PPN, "PPN4447_1_gamma_minus_1_source_norm", "PPN residual output."),
        ("SRC4601_26_4530_poynting", CSV_4530_POYNTING, "B4530_2_radiative_poynting_flux", "Poynting routing."),
        ("SRC4601_27_4583_EM", CSV_4583_EM, "CCO4583_4_open_dynamic_bound", "EM dynamic bound schema."),
        ("SRC4601_28_4486_M2", CSV_4486_M2, "M2I4486_3_recast_hessian_product_bound", "first M2/Hessian finite scorer input."),
        ("SRC4601_29_4475_lambda", CSV_4475_LAMBDA, "LMR4475_1_lambda_M", "lambda/range source row."),
        ("SRC4601_30_4476_projection", CSV_4476_PROJECTION, "PMAP4476_0_universal_projection", "projection map template."),
        ("SRC4601_31_claim_442", CLAIMS_PATH, "L-442", "claim-register handoff from 4600."),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": bool(line),
                "line_number": line,
                "role": role,
                "generated_utc": now,
                "valid_for_claim": False,
            }
        )
    return rows


def operator_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "operator_id": "OP4601_0_common",
            "sector": "common_X",
            "field_equation": "(-Z_X nabla^2 + M_X^2) delta_X = rho_X",
            "source_density": "rho_X = B_X R_obs + C_X^final_live T + J_X^live",
            "range_law": "lambda_X=sqrt(Z_X/M_X^2)",
            "amplitude_bound": "|A_X| <= [exp(R_body/lambda_X) int_body |rho_X| dV + |Q_boundary_X|]/(4*pi |Z_X|)",
            "zero_switch": "Z_X>0, M_X^2>0, zero modes removed, and B_X=C_X^final_live=J_X^live=Q_boundary_X=0 in the same parent branch",
            "current_status": "DERIVED_STRUCTURE_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "operator_id": "OP4601_1_memory",
            "sector": "memory",
            "field_equation": "(-Z_mem nabla^2 + M2_mem) delta_m = rho_mem",
            "source_density": "rho_mem = B_mem_eff R_obs + C_mem^final_live T + J_mem_live",
            "range_law": "lambda_mem=sqrt(Z_mem/M2_mem)",
            "amplitude_bound": "|A_mem| <= [exp(R_body/lambda_mem) int_body (|B_mem_eff||R_obs|+|C_mem^final_live||T|+|J_mem_live|) dV + |Q_boundary_mem|]/(4*pi |Z_mem|)",
            "zero_switch": "B_mem_eff=C_mem^final_live=J_mem_live=Q_boundary_mem=0 plus positive L_mem",
            "current_status": "MEMORY_SCORE_OPERATOR_READY_INPUT_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "operator_id": "OP4601_2_fibre",
            "sector": "fibre",
            "field_equation": "(-Z_h nabla^2 + M2_h) delta_h = rho_h",
            "source_density": "rho_h = B_h R_obs + C_h^final_live T + J_h_live",
            "range_law": "lambda_h=sqrt(Z_h/M2_h)",
            "amplitude_bound": "|A_h| <= [exp(R_body/lambda_h) int_body (|B_h||R_obs|+|C_h^final_live||T|+|J_h_live|) dV + |Q_boundary_h|]/(4*pi |Z_h|)",
            "zero_switch": "B_h=C_h^final_live=J_h_live=Q_boundary_h=0 plus positive L_h",
            "current_status": "FIBRE_SCORE_OPERATOR_READY_INPUT_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def score_vector_rows(now: str) -> list[dict[str, Any]]:
    component_specs = [
        ("memory", "Z_mem", "operator normalization", "4595 schema4595_0_memory_Z;4506 BCIN4506_0_memory_density", "positive numeric/source-backed value or theorem normalization"),
        ("memory", "M2_mem", "operator mass gap", "4595 schema4595_1_memory_M2;4524 RAI4524_4_mass_range", "positive numeric/source-backed value; lambda_mem convention"),
        ("memory", "lambda_mem", "range", "lambda_mem=sqrt(Z_mem/M2_mem)", "derived from Z_mem/M2_mem with units"),
        ("memory", "B_mem_eff", "curvature/source-normalization source vector", "4595 BM4595_5_combined;4514 BMV4514_6_combined", "component zeros or absolute B vector values"),
        ("memory", "C_mem^final_live", "matter-trace coupling", "4600 BU4600_1_memory;4600 C4600_4_final", "all C subblocks zero or source-backed norms"),
        ("memory", "J_mem_live", "direct/Poynting/non-Hilbert current", "4596 J4596_5_live_total", "zero certificate or flux/current profile"),
        ("memory", "Q_boundary_mem", "Green boundary charge", "4595 schema4595_5_memory_boundary;4600 BU4600_3_boundary_separation", "no-flux/topological theorem or finite boundary integral"),
        ("memory", "W_mem/body profile", "body profile and screening kernel", "4505 BC4505_2_absolute_bound;4514 BCB4514_3_amplitude", "body radius/profile/source units"),
        ("fibre", "Z_h", "operator normalization", "4595 schema4595_6_fibre_Z;4506 BCIN4506_1_fibre_density", "positive numeric/source-backed value or theorem normalization"),
        ("fibre", "M2_h", "operator mass gap", "4595 schema4595_7_fibre_M2;4524 RAI4524_4_mass_range", "positive numeric/source-backed value; lambda_h convention"),
        ("fibre", "lambda_h", "range", "lambda_h=sqrt(Z_h/M2_h)", "derived from Z_h/M2_h with units"),
        ("fibre", "B_h", "curvature/source fibre source vector", "4595 schema4595_8_fibre_B", "parent action exclusion or finite coefficient"),
        ("fibre", "C_h^final_live", "matter-trace fibre coupling", "4600 BU4600_2_fibre;4600 C4600_4_final", "all C subblocks zero or source-backed norms"),
        ("fibre", "J_h_live", "direct/Poynting/non-Hilbert fibre current", "4596 J4596_5_live_total", "zero certificate or flux/current profile"),
        ("fibre", "Q_boundary_h", "Green boundary charge", "4595 schema4595_11_fibre_boundary;4600 BU4600_3_boundary_separation", "no-flux/topological theorem or finite boundary integral"),
        ("fibre", "W_h/body profile", "body profile and screening kernel", "4505 BC4505_2_absolute_bound;4595 FIB4595_2_amplitude", "body radius/profile/source units"),
    ]
    rows = []
    for index, (sector, symbol, role, source_anchor, required) in enumerate(component_specs):
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "component_id": f"BCV4601_{index:02d}",
                "sector": sector,
                "symbol": symbol,
                "role": role,
                "source_anchor": source_anchor,
                "required_for_claim": required,
                "score_status": "MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW",
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": now,
            }
        )
    return rows


def arena_matrix_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        (
            "R10",
            "short-range inverse-square",
            "alpha_X(lambda_X) from A_X or K_R10_X Qbar_XS qbar_XT/(G_N M_S m_T M_X^2)",
            "Z_X;M_X^2;lambda_X;B_X;C_X^final_live;J_X_live;Q_boundary_X;K_R10_X;Qbar_XS;qbar_XT;alpha_bound(lambda)",
            "full source-backed alpha(lambda) curve and MTS projection convention",
        ),
        (
            "PPN",
            "gamma,beta,alpha_i,xi,zeta_i,Gdot",
            "Delta p_i <= sum_X ||K_iX|| |A_X| + direct_tail_i",
            "A_X vector;K_gamma,K_beta,K_alpha_i,K_xi,K_zeta,K_Gdot;EH principal block;survivor tails",
            "compare against GR baseline and PPN limits without absorbing into fitted G/GM",
        ),
        (
            "clock_WEP",
            "clock redshift, WEP eta, material universality",
            "Delta O <= K_C C_X^final_live + K_shadow E_shadow_projector + K_std C_X^std_weight_live + material_tail",
            "material sensitivities;clock kernels;source/test composition;standard/weight rows;shadow rows",
            "source-backed material coefficients and same-frame calibration",
        ),
        (
            "orbital_GM",
            "orbital acceleration/light-time/GM transfer",
            "Delta a/a_N = alpha_X (1+r/lambda_X) exp(-r/lambda_X) plus boundary/reference drift terms",
            "alpha_X;lambda_X;Q_boundary_X;Delta_symp_X;J_boundary_X;GM calibration rule;orbital threshold",
            "no absorption into fitted GM unless a separate nuisance/control branch is declared",
        ),
        (
            "EM_Poynting",
            "EM stress, Poynting flux, alpha_EM/current owner",
            "Delta O_EM <= K_EM(|J_X^EM_open|+|Delta_Hodge_EM_X|+|Phi_EM_rad|+|C_XF2|+|b_alpha|)",
            "same-Hodge/current owner;closed collar or Poynting flux profile;EM readout tail;units",
            "stationary no-flux theorem or sourced radiative/open-flux profile",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "arena_id": f"ASM4601_{index}",
            "arena": arena,
            "observable_target": target,
            "score_law": law,
            "required_inputs": required,
            "acceptance_gate": gate,
            "score_status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        }
        for index, (arena, target, law, required, gate) in enumerate(rows)
    ]


def missing_input_rows(now: str) -> list[dict[str, Any]]:
    blockers = [
        ("MIS4601_0_operator_range", "Z_X,M_X^2,lambda_X", "parent quadratic operator/eigenvalue with unit convention", "4602 target"),
        ("MIS4601_1_body_source_vector", "B_X,C_X^final_live,J_X_live,Q_boundary_X", "component zero certificates or finite source-backed values", "after range owner"),
        ("MIS4601_2_body_profile", "R_body,R_obs,T,W_X,screening", "body/source profile in declared units", "before any numeric amplitude"),
        ("MIS4601_3_source_test_charges", "Qbar_XS,qbar_XT,M_S,m_T,G_N", "same-frame source/test charge and calibration convention", "before R10 alpha"),
        ("MIS4601_4_arena_kernels", "K_R10,K_PPN,K_clock,K_orbit,K_EM", "transfer operators with dimensions and baseline convention", "before scoring"),
        ("MIS4601_5_external_bounds", "alpha_bound(lambda),PPN/clock/orbital thresholds", "source-backed bounds or official tables", "before pass/fail claim"),
        ("MIS4601_6_EM_flux", "Phi_EM_rad,Delta_Hodge_EM,C_XF2,b_alpha", "stationary no-flux theorem or finite EM/Poynting profile", "before EM branch scoring"),
        ("MIS4601_7_no_cancellation", "component signs/correlation", "parent-owned cancellation if not using absolute sums", "default absolute envelope"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "missing_id": missing_id,
            "missing_input": missing_input,
            "required_evidence": evidence,
            "priority": priority,
            "current_status": "MISSING_BLOCKS_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        }
        for missing_id, missing_input, evidence, priority in blockers
    ]


def runner_schema_rows(now: str) -> list[dict[str, Any]]:
    columns = [
        ("run_id", "string", "unique run tag"),
        ("sector", "enum(memory,fibre)", "which X sector is scored"),
        ("arena", "enum(R10,PPN,clock_WEP,orbital_GM,EM_Poynting)", "test arena"),
        ("Z_X", "numeric_or_THEOREM_ZERO", "operator normalization"),
        ("M2_X", "numeric_or_THEOREM_ZERO", "operator mass gap"),
        ("lambda_X", "numeric", "range in declared units"),
        ("B_X_norm", "numeric_or_zero_certificate", "curvature/source vector norm"),
        ("C_X_final_norm", "numeric_or_zero_certificate", "final matter-trace coupling norm"),
        ("J_X_live_norm", "numeric_or_zero_certificate", "live current norm"),
        ("Q_boundary_X_norm", "numeric_or_zero_certificate", "Green boundary charge norm"),
        ("K_arena", "numeric_or_matrix", "arena transfer kernel"),
        ("source_charge", "numeric_or_zero_certificate", "source body charge"),
        ("test_charge", "numeric_or_zero_certificate", "test body charge"),
        ("calibration", "string_with_units", "G_N/GM/source convention"),
        ("bound_reference", "source_path_or_url", "empirical bound source"),
        ("predicted_value", "numeric", "computed residual or alpha"),
        ("units", "string", "units for every numeric input"),
        ("source_paths", "semicolon_paths", "local/web provenance"),
        ("valid_for_claim", "boolean", "true only when all numeric/theorem/source conditions pass"),
        ("blockers", "semicolon_strings", "missing fields if invalid"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "column_id": f"RS4601_{index:02d}",
            "column_name": name,
            "type": col_type,
            "meaning": meaning,
            "required_before_claim": True,
            "schema_status": "REQUIRED_COLUMN",
            "valid_for_claim": False,
            "generated_utc": now,
        }
        for index, (name, col_type, meaning) in enumerate(columns)
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4601_placeholder_block",
            "input_branch": "any score row uses MISSING, placeholder, inferred-from-bound, or unsourced numeric values",
            "expected": "valid_for_claim remains false and claim_allowed remains false",
            "status": "GUARD_ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4601_range_first",
            "input_branch": "B/C/J/Q values are proposed but Z_X,M_X^2,lambda_X are missing",
            "expected": "amplitude and R10 scoring remain blocked",
            "status": "COUNTERMODEL_CAUGHT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4601_GM_absorption",
            "input_branch": "orbital or PPN residual is hidden inside fitted G/GM without a declared nuisance comparison",
            "expected": "score row rejected; calibration must be explicit",
            "status": "GUARD_ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4601_Poynting_firewall",
            "input_branch": "Poynting/EM flux is set to zero by convention rather than same-Hodge closed-collar theorem",
            "expected": "EM_Poynting and J_X_live rows stay open",
            "status": "COUNTERMODEL_CAUGHT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4601_no_cancellation",
            "input_branch": "B,C,J,Q terms cancel numerically without a parent signed relation",
            "expected": "absolute-sum bound used; no cancellation credit",
            "status": "GUARD_ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4601_0_sources_exist",
            "claim": "all cited source paths exist",
            "passed": all(row["path_exists"] for row in sources),
            "detail": "source register path check",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4601_1_needles_found",
            "claim": "all cited source needles found",
            "passed": all(row["needle_found"] for row in sources),
            "detail": "source register needle check",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4601_2_two_sectors",
            "claim": "memory and fibre score vectors both emitted",
            "passed": True,
            "detail": "sector-separated rows for memory and fibre",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4601_3_five_arenas",
            "claim": "R10/PPN/clock/orbital/EM arena rows emitted",
            "passed": True,
            "detail": "arena score matrix has five rows",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4601_4_runner_schema",
            "claim": "nonclaim runner schema emitted",
            "passed": True,
            "detail": "future numeric row has required columns and blockers",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4601_5_no_claim",
            "claim": "no empirical pass emitted",
            "passed": True,
            "detail": "interface only; values and source-backed bounds remain missing",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "score_vector_ready": True,
            "arena_matrix_ready": True,
            "runner_schema_ready": True,
            "numeric_prediction_present": False,
            "empirical_pass_claimed": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "sector-separated body-charge score vector; field operator/range/amplitude law; R10/PPN/clock/orbital/EM arena score matrix; missing-input ledger; nonclaim runner schema",
            "not_derived": "numeric Z_X/M_X^2/lambda_X; numeric or theorem-zero B_X,C_X,J_X,Q_boundary_X; source/test charges; arena kernels; external bound comparisons; local-GR/R10/PPN pass",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "The score interface shows the first hard blocker is not B/C/J bookkeeping but the operator/range owner: without Z_X,M_X^2 and lambda_X no body-charge amplitude or R10/PPN projection is scoreable.",
            "derive_first": "derive parent quadratic operator normalization, mass gap and range for memory/fibre sectors in the same quotient domain",
            "fallback": "emit the first nonclaim source row for Z_X,M_X^2,lambda_X with explicit units and blockers",
            "valid_for_claim": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4601 Y5 R2FR C_X/J_X/B_X body-charge vector to empirical score inputs

Private checkpoint generated at `{now}`.

Marker: `{MARKER}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`
Claim register: `{CLAIM_ID}`

## Result

4601 turns the 4595-4600 body-charge work into an empirical score-input interface. The local branch is now organized as:

```text
(-Z_X nabla^2 + M_X^2) delta_X = rho_X,
rho_X = B_X R_obs + C_X^final_live T + J_X^live,
lambda_X = sqrt(Z_X/M_X^2),
|A_X| <= [exp(R_body/lambda_X) int_body |rho_X| dV + |Q_boundary_X|]/(4*pi |Z_X|).
```

The scoring vector is sector separated:

```text
memory: Z_mem, M2_mem, lambda_mem, B_mem_eff, C_mem^final_live,
        J_mem_live, Q_boundary_mem, W_mem/body profile;

fibre:  Z_h, M2_h, lambda_h, B_h, C_h^final_live,
        J_h_live, Q_boundary_h, W_h/body profile.
```

And arena separated:

```text
R10, PPN/local-GR, clock/WEP, orbital/GM, EM/Poynting.
```

No prediction is made. The useful advance is that a future runner now has a strict schema and a blocker ledger: if a row does not have parent-owned/theorem-zero or source-backed numeric values, it cannot become a claim.

The next best target is `{NEXT_TARGET}`, because `Z_X`, `M_X^2` and `lambda_X` are the first hard gate before any amplitude or alpha score can be honest.

## Source Register

{markdown_table(tables["sources"])}

## Field Operator Inputs

{markdown_table(tables["operators"])}

## Body-Charge Score Vector

{markdown_table(tables["score_vector"])}

## Arena Score Matrix

{markdown_table(tables["arena_matrix"])}

## Missing Input Ledger

{markdown_table(tables["missing"])}

## Nonclaim Runner Schema

{markdown_table(tables["runner_schema"])}

## Controls

{markdown_table(tables["controls"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Decision

{markdown_table(tables["decision"])}

## Status

{markdown_table(tables["status"])}

## Next Target

{markdown_table(tables["next"])}
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 617 - C_X/J_X/B_X Body-Charge Vector To Empirical Score Inputs

Generated: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Claim register: `{CLAIM_ID}`

## Formal Statement

For `X in {{mem,h}}`, the empirical local branch is scored only through the declared body-charge operator:

```text
(-Z_X nabla^2 + M_X^2) delta_X = B_X R_obs + C_X^final_live T + J_X^live,
lambda_X = sqrt(Z_X/M_X^2),
|A_X| <= [exp(R_body/lambda_X) int_body |B_X R_obs + C_X^final_live T + J_X^live| dV + |Q_boundary_X|]/(4*pi |Z_X|).
```

Every arena score is a map from `A_X` plus declared direct tails into an observable:

```text
Delta O_a <= sum_X ||K_aX|| |A_X| + |direct_tail_a|.
```

For R10, a finite-range row may equivalently use the source/test charge product form:

```text
alpha_X(lambda_X) = K_X Qbar_XS qbar_XT / (G_N M_S m_T M_X^2)
```

only after the source/test charges, calibration, units and bound curve are source-backed.

Private nonclaim. The next target is `{NEXT_TARGET}`.
"""


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    add("VAL4601_00_sources_exist", all(row["path_exists"] for row in tables["sources"]), "all cited source paths exist")
    add("VAL4601_01_needles_found", all(row["needle_found"] for row in tables["sources"]), "all cited source needles found")
    csv_paths = [
        SOURCE_REGISTER,
        SCORE_VECTOR_CSV,
        OPERATOR_INPUTS_CSV,
        ARENA_MATRIX_CSV,
        MISSING_INPUTS_CSV,
        RUNNER_SCHEMA_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    csv_ok = True
    details = []
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4601_02_csv_parse", csv_ok, ";".join(details))

    score_text = "\n".join(str(row) for row in tables["score_vector"])
    add("VAL4601_03_memory_and_fibre", "Z_mem" in score_text and "Z_h" in score_text and "Q_boundary_h" in score_text, "memory and fibre score vectors present")
    add("VAL4601_04_required_symbols", all(token in score_text for token in ["B_mem_eff", "C_mem^final_live", "J_mem_live", "B_h", "C_h^final_live", "J_h_live"]), "B/C/J symbols present")

    operator_text = "\n".join(str(row) for row in tables["operators"])
    add("VAL4601_05_operator_law", "lambda_X=sqrt(Z_X/M_X^2)" in operator_text and "Q_boundary_X" in operator_text, "operator/range/amplitude law present")

    arena_text = "\n".join(str(row) for row in tables["arena_matrix"])
    add("VAL4601_06_five_arenas", all(token in arena_text for token in ["R10", "PPN", "clock_WEP", "orbital_GM", "EM_Poynting"]), "five arena rows present")

    missing_text = "\n".join(str(row) for row in tables["missing"])
    add("VAL4601_07_missing_ledger", "Z_X,M_X^2,lambda_X" in missing_text and "K_R10" in missing_text, "missing input ledger names hard blockers")

    schema_text = "\n".join(str(row) for row in tables["runner_schema"])
    add("VAL4601_08_runner_schema", "valid_for_claim" in schema_text and "blockers" in schema_text and "source_paths" in schema_text, "runner schema has claim guard columns")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "empirical_pass_claimed", "numeric_prediction_present"} and value is True:
                    all_false = False
    add("VAL4601_09_no_claim_true", all_false, "no generated table promotes a claim")
    add("VAL4601_10_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4601_11_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4601_12_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4601_13_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4601_14_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4601_15_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4601_16_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4601_17_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4601_OVERALL", all(row["status"] == "PASS" for row in rows), "4601 body-charge score input interface")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "operators": operator_rows(now),
        "score_vector": score_vector_rows(now),
        "arena_matrix": arena_matrix_rows(now),
        "missing": missing_input_rows(now),
        "runner_schema": runner_schema_rows(now),
        "controls": control_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])

    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(OPERATOR_INPUTS_CSV, tables["operators"])
    write_csv(SCORE_VECTOR_CSV, tables["score_vector"])
    write_csv(ARENA_MATRIX_CSV, tables["arena_matrix"])
    write_csv(MISSING_INPUTS_CSV, tables["missing"])
    write_csv(RUNNER_SCHEMA_CSV, tables["runner_schema"])
    write_csv(CONTROL_CSV, tables["controls"])
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
## PPC4161 Local Addendum - Body-Charge Score Input Interface

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The local memory/fibre branch now has a sector-separated empirical score-input interface. `Z_X`, `M_X^2`, `lambda_X`, `B_X`, `C_X^final_live`, `J_X^live`, `Q_boundary_X`, body profiles, arena kernels and calibration inputs are all named before any R10/PPN/clock/orbital/EM comparison is allowed. The first hard blocker is the parent range/operator row.
""",
    )

    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Body-Charge Score Vector

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private packet now has the nonclaim score vector for memory/fibre local tests. Future numeric rows must use the 4601 runner schema and keep `valid_for_claim=false` unless every coefficient, unit, source path and empirical bound is real.
""",
    )

    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4601 validation failed: {failed}")
    print(f"4601 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
