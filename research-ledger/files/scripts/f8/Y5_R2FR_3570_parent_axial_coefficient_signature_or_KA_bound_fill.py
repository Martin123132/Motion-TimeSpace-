from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3570-Y5-R2FR-parent-axial-coefficient-signature-or-KA-bound-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_PARENT_AXIAL_SELECTOR_3570"
CHECKPOINT_ID = "3570"


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
        "handoff_3569": RESIDUALS / "P8_Y5_R2FR_3569_NEXT_TARGET.csv",
        "axial_derivation_3569": RESIDUALS / "P8_Y5_R2FR_3569_AXIAL_TORSION_STIFFNESS_DERIVATION.csv",
        "axial_source_3569": RESIDUALS / "P8_Y5_R2FR_3569_AXIAL_RESPONSE_SOURCE_ROWS.csv",
        "validation_3569": RESIDUALS / "P8_Y5_BRR545_3569_VALIDATION.csv",
        "signature_3566": RESIDUALS / "P8_Y5_R2FR_3566_PARENT_LOCAL_LC_ACTION_SIGNATURE.csv",
        "variation_3566": RESIDUALS / "P8_Y5_R2FR_3566_NO_GAMMA_VARIATION_DERIVATION.csv",
        "coeff_queue_3566": RESIDUALS / "P8_Y5_R2FR_3566_FIRST_SPIN_P4_COEFFICIENT_QUEUE.csv",
        "status_3566": RESIDUALS / "P8_Y5_R2FR_3566_STATUS.csv",
        "source_signature_3497": RESIDUALS / "P8_Y5_R2FR_3497_MINIMAL_PARENT_SOURCE_ACTION_SIGNATURE.csv",
        "variation_chain_3497": RESIDUALS / "P8_Y5_R2FR_3497_VARIATION_CHAIN.csv",
        "em_signature_3506": RESIDUALS / "P8_Y5_R2FR_3506_PARENT_VISIBLE_EM_GENERATOR_SIGNATURE.csv",
        "spin_p4_3565": RESIDUALS / "P8_Y5_R2FR_3565_P4_SPIN_HYPERMOMENTUM_BOUND_ROWS.csv",
        "spin_theorem_3565": RESIDUALS / "P8_Y5_R2FR_3565_SPIN_TORSION_THEOREM_STACK.csv",
        "kspin_3567": RESIDUALS / "P8_Y5_R2FR_3567_KSPIN_P4_BOUND_MAP.csv",
        "sector_gamma_3493": RESIDUALS / "P8_Y5_R2FR_3493_SECTOR_GAMMA_SIGNATURE_MATRIX.csv",
        "sector_gamma_3565": RESIDUALS / "P8_Y5_R2FR_3565_SECTOR_GAMMA_SLOT_VERDICT.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    roles = {
        "handoff_3569": "declares 3570 target",
        "axial_derivation_3569": "imports axial stiffness fork",
        "axial_source_3569": "imports source-ready axial coefficient rows",
        "validation_3569": "imports last checkpoint validation",
        "signature_3566": "imports private LC local action signature",
        "variation_3566": "imports no-Gamma variation proof",
        "coeff_queue_3566": "imports c_A/K_spin queue",
        "status_3566": "imports missing public selector status",
        "source_signature_3497": "imports minimal parent source action domain",
        "variation_chain_3497": "imports source-current Gamma variation chain",
        "em_signature_3506": "imports Maxwell/Poynting same-frame domain",
        "spin_p4_3565": "imports official affine fallback envelope",
        "spin_theorem_3565": "imports variable-absence theorem",
        "kspin_3567": "imports local response bound map",
        "sector_gamma_3493": "imports sector Gamma signature matrix",
        "sector_gamma_3565": "imports current sector Gamma slot verdict",
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


