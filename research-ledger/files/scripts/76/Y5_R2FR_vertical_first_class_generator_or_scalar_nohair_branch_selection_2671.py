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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2671"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2671-Y5-R2FR-vertical-first-class-generator-or-scalar-nohair-branch-selection.md"

CHECKPOINT = "2671"
BRANCH_ID = "Y5_R2FR_VERTICAL_FIRST_CLASS_OR_SCALAR_NOHAIR_2671"
PREFIX = "P8_Y5_R2FR_VERTICAL_FIRST_CLASS_2671"
MISSING_TOKENS = (
    "MISSING",
    "UNSIGNED",
    "NOT_PARENT",
    "NOT_DERIVED",
    "BLOCKED",
    "NOT_COMPUTED",
    "NOT_CHECKED",
    "OPEN",
    "VALUES_MISSING",
)

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "vertical_certificate": RESIDUALS / f"{PREFIX}_CERTIFICATE_AUDIT.csv",
    "omega_bridge": RESIDUALS / f"{PREFIX}_OMEGA_BRIDGE_AUDIT.csv",
    "demotion": RESIDUALS / f"{PREFIX}_THEOREM_ZERO_DEMOTION_LEDGER.csv",
    "scalar_fallback": RESIDUALS / f"{PREFIX}_SCALAR_NOHAIR_FALLBACK_INTERFACE_NONCLAIM.csv",
    "runner_results": RESIDUALS / f"{PREFIX}_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2671_VERTICAL_FIRST_CLASS_QUEUE_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "Vertical_first_class_generator_2671_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "SCALAR_NOHAIR_FALLBACK_INTERFACE_2671_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2671_VERTICAL_FIRST_CLASS.csv",
    "quarantine": QUARANTINE / "P8_Y5_2671_VERTICAL_RUNNER_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2670_doc": {
        "path": ROOT / "2670-Y5-R2FR-absent-quotient-LX-erasure-certificate-or-branch-demotion.md",
        "needles": ["NEXT2670_0_selected", "VFB2670_0_vX_generator", "QER2670_10_verdict"],
        "role": "handoff from absent-quotient demotion into vertical first-class route",
    },
    "590_dcdagger": {
        "path": RESIDUALS / "P8_Y5_R10_590_DCDAGGER_VERTICAL_MAP.csv",
        "needles": ["DVM590_2_momentum_map_identity", "DVM590_3_precise_map", "DVM590_4_raise_index"],
        "role": "DCdagger/Omega-flat bridge and warning that DCdagger is not v_X by itself",
    },
    "590_field_map": {
        "path": RESIDUALS / "P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv",
        "needles": ["metric_or_coframe", "domain_memory_projector_fields", "boundary_edge"],
        "role": "field-by-field vertical action gaps",
    },
    "590_gate": {
        "path": RESIDUALS / "P8_Y5_R10_590_MAPPING_CLOSURE_GATE.csv",
        "needles": ["MCG590_0_parent_Omega", "MCG590_2_vertical_generator", "MCG590_5_no_proper_stabilizer"],
        "role": "mapping closure gates for Omega, DC_X, v_X and stabilizers",
    },
    "581_chain": {
        "path": RESIDUALS / "P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv",
        "needles": ["QVT581_4_Hamiltonian_constraints", "QVT581_5_boundary_charge", "QVT581_7_alpha_result"],
        "role": "first-class constraint theorem chain and unfilled premises",
    },
    "581_boundary": {
        "path": RESIDUALS / "P8_Y5_R10_581_BOUNDARY_CHARGE_AUDIT.csv",
        "needles": ["BCA581_0_proper_gauge", "BCA581_4_mass_channel_projection", "BCA581_5_verdict"],
        "role": "boundary charge and mass projection blockers",
    },
    "581_constraint": {
        "path": RESIDUALS / "P8_Y5_R10_581_CONSTRAINT_ALGEBRA_REQUIREMENTS.csv",
        "needles": ["CAR581_3_bracket_closure", "CAR581_5_boundary_generator"],
        "role": "constraint algebra requirements",
    },
    "582_gate": {
        "path": RESIDUALS / "P8_Y5_R10_582_NOPOLE_GATE_STATUS.csv",
        "needles": ["NPG582_0_momentum_map_owner", "NPG582_3_bracket_closure", "NPG582_4_degree_count"],
        "role": "no-pole gate status for momentum map, boundary, bracket and degree count",
    },
    "618_no_pole": {
        "path": RESIDUALS / "P8_Y5_R10_618_NO_POLE_CERTIFICATE_AUDIT.csv",
        "needles": ["NPC618_3_constraint_and_boundary", "NPC618_5_exact_q_loc_zero"],
        "role": "no-pole certificate audit and residual warning",
    },
    "669_doc": {
        "path": ROOT / "669-Y5-R10-minimal-LX-sector-operator-owner-or-retained-residual-vector.md",
        "needles": ["LX669_1_vertical_constraint", "LX669_2_positive_sourcefree_massive", "EV669_1_best_route"],
        "role": "minimal L_X route ordering: vertical before scalar no-hair",
    },
    "1025_doc": {
        "path": ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
        "needles": ["SV1025_2_Hessian_signs", "SV1025_5_sourcefree_nohair", "BV1025_3_coupling_gap"],
        "role": "positive scalar no-hair fallback contract",
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
    return any(token in joined.upper() for token in MISSING_TOKENS)


def source_register_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": f"SRC2671_{source_id}",
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


def vertical_certificate_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "clause_id": "VFC2671_0_contract",
            "clause": "vertical first-class theorem-zero route",
            "required_statement": "X is a first-class vertical generator, not a physical local propagating or sourced field",
            "evidence_now": "2670 staged this as the next theorem-zero route after absent quotient demotion",
            "current_status": "TARGET_EXACT",
            "failure_effect": "none; this is the target",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "VFC2671_1_parent_symplectic_package",
            "clause": "parent Theta/Omega owned",
            "required_statement": "parent symplectic potential Theta and two-form Omega exist on all variables used by the local branch",
            "evidence_now": "590 mapping gate marks parent Omega missing",
            "current_status": "MISSING_PARENT_OMEGA",
            "failure_effect": "DCdagger remains a covector with no legal inverse map to v_X",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "VFC2671_2_DCX_operator",
            "clause": "explicit C_X and DC_X",
            "required_statement": "C_X and its linearization DC_X are written from the parent action with a fixed domain and boundary pairing",
            "evidence_now": "590 only gives the formal adjoint side",
            "current_status": "MISSING_DCX_OPERATOR",
            "failure_effect": "cannot compare DCdagger with Omega-flat vertical action",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "VFC2671_3_raise_index",
            "clause": "construct v_X=Omega^{-1}[(DC_X)^dagger X]",
            "required_statement": "Omega is nondegenerate on the reduced domain and raises the DCdagger covector to the actual vertical generator",
            "evidence_now": "590 derives the category correction exactly",
            "current_status": "CONDITIONAL_MAP_THEOREM_VALUES_MISSING",
            "failure_effect": "using DCdagger as v_X would be a category error",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "VFC2671_4_field_by_field_action",
            "clause": "v_X on every parent field",
            "required_statement": "v_X acts on metric/coframe, canonical momenta, GK/qloc sector, memory/projectors, matter readout and boundary/edge variables",
            "evidence_now": "590 field map lists candidates but marks several blocks unmapped or not derived",
            "current_status": "MISSING_FIELD_BY_FIELD_VERTICAL_ACTION",
            "failure_effect": "no actual generator exists to test as first-class",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "VFC2671_5_momentum_map",
            "clause": "delta G_X=Omega(delta Phi,v_X)",
            "required_statement": "G_X=int epsilon C_X+Q_X is differentiable and its variation equals the Omega pairing with v_X",
            "evidence_now": "590 and 582 state the required identity",
            "current_status": "MOMENTUM_MAP_OWNER_NOT_DERIVED",
            "failure_effect": "X cannot be classified as a true gauge/constraint generator",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "VFC2671_6_boundary_differentiability",
            "clause": "Q_X differentiable and zero/proper/exact",
            "required_statement": "Q_X cancels boundary variation and is zero, proper gauge, or exact on compact local branch",
            "evidence_now": "581/582 boundary audits keep edge and Hamiltonian mass projection live",
            "current_status": "BOUNDARY_CHARGE_ZERO_NOT_DERIVED",
            "failure_effect": "edge hair or Qbar_XH leakage survives",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "VFC2671_7_bracket_closure",
            "clause": "first-class bracket closure",
            "required_statement": "{G_X[epsilon],G_X[eta]} closes weakly on parent constraints with no boundary cocycle",
            "evidence_now": "581 constraint audit and 582 no-pole gate mark bracket not computed",
            "current_status": "BRACKET_CLOSURE_NOT_COMPUTED",
            "failure_effect": "second-class remnant or physical local X mode remains possible",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "VFC2671_8_degree_count",
            "clause": "constraint rank and no proper stabilizer",
            "required_statement": "primary/secondary constraints remove the X pair and reduced Omega has no proper X stabilizer",
            "evidence_now": "590/581/582 mark reduced nondegeneracy, stabilizer and rank count missing",
            "current_status": "DEGREE_COUNT_NOT_CHECKED",
            "failure_effect": "zero Hessian can mean under-specified dynamics instead of gauge",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "clause_id": "VFC2671_9_verdict",
            "clause": "vertical theorem-zero verdict",
            "required_statement": "VFC2671_1 through VFC2671_8 close together",
            "evidence_now": "formal bridge is clear, but parent symplectic package, field map, boundary, bracket and rank are missing",
            "current_status": "VERTICAL_FIRST_CLASS_GENERATOR_NOT_DERIVED",
            "failure_effect": "demote theorem-zero vertical route and move to scalar no-hair/source branch",
            "theorem_zero_credit": False,
            "demote_if_missing": True,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def omega_bridge_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "bridge_id": "OMB2671_0_category_rule",
            "statement": "(DC_X)^dagger X is a covector; v_X is a vector",
            "required_for_use": "Omega^flat(v_X)=(DC_X)^dagger X with parent Omega owned",
            "status": "CATEGORY_RULE_DERIVED",
            "claim_effect": "blocks the cheat of calling DCdagger the generator directly",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "bridge_id": "OMB2671_1_inverse_rule",
            "statement": "v_X=Omega^{-1}[(DC_X)^dagger X] only after reduced nondegeneracy",
            "required_for_use": "reduced Omega inverse, ordinary gauge quotient, domain and stabilizer theorem",
            "status": "INVERSE_RULE_CONDITIONAL",
            "claim_effect": "no vertical theorem-zero without Omega inverse and no-stabilizer proof",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "bridge_id": "OMB2671_2_boundary_rule",
            "statement": "even a good bulk v_X fails no-pole if Q_X or K_boundary survives",
            "required_for_use": "differentiable zero/proper/exact Q_X and mass-projector silence",
            "status": "BOUNDARY_RULE_BLOCKED",
            "claim_effect": "edge branch remains live",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "bridge_id": "OMB2671_3_verdict",
            "statement": "the bridge is logically sharp but not parent-filled",
            "required_for_use": "all bridge rows plus VFC2671 certificate",
            "status": "OMEGA_BRIDGE_NOT_CLAIM_READY",
            "claim_effect": "vertical generator cannot zero R10/PPN/local-GR yet",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def demotion_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "demotion_id": "DEM2671_0_vertical",
            "branch": "vertical first-class generator",
            "demotion_status": "DEMOTED_TO_CONDITIONAL_ONLY",
            "reason": "parent Omega, DC_X, v_X field map, boundary charge, bracket closure and degree count do not close together",
            "retained_obligation": "cannot set K_X, qbar_XT or Qbar_XH to zero from vertical/gauge language",
            "next_route": "positive scalar no-hair operator/source/boundary lock",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "demotion_id": "DEM2671_1_theorem_zero_routes",
            "branch": "quotient plus vertical theorem-zero family",
            "demotion_status": "NOT_AVAILABLE_FOR_CURRENT_CLAIMS",
            "reason": "absent quotient failed in 2670 and vertical first-class fails here",
            "retained_obligation": "future parent action can reopen theorem-zero, but current local work must use scalar no-hair or finite residual rows",
            "next_route": "2672 scalar no-hair branch",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def scalar_fallback_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "row_id": "SNH2671_0_operator",
            "target": "positive self-adjoint local X operator",
            "required_inputs": "Z_X>0;M_X^2>0;field_units;self_adjoint_domain;lambda_X",
            "source_hint": "1025 SV1025_2_Hessian_signs",
            "status": "MISSING_PARENT_OPERATOR_VALUES",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "SNH2671_1_source_zero",
            "target": "J_X=0 channel-by-channel",
            "required_inputs": "matter pullback;hidden conformal/disformal exclusion;clock/EM/material-marker descent",
            "source_hint": "1025 SV1025_5_sourcefree_nohair",
            "status": "MISSING_SOURCE_ZERO_PROOF",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "SNH2671_2_boundary_flux_zero",
            "target": "boundary_flux_X=0",
            "required_inputs": "boundary class;falloff;B_X exact/proper;projector orthogonality",
            "source_hint": "581/1019 boundary audits",
            "status": "MISSING_BOUNDARY_LOCK",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "SNH2671_3_energy_identity",
            "target": "integral_A[Z_X|grad X|^2+M_X^2 X^2]=integral_A XJ_X+boundary_flux_X",
            "required_inputs": "operator values;source zero;boundary zero;domain",
            "source_hint": "1025 sourcefree nohair row",
            "status": "CONDITIONAL_IDENTITY_READY_VALUES_MISSING",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "row_id": "SNH2671_4_sourced_residual_fallback",
            "target": "finite source alpha if no-hair fails",
            "required_inputs": "K_X;Qbar_XH;qbar_XT;lambda_X;bound_curve;source paths",
            "source_hint": "1025 ASR1025_5_candidate_alpha",
            "status": "MISSING_SOURCE_BACKED_ALPHA_PACK",
            "score_ready": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def runner_results_rows(
    vertical_certificate: list[dict[str, Any]],
    omega_bridge: list[dict[str, Any]],
    demotion: list[dict[str, Any]],
    scalar_fallback: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated = stamp()
    rows: list[dict[str, Any]] = []
    for row in vertical_certificate:
        status = "REJECTED_VERTICAL_CLAUSE_UNSIGNED"
        if row["clause_id"] == "VFC2671_0_contract":
            status = "PASS_TARGET_ONLY_NO_ZERO_CREDIT"
        rows.append(
            {
                "run_id": f"RUN2671_{row['clause_id']}",
                "input_id": row["clause_id"],
                "input_type": "vertical_certificate",
                "has_missing_marker": has_missing(row),
                "runner_status": status,
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    for table_name, table in (
        ("omega_bridge", omega_bridge),
        ("demotion", demotion),
        ("scalar_fallback", scalar_fallback),
    ):
        key = "bridge_id" if table_name == "omega_bridge" else "demotion_id" if table_name == "demotion" else "row_id"
        for row in table:
            rows.append(
                {
                    "run_id": f"RUN2671_{row[key]}",
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
            "gate_id": "CG2671_0_vertical_zero",
            "claim": "X is first-class vertical and has no physical local pole",
            "current_status": "FAIL_VERTICAL_CERTIFICATE_UNSIGNED",
            "blocking_rows": "VFC2671_1_parent_symplectic_package;VFC2671_4_field_by_field_action;VFC2671_7_bracket_closure",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2671_1_R10",
            "claim": "R10 X alpha row inactive by first-class constraint",
            "current_status": "FAIL_NO_FIRST_CLASS_NO_POLE_CREDIT",
            "blocking_rows": "VFC2671_6_boundary_differentiability;VFC2671_9_verdict",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2671_2_PPN_clock_orbit",
            "claim": "PPN/clock/orbital residuals killed by vertical gauge",
            "current_status": "FAIL_MATTER_GEOMETRY_AND_BOUNDARY_STILL_LIVE",
            "blocking_rows": "VFC2671_4_field_by_field_action;VFC2671_6_boundary_differentiability",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2671_3_local_GR",
            "claim": "local GR branch follows from first-class vertical X",
            "current_status": "FAIL_THEOREM_ZERO_ROUTE_DEMOTED",
            "blocking_rows": "DEM2671_0_vertical;DEM2671_1_theorem_zero_routes",
            "gate_pass": False,
            "blocks_claim": True,
            "claim_allowed": False,
            "timestamp_utc": generated,
        },
        {
            "gate_id": "CG2671_4_verdict",
            "claim": "any vertical theorem-zero local claim",
            "current_status": "CLAIM_BLOCKED",
            "blocking_rows": "VFC2671_9_verdict",
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
            "decision_id": "DEC2671_0_result",
            "question": "Did the vertical first-class route close?",
            "answer": "No. The formal category is now sharp, but parent Omega, DC_X, v_X, boundary, bracket and degree count are not all owned.",
            "consequence": "vertical theorem-zero route is demoted to conditional-only for current claims",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "decision_id": "DEC2671_1_best_next",
            "question": "What route remains most honest?",
            "answer": "Positive scalar no-hair: derive Z_X>0, M_X^2>0, J_X=0, boundary_flux_X=0 and a self-adjoint local domain; if that fails, source alpha rows must be filled.",
            "consequence": "move from gauge-erasure attempts to operator/source/boundary derivation",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "decision_id": "DEC2671_2_interpretation",
            "question": "What did this improve?",
            "answer": "It prevents a major category error: DCdagger is not the vertical generator until Omega supplies the inverse map.",
            "consequence": "future local-GR derivations must explicitly own the symplectic bridge",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def next_target_rows() -> list[dict[str, Any]]:
    generated = stamp()
    return [
        {
            "target_id": "NEXT2671_0_selected",
            "status": "selected",
            "next_doc": "2672-Y5-R2FR-positive-scalar-nohair-operator-source-boundary-lock-or-alpha-row.md",
            "next_script": "scripts/Y5_R2FR_positive_scalar_nohair_operator_source_boundary_lock_or_alpha_row_2672.py",
            "purpose": "derive local X silence from a positive source-free scalar operator, or stage source-backed alpha rows",
            "acceptance_gate": "Z_X>0, M_X^2>0, self-adjoint domain, J_X=0, boundary_flux_X=0 and units all close together",
            "forbidden": "source-free by assertion, boundary zero by wish, fitted scalar values, cancelling unknowns, local-GR/R10 pass claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": generated,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    generated = stamp()
    rows = [
        {
            "status_id": "PS2671_0_theorem_zero",
            "area": "quotient/vertical theorem-zero routes",
            "state": "conditional_only_for_current_claims",
            "why": "absent quotient and vertical first-class routes both lack parent certificates",
            "next_needed": "positive scalar no-hair or finite source residual",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "status_id": "PS2671_1_local_GR",
            "area": "local GR reduction",
            "state": "not_claimed_but_still_structured",
            "why": "the derivation ladder is now explicit: quotient -> vertical -> scalar no-hair -> sourced residual",
            "next_needed": "2672 scalar operator/source/boundary lock",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
        {
            "status_id": "PS2671_2_coupling",
            "area": "coupling/source gap",
            "state": "now_hits_operator_source_boundary_lock",
            "why": "the remaining clean route needs J_X=0 and boundary_flux_X=0 rather than gauge language",
            "next_needed": "derive source-zero or fill alpha coefficients",
            "valid_for_claim": False,
            "timestamp_utc": generated,
        },
    ]
    return rows


def branch_copy_rows() -> list[dict[str, Any]]:
    generated = stamp()
    copy_specs = {
        "queue": (OUTPUTS["vertical_certificate"], BRANCH_COPIES["queue"], "vertical first-class queue copy"),
        "local_bounds": (OUTPUTS["vertical_certificate"], BRANCH_COPIES["local_bounds"], "local vertical nonclaim copy"),
        "source_weight": (OUTPUTS["scalar_fallback"], BRANCH_COPIES["source_weight"], "scalar fallback nonclaim copy"),
        "microscope": (OUTPUTS["omega_bridge"], BRANCH_COPIES["microscope"], "Omega bridge audit copy"),
        "quarantine": (OUTPUTS["runner_results"], BRANCH_COPIES["quarantine"], "vertical runner refusal results"),
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
                "copy_id": f"COPY2671_{copy_id}",
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
        "*2671-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2671*",
        "*Y5_R2FR_vertical_first_class_generator_or_scalar_nohair_branch_selection_2671*",
        "*JR2671*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    vertical_ok = any(
        row["clause_id"] == "VFC2671_9_verdict" and row["current_status"] == "VERTICAL_FIRST_CLASS_GENERATOR_NOT_DERIVED"
        for row in rows["vertical_certificate"]
    ) and all(not row["theorem_zero_credit"] and not row["valid_for_claim"] for row in rows["vertical_certificate"])
    bridge_ok = any(
        row["bridge_id"] == "OMB2671_0_category_rule" and row["status"] == "CATEGORY_RULE_DERIVED"
        for row in rows["omega_bridge"]
    ) and any(row["bridge_id"] == "OMB2671_3_verdict" and row["status"] == "OMEGA_BRIDGE_NOT_CLAIM_READY" for row in rows["omega_bridge"])
    demotion_ok = any(
        row["demotion_id"] == "DEM2671_0_vertical" and row["demotion_status"] == "DEMOTED_TO_CONDITIONAL_ONLY"
        for row in rows["demotion"]
    )
    scalar_ok = all(not row["score_ready"] and not row["valid_for_claim"] for row in rows["scalar_fallback"]) and any(
        row["row_id"] == "SNH2671_3_energy_identity" for row in rows["scalar_fallback"]
    )
    runner_ok = len(rows["runner_results"]) == len(rows["vertical_certificate"]) + len(rows["omega_bridge"]) + len(rows["demotion"]) + len(rows["scalar_fallback"]) and all(
        row["runner_status"] in {"REJECTED_VERTICAL_CLAUSE_UNSIGNED", "PASS_TARGET_ONLY_NO_ZERO_CREDIT", "NONCLAIM_LEDGER_RETAINED"}
        for row in rows["runner_results"]
    )
    claim_ok = any(
        row["gate_id"] == "CG2671_4_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"]
    ) and all(not row["gate_pass"] and row["blocks_claim"] for row in rows["claim_gates"])
    decision_ok = any(row["decision_id"] == "DEC2671_1_best_next" and "Positive scalar no-hair" in row["answer"] for row in rows["decision"])
    next_ok = any("2672-Y5-R2FR-positive-scalar-nohair" in row["next_doc"] for row in rows["next_target"])
    copies_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2671_00_sources", source_ok, "all vertical/scalar source paths exist and required needles are present"),
        ("VAL2671_01_vertical_certificate", vertical_ok, "vertical first-class certificate rejects theorem-zero credit"),
        ("VAL2671_02_omega_bridge", bridge_ok, "Omega bridge category rule is recorded but not promoted"),
        ("VAL2671_03_demotion", demotion_ok, "vertical theorem-zero route is demoted to conditional-only"),
        ("VAL2671_04_scalar_fallback", scalar_ok, "scalar no-hair fallback interface is staged nonclaim"),
        ("VAL2671_05_runner_refuses", runner_ok, "runner refuses unsigned vertical clauses and retains nonclaim ledgers"),
        ("VAL2671_06_claim_gates_blocked", claim_ok, "R10/PPN/clock/orbital/local-GR claims remain blocked"),
        ("VAL2671_07_decision", decision_ok, "positive scalar no-hair selected as next route"),
        ("VAL2671_08_next_target", next_ok, "2672 scalar no-hair target selected"),
        ("VAL2671_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2671_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2671_11_formalization_untouched", formal_ok, "no 2671 outputs are written under formalization-workbench"),
        ("VAL2671_12_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
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
            "validation_id": "VAL2671_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2671 demotes the vertical first-class theorem-zero route and selects positive scalar no-hair/source rows next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = read_csv(OUTPUTS["validation"])
    content = f"""# 2671 - Vertical First-Class Generator Or Scalar Nohair Branch Selection

## Purpose

This checkpoint tests the vertical theorem-zero route directly. After `2670` demoted absent quotient, the clean remaining possibility was that `X` is a first-class vertical generator: a true gauge/constraint direction with no physical local pole.

## Result

- The formal bridge is clarified: `(DC_X)^dagger X` is a covector, not the generator.
- The actual generator would require `v_X = Omega^{-1}[(DC_X)^dagger X]` on a parent-owned reduced symplectic domain.
- Current MTS does not yet own the required `Omega`, `DC_X`, field-by-field `v_X`, differentiable zero boundary charge, bracket closure, or degree count.
- The vertical theorem-zero route is demoted to conditional-only for current claims.
- The next honest derivation route is positive scalar no-hair: prove `Z_X>0`, `M_X^2>0`, `J_X=0`, `boundary_flux_X=0`, and a self-adjoint domain, or stage source-backed alpha rows.

## Source Register

{markdown_table(rows["source_register"])}

## Vertical Certificate Audit

{markdown_table(rows["vertical_certificate"])}

## Omega Bridge Audit

{markdown_table(rows["omega_bridge"])}

## Theorem-Zero Demotion Ledger

{markdown_table(rows["demotion"])}

## Scalar Nohair Fallback Interface

{markdown_table(rows["scalar_fallback"])}

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
        "vertical_certificate": vertical_certificate_rows(),
        "omega_bridge": omega_bridge_rows(),
        "demotion": demotion_rows(),
        "scalar_fallback": scalar_fallback_rows(),
    }
    rows["runner_results"] = runner_results_rows(
        rows["vertical_certificate"], rows["omega_bridge"], rows["demotion"], rows["scalar_fallback"]
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
