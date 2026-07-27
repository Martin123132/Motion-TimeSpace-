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

from ppn_survivor_map_gate import (  # noqa: E402
    evaluate_survivor_rows,
    evaluate_target_rows,
    write_csv,
)


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4448"
CLAIM_ID = "L-290"
MARKER = "PPC4161_NON_SOURCE_PPN_SURVIVOR_MAP_A_MF_TARGET_4448"
PACKET_MARKER = "PPC4161_PACKET_NON_SOURCE_SURVIVOR_MAP_A_MF_TARGET_4448"
DECISION = "NON_SOURCE_SURVIVORS_RANKED_PRIVATE_CLOSURES_RECOVERED_A_MF_PARENT_SIGNATURE_SELECTED_AS_NEXT_DERIVATION_TARGET"
NEXT_TARGET = "4449-Y5-R2FR-parent-motion-frame-A-MF-adoption-or-derived-flow-symmetry.md"

FORMAL_PATH = FORMAL / "464-PPC4161-non-source-PPN-residual-survivor-map-or-first-material-Req-value.md"
DOC_PATH = POST / "4448-Y5-R2FR-non-source-PPN-residual-survivor-map-or-first-material-Req-value.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4448_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4448_SOURCE_REGISTER.csv"
DERIVATION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4448_DERIVATION_ROWS.csv"
SURVIVOR_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4448_SURVIVOR_MAP_INPUT.csv"
SURVIVOR_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4448_SURVIVOR_MAP_OUTPUT.csv"
TARGET_INPUT = SOURCE_DIR / "P8_Y5_R2FR_4448_TARGET_RANKING_INPUT.csv"
TARGET_OUTPUT = SOURCE_DIR / "P8_Y5_R2FR_4448_TARGET_RANKING_OUTPUT.csv"
MATERIAL_CARRY = SOURCE_DIR / "P8_Y5_R2FR_4448_MATERIAL_REQ_CARRY_FORWARD.csv"
REDUCTION_ROWS = SOURCE_DIR / "P8_Y5_R2FR_4448_REDUCTION_ROWS.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4448_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4448_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4448_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4448_NEXT_TARGET.csv"

GATE_PATH = SCRIPT_DIR / "ppn_survivor_map_gate.py"
GENERATOR_PATH = SCRIPT_DIR / "Y5_R2FR_4448_non_source_PPN_residual_survivor_map_or_first_material_Req_value.py"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

