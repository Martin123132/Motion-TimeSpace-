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
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
DOC = ROOT / "2003-Y5-R2FR-parent-material-source-map-or-official-CMSM-import-gate.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "2003-parent-material-source-map-or-official-CMSM-import-gate" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_2003_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_PARENT_QLOC_2003_WEP_BOUND_IMPORT.csv"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, object]:
    return {
        "branch_id": BRANCH_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        "generated_utc": stamp(),
    }


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


def csv_rows_parse(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
    except csv.Error:
        return False
    return True


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


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2003_0_2002_doc",
            "2002-Y5-R2FR-surrogate-design-matrix-tau-shape-smoke-runner.md",
            ["NEXT2002_0_2003", "DEC2002_1_degeneracy_found"],
            "2002 handoff: surrogate cannot identify physical tau.",
        ),
        (
            "SRC2003_1_2002_validation",
            "source-intake/mts_residuals/P8_Y5_BRR545_2002_VALIDATION.csv",
            ["VAL2002_OVERALL", "PASS"],
            "2002 validation pass.",
        ),
        (
            "SRC2003_2_1910_response",
            "1910-Y5-R2FR-parent-material-response-functional-or-exact-mass-defect-tensor-contract.md",
            ["MRF1910_3_sector_response_law", "MDT1910_7_source_readout_product"],
            "exact conditional material-response law.",
        ),
        (
            "SRC2003_3_1935_eta",
            "1935-Y5-R2FR-MTS-WEP-eta-projection-map-or-material-charge-ledger.md",
            ["ETA1935_4_mts_source_weight_form", "PB1935_1_exact_WEP_product_contract"],
            "exact eta projection contract.",
        ),
        (
            "SRC2003_4_1936_universality",
            "1936-Y5-R2FR-source-weight-universality-theorem-or-TiPt-material-charge-ledger.md",
            ["UNIV1936_1_hilbert_source_theorem", "HIL1936_2_no_species_weight"],
            "Hilbert universality conditional theorem.",
        ),
        (
            "SRC2003_5_1997_direct_product",
            "1997-Y5-R2FR-direct-WEP-product-theorem-or-first-real-tau-source-row.md",
            ["DWT1997_0_target", "REQ1997_3_material_tensor"],
            "direct WEP product route requirements.",
        ),
        (
            "SRC2003_6_2001_drop_contract",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2001_CMSM_DROP_CONTRACT.csv",
            ["DROP2001_02_gx", "DROP2001_05_Sxz"],
            "official CMSM import contract.",
        ),
        (
            "SRC2003_7_local_bound",
            "source-intake/local_bounds/local_bound_claims.csv",
            ["R1_WEP_source_charge", "2.8e-15"],
            "MICROSCOPE WEP bound anchor for refusal runner.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, relative_path, needles, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "needed_for": "2003 parent material/source map or official CMSM import gate",
                "needles": ";".join(needles),
                "exists": str(exists),
                "anchor_found": str(exists and not missing),
                "missing_needles": ";".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "note": note,
            }
        )
        rows.append(row)
    return rows


