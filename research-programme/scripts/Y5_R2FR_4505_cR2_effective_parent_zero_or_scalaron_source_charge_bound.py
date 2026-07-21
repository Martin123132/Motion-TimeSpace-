from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deltaktf_shell_profile_gate import read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4505"
CLAIM_ID = "L-347"
MARKER = "PPC4161_CR2_EFFECTIVE_PARENT_ZERO_OR_SCALARON_SOURCE_CHARGE_BOUND_4505"
PACKET_MARKER = "PPC4161_PACKET_CR2_EFFECTIVE_PARENT_ZERO_OR_SCALARON_SOURCE_CHARGE_BOUND_4505"
DECISION = "CR2EFF_POSITIVE_MATRIX_AND_BODY_CHARGE_GREEN_FUNCTION_GATE_DERIVED_MEMORY_FIBRE_OWNER_ROWS_REMAIN_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4506-Y5-R2FR-memory-fibre-BX-CX-owner-or-body-charge-input-row.md"

FORMAL_PATH = FORMAL / "521-PPC4161-cR2-effective-parent-zero-or-scalaron-source-charge-bound.md"
DOC_PATH = POST / "4505-Y5-R2FR-cR2-effective-parent-zero-or-scalaron-source-charge-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4505_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4505_SOURCE_REGISTER.csv"
ZERO_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4505_CR2_ZERO_THEOREM.csv"
POSITIVE_LEMMA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4505_POSITIVE_MATRIX_LEMMA.csv"
BODY_CHARGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4505_BODY_CHARGE_GREEN_FUNCTION_LAW.csv"
BOUND_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4505_SCALARON_BOUND_CONTRACT.csv"
DIRECT_ROWS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4505_DIRECT_SCALAR_PRESSURE_ROWS.csv"
PARENT_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4505_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4505_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4505_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4505_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4505_DECISION.csv"

FORMAL_520 = FORMAL / "520-PPC4161-R2-fR-scalar-mode-double-zero-or-first-coefficient-bound.md"
POST_4504 = POST / "4504-Y5-R2FR-R2-fR-scalar-mode-double-zero-or-first-coefficient-bound.md"
SCRIPT_4504 = SCRIPT_DIR / "Y5_R2FR_4504_R2_fR_scalar_mode_double_zero_or_first_coefficient_bound.py"
STATUS_4504 = SOURCE_DIR / "P8_Y5_R2FR_4504_STATUS.csv"
COEFF_4504 = SOURCE_DIR / "P8_Y5_R2FR_4504_MTS_COEFFICIENT_LAW_MERGE.csv"
BOUND_4504 = SOURCE_DIR / "P8_Y5_R2FR_4504_FINITE_BOUND_CONTRACT.csv"
COMPONENT_BUDGET_4501 = SOURCE_DIR / "P8_Y5_R2FR_4501_COMPONENT_TRANSFER_BUDGET.csv"

POST_1343 = POST / "1343-Y5-R10-RAB-R2FR-parent-coefficient-zero-signature-or-finite-scalar-map-fill.md"
POST_1344 = POST / "1344-Y5-R10-RAB-no-XR-vertex-theorem-or-retained-scalar-source-charge-row.md"
POST_1345 = POST / "1345-Y5-R10-RAB-parent-vertex-inventory-by-generator-or-source-charge-runner-inputs.md"
POST_1346 = POST / "1346-Y5-R10-RAB-memory-and-fibre-vertex-zero-or-symbolic-coefficient-fill.md"
POST_2250 = POST / "2250-Y5-R2FR-RAB-parent-matter-curvature-source-signature-or-first-body-charge-row.md"
POST_4471 = POST / "4471-Y5-R2FR-no-local-length-scale-or-grain-proof-or-first-cR2eff-intake-row.md"
POST_4476 = POST / "4476-Y5-R2FR-parent-action-inventory-signature-or-lambdaM-projection-map.md"
POST_4479 = POST / "4479-Y5-R2FR-profile-symmetry-dimension-branch-or-anisotropic-quadrupole-bound.md"
GENERATOR_MATRIX_1345 = SOURCE_DIR / "P8_Y5_R10_1345_GENERATOR_VERTEX_MATRIX.csv"
COEFF_PACK_1346 = SOURCE_DIR / "P8_Y5_R10_1346_SYMBOLIC_COEFFICIENT_PACK.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    return read_csv(path)


