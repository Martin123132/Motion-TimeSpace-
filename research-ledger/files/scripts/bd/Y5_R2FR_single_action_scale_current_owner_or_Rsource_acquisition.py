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
QUARANTINE = MICROSCOPE / "quarantine" / "1677"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1677-Y5-R2FR-single-action-scale-current-owner-or-Rsource-acquisition.md"

SOURCE_FILES = {
    "1676_doc": ROOT / "1676-Y5-R2FR-parent-source-object-language-and-no-marker-theorem.md",
    "1676_validation": OUT / "P8_Y5_BRR545_1676_VALIDATION.csv",
    "1676_rsource": OUT / "P8_Y5_PARENT_QLOC_1676_RSOURCE_COEFFICIENT_PACK_NONCLAIM.csv",
    "1676_arena": OUT / "P8_Y5_PARENT_QLOC_1676_ARENA_PRODUCT_HANDOFF_NONCLAIM.csv",
    "1055_parent_action": OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
    "1055_adoption": OUT / "P8_Y5_R10_1055_CONTRACT_ADOPTION_GATES.csv",
    "1066_measure": OUT / "P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv",
    "1224_owner": OUT / "P8_Y5_R10_1224_OWNER_PROOF_CLAUSES.csv",
    "1224_finite_contract": OUT / "P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv",
    "1224_product": OUT / "P8_Y5_R10_1224_SOURCE_WEIGHT_PRODUCT_LAW.csv",
    "1415_owner": OUT / "P8_Y5_R10_1415_SOURCE_CURRENT_OWNER_ATTEMPT.csv",
    "1416_ban": OUT / "P8_Y5_R10_1416_SOURCE_SLOT_CURRENT_RESCALING_BAN_ATTEMPT.csv",
    "1416_first_rows": OUT / "P8_Y5_R10_1416_FIRST_RSOURCE_COEFFICIENT_ROW.csv",
    "1416_acceptance": OUT / "P8_Y5_R10_1416_RSOURCE_ROW_ACCEPTANCE_GATE.csv",
    "1076_owner_gates": OUT / "P8_Y5_R10_1076_COUPLING_OWNER_GATES.csv",
    "1077_counterexamples": OUT / "P8_Y5_R10_1077_ZERO_THEOREM_COUNTEREXAMPLE_AUDIT.csv",
    "1084_readout_gate": OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv",
    "1409_readout_blockers": OUT / "P8_Y5_R10_1409_OFFICIAL_READOUT_BLOCKER_LEDGER.csv",
    "1225_formula": OUT / "P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv",
    "1225_acquisition": OUT / "P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv",
}

