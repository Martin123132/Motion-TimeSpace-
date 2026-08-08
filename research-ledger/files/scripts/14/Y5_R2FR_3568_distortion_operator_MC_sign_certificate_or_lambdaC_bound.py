from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3568-Y5-R2FR-distortion-operator-MC-sign-certificate-or-lambdaC-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_DISTORTION_OPERATOR_MC_3568"
CHECKPOINT_ID = "3568"


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
        "handoff_3567": RESIDUALS / "P8_Y5_R2FR_3567_NEXT_TARGET.csv",
        "selector_3567": RESIDUALS / "P8_Y5_R2FR_3567_LOCAL_LC_SELECTOR_THEOREM.csv",
        "proof_3567": RESIDUALS / "P8_Y5_R2FR_3567_DISTORTION_ZERO_PROOF.csv",
        "kspin_3567": RESIDUALS / "P8_Y5_R2FR_3567_KSPIN_P4_BOUND_MAP.csv",
        "gates_3567": RESIDUALS / "P8_Y5_R2FR_3567_SELECTOR_ACTIVATION_GATES.csv",
        "distortion_contract_1832": RESIDUALS / "P8_Y5_PARENT_QLOC_1832_DISTORTION_EQUATION_CONTRACT.csv",
        "distortion_owner_1833": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_DISTORTION_EQUATION_OWNER_AUDIT.csv",
        "operator_decomp_1833": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_OPERATOR_DECOMPOSITION_CONTRACT.csv",
        "positive_nohair_3429": RESIDUALS / "P8_Y5_R2FR_3429_POSITIVE_OPERATOR_NOHAIR_THEOREM.csv",
        "positive_contract_3092": RESIDUALS / "P8_Y5_R2FR_3092_POSITIVE_NOHAIR_CONTRACT.csv",
        "positive_inputs_2949": RESIDUALS / "P8_Y5_R2FR_2949_POSITIVE_OPERATOR_INPUT_QUEUE.csv",
        "positive_pack_1846": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_POSITIVE_OPERATOR_PACK.csv",
        "gk_operator_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_OPERATOR_ANSATZ.csv",
        "gk_coercivity_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_COERCIVITY_AUDIT.csv",
        "gk_eligibility_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_NOHAIR_ELIGIBILITY.csv",
        "gk_positivity_2470": RESIDUALS / "P8_Y5_GK_NOHAIR_2470_POSITIVITY_CLAUSES.csv",
        "local_geometry_3493": RESIDUALS / "P8_Y5_R2FR_3493_OFFICIAL_P4_LOCAL_GEOMETRY_INTERFACE.csv",
        "local_eh_r11": RESIDUALS / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv",
        "double_zero_r11": RESIDUALS / "P8_DOUBLE_ZERO_R11_OPERATOR_MAPPING.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    roles = {
        "handoff_3567": "declares 3568 target",
        "selector_3567": "imports distortion selector theorem",
        "proof_3567": "imports C=0 proof and bound branch",
        "kspin_3567": "imports K_spin/lambda_C map",
        "gates_3567": "imports open selector gates",
        "distortion_contract_1832": "distortion equation contract",
        "distortion_owner_1833": "distortion equation owner audit",
        "operator_decomp_1833": "torsion/nonmetricity/projective block decomposition",
        "positive_nohair_3429": "positive operator no-hair theorem",
        "positive_contract_3092": "energy identity contract",
        "positive_inputs_2949": "positive operator input queue",
        "positive_pack_1846": "operator sign/gap pack",
        "gk_operator_2471": "quadratic operator ansatz and mixed term model",
        "gk_coercivity_2471": "coercivity audit and cross-term rule",
        "gk_eligibility_2471": "no-hair eligibility status",
        "gk_positivity_2470": "positivity/boundary/topology clauses",
        "local_geometry_3493": "official local geometry fallback interface",
        "local_eh_r11": "R11 operator family audit",
        "double_zero_r11": "torsion/nonmetricity double-zero mapping contract",
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