def rows_by(path: Path, key: str) -> Dict[str, Dict[str, str]]:
    return {row[key]: row for row in csv_rows(path) if key in row}


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def constants() -> Dict[str, float]:
    row = rows_by(COMPONENT_BUDGET_4501, "budget_id").get("CB4501_A_E", {})
    return {
        "equal_a": float(row.get("equal_no_cancellation_A_budget", "3.502129240739837e-14")),
        "single_a": float(row.get("single_survivor_A_bound", "1.400851696295935e-13")),
        "mu_bound_m2": 1.443476e15,
        "lambda_r_m": 9.306372e7,
    }


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4505_00_formal520", "4504 formal handoff", FORMAL_520, "c_R2_eff_total_or_scalaron_body_charge", "4504 selected target"),
        ("SRC4505_01_post4504", "4504 post mirror", POST_4504, "c_R2_eff_total_or_scalaron_body_charge", "post checkpoint target"),
        ("SRC4505_02_script4504", "4504 generator", SCRIPT_4504, 'CHECKPOINT = "4504"', "reproducible predecessor"),
        ("SRC4505_03_status4504", "4504 status", STATUS_4504, "c_R2_eff_total_or_scalaron_body_charge", "first open component"),
        ("SRC4505_04_coeff4504", "4504 coefficient law", COEFF_4504, "CL4504_0_total_effective", "effective c_R2 law"),
        ("SRC4505_05_bound4504", "4504 finite bound contract", BOUND_4504, "FB4504_3_yukawa_hessian", "scalaron Hessian bound"),
        ("SRC4505_06_1343_law", "1343 coefficient law", POST_1343, "LAW1343_0_quadratic_parent_block", "hidden-mode coefficient law"),
        ("SRC4505_07_1344_charge", "1344 source-charge law", POST_1344, "Q_X[body]", "body charge law"),
        ("SRC4505_08_1345_matrix", "1345 generator matrix", POST_1345, "VM1345_4_memory_class_scalar", "direct scalar pressure rows"),
        ("SRC4505_09_1346_packs", "1346 coefficient packs", POST_1346, "COEFF1346_M_B", "memory/fibre symbolic pack"),
        ("SRC4505_10_2250_body", "2250 body-charge precedent", POST_2250, "BCR2250_1_body_charge", "body charge schema"),
        ("SRC4505_11_4471_visible", "4471 no-grain component", POST_4471, "NG4471_1_refinement_gauge_zero", "visible c_cell zero route"),
        ("SRC4505_12_4476_marker", "4476 marker projection", POST_4476, "PMAP4476_1_curvature_square", "marker c_R2 projection"),
        ("SRC4505_13_4479_quad", "4479 quadrupole bound", POST_4479, "LSS4479_4_quadrupole_bound", "shape anisotropy fallback"),
        ("SRC4505_14_matrix_csv", "1345 generator matrix csv", GENERATOR_MATRIX_1345, "VM1345_4_memory_class_scalar", "machine-readable direct row"),
        ("SRC4505_15_pack_csv", "1346 coefficient pack csv", COEFF_PACK_1346, "COEFF1346_M_B", "machine-readable coefficient pack"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, role, path, needle, note in specs:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text(path),
                "line": line_of(path, needle),
                "note": note,
                "valid_for_claim": False,
            }
        )
    return rows


