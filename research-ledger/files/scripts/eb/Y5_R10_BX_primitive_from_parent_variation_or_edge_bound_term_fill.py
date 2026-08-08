from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1021-Y5-R10-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md"
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
        ("SRC1021_0_1020_next", "source-intake/mts_residuals/P8_Y5_R10_1020_NEXT_TARGET.csv", "BX-primitive", "1020 handoff to B_X primitive or bound-term fill."),
        ("SRC1021_1_1020_stokes", "source-intake/mts_residuals/P8_Y5_R10_1020_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv", "ETB1020_3_residual_bound", "1020 weighted-Stokes bound law."),
        ("SRC1021_2_1020_audit", "source-intake/mts_residuals/P8_Y5_R10_1020_BX_PRIMITIVE_AUDIT.csv", "BXP1020_2_exact_primitive", "1020 B_X primitive obstruction."),
        ("SRC1021_3_1020_first_row", "source-intake/mts_residuals/P8_Y5_R10_1020_SOURCE_PACK_FIRST_BOUND_ROW.csv", "EDGEBOUND1020_0_formal_bound_row", "1020 first edge-bound row."),
        ("SRC1021_4_667_variation", "source-intake/mts_residuals/P8_Y5_R10_667_VARIATION_LEDGER.csv", "VL667_0_total_variation", "667 parent variation ledger."),
        ("SRC1021_5_667_action", "source-intake/mts_residuals/P8_Y5_R10_667_PARENT_BOUNDARY_ACTION_ANSATZ.csv", "PBA667_1_bulk_action", "667 parent/boundary action ansatz."),
        ("SRC1021_6_667_fallback", "source-intake/mts_residuals/P8_Y5_R10_667_RESIDUAL_FALLBACK_ROWS.csv", "RF667_0_LX_theta_Qtau_owner", "667 missing L_X/Theta/Q owner row."),
        ("SRC1021_7_669_candidates", "source-intake/mts_residuals/P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv", "LX669_1_vertical_constraint", "669 vertical constraint candidate."),
        ("SRC1021_8_669_scalar", "source-intake/mts_residuals/P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv", "LX669_2_positive_sourcefree_massive", "669 scalar-like positive source-free branch."),
        ("SRC1021_9_669_variation", "source-intake/mts_residuals/P8_Y5_R10_669_THETA_QX_VARIATION_LEDGER.csv", "V669_0_variation", "669 Theta/QX variation ledger."),
        ("SRC1021_10_583_contract", "source-intake/mts_residuals/P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv", "NMC583_3_momentum_map", "583 momentum-map contract."),
        ("SRC1021_11_583_owner", "source-intake/mts_residuals/P8_Y5_R10_583_PARENT_MOMENTUM_MAP_OWNER_ATTEMPT.csv", "OMA583_1_noether_current_owner", "583 Noether-current owner route."),
        ("SRC1021_12_591_boundary", "source-intake/mts_residuals/P8_Y5_R10_591_DCDAGGER_FORMULA.csv", "DCA591_3_boundary_adjoint", "591 DCdagger boundary adjoint."),
        ("SRC1021_13_591_comparison", "source-intake/mts_residuals/P8_Y5_R10_591_OMEGA_DCDAGGER_COMPARISON.csv", "CMP591_4_boundary", "591 Omega/DCdagger boundary comparison."),
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


