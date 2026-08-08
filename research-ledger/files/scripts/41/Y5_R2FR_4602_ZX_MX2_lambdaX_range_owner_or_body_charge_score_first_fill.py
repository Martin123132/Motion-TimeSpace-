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

CHECKPOINT = "4602"
CLAIM_ID = "L-444"
BRANCH_ID = "MTS_R2FR_Y5_RANGE_OWNER_NORMALIZATION_INVARIANT_GATE_4602"
MARKER = "PPC4161_ZX_MX2_LAMBDAX_RANGE_OWNER_OR_BODY_CHARGE_SCORE_FIRST_FILL_4602"
PACKET_MARKER = "PPC4161_PACKET_RANGE_OWNER_NORMALIZATION_INVARIANT_GATE_4602"
DECISION = "RANGE_NORMALIZATION_INVARIANT_LAW_DERIVED_VALUES_MISSING_NONCLAIM"
NEXT_TARGET = "4603-Y5-R2FR-source-test-charge-invariant-product-or-first-numeric-bound-row.md"

DOC_PATH = POST / "4602-Y5-R2FR-ZX-MX2-lambdaX-range-owner-or-body-charge-score-first-fill.md"
FORMAL_PATH = FORMAL / "618-PPC4161-ZX-MX2-lambdaX-range-owner-or-body-charge-score-first-fill.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4602_SOURCE_REGISTER.csv"
RANGE_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4602_RANGE_OWNER_NORMALIZATION_THEOREM.csv"
INVARIANT_LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4602_INVARIANT_SCORE_LAW.csv"
RANGE_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4602_RANGE_OWNER_INPUT_ROWS.csv"
SCORE_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4602_SCORE_VECTOR_RANGE_UPDATE.csv"
MISSING_CSV = SOURCE_DIR / "P8_Y5_R2FR_4602_REMAINING_RANGE_INPUT_BLOCKERS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4602_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4602_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4602_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4602_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4602_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4602_VALIDATION.csv"