def zero_certificate_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "AZC3570_0_configuration",
            "configuration excludes independent affine variables",
            "Arg(S_loc^LC) contains q(Phi), e_obs/g_obs, ordinary matter, A_Q, theta/tau, boundary/topology and source-normalization data, but no Gamma_ind/omega_ind.",
            "C_A is not a coordinate of the selected branch.",
            "PRIVATE_PASS_PUBLIC_SELECTOR_UNSIGNED",
            "signature_3566",
        ),
        (
            "AZC3570_1_matter_spin",
            "ordinary spinors use omega_LC[e_obs]",
            "S_m depends on D_LC[e_obs,A_Q] and not on a torsionful spin connection.",
            "delta S_m/delta C_A=0 by variable absence; spin stress remains in the coframe/Hilbert equation.",
            "PRIVATE_PASS",
            "signature_3566",
        ),
        (
            "AZC3570_2_visible_EM",
            "Maxwell/Poynting energy is same-frame Hilbert source",
            "S_EM uses A_Q,F_Q,*_obs(e_obs) and has no affine Gamma argument; Poynting energy is included in J_H/H_tau or retained as named boundary flux.",
            "EM cannot source axial torsion through hidden affine slots inside the LC branch.",
            "PRIVATE_PASS_ALPHA_SCALAR_COUPLING_SEPARATE",
            "em_signature_3506",
        ),
        (
            "AZC3570_3_source_current",
            "source current descends from e_obs Hilbert variation",
            "J_H[tau] is derived from S_m+S_EM by e_obs variation, so delta_Gamma_ind J_H=0 when e_obs/q are the only geometry arguments.",
            "J5_A and hypermomentum source vanish inside the branch.",
            "PRIVATE_PASS_REGULAR_SUPPORT_CONDITIONAL",
            "variation_3566",
        ),
        (
            "AZC3570_4_projector_domain",
            "projector/domain maps cannot reintroduce Gamma_ind",
            "Pi_M, collars, weights and boundary transport must be q/e_obs/tau/topology-natural before variation.",
            "This is the weakest LC-zero clause: if Pi uses Gamma_ind, the axial zero certificate fails and the P4 affine row is live.",
            "PRIVATE_CONDITIONAL_WEAK_LINK",
            "variation_chain_3497",
        ),
        (
            "AZC3570_5_readouts",
            "clock/light/orbit/WEP/PPN/R10 readouts are post-variation",
            "R_arena is a functor of solved e_obs,A_Q,J_H,M_H,tau,theta_A and cannot create the parent source current.",
            "readouts test residuals but do not create C_A in the action.",
            "PRIVATE_PASS_OPERATOR_TESTS_REMAIN",
            "signature_3566",
        ),
        (
            "AZC3570_6_projective_boundary",
            "projective and boundary sectors are absent or fixed in LC branch",
            "No independent projective direction exists in the LC branch; boundary/reference data are e_obs/LC fixed before readout.",
            "C_A=0 is not spoiled by projective trace if the branch selector and boundary owner are accepted.",
            "PRIVATE_CONDITIONAL_BOUNDARY_SOURCE_OWNER_OPEN",
            "signature_3566",
        ),
        (
            "AZC3570_7_total",
            "parent axial zero certificate",
            "If AZC3570_0 through AZC3570_6 are promoted from private branch signature to parent-selected public branch, then C_A=0, c_A is not live, K_A is not needed, and epsilon_axial_torsion_spin=0.",
            "This is the clean route to local LC/GR for the axial channel; no small torsion coefficient is fitted.",
            "EXACT_BRANCH_THEOREM_PUBLIC_NOT_YET_CLAIMED",
            "axial_derivation_3569",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "certificate_id": certificate_id,
            "clause": clause,
            "formal_content": formal_content,
            "effect_on_axial_channel": effect,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "private_branch_pass": True,
            "public_parent_derived": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for certificate_id, clause, formal_content, effect, status, source_key in specs
    ]


