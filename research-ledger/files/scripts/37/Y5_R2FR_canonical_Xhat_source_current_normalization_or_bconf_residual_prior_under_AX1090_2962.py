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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
WEP_SOURCES = ROOT / "source-intake" / "wep-sources"
BETA_SOURCE = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2962"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2962-Y5-R2FR-canonical-Xhat-source-current-normalization-or-bconf-residual-prior-under-AX1090.md"

SRC_2961_DOC = ROOT / "2961-Y5-R2FR-bconf-branch-selector-closure-debt-or-residual-smoke-runner-under-AX1090.md"
SRC_2961_NEXT = RESIDUALS / "P8_Y5_R2FR_2961_NEXT_TARGET.csv"
SRC_2961_SELECTOR = RESIDUALS / "P8_Y5_R2FR_2961_BCONF_BRANCH_SELECTOR.csv"
SRC_2961_RESIDUAL = RESIDUALS / "P8_Y5_R2FR_2961_RESIDUAL_BRANCH_NONCLAIM.csv"
SRC_2961_SMOKE = RESIDUALS / "P8_Y5_R2FR_2961_SMOKE_RUNNER_STATUS.csv"
SRC_2954_FIELD = RESIDUALS / "P8_Y5_R2FR_2954_FIELD_SPACE_LAW_AUDIT.csv"
SRC_2953_BETA = PARENT_ACTION / "field_space_beta_blocker_2953_NONCLAIM.csv"
SRC_2951_COEFF = PARENT_ACTION / "ZX_MX2_source_row_attempt_2951_BLOCKED.csv"
SRC_2951_OWNER = PARENT_ACTION / "parent_X_owner_contract_2951_NONCLAIM.csv"
SRC_GLOBAL_COUPLING = RESIDUALS / "P8_global_coupling_superselection_CONTRACT.csv"
SRC_FIELD_QUEUE = RESIDUALS / "P8_FIELD_SPECIFIC_SILENCE_QUEUE.csv"
SRC_2676_OWNER = WEP_SOURCES / "action_scale_measure_owner_wip_nonclaim_2676.csv"
SRC_2677_GRAMMAR = WEP_SOURCES / "no_species_action_weight_object_language_wip_2677.csv"
SRC_2774_OWNER = BETA_SOURCE / "ACTION_SCALE_OWNER_2774_NONCLAIM.csv"
SRC_2916_PRODUCT = PARENT_ACTION / "Cg_invariant_source_test_product_law_2916_NONCLAIM.csv"
SRC_1920_CURRENT = SOURCE_WEIGHT / "SOURCE_WEIGHT_PARENT_CURRENT_OWNER_PROOF_1920_NONCLAIM.csv"
SRC_2661_R10 = SOURCE_WEIGHT / "R10_PROJECTION_2661_NONCLAIM.csv"
SRC_2673_QBAR = SOURCE_WEIGHT / "QBARXT_FIRST_COEFFICIENT_TEMPLATE_2673_NONCLAIM.csv"
SRC_LOCAL_BOUNDS = LOCAL_BOUNDS / "local_bound_claims.csv"
SRC_R10_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2962_SOURCE_REGISTER.csv",
    "xhat_gate": RESIDUALS / "P8_Y5_R2FR_2962_CANONICAL_XHAT_NORMALIZATION_GATE.csv",
    "current_gate": RESIDUALS / "P8_Y5_R2FR_2962_SOURCE_TEST_CURRENT_OWNER_GATE.csv",
    "prior": RESIDUALS / "P8_Y5_R2FR_2962_BCONF_RESIDUAL_PRIOR_INTAKE_NONCLAIM.csv",
    "projection": RESIDUALS / "P8_Y5_R2FR_2962_PROJECTION_INTAKE_ROWS_NONCLAIM.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2962_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2962_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2962_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2962_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2962_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "gate_copy": PARENT_ACTION / "canonical_Xhat_source_current_gate_2962_NOT_DERIVED.csv",
    "prior_copy": LOCAL_BOUNDS / "bconf_prior_projection_intake_2962_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2962_XHAT_ZX_MX2_SOURCE_CURRENT_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


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
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2962_00_2961_doc", SRC_2961_DOC, "NEXT2961_0_2962;Validation overall: `True`", "2961 handoff"),
        ("SRC2962_01_2961_next", SRC_2961_NEXT, "NEXT2961_0_2962", "machine-readable 2962 target"),
        ("SRC2962_02_2961_selector", SRC_2961_SELECTOR, "SEL2961_0_closure_debt;SEL2961_1_residual", "b_conf branch selector"),
        ("SRC2962_03_2961_residual", SRC_2961_RESIDUAL, "RES2961_0_b_conf;RES2961_6_B_conf_envelope", "finite residual branch rows"),
        ("SRC2962_04_2961_smoke", SRC_2961_SMOKE, "SMOKE2961_3_expected", "2961 smoke runner"),
        ("SRC2962_05_2954_field", SRC_2954_FIELD, "LAW2954_2_canonical_metric_contract;LAW2954_6_verdict", "field-space law and normalization blocker"),
        ("SRC2962_06_2953_beta", SRC_2953_BETA, "BETA2953_1_field_metric;BETA2953_4_verdict", "field metric beta blocker"),
        ("SRC2962_07_2951_coeff", SRC_2951_COEFF, "COEFF2951_4_lambdaX;COEFF2951_5_candidate_row", "Z_X/M_X^2/lambda_X blocked row"),
        ("SRC2962_08_2951_owner", SRC_2951_OWNER, "OWN2951_3_field_normalization;OWN2951_5_MX2_owner", "parent X owner contract"),
        ("SRC2962_09_global_coupling", SRC_GLOBAL_COUPLING, "GS4_no_range_radial_time_dependence;GS7_scalar_branch_fallback", "global coupling/source normalization contract"),
        ("SRC2962_10_field_queue", SRC_FIELD_QUEUE, "source_measure_and_Meff_flux;motion_time_flow_modes", "field-specific silence queue"),
        ("SRC2962_11_2676_owner", SRC_2676_OWNER, "OWN2676_0_parent_owner_target;OWN2676_4_verdict", "action scale/current owner"),
        ("SRC2962_12_2677_grammar", SRC_2677_GRAMMAR, "GRM2677_0_single_action_density_line;GRM2677_6_verdict", "no species action-weight grammar"),
        ("SRC2962_13_2774_owner", SRC_2774_OWNER, "ASO2774_0_target;ASO2774_5_verdict", "action-scale owner obstruction"),
        ("SRC2962_14_2916_product", SRC_2916_PRODUCT, "LAW2916_0_point_source;LAW2916_1_two_body_exchange", "conditional source/test product law"),
        ("SRC2962_15_1920_current", SRC_1920_CURRENT, "SWP1920_2_common_measure_current;SWP1920_5_verdict", "source-weight current owner proof"),
        ("SRC2962_16_2661_r10", SRC_2661_R10, "R10P2661_3_Qbar_XH", "R10 projection missing source charge"),
        ("SRC2962_17_2673_qbar", SRC_2673_QBAR, "QXT2673_0_qbarXT;QXT2673_3_alpha_feed", "qbarXT coefficient template"),
        ("SRC2962_18_local_bounds", SRC_LOCAL_BOUNDS, "R1_WEP_source_charge;R2_clock_redshift;R3_gamma", "local bounds"),
        ("SRC2962_19_r10_curve", SRC_R10_CURVE, "R10_VECTOR_2020_REVIEW_0000;review_candidate_only", "R10 nonclaim curve"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def xhat_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "XHAT2962_0_field_identity",
            "parent Xhat identity",
            "choose one parent-owned finite local mode X and define Xhat = X/f_X or canonical Xhat = sqrt(Z_X)X in the same action normalization",
            "NOT_PARENT_SELECTED",
            "2951 says the X field identity and parent action block are not selected",
            False,
        ),
        (
            "XHAT2962_1_field_metric",
            "canonical field-space metric",
            "Z_X f_X^2 or equivalent parent field metric fixes the conversion between X coordinate and physical charge",
            "MISSING_FIELD_METRIC_OWNER",
            "2954 has a clean contract but not a signed owner",
            False,
        ),
        (
            "XHAT2962_2_mass_range",
            "lambda_X",
            "lambda_X=sqrt(Z_X/M_X^2) with Z_X and M_X^2 source-backed in the same normalization",
            "BLOCKED_BY_ZX_MX2",
            "2951 keeps Z_X, M_X^2, mass gap and lambda_X formula-only",
            False,
        ),
        (
            "XHAT2962_3_rescaling_guard",
            "rescaling guard",
            "b_conf and tau maps must be invariant under X -> aX by transforming charges and Z_X together",
            "GUARDRAIL_ONLY",
            "prevents fake wins but does not source a number",
            False,
        ),
        (
            "XHAT2962_4_verdict",
            "canonical Xhat package",
            "XHAT2962_0 through XHAT2962_3 close in one parent branch",
            "CANONICAL_XHAT_NOT_DERIVED",
            "finite b_conf branch cannot score until Xhat/lambda normalization is owned",
            False,
        ),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "object": obj,
                "required_statement": statement,
                "current_status": status,
                "evidence_summary": evidence,
                "owner_acquired": acquired,
            }
        )
        for gate_id, obj, statement, status, evidence, acquired in rows
    ]


