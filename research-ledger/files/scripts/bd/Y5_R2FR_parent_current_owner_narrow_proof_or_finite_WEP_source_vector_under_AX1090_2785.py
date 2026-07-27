from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2785-Y5-R2FR-parent-current-owner-narrow-proof-or-finite-WEP-source-vector-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2785_SOURCE_REGISTER.csv",
    "narrow_proof": MTS / "P8_Y5_R2FR_2785_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
    "premises": MTS / "P8_Y5_R2FR_2785_CURRENT_OWNER_PREMISE_LEDGER.csv",
    "counterexamples": MTS / "P8_Y5_R2FR_2785_COUNTEREXAMPLE_RESOLUTION_MATRIX.csv",
    "finite_contract": MTS / "P8_Y5_R2FR_2785_FINITE_WEP_SOURCE_VECTOR_CONTRACT.csv",
    "material_contract": MTS / "P8_Y5_R2FR_2785_MATERIAL_TENSOR_CONTRACT.csv",
    "finite_template": MTS / "P8_Y5_R2FR_2785_FINITE_VECTOR_TEMPLATE_NONCLAIM.csv",
    "candidate": MTS / "P8_Y5_R2FR_2785_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "bounds": MTS / "P8_Y5_R2FR_2785_WEP_BOUND_IMPORT.csv",
    "runner": MTS / "P8_Y5_R2FR_2785_PRODUCT_RUNNER_STATUS.csv",
    "comparisons": MTS / "P8_Y5_R2FR_2785_PRODUCT_COMPARISON_ROWS.csv",
    "gates": MTS / "P8_Y5_R2FR_2785_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2785_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2785_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2785_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2785_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "proof_queue": RAB_QUEUE / "JR2785_CURRENT_OWNER_NARROW_PROOF_NONCLAIM.csv",
    "finite_queue": RAB_QUEUE / "JR2785_FINITE_WEP_VECTOR_CONTRACT_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "MICROSCOPE_FINITE_WEP_VECTOR_CONTRACT_2785_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_finite_wep_contract_2785_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2785_FINITE_WEP_ACQUISITION_PACK_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["valid_for_claim"] = False
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def is_numeric(value: Any) -> bool:
    try:
        float(str(value))
    except (TypeError, ValueError):
        return False
    return True


def has_missing_marker(row: dict[str, Any]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values()).upper()


def trueish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def get_local_bound(row_id: str) -> dict[str, str]:
    for row in read_csv_rows(LOCAL_BOUNDS / "local_bound_claims.csv"):
        if row.get("row_id") == row_id:
            return row
    return {}


