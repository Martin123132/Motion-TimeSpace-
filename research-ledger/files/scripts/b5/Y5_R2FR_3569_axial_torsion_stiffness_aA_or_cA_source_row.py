from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3569-Y5-R2FR-axial-torsion-stiffness-aA-or-cA-source-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_AXIAL_TORSION_STIFFNESS_3569"
CHECKPOINT_ID = "3569"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty CSV requested: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def sources() -> dict[str, Path]:
    return {
        "handoff_3568": RESIDUALS / "P8_Y5_R2FR_3568_NEXT_TARGET.csv",
        "mc_blocks_3568": RESIDUALS / "P8_Y5_R2FR_3568_MC_OPERATOR_BLOCKS.csv",
        "coercivity_3568": RESIDUALS / "P8_Y5_R2FR_3568_MC_COERCIVITY_CERTIFICATE.csv",
        "lambda_rows_3568": RESIDUALS / "P8_Y5_R2FR_3568_LAMBDAC_KSPIN_BOUND_ROWS.csv",
        "kspin_3567": RESIDUALS / "P8_Y5_R2FR_3567_KSPIN_P4_BOUND_MAP.csv",
        "spin_theorem_3565": RESIDUALS / "P8_Y5_R2FR_3565_SPIN_TORSION_THEOREM_STACK.csv",
        "no_gamma_3566": RESIDUALS / "P8_Y5_R2FR_3566_NO_GAMMA_VARIATION_DERIVATION.csv",
        "operator_decomp_1833": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_OPERATOR_DECOMPOSITION_CONTRACT.csv",
        "positive_pack_1846": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_POSITIVE_OPERATOR_PACK.csv",
        "positive_inputs_2949": RESIDUALS / "P8_Y5_R2FR_2949_POSITIVE_OPERATOR_INPUT_QUEUE.csv",
        "gk_coercivity_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_COERCIVITY_AUDIT.csv",
        "axial_kernel_3494": RESIDUALS / "P8_Y5_R2FR_3494_AXIAL_TORSION_KERNEL_INTERFACE.csv",
        "axial_p4_2348": RESIDUALS / "P8_Y5_PARENT_QLOC_2348_AXIAL_TORSION_P4_COMPONENT_ROW.csv",
        "axial_map_2115": RESIDUALS / "P8_Y5_PARENT_QLOC_2115_AXIAL_CMTS_KRT_MAP.csv",
        "axial_values_2116": RESIDUALS / "P8_Y5_PARENT_QLOC_2116_AXIAL_COMPONENT_SOURCE_VALUES.csv",
        "torsion_decision_2041": RESIDUALS / "P8_Y5_PARENT_QLOC_2041_TORSION_CONNECTION_DECISION_LEDGER.csv",
        "lc_gate_960": RESIDUALS / "P8_Y5_R10_960_TORSION_LEVI_CIVITA_GATE_ATTEMPT.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    roles = {
        "handoff_3568": "declares 3569 axial target",
        "mc_blocks_3568": "imports axial C_A block and a_A formula",
        "coercivity_3568": "imports lambda_C diagonal-dominance certificate",
        "lambda_rows_3568": "imports missing a_i and K_spin rows",
        "kspin_3567": "imports axial response residual map",
        "spin_theorem_3565": "imports no-Gamma versus P4 fork",
        "no_gamma_3566": "imports LC-branch affine variation zero",
        "operator_decomp_1833": "imports torsion irreducible operator need",
        "positive_pack_1846": "imports Z and mass-gap operator requirements",
        "positive_inputs_2949": "imports positive operator input queue",
        "gk_coercivity_2471": "imports eta/cross-term rule",
        "axial_kernel_3494": "imports axial projection and spin-coupling kernel",
        "axial_p4_2348": "imports axial P4 response row",
        "axial_map_2115": "imports C to torsion to axial component map",
        "axial_values_2116": "imports earlier candidate zero/fallback source values",
        "torsion_decision_2041": "imports torsion connection decision ledger",
        "lc_gate_960": "imports older LC/torsion gate",
    }
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def stiffness_derivation_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        {
            "derivation_id": "AXST3569_0_mode_definition",
            "claim_piece": "axial distortion mode",
            "mathematical_statement": "C_A is the axial torsion irreducible component of C=Gamma-Gamma_LC[g_obs], with T^lambda_{mu nu}=2C^lambda_[mu nu] and A^mu=(1/6)epsilon^{alpha beta gamma mu}T_{alpha beta gamma}.",
            "derivation": "This is the existing 2115/3494 projection chain specialized to the axial spin channel.",
            "units": "C_A and A^mu carry m^-1 before GeV/KRT conversion",
            "status": "EXACT_DEFINITION_IF_INDEPENDENT_CONNECTION_RETAINED",
            "source_key": "axial_kernel_3494",
        },
        {
            "derivation_id": "AXST3569_1_LC_branch_zero",
            "claim_piece": "zero by variable absence",
            "mathematical_statement": "If the active local parent branch uses only e_obs,g_obs and omega_LC[e_obs], then Gamma_ind/omega_ind is not a coordinate and C_A is absent; equivalently C_A=0 on that reduced configuration space.",
            "derivation": "The Frechet derivative with respect to the missing affine coordinate is zero; spin response is routed through the coframe/Hilbert equation rather than a torsion equation.",
            "units": "boolean branch statement",
            "status": "EXACT_INSIDE_3566_BRANCH_NOT_PUBLIC_PARENT_SIGNED",
            "source_key": "no_gamma_3566",
        },
        {
            "derivation_id": "AXST3569_2_independent_axial_action",
            "claim_piece": "independent axial quadratic block",
            "mathematical_statement": "If C_A is retained, the minimal honest quadratic branch has E_A=1/2 int sqrt|g| [Z_A |nabla C_A|^2 + m_A^2 |C_A|^2] plus mixed blocks and source coupling <C_A,J5_A>.",
            "derivation": "This is the axial restriction of the 3568 M_C decomposition and the 1833 torsion irreducible operator contract.",
            "units": "Z_A and m_A^2 in action-normalized operator units",
            "status": "STRUCTURAL_ACTION_ANSATZ_PARENT_COEFFICIENTS_UNSIGNED",
            "source_key": "operator_decomp_1833",
        },
        {
            "derivation_id": "AXST3569_3_diagonal_stiffness_law",
            "claim_piece": "a_A lower weight",
            "mathematical_statement": "<C_A,M_AA C_A> >= a_A ||C_A||^2 with a_A := Z_A lambda_1(D_local,boundary)+m_A^2, after gauge/zero-mode handling.",
            "derivation": "On a self-adjoint local domain, Poincare/coercive inequality gives ||nabla C_A||^2 >= lambda_1||C_A||^2; positive Z_A and nonnegative/positive m_A^2 give the lower bound.",
            "units": "inverse length^2 or action-normalized stiffness",
            "status": "DERIVED_SYMBOLIC_STIFFNESS_LAW_NOT_NUMERIC",
            "source_key": "positive_pack_1846",
        },
        {
            "derivation_id": "AXST3569_4_cross_term_guard",
            "claim_piece": "axial block inside full M_C",
            "mathematical_statement": "The axial mode contributes a positive sector to lambda_C only if a_A(1-eta_A)>0, where eta_A=sum_j eta_Aj bounds axial mixing with trace torsion, nonmetricity, projective and tensor modes.",
            "derivation": "This is the axial row of the 3568 Young/Schur diagonal-dominance certificate.",
            "units": "eta_A dimensionless",
            "status": "EXACT_IF_ETA_A_BOUNDS_PARENT_SIGNED",
            "source_key": "gk_coercivity_2471",
        },
        {
            "derivation_id": "AXST3569_5_solution_bound",
            "claim_piece": "axial amplitude bound",
            "mathematical_statement": "||C_A|| <= [a_A(1-eta_A)]^-1 (||J5_A||+||B_A||+||P_A||+||N_A||+||R_A_mix||), whenever a_A(1-eta_A)>0.",
            "derivation": "Test the axial Euler-Lagrange equation against C_A, absorb controlled mixed terms by eta_A, and apply Cauchy-Schwarz to the surviving sources.",
            "units": "m^-1 in geometric units before arena response conversion",
            "status": "DERIVED_SYMBOLIC_BOUND_NUMERATOR_INPUTS_MISSING",
            "source_key": "coercivity_3568",
        },
        {
            "derivation_id": "AXST3569_6_observable_response",
            "claim_piece": "spin/coupling observable tail",
            "mathematical_statement": "epsilon_axial_torsion_spin <= K_A ||C_A||, equivalently S_axial_abs=||c_A S_mu J5^mu||/N_source in the older P4 normalization.",
            "derivation": "This combines the 3567 K_A response row with the 2348 c_A axial spin-torsion P4 row; the coefficient is not allowed to be silently set to zero outside the LC branch.",
            "units": "spin/clock/WEP/KRT response units after declared projection",
            "status": "RESPONSE_FORMULA_READY_K_A_OR_c_A_MISSING",
            "source_key": "kspin_3567",
        },
        {
            "derivation_id": "AXST3569_7_verdict",
            "claim_piece": "3569 axial verdict",
            "mathematical_statement": "The axial stiffness law is derivable: a_A=Z_A lambda_1+m_A^2, and the surviving amplitude/observable bound is explicit. A public local-GR pass is still false until Z_A,m_A^2,eta_A,J5_A,boundary/projective silence and K_A/c_A are parent-owned or sourced.",
            "derivation": "3569 replaces a vague missing-coupling complaint with an exact axial fork: zero by selected LC variable domain, or retained axial response with a concrete denominator and numerator.",
            "units": "mixed symbolic gate",
            "status": "AXIAL_LAW_DERIVED_PUBLIC_CLAIM_BLOCKED",
            "source_key": "lambda_rows_3568",
        },
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": row["derivation_id"],
            "claim_piece": row["claim_piece"],
            "mathematical_statement": row["mathematical_statement"],
            "derivation": row["derivation"],
            "units": row["units"],
            "status": row["status"],
            "source_path": str(source_paths[row["source_key"]]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row in rows
    ]


