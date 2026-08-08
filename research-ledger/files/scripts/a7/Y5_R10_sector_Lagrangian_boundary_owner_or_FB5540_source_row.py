from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


def missing(value: object) -> bool:
    text = str(value or "").strip()
    upper = text.upper()
    return (
        text == ""
        or upper.startswith("MISSING")
        or upper.startswith("NOT_COMPUTED")
        or upper.startswith("PRIVATE_OR_PLACEHOLDER")
        or text.startswith("FILL_")
    )


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1018_0_1017_next", "source-intake/mts_residuals/P8_Y5_R10_1017_NEXT_TARGET.csv", "L_X/Theta_X/Q_X", "1017 handoff target."),
        ("SRC1018_1_1017_law", "source-intake/mts_residuals/P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv", "HRL1017_1_integrability_curl", "1017 reference-lock law."),
        ("SRC1018_2_1017_schema", "source-intake/mts_residuals/P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv", "MHR1017_0_M_H_ref_denominator", "1017 MHref first-row schema."),
        ("SRC1018_3_668_sector", "source-intake/mts_residuals/P8_Y5_R10_668_SECTOR_OWNER_AUDIT.csv", "SO668_2_MTS_extra_LX", "668 sector owner audit."),
        ("SRC1018_4_668_boundary", "source-intake/mts_residuals/P8_Y5_R10_668_BOUNDARY_CONDITION_LOCK.csv", "BCL668_1_reference_fixed_branch", "668 boundary condition lock."),
        ("SRC1018_5_668_impact", "source-intake/mts_residuals/P8_Y5_R10_668_FB5540_IMPACT_MAP.csv", "IM668_0_delta_H_tau", "668 FB5540 impact map."),
        ("SRC1018_6_669_candidates", "source-intake/mts_residuals/P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv", "LX669_0_absent_quotient_variable", "669 minimal L_X candidates."),
        ("SRC1018_7_669_gates", "source-intake/mts_residuals/P8_Y5_R10_669_LX_OWNER_GATE_TESTS.csv", "G669_6_theta_QX_owner", "669 L_X owner gate tests."),
        ("SRC1018_8_669_variation", "source-intake/mts_residuals/P8_Y5_R10_669_THETA_QX_VARIATION_LEDGER.csv", "V669_4_integrability", "669 Theta/QX variation ledger."),
        ("SRC1018_9_669_vector", "source-intake/mts_residuals/P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv", "RV669_0_Z_X", "669 retained residual vector."),
        ("SRC1018_10_670_no_pole", "source-intake/mts_residuals/P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv", "NQ670_8_no_pole_result", "670 no-pole quotient proof chain."),
        ("SRC1018_11_670_sourcefree", "source-intake/mts_residuals/P8_Y5_R10_670_POSITIVE_SOURCEFREE_PROOF_CHAIN.csv", "PSF670_6_zero_profile_result", "670 positive sourcefree proof chain."),
        ("SRC1018_12_670_effect", "source-intake/mts_residuals/P8_Y5_R10_670_R10_R11_ZERO_OR_RESIDUAL_EFFECT.csv", "ZE670_5_R10_R11", "670 zero/residual effect map."),
        ("SRC1018_13_671_boundary", "source-intake/mts_residuals/P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv", "BCG671_7_verdict", "671 boundary charge owner gate."),
        ("SRC1018_14_671_edge", "source-intake/mts_residuals/P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv", "ERV671_9_decision_row", "671 edge residual vector."),
    ]
    rows = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": path_text,
                "exists": str(path.exists()).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "generated_utc": stamp(),
            }
        )
    return rows


