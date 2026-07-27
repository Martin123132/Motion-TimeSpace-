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
WEP_SOURCES = ROOT / "source-intake" / "wep-sources"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
BETA_SOURCE = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2964"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2964-Y5-R2FR-Xhat-ZX-MX2-lambda-or-source-current-first-value-under-AX1090.md"

SRC_2963_DOC = ROOT / "2963-Y5-R2FR-bconf-residual-placeholder-refusal-smoke-runner-under-AX1090.md"
SRC_2963_NEXT = RESIDUALS / "P8_Y5_R2FR_2963_NEXT_TARGET.csv"
SRC_2963_PROMOTION = RESIDUALS / "P8_Y5_R2FR_2963_PROMOTION_RULES.csv"
SRC_2963_REFUSAL = RESIDUALS / "P8_Y5_R2FR_2963_PLACEHOLDER_REFUSAL_ROWS.csv"
SRC_2963_SMOKE = RESIDUALS / "P8_Y5_R2FR_2963_SMOKE_RUNNER_STATUS.csv"
SRC_2962_PRIOR = RESIDUALS / "P8_Y5_R2FR_2962_BCONF_RESIDUAL_PRIOR_INTAKE_NONCLAIM.csv"
SRC_2962_PROJECTION = RESIDUALS / "P8_Y5_R2FR_2962_PROJECTION_INTAKE_ROWS_NONCLAIM.csv"
SRC_2962_XHAT = RESIDUALS / "P8_Y5_R2FR_2962_CANONICAL_XHAT_NORMALIZATION_GATE.csv"
SRC_2962_CURRENT = RESIDUALS / "P8_Y5_R2FR_2962_SOURCE_TEST_CURRENT_OWNER_GATE.csv"
SRC_2954_FIELD = RESIDUALS / "P8_Y5_R2FR_2954_FIELD_SPACE_LAW_AUDIT.csv"
SRC_2953_BETA = PARENT_ACTION / "field_space_beta_blocker_2953_NONCLAIM.csv"
SRC_2951_COEFF = PARENT_ACTION / "ZX_MX2_source_row_attempt_2951_BLOCKED.csv"
SRC_2951_OWNER = PARENT_ACTION / "parent_X_owner_contract_2951_NONCLAIM.csv"
SRC_2676_OWNER = WEP_SOURCES / "action_scale_measure_owner_wip_nonclaim_2676.csv"
SRC_2677_GRAMMAR = WEP_SOURCES / "no_species_action_weight_object_language_wip_2677.csv"
SRC_2774_OWNER = BETA_SOURCE / "ACTION_SCALE_OWNER_2774_NONCLAIM.csv"
SRC_2916_PRODUCT = PARENT_ACTION / "Cg_invariant_source_test_product_law_2916_NONCLAIM.csv"
SRC_1920_CURRENT = SOURCE_WEIGHT / "SOURCE_WEIGHT_PARENT_CURRENT_OWNER_PROOF_1920_NONCLAIM.csv"
SRC_2661_R10 = SOURCE_WEIGHT / "R10_PROJECTION_2661_NONCLAIM.csv"
SRC_2673_QBAR = SOURCE_WEIGHT / "QBARXT_FIRST_COEFFICIENT_TEMPLATE_2673_NONCLAIM.csv"
SRC_R10_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2964_SOURCE_REGISTER.csv",
    "x_payload": RESIDUALS / "P8_Y5_R2FR_2964_XHAT_ZX_MX2_LAMBDA_PAYLOAD_GATE.csv",
    "current_payload": RESIDUALS / "P8_Y5_R2FR_2964_SOURCE_CURRENT_PAYLOAD_GATE.csv",
    "first_slots": RESIDUALS / "P8_Y5_R2FR_2964_FIRST_VALUE_SLOTS_NONCLAIM.csv",
    "runner_update": RESIDUALS / "P8_Y5_R2FR_2964_RUNNER_UPDATE_ROWS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2964_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2964_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2964_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2964_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2964_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "x_payload_copy": PARENT_ACTION / "Xhat_ZX_MX2_lambda_payload_gate_2964_NOT_DERIVED.csv",
    "slot_copy": LOCAL_BOUNDS / "bconf_first_value_slots_2964_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2964_NXHAT_FIELD_METRIC_OR_SOURCE_CURRENT_NEXT_NONCLAIM.csv",
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
        ("SRC2964_00_2963_doc", SRC_2963_DOC, "NEXT2963_0_2964;Validation overall: `True`", "2963 handoff"),
        ("SRC2964_01_2963_next", SRC_2963_NEXT, "NEXT2963_0_2964", "machine-readable 2964 target"),
        ("SRC2964_02_2963_promotion", SRC_2963_PROMOTION, "PROM2963_0_b_conf;PROM2963_6_verdict", "promotion rules"),
        ("SRC2964_03_2963_refusal", SRC_2963_REFUSAL, "REF2963_1;REF2963_3", "placeholder refusal rows"),
        ("SRC2964_04_2963_smoke", SRC_2963_SMOKE, "SMOKE2963_3_expected", "smoke runner status"),
        ("SRC2964_05_2962_prior", SRC_2962_PRIOR, "PRIOR2962_1_Xhat_norm;PRIOR2962_3_beta_source_test", "b_conf prior intake"),
        ("SRC2964_06_2962_projection", SRC_2962_PROJECTION, "PROJ2962_0_R10;PROJ2962_4_joint", "projection intake rows"),
        ("SRC2964_07_2962_Xhat", SRC_2962_XHAT, "XHAT2962_2_mass_range;XHAT2962_4_verdict", "canonical Xhat gate"),
        ("SRC2964_08_2962_current", SRC_2962_CURRENT, "CUR2962_1_source_test_charges;CUR2962_4_verdict", "source/test current gate"),
        ("SRC2964_09_2954_field", SRC_2954_FIELD, "LAW2954_2_canonical_metric_contract;LAW2954_6_verdict", "field-space law"),
        ("SRC2964_10_2953_beta", SRC_2953_BETA, "BETA2953_1_field_metric;BETA2953_4_verdict", "field metric beta blocker"),
        ("SRC2964_11_2951_coeff", SRC_2951_COEFF, "COEFF2951_4_lambdaX;COEFF2951_5_candidate_row", "Z_X/M_X^2/lambda source row attempt"),
        ("SRC2964_12_2951_owner", SRC_2951_OWNER, "OWN2951_3_field_normalization;OWN2951_5_MX2_owner", "parent X owner contract"),
        ("SRC2964_13_2676_owner", SRC_2676_OWNER, "OWN2676_0_parent_owner_target;OWN2676_4_verdict", "common action/current owner"),
        ("SRC2964_14_2677_grammar", SRC_2677_GRAMMAR, "GRM2677_0_single_action_density_line;GRM2677_6_verdict", "no species action-weight grammar"),
        ("SRC2964_15_2774_owner", SRC_2774_OWNER, "ASO2774_0_target;ASO2774_5_verdict", "action-scale owner obstruction"),
        ("SRC2964_16_2916_product", SRC_2916_PRODUCT, "LAW2916_0_point_source;LAW2916_1_two_body_exchange", "conditional product law"),
        ("SRC2964_17_1920_current", SRC_1920_CURRENT, "SWP1920_2_common_measure_current;SWP1920_5_verdict", "source-current owner proof"),
        ("SRC2964_18_2661_r10", SRC_2661_R10, "R10P2661_3_Qbar_XH", "R10 projection missing source charge"),
        ("SRC2964_19_2673_qbar", SRC_2673_QBAR, "QXT2673_0_qbarXT;QXT2673_3_alpha_feed", "qbar source/test template"),
        ("SRC2964_20_r10_curve", SRC_R10_CURVE, "R10_VECTOR_2020_REVIEW_0000;review_candidate_only", "R10 nonclaim curve"),
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


