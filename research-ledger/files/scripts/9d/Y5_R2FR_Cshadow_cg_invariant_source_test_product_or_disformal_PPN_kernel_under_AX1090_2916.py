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

CHECKPOINT = "2916"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2916-Y5-R2FR-Cshadow-cg-invariant-source-test-product-or-disformal-PPN-kernel-under-AX1090.md"

SRC_2915_DOC = ROOT / "2915-Y5-R2FR-Cshadow-component-bound-pack-or-Cobs-parent-normalization-proof-under-AX1090.md"
SRC_2915_ACQ = RESIDUALS / "P8_Y5_R2FR_2915_COMPONENT_ACQUISITION_ROWS.csv"
SRC_2915_ARENA = RESIDUALS / "P8_Y5_R2FR_2915_ARENA_ROUTING_AND_PRODUCT_RULES.csv"
SRC_2915_NEXT = RESIDUALS / "P8_Y5_R2FR_2915_NEXT_TARGET.csv"
SRC_2915_CLAIMS = RESIDUALS / "P8_Y5_R2FR_2915_CLAIM_GATES.csv"
SRC_1035_SPLIT = RESIDUALS / "P8_Y5_R10_1035_SOURCE_TEST_CHARGE_SPLIT.csv"
SRC_1035_KX = RESIDUALS / "P8_Y5_R10_1035_KX_FACTORIZATION_ROWS.csv"
SRC_1036_DERIV = RESIDUALS / "P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv"
SRC_1036_BRANCH = RESIDUALS / "P8_Y5_R10_1036_BRANCH_CLASSIFICATION.csv"
SRC_1037_BETA = RESIDUALS / "P8_Y5_R10_1037_BOUNDED_BETA_SOURCE_TEST_TEMPLATE.csv"
SRC_1038_QUARANTINE = RESIDUALS / "P8_Y5_R10_1038_LEGACY_LINEAR_CG_QUARANTINE.csv"
SRC_1038_ACQ = RESIDUALS / "P8_Y5_R10_1038_BETA_BOUND_SOURCE_ACQUISITION.csv"
SRC_944_FRAME = RESIDUALS / "P8_Y5_R10_944_FRAME_LEAK_BOUND_PACK.csv"
SRC_945_BOUNDS = RESIDUALS / "P8_Y5_R10_945_FIRST_FRAME_LEAK_BOUND_ROWS.csv"
SRC_1029_THEOREM = RESIDUALS / "P8_Y5_R10_1029_NO_SHADOW_FRAME_THEOREM_AUDIT.csv"
SRC_1030_PROVENANCE = RESIDUALS / "P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv"
SRC_1031_FALLBACK = RESIDUALS / "P8_Y5_R10_1031_FINITE_CG_TAU_FALLBACK.csv"
SRC_1157_CG = RESIDUALS / "P8_Y5_R10_1157_CG_BOUND_FIRST_FILL_ROWS.csv"
SRC_1027_SCHEMA = RESIDUALS / "P8_Y5_R10_1027_BOUNDED_QBARXT_ROW_SCHEMA.csv"
SRC_2888_CSHADOW = RESIDUALS / "P8_Y5_R2FR_2888_CSHADOW_BOUND_ROW_NONCLAIM.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2916_SOURCE_REGISTER.csv",
    "law": RESIDUALS / "P8_Y5_R2FR_2916_CG_INVARIANT_SOURCE_TEST_PRODUCT_LAW.csv",
    "source_leg": RESIDUALS / "P8_Y5_R2FR_2916_QBAR_SOURCE_LEG_DECLARATION_GATE.csv",
    "beta_pack": RESIDUALS / "P8_Y5_R2FR_2916_BETA_SOURCE_TEST_ENVELOPE_ROWS.csv",
    "disformal": RESIDUALS / "P8_Y5_R2FR_2916_DISFORMAL_PPN_KERNEL_FALLBACK.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2916_RUNNER_STATUS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2916_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2916_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2916_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2916_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2916_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "law_copy": PARENT_ACTION / "Cg_invariant_source_test_product_law_2916_NONCLAIM.csv",
    "beta_copy": LOCAL_BOUNDS / "Cg_beta_source_test_envelope_2916_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2916_DISFORMAL_PPN_KERNEL_OR_CG_SOURCE_LEG_NEXT_NONCLAIM.csv",
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
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2916_00_2915_doc", SRC_2915_DOC, "NEXT2915_0_2916;naked linear", "2915 handoff to invariant c_g product"),
        ("SRC2916_01_2915_acq", SRC_2915_ACQ, "ACQ2915_3_cg_product_rule;NAKED_LINEAR_CG_FORBIDDEN", "2915 c_g acquisition gate"),
        ("SRC2916_02_2915_arena", SRC_2915_ARENA, "ARENA2915_0_R10;beta_s beta_t", "2915 arena rule"),
        ("SRC2916_03_2915_next", SRC_2915_NEXT, "NEXT2915_0_2916;source-test product", "machine-readable 2916 target"),
        ("SRC2916_04_2915_claims", SRC_2915_CLAIMS, "CG2915_2_cg_score;BLOCKED_NONCLAIM", "2915 c_g claim gate"),
        ("SRC2916_05_1035_split", SRC_1035_SPLIT, "BETA1035_0_product_law;BETA1035_1_universal_weyl", "source/test charge split"),
        ("SRC2916_06_1035_kx", SRC_1035_KX, "KXF1035_0_KX_point;KXF1035_4_total", "K_X factorization requirements"),
        ("SRC2916_07_1036_deriv", SRC_1036_DERIV, "BETA1036_1_two_body_exchange;BETA1036_3_common_Weyl_cg", "beta product derivation"),
        ("SRC2916_08_1036_branch", SRC_1036_BRANCH, "BR1036_2_sourced_finite_exchange;BR1036_3_shadow_frame_marker", "finite exchange branch classification"),
        ("SRC2916_09_1037_beta", SRC_1037_BETA, "BB1037_6_beta_abs_totals;BB1037_7_beta_product_guard", "bounded beta source/test template"),
        ("SRC2916_10_1038_quarantine", SRC_1038_QUARANTINE, "LCG1038_0_944_linear_shorthand;LCG1038_1_runner_guard", "legacy linear c_g quarantine"),
        ("SRC2916_11_1038_acq", SRC_1038_ACQ, "BBA1038_0_R10_beta_product;BBA1038_3_PPN_common_frame_gamma", "beta/disformal acquisition anchors"),
        ("SRC2916_12_944_frame", SRC_944_FRAME, "FLB944_0_cg_weyl;FLB944_1_disformal", "frame leak bound pack"),
        ("SRC2916_13_945_bounds", SRC_945_BOUNDS, "BND945_0_cg_value;BND945_4_disformal_value", "first frame leak bound rows"),
        ("SRC2916_14_1029_theorem", SRC_1029_THEOREM, "NST1029_1_chain_rule_zero;NST1029_6_verdict", "no-shadow c_g theorem audit"),
        ("SRC2916_15_1030_provenance", SRC_1030_PROVENANCE, "CPG1030_1_finite_cg_value;CPG1030_4_no_cancellation", "c_g provenance gate"),
        ("SRC2916_16_1031_fallback", SRC_1031_FALLBACK, "FCG1031_0_cg_value;FCG1031_3_no_cancellation", "finite c_g/tau fallback"),
        ("SRC2916_17_1157_cg", SRC_1157_CG, "CG1157_0_cg_first_fill;CG1157_5_score_interface", "c_g first fill rows"),
        ("SRC2916_18_1027_schema", SRC_1027_SCHEMA, "BQT1027_0_visible_geometry;BQT1027_4_claim_gate", "qbar geometry source/test schema"),
        ("SRC2916_19_2888_cshadow", SRC_2888_CSHADOW, "CSH2888_1_b_R_common_weyl;CSH2888_2_d_R_disformal", "older Weyl/disformal Cshadow rows"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
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


def law_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "LAW2916_0_point_source",
            "beta_i definition",
            "For an ordinary body i with S_i=-int m_i^eff(Xhat) ds_i, beta_i := partial_Xhat ln m_i^eff and J_X carries beta_i m_i.",
            "CONDITIONAL_STANDARD_VARIATION",
            "requires parent Xhat normalization and matter/source definition",
        ),
        (
            "LAW2916_1_two_body_exchange",
            "finite exchange product",
            "Integrating out a finite local X mode gives V_X proportional to beta_s beta_t exp(-r/lambda)/r; the R10 alpha form is K_X^R10(lambda) beta_s beta_t plus absolute tails.",
            "CONDITIONAL_INVARIANT_PRODUCT_LAW",
            "requires Z_X/lambda_X/sign/profile/K_X and beta source/test rows",
        ),
        (
            "LAW2916_2_universal_weyl",
            "universal c_g branch",
            "If m_i^eff=A_g(Xhat)m_i for both source and test, then beta_s=P_s^W c_g and beta_t=P_t^W c_g, so the force product is P_s^W P_t^W c_g^2, not a naked linear c_g.",
            "CG_SQUARED_BRANCH_CONDITIONAL",
            "requires c_g value or zero theorem plus source/test profile factors",
        ),
        (
            "LAW2916_3_source_leg_exception",
            "linear c_g exception",
            "A linear-looking row is allowed only when Qbar_XH or beta_s already contains a source leg with source path, units and no MISSING markers; otherwise linear c_g is underfactored.",
            "SOURCE_LEG_EXCEPTION_DEFINED_NOT_SATISFIED",
            "no parent-signed source leg is currently declared",
        ),
        (
            "LAW2916_4_mixed_shadow",
            "mixed Weyl/disformal/marker/non-Hilbert branch",
            "The safe envelope is |beta_s beta_t| <= beta_s_abs beta_t_abs with beta_s_abs and beta_t_abs absolute sums over Weyl, disformal, marker and source-tail components.",
            "ABSOLUTE_ENVELOPE_REQUIRED",
            "component values/projections are missing",
        ),
        (
            "LAW2916_5_verdict",
            "current c_g invariant product status",
            "MTS has a claim-ready c_g R10/source-test prediction.",
            "PRODUCT_LAW_DERIVED_AS_CONTRACT_NOT_SCORE_READY",
            "c_g, source/test profiles, K_X, Qbar source leg, lambda and tails are missing or nonclaim",
        ),
    ]
    return [
        add_common(
            {
                "law_id": law_id,
                "target": target,
                "statement": statement,
                "current_status": status,
                "missing_for_claim": missing,
                "claim_value": "NONE",
                "theorem_zero": False,
            }
        )
        for law_id, target, statement, status, missing in specs
    ]


