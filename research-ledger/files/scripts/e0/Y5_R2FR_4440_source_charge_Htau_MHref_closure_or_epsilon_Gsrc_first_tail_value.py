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

from source_charge_closure_gate import evaluate_source_charge_rows, evaluate_tail_bound_rows, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4440"
CLAIM_ID = "L-281"
MARKER = "PPC4161_SOURCE_CHARGE_HTAU_MHREF_CLOSURE_OR_EPSILON_GSRC_TAIL_4440"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_CHARGE_HTAU_MHREF_EPSILON_GSRC_TAIL_4440"
DECISION = "EPSILON_GSRC_REDUCED_TO_SOURCE_CHARGE_ACTION_MEASURE_CURRENT_CONTRACT_FIRST_TAIL_RUNNER_READY_NONCLAIM"
NEXT_TARGET = "4441-Y5-R2FR-action-measure-current-owner-contract-after-EM-zero-or-Req-tail-values.md"

FORMAL_PATH = FORMAL / "456-PPC4161-source-charge-Htau-MHref-closure-or-epsilon-Gsrc-first-tail-value.md"
DOC_PATH = POST / "4440-Y5-R2FR-source-charge-Htau-MHref-closure-or-epsilon-Gsrc-first-tail-value.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4440_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4440_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4440_DERIVATION_ROWS.csv"
SOURCE_CLOSURE_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4440_SOURCE_CHARGE_CLOSURE_INPUT.csv"
SOURCE_CLOSURE_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4440_SOURCE_CHARGE_CLOSURE_OUTPUT.csv"
TAIL_BOUND_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4440_EPSILON_GSRC_TAIL_BOUND_INPUT.csv"
TAIL_BOUND_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4440_EPSILON_GSRC_TAIL_BOUND_OUTPUT.csv"
REDUCED_CONTRACT_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4440_REDUCED_CONTRACT_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4440_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4440_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4440_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4440_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "source_charge_closure_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4440_source_charge_Htau_MHref_closure_or_epsilon_Gsrc_first_tail_value.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4439 = SOURCE_DIR / "P8_Y5_R2FR_4439_NEXT_TARGET.csv"
FORMAL_455 = FORMAL / "455-PPC4161-integrate-fixed-branch-EM-zero-into-local-residual-vector-or-source-charge-tail.md"
FORMAL_370 = FORMAL / "370-PPC4161-Htau-MHref-source-charge-owner-or-finite-GN-drift-bound.md"
FORMAL_422 = FORMAL / "422-PPC4161-transition-source-charge-coupling-gate-import-or-epsilonGsrc-bound-runner.md"
FORMAL_435 = FORMAL / "435-PPC4161-transition-NoSourceOnlySpeciesSlot-or-topological-mass-current-origin.md"
FORMAL_443 = FORMAL / "443-PPC4161-total-Hilbert-source-owner-no-source-weight-signature-or-TiPt-DD-map.md"
FORMAL_4430 = FORMAL / "4430-PPC4161-total-Hilbert-source-owner-no-source-weight-signature-or-TiPt-DD-map.md"
POST_4430_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4430_DECISION.csv"
POST_4406_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4406_SOURCE_BRIDGE_OUTPUT.csv"
POST_4406_EPERP = SOURCE_DIR / "P8_Y5_R2FR_4406_EPERP_BOUND_OUTPUT.csv"
POST_4438_KLEG = SOURCE_DIR / "P8_Y5_R2FR_4438_K_ACTION_SOURCE_LEG_OUTPUT.csv"
POST_4439_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4439_LOCAL_RESIDUAL_VECTOR_AFTER_EM.csv"

K_N_NEWTON = 0.00943177578696
DELTA_N_SMOKE = 1.0e-5
SMALL_EPSILON_SMOKE = 5.0e-7
FAIL_EPSILON_SMOKE = 2.0e-3


