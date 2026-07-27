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
from radiative_readout_em_closure_gate import evaluate_em_closure_rows  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4438"
CLAIM_ID = "L-279"
MARKER = "PPC4161_RADIATIVE_READOUT_EM_CLOSURE_OR_TOTAL_KMACTIONSCALE_SOURCE_VALUE_4438"
PACKET_MARKER = "PPC4161_PACKET_RADIATIVE_READOUT_EM_CLOSURE_OR_TOTAL_KMACTIONSCALE_SOURCE_VALUE_4438"
DECISION = "TOTAL_FIXED_BRANCH_EM_PRODUCT_ZERO_IN_QBASIC_SAMEHODGE_CLOSED_COLLAR_BRANCH_OPEN_RADIATIVE_DYNAMIC_BRANCHES_RETAINED"
NEXT_TARGET = "4439-Y5-R2FR-integrate-fixed-branch-EM-zero-into-local-residual-vector-or-source-charge-tail.md"

FORMAL_PATH = FORMAL / "454-PPC4161-radiative-readout-EM-closure-or-total-Kmactionscale-source-value.md"
DOC_PATH = POST / "4438-Y5-R2FR-radiative-readout-EM-closure-or-total-Kmactionscale-source-value.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4438_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4438_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4438_DERIVATION_ROWS.csv"
EM_CLOSURE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4438_RADIATIVE_READOUT_EM_CLOSURE_INPUT.csv"
EM_CLOSURE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4438_RADIATIVE_READOUT_EM_CLOSURE_OUTPUT.csv"
ZERO_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4438_TOTAL_EM_ZERO_ROWS.csv"
SURVIVOR_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4438_OPEN_EM_SURVIVOR_ROWS.csv"
KLEG_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4438_K_ACTION_SOURCE_LEG_INPUT.csv"
KLEG_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4438_K_ACTION_SOURCE_LEG_OUTPUT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4438_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4438_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4438_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4438_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "radiative_readout_em_closure_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4438_radiative_readout_EM_closure_or_total_Kmactionscale_source_value.py"
ACTION_EDGE_GATE = SCRIPT_DIR / "action_density_edge_gate.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4437 = SOURCE_DIR / "P8_Y5_R2FR_4437_NEXT_TARGET.csv"
FORMAL_453 = FORMAL / "453-PPC4161-EM-charge-current-unique-F2-owner-or-Kmactionscale-source-value.md"
FORMAL_278 = FORMAL / "278-PPC4161-visible-EM-readout-guard-or-charge-normalization-bound.md"
FORMAL_330 = FORMAL / "330-PPC4161-radiative-Poynting-no-flux-or-boundary-flux-row.md"
FORMAL_331 = FORMAL / "331-PPC4161-Hodge-constitutive-owner-zero-or-DeltaHodge-bound.md"
FORMAL_345 = FORMAL / "345-PPC4161-Dq-EM-Hodge-Hperp-zero-or-constitutive-tail-bound.md"
FORMAL_346 = FORMAL / "346-PPC4161-coefficient-drift-zero-or-source-backed-tail-bound.md"
EM_BOUND3503 = SOURCE_DIR / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv"
EM_POYNTING3502 = SOURCE_DIR / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv"
VEB3505 = SOURCE_DIR / "P8_EM_visible_action_domain_exhaustion_no_chiEM_bound_vector.csv"
OWNER3465 = SOURCE_DIR / "P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv"
KLEG4437 = SOURCE_DIR / "P8_Y5_R2FR_4437_K_ACTION_SOURCE_LEG_OUTPUT.csv"
ZERO4437 = SOURCE_DIR / "P8_Y5_R2FR_4437_EM_COUPLING_ZERO_ROWS.csv"
SURV4437 = SOURCE_DIR / "P8_Y5_R2FR_4437_EM_COUPLING_SURVIVOR_ROWS.csv"

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
        {"source_id": "SRC4438_00_4437_next", "path": NEXT_4437, "needle": "4438-Y5-R2FR-radiative-readout-EM-closure", "role": "4437 handoff."},
        {"source_id": "SRC4438_01_453_formal", "path": FORMAL_453, "needle": "KLEG4437_0_EM_scale_current_branch_zero", "role": "4437 scale/current zero."},
        {"source_id": "SRC4438_02_278_readout", "path": FORMAL_278, "needle": "C_Hodge_readout = 0", "role": "readout-after-variation zero."},
        {"source_id": "SRC4438_03_330_radiation", "path": FORMAL_330, "needle": "NF4314_3_closed_collar_zero", "role": "closed collar radiative zero."},
        {"source_id": "SRC4438_04_331_hodge", "path": FORMAL_331, "needle": "HT4315_3_readout_guard", "role": "same-Hodge/readout guard."},
        {"source_id": "SRC4438_05_345_rollup", "path": FORMAL_345, "needle": "RUN4329_0_standard_visible_closed_collar", "role": "same-Hodge closed-collar Dq_EM rollup."},
        {"source_id": "SRC4438_06_346_coeff", "path": FORMAL_346, "needle": "D_X ln g_J = D_X ln lambda_A = 0", "role": "fixed coefficient branch."},
        {"source_id": "SRC4438_07_3503_bound", "path": EM_BOUND3503, "needle": "EMB3503_5_C_EM_readout", "role": "readout coefficient survivor row."},
        {"source_id": "SRC4438_08_3502_poynting", "path": EM_POYNTING3502, "needle": "EMF3502_1_radiative_poynting_flux", "role": "radiative flux survivor row."},
        {"source_id": "SRC4438_09_3505_bound", "path": VEB3505, "needle": "VEB3505_5_C_Hodge_readout", "role": "readout Hodge branch guard."},
        {"source_id": "SRC4438_10_3465_owner", "path": OWNER3465, "needle": "EMO3465_4_readout_radiative", "role": "readout/radiative closure gap."},
        {"source_id": "SRC4438_11_kleg4437", "path": KLEG4437, "needle": "KLEG4437_0_EM_scale_current_branch_zero", "role": "previous K product zero."},
        {"source_id": "SRC4438_12_zero4437", "path": ZERO4437, "needle": "ZERO4437_0_C_XF2", "role": "previous branch zeros."},
        {"source_id": "SRC4438_13_surv4437", "path": SURV4437, "needle": "SURV4437_3_radiative_readout", "role": "previous survivor target."},
        {"source_id": "SRC4438_14_gate", "path": GATE_PATH, "needle": "def evaluate_em_closure_row", "role": "4438 gate script."},
        {"source_id": "SRC4438_15_generator", "path": GENERATOR_PATH, "needle": "CHECKPOINT = \"4438\"", "role": "4438 generator script."},
        {"source_id": "SRC4438_16_kleg_gate", "path": ACTION_EDGE_GATE, "needle": "def evaluate_k_source_leg_row", "role": "K source-leg evaluator."},
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
            "derivation_id": "RRC4438_0_total_fixed_branch_EM_zero",
            "claim": "The fixed q-basic same-Hodge closed-collar branch kills the remaining EM action-scale product.",
            "derivation": "4437 gives C_XF2=C_JQ=b_alpha=dlnlambda=0 for the fixed q-basic standard branch. 4315/4329 give Delta_Hodge_EM=C_Hodge_readout=0 when the same observed Hodge action is used and readout is post-variation. 4314 gives Phi_EM_rad=0 when P_rad_EM(tau)=0 pointwise on a fixed-orientation closed collar. Combining these clauses gives C_EM_total=0 for the local EM residual product in that branch.",
            "consequence": "K_m_EM_action_scale*C_EM_action_scale_total is DERIVED_ZERO only on the fixed q-basic same-Hodge static closed-collar branch.",
            "status": "TOTAL_FIXED_BRANCH_EM_ZERO_DERIVED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "RRC4438_1_readout_preservation",
            "claim": "Readout preservation is branch typing, not a loop calculation.",
            "derivation": "If clocks, spectroscopy and EM readout are postprocessing maps with no argument slot in S_parent or S_eff, then their variations do not source parent equations and cannot regenerate C_Hodge_readout, C_XF2 or b_alpha. If S_eff or readout maps acquire hidden-field arguments, the retained branch reopens.",
            "consequence": "The zero is legal for the fixed readout branch; dynamic EFT/readout regeneration remains a finite survivor.",
            "status": "READOUT_ZERO_WITH_COUNTERBRANCH",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "RRC4438_2_radiation_boundary_split",
            "claim": "Open radiation is not erased; it is routed to a boundary/source-energy row.",
            "derivation": "Closed-collar pointwise P_rad_EM=0 gives Delta_rad_Poynting=0. If P_rad_EM or E_rad_EM is nonzero, the contribution is N_boundary_rad_EM=|E_rad_EM|/(M_H c^2) or its power-normalized analogue, and feeds R_EM/Eta_H/S_U as a declared boundary term.",
            "consequence": "No hidden Poynting force and no deleted radiation: closed collars zero it, open collars need sourced values.",
            "status": "ZERO_OR_BOUNDARY_ROUTE_DERIVED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "RRC4438_3_scope_firewall",
            "claim": "The total EM zero is not a global local-GR or Maxwell claim.",
            "derivation": "The result depends on the standard visible branch, same-Hodge action, q-basic fixed coefficients, readout-after-variation discipline and a static closed collar. It does not predict alpha_EM, derive global Maxwell/QED, close non-EM residuals, or prove source-charge equality.",
            "consequence": "4439 should integrate this zero into the local residual vector while preserving source-charge, geometry, projection and open-branch debts.",
            "status": "PRIVATE_BRANCH_ZERO_PUBLIC_CLAIM_BLOCKED",
            "valid_for_claim": False,
        },
    ]


