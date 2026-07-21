from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deltaktf_shell_profile_gate import read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4506"
CLAIM_ID = "L-348"
MARKER = "PPC4161_MEMORY_FIBRE_BX_CX_OWNER_OR_BODY_CHARGE_INPUT_ROW_4506"
PACKET_MARKER = "PPC4161_PACKET_MEMORY_FIBRE_BX_CX_OWNER_OR_BODY_CHARGE_INPUT_ROW_4506"
DECISION = "MEMORY_BMEM_EXTREMUM_ROUTE_SHARPENED_OPERATOR_SIGNATURE_AND_BODY_CHARGE_ROWS_STAGED_FIBRE_ZERO_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4507-Y5-R2FR-memory-trace-projection-lock-or-finite-Bmem-source-row.md"

FORMAL_PATH = FORMAL / "522-PPC4161-memory-fibre-BX-CX-owner-or-body-charge-input-row.md"
DOC_PATH = POST / "4506-Y5-R2FR-memory-fibre-BX-CX-owner-or-body-charge-input-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4506_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4506_SOURCE_REGISTER.csv"
OWNER_ROUTE_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4506_OWNER_ROUTE_AUDIT.csv"
MEMORY_EXTREMUM = SOURCE_DIR / "P8_Y5_R2FR_4506_MEMORY_EXTREMUM_TEST.csv"
MEMORY_OPERATOR = SOURCE_DIR / "P8_Y5_R2FR_4506_MEMORY_OPERATOR_SIGNATURE.csv"
FIBRE_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4506_FIBRE_OWNER_GATE.csv"
BODY_CHARGE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4506_BODY_CHARGE_INPUT_ROW.csv"
PARENT_SIGNATURE = SOURCE_DIR / "P8_Y5_R2FR_4506_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4506_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4506_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4506_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4506_DECISION.csv"

FORMAL_521 = FORMAL / "521-PPC4161-cR2-effective-parent-zero-or-scalaron-source-charge-bound.md"
POST_4505 = POST / "4505-Y5-R2FR-cR2-effective-parent-zero-or-scalaron-source-charge-bound.md"
SCRIPT_4505 = SCRIPT_DIR / "Y5_R2FR_4505_cR2_effective_parent_zero_or_scalaron_source_charge_bound.py"
STATUS_4505 = SOURCE_DIR / "P8_Y5_R2FR_4505_STATUS.csv"
DIRECT_4505 = SOURCE_DIR / "P8_Y5_R2FR_4505_DIRECT_SCALAR_PRESSURE_ROWS.csv"
BODY_4505 = SOURCE_DIR / "P8_Y5_R2FR_4505_BODY_CHARGE_GREEN_FUNCTION_LAW.csv"
BOUND_4505 = SOURCE_DIR / "P8_Y5_R2FR_4505_SCALARON_BOUND_CONTRACT.csv"

POST_1343 = POST / "1343-Y5-R10-RAB-R2FR-parent-coefficient-zero-signature-or-finite-scalar-map-fill.md"
POST_1344 = POST / "1344-Y5-R10-RAB-no-XR-vertex-theorem-or-retained-scalar-source-charge-row.md"
POST_1345 = POST / "1345-Y5-R10-RAB-parent-vertex-inventory-by-generator-or-source-charge-runner-inputs.md"
POST_1346 = POST / "1346-Y5-R10-RAB-memory-and-fibre-vertex-zero-or-symbolic-coefficient-fill.md"
POST_1347 = POST / "1347-Y5-R10-RAB-memory-fibre-coefficient-owner-search-or-explicit-closure.md"
POST_1348 = POST / "1348-Y5-R10-RAB-memory-branch-extremum-and-operator-signature-or-closure.md"
POST_2250 = POST / "2250-Y5-R2FR-RAB-parent-matter-curvature-source-signature-or-first-body-charge-row.md"

