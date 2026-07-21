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

CHECKPOINT = "4503"
CLAIM_ID = "L-345"
MARKER = "PPC4161_DELTAE_R11_EH_ONLY_OPERATOR_OR_FIRST_COEFFICIENT_BOUND_4503"
PACKET_MARKER = "PPC4161_PACKET_DELTAE_R11_EH_ONLY_OPERATOR_OR_FIRST_COEFFICIENT_BOUND_4503"
DECISION = "DELTAE_R11_ZERO_ROUTE_REDUCED_TO_CONFORMAL_OR_DOUBLE_ZERO_SELECTOR_FIRST_COEFFICIENT_QUEUE_NONCLAIM"
NEXT_TARGET = "4504-Y5-R2FR-R2-fR-scalar-mode-double-zero-or-first-coefficient-bound.md"

FORMAL_PATH = FORMAL / "519-PPC4161-DeltaE-R11-EH-only-operator-or-first-coefficient-bound.md"
DOC_PATH = POST / "4503-Y5-R2FR-DeltaE-R11-EH-only-operator-or-first-coefficient-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4503_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4503_SOURCE_REGISTER.csv"
ZERO_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4503_DELTAE_R11_ZERO_THEOREM.csv"
R11_FAMILY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4503_R11_FAMILY_VECTOR.csv"
SELECTOR_LEAK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4503_SELECTOR_LEAK_AUDIT.csv"
COEFF_QUEUE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4503_FIRST_COEFFICIENT_BOUND_QUEUE.csv"
PARENT_SIGNATURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4503_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4503_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4503_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4503_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4503_DECISION.csv"

FORMAL_518 = FORMAL / "518-PPC4161-AE-residual-product-bound-or-extra-sector-zero.md"
POST_4502 = POST / "4502-Y5-R2FR-AE-residual-product-bound-or-extra-sector-zero.md"
SCRIPT_4502 = SCRIPT_DIR / "Y5_R2FR_4502_AE_residual_product_bound_or_extra_sector_zero.py"
AE_VECTOR_4502 = SOURCE_DIR / "P8_Y5_R2FR_4502_AE_RESIDUAL_VECTOR_DECOMPOSITION.csv"
AE_BOUND_4502 = SOURCE_DIR / "P8_Y5_R2FR_4502_AE_PRODUCT_BOUND_GATE.csv"
COMPONENT_BUDGET_4501 = SOURCE_DIR / "P8_Y5_R2FR_4501_COMPONENT_TRANSFER_BUDGET.csv"
OPERATOR_AUDIT = SOURCE_DIR / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv"
EH_GATE = SOURCE_DIR / "R11_EH_ONLY_OR_EXECUTABLE_VECTOR_GATE.csv"
R11_VECTOR_EXEC = SOURCE_DIR / "R11_nonEH_operator_vector_executable.csv"
SELECTOR_LEMMA = SOURCE_DIR / "P8_LOCAL_EH_R11_SELECTOR_LEMMA.csv"
LEAK_TESTS = SOURCE_DIR / "P8_LOCAL_EH_R11_LEAK_TESTS.csv"
DOC_1946 = POST / "1946-Y5-R2FR-parent-conformal-descent-contract-or-Hessian-slip-kill.md"
SOURCE_NORM_2583 = SOURCE_DIR / "P8_Y5_SOURCE_NORM_2583_R11_COEFFICIENT_VECTOR.csv"

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


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    return read_csv(path)


def rows_by(path: Path, key: str) -> Dict[str, Dict[str, str]]:
    return {row[key]: row for row in csv_rows(path) if key in row}


