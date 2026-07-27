from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_parent_Omega_DCX_boundary_charge_owner_attempted_formal_Omega_DCX_available_single_parent_owner_and_boundary_zero_unsigned_edge_residual_vector_retained_nonclaim"
CLAIM_CEILING = "Omega_DCX_boundary_owner_audit_and_edge_vector_only_no_KX_zero_no_Qbar_zero_no_R10_no_R11_no_local_GR_claim"
NEXT_TARGET = "672-Y5-R10-boundary-exactness-projector-orthogonality-or-edge-coefficient-source-plan.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "671-Y5-R10-parent-Omega-DCX-boundary-charge-owner-or-edge-residual-vector.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "583_doc": ROOT / "583-Y5-R10-parent-momentum-map-owner-or-edge-residual-demotion.md",
    "583_validation": RESIDUALS / "P8_Y5_BRR545_583_VALIDATION.csv",
    "583_contract": RESIDUALS / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv",
    "583_owner_attempt": RESIDUALS / "P8_Y5_R10_583_PARENT_MOMENTUM_MAP_OWNER_ATTEMPT.csv",
    "583_edge": RESIDUALS / "P8_Y5_R10_583_EDGE_RESIDUAL_DEMOTION.csv",
    "583_owner_gates": RESIDUALS / "P8_Y5_R10_583_OWNER_GATE_STATUS.csv",
    "584_doc": ROOT / "584-Y5-R10-edge-residual-alpha-envelope-or-owner-repair.md",
    "584_validation": RESIDUALS / "P8_Y5_BRR545_584_VALIDATION.csv",
    "584_edge_law": RESIDUALS / "P8_Y5_R10_584_EDGE_ENVELOPE_LAW.csv",
    "584_input_contract": RESIDUALS / "P8_Y5_R10_584_EDGE_CLAIM_INPUT_CONTRACT.csv",
    "584_owner_repair": RESIDUALS / "P8_Y5_R10_584_OWNER_REPAIR_ATTEMPT.csv",
    "589_doc": ROOT / "589-Y5-R10-adjoint-zero-mode-certificate-or-source-backed-edge-product-row.md",
    "589_validation": RESIDUALS / "P8_Y5_BRR545_589_VALIDATION.csv",
    "589_required_sources": RESIDUALS / "P8_Y5_R10_589_SOURCES_REQUIRED_TO_CLOSE_CERTIFICATE.csv",
    "589_edge_template": RESIDUALS / "P8_Y5_R10_589_SOURCE_BACKED_EDGE_PRODUCT_ROW_TEMPLATE.csv",
    "590_doc": ROOT / "590-Y5-R10-map-DCdagger-to-vertical-generator-or-fill-edge-row-source.md",
    "590_dc_map": RESIDUALS / "P8_Y5_R10_590_DCDAGGER_VERTICAL_MAP.csv",
    "590_field_map": RESIDUALS / "P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv",
    "591_doc": ROOT / "591-Y5-R10-parent-Omega-and-DC-operator-fill-or-edge-row-source-input.md",
    "591_validation": RESIDUALS / "P8_Y5_BRR545_591_VALIDATION.csv",
    "591_omega": RESIDUALS / "P8_Y5_R10_591_PARENT_OMEGA_CANDIDATE.csv",
    "591_dc": RESIDUALS / "P8_Y5_R10_591_DC_OPERATOR_FORMULA.csv",
    "591_comparison": RESIDUALS / "P8_Y5_R10_591_OMEGA_DCDAGGER_COMPARISON.csv",
    "591_edge_status": RESIDUALS / "P8_Y5_R10_591_EDGE_SOURCE_INPUT_STATUS.csv",
    "592_doc": ROOT / "592-Y5-R10-fill-PJ-parent-origin-or-source-backed-edge-coefficients.md",
    "592_validation": RESIDUALS / "P8_Y5_BRR545_592_VALIDATION.csv",
    "592_noether": RESIDUALS / "P8_Y5_R10_592_NOETHER_PJ_ORIGIN_FORMULA.csv",
    "592_pj_attempt": RESIDUALS / "P8_Y5_R10_592_PJ_PARENT_ORIGIN_ATTEMPT.csv",
    "592_ambiguity": RESIDUALS / "P8_Y5_R10_592_IMPROVEMENT_AMBIGUITY_GATE.csv",
    "593_doc": ROOT / "593-Y5-R10-parent-Lagrangian-theta-vX-minimal-fill-or-edge-coefficients.md",
    "593_validation": RESIDUALS / "P8_Y5_BRR545_593_VALIDATION.csv",
    "593_candidates": RESIDUALS / "P8_Y5_R10_593_MINIMAL_PARENT_FILL_CANDIDATES.csv",
    "593_pj_test": RESIDUALS / "P8_Y5_R10_593_PJ_EXTRACTION_TEST.csv",
    "670_doc": ROOT / "670-Y5-R10-no-pole-quotient-LX-route-or-positive-sourcefree-operator-proof.md",
    "670_validation": RESIDUALS / "P8_Y5_BRR545_670_VALIDATION.csv",
    "670_vertical": RESIDUALS / "P8_Y5_R10_670_VERTICAL_GENERATOR_CERTIFICATE.csv",
    "670_effect": RESIDUALS / "P8_Y5_R10_670_R10_R11_ZERO_OR_RESIDUAL_EFFECT.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for path in FORMALIZATION_WORKBENCH.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def validation_failures_for(source_id: str) -> list[dict[str, str]]:
    return [row for row in read_csv(SOURCE_PATHS[source_id]) if row.get("result") != "pass"]


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "583_doc": "parent momentum-map owner / edge demotion fork",
        "583_validation": "583 validation gate",
        "583_contract": "Noether momentum-map contract",
        "583_owner_attempt": "parent momentum-map owner attempts",
        "583_edge": "edge residual demotion definitions",
        "583_owner_gates": "owner gate status",
        "584_doc": "edge residual envelope and owner-repair contract",
        "584_validation": "584 validation gate",
        "584_edge_law": "edge alpha envelope law",
        "584_input_contract": "edge claim input contract",
        "584_owner_repair": "owner repair routes",
        "589_doc": "adjoint zero-mode certificate / edge product row",
        "589_validation": "589 validation gate",
        "589_required_sources": "sources required to close adjoint certificate",
        "589_edge_template": "source-backed edge product template",
        "590_doc": "DCdagger to Omega-flat vertical generator map",
        "590_dc_map": "DCdagger map rows",
        "590_field_map": "field-by-field vertical action map",
        "591_doc": "parent Omega and DC operator fill",
        "591_validation": "591 validation gate",
        "591_omega": "parent Omega candidate rows",
        "591_dc": "DC operator formula rows",
        "591_comparison": "Omega/DCdagger comparison rows",
        "591_edge_status": "edge source input status rows",
        "592_doc": "Noether P/J parent-origin attempt",
        "592_validation": "592 validation gate",
        "592_noether": "Noether P/J origin formula rows",
        "592_pj_attempt": "P/J parent origin attempts",
        "592_ambiguity": "improvement ambiguity gates",
        "593_doc": "minimal L/theta/mu/vX fill attempt",
        "593_validation": "593 validation gate",
        "593_candidates": "minimal parent fill candidates",
        "593_pj_test": "P/J extraction tests",
        "670_doc": "immediate 670 no-pole/source-free handoff",
        "670_validation": "670 validation gate",
        "670_vertical": "670 vertical generator certificate",
        "670_effect": "670 zero-or-residual effect rows",
    }
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def omega_dcx_owner_audit_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "audit_id": "ODA671_0_variational_definition",
            "object": "theta_Y and Omega_Y",
            "formula_or_test": "delta L_parent = E_A delta Y^A + d theta_Y(delta Y); Omega_Y=delta theta_Y",
            "current_status": "formal_definition_only",
            "what_is_gained": "defines the pairing needed for DCdagger=Omega_flat(v_X)",
            "owner_blocker": "actual MTS parent Lagrangian and extra-sector theta are not signed",
            "claim_effect": "no generator ownership",
            "valid_for_claim": "false",
            "source_paths": source_list("591_omega", "592_noether"),
            "generated_utc": now,
        },
        {
            "audit_id": "ODA671_1_EH_metric_core",
            "object": "EH symplectic template",
            "formula_or_test": "theta_EH and standard covariant phase-space current",
            "current_status": "standard_GR_template_not_MTS_owner",
            "what_is_gained": "shows the diffeomorphism route is mathematically available",
            "owner_blocker": "MTS C_X/P/J not identified with the EH/ADM momentum current",
            "claim_effect": "conditional template only",
            "valid_for_claim": "false",
            "source_paths": source_list("591_omega", "593_candidates", "593_pj_test"),
            "generated_utc": now,
        },
        {
            "audit_id": "ODA671_2_extra_sector_theta",
            "object": "theta_extra for MTS fields",
            "formula_or_test": "theta_extra=sum_A Pi_A^mu delta Phi^A + improvements",
            "current_status": "missing_explicit_MTS_extra_parent_Lagrangian",
            "what_is_gained": "would let the vertical action be checked field by field",
            "owner_blocker": "motion/time/domain/memory/projector Lagrangians remain unfilled",
            "claim_effect": "extra-sector pole/source not erased",
            "valid_for_claim": "false",
            "source_paths": source_list("591_omega", "590_field_map", "670_vertical"),
            "generated_utc": now,
        },
        {
            "audit_id": "ODA671_3_DCX_tensor_formula",
            "object": "DC_X tensor convention",
            "formula_or_test": "DC_X^nu=-nabla_mu(delta P^{mu nu})-deltaGamma^mu_{mu rho}P^{rho nu}-deltaGamma^nu_{mu rho}P^{mu rho}+delta J_eff^nu",
            "current_status": "formal_operator_formula",
            "what_is_gained": "DC_X is no longer a pure symbol",
            "owner_blocker": "P/J parent composites and tensor-vs-density convention are still open",
            "claim_effect": "no adjoint certificate",
            "valid_for_claim": "false",
            "source_paths": source_list("591_dc", "592_pj_attempt", "592_ambiguity"),
            "generated_utc": now,
        },
        {
            "audit_id": "ODA671_4_DCX_boundary_pairing",
            "object": "DC boundary term",
            "formula_or_test": "int X[-nabla delta P]=int (nabla X)delta P - int_boundary n_mu X_nu delta P^{mu nu}",
            "current_status": "edge_risk_explicit",
            "what_is_gained": "identifies the exact boundary term Q_X must cancel or zero",
            "owner_blocker": "delta Q_X, boundary primitive, and allowed X domain are not derived",
            "claim_effect": "edge residual retained",
            "valid_for_claim": "false",
            "source_paths": source_list("591_dc", "583_edge", "584_edge_law"),
            "generated_utc": now,
        },
        {
            "audit_id": "ODA671_5_Omega_DCX_comparison",
            "object": "DCdagger X vs Omega_flat(v_X)",
            "formula_or_test": "DCdagger X = Omega_Y^flat(v_X) iff P,J,Omega,Q_X come from one parent current",
            "current_status": "formula_progress_but_no_certificate",
            "what_is_gained": "the exact equality criterion is known",
            "owner_blocker": "same parent action does not yet supply Omega, C_X, P/J, v_X, and Q_X",
            "claim_effect": "no first-class no-pole credit",
            "valid_for_claim": "false",
            "source_paths": source_list("591_comparison", "590_dc_map", "670_vertical"),
            "generated_utc": now,
        },
        {
            "audit_id": "ODA671_6_reduced_Omega",
            "object": "Omega_reduced nondegeneracy",
            "formula_or_test": "Omega_reduced must be nondegenerate after quotienting proper vertical degeneracies",
            "current_status": "not_constructed",
            "what_is_gained": "DCdagger X=0 could imply no proper stabilizer",
            "owner_blocker": "reduced phase space and domain are not constructed",
            "claim_effect": "zero-mode/stabilizer route not closed",
            "valid_for_claim": "false",
            "source_paths": source_list("591_omega", "589_required_sources", "670_vertical"),
            "generated_utc": now,
        },
        {
            "audit_id": "ODA671_7_verdict",
            "object": "parent Omega/DC_X owner",
            "formula_or_test": "all Omega/DC/PJ/Q boundary objects must have one parent owner",
            "current_status": "not_parent_owned",
            "what_is_gained": "formal math is usable as a target",
            "owner_blocker": "single-owner equality not closed",
            "claim_effect": "edge residual vector required",
            "valid_for_claim": "false",
            "source_paths": source_list("591_comparison", "592_noether", "593_pj_test"),
            "generated_utc": now,
        },
    ]


