from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_HIDDEN_CURVATURE_VERTEX_BTLINVB_2518"
CHECKPOINT_ID = "2518"
DOC = ROOT / "2518-Y5-R2FR-hidden-curvature-vertex-BTLinvB-zero-or-finite-row.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2518_SOURCE_REGISTER.csv",
    "zero_audit": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2518_HIDDEN_VERTEX_ZERO_AUDIT.csv",
    "schur_components": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2518_SCHUR_TERM_COMPONENTS.csv",
    "finite_inputs": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2518_FINITE_VERTEX_INPUT_ROWS.csv",
    "observable_map": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2518_OBSERVABLE_MAP.csv",
    "dryrun_results": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2518_DRYRUN_RESULTS.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2518_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2518_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2518_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2518_VALIDATION.csv",
}

BRANCH_COPIES = {
    "zero_audit": ROOT
    / "source-intake"
    / "local_bounds"
    / "Hidden_vertex_zero_audit_2518_NONCLAIM.csv",
    "schur_components": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Schur_BTLinvB_components_2518_NONCLAIM.csv",
    "finite_inputs": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2518_HIDDEN_VERTEX_FINITE_INPUTS_NONCLAIM.csv",
    "next_target": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2518_BMEM_QNORM_FINITE_ROW_NEXT_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2518_0_2517_next",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2517_NEXT_TARGET.csv",
        "needles": ["NEXT2517_0_selected", "B^T L^-1 B"],
        "role": "authoritative handoff to hidden curvature vertex gate",
    },
    {
        "source_id": "SRC2518_1_2517_split",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2517_CR2_COMPONENT_SPLIT.csv",
        "needles": ["CR2C2517_1_hidden_vertex", "OPEN_NEXT_AFTER_CBARE"],
        "role": "current c_R2_eff limb being attacked",
    },
    {
        "source_id": "SRC2518_2_1343_law",
        "path": "1343-Y5-R10-RAB-R2FR-parent-coefficient-zero-signature-or-finite-scalar-map-fill.md",
        "needles": ["LAW1343_0_quadratic_parent_block", "B_X X R"],
        "role": "symbolic Schur coefficient law and no-hair correction",
    },
    {
        "source_id": "SRC2518_3_1346_pack",
        "path": "source-intake/mts_residuals/P8_Y5_R10_1346_SYMBOLIC_COEFFICIENT_PACK.csv",
        "needles": ["COEFF1346_M_B", "COEFF1346_H_B"],
        "role": "memory/fibre symbolic coefficient rows",
    },
    {
        "source_id": "SRC2518_4_1347_owner_matrix",
        "path": "source-intake/mts_residuals/P8_Y5_R10_1347_COEFFICIENT_OWNER_MATRIX.csv",
        "needles": ["COWN1347_2_B_mem", "COWN1347_6_Bh"],
        "role": "best owner candidates and current unsigned status",
    },
    {
        "source_id": "SRC2518_5_1348_bmem",
        "path": "1348-Y5-R10-RAB-memory-branch-extremum-and-operator-signature-or-closure.md",
        "needles": ["B_MEM_ZERO_NOT_PARENT_OWNED_CURRENT_CORPUS", "OPERATOR_SIGNATURE_NOT_PARENT_OWNED_CURRENT_CORPUS"],
        "role": "B_mem conditional extremum route fails parent ownership",
    },
    {
        "source_id": "SRC2518_6_1349_closure",
        "path": "1349-Y5-R10-RAB-KMTS-trace-projection-owner-or-memory-closure-declaration.md",
        "needles": ["KMTS_TRACE_PROJECTION_OWNER_NOT_DERIVED", "SYMBOLIC_NONCLAIM_RETAINED"],
        "role": "B_mem zero demoted to private closure; finite residual retained",
    },
    {
        "source_id": "SRC2518_7_1590_coupling",
        "path": "1590-Y5-R2FR-Gamma-Khat-Ploc-owner-bundle-or-cR2-finite-coefficient-row.md",
        "needles": ["COUPLING_AND_RESPONSE_REMAIN_THE_BOTTLENECK", "Q_norm"],
        "role": "newer R2FR owner-bundle summary and Qnorm test lane",
    },
    {
        "source_id": "SRC2518_8_2517_validation",
        "path": "source-intake/mts_residuals/P8_Y5_BRR545_2517_VALIDATION.csv",
        "needles": ["VAL2517_OVERALL", "PASS"],
        "role": "previous checkpoint validation gate",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), "OK"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", "<br>").replace("|", "\\|")
            cells.append(value)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = ROOT / spec["path"]
        text = read_text(path)
        found = [needle for needle in spec["needles"] if needle in text]
        rows.append(
            base_row(
                source_id=spec["source_id"],
                source_path=spec["path"],
                path_exists=path.exists(),
                required_needles=";".join(spec["needles"]),
                found_needles=";".join(found),
                role=spec["role"],
                source_pass=path.exists() and len(found) == len(spec["needles"]),
            )
        )
    return rows