def zero_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "ZC4505_0_componentwise_zero",
            "target": "c_R2_eff_total",
            "statement": "Without a named parent identity, c_R2_eff_total is zero only when every retained component is zero/topological/boundary-silent in the same branch.",
            "formula": "c_R2_eff_total=c_cell+c_bare+1/2 B^T L^-1 B+c_measure+c_boundary+c_marker",
            "derived_result": "componentwise_zero_or_parent_identity_required",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ZC4505_1_positive_hidden_block",
            "target": "0.5 B^T L^-1 B",
            "statement": "For positive definite L, the hidden-mode curvature block is nonnegative and vanishes iff B=0 on the physical subspace.",
            "formula": "B^T L^-1 B = ||L^-1/2 B||^2 >= 0",
            "derived_result": "no-XR/no-curvature-vertex is mathematically necessary for this block",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ZC4505_2_source_charge_zero",
            "target": "A_body",
            "statement": "The exterior scalar tail is zero if the weighted body source and boundary charge vanish, not merely because the exterior region has T=0.",
            "formula": "A_body=0 iff Q_X[body]+Q_boundary=0 under the selected Green-function convention",
            "derived_result": "body_charge_zero_switch_written",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "ZC4505_3_memory_fibre_pressure",
            "target": "direct scalar pressure rows",
            "statement": "The direct R2/fR pressure rows are memory/class scalar and finite-cell fibre spectrum.",
            "formula": "memory: {Z_mem,M2_mem,B_mem,C_mem,J_mem,Qb_mem}; fibre: {Z_h,M2_h,B_h,C_h,J_h,Qb_h}",
            "derived_result": "direct_rows_selected_for_next_owner_search",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def positive_lemma_rows() -> List[Dict[str, object]]:
    return [
        {
            "lemma_id": "PM4505_0_positive_definite",
            "assumption": "L is positive definite on the retained physical scalar/memory/fibre subspace",
            "derivation": "write L=L^1/2 L^1/2 and B^T L^-1 B=(L^-1/2 B)^T(L^-1/2 B)",
            "conclusion": "B^T L^-1 B>=0 and equals zero iff B=0",
            "effect": "a finite curvature-linear vertex cannot be hidden by positive no-hair; it creates c_R2_eff",
            "valid_for_claim": False,
        },
        {
            "lemma_id": "PM4505_1_semidefinite_or_gauge",
            "assumption": "L has gauge/kernel directions",
            "derivation": "the inverse is defined only on the physical quotient/range; source components along a nonproper boundary/kernel require separate constraints",
            "conclusion": "zero requires B projected to every physical propagating direction to vanish and boundary charges to be proper/exact/zero",
            "effect": "quotient language helps only after the physical projection and boundary charge are signed",
            "valid_for_claim": False,
        },
        {
            "lemma_id": "PM4505_2_no_cancellation_guard",
            "assumption": "no parent Ward/topological identity is supplied",
            "derivation": "opposite-sign bare/measure/boundary terms can cancel numerically only as closure or tuning",
            "conclusion": "componentwise absolute residuals are required for local-GR evidence",
            "effect": "do not count c_bare + B^T L^-1 B + c_measure cancellation as derivation",
            "valid_for_claim": False,
        },
    ]


def body_charge_rows() -> List[Dict[str, object]]:
    return [
        {
            "law_id": "BC4505_0_generic_field",
            "field_equation": "(-Z_X nabla^2 + M_X^2) X = rho_X",
            "source_density": "rho_X=B_X R_obs + C_X T + J_X",
            "exterior_profile": "X(r,n)=A_X(n) exp(-r/lambda_X)/r + higher multipoles",
            "charge_formula": "A_X(n)=Q_X(n)/(4*pi*Z_X)+A_boundary, Q_X(n)=int_body exp(n.x'/lambda_X) rho_X(x') dV'",
            "zero_condition": "Q_X(n)=0 for all directions plus A_boundary=0",
            "valid_for_claim": False,
        },
        {
            "law_id": "BC4505_1_spherical_monopole",
            "field_equation": "static spherical massive scalar",
            "source_density": "rho_X(r)",
            "exterior_profile": "X(r)=A_X exp(-r/lambda_X)/r",
            "charge_formula": "Q_X0=4*pi int_0^R dr' r'^2 rho_X(r') sinh(r'/lambda_X)/(r'/lambda_X)",
            "zero_condition": "weighted monopole Q_X0 plus boundary charge vanishes",
            "valid_for_claim": False,
        },
        {
            "law_id": "BC4505_2_absolute_bound",
            "field_equation": "same generic branch",
            "source_density": "rho_X with support radius R_body",
            "exterior_profile": "|A_X| bound",
            "charge_formula": "|A_X| <= [exp(R_body/lambda_X) int_body |rho_X| dV + |Q_boundary|]/(4*pi |Z_X|)",
            "zero_condition": "finite bound route if zero theorem fails",
            "valid_for_claim": False,
        },
        {
            "law_id": "BC4505_3_scalaron_mapping",
            "field_equation": "(nabla^2-m_R^2)R=S_R",
            "source_density": "S_R is the MTS-mapped scalaron source, conventionally kappa T/(6 mu) only in standard f(R)",
            "exterior_profile": "R=A_body exp(-m_R r)/r",
            "charge_formula": "A_body is the corresponding weighted Green-function charge after MTS source/frame/screening normalization",
            "zero_condition": "A_body=0 or short-range/finite bound",
            "valid_for_claim": False,
        },
    ]


