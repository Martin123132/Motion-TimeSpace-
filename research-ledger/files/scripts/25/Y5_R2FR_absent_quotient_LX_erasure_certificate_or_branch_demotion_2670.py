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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2670"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2670-Y5-R2FR-absent-quotient-LX-erasure-certificate-or-branch-demotion.md"

CHECKPOINT = "2670"
BRANCH_ID = "Y5_R2FR_ABSENT_QUOTIENT_ERASURE_2670"
PREFIX = "P8_Y5_R2FR_QUOTIENT_ERASURE_2670"
MISSING_TOKENS = (
    "MISSING",
    "UNSIGNED",
    "NOT_PARENT",
    "NOT_DERIVED",
    "BLOCKED",
    "UNFILLED",
    "CONDITIONAL_ONLY",
    "VALUES_MISSING",
)

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "erasure_certificate": RESIDUALS / f"{PREFIX}_ERASURE_CERTIFICATE_AUDIT.csv",
    "theorem_ledger": RESIDUALS / f"{PREFIX}_THEOREM_LEDGER.csv",
    "demotion": RESIDUALS / f"{PREFIX}_BRANCH_DEMOTION_LEDGER.csv",
    "vertical_fallback": RESIDUALS / f"{PREFIX}_VERTICAL_FALLBACK_INTERFACE_NONCLAIM.csv",
    "runner_results": RESIDUALS / f"{PREFIX}_ERASURE_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2670_ABSENT_QUOTIENT_ERASURE_QUEUE_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "Absent_quotient_erasure_certificate_2670_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "QUOTIENT_ERASURE_DEMOTION_2670_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2670_QUOTIENT_ERASURE.csv",
    "quarantine": QUARANTINE / "P8_Y5_2670_ERASURE_RUNNER_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2669_doc": {
        "path": ROOT / "2669-Y5-R2FR-parent-LX-normal-form-branch-selection-or-omega-bound.md",
        "needles": ["LXB2669_1_absent_quotient", "SEL2669_1_absent_quotient_certificate", "NEXT2669_0_selected"],
        "role": "handoff selecting absent quotient as the cleanest local-GR route",
    },
    "1023_doc": {
        "path": ROOT / "1023-Y5-R10-q-vX-action-descent-certificate-or-scalar-nohair-demotion.md",
        "needles": ["QVC1023_8_verdict", "CDA1023_4_verdict", "DEC1023_1_demotion"],
        "role": "prior single q/v_X/action certificate failure",
    },
    "1022_doc": {
        "path": ROOT / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
        "needles": ["VQC1022_7_verdict", "BDM1022_0_absent_quotient", "FBR1022_0_quotient_certificate"],
        "role": "quotient/vertical clause menu",
    },
    "637_qmap": {
        "path": RESIDUALS / "P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv",
        "needles": ["QM637_0_topological_projection", "QM637_2_vertical_kernel", "QM637_3_observed_domain_guard"],
        "role": "conditional quotient map and Dq kernel math",
    },
    "637_obs": {
        "path": RESIDUALS / "P8_Y5_R10_637_OBS_FUNCTOR_DERIVATION.csv",
        "needles": ["OF637_0_observed_geometry", "OF637_1_chain_rule"],
        "role": "observed geometry and matter chain-rule descent",
    },
    "590_vertical": {
        "path": RESIDUALS / "P8_Y5_R10_590_DCDAGGER_VERTICAL_MAP.csv",
        "needles": ["DVM590_2_momentum_map_identity", "DVM590_3_precise_map", "DVM590_4_raise_index"],
        "role": "DCdagger-to-vertical generator map",
    },
    "581_chain": {
        "path": RESIDUALS / "P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv",
        "needles": ["QVT581_0_parent_projection", "QVT581_5_boundary_charge", "QVT581_7_alpha_result"],
        "role": "older theorem chain with unfilled premises",
    },
    "670_no_pole": {
        "path": RESIDUALS / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
        "needles": ["NQ670_2_kernel_transfer", "NQ670_7_boundary_and_degree_count", "NQ670_8_no_pole_result"],
        "role": "no-pole quotient proof chain and blockers",
    },
    "1019_doc": {
        "path": ROOT / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
        "needles": ["PO1019_2_symplectic_block", "DC1019_0_orthogonal_split", "V1019_9_claim_gates_blocked"],
        "role": "boundary/projector silence guardrail",
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
    joined = " ".join(str(value) for value in row.values())
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
                "source_id": f"SRC2670_{source_id}",
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


def erasure_certificate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "clause_id": "QER2670_0_contract",
            "clause": "absent-quotient erasure theorem",
            "required_statement": "X is absent from physical tangent space before variation, not set to zero after readout",
            "evidence_now": "2669 selected this as the cleanest branch because it would erase the local pole rather than tune it",
            "current_status": "TARGET_EXACT",
            "blocker": "none; this is the theorem contract",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "QER2670_1_parent_quotient_map",
            "clause": "parent quotient map q",
            "required_statement": "q: Conf_parent -> Q_obs is canonical, parent-owned, domain-scoped and not a post-readout projector",
            "evidence_now": "637 gives conditional topological projection and Dq-kernel math",
            "current_status": "CONDITIONAL_MATH_NOT_PARENT_SIGNED",
            "blocker": "actual local X variations must be identified with parent null/relative-exact directions on the local branch",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "QER2670_2_null_distribution",
            "clause": "integrable invariant null distribution N_X",
            "required_statement": "N_X is invariant under parent symmetries, integrable, local-domain admissible and has v_X in its tangent fibres",
            "evidence_now": "581/670 state the condition and partial setup",
            "current_status": "NOT_PARENT_SIGNED",
            "blocker": "field-space distribution, compact-domain admissibility and symmetry invariance are not proved for current MTS",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "QER2670_3_vertical_local_generator",
            "clause": "field-by-field local v_X",
            "required_statement": "v_X is specified on metric/coframe, canonical variables, memory/projector/domain fields, matter readout and boundary fields",
            "evidence_now": "590 clarifies DCdagger is Omega-flat(v_X), not the generator itself",
            "current_status": "MISSING_FIELD_BY_FIELD_VERTICAL_ACTION",
            "blocker": "parent Omega, DC_X, field-by-field action and reduced Omega inverse are not available",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "QER2670_4_action_descent",
            "clause": "bulk action descends before variation",
            "required_statement": "S_bulk[Phi]=S_red[q(Phi)] plus fixed boundary/topological terms, so i_vX dS_bulk=0 off shell",
            "evidence_now": "581/670 provide conditional theorem steps",
            "current_status": "CONDITIONAL_ONLY",
            "blocker": "explicit parent Lagrangian, boundary/domain terms and invariant variational class are not signed",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "QER2670_5_matter_descent",
            "clause": "ordinary matter quotient functor",
            "required_statement": "S_matter=Sbar_m[Obs(q(Phi)),psi,theta_A] and Lie_vX(theta_A)=0 for constants/material markers",
            "evidence_now": "637 chain rule kills the metric/coframe pullback only conditionally",
            "current_status": "GEOMETRY_CHAIN_RULE_CONDITIONAL_MARKERS_OPEN",
            "blocker": "constant/material marker ownership, EM/clocks/masses and hidden conformal/disformal channels are not excluded",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "QER2670_6_measure_coframe_connection_descent",
            "clause": "measure/coframe/connection descent",
            "required_statement": "volume measure, observed coframe, metric connection and matter connection all factor through q with no representative X coefficient",
            "evidence_now": "observed geometry functor is conditional for e_obs/g_obs/omega[e_obs]",
            "current_status": "UNSIGNED_GEOMETRY_FUNCTOR_EXTENSION",
            "blocker": "connection/coframe descent is not parent-signed for every matter and clock arena",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "QER2670_7_boundary_silence",
            "clause": "local boundary and projector silence",
            "required_statement": "Q_X=0/proper/exact, K_boundary=0 and Pi_M^H[Q_X]=0 on compact local branch",
            "evidence_now": "1019/1023/670 all retain boundary/projector blockers",
            "current_status": "BLOCKED_BOUNDARY_PROJECTOR_SILENCE",
            "blocker": "B_X primitive, weighted-Stokes zero/bound, projector orthogonality and cocycle are unsigned",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "QER2670_8_degree_count",
            "clause": "constraint degree removal",
            "required_statement": "primary+secondary first-class pair removes the X pair and reduced Omega has no proper X stabilizer",
            "evidence_now": "581/670 state the rank condition",
            "current_status": "NOT_CHECKED",
            "blocker": "constraint rank, bracket closure and no-stabilizer theorem are missing",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "QER2670_9_no_post_readout_cheat",
            "clause": "readout order guard",
            "required_statement": "readout and projectors are applied after parent variation and cannot be used as parent equations",
            "evidence_now": "581/670 correctly mark post-readout closure as a no-cheat guard",
            "current_status": "GUARD_ACTIVE",
            "blocker": "guard blocks false positives but does not itself prove erasure",
            "theorem_zero_credit": False,
            "demote_if_missing": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "QER2670_10_verdict",
            "clause": "absent quotient branch verdict",
            "required_statement": "QER2670_1 through QER2670_8 all close together",
            "evidence_now": "kernel math and chain-rule fragments exist, but the parent certificate does not close",
            "current_status": "ABSENT_QUOTIENT_ERASURE_NOT_DERIVED",
            "blocker": "missing vertical action, action descent, matter-marker descent, boundary silence and degree count",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def theorem_ledger_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "theorem_id": "THM2670_0_if_closed",
            "statement": "If q, N_X, v_X, action descent, matter descent, geometry descent, boundary silence and degree count all close, then X has no independent local L_X.",
            "consequence": "K_X=0, qbar_XT=0, Qbar_XH=0, alpha_X(lambda) inactive and no local fifth-force pole from X",
            "proof_status": "CONDITIONAL_THEOREM_FORM_VALID",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "theorem_id": "THM2670_1_current",
            "statement": "Current corpus supplies useful fragments but not the single parent certificate.",
            "consequence": "no theorem-zero credit may be spent in R10, PPN, clocks, EM or orbital branches",
            "proof_status": "PREMISES_UNFILLED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "theorem_id": "THM2670_2_demote_rule",
            "statement": "Failure of one required erasure clause demotes absent quotient to conditional-only.",
            "consequence": "next theorem-zero attempt is vertical first-class generator; if it fails, scalar no-hair/source rows become active",
            "proof_status": "ROUTE_HYGIENE_RULE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def demotion_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "demotion_id": "DEM2670_0_absent_quotient",
            "branch": "absent quotient",
            "demotion_status": "DEMOTED_TO_CONDITIONAL_ONLY",
            "reason": "single q/v/action/matter/geometry/boundary/degree certificate is not parent-signed",
            "retained_obligation": "cannot set K_X, qbar_XT or Qbar_XH to zero from quotient language",
            "next_route": "vertical first-class generator certificate",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "demotion_id": "DEM2670_1_residuals",
            "branch": "finite residual safeguard",
            "demotion_status": "RETAINED_AS_NONCLAIM",
            "reason": "if X is physical or boundary-active, source/coupling rows must be bounded rather than cancelled",
            "retained_obligation": "keep sourced alpha, edge, omega and PPN residual interfaces live",
            "next_route": "vertical or scalar no-hair before finite-source scoring",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def vertical_fallback_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "row_id": "VFB2670_0_vX_generator",
            "target": "field-by-field v_X",
            "required_inputs": "metric/coframe action;canonical action;memory/projector action;matter readout action;boundary action",
            "status": "MISSING_FIELD_BY_FIELD_VERTICAL_ACTION",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "VFB2670_1_momentum_map",
            "target": "delta G_X=Omega(delta Phi,v_X)",
            "required_inputs": "parent Theta;parent Omega;DC_X;Q_X differentiability;domain",
            "status": "MISSING_PARENT_SYMPLECTIC_PACKAGE",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "VFB2670_2_bracket",
            "target": "first-class bracket closure",
            "required_inputs": "constraint algebra;structure functions;boundary cocycle;rank count",
            "status": "MISSING_BRACKET_AND_RANK_COUNT",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "VFB2670_3_boundary",
            "target": "zero/proper boundary charge",
            "required_inputs": "Q_X;B_X primitive;K_boundary;projector orthogonality;compact local boundary class",
            "status": "MISSING_BOUNDARY_ZERO_CERTIFICATE",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "VFB2670_4_verdict",
            "target": "vertical theorem-zero route",
            "required_inputs": "VFB2670_0 through VFB2670_3",
            "status": "STAGED_NEXT_NOT_CLAIM_READY",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def runner_results_rows(
    erasure_certificate: list[dict[str, Any]],
    theorem_ledger: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    vertical_fallback: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for row in erasure_certificate:
        status = "REJECTED_ERASURE_CLAUSE_UNSIGNED"
        if row["clause_id"] == "QER2670_9_no_post_readout_cheat":
            status = "PASS_GUARD_ONLY_NO_ZERO_CREDIT"
        rows.append(
            {
                "run_id": f"RUN2670_{row['clause_id']}",
                "input_id": row["clause_id"],
                "input_type": "erasure_certificate",
                "has_missing_marker": has_missing(row),
                "runner_status": status,
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    for table_name, table in (
        ("theorem_ledger", theorem_ledger),
        ("demotion", demotion),
        ("vertical_fallback", vertical_fallback),
    ):
        key = "theorem_id" if table_name == "theorem_ledger" else "demotion_id" if table_name == "demotion" else "row_id"
        for row in table:
            rows.append(
                {
                    "run_id": f"RUN2670_{row[key]}",
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
            "gate_id": "CG2670_0_absent_quotient_zero",
            "claim": "X is absent before variation and local L_X is erased",
            "current_status": "FAIL_ERASURE_CERTIFICATE_UNSIGNED",
            "blocking_rows": "QER2670_3_vertical_local_generator;QER2670_4_action_descent;QER2670_7_boundary_silence;QER2670_8_degree_count",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2670_1_R10",
            "claim": "R10 X alpha row inactive by quotient theorem",
            "current_status": "FAIL_NO_ZERO_CREDIT",
            "blocking_rows": "QER2670_10_verdict",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2670_2_local_GR",
            "claim": "local-GR branch follows from absent quotient",
            "current_status": "FAIL_QUOTIENT_BRANCH_DEMOTED",
            "blocking_rows": "DEM2670_0_absent_quotient",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2670_3_PPN_clock_orbital",
            "claim": "PPN/clock/orbital residuals are killed by quotient erasure",
            "current_status": "FAIL_MATTER_GEOMETRY_BOUNDARY_DESCENT_UNSIGNED",
            "blocking_rows": "QER2670_5_matter_descent;QER2670_6_measure_coframe_connection_descent;QER2670_7_boundary_silence",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2670_4_verdict",
            "claim": "any absent-quotient local claim",
            "current_status": "CLAIM_BLOCKED",
            "blocking_rows": "QER2670_10_verdict",
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
            "decision_id": "DEC2670_0_result",
            "question": "Did the absent-quotient erasure route close?",
            "answer": "No. The route is mathematically clean if all premises hold, but current MTS does not parent-sign the full certificate.",
            "consequence": "demote absent quotient to conditional-only and do not spend no-pole credit",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "decision_id": "DEC2670_1_best_next",
            "question": "What is the best next derivation attempt?",
            "answer": "Try the vertical first-class generator route directly, because it is the next theorem-zero path and may close part of the same obstruction more explicitly.",
            "consequence": "construct v_X, Omega, G_X, bracket, boundary and degree-count certificate or demote to scalar no-hair",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "decision_id": "DEC2670_2_status",
            "question": "Is this grim?",
            "answer": "Not grim, but unforgiving: quotient language alone is not enough. The useful gain is that the missing pieces are now localised to vertical generator, matter/geometry descent, boundary silence and degree count.",
            "consequence": "we have sharper attack points rather than vague coupling anxiety",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def next_target_rows() -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {
            "target_id": "NEXT2670_0_selected",
            "status": "selected",
            "next_doc": "2671-Y5-R2FR-vertical-first-class-generator-or-scalar-nohair-branch-selection.md",
            "next_script": "scripts/Y5_R2FR_vertical_first_class_generator_or_scalar_nohair_branch_selection_2671.py",
            "purpose": "derive the vertical generator/first-class constraint certificate directly, or demote theorem-zero routes to scalar no-hair",
            "acceptance_gate": "v_X field map, parent Omega, momentum map, bracket closure, boundary zero and degree count close together",
            "forbidden": "using DCdagger as v_X without Omega, ignoring boundary charge, assuming matter descent, local-GR/R10 pass claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": generated,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "status_id": "PS2670_0_quotient",
            "area": "absent quotient branch",
            "state": "demoted_to_conditional_only",
            "why": "single parent erasure certificate remains unsigned",
            "next_needed": "vertical first-class generator certificate",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "status_id": "PS2670_1_GR",
            "area": "local GR reduction",
            "state": "still_alive_not_claimed",
            "why": "theorem-zero route failed as claim, but the vertical generator route may still erase X without fitted coefficients",
            "next_needed": "2671 vertical theorem-zero attempt",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "status_id": "PS2670_2_testing",
            "area": "R10/PPN/clock/orbital",
            "state": "no_claim",
            "why": "no source-zero/no-pole theorem has closed",
            "next_needed": "theorem-zero vertical route or scalar/source residual rows",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def branch_copy_rows() -> list[dict[str, Any]]:
    generated = stamp()
    copy_specs = {
        "queue": (OUTPUTS["erasure_certificate"], BRANCH_COPIES["queue"], "absent quotient erasure queue copy"),
        "local_bounds": (OUTPUTS["erasure_certificate"], BRANCH_COPIES["local_bounds"], "local branch erasure nonclaim copy"),
        "source_weight": (OUTPUTS["demotion"], BRANCH_COPIES["source_weight"], "quotient demotion nonclaim copy"),
        "microscope": (OUTPUTS["vertical_fallback"], BRANCH_COPIES["microscope"], "vertical fallback interface copy"),
        "quarantine": (OUTPUTS["runner_results"], BRANCH_COPIES["quarantine"], "erasure runner refusal results"),
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
                "copy_id": f"COPY2670_{copy_id}",
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
        "*2670-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2670*",
        "*Y5_R2FR_absent_quotient_LX_erasure_certificate_or_branch_demotion_2670*",
        "*JR2670*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    certificate_ok = any(
        row["clause_id"] == "QER2670_10_verdict" and row["current_status"] == "ABSENT_QUOTIENT_ERASURE_NOT_DERIVED"
        for row in rows["erasure_certificate"]
    ) and all(not row["theorem_zero_credit"] and not row["valid_for_claim"] for row in rows["erasure_certificate"])
    theorem_ok = any(row["theorem_id"] == "THM2670_0_if_closed" for row in rows["theorem_ledger"]) and all(
        not row["claim_allowed"] and not row["valid_for_claim"] for row in rows["theorem_ledger"]
    )
    demotion_ok = any(
        row["demotion_id"] == "DEM2670_0_absent_quotient" and row["demotion_status"] == "DEMOTED_TO_CONDITIONAL_ONLY"
        for row in rows["demotion"]
    )
    fallback_ok = any(row["row_id"] == "VFB2670_4_verdict" for row in rows["vertical_fallback"]) and all(
        not row["score_ready"] and not row["valid_for_claim"] for row in rows["vertical_fallback"]
    )
    runner_ok = len(rows["runner_results"]) == len(rows["erasure_certificate"]) + len(rows["theorem_ledger"]) + len(rows["demotion"]) + len(rows["vertical_fallback"]) and all(
        row["runner_status"] in {"REJECTED_ERASURE_CLAUSE_UNSIGNED", "PASS_GUARD_ONLY_NO_ZERO_CREDIT", "NONCLAIM_LEDGER_RETAINED"}
        for row in rows["runner_results"]
    )
    claim_ok = any(
        row["gate_id"] == "CG2670_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]
    ) and all(not row["gate_pass"] and row["blocks_claim"] for row in rows["claim_gates"])
    decision_ok = any(row["decision_id"] == "DEC2670_1_best_next" and "vertical" in row["answer"] for row in rows["decision"])
    next_ok = any("2671-Y5-R2FR-vertical-first-class-generator" in row["next_doc"] for row in rows["next_target"])
    copies_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2670_00_sources", source_ok, "all cited quotient/vertical source paths exist and required needles are present"),
        ("VAL2670_01_erasure_certificate", certificate_ok, "absent quotient erasure certificate rejects zero credit"),
        ("VAL2670_02_theorem_ledger", theorem_ok, "conditional theorem is recorded without claim promotion"),
        ("VAL2670_03_demotion", demotion_ok, "absent quotient branch is demoted to conditional-only"),
        ("VAL2670_04_vertical_fallback", fallback_ok, "vertical first-class fallback interface is staged nonclaim"),
        ("VAL2670_05_runner_refuses", runner_ok, "runner rejects unsigned erasure clauses and retains nonclaim ledgers"),
        ("VAL2670_06_claim_gates_blocked", claim_ok, "R10/PPN/clock/orbital/local-GR claims remain blocked"),
        ("VAL2670_07_decision", decision_ok, "vertical generator selected as next derivation target"),
        ("VAL2670_08_next_target", next_ok, "2671 vertical-first-class target selected"),
        ("VAL2670_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2670_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2670_11_formalization_untouched", formal_ok, "no 2670 outputs are written under formalization-workbench"),
        ("VAL2670_12_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
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
            "validation_id": "VAL2670_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2670 demotes absent quotient to conditional-only and selects vertical first-class generator as the next theorem-zero attempt",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = read_csv(OUTPUTS["validation"])
    content = f"""# 2670 - Absent Quotient LX Erasure Certificate Or Branch Demotion

## Purpose

This checkpoint tests the cleanest local-GR route from 2669: whether `X` is absent from the physical tangent before variation. If this were parent-signed, `L_X` would not be an independent local sector and the R10/PPN local pole would be erased rather than fitted.

## Result

- The conditional theorem is mathematically clean: if the full certificate closes, `K_X=0`, `qbar_XT=0`, `Qbar_XH=0`, and the local `X` alpha row is inactive.
- The current corpus does not close the full certificate.
- The absent-quotient branch is demoted to conditional-only for current MTS.
- The main blockers are field-by-field `v_X`, action descent, matter/marker and geometry descent, boundary silence, and degree count.
- The next target is the vertical first-class generator route; if that fails, theorem-zero routes likely give way to scalar no-hair/source rows.

## Source Register

{markdown_table(rows["source_register"])}

## Erasure Certificate Audit

{markdown_table(rows["erasure_certificate"])}

## Theorem Ledger

{markdown_table(rows["theorem_ledger"])}

## Branch Demotion Ledger

{markdown_table(rows["demotion"])}

## Vertical Fallback Interface

{markdown_table(rows["vertical_fallback"])}

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
        "erasure_certificate": erasure_certificate_rows(),
        "theorem_ledger": theorem_ledger_rows(),
        "demotion": demotion_rows(),
        "vertical_fallback": vertical_fallback_rows(),
    }
    rows["runner_results"] = runner_results_rows(
        rows["erasure_certificate"], rows["theorem_ledger"], rows["demotion"], rows["vertical_fallback"]
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
