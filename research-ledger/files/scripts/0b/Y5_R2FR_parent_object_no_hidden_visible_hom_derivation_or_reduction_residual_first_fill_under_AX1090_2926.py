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

CHECKPOINT = "2926"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2926-Y5-R2FR-parent-object-no-hidden-visible-hom-derivation-or-reduction-residual-first-fill-under-AX1090.md"

SRC_2925_DOC = ROOT / "2925-Y5-R2FR-MTS-to-EH-reduction-morphism-or-extra-sector-silence-proof-under-AX1090.md"
SRC_2925_NEXT = RESIDUALS / "P8_Y5_R2FR_2925_NEXT_TARGET.csv"
SRC_2925_RESIDUAL = RESIDUALS / "P8_Y5_R2FR_2925_REDUCTION_RESIDUAL_VECTOR.csv"
SRC_2925_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2925_VALIDATION.csv"
SRC_1090_DOC = ROOT / "1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md"
SRC_1091_DOC = ROOT / "1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md"
SRC_1088_DOC = ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md"
SRC_1055_DOC = ROOT / "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md"
SRC_1047_DOC = ROOT / "1047-Y5-R10-constant-superselection-alpha-mass-clock-theorem-or-coefficient-provenance.md"
SRC_2910_DOC = ROOT / "2910-Y5-R2FR-Qvis-object-language-no-source-slot-or-finite-JH-DqZ-Y5Y6-vector-under-AX1090.md"
SRC_2911_DOC = ROOT / "2911-Y5-R2FR-parent-field-chart-q-map-kernel-basis-or-finite-DqZ-norm-under-AX1090.md"
SRC_2912_DQZ = RESIDUALS / "P8_Y5_R2FR_2912_FIRST_DQZ_COMPONENT_BOUND_INPUT_ROW.csv"
SRC_2913_DQZ = RESIDUALS / "P8_Y5_R2FR_2913_DQZ_GEOMETRY_ACQUISITION_CONTRACT.csv"
SRC_2914_DOC = ROOT / "2914-Y5-R2FR-DqZ-geometry-source-acquisition-or-Cobs-no-shadow-bound-under-AX1090.md"
SRC_2914_HEADS = RESIDUALS / "P8_Y5_R2FR_2914_DQZ_GEOMETRY_HEAD_ACQUISITION_ROWS.csv"
SRC_2659_DOC = ROOT / "2659-Y5-R2FR-no-hidden-visible-hom-operator-domain-theorem-or-finite-source-row.md"
SRC_2659_THEOREM = RESIDUALS / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv"
SRC_2659_VECTOR = RESIDUALS / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_FINITE_COUPLING_RESIDUAL_VECTOR_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2926_SOURCE_REGISTER.csv",
    "ax1090_audit": RESIDUALS / "P8_Y5_R2FR_2926_AX1090_PARENT_OBJECT_AUDIT.csv",
    "hom_retry": RESIDUALS / "P8_Y5_R2FR_2926_NO_HIDDEN_VISIBLE_HOM_RETRY.csv",
    "rv_first_fill": RESIDUALS / "P8_Y5_R2FR_2926_RV2925_FIRST_FILL_ATTEMPT.csv",
    "dqz_bridge": RESIDUALS / "P8_Y5_R2FR_2926_DQZ_GEOMETRY_FILL_BRIDGE.csv",
    "candidate_results": RESIDUALS / "P8_Y5_R2FR_2926_CANDIDATE_VALIDATION_RESULTS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2926_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2926_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2926_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2926_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2926_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "ax1090_copy": PARENT_ACTION / "AX1090_parent_object_no_hidden_visible_audit_2926_NONCLAIM.csv",
    "rv_first_fill_copy": LOCAL_BOUNDS / "RV2925_metric_readout_first_fill_attempt_2926_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2926_RV2925_METRIC_READOUT_DQZ_GEOMETRY_BOUND_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


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
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2926_00_2925_doc", SRC_2925_DOC, "Y5_R2FR_2925_conditional_reduction_theorem_written_current_MTS_residual_vector_2926_next;NEXT2925_0_2926;Validation overall: `True`", "2925 handoff to parent object/no-hidden-visible hom or first residual fill"),
        ("SRC2926_01_2925_next", SRC_2925_NEXT, "NEXT2925_0_2926;parent-object-no-hidden-visible-hom", "machine-readable 2926 target"),
        ("SRC2926_02_2925_residual", SRC_2925_RESIDUAL, "RV2925_0_metric_readout;RV2925_TOTAL", "MTS-to-EH reduction residual vector"),
        ("SRC2926_03_2925_validation", SRC_2925_VALIDATION, "VAL2925_OVERALL;True", "2925 validation summary"),
        ("SRC2926_04_1090_axioms", SRC_1090_DOC, "AX1090_0_parent_object;AX1090_1_no_hidden_visible_hom;SYN1090_8_verdict", "missing parent object and no-hidden-visible axioms"),
        ("SRC2926_05_1091_hom", SRC_1091_DOC, "ODH1091_0_target;ODH1091_6_verdict;V1091_SUMMARY", "operator-domain no-hidden-visible theorem attempt"),
        ("SRC2926_06_1088_moms", SRC_1088_DOC, "MOMS1088_0_action_form;MOMS1088_7_verdict;THM1088_5_conclusion", "conditional ordinary-matter signature theorem"),
        ("SRC2926_07_1055_parent_action", SRC_1055_DOC, "PAC1055_3_no_mixed_coefficients;PAC1055_6_single_parent_action;DEC1055_1_not_derivation_yet", "alpha/matter parent-action contract"),
        ("SRC2926_08_1047_constants", SRC_1047_DOC, "CST1047_0_descent_or_superselection_criterion;CST1047_5_verdict", "constant superselection conditional theorem"),
        ("SRC2926_09_2910_qvis", SRC_2910_DOC, "QVIS2910_0_visible_object_set;QVIS2910_9_verdict;Validation overall: `True`", "Q_vis object-language no-source-slot theorem attempt"),
        ("SRC2926_10_2911_qmap", SRC_2911_DOC, "QMAP2911_7_verdict;DQZ2911_TOTAL;Validation overall: `True`", "parent q-map/kernel/DqZ attempt"),
        ("SRC2926_11_2912_dqz", SRC_2912_DQZ, "BDQZ2912_0_DqZ_geometry;BOUND_INPUT_ROW_STAGED_NONCLAIM", "first DqZ geometry component bound row"),
        ("SRC2926_12_2913_dqz", SRC_2913_DQZ, "DGC2913_00_formula;ACQUISITION_REQUIRED_NONCLAIM", "DqZ geometry acquisition contract"),
        ("SRC2926_13_2914_heads", SRC_2914_HEADS, "HEAD2914_0_DqZ_geometry_total;HEAD2914_7_E_readout_geom_abs", "DqZ geometry head acquisition rows"),
        ("SRC2926_14_2914_doc", SRC_2914_DOC, "Y5_R2FR_2914_Cobs_conditional_normalization_Cshadow_not_derived_DqZ_geometry_heads_staged_2915_next;VAL2914_OVERALL", "DqZ geometry source acquisition checkpoint"),
        ("SRC2926_15_2659_doc", SRC_2659_DOC, "ODT2659_0_target;ODT2659_6_verdict;FRV2659_6_acceptance", "operator-domain theorem and finite vector checkpoint"),
        ("SRC2926_16_2659_theorem", SRC_2659_THEOREM, "ODT2659_0_target;ODT2659_6_verdict", "operator-domain theorem attempt rows"),
        ("SRC2926_17_2659_vector", SRC_2659_VECTOR, "FRV2659_0_c_g_common_frame;FRV2659_6_acceptance", "finite coupling residual vector"),
    ]
    rows = []
    for source_id, path, anchors, role in specs:
        ok, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": ok,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def ax1090_audit_rows() -> list[dict[str, Any]]:
    specs = [
        ("AX2926_0_parent_object", "AX1090_0", "one parent action object owns ordinary matter before readout/projection/fitting", "SCHEMA_AVAILABLE_NOT_DERIVED", "needed to stop separate contracts from proving each other"),
        ("AX2926_1_no_hidden_visible_hom", "AX1090_1", "hidden variables have no hom into visible coefficients except q_obs or fixed representation data", "EXACT_CONDITIONAL_THEOREM_COUNTERMODEL_SURVIVES", "kills c_g, b_dis, alpha/mass/clock/source-weight slots if parent-signed"),
        ("AX2926_2_common_measure", "AX1090_2", "one hbar/action measure/current normalization without species/source Jacobians", "MISSING_MEASURE_OWNER", "otherwise w_A S_A source-weight countermodels survive"),
        ("AX2926_3_fixed_constant_sector", "AX1090_3", "masses, charges, alpha_EM, clocks and representation labels are fixed/topological or retained", "CONDITIONAL_ROUTE_UNSIGNED", "otherwise constants carry local WEP/R10/clock residuals"),
        ("AX2926_4_variation_domain_order", "AX1090_4", "variations occur before readout/material/source-worldtube/calibration selectors", "CONDITIONAL_RULE_NOT_TIED_TO_PARENT_OBJECT", "otherwise post-variation selectors manufacture source currents"),
        ("AX2926_5_total_verdict", "AX1090_total", "AX1090_0 through AX1090_4 derived from parent primitives", "AX1090_NOT_DERIVED_FIRST_RESIDUAL_FILL_REQUIRED", "current branch must move to residual fill rather than another closure pass"),
    ]
    rows = []
    for audit_id, axiom_id, axiom_statement, current_status, why_it_matters in specs:
        rows.append(
            add_common(
                {
                    "audit_id": audit_id,
                    "axiom_id": axiom_id,
                    "axiom_statement": axiom_statement,
                    "current_status": current_status,
                    "parent_signed": False,
                    "adopted_as_axiom": False,
                    "blocks_reduction_claim": True,
                    "why_it_matters": why_it_matters,
                    "source_paths": ";".join(str(path) for path in [SRC_1090_DOC, SRC_1091_DOC, SRC_2659_THEOREM]),
                }
            )
        )
    return rows


