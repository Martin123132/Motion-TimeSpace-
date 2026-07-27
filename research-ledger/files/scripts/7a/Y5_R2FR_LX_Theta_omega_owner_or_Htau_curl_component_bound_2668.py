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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2668"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2668-Y5-R2FR-LX-Theta-omega-owner-or-Htau-curl-component-bound.md"

CHECKPOINT = "2668"
BRANCH_ID = "Y5_R2FR_LX_THETA_OMEGA_OWNER_2668"
PREFIX = "P8_Y5_R10_LX_THETA_OMEGA_OWNER_2668"
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
    "owner_proof_audit": RESIDUALS / f"{PREFIX}_OWNER_PROOF_AUDIT.csv",
    "omega_component_template": RESIDUALS / f"{PREFIX}_OMEGA_COMPONENT_TEMPLATE_NONCLAIM.csv",
    "owner_gate": RESIDUALS / f"{PREFIX}_OWNER_GATE.csv",
    "runner_results": RESIDUALS / f"{PREFIX}_OWNER_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2668_LX_THETA_OMEGA_OWNER_QUEUE_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "LX_Theta_omega_owner_audit_2668_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "OMEGA_X_INTEGRAL_COMPONENT_2668_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2668_OMEGA_COMPONENT.csv",
    "quarantine": QUARANTINE / "P8_Y5_2668_OWNER_RUNNER_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2667_doc": {
        "path": ROOT / "2667-Y5-R2FR-Htau-integrability-curl-zero-or-MHref-component-row.md",
        "needles": ["HTC2667_1_LX_owner", "HTC2667_2_theta_omega", "NEXT2667_0_selected"],
        "role": "immediate handoff selecting L_X/Theta_X/omega_X ownership",
    },
    "669_doc": {
        "path": ROOT / "669-Y5-R10-minimal-LX-sector-operator-owner-or-retained-residual-vector.md",
        "needles": ["LX669_0_absent_quotient_variable", "V669_0_variation", "G669_6_theta_QX_owner"],
        "role": "minimal L_X branch ranking and formal variation ledger",
    },
    "1018_doc": {
        "path": ROOT / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
        "needles": ["LOC1018_0_LX_owner", "LOC1018_1_Theta_QX_owner", "CG1018_1_LX_owned"],
        "role": "sector-owner map and L_X/Theta/Q owner gate",
    },
    "1021_doc": {
        "path": ROOT / "1021-Y5-R10-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md",
        "needles": ["BXG1021_0_same_parent_origin", "SB1021_0_scalar_like_LX", "DEC1021_3_fallback"],
        "role": "same-parent origin check and scalar-like L_X conditional route",
    },
    "1022_doc": {
        "path": ROOT / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
        "needles": ["VQC1022_7_verdict", "SNH1022_5_energy_identity", "FBR1022_1_scalar_operator_pack"],
        "role": "quotient/vertical failure and scalar no-hair fallback",
    },
    "1025_doc": {
        "path": ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
        "needles": ["SV1025_0_local_block", "SV1025_2_Hessian_signs", "SV1025_6_verdict"],
        "role": "minimal scalar block and Hessian/sign contract",
    },
    "1019_doc": {
        "path": ROOT / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
        "needles": ["PO1019_2_symplectic_block", "DC1019_0_orthogonal_split", "V1019_9_claim_gates_blocked"],
        "role": "symplectic boundary block and no-cancellation source split",
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
                "source_id": f"SRC2668_{source_id}",
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


def owner_proof_audit_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "proof_id": "LTO2668_0_target",
            "object": "L_X/Theta_X/omega_X",
            "claim_candidate": "sector symplectic package is parent-owned",
            "required_condition": "one parent branch supplies L_X, delta L_X=E_X delta X+dTheta_X, omega_X=delta Theta_X, tau action, boundary pullback and units",
            "current_status": "TARGET_EXACT",
            "blocker": "none; this is the target",
            "next_action": "audit possible owner routes",
        },
        {
            "proof_id": "LTO2668_1_absent_quotient",
            "object": "quotient no-X route",
            "claim_candidate": "X has no independent L_X because it is absent from the physical quotient before variation",
            "required_condition": "S_parent=S_red[q(Phi)] and X is removed from physical tangent space with matter and boundary descent",
            "current_status": "BEST_GR_REDUCTION_ROUTE_NOT_DERIVED",
            "blocker": "actual q map, vertical generator, matter descent and boundary charge silence are unsigned",
            "next_action": "do not use quotient language to erase omega_X",
        },
        {
            "proof_id": "LTO2668_2_vertical_constraint",
            "object": "vertical first-class route",
            "claim_candidate": "X is a first-class vertical constraint direction with differentiable generator and zero boundary charge",
            "required_condition": "Dq[v_X]=0, delta G_X=Omega(delta Phi,v_X), Q_X differentiable and K_boundary=0",
            "current_status": "CONDITIONAL_ROUTE_UNSIGNED",
            "blocker": "parent Omega/DC_X and boundary differentiability do not close",
            "next_action": "retain edge/symplectic residual rows",
        },
        {
            "proof_id": "LTO2668_3_scalar_physical",
            "object": "physical scalar-like L_X",
            "claim_candidate": "L_X is a positive scalar-like local sector with source-free or sourced residual branch",
            "required_condition": "L_X=1/2 sqrt(h)(Z_X|grad X|^2+M_X^2 X^2)-sqrt(h)XJ_X plus boundary conditions from parent action",
            "current_status": "CONDITIONAL_ANSATZ_ONLY",
            "blocker": "Z_X, M_X^2, J_X, field normalization, self-adjoint domain and boundary class remain unowned",
            "next_action": "stage finite coefficients if this route is retained",
        },
        {
            "proof_id": "LTO2668_4_theta_charge",
            "object": "Theta_X,Q_tau^X,C_tau^X",
            "claim_candidate": "Hamiltonian charge comes from the same sector variation",
            "required_condition": "J_tau^X=Theta_X(L_tau X)-i_tau L_X=dQ_tau^X+C_tau^X with all terms from signed L_X",
            "current_status": "FORMULA_WRITTEN_NOT_OWNED",
            "blocker": "Theta_X/Q_X normalization is symbolic",
            "next_action": "no Hamiltonian charge credit from symbols",
        },
        {
            "proof_id": "LTO2668_5_omega",
            "object": "omega_X",
            "claim_candidate": "omega_X=delta Theta_X is parent-owned and has controlled surface pullback",
            "required_condition": "Theta_X is explicit, omega_X is closed on the branch, and surface pullback is zero/exact/bounded",
            "current_status": "MISSING_THETA_OMEGA_OWNER",
            "blocker": "surface pullback and boundary exact/proper-gauge conditions are unsigned",
            "next_action": "stage omega_X_integral component",
        },
        {
            "proof_id": "LTO2668_6_boundary_units",
            "object": "boundary pullback and units",
            "claim_candidate": "omega_X_integral has a declared surface orientation, units and no boundary leakage",
            "required_condition": "surface_pair, orientation, tau action, boundary class and Hamiltonian units are all declared",
            "current_status": "MISSING_SURFACE_BOUNDARY_UNITS",
            "blocker": "no source-backed component row exists",
            "next_action": "keep units/source paths mandatory",
        },
        {
            "proof_id": "LTO2668_7_no_cancellation",
            "object": "omega/reference/boundary/projector split",
            "claim_candidate": "symplectic curl can be cancelled by reference or boundary terms",
            "required_condition": "cancellation forbidden; each component needs theorem-zero or bound",
            "current_status": "CANCELLATION_FORBIDDEN",
            "blocker": "unknown components cannot be netted",
            "next_action": "use absolute envelope",
        },
        {
            "proof_id": "LTO2668_8_verdict",
            "object": "sector symplectic package",
            "claim_candidate": "L_X/Theta_X/omega_X is parent-owned for current MTS",
            "required_condition": "one of LTO2668_1 through LTO2668_6 closes in a single branch",
            "current_status": "LX_THETA_OMEGA_OWNER_NOT_PARENT_DERIVED",
            "blocker": "all current owner routes are conditional or symbolic",
            "next_action": "stage omega_X_integral and attack parent L_X normal-form branch selection next",
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "owner_claimed": False,
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def omega_component_template_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "row_id": "OMG2668_0_omega_X_integral",
            "component": "omega_X_integral",
            "definition": "integral_S i_tau omega_X(delta_1,delta_2) over the linked surface pair",
            "required_inputs": "L_X;Theta_X;omega_X;tau_action;surface_pair;orientation;units;source_path",
            "current_status": "MISSING_THETA_OMEGA_SURFACE_INPUTS",
            "units": "Hamiltonian_curl_units",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "OMG2668_1_LX_branch",
            "component": "L_X_branch_selector",
            "definition": "which owner branch is active: absent quotient, vertical constraint, scalar source-free, scalar sourced, edge branch or nonlocal kernel",
            "required_inputs": "branch_id;parent_action_signature;field_normalization;boundary_class;source_path",
            "current_status": "MISSING_PARENT_LX_BRANCH_SELECTION",
            "units": "branch_metadata",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "OMG2668_2_Theta_Q_normalization",
            "component": "Theta_X/Q_tau^X normalization",
            "definition": "sector symplectic potential and Hamiltonian charge normalization from signed L_X",
            "required_inputs": "Theta_X;Q_tau_X;C_tau_X;normalization;units;source_path",
            "current_status": "MISSING_THETA_Q_NORMALIZATION",
            "units": "Hamiltonian_charge_units",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "OMG2668_3_tau_surface_pullback",
            "component": "tau_surface_pullback",
            "definition": "pullback of i_tau omega_X to the selected linked surface pair",
            "required_inputs": "tau_id;S_inner;S_outer;orientation;normal;boundary_rule;source_path",
            "current_status": "MISSING_TAU_SURFACE_PULLBACK",
            "units": "surface_flux_units",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "OMG2668_4_boundary_exactness",
            "component": "boundary_exact_or_proper_gauge",
            "definition": "theorem-zero or finite bound for boundary pullback of omega_X",
            "required_inputs": "boundary_class;B_class;proper_gauge_rule;no_hair_rule;bound_value;units;source_path",
            "current_status": "MISSING_BOUNDARY_EXACTNESS_OR_BOUND",
            "units": "surface_flux_units",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "OMG2668_5_absolute_envelope",
            "component": "epsilon_omega_abs",
            "definition": "absolute envelope for omega_X_integral plus boundary/reference/projector splits with no cancellation",
            "required_inputs": "componentwise theorem-zero or source-backed bound for every contribution",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "units": "dimensionless_or_flux_over_mass",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "OMG2668_6_Htau_feed",
            "component": "H_tau curl feed",
            "definition": "delta_H_tau_nonintegrable_over_MH can only be zero or bounded after omega_X_integral is owned or bounded",
            "required_inputs": "omega_X_integral plus reference/projector/boundary components and M_H_ref normalization",
            "current_status": "BLOCKED_BY_OMEGA_OWNER",
            "units": "dimensionless_or_flux_over_mass",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            **row,
            "source_path": "NONCLAIM_OMEGA_COMPONENT_TEMPLATE",
            "timestamp_utc": generated,
        }
        for row in rows
    ]


