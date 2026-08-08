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
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2896-Y5-R2FR-source-normalized-Newton-beta-envelope-or-first-R11-fill-under-AX1090.md"

SRC_2895_DOC = ROOT / "2895-Y5-R2FR-R11-beta-component-vector-or-EH-nohair-theorem-under-AX1090.md"
SRC_2895_NEXT = RESIDUALS / "P8_Y5_R2FR_2895_NEXT_TARGET.csv"
SRC_2895_COMPONENTS = RESIDUALS / "P8_Y5_R2FR_2895_R11_BETA_COMPONENT_ROWS_NONCLAIM.csv"
SRC_2894_AB = RESIDUALS / "P8_Y5_R2FR_2894_AB_COEFFICIENT_ROW_NONCLAIM.csv"
SRC_2893_VECTOR = RESIDUALS / "P8_Y5_R2FR_2893_FINITE_BETA_VECTOR_ROW_NONCLAIM.csv"
SRC_531_DOC = ROOT / "531-Y5-source-normalized-Newton-and-beta-residual-envelope.md"
SRC_531_COMPONENTS = RESIDUALS / "P8_Y5_BETA_ENVELOPE_COMPONENTS.csv"
SRC_531_ROUTE = RESIDUALS / "P8_Y5_BETA_ENVELOPE_ROUTE_UPDATE.csv"
SRC_BETA_EVAL = RESIDUALS / "P8_Y5_BETA_COEFFICIENT_EVALUATOR.csv"
SRC_QLOC_U2 = RESIDUALS / "P8_Y5_QLOC_U2_BOUND.csv"
SRC_SOURCE_SCORE = RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv"
SRC_R11_STATUS = RESIDUALS / "R11_EXECUTABLE_VECTOR_STATUS.csv"
SRC_LOCAL_BOUNDS = LOCAL_BOUNDS / "local_bound_claims.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2896_SOURCE_REGISTER.csv",
    "components": RESIDUALS / "P8_Y5_R2FR_2896_BETA_ENVELOPE_COMPONENTS.csv",
    "evaluator": RESIDUALS / "P8_Y5_R2FR_2896_BETA_ENVELOPE_EVALUATOR.csv",
    "newton": RESIDUALS / "P8_Y5_R2FR_2896_SOURCE_NORMALIZED_NEWTON_PRECONDITION_GATE.csv",
    "firstfill": RESIDUALS / "P8_Y5_R2FR_2896_FIRST_R11_FILL_QUEUE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2896_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2896_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2896_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2896_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2896_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2896_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "components_copy": LOCAL_BOUNDS / "RAB_BETA_ENVELOPE_COMPONENTS_2896_NONCLAIM.csv",
    "evaluator_copy": BETA_DOCS / "RAB_BETA_ENVELOPE_EVALUATOR_2896_NONCLAIM.csv",
    "firstfill_copy": BETA_DOCS / "RAB_FIRST_R11_FILL_QUEUE_2896_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2896_source_normalization_operator_first_fill_NEXT.csv",
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
        ("SRC2896_0_2895_doc", SRC_2895_DOC, "Status: `Y5_R2FR_2895;NEXT2895_0_2896", "2895 R11 beta handoff"),
        ("SRC2896_1_2895_next", SRC_2895_NEXT, "NEXT2895_0_2896;combine A/B source", "explicit 2896 target"),
        ("SRC2896_2_2895_components", SRC_2895_COMPONENTS, "R11B2895_0_source_normalization;sum_abs_delta_beta_R11_i", "current R11 beta components"),
        ("SRC2896_3_2894_ab", SRC_2894_AB, "ABR2894_0_current_MTS_AB_source_row;MISSING_A_SOURCE", "A/B source row"),
        ("SRC2896_4_2893_vector", SRC_2893_VECTOR, "FBR2893_6_Delta_beta_total_abs;ALL_COMPONENTS_NUMERIC_OR_THEOREM_ZERO", "finite beta vector source"),
        ("SRC2896_5_531_doc", SRC_531_DOC, "Delta_beta_total_abs;source-normalized Newton remains", "older strict beta envelope"),
        ("SRC2896_6_531_components", SRC_531_COMPONENTS, "ENV531_0_first_order_Newton_precondition;ENV531_6_q_loc_alpha3_guard", "prior beta envelope components"),
        ("SRC2896_7_531_route", SRC_531_ROUTE, "SOURCE_NORMALIZED_NEWTON;first_order_precondition", "prior route update"),
        ("SRC2896_8_beta_eval", SRC_BETA_EVAL, "BETA526_0_source_AB;not_run_missing_A_or_B", "beta coefficient evaluator"),
        ("SRC2896_9_qloc_u2", SRC_QLOC_U2, "QBU526_0_compact_shell_to_beta_if_same_normalization;QBU526_1_compact_shell_to_alpha3_warning", "q_loc provisional beta and alpha3 guards"),
        ("SRC2896_10_source_score", SRC_SOURCE_SCORE, "SRC523_10_second_order_PPN_source;SRC523_11_total_no_cancellation_score", "source-normalization residual scorecard"),
        ("SRC2896_11_r11_status", SRC_R11_STATUS, "source_normalization_operator;template_only_retained_core_blocker", "R11 first-fill status"),
        ("SRC2896_12_local_bounds", SRC_LOCAL_BOUNDS, "Will_2014_PPN_beta_table;7.8e-05", "local beta comparator anchor"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def component_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "ENV2896_0_Newton_precondition",
            "source_normalized_Newton_precondition",
            "measured_mu=G0*M_H with zero charge/current/source/range/time/frame/domain residuals",
            "MISSING_SOURCE_NORMALIZATION_SCORECARD_CLOSE",
            "",
            "fail_unfilled",
            "blocks beta/PPN/local-GR promotion even if second-order rows later fill",
            "highest",
        ),
        (
            "ENV2896_1_source_AB",
            "delta_beta_source",
            "B_source/A_source^2 - 1",
            "MISSING_A_SOURCE_AND_B_SOURCE",
            "",
            "missing",
            "blocks strict beta envelope evaluation",
            "highest",
        ),
        (
            "ENV2896_2_R11_sum",
            "sum_i_abs_delta_beta_R11_i",
            "sum_abs(delta_beta_source_R11,delta_beta_R2_fR,delta_beta_boundary_domain,delta_beta_scalar_class,delta_beta_readout_connection,...)",
            "MISSING_R11_COMPONENT_VALUES_OR_EH_NOHAIR",
            "",
            "missing",
            "blocks strict beta envelope evaluation",
            "highest",
        ),
        (
            "ENV2896_3_q_loc",
            "delta_beta_q_loc",
            "physical U2 projection of P_loc(nabla Gamma_eff-div Khat)",
            "7.432631961576971e-06_PROVISIONAL_SAME_NORMALIZATION_ONLY",
            "7.432631961576971e-06_DIAGNOSTIC_ONLY",
            "provisional_not_claimable",
            "below beta lock only if same beta normalization is proved",
            "high",
        ),
        (
            "ENV2896_4_boundary_domain",
            "delta_beta_boundary_domain",
            "boundary/domain/projector quadratic stress beta projection",
            "MISSING_BOUNDARY_DOMAIN_ZERO_OR_COEFFICIENT_MAP",
            "",
            "missing",
            "blocks strict beta envelope evaluation and alpha3/xi safety",
            "high",
        ),
        (
            "ENV2896_5_readout",
            "delta_beta_readout",
            "second-order source metric to observed isotropic PPN readout mismatch",
            "MISSING_SAME_READOUT_THEOREM_THROUGH_O_U2",
            "",
            "missing",
            "blocks coordinate/readout-safe beta claim",
            "high",
        ),
        (
            "ENV2896_6_epsilon_SN",
            "epsilon_SN",
            "(mu_obs-G_eff M_H)/(G_eff M_H)",
            "MISSING_GAUSS_ORBITAL_SOURCE_CURRENT_SCORECARD",
            "",
            "missing",
            "prevents measured-GM denominator from acting as hidden beta fit",
            "highest",
        ),
        (
            "ENV2896_7_q_loc_alpha3_guard",
            "q_loc_alpha3_projection_warning",
            "same compact q_loc budget compared to alpha3 if it leaks into preferred-frame/momentum-flux rows",
            "185815799039424.3_ALPHA3_RATIO_IF_PROJECTION_APPLIES",
            "not_beta_sum_component",
            "severe_guard",
            "blocks local-GR even if q_loc beta diagnostic looks small",
            "guard",
        ),
    ]
    return [
        add_common(
            {
                "component_id": component_id,
                "symbol": symbol,
                "formula_or_map": formula,
                "current_value": current_value,
                "absolute_value_for_sum": abs_value,
                "status": status,
                "claim_effect": claim_effect,
                "priority": priority,
                "source_path": "MISSING_SOURCE_BACKED_THEOREM_OR_NUMERIC_COMPONENT_ROW",
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for component_id, symbol, formula, current_value, abs_value, status, claim_effect, priority in specs
    ]


def evaluator_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "EVAL2896_0_strict_claim_envelope",
            "strict_claim",
            "delta_beta_source;sum_i_abs_delta_beta_R11_i;delta_beta_q_loc;delta_beta_boundary_domain;delta_beta_readout;epsilon_SN",
            "source_normalized_Newton_precondition;delta_beta_source;sum_i_abs_delta_beta_R11_i;delta_beta_q_loc_U2_conversion;delta_beta_boundary_domain;delta_beta_readout;epsilon_SN",
            "NOT_EVALUATED",
            "7.8e-05",
            "",
            "not_evaluable_missing_components",
        ),
        (
            "EVAL2896_1_provisional_q_loc_only",
            "diagnostic_not_claim",
            "q_loc_compact_shell_if_same_beta_normalization",
            "all_other_components_assumed_zero_only_for_diagnostic",
            "7.432631961576971e-06",
            "7.8e-05",
            "0.09529015335355091",
            "below_beta_lock_if_same_normalization_only",
        ),
        (
            "EVAL2896_2_alpha3_guard",
            "local_GR_guard_not_beta_sum",
            "q_loc_compact_shell_if_same_preferred_frame_projection",
            "physical_projection_map",
            "NOT_BETA_ENVELOPE",
            "4e-20_alpha3_bound",
            "185815799039424.3",
            "severe_warning_if_projection_applies",
        ),
        (
            "EVAL2896_3_no_cancellation_policy",
            "policy",
            "absolute_values_only",
            "none_can_be_cancelled_by_tuning",
            "SUM_ABS_REQUIRED",
            "7.8e-05",
            "",
            "policy_enforced",
        ),
    ]
    return [
        add_common(
            {
                "evaluator_id": evaluator_id,
                "mode": mode,
                "included_components": included,
                "missing_components": missing,
                "total_abs_beta_envelope": total,
                "beta_bound_abs": beta_bound,
                "bound_ratio": ratio,
                "result": result,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for evaluator_id, mode, included, missing, total, beta_bound, ratio, result in specs
    ]


def newton_rows() -> list[dict[str, Any]]:
    specs = [
        ("NG2896_0_scorecard_exists", "source-normalization scorecard exists", "PASS_NONCLAIM", "scorecard rows exist but are unfilled"),
        ("NG2896_1_measured_GM", "measured orbital mu equals parent Hilbert/source charge", "FAIL", "charge-current/Gauss/orbital/source-current chain remains unfilled"),
        ("NG2896_2_derivative_hair", "mu_obs has no time/range/radial/species/frame/domain derivative", "FAIL", "derivative residual rows are unfilled"),
        ("NG2896_3_second_order_source", "first-order source normalization survives beta/PPN order", "FAIL", "delta_beta_source and R11 source/operator rows are missing"),
        ("NG2896_4_no_absorption_cheat", "measured GM cannot absorb relative/range/time/source coefficients", "PASS_GUARD", "all source-normalization residual rows remain explicit and nonclaim"),
        ("NG2896_5_precondition_verdict", "source-normalized Newton precondition for local GR", "FAIL_CLOSED", "not derived and not scored"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "gate": gate,
                "current_status": status,
                "detail": detail,
                "gate_passed": False,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for gate_id, gate, status, detail in specs
    ]


def firstfill_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "FILL2896_0_source_normalization_operator",
            "source_normalization_operator",
            "mu_extra_or_delta_GM_operator_vector;A_source;B_source;epsilon_SN",
            "highest",
            "blocks source-normalized Newton and beta source square law at the same time",
            "derive constant measured-GM/source-current closure or fill first finite source-normalization residual row",
            True,
        ),
        (
            "FILL2896_1_R2_fR_scalar_mode",
            "R2_fR_scalar_mode",
            "c_R2_or_c_fR;scalar_mass;source_coupling;beta/gamma/alpha(lambda)_map",
            "high",
            "first metric-operator family that can be bounded against beta/gamma/R10 if source-normalization stalls",
            "fill only after source-normalization route is explicitly blocked or in parallel data pass",
            False,
        ),
        (
            "FILL2896_2_boundary_projector_domain",
            "boundary_topological_terms;projector_domain_stress",
            "boundary coefficient;projector stress map;alpha3/xi guard",
            "high",
            "could dominate through alpha3/xi even if beta is small",
            "derive no-flux/no-stress theorem or finite projector-stress row",
            False,
        ),
        (
            "FILL2896_3_q_loc_U2_projection",
            "q_loc_Gamma_Khat",
            "U2 conversion factor;physical profile;alpha3 projection map",
            "high",
            "diagnostic q_loc beta number is promising but unsafe without projection proof",
            "return after source-normalization convention is fixed",
            False,
        ),
    ]
    return [
        add_common(
            {
                "queue_id": queue_id,
                "operator_family": family,
                "required_real_input": required,
                "priority": priority,
                "why_first_or_held": why,
                "next_action": next_action,
                "selected_primary": selected,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for queue_id, family, required, priority, why, next_action, selected in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2896_0_envelope_written", "strict beta no-cancellation envelope is written", "PASS_NONCLAIM", "all live source/R11/q_loc/boundary/readout/source-normalization pieces are present"),
        ("GATE2896_1_newton_precondition", "source-normalized Newton precondition passes", "FAIL", "source scorecard is unfilled"),
        ("GATE2896_2_source_AB", "A/B source beta row is executable", "FAIL", "A_source and B_source are missing"),
        ("GATE2896_3_R11_beta", "R11 beta component sum is executable", "FAIL", "component rows are template/missing"),
        ("GATE2896_4_q_loc", "q_loc U2 projection is physically normalized and preferred-frame safe", "FAIL", "q_loc number is diagnostic only and alpha3 guard remains"),
        ("GATE2896_5_total_beta", "Delta_beta_total_abs can be compared to beta bound", "FAIL", "strict envelope missing components"),
        ("GATE2896_6_first_fill", "first fill target selected", "PASS_NONCLAIM", "source_normalization_operator selected as primary fill target"),
        ("GATE2896_7_local_gr", "local GR/PPN branch closes", "FAIL", "Newton precondition and beta envelope remain blocked"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": False,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for gate_id, criterion, result, reason in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2896_0_strict_beta_envelope_runner",
                "status": "REFUSED_MISSING_COMPONENTS",
                "strict_components_required": 6,
                "strict_components_evaluable": 0,
                "diagnostic_components_evaluable": 1,
                "reason": "strict envelope requires source-normalized Newton, A/B, R11 sum, physical q_loc U2, boundary/domain, readout, and epsilon_SN rows; only q_loc diagnostic has a provisional number",
                "runner_ready": False,
                "claim_unlocked": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2896_0_envelope", "KEEP_STRICT_BETA_ENVELOPE", "this is the no-cheat object needed before local GR beta can be claimed", "use only sum_abs over real/theorem-zero components"),
        ("DEC2896_1_q_loc", "KEEP_QLOC_DIAGNOSTIC_ONLY", "it is below beta lock only under unproved normalization and may be disastrous under alpha3 projection", "do not score it yet"),
        ("DEC2896_2_Newton", "SOURCE_NORMALIZED_NEWTON_IS_FIRST_PRECONDITION", "measured-GM/source-current closure is required before A/B and beta are physically meaningful", "attack source_normalization_operator first"),
        ("DEC2896_3_next", "SELECT_SOURCE_NORMALIZATION_OPERATOR_FIRST_FILL", "it is the highest priority R11 family and touches Newton, A/B, beta, Gdot and R10", "build 2897 measured-GM/source-normalization operator first-fill checkpoint"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
                "accepted_for_scoring": False,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2896_0_2897",
                "status": "selected_primary",
                "target_doc": "2897-Y5-R2FR-source-normalization-operator-first-fill-or-measured-GM-current-closure-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_source_normalization_operator_first_fill_or_measured_GM_current_closure_under_AX1090_2897.py",
                "mission": "derive measured-GM/source-current closure for the source_normalization_operator; if it fails, stage the first finite source-normalization residual row with units, source paths, and no-cancellation guards",
                "forbidden_shortcuts": "no measured-GM absorption; no A/B fill from reference GR; no cancellation; no placeholder coefficients; no GitHub action",
                "selected": True,
                "accepted_for_scoring": False,
            }
        ),
        add_common(
            {
                "next_id": "NEXT2896_1_held_R2_fR",
                "status": "held_next_if_source_norm_stalls",
                "target_doc": "2897b-Y5-R2FR-R2-fR-scalar-beta-row-or-nohair-proof.md",
                "target_script": "scripts/Y5_R2FR_R2_fR_scalar_beta_row_or_nohair_proof_2897b.py",
                "mission": "fill the first metric-operator R11 beta row only after source-normalization status is explicit",
                "forbidden_shortcuts": "do not skip measured-GM/source-normalization precondition silently",
                "selected": False,
                "accepted_for_scoring": False,
            }
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("BR2896_0_components_copy", OUTPUTS["components"], BRANCH_OUTPUTS["components_copy"], "local-bounds copy of beta envelope components"),
        ("BR2896_1_evaluator_copy", OUTPUTS["evaluator"], BRANCH_OUTPUTS["evaluator_copy"], "beta-source copy of envelope evaluator"),
        ("BR2896_2_firstfill_copy", OUTPUTS["firstfill"], BRANCH_OUTPUTS["firstfill_copy"], "beta-source copy of first R11 fill queue"),
        ("BR2896_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue next target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in copy_specs:
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


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def generated_under_root(paths: list[Path]) -> bool:
    root_resolved = ROOT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError:
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "parent_signed",
        "theorem_zero_adopted",
        "finite_value_present",
        "prediction_source_backed",
        "accepted_for_scoring",
        "gate_passed",
        "runner_ready",
        "claim_unlocked",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    components = rows_by_name["components"]
    evaluator = rows_by_name["evaluator"]
    newton = rows_by_name["newton"]
    firstfill = rows_by_name["firstfill"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    symbols = {row["symbol"] for row in components}
    required_symbols = {
        "source_normalized_Newton_precondition",
        "delta_beta_source",
        "sum_i_abs_delta_beta_R11_i",
        "delta_beta_q_loc",
        "delta_beta_boundary_domain",
        "delta_beta_readout",
        "epsilon_SN",
        "q_loc_alpha3_projection_warning",
    }
    strict = next(row for row in evaluator if row["evaluator_id"] == "EVAL2896_0_strict_claim_envelope")
    qloc = next(row for row in evaluator if row["evaluator_id"] == "EVAL2896_1_provisional_q_loc_only")
    selected_fill = next(row for row in firstfill if row["selected_primary"] is True)

    checks = [
        ("VAL2896_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2896_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2896_2_components_complete", required_symbols.issubset(symbols), "strict beta envelope includes all required live components"),
        ("VAL2896_3_strict_refused", strict["result"] == "not_evaluable_missing_components" and strict["total_abs_beta_envelope"] == "NOT_EVALUATED", "strict beta envelope refuses missing components"),
        ("VAL2896_4_qloc_diagnostic", qloc["total_abs_beta_envelope"] == "7.432631961576971e-06" and qloc["valid_for_claim"] is False, "q_loc remains diagnostic only"),
        ("VAL2896_5_newton_fail_closed", all(row["gate_passed"] is False for row in newton), "source-normalized Newton gates fail closed"),
        ("VAL2896_6_first_fill_selected", selected_fill["operator_family"] == "source_normalization_operator", "source_normalization_operator is selected as first fill target"),
        ("VAL2896_7_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "acceptance gates fail closed"),
        ("VAL2896_8_runner_refused", runner[0]["status"] == "REFUSED_MISSING_COMPONENTS" and runner[0]["runner_ready"] is False, "runner refuses missing components"),
        ("VAL2896_9_next_target_2897", next_target[0]["next_id"] == "NEXT2896_0_2897" and next_target[0]["selected"] is True, "2897 source-normalization first-fill target selected"),
        ("VAL2896_10_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2896_11_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2896_12_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2896_13_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2896_14_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2896_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2896_16_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2896_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2896 wrote the strict source-normalized beta envelope, kept q_loc diagnostic-only, failed source-normalized Newton closed, and selected source_normalization_operator/measured-GM closure as the first fill target for 2897.",
            "timestamp_utc": now(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    text = f"""# 2896 - Y5 R2FR Source-Normalized Newton Beta Envelope Or First R11 Fill Under AX1090

Status: `Y5_R2FR_2896_strict_beta_envelope_written_missing_components_source_normalization_first_fill_2897_next`

## Private Verdict

2896 puts the local beta problem into one boxing ring.

The strict claim object is:

`Delta_beta_total_abs = |delta_beta_source| + sum_i|delta_beta_R11_i| + |delta_beta_q_loc| + |delta_beta_boundary_domain| + |delta_beta_readout| + |epsilon_SN|`.

Current MTS cannot evaluate it. `A_source/B_source`, the R11 beta sum, boundary/domain, readout, physical `q_loc` U2 normalization, and the measured-GM/source-current scorecard are not closed.

The q_loc compact-shell number remains interesting but diagnostic only: it is about `0.095` of the beta lock if already beta-normalized, while the same leakage would be violently unsafe if it projects into alpha3/preferred-frame momentum flux.

Therefore the next first-fill target is not a glamorous new operator; it is the source-normalization operator / measured-GM current chain. If that does not close, no beta or local-GR route can honestly claim the observed Newtonian denominator.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Beta Envelope Components

{md_table(rows_by_name["components"], ["component_id", "symbol", "formula_or_map", "current_value", "absolute_value_for_sum", "status", "priority", "valid_for_claim"])}

## Beta Envelope Evaluator

{md_table(rows_by_name["evaluator"], ["evaluator_id", "mode", "included_components", "missing_components", "total_abs_beta_envelope", "beta_bound_abs", "bound_ratio", "result", "valid_for_claim"])}

## Source-Normalized Newton Gate

{md_table(rows_by_name["newton"], ["gate_id", "gate", "current_status", "detail", "gate_passed", "valid_for_claim"])}

## First R11 Fill Queue

{md_table(rows_by_name["firstfill"], ["queue_id", "operator_family", "required_real_input", "priority", "why_first_or_held", "selected_primary", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "strict_components_required", "strict_components_evaluable", "diagnostic_components_evaluable", "reason", "runner_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    remove_pycache()
    rows_by_name = {
        "sources": source_register_rows(),
        "components": component_rows(),
        "evaluator": evaluator_rows(),
        "newton": newton_rows(),
        "firstfill": firstfill_rows(),
        "gates": gate_rows(),
        "runner": runner_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], branch_rows)
    rows_by_name["branches"] = branch_rows
    remove_pycache()
    validation = validation_rows(rows_by_name, branch_rows)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name, branch_rows, validation)
    remove_pycache()
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation if row["validation_id"] == "VAL2896_OVERALL")
    print(f"VAL2896_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