def operator_block_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("MC3568_0_axial_torsion", "C_A", "axial torsion / spin contorsion", "a_A = Z_A lambda_1 + m_A^2", "epsilon_axial_torsion_spin", "positive a_A and no spin hypermomentum source", "operator_decomp_1833"),
        ("MC3568_1_trace_torsion", "C_T", "trace torsion", "a_T = Z_T lambda_1 + m_T^2", "epsilon_trace_torsion", "positive a_T and no trace torsion current", "operator_decomp_1833"),
        ("MC3568_2_weyl_nonmetricity", "C_Q", "Weyl nonmetricity trace", "a_Q = Z_Q lambda_1 + m_Q^2", "epsilon_weyl_nonmetricity", "positive a_Q and no clock/rod/source scale current", "operator_decomp_1833"),
        ("MC3568_3_shear_nonmetricity", "C_S", "trace-free/shear nonmetricity", "a_S = Z_S lambda_1 + m_S^2", "epsilon_shear_nonmetricity", "positive a_S and no optical/lightcone shear current", "operator_decomp_1833"),
        ("MC3568_4_projective_trace", "C_P", "projective trace", "gauge-fixed/quotiented or a_P = Z_P lambda_1 + m_P^2", "epsilon_projective_trace", "projective mode absent/gauge/invariant, or positive with no trace source", "local_geometry_3493"),
        ("MC3568_5_tensor_torsion", "C_R", "tensor torsion remainder", "a_R = Z_R lambda_1 + m_R^2", "epsilon_tensor_torsion", "positive a_R and no residual tensor spin source", "operator_decomp_1833"),
        ("MC3568_6_boundary_domain", "B_C", "connection boundary/domain work", "B_C=0 or ||B_C|| source-bounded", "epsilon_boundary_connection", "proper boundary/no-flux/topology or retained bound", "gk_positivity_2470"),
        ("MC3568_7_source", "Delta_Gamma", "hypermomentum source", "Delta_Gamma=0 in 3566 LC branch else norm-bounded", "epsilon_hypermomentum_source", "no-Gamma source/readout theorem or source derivative row", "proof_3567"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "block_id": block_id,
            "mode_symbol": mode,
            "mode_description": description,
            "diagonal_lower_weight": lower_weight,
            "observable_tail": tail,
            "zero_or_positive_condition": condition,
            "source_path": str(source_paths[source_key]),
            "numeric_value": "MISSING_PARENT_SIGNED_VALUE",
            "units_status": "MISSING_DECLARED_UNITS",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for block_id, mode, description, lower_weight, tail, condition, source_key in rows
    ]


