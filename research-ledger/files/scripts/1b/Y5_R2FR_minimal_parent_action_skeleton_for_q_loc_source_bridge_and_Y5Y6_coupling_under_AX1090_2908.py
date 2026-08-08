from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2908-Y5-R2FR-minimal-parent-action-skeleton-for-q_loc-source-bridge-and-Y5Y6-coupling-under-AX1090.md"

SRC_2907_DOC = ROOT / "2907-Y5-R2FR-MHref-tau-source-frame-surface-lock-or-first-denominator-row-under-AX1090.md"
SRC_2907_NEXT = RESIDUALS / "P8_Y5_R2FR_2907_NEXT_TARGET.csv"
SRC_2907_DENOM_ROWS = RESIDUALS / "P8_Y5_R2FR_2907_DENOMINATOR_SOURCE_ROWS.csv"
SRC_2906_SPLIT = RESIDUALS / "P8_Y5_R2FR_2906_EPSILON_EXTRA_SOURCE_SPLIT.csv"
SRC_2464_DOC = ROOT / "2464-Y5-R2FR-minimal-parent-action-skeleton-for-q_loc-and-source-bridge.md"
SRC_2464_CANDIDATES = RESIDUALS / "P8_Y5_PARENT_ACTION_2464_CANDIDATE_ACTIONS.csv"
SRC_2464_FIELDS = RESIDUALS / "P8_Y5_PARENT_ACTION_2464_FIELD_INVENTORY.csv"
SRC_2464_VARIATION = RESIDUALS / "P8_Y5_PARENT_ACTION_2464_VARIATION_OWNERSHIP.csv"
SRC_2464_QDER = RESIDUALS / "P8_Y5_PARENT_ACTION_2464_QLOC_DERIVATION_ATTEMPT.csv"
SRC_2464_SOURCE_BRIDGE = RESIDUALS / "P8_Y5_PARENT_ACTION_2464_SOURCE_BRIDGE_CONTRACT.csv"
SRC_2464_LAWS = RESIDUALS / "P8_Y5_PARENT_ACTION_2464_LOCAL_VACUUM_AMPLITUDE_LAW.csv"
SRC_2463_PREREQ = RESIDUALS / "P8_Y5_LOCAL_GR_2463_PREREQUISITE_MATRIX.csv"
SRC_2462_REOPEN = RESIDUALS / "P8_Y5_PARENT_QLOC_2462_REOPEN_MATERIAL_SPEC.csv"
SRC_ACTION_BLOCKS = RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"
SRC_SYMBOL_MAP = RESIDUALS / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv"
SRC_VARIATION_GATES = RESIDUALS / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv"
SRC_1619_NORMAL = RESIDUALS / "P8_Y5_PARENT_QLOC_1619_POSITIVE_AUXILIARY_NORMAL_FORM.csv"
SRC_1619_GAPS = RESIDUALS / "P8_Y5_PARENT_QLOC_1619_PARENT_SIGNATURE_GAP_LEDGER.csv"
SRC_1620_BRIDGE = RESIDUALS / "P8_Y5_PARENT_QLOC_1620_PARENT_SIGNATURE_BRIDGE_CONTRACT.csv"
SRC_1620_CHAIN = RESIDUALS / "P8_Y5_PARENT_QLOC_1620_CHAIN_RULE_SOURCE_CURRENT_ZERO_ATTEMPT.csv"
SRC_1620_BOUNDS = RESIDUALS / "P8_Y5_PARENT_QLOC_1620_SOURCE_CURRENT_BOUND_FILL_ROWS.csv"
SRC_1030_DOC = ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2908_SOURCE_REGISTER.csv",
    "skeleton": RESIDUALS / "P8_Y5_R2FR_2908_PARENT_ACTION_SKELETON.csv",
    "variation": RESIDUALS / "P8_Y5_R2FR_2908_VARIATION_AND_QLOC_DERIVATION.csv",
    "coupling": RESIDUALS / "P8_Y5_R2FR_2908_Y5Y6_COUPLING_OWNER_AUDIT.csv",
    "laws": RESIDUALS / "P8_Y5_R2FR_2908_LOCAL_VACUUM_AND_AMPLITUDE_LAWS.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2908_RUNNER_STATUS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2908_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2908_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2908_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2908_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2908_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "skeleton_copy": RAB_QUEUE / "JR2908_PARENT_ACTION_SKELETON_NONCLAIM.csv",
    "coupling_copy": LOCAL_BOUNDS / "Y5Y6_coupling_owner_audit_2908_NONCLAIM.csv",
    "next_copy": PARENT_ACTION / "Source_current_descent_Y5Y6_next_2908_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2908_00_2907_doc", SRC_2907_DOC, "NEXT2907_0_2908;smallest parent-action skeleton", "current handoff selecting parent-action skeleton"),
        ("SRC2908_01_2907_next", SRC_2907_NEXT, "NEXT2907_0_2908;Gamma/Khat/q_loc, Pi_M/worldtube source bridge, Y5 source normalization and Y6 extra-stress coupling", "machine-readable 2908 target"),
        ("SRC2908_02_2907_denominator_rows", SRC_2907_DENOM_ROWS, "DROW2907_8_denominator_reopen_material;DROW2907_TOTAL", "denominator rows that force parent-action route"),
        ("SRC2908_03_2906_Y5Y6_split", SRC_2906_SPLIT, "epsilon_extra_odd_source_Y5;epsilon_extra_odd_source_Y6;epsilon_extra_odd_source_Y5Y6_total", "Y5/Y6 coupling pressure to be owned"),
        ("SRC2908_04_2464_doc", SRC_2464_DOC, "ACT2464_A_vertical_generator_current_law;QDER2464_1_vary_A;SRCBR2464_0_current_origin;LAW2464_1_F1_zero", "constructive q_loc parent-action candidate"),
        ("SRC2908_05_2464_candidates", SRC_2464_CANDIDATES, "ACT2464_A_vertical_generator_current_law;BEST_CONSTRUCTIVE_CANDIDATE_BUT_NONCLAIM", "candidate action rows"),
        ("SRC2908_06_2464_fields", SRC_2464_FIELDS, "FLD2464_2_vertical_generator;FLD2464_5_source_current;FLD2464_6_projector", "field inventory for q_loc skeleton"),
        ("SRC2908_07_2464_variation", SRC_2464_VARIATION, "VAR2464_0_delta_A;VAR2464_3_delta_metric;VAR2464_5_boundary", "variation ownership audit"),
        ("SRC2908_08_2464_qder", SRC_2464_QDER, "QDER2464_1_vary_A;QDER2464_4_not_promoted", "q_loc formal derivation attempt"),
        ("SRC2908_09_2464_source_bridge", SRC_2464_SOURCE_BRIDGE, "SRCBR2464_0_current_origin;SRCBR2464_4_universality", "J_M source bridge requirements"),
        ("SRC2908_10_2464_laws", SRC_2464_LAWS, "LAW2464_1_F1_zero;LAW2464_2_Delta_m_bound;LAW2464_3_transition_length", "conditional local laws"),
        ("SRC2908_11_2463_prereq", SRC_2463_PREREQ, "PRE2463_1_variational_origin_q_loc;PRE2463_2_source_bridge;PRE2463_4_local_vacuum_double_zero", "route prerequisites"),
        ("SRC2908_12_2462_reopen", SRC_2462_REOPEN, "MAT2462_0_action_source;MAT2462_3_GK_pack;MAT2462_4_source_pack", "parent-action reopen material"),
        ("SRC2908_13_action_blocks", SRC_ACTION_BLOCKS, "A511_0_EH_core;A511_2_universal_matter;A511_6_metric_readout", "minimum local-GR action blocks"),
        ("SRC2908_14_symbol_map", SRC_SYMBOL_MAP, "Gamma_eff;K_hat;Pi_M;M_eff / M_source / Q_M", "symbol-to-action placement map"),
        ("SRC2908_15_variation_gates", SRC_VARIATION_GATES, "FV512_2_Gamma_Khat_q;FV512_5_mass_projector", "first-variation gates"),
        ("SRC2908_16_1619_normal", SRC_1619_NORMAL, "NF1619_6_verdict;FORMAL_MECHANISM_EXISTS_NOT_PARENT_SIGNED", "positive auxiliary/response-doublet formal mechanism"),
        ("SRC2908_17_1619_gaps", SRC_1619_GAPS, "GAP1619_7_verdict;PARENT_SIGNATURE_OPEN_NO_PROMOTION", "parent-signature gaps after normal form"),
        ("SRC2908_18_1620_bridge", SRC_1620_BRIDGE, "BRC1620_0_Z_map;BRC1620_6_verdict", "parent signature bridge contract"),
        ("SRC2908_19_1620_chain", SRC_1620_CHAIN, "CR1620_1_zero_lemma;CR1620_5_verdict", "chain-rule source-current zero lemma"),
        ("SRC2908_20_1620_bounds", SRC_1620_BOUNDS, "SCB1620_0_JZ_bulk;SCB1620_4_PPN_source_lock", "fallback source-current bound rows"),
        ("SRC2908_21_1030_doc", SRC_1030_DOC, "SPM1030_0_public_metric_object;SPM1030_6_contract_verdict", "single public metric/source-side contract"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        anchors_found, missing_anchors = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": anchors_found,
                    "missing_anchors": missing_anchors,
                }
            )
        )
    return rows