def em_closure_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "RRC4438_0_fixed_qbasic_samehodge_closed_collar",
            "branch": "fixed q-basic same-Hodge static closed-collar branch",
            "same_hodge_zero": True,
            "scale_current_zero": True,
            "readout_postprocess": True,
            "no_effective_action_reentry": True,
            "no_loop_hidden_argument": True,
            "closed_collar_pointwise_no_flux": True,
            "orientation_normal_fixed": True,
            "poynting_once_only": True,
            "open_flux_routed_to_boundary": True,
            "source_path": str(FORMAL_345),
            "input_valid": True,
            "valid_for_claim": False,
            "notes": "Total EM residual product zero in the private static fixed branch.",
        },
        {
            "row_id": "RRC4438_1_open_radiative_boundary_route",
            "branch": "open radiative collar branch",
            "same_hodge_zero": True,
            "scale_current_zero": True,
            "readout_postprocess": True,
            "no_effective_action_reentry": True,
            "no_loop_hidden_argument": True,
            "closed_collar_pointwise_no_flux": False,
            "orientation_normal_fixed": True,
            "poynting_once_only": True,
            "open_flux_routed_to_boundary": True,
            "source_path": str(FORMAL_330),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Open radiation is allowed only as a boundary flux/source-energy row.",
        },
        {
            "row_id": "RRC4438_2_effective_readout_regeneration",
            "branch": "effective/readout regenerated EM branch",
            "same_hodge_zero": True,
            "scale_current_zero": True,
            "readout_postprocess": False,
            "no_effective_action_reentry": False,
            "no_loop_hidden_argument": False,
            "closed_collar_pointwise_no_flux": True,
            "orientation_normal_fixed": True,
            "poynting_once_only": True,
            "open_flux_routed_to_boundary": True,
            "source_path": str(VEB3505),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "S_eff/readout hidden arguments regenerate C_EM_readout or coefficient response.",
        },
        {
            "row_id": "RRC4438_3_global_dynamic_EM_branch",
            "branch": "global/dynamic EM deformation branch",
            "same_hodge_zero": False,
            "scale_current_zero": False,
            "readout_postprocess": False,
            "no_effective_action_reentry": False,
            "no_loop_hidden_argument": False,
            "closed_collar_pointwise_no_flux": False,
            "orientation_normal_fixed": False,
            "poynting_once_only": True,
            "open_flux_routed_to_boundary": True,
            "source_path": str(OWNER3465),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Global EM generator/radiative closure remains unsigned.",
        },
    ]