NEEDLES = {
    "1676_doc": ["NoSourceOnlySpeciesSlot", "1677-Y5-R2FR-single-action-scale-current-owner-or-Rsource-acquisition.md"],
    "1676_validation": ["VAL1676_OVERALL", "PASS"],
    "1676_rsource": ["RSC1676_0_qbar_source_weight", "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT"],
    "1676_arena": ["APH1676_0_WEP", "MISSING_DELTA_W_TAUPROJECTION_OR_THEOREM_ZERO"],
    "1055_parent_action": ["PAC1055_6_single_parent_action", "SCHEMA_WRITTEN_NOT_DERIVED_FROM_DEEPER_MTS"],
    "1055_adoption": ["ADG1055_3_source_label_forgetting", "CONDITIONAL_LEMMA_NOT_PARENT_SIGNED"],
    "1066_measure": ["FMQ1066_4_verdict", "NOT_PARENT_SIGNED"],
    "1224_owner": ["OWN1224_6_verdict", "SOURCE_WEIGHT_OWNER_PROOF_NOT_DERIVED"],
    "1224_finite_contract": ["FSW1224_1_delta_w", "MISSING_NUMERIC_PRIOR_WIDTH"],
    "1224_product": ["PROD1224_0_source_weight", "NOT_SCOREABLE"],
    "1415_owner": ["SCO1415_6_verdict", "SOURCE_CURRENT_OWNER_NOT_DERIVED_RSOURCE_TEMPLATE_REQUIRED"],
    "1416_ban": ["BAN1416_6_verdict", "BAN_NOT_PROVED_FIRST_RSOURCE_ROW_REQUIRED"],
    "1416_first_rows": ["RSC1416_1_current_rescaling", "MISSING_CURRENT_OWNER_OR_COEFFICIENT"],
    "1416_acceptance": ["ACC1416_5_verdict", "ROW_SCHEMA_READY_VALUES_MISSING_NO_PASS"],
    "1076_owner_gates": ["OWN1076_2_current_owner", "MISSING_CURRENT_OWNER"],
    "1077_counterexamples": ["CE1077_1_current_rescaling", "current owner"],
    "1084_readout_gate": ["RIG1084_0_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
    "1409_readout_blockers": ["ORB1409_7_verdict", "UA_KERNEL_BLOCKED"],
    "1225_formula": ["FORM1225_1_source_weight_product", "NOT_SCOREABLE"],
    "1225_acquisition": ["ACQ1225_5_delta_w", "MISSING_NUMERIC_PRIOR_WIDTH"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1677_SOURCE_REGISTER.csv"
ACTION_SCALE_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1677_SINGLE_ACTION_SCALE_OWNER_ATTEMPT.csv"
CURRENT_OWNER_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1677_SOURCE_CURRENT_OWNER_ATTEMPT.csv"
OWNER_VERDICT = OUT / "P8_Y5_PARENT_QLOC_1677_OWNER_PROOF_VERDICT.csv"
RSOURCE_ACQUISITION = OUT / "P8_Y5_PARENT_QLOC_1677_RSOURCE_ACQUISITION_ROWS_NONCLAIM.csv"
ARENA_PROJECTION = OUT / "P8_Y5_PARENT_QLOC_1677_ARENA_PROJECTION_REQUIREMENTS_NONCLAIM.csv"
FINITE_RUNNER_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1677_FINITE_RSOURCE_RUNNER_CONTRACT_NONCLAIM.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1677_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1677_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1677_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1677_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    ACTION_SCALE_ATTEMPT,
    CURRENT_OWNER_ATTEMPT,
    OWNER_VERDICT,
    RSOURCE_ACQUISITION,
    ARENA_PROJECTION,
    FINITE_RUNNER_CONTRACT,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    ACTION_SCALE_ATTEMPT,
    CURRENT_OWNER_ATTEMPT,
    OWNER_VERDICT,
    RSOURCE_ACQUISITION,
    ARENA_PROJECTION,
    FINITE_RUNNER_CONTRACT,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    OWNER_VERDICT: [
        QUARANTINE / "OWNER_PROOF_VERDICT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_owner_proof_verdict_nonclaim_1677.csv",
        QUEUE / "JR1677_OWNER_PROOF_VERDICT_NONCLAIM.csv",
    ],
    RSOURCE_ACQUISITION: [
        QUARANTINE / "RSOURCE_ACQUISITION_ROWS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Rsource_acquisition_rows_nonclaim_1677.csv",
        QUEUE / "JR1677_RSOURCE_ACQUISITION_ROWS_NONCLAIM.csv",
    ],
    ARENA_PROJECTION: [
        QUARANTINE / "ARENA_PROJECTION_REQUIREMENTS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_arena_projection_requirements_nonclaim_1677.csv",
        QUEUE / "JR1677_ARENA_PROJECTION_REQUIREMENTS_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1677.csv",
        QUEUE / "JR1677_NEXT_TARGET_NONCLAIM.csv",
    ],
}


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


def bool_cell(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    return value.strip().lower() == "true"


def blocked_marker(value: object) -> bool:
    value_text = str(value)
    markers = ["MISSING_", "NOT_DERIVED", "NOT_PARENT_SIGNED", "NOT_SCOREABLE", "BLOCKED", "TEMPLATE_ONLY"]
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
                "use_in_1677": "single action-scale/current owner attempt or R_source acquisition handoff",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def action_scale_attempt_rows() -> list[dict[str, object]]:
    rows = [
        (
            "ASO1677_0_parent_action",
            "one parent variational object owns geometry, EM, matter, source, and readout",
            "PAC1055_6 writes a schema but says it is not derived from deeper MTS.",
            "SCHEMA_WRITTEN_NOT_DERIVED_FROM_DEEPER_MTS",
            "derive S_parent from MTS primitives rather than use as private contract",
        ),
        (
            "ASO1677_1_single_scale",
            "one universal action scale/hbar/normalization for all ordinary matter species",
            "OWN1224_0 and FMQ1066_4 mark this NOT_PARENT_SIGNED.",
            "SINGLE_ACTION_SCALE_OWNER_NOT_DERIVED",
            "show species multipliers are gauge/quotient redundancy for Hilbert source and quantum measure",
        ),
        (
            "ASO1677_2_measure_jacobian",
            "species-blind measure/coframe/boundary descent cannot regenerate w_A",
            "FMQ1066_3 and OWN1224_4 keep the measure/coframe gate open.",
            "MEASURE_COFRAME_DESCENT_OPEN",
            "derive species-blind measure/coframe/boundary theorem",
        ),
        (
            "ASO1677_3_classical_guard",
            "classical equation-form equivalence is not enough to erase source weights",
            "FMQ1066_0/1 says w_A can preserve isolated EOM while changing Hilbert stress.",
            "CLASSICAL_EOM_SHORTCUT_REJECTED",
            "require source and quantum/action-scale ownership before theorem-zero",
        ),
        (
            "ASO1677_4_verdict",
            "single action-scale owner closes",
            "no source signs all ASO clauses together.",
            "ACTION_SCALE_OWNER_NOT_PROVED",
            "do not set Delta_w or qbar_source_weight to zero from action-scale route",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "required_clause": clause,
            "current_evidence": evidence,
            "status": status,
            "next_action": next_action,
            "clause_met": False,
            "parent_signed": False,
            "theorem_zero_adopted": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for attempt_id, clause, evidence, status, next_action in rows
    ]


def current_owner_attempt_rows() -> list[dict[str, object]]:
    rows = [
        (
            "SCO1677_0_current_functor",
            "one matter/source current functor owns source normalization before species/readout selection",
            "SCO1415_3 and OWN1076_2 mark current owner missing.",
            "MISSING_CURRENT_OWNER",
            "define current_id, Noether owner, charge-unit owner, and source normalization basis",
        ),
        (
            "SCO1677_1_source_label_forgetting",
            "source labels are forgotten before gravitational source coupling selection",
            "PAC1055_4/ADG1055_3 remain conditional lemma only.",
            "SOURCE_LABEL_FORGETTING_NOT_PARENT_SIGNED",
            "derive category/source functor that maps species data to total Hilbert current only",
        ),
        (
            "SCO1677_2_current_rescaling_guard",
            "J_A -> c_A J_A or beta_source,A marker is forbidden or explicit residual",
            "CE1077_1 and RSC1416_1 keep current rescaling active.",
            "CURRENT_RESCALING_COUNTERMODEL_ACTIVE",
            "ban current-rescaling slot or keep current_rescaling_residual row",
        ),
        (
            "SCO1677_3_source_worldtube",
            "source stress-current worldtube/profile is source-backed or theorem-reduced",
            "SCO1415_4, OWN1076_4, and ORB1409_3 keep source worldtube missing.",
            "MISSING_SOURCE_WORLDTUBE",
            "acquire source profile/composition/frame or derive common-mode source leg",
        ),
        (
            "SCO1677_4_readout_product",
            "source-current residual maps to WEP/Newton/R10/R11 with declared units and readout kernel",
            "SCO1415_5 and ORB1409_7 keep product convention/readout blocked.",
            "READOUT_PRODUCT_BLOCKED",
            "acquire official readout arrays or exact-equivalent reconstruction before scoring",
        ),
        (
            "SCO1677_5_verdict",
            "source-current owner closes",
            "SCO1415_6 says owner not derived and R_source template required.",
            "SOURCE_CURRENT_OWNER_NOT_DERIVED",
            "retain finite R_source acquisition rows",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "required_clause": clause,
            "current_evidence": evidence,
            "status": status,
            "next_action": next_action,
            "clause_met": False,
            "parent_signed": False,
            "theorem_zero_adopted": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for attempt_id, clause, evidence, status, next_action in rows
    ]


def owner_verdict_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "OWN1677_0_combined_owner",
            "claim": "Delta_w/qbar_source/current_rescaling/marker_readout theorem-zero from parent owner",
            "result": "OWNER_PROOF_NOT_DERIVED",
            "reason": "single action-scale owner, source-current functor, source-label forgetting, source worldtube, and readout product remain unsigned",
            "what_survives": "finite R_source acquisition rows for source weight, current rescaling, marker/readout, parent basis, and arena projections",
            "theorem_zero_adopted": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def rsource_acquisition_rows() -> list[dict[str, object]]:
    rows = [
        (
            "RSA1677_0_qbar_source_weight",
            "qbar_source_weight",
            "species/source-only gravitational prefactor or kappa_A sensitivity",
            "dimensionless derivative in parent source basis",
            "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT",
            "source-weight exclusion theorem or finite coefficient with sign/units/source path",
            "WEP;Newton_GM;R10;R11;local_GR",
        ),
        (
            "RSA1677_1_current_rescaling",
            "current_rescaling_residual",
            "source/test current normalization from J_A -> c_A J_A or beta_source,A marker",
            "dimensionless or parent current-normalization units",
            "MISSING_CURRENT_OWNER_OR_COEFFICIENT",
            "Noether/current owner theorem or finite c_A/beta_source,A coefficient with source path",
            "WEP;R10_source_side;Newton_GM;local_GR",
        ),
        (
            "RSA1677_2_marker_readout",
            "marker_readout_residual",
            "material marker, hidden frame, or readout-only source coefficient",
            "dimensionless readout/source-marker coefficient",
            "MISSING_NO_MARKER_THEOREM_OR_COEFFICIENT",
            "no-marker theorem or finite marker/readout coefficient with source path",
            "clocks;EM;WEP;orbital;PPN",
        ),
        (
            "RSA1677_3_parent_basis",
            "R_source parent basis",
            "parent source-current coordinate basis and normalization for all finite source rows",
            "declared parent basis units",
            "MISSING_PARENT_COUPLING_BASIS",
            "typed parent basis X_I and source-current coordinate normalization",
            "all R_source arenas",
        ),
        (
            "RSA1677_4_source_worldtube",
            "T_source^Earth(x)",
            "profile-weighted source stress/current in observed local frame",
            "stress/profile convention",
            "MISSING_SOURCE_PROFILE_WEIGHTING",
            "source composition/profile/worldtube with frame units and uncertainty",
            "WEP;Newton_GM;R10",
        ),
        (
            "RSA1677_5_readout_kernel",
            "K_MICROSCOPE/source readout kernel",
            "map from parent source residual to reported eta_AB channel",
            "eta per source-weight product",
            "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "official CMSM arrays or exact-equivalent reconstruction with masks/conventions",
            "WEP",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "definition": definition,
            "units": units,
            "current_value": current_value,
            "required_for_promotion": required,
            "observable_links": observables,
            "source_paths": "1676 R_source pack; 1224 finite source contract; 1416 first rows; 1084/1409 readout blockers",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, quantity, definition, units, current_value, required, observables in rows
    ]


def arena_projection_rows() -> list[dict[str, object]]:
    rows = [
        (
            "APR1677_0_WEP",
            "WEP/MICROSCOPE",
            "P_WEP_source_weight = abs(Delta_w_TiPt*tau_WEP) <= 2.8e-15",
            "Delta_w_TiPt;tau_WEP;official arrays/source worldtube/material tensor/no-cancellation guard",
            "NOT_SCOREABLE",
        ),
        (
            "APR1677_1_Newton",
            "Newton measured-GM/source normalization",
            "Delta(GM)/(GM) <= Pi_GM*(qbar_source_weight,current_rescaling,common-mode guard)",
            "source-current owner or Gauss/orbital calibration plus single G_N normalization",
            "MISSING_SOURCE_CURRENT_OWNER_AND_GAUSS_CALIBRATION",
        ),
        (
            "APR1677_2_R10",
            "short-range fifth force",
            "alpha_source(lambda) <= Pi_R10(lambda)*(qbar_source_weight,current_rescaling,marker_readout)",
            "R10 field map;source-current basis;lambda_X;bound curve",
            "MISSING_R10_SOURCE_PROJECTION",
        ),
        (
            "APR1677_3_R11",
            "local non-EH operator/source residual",
            "operator_source_residual <= Pi_R11*R_source_coefficients",
            "operator basis;current owner;projection coefficients",
            "MISSING_R11_OPERATOR_SOURCE_BASIS",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "projection_id": projection_id,
            "arena": arena,
            "projection_formula": formula,
            "required_inputs": required_inputs,
            "current_status": status,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for projection_id, arena, formula, required_inputs, status in rows
    ]


def finite_runner_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1677_0_finite_Rsource_runner_contract",
            "runner_status": "SCHEMA_READY_VALUES_MISSING",
            "input_rows": "RSA1677_0_qbar_source_weight;RSA1677_1_current_rescaling;RSA1677_2_marker_readout;RSA1677_3_parent_basis;RSA1677_4_source_worldtube;RSA1677_5_readout_kernel",
            "arena_rows": "APR1677_0_WEP;APR1677_1_Newton;APR1677_2_R10;APR1677_3_R11",
            "acceptance_rule": "claim remains false unless every coefficient/projection has numeric or theorem-zero value, units, source paths, and no MISSING/OFFICIAL_ARRAYS_NOT_IMPORTED/NOT_SCOREABLE markers",
            "current_blocker": "MISSING_COEFFICIENTS_AND_PROJECTIONS",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        (
            "D1677_0_action_scale",
            "ACTION_SCALE_OWNER_NOT_PROVED",
            "written parent action is a disciplined contract but not derived from deeper MTS primitives",
            "do not erase species/source weights by action-scale rhetoric",
        ),
        (
            "D1677_1_current_owner",
            "SOURCE_CURRENT_OWNER_NOT_DERIVED",
            "source current, current normalization, source worldtube, and readout product remain unsigned",
            "retain current_rescaling_residual and source rows",
        ),
        (
            "D1677_2_acquisition",
            "RSOURCE_ROWS_PROMOTED_TO_SOURCE_READY_NONCLAIM",
            "finite source rows now specify required units, source paths, and arena projections",
            "fill rows only from theorem-zero or source-backed values",
        ),
        (
            "D1677_3_safety",
            "NO_GR_NEWTON_CLAIM",
            "source side is not derived and finite rows are not score-ready",
            "keep GR/Newton/WEP/R10/R11 gates false",
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
    gates = [
        ("CG1677_0_action_scale", "single action-scale/hbar/measure owner is parent-signed", False, "BLOCKED", "parent action schema is not derived"),
        ("CG1677_1_current_owner", "single source-current owner is parent-signed", False, "BLOCKED", "current owner missing"),
        ("CG1677_2_source_weights", "qbar_source_weight/current_rescaling/marker rows are theorem-zero", False, "BLOCKED", "theorem-zero not adopted"),
        ("CG1677_3_finite_values", "R_source finite coefficients/projections are source-backed", False, "BLOCKED", "values/projections missing"),
        ("CG1677_4_WEP_Newton_R10", "WEP/Newton/R10/R11 source projections are score-ready", False, "BLOCKED", "official/projection inputs missing"),
        ("CG1677_5_local_GR", "GR/Newton source side follows", False, "BLOCKED", "owner proof and finite branch both incomplete"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_pass": gate_pass,
            "status": status,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, gate_pass, status, reason in gates
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1678-Y5-R2FR-Rsource-parent-basis-and-WEP-R10-projection-acquisition.md",
            "script": "scripts/Y5_R2FR_Rsource_parent_basis_and_WEP_R10_projection_acquisition.py",
            "objective": "fill or source-block the R_source parent basis, source-worldtube/readout kernel, WEP product, Newton-GM projection, and R10 source projection without claim flags",
            "success_condition": "finite source branch has either theorem-zero owner closure or source-backed nonclaim coefficient/projection rows with units, paths, and explicit remaining blockers",
            "why_next": "1677 shows the derivation route is not signed; the honest next move is finite source-side acquisition/projection plumbing",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)


def validate() -> list[dict[str, object]]:
    source_rows = read_csv(SOURCE_REGISTER)
    action_rows = read_csv(ACTION_SCALE_ATTEMPT)
    current_rows = read_csv(CURRENT_OWNER_ATTEMPT)
    verdict_rows = read_csv(OWNER_VERDICT)
    acquisition_rows = read_csv(RSOURCE_ACQUISITION)
    projection_rows = read_csv(ARENA_PROJECTION)
    runner_rows = read_csv(FINITE_RUNNER_CONTRACT)
    decision_rows_ = read_csv(DECISION)
    claim_rows = read_csv(CLAIM_GATE)
    next_rows = read_csv(NEXT_TARGET)

    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    action_verdict = any(row["attempt_id"] == "ASO1677_4_verdict" and row["status"] == "ACTION_SCALE_OWNER_NOT_PROVED" for row in action_rows)
    current_verdict = any(row["attempt_id"] == "SCO1677_5_verdict" and row["status"] == "SOURCE_CURRENT_OWNER_NOT_DERIVED" for row in current_rows)
    owner_not_adopted = verdict_rows[0]["result"] == "OWNER_PROOF_NOT_DERIVED" and not bool_cell(verdict_rows[0]["theorem_zero_adopted"])
    acquisition_complete = {"qbar_source_weight", "current_rescaling_residual", "marker_readout_residual", "R_source parent basis", "T_source^Earth(x)", "K_MICROSCOPE/source readout kernel"} == {row["quantity"] for row in acquisition_rows}
    acquisition_nonclaim = all(not bool_cell(row["score_ready"]) and not bool_cell(row["valid_for_claim"]) for row in acquisition_rows)
    projections_complete = {"WEP/MICROSCOPE", "Newton measured-GM/source normalization", "short-range fifth force", "local non-EH operator/source residual"} == {row["arena"] for row in projection_rows}
    runner_blocked = runner_rows[0]["runner_status"] == "SCHEMA_READY_VALUES_MISSING" and runner_rows[0]["current_blocker"] == "MISSING_COEFFICIENTS_AND_PROJECTIONS"
    decision_next = any(row["decision"] == "RSOURCE_ROWS_PROMOTED_TO_SOURCE_READY_NONCLAIM" for row in decision_rows_)
    claim_gate_safe = all(not bool_cell(row["gate_pass"]) and not bool_cell(row["claim_allowed"]) for row in claim_rows)
    next_target_selected = next_rows[0]["next_target"] == "1678-Y5-R2FR-Rsource-parent-basis-and-WEP-R10-projection-acquisition.md"
    csv_parse = all(path.exists() and len(read_csv(path)) >= 1 for path in GENERATED)
    branch_copies = all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1677*")) if FORMALIZATION.exists() else True

    no_claim_flags = True
    blocked_not_ready = True
    for generated_path in CLAIM_CHECKED:
        for generated_row in read_csv(generated_path):
            if generated_row.get("valid_for_claim", "False").lower() == "true" or generated_row.get("claim_allowed", "False").lower() == "true":
                no_claim_flags = False
            if any(blocked_marker(value) for value in generated_row.values()):
                for claim_key in ["valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring", "valid_prediction_row"]:
                    if claim_key in generated_row and bool_cell(generated_row[claim_key]):
                        blocked_not_ready = False

    checks = [
        ("VAL1677_0_sources_exist", sources_ok, "all cited 1677 source paths exist and needles are present"),
        ("VAL1677_1_action_verdict", action_verdict, "single action-scale owner remains not proved"),
        ("VAL1677_2_current_verdict", current_verdict, "source-current owner remains not derived"),
        ("VAL1677_3_owner_not_adopted", owner_not_adopted, "owner theorem-zero is not adopted"),
        ("VAL1677_4_acquisition_complete", acquisition_complete, "R_source acquisition rows cover source/current/marker/basis/worldtube/readout"),
        ("VAL1677_5_acquisition_nonclaim", acquisition_nonclaim, "R_source acquisition rows remain nonclaim/non-score-ready"),
        ("VAL1677_6_projection_complete", projections_complete, "arena projections cover WEP/Newton/R10/R11"),
        ("VAL1677_7_runner_blocked", runner_blocked, "finite R_source runner contract remains blocked by missing values/projections"),
        ("VAL1677_8_decision_next", decision_next, "decision promotes finite R_source rows to source-ready nonclaim"),
        ("VAL1677_9_claim_gate_safe", claim_gate_safe, "all claim gates keep local/source claims false"),
        ("VAL1677_10_no_claim_flags", no_claim_flags, "all generated rows keep claim flags false"),
        ("VAL1677_11_blocked_not_ready", blocked_not_ready, "no blocked/missing row is marked claim/scoring ready"),
        ("VAL1677_12_next_target_selected", next_target_selected, "next target selects R_source basis/projection acquisition"),
        ("VAL1677_13_csv_parse", csv_parse, "all generated 1677 CSVs parse"),
        ("VAL1677_14_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1677_15_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1677_16_formalization_untouched", formalization_clean, "no 1677 outputs found under formalization-workbench"),
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
            "check_id": "VAL1677_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1677 single action-scale/current owner or R_source acquisition validation",
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
    action_rows: list[dict[str, object]],
    current_rows: list[dict[str, object]],
    verdict_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    projection_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1677 - Single Action-Scale Current Owner Or Rsource Acquisition

**Private status:** owner derivation attempt plus source-ready nonclaim acquisition handoff. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

The clean derivation still does **not** close.

Single parent action-scale ownership would kill species action multipliers only if the parent action, hbar/action measure, Hilbert source current, measure/coframe descent, and readout order are all parent-signed. Current evidence does not sign that package.

So `qbar_source_weight`, `current_rescaling_residual`, `marker_readout_residual`, `R_source` parent basis, source worldtube, and readout kernel are retained as source-ready **nonclaim** acquisition rows.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1677"])}

## Single Action-Scale Owner Attempt

{markdown_table(action_rows, ["attempt_id", "required_clause", "current_evidence", "status", "next_action"])}

## Source-Current Owner Attempt

{markdown_table(current_rows, ["attempt_id", "required_clause", "current_evidence", "status", "next_action"])}

## Owner Verdict

{markdown_table(verdict_rows, ["verdict_id", "claim", "result", "reason", "what_survives"])}

## Rsource Acquisition Rows

{markdown_table(acquisition_rows, ["row_id", "quantity", "current_value", "required_for_promotion", "observable_links"])}

## Arena Projection Requirements

{markdown_table(projection_rows, ["projection_id", "arena", "projection_formula", "current_status", "required_inputs"])}

## Finite Runner Contract

{markdown_table(runner_rows, ["runner_id", "runner_status", "input_rows", "arena_rows", "current_blocker"])}

## Decisions

{markdown_table(decision_rows_, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "gate", "gate_pass", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This is a useful loss. The source side cannot be beaten by saying “one action” unless the one action is actually derived from MTS primitives and owns the current before readout. The finite branch is now more honest: it has named coefficients, units, arenas, and promotion rules. The next work should either fill the parent source basis/projections or prove they are theorem-zero.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    action_rows = action_scale_attempt_rows()
    current_rows = current_owner_attempt_rows()
    verdict_rows = owner_verdict_rows()
    acquisition_rows = rsource_acquisition_rows()
    projection_rows = arena_projection_rows()
    runner_rows = finite_runner_contract_rows()
    decision_rows_ = decision_rows()
    claim_rows = claim_gate_rows()
    next_rows = next_target_rows()

    write_csv(
        SOURCE_REGISTER,
        source_rows,
        ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1677", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        ACTION_SCALE_ATTEMPT,
        action_rows,
        ["branch_id", "attempt_id", "required_clause", "current_evidence", "status", "next_action", "clause_met", "parent_signed", "theorem_zero_adopted", "accepted_for_scoring", "score_ready", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        CURRENT_OWNER_ATTEMPT,
        current_rows,
        ["branch_id", "attempt_id", "required_clause", "current_evidence", "status", "next_action", "clause_met", "parent_signed", "theorem_zero_adopted", "accepted_for_scoring", "score_ready", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        OWNER_VERDICT,
        verdict_rows,
        ["branch_id", "verdict_id", "claim", "result", "reason", "what_survives", "theorem_zero_adopted", "accepted_for_scoring", "score_ready", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        RSOURCE_ACQUISITION,
        acquisition_rows,
        ["branch_id", "row_id", "quantity", "definition", "units", "current_value", "required_for_promotion", "observable_links", "source_paths", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        ARENA_PROJECTION,
        projection_rows,
        ["branch_id", "projection_id", "arena", "projection_formula", "required_inputs", "current_status", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        FINITE_RUNNER_CONTRACT,
        runner_rows,
        ["branch_id", "runner_id", "runner_status", "input_rows", "arena_rows", "acceptance_rule", "current_blocker", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        DECISION,
        decision_rows_,
        ["branch_id", "decision_id", "decision", "reason", "next_action", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        CLAIM_GATE,
        claim_rows,
        ["branch_id", "gate_id", "gate", "gate_pass", "status", "reason", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        NEXT_TARGET,
        next_rows,
        ["branch_id", "next_target", "script", "objective", "success_condition", "why_next", "valid_for_claim", "claim_allowed"],
    )

    copy_outputs()
    validation_rows = validate()
    write_csv(VALIDATION, validation_rows, ["check_id", "result", "detail", "valid_for_claim", "claim_allowed"])
    write_doc(source_rows, action_rows, current_rows, verdict_rows, acquisition_rows, projection_rows, runner_rows, decision_rows_, claim_rows, next_rows, validation_rows)

    failed_rows = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAIL {failed_row['check_id']}: {failed_row['detail']}")
        raise SystemExit(1)
    print("1677 validation PASS")


if __name__ == "__main__":
    main()
