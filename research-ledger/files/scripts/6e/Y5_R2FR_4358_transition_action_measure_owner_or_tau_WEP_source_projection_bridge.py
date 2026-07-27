from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = POST / "source-intake" / "local_bounds"

CHECKPOINT = "4358"
CLAIM_ID = "L-199"
BRANCH = "MTS_R2FR_Y5_TRANSITION_ACTION_MEASURE_OWNER_OR_TAU_WEP_SOURCE_PROJECTION_BRIDGE_4358"
DECISION = "TAU_WEP_PRODUCT_TO_AMPLITUDE_BRIDGE_DERIVED_ACTION_MEASURE_OWNER_UNSIGNED_TAUMIN_TARGET_SELECTED_NONCLAIM"
MARKER = "PPC4161_TRANSITION_ACTION_MEASURE_OWNER_OR_TAU_WEP_SOURCE_PROJECTION_BRIDGE_4358"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_ACTION_MEASURE_OWNER_OR_TAU_WEP_SOURCE_PROJECTION_BRIDGE_4358"
NEXT_TARGET = "4359-Y5-R2FR-transition-tau-min-lower-bound-or-action-measure-zero-proof.md"

FORMAL_PATH = FORMAL / "374-PPC4161-transition-action-measure-owner-or-tau-WEP-source-projection-bridge.md"
DOC_PATH = POST / "4358-Y5-R2FR-transition-action-measure-owner-or-tau-WEP-source-projection-bridge.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4358_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4358_00_4357_next": (
        FORMAL / "373-PPC4161-transition-common-mode-parent-grammar-or-first-finite-hair-inputs.md",
        "4358-Y5-R2FR-transition-action-measure-owner-or-tau-WEP-source-projection-bridge.md",
        "4357 handoff to action-measure owner or tau-WEP source projection.",
    ),
    "SRC4358_01_4357_wa": (
        FORMAL / "373-PPC4161-transition-common-mode-parent-grammar-or-first-finite-hair-inputs.md",
        "S_matter -> sum_A w_A S_A",
        "Pre-variation action-weight counterexample retained in the transition branch.",
    ),
    "SRC4358_02_1596_product_law": (
        POST / "1596-Y5-R2FR-tau-WEP-source-projection-or-action-measure-owner-last-gate.md",
        "1596 derives the exact useful amplitude law",
        "Existing product-to-amplitude law for the WEP anchor.",
    ),
    "SRC4358_03_1596_tau_min": (
        POST / "1596-Y5-R2FR-tau-WEP-source-projection-or-action-measure-owner-last-gate.md",
        "abs(Delta_w_TiPt) <= 2.8e-15/tau_min",
        "Conditional Delta_w amplitude law if tau_min is sourced.",
    ),
    "SRC4358_04_1596_tau_unity": (
        POST / "1596-Y5-R2FR-tau-WEP-source-projection-or-action-measure-owner-last-gate.md",
        "`tau_WEP=1` and measured-`G` absorption are explicitly rejected",
        "No tau=1 shortcut and no measured-G hiding.",
    ),
    "SRC4358_05_1596_action_gate": (
        POST / "1596-Y5-R2FR-tau-WEP-source-projection-or-action-measure-owner-last-gate.md",
        "ACTION_MEASURE_OWNER_LAST_GATE_NOT_CLOSED",
        "Action-measure owner remains unsigned.",
    ),
    "SRC4358_06_1596_next": (
        POST / "1596-Y5-R2FR-tau-WEP-source-projection-or-action-measure-owner-last-gate.md",
        "1597-Y5-R2FR-tau-lower-bound-or-coupling-zero-proof.md",
        "Existing next target chooses tau lower bound or coupling zero proof.",
    ),
    "SRC4358_07_1225_tau_formula": (
        SOURCE_DIR / "P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv",
        "FORM1225_0_tau_WEP_functional",
        "Symbolic tau-WEP functional.",
    ),
    "SRC4358_08_1225_projection": (
        SOURCE_DIR / "P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv",
        "TAU1225_6_verdict",
        "tau-WEP projection attempt verdict.",
    ),
    "SRC4358_09_1224_contract": (
        SOURCE_DIR / "P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv",
        "FSW1224_2_tau_WEP",
        "Finite source-weight tau-WEP input contract.",
    ),
    "SRC4358_10_1083_source": (
        SOURCE_DIR / "P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
        "MISSING_SOURCE_PROFILE_WEIGHTING",
        "Earth/source worldtube profile weighting is missing.",
    ),
    "SRC4358_11_1084_readout": (
        SOURCE_DIR / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
        "OFFICIAL_ARRAYS_NOT_IMPORTED",
        "Official MICROSCOPE readout arrays are missing.",
    ),
    "SRC4358_12_1078_action_measure": (
        SOURCE_DIR / "P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv",
        "ACTION_MEASURE_NOT_SIGNED",
        "Action-measure proof attempt does not close.",
    ),
    "SRC4358_13_2995_readout_profile": (
        LOCAL_BOUNDS / "MICROSCOPE_readout_and_profile_gate_2995_NONCLAIM.csv",
        "OFFICIAL_READOUT_NOT_IMPORTED",
        "Later MICROSCOPE readout/profile gate remains nonclaim.",
    ),
    "SRC4358_14_local_bound": (
        LOCAL_BOUNDS / "local_bound_claims.csv",
        "R1_WEP_source_charge",
        "Source-backed MICROSCOPE WEP product-bound anchor.",
    ),
}

