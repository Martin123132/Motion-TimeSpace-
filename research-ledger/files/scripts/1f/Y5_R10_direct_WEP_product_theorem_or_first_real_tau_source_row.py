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
DOC = ROOT / "1069-Y5-R10-direct-WEP-product-theorem-or-first-real-tau-source-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1069-direct-WEP-product-or-first-tau-source" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1069_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1069_WEP_BOUND_IMPORT.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    candidate = Path(path_text)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


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
        ("SRC1069_0_1068_next", "source-intake/mts_residuals/P8_Y5_R10_1068_NEXT_TARGET.csv", "1069-Y5-R10-direct-WEP-product-theorem", "1068 handoff."),
        ("SRC1069_1_1068_fallback", "source-intake/mts_residuals/P8_Y5_R10_1068_DIRECT_PRODUCT_FALLBACK.csv", "DPF1068_0_preferred_route", "direct product fallback."),
        ("SRC1069_2_1068_pack", "source-intake/mts_residuals/P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv", "TAP1068_2_eta_readout", "tau acquisition pack."),
        ("SRC1069_3_1068_orbit", "source-intake/mts_residuals/P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv", "ORB1068_2_eta_convention", "MICROSCOPE readout requirement."),
        ("SRC1069_4_1068_force", "source-intake/mts_residuals/P8_Y5_R10_1068_OBSERVED_FRAME_FORCE_MAP.csv", "FRM1068_1_eta_mapping", "eta force/readout map."),
        ("SRC1069_5_1068_worldtube", "source-intake/mts_residuals/P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv", "SWT1068_5_verdict", "source worldtube still missing."),
        ("SRC1069_6_1068_material", "source-intake/mts_residuals/P8_Y5_R10_1068_MATERIAL_RESPONSE_REQUIREMENTS.csv", "MAT1068_5_verdict", "material response still missing."),
        ("SRC1069_7_1067_tau", "source-intake/mts_residuals/P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv", "TAQ1067_3_direct_product_option", "direct product option."),
        ("SRC1069_8_1062_parent", "source-intake/mts_residuals/P8_Y5_R10_1062_PARENT_PRODUCT_THEOREM_ATTEMPT.csv", "THM1062_6_verdict", "prior parent product theorem attempt."),
        ("SRC1069_9_1063_source", "source-intake/mts_residuals/P8_Y5_R10_1063_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv", "THM1063_5_verdict", "source label forgetting gap."),
        ("SRC1069_10_1066_scalar", "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv", "SSE1066_5_verdict", "source-scalar exclusion gap."),
        ("SRC1069_11_1067_action", "source-intake/mts_residuals/P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv", "ASO1067_5_verdict", "action-scale owner gap."),
        ("SRC1069_12_1061_material", "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_0_test_pair", "MICROSCOPE material convention."),
        ("SRC1069_13_708_wep", "source-intake/mts_residuals/P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv", "PGW708_0_R1_WEP", "WEP source/test charge vector missing."),
        ("SRC1069_14_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP provenance."),
        ("SRC1069_15_393_common", "393-source-normalized-Newtonian-limit-under-identity-closure.md", "Only a constant, universal, range-independent", "measured-G common-mode guard."),
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


