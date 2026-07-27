from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "1079-Y5-R10-parent-current-owner-narrow-proof-or-finite-WEP-source-vector.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1079-parent-current-owner-narrow-proof-or-finite-WEP-source-vector" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1079_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1079_WEP_BOUND_IMPORT.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def local_bound_row(row_id: str) -> dict[str, str]:
    for row in read_csv(LOCAL_BOUNDS):
        if row.get("row_id") == row_id:
            return row
    raise ValueError(f"missing local bound row {row_id}")


def split_reference(reference: str) -> tuple[str, str]:
    parts = [part.strip() for part in reference.split(";")]
    url = next((part for part in parts if part.startswith("http")), "")
    doi = next((part.replace("doi:", "").strip() for part in parts if part.lower().startswith("doi:")), "")
    return url, doi


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1079_0_1078_next", "source-intake/mts_residuals/P8_Y5_R10_1078_NEXT_TARGET.csv", "1079-Y5-R10-parent-current-owner-narrow-proof-or-finite-WEP-source-vector.md", "1078 handoff."),
        ("SRC1079_1_1078_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1078_VALIDATION.csv", "V1078_SUMMARY", "1078 validation summary."),
        ("SRC1079_2_1078_current", "source-intake/mts_residuals/P8_Y5_R10_1078_CURRENT_OWNER_PROOF_ATTEMPT.csv", "CO1078_4_verdict", "current-owner failure to close."),
        ("SRC1079_3_1078_demotion", "source-intake/mts_residuals/P8_Y5_R10_1078_THEOREM_ZERO_DEMOTION.csv", "TZD1078_2_demote", "theorem-zero closure-only demotion."),
        ("SRC1079_4_1078_finite", "source-intake/mts_residuals/P8_Y5_R10_1078_FINITE_ROUTE_DEMOTION_GATES.csv", "FRD1078_2_coupling_owner", "finite WEP route gates."),
        ("SRC1079_5_1078_counter", "source-intake/mts_residuals/P8_Y5_R10_1078_COUNTEREXAMPLE_KILL_MATRIX.csv", "CEK1078_0_species_action_weight", "counterexample survival matrix."),
        ("SRC1079_6_1077_finite", "source-intake/mts_residuals/P8_Y5_R10_1077_FINITE_ROUTE_REQUIREMENTS.csv", "FIN1077_1_R_source", "finite route requirement source."),
        ("SRC1079_7_1076_owner", "source-intake/mts_residuals/P8_Y5_R10_1076_COUPLING_OWNER_GATES.csv", "OWN1076_2_current_owner", "coupling-owner gate source."),
        ("SRC1079_8_1075_tau_shape", "source-intake/mts_residuals/P8_Y5_R10_1075_TAU_SHAPE_STATUS.csv", "status_id", "surrogate readout status source."),
        ("SRC1079_9_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        needle_found = exists and needle in read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle_found).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def narrow_current_owner_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "NCO1079_0_target",
            "claim": "narrow current/source normalization owner",
            "statement": "inside a common parent matter action, the gravitational source is the Hilbert variation with respect to the observed coframe/metric before any readout selector",
            "proof_move": "separate current ownership from wider object-language and action-measure ownership",
            "result": "TARGET_SHARPENED",
            "gap": "this can only sign a subtheorem, not full WEP theorem-zero",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NCO1079_1_hilbert_variation",
            "claim": "Hilbert source is unique after a common action is fixed",
            "statement": "T_mu_nu := delta S_matter / delta e_obs is the only source seen by the metric/coframe variation when variation is performed before readout",
            "proof_move": "functional derivative of one action with one observed coframe has one source tensor at that variation point",
            "result": "EXACT_SUBTHEOREM_CONDITIONAL",
            "gap": "requires a common S_matter and variation-before-readout as premises",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NCO1079_2_ward_identity",
            "claim": "diffeomorphism Ward identity owns source conservation",
            "statement": "on matter shell, diffeomorphism invariance of S_matter gives covariant conservation of the Hilbert source in the observed geometry",
            "proof_move": "move infinitesimal diffeomorphism through the common action and collect the coefficient of the generator",
            "result": "CONDITIONAL_WARD_IDENTITY",
            "gap": "conservation does not by itself fix relative source weights already inserted into S_matter",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NCO1079_3_post_variation_selector",
            "claim": "post-variation material selector is forbidden by current ownership",
            "statement": "if readout is downstream of variation, F(T_A,A) cannot redefine the source tensor that varied the geometry",
            "proof_move": "readout maps may project measured channels but cannot retroactively alter the variational source",
            "result": "KILLS_POST_VARIATION_SELECTOR_CONDITIONAL",
            "gap": "parent readout-order axiom remains a contract, not a full corpus theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NCO1079_4_current_rescaling",
            "claim": "J_A -> c_A J_A is not legal after Hilbert-source ownership",
            "statement": "once T_mu_nu is defined by variation, a later source-current rescaling is not a new parent source",
            "proof_move": "classify c_A after variation as readout/calibration, not action-source ownership",
            "result": "PARTIALLY_KILLED_AFTER_HILBERT_OWNER",
            "gap": "c_A can still be hidden as a pre-variation action coefficient unless action-measure/object-language clauses are signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NCO1079_5_species_action_weight",
            "claim": "S_matter = sum_A w_A S_A is killed by current ownership alone",
            "statement": "pre-variation species weights would be rejected by the current-owner subtheorem",
            "proof_move": "test whether Hilbert variation removes w_A when w_A is already inside S_matter",
            "result": "SURVIVES_PRE_VARIATION",
            "gap": "Hilbert stress simply inherits w_A; this needs action-measure/object-language ownership, not current ownership alone",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NCO1079_6_verdict",
            "claim": "narrow current-owner proof closes WEP theorem-zero",
            "statement": "current-owner subtheorem is strong enough to make P_WEP=0",
            "proof_move": "assemble Hilbert variation, Ward identity, post-variation selector kill, and pre-variation counterexample audit",
            "result": "NARROW_CURRENT_OWNER_PARTIAL_NOT_WEP_CLOSED",
            "gap": "post-variation tricks are conditionally killed, but pre-variation species weights survive",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def premise_ledger_rows() -> list[dict[str, str]]:
    return [
        {
            "premise_id": "PR1079_0_common_action",
            "premise": "one common ordinary-matter action before readout",
            "status": "UNSIGNED",
            "effect_if_signed": "lets Hilbert source owner apply to all ordinary matter sectors",
            "effect_if_unsigned": "species weights may be inserted before variation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "premise_id": "PR1079_1_variation_before_readout",
            "premise": "variation occurs before material/readout projection",
            "status": "CONDITIONAL_READOUT_CONTRACT",
            "effect_if_signed": "kills post-variation selector F(T_A,A)",
            "effect_if_unsigned": "readout can mimic composition-dependent source residuals",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "premise_id": "PR1079_2_hilbert_source_definition",
            "premise": "source tensor is the Hilbert variation of S_matter",
            "status": "EXACT_GIVEN_COMMON_ACTION",
            "effect_if_signed": "single variational source owner exists",
            "effect_if_unsigned": "current/source normalization remains undefined",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "premise_id": "PR1079_3_no_later_current_rescale",
            "premise": "no current rescaling after Hilbert source extraction",
            "status": "CONDITIONAL_ON_READOUT_ORDER",
            "effect_if_signed": "blocks J_A -> c_A J_A as a post-variation source redefinition",
            "effect_if_unsigned": "finite C_parent coefficient remains required",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "premise_id": "PR1079_4_no_pre_action_species_weight",
            "premise": "no w_A S_A inside S_matter",
            "status": "NOT_SIGNED",
            "effect_if_signed": "would close the major species-weight leak",
            "effect_if_unsigned": "WEP theorem-zero cannot close from current ownership alone",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def counterexample_resolution_rows() -> list[dict[str, str]]:
    return [
        {
            "counterexample_id": "CER1079_0_species_action_weight",
            "counterexample": "S_matter = sum_A w_A S_A",
            "1079_resolution": "SURVIVES",
            "reason": "Hilbert variation inherits w_A if it is inserted before variation",
            "needed_next": "object-language or action-measure owner, or finite sourced coefficient",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CER1079_1_current_rescaling",
            "counterexample": "J_A -> c_A J_A after source extraction",
            "1079_resolution": "KILLED_CONDITIONALLY",
            "reason": "post-variation current rescaling is not a variational source if Hilbert owner and readout order are signed",
            "needed_next": "parent readout-order signature",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CER1079_2_disconnected_material_components",
            "counterexample": "independent constants on disconnected material components",
            "1079_resolution": "SURVIVES",
            "reason": "current ownership cannot forbid constants inserted into disconnected action summands",
            "needed_next": "matter functor connectedness or finite material tensor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "counterexample_id": "CER1079_3_post_variation_selector",
            "counterexample": "post-variation selector F(T_A,A)",
            "1079_resolution": "KILLED_CONDITIONALLY",
            "reason": "readout cannot retroactively redefine the source under variation-before-readout",
            "needed_next": "official readout-order/readout-kernel contract",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def finite_source_vector_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "FSV1079_0_formula",
            "object": "finite WEP product formula",
            "required_content": "P_WEP = C_parent * <K_MICROSCOPE, R_source^Earth dot (R_TA6V - R_PtRh10)> with declared basis and units",
            "current_status": "FORMULA_CONTRACT_ONLY",
            "missing_for_claim": "numeric C_parent; numeric source vector; numeric material vector; official readout kernel",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "FSV1079_1_C_parent",
            "object": "C_parent coupling owner",
            "required_content": "parent coefficient, units, sign convention, normalization, and source path",
            "current_status": "MISSING_PARENT_COEFFICIENT",
            "missing_for_claim": "signed current/action owner or sourced finite coefficient",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "FSV1079_2_material_vector",
            "object": "R_TA6V - R_PtRh10",
            "required_content": "source-backed material response vector for test-mass compositions in the same basis as C_parent",
            "current_status": "TOY_VECTOR_ONLY",
            "missing_for_claim": "composition/material tensor source and uncertainty convention",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "FSV1079_3_source_vector",
            "object": "R_source^Earth",
            "required_content": "Earth/source worldtube response vector in the same basis as material vector",
            "current_status": "MISSING_SOURCE_VECTOR",
            "missing_for_claim": "source composition/profile or common-mode theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "FSV1079_4_readout_kernel",
            "object": "K_MICROSCOPE",
            "required_content": "official CMSM arrays/masks or accepted reconstruction with projection units",
            "current_status": "SURROGATE_ONLY",
            "missing_for_claim": "official arrays or validated replacement",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def finite_vector_template_rows() -> list[dict[str, str]]:
    return [
        {
            "vector_id": "VT1079_0_R_source_Earth",
            "arena": "MICROSCOPE_WEP",
            "leg": "source",
            "object": "R_source^Earth",
            "component_basis": "MISSING_PARENT_BASIS",
            "component_values": "MISSING_SOURCE_VECTOR",
            "units": "basis-dependent",
            "source_path": "MISSING_SOURCE_PATH",
            "source_row": "MISSING_SOURCE_ROW",
            "extraction_method": "source composition/profile or common-mode theorem required",
            "status": "MISSING_SOURCE_VECTOR",
            "valid_for_claim": "false",
            "notes": "no measured-G absorption; source leg must be explicit or parent-common-mode signed",
            "generated_utc": stamp(),
        },
        {
            "vector_id": "VT1079_1_R_TA6V_minus_PtRh10",
            "arena": "MICROSCOPE_WEP",
            "leg": "test",
            "object": "R_TA6V - R_PtRh10",
            "component_basis": "MISSING_PARENT_BASIS",
            "component_values": "TOY_VECTOR_NOT_ALLOWED_FOR_CLAIM",
            "units": "basis-dependent",
            "source_path": "MISSING_MATERIAL_SOURCE_PATH",
            "source_row": "MISSING_MATERIAL_SOURCE_ROW",
            "extraction_method": "composition/material tensor source required",
            "status": "TOY_ONLY_NONCLAIM",
            "valid_for_claim": "false",
            "notes": "toy row can guide schema only",
            "generated_utc": stamp(),
        },
        {
            "vector_id": "VT1079_2_C_parent",
            "arena": "MICROSCOPE_WEP",
            "leg": "coupling",
            "object": "C_parent",
            "component_basis": "MISSING_PARENT_BASIS",
            "component_values": "MISSING_COUPLING_OWNER",
            "units": "basis-dependent",
            "source_path": "MISSING_PARENT_SOURCE_PATH",
            "source_row": "MISSING_PARENT_SOURCE_ROW",
            "extraction_method": "signed current/action owner or finite coefficient derivation",
            "status": "MISSING_PARENT_COEFFICIENT",
            "valid_for_claim": "false",
            "notes": "current-owner partial theorem does not supply this coefficient",
            "generated_utc": stamp(),
        },
    ]


def material_tensor_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "tensor_id": "MTC1079_0_basis",
            "required_item": "basis declaration",
            "definition": "same component basis for C_parent, R_source, and R_material",
            "status": "MISSING_PARENT_BASIS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tensor_id": "MTC1079_1_test_mass_composition",
            "required_item": "Ti/Pt alloy composition and uncertainties",
            "definition": "TA6V and PtRh10 material inputs mapped into the response basis",
            "status": "MISSING_SOURCED_COMPOSITION_TABLE",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tensor_id": "MTC1079_2_response_map",
            "required_item": "material response map",
            "definition": "map from composition/binding content to R_A components with units",
            "status": "MISSING_RESPONSE_MAP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tensor_id": "MTC1079_3_uncertainty",
            "required_item": "uncertainty propagation",
            "definition": "uncertainty convention for vector components and product score",
            "status": "MISSING_UNCERTAINTY_MODEL",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def product_prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1079_0_WEP_current_owner_partial_nonclaim",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_FINITE_WEP_SOURCE_VECTOR_AFTER_PARTIAL_CURRENT_OWNER",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
            "inputs_present": "partial Hilbert current-owner theorem; finite source-vector contract",
            "required_inputs": "no pre-action species weight theorem OR numeric C_parent, R_source, R_material, K_readout",
            "derivation_status": "CURRENT_OWNER_PARTIAL_FINITE_INPUTS_MISSING",
            "valid_for_claim": "false",
            "notes": "post-variation source rescaling is conditionally killed, but WEP prediction is not numeric",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    row = local_bound_row("R1_WEP_source_charge")
    url, doi = split_reference(row.get("reference_path_or_url", ""))
    return [
        {
            "bound_id": "BOUND1079_0_MICROSCOPE_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": row["upper_bound"],
            "bound_units": row["units"],
            "bound_source": url,
            "source_row": f"{row['dataset_id']}:{row['row_id']};doi:{doi}",
            "bound_type": "upper_abs_WEP_proxy_bound",
            "valid_for_claim": "true",
            "notes": "source-backed numeric bound only; prediction remains invalid",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1079_0_WEP_current_owner_partial_product_stub",
            "prediction_rows": str(status.get("prediction_rows", "")),
            "bound_rows": str(status.get("bound_rows", "")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "passed_rows": str(status.get("passed_rows", "")),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject partial current-owner theorem and missing finite WEP vectors",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1079_0_hilbert_subtheorem",
            "claim_component": "Hilbert current-owner subtheorem",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "exact only after common action and variation-before-readout premises",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1079_1_WEP_theorem_zero",
            "claim_component": "WEP theorem-zero",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "pre-variation species action weight survives current-owner proof",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1079_2_finite_source_vector",
            "claim_component": "finite WEP source vector",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "R_source^Earth is missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1079_3_finite_material_tensor",
            "claim_component": "finite WEP material tensor",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "R_TA6V - R_PtRh10 is toy-only/nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1079_4_product_runner",
            "claim_component": "WEP product runner",
            "gate_pass": "false",
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1079_0_partial_win",
            "decision": "retain Hilbert-current ownership as a conditional subtheorem",
            "because": "inside a common action, variation-before-readout gives a unique source tensor",
            "next_action": "use it to forbid post-variation selectors only after readout order is signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1079_1_not_WEP_closed",
            "decision": "do not promote current-owner proof to WEP theorem-zero",
            "because": "pre-variation species weights survive and are outside current ownership",
            "next_action": "route WEP through finite source/material vectors unless object/action owner proof reopens",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1079_2_acquisition_route",
            "decision": "begin finite WEP source-vector/material-tensor acquisition pack",
            "because": "it is now the least dishonest scoreable route",
            "next_action": "build the first real R_source, R_material, C_parent, K_readout input pack",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1079_0_1080",
            "next_target": "1080-Y5-R10-finite-WEP-source-vector-and-material-tensor-acquisition-pack.md",
            "objective": "build the first finite WEP input acquisition pack: source-backed Earth/source vector, Ti/Pt material response tensor contract, C_parent coefficient contract, and official/surrogate readout gate; keep product invalid until all rows are numeric and sourced.",
            "include": "R_source^Earth; R_TA6V - R_PtRh10; C_parent; K_MICROSCOPE; units; basis; provenance; runner refusal",
            "exclude": "toy vector as evidence; measured-G absorption; tau=1; Delta_w=0 by taste; public claim; GitHub; formalization edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def csv_rows_parse(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
    except csv.Error:
        return False
    return True


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    premise_rows: list[dict[str, str]],
    counter_rows: list[dict[str, str]],
    finite_contract_rows: list[dict[str, str]],
    vector_rows: list[dict[str, str]],
    tensor_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1079_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1079_1_hilbert_subtheorem", any(row["theorem_id"] == "NCO1079_1_hilbert_variation" and row["result"] == "EXACT_SUBTHEOREM_CONDITIONAL" for row in theorem_rows), "Hilbert-current owner subtheorem is captured"))
    checks.append(("V1079_2_not_WEP_closed", any(row["theorem_id"] == "NCO1079_6_verdict" and row["result"] == "NARROW_CURRENT_OWNER_PARTIAL_NOT_WEP_CLOSED" for row in theorem_rows), "narrow current-owner proof does not close WEP"))
    checks.append(("V1079_3_pre_action_weight_survives", any(row["theorem_id"] == "NCO1079_5_species_action_weight" and row["result"] == "SURVIVES_PRE_VARIATION" for row in theorem_rows), "pre-variation species action weight survives"))
    checks.append(("V1079_4_premise_ledger_safe", any(row["premise_id"] == "PR1079_4_no_pre_action_species_weight" and row["status"] == "NOT_SIGNED" for row in premise_rows), "premise ledger records missing no-species-weight theorem"))
    checks.append(("V1079_5_counterexample_matrix", len(counter_rows) == 4 and any(row["counterexample_id"] == "CER1079_0_species_action_weight" and row["1079_resolution"] == "SURVIVES" for row in counter_rows), "counterexample resolution matrix is explicit"))
    checks.append(("V1079_6_finite_contract_nonclaim", len(finite_contract_rows) == 5 and all(row["valid_for_claim"] == "false" for row in finite_contract_rows), "finite WEP contract rows are nonclaim"))
    checks.append(("V1079_7_vector_templates_nonclaim", len(vector_rows) == 3 and all(row["valid_for_claim"] == "false" and ("MISSING" in row["component_values"] or "TOY" in row["component_values"]) for row in vector_rows), "finite vector template remains missing/toy nonclaim"))
    checks.append(("V1079_8_material_tensor_contract", len(tensor_rows) == 4 and all(row["valid_for_claim"] == "false" for row in tensor_rows), "material tensor contract remains nonclaim"))
    checks.append(("V1079_9_prediction_nonclaim_missing", any("MISSING_FINITE_WEP_SOURCE_VECTOR" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows), "prediction row remains missing finite WEP inputs"))
    checks.append(("V1079_10_bound_numeric", bool(bound_rows_) and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "bound import is positive numeric"))
    checks.append(("V1079_11_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "runner reports no valid prediction rows and claim false"))
    checks.append(("V1079_12_claim_gates_safe", all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1079_13_next_target", any(row["next_target"].startswith("1080-Y5-R10-finite-WEP") for row in next_rows), "1080 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1079_14_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1079_15_csv_parse", all(path.exists() and csv_rows_parse(path) for path in outputs.values() if path.suffix == ".csv" and path.name != "P8_Y5_BRR545_1079_VALIDATION.csv"), "all 1079 CSV outputs parse cleanly"))
    checks.append(("V1079_16_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1079_SUMMARY", True, "Hilbert current-owner subtheorem retained; pre-variation species weights survive; finite WEP source-vector acquisition becomes next route; claim blocked"))
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]


def write_doc(
    source_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    premise_rows: list[dict[str, str]],
    counter_rows: list[dict[str, str]],
    finite_contract_rows: list[dict[str, str]],
    vector_rows: list[dict[str, str]],
    tensor_rows: list[dict[str, str]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparison_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1079 - Parent current-owner narrow proof or finite WEP source vector",
            "",
            "## Current verdict",
            "1079 gets a real but narrow win: inside a common parent matter action, Hilbert variation before readout gives a unique source owner and conditionally kills post-variation source selectors. It does not close WEP theorem-zero, because species weights inserted before variation are inherited by the Hilbert stress. The honest next route is finite WEP input acquisition: C_parent, R_source^Earth, R_TA6V - R_PtRh10, and K_MICROSCOPE.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Narrow current-owner theorem attempt",
            md_table(theorem_rows, ["theorem_id", "claim", "result", "gap"]),
            "## Premise ledger",
            md_table(premise_rows, ["premise_id", "premise", "status", "effect_if_unsigned"]),
            "## Counterexample resolution matrix",
            md_table(counter_rows, ["counterexample_id", "counterexample", "1079_resolution", "reason", "needed_next"]),
            "## Finite WEP source-vector contract",
            md_table(finite_contract_rows, ["contract_id", "object", "current_status", "missing_for_claim"]),
            "## Finite vector template",
            md_table(vector_rows, ["vector_id", "object", "component_basis", "component_values", "status", "valid_for_claim"]),
            "## Material tensor contract",
            md_table(tensor_rows, ["tensor_id", "required_item", "status", "definition"]),
            "## Nonclaim product candidate",
            md_table(prediction_rows, ["prediction_id", "product_symbol", "product_value", "derivation_status", "valid_for_claim"]),
            "## Bound import",
            md_table(bound_rows_, ["bound_id", "product_symbol", "bound_value", "bound_units", "valid_for_claim"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparison_rows, ["comparison_id", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    theorem_rows = narrow_current_owner_rows()
    premise_rows = premise_ledger_rows()
    counter_rows = counterexample_resolution_rows()
    finite_contract_rows = finite_source_vector_contract_rows()
    vector_rows = finite_vector_template_rows()
    tensor_rows = material_tensor_contract_rows()
    prediction_rows = product_prediction_rows()
    bound_rows_ = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1079_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
        "premise_ledger": OUT / "P8_Y5_R10_1079_CURRENT_OWNER_PREMISE_LEDGER.csv",
        "counterexamples": OUT / "P8_Y5_R10_1079_COUNTEREXAMPLE_RESOLUTION_MATRIX.csv",
        "finite_contract": OUT / "P8_Y5_R10_1079_FINITE_WEP_SOURCE_VECTOR_CONTRACT.csv",
        "vector_template": OUT / "P8_Y5_R10_1079_FINITE_VECTOR_TEMPLATE_NONCLAIM.csv",
        "material_tensor": OUT / "P8_Y5_R10_1079_MATERIAL_TENSOR_CONTRACT.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1079_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1079_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1079_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1079_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1079_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1079_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["theorem"], theorem_rows)
    write_csv(outputs["premise_ledger"], premise_rows)
    write_csv(outputs["counterexamples"], counter_rows)
    write_csv(outputs["finite_contract"], finite_contract_rows)
    write_csv(outputs["vector_template"], vector_rows)
    write_csv(outputs["material_tensor"], tensor_rows)
    write_csv(outputs["prediction"], prediction_rows, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    claim_rows = claim_gate_rows(product_status)

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_result["comparisons"])
    write_csv(outputs["claim_gates"], claim_rows)

    remove_pycache()
    validation_rows = validate_outputs(
        outputs,
        source_rows,
        theorem_rows,
        premise_rows,
        counter_rows,
        finite_contract_rows,
        vector_rows,
        tensor_rows,
        prediction_rows,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        theorem_rows,
        premise_rows,
        counter_rows,
        finite_contract_rows,
        vector_rows,
        tensor_rows,
        prediction_rows,
        bound_rows_,
        product_status_rows_,
        product_result["comparisons"],
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