def zero_rows() -> List[Dict[str, object]]:
    return [
        {"zero_id": "ZERO4438_0_total_EM_product", "symbol": "K_m_EM_action_scale*C_EM_action_scale_total", "zero_statement": "total fixed-branch EM residual product is zero", "branch_conditions": "fixed q-basic + same Hodge + post-variation readout + no S_eff hidden argument + closed collar P_rad_EM=0", "source_path": str(FORMAL_345), "status": "TOTAL_FIXED_BRANCH_ZERO", "valid_for_claim": False},
        {"zero_id": "ZERO4438_1_C_EM_readout", "symbol": "C_EM_readout", "zero_statement": "C_EM_readout=0", "branch_conditions": "readout is pure postprocessing and not an argument of S_parent/S_eff", "source_path": str(FORMAL_278), "status": "BRANCH_ZERO_WITH_COUNTERBRANCH", "valid_for_claim": False},
        {"zero_id": "ZERO4438_2_Phi_EM_rad", "symbol": "Phi_EM_rad", "zero_statement": "Phi_EM_rad=0", "branch_conditions": "P_rad_EM(tau)=0 pointwise on fixed-orientation closed collar", "source_path": str(FORMAL_330), "status": "CLOSED_COLLAR_ZERO", "valid_for_claim": False},
        {"zero_id": "ZERO4438_3_Delta_Hodge_EM", "symbol": "Delta_Hodge_EM", "zero_statement": "Delta_Hodge_EM=0", "branch_conditions": "same observed Hodge/action-domain with no independent constitutive/readout Hodge term", "source_path": str(FORMAL_331), "status": "SAME_HODGE_BRANCH_ZERO", "valid_for_claim": False},
    ]