NEXT_4447 = SOURCE_DIR / "P8_Y5_R2FR_4447_NEXT_TARGET.csv"
FORMAL_463 = FORMAL / "463-PPC4161-GR-parity-source-universality-to-local-PPN-residual-vector-or-material-values.md"
FORMAL_191 = FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md"
FORMAL_192 = FORMAL / "192-PPC4161-local-boundary-no-flux-sector-interface-theorem.md"
FORMAL_193 = FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md"
FORMAL_195 = FORMAL / "195-PPC4161-local-GR-private-closure-summary-and-parent-adoption-burden-map.md"
FORMAL_197 = FORMAL / "197-PPC4161-EH-local-metric-principal-block-origin-gate.md"
FORMAL_198 = FORMAL / "198-PPC4161-motion-frame-symmetry-parent-signature-gate.md"
FORMAL_223 = FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md"
FORMAL_247 = FORMAL / "247-PPC4161-private-local-GR-scorecard-refresh-and-nonEH-parent-adoption-gate.md"
FORMAL_185 = FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md"
FORMAL_222 = FORMAL / "222-PPC4161-calibrated-GN-bridge-and-source-charge-caveat.md"
OUT_4168_COUPLING = SOURCE_DIR / "P8_Y5_R2FR_4168_LOCAL_COUPLING_RESIDUAL_CLOSE.csv"
OUT_4169_ZH = SOURCE_DIR / "P8_Y5_R2FR_4169_DELTA_ZH_CHANNEL_CLOSURE.csv"
OUT_4172_PPN = SOURCE_DIR / "P8_Y5_R2FR_4172_RESIDUAL_CLOSE_OR_REACTIVATE.csv"
OUT_4175_EM = SOURCE_DIR / "P8_Y5_R2FR_4175_EM_SIDE_CHANNEL_CLOSE_OR_REACTIVATE.csv"
OUT_4177_PROJ = SOURCE_DIR / "P8_Y5_R2FR_4177_PROJECTOR_RESIDUAL_CLOSE_OR_BOUND.csv"
OUT_4181_DEMOTION = SOURCE_DIR / "P8_Y5_R2FR_4181_EFFECTIVE_GR_DEMOTION_LEDGER.csv"
OUT_4182_SWEEP = SOURCE_DIR / "P8_Y5_R2FR_4182_PARENT_SYMMETRY_EVIDENCE_SWEEP.csv"
OUT_4182_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4182_EFFECTIVE_GR_LABEL_DECISION.csv"
OUT_4207_POYNTING = SOURCE_DIR / "P8_Y5_R2FR_4207_POYNTING_OWNER_CHAIN.csv"
OUT_4447_MATERIAL = SOURCE_DIR / "P8_Y5_R2FR_4447_MATERIAL_REQ_OUTPUT.csv"
OUT_4447_ROLLUP = SOURCE_DIR / "P8_Y5_R2FR_4447_RESIDUAL_ROLLUP.csv"
PROMOTION_GATES = SOURCE_DIR / "P8_LOCAL_GR_RESIDUAL_PROMOTION_GATES.csv"
DOMAIN_VECTOR = SOURCE_DIR / "P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv"


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
        {"source_id": "SRC4448_00_next4447", "path": NEXT_4447, "needle": "4448-Y5-R2FR-non-source-PPN-residual-survivor-map-or-first-material-Req-value.md", "role": "4447 handoff."},
        {"source_id": "SRC4448_01_formal463", "path": FORMAL_463, "needle": "does **not** erase non-source residuals", "role": "4447 survivor statement."},
        {"source_id": "SRC4448_02_private_closure_summary", "path": FORMAL_195, "needle": "coherent private selector route", "role": "private local-GR closure summary."},
        {"source_id": "SRC4448_03_EH_origin_gate", "path": FORMAL_197, "needle": "current_MTS_EH_derivation = false", "role": "EH block effective-GR demotion."},
        {"source_id": "SRC4448_04_A_MF_formal", "path": FORMAL_198, "needle": "A_MF_PARENT_SIGNATURE_NOT_FOUND", "role": "motion-frame parent signature missing."},
        {"source_id": "SRC4448_05_A_MF_sweep", "path": OUT_4182_SWEEP, "needle": "EV4182_7_current_verdict", "role": "source sweep verdict for A_MF."},
        {"source_id": "SRC4448_06_A_MF_decision", "path": OUT_4182_DECISION, "needle": "current_MTS_local_GR_derivation", "role": "effective-GR label decision."},
        {"source_id": "SRC4448_07_projector_formal", "path": FORMAL_193, "needle": "R_proj = Pi_loc D Obar_loc[Dq[v]] = 0", "role": "quotient/projector private closure."},
        {"source_id": "SRC4448_08_projector_output", "path": OUT_4177_PROJ, "needle": "PR4177_1_preferred_frame", "role": "machine projector closure rows."},
        {"source_id": "SRC4448_09_poynting_formal", "path": FORMAL_191, "needle": "So the Poynting vector is not a separate background field.", "role": "Maxwell-Hodge Poynting owner theorem."},
        {"source_id": "SRC4448_10_poynting_lock", "path": FORMAL_223, "needle": "c_Poynt_extra = 0", "role": "Poynting once-only lock."},
        {"source_id": "SRC4448_11_poynting_output", "path": OUT_4207_POYNTING, "needle": "PO4207_4_once_only", "role": "machine Poynting owner chain."},
        {"source_id": "SRC4448_12_boundary_formal", "path": FORMAL_192, "needle": "J_tr^nu = 0 through <=2PN", "role": "boundary/interface no-flux private closure."},
        {"source_id": "SRC4448_13_ppn_output", "path": OUT_4172_PPN, "needle": "R4172_gamma", "role": "private PPN residual zero rows."},
        {"source_id": "SRC4448_14_kappa_output", "path": OUT_4168_COUPLING, "needle": "RC4168_1_kappa_closed", "role": "kappa coupling drift closure."},
        {"source_id": "SRC4448_15_deltaZH_output", "path": OUT_4169_ZH, "needle": "ZH4169_0_time", "role": "delta_ZH channel closure."},
        {"source_id": "SRC4448_16_EM_side_channel", "path": OUT_4175_EM, "needle": "EMSC4175_0_epsilon_EM_extra_inner", "role": "EM side-channel closure/reactivation rows."},
        {"source_id": "SRC4448_17_nonEH_scorecard", "path": FORMAL_247, "needle": "nonEH/R11 coefficient vector", "role": "later scorecard blocker."},
        {"source_id": "SRC4448_18_promotion_gates", "path": PROMOTION_GATES, "needle": "G482_local_GR_vector", "role": "public promotion gate still failing."},
        {"source_id": "SRC4448_19_domain_vector", "path": DOMAIN_VECTOR, "needle": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION", "role": "domain/R11 template survivor rows."},
        {"source_id": "SRC4448_20_material4447", "path": OUT_4447_MATERIAL, "needle": "MATERIAL_REQ_SOURCE_CANDIDATES_READY_VALUES_MISSING", "role": "material/R_eq values remain open."},
        {"source_id": "SRC4448_21_rollup4447", "path": OUT_4447_ROLLUP, "needle": "RU4447_1_full_PPN_vector", "role": "4447 full PPN nonclaim rollup."},
        {"source_id": "SRC4448_22_GN_caveat", "path": FORMAL_222, "needle": "MTS does not need to numerically predict G_N", "role": "G_N calibration caveat."},
        {"source_id": "SRC4448_23_gate", "path": GATE_PATH, "needle": "def evaluate_survivor_row", "role": "4448 survivor map gate."},
        {"source_id": "SRC4448_24_generator", "path": GENERATOR_PATH, "needle": 'CHECKPOINT = "4448"', "role": "4448 generator script."},
    ]