def current_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CUR2962_0_common_action_line",
            "one ordinary matter action-density/current owner",
            "one parent action/measure/current normalization applies to all ordinary source/test sectors before field equations and readout",
            "CONTRACT_TARGET_NOT_SIGNED",
            "2676/2677/2774 state the right object language but mark it unsigned",
            False,
        ),
        (
            "CUR2962_1_source_test_charges",
            "source/test beta charges",
            "beta_A := partial_Xhat ln m_A^eff or equivalent source/test charge is defined in the same Xhat normalization",
            "CONDITIONAL_STANDARD_VARIATION",
            "2916 gives the product law only after parent Xhat and matter/source definition",
            False,
        ),
        (
            "CUR2962_2_no_species_weight",
            "no species/source-only weights",
            "w_A, hbar_A, J_A, c_A and zeta_A are absent or theorem-zero before source normalization",
            "NOT_PARENT_DERIVED",
            "source-weight/current owner proofs retain finite Delta w_A/c_A rows",
            False,
        ),
        (
            "CUR2962_3_hilbert_source_equality",
            "Hilbert/source current equality",
            "observed source charge equals parent Hilbert current with no non-Hilbert, boundary, marker or readout tails",
            "MISSING_SOURCE_CURRENT_OWNER",
            "same wound appears in WEP, R10, Newton and PPN rows",
            False,
        ),
        (
            "CUR2962_4_verdict",
            "source/test current package",
            "CUR2962_0 through CUR2962_3 close in one parent branch",
            "SOURCE_TEST_CURRENT_OWNER_NOT_DERIVED",
            "finite b_conf residual remains a named nonclaim row, not a score",
            False,
        ),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "object": obj,
                "required_statement": statement,
                "current_status": status,
                "evidence_summary": evidence,
                "owner_acquired": acquired,
            }
        )
        for gate_id, obj, statement, status, evidence, acquired in rows
    ]


