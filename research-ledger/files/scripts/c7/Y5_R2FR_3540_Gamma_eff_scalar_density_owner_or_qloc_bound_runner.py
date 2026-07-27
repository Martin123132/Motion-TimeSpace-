from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3540-Y5-R2FR-Gamma-eff-scalar-density-owner-or-qloc-bound-runner.md"
CANONICAL_STATUS = OUT / "P8_Gamma_Khat_parent_response_or_qloc_bound_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3540": {"path": Path(__file__).resolve(), "role": "3540 generator"},
    "doc_3539": {
        "path": ROOT / "3539-Y5-R2FR-qloc-Gamma-Khat-Ward-residual-no-flux-or-PPN-bound-vector.md",
        "role": "q_loc Ward residual derivation handoff",
    },
    "next_3539": {
        "path": OUT / "P8_Y5_R2FR_3539_NEXT_TARGET.csv",
        "role": "selected Gamma_eff/Khat or q_loc-bound target",
    },
    "profile_3539": {
        "path": OUT / "P8_Y5_R2FR_3539_QLOC_PROFILE_LAWS.csv",
        "role": "q_loc profile law with E_A, B_GK and Delta_K",
    },
    "bound_vector_3539": {
        "path": OUT / "P8_Y5_R2FR_3539_PPN_BOUND_VECTOR.csv",
        "role": "PPN/local bound rows from q_loc residual",
    },
    "gamma_candidate_516": {
        "path": OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
        "role": "response-doublet Gamma_eff action candidates",
    },
    "response_contract_516": {
        "path": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
        "role": "response-doublet action contract",
    },
    "response_variation_517": {
        "path": OUT / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
        "role": "response-doublet variation and double-zero equations",
    },
    "response_metric_517": {
        "path": OUT / "P8_RESPONSE_DOUBLET_METRIC_RESPONSE_LEDGER.csv",
        "role": "metric-response terms and Khat hazards",
    },
    "response_euler_517": {
        "path": OUT / "P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv",
        "role": "Y0-Y6 source and boundary problems",
    },
    "response_obstructions_517": {
        "path": OUT / "P8_RESPONSE_DOUBLET_OBSTRUCTION_LEDGER.csv",
        "role": "Y5/Y6/PPN lock and boundary obstructions",
    },
    "bound_trigger_517": {
        "path": OUT / "P8_QLOC_BOUND_TRIGGER_LEDGER.csv",
        "role": "q_loc fallback triggers",
    },
    "qbound_spec_516": {
        "path": OUT / "P8_QLOC_BOUND_RUNNER_SPEC.csv",
        "role": "older q_loc bound runner requirements",
    },
    "symbol_map": {
        "path": OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "role": "Gamma/Khat/q_loc/P_loc symbol-action placement",
    },
    "first_variation_gates": {
        "path": OUT / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv",
        "role": "Gamma/Khat/q_loc first variation gate",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "empirical WEP/PPN/Gdot/R10/R11 bounds",
    },
    "r11_vector": {
        "path": OUT / "R11_nonEH_operator_vector_executable.csv",
        "role": "R11 non-EH operator vector",
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


def parent_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "construction_id": "PAC3540_0_response_variables",
            "object": "Y^A response coordinates",
            "formula": "Y^A = local kernel/residual coordinates including trace, projector, boundary, domain vector, domain STF, source normalization, and extra stress channels",
            "derivation": "Use the 3534-3539 local kernel stack as the variable target; do not let Y^A be auxiliary shadows unless PPN/source rows lock them to observables.",
            "what_it_kills": "none by itself",
            "remaining_debt": "PPN lock for Y5 source normalization and Y6 extra stress",
            "current_status": "TARGET_COORDINATES_DECLARED_NOT_PARENT_SIGNED",
            "claim_allowed": "False",
        },
        {
            "construction_id": "PAC3540_1_scalar_density",
            "object": "Gamma_eff",
            "formula": "Gamma_eff = Gamma0 + 1/2 G_AB g^{mu nu} D_mu Y^A D_nu Y^B + 1/2 M_AB Y^A Y^B + O(Y^4)",
            "derivation": "This is a covariant scalar action density once G_AB, M_AB, D_mu and Y^A are parent-owned tensors/sections.",
            "what_it_kills": "linear Gamma source term; Gamma_eff-Gamma0 and partial_A Gamma_eff vanish at Y=0",
            "remaining_debt": "parent ownership of G_AB/M_AB/D_mu/Y^A and proof no hidden linear J_A Y^A term",
            "current_status": "CLEAN_PARENT_ACTION_CANDIDATE",
            "claim_allowed": "False",
        },
        {
            "construction_id": "PAC3540_2_define_Khat",
            "object": "K_hat^{mu nu}",
            "formula": "K_hat^{mu nu} := K_metric^{mu nu}[Gamma_eff] = G_AB D^mu Y^A D^nu Y^B + K_extra^{mu nu}[delta_g G, delta_g M, delta_g D, delta_g Y]",
            "derivation": "If MTS promotes this definition, Delta_K=K_hat-K_metric is zero by construction.",
            "what_it_kills": "the 3539 Delta_K branch in the clean parent-response construction",
            "remaining_debt": "must prove existing K_hat symbol equals this response, not merely rename it",
            "current_status": "DELTA_K_ZERO_IN_CLEAN_BRANCH_ONLY",
            "claim_allowed": "False",
        },
        {
            "construction_id": "PAC3540_3_Euler_operator",
            "object": "Y^A Euler equations",
            "formula": "L_AB Y^B = J_A + B_A, with L_AB = -D_mu(G_AB D^mu) + M_AB + curvature/projector terms",
            "derivation": "Vary S_GK with respect to Y^A; if L_AB is positive and J_A=B_A=0, the compact local solution is Y^A=0.",
            "what_it_kills": "E_A term in q_loc and local finite-range tails in source-free compact vacuum",
            "remaining_debt": "J_A=0 for Y5/Y6 and B_A=0 for boundary/domain channels are not proved",
            "current_status": "EULER_ZERO_ROUTE_BUILT_NOT_SOURCED",
            "claim_allowed": "False",
        },
        {
            "construction_id": "PAC3540_4_Ward_reduction",
            "object": "q_loc^nu",
            "formula": "q_loc^nu = P_loc^nu_rho(E_A R_A^rho + B_GK^rho) in the clean Delta_K=0 branch",
            "derivation": "Combine the metric-response definition with 3539 Ward identity.",
            "what_it_kills": "q_loc if E_A=0, B_GK=0, and P_loc is parent-owned",
            "remaining_debt": "boundary/domain no-flux and P_loc observed-quotient ownership",
            "current_status": "WARD_REDUCTION_EXACT_CONDITIONAL",
            "claim_allowed": "False",
        },
    ]