def source_leg_rows() -> list[dict[str, Any]]:
    specs = [
        ("SLG2916_0_Qbar_source_leg", "Qbar_XH_contains_source_leg", "Qbar_XH or beta_s explicitly includes source coupling/source mass response", "MISSING_SOURCE_LEG_DECLARATION", "without this a linear c_g alpha row is rejected"),
        ("SLG2916_1_source_path", "source_leg_source_path", "source leg has equation/source path/row id and units", "MISSING_SOURCE_PATH", "no provenance means no score"),
        ("SLG2916_2_units", "source_leg_units", "source leg and c_g normalization use declared Xhat/charge units", "MISSING_UNITS", "prevents hiding Z_X/G_N inside c_g"),
        ("SLG2916_3_no_double_count", "Qbar_beta_no_double_count", "if source leg is inside Qbar_XH, beta_t/c_g is not counted twice", "MISSING_FACTOR_LEDGER", "prevents c_g and beta_s duplication"),
        ("SLG2916_4_runner_rule", "linear_cg_runner_policy", "alpha(lambda)=numeric*c_g is rejected unless SLG2916_0 through SLG2916_3 pass", "REJECT_LINEAR_CG_NOW", "keeps 1038 quarantine active"),
        ("SLG2916_5_verdict", "Qbar source-leg gate for current MTS", "linear c_g exception is claim-safe now", "SOURCE_LEG_GATE_FAILS_CURRENT_MTS", "use beta_s beta_t envelope or keep c_g nonclaim"),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "gate": gate,
                "required_statement": statement,
                "current_status": status,
                "if_open": consequence,
                "gate_pass": False,
            }
        )
        for gate_id, gate, statement, status, consequence in specs
    ]


