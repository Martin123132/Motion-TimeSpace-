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

CHECKPOINT = "4614"
CLAIM_ID = "L-456"
BRANCH_ID = "MTS_R2FR_Y5_EM_GAUGE_KINETIC_DESCENT_4614"
MARKER = "PPC4161_EM_GAUGE_KINETIC_DESCENT_OR_B_ALPHA_SOURCE_ROW_4614"
PACKET_MARKER = "PPC4161_PACKET_EM_GAUGE_KINETIC_DESCENT_4614"
DECISION = "EM_GAUGE_KINETIC_DESCENT_ZERO_CONTRACT_AND_B_ALPHA_SOURCE_ROW_READY_NONCLAIM"
NEXT_TARGET = "4615-Y5-R2FR-no-extra-F2-operator-domain-or-lambdaA-source-row.md"

DOC_PATH = POST / "4614-Y5-R2FR-EM-gauge-kinetic-descent-or-b-alpha-source-row.md"
FORMAL_PATH = FORMAL / "630-PPC4161-EM-gauge-kinetic-descent-or-b-alpha-source-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4614_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4614_EM_GAUGE_KINETIC_THEOREM.csv"
OWNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4614_GAUGE_OWNER_CLAUSES.csv"
B_ALPHA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4614_B_ALPHA_NORMAL_FORM_ROWS.csv"
MAXWELL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4614_MAXWELL_STRESS_LIMIT_ROWS.csv"
ARENA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4614_ALPHA_ARENA_PROJECTION_ROWS.csv"
COEFFICIENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4614_B_ALPHA_SOURCE_ROW_NONCLAIM.csv"
QBARXT_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4614_QBARXT_EM_UPDATE_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4614_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4614_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4614_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4614_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4614_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4614_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4614_VALIDATION.csv"

CSV_4613_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4613_NEXT_TARGET.csv"
CSV_4613_EM = SOURCE_DIR / "P8_Y5_R2FR_4613_EM_ALPHA_DESCENT_ROWS.csv"
CSV_4613_COEFF = SOURCE_DIR / "P8_Y5_R2FR_4613_QBARXT_COEFFICIENT_ROWS_NONCLAIM.csv"
CSV_3526_STATUS = SOURCE_DIR / "P8_EM_scalar_gauge_coupling_owner_status.csv"
CSV_3507_ALPHA = SOURCE_DIR / "P8_EM_scalar_coupling_owner_alpha_residual.csv"
CSV_3528_UNIQUE = SOURCE_DIR / "P8_EM_unique_F2_or_calibrated_alpha_status.csv"
CSV_3505_VISIBLE = SOURCE_DIR / "P8_EM_visible_action_domain_exhaustion_no_chiEM_bound_vector.csv"
CSV_3503_BOUND = SOURCE_DIR / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv"
CSV_3502_POYNTING = SOURCE_DIR / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv"
CSV_3524_OWNER = SOURCE_DIR / "P8_EM_observed_stack_charge_lattice_owner_status.csv"
CSV_3525_BRANCH = SOURCE_DIR / "P8_EM_visible_EM_first_owner_branch_status.csv"
CSV_1047_AUDIT = SOURCE_DIR / "P8_Y5_R10_1047_ALPHA_GAUGE_NORMALIZATION_AUDIT.csv"
CSV_1100_SIGNATURE = SOURCE_DIR / "P8_Y5_R10_1100_TQ_GAUGE_NORM_SIGNATURE.csv"
CSV_1101_THEOREM = SOURCE_DIR / "P8_Y5_R10_1101_GAUGE_NORM_THEOREM_ATTEMPT.csv"
CSV_1101_CANDIDATES = SOURCE_DIR / "P8_Y5_R10_1101_GAUGE_NORM_OWNER_CANDIDATE_AUDIT.csv"
CSV_1397_LAMBDA = SOURCE_DIR / "P8_Y5_R10_1397_LAMBDA_A_ALPHAEM_ARENA_GATE.csv"
CSV_1398_ARENA = SOURCE_DIR / "P8_Y5_R10_1398_ALPHAEM_LOCAL_ARENA_GATE.csv"
CSV_1399_PRIOR = SOURCE_DIR / "P8_Y5_R10_1399_FINITE_ALPHAEM_PRIOR_VECTOR.csv"

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
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines)


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