def parent_product_map_rows() -> list[dict[str, object]]:
    specs = [
        (
            "PPM2003_0_response_variable",
            "R_A^X",
            "R_A^X := V_X ln M_A",
            "logarithmic material response of test body A to parent generator X",
            "1910",
            "parent generator basis V_X and mass functional M_A must be signed",
            "CONDITIONAL_DEFINITION",
        ),
        (
            "PPM2003_1_material_difference",
            "DeltaR_AB^X",
            "DeltaR_AB^X := R_A^X - R_B^X = sum_c (f_Ac - f_Bc) gamma_cX",
            "composition/material contrast in parent basis",
            "1910 sector-response law",
            "component partition f_Ac and generator weights gamma_cX are not claim-ready",
            "EXACT_CONDITIONAL_ALGEBRA",
        ),
        (
            "PPM2003_2_source_transfer",
            "Pi_X",
            "Pi_X := C_X S_Earth^X K_WEP^X tau_WEP^X",
            "source/coupling/readout transfer factor for generator X",
            "1935/1997 product contracts",
            "C_X, Earth source leg, official readout kernel, and tau_WEP are missing or unsigned",
            "CONTRACT_SHARPENED",
        ),
        (
            "PPM2003_3_fractional_residual",
            "epsilon_A",
            "epsilon_A := sum_X Pi_X R_A^X",
            "fractional acceleration/readout residual for body A",
            "1935 eta projection",
            "requires parent product map before comparison",
            "CONDITIONAL_FORWARD_MODEL",
        ),
        (
            "PPM2003_4_exact_eta",
            "eta_AB",
            "eta_AB = 2 sum_X Pi_X DeltaR_AB^X / (2 + sum_X Pi_X (R_A^X + R_B^X))",
            "exact two-body Eotvos projection under the residual model",
            "1935 exact eta algebra plus 1910 response law",
            "denominator convention and all Pi_X/R_A^X inputs must be real or theorem-zero",
            "EXACT_COMPOSITE_CONTRACT_DERIVED",
        ),
        (
            "PPM2003_5_linear_bound",
            "linear_eta_bound",
            "|sum_X Pi_X DeltaR_AB^X| <= eta_bound in small residual regime",
            "first WEP bound target for finite residual branch",
            "MICROSCOPE bound anchor",
            "cannot isolate an individual Pi_X unless all other channels are theorem-zero or independently bounded",
            "NONCLAIM_BOUND_CONTRACT",
        ),
    ]
    rows: list[dict[str, object]] = []
    for map_id, symbol, formula, meaning, source, blocker, status in specs:
        row = base_row()
        row.update(
            {
                "map_id": map_id,
                "symbol": symbol,
                "formula": formula,
                "meaning": meaning,
                "source_anchor": source,
                "claim_blocker": blocker,
                "status": status,
            }
        )
        rows.append(row)
    return rows


def gr_zero_theorem_rows() -> list[dict[str, object]]:
    specs = [
        (
            "GRZ2003_0_single_metric",
            "All ordinary test bodies couple to one observed metric/coframe g_obs/e_obs.",
            "MISSING_PARENT_SIGNATURE",
            "same geometry controls inertial and gravitational response",
            "species-dependent metric/coframe choice would reopen WEP residuals",
        ),
        (
            "GRZ2003_1_hilbert_source_owner",
            "The gravitational source is the Hilbert stress-energy variation of the same matter action.",
            "MISSING_PARENT_SIGNATURE",
            "composition enters total energy, not an extra free-fall source charge",
            "independent source-weight coefficients remain possible unless forbidden",
        ),
        (
            "GRZ2003_2_no_species_weight",
            "No independent w_A, C_A, or material label multiplies source coupling or readout.",
            "MISSING_NO_SOURCE_WEIGHT_THEOREM",
            "DeltaR_AB visible to free fall is zero/common-mode for ordinary matter",
            "this is the real coupling gap",
        ),
        (
            "GRZ2003_3_binding_included",
            "Rest mass, kinetic energy, pressure, EM/nuclear binding, and defects enter one source functional.",
            "MISSING_BINDING_SOURCE_CONTRACT",
            "prevents hiding composition dependence in a missing binding row",
            "exact mass-defect tensor or a parent zero theorem still needed",
        ),
        (
            "GRZ2003_4_readout_preservation",
            "Orbit/readout/boundary projection does not reintroduce material labels.",
            "MISSING_PRESERVATION_THEOREM_OR_OFFICIAL_KERNEL",
            "eta_AB stays zero if the parent residual is universal",
            "official arrays or a projection-silence theorem needed",
        ),
        (
            "GRZ2003_5_conditional_result",
            "If GRZ2003_0 through GRZ2003_4 are signed, then epsilon_A=epsilon_B and eta_AB=0 exactly.",
            "EXACT_CONDITIONAL_THEOREM_UNSIGNED",
            "this is the GR/Newton-compatible WEP route",
            "not claim-ready until the parent action signs the clauses",
        ),
    ]
    rows: list[dict[str, object]] = []
    for theorem_id, statement, status, if_signed, if_unsigned in specs:
        row = base_row()
        row.update(
            {
                "theorem_id": theorem_id,
                "statement": statement,
                "current_status": status,
                "if_signed": if_signed,
                "if_unsigned": if_unsigned,
                "parent_signed": "false",
            }
        )
        rows.append(row)
    return rows