def coercivity_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        {
            "coercivity_id": "COER3568_0_norm",
            "claim_piece": "distortion norm",
            "statement": "||C||_C^2 := sum_i ||C_i||^2 over non-gauge irreducible distortion modes i={A,T,Q,S,R} plus projective P only if not gauge-removed.",
            "derivation": "Decompose C into torsion irreps, nonmetricity trace/shear, projective trace and tensor remainder; projective/gauge modes are quotiented or retained as P_C.",
            "status": "EXACT_DECOMPOSITION_CONDITIONAL_ON_FIELD_BASIS",
            "source_key": "operator_decomp_1833",
        },
        {
            "coercivity_id": "COER3568_1_diagonal",
            "claim_piece": "diagonal lower weights",
            "statement": "For each active mode i, <C_i,M_ii C_i> >= a_i ||C_i||^2 with a_i := Z_i lambda_1(A,boundary)+m_i^2 after gauge/zero-mode removal.",
            "derivation": "Poincare/coercive domain gives ||nabla C_i||^2 >= lambda_1 ||C_i||^2; positive kinetic and mass/gap terms give the lower bound.",
            "status": "EXACT_IF_Z_MASS_DOMAIN_SIGNED",
            "source_key": "positive_contract_3092",
        },
        {
            "coercivity_id": "COER3568_2_cross_terms",
            "claim_piece": "mixed block control",
            "statement": "For cross blocks M_ij, require |<C_i,M_ij C_j>| <= eta_ij/2*(a_i||C_i||^2+a_j||C_j||^2) with eta_ij>=0.",
            "derivation": "Young/Schur bound controls torsion-nonmetricity/projective mixing without assuming cancellation.",
            "status": "EXACT_INEQUALITY_IF_ETA_BOUNDS_SIGNED",
            "source_key": "gk_coercivity_2471",
        },
        {
            "coercivity_id": "COER3568_3_lambda_formula",
            "claim_piece": "lambda_C lower bound",
            "statement": "If eta_i := sum_{j!=i} eta_ij < 1 for every active mode, then <C,M_C C> >= lambda_C ||C||_C^2 with lambda_C := min_i a_i(1-eta_i).",
            "derivation": "Sum diagonal lower bounds and subtract the cross Young envelopes. Strict diagonal dominance in energy norm gives positivity.",
            "status": "EXACT_SYMBOLIC_SIGN_CERTIFICATE",
            "source_key": "gk_coercivity_2471",
        },
        {
            "coercivity_id": "COER3568_4_projective_clause",
            "claim_piece": "projective handling",
            "statement": "Projective trace cannot sit in the kernel unnoticed: it is either gauge-fixed/quotiented/all-sector invisible, or included as an active C_P mode with positive a_P and response map.",
            "derivation": "A zero eigenvalue is legal only for gauge/invisible projective direction; otherwise it destroys lambda_C and moves to P4_projective.",
            "status": "REQUIRED_CLAUSE_UNSIGNED",
            "source_key": "local_geometry_3493",
        },
        {
            "coercivity_id": "COER3568_5_zero_result",
            "claim_piece": "selector zero",
            "statement": "With lambda_C>0, Delta_Gamma=B_C=P_C=0, and nonlinear radius c_N||C||<lambda_C, the distortion equation forces C=0.",
            "derivation": "Insert COER3568_3 into the 3567 energy identity; the only small finite-energy solution is the LC branch.",
            "status": "EXACT_CONDITIONAL_MC_ZERO_THEOREM",
            "source_key": "selector_3567",
        },
        {
            "coercivity_id": "COER3568_6_bound_result",
            "claim_piece": "lambda_C fallback",
            "statement": "If source/boundary/projective pieces survive, ||C||_C <= lambda_C^-1(||Delta_Gamma||+||B_C||+||P_C||+||N_C||), provided lambda_C>0.",
            "derivation": "Use Cauchy-Schwarz in the same energy identity; this is the nonclaim P4 route.",
            "status": "BOUND_FORMULA_SOURCE_READY_BUT_NUMERIC_INPUTS_MISSING",
            "source_key": "kspin_3567",
        },
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coercivity_id": row["coercivity_id"],
            "claim_piece": row["claim_piece"],
            "statement": row["statement"],
            "derivation": row["derivation"],
            "status": row["status"],
            "source_path": str(source_paths[row["source_key"]]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for row in rows
    ]


def lambda_bound_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("LAMB3568_0_lambdaC", "lambda_C", "min_i a_i(1-eta_i)", "operator eigenvalue / inverse length^2 after normalization", "SOURCE_READY_SCHEMA_NUMERIC_VALUES_MISSING", "a_i values, eta_ij bounds, active mode list, boundary/gauge zero-mode policy", "positive_inputs_2949"),
        ("LAMB3568_1_a_i", "a_i", "Z_i lambda_1(A,boundary)+m_i^2", "inverse length^2 or action-normalized stiffness", "MISSING_Z_MASS_DOMAIN_VALUES", "Z_i, m_i^2, lambda_1, units, source path per mode", "positive_pack_1846"),
        ("LAMB3568_2_eta_i", "eta_i", "sum_j eta_ij", "dimensionless", "MISSING_CROSS_TERM_BOUNDS", "cross coefficient basis and Young/Schur bounds", "gk_coercivity_2471"),
        ("LAMB3568_3_Kspin", "K_spin", "operator norm from ||C||_C to local WEP/PPN/clock/light/orbit/R10 residual", "arena response units", "SYMBOLIC_MAP_NUMERIC_KERNELS_MISSING", "response kernels K_A,K_P,K_Q,K_Qs,K_Delta and units", "kspin_3567"),
        ("LAMB3568_4_master_bound", "epsilon_local_connection", "epsilon_local_connection <= K_spin/lambda_C * (||Delta_Gamma||+||B_C||+||P_C||+||N_C||)", "arena residual units", "EXECUTABLE_SYMBOLIC_NONCLAIM", "all numerator norms plus K_spin/lambda_C source-backed", "kspin_3567"),
        ("LAMB3568_5_claim_gate", "local_LC_selector_claim", "claim_allowed = lambda_C>0 and Delta_Gamma=B_C=P_C=N_C=0 in same parent branch", "boolean", "FALSE_CURRENTLY", "parent-owned M_C, boundary/projective silence, public no-Gamma source", "gates_3567"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": bound_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "status": status,
            "required_inputs": required,
            "source_path": str(source_paths[source_key]),
            "numeric_value": "MISSING",
            "source_backed_numeric": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for bound_id, symbol, formula, units, status, required, source_key in rows
    ]


