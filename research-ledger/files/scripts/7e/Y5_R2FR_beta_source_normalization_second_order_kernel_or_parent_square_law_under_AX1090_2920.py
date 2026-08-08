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

CHECKPOINT = "2920"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2920-Y5-R2FR-beta-source-normalization-second-order-kernel-or-parent-square-law-under-AX1090.md"

SRC_2919_DOC = ROOT / "2919-Y5-R2FR-stationary-alpha3-flux-zero-theorem-or-beta-source-normalization-kernel-under-AX1090.md"
SRC_2919_NEXT = RESIDUALS / "P8_Y5_R2FR_2919_NEXT_TARGET.csv"
SRC_BETA_2574 = RESIDUALS / "P8_Y5_PPN_VECTOR_2574_BETA_SECOND_ORDER_COUPLING_GATE.csv"
SRC_BETA_LAW_2893 = RESIDUALS / "P8_Y5_R2FR_2893_BETA_SOURCE_NORMALIZED_COEFFICIENT_LAW.csv"
SRC_BETA_VECTOR_2893 = RESIDUALS / "P8_Y5_R2FR_2893_FINITE_BETA_VECTOR_ROW_NONCLAIM.csv"
SRC_EH_NOHAIR_2895 = RESIDUALS / "P8_Y5_R2FR_2895_EH_NOHAIR_BETA_THEOREM_ATTEMPT.csv"
SRC_R11_BETA_2895 = RESIDUALS / "P8_Y5_R2FR_2895_R11_BETA_COMPONENT_ROWS_NONCLAIM.csv"
SRC_BETA_ENV_2896 = RESIDUALS / "P8_Y5_R2FR_2896_BETA_ENVELOPE_COMPONENTS.csv"
SRC_NEWTON_GATE_2896 = RESIDUALS / "P8_Y5_R2FR_2896_SOURCE_NORMALIZED_NEWTON_PRECONDITION_GATE.csv"
SRC_SOURCE_OPERATOR_2897 = RESIDUALS / "P8_Y5_R2FR_2897_SOURCE_NORMALIZATION_OPERATOR_ROW_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2920_SOURCE_REGISTER.csv",
    "square_audit": RESIDUALS / "P8_Y5_R2FR_2920_PARENT_SQUARE_LAW_AUDIT.csv",
    "beta_kernel": RESIDUALS / "P8_Y5_R2FR_2920_BETA_SECOND_ORDER_SOURCE_NORMALIZATION_KERNEL.csv",
    "newton_queue": RESIDUALS / "P8_Y5_R2FR_2920_SOURCE_NORMALIZED_NEWTON_GAUSS_ORBITAL_SCORECARD_QUEUE.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2920_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2920_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2920_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2920_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2920_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "square_audit_copy": PARENT_ACTION / "Beta_parent_square_law_audit_2920_NONCLAIM.csv",
    "beta_kernel_copy": LOCAL_BOUNDS / "Beta_second_order_source_normalization_kernel_2920_NONCLAIM.csv",
    "newton_queue_copy": RAB_QUEUE / "JR2920_SOURCE_NORMALIZED_NEWTON_GAUSS_ORBITAL_SCORECARD_NEXT_NONCLAIM.csv",
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


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


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
        ("SRC2920_00_2919_doc", SRC_2919_DOC, "beta_eff = B_source/A_source^2;Validation overall", "2919 handoff: beta square-law selected after alpha3 stationary route failed"),
        ("SRC2920_01_2919_next", SRC_2919_NEXT, "NEXT2919_0_2920;B_source=A_source^2", "machine-readable 2920 target"),
        ("SRC2920_02_2574_beta_gate", SRC_BETA_2574, "BETA2574_2_source_coupling;BETA2574_4_verdict", "older beta second-order coupling gate"),
        ("SRC2920_03_2893_beta_law", SRC_BETA_LAW_2893, "BSL2893_2_extract_beta;BSL2893_3_source_residual;BSL2893_5_no_smuggling", "source-normalized beta extraction law"),
        ("SRC2920_04_2893_beta_vector", SRC_BETA_VECTOR_2893, "FBR2893_0_delta_beta_source;FBR2893_6_Delta_beta_total_abs", "finite beta vector row"),
        ("SRC2920_05_2895_eh_nohair", SRC_EH_NOHAIR_2895, "NH2895_4_source_mass;NH2895_6_verdict", "EH/no-hair attempt blocks beta import"),
        ("SRC2920_06_2895_r11_beta", SRC_R11_BETA_2895, "R11B2895_0_source_normalization;R11B2895_5_total_R11_beta_abs", "R11 beta operator family rows"),
        ("SRC2920_07_2896_beta_env", SRC_BETA_ENV_2896, "ENV2896_0_Newton_precondition;ENV2896_7_q_loc_alpha3_guard", "beta envelope and alpha3 leakage guard"),
        ("SRC2920_08_2896_newton_gate", SRC_NEWTON_GATE_2896, "NG2896_1_measured_GM;NG2896_5_precondition_verdict", "source-normalized Newton precondition gate"),
        ("SRC2920_09_2897_source_operator", SRC_SOURCE_OPERATOR_2897, "SNO2897_0_source_normalization_operator;MISSING_NUMERIC_OR_THEOREM_ZERO_COEFFICIENT", "source-normalization operator placeholder"),
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