def source_rows() -> List[Dict[str, object]]:
    rows = []
    for spec in source_specs():
        path = Path(spec["path"])
        needle = str(spec["needle"])
        line = line_of(path, needle)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": spec["source_id"],
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": line > 0,
            "line_number": line,
            "role": spec["role"],
            "valid_for_claim": False,
        })
    return rows


def derivation_rows() -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "SURV4448_D0_recover_private_closures",
            "claim": "Several 4447 survivors are not unworked holes; they are private closures with parent-adoption guards.",
            "derivation": "4175/4207 own Poynting as Maxwell-Hodge Hilbert stress, 4177 closes quotient/projector residuals inside the private selector, 4168/4169 close kappa and source-measure drift, and 4172 records the private PPN vector. Therefore 4448 must not send the next work back into already closed-private Poynting/projector rows unless their reactivation guards fail.",
            "consequence": "Poynting, quotient/projector and coupling drift move from undifferentiated survivor list to closed-private/parent-adoption-open rows.",
            "status": "PRIVATE_CLOSURES_RECOVERED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SURV4448_D1_identify_actual_derivation_blocker",
            "claim": "The highest-value derivation blocker is the parent-owned motion-frame gauge axiom A_MF.",
            "derivation": "4181/4182 prove the compensator forcing theorem: if local affine/Lorentz motion-frame symmetry is parent-signed, omega and B are forced and the Cartan/Palatini route can own the EH principal block. The sweep did not find A_MF in the corpus, so current_MTS_local_GR_derivation=false and effective_GR_closure_label_active=true.",
            "consequence": "The next derivation should try to adopt or derive A_MF from motion/time/space/flow primitives, not repeat Poynting or source-weight closure.",
            "status": "A_MF_SELECTED_AS_PRIMARY_TARGET",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "SURV4448_D2_empirical_fallback_kept",
            "claim": "If A_MF cannot be derived/adopted, the useful fallback is empirical: nonEH/R11 or material/R_eq bound rows.",
            "derivation": "The scorecard and promotion gates still show nonEH/R11/domain coefficient rows and material/R_eq values missing for public scoring. Those are fallback empirical routes, but they do not convert the EH block from effective-GR infrastructure into MTS-derived geometry.",
            "consequence": "The chosen next target is derivation-first; empirical rows remain second track.",
            "status": "EMPIRICAL_FALLBACK_RANKED_SECONDARY",
            "valid_for_claim": False,
        },
    ]