def survivor_rows() -> List[Dict[str, object]]:
    return [
        {"survivor_id": "SURV4438_0_open_radiation", "symbol": "E_rad_EM or P_rad_EM", "why_survives": "open collars have nonzero EM flux and must be source-energy/boundary data", "needed_to_close": "source P_rad_EM/E_rad_EM over the test window or prove pointwise closed-collar zero", "source_path": str(FORMAL_330), "valid_for_claim": False},
        {"survivor_id": "SURV4438_1_readout_regeneration", "symbol": "C_EM_readout", "why_survives": "S_eff/readout hidden arguments can regenerate Hodge/alpha/EM binding response", "needed_to_close": "prove no hidden argument in readout/EFT map or source a bound", "source_path": str(VEB3505), "valid_for_claim": False},
        {"survivor_id": "SURV4438_2_global_dynamic_EM", "symbol": "global C_XF2/C_JQ/b_alpha", "why_survives": "global parent generator and dynamic coefficient branches remain unsigned", "needed_to_close": "parent typed EM generator or source-backed dynamic product rows", "source_path": str(OWNER3465), "valid_for_claim": False},
        {"survivor_id": "SURV4438_3_nonEM_local_residuals", "symbol": "source-charge/geometry/projection tails", "why_survives": "EM zero alone does not prove source-charge equality or all local residual components", "needed_to_close": NEXT_TARGET, "source_path": str(FORMAL_345), "valid_for_claim": False},
    ]


def kleg_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "KLEG4438_0_total_fixed_branch_EM_product_zero",
            "product": "K_m_EM_action_scale*C_EM_action_scale_total_fixed_branch",
            "coefficient_value": "DERIVED_ZERO",
            "units": "dimensionless",
            "parent_coefficient_source": str(FORMAL_345),
            "source_leg": "C_XF2=C_JQ=b_alpha=dlnlambda=C_EM_readout=Phi_EM_rad=Delta_Hodge_EM=0 in fixed q-basic same-Hodge closed-collar branch",
            "source_leg_units": "dimensionless_branch_zero",
            "projection": "total EM action-scale residual product vanishes inside the fixed same-Hodge closed-collar branch",
            "bound_value": "0",
            "no_bound_inversion_guard": True,
            "source_path": str(FORMAL_345),
            "input_valid": True,
            "valid_for_claim": False,
            "notes": "Total EM branch zero; not global Maxwell, not alpha prediction, not public local-GR claim.",
        },
        {
            "row_id": "KLEG4438_1_open_dynamic_total_EM_product_retained",
            "product": "K_m_EM_action_scale*C_EM_action_scale_open_dynamic",
            "coefficient_value": "MISSING_PARENT_COEFFICIENT",
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_OPEN_RADIATIVE_READOUT_OR_GLOBAL_EM_SOURCE",
            "source_leg": "MISSING_Erad_Pradiative_CEMreadout_OR_DYNAMIC_COEFFICIENT_SOURCE_LEG",
            "source_leg_units": "dimensionless_or_declared_parent_units",
            "projection": f"{DELTA_Q_MHAT:.5f}*abs(K_m_EM_action_scale*C_EM_action_scale_open_dynamic) <= {ETA_BOUND:.12e}",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "no_bound_inversion_guard": True,
            "source_path": str(KLEG4437),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Retained for open radiation, dynamic readout, or global EM deformation branches.",
        },
        {
            "row_id": "KLEG4438_2_boundary_flux_bound_target_only",
            "product": "K_m_EM_action_scale*C_EM_boundary_flux_effective",
            "coefficient_value": f"BOUND_ONLY_{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "units": "dimensionless",
            "parent_coefficient_source": "MISSING_BOUNDARY_FLUX_SOURCE",
            "source_leg": "MISSING_E_RAD_OR_P_RAD_SOURCE_LEG",
            "source_leg_units": "energy_fraction_or_power_fraction",
            "projection": "open radiation must use E_rad_EM/(M_H c^2) or P_rad_EM/(M_H c^2/DeltaTau), then compare to local bound",
            "bound_value": f"{D_MHAT_ONE_CHANNEL_CEILING:.12e}",
            "no_bound_inversion_guard": True,
            "source_path": str(FORMAL_330),
            "input_valid": False,
            "valid_for_claim": False,
            "notes": "Dimensional open-flux target only; no coefficient inferred from the bound.",
        },
    ]


