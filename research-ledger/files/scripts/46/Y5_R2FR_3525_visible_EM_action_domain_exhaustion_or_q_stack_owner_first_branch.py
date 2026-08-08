from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3525-Y5-R2FR-visible-EM-action-domain-exhaustion-or-q-stack-owner-first-branch.md"
CANONICAL_STATUS = OUT / "P8_EM_visible_EM_first_owner_branch_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3525": {"path": Path(__file__).resolve(), "role": "3525 generator"},
    "doc_3524": {
        "path": ROOT / "3524-Y5-R2FR-observed-stack-and-charge-lattice-parent-owner-or-local-source-kernel-values.md",
        "role": "3524 composite local owner handoff",
    },
    "next_3524": {
        "path": OUT / "P8_Y5_R2FR_3524_NEXT_TARGET.csv",
        "role": "3524-selected first-owner branch target",
    },
    "doc_3505": {
        "path": ROOT / "3505-Y5-R2FR-visible-EM-action-domain-exhaustion-no-chiEM-no-hidden-Hodge-or-bound.md",
        "role": "visible EM action-domain theorem shape",
    },
    "domain_theorem_3505": {
        "path": OUT / "P8_Y5_R2FR_3505_VISIBLE_EM_ACTION_DOMAIN_THEOREM.csv",
        "role": "3505 typed EM action-domain theorem and countermodels",
    },
    "bound_vector_3505": {
        "path": OUT / "P8_Y5_R2FR_3505_VISIBLE_EM_BOUND_VECTOR.csv",
        "role": "3505 EM residual vector before generator-signature reduction",
    },
    "doc_3506": {
        "path": ROOT / "3506-Y5-R2FR-parent-visible-EM-generator-signature-or-first-constitutive-bound-runner.md",
        "role": "parent visible EM generator signature and reduction theorem",
    },
    "generator_signature_3506": {
        "path": OUT / "P8_Y5_R2FR_3506_PARENT_VISIBLE_EM_GENERATOR_SIGNATURE.csv",
        "role": "3506 visible U(1), no-extra-tensor, Lorentz naturality and reciprocity clauses",
    },
    "residual_reduction_3506": {
        "path": OUT / "P8_Y5_R2FR_3506_RESIDUAL_REDUCTION_MAP.csv",
        "role": "3506 residual reduction map",
    },
    "bound_template_3506": {
        "path": OUT / "P8_Y5_R2FR_3506_CONSTITUTIVE_BOUND_INPUT_TEMPLATE.csv",
        "role": "3506 constitutive bound placeholder/input template",
    },
    "doc_2588": {
        "path": ROOT / "2588-Y5-R2FR-observed-stack-q-eobs-tau-parent-owner-or-source-leak-fill.md",
        "role": "q/e_obs/tau/ell_J observed-stack owner comparator",
    },
    "owner_certificate_2588": {
        "path": OUT / "P8_Y5_OBS_STACK_2588_OWNER_CERTIFICATE.csv",
        "role": "2588 observed-stack owner certificate blockers",
    },
    "doc_3466": {
        "path": ROOT / "3466-Y5-R2FR-unique-F2-Hodge-owner-or-WEP-nuclear-mass-component-row.md",
        "role": "unique F2/Hodge owner audit and finite nonclaim mass-row contrast",
    },
    "wep_mass_row_3466": {
        "path": OUT / "P8_Y5_R2FR_3466_WEP_MASS_COMPONENT_ROW.csv",
        "role": "3466 finite nonclaim WEP material-mass component example",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def branch_selection_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "BR3525_0_visible_EM_first",
            "candidate": "visible EM action-domain exhaustion",
            "input_stack": "3505 typed domain plus 3506 visible U(1)/naturality/reciprocity reduction",
            "derivation_move": "normal-form the EM action before touching the full q/e_obs/tau/source stack",
            "why_less_circular": "requires only the observed EM generator, Hodge owner and fixed scalar coupling; does not first require the whole local source/clock/orbit owner",
            "blocking_clause": "scalar gauge kinetic owner lambda_A/e_obs^2 remains unsigned",
            "selected": "True",
            "claim_allowed": "False",
        },
        {
            "branch_id": "BR3525_1_q_stack_first",
            "candidate": "q/e_obs/tau/ell_J observed-stack owner",
            "input_stack": "2588 owner certificate plus 3524 composite owner",
            "derivation_move": "try to close q map, vertical kernel, same-frame readout, tau identity and ell_J before EM normal form",
            "why_less_circular": "not selected; it asks for almost the whole local branch at once",
            "blocking_clause": "MISSING_PARENT_Q_MAP; MISSING_PRESYMPLECTIC_NULL_KERNEL; MISSING_PARENT_OBS_E_FUNCTOR; MISSING_PARENT_TAU_IDENTITY; MISSING_PARENT_ELLJ_SCALE",
            "selected": "False",
            "claim_allowed": "False",
        },
    ]