ARENAS = [
    ("WEP_species", "Delta_w_TiPt source/test composition residual", "requires tau_min>0 or action-measure zero theorem"),
    ("Newton_source", "source normalization in calibrated GM/G_cal", "blocked by w_A unless common action-measure owner closes"),
    ("local_GR", "source/coupling part of local GR reduction", "blocked while Delta_w can hide in tau_WEP null space"),
    ("PPN_gamma_beta", "source-weight transfer into metric response", "needs source/readout projection, not WEP anchor alone"),
    ("clock_Gdot", "time-dependent source normalization", "no measured-G absorption for derivative/source weights"),
    ("orbital_GM", "orbital source mass normalization", "requires same source-worldtube/readout owner"),
    ("R10_range", "finite-range source coupling", "separate lambda/alpha inputs still required"),
]


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: str(row.get(key, "")) for key in fields})


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def action_measure_rows() -> List[Dict[str, str]]:
    return [
        {
            "audit_id": "AM4358_0_target",
            "route": "one parent action measure/hbar owner",
            "would_close": "w_A source/action multipliers become inadmissible except for one common derivative-silent calibration factor",
            "current_evidence": "1078/1596 keep this as a clean conditional route but not parent-signed",
            "result": "ACTION_MEASURE_OWNER_UNSIGNED",
            "effect": "Delta_w_TiPt finite route remains active",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AM4358_1_classical_shortcut_reject",
            "route": "classical equations/free-fall remove action weights",
            "would_close": "Delta_w_TiPt=0",
            "current_evidence": "delta(w_A S_A)/delta Psi can be unchanged while metric source variation inherits w_A T_A",
            "result": "REJECTED",
            "effect": "do not infer common coupling from matter equations alone",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AM4358_2_current_owner_limit",
            "route": "Hilbert current owner after a common action is fixed",
            "would_close": "post-variation source rescalings",
            "current_evidence": "does not kill weights inserted before metric variation",
            "result": "PARTIAL_ONLY",
            "effect": "pre-variation w_A still needs action-measure owner or finite bound",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "AM4358_3_transition_verdict",
            "route": "use action-measure owner to kill transition common-mode source hair",
            "would_close": "Y_species_frame_source=0",
            "current_evidence": "owner is unsigned in current corpus",
            "result": "NO_ZERO_CLAIM",
            "effect": "continue through tau_WEP product-to-amplitude bridge",
            "valid_for_claim": "False",
        },
    ]


def tau_bridge_rows() -> List[Dict[str, str]]:
    return [
        {
            "bridge_id": "TB4358_0_linear_observable",
            "object": "MICROSCOPE Ti/Pt eta channel",
            "law": "eta_TiPt = Delta_w_TiPt * tau_WEP + O((Delta_w_TiPt*tau_WEP)^2) + R_readout_tail",
            "meaning": "finite source/action weight enters the reported WEP observable only through the projection tau_WEP on this branch",
            "status": "CONDITIONAL_LINEAR_BRIDGE_IMPORTED",
            "valid_for_claim": "False",
        },
        {
            "bridge_id": "TB4358_1_product_bound",
            "object": "P_WEP_relative_source_weight",
            "law": "abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15",
            "meaning": "source-backed MICROSCOPE anchor constrains the product, not Delta_w_TiPt alone",
            "status": "SOURCE_BACKED_PRODUCT_BOUND",
            "valid_for_claim": "False",
        },
        {
            "bridge_id": "TB4358_2_amplitude_law",
            "object": "Delta_w_TiPt",
            "law": "if abs(tau_WEP) >= tau_min > 0, then abs(Delta_w_TiPt) <= 2.8e-15/tau_min",
            "meaning": "the WEP anchor becomes a usable finite source-weight bound only after a positive projection lower bound is sourced",
            "status": "EXACT_CONDITIONAL_AMPLITUDE_LAW",
            "valid_for_claim": "False",
        },
        {
            "bridge_id": "TB4358_3_null_escape",
            "object": "tau_WEP",
            "law": "if tau_WEP can vanish or be arbitrarily small, no finite Delta_w_TiPt bound follows from the product anchor",
            "meaning": "tau_WEP=1 is not a convention; it is a source/readout projection that must be derived or measured",
            "status": "NO_SHORTCUT_THEOREM",
            "valid_for_claim": "False",
        },
    ]