def append_claim_once() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = [
        "claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk",
        "sector", "evidence", "next_action", "risk",
    ]
    rows.append({
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4614 derives the EM gauge-kinetic normal form for b_alpha_EM, identifies the exact zero contract, and stages finite b_alpha source rows for clocks, WEP, R10, Maxwell stress and local residual gates.",
        "current_evidence": "Generated EM gauge kinetic theorem rows, owner clauses, b_alpha normal form rows, Maxwell stress limit rows, arena projections, source-row templates and validation.",
        "status": "EM_gauge_kinetic_descent_zero_contract_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Claiming Maxwell/local-GR or alpha silence from charge quantization, Ward identities, calibration, or units while the Maxwell kinetic coefficient, current normalization and no-extra-F2 operator domain remain unsigned.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No alpha_EM, Maxwell, WEP, clock, R10, Newton or local-GR pass until b_alpha_EM is parent-zero or finite/source-backed in the product rows.",
    })
    existing = list(rows[0].keys()) if rows else fieldnames
    for name in fieldnames:
        if name not in existing:
            existing.append(name)
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=existing)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in existing})


def source_rows(now: str) -> list[dict[str, Any]]:
    sources = [
        ("SRC4614_00_4613_handoff", CSV_4613_NEXT, "4614-Y5-R2FR-EM-gauge-kinetic-descent-or-b-alpha-source-row.md", "4613 selected EM gauge kinetic descent."),
        ("SRC4614_01_4613_EM", CSV_4613_EM, "EM4613_0_gauge_kinetic", "4613 b_alpha EM row."),
        ("SRC4614_02_4613_Maxwell", CSV_4613_EM, "EM4613_2_Maxwell_limit", "4613 Maxwell limit row."),
        ("SRC4614_03_4613_coeff", CSV_4613_COEFF, "QTC4613_1_b_alpha", "4613 b_alpha coefficient row."),
        ("SRC4614_04_3526_identity", CSV_3526_STATUS, "STAT3526_0_identity", "C_XF2/b_alpha identity."),
        ("SRC4614_05_3526_zero", CSV_3526_STATUS, "STAT3526_1_zero_theorem", "conditional zero theorem."),
        ("SRC4614_06_3526_blocker", CSV_3526_STATUS, "STAT3526_2_live_blocker", "current corpus blocker."),
        ("SRC4614_07_3507_balpha", CSV_3507_ALPHA, "ARE3507_0_b_alpha_X", "b_alpha normal form."),
        ("SRC4614_08_3507_CXF2", CSV_3507_ALPHA, "ARE3507_1_C_XF2", "F2 scalar multiplier."),
        ("SRC4614_09_3507_zg", CSV_3507_ALPHA, "ARE3507_2_z_g", "current normalization derivative."),
        ("SRC4614_10_3507_zlambda", CSV_3507_ALPHA, "ARE3507_3_z_lambda", "kinetic normalization derivative."),
        ("SRC4614_11_3528_unique", CSV_3528_UNIQUE, "STAT3528_0_unique_F2", "unique F2 status."),
        ("SRC4614_12_3528_CXF2", CSV_3528_UNIQUE, "STAT3528_2_CXF2", "C_XF2 status."),
        ("SRC4614_13_3505_CXF2", CSV_3505_VISIBLE, "VEB3505_6_C_XF2", "visible action C_XF2 retained row."),
        ("SRC4614_14_3503_CXF2", CSV_3503_BOUND, "EMB3503_2_C_XF2", "EM bound vector C_XF2."),
        ("SRC4614_15_3503_CJQ", CSV_3503_BOUND, "EMB3503_3_C_JQ", "charge/current normalization bound row."),
        ("SRC4614_16_3503_readout", CSV_3503_BOUND, "EMB3503_5_C_EM_readout", "readout/radiative regeneration."),
        ("SRC4614_17_3502_exchange", CSV_3502_POYNTING, "EMF3502_5_matter_EM_internal_exchange", "matter-EM total stress exchange."),
        ("SRC4614_18_3524_owner", CSV_3524_OWNER, "STAT3524_0_composite_theorem", "shared owner theorem."),
        ("SRC4614_19_3525_branch", CSV_3525_BRANCH, "STAT3525_2_scalar_throat", "visible EM scalar throat."),
        ("SRC4614_20_1047_verdict", CSV_1047_AUDIT, "AGN1047_4_verdict", "alpha theorem zero verdict."),
        ("SRC4614_21_1100_norm", CSV_1100_SIGNATURE, "TQS1100_2_fixed_generator_norm", "fixed generator norm clause."),
        ("SRC4614_22_1100_F2", CSV_1100_SIGNATURE, "TQS1100_3_unique_curvature_norm", "unique F2 clause."),
        ("SRC4614_23_1100_current", CSV_1100_SIGNATURE, "TQS1100_4_same_current_owner", "same current owner clause."),
        ("SRC4614_24_1100_verdict", CSV_1100_SIGNATURE, "TQS1100_6_verdict", "TQ gauge norm verdict."),
        ("SRC4614_25_1101_verdict", CSV_1101_THEOREM, "GFT1101_4_verdict", "gauge norm theorem verdict."),
        ("SRC4614_26_1101_metric", CSV_1101_CANDIDATES, "GNO1101_0_fixed_fibre_metric", "fixed fibre metric candidate."),
        ("SRC4614_27_1397_verdict", CSV_1397_LAMBDA, "LAG1397_6_verdict", "alphaEM arena verdict."),
        ("SRC4614_28_1398_verdict", CSV_1398_ARENA, "NAG1398_6_verdict", "local arena verdict."),
        ("SRC4614_29_1399_prior", CSV_1399_PRIOR, "FAP1399_0_alphaEM_residual", "finite b_alpha prior vector."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in sources:
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": line_of(path, needle) > 0,
            "line": line_of(path, needle),
            "role": role,
            "valid_for_claim": False,
            "generated_utc": now,
        })
    return rows


def theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "EGK4614_0_normal_form",
            "claim": "The physical EM coupling throat is the vertical derivative of fine-structure normalization, not a unit convention.",
            "formula": "b_alpha_EM := Lie_v ln(alpha_EM) = 2 z_g - z_lambda - z_readout - z_rad",
            "derivation": "Use alpha_EM proportional to current/charge normalization squared divided by Maxwell kinetic normalization, then vary along v_X.",
            "status": "EXACT_NORMAL_FORM_NONNUMERIC",
            "source_anchor": "ARE3507_0_b_alpha_X;STAT3526_0_identity",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "EGK4614_1_zero_contract",
            "claim": "b_alpha_EM=0 only when gauge object, charge lattice, generator norm, unique F2, same current owner and readout/radiative closure are all parent-signed.",
            "formula": "z_g=z_lambda=z_readout=z_rad=0 and no lambda_A/f_X F_Q^2 counterterm",
            "derivation": "The 1100 and 1047 clauses are conjunctive; charge quantization, Ward identity or calibration alone does not fix the kinetic coefficient.",
            "status": "EXACT_CONDITIONAL_ZERO_CONTRACT_PARENT_UNSIGNED",
            "source_anchor": "TQS1100_6_verdict;AGN1047_4_verdict;GFT1101_4_verdict",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "EGK4614_2_bound_branch",
            "claim": "If the zero contract is not signed, b_alpha_EM is retained as a finite qbar_XT coefficient.",
            "formula": "|b_alpha_EM| <= 2|z_g| + |z_lambda| + |z_readout| + |z_rad|",
            "derivation": "Triangle inequality on the normal form; no cancellation between current normalization, F2 normalization and readout/radiative terms.",
            "status": "BOUND_BRANCH_READY_VALUES_MISSING",
            "source_anchor": "ARE3507_0_b_alpha_X;FAP1399_0_alphaEM_residual",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "EGK4614_3_Maxwell_stress_limit",
            "claim": "The local Maxwell stress limit is clean only if the observed Hodge/coframe, Maxwell kinetic normalization and same current owner descend together.",
            "formula": "S_EM=-1/4 Z_A F_Q wedge *_obs F_Q; T_EM varies through e_obs with fixed Z_A and fixed current owner",
            "derivation": "With fixed Z_A and observed Hodge, EM stress joins total Hilbert stress; if Z_A or Hodge/readout varies, retain EM residual rows.",
            "status": "MAXWELL_LIMIT_CONDITIONAL_NOT_CLAIMED",
            "source_anchor": "EMB3503_0_Delta_Hodge_EM;EMB3503_1_w_EM;EMF3502_5_matter_EM_internal_exchange",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "EGK4614_4_next_source_throat",
            "claim": "The immediate derivation target is no-extra-F2/operator-domain exhaustion; otherwise lambda_A becomes the first b_alpha source input.",
            "formula": "Z_A = C_P N_Q + lambda_A + f_X + Z_readout/rad",
            "derivation": "The current corpus explicitly keeps lambda_A/f_X F^2 legal unless operator-domain exhaustion is derived.",
            "status": "NEXT_TARGET_SELECTED",
            "source_anchor": "TQS1100_3_unique_curvature_norm;VEB3505_6_C_XF2;STAT3525_2_scalar_throat",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def owner_rows(now: str) -> list[dict[str, Any]]:
    clauses = [
        ("OWN4614_0_parent_TQ", "T_Q parent object", "T_Q is in the parent gauge algebra/lattice before observed readout", "PARTIAL_TEMPLATE_ONLY", "TQS1100_0_parent_TQ_object"),
        ("OWN4614_1_charge_lattice", "fixed charge lattice", "charge labels n_A are fixed representation/winding data with nonrescalable base unit", "PARTIAL_INTEGER_LABELS_BASE_UNIT_UNSIGNED", "TQS1100_1_fixed_charge_lattice"),
        ("OWN4614_2_generator_norm", "fixed generator norm", "N_Q=<T_Q,T_Q>_P is fixed by parent metric/symplectic/level/lattice data", "NOT_PARENT_SIGNED", "TQS1100_2_fixed_generator_norm"),
        ("OWN4614_3_unique_F2", "unique Maxwell F2", "no independent lambda_A F_Q^2 or f_X(Phi)F_Q^2 counterterm", "FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL", "TQS1100_3_unique_curvature_norm"),
        ("OWN4614_4_same_current", "same current owner", "J_Q is the Noether current of the same T_Q owner with no q_A(X) or current weights", "NOT_PARENT_SIGNED", "TQS1100_4_same_current_owner"),
        ("OWN4614_5_readout_radiative", "readout/radiative guard", "effective/readout alpha remains in quotient-owned EM algebra", "UNSIGNED", "TQS1100_5_readout_radiative_guard"),
        ("OWN4614_6_verdict", "b_alpha zero contract", "all owner clauses close together", "ZERO_NOT_PROMOTED_RETAIN_B_ALPHA", "TQS1100_6_verdict;AGN1047_4_verdict"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "clause_id": clause_id,
            "owner_clause": owner_clause,
            "required_statement": required_statement,
            "current_status": current_status,
            "source_anchor": source_anchor,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        }
        for clause_id, owner_clause, required_statement, current_status, source_anchor in clauses
    ]