def noether_pj_single_owner_test_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "test_id": "NPJ671_0_single_current_contract",
            "route": "Noether current origin",
            "test": "j_X=theta_Y(v_X)-mu_X splits into X_nu J_eff^nu + (nabla_mu X_nu)P^{mu nu}+dB",
            "current_result": "formal_derivation_not_filled",
            "blocker": "L_parent, theta_Y, mu_X, and v_X are not all explicit",
            "if_success": "P and J become one-current objects rather than inserted symbols",
            "if_fail": "P/J owner residual remains",
            "valid_for_claim": "false",
            "source_paths": source_list("592_noether", "592_pj_attempt"),
            "generated_utc": now,
        },
        {
            "test_id": "NPJ671_1_diffeomorphism_route",
            "route": "ordinary diffeomorphism current",
            "test": "MTS C_X equals the EH+matter+extra diffeomorphism momentum constraint",
            "current_result": "conditional_GR_template_only",
            "blocker": "identity between MTS defect current and diffeo current is not proven",
            "if_success": "standard momentum-map machinery could own C_X",
            "if_fail": "diffeo route stays analogy/template",
            "valid_for_claim": "false",
            "source_paths": source_list("593_candidates", "593_pj_test", "591_omega"),
            "generated_utc": now,
        },
        {
            "test_id": "NPJ671_2_strict_quotient_zero_route",
            "route": "strict quotient zero current",
            "test": "L_parent=L_red[pi(Y)] and Dpi[v_X]=0 imply P=0/J_eff=0 up to exact terms",
            "current_result": "best_no_pole_if_pi_and_matter_are_constructed",
            "blocker": "pi, matter functor blindness, and boundary exact terms are not fully constructed",
            "if_success": "C_X has no physical pole and edge charge can vanish structurally",
            "if_fail": "quotient route remains conditional",
            "valid_for_claim": "false",
            "source_paths": source_list("593_candidates", "593_pj_test", "670_doc"),
            "generated_utc": now,
        },
        {
            "test_id": "NPJ671_3_affine_route",
            "route": "affine/topological block",
            "test": "P/J appear as coefficients in an affine V_def block",
            "current_result": "rejected_as_parent_origin",
            "blocker": "declaring P/J inside a new block names the coefficients but does not derive them",
            "if_success": "would need upstream L0/theta0/vX to produce P/J before the affine block",
            "if_fail": "no theorem credit",
            "valid_for_claim": "false",
            "source_paths": source_list("592_pj_attempt", "593_candidates", "593_pj_test"),
            "generated_utc": now,
        },
        {
            "test_id": "NPJ671_4_hybrid_route",
            "route": "EH plus quotient-extra split",
            "test": "EH current owned, representative/MTS-extra directions quotient-zero or exact",
            "current_result": "promising_but_unfilled",
            "blocker": "observed/representative split of MTS variables is not explicit enough",
            "if_success": "could preserve local GR metric while making extra MTS directions pure representative data",
            "if_fail": "extra-sector residual remains",
            "valid_for_claim": "false",
            "source_paths": source_list("593_candidates", "593_pj_test", "670_doc"),
            "generated_utc": now,
        },
        {
            "test_id": "NPJ671_5_improvement_ambiguity",
            "route": "current/superpotential representative choice",
            "test": "P and Q_X are invariantly fixed under P->P+dS and j->j+dB improvements",
            "current_result": "open",
            "blocker": "boundary/reference choice does not yet fix representative",
            "if_success": "edge charge becomes unambiguous",
            "if_fail": "edge alpha can shift under improvements and cannot be claimed",
            "valid_for_claim": "false",
            "source_paths": source_list("592_ambiguity", "583_edge"),
            "generated_utc": now,
        },
        {
            "test_id": "NPJ671_6_verdict",
            "route": "single parent owner",
            "test": "same L_parent supplies theta, Omega, v_X, P, J_eff, Q_X, and boundary domain",
            "current_result": "not_closed",
            "blocker": "no route signs every object together",
            "if_success": "no-pole theorem can be revisited",
            "if_fail": "edge residual vector remains mandatory",
            "valid_for_claim": "false",
            "source_paths": source_list("583_contract", "591_comparison", "592_noether", "593_pj_test"),
            "generated_utc": now,
        },
    ]