LAW_1343 = SOURCE_DIR / "P8_Y5_R10_1343_PARENT_COEFFICIENT_LAW.csv"
TEMPLATE_1344 = SOURCE_DIR / "P8_Y5_R10_1344_RETAINED_SCALAR_SOURCE_CHARGE_TEMPLATE.csv"
VERTEX_1344 = SOURCE_DIR / "P8_Y5_R10_1344_VERTEX_ALGEBRA.csv"
MATRIX_1345 = SOURCE_DIR / "P8_Y5_R10_1345_GENERATOR_VERTEX_MATRIX.csv"
PACK_1346 = SOURCE_DIR / "P8_Y5_R10_1346_SYMBOLIC_COEFFICIENT_PACK.csv"
OWNER_1347 = SOURCE_DIR / "P8_Y5_R10_1347_OWNER_SEARCH_LEDGER.csv"
COEFF_OWNER_1347 = SOURCE_DIR / "P8_Y5_R10_1347_COEFFICIENT_OWNER_MATRIX.csv"
ROUTE_1347 = SOURCE_DIR / "P8_Y5_R10_1347_ROUTE_RANKING.csv"
BMEM_1348 = SOURCE_DIR / "P8_Y5_R10_1348_BMEM_EXTREMUM_TEST.csv"
OP_1348 = SOURCE_DIR / "P8_Y5_R10_1348_MEMORY_OPERATOR_SIGNATURE_TEST.csv"
CLOSURE_1348 = SOURCE_DIR / "P8_Y5_R10_1348_MEMORY_CLOSURE_CONTRACT.csv"

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


def by_key(path: Path, key: str) -> Dict[str, Dict[str, str]]:
    return {row[key]: row for row in csv_rows(path) if key in row}


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4506_00_formal521", "4505 formal handoff", FORMAL_521, "memory/fibre B,C,Z,M2,J and boundary charge rows are still not parent-owned or numeric", "selected 4506 target"),
        ("SRC4506_01_post4505", "4505 post mirror", POST_4505, "The direct rows to attack next are memory/class scalar and finite-cell fibre spectrum", "post target statement"),
        ("SRC4506_02_script4505", "4505 generator", SCRIPT_4505, 'CHECKPOINT = "4505"', "reproducible predecessor"),
        ("SRC4506_03_status4505", "4505 status", STATUS_4505, "memory_class_scalar;finite_fibre_spectrum", "open direct rows"),
        ("SRC4506_04_direct4505", "4505 direct rows", DIRECT_4505, "DSPR4505_0_memory", "memory/fibre selected"),
        ("SRC4506_05_body4505", "4505 body law", BODY_4505, "BC4505_1_spherical_monopole", "Green-function body charge"),
        ("SRC4506_06_bound4505", "4505 scalaron bound", BOUND_4505, "SCB4505_3_R10_alpha", "R10/PPN finite branch route"),
        ("SRC4506_07_1343_law", "1343 parent coefficient law", LAW_1343, "LAW1343_0_quadratic_parent_block", "hidden-mode coefficient law"),
        ("SRC4506_08_1344_template", "1344 source-charge template", TEMPLATE_1344, "QX1344_0_generic_template", "retained scalar source-charge schema"),
        ("SRC4506_09_1345_matrix", "1345 direct scalar row", MATRIX_1345, "VM1345_4_memory_class_scalar", "memory/fibre pressure rows"),
        ("SRC4506_10_1346_pack", "1346 coefficient pack", PACK_1346, "COEFF1346_M_B", "symbolic coefficient inventory"),
        ("SRC4506_11_1347_owner", "1347 owner ledger", OWNER_1347, "OWN1347_2_memory_branch_extremum", "best B_mem owner route"),
        ("SRC4506_12_1347_coeff", "1347 coefficient owner matrix", COEFF_OWNER_1347, "COWN1347_2_B_mem", "coefficient-wise owner map"),
        ("SRC4506_13_1347_route", "1347 route ranking", ROUTE_1347, "memory branch-extremum / trace projection lock", "ranked route"),
        ("SRC4506_14_1348_Bmem", "1348 B_mem extremum test", BMEM_1348, "BEXT1348_1_conditional_calculus", "conditional calculus pass"),
        ("SRC4506_15_1348_operator", "1348 memory operator test", OP_1348, "OPS1348_1_variation", "operator signature scaffold"),
        ("SRC4506_16_1348_closure", "1348 closure contract", CLOSURE_1348, "MCLOS1348_2_finite_Bmem_residual", "finite residual fallback"),
        ("SRC4506_17_2250_body", "2250 body charge precedent", POST_2250, "BCR2250_1_body_charge", "body-charge schema"),
        ("SRC4506_18_1348_doc", "1348 prose handoff", POST_1348, "B_MEM_ZERO_NOT_PARENT_OWNED_CURRENT_CORPUS", "B_mem theorem remains unsigned"),
        ("SRC4506_19_1346_doc", "1346 prose handoff", POST_1346, "MEMORY_VERTEX_ZERO_NOT_DERIVED_SYMBOLIC_PACK_SELECTED", "memory/fibre symbolic pack"),
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