def beta_pack_rows() -> list[dict[str, Any]]:
    specs = [
        ("BETA2916_0_beta_s_geom", "beta_s_geom", "source-body Weyl/disformal geometry charge", "|beta_s_geom| <= |profile_s_W c_g| + |profile_s_dis b_dis|", "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND", "R10;PPN;clock"),
        ("BETA2916_1_beta_t_geom", "beta_t_geom", "test/readout Weyl/disformal geometry charge", "|beta_t_geom| <= |tau_R10 c_g| + |tau_dis b_dis|", "MISSING_ARENA_PROJECTION", "R10;PPN;clock"),
        ("BETA2916_2_beta_s_marker", "beta_s_marker", "source material/EM marker charge", "|beta_s_marker| <= sum_A |S_sA b_A| + |S_salpha b_alpha|", "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS", "WEP;clock;R10"),
        ("BETA2916_3_beta_t_marker", "beta_t_marker", "test material/readout marker charge", "|beta_t_marker| <= sum_A |S_tA b_A| + |S_talpha b_alpha|", "MISSING_MARKER_READOUT_PROJECTION", "WEP;clock;R10"),
        ("BETA2916_4_beta_s_nonH", "beta_s_nonH", "source-side non-Hilbert/support current", "|beta_s_nonH| <= |q_nonH_s| + |Delta_W_support_s| + |q_domain_s| + |q_boundary_s|", "MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND", "R10;orbital;source"),
        ("BETA2916_5_beta_t_nonH", "beta_t_nonH", "test/readout non-Hilbert/support current", "|beta_t_nonH| <= |q_nonH_t| + |Delta_W_support_t| + |q_domain_t| + |q_boundary_t|", "MISSING_HIDDEN_TEST_ZERO_OR_NUMERIC_BOUND", "R10;orbital;readout"),
        ("BETA2916_6_beta_abs", "beta_s_abs;beta_t_abs", "absolute no-cancellation source/test envelopes", "beta_s_abs=sum_i |beta_s_i|; beta_t_abs=sum_i |beta_t_i|", "SCHEMA_READY_VALUES_MISSING", "all_local_arenas"),
        ("BETA2916_7_alpha_product", "alpha_X_abs", "claim-safe finite exchange product", "|alpha_X(lambda)| <= |K_X^R10(lambda)| beta_s_abs beta_t_abs + epsilon_tail_abs", "KX_BETA_TAILS_MISSING_NONCLAIM", "R10"),
    ]
    return [
        add_common(
            {
                "beta_id": beta_id,
                "symbol": symbol,
                "definition": definition,
                "formula_or_bound": formula,
                "current_status": status,
                "arena_links": arenas,
                "source_paths": ";".join(str(p) for p in [SRC_1037_BETA, SRC_1038_ACQ, SRC_2915_ACQ]),
                "promotion_allowed_now": False,
            }
        )
        for beta_id, symbol, definition, formula, status, arenas in specs
    ]


