from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3567-Y5-R2FR-local-LC-branch-selector-or-Kspin-P4-map.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_LOCAL_LC_SELECTOR_3567"
CHECKPOINT_ID = "3567"


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
        "handoff_3566": RESIDUALS / "P8_Y5_R2FR_3566_NEXT_TARGET.csv",
        "signature_3566": RESIDUALS / "P8_Y5_R2FR_3566_PARENT_LOCAL_LC_ACTION_SIGNATURE.csv",
        "variation_3566": RESIDUALS / "P8_Y5_R2FR_3566_NO_GAMMA_VARIATION_DERIVATION.csv",
        "activation_3566": RESIDUALS / "P8_Y5_R2FR_3566_SIGNATURE_ACTIVATION_GATES.csv",
        "p4_queue_3566": RESIDUALS / "P8_Y5_R2FR_3566_FIRST_SPIN_P4_COEFFICIENT_QUEUE.csv",
        "local_geometry_3079": RESIDUALS / "P8_Y5_R2FR_3079_LOCAL_GEOMETRY_FIELD_LIST_SIGNATURE_AUDIT.csv",
        "p4_geometry_3493": RESIDUALS / "P8_Y5_R2FR_3493_OFFICIAL_P4_LOCAL_GEOMETRY_INTERFACE.csv",
        "distortion_contract_1832": RESIDUALS / "P8_Y5_PARENT_QLOC_1832_DISTORTION_EQUATION_CONTRACT.csv",
        "distortion_owner_1833": RESIDUALS / "P8_Y5_PARENT_QLOC_1833_DISTORTION_EQUATION_OWNER_AUDIT.csv",
        "positive_nohair_3429": RESIDUALS / "P8_Y5_R2FR_3429_POSITIVE_OPERATOR_NOHAIR_THEOREM.csv",
        "positive_contract_3092": RESIDUALS / "P8_Y5_R2FR_3092_POSITIVE_NOHAIR_CONTRACT.csv",
        "positive_inputs_2949": RESIDUALS / "P8_Y5_R2FR_2949_POSITIVE_OPERATOR_INPUT_QUEUE.csv",
        "positive_pack_1846": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_POSITIVE_OPERATOR_PACK.csv",
        "gk_operator_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_OPERATOR_ANSATZ.csv",
        "gk_coercivity_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_COERCIVITY_AUDIT.csv",
        "gk_eligibility_2471": RESIDUALS / "P8_Y5_GK_OPERATOR_2471_NOHAIR_ELIGIBILITY.csv",
        "gk_positivity_2470": RESIDUALS / "P8_Y5_GK_NOHAIR_2470_POSITIVITY_CLAUSES.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    roles = {
        "handoff_3566": "declares 3567 target",
        "signature_3566": "local LC action signature and no-independent-Gamma branch",
        "variation_3566": "internal no-Gamma/E_spin zero derivation",
        "activation_3566": "branch selector remains public gap",
        "p4_queue_3566": "first affine/P4 coefficient queue",
        "local_geometry_3079": "local geometry field-list and no-independent-connection gap",
        "p4_geometry_3493": "official local geometry P4 interface",
        "distortion_contract_1832": "distortion equation contract C=Gamma-Gamma_LC",
        "distortion_owner_1833": "distortion equation owner audit",
        "positive_nohair_3429": "positive operator no-hair theorem",
        "positive_contract_3092": "positive no-hair energy identity contract",
        "positive_inputs_2949": "positive operator input queue",
        "positive_pack_1846": "positive operator sign/gap pack",
        "gk_operator_2471": "explicit stationary quadratic operator ansatz",
        "gk_coercivity_2471": "coercivity inequalities for mixed operator",
        "gk_eligibility_2471": "no-hair eligibility status",
        "gk_positivity_2470": "positivity clauses and boundary/topology caveats",
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