def b_alpha_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("BA4614_0_b_alpha", "b_alpha_EM", "Lie_v ln alpha_EM", "2 z_g - z_lambda - z_readout - z_rad", "MISSING_ZERO_OR_VALUE", "dimensionless"),
        ("BA4614_1_z_g", "z_g", "current/charge normalization derivative", "Lie_v ln g_J", "CURRENT_OWNER_UNSIGNED", "dimensionless"),
        ("BA4614_2_z_lambda", "z_lambda", "Maxwell kinetic normalization derivative", "Lie_v ln Z_A or Lie_v ln lambda_A", "KINETIC_OWNER_UNSIGNED", "dimensionless"),
        ("BA4614_3_C_XF2", "C_XF2/lambda_A", "independent scalar multiplier of F_Q^2", "lambda_A or f_X(Phi) F_Q^2 coefficient", "CORE_COUPLING_THROAT", "model_dependent"),
        ("BA4614_4_z_readout", "z_readout", "spectral/clock/readout derivative of alpha", "Lie_v ln readout_alpha", "READOUT_OWNER_UNSIGNED", "dimensionless"),
        ("BA4614_5_z_rad", "z_rad", "effective/radiative regenerated F2 coefficient", "loop/readout/radiative alpha tail", "RADIATIVE_CLOSURE_UNSIGNED", "dimensionless"),
        ("BA4614_6_bound", "b_alpha_EM_abs", "absolute finite branch", "2|z_g|+|z_lambda|+|z_readout|+|z_rad|", "VALUES_MISSING_NONCLAIM", "dimensionless"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "quantity": quantity,
            "definition": definition,
            "formula_or_bound": formula,
            "current_status": status,
            "units": units,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        }
        for row_id, quantity, definition, formula, status, units in rows
    ]


