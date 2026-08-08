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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2666"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2666-Y5-R2FR-MHref-integrability-reference-lock-or-denominator-row.md"

CHECKPOINT = "2666"
BRANCH_ID = "Y5_R2FR_MHREF_INTEGRABILITY_REFERENCE_LOCK_2666"
PREFIX = "P8_Y5_R10_MHREF_DENOMINATOR_2666"
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
    "mhref_lock_audit": RESIDUALS / f"{PREFIX}_MHREF_LOCK_AUDIT.csv",
    "denominator_template": RESIDUALS / f"{PREFIX}_DENOMINATOR_ROW_TEMPLATE_NONCLAIM.csv",
    "component_gate": RESIDUALS / f"{PREFIX}_COMPONENT_GATE.csv",
    "runner_results": RESIDUALS / f"{PREFIX}_DENOMINATOR_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2666_MHREF_DENOMINATOR_ROW_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "MHref_integrability_reference_lock_2666_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "MHREF_DENOMINATOR_TEMPLATE_2666_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2666_MHREF_DENOMINATOR_ROW.csv",
    "quarantine": QUARANTINE / "P8_Y5_2666_DENOMINATOR_RUNNER_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2665_doc": {
        "path": ROOT / "2665-Y5-R2FR-Hamiltonian-source-domain-and-PiM-QbarXH-lock.md",
        "needles": ["HLOCK2665_3_MHref", "DEC2665_2_best_next", "NEXT2665_0_selected"],
        "role": "immediate handoff selecting M_H_ref integrability/reference lock",
    },
    "1017_doc": {
        "path": ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
        "needles": ["MHR1017_0_M_H_ref_denominator", "MHR1017_1_delta_H_tau_nonintegrable", "DEC1017_1_no_MHref_shortcut"],
        "role": "first denominator schema and no-shortcut guardrail",
    },
    "1018_doc": {
        "path": ROOT / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
        "needles": ["LOC1018_1_Theta_QX_owner", "FSR1018_0_M_H_ref", "FSR1018_1_delta_H_tau"],
        "role": "sector Lagrangian, Hamiltonian charge and denominator component rows",
    },
    "1016_doc": {
        "path": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        "needles": ["PSC1016_5_dressed_source_charge", "FIS1016_0_M_H_ref", "PST1016_4_R_eq_first_input_rule"],
        "role": "dressed source charge and normalized first-input rule",
    },
    "1013_doc": {
        "path": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
        "needles": ["PFC1013_0_same_frame_JH", "OBS1013_1_PiM_commutator", "V1013_6_claim_gates_blocked"],
        "role": "same-frame Hilbert current and commutator obstruction",
    },
    "1014_doc": {
        "path": ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
        "needles": ["PCT1014_6_no_closure_from_algebra", "PCC1014_3_projector_stress_beta_equiv", "V1014_7_claim_gates_blocked"],
        "role": "projector algebra is not enough and projector stress remains retained",
    },
    "1019_doc": {
        "path": ROOT / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
        "needles": ["SP1019_0_M_H_ref", "PO1019_0_projector_definition", "V1019_9_claim_gates_blocked"],
        "role": "same-frame denominator in source pack and fixed-frame projector definition",
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
                "source_id": f"SRC2666_{source_id}",
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


def mhref_lock_audit_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "audit_id": "MHL2666_0_target",
            "object": "M_H_ref",
            "requirement": "M_H_ref := H_tau[S_outer]-H_ref = integral_{S_outer} Q_tau after integrability/reference lock",
            "current_status": "TARGET_EXACT",
            "blocker": "none; this is the denominator target",
            "next_action": "audit each denominator component",
        },
        {
            "audit_id": "MHL2666_1_Qtau_owner",
            "object": "Q_tau/H_tau",
            "requirement": "sector Lagrangian, symplectic potential and Hamiltonian charge are parent-owned: delta L=dTheta+E delta Phi, J_tau=dQ_tau+C_tau",
            "current_status": "FORMULA_WRITTEN_NOT_PARENT_OWNED",
            "blocker": "L_X/Theta_X/Q_X and boundary class remain unsigned",
            "next_action": "retain Q_tau_integral as missing source path/value",
        },
        {
            "audit_id": "MHL2666_2_integrability",
            "object": "delta_H_tau_nonintegrable_over_MH",
            "requirement": "field-space curl of H_tau vanishes or is bounded before H_tau is a state function",
            "current_status": "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO",
            "blocker": "omega_X, tau action, surface pair and reference curl are not parent-signed",
            "next_action": "attack integrability curl first",
        },
        {
            "audit_id": "MHL2666_3_reference",
            "object": "H_ref;Delta_ref",
            "requirement": "reference subtraction is selected before readout and derivative-silent with respect to source/domain/frame/lambda",
            "current_status": "MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO",
            "blocker": "B_ref and reference branch are not parent-owned",
            "next_action": "keep Delta_ref_over_MH row active",
        },
        {
            "audit_id": "MHL2666_4_boundary_symplectic",
            "object": "B_zero_flux;Delta_symp;symplectic_boundary_flux",
            "requirement": "boundary/exact/reference/symplectic leakage is theorem-zero or bounded componentwise",
            "current_status": "MISSING_SYMPLECTIC_BOUNDARY_NUMERIC_OR_THEOREM_ZERO",
            "blocker": "boundary class/no-hair/projector silence is unsigned",
            "next_action": "separate boundary/symplectic rows under no-cancellation",
        },
        {
            "audit_id": "MHL2666_5_tau_surface",
            "object": "tau and surface pair",
            "requirement": "tau_id, S_inner/S_outer, homology class and source-exterior domain are fixed before scoring",
            "current_status": "MISSING_TAU_SURFACE_LOCK",
            "blocker": "source worldtube and linking surfaces remain conditional",
            "next_action": "carry surface_pair and domain_rule fields",
        },
        {
            "audit_id": "MHL2666_6_positive_same_frame",
            "object": "positive same-frame denominator",
            "requirement": "M_H_ref is positive/nonzero and in the same observed frame as Qbar_XH, clocks, rods and orbital readout",
            "current_status": "MISSING_POSITIVE_SAME_FRAME_DENOMINATOR",
            "blocker": "same-frame source measure is conditional and denominator value is absent",
            "next_action": "do not divide by a placeholder",
        },
        {
            "audit_id": "MHL2666_7_shortcut_ban",
            "object": "denominator substitutions",
            "requirement": "bare mass, orbital GM, reference-only 1, fitted source radius and calibrated readout mass are forbidden as M_H_ref substitutes",
            "current_status": "GUARDRAIL_ACTIVE",
            "blocker": "shortcuts would normalize with the readout the theorem is meant to derive",
            "next_action": "keep shortcuts invalid",
        },
        {
            "audit_id": "MHL2666_8_verdict",
            "object": "M_H_ref integrability/reference lock",
            "requirement": "MHL2666_1 through MHL2666_7 close together before M_H_ref is stable",
            "current_status": "MHREF_INTEGRABILITY_REFERENCE_LOCK_NOT_PARENT_DERIVED",
            "blocker": "the denominator contract is exact but all live components are missing or conditional",
            "next_action": "stage denominator row and attack H_tau integrability curl next",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "lock_pass": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def denominator_template_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "row_id": "DROW2666_0_M_H_ref",
            "component": "M_H_ref",
            "definition": "H_tau[S_outer]-H_ref = integral_{S_outer} Q_tau after integrability/reference lock",
            "required_inputs": "system_id;tau_id;surface_outer;Q_tau_integral;H_ref;M_H_ref;units;reference_rule;source_path",
            "current_status": "MISSING_STABLE_MH_REF",
            "units": "Hamiltonian_mass_or_energy",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DROW2666_1_integrability_curl",
            "component": "delta_H_tau_nonintegrable_over_MH",
            "definition": "field-space curl obstruction of H_tau normalized by M_H_ref",
            "required_inputs": "surface_pair;field_variation_pair;integrability_curl;M_H_ref;units;source_path",
            "current_status": "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_or_flux_over_mass",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DROW2666_2_reference_shift",
            "component": "Delta_ref_over_MH;H_ref_shift",
            "definition": "reference subtraction shift and derivative profile normalized by M_H_ref",
            "required_inputs": "reference_branch;Delta_ref;H_ref_shift;derivative_profile;M_H_ref;units;source_path",
            "current_status": "MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_or_flux_over_mass",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DROW2666_3_boundary_symplectic",
            "component": "symplectic_boundary_flux_over_MH;B_zero_flux;Delta_symp",
            "definition": "boundary/projector/non-EH symplectic leakage through linked surfaces normalized by M_H_ref",
            "required_inputs": "surface_pair;boundary_rule;symplectic_boundary_flux;B_zero_flux;Delta_symp;M_H_ref;units;source_path",
            "current_status": "MISSING_SYMPLECTIC_BOUNDARY_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless_or_flux_over_mass",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DROW2666_4_tau_surface_domain",
            "component": "tau_surface_domain_lock",
            "definition": "tau, surface pair and source-exterior domain are fixed before denominator evaluation",
            "required_inputs": "tau_id;S_inner;S_outer;homology_class;W_source;domain_rule;source_path",
            "current_status": "MISSING_TAU_SURFACE_DOMAIN_LOCK",
            "units": "domain_metadata",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DROW2666_5_no_cancellation_total",
            "component": "epsilon_HPiM_integrability_abs",
            "definition": "absolute component sum for denominator/reference/integrability leakage",
            "required_inputs": "abs(delta_H_tau)+abs(Delta_ref)+abs(boundary_symplectic)+abs(domain_shift) all normalized by M_H_ref",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "units": "dimensionless_envelope",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "DROW2666_6_Qbar_feed",
            "component": "Qbar_XH denominator feed",
            "definition": "Qbar_XH uses M_H_ref only after DROW2666_0 through DROW2666_5 are real",
            "required_inputs": "stable M_H_ref plus Qbar numerator components and Pi_M^H lock",
            "current_status": "BLOCKED_BY_MHREF_COMPONENTS",
            "units": "parent_X_charge_per_Hamiltonian_mass",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "source_path": "NONCLAIM_DENOMINATOR_TEMPLATE",
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def component_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("MCG2666_0_Qtau_owner", "Q_tau/H_tau is derived from parent L/Theta/Q", "MISSING_HAMILTONIAN_CHARGE_OWNER"),
        ("MCG2666_1_integrability", "delta_H_tau_nonintegrable is zero or bounded", "MISSING_INTEGRABILITY_CURL_ZERO_OR_BOUND"),
        ("MCG2666_2_reference", "H_ref and Delta_ref are fixed and derivative-silent", "MISSING_REFERENCE_LOCK"),
        ("MCG2666_3_boundary", "B_zero_flux, Delta_symp and boundary flux are zero or bounded", "MISSING_BOUNDARY_SYMPLECTIC_LOCK"),
        ("MCG2666_4_tau_surface", "tau and linked surfaces are fixed pre-readout", "MISSING_TAU_SURFACE_DOMAIN_LOCK"),
        ("MCG2666_5_positive_units", "M_H_ref is positive, nonzero and unit-locked", "MISSING_POSITIVE_UNIT_LOCKED_DENOMINATOR"),
        ("MCG2666_6_shortcuts", "bare mass/orbital GM/reference-only denominator shortcuts remain forbidden", "SHORTCUTS_FORBIDDEN_PASS"),
        ("MCG2666_7_verdict", "M_H_ref denominator is claim-ready", "MHREF_DENOMINATOR_NOT_CLAIM_READY"),
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


def runner_results_rows(audit_rows: list[dict[str, Any]], template_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for row in audit_rows:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "runner_id": f"RUN2666_{row['audit_id']}",
                "input_id": row["audit_id"],
                "input_type": "mhref_lock_audit",
                "has_missing_markers": has_missing(row),
                "score_ready": row["score_ready"],
                "runner_status": "REJECTED_MHREF_LOCK_NOT_PARENT_DERIVED",
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    for row in template_rows:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "runner_id": f"RUN2666_{row['row_id']}",
                "input_id": row["row_id"],
                "input_type": "denominator_template",
                "has_missing_markers": has_missing(row),
                "score_ready": row["score_ready"],
                "runner_status": "REJECTED_MHREF_COMPONENT_INPUTS_MISSING",
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("CG2666_0_MHref", "M_H_ref denominator is stable", "FAIL_MHREF_LOCK_MISSING", "MHL2666_8_verdict"),
        ("CG2666_1_integrability", "H_tau is integrable or bounded", "FAIL_INTEGRABILITY_CURL_MISSING", "DROW2666_1_integrability_curl"),
        ("CG2666_2_reference", "H_ref/Delta_ref are fixed or bounded", "FAIL_REFERENCE_LOCK_MISSING", "DROW2666_2_reference_shift"),
        ("CG2666_3_boundary", "boundary/symplectic components are zero or bounded", "FAIL_BOUNDARY_LOCK_MISSING", "DROW2666_3_boundary_symplectic"),
        ("CG2666_4_Qbar", "Qbar_XH may divide by M_H_ref", "FAIL_DENOMINATOR_TEMPLATE_NONCLAIM", "DROW2666_6_Qbar_feed"),
        ("CG2666_5_verdict", "R10/local source denominator can be scored or claimed", "CLAIM_BLOCKED", "M_H_ref denominator and components are missing"),
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
            "decision_id": "DEC2666_0_derivation_status",
            "decision": "M_H_ref is not derived in the current corpus",
            "reason": "H_tau integrability, H_ref/reference silence, boundary flux, tau/surface lock and positive units are not signed together",
            "next_action": "keep denominator row nonclaim",
        },
        {
            "decision_id": "DEC2666_1_denominator_row",
            "decision": "first M_H_ref denominator row is staged",
            "reason": "the row now includes denominator and numerator obstruction pieces together under no-cancellation",
            "next_action": "fill no component without source path, units and valid theorem/bound",
        },
        {
            "decision_id": "DEC2666_2_best_next",
            "decision": "attack H_tau integrability curl next",
            "reason": "without integrability, H_tau is not a state function and M_H_ref cannot be stable",
            "next_action": "derive delta_H_tau_nonintegrable=0 or stage that component as a finite row",
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
            "next_id": "NEXT2666_0_selected",
            "status": "selected",
            "next_doc": "2667-Y5-R2FR-Htau-integrability-curl-zero-or-MHref-component-row.md",
            "next_script": "scripts/Y5_R2FR_Htau_integrability_curl_zero_or_MHref_component_row_2667.py",
            "task": "try to derive H_tau integrability curl zero; if it fails, stage delta_H_tau_nonintegrable_over_MH as the first denominator obstruction component",
            "must_include": "omega_X, tau action, surface pair, field variation pair, reference curl, units, source path and no-cancellation normalization by M_H_ref",
            "must_exclude": "assuming H_tau is integrable, bare/orbital mass denominator, cancellation with Delta_ref or boundary flux, R10/local-GR pass claim, GitHub action, formalization-workbench edits",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("STAT2666_0_progress", "M_H_ref", "DENOMINATOR_CONTRACT_EXPLICIT_NONCLAIM", "stable denominator now has component rows instead of a vague missing value"),
        ("STAT2666_1_root_blocker", "H_tau integrability", "NEXT_ROOT_TARGET", "integrability is the first thing to prove before reference and boundary locks can matter"),
        ("STAT2666_2_guardrail", "shortcuts", "DENOMINATOR_SHORTCUTS_FORBIDDEN", "bare mass/orbital GM/reference-only normalization remains blocked"),
        ("STAT2666_3_project", "GR/local route", "SOURCE_NORMALIZATION_CHAIN_SHARPER_NOT_CLOSED", "local source side is more exact but still nonclaim"),
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
        "queue": (OUTPUTS["denominator_template"], BRANCH_COPIES["queue"], "M_H_ref denominator row queue"),
        "local_bounds": (OUTPUTS["mhref_lock_audit"], BRANCH_COPIES["local_bounds"], "M_H_ref lock audit"),
        "source_weight": (OUTPUTS["denominator_template"], BRANCH_COPIES["source_weight"], "M_H_ref denominator template"),
        "microscope": (OUTPUTS["denominator_template"], BRANCH_COPIES["microscope"], "microscope denominator row copy"),
        "quarantine": (OUTPUTS["runner_results"], BRANCH_COPIES["quarantine"], "denominator runner refusal results"),
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
                "copy_id": f"COPY2666_{copy_id}",
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
        "*2666-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2666*",
        "*Y5_R2FR_MHref_integrability_reference_lock_or_denominator_row_2666*",
        "*JR2666*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    audit_ok = any(
        row["audit_id"] == "MHL2666_8_verdict"
        and row["current_status"] == "MHREF_INTEGRABILITY_REFERENCE_LOCK_NOT_PARENT_DERIVED"
        for row in rows["mhref_lock_audit"]
    ) and all(not row["lock_pass"] and not row["score_ready"] and not row["valid_for_claim"] for row in rows["mhref_lock_audit"])
    template_ok = any(row["row_id"] == "DROW2666_0_M_H_ref" for row in rows["denominator_template"]) and any(
        row["row_id"] == "DROW2666_5_no_cancellation_total" for row in rows["denominator_template"]
    ) and all(not row["score_ready"] and not row["valid_for_claim"] for row in rows["denominator_template"])
    gate_ok = all(not row["gate_pass"] and row["blocks_claim"] for row in rows["component_gate"]) and any(
        row["gate_id"] == "MCG2666_7_verdict" and row["current_status"] == "MHREF_DENOMINATOR_NOT_CLAIM_READY"
        for row in rows["component_gate"]
    )
    runner_ok = len(rows["runner_results"]) == len(rows["mhref_lock_audit"]) + len(rows["denominator_template"]) and all(
        row["runner_status"] in {"REJECTED_MHREF_LOCK_NOT_PARENT_DERIVED", "REJECTED_MHREF_COMPONENT_INPUTS_MISSING"}
        for row in rows["runner_results"]
    )
    claim_ok = any(
        row["gate_id"] == "CG2666_5_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]
    ) and all(not row["gate_pass"] and row["blocks_claim"] for row in rows["claim_gates"])
    next_ok = any("2667-Y5-R2FR-Htau-integrability-curl-zero" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2666_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2666_01_mhref_audit", audit_ok, "M_H_ref lock audit is written and nonclaim"),
        ("VAL2666_02_denominator_template", template_ok, "denominator row template includes M_H_ref and no-cancellation total"),
        ("VAL2666_03_component_gate", gate_ok, "component gates block denominator claim promotion"),
        ("VAL2666_04_runner_refuses", runner_ok, "runner rejects unsigned denominator lock and missing components"),
        ("VAL2666_05_claim_gates_blocked", claim_ok, "R10/local claim gates remain blocked"),
        ("VAL2666_06_next_target", next_ok, "2667 H_tau integrability curl target selected"),
        ("VAL2666_07_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2666_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2666_09_formalization_untouched", formal_ok, "no 2666 outputs are written under formalization-workbench"),
        ("VAL2666_10_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
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
            "validation_id": "VAL2666_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2666 stages the M_H_ref denominator contract, keeps all denominator components nonclaim, and selects H_tau integrability curl next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = read_csv(OUTPUTS["validation"])
    content = f"""# 2666 - MHref Integrability Reference Lock Or Denominator Row

## Purpose

This checkpoint asks whether the stable denominator `M_H_ref` can be derived. It cannot be promoted from the current corpus, so the fallback is a nonclaim denominator row with every obstruction component exposed.

## Result

- `M_H_ref := H_tau[S_outer]-H_ref = integral_S Q_tau` is the exact target.
- The denominator is not stable until `H_tau` is integrable, `H_ref` is fixed, boundary/symplectic leakage is zero or bounded, tau/surface data are fixed, and units are owned.
- Bare mass, orbital `GM`, fitted source radius and reference-only normalization remain forbidden shortcuts.
- The first `M_H_ref` row is staged with `delta_H_tau_nonintegrable`, `Delta_ref`, boundary/symplectic flux and no-cancellation total.
- The next root target is the `H_tau` integrability curl.

## Source Register

{markdown_table(rows["source_register"])}

## MHref Lock Audit

{markdown_table(rows["mhref_lock_audit"])}

## Denominator Row Template

{markdown_table(rows["denominator_template"])}

## Component Gate

{markdown_table(rows["component_gate"])}

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
        "mhref_lock_audit": mhref_lock_audit_rows(),
        "denominator_template": denominator_template_rows(),
        "component_gate": component_gate_rows(),
    }
    rows["runner_results"] = runner_results_rows(rows["mhref_lock_audit"], rows["denominator_template"])
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