def selector_theorem_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "SEL3567_0_distortion_variable",
            "distortion split",
            "C^lambda_{mu nu} := Gamma^lambda_{mu nu} - Gamma_LC^lambda_{mu nu}[g_obs]",
            "Any affine deviation from LC is now a named distortion field C; if C is absent, LC branch is kinematic; if C is present, it must obey an equation or become P4.",
            "EXACT_DEFINITION",
            "distortion_contract_1832",
        ),
        (
            "SEL3567_1_domain_selector",
            "type/domain selector",
            "Allowed(Conf_loc^LC) excludes C/Gamma_ind/omega_ind.",
            "This is the 3566 private branch selector. It buys E_spin=0 internally but does not prove why the full parent cannot choose affine C.",
            "PRIVATE_SELECTOR_BRANCH_NOT_PUBLIC_DERIVATION",
            "signature_3566",
        ),
        (
            "SEL3567_2_dynamic_selector_equation",
            "dynamic distortion selector",
            "delta_C S_parent = M_C C - Delta_Gamma + B_C + P_C + N_C(C) = 0",
            "If C is admitted, it must be controlled by a parent-owned Euler equation with operator M_C, source hypermomentum Delta_Gamma, boundary work B_C, projective kernel P_C and nonlinear remainder N_C.",
            "SELECTOR_EQUATION_WRITTEN",
            "distortion_owner_1833",
        ),
        (
            "SEL3567_3_positive_zero_theorem",
            "positive source-free zero",
            "If <C,M_C C> >= lambda_C ||C||^2, Delta_Gamma=B_C=P_C=0, and ||N_C(C)|| <= c_N ||C||^2 inside c_N||C|| < lambda_C, then C=0.",
            "Multiply the C equation by C and integrate. Positivity gives lambda_C||C||^2 <= c_N||C||^3. In the small local branch this implies ||C||=0.",
            "EXACT_CONDITIONAL_SELECTOR_THEOREM",
            "positive_nohair_3429",
        ),
        (
            "SEL3567_4_bound_theorem",
            "finite affine fallback bound",
            "||C|| <= lambda_C^-1 (||Delta_Gamma|| + ||B_C|| + ||P_C|| + ||N_C(C)||)",
            "If any source/boundary/projective term survives, the same equation becomes a P4/K_spin bound rather than a closure assumption.",
            "BOUND_FORMULA_READY_VALUES_MISSING",
            "positive_nohair_3429",
        ),
        (
            "SEL3567_5_Espin_link",
            "connection residual map",
            "E_spin_abs <= K_spin ||C|| + epsilon_noGamma_branch",
            "3566 makes epsilon_noGamma_branch=0 in the LC branch. Outside it, K_spin maps distortion amplitude into WEP/PPN/clock/light/orbit/R10 response.",
            "P4_MAP_SYMBOLIC_NONCLAIM",
            "p4_geometry_3493",
        ),
        (
            "SEL3567_6_live_verdict",
            "current MTS selector status",
            "The LC selector is derived as a conditional theorem, but not activated as a public parent theorem because M_C positivity, boundary/projective silence and parent-owned C equation are unsigned.",
            "This is progress: the missing item is now a precise distortion operator/sign/source theorem, not a vague coupling gap.",
            "CONDITIONAL_SELECTOR_NOT_PUBLIC_CLAIM",
            "activation_3566",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "selector_id": selector_id,
            "name": name,
            "statement": statement,
            "derivation_or_effect": derivation,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for selector_id, name, statement, derivation, status, source_key in rows
    ]