def first_existing(*paths: Path) -> Path:
    for path in paths:
        if path.exists():
            return path
    return paths[0]


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
    source_4430 = first_existing(FORMAL_4430, POST_4430_DECISION)
    return [
        {"source_id": "SRC4440_00_4439_next", "path": NEXT_4439, "needle": "source-charge-Htau-MHref", "role": "4439 handoff into source-charge/coupling."},
        {"source_id": "SRC4440_01_455_vector", "path": FORMAL_455, "needle": "Delta_local_fixed_after_EM", "role": "4439 reduced local residual vector."},
        {"source_id": "SRC4440_02_370_epsilon", "path": FORMAL_370, "needle": "epsilon_Gsrc <=", "role": "4354 source/coupling no-cancellation envelope."},
        {"source_id": "SRC4440_03_370_theorem", "path": FORMAL_370, "needle": "NB4354_4_conditional_theorem", "role": "conditional local Newton/GR source theorem."},
        {"source_id": "SRC4440_04_422_perp", "path": FORMAL_422, "needle": "epsilon_Gsrc_perp = epsilon_Gsrc - epsilon_bar_H", "role": "4406 calibrated common-mode subtraction."},
        {"source_id": "SRC4440_05_422_runner", "path": FORMAL_422, "needle": "E_perp <= E_measure + E_mass + E_transition + E_Xi + E_T", "role": "4406 executable finite Eperp runner."},
        {"source_id": "SRC4440_06_435_contract", "path": FORMAL_435, "needle": "JNT4419_0_joint_source_newton_gate", "role": "4419 action-measure/current contract."},
        {"source_id": "SRC4440_07_4430_signature", "path": source_4430, "needle": "TOTAL_HILBERT_SOURCE_ZERO_SIGNATURE_EXACT", "role": "4430 total Hilbert source zero signature."},
        {"source_id": "SRC4440_08_4406_bridge", "path": POST_4406_SOURCE, "needle": "SB4406_0_current_integrated_bridge_profile_open", "role": "4406 bridge output current state."},
        {"source_id": "SRC4440_09_4406_eperp", "path": POST_4406_EPERP, "needle": "EG4406_2_small_component_pass_smoke", "role": "4406 Eperp smoke/fail controls."},
        {"source_id": "SRC4440_10_4438_kleg", "path": POST_4438_KLEG, "needle": "KLEG4438_0_total_fixed_branch_EM_product_zero", "role": "fixed EM source-leg zero."},
        {"source_id": "SRC4440_11_4439_vector_csv", "path": POST_4439_VECTOR, "needle": "RV4439_0_fixed_clean_private_after_EM", "role": "machine-readable reduced residual vector."},
        {"source_id": "SRC4440_12_gate", "path": GATE_PATH, "needle": "def evaluate_source_charge_row", "role": "4440 source-charge/tail gate."},
        {"source_id": "SRC4440_13_generator", "path": GENERATOR_PATH, "needle": "CHECKPOINT = \"4440\"", "role": "4440 generator script."},
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
            "derivation_id": "SC4440_0_common_mode_split",
            "claim": "The calibrated common Hilbert-source monopole is not the physical source-coupling residual.",
            "derivation": "Write epsilon_Gsrc = epsilon_bar_H + epsilon_Gsrc_perp. The common Hilbert-source part epsilon_bar_H rescales the calibrated G_cal and is fair GR-style calibration. Local tests must score the noncommon/profile component epsilon_Gsrc_perp.",
            "consequence": "The live finite object is epsilon_Gsrc_perp, not a demand that MTS predicts the numerical value of G_N.",
            "status": "COMMON_MODE_REMOVED_FROM_PHYSICAL_TAIL",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SC4440_1_structural_newton_bridge",
            "claim": "The clean branch has the right GR/Newton source law if the source-charge clauses close on one branch.",
            "derivation": "If D_A ln kappa_eff=0, rho_eff=rho_H on the same worldtube, M_H^dress=H_tau-H_ref, H_tau is integrable, H_ref/tau/frame/boundary/MHref are locked, and the action-measure/current owner gives R_eq=0, then G_munu[g_obs]=kappa_eff T_H_munu+residual_munu reduces weakly to nabla^2 Phi_N=4*pi G_cal rho_H and a=-G_cal M_H^dress/r^2.",
            "consequence": "This is the exact source-charge theorem target; observed orbital GM is not used as source input.",
            "status": "CONDITIONAL_GR_NEWTON_BRIDGE_EXPLICIT",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SC4440_2_after_EM_integration",
            "claim": "The fixed EM action-scale tail no longer belongs in epsilon_Gsrc for the fixed clean branch.",
            "derivation": "4438 gives K_m_EM_action_scale*C_EM_action_scale_total_fixed_branch=0 and 4439 subtracts Delta_EM_fixed from the local residual vector. Therefore the remaining source-charge task is not the fixed EM throat, but H_tau/MHref, action-measure/current ownership, R_eq/B_zero/profile equality and projection tails.",
            "consequence": "The coupling gap is now sharper and less foggy: source-charge/action-measure/current, not generic EM coupling.",
            "status": "FIXED_EM_REMOVED_FROM_SOURCE_COUPLING_TAIL",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SC4440_3_first_tail_runner",
            "claim": "If the clean proof is not closed, the finite branch is scoreable as a no-cancellation component sum.",
            "derivation": "Use E_perp <= E_measure + E_mass + E_transition + E_Xi + E_T and project by arena coefficients. The first executable row is |delta a|/|a_N| <= K_N(s) E_perp; R10, PPN, clock and orbital rows are now explicit contract rows requiring real projection coefficients and bounds.",
            "consequence": "No more vague missing coupling: the live finite tail is a row schema with component values, projections, arena bounds and no-bound-inversion guards.",
            "status": "FINITE_TAIL_RUNNER_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def source_closure_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "SC4440_0_current_after_EM_zero",
            "branch": "current fixed-clean branch after 4439 EM deletion",
            "source_blind_kappa_eff": True,
            "same_worldtube": True,
            "Htau_MHref_defined": True,
            "PiH_glue_private": True,
            "Htau_integrable": False,
            "Href_fixed": False,
            "same_tau_frame_surface": False,
            "boundary_flux_routed": False,
            "MHref_positive": False,
            "anti_circularity": True,
            "action_measure_owner": False,
            "same_current_Req_zero": False,
            "fixed_EM_zero_integrated": True,
            "source_path": str(FORMAL_455),
            "public_authority": False,
            "input_valid_for_claim": False,
        },
        {
            "row_id": "SC4440_1_future_full_private_source_charge",
            "branch": "future same-branch Htau/MHref/action-measure clean branch",
            "source_blind_kappa_eff": True,
            "same_worldtube": True,
            "Htau_MHref_defined": True,
            "PiH_glue_private": True,
            "Htau_integrable": True,
            "Href_fixed": True,
            "same_tau_frame_surface": True,
            "boundary_flux_routed": True,
            "MHref_positive": True,
            "anti_circularity": True,
            "action_measure_owner": True,
            "same_current_Req_zero": True,
            "fixed_EM_zero_integrated": True,
            "source_path": str(FORMAL_435),
            "public_authority": False,
            "input_valid_for_claim": False,
        },
        {
            "row_id": "SC4440_2_public_or_raw_branch",
            "branch": "public/global or raw unselected branch",
            "source_blind_kappa_eff": False,
            "same_worldtube": False,
            "Htau_MHref_defined": True,
            "PiH_glue_private": False,
            "Htau_integrable": False,
            "Href_fixed": False,
            "same_tau_frame_surface": False,
            "boundary_flux_routed": False,
            "MHref_positive": False,
            "anti_circularity": True,
            "action_measure_owner": False,
            "same_current_Req_zero": False,
            "fixed_EM_zero_integrated": False,
            "source_path": str(FORMAL_370),
            "public_authority": False,
            "input_valid_for_claim": False,
        },
    ]