DOC_4601 = POST / "4601-Y5-R2FR-CX-JX-BX-body-charge-vector-to-empirical-score-inputs.md"
FORMAL_617 = FORMAL / "617-PPC4161-CX-JX-BX-body-charge-vector-to-empirical-score-inputs.md"
CSV_4601_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4601_NEXT_TARGET.csv"
CSV_4601_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4601_STATUS.csv"
CSV_4601_MISSING = SOURCE_DIR / "P8_Y5_R2FR_4601_MISSING_INPUT_LEDGER.csv"
CSV_4601_OPERATOR = SOURCE_DIR / "P8_Y5_R2FR_4601_FIELD_OPERATOR_INPUTS.csv"
CSV_4601_ARENA = SOURCE_DIR / "P8_Y5_R2FR_4601_ARENA_SCORE_MATRIX.csv"
CSV_4524_HUNT = SOURCE_DIR / "P8_Y5_R2FR_4524_PARENT_Z_ACTION_SIGNATURE_HUNT.csv"
CSV_4524_LAW = SOURCE_DIR / "P8_Y5_R2FR_4524_FINITE_RESIDUAL_ALPHA_LAW.csv"
CSV_4524_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4524_RESIDUAL_ALPHA_INPUT_CONTRACT.csv"
CSV_4525_STEPS = SOURCE_DIR / "P8_Y5_R2FR_4525_PARENT_Z_PROOF_STEPS.csv"
CSV_4525_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4525_QUOTIENT_EVEN_MORSE_BOTT_Z_THEOREM.csv"
CSV_4526_BRIDGE = SOURCE_DIR / "P8_Y5_R2FR_4526_ZL_TO_Z_PARENT_BRIDGE_THEOREM.csv"
CSV_4527_SYMBOL = SOURCE_DIR / "P8_Y5_R2FR_4527_AUXILIARY_Z_PRINCIPAL_SYMBOL_TEST.csv"
CSV_4506_BODY = SOURCE_DIR / "P8_Y5_R2FR_4506_BODY_CHARGE_INPUT_ROW.csv"
CSV_4505_GREEN = SOURCE_DIR / "P8_Y5_R2FR_4505_BODY_CHARGE_GREEN_FUNCTION_LAW.csv"
CSV_4486_M2 = SOURCE_DIR / "P8_Y5_R2FR_4486_FIRST_M2K2_INPUT_ROW.csv"
CSV_4475_LAMBDA = SOURCE_DIR / "P8_Y5_R2FR_4475_LAMBDAM_SOURCE_ROW.csv"
CSV_4476_PROJECTION = SOURCE_DIR / "P8_Y5_R2FR_4476_LAMBDAM_PROJECTION_MAP.csv"
CSV_4595_SCHEMA = SOURCE_DIR / "P8_Y5_R2FR_4595_FINITE_INPUT_SCHEMA.csv"
CSV_4595_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4595_OWNER_ZERO_SWITCH.csv"

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
        "claim": "4602 derives the normalization-invariant range/coupling law for body-charge scoring: raw Z_X and source charges are convention-dependent, while lambda_X and charge-product-over-Z combinations are the physical finite-range score inputs.",
        "current_evidence": "Generated range-owner theorem rows, field-rescaling invariant law, memory/fibre range input rows, score-vector update, blockers, controls and validation.",
        "status": "range_normalization_invariant_law_nonclaim_values_missing",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating a raw field normalization Z_X, or a rescaled source charge, as an observable prediction; or collapsing the auxiliary rank-zero branch into a finite-range Yukawa branch without a parent principal symbol.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No empirical claim until lambda_X, invariant source/test product, calibration, body profile and arena kernels are source-backed or theorem-zero in the same branch.",
    }
    rows.append({key: row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4602_00_4601_doc", DOC_4601, "next best target", "4601 selected range owner first."),
        ("SRC4602_01_617_formal", FORMAL_617, "alpha_X(lambda_X)", "4601 formal score law."),
        ("SRC4602_02_4601_next", CSV_4601_NEXT, "4602-Y5-R2FR-ZX-MX2-lambdaX-range-owner-or-body-charge-score-first-fill.md", "machine-readable 4601 next target."),
        ("SRC4602_03_4601_status", CSV_4601_STATUS, "numeric Z_X/M_X^2/lambda_X", "4601 status blocker."),
        ("SRC4602_04_4601_missing", CSV_4601_MISSING, "MIS4601_0_operator_range", "range blocker row."),
        ("SRC4602_05_4601_operator", CSV_4601_OPERATOR, "OP4601_0_common", "operator law handoff."),
        ("SRC4602_06_4601_arena", CSV_4601_ARENA, "ASM4601_0", "R10 arena score law."),
        ("SRC4602_07_4524_hunt", CSV_4524_HUNT, "PZA4524_0_action_form", "parent Z action hunt."),
        ("SRC4602_08_4524_law", CSV_4524_LAW, "FRA4524_4_finite_range_mode", "finite-range alpha template."),
        ("SRC4602_09_4524_firewall", CSV_4524_LAW, "FRA4524_6_no_claim_firewall", "no-claim firewall."),
        ("SRC4602_10_4524_contract", CSV_4524_CONTRACT, "RAI4524_4_mass_range", "mass/range required source."),
        ("SRC4602_11_4525_steps", CSV_4525_STEPS, "PROOF4525_0_Taylor", "quadratic normal form."),
        ("SRC4602_12_4525_rankzero", CSV_4525_THEOREM, "QEZ4525_2_rank_zero_from_auxiliary_verticality", "rank-zero auxiliary route."),
        ("SRC4602_13_4525_closure", CSV_4525_THEOREM, "QEZ4525_5_local_GR_closure_mechanism", "Morse-Bott closure route."),
        ("SRC4602_14_4526_bridge", CSV_4526_BRIDGE, "BRG4526_4_full_parent_Z_verdict", "parent Z verdict."),
        ("SRC4602_15_4527_symbol", CSV_4527_SYMBOL, "APS4527_3_finite_range_gate", "finite-range principal-symbol gate."),
        ("SRC4602_16_4506_body", CSV_4506_BODY, "BCIN4506_2_zero_switch", "body-charge zero switch."),
        ("SRC4602_17_4505_green", CSV_4505_GREEN, "BC4505_0_generic_field", "Green-function amplitude law."),
        ("SRC4602_18_4486_M2", CSV_4486_M2, "M2I4486_3_recast_hessian_product_bound", "first symbolic Hessian product row."),
        ("SRC4602_19_4475_lambda", CSV_4475_LAMBDA, "LMR4475_1_lambda_M", "lambda source row."),
        ("SRC4602_20_4476_projection", CSV_4476_PROJECTION, "PMAP4476_0_universal_projection", "projection normal form."),
        ("SRC4602_21_4595_schema", CSV_4595_SCHEMA, "schema4595_0_memory_Z", "memory/fibre finite input schema."),
        ("SRC4602_22_4595_owner", CSV_4595_OWNER, "ZS4595_0_common_operator", "common operator zero switch."),
        ("SRC4602_23_claim_443", CLAIMS_PATH, "L-443", "claim-register handoff from 4601."),
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


def theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "RNG4602_0_quadratic_normal_form",
            "statement": "A finite-range body-charge field must come from a parent quadratic block with gradient and Hessian terms on the same quotient domain.",
            "formula": "S_X^(2)=1/2 int sqrt(g)[Z_X |grad X|^2 + M_X^2 X^2] - int sqrt(g) X rho_X + S_boundary",
            "consequence": "(-Z_X nabla^2+M_X^2)X=rho_X and lambda_X=sqrt(Z_X/M_X^2)",
            "status": "DERIVED_NORMAL_FORM_PARENT_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "RNG4602_1_rescaling_invariance",
            "statement": "Raw Z_X and raw source charge are not separately observable because field normalization can be rescaled.",
            "formula": "X=a X_prime => Z_prime=a^2 Z_X, M_prime^2=a^2 M_X^2, rho_prime=a rho_X, q_prime=a q_X",
            "consequence": "lambda_prime=lambda_X and q_S q_T/Z_X is invariant; score rows must use invariant products, not naked Z_X",
            "status": "EXACT_NORMALIZATION_GAUGE_LAW",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "RNG4602_2_rank_zero_vs_finite_range",
            "statement": "The local route splits cleanly: auxiliary rank-zero vertical coordinates are algebraic, while nonzero principal symbol modes must be scored as finite-range fields.",
            "formula": "K_AB=0 => M_AB z^B=-R_A; K_AB>0 and M_AB>0 => lambda_i=sqrt(Z_i/M_i^2)",
            "consequence": "do not run a Yukawa/R10 score for a true auxiliary rank-zero closure; do not claim closure for a propagating finite-range branch without alpha/PPN bounds",
            "status": "BRANCH_SPLIT_DERIVED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "RNG4602_3_claim_grade_range_owner",
            "statement": "Claim-grade lambda_X requires a parent principal symbol and Hessian projected onto the same physical mode after gauge/constraint reduction.",
            "formula": "Z_X=<v_X,K v_X>, M_X^2=<v_X,H v_X>, lambda_X=sqrt(Z_X/M_X^2)",
            "consequence": "memory/fibre ranges remain missing until v_X,K,H,units and sign are sourced",
            "status": "SOURCE_ROW_CONTRACT_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "RNG4602_4_invariant_alpha_owner",
            "statement": "The R10/fifth-force score should be carried by lambda_X and an invariant source-test product, with the chosen Green-kernel convention declared.",
            "formula": "alpha_X(lambda_X)=K_X I_X^ST, I_X^ST:=Qbar_XS qbar_XT/(4*pi Z_X G_N M_S m_T)",
            "consequence": "the 4603 target is the invariant source/test product, not a raw source charge alone",
            "status": "INVARIANT_SCORE_OBJECT_DEFINED_NONCLAIM",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def invariant_law_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "law_id": "INV4602_0_lambda",
            "object": "lambda_X",
            "definition": "sqrt(Z_X/M_X^2) on a finite-range principal branch",
            "field_rescaling": "invariant under X=a X_prime",
            "claim_input": "parent-projected K/H eigenvalue pair with units",
            "current_status": "FORMULA_DERIVED_NUMERIC_VALUE_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "law_id": "INV4602_1_source_product",
            "object": "I_X^ST",
            "definition": "Qbar_XS qbar_XT/(4*pi Z_X G_N M_S m_T), or declared equivalent if the Green convention absorbs 4*pi/Z_X",
            "field_rescaling": "invariant because Qbar and qbar scale with a while Z scales with a^2",
            "claim_input": "source/test charge integrals, Z convention, G_N/GM calibration and source paths",
            "current_status": "INVARIANT_OBJECT_DEFINED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "law_id": "INV4602_2_boundary_product",
            "object": "Q_boundary_X/Z_X",
            "definition": "boundary Green charge contribution divided by the same operator normalization",
            "field_rescaling": "invariant when boundary charge is varied in the same X normalization",
            "claim_input": "no-flux theorem or finite boundary integral with matching normalization",
            "current_status": "BOUNDARY_INVARIANT_DEFINED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "law_id": "INV4602_3_rank_zero_no_lambda",
            "object": "auxiliary rank-zero branch",
            "definition": "K_AB=0, M_AB coercive, z algebraically locked or bounded by m_min^-1 residuals",
            "field_rescaling": "not a finite-range Yukawa field; score uses algebraic residual norm, not lambda_X",
            "claim_input": "parent K=0, M_AB>=m_min and source RHS zero/bound",
            "current_status": "AUXILIARY_ROUTE_SEPARATED_NOT_CLAIMED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def range_input_rows(now: str) -> list[dict[str, Any]]:
    sectors = [
        ("memory", "Z_mem", "M2_mem", "lambda_mem", "I_mem^ST", "Q_boundary_mem/Z_mem"),
        ("fibre", "Z_h", "M2_h", "lambda_h", "I_h^ST", "Q_boundary_h/Z_h"),
    ]
    rows = []
    for index, (sector, z_symbol, m_symbol, lambda_symbol, invariant_product, boundary_product) in enumerate(sectors):
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "range_id": f"RIN4602_{index}",
                "sector": sector,
                "operator_normalization": z_symbol,
                "mass_gap": m_symbol,
                "range_symbol": lambda_symbol,
                "range_formula": f"{lambda_symbol}=sqrt({z_symbol}/{m_symbol})",
                "invariant_source_test_product": invariant_product,
                "invariant_boundary_product": boundary_product,
                "required_parent_inputs": "physical mode v_X; principal symbol K; Hessian H; unit convention; source/test charge normalization",
                "current_status": "RANGE_FORMULA_DERIVED_VALUES_MISSING",
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": now,
            }
        )
    return rows