def survivor_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "row_id": "SURV4448_0_A_MF_parent_motion_frame",
            "residual_family": "EH_principal_block_origin",
            "observable_targets": "gamma,beta,Newtonian_metric_principal_block",
            "source_path": str(OUT_4182_DECISION),
            "private_closed": False,
            "conditional_theorem": True,
            "parent_signed": False,
            "empirical_ready": False,
            "reactivation_guard": True,
            "primary_derivation_target": True,
            "active_blocker": True,
            "public_claim_false": True,
            "priority_rank": 1,
            "next_action": "derive_or_explicitly_adopt_A_MF_from_motion_time_space_flow_primitives",
        },
        {
            "row_id": "SURV4448_1_EH_effective_GR_label",
            "residual_family": "EH_Palatini_normal_form",
            "observable_targets": "gamma,beta,PPN_metric_coefficients",
            "source_path": str(OUT_4181_DEMOTION),
            "private_closed": False,
            "conditional_theorem": True,
            "parent_signed": False,
            "empirical_ready": False,
            "reactivation_guard": True,
            "primary_derivation_target": False,
            "active_blocker": True,
            "public_claim_false": True,
            "priority_rank": 1,
            "next_action": "same_as_A_MF_then_parent_sign_Palatini_EH_normal_form_or_keep_effective_GR_label",
        },
        {
            "row_id": "SURV4448_2_nonEH_R11_vector",
            "residual_family": "nonEH_R11_domain_coefficient_vector",
            "observable_targets": "alpha_i,xi,R11,source_normalization",
            "source_path": str(FORMAL_247),
            "private_closed": False,
            "conditional_theorem": False,
            "parent_signed": False,
            "empirical_ready": False,
            "reactivation_guard": True,
            "primary_derivation_target": False,
            "active_blocker": True,
            "public_claim_false": True,
            "priority_rank": 2,
            "next_action": "after_A_MF_or_if_A_MF_rejected_build_nonEH_R11_zero_vector_or_bound_runner",
        },
        {
            "row_id": "SURV4448_3_quotient_projector_domain",
            "residual_family": "quotient_projector_domain",
            "observable_targets": "alpha_i,xi,WEP,clock,R10,orbital_projector_pieces",
            "source_path": str(OUT_4177_PROJ),
            "private_closed": True,
            "conditional_theorem": True,
            "parent_signed": False,
            "empirical_ready": False,
            "reactivation_guard": True,
            "primary_derivation_target": False,
            "active_blocker": False,
            "public_claim_false": True,
            "priority_rank": 3,
            "next_action": "do_not_reopen_unless_q_factorization_or_boundary_guard_fails",
        },
        {
            "row_id": "SURV4448_4_EM_Poynting_once_only",
            "residual_family": "EM_Poynting_Hilbert_owner",
            "observable_targets": "zeta3,preferred_frame,WEP_clock_EM_leak,R10_EM_background",
            "source_path": str(OUT_4207_POYNTING),
            "private_closed": True,
            "conditional_theorem": True,
            "parent_signed": False,
            "empirical_ready": False,
            "reactivation_guard": True,
            "primary_derivation_target": False,
            "active_blocker": False,
            "public_claim_false": True,
            "priority_rank": 4,
            "next_action": "retain_deformation_and_radiative_boundary_tails_only",
        },
        {
            "row_id": "SURV4448_5_boundary_no_flux",
            "residual_family": "boundary_transition_current",
            "observable_targets": "xi,alpha_i,clock,R10,transition_force",
            "source_path": str(FORMAL_192),
            "private_closed": True,
            "conditional_theorem": True,
            "parent_signed": False,
            "empirical_ready": False,
            "reactivation_guard": True,
            "primary_derivation_target": False,
            "active_blocker": False,
            "public_claim_false": True,
            "priority_rank": 5,
            "next_action": "route_nonzero_radiative_flux_as_boundary_Hamiltonian_charge_not_bulk_source",
        },
        {
            "row_id": "SURV4448_6_kappa_deltaZH_Gdot",
            "residual_family": "calibrated_source_coupling_drift",
            "observable_targets": "Gdot/G,source_frame_range_readout_drift",
            "source_path": str(FORMAL_222),
            "private_closed": True,
            "conditional_theorem": True,
            "parent_signed": False,
            "empirical_ready": False,
            "reactivation_guard": True,
            "primary_derivation_target": False,
            "active_blocker": False,
            "public_claim_false": True,
            "priority_rank": 6,
            "next_action": "keep_calibrated_G_caveat_and_do_not_try_to_predict_numeric_G_here",
        },
        {
            "row_id": "SURV4448_7_material_Req_values",
            "residual_family": "material_R_eq_empirical_values",
            "observable_targets": "WEP,clock,orbital,compact_R_eq",
            "source_path": str(OUT_4447_MATERIAL),
            "private_closed": False,
            "conditional_theorem": False,
            "parent_signed": False,
            "empirical_ready": False,
            "reactivation_guard": True,
            "primary_derivation_target": False,
            "active_blocker": True,
            "public_claim_false": True,
            "priority_rank": 3,
            "next_action": "fill_numeric_projection_coeff_residual_value_arena_bound_if_derivation_route_stalls",
        },
        {
            "row_id": "SURV4448_8_R10_alpha_curve",
            "residual_family": "R10_alpha_lambda_empirical_curve",
            "observable_targets": "short_range_fifth_force_alpha_lambda",
            "source_path": str(PROMOTION_GATES),
            "private_closed": False,
            "conditional_theorem": False,
            "parent_signed": False,
            "empirical_ready": False,
            "reactivation_guard": True,
            "primary_derivation_target": False,
            "active_blocker": True,
            "public_claim_false": True,
            "priority_rank": 4,
            "next_action": "fill_full_curve_or_mapped_fifth_force_envelope_later",
        },
    ]


