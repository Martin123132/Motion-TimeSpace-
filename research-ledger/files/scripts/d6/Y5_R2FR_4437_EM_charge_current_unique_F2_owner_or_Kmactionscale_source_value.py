from __future__ import annotations

import csv
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from action_density_edge_gate import evaluate_k_source_leg_rows, write_csv  # noqa: E402
from same_owner_coupling_gate import evaluate_same_owner_rows  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4437"
CLAIM_ID = "L-278"
MARKER = "PPC4161_EM_CHARGE_CURRENT_UNIQUE_F2_OWNER_OR_KMACTIONSCALE_SOURCE_VALUE_4437"
PACKET_MARKER = "PPC4161_PACKET_EM_CHARGE_CURRENT_UNIQUE_F2_OWNER_OR_KMACTIONSCALE_SOURCE_VALUE_4437"
DECISION = "SAME_OWNER_EM_COUPLING_ZERO_IN_FIXED_QBASIC_STANDARD_BRANCH_GLOBAL_DYNAMIC_BRANCH_AND_NUMERIC_ALPHA_RETAINED"
NEXT_TARGET = "4438-Y5-R2FR-radiative-readout-EM-closure-or-total-Kmactionscale-source-value.md"

FORMAL_PATH = FORMAL / "453-PPC4161-EM-charge-current-unique-F2-owner-or-Kmactionscale-source-value.md"
DOC_PATH = POST / "4437-Y5-R2FR-EM-charge-current-unique-F2-owner-or-Kmactionscale-source-value.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4437_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4437_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4437_DERIVATION_ROWS.csv"
SAME_OWNER_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4437_SAME_OWNER_COUPLING_INPUT.csv"
SAME_OWNER_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4437_SAME_OWNER_COUPLING_OUTPUT.csv"
ZERO_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4437_EM_COUPLING_ZERO_ROWS.csv"
SURVIVOR_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4437_EM_COUPLING_SURVIVOR_ROWS.csv"
KLEG_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4437_K_ACTION_SOURCE_LEG_INPUT.csv"
KLEG_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4437_K_ACTION_SOURCE_LEG_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4437_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4437_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4437_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4437_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "same_owner_coupling_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4437_EM_charge_current_unique_F2_owner_or_Kmactionscale_source_value.py"
ACTION_EDGE_GATE = SCRIPT_DIR / "action_density_edge_gate.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4436 = SOURCE_DIR / "P8_Y5_R2FR_4436_NEXT_TARGET.csv"
FORMAL_452 = FORMAL / "452-PPC4161-visible-EM-action-edge-parent-signature-or-Kmactionscale-source-leg.md"
FORMAL_225 = FORMAL / "225-PPC4161-Maxwell-normalization-charge-current-owner.md"
FORMAL_226 = FORMAL / "226-PPC4161-standard-visible-matter-import-contract.md"
FORMAL_277 = FORMAL / "277-PPC4161-visible-EM-action-domain-fork-or-constitutive-bound.md"
FORMAL_278 = FORMAL / "278-PPC4161-visible-EM-readout-guard-or-charge-normalization-bound.md"
FORMAL_283 = FORMAL / "283-PPC4161-Dq-coeff-fixed-parent-constant-or-Newton-calibration-bound.md"
FORMAL_329 = FORMAL / "329-PPC4161-EM-Ward-current-normalization-or-collar-residual-bound-values.md"
FORMAL_346 = FORMAL / "346-PPC4161-coefficient-drift-zero-or-source-backed-tail-bound.md"
ALPHA3464 = SOURCE_DIR / "P8_Y5_R2FR_3464_EM_ALPHA_CHARGE_OWNER_AUDIT.csv"
OWNER3465 = SOURCE_DIR / "P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv"
ALPHA_RESIDUAL3507 = SOURCE_DIR / "P8_EM_scalar_coupling_owner_alpha_residual.csv"
ALPHA1812 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1812_ALPHA_LEVEL_OWNER_AUDIT.csv"
VGN765 = SOURCE_DIR / "P8_Y5_R10_765_VERTICAL_GENERATOR_NORM_THEOREM_ATTEMPT.csv"
RES4436 = SOURCE_DIR / "P8_Y5_R2FR_4436_EM_SCALE_CURRENT_RESIDUAL_ROWS.csv"
KLEG4436 = SOURCE_DIR / "P8_Y5_R2FR_4436_K_ACTION_SOURCE_LEG_OUTPUT.csv"

