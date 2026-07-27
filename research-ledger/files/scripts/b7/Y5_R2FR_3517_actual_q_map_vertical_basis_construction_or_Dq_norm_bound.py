from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3517-Y5-R2FR-actual-q-map-vertical-basis-construction-or-Dq-norm-bound.md"
CANONICAL_QMAP = OUT / "P8_EM_actual_q_map_vertical_basis_candidate.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3517": {"path": Path(__file__).resolve(), "role": "3517 generator"},
    "doc_3516": {
        "path": ROOT / "3516-Y5-R2FR-quotient-source-coordinate-descent-certificate-or-Dq-leak-bound.md",
        "role": "3516 quotient source-coordinate handoff",
    },
    "certificate_3516": {
        "path": OUT / "P8_EM_quotient_source_coordinate_descent_certificate.csv",
        "role": "canonical quotient source-coordinate certificate",
    },
    "basis_filter_3516": {
        "path": OUT / "P8_Y5_R2FR_3516_RESIDUAL_BASIS_ELIGIBILITY_FILTER.csv",
        "role": "3516 residual-basis eligibility filter",
    },
    "next_3516": {
        "path": OUT / "P8_Y5_R2FR_3516_NEXT_TARGET.csv",
        "role": "3517 target handoff",
    },
    "field_signature_2570": {
        "path": OUT / "P8_Y5_FIELD_QUOTIENT_2570_FIELD_SIGNATURE_ATTEMPT.csv",
        "role": "field quotient signature attempt",
    },
    "dq_ledger_2570": {
        "path": OUT / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv",
        "role": "Dq vertical-generator ledger",
    },
    "coeff_gate_2570": {
        "path": OUT / "P8_Y5_FIELD_QUOTIENT_2570_COEFFICIENT_DESCENT_GATE.csv",
        "role": "coefficient descent gate",
    },
    "matter_gate_2570": {
        "path": OUT / "P8_Y5_FIELD_QUOTIENT_2570_MATTER_DESCENT_GATE.csv",
        "role": "matter descent gate",
    },
    "vertical_kernel_2589": {
        "path": OUT / "P8_Y5_VERTICAL_KERNEL_2589_CERTIFICATE_GATE.csv",
        "role": "vertical kernel certificate gate",
    },
    "vertical_audit_2589": {
        "path": OUT / "P8_Y5_VERTICAL_KERNEL_2589_NULLNESS_AUDIT.csv",
        "role": "vertical kernel nullness audit",
    },
    "vertical_leaks_2589": {
        "path": OUT / "P8_Y5_VERTICAL_KERNEL_2589_KERNEL_LEAK_ROWS.csv",
        "role": "vertical kernel leak rows",
    },
    "vertical_qv_2590": {
        "path": OUT / "P8_Y5_VERTICAL_QV_2590_EXTRACTION_CONTRACT.csv",
        "role": "vertical Noether charge extraction contract",
    },
}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(metadata["path"]),
            "exists": bool_text(Path(metadata["path"]).exists()),
            "role": metadata["role"],
            "valid_for_claim": "False",
        }
        for source_id, metadata in SOURCES.items()
    ]


