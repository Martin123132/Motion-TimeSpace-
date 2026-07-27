from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1679"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1679-Y5-R2FR-parent-Rsource-basis-minimal-symbolic-map-or-data-probe.md"

SOURCE_FILES = {
    "1678_doc": ROOT / "1678-Y5-R2FR-Rsource-parent-basis-and-WEP-R10-projection-acquisition.md",
    "1678_validation": OUT / "P8_Y5_BRR545_1678_VALIDATION.csv",
    "1678_basis_gate": OUT / "P8_Y5_PARENT_QLOC_1678_RSOURCE_PARENT_BASIS_GATE.csv",
    "1678_next_target": OUT / "P8_Y5_PARENT_QLOC_1678_NEXT_TARGET.csv",
    "1415_rsource_template": OUT / "P8_Y5_R10_1415_RSOURCE_FINITE_TEMPLATE.csv",
    "1309_qc_residual": OUT / "P8_Y5_R10_1309_QC_RESIDUAL_VECTOR_NONCLAIM.csv",
    "1308_alpha_inputs": OUT / "P8_Y5_R10_1308_CANONICAL_ALPHA_INPUTS_NONCLAIM.csv",
    "1310_qc_acquisition": OUT / "P8_Y5_R10_1310_QC_COEFFICIENT_ACQUISITION_NONCLAIM.csv",
    "1310_r10_bridge": OUT / "P8_Y5_R10_1310_R10_QC_TEMPLATE_BRIDGE_NONCLAIM.csv",
    "1409_web_probe": OUT / "P8_Y5_R10_1409_WEB_SOURCE_PROBE_LEDGER.csv",
    "1409_readout_blockers": OUT / "P8_Y5_R10_1409_OFFICIAL_READOUT_BLOCKER_LEDGER.csv",
    "1076_owner_gates": OUT / "P8_Y5_R10_1076_COUPLING_OWNER_GATES.csv",
    "1077_counterexamples": OUT / "P8_Y5_R10_1077_ZERO_THEOREM_COUNTEREXAMPLE_AUDIT.csv",
    "1224_finite_contract": OUT / "P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv",
}

