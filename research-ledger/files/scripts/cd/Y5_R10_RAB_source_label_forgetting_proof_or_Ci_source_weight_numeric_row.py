from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1476"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1476-Y5-R10-RAB-source-label-forgetting-proof-or-Ci-source-weight-numeric-row.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1475_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1475_VALIDATION.csv"
PREV_SMOKE = OUT / "P8_Y5_R10_1475_CI_SMOKE_EVALUATOR_RESULTS.csv"
PREV_PROOF = OUT / "P8_Y5_R10_1475_FIRST_CI_PROOF_ATTEMPT.csv"
PREV_REJECTION = OUT / "P8_Y5_R10_1475_CLAIM_ROW_REJECTION_LEDGER.csv"
CI_MAP_1474 = OUT / "P8_Y5_R10_1474_COMPLETE_CI_PARENT_ACTION_MAP.csv"
EVALUATORS_1474 = OUT / "P8_Y5_R10_1474_CI_RESIDUAL_EVALUATOR_ROWS.csv"

SOURCE_FORGET_1063 = OUT / "P8_Y5_R10_1063_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv"
SOURCE_SCALAR_1066 = OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv"
ACTION_SCALE_1067 = OUT / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv"
SOURCE_WEIGHT_1067 = OUT / "P8_Y5_R10_1067_SOURCE_WEIGHT_CONSEQUENCE_LEDGER.csv"
TAU_SCHEMA_1067 = OUT / "P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv"
OWNER_GATES_1076 = OUT / "P8_Y5_R10_1076_COUPLING_OWNER_GATES.csv"
WEP_OWNER_1077 = OUT / "P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv"
SOURCE_COUPLING_1229 = OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv"
SOURCE_GATE_1230 = OUT / "P8_Y5_R10_1230_LOCAL_GR_SOURCE_COUPLING_GATE_UPDATE.csv"
CONNECTED_1231 = OUT / "P8_Y5_R10_1231_MATTER_CATEGORY_CONNECTEDNESS_ATTEMPT.csv"
STACK_1231 = OUT / "P8_Y5_R10_1231_SOURCE_LABEL_FORGETTING_PROOF_STACK.csv"
HILBERT_1450 = OUT / "P8_Y5_R10_1450_HILBERT_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv"
MEASURE_CURRENT_1452 = OUT / "P8_Y5_R10_1452_COMMON_MEASURE_CURRENT_THEOREM_ATTEMPT.csv"
CURRENT_AUDIT_1452 = OUT / "P8_Y5_R10_1452_CURRENT_OWNER_AUDIT.csv"
NO_RELATIVE_1461 = OUT / "P8_Y5_R10_1461_NO_RELATIVE_SOURCE_LABEL_AUDIT.csv"
COUNTER_1461 = OUT / "P8_Y5_R10_1461_SOURCE_LABEL_COUNTERMODEL_AUDIT.csv"
MEASURE_SIGNATURE_1462 = OUT / "P8_Y5_R10_1462_COMMON_MEASURE_CURRENT_SIGNATURE_ATTEMPT.csv"
CURRENT_UPDATE_1462 = OUT / "P8_Y5_R10_1462_CURRENT_OWNER_UPDATE.csv"
CONNECTED_AUDIT_1463 = OUT / "P8_Y5_R10_1463_CONNECTED_MATTER_NATURALITY_AUDIT.csv"
CONNECTED_PROOF_1464 = OUT / "P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv"
SOURCE_IMPACT_1467 = OUT / "P8_Y5_R10_1467_SOURCE_LABEL_FORGETTING_IMPACT.csv"
NEWTON_SPINE_956 = OUT / "P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv"

LIVE_DELTAW_INPUT = COEFF / "Ci_source_weight_delta_w_claim_input.csv"
LIVE_SOURCE_FORGET = COEFF / "source_label_forgetting_parent_signed_import.csv"
LIVE_NEWTON = COEFF / "Newton_transfer_claim_rows.csv"
LIVE_LOCAL_GR = COEFF / "local_GR_claim_promotion_rows.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1476_SOURCE_REGISTER.csv"
PROOF_ATTEMPT = OUT / "P8_Y5_R10_1476_SOURCE_LABEL_FORGETTING_PROOF_ATTEMPT.csv"
PREMISE_AUDIT = OUT / "P8_Y5_R10_1476_SOURCE_LABEL_PREMISE_AUDIT.csv"
DELTAW_INPUT = OUT / "P8_Y5_R10_1476_DELTA_W_SOURCE_WEIGHT_INPUT_ROW_NONCLAIM.csv"
EVALUATOR_UPDATE = OUT / "P8_Y5_R10_1476_CI_SOURCE_WEIGHT_EVALUATOR_UPDATE.csv"
COUNTERMODELS = OUT / "P8_Y5_R10_1476_COUNTERMODEL_LEDGER.csv"
LIVE_GUARD = OUT / "P8_Y5_R10_1476_LIVE_IMPORT_GUARD.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1476_REDUCTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1476_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1476_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1476_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1476_VALIDATION.csv"