def source_row(row_id: str, source_key: str, path: Path, needle: str, role: str) -> dict[str, Any]:
    text = read_text(path)
    exists = path.exists()
    return nonclaim({
        "row_id": row_id,
        "source_key": source_key,
        "source_path": str(path),
        "exists": exists,
        "needle": needle,
        "needle_found": exists and needle in text,
        "source_role": role,
    })


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2785_00_2784_next", "2784_next", MTS / "P8_Y5_R2FR_2784_NEXT_TARGET.csv", "NEXT2784_0_2785", "current handoff into narrow current-owner proof"),
        ("SRC2785_01_2784_validation", "2784_validation", MTS / "P8_Y5_BRR545_2784_VALIDATION.csv", "VAL2784_OVERALL", "2784 validation baseline"),
        ("SRC2785_02_2784_current_owner", "2784_current_owner", MTS / "P8_Y5_R2FR_2784_CURRENT_OWNER_PROOF_ATTEMPT.csv", "CO2784_4_verdict", "current-owner proof stack obstruction"),
        ("SRC2785_03_2784_demotion", "2784_demotion", MTS / "P8_Y5_R2FR_2784_THEOREM_ZERO_DEMOTION.csv", "TZD2784_2_demote", "closure-only theorem-zero demotion"),
        ("SRC2785_04_2784_finite_gates", "2784_finite_gates", MTS / "P8_Y5_R2FR_2784_FINITE_ROUTE_DEMOTION_GATES.csv", "FRD2784_2_coupling_owner", "finite WEP route gates"),
        ("SRC2785_05_2783_requirements", "2783_requirements", MTS / "P8_Y5_R2FR_2783_FINITE_ROUTE_REQUIREMENTS.csv", "FIN2783_2_C_parent", "finite WEP input requirements"),
        ("SRC2785_06_2782_material", "2782_material", MTS / "P8_Y5_R2FR_2782_TOY_MATERIAL_VECTOR_FROM_651.csv", "MV2782_delta_TA6V_minus_PtRh10", "toy material vector warning"),
        ("SRC2785_07_1079_precedent", "1079_precedent", MTS / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv", "NCO1079_6_verdict", "R10 narrow current-owner precedent"),
        ("SRC2785_08_1079_contract", "1079_contract", MTS / "P8_Y5_R10_1079_FINITE_WEP_SOURCE_VECTOR_CONTRACT.csv", "FSV1079_0_formula", "R10 finite WEP source-vector contract"),
        ("SRC2785_09_1080_pack", "1080_pack", MTS / "P8_Y5_R10_1080_FINITE_WEP_INPUT_PACK_NONCLAIM.csv", "FIP1080_0_product_formula", "R10 finite WEP acquisition pack"),
        ("SRC2785_10_1080_material", "1080_material", MTS / "P8_Y5_R10_1080_MATERIAL_COMPOSITION_AND_TENSOR_CANDIDATES.csv", "MAT1080_4_full_tensor_upgrade", "R10 material tensor acquisition status"),
        ("SRC2785_11_1080_cparent", "1080_cparent", MTS / "P8_Y5_R10_1080_C_PARENT_COEFFICIENT_CONTRACT.csv", "CP1080_0_definition", "R10 parent coefficient contract"),
        ("SRC2785_12_1080_next", "1080_next", MTS / "P8_Y5_R10_1080_NEXT_TARGET.csv", "NEXT1080_0_1081", "R10 post-pack route"),
        ("SRC2785_13_local_bounds", "local_bounds", LOCAL_BOUNDS / "local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row"),
    ]
    return [source_row(*spec) for spec in specs]


def build_narrow_proof_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        {
            "theorem_id": "NCO2785_0_target",
            "claim": "narrow current/source normalization owner",
            "statement": "inside a common parent matter action, the gravitational source is the Hilbert variation with respect to the observed coframe/metric before any readout selector",
            "proof_move": "strip the problem down to current ownership only; do not ask it to solve object-language or action-measure ownership",
            "result": "TARGET_SHARPENED",
            "gap": "this can only sign a subtheorem; it cannot by itself forbid pre-variation species action weights",
            "claim_allowed": False,
            "generated_utc": generated,
        },
        {
            "theorem_id": "NCO2785_1_hilbert_variation",
            "claim": "Hilbert source is unique after a common action is fixed",
            "statement": "T_mu_nu := delta S_matter / delta e_obs is the only source seen by the metric/coframe variation when variation is performed before readout",
            "proof_move": "functional derivative of one fixed action with one observed coframe has one source tensor at that variation point",
            "result": "EXACT_SUBTHEOREM_CONDITIONAL",
            "gap": "requires common S_matter and variation-before-readout as premises",
            "claim_allowed": False,
            "generated_utc": generated,
        },
        {
            "theorem_id": "NCO2785_2_ward_identity",
            "claim": "diffeomorphism Ward identity owns source conservation",
            "statement": "on matter shell, diffeomorphism invariance of S_matter gives covariant conservation of the Hilbert source in the observed geometry",
            "proof_move": "push an infinitesimal diffeomorphism through the common action and collect the coefficient of the generator",
            "result": "CONDITIONAL_WARD_IDENTITY",
            "gap": "conservation does not fix relative source weights already inserted into S_matter",
            "claim_allowed": False,
            "generated_utc": generated,
        },
        {
            "theorem_id": "NCO2785_3_post_variation_selector",
            "claim": "post-variation material selector is forbidden by current ownership",
            "statement": "if readout is downstream of variation, F(T_A,A) cannot redefine the source tensor that varied the geometry",
            "proof_move": "readout maps may project measured channels but cannot retroactively alter the variational source",
            "result": "KILLS_POST_VARIATION_SELECTOR_CONDITIONAL",
            "gap": "parent readout-order axiom remains a contract, not a full corpus theorem",
            "claim_allowed": False,
            "generated_utc": generated,
        },
        {
            "theorem_id": "NCO2785_4_current_rescaling",
            "claim": "J_A -> c_A J_A is not legal after Hilbert-source ownership",
            "statement": "once T_mu_nu is defined by variation, a later source-current rescaling is not a new parent source",
            "proof_move": "classify c_A after variation as readout/calibration, not action-source ownership",
            "result": "PARTIALLY_KILLED_AFTER_HILBERT_OWNER",
            "gap": "c_A can still hide as a pre-variation action coefficient unless action-measure/object-language clauses are signed",
            "claim_allowed": False,
            "generated_utc": generated,
        },
        {
            "theorem_id": "NCO2785_5_species_action_weight",
            "claim": "S_matter = sum_A w_A S_A is killed by current ownership alone",
            "statement": "pre-variation species weights would be rejected by the current-owner subtheorem",
            "proof_move": "test whether Hilbert variation removes w_A when w_A is already inside S_matter",
            "result": "SURVIVES_PRE_VARIATION",
            "gap": "Hilbert stress simply inherits w_A; this needs action-measure/object-language ownership, not current ownership alone",
            "claim_allowed": False,
            "generated_utc": generated,
        },
        {
            "theorem_id": "NCO2785_6_verdict",
            "claim": "narrow current-owner proof closes WEP theorem-zero",
            "statement": "current-owner subtheorem is strong enough to make P_WEP=0",
            "proof_move": "assemble Hilbert variation, Ward identity, post-variation selector kill, and pre-variation counterexample audit",
            "result": "NARROW_CURRENT_OWNER_PARTIAL_NOT_WEP_CLOSED",
            "gap": "post-variation tricks are conditionally killed, but pre-variation species weights survive",
            "claim_allowed": False,
            "generated_utc": generated,
        },
    ]
    return [nonclaim(row) for row in rows]


