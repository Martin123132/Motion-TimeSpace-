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
QUARANTINE = MICROSCOPE / "quarantine" / "1676"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1676-Y5-R2FR-parent-source-object-language-and-no-marker-theorem.md"

SOURCE_FILES = {
    "1675_doc": ROOT / "1675-Y5-R2FR-constraint-first-Z-elimination-and-coframe-source-descent.md",
    "1675_validation": OUT / "P8_Y5_BRR545_1675_VALIDATION.csv",
    "1675_leaks": OUT / "P8_Y5_PARENT_QLOC_1675_SURVIVING_DQZ_LEAK_VECTOR_NONCLAIM.csv",
    "1066_object_language": OUT / "P8_Y5_R10_1066_OBJECT_LANGUAGE_TYPING_AUDIT.csv",
    "1066_source_scalar": OUT / "P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
    "1066_measure_quantum": OUT / "P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv",
    "1224_owner": OUT / "P8_Y5_R10_1224_OWNER_PROOF_CLAUSES.csv",
    "1224_obstruction": OUT / "P8_Y5_R10_1224_SOURCE_WEIGHT_OBSTRUCTION_LEDGER.csv",
    "1224_finite_contract": OUT / "P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv",
    "1224_product": OUT / "P8_Y5_R10_1224_SOURCE_WEIGHT_PRODUCT_LAW.csv",
    "1229_clause_audit": OUT / "P8_Y5_R10_1229_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv",
    "1229_counterexamples": OUT / "P8_Y5_R10_1229_SOURCE_COUPLING_COUNTEREXAMPLE_LEDGER.csv",
    "1415_owner_attempt": OUT / "P8_Y5_R10_1415_SOURCE_CURRENT_OWNER_ATTEMPT.csv",
    "1416_ban_attempt": OUT / "P8_Y5_R10_1416_SOURCE_SLOT_CURRENT_RESCALING_BAN_ATTEMPT.csv",
    "1416_first_rows": OUT / "P8_Y5_R10_1416_FIRST_RSOURCE_COEFFICIENT_ROW.csv",
    "1416_acceptance": OUT / "P8_Y5_R10_1416_RSOURCE_ROW_ACCEPTANCE_GATE.csv",
    "1225_formula": OUT / "P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv",
    "1225_acquisition": OUT / "P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv",
}