def disformal_rows() -> list[dict[str, Any]]:
    specs = [
        ("DIS2916_0_bdis_value", "b_dis", "representative disformal derivative or profile coefficient", "B_g definition; U_mu/current owner; units; source path", "MISSING_DISFORMAL_ZERO_OR_NUMERIC_BOUND", "PPN;clock;orbital"),
        ("DIS2916_1_gamma_kernel", "M_gamma_dis", "PPN gamma response to disformal/common-frame leakage", "gauge-fixed weak-field map to gamma-1; Cassini anchor 2.3e-05", "SOURCE_BACKED_BOUND_ANCHOR_PROJECTION_MISSING", "PPN"),
        ("DIS2916_2_preferred_frame", "M_alpha_i_dis", "preferred-frame alpha1/alpha2/alpha3/xi response to disformal/vector current", "vector/current owner and weak-field kernel", "MISSING_PREFERRED_FRAME_KERNEL", "PPN preferred-frame"),
        ("DIS2916_3_clock_orbit", "M_clock_orbit_dis", "clock/orbital readout response to disformal branch", "clock sensitivities, orbital support, source path", "MISSING_CLOCK_ORBIT_KERNEL", "clock;orbital"),
        ("DIS2916_4_fallback_verdict", "b_dis fallback", "if c_g source-test product remains unsourced, b_dis PPN kernel is the next concrete component", "selected fallback after linear c_g rejection", "DISFORMAL_PPN_KERNEL_STAGED_NONCLAIM", "PPN"),
    ]
    return [
        add_common(
            {
                "kernel_id": kernel_id,
                "symbol": symbol,
                "definition": definition,
                "required_inputs": required,
                "current_status": status,
                "arena_links": arenas,
                "source_paths": ";".join(str(p) for p in [SRC_944_FRAME, SRC_945_BOUNDS, SRC_1038_ACQ, SRC_2888_CSHADOW]),
                "promotion_allowed_now": False,
            }
        )
        for kernel_id, symbol, definition, required, status, arenas in specs
    ]


