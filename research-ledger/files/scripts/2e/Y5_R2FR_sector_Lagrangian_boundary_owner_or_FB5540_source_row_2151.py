from __future__ import annotations

from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2151-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2150": ROOT / "2150-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-row.md",
    "1841": ROOT / "1841-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md",
    "1842": ROOT / "1842-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
    "1843": ROOT / "1843-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md",
    "1841_operator": OUT / "P8_Y5_PARENT_QLOC_1841_OPERATOR_BOUND_INPUT_PACK.csv",
    "1842_validation": OUT / "P8_Y5_BRR545_1842_VALIDATION.csv",
    "1843_validation": OUT / "P8_Y5_BRR545_1843_VALIDATION.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2151_SOURCE_REGISTER.csv",
    "owner_clauses": OUT / "P8_Y5_PARENT_QLOC_2151_OWNER_CLAUSES.csv",
    "route_tests": OUT / "P8_Y5_PARENT_QLOC_2151_ROUTE_TESTS.csv",
    "source_schema": OUT / "P8_Y5_PARENT_QLOC_2151_FB5540_SOURCE_ROW_SCHEMA.csv",
    "source_runner": OUT / "P8_Y5_PARENT_QLOC_2151_FB5540_SOURCE_ROW_RUNNER.csv",
    "gr_bridge": OUT / "P8_Y5_PARENT_QLOC_2151_GR_BRIDGE_STATUS.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2151_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2151_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2151_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2151_VALIDATION.csv",
}


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def has_any(text: str, alternatives: list[str]) -> bool:
    return any(item in text for item in alternatives)


def find_line(path: Path, alternatives: list[str]) -> tuple[int, str]:
    text = read_text(path) if path.exists() else ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        if has_any(line, alternatives):
            return line_number, line.strip()
    return 0, "MISSING_NEEDLE"


def formalization_has_2151_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2151-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2151*",
        "*P8_Y5_BRR545_2151*",
        "*Y5_R2FR_sector_Lagrangian_boundary_owner_or_FB5540_source_row_2151*",
        "*AFRAME_SOURCE_OWNER_FB5540_2151*",
        "*JR2151*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2151_00_2150_handoff",
            DOCS["2150"],
            [["NEXT2150_0_2151"], ["SECTOR_LAGRANGIAN_BOUNDARY_OWNER_NEXT"], ["L_X, Theta_X, Q_X"]],
            "current branch handoff selects sector/source-charge ownership.",
        ),
        (
            "SRC2151_01_1841_source_root",
            DOCS["1841"],
            [["OBI1841_6_source_normalization"], ["MISSING_MHREF_AND_FB5540_COMPONENTS"], ["sector Lagrangian/boundary owner"]],
            "old R2FR source-normalization root identifies M_H_ref and numerator components.",
        ),
        (
            "SRC2151_02_1841_operator_csv",
            DOCS["1841_operator"],
            [["OBI1841_6_source_normalization"], ["MISSING_MHREF_AND_FB5540_COMPONENTS"]],
            "machine-readable old source-normalization row.",
        ),
        (
            "SRC2151_03_1842_owner_map",
            DOCS["1842"],
            [["LOC1842_0_LX_owner"], ["LOC1842_7_MHref_owner"], ["VAL1842_OVERALL"]],
            "old 1842 owner map gives the current 2151 clause set.",
        ),
        (
            "SRC2151_04_1842_validation",
            DOCS["1842_validation"],
            [["VAL1842_OVERALL"], ["PASS"]],
            "old 1842 nonclaim validation.",
        ),
        (
            "SRC2151_05_1843_boundary_route",
            DOCS["1843"],
            [["ETB1843_5_verdict"], ["BX_PRIMITIVE_FROM_PARENT_VARIATION_OR_EDGE_BOUND_TERM_FILL_IS_NEXT"], ["VAL1843_OVERALL"]],
            "old 1843 boundary/projector continuation proves the next live edge object.",
        ),
        (
            "SRC2151_06_1843_validation",
            DOCS["1843_validation"],
            [["VAL1843_OVERALL"], ["PASS"]],
            "old 1843 nonclaim validation.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                needles_found=needles_found,
                expected_needles="; ".join(" OR ".join(group) for group in needle_groups),
                role=role,
            )
        )
    return rows


