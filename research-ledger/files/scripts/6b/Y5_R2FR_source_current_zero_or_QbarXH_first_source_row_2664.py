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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2664"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2664-Y5-R2FR-source-current-zero-or-QbarXH-first-source-row.md"

CHECKPOINT = "2664"
BRANCH_ID = "Y5_R2FR_SOURCE_CURRENT_ZERO_OR_QBARXH_FIRST_ROW_2664"
PREFIX = "P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664"
MISSING_TOKENS = (
    "MISSING",
    "UNSIGNED",
    "NOT_PARENT",
    "NOT_DERIVED",
    "BLOCKED",
    "RETAINED",
    "PLACEHOLDER",
)

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "zero_proof_audit": RESIDUALS / f"{PREFIX}_ZERO_PROOF_AUDIT.csv",
    "qbarxh_first_row": RESIDUALS / f"{PREFIX}_QBARXH_FIRST_SOURCE_ROW_NONCLAIM.csv",
    "qbarxh_input_gate": RESIDUALS / f"{PREFIX}_QBARXH_INPUT_GATE.csv",
    "runner_results": RESIDUALS / f"{PREFIX}_SOURCE_CURRENT_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2664_SOURCE_CURRENT_ZERO_OR_QBARXH_ROW_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "Source_current_zero_audit_2664_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "QbarXH_first_source_row_2664_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2664_QBARXH_FIRST_ROW.csv",
    "quarantine": QUARANTINE / "P8_Y5_2664_SOURCE_CURRENT_RUNNER_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2663_doc": {
        "path": ROOT / "2663-Y5-R2FR-R10-source-test-charge-normalization-or-QbarXH-source-row.md",
        "needles": ["CHG2663_1_parent_charge_definition", "ZERO2663_1_source_current", "NEXT2663_0_selected"],
        "role": "immediate handoff selecting source-current zero or first Qbar_XH row",
    },
    "618_doc": {
        "path": ROOT / "618-Y5-R10-no-pole-source-zero-certificate-after-finite-branch-demotion.md",
        "needles": ["SZ618_1_Qbar_XH_boundary", "SZ618_5_full_source_zero_certificate", "V618_9_no_R10_or_local_GR_claim"],
        "role": "prior no-pole/source-zero audit showing Qbar_XH zero is not promoted",
    },
    "669_doc": {
        "path": ROOT / "669-Y5-R10-minimal-LX-sector-operator-owner-or-retained-residual-vector.md",
        "needles": ["RV669_2_J_X", "RV669_4_Qbar_XH", "V669_5_residual_vector_missing_markers"],
        "role": "minimal X-sector owner attempt and retained J_X/Qbar_XH residual vector",
    },
    "1025_doc": {
        "path": ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
        "needles": ["PHA1025_5_source_current", "ASR1025_3_Hamiltonian_projection", "BV1025_3_coupling_gap"],
        "role": "parent Hessian source-current and Hamiltonian projection schema",
    },
    "1019_doc": {
        "path": ROOT / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
        "needles": ["PO1019_4_conditional_zero", "SP1019_0_M_H_ref", "SP1019_3_bulk_R10_projection"],
        "role": "Hamiltonian projector, M_H_ref denominator and edge split obligations",
    },
    "2617_doc": {
        "path": ROOT / "2617-Y5-R2FR-single-source-map-grammar-and-source-shadow-ban-or-shadow-bound.md",
        "needles": ["SMI2617_5_current_verdict", "SSZ2617_4_current_verdict", "VAL2617_OVERALL"],
        "role": "single source-map and source-shadow trichotomy needed to silence hidden source current",
    },
    "2618_doc": {
        "path": ROOT / "2618-Y5-R2FR-parent-action-normal-form-and-source-map-identity-signature-or-shadow-coefficient-pack.md",
        "needles": ["SMG2618_0_euler_equation_gate", "ANF2618_6_current_verdict", "VAL2618_OVERALL"],
        "role": "parent action normal form showing source-map identity is signature-ready but unsigned",
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
                "source_id": f"SRC2664_{source_id}",
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


def zero_proof_audit_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "proof_id": "SCZ2664_0_target",
            "claim_candidate": "Q_X^H(lambda)=0 and therefore Qbar_XH(lambda)=0",
            "exact_condition": "parent source current rho_X and edge Hamiltonian charge vanish on the R10 source domain",
            "current_status": "TARGET_EXACT",
            "failure_mode": "none; this is the target",
            "next_action": "test each required clause",
        },
        {
            "proof_id": "SCZ2664_1_variational_definition",
            "claim_candidate": "rho_X is an Euler source, not a fitted readout",
            "exact_condition": "rho_X := delta S_parent/delta X restricted to the Hamiltonian source worldtube, with all source-like terms owned by S_parent",
            "current_status": "CONDITIONAL_DEFINITION_SCHEMA",
            "failure_mode": "parent action normal form is signature-ready but not complete",
            "next_action": "carry rho_X as missing parent current",
        },
        {
            "proof_id": "SCZ2664_2_absent_quotient_zero",
            "claim_candidate": "source current vanishes because X is absent from the physical quotient",
            "exact_condition": "S_parent=S_obs[q(Phi)]+S_matter[psi,e_obs(q(Phi)),theta]+S_boundary[q(Phi)] and X is not an independent tangent direction",
            "current_status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "failure_mode": "current corpus still permits physical X blocks or shadow/source residuals",
            "next_action": "do not set Q_X^H=0 from quotient language alone",
        },
        {
            "proof_id": "SCZ2664_3_vertical_descent_zero",
            "claim_candidate": "source current vanishes along a vertical first-class direction",
            "exact_condition": "v_X in ker(Dq), S_matter descends to q(Phi), representation constants are vertical-silent, and hidden source tails are absent",
            "current_status": "CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "failure_mode": "same missing q/v_X/matter/no-marker/no-hidden-tail clauses that blocked qbar_XT",
            "next_action": "retain finite source row unless a single parent certificate closes",
        },
        {
            "proof_id": "SCZ2664_4_projector_boundary_zero",
            "claim_candidate": "Hamiltonian projection kills source/edge charge",
            "exact_condition": "Q_X^H is exact/proper gauge or edge-only mass-independent, and Pi_M^H[Q_X^H]=0 at fixed reference data",
            "current_status": "CONDITIONAL_PROJECTOR_ZERO_NOT_DERIVED",
            "failure_mode": "Pi_M^H, M_H_ref, edge mass-independence and reference silence remain unsigned",
            "next_action": "split bulk, edge and shadow charges rather than cancel them",
        },
        {
            "proof_id": "SCZ2664_5_source_shadow_blocker",
            "claim_candidate": "no source-shadow or non-Hilbert route regenerates rho_X",
            "exact_condition": "single identity source-map, no post-Euler projector, no nonminimal/shadow action term, no boundary/improvement bulk source, no decoupled conserved residual",
            "current_status": "NORMAL_FORM_CONTRACT_READY_PARENT_UNSIGNED",
            "failure_mode": "2617/2618 classify the loophole but do not eliminate every parent candidate",
            "next_action": "keep shadow/non-Hilbert source as an explicit blocker",
        },
        {
            "proof_id": "SCZ2664_6_no_cancellation_guard",
            "claim_candidate": "bulk source, edge charge and shadow source can cancel",
            "exact_condition": "cancellation is forbidden; each component needs theorem-zero or source-backed bound before summing",
            "current_status": "CANCELLATION_FORBIDDEN",
            "failure_mode": "a small total without component ownership is not evidence",
            "next_action": "use absolute envelope",
        },
        {
            "proof_id": "SCZ2664_7_verdict",
            "claim_candidate": "source-current zero theorem for current MTS branch",
            "exact_condition": "SCZ2664_1 through SCZ2664_6 all parent-signed in one branch",
            "current_status": "SOURCE_CURRENT_ZERO_NOT_PARENT_SIGNED",
            "failure_mode": "the theorem route is exact but currently unsigned; Qbar_XH must stay as a finite nonclaim row",
            "next_action": "stage first Qbar_XH row with all missing inputs explicit",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "zero_claimed": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def qbarxh_first_row_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "row_id": "QXH2664_0_bulk_source_current",
            "component": "bulk_Q_XH(lambda)",
            "definition": "Q_bulk_X^H(lambda)=integral_{Sigma_H cap W_source} W_lambda(x;geometry) rho_X(x) dV_H",
            "required_inputs": "rho_X; source worldtube W_source; Hamiltonian slice Sigma_H; kernel weight W_lambda; dV_H; units; source_path",
            "current_status": "MISSING_PARENT_SOURCE_CURRENT_AND_DOMAIN",
            "units": "parent_X_charge",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "QXH2664_1_edge_charge",
            "component": "edge_Q_XH(lambda)",
            "definition": "Q_edge_X^H(lambda)=surface/corner/boundary Hamiltonian X charge separated from bulk current",
            "required_inputs": "B_X primitive or edge charge formula; boundary class; projector action; source_path",
            "current_status": "MISSING_EDGE_ZERO_OR_BOUND",
            "units": "parent_X_charge",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "QXH2664_2_shadow_source",
            "component": "shadow/non-Hilbert source contribution",
            "definition": "Q_shadow_X^H(lambda)=projection of any allowed source-shadow, nonminimal, post-Euler or non-Hilbert current into the X channel",
            "required_inputs": "parent normal-form classification; basis; arena projection; theorem-zero or bound",
            "current_status": "MISSING_SHADOW_SOURCE_ZERO_OR_BOUND",
            "units": "parent_X_charge",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "QXH2664_3_projected_Qbar",
            "component": "Qbar_XH(lambda)",
            "definition": "Qbar_XH(lambda)=Pi_M^H[Q_bulk_X^H(lambda)+Q_edge_X^H(lambda)+Q_shadow_X^H(lambda)]/M_H_ref",
            "required_inputs": "Pi_M^H; M_H_ref; Q_bulk; Q_edge; Q_shadow; units; source_path",
            "current_status": "MISSING_ARENA_PROJECTION",
            "units": "parent_X_charge_per_Hamiltonian_mass",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "QXH2664_4_absolute_envelope",
            "component": "abs_Qbar_XH_envelope(lambda)",
            "definition": "abs(Qbar_XH)<=abs(Pi_M Q_bulk)/M_H_ref + abs(Pi_M Q_edge)/M_H_ref + abs(Pi_M Q_shadow)/M_H_ref",
            "required_inputs": "componentwise zero theorem or source-backed bound for each term",
            "current_status": "NONCLAIM_ENVELOPE_ONLY",
            "units": "same_as_Qbar_XH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "QXH2664_5_alpha_feed",
            "component": "alpha_R10 source-side factor",
            "definition": "alpha_R10(lambda)=K_X Qbar_XH qbar_XT tau_R10 + alpha_tail_abs",
            "required_inputs": "Qbar_XH plus K_X, qbar_XT, tau_R10, tail bound and claim-valid external curve",
            "current_status": "BLOCKED_BY_QBAR_AND_OTHER_INPUTS",
            "units": "dimensionless alpha contribution",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "source_path": "NONCLAIM_FIRST_ROW",
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def qbarxh_input_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("QG2664_0_parent_rhoX", "parent source current rho_X is defined by the action", "MISSING_PARENT_SOURCE_CURRENT"),
        ("QG2664_1_source_domain", "Hamiltonian source worldtube/slice/domain is parent-owned", "MISSING_SOURCE_DOMAIN_SELECTOR"),
        ("QG2664_2_PiM", "Pi_M^H projector is defined at fixed observed frame/reference", "MISSING_PROJECTOR_LOCK"),
        ("QG2664_3_MHref", "M_H_ref denominator is stable and same-frame", "MISSING_STABLE_M_H_REF"),
        ("QG2664_4_edge_split", "bulk, edge and shadow source pieces are orthogonally split", "MISSING_ORTHOGONAL_SOURCE_SPLIT"),
        ("QG2664_5_units", "parent X charge units map into alpha(lambda)", "MISSING_DIMENSIONAL_LEDGER"),
        ("QG2664_6_verdict", "Qbar_XH can be used in an R10 alpha row", "QBAR_XH_NOT_CLAIM_READY"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "condition": condition,
            "current_status": status,
            "gate_pass": False,
            "blocks_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for gate_id, condition, status in rows
    ]


def runner_results_rows(qbar_rows: list[dict[str, Any]], proof_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for row in proof_rows:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "runner_id": f"RUN2664_{row['proof_id']}",
                "input_id": row["proof_id"],
                "input_type": "zero_proof_clause",
                "has_missing_markers": has_missing(row),
                "score_ready": row["score_ready"],
                "runner_status": "REJECTED_ZERO_PROOF_NOT_PARENT_SIGNED",
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    for row in qbar_rows:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "runner_id": f"RUN2664_{row['row_id']}",
                "input_id": row["row_id"],
                "input_type": "qbarxh_source_row",
                "has_missing_markers": has_missing(row),
                "score_ready": row["score_ready"],
                "runner_status": "REJECTED_QBARXH_INPUTS_MISSING",
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("CG2664_0_zero_theorem", "Q_X^H=0 is parent-signed", "FAIL_SOURCE_CURRENT_ZERO_UNSIGNED", "SCZ2664_7_verdict"),
        ("CG2664_1_rhoX", "rho_X/J_X is action-owned or bounded", "FAIL_PARENT_SOURCE_CURRENT_MISSING", "QG2664_0_parent_rhoX"),
        ("CG2664_2_projector", "Pi_M^H and M_H_ref are stable", "FAIL_PROJECTOR_DENOMINATOR_MISSING", "QG2664_2_PiM;QG2664_3_MHref"),
        ("CG2664_3_components", "bulk/edge/shadow source pieces are separately zeroed or bounded", "FAIL_COMPONENT_SPLIT_MISSING", "QG2664_4_edge_split"),
        ("CG2664_4_qbar_row", "Qbar_XH row is numeric/theorem-zero and sourced", "FAIL_QBARXH_NONCLAIM_TEMPLATE", "QXH2664_3_projected_Qbar"),
        ("CG2664_5_verdict", "R10/local finite-range source side can be scored or claimed", "CLAIM_BLOCKED", "zero theorem unsigned and Qbar row missing inputs"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "requirement": requirement,
            "current_status": status,
            "evidence_ref": evidence_ref,
            "gate_pass": False,
            "blocks_claim": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for gate_id, requirement, status, evidence_ref in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "decision_id": "DEC2664_0_zero_attempt",
            "decision": "source-current zero is an exact theorem target but not a current result",
            "reason": "absent-quotient, vertical descent, boundary projector and source-shadow clauses do not close together",
            "next_action": "keep Qbar_XH finite/nonclaim",
        },
        {
            "decision_id": "DEC2664_1_first_row",
            "decision": "first Qbar_XH row is staged",
            "reason": "the row now names bulk source current, edge charge, shadow source, projector, denominator and units explicitly",
            "next_action": "derive the Hamiltonian source-domain/projector lock before any numeric Qbar row",
        },
        {
            "decision_id": "DEC2664_2_best_next",
            "decision": "attack Pi_M^H/M_H_ref/source-domain ownership next",
            "reason": "even a finite source current cannot enter alpha(lambda) until the source domain and Hamiltonian mass projector are owned",
            "next_action": "build 2665 Hamiltonian source-domain and PiM lock",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2664_0_selected",
            "status": "selected",
            "next_doc": "2665-Y5-R2FR-Hamiltonian-source-domain-and-PiM-QbarXH-lock.md",
            "next_script": "scripts/Y5_R2FR_Hamiltonian_source_domain_and_PiM_QbarXH_lock_2665.py",
            "task": "derive or source-lock the Hamiltonian source domain, Pi_M^H projector and M_H_ref denominator needed by Qbar_XH",
            "must_include": "source worldtube, Hamiltonian slice, fixed-reference projector, M_H_ref, edge/shadow split, units and no-cancellation guard",
            "must_exclude": "invented Qbar_XH values, source-current zero by assertion, R10/local-GR pass claim, GitHub action, formalization-workbench edits",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("STAT2664_0_progress", "source-current zero", "EXACT_TARGET_FAILED_CURRENT_CLAIM", "the zero theorem is now clause-by-clause and no longer hand-wavy"),
        ("STAT2664_1_progress", "Qbar_XH", "FIRST_NONCLAIM_ROW_STAGED", "bulk, edge, shadow, projector and denominator are separated"),
        ("STAT2664_2_gap", "source side", "PROJECTOR_DOMAIN_DENOMINATOR_MISSING", "Qbar cannot be numeric until Pi_M^H and M_H_ref are owned"),
        ("STAT2664_3_project", "GR/local route", "STILL_BLOCKED_BUT_MORE_EXECUTABLE", "the coupling wall is now a finite source/projection ledger, not a fog bank"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": status_id,
            "topic": topic,
            "status": status,
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for status_id, topic, status, detail in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    generated = stamp()
    copy_specs = {
        "queue": (OUTPUTS["qbarxh_first_row"], BRANCH_COPIES["queue"], "QbarXH source-current input queue"),
        "local_bounds": (OUTPUTS["zero_proof_audit"], BRANCH_COPIES["local_bounds"], "source-current zero audit"),
        "source_weight": (OUTPUTS["qbarxh_first_row"], BRANCH_COPIES["source_weight"], "first QbarXH source row"),
        "microscope": (OUTPUTS["qbarxh_first_row"], BRANCH_COPIES["microscope"], "microscope QbarXH source row copy"),
        "quarantine": (OUTPUTS["runner_results"], BRANCH_COPIES["quarantine"], "runner refusal results"),
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
                "copy_id": f"COPY2664_{copy_id}",
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
        "*2664-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2664*",
        "*Y5_R2FR_source_current_zero_or_QbarXH_first_source_row_2664*",
        "*JR2664*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    zero_ok = any(
        row["proof_id"] == "SCZ2664_7_verdict" and row["current_status"] == "SOURCE_CURRENT_ZERO_NOT_PARENT_SIGNED"
        for row in rows["zero_proof_audit"]
    ) and all(not row["zero_claimed"] and not row["valid_for_claim"] for row in rows["zero_proof_audit"])
    qbar_ok = any(row["row_id"] == "QXH2664_3_projected_Qbar" for row in rows["qbarxh_first_row"]) and all(
        not row["score_ready"] and not row["valid_for_claim"] for row in rows["qbarxh_first_row"]
    )
    gate_ok = all(not row["gate_pass"] and row["blocks_claim"] for row in rows["qbarxh_input_gate"]) and any(
        row["gate_id"] == "QG2664_6_verdict" and row["current_status"] == "QBAR_XH_NOT_CLAIM_READY"
        for row in rows["qbarxh_input_gate"]
    )
    runner_ok = len(rows["runner_results"]) == len(rows["zero_proof_audit"]) + len(rows["qbarxh_first_row"]) and all(
        row["runner_status"] in {"REJECTED_ZERO_PROOF_NOT_PARENT_SIGNED", "REJECTED_QBARXH_INPUTS_MISSING"}
        for row in rows["runner_results"]
    )
    claim_ok = any(
        row["gate_id"] == "CG2664_5_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]
    ) and all(not row["gate_pass"] and row["blocks_claim"] for row in rows["claim_gates"])
    next_ok = any("2665-Y5-R2FR-Hamiltonian-source-domain" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2664_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2664_01_zero_audit", zero_ok, "source-current zero theorem is audited and not promoted"),
        ("VAL2664_02_qbar_first_row", qbar_ok, "first Qbar_XH row is staged as nonclaim"),
        ("VAL2664_03_input_gate", gate_ok, "Qbar_XH input gates block claim promotion"),
        ("VAL2664_04_runner_refuses", runner_ok, "runner rejects unsigned zero proof and missing Qbar inputs"),
        ("VAL2664_05_claim_gates_blocked", claim_ok, "R10/local claim gates remain blocked"),
        ("VAL2664_06_next_target", next_ok, "2665 Hamiltonian source-domain/PiM lock target selected"),
        ("VAL2664_07_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2664_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2664_09_formalization_untouched", formal_ok, "no 2664 outputs are written under formalization-workbench"),
        ("VAL2664_10_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
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
            "validation_id": "VAL2664_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2664 rejects source-current zero as unsigned, stages the first Qbar_XH row, and selects Hamiltonian source-domain/PiM lock next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = read_csv(OUTPUTS["validation"])
    content = f"""# 2664 - Source-Current Zero Or QbarXH First Source Row

## Purpose

This checkpoint tries the clean theorem first: `Q_X^H=0`, hence `Qbar_XH=0`. The theorem does not close for the current corpus, so the fallback is a first honest `Qbar_XH` source row with every missing parent input named.

## Result

- `Q_X^H=0` is an exact theorem target, but not a current MTS result.
- The blockers are now explicit: parent `rho_X`, source domain, `Pi_M^H`, `M_H_ref`, edge split, source-shadow silence and units.
- The first `Qbar_XH` row is staged as nonclaim: bulk, edge and shadow components are separated under an absolute no-cancellation envelope.
- Next target is the Hamiltonian source-domain and `Pi_M^H/M_H_ref` lock.

## Source Register

{markdown_table(rows["source_register"])}

## Source-Current Zero Proof Audit

{markdown_table(rows["zero_proof_audit"])}

## First QbarXH Source Row

{markdown_table(rows["qbarxh_first_row"])}

## QbarXH Input Gate

{markdown_table(rows["qbarxh_input_gate"])}

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
        "zero_proof_audit": zero_proof_audit_rows(),
        "qbarxh_first_row": qbarxh_first_row_rows(),
        "qbarxh_input_gate": qbarxh_input_gate_rows(),
    }
    rows["runner_results"] = runner_results_rows(rows["qbarxh_first_row"], rows["zero_proof_audit"])
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