def tau_factor_rows() -> List[Dict[str, str]]:
    return [
        {
            "factor_id": "TF4358_0_tau_functional",
            "factor": "tau_WEP functional",
            "required_object": "N_eta^-1 < K_eta[e_obs,orbit,masks] Integral_Earth dV K_source R_source R_material(TiPt) >_orbit",
            "current_status": "SYMBOLIC_ONLY_NONCLAIM",
            "source_basis": "P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv",
            "effect": "formula shape exists but not numeric",
            "valid_for_claim": "False",
        },
        {
            "factor_id": "TF4358_1_source_worldtube",
            "factor": "T_source^Earth(x)",
            "required_object": "profile-weighted Earth/source stress-current in observed local frame",
            "current_status": "MISSING_SOURCE_PROFILE_WEIGHTING",
            "source_basis": "P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
            "effect": "tau_WEP cannot be evaluated",
            "valid_for_claim": "False",
        },
        {
            "factor_id": "TF4358_2_orbit_average",
            "factor": "orbit/session/mask average",
            "required_object": "time-weighted projection into the reported MICROSCOPE eta channel",
            "current_status": "MISSING_ORBIT_AVERAGE_ARRAYS",
            "source_basis": "P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv",
            "effect": "tau normalization open",
            "valid_for_claim": "False",
        },
        {
            "factor_id": "TF4358_3_material_tensor",
            "factor": "Ti/Pt material response",
            "required_object": "TA6V-minus-PtRh10 response tensor in same source-weight convention",
            "current_status": "MISSING_FULL_MATERIAL_TENSOR",
            "source_basis": "1596 factor audit / 1225 projection attempt",
            "effect": "Delta_w_TiPt mapping incomplete",
            "valid_for_claim": "False",
        },
        {
            "factor_id": "TF4358_4_readout_matrix",
            "factor": "K_MICROSCOPE / K_CMSM",
            "required_object": "official readout/design matrix with masks, timing, orbit/attitude convention and units",
            "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "source_basis": "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
            "effect": "no surrogate kernel can promote WEP claim",
            "valid_for_claim": "False",
        },
        {
            "factor_id": "TF4358_5_product_convention",
            "factor": "eta product normalization",
            "required_object": "map source response x material response x readout kernel to reported Eotvos eta",
            "current_status": "NORMALIZATION_NOT_FILLED",
            "source_basis": "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
            "effect": "tau_WEP=1 shortcut forbidden",
            "valid_for_claim": "False",
        },
    ]


def delta_w_rows() -> List[Dict[str, str]]:
    return [
        {
            "delta_id": "DW4358_0_product_anchor",
            "quantity": "abs(Delta_w_TiPt * tau_WEP)",
            "value_or_law": "<= 2.8e-15",
            "evidence": "MICROSCOPE R1_WEP_source_charge source-backed bound anchor",
            "numeric_status": "AVAILABLE_PRODUCT_ONLY",
            "claim_status": "NONCLAIM_BOUND_INPUT",
            "valid_for_claim": "False",
        },
        {
            "delta_id": "DW4358_1_tau_min",
            "quantity": "tau_min",
            "value_or_law": "need abs(tau_WEP) >= tau_min > 0",
            "evidence": "not sourced in current corpus",
            "numeric_status": "MISSING_POSITIVE_LOWER_BOUND",
            "claim_status": "BLOCKS_DELTA_W_BOUND",
            "valid_for_claim": "False",
        },
        {
            "delta_id": "DW4358_2_delta_w_bound",
            "quantity": "abs(Delta_w_TiPt)",
            "value_or_law": "if tau_min exists, abs(Delta_w_TiPt) <= 2.8e-15/tau_min",
            "evidence": "exact amplitude law from product bound",
            "numeric_status": "SYMBOLIC_ONLY",
            "claim_status": "NO_NUMERIC_DELTA_W_YET",
            "valid_for_claim": "False",
        },
        {
            "delta_id": "DW4358_3_transition_hair",
            "quantity": "Y_species_frame_source projection",
            "value_or_law": "P_WEP[Y_species_frame_source] <= 2.8e-15 as a product-channel bound only",
            "evidence": "WEP anchor plus tau bridge",
            "numeric_status": "PRODUCT_CHANNEL_BOUND_ONLY",
            "claim_status": "NO_LOCAL_GR_REENTRY",
            "valid_for_claim": "False",
        },
    ]