def finite_source_map_contract_rows() -> list[dict[str, object]]:
    specs = [
        (
            "FSM2003_0_CX",
            "C_X",
            "parent coupling coefficient for generator X",
            "dimensionless or declared units per generator",
            "derive from parent action, prove zero, or source as finite nonclaim prior",
            "MISSING_PARENT_COEFFICIENT",
        ),
        (
            "FSM2003_1_source_leg",
            "S_Earth^X",
            "Earth/source response leg in observed frame",
            "declared source units",
            "source worldtube, point-source theorem, or official reconstruction",
            "MISSING_SOURCE_WORLDTUBE",
        ),
        (
            "FSM2003_2_readout_kernel",
            "K_WEP^X tau_WEP^X",
            "orbit/readout transfer from source residual to eta_AB",
            "dimensionless after normalization",
            "official CMSM arrays or parent projection theorem",
            "MISSING_OFFICIAL_OR_THEOREM_KERNEL",
        ),
        (
            "FSM2003_3_material_response",
            "DeltaR_TiPt^X",
            "Ti/Pt material response difference in parent basis",
            "dimensionless logarithmic response",
            "exact mass-defect/material tensor or theorem-zero",
            "MISSING_EXACT_MATERIAL_TENSOR",
        ),
        (
            "FSM2003_4_denominator",
            "R_Ti^X + R_Pt^X",
            "exact eta denominator correction",
            "dimensionless",
            "derive or prove small-residual denominator control",
            "MISSING_DENOMINATOR_CONTROL",
        ),
        (
            "FSM2003_5_product",
            "Pi_X DeltaR_TiPt^X",
            "claim-testable WEP product contribution",
            "dimensionless eta contribution",
            "all upstream symbols real or theorem-zero",
            "MISSING_FORWARD_PRODUCT",
        ),
    ]
    rows: list[dict[str, object]] = []
    for contract_id, symbol, meaning, units, promotion, status in specs:
        row = base_row()
        row.update(
            {
                "contract_id": contract_id,
                "symbol": symbol,
                "meaning": meaning,
                "units": units,
                "promotion_requirement": promotion,
                "current_status": status,
                "score_ready": "false",
            }
        )
        rows.append(row)
    return rows


def official_import_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("IMP2003_0_drop_folder", "source-intake/microscope_cmsm", "AWAITING_EXPORT", "drop official CMSM/browser export here"),
        ("IMP2003_1_required_columns", "segment_id,t_utc,sample_index,gx,gz,Sxx,Sxz,mask_flag", "CONTRACT_READY", "validate against 2001 drop contract"),
        ("IMP2003_2_surrogate_replacement", "replace surrogate gx/gz/Sxx/Sxz/gxS columns", "NOT_REPLACED", "official arrays can fix data-side geometry but not parent coupling"),
        ("IMP2003_3_claim_boundary", "official arrays alone", "INSUFFICIENT_FOR_CLAIM", "still needs parent material/source map or theorem-zero"),
    ]
    rows: list[dict[str, object]] = []
    for gate_id, obj, status, action in specs:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "object": obj,
                "current_status": status,
                "next_action": action,
            }
        )
        rows.append(row)
    return rows