def tail_bound_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "tail_id": "TAIL4440_0_newton_source_live_contract",
            "arena": "Newton_source_normalization",
            "residual_symbol": "epsilon_Gsrc_perp",
            "projection_law": "|delta a|/|a_N| <= K_N(s) E_perp",
            "projection_coeff": f"{K_N_NEWTON:.12g}",
            "epsilon_component_value": "MISSING_EPERP_COMPONENT_SUM",
            "arena_bound": f"{DELTA_N_SMOKE:.12g}",
            "units": "dimensionless",
            "source_path": str(FORMAL_422),
            "input_valid_for_claim": False,
        },
        {
            "tail_id": "TAIL4440_1_newton_zero_smoke",
            "arena": "Newton_source_normalization",
            "residual_symbol": "epsilon_Gsrc_perp",
            "projection_law": "|delta a|/|a_N| <= K_N(s) E_perp",
            "projection_coeff": f"{K_N_NEWTON:.12g}",
            "epsilon_component_value": "0",
            "arena_bound": f"{DELTA_N_SMOKE:.12g}",
            "units": "dimensionless",
            "source_path": str(POST_4406_EPERP),
            "input_valid_for_claim": False,
        },
        {
            "tail_id": "TAIL4440_2_newton_small_smoke",
            "arena": "Newton_source_normalization",
            "residual_symbol": "epsilon_Gsrc_perp",
            "projection_law": "|delta a|/|a_N| <= K_N(s) E_perp",
            "projection_coeff": f"{K_N_NEWTON:.12g}",
            "epsilon_component_value": f"{SMALL_EPSILON_SMOKE:.12g}",
            "arena_bound": f"{DELTA_N_SMOKE:.12g}",
            "units": "dimensionless",
            "source_path": str(POST_4406_EPERP),
            "input_valid_for_claim": False,
        },
        {
            "tail_id": "TAIL4440_3_newton_fail_control",
            "arena": "Newton_source_normalization",
            "residual_symbol": "epsilon_Gsrc_perp",
            "projection_law": "|delta a|/|a_N| <= K_N(s) E_perp",
            "projection_coeff": f"{K_N_NEWTON:.12g}",
            "epsilon_component_value": f"{FAIL_EPSILON_SMOKE:.12g}",
            "arena_bound": f"{DELTA_N_SMOKE:.12g}",
            "units": "dimensionless",
            "source_path": str(POST_4406_EPERP),
            "input_valid_for_claim": False,
        },
        {
            "tail_id": "TAIL4440_4_R10_contract",
            "arena": "R10_short_range",
            "residual_symbol": "alpha_src(lambda)",
            "projection_law": "alpha_src(lambda) = P_R10(lambda) epsilon_Gsrc_perp",
            "projection_coeff": "MISSING_P_R10_LAMBDA",
            "epsilon_component_value": "MISSING_EPERP_COMPONENT_SUM",
            "arena_bound": "MISSING_ALPHA_BOUND_LAMBDA",
            "units": "dimensionless",
            "source_path": str(FORMAL_370),
            "input_valid_for_claim": False,
        },
        {
            "tail_id": "TAIL4440_5_PPN_contract",
            "arena": "PPN_solar_system",
            "residual_symbol": "delta_gamma_beta_alpha_i",
            "projection_law": "delta_PPN = P_PPN epsilon_Gsrc_perp + other explicit residuals",
            "projection_coeff": "MISSING_P_PPN",
            "epsilon_component_value": "MISSING_EPERP_COMPONENT_SUM",
            "arena_bound": "MISSING_PPN_BOUND_VECTOR",
            "units": "dimensionless",
            "source_path": str(FORMAL_370),
            "input_valid_for_claim": False,
        },
        {
            "tail_id": "TAIL4440_6_clock_contract",
            "arena": "clock_redshift_Gdot",
            "residual_symbol": "delta_clock_or_Gdot_over_G",
            "projection_law": "delta_clock = P_clock epsilon_Gsrc_perp + tau/frame leakage",
            "projection_coeff": "MISSING_P_CLOCK",
            "epsilon_component_value": "MISSING_EPERP_COMPONENT_SUM",
            "arena_bound": "MISSING_CLOCK_BOUND",
            "units": "dimensionless_or_per_time_declared",
            "source_path": str(FORMAL_370),
            "input_valid_for_claim": False,
        },
        {
            "tail_id": "TAIL4440_7_orbital_contract",
            "arena": "orbital_GM",
            "residual_symbol": "delta_GM_orbit",
            "projection_law": "delta_GM/GM = P_orbit epsilon_Gsrc_perp + Href/MHref/boundary residuals",
            "projection_coeff": "MISSING_P_ORBIT",
            "epsilon_component_value": "MISSING_EPERP_COMPONENT_SUM",
            "arena_bound": "MISSING_ORBITAL_BOUND",
            "units": "dimensionless",
            "source_path": str(FORMAL_370),
            "input_valid_for_claim": False,
        },
    ]


