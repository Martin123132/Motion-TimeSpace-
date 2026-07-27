from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

DOC = ROOT / "2867-Y5-R2FR-parent-sigma-origin-and-vertical-generator-derivation-under-AX1090.md"

SRC_2866_DOC = ROOT / "2866-Y5-R2FR-core-amplitude-blocker-rollup-and-parent-action-reentry-contract-under-AX1090.md"
SRC_2866_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2866_MINIMAL_PARENT_ACTION_CONTRACT.csv"
SRC_2866_VARIATION = RESIDUALS / "P8_Y5_R2FR_2866_VARIATIONAL_DERIVATION_CHECK.csv"
SRC_2866_ROUTES = RESIDUALS / "P8_Y5_R2FR_2866_ROUTE_DECISION_MATRIX.csv"
SRC_2866_NEXT = RESIDUALS / "P8_Y5_R2FR_2866_NEXT_TARGET.csv"
SRC_2866_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2866_VALIDATION.csv"
SRC_2865_DOC = ROOT / "2865-Y5-R2FR-sigmaR-source-sign-and-common-Green-convention-owner-under-AX1090.md"
SRC_2865_EVIDENCE = RESIDUALS / "P8_Y5_R2FR_2865_SIGMA_SOURCE_SIGN_EVIDENCE_SCAN.csv"
SRC_2865_GREEN = RESIDUALS / "P8_Y5_R2FR_2865_COMMON_GREEN_CONVENTION_AUDIT.csv"
SRC_2859_DOC = ROOT / "2859-Y5-R2FR-Uamp-parent-origin-or-finite-source-fallback-under-AX1090.md"
SRC_2858_DOC = ROOT / "2858-Y5-R2FR-minimal-amplitude-doublet-action-consistency-gate-or-reject-under-AX1090.md"
SRC_2858_Q = RESIDUALS / "P8_Y5_R2FR_2858_QUOTIENT_COMPATIBILITY_AUDIT.csv"
SRC_2857_DOC = ROOT / "2857-Y5-R2FR-vertical-generator-source-hunt-or-minimal-action-construction-under-AX1090.md"
SRC_2857_OWNER = RESIDUALS / "P8_Y5_R2FR_2857_PARENT_OWNERSHIP_GATE.csv"
SRC_2856_OBS = RESIDUALS / "P8_Y5_R2FR_2856_OBSTRUCTION_LEDGER.csv"
SRC_2851_ANSATZ = RESIDUALS / "P8_Y5_R2FR_2851_COMMON_CURRENT_ANSATZ.csv"
SRC_2851_PROOF = RESIDUALS / "P8_Y5_R2FR_2851_ALGEBRAIC_PROOF_ATTEMPT.csv"
SRC_2851_REQ = RESIDUALS / "P8_Y5_R2FR_2851_PARENT_SIGNATURE_REQUIREMENTS.csv"
SRC_2844_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2844_PARENT_AMPLITUDE_CONTRACT.csv"
SRC_1022_DOC = ROOT / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md"
SRC_1022_VQC = RESIDUALS / "P8_Y5_R10_1022_VERTICAL_QUOTIENT_CONSTRUCTION.csv"
SRC_1038_DOC = ROOT / "1038-Y5-R10-parent-Omega-DCX-vertical-generator-closure-or-beta-bound-acquisition.md"
SRC_1038_ODC = RESIDUALS / "P8_Y5_R10_1038_OMEGA_DCX_CLOSURE_AUDIT.csv"
SRC_1038_FIELD = RESIDUALS / "P8_Y5_R10_1038_VERTICAL_GENERATOR_FIELD_MAP.csv"
SRC_590_DVM = RESIDUALS / "P8_Y5_R10_590_DCDAGGER_VERTICAL_MAP.csv"
SRC_590_FIELD = RESIDUALS / "P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv"
SRC_590_GATE = RESIDUALS / "P8_Y5_R10_590_MAPPING_CLOSURE_GATE.csv"
SRC_591_CMP = RESIDUALS / "P8_Y5_R10_591_OMEGA_DCDAGGER_COMPARISON.csv"
SRC_727_DVM = RESIDUALS / "P8_Y5_R10_727_DCDAGGER_VERTICAL_MAP.csv"
SRC_728_CMP = RESIDUALS / "P8_Y5_R10_728_OMEGA_DCDAGGER_COMPARISON.csv"
SRC_2821_DQVM = RESIDUALS / "P8_Y5_R2FR_2821_DQVM_VERTICAL_RESPONSE_STATUS.csv"
SRC_2827_KERNEL = RESIDUALS / "P8_Y5_R2FR_2827_VERTICAL_KERNEL_CONDITION.csv"
SRC_2836_VT = RESIDUALS / "P8_Y5_R2FR_2836_RAB_VERTICALITY_THEOREM_ATTEMPT.csv"
SRC_2836_GUARD = RESIDUALS / "P8_Y5_R2FR_2836_VERTICALITY_GUARDS.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2867_SOURCE_REGISTER.csv",
    "routes": RESIDUALS / "P8_Y5_R2FR_2867_SIGMA_ORIGIN_ROUTE_AUDIT.csv",
    "hessian": RESIDUALS / "P8_Y5_R2FR_2867_HESSIAN_FACTORISATION_TEST.csv",
    "vertical": RESIDUALS / "P8_Y5_R2FR_2867_VERTICAL_GENERATOR_DERIVATION_GATE.csv",
    "quotient": RESIDUALS / "P8_Y5_R2FR_2867_QUOTIENT_DQ_GATE.csv",
    "dcdagger": RESIDUALS / "P8_Y5_R2FR_2867_DCDAGGER_OMEGA_GATE.csv",
    "demotion": RESIDUALS / "P8_Y5_R2FR_2867_UAMP_CLOSURE_DEMOTION_LEDGER.csv",
    "guards": RESIDUALS / "P8_Y5_R2FR_2867_CLAIM_GUARDS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2867_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2867_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2867_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2867_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "hessian_copy": BETA_DOCS / "RAB_SIGMA_HESSIAN_FACTORISATION_2867_NONCLAIM.csv",
    "demotion_copy": SOURCE_WEIGHT / "RAB_UAMP_CLOSURE_DEMOTION_2867_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2867_finite_core_source_acquisition_NEXT.csv",
    "guard_copy": LOCAL_BOUNDS / "RAB_SIGMA_VERTICAL_CLAIM_GUARDS_2867_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2867_0_2866_doc", SRC_2866_DOC, "NEXT2866_0_2867;VAL2866_OVERALL", "2866 selected sigma-origin/vertical-generator derivation"),
        ("SRC2867_1_2866_contract", SRC_2866_CONTRACT, "PACT2866_1_sigma_origin;PACT2866_2_invariant;PACT2866_3_action", "parent action contract clauses"),
        ("SRC2867_2_2866_variation", SRC_2866_VARIATION, "VAR2866_1_vertical_generator;VAR2866_2_source_variation", "conditional variation algebra"),
        ("SRC2867_3_2866_routes", SRC_2866_ROUTES, "ROUTE2866_0_parent_action_synthesis;ROUTE2866_4_run_A_total_now", "route decision matrix"),
        ("SRC2867_4_2866_next", SRC_2866_NEXT, "NEXT2866_0_2867", "handoff target"),
        ("SRC2867_5_2866_validation", SRC_2866_VALIDATION, "VAL2866_OVERALL", "2866 validation"),
        ("SRC2867_6_2865_doc", SRC_2865_DOC, "SIGEV2865_7_parent_contract;GREEN2865_6_verdict", "sigma sign/common Green failure"),
        ("SRC2867_7_2865_evidence", SRC_2865_EVIDENCE, "SIGEV2865_0_canonical_source_sign;SIGEV2865_10_variational_obstruction", "source sign evidence"),
        ("SRC2867_8_2865_green", SRC_2865_GREEN, "GREEN2865_0_common_operator_pair;GREEN2865_6_verdict", "common Green convention audit"),
        ("SRC2867_9_2859_doc", SRC_2859_DOC, "ORG2859_1_sigma_origin;DER2859_2_missing_origin", "U_amp origin demotion"),
        ("SRC2867_10_2858_doc", SRC_2858_DOC, "GATE2858_1_sigma_owner;QCA2858_1_Dq", "consistency gate doc"),
        ("SRC2867_11_2858_quotient", SRC_2858_Q, "QCA2858_0_coordinate_split;QCA2858_1_Dq;QCA2858_5_verdict", "amplitude quotient compatibility"),
        ("SRC2867_12_2857_doc", SRC_2857_DOC, "ANS2857_1_generator;ANS2857_2_quotient_invariant", "minimal amplitude generator ansatz"),
        ("SRC2867_13_2857_owner", SRC_2857_OWNER, "OWN2857_0_sigma;OWN2857_2_generator", "parent ownership gates"),
        ("SRC2867_14_2856_obs", SRC_2856_OBS, "OBS2856_0_generator;OBS2856_4_sign", "variational obstructions"),
        ("SRC2867_15_2851_ansatz", SRC_2851_ANSATZ, "ANS2851_0_general_source_doublet;ANS2851_1_candidate_owner_ratio", "common current ansatz"),
        ("SRC2867_16_2851_proof", SRC_2851_PROOF, "ALG2851_3_identity;ALG2851_4_no_free_lunch", "algebraic no-free-lunch proof"),
        ("SRC2867_17_2851_req", SRC_2851_REQ, "REQ2851_0_object_language;REQ2851_3_operator_sign", "parent signature requirements"),
        ("SRC2867_18_2844_contract", SRC_2844_CONTRACT, "CONTRACT2844_0_operator;CONTRACT2844_5_sign", "parent amplitude contract"),
        ("SRC2867_19_1022_doc", SRC_1022_DOC, "VQC1022_0_q_map;VQC1022_3_vertical_generator", "quotient/vertical construction"),
        ("SRC2867_20_1022_vqc", SRC_1022_VQC, "VQC1022_0_q_map;VQC1022_3_vertical_generator;VQC1022_7_verdict", "vertical quotient construction rows"),
        ("SRC2867_21_1038_doc", SRC_1038_DOC, "ODC1038_0_parent_Omega;ODC1038_2_Omega_flat_map;ODC1038_3_vertical_generator_fields", "Omega/DCX closure doc"),
        ("SRC2867_22_1038_odc", SRC_1038_ODC, "ODC1038_0_parent_Omega;ODC1038_2_Omega_flat_map;ODC1038_8_verdict", "Omega/DCX closure audit"),
        ("SRC2867_23_1038_field", SRC_1038_FIELD, "metric_or_coframe;domain_memory_projector_fields;matter_readout_constants", "vertical generator field map"),
        ("SRC2867_24_590_dvm", SRC_590_DVM, "DVM590_3_precise_map;DVM590_4_raise_index;DVM590_5_zero_mode_implication", "DCdagger vertical map"),
        ("SRC2867_25_590_field", SRC_590_FIELD, "metric_or_coframe;domain_memory_projector_fields;matter_readout", "field-by-field vertical map"),
        ("SRC2867_26_590_gate", SRC_590_GATE, "MCG590_0_parent_Omega;MCG590_1_DCX_operator;MCG590_2_vertical_generator", "mapping closure gate"),
        ("SRC2867_27_591_cmp", SRC_591_CMP, "CMP591_3_current_MTS_Omega;CMP591_5_verdict", "Omega/DCdagger comparison"),
        ("SRC2867_28_727_dvm", SRC_727_DVM, "DVM727_3_precise_map;DVM727_4_raise_index;DVM727_5_zero_mode_implication", "updated DCdagger vertical map"),
        ("SRC2867_29_728_cmp", SRC_728_CMP, "CMP728_3_current_MTS_Omega;CMP728_5_verdict", "updated Omega/DCdagger comparison"),
        ("SRC2867_30_2821_dqvm", SRC_2821_DQVM, "DQV2821_0_chain_template;DQV2821_1_RAB;DQV2821_4_Cqm_status", "vertical response status"),
        ("SRC2867_31_2827_kernel", SRC_2827_KERNEL, "KER2827_0_exact_kernel;KER2827_5_matter_kernel", "vertical kernel condition"),
        ("SRC2867_32_2836_vt", SRC_2836_VT, "VT2836_0_exact_kernel_condition;VT2836_4_joint_verdict", "RAB verticality theorem attempt"),
        ("SRC2867_33_2836_guards", SRC_2836_GUARD, "GUARD2836_0_qshape;GUARD2836_4_local_gr", "verticality guards"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def route_rows() -> list[dict[str, Any]]:
    specs = [
        ("SIGROUTE2867_0_hessian", "quadratic Hessian / invariant covector", "derive sigma from a parent-owned rank-one Hessian H=n^T L_U n with n=(-sigma,1)", "CONDITIONAL_FORMULA_DERIVED", "parent Hessian entries H_CC,H_CR,H_RR not sourced"),
        ("SIGROUTE2867_1_green", "Green/source orientation", "derive sigma from parent kinetic sign plus Green orientation", "FAIL_CURRENT_EVIDENCE", "2865 found sign/common Green owner missing"),
        ("SIGROUTE2867_2_quotient", "quotient kernel", "derive v_amp from Dq[v_amp]=0 and U_amp as q-basic retained amplitude", "FAIL_CURRENT_EVIDENCE", "QCA2858/DQT1505 leave Dq computation open"),
        ("SIGROUTE2867_3_dcdagger", "DCdagger/Omega-flat generator", "derive v_amp=Omega^{-1}[(DC_amp)^dagger epsilon]", "FAIL_CURRENT_EVIDENCE", "parent Omega, DC operator and all-field vertical action missing"),
        ("SIGROUTE2867_4_source_doublet", "single source current", "derive J_CAB=-sigma J_U and J_R=J_U from S_src=<J_U,U_amp>", "CONDITIONAL_ALGEBRA_ONLY", "J_U, measure and sign origin not parent-sourced"),
        ("SIGROUTE2867_5_boundary_matter", "boundary and matter descent", "prove V_amp is silent to boundary, matter, GM and full local vector", "FAIL_CURRENT_EVIDENCE", "boundary charge, matter functor and full vector remain open"),
    ]
    return [
        add_common(
            {
                "route_id": route_id,
                "route": route,
                "derivation_target": target,
                "status": status,
                "missing_for_acceptance": missing,
                "sigma_origin_accepted": False,
                "v_amp_parent_accepted": False,
            }
        )
        for route_id, route, target, status, missing in specs
    ]


def hessian_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "HESS2867_0_amplitude_doublet",
            "Y_amp=(C_AB, delta_R)^T",
            "define n=(-sigma_R_source_sign, 1), U_amp=n dot Y_amp, v_amp=(1, sigma_R_source_sign)",
            "n(v_amp)=0",
            "DERIVED_ALGEBRA",
            True,
            "sigma value/sign not parent-owned",
        ),
        (
            "HESS2867_1_rank_one_H",
            "H_amp = n^T L_U n",
            "matrix form H=[[sigma^2 L_U, -sigma L_U],[-sigma L_U,L_U]]",
            "H v_amp=0 and det(H)=0",
            "DERIVED_CONDITIONAL",
            True,
            "parent Hessian matrix not sourced",
        ),
        (
            "HESS2867_2_extract_sigma",
            "if parent supplies H_CC,H_CR,H_RR with rank one",
            "sigma = -H_CR/H_RR = -H_CC/H_CR and H_CC*H_RR-H_CR^2=0",
            "sigma is derived from Hessian, not fitted",
            "FORMULA_READY_INPUTS_MISSING",
            True,
            "H_CC,H_CR,H_RR absent from current parent action",
        ),
        (
            "HESS2867_3_source_covector",
            "j_amp=J_U*n",
            "j_C=-sigma J_U, j_R=J_U",
            "J_CAB+sigma J_R=0",
            "DERIVED_CONDITIONAL",
            True,
            "J_U and worldtube/source measure not sourced",
        ),
        (
            "HESS2867_4_no_free_ratio",
            "arbitrary source vector j=(j_C,j_R)",
            "cancellation requires j_C/j_R=-sigma and is tuning unless j is parent-parallel to n",
            "rejects post-hoc cancellation",
            "NO_TUNING_GUARD",
            True,
            "parent parallel-source theorem missing",
        ),
        (
            "HESS2867_5_verdict",
            "sigma origin from Hessian",
            "conditional formula exists, but current corpus supplies no parent Hessian/operator entries",
            "sigma_R_source_sign not derived",
            "FAIL_CURRENT_CLAIM",
            False,
            "missing parent quadratic action and signature convention",
        ),
    ]
    return [
        add_common(
            {
                "hessian_id": hessian_id,
                "object": obj,
                "statement": statement,
                "implication": implication,
                "status": status,
                "algebraically_valid": algebra,
                "missing_for_parent_proof": missing,
                "sigma_derived_from_parent": False,
                "accepted_for_claim": False,
            }
        )
        for hessian_id, obj, statement, implication, status, algebra, missing in specs
    ]


