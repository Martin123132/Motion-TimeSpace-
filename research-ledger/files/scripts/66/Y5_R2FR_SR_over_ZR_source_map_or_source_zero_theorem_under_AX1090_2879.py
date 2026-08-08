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

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2879-Y5-R2FR-SR-over-ZR-source-map-or-source-zero-theorem-under-AX1090.md"

SRC_2878_DOC = ROOT / "2878-Y5-R2FR-qReff-normalization-pack-derivation-or-raw-coefficient-intake-under-AX1090.md"
SRC_2878_NEXT = RESIDUALS / "P8_Y5_R2FR_2878_NEXT_TARGET.csv"
SRC_2878_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2878_VALIDATION.csv"
SRC_2878_RAW_QUEUE = RESIDUALS / "P8_Y5_R2FR_2878_RAW_COEFFICIENT_INTAKE_QUEUE.csv"
SRC_2878_DERIVATION = RESIDUALS / "P8_Y5_R2FR_2878_QREFF_NORMALIZATION_DERIVATION.csv"

SRC_2839_KERNEL = RESIDUALS / "P8_Y5_R2FR_2839_GREEN_KERNEL_NORMALIZATION.csv"
SRC_2839_SELECTOR = RESIDUALS / "P8_Y5_R2FR_2839_FIRST_SOURCE_ROW_SELECTOR.csv"
SRC_2840_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2840_NORMALIZATION_PACK_CONTRACT.csv"
SRC_2840_ZERO = RESIDUALS / "P8_Y5_R2FR_2840_PARENT_ZERO_CERTIFICATE_AUDIT.csv"
SRC_2855_DRAFT = RESIDUALS / "P8_Y5_R2FR_2855_PARENT_SOURCE_EQUATION_DRAFT.csv"
SRC_2864_AUDIT = RESIDUALS / "P8_Y5_R2FR_2864_QREFF_PARENT_NORMALIZATION_AUDIT.csv"
SRC_2864_EVIDENCE = RESIDUALS / "P8_Y5_R2FR_2864_QREFF_SOURCE_EVIDENCE_SCAN.csv"
SRC_2864_BLOCKERS = RESIDUALS / "P8_Y5_R2FR_2864_QREFF_BLOCKER_LEDGER.csv"
SRC_2872_LAW = RESIDUALS / "P8_Y5_R2FR_2872_QREFF_SOURCE_EQUATION_AUDIT.csv"
SRC_2872_TEMPLATE = RESIDUALS / "P8_Y5_R2FR_2872_QREFF_FINITE_ROW_TEMPLATE_NONCLAIM.csv"
SRC_1625_BUILDER = RESIDUALS / "P8_Y5_PARENT_QLOC_1625_FINITE_ZR_PRIOR_ROW_BUILDER.csv"
SRC_1869_SCHEMA = RESIDUALS / "P8_Y5_PARENT_QLOC_1869_COMPONENT_INPUT_SCHEMA.csv"
SRC_2169_SCHEMA = RESIDUALS / "P8_Y5_PARENT_QLOC_2169_FINITE_LOCAL_COMPONENT_SCHEMA.csv"
SRC_OWNER_CONTRACT = RESIDUALS / "P8_source_owner_parent_action_terms_CONTRACT.csv"
SRC_CURRENT_CONTRACT = RESIDUALS / "P8_source_current_Ward_universality_CONTRACT.csv"
SRC_WARD_CONTRACT = RESIDUALS / "P8_Ward_source_owner_identity_CONTRACT.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2879_SOURCE_REGISTER.csv",
    "decomposition": RESIDUALS / "P8_Y5_R2FR_2879_SRZR_SOURCE_MAP_DECOMPOSITION.csv",
    "zero_audit": RESIDUALS / "P8_Y5_R2FR_2879_SOURCE_ZERO_THEOREM_AUDIT.csv",
    "evidence": RESIDUALS / "P8_Y5_R2FR_2879_PARENT_MATTER_READOUT_EVIDENCE_REVIEW.csv",
    "fill": RESIDUALS / "P8_Y5_R2FR_2879_SRZR_FILL_ATTEMPT.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2879_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2879_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2879_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2879_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2879_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2879_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "decomposition_copy": LOCAL_BOUNDS / "RAB_SRZR_SOURCE_MAP_DECOMPOSITION_2879_NONCLAIM.csv",
    "zero_copy": SOURCE_WEIGHT / "RAB_SRZR_SOURCE_ZERO_AUDIT_2879_NONCLAIM.csv",
    "fill_copy": BETA_DOCS / "RAB_SRZR_FILL_ATTEMPT_2879_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2879_ZR_MR2_operator_normalization_NEXT.csv",
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
        ("SRC2879_0_2878_doc", SRC_2878_DOC, "Status: `Y5_R2FR_2878_qReff_normalization_pack_algebra_derived_raw_queue_written_SRZR_2879_next`;S_R/Z_R", "2878 handoff doc"),
        ("SRC2879_1_2878_next", SRC_2878_NEXT, "NEXT2878_0_2879", "2878 selected this target"),
        ("SRC2879_2_2878_validation", SRC_2878_VALIDATION, "VAL2878_OVERALL", "2878 validation"),
        ("SRC2879_3_2878_raw_queue", SRC_2878_RAW_QUEUE, "RAW2878_2_SRZR", "S_R/Z_R selected queue row"),
        ("SRC2879_4_2878_derivation", SRC_2878_DERIVATION, "DER2878_3_compact_charge", "q_R_eff compact charge law"),
        ("SRC2879_5_2839_kernel", SRC_2839_KERNEL, "KER2839_0_static_operator;KER2839_1_normalized_operator;KER2839_4_compact_body", "static source decomposition and normalized Green law"),
        ("SRC2879_6_2839_selector", SRC_2839_SELECTOR, "SEL2839_3_JR_PiR_readout;SEL2839_4_projection", "source terms and projection remain required"),
        ("SRC2879_7_2840_contract", SRC_2840_CONTRACT, "PACK2840_1_amplitude;PACK2840_5_source", "normalization source contract"),
        ("SRC2879_8_2840_zero", SRC_2840_ZERO, "PZ2840_2_source_zero;PZ2840_3_boundary_zero;PZ2840_4_readout_zero;PZ2840_5_joint_certificate", "source-zero theorem blockers"),
        ("SRC2879_9_2855_draft", SRC_2855_DRAFT, "PEQ2855_1_R_source;PEQ2855_3_amp_current_identity", "draft source equation only"),
        ("SRC2879_10_2864_audit", SRC_2864_AUDIT, "NORM2864_1_source_integral;NORM2864_2_source_zero;NORM2864_6_verdict", "parent normalization audit"),
        ("SRC2879_11_2864_evidence", SRC_2864_EVIDENCE, "EVID2864_1_compact_body_charge;EVID2864_5_parent_equation_hunt", "q_R_eff evidence scan"),
        ("SRC2879_12_2864_blockers", SRC_2864_BLOCKERS, "BLOCK2864_2_SOURCE_EQUATION;BLOCK2864_3_SR_ZR", "source equation and S_R/Z_R blockers"),
        ("SRC2879_13_2872_law", SRC_2872_LAW, "LAW2872_1_compact_source_charge;LAW2872_6_verdict", "source law acceptance remains blocked"),
        ("SRC2879_14_2872_template", SRC_2872_TEMPLATE, "TPL2872_2_SRZR_source_density", "S_R/Z_R live-row template rejected"),
        ("SRC2879_15_1625_builder", SRC_1625_BUILDER, "PB1625_2_JR", "J_R source-current prior builder"),
        ("SRC2879_16_1869_schema", SRC_1869_SCHEMA, "FLC1869_6_JR", "older finite local component schema"),
        ("SRC2879_17_2169_schema", SRC_2169_SCHEMA, "FLC2169_6_JR", "later finite local component schema"),
        ("SRC2879_18_owner_contract", SRC_OWNER_CONTRACT, "A1_source_owner_decomposition;A2_no_retained_source_constraint;A6_selector_blind_source_action", "parent source owner terms"),
        ("SRC2879_19_current_contract", SRC_CURRENT_CONTRACT, "SC1_Hilbert_source_definition;SC4_no_nonHilbert_source_current;SC7_no_time_range_radial_species_drift", "source-current Ward contract"),
        ("SRC2879_20_ward_contract", SRC_WARD_CONTRACT, "C1_exact_owner_decomposition;C6_no_range_or_radial_source_hair", "Ward/source-owner contract"),
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


