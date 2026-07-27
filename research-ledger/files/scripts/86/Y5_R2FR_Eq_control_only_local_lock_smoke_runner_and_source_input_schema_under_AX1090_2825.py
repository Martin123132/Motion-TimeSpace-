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
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2825-Y5-R2FR-Eq-control-only-local-lock-smoke-runner-and-source-input-schema-under-AX1090.md"

SRC_2824_NEXT = RESIDUALS / "P8_Y5_R2FR_2824_NEXT_TARGET.csv"
SRC_2824_DECISION = RESIDUALS / "P8_Y5_R2FR_2824_DECISION_LEDGER.csv"
SRC_2824_DEMOTION = RESIDUALS / "P8_Y5_R2FR_2824_EQ_CONTROL_ONLY_DEMOTION_LEDGER.csv"
SRC_2824_RUNNER = RESIDUALS / "P8_Y5_R2FR_2824_CONTROL_ONLY_LOCAL_LOCK_RUNNER_CONTRACT.csv"
SRC_2824_EXTRACTION = RESIDUALS / "P8_Y5_R2FR_2824_COVARIANCE_HESSIAN_SOURCE_EXTRACTION_STATUS.csv"
SRC_2824_GATES = RESIDUALS / "P8_Y5_R2FR_2824_CLAIM_GATES.csv"
SRC_2823_CONDITIONAL = RESIDUALS / "P8_Y5_R2FR_2823_COVARIANCE_HESSIAN_CONDITIONAL_EQ_ROW.csv"
SRC_2823_IMPACT = RESIDUALS / "P8_Y5_R2FR_2823_COMPONENT_ROW_REENTRY_IMPACT.csv"
SRC_2823_UNITS = RESIDUALS / "P8_Y5_R2FR_2823_Q_NORMALIZATION_AND_DUAL_UNITS_GATE.csv"
SRC_2822_JQ_FIRST = RESIDUALS / "P8_Y5_R2FR_2822_FIRST_SAME_NORM_JQ_COMPONENT_ROW.csv"
SRC_2822_JQ_FALLBACK = RESIDUALS / "P8_Y5_R2FR_2822_COMPONENT_BOUND_FALLBACK_VECTOR.csv"
SRC_2818_AMPLITUDE = RESIDUALS / "P8_Y5_R2FR_2818_LOCAL_LOCK_AMPLITUDE_LAW.csv"
SRC_2818_CHAIN = RESIDUALS / "P8_Y5_R2FR_2818_CHAIN_BOUND_UPDATE_WITH_NLOCK.csv"
SRC_2818_INTERFACE = RESIDUALS / "P8_Y5_R2FR_2818_FIRST_NLOCK_INPUT_INTERFACE.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2825_SOURCE_REGISTER.csv",
    "schema": RESIDUALS / "P8_Y5_R2FR_2825_CONTROL_INPUT_SCHEMA.csv",
    "placeholders": RESIDUALS / "P8_Y5_R2FR_2825_PLACEHOLDER_INPUT_ROWS_NONCLAIM.csv",
    "formulas": RESIDUALS / "P8_Y5_R2FR_2825_LOCAL_LOCK_CONTROL_FORMULAS.csv",
    "dryrun": RESIDUALS / "P8_Y5_R2FR_2825_DRYRUN_RESULTS_NONCLAIM.csv",
    "promotion": RESIDUALS / "P8_Y5_R2FR_2825_PROMOTION_REQUIREMENTS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2825_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2825_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2825_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2825_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2825_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "schema_copy": SOURCE_WEIGHT / "Eq_control_only_local_lock_smoke_inputs_2825_NONCLAIM.csv",
    "dryrun_copy": LOCAL_BOUNDS / "Eq_control_only_local_lock_smoke_results_2825_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2825_CONTROL_RUNNER_PROMOTION_INPUT_PRIORITY_NEXT.csv",
}