def skeleton_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ACT2908_0_public_metric_EH",
            "S_EH[g_obs,kappa0] plus one public observed coframe",
            "owns spin-2 local GR operator and gives the geometry seen by rods/clocks/matter",
            "A511_0_EH_core;A511_2_universal_matter;SPM1030",
            "CONTRACT_ANCHOR_NOT_FULL_PARENT_DERIVATION",
            "same public metric/coframe not yet parent-signed for all readouts",
            SRC_ACTION_BLOCKS,
        ),
        (
            "ACT2908_1_universal_matter_source",
            "S_matter[psi,e_obs] with Hilbert current J_H and no pre-action source weights",
            "locks the source side of Newton/PPN to the same matter action rather than fitted GM",
            "A511_2_universal_matter;BRC1620_2_matter_descent;CR1620_1_zero_lemma",
            "CONDITIONAL_CHAIN_RULE_AVAILABLE_APPLICATION_BLOCKED",
            "matter descent, no-marker/current-owner and boundary clauses remain unsigned",
            SRC_1620_CHAIN,
        ),
        (
            "ACT2908_2_vertical_generator_current_law",
            "S_GK=int sqrt(-g)[L_K(g,tau,nabla A)+A_nu nabla^nu Gamma_eff-A_nu J_M^nu+L_Gamma]",
            "variation of A_nu formally gives nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu} - J_M^nu = 0",
            "ACT2464_A_vertical_generator_current_law",
            "FORMAL_QLOC_EULER_OWNER_CANDIDATE",
            "A_nu, L_K, L_Gamma, J_M and P_loc are still new parent material",
            SRC_2464_CANDIDATES,
        ),
        (
            "ACT2908_3_response_doublet_extra_stress",
            "positive auxiliary/response-doublet normal form for local extra fields Z^A",
            "can make F1/local linear residual vanish if actual MTS residuals map to Z and source current is zero",
            "NF1619_6_verdict;GAP1619_7_verdict",
            "FORMAL_MECHANISM_EXISTS_NOT_PARENT_SIGNED",
            "actual MTS Z map, verticality, boundary silence and PPN/source lock remain open",
            SRC_1619_NORMAL,
        ),
        (
            "ACT2908_4_PiM_worldtube_source_bridge",
            "Pi_M/worldtube/source-measure bridge attaches J_M/J_H to compact source surfaces",
            "would connect q_loc source current to Newtonian source mass without orbital-GM circularity",
            "MAT2462_4_source_pack;SRCBR2464_0_current_origin",
            "MISSING_SOURCE_BRIDGE",
            "source charge and linking surfaces are still not parent-owned",
            SRC_2464_SOURCE_BRIDGE,
        ),
        (
            "ACT2908_5_selector_projector_owner",
            "P_loc and Pi_M are parent readout/projector operators, not data-chosen masks",
            "prevents projectors from adding hidden PPN/source-normalization stress",
            "A511_4_domain_projector_selector;FV512_5_mass_projector",
            "OPEN_PROJECTOR_OWNER",
            "projector variation/stress and mass-projector equality remain unproved",
            SRC_VARIATION_GATES,
        ),
        (
            "ACT2908_6_boundary_reference_guard",
            "fixed boundary/reference terms only after parent action ownership",
            "blocks H_ref/B_ref/counterterm laundering and local plateau axioms",
            "MAT2462_5_reference_pack;DROW2907_5_Delta_Htau_Href_integrability",
            "GUARDRAIL_ACTIVE_NOT_THEOREM",
            "fixed-reference and no-flux clauses are not signed",
            SRC_2907_DENOM_ROWS,
        ),
        (
            "ACT2908_7_total_verdict",
            "minimal parent-action skeleton for q_loc/source bridge/Y5Y6 coupling",
            "combines EH/public metric, universal matter, vertical-generator q_loc law, response-doublet local silence, source bridge and readout guards",
            "ACT2908_0 through ACT2908_6",
            "SKELETON_WRITTEN_NOT_PROMOTED",
            "formal q_loc algebra is promising, but source-current descent/Y5Y6 coupling ownership is still the hard missing proof",
            SRC_2907_NEXT,
        ),
    ]
    return [
        add_common(
            {
                "action_id": action_id,
                "action_block": action_block,
                "purpose": purpose,
                "source_clauses": source_clauses,
                "current_status": current_status,
                "blocking_gap": blocking_gap,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "parent_signed": False,
                "promote_now": False,
            }
        )
        for action_id, action_block, purpose, source_clauses, current_status, blocking_gap, source_path in specs
    ]


