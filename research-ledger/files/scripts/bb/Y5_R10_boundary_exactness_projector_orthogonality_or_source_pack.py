from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: object) -> bool:
    return str(value).strip().lower() == "true"


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
        ("SRC1019_0_1018_next", "source-intake/mts_residuals/P8_Y5_R10_1018_NEXT_TARGET.csv", "boundary exactness", "1018 handoff names the exactness/projector/source-pack fork."),
        ("SRC1019_1_1018_boundary_owner", "source-intake/mts_residuals/P8_Y5_R10_1018_OWNER_CLAUSES.csv", "LOC1018_5_Bclass_owner", "1018 boundary class/no-hair/projector owner."),
        ("SRC1019_2_1018_edge_route", "source-intake/mts_residuals/P8_Y5_R10_1018_ROUTE_TESTS.csv", "RT1018_4_edge_branch", "1018 retained edge/boundary residual route."),
        ("SRC1019_3_1018_source_schema", "source-intake/mts_residuals/P8_Y5_R10_1018_SOURCE_ROW_SCHEMA.csv", "FSR1018_6_edge_projection", "1018 edge projection source-row schema."),
        ("SRC1019_4_671_exact", "source-intake/mts_residuals/P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv", "BCG671_2_exact_boundary_form", "671 exact boundary form gate."),
        ("SRC1019_5_671_projector", "source-intake/mts_residuals/P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv", "BCG671_4_projector_orthogonality", "671 projector orthogonality gate."),
        ("SRC1019_6_671_cocycle", "source-intake/mts_residuals/P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv", "BCG671_5_boundary_cocycle", "671 boundary cocycle gate."),
        ("SRC1019_7_671_split", "source-intake/mts_residuals/P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv", "BCG671_6_no_double_count", "671 no-double-count gate."),
        ("SRC1019_8_671_verdict", "source-intake/mts_residuals/P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv", "BCG671_7_verdict", "671 boundary-zero verdict."),
        ("SRC1019_9_671_qbar_edge", "source-intake/mts_residuals/P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv", "ERV671_2_Qbar_edge_XH", "671 edge Hamiltonian/source projection residual."),
        ("SRC1019_10_671_bulk_edge", "source-intake/mts_residuals/P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv", "ERV671_6_bulk_edge_split", "671 bulk-edge split residual."),
        ("SRC1019_11_671_alpha_edge", "source-intake/mts_residuals/P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv", "ERV671_8_alpha_edge_product", "671 alpha edge product residual."),
        ("SRC1019_12_670_boundary_degree", "source-intake/mts_residuals/P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv", "NQ670_7_boundary_and_degree_count", "670 boundary and degree-count obstruction."),
        ("SRC1019_13_1017_boundary_flux", "source-intake/mts_residuals/P8_Y5_R10_1017_REFERENCE_LOCK_LAW.csv", "HRL1017_3_boundary_flux_zero", "1017 FB5540 boundary flux lock."),
        ("SRC1019_14_669_boundary_flux", "source-intake/mts_residuals/P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv", "RV669_7_boundary_flux_X", "669 X-sector boundary-flux residual."),
    ]
    rows = []
    for source_id, path_text, needle, role in specs:
        path = source_path(path_text)
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="ignore") if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle in text).lower(),
                "role": role,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def exactness_clause_rows() -> list[dict[str, str]]:
    rows = [
        {
            "clause_id": "BE1019_0_domain",
            "claim": "edge integration domain is compact, oriented, corner-free, and cohomologically controlled",
            "mathematical_form": "partial Sigma closed, partial(partial Sigma)=empty, H^{d-1}_edge either trivial or separately projected",
            "current_status": "not_signed",
            "what_would_close": "parent boundary class certificate with no corners, no harmonic edge sector, and allowed source surfaces",
            "failure_mode": "Stokes zero can miss corner/harmonic charges",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "BE1019_1_BX_exact",
            "claim": "boundary momentum is exact or pure-gauge on the allowed boundary class",
            "mathematical_form": "B_X=d_boundary b_X + B_X^pure with epsilon.B_X^pure=0",
            "current_status": "not_derived",
            "what_would_close": "explicit b_X from parent L_X/Theta_X/Q_X and reference boundary functional",
            "failure_mode": "Q_edge^H(lambda) remains an active residual",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "BE1019_2_Stokes_zero",
            "claim": "exact part integrates to zero on the certified edge domain",
            "mathematical_form": "int_partialSigma F_lambda epsilon.d_boundary b_X = int_partialpartialSigma F_lambda epsilon.b_X + kernel_derivative_terms = 0",
            "current_status": "conditional_math_pass",
            "what_would_close": "BE1019_0, BE1019_1, and a kernel condition d_boundary(F_lambda epsilon)=0 or a bound on kernel_derivative_terms",
            "failure_mode": "the range kernel F_lambda can reintroduce a boundary derivative term",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "BE1019_3_proper_gauge",
            "claim": "allowed gauge parameter kills improper edge modes without deleting physical mass/time/rotation charges",
            "mathematical_form": "epsilon_X|partialSigma=0 or epsilon_X compact-support while tau, ADM/time, and rotation generators remain admissible",
            "current_status": "closure_only",
            "what_would_close": "domain proof separating X-representative gauge from physical Hamiltonian generators",
            "failure_mode": "overrestricting the domain would falsely erase physical charge",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "BE1019_4_counterterm",
            "claim": "Q_X is differentiable after a local covariant boundary counterterm/reference subtraction",
            "mathematical_form": "delta(Q_X+B_X^ct)-i_epsilon Theta_X has no uncancelled partialSigma term",
            "current_status": "not_derived",
            "what_would_close": "local counterterm and fixed reference branch tied to 1017 HRL1017_3",
            "failure_mode": "Hamiltonian variation remains nonintegrable and feeds FB554_0",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "BE1019_5_cocycle_zero",
            "claim": "boundary generator algebra has no central/edge cocycle",
            "mathematical_form": "{G[epsilon],G[eta]}=G[[epsilon,eta]] with K_boundary[epsilon,eta]=0",
            "current_status": "uncomputed",
            "what_would_close": "bracket computation from parent Omega and differentiable G_X",
            "failure_mode": "edge mode survives as a central-extension/source residual",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "BE1019_6_verdict",
            "claim": "boundary exactness kills the edge branch",
            "mathematical_form": "BE1019_0 through BE1019_5 together imply Q_edge^H(lambda)=0 and K_boundary=0",
            "current_status": "fail_current_claim",
            "what_would_close": "all exactness clauses parent-signed in one boundary class",
            "failure_mode": "retain source-pack fallback rows for Qbar_edge_XH and K_edge",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def projector_clause_rows() -> list[dict[str, str]]:
    rows = [
        {
            "clause_id": "PO1019_0_projector_definition",
            "claim": "Hamiltonian mass/source projector is defined at fixed observed frame",
            "mathematical_form": "Pi_M^H[f]=partial f/partial M_H_ref |_{tau, surface, reference, C_top, chi_B}",
            "current_status": "formal_definition_only",
            "what_would_close": "1017 tau/reference/M_H_ref locks plus explicit source coordinate on solution space",
            "failure_mode": "projector can silently absorb reference or boundary variation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PO1019_1_edge_mass_independence",
            "claim": "edge charge has no same-frame source-mass dependence",
            "mathematical_form": "partial Q_edge^H(lambda)/partial M_H_ref |_{tau,reference,surface}=0",
            "current_status": "not_derived",
            "what_would_close": "show Q_edge depends only on fixed boundary cohomology/gauge data, not source worldtube data",
            "failure_mode": "Qbar_edge_XH(lambda) remains live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PO1019_2_symplectic_block",
            "claim": "source and edge sectors are symplectically orthogonal",
            "mathematical_form": "Omega(delta_M Phi, delta_edge Phi)=0 and Pi_M^H[delta_edge Q]=0",
            "current_status": "not_derived",
            "what_would_close": "block-diagonal reduced symplectic form or exact mixed term",
            "failure_mode": "edge/source mixing feeds FB554_0 or R10/R11",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PO1019_3_reference_silence",
            "claim": "reference subtraction does not reroute edge charge into mass readout",
            "mathematical_form": "Pi_M^H[Delta_ref + Delta_symp + B_class]=0",
            "current_status": "not_signed",
            "what_would_close": "B_ref derivative-silent theorem plus boundary class certificate",
            "failure_mode": "projector orthogonality is broken by reference movement",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PO1019_4_conditional_zero",
            "claim": "if projector clauses close, the edge Hamiltonian source charge is zero",
            "mathematical_form": "PO1019_0 through PO1019_3 imply Qbar_edge_XH(lambda)=Pi_M^H[Q_edge^H(lambda)]/M_H_ref=0",
            "current_status": "conditional_theorem_only",
            "what_would_close": "parent-signed projector definition plus mass-independence/block/reference lemmas",
            "failure_mode": "cannot zero ERV671_2_Qbar_edge_XH",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PO1019_5_verdict",
            "claim": "projector orthogonality kills the edge source projection",
            "mathematical_form": "Pi_M^H[Q_edge]=0 with no reference, tau, or surface leakage",
            "current_status": "fail_current_claim",
            "what_would_close": "PO1019_0 through PO1019_4 signed by same parent action/boundary class",
            "failure_mode": "retain Qbar_edge_XH source-pack row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def double_count_rows() -> list[dict[str, str]]:
    rows = [
        {
            "guard_id": "DC1019_0_orthogonal_split",
            "claim": "bulk X, edge X, FB5540, and R11 pieces occupy non-overlapping source directions",
            "mathematical_form": "Q_total=Q_bulk_X orthogonal_sum Q_edge_X orthogonal_sum Q_FB5540 orthogonal_sum Q_R11",
            "current_status": "missing_parent_split",
            "required_input": "projectors, source currents, and reference map for every component",
            "guardrail": "no component may be used twice or cancelled against an unknown component",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "guard_id": "DC1019_1_no_cancellation_total",
            "claim": "total local residual is scored by absolute-component envelope until the split is signed",
            "mathematical_form": "alpha_total_guard(lambda)=|alpha_bulk_X|+|alpha_edge_X|+|epsilon_FB5540|+|alpha_R11|",
            "current_status": "guard_written_components_missing",
            "required_input": "numeric/source-backed component rows and units",
            "guardrail": "opposite signs cannot create a pass while inputs are missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "guard_id": "DC1019_2_decision",
            "claim": "no local/R10/R11 pass without theorem-zero or complete no-cancellation source pack",
            "mathematical_form": "pass only if theorem_zero=true or all source rows valid_for_claim=true and abs-envelope <= bound",
            "current_status": "blocks_current_claim",
            "required_input": "boundary exactness/projector proof or complete coefficient pack",
            "guardrail": "retains residual vector instead of promoting symbolic zeros",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def source_pack_rows() -> list[dict[str, str]]:
    rows = [
        {
            "pack_id": "SP1019_0_M_H_ref",
            "quantity": "M_H_ref",
            "definition": "same-frame Hamiltonian source denominator",
            "required_columns": "system_id;tau_id;surface;Q_tau_integral;G_ref;H_ref;M_H_ref;units;reference_rule;source_path;valid_for_claim",
            "current_status": "MISSING_STABLE_MH_REF",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "SP1019_1_FB5540_components",
            "quantity": "delta_H_tau_nonintegrable_over_MH;Delta_ref_over_MH;symplectic_boundary_flux_over_MH",
            "definition": "componentwise FB554_0 numerator rows normalized by M_H_ref",
            "required_columns": "system_id;component_id;value_abs;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_FB5540_COMPONENT_VALUES",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "SP1019_2_bulk_X_coefficients",
            "quantity": "Z_X;M_X2;J_X;lambda_X",
            "definition": "bulk X operator coefficients and range",
            "required_columns": "system_id;field_id;Z_X;M_X2;J_X;lambda_X;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_PARENT_INPUT",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "SP1019_3_bulk_R10_projection",
            "quantity": "K_X;Qbar_XH;qbar_XT",
            "definition": "bulk R10 residual amplitude factors",
            "required_columns": "system_id;lambda_X;K_X;Qbar_XH;qbar_XT;normalization;units;source_path;valid_for_claim",
            "current_status": "MISSING_ARENA_PROJECTION",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_669_R10_R11_RESIDUAL_VECTOR.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "SP1019_4_edge_coefficients",
            "quantity": "lambda_edge;K_edge;B_X;K_boundary",
            "definition": "edge support, kernel normalization, boundary primitive, and cocycle",
            "required_columns": "system_id;lambda_edge;K_edge;B_X_status;K_boundary;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_EDGE_COEFFICIENTS",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "SP1019_5_edge_R10_projection",
            "quantity": "Qbar_edge_XH;qbar_XT;alpha_edge(lambda)",
            "definition": "edge Hamiltonian/source projection and test-body response",
            "required_columns": "system_id;lambda_edge;Qbar_edge_XH;qbar_XT;K_edge;alpha_edge;units;source_path;valid_for_claim",
            "current_status": "MISSING_EDGE_PROJECTION",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "SP1019_6_projector_zero_or_bound",
            "quantity": "Pi_M^H[Q_edge]",
            "definition": "projector orthogonality theorem certificate or numeric upper bound",
            "required_columns": "system_id;projector_definition;Q_edge;Pi_M_Q_edge;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_PROJECTOR_CERTIFICATE_OR_BOUND",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "SP1019_7_total_guard",
            "quantity": "alpha_total_guard(lambda)",
            "definition": "absolute no-cancellation envelope across FB5540, bulk X, edge X, and R11",
            "required_columns": "system_id;lambda;abs_alpha_bulk;abs_alpha_edge;abs_FB5540;abs_alpha_R11;component_sum_abs;bound;source_path;valid_for_claim",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1018_SOURCE_ROW_SCHEMA.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def route_verdict_rows() -> list[dict[str, str]]:
    rows = [
        {
            "route_id": "RVT1019_0_boundary_exactness",
            "route": "derive Q_edge=0 from exact boundary form",
            "status": "conditional_not_promoted",
            "requires": "BE1019_0 through BE1019_5 parent-signed",
            "result": "fail_current_claim",
            "fallback": "retain edge source-pack rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "RVT1019_1_projector_orthogonality",
            "route": "derive Qbar_edge_XH=0 from mass-projector orthogonality",
            "status": "conditional_not_promoted",
            "requires": "PO1019_0 through PO1019_4 parent-signed",
            "result": "fail_current_claim",
            "fallback": "source or bound Pi_M^H[Q_edge]",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "RVT1019_2_no_double_count",
            "route": "orthogonal source split prevents duplicate scoring",
            "status": "guard_written_not_derived",
            "requires": "bulk/edge/FB5540/R11 projectors and source currents",
            "result": "blocks_current_claim",
            "fallback": "absolute no-cancellation envelope",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "RVT1019_3_source_pack",
            "route": "complete source-backed coefficient pack if theorem-zero fails",
            "status": "schema_ready_no_values",
            "requires": "SP1019_0 through SP1019_7 numeric/source-backed rows",
            "result": "not_ready",
            "fallback": "next target obtains boundary certificate or first source row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "RVT1019_4_verdict",
            "route": "1019 branch closure",
            "status": "fail_current_claim",
            "requires": "theorem-zero route or complete source pack",
            "result": "no R10/R11/local-GR pass",
            "fallback": "1020 boundary cohomology/domain certificate or source-pack first row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def claim_gate_rows() -> list[dict[str, str]]:
    rows = [
        ("CG1019_0_source_chain_written", "1019 source chain exists", True, "all cited 1017/1018/669/670/671 rows are found", False),
        ("CG1019_1_boundary_exactness_closed", "boundary exactness theorem", False, "B_X exactness/domain/counterterm/cocycle clauses are unsigned", False),
        ("CG1019_2_projector_orthogonality_closed", "projector orthogonality theorem", False, "Pi_M definition, edge mass-independence, symplectic block, and reference silence are unsigned", False),
        ("CG1019_3_no_double_count_closed", "bulk-edge no-double-count split", False, "source projectors and absolute envelope inputs are missing", False),
        ("CG1019_4_source_pack_complete", "FB5540/bulk/edge/R11 source pack", False, "all source pack rows remain missing or not computed", False),
        ("CG1019_5_R10_R11_claim", "R10/R11 pass", False, "no theorem-zero or source-backed comparator row", False),
        ("CG1019_6_Newton_local_GR", "Newton/local-GR reduction", False, "Hamiltonian denominator, tau lock, and source charge remain downstream", False),
        ("CG1019_7_guardrail", "theorem-or-source-pack guardrail installed", True, "edge charge cannot be set to zero unless exactness/projector clauses close; otherwise source pack is mandatory", False),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": str(gate_pass).lower(),
            "reason": reason,
            "claim_allowed": str(claim_allowed).lower(),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for gate_id, claim, gate_pass, reason, claim_allowed in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    rows = [
        {
            "decision_id": "DEC1019_0_theorem_attempt",
            "decision": "The boundary exactness/projector route is now a precise conditional theorem, not a claim.",
            "because": "Stokes/projector arguments can kill Q_edge only after boundary domain, B_X primitive, counterterm, cocycle, and reference silence are parent-signed.",
            "next_action": "try to certify boundary cohomology/domain and B_X primitive first",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1019_1_best_route",
            "decision": "The cleanest derivation remains exactness plus projector orthogonality.",
            "because": "It removes the edge channel by structure rather than tuning coefficients.",
            "next_action": "derive or reject the boundary cohomology/domain certificate",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1019_2_fallback",
            "decision": "If exactness/projector clauses fail, the fallback is a no-cancellation source pack.",
            "because": "The edge branch then becomes a physical residual requiring lambda_edge, K_edge, Qbar_edge_XH, and qbar_XT.",
            "next_action": "fill SP1019 source rows before any R10/R11 comparator claim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1019_3_next_target",
            "decision": "The next checkpoint should attack the boundary cohomology/domain certificate or produce the first source-pack row.",
            "because": "BE1019_0/1 and PO1019_0/1 are the earliest clauses that can collapse the edge branch without data fitting.",
            "next_action": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            "objective": "either certify the boundary domain/cohomology and B_X primitive needed for Q_edge=0, or produce the first source-backed nonclaim row for the edge/source pack",
            "include": "closed boundary/corner audit, H_edge cohomology, allowed epsilon_X domain, B_X primitive, F_lambda derivative term, Pi_M^H definition, first source row if theorem route fails",
            "exclude": "symbolic edge zero, cancellation between unknown components, local-GR claim, R10/R11 pass, GitHub action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    changed = []
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file():
            modified = datetime.fromtimestamp(candidate.stat().st_mtime, timezone.utc)
            if modified >= STARTED:
                changed.append(candidate)
    return changed


def validation_rows(
    sources: list[dict[str, str]],
    exactness: list[dict[str, str]],
    projector: list[dict[str, str]],
    double_count: list[dict[str, str]],
    source_pack: list[dict[str, str]],
    routes: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    exactness_required = {"BE1019_0_domain", "BE1019_1_BX_exact", "BE1019_2_Stokes_zero", "BE1019_3_proper_gauge", "BE1019_4_counterterm", "BE1019_5_cocycle_zero", "BE1019_6_verdict"}
    projector_required = {"PO1019_0_projector_definition", "PO1019_1_edge_mass_independence", "PO1019_2_symplectic_block", "PO1019_3_reference_silence", "PO1019_4_conditional_zero", "PO1019_5_verdict"}
    source_required = {"SP1019_0_M_H_ref", "SP1019_1_FB5540_components", "SP1019_2_bulk_X_coefficients", "SP1019_3_bulk_R10_projection", "SP1019_4_edge_coefficients", "SP1019_5_edge_R10_projection", "SP1019_6_projector_zero_or_bound", "SP1019_7_total_guard"}
    checks = [
        ("V1019_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all cited source paths exist and expected row needles are present"),
        ("V1019_1_exactness_complete", exactness_required.issubset({row["clause_id"] for row in exactness}), "boundary exactness route covers domain, B_X, Stokes, gauge, counterterm, cocycle, and verdict"),
        ("V1019_2_exactness_blocks_claim", any(row["clause_id"] == "BE1019_6_verdict" and row["current_status"] == "fail_current_claim" for row in exactness), "exactness theorem is not promoted while clauses remain unsigned"),
        ("V1019_3_projector_complete", projector_required.issubset({row["clause_id"] for row in projector}), "projector route covers definition, edge mass-independence, symplectic block, reference silence, conditional zero, and verdict"),
        ("V1019_4_projector_blocks_claim", any(row["clause_id"] == "PO1019_5_verdict" and row["current_status"] == "fail_current_claim" for row in projector), "projector orthogonality is not promoted while parent locks are unsigned"),
        ("V1019_5_double_count_guard", all(row["valid_for_claim"] == "false" for row in double_count) and any(row["guard_id"] == "DC1019_1_no_cancellation_total" for row in double_count), "absolute no-cancellation guard is installed"),
        ("V1019_6_source_pack_complete", source_required.issubset({row["pack_id"] for row in source_pack}), "source pack schema covers M_H_ref, FB5540, bulk X, edge X, projector, and total guard"),
        ("V1019_7_source_pack_nonclaim", all(row["valid_for_claim"] == "false" and ("MISSING" in row["current_status"] or "NOT_COMPUTED" in row["current_status"]) for row in source_pack), "source pack remains nonclaim until real rows exist"),
        ("V1019_8_route_verdict_fails", any(row["route_id"] == "RVT1019_4_verdict" and row["result"] == "no R10/R11/local-GR pass" for row in routes), "1019 route verdict blocks promotion"),
        ("V1019_9_claim_gates_blocked", all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in gates), "R10/R11, Newton, and local-GR claims remain blocked"),
        ("V1019_10_guardrail_written", any(row["gate_id"] == "CG1019_7_guardrail" and flag(row["gate_pass"]) for row in gates), "theorem-or-source-pack guardrail is installed"),
        ("V1019_11_decision_written", any(row["decision_id"] == "DEC1019_3_next_target" for row in decisions), "1020 decision row is present"),
        ("V1019_12_next_target_written", len(next_target) == 1 and "1020-Y5-R10-boundary-cohomology" in next_target[0]["next_target"], "1020 next target row is present and nonclaim"),
        ("V1019_13_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1019_SUMMARY", "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail", "detail": "1019 boundary exactness/projector/source-pack validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    exactness: list[dict[str, str]],
    projector: list[dict[str, str]],
    double_count: list[dict[str, str]],
    source_pack: list[dict[str, str]],
    routes: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1019 Y5 R10 boundary exactness projector orthogonality or source pack",
            "",
            "**Status:** The edge/boundary obstruction is now split into two clean theorem routes and one source-pack fallback. Exactness plus Stokes can kill `Q_edge`, and projector orthogonality can kill `Qbar_edge_XH`, but neither is parent-signed in current MTS.",
            "",
            "**Claim ceiling:** no boundary-zero theorem, `Qbar_edge_XH=0`, `K_boundary=0`, no-double-count closure, R10/R11 pass, Newton limit, PPN pass, or local-GR reduction is allowed from 1019.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Boundary exactness clauses",
            md_table(exactness, ["clause_id", "claim", "mathematical_form", "current_status", "what_would_close", "failure_mode", "valid_for_claim"]),
            "## Projector orthogonality clauses",
            md_table(projector, ["clause_id", "claim", "mathematical_form", "current_status", "what_would_close", "failure_mode", "valid_for_claim"]),
            "## No-double-count guard",
            md_table(double_count, ["guard_id", "claim", "mathematical_form", "current_status", "required_input", "guardrail", "valid_for_claim"]),
            "## Source-pack schema",
            md_table(source_pack, ["pack_id", "quantity", "definition", "required_columns", "current_status", "source_path", "valid_for_claim"]),
            "## Route verdicts",
            md_table(routes, ["route_id", "route", "status", "requires", "result", "fallback", "valid_for_claim"]),
            "## Claim gates",
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
    exactness = exactness_clause_rows()
    projector = projector_clause_rows()
    double_count = double_count_rows()
    source_pack = source_pack_rows()
    routes = route_verdict_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, exactness, projector, double_count, source_pack, routes, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1019_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv", exactness)
    write_csv(OUT / "P8_Y5_R10_1019_PROJECTOR_ORTHOGONALITY_CLAUSES.csv", projector)
    write_csv(OUT / "P8_Y5_R10_1019_NO_DOUBLE_COUNT_GUARD.csv", double_count)
    write_csv(OUT / "P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv", source_pack)
    write_csv(OUT / "P8_Y5_R10_1019_ROUTE_VERDICTS.csv", routes)
    write_csv(OUT / "P8_Y5_R10_1019_CLAIM_GATES.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1019_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1019_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1019_VALIDATION.csv", validations)
    write_doc(sources, exactness, projector, double_count, source_pack, routes, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()