def maxwell_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("MX4614_0_Hodge", "Delta_Hodge_EM", "EM Hodge/constitutive flow differs from observed coframe", "zero if *_EM=*_obs[e_obs(q)]", "MISSING_PARENT_SIGNATURE"),
        ("MX4614_1_wEM", "w_EM", "independent multiplier of observed Maxwell action/stress", "zero if unique Maxwell curvature norm plus alpha/current owner", "RETAINED_NORMALIZATION_COEFFICIENT"),
        ("MX4614_2_CXF2", "C_XF2", "hidden/motion/time coefficient multiplying F^2 or F*F", "zero if operator-domain exhaustion forbids hidden-visible EM coefficient morphisms", "RETAINED_OPERATOR_COEFFICIENT"),
        ("MX4614_3_CJQ", "C_JQ", "charge/current normalization not fixed by same parent owner", "zero if T_Q, representation weights and current normalization fixed together", "PARENT_CHARGE_VALUES_MISSING"),
        ("MX4614_4_Poynting", "Phi_EM_rad/(G_ref M_H)", "net radiative/background EM energy flux through local boundary", "zero for stationary isolated local branch", "RETAINED_FLUX_COEFFICIENT"),
        ("MX4614_5_readout", "C_EM_readout", "effective readout/loop/clock/spectroscopy map regenerates EM coefficient dependence", "zero if readout/radiative closure preserves visible pullback", "RETAINED_EFFECTIVE_COEFFICIENT"),
        ("MX4614_6_exchange", "epsilon_internal_exchange", "matter-EM Lorentz exchange cancels only in total stress", "zero in total Hilbert stress if same current/action owner", "CONDITIONAL_ZERO_IN_TOTAL_HILBERT_STRESS"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "quantity": quantity,
            "meaning": meaning,
            "zero_condition": zero_condition,
            "current_status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        }
        for row_id, quantity, meaning, zero_condition, status in rows
    ]


def arena_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("ARENA4614_0_clock", "clock/fine-structure", "Delta ln(nu_a/nu_b)=Delta K_alpha^{ab} b_alpha_EM tau_clock + other marker terms", "BLOCKED_CLOCK_PRODUCT_ONLY"),
        ("ARENA4614_1_WEP", "WEP/Coulomb composition", "eta_alpha <= beta_source_alpha b_alpha_EM tau_WEP plus EM binding/source-normalization residuals", "BLOCKED_WEP_SOURCE_MAP_MISSING"),
        ("ARENA4614_2_R10", "short-range material force", "alpha_bulk(lambda) receives beta_EM(lambda_A) and Qbar_XH*qbar_XT material legs", "BLOCKED_R10_MATERIAL_KERNEL_MISSING"),
        ("ARENA4614_3_Maxwell", "Maxwell stress/Poynting", "fixed Z_A and observed Hodge give standard stress; finite rows feed Delta_Hodge/w_EM/C_XF2/Poynting", "MAXWELL_LIMIT_CONDITIONAL"),
        ("ARENA4614_4_local_GR_Newton", "local GR/Newton", "finite R_EM_local(lambda_A) must vanish or be bounded inside local residual vector", "LOCAL_VECTOR_INCOMPLETE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "arena_id": arena_id,
            "arena": arena,
            "projection_formula": formula,
            "current_status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        }
        for arena_id, arena, formula, status in rows
    ]