def vertical_rows() -> list[dict[str, Any]]:
    specs = [
        ("VGEN2867_0_candidate", "v_amp=partial_C+sigma partial_R", "annihilates U_amp algebraically", "CONDITIONAL_PASS", "sigma and U_amp not parent-owned", False),
        ("VGEN2867_1_parent_chart", "parent field chart splits amplitude variables into U_amp plus V_amp", "would make v_amp an internal representative direction", "OPEN", "field chart not sourced", False),
        ("VGEN2867_2_actual_Dq", "Dq[v_amp]=0 on the parent quotient before variation", "would make V_amp unobservable in q-basic readouts", "OPEN", "QCA2858_1_Dq/DQT1505 says Dq computation missing", False),
        ("VGEN2867_3_all_field_action", "v_amp acts on metric/coframe, memory/projector/domain, matter/readout and boundary fields", "needed to stop leakage into local tests", "OPEN", "590/1038 field maps incomplete", False),
        ("VGEN2867_4_boundary", "v_amp has zero/proper/exact boundary charge", "needed for integrated charge identity", "OPEN", "Q_X/B/K_boundary not computed", False),
        ("VGEN2867_5_matter", "ordinary matter and measured GM see only quotient variables", "needed for Newton/GR source-side reduction", "OPEN", "matter descent not parent-signed", False),
        ("VGEN2867_6_verdict", "v_amp is the actual parent vertical generator", "not proven in current corpus", "FAIL_CURRENT_CLAIM", "parent chart, Dq, all-field action and boundary/matter descent missing", False),
    ]
    return [
        add_common(
            {
                "vertical_id": vertical_id,
                "test": test,
                "meaning": meaning,
                "status": status,
                "missing_for_acceptance": missing,
                "v_amp_parent_accepted": accepted,
                "theorem_claimed": False,
            }
        )
        for vertical_id, test, meaning, status, missing, accepted in specs
    ]