def zero_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "HVZ2518_0_schur_law",
            "claim_attempted": "classify integrated-out hidden curvature vertex contribution",
            "result": "SYMBOLIC_LAW_DERIVED",
            "mathematical_form": "Delta c_R2_hidden(k)=1/2 B^T L^-1(k) B",
            "blocking_gap": "law is exact bookkeeping; zero requires B=0, L^-1=0/decoupled, or sourced identity",
        },
        {
            "audit_id": "HVZ2518_1_J_nohair_repair",
            "claim_attempted": "use ordinary source silence J_X=0 to remove hidden mode",
            "result": "REFUSED_INSUFFICIENT",
            "mathematical_form": "L_X X = B_X R_obs + C_X T + J_X + boundary",
            "blocking_gap": "even with J_X=0, nonzero B_X gives R L^-1 R after elimination",
        },
        {
            "audit_id": "HVZ2518_2_memory_Bmem",
            "claim_attempted": "derive B_mem=0 by branch extremum/F1 route",
            "result": "CONDITIONAL_ROUTE_NOT_PARENT_OWNED",
            "mathematical_form": "partial_m Gamma_eff|m_L=0 if trace projection and branch extremum are parent-owned",
            "blocking_gap": "K_MTS trace projection, R(m;X_B), m_L, Khat/Ward response and boundary locks are not derived",
        },
        {
            "audit_id": "HVZ2518_3_fibre_Bh",
            "claim_attempted": "derive B_h=0 by hidden-visible typing/fibre constraint",
            "result": "UNSIGNED",
            "mathematical_form": "B_h=delta^2 S_parent/(delta h delta R_obs)=0 if fibre is constrained, source-independent, or no hidden-visible coefficient grammar is signed",
            "blocking_gap": "parent fibre potential/gap, matter blindness and hidden-visible coefficient typing remain conditional",
        },
        {
            "audit_id": "HVZ2518_4_decoupling",
            "claim_attempted": "make L^-1 vanish by infinite mass/gap or zero range",
            "result": "UNSIGNED",
            "mathematical_form": "L_X(k)=Z_X k^2+M_X^2; L^-1->0 only with sourced decoupling/infinite gap limit or theorem-zero B_X",
            "blocking_gap": "Z_X, M_X^2, units, branch domain and lower gap are missing for memory and fibre",
        },
        {
            "audit_id": "HVZ2518_5_cross_matrix",
            "claim_attempted": "ignore mode mixing in B^T L^-1 B",
            "result": "REFUSED",
            "mathematical_form": "B^T L^-1 B includes diagonal and cross terms B_A (L^-1)AB B_B",
            "blocking_gap": "no positivity/orthogonality or diagonalization theorem is sourced; no cancellation allowed",
        },
        {
            "audit_id": "HVZ2518_6_verdict",
            "claim_attempted": "zero the hidden Schur limb of c_R2_eff",
            "result": "BTLINVB_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "mathematical_form": "Delta c_R2_hidden is retained unless every B_X or propagator channel is theorem-zero/bounded",
            "blocking_gap": "finite memory/fibre/generic hidden rows are required before R10/PPN/Qnorm scoring",
        },
    ]
    return [base_row(score_ready=False, valid_prediction_row=False, claim_pass=False, **row) for row in rows]