def coefficient_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BSR4614_0_b_alpha_source_row",
            "quantity": "b_alpha_EM(lambda_A)",
            "definition": "finite vertical derivative of fine-structure/gauge kinetic data if zero contract is unsigned",
            "required_columns": "system_id;lambda_X;b_alpha_EM;z_g;z_lambda;z_readout;z_rad;normalization;units;source_path;equation_ref;valid_for_claim",
            "current_value": "MISSING_DERIVATIVE_MAP",
            "units": "dimensionless",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BSR4614_1_lambdaA_source_row",
            "quantity": "lambda_A or C_XF2",
            "definition": "independent F_Q^2 coefficient or hidden-visible EM scalar multiplier",
            "required_columns": "operator_id;lambda_A;f_X;support;normalization;sign;units;source_path;operator_domain_status;valid_for_claim",
            "current_value": "MISSING_NO_EXTRA_F2_PROOF_OR_VALUE",
            "units": "operator_dimension_dependent",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BSR4614_2_alpha_product_row",
            "quantity": "alphaEM_product_projection",
            "definition": "arena product using b_alpha_EM only after source-backed derivative and tau/kernel rows exist",
            "required_columns": "arena;K_alpha_or_beta;beta_source_alpha;tau;bound;source_path;valid_for_claim",
            "current_value": "MISSING_ARENA_PROJECTIONS",
            "units": "arena_declared",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def qbarxt_update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QEU4614_0_balpha_insert",
            "quantity": "qbar_theta_marker_abs",
            "update_formula": "replace |b_alpha| slot with |b_alpha_EM| <= 2|z_g|+|z_lambda|+|z_readout|+|z_rad|",
            "zero_condition": "all gauge kinetic/current/readout clauses close in the same parent branch",
            "current_status": "QBARXT_EM_SLOT_REFINED_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QEU4614_1_Maxwell_Qbulk",
            "quantity": "Q_bulk_EM/Poynting_abs",
            "update_formula": "finite b_alpha/C_XF2/w_EM/Delta_Hodge/Poynting/readout rows feed the EM bulk/source side instead of disappearing",
            "zero_condition": "fixed Maxwell action plus observed Hodge plus stationary/no-readout-regeneration branch",
            "current_status": "EM_BULK_REMAINS_CONDITIONAL",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4614_0_no_public_push", "rule": "work stays local/private; no GitHub push, no public repo mutation", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4614_1_no_unit_alpha", "rule": "alpha_EM is dimensionless and cannot be unit-gauged away", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4614_2_no_Ward_overclaim", "rule": "Ward/Noether current ownership does not by itself fix the Maxwell kinetic coefficient", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4614_3_no_charge_quantization_overclaim", "rule": "charge quantization or compact U1 labels do not alone determine continuous alpha_EM", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4614_4_no_cancellation", "rule": "z_g, z_lambda, readout and radiative branches are absolute-bounded, not cancellation-fitted", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4614_0_no_extra_F2", "blocks": "b_alpha_EM zero", "missing": "operator-domain exhaustion forbidding lambda_A/f_X F_Q^2", "resolution": NEXT_TARGET, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4614_1_gauge_norm", "blocks": "gauge kinetic derivation", "missing": "parent-fixed fibre metric/topological level/generator norm", "resolution": "derive fixed N_Q or keep z_lambda finite", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4614_2_current_owner", "blocks": "source/test charge normalization", "missing": "same T_Q Noether current owner and nonrescalable charge unit", "resolution": "derive current owner or retain z_g/beta_source_alpha", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4614_3_readout", "blocks": "clock/alpha readout silence", "missing": "readout/radiative closure preserving parent EM owner", "resolution": "derive closure or retain z_readout/z_rad", "valid_for_claim": False, "generated_utc": now},
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4614_0_source_traceability", "requirement": "every cited EM source path exists and every cited row needle is found", "current_status": "PASS" if all(row["path_exists"] and row["needle_found"] for row in sources) else "FAIL", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4614_1_zero_contract", "requirement": "T_Q object, charge lattice, generator norm, unique F2, same current owner and readout closure all parent-signed", "current_status": "BLOCKED_PARENT_UNSIGNED", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4614_2_balpha_source", "requirement": "finite b_alpha source row has z_g,z_lambda,z_readout,z_rad values, units and source paths", "current_status": "BLOCKED_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4614_3_Maxwell_local", "requirement": "Delta_Hodge,w_EM,C_XF2,C_JQ,Poynting,readout rows are zero or source-backed", "current_status": "BLOCKED_EM_RESIDUALS_OPEN", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "decision": DECISION,
        "meaning": "The alpha/EM throat is now a precise normal form: zero is a conjunctive parent-owner theorem, otherwise b_alpha_EM is a live coefficient.",
        "next_target": NEXT_TARGET,
        "valid_for_claim": False,
        "generated_utc": now,
    }]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "status": DECISION,
        "what_moved": "b_alpha_EM is reduced to current normalization, Maxwell kinetic normalization and readout/radiative derivatives, with explicit zero clauses and finite coefficient rows.",
        "what_did_not_move": "No alpha prediction, Maxwell pass, WEP/clock/R10 pass, Newton/local-GR pass or no-extra-F2 proof is claimed.",
        "valid_for_claim": False,
        "generated_utc": now,
    }]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "generated_utc": now,
        "next_target": NEXT_TARGET,
        "reason": "The strongest blocker is the legal lambda_A/f_X F^2 counterterm; proving no-extra-F2 would close the main b_alpha throat more directly than circling all local tests.",
        "derive_first": "prove operator-domain exhaustion forbids independent lambda_A F_Q^2 and f_X(Phi)F_Q^2 terms in the visible EM action",
        "fallback": "stage lambda_A/C_XF2 as the first finite source-backed b_alpha input row",
        "valid_for_claim": False,
    }]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4614 - EM Gauge-Kinetic Descent Or `b_alpha` Source Row

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register row: `{CLAIM_ID}`