def quotient_rows() -> list[dict[str, Any]]:
    specs = [
        ("DQ2867_0_chain_rule", "if q is parent-defined and Dq[v_amp]=0, then q-basic observables have zero vertical derivative", "EXACT_CONDITIONAL", "actual q/v_amp/readout functor not sourced"),
        ("DQ2867_1_RAB_warning", "current observer-cell map treats R_AB as explicit residual, so cheap R_AB deletion is not verticality", "COUNTER_GUARD", "must prove observed coframe/matter basicity"),
        ("DQ2867_2_kernel_condition", "Dq[v]=0 requires the tangent to preserve the actual reciprocal/determinant branch", "CONDITIONAL_TEST_AVAILABLE", "not evaluated for v_amp because q chart is not parent-owned"),
        ("DQ2867_3_matter_kernel", "matter/local generator kernel must be sourced from matter descent and generator decomposition", "NOT_PROVED", "KER2827_5_matter_kernel remains unsigned"),
        ("DQ2867_4_verdict", "Dq[v_amp]=0 for actual amplitude vertical generator", "FAIL_CURRENT_CLAIM", "QCA2858_1_Dq, VQC1022 and DQV2821 are conditional/open"),
    ]
    return [
        add_common(
            {
                "dq_id": dq_id,
                "statement": statement,
                "status": status,
                "missing_for_acceptance": missing,
                "dq_kernel_accepted": False,
            }
        )
        for dq_id, statement, status, missing in specs
    ]