def scalaron_bound_rows(c: Mapping[str, float]) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "SCB4505_0_hessian_envelope",
            "target": "DeltaE_R11 scalar Hessian channel",
            "formula": "H_R(r)=|A_body| exp(-m_R r)(m_R^2/r+3m_R/r^2+3/r^3)",
            "bound_condition": f"||W_STF||_1||K_2^X|| Pi_R H_R <= {c['equal_a']:.15e}",
            "needed_inputs": "A_body;m_R;support radius r;Pi_R;W_STF;K_2^X",
            "status": "DERIVED_BOUND_FORMULA_INPUTS_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "bound_id": "SCB4505_1_body_charge_bound",
            "target": "A_body finite row",
            "formula": "|A_body| <= [exp(R_body/lambda_R) int_body |S_R| dV + |Q_boundary|]/(4*pi |Z_R|)",
            "bound_condition": "insert into SCB4505_0 and PPN/R10 branches componentwise",
            "needed_inputs": "S_R;R_body;lambda_R;Z_R;Q_boundary;source path",
            "status": "GREEN_FUNCTION_BOUND_READY_INPUTS_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "bound_id": "SCB4505_2_standard_mu_template",
            "target": "standard f(R) coefficient branch",
            "formula": f"mu <= {c['mu_bound_m2']:.6e} m^2 and lambda_R <= {c['lambda_r_m']:.6e} m if unscreened standard branch is selected",
            "bound_condition": "requires MTS c_R2_eff_total -> mu map and body/source-charge normalization",
            "needed_inputs": "N_MTS_to_fR;c_R2_eff_total;screening;A_body/C_body",
            "status": "TEMPLATE_READY_MTS_MAP_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "bound_id": "SCB4505_3_R10_alpha",
            "target": "R10 Yukawa comparison",
            "formula": "alpha_X(lambda)=K_X beta_source(lambda) beta_test(lambda)+epsilon_tail(lambda)",
            "bound_condition": "abs(alpha_X(lambda)) <= alpha_bound(lambda) on claim-grade curve",
            "needed_inputs": "source/test charges;valid alpha_bound(lambda);lambda;tail;units",
            "status": "R10_PROJECTION_SHAPE_READY_INPUTS_UNSIGNED",
            "valid_for_claim": False,
        },
    ]