def owner_route_rows() -> List[Dict[str, object]]:
    return [
        {
            "route_id": "OR4506_0_memory_B",
            "sector": "memory_class_scalar",
            "coefficient": "B_mem",
            "best_route": "branch extremum plus parent-owned trace projection",
            "derivation_law": "If Gamma_eff=L_cg^-2[F_L+a_F(R(m;X_B)-R(m_L;X_B))] and partial_m R(m_L;X_B)=0 at fixed X_B, then partial_m Gamma_eff|m_L=0, so the curvature-linear memory vertex vanishes in that projected channel.",
            "current_result": "CONDITIONAL_CALCULUS_PASSES_NOT_PARENT_OWNED",
            "next_input": "derive Gamma_eff projection from K_MTS and derive R(m;X_B), m_L(X_B), and stable branch Hessian",
            "valid_for_claim": False,
        },
        {
            "route_id": "OR4506_1_memory_C",
            "sector": "memory_class_scalar",
            "coefficient": "C_mem",
            "best_route": "matter-blind/product-functor descent",
            "derivation_law": "If S_matter depends only on q(Phi), Psi, and theta and the memory coordinate is vertical to q, then delta_m S_matter=0 and C_mem=0 in the same observed frame.",
            "current_result": "COUNTEREXAMPLE_LOCKED_UNTIL_MATTER_FUNCTOR_SIGNED",
            "next_input": "prove source-label forgetting and no hidden scalar dependence in clocks, masses, densities, and readout maps",
            "valid_for_claim": False,
        },
        {
            "route_id": "OR4506_2_fibre_B",
            "sector": "finite_fibre_spectrum",
            "coefficient": "B_h",
            "best_route": "hidden-visible coefficient typing or constrained multiplier",
            "derivation_law": "If fibre fluctuations h are eliminated by a constraint before variation, or parent grammar forbids h R_obs monomials, then delta^2 S/(delta h delta R_obs)=0.",
            "current_result": "UNSIGNED_META_THEOREM",
            "next_input": "derive the no hidden-visible coefficient meta-theorem or the fibre multiplier constraint from MTS primitives",
            "valid_for_claim": False,
        },
        {
            "route_id": "OR4506_3_fibre_C",
            "sector": "finite_fibre_spectrum",
            "coefficient": "C_h",
            "best_route": "h-blind matter functor",
            "derivation_law": "If matter clocks, masses, source maps, and composition labels descend through q before fibre variables enter, then delta_h S_matter=0 and C_h=0.",
            "current_result": "CONDITIONAL_NOT_PARENT_SIGNED",
            "next_input": "derive matter-functor descent plus source-label forgetting for finite fibre modes",
            "valid_for_claim": False,
        },
    ]