def square_law_audit_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SQA2920_0_ppn_extraction_law",
            "PPN beta extraction in measured-U convention",
            "g_00=-1+2 A_source W/c^2 - 2 B_source W^2/c^4; U=A_source W; beta_eff=B_source/A_source^2",
            "PASS_KINEMATIC_FROM_2893",
            "the comparison formula is owned; this does not set beta_eff=1",
            True,
        ),
        (
            "SQA2920_1_parent_W_single_source",
            "one parent weak-field potential W before readout",
            "W sourced by the same Hilbert/local source charge used at first and second order",
            "UNSIGNED",
            "needed to stop first-order source calibration splitting from second-order source response",
            False,
        ),
        (
            "SQA2920_2_measured_U_fixed_first",
            "measured Newtonian potential fixed before PPN beta comparison",
            "U=A_source W with A_source nonzero and fixed, not refitted at O(U^2)",
            "PARTIAL_GUARD_ONLY",
            "current rows keep the measured-GM absorption explicit but do not prove the source identity",
            False,
        ),
        (
            "SQA2920_3_parent_square_source",
            "parent second-order source coefficient squares the first-order coefficient",
            "B_source=A_source^2",
            "NOT_DERIVED",
            "this is the desired clean GR-reduction theorem and is not present in the corpus yet",
            False,
        ),
        (
            "SQA2920_4_no_eh_smuggling",
            "Schwarzschild/EH beta=1 not imported as an axiom",
            "EH control lane can show what must be recovered but cannot replace a parent MTS proof",
            "PASS_GUARD",
            "keeps the branch honest: GR is the limit to derive, not a magic patch",
            True,
        ),
        (
            "SQA2920_5_no_r11_operator_hair",
            "no R11/non-EH operator contributes to the O(U^2) beta row",
            "sum_abs(delta_beta_source_R11, delta_beta_R2_fR, delta_beta_boundary_domain, delta_beta_scalar_class, delta_beta_readout_connection)=0",
            "UNSIGNED",
            "R11B2895 rows are templates/nonclaim, not zeros",
            False,
        ),
        (
            "SQA2920_6_newton_precondition",
            "measured orbital mu equals parent Hilbert source charge with no derivative hair",
            "mu_obs=G0 M_H and epsilon_SN=0 through charge-current/Gauss/orbital source-current scorecard",
            "FAIL_CLOSED_FROM_2896",
            "without this, beta can be contaminated by source-normalization rather than gravity itself",
            False,
        ),
        (
            "SQA2920_7_boundary_domain_readout",
            "boundary/domain/readout transfer silent through O(U^2)",
            "delta_beta_boundary_domain=delta_beta_readout=0",
            "UNSIGNED",
            "the stationary q_loc win does not prove second-order metric readout silence",
            False,
        ),
        (
            "SQA2920_8_verdict",
            "current parent square-law theorem for local beta",
            "B_source=A_source^2 in the observed-U convention",
            "PARENT_SQUARE_LAW_NOT_PROVED_BETA_NONCLAIM",
            "proceed to source-normalized Newton/Gauss/orbital scorecard and parent source-mass identity",
            False,
        ),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "clause": clause,
                "math_form": math_form,
                "current_status": status,
                "meaning": meaning,
                "clause_passed": passed,
                "source_paths": f"{SRC_BETA_LAW_2893};{SRC_EH_NOHAIR_2895};{SRC_NEWTON_GATE_2896}",
            }
        )
        for audit_id, clause, math_form, status, meaning, passed in specs
    ]