def selector_contract_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "SEL3570_0_selector_variable",
            "B_LC_selector",
            "B_LC_selector=1 iff the parent-selected ordinary/source/readout branch excludes Gamma_ind/omega_ind in every active sector; otherwise B_LC_selector=0 and affine residual rows are live.",
            "boolean structural selector",
            "PRIVATE_BRANCH_VALUE_1_PUBLIC_VALUE_UNDERIVED",
            "coeff_queue_3566",
        ),
        (
            "SEL3570_1_axial_split",
            "C_A_public",
            "C_A_public = (1-B_LC_selector) C_A_affine, with C_A_affine governed by the retained affine equation.",
            "m^-1",
            "DERIVED_SPLIT_CONTRACT",
            "axial_derivation_3569",
        ),
        (
            "SEL3570_2_response_split",
            "epsilon_A_public",
            "epsilon_A_public = (1-B_LC_selector) * K_A/[a_A(1-eta_A)] * (||J5_A||+||B_A||+||P_A||+||N_A||+||R_A_mix||).",
            "arena residual units",
            "DERIVED_NO_SMUGGLING_CONTRACT",
            "axial_source_3569",
        ),
        (
            "SEL3570_3_coefficients_when_LC",
            "c_A,K_A,Z_A,m_A^2,eta_A",
            "When B_LC_selector=1, affine axial coefficients are inactive/undefined rather than fitted small; the observable axial tail is zero because C_A is absent.",
            "branch logic",
            "DERIVED_BRANCH_LOGIC",
            "variation_3566",
        ),
        (
            "SEL3570_4_coefficients_when_affine",
            "a_A,K_A,c_A",
            "When B_LC_selector=0, the theory must provide parent-owned or sourced Z_A,m_A^2,lambda_1,eta_A,K_A/c_A and numerator norms before any local test claim.",
            "coefficient contract",
            "AFFINE_FALLBACK_SOURCE_READY_NONCLAIM",
            "axial_source_3569",
        ),
        (
            "SEL3570_5_public_gate",
            "axial_local_GR_gate",
            "public pass iff B_LC_selector is parent-derived OR all affine coefficient/numerator/arena rows are source-backed and satisfy the empirical bound.",
            "boolean",
            "FALSE_CURRENTLY",
            "status_3566",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "selector_id": selector_id,
            "symbol": symbol,
            "contract": contract,
            "units": units,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for selector_id, symbol, contract, units, status, source_key in specs
    ]


def coefficient_attempt_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "COEF3570_0_cA_LC",
            "c_A",
            "LC branch",
            "inactive/not a coordinate coefficient",
            "not live",
            "C_A is absent; c_A is not tuned to zero and not fitted.",
            "DERIVED_INSIDE_BRANCH",
            "variation_3566",
        ),
        (
            "COEF3570_1_KA_LC",
            "K_A",
            "LC branch",
            "not required",
            "not live",
            "epsilon_A=K_A||C_A||=0 because C_A=0/absent, independent of K_A.",
            "DERIVED_INSIDE_BRANCH",
            "axial_derivation_3569",
        ),
        (
            "COEF3570_2_ZA_affine",
            "Z_A",
            "affine fallback",
            "coefficient of |nabla C_A|^2",
            "MISSING_PARENT_SIGN_CERTIFICATE",
            "No source-backed parent second-variation row found in the current axial files.",
            "NOT_FILLED",
            "axial_source_3569",
        ),
        (
            "COEF3570_3_mA2_affine",
            "m_A^2",
            "affine fallback",
            "zeroth-order axial operator gap",
            "MISSING_PARENT_GAP",
            "No parent-signed mass/gap/range row found for retained axial torsion.",
            "NOT_FILLED",
            "axial_source_3569",
        ),
        (
            "COEF3570_4_etaA_affine",
            "eta_A",
            "affine fallback",
            "sum of axial cross-term Young/Schur bounds",
            "MISSING_CROSS_BOUNDS",
            "The general eta rule exists, but axial-specific eta_Aj values are not signed.",
            "NOT_FILLED",
            "axial_derivation_3569",
        ),
        (
            "COEF3570_5_KA_affine",
            "K_A",
            "affine fallback",
            "operator norm from ||C_A|| to spin/clock/WEP/KRT residual",
            "MISSING_RESPONSE_KERNEL",
            "The map form exists; no arena projection kernel is sourced.",
            "NOT_FILLED",
            "kspin_3567",
        ),
        (
            "COEF3570_6_cA_affine",
            "c_A or xi_A",
            "affine fallback",
            "matter axial spin-torsion coupling coefficient",
            "MISSING_COUPLING_COEFFICIENT",
            "Earlier xi_A=0 is only inside candidate LC branch; affine coefficient remains unsourced.",
            "NOT_FILLED",
            "coeff_queue_3566",
        ),
        (
            "COEF3570_7_affine_master",
            "epsilon_A_affine",
            "affine fallback",
            "K_A/[a_A(1-eta_A)] times axial numerator",
            "SCHEMA_FILLED_NUMERIC_VALUES_MISSING",
            "This row is the honest nonclaim test path if the LC selector fails.",
            "SOURCE_READY_NONCLAIM",
            "axial_source_3569",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "branch": branch,
            "formula_or_value": formula,
            "units": units,
            "finding": finding,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for coefficient_id, symbol, branch, formula, units, finding, status, source_key in specs
    ]


