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
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2960"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2960-Y5-R2FR-bconf-tau-projection-map-or-single-frame-closure-declaration-under-AX1090.md"

SRC_2959_DOC = ROOT / "2959-Y5-R2FR-single-observed-frame-parent-action-clause-or-bconf-bound-intake-under-AX1090.md"
SRC_2959_NEXT = RESIDUALS / "P8_Y5_R2FR_2959_NEXT_TARGET.csv"
SRC_2959_FRAME = RESIDUALS / "P8_Y5_R2FR_2959_SINGLE_OBSERVED_FRAME_PARENT_ACTION_GATE.csv"
SRC_2959_BCONF = RESIDUALS / "P8_Y5_R2FR_2959_BCONF_BOUND_INTAKE_NONCLAIM.csv"
SRC_2959_PROJ = RESIDUALS / "P8_Y5_R2FR_2959_BCONF_PROJECTION_MAP_REQUIREMENTS.csv"
SRC_2958_BOUNDS = RESIDUALS / "P8_Y5_R2FR_2958_COMPONENT_BOUND_ROWS_NONCLAIM.csv"
SRC_1046_NOSHADOW = RESIDUALS / "P8_Y5_R10_1046_NO_SHADOW_FRAME_THEOREM_ATTEMPT.csv"
SRC_1046_QBAR = RESIDUALS / "P8_Y5_R10_1046_QBAR_MARKER_COEFFICIENT_ROWS.csv"
SRC_2571_COFRAME = RESIDUALS / "P8_Y5_OBS_COFRAME_2571_DOBS_KERNEL_GATE.csv"
SRC_2673_JX = RESIDUALS / "P8_Y5_R2FR_JX_QBARXT_2673_SOURCE_ZERO_AUDIT.csv"
SRC_LOCAL_TEMPLATE = RESIDUALS / "MTS_local_residual_predictions_TEMPLATE.csv"
SRC_GLOBAL_COUPLING = RESIDUALS / "P8_global_coupling_superselection_CONTRACT.csv"
SRC_LOCAL_BOUNDS = LOCAL_BOUNDS / "local_bound_claims.csv"
SRC_R10_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv"
SRC_CLOCK_ALPHA = RESIDUALS / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2960_SOURCE_REGISTER.csv",
    "tau_gate": RESIDUALS / "P8_Y5_R2FR_2960_BCONF_TAU_PROJECTION_GATE.csv",
    "conditional": RESIDUALS / "P8_Y5_R2FR_2960_CONDITIONAL_SCALAR_TENSOR_COUNTERMODEL_MAP.csv",
    "closure": RESIDUALS / "P8_Y5_R2FR_2960_SINGLE_FRAME_CLOSURE_DECLARATION_NONCLAIM.csv",
    "bound_rows": RESIDUALS / "P8_Y5_R2FR_2960_BCONF_BOUND_ROWS_NONCLAIM.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2960_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2960_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2960_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2960_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2960_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "closure_copy": PARENT_ACTION / "single_frame_closure_declaration_2960_NONCLAIM.csv",
    "bound_copy": LOCAL_BOUNDS / "b_conf_tau_projection_bound_rows_2960_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2960_BCONF_BRANCH_SELECTOR_NEXT_NONCLAIM.csv",
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
        ("SRC2960_00_2959_doc", SRC_2959_DOC, "NEXT2959_0_2960;Validation overall: `True`", "2959 handoff"),
        ("SRC2960_01_2959_next", SRC_2959_NEXT, "NEXT2959_0_2960", "machine-readable 2960 target"),
        ("SRC2960_02_2959_frame", SRC_2959_FRAME, "SFRAME2959_1_chain_rule;SFRAME2959_7_verdict", "single-frame gate"),
        ("SRC2960_03_2959_bconf", SRC_2959_BCONF, "BCI2959_1_tau_R10_conf;BCI2959_5_B_conf_envelope", "b_conf intake rows"),
        ("SRC2960_04_2959_proj", SRC_2959_PROJ, "PROJ2959_0_R10;PROJ2959_4_joint_policy", "projection requirements"),
        ("SRC2960_05_2958_bounds", SRC_2958_BOUNDS, "BOUND2958_0_b_conf;BOUND2958_2_joint_envelope", "prior bound rows"),
        ("SRC2960_06_1046_noshadow", SRC_1046_NOSHADOW, "NSF1046_1_conditional_chain_rule_zero;NSF1046_5_verdict", "no-shadow theorem"),
        ("SRC2960_07_1046_qbar", SRC_1046_QBAR, "QMC1046_0_b_conf;QMC1046_3_qbar_marker_abs", "qbar marker rows"),
        ("SRC2960_08_2571_coframe", SRC_2571_COFRAME, "DOK2571_0_exact_kernel;DOK2571_4_current_verdict", "observed coframe kernel"),
        ("SRC2960_09_2673_jx", SRC_2673_JX, "JX2673_4_hidden_frame;JX2673_7_verdict", "J_X/qbar source-zero audit"),
        ("SRC2960_10_local_template", SRC_LOCAL_TEMPLATE, "R3_gamma;R10_fifth_force", "local residual prediction template"),
        ("SRC2960_11_global_coupling", SRC_GLOBAL_COUPLING, "GS4_no_range_radial_time_dependence;GS7_scalar_branch_fallback", "global coupling/source normalization contract"),
        ("SRC2960_12_local_bounds", SRC_LOCAL_BOUNDS, "R1_WEP_source_charge;R2_clock_redshift;R3_gamma", "local WEP/clock/PPN bounds"),
        ("SRC2960_13_r10_curve", SRC_R10_CURVE, "R10_VECTOR_2020_REVIEW_0000;review_candidate_only", "R10 nonclaim curve"),
        ("SRC2960_14_clock_alpha", SRC_CLOCK_ALPHA, "CAS646_0_AlHg;CAS646_1_YbE3E2", "clock alpha sensitivity source"),
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