def boundary_charge_owner_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "BCG671_0_boundary_charge_definition",
            "object": "Q_edge^H(lambda)",
            "zero_or_owner_test": "Q_edge^H=int_boundary dS F_lambda epsilon_nu B_X^nu",
            "current_status": "symbolic_residual",
            "missing": "B_X owner, edge kernel F_lambda, allowed epsilon domain",
            "fallback": "Qbar_edge_XH(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_list("583_edge", "584_edge_law"),
            "generated_utc": now,
        },
        {
            "gate_id": "BCG671_1_proper_gauge",
            "object": "allowed X domain",
            "zero_or_owner_test": "epsilon|boundary=0 or compact-support proper gauge",
            "current_status": "closure_only",
            "missing": "proof that this domain does not remove physical ADM/time/rotation charges or overrestrict sources",
            "fallback": "retain improper edge mode possibility",
            "valid_for_claim": "false",
            "source_paths": source_list("583_owner_gates", "589_required_sources"),
            "generated_utc": now,
        },
        {
            "gate_id": "BCG671_2_exact_boundary_form",
            "object": "B_X exact/pure-gauge",
            "zero_or_owner_test": "B_X=d_boundary b_X or pure gauge on compact closed shell",
            "current_status": "not_derived",
            "missing": "explicit b_X from parent fields and boundary class",
            "fallback": "Q_edge residual",
            "valid_for_claim": "false",
            "source_paths": source_list("584_owner_repair", "583_edge"),
            "generated_utc": now,
        },
        {
            "gate_id": "BCG671_3_counterterm_cancellation",
            "object": "Q_X differentiability",
            "zero_or_owner_test": "delta Q_X cancels the DC boundary term without deleting physical mass charge",
            "current_status": "not_derived",
            "missing": "local covariant boundary counterterm and reference subtraction",
            "fallback": "edge residual plus reference projection row",
            "valid_for_claim": "false",
            "source_paths": source_list("591_dc", "584_owner_repair"),
            "generated_utc": now,
        },
        {
            "gate_id": "BCG671_4_projector_orthogonality",
            "object": "Pi_M^H[Q_edge]",
            "zero_or_owner_test": "mass/Hamiltonian projector is orthogonal to edge charge including reference-boundary terms",
            "current_status": "not_derived",
            "missing": "Pi_M action on edge charge and delta Pi_M stress destination",
            "fallback": "Qbar_edge_XH(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_list("584_owner_repair", "584_input_contract", "670_effect"),
            "generated_utc": now,
        },
        {
            "gate_id": "BCG671_5_boundary_cocycle",
            "object": "K_boundary[epsilon,eta]",
            "zero_or_owner_test": "{G[epsilon],G[eta]}=G[[epsilon,eta]] with K_boundary=0",
            "current_status": "uncomputed",
            "missing": "bracket closure calculation from parent Omega and differentiable generator",
            "fallback": "edge-mode/central-extension residual",
            "valid_for_claim": "false",
            "source_paths": source_list("583_edge", "670_vertical"),
            "generated_utc": now,
        },
        {
            "gate_id": "BCG671_6_no_double_count",
            "object": "bulk-edge split",
            "zero_or_owner_test": "Q_X=Q_bulk+Q_edge orthogonally with no duplicated source charge",
            "current_status": "missing",
            "missing": "projection rules and source split",
            "fallback": "combined alpha_total remains nonclaim",
            "valid_for_claim": "false",
            "source_paths": source_list("584_edge_law", "584_input_contract"),
            "generated_utc": now,
        },
        {
            "gate_id": "BCG671_7_verdict",
            "object": "boundary charge zero",
            "zero_or_owner_test": "all boundary gates pass together",
            "current_status": "not_passed",
            "missing": "proper/exact/counterterm/projector/cocycle/no-double-count proof",
            "fallback": "edge residual vector retained",
            "valid_for_claim": "false",
            "source_paths": source_list("583_edge", "584_edge_law", "670_effect"),
            "generated_utc": now,
        },
    ]