def bound_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "BOUND3570_0_axial_public",
            "epsilon_A_public",
            "(1-B_LC_selector) * epsilon_A_affine",
            "arena residual units",
            "exact split; nonzero only if affine branch is live",
            "selector_contract",
            "selector",
        ),
        (
            "BOUND3570_1_axial_affine",
            "epsilon_A_affine",
            "K_A/[a_A(1-eta_A)] * (||J5_A||+||B_A||+||P_A||+||N_A||+||R_A_mix||)",
            "arena residual units",
            "source-ready nonclaim formula",
            "axial_source_3569",
            "affine",
        ),
        (
            "BOUND3570_2_LC_zero",
            "epsilon_A_LC",
            "0",
            "arena residual units",
            "exact inside selected LC branch because C_A is absent",
            "zero_certificate",
            "LC",
        ),
        (
            "BOUND3570_3_claim_condition",
            "axial_claim_allowed",
            "B_LC_selector parent-derived OR affine rows numeric/sourced/below bounds",
            "boolean",
            "false now",
            "selector_contract",
            "gate",
        ),
    ]
    source_lookup = {
        "selector_contract": source_paths["coeff_queue_3566"],
        "axial_source_3569": source_paths["axial_source_3569"],
        "zero_certificate": source_paths["signature_3566"],
    }
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": bound_id,
            "symbol": symbol,
            "formula": formula,
            "units": units,
            "interpretation": interpretation,
            "branch": branch,
            "source_path": str(source_lookup[source_key]),
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for bound_id, symbol, formula, units, interpretation, source_key, branch in specs
    ]