DELTA_Q_MHAT = 3.330000e-03
ETA_BOUND = 2.8e-15
D_MHAT_ONE_CHANNEL_CEILING = ETA_BOUND / DELTA_Q_MHAT


def text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


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


def rows_from(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def source_specs() -> List[Dict[str, object]]:
    return [
        {"source_id": "SRC4437_00_4436_next", "path": NEXT_4436, "needle": "4437-Y5-R2FR-EM-charge-current-unique-F2-owner", "role": "4436 handoff."},
        {"source_id": "SRC4437_01_452_formal", "path": FORMAL_452, "needle": "VEM4436_3_scale_current_coupling_throat", "role": "current coupling throat."},
        {"source_id": "SRC4437_02_225_norm", "path": FORMAL_225, "needle": "alpha_eff proportional to g_J^2/lambda_A", "role": "normalization identity."},
        {"source_id": "SRC4437_03_226_visible_import", "path": FORMAL_226, "needle": "calibrated/q-basic visible-sector readout constants", "role": "standard visible import contract."},
        {"source_id": "SRC4437_04_277_action_domain", "path": FORMAL_277, "needle": "DeltaS_MTS_visible = 0 before variation", "role": "standard visible action-domain signature."},
        {"source_id": "SRC4437_05_278_readout_guard", "path": FORMAL_278, "needle": "D_X ln g_J = 0", "role": "fixed EM coupling branch."},
        {"source_id": "SRC4437_06_283_coeff", "path": FORMAL_283, "needle": "Dq_coeff = 0", "role": "fixed coefficient branch."},
        {"source_id": "SRC4437_07_329_ward", "path": FORMAL_329, "needle": "CN4313_1_fixed_visible_branch", "role": "current owner / Ward branch."},
        {"source_id": "SRC4437_08_346_coeff", "path": FORMAL_346, "needle": "D_X ln g_J = D_X ln lambda_A = 0", "role": "coefficient drift zero rollup."},
        {"source_id": "SRC4437_09_3464_alpha", "path": ALPHA3464, "needle": "EAC3464_5_verdict", "role": "alpha/action normalization older audit."},
        {"source_id": "SRC4437_10_3465_owner", "path": OWNER3465, "needle": "EMO3465_5_verdict", "role": "EM owner package older gap."},
        {"source_id": "SRC4437_11_3507_alpha_residual", "path": ALPHA_RESIDUAL3507, "needle": "ARE3507_0_b_alpha_X", "role": "same-owner identity source."},
        {"source_id": "SRC4437_12_1812_alpha_level", "path": ALPHA1812, "needle": "ALO1812_2_unique_F2", "role": "global parent alpha-level gap."},
        {"source_id": "SRC4437_13_765_generator_norm", "path": VGN765, "needle": "VGN765_6_verdict", "role": "vertical generator route gap."},
        {"source_id": "SRC4437_14_4436_residual", "path": RES4436, "needle": "RES4436_0_C_XF2", "role": "4436 residual vector."},
        {"source_id": "SRC4437_15_4436_kleg", "path": KLEG4436, "needle": "KLEG4436_1_EM_action_scale_component", "role": "4436 K action-scale source leg."},
        {"source_id": "SRC4437_16_gate", "path": GATE_PATH, "needle": "def evaluate_same_owner_row", "role": "4437 gate script."},
        {"source_id": "SRC4437_17_generator", "path": GENERATOR_PATH, "needle": "CHECKPOINT = \"4437\"", "role": "4437 generator script."},
        {"source_id": "SRC4437_18_kleg_gate", "path": ACTION_EDGE_GATE, "needle": "def evaluate_k_source_leg_row", "role": "K source-leg evaluator."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for spec in source_specs():
        source_path = Path(spec["path"])
        needle = str(spec["needle"])
        content = text(source_path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "path": str(source_path),
                "path_exists": source_path.exists(),
                "needle": needle,
                "needle_found": needle in content,
                "line_number": line_of(source_path, needle),
                "role": spec["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "SOC4437_0_same_owner_identity",
            "claim": "The invariant EM drift is the same-owner ratio, not a field convention.",
            "derivation": "Writing S_EM=-lambda_A/4 int F^2 + g_J int A.J gives alpha_eff proportional to g_J^2/lambda_A after canonical normalization. Therefore b_alpha=D_X ln alpha_eff=2 D_X ln g_J-D_X ln lambda_A. A rescaling of A only moves normalization between the two slots; it does not remove a real relative derivative.",
            "consequence": "The true target is not absolute alpha_EM. The target is whether g_J and lambda_A are q-basic/fixed by the same branch owner.",
            "status": "EXACT_IDENTITY",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SOC4437_1_fixed_qbasic_branch_zero",
            "claim": "The standard fixed q-basic visible branch kills the EM coupling drift.",
            "derivation": "In the 4210/4262/4330 branch, theta_obs={m_A,charges,alpha_EM,hbar,c,material labels}, g_J and lambda_A are fixed before variation and readout is postprocessing. Thus D_X ln g_J=0, D_X ln lambda_A=0, b_alpha=0 and C_JQ=0. Since DeltaS_MTS_visible=0 before variation, no independent MTS-visible f_X(Phi)F^2 slot exists in that branch, so C_XF2=0 branch-conditionally.",
            "consequence": "This closes the EM scale/current part of K_m_EM*C_EM for the private standard branch without predicting alpha_EM.",
            "status": "BRANCH_ZERO_DERIVED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SOC4437_2_unique_F2_scope_firewall",
            "claim": "Unique F2 is closed only by branch typing, not by global covariance.",
            "derivation": "Outside the standard visible branch, covariance allows lambda_A(Phi)F^2, hidden coefficient morphisms, readout-regenerated effective terms, or dynamic charge/current normalization. The 1812/765 route remains the stronger global parent route but is unsigned.",
            "consequence": "The branch zero must not be promoted to a global MTS Maxwell/QED derivation.",
            "status": "GLOBAL_DYNAMIC_BRANCH_RETAINED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SOC4437_3_K_source_value_split",
            "claim": "The EM scale-current product is zero in the fixed branch, but the total source-leg value remains branch-sensitive.",
            "derivation": "The fixed branch gives K_m_EM*C_EM_scale_current=0 for C_XF2, C_JQ, b_alpha and dlnlambda. It does not source a numeric alpha_EM value, a global generator norm, or nonstandard dynamic branch coefficients. The empirical ceiling remains a bound on any surviving branch product.",
            "consequence": "The next target is radiative/readout closure or a real source-leg value for nonstandard branches, not fitting the bound backward.",
            "status": "PARTIAL_K_PRODUCT_ZERO_BOUND_RETAINED",
            "valid_for_claim": False,
        },
    ]


def same_owner_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "SOC4437_0_fixed_qbasic_standard_branch",
            "branch": "4210/4262/4330 fixed q-basic standard visible branch",
            "action_edge_signed": True,
            "fixed_theta_obs": True,
            "fixed_lambda_A": True,
            "fixed_g_J": True,
            "no_independent_F2_slot": True,
            "same_current_owner": True,
            "alpha_readout_qbasic": True,
            "readout_after_variation": True,
            "no_hidden_coefficient_slot": True,
            "no_dynamic_coefficient_branch": True,
            "source_path": str(FORMAL_346),
            "input_valid": True,
            "valid_for_claim": False,
            "notes": "Closes C_XF2/C_JQ/b_alpha only in the fixed q-basic standard branch.",
        },
        {
            "row_id": "SOC4437_1_Ward_current_same_action_branch",
            "branch": "same matter+EM action current branch",
            "action_edge_signed": True,
            "fixed_theta_obs": True,
            "fixed_lambda_A": True,
            "fixed_g_J": True,
            "no_independent_F2_slot": False,
            "same_current_owner": True,
            "alpha_readout_qbasic": True,
            "readout_after_variation": True,
            "no_hidden_coefficient_slot": False,
            "no_dynamic_coefficient_branch": False,
            "source_path": str(FORMAL_329),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Current exchange closes if same current is owned, but unique F2/global coefficient branch remains separate.",
        },
        {
            "row_id": "SOC4437_2_global_vertical_generator_norm_route",
            "branch": "global parent vertical generator norm route",
            "action_edge_signed": False,
            "fixed_theta_obs": False,
            "fixed_lambda_A": False,
            "fixed_g_J": False,
            "no_independent_F2_slot": False,
            "same_current_owner": False,
            "alpha_readout_qbasic": False,
            "readout_after_variation": False,
            "no_hidden_coefficient_slot": False,
            "no_dynamic_coefficient_branch": False,
            "source_path": str(VGN765),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "The ambitious global alpha/generator route remains the right theorem shape but unsigned.",
        },
        {
            "row_id": "SOC4437_3_dynamic_or_hidden_EM_deformation_branch",
            "branch": "dynamic hidden EM coefficient branch",
            "action_edge_signed": False,
            "fixed_theta_obs": False,
            "fixed_lambda_A": False,
            "fixed_g_J": False,
            "no_independent_F2_slot": False,
            "same_current_owner": False,
            "alpha_readout_qbasic": False,
            "readout_after_variation": False,
            "no_hidden_coefficient_slot": False,
            "no_dynamic_coefficient_branch": False,
            "source_path": str(OWNER3465),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Any g_J(Phi), lambda_A(Phi), f_X(Phi)F2 or readout-regenerated branch remains physical.",
        },
    ]


def zero_rows() -> List[Dict[str, object]]:
    return [
        {"zero_id": "ZERO4437_0_C_XF2", "symbol": "C_XF2", "zero_statement": "C_XF2=0 in fixed q-basic standard branch", "reason": "DeltaS_MTS_visible=0 before variation and no hidden coefficient slot in S_vis_standard", "source_path": str(FORMAL_277), "status": "BRANCH_ZERO_NOT_GLOBAL", "valid_for_claim": False},
        {"zero_id": "ZERO4437_1_C_JQ", "symbol": "C_JQ", "zero_statement": "C_JQ=0 in fixed q-basic standard branch", "reason": "J and A normalization are fixed visible readout data before variation", "source_path": str(FORMAL_278), "status": "BRANCH_ZERO_NOT_GLOBAL", "valid_for_claim": False},
        {"zero_id": "ZERO4437_2_b_alpha", "symbol": "b_alpha_X", "zero_statement": "b_alpha=2D_X ln g_J-D_X ln lambda_A=0", "reason": "D_X ln g_J=D_X ln lambda_A=0 in q-basic calibrated branch", "source_path": str(FORMAL_346), "status": "BRANCH_ZERO_NUMERIC_ALPHA_NOT_PREDICTED", "valid_for_claim": False},
        {"zero_id": "ZERO4437_3_dlnlambda", "symbol": "dlnlambda_derivative", "zero_statement": "d lambda_A=0 in fixed coefficient branch", "reason": "lambda_A is a calibrated branch constant, not a hidden field function", "source_path": str(FORMAL_283), "status": "BRANCH_ZERO_NOT_GLOBAL", "valid_for_claim": False},
    ]


def survivor_rows() -> List[Dict[str, object]]:
    return [
        {"survivor_id": "SURV4437_0_numeric_alpha", "symbol": "alpha_EM", "why_survives": "fixed/readout-stable does not predict the numerical value", "needed_to_close": "parent scale law or accepted calibrated constant policy", "source_path": str(FORMAL_225), "valid_for_claim": False},
        {"survivor_id": "SURV4437_1_global_unique_F2", "symbol": "global C_XF2", "why_survives": "global parent generator has not forbidden hidden-visible coefficient morphisms", "needed_to_close": "parent typed action grammar or vertical generator norm theorem", "source_path": str(ALPHA1812), "valid_for_claim": False},
        {"survivor_id": "SURV4437_2_dynamic_current", "symbol": "dynamic C_JQ", "why_survives": "outside fixed branch current/coupling can be field-dependent", "needed_to_close": "same parent current owner or source-backed deltaJ bound", "source_path": str(FORMAL_329), "valid_for_claim": False},
        {"survivor_id": "SURV4437_3_radiative_readout", "symbol": "C_EM_readout/Phi_EM_rad", "why_survives": "same-owner drift zero does not by itself close EFT/readout/radiation boundary regeneration", "needed_to_close": NEXT_TARGET, "source_path": str(OWNER3465), "valid_for_claim": False},
    ]


def kleg_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "KLEG4437_0_EM_scale_current_branch_zero",
            "product": "K_m_EM_action_scale*C_EM_scale_current",
            "coefficient_value": "DERIVED_ZERO",
            "units": "dimensionless",
            "parent_coefficient_source": str(FORMAL_346),
            "source_leg": "C_XF2=C_JQ=b_alpha=dlnlambda=0 in fixed q-basic standard branch",
            "source_leg_units": "dimensionless_branch_zero",
            "projection": "EM scale/current drift product vanishes inside the fixed standard visible branch",
            "bound_value": "0",
            "no_bound_inversion_guard": True,
            "source_path": str(FORMAL_346),
            "input_valid": True,
            "valid_for_claim": False,
            "notes": "Branch-level zero for the EM scale/current piece; not an alpha prediction and not a global branch.",
        },
        {
            "row_id": "KLEG4437_1_total_dynamic_EM_product_retained",
            "product": "K_m_EM_action_scale*C_EM_action_scale_dynamic",
            "coefficient_value": "MISSING_PARENT_COEFFICIENT",
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_GLOBAL_UNIQUE_F2_CURRENT_ALPHA_OWNER",
            "source_leg": "MISSING_DYNAMIC_EM_SOURCE_LEG",
            "source_leg_units": "dimensionless_or_declared_parent_units",
            "projection": f"{DELTA_Q_MHAT:.5f}*abs(K_m_EM_action_scale*C_EM_action_scale_dynamic) <= {ETA_BOUND:.12e}",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "no_bound_inversion_guard": True,
            "source_path": str(KLEG4436),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Retained for nonstandard/global/dynamic coefficient branches.",
        },
        {
            "row_id": "KLEG4437_2_bound_target_only",
            "product": "K_m_EM_action_scale*C_EM_action_scale_effective",
            "coefficient_value": f"BOUND_ONLY_{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_PARENT_SOURCE",
            "source_leg": "MISSING_SOURCE_LEG",
            "source_leg_units": "MISSING_SOURCE_LEG_UNITS",
            "projection": f"abs(K_m_EM_action_scale*C_EM_action_scale_effective) <= {D_MHAT_ONE_CHANNEL_CEILING:.12e} only as one-channel target",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "no_bound_inversion_guard": True,
            "source_path": str(KLEG4436),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Bound target only; cannot define the coefficient.",
        },
    ]


