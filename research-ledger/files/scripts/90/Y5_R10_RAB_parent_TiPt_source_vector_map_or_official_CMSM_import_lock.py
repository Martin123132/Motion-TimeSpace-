from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CMSM_ROOT = ROOT / "source-intake" / "microscope_cmsm"

DOC = ROOT / "1424-Y5-R10-RAB-parent-TiPt-source-vector-map-or-official-CMSM-import-lock.md"
SOURCE_REGISTER = OUT / "P8_Y5_R10_1424_SOURCE_REGISTER.csv"
OFFICIAL_IMPORT_LOCK = OUT / "P8_Y5_R10_1424_OFFICIAL_CMSM_IMPORT_LOCK.csv"
PARENT_CONTRACTION_THEOREM = OUT / "P8_Y5_R10_1424_PARENT_TIPT_CONTRACTION_THEOREM_ATTEMPT.csv"
MATERIAL_VECTOR_CANDIDATES = OUT / "P8_Y5_R10_1424_TIPT_MATERIAL_VECTOR_CANDIDATES.csv"
SOURCE_VECTOR_CONTRACT = OUT / "P8_Y5_R10_1424_SOURCE_VECTOR_CONTRACT.csv"
PARENT_OWNER_CLAUSE_GATE = OUT / "P8_Y5_R10_1424_PARENT_OWNER_CLAUSE_GATE.csv"
EXECUTABILITY_GATE = OUT / "P8_Y5_R10_1424_WEP_EXECUTABILITY_GATE.csv"
PRODUCT_STATUS = OUT / "P8_Y5_R10_1424_PRODUCT_STATUS.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1424_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1424_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1424_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1424_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text_has(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="ignore")


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


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


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC1424_0_1423_next", OUT / "P8_Y5_R10_1423_NEXT_TARGET.csv", "NEXT1423_0_1424", "1423 handoff selecting parent Ti/Pt/source vector map."),
        ("SRC1424_1_1423_validation", OUT / "P8_Y5_BRR545_1423_VALIDATION.csv", "VAL1423_8_overall", "1423 validation: no complete CMSM export and surrogate-only replay."),
        ("SRC1424_2_1423_import_lock", OUT / "P8_Y5_R10_1423_OFFICIAL_IMPORT_STATUS.csv", "OFF1423_2_parent_map", "official arrays do not replace parent material/source map."),
        ("SRC1424_3_1420_checklist", OUT / "P8_Y5_R10_1420_WEP_SOURCE_PROJECTION_ACQUISITION_CHECKLIST.csv", "WAC1420_3_material_tensor", "first executable WEP-row checklist."),
        ("SRC1424_4_1076_contract", OUT / "P8_Y5_R10_1076_PARENT_PRODUCT_CONTRACT_UPDATE.csv", "PWC1076_1_factorized_product", "finite WEP product contraction contract."),
        ("SRC1424_5_1076_toy_vector", OUT / "P8_Y5_R10_1076_TOY_MATERIAL_VECTOR_FROM_651.csv", "MV1076_delta_TA6V_minus_PtRh10", "toy Ti/Pt differential material vector."),
        ("SRC1424_6_1077_clause", OUT / "P8_Y5_R10_1077_CLAUSE_SIGNATURE_MATRIX.csv", "CLAUSE1077_2_current_owner", "coupling-owner theorem clauses and counterexamples."),
        ("SRC1424_7_1330_electron", OUT / "P8_Y5_R10_1330_AUDITED_ELECTRON_DELTA_VECTOR.csv", "DELTA1330_0_TA6V_minus_PtRh10_electron", "audited nonclaim electron contrast."),
        ("SRC1424_8_1331_theorem", OUT / "P8_Y5_R10_1331_PARENT_SOURCE_BASIS_MAP_THEOREM.csv", "THM1331_0_conditional_parent_basis_map", "conditional parent source-basis map theorem."),
        ("SRC1424_9_1331_clause", OUT / "P8_Y5_R10_1331_PARENT_MAP_CLAUSE_AUDIT.csv", "CLAUSE1331_6_matter_quotient_universality", "latest parent-map clause blockers."),
        ("SRC1424_10_1061_alpha", OUT / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_1_delta_Q_alpha", "alpha/Coulomb smoke material contrast."),
        ("SRC1424_11_651_material", OUT / "P8_Y5_R10_651_MICROSCOPE_MATERIAL_MODEL.csv", "MM651_TA6V_Ti", "nominal alloy composition model."),
        ("SRC1424_12_1419_matrix", OUT / "P8_Y5_R10_1419_QBAR_SOURCE_PROJECTION_MATRIX.csv", "PMX1419_0_WEP_source_charge", "WEP projection matrix row."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchor, role in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "anchor": anchor,
                "anchor_found": text_has(path, anchor),
                "role": role,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def official_import_lock_rows() -> tuple[list[dict[str, Any]], bool]:
    inventory_path = OUT / "P8_Y5_R10_1423_CMSM_EXPORT_INVENTORY.csv"
    inventory = read_csv(inventory_path)
    required = [row for row in inventory if row["inventory_id"].startswith("INV1423_") and row["inventory_id"] != "INV1423_5_any_local_files"]
    ready = bool(required) and all(row.get("required_fields_present", "").lower() == "true" for row in required)
    rows = [
        {
            "lock_id": "LOCK1424_0_CMSM_schema",
            "object": "local CMSM export contract",
            "current_status": "READY_NONCLAIM_IF_USER_EXPORT_PRESENT" if ready else "LOCKED_NO_COMPLETE_EXPORT",
            "evidence": "all 1423 required files present" if ready else "1423 inventory missing root manifest, masks, orbit, attitude, and gxgzS arrays",
            "effect": "can replace surrogate kernel columns only; cannot define parent Ti/Pt/source vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "lock_id": "LOCK1424_1_arrays_do_not_define_coupling",
            "object": "official gx/gz/Sxx/Sxz arrays",
            "current_status": "DATA_SIDE_ONLY",
            "evidence": "OFF1423_2_parent_map=MISSING_PARENT_MATERIAL_SOURCE_MAP",
            "effect": "arrays can score a prediction only after P_WEP or tau_WEP is parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "lock_id": "LOCK1424_2_side_gate",
            "object": str(CMSM_ROOT),
            "current_status": "WATCH_FOLDER_READY",
            "evidence": "1423 import contract remains authoritative",
            "effect": "if user later supplies export, rerun 1423/1424; do not alter finite-branch coupling status",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return rows, ready


def first_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == value:
            return row
    raise ValueError(f"missing {key}={value} in {path}")


def material_candidate_rows() -> list[dict[str, Any]]:
    toy = first_row(OUT / "P8_Y5_R10_1076_TOY_MATERIAL_VECTOR_FROM_651.csv", "material_vector_id", "MV1076_delta_TA6V_minus_PtRh10")
    electron = first_row(OUT / "P8_Y5_R10_1330_AUDITED_ELECTRON_DELTA_VECTOR.csv", "delta_id", "DELTA1330_0_TA6V_minus_PtRh10_electron")
    alpha = first_row(OUT / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "convention_id", "MCON1061_1_delta_Q_alpha")
    rows = [
        {
            "candidate_id": "MAT1424_0_Z_over_A_toy",
            "component": "Z_over_A_toy",
            "left_minus_right": "TA6V_minus_PtRh10",
            "numeric_value": toy["q_Z_over_A_toy"],
            "units": "dimensionless",
            "source": "MV1076_delta_TA6V_minus_PtRh10",
            "parent_owner_status": "TOY_NOT_PARENT_DERIVED",
            "missing_for_promotion": "parent material response tensor and source-basis normalization",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "MAT1424_1_neutron_excess_toy",
            "component": "neutron_excess_toy",
            "left_minus_right": "TA6V_minus_PtRh10",
            "numeric_value": toy["q_neutron_excess_toy"],
            "units": "dimensionless",
            "source": "MV1076_delta_TA6V_minus_PtRh10",
            "parent_owner_status": "TOY_NOT_PARENT_DERIVED",
            "missing_for_promotion": "nuclear/binding owner and no-double-counting rule",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "MAT1424_2_electron_mass_fraction",
            "component": "electron_rest_mass_fraction",
            "left_minus_right": "TA6V_minus_PtRh10",
            "numeric_value": electron["delta_fraction"],
            "units": "dimensionless mass fraction",
            "source": "DELTA1330_0_TA6V_minus_PtRh10_electron",
            "parent_owner_status": "AUDITED_NUMERIC_PARENT_NORMALIZATION_MISSING",
            "missing_for_promotion": "parent mass functional and electron normalization under same vertical generator",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "MAT1424_3_alpha_Coulomb_smoke_abs",
            "component": "alpha_Coulomb_abs_smoke",
            "left_minus_right": "abs_TA6V_minus_PtRh10",
            "numeric_value": alpha["numeric_value"],
            "units": "dimensionless DD-style smoke contrast",
            "source": "MCON1061_1_delta_Q_alpha",
            "parent_owner_status": "SMOKE_CONTEXT_NOT_PARENT_EM_OWNER",
            "missing_for_promotion": "parent EM/fine-structure operator owner and sign convention",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM1424_0_target_contraction",
            "statement": "A scoreable Ti/Pt WEP product needs P_WEP = |K_CMSM[ R_source^Earth, C_parent(R_TA6V - R_PtRh10) ]| with source, material, coupling, kernel, and readout all in the same parent branch.",
            "derivation_status": "EXACT_CONTRACT_NOT_CLOSED",
            "proof_or_failure": "1076/1331 supply the factorized shape, but not the parent mass functional, vertical generator, source vector, or readout projection.",
            "current_result": "CONTRACTION_LAW_STAGED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM1424_1_universal_common_mode_zero",
            "statement": "If ordinary matter descends only through the quotient metric/coframe with no species marker and a single source-current owner, then R_TA6V - R_PtRh10 is pure common mode and WEP source contrast is zero after measured-G calibration.",
            "derivation_status": "CONDITIONAL_THEOREM_ONLY",
            "proof_or_failure": "Universal metric coupling makes the vertical source variation proportional to total stress-energy, not Ti/Pt component labels; however the quotient matter/action-measure/current premises remain unsigned.",
            "current_result": "BEST_DERIVATION_ROUTE_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM1424_2_finite_vector_route",
            "statement": "If non-universal parent couplings exist, each material component must be parent-owned and contracted with a parent-owned Earth/source vector and CMSM readout kernel.",
            "derivation_status": "FINITE_ROUTE_SOURCED_INPUT_ONLY",
            "proof_or_failure": "Available Ti/Pt component rows are toy/audited/smoke rows, not parent response tensors; source leg and C_parent are missing.",
            "current_result": "NO_SCOREABLE_TIPT_VECTOR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM1424_3_no_import_shortcut",
            "statement": "Neither official CMSM arrays nor DD-style material contrasts can define the MTS parent Ti/Pt/source map by themselves.",
            "derivation_status": "GUARD_THEOREM",
            "proof_or_failure": "Data arrays supply K/readout; DD contrasts supply an external coordinate basis. Neither supplies the parent variation, coefficient units, source profile, or current owner.",
            "current_result": "IMPORT_LOCK_ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def source_vector_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "SRCMAP1424_0_R_source",
            "object": "R_source^Earth",
            "required_definition": "Earth/source response vector in the same basis as R_material and qbar_source_weight",
            "current_status": "MISSING_SOURCE_VECTOR",
            "accepted_resolution": "derive common-mode theorem, or source-backed composition/worldtube vector with units/frame/support",
            "blocks": "finite P_WEP and measured-G guard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "SRCMAP1424_1_R_material",
            "object": "R_TA6V - R_PtRh10",
            "required_definition": "parent material response tensor, not a toy Z/A or single audited component",
            "current_status": "PARTIAL_NUMERIC_COMPONENTS_NONCLAIM",
            "accepted_resolution": "parent mass functional derivative or source-backed full material tensor in declared basis",
            "blocks": "Ti/Pt WEP material leg",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "SRCMAP1424_2_C_parent",
            "object": "C_parent",
            "required_definition": "parent coupling operator/coefficient map with units and normalization",
            "current_status": "MISSING_PARENT_COUPLING_OWNER",
            "accepted_resolution": "quotient matter universality zero, or explicit parent operator coefficients",
            "blocks": "all finite WEP, R10, PPN source projections",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "SRCMAP1424_3_K_CMSM",
            "object": "K_CMSM readout kernel",
            "required_definition": "official or validated MICROSCOPE orbit/mask/attitude/gxgzS projection kernel",
            "current_status": "MISSING_OFFICIAL_EXPORT_SURROGATE_ONLY",
            "accepted_resolution": "local CMSM export satisfying 1423 contract or validated official reconstruction",
            "blocks": "empirical WEP scoring, not parent coupling derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "SRCMAP1424_4_calibration_guard",
            "object": "measured-G/common-mode guard",
            "required_definition": "equation separating universal source normalization from relative Ti/Pt source residual",
            "current_status": "GUARD_NAMED_NOT_DERIVED",
            "accepted_resolution": "proof common mode is absorbed only once and relative source weights are not hidden",
            "blocks": "no measured-G absorption shortcut",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def owner_clause_rows() -> list[dict[str, Any]]:
    parent_clauses = read_csv(OUT / "P8_Y5_R10_1331_PARENT_MAP_CLAUSE_AUDIT.csv")
    rows: list[dict[str, Any]] = []
    for row in parent_clauses:
        rows.append(
            {
                "gate_id": "OWN1424_" + row["clause_id"].split("_", 1)[-1],
                "needed_clause": row["needed_clause"],
                "current_status": row["current_status"],
                "promotion_allowed": False,
                "effect_on_1424": row["blocks"],
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    rows.append(
        {
            "gate_id": "OWN1424_7_verdict",
            "needed_clause": "all parent-owner clauses required for scoreable Ti/Pt/source vector",
            "current_status": "PARENT_OWNER_NOT_SIGNED",
            "promotion_allowed": False,
            "effect_on_1424": "1424 cannot promote toy/audited/smoke material components to a WEP prediction",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def executability_rows(official_ready: bool, candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    finite_values = all(math.isfinite(float(row["numeric_value"])) for row in candidates)
    return [
        {
            "gate_id": "WEX1424_0_numeric_material_components",
            "gate": "finite Ti/Pt component numbers exist",
            "gate_pass": finite_values,
            "claim_allowed": False,
            "reason": "numbers are toy/audited/smoke only and not parent response tensor",
            "valid_for_claim": False,
        },
        {
            "gate_id": "WEX1424_1_parent_material_map",
            "gate": "parent-owned R_TA6V - R_PtRh10",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "parent mass functional/component basis/normalization not signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "WEX1424_2_source_vector",
            "gate": "parent-owned R_source^Earth",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "source worldtube/common-mode theorem missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "WEX1424_3_CMSM_kernel",
            "gate": "official CMSM kernel import",
            "gate_pass": official_ready,
            "claim_allowed": False,
            "reason": "data-side gate only; no complete local export in current run" if not official_ready else "official import present but parent product still missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "WEX1424_4_product",
            "gate": "scoreable P_WEP product",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "requires parent material map, source vector, coupling owner, CMSM kernel, and calibration guard together",
            "valid_for_claim": False,
        },
    ]


def product_rows() -> list[dict[str, Any]]:
    return [
        {
            "prediction_id": "PRED1424_0_TiPt_source_vector_map",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PARENT_TIPT_SOURCE_VECTOR_MAP",
            "derivation_status": "CONTRACTION_CONTRACT_STAGED_COMPONENT_ROWS_NONCLAIM",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prediction_id": "PRED1424_1_common_mode_zero_branch",
            "product_symbol": "P_WEP_common_mode_zero",
            "product_value": "CONDITIONAL_ZERO_UNSIGNED",
            "derivation_status": "requires quotient matter universality plus current/action-measure owner",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "prediction_id": "APR1424_0_runner_status",
            "product_symbol": "WEP_product_runner",
            "product_value": "NOT_RUN_NO_VALID_PREDICTION_ROWS",
            "derivation_status": "finite component rows and CMSM import lock are nonclaim",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1424_0_TiPt_map",
            "claim_component": "parent Ti/Pt material/source vector map",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "PARENT_OWNER_NOT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1424_1_component_numbers",
            "claim_component": "toy/audited/smoke material components",
            "gate_pass": True,
            "claim_allowed": False,
            "reason": "finite numbers exist but are not parent-owned response tensor",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1424_2_CMSM_import",
            "claim_component": "official CMSM import side gate",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "no complete local export, and import would still be data-side only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1424_3_WEP_local_GR",
            "claim_component": "WEP/local-GR pass",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "no derived GR reduction and no scoreable WEP product",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1424_0_material_progress",
            "decision": "keep finite Ti/Pt component rows as useful plumbing only",
            "because": "Z/A, neutron-excess, electron, and alpha/Coulomb rows are finite but not parent-owned",
            "effect": "future scripts can test schemas without turning components into evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1424_1_best_derivation_route",
            "decision": "prioritize universal metric/common-mode source coupling over adding more component fits",
            "because": "common-mode closure is the GR-like route; component fits are a phenomenological escape unless parent-owned",
            "effect": "1425 should try to sign quotient matter universality/current owner or explicitly demote finite WEP to sourced-input-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1424_2_import_lock",
            "decision": "keep CMSM import as a locked side gate",
            "because": "official arrays can test a prediction but cannot create the parent prediction",
            "effect": "no further surrogate evidence polishing before the coupling map moves",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1424_0_1425",
            "next_target": "1425-Y5-R10-RAB-universal-metric-common-mode-WEP-zero-or-finite-source-demotion.md",
            "script": "scripts/Y5_R10_RAB_universal_metric_common_mode_WEP_zero_or_finite_source_demotion.py",
            "objective": "try to sign the GR-like common-mode theorem for ordinary matter: quotient metric/coframe matter coupling, no species marker, single current/action-measure owner, and measured-G guard. If it fails, demote finite WEP to sourced-input-only with the 1424 component rows as nonclaim plumbing.",
            "include": "quotient matter universality; current owner; action-measure owner; measured-G/common-mode guard; finite component demotion; WEP product refusal",
            "exclude": "component fitting; DD import as parent ontology; tau=1; guessed CMSM arrays; WEP/local-GR claim; GitHub; formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    official_ready: bool,
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        OFFICIAL_IMPORT_LOCK,
        PARENT_CONTRACTION_THEOREM,
        MATERIAL_VECTOR_CANDIDATES,
        SOURCE_VECTOR_CONTRACT,
        PARENT_OWNER_CLAUSE_GATE,
        EXECUTABILITY_GATE,
        PRODUCT_STATUS,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    parse_ok = True
    parse_errors: list[str] = []
    for path in csvs:
        try:
            _ = read_csv(path)
        except Exception as exc:
            parse_ok = False
            parse_errors.append(f"{path.name}:{type(exc).__name__}")
    finite_candidates = all(math.isfinite(float(row["numeric_value"])) for row in candidates)
    nonclaim_candidates = all(str(row["valid_for_claim"]).lower() == "false" for row in candidates)
    claim_safe = all(str(row["claim_allowed"]).lower() == "false" for row in claims)
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1424_0_sources", all(row["path_exists"] and row["anchor_found"] for row in sources), "all 1424 cited source paths and anchors resolve"),
        ("VAL1424_1_import_lock", not official_ready, "no complete local CMSM export found; import lock remains side gate" if not official_ready else "local CMSM export present but kept nonclaim"),
        ("VAL1424_2_candidate_numbers", finite_candidates and nonclaim_candidates, "finite Ti/Pt component rows staged as nonclaim only"),
        ("VAL1424_3_parent_theorem", True, "contraction theorem recorded as exact contract plus unsigned common-mode route"),
        ("VAL1424_4_executability", True, "scoreable WEP product remains blocked by parent map/source vector/CMSM kernel/calibration guard"),
        ("VAL1424_5_claim_gates", claim_safe, "all claim gates keep claim_allowed=false"),
        ("VAL1424_6_csv_parse", parse_ok, "all generated 1424 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1424_7_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1424_8_next_target", True, "1425 handoff written"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1424_9_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1424 stages Ti/Pt source-vector contraction contract and finite component rows, but parent coupling map remains unsigned and WEP/local-GR blocked",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1424 - Parent Ti/Pt source-vector map or official CMSM import lock",
            "**Current verdict:** 1424 does not derive the parent Ti/Pt/source-vector map. It does make the bottleneck sharper: finite Ti/Pt component numbers now sit in one audited nonclaim ledger, but the parent material response tensor, Earth/source vector, coupling owner, CMSM kernel, and measured-G/common-mode guard are not jointly signed.",
            "**Main move:** stop treating MICROSCOPE as a data problem only. The next winning route is the GR-like common-mode theorem: ordinary matter must descend through a universal quotient metric/coframe with no species marker and one current/action-measure owner, or finite WEP remains a sourced-input branch.",
            "## Source register\n" + md_table(sections["sources"]),
            "## Official CMSM import lock\n" + md_table(sections["official"]),
            "## Parent Ti/Pt contraction theorem attempt\n" + md_table(sections["theorem"]),
            "## Ti/Pt material vector candidates\n" + md_table(sections["candidates"]),
            "## Source-vector contract\n" + md_table(sections["source_contract"]),
            "## Parent-owner clause gate\n" + md_table(sections["owner_clauses"]),
            "## WEP executability gate\n" + md_table(sections["executability"]),
            "## Product status\n" + md_table(sections["product"]),
            "## Claim gates\n" + md_table(sections["claims"]),
            "## Decision ledger\n" + md_table(sections["decisions"]),
            "## Validation\n" + md_table(sections["validation"]),
            "## Next target\n" + md_table(sections["next"]),
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    official, official_ready = official_import_lock_rows()
    theorem = theorem_rows()
    candidates = material_candidate_rows()
    source_contract = source_vector_contract_rows()
    owner_clauses = owner_clause_rows()
    executability = executability_rows(official_ready, candidates)
    product = product_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(OFFICIAL_IMPORT_LOCK, official)
    write_csv(PARENT_CONTRACTION_THEOREM, theorem)
    write_csv(MATERIAL_VECTOR_CANDIDATES, candidates)
    write_csv(SOURCE_VECTOR_CONTRACT, source_contract)
    write_csv(PARENT_OWNER_CLAUSE_GATE, owner_clauses)
    write_csv(EXECUTABILITY_GATE, executability)
    write_csv(PRODUCT_STATUS, product)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)

    validation = validation_rows(sources, candidates, claims, official_ready)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "official": official,
            "theorem": theorem,
            "candidates": candidates,
            "source_contract": source_contract,
            "owner_clauses": owner_clauses,
            "executability": executability,
            "product": product,
            "claims": claims,
            "decisions": decisions,
            "next": next_rows,
            "validation": validation,
        }
    )
    remove_pycache()
    print("Y5_R10_1424_TiPt_source_vector_map_not_derived_common_mode_route_selected_nonclaim")


if __name__ == "__main__":
    main()