NEEDLES = {
    "1678_doc": ["PARENT_BASIS_FIRST", "numbers would be a costume party"],
    "1678_validation": ["VAL1678_OVERALL", "PASS"],
    "1678_basis_gate": ["PBG1678_0_basis", "MISSING_PARENT_COUPLING_BASIS"],
    "1678_next_target": ["1679-Y5-R2FR-parent-Rsource-basis-minimal-symbolic-map-or-data-probe.md"],
    "1415_rsource_template": ["RSF1415_0_R_source", "FINITE_RSOURCE_TEMPLATE_NONCLAIM"],
    "1309_qc_residual": ["QCR1309_2_qbar_source_weight", "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT"],
    "1308_alpha_inputs": ["CAI1308_4_alpha_c", "MISSING_ALPHA_NUMERATOR_AND_MEASURED_GM_SPLIT"],
    "1310_qc_acquisition": ["QCA1310_5_qbar_source_weight", "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT"],
    "1310_r10_bridge": ["RTB1310_2_source_weight_alpha", "TEMPLATE_NONCLAIM_SOURCE_WEIGHT_ROW_CREATED"],
    "1409_web_probe": ["WEB1409_2_onera_portal_pointer", "PORTAL_POINTER_ONLY_NO_LOCAL_CMSM_EXPORT"],
    "1409_readout_blockers": ["ORB1409_0_CMSM_export", "OFFICIAL_ARRAYS_NOT_ACQUIRED"],
    "1076_owner_gates": ["OWN1076_0_parent_object_language", "MISSING_PARENT_COUPLING_BASIS"],
    "1077_counterexamples": ["CE1077_1_current_rescaling", "source charge vector"],
    "1224_finite_contract": ["FSW1224_4_readout_kernel", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1679_SOURCE_REGISTER.csv"
MINIMAL_BASIS_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1679_MINIMAL_RSOURCE_BASIS_ATTEMPT.csv"
BASIS_COMPONENT_MAP = OUT / "P8_Y5_PARENT_QLOC_1679_BASIS_COMPONENT_MAP_NONCLAIM.csv"
BASIS_VERDICT = OUT / "P8_Y5_PARENT_QLOC_1679_BASIS_VERDICT.csv"
WEP_DATA_PROBE = OUT / "P8_Y5_PARENT_QLOC_1679_WEP_DATA_PROBE_DRY_RUN_LEDGER.csv"
R10_SOURCE_PROBE = OUT / "P8_Y5_PARENT_QLOC_1679_R10_SOURCE_PROBE_DRY_RUN_LEDGER.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1679_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1679_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1679_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1679_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    MINIMAL_BASIS_ATTEMPT,
    BASIS_COMPONENT_MAP,
    BASIS_VERDICT,
    WEP_DATA_PROBE,
    R10_SOURCE_PROBE,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    MINIMAL_BASIS_ATTEMPT,
    BASIS_COMPONENT_MAP,
    BASIS_VERDICT,
    WEP_DATA_PROBE,
    R10_SOURCE_PROBE,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    BASIS_COMPONENT_MAP: [
        QUARANTINE / "BASIS_COMPONENT_MAP_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Rsource_basis_component_map_nonclaim_1679.csv",
        QUEUE / "JR1679_RSOURCE_BASIS_COMPONENT_MAP_NONCLAIM.csv",
    ],
    WEP_DATA_PROBE: [
        QUARANTINE / "WEP_DATA_PROBE_DRY_RUN_LEDGER.csv",
        BRANCH_RESIDUALS / "R2FR_WEP_data_probe_dry_run_1679.csv",
        QUEUE / "JR1679_WEP_DATA_PROBE_DRY_RUN.csv",
    ],
    R10_SOURCE_PROBE: [
        QUARANTINE / "R10_SOURCE_PROBE_DRY_RUN_LEDGER.csv",
        BRANCH_RESIDUALS / "R2FR_R10_source_probe_dry_run_1679.csv",
        QUEUE / "JR1679_R10_SOURCE_PROBE_DRY_RUN.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1679.csv",
        QUEUE / "JR1679_NEXT_TARGET_NONCLAIM.csv",
    ],
}

EXPECTED_COMPONENTS = {
    "qbar_source_weight",
    "current_rescaling_residual",
    "marker_readout_residual",
    "source_worldtube_projection",
    "direct_source_product",
    "beta_source_alpha_projection",
}

SCORE_FLAGS = [
    "accepted_for_scoring",
    "score_ready",
    "valid_prediction_row",
    "valid_for_claim",
    "claim_allowed",
    "parent_signed",
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
    value_text = str(value)
    markers = [
        "MISSING_",
        "NOT_SCORE",
        "NOT_IMPORTED",
        "NOT_ACQUIRED",
        "NOT_PROVED",
        "NOT_PARENT",
        "BLOCKED",
        "TEMPLATE_NONCLAIM",
        "CONTEXT_ONLY",
        "PORTAL_POINTER",
        "DRY_RUN",
        "UNSIGNED",
    ]
    return any(marker in value_text for marker in markers)


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
                "use_in_1679": "minimal R_source parent-basis map or dry-run WEP/R10 data probe",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def minimal_basis_attempt_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MBA1679_0_object",
            "object": "R_source^I",
            "candidate_definition": "finite source-side residual vector in the parent coupling/current basis X_I",
            "minimal_symbolic_map": "R_source^I := (partial_X ln kappa_A, partial_X ln c_A, partial_X marker_A, Integral_source K_source delta T_source/delta X_I, direct parent product, beta_source_alpha)",
            "parent_requirements": "typed parent object language; current owner; source-current units; measure/coframe descent; source worldtube; arena projection",
            "current_status": "SYMBOLIC_MAP_WRITTEN_BASIS_NOT_PARENT_SIGNED",
            "parent_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MBA1679_1_obstruction",
            "object": "source-current owner",
            "candidate_definition": "one parent owner forbidding species/source-only weights and current rescalings",
            "minimal_symbolic_map": "NoSourceOnlySpeciesSlot + current-owner theorem would set source-only components to zero",
            "parent_requirements": "derive from the parent action, not from desired WEP/R10 outcome",
            "current_status": "UNSIGNED_COUNTEREXAMPLES_STILL_LEGAL",
            "parent_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "MBA1679_2_consequence",
            "object": "arena projections",
            "candidate_definition": "WEP/Newton/R10/R11 readout maps applied to R_source^I",
            "minimal_symbolic_map": "observable residual = arena_kernel_I R_source^I with no cancellation unless the parent signs the kernel and basis",
            "parent_requirements": "basis/units before empirical numbers; official/equivalent WEP arrays and R10 bound/source projection before scoring",
            "current_status": "DATA_PROBE_ONLY_NO_SCORE",
            "parent_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def basis_component_rows() -> list[dict[str, object]]:
    raw_rows = [
        (
            "BMAP1679_0",
            "qbar_source_weight",
            "partial_X ln kappa_A or source-only weight derivative",
            "species/source-only gravitational prefactor sensitivity",
            "dimensionless",
            "P8_Y5_R10_1415_RSOURCE_FINITE_TEMPLATE.csv:RSF1415_1_qbar_source_weight;P8_Y5_R10_1310_QC_COEFFICIENT_ACQUISITION_NONCLAIM.csv:QCA1310_5_qbar_source_weight",
            "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT",
        ),
        (
            "BMAP1679_1",
            "current_rescaling_residual",
            "partial_X ln c_A or beta_source,A current marker",
            "source/test current normalization residual",
            "dimensionless or parent current-normalization units",
            "P8_Y5_R10_1415_RSOURCE_FINITE_TEMPLATE.csv:RSF1415_2_current_rescaling;P8_Y5_R10_1077_ZERO_THEOREM_COUNTEREXAMPLE_AUDIT.csv:CE1077_1_current_rescaling",
            "MISSING_CURRENT_OWNER_OR_COEFFICIENT",
        ),
        (
            "BMAP1679_2",
            "marker_readout_residual",
            "partial_X marker_A or post-variation readout selector residual",
            "material/preparation/shadow-frame marker sensitivity",
            "dimensionless or declared marker units",
            "P8_Y5_R10_1309_QC_RESIDUAL_VECTOR_NONCLAIM.csv:QCR1309_1_qbar_marker_abs;P8_Y5_R10_1077_ZERO_THEOREM_COUNTEREXAMPLE_AUDIT.csv:CE1077_3_post_variation_selector",
            "MISSING_MARKER_THEOREM_OR_COEFFICIENTS",
        ),
        (
            "BMAP1679_3",
            "source_worldtube_projection",
            "Integral_source K_source(x) delta T_source(x)/delta X_I",
            "Earth/source stress-current profile in observed coframe after common-mode convention is declared",
            "stress/profile convention",
            "P8_Y5_R10_1415_RSOURCE_FINITE_TEMPLATE.csv:RSF1415_3_source_worldtube;P8_Y5_R10_1409_OFFICIAL_READOUT_BLOCKER_LEDGER.csv:ORB1409_3_source_worldtube",
            "MISSING_SOURCE_WORLDTUBE",
        ),
        (
            "BMAP1679_4",
            "direct_source_product",
            "direct parent variation product into eta_AB, Newton-GM, R10, or R11 source leg",
            "bypass beta/tau split only if parent action derives the full observable contraction",
            "arena-specific source-current units",
            "P8_Y5_R10_1415_RSOURCE_FINITE_TEMPLATE.csv:RSF1415_4_direct_product;P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv:FSW1224_5_no_cancellation",
            "MISSING_DIRECT_PARENT_PRODUCT",
        ),
        (
            "BMAP1679_5",
            "beta_source_alpha_projection",
            "beta_source_alpha as EM/alpha subprojection of R_source^I",
            "source-side EM/fine-structure channel contribution to WEP/R10-like readouts",
            "dimensionless or alpha-channel projection units",
            "P8_Y5_R10_1415_RSOURCE_FINITE_TEMPLATE.csv:RSF1415_5_beta_source_alpha_projection;P8_Y5_R10_1310_R10_QC_TEMPLATE_BRIDGE_NONCLAIM.csv:RTB1310_2_source_weight_alpha",
            "TARGET_ONLY_NOT_PARENT_SIGNED",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "component_id": component_id,
            "basis_component": basis_component,
            "candidate_parent_symbol": symbol,
            "role": role,
            "unit_requirement": unit_requirement,
            "source_anchor": source_anchor,
            "current_status": status,
            "parent_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for component_id, basis_component, symbol, role, unit_requirement, source_anchor, status in raw_rows
    ]


def basis_verdict_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BVER1679_0_symbolic_basis",
            "verdict": "MINIMAL_SYMBOLIC_RSOURCE_BASIS_WRITTEN",
            "reason": "six finite source-side slots can be named in a common parent-basis ledger",
            "promotion_requirement": "parent action must sign the object language, units, source-current owner, measure/coframe descent, and no representative-only coefficients",
            "parent_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BVER1679_1_no_zero_claim",
            "verdict": "NO_ZERO_THEOREM_FROM_SYMBOL_NAMES",
            "reason": "naming R_source components does not prove qbar_source_weight, current_rescaling, marker, worldtube, or direct products vanish",
            "promotion_requirement": "derive NoSourceOnlySpeciesSlot/current-owner/no-marker theorem or retain finite nonclaim rows",
            "parent_signed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def wep_data_probe_rows() -> list[dict[str, object]]:
    raw_rows = [
        (
            "WDP1679_0_public_context",
            "MICROSCOPE mission/final result context",
            "https://arxiv.org/abs/2201.10841; https://elib.dlr.de/193667/2/Touboul_2022_Class._Quantum_Grav._39_204009.pdf",
            "public scenario/final-result context",
            "CONTEXT_ONLY_NO_MACHINE_READABLE_KERNEL_ARRAYS_ACQUIRED",
            "WEB1409_0_mission_scenario_data_flow;WEB1409_1_final_result_kernel_context",
        ),
        (
            "WDP1679_1_portal",
            "ONERA MICROSCOPE data portal route",
            "https://microscope.onera.fr/fr/publication/microscope-data-are-available",
            "portal pointer for future local export",
            "PORTAL_POINTER_ONLY_NO_LOCAL_CMSM_EXPORT",
            "WEB1409_2_onera_portal_pointer",
        ),
        (
            "WDP1679_2_CMSM_arrays",
            "official or exactly equivalent CMSM arrays",
            "local file required",
            "time;segment;gx;gz;Sxx;Sxz;masks;calibration_flags;attitude/orbit convention",
            "OFFICIAL_ARRAYS_NOT_ACQUIRED",
            "ORB1409_0_CMSM_export",
        ),
        (
            "WDP1679_3_exact_equivalent",
            "exact-equivalent reconstruction certificate",
            "local reconstruction required",
            "reproduce official kernel columns with tolerance/provenance",
            "NOT_PROVED",
            "ORB1409_1_exact_equivalent_proof",
        ),
        (
            "WDP1679_4_product_convention",
            "WEP product normalization",
            "local convention row required",
            "N_eta;sign convention;readout axis;material pair;source response basis",
            "NORMALIZATION_NOT_FILLED",
            "ORB1409_2_product_convention",
        ),
        (
            "WDP1679_5_source_worldtube",
            "Earth/source stress-current worldtube",
            "local source model required",
            "source profile;parent basis;lab-frame projection;lambda/domain;uncertainty",
            "MISSING_SOURCE_PROFILE_WEIGHTING",
            "ORB1409_3_source_worldtube",
        ),
        (
            "WDP1679_6_orbit_average",
            "orbit/session averaging operator",
            "local arrays required",
            "segment windows;masks;sample weights;calibration flags",
            "MISSING_ORBIT_AVERAGE_ARRAYS",
            "ORB1409_4_orbit_average",
        ),
        (
            "WDP1679_7_material_tensor",
            "full Ti/Pt material response tensor",
            "local tensor required",
            "Delta_f_s_AB;sector basis;uncertainties;basis map to beta_s",
            "MISSING_FULL_MATERIAL_TENSOR",
            "ORB1409_5_material_tensor",
        ),
        (
            "WDP1679_8_delta_tau",
            "Delta_w_TiPt and tau_WEP",
            "local parent/source-basis rows required",
            "positive width or signed tensor; tau functional in same basis",
            "MISSING_NUMERIC_PRIOR_WIDTH_AND_LAB_SOURCE_ORBIT_PROJECTION",
            "FSW1224_1_delta_w;FSW1224_2_tau_WEP",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "probe_id": probe_id,
            "needed_object": needed_object,
            "source_or_local_target": source_or_local_target,
            "fields_required": fields_required,
            "current_status": current_status,
            "source_anchor": source_anchor,
            "probe_status": "DRY_RUN_ONLY",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for probe_id, needed_object, source_or_local_target, fields_required, current_status, source_anchor in raw_rows
    ]


def r10_source_probe_rows() -> list[dict[str, object]]:
    raw_rows = [
        (
            "R10P1679_0_coefficients",
            "qbar_source_weight/current_rescaling/marker coefficients",
            "parent coefficient rows with units/sign/source path",
            "MISSING_COMPONENT_VALUES",
            "QCA1310_5_qbar_source_weight;QCR1309_1_qbar_marker_abs;RSF1415_2_current_rescaling",
        ),
        (
            "R10P1679_1_lambda_owner",
            "lambda_c or finite-range mass owner",
            "canonical mass gap M_c or zero/massless-tail theorem",
            "MISSING_M_c_OR_MASS_GAP",
            "CAI1308_0_lambda_c",
        ),
        (
            "R10P1679_2_source_charge",
            "Q_c^H(lambda)",
            "compact source/form-factor charge including boundary/projector/memory pieces",
            "MISSING_SOURCE_CHARGE_OR_ZERO_THEOREM",
            "CAI1308_1_Qc",
        ),
        (
            "R10P1679_3_test_charge",
            "q_c^T",
            "test-body charge/coupling or matter-descent zero theorem",
            "MISSING_TEST_CHARGE_OR_MATTER_DESCENT_ZERO",
            "CAI1308_2_qc",
        ),
        (
            "R10P1679_4_projection",
            "Pi_M^H[Q_c^H(lambda)]",
            "mass/Hamiltonian projection or orthogonality theorem",
            "MISSING_PROJECTOR_ORTHOGONALITY_OR_NUMERIC_PROJECTION",
            "CAI1308_3_PiMQ",
        ),
        (
            "R10P1679_5_alpha_row",
            "alpha_c(lambda) comparator row",
            "alpha numerator plus measured GM split and no-cancellation convention",
            "MISSING_ALPHA_NUMERATOR_AND_MEASURED_GM_SPLIT",
            "CAI1308_4_alpha_c;RTB1310_3_total_alpha_envelope",
        ),
        (
            "R10P1679_6_bound_curve",
            "R10 alpha(lambda) bound curve",
            "positive numeric full curve or source-backed anchor explicitly marked non-curve",
            "MISSING_FULL_CURVE_OR_CLAIM_GRADE_ANCHORS",
            "R10_alpha_lambda_bound_curve_DIGITIZED.csv pending acquisition",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "probe_id": probe_id,
            "needed_object": needed_object,
            "fields_required": fields_required,
            "current_status": current_status,
            "source_anchor": source_anchor,
            "probe_status": "DRY_RUN_ONLY",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for probe_id, needed_object, fields_required, current_status, source_anchor in raw_rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        (
            "D1679_0_basis",
            "MINIMAL_SYMBOLIC_MAP_NOT_PARENT_SIGNED",
            "R_source components can be named but no parent theorem fixes units/owner/zero conditions",
            "do not score WEP/R10; derive source-current owner or retain finite rows",
        ),
        (
            "D1679_1_WEP",
            "WEP_PROBE_DRY_RUN_READY",
            "public source context and portal route are recorded but official/equivalent kernel arrays are absent",
            "prepare official/equivalent data intake only after parent basis is meaningful",
        ),
        (
            "D1679_2_R10",
            "R10_PROBE_DRY_RUN_READY",
            "R10 missing chain is explicit from coefficients through lambda/projection/bound curve",
            "source coefficients and alpha bound curve remain acquisition tasks, not evidence",
        ),
        (
            "D1679_3_safety",
            "NO_LOCAL_GR_OR_R10_WEP_CLAIM",
            "symbolic map plus dry-run data probe does not derive q_loc=0 or score a bound",
            "keep all finite source branch gates false",
        ),
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
        ("CG1679_0_basis", "R_source basis parent-signed", "BLOCKED", "minimal symbolic map is not a parent action derivation"),
        ("CG1679_1_WEP", "MICROSCOPE WEP score-ready", "BLOCKED", "official/equivalent arrays, product convention, worldtube, and material tensor missing"),
        ("CG1679_2_R10", "R10 alpha(lambda) score-ready", "BLOCKED", "coefficients, lambda, source/test charges, projection, measured GM split, and bound curve missing"),
        ("CG1679_3_local_GR", "local GR/Newton/PPN pass", "BLOCKED", "finite source branch remains a residual closure/acquisition route"),
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
            "next_target": "1680-Y5-R2FR-source-current-owner-zero-theorem-or-finite-coefficient-contract.md",
            "script": "scripts/Y5_R2FR_source_current_owner_zero_theorem_or_finite_coefficient_contract.py",
            "objective": "try to derive the source-current owner/NoSourceOnlySpeciesSlot/no-marker zero theorem for the minimal R_source basis; if it fails, freeze finite coefficient contracts with units/sign/source paths",
            "success_condition": "either parent action signs R_source zero/units/owner clauses, or each surviving source component has an explicit finite coefficient acquisition contract without claim flags",
            "why_next": "1679 shows empirical data acquisition is useful but cannot become evidence until the parent source-current basis is signed or finite coefficients are honestly retained",
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
    basis_rows: list[dict[str, object]],
    basis_verdicts: list[dict[str, object]],
    wep_rows: list[dict[str, object]],
    r10_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claims: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    basis_components_exact = {row["basis_component"] for row in basis_rows} == EXPECTED_COMPONENTS
    symbolic_not_signed = all(not bool_cell(row["parent_signed"]) for row in basis_rows + basis_verdicts)
    basis_verdict_safe = any(row["verdict"] == "NO_ZERO_THEOREM_FROM_SYMBOL_NAMES" for row in basis_verdicts)
    wep_probe_complete = {
        "MICROSCOPE mission/final result context",
        "ONERA MICROSCOPE data portal route",
        "official or exactly equivalent CMSM arrays",
        "exact-equivalent reconstruction certificate",
        "WEP product normalization",
        "Earth/source stress-current worldtube",
        "orbit/session averaging operator",
        "full Ti/Pt material response tensor",
        "Delta_w_TiPt and tau_WEP",
    } == {row["needed_object"] for row in wep_rows}
    r10_probe_complete = {
        "qbar_source_weight/current_rescaling/marker coefficients",
        "lambda_c or finite-range mass owner",
        "Q_c^H(lambda)",
        "q_c^T",
        "Pi_M^H[Q_c^H(lambda)]",
        "alpha_c(lambda) comparator row",
        "R10 alpha(lambda) bound curve",
    } == {row["needed_object"] for row in r10_rows}
    decisions_safe = any(row["decision"] == "MINIMAL_SYMBOLIC_MAP_NOT_PARENT_SIGNED" for row in decisions)
    claim_gate_safe = all(not bool_cell(row["gate_pass"]) and not bool_cell(row["claim_allowed"]) for row in claims)
    next_target_selected = next_rows[0]["next_target"] == "1680-Y5-R2FR-source-current-owner-zero-theorem-or-finite-coefficient-contract.md"
    csv_parse = all(path.exists() and len(read_csv(path)) >= 1 for path in GENERATED)
    branch_copies = all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1679*")) if FORMALIZATION.exists() else True

    no_claim_flags = True
    blocked_not_ready = True
    for generated_path in CLAIM_CHECKED:
        for generated_row in read_csv(generated_path):
            if generated_row.get("valid_for_claim", "False").lower() == "true" or generated_row.get("claim_allowed", "False").lower() == "true":
                no_claim_flags = False
            if any(blocked_marker(value) for value in generated_row.values()):
                for claim_key in SCORE_FLAGS:
                    if claim_key in generated_row and bool_cell(generated_row[claim_key]):
                        blocked_not_ready = False

    checks = [
        ("VAL1679_0_sources_exist", sources_ok, "all cited 1679 source paths exist and required needles are present"),
        ("VAL1679_1_basis_components_exact", basis_components_exact, "minimal basis has exactly the six intended R_source components"),
        ("VAL1679_2_symbolic_not_signed", symbolic_not_signed, "basis map is symbolic and not parent-signed"),
        ("VAL1679_3_basis_verdict_safe", basis_verdict_safe, "zero theorem is not claimed from symbol naming"),
        ("VAL1679_4_wep_probe_complete", wep_probe_complete, "WEP dry-run data probe has all required object rows"),
        ("VAL1679_5_r10_probe_complete", r10_probe_complete, "R10 dry-run source probe has all missing-chain rows"),
        ("VAL1679_6_decisions_safe", decisions_safe, "decision records basis-not-parent-signed status"),
        ("VAL1679_7_claim_gate_safe", claim_gate_safe, "all claim gates remain false"),
        ("VAL1679_8_no_claim_flags", no_claim_flags, "all generated rows keep claim flags false"),
        ("VAL1679_9_blocked_not_ready", blocked_not_ready, "no blocked/missing/dry-run row is marked claim/scoring ready"),
        ("VAL1679_10_next_target_selected", next_target_selected, "next target selects source-current owner theorem or finite coefficient contract"),
        ("VAL1679_11_csv_parse", csv_parse, "all generated 1679 CSVs parse"),
        ("VAL1679_12_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1679_13_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1679_14_formalization_untouched", formalization_clean, "no 1679 outputs found under formalization-workbench"),
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
            "check_id": "VAL1679_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1679 parent R_source basis minimal symbolic map or data-probe validation",
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
    attempt_rows: list[dict[str, object]],
    basis_rows: list[dict[str, object]],
    verdict_rows: list[dict[str, object]],
    wep_rows: list[dict[str, object]],
    r10_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1679 - Parent Rsource Basis Minimal Symbolic Map Or Data Probe

**Private status:** derivation-first source-basis checkpoint. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

The minimal symbolic `R_source` basis can be written, but it is **not parent-signed**.

This is useful but not victorious. We now have a named six-slot source residual basis, yet the parent action still has to sign the source-current owner, source-current units, no source-only species slot, no marker readout leak, worldtube/profile convention, and direct-product projection. Until that happens, WEP and R10 remain dry-run acquisition routes, not evidence.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1679"])}

## Minimal Basis Attempt

{markdown_table(attempt_rows, ["attempt_id", "object", "candidate_definition", "minimal_symbolic_map", "current_status"])}

## Basis Component Map

{markdown_table(basis_rows, ["component_id", "basis_component", "candidate_parent_symbol", "role", "unit_requirement", "current_status"])}

## Basis Verdict

{markdown_table(verdict_rows, ["verdict_id", "verdict", "reason", "promotion_requirement"])}

## WEP Data Probe Dry Run

{markdown_table(wep_rows, ["probe_id", "needed_object", "source_or_local_target", "current_status", "source_anchor"])}

## R10 Source Probe Dry Run

{markdown_table(r10_rows, ["probe_id", "needed_object", "fields_required", "current_status", "source_anchor"])}

## Decisions

{markdown_table(decision_rows_, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "gate", "gate_pass", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

1679 turns the fog into a labelled panel: six possible source-side leak slots, all currently nonclaim. The best next attack is not to chase numbers yet. It is to try to prove the source-current owner/no-source-only/no-marker theorem from the parent action. If that fails, the honest branch is finite coefficient contracts with units, signs, and source paths.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    attempt_rows = minimal_basis_attempt_rows()
    basis_rows = basis_component_rows()
    verdict_rows = basis_verdict_rows()
    wep_rows = wep_data_probe_rows()
    r10_rows = r10_source_probe_rows()
    decisions = decision_rows()
    claims = claim_gate_rows()
    next_rows = next_target_rows()

    write_csv(
        SOURCE_REGISTER,
        source_rows,
        ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1679", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        MINIMAL_BASIS_ATTEMPT,
        attempt_rows,
        ["branch_id", "attempt_id", "object", "candidate_definition", "minimal_symbolic_map", "parent_requirements", "current_status", "parent_signed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        BASIS_COMPONENT_MAP,
        basis_rows,
        ["branch_id", "component_id", "basis_component", "candidate_parent_symbol", "role", "unit_requirement", "source_anchor", "current_status", "parent_signed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        BASIS_VERDICT,
        verdict_rows,
        ["branch_id", "verdict_id", "verdict", "reason", "promotion_requirement", "parent_signed", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        WEP_DATA_PROBE,
        wep_rows,
        ["branch_id", "probe_id", "needed_object", "source_or_local_target", "fields_required", "current_status", "source_anchor", "probe_status", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        R10_SOURCE_PROBE,
        r10_rows,
        ["branch_id", "probe_id", "needed_object", "fields_required", "current_status", "source_anchor", "probe_status", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(DECISION, decisions, ["branch_id", "decision_id", "decision", "reason", "next_action", "valid_for_claim", "claim_allowed"])
    write_csv(CLAIM_GATE, claims, ["branch_id", "gate_id", "gate", "gate_pass", "status", "reason", "valid_for_claim", "claim_allowed"])
    write_csv(NEXT_TARGET, next_rows, ["branch_id", "next_target", "script", "objective", "success_condition", "why_next", "valid_for_claim", "claim_allowed"])

    copy_outputs()
    validation_rows = validate(source_rows, basis_rows, verdict_rows, wep_rows, r10_rows, decisions, claims, next_rows)
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, attempt_rows, basis_rows, verdict_rows, wep_rows, r10_rows, decisions, claims, next_rows, validation_rows)

    failed_rows = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAIL {failed_row['check_id']}: {failed_row['detail']}")
        raise SystemExit(1)
    print("1679 validation PASS")


if __name__ == "__main__":
    main()