def target_input_rows() -> List[Dict[str, object]]:
    return [
        {
            "target_id": "T4448_0_A_MF",
            "target": "derive_or_adopt_parent_motion_frame_gauge_axiom_A_MF",
            "priority_rank": 1,
            "chosen": True,
            "source_path": str(OUT_4182_DECISION),
            "moves_derivation": True,
            "avoids_repeating_closed_work": True,
            "next_artifact": NEXT_TARGET,
        },
        {
            "target_id": "T4448_1_nonEH_R11",
            "target": "nonEH_R11_zero_vector_or_bound_runner",
            "priority_rank": 2,
            "chosen": False,
            "source_path": str(FORMAL_247),
            "moves_derivation": True,
            "avoids_repeating_closed_work": True,
            "next_artifact": "later_if_A_MF_stalls",
        },
        {
            "target_id": "T4448_2_material_Req",
            "target": "first_material_or_R_eq_numeric_value",
            "priority_rank": 3,
            "chosen": False,
            "source_path": str(OUT_4447_MATERIAL),
            "moves_derivation": False,
            "avoids_repeating_closed_work": True,
            "next_artifact": "empirical_fallback",
        },
        {
            "target_id": "T4448_3_Poynting",
            "target": "repeat_EM_Poynting_once_only_theorem",
            "priority_rank": 4,
            "chosen": False,
            "source_path": str(OUT_4207_POYNTING),
            "moves_derivation": False,
            "avoids_repeating_closed_work": False,
            "next_artifact": "not_selected_already_closed_private",
        },
    ]


def material_rows() -> List[Dict[str, object]]:
    return [
        {
            "carry_id": "MAT4448_0_material_values",
            "source_path": str(OUT_4447_MATERIAL),
            "status": "CARRIED_FORWARD_VALUES_MISSING",
            "needed_for": "public WEP/clock/orbital/material scoring",
            "not_needed_for": "choosing A_MF as next derivation target",
            "next_action": "fill after derivation route or if empirical fallback selected",
            "valid_for_claim": False,
        },
        {
            "carry_id": "MAT4448_1_R_eq",
            "source_path": str(OUT_4447_MATERIAL),
            "status": "CARRIED_FORWARD_VALUES_MISSING",
            "needed_for": "compact R_eq/orbital same-current scoring",
            "not_needed_for": "A_MF parent-signature derivation attempt",
            "next_action": "source projection coefficient, residual value and arena bound later",
            "valid_for_claim": False,
        },
    ]