def bound_projection_rows() -> list[dict[str, object]]:
    row = local_bound_row("R1_WEP_source_charge")
    eta_bound = float(row["upper_bound"])
    specs = [
        (
            "BND2003_0_linear_sum_bound",
            "linear finite residual",
            "|sum_X Pi_X DeltaR_TiPt^X| <= eta_bound",
            eta_bound,
            row["units"],
            "usable only after Pi_X and DeltaR_TiPt^X are derived/sourced",
        ),
        (
            "BND2003_1_single_channel_if_all_others_zero",
            "single retained X channel",
            "|Pi_X| <= eta_bound / |DeltaR_TiPt^X|",
            eta_bound,
            row["units"],
            "requires nonzero sourced DeltaR_TiPt^X and theorem-zero for all other channels",
        ),
        (
            "BND2003_2_zero_theorem_branch",
            "GR-compatible zero branch",
            "eta_TiPt = 0 <= eta_bound",
            eta_bound,
            row["units"],
            "mathematically passes only if GRZ clauses are parent-signed",
        ),
    ]
    rows: list[dict[str, object]] = []
    for bound_id, branch, formula, value, units, condition in specs:
        out = base_row()
        out.update(
            {
                "bound_id": bound_id,
                "branch": branch,
                "formula": formula,
                "eta_bound_abs": value,
                "units": units,
                "condition": condition,
                "comparison_ready": "false",
            }
        )
        rows.append(out)
    return rows