def x_payload_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "XPL2964_0_parent_object",
            "X parent object",
            "one selected parent-owned physical finite mode X before readout",
            "NOT_PARENT_SELECTED",
            "2951 owner contract keeps X field identity and action block open",
            False,
        ),
        (
            "XPL2964_1_ZX",
            "Z_X",
            "positive kinetic/operator coefficient in declared units and branch",
            "FORMULA_ONLY_NOT_PARENT_SIGNED",
            "2951 gives formula-only, no parent sign/unit owner",
            False,
        ),
        (
            "XPL2964_2_MX2",
            "M_X^2",
            "positive Hessian/mass-gap coefficient in same normalization as Z_X",
            "FORMULA_ONLY_NOT_PARENT_SIGNED",
            "2951 keeps mass gap and zero-mode policy open",
            False,
        ),
        (
            "XPL2964_3_lambda",
            "lambda_X",
            "lambda_X=sqrt(Z_X/M_X^2) with Z_X and M_X^2 source-backed in one branch",
            "BLOCKED_BY_ZX_MX2",
            "lambda remains formula-only until Z/M close together",
            False,
        ),
        (
            "XPL2964_4_NXhat",
            "N_Xhat",
            "canonical normalization map from corpus X coordinate to Xhat",
            "MISSING_FIELD_METRIC_OWNER",
            "2954 has a clean metric contract but not parent ownership",
            False,
        ),
        (
            "XPL2964_5_verdict",
            "canonical Xhat/Z/M/lambda payload",
            "XPL2964_0 through XPL2964_4 all close with source paths",
            "XHAT_ZX_MX2_LAMBDA_NOT_DERIVED",
            "no finite-bconf score can be made from X payload yet",
            False,
        ),
    ]
    return [
        add_common(
            {
                "payload_id": payload_id,
                "symbol": symbol,
                "required_payload": payload,
                "current_status": status,
                "evidence_summary": evidence,
                "payload_acquired": acquired,
            }
        )
        for payload_id, symbol, payload, status, evidence, acquired in rows
    ]