def claim_gate_rows(same_owner: Sequence[Mapping[str, str]], klegs: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    same_rows = {row["row_id"]: row for row in same_owner}
    kleg_rows = {row["row_id"]: row for row in klegs}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in same_owner) and not any(row.get("valid_for_claim") == "True" for row in klegs)
    return [
        {"gate_id": "CG4437_0_same_owner_branch_zero", "claim": "fixed q-basic branch kills C_XF2/C_JQ/b_alpha", "passed": same_rows["SOC4437_0_fixed_qbasic_standard_branch"].get("current_status") == "SAME_OWNER_COUPLING_BRANCH_ZERO_READY_NONCLAIM", "valid_for_claim": False, "detail": "Branch zero ready; private nonclaim."},
        {"gate_id": "CG4437_1_K_scale_current_zero", "claim": "EM scale/current K product zero in fixed branch", "passed": kleg_rows["KLEG4437_0_EM_scale_current_branch_zero"].get("current_status") == "K_ACTION_SOURCE_LEG_READY_NONCLAIM", "valid_for_claim": False, "detail": "Zeroes only the scale/current piece."},
        {"gate_id": "CG4437_2_dynamic_product_retained", "claim": "dynamic/global EM product remains missing", "passed": kleg_rows["KLEG4437_1_total_dynamic_EM_product_retained"].get("current_status") == "K_ACTION_SOURCE_LEG_CONTRACT_ONLY", "valid_for_claim": False, "detail": "Nonstandard branch needs source leg."},
        {"gate_id": "CG4437_3_bound_not_coefficient", "claim": "bound-only target retained", "passed": kleg_rows["KLEG4437_2_bound_target_only"].get("current_status") == "K_ACTION_SOURCE_LEG_BOUND_TARGET_ONLY", "valid_for_claim": False, "detail": "No bound inversion."},
        {"gate_id": "CG4437_4_survivors_retained", "claim": "numeric alpha/global dynamic branches retained", "passed": len(survivor_rows()) == 4 and "SURV4437_0_numeric_alpha" in text(SURVIVOR_ROWS), "valid_for_claim": False, "detail": "No fake alpha derivation."},
        {"gate_id": "CG4437_5_zero_rows_written", "claim": "branch zero rows written", "passed": len(zero_rows()) == 4 and "ZERO4437_0_C_XF2" in text(ZERO_ROWS), "valid_for_claim": False, "detail": "C_XF2, C_JQ, b_alpha and dlnlambda separated."},
        {"gate_id": "CG4437_6_no_public_claim", "claim": "4437 emits no local-GR/Maxwell/R10 public claim", "passed": no_claims, "valid_for_claim": False, "detail": "Private branch progress only."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4437_0",
            "decision": DECISION,
            "summary": "4437 closes the EM scale/current coupling throat inside the fixed q-basic standard visible branch. The exact identity alpha_eff proportional to g_J^2/lambda_A means b_alpha=2D ln g_J-D ln lambda_A. In the standard branch, g_J, lambda_A, alpha_EM, charges and readout labels are fixed before variation; DeltaS_MTS_visible=0 removes the independent hidden F2 slot. Therefore C_XF2, C_JQ, b_alpha and dlnlambda vanish branch-conditionally. This does not predict alpha_EM and does not close global/dynamic coefficient branches.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4437_0_branch", "status": "EM_SCALE_CURRENT_ZERO_IN_FIXED_QBASIC_BRANCH", "detail": "C_XF2, C_JQ, b_alpha and dlnlambda are zero on the private standard branch.", "valid_for_claim": False},
        {"status_id": "STAT4437_1_alpha", "status": "ALPHA_NUMERIC_VALUE_NOT_DERIVED", "detail": "The branch is calibrated/readout-stable; it is not an alpha prediction.", "valid_for_claim": False},
        {"status_id": "STAT4437_2_survivor", "status": "GLOBAL_DYNAMIC_AND_RADIATIVE_READOUT_BRANCHES_RETAINED", "detail": "Nonstandard coefficient functions and radiative/readout regeneration still need zero or source-backed values.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4437_0",
            "target": NEXT_TARGET,
            "objective": "Close radiative/readout EM regeneration or source the remaining total K_m_EM_action_scale product value.",
            "derive_first": "prove readout/EFT/radiation preservation: fixed branch EM coefficients are not regenerated by S_eff, clocks, spectroscopy, open collar flux or loop/readout maps.",
            "fallback": "fill source-backed C_EM_readout/Phi_EM_rad/dynamic C_XF2/C_JQ/b_alpha product rows with units and no-cancellation projection.",
            "avoid": "calling b_alpha=0 a numerical alpha prediction; globalizing the standard visible branch; using the local bound as a source coefficient.",
            "valid_for_claim": False,
        }
    ]