def tau_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "TAU2960_0_canonical_state",
            "Xhat canonical/local state normalization",
            "Define canonical local field Xhat, mass/range lambda_X, and source/test response charges so b_conf has a unique observable normalization.",
            "MISSING_NORMALIZATION_OWNER",
            "Without Xhat normalization and response charge, b_conf can be rescaled into Xhat.",
            False,
        ),
        (
            "TAU2960_1_R10",
            "tau_R10_conf",
            "Map hidden conformal coupling into Yukawa alpha(lambda), e.g. alpha_R10 = C_R10 beta_source beta_test F(lambda_X), beta_A := tau_A b_conf.",
            "CONDITIONAL_TEMPLATE_ONLY",
            "Needs canonical scalar normalization, source/test scalar charges, lambda_X and curve identity.",
            False,
        ),
        (
            "TAU2960_2_PPN",
            "tau_PPN_gamma_conf",
            "Map b_conf into gamma_minus_1, with scalar-tensor countermodel gamma-1 = -2 beta_0^2/(1+beta_0^2) only after frame and range choices.",
            "CONDITIONAL_COUNTERMODEL_ONLY",
            "Needs massless/finite-range regime, observed-vs-matter frame relation and solar-system background.",
            False,
        ),
        (
            "TAU2960_3_clock",
            "tau_clock_conf",
            "Map b_conf Delta Xhat into redshift/LPI or clock ratios; pure common conformal changes can cancel in dimensionless ratios if all clocks share the same frame.",
            "MISSING_LOCAL_CLOCK_MAP",
            "Needs local Xhat profile and declaration of which frame defines rods/clocks/observed metric.",
            False,
        ),
        (
            "TAU2960_4_source",
            "tau_source_conf",
            "Map b_conf into source-current normalization, measured GM or source-charge response.",
            "MISSING_SOURCE_CURRENT_OWNER",
            "Existing source-normalization contracts keep this as a hard local-GR blocker.",
            False,
        ),
        (
            "TAU2960_5_verdict",
            "b_conf tau projection package",
            "TAU2960_0 through TAU2960_4 are parent-owned or source-backed.",
            "TAU_PACKAGE_NOT_DERIVED",
            "The maps are useful conditional templates, not claim-grade MTS predictions.",
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
                "derived_for_claim": derived,
            }
        )
        for gate_id, obj, statement, status, evidence, derived in rows
    ]