def current_payload_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CURPL2964_0_current_owner",
            "common current owner",
            "single ordinary matter action-scale/measure/current owner before readout",
            "CONTRACT_TARGET_NOT_SIGNED",
            "2676/2677/2774 retain action-scale and current owner debt",
            False,
        ),
        (
            "CURPL2964_1_no_source_weight",
            "no source-only weights",
            "w_A, hbar_A, J_A, c_A, zeta_A absent or theorem-zero",
            "NOT_PARENT_DERIVED",
            "source-weight/current files keep finite countermodel rows",
            False,
        ),
        (
            "CURPL2964_2_beta_source",
            "beta_source_conf",
            "source charge beta_s := partial_Xhat ln m_source^eff in canonical Xhat units",
            "CONDITIONAL_STANDARD_VARIATION_ONLY",
            "2916 requires parent Xhat and matter/source definition first",
            False,
        ),
        (
            "CURPL2964_3_beta_test",
            "beta_test_conf",
            "test charge beta_t := partial_Xhat ln m_test^eff in canonical Xhat units",
            "CONDITIONAL_STANDARD_VARIATION_ONLY",
            "qbar/test coupling template remains missing",
            False,
        ),
        (
            "CURPL2964_4_Qbar",
            "Qbar_XH/qbar_XT",
            "source/test projections for R10 product law",
            "MISSING_SOURCE_CHARGE_PROJECTION",
            "2661/2673 keep Qbar_XH and qbar_XT missing",
            False,
        ),
        (
            "CURPL2964_5_verdict",
            "source/test current payload",
            "CURPL2964_0 through CURPL2964_4 all close with source paths",
            "SOURCE_CURRENT_FIRST_VALUE_NOT_DERIVED",
            "no finite-bconf product score can be made from current payload yet",
            False,
        ),
    ]
    return [
        add_common(
            {
                "payload_id": payload_id,
                "symbol": symbol,
                "required_payload": payload,
                "current_status": status,
                "evidence_summary": evidence,
                "payload_acquired": acquired,
            }
        )
        for payload_id, symbol, payload, status, evidence, acquired in rows
    ]


