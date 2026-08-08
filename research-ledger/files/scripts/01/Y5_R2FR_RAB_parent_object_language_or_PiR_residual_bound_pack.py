from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1636"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1636-Y5-R2FR-RAB-parent-object-language-or-PiR-residual-bound-pack.md"

SOURCE_FILES = {
    "1635_doc": ROOT / "1635-Y5-R2FR-parent-matter-descent-signature-for-PiR-zero.md",
    "1635_validation": OUT / "P8_Y5_BRR545_1635_VALIDATION.csv",
    "1635_next": OUT / "P8_Y5_PARENT_QLOC_1635_NEXT_TARGET.csv",
    "1635_residual": OUT / "P8_Y5_PARENT_QLOC_1635_PIR_RESIDUAL_ENVELOPE.csv",
    "10_observer_map": ROOT / "10-observer-map-symplectic-contract.md",
    "1055_contract_doc": ROOT / "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md",
    "1055_contract_csv": OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
    "1049_operator_doc": ROOT / "1049-Y5-R10-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md",
    "1049_operator_csv": OUT / "P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv",
    "1048_vertex_doc": ROOT / "1048-Y5-R10-no-extra-F2-no-mass-vertex-parent-action-signature-or-alpha-mass-bound-matrix.md",
    "1048_vertex_csv": OUT / "P8_Y5_R10_1048_ALLOWED_FORBIDDEN_VERTEX_TABLE.csv",
    "1064_label_doc": ROOT / "1064-Y5-R10-parent-category-label-forgetting-proof-or-relative-weight-runner-fill.md",
    "1064_no_source_csv": OUT / "P8_Y5_R10_1064_NO_SOURCE_ONLY_SLOT_AUDIT.csv",
}

