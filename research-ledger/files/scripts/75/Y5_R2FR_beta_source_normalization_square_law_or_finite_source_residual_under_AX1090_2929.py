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

CHECKPOINT = "2929"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2929-Y5-R2FR-beta-source-normalization-square-law-or-finite-source-residual-under-AX1090.md"

SRC_2928_DOC = ROOT / "2928-Y5-R2FR-RV2925-alpha3-stationary-flux-zero-or-kappa-ellJ-coupling-baseline-under-AX1090.md"
SRC_2928_BETA = RESIDUALS / "P8_Y5_R2FR_2928_BETA_SOURCE_NORMALIZATION_HANDOFF.csv"
SRC_2928_NEXT = RESIDUALS / "P8_Y5_R2FR_2928_NEXT_TARGET.csv"
SRC_2928_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2928_VALIDATION.csv"

SRC_2920_DOC = ROOT / "2920-Y5-R2FR-beta-source-normalization-second-order-kernel-or-parent-square-law-under-AX1090.md"
SRC_2920_SQUARE = RESIDUALS / "P8_Y5_R2FR_2920_PARENT_SQUARE_LAW_AUDIT.csv"
SRC_2920_KERNEL = RESIDUALS / "P8_Y5_R2FR_2920_BETA_SECOND_ORDER_SOURCE_NORMALIZATION_KERNEL.csv"
SRC_2920_QUEUE = RESIDUALS / "P8_Y5_R2FR_2920_SOURCE_NORMALIZED_NEWTON_GAUSS_ORBITAL_SCORECARD_QUEUE.csv"
SRC_2920_CLAIMS = RESIDUALS / "P8_Y5_R2FR_2920_CLAIM_GATES.csv"
SRC_2920_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2920_VALIDATION.csv"

SRC_2921_DOC = ROOT / "2921-Y5-R2FR-source-normalized-Newton-Gauss-orbital-scorecard-or-parent-source-mass-identity-under-AX1090.md"
SRC_2921_IDENTITY = RESIDUALS / "P8_Y5_R2FR_2921_PARENT_SOURCE_MASS_IDENTITY_AUDIT.csv"
SRC_2921_PG = RESIDUALS / "P8_Y5_R2FR_2921_POISSON_GAUSS_ORBITAL_BRIDGE_AUDIT.csv"
SRC_2921_SCORECARD = RESIDUALS / "P8_Y5_R2FR_2921_SOURCE_NORMALIZED_NEWTON_SCORECARD_ROWS.csv"
SRC_2921_NEXT = RESIDUALS / "P8_Y5_R2FR_2921_NEXT_TARGET.csv"