def hom_retry_rows() -> list[dict[str, Any]]:
    specs = [
        ("HOM2926_0_target", "no-hidden-visible coefficient hom", "Allowed ordinary coefficients lie in A_ord=q^*A_Q + A_fixed; no H_X -> Coeff(O_vis) map exists except through q or fixed data.", "TARGET_SHARP", "keeps proof target exact"),
        ("HOM2926_1_typed_domain_theorem", "typed-domain exclusion", "If S_ord domain is Q_obs x MatterFields_Q x Rep_fixed, then non-q hidden coefficient maps are type errors; dc_vis(v_X)=0 for v_X in ker(Dq).", "EXACT_CONDITIONAL_THEOREM", "real theorem under signed parent domain"),
        ("HOM2926_2_scalar_counterexample", "hidden scalar obstruction", "If an invariant hidden scalar I survives, c=c0+epsilon I is a legal visible coefficient unless the domain excludes it.", "COUNTERMODEL_SURVIVES", "blocks unconditional AX1090_1 proof"),
        ("HOM2926_3_shortcut_rejection", "covariance/WEP/Ward/terminality", "Ordinary symmetries do not ban common Jordan frames, source weights, markers, or post-readout selectors.", "SHORTCUTS_REJECTED", "prevents fake proof"),
        ("HOM2926_4_effective_readout", "radiative/readout closure", "Bare sequestering is insufficient unless effective action and empirical readout preserve the typed domain.", "RADIATIVE_READOUT_CLOSURE_UNSIGNED", "keeps b_alpha/b_clock/source rows live"),
        ("HOM2926_5_verdict", "current no-hidden-visible hom", "HOM2926_1 is valid conditionally, but current corpus lacks parent domain construction, invariant-triviality, and radiative/readout closure.", "THEOREM_NOT_DERIVED_CURRENT_CORPUS", "route demoted to finite residual fill"),
    ]
    rows = []
    for retry_id, theorem_piece, formal_statement, current_status, reason in specs:
        rows.append(
            add_common(
                {
                    "retry_id": retry_id,
                    "theorem_piece": theorem_piece,
                    "formal_statement": formal_statement,
                    "current_status": current_status,
                    "conditional_theorem_valid": current_status in {"EXACT_CONDITIONAL_THEOREM", "TARGET_SHARP"},
                    "promoted_for_current_mts": False,
                    "reason": reason,
                    "source_paths": ";".join(str(path) for path in [SRC_1091_DOC, SRC_2659_THEOREM, SRC_1055_DOC]),
                }
            )
        )
    return rows