NEEDLES = {
    "1675_doc": ["source/coupling ownership", "1676-Y5-R2FR-parent-source-object-language-and-no-marker-theorem.md"],
    "1675_validation": ["VAL1675_OVERALL", "PASS"],
    "1675_leaks": ["LEAK1675_1_source_weight", "SOURCE_WEIGHT_OBSTRUCTION_ACTIVE"],
    "1066_object_language": ["OLT1066_6_verdict", "conditional_not_parent_derived"],
    "1066_source_scalar": ["SSE1066_5_verdict", "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED"],
    "1066_measure_quantum": ["FMQ1066_4_verdict", "NOT_PARENT_SIGNED"],
    "1224_owner": ["OWN1224_6_verdict", "SOURCE_WEIGHT_OWNER_PROOF_NOT_DERIVED"],
    "1224_obstruction": ["OBS1224_0_wA_action_multiplier", "ACTIVE_OBSTRUCTION"],
    "1224_finite_contract": ["FSW1224_1_delta_w", "MISSING_NUMERIC_PRIOR_WIDTH"],
    "1224_product": ["PROD1224_0_source_weight", "NOT_SCOREABLE"],
    "1229_clause_audit": ["CLC1229_8_verdict", "NOT_CLOSED"],
    "1229_counterexamples": ["CEX1229_0_action_multiplier", "ACTIVE"],
    "1415_owner_attempt": ["SCO1415_6_verdict", "SOURCE_CURRENT_OWNER_NOT_DERIVED_RSOURCE_TEMPLATE_REQUIRED"],
    "1416_ban_attempt": ["BAN1416_6_verdict", "BAN_NOT_PROVED_FIRST_RSOURCE_ROW_REQUIRED"],
    "1416_first_rows": ["RSC1416_0_qbar_source_weight", "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT"],
    "1416_acceptance": ["ACC1416_5_verdict", "ROW_SCHEMA_READY_VALUES_MISSING_NO_PASS"],
    "1225_formula": ["FORM1225_1_source_weight_product", "NOT_SCOREABLE"],
    "1225_acquisition": ["ACQ1225_5_delta_w", "MISSING_NUMERIC_PRIOR_WIDTH"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1676_SOURCE_REGISTER.csv"
OBJECT_LANGUAGE_THEOREM = OUT / "P8_Y5_PARENT_QLOC_1676_OBJECT_LANGUAGE_NO_MARKER_THEOREM_ATTEMPT.csv"
ACTION_CURRENT_OWNER_GATE = OUT / "P8_Y5_PARENT_QLOC_1676_ACTION_SCALE_CURRENT_OWNER_GATE.csv"
COUNTERMODEL_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1676_SOURCE_SLOT_COUNTERMODEL_LEDGER.csv"
FINITE_COEFFICIENT_PACK = OUT / "P8_Y5_PARENT_QLOC_1676_RSOURCE_COEFFICIENT_PACK_NONCLAIM.csv"
ARENA_PRODUCT_HANDOFF = OUT / "P8_Y5_PARENT_QLOC_1676_ARENA_PRODUCT_HANDOFF_NONCLAIM.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1676_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1676_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1676_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1676_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    OBJECT_LANGUAGE_THEOREM,
    ACTION_CURRENT_OWNER_GATE,
    COUNTERMODEL_LEDGER,
    FINITE_COEFFICIENT_PACK,
    ARENA_PRODUCT_HANDOFF,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    OBJECT_LANGUAGE_THEOREM,
    ACTION_CURRENT_OWNER_GATE,
    COUNTERMODEL_LEDGER,
    FINITE_COEFFICIENT_PACK,
    ARENA_PRODUCT_HANDOFF,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    OBJECT_LANGUAGE_THEOREM: [
        QUARANTINE / "OBJECT_LANGUAGE_NO_MARKER_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_object_language_no_marker_theorem_attempt_nonclaim_1676.csv",
        QUEUE / "JR1676_OBJECT_LANGUAGE_NO_MARKER_THEOREM_ATTEMPT_NONCLAIM.csv",
    ],
    FINITE_COEFFICIENT_PACK: [
        QUARANTINE / "RSOURCE_COEFFICIENT_PACK_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Rsource_coefficient_pack_nonclaim_1676.csv",
        QUEUE / "JR1676_RSOURCE_COEFFICIENT_PACK_NONCLAIM.csv",
    ],
    ARENA_PRODUCT_HANDOFF: [
        QUARANTINE / "ARENA_PRODUCT_HANDOFF_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_arena_product_handoff_nonclaim_1676.csv",
        QUEUE / "JR1676_ARENA_PRODUCT_HANDOFF_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1676.csv",
        QUEUE / "JR1676_NEXT_TARGET_NONCLAIM.csv",
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
    markers = ["MISSING_", "NOT_PARENT_SIGNED", "NOT_DERIVED", "NOT_CLOSED", "ACTIVE_OBSTRUCTION", "NOT_SCOREABLE", "BLOCKED"]
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
                "use_in_1676": "parent source object-language/no-marker theorem and finite source coefficient handoff",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def object_language_theorem_rows() -> list[dict[str, object]]:
    common = {
        "branch_id": BRANCH_ID,
        "theorem_name": "NoSourceOnlySpeciesSlot",
        "formal_statement": "If every parent matter argument is geometry, matter field, owned gauge/current data, measured representation constant, or one universal constant, and variation precedes readout/projection, then source-only species weights and material markers are inadmissible parent arguments.",
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    clauses = [
        (
            "NSS1676_0_parent_constructor_list",
            "Arg(S_parent) subset {geometry, matter fields, owned gauge/current data, measured representation constants, universal constants}.",
            "SSE1066_1 gives this as conditional object-language route.",
            "CONDITIONAL_TYPING_LEMMA_NOT_PARENT_DERIVED",
            "derive constructor list from MTS primitives rather than minimality preference",
        ),
        (
            "NSS1676_1_no_inert_source_scalar",
            "No w_A multiplying only active gravitational source strength with no other observable type.",
            "OLT1066_4 rejects inert source scalar by candidate typing only.",
            "REJECTED_BY_CANDIDATE_TYPING_NOT_PARENT_SIGNED",
            "prove source-only slots are syntactically impossible or retain qbar_source_weight",
        ),
        (
            "NSS1676_2_no_hidden_marker",
            "No material marker, hidden frame, source-only constant, or readout-only label may alter source strength.",
            "OLT1066_5 and CDA1023 keep marker/domain/boundary scalars active.",
            "HIDDEN_MARKER_OBSTRUCTION_ACTIVE",
            "ban marker morphisms or emit finite marker/readout coefficient rows",
        ),
        (
            "NSS1676_3_variation_before_readout",
            "Hilbert source current is varied before detector/readout/projector reduction.",
            "SSE1066_2 is clean if parent variation order and readout/EFT closure are signed.",
            "VARIATION_ORDER_NOT_PARENT_SIGNED",
            "derive readout order and no post-variation source weighting",
        ),
        (
            "NSS1676_4_naturality_limit",
            "Connected ordinary matter category would force natural positive source scalar to be common.",
            "SSE1066_3 says disconnected/simple components allow a family w_A.",
            "NATURALITY_HELPFUL_BUT_INSUFFICIENT",
            "do not rely on naturality alone; need parent grammar or finite coefficients",
        ),
        (
            "NSS1676_5_verdict",
            "NoSourceOnlySpeciesSlot theorem closes.",
            "SSE1066_5 and BAN1416_6 both say the ban is not parent-derived.",
            "NO_SOURCE_ONLY_SLOT_THEOREM_NOT_PROVED",
            "move to action-scale/current owner or finite R_source rows",
        ),
    ]
    return [
        {
            **common,
            "clause_id": clause_id,
            "required_clause": required_clause,
            "current_evidence": current_evidence,
            "status": status,
            "next_action": next_action,
            "clause_met": False,
            "parent_signed": False,
            "theorem_zero_adopted": False,
            "accepted_for_scoring": False,
            "score_ready": False,
        }
        for clause_id, required_clause, current_evidence, status, next_action in clauses
    ]


def action_current_owner_rows() -> list[dict[str, object]]:
    gates = [
        (
            "ACO1676_0_single_action_scale",
            "one universal parent action scale/hbar/normalization for all ordinary matter",
            "OWN1224_0 and FMQ1066_4 keep this NOT_PARENT_SIGNED.",
            "NOT_PARENT_SIGNED",
            "kills w_A S_A and species hbar counterexamples",
        ),
        (
            "ACO1676_1_source_current_owner",
            "one Hilbert source current is varied before source/readout selection",
            "OWN1224_1 is conditional, SCO1415_3 current owner is missing.",
            "CURRENT_OWNER_NOT_DERIVED",
            "kills current rescaling/source-marker residual",
        ),
        (
            "ACO1676_2_source_label_forgetting",
            "source labels are quotient-forgotten before local/material/readout projection",
            "OWN1224_2 is contract clause only.",
            "SOURCE_LABEL_FORGETTING_NOT_DERIVED",
            "kills source-only species scalar branch",
        ),
        (
            "ACO1676_3_measure_coframe_boundary",
            "measure/coframe/boundary descent cannot regenerate species weights",
            "OWN1224_4 and CLC1229_4/5 remain open.",
            "PARALLEL_DESCENT_GATE_OPEN",
            "prevents hidden Jacobian or edge weight",
        ),
        (
            "ACO1676_4_readout_projection",
            "tau_WEP/R10/Newton readout projection does not reweight source channels",
            "OWN1224_5 and 1225 acquisition table are missing official arrays/projection.",
            "READOUT_PROJECTION_NOT_DERIVED",
            "allows finite rows to become scoreable if theorem route fails",
        ),
        (
            "ACO1676_5_verdict",
            "source object-language and current owner close together",
            "OWN1224_6 says SOURCE_WEIGHT_OWNER_PROOF_NOT_DERIVED.",
            "SOURCE_WEIGHT_OWNER_PROOF_NOT_DERIVED",
            "retain R_source coefficient pack",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "current_evidence": evidence,
            "status": status,
            "effect_if_signed": effect,
            "gate_pass": False,
            "theorem_zero_adopted": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, evidence, status, effect in gates
    ]


def countermodel_rows() -> list[dict[str, object]]:
    rows = [
        (
            "CEX1676_0_action_multiplier",
            "S_matter=sum_A w_A S_A",
            "preserves isolated classical Euler-Lagrange equation form",
            "breaks universal Hilbert source normalization",
            "single action scale plus source-only slot ban",
        ),
        (
            "CEX1676_1_path_integral_scale",
            "species-dependent effective hbar/action measure",
            "can look classical in narrow limit",
            "breaks quantum/statistical/source normalization",
            "universal action-scale owner",
        ),
        (
            "CEX1676_2_measure_jacobian",
            "species-dependent measure/coframe/quotient Jacobian",
            "preserves bare syntax",
            "recreates effective source weight after descent",
            "species-blind measure/coframe/boundary theorem",
        ),
        (
            "CEX1676_3_readout_reweighting",
            "post-variation detector/source projection reweights species channels",
            "preserves bulk source equation",
            "breaks reported WEP/clock/orbital/R10 observables",
            "variation-before-readout plus projection kernel",
        ),
        (
            "CEX1676_4_disconnected_species",
            "natural family w_A on disconnected ordinary matter components",
            "preserves naturality inside each component",
            "breaks cross-species universality",
            "connected category or grammar ban",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": countermodel_id,
            "construction": construction,
            "what_it_preserves": preserves,
            "what_it_breaks": breaks,
            "defeated_by": defeated_by,
            "status": "ACTIVE_OBSTRUCTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for countermodel_id, construction, preserves, breaks, defeated_by in rows
    ]


def finite_coefficient_rows() -> list[dict[str, object]]:
    rows = [
        (
            "RSC1676_0_qbar_source_weight",
            "qbar_source_weight",
            "species/source-only gravitational prefactor or kappa_A sensitivity",
            "qbar_source_weight = partial_X ln kappa_A or equivalent source-only weight derivative",
            "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT",
            "WEP_source_charge;Newton_GM;R10;R11;local_GR",
        ),
        (
            "RSC1676_1_current_rescaling",
            "current_rescaling_residual",
            "source/test current normalization from J_A -> c_A J_A or beta_source,A marker",
            "delta_source_current = partial_X ln c_A or beta_source,A",
            "MISSING_CURRENT_OWNER_OR_COEFFICIENT",
            "WEP_source_charge;R10_source_side;Newton_GM;local_GR",
        ),
        (
            "RSC1676_2_marker_readout",
            "marker_readout_residual",
            "material marker, hidden frame, or readout-only source coefficient",
            "qbar_marker_Z or Pi_readout[source marker]",
            "MISSING_NO_MARKER_THEOREM_OR_COEFFICIENT",
            "clocks;EM;WEP;orbital;PPN",
        ),
        (
            "RSC1676_3_parent_basis",
            "R_source parent basis",
            "parent source-current coordinate basis and normalization",
            "declared basis X_I and source-current units",
            "MISSING_PARENT_COUPLING_BASIS",
            "all R_source arenas",
        ),
        (
            "RSC1676_4_verdict",
            "R_source coefficient pack",
            "source-only species/current-rescaling ban not proved, so finite rows remain explicit",
            "score-ready iff rows are theorem-zero or source-backed with units/signs/projections",
            "TEMPLATE_ONLY_VALUES_MISSING_NO_PASS",
            "WEP;Newton_GM;R10;R11;local_GR",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "definition": definition,
            "formula_or_bound": formula,
            "current_value": current_value,
            "units": "dimensionless or parent source-current normalization units",
            "observable_links": observable_links,
            "source_paths": "P8_Y5_R10_1416_FIRST_RSOURCE_COEFFICIENT_ROW.csv; P8_Y5_R10_1224_FINITE_SOURCE_WEIGHT_INPUT_CONTRACT.csv; P8_Y5_PARENT_QLOC_1675_SURVIVING_DQZ_LEAK_VECTOR_NONCLAIM.csv",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for row_id, quantity, definition, formula, current_value, observable_links in rows
    ]


def arena_product_rows() -> list[dict[str, object]]:
    rows = [
        (
            "APH1676_0_WEP",
            "WEP/MICROSCOPE source-weight product",
            "P_WEP_source_weight = abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15",
            "MISSING_DELTA_W_TAUPROJECTION_OR_THEOREM_ZERO",
            "Delta_w_TiPt;tau_WEP;source worldtube;readout arrays;no-cancellation guard",
        ),
        (
            "APH1676_1_Newton_GM",
            "Newton measured-GM/source normalization",
            "Delta(GM)/(GM) sourced by common-mode plus relative R_source terms",
            "MISSING_SOURCE_CURRENT_OWNER_AND_GAUSS_CALIBRATION",
            "source-current owner;Gauss/orbital calibration;single G_N normalization",
        ),
        (
            "APH1676_2_R10",
            "short-range fifth force source side",
            "alpha_source(lambda) includes qbar_source_weight/current_rescaling coefficients",
            "MISSING_R10_SOURCE_PROJECTION",
            "R10 field map;bound curve;source-current basis;lambda_X",
        ),
        (
            "APH1676_3_R11",
            "local non-EH operator/source residual",
            "operator/source residual includes source-weight/current-owner leakage",
            "MISSING_R11_OPERATOR_SOURCE_BASIS",
            "operator basis;current owner;projection coefficients",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "handoff_id": handoff_id,
            "arena": arena,
            "product_or_projection": product,
            "current_status": status,
            "required_inputs": required_inputs,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for handoff_id, arena, product, status, required_inputs in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        (
            "D1676_0_no_marker",
            "NO_SOURCE_ONLY_SLOT_NOT_PROVED",
            "object-language ban is sharp but still parent-grammar conditional",
            "do not set source-weight/marker coefficients to zero",
        ),
        (
            "D1676_1_owner",
            "ACTION_SCALE_CURRENT_OWNER_IS_NEXT_DERIVATION_TARGET",
            "classical EOM equivalence is too weak because Hilbert source and quantum/action scale change",
            "derive single action-scale/current owner or keep finite rows",
        ),
        (
            "D1676_2_finite_pack",
            "RSOURCE_COEFFICIENT_PACK_RETAINED_NONCLAIM",
            "qbar_source_weight, current_rescaling, marker_readout, and parent basis are now explicit rows",
            "fill only from theorem-zero or source-backed values",
        ),
        (
            "D1676_3_safety",
            "NO_GR_NEWTON_CLAIM",
            "source/coupling ownership remains open",
            "keep GR/Newton/source-side gates false",
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
        ("CG1676_0_object_language", "parent object-language excludes source-only species slots", False, "BLOCKED", "typing lemma not parent-derived"),
        ("CG1676_1_no_marker", "hidden markers/readout-only constants are theorem-banned", False, "BLOCKED", "marker obstruction active"),
        ("CG1676_2_action_scale", "single action-scale/hbar/measure owner is parent-signed", False, "BLOCKED", "action scale owner missing"),
        ("CG1676_3_current_owner", "single source-current owner is parent-signed", False, "BLOCKED", "current owner missing"),
        ("CG1676_4_finite_rows", "finite source coefficients are source-backed with units/projections", False, "BLOCKED", "coefficient pack template-only"),
        ("CG1676_5_local_GR", "GR/Newton source side follows", False, "BLOCKED", "source-weight countermodels remain active"),
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
            "next_target": "1677-Y5-R2FR-single-action-scale-current-owner-or-Rsource-acquisition.md",
            "script": "scripts/Y5_R2FR_single_action_scale_current_owner_or_Rsource_acquisition.py",
            "objective": "try to derive one parent action-scale/hbar/measure and one source-current owner; if not, turn qbar_source_weight/current_rescaling/marker_readout into source-ready finite acquisition rows",
            "success_condition": "source-weight coefficients become theorem-zero through parent ownership, or finite nonclaim rows gain source-backed values/units/projection requirements without any claim flags",
            "why_next": "1676 shows object-language typing alone is not enough; action-scale/current ownership is the decisive source-side derivation",
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
    theorem_rows = read_csv(OBJECT_LANGUAGE_THEOREM)
    owner_rows = read_csv(ACTION_CURRENT_OWNER_GATE)
    countermodel_rows_ = read_csv(COUNTERMODEL_LEDGER)
    coefficient_rows = read_csv(FINITE_COEFFICIENT_PACK)
    arena_rows = read_csv(ARENA_PRODUCT_HANDOFF)
    decision_rows_ = read_csv(DECISION)
    claim_rows = read_csv(CLAIM_GATE)
    next_rows = read_csv(NEXT_TARGET)

    sources_ok = all(bool_cell(row["exists"]) and bool_cell(row["needles_present"]) for row in source_rows)
    theorem_verdict = any(row["clause_id"] == "NSS1676_5_verdict" and row["status"] == "NO_SOURCE_ONLY_SLOT_THEOREM_NOT_PROVED" for row in theorem_rows)
    theorem_not_adopted = all(not bool_cell(row["theorem_zero_adopted"]) and not bool_cell(row["parent_signed"]) for row in theorem_rows)
    owner_verdict = any(row["gate_id"] == "ACO1676_5_verdict" and row["status"] == "SOURCE_WEIGHT_OWNER_PROOF_NOT_DERIVED" for row in owner_rows)
    countermodels_active = len(countermodel_rows_) == 5 and all(row["status"] == "ACTIVE_OBSTRUCTION" for row in countermodel_rows_)
    coefficient_pack_complete = {"qbar_source_weight", "current_rescaling_residual", "marker_readout_residual", "R_source parent basis", "R_source coefficient pack"} == {row["quantity"] for row in coefficient_rows}
    coefficient_pack_nonclaim = all(row["current_value"].startswith("MISSING_") or row["current_value"] == "TEMPLATE_ONLY_VALUES_MISSING_NO_PASS" for row in coefficient_rows)
    arena_handoff_complete = {"WEP/MICROSCOPE source-weight product", "Newton measured-GM/source normalization", "short-range fifth force source side", "local non-EH operator/source residual"} == {row["arena"] for row in arena_rows}
    decision_next = any(row["decision"] == "ACTION_SCALE_CURRENT_OWNER_IS_NEXT_DERIVATION_TARGET" for row in decision_rows_)
    claim_gate_safe = all(not bool_cell(row["gate_pass"]) and not bool_cell(row["claim_allowed"]) for row in claim_rows)
    next_target_selected = next_rows[0]["next_target"] == "1677-Y5-R2FR-single-action-scale-current-owner-or-Rsource-acquisition.md"
    csv_parse = all(path.exists() and len(read_csv(path)) >= 1 for path in GENERATED)
    branch_copies = all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_clean = not any(FORMALIZATION.rglob("*1676*")) if FORMALIZATION.exists() else True

    no_claim_flags = True
    blocked_not_ready = True
    for generated_path in CLAIM_CHECKED:
        for generated_row in read_csv(generated_path):
            if generated_row.get("valid_for_claim", "False").lower() == "true" or generated_row.get("claim_allowed", "False").lower() == "true":
                no_claim_flags = False
            if any(blocked_marker(value) for value in generated_row.values()):
                for claim_key in ["valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring", "prediction_source_backed", "valid_prediction_row"]:
                    if claim_key in generated_row and bool_cell(generated_row[claim_key]):
                        blocked_not_ready = False

    checks = [
        ("VAL1676_0_sources_exist", sources_ok, "all cited 1676 source paths exist and needles are present"),
        ("VAL1676_1_theorem_verdict", theorem_verdict, "no-source-only-slot theorem remains not proved"),
        ("VAL1676_2_theorem_not_adopted", theorem_not_adopted, "no object-language theorem-zero clause is adopted"),
        ("VAL1676_3_owner_verdict", owner_verdict, "source-weight owner proof remains not derived"),
        ("VAL1676_4_countermodels_active", countermodels_active, "source-side countermodels remain active"),
        ("VAL1676_5_coefficient_pack_complete", coefficient_pack_complete, "R_source coefficient pack includes source/current/marker/basis/verdict rows"),
        ("VAL1676_6_coefficient_pack_nonclaim", coefficient_pack_nonclaim, "R_source coefficient pack remains template-only/nonclaim"),
        ("VAL1676_7_arena_handoff_complete", arena_handoff_complete, "arena handoff covers WEP/Newton/R10/R11"),
        ("VAL1676_8_decision_next", decision_next, "decision selects action-scale/current-owner derivation"),
        ("VAL1676_9_claim_gate_safe", claim_gate_safe, "all claim gates keep source/local claims false"),
        ("VAL1676_10_no_claim_flags", no_claim_flags, "all generated rows keep claim flags false"),
        ("VAL1676_11_blocked_not_ready", blocked_not_ready, "no blocked/missing row is marked claim/scoring/source ready"),
        ("VAL1676_12_next_target_selected", next_target_selected, "next target selects action-scale/current owner or R_source acquisition"),
        ("VAL1676_13_csv_parse", csv_parse, "all generated 1676 CSVs parse"),
        ("VAL1676_14_branch_copies", branch_copies, "branch/quarantine/queue copies exist"),
        ("VAL1676_15_pycache_absent", pycache_absent, "scripts __pycache__ absent"),
        ("VAL1676_16_formalization_untouched", formalization_clean, "no 1676 outputs found under formalization-workbench"),
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
            "check_id": "VAL1676_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1676 parent source object-language/no-marker theorem validation",
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
    theorem_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    countermodel_rows_: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
    arena_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
) -> None:
    body = f"""# 1676 - Parent Source Object-Language And No-Marker Theorem

**Private status:** source/coupling derivation attempt plus finite nonclaim source-coefficient handoff. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

The theorem we need is now exact:

```text
NoSourceOnlySpeciesSlot:
Arg(S_parent) contains geometry, matter fields, owned gauge/current data,
measured representation constants, and universal constants only.
No w_A, source-only marker, hidden frame, or readout-only constant may alter
active gravitational source strength unless it is an explicit residual field.
```

That theorem is **not proved** in the current corpus. Object-language typing is a strong candidate, but it is not parent-derived; action-scale/current ownership is still missing; readout and measure can still regenerate source weights.

Therefore `qbar_source_weight`, `current_rescaling_residual`, `marker_readout_residual`, and the `R_source` parent basis stay as explicit nonclaim coefficient rows.

## Source Register

{markdown_table(source_rows, ["source_key", "source_path", "exists", "needles_present", "use_in_1676"])}

## Object-Language No-Marker Theorem Attempt

{markdown_table(theorem_rows, ["clause_id", "required_clause", "current_evidence", "status", "next_action"])}

## Action-Scale / Current-Owner Gate

{markdown_table(owner_rows, ["gate_id", "gate", "current_evidence", "status", "effect_if_signed"])}

## Countermodel Ledger

{markdown_table(countermodel_rows_, ["countermodel_id", "construction", "what_it_preserves", "what_it_breaks", "defeated_by"])}

## Rsource Coefficient Pack

{markdown_table(coefficient_rows, ["row_id", "quantity", "definition", "current_value", "observable_links"])}

## Arena Product Handoff

{markdown_table(arena_rows, ["handoff_id", "arena", "product_or_projection", "current_status", "required_inputs"])}

## Decisions

{markdown_table(decision_rows_, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim_rows, ["gate_id", "gate", "gate_pass", "status", "reason"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation_rows, ["check_id", "result", "detail"])}

## Working Interpretation

This is where the source side becomes engineering-clean. Locality and covariance do not kill source weights. Classical equation form does not kill source weights. The only clean derivation is one parent action-scale/current owner plus a typed object language with no source-only slots. If that closes, the GR/Newton source side gets serious. If not, the theory must carry finite source coefficients into WEP/Newton/R10/R11 tests.
"""
    DOC.write_text(body, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    theorem_rows = object_language_theorem_rows()
    owner_rows = action_current_owner_rows()
    countermodel_rows_ = countermodel_rows()
    coefficient_rows = finite_coefficient_rows()
    arena_rows = arena_product_rows()
    decision_rows_ = decision_rows()
    claim_rows = claim_gate_rows()
    next_rows = next_target_rows()

    write_csv(
        SOURCE_REGISTER,
        source_rows,
        ["branch_id", "source_key", "source_path", "exists", "needles_present", "required_needles", "use_in_1676", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        OBJECT_LANGUAGE_THEOREM,
        theorem_rows,
        ["branch_id", "theorem_name", "formal_statement", "clause_id", "required_clause", "current_evidence", "status", "next_action", "clause_met", "parent_signed", "theorem_zero_adopted", "accepted_for_scoring", "score_ready", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        ACTION_CURRENT_OWNER_GATE,
        owner_rows,
        ["branch_id", "gate_id", "gate", "current_evidence", "status", "effect_if_signed", "gate_pass", "theorem_zero_adopted", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        COUNTERMODEL_LEDGER,
        countermodel_rows_,
        ["branch_id", "countermodel_id", "construction", "what_it_preserves", "what_it_breaks", "defeated_by", "status", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        FINITE_COEFFICIENT_PACK,
        coefficient_rows,
        ["branch_id", "row_id", "quantity", "definition", "formula_or_bound", "current_value", "units", "observable_links", "source_paths", "accepted_for_scoring", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"],
    )
    write_csv(
        ARENA_PRODUCT_HANDOFF,
        arena_rows,
        ["branch_id", "handoff_id", "arena", "product_or_projection", "current_status", "required_inputs", "valid_for_claim", "claim_allowed"],
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
    write_doc(source_rows, theorem_rows, owner_rows, countermodel_rows_, coefficient_rows, arena_rows, decision_rows_, claim_rows, next_rows, validation_rows)

    failed_rows = [row for row in validation_rows if row["result"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    if failed_rows:
        for failed_row in failed_rows:
            print(f"FAIL {failed_row['check_id']}: {failed_row['detail']}")
        raise SystemExit(1)
    print("1676 validation PASS")


if __name__ == "__main__":
    main()