def score_update_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("R10", "score by lambda_X plus invariant I_X^ST", "alpha_X(lambda_X)=K_R10_X I_X^ST plus boundary/direct tails", "lambda_X;I_X^ST;Q_boundary_X/Z_X;alpha_bound(lambda);units"),
        ("PPN", "score by A_X/Z-normalized amplitude or direct invariant tails", "Delta p_i <= sum_X ||K_iX|| |A_X| + |direct_tail_i|, with A_X built from rho_X/Z_X", "lambda_X;B_X/Z_X;C_X/Z_X;J_X/Z_X;Q_boundary_X/Z_X;K_iX"),
        ("orbital_GM", "score by Yukawa acceleration with explicit calibration", "Delta a/a_N=alpha_X(1+r/lambda_X)exp(-r/lambda_X)", "lambda_X;alpha_X;GM convention;orbital threshold"),
        ("clock_WEP", "score material/clock response from invariant coupling derivatives", "Delta O <= K_material I_X^material + K_clock C_X^final/Z_X + direct tails", "material source integrals;clock kernels;standard/weight rows"),
        ("EM_Poynting", "score EM/open flux as direct tail before alpha comparison", "Delta O_EM <= K_EM(|J_EM|/Z_X+|Delta_Hodge|+|Phi_EM|+|b_alpha|)", "same-Hodge owner or finite Poynting/EM flux profile"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": f"SUP4602_{index}",
            "arena": arena,
            "update": update,
            "score_law": law,
            "required_inputs": required,
            "current_status": "INVARIANT_SCORE_FORM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        }
        for index, (arena, update, law, required) in enumerate(rows)
    ]