def decomposition_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "map_id": "MAP2879_0_source_normal_form",
            "branch_id": BRANCH_ID,
            "quantity": "S_R/Z_R",
            "formal_statement": "S_R/Z_R=(J_R+Pi_R+R_readout)/Z_R in the same static operator normalization as E_R^finite",
            "derived_from": "E_R^finite=-Div(Z_R Grad delta_R)+M_R^2 delta_R+S_R=0; S_R:=J_R+Pi_R+R_readout",
            "current_status": "FORMAL_DECOMPOSITION_ONLY",
            "missing_for_live_row": "component source functionals J_R, Pi_R, R_readout and same-normalization finite Z_R",
            "source_path": str(SRC_2839_KERNEL),
            "source_anchor": "KER2839_0_static_operator",
            "parent_signed": False,
            "accepted_source_map": False,
        },
        {
            "map_id": "MAP2879_1_matter_current",
            "branch_id": BRANCH_ID,
            "quantity": "J_R/Z_R",
            "formal_statement": "J_R is the residual-channel matter/source current obtained by varying the parent matter/source action with respect to delta_R after fixing the observed coframe convention",
            "derived_from": "standard variational source-current slot, not yet a concrete MTS functional",
            "current_status": "MISSING_MATTER_VARIATION",
            "missing_for_live_row": "explicit S_matter[Psi,e_obs,delta_R or q] dependence, universal coupling, units and source anchor",
            "source_path": str(SRC_1625_BUILDER),
            "source_anchor": "PB1625_2_JR",
            "parent_signed": False,
            "accepted_source_map": False,
        },
        {
            "map_id": "MAP2879_2_projector_bulk_current",
            "branch_id": BRANCH_ID,
            "quantity": "Pi_R/Z_R",
            "formal_statement": "Pi_R is the bulk/projector/domain/improvement source that remains after owned divergences are separated from the parent Ward identity",
            "derived_from": "source-owner decomposition contract",
            "current_status": "MISSING_OWNER_DECOMPOSITION",
            "missing_for_live_row": "formula-level K_owner, q_retained=0 proof or retained finite coefficient row, and boundary flux policy",
            "source_path": str(SRC_OWNER_CONTRACT),
            "source_anchor": "A1_source_owner_decomposition",
            "parent_signed": False,
            "accepted_source_map": False,
        },
        {
            "map_id": "MAP2879_3_readout_current",
            "branch_id": BRANCH_ID,
            "quantity": "R_readout/Z_R",
            "formal_statement": "R_readout is any source regenerated by the coframe/readout/arena projection after the residual variable is mapped into observables",
            "derived_from": "readout-zero and arena-projection blockers",
            "current_status": "MISSING_READOUT_SILENCE_OR_KERNEL",
            "missing_for_live_row": "proof readout cannot regenerate R_AB, or explicit tau_R10/tau_PPN/tau_clock/tau_orbital kernels",
            "source_path": str(SRC_2840_ZERO),
            "source_anchor": "PZ2840_4_readout_zero",
            "parent_signed": False,
            "accepted_source_map": False,
        },
        {
            "map_id": "MAP2879_4_denominator",
            "branch_id": BRANCH_ID,
            "quantity": "Z_R",
            "formal_statement": "Z_R must be finite, nonzero and same-normalized with the static Green equation before any numerator source is meaningful",
            "derived_from": "normalization pack and operator rows",
            "current_status": "MISSING_Z_R_SAME_NORMALIZATION",
            "missing_for_live_row": "parent quadratic-action/Hessian coefficient or theorem-zero route with declared units",
            "source_path": str(SRC_2878_RAW_QUEUE),
            "source_anchor": "RAW2878_0_ZR",
            "parent_signed": False,
            "accepted_source_map": False,
        },
        {
            "map_id": "MAP2879_5_compact_charge",
            "branch_id": BRANCH_ID,
            "quantity": "q_R_eff",
            "formal_statement": "q_R_eff=-int_W S_R/Z_R d^3x, with boundary_homogeneous kept separately until zero/boundary theorem closes",
            "derived_from": "normalized Green kernel compact-body solution",
            "current_status": "SOURCE_MAP_NOT_FILLED",
            "missing_for_live_row": "finite S_R/Z_R, compact support/worldtube, H_R boundary class, units and source path",
            "source_path": str(SRC_2839_KERNEL),
            "source_anchor": "KER2839_4_compact_body",
            "parent_signed": False,
            "accepted_source_map": False,
        },
    ]
    return [add_common(row) for row in rows]


