from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1790"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1790_0_1789_handoff_doc",
        "source_key": "1789_handoff",
        "source_path": ROOT / "1789-Y5-R2FR-no-integrated-out-curvature-tower-or-finite-scalar-bound-pack.md",
        "needles": ["EID1789_1_effective_tail", "CEC1789_0_effective_law", "NEXT1789_0_primary"],
        "role": "selected 1790 as Gamma/Khat/Ploc owner-bundle or cR2 input-pack smoke target",
    },
    {
        "source_id": "SRC1790_1_1789_validation",
        "source_key": "1789_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1789_VALIDATION.csv",
        "needles": ["VAL1789_OVERALL", "PASS"],
        "role": "confirms 1789 checkpoint passed before 1790 continues it",
    },
    {
        "source_id": "SRC1790_2_1789_effective_pack",
        "source_key": "1789_effective_cr2_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1789_EFFECTIVE_CR2_COEFFICIENT_PACK.csv",
        "needles": ["CEC1789_0_effective_law", "CEC1789_4_verdict"],
        "role": "effective c_R2 law exists but executable coefficients are missing",
    },
    {
        "source_id": "SRC1790_3_1789_finite_scalar_pack",
        "source_key": "1789_finite_scalar_input_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1789_FINITE_SCALAR_INPUT_PACK.csv",
        "needles": ["FSI1789_1_coefficient", "FSI1789_6_acceptance"],
        "role": "finite scalar input pack is rejected until coefficient, units, and maps exist",
    },
    {
        "source_id": "SRC1790_4_1710_scalaron_contract",
        "source_key": "1710_scalaron_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1710_SCALARON_MAP_CONTRACT.csv",
        "needles": ["SMC1710_0_flat_R_plus_aR2", "SMC1710_4_prediction_row"],
        "role": "known scalaron map is formula-only without parent c_R2/fRR coefficient",
    },
    {
        "source_id": "SRC1790_5_1710_input_pack",
        "source_key": "1710_cr2_input_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1710_CR2_INPUT_PACK_CONTRACT.csv",
        "needles": ["IP1710_1_coefficient", "IP1710_8_acceptance"],
        "role": "strict fields required for c_R2/fRR prediction row",
    },
    {
        "source_id": "SRC1790_6_1710_coefficient_hunt",
        "source_key": "1710_coefficient_hunt",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1710_COEFFICIENT_SOURCE_HUNT_REFRESH.csv",
        "needles": ["CH1710_0_parent_zero", "CH1710_6_verdict"],
        "role": "coefficient source hunt did not find a claim-grade parent coefficient",
    },
    {
        "source_id": "SRC1790_7_1710_runner_refusal",
        "source_key": "1710_runner_refusal",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1710_RUNNER_REFUSAL.csv",
        "needles": ["RUN1710_1_input_pack", "RUN1710_5_future_accept"],
        "role": "runner refuses formula-only and missing-pack rows",
    },
    {
        "source_id": "SRC1790_8_1711_owner_retest",
        "source_key": "1711_owner_retest",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1711_GAMMA_KHAT_PLOC_OWNER_RETEST.csv",
        "needles": ["OBR1711_1_Gamma_eff", "OBR1711_2_Khat_response", "OBR1711_7_verdict"],
        "role": "Gamma/Khat/Ploc owner bundle remains not closed",
    },
    {
        "source_id": "SRC1790_9_1711_smoke_dryrun",
        "source_key": "1711_cr2_input_smoke",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1711_CR2_INPUT_PACK_SMOKE_DRYRUN.csv",
        "needles": ["DRY1711_0_current_cR2_pack", "DRY1711_5_future_complete_template"],
        "role": "strict schema smoke runner pattern for c_R2/fRR input packs",
    },
    {
        "source_id": "SRC1790_10_1711_response_doublet",
        "source_key": "1711_response_doublet",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1711_RESPONSE_DOUBLET_STATUS.csv",
        "needles": ["RD1711_2_metric_response", "RD1711_5_verdict"],
        "role": "response doublet is promising but not current derivation",
    },
    {
        "source_id": "SRC1790_11_1711_claim_gate",
        "source_key": "1711_claim_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1711_CLAIM_GATE.csv",
        "needles": ["CG1711_0_owner", "CG1711_5_local_GR"],
        "role": "local GR and owner claims blocked in prior gate",
    },
    {
        "source_id": "SRC1790_12_1712_conjugacy_attempt",
        "source_key": "1712_conjugacy_attempt",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1712_RESPONSE_DISPLACEMENT_CONJUGACY_ATTEMPT.csv",
        "needles": ["CJA1712_2_metric_response", "CJA1712_6_verdict"],
        "role": "response/displacement route is alive but not parent-signed",
    },
    {
        "source_id": "SRC1790_13_1712_q_loc_profile",
        "source_key": "1712_q_loc_profile",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1712_FIRST_QLOC_PROFILE_ROW.csv",
        "needles": ["QPROF1712_0_parent_residual_vector", "QPROF1712_4_theorem_zero_certificate"],
        "role": "fallback q_loc profile rows are template-only and not scoreable",
    },
    {
        "source_id": "SRC1790_14_1712_claim_gate",
        "source_key": "1712_claim_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1712_CLAIM_GATE.csv",
        "needles": ["CG1712_3_cR2_zero_or_value", "CG1712_5_local_GR"],
        "role": "c_R2, R10/PPN, and local GR remain blocked",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1790_SOURCE_REGISTER.csv",
    "owner_bundle_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1790_OWNER_BUNDLE_GATE.csv",
    "response_to_cr2_link": RESIDUALS / "P8_Y5_PARENT_QLOC_1790_RESPONSE_TO_CR2_LINK.csv",
    "cr2_input_pack_strict_smoke": RESIDUALS / "P8_Y5_PARENT_QLOC_1790_CR2_INPUT_PACK_STRICT_SMOKE.csv",
    "q_loc_profile_fallback": RESIDUALS / "P8_Y5_PARENT_QLOC_1790_QLOC_PROFILE_FALLBACK.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1790_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1790_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1790_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1790_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1790_VALIDATION.csv",
}

