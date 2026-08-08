from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2673"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2673-Y5-R2FR-JX-source-zero-or-qbarXT-first-coefficient-row.md"

CHECKPOINT = "2673"
BRANCH_ID = "Y5_R2FR_JX_SOURCE_ZERO_OR_QBARXT_ROW_2673"
PREFIX = "P8_Y5_R2FR_JX_QBARXT_2673"
MISSING_TOKENS = (
    "MISSING",
    "UNSIGNED",
    "NOT_PARENT",
    "NOT_DERIVED",
    "BLOCKED",
    "OPEN",
    "VALUES_MISSING",
    "NONCLAIM",
)

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "source_zero_audit": RESIDUALS / f"{PREFIX}_SOURCE_ZERO_AUDIT.csv",
    "matter_channel_audit": RESIDUALS / f"{PREFIX}_MATTER_CHANNEL_AUDIT.csv",
    "coefficient_template": RESIDUALS / f"{PREFIX}_FIRST_COEFFICIENT_TEMPLATE_NONCLAIM.csv",
    "alpha_impact": RESIDUALS / f"{PREFIX}_ALPHA_IMPACT_LEDGER.csv",
    "runner_results": RESIDUALS / f"{PREFIX}_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2673_JX_QBARXT_COUPLING_QUEUE_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "JX_qbarXT_coupling_2673_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "QBARXT_FIRST_COEFFICIENT_TEMPLATE_2673_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2673_JX_QBARXT.csv",
    "quarantine": QUARANTINE / "P8_Y5_2673_COUPLING_RUNNER_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2672_doc": {
        "path": ROOT / "2672-Y5-R2FR-positive-scalar-nohair-operator-source-boundary-lock-or-alpha-row.md",
        "needles": ["NEXT2672_0_selected", "COUP2672_1_qbarXT", "SNH2672_5_JX_zero"],
        "role": "handoff selecting J_X/qbar_XT coupling as the next target",
    },
    "1023_doc": {
        "path": ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
        "needles": ["QVC1023_3_matter_descent", "CDA1023_4_verdict", "SNH1023_2_J_X_zero"],
        "role": "matter-descent and coupling-demotion audit",
    },
    "637_obs": {
        "path": RESIDUALS / "P8_Y5_R10_637_OBS_FUNCTOR_DERIVATION.csv",
        "needles": ["OF637_0_observed_geometry", "OF637_1_chain_rule", "OF637_2_counterexample_filter"],
        "role": "observed functor chain rule and hidden-frame counterexample filter",
    },
    "618_source_zero": {
        "path": RESIDUALS / "P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv",
        "needles": ["SZ618_0_qbar_XT_chain_rule", "SZ618_5_full_source_zero_certificate"],
        "role": "qbar_XT and source-zero certificate status",
    },
    "1024_doc": {
        "path": ROOT / "1024-Y5-R10-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md",
        "needles": ["SIA1024_3_J_X_zero", "ALPHA1024_1_source_current", "BV1024_2_coupling_status"],
        "role": "scalar source-zero and alpha coefficient template",
    },
    "1025_doc": {
        "path": ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
        "needles": ["PHA1025_5_source_current", "ASR1025_2_source_current", "BV1025_3_coupling_gap"],
        "role": "source-current coefficient row and coupling normalization gap",
    },
    "2664_doc": {
        "path": ROOT / "2664-Y5-R2FR-source-current-zero-or-QbarXH-first-source-row.md",
        "needles": ["SCZ2664_1_variational_definition", "SCZ2664_7_verdict", "QXH2664_5_alpha_feed"],
        "role": "rho_X/J_X variational definition and Qbar alpha feed",
    },
    "2665_doc": {
        "path": ROOT / "2665-Y5-R2FR-Hamiltonian-source-domain-and-PiM-QbarXH-lock.md",
        "needles": ["HLOCK2665_7_verdict", "PIM2665_5_QbarXH_locked", "DEC2665_0_lock_status"],
        "role": "Qbar_XH lock blocker for alpha normalization",
    },
    "2618_doc": {
        "path": ROOT / "2618-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
        "needles": ["ANF2618_6_current_verdict", "SMG2618_0_euler_equation_gate", "CM2618_0_unlisted_nonminimal_action"],
        "role": "parent action normal form and shadow/source countermodel",
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in list(OUTPUTS.values()) + list(BRANCH_COPIES.values()) + [DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join("---" for _ in fieldnames) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fieldnames]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def has_missing(row: dict[str, Any]) -> bool:
    joined = " ".join(str(value) for value in row.values()).upper()
    return any(token in joined for token in MISSING_TOKENS)


def source_register_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": f"SRC2673_{source_id}",
                "role": spec["role"],
                "path": str(path),
                "exists": path.exists(),
                "needles_required": len(spec["needles"]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def source_zero_audit_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "clause_id": "JX2673_0_contract",
            "clause": "J_X=0/qbar_XT=0 coupling theorem",
            "required_statement": "all matter, clock, EM, material-marker and hidden-frame channels descend through observed quotient data or have zero X derivative",
            "current_evidence": "2672 selected this as the decisive source-RHS target",
            "current_status": "TARGET_EXACT",
            "missing_for_claim": "none; this is the target",
            "if_missing": "audit channels and stage coefficient rows",
            "theorem_zero_credit": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "JX2673_1_variational_definition",
            "clause": "J_X/rho_X is action-owned",
            "required_statement": "J_X := delta_X S_parent plus all hidden/source/domain terms in the same parent normal form",
            "current_evidence": "2664 gives a conditional definition schema; 2618 says parent action normal form is signature-ready, not complete",
            "current_status": "CONDITIONAL_DEFINITION_SCHEMA",
            "missing_for_claim": "complete parent action inventory and source-term classification",
            "if_missing": "J_X must remain a missing source current",
            "theorem_zero_credit": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "JX2673_2_metric_coframe_chain_rule",
            "clause": "metric/coframe matter pullback",
            "required_statement": "DObs(Dq[v_X])=0 kills the metric/coframe matter variation",
            "current_evidence": "637/1023 mark the chain rule as a conditional math pass",
            "current_status": "CONDITIONAL_MATH_PASS_ONLY",
            "missing_for_claim": "q/v_X certificate and parent observed functor selection",
            "if_missing": "finite qbar_XT row remains live",
            "theorem_zero_credit": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "JX2673_3_constants_markers",
            "clause": "theta_A constants/material labels",
            "required_statement": "Lie_vX(theta_A)=0 for constants, masses, material labels, atomic/clock parameters and calibration markers",
            "current_evidence": "1023 says constants/material labels are not parent-owned",
            "current_status": "MISSING_NO_MARKER_THEOREM",
            "missing_for_claim": "EM, clocks, masses and material labels must be shown vertical-silent",
            "if_missing": "clock/WEP/material qbar_XT coefficient rows remain live",
            "theorem_zero_credit": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "JX2673_4_hidden_frame",
            "clause": "hidden conformal/disformal frame",
            "required_statement": "any X-dependent matter frame either factors through q or is finite-coupled explicitly",
            "current_evidence": "637 hidden-frame counterexample filter is classification, not zero proof",
            "current_status": "COUNTEREXAMPLE_FILTER_ONLY",
            "missing_for_claim": "F_X prime/disformal coefficient must be zeroed or bounded",
            "if_missing": "hidden-frame qbar_XT row remains live",
            "theorem_zero_credit": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "JX2673_5_domain_projector_source",
            "clause": "domain/projector/source selectors",
            "required_statement": "domain, boundary and projector labels do not inject X-dependence into matter/source readout",
            "current_evidence": "1023 and 1019 keep projector/boundary coupling open",
            "current_status": "MISSING_DOMAIN_PROJECTOR_ZERO",
            "missing_for_claim": "source split, Pi_M^H, boundary class and reference silence",
            "if_missing": "Qbar_XH/edge/source rows remain live",
            "theorem_zero_credit": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "JX2673_6_shadow_source",
            "clause": "shadow/non-Hilbert source tails",
            "required_statement": "nonminimal, post-Euler, non-Hilbert or source-shadow terms are forbidden, reclassified or bounded",
            "current_evidence": "2618 and 2664 keep shadow/source terms as countermodel rows",
            "current_status": "MISSING_SHADOW_SOURCE_ZERO_OR_BOUND",
            "missing_for_claim": "normal-form inventory and arena projection",
            "if_missing": "alpha_tail_abs and Q_shadow_XH remain live",
            "theorem_zero_credit": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "JX2673_7_verdict",
            "clause": "J_X/qbar_XT source-zero verdict",
            "required_statement": "JX2673_1 through JX2673_6 all close together",
            "current_evidence": "metric chain rule helps, but marker/hidden/source/projector clauses remain unsigned",
            "current_status": "JX_QBARXT_ZERO_NOT_PARENT_DERIVED",
            "missing_for_claim": "matter-marker descent, hidden-frame exclusion, domain/projector silence, source-shadow zero",
            "if_missing": "stage first qbar_XT/J_X coefficient rows",
            "theorem_zero_credit": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def matter_channel_audit_rows() -> list[dict[str, Any]]:
    generated = stamp()
    channels = [
        ("MAT2673_0_rods_clocks_photons", "rods/clocks/photons", "e_obs,g_obs,omega[e_obs] descended from q", "CONDITIONAL_FUNCTOR_ONLY", "clock normalization and marker silence"),
        ("MAT2673_1_atomic_masses", "atomic masses/material constants", "theta_A vertical silence", "MISSING_NO_MARKER_THEOREM", "mass/material qbar_XT"),
        ("MAT2673_2_EM", "EM/fine-structure sector", "charge/fine-structure readout descends or has zero X derivative", "MISSING_EM_DESCENT_CERTIFICATE", "EM qbar_XT or alpha_EM coefficient"),
        ("MAT2673_3_hidden_frame", "hidden conformal/disformal frame", "F_X'=0 or finite coefficient row", "MISSING_HIDDEN_FRAME_ZERO_OR_BOUND", "F_X/disformal coefficient"),
        ("MAT2673_4_domain_projector", "domain/projector/source labels", "selectors are fixed representation data or source-bounded", "MISSING_PROJECTOR_SOURCE_ZERO", "domain/projector coupling"),
        ("MAT2673_5_verdict", "all matter channels", "all channels theorem-zero or coefficient-staged", "MATTER_CHANNEL_ZERO_NOT_CLAIM_READY", "qbar_XT/J_X coefficient rows"),
    ]
    rows: list[dict[str, Any]] = []
    for channel_id, channel, zero_condition, status, retained_row in channels:
        rows.append(
            {
                "channel_id": channel_id,
                "channel": channel,
                "zero_condition": zero_condition,
                "current_status": status,
                "retained_if_missing": retained_row,
                "score_ready": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def coefficient_template_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "row_id": "QXT2673_0_qbarXT",
            "quantity": "qbar_XT",
            "definition": "dimensionless test-body or matter-sector X coupling normalized in the same field convention as K_X and Qbar_XH",
            "required_columns": "system_id;matter_sector;test_body;lambda_X;qbar_XT;qbar_XT_bound;normalization;units;source_path;equation_ref;valid_for_claim",
            "current_status": "MISSING_TEST_COUPLING_COEFFICIENT",
            "runner_status": "blocked_missing_qbarXT_source",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "QXT2673_1_JX",
            "quantity": "J_X or J_X_bound",
            "definition": "source current in O_X X=J_X including matter, hidden frame, domain and shadow source terms",
            "required_columns": "system_id;source_body;source_channel;J_X;J_X_bound;units;source_path;equation_ref;valid_for_claim",
            "current_status": "MISSING_SOURCE_CURRENT_ZERO_OR_BOUND",
            "runner_status": "blocked_missing_JX_source",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "QXT2673_2_hidden_frame",
            "quantity": "F_X_prime or disformal coefficient",
            "definition": "hidden conformal/disformal X derivative that would make matter see X outside q",
            "required_columns": "system_id;frame_channel;F_X_prime;disformal_coeff;bound;units;source_path;equation_ref;valid_for_claim",
            "current_status": "MISSING_HIDDEN_FRAME_COEFFICIENT",
            "runner_status": "blocked_missing_hidden_frame_bound",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "QXT2673_3_alpha_feed",
            "quantity": "alpha_bulk(lambda_X)",
            "definition": "alpha_bulk(lambda_X)=K_X*Qbar_XH(lambda_X)*qbar_XT*tau_R10 + alpha_tail_abs",
            "required_columns": "system_id;lambda_X;K_X;Qbar_XH;qbar_XT;tau_R10;alpha_tail_abs;alpha_bulk;bound;source_path;valid_for_claim",
            "current_status": "BLOCKED_BY_QBAR_KX_QBARXT_AND_BOUND",
            "runner_status": "blocked_missing_alpha_feed_inputs",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "QXT2673_4_no_cancellation",
            "quantity": "absolute coupling envelope",
            "definition": "abs_alpha_total >= abs(alpha_bulk)+abs(alpha_edge)+abs(alpha_hidden)+abs(alpha_shadow)",
            "required_columns": "system_id;component_abs_values;component_sum_abs;bound_curve;source_path;valid_for_claim",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "runner_status": "blocked_missing_no_cancellation_components",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def alpha_impact_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "impact_id": "AIM2673_0_nohair",
            "condition": "J_X=0 and boundary_flux_X=0",
            "effect": "scalar no-hair RHS vanishes if operator inputs also close",
            "current_status": "NOT_CLOSED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "impact_id": "AIM2673_1_finite_alpha",
            "condition": "qbar_XT or J_X nonzero",
            "effect": "finite local alpha/source row must be compared against R10/PPN/clock/orbital bounds",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "impact_id": "AIM2673_2_verdict",
            "condition": "current corpus",
            "effect": "source-zero cannot be claimed; first coefficient template is staged nonclaim",
            "current_status": "COUPLING_ROW_REQUIRED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def runner_results_rows(
    source_zero: list[dict[str, Any]],
    matter_channels: list[dict[str, Any]],
    coefficient_template: list[dict[str, Any]],
    alpha_impact: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for row in source_zero:
        status = "REJECTED_SOURCE_ZERO_NOT_PARENT_DERIVED"
        if row["clause_id"] == "JX2673_0_contract":
            status = "PASS_TARGET_ONLY_NO_ZERO_CREDIT"
        rows.append(
            {
                "run_id": f"RUN2673_{row['clause_id']}",
                "input_id": row["clause_id"],
                "input_type": "source_zero_audit",
                "has_missing_marker": has_missing(row),
                "runner_status": status,
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    for table_name, table in (
        ("matter_channel_audit", matter_channels),
        ("coefficient_template", coefficient_template),
        ("alpha_impact", alpha_impact),
    ):
        key = "channel_id" if table_name == "matter_channel_audit" else "row_id" if table_name == "coefficient_template" else "impact_id"
        for row in table:
            rows.append(
                {
                    "run_id": f"RUN2673_{row[key]}",
                    "input_id": row[key],
                    "input_type": table_name,
                    "has_missing_marker": has_missing(row),
                    "runner_status": "NONCLAIM_LEDGER_RETAINED",
                    "claim_allowed": False,
                    "valid_for_claim": False,
                    "timestamp_utc": generated,
                }
            )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "gate_id": "CG2673_0_JX_zero",
            "claim": "J_X=0 source-free scalar RHS",
            "current_status": "FAIL_SOURCE_ZERO_NOT_PARENT_DERIVED",
            "blocking_rows": "JX2673_3_constants_markers;JX2673_4_hidden_frame;JX2673_6_shadow_source",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2673_1_qbarXT_zero",
            "claim": "qbar_XT=0 matter/test coupling silence",
            "current_status": "FAIL_MATTER_MARKER_DESCENT_UNSIGNED",
            "blocking_rows": "JX2673_3_constants_markers;MAT2673_2_EM;MAT2673_3_hidden_frame",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2673_2_first_coefficient",
            "claim": "first qbar_XT/J_X coefficient row can be scored",
            "current_status": "FAIL_COEFFICIENT_TEMPLATE_NONCLAIM",
            "blocking_rows": "QXT2673_0_qbarXT;QXT2673_1_JX;QXT2673_3_alpha_feed",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2673_3_local_GR",
            "claim": "local GR follows from coupling silence",
            "current_status": "FAIL_COUPLING_ZERO_UNSIGNED",
            "blocking_rows": "JX2673_7_verdict",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2673_4_verdict",
            "claim": "any J_X/qbar_XT source-zero or coefficient pass",
            "current_status": "CLAIM_BLOCKED",
            "blocking_rows": "JX2673_7_verdict;QXT2673_4_no_cancellation",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def decision_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "decision_id": "DEC2673_0_result",
            "question": "Did J_X=0/qbar_XT=0 close?",
            "answer": "No. The metric/coframe chain rule is useful but marker, hidden-frame, EM/clock/material, domain/projector and shadow-source channels are not parent-signed.",
            "consequence": "source-zero is not claim-ready",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "decision_id": "DEC2673_1_first_row",
            "question": "What did 2673 add?",
            "answer": "A first qbar_XT/J_X coefficient template with hidden-frame and no-cancellation rows, all nonclaim.",
            "consequence": "finite coupling can be tested later without inventing values",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "decision_id": "DEC2673_2_best_next",
            "question": "What is the next best attack?",
            "answer": "Split matter channels one by one: clocks/masses/EM/material markers first, hidden conformal/disformal frame second, coefficient fill third.",
            "consequence": "2674 should attack matter-marker descent or produce channel-specific qbar_XT rows",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def next_target_rows() -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {
            "target_id": "NEXT2673_0_selected",
            "status": "selected",
            "next_doc": "2674-Y5-R2FR-matter-marker-channel-descent-or-qbarXT-bound-row.md",
            "next_script": "scripts/Y5_R2FR_matter_marker_channel_descent_or_qbarXT_bound_row_2674.py",
            "purpose": "try to zero clocks, masses, EM and material-marker X-dependence channel-by-channel, or stage channel-specific qbar_XT bounds",
            "acceptance_gate": "each matter channel is either parent-descended with Lie_vX theta_A=0 or has a sourced coefficient/bound row",
            "forbidden": "universal WEP wording as proof, hiding conformal/disformal channels, invented coefficients, alpha pass claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": generated,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "status_id": "PS2673_0_coupling",
            "area": "coupling/source RHS",
            "state": "not_zeroed_but_schema_locked",
            "why": "source-zero theorem fails, but coefficient rows now name qbar_XT, J_X, hidden frame and alpha feed explicitly",
            "next_needed": "channel-specific matter-marker descent",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "status_id": "PS2673_1_local_GR",
            "area": "local GR reduction",
            "state": "blocked_by_coupling_channels",
            "why": "local scalar no-hair needs zero RHS, and qbar_XT/J_X are not zeroed",
            "next_needed": "zero or bound matter channels",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "status_id": "PS2673_2_empirical",
            "area": "test readiness",
            "state": "schema_ready_not_score_ready",
            "why": "R10/PPN/clock/orbital alpha feed still lacks numeric/source-backed coefficients",
            "next_needed": "source-backed qbar_XT/J_X/Qbar/K_X rows and bound curves",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def branch_copy_rows() -> list[dict[str, Any]]:
    generated = stamp()
    copy_specs = {
        "queue": (OUTPUTS["source_zero_audit"], BRANCH_COPIES["queue"], "JX/qbarXT source-zero queue copy"),
        "local_bounds": (OUTPUTS["coefficient_template"], BRANCH_COPIES["local_bounds"], "local qbarXT coefficient nonclaim copy"),
        "source_weight": (OUTPUTS["coefficient_template"], BRANCH_COPIES["source_weight"], "qbarXT first coefficient template copy"),
        "microscope": (OUTPUTS["matter_channel_audit"], BRANCH_COPIES["microscope"], "matter channel audit copy"),
        "quarantine": (OUTPUTS["runner_results"], BRANCH_COPIES["quarantine"], "coupling runner refusal results"),
    }
    rows: list[dict[str, Any]] = []
    for copy_id, (source, destination, role) in copy_specs.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, destination)
        parseable = False
        if destination.exists():
            try:
                read_csv(destination)
                parseable = True
            except Exception:
                parseable = False
        rows.append(
            {
                "copy_id": f"COPY2673_{copy_id}",
                "role": role,
                "source": str(source),
                "destination": str(destination),
                "exists": destination.exists(),
                "parseable_csv": parseable,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def generated_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())


def all_csv_parse(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        try:
            read_csv(path)
        except Exception:
            return False
    return True


def formalization_hit_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = [
        "*2673-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2673*",
        "*Y5_R2FR_JX_source_zero_or_qbarXT_first_coefficient_row_2673*",
        "*JR2673*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    zero_ok = any(
        row["clause_id"] == "JX2673_7_verdict" and row["current_status"] == "JX_QBARXT_ZERO_NOT_PARENT_DERIVED"
        for row in rows["source_zero_audit"]
    ) and all(not row["theorem_zero_credit"] and not row["valid_for_claim"] for row in rows["source_zero_audit"])
    channel_ok = any(row["channel_id"] == "MAT2673_5_verdict" for row in rows["matter_channel_audit"]) and all(
        not row["score_ready"] and not row["valid_for_claim"] for row in rows["matter_channel_audit"]
    )
    coeff_ok = any(row["row_id"] == "QXT2673_0_qbarXT" for row in rows["coefficient_template"]) and any(
        row["row_id"] == "QXT2673_3_alpha_feed" for row in rows["coefficient_template"]
    ) and all(not row["valid_for_claim"] for row in rows["coefficient_template"])
    impact_ok = any(row["impact_id"] == "AIM2673_2_verdict" and row["current_status"] == "COUPLING_ROW_REQUIRED" for row in rows["alpha_impact"])
    runner_ok = len(rows["runner_results"]) == len(rows["source_zero_audit"]) + len(rows["matter_channel_audit"]) + len(rows["coefficient_template"]) + len(rows["alpha_impact"]) and all(
        row["runner_status"] in {"REJECTED_SOURCE_ZERO_NOT_PARENT_DERIVED", "PASS_TARGET_ONLY_NO_ZERO_CREDIT", "NONCLAIM_LEDGER_RETAINED"}
        for row in rows["runner_results"]
    )
    claim_ok = any(
        row["gate_id"] == "CG2673_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]
    ) and all(not row["gate_pass"] and row["blocks_claim"] for row in rows["claim_gates"])
    decision_ok = any(row["decision_id"] == "DEC2673_2_best_next" and "matter" in row["answer"].lower() for row in rows["decision"])
    next_ok = any("2674-Y5-R2FR-matter-marker-channel" in row["next_doc"] for row in rows["next_target"])
    copies_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2673_00_sources", source_ok, "all coupling source paths exist and required needles are present"),
        ("VAL2673_01_source_zero_audit", zero_ok, "J_X/qbar_XT source-zero audit rejects theorem-zero credit"),
        ("VAL2673_02_matter_channels", channel_ok, "matter channel audit is nonclaim and complete"),
        ("VAL2673_03_coeff_template", coeff_ok, "first qbar_XT/J_X coefficient rows are staged nonclaim"),
        ("VAL2673_04_alpha_impact", impact_ok, "alpha impact ledger requires coupling rows"),
        ("VAL2673_05_runner_refuses", runner_ok, "runner refuses source-zero and retains nonclaim ledgers"),
        ("VAL2673_06_claim_gates_blocked", claim_ok, "source-zero/coefficient/local-GR claims remain blocked"),
        ("VAL2673_07_decision", decision_ok, "matter-channel descent selected as next route"),
        ("VAL2673_08_next_target", next_ok, "2674 matter-marker channel target selected"),
        ("VAL2673_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2673_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2673_11_formalization_untouched", formal_ok, "no 2673 outputs are written under formalization-workbench"),
        ("VAL2673_12_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
    ]
    generated = stamp()
    out = [
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in checks
    ]
    out.append(
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": "VAL2673_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2673 rejects J_X/qbar_XT source-zero as unsigned, stages first coupling rows, and selects matter-marker channel descent next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = read_csv(OUTPUTS["validation"])
    content = f"""# 2673 - JX Source Zero Or qbarXT First Coefficient Row

## Purpose

This checkpoint attacks the coupling hinge exposed by `2672`. The clean local no-hair route needs `J_X=0`; the finite residual route needs `qbar_XT/J_X` rows with units, source paths and no-cancellation guards.

## Result

- `J_X=0/qbar_XT=0` is not parent-derived for current MTS.
- The metric/coframe chain rule is useful but only conditional.
- Constants/material markers, clocks, EM, hidden conformal/disformal frames, domain/projector selectors and shadow-source terms are still live channels.
- First `qbar_XT/J_X` coefficient rows are staged as nonclaim templates.
- The next target is channel-by-channel matter-marker descent, or channel-specific coefficient bounds.

## Source Register

{markdown_table(rows["source_register"])}

## Source-Zero Audit

{markdown_table(rows["source_zero_audit"])}

## Matter Channel Audit

{markdown_table(rows["matter_channel_audit"])}

## First Coefficient Template

{markdown_table(rows["coefficient_template"])}

## Alpha Impact Ledger

{markdown_table(rows["alpha_impact"])}

## Runner Results

{markdown_table(rows["runner_results"])}

## Claim Gates

{markdown_table(rows["claim_gates"])}

## Decision Ledger

{markdown_table(rows["decision"])}

## Next Target

{markdown_table(rows["next_target"])}

## Project Status Snapshot

{markdown_table(rows["project_status"])}

## Branch Copies

{markdown_table(rows["branch_copies"])}

## Validation

{markdown_table(validation)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "source_zero_audit": source_zero_audit_rows(),
        "matter_channel_audit": matter_channel_audit_rows(),
        "coefficient_template": coefficient_template_rows(),
        "alpha_impact": alpha_impact_rows(),
    }
    rows["runner_results"] = runner_results_rows(
        rows["source_zero_audit"], rows["matter_channel_audit"], rows["coefficient_template"], rows["alpha_impact"]
    )
    rows["claim_gates"] = claim_gate_rows()
    rows["decision"] = decision_rows()
    rows["next_target"] = next_target_rows()
    rows["project_status"] = project_status_rows()
    for name, table in rows.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], table)
    rows["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows["branch_copies"])
    remove_pycache()
    rows["validation"] = validation_rows(rows, generated_paths())
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)
    remove_pycache()


if __name__ == "__main__":
    main()