def edge_residual_vector_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "residual_id": "ERV671_0_lambda_edge",
            "symbol": "lambda_edge or F_lambda support",
            "definition": "edge range/support envelope used to select alpha_bound(lambda)",
            "value_status": "MISSING_EDGE_RANGE_OR_ENVELOPE",
            "units_status": "MISSING_LENGTH_UNITS",
            "source_status": "missing",
            "zero_repair": "no edge support if boundary charge is theorem-zero",
            "feeds": "alpha_edge(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_list("584_input_contract", "584_edge_law"),
            "generated_utc": now,
        },
        {
            "residual_id": "ERV671_1_K_edge",
            "symbol": "K_edge(lambda)",
            "definition": "normalization from edge Green/boundary kernel divided by observed gravity normalization",
            "value_status": "MISSING_SOURCE_BACKED_K_EDGE",
            "units_status": "MISSING_UNITS",
            "source_status": "missing",
            "zero_repair": "parent no-pole or exact boundary primitive makes K_edge inactive",
            "feeds": "alpha_edge(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_list("584_edge_law", "589_edge_template", "591_edge_status"),
            "generated_utc": now,
        },
        {
            "residual_id": "ERV671_2_Qbar_edge_XH",
            "symbol": "Qbar_edge_XH(lambda)",
            "definition": "Pi_M^H[Q_edge^H(lambda)]/M_H",
            "value_status": "MISSING_SOURCE_BACKED_QBAR_EDGE_XH",
            "units_status": "MISSING_DIMENSIONLESS_OR_DECLARED_UNITS",
            "source_status": "missing",
            "zero_repair": "projector orthogonality including reference boundary terms",
            "feeds": "alpha_edge(lambda);Qbar_XH",
            "valid_for_claim": "false",
            "source_paths": source_list("583_edge", "584_input_contract", "589_edge_template"),
            "generated_utc": now,
        },
        {
            "residual_id": "ERV671_3_qbar_XT",
            "symbol": "qbar_XT",
            "definition": "test-body X/edge response factor",
            "value_status": "MISSING_SOURCE_BACKED_QBAR_XT_OR_THEOREM_ZERO",
            "units_status": "MISSING_DIMENSIONLESS_OR_DECLARED_UNITS",
            "source_status": "retained_from_prior_residuals",
            "zero_repair": "matter quotient blindness/no-marker constant theorem",
            "feeds": "alpha_edge(lambda);alpha_bulk(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_list("589_edge_template", "670_effect"),
            "generated_utc": now,
        },
        {
            "residual_id": "ERV671_4_BX_boundary_momentum",
            "symbol": "B_X^nu=n_mu P^{mu nu}+B_ct^nu",
            "definition": "boundary primitive/momentum entering Q_edge",
            "value_status": "MISSING_BOUNDARY_OWNER",
            "units_status": "MISSING_UNITS",
            "source_status": "symbolic",
            "zero_repair": "B_X zero/exact/pure-gauge from parent boundary action",
            "feeds": "Q_edge^H(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_list("583_edge", "591_dc", "592_ambiguity"),
            "generated_utc": now,
        },
        {
            "residual_id": "ERV671_5_K_boundary",
            "symbol": "K_boundary[epsilon,eta]",
            "definition": "boundary cocycle/central term in the generator algebra",
            "value_status": "MISSING_BRACKET_CALCULATION",
            "units_status": "MISSING_UNITS",
            "source_status": "uncomputed",
            "zero_repair": "equivariant momentum map with zero boundary cocycle",
            "feeds": "no_pole_gate;edge_mode_diagnosis",
            "valid_for_claim": "false",
            "source_paths": source_list("583_edge", "670_vertical"),
            "generated_utc": now,
        },
        {
            "residual_id": "ERV671_6_bulk_edge_split",
            "symbol": "Q_X=Q_bulk+Q_edge",
            "definition": "orthogonal source split preventing double counting in alpha_total",
            "value_status": "MISSING_SOURCE_SPLIT",
            "units_status": "not_applicable_until_split_defined",
            "source_status": "missing",
            "zero_repair": "parent projector/reference split",
            "feeds": "combined_alpha_total(lambda)",
            "valid_for_claim": "false",
            "source_paths": source_list("584_edge_law", "584_input_contract"),
            "generated_utc": now,
        },
        {
            "residual_id": "ERV671_7_claim_grade_bound_curve",
            "symbol": "alpha_bound(lambda)",
            "definition": "claim-grade local fifth-force bound curve for active edge support",
            "value_status": "PRIVATE_OR_PLACEHOLDER_ONLY_FOR_EDGE_CONTEXT",
            "units_status": "lambda_units_required",
            "source_status": "not_claim_grade_for_edge_branch_here",
            "zero_repair": "not needed if edge theorem-zero closes",
            "feeds": "R10 edge comparator",
            "valid_for_claim": "false",
            "source_paths": source_list("584_input_contract", "591_edge_status"),
            "generated_utc": now,
        },
        {
            "residual_id": "ERV671_8_alpha_edge_product",
            "symbol": "alpha_edge(lambda)=K_edge(lambda) Qbar_edge_XH(lambda) qbar_XT",
            "definition": "R10-comparable edge residual amplitude",
            "value_status": "MISSING_PRODUCT",
            "units_status": "dimensionless_after_inputs_owned",
            "source_status": "all factors missing_or_retained",
            "zero_repair": "any factor theorem-zero with no substitute edge mode",
            "feeds": "R10 edge residual",
            "valid_for_claim": "false",
            "source_paths": source_list("584_edge_law", "589_edge_template"),
            "generated_utc": now,
        },
        {
            "residual_id": "ERV671_9_decision_row",
            "symbol": "edge_residual_vector",
            "definition": "fallback vector retained if parent Omega/DC_X/boundary owner fails",
            "value_status": "RETAINED_NONCLAIM",
            "units_status": "mixed_missing_units",
            "source_status": "schema_ready_sources_missing",
            "zero_repair": "672 boundary exactness/projector orthogonality before coefficient scoring",
            "feeds": NEXT_TARGET,
            "valid_for_claim": "false",
            "source_paths": source_list("583_edge", "584_edge_law", "670_effect"),
            "generated_utc": now,
        },
    ]