def build_premise_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("PR2785_0_common_parent_action", "common parent S_matter for all ordinary matter", "UNSIGNED_IN_R2FR", "without this, Hilbert uniqueness is not a universal WEP theorem", False),
        ("PR2785_1_variation_before_readout", "variation is performed before material/readout projection", "CONDITIONAL_CONTRACT", "kills only post-variation selectors", False),
        ("PR2785_2_hilbert_source_uniqueness", "source is owned by functional variation of the fixed action", "EXACT_IF_PREMISES", "useful subtheorem, not a full local-GR/WEP pass", False),
        ("PR2785_3_ward_conservation", "diffeomorphism Ward identity gives conservation of the owned source", "EXACT_IF_PREMISES", "conservation is not normalization ownership", False),
        ("PR2785_4_no_pre_action_species_weight", "no w_A S_A inside S_matter", "NOT_SIGNED", "pre-variation weight survives current-owner proof", False),
        ("PR2785_5_gauge_current_owner", "Noether/gauge current normalization fixed by representation data", "PARTIAL_GAUGE_ONLY", "does not fix Hilbert gravitational source coefficient", False),
        ("PR2785_6_finite_route_needed", "if proof is partial, build finite source/material/C_parent product", "ROUTE_SELECTED", "least dishonest scoreable path after current-owner partial result", False),
    ]
    return [
        nonclaim({
            "premise_id": premise_id,
            "premise": premise,
            "status": status,
            "why_it_matters": why,
            "claim_allowed": claim_allowed,
            "generated_utc": generated,
        })
        for premise_id, premise, status, why, claim_allowed in rows
    ]


def build_counterexample_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        {
            "counterexample_id": "CER2785_0_post_variation_selector",
            "counterexample": "post-variation material selector F(T_A,A)",
            "current_owner_resolution": "CONDITIONALLY_KILLED",
            "survives_as": "only if variation-before-readout/readout-order premise is unsigned",
            "next_action": "keep as contract until parent action signs readout order",
            "claim_allowed": False,
            "generated_utc": generated,
        },
        {
            "counterexample_id": "CER2785_1_current_rescaling_after_variation",
            "counterexample": "J_A -> c_A J_A after Hilbert source has been varied",
            "current_owner_resolution": "PARTIALLY_KILLED",
            "survives_as": "not a post-variation current, but c_A can be moved into the action before variation",
            "next_action": "do not claim theorem-zero; route unresolved coefficient into C_parent",
            "claim_allowed": False,
            "generated_utc": generated,
        },
        {
            "counterexample_id": "CER2785_2_species_action_weight",
            "counterexample": "S_matter = sum_A w_A S_A",
            "current_owner_resolution": "SURVIVES_PRE_VARIATION",
            "survives_as": "Hilbert stress inherits w_A and the current-owner proof has no lever on it",
            "next_action": "needs action-measure/object-language owner or finite sourced WEP product",
            "claim_allowed": False,
            "generated_utc": generated,
        },
        {
            "counterexample_id": "CER2785_3_disconnected_material_constants",
            "counterexample": "independent constants on disconnected material components",
            "current_owner_resolution": "SURVIVES_OBJECT_LANGUAGE",
            "survives_as": "direct-sum matter sectors can carry label constants unless object language forbids them",
            "next_action": "keep object-language proof separate; do not smuggle it into current ownership",
            "claim_allowed": False,
            "generated_utc": generated,
        },
    ]
    return [nonclaim(row) for row in rows]