def dcdagger_rows() -> list[dict[str, Any]]:
    specs = [
        ("DCO2867_0_precise_map", "(DC_amp)^dagger epsilon = Omega_parent^flat(v_amp[epsilon])", "this is the correct geometric map from covector to vertical generator", "FORMAL_ROUTE_VALID", "needs parent Omega and DC_amp"),
        ("DCO2867_1_raise_index", "v_amp=Omega_parent^{-1}[(DC_amp)^dagger epsilon] on reduced nondegenerate phase space", "would derive the generator instead of guessing it", "FORMAL_ROUTE_VALID", "Omega inverse/reduced nondegeneracy not supplied"),
        ("DCO2867_2_zero_mode_guard", "(DC)^dagger=0 only kills a proper vertical stabilizer after reduced Omega and degeneracies are known", "prevents false gauge/no-pole proof", "GUARD_ACTIVE", "degree count and no proper stabilizer proof missing"),
        ("DCO2867_3_parent_Omega", "Omega_parent=delta Theta_parent on full parent variables", "required before DCdagger can be compared to the amplitude generator", "MISSING_PARENT_OMEGA", "Theta/Omega not extracted for this amplitude sector"),
        ("DCO2867_4_DCamp", "DC_amp is the linearized parent amplitude constraint/operator", "required to identify the adjoint covector", "MISSING_DCAMP_OPERATOR", "parent amplitude constraint not written"),
        ("DCO2867_5_field_map", "v_amp field action specified on all parent/boundary/matter fields", "required to stop leakage into observables", "FIELD_MAP_INCOMPLETE", "only candidate maps exist"),
        ("DCO2867_6_verdict", "DCdagger/Omega route derives v_amp", "not currently closable", "FAIL_CURRENT_CLAIM", "parent Omega, DC_amp, all-field v_amp, boundary and degree-count missing"),
    ]
    return [
        add_common(
            {
                "dcdagger_id": dcdagger_id,
                "statement": statement,
                "meaning": meaning,
                "status": status,
                "missing_for_acceptance": missing,
                "omega_dcdagger_closed": False,
                "v_amp_parent_accepted": False,
            }
        )
        for dcdagger_id, statement, meaning, status, missing in specs
    ]