def metric_response_rows() -> list[dict[str, Any]]:
    return [
        {
            "response_id": "MR3540_0_variation_identity",
            "piece": "metric variation",
            "equation": "delta(sqrt(-g)Gamma_eff)=1/2 sqrt(-g)(Gamma_eff g^{mu nu}-K_metric^{mu nu})delta g_{mu nu}+sqrt(-g)E_A delta Y^A+dTheta",
            "result": "Defines K_metric and locks the stress to one variational object.",
            "deltaK_status": "ZERO_IF_KHAT_DEFINED_AS_KMETRIC",
            "claim_allowed": "False",
        },
        {
            "response_id": "MR3540_1_potential_piece",
            "piece": "1/2 M_AB Y^A Y^B",
            "equation": "K_potential^{mu nu}= -2 partial_g^{mu nu}(1/2 M_AB Y^A Y^B) plus convention terms; if M_AB,Y are metric-independent at fixed readout then K_potential=0",
            "result": "Potential-only quadratic Gamma has no local stress at Y=0 and no first variation.",
            "deltaK_status": "CONDITIONAL_ON_METRIC_LOCK",
            "claim_allowed": "False",
        },
        {
            "response_id": "MR3540_2_kinetic_piece",
            "piece": "1/2 G_AB g^{alpha beta}D_alphaY^A D_betaY^B",
            "equation": "K_kin^{mu nu}=G_AB D^muY^A D^nuY^B plus response terms from G_AB,D,Y metric dependence",
            "result": "K_kin is quadratic in local deviations if the metric-dependence of the readout variables is regular.",
            "deltaK_status": "REGULAR_BUT_PPN_LOCK_OPEN",
            "claim_allowed": "False",
        },
        {
            "response_id": "MR3540_3_boundary_piece",
            "piece": "integration by parts and domain/projector collars",
            "equation": "K_boundary^{mu nu} enters through dTheta_GK and projector/domain variation",
            "result": "Bulk Delta_K can be zero while boundary/domain B_GK still sources q_loc.",
            "deltaK_status": "BOUNDARY_NOT_KILLED_BY_DEFINITION",
            "claim_allowed": "False",
        },
        {
            "response_id": "MR3540_4_existing_symbol_test",
            "piece": "current MTS K_hat",
            "equation": "Delta_K^{mu nu}=K_hat_existing^{mu nu}-K_metric^{mu nu}[Gamma_eff]",
            "result": "Existing symbols pass only if the current K_hat formula is shown to equal the response formula.",
            "deltaK_status": "NOT_PROVED_FOR_CURRENT_CORPUS",
            "claim_allowed": "False",
        },
    ]