def build_finite_contract_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("FWSC2785_0_formula", "finite WEP product formula", "P_WEP = sum_I C_parent^I * R_source_I^Earth * DeltaR_material_I projected by K_MICROSCOPE", "FORMULA_CONTRACT_ONLY", "numeric C_parent; numeric source vector; numeric material vector; official readout kernel"),
        ("FWSC2785_1_C_parent", "C_parent coupling owner", "parent coefficient vector, units, sign convention, normalization, and source path", "MISSING_PARENT_COEFFICIENT", "signed current/action owner or sourced finite coefficient"),
        ("FWSC2785_2_source_vector", "R_source^Earth", "Earth/source worldtube response vector in same basis as material response and C_parent", "MISSING_SOURCE_VECTOR", "source composition/profile/current vector or common-mode theorem"),
        ("FWSC2785_3_material_vector", "R_TA6V - R_PtRh10", "source-backed material response vector for MICROSCOPE test-mass compositions in the same parent basis", "TOY_OR_EXTERNAL_SMOKE_ONLY", "composition/material tensor source and uncertainty convention"),
        ("FWSC2785_4_readout_kernel", "K_MICROSCOPE", "official CMSM arrays/masks or accepted reconstruction with projection units", "SURROGATE_ONLY", "official arrays or validated replacement"),
        ("FWSC2785_5_tau_shape", "tau_WEP", "arena projection from parent residual to MICROSCOPE eta channel", "MISSING_PHYSICAL_TAU", "readout kernel plus same-basis finite product"),
    ]
    return [
        nonclaim({
            "contract_id": contract_id,
            "object": obj,
            "required_content": required,
            "current_status": status,
            "missing_for_claim": missing,
            "generated_utc": generated,
        })
        for contract_id, obj, required, status, missing in rows
    ]


def build_material_contract_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("MTC2785_0_basis", "parent material response basis", "basis labels I, units, normalization, and relation to parent C_parent", "MISSING_MTS_PARENT_BASIS", "cannot multiply source/material vectors without same basis"),
        ("MTC2785_1_test_mass_composition", "TA6V and PtRh10 composition", "mass fractions, isotope/element assumptions, uncertainty convention, source path", "SOURCE_CONTEXT_EXISTS_NOT_FULL_RESPONSE", "composition is not yet a parent response tensor"),
        ("MTC2785_2_delta_response", "DeltaR_material = R_TA6V - R_PtRh10", "same-basis response components and uncertainty propagation", "MISSING_FULL_MATERIAL_TENSOR", "toy Z/A and external DD smoke components are nonclaim"),
        ("MTC2785_3_source_response", "R_source^Earth", "Earth composition/worldtube response in same basis and normalization", "MISSING_SOURCE_VECTOR", "source proxy cannot be assumed tau=1"),
        ("MTC2785_4_parent_coefficient", "C_parent", "derived or sourced finite coupling coefficient in same basis", "MISSING_PARENT_COEFFICIENT", "current-owner partial proof is not a coefficient"),
        ("MTC2785_5_claim_gate", "finite WEP tensor readiness", "all four objects numeric, sourced, same-basis, and readout-projected", "BLOCKED", "do not promote smoke rows to evidence"),
    ]
    return [
        nonclaim({
            "material_contract_id": contract_id,
            "object": obj,
            "required_content": required,
            "current_status": status,
            "missing_for_claim": missing,
            "generated_utc": generated,
        })
        for contract_id, obj, required, status, missing in rows
    ]