def build_doc(
    sources: Sequence[Mapping[str, object]],
    same_owner: Sequence[Mapping[str, str]],
    klegs: Sequence[Mapping[str, str]],
    gates: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 453 PPC4161 EM charge-current unique F2 owner or Kmactionscale source value

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4437 is a real coupling-narrowing step:

- The invariant EM drift is `b_alpha = 2 D_X ln g_J - D_X ln lambda_A`; this is not removable by field convention.
- In the fixed q-basic standard visible branch, `g_J`, `lambda_A`, charges, `alpha_EM` and readout labels are fixed before variation, while `DeltaS_MTS_visible=0` removes an independent MTS `f_X(Phi)F^2` slot.
- Therefore `C_XF2=0`, `C_JQ=0`, `b_alpha=0`, and `dlnlambda=0` **only in that private branch**.
- The EM scale/current piece of `K_m_EM_action_scale*C_EM_action_scale` is `DERIVED_ZERO` in the fixed branch.
- This does **not** predict numerical `alpha_EM`, does not parent-sign the global vertical-generator route, and does not close radiative/readout regeneration.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Same-Owner Coupling Gate

{table(same_owner)}

## Branch Zero Rows

{table(zero_rows())}

## Survivor Rows

{table(survivor_rows())}

## K Action-Scale Source Leg Gate

{table(klegs)}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4437 - EM charge-current unique F2 owner or Kmactionscale source value

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Closed the EM scale/current drift piece inside the fixed q-basic standard visible branch.
- Wrote explicit zeros for `C_XF2`, `C_JQ`, `b_alpha`, and `dlnlambda` in that branch.
- Kept numerical `alpha_EM`, global generator norm, dynamic hidden coefficients and radiative/readout regeneration out of the claim.
- Converted the EM scale/current part of `K_m_EM_action_scale*C_EM_action_scale` to branch `DERIVED_ZERO`, while retaining dynamic/global source-leg rows.

## Decision

{table(decision_rows())}

## Next target

{table(next_rows())}
"""


def upsert_marked_section(path: Path, marker: str, section: str) -> None:
    existing = text(path)
    start = f"<!-- {marker}:START -->"
    end = f"<!-- {marker}:END -->"
    block = f"{start}\n{section.rstrip()}\n{end}\n"
    if start in existing and end in existing:
        before = existing.split(start)[0]
        after = existing.split(end, 1)[1].lstrip("\n")
        write_text(path, before + block + after)
    else:
        separator = "" if existing.endswith("\n") or not existing else "\n"
        write_text(path, existing + separator + block)


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH) if CLAIMS_PATH.exists() else []
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    rows = [row for row in rows if row.get("claim_id") != CLAIM_ID]
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "em_local_gr",
        "claim": "4437 closes the EM scale/current coupling throat only inside the fixed q-basic standard visible branch: C_XF2, C_JQ, b_alpha and dlnlambda vanish there, so the EM scale/current piece of K_m_EM_action_scale*C_EM_action_scale is DERIVED_ZERO. Numerical alpha_EM, global generator norm, dynamic coefficient branches and radiative/readout regeneration remain unsigned.",
        "current_evidence": "4437 source register, derivation rows, same-owner coupling gate, zero rows, survivor rows, K source-leg rows, claim gates, decision, status, next target and validation CSV.",
        "status": "same_owner_EM_coupling_zero_in_fixed_qbasic_branch_global_dynamic_radiative_retained_nonclaim",
        "next_test": "Close radiative/readout EM regeneration or source remaining total K_m_EM_action_scale product values.",
        "key_risk": "Calling stable calibrated alpha a prediction; globalizing the standard visible branch; using the local bound as a coefficient.",
        "sector": "em_local_gr",
        "evidence": "4437 source register, derivation rows, same-owner coupling gate, zero rows, survivor rows, K source-leg rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Close radiative/readout EM regeneration or source remaining total K_m_EM_action_scale product values.",
        "risk": "Calling stable calibrated alpha a prediction; globalizing the standard visible branch; using the local bound as a coefficient.",
    }
    rows.append({fieldname: new_row.get(fieldname, "") for fieldname in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = """## 4437 local spine update: EM coupling drift zero in fixed branch

4437 closes the branch-level EM scale/current coupling throat. In the fixed q-basic standard visible branch, `D_X ln g_J=D_X ln lambda_A=0`, `DeltaS_MTS_visible=0`, and readout is post-variation. Therefore `C_XF2`, `C_JQ`, `b_alpha` and `dlnlambda` vanish in that branch. This is not a numerical prediction of `alpha_EM` and not a global MTS EM derivation; dynamic coefficient and radiative/readout branches remain explicit.
"""
    packet_section = f"""## 4437 packet update: same-owner EM drift closed branch-conditionally

`{PACKET_MARKER}`

Private packet result: the EM scale/current part of `K_m_EM_action_scale*C_EM_action_scale` is `DERIVED_ZERO` on the fixed q-basic branch. Next, close radiative/readout regeneration or fill source-backed dynamic/global EM product rows.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    same_owner = {row["row_id"]: row for row in rows_from(SAME_OWNER_OUTPUT)}
    klegs = {row["row_id"]: row for row in rows_from(KLEG_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in same_owner.values()) and not any(row.get("valid_for_claim") == "True" for row in klegs.values())
    checks = [
        ("VAL4437_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4437_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4437_2_same_owner_zero", same_owner["SOC4437_0_fixed_qbasic_standard_branch"].get("current_status") == "SAME_OWNER_COUPLING_BRANCH_ZERO_READY_NONCLAIM", "fixed q-basic same-owner branch zero ready"),
        ("VAL4437_3_global_retained", same_owner["SOC4437_2_global_vertical_generator_norm_route"].get("valid_for_claim") == "False", "global vertical generator route remains unsigned"),
        ("VAL4437_4_zero_rows", len(rows_from(ZERO_ROWS)) == 4 and "ZERO4437_0_C_XF2" in text(ZERO_ROWS), "zero rows written"),
        ("VAL4437_5_survivor_rows", len(rows_from(SURVIVOR_ROWS)) == 4 and "SURV4437_0_numeric_alpha" in text(SURVIVOR_ROWS), "survivor rows written"),
        ("VAL4437_6_kleg_zero", klegs["KLEG4437_0_EM_scale_current_branch_zero"].get("current_status") == "K_ACTION_SOURCE_LEG_READY_NONCLAIM", "EM scale-current K product branch zero"),
        ("VAL4437_7_kleg_dynamic", klegs["KLEG4437_1_total_dynamic_EM_product_retained"].get("current_status") == "K_ACTION_SOURCE_LEG_CONTRACT_ONLY", "dynamic/global product retained"),
        ("VAL4437_8_bound_only", klegs["KLEG4437_2_bound_target_only"].get("current_status") == "K_ACTION_SOURCE_LEG_BOUND_TARGET_ONLY", "bound-only row retained"),
        ("VAL4437_9_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4437_10_claim_gate_no_claim", any(row["gate_id"] == "CG4437_6_no_public_claim" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4437_11_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-278"),
        ("VAL4437_12_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4437_13_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4437_14_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4437_15_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4437_16_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4437_17_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(SAME_OWNER_INPUT, same_owner_input_rows())
    write_csv(SAME_OWNER_OUTPUT, evaluate_same_owner_rows(SAME_OWNER_INPUT))
    write_csv(ZERO_ROWS, zero_rows())
    write_csv(SURVIVOR_ROWS, survivor_rows())
    write_csv(KLEG_INPUT, kleg_input_rows())
    write_csv(KLEG_OUTPUT, evaluate_k_source_leg_rows(KLEG_INPUT))
    same_owner = rows_from(SAME_OWNER_OUTPUT)
    klegs = rows_from(KLEG_OUTPUT)
    gates = claim_gate_rows(same_owner, klegs)
    write_csv(CLAIM_GATES, gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), same_owner, klegs, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()