def direct_product_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "DWT1069_0_target",
            "claim": "derive P_WEP_relative_source_weight directly from parent variation",
            "formal_move": "delta S_parent -> source residual -> eta_AB without splitting into Delta_w_TiPt and tau_WEP",
            "attempt_result": "TARGET_SHARPENED",
            "gap": "needs source variation, force/readout map, and observed-frame eta convention",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "DWT1069_1_variation_route",
            "claim": "parent variation gives the differential acceleration observable",
            "formal_move": "P_WEP := readout_eta[delta_e S_matter, source worldtube, orbit average, material response]",
            "attempt_result": "FORMALLY_CLEAN_IF_ALL_MAPS_EXIST",
            "gap": "1068 shows those maps are acquisition rows, not derived objects",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "DWT1069_2_theorem_zero_route",
            "claim": "direct product is theorem-zero",
            "formal_move": "P_WEP=0 if source-scalar exclusion/action-scale owner or WEP projection silence is parent-signed",
            "attempt_result": "CONDITIONAL_ONLY",
            "gap": "SSE1066 and ASO1067 verdicts are still unsigned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "DWT1069_3_finite_route",
            "claim": "direct product is a numeric finite prediction",
            "formal_move": "P_WEP = abs(parent predicted eta_AB residual) in dimensionless MICROSCOPE convention",
            "attempt_result": "MISSING_NUMERIC_PARENT_PRODUCT",
            "gap": "no source worldtube/orbit/readout/material/Xhat pack yet",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "DWT1069_4_no_shortcuts",
            "claim": "refuse false direct products",
            "formal_move": "reject tau=1, Delta_w=0 by taste, measured-G absorption of relative weights, and cancellation",
            "attempt_result": "REFUSAL_RULE_ACTIVE",
            "gap": "none; this is a guard, not a derivation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "DWT1069_5_verdict",
            "claim": "direct WEP product theorem",
            "formal_move": "parent variation to eta_AB product",
            "attempt_result": "DIRECT_PRODUCT_THEOREM_NOT_DERIVED",
            "gap": "direct product remains preferred route, but first real source/readout row is needed for finite branch",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def first_real_tau_source_rows() -> list[dict[str, str]]:
    source_row = local_bound_row("R1_WEP_source_charge")
    url, doi = split_reference(source_row["reference_path_or_url"])
    direct_row = local_bound_row("R0_identity_coframe_direct")
    direct_url, direct_doi = split_reference(direct_row["reference_path_or_url"])
    return [
        {
            "tau_source_id": "WTS1069_0_MICROSCOPE_eta_source_charge_proxy",
            "pack_component": "eta/readout bound anchor",
            "fills_1068_row": "TAP1068_2_eta_readout; ORB1068_2_eta_convention",
            "dataset_id": source_row["dataset_id"],
            "row_id": source_row["row_id"],
            "observable": source_row["observable"],
            "measured_value": source_row["measured_value"],
            "one_sigma": source_row["one_sigma"],
            "upper_bound": source_row["upper_bound"],
            "units": source_row["units"],
            "reference_url": url,
            "doi": doi,
            "source_backed": "true",
            "claim_ready": "false",
            "why_not_claim": "bound/readout anchor only; does not supply tau_WEP, source worldtube, orbit kernel, material tensor, or parent product",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tau_source_id": "WTS1069_1_MICROSCOPE_direct_geometry_context",
            "pack_component": "direct eta context",
            "fills_1068_row": "FRM1068_1_eta_mapping",
            "dataset_id": direct_row["dataset_id"],
            "row_id": direct_row["row_id"],
            "observable": direct_row["observable"],
            "measured_value": direct_row["measured_value"],
            "one_sigma": direct_row["one_sigma"],
            "upper_bound": direct_row["upper_bound"],
            "units": direct_row["units"],
            "reference_url": direct_url,
            "doi": direct_doi,
            "source_backed": "true",
            "claim_ready": "false",
            "why_not_claim": "context for eta readout only; not an MTS residual prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "tau_source_id": "WTS1069_2_MICROSCOPE_material_smoke_context",
            "pack_component": "material pair context",
            "fills_1068_row": "TAP1068_3_material_response; MAT1068_0_pair_convention",
            "dataset_id": "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION",
            "row_id": "MCON1061_0_test_pair",
            "observable": "TA6V_minus_PtRh10 convention",
            "measured_value": "not_applicable",
            "one_sigma": "not_applicable",
            "upper_bound": "not_applicable",
            "units": "dimensionless convention",
            "reference_url": "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv",
            "doi": "not_applicable",
            "source_backed": "internal_smoke_context",
            "claim_ready": "false",
            "why_not_claim": "material pair convention only; not full material/source response tensor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def provenance_rows() -> list[dict[str, str]]:
    rows = []
    for provenance_id, row_id, use in [
        ("PROV1069_0_R1_source_charge", "R1_WEP_source_charge", "primary nonclaim source-charge/readout bound anchor"),
        ("PROV1069_1_R0_direct_geometry", "R0_identity_coframe_direct", "direct eta context, not source-weight prediction"),
    ]:
        bound_row = local_bound_row(row_id)
        url, doi = split_reference(bound_row["reference_path_or_url"])
        rows.append(
            {
                "provenance_id": provenance_id,
                "dataset_id": bound_row["dataset_id"],
                "row_id": bound_row["row_id"],
                "observable": bound_row["observable"],
                "reference_url": url,
                "doi": doi,
                "reference_note": bound_row["reference_note"],
                "use_in_1069": use,
                "source_backed": "true",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def readout_fill_matrix_rows() -> list[dict[str, str]]:
    return [
        {
            "matrix_id": "RFM1069_0_eta_bound",
            "component": "eta_AB upper bound/readout anchor",
            "filled_by": "WTS1069_0_MICROSCOPE_eta_source_charge_proxy",
            "fill_status": "SOURCE_BACKED_ANCHOR_FILLED",
            "still_missing": "parent product; tau_WEP; orbit kernel; source worldtube; material tensor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "matrix_id": "RFM1069_1_eta_formula",
            "component": "eta_AB formula/sign/readout convention",
            "filled_by": "local bound row only",
            "fill_status": "PARTIAL_CONTEXT_ONLY",
            "still_missing": "official formula/readout extraction row and parent force-map derivation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "matrix_id": "RFM1069_2_orbit_kernel",
            "component": "MICROSCOPE orbit/averaging kernel",
            "filled_by": "none",
            "fill_status": "MISSING",
            "still_missing": "orbit/altitude/time/attitude averaging source",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "matrix_id": "RFM1069_3_source_worldtube",
            "component": "Earth/source worldtube",
            "filled_by": "none",
            "fill_status": "MISSING",
            "still_missing": "source profile, composition/source-charge convention, finite-source correction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "matrix_id": "RFM1069_4_material_tensor",
            "component": "Ti/Pt material response tensor",
            "filled_by": "WTS1069_2 material pair smoke context",
            "fill_status": "PAIR_CONTEXT_ONLY",
            "still_missing": "full material/source response tensor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "matrix_id": "RFM1069_5_direct_product",
            "component": "direct parent P_WEP product",
            "filled_by": "none",
            "fill_status": "MISSING",
            "still_missing": "parent variation to dimensionless eta_AB residual",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def remaining_requirements_rows() -> list[dict[str, str]]:
    return [
        {
            "requirement_id": "REQ1069_0_direct_product",
            "requirement": "derive numeric/theorem-zero P_WEP_relative_source_weight directly",
            "current_status": "MISSING_DIRECT_PARENT_PRODUCT",
            "next_action": "try parent variation force/readout kernel",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "REQ1069_1_readout_formula",
            "requirement": "official MICROSCOPE eta_AB formula/sign/readout convention",
            "current_status": "PARTIAL_BOUND_PROVENANCE_ONLY",
            "next_action": "extract formula/source row from MICROSCOPE paper or local corpus",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "REQ1069_2_orbit_kernel",
            "requirement": "MICROSCOPE orbit/attitude/averaging kernel",
            "current_status": "MISSING_ORBIT_KERNEL",
            "next_action": "source official orbit/readout metadata",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "REQ1069_3_source_worldtube",
            "requirement": "Earth/source worldtube and source charge convention",
            "current_status": "MISSING_SOURCE_WORLDTUBE",
            "next_action": "source Earth profile or theorem-reduce to calibrated point-source convention",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "REQ1069_4_material_tensor",
            "requirement": "Ti/Pt source-weight material response tensor",
            "current_status": "MISSING_MATERIAL_TENSOR",
            "next_action": "source material model or derive theorem reducing to Delta_w_TiPt",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "requirement_id": "REQ1069_5_xhat_norm",
            "requirement": "shared Xhat/chi_X normalization",
            "current_status": "MISSING_XHAT_NORMALIZATION",
            "next_action": "derive shared branch normalization or direct product",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1069_0_WEP_direct_or_tau_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_DIRECT_PRODUCT_OR_TAU_WEP_SPLIT_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1069_DIRECT_WEP_PRODUCT_THEOREM_ATTEMPT.csv",
            "inputs_present": "MICROSCOPE_R1_eta_bound=2.8e-15;reference=https://arxiv.org/abs/2209.15487;doi=10.1103/PhysRevLett.129.121102",
            "required_inputs": "direct parent P_WEP product OR tau_WEP source/orbit/readout pack plus Delta_w_TiPt",
            "derivation_status": "MISSING_DIRECT_PRODUCT_AND_TAU_SPLIT_PRODUCT",
            "valid_for_claim": "false",
            "notes": "1069 acquired the first real readout/bound provenance row only; prediction remains missing.",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    bound_row = local_bound_row("R1_WEP_source_charge")
    return [
        {
            "bound_id": "BOUND1069_0_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": bound_row["upper_bound"],
            "bound_units": bound_row["units"],
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": bound_row["row_id"],
            "bound_type": "numeric_bound_anchor_nonclaim",
            "valid_for_claim": "true",
            "notes": "MICROSCOPE Ti/Pt source-charge proxy bound; bound only, not an MTS prediction.",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1069_0_WEP_direct_or_tau_product",
            "prediction_rows": str(status.get("prediction_rows", "")),
            "bound_rows": str(status.get("bound_rows", "")),
            "valid_prediction_rows": str(status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(status.get("valid_bound_rows", "")),
            "comparison_rows": str(status.get("comparison_rows", "")),
            "passed_rows": str(status.get("passed_rows", "")),
            "blocked_or_failed_rows": str(status.get("blocked_or_failed_rows", "")),
            "claim_allowed": str(status.get("claim_allowed", "")).lower(),
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1069_0_direct_product_theorem",
            "claim": "direct P_WEP product theorem is derived",
            "gate_pass": "false",
            "reason": "parent variation to eta_AB remains missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1069_1_first_real_source_row",
            "claim": "first real MICROSCOPE eta/readout source row is acquired",
            "gate_pass": "true",
            "reason": "R1 source-charge proxy row has numeric bound, units, URL, and DOI provenance",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1069_2_tau_WEP_numeric",
            "claim": "tau_WEP is numeric or theorem-zero",
            "gate_pass": "false",
            "reason": "source row is a bound/readout anchor, not tau_WEP",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1069_3_runner_score",
            "claim": "WEP product can be scored",
            "gate_pass": "false",
            "reason": "strict runner has valid_prediction_rows=0",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1069_4_local_GR_WEP",
            "claim": "local GR/WEP coupling branch is derived",
            "gate_pass": "false",
            "reason": "direct product and tau acquisition branches remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1069_0_direct_product_status",
            "decision": "direct WEP product theorem is not derived",
            "because": "parent variation still lacks eta_AB force/readout and source worldtube maps",
            "next_action": "keep direct theorem as preferred route, but acquire readout/formula data next",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1069_1_first_source_row_status",
            "decision": "first real MICROSCOPE eta/readout source row is acquired as nonclaim provenance",
            "because": "local bound row R1 supplies numeric bound, units, URL, DOI, and reference note",
            "next_action": "extract official eta_AB formula/readout convention or orbit kernel",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1069_2_best_next",
            "decision": "next target is MICROSCOPE eta formula/readout extraction or orbit kernel",
            "because": "the first source row gives a bound anchor but not a projection functional",
            "next_action": "1070-Y5-R10-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1070-Y5-R10-MICROSCOPE-eta-readout-formula-or-orbit-kernel-acquisition.md",
            "objective": "extract the official MICROSCOPE eta_AB formula/readout convention and, if available, the first orbit/averaging kernel row; keep all rows nonclaim until a direct P_WEP product or tau_WEP projection exists.",
            "include": "eta_AB definition, sign/absolute-value convention, test-mass pair convention, orbit/attitude/averaging source row, URL/DOI provenance, unit checks, runner refusal gates",
            "exclude": "setting tau_WEP to one, setting Delta_w to zero by taste, measured-G absorption of relative weights, cancellation arguments, public WEP/local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validate_outputs(
    outputs: dict[str, Path],
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    tau_sources: list[dict[str, str]],
    provenance: list[dict[str, str]],
    matrix: list[dict[str, str]],
    remaining: list[dict[str, str]],
    predictions: list[dict[str, str]],
    bounds: list[dict[str, str]],
    product_status: dict[str, Any],
    claims: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    def add(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "result": "pass" if condition else "fail", "detail": detail, "generated_utc": stamp()})

    add("V1069_1_sources_exist_and_needles", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "every cited source path exists and every source needle was found")
    add("V1069_2_direct_theorem_not_promoted", any(row["theorem_id"] == "DWT1069_5_verdict" and row["attempt_result"] == "DIRECT_PRODUCT_THEOREM_NOT_DERIVED" for row in theorem), "direct product theorem remains unproved")
    acquired = any(row["tau_source_id"] == "WTS1069_0_MICROSCOPE_eta_source_charge_proxy" and row["source_backed"] == "true" and row["upper_bound"] == "2.8e-15" and row["units"] == "dimensionless" for row in tau_sources)
    add("V1069_3_first_real_source_row_acquired", acquired, "first real MICROSCOPE eta/readout source row acquired with numeric bound and units")
    prov_ok = all(row["source_backed"] == "true" and row["reference_url"].startswith("https://") and row["doi"] for row in provenance)
    add("V1069_4_provenance_has_url_doi", prov_ok, "provenance rows contain source URL and DOI")
    add("V1069_5_readout_matrix_partial_only", any(row["matrix_id"] == "RFM1069_0_eta_bound" and row["fill_status"] == "SOURCE_BACKED_ANCHOR_FILLED" for row in matrix) and any(row["matrix_id"] == "RFM1069_2_orbit_kernel" and row["fill_status"] == "MISSING" for row in matrix), "readout matrix records first filled anchor while orbit kernel remains missing")
    add("V1069_6_remaining_requirements_written", len(remaining) >= 6 and all(row["valid_for_claim"] == "false" for row in remaining), "remaining direct/tau requirements are written as nonclaim rows")
    add("V1069_7_prediction_nonclaim", len(predictions) == 1 and "MISSING" in predictions[0]["product_value"] and predictions[0]["valid_for_claim"] == "false", "WEP product prediction remains nonclaim")
    try:
        bound_numeric = len(bounds) == 1 and float(bounds[0]["bound_value"]) > 0
    except (KeyError, ValueError):
        bound_numeric = False
    add("V1069_8_bound_anchor_numeric", bound_numeric and bounds[0]["valid_for_claim"] == "true", "WEP bound anchor is numeric")
    add("V1069_9_runner_refuses_placeholder", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "strict runner refuses missing direct/tau product")
    first_source_gate = any(row["gate_id"] == "CG1069_1_first_real_source_row" and row["gate_pass"] == "true" and row["claim_allowed"] == "false" for row in claims)
    blocked_claims = all(row["claim_allowed"] == "false" for row in claims)
    add("V1069_10_claim_gates_safe", first_source_gate and blocked_claims, "first source-row gate passes only as nonclaim provenance and all claims remain blocked")
    add("V1069_11_next_target_written", bool(next_rows) and next_rows[0]["next_target"].startswith("1070-Y5-R10-MICROSCOPE-eta-readout-formula"), "next target selects eta formula/readout or orbit kernel acquisition")
    generated_inside = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs.values())
    add("V1069_12_generated_files_in_post_checkpoint", generated_inside, "all generated files are under post-checkpoint-work")
    formalization_count = count_formalization_modified_since_start()
    add("V1069_13_formalization_untouched", formalization_count == 0, f"formalization-workbench modified-file count since script start is {formalization_count}")
    summary_pass = all(row["result"] == "pass" for row in checks)
    checks.insert(0, {"check_id": "V1069_SUMMARY", "result": "pass" if summary_pass else "fail", "detail": "1069 direct WEP product theorem / first real tau source-row validation summary", "generated_utc": stamp()})
    return checks


def write_doc(
    sources: list[dict[str, str]],
    theorem: list[dict[str, str]],
    tau_sources: list[dict[str, str]],
    provenance: list[dict[str, str]],
    matrix: list[dict[str, str]],
    remaining: list[dict[str, str]],
    predictions: list[dict[str, str]],
    bounds: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1069 — Direct WEP Product Theorem Or First Real tau Source Row",
            "",
            "**Current verdict:** direct `P_WEP_relative_source_weight` is still the cleanest theory route, but the theorem does not close because parent variation to `eta_AB` is missing.",
            "",
            "**Progress:** the first real MICROSCOPE eta/readout provenance row is now acquired from `local_bound_claims.csv`: numeric bound, units, URL, and DOI are recorded. This is not `tau_WEP` and not a prediction.",
            "",
            "**Runner result:** strict product scoring remains blocked with `valid_prediction_rows=0`.",
            "",
            "## Direct WEP Product Theorem Attempt",
            md_table(theorem, ["theorem_id", "claim", "formal_move", "attempt_result", "gap", "valid_for_claim"]),
            "",
            "## First Real tau / Readout Source Rows",
            md_table(tau_sources, ["tau_source_id", "pack_component", "fills_1068_row", "dataset_id", "row_id", "observable", "upper_bound", "units", "reference_url", "doi", "source_backed", "claim_ready", "valid_for_claim"]),
            "",
            "## Provenance",
            md_table(provenance, ["provenance_id", "dataset_id", "row_id", "observable", "reference_url", "doi", "use_in_1069", "source_backed", "valid_for_claim"]),
            "",
            "## Readout Fill Matrix",
            md_table(matrix, ["matrix_id", "component", "filled_by", "fill_status", "still_missing", "valid_for_claim"]),
            "",
            "## Remaining Requirements",
            md_table(remaining, ["requirement_id", "requirement", "current_status", "next_action", "valid_for_claim"]),
            "",
            "## WEP Product Candidate",
            md_table(predictions, PRODUCT_REQUIRED_COLUMNS),
            "",
            "## WEP Bound Import",
            md_table(bounds, BOUND_REQUIRED_COLUMNS),
            "",
            "## Runner Status",
            md_table(product_status_rows_, ["runner_id", "prediction_rows", "bound_rows", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "passed_rows", "blocked_or_failed_rows", "claim_allowed", "generated_utc"]),
            "",
            "## Runner Comparisons",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "",
            "## Claim Gates",
            md_table(claims, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Source Register",
            md_table(sources, ["source_id", "relative_path", "exists", "needle", "needle_found", "valid_for_claim"]),
            "",
            "## Validation",
            md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
            "",
            "## Next Target",
            md_table(next_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    theorem = direct_product_theorem_rows()
    tau_sources = first_real_tau_source_rows()
    provenance = provenance_rows()
    matrix = readout_fill_matrix_rows()
    remaining = remaining_requirements_rows()
    predictions = prediction_rows()
    bounds = bound_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs: dict[str, Path] = {
        "source_register": OUT / "P8_Y5_R10_1069_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R10_1069_DIRECT_WEP_PRODUCT_THEOREM_ATTEMPT.csv",
        "tau_sources": OUT / "P8_Y5_R10_1069_FIRST_REAL_TAU_SOURCE_ROW.csv",
        "provenance": OUT / "P8_Y5_R10_1069_MICROSCOPE_PROVENANCE_LEDGER.csv",
        "matrix": OUT / "P8_Y5_R10_1069_READOUT_FILL_MATRIX.csv",
        "remaining": OUT / "P8_Y5_R10_1069_REMAINING_TAU_REQUIREMENTS.csv",
        "predictions": PREDICTION_TEMPLATE,
        "bounds": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1069_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1069_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1069_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1069_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1069_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1069_VALIDATION.csv",
        "doc": DOC,
    }

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["tau_sources"], tau_sources)
    write_csv(outputs["provenance"], provenance)
    write_csv(outputs["matrix"], matrix)
    write_csv(outputs["remaining"], remaining)
    write_csv(outputs["predictions"], predictions, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bounds"], bounds, BOUND_REQUIRED_COLUMNS)
    write_csv(outputs["claim_gates"], claims)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_result["comparisons"])

    validation = validate_outputs(
        outputs,
        sources,
        theorem,
        tau_sources,
        provenance,
        matrix,
        remaining,
        predictions,
        bounds,
        product_status,
        claims,
        next_rows,
    )
    write_csv(outputs["validation"], validation)
    write_doc(
        sources,
        theorem,
        tau_sources,
        provenance,
        matrix,
        remaining,
        predictions,
        bounds,
        product_status_rows_,
        product_result["comparisons"],
        claims,
        decisions,
        validation,
        next_rows,
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