def reduced_contract_rows() -> List[Dict[str, object]]:
    return [
        {"contract_id": "RC4440_0_clean_source_law", "object": "local Newton/GR source law", "reduced_to": "source_blind_kappa_eff + same H_tau/MHref source charge + action_measure_owner + same_current_Req_zero + fixed_EM_zero_integrated", "current_state": "CORE_PARTLY_CLOSED_CONTRACT_OPEN", "source_path": str(FORMAL_370), "valid_for_claim": False},
        {"contract_id": "RC4440_1_physical_tail", "object": "epsilon_Gsrc_perp", "reduced_to": "E_measure + E_mass + E_transition + E_Xi + E_T after common-mode calibration subtraction", "current_state": "EXECUTABLE_TAIL_RUNNER_READY_VALUES_MISSING", "source_path": str(FORMAL_422), "valid_for_claim": False},
        {"contract_id": "RC4440_2_source_owner", "object": "NoSourceOnlySpeciesSlot/action-measure/current owner", "reduced_to": "one Hilbert-source action line, universal hbar/measure/action density, no active source Hom, same topological/Hamiltonian current", "current_state": "EXACT_CONDITIONAL_PARENT_SIGNATURE_OPEN", "source_path": str(FORMAL_435), "valid_for_claim": False},
        {"contract_id": "RC4440_3_fixed_EM", "object": "fixed EM source/action-scale tail", "reduced_to": "deleted from fixed clean branch; open EM retained elsewhere", "current_state": "FIXED_BRANCH_ZERO_IMPORTED", "source_path": str(FORMAL_455), "valid_for_claim": False},
    ]