SRC_2922_DOC = ROOT / "2922-Y5-R2FR-Hamiltonian-sector-owner-or-source-mass-first-row-under-AX1090.md"
SRC_2922_OWNER = RESIDUALS / "P8_Y5_R2FR_2922_HAMILTONIAN_SECTOR_OWNER_AUDIT.csv"
SRC_2922_SCHEMA = RESIDUALS / "P8_Y5_R2FR_2922_SOURCE_MASS_FIRST_ROW_SCHEMA.csv"
SRC_2924_DOC = ROOT / "2924-Y5-R2FR-parent-Hcore-coefficient-map-or-finite-source-mass-first-row-fill-under-AX1090.md"
SRC_2924_REDUCTION = RESIDUALS / "P8_Y5_R2FR_2924_MTS_TO_EH_REDUCTION_CONTRACT.csv"
SRC_2925_DOC = ROOT / "2925-Y5-R2FR-MTS-to-EH-reduction-morphism-or-extra-sector-silence-proof-under-AX1090.md"
SRC_2925_VECTOR = RESIDUALS / "P8_Y5_R2FR_2925_REDUCTION_RESIDUAL_VECTOR.csv"
SRC_2926_DOC = ROOT / "2926-Y5-R2FR-parent-object-no-hidden-visible-hom-derivation-or-reduction-residual-first-fill-under-AX1090.md"
SRC_2926_RV = RESIDUALS / "P8_Y5_R2FR_2926_RV2925_FIRST_FILL_ATTEMPT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2929_SOURCE_REGISTER.csv",
    "beta_reentry": RESIDUALS / "P8_Y5_R2FR_2929_BETA_SQUARE_LAW_REENTRY_AUDIT.csv",
    "beta_vector": RESIDUALS / "P8_Y5_R2FR_2929_BETA_FINITE_RESIDUAL_VECTOR.csv",
    "newton_handoff": RESIDUALS / "P8_Y5_R2FR_2929_NEWTON_GAUSS_ORBITAL_HANDOFF.csv",
    "rv_impact": RESIDUALS / "P8_Y5_R2FR_2929_RV2925_REDUCTION_IMPACT.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2929_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2929_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2929_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2929_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2929_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "beta_reentry_copy": PARENT_ACTION / "Beta_square_law_reentry_2929_NONCLAIM.csv",
    "beta_vector_copy": LOCAL_BOUNDS / "Beta_finite_residual_vector_2929_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2929_SOURCE_OWNER_HCORE_TO_BETA_DENOMINATOR_NEXT_NONCLAIM.csv",
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


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


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
        ("SRC2929_00_2928_doc", SRC_2928_DOC, "NEXT2928_0_2929;B_source=A_source^2;Validation overall: `True`", "2928 selected beta/source-normalization square law as next target"),
        ("SRC2929_01_2928_beta", SRC_2928_BETA, "BH2928_BFB2919_0_beta_law;BH2928_BFB2919_1_source_residual;BH2928_BFB2919_7_total", "machine-readable beta handoff from 2928"),
        ("SRC2929_02_2928_next", SRC_2928_NEXT, "NEXT2928_0_2929;derive B_source=A_source^2", "machine-readable 2929 target"),
        ("SRC2929_03_2928_validation", SRC_2928_VALIDATION, "VAL2928_OVERALL;True", "2928 validation summary"),
        ("SRC2929_04_2920_doc", SRC_2920_DOC, "beta_eff = B_source/A_source^2;PARENT_SQUARE_LAW_NOT_PROVED_BETA_NONCLAIM;NEXT2920_0_2921", "prior beta square-law result to import rather than rerun"),
        ("SRC2929_05_2920_square", SRC_2920_SQUARE, "SQA2920_0_ppn_extraction_law;SQA2920_3_parent_square_source;SQA2920_8_verdict", "parent square-law audit"),
        ("SRC2929_06_2920_kernel", SRC_2920_KERNEL, "B2K2920_0_delta_beta_source;B2K2920_6_Delta_beta_total_abs", "finite beta residual vector"),
        ("SRC2929_07_2920_queue", SRC_2920_QUEUE, "NGQ2920_4_second_order_square_law;NGQ2920_5_scorecard_verdict", "source-normalized Newton/Gauss/orbital queue"),
        ("SRC2929_08_2920_claims", SRC_2920_CLAIMS, "CG2920_0_beta_square_law;CG2920_2_newton_source_normalized", "2920 claim gates"),
        ("SRC2929_09_2920_validation", SRC_2920_VALIDATION, "VAL2920_3_ppn_extraction_law_retained;VAL2920_4_square_law_not_claimed", "2920 validation summary"),
        ("SRC2929_10_2921_doc", SRC_2921_DOC, "mu_obs = G0 M_H;PARENT_SOURCE_MASS_IDENTITY_NOT_DERIVED_SCORECARD_STAGED;NEXT2921_0_2922", "source-normalized Newton/source-mass identity audit"),
        ("SRC2929_11_2921_identity", SRC_2921_IDENTITY, "PSM2921_0_target_identity;PSM2921_10_verdict", "parent source-mass identity rows"),
        ("SRC2929_12_2921_pg", SRC_2921_PG, "PG2921_0_Hamiltonian_charge_input;PG2921_10_residual_fallback", "Poisson/Gauss/orbital bridge contract"),
        ("SRC2929_13_2921_scorecard", SRC_2921_SCORECARD, "SN2921_0_dln_Geff_dt;SN2921_9_total_guard", "source-normalized Newton residual scorecard"),
        ("SRC2929_14_2922_doc", SRC_2922_DOC, "OWNER_THEOREM_NOT_DERIVED_FIRST_ROW_TEMPLATE_REQUIRED;M_H_ref;Pi_M^H", "Hamiltonian owner/source-row bottleneck"),
        ("SRC2929_15_2922_owner", SRC_2922_OWNER, "HOA2922_0_target;HOA2922_10_verdict", "Hamiltonian owner audit"),
        ("SRC2929_16_2922_schema", SRC_2922_SCHEMA, "SMR2922_0_identity;SMR2922_8_qRhat", "source-mass first-row schema"),
        ("SRC2929_17_2924_doc", SRC_2924_DOC, "Hcore;source;Validation overall", "Hcore coefficient map / finite source-mass row checkpoint"),
        ("SRC2929_18_2924_reduction", SRC_2924_REDUCTION, "RED2924_0_metric_identification;RED2924_10_total_verdict", "MTS-to-EH reduction contract"),
        ("SRC2929_19_2925_doc", SRC_2925_DOC, "MTS-to-EH;reduction;Validation overall", "MTS-to-EH reduction vector context"),
        ("SRC2929_20_2925_vector", SRC_2925_VECTOR, "RV2925_0_metric_readout;RV2925_TOTAL", "MTS-to-EH residual vector"),
        ("SRC2929_21_2926_doc", SRC_2926_DOC, "RV2925_0_metric_readout;AX1090_NOT_DERIVED_FIRST_RESIDUAL_FILL_REQUIRED;NEXT2926_0_2927", "first metric-readout residual fill selection"),
        ("SRC2929_22_2926_rv", SRC_2926_RV, "RVF2926_0_selected_component;RVF2926_3_acceptance_gate", "RV2925 first fill selection"),
    ]
    rows = []
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


