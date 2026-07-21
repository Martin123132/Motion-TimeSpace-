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

CHECKPOINT = "4501"
CLAIM_ID = "L-343"
MARKER = "PPC4161_A_SHELL_COMPONENT_SOURCE_COEFFICIENT_FILL_OR_KERNEL_ZERO_4501"
PACKET_MARKER = "PPC4161_PACKET_A_SHELL_COMPONENT_SOURCE_COEFFICIENT_FILL_OR_KERNEL_ZERO_4501"
DECISION = "COMPONENT_CHAIN_RULE_AND_J2_BUDGET_FILLED_READOUT_IDENTITY_ZERO_CONDITIONAL_NONCLAIM"
NEXT_TARGET = "4502-Y5-R2FR-AE-residual-product-bound-or-extra-sector-zero.md"

FORMAL_PATH = FORMAL / "517-PPC4161-A-shell-component-source-coefficient-fill-or-kernel-zero.md"
DOC_PATH = POST / "4501-Y5-R2FR-A-shell-component-source-coefficient-fill-or-kernel-zero.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4501_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4501_SOURCE_REGISTER.csv"
CHAIN_RULE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4501_COMPONENT_ZERO_CHAIN_RULE.csv"
COMPONENT_BUDGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4501_COMPONENT_TRANSFER_BUDGET.csv"
RESIDUAL_MAP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4501_RESIDUAL_LEDGER_COMPONENT_MAP.csv"
READOUT_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4501_READOUT_IDENTITY_ZERO_AUDIT.csv"
PARENT_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4501_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4501_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4501_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4501_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4501_NEXT_TARGET.csv"

FORMAL_516 = FORMAL / "516-PPC4161-J2-shell-surface-amplitude-source-row-or-parent-kernel-zero.md"
POST_4500 = POST / "4500-Y5-R2FR-J2-shell-surface-amplitude-source-row-or-parent-kernel-zero.md"
SCRIPT_4500 = SCRIPT_DIR / "Y5_R2FR_4500_J2_shell_surface_amplitude_source_row_or_parent_kernel_zero.py"
ZERO_THEOREM_4500 = SOURCE_DIR / "P8_Y5_R2FR_4500_A_SHELL_ZERO_THEOREM.csv"
SOURCE_COMPONENTS_4500 = SOURCE_DIR / "P8_Y5_R2FR_4500_A_SHELL_SOURCE_COMPONENTS.csv"
FINITE_4500 = SOURCE_DIR / "P8_Y5_R2FR_4500_FINITE_A_SHELL_SOURCE_ROW.csv"
PRESSURE_4500 = SOURCE_DIR / "P8_Y5_R2FR_4500_J2_PRESSURE_BOUND_ROWS.csv"
J2_OPERATOR_4499 = SOURCE_DIR / "P8_Y5_R2FR_4499_J2_SHELL_TRANSFER_OPERATOR.csv"
J2_BOUNDS_3170 = SOURCE_DIR / "P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv"
J2_NORMALIZATION_3170 = SOURCE_DIR / "P8_Y5_R2FR_3170_SOLAR_J2_NORMALIZATION_DERIVATION.csv"
RESIDUAL_L2_1955 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1955_RESIDUAL_L2_BOUND_LEDGER.csv"
K2_SOURCE_4484 = SOURCE_DIR / "P8_Y5_R2FR_4484_K2_SOURCE_OWNER_ROWS.csv"
K2_ZERO_4485 = SOURCE_DIR / "P8_Y5_R2FR_4485_K2_SOURCE_SILENCE_THEOREM.csv"
K2_AUDIT_4485 = SOURCE_DIR / "P8_Y5_R2FR_4485_CURRENT_K2_SOURCE_AUDIT.csv"
PARENT_AUDIT_4498 = SOURCE_DIR / "P8_Y5_R2FR_4498_PARENT_SIGNATURE_AUDIT.csv"

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