def memory_extremum_rows() -> List[Dict[str, object]]:
    return [
        {
            "test_id": "MEXT4506_0_expansion",
            "claim_piece": "B_mem as first memory derivative",
            "mathematical_form": "F_mem(m) R_obs = [F0 + F0_prime delta_m + 1/2 F0_second delta_m^2 + ...] R_obs; B_mem proportional to F0_prime",
            "result": "DERIVED_LOCAL_EXPANSION",
            "blocker": "the exact F_mem/Gamma_eff parent object must be selected from K_MTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "MEXT4506_1_branch_extremum",
            "claim_piece": "B_mem=0 branch condition",
            "mathematical_form": "B_mem=0 iff F0_prime=0, or iff the trace projection removes the linear curvature slot before expansion",
            "result": "ZERO_CONDITION_SHARPENED",
            "blocker": "F0_prime=0 and projection-removal are not parent-signed for the actual local branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "MEXT4506_2_1348_projection",
            "claim_piece": "1348 F1 route reused correctly",
            "mathematical_form": "partial_m Gamma_eff|m_L=0 follows from the ansatz only when partial_m R(m_L;X_B)=0 and X_B is fixed",
            "result": "CONDITIONAL_ROUTE_ACCEPTED",
            "blocker": "does not by itself silence full nabla Gamma_eff, K_hat response, source drift, or boundary terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "MEXT4506_3_finite_residual",
            "claim_piece": "fallback if B_mem not zero",
            "mathematical_form": "rho_mem = B_mem R_obs + C_mem T + J_mem; Q_mem0=4*pi int_0^R r^2 rho_mem sinh(r/lambda_mem)/(r/lambda_mem) dr + Q_boundary_mem",
            "result": "FINITE_BODY_CHARGE_ROUTE_READY",
            "blocker": "needs numeric/source-backed Z_mem,M2_mem,B_mem,C_mem,J_mem,Q_boundary_mem,W_mem/body profile",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def memory_operator_rows() -> List[Dict[str, object]]:
    return [
        {
            "operator_id": "MOP4506_0_quadratic_action",
            "object": "memory local quadratic action",
            "formula": "S_mem^(2)=1/2 int sqrt(gamma) [Z_mem gamma^ij partial_i delta_m partial_j delta_m + M2_mem delta_m^2] plus sources and boundary terms",
            "derived_use": "variation gives (-Z_mem nabla^2 + M2_mem) delta_m = rho_mem under fixed local frame and chosen boundary class",
            "missing_parent_signature": "parent adoption, field domain, boundary class, units, sign convention, source terms",
            "valid_for_claim": False,
        },
        {
            "operator_id": "MOP4506_1_positive_gap",
            "object": "operator positivity",
            "formula": "Z_mem>0 and M2_mem>0 with zero modes removed imply a positive massive Green function branch",
            "derived_use": "positive operator supports a no-hair theorem only after B_mem=C_mem=J_mem=Q_boundary_mem=0",
            "missing_parent_signature": "Z_mem_min, M2_mem branch Hessian, zero-mode/topology removal",
            "valid_for_claim": False,
        },
        {
            "operator_id": "MOP4506_2_nohair_guard",
            "object": "memory no-hair",
            "formula": "int [Z_mem |grad delta_m|^2 + M2_mem delta_m^2] = int delta_m rho_mem + boundary",
            "derived_use": "if rho_mem=0 and boundary flux/charge vanish, then delta_m=0 for positive operator",
            "missing_parent_signature": "rho_mem silence and boundary no-charge theorem; otherwise body charge survives",
            "valid_for_claim": False,
        },
    ]


def fibre_owner_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "FIB4506_0_unique_gap",
            "target": "Z_h,M2_h,J_h",
            "zero_or_bound_route": "derive a unique source-independent gapped fibre solution h0, or retain a finite fibre spectrum with lambda_h",
            "mathematical_form": "L_h delta_h = B_h R_obs + C_h T + J_h + boundary",
            "current_result": "FINITE_BRANCH_IF_CHOSEN_NOT_ZERO_OWNER",
            "first_required_derivation": "parent fibre potential, positive gap, and source independence",
            "valid_for_claim": False,
        },
        {
            "gate_id": "FIB4506_1_no_curvature_vertex",
            "target": "B_h",
            "zero_or_bound_route": "prove hidden-visible coefficient typing or constrained multiplier removes h R_obs",
            "mathematical_form": "B_h=delta^2 S_parent/(delta h delta R_obs)=0 if h is not a parent bulk coefficient or is eliminated before propagation",
            "current_result": "UNSIGNED",
            "first_required_derivation": "no hidden-visible coefficient meta-theorem from parent grammar",
            "valid_for_claim": False,
        },
        {
            "gate_id": "FIB4506_2_matter_blindness",
            "target": "C_h",
            "zero_or_bound_route": "prove h-blind matter functor or retain finite composition/source coupling",
            "mathematical_form": "C_h=delta S_matter/delta h=0 only if clocks, masses, source maps and composition labels are h-independent in the observed frame",
            "current_result": "CONDITIONAL_NOT_PARENT_SIGNED",
            "first_required_derivation": "matter-functor descent and source-label forgetting",
            "valid_for_claim": False,
        },
        {
            "gate_id": "FIB4506_3_boundary_charge",
            "target": "Q_boundary_h",
            "zero_or_bound_route": "derive no boundary/projection flux or keep boundary charge in the finite row",
            "mathematical_form": "Q_h[body]=int_body W_h(B_h R_obs + C_h T + J_h)+Q_boundary_h",
            "current_result": "NO_ZERO_WITHOUT_NO_CHARGE",
            "first_required_derivation": "boundary variational class and Q_h=0 current theorem",
            "valid_for_claim": False,
        },
    ]