def transition_update_rows() -> List[Dict[str, str]]:
    return [
        {
            "update_id": "TU4358_0_species_hair",
            "4357_object": "Y_species_frame_source",
            "4358_update": "converted the MICROSCOPE anchor from a loose finite input into an exact product-to-amplitude bridge",
            "new_law": "abs(Delta_w_TiPt*tau_WEP)<=2.8e-15; if tau_min>0 then abs(Delta_w_TiPt)<=2.8e-15/tau_min",
            "remaining_gap": "source-backed tau_min or action-measure theorem-zero",
            "valid_for_claim": "False",
        },
        {
            "update_id": "TU4358_1_common_mode_zero",
            "4357_object": "action-measure owner route",
            "4358_update": "last-gate evidence imported; still unsigned",
            "new_law": "Delta_w_TiPt=0 only if common action-measure owner/no-w_A theorem is parent-signed",
            "remaining_gap": "parent measure/action-scale owner",
            "valid_for_claim": "False",
        },
        {
            "update_id": "TU4358_2_local_GR_gate",
            "4357_object": "local GR source coupling branch",
            "4358_update": "local GR remains blocked not because the WEP anchor is absent, but because tau_WEP injectivity is unproved",
            "new_law": "product bound is compatible with arbitrarily large Delta_w if tau_WEP approaches zero",
            "remaining_gap": "positive projection lower bound or zero theorem",
            "valid_for_claim": "False",
        },
    ]