def source_zero_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "zero_id": "ZERO2879_0_JR_matter_silence",
            "target": "J_R=0",
            "required_clause": "actual R_AB/delta_R direction is invisible to matter/source after observed coframe and measured source convention are fixed",
            "current_evidence": "PZ2840_2 says source zero is not signed; PB1625_2_JR remains missing source-backed input",
            "status": "NOT_SIGNED",
            "blocker": "MISSING_JR_MATTER_DESCENT_ZERO_THEOREM",
            "source_path": str(SRC_2840_ZERO),
            "source_anchor": "PZ2840_2_source_zero",
            "parent_signed": False,
            "theorem_zero": False,
        },
        {
            "zero_id": "ZERO2879_1_PiR_owner_silence",
            "target": "Pi_R=0",
            "required_clause": "bulk/projector/domain/improvement terms are exact owned divergences with zero compact exterior flux or are absent",
            "current_evidence": "source-owner contract says exact owner decomposition and no-retained-source constraint are not parent-derived",
            "status": "NOT_SIGNED",
            "blocker": "MISSING_OWNER_DECOMPOSITION_AND_ZERO_FLUX",
            "source_path": str(SRC_OWNER_CONTRACT),
            "source_anchor": "A1_source_owner_decomposition;A2_no_retained_source_constraint",
            "parent_signed": False,
            "theorem_zero": False,
        },
        {
            "zero_id": "ZERO2879_2_readout_silence",
            "target": "R_readout=0",
            "required_clause": "readout/coarse-graining/arena projection cannot regenerate an R_AB source channel",
            "current_evidence": "PZ2840_4 marks readout-zero not signed and SEL2839_4 keeps arena projection required",
            "status": "NOT_SIGNED",
            "blocker": "MISSING_READOUT_ZERO_OR_ARENA_KERNEL",
            "source_path": str(SRC_2840_ZERO),
            "source_anchor": "PZ2840_4_readout_zero",
            "parent_signed": False,
            "theorem_zero": False,
        },
        {
            "zero_id": "ZERO2879_3_boundary_silence",
            "target": "boundary_homogeneous/no-hair silence",
            "required_clause": "no R_AB edge charge, no homogeneous exterior mode and no hidden boundary source",
            "current_evidence": "PZ2840_3 boundary-zero and PACK2840_3 boundary class are not signed",
            "status": "NOT_SIGNED",
            "blocker": "MISSING_BOUNDARY_NO_HAIR_CLASS",
            "source_path": str(SRC_2840_ZERO),
            "source_anchor": "PZ2840_3_boundary_zero",
            "parent_signed": False,
            "theorem_zero": False,
        },
        {
            "zero_id": "ZERO2879_4_ZR_regular_denominator",
            "target": "Z_R finite same-normalized denominator",
            "required_clause": "Z_R exists, is finite/nonzero or has a legal zero route, and shares the Green-kernel normalization",
            "current_evidence": "2878 raw queue leaves Z_R missing; 2864 audit blocks ell_R or Z_R/M_R^2 source",
            "status": "NOT_SIGNED",
            "blocker": "MISSING_ZR_OPERATOR_NORMALIZATION",
            "source_path": str(SRC_2878_RAW_QUEUE),
            "source_anchor": "RAW2878_0_ZR",
            "parent_signed": False,
            "theorem_zero": False,
        },
        {
            "zero_id": "ZERO2879_5_joint_source_zero",
            "target": "S_R/Z_R=0 and q_R_eff=0",
            "required_clause": "all numerator components vanish and denominator/operator convention is parent-owned in one theorem",
            "current_evidence": "no component zero theorem is signed, and NORM2864_2 rejects source-zero derivation",
            "status": "NOT_CLOSED",
            "blocker": "SOURCE_ZERO_THEOREM_REJECTED_FOR_CURRENT_CORPUS",
            "source_path": str(SRC_2864_AUDIT),
            "source_anchor": "NORM2864_2_source_zero",
            "parent_signed": False,
            "theorem_zero": False,
        },
    ]
    return [add_common(row) for row in rows]