def runner_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    all_sources_ready = all(bool(row["path_exists"]) and bool(row["anchors_found"]) for row in source_rows)
    specs = [
        ("RUN2916_0_sources", "SOURCE_AUDIT_COMPLETE" if all_sources_ready else "SOURCE_AUDIT_HAS_BLOCKERS", "all cited source paths and anchors", all_sources_ready, "source evidence checked"),
        ("RUN2916_1_product_law", "INVARIANT_PRODUCT_LAW_DERIVED_AS_CONTRACT", "beta_s beta_t finite-exchange law", True, "physics form is fixed but inputs missing"),
        ("RUN2916_2_linear_guard", "NAKED_LINEAR_CG_REJECTED", "linear c_g exception gate", True, "Qbar source leg not declared"),
        ("RUN2916_3_universal_cg", "UNIVERSAL_CG_BRANCH_IS_CG_SQUARED_CONDITIONAL", "c_g Weyl branch", True, "score blocked by missing c_g/profile/K_X"),
        ("RUN2916_4_disformal", "DISFORMAL_PPN_KERNEL_STAGED", "b_dis fallback rows", False, "kernel/projection values missing"),
        ("RUN2916_5_next", "2917_DISFORMAL_OR_CG_SOURCE_LEG_SELECTED", "next target", False, "c_g product law is settled enough to move to source leg or disformal kernel"),
    ]
    return [
        add_common(
            {
                "runner_id": runner_id,
                "status": status,
                "required_components": required,
                "components_evaluable": evaluable,
                "reason": reason,
            }
        )
        for runner_id, status, required, evaluable, reason in specs
    ]