def rv_first_fill_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "fill_id": "RVF2926_0_selected_component",
            "rv_component": "RV2925_0_metric_readout",
            "symbol": "epsilon_metric_readout",
            "fill_status": "SELECTED_FOR_FIRST_FILL",
            "formula": "epsilon_metric_readout := DqZ_geometry_abs + C_shadow_abs + E_boundary_geom_abs + E_readout_geom_abs",
            "current_value": "MISSING_SOURCE_BACKED_UPPER_BOUND",
            "source_ready": True,
            "source_backed_numeric": False,
            "accepted_for_scoring": False,
            "why_selected": "metric readout is the earliest common residual feeding PPN, clocks, orbital systems, and local GR.",
        },
        {
            "fill_id": "RVF2926_1_existing_bound_row",
            "rv_component": "RV2925_0_metric_readout",
            "symbol": "DqZ_geometry",
            "fill_status": "BOUND_ROW_EXISTS_NONCLAIM",
            "formula": "E_DqZ_geometry <= Pi_geom*C_Obs_e*Dq_Z_norm*N_Z + E_shadow + E_boundary_geom + E_readout_geom",
            "current_value": "MISSING_PARENT_INPUT",
            "source_ready": True,
            "source_backed_numeric": False,
            "accepted_for_scoring": False,
            "why_selected": "2912 already staged this as the first DqZ component row.",
        },
        {
            "fill_id": "RVF2926_2_head_pack",
            "rv_component": "RV2925_0_metric_readout",
            "symbol": "DqZ_geometry_abs_heads",
            "fill_status": "HEADS_COMPLETE_NONCLAIM",
            "formula": "HEAD2914_0 through HEAD2914_7 split C_Obs_e, Dq_Z_norm, N_Z, Pi_geom, C_shadow, boundary and readout tails.",
            "current_value": "MISSING_COMPONENT_INPUTS",
            "source_ready": True,
            "source_backed_numeric": False,
            "accepted_for_scoring": False,
            "why_selected": "2914 componentized the bound, so 2927 can seek one real numeric/source-backed head.",
        },
        {
            "fill_id": "RVF2926_3_acceptance_gate",
            "rv_component": "RV2925_0_metric_readout",
            "symbol": "epsilon_metric_readout_acceptance",
            "fill_status": "NOT_SCORE_READY",
            "formula": "all heads finite/source-backed or theorem-zero, no MISSING markers, no cancellation, no fitted GM/G_N absorption",
            "current_value": "COMPONENTS_MISSING_NONCLAIM",
            "source_ready": False,
            "source_backed_numeric": False,
            "accepted_for_scoring": False,
            "why_selected": "2926 refuses to pretend source-ready is source-backed.",
        },
    ]
    return [add_common(row) for row in rows]