def lower_bound_requirement_rows() -> List[Dict[str, str]]:
    return [
        {
            "requirement_id": "LBR4358_0_tau_min_source",
            "target": "P_WEP_tau_min_lower_bound.csv",
            "required_fields": "tau_min; confidence; source_path; extraction_method; sign/absolute convention; assumptions; branch_id",
            "acceptance_rule": "strictly positive numeric tau_min fixed before Delta_w scoring",
            "why_needed": "turn product anchor into Delta_w amplitude bound",
            "priority": "highest",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "LBR4358_1_official_readout",
            "target": "K_MICROSCOPE / K_CMSM arrays",
            "required_fields": "time; segment/session id; gx/gz/Sxx/Sxz or equivalent; masks; calibration flags; attitude/orbit convention",
            "acceptance_rule": "official export or validated exact equivalent with units",
            "why_needed": "evaluate or bound tau_WEP",
            "priority": "highest",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "LBR4358_2_source_worldtube",
            "target": "T_source^Earth(x)",
            "required_fields": "profile/stress-current convention; observed coframe; orbit weighting; source path",
            "acceptance_rule": "same branch and same normalization as readout kernel",
            "why_needed": "source-weight residual projection",
            "priority": "high",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "LBR4358_3_action_measure_zero",
            "target": "parent_action_measure_owner_theorem",
            "required_fields": "single action scale/measure; ordinary matter sector ownership; no w_A slot; boundary/readout order",
            "acceptance_rule": "parent-signed theorem, not a convention or post-variation redefinition",
            "why_needed": "kill Delta_w_TiPt without finite WEP projection",
            "priority": "highest_parallel",
            "valid_for_claim": "False",
        },
    ]


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "TH4358_0_product_to_amplitude",
            "statement": "A source-backed MICROSCOPE product bound gives an individual Delta_w_TiPt bound only if tau_WEP has a strictly positive sourced lower bound.",
            "derivation": "abs(Delta_w_TiPt*tau_WEP)<=2.8e-15 and abs(tau_WEP)>=tau_min>0 imply abs(Delta_w_TiPt)<=2.8e-15/tau_min.",
            "consequence": "tau_min is now the concrete bridge target for bounding source-label transition hair.",
            "status": "EXACT_CONDITIONAL_LAW_DERIVED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4358_1_tau_null_escape",
            "statement": "If tau_WEP can vanish or be arbitrarily small, the product bound does not constrain Delta_w_TiPt.",
            "derivation": "For any finite product bound B, |Delta_w| can grow as |tau_WEP| -> 0 while |Delta_w*tau_WEP|<=B.",
            "consequence": "tau_WEP=1 and identity projection are forbidden shortcuts.",
            "status": "NO_SHORTCUT_THEOREM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4358_2_action_measure_unsigned",
            "statement": "The action-measure owner route would kill w_A, but current corpus evidence does not parent-sign it.",
            "derivation": "Classical equations and current-owner arguments do not remove weights inserted before variation; 1078/1596 keep common measure as unsigned.",
            "consequence": "finite Delta_w/tau route remains active.",
            "status": "ZERO_ROUTE_OPEN_NOT_CLOSED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4358_3_transition_branch_update",
            "statement": "4358 improves the transition source-coupling gate from a generic missing tau row to a precise tau_min or action-measure fork.",
            "derivation": "4357 finite WEP anchor plus 1596 amplitude law yields the bridge; 1225/1083/1084 specify missing projection factors.",
            "consequence": "next work can hunt a positive projection lower bound instead of circling the coupling label.",
            "status": "REAL_NARROWING_NONCLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def arena_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for arena, observable, requirement in ARENAS:
        rows.append(
            {
                "arena_id": f"AR4358_{arena}",
                "arena": arena,
                "observable": observable,
                "4358_requirement": requirement,
                "zero_route": "parent action-measure/no-w_A theorem",
                "finite_route": "tau_min>0 plus product-bound amplitude law",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4358_0_action_measure",
            "input": "parent action-measure owner signed",
            "action": "SET_DELTA_W_ZERO",
            "result": "Y_species_frame_source zero route can close",
            "current_result": "REJECT_ZERO_CLAIM_NOW",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4358_1_product_bound",
            "input": "MICROSCOPE R1 product anchor",
            "action": "ACCEPT_PRODUCT_ONLY",
            "result": "abs(Delta_w_TiPt*tau_WEP)<=2.8e-15",
            "current_result": "BOUND_INPUT_ACCEPTED_NONCLAIM",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4358_2_delta_w",
            "input": "product anchor without tau_min",
            "action": "REJECT_DELTA_W_SCORE",
            "result": "no numeric Delta_w_TiPt bound",
            "current_result": "BLOCKED_BY_TAU_MIN",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4358_3_tau_min",
            "input": "future tau_min>0",
            "action": "COMPUTE_DELTA_W_BOUND",
            "result": "abs(Delta_w_TiPt)<=2.8e-15/tau_min",
            "current_result": "READY_FORMULA_WAITING_FOR_INPUT",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4358_4_next",
            "input": "no action-measure zero and no tau_min",
            "action": "SELECT_TAU_MIN_OR_ZERO_PROOF_TARGET",
            "result": NEXT_TARGET,
            "current_result": "NEXT_TARGET_SELECTED",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4358_0",
            "rule": "Do not turn abs(Delta_w_TiPt*tau_WEP)<=2.8e-15 into abs(Delta_w_TiPt)<=2.8e-15.",
            "reason": "that silently assumes tau_WEP=1; tau_WEP is a physical source/readout projection.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4358_1",
            "rule": "Do not use an upper bound on tau_WEP to bound Delta_w_TiPt.",
            "reason": "individual amplitude bound requires a strictly positive lower bound tau_min.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4358_2",
            "rule": "Do not claim action-measure owner from classical matter equations or post-variation current ownership.",
            "reason": "pre-variation w_A survives those arguments.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4358_3",
            "rule": "Do not score WEP/local GR without official readout/source-worldtube/material/projection convention.",
            "reason": "tau_WEP and tau_min cannot be numeric without those factors.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4358_4",
            "rule": "Do not absorb Delta_w or source-label hair into measured G.",
            "reason": "relative/source-dependent weights are physical unless a common derivative-silent theorem closes.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4358_0",
            "decision": DECISION,
            "reason": "4358 imports the 1596 product-to-amplitude law into the transition common-mode source-coupling branch. The action-measure owner route remains the clean zero theorem for w_A, but it is still unsigned. The finite route is now exact: MICROSCOPE gives a source-backed product bound abs(Delta_w_TiPt*tau_WEP)<=2.8e-15; it becomes an individual source-weight bound only if a strictly positive tau_min is sourced, giving abs(Delta_w_TiPt)<=2.8e-15/tau_min. Current corpus has a symbolic tau_WEP functional and factor audit, but source worldtube, orbit/mask average, material tensor, official readout matrix and normalization are missing. Therefore 4358 narrows the next target to tau_min>0 or a parent action-measure zero proof.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4358_0",
            "item": "product bound",
            "status": "SOURCE_BACKED_AND_IMPORTED",
            "note": "abs(Delta_w_TiPt*tau_WEP)<=2.8e-15.",
        },
        {
            "status_id": "STAT4358_1",
            "item": "amplitude law",
            "status": "DERIVED_CONDITIONAL",
            "note": "abs(Delta_w_TiPt)<=2.8e-15/tau_min if tau_min>0 is sourced.",
        },
        {
            "status_id": "STAT4358_2",
            "item": "tau_WEP",
            "status": "SYMBOLIC_FUNCTIONAL_ONLY",
            "note": "source/readout/material/orbit factors missing.",
        },
        {
            "status_id": "STAT4358_3",
            "item": "action-measure owner",
            "status": "UNSIGNED_ZERO_ROUTE",
            "note": "cleanest way to kill w_A remains open.",
        },
        {
            "status_id": "STAT4358_4",
            "item": "next target",
            "status": "TAU_MIN_OR_ACTION_MEASURE_ZERO",
            "note": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4358_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can we derive a strictly positive tau_WEP lower bound from source/readout geometry, or parent-sign the action-measure owner that kills w_A?",
            "preferred_route": "derive tau_min>0 from the symbolic tau_WEP functional using source worldtube, readout kernel, material tensor and normalization signs",
            "fallback_route": "close the parent action-measure/no-w_A theorem; if neither closes, keep only the product-bound nonclaim",
            "valid_for_claim": "False",
        }
    ]