def schur_component_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "component_id": "SCH2518_0_memory_diagonal",
            "symbol": "B_mem^2/(2 L_mem)",
            "meaning": "memory/class scalar diagonal Schur contribution to c_R2_eff",
            "zero_condition": "B_mem=0 from parent-owned trace projection/extremum, or L_mem^-1=0 from sourced decoupling",
            "current_status": "RETAINED_SYMBOLIC",
            "observable_links": "R10;PPN_gamma;Qnorm;clock_orbit",
        },
        {
            "component_id": "SCH2518_1_fibre_diagonal",
            "symbol": "B_h^2/(2 L_h)",
            "meaning": "finite fibre spectrum diagonal Schur contribution to c_R2_eff",
            "zero_condition": "B_h=0 from hidden-visible coefficient theorem or source-independent constrained fibre solution",
            "current_status": "RETAINED_SYMBOLIC",
            "observable_links": "R10;WEP;PPN;source_normalization",
        },
        {
            "component_id": "SCH2518_2_generic_hidden",
            "symbol": "sum_X B_X^2/(2 L_X)",
            "meaning": "other hidden scalar/class/auxiliary curvature-linear channels",
            "zero_condition": "each B_X=0 or each channel is decoupled with a sourced operator inverse",
            "current_status": "RETAINED_SYMBOLIC",
            "observable_links": "R10;PPN;operator_ledger",
        },
        {
            "component_id": "SCH2518_3_cross_terms",
            "symbol": "sum_A!=B B_A (L^-1)AB B_B/2",
            "meaning": "mixed memory-fibre-hidden Schur contribution",
            "zero_condition": "parent diagonalization/orthogonality or component theorem-zero for at least one leg of every cross term",
            "current_status": "RETAINED_SYMBOLIC_NO_CANCELLATION",
            "observable_links": "R10;PPN;Qnorm",
        },
        {
            "component_id": "SCH2518_4_source_charge",
            "symbol": "C_X,J_X,Q_boundary_X",
            "meaning": "not part of pure B^T L^-1 B but required for observable amplitude/body charge",
            "zero_condition": "matter blindness, source silence and boundary no-hair after B_X owner is settled",
            "current_status": "RETAINED_SYMBOLIC",
            "observable_links": "alpha(lambda);WEP;clock;orbit",
        },
        {
            "component_id": "SCH2518_5_total",
            "symbol": "Delta c_R2_hidden",
            "meaning": "full hidden Schur limb entering c_R2_eff",
            "zero_condition": "all diagonal, cross and source/readout routes zeroed or bounded with no cancellation",
            "current_status": "MISSING_ZERO_THEOREM_OR_NUMERIC_BOUND_ROWS",
            "observable_links": "R2FR_scalaron;R10;PPN;local_GR",
        },
    ]
    return [base_row(score_ready=False, valid_prediction_row=False, accepted_for_scoring=False, claim_pass=False, **row) for row in rows]