def first_slot_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SLOT2964_0_N_Xhat",
            "N_Xhat",
            "field_normalization",
            "highest-priority first value: canonical map from X to Xhat",
            "MISSING_FIELD_METRIC_OWNER",
            "accepted sources: parent field metric theorem; explicit Z_X/f_X source row; closure-debt branch label only as nonclaim",
        ),
        (
            "SLOT2964_1_lambda_X",
            "lambda_X",
            "length",
            "finite exchange range in same normalization",
            "MISSING_ZX_MX2_SAME_NORMALIZATION",
            "accepted sources: Z_X and M_X^2 numeric/theorem-zero with positive gap in same branch",
        ),
        (
            "SLOT2964_2_beta_source_test",
            "beta_source_conf;beta_test_conf",
            "dimensionless",
            "source/test charges in canonical Xhat units",
            "MISSING_SOURCE_CURRENT_OWNER",
            "accepted sources: common current owner theorem or explicit finite nonclaim source/test charge rows",
        ),
        (
            "SLOT2964_3_b_conf",
            "b_conf",
            "dimensionless",
            "finite hidden-frame prior or theorem-zero in canonical Xhat units",
            "MISSING_PRIOR_OR_THEOREM_ZERO",
            "accepted sources: parent theorem-zero, closure-debt flag, external phenomenological prior, or future fit value",
        ),
    ]
    source_path = ";".join(str(path) for path in [SRC_2963_PROMOTION, SRC_2962_PRIOR, SRC_2951_COEFF, SRC_2951_OWNER, SRC_2676_OWNER, SRC_2916_PRODUCT])
    return [
        add_common(
            {
                "slot_id": slot_id,
                "symbol": symbol,
                "units": units,
                "priority_reason": reason,
                "numeric_or_theorem_value": value,
                "acceptance_policy": policy,
                "source_path": source_path,
                "source_path_exists": all(Path(path).exists() for path in source_path.split(";")),
                "accepted_for_scoring": False,
                "no_cancellation_policy": True,
            }
        )
        for slot_id, symbol, units, reason, value, policy in rows
    ]