def variation_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "VAR2908_0_delta_A_q_loc",
            "A_nu",
            "delta_A S_GK = int sqrt(-g)[-nabla_mu K_hat^{mu nu}+nabla^nu Gamma_eff-J_M^nu] delta A_nu + boundary",
            "q_loc^nu = P_loc^nu_rho J_M^rho after projection",
            "FORMAL_PASS_CANDIDATE",
            "does not promote MTS until A_nu/L_K/J_M/P_loc are parent-sourced",
            SRC_2464_QDER,
        ),
        (
            "VAR2908_1_delta_Gamma_companion",
            "Gamma_eff",
            "-nabla_nu A^nu + partial L_Gamma/partial Gamma_eff = 0 plus boundary",
            "companion equation for compression/connection scalar",
            "CONDITIONAL_ONLY",
            "must not force unphysical clock gauge or nonlocal source response",
            SRC_2464_VARIATION,
        ),
        (
            "VAR2908_2_delta_Z_response_doublet",
            "Z^A local residual coordinates",
            "positive normal form gives L_AB Z^B + source/boundary terms = 0",
            "F1=0 if source and boundary terms vanish and actual MTS maps to Z",
            "FORMAL_NORMAL_FORM_ONLY",
            "actual MTS residual basis and source-current zero are unsigned",
            SRC_1619_NORMAL,
        ),
        (
            "VAR2908_3_delta_matter_source",
            "psi/e_obs matter sector",
            "Hilbert/source variation produces J_H/J_M if matter descends through the public metric",
            "would tie q_loc source to physical source mass/current",
            "MISSING_SOURCE_DESCENT_APPLICATION",
            "chain-rule lemma exists but verticality/descent/no-marker/boundary premises do not fire",
            SRC_1620_CHAIN,
        ),
        (
            "VAR2908_4_delta_metric_Y6_stress",
            "g_obs",
            "Einstein operator equals matter stress plus GK/extra/projector/boundary stress residuals",
            "Y6 extra-stress must be theorem-zero, bounded or included in PPN/local tests",
            "Y6_STRESS_OWNER_OPEN",
            "formal q_loc equation alone does not silence stress in the metric equation",
            SRC_2906_SPLIT,
        ),
        (
            "VAR2908_5_delta_projector_PiM",
            "P_loc/Pi_M",
            "projector/readout variation must be zero, exact, constrained or source-bounded",
            "prevents source-normalization and PPN leakage through the projector itself",
            "PROJECTOR_VARIATION_OPEN",
            "mass-projector equality and projector stress remain failed/current nonclaim gates",
            SRC_VARIATION_GATES,
        ),
        (
            "VAR2908_6_boundary_worldtube",
            "boundary/reference/worldtube data",
            "n_mu K_hat^{mu nu} delta A_nu, Gamma/A surface terms and source-worldtube flux must vanish or be bounded",
            "needed before local vacuum q_loc=0 or M_ref scoring can reopen",
            "BOUNDARY_SOURCE_FLUX_OPEN",
            "bulk Euler equations do not silence boundary leakage",
            SRC_2464_SOURCE_BRIDGE,
        ),
        (
            "VAR2908_7_verdict",
            "full skeleton variation",
            "q_loc Euler equation closes formally, but source, stress, projector and boundary ownership are not current-MTS theorems",
            "skeleton is a serious candidate, not a GR/Newton reduction proof",
            "SKELETON_VARIATION_NONCLAIM",
            "next proof must attack J_M/J_Z source-current descent and Y5/Y6 coupling zero",
            SRC_2907_NEXT,
        ),
    ]
    return [
        add_common(
            {
                "variation_id": variation_id,
                "varied_object": varied_object,
                "formal_variation": formal_variation,
                "would_prove": would_prove,
                "current_status": current_status,
                "remaining_issue": remaining_issue,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "formal_pass": current_status == "FORMAL_PASS_CANDIDATE",
                "parent_signed": False,
                "accepted_for_local_gr": False,
            }
        )
        for variation_id, varied_object, formal_variation, would_prove, current_status, remaining_issue, source_path in specs
    ]