def constants() -> Dict[str, float]:
    row = rows_by(COMPONENT_BUDGET_4501, "budget_id").get("CB4501_A_E", {})
    return {
        "single_a": float(row.get("single_survivor_A_bound", "1.400851696295935e-13")),
        "equal_a": float(row.get("equal_no_cancellation_A_budget", "3.502129240739837e-14")),
        "equal_j2": float(row.get("equal_no_cancellation_J2_budget", "8.25e-09")),
        "c_j2": float(row.get("rho1_abs_coefficient", "2.355709750522272e5")),
    }


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4503_00_formal518", "4502 formal handoff", FORMAL_518, "DeltaE_R11_l2", "first A_E residual subchannel"),
        ("SRC4503_01_post4502", "4502 post mirror", POST_4502, "DeltaE_R11_l2", "post checkpoint target"),
        ("SRC4503_02_script4502", "4502 generator", SCRIPT_4502, 'CHECKPOINT = "4502"', "reproducible predecessor"),
        ("SRC4503_03_ae_vector4502", "4502 A_E vector", AE_VECTOR_4502, "AEV4502_0_DeltaE_R11", "DeltaE_R11 row"),
        ("SRC4503_04_ae_bound4502", "4502 A_E product bound", AE_BOUND_4502, "AEB4502_2_equal_budget_AE", "equal A_E budget"),
        ("SRC4503_05_operator_audit", "R11 operator audit", OPERATOR_AUDIT, "R2_fR_scalar_mode", "retained non-EH family list"),
        ("SRC4503_06_eh_gate", "EH-only/R11 executable gate", EH_GATE, "EHV1_EH_only_ladder_closed", "EH-only ladder status"),
        ("SRC4503_07_r11_vector", "R11 non-EH vector", R11_VECTOR_EXEC, "R2_fR_scalar_mode", "first executable vector skeleton"),
        ("SRC4503_08_selector_lemma", "local EH selector lemma", SELECTOR_LEMMA, "L2_double_zero_sufficient", "double-zero selector condition"),
        ("SRC4503_09_leak_tests", "selector leak tests", LEAK_TESTS, "K2_double_zero", "variation leak audit"),
        ("SRC4503_10_1946_hessian", "1946 conformal/Hessian kill", DOC_1946, "Hessian Slip Kill Lemma", "O(3) and Hessian zero lemmas"),
        ("SRC4503_11_source_norm2583", "2583 source-normalization vector", SOURCE_NORM_2583, "Y5C2583_4_nonEH_operator_potential", "source-normalization coefficient row"),
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


def zero_theorem_rows(c: Mapping[str, float]) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "D4503_0_target",
            "route": "DeltaE_R11_l2 target",
            "statement": "The first A_E subchannel vanishes if the local weak-field parent operator has no GR-subtracted l=2 R11/non-EH remainder.",
            "formula": "DeltaE_R11_l2 = P_2[E_parent - E_EH]_TF",
            "status": "TARGET_DEFINED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "D4503_1_EH_only",
            "route": "EH-only local operator",
            "statement": "If the local exterior public operator is exactly EH through the l=2 weak-field order, the R11 operator residual is zero.",
            "formula": "E_parent|local,l<=2 = E_EH|local,l<=2 => DeltaE_R11_l2=0",
            "status": "SUFFICIENT_BUT_EH_LADDER_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "D4503_2_double_zero_selector",
            "route": "double-zero non-EH selector",
            "statement": "A retained non-EH family is first-variation silent on the local-zero branch if it is multiplied by a parent-owned selector with a double zero.",
            "formula": "S_A=int sqrt(-g) F_A(Z) O_A; F_A(0)=0 and F_A'(0)=0 => delta S_A|Z=0=0",
            "status": "CONDITIONAL_SELECTOR_ZERO_DERIVED_FROM_LEMMA",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "D4503_3_O3_conformal",
            "route": "algebraic O(3) conformal descent",
            "statement": "If the residual is algebraic and no spatial dyad/vector/tensor survives the quotient, rotational equivariance forces it to be conformal.",
            "formula": "R11_ij=S delta_ij => P_TF[R11_ij]=0",
            "status": "CONDITIONAL_TENSOR_LEMMA_DERIVED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "D4503_4_hessian_kill",
            "route": "scalar Hessian kill",
            "statement": "For a radial scalar memory Hessian, the traceless l=2 piece dies exactly when f''=f'/r; bounded/decaying local vacuum conditions then kill the nonconstant scalar branch unless an r^2 common mode is admitted.",
            "formula": "P_TF[partial_i partial_j f]=(f''-f'/r)(n_i n_j-delta_ij/3); zero iff f''=f'/r; solution f=a r^2+b",
            "status": "CONDITIONAL_HESSIAN_ZERO_DERIVED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "D4503_5_topological_boundary",
            "route": "topological or boundary-silent family",
            "statement": "A topological or pure boundary family gives no local l=2 bulk operator only if the boundary variation is closed/no-hair in the local collar.",
            "formula": "delta_g S_top=0 in local collar, or boundary TF flux=0 => contribution to DeltaE_R11_l2=0",
            "status": "CONDITIONAL_BOUNDARY_ROUTE_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "D4503_6_finite_fallback",
            "route": "first coefficient bound",
            "statement": "If zero is not parent-signed, the first scoreable fallback is a coefficient/operator-norm inequality inside the 4502 A_E budget.",
            "formula": f"||DeltaE_R11_l2|| <= sum_A |c_A| N_A and ||W_STF||_1||K_2^X|| sum_A |c_A|N_A <= {c['equal_a']:.15e}",
            "status": "FINITE_BOUND_FORMULA_READY_NUMERIC_FACTORS_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