def evaluator_rows(
    omega_rows: list[dict[str, str]],
    noether_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    edge_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    all_nonclaim = all(row["valid_for_claim"] == "false" for row in omega_rows + noether_rows + boundary_rows + edge_rows)
    return [
        {
            "evaluator_id": "EV671_0_parent_Omega_DCX",
            "target": "own Omega/DC_X from one parent action",
            "status": "fail_nonclaim",
            "reason": "Omega and DC_X formulas exist, but not as one parent-owned equality with P/J/Q_X",
            "claim_effect": "no K_X=0 or first-class no-pole credit",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV671_1_boundary_charge_zero",
            "target": "kill boundary charge",
            "status": "fail_nonclaim",
            "reason": "proper/exact/counterterm/projector/cocycle/no-double-count gates remain unsigned",
            "claim_effect": "Qbar_edge_XH remains live",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV671_2_edge_vector",
            "target": "retain explicit edge residual vector",
            "status": "pass_nonclaim",
            "reason": "all edge factors are named with source/unit/status blockers and valid_for_claim=false",
            "claim_effect": "fallback is testable later but not evidence now",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV671_3_next_route",
            "target": "select next zero-repair target",
            "status": "boundary_exactness_projector_orthogonality_first",
            "reason": "this can zero Qbar_edge_XH before we pay the cost of sourcing edge coefficients",
            "claim_effect": "next derivation only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "evaluator_id": "EV671_4_safety",
            "target": "prevent silent promotion",
            "status": "pass" if all_nonclaim else "fail",
            "reason": "all generated owner/gate/vector rows remain invalid for claim",
            "claim_effect": "private nonclaim checkpoint",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D671_0",
            "status": STATUS,
            "meaning": "formal Omega/DC_X/PJ machinery exists, but the single-parent owner and zero-boundary-charge certificates do not close; edge residual vector is retained",
            "claim_status": CLAIM_CEILING,
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, str]],
    omega_rows: list[dict[str, str]],
    noether_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    edge_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    prior_validation_ids = ["583_validation", "584_validation", "589_validation", "591_validation", "592_validation", "593_validation", "670_validation"]
    prior_failures = {source_id: validation_failures_for(source_id) for source_id in prior_validation_ids}
    prior_failure_count = sum(len(rows) for rows in prior_failures.values())
    edge_statuses = ";".join(row["value_status"] for row in edge_rows)
    all_generated_rows = omega_rows + noether_rows + boundary_rows + edge_rows + evaluator_data + decision
    generated_outputs = [
        DOC_PATH,
        RESIDUALS / "P8_Y5_R10_671_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_671_PARENT_OMEGA_DCX_OWNER_AUDIT.csv",
        RESIDUALS / "P8_Y5_R10_671_NOETHER_PJ_SINGLE_OWNER_TEST.csv",
        RESIDUALS / "P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv",
        RESIDUALS / "P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv",
        RESIDUALS / "P8_Y5_R10_671_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_671_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_671_NONCLAIM_SUMMARY.csv",
    ]
    return [
        {
            "check_id": "V671_0_source_paths_exist",
            "result": "pass" if all(row["exists"] == "true" for row in source_rows) else "fail",
            "detail": "all cited source paths exist" if all(row["exists"] == "true" for row in source_rows) else "one or more cited source paths missing",
            "generated_utc": now,
        },
        {
            "check_id": "V671_1_prior_validations_clean",
            "result": "pass" if prior_failure_count == 0 else "fail",
            "detail": ";".join(f"{source_id}={len(rows)}" for source_id, rows in prior_failures.items()),
            "generated_utc": now,
        },
        {
            "check_id": "V671_2_omega_dcx_audit_coverage",
            "result": "pass" if len(omega_rows) >= 8 and any(row["current_status"] == "not_parent_owned" for row in omega_rows) else "fail",
            "detail": f"omega_rows={len(omega_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "V671_3_noether_single_owner_coverage",
            "result": "pass" if len(noether_rows) >= 7 and any(row["current_result"] == "rejected_as_parent_origin" for row in noether_rows) else "fail",
            "detail": f"noether_rows={len(noether_rows)} affine_rejection_present={any(row['current_result'] == 'rejected_as_parent_origin' for row in noether_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "V671_4_boundary_gate_coverage",
            "result": "pass" if len(boundary_rows) >= 8 and any(row["current_status"] == "not_passed" for row in boundary_rows) else "fail",
            "detail": f"boundary_rows={len(boundary_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "V671_5_edge_vector_missing_markers",
            "result": "pass"
            if len(edge_rows) >= 10
            and "MISSING_SOURCE_BACKED_K_EDGE" in edge_statuses
            and "MISSING_SOURCE_BACKED_QBAR_EDGE_XH" in edge_statuses
            and "MISSING_PRODUCT" in edge_statuses
            else "fail",
            "detail": f"edge_rows={len(edge_rows)} statuses={edge_statuses}",
            "generated_utc": now,
        },
        {
            "check_id": "V671_6_no_claim_rows_promoted",
            "result": "pass" if all(row["valid_for_claim"] == "false" for row in all_generated_rows) else "fail",
            "detail": "all generated rows remain valid_for_claim=false",
            "generated_utc": now,
        },
        {
            "check_id": "V671_7_next_target_selected",
            "result": "pass" if decision and decision[0]["next_action"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "check_id": "V671_8_generated_outputs_scoped",
            "result": "pass" if all(str(path).startswith(str(ROOT)) for path in generated_outputs) else "fail",
            "detail": "all 671 outputs target post-checkpoint-work",
            "generated_utc": now,
        },
        {
            "check_id": "V671_9_formalization_workbench_untouched",
            "result": "pass" if formalization_changed_count() == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_changed_count()}",
            "generated_utc": now,
        },
        {
            "check_id": "V671_10_status_nonclaim",
            "result": "pass" if "no_KX_zero" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING else "fail",
            "detail": CLAIM_CEILING,
            "generated_utc": now,
        },
        {
            "check_id": "V671_11_evaluator_nonclaim_passes",
            "result": "pass" if any(row["status"] == "pass_nonclaim" for row in evaluator_data) and evaluator_data[-1]["status"] == "pass" else "fail",
            "detail": ";".join(row["status"] for row in evaluator_data),
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows(
    omega_rows: list[dict[str, str]],
    noether_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    edge_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    failures = [row["check_id"] for row in validation if row["result"] != "pass"]
    hard_blockers = [
        "single_parent_L_theta_Omega",
        "P_J_current_owner",
        "DC_convention_and_parent_expansion",
        "Q_X_boundary_differentiability",
        "projector_orthogonality",
        "K_boundary_closure",
        "edge_coefficient_sources",
    ]
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "omega_rows": str(len(omega_rows)),
            "noether_rows": str(len(noether_rows)),
            "boundary_rows": str(len(boundary_rows)),
            "edge_rows": str(len(edge_rows)),
            "evaluator_rows": str(len(evaluator_data)),
            "hard_blockers": ";".join(hard_blockers),
            "validation_failures": ";".join(failures),
            "next_target": NEXT_TARGET,
            "generated_utc": now,
        }
    ]


def cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, str]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |\n"
    separator = "| " + " | ".join("---" for _ in fields) + " |\n"
    body = "".join("| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |\n" for row in rows)
    return header + separator + body


def write_document(
    source_rows: list[dict[str, str]],
    omega_rows: list[dict[str, str]],
    noether_rows: list[dict[str, str]],
    boundary_rows: list[dict[str, str]],
    edge_rows: list[dict[str, str]],
    evaluator_data: list[dict[str, str]],
    decision: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    validation_table = markdown_table(validation, ["check_id", "result", "detail"]) if validation else "_Validation pending final write._\n"
    doc = f"""# 671 - Y5 R10 Parent Omega DCX Boundary Charge Owner Or Edge Residual Vector

## Verdict

671 tried to turn the 670 quotient/no-pole route into an owned parent-generator proof.

Result: useful formal machinery exists, but not enough to claim no-pole.

```text
Omega_Y and DC_X have formal candidate expressions.
P and J_eff have a clean Noether-current origin contract.
Q_boundary has an exact residual formula.
But the same parent action does not yet own L_parent, theta_Y, Omega_Y, v_X, P/J, Q_X, and the boundary domain together.
```

Therefore `K_X=0`, `Qbar_edge_XH=0`, R10, R11, PPN, and local GR remain nonclaim. The edge channel is retained as an explicit residual vector, not hidden as gauge fog.

| Field | Value |
| --- | --- |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "source_path", "exists", "role"])}

## Parent Omega/DCX Owner Audit

{markdown_table(omega_rows, ["audit_id", "object", "formula_or_test", "current_status", "what_is_gained", "owner_blocker", "claim_effect", "valid_for_claim"])}

## Noether P/J Single-Owner Test

{markdown_table(noether_rows, ["test_id", "route", "test", "current_result", "blocker", "if_success", "if_fail", "valid_for_claim"])}

## Boundary Charge Owner Gate

{markdown_table(boundary_rows, ["gate_id", "object", "zero_or_owner_test", "current_status", "missing", "fallback", "valid_for_claim"])}

## Edge Residual Vector

{markdown_table(edge_rows, ["residual_id", "symbol", "definition", "value_status", "units_status", "source_status", "zero_repair", "feeds", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator_data, ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision, ["decision_id", "status", "meaning", "claim_status", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "omega_rows", "noether_rows", "boundary_rows", "edge_rows", "evaluator_rows", "hard_blockers", "validation_failures", "next_target"])}

## Validation

{validation_table}

## Interpretation

The best derivation move is now very specific. We should not try to source `K_edge` first unless we have to. The cleaner route is to kill the source side by proving either:

1. `B_X` is exact/pure gauge or killed by a proper compact-local boundary domain, or
2. `Pi_M^H[Q_edge]=0` by projector/reference orthogonality.

If those fail, then the edge branch becomes empirical and needs real `lambda_edge`, `K_edge`, `Qbar_edge_XH`, and `qbar_XT` inputs.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    omega_rows = omega_dcx_owner_audit_rows()
    noether_rows = noether_pj_single_owner_test_rows()
    boundary_rows = boundary_charge_owner_gate_rows()
    edge_rows = edge_residual_vector_rows()
    evaluator_data = evaluator_rows(omega_rows, noether_rows, boundary_rows, edge_rows)
    decision = decision_rows()

    write_csv(RESIDUALS / "P8_Y5_R10_671_SOURCE_REGISTER.csv", source_rows, ["source_id", "source_path", "exists", "role", "generated_utc"])
    write_csv(
        RESIDUALS / "P8_Y5_R10_671_PARENT_OMEGA_DCX_OWNER_AUDIT.csv",
        omega_rows,
        ["audit_id", "object", "formula_or_test", "current_status", "what_is_gained", "owner_blocker", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_671_NOETHER_PJ_SINGLE_OWNER_TEST.csv",
        noether_rows,
        ["test_id", "route", "test", "current_result", "blocker", "if_success", "if_fail", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_671_BOUNDARY_CHARGE_OWNER_GATE.csv",
        boundary_rows,
        ["gate_id", "object", "zero_or_owner_test", "current_status", "missing", "fallback", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_671_EDGE_RESIDUAL_VECTOR.csv",
        edge_rows,
        ["residual_id", "symbol", "definition", "value_status", "units_status", "source_status", "zero_repair", "feeds", "valid_for_claim", "source_paths", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_671_EVALUATOR.csv",
        evaluator_data,
        ["evaluator_id", "target", "status", "reason", "claim_effect", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_671_DECISION.csv",
        decision,
        ["decision_id", "status", "meaning", "claim_status", "next_action", "valid_for_claim", "generated_utc"],
    )

    write_document(source_rows, omega_rows, noether_rows, boundary_rows, edge_rows, evaluator_data, decision, [], [])

    validation = validation_rows(source_rows, omega_rows, noether_rows, boundary_rows, edge_rows, evaluator_data, decision)
    summary_rows = nonclaim_summary_rows(omega_rows, noether_rows, boundary_rows, edge_rows, evaluator_data, validation)
    write_csv(
        RESIDUALS / "P8_Y5_R10_671_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "omega_rows",
            "noether_rows",
            "boundary_rows",
            "edge_rows",
            "evaluator_rows",
            "hard_blockers",
            "validation_failures",
            "next_target",
            "generated_utc",
        ],
    )
    write_csv(RESIDUALS / "P8_Y5_BRR545_671_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_document(source_rows, omega_rows, noether_rows, boundary_rows, edge_rows, evaluator_data, decision, summary_rows, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"omega_rows={len(omega_rows)}")
    print(f"noether_rows={len(noether_rows)}")
    print(f"boundary_rows={len(boundary_rows)}")
    print(f"edge_rows={len(edge_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