def activation_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        ("GATE3570_0_sources", "source audit", "PASS", "all required 3570 source paths exist"),
        ("GATE3570_1_private_LC_certificate", "private axial zero", "PASS_PRIVATE_ONLY", "all LC branch clauses needed for C_A absence are present as private/candidate rows"),
        ("GATE3570_2_public_selector", "public B_LC selector", "FAIL_CURRENT_PUBLIC_CLAIM", "3566 status explicitly says parent branch-selector theorem is still missing"),
        ("GATE3570_3_affine_ZA", "affine Z_A", "FAIL_AFFINE_NUMERIC_CLAIM", "no parent-signed axial kinetic coefficient found"),
        ("GATE3570_4_affine_mA2_eta", "affine gap/cross terms", "FAIL_AFFINE_NUMERIC_CLAIM", "no parent-signed m_A^2 or eta_A values found"),
        ("GATE3570_5_affine_KA_cA", "affine response/coupling", "FAIL_AFFINE_NUMERIC_CLAIM", "no sourced K_A/c_A or xi_A outside LC candidate branch"),
        ("GATE3570_6_public_axial_local_GR", "public axial local-GR pass", "FAIL_CURRENT_PUBLIC_CLAIM", "local-GR axial channel remains private-zero or source-ready affine fallback, not a claim"),
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
            "source_path": str(source_paths["status_3566"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, gate, status, detail in specs
    ]


def decision_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3570_0_best_route",
            "prioritize the LC branch selector over hunting arbitrary affine torsion numbers",
            "The LC path is cleaner and lower-scrutiny: it removes axial torsion by field-domain selection, not tuning.",
            "3571 should attack the parent branch selector and the two weak clauses: projector naturality and boundary/source-owner closure.",
            "ADOPTED",
            "status_3566",
        ),
        (
            "DEC3570_1_affine_fallback_kept",
            "keep the affine coefficient branch alive as a nonclaim fallback",
            "If the LC selector fails, the work must not hide torsion; it must fill Z_A,m_A^2,eta_A,K_A/c_A.",
            "3570 preserves the honest test path without pretending it is filled.",
            "ADOPTED",
            "axial_source_3569",
        ),
        (
            "DEC3570_2_coupling_interpretation",
            "the coupling hinge is now structural first, numeric second",
            "A missing c_A is not the only issue: the parent must first decide whether C_A is a field at all.",
            "This reframes the problem as branch selection plus explicit fallback coefficients.",
            "ADOPTED",
            "coeff_queue_3566",
        ),
        (
            "DEC3570_3_next_target",
            "try to derive the parent B_LC_selector",
            "That is the move that would convert the private C_A=0 certificate into the first serious local-GR closure.",
            "Next target is branch selector theorem or source-owner/projector bound.",
            "NEXT_TARGET_SELECTED",
            "signature_3566",
        ),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            "status": status,
            "source_path": str(source_paths[source_key]),
            "valid_for_claim": False,
        }
        for decision_id, decision, reason, consequence, status, source_key in specs
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "PARENT_AXIAL_SELECTOR_CONTRACT_DERIVED_PRIVATE_ZERO_OR_AFFINE_BOUND",
            "strongest_result": "epsilon_A_public=(1-B_LC_selector)*K_A/[a_A(1-eta_A)]*numerator_A, with exact zero inside the private LC branch and explicit source-ready affine fallback if the selector fails.",
            "still_missing": "public parent derivation of B_LC_selector; projector naturality; boundary/source-owner closure; or source-backed affine Z_A,m_A^2,eta_A,K_A/c_A rows",
            "public_claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3570_0",
            "target_doc": "3571-Y5-R2FR-parent-LC-branch-selector-theorem-or-source-owner-bound.md",
            "target_script": "scripts/Y5_R2FR_3571_parent_LC_branch_selector_theorem_or_source_owner_bound.py",
            "objective": "try to derive the parent-level B_LC_selector by quotient-visible action-domain exhaustion; if it fails, bound projector/boundary/source-owner leakage explicitly",
            "success_gate": "public parent selector for no independent affine connection, or source-backed bound rows for the remaining projector and boundary/source-owner leaks",
            "reason": "3570 shows axial torsion closes cleanly once the LC branch selector is parent-derived",
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_item": "parent_axial_selector_and_coefficient_contract",
            "status": "PRIVATE_ZERO_OR_EXPLICIT_AFFINE_BOUND_NONCLAIM",
            "selector_formula": "epsilon_A_public=(1-B_LC_selector)*epsilon_A_affine",
            "LC_result": "C_A absent and epsilon_A=0 if B_LC_selector=1",
            "affine_result": "epsilon_A_affine=K_A/[a_A(1-eta_A)]*numerator_A if B_LC_selector=0",
            "next_action": "derive B_LC_selector or bound projector/boundary leakage",
            "valid_for_claim": False,
        }
    ]