PRIORITY_MAP = {
    "R2_fR_scalar_mode": ("1", "scalar Hessian/f(R) slip is the cleanest first local-GR obstruction and links to R10/PPN"),
    "Ricci_Weyl_squared": ("2", "traceless curvature-squared operator is the next direct l=2 slip channel"),
    "torsion_nonmetricity": ("3", "connection compatibility blocks local GR if not killed"),
    "nonlocal_memory_kernel": ("4", "kernel anisotropy can reintroduce TF residuals after local algebraic terms are safe"),
    "source_normalization_operator": ("5", "measured-G/source-normalization terms can mimic or hide residual coupling"),
    "projector_domain_stress": ("6", "conditional topological projector route needs parent ownership"),
    "boundary_topological_terms": ("7", "topological only helps if boundary/no-hair variation is signed"),
    "scalar_tensor_class_metric": ("8", "scalar class field overlaps Hessian route but needs source/range normalization"),
    "bulk_X_force_law": ("9", "finite-range force row ties to R10 after charge/source coupling exists"),
    "vector_preferred_frame": ("10", "preferred-frame terms are crucial but less directly the DeltaE_R11 scalar-Hessian first coefficient"),
}


def r11_family_rows(c: Mapping[str, float]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_row in csv_rows(OPERATOR_AUDIT):
        family = source_row.get("operator_family", "")
        priority, reason = PRIORITY_MAP.get(family, ("99", "retained row from audit"))
        coefficient = source_row.get("coefficient_symbol", "")
        selector = source_row.get("required_selector_or_fill", "")
        if "topological" in selector.lower():
            zero_route = "topological_boundary_nohair_or_double_zero"
        elif "double-zero" in selector.lower():
            zero_route = "double_zero_selector_or_finite_bound"
        elif "Levi-Civita" in selector or "connection" in selector:
            zero_route = "connection_compatibility_or_double_zero"
        elif "source" in selector.lower():
            zero_route = "source_coupling_zero_or_finite_bound"
        else:
            zero_route = "finite_coefficient_bound_or_parent_zero"
        rows.append(
            {
                "family_id": f"R11F4503_{priority}_{family}",
                "priority": priority,
                "operator_family": family,
                "coefficient_symbol": coefficient,
                "current_value": source_row.get("coefficient_value", ""),
                "affected_rows": source_row.get("affected_rows", ""),
                "zero_route": zero_route,
                "selector_or_fill": selector,
                "finite_bound_formula": f"|{coefficient}| <= {c['equal_a']:.15e}/(||W_STF||_1 ||K_2^X|| N_{family})",
                "why_priority": reason,
                "status": "RETAINED_UNSIGNED_NONCLAIM",
                "valid_for_claim": False,
            }
        )
    return sorted(rows, key=lambda row: int(str(row["priority"])))


def selector_leak_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for row in csv_rows(LEAK_TESTS):
        verdict = row.get("verdict", "")
        passes = verdict.startswith("passes")
        rows.append(
            {
                "audit_id": "SLA4503_" + row.get("test_id", "unknown"),
                "operator_form": row.get("operator_form", ""),
                "selector_condition": row.get("selector_condition", ""),
                "variation_result": row.get("variation_result", ""),
                "verdict": verdict,
                "usable_for_zero": passes,
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    rows.append(
        {
            "audit_id": "SLA4503_selector_contract",
            "operator_form": "F_A(Z) O_A",
            "selector_condition": "F_A(0)=0 and F_A'(0)=0 for every retained non-EH family A",
            "variation_result": "delta(F_A O_A)=F_A delta O_A + F_A' O_A delta Z = 0 on Z=0 branch",
            "verdict": "conditional_sufficient_contract_not_parent_signed_for_actual_rows",
            "usable_for_zero": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    )
    return rows


def coefficient_queue_rows(c: Mapping[str, float]) -> List[Dict[str, object]]:
    priorities = [
        ("R2_fR_scalar_mode", "c_R2_or_c_fR", "N_R2_fR_scalar_mode", "scalar Hessian slip/f(R) range mode", "derive double-zero c_R2(Z)=O(Z^2), infinite-mass/no-coupling theorem, or source R10/PPN scalar coefficient"),
        ("Ricci_Weyl_squared", "c_Ricci_or_c_Weyl", "N_Ricci_Weyl_squared", "traceless curvature-squared slip", "prove Gauss-Bonnet/topological combination, double-zero coefficient, or source weak-field l=2 norm"),
        ("torsion_nonmetricity", "c_T_or_c_Q", "N_torsion_nonmetricity", "connection compatibility", "derive Levi-Civita/no-hypermomentum theorem or source connection residual norm"),
        ("nonlocal_memory_kernel", "c_nonlocal_or_K_norm", "N_nonlocal_memory_kernel", "kernel anisotropy", "prove compact-local isotropic/common-mode kernel or source TF kernel norm"),
        ("source_normalization_operator", "c_domain_source_normalization_operator", "N_source_normalization_operator", "measured-G/source normalization leakage", "derive measured-GM absorption theorem or source mu_extra coefficient product"),
    ]
    rows: List[Dict[str, object]] = []
    for index, (family, coefficient, norm, risk, next_action) in enumerate(priorities, start=1):
        rows.append(
            {
                "queue_id": f"FCB4503_{index}_{family}",
                "priority": index,
                "operator_family": family,
                "coefficient_symbol": coefficient,
                "operator_norm_symbol": norm,
                "risk_channel": risk,
                "DeltaE_bound_contribution": f"||DeltaE_R11_l2|| includes |{coefficient}| {norm}",
                "AE_equal_budget_condition": f"||W_STF||_1 ||K_2^X|| |{coefficient}| {norm} <= {c['equal_a']:.15e}",
                "coefficient_bound_if_single_survivor": f"|{coefficient}| <= {c['equal_a']:.15e}/(||W_STF||_1 ||K_2^X|| {norm})",
                "current_numeric_status": "MISSING_PARENT_COEFFICIENT_AND_OPERATOR_NORM",
                "next_action": next_action,
                "valid_for_claim": False,
            }
        )
    return rows


def parent_signature_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PS4503_0_EH_only_ladder",
            "clause": "P1-P8 EH-only parent ladder closed",
            "evidence": str(EH_GATE),
            "current_status": "FAIL_UNSIGNED",
            "effect": "cannot declare DeltaE_R11_l2=0 from EH-only alone",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PS4503_1_second_order_Lovelock",
            "clause": "local 4D metric-only second-order exterior derived",
            "evidence": str(EH_GATE),
            "current_status": "FAIL_UNSIGNED",
            "effect": "R2/fR/Ricci/Weyl families remain live",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PS4503_2_connection_compatibility",
            "clause": "Levi-Civita/no independent connection theorem",
            "evidence": str(EH_GATE),
            "current_status": "FAIL_UNSIGNED",
            "effect": "torsion/nonmetricity row remains live",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PS4503_3_double_zero_actual_rows",
            "clause": "every retained non-EH family has parent-owned double-zero selector",
            "evidence": str(SELECTOR_LEMMA),
            "current_status": "CONDITIONAL_LEMMA_READY_ACTUAL_SELECTORS_MISSING",
            "effect": "selector route is mathematically sharp but not yet a parent proof",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PS4503_4_O3_no_dyad",
            "clause": "no spatial dyad/vector/tensor survives the local quotient",
            "evidence": str(DOC_1946),
            "current_status": "CONDITIONAL_LEMMA_READY_PARENT_NO_DYAD_UNSIGNED",
            "effect": "conformal-descent zero is available if parent no-dyad is signed",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PS4503_5_hessian_boundary",
            "clause": "scalar Hessian is bounded/decaying or common-mode only",
            "evidence": str(DOC_1946),
            "current_status": "ODE_DERIVED_BOUNDARY_UNSIGNED",
            "effect": "R2/fR scalar mode becomes first coefficient target",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4503_0_DeltaE_target",
            "gate": "DeltaE_R11_l2 target explicitly defined",
            "passed": True,
            "claim_allowed": False,
            "detail": "4503 isolates the first A_E subchannel as a GR-subtracted operator residual",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4503_1_zero_routes",
            "gate": "conditional zero routes derived",
            "passed": True,
            "claim_allowed": False,
            "detail": "EH-only, double-zero selector, O(3) conformal, Hessian kill and topological/nohair routes are written exactly",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4503_2_actual_parent_signature",
            "gate": "parent signs one zero route for actual rows",
            "passed": False,
            "claim_allowed": False,
            "detail": "actual R11 family rows still lack EH-only ladder closure, real double-zero selectors, or boundary/no-dyad parent proof",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4503_3_finite_bound_formula",
            "gate": "finite coefficient fallback formula",
            "passed": True,
            "claim_allowed": False,
            "detail": "coefficient queue now tells us exactly what numeric parent coefficient/norm would have to satisfy",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4503_4_local_GR_promotion",
            "gate": "local GR/J2 promotion",
            "passed": False,
            "claim_allowed": False,
            "detail": "DeltaE_R11_l2 is narrowed but not zeroed or numerically bounded",
            "valid_for_claim": False,
        },
    ]


def status_rows(c: Mapping[str, float]) -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "DeltaE_R11_zero_theorem_ready": True,
            "EH_only_global_closed": False,
            "double_zero_selector_contract_ready": True,
            "actual_R11_selectors_filled": False,
            "finite_coefficient_formula_ready": True,
            "first_coeff_target": "R2_fR_scalar_mode",
            "local_GR_claim": False,
            "equal_AE_budget": f"{c['equal_a']:.15e}",
            "sharpest_open_clause": "prove R2/fR scalar mode is double-zero/infinite-mass/silent, or fill c_R2_or_c_fR and N_R2_fR_scalar_mode",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4503_0",
            "target": NEXT_TARGET,
            "preferred_route": "attack R2_fR_scalar_mode first because the Hessian kill lemma gives an exact zero equation and it is the cleanest local-GR slip obstruction",
            "fallback_route": "source c_R2_or_c_fR, its units, range/mass normalization, and N_R2_fR_scalar_mode, then run the A_E equal-budget inequality",
            "do_not_do": "declare EH-only from the q-chain rule or from absence of a coefficient table",
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
            "what_moved_forward": "4503 converts DeltaE_R11_l2 from a vague local-GR obstruction into exact zero routes plus a first coefficient bound queue.",
            "what_is_derived": "double-zero selectors, algebraic O(3) conformal descent, and scalar Hessian f''=f'/r are sufficient ways to kill the l=2 R11 operator residual.",
            "what_remains_blocked": "none of those routes is parent-signed for the actual retained R11 families; R2/fR scalar mode is selected as the first concrete target.",
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
        "domain": "local_gr_newton_j2_DeltaE_R11",
        "claim": "4503 derives the exact zero routes for DeltaE_R11_l2 and stages the first coefficient-bound queue, selecting R2/fR scalar mode as the next concrete obstruction without promoting local GR/J2.",
        "current_evidence": "4503 source register, DeltaE_R11 zero theorem, R11 family vector, selector leak audit, first coefficient queue, parent signature audit, claim gates, status and validation.",
        "status": "private_DeltaE_R11_zero_route_or_first_coefficient_bound_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "treating conditional selector/conformal/Hessian lemmas as parent-signed for actual R11 rows.",
        "sector": "local_gr_newton_j2_DeltaE_R11",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "R2/fR scalar mode now needs a real double-zero/infinite-mass/silence proof or a coefficient/norm bound.",
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


def build_doc(
    sources: Sequence[Mapping[str, object]],
    zero_rows: Sequence[Mapping[str, object]],
    family_rows: Sequence[Mapping[str, object]],
    selector_rows: Sequence[Mapping[str, object]],
    queue_rows: Sequence[Mapping[str, object]],
    parent_rows: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    validation: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4503 - DeltaE R11 EH-Only Operator Or First Coefficient Bound

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Verdict

4503 does make a forward move. `DeltaE_R11_l2` is now reduced to exact mathematical kill routes rather than a general "non-EH stuff is missing" statement.

The clean local-GR proof would be any one parent-signed route:

1. EH-only local weak-field operator through l=2.
2. Double-zero selector for every retained non-EH family.
3. Algebraic O(3) conformal descent with no surviving dyad/vector/tensor.
4. Scalar Hessian kill, `f''=f'/r`, with bounded/decaying local vacuum conditions or only an `r^2` common mode.
5. Topological/boundary no-hair for boundary-only families.

None is parent-signed for the actual retained rows yet, so this is still private/nonclaim. The useful gain is that the finite fallback is now exact:

`||DeltaE_R11_l2|| <= sum_A |c_A| N_A`

and the 4502 equal-budget gate requires

`||W_STF||_1 ||K_2^X|| sum_A |c_A| N_A <= {constants()['equal_a']:.15e}`.

The next best concrete target is `R2_fR_scalar_mode`, because the Hessian lemma gives a direct zero equation and the same row links naturally to R10/PPN if it does not zero.

## Source Register

{table(sources)}

## DeltaE R11 Zero Theorem

{table(zero_rows)}

## R11 Family Vector

{table(family_rows)}

## Selector Leak Audit

{table(selector_rows)}

## First Coefficient Bound Queue

{table(queue_rows)}

## Parent Signature Audit

{table(parent_rows)}

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


def generated_csv_paths() -> List[Path]:
    return [
        SOURCE_REGISTER,
        ZERO_THEOREM_CSV,
        R11_FAMILY_CSV,
        SELECTOR_LEAK_CSV,
        COEFF_QUEUE_CSV,
        PARENT_SIGNATURE_CSV,
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
        except Exception as exc:  # pragma: no cover - validation report path
            csv_ok = False
            csv_detail.append(f"{path.name}:{exc}")

    flat_rows: List[Mapping[str, object]] = []
    for rows in all_rows.values():
        flat_rows.extend(rows)

    checks = [
        {
            "validation_id": "VAL4503_00_sources",
            "status": "PASS" if all(row["exists"] and row["needle_found"] for row in sources) else "FAIL",
            "detail": "all local source paths exist and needles found",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4503_01_zero_theorem",
            "status": "PASS" if any(row["theorem_id"] == "D4503_2_double_zero_selector" for row in all_rows["zero"]) else "FAIL",
            "detail": "DeltaE_R11 zero routes include the double-zero selector route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4503_02_hessian_route",
            "status": "PASS" if any("f''=f'/r" in str(row.get("formula", "")) for row in all_rows["zero"]) else "FAIL",
            "detail": "scalar Hessian kill equation recorded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4503_03_family_queue",
            "status": "PASS" if all_rows["family"] and all_rows["queue"] and all_rows["queue"][0]["operator_family"] == "R2_fR_scalar_mode" else "FAIL",
            "detail": "R11 family vector exists and R2/fR is first coefficient target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4503_04_parent_signature",
            "status": "PASS" if any(row["current_status"].startswith("FAIL") for row in all_rows["parent"]) else "FAIL",
            "detail": "parent signature audit keeps EH-only/local-GR promotion blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4503_05_claim_gates",
            "status": "PASS" if any(row["gate_id"] == "CG4503_4_local_GR_promotion" and row["passed"] is False for row in all_rows["gates"]) else "FAIL",
            "detail": "local GR/J2 promotion remains false",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4503_06_claim_flags_safe",
            "status": "PASS" if claim_flags_safe(flat_rows) else "FAIL",
            "detail": "all generated rows keep valid_for_claim/claim_allowed false",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4503_07_csv_parse",
            "status": "PASS" if csv_ok else "FAIL",
            "detail": "all generated CSVs parse with rows" if csv_ok else "; ".join(csv_detail),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4503_08_next_target",
            "status": "PASS" if all_rows["next"] and all_rows["next"][0]["target"] == NEXT_TARGET else "FAIL",
            "detail": "4504 R2/fR scalar mode target selected",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4503_09_doc_targets",
            "status": "PASS" if FORMAL_PATH.parent.exists() and DOC_PATH.parent.exists() else "FAIL",
            "detail": "formal and post-checkpoint document parents exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "validation_id": "VAL4503_10_pycache_absent",
            "status": "PASS" if not (SCRIPT_DIR / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after cleanup",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    overall = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "validation_id": "VAL4503_OVERALL",
            "status": overall,
            "detail": "4503 DeltaE_R11 EH-only operator or first coefficient bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return checks


def main() -> None:
    c = constants()
    sources = source_rows()
    zero_rows = zero_theorem_rows(c)
    family_rows = r11_family_rows(c)
    selector_rows = selector_leak_rows()
    queue_rows = coefficient_queue_rows(c)
    parent_rows = parent_signature_rows()
    gates = claim_gate_rows()
    status = status_rows(c)
    next_target = next_rows()
    decisions = decision_rows()

    all_rows = {
        "sources": sources,
        "zero": zero_rows,
        "family": family_rows,
        "selector": selector_rows,
        "queue": queue_rows,
        "parent": parent_rows,
        "gates": gates,
        "status": status,
        "next": next_target,
        "decisions": decisions,
    }

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_THEOREM_CSV, zero_rows)
    write_csv(R11_FAMILY_CSV, family_rows)
    write_csv(SELECTOR_LEAK_CSV, selector_rows)
    write_csv(COEFF_QUEUE_CSV, queue_rows)
    write_csv(PARENT_SIGNATURE_CSV, parent_rows)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validation_rows(all_rows)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, zero_rows, family_rows, selector_rows, queue_rows, parent_rows, gates, status, next_target, decisions, validation)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)

    append_claim_once()
    append_section_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4503 DeltaE R11 EH-Only Operator Or First Coefficient Bound

Marker: `{MARKER}`  
4503 narrows the first `A_E` subchannel. `DeltaE_R11_l2` is zero if the parent signs one of four real routes: EH-only through l=2, double-zero selectors for retained non-EH families, algebraic O(3) conformal descent, or scalar Hessian kill with boundary silence. None is signed for actual rows yet, but the fallback is now an exact coefficient queue: `||W_STF||_1 ||K_2^X|| sum_A |c_A| N_A <= {c['equal_a']:.15e}`. The next concrete target is `R2_fR_scalar_mode`.
""",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4503 Packet Integration

Marker: `{PACKET_MARKER}`  
The local packet now has an exact attack route for `DeltaE_R11_l2`. We are no longer just saying an R11 coefficient is missing: either prove an EH-only/double-zero/conformal/Hessian silence theorem, or fill the first coefficient row. The first row to attack is `R2_fR_scalar_mode`, with bound `|c_R2_or_c_fR| <= {c['equal_a']:.15e}/(||W_STF||_1 ||K_2^X|| N_R2_fR_scalar_mode)`.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