def build_tables() -> Dict[str, List[Dict[str, str]]]:
    return {
        "sources": source_rows(),
        "action_measure": action_measure_rows(),
        "tau_bridge": tau_bridge_rows(),
        "tau_factors": tau_factor_rows(),
        "delta_w": delta_w_rows(),
        "transition_updates": transition_update_rows(),
        "lower_bound_requirements": lower_bound_requirement_rows(),
        "theorems": theorem_rows(),
        "arenas": arena_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }


def write_tables(tables: Dict[str, List[Dict[str, str]]]) -> None:
    mapping = {
        "sources": "P8_Y5_R2FR_4358_SOURCE_REGISTER.csv",
        "action_measure": "P8_Y5_R2FR_4358_ACTION_MEASURE_AUDIT.csv",
        "tau_bridge": "P8_Y5_R2FR_4358_TAU_WEP_BRIDGE_ROWS.csv",
        "tau_factors": "P8_Y5_R2FR_4358_TAU_FACTOR_ROWS.csv",
        "delta_w": "P8_Y5_R2FR_4358_DELTA_W_AMPLITUDE_ROWS.csv",
        "transition_updates": "P8_Y5_R2FR_4358_TRANSITION_UPDATE_ROWS.csv",
        "lower_bound_requirements": "P8_Y5_R2FR_4358_LOWER_BOUND_REQUIREMENTS.csv",
        "theorems": "P8_Y5_R2FR_4358_THEOREM_ROWS.csv",
        "arenas": "P8_Y5_R2FR_4358_ARENA_ROWS.csv",
        "runner": "P8_Y5_R2FR_4358_RUNNER.csv",
        "firewall": "P8_Y5_R2FR_4358_CLAIM_FIREWALL.csv",
        "decision": "P8_Y5_R2FR_4358_DECISION.csv",
        "status": "P8_Y5_R2FR_4358_STATUS.csv",
        "next": "P8_Y5_R2FR_4358_NEXT_TARGET.csv",
    }
    for key, filename in mapping.items():
        write_csv(SOURCE_DIR / filename, tables[key])


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 374 PPC4161 transition action-measure owner or tau-WEP source projection bridge

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. 4358 does not prove public local GR, Newton, WEP, R10, PPN, clock, orbital, EM, or transition-shell safety.

## Result

4358 imports the 1596 amplitude law into the transition common-mode source-coupling branch.

The clean zero theorem is still:

```text
one parent action-measure owner
+ no pre-variation w_A source/action multiplier
=> Delta_w_TiPt = 0
=> Y_species_frame_source = 0.
```

That theorem is not parent-signed in the current corpus. Classical equations and post-variation current ownership do not kill a weight inserted before metric variation.

So the finite route is the WEP projection bridge:

```text
eta_TiPt = Delta_w_TiPt * tau_WEP
         + O((Delta_w_TiPt*tau_WEP)^2)
         + R_readout_tail.
```

The source-backed MICROSCOPE anchor gives:

```text
abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15.
```

This is a product bound. It becomes an individual amplitude bound only if a positive projection lower bound is sourced:

```text
if abs(tau_WEP) >= tau_min > 0,
then abs(Delta_w_TiPt) <= 2.8e-15/tau_min.
```

If `tau_WEP` can vanish or be arbitrarily small, the product bound does not constrain `Delta_w_TiPt`. So `tau_WEP=1` is forbidden as a convention; `tau_min` is now the actual target.

## tau-WEP Functional

The current symbolic functional is:

```text
tau_WEP :=
N_eta^-1 < K_eta[e_obs, orbit, masks]
  Integral_Earth dV K_source(x;orbit) R_source(x)
  R_material(TiPt) >_orbit.
```

Current blockers are source worldtube/profile, orbit/session masks, full Ti/Pt material tensor, official MICROSCOPE readout matrix, product normalization, and parent coupling/action-measure owner.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role", "valid_for_claim"])}

## Action Measure Audit

{md_table(tables["action_measure"], ["audit_id", "route", "would_close", "current_evidence", "result", "effect", "valid_for_claim"])}

## tau-WEP Bridge Rows