def reduction_rows() -> List[Dict[str, object]]:
    return [
        {
            "reduction_id": "RED4448_0_survivor_map",
            "from_problem": "undifferentiated non-source survivor list",
            "to_problem": "ranked closed-private/effective-only/open-public blocker map",
            "status": "SURVIVORS_RANKED",
            "reason": "Existing private closures should not be attacked again unless their reactivation guards fail.",
            "valid_for_claim": False,
        },
        {
            "reduction_id": "RED4448_1_poynting_not_next",
            "from_problem": "EM/Poynting suspected side-channel",
            "to_problem": "closed-private Maxwell-Hodge Hilbert-owner row with retained deformation/radiative tails",
            "status": "PRIVATE_CLOSURE_RECOVERED",
            "reason": "4175/4207 already gives c_Poynt_extra=0 inside the private selector.",
            "valid_for_claim": False,
        },
        {
            "reduction_id": "RED4448_2_A_MF_next",
            "from_problem": "effective-GR demotion of local EH block",
            "to_problem": NEXT_TARGET,
            "status": "NEXT_DERIVATION_TARGET_SELECTED",
            "reason": "A_MF is the narrow axiom that would force omega/B compensators and turn the local metric route from imported/effective GR into parent-owned MTS geometry.",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(survivor_outputs: Sequence[Mapping[str, str]], target_outputs: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    survivors = {row["row_id"]: row for row in survivor_outputs}
    targets = {row["target_id"]: row for row in target_outputs}
    sources = rows_from(SOURCE_REGISTER)
    no_claim = not any(row.get("valid_for_claim") == "True" for row in survivor_outputs)
    return [
        {"gate_id": "CG4448_0_sources_exist", "claim": "all cited source paths exist", "passed": all(row["path_exists"] == "True" for row in sources), "valid_for_claim": False, "detail": "Source register path-backed."},
        {"gate_id": "CG4448_1_needles_found", "claim": "all cited source needles found", "passed": all(row["needle_found"] == "True" for row in sources), "valid_for_claim": False, "detail": "No survivor ranking without source text."},
        {"gate_id": "CG4448_2_A_MF_primary", "claim": "A_MF is selected as primary derivation target", "passed": survivors["SURV4448_0_A_MF_parent_motion_frame"].get("current_status") == "PRIMARY_DERIVATION_TARGET", "valid_for_claim": False, "detail": "This is the route from effective-GR infrastructure toward MTS-owned local geometry."},
        {"gate_id": "CG4448_3_EH_effective_label", "claim": "EH principal block remains effective-only until A_MF is signed", "passed": survivors["SURV4448_1_EH_effective_GR_label"].get("current_status") == "CONDITIONAL_THEOREM_EFFECTIVE_GR_LABEL_ACTIVE", "valid_for_claim": False, "detail": "No public local-GR derivation is smuggled."},
        {"gate_id": "CG4448_4_projector_private_closed", "claim": "quotient/projector rows recovered as closed-private", "passed": survivors["SURV4448_3_quotient_projector_domain"].get("current_status") == "CLOSED_PRIVATE_PARENT_ADOPTION_OPEN", "valid_for_claim": False, "detail": "Do not re-derive unless q-factorization fails."},
        {"gate_id": "CG4448_5_poynting_private_closed", "claim": "EM/Poynting once-only row recovered as closed-private", "passed": survivors["SURV4448_4_EM_Poynting_once_only"].get("current_status") == "CLOSED_PRIVATE_PARENT_ADOPTION_OPEN", "valid_for_claim": False, "detail": "Poynting is Hilbert stress flux, not extra bulk source, inside private selector."},
        {"gate_id": "CG4448_6_material_values_open", "claim": "material/R_eq values remain empirical fallback", "passed": survivors["SURV4448_7_material_Req_values"].get("current_status") == "SURVIVES_AS_ACTIVE_PUBLIC_BLOCKER", "valid_for_claim": False, "detail": "Values missing but not the next derivation-first target."},
        {"gate_id": "CG4448_7_target_selected", "claim": "target ranking selects 4449", "passed": targets["T4448_0_A_MF"].get("current_status") == "NEXT_TARGET_SELECTED", "valid_for_claim": False, "detail": NEXT_TARGET},
        {"gate_id": "CG4448_8_no_public_claim", "claim": "4448 emits no public local-GR claim", "passed": no_claim, "valid_for_claim": False, "detail": "Every survivor row remains nonclaim."},
        {"gate_id": "CG4448_9_next_target_written", "claim": "next target file recorded", "passed": NEXT_CSV.exists() and NEXT_TARGET in text(NEXT_CSV), "valid_for_claim": False, "detail": NEXT_TARGET},
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4448_0",
            "decision": DECISION,
            "summary": "4448 turns the loose survivor list into a ranked map. EM/Poynting, quotient/projector, boundary, kappa/deltaZH and private PPN rows are recovered as closed-private with parent-adoption guards. The true derivation blocker is A_MF: the parent-owned local motion-frame gauge principle that would force omega/B compensators and convert the EH principal block from effective GR infrastructure into MTS-owned geometry. Material/R_eq and nonEH/R11 remain empirical/secondary fallback routes.",
            "next_target": NEXT_TARGET,
            "public_claim": False,
            "valid_for_claim": False,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "root_result": "non-source survivors ranked; private closures recovered; A_MF chosen next",
            "closed_private_recovered": "Poynting once-only; quotient/projector vertical silence; boundary no-flux; kappa/deltaZH; private PPN vector",
            "primary_missing_derivation": "A_MF parent-owned motion-frame gauge symmetry/flow principle",
            "secondary_missing": "nonEH/R11 coefficient vector; material/R_eq values; R10 alpha(lambda) full curve",
            "next_target": NEXT_TARGET,
            "public_claim": False,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4448_0",
            "target": NEXT_TARGET,
            "objective": "Try to derive or explicitly adopt the parent-owned motion-frame gauge axiom A_MF from motion/time/space/flow primitives, then list the exact consequences for omega, B, e, g_obs, EH/Palatini normal form and source coupling.",
            "derive_first": "show internal motion-frame labels are local affine/Lorentz gauge redundancies whose covariance forces omega and B, rather than imported GR decoration",
            "fallback": "if A_MF cannot be derived/adopted, keep effective-GR label and move to nonEH/R11 coefficient bounds or first material/R_eq value",
            "risk": "calling the EH principal block MTS-derived before A_MF is parent-signed",
            "valid_for_claim": False,
        }
    ]


def build_doc(sources: Sequence[Mapping[str, object]], survivor_outputs: Sequence[Mapping[str, object]], target_outputs: Sequence[Mapping[str, object]], gates: Sequence[Mapping[str, object]]) -> str:
    return f"""# 464 PPC4161 non-source PPN residual survivor map or first material Req value

Marker: `{MARKER}`

Decision: `{DECISION}`

Claim register: `{CLAIM_ID}`

## Result

4448 stops treating every non-source survivor as equally open. The map says:

```text
Poynting once-only: closed private, parent-adoption guard retained.
Quotient/projector silence: closed private, parent-adoption guard retained.
Boundary/no-flux and kappa/deltaZH: closed private/guarded.
Material/R_eq and nonEH/R11: empirical or coefficient fallback.
Actual derivation blocker: A_MF, the parent motion-frame gauge principle.
```

The next move is therefore not another Poynting pass. It is to try to derive or explicitly adopt `A_MF` from motion/time/space/flow primitives.

## Source Register

{table(sources)}

## Derivation Rows

{table(rows_from(DERIVATION_ROWS))}

## Survivor Map

{table(survivor_outputs)}

## Target Ranking

{table(target_outputs)}

## Material / R_eq Carry Forward

{table(rows_from(MATERIAL_CARRY))}

## Reduction Rows

{table(rows_from(REDUCTION_ROWS))}

## Claim Gates

{table(gates)}

## Decision

{table(rows_from(DECISION_CSV))}

## Status

{table(rows_from(STATUS_CSV))}

## Next Target

{table(rows_from(NEXT_CSV))}
"""


def post_doc() -> str:
    return f"""# 4448 Y5 R2FR non-source PPN residual survivor map or first material Req value

Private checkpoint generated at `{STAMP}`.

Summary:
- Ranked non-source survivors instead of treating them as one fog bank.
- Recovered Poynting, quotient/projector, boundary, kappa/deltaZH and private PPN rows as closed-private with reactivation guards.
- Selected `A_MF` as the actual next derivation target because it can turn the EH block from effective-GR infrastructure into parent-owned MTS geometry.

Next target: `{NEXT_TARGET}`
"""


def update_claims_register() -> None:
    rows = rows_from(CLAIMS_PATH)
    fieldnames = list(rows[0].keys()) if rows else ["claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"]
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_derivation",
        "claim": "4448 ranks the non-source PPN survivors: several are recovered as closed-private with parent-adoption guards, while the true derivation blocker is A_MF, the parent-owned motion-frame gauge principle needed to turn the EH principal block from effective GR infrastructure into MTS-owned geometry.",
        "current_evidence": "4448 source register, derivation rows, survivor map, target ranking, material carry-forward, reduction rows, claim gates, decision, status, next target and validation CSV.",
        "status": "A_MF_parent_motion_frame_signature_selected_as_next_derivation_target_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Repeating already closed-private Poynting/projector work instead of attacking the parent EH-origin blocker.",
        "sector": "local_gr_parent_derivation",
        "evidence": "4448 source register, derivation rows, survivor map, target ranking, material carry-forward, reduction rows, claim gates, decision, status, next target and validation CSV.",
        "next_action": NEXT_TARGET,
        "risk": "Repeating already closed-private Poynting/projector work instead of attacking the parent EH-origin blocker.",
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
    spine_section = f"""## Local GR Parent-Derivation Update - Non-Source Survivor Map

Marker: `{MARKER}`  
Source checkpoint: `4448-Y5-R2FR-non-source-PPN-residual-survivor-map-or-first-material-Req-value.md`  
Claim register row: `{CLAIM_ID}`

The non-source survivor list is now ranked. EM/Poynting, quotient/projector, boundary, kappa/deltaZH and private PPN readout are closed-private with reactivation guards. The primary derivation target is `A_MF`: a parent-owned local motion-frame gauge principle that would force `omega`, `B`, `e`, `g_obs` and the EH/Palatini normal form from MTS structure rather than importing effective GR.
"""
    packet_section = f"""## PPC4161 Packet Addendum - Non-Source Survivor Map

Marker: `{PACKET_MARKER}`  
Source checkpoint: `4448-Y5-R2FR-non-source-PPN-residual-survivor-map-or-first-material-Req-value.md`

The packet now separates closed-private non-source residuals from the real parent-derivation blocker. Do not spend the next pass re-proving Poynting/projector closure unless a reactivation guard fails; attack `A_MF` first.
"""
    append_marker_section(SPINE_PATH, MARKER, spine_section)
    append_marker_section(PACKET_PATH, PACKET_MARKER, packet_section)


def validation_rows(paths: Mapping[str, Path]) -> List[Dict[str, object]]:
    sources = rows_from(SOURCE_REGISTER)
    survivors = {row["row_id"]: row for row in rows_from(SURVIVOR_OUTPUT)}
    targets = {row["target_id"]: row for row in rows_from(TARGET_OUTPUT)}
    gates = rows_from(CLAIM_GATES)
    no_claims = not any(row.get("valid_for_claim") == "True" for row in survivors.values())
    checks = [
        ("VAL4448_0_sources_exist", all(row["path_exists"] == "True" for row in sources), "every cited source path exists"),
        ("VAL4448_1_needles_found", all(row["needle_found"] == "True" for row in sources), "every cited source needle is present"),
        ("VAL4448_2_A_MF_primary", survivors["SURV4448_0_A_MF_parent_motion_frame"].get("current_status") == "PRIMARY_DERIVATION_TARGET", "A_MF selected as primary derivation target"),
        ("VAL4448_3_EH_effective_label", survivors["SURV4448_1_EH_effective_GR_label"].get("current_status") == "CONDITIONAL_THEOREM_EFFECTIVE_GR_LABEL_ACTIVE", "EH effective-GR label retained"),
        ("VAL4448_4_projector_closed", survivors["SURV4448_3_quotient_projector_domain"].get("current_status") == "CLOSED_PRIVATE_PARENT_ADOPTION_OPEN", "projector closure recovered as private"),
        ("VAL4448_5_poynting_closed", survivors["SURV4448_4_EM_Poynting_once_only"].get("current_status") == "CLOSED_PRIVATE_PARENT_ADOPTION_OPEN", "Poynting closure recovered as private"),
        ("VAL4448_6_material_open", survivors["SURV4448_7_material_Req_values"].get("current_status") == "SURVIVES_AS_ACTIVE_PUBLIC_BLOCKER", "material values still open"),
        ("VAL4448_7_target_selected", targets["T4448_0_A_MF"].get("current_status") == "NEXT_TARGET_SELECTED", "4449 target selected"),
        ("VAL4448_8_all_claim_gates_pass", all(row["passed"] == "True" for row in gates), "all claim gates pass"),
        ("VAL4448_9_no_claim_outputs", no_claims, "no survivor output row is claim-ready"),
        ("VAL4448_10_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-290"),
        ("VAL4448_11_formal_doc", paths["formal"].exists() and MARKER in text(paths["formal"]), "formal doc exists with marker"),
        ("VAL4448_12_post_doc", paths["post"].exists() and "Private checkpoint" in text(paths["post"]), "post checkpoint doc exists"),
        ("VAL4448_13_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4448_14_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
        ("VAL4448_15_next_target", paths["next"].exists() and NEXT_TARGET in text(paths["next"]), "next target file exists"),
        ("VAL4448_16_pycache_absent", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent"),
    ]
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": bool(passed), "detail": detail} for check_id, passed, detail in checks]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    write_csv(SOURCE_REGISTER, source_rows())
    write_csv(DERIVATION_ROWS, derivation_rows())
    write_csv(SURVIVOR_INPUT, survivor_input_rows())
    write_csv(SURVIVOR_OUTPUT, evaluate_survivor_rows(SURVIVOR_INPUT))
    write_csv(TARGET_INPUT, target_input_rows())
    write_csv(TARGET_OUTPUT, evaluate_target_rows(TARGET_INPUT))
    write_csv(MATERIAL_CARRY, material_rows())
    write_csv(REDUCTION_ROWS, reduction_rows())
    write_csv(DECISION_CSV, decision_rows())
    write_csv(STATUS_CSV, status_rows())
    write_csv(NEXT_CSV, next_rows())
    survivor_outputs = rows_from(SURVIVOR_OUTPUT)
    target_outputs = rows_from(TARGET_OUTPUT)
    gates = claim_gate_rows(survivor_outputs, target_outputs)
    write_csv(CLAIM_GATES, gates)
    write_text(FORMAL_PATH, build_doc(rows_from(SOURCE_REGISTER), survivor_outputs, target_outputs, gates))
    write_text(DOC_PATH, post_doc())
    update_claims_register()
    write_spine_and_packet()
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    write_csv(VALIDATION_PATH, validation_rows({"formal": FORMAL_PATH, "post": DOC_PATH, "next": NEXT_CSV}))


if __name__ == "__main__":
    main()
