from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1706"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1706-Y5-R2FR-Delta-w-parent-zero-final-route-or-direct-product-only.md"

SOURCE_FILES = {
    "1705_doc": ROOT / "1705-Y5-R2FR-MICROSCOPE-public-source-probe-or-parent-zero-route-switch.md",
    "1705_validation": OUT / "P8_Y5_BRR545_1705_VALIDATION.csv",
    "1705_next": OUT / "P8_Y5_PARENT_QLOC_1705_NEXT_TARGET.csv",
    "1705_route_decision": OUT / "P8_Y5_PARENT_QLOC_1705_ROUTE_SWITCH_DECISION.csv",
    "1705_source_blocker": OUT / "P8_Y5_PARENT_QLOC_1705_SOURCE_ACQUISITION_BLOCKER.csv",
    "1704_contract": OUT / "P8_Y5_PARENT_QLOC_1704_DROP_FOLDER_CONTRACT.csv",
    "1704_computation_plan": OUT / "P8_Y5_PARENT_QLOC_1704_IF_UNLOCKED_COMPUTATION_PLAN.csv",
    "1703_delta_route": OUT / "P8_Y5_PARENT_QLOC_1703_DELTA_W_ROUTE.csv",
    "1703_direct_route": OUT / "P8_Y5_PARENT_QLOC_1703_DIRECT_PRODUCT_ROUTE.csv",
    "1701_no_reentry": OUT / "P8_Y5_PARENT_QLOC_1701_NO_REENTRY_THEOREM_ATTEMPT.csv",
    "1701_product_map": OUT / "P8_Y5_PARENT_QLOC_1701_ARENA_FINITE_PRODUCT_MAP.csv",
    "1700_signoff": OUT / "P8_Y5_PARENT_QLOC_1700_PARENT_ACTION_SIGNOFF_CONTRACT.csv",
    "1700_counterexamples": OUT / "P8_Y5_PARENT_QLOC_1700_COUNTEREXAMPLE_MERGE.csv",
    "1699_grammar": OUT / "P8_Y5_PARENT_QLOC_1699_PARENT_SOURCE_OWNER_GRAMMAR.csv",
    "1699_hom": OUT / "P8_Y5_PARENT_QLOC_1699_HOM_EXCLUSION_CONDITIONAL_PROOF.csv",
    "1699_signoffs": OUT / "P8_Y5_PARENT_QLOC_1699_REMAINING_SIGNOFFS.csv",
    "1476_delta_w": MICROSCOPE / "branch_locked_wep" / "coefficients" / "Ci_source_weight_delta_w_input_nonclaim_1476.csv",
}

