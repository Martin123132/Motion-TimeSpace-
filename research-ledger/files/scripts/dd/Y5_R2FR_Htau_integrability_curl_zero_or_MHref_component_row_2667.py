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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2667"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2667-Y5-R2FR-Htau-integrability-curl-zero-or-MHref-component-row.md"

CHECKPOINT = "2667"
BRANCH_ID = "Y5_R2FR_HTAU_INTEGRABILITY_CURL_2667"
PREFIX = "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667"
MISSING_TOKENS = (
    "MISSING",
    "UNSIGNED",
    "NOT_PARENT",
    "NOT_DERIVED",
    "BLOCKED",
    "RETAINED",
    "UNFILLED",
    "PLACEHOLDER",
)

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "curl_proof_audit": RESIDUALS / f"{PREFIX}_CURL_PROOF_AUDIT.csv",
    "component_template": RESIDUALS / f"{PREFIX}_COMPONENT_ROW_TEMPLATE_NONCLAIM.csv",
    "integrability_gate": RESIDUALS / f"{PREFIX}_INTEGRABILITY_GATE.csv",
    "runner_results": RESIDUALS / f"{PREFIX}_CURL_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2667_HTAU_INTEGRABILITY_CURL_COMPONENT_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "Htau_integrability_curl_audit_2667_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "HTAU_INTEGRABILITY_COMPONENT_2667_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2667_HTAU_CURL_COMPONENT.csv",
    "quarantine": QUARANTINE / "P8_Y5_2667_CURL_RUNNER_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2666_doc": {
        "path": ROOT / "2666-Y5-R2FR-MHref-integrability-reference-lock-or-denominator-row.md",
        "needles": ["MHL2666_2_integrability", "DROW2666_1_integrability_curl", "NEXT2666_0_selected"],
        "role": "immediate handoff selecting H_tau integrability curl",
    },
    "1018_doc": {
        "path": ROOT / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
        "needles": ["LOC1018_1_Theta_QX_owner", "FSR1018_1_delta_H_tau", "V1018_1_owner_map_complete"],
        "role": "sector Lagrangian, symplectic potential and delta_H_tau row",
    },
    "669_doc": {
        "path": ROOT / "669-Y5-R10-minimal-LX-sector-operator-owner-or-retained-residual-vector.md",
        "needles": ["V669_3_symplectic", "V669_4_integrability", "IM669_0_delta_H_tau"],
        "role": "minimal X-sector symplectic/integrability formula and residual impact",
    },
    "1017_doc": {
        "path": ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
        "needles": ["MHR1017_1_delta_H_tau_nonintegrable", "MHR1017_5_FB5540_total", "DEC1017_0_reference_lock"],
        "role": "denominator integrability row and no-cancellation total",
    },
    "1014_doc": {
        "path": ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
        "needles": ["PCT1014_6_no_closure_from_algebra", "PCC1014_3_projector_stress_beta_equiv", "V1014_7_claim_gates_blocked"],
        "role": "projector algebra and projector-stress obstruction",
    },
    "1019_doc": {
        "path": ROOT / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
        "needles": ["PO1019_2_symplectic_block", "PO1019_3_reference_silence", "DC1019_0_orthogonal_split"],
        "role": "symplectic block, reference silence and no-cancellation split",
    },
    "1013_doc": {
        "path": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
        "needles": ["PFC1013_0_same_frame_JH", "OBS1013_1_PiM_commutator", "OBS1013_5_projector_stress"],
        "role": "same-frame source and PiM commutator/projector stress retained rows",
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
                "source_id": f"SRC2667_{source_id}",
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


def curl_proof_audit_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "proof_id": "HTC2667_0_target",
            "object": "delta_H_tau_nonintegrable_over_MH",
            "claim_candidate": "H_tau integrability curl vanishes",
            "required_condition": "delta_1 delta_2 H_tau - delta_2 delta_1 H_tau = integral_S i_tau omega_X(delta_1,delta_2) plus reference/boundary pieces = 0",
            "current_status": "TARGET_EXACT",
            "blocker": "none; this is the target",
            "next_action": "audit owner clauses",
        },
        {
            "proof_id": "HTC2667_1_LX_owner",
            "object": "L_X",
            "claim_candidate": "sector action owns the Hamiltonian variation",
            "required_condition": "delta L_X=E_X delta X+dTheta_X from a parent-signed L_X with field normalization and boundary class",
            "current_status": "FORMULA_WRITTEN_NOT_PARENT_OWNED",
            "blocker": "minimal L_X candidates are routes, not signed current-MTS derivations",
            "next_action": "retain L_X owner as first missing clause",
        },
        {
            "proof_id": "HTC2667_2_theta_omega",
            "object": "Theta_X and omega_X",
            "claim_candidate": "symplectic form is exact and controlled",
            "required_condition": "omega_X=delta Theta_X is derived from the same parent sector and its boundary pullback is zero/exact/bounded",
            "current_status": "MISSING_THETA_OMEGA_OWNER",
            "blocker": "Theta_X/Q_X normalization and boundary pullback are not owned",
            "next_action": "stage omega_X_integral component",
        },
        {
            "proof_id": "HTC2667_3_tau_action_surface",
            "object": "tau action and surface pair",
            "claim_candidate": "the same tau and linked surfaces define H_tau and the curl",
            "required_condition": "L_tau Phi, S_inner/S_outer, source-exterior homology class and field-variation pair are fixed pre-readout",
            "current_status": "MISSING_TAU_SURFACE_VARIATION_LOCK",
            "blocker": "tau/surface/domain selector remains conditional",
            "next_action": "carry tau_id and surface_pair fields",
        },
        {
            "proof_id": "HTC2667_4_boundary_exactness",
            "object": "surface curl",
            "claim_candidate": "integrability obstruction is a pure boundary exact term that vanishes",
            "required_condition": "integral_S i_tau omega_X is exact/proper gauge or zero under boundary class/no-hair/projector silence",
            "current_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "blocker": "boundary class, symplectic block and reference silence are unsigned",
            "next_action": "no boundary-zero credit",
        },
        {
            "proof_id": "HTC2667_5_projector_domain_stress",
            "object": "Pi_M/domain/Hodge variation",
            "claim_candidate": "projector/domain variation does not feed the curl",
            "required_condition": "delta Pi_M, domain selector, normals and Green/Hodge data are fixed or stress-bounded",
            "current_status": "RETAINED_UNFILLED_PROJECTOR_STRESS",
            "blocker": "Pi_M algebra alone does not imply flux closure",
            "next_action": "retain projector stress component",
        },
        {
            "proof_id": "HTC2667_6_reference_curl_split",
            "object": "reference curl",
            "claim_candidate": "reference subtraction does not cancel integrability curl",
            "required_condition": "reference curl, Delta_ref and symplectic boundary flux are separated and bounded without cancellation",
            "current_status": "NO_CANCELLATION_SPLIT_REQUIRED",
            "blocker": "reference silence is not signed",
            "next_action": "stage reference_curl as separate component",
        },
        {
            "proof_id": "HTC2667_7_verdict",
            "object": "H_tau integrability curl zero",
            "claim_candidate": "delta_H_tau_nonintegrable_over_MH=0 for current MTS branch",
            "required_condition": "HTC2667_1 through HTC2667_6 close in one parent branch",
            "current_status": "HTAU_INTEGRABILITY_CURL_ZERO_NOT_PARENT_DERIVED",
            "blocker": "the proof shape is exact but L_X/Theta/omega/tau/boundary/projector clauses are unsigned",
            "next_action": "stage delta_H_tau_nonintegrable_over_MH component row",
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


def component_template_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "row_id": "HCUR2667_0_delta_H_tau_nonintegrable",
            "component": "delta_H_tau_nonintegrable_over_MH",
            "definition": "field-space curl obstruction of H_tau normalized by M_H_ref",
            "required_inputs": "surface_pair;field_variation_pair;integrability_curl;M_H_ref;units;source_path",
            "current_status": "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_or_flux_over_mass",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "HCUR2667_1_omega_integral",
            "component": "omega_X_integral",
            "definition": "integral_S i_tau omega_X(delta_1,delta_2) over the linked surface pair",
            "required_inputs": "Theta_X;omega_X;tau_action;surface_pair;orientation;units;source_path",
            "current_status": "MISSING_THETA_OMEGA_SURFACE_INPUTS",
            "units": "Hamiltonian_curl_units",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "HCUR2667_2_tau_surface_variations",
            "component": "tau_surface_variation_lock",
            "definition": "fixed tau and two independent field variations used for the curl test",
            "required_inputs": "tau_id;delta_1;delta_2;S_inner;S_outer;domain_rule;source_path",
            "current_status": "MISSING_TAU_SURFACE_VARIATION_LOCK",
            "units": "metadata",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "HCUR2667_3_reference_curl",
            "component": "reference_curl_over_MH",
            "definition": "curl induced by reference subtraction, kept separate from H_tau integrability",
            "required_inputs": "H_ref;reference_branch;reference_curl;M_H_ref;units;source_path",
            "current_status": "MISSING_REFERENCE_CURL_ZERO_OR_BOUND",
            "units": "dimensionless_or_flux_over_mass",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "HCUR2667_4_projector_domain_stress",
            "component": "projector_domain_stress_over_MH",
            "definition": "delta Pi_M/domain/Hodge stress contribution if the projector varies through the curl",
            "required_inputs": "delta_PiM;domain_selector;normal_variation;Green_or_Hodge_data;PPN_map;units;source_path",
            "current_status": "MISSING_PROJECTOR_STRESS_MAP",
            "units": "dimensionless_or_PPN_mapped_units",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "HCUR2667_5_absolute_envelope",
            "component": "epsilon_Htau_curl_abs",
            "definition": "abs(delta_H_tau_curl)+abs(reference_curl)+abs(projector_domain_stress)+abs(boundary_flux) with no cancellation",
            "required_inputs": "componentwise theorem-zero or source-backed bound for each term",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "units": "dimensionless_envelope",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "HCUR2667_6_MHref_feed",
            "component": "M_H_ref denominator feed",
            "definition": "M_H_ref may use H_tau only if the integrability curl component is zero or bounded",
            "required_inputs": "HCUR2667_0 through HCUR2667_5 plus M_H_ref denominator row",
            "current_status": "BLOCKED_BY_HTAU_CURL_COMPONENT",
            "units": "Hamiltonian_mass_or_energy",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "source_path": "NONCLAIM_HTAU_CURL_TEMPLATE",
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def integrability_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("ICG2667_0_LX_owner", "parent L_X owns the sector Hamiltonian variation", "MISSING_LX_OWNER"),
        ("ICG2667_1_theta_omega", "Theta_X and omega_X are parent-derived with units", "MISSING_THETA_OMEGA_OWNER"),
        ("ICG2667_2_tau_surface", "tau, surface pair and variation pair are fixed before readout", "MISSING_TAU_SURFACE_VARIATION_LOCK"),
        ("ICG2667_3_boundary_exact", "surface curl is zero/exact/proper gauge or bounded", "MISSING_BOUNDARY_EXACTNESS_OR_BOUND"),
        ("ICG2667_4_projector_stress", "PiM/domain/Hodge projector stress is zero or bounded", "MISSING_PROJECTOR_STRESS_MAP"),
        ("ICG2667_5_reference_split", "reference curl is separated and not cancelled", "MISSING_REFERENCE_CURL_ZERO_OR_BOUND"),
        ("ICG2667_6_units", "curl units and M_H_ref normalization are declared", "MISSING_CURL_UNITS_AND_DENOMINATOR"),
        ("ICG2667_7_verdict", "H_tau integrability curl is claim-ready", "HTAU_INTEGRABILITY_CURL_NOT_CLAIM_READY"),
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


def runner_results_rows(proof_rows: list[dict[str, Any]], component_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for row in proof_rows:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "runner_id": f"RUN2667_{row['proof_id']}",
                "input_id": row["proof_id"],
                "input_type": "curl_proof_clause",
                "has_missing_markers": has_missing(row),
                "score_ready": row["score_ready"],
                "runner_status": "REJECTED_CURL_ZERO_NOT_PARENT_DERIVED",
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    for row in component_rows:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "runner_id": f"RUN2667_{row['row_id']}",
                "input_id": row["row_id"],
                "input_type": "curl_component_row",
                "has_missing_markers": has_missing(row),
                "score_ready": row["score_ready"],
                "runner_status": "REJECTED_CURL_COMPONENT_INPUTS_MISSING",
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("CG2667_0_zero", "H_tau integrability curl is theorem-zero", "FAIL_CURL_ZERO_UNSIGNED", "HTC2667_7_verdict"),
        ("CG2667_1_LX", "L_X/Theta_X/omega_X are parent-owned", "FAIL_SECTOR_OWNER_MISSING", "ICG2667_0_LX_owner;ICG2667_1_theta_omega"),
        ("CG2667_2_surface", "tau/surface/variation locks are fixed", "FAIL_SURFACE_VARIATION_LOCK_MISSING", "ICG2667_2_tau_surface"),
        ("CG2667_3_components", "curl/reference/projector/boundary pieces are zero or bounded separately", "FAIL_COMPONENT_BOUNDS_MISSING", "HCUR2667_5_absolute_envelope"),
        ("CG2667_4_MHref", "M_H_ref may treat H_tau as integrable", "FAIL_MHREF_HTAU_FEED_BLOCKED", "HCUR2667_6_MHref_feed"),
        ("CG2667_5_verdict", "R10/local denominator branch can be scored or claimed", "CLAIM_BLOCKED", "H_tau curl zero unsigned and component rows missing"),
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
            "decision_id": "DEC2667_0_zero_status",
            "decision": "H_tau integrability curl zero is not derived",
            "reason": "L_X, Theta_X, omega_X, tau/surface lock, boundary exactness and projector stress are not parent-signed together",
            "next_action": "stage the curl component row",
        },
        {
            "decision_id": "DEC2667_1_component_row",
            "decision": "delta_H_tau_nonintegrable_over_MH is retained as the first M_H_ref obstruction component",
            "reason": "without it H_tau cannot be treated as a stable state function",
            "next_action": "do not use M_H_ref until the curl component is zero or bounded",
        },
        {
            "decision_id": "DEC2667_2_best_next",
            "decision": "attack L_X/Theta_X/omega_X ownership next",
            "reason": "the curl cannot be zeroed before the sector symplectic potential and form are parent-owned",
            "next_action": "derive the sector symplectic owner or stage omega_X_integral as a finite component",
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
            "next_id": "NEXT2667_0_selected",
            "status": "selected",
            "next_doc": "2668-Y5-R2FR-LX-Theta-omega-owner-or-Htau-curl-component-bound.md",
            "next_script": "scripts/Y5_R2FR_LX_Theta_omega_owner_or_Htau_curl_component_bound_2668.py",
            "task": "try to derive the parent-owned L_X/Theta_X/omega_X package needed for H_tau integrability; if it fails, stage omega_X_integral as a finite nonclaim component",
            "must_include": "L_X variation, Theta_X, omega_X=delta Theta_X, tau action, surface pullback, boundary exact/proper gauge conditions, units and source paths",
            "must_exclude": "assuming symplectic exactness, using projector algebra as closure, cancelling against reference/boundary terms, R10/local-GR pass claim, GitHub action, formalization-workbench edits",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("STAT2667_0_progress", "H_tau curl", "ZERO_THEOREM_AUDITED_NONCLAIM", "the integrability obstruction is now clause-by-clause"),
        ("STAT2667_1_component", "delta_H_tau_nonintegrable", "FIRST_DENOMINATOR_COMPONENT_STAGED", "the component row is ready for a future theorem-zero or source-backed bound"),
        ("STAT2667_2_root_blocker", "L_X/Theta/omega", "NEXT_ROOT_TARGET", "sector symplectic ownership is the next mathematical lock"),
        ("STAT2667_3_project", "GR/local route", "DENOMINATOR_CHAIN_SHARPER_NOT_CLOSED", "source normalization keeps becoming more exact, but no local claim is allowed"),
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
        "queue": (OUTPUTS["component_template"], BRANCH_COPIES["queue"], "H_tau curl component queue"),
        "local_bounds": (OUTPUTS["curl_proof_audit"], BRANCH_COPIES["local_bounds"], "H_tau integrability curl audit"),
        "source_weight": (OUTPUTS["component_template"], BRANCH_COPIES["source_weight"], "H_tau curl component template"),
        "microscope": (OUTPUTS["component_template"], BRANCH_COPIES["microscope"], "microscope H_tau curl component copy"),
        "quarantine": (OUTPUTS["runner_results"], BRANCH_COPIES["quarantine"], "curl runner refusal results"),
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
                "copy_id": f"COPY2667_{copy_id}",
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
        "*2667-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2667*",
        "*Y5_R2FR_Htau_integrability_curl_zero_or_MHref_component_row_2667*",
        "*JR2667*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    proof_ok = any(
        row["proof_id"] == "HTC2667_7_verdict"
        and row["current_status"] == "HTAU_INTEGRABILITY_CURL_ZERO_NOT_PARENT_DERIVED"
        for row in rows["curl_proof_audit"]
    ) and all(not row["zero_claimed"] and not row["score_ready"] and not row["valid_for_claim"] for row in rows["curl_proof_audit"])
    template_ok = any(row["row_id"] == "HCUR2667_0_delta_H_tau_nonintegrable" for row in rows["component_template"]) and any(
        row["row_id"] == "HCUR2667_5_absolute_envelope" for row in rows["component_template"]
    ) and all(not row["score_ready"] and not row["valid_for_claim"] for row in rows["component_template"])
    gate_ok = all(not row["gate_pass"] and row["blocks_claim"] for row in rows["integrability_gate"]) and any(
        row["gate_id"] == "ICG2667_7_verdict" and row["current_status"] == "HTAU_INTEGRABILITY_CURL_NOT_CLAIM_READY"
        for row in rows["integrability_gate"]
    )
    runner_ok = len(rows["runner_results"]) == len(rows["curl_proof_audit"]) + len(rows["component_template"]) and all(
        row["runner_status"] in {"REJECTED_CURL_ZERO_NOT_PARENT_DERIVED", "REJECTED_CURL_COMPONENT_INPUTS_MISSING"}
        for row in rows["runner_results"]
    )
    claim_ok = any(
        row["gate_id"] == "CG2667_5_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]
    ) and all(not row["gate_pass"] and row["blocks_claim"] for row in rows["claim_gates"])
    next_ok = any("2668-Y5-R2FR-LX-Theta-omega-owner" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2667_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2667_01_curl_proof_audit", proof_ok, "H_tau curl zero proof is audited and not promoted"),
        ("VAL2667_02_component_template", template_ok, "curl component template includes delta_H_tau and absolute envelope"),
        ("VAL2667_03_integrability_gate", gate_ok, "integrability gates block claim promotion"),
        ("VAL2667_04_runner_refuses", runner_ok, "runner rejects unsigned curl proof and missing components"),
        ("VAL2667_05_claim_gates_blocked", claim_ok, "R10/local claim gates remain blocked"),
        ("VAL2667_06_next_target", next_ok, "2668 L_X/Theta/omega owner target selected"),
        ("VAL2667_07_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2667_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2667_09_formalization_untouched", formal_ok, "no 2667 outputs are written under formalization-workbench"),
        ("VAL2667_10_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
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
            "validation_id": "VAL2667_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2667 rejects H_tau integrability curl zero as unsigned, stages delta_H_tau_nonintegrable_over_MH, and selects L_X/Theta/omega ownership next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = read_csv(OUTPUTS["validation"])
    content = f"""# 2667 - Htau Integrability Curl Zero Or MHref Component Row

## Purpose

This checkpoint tries the next denominator theorem: prove the `H_tau` integrability curl vanishes. The proof shape is exact, but the current corpus does not parent-sign the sector symplectic package, so the curl remains a live nonclaim component.

## Result

- `delta_H_tau_nonintegrable_over_MH=0` is not derived for the current branch.
- The missing root is the parent-owned `L_X/Theta_X/omega_X` package plus tau/surface locks and boundary/projector silence.
- The first curl component row is staged with `omega_X_integral`, tau/surface variations, reference curl, projector/domain stress and an absolute envelope.
- The next target is `L_X/Theta_X/omega_X` ownership, not a denominator shortcut.

## Source Register

{markdown_table(rows["source_register"])}

## Curl Proof Audit

{markdown_table(rows["curl_proof_audit"])}

## Curl Component Template

{markdown_table(rows["component_template"])}

## Integrability Gate

{markdown_table(rows["integrability_gate"])}

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
        "curl_proof_audit": curl_proof_audit_rows(),
        "component_template": component_template_rows(),
        "integrability_gate": integrability_gate_rows(),
    }
    rows["runner_results"] = runner_results_rows(rows["curl_proof_audit"], rows["component_template"])
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
