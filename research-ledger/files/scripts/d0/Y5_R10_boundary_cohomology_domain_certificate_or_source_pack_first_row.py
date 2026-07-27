from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md"
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
        ("SRC1020_0_1019_next", "source-intake/mts_residuals/P8_Y5_R10_1019_NEXT_TARGET.csv", "boundary domain/cohomology", "1019 handoff to boundary domain/cohomology or first source row."),
        ("SRC1020_1_1019_exactness", "source-intake/mts_residuals/P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv", "BE1019_0_domain", "1019 domain/corner/cohomology clause."),
        ("SRC1020_2_1019_BX", "source-intake/mts_residuals/P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv", "BE1019_1_BX_exact", "1019 B_X exactness clause."),
        ("SRC1020_3_1019_kernel", "source-intake/mts_residuals/P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv", "kernel_derivative_terms", "1019 Stokes kernel derivative obstruction."),
        ("SRC1020_4_1019_projector", "source-intake/mts_residuals/P8_Y5_R10_1019_PROJECTOR_ORTHOGONALITY_CLAUSES.csv", "PO1019_1_edge_mass_independence", "1019 projector mass-independence clause."),
        ("SRC1020_5_1019_source_pack", "source-intake/mts_residuals/P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv", "SP1019_6_projector_zero_or_bound", "1019 projector zero/bound source-pack row."),
        ("SRC1020_6_1019_guard", "source-intake/mts_residuals/P8_Y5_R10_1019_NO_DOUBLE_COUNT_GUARD.csv", "DC1019_1_no_cancellation_total", "1019 no-cancellation guard."),
        ("SRC1020_7_671_gate", "source-intake/mts_residuals/P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv", "BCG671_2_exact_boundary_form", "671 boundary exactness gate."),
        ("SRC1020_8_671_projector", "source-intake/mts_residuals/P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv", "BCG671_4_projector_orthogonality", "671 projector orthogonality gate."),
        ("SRC1020_9_671_edge_vector", "source-intake/mts_residuals/P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv", "ERV671_4_BX_boundary_momentum", "671 B_X residual vector."),
        ("SRC1020_10_671_qbar_edge", "source-intake/mts_residuals/P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv", "ERV671_2_Qbar_edge_XH", "671 Qbar_edge residual."),
        ("SRC1020_11_670_boundary", "source-intake/mts_residuals/P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv", "NQ670_7_boundary_and_degree_count", "670 boundary/degree-count obstruction."),
        ("SRC1020_12_1018_Bclass", "source-intake/mts_residuals/P8_Y5_R10_1018_OWNER_CLAUSES.csv", "LOC1018_5_Bclass_owner", "1018 boundary class/no-hair/projector owner."),
        ("SRC1020_13_1001_surface", "1001-Y5-R10-Bref-radius-surface-term-theorem-or-Delta-ref-radial-profile-row.md", "MISSING_PARENT_SURFACE_CLASS", "1001 surface/corner Stokes precedent."),
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