def direct_pressure_rows() -> List[Dict[str, object]]:
    matrix = rows_by(GENERATOR_MATRIX_1345, "matrix_id")
    coeff_pack = csv_rows(COEFF_PACK_1346)
    pack_ids = {row.get("pack_id", ""): row for row in coeff_pack}
    memory = matrix.get("VM1345_4_memory_class_scalar", {})
    fibre = matrix.get("VM1345_5_finite_fibre_spectrum", {})
    return [
        {
            "row_id": "DSPR4505_0_memory",
            "generator": memory.get("generator", "memory/class scalar"),
            "why_direct": "direct B_X X R and C_X T scalar pressure row",
            "required_zero": "B_mem=C_mem=J_mem=Q_boundary_mem=0 plus positive/gapped operator",
            "required_finite": "Z_mem,M2_mem,B_mem,C_mem,J_mem,Q_boundary_mem,W_mem,screening,source paths",
            "current_status": memory.get("classification", "RETAINED_SCALAR_SOURCE_CHARGE_SYMBOLIC_HIGH_PRIORITY"),
            "first_missing_owner": pack_ids.get("COEFF1346_M_B", {}).get("current_value", "MISSING_NO_XR_VERTEX_OR_VALUE"),
            "valid_for_claim": False,
        },
        {
            "row_id": "DSPR4505_1_fibre",
            "generator": fibre.get("generator", "finite-cell fibre spectrum"),
            "why_direct": "finite fibre can integrate out into R L^-1 R and matter/source charge",
            "required_zero": "unique source-independent h0, B_h=C_h=J_h=Q_boundary_h=0, gapped operator",
            "required_finite": "Z_h,M2_h,B_h,C_h,J_h,Q_boundary_h,W_h,screening,source paths",
            "current_status": fibre.get("classification", "RETAINED_FIBRE_SOURCE_CHARGE_SYMBOLIC_HIGH_PRIORITY"),
            "first_missing_owner": pack_ids.get("COEFF1346_H_B", {}).get("current_value", "MISSING_NO_FIBRE_CURVATURE_VERTEX_OR_VALUE"),
            "valid_for_claim": False,
        },
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PA4505_0_positive_hidden",
            "clause": "L positive and B_X=0 for memory/fibre physical directions",
            "current_status": "B_X_ZERO_UNSIGNED",
            "evidence": str(POST_1346),
            "effect": "hidden scalar/fibre R2 contribution remains live",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4505_1_source_charge",
            "clause": "C_X=J_X=Q_boundary=0 or weighted body charge zero",
            "current_status": "SOURCE_CHARGE_ZERO_UNSIGNED",
            "evidence": str(POST_1344),
            "effect": "exterior Yukawa tail may survive even with source-free exterior",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4505_2_visible_cell",
            "clause": "visible c_cell zero extends to total c_R2_eff",
            "current_status": "VISIBLE_ZERO_ONLY_TOTAL_UNSIGNED",
            "evidence": str(POST_4471),
            "effect": "bare/hidden/measure/boundary/marker residues remain possible",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4505_3_marker_projection",
            "clause": "marker ideal empty or c_marker=0",
            "current_status": "MARKER_INVENTORY_UNSIGNED",
            "evidence": str(POST_4476),
            "effect": "marker/readout materialization can generate c_R2_marker",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4505_4_mu_map",
            "clause": "MTS c_R2_eff_total maps to standard mu",
            "current_status": "NORMALIZATION_UNSIGNED",
            "evidence": str(POST_4504),
            "effect": "standard PPN/R10 bound remains a template",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4505_0_positive_matrix",
            "gate": "positive matrix no-XR lemma derived",
            "passed": True,
            "claim_allowed": False,
            "detail": "for positive L, hidden B block zero requires B=0",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4505_1_body_charge_law",
            "gate": "Green-function body-charge law derived",
            "passed": True,
            "claim_allowed": False,
            "detail": "A_body is a weighted interior/boundary charge, not erased by exterior source-free equations",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4505_2_direct_rows_selected",
            "gate": "direct scalar pressure rows selected",
            "passed": True,
            "claim_allowed": False,
            "detail": "memory/class scalar and finite fibre rows are selected as the next owner search",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4505_3_parent_zero_or_bound",
            "gate": "c_R2_eff_total or A_body parent-zero/numeric bound ready",
            "passed": False,
            "claim_allowed": False,
            "detail": "B/C/Z/M/source/body-charge inputs remain unsigned or symbolic",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4505_4_local_GR_promotion",
            "gate": "local GR/R2 scalar branch promoted",
            "passed": False,
            "claim_allowed": False,
            "detail": "4505 gives a sharper theorem/bound gate but no local-GR, PPN or R10 pass",
            "valid_for_claim": False,
        },
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "positive_matrix_lemma": True,
            "body_charge_green_law": True,
            "direct_scalar_pressure_rows": "memory_class_scalar;finite_fibre_spectrum",
            "c_R2_eff_zero_signed": False,
            "A_body_zero_or_bound_signed": False,
            "local_GR_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4505_0",
            "target": NEXT_TARGET,
            "preferred_route": "find a parent owner for B_mem/C_mem and B_h/C_h: branch extremum, symmetry, matter-blindness, source-independent mass gap, or action-inventory exclusion",
            "fallback_route": "source Z,M2,B,C,J,Q_boundary and body profile rows for memory/fibre, then execute the scalaron PPN/R10/A_E bound contracts",
            "do_not_do": "claim local GR from positive no-hair while B_X or body charge is still live",
            "valid_for_claim": False,
        }
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "what_moved_forward": "4505 proves the positive-matrix no-XR requirement and derives the Green-function body-charge bound for scalaron tails.",
            "what_is_derived": "if L is positive, B^T L^-1 B can vanish only when B vanishes; exterior Yukawa amplitude is a weighted body/boundary charge with an absolute bound.",
            "what_remains_blocked": "memory/fibre B,C,Z,M2,J and boundary charge rows are still not parent-owned or numeric.",
            "claim_status": "private_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def append_section_once(path: Path, marker: str, section: str) -> None:
    body = text(path)
    if marker in body:
        return
    path.write_text(body.rstrip() + "\n\n" + section.strip() + "\n", encoding="utf-8")