## Decision

`{DECISION}`

The EM coupling throat is now the normal form

```text
b_alpha_EM := Lie_v ln(alpha_EM) = 2 z_g - z_lambda - z_readout - z_rad.
```

So the exact zero route is not "EM is gauge invariant". It is the joined contract:

```text
fixed parent T_Q,
fixed charge lattice and base unit,
fixed generator norm / gauge kinetic owner,
no independent lambda_A F_Q^2 or f_X(Phi)F_Q^2,
same Noether current owner,
and readout/radiative closure.
```

If that contract fails, retain

```text
|b_alpha_EM| <= 2|z_g| + |z_lambda| + |z_readout| + |z_rad|.
```

This is not a Maxwell/local-GR pass; it is the sharpest EM coupling gate so far.

## Source Register

{markdown_table(tables["sources"])}

## EM Gauge-Kinetic Theorem

{markdown_table(tables["theorem"])}

## Gauge Owner Clauses

{markdown_table(tables["owner"])}

## `b_alpha` Normal Form Rows

{markdown_table(tables["balpha"])}

## Maxwell Stress Limit Rows

{markdown_table(tables["maxwell"])}

## Arena Projection Rows

{markdown_table(tables["arena"])}

## `b_alpha` Source Rows

{markdown_table(tables["coefficients"])}

## `qbar_XT` / EM Update Rows

{markdown_table(tables["qbarxt_update"])}

## Controls

{markdown_table(tables["controls"])}

## Claim Blockers