def owner_clause_rows() -> list[dict[str, object]]:
    data = [
        (
            "SOC2151_0_LX_owner",
            "parent-owned extra-sector Lagrangian",
            "L_X[g,X,nabla X] with explicit kinetic operator, source term, normalization and admissible boundary class",
            "NOT_SIGNED",
            "Theta_X,Q_X,omega_X,C_X,R10/R11 and local scaling cannot be computed as derivations.",
            "delta_H_tau_nonintegrable_over_MH;C_extra;R10;R11",
        ),
        (
            "SOC2151_1_Theta_QX_owner",
            "sector symplectic potential and Hamiltonian charge",
            "delta L_X=E_X delta X+dTheta_X; J_tau^X=Theta_X(L_tau X)-i_tau L_X=dQ_tau^X+C_tau^X",
            "FORMULA_WRITTEN_NOT_PARENT_OWNED",
            "Hamiltonian integrability and boundary charge remain schematic rather than owned.",
            "delta_H_tau_nonintegrable_over_MH;symplectic_boundary_flux_over_MH",
        ),
        (
            "SOC2151_2_source_current_owner",
            "source coupling/source current owner",
            "J_X = -delta L_matter/delta X or J_X=0 from quotient verticality, with units and sign fixed before readout",
            "MISSING_SOURCE_CURRENT_RULE",
            "X can couple to matter or source normalization by hidden convention.",
            "K_X;qbar_XT;Qbar_XH;alpha_X",
        ),
        (
            "SOC2151_3_boundary_reference_owner",
            "boundary and reference class owner",
            "B_ref[gamma_ref,tau_ref,C_top] and B_class[chi_B,C_top] fixed before source variation and readout",
            "NOT_SIGNED",
            "reference subtraction or boundary class can absorb or reroute source calibration.",
            "Delta_ref_over_MH;Delta_symp_over_MH;Qbar_edge_XH",
        ),
        (
            "SOC2151_4_tau_owner",
            "same generator for source, charge, clocks and readout",
            "tau_source=tau_charge=tau_clock=tau_readout up to a sourced mismatch bound",
            "NOT_SIGNED",
            "Hamiltonian source charge, clocks and PPN readout can drift apart.",
            "tau_lock_mismatch;clock;PPN;M_H_ref",
        ),
        (
            "SOC2151_5_MHref_owner",
            "same-frame Hamiltonian/Hilbert denominator",
            "M_H_ref=H_tau[S_outer]-H_ref=int_S Q_tau-H_ref, positive and fixed before orbital readout",
            "MISSING_STABLE_MH_REF",
            "R_eq, FB5540 and source-normalization rows remain unnormalized.",
            "FB5540;R_eq;I_commutator;Newton;local_GR",
        ),
        (
            "SOC2151_6_FB5540_numerator_pack",
            "complete FB5540 numerator pack",
            "|delta_H_tau_nonintegrable|+|Delta_ref|+|Delta_symp|+|boundary_flux|+|bulk_X|+|edge_X| with no-cancellation guard",
            "MISSING_NUMERATOR_COMPONENTS",
            "unknown pieces could be accidentally hidden in measured GM or assumed cancellations.",
            "FB5540;R10;R11;PPN",
        ),
        (
            "SOC2151_7_verdict",
            "full source-owner gate",
            "SOC2151_0 through SOC2151_6 signed by one parent action/boundary/readout grammar",
            "FAIL_CURRENT_CLAIM",
            "current MTS has a sharp owner contract but not a closed source-coupling derivation.",
            "Newton;local_GR;R10;R11",
        ),
    ]
    return [
        row(
            owner_id=owner_id,
            required_owner=required_owner,
            mathematical_form=mathematical_form,
            current_status=current_status,
            failure_if_missing=failure_if_missing,
            feeds=feeds,
        )
        for owner_id, required_owner, mathematical_form, current_status, failure_if_missing, feeds in data
    ]