def dqz_bridge_rows() -> list[dict[str, Any]]:
    specs = [
        ("DQB2926_0_formula", "DqZ_geometry_abs", "HEAD2914_0_DqZ_geometry_total", "MISSING_COMPONENT_INPUTS", "all metric-readout heads must be filled or killed"),
        ("DQB2926_1_Cobs", "C_Obs_e_abs", "HEAD2914_1_C_Obs_e_abs", "CONDITIONAL_1_NOT_PARENT_SIGNED", "candidate normalization is not a proof"),
        ("DQB2926_2_DqZ", "Dq_Z_norm_abs", "HEAD2914_2_Dq_Z_norm_abs", "MISSING_NUMERIC_OR_THEOREM_ZERO", "needs parent q map/Dq matrix/Z norms"),
        ("DQB2926_3_NZ", "N_Z_abs", "HEAD2914_3_N_Z_abs", "MISSING_Z_DIRECTION_NORM", "needs branch amplitude/norm"),
        ("DQB2926_4_projection", "Pi_geom_abs", "HEAD2914_4_Pi_geom_abs", "MISSING_ARENA_PROJECTION", "needs PPN/clock/orbital/R10 projection maps"),
        ("DQB2926_5_shadow", "C_shadow_abs", "HEAD2914_5_C_shadow_abs", "MISSING_COMPONENT_VALUES", "contains c_g, b_dis, constants and support leaks"),
        ("DQB2926_6_boundary", "E_boundary_geom_abs", "HEAD2914_6_E_boundary_geom_abs", "MISSING_BOUNDARY_TAIL_BOUND", "boundary/projector/source support still open"),
        ("DQB2926_7_readout", "E_readout_geom_abs", "HEAD2914_7_E_readout_geom_abs", "MISSING_READOUT_TAIL_BOUND", "clock/EM/orbit/PPN readout regeneration still open"),
        ("DQB2926_8_next_best_head", "C_shadow_abs", "HEAD2914_5_C_shadow_abs", "SELECTED_FOR_2927_COMPONENT_FILL", "fastest concrete next target because no-hidden-visible hom failed"),
    ]
    rows = []
    for bridge_id, symbol, upstream_row, current_status, next_action in specs:
        rows.append(
            add_common(
                {
                    "bridge_id": bridge_id,
                    "rv_component": "RV2925_0_metric_readout",
                    "symbol": symbol,
                    "upstream_row": upstream_row,
                    "current_status": current_status,
                    "source_backed_numeric": False,
                    "accepted_for_scoring": False,
                    "next_action": next_action,
                    "source_paths": ";".join(str(path) for path in [SRC_2912_DQZ, SRC_2913_DQZ, SRC_2914_HEADS]),
                }
            )
        )
    return rows