def rows_by(path: Path, key: str) -> Dict[str, Dict[str, str]]:
    if not path.exists():
        return {}
    return {row[key]: row for row in read_csv(path) if key in row}


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4501_00_formal516", "4500 formal handoff", FORMAL_516, "A_shell_surface = A_H + A_E + A_B + A_R", "amplitude decomposition"),
        ("SRC4501_01_post4500", "4500 post mirror", POST_4500, "derive or bound A_H, A_E, A_B, A_R", "selected target"),
        ("SRC4501_02_zero4500", "4500 zero theorem rows", ZERO_THEOREM_4500, "AZ4500_1_zero_condition", "simultaneous component zero theorem"),
        ("SRC4501_03_components4500", "4500 component rows", SOURCE_COMPONENTS_4500, "ASC4500_1_residual", "four component definitions"),
        ("SRC4501_04_finite4500", "4500 finite row", FINITE_4500, "FAS4500_0_master", "triangle-bound target"),
        ("SRC4501_05_pressure4500", "4500 J2 pressure bounds", PRESSURE_4500, "J2B4500_0_surface_amplitude", "tau_A_shell_surface"),
        ("SRC4501_06_j2op4499", "4499 J2 transfer operator", J2_OPERATOR_4499, "J2OP4499_0_public_metric_conversion", "component-to-J2 coefficient"),
        ("SRC4501_07_bounds3170", "3170 corrected J2 bounds", J2_BOUNDS_3170, "CJ3170_2_Rozelot_half_range_proxy", "numeric pressure row"),
        ("SRC4501_08_norm3170", "3170 J2 normalization", J2_NORMALIZATION_3170, "JN3170_1_corrected_J2eff_map", "two-epsilon convention"),
        ("SRC4501_09_residual1955", "1955 residual l2 ledger", RESIDUAL_L2_1955, "RB1955_0_residual_bound_formula", "component product fallback"),
        ("SRC4501_10_k2source4484", "4484 source owner rows", K2_SOURCE_4484, "KSO4484_3_readout_l2_derivative", "readout derivative slot"),
        ("SRC4501_11_k2zero4485", "4485 source-silence theorem", K2_ZERO_4485, "KZS4485_1_clean_zero_theorem", "component zero template"),
        ("SRC4501_12_k2audit4485", "4485 current K2 audit", K2_AUDIT_4485, "CSA4485_4_readout", "identity-readout evidence"),
        ("SRC4501_13_parent4498", "4498 parent signature audit", PARENT_AUDIT_4498, "PS4498_3_no_rep_coefficients", "representative/readout coefficient hazard"),
        ("SRC4501_14_script4500", "4500 generator", SCRIPT_4500, 'CHECKPOINT = "4500"', "reproducible predecessor script"),
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


def constants() -> Dict[str, float]:
    j2_operator = rows_by(J2_OPERATOR_4499, "operator_id").get("J2OP4499_0_public_metric_conversion", {})
    j2_bound = rows_by(J2_BOUNDS_3170, "bound_id").get("CJ3170_2_Rozelot_half_range_proxy", {})
    c_j2 = float(j2_operator.get("numeric_coefficient_rho1_abs", "2.355709750522272e+05"))
    tau_a = float(j2_bound.get("A_metric_bound_surface", "1.400851696295935e-13"))
    tau_j2 = float(j2_bound.get("J2_eff_bound", "3.3e-08"))
    two_epsilon = float(j2_bound.get("two_epsilon_sun_surface", "4.245005140290714e-06"))
    return {
        "c_j2": c_j2,
        "tau_a": tau_a,
        "tau_j2": tau_j2,
        "two_epsilon": two_epsilon,
        "equal_a_budget": tau_a / 4.0,
        "equal_j2_budget": tau_j2 / 4.0,
    }