def coupling_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CPL2908_0_Y5_GM_transfer",
            "epsilon_Y5_GM_transfer",
            "parent source current must equal Pi_M/worldtube source charge and slow-orbit readout before fitting",
            "dimensionless after true source norm",
            "MISSING_JM_PIM_WORLDTUBE_EQUALITY",
            SRC_2906_SPLIT,
            "Newton;source_mass;PPN",
            "J_M source descent;Pi_M equality;worldtube bridge;no orbital GM shortcut",
        ),
        (
            "CPL2908_1_Y5_mu_extra",
            "epsilon_Y5_mu_extra_vector",
            "source-normalization offsets from nonEH, boundary, radial, time, species and calibration channels",
            "dimensionless after true source norm",
            "EIGHT_CHANNEL_MU_EXTRA_VECTOR_STILL_OPEN",
            SRC_2906_SPLIT,
            "Newton;PPN;R10;WEP",
            "source-current owner;single public metric;no marker/source weights;boundary silence",
        ),
        (
            "CPL2908_2_JM_source_current",
            "J_M^nu",
            "current appearing in ACT2908_2 must be the parent Hilbert/worldtube matter current, not fitted GM",
            "source_current_units",
            "MISSING_PARENT_SOURCE_CURRENT_DESCENT",
            SRC_2464_SOURCE_BRIDGE,
            "source_mass;Newton;orbital",
            "matter descent;worldtube compact support;universality;external vacuum",
        ),
        (
            "CPL2908_3_JZ_source_zero",
            "J_Z",
            "response-doublet/local residual source current must vanish by quotient descent or be bounded",
            "action_variation_units",
            "CONDITIONAL_CHAIN_RULE_NOT_APPLIED",
            SRC_1620_CHAIN,
            "PPN;R10;local_GR;WEP",
            "Dq[Z]=0;matter descent;no-marker;boundary silence;PPN source lock",
        ),
        (
            "CPL2908_4_Y6_extra_stress",
            "epsilon_extra_odd_source_Y6",
            "extra stress contribution in metric equation must be theorem-zero, q-basic invisible or source-bounded",
            "dimensionless after true source norm",
            "MISSING_Y6_STRESS_PARENT_SIGNATURE",
            SRC_2906_SPLIT,
            "Bianchi;PPN;local_GR",
            "response doublet maps to actual MTS;metric stress double-zero;boundary no-flux",
        ),
        (
            "CPL2908_5_projector_stress",
            "epsilon_Y6_projector_stress",
            "P_loc/Pi_M/readout projector stress must not add hidden source normalization",
            "dimensionless source/stress leakage",
            "MISSING_PROJECTOR_VARIATION_ZERO_OR_BOUND",
            SRC_VARIATION_GATES,
            "source_mass;R11;PPN",
            "projector owner;mass projector equality;metric response",
        ),
        (
            "CPL2908_6_boundary_flux",
            "epsilon_boundary_worldtube_flux",
            "boundary/worldtube terms can leak source current or q_loc even if bulk Euler equation is clean",
            "flux_or_action_boundary_units",
            "MISSING_BOUNDARY_NO_FLUX_OR_BOUND",
            SRC_1620_BOUNDS,
            "clock;orbital;PPN;local_GR",
            "surface class;compact support;proper boundary condition;source-backed flux row",
        ),
        (
            "CPL2908_7_observable_lock",
            "epsilon_Y5Y6_observable_projection",
            "Z/q_loc/Y5/Y6 residual basis must map to PPN, R10, clock, orbital and source-normalization observables with units",
            "mixed_projection_units",
            "MISSING_OBSERVABLE_PROJECTION_AND_UNITS",
            SRC_1620_BOUNDS,
            "PPN;R10;clock;orbital;Newton",
            "arena projection matrices;units;signs;source paths",
        ),
        (
            "CPL2908_TOTAL",
            "epsilon_parent_action_Y5Y6_coupling_total",
            "absolute no-cancellation envelope for source-current descent, Y5 source normalization, Y6 stress, projector and boundary leakage",
            "dimensionless gate",
            "COMPONENTS_MISSING",
            SRC_2906_SPLIT,
            "PPN;R10;clock;orbital;Newton;local_GR",
            "all CPL2908 rows theorem-zero or source-backed bounded in one branch",
        ),
    ]
    return [
        add_common(
            {
                "coupling_id": coupling_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "current_value": current_value,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "observable_link": observable_link,
                "required_before_claim": required_before_claim,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "accepted_for_scoring": False,
            }
        )
        for coupling_id, symbol, definition, units, current_value, source_path, observable_link, required_before_claim in specs
    ]