def claim_gate_rows(source_outputs: Sequence[Mapping[str, str]], tail_outputs: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    source_by_id = {row["row_id"]: row for row in source_outputs}
    tail_by_id = {row["tail_id"]: row for row in tail_outputs}
    no_claims = not any(row.get("valid_for_claim") == "True" for row in source_outputs) and not any(row.get("valid_for_claim") == "True" for row in tail_outputs)
    return [
        {"gate_id": "CG4440_0_sources_exist", "claim": "all cited source paths exist", "passed": all(row["path_exists"] == "True" for row in rows_from(SOURCE_REGISTER)), "valid_for_claim": False, "detail": "Source register is path-backed."},
        {"gate_id": "CG4440_1_needles_found", "claim": "all cited source needles found", "passed": all(row["needle_found"] == "True" for row in rows_from(SOURCE_REGISTER)), "valid_for_claim": False, "detail": "No vibe-only source import."},
        {"gate_id": "CG4440_2_contract_reduction", "claim": "current source charge reduced to action-measure/current contract", "passed": source_by_id["SC4440_0_current_after_EM_zero"].get("current_status") == "SOURCE_CHARGE_REDUCED_TO_ACTION_MEASURE_CURRENT_CONTRACT", "valid_for_claim": False, "detail": "Core fixed branch sharpened but clauses remain open."},
        {"gate_id": "CG4440_3_common_mode_split", "claim": "epsilon_Gsrc_perp used as physical tail", "passed": "epsilon_Gsrc_perp" in text(DERIVATION_ROWS), "valid_for_claim": False, "detail": "Common calibrated source mode separated from physical residual."},
        {"gate_id": "CG4440_4_tail_runner_controls", "claim": "tail runner has pass and fail controls", "passed": tail_by_id["TAIL4440_2_newton_small_smoke"].get("current_status") == "EPSILON_GSRC_TAIL_SCHEMA_PASS_NONCLAIM" and tail_by_id["TAIL4440_3_newton_fail_control"].get("current_status") == "EPSILON_GSRC_TAIL_FAILS_BOUND", "valid_for_claim": False, "detail": "Schema catches both safe-smoke and fail-control rows."},
        {"gate_id": "CG4440_5_arena_contracts", "claim": "R10/PPN/clock/orbital tail contracts written", "passed": all(key in text(TAIL_BOUND_OUTPUT) for key in ("TAIL4440_4_R10_contract", "TAIL4440_5_PPN_contract", "TAIL4440_6_clock_contract", "TAIL4440_7_orbital_contract")), "valid_for_claim": False, "detail": "Arena rows exist but require projection values and bounds."},
        {"gate_id": "CG4440_6_no_public_claim", "claim": "4440 emits no local-GR/Newton/PPN public claim", "passed": no_claims, "valid_for_claim": False, "detail": "Every output row remains nonclaim."},
        {"gate_id": "CG4440_7_next_target_written", "claim": "next target selected", "passed": NEXT_TARGET in text(NEXT_CSV), "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4440_0",
            "decision": DECISION,
            "summary": "4440 does the source-coupling cleanup after the fixed EM tail deletion. The clean GR/Newton source route is now an exact branch contract: source-blind kappa_eff, same H_tau/MHref charge, action-measure/current ownership, same-current R_eq zero, and the already-integrated fixed EM zero. The common Hilbert-source mode is calibration, so the physical finite tail is epsilon_Gsrc_perp. Current MTS still lacks action-measure owner, same-current R_eq/B_zero, H_tau integrability/reference/tau/boundary/MHref closure and real arena projections, but the first finite tail runner is now explicit for Newton/R10/PPN/clock/orbital rows.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "public_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {"status_id": "STAT4440_0_source_law", "object": "local source law", "status": "CONDITIONAL_CONTRACT_EXPLICIT", "detail": "Fair GR-like calibrated G plus Hamiltonian/Hilbert source mass; no numeric G prediction required.", "valid_for_claim": False},
        {"status_id": "STAT4440_1_epsilon", "object": "epsilon_Gsrc_perp", "status": "FIRST_TAIL_RUNNER_READY_VALUES_MISSING", "detail": "Component/projection rows are executable but live values are not claim-grade.", "valid_for_claim": False},
        {"status_id": "STAT4440_2_fixed_EM", "object": "fixed EM action-scale tail", "status": "REMOVED_FROM_FIXED_SOURCE_TAIL", "detail": "Open/dynamic EM remains outside branch.", "valid_for_claim": False},
        {"status_id": "STAT4440_3_next", "object": "next target", "status": "ACTION_MEASURE_CURRENT_OWNER_CONTRACT", "detail": NEXT_TARGET, "valid_for_claim": False},
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4440_0",
            "target": NEXT_TARGET,
            "objective": "Prove the action-measure/current owner contract after fixed EM deletion, or fill R_eq/B_zero/Delta_w/tau/source-profile tail values.",
            "derive_first": "show one parent action-measure/current owner makes ordinary matter a single Hilbert-source object and locks the topological/Hamiltonian current distributionally to Pi_M J_H on the same worldtube",
            "fallback": "fill first finite R_eq compact-test/multipole moment, B_zero_flux, Delta_w/tau_WEP, MHref or arena projection rows with values, units and source paths",
            "avoid": "using observed GM or comparator bounds as source definitions; treating total mass as profile equality; claiming local GR from the conditional source law alone",
            "valid_for_claim": False,
        }
    ]


def build_doc(
    sources: Sequence[Mapping[str, object]],
    source_outputs: Sequence[Mapping[str, object]],
    tail_outputs: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 456 PPC4161 source charge Htau MHref closure or epsilon Gsrc first tail value

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4440 narrows the coupling problem rather than just naming it.

```text
Delta_local_fixed_after_EM
  = epsilon_Gsrc
  + epsilon_geom_projection
  + epsilon_nonEH
  + epsilon_parent_selector
  + epsilon_empirical

epsilon_Gsrc = epsilon_bar_H + epsilon_Gsrc_perp
epsilon_bar_H -> calibrated common G_cal mode
epsilon_Gsrc_perp <= E_measure + E_mass + E_transition + E_Xi + E_T
```

So the physical source-coupling debt is no longer generic. It is:

```text
source_blind_kappa_eff
+ same H_tau/MHref source charge
+ action_measure_owner
+ same_current_R_eq_zero
+ fixed_EM_zero_integrated
```

The fixed EM piece is already integrated by 4439. The live hard contract is action-measure/current ownership plus H_tau/MHref same-branch closure and real finite-tail values.

## Source Register

{table(sources)}

## Derivation Rows

{table(derivation_rows())}

## Source Charge Closure Gate

{table(source_outputs)}

## Epsilon Gsrc Tail Bound Gate

{table(tail_outputs)}

## Reduced Contract Rows

{table(reduced_contract_rows())}

## Claim Gates

{table(gates)}

## Decision

{table(decision_rows())}

## Status

{table(status_rows())}

## Next Target

{table(next_rows())}
"""


def post_doc() -> str:
    return f"""# 4440 Y5 R2FR source charge Htau MHref closure or epsilon Gsrc first tail value

Private checkpoint generated at `{STAMP}`.

Formal mirror: `{FORMAL_PATH}`

Decision: `{DECISION}`

Summary:
- Common calibrated source mode is split away from the physical source tail.
- Current fixed clean branch reduces to the action-measure/current owner contract plus H_tau/MHref same-branch locks.
- First finite `epsilon_Gsrc_perp` tail rows are executable for Newton/R10/PPN/clock/orbital arenas but remain nonclaim until values/projections are sourced.

Next target: `{NEXT_TARGET}`
"""


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH)
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
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_source_coupling",
        "claim": "4440 reduces epsilon_Gsrc after the fixed EM zero: the common Hilbert-source mode is calibration, the physical tail is epsilon_Gsrc_perp, and the clean source law is now an explicit action-measure/current plus H_tau/MHref contract. First finite Newton/R10/PPN/clock/orbital tail rows are executable but nonclaim.",
        "current_evidence": "4440 source register, derivation rows, source charge closure gate, epsilon_Gsrc tail bound gate, reduced contract rows, claim gates, decision, status, next target and validation CSV.",
        "status": "epsilon_Gsrc_reduced_to_action_measure_current_contract_first_tail_runner_nonclaim",
        "next_test": "Prove action-measure/current owner and same-current R_eq zero, or fill first finite R_eq/B_zero/Delta_w/tau/source-profile tail values.",
        "key_risk": "Using observed GM as source input; treating common G calibration as source-coupling evidence; claiming local GR before H_tau/MHref and projection tails close.",
        "sector": "local_gr_source_coupling",
        "evidence": "4440 source register, derivation rows, source charge closure gate, epsilon_Gsrc tail bound gate, reduced contract rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": "Prove action-measure/current owner and same-current R_eq zero, or fill first finite R_eq/B_zero/Delta_w/tau/source-profile tail values.",
        "risk": "Using observed GM as source input; treating common G calibration as source-coupling evidence; claiming local GR before H_tau/MHref and projection tails close.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writerow(new_row)


def append_marker_section(path: Path, marker: str, section: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    write_text(path, existing.rstrip() + "\n\n" + section.strip() + "\n")


def write_spine_and_packet() -> None:
    spine_section = f"""## Local GR Source Coupling Update - Epsilon Gsrc Tail Split

Marker: `{MARKER}`  
Source checkpoint: `4440-Y5-R2FR-source-charge-Htau-MHref-closure-or-epsilon-Gsrc-first-tail-value.md`  
Claim register row: `{CLAIM_ID}`

Source-coupling residual split:

```text
epsilon_Gsrc = epsilon_bar_H + epsilon_Gsrc_perp
epsilon_bar_H -> calibrated common G_cal mode
epsilon_Gsrc_perp <= E_measure + E_mass + E_transition + E_Xi + E_T
```

The fixed EM branch has been removed from this tail. The remaining source-coupling proof target is the action-measure/current owner plus same-current `R_eq=0`, H_tau/MHref same-branch locks and arena projection values.
"""
    packet_section = f"""## PPC4161 Packet Addendum - Source Charge Tail Split

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4440-Y5-R2FR-source-charge-Htau-MHref-closure-or-epsilon-Gsrc-first-tail-value.md`

The packet now carries `epsilon_Gsrc_perp` as the physical finite source-coupling tail after common-mode calibration and fixed EM deletion. The live closure contract is action-measure/current ownership, same-current `R_eq=0`, H_tau/MHref integrability/reference/tau/boundary/MHref locks, and real arena projection values.
"""
    append_marker_section(SPINE_PATH, MARKER, spine_section)
    append_marker_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    source_outputs = {row["row_id"]: row for row in rows_from(SOURCE_CLOSURE_OUTPUT)}
    tail_outputs = {row["tail_id"]: row for row in rows_from(TAIL_BOUND_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in source_outputs.values()) and not any(row.get("valid_for_claim") == "True" for row in tail_outputs.values())
    checks = [
        ("VAL4440_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4440_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4440_2_contract_reduced", source_outputs["SC4440_0_current_after_EM_zero"].get("current_status") == "SOURCE_CHARGE_REDUCED_TO_ACTION_MEASURE_CURRENT_CONTRACT", "current source charge reduced to action-measure/current contract"),
        ("VAL4440_3_tail_smoke_pass", tail_outputs["TAIL4440_2_newton_small_smoke"].get("current_status") == "EPSILON_GSRC_TAIL_SCHEMA_PASS_NONCLAIM", "small finite tail smoke row passes schema nonclaim"),
        ("VAL4440_4_tail_fail_control", tail_outputs["TAIL4440_3_newton_fail_control"].get("current_status") == "EPSILON_GSRC_TAIL_FAILS_BOUND", "fail-control tail row fails bound"),
        ("VAL4440_5_arena_contracts", all(key in text(TAIL_BOUND_OUTPUT) for key in ("TAIL4440_4_R10_contract", "TAIL4440_5_PPN_contract", "TAIL4440_6_clock_contract", "TAIL4440_7_orbital_contract")), "R10/PPN/clock/orbital rows written"),
        ("VAL4440_6_no_claim_outputs", no_claims, "no output row is claim-ready"),
        ("VAL4440_7_claim_gate_no_claim", any(row["gate_id"] == "CG4440_6_no_public_claim" and row["passed"] == "True" for row in gates), "claim gate explicitly blocks public claim"),
        ("VAL4440_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-281"),
        ("VAL4440_9_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4440_10_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4440_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4440_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4440_13_next_gate", any(row["gate_id"] == "CG4440_7_next_target_written" and row["passed"] == "True" for row in gates), "next target claim gate is true"),
        ("VAL4440_14_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4440_15_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(SOURCE_CLOSURE_INPUT, source_closure_input_rows())
    write_csv(SOURCE_CLOSURE_OUTPUT, evaluate_source_charge_rows(SOURCE_CLOSURE_INPUT))
    write_csv(TAIL_BOUND_INPUT, tail_bound_input_rows())
    write_csv(TAIL_BOUND_OUTPUT, evaluate_tail_bound_rows(TAIL_BOUND_INPUT))
    write_csv(REDUCED_CONTRACT_ROWS, reduced_contract_rows())
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    source_outputs = rows_from(SOURCE_CLOSURE_OUTPUT)
    tail_outputs = rows_from(TAIL_BOUND_OUTPUT)
    gates = claim_gate_rows(source_outputs, tail_outputs)
    write_csv(CLAIM_GATES, gates)
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), source_outputs, tail_outputs, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()