def chain_rule_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "CR4501_0_chain_rule",
            "component": "all",
            "functional_slot": "F_i[Phi]",
            "statement": "For any component functional that is q-basic, the shell-vertical derivative vanishes by the chain rule.",
            "formula": "F_i[Phi]=Fbar_i(q(Phi)); v_shell in ker(Dq) => delta_v F_i = DFbar_i[Dq(v_shell)] = 0",
            "derived_result": "EXACT_COMPONENT_ZERO_TEMPLATE",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CR4501_1_Hilbert",
            "component": "A_H",
            "functional_slot": "T_H[q(Phi),Psi]",
            "statement": "Hilbert/coframe stress contributes no shell quadrupole if the matter/source action descends through the same public metric/coframe and the shell direction is q-vertical.",
            "formula": "S_m=Sbar_m[q(Phi),Psi] and Dq(v_shell)=0 => delta_v T_H=0 => A_H=0",
            "derived_result": "CONDITIONAL_CHAIN_RULE_ZERO",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CR4501_2_residual",
            "component": "A_E",
            "functional_slot": "E_extra[q(Phi)]",
            "statement": "Extra residual stress contributes no shell quadrupole if the extra-sector field equation is q-basic or on-shell exact in the shell direction.",
            "formula": "E_extra=Ebar_extra(q(Phi)) or delta_v E_extra=0 => A_E=0",
            "derived_result": "CONDITIONAL_EXTRA_SECTOR_ZERO",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CR4501_3_boundary",
            "component": "A_B",
            "functional_slot": "B_l2[q(Phi)]",
            "statement": "Boundary/matching data contributes no shell quadrupole if the local collar boundary functional is fixed, no-flux, or q-basic under the shell variation.",
            "formula": "delta_v B_l2=0 => A_B=0",
            "derived_result": "CONDITIONAL_BOUNDARY_ZERO",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CR4501_4_readout",
            "component": "A_R",
            "functional_slot": "R_readout[q(Phi)]",
            "statement": "Readout contributes no independent shell quadrupole on the identity-readout branch because the public metric/coframe is the readout, not a second map with its own shell coefficient.",
            "formula": "g_obs=q(Phi) with no disformal/source-shadow readout => delta_v R_readout=0 => A_R=0",
            "derived_result": "IDENTITY_READOUT_CONDITIONAL_ZERO",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def component_budget_rows(c: Mapping[str, float]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for component, meaning in [
        ("A_H", "Hilbert/source l=2 stress derivative"),
        ("A_E", "extra-sector l=2 residual derivative"),
        ("A_B", "boundary/matching l=2 derivative"),
        ("A_R", "independent readout/shadow l=2 derivative"),
    ]:
        rows.append(
            {
                "budget_id": f"CB4501_{component}",
                "component": component,
                "meaning": meaning,
                "J2_transfer": "DeltaJ2_i=s_J2*A_i*rho^3/two_epsilon_surface",
                "rho1_abs_coefficient": f"{c['c_j2']:.15e}",
                "single_survivor_A_bound": f"{c['tau_a']:.15e}",
                "single_survivor_J2_bound": f"{c['tau_j2']:.15e}",
                "equal_no_cancellation_A_budget": f"{c['equal_a_budget']:.15e}",
                "equal_no_cancellation_J2_budget": f"{c['equal_j2_budget']:.15e}",
                "claim_effect": "component now has a concrete J2 scoring budget once its amplitude is sourced or zeroed",
                "valid_for_claim": False,
            }
        )
    rows.append(
        {
            "budget_id": "CB4501_triangle_total",
            "component": "A_shell_surface",
            "meaning": "no-cancellation total safety condition",
            "J2_transfer": "DeltaJ2_shell=s_J2*(A_H+A_E+A_B+A_R)*rho^3/two_epsilon_surface",
            "rho1_abs_coefficient": f"{c['c_j2']:.15e}",
            "single_survivor_A_bound": f"{c['tau_a']:.15e}",
            "single_survivor_J2_bound": f"{c['tau_j2']:.15e}",
            "equal_no_cancellation_A_budget": f"{c['equal_a_budget']:.15e}",
            "equal_no_cancellation_J2_budget": f"{c['equal_j2_budget']:.15e}",
            "claim_effect": "|A_H|+|A_E|+|A_B|+|A_R| <= tau_A_shell_surface is sufficient; cancellation is not credited",
            "valid_for_claim": False,
        }
    )
    return rows


def residual_map_rows(c: Mapping[str, float]) -> List[Dict[str, object]]:
    return [
        {
            "map_id": "RM4501_0_source_Hilbert",
            "component": "A_H",
            "source_ledger_term": "||W_STF||_1 ||K_2|| ||Delta J_2^MTS||",
            "component_bound": "|A_H| <= ||W_STF||_1 ||K_2|| ||Delta J_2^MTS||",
            "single_component_pass_condition": f"||W_STF||_1 ||K_2|| ||Delta J_2^MTS|| <= {c['tau_a']:.15e}",
            "equal_budget_condition": f"||W_STF||_1 ||K_2|| ||Delta J_2^MTS|| <= {c['equal_a_budget']:.15e}",
            "status": "SYMBOLIC_PRODUCT_BOUND_FILLED_NUMERIC_FACTORS_MISSING",
            "valid_for_claim": False,
        },
        {
            "map_id": "RM4501_1_extra_residual",
            "component": "A_E",
            "source_ledger_term": "||W_STF||_1 ||K_2^X|| ||P_2 R_extra||",
            "component_bound": "|A_E| <= ||W_STF||_1 ||K_2^X|| ||P_2 R_extra||",
            "single_component_pass_condition": f"||W_STF||_1 ||K_2^X|| ||P_2 R_extra|| <= {c['tau_a']:.15e}",
            "equal_budget_condition": f"||W_STF||_1 ||K_2^X|| ||P_2 R_extra|| <= {c['equal_a_budget']:.15e}",
            "status": "AE_RESIDUAL_PRODUCT_BOUND_FILLED_NUMERIC_FACTORS_MISSING",
            "valid_for_claim": False,
        },
        {
            "map_id": "RM4501_2_boundary",
            "component": "A_B",
            "source_ledger_term": "||W_STF||_1 ||H_2|| ||Delta h_boundary2^MTS||",
            "component_bound": "|A_B| <= ||W_STF||_1 ||H_2|| ||Delta h_boundary2^MTS||",
            "single_component_pass_condition": f"||W_STF||_1 ||H_2|| ||Delta h_boundary2^MTS|| <= {c['tau_a']:.15e}",
            "equal_budget_condition": f"||W_STF||_1 ||H_2|| ||Delta h_boundary2^MTS|| <= {c['equal_a_budget']:.15e}",
            "status": "BOUNDARY_PRODUCT_BOUND_FILLED_NUMERIC_FACTORS_MISSING",
            "valid_for_claim": False,
        },
        {
            "map_id": "RM4501_3_total",
            "component": "A_H+A_E+A_B",
            "source_ledger_term": "RB1955_0 residual bound formula",
            "component_bound": "|A_H|+|A_E|+|A_B| <= ||W_STF||_1(||K_2||||Delta J_2^MTS||+||K_2^X||||P_2 R_extra||+||H_2||||Delta h_boundary2^MTS||)",
            "single_component_pass_condition": f"total product <= {c['tau_a']:.15e} if A_R=0",
            "equal_budget_condition": f"each of A_H,A_E,A_B,A_R <= {c['equal_a_budget']:.15e} is sufficient",
            "status": "TOTAL_SYMBOLIC_SCORER_FILLED_READOUT_SEPARATE",
            "valid_for_claim": False,
        },
    ]


def readout_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "RA4501_0_identity_readout",
            "clause": "public metric/coframe is the readout",
            "formula": "g_obs=q(Phi), theta_obs=theta(q(Phi))",
            "result": "A_R=0 on the identity-readout branch",
            "status": "CONDITIONAL_ZERO_BRANCH_AVAILABLE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "RA4501_1_shadow_readout_guard",
            "clause": "no hidden disformal/source-shadow map",
            "formula": "g_obs=q(Phi)+D_shadow[Phi] is forbidden unless D_shadow is sourced and bounded",
            "result": "any nonzero D_shadow is A_R and must satisfy the same tau_A budget",
            "status": "NO_DOUBLE_COUNT_GUARD_ACTIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "RA4501_2_parent_signature",
            "clause": "identity readout must be parent-owned for promotion",
            "formula": "delta_v R_readout=0 follows only after the parent response map is fixed",
            "result": "use A_R=0 as a conditional branch, not local-GR proof",
            "status": "PARENT_SIGNATURE_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PA4501_0_chain_rule_theorem",
            "clause": "q-basic component functional",
            "current_status": "EXACT_TEMPLATE_DERIVED",
            "evidence": str(CHAIN_RULE_CSV),
            "remaining_unsigned": "which of A_H/A_E/A_B/A_R are actually q-basic in the parent action",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4501_1_component_budgets",
            "clause": "component-to-J2 transfer",
            "current_status": "NUMERIC_BUDGET_FILLED",
            "evidence": str(COMPONENT_BUDGET_CSV),
            "remaining_unsigned": "component amplitudes or zero theorems",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4501_2_AE_residual",
            "clause": "extra-sector residual component",
            "current_status": "PRODUCT_BOUND_FORMULA_FILLED",
            "evidence": str(RESIDUAL_MAP_CSV),
            "remaining_unsigned": "numeric ||W_STF||_1, ||K_2^X|| and ||P_2 R_extra|| or parent zero",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4501_3_readout",
            "clause": "identity readout",
            "current_status": "CONDITIONAL_ZERO_STAGED",
            "evidence": str(READOUT_AUDIT_CSV),
            "remaining_unsigned": "parent-owned no-shadow/no-disformal readout clause",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4501_0_chain_rule",
            "gate": "component chain-rule zero theorem written",
            "passed": True,
            "claim_allowed": False,
            "detail": "exact q-basic component template exists, but parent does not sign all components",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4501_1_j2_budget",
            "gate": "component J2 budgets numeric",
            "passed": True,
            "claim_allowed": False,
            "detail": "component-to-J2 coefficient and tau_A/4 budget are filled",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4501_2_AE_source",
            "gate": "A_E residual finite scorer",
            "passed": "symbolic_only",
            "claim_allowed": False,
            "detail": "product formula is filled but numeric factors or zero theorem are missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4501_3_readout_zero",
            "gate": "A_R identity-readout zero",
            "passed": "conditional",
            "claim_allowed": False,
            "detail": "clean branch exists; parent no-shadow signature still unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4501_4_local_GR_J2_promotion",
            "gate": "local GR/J2 promotion",
            "passed": False,
            "claim_allowed": False,
            "detail": "A_H/A_E/A_B/A_R are not all zeroed or numerically below the triangle bound",
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
            "chain_rule_zero_template_ready": True,
            "component_J2_budget_ready": True,
            "AE_product_bound_ready": True,
            "readout_identity_zero_conditional": True,
            "all_components_parent_signed": False,
            "local_GR_claim": False,
            "tau_A_shell_surface": f"{c['tau_a']:.15e}",
            "equal_component_budget": f"{c['equal_a_budget']:.15e}",
            "sharpest_open_clause": "prove A_E=0 from extra-sector on-shell/q-basic residual, or source numeric ||W_STF||_1 ||K_2^X|| ||P_2 R_extra|| below the component budget",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4501_0",
            "target": NEXT_TARGET,
            "preferred_route": "try to prove A_E=0 by showing the extra-sector l=2 residual is q-basic/on-shell exact under v_shell",
            "fallback_route": "source or bound ||W_STF||_1, ||K_2^X||, and ||P_2 R_extra|| against tau_A_shell_surface/4",
            "do_not_do": "use cancellation between A_H, A_E, A_B and A_R as evidence",
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
            "what_moved_forward": "4501 turns the four A_shell_surface components into chain-rule zero clauses plus numeric no-cancellation J2 budgets",
            "what_is_derived": "q-basic component functionals vanish under shell-vertical variation; every component has the same rho=1 J2 transfer coefficient and an equal-budget target",
            "what_remains_blocked": "A_E needs either an extra-sector zero theorem or numeric product factors; A_H/A_B/A_R still require parent signatures or source rows",
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
        "domain": "local_gr_newton_j2_shell_components",
        "claim": "4501 derives the q-basic component chain-rule zero template for A_H/A_E/A_B/A_R, fills numeric component-to-J2 budgets, and extracts the A_E residual product-bound lane without promoting a local-GR/J2 claim.",
        "current_evidence": "4501 source register, component chain-rule rows, component transfer budget, residual ledger component map, readout identity audit, parent audit, claim gates, status and validation.",
        "status": "private_component_chain_rule_and_budget_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "mistaking symbolic product bounds or conditional identity readout for a parent-signed local-GR theorem.",
        "sector": "local_gr_newton_j2_shell_components",
        "evidence": str(FORMAL_PATH),
        "next_action": NEXT_TARGET,
        "risk": "derive or numerically bound A_E first; no cancellation credit is allowed",
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
    chain: Sequence[Mapping[str, object]],
    budgets: Sequence[Mapping[str, object]],
    residuals: Sequence[Mapping[str, object]],
    readout: Sequence[Mapping[str, object]],
    parent_audit: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4501 - A Shell Component Source Coefficient Fill Or Kernel Zero

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Result

4501 does the component hunt rather than another broad audit.

The exact useful theorem is the component chain rule:

`F_i[Phi]=Fbar_i(q(Phi)); v_shell in ker(Dq) => delta_v F_i = DFbar_i[Dq(v_shell)] = 0`.

Applied to `A_shell_surface = A_H + A_E + A_B + A_R`, this means any Hilbert, residual, boundary, or readout component that is genuinely q-basic under the shell direction is zero. That is a derivation route, not a fitted cancellation.

The finite fallback is now concrete too. At `rho=1`, every component has

`DeltaJ2_i=s_J2*A_i/two_epsilon_surface`,

with `|DeltaJ2_i| = 2.355709750522272e+05 |A_i|`. The total no-cancellation pass condition remains

`|A_H|+|A_E|+|A_B|+|A_R| <= 1.400851696295935e-13`.

For a strict equal-budget smoke gate this gives

`|A_i| <= 3.502129240739837e-14`

for each of the four components. The first sharp next target is `A_E`: either prove the extra-sector residual is q-basic/on-shell exact, or source the product

`||W_STF||_1 ||K_2^X|| ||P_2 R_extra||`

below the component budget.

No local-GR, J2, PPN, or Newtonian-recovery claim is promoted.

## Component Chain Rule

{table(chain)}

## Component Transfer Budgets

{table(budgets)}

## Residual Ledger Component Map

{table(residuals)}

## Readout Identity Audit

{table(readout)}

## Parent Signature Audit

{table(parent_audit)}

## Claim Gates

{table(gates)}

## Status

{table(status)}

## Next Target

{table(next_target)}

## Source Register

{table(sources)}

## Decision Row

{table(decisions)}
"""


def validation_rows(
    sources: Sequence[Mapping[str, object]],
    chain: Sequence[Mapping[str, object]],
    budgets: Sequence[Mapping[str, object]],
    residuals: Sequence[Mapping[str, object]],
    readout: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
) -> List[Dict[str, object]]:
    csv_paths = [
        SOURCE_REGISTER,
        CHAIN_RULE_CSV,
        COMPONENT_BUDGET_CSV,
        RESIDUAL_MAP_CSV,
        READOUT_AUDIT_CSV,
        PARENT_AUDIT_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    parsed = []
    for path in csv_paths:
        parsed.append(f"{path.name}:{len(read_csv(path)) if path.exists() and text(path).strip() else 0}")
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4501_0_sources_exist_and_needles_found",
            "passed": all(bool(row["exists"]) and bool(row["needle_found"]) for row in sources),
            "detail": "all source-register paths exist and needles are found",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4501_1_chain_rule_rows",
            "passed": len(chain) == 5 and any(row["component"] == "A_E" for row in chain),
            "detail": "component chain-rule theorem rows present",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4501_2_component_budgets_numeric",
            "passed": len(budgets) == 5 and "3.502129240739837e-14" in text(COMPONENT_BUDGET_CSV),
            "detail": "component J2 budgets and tau_A/4 equal budget are numeric",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4501_3_AE_residual_product_bound",
            "passed": any(row["component"] == "A_E" and "||P_2 R_extra||" in row["component_bound"] for row in residuals),
            "detail": "A_E residual product-bound lane is filled symbolically",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4501_4_readout_identity_guard",
            "passed": len(readout) == 3 and "A_R=0" in text(READOUT_AUDIT_CSV),
            "detail": "identity-readout zero branch and no-shadow guard present",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4501_5_claim_gates_block_promotion",
            "passed": all(str(row["claim_allowed"]).lower() == "false" for row in gates),
            "detail": "claim gates block local-GR/J2 promotion",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4501_6_all_generated_rows_nonclaim",
            "passed": all("True" not in line.rsplit(",", 1)[-1] for path in csv_paths for line in text(path).splitlines()[1:]),
            "detail": "all generated rows keep valid_for_claim=false",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4501_7_csvs_parse",
            "passed": all(path.exists() for path in csv_paths),
            "detail": "; ".join(parsed),
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4501_8_docs_written",
            "passed": FORMAL_PATH.exists() and DOC_PATH.exists() and MARKER in text(FORMAL_PATH),
            "detail": "formal and post checkpoint docs exist",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4501_9_claim_register_updated",
            "passed": CLAIM_ID in text(CLAIMS_PATH),
            "detail": "claims register contains L-343",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4501_10_spine_and_packet_updated",
            "passed": MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH),
            "detail": "spine and packet contain 4501 markers",
            "valid_for_claim": False,
        },
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4501_11_pycache_removed",
            "passed": not (SCRIPT_DIR / "__pycache__").exists(),
            "detail": "scripts __pycache__ absent after generation",
            "valid_for_claim": False,
        },
    ]


def main() -> None:
    c = constants()
    sources = source_rows()
    chain = chain_rule_rows()
    budgets = component_budget_rows(c)
    residuals = residual_map_rows(c)
    readout = readout_audit_rows()
    parent_audit = parent_audit_rows()
    gates = claim_gate_rows()
    status = status_rows(c)
    next_target = next_rows()
    decisions = decision_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(CHAIN_RULE_CSV, chain)
    write_csv(COMPONENT_BUDGET_CSV, budgets)
    write_csv(RESIDUAL_MAP_CSV, residuals)
    write_csv(READOUT_AUDIT_CSV, readout)
    write_csv(PARENT_AUDIT_CSV, parent_audit)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    doc = build_doc(sources, chain, budgets, residuals, readout, parent_audit, gates, status, next_target, decisions)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)

    append_claim_once()

    append_section_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4501 A Shell Component Source Coefficient Fill Or Kernel Zero

Marker: `{MARKER}`  
4501 turns `A_shell_surface=A_H+A_E+A_B+A_R` into component-level zero and scoring gates. The derived theorem is the q-basic chain rule: any component functional that descends through `q` has zero shell-vertical derivative. The fallback is numeric: every component has the same J2 transfer coefficient at `rho=1`, and the no-cancellation equal budget is `|A_i| <= {c['equal_a_budget']:.15e}`. The first hard target is `A_E`, via an extra-sector zero theorem or the product bound `||W_STF||_1 ||K_2^X|| ||P_2 R_extra||`.
""",
    )

    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4501 Packet Integration

Marker: `{PACKET_MARKER}`  
The local packet now has component-level handles rather than a vague `A_shell_surface` gap. `A_H`, `A_E`, `A_B`, and `A_R` each have an exact chain-rule zero condition and a numeric J2 component budget. The next lever is `A_E`: prove the extra residual is q-basic/on-shell exact, or source the residual product factors below `{c['equal_a_budget']:.15e}` without using cancellation.
""",
    )

    if (SCRIPT_DIR / "__pycache__").exists():
        shutil.rmtree(SCRIPT_DIR / "__pycache__")

    validation = validation_rows(sources, chain, budgets, residuals, readout, gates)
    write_csv(VALIDATION_PATH, validation)
    failed = [row for row in validation if not bool(row["passed"])]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"{CHECKPOINT} validation passed ({len(validation)} checks)")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