def conditional_countermodel_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CMAP2960_0_universal_scalar_tensor",
            "universal conformal countermodel",
            "S_matter[psi, A(Xhat)^2 g_obs] with A=exp(b_conf Xhat)",
            "covariant, often leading-order WEP-safe, but not GR-identical",
            "shows why covariance/WEP cannot derive b_conf=0",
        ),
        (
            "CMAP2960_1_R10_template",
            "short-range fifth force",
            "alpha_R10(lambda_X) = C_R10 [tau_source_conf b_conf][tau_test_conf b_conf] F_range(lambda_X)",
            "conditional only",
            "missing C_R10, tau_source_conf, tau_test_conf, lambda_X and finite-range profile",
        ),
        (
            "CMAP2960_2_PPN_template",
            "PPN gamma",
            "gamma_minus_1 = -2 beta_0^2/(1+beta_0^2), beta_0=tau_PPN_gamma_conf b_conf, in the simplest massless scalar-tensor limit",
            "countermodel only",
            "finite range, screening and observed-frame relation are not MTS-derived",
        ),
        (
            "CMAP2960_3_clock_template",
            "clock/redshift",
            "delta y_clock = tau_clock_conf b_conf Delta Xhat_local",
            "conditional only",
            "pure common conformal changes may be calibration unless frame/readout order is fixed",
        ),
        (
            "CMAP2960_4_source_template",
            "source normalization",
            "delta ln GM_obs = tau_source_conf b_conf Delta Xhat_source",
            "conditional only",
            "source-current owner and measured-GM calibration remain missing",
        ),
    ]
    return [
        add_common(
            {
                "map_id": map_id,
                "arena": arena,
                "conditional_formula": formula,
                "status": status,
                "lesson": lesson,
                "accepted_for_scoring": False,
            }
        )
        for map_id, arena, formula, status, lesson in rows
    ]


def closure_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CLOSE2960_0_statement",
            "single-observed-frame closure",
            "Ordinary matter in the local branch couples only to e_obs(q) and fixed representation data; hidden conformal/disformal/source frames are not in the parent action grammar.",
            "CLOSURE_AVAILABLE_NOT_DERIVED",
            "Adopting this gives b_conf=0 by definition/domain typing, but it is not a derivation.",
        ),
        (
            "CLOSE2960_1_credit_limit",
            "credit limit",
            "Closure may be used as a private branch assumption, never as a local-GR proof or public claim.",
            "NO_THEOREM_ZERO_CREDIT",
            "The branch must carry closure_debt=true until parent action derivation appears.",
        ),
        (
            "CLOSE2960_2_residual_fallback",
            "residual fallback",
            "If closure is not adopted, retain b_conf as an explicit residual and evaluate conditional tau maps when sourced.",
            "RESIDUAL_BRANCH_OPEN",
            "This keeps the theory testable rather than pretending local GR is derived.",
        ),
        (
            "CLOSE2960_3_verdict",
            "2960 fork verdict",
            "Either closure_debt branch or b_conf residual branch; neither is a derived local-GR result.",
            "DEMOTE_TO_EXPLICIT_FORK",
            "The next checkpoint should build a branch selector instead of looping the same proof.",
        ),
    ]
    return [
        add_common(
            {
                "closure_id": closure_id,
                "object": obj,
                "statement": statement,
                "current_status": status,
                "consequence": consequence,
                "closure_debt": True,
                "theorem_zero_credit": False,
            }
        )
        for closure_id, obj, statement, status, consequence in rows
    ]