def activation_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("ACT3568_0_symbolic_certificate", "Schur/Young symbolic coercivity certificate exists", "PASS_SYMBOLIC", "lambda_C=min_i a_i(1-eta_i) derived", "gk_coercivity_2471"),
        ("ACT3568_1_parent_operator", "M_C parent-owned operator basis", "FAIL", "operator blocks and coefficients are not parent-signed", "distortion_owner_1833"),
        ("ACT3568_2_positive_inputs", "a_i positive sign/unit values", "FAIL", "Z_i, m_i^2, lambda_1 and units missing", "positive_pack_1846"),
        ("ACT3568_3_cross_bounds", "eta_ij cross-term bounds", "FAIL", "cross coefficient basis and eta values missing", "gk_coercivity_2471"),
        ("ACT3568_4_projective_boundary", "projective and boundary zero/fix", "FAIL", "projective guard and boundary C-work remain unsigned", "gates_3567"),
        ("ACT3568_5_lambda_source_ready", "lambda_C/K_spin bound schema", "PASS_SCHEMA_ONLY", "schema is source-ready but not numeric/source-backed", "kspin_3567"),
        ("ACT3568_6_public_selector", "public LC selector claim", "FAIL_CURRENT_PUBLIC_CLAIM", "symbolic certificate is not enough without parent-owned signs and zero inputs", "selector_3567"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "activation_id": activation_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for activation_id, gate, status, detail, source_key in rows
    ]


def decision_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3568_0_sign_certificate_derived_symbolically",
            "decision": "accept lambda_C=min_i a_i(1-eta_i) as the exact symbolic sign certificate",
            "reason": "diagonal positive sector weights plus Young/Schur cross bounds are the cleanest non-fitted way to prove M_C coercive",
            "consequence": "future work must source a_i and eta_ij rather than restating M_C missing",
            "status": "SYMBOLIC_CERTIFICATE_READY",
            "source_path": str(source_paths["gk_coercivity_2471"]),
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3568_1_no_public_selector",
            "decision": "do not promote LC selector as public theorem",
            "reason": "no parent-owned numeric/sign/unit payload for a_i, eta_ij, projective and boundary clauses",
            "consequence": "selector remains exact conditional; K_spin/lambda_C fallback remains live",
            "status": "PUBLIC_CLAIM_BLOCKED",
            "source_path": str(source_paths["positive_pack_1846"]),
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3568_2_best_next",
            "decision": "source or derive the first diagonal stiffness a_A for axial torsion",
            "reason": "axial torsion is the most direct spin/coupling local test channel and anchors one concrete lambda_C sector",
            "consequence": "3569 targets a_A/c_A sign-unit row or a parent theorem excluding axial torsion",
            "status": "NEXT_TARGET_SELECTED",
            "source_path": str(source_paths["operator_decomp_1833"]),
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "MC_SYMBOLIC_COERCIVITY_CERTIFICATE_DERIVED_NUMERIC_SIGN_INPUTS_MISSING",
            "strongest_result": "lambda_C=min_i a_i(1-eta_i) exact symbolic sign certificate and K_spin/lambda_C bound schema",
            "still_missing": "parent-signed a_i values/units, eta_ij cross bounds, projective gauge/invariance, boundary C-work silence, source-backed K_spin kernels",
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
            "next_id": "NEXT3568_0",
            "target_doc": "3569-Y5-R2FR-axial-torsion-stiffness-aA-or-cA-source-row.md",
            "target_script": "scripts/Y5_R2FR_3569_axial_torsion_stiffness_aA_or_cA_source_row.py",
            "objective": "derive or source the first diagonal distortion stiffness a_A/c_A for axial torsion; if impossible, create the first source-ready axial torsion response row with units and local test arenas",
            "success_gate": "a_A positive sign/unit certificate or c_A/K_A source-backed bound row",
            "reason": "3568 reduces M_C coercivity to sector weights a_i and cross bounds eta_ij; axial torsion is the closest spin/coupling sector",
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_item": "distortion_operator_MC_coercivity",
            "status": "SYMBOLIC_SIGN_CERTIFICATE_READY_NONCLAIM",
            "lambda_C_formula": "lambda_C=min_i a_i(1-eta_i)",
            "fallback": "epsilon_local_connection <= K_spin/lambda_C * residual_norm_sum",
            "next_action": "derive/source axial torsion stiffness a_A or c_A response",
            "valid_for_claim": False,
        }
    ]