def visible_em_reduction_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "VEM3525_0_domain_normal_form",
            "claim_piece": "visible EM first-owner normal form",
            "premises": "A_Q is the quotient-visible U(1) connection; F_Q=dA_Q; action arguments are exhausted by A_Q,F_Q,e_obs(q),orientation,fixed charge/current data and constants; local action is reciprocal and Lorentz-natural under e_obs",
            "derivation": "Gauge invariance makes the kinetic variable F_Q. Local quadratic naturality with only e_obs and orientation gives exactly F_Q wedge *_obs F_Q and F_Q wedge F_Q. Reciprocity removes skewon response because it cannot be a symmetric action Hessian. Typed domain exhaustion removes chi_EM, hidden/disformal Hodge and varied readout-Hodge slots by absence.",
            "normal_form": "S_EM = -1/2 int lambda_A F_Q wedge *_obs F_Q + 1/2 int theta_A F_Q wedge F_Q + int A_Q wedge J_Q + boundary",
            "zero_result": "Delta_chi_principal=0 modulo scalar lambda_A and axion; Delta_chi_skewon=0; C_Hodge_hidden=0; C_Hodge_readout=0 if readout is after variation",
            "surviving_frontier": "D_X ln(lambda_A/e_obs^2), d theta_A, source/current normalization and conformal scale",
            "status": "DERIVED_CONDITIONAL_NORMAL_FORM_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "VEM3525_1_poynting_source_identity",
            "claim_piece": "Poynting is not an extra source if Maxwell Hilbert owner closes",
            "premises": "VEM3525_0 plus same observed metric/coframe used in Hilbert variation",
            "derivation": "Variation with respect to the observed geometry gives T_EM^{mu nu}=lambda_A(F^{mu alpha}F^nu_alpha - 1/4 g_obs^{mu nu}F^2) plus scalar/axion derivative terms if lambda_A or theta_A vary. The Poynting vector is the spatial flux T_EM^{0i}; it is bookkeeping inside the Maxwell Hilbert stress, not an independent force term.",
            "normal_form": "S_Poynting^i = T_EM^{0i}; nabla_mu(T_matter^{mu nu}+T_EM^{mu nu})=0 after matter-EM exchange cancellation and boundary flux accounting",
            "zero_result": "epsilon_Poynting=0 only when lambda_A, J_Q and readout are same-owner and external flux is bounded",
            "surviving_frontier": "source-current normalization, radiative/boundary flux and scalar kinetic prefactor",
            "status": "EXACT_CONDITIONAL_IDENTITY",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "VEM3525_2_scalar_coupling_obstruction",
            "claim_piece": "scalar F2 coefficient is the real coupling throat",
            "premises": "Gauge invariance, diffeomorphism covariance, Lorentz naturality and visible U(1) are imposed",
            "derivation": "Those symmetries do not forbid lambda_A(q,X) F_Q wedge *_obs F_Q. If lambda_A is not parent-fixed or locked to e_obs/charge-current normalization, it shifts alpha_EM, WEP/R10 response, clocks, binding energy and the source weight of EM stress.",
            "normal_form": "C_XF2 := D_X ln(lambda_A/e_obs^2); parent success requires C_XF2=0 in the physical vertical/source direction or a sourced bound with arena kernels",
            "zero_result": "no zero theorem from the current premises",
            "surviving_frontier": "lambda_A/e_obs^2 owner, T_Q charge norm, J_Q source current and clock/mass calibration",
            "status": "NOT_DERIVED_NEXT_TARGET",
            "valid_for_claim": "False",
        },
    ]