DOC_PATH = ROOT / "1790-Y5-R2FR-Gamma-Khat-Ploc-owner-bundle-or-cR2-input-pack-smoke-runner.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and all(needle in text for needle in needles),
                "role": source["role"],
            }
        )
    return rows


def owner_bundle_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OBG1790_0_Gamma_eff",
            "bundle_piece": "Gamma_eff",
            "required_evidence": "single parent scalar-density formula with fields, units, derivative order, sign convention, branch labels, and source path",
            "current_status": "CONTRACT_ONLY_NOT_LIVE_FORMULA",
            "blocking_reason": "1711 records only a contract; no live formula can be varied, unit-checked, or tied to all local arenas",
            "parent_signed": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OBG1790_1_Khat_response",
            "bundle_piece": "K_hat^{mu nu}",
            "required_evidence": "K_hat^{mu nu} = 2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu}, including volume, derivative and boundary terms",
            "current_status": "NOT_MATCHED",
            "blocking_reason": "without term-by-term metric variation, the divergence cancellation can be inserted by hand",
            "parent_signed": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OBG1790_2_Ploc_owner",
            "bundle_piece": "P_loc",
            "required_evidence": "covariant parent projector fixed before readout and commuting with the compact local limit",
            "current_status": "OPEN_PROJECTOR_OWNER",
            "blocking_reason": "a projection chosen after seeing the residual can hide force components or tune the answer",
            "parent_signed": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OBG1790_3_Euler_source",
            "bundle_piece": "Euler/Ward/source closure",
            "required_evidence": "all Gamma/Khat fields are varied, on shell, and free of external, bath, spurion, source-normalization, and readout currents",
            "current_status": "NOT_DERIVED",
            "blocking_reason": "J_Z, B_Z, Y5 source-normalization, Y6 extra-stress, and boundary/readout terms remain source channels",
            "parent_signed": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OBG1790_4_boundary",
            "bundle_piece": "boundary/symplectic no-flux",
            "required_evidence": "boundary response vanishes or is a fixed topological subtraction on compact local domains",
            "current_status": "OPEN_BOUNDARY_FLUX",
            "blocking_reason": "bulk cancellation can leak through boundary charge, mass flux, or readout-corner terms",
            "parent_signed": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OBG1790_5_observable_lock",
            "bundle_piece": "R10/PPN/clock/orbital maps",
            "required_evidence": "same q_loc profile maps into alpha(lambda), PPN vector, clock shifts, orbital residuals, and source normalization with units",
            "current_status": "MISSING_ARENA_LOCK",
            "blocking_reason": "finite residual cannot be scored without response coefficients and arena projection maps",
            "parent_signed": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OBG1790_6_verdict",
            "bundle_piece": "minimal Gamma_eff/K_hat/P_loc owner bundle",
            "required_evidence": "OBG1790_0 through OBG1790_5 all close with source paths",
            "current_status": "OWNER_BUNDLE_NOT_CLOSED",
            "blocking_reason": "Gamma_eff is contract-only, K_hat is not matched, P_loc is open, and arena locks are missing",
            "parent_signed": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def response_to_cr2_link_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "link_id": "RCL1790_0_effective_law",
            "object": "c_R2_eff",
            "mathematical_form": "c_R2_eff = c_bare + 1/2 B_R^T L_X^{-1} B_R + c_measure + c_boundary + c_field_redef_remnant",
            "required_owner": "Gamma_eff/K_hat/P_loc must own or kill B_R, J_X, measure, and boundary terms before scoring",
            "current_status": "FORMULA_LINK_WRITTEN_INPUTS_MISSING",
            "payoff_if_closed": "would either prove c_R2/fRR zero or supply a real finite scalar coefficient row",
            "parent_signed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "link_id": "RCL1790_1_BR_owner",
            "object": "B_R",
            "mathematical_form": "J_X includes B_R R plus matter, boundary, coframe, or readout sources",
            "required_owner": "prove B_R=0 by parent symmetry/descent or provide B_R with units and source path",
            "current_status": "MISSING_VERTEX_OWNER",
            "payoff_if_closed": "would decide whether integrated-out sectors regenerate R L_X^{-1} R",
            "parent_signed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "link_id": "RCL1790_2_JX_owner",
            "object": "J_X",
            "mathematical_form": "S_X = 1/2<X,L_X X> - <J_X,X> gives S_eff = S_rest - 1/2<J_X,L_X^{-1}J_X>",
            "required_owner": "derive J_X=0 in compact local exterior or source every nonzero component",
            "current_status": "MISSING_SOURCE_OWNER",
            "payoff_if_closed": "would decide whether the safe no-tail branch is legal",
            "parent_signed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "link_id": "RCL1790_3_Khat_metric_response",
            "object": "K_hat metric response",
            "mathematical_form": "K_hat^{mu nu} = 2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu}",
            "required_owner": "term-by-term comparison of live K_hat to metric variation of the same Gamma_eff density",
            "current_status": "NOT_MATCHED",
            "payoff_if_closed": "would make q_loc a Ward residual rather than a closure axiom",
            "parent_signed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "link_id": "RCL1790_4_q_loc_bridge",
            "object": "q_loc^nu",
            "mathematical_form": "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "required_owner": "Gamma_eff formula, K_hat metric match, P_loc owner, source/boundary silence or finite profile, and arena maps",
            "current_status": "QLOC_PROFILE_TEMPLATE_ONLY",
            "payoff_if_closed": "would feed R10, PPN, clocks, and orbital tests from one local residual vector",
            "parent_signed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "link_id": "RCL1790_5_verdict",
            "object": "Gamma/Khat/Ploc to c_R2/q_loc bridge",
            "mathematical_form": "OBG1790 closes and RCL1790 inputs are zero theorem or source-backed numeric rows",
            "required_owner": "parent-signed response bundle plus sourced coefficient/profile pack",
            "current_status": "CANNOT_ZERO_OR_SCORE_CR2_QLOC",
            "payoff_if_closed": "activates genuine local-GR/R10/PPN tests instead of symbolic smoke rows",
            "parent_signed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def cr2_input_pack_strict_smoke_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "dry_run_id": "DRY1790_0_current_cR2_pack",
            "candidate": "current 1710/1789 c_R2 input pack",
            "missing_or_forbidden": "c_R2/fRR coefficient, units, sign, normalization, screening, source path, and arena maps missing",
            "runner_verdict": "REJECT",
            "reason": "valid_for_claim_false",
            "score_emitted": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "dry_run_id": "DRY1790_1_formula_only",
            "candidate": "scalaron formula without parent coefficient",
            "missing_or_forbidden": "m_s^2=1/(6 c_R2) is known but c_R2 is missing",
            "runner_verdict": "REJECT_FORMULA_ONLY",
            "reason": "formula is a map, not an MTS prediction",
            "score_emitted": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "dry_run_id": "DRY1790_2_Gamma_without_Khat",
            "candidate": "Gamma_eff candidate without matched K_hat metric response",
            "missing_or_forbidden": "scalar-density idea does not match K_hat tensor response",
            "runner_verdict": "REJECT_PARTIAL_OWNER",
            "reason": "q_loc/c_R2 owner not derived",
            "score_emitted": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "dry_run_id": "DRY1790_3_private_Bmem_zero",
            "candidate": "use B_mem=0 or double-zero closure to zero c_R2_eff",
            "missing_or_forbidden": "private closure branch lacks K_MTS/Gamma/Khat/P_loc owner",
            "runner_verdict": "FORBIDDEN_PRIVATE_CLOSURE",
            "reason": "not public theorem evidence and cannot score as prediction",
            "score_emitted": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "dry_run_id": "DRY1790_4_anchor_backsolve",
            "candidate": "derive c_R2 from R10 alpha=1 or threshold anchors",
            "missing_or_forbidden": "bound rows cannot generate parent coefficient",
            "runner_verdict": "FORBIDDEN_BACKSOLVE",
            "reason": "prediction-from-bound cheating",
            "score_emitted": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "dry_run_id": "DRY1790_5_future_complete_template",
            "candidate": "future complete c_R2/fRR input pack",
            "missing_or_forbidden": "none if all values, theorem-zero/source paths, units, response maps and bounds are supplied by real files",
            "runner_verdict": "WOULD_ACCEPT_IF_REAL_FILES_AND_VALUES_EXIST",
            "reason": "template remains nonclaim until files and comparison pass",
            "score_emitted": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def q_loc_profile_fallback_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "profile_id": "QLP1790_0_formula",
            "profile_object": "q_loc^nu parent residual vector",
            "expression": "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "required_inputs": "Gamma_eff;K_hat metric match;P_loc owner;domain;coframe;normalization",
            "current_missing": "MISSING_LIVE_GAMMA;MISSING_KHAT_MATCH;MISSING_PLOC_OWNER",
            "row_status": "FORMULA_ONLY",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "profile_id": "QLP1790_1_profile_values",
            "profile_object": "finite local profile",
            "expression": "q_loc^nu(r,material,domain) with uncertainty and units",
            "required_inputs": "radial/profile values; units; source path; extraction method; normalization",
            "current_missing": "MISSING_NUMERIC_PROFILE;MISSING_UNITS;MISSING_SOURCE_PATH",
            "row_status": "TEMPLATE_ONLY_NOT_SCOREABLE",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "profile_id": "QLP1790_2_arena_maps",
            "profile_object": "R10/PPN/clock/orbital projections",
            "expression": "q_loc -> alpha(lambda), PPN vector, clock shift, orbital residual, GM drift",
            "required_inputs": "projection theorem and bound source for every arena",
            "current_missing": "MISSING_ARENA_PROJECTION_MAPS",
            "row_status": "TEMPLATE_ONLY_NOT_SCOREABLE",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "profile_id": "QLP1790_3_bound_policy",
            "profile_object": "claim policy",
            "expression": "only score if theorem-zero certificate or source-backed numeric profile exists",
            "required_inputs": "no MISSING_* fields, real source paths, units, and comparison bounds",
            "current_missing": "MISSING_CLAIM_GRADE_PROFILE_OR_ZERO_THEOREM",
            "row_status": "NO_CLAIM_POLICY",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "profile_id": "QLP1790_4_verdict",
            "profile_object": "q_loc fallback profile row",
            "expression": "first q_loc profile remains a placeholder until owner bundle closes or finite values are sourced",
            "required_inputs": "Gamma/Khat/Ploc owner or complete nonzero profile pack",
            "current_missing": "MISSING_OWNER_BUNDLE_AND_NUMERIC_PROFILE",
            "row_status": "FALLBACK_ROW_TEMPLATE_NOT_SCORE_READY",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1790_0_scalar_density_unmatched_response",
            "countermodel": "Gamma_eff scalar density exists but the live K_hat tensor is not its metric variation",
            "survives_current_constraints": True,
            "why_survives": "K_hat response is not term-by-term matched",
            "what_kills_it": "source-backed metric variation matching the same Gamma_eff density",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1790_1_projector_tuning",
            "countermodel": "P_loc is selected after readout to remove inconvenient force components",
            "survives_current_constraints": True,
            "why_survives": "P_loc owner remains open",
            "what_kills_it": "parent covariant projector fixed before readout and shown to commute with local limit",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1790_2_formula_only_scalaron",
            "countermodel": "m_s^2=1/(6 c_R2) is treated as an MTS prediction despite missing c_R2",
            "survives_current_constraints": True,
            "why_survives": "known map is not a coefficient source",
            "what_kills_it": "parent-sourced c_R2/fRR value or theorem-zero",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1790_3_private_closure",
            "countermodel": "B_mem or double-zero closure is smuggled into a public theorem without parent owner",
            "survives_current_constraints": True,
            "why_survives": "doublet/component/source locks are still conditional",
            "what_kills_it": "response-displacement conjugacy action with component lock, no-linear-source theorem, and Khat match",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1790_4_anchor_backsolve",
            "countermodel": "R10 bounds or anchors are used to infer MTS c_R2 instead of testing a prediction",
            "survives_current_constraints": True,
            "why_survives": "strict smoke policy forbids bound-to-coefficient backsolves",
            "what_kills_it": "MTS coefficient produced independently before comparison to bound curve",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1790_5_q_loc_profile_no_units",
            "countermodel": "q_loc profile is written symbolically without units, maps, source paths, or arena bounds",
            "survives_current_constraints": True,
            "why_survives": "1712 and 1790 fallback rows are template-only",
            "what_kills_it": "source-backed q_loc profile with units and R10/PPN/clock/orbital projection maps",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1790_0_owner_bundle",
            "claim": "Gamma_eff/K_hat/P_loc owner bundle is derived",
            "status": "BLOCKED",
            "reason": "Gamma_eff is contract-only, K_hat is unmatched, P_loc is open, and source/boundary locks are missing",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1790_1_q_loc_zero_or_profile",
            "claim": "q_loc^nu is zero or has a finite source-backed profile",
            "status": "BLOCKED",
            "reason": "no parent-signed zero theorem and no numeric profile with units/maps",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1790_2_cR2_zero",
            "claim": "c_R2/fRR theorem-zero",
            "status": "BLOCKED",
            "reason": "B_R/J_X/measure/boundary owners are missing",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1790_3_finite_scalar_score",
            "claim": "finite scalaron/R10/PPN score can run",
            "status": "BLOCKED",
            "reason": "strict c_R2/fRR input smoke rejects incomplete, formula-only, private closure, and anchor-backsolve rows",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1790_4_local_GR_Newton",
            "claim": "derived local GR/Newton reduction",
            "status": "BLOCKED",
            "reason": "R2/fR, q_loc, PPN, GM/source-normalization, and boundary gates are not jointly closed",
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1790_0_owner_route",
            "decision": "OWNER_ROUTE_REMAINS_BEST_NONCLAIM_PATH",
            "reason": "Gamma/Khat/Ploc is the narrowest route that could turn q_loc into a Ward residual and decide J_X/B_R/c_R2_eff",
            "next_action": "refresh response-displacement conjugacy with explicit 1789/1790 coefficient-law constraints",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1790_1_smoke_runner",
            "decision": "STRICT_SMOKE_REJECTS_CURRENT_CR2_PACK",
            "reason": "the current pack has no coefficient, units, sign, normalization, screening, source path, or projection maps",
            "next_action": "do not run R10/PPN scores until real parent coefficient/profile rows exist",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1790_2_no_claim",
            "decision": "NO_GAMMA_KHAT_PLOC_CLAIM",
            "reason": "contract-only Gamma, unmatched Khat, and open P_loc would be smuggling a plateau axiom",
            "next_action": "write the exact parent action or produce a first nonclaim q_loc/c_R2 input pack row",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1790_3_next",
            "decision": "RESPONSE_DISPLACEMENT_CONJUGACY_REFRESH_OR_QLOC_PROFILE_ROW_NEXT",
            "reason": "1712 is the live derivation route, but it must now be tied to the 1789/1790 c_R2 effective-law and strict input-pack gates",
            "next_action": "build 1791 response-displacement conjugacy owner refresh or first q_loc profile pack",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1790_0_primary",
            "next_target": "1791-Y5-R2FR-response-displacement-conjugacy-owner-refresh-or-q_loc-profile-pack.md",
            "script": "scripts/Y5_R2FR_response_displacement_conjugacy_owner_refresh_or_q_loc_profile_pack.py",
            "objective": "refresh 1712 using the 1789/1790 c_R2 effective-law gates; either construct a source-checkable response/displacement parent action or emit the first strict nonclaim q_loc/c_R2 profile pack with units, source paths, and arena maps",
            "selection_status": "selected",
            "success_condition": "parent-signed conjugacy owner bundle, or complete nonclaim finite profile/input-pack rows that cannot be mistaken for claims",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1790_1_parallel_cR2",
            "next_target": "1791b-Y5-R2FR-cR2-input-pack-acquisition-ledger.md",
            "script": "scripts/Y5_R2FR_cR2_input_pack_acquisition_ledger.py",
            "objective": "collect possible source-ready c_R2/fRR coefficient inputs, keeping every row nonclaim until source, units, and projection maps exist",
            "selection_status": "held_parallel",
            "success_condition": "real coefficient/source rows only, no anchor backsolve",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1790_2_parallel_connection",
            "next_target": "1791c-Y5-R2FR-connection-and-boundary-owner-gate.md",
            "script": "scripts/Y5_R2FR_connection_and_boundary_owner_gate.py",
            "objective": "separate Levi-Civita/torsion/nonmetricity and boundary-flux owner gaps from the c_R2 input-pack gate",
            "selection_status": "held_parallel",
            "success_condition": "explicit connection and boundary assumptions for any local-GR reduction branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "owner_bundle_gate": owner_bundle_gate_rows(),
        "response_to_cr2_link": response_to_cr2_link_rows(),
        "cr2_input_pack_strict_smoke": cr2_input_pack_strict_smoke_rows(),
        "q_loc_profile_fallback": q_loc_profile_fallback_rows(),
        "countermodel_ledger": countermodel_ledger_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def fieldnames_for(rows: list[dict[str, Any]]) -> list[str]:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    return fieldnames


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames_for(rows))
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
        shutil.copy2(path, RAB_QUEUE / f"JR1790_{key.upper()}.csv")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "pass", "passed"}


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return (
        all(boolish(row["exists"]) for row in rows),
        all(boolish(row["needles_present"]) for row in rows),
    )


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for flag in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "score_emitted",
                "accepted_for_scoring",
                "theorem_closed_for_claim",
                "parent_signed",
                "valid_prediction_row",
                "gate_pass",
            ):
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                for flag in (
                    "valid_for_claim",
                    "claim_allowed",
                    "score_ready",
                    "score_emitted",
                    "accepted_for_scoring",
                    "theorem_closed_for_claim",
                    "valid_prediction_row",
                    "gate_pass",
                ):
                    if boolish(row.get(flag, False)):
                        return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not (MICROSCOPE_RESIDUALS / path.name).exists():
            return False
        if not (QUARANTINE / path.name).exists():
            return False
        if not (RAB_QUEUE / f"JR1790_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    generated_names = {path.name for path in OUTPUTS.values()}
    generated_names.add(DOC_PATH.name)
    return not any(path.name in generated_names for path in FORMALIZATION.rglob("*"))


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1790_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1790_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1790_2_owner_bundle_blocks",
            any(
                row["owner_id"] == "OBG1790_6_verdict"
                and row["current_status"] == "OWNER_BUNDLE_NOT_CLOSED"
                for row in rows_map["owner_bundle_gate"]
            )
            and all(
                not boolish(row["parent_signed"])
                and not boolish(row["score_ready"])
                and not boolish(row["valid_prediction_row"])
                and not boolish(row["valid_for_claim"])
                for row in rows_map["owner_bundle_gate"]
            ),
            "Gamma/Khat/Ploc owner bundle remains blocked and nonclaim",
        ),
        (
            "VAL1790_3_response_link_written",
            any(
                row["link_id"] == "RCL1790_0_effective_law"
                and "B_R^T L_X^{-1} B_R" in row["mathematical_form"]
                for row in rows_map["response_to_cr2_link"]
            ),
            "effective c_R2 response law is written",
        ),
        (
            "VAL1790_4_response_verdict_blocks",
            any(
                row["link_id"] == "RCL1790_5_verdict"
                and row["current_status"] == "CANNOT_ZERO_OR_SCORE_CR2_QLOC"
                for row in rows_map["response_to_cr2_link"]
            )
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["response_to_cr2_link"]),
            "response-to-c_R2 bridge cannot claim or score",
        ),
        (
            "VAL1790_5_smoke_rejects_current_pack",
            any(
                row["dry_run_id"] == "DRY1790_0_current_cR2_pack"
                and row["runner_verdict"] == "REJECT"
                for row in rows_map["cr2_input_pack_strict_smoke"]
            )
            and any(
                row["dry_run_id"] == "DRY1790_5_future_complete_template"
                and row["runner_verdict"] == "WOULD_ACCEPT_IF_REAL_FILES_AND_VALUES_EXIST"
                for row in rows_map["cr2_input_pack_strict_smoke"]
            )
            and all(not boolish(row["score_emitted"]) and not boolish(row["valid_for_claim"]) for row in rows_map["cr2_input_pack_strict_smoke"]),
            "strict smoke runner rejects current pack and keeps future template nonclaim",
        ),
        (
            "VAL1790_6_forbids_private_and_backsolve",
            any(row["dry_run_id"] == "DRY1790_3_private_Bmem_zero" and row["runner_verdict"] == "FORBIDDEN_PRIVATE_CLOSURE" for row in rows_map["cr2_input_pack_strict_smoke"])
            and any(row["dry_run_id"] == "DRY1790_4_anchor_backsolve" and row["runner_verdict"] == "FORBIDDEN_BACKSOLVE" for row in rows_map["cr2_input_pack_strict_smoke"]),
            "private closure and anchor backsolve are explicitly forbidden",
        ),
        (
            "VAL1790_7_q_loc_fallback_nonclaim",
            any(
                row["profile_id"] == "QLP1790_4_verdict"
                and row["row_status"] == "FALLBACK_ROW_TEMPLATE_NOT_SCORE_READY"
                for row in rows_map["q_loc_profile_fallback"]
            )
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_prediction_row"]) for row in rows_map["q_loc_profile_fallback"]),
            "q_loc profile fallback is template-only and not score-ready",
        ),
        (
            "VAL1790_8_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain live until owner bundle closes",
        ),
        (
            "VAL1790_9_claim_gates_blocked",
            all(
                row["status"] == "BLOCKED"
                and not boolish(row["gate_pass"])
                and not boolish(row["valid_for_claim"])
                for row in rows_map["claim_gate"]
            ),
            "all 1790 claim gates are blocked",
        ),
        ("VAL1790_10_no_claim_flags", no_claim_flags(rows_map), "no generated claim/score flags are true"),
        ("VAL1790_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1790_12_decision_next",
            any(
                row["decision_id"] == "DEC1790_3_next"
                and row["decision"] == "RESPONSE_DISPLACEMENT_CONJUGACY_REFRESH_OR_QLOC_PROFILE_ROW_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects 1791 response-displacement refresh or q_loc profile pack",
        ),
        (
            "VAL1790_13_next_selected",
            any(row["route_id"] == "NEXT1790_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1790_14_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1790 CSVs parse"),
        ("VAL1790_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1790_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1790_17_formalization_untouched", formalization_untouched(), "no 1790 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1790_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1790 Gamma/Khat/Ploc owner bundle or c_R2 input-pack smoke checkpoint",
        }
    )
    return rows


def clean_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "/")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(clean_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1790 - Y5/R2FR Gamma-Khat-Ploc Owner Bundle or cR2 Input-Pack Smoke Runner",
            "",
            "## Verdict",
            "",
            "1790 keeps the derivation-first route alive but does not promote it. The exact local residual object remains",
            "",
            "`q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})`.",
            "",
            "That expression becomes a theorem only if one parent bundle owns all three pieces: a live `Gamma_eff` scalar-density formula, a `K_hat^{mu nu}` that is the metric response of the same density, and a covariant `P_loc` fixed before readout. Current source rows do not close that bundle. Therefore 1790 also runs the strict c_R2/fRR smoke policy: formula-only rows, private closures, partial Gamma-without-Khat rows, and R10-anchor backsolves are rejected.",
            "",
            "**Claim ceiling:** no Gamma/Khat/Ploc owner claim, no q_loc zero/profile claim, no c_R2/fRR zero, no scalaron/R10/PPN score, no local-GR/Newton claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1790.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Owner Bundle Gate",
            markdown_table(rows_map["owner_bundle_gate"], ["owner_id", "bundle_piece", "required_evidence", "current_status", "blocking_reason", "valid_for_claim"]),
            "",
            "## Response to cR2 Link",
            markdown_table(rows_map["response_to_cr2_link"], ["link_id", "object", "mathematical_form", "required_owner", "current_status", "payoff_if_closed", "valid_for_claim"]),
            "",
            "## cR2 Input-Pack Strict Smoke",
            markdown_table(rows_map["cr2_input_pack_strict_smoke"], ["dry_run_id", "candidate", "missing_or_forbidden", "runner_verdict", "reason", "score_emitted", "valid_prediction_row", "valid_for_claim"]),
            "",
            "## q_loc Profile Fallback",
            markdown_table(rows_map["q_loc_profile_fallback"], ["profile_id", "profile_object", "expression", "required_inputs", "current_missing", "row_status", "score_ready", "valid_prediction_row", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel_ledger"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is not a failure of the route; it is the route refusing to cheat. The target has now narrowed to the actual hinge: either derive a response/displacement parent action that makes `K_hat` the metric response of `Gamma_eff` and fixes `P_loc`, or stop calling the local branch a theorem and build source-backed finite q_loc/c_R2 rows. The next checkpoint should refresh 1712 with the 1789/1790 coefficient-law constraints so the conjugacy attempt is tested against the real missing pieces rather than against broad words.",
            "",
        ]
    )


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1790 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