def build_finite_template_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("FVT2785_0_C_parent", "C_parent^I", "MISSING_PARENT_COEFFICIENT_VECTOR", "basis-dependent", "MISSING_FOR_CLAIM", "parent action/current/action-measure owner or sourced finite coefficient"),
        ("FVT2785_1_R_source", "R_source_I^Earth", "MISSING_SOURCE_VECTOR", "basis-dependent", "MISSING_FOR_CLAIM", "Earth/source composition or worldtube response in same basis"),
        ("FVT2785_2_DeltaR_material", "R_TA6V_I - R_PtRh10_I", "MISSING_FULL_MATERIAL_TENSOR", "basis-dependent", "MISSING_FOR_CLAIM", "source-backed material response tensor in same basis"),
        ("FVT2785_3_K_MICROSCOPE", "K_MICROSCOPE^I", "MISSING_OFFICIAL_OR_VALIDATED_READOUT_KERNEL", "eta projection", "MISSING_FOR_CLAIM", "official CMSM arrays or validated reconstruction"),
        ("FVT2785_4_tau_WEP", "tau_WEP", "MISSING_PHYSICAL_TAU", "dimensionless", "MISSING_FOR_CLAIM", "derived from readout kernel and parent-to-arena projection"),
    ]
    return [
        nonclaim({
            "template_id": template_id,
            "symbol": symbol,
            "candidate_value": value,
            "units": units,
            "status": status,
            "missing_for_claim": missing,
            "generated_utc": generated,
        })
        for template_id, symbol, value, units, status, missing in rows
    ]


def build_candidate_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "prediction_id": "PRED2785_0_WEP_current_owner_or_finite_vector_nonclaim",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_NARROW_CURRENT_OWNER_OR_FINITE_SOURCE_VECTOR",
            "product_units": "dimensionless",
            "derivation_status": "NARROW_CURRENT_OWNER_PARTIAL_FINITE_VECTOR_MISSING",
            "notes": "post-variation selector is conditionally killed, but pre-variation species weights survive and finite source/material/C_parent/K inputs are missing",
        })
    ]


def build_bound_rows() -> list[dict[str, Any]]:
    bound = get_local_bound("R1_WEP_source_charge")
    return [
        nonclaim({
            "bound_id": "BOUND2785_0_MICROSCOPE_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "observable": "eta_WEP_source_charge",
            "upper_bound": bound.get("upper_bound", "2.8e-15"),
            "units": bound.get("units", "dimensionless"),
            "source_path_or_url": bound.get("reference_path_or_url", "https://arxiv.org/abs/2209.15487; doi:10.1103/PhysRevLett.129.121102"),
            "source_row": "source-intake/local_bounds/local_bound_claims.csv:R1_WEP_source_charge",
            "valid_bound_row": True,
        })
    ]


def build_runner_rows(candidate_rows: list[dict[str, Any]], bound_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    valid_prediction_rows = [
        row for row in candidate_rows
        if trueish(row.get("valid_for_claim")) and is_numeric(row.get("product_value")) and not has_missing_marker(row)
    ]
    valid_bound_rows = [
        row for row in bound_rows
        if trueish(row.get("valid_bound_row")) and is_numeric(row.get("upper_bound")) and float(row.get("upper_bound", 0)) > 0
    ]
    return [
        nonclaim({
            "runner_id": "RUN2785_0_WEP_current_owner_partial_product_stub",
            "valid_prediction_rows": len(valid_prediction_rows),
            "valid_bound_rows": len(valid_bound_rows),
            "claim_allowed": False,
            "failure_mode": "REJECT_NARROW_CURRENT_OWNER_PARTIAL_AND_MISSING_FINITE_WEP_VECTORS",
            "notes": "runner schema, unit, and refusal behaviour work; no WEP/local-GR pass is claimed",
        })
    ]


def build_comparison_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "comparison_id": "COMP2785_0_MICROSCOPE_WEP",
            "prediction_id": "PRED2785_0_WEP_current_owner_or_finite_vector_nonclaim",
            "bound_id": "BOUND2785_0_MICROSCOPE_WEP_source_charge",
            "abs_prediction": "MISSING_NARROW_CURRENT_OWNER_OR_FINITE_SOURCE_VECTOR",
            "upper_bound": "2.8e-15",
            "passes_bound": False,
            "comparison_status": "NOT_RUN_NUMERICALLY",
            "reason": "prediction is not numeric and finite WEP input vectors are missing",
        })
    ]