def validate(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    blocks: list[dict[str, object]],
    coercivity: list[dict[str, object]],
    lambda_rows: list[dict[str, object]],
    activation: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in outputs.items() if key != "validation"}
    validations.append(("VAL3568_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required source paths exist"))
    needles = {
        "handoff_3567": "NEXT3567_0",
        "selector_3567": "SEL3567_3_positive_zero_theorem",
        "proof_3567": "DZ3567_2_coercivity",
        "kspin_3567": "KSP3567_6_lambdaC",
        "gates_3567": "GATE3567_2_positive_MC",
        "distortion_contract_1832": "DC1832_0_variable",
        "distortion_owner_1833": "DEO1833_2_M_C_operator",
        "operator_decomp_1833": "OPD1833_0_torsion_irreducible",
        "positive_nohair_3429": "PON3429_3_bound_branch",
        "positive_contract_3092": "NHC3092_2_zero_result",
        "positive_inputs_2949": "PIN2949_2_ZX",
        "positive_pack_1846": "OP1846_4_verdict",
        "gk_operator_2471": "OP2471_0_stationary_energy",
        "gk_coercivity_2471": "COER2471_5_current_status",
        "gk_eligibility_2471": "NHG2471_5_eligibility",
        "gk_positivity_2470": "POS2470_6_parent_sign",
        "local_geometry_3493": "LOCK3493_P4T3492_0_axial_torsion",
        "local_eh_r11": "torsion_nonmetricity",
        "double_zero_r11": "torsion_nonmetricity",
    }
    validations.append(("VAL3568_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected source needles found"))
    validations.append(("VAL3568_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3568 output files written"))
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
    validations.append(("VAL3568_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3568_4_operator_blocks_cover_modes", {"C_A", "C_T", "C_Q", "C_S", "C_P"}.issubset({str(row["mode_symbol"]) for row in blocks}), "operator blocks cover torsion/nonmetricity/projective modes"))
    validations.append(("VAL3568_5_lambda_formula_present", any(row["coercivity_id"] == "COER3568_3_lambda_formula" and "min_i" in str(row["statement"]) for row in coercivity), "lambda_C symbolic formula present"))
    validations.append(("VAL3568_6_bound_schema_present", any(row["bound_id"] == "LAMB3568_4_master_bound" for row in lambda_rows), "master K_spin/lambda_C bound row present"))
    validations.append(("VAL3568_7_public_claim_blocked", any(row["activation_id"] == "ACT3568_6_public_selector" and row["status"] == "FAIL_CURRENT_PUBLIC_CLAIM" for row in activation), "public selector claim remains blocked"))
    validations.append(("VAL3568_8_no_claim_flags", all(str(row["valid_for_claim"]).lower() == "false" for row in blocks + coercivity + lambda_rows + activation), "all generated physics rows remain nonclaim"))
    formalization_touched = any(FORMALIZATION.rglob("*3568*")) if FORMALIZATION.exists() else False
    validations.append(("VAL3568_9_formalization_workbench_untouched", not formalization_touched, "no 3568 checkpoint output appears in formalization-workbench"))
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
    blocks: list[dict[str, object]],
    coercivity: list[dict[str, object]],
    lambda_rows: list[dict[str, object]],
    activation: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3568 - Distortion operator MC sign certificate or lambdaC bound",
        "",
        "## Verdict",
        "3568 derives the exact symbolic sign certificate for the distortion operator.  Decompose `C = Gamma-Gamma_LC` into irreducible torsion/nonmetricity/projective modes.  If each diagonal mode has lower weight `a_i` and every mixed block obeys a Young/Schur cross bound with row-sum `eta_i<1`, then `M_C` is coercive with `lambda_C = min_i a_i(1-eta_i)`.",
        "",
        "That is a real rung: the LC selector no longer depends on an undefined positive operator.  But it is not a public local-GR claim because the actual parent-owned `a_i`, `eta_ij`, projective policy, boundary C-work and response kernels are still unsigned.  The fallback is now executable in form: `epsilon_local_connection <= K_spin/lambda_C * residual_norm_sum`.",
        "",
        "## Generated outputs",
    ]
    for output_id, path in outputs.items():
        lines.append(f"- `{output_id}`: `{path}`")
    lines.extend(["", "## Operator blocks"])
    for row in blocks:
        lines.append(f"- `{row['block_id']}` `{row['mode_symbol']}`: {row['diagonal_lower_weight']} ({row['zero_or_positive_condition']})")
    lines.extend(["", "## Coercivity certificate"])
    for row in coercivity:
        lines.append(f"- `{row['coercivity_id']}`: {row['statement']} ({row['status']})")
    lines.extend(["", "## Lambda/Kspin bound rows"])
    for row in lambda_rows:
        lines.append(f"- `{row['bound_id']}` `{row['symbol']}`: {row['formula']} ({row['status']})")
    lines.extend(["", "## Activation gates"])
    for row in activation:
        lines.append(f"- `{row['activation_id']}`: {row['status']} ({row['detail']})")
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
    blocks = operator_block_rows(source_paths)
    coercivity = coercivity_rows(source_paths)
    lambda_rows = lambda_bound_rows(source_paths)
    activation = activation_rows(source_paths)
    decisions = decision_rows(source_paths)
    status = status_rows()
    next_target = next_target_rows()
    canonical = canonical_status_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3568_SOURCE_REGISTER.csv",
        "operator_blocks": RESIDUALS / "P8_Y5_R2FR_3568_MC_OPERATOR_BLOCKS.csv",
        "coercivity_certificate": RESIDUALS / "P8_Y5_R2FR_3568_MC_COERCIVITY_CERTIFICATE.csv",
        "lambda_kspin_rows": RESIDUALS / "P8_Y5_R2FR_3568_LAMBDAC_KSPIN_BOUND_ROWS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3568_ACTIVATION_GATES.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3568_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3568_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3568_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_distortion_MC_coercivity_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3568_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], register)
    write_csv(outputs["operator_blocks"], blocks)
    write_csv(outputs["coercivity_certificate"], coercivity)
    write_csv(outputs["lambda_kspin_rows"], lambda_rows)
    write_csv(outputs["activation_gates"], activation)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], next_target)
    write_csv(outputs["canonical_status"], canonical)
    validation = validate(source_paths, outputs, blocks, coercivity, lambda_rows, activation)
    write_csv(outputs["validation"], validation)
    write_doc(outputs, blocks, coercivity, lambda_rows, activation, decisions, status, validation, next_target)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"3568 validation failed: {failed}")
    print(f"wrote {DOC}")
    for output_id, path in outputs.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