def law_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "LAW2908_0_q_loc_Euler_source",
            "q_loc^nu",
            "q_loc^nu = P_loc^nu_rho J_M^rho",
            "ACT2908_2 valid; P_loc parent-owned/fixed; boundary terms controlled",
            "local residual becomes a projected physical source current rather than a plateau axiom",
            "CONDITIONAL_CANDIDATE_ONLY",
            SRC_2464_LAWS,
        ),
        (
            "LAW2908_1_F1_zero",
            "F_1",
            "F_1 = 0 in a source-free local collar because q_loc is proportional to J_M plus boundary leakage",
            "J_M=0 outside parent-selected compact source; boundary flux silent; weak-field expansion smooth",
            "linear local fifth-force term is removed by an Euler/source equation",
            "CONDITIONAL_NOT_CURRENT_MTS",
            SRC_2464_LAWS,
        ),
        (
            "LAW2908_2_Delta_m_bound",
            "Delta m / m",
            "abs(Delta m/m) <= C_P*(||P_loc J_M||_collar + ||boundary_flux|| + ||J_Z||)/M_source",
            "source bridge supplies M_source and norms; J_Z/boundary rows are sourced or zero",
            "amplitude leakage is bounded by source-current and boundary debts",
            "BOUND_FORM_ONLY",
            SRC_2464_LAWS,
        ),
        (
            "LAW2908_3_transition_ratio",
            "ell_tr / L_cg",
            "ell_tr/L_cg = 1/(m_tr L_cg) or domain-spectrum equivalent",
            "parent operator supplies positive gap m_tr and independent cosmological scale L_cg",
            "transition length becomes derived from action spectrum rather than fitted switch",
            "PARAMETRIC_ONLY_PARENT_GAP_MISSING",
            SRC_VARIATION_GATES,
        ),
        (
            "LAW2908_4_Newton_source",
            "Newton/source mass",
            "M_source = integral_W J_M = linked surface charge = Pi_M readout before orbital fitting",
            "source-current descent, worldtube compact support, Pi_M equality and no-orbital-GM guard",
            "would reopen source-normalized Newton after local residuals are controlled",
            "NOT_DERIVED_CURRENT_MTS",
            SRC_2907_DENOM_ROWS,
        ),
        (
            "LAW2908_5_current_limit",
            "local GR/Newton/PPN",
            "blocked until all source-current, Y5/Y6 stress, projector, boundary and observable projection rows close",
            "no missing parent signatures and no MISSING values in coupling/source rows",
            "2908 is a constructive candidate, not a claim",
            "BLOCKED_NONCLAIM",
            SRC_2907_NEXT,
        ),
    ]
    return [
        add_common(
            {
                "law_id": law_id,
                "quantity": quantity,
                "law": law,
                "conditions": conditions,
                "consequence": consequence,
                "claim_status": claim_status,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "parent_signed": False,
                "accepted_for_local_gr": False,
            }
        )
        for law_id, quantity, law, conditions, consequence, claim_status, source_path in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2908_0_sources", "SOURCE_CONTEXT_READY", "2907 handoff, 2464 vertical-generator action, 1619 normal form, 1620 source-current bridge", 4, "2908 is anchored to existing evidence"),
        ("RUN2908_1_skeleton", "SKELETON_WRITTEN_NOT_PROMOTED", "EH/public metric; universal matter; vertical-generator q_loc; response doublet; PiM/worldtube; projector; boundary guard", 2, "formal q_loc owner exists but source coupling is unsigned"),
        ("RUN2908_2_q_loc", "FORMAL_QLOC_EULER_PASS_CANDIDATE", "delta_A variation", 1, "nabla Gamma - div Khat - J_M equation follows algebraically in the candidate"),
        ("RUN2908_3_Y5Y6", "Y5Y6_COUPLING_OWNER_OPEN", "J_M;J_Z;Y5 GM transfer;Y6 extra stress;projector;boundary;observable lock", 0, "source and stress ownership remain missing"),
        ("RUN2908_4_claim_refusal", "LOCAL_GR_NEWTON_BLOCKED", "all current claim gates", 0, "candidate action is not current MTS parent theorem"),
        ("RUN2908_5_next", "SOURCE_CURRENT_DESCENT_SELECTED_NEXT", "J_M/J_Z source-current descent and Y5Y6 coupling-zero proof", 0, "this is the shortest route to make the skeleton more than algebra"),
    ]
    return [
        add_common(
            {
                "runner_id": runner_id,
                "status": status,
                "required_components": required_components,
                "components_evaluable": components_evaluable,
                "reason": reason,
                "runner_ready": False,
            }
        )
        for runner_id, status, required_components, components_evaluable, reason in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2908_0_formal_q_loc_variation", "candidate action formally produces q_loc Euler equation", "PASS_AS_CANDIDATE_ONLY", "delta_A variation from 2464 survives the 2908 skeleton", True),
        ("CG2908_1_parent_action_promoted", "current MTS has a single parent action owning all retained sectors", "BLOCKED_NONCLAIM", "skeleton is assembled from contracts and new candidate material", False),
        ("CG2908_2_source_current_descent", "J_M/J_Z source currents are parent-derived and vanish/bound correctly", "BLOCKED_NONCLAIM", "verticality, matter descent, no-marker, boundary and source bridge are unsigned", False),
        ("CG2908_3_Y5_zero", "Y5 source-normalization no longer sources the extra mode", "BLOCKED_NONCLAIM", "GM transfer and mu_extra channels remain open", False),
        ("CG2908_4_Y6_zero", "Y6 extra stress is locally silent or bounded", "BLOCKED_NONCLAIM", "metric stress/projector/boundary components are not parent-signed", False),
        ("CG2908_5_F1_zero_current", "F1=0 is proved for current MTS", "CONDITIONAL_ONLY", "follows only if source-current and boundary clauses close", False),
        ("CG2908_6_Delta_m_elltr", "Delta m bound and ell_tr/L_cg are derived numerically", "BLOCKED_NONCLAIM", "M_source, J bounds, boundary flux, m_tr and L_cg are not sourced", False),
        ("CG2908_7_local_GR_Newton", "local GR/Newton follows after 2908", "BLOCKED_NONCLAIM", "formal skeleton does not yet close source/stress/readout ownership", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": gate_status,
                "reason": reason,
                "gate_pass": gate_pass,
                "accepted_for_local_gr": False,
            }
        )
        for gate_id, claim, gate_status, reason, gate_pass in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2908_0_candidate_kept", "KEEP_VERTICAL_GENERATOR_CURRENT_LAW_AS_BEST_CANDIDATE", "it derives q_loc as an Euler/source equation rather than a plateau axiom", "use it as the live parent-action skeleton"),
        ("DEC2908_1_not_promoted", "DO_NOT_PROMOTE_SKELETON_TO_CURRENT_MTS_THEOREM", "source current, stress, projector, boundary and observable lock are still unsigned", "local GR/Newton claim remains blocked"),
        ("DEC2908_2_Y5Y6_key", "SOURCE_CURRENT_AND_Y5Y6_COUPLING_ARE_NOW_THE_KEY", "the q_loc algebra is less foggy; the surviving wound is whether J_M/J_Z/Y5/Y6 are parent-owned", "next proof attacks source-current descent and coupling zero"),
        ("DEC2908_3_no_denominator_retry", "NO_MHREF_RETRY_FROM_2908", "2907/2462 already block MHref until parent action material exists", "stay on constructive route"),
        ("DEC2908_4_next", "NEXT_2909_SOURCE_CURRENT_DESCENT_Y5Y6_COUPLING_ZERO", "this is the shortest route from formal skeleton to possible local GR reduction", "derive or residualize source-current/coupling rows"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "effect": effect,
            }
        )
        for decision_id, decision, reason, effect in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2908_0_2909",
                "selection_status": "selected_primary",
                "target_file": "2909-Y5-R2FR-source-current-descent-and-Y5Y6-coupling-zero-or-residual-vector-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_source_current_descent_and_Y5Y6_coupling_zero_or_residual_vector_under_AX1090_2909.py",
                "task": "try to prove the source-current descent clauses for J_M and J_Z and close or explicitly residualize the Y5/Y6 coupling channels in the 2908 parent-action skeleton",
                "success_condition": "J_M is the parent Hilbert/worldtube source current, J_Z vanishes by quotient descent/no-marker/boundary silence, and Y5/Y6 coupling rows become theorem-zero or source-bounded in one branch",
                "fallback_condition": "write explicit residual vector rows for J_M, J_Z, Y5 GM transfer, Y5 mu_extra, Y6 stress, projector stress, boundary flux and observable projections",
                "guardrails": "no orbital-GM source definition; no plateau axiom; no MHref retry; no closure-only current zero; no local-GR claim; no GitHub; no formalization-workbench edits",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    specs = [
        ("BR2908_0_skeleton_copy", OUTPUTS["skeleton"], BRANCH_OUTPUTS["skeleton_copy"], "RAB queue copy of parent-action skeleton"),
        ("BR2908_1_coupling_copy", OUTPUTS["coupling"], BRANCH_OUTPUTS["coupling_copy"], "local-bounds copy of Y5/Y6 coupling owner audit"),
        ("BR2908_2_next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"], "parent-action copy of 2909 source-current descent target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in specs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def formalization_touched() -> bool:
    if not FORMALIZATION.exists():
        return False
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for candidate in FORMALIZATION.rglob("*"):
        try:
            if candidate.is_file() and candidate.stat().st_mtime >= start_timestamp:
                return True
        except OSError:
            return True
    return False


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows_data = all_rows["sources"]
    skeleton_rows_data = all_rows["skeleton"]
    variation_rows_data = all_rows["variation"]
    coupling_rows_data = all_rows["coupling"]
    law_rows_data = all_rows["laws"]
    runner_rows_data = all_rows["runner"]
    claim_rows_data = all_rows["claims"]
    decision_rows_data = all_rows["decision"]
    next_rows_data = all_rows["next"]
    branch_rows_data = all_rows["branches"]
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    required_couplings = {
        "epsilon_Y5_GM_transfer",
        "epsilon_Y5_mu_extra_vector",
        "J_M^nu",
        "J_Z",
        "epsilon_extra_odd_source_Y6",
        "epsilon_Y6_projector_stress",
        "epsilon_boundary_worldtube_flux",
        "epsilon_Y5Y6_observable_projection",
        "epsilon_parent_action_Y5Y6_coupling_total",
    }
    found_couplings = {row["symbol"] for row in coupling_rows_data}
    checks = [
        ("VAL2908_0_sources_exist", all(row["path_exists"] for row in source_rows_data), "all registered source paths exist"),
        ("VAL2908_1_source_anchors", all(row["anchors_found"] for row in source_rows_data), "all registered source anchors were found"),
        ("VAL2908_2_skeleton_complete", len(skeleton_rows_data) == 8 and any(row["action_id"] == "ACT2908_7_total_verdict" for row in skeleton_rows_data), "parent-action skeleton has all action blocks"),
        ("VAL2908_3_skeleton_nonclaim", all(not row["parent_signed"] and not row["promote_now"] for row in skeleton_rows_data), "skeleton rows remain nonclaim"),
        ("VAL2908_4_variation_q_loc_formal_pass", any(row["variation_id"] == "VAR2908_0_delta_A_q_loc" and row["formal_pass"] for row in variation_rows_data), "q_loc Euler equation formal candidate pass is recorded"),
        ("VAL2908_5_variation_not_promoted", all(not row["parent_signed"] and not row["accepted_for_local_gr"] for row in variation_rows_data), "variation rows do not promote local GR"),
        ("VAL2908_6_coupling_symbols_present", required_couplings <= found_couplings, "Y5/Y6 coupling symbols are present"),
        ("VAL2908_7_coupling_rows_nonclaim", all(not row["valid_for_claim"] and not row["accepted_for_scoring"] for row in coupling_rows_data), "coupling rows remain non-score-ready and nonclaim"),
        ("VAL2908_8_local_laws_complete", {"F_1", "Delta m / m", "ell_tr / L_cg"} <= {row["quantity"] for row in law_rows_data}, "F1, Delta m and transition laws are recorded"),
        ("VAL2908_9_runner_refuses_claim", any(row["runner_id"] == "RUN2908_4_claim_refusal" and row["status"] == "LOCAL_GR_NEWTON_BLOCKED" for row in runner_rows_data), "runner refuses local-GR/Newton promotion"),
        ("VAL2908_10_claim_gates_safe", all(not row["claim_allowed"] for row in claim_rows_data) and any(row["gate_id"] == "CG2908_7_local_GR_Newton" and row["gate_status"] == "BLOCKED_NONCLAIM" for row in claim_rows_data), "claim gates keep local GR/Newton blocked"),
        ("VAL2908_11_decision_source_current_next", any(row["decision_id"] == "DEC2908_4_next" for row in decision_rows_data), "source-current/Y5Y6 next decision is recorded"),
        ("VAL2908_12_next_target_2909", any(row["route_id"] == "NEXT2908_0_2909" and row["selected"] for row in next_rows_data), "2909 source-current descent target selected"),
        ("VAL2908_13_branch_copies_exist", all(row["exists"] for row in branch_rows_data), "branch copies were written"),
        ("VAL2908_14_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs), "all generated CSV outputs parse cleanly"),
        ("VAL2908_15_formalization_untouched_during_run", not formalization_touched(), "formalization-workbench was not touched during this run"),
    ]
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL2908_OVERALL", overall, "2908 validation overall"))
    return [
        {
            "check_id": check_id,
            "passed": passed,
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, passed, detail in checks
    ]


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "/")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def write_doc(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2908 - Y5 R2FR Minimal Parent-Action Skeleton for q_loc/Source Bridge/Y5Y6 Coupling Under AX1090",
        "",
        f"Run: `runs/{SCRIPT_START_UTC.strftime('%Y%m%d-%H%M%S')}-Y5-R2FR-minimal-parent-action-skeleton-for-q_loc-source-bridge-and-Y5Y6-coupling-under-AX1090`",
        "Status: `Y5_R2FR_2908_parent_action_skeleton_written_q_loc_formal_candidate_Y5Y6_source_coupling_open_2909_next`",
        "Claim ceiling: `formal_parent_action_skeleton_nonclaim_only_no_source_current_zero_no_Y5Y6_zero_no_PPN_no_R10_no_Newton_no_local_GR_no_GitHub_claim`",
        "",
        "## Summary",
        "",
        "2908 takes the constructive leap rather than circling `M_H_ref`: it assembles a minimal parent-action skeleton around the old vertical-generator current-law candidate.",
        "",
        "The win is real but conditional. Varying the candidate vertical generator `A_nu` can formally produce the exact unprojected local equation `nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu} - J_M^nu = 0`, so `q_loc` is no longer just a plateau wish. It can be an Euler/source equation.",
        "",
        "The block is also real: the current MTS corpus has not yet parent-signed `J_M`, `J_Z`, the Y5 source-normalization channels, Y6 extra stress, projector stress, boundary flux, or observable projection maps. So 2908 is a serious skeleton, not a local-GR/Newton claim.",
        "",
        "## Source Register",
        "",
        md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"]),
        "",
        "## Parent-Action Skeleton",
        "",
        md_table(all_rows["skeleton"], ["action_id", "action_block", "current_status", "purpose", "blocking_gap", "valid_for_claim"]),
        "",
        "## Variation and q_loc Derivation",
        "",
        md_table(all_rows["variation"], ["variation_id", "varied_object", "current_status", "formal_variation", "would_prove", "remaining_issue", "valid_for_claim"]),
        "",
        "## Y5/Y6 Coupling Owner Audit",
        "",
        md_table(all_rows["coupling"], ["coupling_id", "symbol", "definition", "units", "current_value", "observable_link", "required_before_claim", "valid_for_claim"]),
        "",
        "## Local Vacuum and Amplitude Laws",
        "",
        md_table(all_rows["laws"], ["law_id", "quantity", "law", "conditions", "consequence", "claim_status", "valid_for_claim"]),
        "",
        "## Runner Status",
        "",
        md_table(all_rows["runner"], ["runner_id", "status", "required_components", "components_evaluable", "reason", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(all_rows["claims"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(all_rows["decision"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(all_rows["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(all_rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(all_rows["validation"], ["check_id", "passed", "detail", "generated_utc"]),
        "",
        "## Working Read",
        "",
        "This is the closest the local branch has got to a genuine derivational object: a candidate action whose Euler equation can own the `q_loc` profile. The theory still has to pay the source bill. If the next step can prove `J_M` is the parent Hilbert/worldtube source current and `J_Z` vanishes by descent, then the Y5/Y6 wound starts healing. If not, the residual vector is now explicit enough to score or falsify.",
        "",
        "## Forbidden Claims From 2908",
        "",
        "- The 2908 skeleton is the current MTS parent action.",
        "- `J_M` or `J_Z` is parent-derived or zero for current MTS.",
        "- Y5 source normalization or Y6 extra stress is locally silent.",
        "- `F_1=0`, `Delta m`, or `ell_tr/L_cg` is derived for current MTS rather than conditional.",
        "- Source-normalized Newton, PPN, R10, clock, orbital or local GR is proved.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {}
    all_rows["sources"] = source_register_rows()
    all_rows["skeleton"] = skeleton_rows()
    all_rows["variation"] = variation_rows()
    all_rows["coupling"] = coupling_rows()
    all_rows["laws"] = law_rows()
    all_rows["runner"] = runner_rows()
    all_rows["claims"] = claim_gate_rows()
    all_rows["decision"] = decision_rows()
    all_rows["next"] = next_rows()

    for key in ["sources", "skeleton", "variation", "coupling", "laws", "runner", "claims", "decision", "next"]:
        write_csv(OUTPUTS[key], all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_doc(all_rows)

    overall = next(row["passed"] for row in all_rows["validation"] if row["check_id"] == "VAL2908_OVERALL")
    print(f"2908 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()