def beta_reentry_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "BSR2929_0_2928_handoff",
            "2928 beta square-law handoff",
            "derive B_source=A_source^2 or stage finite beta/source-normalization residuals",
            "PASS_IMPORT",
            "2928 already selected the right target; 2929 binds it to the existing 2920 result",
            True,
            False,
        ),
        (
            "BSR2929_1_exact_extraction_law",
            "source-normalized PPN beta extraction",
            "beta_eff = B_source/A_source^2",
            "PASS_KINEMATIC_FROM_2893_AND_2920",
            "this is usable grammar, not a GR-reduction proof",
            True,
            False,
        ),
        (
            "BSR2929_2_square_law_theorem",
            "parent second-order source coefficient squares first-order source coefficient",
            "B_source = A_source^2",
            "NOT_DERIVED_IN_CURRENT_CORPUS",
            "2920 already found this missing; 2929 must not repackage it as success",
            False,
            False,
        ),
        (
            "BSR2929_3_source_normalized_Newton",
            "measured orbital source equals parent Hamiltonian source",
            "mu_obs = G0*M_H = G_eff*M_source_parent with epsilon_SN=0",
            "PARENT_SOURCE_MASS_IDENTITY_NOT_DERIVED",
            "2921 shows a clean conditional bridge but unsigned source-owner premises",
            False,
            False,
        ),
        (
            "BSR2929_4_no_measured_GM_smuggling",
            "measured GM is not allowed to absorb source residuals",
            "epsilon_SN and delta_beta_source remain explicit residual heads",
            "PASS_GUARDRAIL",
            "keeps the route from becoming a calibration trick",
            True,
            False,
        ),
        (
            "BSR2929_5_no_loop_rule",
            "do not rerun the 2920 square-law attempt as if fresh",
            "import result: extraction law yes, square theorem no",
            "REENTRY_DECISION",
            "the next forward move is source-owner/Hcore denominator binding, not another beta prose pass",
            True,
            False,
        ),
        (
            "BSR2929_6_verdict",
            "current beta/local-GR square-law status",
            "beta_eff=1 requires B_source=A_source^2 plus source-normalized Newton",
            "BETA_SQUARE_LAW_BLOCKED_NONCLAIM",
            "retain finite residual vector and keep beta, Newton, PPN and local-GR claims closed",
            False,
            False,
        ),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "clause": clause,
                "math_form": math_form,
                "current_status": current_status,
                "reason": reason,
                "condition_passed": condition_passed,
                "adopted_for_claim": adopted_for_claim,
                "source_paths": ";".join(str(path) for path in [SRC_2928_BETA, SRC_2920_SQUARE, SRC_2921_IDENTITY]),
            }
        )
        for audit_id, clause, math_form, current_status, reason, condition_passed, adopted_for_claim in specs
    ]


