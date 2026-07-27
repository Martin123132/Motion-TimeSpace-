from __future__ import annotations

import csv
import importlib.util
import shutil
import sys
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1687"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1687-Y5-R2FR-common-action-measure-current-owner-or-source-weight-bound-acquisition.md"
VALIDATOR_MODULE = ROOT / "scripts" / "qbar_source_weight_intake_validator_1685.py"

SOURCE_FILES = {
    "1686_doc": ROOT / "1686-Y5-R2FR-parent-label-quotient-clause-or-first-real-qbar-row-source-fill.md",
    "1686_validation": OUT / "P8_Y5_BRR545_1686_VALIDATION.csv",
    "1686_quotient": OUT / "P8_Y5_PARENT_QLOC_1686_PARENT_LABEL_QUOTIENT_CLAUSE_AUDIT.csv",
    "1686_failure": OUT / "P8_Y5_PARENT_QLOC_1686_QUOTIENT_FAILURE_LEDGER.csv",
    "1686_validator": OUT / "P8_Y5_PARENT_QLOC_1686_QBAR_VALIDATOR_RESULT.csv",
    "1685_validator_module": VALIDATOR_MODULE,
    "1067_doc": ROOT / "1067-Y5-R10-parent-quantum-action-scale-normalization-or-WEP-tau-projection.md",
    "1067_action_owner": OUT / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv",
    "1067_hbar_measure": OUT / "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv",
    "1067_source_weight": OUT / "P8_Y5_R10_1067_SOURCE_WEIGHT_CONSEQUENCE_LEDGER.csv",
    "1079_doc": ROOT / "1079-Y5-R10-parent-current-owner-narrow-proof-or-finite-WEP-source-vector.md",
    "1079_current_owner": OUT / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
    "1079_counterexamples": OUT / "P8_Y5_R10_1079_COUNTEREXAMPLE_RESOLUTION_MATRIX.csv",
    "1090_doc": ROOT / "1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md",
    "1090_synthesis": OUT / "P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv",
    "1090_missing_axioms": OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv",
    "1098_doc": ROOT / "1098-Y5-R10-ordinary-constant-owner-action-signature-or-source-backed-coefficient-prior.md",
    "1098_owner": OUT / "P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
    "1311_audit": OUT / "P8_Y5_R10_1311_COEFFICIENT_SOURCE_AUDIT.csv",
    "1417_acquisition": OUT / "P8_Y5_R10_1417_QBAR_SOURCE_WEIGHT_ACQUISITION_ROWS.csv",
}