def evidence_review_rows() -> list[dict[str, Any]]:
    rows = [
        ("EVID2879_0_symbolic_decomposition", "S_R := J_R+Pi_R+R_readout exists", "SYMBOLIC_ONLY", "source-intake row defines components but gives no functional, value, units or parent source path", SRC_2839_KERNEL, "KER2839_0_static_operator"),
        ("EVID2879_1_compact_charge", "q_R_eff=-int S_R/Z_R d^3x exists", "CONTRACT_ONLY", "compact charge law is exact but unfilled", SRC_2839_KERNEL, "KER2839_4_compact_body"),
        ("EVID2879_2_source_zero", "J_R=0 attempted", "NOT_SIGNED", "matter/source invisibility has not been proved", SRC_2840_ZERO, "PZ2840_2_source_zero"),
        ("EVID2879_3_readout_zero", "R_readout=0 attempted", "NOT_SIGNED", "readout/coarse-graining silence has not been proved", SRC_2840_ZERO, "PZ2840_4_readout_zero"),
        ("EVID2879_4_parent_source_equation", "L_R delta_R=J_R draft", "DRAFT_NOT_PARENT_DERIVED", "source equation request exists but is not an accepted parent derivation", SRC_2855_DRAFT, "PEQ2855_1_R_source"),
        ("EVID2879_5_SRZR_blocker", "S_R/Z_R row", "MISSING_SOURCE_DENSITY_NORMALIZATION", "source density over same worldtube is missing", SRC_2864_BLOCKERS, "BLOCK2864_3_SR_ZR"),
        ("EVID2879_6_template", "S_R/Z_R template", "TEMPLATE_ONLY_NOT_LIVE_ROW", "template contains MISSING markers and cannot be imported", SRC_2872_TEMPLATE, "TPL2872_2_SRZR_source_density"),
        ("EVID2879_7_JR_builder", "J_R prior builder", "MISSING_SOURCE_BACKED_INPUT", "matter/source coupling row has requirements but no value/theorem", SRC_1625_BUILDER, "PB1625_2_JR"),
        ("EVID2879_8_Ward_current", "Hilbert/current Ward contracts", "CONDITIONAL_NOT_PARENT_DERIVED", "standard current identities need explicit MTS parent source-current definition before scoring", SRC_CURRENT_CONTRACT, "SC1_Hilbert_source_definition"),
        ("EVID2879_9_owner_decomposition", "owner decomposition", "NOT_PARENT_DERIVED", "q_res owner split and retained zero proof remain open", SRC_WARD_CONTRACT, "C1_exact_owner_decomposition"),
    ]
    return [
        add_common(
            {
                "evidence_id": evidence_id,
                "claim_reviewed": claim,
                "status": status,
                "reason": reason,
                "source_path": str(path),
                "source_anchor": anchor,
                "accepted_evidence": False,
                "parent_signed": False,
            }
        )
        for evidence_id, claim, status, reason, path, anchor in rows
    ]