def fork_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "FT3540_0_clean_parent_branch",
            "test": "Adopt Gamma_eff as a scalar density and define K_hat as its metric response.",
            "result": "Delta_K can be killed in the clean branch.",
            "blocks": "does not prove old K_hat symbol or all MTS source channels match the branch",
            "next_action": "lock Y^A to physical PPN/source residual vector",
            "claim_allowed": "False",
        },
        {
            "test_id": "FT3540_1_existing_MTS_branch",
            "test": "Use existing Gamma_eff/K_hat appearances without rewriting them as a response pair.",
            "result": "Delta_K remains open.",
            "blocks": "local-GR/Newton/PPN pass",
            "next_action": "fill q_loc bound runner coefficients",
            "claim_allowed": "False",
        },
        {
            "test_id": "FT3540_2_source_zero",
            "test": "Set J_A=0 in the Euler equation.",
            "result": "fails for claim because Y5 source-normalization and Y6 extra stress are not source-zeroed.",
            "blocks": "Newton/source coupling and EH-only exterior",
            "next_action": "derive Y5/Y6 source lock or component coefficients",
            "claim_allowed": "False",
        },
        {
            "test_id": "FT3540_3_boundary_zero",
            "test": "Set B_A and B_GK to zero.",
            "result": "not signed; boundary/domain alpha3 pressure remains.",
            "blocks": "R7 alpha3 and domain flux claims",
            "next_action": "boundary/domain no-flux theorem or alpha3 coefficient fill",
            "claim_allowed": "False",
        },
        {
            "test_id": "FT3540_4_bound_runner",
            "test": "Instantiate q_loc coefficient rows when any structural clause fails.",
            "result": "runner inputs are now staged by source term E_A, B_GK, Delta_K and observable row.",
            "blocks": "numerical claim until coefficients are real",
            "next_action": "fill first hard coefficients, starting Y5/Y6 and alpha3",
            "claim_allowed": "False",
        },
    ]