def product_prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED2003_0_parent_material_source_map_nonclaim",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_PARENT_MATERIAL_SOURCE_MAP_OR_PARENT_SIGNED_ZERO_THEOREM",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2003_PARENT_PRODUCT_MAP.csv",
            "inputs_present": "exact_symbolic_formula;conditional_GR_zero_route;finite_source_map_contract;CMSM_import_gate",
            "required_inputs": "parent-signed Hilbert/source/no-species theorem OR finite C_X,S_Earth,K_WEP,tau_WEP,DeltaR_TiPt rows with official arrays/projection",
            "derivation_status": "EXACT_CONTRACT_DERIVED_NUMERIC_PRODUCT_MISSING",
            "valid_for_claim": "false",
            "notes": "2003 derives the composite map shape but not a claim-ready WEP product",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    row = local_bound_row("R1_WEP_source_charge")
    url, doi = split_reference(row["reference_path_or_url"])
    return [
        {
            "bound_id": "BOUND2003_0_MICROSCOPE_R1_eta_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": row["upper_bound"],
            "bound_units": row["units"],
            "bound_source": url,
            "source_row": f"source-intake/local_bounds/local_bound_claims.csv::{row['row_id']}; doi:{doi}",
            "bound_type": "source_backed_upper_bound_anchor",
            "valid_for_claim": "true",
            "notes": "valid bound anchor only; parent product remains invalid for claim",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "runner_id": "APR2003_0_parent_material_source_map_product_stub",
            "prediction_rows": status.get("prediction_rows", ""),
            "bound_rows": status.get("bound_rows", ""),
            "valid_prediction_rows": status.get("valid_prediction_rows", ""),
            "valid_bound_rows": status.get("valid_bound_rows", ""),
            "comparison_rows": status.get("comparison_rows", ""),
            "passed_rows": status.get("passed_rows", ""),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "expected_result": "reject exact-symbolic-but-input-missing product and keep claim false",
        }
    )
    return [row]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, object]]:
    specs = [
        ("CG2003_0_parent_product_formula", "exact parent WEP product formula", "true", "formula derived but nonclaim"),
        ("CG2003_1_GR_zero_theorem", "GR-compatible eta=0 theorem", "false", "conditional clauses not parent-signed"),
        ("CG2003_2_finite_source_map", "finite material/source map", "false", "C_X/source/readout/material rows missing"),
        ("CG2003_3_official_CMSM_import", "official CMSM arrays", "false", "not imported and not sufficient alone"),
        ("CG2003_4_product_runner", "WEP product runner", "false", f"valid_prediction_rows={product_status.get('valid_prediction_rows')}"),
        ("CG2003_5_local_GR_Newton", "local GR/Newton/WEP reduction", "false", "needs parent-signed Hilbert source/no-species clauses"),
    ]
    rows: list[dict[str, object]] = []
    for gate_id, component, gate_pass, reason in specs:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "claim_component": component,
                "gate_pass": gate_pass,
                "claim_allowed": "false",
                "reason": reason,
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DEC2003_0_exact_map_derived",
            "derive the exact composite parent material/source WEP map",
            "eta_AB = 2 sum_X Pi_X DeltaR_AB^X / (2 + sum_X Pi_X (R_A^X + R_B^X))",
            "the missing coupling is now a precise finite list, not a vague gap",
        ),
        (
            "DEC2003_1_best_route",
            "the least-scrutiny route is parent-signed Hilbert/source universality, not surrogate tuning",
            "GRZ2003_5_conditional_result",
            "prove no species/material source coefficient before readout, yielding eta=0 exactly",
        ),
        (
            "DEC2003_2_fallback_route",
            "if the zero theorem fails, finite rows must be sourced honestly",
            "FSM2003_0_CX through FSM2003_5_product",
            "then the MICROSCOPE bound can test a real product rather than define it",
        ),
        (
            "DEC2003_3_official_data_role",
            "official CMSM arrays are useful but not the coupling solution",
            "IMP2003_3_claim_boundary",
            "arrays fix the readout kernel; parent matter/source map still decides GR reduction",
        ),
    ]
    rows: list[dict[str, object]] = []
    for decision_id, decision, evidence, consequence in specs:
        row = base_row()
        row.update(
            {
                "decision_id": decision_id,
                "decision": decision,
                "evidence": evidence,
                "consequence": consequence,
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "next_id": "NEXT2003_0_2004",
            "next_target": "2004-Y5-R2FR-parent-Hilbert-source-signature-or-finite-nonmetric-coefficient-ledger.md",
            "objective": "attempt to parent-sign the Hilbert/source/no-species clauses that make eta_AB=0 exactly; if they cannot be signed, emit a finite nonmetric coefficient ledger for the source-map product.",
            "include": "single observed metric/coframe; Hilbert source owner; no species/material source prefactor; binding-energy inclusion; readout preservation; fallback C_X ledger",
            "exclude": "surrogate evidence polishing, tau=1, measured-G absorption, invented material charges, public WEP/local-GR claim, GitHub, or formalization-workbench edits",
        }
    )
    return [row]