NEEDLES = {
    "1635_doc": [
        "NEXT_1636_RAB_PARENT_OBJECT_LANGUAGE_OR_PIR_RESIDUAL_BOUND_PACK",
        "Bulk chain-rule descent alone is not enough",
    ],
    "1635_validation": ["VAL1635_OVERALL", "PASS"],
    "1635_next": [
        "1636-Y5-R2FR-RAB-parent-object-language-or-PiR-residual-bound-pack.md",
        "do not claim Pi_R=0 from bulk descent alone",
    ],
    "1635_residual": ["Pi_R_abs_total", "TOTAL_TEMPLATE_NONCLAIM_MISSING_COMPONENTS"],
    "10_observer_map": ["R_AB = ln(T^2 S) = 2 ln(J_q).", "derive R_AB=0 from the parent theory"],
    "1055_contract_doc": ["Parent action contract candidate", "PAC1055_6_single_parent_action"],
    "1055_contract_csv": [
        "PAC1055_6_single_parent_action",
        "PAC1055_3_no_mixed_coefficients",
        "SCHEMA_WRITTEN_NOT_DERIVED_FROM_DEEPER_MTS",
    ],
    "1049_operator_doc": [
        "ordinary covariance and gauge symmetry are insufficient",
        "product/sequester parent functor is the clean theorem route",
    ],
    "1049_operator_csv": [
        "OCR1049_0_declared_parent_domain",
        "CONTRACT_EXACT_IF_ADOPTED_NOT_DERIVED",
        "OCR1049_4_naturalness_guard",
    ],
    "1048_vertex_doc": ["FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL", "VT1048_1_scalar_F2"],
    "1048_vertex_csv": ["VT1048_1_scalar_F2", "VT1048_3_mass_X", "blocks_claim"],
    "1064_label_doc": ["no-source-only-slot rule", "COUNTEREXAMPLE_SURVIVES"],
    "1064_no_source_csv": ["NSS1064_0_absent_slot", "NSS1064_2_relative_weight", "retained_nonclaim"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1636_SOURCE_REGISTER.csv"
OBJECT_LANGUAGE = OUT / "P8_Y5_PARENT_QLOC_1636_RAB_OBJECT_LANGUAGE_AUDIT.csv"
FORBIDDEN_SLOTS = OUT / "P8_Y5_PARENT_QLOC_1636_FORBIDDEN_RAB_SLOT_LEDGER.csv"
PIR_BOUND_PACK = OUT / "P8_Y5_PARENT_QLOC_1636_PIR_BOUND_INPUT_PACK.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1636_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1636_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1636_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1636_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    OBJECT_LANGUAGE,
    FORBIDDEN_SLOTS,
    PIR_BOUND_PACK,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    OBJECT_LANGUAGE,
    FORBIDDEN_SLOTS,
    PIR_BOUND_PACK,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]


def ensure_dirs() -> None:
    for path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def copy_outputs() -> None:
    paths = GENERATED + ([VALIDATION] if VALIDATION.exists() else [])
    for path in paths:
        for target_dir in [QUARANTINE, BRANCH_RESIDUALS]:
            shutil.copy2(path, target_dir / path.name)
    shutil.copy2(OBJECT_LANGUAGE, QUEUE / "JR1636_RAB_OBJECT_LANGUAGE_AUDIT_NONCLAIM.csv")
    shutil.copy2(PIR_BOUND_PACK, QUEUE / "JR1636_PIR_BOUND_INPUT_PACK_NONCLAIM.csv")
    shutil.copy2(NEXT_TARGET, QUEUE / "JR1636_NEXT_TARGET_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for key, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": key,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1636 parent object-language / Pi_R residual-bound input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def object_language_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OBJ1636_0_single_parent_action",
            "object_language_clause": "one parent variational object owns geometry, EM, matter, source, readout, and boundary before local tests",
            "minimal_form": "S_parent=S_geom[Phi]+S_hidden[Phi]+S_EM[q(Phi),A_Q,ell_EM]+sum_A S_A[Psi_A,q(Phi),A_Q,theta_A]+S_boundary[q(Phi)]",
            "current_status": "SCHEMA_WRITTEN_NOT_DERIVED_FROM_DEEPER_MTS",
            "buys_for_RAB": "prevents post-hoc insertion of independent R_AB matter/source/readout slots",
            "missing_for_derivation": "derive this grammar from MTS primitives, not as an after-the-fact discipline axiom",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OBJ1636_1_RAB_location",
            "object_language_clause": "R_AB is either absent/nonpropagating, or a proper representative coordinate in ker(Dq), not an observed matter argument",
            "minimal_form": "R_AB notin Arguments(S_matter,S_source,S_boundary) except through q(Phi), or R_AB=0 by parent constraint/no-pole",
            "current_status": "RAB_VERTICALITY_OBJECT_LANGUAGE_UNSIGNED",
            "buys_for_RAB": "turns matter descent from closure language into an evaluable parent theorem",
            "missing_for_derivation": "field-domain/equivalence relation showing R_AB is not coframe-visible physical data",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OBJ1636_2_allowed_operator_algebra",
            "object_language_clause": "all visible/local operators are generated from quotient data, representation constants, topological levels, and declared parent fields",
            "minimal_form": "Op_allowed subset Alg[q(Phi),Dq(Phi),F_parent,theta_rep,topological_classes]",
            "current_status": "CONTRACT_EXACT_IF_ADOPTED_NOT_DERIVED",
            "buys_for_RAB": "forbids arbitrary scalar functions of R_AB multiplying visible operators",
            "missing_for_derivation": "operator-classification theorem or symmetry/sequestration rule derived from parent action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OBJ1636_3_no_mixed_coefficients",
            "object_language_clause": "visible coefficients are quotient or representation data; Hom(hidden/R_AB, visible coefficients) is absent",
            "minimal_form": "Allowed[Coeff(O_vis)] subset O(Q_obs) x Theta_rep x Level_EM",
            "current_status": "POWERFUL_AXIOM_IF_UNSIGNED",
            "buys_for_RAB": "kills alpha/mass/clock/material-marker contributions to Pi_R",
            "missing_for_derivation": "hidden invariant algebra triviality or product/sequester functor proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OBJ1636_4_no_source_only_slot",
            "object_language_clause": "source functor forgets species/source labels and has no source-only weight w_A(R_AB)",
            "minimal_form": "T_total=sum_A 2/sqrt(-g_obs) delta S_A/delta g_obs, not sum_A w_A(R_AB)T_A",
            "current_status": "EXACT_CLAUSE_NOT_DERIVED",
            "buys_for_RAB": "removes relative source-weight contribution to Pi_R and WEP/PPN/R10 residuals",
            "missing_for_derivation": "parent category/grammar proof that w_A is not an allowed argument",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OBJ1636_5_boundary_language",
            "object_language_clause": "boundary/worldtube/readout terms depend only on quotient data or are proper/exact with zero local projection",
            "minimal_form": "S_boundary=S_boundary[q(Phi)] + exact/proper terms, with no B_R[R_AB] local source projection",
            "current_status": "BOUNDARY_OBJECT_LANGUAGE_MISSING",
            "buys_for_RAB": "closes the actual Pi_R loophole left by bulk chain-rule descent",
            "missing_for_derivation": "worldtube/boundary grammar or absolute boundary-tail coefficient rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "OBJ1636_6_verdict",
            "object_language_clause": "R_AB parent object-language theorem",
            "minimal_form": "OBJ1636_0 through OBJ1636_5 jointly derived from MTS primitives",
            "current_status": "OBJECT_LANGUAGE_CONTRACT_READY_NOT_DERIVED",
            "buys_for_RAB": "would promote Pi_R=0 -> Q_R=0 -> local R_AB sector GR-safe",
            "missing_for_derivation": "current evidence supports a contract, not a derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def forbidden_slot_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "slot_id": "SLOT1636_0_direct_RAB",
            "forbidden_slot": "S_matter[...,R_AB] independent of q(Phi)",
            "why_forbidden_if_theorem": "would create direct Pi_R bulk/source momentum",
            "current_status": "FORBIDDEN_BY_CONTRACT_NOT_PARENT_DERIVED",
            "fallback": "Pi_R_vertical_abs / direct_RAB coefficient row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "slot_id": "SLOT1636_1_frame_leak",
            "forbidden_slot": "A_R(R_AB)^2 e_obs or disformal/connection shadow frame",
            "why_forbidden_if_theorem": "would let rods/clocks/matter derivatives see representative data",
            "current_status": "FORBIDDEN_BY_GEOMETRY_STACK_CONTRACT_NOT_DERIVED",
            "fallback": "Pi_R_geometry_abs frame-leak coefficient row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "slot_id": "SLOT1636_2_visible_coefficients",
            "forbidden_slot": "f_R(R_AB)F^2, m_A(R_AB), y_A(R_AB), B_A(R_AB), nu_i(R_AB)",
            "why_forbidden_if_theorem": "would generate EM, mass, binding, and clock contributions to Pi_R",
            "current_status": "LEGAL_COUNTERTERMS_UNLESS_OPERATOR_RULE_SIGNED",
            "fallback": "Pi_R_constants_abs coefficient rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "slot_id": "SLOT1636_3_source_weight",
            "forbidden_slot": "w_A(R_AB)S_A or source-only reciprocal prefactor",
            "why_forbidden_if_theorem": "would preserve covariance while changing gravitational source normalization",
            "current_status": "RELATIVE_WEIGHT_COUNTERMODEL_SURVIVES",
            "fallback": "Pi_R_source_weight_abs / Delta_w_A rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "slot_id": "SLOT1636_4_boundary_tail",
            "forbidden_slot": "B_R[R_AB] worldtube/readout/local boundary projection",
            "why_forbidden_if_theorem": "bulk descent could still leave Pi_R boundary hair",
            "current_status": "BOUNDARY_SLOT_NOT_CLASSIFIED",
            "fallback": "Pi_R_boundary_abs tail row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "slot_id": "SLOT1636_5_readout_EFT",
            "forbidden_slot": "post-readout or radiative EFT re-entry of R_AB visible coefficients",
            "why_forbidden_if_theorem": "tree-level quotient silence would not survive effective/readout reduction",
            "current_status": "RADIATIVE_READOUT_CLOSURE_UNSIGNED",
            "fallback": "Pi_R_readout_abs residual row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def pir_bound_pack_rows() -> list[dict[str, object]]:
    required_columns = "coefficient_id;arena;projection;bound_or_value;units;source_path;equation_ref;valid_for_claim"
    return [
        {
            "branch_id": BRANCH_ID,
            "pack_id": "PIRBP1636_0_verticality",
            "residual_quantity": "Pi_R_vertical_abs",
            "required_input": "Dq[v_R] response or theorem-zero R_AB verticality certificate",
            "required_columns": required_columns,
            "current_status": "MISSING_VERTICALITY_CERTIFICATE_OR_BOUND",
            "priority": 1,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "PIRBP1636_1_geometry",
            "residual_quantity": "Pi_R_geometry_abs",
            "required_input": "frame/coframe/connection derivative response to R_AB",
            "required_columns": required_columns,
            "current_status": "MISSING_GEOMETRY_STACK_BOUND",
            "priority": 3,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "PIRBP1636_2_constants",
            "residual_quantity": "Pi_R_constants_abs",
            "required_input": "b_alpha_R, b_mA_R, b_mu_R, b_clock_R, marker/source-label coefficients or theorem zeros",
            "required_columns": required_columns,
            "current_status": "MISSING_CONSTANT_MARKER_ZERO_OR_VALUES",
            "priority": 4,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "PIRBP1636_3_source_weight",
            "residual_quantity": "Pi_R_source_weight_abs",
            "required_input": "Delta_w_A / source-only prefactor theorem zero or numeric vector",
            "required_columns": required_columns,
            "current_status": "MISSING_NO_SOURCE_WEIGHT_THEOREM",
            "priority": 2,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "PIRBP1636_4_boundary",
            "residual_quantity": "Pi_R_boundary_abs",
            "required_input": "worldtube/boundary projection zero certificate or absolute boundary-tail coefficient",
            "required_columns": required_columns,
            "current_status": "MISSING_BOUNDARY_ZERO_OR_ABSOLUTE_TAIL",
            "priority": 1,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "PIRBP1636_5_readout",
            "residual_quantity": "Pi_R_readout_abs",
            "required_input": "readout/EFT closure theorem or residual coefficient with arena projection",
            "required_columns": required_columns,
            "current_status": "MISSING_READOUT_RADIATIVE_CLOSURE",
            "priority": 5,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "pack_id": "PIRBP1636_6_qR_normalization",
            "residual_quantity": "q_R / Delta gamma",
            "required_input": "local normalization N_R mapping Pi_R or Q_R into q_R and Delta gamma",
            "required_columns": required_columns,
            "current_status": "MISSING_LOCAL_NORMALIZATION",
            "priority": 1,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1636_0_contract",
            "decision": "OBJECT_LANGUAGE_CONTRACT_IS_STRONG_ENOUGH_IF_DERIVED",
            "reason": "1055/1049 provide a parent grammar that would forbid the R_AB slots responsible for Pi_R",
            "next_action": "try to derive the no-independent-RAB-slot grammar from MTS primitives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1636_1_no_promotion",
            "decision": "OBJECT_LANGUAGE_NOT_DERIVED_CURRENT_CORPUS",
            "reason": "current evidence is a discipline contract/adoptable axiom, not a parent derivation",
            "next_action": "keep Pi_R=0, Q_R=0, local GR, and PPN claims blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1636_2_bound_pack",
            "decision": "PIR_RESIDUAL_BOUND_PACK_STAGED_NONCLAIM",
            "reason": "if the object-language proof fails, Pi_R_abs_total must be bounded component by component",
            "next_action": "fill first source-backed residual row only after units/projection/source path exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1636_3_next",
            "decision": "NEXT_1637_NO_INDEPENDENT_RAB_SLOT_GRAMMAR_OR_FIRST_PIR_BOUND_ROW",
            "reason": "the smallest proof target is absence of independent R_AB slots; fallback is first concrete bound row",
            "next_action": "attack no-independent-RAB-slot grammar before numeric residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1636_0_object_language",
            "claim": "parent object-language closes R_AB slots",
            "status": "BLOCKED",
            "blocker": "contract written but not derived from MTS primitives",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1636_1_PiR_zero",
            "claim": "Pi_R=0 theorem",
            "status": "BLOCKED",
            "blocker": "no-independent-RAB-slot and boundary grammar not signed",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1636_2_PiR_bound",
            "claim": "Pi_R residual bound score",
            "status": "BLOCKED",
            "blocker": "bound pack is schema only; no numeric/theorem-zero rows are valid",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1636_3_local_GR",
            "claim": "local GR/Newton/PPN recovery",
            "status": "BLOCKED",
            "blocker": "Q_R/q_R remains neither theorem-zero nor bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1637-Y5-R2FR-no-independent-RAB-slot-grammar-or-first-PiR-bound-row.md",
            "script": "scripts/Y5_R2FR_no_independent_RAB_slot_grammar_or_first_PiR_bound_row.py",
            "objective": "derive the parent grammar that excludes independent R_AB matter/source/boundary slots before variation; if it fails, stage the first source-backed Pi_R residual bound row with units and projection",
            "success_condition": "either the no-independent-RAB-slot theorem is parent-derived, or at least one Pi_R residual component has a source-ready nonclaim bound schema with no placeholders promoted",
            "guardrails": "do not adopt object-language as proof, do not claim Pi_R=0 from minimality, do not hide relative source weights in measured G, do not claim local GR until Q_R/q_R closes",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def all_claim_flags_false(paths: Iterable[Path]) -> bool:
    for path in paths:
        for row in csv_rows(path):
            for field in ["valid_for_claim", "claim_allowed", "score_allowed"]:
                if field in row and row[field] != "False":
                    return False
    return True


def validation_rows() -> list[dict[str, object]]:
    source_rows = source_register_rows()
    object_ids = {row["clause_id"] for row in object_language_rows()}
    slot_ids = {row["slot_id"] for row in forbidden_slot_rows()}
    pack_ids = {row["pack_id"] for row in pir_bound_pack_rows()}
    checks: list[tuple[str, bool, str]] = [
        (
            "VAL1636_0_sources_exist",
            all(row["path_exists"] for row in source_rows),
            "all cited 1636 source paths exist",
        ),
        (
            "VAL1636_1_needles_found",
            all(row["needles_found"] for row in source_rows),
            "all required 1636 source needles found",
        ),
        (
            "VAL1636_2_object_language_verdict",
            any(row["current_status"] == "OBJECT_LANGUAGE_CONTRACT_READY_NOT_DERIVED" for row in object_language_rows()),
            "object-language contract is not promoted as derivation",
        ),
        (
            "VAL1636_3_object_clause_coverage",
            object_ids
            == {
                "OBJ1636_0_single_parent_action",
                "OBJ1636_1_RAB_location",
                "OBJ1636_2_allowed_operator_algebra",
                "OBJ1636_3_no_mixed_coefficients",
                "OBJ1636_4_no_source_only_slot",
                "OBJ1636_5_boundary_language",
                "OBJ1636_6_verdict",
            },
            "object-language audit covers action, RAB location, operators, coefficients, source slots, and boundary",
        ),
        (
            "VAL1636_4_forbidden_slots",
            slot_ids
            == {
                "SLOT1636_0_direct_RAB",
                "SLOT1636_1_frame_leak",
                "SLOT1636_2_visible_coefficients",
                "SLOT1636_3_source_weight",
                "SLOT1636_4_boundary_tail",
                "SLOT1636_5_readout_EFT",
            },
            "forbidden slot ledger covers direct, frame, coefficient, source, boundary, and readout slots",
        ),
        (
            "VAL1636_5_bound_pack",
            pack_ids
            == {
                "PIRBP1636_0_verticality",
                "PIRBP1636_1_geometry",
                "PIRBP1636_2_constants",
                "PIRBP1636_3_source_weight",
                "PIRBP1636_4_boundary",
                "PIRBP1636_5_readout",
                "PIRBP1636_6_qR_normalization",
            },
            "Pi_R residual bound pack covers all 1635 residual pieces plus q_R normalization",
        ),
        (
            "VAL1636_6_claim_gates_closed",
            all(row["status"] == "BLOCKED" for row in claim_gate_rows()),
            "all 1636 claim gates remain blocked",
        ),
        (
            "VAL1636_7_next_target_selected",
            next_target_rows()[0]["next_target"]
            == "1637-Y5-R2FR-no-independent-RAB-slot-grammar-or-first-PiR-bound-row.md",
            "next target selects no-independent-RAB-slot grammar or first Pi_R bound row",
        ),
        (
            "VAL1636_8_csv_parse",
            all(len(csv_rows(path)) > 0 for path in GENERATED),
            "all generated 1636 CSVs parse",
        ),
        (
            "VAL1636_9_nonclaim_flags",
            all_claim_flags_false(CLAIM_CHECKED),
            "all 1636 generated decision rows remain nonclaim",
        ),
        (
            "VAL1636_10_branch_copies",
            all((QUARANTINE / path.name).exists() and (BRANCH_RESIDUALS / path.name).exists() for path in GENERATED),
            "branch/quarantine copies exist",
        ),
        (
            "VAL1636_11_queue_copies",
            all(
                path.exists()
                for path in [
                    QUEUE / "JR1636_RAB_OBJECT_LANGUAGE_AUDIT_NONCLAIM.csv",
                    QUEUE / "JR1636_PIR_BOUND_INPUT_PACK_NONCLAIM.csv",
                    QUEUE / "JR1636_NEXT_TARGET_NONCLAIM.csv",
                ]
            ),
            "acquisition queue nonclaim copies exist",
        ),
        (
            "VAL1636_12_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1636_13_formalization_untouched",
            not any(FORMALIZATION.rglob("*1636*")) if FORMALIZATION.exists() else True,
            "no 1636 outputs found under formalization-workbench",
        ),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1636_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1636 R_AB parent object-language or Pi_R residual bound-pack validation",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ") for column in columns]
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc() -> None:
    source_rows = csv_rows(SOURCE_REGISTER)
    object_rows = csv_rows(OBJECT_LANGUAGE)
    slot_rows = csv_rows(FORBIDDEN_SLOTS)
    pack_rows = csv_rows(PIR_BOUND_PACK)
    decisions = csv_rows(DECISION)
    gates = csv_rows(CLAIM_GATE)
    next_rows = csv_rows(NEXT_TARGET)
    validation = csv_rows(VALIDATION)

    content = f"""# 1636 — R_AB Parent Object-Language Or Pi_R Residual Bound Pack

**Private status:** nonclaim checkpoint. No `Pi_R=0`, `Q_R=0`, local-GR, Newton, PPN, WEP, clock, EM, orbital, or R10 pass is claimed.

## Verdict

The parent-action object-language route is strong enough in form, but it is still a contract, not a derivation. If MTS derives a single parent grammar where visible matter/source/boundary terms are generated only from quotient data and fixed representation/topological constants, then independent `R_AB` slots disappear and the 1635 `Pi_R=0` theorem can close.

But current evidence says:

```text
object-language contract ready != parent-derived theorem
```

So the honest fork is now exact:

```text
derive no independent R_AB slot  -> Pi_R=0 route can advance
fail to derive it                -> Pi_R_abs_total bound pack must be filled
```

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## R_AB Object-Language Audit

{markdown_table(object_rows, ["clause_id", "object_language_clause", "current_status", "buys_for_RAB", "missing_for_derivation"])}

## Forbidden R_AB Slot Ledger

{markdown_table(slot_rows, ["slot_id", "forbidden_slot", "why_forbidden_if_theorem", "current_status", "fallback"])}

## Pi_R Bound Input Pack

{markdown_table(pack_rows, ["pack_id", "residual_quantity", "required_input", "current_status", "priority"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "claim", "status", "blocker"])}

## Next Target

{markdown_table(next_rows, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    outputs = {
        SOURCE_REGISTER: source_register_rows(),
        OBJECT_LANGUAGE: object_language_rows(),
        FORBIDDEN_SLOTS: forbidden_slot_rows(),
        PIR_BOUND_PACK: pir_bound_pack_rows(),
        DECISION: decision_rows(),
        CLAIM_GATE: claim_gate_rows(),
        NEXT_TARGET: next_target_rows(),
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    copy_outputs()
    remove_pycache()
    write_csv(VALIDATION, validation_rows())
    copy_outputs()
    write_doc()
    remove_pycache()
    print(f"wrote {rel(DOC)}")
    print(f"validation {rel(VALIDATION)}")


if __name__ == "__main__":
    main()