def prior_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PRIOR2962_0_b_conf_prior",
            "b_conf",
            "dimensionless",
            "finite hidden conformal-frame coefficient in canonical Xhat units",
            "MISSING_PRIOR_OR_THEOREM_ZERO",
            "allowed sources: parent theorem-zero; explicit closure-debt flag; external prior clearly marked phenomenological; fit value from future smoke run",
        ),
        (
            "PRIOR2962_1_Xhat_norm",
            "N_Xhat",
            "field_normalization",
            "canonical mapping from corpus X coordinate to Xhat",
            "MISSING_ZX_FX_OWNER",
            "requires field metric/sign/unit owner",
        ),
        (
            "PRIOR2962_2_lambda_X",
            "lambda_X",
            "length",
            "finite range for b_conf exchange branch",
            "MISSING_ZX_MX2_SAME_NORMALIZATION",
            "requires Z_X and M_X^2 source-backed in same branch",
        ),
        (
            "PRIOR2962_3_beta_source_test",
            "beta_source_conf;beta_test_conf",
            "dimensionless",
            "source/test charges beta_A=tau_A b_conf in canonical Xhat units",
            "MISSING_SOURCE_TEST_CHARGES",
            "requires common source current owner and no species/source weights",
        ),
        (
            "PRIOR2962_4_prior_policy",
            "b_conf_prior_policy",
            "policy",
            "no cancellation and no promotion from placeholders",
            "POLICY_READY_VALUES_MISSING",
            "future runner may test placeholders but must keep valid_for_claim=false",
        ),
    ]
    source_path = ";".join(str(path) for path in [SRC_2961_RESIDUAL, SRC_2954_FIELD, SRC_2951_COEFF, SRC_2676_OWNER, SRC_2916_PRODUCT])
    return [
        add_common(
            {
                "row_id": row_id,
                "symbol": symbol,
                "units": units,
                "definition": definition,
                "numeric_or_theorem_value": value,
                "intake_policy": policy,
                "source_path": source_path,
                "source_path_exists": all(Path(path).exists() for path in source_path.split(";")),
                "accepted_for_scoring": False,
                "no_cancellation_policy": True,
            }
        )
        for row_id, symbol, units, definition, value, policy in rows
    ]