def beta_vector_rows() -> list[dict[str, Any]]:
    source_rows = read_csv_rows(SRC_2920_KERNEL)
    fallback_rows = [
        ("B2K2920_0_delta_beta_source", "delta_beta_source", "B_source/A_source^2 - 1", "MISSING_A_SOURCE_B_SOURCE_OR_PARENT_SQUARE_THEOREM", "derive B_source=A_source^2 or provide numeric source-backed A_source/B_source"),
        ("B2K2920_1_delta_beta_operator", "delta_beta_operator_R11", "sum_abs(delta_beta_source_R11,delta_beta_R2_fR,delta_beta_boundary_domain,delta_beta_scalar_class,delta_beta_readout_connection)", "MISSING_R11_COMPONENT_VALUES_OR_EH_NOHAIR", "derive no-R11/no-nonEH theorem or source-backed finite values"),
        ("B2K2920_2_delta_beta_q_loc", "delta_beta_q_loc", "physical U2 projection of P_loc(nabla Gamma_eff - div Khat)", "MISSING_SECOND_ORDER_QLOC_PROJECTION", "extend local q_loc theorem to second-order beta projection"),
        ("B2K2920_3_delta_beta_boundary_domain", "delta_beta_boundary_domain", "boundary/domain/projector quadratic stress beta projection", "MISSING_BOUNDARY_DOMAIN_ZERO_OR_COEFFICIENT_MAP", "prove boundary/domain silence or source-backed coefficient rows"),
        ("B2K2920_4_delta_beta_readout", "delta_beta_readout", "second-order source metric to observed isotropic PPN readout mismatch", "MISSING_SAME_READOUT_THEOREM_THROUGH_O_U2", "derive same-readout map through O(U^2)"),
        ("B2K2920_5_epsilon_SN", "epsilon_SN", "(mu_obs - G_eff M_H)/(G_eff M_H)", "MISSING_GAUSS_ORBITAL_SOURCE_CURRENT_SCORECARD", "close source-normalized Newton/Gauss/orbital identity"),
        ("B2K2920_6_Delta_beta_total_abs", "Delta_beta_total_abs", "sum_abs(delta_beta_source,delta_beta_operator_R11,delta_beta_q_loc,delta_beta_boundary_domain,delta_beta_readout,epsilon_SN)", "BETA_SOURCE_NORMALIZATION_KERNEL_RETAINED_NONCLAIM", "all heads theorem-zero or finite/source-backed before scoring"),
    ]
    if source_rows:
        normalized_rows = [
            (
                row.get("kernel_id", ""),
                row.get("symbol", ""),
                row.get("formula_or_map", ""),
                row.get("current_status", ""),
                row.get("next_requirement", ""),
            )
            for row in source_rows
        ]
    else:
        normalized_rows = fallback_rows

    rows = []
    for kernel_id, symbol, formula_or_map, current_status, next_requirement in normalized_rows:
        rows.append(
            add_common(
                {
                    "residual_id": kernel_id.replace("B2K2920", "BFR2929"),
                    "imported_kernel_id": kernel_id,
                    "symbol": symbol,
                    "formula_or_map": formula_or_map,
                    "status_2920": current_status,
                    "status_2929": "RETAINED_ACTIVE_NONCLAIM",
                    "next_requirement": next_requirement,
                    "beta_bound_abs": "7.8e-05",
                    "source_paths": ";".join(str(path) for path in [SRC_2920_KERNEL, SRC_2928_BETA, SRC_2921_SCORECARD]),
                    "numeric_value_present": False,
                    "theorem_zero": False,
                    "selected_for_next_fill": symbol in {"delta_beta_source", "epsilon_SN", "Delta_beta_total_abs"},
                }
            )
        )
    return rows