def bound_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BROW2960_0_b_conf",
            "b_conf",
            "dimensionless",
            "retained hidden conformal frame coefficient",
            "MISSING_VALUE_OR_CLOSURE",
            "not score-ready unless closure sets zero or tau package is sourced",
        ),
        (
            "BROW2960_1_R10_alpha",
            "alpha_R10_conf",
            "dimensionless",
            "alpha_R10_conf(lambda)=C_R10(tau_source_conf b_conf)(tau_test_conf b_conf)F_range(lambda)",
            "MISSING_C_R10_TAU_LAMBDA",
            "use R10 curve only after MTS-side alpha(lambda) row is numeric/source-backed",
        ),
        (
            "BROW2960_2_PPN_gamma",
            "gamma_minus_1_conf",
            "dimensionless",
            "gamma_minus_1_conf=-2(tau_PPN_gamma_conf b_conf)^2/(1+(tau_PPN_gamma_conf b_conf)^2) in simplest countermodel",
            "MISSING_TAU_PPN_AND_FRAME_REGIME",
            "conditional scalar-tensor template, not an MTS prediction",
        ),
        (
            "BROW2960_3_clock",
            "clock_conf",
            "dimensionless",
            "clock_conf=tau_clock_conf b_conf Delta Xhat_local",
            "MISSING_TAU_CLOCK_AND_LOCAL_PROFILE",
            "clock sensitivity sources exist but not the MTS local projection",
        ),
        (
            "BROW2960_4_source",
            "source_conf",
            "dimensionless",
            "source_conf=tau_source_conf b_conf Delta Xhat_source",
            "MISSING_SOURCE_CURRENT_MAP",
            "source normalization remains a hard local-GR blocker",
        ),
    ]
    source_path = ";".join(str(path) for path in [SRC_2959_BCONF, SRC_2959_PROJ, SRC_LOCAL_BOUNDS, SRC_R10_CURVE])
    return [
        add_common(
            {
                "row_id": row_id,
                "symbol": symbol,
                "units": units,
                "formula_or_bound": formula,
                "numeric_or_theorem_value": value,
                "notes": notes,
                "source_path": source_path,
                "source_path_exists": all(Path(path).exists() for path in source_path.split(";")),
                "accepted_for_scoring": False,
                "no_cancellation_policy": True,
            }
        )
        for row_id, symbol, units, formula, value, notes in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2960_0_tau_package", "b_conf tau projection package derived", False, "MISSING_NORMALIZATION_AND_SOURCE_CURRENT"),
        ("CG2960_1_single_frame_theorem", "single-frame rule promoted as theorem", False, "DEMOTED_TO_CLOSURE_DEBT"),
        ("CG2960_2_bconf_zero", "b_conf=0 claim", False, "ONLY_CLOSURE_NOT_DERIVATION"),
        ("CG2960_3_bconf_score", "b_conf residual score-ready", False, "MISSING_TAU_VALUES"),
        ("CG2960_4_R10_PPN_clock", "R10/PPN/clock comparison allowed", False, "MTS_SIDE_ROWS_NONCLAIM"),
        ("CG2960_5_local_GR", "local GR/Newton reduction allowed", False, "NO_LOCAL_GR_CLAIM"),
        ("CG2960_6_public", "public claim allowed", False, "PRIVATE_NONCLAIM_CHECKPOINT"),
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
            "DEC2960_0_tau_result",
            "b_conf tau maps are not derived",
            "R10, PPN, clock and source projections all need canonical Xhat normalization plus source/test/local-state maps",
            "do not score b_conf residuals yet",
        ),
        (
            "DEC2960_1_closure_result",
            "single-frame rule is demoted to explicit closure",
            "it is a clean branch assumption that kills b_conf, but current evidence does not make it a theorem",
            "carry closure_debt=true if used",
        ),
        (
            "DEC2960_2_best_next",
            "build a branch selector instead of repeating the proof loop",
            "the theory now has two honest paths: closure-debt local-GR branch or finite b_conf residual branch",
            "create 2961 branch selector with no public/local-GR claim",
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
                "next_id": "NEXT2960_0_2961",
                "priority": "selected_primary",
                "next_doc": "2961-Y5-R2FR-bconf-branch-selector-closure-debt-or-residual-smoke-runner-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_bconf_branch_selector_closure_debt_or_residual_smoke_runner_under_AX1090_2961.py",
                "objective": "Create an explicit two-branch selector: closure-debt branch where the single-observed-frame rule sets b_conf=0 with no theorem credit, and residual branch where b_conf remains finite with nonclaim tau-map placeholders ready for later smoke tests.",
                "include": "closure_debt flag;b_conf=0 closure row;finite b_conf residual row;tau map placeholders;R10/PPN/clock/source blocked gates;no-cancellation policy;no local-GR claim",
                "exclude": "derive single-frame theorem again;b_marker full taxonomy;quotient/vertical no-pole rerun;beta prediction;direct lambda closure;alpha(lambda) scoring;I_X scoring;public claim;formalization-workbench edits;GitHub action",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("closure_copy", OUTPUTS["closure"], BRANCH_OUTPUTS["closure_copy"]),
        ("bound_copy", OUTPUTS["bound_rows"], BRANCH_OUTPUTS["bound_copy"]),
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
        ("VAL2960_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2960_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all cited source anchors found", True),
        ("VAL2960_2_tau_not_derived", any(row["gate_id"] == "TAU2960_5_verdict" and row["derived_for_claim"] is False for row in all_rows["tau_gate"]), "tau package remains not derived", True),
        ("VAL2960_3_closure_debt", all(row["closure_debt"] is True and row["theorem_zero_credit"] is False for row in all_rows["closure"]), "closure declaration carries debt and no theorem credit", True),
        ("VAL2960_4_bound_rows_nonclaim", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["bound_rows"]), "bound rows remain nonclaim", True),
        ("VAL2960_5_bound_paths_exist", all(row["source_path_exists"] is True for row in all_rows["bound_rows"]), "bound rows cite existing paths", True),
        ("VAL2960_6_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates remain blocked", True),
        ("VAL2960_7_next_target_written", any(row["next_id"] == "NEXT2960_0_2961" for row in all_rows["next"]), "2961 next target selected", True),
        ("VAL2960_8_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2960_9_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2960_10_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2960_11_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2960 outputs were written to formalization-workbench", True),
        ("VAL2960_12_doc_written", DOC.exists(), "2960 markdown checkpoint exists", True),
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
    rows.append(add_common({"validation_id": "VAL2960_OVERALL", "passed": overall, "check": "2960 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2960 - Y5 R2FR: bconf tau projection map or single-frame closure declaration under AX1090

Status: `Y5_R2FR_2960_bconf_tau_maps_not_derived_single_frame_demoted_to_closure_debt`

Claim ceiling: `no_tau_projection_package_no_b_conf_theorem_zero_no_bconf_score_no_local_GR_no_Newton_no_public_claim`

2960 asks whether the finite `b_conf` branch can be projected into real local arenas, or whether the single-frame rule must be treated as a closure. The result is:

- Conditional projection formulas exist for R10, PPN gamma, clocks and source normalization, but they require canonical `Xhat` normalization, source/test charges, `lambda_X`, local profile and source-current ownership.
- The simplest scalar-tensor countermodel shows why this cannot be skipped: a universal conformal frame can be covariant and leading-order WEP-safe while still producing fifth-force/PPN/source-normalization pressure.
- The single-observed-frame rule is therefore demoted to an explicit closure/axiom branch with `closure_debt=true`; it gets no theorem-zero credit.
- The honest fork is now explicit: either carry a closure-debt branch with `b_conf=0`, or keep a finite `b_conf` residual branch until tau maps are sourced.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## b_conf Tau Projection Gate

{md_table(all_rows["tau_gate"], ["gate_id", "object", "current_status", "derived_for_claim", "evidence_summary"])}

## Conditional Scalar-Tensor Countermodel Map

{md_table(all_rows["conditional"], ["map_id", "arena", "status", "conditional_formula", "lesson"])}

## Single-Frame Closure Declaration

{md_table(all_rows["closure"], ["closure_id", "object", "current_status", "closure_debt", "theorem_zero_credit", "consequence"])}

## b_conf Bound Rows

{md_table(all_rows["bound_rows"], ["row_id", "symbol", "numeric_or_theorem_value", "units", "accepted_for_scoring", "formula_or_bound"])}

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
        "tau_gate": tau_gate_rows(),
        "conditional": conditional_countermodel_rows(),
        "closure": closure_rows(),
        "bound_rows": bound_rows(),
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

    print(f"2960 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