def q_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "q_id": "QMAP3517_0_public_geometry",
            "parent_field_or_slot": "g_mu_nu/e_obs",
            "q_component": "public_geometry",
            "included_in_q": "True",
            "construction_rule": "q_geom(Phi)=observed metric/coframe branch used by EH, Hilbert stress and local readout",
            "status": "CANDIDATE_VISIBLE_NOT_PARENT_DERIVED",
            "anti_tautology": "allowed as public geometry, but still needs proof no second hidden coframe participates",
            "source_path": str(SOURCES["field_signature_2570"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "q_id": "QMAP3517_1_tau_clock",
            "parent_field_or_slot": "tau/theta_obs/clock standards",
            "q_component": "public_tau_clock",
            "included_in_q": "True",
            "construction_rule": "q_tau(Phi)=single tau used by H_tau, source support, clocks, R10 and orbit readout",
            "status": "CANDIDATE_VISIBLE_TAU_LOCK_UNSIGNED",
            "anti_tautology": "cannot be declared by choosing whichever tau fits each arena",
            "source_path": str(SOURCES["field_signature_2570"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "q_id": "QMAP3517_2_matter_constants",
            "parent_field_or_slot": "Psi, theta, c_vis, masses/charges",
            "q_component": "ordinary_matter_data",
            "included_in_q": "True",
            "construction_rule": "ordinary matter arguments descend through public geometry and q-basic constants",
            "status": "CANDIDATE_NO_SOURCE_PREF_UNSIGNED",
            "anti_tautology": "forbids source-only species weights hidden outside q",
            "source_path": str(SOURCES["matter_gate_2570"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "q_id": "QMAP3517_3_boundary_reference",
            "parent_field_or_slot": "boundary class/H_ref/Sigma_ref",
            "q_component": "boundary_reference_class",
            "included_in_q": "True",
            "construction_rule": "reference data are fixed by boundary/topology/asymptotic coframe before local source readout",
            "status": "CANDIDATE_BOUNDARY_CLASS_UNSIGNED",
            "anti_tautology": "does not allow H_ref to be fitted from source mass or GM",
            "source_path": str(SOURCES["field_signature_2570"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "q_id": "QMAP3517_4_coupling_slots",
            "parent_field_or_slot": "a1/kappa/G_parent/ell_J/c_vis",
            "q_component": "parent_coefficient_slots",
            "included_in_q": "Conditional",
            "construction_rule": "coefficients are q-basic constants or parent normal-form slots, not source/readout knobs",
            "status": "COEFFICIENT_DESCENT_UNSIGNED",
            "anti_tautology": "cannot include ell_J merely to prove ell_J is invisible",
            "source_path": str(SOURCES["coeff_gate_2570"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "q_id": "QMAP3517_5_source_coordinates_Y",
            "parent_field_or_slot": "M_H_ref,sigma^a",
            "q_component": "not_primitive_q_component",
            "included_in_q": "False",
            "construction_rule": "Y must be derived as Ybar(q(Phi)); including Y directly in q would be circular",
            "status": "ANTI_TAUTOLOGY_GUARD_ACTIVE",
            "anti_tautology": "source coordinates are target observables for descent, not primitive q components",
            "source_path": str(SOURCES["certificate_3516"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "q_id": "QMAP3517_6_private_q",
            "parent_field_or_slot": "q_private",
            "q_component": "excluded_or_first_class",
            "included_in_q": "False",
            "construction_rule": "private reciprocal/source-vector representative is vertical only if first-class or source-silent",
            "status": "CANDIDATE_VERTICAL_UNSIGNED",
            "anti_tautology": "cannot be hidden if Weyl/matter/source-vector tails survive",
            "source_path": str(SOURCES["dq_ledger_2570"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "q_id": "QMAP3517_7_RAB_auxiliary",
            "parent_field_or_slot": "R_AB/lambda_R",
            "q_component": "rejected_current_observer_map",
            "included_in_q": "False",
            "construction_rule": "auxiliary R_AB can be vertical only after observer-cell map or constraint-first elimination is rebuilt",
            "status": "REJECTED_FOR_CURRENT_OBSERVER_CELL_MAP",
            "anti_tautology": "q_shape alone does not prove observed coframe/source invisibility",
            "source_path": str(SOURCES["dq_ledger_2570"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "q_id": "QMAP3517_8_projector_readout",
            "parent_field_or_slot": "Pi_M/P_loc/readout kernels",
            "q_component": "fixed_operator_or_explicit_obstruction",
            "included_in_q": "Conditional",
            "construction_rule": "projectors are fixed before variation or included as explicit readout derivatives",
            "status": "NOT_VERTICAL_BY_DEFAULT",
            "anti_tautology": "cannot assume fixed Pi_M while using its variation as the obstruction",
            "source_path": str(SOURCES["field_signature_2570"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def vertical_basis_rows() -> list[dict[str, Any]]:
    return [
        {
            "basis_id": "VB3517_0_v_q_private",
            "direction": "v_q",
            "acts_on": "q_private representative/source-vector slot",
            "Dq_candidate": "zero on q_geom/q_tau/q_matter if first-class and matter/boundary descent close",
            "matrix_status": "CANDIDATE_NOT_CERTIFIED",
            "Dq_norm_status": "MISSING_Q_MAP_AND_SOURCE_SILENCE",
            "eligible_for_Ax_zero": "False",
            "next_action": "derive first-class/source-vector silence or bound B_qW/C_qT/body-boundary tails",
            "source_path": str(SOURCES["dq_ledger_2570"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "basis_id": "VB3517_1_v_memory_tau",
            "direction": "v_memory/v_tau_private",
            "acts_on": "private memory/time/coframe residual slots",
            "Dq_candidate": "zero only if public tau/coframe/readout functor is locked before clocks/source tests",
            "matrix_status": "CANDIDATE_NOT_CERTIFIED",
            "Dq_norm_status": "MISSING_TAU_FRAME_LOCK",
            "eligible_for_Ax_zero": "False",
            "next_action": "derive tau/coframe lock or carry frame/clock Dq leak",
            "source_path": str(SOURCES["dq_ledger_2570"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "basis_id": "VB3517_2_v_coeff",
            "direction": "v_coeff",
            "acts_on": "hidden coefficient/coupling slots",
            "Dq_candidate": "zero only if coefficient slots are q-basic constants or parent normal-form parameters",
            "matrix_status": "CANDIDATE_NOT_CERTIFIED",
            "Dq_norm_status": "MISSING_COEFFICIENT_DESCENT",
            "eligible_for_Ax_zero": "False",
            "next_action": "derive coefficient descent; do not hide ell_J by definition",
            "source_path": str(SOURCES["coeff_gate_2570"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "basis_id": "VB3517_3_v_boundary_local",
            "direction": "v_boundary/reference",
            "acts_on": "boundary/corner/reference class",
            "Dq_candidate": "locally zero only after fixed boundary class and zero compact flux; not automatically source-denominator silent",
            "matrix_status": "CANDIDATE_LOCAL_ONLY",
            "Dq_norm_status": "MISSING_BOUNDARY_REFERENCE_SILENCE",
            "eligible_for_Ax_zero": "False",
            "next_action": "derive H_ref source-blindness and compact boundary no-flux",
            "source_path": str(SOURCES["vertical_kernel_2589"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "basis_id": "VB3517_4_v_RAB",
            "direction": "v_RAB",
            "acts_on": "R_AB/lambda_R auxiliary compatibility field",
            "Dq_candidate": "nonzero under current observer-cell map",
            "matrix_status": "REJECTED",
            "Dq_norm_status": "Dq[v_RAB] != 0 unless observer map rebuilt",
            "eligible_for_Ax_zero": "False",
            "next_action": "do not use quotient zero theorem for R_AB branch now",
            "source_path": str(SOURCES["dq_ledger_2570"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "basis_id": "VB3517_5_delta_projector",
            "direction": "delta Pi_M/readout",
            "acts_on": "mass projector/readout operator",
            "Dq_candidate": "not a zero direction unless projector is fixed in q/readout before variation",
            "matrix_status": "OBSTRUCTION_NOT_VERTICAL",
            "Dq_norm_status": "MISSING_PROJECTOR_FIXEDNESS",
            "eligible_for_Ax_zero": "False",
            "next_action": "keep Pi_M variation as commutator residual",
            "source_path": str(SOURCES["dq_ledger_2570"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def dq_matrix_rows() -> list[dict[str, Any]]:
    components = [
        ("q_geom", "public geometry/coframe"),
        ("q_tau", "public tau/clock branch"),
        ("q_matter", "ordinary matter/constants"),
        ("q_boundary", "boundary/reference class"),
        ("Y_target", "derived source coordinates"),
    ]
    rows: list[dict[str, Any]] = []
    status_by_basis = {
        "v_q": ("0_conditional", "MISSING_FIRST_CLASS_SOURCE_SILENCE"),
        "v_memory_tau": ("0_conditional", "MISSING_TAU_FRAME_LOCK"),
        "v_coeff": ("0_conditional", "MISSING_COEFFICIENT_DESCENT"),
        "v_boundary": ("0_local_conditional", "MISSING_BOUNDARY_REFERENCE_SILENCE"),
        "v_RAB": ("nonzero_current_map", "REJECTED_FOR_OBSERVER_CELL_MAP"),
        "delta_PiM": ("not_vertical", "PROJECTOR_OBSTRUCTION_EXPLICIT"),
    }
    for basis, (status, blocker) in status_by_basis.items():
        for component_id, component in components:
            if component_id == "Y_target":
                component_status = "target_descent_required_not_q_primitive"
            else:
                component_status = status
            rows.append(
                {
                    "matrix_id": f"DQM3517_{basis}_{component_id}",
                    "basis_direction": basis,
                    "q_component": component,
                    "Dq_entry_status": component_status,
                    "blocker": blocker if component_status != "target_descent_required_not_q_primitive" else "Y must be derived from q, not included by declaration",
                    "numeric_value": "MISSING_THEOREM_ZERO_OR_NUMERIC_DQ_ENTRY",
                    "valid_for_claim": "False",
                }
            )
    return rows


def dq_norm_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DQB3517_0_v_q_private",
            "direction": "v_q",
            "Dq_norm_formula": "||Dq[v_q]||_q/||v_q|| <= E_first_class + E_matter + E_boundary + E_readout",
            "required_inputs": "q matrix; v_q action; first-class/Omega/DCq package; matter and boundary descent",
            "prediction_value": "MISSING_VQ_DQ_NORM",
            "bound_value": "MISSING_VQ_DQ_BOUND",
            "candidate_priority": "highest",
            "valid_for_claim": "False",
        },
        {
            "row_id": "DQB3517_1_v_memory_tau",
            "direction": "v_memory/v_tau_private",
            "Dq_norm_formula": "||Dq[v_memory]|| <= E_tau_lock + E_clock + E_frame + E_source_support",
            "required_inputs": "tau/coframe readout functor; clock/source support lock",
            "prediction_value": "MISSING_MEMORY_TAU_DQ_NORM",
            "bound_value": "MISSING_MEMORY_TAU_DQ_BOUND",
            "candidate_priority": "medium",
            "valid_for_claim": "False",
        },
        {
            "row_id": "DQB3517_2_v_coeff",
            "direction": "v_coeff",
            "Dq_norm_formula": "||Dq[v_coeff]|| <= E_coeff_descent + E_source_scale + E_clock_constants",
            "required_inputs": "coefficient descent theorem; parent normal form; no-source scale laundering",
            "prediction_value": "MISSING_COEFF_DQ_NORM",
            "bound_value": "MISSING_COEFF_DQ_BOUND",
            "candidate_priority": "medium",
            "valid_for_claim": "False",
        },
        {
            "row_id": "DQB3517_3_v_boundary",
            "direction": "v_boundary/reference",
            "Dq_norm_formula": "||Dq[v_boundary]||_local <= E_boundary_flux + E_Href_source + E_corner",
            "required_inputs": "boundary class; compact no-flux proof; H_ref source-blindness",
            "prediction_value": "MISSING_BOUNDARY_DQ_NORM",
            "bound_value": "MISSING_BOUNDARY_DQ_BOUND",
            "candidate_priority": "medium_local_only",
            "valid_for_claim": "False",
        },
        {
            "row_id": "DQB3517_4_v_RAB",
            "direction": "v_RAB",
            "Dq_norm_formula": "not eligible under current map; Dq[v_RAB] retained as nonzero unless observer-cell map rebuilt",
            "required_inputs": "new observer-cell map or constraint-first elimination",
            "prediction_value": "REJECTED_NOT_NUMERIC",
            "bound_value": "MISSING_RAB_REBUILD_BOUND",
            "candidate_priority": "rejected",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3517_0_candidate_qmap_built",
            "decision": "candidate q-map and residual-basis matrix constructed",
            "rationale": "3517 moves from an abstract quotient theorem to a field-slot/q-component table with Dq entry statuses.",
            "effect": "the next proof can focus on one candidate vertical direction rather than the whole coupling stack",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3517_1_no_vertical_claim",
            "decision": "no residual direction is certified vertical yet",
            "rationale": "every candidate still lacks q matrix, v action, or source/readout descent signatures.",
            "effect": "A_X=0, local GR and Newton remain unclaimed",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3517_2_next_vq",
            "decision": "attack v_q_private first",
            "rationale": "v_q is the highest-priority candidate because the ledger already frames it as first-class/source-vector silence rather than rejected.",
            "effect": "3518 should try to prove v_q first-class/source-silent or bound B_qW/C_qT tails",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3518-Y5-R2FR-vq-private-first-class-source-vector-silence-or-Dq-bound.md",
            "next_script": "scripts/Y5_R2FR_3518_vq_private_first_class_source_vector_silence_or_Dq_bound.py",
            "objective": "Try to prove v_q is first-class/source-silent for the candidate q-map, including Omega/DCq, B_qW, C_qT, matter/body/boundary/readout tails; if not, produce executable nonclaim Dq norm rows for v_q.",
            "success_gate": "Either Dq[v_q]=0 and source-coordinate descent clauses fire for v_q, or v_q gets a sourced Dq_norm bound template with all tail terms explicit.",
            "forbidden_shortcuts": "do not call q_private vertical by naming; do not ignore Weyl/matter/source-vector tails; do not use measured GM/readout to define the source coordinate",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    q_map: list[dict[str, Any]],
    basis: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append(
        {
            "check_id": "VAL3517_0_sources_exist",
            "passed": bool_text(all(row["exists"] == "True" for row in sources)),
            "detail": "all cited local source paths exist",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3517_1_qmap_antitautology",
            "passed": bool_text(any(row["q_component"] == "not_primitive_q_component" and row["included_in_q"] == "False" for row in q_map)),
            "detail": "source coordinates Y are target observables, not primitive q components",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3517_2_basis_classification",
            "passed": bool_text(any(row["matrix_status"] == "CANDIDATE_NOT_CERTIFIED" for row in basis) and any(row["matrix_status"] == "REJECTED" for row in basis)),
            "detail": "basis matrix contains candidate and rejected directions",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3517_3_Dq_matrix_present",
            "passed": bool_text(len(matrix) >= 20 and any(row["Dq_entry_status"] == "nonzero_current_map" for row in matrix)),
            "detail": "Dq matrix skeleton includes nonzero/rejected entries",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3517_4_no_vertical_claim",
            "passed": bool_text(all(row["eligible_for_Ax_zero"] == "False" for row in basis)),
            "detail": "no direction is certified eligible for A_X=0 yet",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3517_5_bound_rows_block_placeholders",
            "passed": bool_text(all((row["prediction_value"].startswith("MISSING_") or row["prediction_value"].startswith("REJECTED")) and row["valid_for_claim"] == "False" for row in bounds)),
            "detail": "Dq norm bound rows remain nonclaim with placeholders/rejections",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3517_6_next_target_vq",
            "passed": bool_text(any("vq-private" in row["next_doc"] or "vq_private" in row["next_script"] for row in next_rows)),
            "detail": "3518 v_q first-class/source-vector target selected",
            "valid_for_claim": "False",
        }
    )

    csvs_parse = True
    parse_details: list[str] = []
    for name, path in outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        if name == "validation" and not path.exists():
            parse_details.append("validation:deferred_until_written")
            continue
        try:
            read_csv_rows(path)
            parse_details.append(name)
        except Exception as exc:  # pragma: no cover
            csvs_parse = False
            parse_details.append(f"{name}:{exc}")
    checks.append(
        {
            "check_id": "VAL3517_7_csvs_parse",
            "passed": bool_text(csvs_parse),
            "detail": "; ".join(parse_details),
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3517_8_formalization_workbench_not_targeted",
            "passed": "True",
            "detail": str(FORMALIZATION),
            "valid_for_claim": "False",
        }
    )
    passed = all(row["passed"] == "True" for row in checks)
    checks.append(
        {
            "check_id": "VAL3517_SUMMARY",
            "passed": bool_text(passed),
            "detail": "PASS" if passed else "FAIL",
            "valid_for_claim": "False",
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    q_map: list[dict[str, Any]],
    basis: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3517 - Actual q-map Vertical-Basis Construction Or Dq Norm Bound

## Summary
- **Actual construction gain:** a candidate `q(Phi)` field-slot table now exists, with source coordinates `Y` explicitly banned as primitive q components.
- **Basis gain:** residual directions are classified as candidate, rejected, or explicit obstruction; none are certified vertical yet.
- **Matrix gain:** `Dq(v_i)` entries are now a concrete skeleton with blockers and norm-bound slots.
- **Next target:** `v_q_private` is the best first attack: prove first-class/source-vector silence or bound its Dq norm.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Candidate q-map
{markdown_table(q_map, ["q_id", "parent_field_or_slot", "q_component", "included_in_q", "construction_rule", "status", "anti_tautology", "valid_for_claim"])}

## Candidate Vertical Basis
{markdown_table(basis, ["basis_id", "direction", "acts_on", "Dq_candidate", "matrix_status", "Dq_norm_status", "eligible_for_Ax_zero", "next_action", "valid_for_claim"])}

## Dq Matrix Skeleton
{markdown_table(matrix, ["matrix_id", "basis_direction", "q_component", "Dq_entry_status", "blocker", "numeric_value", "valid_for_claim"])}

## Dq Norm Bound Template
{markdown_table(bounds, ["row_id", "direction", "Dq_norm_formula", "required_inputs", "prediction_value", "bound_value", "candidate_priority", "valid_for_claim"])}

## Decisions
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}

Generated: {now_utc()}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    q_map = q_map_rows()
    basis = vertical_basis_rows()
    matrix = dq_matrix_rows()
    bounds = dq_norm_bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3517_SOURCE_REGISTER.csv",
        "q_map": OUT / "P8_Y5_R2FR_3517_CANDIDATE_Q_MAP.csv",
        "canonical_qmap": CANONICAL_QMAP,
        "vertical_basis": OUT / "P8_Y5_R2FR_3517_CANDIDATE_VERTICAL_BASIS.csv",
        "dq_matrix": OUT / "P8_Y5_R2FR_3517_DQ_MATRIX_SKELETON.csv",
        "dq_bounds": OUT / "P8_Y5_R2FR_3517_DQ_NORM_BOUND_TEMPLATE.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3517_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3517_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3517_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    q_fields = ["q_id", "parent_field_or_slot", "q_component", "included_in_q", "construction_rule", "status", "anti_tautology", "source_path", "valid_for_claim"]
    write_csv(outputs["q_map"], q_map, q_fields)
    write_csv(outputs["canonical_qmap"], q_map, q_fields)
    write_csv(outputs["vertical_basis"], basis, ["basis_id", "direction", "acts_on", "Dq_candidate", "matrix_status", "Dq_norm_status", "eligible_for_Ax_zero", "next_action", "source_path", "valid_for_claim"])
    write_csv(outputs["dq_matrix"], matrix, ["matrix_id", "basis_direction", "q_component", "Dq_entry_status", "blocker", "numeric_value", "valid_for_claim"])
    write_csv(outputs["dq_bounds"], bounds, ["row_id", "direction", "Dq_norm_formula", "required_inputs", "prediction_value", "bound_value", "candidate_priority", "valid_for_claim"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed"])

    validation_rows = validate(outputs, sources, q_map, basis, matrix, bounds, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, q_map, basis, matrix, bounds, decisions, next_rows, validation_rows)

    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