def newton_handoff_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "NGH2929_0_2921_conditional_bridge",
            "Hamiltonian-to-Poisson/Gauss/orbital bridge",
            "if one parent source charge feeds Poisson, Gauss surface flux and orbital acceleration, then mu_obs=G_eff*M_H",
            "PASS_CONDITIONAL_THEOREM_ONLY",
            "algebra is not the weak point; source ownership is",
            True,
            False,
        ),
        (
            "NGH2929_1_source_owner_gap",
            "same-frame parent source mass ownership",
            "L_X, Theta_X, Q_X, B_ref, B_class, tau, M_H_ref, Pi_M^H owned together",
            "OWNER_THEOREM_NOT_DERIVED",
            "2922 stages schema and owner map, but not a signed parent package",
            False,
            False,
        ),
        (
            "NGH2929_2_hcore_gap",
            "Hcore coefficient/source denominator map",
            "A_source and B_source must be read from the same source-normalized parent family",
            "HCORE_SOURCE_MAP_NOT_CLOSED",
            "without this, beta square-law cannot be physically scored",
            False,
            False,
        ),
        (
            "NGH2929_3_rv2925_context",
            "MTS-to-EH local reduction vector",
            "RV2925_0_metric_readout plus DqZ/C_shadow/boundary/readout heads",
            "SOURCE_READY_NOT_SCORE_READY",
            "2926-2928 selected concrete residual heads but not numeric MTS predictions",
            False,
            False,
        ),
        (
            "NGH2929_4_next_forward_move",
            "bind source owner/Hcore denominator to beta and RV2925",
            "source-normalized Newton first, beta second, alpha3/readout as independent guardrails",
            "SELECT_2930_REENTRY_BINDING",
            "this is the leap forward: one denominator/source coefficient must become parent-signed or finite/source-backed",
            True,
            False,
        ),
    ]
    return [
        add_common(
            {
                "handoff_id": handoff_id,
                "target": target,
                "required_identity": required_identity,
                "current_status": current_status,
                "reason": reason,
                "condition_passed": condition_passed,
                "adopted_for_claim": adopted_for_claim,
                "source_paths": ";".join(str(path) for path in [SRC_2921_DOC, SRC_2922_DOC, SRC_2924_DOC, SRC_2926_DOC]),
            }
        )
        for handoff_id, target, required_identity, current_status, reason, condition_passed, adopted_for_claim in specs
    ]