{markdown_table(tables["blockers"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Next Target

`{NEXT_TARGET}`

The best next derivation is the no-extra-`F^2` operator-domain proof. If that fails, `lambda_A/C_XF2` becomes the first finite source-backed `b_alpha` input.

Private nonclaim. No GitHub action. No alpha, Maxwell, WEP, clock, R10, PPN, orbital, Newton or local-GR pass is claimed.
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 Formal Addendum 630 - EM Gauge-Kinetic Descent Gate

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

## Normal Form

The EM fine-structure leakage is

```text
b_alpha_EM := Lie_v ln(alpha_EM) = 2 z_g - z_lambda - z_readout - z_rad.
```

Here `z_g` is current/charge normalization, `z_lambda` is Maxwell kinetic normalization, and `z_readout,z_rad` are effective readout/radiative regeneration terms.

The zero branch is

```text
z_g=z_lambda=z_readout=z_rad=0,
no lambda_A F_Q^2,
no f_X(Phi)F_Q^2,
fixed T_Q, fixed charge lattice, fixed generator norm,
same Noether current owner.
```

The retained branch is

```text
|b_alpha_EM| <= 2|z_g| + |z_lambda| + |z_readout| + |z_rad|.
```

## Maxwell Link

The Maxwell stress limit is conditional on fixed `Z_A`, observed Hodge/coframe descent, same current owner and no readout/radiative regeneration. Otherwise the EM residual vector remains live.

Next target: `{NEXT_TARGET}`.
"""


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
    add("VAL4614_00_sources_exist_and_needles_found", not missing_sources, "missing: " + ",".join(missing_sources) if missing_sources else "all cited paths/needles found")

    csv_paths = [
        SOURCE_REGISTER, THEOREM_CSV, OWNER_CSV, B_ALPHA_CSV, MAXWELL_CSV, ARENA_CSV, COEFFICIENT_CSV,
        QBARXT_UPDATE_CSV, CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV,
    ]
    csv_ok = True
    details = []
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4614_01_csv_parse", csv_ok, ";".join(details))

    theorem_text = "\n".join(str(row) for row in tables["theorem"])
    owner_text = "\n".join(str(row) for row in tables["owner"])
    balpha_text = "\n".join(str(row) for row in tables["balpha"])
    maxwell_text = "\n".join(str(row) for row in tables["maxwell"])
    arena_text = "\n".join(str(row) for row in tables["arena"])
    add("VAL4614_02_normal_form", "b_alpha_EM := Lie_v ln(alpha_EM)" in theorem_text and "2 z_g - z_lambda" in theorem_text, "b_alpha normal form present")
    add("VAL4614_03_zero_contract", "unique Maxwell F2" in owner_text and "same current owner" in owner_text, "zero owner clauses present")
    add("VAL4614_04_bound_branch", "2|z_g|+|z_lambda|" in balpha_text or "2|z_g| + |z_lambda|" in theorem_text, "absolute b_alpha bound present")
    add("VAL4614_05_Maxwell_rows", "Delta_Hodge_EM" in maxwell_text and "C_XF2" in maxwell_text and "C_JQ" in maxwell_text, "Maxwell residual rows present")
    add("VAL4614_06_arena_rows", "clock/fine-structure" in arena_text and "short-range material force" in arena_text and "local GR/Newton" in arena_text, "arena projections present")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "claim_pass", "empirical_pass_claimed", "score_ready"} and value is True:
                    all_false = False
    add("VAL4614_07_no_claim_true", all_false, "no generated row promotes a claim")
    add("VAL4614_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4614_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4614_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4614_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4614_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4614_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4614_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4614_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4614_OVERALL", all(row["status"] == "PASS" for row in rows), "4614 EM gauge kinetic descent gate")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "theorem": theorem_rows(now),
        "owner": owner_rows(now),
        "balpha": b_alpha_rows(now),
        "maxwell": maxwell_rows(now),
        "arena": arena_rows(now),
        "coefficients": coefficient_rows(now),
        "qbarxt_update": qbarxt_update_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(THEOREM_CSV, tables["theorem"])
    write_csv(OWNER_CSV, tables["owner"])
    write_csv(B_ALPHA_CSV, tables["balpha"])
    write_csv(MAXWELL_CSV, tables["maxwell"])
    write_csv(ARENA_CSV, tables["arena"])
    write_csv(COEFFICIENT_CSV, tables["coefficients"])
    write_csv(QBARXT_UPDATE_CSV, tables["qbarxt_update"])
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
## PPC4161 Local Addendum - EM Gauge-Kinetic Descent Gate

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The EM/fine-structure slot now has the normal form `b_alpha_EM := Lie_v ln(alpha_EM) = 2 z_g - z_lambda - z_readout - z_rad`. The zero branch requires fixed parent `T_Q`, fixed charge lattice/base unit, fixed generator norm, no independent `lambda_A F_Q^2` or `f_X(Phi)F_Q^2`, same Noether current owner, and readout/radiative closure. Without that package, `b_alpha_EM` remains a finite qbar_XT/EM residual coefficient.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - EM Gauge-Kinetic Descent Gate

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private packet now treats alpha_EM as the sharp EM coupling throat. Charge quantization, Ward identity, unit conventions and calibration are not enough; the next pressure point is the no-extra-F2 operator-domain proof or a finite lambda_A/C_XF2 source row.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4614 validation failed: {failed}")
    print(f"4614 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