def claim_gate_rows(em_rows: Sequence[Mapping[str, str]], klegs: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    closure_rows = {row["row_id"]: row for row in em_rows}
    kleg_rows = {row["row_id"]: row for row in klegs}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in em_rows) and not any(row.get("valid_for_claim") == "True" for row in klegs)
    return [
        {"gate_id": "CG4438_0_total_fixed_zero", "claim": "total fixed-branch EM residual zero", "passed": closure_rows["RRC4438_0_fixed_qbasic_samehodge_closed_collar"].get("current_status") == "TOTAL_FIXED_BRANCH_EM_ZERO_READY_NONCLAIM", "valid_for_claim": False, "detail": "Private branch zero only."},
        {"gate_id": "CG4438_1_total_K_zero", "claim": "total EM K product zero in fixed branch", "passed": kleg_rows["KLEG4438_0_total_fixed_branch_EM_product_zero"].get("current_status") == "K_ACTION_SOURCE_LEG_READY_NONCLAIM", "valid_for_claim": False, "detail": "No alpha/global claim."},
        {"gate_id": "CG4438_2_open_flux_retained", "claim": "open radiation routed to boundary row", "passed": closure_rows["RRC4438_1_open_radiative_boundary_route"].get("current_status") == "OPEN_RADIATIVE_BRANCH_ROUTED_BOUNDARY_VALUE_REQUIRED", "valid_for_claim": False, "detail": "Open flux needs E/P values."},
        {"gate_id": "CG4438_3_readout_counterbranch", "claim": "effective/readout regeneration retained", "passed": closure_rows["RRC4438_2_effective_readout_regeneration"].get("current_status") == "EM_READOUT_RADIATIVE_REGENERATION_OPEN", "valid_for_claim": False, "detail": "S_eff/readout hidden-argument branch remains physical."},
        {"gate_id": "CG4438_4_dynamic_product_retained", "claim": "dynamic/open EM product remains source-leg missing", "passed": kleg_rows["KLEG4438_1_open_dynamic_total_EM_product_retained"].get("current_status") == "K_ACTION_SOURCE_LEG_CONTRACT_ONLY", "valid_for_claim": False, "detail": "No bound inversion."},
        {"gate_id": "CG4438_5_survivors_retained", "claim": "non-EM/source-charge survivors retained", "passed": len(survivor_rows()) == 4 and "SURV4438_3_nonEM_local_residuals" in text(SURVIVOR_ROWS), "valid_for_claim": False, "detail": "EM zero not promoted to local-GR pass."},
        {"gate_id": "CG4438_6_no_public_claim", "claim": "4438 emits no local-GR/Maxwell/R10 public claim", "passed": no_claims, "valid_for_claim": False, "detail": "Private branch progress only."},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4438_0",
            "decision": DECISION,
            "summary": "4438 fuses the 4437 EM scale/current zero with same-Hodge/readout and closed-collar radiation gates. In the fixed q-basic same-Hodge static closed-collar branch, C_XF2, C_JQ, b_alpha, dlnlambda, C_EM_readout, Phi_EM_rad and Delta_Hodge_EM vanish, so the total EM action-scale residual product is DERIVED_ZERO. Open radiation, effective/readout regeneration and global/dynamic EM branches remain explicit nonclaim source-leg rows.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4438_0_total_EM", "status": "TOTAL_FIXED_BRANCH_EM_PRODUCT_ZERO", "detail": "All named EM scale/current/Hodge/readout/radiation pieces are zero in the fixed same-Hodge closed-collar branch.", "valid_for_claim": False},
        {"status_id": "STAT4438_1_open", "status": "OPEN_RADIATIVE_DYNAMIC_BRANCHES_RETAINED", "detail": "Open Poynting flux and S_eff/readout hidden arguments still need source-backed values.", "valid_for_claim": False},
        {"status_id": "STAT4438_2_next", "status": "INTEGRATE_EM_ZERO_INTO_LOCAL_RESIDUAL_VECTOR_NEXT", "detail": "Next step should remove the EM tail from the fixed-branch local residual vector while preserving non-EM/source-charge tails.", "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4438_0",
            "target": NEXT_TARGET,
            "objective": "Integrate the fixed-branch total EM zero into the local residual vector, while retaining source-charge, geometry, projection and open-branch tails.",
            "derive_first": "subtract the fixed-branch EM residual from the local R_EM/Eta_H/S_U or equivalent source-coupling vector and show which non-EM terms still block local GR/Newton/PPN.",
            "fallback": "if integration reveals hidden dependencies, keep the total EM zero as a branch component and write explicit remaining tail products.",
            "avoid": "claiming local GR from EM closure alone; deleting open-radiation/dynamic-readout rows; using branch-zero outside its static closed-collar domain.",
            "valid_for_claim": False,
        }
    ]