def axial_source_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    row_specs = [
        ("AXSRC3569_0_aA", "a_A", "diagonal axial stiffness", "a_A=Z_A lambda_1(D_local,boundary)+m_A^2", "inverse length^2 or action-normalized stiffness", "MISSING_PARENT_NUMERIC", "Z_A, lambda_1, m_A^2, domain/boundary normalization", "operator_decomp_1833", "R10/PPN/clocks/orbital via lambda_C", "MISSING_PARENT_SIGNED_VALUE"),
        ("AXSRC3569_1_ZA", "Z_A", "axial kinetic normalization", "coefficient of |nabla C_A|^2 in the parent local action", "action-normalized kinetic weight", "MISSING_SIGN_CERTIFICATE", "parent second variation in axial torsion direction", "positive_pack_1846", "all local arenas through a_A", "MISSING_PARENT_LX"),
        ("AXSRC3569_2_mA2", "m_A^2", "axial mass/gap", "zeroth-order axial operator gap after zero-mode handling", "inverse length^2 or action-normalized mass", "MISSING_GAP_INPUT", "mass/gap/range term or justified zero-mode removal", "positive_inputs_2949", "range/local suppression", "MISSING_GAP_INPUTS"),
        ("AXSRC3569_3_lambda1", "lambda_1(D_local)", "domain coercive gap", "first positive eigenvalue/Poincare constant of selected local axial domain", "inverse length^2", "MISSING_DOMAIN_SIGNATURE", "self-adjoint domain, boundary condition, topology/no-flux rule", "positive_inputs_2949", "local exterior and lab-domain suppression", "MISSING_PARENT_SELECTED_DOMAIN"),
        ("AXSRC3569_4_etaA", "eta_A", "axial cross-term row sum", "eta_A=sum_j eta_Aj for axial mixing with retained distortion modes", "dimensionless", "MISSING_CROSS_BOUNDS", "Young/Schur bounds in declared irreducible basis", "gk_coercivity_2471", "lambda_C stability", "MISSING_OPERATOR_BASIS"),
        ("AXSRC3569_5_J5A", "J5_A", "spin/hypermomentum axial source", "delta S_matter/delta C_A or axial spin current in independent affine branch", "source norm dual to C_A", "ZERO_ONLY_INSIDE_LC_BRANCH_ELSE_MISSING_SOURCE_NORM", "all matter/source/readout no-Gamma theorem or explicit J5_A norm", "spin_theorem_3565", "spin/clock/WEP source response", "MISSING_NO_GAMMA_PUBLIC_SELECTOR"),
        ("AXSRC3569_6_BA", "B_A", "axial boundary/domain work", "boundary term from integration by parts in axial C_A energy identity", "dual source norm", "MISSING_BOUNDARY_SILENCE", "compact support/no-flux/local exterior boundary theorem or bound", "positive_pack_1846", "local vacuum exterior", "MISSING_DOMAIN_SIGNATURE"),
        ("AXSRC3569_7_PA", "P_A", "projective or gauge leakage into axial sector", "unremoved gauge/projective/basis leakage projected into axial response", "dual source norm", "MISSING_PROJECTIVE_OR_BASIS_GUARD", "basis, gauge, projective silence, representative invariance", "torsion_decision_2041", "PPN/clocks/orbits", "MISSING_PROJECTIVE_GUARD"),
        ("AXSRC3569_8_KA", "K_A", "axial response kernel", "epsilon_axial_torsion_spin <= K_A ||C_A||", "arena response per m^-1", "MISSING_RESPONSE_KERNEL", "projection from axial geometric norm to KRT/spin/clock/WEP arena residual", "kspin_3567", "spin, clock, PPN, R10", "MISSING_WEAK_FIELD_MAP"),
        ("AXSRC3569_9_cA_xiA", "c_A or xi_A", "axial matter coupling coefficient", "S_axial_abs=||c_A S_mu J5^mu||/N_source; b_eff^I=xi_A R^I_mu A^mu", "dimensionless or declared KRT convention", "MISSING_COUPLING_COEFFICIENT_OUTSIDE_CANDIDATE_BRANCH", "parent matter coupling signature or sourced coefficient", "axial_values_2116", "spin/KRT response", "MISSING_XI_A_AND_MIXING_MATRIX"),
        ("AXSRC3569_10_bound_master", "epsilon_axial_torsion_spin", "nonclaim axial observable bound", "epsilon_axial_torsion_spin <= K_A [a_A(1-eta_A)]^-1 (||J5_A||+||B_A||+||P_A||+||N_A||+||R_A_mix||)", "arena residual units", "SCHEMA_READY_NUMERIC_INPUTS_MISSING", "AXSRC3569_0 through AXSRC3569_9", "axial_p4_2348", "R10/PPN/clocks/orbital/spin", "MISSING_PARENT_INPUTS"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": row_id,
            "symbol": symbol,
            "role": role,
            "formula": formula,
            "units": units,
            "current_value": current_value,
            "required_inputs": required_inputs,
            "source_path": str(source_paths[source_key]),
            "arena": arena,
            "status": status,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row_id, symbol, role, formula, units, current_value, required_inputs, source_key, arena, status in row_specs
    ]


def activation_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("GATE3569_0_sources", "source audit", "PASS", "all referenced upstream axial/coercivity source files exist"),
        ("GATE3569_1_LC_zero_branch", "LC variable absence", "CONDITIONAL_PASS_PRIVATE_BRANCH_ONLY", "C_A=0 if 3566 LC/no-Gamma branch is the selected parent ordinary branch"),
        ("GATE3569_2_aA_positive", "axial stiffness positivity", "FAIL_CURRENT_PUBLIC_CLAIM", "a_A law derived, but Z_A, m_A^2, lambda_1 and domain are not parent-signed numeric/theorem rows"),
        ("GATE3569_3_etaA_cross", "axial cross-term guard", "FAIL_CURRENT_PUBLIC_CLAIM", "eta_A row-sum bound is not parent-signed"),
        ("GATE3569_4_source_silence", "axial source silence", "FAIL_CURRENT_PUBLIC_CLAIM", "J5_A is zero only inside the LC branch; independent affine fallback still lacks a source norm"),
        ("GATE3569_5_boundary_projective", "boundary/projective silence", "FAIL_CURRENT_PUBLIC_CLAIM", "B_A and P_A are not closed by a source path with units"),
        ("GATE3569_6_response_kernel", "K_A/c_A response", "FAIL_CURRENT_PUBLIC_CLAIM", "K_A or c_A/xi_A remains missing outside the candidate zero branch"),
        ("GATE3569_7_public_axial_pass", "public axial/local-GR pass", "FAIL_CURRENT_PUBLIC_CLAIM", "no R10, PPN, clock, orbital or local-GR claim follows from 3569"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths["mc_blocks_3568"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, detail in rows
    ]


def decision_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "DEC3569_0_no_smuggling",
            "decision": "do not silently set c_A or K_A to zero",
            "reason": "zero is exact only if the LC/no-independent-connection parent branch is selected; otherwise the independent affine branch must carry the axial response",
            "consequence": "3569 keeps both forks explicit and nonclaim",
            "status": "ADOPTED",
            "source_key": "spin_theorem_3565",
        },
        {
            "decision_id": "DEC3569_1_stiffness_law",
            "decision": "promote a_A=Z_A lambda_1+m_A^2 as the axial denominator contract",
            "reason": "this is a derivable operator law, not merely a missing-data note",
            "consequence": "future work can fill Z_A/m_A^2/lambda_1 rather than re-litigating the whole torsion branch",
            "status": "ADOPTED",
            "source_key": "positive_pack_1846",
        },
        {
            "decision_id": "DEC3569_2_fallback_bound",
            "decision": "stage an axial source-ready response row",
            "reason": "if the parent selector remains unsigned, the best honest route is a bound with named numerator terms and named arena kernels",
            "consequence": "AXSRC3569_10 is the first concrete axial P4 row for later R10/PPN/clock/orbital tests",
            "status": "ADOPTED_NONCLAIM",
            "source_key": "axial_p4_2348",
        },
        {
            "decision_id": "DEC3569_3_next_target",
            "decision": "hunt parent coefficients before expanding more sectors",
            "reason": "a_A is now the nearest denominator; K_A/c_A is the nearest observable coupling",
            "consequence": "3570 should try to extract/sign Z_A, m_A^2, eta_A and K_A/c_A from the parent local action or demote axial fallback to closure-only",
            "status": "NEXT_TARGET_SELECTED",
            "source_key": "handoff_3568",
        },
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": row["decision_id"],
            "decision": row["decision"],
            "reason": row["reason"],
            "consequence": row["consequence"],
            "status": row["status"],
            "source_path": str(source_paths[row["source_key"]]),
            "valid_for_claim": False,
        }
        for row in rows
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "AXIAL_STIFFNESS_LAW_DERIVED_SYMBOLIC_NONCLAIM",
            "strongest_result": "For retained axial torsion, a_A=Z_A lambda_1(D_local,boundary)+m_A^2 and epsilon_axial_torsion_spin <= K_A/[a_A(1-eta_A)] times the named source/boundary/projective/nonlinear numerator.",
            "still_missing": "parent-signed Z_A, m_A^2, lambda_1, eta_A, J5_A silence or bound, B_A/P_A silence, K_A or c_A/xi_A response coefficient",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3569_0",
            "target_doc": "3570-Y5-R2FR-parent-axial-coefficient-signature-or-KA-bound-fill.md",
            "target_script": "scripts/Y5_R2FR_3570_parent_axial_coefficient_signature_or_KA_bound_fill.py",
            "objective": "try to source or derive the parent axial coefficients Z_A, m_A^2, eta_A and K_A/c_A; if the LC selector is selected, write the parent-owned C_A=0 certificate instead",
            "success_gate": "either a parent-owned axial zero selector, or source-backed nonclaim numeric/theorem rows for a_A and K_A/c_A",
            "reason": "3569 has reduced the coupling hinge to a small set of explicit axial denominator and response coefficients",
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_item": "axial_torsion_stiffness_and_response",
            "status": "DERIVED_SYMBOLIC_NONCLAIM",
            "stiffness_law": "a_A=Z_A lambda_1(D_local,boundary)+m_A^2",
            "observable_bound": "epsilon_axial_torsion_spin <= K_A/[a_A(1-eta_A)] * numerator_A",
            "next_action": "fill parent coefficients or certify LC variable absence as selected public branch",
            "valid_for_claim": False,
        }
    ]