{md_table(tables["tau_bridge"], ["bridge_id", "object", "law", "meaning", "status", "valid_for_claim"])}

## tau Factor Rows

{md_table(tables["tau_factors"], ["factor_id", "factor", "required_object", "current_status", "source_basis", "effect", "valid_for_claim"])}

## Delta-w Amplitude Rows

{md_table(tables["delta_w"], ["delta_id", "quantity", "value_or_law", "evidence", "numeric_status", "claim_status", "valid_for_claim"])}

## Transition Update Rows

{md_table(tables["transition_updates"], ["update_id", "4357_object", "4358_update", "new_law", "remaining_gap", "valid_for_claim"])}

## Lower Bound Requirements

{md_table(tables["lower_bound_requirements"], ["requirement_id", "target", "required_fields", "acceptance_rule", "why_needed", "priority", "valid_for_claim"])}

## Theorem Rows

{md_table(tables["theorems"], ["theorem_id", "statement", "derivation", "consequence", "status", "claim_allowed", "valid_for_claim"])}

## Arena Rows

{md_table(tables["arenas"], ["arena_id", "arena", "observable", "4358_requirement", "zero_route", "finite_route", "claim_allowed", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "input", "action", "result", "current_result", "valid_for_claim"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "rule", "reason", "status", "valid_for_claim"])}

## Decision