def owner_clause_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G3525_0_visible_U1",
            "owner_clause": "visible U(1) connection owner",
            "required_signature": "A_Q is the quotient-visible connection; F_Q=dA_Q; J_Q is conserved and owned before readout",
            "current_status": "DERIVED_CONDITIONAL_FROM_3506",
            "if_unsigned": "C_JQ and readout current leakage remain",
            "source_path": str(SOURCES["generator_signature_3506"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3525_1_no_extra_tensor_domain",
            "owner_clause": "no independent chi_EM/hidden-Hodge/readout tensor arguments",
            "required_signature": "Args(S_EM) cap {chi_EM,g_hidden,f_H(Phi),chi_readout}=empty before variation",
            "current_status": "EXACT_IF_PARENT_DOMAIN_SIGNED",
            "if_unsigned": "Delta_chi_principal, C_Hodge_hidden and C_Hodge_readout stay live components",
            "source_path": str(SOURCES["domain_theorem_3505"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3525_2_lorentz_natural_quadratic",
            "owner_clause": "Lorentz-natural quadratic two-form action",
            "required_signature": "only e_obs(q), orientation and constants build the local two-form bilinear",
            "current_status": "DERIVED_IF_NATURALITY_AND_NO_EXTRA_TENSOR_SIGNED",
            "if_unsigned": "anisotropic principal constitutive tensor must be bounded",
            "source_path": str(SOURCES["generator_signature_3506"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3525_3_reciprocal_action",
            "owner_clause": "conservative reciprocal action Hessian",
            "required_signature": "EM response comes from a symmetric second variation, not a post-variation medium law",
            "current_status": "ZERO_IF_RECIPROCAL_ACTION_SIGNED",
            "if_unsigned": "skewon/dissipative/readout branch must be bounded",
            "source_path": str(SOURCES["generator_signature_3506"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3525_4_scalar_gauge_kinetic",
            "owner_clause": "lambda_A/e_obs^2 source-coupling owner",
            "required_signature": "lambda_A is a fixed parent constant or D_X ln(lambda_A/e_obs^2)=0 in the physical source direction",
            "current_status": "NOT_DERIVED_CORE_COUPLING_TARGET",
            "if_unsigned": "alpha_EM, WEP/R10, clocks, binding and source-normalization residuals remain",
            "source_path": str(SOURCES["residual_reduction_3506"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "gate_id": "G3525_5_q_stack_deferred",
            "owner_clause": "q/e_obs/tau/ell_J observed stack",
            "required_signature": "q map, parent-null vertical kernel, e_obs functor, same-frame readout, tau identity and ell_J all signed",
            "current_status": "DEFERRED_NOT_IGNORED",
            "if_unsigned": "full local GR/Newton/source normalization cannot be claimed even if EM normal-form route improves",
            "source_path": str(SOURCES["owner_certificate_2588"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def executable_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "REQ3525_0_Delta_chi_principal",
            "coefficient": "Delta_chi_principal",
            "current_reduction": "conditional zero if no-extra-tensor domain plus Lorentz-natural action are parent-signed",
            "needed_numeric_row": "anisotropic principal fraction or parent coefficient vector",
            "units": "dimensionless constitutive fraction",
            "source_requirement": "parent generator proof excluding chi_EM, or sourced vacuum-birefringence/light-cone bound and projection kernel",
            "projection_requirement": "map parent tensor coefficient to propagation/birefringence/Shapiro observable",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "REQ3525_1_Delta_chi_skewon",
            "coefficient": "Delta_chi_skewon",
            "current_reduction": "conditional zero from reciprocal conservative action Hessian",
            "needed_numeric_row": "skewon response fraction or dissipative medium coefficient",
            "units": "dimensionless response fraction",
            "source_requirement": "signed reciprocal-action clause, or sourced polarization/dispersion/Poynting nonconservation bound",
            "projection_requirement": "map skewon component to dispersion/energy-flux residual in the chosen arena",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "REQ3525_2_Delta_chi_axion_gradient",
            "coefficient": "Delta_chi_axion_gradient",
            "current_reduction": "constant theta_A is boundary/topological; gradient remains",
            "needed_numeric_row": "d theta_A along local/source/cosmological branch",
            "units": "inverse length or inverse canonical field, with normalization stated",
            "source_requirement": "parent no-pseudoscalar proof or sourced polarization-rotation/effective-current bound",
            "projection_requirement": "map dtheta_A to polarization rotation, spectroscopy or effective current observable",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "REQ3525_3_C_Hodge_hidden",
            "coefficient": "C_Hodge_hidden",
            "current_reduction": "conditional zero if the visible generator has no hidden/disformal Hodge slot",
            "needed_numeric_row": "hidden-Hodge/disformal coefficient",
            "units": "dimensionless metric/Hodge deformation",
            "source_requirement": "parent no-hidden-visible tensor-slot proof or sourced preferred-frame/light-speed anisotropy bound",
            "projection_requirement": "map hidden metric/Hodge deformation to PPN, clock or null propagation residual",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "REQ3525_4_C_Hodge_readout",
            "coefficient": "C_Hodge_readout",
            "current_reduction": "conditional zero if EM readout is after variation and never reinserted as S_red",
            "needed_numeric_row": "readout-Hodge backreaction coefficient",
            "units": "dimensionless readout deformation",
            "source_requirement": "readout-domain certificate or sourced clock/spectroscopy/alpha readout bound",
            "projection_requirement": "separate harmless observation map from varied reduced-action coefficient",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "REQ3525_5_C_XF2",
            "coefficient": "C_XF2",
            "current_reduction": "not killed by symmetry; this is the scalar coupling throat",
            "needed_numeric_row": "D_X ln(lambda_A/e_obs^2), Z_X, M_X^2, source normalization and arena sensitivity kernel",
            "units": "per canonical X or dimensionless log-derivative with X normalization stated",
            "source_requirement": "parent charge/current/gauge norm owner proof or sourced alpha_EM/WEP/R10/clock/source-normalization bound rows",
            "projection_requirement": "map C_XF2 to alpha drift, material binding, R10 force strength, clock ratios and EM stress source weight",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "REQ3525_6_Delta_conformal_scale",
            "coefficient": "Delta_conformal_scale",
            "current_reduction": "not visible in 4D source-free Maxwell light cone; needs matter/current/clock owner",
            "needed_numeric_row": "Weyl/source scale derivative or same-frame calibration theorem",
            "units": "dimensionless scale or log-derivative",
            "source_requirement": "same-frame clock/mass/current normalization proof or sourced redshift/source-normalization bound",
            "projection_requirement": "map conformal scale to clocks, masses, source current and Newtonian limit",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3525_0_branch",
            "quantity": "selected_first_owner_branch",
            "value": "visible_EM_action_domain",
            "meaning": "the next least-circular attack is the visible EM normal-form route, not the full q-stack route",
            "claim_effect": "progresses the coupling problem while preserving no-claim discipline",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3525_1_reduction",
            "quantity": "EM_residual_rank",
            "value": "reduced_to_scalar_coupling_plus_axion_readout_source_frontier",
            "meaning": "principal/skewon/hidden/readout chaos has exact conditional zero routes; C_XF2 is now the main coupling throat",
            "claim_effect": "this is real narrowing, not a local-GR/Maxwell pass",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3525_2_scalar_throat",
            "quantity": "D_X_ln_lambdaA_over_eobs2",
            "value": "not_derived",
            "meaning": "the current source hierarchy does not parent-sign lambda_A/e_obs^2 as constant in the physical source direction",
            "claim_effect": "no alpha/WEP/R10/clock/source-normalization victory may be claimed",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3525_3_q_stack",
            "quantity": "q_stack_branch",
            "value": "deferred_with_blockers_recorded",
            "meaning": "2588 blockers are kept live; the branch is not thrown away",
            "claim_effect": "full local GR/Newton route remains open but unsigned",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3525_0_select_visible_EM",
            "decision": "take the visible EM action-domain/generator route first",
            "rationale": "3505/3506 already provide a normal-form reduction; q-stack-first demands too much of the full local branch at once",
            "effect": "turns the coupling hunt into a precise scalar prefactor problem",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3525_1_no_fake_maxwell_pass",
            "decision": "do not claim Maxwell/local-GR source closure from the normal form alone",
            "rationale": "lambda_A/e_obs^2, J_Q and conformal/source scale still control alpha, clocks, WEP/R10 and Newtonian source weight",
            "effect": "keeps the attractive theorem from overreaching",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3525_2_next_throat",
            "decision": "make scalar gauge coupling owner the next target",
            "rationale": "C_XF2 is the surviving coefficient not killed by gauge/Lorentz/naturality/reciprocity",
            "effect": "next checkpoint should try to prove D_X ln(lambda_A/e_obs^2)=0 or produce numeric-ready alpha/WEP/R10/clock rows",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3526-Y5-R2FR-scalar-gauge-coupling-owner-DXlambda-zero-or-alpha-bound-runner.md",
            "next_script": "scripts/Y5_R2FR_3526_scalar_gauge_coupling_owner_DXlambda_zero_or_alpha_bound_runner.py",
            "objective": "Try to derive D_X ln(lambda_A/e_obs^2)=0 from parent charge/current/gauge-norm/source-normalization ownership; if it fails, create numeric-ready alpha_EM/WEP/R10/clock/source-normalization bound rows.",
            "success_gate": "Either the scalar F2 prefactor is parent-fixed in the physical source direction, or C_XF2 rows have real units, source paths, projections and no placeholder parent coefficients.",
            "why_next": "3525 reduces the visible EM side to the scalar coupling throat; this is the coupling missing in the local-GR/Newton/Maxwell source route.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append({"check_id": "VAL3525_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited local source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3525_1_branch_selected", "passed": bool_text(any(row["branch_id"] == "BR3525_0_visible_EM_first" and row["selected"] == "True" for row in branches)), "detail": "visible EM branch selected as least-circular first owner route", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3525_2_q_stack_deferred_not_ignored", "passed": bool_text(any(row["branch_id"] == "BR3525_1_q_stack_first" and "MISSING_PARENT_Q_MAP" in row["blocking_clause"] for row in branches) and any(row["gate_id"] == "G3525_5_q_stack_deferred" for row in gates)), "detail": "q-stack branch blockers are explicitly retained", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3525_3_normal_form_written", "passed": bool_text(any(row["theorem_id"] == "VEM3525_0_domain_normal_form" and "lambda_A" in row["normal_form"] for row in reductions)), "detail": "visible EM action normal form is written", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3525_4_scalar_throat_identified", "passed": bool_text(any(row["coefficient"] == "C_XF2" and "scalar coupling throat" in row["current_reduction"] for row in requirements) and any(row["status_id"] == "STAT3525_2_scalar_throat" and row["value"] == "not_derived" for row in status)), "detail": "C_XF2 / D_X ln(lambda_A/e_obs^2) is identified as the surviving coupling throat", "valid_for_claim": "False"})
    required_coeffs = {"Delta_chi_principal", "Delta_chi_skewon", "Delta_chi_axion_gradient", "C_Hodge_hidden", "C_Hodge_readout", "C_XF2", "Delta_conformal_scale"}
    checks.append({"check_id": "VAL3525_5_residual_requirements_complete", "passed": bool_text({row["coefficient"] for row in requirements} >= required_coeffs), "detail": "all 3506 residual components have source/unit/projection requirements", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3525_6_no_claim_flags_true", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + reductions + gates + requirements + status) and all(row["claim_allowed"] == "False" for row in branches + decisions + next_rows)), "detail": "no local-GR/Newton/Maxwell/source-coupling claim is promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3525_7_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3526-Y5-R2FR-scalar-gauge-coupling-owner")), "detail": "3526 scalar-coupling target selected", "valid_for_claim": "False"})
    parse_ok = True
    parsed: list[str] = []
    for name, path in outputs.items():
        if name in {"doc", "validation"}:
            continue
        try:
            read_csv_rows(path)
            parsed.append(name)
        except Exception:
            parse_ok = False
            parsed.append(f"{name}:PARSE_FAIL")
    checks.append({"check_id": "VAL3525_8_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3525_9_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3525_10_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3525_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    status: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3525 - Visible EM Action-Domain Exhaustion Or Q-Stack Owner First Branch

## Summary
- **Branch chosen:** visible EM action-domain/generator first. This is the least-circular route because 3505/3506 already narrow the EM sector before the full q/e_obs/tau/source stack has to close.
- **Actual derivation gained:** under visible U(1), no-extra-tensor action domain, Lorentz naturality and reciprocal action, the EM action reduces to Maxwell normal form plus scalar prefactor and possible axion term.
- **Important consequence:** principal constitutive chaos, skewon response and hidden/readout Hodge branches now have exact conditional zero routes instead of being a shapeless missing list.
- **Still not a claim:** the scalar F2 prefactor `lambda_A/e_obs^2` is not derived. That is the coupling throat feeding alpha, WEP/R10, clocks, binding and EM source weight.
- **q-stack not discarded:** the 2588 q/e_obs/tau/ell_J owner route is deferred because it currently asks for most of the whole local branch at once.

## Normal-Form Result
`S_EM = -1/2 int lambda_A F_Q wedge *_obs F_Q + 1/2 int theta_A F_Q wedge F_Q + int A_Q wedge J_Q + boundary`

If `lambda_A/e_obs^2` is parent-fixed and `theta_A` is constant or absent, this is ordinary Maxwell stress on the observed geometry. If not, the surviving residual is not vague: it is `C_XF2 = D_X ln(lambda_A/e_obs^2)` plus axion/readout/source-normalization tails.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Branch Selection
{markdown_table(branches, ["branch_id", "candidate", "input_stack", "derivation_move", "why_less_circular", "blocking_clause", "selected", "claim_allowed"])}

## Visible EM Reduction Theorems
{markdown_table(reductions, ["theorem_id", "claim_piece", "premises", "derivation", "normal_form", "zero_result", "surviving_frontier", "status", "valid_for_claim"])}

## Owner Clause Gates
{markdown_table(gates, ["gate_id", "owner_clause", "required_signature", "current_status", "if_unsigned", "source_path", "valid_for_claim"])}

## Executable Residual Requirements
{markdown_table(requirements, ["requirement_id", "coefficient", "current_reduction", "needed_numeric_row", "units", "source_requirement", "projection_requirement", "valid_for_claim"])}

## Canonical Status
{markdown_table(status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    branches = branch_selection_rows()
    reductions = visible_em_reduction_rows()
    gates = owner_clause_gate_rows()
    requirements = executable_requirement_rows()
    status = status_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3525_SOURCE_REGISTER.csv",
        "branch_selection": OUT / "P8_Y5_R2FR_3525_BRANCH_SELECTION.csv",
        "visible_em_reduction": OUT / "P8_Y5_R2FR_3525_VISIBLE_EM_REDUCTION_THEOREM.csv",
        "owner_clause_gates": OUT / "P8_Y5_R2FR_3525_OWNER_CLAUSE_GATES.csv",
        "executable_requirements": OUT / "P8_Y5_R2FR_3525_EXECUTABLE_RESIDUAL_REQUIREMENTS.csv",
        "status": OUT / "P8_Y5_R2FR_3525_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "decision_ledger": OUT / "P8_Y5_R2FR_3525_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3525_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3525_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["branch_selection"], branches, ["branch_id", "candidate", "input_stack", "derivation_move", "why_less_circular", "blocking_clause", "selected", "claim_allowed"])
    write_csv(outputs["visible_em_reduction"], reductions, ["theorem_id", "claim_piece", "premises", "derivation", "normal_form", "zero_result", "surviving_frontier", "status", "valid_for_claim"])
    write_csv(outputs["owner_clause_gates"], gates, ["gate_id", "owner_clause", "required_signature", "current_status", "if_unsigned", "source_path", "valid_for_claim"])
    write_csv(outputs["executable_requirements"], requirements, ["requirement_id", "coefficient", "current_reduction", "needed_numeric_row", "units", "source_requirement", "projection_requirement", "valid_for_claim"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, branches, reductions, gates, requirements, status, decisions, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, branches, reductions, gates, requirements, status, decisions, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