def distortion_proof_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "DZ3567_0_equation",
            "Euler equation",
            "M_C C = Delta_Gamma - B_C - P_C - N_C(C)",
            "STARTING_POINT",
            "distortion_owner_1833",
        ),
        (
            "DZ3567_1_energy_identity",
            "multiply by C and integrate over compact local exterior A",
            "<C,M_C C> = <C,Delta_Gamma-B_C-P_C-N_C(C)> + boundary_pairing",
            "EXACT_CONDITIONAL_IDENTITY",
            "positive_contract_3092",
        ),
        (
            "DZ3567_2_coercivity",
            "positive/invertible nonprojective operator",
            "<C,M_C C> >= lambda_C ||C||^2 after quotienting gauge/projective zero modes",
            "MISSING_PARENT_SIGN_CERTIFICATE",
            "gk_coercivity_2471",
        ),
        (
            "DZ3567_3_source_zero",
            "hypermomentum/source zero",
            "Delta_Gamma=0 if 3566 no-Gamma branch is selected across matter/source/readout sectors",
            "PRIVATE_BRANCH_PASS_PUBLIC_SELECTOR_OPEN",
            "variation_3566",
        ),
        (
            "DZ3567_4_boundary_zero",
            "connection boundary work",
            "B_C=0 if integration-by-parts, symplectic and worldtube boundary C-work are fixed/proper/no-flux",
            "BOUNDARY_UNSIGNED_RETAINS_ROW",
            "distortion_owner_1833",
        ),
        (
            "DZ3567_5_projective_zero",
            "projective kernel",
            "P_C=0 if projective trace is absent, gauge-fixed or all-sector unobservable",
            "PROJECTIVE_UNSIGNED_RETAINS_ROW",
            "p4_geometry_3493",
        ),
        (
            "DZ3567_6_nonlinear_radius",
            "small-branch control",
            "||N_C(C)|| <= c_N ||C||^2 and c_N||C|| < lambda_C",
            "LOCAL_SMALL_BRANCH_PREMISE_UNSIGNED",
            "positive_nohair_3429",
        ),
        (
            "DZ3567_7_zero_result",
            "LC dynamic selector",
            "C=0",
            "EXACT_IF_DZ3567_2_TO_DZ3567_6_PASS_TOGETHER",
            "positive_nohair_3429",
        ),
        (
            "DZ3567_8_bound_result",
            "affine fallback",
            "||C|| <= lambda_C^-1(||Delta_Gamma||+||B_C||+||P_C||+||N_C||)",
            "P4_BOUND_IF_ANY_PREMISE_FAILS",
            "distortion_contract_1832",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "proof_id": proof_id,
            "step": step,
            "mathematical_statement": statement,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for proof_id, step, statement, status, source_key in rows
    ]