def runner_update_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN2964_0_runner_state", "2963 runner remains correct", "valid_mts_rows=0 until first slot is numeric/theorem-zero", "KEEP_REFUSAL"),
        ("RUN2964_1_first_unlock", "first unlock candidate", "SLOT2964_0_N_Xhat or SLOT2964_1_lambda_X must be sourced before R10 alpha row can even be dimensionally stable", "TARGET_X_PAYLOAD_FIRST"),
        ("RUN2964_2_current_unlock", "product unlock candidate", "SLOT2964_2_beta_source_test must be sourced before alpha_R10_conf can be computed", "TARGET_CURRENT_PAYLOAD_SECOND"),
        ("RUN2964_3_no_claim", "claim state", "no runner promotion, local-GR, R10, PPN or clock claim allowed", "CLAIM_FALSE"),
    ]
    return [
        add_common(
            {
                "runner_update_id": update_id,
                "object": obj,
                "statement": statement,
                "status": status,
            }
        )
        for update_id, obj, statement, status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2964_0_X_payload", "Xhat/Z_X/M_X^2/lambda payload acquired", False, "X_PAYLOAD_NOT_DERIVED"),
        ("CG2964_1_current_payload", "source/test current payload acquired", False, "CURRENT_PAYLOAD_NOT_DERIVED"),
        ("CG2964_2_first_slot", "first value slot score-ready", False, "FIRST_SLOTS_NONCLAIM_PLACEHOLDERS"),
        ("CG2964_3_runner", "2963 runner now has valid MTS rows", False, "VALID_MTS_ROWS_ZERO"),
        ("CG2964_4_local_GR", "local GR/Newton reduction allowed", False, "NO_LOCAL_GR_CLAIM"),
        ("CG2964_5_public", "public claim allowed", False, "PRIVATE_NONCLAIM_CHECKPOINT"),
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
            "DEC2964_0_X_payload",
            "Xhat/Z/M/lambda payload not acquired",
            "all pieces are already named, but field identity, field metric, mass gap and lambda remain owner-missing",
            "do not promote Xhat or lambda rows",
        ),
        (
            "DEC2964_1_current_payload",
            "source/test current payload not acquired",
            "source-current owner and source/test charge projections remain conditional or missing",
            "do not compute alpha_R10_conf product",
        ),
        (
            "DEC2964_2_first_slots",
            "first value slots emitted",
            "N_Xhat, lambda_X, beta_source/test and b_conf are now prioritized as the exact payloads the 2963 runner needs",
            "source SLOT2964_0 or SLOT2964_2 next",
        ),
        (
            "DEC2964_3_next",
            "next target should attack field metric normalization first",
            "without N_Xhat/lambda the finite branch is not even invariantly normalized; source current product can follow",
            "build 2965 N_Xhat field metric owner or first prior slot",
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
                "next_id": "NEXT2964_0_2965",
                "priority": "selected_primary",
                "next_doc": "2965-Y5-R2FR-NXhat-field-metric-owner-or-first-prior-slot-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_NXhat_field_metric_owner_or_first_prior_slot_under_AX1090_2965.py",
                "objective": "Try to derive or source the canonical N_Xhat field metric owner, including Z_X f_X^2 or equivalent normalization and rescaling guard. If this fails, emit the first nonclaim N_Xhat prior/source slot accepted by the 2963 runner.",
                "include": "N_Xhat;Z_X;f_X;Z_X f_X^2;field metric owner;rescaling guard;lambda_X dependency;source paths;units;claim gates",
                "exclude": "derive single-frame theorem again;b_marker full taxonomy;source-current product until N_Xhat route audited;quotient/vertical no-pole rerun;beta prediction without owners;direct lambda closure;I_X scoring;local-GR claim;public claim;formalization-workbench edits;GitHub action",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("x_payload_copy", OUTPUTS["x_payload"], BRANCH_OUTPUTS["x_payload_copy"]),
        ("slot_copy", OUTPUTS["first_slots"], BRANCH_OUTPUTS["slot_copy"]),
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
        ("VAL2964_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2964_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all cited source anchors found", True),
        ("VAL2964_2_X_payload_blocked", any(row["payload_id"] == "XPL2964_5_verdict" and row["payload_acquired"] is False for row in all_rows["x_payload"]), "Xhat/Z/M/lambda payload remains blocked", True),
        ("VAL2964_3_current_payload_blocked", any(row["payload_id"] == "CURPL2964_5_verdict" and row["payload_acquired"] is False for row in all_rows["current_payload"]), "source-current payload remains blocked", True),
        ("VAL2964_4_slots_nonclaim", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["first_slots"]), "first value slots remain nonclaim", True),
        ("VAL2964_5_slot_paths_exist", all(row["source_path_exists"] is True for row in all_rows["first_slots"]), "first value slots cite existing paths", True),
        ("VAL2964_6_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates remain blocked", True),
        ("VAL2964_7_next_target_written", any(row["next_id"] == "NEXT2964_0_2965" for row in all_rows["next"]), "2965 next target selected", True),
        ("VAL2964_8_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2964_9_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2964_10_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2964_11_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2964 outputs were written to formalization-workbench", True),
        ("VAL2964_12_doc_written", DOC.exists(), "2964 markdown checkpoint exists", True),
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
    rows.append(add_common({"validation_id": "VAL2964_OVERALL", "passed": overall, "check": "2964 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2964 - Y5 R2FR: Xhat-ZX-MX2-lambda or source-current first value under AX1090

Status: `Y5_R2FR_2964_first_finite_bconf_payload_not_acquired_first_value_slots_emitted_nonclaim`

Claim ceiling: `no_Xhat_payload_no_source_current_payload_no_first_value_score_no_R10_PPN_clock_score_no_local_GR_no_Newton_no_public_claim`

2964 tries to source the first decisive payload needed by the finite `b_conf` branch. The result is:

- The canonical `Xhat/Z_X/M_X^2/lambda_X` route does not close: parent X identity, field metric, Z sign, mass gap and same-normalization lambda are still unsigned.
- The source/test current route does not close: common current owner, no source-only weights, source/test charges and Qbar/qbar projections remain conditional or missing.
- First value slots are now explicit and ordered: `N_Xhat` first, then `lambda_X`, then `beta_source/test`, then `b_conf`.
- The 2963 runner remains correctly blocked until one of these slots is numeric or theorem-zero with source paths.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Xhat/Z/M/lambda Payload Gate

{md_table(all_rows["x_payload"], ["payload_id", "symbol", "current_status", "payload_acquired", "evidence_summary"])}

## Source/Test Current Payload Gate

{md_table(all_rows["current_payload"], ["payload_id", "symbol", "current_status", "payload_acquired", "evidence_summary"])}

## First Value Slots

{md_table(all_rows["first_slots"], ["slot_id", "symbol", "numeric_or_theorem_value", "units", "accepted_for_scoring", "priority_reason"])}

## Runner Update Rows

{md_table(all_rows["runner_update"], ["runner_update_id", "object", "status", "statement"])}

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
        "x_payload": x_payload_rows(),
        "current_payload": current_payload_rows(),
        "first_slots": first_slot_rows(),
        "runner_update": runner_update_rows(),
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

    print(f"2964 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