def fill_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "fill_id": "FILL2879_0_SRZR_live_row_attempt",
            "quantity": "S_R/Z_R",
            "candidate_formula": "(J_R+Pi_R+R_readout)/Z_R",
            "candidate_value": "MISSING_S_R_OVER_Z_R",
            "units": "MISSING_SOURCE_DENSITY_UNITS",
            "source_path": "MISSING_PARENT_SOURCE_PATH",
            "equation_anchor": "MISSING_SOURCE_ANCHOR",
            "branch_id": BRANCH_ID,
            "status": "FAILED_TO_FILL_FROM_CURRENT_CORPUS",
            "failure_mode": "component functionals and denominator are not parent-signed",
            "accepted_live_input": False,
            "parent_signed": False,
        },
        {
            "fill_id": "FILL2879_1_source_zero_attempt",
            "quantity": "S_R/Z_R theorem-zero",
            "candidate_formula": "J_R=Pi_R=R_readout=0 with finite same-normalized Z_R",
            "candidate_value": "THEOREM_ZERO_NOT_AVAILABLE",
            "units": "n/a",
            "source_path": "MISSING_JOINT_PARENT_ZERO_THEOREM",
            "equation_anchor": "MISSING_ZERO_THEOREM_ANCHOR",
            "branch_id": BRANCH_ID,
            "status": "SOURCE_ZERO_REJECTED_CURRENT_CORPUS",
            "failure_mode": "no component zero theorem is signed",
            "accepted_live_input": False,
            "parent_signed": False,
        },
        {
            "fill_id": "FILL2879_2_qReff_consequence",
            "quantity": "q_R_eff",
            "candidate_formula": "-int_W S_R/Z_R d^3x",
            "candidate_value": "MISSING_q_R_eff",
            "units": "length_if_delta_R_dimensionless_else_DECLARED_UNITS",
            "source_path": "MISSING_PARENT_SOURCE_PATH",
            "equation_anchor": "MISSING_SOURCE_ANCHOR",
            "branch_id": BRANCH_ID,
            "status": "REMAINS_BLOCKED_BY_SRZR",
            "failure_mode": "cannot integrate a missing source density and boundary class remains missing",
            "accepted_live_input": False,
            "parent_signed": False,
        },
    ]
    return [add_common(row) for row in rows]


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2879_0_source_map_formula", "formal S_R/Z_R decomposition exists", "PASS_CONTROL_ONLY", "MAP2879_0 records the exact components but not values or parent functionals", False),
        ("GATE2879_1_JR_functional", "J_R matter/source current is parent-derived", "FAIL", "PB1625_2_JR and FLC rows remain missing source-backed input", False),
        ("GATE2879_2_PiR_owner", "Pi_R owner/improvement source is zero or mapped", "FAIL", "owner decomposition and retained-source zero proof are not parent-derived", False),
        ("GATE2879_3_readout", "R_readout is zero or explicitly projected", "FAIL", "readout-zero and arena kernels remain missing", False),
        ("GATE2879_4_ZR", "Z_R denominator is same-normalized and finite", "FAIL", "Z_R remains a raw queue item", False),
        ("GATE2879_5_zero_theorem", "joint source-zero theorem closes", "FAIL", "no numerator zero theorem is signed", False),
        ("GATE2879_6_fill", "S_R/Z_R can be used as a live finite source row", "FAIL", "fill attempt keeps MISSING markers and accepted_live_input=False", False),
        ("GATE2879_7_claim", "R10/PPN/local-GR claim can be made from this row", "FAIL_CLOSED", "q_R_eff, ell_R, boundary and arena projection remain blocked", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": passed,
            }
        )
        for gate_id, criterion, result, reason, passed in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2879_0_SRZR_import",
                "status": "REFUSED_SOURCE_MAP_NOT_LIVE",
                "accepted_SRZR_rows": 0,
                "required_SRZR_rows": 1,
                "reason": "S_R/Z_R has a formal decomposition but no parent-signed J_R, Pi_R, R_readout, Z_R or joint source-zero theorem",
                "runner_ready": False,
                "claim_unlocked": False,
                "score_allowed": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2879_0_decomposition", "Write the exact source-map decomposition.", "COMPLETE_CONTROL_ONLY", "S_R/Z_R=(J_R+Pi_R+R_readout)/Z_R is explicit but formal-only"),
        ("DEC2879_1_zero_attempt", "Attempt source-zero theorem.", "REJECTED_CURRENT_CORPUS", "J_R, Pi_R, R_readout and boundary silence are not signed"),
        ("DEC2879_2_fill", "Try to fill a live S_R/Z_R row.", "FAILED_NONCLAIM", "component source functionals, units, source path and Z_R are missing"),
        ("DEC2879_3_route", "Route to operator normalization instead of pretending source is solved.", "SELECTED_2880", "2878 said if source-map and zero theorem fail, attack Z_R/M_R^2 operator normalization"),
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
        for decision_id, decision, result, because in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2879_0_2880",
                "status": "selected_primary",
                "target_doc": "2880-Y5-R2FR-ZR-MR2-operator-normalization-or-range-source-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_ZR_MR2_operator_normalization_or_range_source_row_under_AX1090_2880.py",
                "mission": "derive/source same-normalization Z_R and M_R^2, or a direct ell_R range row, from the parent quadratic action/Hessian; if unavailable, keep q_R_eff blocked and route to matter-source current J_R",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    pairs = [
        ("COPY2879_0_decomposition", OUTPUTS["decomposition"], BRANCH_OUTPUTS["decomposition_copy"], "S_R/Z_R source-map decomposition nonclaim copy"),
        ("COPY2879_1_zero_audit", OUTPUTS["zero_audit"], BRANCH_OUTPUTS["zero_copy"], "source-zero theorem audit nonclaim copy"),
        ("COPY2879_2_fill", OUTPUTS["fill"], BRANCH_OUTPUTS["fill_copy"], "failed S_R/Z_R fill attempt nonclaim copy"),
        ("COPY2879_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to Z_R/M_R^2 operator normalization"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in pairs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def generated_under_root(paths: list[Path]) -> bool:
    root_resolved = ROOT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError:
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "parent_signed",
        "accepted_source_map",
        "theorem_zero",
        "accepted_evidence",
        "accepted_live_input",
        "gate_passed",
        "claim_unlocked",
        "runner_ready",
        "score_allowed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    decomposition = rows_by_name["decomposition"]
    zero_audit = rows_by_name["zero_audit"]
    evidence = rows_by_name["evidence"]
    fill = rows_by_name["fill"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2879_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2879_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2879_2_decomposition_complete", {row["quantity"] for row in decomposition} >= {"S_R/Z_R", "J_R/Z_R", "Pi_R/Z_R", "R_readout/Z_R", "Z_R", "q_R_eff"}, "source map decomposition covers numerator, denominator and compact charge"),
        ("VAL2879_3_no_source_map_acceptance", not any(row["accepted_source_map"] for row in decomposition), "decomposition is formal-only, not accepted source map"),
        ("VAL2879_4_zero_theorem_rejected", any(row["zero_id"] == "ZERO2879_5_joint_source_zero" and row["status"] == "NOT_CLOSED" for row in zero_audit) and not any(row["theorem_zero"] for row in zero_audit), "joint source-zero theorem not closed"),
        ("VAL2879_5_evidence_reviewed", len(evidence) >= 10 and not any(row["accepted_evidence"] for row in evidence), "parent/matter/readout evidence reviewed without promotion"),
        ("VAL2879_6_fill_refused", fill[0]["status"] == "FAILED_TO_FILL_FROM_CURRENT_CORPUS" and not any(row["accepted_live_input"] for row in fill), "S_R/Z_R fill attempt refused"),
        ("VAL2879_7_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "all source-map claim gates fail closed"),
        ("VAL2879_8_runner_refused", runner[0]["status"] == "REFUSED_SOURCE_MAP_NOT_LIVE" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2879_9_next_target_2880", next_target[0]["next_id"] == "NEXT2879_0_2880" and next_target[0]["selected"] is True, "2880 operator-normalization target selected"),
        ("VAL2879_10_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2879_11_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2879_12_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2879_13_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2879_14_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2879_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2879_16_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
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
            "validation_id": "VAL2879_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2879 wrote the exact S_R/Z_R source-map contract, rejected the source-zero theorem for current corpus, refused live-row import, and selected Z_R/M_R^2 operator normalization for 2880.",
            "timestamp_utc": now(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    text = f"""# 2879 - Y5 R2FR S_R over Z_R Source Map Or Source-Zero Theorem Under AX1090

Status: `Y5_R2FR_2879_SRZR_source_map_contract_written_source_zero_rejected_operator_normalization_2880_next`

## Private Verdict

2879 gets the source map into an exact contract but does not let it sneak through as evidence.

The only honest current formula is:

`S_R/Z_R=(J_R+Pi_R+R_readout)/Z_R`

and therefore

`q_R_eff=-int_W S_R/Z_R d^3x`.

That is useful, because it names the missing gears cleanly: the matter/source current `J_R`, the projector/bulk/improvement current `Pi_R`, the readout-regeneration current `R_readout`, and the same-normalization denominator `Z_R`. The zero route also fails for now: none of `J_R=0`, `Pi_R=0`, `R_readout=0`, boundary silence, or finite/same-normalized `Z_R` is parent-signed as one theorem.

So this is progress, but not a local-GR/R10/PPN pass. The next best attack is the operator-normalization route: derive/source `Z_R` and `M_R^2`, or a direct `ell_R`, from the parent quadratic action/Hessian.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## S_R/Z_R Source-Map Decomposition

{md_table(rows_by_name["decomposition"], ["map_id", "quantity", "formal_statement", "current_status", "missing_for_live_row", "parent_signed", "accepted_source_map", "valid_for_claim"])}

## Source-Zero Theorem Audit

{md_table(rows_by_name["zero_audit"], ["zero_id", "target", "required_clause", "status", "blocker", "parent_signed", "theorem_zero", "valid_for_claim"])}

## Parent/Matter/Readout Evidence Review

{md_table(rows_by_name["evidence"], ["evidence_id", "claim_reviewed", "status", "reason", "accepted_evidence", "parent_signed", "valid_for_claim"])}

## S_R/Z_R Fill Attempt

{md_table(rows_by_name["fill"], ["fill_id", "quantity", "candidate_formula", "candidate_value", "status", "failure_mode", "accepted_live_input", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_SRZR_rows", "required_SRZR_rows", "reason", "runner_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    remove_pycache()

    rows_by_name = {
        "sources": source_register_rows(),
        "decomposition": decomposition_rows(),
        "zero_audit": source_zero_rows(),
        "evidence": evidence_review_rows(),
        "fill": fill_rows(),
        "gates": gate_rows(),
        "runner": runner_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], branch_rows)
    rows_by_name["branches"] = branch_rows

    remove_pycache()
    validation = validation_rows(rows_by_name, branch_rows)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name, branch_rows, validation)
    remove_pycache()

    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation if row["validation_id"] == "VAL2879_OVERALL")
    print(f"VAL2879_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