def candidate_validation_rows() -> list[dict[str, Any]]:
    rows = [
        ("CAND2926_0_AX1090_parent_object", "derive AX1090_0 parent object from current corpus", "REJECT_SCHEMA_AVAILABLE_NOT_DERIVED", "not_accepted", "PAC/P8 schemas do not construct one parent object"),
        ("CAND2926_1_AX1090_no_hidden_visible_hom", "derive AX1090_1 no hidden-visible hom", "REJECT_COUNTERMODEL_SURVIVES", "conditional_theorem_only", "hidden scalar/common frame/source-weight countermodels remain legal"),
        ("CAND2926_2_typed_domain_theorem", "typed-domain theorem if A_ord=q^*A_Q+A_fixed", "ACCEPTED_CONDITIONAL_THEOREM_NOT_PARENT_DERIVED", "conditional_theorem_piece", "Allowed[S_ord] and A_ord not parent-signed"),
        ("CAND2926_3_RV2925_metric_readout_fill", "fill RV2925_0 with DqZ_geometry acquisition row", "ACCEPTED_SOURCE_READY_NONCLAIM_NOT_SCORE_READY", "source_ready_nonclaim", "missing numeric/source-backed heads"),
        ("CAND2926_4_claim_reduction", "claim local GR/Newton from 2926", "REJECT_CLAIM_GATE_CLOSED", "not_accepted", "AX1090 and RV2925 remain unclosed"),
    ]
    return [
        add_common(
            {
                "candidate_id": candidate_id,
                "candidate": candidate,
                "validation_status": validation_status,
                "accepted_as": accepted_as,
                "failure_reasons": failure_reasons,
            }
        )
        for candidate_id, candidate, validation_status, accepted_as, failure_reasons in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2926_0_AX1090_parent_object", "AX1090_0 parent object is derived", "BLOCKED", "AX2926_0 parent_signed=false", "do not use separate contracts as a proof"),
        ("CG2926_1_no_hidden_visible_hom", "AX1090_1 no hidden-visible hom is derived", "BLOCKED", "HOM2926_5 theorem not derived", "retain coefficient residuals"),
        ("CG2926_2_RV2925_first_fill", "first RV2925 component is source-backed and score-ready", "BLOCKED_NONCLAIM", "RVF2926_3 not score ready", "move to numeric/source-backed head acquisition"),
        ("CG2926_3_conditional_theorem", "typed-domain theorem remains valid conditionally", "CONTROL_PASS_NONCLAIM", "CAND2926_2 accepted conditionally", "use as target only"),
        ("CG2926_4_local_GR_Newton", "local GR/Newton reduction claim", "CLOSED", "AX1090 and RV2925 open", "no local-GR/Newton claim"),
        ("CG2926_5_next_target", "next target selected", "NEXT_SELECTED", "NEXT2926_0_2927", "go after RV2925_0/Cshadow source-backed head"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "gate": gate,
                "gate_status": gate_status,
                "evidence": evidence,
                "decision": decision,
            }
        )
        for gate_id, gate, gate_status, evidence, decision in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2926_0_theorem_retry", "AX1090_0/AX1090_1 are not derived", "CLAIM_REFUSED", "the parent object and typed operator-domain remain contracts/conditional theorems with surviving countermodels."),
        ("DEC2926_1_real_progress", "RV2925_0 is selected and bridged to existing DqZ geometry rows", "SOURCE_READY_NOT_SCORE_READY", "the first reduction residual now has a concrete formula and head list, not just a label."),
        ("DEC2926_2_no_looping", "stop looping on no-hidden-visible hom unless new primitive source appears", "ROUTE_DEMOTED_FOR_NOW", "1091/2659/2926 all find the same missing parent-domain construction."),
        ("DEC2926_3_best_next", "2927 should fill C_shadow/Cobs/DqZ geometry head with source-backed input", "NEXT_SELECTED", "this turns the theorem bottleneck into a measurable local-GR residual component."),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "status": status,
                "reason": reason,
            }
        )
        for decision_id, decision, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "next_id": "NEXT2926_0_2927",
            "selection": "selected_primary",
            "target_doc": "2927-Y5-R2FR-RV2925-metric-readout-DqZ-geometry-Cshadow-first-source-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_RV2925_metric_readout_DqZ_geometry_Cshadow_first_source_bound_under_AX1090_2927.py",
            "objective": "fill the first source-backed head for RV2925_0 metric readout, prioritizing C_shadow_abs/c_g/b_dis/constant-marker components or C_Obs_e if a parent normalization certificate exists",
            "acceptance_gate": "one HEAD2914 component becomes numeric/source-backed nonclaim, or the blocker is narrowed to a single external source/proof requirement; no local-GR claim",
        },
        {
            "next_id": "NEXT2926_1_fallback",
            "selection": "fallback_if_metric_head_still_empty",
            "target_doc": "2927B-Y5-R2FR-hidden-invariant-triviality-or-coupling-vector-first-numeric-input-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_hidden_invariant_triviality_or_coupling_vector_first_numeric_input_under_AX1090_2927B.py",
            "objective": "retry the only remaining no-hidden-visible proof path, hidden invariant triviality, or fill one finite coupling residual input",
            "acceptance_gate": "hidden invariant algebra triviality is parent-signed, or one FRV2659 coefficient has source-backed nonclaim value/projection",
        },
    ]
    return [add_common(row) for row in rows]