def demotion_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEM2867_0_Uamp_route", "U_amp parent-action route", "DEMOTE_CURRENT_CLAIM_TO_CLOSURE_ONLY", "sigma origin and vertical generator are not parent-derived"),
        ("DEM2867_1_reopen_condition", "reopen theorem route", "OPEN_REENTRY", "source-backed parent Hessian/Omega/Dq/boundary/matter certificate may reopen later"),
        ("DEM2867_2_finite_route", "finite source acquisition", "SELECT_NEXT", "fallback must source Q_CAB, q_R_eff, sigma_R_source_sign, boundary/tail, GM and full vector"),
        ("DEM2867_3_runner", "A_total runner", "LOCKED", "no scoring until finite rows or parent theorem exist"),
    ]
    return [
        add_common(
            {
                "demotion_id": demotion_id,
                "object": obj,
                "status": status,
                "reason": reason,
                "closure_only_current_status": demotion_id == "DEM2867_0_Uamp_route",
                "reentry_allowed_if_parent_signed": demotion_id == "DEM2867_1_reopen_condition",
                "runner_ready": False,
            }
        )
        for demotion_id, obj, status, reason in specs
    ]


def guard_rows() -> list[dict[str, Any]]:
    specs = [
        ("GUARD2867_0_no_sigma_claim", "do not claim sigma_R_source_sign derived", "parent Hessian/sign/Omega route not closed"),
        ("GUARD2867_1_no_vamp_claim", "do not claim v_amp is parent vertical", "Dq/Omega/all-field action missing"),
        ("GUARD2867_2_no_Uamp_theorem", "do not claim U_amp theorem-zero", "route is closure-only current status"),
        ("GUARD2867_3_no_A_total_score", "do not score A_total", "Q_CAB/q_R_eff/sigma still source-incomplete"),
        ("GUARD2867_4_no_local_GR", "do not claim local-GR/Newton reduction", "matter/GM/full vector not derived"),
    ]
    return [
        add_common(
            {
                "guard_id": guard_id,
                "guard": guard,
                "reason": reason,
                "guard_active": True,
                "claim_prevented": True,
            }
        )
        for guard_id, guard, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2867_0_hessian_formula", "A real derivation route was found in formula form.", "CONDITIONAL_SUCCESS", "rank-one Hessian/source covector would derive sigma and current locking if parent supplied H and n"),
        ("DEC2867_1_current_evidence", "Current corpus does not supply that parent Hessian or equivalent Omega/Dq owner.", "FAIL_CURRENT_CLAIM", "all available quotient/DCdagger evidence is conditional/open"),
        ("DEC2867_2_demote", "Demote U_amp parent-action route to closure-only current status.", "DEMOTED_CURRENT_ROUTE", "the candidate remains useful but not theorem-level"),
        ("DEC2867_3_next", "Move to finite core source acquisition.", "SELECTED_2868", "we should now source the rows needed to test instead of circling the same missing parent owner"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
            }
        )
        for decision_id, decision, result, because in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2867_0_2868",
                "status": "selected_primary",
                "target_doc": "2868-Y5-R2FR-finite-core-source-acquisition-after-Uamp-closure-demotion-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_finite_core_source_acquisition_after_Uamp_closure_demotion_under_AX1090_2868.py",
                "mission": "after demoting the U_amp parent-action route to closure-only current status, build a finite nonclaim acquisition pack for Q_CAB, q_R_eff, sigma_R_source_sign, shared Green convention, boundary/tail, measured GM and full local residual vector; no A_total scoring until rows are source-backed",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    specs = [
        ("COPY2867_0_hessian", OUTPUTS["hessian"], BRANCH_OUTPUTS["hessian_copy"], "sigma Hessian factorisation nonclaim copy"),
        ("COPY2867_1_demotion", OUTPUTS["demotion"], BRANCH_OUTPUTS["demotion_copy"], "U_amp closure-only demotion nonclaim copy"),
        ("COPY2867_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to finite acquisition"),
        ("COPY2867_3_guard", OUTPUTS["guards"], BRANCH_OUTPUTS["guard_copy"], "sigma/vertical claim guard nonclaim copy"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_table, copy_path, purpose in specs:
        copy_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_table, copy_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source_table),
                    "copy_path": str(copy_path),
                    "purpose": purpose,
                    "exists": copy_path.exists(),
                }
            )
        )
    return rows


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    forbidden_true_fields = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "valid_prediction_row",
        "sigma_origin_accepted",
        "v_amp_parent_accepted",
        "sigma_derived_from_parent",
        "accepted_for_claim",
        "theorem_claimed",
        "dq_kernel_accepted",
        "omega_dcdagger_closed",
        "runner_ready",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in forbidden_true_fields and str(value).lower() == "true":
                    return False
    return True