def validate(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    zero: list[dict[str, object]],
    selector: list[dict[str, object]],
    coefficients: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {key: path for key, path in outputs.items() if key != "validation"}
    validations.append(("VAL3570_0_sources_exist", all(path.exists() for path in source_paths.values()), "all required 3570 source paths exist"))
    needles = {
        "handoff_3569": "NEXT3569_0",
        "axial_derivation_3569": "AXST3569_7_verdict",
        "axial_source_3569": "AXSRC3569_10_bound_master",
        "validation_3569": "VAL3569_7_public_claim_blocked",
        "signature_3566": "SIG3566_10_total_signature",
        "variation_3566": "VAR3566_0_total_noGamma",
        "coeff_queue_3566": "P4C3566_1_axial_torsion",
        "status_3566": "parent branch-selector theorem",
        "source_signature_3497": "MPA3497_2_spin_connection",
        "variation_chain_3497": "VAR3497_4_projector_zero",
        "em_signature_3506": "GEN3506_5_scalar_gauge_kinetic_owner",
        "spin_p4_3565": "P4H3565_2_spin_owned_or_axial",
        "spin_theorem_3565": "STH3565_1_variable_absence_zero",
        "kspin_3567": "KSP3567_1_axial_torsion",
        "sector_gamma_3493": "Gamma",
        "sector_gamma_3565": "Gamma",
    }
    validations.append(("VAL3570_1_required_needles_found", all(source_paths[key].exists() and file_contains(source_paths[key], token) for key, token in needles.items()), "all selected selector/coefficient source needles found"))
    validations.append(("VAL3570_2_outputs_exist", all(path.exists() for path in pre_validation_outputs.values()), "all pre-validation 3570 output files written"))
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
    validations.append(("VAL3570_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    validations.append(("VAL3570_4_zero_certificate_present", any(row["certificate_id"] == "AZC3570_7_total" and "C_A=0" in str(row["formal_content"]) for row in zero), "parent axial zero certificate row present"))
    validations.append(("VAL3570_5_selector_formula_present", any(row["selector_id"] == "SEL3570_2_response_split" and "1-B_LC_selector" in str(row["contract"]) for row in selector), "selector response split formula present"))
    validations.append(("VAL3570_6_affine_coefficients_audited", {"Z_A", "m_A^2", "eta_A", "K_A", "c_A or xi_A"}.issubset({str(row["symbol"]) for row in coefficients}), "affine coefficient set audited"))
    validations.append(("VAL3570_7_bound_split_present", {"epsilon_A_public", "epsilon_A_affine", "epsilon_A_LC"}.issubset({str(row["symbol"]) for row in bounds}), "public/affine/LC bound split rows present"))
    validations.append(("VAL3570_8_public_claim_blocked", any(row["gate_id"] == "GATE3570_6_public_axial_local_GR" and row["status"] == "FAIL_CURRENT_PUBLIC_CLAIM" for row in gates), "public axial local-GR claim remains blocked"))
    validations.append(("VAL3570_9_next_selector_target_selected", any(row["decision_id"] == "DEC3570_3_next_target" for row in decisions), "next branch-selector target selected"))
    validations.append(("VAL3570_10_no_claim_flags", all(str(row["valid_for_claim"]).lower() == "false" for row in zero + selector + coefficients + bounds + gates + decisions), "all generated physics rows remain nonclaim"))
    generated_source_paths_exist = all(Path(str(row["source_path"])).exists() for row in zero + selector + coefficients + bounds + gates + decisions)
    validations.append(("VAL3570_11_generated_source_paths_exist", generated_source_paths_exist, "every generated row source_path exists"))
    formalization_touched = any(FORMALIZATION.rglob("*3570*")) if FORMALIZATION.exists() else False
    validations.append(("VAL3570_12_formalization_workbench_untouched", not formalization_touched, "no 3570 checkpoint output appears in formalization-workbench"))
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
    zero: list[dict[str, object]],
    selector: list[dict[str, object]],
    coefficients: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3570 - Parent axial coefficient signature or KA bound fill",
        "",
        "## Verdict",
        "3570 makes the axial coupling hinge explicit.  The clean route is not to guess a tiny torsion coupling.  It is to prove the parent selector `B_LC_selector=1`, meaning the local ordinary/source/readout action has no independent `Gamma_ind/omega_ind` slot.  In that branch `C_A` is absent and `epsilon_A=0` by field-domain descent.",
        "",
        "If that selector is not parent-derived, the fallback is not rhetoric: `epsilon_A_public=(1-B_LC_selector) * K_A/[a_A(1-eta_A)] * (||J5_A||+||B_A||+||P_A||+||N_A||+||R_A_mix||)`.  The affine coefficients `Z_A`, `m_A^2`, `eta_A`, `K_A`, and `c_A/xi_A` remain unsourced, so no public axial/local-GR claim is made.",
        "",
        "## Generated outputs",
    ]
    for output_id, path in outputs.items():
        lines.append(f"- `{output_id}`: `{path}`")
    lines.extend(["", "## Parent axial zero certificate"])
    for row in zero:
        lines.append(f"- `{row['certificate_id']}`: {row['clause']} -> {row['effect_on_axial_channel']} ({row['status']})")
    lines.extend(["", "## Selector contract"])
    for row in selector:
        lines.append(f"- `{row['selector_id']}` `{row['symbol']}`: {row['contract']} ({row['status']})")
    lines.extend(["", "## Coefficient attempt"])
    for row in coefficients:
        lines.append(f"- `{row['coefficient_id']}` `{row['symbol']}` [{row['branch']}]: {row['finding']} ({row['status']})")
    lines.extend(["", "## Bound split"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}` `{row['symbol']}`: {row['formula']} ({row['interpretation']})")
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
    zero = zero_certificate_rows(source_paths)
    selector = selector_contract_rows(source_paths)
    coefficients = coefficient_attempt_rows(source_paths)
    bounds = bound_rows(source_paths)
    gates = activation_rows(source_paths)
    decisions = decision_rows(source_paths)
    status = status_rows()
    next_target = next_target_rows()
    canonical = canonical_status_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3570_SOURCE_REGISTER.csv",
        "parent_axial_zero_certificate": RESIDUALS / "P8_Y5_R2FR_3570_PARENT_AXIAL_ZERO_CERTIFICATE.csv",
        "selector_contract": RESIDUALS / "P8_Y5_R2FR_3570_AXIAL_BRANCH_SELECTOR_CONTRACT.csv",
        "coefficient_attempt": RESIDUALS / "P8_Y5_R2FR_3570_AFFINE_COEFFICIENT_FILL_ATTEMPT.csv",
        "bound_rows": RESIDUALS / "P8_Y5_R2FR_3570_KA_CA_BOUND_ROWS.csv",
        "activation_gates": RESIDUALS / "P8_Y5_R2FR_3570_ACTIVATION_GATES.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3570_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3570_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3570_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_axial_parent_coefficient_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3570_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], register)
    write_csv(outputs["parent_axial_zero_certificate"], zero)
    write_csv(outputs["selector_contract"], selector)
    write_csv(outputs["coefficient_attempt"], coefficients)
    write_csv(outputs["bound_rows"], bounds)
    write_csv(outputs["activation_gates"], gates)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], next_target)
    write_csv(outputs["canonical_status"], canonical)
    validation = validate(source_paths, outputs, zero, selector, coefficients, bounds, gates, decisions)
    write_csv(outputs["validation"], validation)
    write_doc(outputs, zero, selector, coefficients, bounds, gates, decisions, status, validation, next_target)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"3570 validation failed: {failed}")
    print(f"wrote {DOC}")
    for output_id, path in outputs.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