def route_test_rows() -> list[dict[str, object]]:
    data = [
        (
            "RT2151_0_direct_parent_owner",
            "derive full L_X/Theta_X/Q_X/B/tau/M_H_ref owner",
            "one parent action supplies sector equations, symplectic potential, charges, boundary class, reference and tau before readout",
            "BEST_BUT_UNSIGNED",
            "no current parent document signs all clauses together",
            "move to boundary/projector theorem route or source pack",
        ),
        (
            "RT2151_1_vertical_no_pole",
            "X is vertical/constraint and carries no physical pole",
            "Dq[v_X]=0 and delta G_X=Omega(delta Phi,v_X) is differentiable with zero boundary charge",
            "BEST_ZERO_ROUTE_NOT_SIGNED",
            "Omega/DC_X plus differentiable zero boundary charge are not parent-signed",
            "retain edge and bulk residual rows",
        ),
        (
            "RT2151_2_positive_sourcefree",
            "positive source-free operator kills local X profile",
            "int_A(Z_X|grad X|^2+M_X^2 X^2)=int_A XJ_X+boundary_flux_X with Z_X>0,M_X^2>0,J_X=0,boundary_flux_X=0",
            "CONDITIONAL_THEOREM_ONLY",
            "Z_X,M_X^2,J_X=0 and boundary_flux_X=0 are not all signed",
            "retain alpha/lambda residual vector",
        ),
        (
            "RT2151_3_massive_sourced_residual",
            "finite physical X residual",
            "lambda_X=sqrt(Z_X/M_X^2), alpha_X=K_X Qbar_XH qbar_XT",
            "SCHEMA_READY_NO_VALUES",
            "all coefficients, units and source paths are missing/nonclaim",
            "R10/R11 source acquisition required",
        ),
        (
            "RT2151_4_boundary_projector_route",
            "edge/source leakage theorem route",
            "Q_edge=0 from exact boundary primitive or Qbar_edge_XH=0 from source-mass projector orthogonality",
            "NEXT_DERIVATION_ROUTE",
            "B_X primitive, cohomology/kernel and Pi_M^H/M_H_ref owner remain unsigned",
            "2152 boundary exactness/projector/source-pack checkpoint",
        ),
        (
            "RT2151_5_verdict",
            "source-owner gate closed",
            "one theorem-zero route closes or a complete no-cancellation source pack exists",
            "FAIL_CURRENT_CLAIM",
            "no route yet signs enough clauses or supplies source-backed values",
            "continue derivation-first with boundary/projector route",
        ),
    ]
    return [
        row(
            route_id=route_id,
            route=route_name,
            mathematical_form=mathematical_form,
            current_status=current_status,
            blocker=blocker,
            fallback=fallback,
        )
        for route_id, route_name, mathematical_form, current_status, blocker, fallback in data
    ]


def source_schema_rows() -> list[dict[str, object]]:
    data = [
        (
            "FSR2151_0_M_H_ref",
            "M_H_ref",
            "same-frame Hamiltonian source denominator",
            "system_id;surface;tau_id;Q_tau_integral;H_ref;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "MISSING_STABLE_MH_REF",
        ),
        (
            "FSR2151_1_delta_H_tau",
            "delta_H_tau_nonintegrable_over_MH",
            "field-space curl/nonintegrability of Hamiltonian variation normalized by M_H_ref",
            "system_id;surface_pair;omega_X_integral;reference_curl;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO",
        ),
        (
            "FSR2151_2_Delta_ref",
            "Delta_ref_over_MH",
            "reference shift/derivative profile normalized by M_H_ref",
            "system_id;reference_branch;Delta_ref;derivative_profile;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO",
        ),
        (
            "FSR2151_3_boundary_flux",
            "symplectic_boundary_flux_over_MH;B_zero_flux;Delta_symp",
            "boundary/projector/non-EH linked flux normalized by M_H_ref",
            "system_id;surface_pair;symplectic_boundary_flux;B_zero_flux;Delta_symp;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "MISSING_SYMPLECTIC_BOUNDARY_NUMERIC_OR_THEOREM_ZERO",
        ),
        (
            "FSR2151_4_LX_bulk_coefficients",
            "Z_X;M_X2;J_X;lambda_X",
            "bulk X-sector coefficients if no theorem-zero route closes",
            "system_id;field_id;Z_X;M_X2;J_X;lambda_X;units;source_path;assumptions;valid_for_claim",
            "MISSING_PARENT_INPUT",
        ),
        (
            "FSR2151_5_R10_source_projection",
            "K_X;Qbar_XH;qbar_XT",
            "R10 residual amplitude factors for active X exchange",
            "system_id;K_X;Qbar_XH;qbar_XT;normalization;units;source_path;assumptions;valid_for_claim",
            "MISSING_ARENA_PROJECTION",
        ),
        (
            "FSR2151_6_edge_projection",
            "lambda_edge;K_edge;Qbar_edge_XH;qbar_XT",
            "edge/boundary residual amplitude factors if boundary theorem fails",
            "system_id;lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;units;source_path;assumptions;valid_for_claim",
            "MISSING_EDGE_COEFFICIENTS",
        ),
        (
            "FSR2151_7_total_guard",
            "FB5540_alpha_R11_total_guard",
            "absolute no-cancellation envelope across FB5540, bulk X, edge X and R11 coefficients",
            "system_id;component_sum_abs;M_H_ref;normalization;source_path;assumptions;valid_for_claim",
            "NOT_COMPUTED_COMPONENTS_MISSING",
        ),
    ]
    return [
        row(row_id=row_id, quantity=quantity, definition=definition, required_columns=required_columns, current_status=current_status)
        for row_id, quantity, definition, required_columns, current_status in data
    ]