{md_table(tables["decision"], ["decision_id", "decision", "reason", "next_action", "claim_allowed", "valid_for_claim"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "note"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route", "valid_for_claim"])}
"""
    post = f"""# 4358 Y5-R2FR transition action-measure owner or tau-WEP source projection bridge

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4358 gives the exact bridge from the MICROSCOPE product anchor to an actual source-weight amplitude:

```text
abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15
```

implies:

```text
abs(Delta_w_TiPt) <= 2.8e-15/tau_min
```

only if:

```text
abs(tau_WEP) >= tau_min > 0.
```

No `tau_WEP=1` shortcut. No measured-G absorption. No WEP/local-GR score yet.

## Next

{md_table(tables["next"], ["next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path)
    if CLAIM_ID in existing:
        return
    with path.open("a", newline="", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        csv.writer(handle).writerow(
            [
                CLAIM_ID,
                "local_gr",
                (
                    "4358 imports the 1596 tau-WEP product-to-amplitude law into the transition common-mode source-coupling branch. The clean zero route remains a parent-signed action-measure/no-w_A theorem, but current evidence does not close it: classical equations and current-owner arguments do not remove pre-variation action weights. The finite route is now exact: MICROSCOPE gives abs(Delta_w_TiPt*tau_WEP)<=2.8e-15, and if a source-backed positive lower bound abs(tau_WEP)>=tau_min>0 is supplied, then abs(Delta_w_TiPt)<=2.8e-15/tau_min. If tau_WEP can vanish or be arbitrarily small, the product bound does not constrain Delta_w_TiPt. Current tau_WEP is symbolic only; source worldtube/profile, orbit/mask average, material tensor, official readout matrix, product normalization and parent coupling owner remain missing. No WEP/local-GR/Newton/PPN/R10/clock/orbital claim fires."
                ),
                (
                    "4358 source register, action-measure audit, tau-WEP bridge rows, tau factor rows, Delta-w amplitude rows, transition update rows, lower-bound requirements, theorem rows, arena rows, runner, firewall, decision, status, next-target and validation CSV."
                ),
                "tau_WEP_product_to_amplitude_bridge_derived_tau_min_or_action_measure_zero_needed_nonclaim",
                (
                    "Derive tau_min>0 from source/readout geometry or parent-sign the action-measure/no-w_A theorem."
                ),
                (
                    "Setting tau_WEP=1 by convention; using an upper bound on tau to bound Delta_w; claiming action-measure owner from classical equations; scoring WEP/local GR without source worldtube/readout/material/normalization; absorbing Delta_w into measured G."
                ),
            ]
        )


def append_spine_and_packet() -> None:
    spine_block = f"""

## PPC4161 4358 transition tau-WEP product-to-amplitude bridge

Marker: `{MARKER}`

4358 turns the finite WEP anchor into an exact amplitude fork:

```text
abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15.
```

This implies an individual source-weight bound only if:

```text
abs(tau_WEP) >= tau_min > 0
=> abs(Delta_w_TiPt) <= 2.8e-15/tau_min.
```

If `tau_WEP` can vanish, the product bound gives no finite `Delta_w_TiPt` bound. The action-measure/no-`w_A` route remains the clean zero theorem but is unsigned. Next target: derive `tau_min>0` from source/readout geometry or close the action-measure theorem.
"""
    packet_block = f"""

## PPC4161 packet update 4358 tau-WEP bridge

Marker: `{PACKET_MARKER}`

Packet update: the WEP source-weight anchor is now a precise product bound, not a loose missing row. The next hard target is a positive `tau_WEP` lower bound or a parent-signed action-measure owner that kills `w_A`.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)


def validate(tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    checks: List[Tuple[str, bool, str]] = []
    formal_text = read_text(FORMAL_PATH)
    checks.append(("formal_doc_written", FORMAL_PATH.exists(), str(FORMAL_PATH)))
    checks.append(("post_doc_written", DOC_PATH.exists(), str(DOC_PATH)))
    checks.append(("marker_in_formal", MARKER in formal_text, MARKER))
    checks.append(("decision_in_formal", DECISION in formal_text, DECISION))
    checks.append(("product_bound_present", "abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15" in formal_text, "product bound"))
    checks.append(("amplitude_law_present", "abs(Delta_w_TiPt) <= 2.8e-15/tau_min" in formal_text, "amplitude law"))
    checks.append(("tau_min_condition_present", "abs(tau_WEP) >= tau_min > 0" in formal_text, "tau min condition"))
    checks.append(("tau_unity_rejected", "tau_WEP=1" in formal_text, "tau unity shortcut rejected"))
    checks.append(("tau_functional_present", "tau_WEP :=" in formal_text, "tau functional"))
    checks.append(("action_owner_unsigned_present", "not parent-signed" in formal_text, "action-measure owner unsigned"))
    checks.append(("all_sources_exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source paths"))
    checks.append(("all_needles_found", all(row["needle_found"] == "True" for row in tables["sources"]), "source needles"))
    checks.append(("action_measure_rows_present", len(tables["action_measure"]) >= 4, str(len(tables["action_measure"]))))
    checks.append(("tau_bridge_rows_present", len(tables["tau_bridge"]) >= 4, str(len(tables["tau_bridge"]))))
    checks.append(("tau_factor_rows_present", len(tables["tau_factors"]) >= 6, str(len(tables["tau_factors"]))))
    checks.append(("delta_w_rows_present", len(tables["delta_w"]) >= 4, str(len(tables["delta_w"]))))
    checks.append(("lower_bound_requirements_present", len(tables["lower_bound_requirements"]) >= 4, str(len(tables["lower_bound_requirements"]))))
    checks.append(("theorem_rows_present", len(tables["theorems"]) >= 4, str(len(tables["theorems"]))))
    checks.append(("arena_rows_present", len(tables["arenas"]) == len(ARENAS), str(len(tables["arenas"]))))
    checks.append(("no_valid_claim_rows", all(row.get("valid_for_claim") == "False" for rows in tables.values() for row in rows if "valid_for_claim" in row), "all generated claim flags false"))
    checks.append(("claim_row_recorded", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), CLAIM_ID))
    checks.append(("spine_marker_recorded", MARKER in read_text(FORMAL / "07-unification-spine.md"), MARKER))
    checks.append(("packet_marker_recorded", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), PACKET_MARKER))
    for filename in [
        "P8_Y5_R2FR_4358_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4358_ACTION_MEASURE_AUDIT.csv",
        "P8_Y5_R2FR_4358_TAU_WEP_BRIDGE_ROWS.csv",
        "P8_Y5_R2FR_4358_TAU_FACTOR_ROWS.csv",
        "P8_Y5_R2FR_4358_DELTA_W_AMPLITUDE_ROWS.csv",
        "P8_Y5_R2FR_4358_TRANSITION_UPDATE_ROWS.csv",
        "P8_Y5_R2FR_4358_LOWER_BOUND_REQUIREMENTS.csv",
        "P8_Y5_R2FR_4358_THEOREM_ROWS.csv",
        "P8_Y5_R2FR_4358_ARENA_ROWS.csv",
        "P8_Y5_R2FR_4358_RUNNER.csv",
        "P8_Y5_R2FR_4358_CLAIM_FIREWALL.csv",
        "P8_Y5_R2FR_4358_DECISION.csv",
        "P8_Y5_R2FR_4358_STATUS.csv",
        "P8_Y5_R2FR_4358_NEXT_TARGET.csv",
    ]:
        path = SOURCE_DIR / filename
        rows = list(csv.DictReader(path.open(newline="", encoding="utf-8"))) if path.exists() else []
        checks.append((f"csv_{filename}_parse_rows", bool(rows), f"{len(rows)} rows"))
    return [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "passed": str(bool(passed)),
            "detail": detail,
            "valid_for_claim": "False",
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    tables = build_tables()
    write_tables(tables)
    write_docs(tables)
    append_claim_once()
    append_spine_and_packet()
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    failures = [row for row in validation_rows if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote 14 csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation_rows)} failed={len(failures)}")
    if failures:
        for row in failures:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