NEEDLES = {
    "1705_doc": ["SWITCH_TO_DELTA_W_PARENT_ZERO_OR_DIRECT_PRODUCT_ONLY", "NEXT1705_0_primary"],
    "1705_validation": ["VAL1705_OVERALL", "PASS"],
    "1705_next": ["1706-Y5-R2FR-Delta-w-parent-zero-final-route-or-direct-product-only.md", "selected"],
    "1705_route_decision": ["DEC1705_1_route_switch", "SWITCH_TO_DELTA_W_PARENT_ZERO_OR_DIRECT_PRODUCT_ONLY"],
    "1705_source_blocker": ["BLK1705_3_manual_request", "continue theory route privately"],
    "1704_contract": ["ART1704_0_readout", "P_WEP_tau_parser_manifest.json"],
    "1704_computation_plan": ["CPU1704_1_direct_product", "P_WEP_source_weight"],
    "1703_delta_route": ["DWR1703_0_parent_zero", "BLOCKED_UNSIGNED_PARENT_GRAMMAR_AND_READOUT"],
    "1703_direct_route": ["DPR1703_3_verdict", "SELECTED_FOR_1704_PARSER_SHELL"],
    "1701_no_reentry": ["NRE1701_5_verdict", "PURE_POSTPROCESSING_ONLY_GENERAL_BLOCKED"],
    "1701_product_map": ["FPM1701_0_WEP_source_weight", "Delta_w_TiPt * tau_WEP or direct P_WEP_source"],
    "1700_signoff": ["SIG1700_6_verdict", "CONTRACT_READY_NOT_SIGNED"],
    "1700_counterexamples": ["CM1700_1_species_kappa", "CM1700_4_readout_reentry"],
    "1699_grammar": ["G1699_4_forbidden_target", "G1699_8_verdict"],
    "1699_hom": ["HP1699_5_Delta_w_result", "blocked_no_claim"],
    "1699_signoffs": ["SO1699_0_parent_grammar_exhaustiveness", "required_before_claim"],
    "1476_delta_w": ["DW1476_0_delta_w_A", "MISSING_THEOREM_ZERO_OR_NUMERIC_DELTA_W"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1706_SOURCE_REGISTER.csv"
ZERO_SIGNATURE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1706_DELTA_W_ZERO_SIGNATURE_AUDIT.csv"
COUNTERMODEL_SURVIVAL = OUT / "P8_Y5_PARENT_QLOC_1706_COUNTERMODEL_SURVIVAL.csv"
ZERO_THEOREM_RESULT = OUT / "P8_Y5_PARENT_QLOC_1706_ZERO_THEOREM_RESULT.csv"
SPLIT_ROUTE_DEMOTION = OUT / "P8_Y5_PARENT_QLOC_1706_SPLIT_DELTA_W_ROUTE_DEMOTION.csv"
DIRECT_PRODUCT_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1706_DIRECT_PRODUCT_ONLY_CONTRACT.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_PARENT_QLOC_1706_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1706_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1706_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1706_VALIDATION.csv"

GENERATED_CSVS = [
    SOURCE_REGISTER,
    ZERO_SIGNATURE_AUDIT,
    COUNTERMODEL_SURVIVAL,
    ZERO_THEOREM_RESULT,
    SPLIT_ROUTE_DEMOTION,
    DIRECT_PRODUCT_CONTRACT,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED_CSVS = [
    ZERO_SIGNATURE_AUDIT,
    COUNTERMODEL_SURVIVAL,
    ZERO_THEOREM_RESULT,
    SPLIT_ROUTE_DEMOTION,
    DIRECT_PRODUCT_CONTRACT,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    ZERO_SIGNATURE_AUDIT: [
        QUARANTINE / "DELTA_W_ZERO_SIGNATURE_AUDIT.csv",
        BRANCH_RESIDUALS / "R2FR_Delta_w_zero_signature_audit_1706.csv",
        QUEUE / "JR1706_DELTA_W_ZERO_SIGNATURE_AUDIT.csv",
    ],
    COUNTERMODEL_SURVIVAL: [
        QUARANTINE / "COUNTERMODEL_SURVIVAL.csv",
        BRANCH_RESIDUALS / "R2FR_countermodel_survival_1706.csv",
        QUEUE / "JR1706_COUNTERMODEL_SURVIVAL.csv",
    ],
    ZERO_THEOREM_RESULT: [
        QUARANTINE / "ZERO_THEOREM_RESULT.csv",
        BRANCH_RESIDUALS / "R2FR_zero_theorem_result_1706.csv",
        QUEUE / "JR1706_ZERO_THEOREM_RESULT.csv",
    ],
    SPLIT_ROUTE_DEMOTION: [
        QUARANTINE / "SPLIT_DELTA_W_ROUTE_DEMOTION.csv",
        BRANCH_RESIDUALS / "R2FR_split_Delta_w_route_demotion_1706.csv",
        QUEUE / "JR1706_SPLIT_DELTA_W_ROUTE_DEMOTION.csv",
    ],
    DIRECT_PRODUCT_CONTRACT: [
        QUARANTINE / "DIRECT_PRODUCT_ONLY_CONTRACT.csv",
        BRANCH_RESIDUALS / "R2FR_direct_product_only_contract_1706.csv",
        QUEUE / "JR1706_DIRECT_PRODUCT_ONLY_CONTRACT.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1706.csv",
        QUEUE / "JR1706_NEXT_TARGET.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_1706.csv",
        QUEUE / "JR1706_CLAIM_GATE.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_key, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC1706_{index}_{source_key}",
                "source_key": source_key,
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "required_needles": ";".join(needles),
                "use_in_1706": "Delta_w zero final theorem gate and direct-product-only demotion",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def zero_signature_rows() -> list[dict[str, Any]]:
    clauses = [
        (
            "ZSG1706_0_interface_category",
            "ordinary matter interface category fixed by parent action",
            "would prevent adding source-only coefficient objects",
            "SIG1700_0_interface_category",
            "UNSIGNED",
            "1700 marks the signoff missing",
        ),
        (
            "ZSG1706_1_grammar_exhaustiveness",
            "source-owner grammar exhaustive",
            "would promote 1699 Hom exclusion from conditional theorem to parent theorem",
            "SO1699_0_parent_grammar_exhaustiveness; EXH1700_6_result",
            "UNSIGNED",
            "1700 verdict is EXHAUSTIVENESS_NOT_DERIVED",
        ),
        (
            "ZSG1706_2_no_source_prefactor",
            "no source/species-only active prefactor target",
            "would kill Coeff_active_source[species] rather than only forbidding it in proposed grammar",
            "G1699_4_forbidden_target; HP1699_5_Delta_w_result",
            "CONDITIONAL_ONLY",
            "works inside unsigned grammar but not parent-signed",
        ),
        (
            "ZSG1706_3_global_source_coupling",
            "one global source coupling",
            "would prevent species/source weighted kappa_A countermodel",
            "SIG1700_3_global_source_coupling; CM1700_1_species_kappa",
            "UNSIGNED_COUNTERMODEL_ACTIVE",
            "species/source weighted active coupling still legal",
        ),
        (
            "ZSG1706_4_no_marker_constants",
            "constants/material markers parent-trivial or retained explicitly",
            "would prevent hidden material marker from reappearing as source weight",
            "SIG1700_2_no_marker_constants; CM1700_0_marker_spurion",
            "UNSIGNED_COUNTERMODEL_ACTIVE",
            "marker/spurion countermodel survives",
        ),
        (
            "ZSG1706_5_readout_no_reentry",
            "readout/effective maps cannot recreate source coefficients",
            "would stop post-variation source-weight reentry",
            "NRE1701_5_verdict; CM1700_4_readout_reentry",
            "PURE_POSTPROCESSING_ONLY_GENERAL_BLOCKED",
            "general readout/effective no-reentry not derived",
        ),
        (
            "ZSG1706_6_no_nonHilbert_tail",
            "non-Hilbert/boundary/source tail zero or retained",
            "would protect local-GR source-side reduction from hidden tails",
            "SIG1700_4_no_nonHilbert_tail; CM1700_5_nonHilbert_source_tail",
            "UNSIGNED_COUNTERMODEL_ACTIVE",
            "non-Hilbert/boundary source tail remains live",
        ),
        (
            "ZSG1706_7_verdict",
            "Delta_w_TiPt=0 parent theorem",
            "requires every clause above to be parent-signed",
            "ZSG1706_0..ZSG1706_6",
            "ZERO_THEOREM_NOT_DERIVED",
            "at least one required parent signature is unsigned; actually several are unsigned",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for clause_id, clause, needed_for, source_anchor, status, blocker in clauses:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "clause_id": clause_id,
                "required_parent_signature": clause,
                "needed_for": needed_for,
                "source_anchor": source_anchor,
                "current_status": status,
                "blocker": blocker,
                "parent_signed": False,
                "zero_theorem_piece": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CMS1706_0_species_kappa",
            "species/source weighted active coupling",
            "S_parent admits kappa_A T_A source weights while preserving formal covariance",
            "blocks Delta_w_TiPt=0 because Ti/Pt can carry relative source weight",
            "parent global source-coupling theorem",
        ),
        (
            "CMS1706_1_readout_reentry",
            "post-variation readout/effective source coefficient",
            "readout/projection/effective map reintroduces source coefficient after a clean parent variation",
            "blocks use of conditional grammar as final local-GR source proof",
            "general readout/effective no-reentry theorem or finite product row",
        ),
        (
            "CMS1706_2_marker_spurion",
            "material marker/spurion constants",
            "ordinary constants carry hidden MTS charge or material marker",
            "blocks treating material/source equality as automatic",
            "parent no-marker theorem or explicit retained coefficient",
        ),
        (
            "CMS1706_3_nonHilbert_tail",
            "non-Hilbert/boundary source tail",
            "Hilbert source universality misses a local boundary/projector/source-support contribution",
            "blocks local-GR overclaim from right-hand source silence",
            "tail zero theorem or finite direct-product residual",
        ),
        (
            "CMS1706_4_terminal_predependence",
            "terminal object but pre-terminal matter dependence",
            "terminal public metric exists but pre-terminal matter functor keeps extra labels",
            "blocks terminal metric from proving source coefficient silence",
            "matter interface through terminal evaluation only",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": countermodel_id,
            "countermodel": countermodel,
            "construction": construction,
            "effect_on_delta_w_zero": effect,
            "required_repair": repair,
            "survives_1706": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for countermodel_id, countermodel, construction, effect, repair in rows
    ]


def zero_theorem_result_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "result_id": "ZTR1706_0_conditional_inside_grammar",
            "statement": "Inside the proposed 1699 source-owner grammar, Hom(species_label,Coeff_active_source)=0 modulo common calibration remains a good conditional theorem.",
            "status": "CONDITIONAL_THEOREM_RETAINED",
            "why_not_claim": "the grammar is not parent-signed as exhaustive and readout/effective reentry is not generally zero",
            "effect": "use as design principle, not as local-GR proof",
            "theorem_zero_present": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "result_id": "ZTR1706_1_parent_zero_attempt",
            "statement": "Delta_w_TiPt=0 as a parent-MTS theorem.",
            "status": "REJECT_PARENT_ZERO_PROMOTION",
            "why_not_claim": "required parent signatures remain unsigned and countermodels survive",
            "effect": "do not set Delta_w_TiPt to zero in any runner",
            "theorem_zero_present": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "result_id": "ZTR1706_2_numeric_delta_w",
            "statement": "Delta_w_TiPt numeric finite input.",
            "status": "MISSING_NUMERIC_INPUT",
            "why_not_claim": "1476 still records MISSING_THEOREM_ZERO_OR_NUMERIC_DELTA_W and tau_WEP is not available",
            "effect": "split Delta_w route cannot score",
            "theorem_zero_present": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "result_id": "ZTR1706_3_final_verdict",
            "statement": "The split Delta_w_TiPt route is not a live claim route after 1706.",
            "status": "DEMOTE_SPLIT_DELTA_W_ROUTE",
            "why_not_claim": "neither theorem-zero nor numeric/source-backed split input exists",
            "effect": "retain direct P_WEP_source_weight only",
            "theorem_zero_present": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def split_demotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "demotion_id": "DEM1706_0_split_formula",
            "object": "P_WEP_source_weight = Delta_w_TiPt * tau_WEP",
            "previous_status": "allowed but unfilled split route",
            "new_status": "DEMOTED_TO_DIAGNOSTIC_ONLY",
            "reason": "both factors are unowned: Delta_w has no zero/numeric row and tau_WEP has no live readout/source/material projection",
            "allowed_future_use": "only as a diagnostic identity if both factors later become source-backed",
            "runner_use": "do_not_score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "demotion_id": "DEM1706_1_delta_w_zero",
            "object": "Delta_w_TiPt=0",
            "previous_status": "theory route under final audit",
            "new_status": "NOT_PARENT_SIGNED",
            "reason": "parent signatures fail 1706 audit",
            "allowed_future_use": "can reopen only if a new parent action signs all required clauses",
            "runner_use": "forbidden_as_default",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "demotion_id": "DEM1706_2_delta_w_bound",
            "object": "abs(Delta_w_TiPt)<=2.8e-15/tau_min",
            "previous_status": "conditional amplitude law",
            "new_status": "HELD_CONDITIONAL_NOT_NUMERIC",
            "reason": "tau_min missing",
            "allowed_future_use": "reopen if a strictly positive tau_min exists",
            "runner_use": "do_not_score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def direct_product_contract_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DPC1706_0_observable",
            "P_WEP_source_weight",
            "direct WEP source-weight product in the reported MICROSCOPE Ti/Pt channel",
            "P_WEP_source_weight = N_eta^-1 <K_CMSM, C_parent[S_Earth,M_TiPt]> or parent-derived direct product theorem",
            "1704 drop-folder contract or future parent product theorem",
            "LIVE_NONCLAIM_BRANCH_OBJECT",
        ),
        (
            "DPC1706_1_no_split_requirement",
            "Delta_w/tau split",
            "split factors are not required for the direct product route",
            "score the forward product only after it is source-backed",
            "1703 direct product route; 1704 computation plan",
            "SPLIT_NOT_REQUIRED",
        ),
        (
            "DPC1706_2_acceptance",
            "acceptance gates",
            "all readout/source/material/C_parent-or-zero/product-convention/manifest artifacts parse with units, signs, hashes and no MISSING markers",
            "no tau=1 shortcut; no bound inversion; no mixed branch; no claim flags before validation",
            "1704 parser shell",
            "PARSER_REQUIRED",
        ),
        (
            "DPC1706_3_current_status",
            "direct product score",
            "not currently score-ready",
            "public source probe did not fill required artifacts",
            "1705 public source probe",
            "BLOCKED_EXTERNAL_OR_PARENT_INPUTS",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "object": obj,
            "statement": statement,
            "formula_or_rule": formula,
            "source_anchor": anchor,
            "current_status": status,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for contract_id, obj, statement, formula, anchor, status in rows
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1706_0_zero_claim", "set Delta_w_TiPt=0", "REJECT_ZERO_CLAIM", "parent signatures unsigned; countermodels survive"),
        ("RUN1706_1_numeric_split", "score split Delta_w*tau_WEP", "REJECT_SPLIT_SCORE", "Delta_w numeric/theorem-zero and tau_WEP are both missing"),
        ("RUN1706_2_delta_w_bound", "convert MICROSCOPE product bound into Delta_w bound", "REJECT_BOUND_CONVERSION", "tau_min missing"),
        ("RUN1706_3_direct_product_now", "score direct P_WEP_source_weight now", "REJECT_DIRECT_PRODUCT_SCORE_NOW", "1704/1705 artifacts not present"),
        ("RUN1706_4_local_gr", "claim local GR/Newton from WEP source branch", "BLOCKED_NO_CLAIM", "source coupling branch remains finite/nonclaim"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "can_score": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, case, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1706_0_primary",
            "next_target": "1707-Y5-R2FR-local-GR-remaining-gates-rollup-after-WEP-demotion.md",
            "script": "scripts/Y5_R2FR_local_GR_remaining_gates_rollup_after_WEP_demotion.py",
            "objective": "roll up the remaining local-GR/Newton gates after WEP split-route demotion and select the highest-payoff next derivation/test branch",
            "selection_status": "selected",
            "success_condition": "explicit remaining-gate map across left-hand GR limit, source side, PPN/R10/orbital/clock tests, with no claim flags",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1706_1_r10",
            "next_target": "1707a-Y5-R2FR-R10-alpha-lambda-projection-fill-runner.md",
            "script": "scripts/Y5_R2FR_R10_alpha_lambda_projection_fill_runner.py",
            "objective": "return to R10 alpha(lambda) projection now that WEP split route is demoted",
            "selection_status": "held_fallback",
            "success_condition": "R10 projection inputs or explicit blockers are source-backed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1706_2_manual_wep",
            "next_target": "1707b-Y5-R2FR-MICROSCOPE-manual-file-import-if-user-supplies-data.md",
            "script": "scripts/Y5_R2FR_MICROSCOPE_manual_file_import_if_user_supplies_data.py",
            "objective": "import live MICROSCOPE files through the 1704 drop contract only if supplied externally",
            "selection_status": "held_external_dependency",
            "success_condition": "live files supplied by user/external team; no invented arrays",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1706_0_delta_w_zero", "Delta_w_TiPt=0 parent theorem", "BLOCKED_NO_CLAIM", "1706 final audit rejects parent-zero promotion"),
        ("CG1706_1_split_score", "split Delta_w*tau_WEP WEP score", "BLOCKED_NO_CLAIM", "split route demoted to diagnostic-only"),
        ("CG1706_2_direct_product", "direct P_WEP_source_weight score", "BLOCKED_NO_CLAIM", "direct product retained but required artifacts/theorem are missing"),
        ("CG1706_3_WEP", "MTS passes MICROSCOPE WEP", "BLOCKED_NO_CLAIM", "no forward product prediction exists"),
        ("CG1706_4_local_GR_Newton", "derived local GR/Newton reduction", "BLOCKED_NO_CLAIM", "WEP source branch remains nonclaim and broader local-GR gates remain open"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, status, reason in gates
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    fields = (
        "parent_signed",
        "zero_theorem_piece",
        "theorem_zero_present",
        "can_score",
        "accepted_for_scoring",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
    )
    for path in paths:
        for row in read_csv(path):
            for field in fields:
                if field in row and truthy(row[field]):
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    markers = (
        "1706-Y5",
        "P8_Y5_PARENT_QLOC_1706",
        "P8_Y5_BRR545_1706",
        "Y5_R2FR_Delta_w_parent_zero_final_route_or_direct_product_only",
    )
    for path in FORMALIZATION.rglob("*"):
        if ".venv" in path.parts or "__pycache__" in path.parts:
            continue
        if any(marker in path.name for marker in markers):
            return False
    return True


def validation_rows() -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    audit = read_csv(ZERO_SIGNATURE_AUDIT)
    countermodels = read_csv(COUNTERMODEL_SURVIVAL)
    theorem = read_csv(ZERO_THEOREM_RESULT)
    demotion = read_csv(SPLIT_ROUTE_DEMOTION)
    direct = read_csv(DIRECT_PRODUCT_CONTRACT)
    runner = read_csv(RUNNER_REFUSAL)
    next_rows_ = read_csv(NEXT_TARGET)
    gates = read_csv(CLAIM_GATE)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1706_0_sources_exist", all(truthy(row["exists"]) for row in sources), "all cited local source paths exist"),
        ("VAL1706_1_needles_present", all(truthy(row["needles_present"]) for row in sources), "all required source needles are present"),
        ("VAL1706_2_signature_audit_complete", {"ZSG1706_0_interface_category", "ZSG1706_1_grammar_exhaustiveness", "ZSG1706_5_readout_no_reentry", "ZSG1706_7_verdict"}.issubset({row["clause_id"] for row in audit}), "zero signature audit covers required parent locks"),
        ("VAL1706_3_zero_not_signed", any(row["clause_id"] == "ZSG1706_7_verdict" and row["current_status"] == "ZERO_THEOREM_NOT_DERIVED" for row in audit), "Delta_w zero theorem is not derived"),
        ("VAL1706_4_countermodels_survive", len(countermodels) >= 5 and all(truthy(row["survives_1706"]) for row in countermodels), "live countermodels survive the final zero attempt"),
        ("VAL1706_5_zero_result_demotes", any(row["result_id"] == "ZTR1706_3_final_verdict" and row["status"] == "DEMOTE_SPLIT_DELTA_W_ROUTE" for row in theorem), "zero theorem result demotes split route"),
        ("VAL1706_6_split_diagnostic_only", any(row["demotion_id"] == "DEM1706_0_split_formula" and row["new_status"] == "DEMOTED_TO_DIAGNOSTIC_ONLY" for row in demotion), "split Delta_w route is diagnostic-only"),
        ("VAL1706_7_direct_product_retained", any(row["contract_id"] == "DPC1706_0_observable" and row["current_status"] == "LIVE_NONCLAIM_BRANCH_OBJECT" for row in direct), "direct WEP product branch is retained"),
        ("VAL1706_8_direct_product_blocked", any(row["contract_id"] == "DPC1706_3_current_status" and row["current_status"] == "BLOCKED_EXTERNAL_OR_PARENT_INPUTS" for row in direct), "direct product is not score-ready"),
        ("VAL1706_9_runner_blocks", runner and all(not truthy(row["can_score"]) and not truthy(row["accepted_for_scoring"]) for row in runner), "runner blocks zero, split, direct-score-now, and local-GR claims"),
        ("VAL1706_10_next_selected", any(row["route_id"] == "NEXT1706_0_primary" and row["selection_status"] == "selected" for row in next_rows_), "next target selected"),
        ("VAL1706_11_claim_gates_blocked", gates and all(row["status"] == "BLOCKED_NO_CLAIM" and not truthy(row["claim_allowed"]) for row in gates), "all claim gates remain blocked"),
        ("VAL1706_12_csv_parse", csv_parses(GENERATED_CSVS), "all generated 1706 CSVs parse"),
        ("VAL1706_13_no_claim_flags", no_claim_flags(CLAIM_CHECKED_CSVS), "all generated score/theorem/prediction/claim flags remain false"),
        ("VAL1706_14_branch_copies", all(path.exists() for path in copies), "branch/quarantine/queue copies exist"),
        ("VAL1706_15_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1706_16_formalization_untouched", formalization_untouched(), "no 1706 outputs found under formalization-workbench outside vendor/env folders"),
    ]
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1706_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1706 Delta_w parent-zero final route or direct-product-only validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    direct: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1706 - Delta_w Parent Zero Final Route Or Direct Product Only",
                "## Verdict\n"
                "- 1706 makes the final parent-signature attempt for `Delta_w_TiPt=0` in this branch and refuses to promote it.\n"
                "- The conditional 1699 Hom/source-owner theorem remains useful, but it is still not parent-signed: grammar exhaustiveness, one global source coupling, no-marker, no non-Hilbert tail, and general readout no-reentry remain unsigned.\n"
                "- Therefore the split formula `P_WEP_source_weight = Delta_w_TiPt * tau_WEP` is demoted to diagnostic-only. It cannot be used to score WEP or claim local GR.\n"
                "- The direct product `P_WEP_source_weight` remains the only live WEP branch object, but it is blocked until either the 1704 data contract is filled or a parent direct-product theorem exists.\n"
                "- No WEP, local-GR/Newton, PPN, R10, clock, orbital, coupling, or public claim is made.",
                "## Source Register",
                markdown_table(sources, ["source_id", "source_key", "source_path", "exists", "needles_present"]),
                "## Delta_w Zero Signature Audit",
                markdown_table(audit, ["clause_id", "required_parent_signature", "current_status", "blocker"]),
                "## Countermodel Survival",
                markdown_table(countermodels, ["countermodel_id", "countermodel", "effect_on_delta_w_zero", "required_repair", "survives_1706"]),
                "## Zero Theorem Result",
                markdown_table(theorem, ["result_id", "statement", "status", "why_not_claim", "effect"]),
                "## Split Delta_w Route Demotion",
                markdown_table(demotion, ["demotion_id", "object", "new_status", "reason", "allowed_future_use"]),
                "## Direct Product Only Contract",
                markdown_table(direct, ["contract_id", "object", "current_status", "formula_or_rule"]),
                "## Runner Refusal",
                markdown_table(runner, ["runner_id", "case", "status", "reason"]),
                "## Next Target",
                markdown_table(next_rows_, ["route_id", "next_target", "objective", "selection_status"]),
                "## Claim Gates",
                markdown_table(gates, ["claim_id", "claim", "status", "reason"]),
                "## Validation",
                markdown_table(validation, ["check_id", "result", "detail"]),
                "## Working Interpretation\n"
                "This is a clean cut, not a defeat. We are no longer carrying a half-owned `Delta_w*tau_WEP` split as if it were physics. The branch now says: either derive/source one forward direct WEP product, or leave WEP as an external-data/manual-request dependency while the project returns to the broader local-GR gate map.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    audit = zero_signature_rows()
    countermodels = countermodel_rows()
    theorem = zero_theorem_result_rows()
    demotion = split_demotion_rows()
    direct = direct_product_contract_rows()
    runner = runner_refusal_rows()
    next_rows_ = next_target_rows()
    gates = claim_gate_rows()
    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_SIGNATURE_AUDIT, audit)
    write_csv(COUNTERMODEL_SURVIVAL, countermodels)
    write_csv(ZERO_THEOREM_RESULT, theorem)
    write_csv(SPLIT_ROUTE_DEMOTION, demotion)
    write_csv(DIRECT_PRODUCT_CONTRACT, direct)
    write_csv(RUNNER_REFUSAL, runner)
    write_csv(NEXT_TARGET, next_rows_)
    write_csv(CLAIM_GATE, gates)
    copy_outputs()
    remove_pycache()
    validation = validation_rows()
    write_csv(VALIDATION, validation)
    write_doc(sources, audit, countermodels, theorem, demotion, direct, runner, next_rows_, gates, validation)
    failed = [row for row in validation if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("1706 validation PASS")


if __name__ == "__main__":
    main()