def source_runner_rows(schema: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for item in schema:
        status = "BLOCKED_MISSING_INPUTS"
        reasons = ["MISSING_THEOREM_OR_SOURCE_INPUT", "VALID_FOR_CLAIM_FALSE"]
        if "M_H_ref" in str(item["quantity"]):
            reasons.append("MISSING_STABLE_DENOMINATOR")
        if "Qbar" in str(item["quantity"]) or "K_X" in str(item["quantity"]):
            reasons.append("MISSING_ARENA_PROJECTION")
        rows.append(
            row(
                runner_id=str(item["row_id"]).replace("FSR", "FRR"),
                row_id=item["row_id"],
                quantity=item["quantity"],
                computed_status=status,
                failure_reasons=";".join(reasons),
            )
        )
    return rows


def gr_bridge_rows() -> list[dict[str, object]]:
    data = [
        (
            "GB2151_0_owner_contract",
            "source-owner contract",
            "WRITTEN_EXPLICITLY",
            "SOC2151 rows",
            "all clauses still parent-unsigned",
        ),
        (
            "GB2151_1_source_denominator",
            "Hamiltonian source denominator",
            "BLOCKED_MISSING_MHREF",
            "FSR2151_0",
            "same-frame M_H_ref must be derived or source-backed",
        ),
        (
            "GB2151_2_FB5540_pack",
            "FB5540/source-normalization pack",
            "SCHEMA_READY_NO_VALUES",
            "FSR2151 rows",
            "numerator components and no-cancellation guard missing",
        ),
        (
            "GB2151_3_boundary_projector",
            "boundary exactness/projector orthogonality route",
            "PRIMARY_NEXT_DERIVATION_ROUTE",
            "1843 old frontier",
            "B_X primitive, cohomology/kernel and Pi_M^H owner",
        ),
        (
            "GB2151_4_Newton_GR",
            "Newton/local-GR route",
            "BLOCKED",
            "SOC2151_7;RT2151_5",
            "local GR cannot reopen until source-owner or source-pack route closes",
        ),
    ]
    return [
        row(status_id=status_id, bridge_piece=bridge_piece, current_status=current_status, evidence=evidence, remaining_gap=remaining_gap)
        for status_id, bridge_piece, current_status, evidence, remaining_gap in data
    ]


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2151_0_owner_result",
            "OWNER_MAP_SHARP_BUT_NOT_CLOSED",
            "L_X/Theta_X/Q_X, source current, boundary/reference, tau and M_H_ref are explicit but unsigned",
            "do not promote FB5540, R10/R11, Newton or local GR",
        ),
        (
            "DEC2151_1_best_zero_route",
            "BOUNDARY_PROJECTOR_ROUTE_IS_BEST_NEXT",
            "a structural boundary/projector zero would remove edge/source leakage without tuning coefficients",
            "derive boundary exactness/projector orthogonality before coefficient scoring",
        ),
        (
            "DEC2151_2_source_row_fallback",
            "FULL_NO_CANCELLATION_SOURCE_ROW_REQUIRED_IF_THEOREM_FAILS",
            "unknown FB5540, bulk, edge and R11 terms cannot cancel or borrow orbital GM as denominator",
            "source M_H_ref and every numerator factor together or keep blocked",
        ),
        (
            "DEC2151_3_next",
            "BOUNDARY_EXACTNESS_PROJECTOR_ORTHOGONALITY_OR_SOURCE_PACK_NEXT",
            "old 1843 shows this is the first structural route after the source-owner map",
            "2152 boundary exactness/projector/source-pack checkpoint",
        ),
        (
            "DEC2151_4_claim_policy",
            "NO_LOCAL_GR_NEWTON_CLAIM",
            "source ownership, EH dominance, PPN and empirical residual maps remain nonclaim",
            "continue private derivation/test discipline",
        ),
    ]
    return [row(decision_id=decision_id, decision=decision, reason=reason, next_action=next_action) for decision_id, decision, reason, next_action in data]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2151_0_2152",
            next_target="2152-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md",
            script="scripts/Y5_R2FR_boundary_exactness_projector_orthogonality_or_source_pack_2152.py",
            objective="Derive Q_edge=0 from a certified boundary primitive or Qbar_edge_XH=0 from source-mass projector orthogonality; if either fails, stage the complete weighted-Stokes/source-pack rows nonclaim.",
            forbidden_shortcuts="do not set Q_edge=0 by Stokes without domain/cohomology/kernel certificates; do not set Qbar_edge_XH=0 without Pi_M^H and M_H_ref ownership; do not claim Newton/local GR; no formalization-workbench edits; no GitHub action",
        )
    ]