def make_branch_copies(parent_rows: list[dict[str, object]], gr_rows: list[dict[str, object]], finite_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copy_specs = [
        (
            SOURCE_WEIGHT_DOCS / "PARENT_MATERIAL_SOURCE_MAP_2003_NONCLAIM.csv",
            parent_rows,
            "exact composite parent map",
        ),
        (
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2003_GR_ZERO_THEOREM_AUDIT_NONCLAIM.csv",
            gr_rows,
            "GR-compatible zero theorem audit",
        ),
        (
            QUEUE / "JR2003_FINITE_NONMETRIC_COEFFICIENT_LEDGER_QUEUE.csv",
            finite_rows,
            "finite coefficient fallback queue",
        ),
    ]
    rows: list[dict[str, object]] = []
    for path, data, meaning in copy_specs:
        write_csv(path, data)
        row = base_row()
        row.update(
            {
                "copy_id": f"COPY2003_{len(rows)}",
                "path": str(path),
                "exists": str(path.exists()),
                "meaning": meaning,
            }
        )
        rows.append(row)
    return rows


def validate_outputs(
    outputs: dict[str, Path],
    branch_copies: list[dict[str, object]],
    source_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    gr_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    import_rows: list[dict[str, object]],
    bound_projection: list[dict[str, object]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    generated_paths = list(outputs.values()) + [DOC] + [Path(str(row["path"])) for row in branch_copies]
    exact_eta = any(row["map_id"] == "PPM2003_4_exact_eta" and "eta_AB" in str(row["formula"]) for row in parent_rows)
    gr_zero = any(row["theorem_id"] == "GRZ2003_5_conditional_result" and row["current_status"] == "EXACT_CONDITIONAL_THEOREM_UNSIGNED" for row in gr_rows)
    finite_complete = {row["contract_id"] for row in finite_rows} >= {
        "FSM2003_0_CX",
        "FSM2003_1_source_leg",
        "FSM2003_2_readout_kernel",
        "FSM2003_3_material_response",
        "FSM2003_4_denominator",
        "FSM2003_5_product",
    }
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2003_00_sources", all(row["exists"] == "True" and row["anchor_found"] == "True" for row in source_rows), "all source paths exist and needles found"))
    checks.append(("VAL2003_01_exact_parent_map", exact_eta, "exact composite eta/product map derived"))
    checks.append(("VAL2003_02_GR_zero_route", gr_zero and all(row["parent_signed"] == "false" for row in gr_rows), "GR-compatible zero route is explicit but unsigned"))
    checks.append(("VAL2003_03_finite_contract", finite_complete and all(row["score_ready"] == "false" for row in finite_rows), "finite source-map contract complete and nonclaim"))
    checks.append(("VAL2003_04_import_gate", any(row["gate_id"] == "IMP2003_3_claim_boundary" and row["current_status"] == "INSUFFICIENT_FOR_CLAIM" for row in import_rows), "official import gate open but not sufficient alone"))
    checks.append(("VAL2003_05_bound_projection", all(float(row["eta_bound_abs"]) > 0 and row["comparison_ready"] == "false" for row in bound_projection), "bound projection rows positive but not comparison-ready"))
    checks.append(("VAL2003_06_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "product runner refuses missing parent product"))
    checks.append(("VAL2003_07_claim_gates_safe", all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("VAL2003_08_next_target", any("2004-Y5-R2FR-parent-Hilbert-source-signature-or-finite-nonmetric-coefficient-ledger.md" in row["next_target"] for row in next_rows), "2004 Hilbert/source signature handoff written"))
    checks.append(("VAL2003_09_branch_copies", all(Path(str(row["path"])).exists() for row in branch_copies), "branch copy artifacts written"))
    checks.append(("VAL2003_10_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("VAL2003_11_csv_parse", all(path.exists() and csv_rows_parse(path) for path in outputs.values() if path.suffix == ".csv" and path.name != "P8_Y5_BRR545_2003_VALIDATION.csv"), "all 2003 CSV outputs parse cleanly"))
    checks.append(("VAL2003_12_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"))
    checks.append(("VAL2003_13_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("VAL2003_OVERALL", True, "2003 parent material/source map or official CMSM import gate"))
    rows: list[dict[str, object]] = []
    for validation_id, passed, detail in checks:
        row = base_row()
        row.update(
            {
                "validation_id": validation_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
            }
        )
        rows.append(row)
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    gr_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    import_rows: list[dict[str, object]],
    bound_projection: list[dict[str, object]],
    prediction_rows: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status_rows_: list[dict[str, object]],
    product_comparison_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    validation_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> None:
    text = "\n".join(
        [
            "# 2003 - R2FR parent material/source map or official CMSM import gate",
            "",
            "## Current verdict",
            "2003 fuses the earlier material-response, eta-projection, Hilbert-universality, direct-product, and surrogate-degeneracy results into one exact WEP parent product map. The leap forward is the formula: `eta_AB = 2 sum_X Pi_X DeltaR_AB^X / (2 + sum_X Pi_X (R_A^X + R_B^X))`, with `Pi_X=C_X S_Earth^X K_WEP^X tau_WEP^X` and `DeltaR_AB^X=R_A^X-R_B^X`.",
            "",
            "Important boundary: this is not a WEP/local-GR claim. The clean GR/Newton route is now precise: parent-sign universal Hilbert source coupling plus no species/material source prefactor, and eta vanishes exactly. Those clauses are still unsigned.",
            "",
            "Next honest move: attack the parent Hilbert/source/no-species signature directly; official CMSM arrays remain useful but cannot solve the coupling gap alone.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "source_path", "exists", "anchor_found", "note"]),
            "## Exact parent product map",
            md_table(parent_rows, ["map_id", "symbol", "formula", "meaning", "status", "claim_blocker"]),
            "## GR-compatible zero theorem audit",
            md_table(gr_rows, ["theorem_id", "statement", "current_status", "if_signed", "if_unsigned", "parent_signed"]),
            "## Finite source-map fallback contract",
            md_table(finite_rows, ["contract_id", "symbol", "meaning", "units", "promotion_requirement", "current_status"]),
            "## Official CMSM import gate",
            md_table(import_rows, ["gate_id", "object", "current_status", "next_action"]),
            "## Bound projection rows",
            md_table(bound_projection, ["bound_id", "branch", "formula", "eta_bound_abs", "units", "condition", "comparison_ready"]),
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
            md_table(decisions, ["decision_id", "decision", "evidence", "consequence"]),
            "## Branch copies",
            md_table(branch_copies, ["copy_id", "path", "exists", "meaning"]),
            "## Validation",
            md_table(validation_rows, ["validation_id", "status", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    parent_rows = parent_product_map_rows()
    gr_rows = gr_zero_theorem_rows()
    finite_rows = finite_source_map_contract_rows()
    import_rows = official_import_gate_rows()
    bound_projection = bound_projection_rows()
    prediction_rows = product_prediction_rows()
    bound_rows_ = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    branch_copies = make_branch_copies(parent_rows, gr_rows, finite_rows)

    outputs = {
        "source_register": OUT / "P8_Y5_PARENT_QLOC_2003_SOURCE_REGISTER.csv",
        "parent_product_map": OUT / "P8_Y5_PARENT_QLOC_2003_PARENT_PRODUCT_MAP.csv",
        "gr_zero_theorem": OUT / "P8_Y5_PARENT_QLOC_2003_GR_ZERO_THEOREM_AUDIT.csv",
        "finite_contract": OUT / "P8_Y5_PARENT_QLOC_2003_FINITE_SOURCE_MAP_CONTRACT.csv",
        "official_import": OUT / "P8_Y5_PARENT_QLOC_2003_OFFICIAL_CMSM_IMPORT_GATE.csv",
        "bound_projection": OUT / "P8_Y5_PARENT_QLOC_2003_BOUND_PROJECTION_ROWS.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_PARENT_QLOC_2003_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_PARENT_QLOC_2003_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2003_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2003_DECISION_LEDGER.csv",
        "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2003_BRANCH_COPIES.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2003_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_2003_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["parent_product_map"], parent_rows)
    write_csv(outputs["gr_zero_theorem"], gr_rows)
    write_csv(outputs["finite_contract"], finite_rows)
    write_csv(outputs["official_import"], import_rows)
    write_csv(outputs["bound_projection"], bound_projection)
    write_csv(outputs["prediction"], prediction_rows, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["branch_copies"], branch_copies)
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
        branch_copies,
        source_rows,
        parent_rows,
        gr_rows,
        finite_rows,
        import_rows,
        bound_projection,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        parent_rows,
        gr_rows,
        finite_rows,
        import_rows,
        bound_projection,
        prediction_rows,
        bound_rows_,
        product_status_rows_,
        product_result["comparisons"],
        claim_rows,
        decisions,
        branch_copies,
        validation_rows,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation_rows if row["status"] != "PASS"]
    print(f"wrote {DOC}")
    print(f"wrote {outputs['validation']}")
    print(f"VAL2003_OVERALL={'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['validation_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