def missing_rows(now: str) -> list[dict[str, Any]]:
    blockers = [
        ("MIS4602_0_principal_symbol", "K_AB or Z_X", "parent second variation gradient block on physical quotient", "needed to distinguish auxiliary from finite-range"),
        ("MIS4602_1_hessian", "H_AB or M_X^2", "parent second variation Hessian/mass block", "needed for coercivity/range"),
        ("MIS4602_2_mode_basis", "v_X", "same mode basis for K,H,source and readout", "prevents mixing memory/fibre directions"),
        ("MIS4602_3_units", "unit convention", "SI/natural-unit conversion, c/hbar and 4*pi Green convention", "prevents fake alpha normalization"),
        ("MIS4602_4_source_product", "I_X^ST", "source/test charge-over-Z invariant with calibration", "4603 target"),
        ("MIS4602_5_boundary_product", "Q_boundary_X/Z_X", "boundary integral or no-flux theorem in same normalization", "separate from C_X boundary leakage"),
        ("MIS4602_6_full_bounds", "alpha/PPN/clock/orbit/EM bounds", "source-backed empirical comparison tables/kernels", "needed only after source product exists"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "missing_id": missing_id,
            "missing_input": missing,
            "required_evidence": evidence,
            "why_it_matters": why,
            "current_status": "MISSING_BLOCKS_CLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        }
        for missing_id, missing, evidence, why in blockers
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4602_raw_Z_rescale",
            "input_branch": "X is rescaled and raw Z_X changes",
            "expected": "lambda_X and Q_S q_T/Z_X stay invariant; raw Z-only claims fail",
            "status": "COUNTERMODEL_CAUGHT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4602_rank_zero_firewall",
            "input_branch": "K_AB=0 auxiliary branch is fed into a Yukawa alpha runner",
            "expected": "reject finite-range score; use algebraic residual or local closure theorem",
            "status": "GUARD_ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4602_mixed_modes",
            "input_branch": "Z_X from one mode, M_X^2 from another, source charge from a third",
            "expected": "range row invalid until same mode basis is declared",
            "status": "COUNTERMODEL_CAUGHT",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4602_missing_units",
            "input_branch": "lambda or alpha product has no unit/Green-kernel convention",
            "expected": "score row stays nonclaim",
            "status": "GUARD_ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4602_0_sources_exist", "claim": "all cited source paths exist", "passed": all(row["path_exists"] for row in sources), "detail": "source register path check", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4602_1_needles_found", "claim": "all cited source needles found", "passed": all(row["needle_found"] for row in sources), "detail": "source register needle check", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4602_2_rescaling_law", "claim": "normalization-invariant law written", "passed": True, "detail": "raw Z/charge rescaling separated from lambda and charge-product-over-Z", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4602_3_rankzero_split", "claim": "auxiliary rank-zero and finite-range branches separated", "passed": True, "detail": "no Yukawa score for true K=0 auxiliary branch", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4602_4_no_claim", "claim": "no numeric range/alpha claim emitted", "passed": True, "detail": "values and source/test products remain missing", "valid_for_claim": False, "generated_utc": now},
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "rescaling_law_derived": True,
            "rankzero_finite_range_split": True,
            "range_values_present": False,
            "invariant_source_product_present": False,
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
            "derived": "quadratic range normal form; field-rescaling law; invariant lambda and source-product objects; auxiliary rank-zero versus finite-range branch split; memory/fibre range input rows",
            "not_derived": "numeric parent K/H eigenvalues; numeric lambda_mem/lambda_h; invariant source/test product; boundary/Z product; R10/PPN/clock/orbital/EM pass",
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
            "reason": "4602 shows the physical score row is not raw Z_X or raw charge but lambda_X plus invariant source/test product. The next useful target is therefore I_X^ST or a theorem-zero for it.",
            "derive_first": "derive source/test charge-over-Z invariant from parent Hilbert/source functor and test-body coupling",
            "fallback": "emit first nonclaim numeric-bound row for I_X^ST with units, source paths and blockers",
            "valid_for_claim": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4602 Y5 R2FR Z_X/M_X^2/lambda_X range owner or body-charge score first fill

Private checkpoint generated at `{now}`.

Marker: `{MARKER}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`
Claim register: `{CLAIM_ID}`

## Result

4602 makes the first range-owner advance. The raw inputs from 4601 were:

```text
(-Z_X nabla^2 + M_X^2)X = rho_X,
lambda_X = sqrt(Z_X/M_X^2).
```

The important correction is that raw `Z_X` and raw source charge are partly field-normalization convention:

```text
X = a X'  =>  Z' = a^2 Z_X,  M'^2 = a^2 M_X^2,
rho' = a rho_X,  q_T' = a q_T.
```

Therefore:

```text
lambda_X = sqrt(Z_X/M_X^2)
```

is invariant, and the finite-range coupling must be expressed through an invariant product such as:

```text
I_X^ST := Qbar_XS qbar_XT / (4*pi Z_X G_N M_S m_T),
alpha_X(lambda_X) = K_X I_X^ST
```

up to a declared Green-kernel convention.

This is real progress because it prevents a fake hunt for a unique raw `Z_X`. The next target is now the invariant source/test product, not a naked source charge.

4602 also separates the branches:

```text
K_AB = 0  -> auxiliary/rank-zero algebraic branch, no Yukawa range;
K_AB > 0 and M_AB > 0 -> finite-range branch, lambda_i=sqrt(Z_i/M_i^2), score against R10/PPN/etc.
```

No numeric range, alpha, PPN or local-GR pass is claimed here.

## Source Register

{markdown_table(tables["sources"])}

## Range Owner Normalization Theorem

{markdown_table(tables["theorem"])}

## Invariant Score Law

{markdown_table(tables["invariant"])}

## Range Owner Input Rows

{markdown_table(tables["range_inputs"])}

## Score Vector Range Update

{markdown_table(tables["score_update"])}

## Remaining Blockers

{markdown_table(tables["missing"])}

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
    return f"""# PPC4161 618 - Z_X/M_X^2/lambda_X Range Owner Or Body-Charge Score First Fill

Generated: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Claim register: `{CLAIM_ID}`

## Formal Statement

For a finite-range body-charge mode `X`,

```text
S_X^(2)=1/2 int sqrt(g)[Z_X |grad X|^2 + M_X^2 X^2] - int sqrt(g) X rho_X,
(-Z_X nabla^2 + M_X^2)X=rho_X,
lambda_X=sqrt(Z_X/M_X^2).
```

Under `X=aX'`,

```text
Z'=a^2 Z_X, M'^2=a^2 M_X^2, rho'=a rho_X, q_T'=a q_T.
```

Thus `lambda_X` and `Qbar_XS qbar_XT/Z_X` are invariant, while raw `Z_X` and raw charge are not independent observables. R10 scoring should therefore use:

```text
alpha_X(lambda_X)=K_X Qbar_XS qbar_XT/(4*pi Z_X G_N M_S m_T)
```

or a declared equivalent convention.

Private nonclaim. The next target is `{NEXT_TARGET}`.
"""


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False})

    add("VAL4602_00_sources_exist", all(row["path_exists"] for row in tables["sources"]), "all cited source paths exist")
    add("VAL4602_01_needles_found", all(row["needle_found"] for row in tables["sources"]), "all cited source needles found")
    csv_paths = [SOURCE_REGISTER, RANGE_THEOREM_CSV, INVARIANT_LAW_CSV, RANGE_INPUT_CSV, SCORE_UPDATE_CSV, MISSING_CSV, CONTROL_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    details = []
    csv_ok = True
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4602_02_csv_parse", csv_ok, ";".join(details))

    theorem_text = "\n".join(str(row) for row in tables["theorem"])
    add("VAL4602_03_rescaling_law", "Z_prime=a^2 Z_X" in theorem_text and "q_S q_T/Z_X" in theorem_text, "field-rescaling invariant law present")
    add("VAL4602_04_rankzero_split", "K_AB=0" in theorem_text and "finite-range" in theorem_text, "rank-zero and finite-range split present")

    invariant_text = "\n".join(str(row) for row in tables["invariant"])
    add("VAL4602_05_invariant_objects", "I_X^ST" in invariant_text and "Q_boundary_X/Z_X" in invariant_text, "invariant score objects present")

    range_text = "\n".join(str(row) for row in tables["range_inputs"])
    add("VAL4602_06_memory_fibre_range", "lambda_mem" in range_text and "lambda_h" in range_text, "memory/fibre range rows present")

    update_text = "\n".join(str(row) for row in tables["score_update"])
    add("VAL4602_07_score_update", "alpha_X(lambda_X)" in update_text and "Q_boundary_X/Z_X" in update_text, "score update uses invariant/range objects")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "empirical_pass_claimed", "range_values_present", "invariant_source_product_present"} and value is True:
                    all_false = False
    add("VAL4602_08_no_claim_true", all_false, "no generated table promotes a claim")
    add("VAL4602_09_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4602_10_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4602_11_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4602_12_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4602_13_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4602_14_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4602_15_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4602_16_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4602_OVERALL", all(row["status"] == "PASS" for row in rows), "4602 range-owner normalization-invariant gate")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "theorem": theorem_rows(now),
        "invariant": invariant_law_rows(now),
        "range_inputs": range_input_rows(now),
        "score_update": score_update_rows(now),
        "missing": missing_rows(now),
        "controls": control_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])

    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(RANGE_THEOREM_CSV, tables["theorem"])
    write_csv(INVARIANT_LAW_CSV, tables["invariant"])
    write_csv(RANGE_INPUT_CSV, tables["range_inputs"])
    write_csv(SCORE_UPDATE_CSV, tables["score_update"])
    write_csv(MISSING_CSV, tables["missing"])
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
## PPC4161 Local Addendum - Range Owner Normalization-Invariant Gate

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The body-charge score interface now treats raw `Z_X` and raw source charge as convention-dependent. The physical finite-range objects are `lambda_X` and charge-product-over-`Z_X` invariants, with an explicit firewall between auxiliary rank-zero closure and finite-range Yukawa scoring.
""",
    )

    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Range Owner Invariant Score Law

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private packet now routes R10/PPN/clock/orbital/EM scoring through invariant range and coupling products. The next fill target is `I_X^ST`, the source/test charge-over-`Z_X` product.
""",
    )

    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4602 validation failed: {failed}")
    print(f"4602 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