def owner_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("LOG2668_0_branch", "one L_X owner branch is selected by the parent action", "MISSING_PARENT_LX_BRANCH_SELECTION"),
        ("LOG2668_1_LX", "L_X is signed with field normalization and boundary class", "MISSING_SIGNED_LX"),
        ("LOG2668_2_Theta", "Theta_X is derived from delta L_X", "MISSING_THETA_X_OWNER"),
        ("LOG2668_3_Qtau", "J_tau^X=dQ_tau^X+C_tau^X is derived and normalized", "MISSING_QTAU_X_OWNER"),
        ("LOG2668_4_omega", "omega_X=delta Theta_X is controlled on the branch", "MISSING_OMEGA_X_OWNER"),
        ("LOG2668_5_boundary", "surface pullback is zero/exact/proper gauge or bounded", "MISSING_BOUNDARY_PULLBACK_LOCK"),
        ("LOG2668_6_units", "omega and Hamiltonian charge units are declared", "MISSING_SYMPLECTIC_UNITS"),
        ("LOG2668_7_verdict", "L_X/Theta_X/omega_X owner is claim-ready", "LX_THETA_OMEGA_OWNER_NOT_CLAIM_READY"),
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
                "runner_id": f"RUN2668_{row['proof_id']}",
                "input_id": row["proof_id"],
                "input_type": "owner_proof_clause",
                "has_missing_markers": has_missing(row),
                "score_ready": row["score_ready"],
                "runner_status": "REJECTED_OWNER_NOT_PARENT_DERIVED",
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    for row in component_rows:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "runner_id": f"RUN2668_{row['row_id']}",
                "input_id": row["row_id"],
                "input_type": "omega_component_row",
                "has_missing_markers": has_missing(row),
                "score_ready": row["score_ready"],
                "runner_status": "REJECTED_OMEGA_COMPONENT_INPUTS_MISSING",
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("CG2668_0_owner", "L_X/Theta_X/omega_X are parent-owned", "FAIL_OWNER_UNSIGNED", "LTO2668_8_verdict"),
        ("CG2668_1_branch", "owner branch is selected without ambiguity", "FAIL_BRANCH_SELECTION_MISSING", "OMG2668_1_LX_branch"),
        ("CG2668_2_theta", "Theta_X/Q_tau normalization is real", "FAIL_THETA_Q_MISSING", "OMG2668_2_Theta_Q_normalization"),
        ("CG2668_3_omega", "omega_X_integral is zero or bounded", "FAIL_OMEGA_COMPONENT_MISSING", "OMG2668_0_omega_X_integral"),
        ("CG2668_4_Htau", "H_tau curl can use omega_X safely", "FAIL_HTAU_FEED_BLOCKED", "OMG2668_6_Htau_feed"),
        ("CG2668_5_verdict", "R10/local denominator branch can be scored or claimed", "CLAIM_BLOCKED", "sector symplectic owner unsigned and omega component missing"),
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
            "decision_id": "DEC2668_0_owner_status",
            "decision": "L_X/Theta_X/omega_X ownership is not derived",
            "reason": "quotient, vertical, scalar and sourced branches all remain conditional or coefficient-missing",
            "next_action": "keep omega_X_integral nonclaim",
        },
        {
            "decision_id": "DEC2668_1_component_status",
            "decision": "omega_X_integral is staged as the next H_tau curl component",
            "reason": "without the sector symplectic form, H_tau integrability cannot be claimed",
            "next_action": "fill only after branch, Theta/Q normalization, tau/surface pullback and units exist",
        },
        {
            "decision_id": "DEC2668_2_best_next",
            "decision": "attack parent L_X normal-form branch selection next",
            "reason": "the first missing owner input is not a number but the branch: absent quotient, vertical constraint, scalar source-free, scalar sourced, edge or nonlocal",
            "next_action": "derive the branch selection or stage a finite omega component bound",
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
            "next_id": "NEXT2668_0_selected",
            "status": "selected",
            "next_doc": "2669-Y5-R2FR-parent-LX-normal-form-branch-selection-or-omega-bound.md",
            "next_script": "scripts/Y5_R2FR_parent_LX_normal_form_branch_selection_or_omega_bound_2669.py",
            "task": "derive which parent L_X branch is allowed for the local sector, or stage a finite omega_X_integral bound interface",
            "must_include": "absent quotient, vertical constraint, scalar source-free, scalar sourced, edge/boundary and nonlocal kernel branches; branch exclusion criteria; omega-bound fallback",
            "must_exclude": "mixing branches, symbolic L_X ownership, assuming boundary silence, cancelling unknown components, R10/local-GR pass claim, GitHub action, formalization-workbench edits",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        ("STAT2668_0_progress", "symplectic owner", "OWNER_AUDIT_COMPLETE_NONCLAIM", "L_X/Theta/omega ownership is now the named gate"),
        ("STAT2668_1_component", "omega_X_integral", "COMPONENT_STAGED_NONCLAIM", "omega integral is ready for future theorem-zero or bound"),
        ("STAT2668_2_root_blocker", "branch selection", "NEXT_ROOT_TARGET", "the parent must choose quotient/vertical/scalar/source/nonlocal before coefficients matter"),
        ("STAT2668_3_project", "GR/local route", "DENOMINATOR_CHAIN_SHARPER_NOT_CLOSED", "local source normalization is stricter but still not claim-ready"),
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
        "queue": (OUTPUTS["omega_component_template"], BRANCH_COPIES["queue"], "omega component input queue"),
        "local_bounds": (OUTPUTS["owner_proof_audit"], BRANCH_COPIES["local_bounds"], "L_X/Theta/omega owner audit"),
        "source_weight": (OUTPUTS["omega_component_template"], BRANCH_COPIES["source_weight"], "omega component template"),
        "microscope": (OUTPUTS["omega_component_template"], BRANCH_COPIES["microscope"], "microscope omega component copy"),
        "quarantine": (OUTPUTS["runner_results"], BRANCH_COPIES["quarantine"], "owner runner refusal results"),
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
                "copy_id": f"COPY2668_{copy_id}",
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
        "*2668-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2668*",
        "*Y5_R2FR_LX_Theta_omega_owner_or_Htau_curl_component_bound_2668*",
        "*JR2668*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    proof_ok = any(
        row["proof_id"] == "LTO2668_8_verdict"
        and row["current_status"] == "LX_THETA_OMEGA_OWNER_NOT_PARENT_DERIVED"
        for row in rows["owner_proof_audit"]
    ) and all(not row["owner_claimed"] and not row["score_ready"] and not row["valid_for_claim"] for row in rows["owner_proof_audit"])
    template_ok = any(row["row_id"] == "OMG2668_0_omega_X_integral" for row in rows["omega_component_template"]) and any(
        row["row_id"] == "OMG2668_5_absolute_envelope" for row in rows["omega_component_template"]
    ) and all(not row["score_ready"] and not row["valid_for_claim"] for row in rows["omega_component_template"])
    gate_ok = all(not row["gate_pass"] and row["blocks_claim"] for row in rows["owner_gate"]) and any(
        row["gate_id"] == "LOG2668_7_verdict" and row["current_status"] == "LX_THETA_OMEGA_OWNER_NOT_CLAIM_READY"
        for row in rows["owner_gate"]
    )
    runner_ok = len(rows["runner_results"]) == len(rows["owner_proof_audit"]) + len(rows["omega_component_template"]) and all(
        row["runner_status"] in {"REJECTED_OWNER_NOT_PARENT_DERIVED", "REJECTED_OMEGA_COMPONENT_INPUTS_MISSING"}
        for row in rows["runner_results"]
    )
    claim_ok = any(
        row["gate_id"] == "CG2668_5_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]
    ) and all(not row["gate_pass"] and row["blocks_claim"] for row in rows["claim_gates"])
    next_ok = any("2669-Y5-R2FR-parent-LX-normal-form" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2668_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2668_01_owner_audit", proof_ok, "L_X/Theta/omega owner audit is written and not promoted"),
        ("VAL2668_02_omega_template", template_ok, "omega component template includes omega integral and absolute envelope"),
        ("VAL2668_03_owner_gate", gate_ok, "owner gates block claim promotion"),
        ("VAL2668_04_runner_refuses", runner_ok, "runner rejects unsigned owner and missing omega components"),
        ("VAL2668_05_claim_gates_blocked", claim_ok, "R10/local claim gates remain blocked"),
        ("VAL2668_06_next_target", next_ok, "2669 parent L_X branch-selection target selected"),
        ("VAL2668_07_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2668_08_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2668_09_formalization_untouched", formal_ok, "no 2668 outputs are written under formalization-workbench"),
        ("VAL2668_10_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
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
            "validation_id": "VAL2668_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2668 rejects L_X/Theta/omega ownership as unsigned, stages omega_X_integral, and selects parent L_X branch selection next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = read_csv(OUTPUTS["validation"])
    content = f"""# 2668 - LX Theta Omega Owner Or Htau Curl Component Bound

## Purpose

This checkpoint asks whether the sector symplectic package is actually owned: `L_X`, `Theta_X`, and `omega_X=delta Theta_X`. Without this package, the `H_tau` integrability curl cannot be zeroed.

## Result

- `L_X/Theta_X/omega_X` is not parent-derived for the current branch.
- The allowed owner routes are now explicit: absent quotient, vertical constraint, scalar source-free, scalar sourced, edge/boundary or nonlocal kernel.
- `omega_X_integral` is staged as a live nonclaim component with surface, tau, boundary, units and no-cancellation requirements.
- The next target is parent `L_X` normal-form branch selection.

## Source Register

{markdown_table(rows["source_register"])}

## Owner Proof Audit

{markdown_table(rows["owner_proof_audit"])}

## Omega Component Template

{markdown_table(rows["omega_component_template"])}

## Owner Gate

{markdown_table(rows["owner_gate"])}

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
        "owner_proof_audit": owner_proof_audit_rows(),
        "omega_component_template": omega_component_template_rows(),
        "owner_gate": owner_gate_rows(),
    }
    rows["runner_results"] = runner_results_rows(rows["owner_proof_audit"], rows["omega_component_template"])
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