def beta_kernel_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "B2K2920_0_delta_beta_source",
            "delta_beta_source",
            "B_source/A_source^2 - 1",
            "MISSING_A_SOURCE_B_SOURCE_OR_PARENT_SQUARE_THEOREM",
            "derive B_source=A_source^2 or provide numeric source-backed A_source/B_source",
            "dimensionless",
        ),
        (
            "B2K2920_1_delta_beta_operator",
            "delta_beta_operator_R11",
            "sum_abs(delta_beta_source_R11,delta_beta_R2_fR,delta_beta_boundary_domain,delta_beta_scalar_class,delta_beta_readout_connection)",
            "MISSING_R11_COMPONENT_VALUES_OR_EH_NOHAIR",
            "prove R11 no-hair or acquire finite component coefficients",
            "dimensionless",
        ),
        (
            "B2K2920_2_delta_beta_q_loc",
            "delta_beta_q_loc",
            "physical U2 projection of P_loc(nabla Gamma_eff - div Khat)",
            "PROVISIONAL_7.432631961576971e-06_NOT_SCORE_READY",
            "needs same U2 normalization and alpha3 projection guard before beta scoring",
            "dimensionless",
        ),
        (
            "B2K2920_3_delta_beta_boundary_domain",
            "delta_beta_boundary_domain",
            "boundary/domain/projector quadratic stress beta projection",
            "MISSING_BOUNDARY_DOMAIN_ZERO_OR_COEFFICIENT_MAP",
            "prove silence or provide coefficient map",
            "dimensionless",
        ),
        (
            "B2K2920_4_delta_beta_readout",
            "delta_beta_readout",
            "second-order source metric to observed isotropic PPN readout mismatch",
            "MISSING_SAME_READOUT_THEOREM_THROUGH_O_U2",
            "derive observed coframe/readout transfer through second order",
            "dimensionless",
        ),
        (
            "B2K2920_5_epsilon_SN",
            "epsilon_SN",
            "(mu_obs - G_eff M_H)/(G_eff M_H)",
            "MISSING_GAUSS_ORBITAL_SOURCE_CURRENT_SCORECARD",
            "acquire/derive source-normalized Newton, Gauss, and orbital mass identity",
            "dimensionless",
        ),
        (
            "B2K2920_6_Delta_beta_total_abs",
            "Delta_beta_total_abs",
            "sum_abs(delta_beta_source,delta_beta_operator_R11,delta_beta_q_loc,delta_beta_boundary_domain,delta_beta_readout,epsilon_SN)",
            "TOTAL_BETA_NOT_SCORE_READY",
            "all heads need numeric sourced values or parent-signed zeros; no cancellation credit",
            "dimensionless",
        ),
    ]
    return [
        add_common(
            {
                "kernel_id": kernel_id,
                "symbol": symbol,
                "formula_or_map": formula,
                "current_status": status,
                "next_requirement": requirement,
                "units": units,
                "beta_bound_abs": "7.8e-05",
                "source_paths": f"{SRC_BETA_VECTOR_2893};{SRC_R11_BETA_2895};{SRC_BETA_ENV_2896};{SRC_NEWTON_GATE_2896}",
            }
        )
        for kernel_id, symbol, formula, status, requirement, units in specs
    ]