def kspin_map_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "KSP3567_0_master",
            "epsilon_local_connection",
            "epsilon_local_connection <= K_spin lambda_C^-1 (||Delta_Gamma||+||B_C||+||P_C||+||N_C||)",
            "local WEP/PPN/clock/light/orbit/R10 response units",
            "SYMBOLIC_EXECUTABLE_FORMULA_NONCLAIM",
            "K_spin, lambda_C and component norms with source paths",
            "p4_queue_3566",
        ),
        (
            "KSP3567_1_axial_torsion",
            "epsilon_axial_torsion_spin",
            "epsilon_axial_torsion_spin <= K_A ||C_axial||",
            "spin/clock/WEP response",
            "ZERO_IF_SELECTOR_CLOSES_ELSE_COEFFICIENT_MISSING",
            "K_A or c_A and fermion/spin source density",
            "p4_geometry_3493",
        ),
        (
            "KSP3567_2_projective_trace",
            "epsilon_projective_trace",
            "epsilon_projective_trace <= K_P ||C_projective||",
            "clock/orbit/WEP/source trace response",
            "ZERO_IF_PROJECTIVE_GUARD_CLOSES_ELSE_BOUND_MISSING",
            "projective gauge/invariance proof or K_P",
            "p4_geometry_3493",
        ),
        (
            "KSP3567_3_weyl_nonmetricity",
            "epsilon_weyl_nonmetricity",
            "epsilon_weyl_nonmetricity <= K_Q ||Q_mu||",
            "clock/rod/source normalization response",
            "ZERO_IF_METRIC_COMPATIBILITY_SELECTOR_CLOSES_ELSE_BOUND_MISSING",
            "K_Q and clock/source response kernel",
            "p4_geometry_3493",
        ),
        (
            "KSP3567_4_shear_nonmetricity",
            "epsilon_shear_nonmetricity",
            "epsilon_shear_nonmetricity <= K_Qs ||Q_tilde||",
            "lightcone/PPN/shear response",
            "ZERO_IF_OPTICAL_METRIC_SELECTOR_CLOSES_ELSE_BOUND_MISSING",
            "K_Qs and optical/PPN kernel",
            "p4_geometry_3493",
        ),
        (
            "KSP3567_5_hypermomentum",
            "epsilon_hypermomentum_source",
            "epsilon_hypermomentum_source <= K_Delta ||Delta_Gamma||",
            "source-current response",
            "ZERO_INSIDE_3566_BRANCH_ELSE_KERNEL_MISSING",
            "K_Delta and source/readout action derivative",
            "variation_3566",
        ),
        (
            "KSP3567_6_lambdaC",
            "lambda_C",
            "lambda_C = lower coercivity bound of M_C on non-gauge/nonprojective C modes",
            "inverse length^2 or action-normalized operator eigenvalue",
            "MISSING_PARENT_SIGN_AND_UNITS",
            "operator basis, sign certificate, boundary domain, units",
            "positive_inputs_2949",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "map_id": map_id,
            "residual_symbol": residual,
            "bound_formula": formula,
            "units": units,
            "status": status,
            "required_inputs": required,
            "source_path": str(source_paths[source_key]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for map_id, residual, formula, units, status, required, source_key in rows
    ]


def activation_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        (
            "GATE3567_0_equation_owner",
            "parent owns distortion equation",
            "FAIL",
            "M_C C = Delta_Gamma - B_C - P_C - N_C(C) is written as a selector law but not parent-derived",
            "distortion_owner_1833",
        ),
        (
            "GATE3567_1_noGamma_source",
            "Delta_Gamma source term zero",
            "PASS_PRIVATE_BRANCH_ONLY",
            "3566 gives zero inside LC branch; public selector still needed",
            "variation_3566",
        ),
        (
            "GATE3567_2_positive_MC",
            "M_C coercive positive",
            "FAIL",
            "lambda_C/sign/operator units are missing",
            "positive_pack_1846",
        ),
        (
            "GATE3567_3_boundary_projective",
            "B_C=P_C=0",
            "FAIL",
            "boundary and projective kernels remain open",
            "distortion_owner_1833",
        ),
        (
            "GATE3567_4_zero_selector",
            "C=0 local selector theorem live",
            "FAIL_CURRENT_PUBLIC_CLAIM",
            "exact conditional theorem exists but inputs not parent-signed together",
            "positive_nohair_3429",
        ),
        (
            "GATE3567_5_bound_branch",
            "K_spin/P4 map ready",
            "PARTIAL_SYMBOLIC_PASS",
            "formula exists; numeric/source-backed K_spin/lambda_C missing",
            "p4_geometry_3493",
        ),
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
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, detail, source_key in rows
    ]


def decision_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3567_0_selector_mechanism_written",
            "decision": "use the distortion positive-operator equation as the branch selector mechanism",
            "reason": "it explains LC selection dynamically if C is admitted, and reduces to 3566 variable absence if C is not admitted",
            "consequence": "the missing step is now M_C/sign/boundary/projective/source inputs, not a vague coupling problem",
            "status": "CONDITIONAL_SELECTOR_THEOREM_WRITTEN",
            "source_path": str(source_paths["distortion_contract_1832"]),
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3567_1_no_public_promotion",
            "decision": "do not promote LC selector as a public parent theorem",
            "reason": "M_C positivity/operator ownership plus boundary/projective silence are unsigned",
            "consequence": "retain K_spin/P4 map",
            "status": "PUBLIC_SELECTOR_BLOCKED",
            "source_path": str(source_paths["gk_coercivity_2471"]),
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3567_2_best_next",
            "decision": "derive or source the distortion operator M_C next",
            "reason": "M_C positivity is the highest-leverage input: if it closes with zero sources/boundary/projective, LC follows; if not, it gives lambda_C for K_spin bounds",
            "consequence": "3568 targets M_C operator/sign certificate or first lambda_C/K_spin source row",
            "status": "NEXT_TARGET_SELECTED",
            "source_path": str(source_paths["positive_inputs_2949"]),
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "LC_SELECTOR_CONDITIONAL_THEOREM_WRITTEN_NOT_PUBLICLY_ACTIVATED",
            "strongest_result": "distortion equation plus positive operator theorem gives C=0 if M_C is coercive and source/boundary/projective terms vanish",
            "still_missing": "parent-owned M_C operator/sign/unit certificate, boundary C-work silence, projective all-sector guard, public Delta_Gamma zero outside private branch",
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
            "next_id": "NEXT3567_0",
            "target_doc": "3568-Y5-R2FR-distortion-operator-MC-sign-certificate-or-lambdaC-bound.md",
            "target_script": "scripts/Y5_R2FR_3568_distortion_operator_MC_sign_certificate_or_lambdaC_bound.py",
            "objective": "derive a parent-owned positive/invertible distortion operator M_C with units and boundary domain; if not possible, create the first source-ready lambda_C/K_spin bound row",
            "success_gate": "M_C coercivity/sign certificate closes, or lambda_C and K_spin gain source-backed units/map rows",
            "reason": "3567 reduces local LC selection to M_C positivity plus zero source/boundary/projective terms",
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_item": "local_LC_branch_selector",
            "status": "CONDITIONAL_DISTORTION_ZERO_THEOREM",
            "internal_zero_route": "C absent by 3566 signature or C forced zero by positive source-free M_C equation",
            "fallback_route": "K_spin/lambda_C P4 affine map",
            "next_action": "derive M_C positivity/sign certificate",
            "valid_for_claim": False,
        }
    ]