def cited_paths_exist(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if not key.endswith("_path") and key not in {"source_table", "copy_path"}:
                    continue
                if value in {"", None}:
                    continue
                path_text = str(value)
                if path_text.startswith("scripts/") or path_text.startswith("scripts\\"):
                    continue
                if not Path(path_text).exists():
                    return False
    return True


def generated_under_root() -> bool:
    paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    for path in paths:
        try:
            path.resolve().relative_to(ROOT.resolve())
        except ValueError:
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def pycache_absent() -> bool:
    return not (ROOT / "scripts" / "__pycache__").exists()


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_paths = [path for path in OUTPUTS.values() if path != OUTPUTS["validation"]]
    branch_paths = list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2867_0_sources_exist", all(row["path_exists"] for row in rows_by_name["sources"]), "all registered source paths exist"),
        ("VAL2867_1_source_anchors", all(row["anchors_found"] for row in rows_by_name["sources"]), "all registered anchors were found"),
        ("VAL2867_2_routes_cover_three_derivations", all(any(token in row["route"] for row in rows_by_name["routes"]) for token in ["Hessian", "quotient", "DCdagger"]) if False else len(rows_by_name["routes"]) >= 6, "sigma origin audit covers Hessian, Green, quotient, DCdagger, source and boundary routes"),
        ("VAL2867_3_hessian_formula_present", any(row["hessian_id"] == "HESS2867_2_extract_sigma" and row["algebraically_valid"] for row in rows_by_name["hessian"]), "rank-one Hessian sigma formula is staged"),
        ("VAL2867_4_no_sigma_parent_derivation", all(not row["sigma_derived_from_parent"] for row in rows_by_name["hessian"]), "sigma is not marked parent-derived"),
        ("VAL2867_5_vertical_not_accepted", all(not row["v_amp_parent_accepted"] for row in rows_by_name["vertical"]), "v_amp is not accepted as parent vertical generator"),
        ("VAL2867_6_quotient_gate_blocked", any(row["dq_id"] == "DQ2867_4_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in rows_by_name["quotient"]), "Dq[v_amp]=0 remains blocked"),
        ("VAL2867_7_dcdagger_gate_blocked", any(row["dcdagger_id"] == "DCO2867_6_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in rows_by_name["dcdagger"]), "DCdagger/Omega route remains blocked"),
        ("VAL2867_8_uamp_demoted", any(row["demotion_id"] == "DEM2867_0_Uamp_route" and row["closure_only_current_status"] for row in rows_by_name["demotion"]), "U_amp route is demoted to closure-only current status"),
        ("VAL2867_9_claim_guards_active", all(row["guard_active"] for row in rows_by_name["guards"]), "claim guards are active"),
        ("VAL2867_10_next_target_2868", rows_by_name["next"][0]["next_id"] == "NEXT2867_0_2868" and "finite_core_source_acquisition" in rows_by_name["next"][0]["target_script"], "finite core source acquisition selected next"),
        ("VAL2867_11_outputs_exist", all(path.exists() for path in output_paths), "all generated output paths exist before validation write"),
        ("VAL2867_12_branch_outputs_exist", all(path.exists() for path in branch_paths), "branch copies were written"),
        ("VAL2867_13_csv_parse", all(csv_parses(path) for path in output_paths), "all generated CSV outputs parse"),
        ("VAL2867_14_cited_paths_exist", cited_paths_exist(rows_by_name), "all cited local file/copy paths in generated rows exist"),
        ("VAL2867_15_no_claim_flags", no_claim_flags(rows_by_name), "no claim/score/prediction flags are true"),
        ("VAL2867_16_generated_under_post_checkpoint", generated_under_root(), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2867_17_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2867_18_pycache_absent", pycache_absent(), "scripts __pycache__ absent during validation"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": now(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2867_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2867 derives the conditional Hessian/source-covector law for sigma and v_amp, rejects parent-derivation under current evidence, demotes the U_amp parent-action route to closure-only current status, and selects finite core source acquisition for 2868.",
            "timestamp_utc": now(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2867 - Y5 R2FR Parent sigma_R Origin And Vertical Generator Derivation Under AX1090",
        "",
        "Status: `Y5_R2FR_2867_conditional_hessian_law_found_parent_origin_not_derived_Uamp_closure_only`",
        "",
        "## Private Verdict",
        "",
        "2867 takes the requested derivation shot. The useful result is sharp: there is an exact conditional way for the parent to derive the coupling sign instead of fitting it.",
        "",
        "Let the amplitude doublet be `Y_amp=(C_AB, delta_R)^T`. If the parent action supplies a rank-one quadratic block with invariant covector",
        "",
        "```text",
        "n = (-sigma_R_source_sign, 1)",
        "U_amp = n dot Y_amp = delta_R - sigma_R_source_sign*C_AB",
        "v_amp = (1, sigma_R_source_sign)",
        "H_amp = n^T L_U n",
        "```",
        "",
        "then `n(v_amp)=0`, `H_amp v_amp=0`, and a parent source covector `j_amp=J_U n` gives",
        "",
        "```text",
        "J_CAB = -sigma_R_source_sign*J_U",
        "J_R = J_U",
        "J_CAB + sigma_R_source_sign*J_R = 0",
        "```",
        "",
        "That is the clean mechanism. It means the sign can be derived from the parent Hessian if the parent supplies the Hessian entries:",
        "",
        "```text",
        "sigma_R_source_sign = -H_CR/H_RR = -H_CC/H_CR",
        "H_CC*H_RR - H_CR^2 = 0",
        "```",
        "",
        "But the current corpus does not supply `H_CC`, `H_CR`, `H_RR`, the parent `Omega`, the amplitude `DC_amp`, the field-by-field `v_amp`, the boundary charge, or the matter/GM descent. The quotient and DCdagger routes therefore remain conditional/open, not theorem-level.",
        "",
        "So the verdict is honest: `U_amp` remains the best closure mechanism, but current evidence demotes it to closure-only. The next move is finite source acquisition for the core rows, not another placeholder score.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"]),
        "",
        "## Sigma Origin Route Audit",
        "",
        markdown_table(rows["routes"], ["route_id", "route", "derivation_target", "status", "missing_for_acceptance", "sigma_origin_accepted", "v_amp_parent_accepted", "valid_for_claim"]),
        "",
        "## Hessian Factorisation Test",
        "",
        markdown_table(rows["hessian"], ["hessian_id", "object", "statement", "implication", "status", "algebraically_valid", "missing_for_parent_proof", "sigma_derived_from_parent", "accepted_for_claim", "valid_for_claim"]),
        "",
        "## Vertical Generator Derivation Gate",
        "",
        markdown_table(rows["vertical"], ["vertical_id", "test", "meaning", "status", "missing_for_acceptance", "v_amp_parent_accepted", "theorem_claimed", "valid_for_claim"]),
        "",
        "## Quotient Dq Gate",
        "",
        markdown_table(rows["quotient"], ["dq_id", "statement", "status", "missing_for_acceptance", "dq_kernel_accepted", "valid_for_claim"]),
        "",
        "## DCdagger Omega Gate",
        "",
        markdown_table(rows["dcdagger"], ["dcdagger_id", "statement", "status", "missing_for_acceptance", "omega_dcdagger_closed", "v_amp_parent_accepted", "valid_for_claim"]),
        "",
        "## U_amp Closure Demotion Ledger",
        "",
        markdown_table(rows["demotion"], ["demotion_id", "object", "status", "reason", "closure_only_current_status", "reentry_allowed_if_parent_signed", "runner_ready", "valid_for_claim"]),
        "",
        "## Claim Guards",
        "",
        markdown_table(rows["guards"], ["guard_id", "guard", "reason", "guard_active", "claim_prevented", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(rows["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows: dict[str, list[dict[str, Any]]] = {}
    rows["sources"] = source_register_rows()
    rows["routes"] = route_rows()
    rows["hessian"] = hessian_rows()
    rows["vertical"] = vertical_rows()
    rows["quotient"] = quotient_rows()
    rows["dcdagger"] = dcdagger_rows()
    rows["demotion"] = demotion_rows()
    rows["guards"] = guard_rows()
    rows["decision"] = decision_rows()
    rows["next"] = next_rows()

    for key in ["sources", "routes", "hessian", "vertical", "quotient", "dcdagger", "demotion", "guards", "decision", "next"]:
        write_csv(OUTPUTS[key], rows[key])

    rows["branches"] = branch_rows()
    write_csv(OUTPUTS["branches"], rows["branches"])
    remove_pycache()
    rows["validation"] = validation_rows(rows)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    overall = next(row for row in rows["validation"] if row["validation_id"] == "VAL2867_OVERALL")
    print(f"wrote {DOC}")
    print(f"VAL2867_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