QUAR_DELTAW = QUARANTINE / "DELTA_W_SOURCE_WEIGHT_INPUT_ROW_NONCLAIM.csv"
QUAR_PROOF = QUARANTINE / "SOURCE_LABEL_FORGETTING_PROOF_ATTEMPT.csv"
BRANCH_DELTAW = COEFF / "Ci_source_weight_delta_w_input_nonclaim_1476.csv"
BRANCH_PROOF = COEFF / "source_label_forgetting_proof_attempt_nonclaim_1476.csv"
BRANCH_SIGNING = COEFF / "source_label_forgetting_signing_decision_1476.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def copy_branch(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC1476_0_1475_next", PREV_NEXT, "1475 handoff to source-label forgetting or delta_w input row"),
        ("SRC1476_1_1475_validation", PREV_VALIDATION, "1475 validation baseline"),
        ("SRC1476_2_1475_smoke", PREV_SMOKE, "C_i smoke evaluator row for CI1474_1"),
        ("SRC1476_3_1475_proof", PREV_PROOF, "first C_i source-weight proof attempt"),
        ("SRC1476_4_1475_rejection", PREV_REJECTION, "claim rejection ledger"),
        ("SRC1476_5_Ci_map", CI_MAP_1474, "C_i parent-action map"),
        ("SRC1476_6_Ci_eval", EVALUATORS_1474, "C_i evaluator rows"),
        ("SRC1476_7_1063_source", SOURCE_FORGET_1063, "source forgetting theorem attempt"),
        ("SRC1476_8_1066_scalar", SOURCE_SCALAR_1066, "source scalar exclusion lemma"),
        ("SRC1476_9_1067_action", ACTION_SCALE_1067, "parent action scale owner attempt"),
        ("SRC1476_10_1067_weight", SOURCE_WEIGHT_1067, "source weight consequence ledger"),
        ("SRC1476_11_1067_tau", TAU_SCHEMA_1067, "tau/delta_w acquisition schema"),
        ("SRC1476_12_1076_owner_gates", OWNER_GATES_1076, "coupling owner gates"),
        ("SRC1476_13_1077_wep_owner", WEP_OWNER_1077, "parent WEP coupling owner theorem attempt"),
        ("SRC1476_14_1229_source", SOURCE_COUPLING_1229, "local-GR source coupling theorem contract"),
        ("SRC1476_15_1230_gate", SOURCE_GATE_1230, "source coupling gate update"),
        ("SRC1476_16_1231_connected", CONNECTED_1231, "matter category connectedness attempt"),
        ("SRC1476_17_1231_stack", STACK_1231, "source-label forgetting proof stack"),
        ("SRC1476_18_1450_hilbert", HILBERT_1450, "Hilbert source label forgetting theorem attempt"),
        ("SRC1476_19_1452_measure", MEASURE_CURRENT_1452, "common measure/current theorem attempt"),
        ("SRC1476_20_1452_current", CURRENT_AUDIT_1452, "current owner audit"),
        ("SRC1476_21_1461_no_relative", NO_RELATIVE_1461, "no-relative-source-label audit"),
        ("SRC1476_22_1461_counter", COUNTER_1461, "source-label countermodel audit"),
        ("SRC1476_23_1462_signature", MEASURE_SIGNATURE_1462, "common measure/current signature attempt"),
        ("SRC1476_24_1462_update", CURRENT_UPDATE_1462, "current owner update"),
        ("SRC1476_25_1463_connected_audit", CONNECTED_AUDIT_1463, "connected matter naturality audit"),
        ("SRC1476_26_1464_connected_proof", CONNECTED_PROOF_1464, "connected matter category proof attempt"),
        ("SRC1476_27_1467_impact", SOURCE_IMPACT_1467, "source-label forgetting impact"),
        ("SRC1476_28_newton_spine", NEWTON_SPINE_956, "source-side GR/Newton spine"),
    ]
    return [
        {
            "source_id": source_id,
            "source_type": "local_file",
            "path_or_url": rel(path),
            "exists": path.exists(),
            "usage": usage,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, usage in local_sources
    ]


def proof_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "SLF1476_0_target",
            "ci_id": "CI1474_1_source_weight",
            "claim_piece": "source-label forgetting kills relative source weights",
            "formal_statement": "If the parent ordinary-matter source functor has domain Stress_total rather than labelled pairs {(T_A,A)}, then source labels are not legal arguments and relative weights delta_w_A cannot be formed after variation.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_move": "variation-before-readout gives T_total; a covariant additive source map on T_total has one common normalization only",
            "missing_for_parent_claim": "parent-signed source-functor domain and readout no-reentry theorem",
            "source_artifact": rel(HILBERT_1450),
            "source_anchor": "HT1450_1_total_Hilbert_variation;HT1450_2_covariant_additive_uniqueness;HT1450_6_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "SLF1476_1_connected_naturality",
            "ci_id": "CI1474_1_source_weight",
            "claim_piece": "connected matter category collapses action-density weights",
            "formal_statement": "If ordinary source-relevant sectors form one connected parent category and action-density normalization is natural on that category, naturality forces all w_A=w_*.",
            "proof_status": "EXACT_CATEGORY_LEMMA_CONDITIONAL",
            "proof_move": "for each nonzero morphism f:A->B, w_B F(f)=F(f)w_A implies w_A=w_B; connectedness propagates a common weight",
            "missing_for_parent_claim": "parent-owned interaction/morphism graph and action-density line owner",
            "source_artifact": rel(CONNECTED_PROOF_1464),
            "source_anchor": "CON1464_1_naturality_lemma;CON1464_5_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "SLF1476_2_measure_current_owner",
            "ci_id": "CI1474_1_source_weight",
            "claim_piece": "common measure/current owner forbids pre-variation source weights",
            "formal_statement": "If S_ord/hbar_parent has one action scale, one species-blind measure/Jacobian, one Hilbert/coframe current owner, and no non-Hilbert bypass, then w_A, J_A, c_A, and zeta_A reduce to common mode or zero.",
            "proof_status": "CONDITIONAL_ROUTE_CLEAN_NOT_SIGNED",
            "proof_move": "classical EOM scaling is rejected; only parent action-scale/measure/current ownership can remove the pre-variation weight",
            "missing_for_parent_claim": "hbar/action measure owner, species-blind Jacobian, current owner, and non-Hilbert silence",
            "source_artifact": rel(MEASURE_SIGNATURE_1462),
            "source_anchor": "CMC1462_2_single_hbar_route;CMC1462_4_species_jacobian_countermodel;CMC1462_6_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "SLF1476_3_countermodel",
            "ci_id": "CI1474_1_source_weight",
            "claim_piece": "relative source-weight countermodel remains live",
            "formal_statement": "S_matter=sum_A w_A S_A is covariant and additive and can preserve isolated classical EOM form while changing Hilbert source T_source=sum_A w_A T_A.",
            "proof_status": "COUNTERMODEL_SURVIVES",
            "proof_move": "this is the exact loophole the parent action must forbid; it cannot be removed by covariance, additivity, or classical EOM alone",
            "missing_for_parent_claim": "object-language/no-source-scalar theorem plus common measure/current owner",
            "source_artifact": rel(COUNTER_1461),
            "source_anchor": "CM1461_0_relative_wA;CM1461_1_species_measure_jacobian",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "proof_id": "SLF1476_4_verdict",
            "ci_id": "CI1474_1_source_weight",
            "claim_piece": "CI1474_1 source-weight status",
            "formal_statement": "SLF1476_0 through SLF1476_2 would close CI1474_1, but parent ownership of the source functor, connected matter graph, measure/current owner, and readout no-reentry is still unsigned.",
            "proof_status": "NOT_PARENT_DERIVED_EMIT_DELTA_W_INPUT_ROW",
            "proof_move": "keep CI1474_1 failing in the evaluator and emit a nonclaim delta_w_A input row",
            "missing_for_parent_claim": "all source-label forgetting premises parent-signed together",
            "source_artifact": rel(NO_RELATIVE_1461),
            "source_anchor": "NRS1461_5_delta_q_zero_decision",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def premise_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "SLP1476_0_source_functor_domain",
            "premise": "source functor domain is total Hilbert stress, not labelled stress pairs",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "source_artifact": rel(NO_RELATIVE_1461),
            "source_anchor": "NRS1461_0_source_functor_domain",
            "blocks_delta_w_zero": True,
            "next_action": "parent-sign variation-before-readout and readout no-reentry",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "SLP1476_1_connected_matter_category",
            "premise": "ordinary matter action-density category is connected for source normalization",
            "current_status": "GRAPH_NOT_PARENT_SIGNED",
            "source_artifact": rel(CONNECTED_AUDIT_1463),
            "source_anchor": "CMA1463_0_interaction_graph",
            "blocks_delta_w_zero": True,
            "next_action": "build parent-owned graph/morphism certificate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "SLP1476_2_action_measure_owner",
            "premise": "one hbar/action measure/Jacobian for all ordinary matter sectors",
            "current_status": "MISSING_AXIOM_NOT_REDUCED",
            "source_artifact": rel(MEASURE_CURRENT_1452),
            "source_anchor": "CMT1452_2_quantum_measure_route;CMT1452_3_species_jacobian_countermodel",
            "blocks_delta_w_zero": True,
            "next_action": "derive parent measure/action-density line owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "SLP1476_3_current_owner",
            "premise": "single current/source normalization owner forbids c_A J_A",
            "current_status": "CURRENT_OWNER_NOT_SIGNED",
            "source_artifact": rel(CURRENT_AUDIT_1452),
            "source_anchor": "COA1452_4_verdict",
            "blocks_delta_w_zero": True,
            "next_action": "derive Noether/Hilbert/readout current owner stack",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "SLP1476_4_nonHilbert_silence",
            "premise": "no non-Hilbert current bypasses total stress source",
            "current_status": "OPEN_PARALLEL_GATE",
            "source_artifact": rel(HILBERT_1450),
            "source_anchor": "HT1450_5_nonHilbert_guard",
            "blocks_delta_w_zero": True,
            "next_action": "prove J_NH=0/exact/projected-silent or emit numeric residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "premise_id": "SLP1476_5_readout_no_reentry",
            "premise": "source-worldtube/readout kernels cannot recreate species labels after variation",
            "current_status": "CONDITIONAL_SOURCE_FILES_MISSING",
            "source_artifact": rel(NO_RELATIVE_1461),
            "source_anchor": "NRS1461_4_readout_no_reentry",
            "blocks_delta_w_zero": True,
            "next_action": "source official readout/worldtube kernels or parent no-reentry theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def delta_w_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "DW1476_0_delta_w_A",
            "ci_id": "CI1474_1_source_weight",
            "quantity": "delta_w_A or Delta_w_TiPt",
            "definition": "relative ordinary-matter source/action weight after removing any common source normalization",
            "formula": "q_source^nu = P_loc nabla_mu[sum_A delta_w_A T_A^{mu nu}] + boundary/projector/readout terms",
            "accepted_evidence": "parent theorem-zero certificate OR numeric/source-backed delta_w vector with units/sign/source anchor/no-cancellation statement",
            "current_value": "MISSING_THEOREM_ZERO_OR_NUMERIC_DELTA_W",
            "units": "dimensionless source/action weight",
            "bound_or_gate": "if tau_WEP numeric and nonzero, abs(Delta_w_TiPt) <= 2.8e-15/abs(tau_WEP); otherwise direct q_source/Newton/WEP/R10 evaluator",
            "source_artifact": rel(TAU_SCHEMA_1067),
            "source_anchor": "TAQ1067_2_delta_w_width_if_tau;TAQ1067_3_direct_product_option;TAQ1067_4_refusal_rule",
            "numeric_input_present": False,
            "theorem_zero_present": False,
            "passes_required_gate": False,
            "valid_for_Newton": False,
            "valid_for_PPN": False,
            "valid_for_local_GR": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": "DW1476_1_tau_WEP_dependency",
            "ci_id": "CI1474_1_source_weight",
            "quantity": "tau_WEP for Delta_w width conversion",
            "definition": "normalized lab/source/orbit projection converting relative source weight into WEP observable",
            "formula": "P_WEP_source_weight = Delta_w_TiPt * tau_WEP or direct parent product",
            "accepted_evidence": "parent theorem-zero WEP projection OR numeric local source/orbit/readout integral",
            "current_value": "MISSING_TAU_WEP",
            "units": "dimensionless projection factor",
            "bound_or_gate": "required before converting eta bound into abs(Delta_w_TiPt) width",
            "source_artifact": rel(TAU_SCHEMA_1067),
            "source_anchor": "TAQ1067_0_tau_zero_option;TAQ1067_1_tau_numeric_option",
            "numeric_input_present": False,
            "theorem_zero_present": False,
            "passes_required_gate": False,
            "valid_for_Newton": False,
            "valid_for_PPN": False,
            "valid_for_local_GR": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def evaluator_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "update_id": "EUP1476_0_CI1474_1",
            "ci_id": "CI1474_1_source_weight",
            "previous_smoke_status": "FAIL_EXPECTED_NONCLAIM",
            "new_input_rows": "DW1476_0_delta_w_A;DW1476_1_tau_WEP_dependency",
            "theorem_route_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "numeric_route_status": "INPUT_ROW_WRITTEN_MISSING_VALUE",
            "evaluator_status": "STILL_FAILS",
            "blocks_Newton": True,
            "blocks_PPN": True,
            "blocks_local_GR": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1476_0_relative_wA",
            "countermodel": "S_matter=sum_A w_A S_A remains covariant/additive while changing Hilbert source weights",
            "why_survives": "common measure/action-scale owner is not parent-derived",
            "killed_by_1476": False,
            "needed_to_kill": "single action-density line and no source-only scalar slot",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1476_1_species_jacobian",
            "countermodel": "species-dependent path/statistical measure Jacobian J_A mimics source weight",
            "why_survives": "species-blind measure/Jacobian theorem is unsigned",
            "killed_by_1476": False,
            "needed_to_kill": "parent measure owner and hbar/action-scale proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1476_2_nonHilbert_current",
            "countermodel": "J_src = kappa T_Hilbert + zeta_A J_NH,A bypasses Hilbert source label forgetting",
            "why_survives": "non-Hilbert current silence remains a parallel open gate",
            "killed_by_1476": False,
            "needed_to_kill": "J_NH zero/exact/projected-silent theorem or numeric residual bound",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1476_3_readout_reentry",
            "countermodel": "source/readout kernel acts on material/source labels after common Hilbert variation",
            "why_survives": "official source-worldtube/readout kernels are not signed/imported",
            "killed_by_1476": False,
            "needed_to_kill": "readout no-reentry theorem or source-backed kernels",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def live_guard_rows() -> list[dict[str, Any]]:
    guarded = [
        ("LG1476_0_deltaw", LIVE_DELTAW_INPUT, "live delta_w claim input"),
        ("LG1476_1_source_forget", LIVE_SOURCE_FORGET, "live parent-signed source-label forgetting import"),
        ("LG1476_2_Newton", LIVE_NEWTON, "Newton transfer claim rows"),
        ("LG1476_3_local_GR", LIVE_LOCAL_GR, "local-GR claim promotion rows"),
    ]
    return [
        {
            "guard_id": guard_id,
            "path": rel(path),
            "meaning": meaning,
            "exists_now": path.exists(),
            "would_write_in_1476": False,
            "status": "ABSENT_EXPECTED" if not path.exists() else "PRESENT_PREEXISTING_REVIEW_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, path, meaning in guarded
    ]


def reduction_gate_rows(proofs: list[dict[str, Any]], premises: list[dict[str, Any]], inputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    exact_conditional = any(row["proof_status"] in {"EXACT_CONDITIONAL_THEOREM", "EXACT_CATEGORY_LEMMA_CONDITIONAL"} for row in proofs)
    countermodel_retained = any(row["proof_status"] == "COUNTERMODEL_SURVIVES" for row in proofs)
    refusal = any(row["proof_status"] == "NOT_PARENT_DERIVED_EMIT_DELTA_W_INPUT_ROW" for row in proofs)
    premises_block = all(truth(row["blocks_delta_w_zero"]) and not truth(row["claim_allowed"]) for row in premises)
    input_missing = all(not truth(row["numeric_input_present"]) and not truth(row["theorem_zero_present"]) and not truth(row["passes_required_gate"]) for row in inputs)
    return [
        {
            "gate_id": "GATE1476_0_conditional_proof",
            "gate": "source-label forgetting proof is exact conditionally",
            "gate_pass": exact_conditional,
            "claim_effect": "theorem target only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1476_1_countermodel_retained",
            "gate": "relative source-weight countermodel remains live",
            "gate_pass": countermodel_retained,
            "claim_effect": "blocks proof promotion",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1476_2_premises_block",
            "gate": "all source-label premises remain blocking/nonclaim",
            "gate_pass": premises_block,
            "claim_effect": "delta_w theorem-zero not promoted",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1476_3_delta_w_input_written",
            "gate": "delta_w numeric/theorem input rows are written",
            "gate_pass": len(inputs) >= 2,
            "claim_effect": "input scaffold only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1476_4_delta_w_still_missing",
            "gate": "delta_w/tau inputs remain missing and fail",
            "gate_pass": input_missing,
            "claim_effect": "CI1474_1 still fails evaluator",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1476_5_refusal_recorded",
            "gate": "source-label proof promotion refusal is recorded",
            "gate_pass": refusal,
            "claim_effect": "no source-weight pass",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1476_6_local_GR_claim",
            "gate": "Newton/PPN/local-GR claim allowed",
            "gate_pass": False,
            "claim_effect": "explicitly forbidden in 1476",
            "valid_for_claim": False,
        },
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1476_0_source_label_forgetting",
            "target": "CI1474_1 source-weight source-label forgetting or delta_w input",
            "conditional_proof_written": True,
            "parent_source_functor_signed": False,
            "connected_matter_category_signed": False,
            "measure_current_owner_signed": False,
            "readout_no_reentry_signed": False,
            "delta_w_input_row_written": True,
            "delta_w_numeric_present": False,
            "source_weight_claim_allowed": False,
            "Newton_transfer_allowed": False,
            "PPN_claim_allowed": False,
            "local_GR_claim_allowed": False,
            "decision": "REFUSE_SOURCE_LABEL_FORGETTING_PROMOTION_KEEP_DELTA_W_INPUT_NONCLAIM",
            "reason": "the proof route is clean but parent signatures are still unsigned, and delta_w/tau inputs remain missing",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1476_0",
            "decision": "source-label forgetting is the correct proof route",
            "why": "if parent-signed, it removes the source-weight residual from Newton, WEP, R10, and local GR",
            "consequence": "focus next proof work on parent source-functor domain and matter-category connectedness",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1476_1",
            "decision": "proof does not promote",
            "why": "relative w_A, species Jacobian, non-Hilbert current, and readout re-entry countermodels survive",
            "consequence": "CI1474_1 remains failing in the smoke evaluator",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1476_2",
            "decision": "delta_w input row is now explicit",
            "why": "if proof stalls, numeric/source-backed delta_w and tau_WEP inputs can be filled without changing the theory prose",
            "consequence": "next step can attack connectedness or fill evaluator input schema",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1476_0_1477",
            "next_target": "1477-Y5-R10-RAB-connected-matter-graph-certificate-or-delta-w-input-schema-runner.md",
            "script": "scripts/Y5_R10_RAB_connected_matter_graph_certificate_or_delta_w_input_schema_runner.py",
            "objective": "try to build a parent-owned connected ordinary-matter graph certificate for action-density weights; if it fails, harden the delta_w/tau_WEP evaluator input schema",
            "include": "morphism graph; action-density line; direct-sum obstruction; common-mode calibration; delta_w units/sign/source/no-cancellation fields",
            "exclude": "GitHub action; formalization-workbench edits; local-GR pass; WEP/R10/clock claim promotion; bound inversion",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_csvs() -> list[Path]:
    return [
        SOURCE_REGISTER,
        PROOF_ATTEMPT,
        PREMISE_AUDIT,
        DELTAW_INPUT,
        EVALUATOR_UPDATE,
        COUNTERMODELS,
        QUAR_DELTAW,
        QUAR_PROOF,
        LIVE_GUARD,
        REDUCTION_GATES,
        SIGNING_DECISION,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]


def csv_parse_clean(paths: list[Path]) -> bool:
    try:
        return all(read_csv_rows(path) for path in paths)
    except Exception:
        return False


def branch_copies_exist() -> bool:
    return BRANCH_DELTAW.exists() and BRANCH_PROOF.exists() and BRANCH_SIGNING.exists()


def validation_rows(
    sources: list[dict[str, Any]],
    proofs: list[dict[str, Any]],
    premises: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    evaluator_update: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    local_sources_exist = all(row["source_type"] != "local_file" or truth(row["exists"]) for row in sources)
    proof_sources_exist = all((ROOT / row["source_artifact"]).exists() for row in proofs)
    conditional_proof = any(row["proof_status"] in {"EXACT_CONDITIONAL_THEOREM", "EXACT_CATEGORY_LEMMA_CONDITIONAL"} for row in proofs)
    refusal = any(row["proof_status"] == "NOT_PARENT_DERIVED_EMIT_DELTA_W_INPUT_ROW" for row in proofs)
    premises_sources_exist = all((ROOT / row["source_artifact"]).exists() for row in premises)
    premises_block = all(truth(row["blocks_delta_w_zero"]) and not truth(row["claim_allowed"]) for row in premises)
    input_sources_exist = all((ROOT / row["source_artifact"]).exists() for row in inputs)
    input_rows_fail = all(row["current_value"].startswith("MISSING") and not truth(row["passes_required_gate"]) and not truth(row["claim_allowed"]) for row in inputs)
    evaluator_still_fails = all(row["evaluator_status"] == "STILL_FAILS" and truth(row["blocks_Newton"]) and truth(row["blocks_local_GR"]) for row in evaluator_update)
    countermodels_retained = all(not truth(row["killed_by_1476"]) for row in countermodels)
    live_paths_untouched = all(not truth(row["exists_now"]) and not truth(row["would_write_in_1476"]) for row in live_guard)
    safe_gate_pattern = all(truth(row["gate_pass"]) for row in gates[:-1]) and not truth(gates[-1]["gate_pass"])
    signing_refuses = all(
        truth(row["conditional_proof_written"])
        and truth(row["delta_w_input_row_written"])
        and not truth(row["parent_source_functor_signed"])
        and not truth(row["connected_matter_category_signed"])
        and not truth(row["measure_current_owner_signed"])
        and not truth(row["readout_no_reentry_signed"])
        and not truth(row["delta_w_numeric_present"])
        and not truth(row["source_weight_claim_allowed"])
        and not truth(row["Newton_transfer_allowed"])
        and not truth(row["local_GR_claim_allowed"])
        for row in signing
    )
    generated_parse = csv_parse_clean(generated_csvs())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = formalization_modified_count() == 0
    checks = [
        ("VAL1476_0_sources", local_sources_exist, "all cited local source paths exist"),
        ("VAL1476_1_proof_sources", proof_sources_exist, "all proof source artifacts exist"),
        ("VAL1476_2_conditional_proof", conditional_proof, "source-label forgetting proof is conditional/exact"),
        ("VAL1476_3_refusal", refusal, "proof promotion refused"),
        ("VAL1476_4_premise_sources", premises_sources_exist, "all premise source artifacts exist"),
        ("VAL1476_5_premises_block", premises_block, "premises block delta_w theorem-zero"),
        ("VAL1476_6_input_sources", input_sources_exist, "all delta_w input source artifacts exist"),
        ("VAL1476_7_input_rows_fail", input_rows_fail, "delta_w/tau input rows remain missing and fail"),
        ("VAL1476_8_evaluator_still_fails", evaluator_still_fails, "CI1474_1 evaluator remains failing"),
        ("VAL1476_9_countermodels", countermodels_retained, "all countermodels retained"),
        ("VAL1476_10_live_paths", live_paths_untouched, "critical live claim/import paths remain absent"),
        ("VAL1476_11_gate_pattern", safe_gate_pattern, "conditional/input/refusal gates pass while claim gate fails"),
        ("VAL1476_12_signing_refuses", signing_refuses, "parent signing refuses source-weight/Newton/local-GR promotion"),
        ("VAL1476_13_generated_csv_parse", generated_parse, "all generated 1476 CSVs parse cleanly"),
        ("VAL1476_14_branch_copies", branch_copies_exist(), "nonclaim branch/quarantine copies written"),
        ("VAL1476_15_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1476_16_formalization_untouched", formalization_untouched, f"formalization modified-file count since start={formalization_modified_count()}"),
    ]
    overall = all(result for _, result, _ in checks)
    checks.append(("VAL1476_17_overall", overall, "1476 keeps source-label forgetting conditional and emits failing delta_w input rows"))
    generated = now()
    return [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": generated,
        }
        for check_id, result, detail in checks
    ]


def write_doc(
    sources: list[dict[str, Any]],
    proofs: list[dict[str, Any]],
    premises: list[dict[str, Any]],
    inputs: list[dict[str, Any]],
    evaluator_update: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines: list[str] = []
    lines.append("# 1476 - Y5 R10 RAB Source-Label Forgetting Proof Or C_i Source-Weight Numeric Row")
    lines.append("")
    lines.append("## Verdict")
    lines.append("- Source-label forgetting is exact conditionally: if the parent source functor sees only total Hilbert stress and the action-density/measure/current/readout owners are signed, relative `delta_w_A` cannot form.")
    lines.append("- The proof is not parent-derived yet: connected matter graph, common measure/current owner, non-Hilbert silence, and readout no-reentry remain open.")
    lines.append("- A nonclaim `delta_w_A` input row now exists, but it is missing theorem-zero/numeric content and keeps `CI1474_1` failing.")
    lines.append("")
    lines.append("## Proof Attempt")
    lines.append("| proof_id | proof_status | missing_for_parent_claim |")
    lines.append("|---|---|---|")
    for row in proofs:
        lines.append(f"| {row['proof_id']} | {row['proof_status']} | {row['missing_for_parent_claim']} |")
    lines.append("")
    lines.append("## Premise Audit")
    lines.append("| premise_id | current_status | next_action |")
    lines.append("|---|---|---|")
    for row in premises:
        lines.append(f"| {row['premise_id']} | {row['current_status']} | {row['next_action']} |")
    lines.append("")
    lines.append("## Delta-w Input Rows")
    lines.append("| input_id | quantity | current_value | bound_or_gate |")
    lines.append("|---|---|---|---|")
    for row in inputs:
        lines.append(f"| {row['input_id']} | {row['quantity']} | {row['current_value']} | {row['bound_or_gate']} |")
    lines.append("")
    lines.append("## Evaluator Update")
    for row in evaluator_update:
        lines.append(f"- `{row['update_id']}`: `{row['evaluator_status']}` with inputs `{row['new_input_rows']}`.")
    lines.append("")
    lines.append("## Gates")
    lines.append("| gate_id | gate_pass | claim_effect |")
    lines.append("|---|---:|---|")
    for row in gates:
        lines.append(f"| {row['gate_id']} | {row['gate_pass']} | {row['claim_effect']} |")
    lines.append("")
    lines.append("## Parent Signing Decision")
    for row in signing:
        lines.append(f"- `{row['decision_id']}`: `{row['decision']}` because {row['reason']}.")
    lines.append("")
    lines.append("## Decision Ledger")
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} - {row['consequence']}.")
    lines.append("")
    lines.append("## Validation")
    lines.append("| check_id | result | detail |")
    lines.append("|---|---|---|")
    for row in validation:
        lines.append(f"| {row['check_id']} | {row['result']} | {row['detail']} |")
    lines.append("")
    lines.append("## Source Register")
    lines.append("| source_id | exists | path_or_url | usage |")
    lines.append("|---|---:|---|---|")
    for row in sources:
        lines.append(f"| {row['source_id']} | {row['exists']} | `{row['path_or_url']}` | {row['usage']} |")
    lines.append("")
    lines.append("## Next Target")
    for row in next_target:
        lines.append(f"- `{row['next_target']}` via `{row['script']}`: {row['objective']}")
    lines.append("")
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sources = source_rows()
    proofs = proof_attempt_rows()
    premises = premise_rows()
    inputs = delta_w_input_rows()
    evaluator_update = evaluator_update_rows()
    countermodels = countermodel_rows()
    live_guard = live_guard_rows()
    gates = reduction_gate_rows(proofs, premises, inputs)
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PROOF_ATTEMPT, proofs)
    write_csv(PREMISE_AUDIT, premises)
    write_csv(DELTAW_INPUT, inputs)
    write_csv(EVALUATOR_UPDATE, evaluator_update)
    write_csv(COUNTERMODELS, countermodels)
    write_csv(QUAR_DELTAW, inputs)
    write_csv(QUAR_PROOF, proofs)
    write_csv(LIVE_GUARD, live_guard)
    write_csv(REDUCTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(DELTAW_INPUT, BRANCH_DELTAW)
    copy_branch(PROOF_ATTEMPT, BRANCH_PROOF)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    validation = validation_rows(sources, proofs, premises, inputs, evaluator_update, countermodels, live_guard, gates, signing)
    write_csv(VALIDATION, validation)
    write_doc(sources, proofs, premises, inputs, evaluator_update, gates, signing, decisions, validation, next_target)
    print("Y5_R10_1476_source_label_forgetting_conditional_delta_w_input_nonclaim")


if __name__ == "__main__":
    main()