def bound_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_row": "QBR3540_0_Euler_Y5_source",
            "source_term": "E_A R_A",
            "component": "Y5_source_normalization",
            "observable_rows": "R1_WEP_source_charge;R4_beta;R9_Gdot;R11_EH_operator_ledger",
            "coefficient_needed": "C_Y5_to_eta_source, C_Y5_to_beta, C_Y5_to_Gdot, c_domain_source_normalization_operator",
            "current_value": "MISSING_NUMERIC_PARENT_INPUT",
            "bound_reference": "MICROSCOPE eta<=2.8e-15; beta<=7.8e-5; Gdot/G<=9.6e-15 yr^-1",
            "status": "HARD_BLOCK_SOURCE_COUPLING",
            "valid_for_claim": "False",
        },
        {
            "runner_row": "QBR3540_1_Euler_Y6_stress",
            "source_term": "E_A R_A",
            "component": "Y6_extra_stress",
            "observable_rows": "R3_gamma;R4_beta;R8_xi;R11_EH_operator_ledger",
            "coefficient_needed": "C_Y6_to_gamma, C_Y6_to_beta, C_Y6_to_xi, T_extra_operator_vector",
            "current_value": "MISSING_STRESS_PROJECTION",
            "bound_reference": "gamma<=2.3e-5; beta<=7.8e-5; xi<=4e-9",
            "status": "HARD_BLOCK_EH_ONLY_EXTERIOR",
            "valid_for_claim": "False",
        },
        {
            "runner_row": "QBR3540_2_boundary_flux",
            "source_term": "B_GK",
            "component": "boundary/collar flux",
            "observable_rows": "R7_alpha3;R10_fifth_force;R11_EH_operator_ledger",
            "coefficient_needed": "C_boundary_alpha3, tau_R10_boundary, c_boundary_operator",
            "current_value": "MISSING_BOUNDARY_NOFLUX_OR_COEFFICIENT",
            "bound_reference": "alpha3<=4e-20; alpha(lambda) curve required",
            "status": "HIGHEST_PRESSURE_BOUNDARY_ROW",
            "valid_for_claim": "False",
        },
        {
            "runner_row": "QBR3540_3_domain_vector",
            "source_term": "B_GK or E_A R_A",
            "component": "domain vector/domain exchange",
            "observable_rows": "R5_alpha1;R6_alpha2;R7_alpha3",
            "coefficient_needed": "C_domain_alpha1, C_domain_alpha2, C_domain_alpha3",
            "current_value": "MISSING_DOMAIN_VECTOR_COEFFICIENTS",
            "bound_reference": "alpha1<=1e-4; alpha2<=2e-9; alpha3<=4e-20",
            "status": "DOMAIN_VECTOR_NOT_SCOREABLE",
            "valid_for_claim": "False",
        },
        {
            "runner_row": "QBR3540_4_DeltaK_existing_symbol",
            "source_term": "-div Delta_K",
            "component": "existing K_hat mismatch",
            "observable_rows": "R3_gamma;R4_beta;R5_alpha1;R6_alpha2;R7_alpha3;R8_xi;R11_EH_operator_ledger",
            "coefficient_needed": "Delta_K_operator_norm and weak-field projection matrix",
            "current_value": "ZERO_IN_CLEAN_BRANCH_NOT_PROVED_FOR_EXISTING_SYMBOL",
            "bound_reference": "PPN vector and R11 operator ledger",
            "status": "MUST_PROVE_EQUALITY_OR_SCORE",
            "valid_for_claim": "False",
        },
        {
            "runner_row": "QBR3540_5_R10_mass_gap",
            "source_term": "finite-range Y^A tail",
            "component": "lambda_A=sqrt(Z_A/M_A^2)",
            "observable_rows": "R10_fifth_force",
            "coefficient_needed": "Z_A, M_A^2, source charge C_A, alpha(lambda)",
            "current_value": "MISSING_Z_M2_SOURCE_CHARGE",
            "bound_reference": "alpha(lambda) curve required",
            "status": "R10_NOT_CLAIM_READY",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3540_0_parent_response_constructed",
            "decision": "A clean parent-response action can kill Delta_K by definition.",
            "rationale": "Once Gamma_eff is a scalar action density and K_hat is defined as its metric response, the 3539 mismatch term disappears.",
            "effect": "The best derivation route is no longer vague; it is a concrete action branch.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3540_1_not_old_symbol_claim",
            "decision": "Do not claim the existing corpus already has Delta_K=0.",
            "rationale": "Existing Gamma_eff/K_hat symbols have not been matched to the new response formula.",
            "effect": "The work avoids a rename-as-proof trap.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3540_2_source_coupling_is_now_central",
            "decision": "Move the next attack to Y5/Y6 source-normalization and extra-stress lock.",
            "rationale": "Even the clean Delta_K branch fails local GR/Newton if source coupling and extra stress are not zeroed or bounded.",
            "effect": "Next target focuses on calibrated source coupling, not another generic Gamma audit.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3540_3_bound_runner_active",
            "decision": "Keep the q_loc bound runner active for every unsigned clause.",
            "rationale": "Alpha3, R10 and R11 are too tight to be deferred without rows.",
            "effect": "The theory has an explicit fallback if Y5/Y6/source lock cannot be derived.",
            "claim_allowed": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3540_0_DeltaK_clean",
            "quantity": "Delta_K in clean parent branch",
            "value": "zero_by_definition_if_Khat_is_metric_response",
            "meaning": "the metric-response action branch removes the 3539 Khat-mismatch term",
            "claim_effect": "candidate branch only",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3540_1_DeltaK_existing",
            "quantity": "Delta_K for current corpus symbols",
            "value": "not_proved_zero",
            "meaning": "existing K_hat must still be matched to K_metric[Gamma_eff]",
            "claim_effect": "no local-GR pass",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3540_2_source_coupling",
            "quantity": "Y5/Y6 source lock",
            "value": "hard_next_hinge",
            "meaning": "source normalization and extra stress survive the response-doublet trick unless explicitly derived",
            "claim_effect": "Newton/source-calibration route remains blocked",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3540_3_bound_runner",
            "quantity": "q_loc bound runner",
            "value": "staged_by_E_B_DeltaK_components",
            "meaning": "if a proof clause fails, coefficients are assigned to WEP/PPN/Gdot/R10/R11 rows",
            "claim_effect": "nonclaim until numeric/source coefficients exist",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3541-Y5-R2FR-Y5-Y6-source-coupling-lock-or-first-qloc-coefficients.md",
            "next_script": "scripts/Y5_R2FR_3541_Y5_Y6_source_coupling_lock_or_first_qloc_coefficients.py",
            "objective": "Try to derive that source-normalization Y5 and extra-stress Y6 are absent, topological, or quotient-invisible in the clean parent-response branch; if not, fill the first q_loc coefficient rows for WEP/source charge, beta/gamma, Gdot, alpha3 and R11.",
            "success_gate": "Either Y5/Y6 are theorem-zero/invisible under the same parent action, or the first source-coupling and extra-stress coefficients become explicit nonclaim numeric/source rows.",
            "why_next": "3540 kills Delta_K only in the clean branch; the remaining route to local GR/Newton is now source coupling and extra stress.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    parent_actions: list[dict[str, Any]],
    metric_responses: list[dict[str, Any]],
    fork_tests: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    action_ids = {row["construction_id"] for row in parent_actions}
    response_ids = {row["response_id"] for row in metric_responses}
    runner_ids = {row["runner_row"] for row in runner_rows}
    checks.append({"check_id": "VAL3540_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3540_1_parent_action_constructed", "passed": bool_text({"PAC3540_1_scalar_density", "PAC3540_2_define_Khat", "PAC3540_3_Euler_operator", "PAC3540_4_Ward_reduction"} <= action_ids), "detail": "Gamma_eff scalar density, Khat metric response, Euler operator and Ward reduction are present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3540_2_metric_response_has_DeltaK_branch", "passed": bool_text({"MR3540_0_variation_identity", "MR3540_4_existing_symbol_test"} <= response_ids), "detail": "metric response and existing-symbol Delta_K test present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3540_3_clean_branch_not_overclaimed", "passed": bool_text(any(row["test_id"] == "FT3540_0_clean_parent_branch" and row["claim_allowed"] == "False" for row in fork_tests) and any(row["test_id"] == "FT3540_1_existing_MTS_branch" and row["claim_allowed"] == "False" for row in fork_tests)), "detail": "clean branch and existing-symbol branch are separated as nonclaims", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3540_4_bound_runner_covers_E_B_DeltaK", "passed": bool_text({"QBR3540_0_Euler_Y5_source", "QBR3540_1_Euler_Y6_stress", "QBR3540_2_boundary_flux", "QBR3540_4_DeltaK_existing_symbol", "QBR3540_5_R10_mass_gap"} <= runner_ids), "detail": "Euler, boundary, Delta_K and R10 rows staged", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3540_5_source_coupling_next_hinge", "passed": bool_text(any(row["decision_id"] == "DEC3540_2_source_coupling_is_now_central" for row in decisions) and next_rows[0]["next_doc"].startswith("3541-Y5-R2FR-Y5-Y6")), "detail": "Y5/Y6 source-coupling target selected", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3540_6_no_claims_promoted", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + status + runner_rows) and all(row.get("claim_allowed", "False") == "False" for row in parent_actions + metric_responses + fork_tests + decisions + next_rows)), "detail": "no local-GR/Newton/PPN claim promoted", "valid_for_claim": "False"})
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
    checks.append({"check_id": "VAL3540_7_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3540_8_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3540_9_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3540_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    parent_actions: list[dict[str, Any]],
    metric_responses: list[dict[str, Any]],
    fork_tests: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3540 - Gamma_eff Scalar-Density Owner Or q_loc Bound Runner

## Summary
- **Leap made:** a clean parent-response branch is now explicit: `Gamma_eff` is a covariant scalar action density and `K_hat` is defined as its metric response.
- **Delta_K result:** in that clean branch, `Delta_K = K_hat - K_metric[Gamma_eff]` is zero by construction.
- **No rename trick:** the existing corpus does not yet prove its old `K_hat` symbol equals this response formula.
- **Remaining hard hinge:** even with `Delta_K=0`, local GR/Newton still needs source-normalization `Y5` and extra-stress `Y6` to be absent, topological, quotient-invisible, or coefficient-bounded.
- **Fallback active:** q_loc bound-runner rows are staged by Euler leakage, boundary/domain flux, existing-symbol `Delta_K`, and R10/R11 tails.

## Clean Parent-Response Construction
Use local response coordinates `Y^A` and take

`Gamma_eff = Gamma0 + 1/2 G_AB g^{{mu nu}} D_mu Y^A D_nu Y^B + 1/2 M_AB Y^A Y^B + O(Y^4)`.

Then define

`K_hat^{{mu nu}} := K_metric^{{mu nu}}[Gamma_eff]`.

With this definition the 3539 mismatch term vanishes:

`Delta_K^{{mu nu}} = K_hat^{{mu nu}} - K_metric^{{mu nu}}[Gamma_eff] = 0`.

The q_loc profile reduces to

`q_loc^nu = P_loc^nu_rho(E_A R_A^rho + B_GK^rho)`.

That is real progress, but only for the clean branch. It does not prove the old corpus symbols already satisfy the same response identity, and it does not kill `Y5/Y6` source coupling.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Parent Action Construction
{markdown_table(parent_actions, ["construction_id", "object", "formula", "derivation", "what_it_kills", "remaining_debt", "current_status", "claim_allowed"])}

## Metric Response Ledger
{markdown_table(metric_responses, ["response_id", "piece", "equation", "result", "deltaK_status", "claim_allowed"])}

## Fork Tests
{markdown_table(fork_tests, ["test_id", "test", "result", "blocks", "next_action", "claim_allowed"])}

## q_loc Bound Runner Rows
{markdown_table(runner_rows, ["runner_row", "source_term", "component", "observable_rows", "coefficient_needed", "current_value", "bound_reference", "status", "valid_for_claim"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Canonical Status
{markdown_table(status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    parent_actions = parent_action_rows()
    metric_responses = metric_response_rows()
    fork_tests = fork_test_rows()
    runner_rows = bound_runner_rows()
    decisions = decision_rows()
    status = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3540_SOURCE_REGISTER.csv",
        "parent_action": OUT / "P8_Y5_R2FR_3540_PARENT_RESPONSE_ACTION.csv",
        "metric_response": OUT / "P8_Y5_R2FR_3540_METRIC_RESPONSE_DELTAK_LEDGER.csv",
        "fork_tests": OUT / "P8_Y5_R2FR_3540_FORK_TESTS.csv",
        "bound_runner": OUT / "P8_Y5_R2FR_3540_QLOC_BOUND_RUNNER_ROWS.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3540_DECISION_LEDGER.csv",
        "status": OUT / "P8_Y5_R2FR_3540_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "next_target": OUT / "P8_Y5_R2FR_3540_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3540_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["parent_action"], parent_actions, ["construction_id", "object", "formula", "derivation", "what_it_kills", "remaining_debt", "current_status", "claim_allowed"])
    write_csv(outputs["metric_response"], metric_responses, ["response_id", "piece", "equation", "result", "deltaK_status", "claim_allowed"])
    write_csv(outputs["fork_tests"], fork_tests, ["test_id", "test", "result", "blocks", "next_action", "claim_allowed"])
    write_csv(outputs["bound_runner"], runner_rows, ["runner_row", "source_term", "component", "observable_rows", "coefficient_needed", "current_value", "bound_reference", "status", "valid_for_claim"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, parent_actions, metric_responses, fork_tests, runner_rows, decisions, status, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, parent_actions, metric_responses, fork_tests, runner_rows, decisions, status, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