def owner_clause_rows() -> list[dict[str, str]]:
    rows = [
        (
            "LOC1018_0_LX_owner",
            "parent-owned MTS extra-sector Lagrangian",
            "L_X[g,X,nabla X] with explicit operator, source term, field normalization, and boundary conditions",
            "not_signed",
            "Theta_X, Q_X, omega_X, C_X, R10, and R11 cannot be computed",
            "delta_H_tau_nonintegrable_over_MH;C_extra;R10;R11",
        ),
        (
            "LOC1018_1_Theta_QX_owner",
            "sector symplectic potential and Hamiltonian charge",
            "delta L_X=E_X delta X+dTheta_X; J_tau^X=Theta_X(L_tau X)-i_tau L_X=dQ_tau^X+C_tau^X",
            "formula_written_not_owned",
            "Hamiltonian integrability remains schematic",
            "delta_H_tau_nonintegrable_over_MH;symplectic_boundary_flux_over_MH",
        ),
        (
            "LOC1018_2_no_pole_quotient",
            "X is absent from physical quotient or first-class vertical",
            "Dq[v_X]=0 and G_X=int epsilon C_X+Q_X is differentiable with zero boundary charge",
            "conditional_route_unsigned",
            "parent Omega/DC_X and boundary charge owner do not close",
            "K_X;qbar_XT;Qbar_XH",
        ),
        (
            "LOC1018_3_positive_sourcefree",
            "physical X branch has positive source-free operator",
            "O_X X=-nabla_i(Z_X nabla^i X)+M_X^2 X, Z_X>0, M_X^2>0, J_X=0, boundary_flux_X=0",
            "conditional_theorem_unsigned",
            "Z_X, M_X^2, J_X=0, and boundary_flux_X=0 are not parent-signed together",
            "lambda_X;alpha_X;R10;R11",
        ),
        (
            "LOC1018_4_Bref_owner",
            "reference boundary functional selected before readout",
            "B_ref[gamma_ref,tau_ref,C_top] with partial_{source,r,t,frame,lambda}Delta_ref=0",
            "not_signed",
            "reference can absorb source calibration",
            "Delta_ref_over_MH;Delta_symp_over_MH",
        ),
        (
            "LOC1018_5_Bclass_owner",
            "boundary class/no-hair/projector silence",
            "B_class[chi_B,C_top] plus exact/proper-gauge/no-vector-tensor-hair conditions",
            "not_signed",
            "symplectic boundary flux and edge charge remain live",
            "B_zero_flux;symplectic_boundary_flux;Qbar_edge_XH",
        ),
        (
            "LOC1018_6_tau_owner",
            "observed time/coframe functor",
            "tau_source=tau_charge=tau_clock=tau_readout and delta tau=0",
            "not_signed",
            "same-frame Hamiltonian source charge is not fixed",
            "time_generator_lock;Delta_frame;clock;Gdot",
        ),
        (
            "LOC1018_7_MHref_owner",
            "source denominator and Gauss/readout relation",
            "M_H_ref=G_ref^-1 int_S Q_tau^MTS before GM_orbit=G_ref M_H_ref is derived",
            "not_signed",
            "normalization remains guardrail only",
            "M_H_ref;Delta_cal;PPN_vector",
        ),
        (
            "LOC1018_8_verdict",
            "all owners needed for FB554_0 and local-GR source charge",
            "LOC1018_0 through LOC1018_7 parent-signed together",
            "fail_current_claim",
            "current MTS has a precise owner map but no owner closure",
            "FB554_0;R10;R11;local_GR",
        ),
    ]
    return [
        {
            "owner_id": owner_id,
            "required_owner": required_owner,
            "mathematical_form": mathematical_form,
            "current_status": current_status,
            "failure_if_missing": failure_if_missing,
            "feeds": feeds,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for owner_id, required_owner, mathematical_form, current_status, failure_if_missing, feeds in rows
    ]


def route_test_rows() -> list[dict[str, str]]:
    rows = [
        (
            "RT1018_0_absent_quotient",
            "no independent X after quotient",
            "S_parent=S_red[q(Phi)] and Dq[v_X]=0 before variation",
            "best_GR_reduction_route_not_derived",
            "actual q map, matter descent, parent Omega, and boundary charge silence are unsigned",
            "finite residual vector retained",
        ),
        (
            "RT1018_1_vertical_constraint",
            "X is vertical first-class constraint direction",
            "delta G_X=Omega(delta Phi,v_X); Q_X differentiable; K_boundary=0",
            "best_active_theorem_route_not_signed",
            "single parent owner and boundary differentiability do not close",
            "edge residual vector retained",
        ),
        (
            "RT1018_2_positive_sourcefree",
            "positive source-free local operator kills X profile",
            "int_A(Z_X|grad X|^2+M_X^2 X^2)=int_A XJ_X+boundary_flux_X",
            "conditional_theorem_only",
            "Z_X, M_X^2, J_X=0, and boundary_flux_X=0 are missing",
            "alpha/lambda residual vector retained",
        ),
        (
            "RT1018_3_massive_sourced",
            "finite physical X residual",
            "lambda_X=sqrt(Z_X/M_X^2), alpha_X=K_X Qbar_XH qbar_XT",
            "schema_ready_no_values",
            "all coefficients/units/source paths are missing or nonclaim",
            "R10/R11 source acquisition required",
        ),
        (
            "RT1018_4_edge_branch",
            "edge/boundary charge residual",
            "alpha_edge(lambda)=K_edge(lambda) Qbar_edge_XH(lambda) qbar_XT",
            "schema_ready_no_values",
            "boundary exactness/projector orthogonality and edge coefficients are missing",
            "edge residual vector retained",
        ),
        (
            "RT1018_5_verdict",
            "sector Lagrangian/boundary owner closed",
            "one of RT1018_0, RT1018_1, RT1018_2 theorem-zero routes, or source-backed RT1018_3/4 row",
            "fail_current_claim",
            "no route currently signs enough clauses or supplies source-backed values",
            "move to boundary exactness/projector orthogonality or FB5540 source row",
        ),
    ]
    return [
        {
            "route_id": route_id,
            "route": route,
            "mathematical_form": mathematical_form,
            "current_status": current_status,
            "blocker": blocker,
            "fallback": fallback,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for route_id, route, mathematical_form, current_status, blocker, fallback in rows
    ]


def source_row_schema_rows() -> list[dict[str, str]]:
    rows = [
        ("FSR1018_0_M_H_ref", "M_H_ref", "same-frame Hamiltonian source denominator", "system_id;surface;Q_tau_integral;G_ref;H_ref;M_H_ref;units;source_path;assumptions;valid_for_claim", "MISSING_STABLE_MH_REF", "source-intake/mts_residuals/P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv"),
        ("FSR1018_1_delta_H_tau", "delta_H_tau_nonintegrable_over_MH", "field-space curl of Hamiltonian variation normalized by M_H_ref", "system_id;surface_pair;omega_X_integral;reference_curl;M_H_ref;units;source_path;assumptions;valid_for_claim", "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO", "source-intake/mts_residuals/P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv"),
        ("FSR1018_2_Delta_ref", "Delta_ref_over_MH", "reference shift/derivative profile normalized by M_H_ref", "system_id;reference_branch;Delta_ref;derivative_profile;M_H_ref;units;source_path;assumptions;valid_for_claim", "MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO", "source-intake/mts_residuals/P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv"),
        ("FSR1018_3_boundary_flux", "symplectic_boundary_flux_over_MH;B_zero_flux;Delta_symp", "boundary/projector/non-EH linked flux normalized by M_H_ref", "system_id;surface_pair;symplectic_boundary_flux;B_zero_flux;Delta_symp;M_H_ref;units;source_path;assumptions;valid_for_claim", "MISSING_SYMPLECTIC_BOUNDARY_NUMERIC_OR_THEOREM_ZERO", "source-intake/mts_residuals/P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv"),
        ("FSR1018_4_LX_bulk_coefficients", "Z_X;M_X2;J_X;lambda_X", "bulk X-sector coefficients if no theorem-zero route closes", "system_id;field_id;Z_X;M_X2;J_X;lambda_X;units;source_path;assumptions;valid_for_claim", "MISSING_PARENT_INPUT", "source-intake/mts_residuals/P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv"),
        ("FSR1018_5_R10_source_projection", "K_X;Qbar_XH;qbar_XT", "R10 residual amplitude factors for active X exchange", "system_id;K_X;Qbar_XH;qbar_XT;normalization;units;source_path;assumptions;valid_for_claim", "MISSING_ARENA_PROJECTION", "source-intake/mts_residuals/P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv"),
        ("FSR1018_6_edge_projection", "lambda_edge;K_edge;Qbar_edge_XH;qbar_XT", "edge/boundary residual amplitude factors if boundary theorem fails", "system_id;lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;units;source_path;assumptions;valid_for_claim", "MISSING_EDGE_COEFFICIENTS", "source-intake/mts_residuals/P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv"),
        ("FSR1018_7_total_guard", "FB5540_alpha_R11_total_guard", "no-cancellation envelope across FB5540, bulk X, edge X, and R11 coefficients", "system_id;component_sum_abs;M_H_ref;normalization;source_path;assumptions;valid_for_claim", "NOT_COMPUTED_COMPONENTS_MISSING", "source-intake/mts_residuals/P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv"),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "definition": definition,
            "required_columns": required_columns,
            "current_status": current_status,
            "source_path": source_path_text,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for row_id, quantity, definition, required_columns, current_status, source_path_text in rows
    ]


def runner_rows(schema: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = []
    for row in schema:
        reasons = []
        if missing(row["current_status"]):
            reasons.append("MISSING_THEOREM_OR_SOURCE_INPUT")
        if not flag(row["valid_for_claim"]):
            reasons.append("VALID_FOR_CLAIM_FALSE")
        rows.append(
            {
                "runner_id": row["row_id"].replace("FSR1018", "FRR1018"),
                "row_id": row["row_id"],
                "quantity": row["quantity"],
                "computed_status": "blocked_missing_inputs",
                "claim_allowed": "false",
                "failure_reasons": ";".join(reasons),
                "generated_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, str]]:
    gates = [
        ("CG1018_0_owner_map_written", "sector Lagrangian/boundary owner map is explicit", "true", "owner clauses cover L_X, Theta/Q, quotient, sourcefree, B_ref, boundary, tau, and MHref", "false"),
        ("CG1018_1_LX_owned", "L_X, Theta_X, Q_X, omega_X are parent-owned", "false", "minimal L_X candidates are routes, not signed current-MTS derivations", "false"),
        ("CG1018_2_no_pole_zero", "X has no physical pole and no R10/R11 residual", "false", "parent Omega/DC_X plus boundary charge silence are unsigned", "false"),
        ("CG1018_3_positive_sourcefree_zero", "X=0 in compact local exterior by positive sourcefree theorem", "false", "Z_X, M_X2, J_X=0, and boundary_flux_X=0 are missing", "false"),
        ("CG1018_4_FB5540_first_row_ready", "FB5540 source row is claim-ready", "false", "M_H_ref and numerator components remain missing", "false"),
        ("CG1018_5_R10_R11_ready", "R10/R11 residual vectors are source-backed", "false", "bulk and edge coefficients are missing/nonclaim", "false"),
        ("CG1018_6_Newton_local_GR", "Newton/local-GR gates can reopen", "false", "source charge, FB5540, R10/R11, and PPN owners remain blocked", "false"),
        ("CG1018_7_guardrail", "sector-owner/source-row guardrail is installed", "true", "no closure credit from symbolic L_X, reference-only zero, or cancellation between unknowns", "false"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "claim_allowed": claim_allowed,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for gate_id, claim, gate_pass, reason, claim_allowed in gates
    ]


def decision_rows() -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "DEC1018_0_owner_result",
            "decision": "The owner map is sharp, but no owner route closes current MTS.",
            "because": "L_X/Theta_X/Q_X, B_ref, B_class/C_top/chi_B, tau, M_H_ref, and boundary charge are all still unsigned.",
            "next_action": "do not promote FB5540, R10, R11, or local GR from symbolic sector machinery",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1018_1_best_derivation_route",
            "decision": "The no-pole quotient route is the strongest if boundary exactness and projector orthogonality close.",
            "because": "it removes the physical X pole structurally rather than fitting a small coefficient.",
            "next_action": "try boundary exactness/projector orthogonality before coefficient sourcing",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1018_2_source_row_fallback",
            "decision": "If theorem-zero routes fail, the fallback is a full no-cancellation source row.",
            "because": "FB5540, bulk X, edge X, and R11 pieces cannot cancel as unknowns or borrow orbital GM as denominator.",
            "next_action": "source M_H_ref and all numerator/edge/bulk factors together or keep row blocked",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC1018_3_next_target",
            "decision": "The next root target is boundary exactness/projector orthogonality or a complete source pack.",
            "because": "671 shows Qbar_edge_XH and boundary charge are the live obstruction after L_X/no-pole routes remain unsigned.",
            "next_action": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "valid_for_claim": "false",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "objective": "derive boundary exactness, projector orthogonality, and no edge/source double-count for the X/Hamiltonian branch, or build a complete source pack for FB5540 plus bulk/edge R10/R11 coefficients",
            "include": "B_X exactness, proper gauge domain, Q_X differentiability, Pi_M^H[Q_edge]=0, K_boundary=0, M_H_ref, FB5540 components, K_X, Qbar_XH, qbar_XT, edge coefficients, source paths",
            "exclude": "symbolic edge zero, closure-only quotient, coefficient cancellation, orbital-GM denominator, unnormalized alpha/R_eq row, Newton/local-GR claim, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file() and datetime.fromtimestamp(candidate.stat().st_mtime, timezone.utc) >= STARTED:
            changed.append(candidate)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    owners: list[dict[str, str]],
    routes: list[dict[str, str]],
    schema: list[dict[str, str]],
    runner: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    required_owners = {
        "LOC1018_0_LX_owner",
        "LOC1018_1_Theta_QX_owner",
        "LOC1018_2_no_pole_quotient",
        "LOC1018_3_positive_sourcefree",
        "LOC1018_4_Bref_owner",
        "LOC1018_5_Bclass_owner",
        "LOC1018_6_tau_owner",
        "LOC1018_7_MHref_owner",
        "LOC1018_8_verdict",
    }
    required_routes = {"RT1018_0_absent_quotient", "RT1018_1_vertical_constraint", "RT1018_2_positive_sourcefree", "RT1018_3_massive_sourced", "RT1018_4_edge_branch", "RT1018_5_verdict"}
    required_quantities = {"M_H_ref", "delta_H_tau_nonintegrable_over_MH", "Delta_ref_over_MH", "symplectic_boundary_flux_over_MH;B_zero_flux;Delta_symp", "Z_X;M_X2;J_X;lambda_X", "K_X;Qbar_XH;qbar_XT", "lambda_edge;K_edge;Qbar_edge_XH;qbar_XT", "FB5540_alpha_R11_total_guard"}
    checks = [
        ("V1018_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all source paths exist and needles are present"),
        ("V1018_1_owner_map_complete", required_owners.issubset({row["owner_id"] for row in owners}), "owner map covers L_X, Theta/Q, quotient, sourcefree, boundary, tau, MHref, and verdict"),
        ("V1018_2_owner_map_blocks_claim", any(row["owner_id"] == "LOC1018_8_verdict" and row["current_status"] == "fail_current_claim" for row in owners) and all(not flag(row["valid_for_claim"]) for row in owners), "owner map remains nonclaim and blocks current promotion"),
        ("V1018_3_route_tests_complete", required_routes.issubset({row["route_id"] for row in routes}), "route tests cover no-pole, vertical, sourcefree, sourced, edge, and verdict branches"),
        ("V1018_4_route_verdict_fails", any(row["route_id"] == "RT1018_5_verdict" and row["current_status"] == "fail_current_claim" for row in routes), "no route currently closes theorem-zero or source-backed fallback"),
        ("V1018_5_source_schema_complete", required_quantities.issubset({row["quantity"] for row in schema}), "source schema covers FB5540, bulk X, edge X, and total guard rows"),
        ("V1018_6_source_schema_nonclaim", all(missing(row["current_status"]) and not flag(row["valid_for_claim"]) for row in schema), "all source schema rows remain missing and nonclaim"),
        ("V1018_7_runner_refuses", len(runner) == len(schema) and all(row["computed_status"] == "blocked_missing_inputs" and not flag(row["claim_allowed"]) for row in runner), "runner refuses missing source rows"),
        ("V1018_8_claim_gates_blocked", all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in gates), "owner, R10/R11, Newton, and local-GR claims remain blocked"),
        ("V1018_9_guardrail_written", any(row["gate_id"] == "CG1018_7_guardrail" and flag(row["gate_pass"]) for row in gates), "sector-owner/source-row guardrail is installed"),
        ("V1018_10_decision_written", any(row["decision_id"] == "DEC1018_3_next_target" for row in decisions), "1019 root target decision is written"),
        ("V1018_11_next_target_written", len(next_target) == 1 and "1019-Y5-R10-boundary-exactness" in next_target[0]["next_target"], "1019 target row is present and nonclaim"),
        ("V1018_12_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1018_SUMMARY", "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail", "detail": "1018 sector Lagrangian/boundary owner validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    owners: list[dict[str, str]],
    routes: list[dict[str, str]],
    schema: list[dict[str, str]],
    runner: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1018 Y5 R10 sector Lagrangian boundary owner or FB5540 source row",
            "",
            "**Status:** The sector-owner map is now tied to the modern 1017 `FB554_0` lock. `L_X/Theta_X/Q_X`, `B_ref`, `B_class/C_top/chi_B`, tau, `M_H_ref`, bulk X, and edge X are all explicit, but no theorem-zero route or source-backed row closes current MTS.",
            "",
            "**Claim ceiling:** no `L_X` owner, `FB554_0=0`, no-pole theorem, source-free X theorem, R10/R11 pass, measured-GM closure, Newton/GR reduction, PPN pass, or local-GR claim is allowed from 1018.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Owner clauses",
            md_table(owners, ["owner_id", "required_owner", "mathematical_form", "current_status", "failure_if_missing", "feeds", "valid_for_claim"]),
            "## Route tests",
            md_table(routes, ["route_id", "route", "mathematical_form", "current_status", "blocker", "fallback", "valid_for_claim"]),
            "## Source-row schema",
            md_table(schema, ["row_id", "quantity", "definition", "required_columns", "current_status", "valid_for_claim"]),
            "## Source-row runner",
            md_table(runner, ["runner_id", "row_id", "quantity", "computed_status", "claim_allowed", "failure_reasons"]),
            "## Claim gate",
            md_table(gates, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Validation",
            md_table(validations, ["check_id", "result", "detail", "generated_utc"]),
            "## Next target",
            md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    owners = owner_clause_rows()
    routes = route_test_rows()
    schema = source_row_schema_rows()
    runner = runner_rows(schema)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, owners, routes, schema, runner, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1018_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1018_OWNER_CLAUSES.csv", owners)
    write_csv(OUT / "P8_Y5_R10_1018_ROUTE_TESTS.csv", routes)
    write_csv(OUT / "P8_Y5_R10_1018_SOURCE_ROW_SCHEMA.csv", schema)
    write_csv(OUT / "P8_Y5_R10_1018_SOURCE_ROW_RUNNER.csv", runner)
    write_csv(OUT / "P8_Y5_R10_1018_CLAIM_GATE.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1018_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1018_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1018_VALIDATION.csv", validations)
    write_doc(sources, owners, routes, schema, runner, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()