def build_doc(
    sources: Sequence[Mapping[str, object]],
    closures: Sequence[Mapping[str, str]],
    klegs: Sequence[Mapping[str, str]],
    gates: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 454 PPC4161 radiative-readout EM closure or total Kmactionscale source value

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4438 closes the fixed-branch EM tail:

- 4437 gives `C_XF2=C_JQ=b_alpha=dlnlambda=0`.
- Same-Hodge/readout discipline gives `Delta_Hodge_EM=0` and `C_EM_readout=0`.
- Static closed-collar radiation gives `Phi_EM_rad=0`.
- Therefore the total EM residual product `K_m_EM_action_scale*C_EM_action_scale_total_fixed_branch` is `DERIVED_ZERO` in the fixed q-basic same-Hodge closed-collar branch.
- Open radiation, effective/readout regeneration and global/dynamic EM branches are retained as explicit source-leg/boundary rows.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Radiative / Readout EM Closure Gate

{table(closures)}

## Total EM Zero Rows

{table(zero_rows())}

## Open EM Survivor Rows

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
    return f"""# 4438 - radiative-readout EM closure or total Kmactionscale source value

Marker: `{MARKER}`

Private checkpoint generated at `{STAMP}`.

## What changed

- Fused 4437 scale/current zero with same-Hodge/readout and closed-collar radiation gates.
- Set total fixed-branch `K_m_EM_action_scale*C_EM_action_scale_total` to `DERIVED_ZERO`.
- Retained open radiation, S_eff/readout regeneration, and global/dynamic EM deformation rows.
- Selected integration into the local residual vector as the next target.

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
        "claim": "4438 closes the total EM action-scale residual product in the fixed q-basic same-Hodge static closed-collar branch: C_XF2, C_JQ, b_alpha, dlnlambda, C_EM_readout, Phi_EM_rad and Delta_Hodge_EM vanish there, so K_m_EM_action_scale*C_EM_action_scale_total is DERIVED_ZERO. Open radiation, readout/EFT regeneration and global/dynamic EM branches remain nonclaim source-leg rows.",
        "current_evidence": "4438 source register, derivation rows, radiative/readout EM closure gate, total EM zero rows, survivor rows, K source-leg rows, claim gates, decision, status, next target and validation CSV.",
        "status": "total_fixed_branch_EM_product_zero_open_dynamic_branches_retained_nonclaim",
        "next_test": "Integrate fixed-branch EM zero into the local residual vector while preserving source-charge/non-EM tails.",
        "key_risk": "Claiming local GR from EM closure alone; deleting open radiation; using static closed-collar branch outside domain.",
        "sector": "em_local_gr",
        "evidence": "4438 source register, derivation rows, radiative/readout EM closure gate, total EM zero rows, survivor rows, K source-leg rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Integrate fixed-branch EM zero into the local residual vector while preserving source-charge/non-EM tails.",
        "risk": "Claiming local GR from EM closure alone; deleting open radiation; using static closed-collar branch outside domain.",
    }
    rows.append({fieldname: new_row.get(fieldname, "") for fieldname in fieldnames})
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_spine_and_packet() -> None:
    spine_section = """## 4438 local spine update: total fixed-branch EM product zero

4438 fuses the EM pieces into one fixed-branch result. In the fixed q-basic same-Hodge static closed-collar branch, scale/current drift, Hodge/readout mismatch and radiative Poynting flux are all zero, so the total EM action-scale residual product is `DERIVED_ZERO`. This is not a public local-GR pass: open radiation, readout/EFT regeneration, global/dynamic EM branches and non-EM source-charge/projection tails remain.
"""
    packet_section = f"""## 4438 packet update: EM tail removed from fixed branch

`{PACKET_MARKER}`

Private packet result: remove the EM residual product from the fixed q-basic same-Hodge closed-collar branch. Next, integrate that deletion into the local residual vector and expose exactly which non-EM/source-charge terms still block local GR/Newton/PPN.
"""
    upsert_marked_section(SPINE_PATH, MARKER, spine_section)
    upsert_marked_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    closures = {row["row_id"]: row for row in rows_from(EM_CLOSURE_OUTPUT)}
    klegs = {row["row_id"]: row for row in rows_from(KLEG_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in closures.values()) and not any(row.get("valid_for_claim") == "True" for row in klegs.values())
    checks = [
        ("VAL4438_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4438_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4438_2_total_fixed_zero", closures["RRC4438_0_fixed_qbasic_samehodge_closed_collar"].get("current_status") == "TOTAL_FIXED_BRANCH_EM_ZERO_READY_NONCLAIM", "fixed branch total EM zero ready"),
        ("VAL4438_3_open_flux_route", closures["RRC4438_1_open_radiative_boundary_route"].get("current_status") == "OPEN_RADIATIVE_BRANCH_ROUTED_BOUNDARY_VALUE_REQUIRED", "open radiation routed to boundary value"),
        ("VAL4438_4_readout_counterbranch", closures["RRC4438_2_effective_readout_regeneration"].get("current_status") == "EM_READOUT_RADIATIVE_REGENERATION_OPEN", "readout regeneration retained"),
        ("VAL4438_5_zero_rows", len(rows_from(ZERO_ROWS)) == 4 and "ZERO4438_0_total_EM_product" in text(ZERO_ROWS), "total EM zero rows written"),
        ("VAL4438_6_survivor_rows", len(rows_from(SURVIVOR_ROWS)) == 4 and "SURV4438_3_nonEM_local_residuals" in text(SURVIVOR_ROWS), "survivor rows written"),
        ("VAL4438_7_kleg_zero", klegs["KLEG4438_0_total_fixed_branch_EM_product_zero"].get("current_status") == "K_ACTION_SOURCE_LEG_READY_NONCLAIM", "total K EM branch zero"),
        ("VAL4438_8_kleg_dynamic", klegs["KLEG4438_1_open_dynamic_total_EM_product_retained"].get("current_status") == "K_ACTION_SOURCE_LEG_CONTRACT_ONLY", "open/dynamic product retained"),
        ("VAL4438_9_bound_only", klegs["KLEG4438_2_boundary_flux_bound_target_only"].get("current_status") == "K_ACTION_SOURCE_LEG_BOUND_TARGET_ONLY", "boundary flux bound target requires source leg"),
        ("VAL4438_10_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4438_11_claim_gate_no_claim", any(row["gate_id"] == "CG4438_6_no_public_claim" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4438_12_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-279"),
        ("VAL4438_13_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4438_14_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4438_15_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4438_16_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4438_17_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4438_18_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(EM_CLOSURE_INPUT, em_closure_input_rows())
    write_csv(EM_CLOSURE_OUTPUT, evaluate_em_closure_rows(EM_CLOSURE_INPUT))
    write_csv(ZERO_ROWS, zero_rows())
    write_csv(SURVIVOR_ROWS, survivor_rows())
    write_csv(KLEG_INPUT, kleg_input_rows())
    write_csv(KLEG_OUTPUT, evaluate_k_source_leg_rows(KLEG_INPUT))
    closures = rows_from(EM_CLOSURE_OUTPUT)
    klegs = rows_from(KLEG_OUTPUT)
    gates = claim_gate_rows(closures, klegs)
    write_csv(CLAIM_GATES, gates)
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), closures, klegs, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()