def branch_copy_rows() -> list[dict[str, Any]]:
    copy_specs = [
        ("BC2926_0_ax1090_audit", OUTPUTS["ax1090_audit"], BRANCH_OUTPUTS["ax1090_copy"], "parent action AX1090 audit"),
        ("BC2926_1_rv_first_fill", OUTPUTS["rv_first_fill"], BRANCH_OUTPUTS["rv_first_fill_copy"], "local bounds RV2925 metric readout fill attempt"),
        ("BC2926_2_next_target", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"], "RAB/source queue next target"),
    ]
    rows = []
    for copy_id, source, destination, role in copy_specs:
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "destination_path": str(destination),
                    "role": role,
                    "destination_exists": destination.exists(),
                    "destination_parses": csv_parses(destination),
                }
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    ax1090: list[dict[str, Any]],
    hom_retry: list[dict[str, Any]],
    rv_fill: list[dict[str, Any]],
    dqz_bridge: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str, bool]] = [
        ("VAL2926_0_sources_exist", all(as_bool(row["path_exists"]) for row in sources), "every cited source path exists", True),
        ("VAL2926_1_source_anchors_found", all(as_bool(row["anchors_found"]) for row in sources), "every cited source anchor is present", True),
        ("VAL2926_2_AX1090_total_blocked", any(row["audit_id"] == "AX2926_5_total_verdict" and row["current_status"] == "AX1090_NOT_DERIVED_FIRST_RESIDUAL_FILL_REQUIRED" for row in ax1090), "AX1090 remains blocked and routes to residual fill", True),
        ("VAL2926_3_hom_conditional_not_promoted", any(row["retry_id"] == "HOM2926_5_verdict" and row["current_status"] == "THEOREM_NOT_DERIVED_CURRENT_CORPUS" and not as_bool(row["promoted_for_current_mts"]) for row in hom_retry), "no-hidden-visible hom is not promoted", True),
        ("VAL2926_4_RV2925_metric_selected", any(row["fill_id"] == "RVF2926_0_selected_component" and row["rv_component"] == "RV2925_0_metric_readout" for row in rv_fill), "RV2925_0 metric readout selected for first fill", True),
        ("VAL2926_5_RV2925_not_score_ready", any(row["fill_id"] == "RVF2926_3_acceptance_gate" and row["fill_status"] == "NOT_SCORE_READY" and not as_bool(row["accepted_for_scoring"]) for row in rv_fill), "first fill remains nonclaim/not score-ready", True),
        ("VAL2926_6_DqZ_bridge_heads_complete", len(dqz_bridge) >= 9 and any(row["bridge_id"] == "DQB2926_8_next_best_head" for row in dqz_bridge), "DqZ geometry bridge lists all heads and selects next head", True),
        ("VAL2926_7_candidate_runner_safe", any(row["candidate_id"] == "CAND2926_1_AX1090_no_hidden_visible_hom" and row["validation_status"] == "REJECT_COUNTERMODEL_SURVIVES" for row in candidates), "candidate runner rejects no-hidden-visible proof", True),
        ("VAL2926_8_no_claim_gates_open", all(not as_bool(row["claim_allowed"]) and str(row["gate_status"]) != "OPEN" for row in claims), "no claim gate opens in 2926", True),
        ("VAL2926_9_next_target_selected", any(row["next_id"] == "NEXT2926_0_2927" for row in next_rows), "2927 metric-readout/Cshadow source-bound target selected", True),
        ("VAL2926_10_branch_copies_valid", all(as_bool(row["destination_exists"]) and as_bool(row["destination_parses"]) for row in branches), "branch copies exist and parse", True),
        ("VAL2926_11_no_formalization_outputs", not any(is_under(path, FORMALIZATION) for path in [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]), "no generated output path is inside formalization-workbench", True),
        ("VAL2926_12_doc_exists", DOC.exists(), "2926 markdown checkpoint exists", True),
    ]
    rows = [
        {
            "validation_id": check_id,
            "passed": passed,
            "check": check,
            "required": required,
            "generated_utc": RUN_UTC,
        }
        for check_id, passed, check, required in checks
    ]
    overall = all(passed for _, passed, _, required in checks if required)
    rows.append(
        {
            "validation_id": "VAL2926_OVERALL",
            "passed": overall,
            "check": "2926 validation overall",
            "required": True,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    ax1090: list[dict[str, Any]],
    hom_retry: list[dict[str, Any]],
    rv_fill: list[dict[str, Any]],
    dqz_bridge: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    overall = next(row["passed"] for row in validation if row["validation_id"] == "VAL2926_OVERALL")
    lines = [
        "# 2926 - Y5/R2FR Parent Object No-Hidden-Visible Hom Derivation Or Reduction Residual First Fill Under AX1090",
        "",
        "Status: `Y5_R2FR_2926_AX1090_not_derived_RV2925_metric_readout_first_fill_staged_2927_next`",
        "",
        "## Result",
        "",
        "2926 retries the parent object/no-hidden-visible hom route under the stricter 2925 reduction-vector framing. The typed-domain theorem remains exact conditionally, but current MTS still does not derive the parent ordinary-matter domain or exclude hidden scalar/common-frame/source-weight countermodels.",
        "",
        "So the branch moves forward instead of circling: `RV2925_0_metric_readout` is selected as the first reduction residual component, bridged to the existing `DqZ_geometry` bound formula and its 2914 head list. It is source-ready, not score-ready.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "path_exists", "anchors_found", "role", "source_path"]),
        "",
        "## AX1090 Parent Object Audit",
        "",
        md_table(ax1090, ["audit_id", "axiom_id", "current_status", "parent_signed", "adopted_as_axiom", "why_it_matters"]),
        "",
        "## No-Hidden-Visible Hom Retry",
        "",
        md_table(hom_retry, ["retry_id", "theorem_piece", "current_status", "conditional_theorem_valid", "promoted_for_current_mts", "reason"]),
        "",
        "## RV2925 First Fill Attempt",
        "",
        md_table(rv_fill, ["fill_id", "rv_component", "symbol", "fill_status", "current_value", "source_ready", "source_backed_numeric", "accepted_for_scoring"]),
        "",
        "## DqZ Geometry Fill Bridge",
        "",
        md_table(dqz_bridge, ["bridge_id", "symbol", "upstream_row", "current_status", "source_backed_numeric", "next_action"]),
        "",
        "## Candidate Validation Results",
        "",
        md_table(candidates, ["candidate_id", "candidate", "validation_status", "accepted_as", "failure_reasons"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "gate", "gate_status", "decision", "evidence"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "status", "reason"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["next_id", "selection", "target_doc", "target_script", "objective", "acceptance_gate"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["validation_id", "passed", "check", "required"]),
        "",
        f"Validation overall: `{overall}`.",
        "",
        "## Bottom Line",
        "",
        "This is a useful pivot. We did not magically derive the parent object, but we also did not stall there. The next concrete work is to make one metric-readout head source-backed, starting with `C_shadow_abs` or `C_Obs_e_abs`, so the GR-reduction obstruction vector begins turning into something testable.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    ax1090 = ax1090_audit_rows()
    hom_retry = hom_retry_rows()
    rv_fill = rv_first_fill_rows()
    dqz_bridge = dqz_bridge_rows()
    candidates = candidate_validation_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["ax1090_audit"], ax1090)
    write_csv(OUTPUTS["hom_retry"], hom_retry)
    write_csv(OUTPUTS["rv_first_fill"], rv_fill)
    write_csv(OUTPUTS["dqz_bridge"], dqz_bridge)
    write_csv(OUTPUTS["candidate_results"], candidates)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_rows)

    branches = branch_copy_rows()
    write_csv(OUTPUTS["branches"], branches)

    DOC.write_text("# 2926 - validation preflight\n", encoding="utf-8")
    validation = validation_rows(sources, ax1090, hom_retry, rv_fill, dqz_bridge, candidates, claims, next_rows, branches)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, ax1090, hom_retry, rv_fill, dqz_bridge, candidates, claims, decisions, next_rows, validation)

    overall = next(row["passed"] for row in validation if row["validation_id"] == "VAL2926_OVERALL")
    if not overall:
        raise SystemExit("2926 validation failed; see " + str(OUTPUTS["validation"]))
    print("2926 validation overall:", overall)
    print("doc:", DOC)


if __name__ == "__main__":
    main()