def validate(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    selector: list[dict[str, object]],
    proof: list[dict[str, object]],
    kspin: list[dict[str, object]],
    gates: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in outputs.items() if key != "validation"}
    validations.append(("VAL3567_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required source paths exist"))
    needles = {
        "handoff_3566": "NEXT3566_0",
        "signature_3566": "SIG3566_10_total_signature",
        "variation_3566": "VAR3566_8_Espin_total",
        "activation_3566": "ACT3566_1_public_parent_selector",
        "p4_queue_3566": "P4C3566_6_Kspin_map",
        "local_geometry_3079": "LGS3079_0_metric_coframe_parent",
        "p4_geometry_3493": "LOCK3493_P4T3492_0_axial_torsion",
        "distortion_contract_1832": "DC1832_0_variable",
        "distortion_owner_1833": "DEO1833_2_M_C_operator",
        "positive_nohair_3429": "PON3429_2_zero_branch",
        "positive_contract_3092": "NHC3092_2_zero_result",
        "positive_inputs_2949": "PIN2949_2_ZX",
        "positive_pack_1846": "OP1846_4_verdict",
        "gk_operator_2471": "OP2471_0_stationary_energy",
        "gk_coercivity_2471": "COER2471_5_current_status",
        "gk_eligibility_2471": "NHG2471_5_eligibility",
        "gk_positivity_2470": "POS2470_6_parent_sign",
    }
    validations.append(
        (
            "VAL3567_1_required_needles_found",
            all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()),
            "all selected source needles found",
        )
    )
    validations.append(("VAL3567_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3567 output files written"))
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
    validations.append(("VAL3567_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(
        (
            "VAL3567_4_selector_equation_present",
            any(row["selector_id"] == "SEL3567_2_dynamic_selector_equation" for row in selector),
            "distortion selector equation row present",
        )
    )
    validations.append(
        (
            "VAL3567_5_positive_zero_theorem_present",
            any(row["selector_id"] == "SEL3567_3_positive_zero_theorem" for row in selector) and any(row["proof_id"] == "DZ3567_7_zero_result" for row in proof),
            "positive C=0 theorem and proof row present",
        )
    )
    validations.append(
        (
            "VAL3567_6_kspin_bound_map_present",
            {"epsilon_local_connection", "lambda_C", "epsilon_axial_torsion_spin"}.issubset({str(row["residual_symbol"]) for row in kspin}),
            "K_spin/lambda_C fallback map rows present",
        )
    )
    validations.append(
        (
            "VAL3567_7_public_claim_blocked",
            any(row["gate_id"] == "GATE3567_4_zero_selector" and row["status"] == "FAIL_CURRENT_PUBLIC_CLAIM" for row in gates),
            "public selector claim remains blocked",
        )
    )
    validations.append(
        (
            "VAL3567_8_nonclaim_flags",
            all(str(row["valid_for_claim"]).lower() == "false" for row in selector + proof + kspin + gates),
            "all generated physics rows remain nonclaim",
        )
    )
    formalization_touched = any(FORMALIZATION.rglob("*3567*")) if FORMALIZATION.exists() else False
    validations.append(("VAL3567_9_formalization_workbench_untouched", not formalization_touched, "no 3567 checkpoint output appears in formalization-workbench"))
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
    selector: list[dict[str, object]],
    proof: list[dict[str, object]],
    kspin: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines: list[str] = [
        "# 3567 - Local LC branch selector or Kspin P4 map",
        "",
        "## Verdict",
        "3567 gives the first real selector mechanism for the LC/no-independent-affine branch.  Write the distortion field `C = Gamma - Gamma_LC[g_obs]`.  If `C` is absent, 3566 already gives the LC branch kinematically.  If `C` is present, the parent must provide an equation `M_C C = Delta_Gamma - B_C - P_C - N_C(C)`.",
        "",
        "The useful theorem is exact but conditional: if `M_C` is coercive/positive on non-gauge modes, `Delta_Gamma=0`, boundary work vanishes, projective leakage vanishes, and nonlinear terms stay inside the small branch, then `C=0`.  If any of those fail, the same equation gives the `K_spin/lambda_C` P4 bound map.",
        "",
        "So the local connection problem has moved from 'what is the coupling?' to a concrete target: derive/source the distortion operator `M_C` and its sign certificate.",
        "",
        "## Generated outputs",
    ]
    for output_id, path in outputs.items():
        lines.append(f"- `{output_id}`: `{path}`")
    lines.extend(["", "## Selector theorem"])
    for row in selector:
        lines.append(f"- `{row['selector_id']}`: {row['statement']} ({row['status']})")
    lines.extend(["", "## Distortion proof"])
    for row in proof:
        lines.append(f"- `{row['proof_id']}` `{row['step']}`: {row['mathematical_statement']} ({row['status']})")
    lines.extend(["", "## Kspin/P4 map"])
    for row in kspin:
        lines.append(f"- `{row['map_id']}` `{row['residual_symbol']}`: {row['bound_formula']} ({row['status']})")
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
    lines.extend(
        [
            "",
            "## Next target",
            f"- `{next_target[0]['target_doc']}`",
            f"- Objective: {next_target[0]['objective']}",
        ]
    )
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    register = source_register(source_paths)
    selector = selector_theorem_rows(source_paths)
    proof = distortion_proof_rows(source_paths)
    kspin = kspin_map_rows(source_paths)
    gates = activation_rows(source_paths)
    decisions = decision_rows(source_paths)
    status = status_rows()
    next_target = next_target_rows()
    canonical = canonical_status_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3567_SOURCE_REGISTER.csv",
        "selector_theorem": RESIDUALS / "P8_Y5_R2FR_3567_LOCAL_LC_SELECTOR_THEOREM.csv",
        "distortion_proof": RESIDUALS / "P8_Y5_R2FR_3567_DISTORTION_ZERO_PROOF.csv",
        "kspin_map": RESIDUALS / "P8_Y5_R2FR_3567_KSPIN_P4_BOUND_MAP.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3567_SELECTOR_ACTIVATION_GATES.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3567_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3567_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3567_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_local_LC_branch_selector_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3567_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], register)
    write_csv(outputs["selector_theorem"], selector)
    write_csv(outputs["distortion_proof"], proof)
    write_csv(outputs["kspin_map"], kspin)
    write_csv(outputs["activation_gates"], gates)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], next_target)
    write_csv(outputs["canonical_status"], canonical)
    validation = validate(source_paths, outputs, selector, proof, kspin, gates)
    write_csv(outputs["validation"], validation)
    write_doc(outputs, selector, proof, kspin, gates, decisions, status, validation, next_target)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"3567 validation failed: {failed}")
    print(f"wrote {DOC}")
    for output_id, path in outputs.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