def append_claim_once() -> None:
    claim = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_r2fr_scalaron_source_charge",
        "claim": "4505 derives the positive-matrix condition for c_R2_eff hidden blocks and the scalaron body-charge Green-function law, reducing the R2/fR local-GR route to B_X/source-charge owner rows for memory and fibre sectors.",
        "current_evidence": "4505 source register, c_R2 zero theorem, positive matrix lemma, body-charge Green law, scalaron bound contract, direct pressure rows, parent audit, gates, status and validation.",
        "status": "private_cR2eff_body_charge_gate_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "using positive no-hair or exterior source-free equations while curvature vertices or body charges remain live.",
        "sector": "local_gr_newton_r2fr_scalaron_source_charge",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "memory/fibre B,C,Z,M2,J and boundary-charge rows remain unsigned or symbolic.",
    }
    rows = []
    if CLAIMS_PATH.exists():
        with CLAIMS_PATH.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = [
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
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(claim)


def generated_csv_paths() -> List[Path]:
    return [
        SOURCE_REGISTER,
        ZERO_THEOREM_CSV,
        POSITIVE_LEMMA_CSV,
        BODY_CHARGE_CSV,
        BOUND_CONTRACT_CSV,
        DIRECT_ROWS_CSV,
        PARENT_AUDIT_CSV,
        CLAIM_GATES_CSV,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]


def claim_flags_safe(rows: Iterable[Mapping[str, object]]) -> bool:
    for row in rows:
        for key in ("valid_for_claim", "claim_allowed"):
            if str(row.get(key, "")).lower() == "true":
                return False
    return True


def validation_rows(all_rows: Mapping[str, Sequence[Mapping[str, object]]]) -> List[Dict[str, object]]:
    sources = all_rows["sources"]
    csv_ok = True
    csv_detail: List[str] = []
    for path in generated_csv_paths():
        try:
            parsed = csv_rows(path)
            if not parsed:
                csv_ok = False
                csv_detail.append(f"{path.name}:empty")
        except Exception as exc:  # pragma: no cover
            csv_ok = False
            csv_detail.append(f"{path.name}:{exc}")

    flat_rows: List[Mapping[str, object]] = []
    for rows in all_rows.values():
        flat_rows.extend(rows)

    checks = [
        {
            "validation_id": "VAL4505_00_sources",
            "status": "PASS" if all(row["exists"] and row["needle_found"] for row in sources) else "FAIL",
            "detail": "all local source paths exist and needles found",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4505_01_positive_lemma",
            "status": "PASS" if any("B^T L^-1 B>=0" in str(row.get("conclusion", "")) for row in all_rows["positive"]) else "FAIL",
            "detail": "positive matrix no-XR lemma recorded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4505_02_body_charge",
            "status": "PASS" if any("Q_X0=4*pi" in str(row.get("charge_formula", "")) for row in all_rows["body"]) else "FAIL",
            "detail": "spherical body-charge Green-function law recorded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4505_03_direct_rows",
            "status": "PASS" if len(all_rows["direct"]) == 2 and all("MISSING" in str(row.get("first_missing_owner", "")) for row in all_rows["direct"]) else "FAIL",
            "detail": "memory/fibre direct scalar pressure rows selected and still unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4505_04_bound_contract",
            "status": "PASS" if any(row.get("bound_id") == "SCB4505_0_hessian_envelope" for row in all_rows["bound"]) else "FAIL",
            "detail": "scalaron Hessian envelope bound contract written",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4505_05_claims_blocked",
            "status": "PASS" if any(row.get("gate_id") == "CG4505_4_local_GR_promotion" and row.get("passed") is False for row in all_rows["gates"]) else "FAIL",
            "detail": "local GR/R2 scalar claim remains blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4505_06_claim_flags_safe",
            "status": "PASS" if claim_flags_safe(flat_rows) else "FAIL",
            "detail": "all generated rows keep valid_for_claim/claim_allowed false",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4505_07_csv_parse",
            "status": "PASS" if csv_ok else "FAIL",
            "detail": "all generated CSVs parse with rows" if csv_ok else "; ".join(csv_detail),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4505_08_next_target",
            "status": "PASS" if all_rows["next"] and all_rows["next"][0]["target"] == NEXT_TARGET else "FAIL",
            "detail": "4506 memory/fibre owner target selected",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4505_09_pycache_absent",
            "status": "PASS" if not (SCRIPT_DIR / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after cleanup",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "validation_id": "VAL4505_OVERALL",
            "status": overall,
            "detail": "4505 cR2 effective parent zero or scalaron source charge bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return checks


def build_doc(
    sources: Sequence[Mapping[str, object]],
    zero: Sequence[Mapping[str, object]],
    positive: Sequence[Mapping[str, object]],
    body: Sequence[Mapping[str, object]],
    bound: Sequence[Mapping[str, object]],
    direct: Sequence[Mapping[str, object]],
    parent: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    validation: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4505 - cR2 Effective Parent Zero Or Scalaron Source-Charge Bound

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Verdict

4505 pushes the R2/fR route one step deeper. The useful theorem is the positive-matrix obstruction:

`B^T L^-1 B = ||L^-1/2 B||^2 >= 0`.

So if the hidden/memory/fibre operator is positive, the integrated-out curvature-square block vanishes only when the curvature-linear vertex `B` vanishes on the physical subspace. Positive no-hair is not enough by itself; `B_X=0` is the thing that must be owned.

The source side is also now exact. For `(-Z_X nabla^2 + M_X^2)X=rho_X`, the exterior Yukawa coefficient is a weighted interior/boundary charge. For a spherical source,

`Q_X0=4*pi int_0^R dr r^2 rho_X(r) sinh(r/lambda_X)/(r/lambda_X)`.

That means exterior source-free equations do not erase body charge. The scalaron branch closes by `c_R2_eff_total=0`, or by `A_body=0`, or by a sourced finite bound. The direct rows to attack next are memory/class scalar and finite-cell fibre spectrum.

## Source Register

{table(sources)}

## cR2 Zero Theorem

{table(zero)}

## Positive Matrix Lemma

{table(positive)}

## Body-Charge Green-Function Law

{table(body)}

## Scalaron Bound Contract

{table(bound)}

## Direct Scalar Pressure Rows

{table(direct)}

## Parent Signature Audit

{table(parent)}

## Claim Gates

{table(gates)}

## Status

{table(status)}

## Decision

{table(decisions)}

## Next Target

{table(next_target)}

## Validation

{table(validation)}
"""


def main() -> None:
    c = constants()
    sources = source_rows()
    zero = zero_theorem_rows()
    positive = positive_lemma_rows()
    body = body_charge_rows()
    bound = scalaron_bound_rows(c)
    direct = direct_pressure_rows()
    parent = parent_audit_rows()
    gates = claim_gate_rows()
    status = status_rows()
    next_target = next_rows()
    decisions = decision_rows()

    all_rows = {
        "sources": sources,
        "zero": zero,
        "positive": positive,
        "body": body,
        "bound": bound,
        "direct": direct,
        "parent": parent,
        "gates": gates,
        "status": status,
        "next": next_target,
        "decisions": decisions,
    }

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_THEOREM_CSV, zero)
    write_csv(POSITIVE_LEMMA_CSV, positive)
    write_csv(BODY_CHARGE_CSV, body)
    write_csv(BOUND_CONTRACT_CSV, bound)
    write_csv(DIRECT_ROWS_CSV, direct)
    write_csv(PARENT_AUDIT_CSV, parent)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validation_rows(all_rows)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, zero, positive, body, bound, direct, parent, gates, status, next_target, decisions, validation)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)

    append_claim_once()
    append_section_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4505 cR2 Effective Parent Zero Or Scalaron Source-Charge Bound

Marker: `{MARKER}`  
4505 sharpens the R2/fR scalar branch. If the hidden/memory/fibre operator is positive, `B^T L^-1 B=||L^-1/2 B||^2`, so the integrated-out curvature-square block vanishes only when the curvature-linear vertex `B` vanishes on the physical subspace. The exterior scalaron amplitude is also a weighted body/boundary charge, not erased by exterior source-free equations. The next direct owner rows are memory/class scalar and finite-cell fibre spectrum.
""",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4505 Packet Integration

Marker: `{PACKET_MARKER}`  
The local packet now has a sharper scalaron gate: positive no-hair requires `B_X=0`, and exterior scalar silence requires a body-charge zero or a sourced finite bound. Next target is no longer broad R2/fR; it is the memory/fibre owner search for `B_mem`, `C_mem`, `B_h`, `C_h`, and their source-charge rows.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