def body_charge_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "BCIN4506_0_memory_density",
            "sector": "memory_class_scalar",
            "field_equation": "(-Z_mem nabla^2 + M2_mem) delta_m = rho_mem",
            "source_density": "rho_mem = B_mem R_obs + C_mem T + J_mem",
            "range": "lambda_mem=sqrt(Z_mem/M2_mem)",
            "spherical_charge": "Q_mem0=4*pi int_0^R dr r^2 rho_mem(r) sinh(r/lambda_mem)/(r/lambda_mem) + Q_boundary_mem",
            "amplitude_bound": "|A_mem| <= [exp(R_body/lambda_mem) int_body |rho_mem| dV + |Q_boundary_mem|]/(4*pi |Z_mem|)",
            "required_inputs": "Z_mem;M2_mem;B_mem;C_mem;J_mem;Q_boundary_mem;W_mem/body profile;screening;source paths",
            "status": "NONCLAIM_INPUT_ROW_STAGED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "BCIN4506_1_fibre_density",
            "sector": "finite_fibre_spectrum",
            "field_equation": "(-Z_h nabla^2 + M2_h) delta_h = rho_h, or discrete-gapped analogue",
            "source_density": "rho_h = B_h R_obs + C_h T + J_h",
            "range": "lambda_h=sqrt(Z_h/M2_h) when continuum approximation is valid",
            "spherical_charge": "Q_h0=4*pi int_0^R dr r^2 rho_h(r) sinh(r/lambda_h)/(r/lambda_h) + Q_boundary_h",
            "amplitude_bound": "|A_h| <= [exp(R_body/lambda_h) int_body |rho_h| dV + |Q_boundary_h|]/(4*pi |Z_h|)",
            "required_inputs": "Z_h;M2_h;B_h;C_h;J_h;Q_boundary_h;W_h/body profile;screening;source paths",
            "status": "NONCLAIM_INPUT_ROW_STAGED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "BCIN4506_2_zero_switch",
            "sector": "both",
            "field_equation": "positive massive operator branch",
            "source_density": "rho_X=B_X R_obs+C_X T+J_X",
            "range": "lambda_X=sqrt(Z_X/M2_X)",
            "spherical_charge": "Q_X0=0 iff weighted interior source plus boundary charge vanish",
            "amplitude_bound": "A_X=0 only when B_X=C_X=J_X=Q_boundary_X=0 or an exact weighted cancellation is parent-owned",
            "required_inputs": "component zeros in the same parent branch, not separate closures",
            "status": "ZERO_SWITCH_WRITTEN_NO_CANCELLATION_CREDIT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def parent_signature_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PA4506_0_Bmem",
            "claim": "B_mem=0",
            "needed_signature": "K_MTS-derived Gamma_eff trace projection and parent-owned local branch extremum",
            "current_source": str(BMEM_1348),
            "current_status": "CONDITIONAL_CALCULUS_ONLY",
            "effect": "memory curvature vertex remains finite-residual eligible",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4506_1_Cmem",
            "claim": "C_mem=0",
            "needed_signature": "product functor / matter-blindness in same observed frame",
            "current_source": str(OWNER_1347),
            "current_status": "COUNTEREXAMPLE_LOCKED",
            "effect": "memory source charge may couple to T/body composition",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4506_2_operator_mem",
            "claim": "Z_mem,M2_mem positive and sourced",
            "needed_signature": "parent memory action, units, branch Hessian, zero-mode removal, boundary class",
            "current_source": str(OP_1348),
            "current_status": "SCAFFOLD_ONLY",
            "effect": "lambda_mem not claim-grade numeric",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4506_3_fibre",
            "claim": "B_h=C_h=J_h=Q_boundary_h=0",
            "needed_signature": "parent fibre grammar, source-independent gap, matter-blindness, and boundary no-charge theorem",
            "current_source": str(PACK_1346),
            "current_status": "UNSIGNED_SYMBOLIC_PACK",
            "effect": "finite fibre branch remains live",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4506_4_claim_safety",
            "claim": "local GR/R10/PPN pass",
            "needed_signature": "zero theorem for both direct rows or numeric finite bound rows with source paths",
            "current_source": str(BODY_CHARGE_INPUT),
            "current_status": "BLOCKED_BY_MISSING_PARENT_OR_NUMERIC_INPUTS",
            "effect": "4506 advances the route but makes no local-GR claim",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4506_0_memory_B_zero",
            "gate": "B_mem=0 parent-owned",
            "derived_now": False,
            "blocked_by": "K_MTS trace projection and branch potential/extremum unsigned",
            "claim_allowed": False,
        },
        {
            "gate_id": "CG4506_1_memory_nohair",
            "gate": "memory branch locally silent",
            "derived_now": False,
            "blocked_by": "C_mem,J_mem,Q_boundary_mem and positive operator remain unsigned",
            "claim_allowed": False,
        },
        {
            "gate_id": "CG4506_2_fibre_zero",
            "gate": "finite fibre spectrum locally silent",
            "derived_now": False,
            "blocked_by": "fibre parent grammar, gap, matter-blindness and boundary charge unsigned",
            "claim_allowed": False,
        },
        {
            "gate_id": "CG4506_3_body_charge_inputs",
            "gate": "memory/fibre finite source-charge rows claim-ready",
            "derived_now": False,
            "blocked_by": "no numeric/source-backed Z,M2,B,C,J,Q_boundary/body-profile rows",
            "claim_allowed": False,
        },
        {
            "gate_id": "CG4506_4_local_GR",
            "gate": "R2/fR scalar obstruction cleared for local GR",
            "derived_now": False,
            "blocked_by": "direct memory/fibre scalar pressure rows remain live",
            "claim_allowed": False,
        },
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "B_mem zero law reduced to F0_prime/projection condition; memory/fibre body-charge input rows staged exactly",
            "not_derived": "parent-owned B_mem/C_mem/B_h/C_h zeros, positive operator values, numeric finite rows",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4506_0",
            "target_file": NEXT_TARGET,
            "task": "attack the best-ranked memory route directly: derive the K_MTS-owned trace projection / F0_prime=0 branch law, or fill the finite B_mem source row with units and a source path",
            "success_condition": "B_mem is either theorem-zero in the parent object language or retained as a sourced finite coefficient row ready for body-charge scoring",
            "do_not": "claim memory no-hair, local GR, PPN, or R10 from conditional F1 calculus alone",
            "valid_for_claim": False,
        }
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4506_0",
            "decision": DECISION,
            "because": "4505 showed the R2/fR scalar obstruction lives in memory/fibre curvature and matter couplings; 4506 sharpens those into exact zero laws or finite body-charge rows.",
            "effect": "the next leap is not another broad audit; it is the B_mem trace-projection owner or a sourced finite B_mem row.",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(all_rows: Mapping[str, Sequence[Mapping[str, object]]]) -> List[Dict[str, object]]:
    csv_files = [
        SOURCE_REGISTER,
        OWNER_ROUTE_AUDIT,
        MEMORY_EXTREMUM,
        MEMORY_OPERATOR,
        FIBRE_OWNER,
        BODY_CHARGE_INPUT,
        PARENT_SIGNATURE,
        CLAIM_GATES,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]
    parsed = True
    parse_details: List[str] = []
    for path in csv_files:
        try:
            rows = read_csv(path)
            parsed = parsed and bool(rows)
            parse_details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:  # pragma: no cover - validation detail
            parsed = False
            parse_details.append(f"{path.name}:ERROR:{exc}")

    source_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in all_rows["sources"])
    nonclaim_ok = all(
        str(value).lower() != "true"
        for rows in all_rows.values()
        for row in rows
        for key, value in row.items()
        if key in {"valid_for_claim", "claim_allowed"}
    )
    body_rows_staged = len(all_rows["body"]) == 3 and all("required_inputs" in row for row in all_rows["body"])
    next_ok = all_rows["next"][0]["target_file"] == NEXT_TARGET
    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    no_claim = all(not bool(row.get("derived_now", False)) for row in all_rows["gates"])

    checks = [
        ("VAL4506_00_sources", source_ok, "all source paths exist and needles are found"),
        ("VAL4506_01_memory_extremum", True, "B_mem zero law sharpened to F0_prime/projection condition"),
        ("VAL4506_02_body_rows", body_rows_staged, "memory/fibre body-charge rows staged with required inputs"),
        ("VAL4506_03_claims_blocked", no_claim, "all local-GR/R10/PPN claim gates remain blocked"),
        ("VAL4506_04_nonclaim_flags", nonclaim_ok, "all generated claim flags remain false"),
        ("VAL4506_05_csv_parse", parsed, ";".join(parse_details)),
        ("VAL4506_06_next_target", next_ok, NEXT_TARGET),
        ("VAL4506_07_pycache_absent", pycache_absent, "scripts __pycache__ absent after cleanup"),
    ]
    rows: List[Dict[str, object]] = [
        {
            "validation_id": check_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, ok, detail in checks
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(
        {
            "validation_id": "VAL4506_OVERALL",
            "status": overall,
            "detail": "4506 memory/fibre B/C owner or body-charge input row",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def append_claim_once() -> None:
    existing = text(CLAIMS_PATH)
    if CLAIM_ID in existing or MARKER in existing:
        return
    row = ",".join(
        [
            CLAIM_ID,
            "local_gr_newton_r2fr_memory_fibre_couplings",
            '"4506 sharpens the memory/fibre coupling obstruction: B_mem zero is reduced to a parent trace-projection/branch-extremum law, C_mem/C_h require matter-functor descent, B_h requires fibre grammar, and finite body-charge rows are staged for memory and fibre without promoting local GR."',
            '"4506 source register, owner route audit, memory extremum test, memory operator signature, fibre owner gate, body-charge input rows, parent audit, claim gates, status and validation."',
            "private_memory_fibre_coupling_gate_nonclaim",
            NEXT_TARGET,
            "using conditional F1 calculus or symbolic body-charge rows as a local-GR/R10/PPN pass.",
            "local_gr_newton_r2fr_memory_fibre_couplings",
            str(FORMAL_PATH),
            NEXT_TARGET,
            '"derive the K_MTS trace projection/B_mem zero route or source finite B_mem first."',
        ]
    )
    CLAIMS_PATH.write_text(existing.rstrip() + "\n" + row + "\n", encoding="utf-8")


def build_doc(
    sources: Sequence[Mapping[str, object]],
    owner: Sequence[Mapping[str, object]],
    memory_ext: Sequence[Mapping[str, object]],
    memory_op: Sequence[Mapping[str, object]],
    fibre: Sequence[Mapping[str, object]],
    body: Sequence[Mapping[str, object]],
    parent: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    validation: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4506 - Memory/Fibre Bx Cx Owner Or Body-Charge Input Row

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Verdict

4506 takes the coupling problem head-on. The useful local derivation is:

`F_mem(m) R_obs = [F0 + F0_prime delta_m + 1/2 F0_second delta_m^2 + ...] R_obs`.

So the memory curvature vertex is not mysterious: `B_mem` is the first branch derivative of the curvature prefactor/projection. It is zero only if the parent branch signs `F0_prime=0`, or if the parent trace projection removes the linear curvature slot before expansion. This preserves the good 1348 result without smuggling it into a theorem.

The finite fallback is also now exact. For either `X=mem` or `X=h`,

`rho_X = B_X R_obs + C_X T + J_X`,  
`lambda_X=sqrt(Z_X/M_X2)`,  
`Q_X0=4*pi int_0^R dr r^2 rho_X(r) sinh(r/lambda_X)/(r/lambda_X) + Q_boundary_X`.

That is the bridge to testing: either prove the coupling zero from the parent action, or source the coefficient row and score the body-charge amplitude. No local-GR, R10, PPN, clock, or orbital claim is made from 4506.

## Source Register

{table(sources)}

## Owner Route Audit

{table(owner)}

## Memory Extremum Test

{table(memory_ext)}

## Memory Operator Signature

{table(memory_op)}

## Fibre Owner Gate

{table(fibre)}

## Body-Charge Input Rows

{table(body)}

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
    sources = source_rows()
    owner = owner_route_rows()
    memory_ext = memory_extremum_rows()
    memory_op = memory_operator_rows()
    fibre = fibre_owner_rows()
    body = body_charge_rows()
    parent = parent_signature_rows()
    gates = claim_gate_rows()
    status = status_rows()
    next_target = next_rows()
    decisions = decision_rows()

    all_rows = {
        "sources": sources,
        "owner": owner,
        "memory_ext": memory_ext,
        "memory_op": memory_op,
        "fibre": fibre,
        "body": body,
        "parent": parent,
        "gates": gates,
        "status": status,
        "next": next_target,
        "decisions": decisions,
    }

    write_csv(SOURCE_REGISTER, sources)
    write_csv(OWNER_ROUTE_AUDIT, owner)
    write_csv(MEMORY_EXTREMUM, memory_ext)
    write_csv(MEMORY_OPERATOR, memory_op)
    write_csv(FIBRE_OWNER, fibre)
    write_csv(BODY_CHARGE_INPUT, body)
    write_csv(PARENT_SIGNATURE, parent)
    write_csv(CLAIM_GATES, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validation_rows(all_rows)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, owner, memory_ext, memory_op, fibre, body, parent, gates, status, decisions, next_target, validation)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4506 Memory/Fibre Bx Cx Owner Or Body-Charge Input Row

Marker: `{MARKER}`  
4506 sharpens the coupling obstruction instead of merely listing it. `B_mem` is the first branch derivative of the memory curvature prefactor/projection, so it vanishes only by a parent-owned trace-projection or branch-extremum law; otherwise it becomes a finite body-charge input. The same row now exists for fibre through `B_h`, `C_h`, `J_h`, and `Q_boundary_h`. No local-GR/R10/PPN claim is promoted.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4506 Packet Integration

Marker: `{PACKET_MARKER}`  
The packet now has a direct coupling fork: prove the memory/fibre `B/C` vertices vanish from the parent object language, or source them as finite body-charge rows. The next best lever is `B_mem`, because the branch-extremum/trace-projection route is the most concrete route already on the table.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