def projection_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PROJ2962_0_R10",
            "alpha_R10_conf(lambda)",
            "dimensionless",
            "alpha_R10_conf = K_R10(lambda_X) beta_source_conf beta_test_conf + alpha_tail_abs",
            "MISSING_K_R10_BETA_SOURCE_BETA_TEST_LAMBDA",
            "R10_alpha_lambda;finite_range_Newton",
        ),
        (
            "PROJ2962_1_PPN",
            "gamma_minus_1_conf",
            "dimensionless",
            "gamma_minus_1_conf = Pi_gamma[metric response from b_conf branch]",
            "MISSING_WEAK_FIELD_METRIC_MAP",
            "PPN_gamma",
        ),
        (
            "PROJ2962_2_clock",
            "clock_conf",
            "dimensionless",
            "clock_conf = tau_clock_conf b_conf Delta Xhat_local",
            "MISSING_LOCAL_PROFILE_CLOCK_FRAME",
            "clock_redshift;clock_ratios",
        ),
        (
            "PROJ2962_3_source",
            "source_conf",
            "dimensionless",
            "source_conf = tau_source_conf b_conf Delta Xhat_source",
            "MISSING_SOURCE_CURRENT_OWNER",
            "WEP_source_charge;measured_GM",
        ),
        (
            "PROJ2962_4_joint",
            "B_conf_envelope",
            "dimensionless",
            "B_conf = min_i B_i/|tau_i| over sourced arenas without cancellation",
            "MISSING_ALL_TAU_VALUES",
            "joint_local_bound",
        ),
    ]
    source_path = ";".join(str(path) for path in [SRC_2961_RESIDUAL, SRC_2661_R10, SRC_2673_QBAR, SRC_LOCAL_BOUNDS, SRC_R10_CURVE])
    return [
        add_common(
            {
                "projection_id": projection_id,
                "symbol": symbol,
                "units": units,
                "formula_or_requirement": formula,
                "current_status": status,
                "observable_links": links,
                "source_path": source_path,
                "source_path_exists": all(Path(path).exists() for path in source_path.split(";")),
                "ready_for_smoke": False,
                "accepted_for_scoring": False,
            }
        )
        for projection_id, symbol, units, formula, status, links in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2962_0_Xhat", "canonical Xhat normalization derived", False, "FIELD_METRIC_ZX_MX2_OWNER_MISSING"),
        ("CG2962_1_current", "source/test current owner derived", False, "COMMON_CURRENT_SOURCE_WEIGHT_OWNER_MISSING"),
        ("CG2962_2_prior", "b_conf prior/projection rows score-ready", False, "VALUES_PLACEHOLDER_NONCLAIM"),
        ("CG2962_3_R10_PPN_clock", "R10/PPN/clock smoke run allowed for evidence", False, "VALID_MTS_ROWS_ZERO"),
        ("CG2962_4_local_GR", "local GR/Newton reduction allowed", False, "NO_LOCAL_GR_CLAIM"),
        ("CG2962_5_public", "public claim allowed", False, "PRIVATE_NONCLAIM_CHECKPOINT"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2962_0_Xhat",
            "canonical Xhat normalization is not derived",
            "field metric, Z_X/M_X^2 and lambda_X remain formula-only or owner-missing",
            "keep finite b_conf branch nonclaim",
        ),
        (
            "DEC2962_1_current",
            "source/test current owner is not derived",
            "ordinary matter common-current/source-weight owner remains a shared blocker for WEP, R10, Newton and PPN",
            "retain beta_source/beta_test as missing rows",
        ),
        (
            "DEC2962_2_intake",
            "b_conf prior/projection intake rows are now explicit",
            "the residual branch can now accept future theorem-zero, prior, or fit values without changing claim policy",
            "runner can be built but must reject placeholders",
        ),
        (
            "DEC2962_3_next",
            "next target should build a placeholder-refusal smoke runner",
            "this tests schema and prevents accidental promotion before the hard owners close",
            "build 2963 b_conf residual placeholder-refusal runner",
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
        for decision_id, decision, because, action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2962_0_2963",
                "priority": "selected_primary",
                "next_doc": "2963-Y5-R2FR-bconf-residual-placeholder-refusal-smoke-runner-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_bconf_residual_placeholder_refusal_smoke_runner_under_AX1090_2963.py",
                "objective": "Build a nonclaim smoke runner for the finite b_conf residual branch that ingests the 2962 prior/projection rows, confirms placeholders are rejected, and only permits future scoring when Xhat, lambda_X, beta_source/test and tau maps are numeric or theorem-zero with source paths.",
                "include": "b_conf prior;Xhat normalization;lambda_X;beta_source_conf;beta_test_conf;tau_R10_conf;tau_PPN_gamma_conf;tau_clock_conf;tau_source_conf;placeholder refusal;claim gates",
                "exclude": "derive single-frame theorem again;b_marker full taxonomy;quotient/vertical no-pole rerun;beta prediction;direct lambda closure;I_X scoring;local-GR claim;public claim;formalization-workbench edits;GitHub action",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("gate_copy", OUTPUTS["xhat_gate"], BRANCH_OUTPUTS["gate_copy"]),
        ("prior_copy", OUTPUTS["prior"], BRANCH_OUTPUTS["prior_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        shutil.copyfile(source, target)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "copy_path": str(target),
                    "source_exists": source.exists(),
                    "copy_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    csv_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2962_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2962_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all cited source anchors found", True),
        ("VAL2962_2_Xhat_blocked", any(row["gate_id"] == "XHAT2962_4_verdict" and row["owner_acquired"] is False for row in all_rows["xhat_gate"]), "canonical Xhat remains not derived", True),
        ("VAL2962_3_current_blocked", any(row["gate_id"] == "CUR2962_4_verdict" and row["owner_acquired"] is False for row in all_rows["current_gate"]), "source/test current owner remains not derived", True),
        ("VAL2962_4_prior_nonclaim", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["prior"]), "prior intake rows remain nonclaim", True),
        ("VAL2962_5_prior_paths_exist", all(row["source_path_exists"] is True for row in all_rows["prior"]), "prior intake rows cite existing paths", True),
        ("VAL2962_6_projection_nonclaim", all(row["ready_for_smoke"] is False and row["valid_for_claim"] is False for row in all_rows["projection"]), "projection rows remain nonclaim/not smoke-ready", True),
        ("VAL2962_7_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates remain blocked", True),
        ("VAL2962_8_next_target_written", any(row["next_id"] == "NEXT2962_0_2963" for row in all_rows["next"]), "2963 next target selected", True),
        ("VAL2962_9_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2962_10_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2962_11_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2962_12_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2962 outputs were written to formalization-workbench", True),
        ("VAL2962_13_doc_written", DOC.exists(), "2962 markdown checkpoint exists", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    rows.append(add_common({"validation_id": "VAL2962_OVERALL", "passed": overall, "check": "2962 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2962 - Y5 R2FR: canonical Xhat/source-current normalization or bconf residual prior under AX1090

Status: `Y5_R2FR_2962_Xhat_source_current_not_derived_bconf_prior_projection_intake_emitted_nonclaim`

Claim ceiling: `no_canonical_Xhat_no_source_current_owner_no_bconf_score_no_R10_PPN_clock_score_no_local_GR_no_Newton_no_public_claim`

2962 tests whether the finite `b_conf` residual branch can be sourced. The result is:

- Canonical `Xhat` is not derived: field identity, field-space metric, `Z_X/M_X^2`, mass gap and `lambda_X` are still not parent-owned in one branch.
- Source/test current ownership is not derived: common action-scale, species-blind measure, Hilbert/source equality and no source-only weights remain unsigned.
- The useful progress is intake discipline: `b_conf`, `Xhat` normalization, `lambda_X`, source/test charges and arena projection rows are now explicit nonclaim placeholders.
- The next safe step is a placeholder-refusal smoke runner, not a physics claim.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Canonical Xhat Normalization Gate

{md_table(all_rows["xhat_gate"], ["gate_id", "object", "current_status", "owner_acquired", "evidence_summary"])}

## Source/Test Current Owner Gate

{md_table(all_rows["current_gate"], ["gate_id", "object", "current_status", "owner_acquired", "evidence_summary"])}

## b_conf Residual Prior Intake

{md_table(all_rows["prior"], ["row_id", "symbol", "numeric_or_theorem_value", "units", "accepted_for_scoring", "intake_policy"])}

## Projection Intake Rows

{md_table(all_rows["projection"], ["projection_id", "symbol", "current_status", "units", "ready_for_smoke", "observable_links"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(all_rows["branches"], ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "xhat_gate": xhat_gate_rows(),
        "current_gate": current_gate_rows(),
        "prior": prior_rows(),
        "projection": projection_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2962 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