def validate(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    derivation: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in outputs.items() if key != "validation"}
    validations.append(("VAL3569_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3569 source paths exist"))
    needles = {
        "handoff_3568": "NEXT3568_0",
        "mc_blocks_3568": "MC3568_0_axial_torsion",
        "coercivity_3568": "COER3568_3_lambda_formula",
        "lambda_rows_3568": "LAMB3568_1_a_i",
        "kspin_3567": "KSP3567_1_axial_torsion",
        "spin_theorem_3565": "STH3565_1_variable_absence_zero",
        "no_gamma_3566": "VAR3566_1_matter_spin",
        "operator_decomp_1833": "OPD1833_0_torsion_irreducible",
        "positive_pack_1846": "OP1846_1_Z_positive",
        "positive_inputs_2949": "PIN2949_2_ZX",
        "gk_coercivity_2471": "COER2471_2_eta_form",
        "axial_kernel_3494": "AXK3494_2_axial_projection",
        "axial_p4_2348": "P4S2348_1_axial_torsion",
        "axial_map_2115": "AKM2115_2_axial_projection",
        "axial_values_2116": "ACV2116_0_xi_A_candidate_branch",
        "torsion_decision_2041": "LC2041_4_P4_fallback",
        "lc_gate_960": "LC960_3_connection_residual_route",
    }
    validations.append(("VAL3569_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected axial/coercivity source needles found"))
    validations.append(("VAL3569_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3569 output files written"))
    csvs_parse = True
    parse_details: list[str] = []
    for output_id, path in pre_validation_outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            row_count = len(read_csv(path))
            csvs_parse = csvs_parse and row_count > 0
            parse_details.append(f"{output_id}:{row_count}")
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3569_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3569_4_aA_law_present", any(row["derivation_id"] == "AXST3569_3_diagonal_stiffness_law" and "a_A := Z_A lambda_1" in str(row["mathematical_statement"]) for row in derivation), "diagonal axial stiffness law present"))
    validations.append(("VAL3569_5_bound_row_present", any(row["row_id"] == "AXSRC3569_10_bound_master" and "epsilon_axial_torsion_spin" in str(row["formula"]) for row in source_rows), "master axial response bound row present"))
    validations.append(("VAL3569_6_zero_branch_not_smuggled", any(row["decision_id"] == "DEC3569_0_no_smuggling" for row in decisions), "zero branch is separated from independent affine fallback"))
    validations.append(("VAL3569_7_public_claim_blocked", any(row["gate_id"] == "GATE3569_7_public_axial_pass" and row["status"] == "FAIL_CURRENT_PUBLIC_CLAIM" for row in gates), "public local claim remains blocked"))
    validations.append(("VAL3569_8_no_claim_flags", all(str(row["valid_for_claim"]).lower() == "false" for row in derivation + source_rows + gates + decisions), "all generated physics rows remain nonclaim"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in derivation + source_rows + gates + decisions)
    validations.append(("VAL3569_9_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = any(FORMALIZATION.rglob("*3569*")) if FORMALIZATION.exists() else False
    validations.append(("VAL3569_10_formalization_workbench_untouched", not formalization_touched, "no 3569 checkpoint output appears in formalization-workbench"))
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passed,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passed, detail in validations
    ]


def write_doc(
    outputs: dict[str, Path],
    derivation: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3569 - Axial torsion stiffness aA or cA source row",
        "",
        "## Verdict",
        "3569 does push the coupling problem forward.  It proves the exact axial fork instead of just circling the missing coefficient.  If the 3566 LC/no-independent-connection branch is the selected parent branch, the axial torsion variable is absent and `C_A=0` follows by variable-domain descent.  If the independent affine branch is retained, the axial denominator is no longer vague: `a_A = Z_A lambda_1(D_local,boundary) + m_A^2`, with the full-sector guard `a_A(1-eta_A)>0`.",
        "",
        "The surviving observable tail is now an explicit nonclaim bound: `epsilon_axial_torsion_spin <= K_A/[a_A(1-eta_A)] * (||J5_A||+||B_A||+||P_A||+||N_A||+||R_A_mix||)`.  That is not a local-GR pass yet, but it is a real contract for what the parent action must supply.",
        "",
        "## Generated outputs",
    ]
    for output_id, path in outputs.items():
        lines.append(f"- `{output_id}`: `{path}`")
    lines.extend(["", "## Axial derivation"])
    for row in derivation:
        lines.append(f"- `{row['derivation_id']}`: {row['mathematical_statement']} ({row['status']})")
    lines.extend(["", "## Source-ready rows"])
    for row in source_rows:
        lines.append(f"- `{row['row_id']}` `{row['symbol']}`: {row['formula']} ({row['status']})")
    lines.extend(["", "## Activation gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} -> {row['consequence']}")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: {row['strongest_result']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(["", "## Next target", f"- `{next_target[0]['target_doc']}`", f"- Objective: {next_target[0]['objective']}"])
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    register = source_register(source_paths)
    derivation = stiffness_derivation_rows(source_paths)
    source_rows = axial_source_rows(source_paths)
    gates = activation_rows(source_paths)
    decisions = decision_rows(source_paths)
    status = status_rows()
    next_target = next_target_rows()
    canonical = canonical_status_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3569_SOURCE_REGISTER.csv",
        "stiffness_derivation": RESIDUALS / "P8_Y5_R2FR_3569_AXIAL_TORSION_STIFFNESS_DERIVATION.csv",
        "axial_source_rows": RESIDUALS / "P8_Y5_R2FR_3569_AXIAL_RESPONSE_SOURCE_ROWS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3569_ACTIVATION_GATES.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3569_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3569_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3569_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_axial_torsion_stiffness_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3569_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], register)
    write_csv(outputs["stiffness_derivation"], derivation)
    write_csv(outputs["axial_source_rows"], source_rows)
    write_csv(outputs["activation_gates"], gates)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], next_target)
    write_csv(outputs["canonical_status"], canonical)
    validation = validate(source_paths, outputs, derivation, source_rows, gates, decisions)
    write_csv(outputs["validation"], validation)
    write_doc(outputs, derivation, source_rows, gates, decisions, status, validation, next_target)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"3569 validation failed: {failed}")
    print(f"wrote {DOC}")
    for output_id, path in outputs.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