def build_gate_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("CG2785_0_hilbert_subtheorem", "Hilbert-source uniqueness inside fixed common action", True, False, "exact conditional subtheorem retained, not claim-ready"),
        ("CG2785_1_WEP_theorem_zero", "WEP theorem-zero", False, False, "pre-variation species action weights survive current-owner proof"),
        ("CG2785_2_finite_C_parent", "finite C_parent coefficient", False, False, "parent coefficient/basis missing"),
        ("CG2785_3_finite_source_vector", "finite Earth/source vector", False, False, "R_source^Earth missing"),
        ("CG2785_4_finite_material_tensor", "finite material tensor", False, False, "full R_TA6V - R_PtRh10 missing; toy/external smoke only"),
        ("CG2785_5_readout_kernel", "official/validated MICROSCOPE readout kernel", False, False, "official CMSM arrays or accepted reconstruction still missing"),
        ("CG2785_6_product_runner", "WEP product runner", False, False, "valid_prediction_rows=0"),
    ]
    return [
        nonclaim({
            "gate_id": gate_id,
            "gate": gate,
            "subtheorem_supported": subtheorem_supported,
            "claim_allowed": claim_allowed,
            "reason": reason,
            "generated_utc": generated,
        })
        for gate_id, gate, subtheorem_supported, claim_allowed, reason in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    generated = ts()
    rows = [
        ("DEC2785_0_keep_subtheorem", "retain the Hilbert-source/current-owner subtheorem", "it cleanly kills post-variation source redefinitions once a common action and readout order are assumed", "use it as a proof lemma, not as a WEP/local-GR claim"),
        ("DEC2785_1_not_WEP_closed", "do not promote current-owner proof to WEP theorem-zero", "pre-variation species weights survive and are outside current ownership", "route WEP through action-measure/object-language closure or finite sourced vector product"),
        ("DEC2785_2_acquisition_route", "build the finite WEP source-vector/material-tensor acquisition pack", "this is now the least dishonest scoreable route after the current-owner partial win", "2786 should assemble R_source^Earth, DeltaR_material, C_parent, K_MICROSCOPE, basis, units, provenance, and runner refusal"),
    ]
    return [
        nonclaim({
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "generated_utc": generated,
        })
        for decision_id, decision, reason, next_action in rows
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "next_id": "NEXT2785_0_2786",
            "next_target": "2786-Y5-R2FR-finite-WEP-source-vector-and-material-tensor-acquisition-pack-under-AX1090.md",
            "script": "scripts/Y5_R2FR_finite_WEP_source_vector_and_material_tensor_acquisition_pack_under_AX1090_2786.py",
            "objective": "build the finite WEP input acquisition pack for R2FR: source-backed Earth/source vector, Ti/Pt material response tensor contract, C_parent coefficient contract, and official/surrogate MICROSCOPE readout gate; keep product invalid until same-basis rows are numeric and sourced",
            "include": "R_source^Earth; R_TA6V - R_PtRh10; C_parent; K_MICROSCOPE; tau_WEP; units; basis; provenance; runner refusal",
            "exclude": "toy vector as evidence; measured-G absorption; tau=1; Delta_w=0 by taste; public claim; GitHub; formalization edits",
        })
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_pairs = [
        (OUTPUTS["narrow_proof"], BRANCH_OUTPUTS["proof_queue"], "proof_queue"),
        (OUTPUTS["finite_contract"], BRANCH_OUTPUTS["finite_queue"], "finite_queue"),
        (OUTPUTS["material_contract"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["finite_template"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
    ]
    rows = []
    for source, target, branch_key in copy_pairs:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(nonclaim({
            "branch_id": f"BR2785_{len(rows)}_{branch_key}",
            "source_path": str(source),
            "branch_path": str(target),
            "exists": target.exists(),
            "row_count": csv_row_count(target) if target.exists() else 0,
            "branch_role": branch_key,
        }))
    return rows


def no_claim_flags(paths: list[Path]) -> bool:
    flag_fields = {"valid_for_claim", "claim_allowed", "pass_for_claim"}
    for path in paths:
        for row in read_csv_rows(path):
            for field in flag_fields:
                if trueish(row.get(field)):
                    return False
    return True


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    started = RUN_STARTED_UTC.timestamp()
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime >= started:
            count += 1
    return count


def build_validation_rows(
    sources: list[dict[str, Any]],
    narrow_rows: list[dict[str, Any]],
    premise_rows: list[dict[str, Any]],
    counterexample_rows: list[dict[str, Any]],
    finite_contract_rows: list[dict[str, Any]],
    material_contract_rows: list[dict[str, Any]],
    finite_template_rows: list[dict[str, Any]],
    candidate_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    runner_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2785_0_sources", all(trueish(row["exists"]) and trueish(row["needle_found"]) for row in sources), "every cited source path exists and source needle was found"),
        ("VAL2785_1_hilbert_subtheorem", any(row["theorem_id"] == "NCO2785_1_hilbert_variation" and row["result"] == "EXACT_SUBTHEOREM_CONDITIONAL" for row in narrow_rows), "Hilbert-current owner subtheorem is captured"),
        ("VAL2785_2_not_WEP_closed", any(row["theorem_id"] == "NCO2785_6_verdict" and row["result"] == "NARROW_CURRENT_OWNER_PARTIAL_NOT_WEP_CLOSED" for row in narrow_rows), "narrow current-owner proof does not close WEP"),
        ("VAL2785_3_pre_action_weight_survives", any(row["counterexample_id"] == "CER2785_2_species_action_weight" and row["current_owner_resolution"] == "SURVIVES_PRE_VARIATION" for row in counterexample_rows), "pre-variation species action weight survives"),
        ("VAL2785_4_post_variation_selector_killed", any(row["counterexample_id"] == "CER2785_0_post_variation_selector" and row["current_owner_resolution"] == "CONDITIONALLY_KILLED" for row in counterexample_rows), "post-variation selector is conditionally killed"),
        ("VAL2785_5_premise_ledger_safe", any(row["premise_id"] == "PR2785_4_no_pre_action_species_weight" and row["status"] == "NOT_SIGNED" for row in premise_rows), "premise ledger records unsigned pre-action weight clause"),
        ("VAL2785_6_finite_contract_nonclaim", all(not trueish(row.get("valid_for_claim")) for row in finite_contract_rows) and any("MISSING" in row["current_status"] for row in finite_contract_rows), "finite WEP contract rows are nonclaim and missing claim inputs"),
        ("VAL2785_7_material_contract_blocked", any(row["current_status"] == "MISSING_FULL_MATERIAL_TENSOR" for row in material_contract_rows), "material tensor contract remains blocked"),
        ("VAL2785_8_template_nonclaim_missing", all(has_missing_marker(row) and not trueish(row.get("valid_for_claim")) for row in finite_template_rows), "finite vector template rows remain missing/nonclaim"),
        ("VAL2785_9_prediction_nonclaim_missing", all(has_missing_marker(row) and not trueish(row.get("valid_for_claim")) for row in candidate_rows), "prediction row remains missing finite WEP inputs"),
        ("VAL2785_10_bound_numeric", all(is_numeric(row["upper_bound"]) and float(row["upper_bound"]) > 0 for row in bound_rows), "bound import is positive numeric"),
        ("VAL2785_11_runner_refuses", runner_rows[0]["valid_prediction_rows"] == 0 and not trueish(runner_rows[0]["claim_allowed"]), "runner reports no valid prediction rows and claim false"),
        ("VAL2785_12_claim_gates_safe", all(not trueish(row.get("claim_allowed")) for row in gate_rows), "all claim gates deny WEP/local-GR claim"),
        ("VAL2785_13_next_target", next_rows[0]["next_target"].startswith("2786-Y5-R2FR-finite-WEP-source-vector"), "2786 handoff written"),
        ("VAL2785_14_branch_outputs", all(trueish(row["exists"]) and int(row["row_count"]) > 0 for row in branch_rows), "branch copies exist and contain rows"),
        ("VAL2785_15_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2785_16_no_claim_flags", no_claim_flags(generated_paths), "no generated row is valid_for_claim=true/claim_allowed=true/pass_for_claim=true"),
        ("VAL2785_17_generated_under_post_checkpoint", all(WORK in path.parents or path == WORK for path in generated_paths + [DOC]), "all generated outputs are under post-checkpoint-work"),
        ("VAL2785_18_formalization_untouched", formalization_modified_count() == 0, "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2785_19_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent at validation write"),
    ]
    rows = [
        {
            "validation_id": check_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": ts(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append({
        "validation_id": "VAL2785_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2785 proves a useful narrow Hilbert-current owner subtheorem, conditionally kills post-variation source redefinitions, rejects WEP theorem-zero closure because pre-variation species weights survive, and hands off to finite WEP source/material/C_parent/readout acquisition.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2785 - Parent current-owner narrow proof or finite WEP source vector under AX1090",
        "",
        "## Private Verdict",
        "",
        "2785 gets the narrow win, not the big WEP/local-GR win. A fixed common matter action varied before readout gives a unique Hilbert source, so post-variation source selectors are conditionally killed. But the current-owner proof cannot remove species weights already inserted inside the action before variation. Therefore theorem-zero remains closure-only and the honest next route is a finite WEP acquisition pack: C_parent, R_source^Earth, R_TA6V - R_PtRh10, K_MICROSCOPE, and tau_WEP.",
        "",
        "## Source Register",
        markdown_table(sections["sources"], ["row_id", "source_key", "exists", "needle_found", "source_role"]),
        "",
        "## Narrow Current-Owner Theorem Attempt",
        markdown_table(sections["narrow_proof"], ["theorem_id", "claim", "result", "gap"]),
        "",
        "## Current-Owner Premise Ledger",
        markdown_table(sections["premises"], ["premise_id", "premise", "status", "why_it_matters"]),
        "",
        "## Counterexample Resolution Matrix",
        markdown_table(sections["counterexamples"], ["counterexample_id", "counterexample", "current_owner_resolution", "survives_as", "next_action"]),
        "",
        "## Finite WEP Source-Vector Contract",
        markdown_table(sections["finite_contract"], ["contract_id", "object", "current_status", "missing_for_claim"]),
        "",
        "## Material Tensor Contract",
        markdown_table(sections["material_contract"], ["material_contract_id", "object", "current_status", "missing_for_claim"]),
        "",
        "## Finite Vector Template Nonclaim",
        markdown_table(sections["finite_template"], ["template_id", "symbol", "candidate_value", "status", "missing_for_claim"]),
        "",
        "## Product Stub And Bound",
        markdown_table(sections["candidate"], ["prediction_id", "product_symbol", "product_value", "derivation_status", "valid_for_claim"]),
        "",
        markdown_table(sections["bounds"], ["bound_id", "observable", "upper_bound", "units", "valid_bound_row"]),
        "",
        markdown_table(sections["runner"], ["runner_id", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "failure_mode"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "gate", "subtheorem_supported", "claim_allowed", "reason"]),
        "",
        "## Decision Ledger",
        markdown_table(sections["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Validation",
        markdown_table(sections["validation"], ["validation_id", "passed", "detail"]),
        "",
        "## Next Target",
        markdown_table(sections["next"], ["next_id", "next_target", "objective", "include", "exclude"]),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    if (SCRIPTS / "__pycache__").exists():
        shutil.rmtree(SCRIPTS / "__pycache__")

    sources = build_sources()
    narrow_proof = build_narrow_proof_rows()
    premises = build_premise_rows()
    counterexamples = build_counterexample_rows()
    finite_contract = build_finite_contract_rows()
    material_contract = build_material_contract_rows()
    finite_template = build_finite_template_rows()
    candidate = build_candidate_rows()
    bounds = build_bound_rows()
    runner = build_runner_rows(candidate, bounds)
    comparisons = build_comparison_rows()
    gates = build_gate_rows()
    decision = build_decision_rows()
    next_rows = build_next_rows()

    generated = {
        "sources": sources,
        "narrow_proof": narrow_proof,
        "premises": premises,
        "counterexamples": counterexamples,
        "finite_contract": finite_contract,
        "material_contract": material_contract,
        "finite_template": finite_template,
        "candidate": candidate,
        "bounds": bounds,
        "runner": runner,
        "comparisons": comparisons,
        "gates": gates,
        "decision": decision,
        "next": next_rows,
    }

    for key, rows in generated.items():
        write_csv(OUTPUTS[key], rows)

    branch_rows = copy_branches()
    write_csv(OUTPUTS["branches"], branch_rows)

    validation = build_validation_rows(
        sources,
        narrow_proof,
        premises,
        counterexamples,
        finite_contract,
        material_contract,
        finite_template,
        candidate,
        bounds,
        runner,
        gates,
        next_rows,
        branch_rows,
    )
    write_csv(OUTPUTS["validation"], validation)

    doc_sections = generated | {"branches": branch_rows, "validation": validation}
    DOC.write_text(build_doc(doc_sections), encoding="utf-8")

    print(f"wrote {DOC}")
    print(f"validation overall: {validation[-1]['passed']}")


if __name__ == "__main__":
    main()