NEEDLES = {
    "1686_doc": ["TARGET_COMMON_ACTION_MEASURE_CURRENT_OWNER", "w_A S_A", "1687-Y5-R2FR-common-action-measure-current-owner-or-source-weight-bound-acquisition.md"],
    "1686_validation": ["VAL1686_OVERALL", "PASS"],
    "1686_quotient": ["PLQ1686_2_action_measure", "UNSIGNED"],
    "1686_failure": ["QFL1686_0_species_action_weight", "requires one common action-measure owner"],
    "1686_validator": ["QVR1686_0", "PLACEHOLDER_OR_BLOCKED_FIELDS"],
    "1685_validator_module": ["def evaluate_qbar_source_weight_row", "REQUIRED_FIELDS"],
    "1067_doc": ["ASO1067_5_verdict", "CONDITIONAL_NOT_PARENT_DERIVED"],
    "1067_action_owner": ["ASO1067_5_verdict", "CONDITIONAL_NOT_PARENT_DERIVED"],
    "1067_hbar_measure": ["HMO1067_4_verdict", "OWNER_NOT_DERIVED"],
    "1067_source_weight": ["SWC1067_4_verdict", "relative action-scale branch not eliminated"],
    "1079_doc": ["NCO1079_6_verdict", "NARROW_CURRENT_OWNER_PARTIAL_NOT_WEP_CLOSED"],
    "1079_current_owner": ["NCO1079_5_species_action_weight", "SURVIVES_PRE_VARIATION"],
    "1079_counterexamples": ["CER1079_0_species_action_weight", "SURVIVES"],
    "1090_doc": ["SYN1090_8_verdict", "SYNTHESIS_FAILS_MISSING_AXIOMS"],
    "1090_synthesis": ["SYN1090_8_verdict", "SYNTHESIS_FAILS_MISSING_AXIOMS"],
    "1090_missing_axioms": ["AX1090_2_common_quantum_measure", "MISSING_AXIOM_NOT_ADOPTED"],
    "1098_doc": ["OCS1098_4_source_weight_exclusion", "UNSIGNED"],
    "1098_owner": ["OCS1098_4_source_weight_exclusion", "UNSIGNED"],
    "1311_audit": ["QCSA1311_5_qbar_source_weight", "NONE"],
    "1417_acquisition": ["QSA1417_0_qbar_source_weight", "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1687_SOURCE_REGISTER.csv"
COMMON_OWNER_PROOF = OUT / "P8_Y5_PARENT_QLOC_1687_COMMON_ACTION_MEASURE_CURRENT_OWNER_PROOF_ATTEMPT.csv"
COUNTERMODEL_TRIAGE = OUT / "P8_Y5_PARENT_QLOC_1687_OWNER_COUNTERMODEL_TRIAGE.csv"
BOUND_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1687_SOURCE_WEIGHT_BOUND_ACQUISITION_CONTRACT.csv"
QBAR_CANDIDATE = OUT / "P8_Y5_PARENT_QLOC_1687_QBAR_BOUND_CANDIDATE_NONCLAIM.csv"
QBAR_VALIDATOR_RESULT = OUT / "P8_Y5_PARENT_QLOC_1687_QBAR_VALIDATOR_RESULT.csv"
GATE_STATUS = OUT / "P8_Y5_PARENT_QLOC_1687_GATE_STATUS.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1687_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1687_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1687_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1687_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    COMMON_OWNER_PROOF,
    COUNTERMODEL_TRIAGE,
    BOUND_CONTRACT,
    QBAR_CANDIDATE,
    QBAR_VALIDATOR_RESULT,
    GATE_STATUS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    COMMON_OWNER_PROOF,
    COUNTERMODEL_TRIAGE,
    BOUND_CONTRACT,
    QBAR_CANDIDATE,
    QBAR_VALIDATOR_RESULT,
    GATE_STATUS,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    COMMON_OWNER_PROOF: [
        QUARANTINE / "COMMON_ACTION_MEASURE_CURRENT_OWNER_PROOF_ATTEMPT.csv",
        BRANCH_RESIDUALS / "R2FR_common_action_measure_current_owner_proof_attempt_1687.csv",
        QUEUE / "JR1687_COMMON_ACTION_MEASURE_CURRENT_OWNER_PROOF_ATTEMPT.csv",
    ],
    COUNTERMODEL_TRIAGE: [
        QUARANTINE / "OWNER_COUNTERMODEL_TRIAGE.csv",
        BRANCH_RESIDUALS / "R2FR_owner_countermodel_triage_1687.csv",
        QUEUE / "JR1687_OWNER_COUNTERMODEL_TRIAGE.csv",
    ],
    BOUND_CONTRACT: [
        QUARANTINE / "SOURCE_WEIGHT_BOUND_ACQUISITION_CONTRACT.csv",
        BRANCH_RESIDUALS / "R2FR_source_weight_bound_acquisition_contract_1687.csv",
        QUEUE / "JR1687_SOURCE_WEIGHT_BOUND_ACQUISITION_CONTRACT.csv",
    ],
    QBAR_VALIDATOR_RESULT: [
        QUARANTINE / "QBAR_VALIDATOR_RESULT.csv",
        BRANCH_RESIDUALS / "R2FR_qbar_validator_result_1687.csv",
        QUEUE / "JR1687_QBAR_VALIDATOR_RESULT.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1687.csv",
        QUEUE / "JR1687_NEXT_TARGET_NONCLAIM.csv",
    ],
}

SCORE_FLAGS = [
    "proof_signed",
    "countermodel_killed",
    "bound_ready",
    "row_pass",
    "gate_pass",
    "accepted_for_scoring",
    "score_ready",
    "valid_prediction_row",
    "valid_for_claim",
    "claim_allowed",
]


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_cell(value: object) -> bool:
    return str(value).strip().lower() == "true"


def blocked_marker(value: object) -> bool:
    text = str(value)
    markers = [
        "MISSING_",
        "NOT_",
        "BLOCKED",
        "REJECT",
        "FAIL",
        "DRY_RUN",
        "UNSIGNED",
        "NONE",
        "NO_VALUE",
        "NO_BOUND",
        "NONCLAIM",
        "SURVIVES",
        "OWNER_NOT_DERIVED",
    ]
    return any(marker in text for marker in markers)


def list_cell(value: object) -> str:
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if isinstance(value, dict):
        return ";".join(f"{key}={item}" for key, item in sorted(value.items()))
    return str(value)


def load_validator() -> ModuleType:
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("qbar_source_weight_intake_validator_1685", VALIDATOR_MODULE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load validator module: {VALIDATOR_MODULE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_key, source_path in SOURCE_FILES.items():
        exists = source_path.exists()
        body = read_text(source_path) if exists else ""
        needles_present = all(needle in body for needle in NEEDLES[source_key])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": source_key,
                "source_path": str(source_path),
                "exists": exists,
                "needles_present": needles_present,
                "required_needles": "; ".join(NEEDLES[source_key]),
                "use_in_1687": "common action-measure-current owner proof or source-weight bound acquisition",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def common_owner_proof_rows() -> list[dict[str, object]]:
    rows = [
        (
            "COM1687_0_target",
            "one common action-measure-current owner",
            "S_parent/hbar_parent contains sum_A S_A with one shared hbar_parent, species-blind measure, one Hilbert source, and no w_A S_A or kappa_A T_A slot",
            "TARGET_EXACT",
            "would kill both pre-variation action weights and post-variation source-current rescalings",
            "current corpus has this as a target/contract, not as a parent-derived owner",
            "ASO1067_0_target;HMO1067_4_verdict;PLQ1686_2_action_measure",
        ),
        (
            "COM1687_1_hilbert_source",
            "Hilbert variation gives a unique source after common action is fixed",
            "T_mu_nu := delta S_matter/delta e_obs before readout",
            "EXACT_SUBTHEOREM_CONDITIONAL",
            "kills post-variation source-current selectors and later J_A -> c_A J_A moves",
            "requires common S_matter and variation-before-readout as premises",
            "NCO1079_1_hilbert_variation;NCO1079_3_post_variation_selector",
        ),
        (
            "COM1687_2_ward_conservation",
            "diffeomorphism Ward identity owns conservation",
            "nabla_mu T^mu_nu = 0 on matter shell for the common observed geometry",
            "CONDITIONAL_WARD_IDENTITY",
            "keeps source conservation tied to the same matter action",
            "does not fix relative weights already inserted into S_matter",
            "NCO1079_2_ward_identity",
        ),
        (
            "COM1687_3_action_scale",
            "species action weights are not removable by classical EOM scaling",
            "delta(w_A S_A)/delta g_obs = w_A T_A even when delta(w_A S_A)/delta Psi_A=0 reduces to ordinary EOM",
            "OBSTRUCTION_EXPLICIT",
            "forces the theory to own or bound w_A rather than hand-wave it away",
            "no parent action-measure owner currently forbids w_A S_A",
            "ASO1067_1_classical_EOM_vs_source;ASO1067_2_path_integral_measure",
        ),
        (
            "COM1687_4_measure_hbar",
            "single hbar/path-integral/statistical measure owner",
            "exp(i sum_A S_A/hbar_parent) with no species-dependent hbar_A or Jacobian J_A",
            "OWNER_NOT_DERIVED",
            "would forbid quantum/statistical replicas of source weights",
            "HMO1067_0, HMO1067_1, and AX1090_2 remain missing/not adopted",
            "HMO1067_4_verdict;AX1090_2_common_quantum_measure",
        ),
        (
            "COM1687_5_object_language",
            "parent object language excludes inert source-only slots",
            "Arg(S_parent) has geometry, matter fields, gauge/current data, representation constants, universal constants; no inert w_A/kappa_A",
            "OBJECT_LANGUAGE_NOT_SIGNED",
            "would make owner theorem syntactic rather than fitted",
            "1066/1078/1090 keep object-language and parent action object as missing signatures",
            "SSE1066_5_verdict;OL1078_4_verdict;SYN1090_8_verdict",
        ),
        (
            "COM1687_6_verdict",
            "common owner proves qbar_source_weight theorem-zero",
            "COM1687_0 through COM1687_5 all parent-signed",
            "PROOF_NOT_CLOSED",
            "qbar_source_weight = 0 by owner theorem",
            "Hilbert/current part is a useful conditional subtheorem, but pre-variation action weights and measure owner remain open",
            "ASO1067_5_verdict;NCO1079_6_verdict;SYN1090_8_verdict",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "proof_id": proof_id,
            "claim": claim,
            "mathematical_form": mathematical_form,
            "current_result": current_result,
            "if_signed": if_signed,
            "current_gap": current_gap,
            "source_anchor": source_anchor,
            "proof_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for proof_id, claim, mathematical_form, current_result, if_signed, current_gap, source_anchor in rows
    ]


def countermodel_triage_rows() -> list[dict[str, object]]:
    rows = [
        ("OCT1687_0_post_variation_selector", "F(T_A,A) after source variation", "KILLED_CONDITIONALLY", "Hilbert-source owner plus variation-before-readout forbids retroactive source redefinition", "still needs readout-order signature", "NCO1079_3_post_variation_selector;CER1079_3_post_variation_selector"),
        ("OCT1687_1_current_rescaling", "J_A -> c_A J_A after Hilbert source extraction", "KILLED_CONDITIONALLY", "later current rescaling is not a new variational source if source is owned by delta S/delta e_obs", "c_A can still enter as pre-action coefficient", "NCO1079_4_current_rescaling;CER1079_1_current_rescaling"),
        ("OCT1687_2_species_action_weight", "S_matter = sum_A w_A S_A", "SURVIVES", "Hilbert variation inherits w_A when it is inserted before variation", "needs action-measure/object-language owner or finite sourced coefficient", "ASO1067_1_classical_EOM_vs_source;CER1079_0_species_action_weight"),
        ("OCT1687_3_species_hbar_measure", "hbar_A or J_A measure factors", "SURVIVES", "quantum/statistical normalization can mimic action weights", "needs one parent hbar/measure owner", "HMO1067_0_hbar_parent;HMO1067_1_measure_parent"),
        ("OCT1687_4_disconnected_components", "independent constants on disconnected matter/source components", "SURVIVES", "current owner does not connect disconnected action summands", "needs connected matter functor or finite material/source tensor", "CER1079_2_disconnected_material_components;ODR1066_2_species_component_obstruction"),
        ("OCT1687_5_source_weight_vertex", "w_A(Xhat), kappa_A(Xhat), source-only material multiplier", "SURVIVES", "ordinary-constant owner action signature is not derived", "needs OCS1098_4 parent signature or finite qbar bound", "OCS1098_4_source_weight_exclusion;FV1098_6_source_weight_X"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "triage_id": triage_id,
            "countermodel": countermodel,
            "current_result": current_result,
            "reason": reason,
            "needed_next": needed_next,
            "source_anchor": source_anchor,
            "countermodel_killed": current_result == "KILLED_CONDITIONALLY",
            "proof_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for triage_id, countermodel, current_result, reason, needed_next, source_anchor in rows
    ]


def bound_contract_rows() -> list[dict[str, object]]:
    rows = [
        (
            "BND1687_0_definition",
            "qbar_source_weight",
            "zeta_source_weight_I := sup_{A,B}|partial_{X_I} ln(kappa_A/kappa_B)|",
            "dimensionless per X_I coordinate convention",
            "parent_basis_X_I; normalization; coordinate_dimension",
            "MISSING_PARENT_BASIS_AND_NORMALIZATION",
        ),
        (
            "BND1687_1_WEP",
            "MICROSCOPE/WEP",
            "|zeta| <= eta_bound / |K_WEP tau_WEP DeltaQ_source_AB|",
            "dimensionless",
            "eta_bound; K_WEP; tau_WEP; material/source contrast; orbit/readout convention",
            "MISSING_TAU_MATERIAL_SOURCE_DENOMINATOR",
        ),
        (
            "BND1687_2_R10",
            "short-range inverse-square/R10",
            "|zeta(lambda)| <= alpha_bound(lambda) / |K_R10 Q_source(lambda) Q_test(lambda)|",
            "dimensionless",
            "alpha_bound curve; lambda owner; source/test charges; Pi_M projection",
            "MISSING_ALPHA_BOUND_PROJECTION_DENOMINATOR",
        ),
        (
            "BND1687_3_Newton_GM",
            "Newton/GM calibration",
            "|zeta| <= |Delta(GM)/GM| / |K_GM source_contrast|",
            "dimensionless",
            "measured-G convention; calibration body map; source composition contrast",
            "MISSING_GM_CALIBRATION_CONVENTION",
        ),
        (
            "BND1687_4_PPN",
            "PPN/local-GR source residual",
            "||zeta|| <= ||Delta_PPN|| / ||P_PPN K_source||",
            "dimensionless",
            "weak-field source projection matrix; PPN residual vector; denominator rank",
            "MISSING_PPN_PROJECTION_MATRIX",
        ),
        (
            "BND1687_5_verdict",
            "first source-weight bound row",
            "one arena denominator plus source path must be numeric and nonzero before validator use",
            "not scoreable",
            "at least one complete sourced arena denominator and a parent basis convention",
            "BOUND_CONTRACT_READY_INPUTS_MISSING_NONCLAIM",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "bound_id": bound_id,
            "arena": arena,
            "bound_formula": bound_formula,
            "units": units,
            "required_inputs": required_inputs,
            "current_status": current_status,
            "bound_ready": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for bound_id, arena, bound_formula, units, required_inputs, current_status in rows
    ]


def qbar_candidate_rows(validator: ModuleType) -> list[dict[str, object]]:
    row = {
        "branch_id": BRANCH_ID,
        "candidate_id": "CAND1687_0_source_weight_bound_contract_candidate",
        "basis_component": "qbar_source_weight",
        "coefficient_symbol": "zeta_source_weight_I",
        "accepted_form": "finite envelope bound from WEP/R10/Newton/PPN denominator or theorem-zero common owner",
        "theorem_route_status": "NOT_PARENT_SIGNED",
        "finite_route_status": "NOT_FILLED",
        "source_label_forgetting_status": "NOT_DERIVED",
        "ordinary_matter_connectedness_status": "NOT_DERIVED",
        "value_or_bound": "MISSING_NUMERIC_SOURCE_WEIGHT_BOUND",
        "uncertainty": "MISSING_BOUND_UNCERTAINTY",
        "sign_convention": "absolute envelope bound; sign not claimed",
        "material_or_source_tags": "MISSING_ARENA_SOURCE_TEST_TAGS",
        "lambda_or_domain_if_range_dependent": "MISSING_LAMBDA_OR_DOMAIN_FOR_ARENA",
        "parent_basis_X_I": "MISSING_PARENT_BASIS_X_I",
        "normalization": "MISSING_NORMALIZATION",
        "units": "dimensionless per X_I convention not yet signed",
        "coordinate_dimension": "MISSING_COORDINATE_DIMENSION",
        "common_mode_measured_G_convention": "MISSING_COMMON_MODE_MEASURED_G_CONVENTION",
        "local_source_path": str(BOUND_CONTRACT),
        "source_anchor": "BND1687_5_verdict",
        "derivation_or_data_method": "bound acquisition contract only; no numeric denominator",
        "confidence": "contract high; numeric coefficient unavailable",
        "extraction_status": "BOUND_CONTRACT_READY_INPUTS_MISSING_NONCLAIM",
        "WEP_tau_material_worldtube": "MISSING_WEP_TAU_MATERIAL_WORLDTUBE",
        "R10_lambda_alpha_projection": "MISSING_R10_LAMBDA_ALPHA_PROJECTION",
        "Newton_GM_calibration": "MISSING_NEWTON_GM_CALIBRATION",
        "R11_operator_projection": "MISSING_R11_OPERATOR_PROJECTION",
        "PPN_local_GR_projection": "MISSING_PPN_LOCAL_GR_PROJECTION",
        "accepted_for_scoring": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    return [{field: row.get(field, "") for field in validator.REQUIRED_FIELDS}]


def validator_result_rows(validator: ModuleType, candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for candidate in candidates:
        result = validator.evaluate_qbar_source_weight_row(candidate, root=ROOT)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "result_id": f"QVR1687_{len(rows)}",
                "candidate_id": candidate["candidate_id"],
                "row_pass": result["row_pass"],
                "reason": result["reason"],
                "route": result["route"],
                "route_ok": result["route_ok"],
                "placeholder_fields": list_cell(result["placeholder_fields"]),
                "numeric_failures": list_cell(result["numeric_failures"]),
                "source_path_exists": result["source_path_exists"],
                "resolved_source_path": result["resolved_source_path"],
                "claim_safety_violation": result["claim_safety_violation"],
                "accepted_for_scoring": False,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": result["valid_for_claim"],
                "claim_allowed": result["claim_allowed"],
            }
        )
    return rows


def gate_status_rows(
    proof_rows: list[dict[str, object]],
    triage_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    validator_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    proof_closed = any(row["current_result"] == "PROOF_CLOSED" and bool_cell(row["proof_signed"]) for row in proof_rows)
    hard_survivors = [row for row in triage_rows if row["current_result"] == "SURVIVES"]
    bound_ready = any(bool_cell(row["bound_ready"]) for row in bound_rows)
    validator_pass = any(bool_cell(row["row_pass"]) for row in validator_rows)
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1687_0_common_owner",
            "gate": "common action-measure-current owner theorem",
            "current_status": "PROOF_NOT_CLOSED" if not proof_closed else "UNEXPECTED_PROOF_CLOSED",
            "gate_pass": False,
            "reason": "Hilbert/current subtheorem is conditional; action-measure/object-language owner remains unsigned",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1687_1_countermodels",
            "gate": "source-weight countermodel kill set",
            "current_status": "HARD_COUNTERMODELS_SURVIVE" if hard_survivors else "UNEXPECTED_ALL_KILLED",
            "gate_pass": False,
            "reason": "pre-variation species weights, hbar/measure factors, disconnected components, and source vertices survive",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1687_2_bound_contract",
            "gate": "finite source-weight bound acquisition",
            "current_status": "BOUND_FORMULAS_READY_INPUTS_MISSING" if not bound_ready else "UNEXPECTED_BOUND_READY",
            "gate_pass": False,
            "reason": "WEP/R10/Newton/PPN denominator inputs and parent basis convention are missing",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GST1687_3_qbar_validator",
            "gate": "1685 qbar intake validator",
            "current_status": "ACTIVE_REJECTS_1687_CANDIDATE" if not validator_pass else "UNEXPECTED_VALIDATOR_PASS",
            "gate_pass": False,
            "reason": "candidate has no numeric bound/value and projection fields remain missing",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("D1687_0_partial_win", "HILBERT_CURRENT_OWNER_SUBTHEOREM_RETAINED", "inside a common action, variation-before-readout gives a unique source and kills post-variation selectors", "keep as conditional theorem block"),
        ("D1687_1_no_theorem_zero", "COMMON_OWNER_NOT_DERIVED", "pre-variation w_A S_A and species hbar/measure factors survive without parent action-measure/object-language ownership", "do not set qbar_source_weight=0"),
        ("D1687_2_bound_contract", "SOURCE_WEIGHT_BOUND_FORMULAS_WRITTEN", "WEP/R10/Newton/PPN bound formulas are explicit but denominator inputs are missing", "acquire denominator inputs before scoring"),
        ("D1687_3_validator", "1685_VALIDATOR_REJECTS_1687_BOUND_CANDIDATE", "candidate points to real bound contract but contains no numeric value/bound", "retain source branch gate"),
        ("D1687_4_next", "TARGET_ACTION_MEASURE_OWNER_SOURCE_SEARCH_OR_BOUND_DATA", "next progress is either a real parent source signing hbar/measure ownership or first numeric denominator data", "move to 1688"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1687_0_common_owner", "common action-measure-current owner", "BLOCKED", "action-measure/object-language owner unsigned"),
        ("CG1687_1_qbar_zero", "qbar_source_weight theorem-zero", "BLOCKED", "pre-variation species weights survive"),
        ("CG1687_2_bound_ready", "finite qbar source-weight bound", "BLOCKED", "bound formulas have missing denominators"),
        ("CG1687_3_validator", "qbar validator pass", "BLOCKED", "1687 candidate rejected"),
        ("CG1687_4_local_claim", "local GR/Newton/WEP/R10/PPN source-side claim", "BLOCKED", "neither theorem-zero nor finite bound route passes"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_pass": False,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1688-Y5-R2FR-action-measure-owner-source-search-or-qbar-bound-data-pack.md",
            "script": "scripts/Y5_R2FR_action_measure_owner_source_search_or_qbar_bound_data_pack.py",
            "objective": "search the corpus for a real parent source that signs hbar/action-measure ownership; if none exists, begin a finite qbar_source_weight bound data pack by filling one arena denominator path",
            "success_condition": "either action-measure ownership is parent-signed, or one WEP/R10/Newton/PPN source-weight bound row becomes numeric, sourced, and validator-ready",
            "why_next": "1687 isolates action-measure ownership as the remaining theorem blocker and gives explicit bound formulas for the finite route",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


def validate(
    source_rows: list[dict[str, object]],
    proof_rows: list[dict[str, object]],
    triage_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    candidate_rows_: list[dict[str, object]],
    validator_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    owner_not_closed = any(row["proof_id"] == "COM1687_6_verdict" and row["current_result"] == "PROOF_NOT_CLOSED" for row in proof_rows) and all(not bool_cell(row["proof_signed"]) for row in proof_rows)
    partial_subtheorem = any(row["proof_id"] == "COM1687_1_hilbert_source" and row["current_result"] == "EXACT_SUBTHEOREM_CONDITIONAL" for row in proof_rows)
    hard_survivors = [row for row in triage_rows if row["current_result"] == "SURVIVES"]
    countermodels_survive = len(hard_survivors) >= 4 and all(not bool_cell(row["proof_signed"]) for row in triage_rows)
    bound_contract_ready = len(bound_rows) >= 5 and any(row["bound_id"] == "BND1687_5_verdict" and row["current_status"] == "BOUND_CONTRACT_READY_INPUTS_MISSING_NONCLAIM" for row in bound_rows)
    bound_not_scoreable = all(not bool_cell(row["bound_ready"]) and not bool_cell(row["score_ready"]) for row in bound_rows)
    candidate_nonclaim = len(candidate_rows_) == 1 and candidate_rows_[0]["candidate_id"] == "CAND1687_0_source_weight_bound_contract_candidate" and not bool_cell(candidate_rows_[0]["valid_for_claim"])
    validator_rejects = len(validator_rows) == 1 and not bool_cell(validator_rows[0]["row_pass"]) and "PLACEHOLDER_OR_BLOCKED_FIELDS" in validator_rows[0]["reason"]
    source_path_used = len(validator_rows) == 1 and bool_cell(validator_rows[0]["source_path_exists"])
    gate_locked = all(not bool_cell(row["gate_pass"]) for row in gate_rows)
    decision_safe = any(row["decision"] == "TARGET_ACTION_MEASURE_OWNER_SOURCE_SEARCH_OR_BOUND_DATA" for row in decisions)
    claim_gate_safe = all(not bool_cell(row["gate_pass"]) and not bool_cell(row["claim_allowed"]) for row in claims)
    next_target_selected = next_rows[0]["next_target"] == "1688-Y5-R2FR-action-measure-owner-source-search-or-qbar-bound-data-pack.md"
    csv_parse = all(path.exists() and len(read_csv(path)) >= 1 for path in GENERATED)
    branch_copies = all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1687*")) if FORMALIZATION.exists() else True

    no_claim_flags = True
    blocked_not_ready = True
    for generated_path in CLAIM_CHECKED:
        for generated_row in read_csv(generated_path):
            if generated_row.get("valid_for_claim", "False").lower() == "true" or generated_row.get("claim_allowed", "False").lower() == "true":
                no_claim_flags = False
            if any(blocked_marker(value) for value in generated_row.values()):
                for claim_key in SCORE_FLAGS:
                    if claim_key in generated_row and bool_cell(generated_row[claim_key]):
                        if claim_key == "countermodel_killed" and generated_row.get("current_result") == "KILLED_CONDITIONALLY":
                            continue
                        blocked_not_ready = False

    checks = [
        ("VAL1687_0_sources_exist", sources_ok, "all cited 1687 source paths exist and required needles are present"),
        ("VAL1687_1_owner_not_closed", owner_not_closed, "common action-measure-current owner remains unsigned"),
        ("VAL1687_2_partial_subtheorem", partial_subtheorem, "Hilbert-current owner conditional subtheorem is retained"),
        ("VAL1687_3_countermodels_survive", countermodels_survive, "hard source-weight countermodels survive"),
        ("VAL1687_4_bound_contract_ready", bound_contract_ready, "source-weight bound formulas are written"),
        ("VAL1687_5_bound_not_scoreable", bound_not_scoreable, "bound rows remain non-scoreable"),
        ("VAL1687_6_candidate_nonclaim", candidate_nonclaim, "qbar bound candidate remains nonclaim"),
        ("VAL1687_7_validator_rejects", validator_rejects, "1685 validator rejects 1687 qbar candidate"),
        ("VAL1687_8_source_path_used", source_path_used, "candidate points to existing bound contract"),
        ("VAL1687_9_gate_locked", gate_locked, "all gates remain locked"),
        ("VAL1687_10_decision_safe", decision_safe, "decision selects owner source search or bound data pack"),
        ("VAL1687_11_claim_gate_safe", claim_gate_safe, "all claim gates remain false"),
        ("VAL1687_12_no_claim_flags", no_claim_flags, "all generated rows keep claim flags false"),
        ("VAL1687_13_blocked_not_ready", blocked_not_ready, "no blocked/missing row is marked claim/scoring ready"),
        ("VAL1687_14_next_target_selected", next_target_selected, "next target selects action-measure owner source search or qbar bound data pack"),
        ("VAL1687_15_csv_parse", csv_parse, "all generated 1687 CSVs parse"),
        ("VAL1687_16_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1687_17_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1687_18_formalization_untouched", formalization_clean, "no 1687 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "check_id": "VAL1687_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1687 common action-measure-current owner or source-weight bound acquisition validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return validation_rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    table_rows = []
    for row in rows:
        table_rows.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *table_rows])


def write_doc(
    source_rows: list[dict[str, object]],
    proof_rows: list[dict[str, object]],
    triage_rows: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    candidate_rows_: list[dict[str, object]],
    validator_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1687 - Common Action-Measure-Current Owner Or Source-Weight Bound Acquisition

**Private status:** source-weight owner/bound checkpoint. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, WEP pass, R10 pass, R11 pass, clock pass, orbital pass, or public claim is made.

## Verdict

The owner route gives a real partial win: if one common matter action is varied before readout, the Hilbert source is unique and post-variation source selectors are conditionally killed. But this still does not derive `qbar_source_weight=0`, because pre-variation `w_A S_A`, species-dependent hbar/measure factors, disconnected source components, and explicit source-weight vertices remain legal unless the parent action-measure/object-language owner is signed.

The finite route is now less vague: 1687 writes the bound formulas for WEP, R10, Newton-GM, and PPN/local-GR source-weight constraints. They are not scoreable yet, because the denominators, parent basis convention, and arena projections are missing. The 1685 validator correctly rejects the 1687 qbar candidate.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1687"])}

## Common Owner Proof Attempt

{markdown_table(proof_rows, ["proof_id", "claim", "mathematical_form", "current_result", "current_gap"])}

## Countermodel Triage

{markdown_table(triage_rows, ["triage_id", "countermodel", "current_result", "reason", "needed_next"])}

## Source-Weight Bound Acquisition Contract

{markdown_table(bound_rows, ["bound_id", "arena", "bound_formula", "required_inputs", "current_status"])}

## Qbar Bound Candidate

{markdown_table(candidate_rows_, ["candidate_id", "basis_component", "coefficient_symbol", "finite_route_status", "value_or_bound", "local_source_path", "valid_for_claim"])}

## Validator Result

{markdown_table(validator_rows, ["result_id", "candidate_id", "row_pass", "reason", "route", "source_path_exists", "claim_safety_violation"])}

## Gate Status

{markdown_table(gate_rows, ["gate_id", "gate", "current_status", "gate_pass", "reason"])}

## Decisions

{markdown_table(decision_rows_, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "gate", "gate_pass", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

1687 narrows the fight. We should stop spending broad words on source-label forgetting and either find a parent source that truly owns `hbar/action-measure/current` for all ordinary sectors, or start filling one finite denominator path so `qbar_source_weight` can be bounded instead of wished away.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    validator = load_validator()
    source_rows = source_register_rows()
    proof_rows = common_owner_proof_rows()
    triage_rows = countermodel_triage_rows()
    bound_rows = bound_contract_rows()

    write_csv(SOURCE_REGISTER, source_rows, ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1687", "valid_for_claim", "claim_allowed"])
    write_csv(COMMON_OWNER_PROOF, proof_rows, ["branch_id", "proof_id", "claim", "mathematical_form", "current_result", "if_signed", "current_gap", "source_anchor", "proof_signed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(COUNTERMODEL_TRIAGE, triage_rows, ["branch_id", "triage_id", "countermodel", "current_result", "reason", "needed_next", "source_anchor", "countermodel_killed", "proof_signed", "valid_for_claim", "claim_allowed"])
    write_csv(BOUND_CONTRACT, bound_rows, ["branch_id", "bound_id", "arena", "bound_formula", "units", "required_inputs", "current_status", "bound_ready", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])

    candidates = qbar_candidate_rows(validator)
    validator_rows = validator_result_rows(validator, candidates)
    gate_rows = gate_status_rows(proof_rows, triage_rows, bound_rows, validator_rows)
    decisions = decision_rows()
    claims = claim_gate_rows()
    next_rows = next_target_rows()

    write_csv(QBAR_CANDIDATE, candidates, list(validator.REQUIRED_FIELDS))
    write_csv(QBAR_VALIDATOR_RESULT, validator_rows, ["branch_id", "result_id", "candidate_id", "row_pass", "reason", "route", "route_ok", "placeholder_fields", "numeric_failures", "source_path_exists", "resolved_source_path", "claim_safety_violation", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(GATE_STATUS, gate_rows, ["branch_id", "gate_id", "gate", "current_status", "gate_pass", "reason", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])
    write_csv(DECISION, decisions, ["branch_id", "decision_id", "decision", "reason", "next_action", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claims, ["branch_id", "gate_id", "gate", "gate_pass", "status", "reason", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "next_target", "script", "objective", "success_condition", "why_next", "valid_for_claim", "claim_allowed"])

    copy_outputs()
    validation_rows = validate(source_rows, proof_rows, triage_rows, bound_rows, candidates, validator_rows, gate_rows, decisions, claims, next_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, proof_rows, triage_rows, bound_rows, candidates, validator_rows, gate_rows, decisions, claims, next_rows, validation_rows)

    failed_rows = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAIL {failed_row['check_id']}: {failed_row['detail']}")
        raise SystemExit(1)
    print("1687 validation PASS")


if __name__ == "__main__":
    main()