def claim_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2916_0_product_law", "finite exchange uses beta_s beta_t product", "PASS_CONDITIONAL_STRUCTURE", "source-test product law is derived as a contract", True),
        ("CG2916_1_linear_cg_score", "alpha(lambda) may use naked linear c_g", "REJECTED_NONCLAIM", "Qbar source leg is not parent-signed and 1038 quarantine remains active", False),
        ("CG2916_2_cg_score", "c_g branch can be R10-scored", "BLOCKED_NONCLAIM", "c_g, beta profiles, K_X, lambda and source leg are missing", False),
        ("CG2916_3_disformal_score", "b_dis PPN/preferred-frame branch can be scored", "BLOCKED_NONCLAIM", "b_dis value and PPN kernels missing", False),
        ("CG2916_4_DqZ_geometry", "C_shadow/c_g closes DqZ_geometry", "BLOCKED_NONCLAIM", "C_shadow components remain missing", False),
        ("CG2916_5_local_GR_Newton", "local GR/Newton follows after 2916", "BLOCKED_NONCLAIM", "2916 fixes product grammar only; it is not a local-GR proof", False),
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
        ("DEC2916_0_product_result", "source_test_product_law_locked_nonclaim", "A finite c_g-mediated force must be treated as beta_s beta_t or as a sourced source-leg product; the old linear c_g row is not physically safe.", "use product law in all future R10/local rows"),
        ("DEC2916_1_universal_cg", "universal_Weyl_means_cg_squared", "If source and test both see the same universal Weyl frame, both legs carry c_g and the product scales like c_g^2 up to profiles.", "do not score c_g linearly"),
        ("DEC2916_2_exception", "linear_exception_requires_Qbar_source_leg", "A linear form can appear only if Qbar_XH already contains a source leg with source path, units and no double-counting.", "source Qbar leg or reject row"),
        ("DEC2916_3_fallback", "disformal_PPN_kernel_now_concrete", "If c_g remains unsourced, the next concrete shadow component is b_dis because it feeds PPN/preferred-frame tests directly.", "select 2917 disformal/source-leg fork"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2916_0_2917",
                "selection_status": "selected_primary",
                "target_file": "2917-Y5-R2FR-disformal-PPN-kernel-or-cg-source-leg-provenance-fill-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_disformal_PPN_kernel_or_cg_source_leg_provenance_fill_under_AX1090_2917.py",
                "task": "either source a legitimate Qbar_XH/beta_s source leg for the c_g branch, or fill the b_dis preferred-frame/PPN kernel rows as the next C_shadow component",
                "success_condition": "one of: source-leg declaration passes with units/source path/no-double-counting; or b_dis has a theorem-zero route or source-ready PPN kernel rows for gamma/preferred-frame/clock/orbit",
                "fallback_condition": "keep both c_g and b_dis nonclaim and move to q_nonH/support source-current rows",
                "guardrails": "no naked linear c_g scoring; no c_g/b_dis cancellation; no local GR/Newton/R10/PPN claim; no source-less numeric values; no formalization-workbench edits; no GitHub",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("law_copy", OUTPUTS["law"], BRANCH_OUTPUTS["law_copy"]),
        ("beta_copy", OUTPUTS["beta_pack"], BRANCH_OUTPUTS["beta_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination in specs:
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "destination_path": str(destination),
                    "source_exists": source.exists(),
                    "destination_exists": destination.exists(),
                    "destination_parses": csv_parses(destination),
                }
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    law_rows_: list[dict[str, Any]],
    source_leg_rows_: list[dict[str, Any]],
    beta_rows_: list[dict[str, Any]],
    disformal_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    include_doc_check: bool,
) -> list[dict[str, Any]]:
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_outputs_with_validation = [*csv_outputs, OUTPUTS["validation"]]
    law_verdict = next(row for row in law_rows_ if row["law_id"] == "LAW2916_5_verdict")
    source_leg_verdict = next(row for row in source_leg_rows_ if row["gate_id"] == "SLG2916_5_verdict")
    alpha_product = next(row for row in beta_rows_ if row["symbol"] == "alpha_X_abs")
    dis_verdict = next(row for row in disformal_rows_ if row["kernel_id"] == "DIS2916_4_fallback_verdict")
    linear_claim = next(row for row in claim_rows_ if row["gate_id"] == "CG2916_1_linear_cg_score")
    local_claim = next(row for row in claim_rows_ if row["gate_id"] == "CG2916_5_local_GR_Newton")
    required_beta_symbols = {"beta_s_geom", "beta_t_geom", "beta_s_marker", "beta_t_marker", "beta_s_nonH", "beta_t_nonH", "beta_s_abs;beta_t_abs", "alpha_X_abs"}
    beta_symbols = {str(row["symbol"]) for row in beta_rows_}
    generated_paths = [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC]
    checks = [
        ("VAL2916_0_source_paths_exist", all(bool(row["path_exists"]) for row in source_rows), "all cited source paths exist"),
        ("VAL2916_1_source_anchors_found", all(bool(row["anchors_found"]) for row in source_rows), "all source anchors found"),
        ("VAL2916_2_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs_with_validation if path.exists()), "generated CSV outputs parse cleanly"),
        ("VAL2916_3_product_law_contract", law_verdict["current_status"] == "PRODUCT_LAW_DERIVED_AS_CONTRACT_NOT_SCORE_READY", "invariant product law is contract-only"),
        ("VAL2916_4_source_leg_fails", source_leg_verdict["current_status"] == "SOURCE_LEG_GATE_FAILS_CURRENT_MTS", "linear c_g source-leg exception fails"),
        ("VAL2916_5_beta_pack_complete", required_beta_symbols.issubset(beta_symbols), "beta source/test envelope rows complete"),
        ("VAL2916_6_alpha_product_nonclaim", alpha_product["current_status"] == "KX_BETA_TAILS_MISSING_NONCLAIM" and not bool(alpha_product["valid_for_claim"]), "alpha product row remains nonclaim"),
        ("VAL2916_7_disformal_fallback_staged", dis_verdict["current_status"] == "DISFORMAL_PPN_KERNEL_STAGED_NONCLAIM", "disformal PPN fallback staged"),
        (
            "VAL2916_8_claim_gates_safe",
            linear_claim["gate_status"] == "REJECTED_NONCLAIM"
            and local_claim["gate_status"] == "BLOCKED_NONCLAIM"
            and all(not bool(row["claim_allowed"]) and not bool(row["valid_for_claim"]) for row in claim_rows_),
            "linear c_g, local GR/Newton and empirical claims remain blocked",
        ),
        ("VAL2916_9_next_target_selected", next_rows_[0]["route_id"] == "NEXT2916_0_2917" and bool(next_rows_[0]["selected"]), "2917 disformal/source-leg target selected"),
        ("VAL2916_10_branch_copies_parse", all(bool(row["destination_exists"]) and bool(row["destination_parses"]) for row in branch_rows_), "branch copies exist and parse"),
        ("VAL2916_11_no_formalization_outputs", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no generated output path is inside formalization-workbench"),
        ("VAL2916_12_doc_written", DOC.exists() if include_doc_check else True, "markdown checkpoint exists"),
    ]
    rows: list[dict[str, Any]] = [
        {
            "validation_id": validation_id,
            "status": bool(status),
            "detail": detail,
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
        for validation_id, status, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2916_OVERALL",
            "status": all(bool(row["status"]) for row in rows),
            "detail": "2916 validation overall",
            "valid_for_claim": False,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    law_rows_: list[dict[str, Any]],
    source_leg_rows_: list[dict[str, Any]],
    beta_rows_: list[dict[str, Any]],
    disformal_rows_: list[dict[str, Any]],
    runner_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2916_OVERALL")
    text = f"""# 2916 - Y5/R2FR Cshadow c_g Invariant Source-Test Product Or Disformal PPN Kernel Under AX1090

Status: `Y5_R2FR_2916_cg_source_test_product_law_contract_linear_cg_rejected_disformal_PPN_kernel_staged_2917_next`

Claim ceiling: `cg_product_law_nonclaim_only_no_linear_cg_score_no_Cshadow_zero_no_DqZ_geometry_pass_no_local_GR_no_Newton_no_PPN_no_R10_no_GitHub_claim`

Generated UTC: `{RUN_UTC}`

## Summary

2916 fixes the `c_g` grammar. For any finite local exchange branch, the observable source-test force is a product law:

`alpha_X(lambda) = K_X^R10(lambda) beta_s(lambda) beta_t(lambda) + epsilon_tail(lambda)`.

For a universal Weyl/common-frame branch, both the source and the test body carry the same derivative leg, so `beta_s ~ P_s^W c_g` and `beta_t ~ P_t^W c_g`. That makes the force contribution `~ P_s^W P_t^W c_g^2`, not a naked linear `c_g`.

A linear-looking `c_g` row is allowed only if `Qbar_XH` or `beta_s` already contains a source leg with source path, units, normalization and no double counting. Current MTS does not have that source-leg declaration, so the linear shortcut remains rejected.

This is progress, but not a score. The invariant product law is now a contract; `c_g`, `K_X`, `lambda_X`, source/test profiles, `Qbar_XH`, and tail components are still missing. Therefore 2916 stages the beta source-test envelope and, if the c_g source leg remains missing, moves the next concrete shadow component to the disformal PPN kernel.

## Source Register

{md_table(source_rows, ["source_id", "source_path", "anchors_found", "role", "missing_anchors"])}

## Cg Invariant Source-Test Product Law

{md_table(law_rows_, ["law_id", "target", "current_status", "statement", "missing_for_claim", "valid_for_claim"])}

## Qbar Source-Leg Declaration Gate

{md_table(source_leg_rows_, ["gate_id", "gate", "current_status", "required_statement", "if_open", "gate_pass", "valid_for_claim"])}

## Beta Source-Test Envelope Rows

{md_table(beta_rows_, ["beta_id", "symbol", "current_status", "definition", "formula_or_bound", "arena_links", "promotion_allowed_now", "valid_for_claim"])}

## Disformal PPN Kernel Fallback

{md_table(disformal_rows_, ["kernel_id", "symbol", "current_status", "definition", "required_inputs", "arena_links", "promotion_allowed_now", "valid_for_claim"])}

## Runner Status

{md_table(runner_rows_, ["runner_id", "status", "required_components", "components_evaluable", "reason", "valid_for_claim"])}

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

This closes a dangerous loophole. The theory can still pursue a `c_g` finite branch, but only in a physically invariant form. Either the source leg is explicitly present and sourced, or the force law is a source-test product. No future R10/local row should use `alpha ~ c_g` naked.

The local-GR programme is still not proved, but it is safer now: a fake one-leg coupling cannot accidentally masquerade as an empirical prediction.

## Not Claimed

- `c_g=0` is not derived.
- finite `c_g` is not numeric or score-ready.
- naked linear `c_g` R10/source-test scoring is explicitly rejected.
- `b_dis` PPN/preferred-frame kernels are staged only as nonclaim fallback.
- `DqZ_geometry=0`, Newton, PPN, R10, WEP, clock/EM, orbital or local-GR reduction is not claimed.
- No public/GitHub action is implied.
- No file in `formalization-workbench` is modified by this checkpoint.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    law_rows_ = law_rows()
    source_leg_rows_ = source_leg_rows()
    beta_rows_ = beta_pack_rows()
    disformal_rows_ = disformal_rows()
    runner_rows_ = runner_rows(source_rows)
    claim_rows_ = claim_rows()
    decision_rows_ = decision_rows()
    next_rows_ = next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["law"], law_rows_)
    write_csv(OUTPUTS["source_leg"], source_leg_rows_)
    write_csv(OUTPUTS["beta_pack"], beta_rows_)
    write_csv(OUTPUTS["disformal"], disformal_rows_)
    write_csv(OUTPUTS["runner"], runner_rows_)
    write_csv(OUTPUTS["claims"], claim_rows_)
    write_csv(OUTPUTS["decision"], decision_rows_)
    write_csv(OUTPUTS["next"], next_rows_)

    branch_rows_ = branch_rows()
    write_csv(OUTPUTS["branches"], branch_rows_)

    validation_rows_ = validation_rows(
        source_rows,
        law_rows_,
        source_leg_rows_,
        beta_rows_,
        disformal_rows_,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=False,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        law_rows_,
        source_leg_rows_,
        beta_rows_,
        disformal_rows_,
        runner_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    validation_rows_ = validation_rows(
        source_rows,
        law_rows_,
        source_leg_rows_,
        beta_rows_,
        disformal_rows_,
        claim_rows_,
        next_rows_,
        branch_rows_,
        include_doc_check=True,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)
    write_doc(
        source_rows,
        law_rows_,
        source_leg_rows_,
        beta_rows_,
        disformal_rows_,
        runner_rows_,
        claim_rows_,
        decision_rows_,
        next_rows_,
        branch_rows_,
        validation_rows_,
    )

    overall = next(row for row in validation_rows_ if row["validation_id"] == "VAL2916_OVERALL")
    if not bool(overall["status"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