def write_branch_copies(owner: list[dict[str, object]], bridge: list[dict[str, object]], decisions: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2151_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_SOURCE_OWNER_FB5540_2151_NONCLAIM.csv", owner + bridge + decisions),
        ("COPY2151_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2151_SOURCE_OWNER_NONCLAIM.csv", owner + bridge),
        ("COPY2151_2_acquisition_queue", QUEUE / "JR2151_BOUNDARY_PROJECTOR_SOURCE_PACK_QUEUE.csv", next_rows + bridge),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    owner: list[dict[str, object]],
    routes: list[dict[str, object]],
    schema: list[dict[str, object]],
    runner: list[dict[str, object]],
    bridge: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    owner_ok = {"SOC2151_0_LX_owner", "SOC2151_1_Theta_QX_owner", "SOC2151_5_MHref_owner", "SOC2151_7_verdict"}.issubset({str(item["owner_id"]) for item in owner}) and any(item["owner_id"] == "SOC2151_7_verdict" and item["current_status"] == "FAIL_CURRENT_CLAIM" for item in owner)
    routes_ok = {"RT2151_1_vertical_no_pole", "RT2151_2_positive_sourcefree", "RT2151_3_massive_sourced_residual", "RT2151_4_boundary_projector_route", "RT2151_5_verdict"}.issubset({str(item["route_id"]) for item in routes})
    schema_ok = {"FSR2151_0_M_H_ref", "FSR2151_4_LX_bulk_coefficients", "FSR2151_6_edge_projection", "FSR2151_7_total_guard"}.issubset({str(item["row_id"]) for item in schema})
    schema_nonclaim = all(not truthy(item.get("valid_for_claim", False)) for item in schema) and all(not truthy(item.get("claim_allowed", False)) for item in runner)
    missing_not_ready = all(not truthy(item.get("valid_for_claim", False)) for item in schema if "MISSING_" in " ".join(str(value) for value in item.values()))
    bridge_ok = any(item["status_id"] == "GB2151_3_boundary_projector" and item["current_status"] == "PRIMARY_NEXT_DERIVATION_ROUTE" for item in bridge) and any(item["status_id"] == "GB2151_4_Newton_GR" and item["current_status"] == "BLOCKED" for item in bridge)
    decisions_ok = any(item["decision"] == "BOUNDARY_PROJECTOR_ROUTE_IS_BEST_NEXT" for item in decisions) and any(item["decision"] == "NO_LOCAL_GR_NEWTON_CLAIM" for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2151_0_2152" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, owner, routes, schema, runner, bridge, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2151_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, owner_ok, routes_ok, schema_ok, schema_nonclaim, missing_not_ready, bridge_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2151_00_sources", sources_ok, "2150 handoff plus old 1841-1843 source-owner frontier validate"),
        ("VAL2151_01_owner_map", owner_ok, "source-owner map covers L_X, Theta/Q, M_H_ref and fail verdict"),
        ("VAL2151_02_route_split", routes_ok, "route split covers zero routes, finite source fallback and boundary/projector next"),
        ("VAL2151_03_source_schema", schema_ok, "FB5540/source schema covers denominator, bulk, edge and total guard"),
        ("VAL2151_04_source_schema_nonclaim", schema_nonclaim, "source schema and runner stay nonclaim"),
        ("VAL2151_05_missing_not_ready", missing_not_ready, "no MISSING_* row is marked ready"),
        ("VAL2151_06_bridge", bridge_ok, "GR bridge remains blocked and selects boundary/projector route"),
        ("VAL2151_07_decisions", decisions_ok, "decisions block local claims and select theorem-first route"),
        ("VAL2151_08_next", next_ok, "next target is 2152 boundary exactness/projector/source pack"),
        ("VAL2151_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2151_10_csv_parse", csv_ok, "all generated 2151 CSVs parse cleanly"),
        ("VAL2151_11_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2151_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2151"),
        ("VAL2151_13_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2151_OVERALL", all_ok, "2151 writes the source-owner/FB5540 gate and keeps Newton/local-GR claims blocked."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    owner: list[dict[str, object]],
    routes: list[dict[str, object]],
    schema: list[dict[str, object]],
    runner: list[dict[str, object]],
    bridge: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    line_1842, _ = find_line(DOCS["1842"], ["Current verdict"])
    line_1843, _ = find_line(DOCS["1843"], ["ETB1843_5_verdict"])
    content = "\n\n".join(
        [
            "# 2151 - Y5/R2FR Sector Lagrangian Boundary Owner Or FB5540 Source Row",
            "## Current Verdict",
            "2151 does **not** prove `L_X`, `Theta_X`, `Q_X`, `M_H_ref`, `FB5540=0`, Newton, local GR, PPN, R10/R11, or any public claim. It makes the coupling/source-owner gate explicit in the current 21xx branch.",
            "The useful gain is sharper than another closure loop: the missing object is not just an extra field. It is the parent-owned source coupling plus the same-frame Hamiltonian source denominator. Without that, measured `GM` can accidentally hide residual sector terms.",
            f"This syncs the current handoff to old 1842 line {line_1842} and old 1843 line {line_1843}: source ownership is still unsigned, and the best theorem-first continuation is boundary exactness/projector orthogonality rather than coefficient fitting.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Owner Clauses",
            md_table(owner, ["owner_id", "required_owner", "mathematical_form", "current_status", "failure_if_missing", "feeds", "valid_for_claim"]),
            "## Route Tests",
            md_table(routes, ["route_id", "route", "mathematical_form", "current_status", "blocker", "fallback", "valid_for_claim"]),
            "## FB5540 Source Row Schema",
            md_table(schema, ["row_id", "quantity", "definition", "required_columns", "current_status", "valid_for_claim"]),
            "## FB5540 Source Row Runner",
            md_table(runner, ["runner_id", "row_id", "quantity", "computed_status", "claim_allowed", "failure_reasons"]),
            "## GR Bridge Status",
            md_table(bridge, ["status_id", "bridge_piece", "current_status", "evidence", "remaining_gap", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
            "## Working Interpretation",
            "This is progress, but it is still a hard gate. The local-GR bridge now needs either a true source-owner derivation or a complete nonclaim source pack. The cleanest next shot is the boundary/projector route, because it could kill edge/source leakage structurally instead of asking a small coefficient to save the theory.",
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    owner = owner_clause_rows()
    routes = route_test_rows()
    schema = source_schema_rows()
    runner = source_runner_rows(schema)
    bridge = gr_bridge_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["owner_clauses"], owner)
    write_csv(OUTPUTS["route_tests"], routes)
    write_csv(OUTPUTS["source_schema"], schema)
    write_csv(OUTPUTS["source_runner"], runner)
    write_csv(OUTPUTS["gr_bridge"], bridge)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)
    copies = write_branch_copies(owner, bridge, decisions, next_rows)
    write_csv(OUTPUTS["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    validation = validation_rows(sources, owner, routes, schema, runner, bridge, decisions, next_rows, copies, csv_paths)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, owner, routes, schema, runner, bridge, decisions, next_rows, copies, validation)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"2151 validation {validation[-1]['status']}")


if __name__ == "__main__":
    main()