def domain_certificate_rows() -> list[dict[str, str]]:
    rows = [
        {
            "certificate_id": "BDC1020_0_surface_manifold",
            "object": "edge surface S_edge",
            "required_certificate": "compact oriented smooth codim-2 surface with no active corner boundary",
            "mathematical_test": "partial S_edge = empty, or every corner C has an explicit corner charge Q_C included in the source pack",
            "current_status": "not_signed",
            "failure_if_missing": "Stokes zero can hide corner charge",
            "feeds": "Q_edge_zero;corner_source_row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "certificate_id": "BDC1020_1_boundary_class",
            "object": "allowed boundary class B_class",
            "required_certificate": "same B_class is used by L_X, Q_X, B_ref, Pi_M^H, and R10/R11 readout",
            "mathematical_test": "delta B_class=0 along source variation and no retuning between source/test systems",
            "current_status": "not_signed",
            "failure_if_missing": "reference or boundary class can absorb the signal",
            "feeds": "FB5540;Qbar_edge_XH",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "certificate_id": "BDC1020_2_relative_cohomology",
            "object": "relative edge cohomology H_edge",
            "required_certificate": "harmonic/non-exact edge class is absent or separately measured as h_X",
            "mathematical_test": "B_X=d_S b_X+h_X with h_X=0, or |int_S F_lambda epsilon h_X| source-bounded",
            "current_status": "not_signed",
            "failure_if_missing": "exactness misses a harmonic edge mode",
            "feeds": "harmonic_edge_bound;Q_edge_zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "certificate_id": "BDC1020_3_allowed_epsilon",
            "object": "epsilon_X domain",
            "required_certificate": "epsilon_X is a proper X-representative gauge while physical tau/mass/rotation generators remain admissible",
            "mathematical_test": "epsilon_X|S_edge=0 or d_S(F_lambda epsilon_X)=0 without constraining tau_source or ADM charges",
            "current_status": "closure_only",
            "failure_if_missing": "proper-gauge zero may erase real physical charges",
            "feeds": "Q_edge_zero;projector_definition",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "certificate_id": "BDC1020_4_kernel_weight",
            "object": "F_lambda epsilon_X",
            "required_certificate": "the edge kernel/gauge weight is closed on S_edge or its derivative term is source-bounded",
            "mathematical_test": "d_S(F_lambda epsilon_X)=0, or ||d_S(F_lambda epsilon_X)||_* and ||b_X||_* are supplied",
            "current_status": "not_signed",
            "failure_if_missing": "weighted Stokes identity leaves a derivative residual",
            "feeds": "kernel_derivative_bound",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "certificate_id": "BDC1020_5_verdict",
            "object": "boundary domain certificate",
            "required_certificate": "BDC1020_0 through BDC1020_4 signed in one parent boundary class",
            "mathematical_test": "closed/corner-free plus cohomology plus epsilon/kernel conditions imply no untracked edge domain term",
            "current_status": "fail_current_claim",
            "failure_if_missing": "Q_edge cannot be set to zero by Stokes alone",
            "feeds": "1021_BX_primitive_or_edge_bound",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def exactness_theorem_rows() -> list[dict[str, str]]:
    rows = [
        {
            "theorem_id": "ETB1020_0_decomposition",
            "statement": "Decompose the boundary momentum into exact, harmonic, and non-owned residual parts.",
            "formula": "B_X = d_S b_X + h_X + r_X",
            "current_result": "formal_decomposition",
            "missing_for_claim": "parent L_X/Theta_X/Q_X must prove r_X=0 and identify h_X",
            "bound_if_missing": "|Q_edge| keeps |int_S F epsilon h_X| + |int_S F epsilon r_X|",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "ETB1020_1_weighted_Stokes_identity",
            "statement": "Exactness kills the edge charge only when the kernel/gauge weight has no surface derivative term.",
            "formula": "int_S F epsilon d_S b_X = int_partialS F epsilon b_X - int_S d_S(F epsilon) wedge b_X",
            "current_result": "math_identity_written",
            "missing_for_claim": "partial S=empty or corner row, plus d_S(F epsilon)=0 or a derivative bound",
            "bound_if_missing": "|int_S F epsilon d_S b_X| <= ||d_S(F epsilon)||_* ||b_X||_* + |corner_term|",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "ETB1020_2_zero_conditions",
            "statement": "A genuine edge-zero theorem requires exactness, no harmonic part, no residual part, no corner term, and closed weight.",
            "formula": "partialS=empty, h_X=0, r_X=0, d_S(F epsilon)=0 => Q_edge^H(lambda)=0",
            "current_result": "conditional_theorem",
            "missing_for_claim": "all hypotheses remain unsigned in current MTS",
            "bound_if_missing": "use ETB1020_3 instead of zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "ETB1020_3_residual_bound",
            "statement": "If exact zero fails, the edge charge has a finite source-pack bound rather than an arbitrary closure.",
            "formula": "|Q_edge(lambda)| <= C_corner + ||d_S(F_lambda epsilon_X)||_* ||b_X||_* + |int_S F_lambda epsilon_X h_X| + |int_S F_lambda epsilon_X r_X|",
            "current_result": "bound_law_staged",
            "missing_for_claim": "numeric/source-backed norms for each term and units",
            "bound_if_missing": "first nonclaim source row stores these terms with valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "ETB1020_4_projector_bound",
            "statement": "The Hamiltonian/source projection is bounded by the edge charge bound once M_H_ref and Pi_M norm are owned.",
            "formula": "|Qbar_edge_XH(lambda)| <= ||Pi_M^H|| |Q_edge(lambda)| / M_H_ref_min",
            "current_result": "conditional_bound",
            "missing_for_claim": "Pi_M^H definition, M_H_ref_min, and source-backed Q_edge bound",
            "bound_if_missing": "Qbar_edge_XH remains MISSING_SOURCE_BACKED_QBAR_EDGE_XH",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "ETB1020_5_verdict",
            "statement": "1020 derives the exact local condition and fallback bound, but not the zero theorem.",
            "formula": "Q_edge=0 is conditional; Q_edge_bound is schema-ready; no claim is promoted",
            "current_result": "fail_current_claim_but_derivation_progress",
            "missing_for_claim": "B_X primitive, h_X/r_X zero or bounds, kernel derivative bound, corner audit, M_H_ref/Pi_M",
            "bound_if_missing": "move to 1021 B_X primitive or first numeric/source-bound term",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def bx_primitive_audit_rows() -> list[dict[str, str]]:
    rows = [
        {
            "audit_id": "BXP1020_0_parent_variation",
            "needed_object": "L_X and Theta_X",
            "test": "delta L_X = E_X delta X + d Theta_X with explicit boundary momentum P_X",
            "current_status": "MISSING_PARENT_INPUT",
            "reason": "1018 keeps L_X/Theta_X formula-written but not owned",
            "zero_route": "compute B_X from parent variation and show it is exact/pure gauge",
            "fallback_row": "b_X_norm;h_X_coeff;r_X_bound",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "BXP1020_1_boundary_counterterm",
            "needed_object": "B_ct and reference subtraction",
            "test": "B_X = n_mu P_X^{mu nu} + B_ct^nu is local/covariant and fixed before readout",
            "current_status": "MISSING_COUNTERTERM_OWNER",
            "reason": "1019 counterterm clause is not derived",
            "zero_route": "choose B_ct by parent variational principle, not by fitting R10",
            "fallback_row": "B_ct_source_path;Delta_symp_bound",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "BXP1020_2_exact_primitive",
            "needed_object": "b_X primitive",
            "test": "B_X - h_X = d_S b_X on the certified boundary domain",
            "current_status": "NOT_DERIVED",
            "reason": "no explicit primitive exists in current files",
            "zero_route": "write b_X from parent fields and prove global compatibility on overlap charts",
            "fallback_row": "b_X_norm with units and source path",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "BXP1020_3_harmonic_mode",
            "needed_object": "h_X harmonic edge class",
            "test": "project B_X onto H_edge and prove coefficient zero or bound it",
            "current_status": "MISSING_COHOMOLOGY_PROJECTION",
            "reason": "boundary cohomology class is not certified",
            "zero_route": "H_edge projection vanishes by parent boundary class/no-hair theorem",
            "fallback_row": "h_X_coeff_bound",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "BXP1020_4_verdict",
            "needed_object": "B_X exactness certificate",
            "test": "BXP1020_0 through BXP1020_3 all close",
            "current_status": "fail_current_claim",
            "reason": "B_X primitive is still the earliest hard obstruction",
            "zero_route": "1021 attacks explicit primitive from parent variation",
            "fallback_row": "EDGEBOUND1020 first row retained nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def first_source_bound_rows() -> list[dict[str, str]]:
    rows = [
        {
            "row_id": "EDGEBOUND1020_0_formal_bound_row",
            "system_id": "local_edge_branch_generic",
            "quantity": "Q_edge_bound(lambda)",
            "bound_formula": "C_corner + norm_dS_Feps * norm_bX + harmonic_edge_abs + residual_edge_abs",
            "lambda_status": "MISSING_EDGE_RANGE_OR_ENVELOPE",
            "C_corner": "MISSING_CORNER_AUDIT_OR_ZERO_CERTIFICATE",
            "norm_dS_Feps": "MISSING_KERNEL_DERIVATIVE_BOUND_OR_ZERO_CERTIFICATE",
            "norm_bX": "MISSING_BX_PRIMITIVE_NORM",
            "harmonic_edge_abs": "MISSING_H_EDGE_ZERO_OR_BOUND",
            "residual_edge_abs": "MISSING_PARENT_RESIDUAL_ZERO_OR_BOUND",
            "units": "MISSING_EDGE_CHARGE_UNITS",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1019_BOUNDARY_EXACTNESS_CLAUSES.csv;source-intake/mts_residuals/P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv",
            "current_status": "STAGED_SOURCE_BACKED_NONCLAIM_SCHEMA",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "row_id": "EDGEBOUND1020_1_projected_bound_row",
            "system_id": "local_edge_branch_generic",
            "quantity": "Qbar_edge_XH_bound(lambda)",
            "bound_formula": "PiM_norm * Q_edge_bound(lambda) / M_H_ref_min",
            "lambda_status": "INHERITS_EDGEBOUND1020_0",
            "C_corner": "INHERITS_EDGEBOUND1020_0",
            "norm_dS_Feps": "INHERITS_EDGEBOUND1020_0",
            "norm_bX": "INHERITS_EDGEBOUND1020_0",
            "harmonic_edge_abs": "INHERITS_EDGEBOUND1020_0",
            "residual_edge_abs": "INHERITS_EDGEBOUND1020_0",
            "units": "MISSING_DIMENSIONLESS_OR_DECLARED_UNITS",
            "source_paths": "source-intake/mts_residuals/P8_Y5_R10_1019_PROJECTOR_ORTHOGONALITY_CLAUSES.csv;source-intake/mts_residuals/P8_Y5_R10_1017_MHREF_FIRST_ROW_SCHEMA.csv",
            "current_status": "STAGED_SOURCE_BACKED_NONCLAIM_SCHEMA",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def route_rows() -> list[dict[str, str]]:
    rows = [
        {
            "route_id": "R1020_0_zero_by_closed_weight",
            "route": "closed boundary plus exact B_X plus closed F_lambda epsilon",
            "result": "conditional_only",
            "requires": "BDC1020_0, BDC1020_2, BDC1020_4, BXP1020_2, and h_X=r_X=0",
            "claim_effect": "would set Q_edge=0 and remove edge alpha branch",
            "current_blocker": "B_X primitive and cohomology/kernel certificates missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "R1020_1_zero_by_proper_gauge",
            "route": "epsilon_X proper gauge kills edge charge",
            "result": "closure_only",
            "requires": "proof that proper X gauge does not delete physical tau/mass/rotation charges",
            "claim_effect": "would set Q_edge=0 for representative directions",
            "current_blocker": "allowed epsilon domain not separated from physical Hamiltonian generators",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "R1020_2_bound_by_weighted_Stokes",
            "route": "finite edge residual bound from derivative/harmonic/corner terms",
            "result": "best_current_fallback",
            "requires": "EDGEBOUND1020_0 source values and units",
            "claim_effect": "would bound Q_edge and then Qbar_edge_XH rather than zeroing it",
            "current_blocker": "all numerical/source-bound terms are missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "R1020_3_verdict",
            "route": "boundary cohomology/domain checkpoint",
            "result": "fail_current_claim_but_narrows_gap",
            "requires": "either zero route signed or EDGEBOUND source rows filled",
            "claim_effect": "no R10/R11/local-GR pass from 1020",
            "current_blocker": "explicit B_X primitive remains the next hard object",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def claim_gate_rows() -> list[dict[str, str]]:
    rows = [
        ("CG1020_0_sources_registered", "1020 source chain exists", True, "all cited prior rows and surface precedent are found", False),
        ("CG1020_1_domain_certificate", "boundary domain/cohomology certificate", False, "surface, class, cohomology, epsilon, and kernel clauses are not parent-signed", False),
        ("CG1020_2_BX_primitive", "B_X exact primitive exists", False, "no explicit b_X from parent L_X/Theta_X/Q_X exists", False),
        ("CG1020_3_weighted_Stokes_zero", "weighted Stokes zero", False, "d_S(F_lambda epsilon_X)=0 and h_X=r_X=0 are not proved", False),
        ("CG1020_4_projector_bound", "Qbar_edge_XH bound", False, "M_H_ref, Pi_M norm, and Q_edge bound values are missing", False),
        ("CG1020_5_source_pack_first_row", "first source-pack bound row", True, "formal nonclaim row is staged with explicit missing terms and source paths", False),
        ("CG1020_6_R10_R11_claim", "R10/R11 pass", False, "no theorem-zero or numeric source-bound comparator row exists", False),
        ("CG1020_7_local_GR_claim", "local GR/Newton reduction", False, "boundary/source charge route remains open", False),
        ("CG1020_8_guardrail", "weighted-Stokes guardrail installed", True, "Stokes may not be used unless corner, harmonic, residual, and kernel derivative terms are zero or bounded", False),
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
            "decision_id": "DEC1020_0_derivation_result",
            "decision": "The exactness route is mathematically sharpened but not closed.",
            "because": "Weighted Stokes leaves corner, kernel-derivative, harmonic, and residual terms unless the parent boundary class supplies certificates.",
            "next_action": "derive explicit B_X primitive from parent variation or fill the bound terms",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1020_1_best_next_route",
            "decision": "The best derivation target is now the explicit B_X primitive.",
            "because": "Without b_X, both the zero theorem and the bound law lack their central object.",
            "next_action": "1021-Y5-R10-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1020_2_fallback_route",
            "decision": "If B_X cannot be derived, use the EDGEBOUND1020 source row rather than a closure axiom.",
            "because": "The residual can be bounded term-by-term with no cancellation between unknowns.",
            "next_action": "source C_corner, norm_dS_Feps, norm_bX, harmonic_edge_abs, residual_edge_abs, M_H_ref_min, and PiM_norm",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1020_3_current_status",
            "decision": "No R10/R11/local-GR claim is allowed, but the live gap is smaller.",
            "because": "The edge obstruction is reduced to a primitive/cohomology/kernel-bound problem.",
            "next_action": "attack B_X primitive first; if it fails, fill EDGEBOUND terms",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1021-Y5-R10-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md",
            "objective": "derive the explicit B_X primitive from parent L_X/Theta_X/Q_X and boundary counterterm, or fill the first EDGEBOUND1020 term with source-backed units",
            "include": "delta L_X boundary momentum, b_X primitive, h_X projection, r_X residual test, B_ct/reference rule, norm_bX, dS_Feps bound, corner certificate",
            "exclude": "symbolic B_X exactness, Stokes zero without closed weight, harmonic-mode silence by assumption, R10/R11 pass, local-GR claim, GitHub action",
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
    domain: list[dict[str, str]],
    theorem: list[dict[str, str]],
    bx_audit: list[dict[str, str]],
    first_rows: list[dict[str, str]],
    routes: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    domain_required = {"BDC1020_0_surface_manifold", "BDC1020_1_boundary_class", "BDC1020_2_relative_cohomology", "BDC1020_3_allowed_epsilon", "BDC1020_4_kernel_weight", "BDC1020_5_verdict"}
    theorem_required = {"ETB1020_0_decomposition", "ETB1020_1_weighted_Stokes_identity", "ETB1020_2_zero_conditions", "ETB1020_3_residual_bound", "ETB1020_4_projector_bound", "ETB1020_5_verdict"}
    bx_required = {"BXP1020_0_parent_variation", "BXP1020_1_boundary_counterterm", "BXP1020_2_exact_primitive", "BXP1020_3_harmonic_mode", "BXP1020_4_verdict"}
    checks = [
        ("V1020_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all source paths exist and expected needles are present"),
        ("V1020_1_domain_certificate_complete", domain_required.issubset({row["certificate_id"] for row in domain}), "domain certificate covers surface, class, cohomology, epsilon, kernel, and verdict"),
        ("V1020_2_domain_blocks_claim", any(row["certificate_id"] == "BDC1020_5_verdict" and row["current_status"] == "fail_current_claim" for row in domain), "domain certificate is not promoted"),
        ("V1020_3_weighted_stokes_written", theorem_required.issubset({row["theorem_id"] for row in theorem}) and any(row["theorem_id"] == "ETB1020_1_weighted_Stokes_identity" for row in theorem), "weighted Stokes identity and residual bound are written"),
        ("V1020_4_zero_not_promoted", any(row["theorem_id"] == "ETB1020_5_verdict" and row["current_result"] == "fail_current_claim_but_derivation_progress" for row in theorem), "zero theorem remains conditional only"),
        ("V1020_5_BX_audit_complete", bx_required.issubset({row["audit_id"] for row in bx_audit}), "B_X primitive audit covers parent variation, counterterm, primitive, harmonic, and verdict"),
        ("V1020_6_first_bound_rows_staged", {row["row_id"] for row in first_rows} == {"EDGEBOUND1020_0_formal_bound_row", "EDGEBOUND1020_1_projected_bound_row"}, "first source-pack bound rows are staged"),
        ("V1020_7_first_bound_rows_nonclaim", all(row["valid_for_claim"] == "false" and "MISSING" in ';'.join(row.values()) for row in first_rows), "first source-pack rows remain nonclaim with explicit missing terms"),
        ("V1020_8_routes_block_claim", any(row["route_id"] == "R1020_3_verdict" and row["result"] == "fail_current_claim_but_narrows_gap" for row in routes), "route verdict blocks claim while narrowing gap"),
        ("V1020_9_claim_gates_blocked", all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in gates), "all claim gates are nonclaim"),
        ("V1020_10_guardrail_written", any(row["gate_id"] == "CG1020_8_guardrail" and flag(row["gate_pass"]) for row in gates), "weighted-Stokes guardrail is installed"),
        ("V1020_11_decision_written", any(row["decision_id"] == "DEC1020_1_best_next_route" for row in decisions), "1021 best-route decision is written"),
        ("V1020_12_next_target_written", len(next_target) == 1 and "1021-Y5-R10-BX-primitive" in next_target[0]["next_target"], "1021 next target row is present"),
        ("V1020_13_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1020_SUMMARY", "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail", "detail": "1020 boundary cohomology/domain and weighted-Stokes validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    domain: list[dict[str, str]],
    theorem: list[dict[str, str]],
    bx_audit: list[dict[str, str]],
    first_rows: list[dict[str, str]],
    routes: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1020 Y5 R10 boundary cohomology domain certificate or source pack first row",
            "",
            "**Status:** The boundary route has been sharpened into a weighted-Stokes theorem. `Q_edge=0` needs a closed/corner-free domain, no harmonic or residual edge class, an explicit `B_X=d_S b_X`, and `d_S(F_lambda epsilon_X)=0`; otherwise the residual is bounded term-by-term rather than erased.",
            "",
            "**Claim ceiling:** no `Q_edge=0`, `Qbar_edge_XH=0`, R10/R11 pass, Newton/local-GR reduction, PPN pass, or edge-source cancellation claim is allowed from 1020.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Boundary domain certificate",
            md_table(domain, ["certificate_id", "object", "required_certificate", "mathematical_test", "current_status", "failure_if_missing", "feeds", "valid_for_claim"]),
            "## Weighted-Stokes theorem and bound",
            md_table(theorem, ["theorem_id", "statement", "formula", "current_result", "missing_for_claim", "bound_if_missing", "valid_for_claim"]),
            "## B_X primitive audit",
            md_table(bx_audit, ["audit_id", "needed_object", "test", "current_status", "reason", "zero_route", "fallback_row", "valid_for_claim"]),
            "## First source-pack bound row",
            md_table(first_rows, ["row_id", "system_id", "quantity", "bound_formula", "lambda_status", "C_corner", "norm_dS_Feps", "norm_bX", "harmonic_edge_abs", "residual_edge_abs", "units", "current_status", "valid_for_claim"]),
            "## Route verdicts",
            md_table(routes, ["route_id", "route", "result", "requires", "claim_effect", "current_blocker", "valid_for_claim"]),
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
    domain = domain_certificate_rows()
    theorem = exactness_theorem_rows()
    bx_audit = bx_primitive_audit_rows()
    first_rows = first_source_bound_rows()
    routes = route_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, domain, theorem, bx_audit, first_rows, routes, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1020_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1020_BOUNDARY_DOMAIN_CERTIFICATE.csv", domain)
    write_csv(OUT / "P8_Y5_R10_1020_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv", theorem)
    write_csv(OUT / "P8_Y5_R10_1020_BX_PRIMITIVE_AUDIT.csv", bx_audit)
    write_csv(OUT / "P8_Y5_R10_1020_SOURCE_PACK_FIRST_BOUND_ROW.csv", first_rows)
    write_csv(OUT / "P8_Y5_R10_1020_ROUTE_VERDICTS.csv", routes)
    write_csv(OUT / "P8_Y5_R10_1020_CLAIM_GATES.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1020_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1020_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1020_VALIDATION.csv", validations)
    write_doc(sources, domain, theorem, bx_audit, first_rows, routes, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()