def finite_input_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "input_id": "HVIN2518_0_Bmem",
            "quantity": "B_mem",
            "required_units": "parent_action_units_for_delta_m_R_vertex",
            "required_value_or_formula": "zero theorem or numeric/symbolic bound with source path",
            "current_status": "MISSING_NO_XR_VERTEX_OR_VALUE",
            "observable_links": "R10;PPN_gamma;Qnorm",
        },
        {
            "input_id": "HVIN2518_1_Zmem_M2mem",
            "quantity": "Z_mem;M2_mem;L_mem^-1",
            "required_units": "kinetic_norm;inverse_length_squared_or_parent_equivalent",
            "required_value_or_formula": "L_mem(k)=Z_mem k^2+M2_mem plus branch domain and positivity/gap",
            "current_status": "MISSING_PARENT_INPUTS",
            "observable_links": "lambda_mem;decoupling;R10",
        },
        {
            "input_id": "HVIN2518_2_Bh",
            "quantity": "B_h",
            "required_units": "parent_action_units_for_delta_h_R_vertex",
            "required_value_or_formula": "zero theorem from hidden-visible grammar or finite coefficient",
            "current_status": "MISSING_NO_FIBRE_CURVATURE_VERTEX_OR_VALUE",
            "observable_links": "R10;WEP;source_normalization",
        },
        {
            "input_id": "HVIN2518_3_Zh_M2h",
            "quantity": "Z_h;M2_h;L_h^-1",
            "required_units": "stiffness_or_kinetic_norm;gap_units",
            "required_value_or_formula": "finite fibre operator inverse or source-independent decoupling theorem",
            "current_status": "MISSING_FIBRE_GAP",
            "observable_links": "lambda_h;R10;WEP",
        },
        {
            "input_id": "HVIN2518_4_cross_matrix",
            "quantity": "L^-1_cross",
            "required_units": "operator_inverse_matrix_units",
            "required_value_or_formula": "diagonalization/orthogonality theorem or finite cross matrix bound",
            "current_status": "MISSING_CROSS_OPERATOR_MAP",
            "observable_links": "Delta_cR2_hidden;Qnorm",
        },
        {
            "input_id": "HVIN2518_5_source_charge",
            "quantity": "C_mem;C_h;J_mem;J_h;Q_boundary_mem;Q_boundary_h",
            "required_units": "source_charge_or_body_response_units",
            "required_value_or_formula": "source/test charge normalization and boundary/body integral map",
            "current_status": "MISSING_SOURCE_BOUNDARY_MAP",
            "observable_links": "alpha(lambda);WEP;clock;orbit",
        },
        {
            "input_id": "HVIN2518_6_scalaron_projection",
            "quantity": "Delta c_R2_hidden -> m_s,lambda_s,alpha_s",
            "required_units": "length^2/eV/meter/dimensionless",
            "required_value_or_formula": "map hidden Schur contribution into scalaron range/amplitude only after coefficient and coupling are sourced",
            "current_status": "FORMULA_READY_INPUTS_MISSING",
            "observable_links": "R10;PPN_gamma",
        },
        {
            "input_id": "HVIN2518_7_beta_map",
            "quantity": "delta_beta_hidden",
            "required_units": "dimensionless",
            "required_value_or_formula": "second-order scalar/source/readout map in fixed observed-GM convention",
            "current_status": "MISSING_SECOND_ORDER_BETA_MAP",
            "observable_links": "PPN_beta_bound_7.8e-05",
        },
        {
            "input_id": "HVIN2518_8_provenance",
            "quantity": "source_file;normalization;assumptions",
            "required_units": "path_or_url_and_convention",
            "required_value_or_formula": "every finite/theorem row cites source path and branch convention",
            "current_status": "REQUIRED_FOR_FUTURE_SCORING",
            "observable_links": "all_future_runners",
        },
    ]
    return [
        base_row(
            score_ready=False,
            valid_prediction_row=False,
            accepted_for_scoring=False,
            claim_pass=False,
            **row,
        )
        for row in rows
    ]


def observable_map_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "map_id": "HVMAP2518_0_cR2",
            "observable_or_target": "Delta c_R2_hidden",
            "map_formula": "1/2 B^T L^-1 B with componentwise no-cancellation policy",
            "required_inputs": "B vector, operator inverse, units, sign convention, source path",
            "status": "SYMBOLIC_ONLY",
        },
        {
            "map_id": "HVMAP2518_1_R10",
            "observable_or_target": "alpha(lambda)",
            "map_formula": "lambda_X=sqrt(Z_X/M_X2); alpha_X from source/test charge and matter frame",
            "required_inputs": "Z_X, M_X2, B_X/C_X, body charge, screening, claim-grade or nonclaim curve label",
            "status": "MISSING_INPUTS",
        },
        {
            "map_id": "HVMAP2518_2_gamma",
            "observable_or_target": "gamma_minus_1",
            "map_formula": "linear Yukawa slip or Qgamma/Qnorm bridge after observed-GM convention is fixed",
            "required_inputs": "alpha/lambda or Qnorm components plus U_min,N_G,N_D",
            "status": "MISSING_INPUTS",
        },
        {
            "map_id": "HVMAP2518_3_beta",
            "observable_or_target": "beta_minus_1",
            "map_formula": "second-order scalar/source/readout transfer; not supplied by linear alpha(lambda) alone",
            "required_inputs": "scalar self-interaction/source normalization/readout map",
            "status": "MISSING_SECOND_ORDER_MAP",
        },
        {
            "map_id": "HVMAP2518_4_WEP_clock_orbit",
            "observable_or_target": "eta_WEP;clock_residual;orbital_residual",
            "map_formula": "source/test charges C_X,J_X,Q_boundary_X project into body, clock and orbital kernels",
            "required_inputs": "body-charge integral, material map, clock/orbit kernel, source path",
            "status": "MISSING_ARENA_PROJECTIONS",
        },
        {
            "map_id": "HVMAP2518_5_local_GR",
            "observable_or_target": "local_GR_operator_claim",
            "map_formula": "local GR cannot be promoted until c_bare, hidden Schur, measure, boundary and frame limbs are zeroed/bounded",
            "required_inputs": "all coefficient limbs and source/readout gates",
            "status": "BLOCKED_NONCLAIM",
        },
    ]
    return [base_row(score_ready=False, valid_prediction_row=False, claim_pass=False, **row) for row in rows]


