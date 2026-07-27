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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2672"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2672-Y5-R2FR-positive-scalar-nohair-operator-source-boundary-lock-or-alpha-row.md"

CHECKPOINT = "2672"
BRANCH_ID = "Y5_R2FR_POSITIVE_SCALAR_NOHAIR_OR_ALPHA_ROW_2672"
PREFIX = "P8_Y5_R2FR_SCALAR_NOHAIR_2672"
MISSING_TOKENS = (
    "MISSING",
    "UNSIGNED",
    "NOT_PARENT",
    "NOT_DERIVED",
    "BLOCKED",
    "VALUES_MISSING",
    "TEMPLATE_ONLY",
    "CONDITIONAL",
    "NOT_COMPUTED",
)

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "nohair_audit": RESIDUALS / f"{PREFIX}_NOHAIR_AUDIT.csv",
    "theorem_ledger": RESIDUALS / f"{PREFIX}_THEOREM_LEDGER.csv",
    "alpha_template": RESIDUALS / f"{PREFIX}_ALPHA_SOURCE_TEMPLATE_NONCLAIM.csv",
    "coupling_gap": RESIDUALS / f"{PREFIX}_COUPLING_GAP_LEDGER.csv",
    "runner_results": RESIDUALS / f"{PREFIX}_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2672_SCALAR_NOHAIR_QUEUE_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "Positive_scalar_nohair_2672_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "ALPHA_SOURCE_TEMPLATE_2672_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2672_SCALAR_NOHAIR.csv",
    "quarantine": QUARANTINE / "P8_Y5_2672_SCALAR_RUNNER_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2671_doc": {
        "path": ROOT / "2671-Y5-R2FR-vertical-first-class-generator-or-scalar-nohair-branch-selection.md",
        "needles": ["NEXT2671_0_selected", "SNH2671_3_energy_identity", "DEM2671_0_vertical"],
        "role": "handoff from vertical demotion into scalar no-hair route",
    },
    "1024_doc": {
        "path": ROOT / "1024-Y5-R10-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md",
        "needles": ["SIA1024_5_energy_identity", "ALPHA1024_3_bulk_R10_projection", "BV1024_2_coupling_status"],
        "role": "scalar no-hair input pack and alpha runner schema",
    },
    "1025_doc": {
        "path": ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
        "needles": ["SV1025_2_Hessian_signs", "SV1025_5_sourcefree_nohair", "BV1025_3_coupling_gap"],
        "role": "Hessian sign/range attempt and coupling-gap localization",
    },
    "1022_doc": {
        "path": ROOT / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
        "needles": ["SNH1022_0_operator", "SNH1022_3_source_zero", "SNH1022_5_energy_identity"],
        "role": "earlier scalar no-hair theorem clauses",
    },
    "1019_doc": {
        "path": ROOT / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
        "needles": ["BE1019_1_BX_exact", "PO1019_5_verdict", "V1019_9_claim_gates_blocked"],
        "role": "boundary exactness/projector blockers for boundary_flux_X",
    },
    "2664_doc": {
        "path": ROOT / "2664-Y5-R2FR-source-current-zero-or-QbarXH-first-source-row.md",
        "needles": ["SCZ2664_7_verdict", "QXH2664_5_alpha_feed", "QG2664_0_parent_rhoX"],
        "role": "source-current zero failure and first Qbar_XH nonclaim row",
    },
    "2665_doc": {
        "path": ROOT / "2665-Y5-R2FR-Hamiltonian-source-domain-and-PiM-QbarXH-lock.md",
        "needles": ["HLOCK2665_7_verdict", "PIM2665_5_QbarXH_locked", "DEC2665_0_lock_status"],
        "role": "Hamiltonian source-domain/PiM/Qbar lock blocker",
    },
    "618_source_zero": {
        "path": RESIDUALS / "P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv",
        "needles": ["SZ618_1_Qbar_XH_boundary", "SZ618_2_KX_no_green_function", "SZ618_5_full_source_zero_certificate"],
        "role": "source-zero certificate failure",
    },
    "669_doc": {
        "path": ROOT / "669-Y5-R10-minimal-LX-sector-operator-owner-or-retained-residual-vector.md",
        "needles": ["LX669_2_positive_sourcefree_massive", "V669_5_residual_vector_missing_markers"],
        "role": "minimal scalar source-free branch and retained residual vector",
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
                "source_id": f"SRC2672_{source_id}",
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


def nohair_audit_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "clause_id": "SNH2672_0_contract",
            "clause": "positive scalar no-hair theorem",
            "required_statement": "positive local operator plus zero source and zero boundary flux force X=0 in the local exterior",
            "current_evidence": "1022/1024/1025 write the conditional identity",
            "current_status": "TARGET_EXACT",
            "missing_for_claim": "none; this is the target",
            "if_missing": "audit inputs",
            "theorem_zero_credit": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "SNH2672_1_local_block",
            "clause": "parent local X block",
            "required_statement": "S_X=int_A sqrt(h)[1/2 Z_X |grad X|^2 + 1/2 M_X^2 X^2 - J_X X] plus owned boundary terms",
            "current_evidence": "1025 records this as the minimal conditional scalar block",
            "current_status": "CONDITIONAL_ANSATZ_ONLY",
            "missing_for_claim": "same parent action must produce X, h_ij, Z_X, M_X^2, J_X and boundary terms",
            "if_missing": "scalar branch is not theorem-owned",
            "theorem_zero_credit": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "SNH2672_2_ZX_positive",
            "clause": "Z_X>0",
            "required_statement": "second variation fixes a positive kinetic residue with normalization and units",
            "current_evidence": "1025 gives exact positivity condition but values are missing",
            "current_status": "EXACT_CONDITION_DERIVED_VALUES_MISSING",
            "missing_for_claim": "parent Hessian sign, mixed-sector control, field normalization and units",
            "if_missing": "ghost/anti-elliptic/indefinite residual remains possible",
            "theorem_zero_credit": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "SNH2672_3_MX2_positive_lambda",
            "clause": "M_X^2>0 and lambda_X owned",
            "required_statement": "mass gap is positive and lambda_X=sqrt(Z_X/M_X^2) has source-backed length units",
            "current_evidence": "1024/1025 mark M_X^2/lambda inputs missing",
            "current_status": "MISSING_PARENT_MASS_RANGE_INPUTS",
            "missing_for_claim": "parent Hessian curvature, range derivation and unit convention",
            "if_missing": "zero-mode, tachyonic or arbitrary fitted range branch remains possible",
            "theorem_zero_credit": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "SNH2672_4_self_adjoint_domain",
            "clause": "self-adjoint compact local exterior domain",
            "required_statement": "O_X=-nabla_i(Z_X nabla^i)+M_X^2 is self-adjoint on the local exterior with legal boundary conditions",
            "current_evidence": "1024 marks the operator/domain template only",
            "current_status": "MISSING_SELF_ADJOINT_DOMAIN",
            "missing_for_claim": "domain, falloff, boundary class and mixed-sector boundary Hessian",
            "if_missing": "integration-by-parts energy identity is not a theorem",
            "theorem_zero_credit": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "SNH2672_5_JX_zero",
            "clause": "J_X=0 channel-by-channel",
            "required_statement": "ordinary matter, hidden conformal/disformal channels, clocks, EM, material markers and domain terms are X-source silent",
            "current_evidence": "1024 and 2664 show source zero is not parent-signed",
            "current_status": "MISSING_SOURCE_ZERO_PROOF",
            "missing_for_claim": "matter quotient/no-marker theorem or explicit source-current zero/bound",
            "if_missing": "qbar_XT, rho_X and Qbar_XH remain live coupling rows",
            "theorem_zero_credit": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "SNH2672_6_boundary_flux_zero",
            "clause": "boundary_flux_X=0",
            "required_statement": "int_boundary X Z_X n.grad X plus edge/projector/reference terms vanishes or is source-bounded",
            "current_evidence": "1019 and 581 keep boundary exactness/projector silence unsigned",
            "current_status": "MISSING_BOUNDARY_LOCK",
            "missing_for_claim": "B_X exactness, boundary class, projector orthogonality and reference silence",
            "if_missing": "edge, FB5540 and Qbar_edge_XH rows remain live",
            "theorem_zero_credit": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "SNH2672_7_energy_identity",
            "clause": "positive energy identity",
            "required_statement": "int_A[Z_X|grad X|^2+M_X^2 X^2]=int_A X J_X + boundary_flux_X",
            "current_evidence": "1022/1024/1025 agree this identity is conditionally valid",
            "current_status": "CONDITIONAL_MATH_VALID_INPUTS_MISSING",
            "missing_for_claim": "SNH2672_1 through SNH2672_6 all close together",
            "if_missing": "no X=0 theorem and no local-GR/R10 claim",
            "theorem_zero_credit": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "SNH2672_8_verdict",
            "clause": "scalar no-hair local silence",
            "required_statement": "all scalar no-hair clauses close and the RHS of the identity is zero",
            "current_evidence": "conditions are sharp, but multiple parent/source/boundary inputs are missing",
            "current_status": "SCALAR_NOHAIR_NOT_PARENT_DERIVED",
            "missing_for_claim": "Z_X, M_X^2, domain, J_X=0, boundary_flux_X=0, units",
            "if_missing": "stage alpha/source rows and attack J_X/qbar_XT coupling next",
            "theorem_zero_credit": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def theorem_ledger_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "theorem_id": "THM2672_0_conditional_nohair",
            "statement": "If Z_X>0, M_X^2>0, O_X is self-adjoint, J_X=0 and boundary_flux_X=0, then X=0 on the local exterior.",
            "proof_shape": "the integral of nonnegative terms equals zero, forcing grad X=0 and M_X^2 X^2=0",
            "status": "CONDITIONAL_THEOREM_FORM_VALID",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "theorem_id": "THM2672_1_current",
            "statement": "Current MTS does not supply the parent-owned operator/source/boundary inputs.",
            "proof_shape": "identity is useful but cannot be used as local-GR or R10 evidence",
            "status": "PREMISES_UNFILLED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "theorem_id": "THM2672_2_coupling",
            "statement": "The live obstruction is concrete: the source/coupling RHS must be zero or bounded.",
            "proof_shape": "J_X, qbar_XT, Qbar_XH, K_X and boundary terms feed the same residual family",
            "status": "COUPLING_GAP_LOCALIZED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def alpha_template_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "row_id": "ALP2672_0_operator_range",
            "quantity": "Z_X;M_X2;lambda_X",
            "formula": "lambda_X=sqrt(Z_X/M_X2)",
            "required_columns": "system_id;field_id;Z_X;M_X2;lambda_X;Z_units;M_units;lambda_units;source_path;valid_for_claim",
            "current_status": "MISSING_PARENT_OPERATOR_INPUTS",
            "runner_status": "blocked_missing_operator_inputs",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "ALP2672_1_source_current",
            "quantity": "J_X or J_X_bound",
            "formula": "O_X X = J_X",
            "required_columns": "system_id;J_X;J_X_bound;source_channel;units;source_path;valid_for_claim",
            "current_status": "MISSING_SOURCE_ZERO_PROOF",
            "runner_status": "blocked_missing_source_zero_or_bound",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "ALP2672_2_boundary_flux",
            "quantity": "boundary_flux_X or boundary_flux_bound",
            "formula": "boundary_flux_X=int_boundary X Z_X n.grad X plus edge/projector/reference terms",
            "required_columns": "system_id;boundary_flux_X;boundary_flux_bound;boundary_rule;units;source_path;valid_for_claim",
            "current_status": "MISSING_BOUNDARY_LOCK",
            "runner_status": "blocked_missing_boundary_flux_zero_or_bound",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "ALP2672_3_bulk_projection",
            "quantity": "K_X;Qbar_XH;qbar_XT",
            "formula": "alpha_bulk(lambda_X)=K_X*Qbar_XH(lambda_X)*qbar_XT",
            "required_columns": "system_id;lambda_X;K_X;Qbar_XH;qbar_XT;alpha_bulk;normalization;units;source_path;valid_for_claim",
            "current_status": "MISSING_ARENA_PROJECTION",
            "runner_status": "blocked_missing_alpha_projection_inputs",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "ALP2672_4_edge_projection",
            "quantity": "lambda_edge;K_edge;Qbar_edge_XH;qbar_XT",
            "formula": "alpha_edge(lambda_edge)=K_edge*Qbar_edge_XH(lambda_edge)*qbar_XT",
            "required_columns": "system_id;lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;alpha_edge;units;source_path;valid_for_claim",
            "current_status": "MISSING_EDGE_PROJECTION",
            "runner_status": "blocked_missing_edge_projection_inputs",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "ALP2672_5_no_cancellation_guard",
            "quantity": "abs_alpha_total",
            "formula": "abs_alpha_total=abs(alpha_bulk)+abs(alpha_edge)+abs(epsilon_FB5540)+abs(alpha_R11)",
            "required_columns": "system_id;lambda;abs_alpha_bulk;abs_alpha_edge;abs_FB5540;abs_alpha_R11;component_sum_abs;bound;source_path;valid_for_claim",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "runner_status": "blocked_missing_no_cancellation_components",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def coupling_gap_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "gap_id": "COUP2672_0_JX",
            "gap": "J_X source current",
            "why_it_matters": "it is the RHS of the no-hair identity and the bulk source for finite alpha rows",
            "current_status": "MISSING_SOURCE_ZERO_PROOF_OR_BOUND",
            "next_action": "derive J_X=0 channel-by-channel or write first source-backed J_X/qbar_XT row",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "gap_id": "COUP2672_1_qbarXT",
            "gap": "test-body/source coupling qbar_XT",
            "why_it_matters": "even small universal coupling can source local fifth-force/clock/WEP arenas",
            "current_status": "MISSING_TEST_COUPLING_COEFFICIENT",
            "next_action": "derive matter-marker descent zero or source qbar_XT units and arena projection",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "gap_id": "COUP2672_2_QbarXH",
            "gap": "Hamiltonian source charge Qbar_XH",
            "why_it_matters": "source-side charge remains nonclaim until worldtube/PiM/M_H_ref and edge/shadow split are owned",
            "current_status": "QBAR_XH_NOT_CLAIM_READY",
            "next_action": "continue Qbar lock chain or keep alpha row blocked",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "gap_id": "COUP2672_3_boundary",
            "gap": "boundary_flux_X / edge projection",
            "why_it_matters": "a positive bulk operator does not silence an edge-fed exterior profile",
            "current_status": "MISSING_BOUNDARY_LOCK",
            "next_action": "derive exact/proper boundary class or source edge bound",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "gap_id": "COUP2672_4_verdict",
            "gap": "coupling gap verdict",
            "why_it_matters": "this is the same obstruction from quotient, vertical and scalar routes in coefficient language",
            "current_status": "COUPLING_GAP_IS_NEXT_TARGET",
            "next_action": "attack J_X=0/qbar_XT first because it decides theorem-zero versus finite alpha",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def runner_results_rows(
    nohair_audit: list[dict[str, Any]],
    theorem_ledger: list[dict[str, Any]],
    alpha_template: list[dict[str, Any]],
    coupling_gap: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for row in nohair_audit:
        status = "REJECTED_NOHAIR_INPUTS_MISSING"
        if row["clause_id"] == "SNH2672_0_contract":
            status = "PASS_TARGET_ONLY_NO_ZERO_CREDIT"
        rows.append(
            {
                "run_id": f"RUN2672_{row['clause_id']}",
                "input_id": row["clause_id"],
                "input_type": "nohair_audit",
                "has_missing_marker": has_missing(row),
                "runner_status": status,
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    for table_name, table in (
        ("theorem_ledger", theorem_ledger),
        ("alpha_template", alpha_template),
        ("coupling_gap", coupling_gap),
    ):
        key = "theorem_id" if table_name == "theorem_ledger" else "row_id" if table_name == "alpha_template" else "gap_id"
        for row in table:
            rows.append(
                {
                    "run_id": f"RUN2672_{row[key]}",
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
            "gate_id": "CG2672_0_scalar_nohair",
            "claim": "local X profile vanishes by positive scalar no-hair",
            "current_status": "FAIL_NOHAIR_INPUTS_MISSING",
            "blocking_rows": "SNH2672_2_ZX_positive;SNH2672_3_MX2_positive_lambda;SNH2672_5_JX_zero;SNH2672_6_boundary_flux_zero",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2672_1_R10_alpha",
            "claim": "R10 alpha row passes or is inactive",
            "current_status": "FAIL_ALPHA_INPUTS_NONCLAIM",
            "blocking_rows": "ALP2672_0_operator_range;ALP2672_1_source_current;ALP2672_3_bulk_projection",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2672_2_boundary_edge",
            "claim": "boundary/edge profile is silent",
            "current_status": "FAIL_BOUNDARY_LOCK_MISSING",
            "blocking_rows": "SNH2672_6_boundary_flux_zero;ALP2672_4_edge_projection",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2672_3_local_GR",
            "claim": "local GR follows from scalar no-hair",
            "current_status": "FAIL_SCALAR_NOHAIR_NOT_PARENT_DERIVED",
            "blocking_rows": "SNH2672_8_verdict",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2672_4_verdict",
            "claim": "any scalar no-hair/R10/local-GR pass",
            "current_status": "CLAIM_BLOCKED",
            "blocking_rows": "SNH2672_8_verdict;ALP2672_5_no_cancellation_guard",
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
            "decision_id": "DEC2672_0_result",
            "question": "Did the positive scalar no-hair theorem close?",
            "answer": "No. The energy identity is mathematically useful, but Z_X, M_X^2, domain, J_X=0, boundary_flux_X=0 and units are not all parent-owned.",
            "consequence": "no scalar no-hair/local-GR/R10 claim is promoted",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "decision_id": "DEC2672_1_coupling",
            "question": "What is the sharpest next gap?",
            "answer": "J_X/qbar_XT coupling. If the source is zero, no-hair can still win; if not, the finite alpha path must be sourced.",
            "consequence": "attack source-zero or first qbar_XT coefficient row next",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "decision_id": "DEC2672_2_status",
            "question": "What changed after quotient and vertical routes failed?",
            "answer": "The local problem is no longer vague. The theory now needs either a zero RHS for the scalar identity or a real coefficient ledger for alpha(lambda).",
            "consequence": "testing can proceed only after theorem-zero or source rows are filled",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def next_target_rows() -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {
            "target_id": "NEXT2672_0_selected",
            "status": "selected",
            "next_doc": "2673-Y5-R2FR-JX-source-zero-or-qbarXT-first-coefficient-row.md",
            "next_script": "scripts/Y5_R2FR_JX_source_zero_or_qbarXT_first_coefficient_row_2673.py",
            "purpose": "derive J_X=0/qbar_XT=0 from matter descent, or stage the first source-backed coupling coefficient row",
            "acceptance_gate": "matter, clock, EM, material-marker and hidden conformal/disformal channels are zeroed by parent descent, or qbar_XT/J_X rows are numeric, sourced and nonclaim",
            "forbidden": "source-free by assertion, universal coupling silence by WEP wording, invented coefficients, alpha pass claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": generated,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "status_id": "PS2672_0_local_GR",
            "area": "local GR reduction",
            "state": "not_derived_but_narrowed",
            "why": "quotient, vertical and scalar no-hair theorem routes are now conditional-only for current claims",
            "next_needed": "source-zero/coupling derivation or finite alpha coefficients",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "status_id": "PS2672_1_coupling",
            "area": "coupling",
            "state": "primary_live_gap",
            "why": "J_X/qbar_XT decides whether scalar no-hair has zero RHS",
            "next_needed": "2673 J_X/qbar_XT source-zero or coefficient row",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "status_id": "PS2672_2_empirical",
            "area": "R10/PPN/clock/orbital",
            "state": "blocked_until_coefficients_or_zero_theorem",
            "why": "alpha(lambda) inputs are nonclaim placeholders",
            "next_needed": "source-backed coefficient ledger before comparator use",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def branch_copy_rows() -> list[dict[str, Any]]:
    generated = stamp()
    copy_specs = {
        "queue": (OUTPUTS["nohair_audit"], BRANCH_COPIES["queue"], "scalar no-hair queue copy"),
        "local_bounds": (OUTPUTS["nohair_audit"], BRANCH_COPIES["local_bounds"], "local scalar nonclaim copy"),
        "source_weight": (OUTPUTS["alpha_template"], BRANCH_COPIES["source_weight"], "alpha source template nonclaim copy"),
        "microscope": (OUTPUTS["coupling_gap"], BRANCH_COPIES["microscope"], "coupling gap copy"),
        "quarantine": (OUTPUTS["runner_results"], BRANCH_COPIES["quarantine"], "scalar runner refusal results"),
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
                "copy_id": f"COPY2672_{copy_id}",
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
        "*2672-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2672*",
        "*Y5_R2FR_positive_scalar_nohair_operator_source_boundary_lock_or_alpha_row_2672*",
        "*JR2672*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    nohair_ok = any(
        row["clause_id"] == "SNH2672_8_verdict" and row["current_status"] == "SCALAR_NOHAIR_NOT_PARENT_DERIVED"
        for row in rows["nohair_audit"]
    ) and all(not row["theorem_zero_credit"] and not row["valid_for_claim"] for row in rows["nohair_audit"])
    theorem_ok = any(row["theorem_id"] == "THM2672_0_conditional_nohair" for row in rows["theorem_ledger"]) and all(
        not row["claim_allowed"] and not row["valid_for_claim"] for row in rows["theorem_ledger"]
    )
    alpha_ok = all(not row["valid_for_claim"] for row in rows["alpha_template"]) and any(
        row["row_id"] == "ALP2672_3_bulk_projection" for row in rows["alpha_template"]
    )
    coupling_ok = any(
        row["gap_id"] == "COUP2672_4_verdict" and row["current_status"] == "COUPLING_GAP_IS_NEXT_TARGET"
        for row in rows["coupling_gap"]
    )
    runner_ok = len(rows["runner_results"]) == len(rows["nohair_audit"]) + len(rows["theorem_ledger"]) + len(rows["alpha_template"]) + len(rows["coupling_gap"]) and all(
        row["runner_status"] in {"REJECTED_NOHAIR_INPUTS_MISSING", "PASS_TARGET_ONLY_NO_ZERO_CREDIT", "NONCLAIM_LEDGER_RETAINED"}
        for row in rows["runner_results"]
    )
    claim_ok = any(
        row["gate_id"] == "CG2672_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]
    ) and all(not row["gate_pass"] and row["blocks_claim"] for row in rows["claim_gates"])
    decision_ok = any(row["decision_id"] == "DEC2672_1_coupling" and "J_X/qbar_XT" in row["answer"] for row in rows["decision"])
    next_ok = any("2673-Y5-R2FR-JX-source-zero" in row["next_doc"] for row in rows["next_target"])
    copies_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2672_00_sources", source_ok, "all scalar/coupling source paths exist and required needles are present"),
        ("VAL2672_01_nohair_audit", nohair_ok, "scalar no-hair audit rejects theorem-zero credit"),
        ("VAL2672_02_theorem_ledger", theorem_ok, "conditional no-hair theorem is recorded without claim promotion"),
        ("VAL2672_03_alpha_template", alpha_ok, "alpha/source template rows remain nonclaim"),
        ("VAL2672_04_coupling_gap", coupling_ok, "J_X/qbar_XT coupling gap is selected next"),
        ("VAL2672_05_runner_refuses", runner_ok, "runner refuses missing no-hair inputs and retains nonclaim ledgers"),
        ("VAL2672_06_claim_gates_blocked", claim_ok, "R10/PPN/clock/orbital/local-GR claims remain blocked"),
        ("VAL2672_07_decision", decision_ok, "coupling/source-zero selected as next derivation target"),
        ("VAL2672_08_next_target", next_ok, "2673 J_X/qbar_XT target selected"),
        ("VAL2672_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2672_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2672_11_formalization_untouched", formal_ok, "no 2672 outputs are written under formalization-workbench"),
        ("VAL2672_12_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
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
            "validation_id": "VAL2672_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2672 records the conditional scalar no-hair theorem, blocks current claims, and selects J_X/qbar_XT coupling as the next target",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = read_csv(OUTPUTS["validation"])
    content = f"""# 2672 - Positive Scalar Nohair Operator Source Boundary Lock Or Alpha Row

## Purpose

This checkpoint tests the first non-gauge local-silence route. If `X` is a physical scalar-like local field, the clean theorem is a positive energy identity: positive operator plus zero source plus zero boundary flux forces `X=0` in the local exterior.

## Result

- The scalar no-hair theorem is valid as a conditional mathematical route.
- Current MTS does not parent-own the full input pack: `Z_X>0`, `M_X^2>0`, `lambda_X`, self-adjoint domain, `J_X=0`, `boundary_flux_X=0`, and units.
- No local-GR/R10/PPN/clock/orbital claim is promoted.
- Nonclaim alpha/source rows are staged so a finite residual branch cannot hide behind prose.
- The next sharp target is the coupling: derive `J_X=0/qbar_XT=0`, or write the first source-backed coefficient row.

## Source Register

{markdown_table(rows["source_register"])}

## Nohair Audit

{markdown_table(rows["nohair_audit"])}

## Theorem Ledger

{markdown_table(rows["theorem_ledger"])}

## Alpha Source Template

{markdown_table(rows["alpha_template"])}

## Coupling Gap Ledger

{markdown_table(rows["coupling_gap"])}

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
        "nohair_audit": nohair_audit_rows(),
        "theorem_ledger": theorem_ledger_rows(),
        "alpha_template": alpha_template_rows(),
        "coupling_gap": coupling_gap_rows(),
    }
    rows["runner_results"] = runner_results_rows(
        rows["nohair_audit"], rows["theorem_ledger"], rows["alpha_template"], rows["coupling_gap"]
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