def parent_variation_template_rows() -> list[dict[str, str]]:
    rows = [
        {
            "template_id": "PVT1021_0_parent_first_variation",
            "object": "parent X-sector first variation",
            "formula": "delta L_X = E_A^X delta X^A + d Theta_X(Phi,delta X)",
            "closure_test": "L_X, field normalization, boundary class, and Theta_X are supplied by one parent action",
            "current_status": "formula_known_not_owned",
            "implication": "without this, no B_X primitive can be computed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "template_id": "PVT1021_1_vertical_Noether_route",
            "object": "vertical/gauge branch",
            "formula": "delta_epsilon X^A=R_i^A epsilon^i + R_i^{A mu} nabla_mu epsilon^i; J_epsilon=Theta_X(delta_epsilon X)-mu_epsilon=dQ_epsilon+epsilon C_X",
            "closure_test": "vertical generator, mu_epsilon, C_X, Q_epsilon, and differentiable G[epsilon] are all parent-derived",
            "current_status": "contract_only",
            "implication": "if closed, Q_edge is a Noether surface term that can be tested for exactness/proper-gauge silence",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "template_id": "PVT1021_2_boundary_covector",
            "object": "boundary adjoint covector",
            "formula": "B_DC[X,deltaY]=-int_S n_mu X_nu delta P^{mu nu}+delta Q_X + density/reference terms",
            "closure_test": "delta Q_X cancels B_DC or leaves a fixed exact/proper edge primitive",
            "current_status": "formal_shape_from_591_not_cancelled",
            "implication": "uncancelled B_DC is the concrete source of B_X edge leakage",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "template_id": "PVT1021_3_BX_definition",
            "object": "edge boundary momentum",
            "formula": "B_X := i_S^*(n_mu P_X^{mu nu} epsilon_nu + B_ct[epsilon]) as a surface top form",
            "closure_test": "P_X and B_ct come from the same parent variation/reference rule",
            "current_status": "definition_staged",
            "implication": "B_X is now computable only after P_X/B_ct ownership",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "template_id": "PVT1021_4_hodge_decomposition",
            "object": "surface decomposition",
            "formula": "B_X=d_S b_X + h_X + r_X on S_edge",
            "closure_test": "r_X=0, h_X=0 or bounded, and b_X is globally compatible across charts",
            "current_status": "decomposition_contract",
            "implication": "this is the exact bridge from parent variation to 1020 weighted-Stokes bound",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "template_id": "PVT1021_5_verdict",
            "object": "parent variation to primitive map",
            "formula": "parent L_X/Theta_X/Q_X -> P_X,B_ct -> B_X -> d_S b_X+h_X+r_X -> Q_edge bound",
            "closure_test": "every arrow is source-backed or theorem-zero",
            "current_status": "map_written_not_closed",
            "implication": "B_X primitive is not derived in current MTS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def primitive_gate_rows() -> list[dict[str, str]]:
    rows = [
        {
            "gate_id": "BXG1021_0_same_parent_origin",
            "primitive_requirement": "P_X, J_X, Theta_X, Q_X, and Omega_X all come from one parent L_X",
            "test": "compare P/J adjoint, Noether current, and Omega-flat vertical generator from the same action",
            "current_result": "fail_current_claim",
            "blocker": "667/669/583/591 all keep parent ownership missing",
            "if_passes": "B_X becomes a derived object rather than an inserted boundary term",
            "if_fails": "retain EDGEBOUND1020 terms",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "BXG1021_1_counterterm_owner",
            "primitive_requirement": "B_ct is fixed by differentiability/reference principle before readout",
            "test": "delta(Q_X+B_ct)-i_epsilon Theta_X has no uncancelled boundary covector",
            "current_result": "not_derived",
            "blocker": "B_ct/reference branch is named but not selected by parent principle",
            "if_passes": "r_X can be reduced or set to zero",
            "if_fails": "residual_edge_abs remains live",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "BXG1021_2_exact_surface_pullback",
            "primitive_requirement": "i_S^*B_X-h_X is exact on S_edge",
            "test": "construct b_X with B_X-h_X=d_S b_X and verify overlap compatibility",
            "current_result": "not_derived",
            "blocker": "no explicit P_X/B_ct means no global primitive can be built",
            "if_passes": "norm_bX becomes computable and Stokes route becomes meaningful",
            "if_fails": "norm_bX/h_X/r_X source rows required",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "BXG1021_3_harmonic_zero",
            "primitive_requirement": "harmonic edge class vanishes or is bounded",
            "test": "Pi_Hedge[B_X]=0, or h_X_coeff_bound is source-backed",
            "current_result": "missing_cohomology_projection",
            "blocker": "boundary class/no-hair certificate is unsigned",
            "if_passes": "harmonic_edge_abs can be zero",
            "if_fails": "harmonic_edge_abs row required",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "BXG1021_4_kernel_norm",
            "primitive_requirement": "d_S(F_lambda epsilon_X) is zero or bounded",
            "test": "closed weight on S_edge, or source-backed norm_dS_Feps",
            "current_result": "not_filled",
            "blocker": "edge geometry and lambda support are not specified",
            "if_passes": "weighted-Stokes derivative term is controlled",
            "if_fails": "norm_dS_Feps row required",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "BXG1021_5_verdict",
            "primitive_requirement": "B_X primitive closure",
            "test": "BXG1021_0 through BXG1021_4 close together",
            "current_result": "fail_current_claim",
            "blocker": "current corpus has a contract but no parent-signed primitive",
            "if_passes": "Q_edge theorem or bound becomes executable",
            "if_fails": "source-bound fill becomes mandatory",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def scalar_branch_rows() -> list[dict[str, str]]:
    rows = [
        {
            "branch_id": "SB1021_0_scalar_like_LX",
            "branch": "positive scalar-like physical X",
            "formula": "L_X=1/2 sqrt(h)(Z_X |grad X|^2 + M_X^2 X^2)-sqrt(h) X J_X",
            "boundary_result": "Theta_X ~ Z_X delta X * dX; boundary flux can vanish under Dirichlet/Neumann/no-hair conditions",
            "warning": "this is not a Noether edge-charge primitive unless X also has a gauge/vertical symmetry",
            "status": "conditional_route_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "branch_id": "SB1021_1_scalar_boundary_condition",
            "branch": "Dirichlet/Neumann exterior silence",
            "formula": "delta X|S=0 or n.grad X|S=0 plus positive operator and J_X=0",
            "boundary_result": "can kill boundary flux for a chosen boundary-value problem",
            "warning": "a boundary condition is not a derived local-GR theorem unless parent action selects it for all local systems",
            "status": "not_promoted",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "branch_id": "SB1021_2_scalar_source_route",
            "branch": "sourced scalar residual",
            "formula": "O_X X=J_X, lambda_X=sqrt(Z_X/M_X^2), alpha_X=K_X Qbar_XH qbar_XT",
            "boundary_result": "edge primitive route becomes secondary; bulk/source coefficients dominate local tests",
            "warning": "if J_X or matter coupling is nonzero, R10/R11 must be scored",
            "status": "retained_residual_vector",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "branch_id": "SB1021_3_scalar_verdict",
            "branch": "scalar-like branch effect",
            "formula": "scalar-like X does not naturally provide Q_edge=0; it either needs source-free no-hair or source coefficients",
            "boundary_result": "no boundary-zero claim from scalar boundary conditions alone",
            "warning": "do not mix gauge-edge proof language with scalar no-hair proof language",
            "status": "separates_routes",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def edge_bound_fill_rows() -> list[dict[str, str]]:
    rows = [
        {
            "fill_id": "EBF1021_0_norm_bX",
            "quantity": "norm_bX",
            "definition": "dual norm of the primitive b_X entering |int_S d_S(F epsilon) wedge b_X|",
            "required_source": "explicit b_X from P_X/B_ct or a theorem-bound on b_X",
            "current_status": "MISSING_BX_PRIMITIVE_NORM",
            "units": "MISSING_EDGE_PRIMITIVE_UNITS",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1020_SOURCE_PACK_FIRST_BOUND_ROW.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "EBF1021_1_harmonic_edge_abs",
            "quantity": "harmonic_edge_abs",
            "definition": "absolute harmonic/cohomology contribution |int_S F epsilon h_X|",
            "required_source": "H_edge projection of B_X or no-hair theorem",
            "current_status": "MISSING_H_EDGE_ZERO_OR_BOUND",
            "units": "MISSING_EDGE_CHARGE_UNITS",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1020_SOURCE_PACK_FIRST_BOUND_ROW.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "EBF1021_2_residual_edge_abs",
            "quantity": "residual_edge_abs",
            "definition": "absolute residual non-exact/non-harmonic boundary contribution |int_S F epsilon r_X|",
            "required_source": "proof r_X=0 or a source-backed bound",
            "current_status": "MISSING_PARENT_RESIDUAL_ZERO_OR_BOUND",
            "units": "MISSING_EDGE_CHARGE_UNITS",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1020_SOURCE_PACK_FIRST_BOUND_ROW.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "EBF1021_3_norm_dS_Feps",
            "quantity": "norm_dS_Feps",
            "definition": "surface derivative norm of F_lambda epsilon_X over the selected edge geometry",
            "required_source": "edge geometry, lambda support, and allowed epsilon_X domain",
            "current_status": "MISSING_KERNEL_DERIVATIVE_BOUND_OR_ZERO_CERTIFICATE",
            "units": "MISSING_INVERSE_LENGTH_OR_DECLARED_DUAL_UNITS",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1020_SOURCE_PACK_FIRST_BOUND_ROW.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "EBF1021_4_corner",
            "quantity": "C_corner",
            "definition": "absolute corner contribution if the edge surface has a boundary or joints",
            "required_source": "corner-free certificate or corner charge bound",
            "current_status": "MISSING_CORNER_AUDIT_OR_ZERO_CERTIFICATE",
            "units": "MISSING_EDGE_CHARGE_UNITS",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1020_SOURCE_PACK_FIRST_BOUND_ROW.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fill_id": "EBF1021_5_verdict",
            "quantity": "EDGEBOUND1020 fillability",
            "definition": "first executable edge-bound row requires all EBF1021_0 through EBF1021_4",
            "required_source": "primitive or numeric/source-backed bound for every term",
            "current_status": "not_fillable_currently",
            "units": "mixed_missing_units",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1020_SOURCE_PACK_FIRST_BOUND_ROW.csv",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def route_rows() -> list[dict[str, str]]:
    rows = [
        {
            "route_id": "R1021_0_vertical_gauge_primitive",
            "route": "derive B_X from vertical Noether/momentum-map generator",
            "status": "best_clean_derivation_route_not_closed",
            "evidence": "583 and 591 give the exact contract, but parent theta/Omega/P/J are missing",
            "next_step": "construct parent L_X or prove X is absent from quotient before variation",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "R1021_1_scalar_nohair_route",
            "route": "treat X as scalar-like positive source-free branch",
            "status": "separate_conditional_route",
            "evidence": "669 positive source-free branch can kill exterior X only with Z_X>0, M_X^2>0, J_X=0, and boundary_flux=0",
            "next_step": "do not call this Q_edge exactness; prove no-hair/source-free instead",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "R1021_2_edge_bound_fill",
            "route": "fill EDGEBOUND1020 term-by-term",
            "status": "fallback_schema_ready",
            "evidence": "1020 gives the bound law, but every term is missing",
            "next_step": "first fill norm_bX only after b_X exists; otherwise fill corner/kernel geometry terms",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "route_id": "R1021_3_verdict",
            "route": "B_X primitive checkpoint",
            "status": "fail_current_claim_but_splits_routes",
            "evidence": "current MTS lacks parent-signed B_X primitive; scalar branch is not an edge-charge theorem",
            "next_step": "1022 should pick quotient/vertical L_X construction or scalar no-hair/source-free proof, not mix them",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def claim_gate_rows() -> list[dict[str, str]]:
    rows = [
        ("CG1021_0_sources_registered", "1021 source chain exists", True, "all cited prior ledgers and contracts are found", False),
        ("CG1021_1_parent_variation_owned", "parent L_X/Theta_X/Q_X variation owned", False, "current corpus has contracts but no parent-signed sector variation", False),
        ("CG1021_2_BX_primitive_derived", "B_X=d_S b_X+h_X+r_X derived", False, "P_X/B_ct/b_X are not constructed", False),
        ("CG1021_3_harmonic_or_residual_zero", "h_X=r_X=0", False, "boundary cohomology/no-hair and residual zero are missing", False),
        ("CG1021_4_scalar_branch_silence", "scalar-like branch local silence", False, "Z_X, M_X^2, J_X=0, and boundary_flux=0 are not parent-signed", False),
        ("CG1021_5_edge_bound_executable", "EDGEBOUND1020 executable", False, "norm_bX, harmonic, residual, kernel, corner, and units are missing", False),
        ("CG1021_6_R10_R11_claim", "R10/R11 pass", False, "no primitive theorem or numeric edge/bulk source row exists", False),
        ("CG1021_7_local_GR_claim", "local GR/Newton reduction", False, "extra-sector local silence remains unproved", False),
        ("CG1021_8_route_separation_guardrail", "route separation guardrail installed", True, "gauge-edge proof, scalar no-hair proof, and source-bound fallback are separated", False),
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
            "decision_id": "DEC1021_0_primitive_result",
            "decision": "The explicit B_X primitive is not derivable from current files.",
            "because": "The parent L_X/Theta_X/Q_X/P_X/B_ct chain is a contract, not a signed variation.",
            "next_action": "do not claim Q_edge zero; select the next parent route",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1021_1_route_split",
            "decision": "The gauge-edge route and scalar no-hair route must be separated.",
            "because": "A scalar-like positive operator can kill X by source-free no-hair, but it does not automatically supply a Noether edge primitive.",
            "next_action": "choose absent/vertical quotient construction or scalar source-free theorem as the next attack",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1021_2_best_next",
            "decision": "The least-scrutiny route is the quotient/vertical construction if it can be built.",
            "because": "It removes the local pole before fitting; the scalar route keeps source/current coefficients under R10/R11 pressure.",
            "next_action": "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1021_3_fallback",
            "decision": "If no quotient/vertical construction closes, fill EDGEBOUND and bulk scalar coefficients.",
            "because": "Then the theory must survive as a bounded residual, not a theorem-zero local-GR branch.",
            "next_action": "fill EBF1021 terms plus Z_X/M_X2/J_X/K_X/Qbar/qbar rows",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
            "objective": "choose and test the least-scrutiny local branch: construct X as absent/vertical quotient before variation, or demote to scalar positive no-hair/source-coefficient route",
            "include": "q map, vertical generator, parent L_X absence/constraint form, first-class boundary silence, scalar Z_X/M_X2/J_X branch, no-hair theorem, EDGEBOUND fallback",
            "exclude": "mixing scalar no-hair with Noether edge primitive, symbolic B_X exactness, source-free by assertion, R10/R11 pass, local-GR claim, GitHub action",
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
    templates: list[dict[str, str]],
    primitive_gates: list[dict[str, str]],
    scalar_branch: list[dict[str, str]],
    edge_bound_fill: list[dict[str, str]],
    routes: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    changed = formalization_changed_after_start()
    template_required = {"PVT1021_0_parent_first_variation", "PVT1021_1_vertical_Noether_route", "PVT1021_2_boundary_covector", "PVT1021_3_BX_definition", "PVT1021_4_hodge_decomposition", "PVT1021_5_verdict"}
    primitive_required = {"BXG1021_0_same_parent_origin", "BXG1021_1_counterterm_owner", "BXG1021_2_exact_surface_pullback", "BXG1021_3_harmonic_zero", "BXG1021_4_kernel_norm", "BXG1021_5_verdict"}
    scalar_required = {"SB1021_0_scalar_like_LX", "SB1021_1_scalar_boundary_condition", "SB1021_2_scalar_source_route", "SB1021_3_scalar_verdict"}
    fill_required = {"EBF1021_0_norm_bX", "EBF1021_1_harmonic_edge_abs", "EBF1021_2_residual_edge_abs", "EBF1021_3_norm_dS_Feps", "EBF1021_4_corner", "EBF1021_5_verdict"}
    checks = [
        ("V1021_0_sources_exist", all(flag(row["exists"]) and flag(row["needle_found"]) for row in sources), "all source paths exist and expected needles are present"),
        ("V1021_1_template_complete", template_required.issubset({row["template_id"] for row in templates}), "parent variation to B_X primitive map is complete"),
        ("V1021_2_template_nonclaim", any(row["template_id"] == "PVT1021_5_verdict" and row["current_status"] == "map_written_not_closed" for row in templates), "template is not promoted to primitive"),
        ("V1021_3_primitive_gates_complete", primitive_required.issubset({row["gate_id"] for row in primitive_gates}), "primitive gates cover same-parent, counterterm, exact pullback, harmonic, kernel, and verdict"),
        ("V1021_4_primitive_blocks_claim", any(row["gate_id"] == "BXG1021_5_verdict" and row["current_result"] == "fail_current_claim" for row in primitive_gates), "B_X primitive remains blocked"),
        ("V1021_5_scalar_branch_separated", scalar_required.issubset({row["branch_id"] for row in scalar_branch}) and any(row["branch_id"] == "SB1021_3_scalar_verdict" for row in scalar_branch), "scalar no-hair route is separated from edge Noether route"),
        ("V1021_6_edge_bound_fill_complete", fill_required.issubset({row["fill_id"] for row in edge_bound_fill}), "EDGEBOUND fill schema covers primitive, harmonic, residual, kernel, corner, and verdict"),
        ("V1021_7_edge_bound_nonclaim", all(row["valid_for_claim"] == "false" and ("MISSING" in row["current_status"] or row["current_status"] == "not_fillable_currently") for row in edge_bound_fill), "edge-bound fill rows remain nonclaim"),
        ("V1021_8_route_verdict_blocks", any(row["route_id"] == "R1021_3_verdict" and row["status"] == "fail_current_claim_but_splits_routes" for row in routes), "route verdict blocks claim and splits branch choices"),
        ("V1021_9_claim_gates_blocked", all(not flag(row["claim_allowed"]) and not flag(row["valid_for_claim"]) for row in gates), "all claim gates are nonclaim"),
        ("V1021_10_guardrail_written", any(row["gate_id"] == "CG1021_8_route_separation_guardrail" and flag(row["gate_pass"]) for row in gates), "route separation guardrail is installed"),
        ("V1021_11_decision_written", any(row["decision_id"] == "DEC1021_2_best_next" for row in decisions), "1022 branch-choice decision is written"),
        ("V1021_12_next_target_written", len(next_target) == 1 and "1022-Y5-R10-vertical-quotient" in next_target[0]["next_target"], "1022 next target row is present"),
        ("V1021_13_formalization_untouched", len(changed) == 0, f"formalization-workbench modified-file count since script start is {len(changed)}"),
    ]
    rows = [{"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()} for check_id, passed, detail in checks]
    rows.insert(0, {"check_id": "V1021_SUMMARY", "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail", "detail": "1021 B_X primitive and branch-separation validation summary", "generated_utc": stamp()})
    return rows


def write_doc(
    sources: list[dict[str, str]],
    templates: list[dict[str, str]],
    primitive_gates: list[dict[str, str]],
    scalar_branch: list[dict[str, str]],
    edge_bound_fill: list[dict[str, str]],
    routes: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1021 Y5 R10 B_X primitive from parent variation or edge bound term fill",
            "",
            "**Status:** The `B_X` primitive is not derivable from current files. The parent variation map is now explicit, but `L_X/Theta_X/Q_X/P_X/B_ct` are still contracts rather than a signed parent action. The scalar-like branch is also separated from the Noether edge-charge route.",
            "",
            "**Claim ceiling:** no `B_X=d_S b_X`, no `Q_edge=0`, no scalar local silence, no R10/R11 pass, no PPN pass, and no local-GR/Newton reduction is allowed from 1021.",
            "",
            "## Source register",
            md_table(sources, ["source_id", "source_path", "exists", "needle_found", "role"]),
            "## Parent variation template",
            md_table(templates, ["template_id", "object", "formula", "closure_test", "current_status", "implication", "valid_for_claim"]),
            "## B_X primitive gates",
            md_table(primitive_gates, ["gate_id", "primitive_requirement", "test", "current_result", "blocker", "if_passes", "if_fails", "valid_for_claim"]),
            "## Scalar-like branch separation",
            md_table(scalar_branch, ["branch_id", "branch", "formula", "boundary_result", "warning", "status", "valid_for_claim"]),
            "## Edge-bound fill schema",
            md_table(edge_bound_fill, ["fill_id", "quantity", "definition", "required_source", "current_status", "units", "source_path", "valid_for_claim"]),
            "## Route verdicts",
            md_table(routes, ["route_id", "route", "status", "evidence", "next_step", "claim_allowed", "valid_for_claim"]),
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
    templates = parent_variation_template_rows()
    primitive_gates = primitive_gate_rows()
    scalar_branch = scalar_branch_rows()
    edge_bound_fill = edge_bound_fill_rows()
    routes = route_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validations = validation_rows(sources, templates, primitive_gates, scalar_branch, edge_bound_fill, routes, gates, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_1021_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_1021_PARENT_VARIATION_TEMPLATE.csv", templates)
    write_csv(OUT / "P8_Y5_R10_1021_BX_PRIMITIVE_GATES.csv", primitive_gates)
    write_csv(OUT / "P8_Y5_R10_1021_SCALAR_BRANCH_SEPARATION.csv", scalar_branch)
    write_csv(OUT / "P8_Y5_R10_1021_EDGE_BOUND_FILL_SCHEMA.csv", edge_bound_fill)
    write_csv(OUT / "P8_Y5_R10_1021_ROUTE_VERDICTS.csv", routes)
    write_csv(OUT / "P8_Y5_R10_1021_CLAIM_GATES.csv", gates)
    write_csv(OUT / "P8_Y5_R10_1021_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_1021_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_1021_VALIDATION.csv", validations)
    write_doc(sources, templates, primitive_gates, scalar_branch, edge_bound_fill, routes, gates, decisions, next_target, validations)


if __name__ == "__main__":
    main()