BRANCH_ID = "MTS_R2FR_EQ_CONTROL_ONLY_LOCAL_LOCK_SMOKE_2825"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    paths = {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def csv_parses(path: Path) -> bool:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    row["generated_utc"] = ts()
    return row


def source_row(source_id: str, path: Path, anchors: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    anchor_list = [anchor for anchor in anchors.split(";") if anchor]
    missing = [anchor for anchor in anchor_list if anchor not in text]
    return nonclaim(
        {
            "source_id": source_id,
            "source_path": str(path),
            "anchors": anchors,
            "role": role,
            "path_exists": path.exists(),
            "anchors_found": not missing,
            "missing_anchors": ";".join(missing),
        }
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2825_0_2824_next", SRC_2824_NEXT, "NEXT2824_0_2825", "2824 handoff selecting the control-only local-lock smoke runner"),
        ("SRC2825_1_2824_decision", SRC_2824_DECISION, "DEC2824_2_demotion;DEC2824_3_next", "E_q demotion and control-runner decision"),
        ("SRC2825_2_2824_demotion", SRC_2824_DEMOTION, "DEM2824_0_control_carrier;DEM2824_2_no_Nlock", "control-only carrier and no local-lock reentry"),
        ("SRC2825_3_2824_runner", SRC_2824_RUNNER, "RUN2824_0_inputs;RUN2824_4_acceptance", "runner contract and promotion acceptance rule"),
        ("SRC2825_4_2824_extraction", SRC_2824_EXTRACTION, "EXT2824_2_HAB;EXT2824_9_verdict", "missing source-backed H_AB and final no-extraction verdict"),
        ("SRC2825_5_2824_gates", SRC_2824_GATES, "CG2824_6_control_demotion;CG2824_7_local_claim", "nonclaim demotion and local claim block"),
        ("SRC2825_6_2823_conditional", SRC_2823_CONDITIONAL, "CCR2823_1_Mq2;CCR2823_4_Eq_form", "conditional covariance-Hessian E_q carrier"),
        ("SRC2825_7_2823_impact", SRC_2823_IMPACT, "RI2823_4_Nlock;RI2823_5_claims", "component row reentry remains blocked"),
        ("SRC2825_8_2823_units", SRC_2823_UNITS, "QNG2823_2_Eq_units;QNG2823_6_Newton_source", "q units and Newton-source normalization debt"),
        ("SRC2825_9_2822_jq_first", SRC_2822_JQ_FIRST, "JQC2822_0_j_matter_first_row", "first same-norm J_q component row"),
        ("SRC2825_10_2822_jq_fallback", SRC_2822_JQ_FALLBACK, "FB2822_0_total", "component fallback vector for source norm"),
        ("SRC2825_11_2818_amplitude", SRC_2818_AMPLITUDE, "ALA2818_1_Nlock;ALA2818_4_chain_insert", "local-lock amplitude law and K_alg chain insert"),
        ("SRC2825_12_2818_chain", SRC_2818_CHAIN, "CBU2818_1_finite_route;CBU2818_3_qnorm_status", "N_lock chain update and q-norm blocker"),
        ("SRC2825_13_2818_interface", SRC_2818_INTERFACE, "FPI2818_0_Nsrc;FPI2818_2_Npair", "first N_lock input interface"),
    ]
    return [source_row(*spec) for spec in specs]


def schema_rows() -> list[dict[str, Any]]:
    specs = [
        ("SCH2825_0_HAB", "carrier", "H_AB_shape", "parent covariance Hessian shape", "source-backed effective action Hessian, q-lift, units, background, density convention", "MISSING_SOURCE_BACKED_H_AB", SRC_2824_EXTRACTION, "EXT2824_2_HAB"),
        ("SCH2825_1_Mq2", "carrier", "M_q^2", "conditional projected mass", "M_q^2=n_q^A H_AB n_q^B in one parent normalization", "MISSING_SOURCE_BACKED_Mq2", SRC_2823_CONDITIONAL, "CCR2823_1_Mq2"),
        ("SCH2825_2_Zq", "carrier", "Z_q", "conditional projected stiffness", "Z_q=xi_q^2 M_q^2 with sourced xi_q", "MISSING_SOURCE_BACKED_Zq", SRC_2823_CONDITIONAL, "CCR2823_2_Zq"),
        ("SCH2825_3_xiq", "carrier", "xi_q", "smoothing/correlation scale", "source-backed numeric or theorem-fixed scale", "MISSING_SOURCE_BACKED_XI_Q", SRC_2824_EXTRACTION, "EXT2824_4_xiq"),
        ("SCH2825_4_lambda", "carrier", "lambda_q", "conditional range", "lambda_q=sqrt(Z_q/M_q^2)=xi_q after source promotion", "MISSING_SOURCE_BACKED_LAMBDA_Q", SRC_2823_CONDITIONAL, "CCR2823_3_lambda"),
        ("SCH2825_5_qunits", "normalization", "q_units_flag", "dimension/normalization of q", "same q normalization across E_q, J_q, Dq[v_m], and arenas", "MISSING_Q_UNITS_NORMALIZATION", SRC_2823_UNITS, "QNG2823_2_Eq_units"),
        ("SCH2825_6_selector", "normalization", "selector_flag", "q=0 local branch selector", "parent-signed selector or theorem-zero condition", "MISSING_PARENT_SELECTOR", SRC_2824_EXTRACTION, "EXT2824_6_selector"),
        ("SCH2825_7_boundary", "normalization", "boundary_flag", "domain and boundary class", "parent-signed boundary/domain certificate", "MISSING_BOUNDARY_DOMAIN_CERTIFICATE", SRC_2824_EXTRACTION, "EXT2824_7_boundary"),
        ("SCH2825_8_jmatter", "source_vector", "B_matter^q", "matter J_q component bound", "same E_q dual norm and source-backed or theorem-zero component", "MISSING_JQ_MATTER_COMPONENT", SRC_2822_JQ_FIRST, "JQC2822_0_j_matter_first_row"),
        ("SCH2825_9_jconst", "source_vector", "B_const^q", "constant sector J_q component bound", "same E_q dual norm and source-backed or theorem-zero component", "MISSING_JQ_CONST_COMPONENT", SRC_2822_JQ_FALLBACK, "FB2822_0_total"),
        ("SCH2825_10_jweight", "source_vector", "B_weight^q", "source-weight J_q component bound", "same E_q dual norm and source-backed or theorem-zero component", "MISSING_JQ_WEIGHT_COMPONENT", SRC_2822_JQ_FALLBACK, "FB2822_0_total"),
        ("SCH2825_11_jshadow", "source_vector", "B_shadow^q", "shadow/hidden-sector J_q component bound", "same E_q dual norm and source-backed or theorem-zero component", "MISSING_JQ_SHADOW_COMPONENT", SRC_2822_JQ_FALLBACK, "FB2822_0_total"),
        ("SCH2825_12_jreadout", "source_vector", "B_readout^q", "readout/projection J_q component bound", "same E_q dual norm and source-backed or theorem-zero component", "MISSING_JQ_READOUT_COMPONENT", SRC_2822_JQ_FALLBACK, "FB2822_0_total"),
        ("SCH2825_13_jboundary", "source_vector", "B_boundary^q", "boundary J_q component bound", "same E_q dual norm and source-backed or theorem-zero component", "MISSING_JQ_BOUNDARY_COMPONENT", SRC_2822_JQ_FALLBACK, "FB2822_0_total"),
        ("SCH2825_14_jcurvature", "source_vector", "B_curvature^q", "curvature J_q component bound", "same E_q dual norm and source-backed or theorem-zero component", "MISSING_JQ_CURVATURE_COMPONENT", SRC_2822_JQ_FALLBACK, "FB2822_0_total"),
        ("SCH2825_15_Btotal", "source_vector", "B_total^q", "total J_q source-vector bound", "sum_i B_i^q in one E_q dual norm", "MISSING_TOTAL_JQ_BOUND", SRC_2822_JQ_FALLBACK, "FB2822_0_total"),
        ("SCH2825_16_Cqm", "response", "C_qm", "q-to-m response constant", "parent-signed Dq[v_m] coupling and bounded inverse", "MISSING_C_QM_RESPONSE", SRC_2823_IMPACT, "RI2823_3_Cqm"),
        ("SCH2825_17_Dqvm", "response", "Dq[v_m]", "vertical generator coupling into q", "actual vertical generator, not a placeholder component", "MISSING_DQ_VERTICAL_GENERATOR", SRC_2823_IMPACT, "RI2823_4_Nlock"),
        ("SCH2825_18_UB", "local_lock", "U_B_max", "worldtube lifting/source-to-local constant", "sourced worldtube/profile normalization", "MISSING_WORLD_TUBE_CONSTANT", SRC_2818_INTERFACE, "FPI2818_0_Nsrc"),
        ("SCH2825_19_Cinner", "local_lock", "C_inner", "inner-charge conversion constant", "source-backed inner charge norm", "MISSING_INNER_CHARGE_CONSTANT", SRC_2818_INTERFACE, "FPI2818_2_Npair"),
        ("SCH2825_20_QmH", "local_lock", "Q_m^H", "inner horizontal charge", "source-backed charge or theorem-zero", "MISSING_HORIZONTAL_CHARGE", SRC_2818_INTERFACE, "FPI2818_2_Npair"),
        ("SCH2825_21_Ndomain", "local_lock", "N_inner_domain", "inner-domain leakage", "source-backed domain term or theorem-zero", "MISSING_DOMAIN_LEAKAGE", SRC_2818_INTERFACE, "FPI2818_2_Npair"),
        ("SCH2825_22_Nzero", "local_lock", "N_inner_zero_mode", "zero-mode leakage", "source-backed zero-mode term or theorem-zero", "MISSING_ZERO_MODE_LEAKAGE", SRC_2818_INTERFACE, "FPI2818_2_Npair"),
        ("SCH2825_23_Nrest", "local_lock", "N_rest", "rest-source leakage", "source-backed remainder bound", "MISSING_REST_LEAKAGE", SRC_2818_CHAIN, "CBU2818_1_finite_route"),
        ("SCH2825_24_Cemb", "local_lock", "C_emb", "energy-to-amplitude embedding constant", "source-backed embedding estimate", "MISSING_EMBEDDING_CONSTANT", SRC_2818_AMPLITUDE, "ALA2818_1_Nlock"),
        ("SCH2825_25_F2", "local_lock", "F2_bar", "second-order local transition coefficient", "parent-signed second derivative coefficient", "MISSING_F2_BAR", SRC_2818_AMPLITUDE, "ALA2818_4_chain_insert"),
        ("SCH2825_26_Lmin", "local_lock", "L_min", "minimum local transition length", "source-backed or derived local scale", "MISSING_L_MIN", SRC_2818_AMPLITUDE, "ALA2818_4_chain_insert"),
        ("SCH2825_27_Mm", "local_lock", "M_m_bar", "m amplitude envelope", "source-backed local matter envelope", "MISSING_M_M_BAR", SRC_2818_AMPLITUDE, "ALA2818_4_chain_insert"),
        ("SCH2825_28_ML", "local_lock", "M_L_bar", "transition-length envelope", "source-backed length-gradient envelope", "MISSING_M_L_BAR", SRC_2818_AMPLITUDE, "ALA2818_4_chain_insert"),
    ]
    rows: list[dict[str, Any]] = []
    for schema_id, group, name, role, promotion_requirement, token, source_path, anchor in specs:
        rows.append(
            nonclaim(
                {
                    "branch_id": BRANCH_ID,
                    "schema_id": schema_id,
                    "input_group": group,
                    "input_name": name,
                    "role": role,
                    "promotion_requirement": promotion_requirement,
                    "current_status": token,
                    "value_token": token,
                    "units_policy": "MUST_BE_SOURCE_BACKED_BEFORE_PROMOTION",
                    "source_path": str(source_path),
                    "source_anchor": anchor,
                    "anchor_found": anchor in read_text(source_path),
                    "source_backed": False,
                    "numeric_value_present": False,
                    "control_only": True,
                    "required_for_promotion": True,
                }
            )
        )
    return rows


def placeholder_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    placeholder_rows_out: list[dict[str, Any]] = []
    for row in rows:
        placeholder_rows_out.append(
            nonclaim(
                {
                    "placeholder_id": row["schema_id"].replace("SCH2825", "PH2825"),
                    "input_name": row["input_name"],
                    "input_group": row["input_group"],
                    "value_token": row["value_token"],
                    "value": "",
                    "units": "MISSING_UNITS_UNTIL_SOURCE_BACKED",
                    "source_path": row["source_path"],
                    "source_anchor": row["source_anchor"],
                    "source_backed": False,
                    "numeric_value_present": False,
                    "control_only": True,
                    "claim_policy": "REFUSE_PREDICTION_UNTIL_SOURCE_BACKED",
                    "promotion_requirement": row["promotion_requirement"],
                }
            )
        )
    return placeholder_rows_out


def formula_rows() -> list[dict[str, Any]]:
    specs = [
        ("FORM2825_0_Mq2", "carrier", "M_q^2 = n_q^A H_AB n_q^B", "conditional covariance-Hessian mass term", SRC_2823_CONDITIONAL, "CCR2823_1_Mq2"),
        ("FORM2825_1_Zq", "carrier", "Z_q = xi_q^2 M_q^2", "conditional stiffness from sourced xi_q and M_q", SRC_2823_CONDITIONAL, "CCR2823_2_Zq"),
        ("FORM2825_2_lambda", "carrier", "lambda_q = sqrt(Z_q/M_q^2) = xi_q", "conditional range relation", SRC_2823_CONDITIONAL, "CCR2823_3_lambda"),
        ("FORM2825_3_Btotal", "source_vector", "B_total^q = sum_i B_i^q", "component-source bookkeeping only", SRC_2822_JQ_FALLBACK, "FB2822_0_total"),
        ("FORM2825_4_Tsource", "source_vector", "T_source_norm_control <= B_total^q", "control upper-bound placeholder", SRC_2823_IMPACT, "RI2823_2_Tsource"),
        ("FORM2825_5_Scg", "response", "S_cg,total_control <= 1/2 T_source_norm_control C_qm + S_direct + S_boundary + S_extra", "control coupling sensitivity placeholder", SRC_2818_CHAIN, "CBU2818_3_qnorm_status"),
        ("FORM2825_6_Nsrc", "local_lock", "N_src_control <= U_B,max S_cg,total_control", "local source transfer control formula", SRC_2818_INTERFACE, "FPI2818_0_Nsrc"),
        ("FORM2825_7_Npair", "local_lock", "N_pair_control <= N_src_control + C_inner |Q_m^H| + N_inner_domain + N_inner_zero", "first-pair local-lock interface", SRC_2818_INTERFACE, "FPI2818_2_Npair"),
        ("FORM2825_8_Nlock", "local_lock", "N_lock_control <= N_pair_control + N_rest", "finite leakage control version", SRC_2818_CHAIN, "CBU2818_1_finite_route"),
        ("FORM2825_9_Delta", "local_lock", "Delta_m_control <= C_emb N_lock_control", "local extremum/amplitude law control form", SRC_2818_AMPLITUDE, "ALA2818_1_Nlock"),
        ("FORM2825_10_Kalg", "local_lock", "||K_alg||_D <= L_min^-2 F2_bar C_emb N_lock M_m_bar + L_min^-3 F2_bar C_emb^2 N_lock^2 M_L_bar + higher-order terms", "local transition residual control chain", SRC_2818_AMPLITUDE, "ALA2818_4_chain_insert"),
    ]
    return [
        nonclaim(
            {
                "formula_id": formula_id,
                "formula_group": group,
                "formula": formula,
                "role": role,
                "source_path": str(source_path),
                "source_anchor": anchor,
                "anchor_found": anchor in read_text(source_path),
                "control_only": True,
                "numeric_evaluation_allowed": False,
                "prediction_allowed": False,
            }
        )
        for formula_id, group, formula, role, source_path, anchor in specs
    ]


def dryrun_rows(schema: list[dict[str, Any]], placeholders: list[dict[str, Any]]) -> list[dict[str, Any]]:
    placeholders_safe = all(
        str(row["value_token"]).startswith("MISSING_")
        and not row["source_backed"]
        and not row["numeric_value_present"]
        and row["control_only"]
        for row in placeholders
    )
    required_inputs = ";".join(row["input_name"] for row in schema if row["required_for_promotion"])
    specs = [
        ("DRY2825_0_schema_parse", "schema parse", "PASS_CONTROL_SCHEMA", placeholders_safe, "all placeholder rows parse and remain nonclaim"),
        ("DRY2825_1_numeric_eval", "numeric evaluation", "REFUSED_PLACEHOLDERS_MISSING", True, "numeric evaluation intentionally refused because all values are placeholders"),
        ("DRY2825_2_claim_status", "claim status", "BLOCKED_NO_CLAIM", True, "no local GR/Newton/PPN/R10 score can be produced"),
        ("DRY2825_3_sensitivity_use", "sensitivity use", "CONTROL_ONLY", True, "runner can expose which knobs matter without treating outputs as predictions"),
        ("DRY2825_4_required_inputs", "promotion dependency list", required_inputs, True, "promotion requires every listed input to become source-backed or theorem-zero in one branch"),
    ]
    return [
        nonclaim(
            {
                "dryrun_id": dryrun_id,
                "object": obj,
                "result": result,
                "dryrun_passed": passed,
                "detail": detail,
                "numeric_evaluation_performed": False,
                "prediction_emitted": False,
                "control_only": True,
                "refused_prediction": True,
            }
        )
        for dryrun_id, obj, result, passed, detail in specs
    ]


def promotion_rows() -> list[dict[str, Any]]:
    specs = [
        ("PROM2825_0_HAB", "H_AB effective action/lift/unit source", "carrier", "source-backed H_AB in the same parent branch as q"),
        ("PROM2825_1_xiq", "xi_q smoothing/correlation scale", "carrier", "numeric or theorem-fixed xi_q with units"),
        ("PROM2825_2_selector", "q=0 selector", "normalization", "parent-signed local branch selector or theorem-zero closure"),
        ("PROM2825_3_qunits", "q units/normalization", "normalization", "same q normalization in E_q, J_q, Dq[v_m], and arena projections"),
        ("PROM2825_4_boundary", "boundary/domain class", "normalization", "signed boundary/corner/cohomology/kernel certificate"),
        ("PROM2825_5_newton", "Newton/source normalization", "normalization", "source-measure equality and universal G bridge"),
        ("PROM2825_6_Jq", "J_q components", "source_vector", "every component source-backed or theorem-zero in E_q dual norm"),
        ("PROM2825_7_Dqvm", "Dq[v_m] and C_qm", "response", "actual vertical generator and q-to-m response constant"),
        ("PROM2825_8_worldtube", "worldtube/profile constants", "local_lock", "U_B,max, C_inner, Q_m^H, domain/zero/rest terms sourced"),
        ("PROM2825_9_arena", "arena projection kernels", "empirical", "R10/PPN/clock/orbital projection maps in the same normalization"),
        ("PROM2825_10_norm_coherence", "no mixed norm", "global", "one E_q/E_q* normalization through carrier, source, and local lock"),
        ("PROM2825_11_no_claim", "claim gate", "global", "no prediction row until all above pass"),
    ]
    return [
        nonclaim(
            {
                "promotion_id": promotion_id,
                "requirement": requirement,
                "input_group": group,
                "acceptance_condition": condition,
                "satisfied": False,
                "current_status": "BLOCKED_PENDING_SOURCE_OR_THEOREM_ZERO",
                "promotion_allowed": False,
                "control_only": True,
            }
        )
        for promotion_id, requirement, group, condition in specs
    ]


def gate_rows(rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    sources_ok = all(row["path_exists"] and row["anchors_found"] for row in rows["sources"])
    schema_ok = all(row["anchor_found"] and row["control_only"] for row in rows["schema"])
    placeholders_ok = all(
        str(row["value_token"]).startswith("MISSING_")
        and not row["source_backed"]
        and not row["numeric_value_present"]
        and not row["valid_for_claim"]
        for row in rows["placeholders"]
    )
    dryrun_ok = all(row["dryrun_passed"] and row["control_only"] and row["refused_prediction"] for row in rows["dryrun"])
    formulas_ok = all(row["anchor_found"] and row["control_only"] and not row["prediction_allowed"] for row in rows["formulas"])
    promotion_blocked = not any(row["satisfied"] or row["promotion_allowed"] for row in rows["promotion"])
    specs = [
        ("CG2825_0_sources", "source anchors present", sources_ok, "imported ledgers are reproducible"),
        ("CG2825_1_schema", "control input schema parses", schema_ok, "all schema rows cite an existing source anchor"),
        ("CG2825_2_placeholders", "all placeholder rows are nonclaim", placeholders_ok, "all values are missing tokens with no numeric/source-backed status"),
        ("CG2825_3_formulas", "control formulas parse", formulas_ok, "formula rows are bookkeeping only and cannot emit predictions"),
        ("CG2825_4_dryrun", "dry-run refusal works", dryrun_ok, "numeric prediction is refused until source inputs exist"),
        ("CG2825_5_promotion", "promotion remains blocked", promotion_blocked, "promotion needs source-backed or theorem-zero carrier/source/response/local inputs"),
        ("CG2825_6_GR_Newton", "local GR/Newton claim allowed", False, "q=0 selector, Newton source normalization, and Dq[v_m] remain missing"),
        ("CG2825_7_PPN_R10", "PPN/R10/clock/orbital claim allowed", False, "arena projection and local source vector are not source-backed"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "gate_passed": passed,
                "status": "PASS_NONCLAIM" if passed else "BLOCKED",
                "reason": reason,
            }
        )
        for gate_id, claim, passed, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2825_0_runner", "Control-only runner/schema was built.", "PASS_NONCLAIM_SKELETON", "the carrier/source/local-lock chain is now machine-readable without emitting a physics prediction", "use it only to expose dependencies"),
        ("DEC2825_1_no_claim", "No local claim is promoted.", "BLOCKED_AS_DESIGNED", "every numeric/source-backed input is still missing or theorem-unsigned", "do not feed results into R10/PPN/clock/orbital score rows"),
        ("DEC2825_2_best_gain", "The useful gain is now dependency discipline.", "INPUT_PRIORITY_VISIBLE", "H_AB, xi_q, selector, boundary/domain, J_q components, and Dq[v_m] are explicit promotion gates", "rank the missing inputs before another derivation hunt"),
        ("DEC2825_3_next", "Next target is a promotion-input priority map.", "NEXT_2826_PRIORITY_MAP", "we should choose the least-scrutinized route for source/theorem closure instead of circling the same branch blindly", "build a ranked input-priority ledger and first-fill plan"),
    ]
    return [
        nonclaim(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, result, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2825_0_2826",
                "status": "selected_primary",
                "target_doc": "2826-Y5-R2FR-control-runner-promotion-input-priority-map-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_control_runner_promotion_input_priority_map_under_AX1090_2826.py",
                "mission": "rank the minimum missing source/theorem inputs needed to promote the 2825 control runner, separating derivation targets from empirical/source-bound targets without inserting fake numeric values",
                "acceptance": "priority map cites every blocker, selects a first-fill path, keeps all claim flags false, and does not edit formalization-workbench",
                "forbidden": "do not add toy numeric coefficients; do not claim local GR/Newton/PPN/R10; do not turn control sensitivity into evidence",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("BR2825_0_schema_copy", OUTPUTS["placeholders"], BRANCH_OUTPUTS["schema_copy"], "source-weight copy of control-only smoke input placeholders"),
        ("BR2825_1_dryrun_copy", OUTPUTS["dryrun"], BRANCH_OUTPUTS["dryrun_copy"], "local-bounds copy of refused dry-run results"),
        ("BR2825_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue for promotion-input priority map"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            nonclaim(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def iter_cited_paths(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[Path]:
    keys = {"source_path", "source_paths", "source_table", "copy_path"}
    paths: list[Path] = []
    for rows in rows_by_name.values():
        for row in rows:
            for key in keys:
                value = row.get(key)
                if value is None:
                    continue
                for token in str(value).split(";"):
                    item = token.strip()
                    if not item or item.startswith("http") or item.startswith("MISSING_"):
                        continue
                    path = Path(item)
                    if not path.is_absolute():
                        path = ROOT / item
                    paths.append(path)
    return paths


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            for key in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if str(row.get(key, "")).lower() == "true":
                    return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    start = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            try:
                if path.stat().st_mtime >= start:
                    return False
            except OSError:
                return False
    return True


def under_root(paths: list[Path]) -> bool:
    root_text = str(ROOT.resolve()).lower()
    return all(str(path.resolve()).lower().startswith(root_text) for path in paths)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    cited_paths = iter_cited_paths(rows_by_name)
    checks = [
        ("VAL2825_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all source-register local paths exist"),
        ("VAL2825_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all source-register anchors were found"),
        ("VAL2825_2_schema_anchors", all(row["anchor_found"] for row in rows_by_name["schema"]), "all control schema source anchors were found"),
        ("VAL2825_3_placeholder_nonclaim", all(not row["valid_for_claim"] and not row["score_ready"] and not row["valid_prediction_row"] for row in rows_by_name["placeholders"]), "all placeholders are explicitly nonclaim"),
        ("VAL2825_4_no_numeric_values", not any(row["numeric_value_present"] or row["source_backed"] for row in rows_by_name["placeholders"]), "no placeholder has numeric/source-backed status"),
        ("VAL2825_5_missing_tokens", all(str(row["value_token"]).startswith("MISSING_") for row in rows_by_name["placeholders"]), "all placeholder values are missing-token rows"),
        ("VAL2825_6_formula_nonprediction", all(row["control_only"] and not row["prediction_allowed"] and row["anchor_found"] for row in rows_by_name["formulas"]), "all formulas are nonprediction control formulas"),
        ("VAL2825_7_dryrun_refused", all(row["dryrun_passed"] and row["refused_prediction"] and not row["prediction_emitted"] for row in rows_by_name["dryrun"]), "dry-run refuses numeric prediction"),
        ("VAL2825_8_promotion_blocked", not any(row["satisfied"] or row["promotion_allowed"] for row in rows_by_name["promotion"]), "promotion requirements remain unsatisfied"),
        ("VAL2825_9_claims_blocked", not any(row["claim_allowed"] for row in rows_by_name["gates"]), "no claim gate allows GR/Newton/PPN/R10"),
        ("VAL2825_10_next_target_2826", any(row["next_id"] == "NEXT2825_0_2826" and row["selected"] for row in rows_by_name["next"]), "promotion-input priority map selected next"),
        ("VAL2825_11_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2825_12_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2825_13_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2825_14_cited_paths_exist", all(path.exists() for path in cited_paths), "all cited local file/copy paths in generated rows exist"),
        ("VAL2825_15_no_claim_flags", no_claim_flags(rows_by_name), "no score_ready, valid_prediction_row, valid_for_claim, or claim_allowed flag is true"),
        ("VAL2825_16_generated_under_post_checkpoint", under_root(output_paths + branch_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2825_17_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2825_18_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2825_OVERALL",
            "passed": overall,
            "detail": "2825 builds a machine-readable nonclaim control-only local-lock smoke runner/schema, refuses numeric predictions because every promotion input is missing/source-unsigned, and selects a priority-map target next.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    content = f"""# 2825 - Y5 R2FR Eq Control Only Local Lock Smoke Runner And Source Input Schema Under AX1090

Status: `Y5_R2FR_2825_control_only_local_lock_smoke_runner_schema_nonclaim`

## Private Verdict

2825 builds the runner skeleton, not a physics result.

The conditional `E_q` carrier is retained only as a control coordinate:

`E_q[delta q]^2 = int_W (Z_q |nabla delta q|^2 + M_q^2 delta q^2) dV_e`

with `M_q^2=n_q^A H_AB n_q^B`, `Z_q=xi_q^2 M_q^2`, and `lambda_q=xi_q` still requiring parent-signed sources.

The runner now exposes the missing couplings and local-lock dependencies in a machine-readable way. It refuses all numeric prediction rows because `H_AB`, `xi_q`, `q` normalization, selector, boundary/domain, `J_q` component bounds, `Dq[v_m]`, `C_qm`, and worldtube/local constants remain placeholders.

So the gain is discipline: we can see what must be sourced or theorem-zeroed before local GR/Newton/PPN/R10 claims can even start.

## Source Register

{markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Control Input Schema

{markdown_table(rows["schema"], ["schema_id", "input_group", "input_name", "current_status", "promotion_requirement", "source_backed", "numeric_value_present", "valid_for_claim"])}

## Placeholder Input Rows

{markdown_table(rows["placeholders"], ["placeholder_id", "input_group", "input_name", "value_token", "units", "source_backed", "numeric_value_present", "valid_for_claim"])}

## Local Lock Control Formulas

{markdown_table(rows["formulas"], ["formula_id", "formula_group", "formula", "role", "control_only", "prediction_allowed", "valid_for_claim"])}

## Dry Run Results

{markdown_table(rows["dryrun"], ["dryrun_id", "object", "result", "dryrun_passed", "numeric_evaluation_performed", "prediction_emitted", "refused_prediction", "valid_for_claim"])}

## Promotion Requirements

{markdown_table(rows["promotion"], ["promotion_id", "requirement", "input_group", "acceptance_condition", "satisfied", "promotion_allowed", "valid_for_claim"])}

## Claim Gates

{markdown_table(rows["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "reason", "claim_allowed"])}

## Decision Ledger

{markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "next_action", "valid_for_claim"])}

## Next Target

{markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_rows()
    rows["schema"] = schema_rows()
    rows["placeholders"] = placeholder_rows(rows["schema"])
    rows["formulas"] = formula_rows()
    rows["dryrun"] = dryrun_rows(rows["schema"], rows["placeholders"])
    rows["promotion"] = promotion_rows()
    rows["gates"] = gate_rows(rows)
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "schema", "placeholders", "formulas", "dryrun", "promotion", "gates", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])

    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2825_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2825_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
