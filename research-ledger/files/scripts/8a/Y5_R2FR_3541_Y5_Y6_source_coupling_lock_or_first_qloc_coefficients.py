from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3541-Y5-R2FR-Y5-Y6-source-coupling-lock-or-first-qloc-coefficients.md"
CANONICAL_STATUS = OUT / "P8_Y5_Y6_source_coupling_lock_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3541": {"path": Path(__file__).resolve(), "role": "3541 generator"},
    "doc_3540": {
        "path": ROOT / "3540-Y5-R2FR-Gamma-eff-scalar-density-owner-or-qloc-bound-runner.md",
        "role": "Gamma/Khat clean parent-response handoff",
    },
    "next_3540": {
        "path": OUT / "P8_Y5_R2FR_3540_NEXT_TARGET.csv",
        "role": "selected Y5/Y6 source coupling target",
    },
    "runner_3540": {
        "path": OUT / "P8_Y5_R2FR_3540_QLOC_BOUND_RUNNER_ROWS.csv",
        "role": "q_loc bound runner rows by E/B/DeltaK source term",
    },
    "newton_stack": {
        "path": OUT / "P8_source_normalized_Newton_branch_STACK.csv",
        "role": "source-normalized Newton branch requirements",
    },
    "source_theorem_stack": {
        "path": OUT / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
        "role": "source-normalization theorem stack",
    },
    "source_channel_audit": {
        "path": OUT / "P8_SOURCE_NORMALIZATION_CHANNEL_AUDIT.csv",
        "role": "source-normalization channel audit",
    },
    "hilbert_contract": {
        "path": OUT / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
        "role": "Hilbert monopole calibration contract",
    },
    "mu_extra_vector": {
        "path": OUT / "P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv",
        "role": "mu_extra source-normalization coefficient vector",
    },
    "r11_source_min": {
        "path": OUT / "P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv",
        "role": "minimum R11 source-normalization fill rows",
    },
    "r11_source_gates": {
        "path": OUT / "P8_R11_SOURCE_NORMALIZATION_ACCEPTANCE_GATES.csv",
        "role": "R11/source-normalization acceptance gates",
    },
    "y5_affine_status": {
        "path": OUT / "P8_Y5_AFFINE_SOURCE_GATE_2608_SOURCE_ZERO_STATUS.csv",
        "role": "Y5 affine source-zero status",
    },
    "y5_centered_origin": {
        "path": OUT / "P8_Y5_AFFINE_SOURCE_GATE_2608_CENTERED_ORIGIN_THEOREM_ATTEMPT.csv",
        "role": "centered-origin theorem attempt",
    },
    "y5_affine_bounds": {
        "path": OUT / "P8_Y5_AFFINE_SOURCE_GATE_2608_AFFINE_SOURCE_BOUND_ROWS.csv",
        "role": "Y5 affine source bound rows",
    },
    "y5_beta_input": {
        "path": OUT / "P8_Y5_BETA_COEFFICIENT_FILL_INPUT.csv",
        "role": "beta source coefficient fill template",
    },
    "constant_gm_runner": {
        "path": OUT / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
        "role": "constant GM local residual runner input",
    },
    "response_euler_517": {
        "path": OUT / "P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv",
        "role": "Y0-Y6 source and boundary problems from response branch",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "empirical WEP/PPN/Gdot/R10/R11 bounds",
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


def source_lock_rows() -> list[dict[str, Any]]:
    return [
        {
            "lock_id": "SCL3541_0_universal_matter_descent",
            "target": "Y5 source charge",
            "theorem_clause": "Ordinary matter action descends only through one observed coframe/metric: S_matter[psi,e_obs], with no direct Y5, marker, species, or source-only scalar slot.",
            "mathematical_result": "delta_Y5 S_matter = (delta S_matter/delta e_obs) D_Y5 e_obs = 0 if D_Y5 e_obs=0 and the matter lift is fixed/gauge.",
            "what_this_would_kill": "composition/source charge eta_source and source-only WEP leakage",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "claim_allowed": "False",
        },
        {
            "lock_id": "SCL3541_1_constant_universal_kappa",
            "target": "Y5 G_eff/source normalization",
            "theorem_clause": "kappa_eff is a parent topological/superselected constant independent of source, species, time, range, frame, and domain labels.",
            "mathematical_result": "partial_Y5 kappa_eff = partial_t kappa_eff = partial_lambda kappa_eff = 0, so Y5 cannot enter measured GM through G_eff.",
            "what_this_would_kill": "Gdot, range-dependent G, species-dependent source normalization",
            "current_status": "NOT_PARENT_DERIVED",
            "claim_allowed": "False",
        },
        {
            "lock_id": "SCL3541_2_Hilbert_monopole_lock",
            "target": "Y5 measured mass",
            "theorem_clause": "The Hamiltonian/Gauss monopole equals the projected Hilbert matter current in the same observed frame.",
            "mathematical_result": "mu_obs = G_eff M_Hilbert and d(Pi_M J_H)=0 in the compact local exterior.",
            "what_this_would_kill": "hidden boundary/domain/bulk monopole terms in Newtonian GM",
            "current_status": "CONTRACT_EXISTS_NOT_PARENT_DERIVED",
            "claim_allowed": "False",
        },
        {
            "lock_id": "SCL3541_3_no_source_only_slot",
            "target": "Y5 affine/linear source",
            "theorem_clause": "The clean parent action has no term J_A(q,material)Y5^A, no shifted local origin X0(q), and no invariant marker covector ell_marker.",
            "mathematical_result": "J_Y5=0 follows from a parent zero section, norm-square-only activation, and no nonzero natural source section.",
            "what_this_would_kill": "F_1 affine source and leading hidden source residual",
            "current_status": "CENTERED_ORIGIN_THEOREM_READY_PARENT_UNSIGNED",
            "claim_allowed": "False",
        },
        {
            "lock_id": "SCL3541_4_Y6_quadratic_response_stress",
            "target": "Y6 extra stress",
            "theorem_clause": "All extra stress comes from the quadratic response action, topological constants, or exact improvements, with no independent conserved stress block.",
            "mathematical_result": "T_extra(0)=0 and partial_A T_extra(0)=0 if Gamma_eff-Gamma0=O(Y^2), K_hat=K_metric, and boundary improvements are silent.",
            "what_this_would_kill": "gamma/beta/xi/R11 extra-stress leakage",
            "current_status": "CLEAN_BRANCH_CONDITIONAL_NOT_EXISTING_CORPUS_PROOF",
            "claim_allowed": "False",
        },
        {
            "lock_id": "SCL3541_5_combined_verdict",
            "target": "local GR/Newton source coupling",
            "theorem_clause": "SCL3541_0 through SCL3541_4 all hold in one parent action and one observed frame.",
            "mathematical_result": "Y5/Y6 source terms vanish; q_loc clean branch has no source-coupling/extra-stress residual at linear order.",
            "what_this_would_kill": "main source-coupling block to local Newton/GR",
            "current_status": "NOT_CLAIMED",
            "claim_allowed": "False",
        },
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    return [
        {
            "obstruction_id": "OBS3541_0_even_source_scalar",
            "channel": "Y5_source_normalization",
            "why_it_survives": "Measured GM/source normalization is exchange-even and can survive a response-doublet odd-sector zero theorem.",
            "effect": "The clean Gamma/Khat branch does not by itself derive Newtonian source normalization.",
            "required_fix": "universal constant kappa plus Hilbert monopole lock or explicit coefficient row",
            "claim_allowed": "False",
        },
        {
            "obstruction_id": "OBS3541_1_source_only_coupling",
            "channel": "Y5_affine_source",
            "why_it_survives": "A covariant action may legally contain source-only or shifted-origin terms unless the parent algebra forbids them.",
            "effect": "F_1 can reappear even when the quadratic response density exists.",
            "required_fix": "no source-only slot / centered-origin / no-marker theorem",
            "claim_allowed": "False",
        },
        {
            "obstruction_id": "OBS3541_2_conserved_extra_stress",
            "channel": "Y6_extra_stress",
            "why_it_survives": "A conserved non-EH stress can obey Bianchi/Ward identities and still change gamma, beta, xi or R11.",
            "effect": "Ward ownership is not EH-only exterior.",
            "required_fix": "topological/improvement invisibility theorem or coefficient vector",
            "claim_allowed": "False",
        },
        {
            "obstruction_id": "OBS3541_3_boundary_domain_monopoles",
            "channel": "mu_extra_boundary_domain",
            "why_it_survives": "Boundary and domain/projector pieces can shift the monopole or create alpha3 flux while remaining covariant.",
            "effect": "Measured GM can hide residual physics if derivative/source rows are not explicit.",
            "required_fix": "no-flux/no-monopole theorem or alpha3/source-normalization coefficients",
            "claim_allowed": "False",
        },
    ]


def coefficient_rows() -> list[dict[str, Any]]:
    return [
        {
            "coefficient_id": "COEF3541_0_species_source_charge",
            "component": "Y5 species/source charge",
            "symbol": "epsilon_species_A",
            "direct_map_ceiling": "<= 2.8e-15 if eta_source_AB maps one-to-one",
            "units": "dimensionless",
            "observable_rows": "R1_WEP_source_charge;R2_clock_redshift;R11_EH_operator_ledger",
            "bound_source": "MICROSCOPE source-charge proxy in local_bound_claims.csv",
            "needed_for_claim": "selector-blind source theorem or sourced material charge vector",
            "current_status": "NONCLAIM_NUMERIC_CEILING_ONLY_MAP_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "coefficient_id": "COEF3541_1_beta_source",
            "component": "Y5 nonlinear source normalization",
            "symbol": "delta_beta_source",
            "direct_map_ceiling": "<= 7.8e-5 if beta row maps one-to-one",
            "units": "dimensionless",
            "observable_rows": "R4_beta;R11_EH_operator_ledger",
            "bound_source": "Will beta row in local_bound_claims.csv",
            "needed_for_claim": "second-order weak-field source calculation with A_source=B_source=1 and no q_loc/R11 residue",
            "current_status": "NONCLAIM_NUMERIC_CEILING_ONLY_SECOND_ORDER_MAP_MISSING",
            "valid_for_claim": "False",
        },
        {
            "coefficient_id": "COEF3541_2_gamma_extra_stress",
            "component": "Y6 spatial extra stress",
            "symbol": "delta_gamma_extra",
            "direct_map_ceiling": "<= 2.3e-5 if gamma row maps one-to-one",
            "units": "dimensionless",
            "observable_rows": "R3_gamma;R11_EH_operator_ledger",
            "bound_source": "Cassini gamma row in local_bound_claims.csv",
            "needed_for_claim": "weak-field metric solution for extra stress or topological/improvement theorem",
            "current_status": "NONCLAIM_NUMERIC_CEILING_ONLY_STRESS_MAP_MISSING",
            "valid_for_claim": "False",
        },
        {
            "coefficient_id": "COEF3541_3_xi_extra_STF",
            "component": "Y6/domain STF stress",
            "symbol": "epsilon_STF_xi",
            "direct_map_ceiling": "<= 4e-9 if xi row maps one-to-one",
            "units": "dimensionless",
            "observable_rows": "R8_xi;R11_EH_operator_ledger",
            "bound_source": "Will xi row in local_bound_claims.csv",
            "needed_for_claim": "isotropy/topological stress theorem or STF projection coefficient",
            "current_status": "NONCLAIM_NUMERIC_CEILING_ONLY_STF_MAP_MISSING",
            "valid_for_claim": "False",
        },
        {
            "coefficient_id": "COEF3541_4_time_drift",
            "component": "Y5 time-dependent source normalization",
            "symbol": "epsilon_time_drift",
            "direct_map_ceiling": "<= 9.6e-15 yr^-1 if Gdot row maps one-to-one",
            "units": "yr^-1",
            "observable_rows": "R9_Gdot;R11_EH_operator_ledger",
            "bound_source": "LLR Gdot row in local_bound_claims.csv",
            "needed_for_claim": "stationary tau/constant kappa/M_eff theorem or sourced drift coefficient",
            "current_status": "NONCLAIM_NUMERIC_CEILING_ONLY_DRIFT_MAP_MISSING",
            "valid_for_claim": "False",
        },
        {
            "coefficient_id": "COEF3541_5_boundary_domain_alpha3",
            "component": "boundary/domain momentum flux",
            "symbol": "C_alpha3_boundary_domain",
            "direct_map_ceiling": "<= 4e-20 if alpha3 row maps one-to-one",
            "units": "dimensionless",
            "observable_rows": "R7_alpha3;R11_EH_operator_ledger",
            "bound_source": "Will alpha3 row in local_bound_claims.csv",
            "needed_for_claim": "no-flux theorem or explicit projection coefficient to alpha3",
            "current_status": "NONCLAIM_NUMERIC_CEILING_ONLY_HIGHEST_PRESSURE",
            "valid_for_claim": "False",
        },
        {
            "coefficient_id": "COEF3541_6_R10_bulk_tail",
            "component": "bulk/source-normalization finite range tail",
            "symbol": "epsilon_bulk_X, lambda_X, alpha_X(lambda)",
            "direct_map_ceiling": "alpha(lambda) curve required",
            "units": "dimensionless plus length scale",
            "observable_rows": "R10_fifth_force;R11_EH_operator_ledger",
            "bound_source": "Adelberger/ISL symbolic curve row in local_bound_claims.csv",
            "needed_for_claim": "Z_X, M_X^2, lambda_X, source charge and curve comparison",
            "current_status": "CURVE_REQUIRED_NOT_NUMERIC_CEILING",
            "valid_for_claim": "False",
        },
        {
            "coefficient_id": "COEF3541_7_R11_operator",
            "component": "unfactored source-normalization operator family",
            "symbol": "c_domain_source_normalization_operator;T_extra_operator_vector",
            "direct_map_ceiling": "operator-family bound required",
            "units": "operator-specific",
            "observable_rows": "R11_EH_operator_ledger",
            "bound_source": "R11 source-normalization minimum fill rows",
            "needed_for_claim": "operator coefficient vector with units and weak-field maps",
            "current_status": "R11_VECTOR_REQUIRED",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3541_0_coupling_route_exact",
            "decision": "The source-coupling theorem route is exact but conditional.",
            "rationale": "If matter descends only through e_obs, kappa is universal, Hilbert mass is the monopole, and no source-only slot exists, Y5 is absent/invisible.",
            "effect": "This gives a real route to Newton source coupling, not a vague hope.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3541_1_Y6_not_killed_by_Ward",
            "decision": "Y6 extra stress needs a separate topological/improvement or quadratic-response proof.",
            "rationale": "Conserved stress can satisfy Ward identities and still change PPN/R11.",
            "effect": "Do not confuse Bianchi ownership with EH-only exterior.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3541_2_first_numeric_ceilings",
            "decision": "Install first nonclaim numeric ceilings for source-coupling coefficients.",
            "rationale": "Even without the exact map, direct-map ceilings stop the branch from being purely verbal.",
            "effect": "The next runner can replace map_unsigned rows with real projections or theorem-zero certificates.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3541_3_next",
            "decision": "Attack the no-source-only-slot/Hilbert-monopole lock next.",
            "rationale": "That is the shortest route to deriving Y5 away rather than carrying source coefficients forever.",
            "effect": "3542 should try to prove the source slot is structurally forbidden, or intake concrete coefficient values.",
            "claim_allowed": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3541_0_Y5",
            "quantity": "Y5 source normalization",
            "value": "conditional_zero_route_plus_nonclaim_ceilings",
            "meaning": "Y5 can vanish if source-only slots are forbidden and Hilbert/Gauss mass locks; otherwise coefficient rows are staged",
            "claim_effect": "Newton source coupling still not claimed",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3541_1_Y6",
            "quantity": "Y6 extra stress",
            "value": "quadratic_response_or_R11_vector_required",
            "meaning": "Y6 is not killed by Ward identity alone; it needs topological/improvement invisibility or weak-field coefficients",
            "claim_effect": "local GR/EH-only exterior still not claimed",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3541_2_coefficients",
            "quantity": "first q_loc/source coefficient ceilings",
            "value": "numeric_bounds_installed_map_unsigned",
            "meaning": "R1/R3/R4/R7/R8/R9 ceilings are now explicit nonclaim rows; R10/R11 remain curve/operator rows",
            "claim_effect": "bound branch is more executable, not claim-ready",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3541_3_next",
            "quantity": "next_best_target",
            "value": "no_source_only_slot_and_Hilbert_monopole_lock",
            "meaning": "prove Y5 is structurally absent, or promote coefficient intake from ceiling rows to real projection rows",
            "claim_effect": "direct source-coupling route",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3542-Y5-R2FR-no-source-only-slot-and-Hilbert-monopole-lock-or-coefficient-intake.md",
            "next_script": "scripts/Y5_R2FR_3542_no_source_only_slot_and_Hilbert_monopole_lock_or_coefficient_intake.py",
            "objective": "Try to prove the clean parent action forbids source-only Y5 slots and locks the Hamiltonian/Gauss monopole to the Hilbert matter current; if not, convert the 3541 numeric ceilings into real coefficient-intake rows with projection maps.",
            "success_gate": "Either Y5 source normalization is structurally absent/invisible in the same observed frame, or source-coupling coefficient rows have concrete projection formulas and source paths.",
            "why_next": "3541 isolates source coupling as exact conditional theorem plus explicit ceilings; 3542 must decide whether Y5 is derivable away or must be scored.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    locks: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    coefficients: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    lock_ids = {row["lock_id"] for row in locks}
    coefficient_ids = {row["coefficient_id"] for row in coefficients}
    checks.append({"check_id": "VAL3541_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3541_1_Y5_lock_clauses_present", "passed": bool_text({"SCL3541_0_universal_matter_descent", "SCL3541_1_constant_universal_kappa", "SCL3541_2_Hilbert_monopole_lock", "SCL3541_3_no_source_only_slot"} <= lock_ids), "detail": "Y5 matter descent, kappa, Hilbert monopole and no-source-slot clauses present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3541_2_Y6_lock_clause_present", "passed": bool_text("SCL3541_4_Y6_quadratic_response_stress" in lock_ids and any(row["channel"] == "Y6_extra_stress" for row in obstructions)), "detail": "Y6 quadratic response and obstruction rows present", "valid_for_claim": "False"})
    required_coefficients = {"COEF3541_0_species_source_charge", "COEF3541_1_beta_source", "COEF3541_2_gamma_extra_stress", "COEF3541_3_xi_extra_STF", "COEF3541_4_time_drift", "COEF3541_5_boundary_domain_alpha3", "COEF3541_6_R10_bulk_tail", "COEF3541_7_R11_operator"}
    checks.append({"check_id": "VAL3541_3_coefficients_cover_required_rows", "passed": bool_text(required_coefficients <= coefficient_ids), "detail": "R1/R3/R4/R7/R8/R9/R10/R11 coefficient rows present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3541_4_numeric_ceilings_present", "passed": bool_text(any("2.8e-15" in row["direct_map_ceiling"] for row in coefficients) and any("7.8e-5" in row["direct_map_ceiling"] for row in coefficients) and any("4e-20" in row["direct_map_ceiling"] for row in coefficients)), "detail": "WEP, beta and alpha3 ceilings written", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3541_5_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3542-Y5-R2FR-no-source-only-slot")), "detail": "3542 source slot/Hilbert monopole target selected", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3541_6_no_claims_promoted", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + coefficients + status) and all(row.get("claim_allowed", "False") == "False" for row in locks + obstructions + decisions + next_rows)), "detail": "no Newton/local-GR/PPN claim promoted", "valid_for_claim": "False"})
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
    checks.append({"check_id": "VAL3541_7_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3541_8_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3541_9_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3541_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    locks: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    coefficients: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3541 - Y5/Y6 Source-Coupling Lock Or First q_loc Coefficients

## Summary
- **Coupling is the hinge:** after 3540, the clean `Delta_K=0` branch still fails unless `Y5` source-normalization and `Y6` extra stress are removed, made invisible, or bounded.
- **Y5 theorem route:** matter must descend only through `e_obs`, `kappa` must be universal, the Hilbert/Gauss monopole must lock to measured mass, and source-only slots must be forbidden.
- **Y6 theorem route:** extra stress must be purely quadratic/topological/exact-improvement so `T_extra(0)=0` and its first variation vanishes.
- **Concrete fallback:** first nonclaim numeric ceilings are now installed for WEP/source charge, beta, gamma, xi, Gdot, and alpha3; R10/R11 remain curve/operator rows.
- **No claim:** the ceilings are not predictions until the q_loc/source projection maps are derived or sourced.

## Source-Coupling Lock
The clean route is:

`S_matter = S_matter[psi,e_obs]`, `D_Y5 e_obs = 0`, `partial_Y5 kappa_eff = 0`, `mu_obs = G_eff M_Hilbert`, and no term of the form `J_A(q,material)Y5^A` exists.

Then

`delta_Y5 S_total = 0`

for ordinary matter/source coupling. For `Y6`, the required route is

`Gamma_eff-Gamma0 = O(Y^2)`, `K_hat=K_metric`, `B_GK=0`,

so

`T_extra(0)=0`, `partial_A T_extra(0)=0`.

That is the derivation shape. The current corpus has the contracts and ceilings, not yet the parent-signed proof.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Source Lock Clauses
{markdown_table(locks, ["lock_id", "target", "theorem_clause", "mathematical_result", "what_this_would_kill", "current_status", "claim_allowed"])}

## Obstruction Ledger
{markdown_table(obstructions, ["obstruction_id", "channel", "why_it_survives", "effect", "required_fix", "claim_allowed"])}

## First Coefficient Ceilings
{markdown_table(coefficients, ["coefficient_id", "component", "symbol", "direct_map_ceiling", "units", "observable_rows", "bound_source", "needed_for_claim", "current_status", "valid_for_claim"])}

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
    locks = source_lock_rows()
    obstructions = obstruction_rows()
    coefficients = coefficient_rows()
    decisions = decision_rows()
    status = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3541_SOURCE_REGISTER.csv",
        "source_lock": OUT / "P8_Y5_R2FR_3541_SOURCE_LOCK_CLAUSES.csv",
        "obstructions": OUT / "P8_Y5_R2FR_3541_OBSTRUCTION_LEDGER.csv",
        "coefficients": OUT / "P8_Y5_R2FR_3541_FIRST_QLOC_COEFFICIENT_CEILINGS.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3541_DECISION_LEDGER.csv",
        "status": OUT / "P8_Y5_R2FR_3541_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "next_target": OUT / "P8_Y5_R2FR_3541_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3541_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["source_lock"], locks, ["lock_id", "target", "theorem_clause", "mathematical_result", "what_this_would_kill", "current_status", "claim_allowed"])
    write_csv(outputs["obstructions"], obstructions, ["obstruction_id", "channel", "why_it_survives", "effect", "required_fix", "claim_allowed"])
    write_csv(outputs["coefficients"], coefficients, ["coefficient_id", "component", "symbol", "direct_map_ceiling", "units", "observable_rows", "bound_source", "needed_for_claim", "current_status", "valid_for_claim"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, locks, obstructions, coefficients, decisions, status, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, locks, obstructions, coefficients, decisions, status, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