def newton_queue_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "NGQ2920_0_parent_source_mass_identity",
            "mu_obs = G0 M_H = G_eff M_source_parent",
            "MISSING_PARENT_SOURCE_MASS_IDENTITY",
            "derive the source charge from the parent matter action and show it is the observed orbital mass",
        ),
        (
            "NGQ2920_1_gauss_law_scorecard",
            "surface flux integral equals parent Hilbert source charge",
            "MISSING_GAUSS_LAW_SOURCE_CURRENT_SCORECARD",
            "write the finite local Gauss/orbital scorecard rows with source paths and units",
        ),
        (
            "NGQ2920_2_charge_current_silence",
            "non-Hilbert charge/current/source-shadow components vanish or are bounded",
            "MISSING_CHARGE_CURRENT_SILENCE",
            "connect Noether exchange collapse to a local source-current zero theorem or numeric residuals",
        ),
        (
            "NGQ2920_3_derivative_hair",
            "no time/range/radial/species/frame/domain derivative of measured mu",
            "MISSING_DERIVATIVE_HAIR_ZERO",
            "prove or bound d_t mu, d_r mu, species/source-frame dependence, and domain shifts",
        ),
        (
            "NGQ2920_4_second_order_square_law",
            "B_source=A_source^2 after the same source normalization",
            "MISSING_PARENT_SQUARE_LAW",
            "derive second-order field equation in the source-normalized weak-field family",
        ),
        (
            "NGQ2920_5_scorecard_verdict",
            "source-normalized Newton/Gauss/orbital precondition for beta/local GR",
            "BLOCKED_NONCLAIM",
            "2921 should target this instead of pretending beta is closed",
        ),
    ]
    return [
        add_common(
            {
                "queue_id": queue_id,
                "target": target,
                "current_status": status,
                "next_action": action,
                "source_paths": f"{SRC_NEWTON_GATE_2896};{SRC_SOURCE_OPERATOR_2897}",
            }
        )
        for queue_id, target, status, action in specs
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2920_0_beta_square_law", "B_source=A_source^2 is derived", "BLOCKED_NONCLAIM", "parent square-law clause is not signed", False),
        ("CG2920_1_beta_ppn_pass", "PPN beta passes 7.8e-05", "BLOCKED_NONCLAIM", "Delta_beta_total_abs is not numeric or theorem-zero", False),
        ("CG2920_2_newton_source_normalized", "source-normalized Newton/Gauss/orbital precondition passes", "BLOCKED_NONCLAIM", "2896 precondition remains FAIL_CLOSED", False),
        ("CG2920_3_local_GR", "local GR follows from current branch", "BLOCKED_NONCLAIM", "beta, alpha3, source-normalization, readout, and boundary/domain heads remain open", False),
        ("CG2920_4_public_or_github", "public/GitHub claim can be made from 2920", "BLOCKED_NONCLAIM", "private checkpoint only", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": status,
                "reason": reason,
                "gate_pass": gate_pass,
            }
        )
        for gate_id, claim, status, reason, gate_pass in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2920_0_keep_law",
            "retain beta_eff=B_source/A_source^2 as the exact extraction law",
            "the law is kinematic and useful, already derived from measured-U substitution",
            "use it as the beta grammar for all local-GR scorecards",
        ),
        (
            "DEC2920_1_no_square_claim",
            "do not claim beta_eff=1",
            "B_source=A_source^2 is not parent-derived and EH/no-hair import remains closure-only",
            "keep beta nonclaim",
        ),
        (
            "DEC2920_2_next",
            "move to source-normalized Newton/Gauss/orbital scorecard",
            "without mu_obs=G0 M_H and source-current identity, A_source and B_source cannot be physically scored",
            "select 2921 parent source-mass identity / scorecard acquisition",
        ),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": action,
            }
        )
        for decision_id, decision, because, action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2920_0_2921",
                "selection_status": "selected_primary",
                "target_file": "2921-Y5-R2FR-source-normalized-Newton-Gauss-orbital-scorecard-or-parent-source-mass-identity-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_source_normalized_Newton_Gauss_orbital_scorecard_or_parent_source_mass_identity_under_AX1090_2921.py",
                "task": "prove mu_obs=G0 M_H equals the parent Hilbert/source charge with no derivative hair, or build finite source-backed Newton/Gauss/orbital scorecard rows",
                "success_condition": "source-normalized Newton precondition passes and gives sourced A_source/B_source inputs, or all residual heads remain explicit finite nonclaim rows",
                "fallback_condition": "keep beta nonclaim and move to second-order readout/coframe or R11 no-hair acquisition",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    copies = [
        ("square_audit_copy", OUTPUTS["square_audit"], BRANCH_OUTPUTS["square_audit_copy"]),
        ("beta_kernel_copy", OUTPUTS["beta_kernel"], BRANCH_OUTPUTS["beta_kernel_copy"]),
        ("newton_queue_copy", OUTPUTS["newton_queue"], BRANCH_OUTPUTS["newton_queue_copy"]),
    ]
    rows = []
    for copy_id, source_path, destination_path in copies:
        shutil.copyfile(source_path, destination_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source_path),
                    "destination_path": str(destination_path),
                    "source_exists": source_path.exists(),
                    "destination_exists": destination_path.exists(),
                    "destination_parses": csv_parses(destination_path),
                }
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    square_rows: list[dict[str, Any]],
    beta_rows: list[dict[str, Any]],
    queue_rows: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    include_doc_check: bool,
) -> list[dict[str, Any]]:
    generated_csvs = [*OUTPUTS.values()]
    if not include_doc_check:
        generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]

    rows = [
        {
            "validation_id": "VAL2920_0_source_paths_exist",
            "status": all(bool(row["path_exists"]) for row in source_rows),
            "detail": "all cited source paths exist",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2920_1_source_anchors_found",
            "status": all(bool(row["anchors_found"]) for row in source_rows),
            "detail": "all source anchors found",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2920_2_csv_outputs_parse",
            "status": all(csv_parses(path) for path in generated_csvs),
            "detail": "generated CSV outputs parse cleanly",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2920_3_ppn_extraction_law_retained",
            "status": any(row["audit_id"] == "SQA2920_0_ppn_extraction_law" and bool(row["clause_passed"]) for row in square_rows),
            "detail": "beta_eff=B_source/A_source^2 retained as extraction law",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2920_4_square_law_not_claimed",
            "status": any(row["audit_id"] == "SQA2920_8_verdict" and "NOT_PROVED" in row["current_status"] for row in square_rows),
            "detail": "parent square law remains unproved and nonclaim",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2920_5_beta_kernel_complete",
            "status": {row["symbol"] for row in beta_rows}
            == {
                "delta_beta_source",
                "delta_beta_operator_R11",
                "delta_beta_q_loc",
                "delta_beta_boundary_domain",
                "delta_beta_readout",
                "epsilon_SN",
                "Delta_beta_total_abs",
            },
            "detail": "all required beta heads are present",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2920_6_newton_queue_complete",
            "status": len(queue_rows) >= 6 and any(row["queue_id"] == "NGQ2920_5_scorecard_verdict" for row in queue_rows),
            "detail": "Newton/Gauss/orbital acquisition queue present",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2920_7_claim_gates_safe",
            "status": all(not bool(row["gate_pass"]) and not bool(row["valid_for_claim"]) for row in claim_rows_),
            "detail": "no claim gate is open",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2920_8_next_target_selected",
            "status": any(row["route_id"] == "NEXT2920_0_2921" for row in next_rows_),
            "detail": "2921 source-normalized Newton/Gauss/orbital target selected",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2920_9_branch_copies_parse",
            "status": all(bool(row["destination_exists"]) and bool(row["destination_parses"]) for row in branch_rows_),
            "detail": "branch copies exist and parse",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2920_10_no_formalization_outputs",
            "status": not any(is_under(path, FORMALIZATION) for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]),
            "detail": "no generated output path is inside formalization-workbench",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
        {
            "validation_id": "VAL2920_11_doc_written",
            "status": DOC.exists() if include_doc_check else True,
            "detail": "markdown checkpoint exists",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        },
    ]
    rows.append(
        {
            "validation_id": "VAL2920_OVERALL",
            "status": all(bool(row["status"]) for row in rows),
            "detail": "2920 validation overall",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    square_rows: list[dict[str, Any]],
    beta_rows: list[dict[str, Any]],
    queue_rows: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2920_OVERALL")
    text = f"""# 2920 - Y5/R2FR Beta Source-Normalization Second-Order Kernel Or Parent Square Law Under AX1090

Status: `Y5_R2FR_2920_beta_square_law_not_proved_source_normalized_newton_2921_next`

Claim ceiling: `beta_extraction_law_yes_parent_square_law_no_no_local_GR_no_Newton_no_PPN_no_R10_no_GitHub_claim`

Generated UTC: `{RUN_UTC}`

## Summary

2920 takes the clean beta route. The exact source-normalized PPN extraction law is retained:

`beta_eff = B_source/A_source^2`

so the local GR beta requirement is:

`delta_beta_source = B_source/A_source^2 - 1 = 0`

equivalently:

`B_source = A_source^2`.

That is the right target because it asks whether the second-order source response is forced by the same parent structure that fixes the first-order Newtonian response. This is the GR-reduction question in a sharp form, not a fit-quality question.

The result is not a closure. The extraction law is derived, but the parent square law is not. The current corpus still lacks a signed proof that the measured orbital source normalization, the Hilbert/source charge, the boundary/domain transfer, the R11/non-EH operator sector, and the observed readout frame all stay silent through `O(U^2)`.

So 2920 does not claim beta. It converts the obstruction into the next best target: source-normalized Newton/Gauss/orbital source-mass identity.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "anchors_found", "role", "missing_anchors"])}

## Parent Square-Law Audit

{md_table(square_rows, ["audit_id", "clause", "math_form", "current_status", "meaning", "clause_passed", "valid_for_claim"])}

## Beta Second-Order Source-Normalization Kernel

{md_table(beta_rows, ["kernel_id", "symbol", "formula_or_map", "current_status", "next_requirement", "beta_bound_abs", "valid_for_claim"])}

## Source-Normalized Newton/Gauss/Orbital Queue

{md_table(queue_rows, ["queue_id", "target", "current_status", "next_action", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows_, ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"])}

## Decision Ledger

{md_table(decision_rows_, ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Next Target

{md_table(next_rows_, ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows_, ["copy_id", "source_path", "destination_path", "destination_exists", "destination_parses", "valid_for_claim"])}

## Validation

{md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim"])}

Validation overall: `{overall["status"]}`.

## Interpretation

This is a useful narrowing, not a defeat. We now know the local beta branch cannot be responsibly closed by saying "GR has beta=1" or by absorbing first-order gravity into measured `GM`. The required theorem is more specific:

`B_source=A_source^2` in the same observed-`U` convention, after the parent source charge is shown to be the measured orbital source and all non-EH/readout/boundary/domain beta heads are zero or finite-bounded.

That makes the next move concrete. Before scoring beta, prove or source the Newton/Gauss/orbital identity:

`mu_obs = G0 M_H`

with no derivative hair, no source-shadow current, no range/time/domain dependence, and no second-order readout mismatch.

## Not Claimed

- no parent square law is claimed;
- no beta `7.8e-05` PPN pass is claimed;
- no source-normalized Newton/Gauss/orbital pass is claimed;
- no R11/EH no-hair theorem is claimed;
- no local-GR/Newton/PPN/R10/WEP/clock/orbital pass is claimed;
- no file in `formalization-workbench` is modified by this checkpoint;
- no public/GitHub action is implied.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    square_rows = square_law_audit_rows()
    beta_rows = beta_kernel_rows()
    queue_rows = newton_queue_rows()
    claim_rows_ = claim_rows()
    decision_rows_ = decision_rows()
    next_rows_ = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["square_audit"], square_rows)
    write_csv(OUTPUTS["beta_kernel"], beta_rows)
    write_csv(OUTPUTS["newton_queue"], queue_rows)
    write_csv(OUTPUTS["claims"], claim_rows_)
    write_csv(OUTPUTS["decision"], decision_rows_)
    write_csv(OUTPUTS["next"], next_rows_)

    branch_rows_ = branch_rows()
    write_csv(OUTPUTS["branches"], branch_rows_)

    validation_rows_ = validation_rows(
        source_rows,
        square_rows,
        beta_rows,
        queue_rows,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=False,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        square_rows,
        beta_rows,
        queue_rows,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    validation_rows_ = validation_rows(
        source_rows,
        square_rows,
        beta_rows,
        queue_rows,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=True,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        square_rows,
        beta_rows,
        queue_rows,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2920_OVERALL")
    if not bool(overall["status"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