def rv_impact_rows() -> list[dict[str, Any]]:
    specs = [
        ("RVI2929_0_beta", "beta_eff", "beta_eff=B_source/A_source^2 retained; beta_eff=1 not proved", "BLOCKED_NONCLAIM", "no beta/PPN pass"),
        ("RVI2929_1_newton", "source_normalized_Newton", "mu_obs=G0*M_H remains conditional because parent source mass is unsigned", "BLOCKED_NONCLAIM", "no Newton pass"),
        ("RVI2929_2_alpha3", "alpha3", "2928 stationary result kills only one q_loc head conditionally; total alpha3 remains active", "BLOCKED_NONCLAIM", "no alpha3 pass"),
        ("RVI2929_3_rv2925", "RV2925_0_metric_readout", "metric-readout residual is source-ready but has no numeric/source-backed MTS upper bound", "SOURCE_READY_NOT_SCORE_READY", "no local-GR pass"),
        ("RVI2929_4_progress", "GR_reduction_spine", "bottleneck is now source ownership and source-normalized denominator, not algebraic PPN grammar", "FORWARD_PROGRESS", "select source-owner/Hcore-to-beta-denominator binding"),
    ]
    return [
        add_common(
            {
                "impact_id": impact_id,
                "component": component,
                "result": result,
                "current_status": current_status,
                "claim_effect": claim_effect,
                "source_paths": ";".join(str(path) for path in [SRC_2928_DOC, SRC_2920_DOC, SRC_2921_DOC, SRC_2926_DOC]),
            }
        )
        for impact_id, component, result, current_status, claim_effect in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2929_0_extraction_law", "beta_eff=B_source/A_source^2 is retained as exact extraction grammar", "PASS_NONCLAIM_STRUCTURE", "owned by 2893/2920 and re-bound to 2928", True, False),
        ("CG2929_1_square_law", "B_source=A_source^2 is parent-derived", "BLOCKED_NONCLAIM", "2920 says NOT_DERIVED; 2929 imports that verdict", False, False),
        ("CG2929_2_beta_score", "beta_eff-1 can be scored under the 7.8e-05 comparator", "BLOCKED_NONCLAIM", "A_source/B_source or source-backed finite residual rows missing", False, False),
        ("CG2929_3_source_normalized_Newton", "mu_obs=G0*M_H source-normalized Newton passes", "BLOCKED_NONCLAIM", "2921 conditional bridge lacks signed source-owner package", False, False),
        ("CG2929_4_local_GR_Newton", "local GR/Newton follows after 2929", "BLOCKED_NONCLAIM", "source mass, beta, alpha3/readout, and reduction vector remain open", False, False),
        ("CG2929_5_no_loop", "2929 avoids re-running a closed nonclaim beta square-law audit", "PASS_GUARDRAIL", "moves to source-owner/Hcore denominator binding", True, False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "current_status": current_status,
                "reason": reason,
                "structure_passed": structure_passed,
                "claim_passed": claim_passed,
            }
        )
        for gate_id, claim, current_status, reason, structure_passed, claim_passed in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2929_0_import_2920", "retain the beta extraction law but not the beta=1 claim", "2920 already proved the grammar and blocked the square-law theorem", "use beta_eff=B_source/A_source^2 as a ledger equation only", False),
        ("DEC2929_1_no_smuggling", "do not absorb source residuals into measured GM", "epsilon_SN and delta_beta_source are exactly the danger zone", "keep source-normalized Newton as an explicit gate", False),
        ("DEC2929_2_no_looping", "do not circle 2920 or 2921 without new parent source input", "the missing object is not another explanation of beta; it is the source-owner/Hcore denominator certificate", "select 2930 binding target", False),
        ("DEC2929_3_project_state", "overall project is closer but still nonclaim", "the local-GR path now has a precise bottleneck and independent alpha3/beta/Newton guards", "advance by deriving or sourcing one denominator/source coefficient", False),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
                "valid_for_claim": valid_for_claim,
            }
        )
        for decision_id, decision, because, next_action, valid_for_claim in specs
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2929_0_2930",
                "selection": "selected_primary",
                "target_doc": "2930-Y5-R2FR-source-owner-Hcore-to-beta-denominator-binding-or-finite-local-residual-first-value-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_source_owner_Hcore_to_beta_denominator_binding_or_finite_local_residual_first_value_under_AX1090_2930.py",
                "objective": "bind the 2921-2926 source-owner/Hcore chain back into the 2928 beta/RV2925 local-reduction gates: derive a parent-signed same-frame source denominator/coefficient map for A_source, B_source, kappa_MTS, or ell_J, or stage the first finite source-backed local residual value without measured-GM absorption",
                "acceptance_gate": "one source-normalization denominator or local residual head becomes parent-signed/theorem-zero or finite/source-backed with units and no-cancellation policy; otherwise beta/Newton/local-GR remain blocked and the next empirical residual is selected",
                "fallback": "if no parent coefficient can be signed, move to the first source-backed finite value for delta_beta_source, epsilon_SN, Dln(kappa_MTS), or Dln(ell_J)",
                "valid_for_claim": False,
            }
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("beta_reentry_copy", OUTPUTS["beta_reentry"], BRANCH_OUTPUTS["beta_reentry_copy"]),
        ("beta_vector_copy", OUTPUTS["beta_vector"], BRANCH_OUTPUTS["beta_vector_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
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


def validation_rows() -> list[dict[str, Any]]:
    source_rows = read_csv_rows(OUTPUTS["sources"])
    beta_reentry = read_csv_rows(OUTPUTS["beta_reentry"])
    beta_vector = read_csv_rows(OUTPUTS["beta_vector"])
    newton_handoff = read_csv_rows(OUTPUTS["newton_handoff"])
    claims = read_csv_rows(OUTPUTS["claims"])
    next_rows = read_csv_rows(OUTPUTS["next"])
    branch_rows = read_csv_rows(OUTPUTS["branches"])

    required_symbols = {
        "delta_beta_source",
        "delta_beta_operator_R11",
        "delta_beta_q_loc",
        "delta_beta_boundary_domain",
        "delta_beta_readout",
        "epsilon_SN",
        "Delta_beta_total_abs",
    }
    vector_symbols = {row.get("symbol", "") for row in beta_vector}
    active_claim_promotions = [
        row
        for row in beta_vector
        if as_bool(row.get("numeric_value_present")) or as_bool(row.get("theorem_zero")) or as_bool(row.get("valid_for_claim"))
    ]
    all_paths = [Path(row["source_path"]) for row in source_rows if row.get("source_path")]
    no_formalization_2929 = not list(FORMALIZATION.rglob("*2929*")) if FORMALIZATION.exists() else True

    checks = [
        ("VAL2929_0_sources_exist", all(as_bool(row.get("path_exists")) for row in source_rows), "every cited source path exists"),
        ("VAL2929_1_source_anchors_found", all(as_bool(row.get("anchors_found")) for row in source_rows), "every cited source anchor is present"),
        ("VAL2929_2_outputs_parse", all(csv_parses(path) for path in OUTPUTS.values()), "all 2929 CSV outputs parse"),
        ("VAL2929_3_doc_exists", DOC.exists(), "2929 markdown checkpoint exists"),
        ("VAL2929_4_extraction_law_retained", any(row.get("audit_id") == "BSR2929_1_exact_extraction_law" and row.get("current_status") == "PASS_KINEMATIC_FROM_2893_AND_2920" for row in beta_reentry), "beta_eff extraction law retained"),
        ("VAL2929_5_square_law_not_claimed", any(row.get("audit_id") == "BSR2929_2_square_law_theorem" and row.get("current_status") == "NOT_DERIVED_IN_CURRENT_CORPUS" and not as_bool(row.get("adopted_for_claim")) for row in beta_reentry), "B_source=A_source^2 remains unclaimed"),
        ("VAL2929_6_beta_vector_complete", required_symbols <= vector_symbols, "finite beta residual vector has all required heads"),
        ("VAL2929_7_no_beta_head_promoted", not active_claim_promotions, "no finite beta head is numeric/theorem-zero/valid-for-claim"),
        ("VAL2929_8_newton_handoff_active", any(row.get("handoff_id") == "NGH2929_1_source_owner_gap" and row.get("current_status") == "OWNER_THEOREM_NOT_DERIVED" for row in newton_handoff), "source-owner gap is carried forward"),
        ("VAL2929_9_claims_closed", all(not as_bool(row.get("claim_passed")) for row in claims), "all claim gates remain closed"),
        ("VAL2929_10_next_target_selected", any(row.get("next_id") == "NEXT2929_0_2930" for row in next_rows), "2930 next target selected"),
        ("VAL2929_11_branch_copies_parse", all(as_bool(row.get("destination_parses")) for row in branch_rows), "branch copies parse cleanly"),
        ("VAL2929_12_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in OUTPUTS.values()) and all(is_under(path, ROOT) for path in BRANCH_OUTPUTS.values()), "all outputs remain under post-checkpoint-work"),
        ("VAL2929_13_sources_not_formalization", all(not is_under(path, FORMALIZATION) for path in all_paths) if FORMALIZATION.exists() else True, "no formalization-workbench source/output dependency"),
        ("VAL2929_14_no_formalization_2929_outputs", no_formalization_2929, "no formalization-workbench 2929 outputs"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "blocking_if_false": True,
            }
        )
        for validation_id, passed, check in checks
    ]
    rows.append(
        add_common(
            {
                "validation_id": "VAL2929_OVERALL",
                "passed": overall,
                "check": "2929 validation overall",
                "blocking_if_false": True,
            }
        )
    )
    return rows


def write_doc() -> None:
    source_rows = read_csv_rows(OUTPUTS["sources"])
    beta_reentry = read_csv_rows(OUTPUTS["beta_reentry"])
    beta_vector = read_csv_rows(OUTPUTS["beta_vector"])
    newton_handoff = read_csv_rows(OUTPUTS["newton_handoff"])
    rv_impact = read_csv_rows(OUTPUTS["rv_impact"])
    claims = read_csv_rows(OUTPUTS["claims"])
    decisions = read_csv_rows(OUTPUTS["decision"])
    next_rows = read_csv_rows(OUTPUTS["next"])
    branches = read_csv_rows(OUTPUTS["branches"])
    validation = read_csv_rows(OUTPUTS["validation"])
    overall = next((row for row in validation if row.get("validation_id") == "VAL2929_OVERALL"), {})

    sections = [
        "# 2929 - Y5/R2FR Beta Source-Normalization Square Law Or Finite Source Residual Under AX1090",
        "",
        "Status: `Y5_R2FR_2929_beta_square_law_reentry_bound_to_2920_source_owner_Hcore_2930_next`",
        "",
        "Claim ceiling: `beta_extraction_law_yes_parent_square_law_no_source_owner_no_Newton_no_beta_no_alpha3_no_local_GR_no_PPN_no_R10_no_GitHub_claim`",
        "",
        "## Summary",
        "",
        "2929 is deliberately a binding checkpoint, not another pass around the same lamppost. 2928 selected the beta/source-normalization square law as the next local-GR reduction target. The prior 2920 audit already answered the immediate question: the extraction law is usable,",
        "",
        "`beta_eff = B_source/A_source^2`,",
        "",
        "but the parent square law",
        "",
        "`B_source = A_source^2`",
        "",
        "is not derived in the current corpus. Therefore 2929 keeps beta nonclaim, carries the finite beta residual vector forward, and redirects the next derivation to the actual root: same-frame source ownership and the Hcore/source-denominator map. No measured-`GM` absorption is allowed to hide `delta_beta_source` or `epsilon_SN`.",
        "",
        "This is progress in the GR/Newton direction because the obstruction is now precise: source-normalized Newton first, beta second, and `alpha3`/metric-readout as independent guardrails.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"]),
        "",
        "## Beta Square-Law Reentry Audit",
        "",
        md_table(beta_reentry, ["audit_id", "clause", "math_form", "current_status", "reason", "condition_passed", "adopted_for_claim"]),
        "",
        "## Finite Beta Residual Vector",
        "",
        md_table(beta_vector, ["residual_id", "symbol", "formula_or_map", "status_2929", "next_requirement", "beta_bound_abs", "numeric_value_present", "theorem_zero", "selected_for_next_fill"]),
        "",
        "## Newton/Gauss/Orbital Handoff",
        "",
        md_table(newton_handoff, ["handoff_id", "target", "required_identity", "current_status", "reason", "condition_passed", "adopted_for_claim"]),
        "",
        "## RV2925 Reduction Impact",
        "",
        md_table(rv_impact, ["impact_id", "component", "result", "current_status", "claim_effect"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "current_status", "reason", "structure_passed", "claim_passed"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["next_id", "selection", "target_doc", "target_script", "objective", "acceptance_gate", "fallback", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(branches, ["copy_id", "source_path", "destination_path", "source_exists", "destination_exists", "destination_parses"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["validation_id", "passed", "check", "blocking_if_false"]),
        "",
        f"Validation overall: `{overall.get('passed', False)}`.",
        "",
        "## Bottom Line",
        "",
        "The project is closer, but not because beta passed. It is closer because the beta gate stopped being vague. The exact local PPN extraction law is now pinned to the active 2928 branch, while the missing theorem is named without wiggle room: `B_source=A_source^2` in the same observed-`U` and same source-denominator convention.",
        "",
        "The next useful move is not another broad philosophical derivation. It is to make one source object real: either parent-sign the same-frame source denominator/coefficient map for `A_source`, `B_source`, `kappa_MTS`, or `ell_J`, or fill the first finite source-backed residual row under the no-cancellation policy.",
        "",
        "## Non-Claims",
        "",
        "- no `B_source=A_source^2` theorem is claimed;",
        "- no `beta_eff=1` or PPN beta pass is claimed;",
        "- no source-normalized Newton/Gauss/orbital pass is claimed;",
        "- no total `alpha3` pass is claimed;",
        "- no local-GR/Newton reduction claim is made;",
        "- no public/GitHub claim is made.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["beta_reentry"], beta_reentry_rows())
    write_csv(OUTPUTS["beta_vector"], beta_vector_rows())
    write_csv(OUTPUTS["newton_handoff"], newton_handoff_rows())
    write_csv(OUTPUTS["rv_impact"], rv_impact_rows())
    write_csv(OUTPUTS["claims"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    write_csv(OUTPUTS["branches"], branch_copy_rows())
    DOC.write_text("# 2929 preflight\n", encoding="utf-8")
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()

    validation = read_csv_rows(OUTPUTS["validation"])
    overall = next((row for row in validation if row.get("validation_id") == "VAL2929_OVERALL"), {})
    print(f"wrote {DOC}")
    print(f"validation overall: {overall.get('passed')}")


if __name__ == "__main__":
    main()