def dryrun_rows() -> list[dict[str, Any]]:
    cases = [
        {
            "case_id": "DRY2518_0_J_nohair",
            "case_description": "use J_X=0 or exterior Ricci-flatness to remove B^T L^-1 B",
            "result_status": "REFUSED_CURVATURE_VERTEX_REMAINS",
            "blocking_markers": "B_X_R_SOURCE_TERM_MISSING_ZERO_THEOREM",
        },
        {
            "case_id": "DRY2518_1_Bmem_closure",
            "case_description": "use F1=0/B_mem=0 private closure as theorem",
            "result_status": "REFUSED_PRIVATE_CLOSURE_AS_CLAIM",
            "blocking_markers": "KMTS_TRACE_PROJECTION_OWNER_NOT_DERIVED",
        },
        {
            "case_id": "DRY2518_2_infinite_mass",
            "case_description": "assume hidden/fibre modes decouple by infinite mass/gap",
            "result_status": "REJECTED_MISSING_OPERATOR_GAP",
            "blocking_markers": "MISSING_Z_X;MISSING_M_X2;MISSING_UNITS",
        },
        {
            "case_id": "DRY2518_3_symbolic_score",
            "case_description": "score R10/PPN from symbolic B_mem/B_h rows",
            "result_status": "REJECTED_SYMBOLIC_ONLY_INPUTS",
            "blocking_markers": "MISSING_NUMERIC_VALUES;MISSING_SOURCE_PATHS;MISSING_OBSERVABLE_MAPS",
        },
        {
            "case_id": "DRY2518_4_cancellation",
            "case_description": "cancel memory/fibre/cross Schur terms by sign choice",
            "result_status": "REFUSED_UNSOURCED_CANCELLATION",
            "blocking_markers": "NO_CANCELLATION_GATE_ACTIVE",
        },
        {
            "case_id": "DRY2518_5_future_complete_template",
            "case_description": "future hidden vertex row has real B/L or theorem-zero, units, maps and source paths",
            "result_status": "WOULD_ACCEPT_SCHEMA_IF_REAL_VALUES_AND_FILES_EXIST",
            "blocking_markers": "CURRENT_ROW_STILL_MISSING_REAL_INPUTS",
        },
    ]
    return [
        base_row(
            predicted_value="NOT_COMPUTED",
            pass_fail="BLOCKED_NONCLAIM",
            score_ready=False,
            valid_prediction_row=False,
            claim_pass=False,
            **case,
        )
        for case in cases
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        {
            "decision_id": "DEC2518_0_law",
            "decision": "BTLINVB_SCHUR_LAW_LOCKED",
            "rationale": "Integrating out hidden curvature-linear modes generates 1/2 B^T L^-1 B, so ordinary source silence is insufficient.",
            "status": "retained_derivation",
        },
        {
            "decision_id": "DEC2518_1_zero",
            "decision": "HIDDEN_VERTEX_ZERO_NOT_DERIVED",
            "rationale": "B_mem is private closure only without K_MTS owner, and B_h lacks hidden-visible grammar or fibre constraint proof.",
            "status": "claim_blocked",
        },
        {
            "decision_id": "DEC2518_2_finite",
            "decision": "FINITE_VERTEX_ROWS_STAGED_NONCLAIM",
            "rationale": "Memory/fibre/generic hidden rows now list B, Z, M2, source charge, range, beta/gamma/R10 and provenance requirements.",
            "status": "selected_nonclaim",
        },
        {
            "decision_id": "DEC2518_3_next",
            "decision": "MOVE_TO_BMEM_QNORM_FIRST_FILL",
            "rationale": "The old derivation route already says K_MTS owner is missing; the practical next move is a strict finite B_mem/Qnorm row unless a new owner source appears.",
            "status": "selected",
        },
        {
            "decision_id": "DEC2518_4_claim",
            "decision": "NO_HIDDEN_VERTEX_R2FR_OR_LOCAL_GR_CLAIM",
            "rationale": "No hidden vertex zero theorem or finite numeric row is score-ready.",
            "status": "enforced",
        },
    ]
    return [base_row(**decision) for decision in decisions]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2518_0_selected",
            selection_status="selected",
            target_file="2519-Y5-R2FR-Bmem-Qnorm-first-finite-row-or-new-KMTS-owner-reentry.md",
            target_script="scripts/Y5_R2FR_Bmem_Qnorm_first_finite_row_or_new_KMTS_owner_reentry_2519.py",
            objective="create the first strict finite B_mem/Qnorm nonclaim row with units, source paths and R10/PPN/Qnorm links, while allowing K_MTS-owner derivation reentry only if a genuinely new source appears",
            success_condition="B_mem row is either parent-zeroed by new K_MTS evidence or remains finite with declared units, missing-value blockers, source path requirements, and rejected symbolic scoring",
            do_not_do="do not re-use B_mem=0 private closure as theorem; do not score symbolic B_mem; do not rerun old K_MTS owner proof without new evidence",
        ),
        base_row(
            route_id="NEXT2518_1_fibre_queue",
            selection_status="queued_after_memory",
            target_file="2520-Y5-R2FR-fibre-Bh-finite-row-or-hidden-visible-grammar-reentry.md",
            target_script="scripts/Y5_R2FR_fibre_Bh_finite_row_or_hidden_visible_grammar_reentry_2520.py",
            objective="after memory Bmem, classify fibre B_h with hidden-visible grammar reentry or finite fibre coefficient rows",
            success_condition="B_h has theorem-zero evidence or finite nonclaim Z_h/M2_h/B_h/C_h/source-charge rows",
            do_not_do="do not let memory closure erase fibre residuals",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("zero_audit", OUTPUTS["zero_audit"], BRANCH_COPIES["zero_audit"]),
        ("schur_components", OUTPUTS["schur_components"], BRANCH_COPIES["schur_components"]),
        ("finite_inputs", OUTPUTS["finite_inputs"], BRANCH_COPIES["finite_inputs"]),
        ("next_target", OUTPUTS["next_target"], BRANCH_COPIES["next_target"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        ok, count, message = csv_rows_parse(destination)
        rows.append(
            base_row(
                copy_id=copy_id,
                source=str(source.relative_to(ROOT)),
                destination=str(destination.relative_to(ROOT)),
                copied=destination.exists(),
                parse_ok=ok,
                row_count=count,
                parse_message=message,
            )
        )
    return rows


def falsey(value: Any) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "not_computed", ""}


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name in {"source_register", "validation"}:
            continue
        for row in rows:
            for key in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "valid_prediction_row",
                "accepted_for_scoring",
                "claim_pass",
            ):
                if key in row and not falsey(row[key]):
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, detail: str = "") -> None:
        checks.append(
            base_row(
                check_id=check_id,
                status="PASS" if status else "FAIL",
                detail=detail,
                valid_for_claim=False,
                claim_allowed=False,
            )
        )

    source_rows = rows_by_name["source_register"]
    add("VAL2518_00_sources_exist", all(str(row["path_exists"]) == "True" for row in source_rows))
    add("VAL2518_01_source_needles", all(str(row["source_pass"]) == "True" for row in source_rows))
    add(
        "VAL2518_02_schur_law_present",
        any(row["audit_id"] == "HVZ2518_0_schur_law" and row["result"] == "SYMBOLIC_LAW_DERIVED" for row in rows_by_name["zero_audit"]),
        "Schur law B^T L^-1 B is recorded",
    )
    add(
        "VAL2518_03_zero_not_promoted",
        any(row["audit_id"] == "HVZ2518_6_verdict" and row["result"] == "BTLINVB_ZERO_NOT_DERIVED_CURRENT_CORPUS" for row in rows_by_name["zero_audit"]),
        "hidden vertex zero is not promoted",
    )
    add(
        "VAL2518_04_components_complete",
        len(rows_by_name["schur_components"]) == 6
        and any(row["component_id"] == "SCH2518_0_memory_diagonal" for row in rows_by_name["schur_components"])
        and any(row["component_id"] == "SCH2518_1_fibre_diagonal" for row in rows_by_name["schur_components"]),
        "memory and fibre Schur components present",
    )
    add(
        "VAL2518_05_finite_rows_rejected",
        len(rows_by_name["finite_inputs"]) == 9
        and all(str(row["accepted_for_scoring"]) == "False" for row in rows_by_name["finite_inputs"]),
        "finite vertex rows are schema-only",
    )
    add(
        "VAL2518_06_observable_maps_present",
        all(
            any(row["observable_or_target"] == target for row in rows_by_name["observable_map"])
            for target in ["Delta c_R2_hidden", "alpha(lambda)", "gamma_minus_1", "beta_minus_1"]
        ),
        "R10/PPN maps are staged but blocked",
    )
    add(
        "VAL2518_07_dryruns_block_claims",
        all(str(row["pass_fail"]) == "BLOCKED_NONCLAIM" and str(row["claim_pass"]) == "False" for row in rows_by_name["dryrun_results"]),
        "dry run rejects J-nohair, closure, decoupling and cancellation shortcuts",
    )
    add(
        "VAL2518_08_next_target",
        any(row["route_id"] == "NEXT2518_0_selected" and "Bmem-Qnorm" in row["target_file"] for row in rows_by_name["next_target"]),
        "Bmem/Qnorm finite row selected next",
    )
    add("VAL2518_09_no_claim_flags", no_claim_flags(rows_by_name))
    add(
        "VAL2518_10_branch_copies",
        all(str(row["copied"]) == "True" and str(row["parse_ok"]) == "True" for row in rows_by_name["branch_copies"]),
    )
    formalization = ROOT.parent / "formalization-workbench"
    formalization_hits = list(formalization.rglob("*2518*")) if formalization.exists() else []
    add(
        "VAL2518_11_no_formalization_artifacts",
        len(formalization_hits) == 0,
        ";".join(str(path) for path in formalization_hits),
    )
    add("VAL2518_12_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists())

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2518_CSV_{path.stem}", ok, f"{message}; rows={count}")
    for key, path in BRANCH_COPIES.items():
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2518_COPY_CSV_{key}", ok, f"{message}; rows={count}")

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        base_row(
            check_id="VAL2518_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2518 locks the B^T L^-1 B Schur law, refuses hidden-vertex zero promotion, stages finite memory/fibre rows, and selects Bmem/Qnorm first-fill next",
            valid_for_claim=False,
            claim_allowed=False,
        )
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2518 - Hidden Curvature Vertex BTLinvB Zero or Finite Row",
                "",
                "**Current verdict:** the hidden Schur limb is real and dangerous: an eliminated hidden/memory/fibre mode with curvature-linear vertex `B_X X R` generates `1/2 B^T L^-1 B`. Current MTS does not theorem-zero this limb.",
                "",
                "**Main gain:** the old shortcut is blocked. `J_X=0`, exterior Ricci-flatness, or a positive operator does not remove the Schur term unless `B_X`, the operator inverse, source charges, and boundary terms are also owned.",
                "",
                "**Claim discipline:** no hidden-vertex, R2/f(R), scalaron, beta, gamma, R10, EH, Newton, local-GR, WEP, clock, orbit, or conservation claim is made.",
                "",
                "## Source Register",
                md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "found_needles", "source_pass", "role"]),
                "",
                "## Hidden Vertex Zero Audit",
                md_table(rows_by_name["zero_audit"], ["audit_id", "claim_attempted", "result", "mathematical_form", "blocking_gap"]),
                "",
                "## Schur Term Components",
                md_table(rows_by_name["schur_components"], ["component_id", "symbol", "meaning", "zero_condition", "current_status", "observable_links"]),
                "",
                "## Finite Vertex Input Rows",
                md_table(rows_by_name["finite_inputs"], ["input_id", "quantity", "required_units", "required_value_or_formula", "current_status", "observable_links"]),
                "",
                "## Observable Map",
                md_table(rows_by_name["observable_map"], ["map_id", "observable_or_target", "map_formula", "required_inputs", "status"]),
                "",
                "## Dry Run",
                md_table(rows_by_name["dryrun_results"], ["case_id", "case_description", "result_status", "blocking_markers", "pass_fail"]),
                "",
                "## Decision Ledger",
                md_table(rows_by_name["decision_ledger"], ["decision_id", "decision", "rationale", "status"]),
                "",
                "## Next Target",
                md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"]),
                "",
                "## Validation",
                md_table(rows_by_name["validation"], ["check_id", "status", "detail"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "zero_audit": zero_audit_rows(),
        "schur_components": schur_component_rows(),
        "finite_inputs": finite_input_rows(),
        "observable_map": observable_map_rows(),
        "dryrun_results": dryrun_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
