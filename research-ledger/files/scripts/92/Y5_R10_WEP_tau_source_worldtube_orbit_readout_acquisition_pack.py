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
DOC = ROOT / "1068-Y5-R10-WEP-tau-source-worldtube-orbit-readout-acquisition-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1068-WEP-tau-source-worldtube-orbit-readout" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1068_WEP_TAU_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1068_WEP_TAU_BOUND_IMPORT.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


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


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1068_0_1067_next", "source-intake/mts_residuals/P8_Y5_R10_1067_NEXT_TARGET.csv", "1068-Y5-R10-WEP-tau-source-worldtube-orbit-readout", "1067 handoff."),
        ("SRC1068_1_1067_tau_functional", "source-intake/mts_residuals/P8_Y5_R10_1067_TAU_WEP_FUNCTIONAL_DECOMPOSITION.csv", "TWF1067_6_verdict", "tau_WEP functional decomposition."),
        ("SRC1068_2_1067_acquisition", "source-intake/mts_residuals/P8_Y5_R10_1067_TAU_WEP_ACQUISITION_SCHEMA.csv", "TAQ1067_1_tau_numeric_option", "tau_WEP acquisition schema."),
        ("SRC1068_3_1066_tau_contract", "source-intake/mts_residuals/P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv", "TWP1066_7_verdict", "tau_WEP projection contract."),
        ("SRC1068_4_1053_tau", "source-intake/mts_residuals/P8_Y5_R10_1053_TAU_WEP_R10_PROJECTION_AUDIT.csv", "TPR1053_1_tau_WEP_definition", "old tau_WEP definition."),
        ("SRC1068_5_1061_tau", "source-intake/mts_residuals/P8_Y5_R10_1061_BETA_TAU_DERIVATION_ATTEMPT.csv", "DER1061_2_tau_WEP", "tau_WEP derivation attempt."),
        ("SRC1068_6_1061_material", "source-intake/mts_residuals/P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv", "MCON1061_0_test_pair", "MICROSCOPE Ti/Pt material convention."),
        ("SRC1068_7_708_wep_map", "source-intake/mts_residuals/P8_Y5_R10_708_PPN_GDOT_WEP_MAP.csv", "PGW708_0_R1_WEP", "WEP source/test charge map requirement."),
        ("SRC1068_8_948_bound_runner", "source-intake/mts_residuals/P8_Y5_R10_948_WEP_PRODUCT_BOUND_RUNNER.csv", "WEP948_0_WAS651_0_alpha_Coulomb", "older WEP bound runner."),
        ("SRC1068_9_988_pressure", "source-intake/mts_residuals/P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv", "WEP988_WAS651_0_alpha_Coulomb", "WEP alpha pressure import."),
        ("SRC1068_10_1029_tau_req", "source-intake/mts_residuals/P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv", "TAU1029_3_WEP_limit", "tau projection requirements."),
        ("SRC1068_11_1033_tauR10", "source-intake/mts_residuals/P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv", "TAUR1033_5_universal_cg_limit", "unity shortcut rejection analogy."),
        ("SRC1068_12_742_owner", "source-intake/mts_residuals/P8_Y5_R10_742_OBSERVED_TAU_OWNER_AUDIT.csv", "TOA742_4_owner_verdict", "observed tau owner audit."),
        ("SRC1068_13_742_verdict", "source-intake/mts_residuals/P8_Y5_R10_742_TAU_PROOF_VERDICT.csv", "TPV742_3_tau_owner_result", "tau proof verdict."),
        ("SRC1068_14_1066_delta", "source-intake/mts_residuals/P8_Y5_R10_1066_WEP_DELTA_W_PRIOR_WIDTH_SCHEMA.csv", "DWP1066_4_tau_WEP", "Delta_w/tau finite branch."),
        ("SRC1068_15_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound anchor."),
        ("SRC1068_16_393_common", "393-source-normalized-Newtonian-limit-under-identity-closure.md", "Only a constant, universal, range-independent", "measured-G common-mode guard."),
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


def acquisition_pack_rows() -> list[dict[str, str]]:
    return [
        {
            "pack_id": "TAP1068_0_source_worldtube",
            "component": "Earth/source worldtube",
            "needed_for": "source-leg normalization of the relative source-weight residual",
            "required_artifact": "source stress/profile/composition convention in the observed local frame",
            "current_status": "MISSING_SOURCE_WORLDTUBE",
            "claim_policy": "not scoreable",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "TAP1068_1_orbit_average",
            "component": "MICROSCOPE orbit/environment average",
            "needed_for": "projection from source residual to measured acceleration channel",
            "required_artifact": "orbit/attitude/readout averaging kernel with source path",
            "current_status": "MISSING_ORBIT_AVERAGING_KERNEL",
            "claim_policy": "not scoreable",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "TAP1068_2_eta_readout",
            "component": "eta_AB readout convention",
            "needed_for": "convert differential acceleration residual to the MICROSCOPE observable",
            "required_artifact": "eta_AB sign, normalization, frame, and absolute-value scoring convention",
            "current_status": "BOUND_ANCHOR_ONLY",
            "claim_policy": "bound available but not prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "TAP1068_3_material_response",
            "component": "Ti/Pt material response tensor",
            "needed_for": "test-body leg of the relative source-weight channel",
            "required_artifact": "full material/source response or parent theorem reducing it to Delta_w_TiPt",
            "current_status": "MATERIAL_PAIR_ONLY",
            "claim_policy": "smoke convention only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "TAP1068_4_observed_frame_force_map",
            "component": "observed-frame force map",
            "needed_for": "same-frame acceleration calculation and no hidden readout rescaling",
            "required_artifact": "force law in e_obs with units, calibration, and no measured-G relative absorption",
            "current_status": "MISSING_FORCE_READOUT_MAP",
            "claim_policy": "not scoreable",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "TAP1068_5_Xhat_normalization",
            "component": "Xhat/chi_X normalization",
            "needed_for": "compatibility with clock, R10, and WEP finite branches",
            "required_artifact": "shared parent normalization or explicitly separate finite-branch convention",
            "current_status": "MISSING_XHAT_NORMALIZATION",
            "claim_policy": "not scoreable",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "pack_id": "TAP1068_6_direct_product_fallback",
            "component": "direct P_WEP product",
            "needed_for": "avoid artificial split into Delta_w and tau if parent variation gives the observable directly",
            "required_artifact": "numeric or theorem-zero P_WEP_relative_source_weight with source path",
            "current_status": "MISSING_DIRECT_PRODUCT",
            "claim_policy": "runner refuses until numeric/theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def source_worldtube_rows() -> list[dict[str, str]]:
    return [
        {
            "worldtube_id": "SWT1068_0_source_stress_profile",
            "required_input": "T_source^Earth(x) or equivalent source-mass profile",
            "purpose": "source leg for WEP residual field",
            "accepted_form": "sourced profile/table or theorem reducing extended Earth to calibrated point-source convention",
            "current_status": "MISSING",
            "blocks": "tau_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "worldtube_id": "SWT1068_1_source_composition",
            "required_input": "Earth/source composition or source-charge convention",
            "purpose": "distinguish universal mass source from retained composition/source-weight residual",
            "accepted_form": "species/source map or proof that source leg is universal/common-mode",
            "current_status": "MISSING",
            "blocks": "Delta_w source/test split",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "worldtube_id": "SWT1068_2_GM_calibration",
            "required_input": "measured GM/G calibration convention",
            "purpose": "separate common mode from relative source weight",
            "accepted_form": "calibration row proving only common universal factors are absorbed",
            "current_status": "COMMON_MODE_GUARD_ONLY",
            "blocks": "fake measured-G absorption",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "worldtube_id": "SWT1068_3_finite_source_correction",
            "required_input": "finite-size and altitude/source support correction",
            "purpose": "maps source profile to spacecraft location",
            "accepted_form": "integral kernel or justified point-source limit with error bound",
            "current_status": "MISSING",
            "blocks": "numeric tau_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "worldtube_id": "SWT1068_4_frame_units",
            "required_input": "observed-frame units and source normalization",
            "purpose": "keep tau dimensionless and compatible with eta_AB",
            "accepted_form": "declared observed coframe and units conversion",
            "current_status": "MISSING",
            "blocks": "unit-safe runner input",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "worldtube_id": "SWT1068_5_verdict",
            "required_input": "source worldtube pack",
            "purpose": "source-side of tau_WEP",
            "accepted_form": "all SWT1068_0..4 real or theorem-reduced",
            "current_status": "SOURCE_WORLDTUBE_NOT_ACQUIRED",
            "blocks": "tau_WEP and WEP product scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def orbit_readout_rows() -> list[dict[str, str]]:
    return [
        {
            "orbit_id": "ORB1068_0_orbit_ephemeris",
            "required_input": "MICROSCOPE orbit/altitude/time sampling or averaged equivalent",
            "purpose": "turn Earth/source residual into instrument-frame acceleration",
            "accepted_form": "source-backed orbit parameters or official averaged kernel",
            "current_status": "MISSING",
            "blocks": "tau_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "orbit_id": "ORB1068_1_attitude_axis",
            "required_input": "instrument sensitive axis/attitude convention",
            "purpose": "project residual acceleration into measured channel",
            "accepted_form": "axis convention or theorem that scalar residual is orientation independent",
            "current_status": "MISSING",
            "blocks": "sign/readout convention",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "orbit_id": "ORB1068_2_eta_convention",
            "required_input": "eta_AB normalization/sign convention",
            "purpose": "define comparison to 2.8e-15 bound",
            "accepted_form": "eta_AB formula and absolute-value claim convention",
            "current_status": "BOUND_IMPORTED_BUT_FORMULA_NOT_PARENT_MAPPED",
            "blocks": "direct P_WEP row",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "orbit_id": "ORB1068_3_environmental_model",
            "required_input": "known systematics/environment subtraction convention",
            "purpose": "avoid mixing MTS residual with experimental nuisance subtraction",
            "accepted_form": "official readout/systematics convention or conservative envelope",
            "current_status": "MISSING",
            "blocks": "claim-grade tau",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "orbit_id": "ORB1068_4_average_kernel",
            "required_input": "time/orbit averaging kernel",
            "purpose": "define tau_WEP as an averaged projection, not an instantaneous guess",
            "accepted_form": "kernel K_orb(t) or stated averaged scalar convention",
            "current_status": "MISSING",
            "blocks": "numeric tau_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "orbit_id": "ORB1068_5_verdict",
            "required_input": "orbit/readout pack",
            "purpose": "experiment-side of tau_WEP",
            "accepted_form": "all ORB1068_0..4 real or theorem-reduced",
            "current_status": "ORBIT_READOUT_NOT_ACQUIRED",
            "blocks": "tau_WEP and WEP product scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def material_response_rows() -> list[dict[str, str]]:
    return [
        {
            "material_id": "MAT1068_0_pair_convention",
            "quantity": "MICROSCOPE Ti/Pt test pair",
            "value_or_status": "TA6V_minus_PtRh10",
            "source": "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv:MCON1061_0_test_pair",
            "current_status": "SMOKE_CONTEXT_AVAILABLE",
            "blocks": "does not itself provide material tensor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "material_id": "MAT1068_1_alpha_charge_smoke",
            "quantity": "Delta_Q_alpha_Coulomb_abs",
            "value_or_status": "0.001989808886825",
            "source": "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv:MCON1061_1_delta_Q_alpha",
            "current_status": "SMOKE_VALUE_AVAILABLE",
            "blocks": "alpha/Coulomb smoke channel is not the full relative source-weight tensor",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "material_id": "MAT1068_2_full_tensor",
            "quantity": "Ti/Pt relative-source material response tensor",
            "value_or_status": "MISSING_FULL_MATERIAL_TENSOR",
            "source": "needed: source-backed MICROSCOPE/material model or parent theorem",
            "current_status": "MISSING",
            "blocks": "Delta_w_TiPt mapping",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "material_id": "MAT1068_3_source_weight_response",
            "quantity": "Delta_w_TiPt response convention",
            "value_or_status": "MISSING_DELTA_W_RESPONSE_MAP",
            "source": "needed: source-only weight theorem or finite prior convention",
            "current_status": "MISSING",
            "blocks": "WEP product prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "material_id": "MAT1068_4_no_cancellation",
            "quantity": "signed material cancellation",
            "value_or_status": "FORBIDDEN_WITHOUT_FULL_SIGNED_MODEL",
            "source": "1066/1067 refusal gates",
            "current_status": "ABSOLUTE_VALUE_GUARD",
            "blocks": "fake WEP pass by sign tuning",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "material_id": "MAT1068_5_verdict",
            "quantity": "material response pack",
            "value_or_status": "MATERIAL_PAIR_ONLY_NOT_CLAIM_READY",
            "source": "1061 convention rows",
            "current_status": "NOT_ACQUIRED",
            "blocks": "tau_WEP/direct product scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def force_map_rows() -> list[dict[str, str]]:
    return [
        {
            "force_id": "FRM1068_0_observed_frame",
            "required_clause": "same observed coframe for source variation, force law, clocks, and readout",
            "formula_or_rule": "e_obs = e_source = e_force = e_readout through WEP order",
            "current_status": "CONDITIONAL_FROM_PRIOR_SPINE",
            "blocks": "frame-safe tau_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "force_id": "FRM1068_1_eta_mapping",
            "required_clause": "map residual force to eta_AB",
            "formula_or_rule": "eta_AB = readout[(a_A-a_B), calibration] in MICROSCOPE convention",
            "current_status": "BOUND_OBSERVABLE_KNOWN_MAP_NOT_DERIVED",
            "blocks": "direct product scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "force_id": "FRM1068_2_common_mode_separation",
            "required_clause": "common source normalization removed only by universal calibration",
            "formula_or_rule": "relative w_A/w_B cannot be absorbed into measured G or GM",
            "current_status": "GUARD_ACTIVE",
            "blocks": "fake local-GR pass",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "force_id": "FRM1068_3_units",
            "required_clause": "dimensionless tau/product convention",
            "formula_or_rule": "P_WEP_relative_source_weight must be dimensionless and comparable to eta_bound",
            "current_status": "SCHEMA_ONLY",
            "blocks": "runner validity",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "force_id": "FRM1068_4_direct_variation",
            "required_clause": "direct parent variation option",
            "formula_or_rule": "derive delta a_AB or eta_AB directly from parent action instead of split Delta_w*tau",
            "current_status": "MISSING_DIRECT_PRODUCT",
            "blocks": "fallback remains nonclaim",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "force_id": "FRM1068_5_verdict",
            "required_clause": "observed-frame force/readout map",
            "formula_or_rule": "source residual -> a_A-a_B -> eta_AB with units and calibration",
            "current_status": "FORCE_MAP_NOT_DERIVED",
            "blocks": "tau_WEP/direct product scoring",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def xhat_normalization_rows() -> list[dict[str, str]]:
    return [
        {
            "xhat_id": "XHN1068_0_shared_parent_norm",
            "quantity": "Xhat/chi_X normalization",
            "required_form": "same parent normalization used by clocks, WEP, and R10 or explicitly separated",
            "current_status": "MISSING_SHARED_NORMALIZATION",
            "risk": "tau_WEP cannot be compared to clock/R10 factors",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "xhat_id": "XHN1068_1_clock_transfer_guard",
            "quantity": "clock-to-WEP transfer",
            "required_form": "no clock screening imported into WEP without source/readout map",
            "current_status": "TRANSFER_BLOCKED",
            "risk": "fake tau_WEP via clock branch",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "xhat_id": "XHN1068_2_R10_transfer_guard",
            "quantity": "R10-to-WEP transfer",
            "required_form": "no tau_R10 unity or profile factor imported into WEP",
            "current_status": "TRANSFER_BLOCKED",
            "risk": "profile/unit contamination",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "xhat_id": "XHN1068_3_direct_product_escape",
            "quantity": "direct P_WEP product",
            "required_form": "parent variation gives dimensionless eta_AB product directly",
            "current_status": "MISSING_DIRECT_PRODUCT",
            "risk": "split-factor ambiguity persists",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "xhat_id": "XHN1068_4_verdict",
            "quantity": "Xhat normalization pack",
            "required_form": "shared normalization or direct product",
            "current_status": "NOT_ACQUIRED",
            "risk": "tau_WEP remains a free symbol",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def direct_product_fallback_rows() -> list[dict[str, str]]:
    return [
        {
            "fallback_id": "DPF1068_0_preferred_route",
            "route": "derive P_WEP_relative_source_weight directly",
            "accepted_evidence": "parent variation produces eta_AB residual or theorem-zero with units/source path",
            "current_status": "MISSING_DIRECT_PARENT_PRODUCT",
            "why_it_matters": "bypasses arbitrary split into Delta_w and tau_WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fallback_id": "DPF1068_1_split_route",
            "route": "P = abs(Delta_w_TiPt * tau_WEP)",
            "accepted_evidence": "both factors numeric/sourced or theorem-zero; no unity shortcut",
            "current_status": "MISSING_BOTH_FACTORS",
            "why_it_matters": "finite branch can still be tested if direct product is not derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fallback_id": "DPF1068_2_theorem_zero_route",
            "route": "P=0",
            "accepted_evidence": "parent source-scalar/action-scale theorem or WEP projection silence theorem",
            "current_status": "THEOREM_ZERO_UNSIGNED",
            "why_it_matters": "would close WEP branch without data-fitting",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "fallback_id": "DPF1068_3_refusal_rule",
            "route": "reject non-evidence",
            "accepted_evidence": "no tau=1, no Delta_w=0 by taste, no measured-G absorption, no cancellation",
            "current_status": "REFUSAL_ACTIVE",
            "why_it_matters": "prevents local-GR/WEP false positives",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1068_0_WEP_tau_acquisition_pack_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_DIRECT_PRODUCT_OR_DELTA_W_TiPt_TIMES_TAU_WEP",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1068_DIRECT_PRODUCT_FALLBACK.csv",
            "inputs_present": "eta_TiPt_bound=2.8e-15;material_pair=TA6V_minus_PtRh10;alpha_smoke_deltaQ=0.001989808886825",
            "required_inputs": "source worldtube;orbit/readout kernel;material response tensor;force map;Xhat normalization;direct product or Delta_w*tau",
            "derivation_status": "MISSING_TAU_WEP_ACQUISITION_PACK_INPUTS",
            "valid_for_claim": "false",
            "notes": "1068 is an acquisition pack; the row is intentionally nonclaim until the pack is filled.",
        }
    ]


def bound_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1068_0_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": "2.8e-15",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R1_WEP_source_charge",
            "bound_type": "numeric_bound_anchor_nonclaim",
            "valid_for_claim": "true",
            "notes": "MICROSCOPE Ti/Pt source-charge proxy bound; bound only, not an MTS prediction.",
        }
    ]


def product_status_rows(status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1068_0_WEP_tau_acquisition_pack",
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
            "gate_id": "CG1068_0_tau_acquisition_pack",
            "claim": "tau_WEP acquisition pack is complete",
            "gate_pass": "false",
            "reason": "source worldtube, orbit/readout, material tensor, force map, and Xhat normalization remain missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1068_1_tau_numeric",
            "claim": "tau_WEP is numeric or theorem-zero",
            "gate_pass": "false",
            "reason": "tau_WEP remains definition-only and tau=1 is explicitly forbidden",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1068_2_direct_product",
            "claim": "direct P_WEP product is derived",
            "gate_pass": "false",
            "reason": "no parent variation produces eta_AB residual directly yet",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1068_3_runner_score",
            "claim": "WEP product can be scored",
            "gate_pass": "false",
            "reason": "strict runner has valid_prediction_rows=0",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1068_4_local_GR_WEP",
            "claim": "local GR/WEP coupling branch is derived",
            "gate_pass": "false",
            "reason": "finite WEP projection and source-scalar theorem routes remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1068_0_pack_status",
            "decision": "tau_WEP acquisition pack is now explicit but empty of claim-grade data",
            "because": "each required component has a named row and refusal gate",
            "next_action": "source real MICROSCOPE/source/readout rows or derive direct product",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1068_1_best_route",
            "decision": "direct P_WEP derivation remains the cleanest theory route",
            "because": "it avoids arbitrary split-factor priors; if unavailable, tau pack components must be sourced",
            "next_action": "attempt direct eta_AB product theorem before web/data acquisition",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1068_2_best_next",
            "decision": "next target is direct WEP product theorem or first real tau source row",
            "because": "1068 names the missing pack; 1069 should either derive P_WEP or acquire the first real component",
            "next_action": "1069-Y5-R10-direct-WEP-product-theorem-or-first-real-tau-source-row.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "1069-Y5-R10-direct-WEP-product-theorem-or-first-real-tau-source-row.md",
            "objective": "attempt a direct parent variation theorem for P_WEP_relative_source_weight; if it fails, acquire the first real tau_WEP source row, starting with MICROSCOPE eta/readout convention or Earth/source worldtube metadata.",
            "include": "direct eta_AB variation theorem, no split-factor shortcut, official MICROSCOPE readout/source row requirements, source URL/DOI provenance, units, valid_for_claim refusal gates",
            "exclude": "setting tau_WEP to one, setting Delta_w to zero by taste, measured-G absorption of relative weights, cancellation arguments, public WEP/local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validate_outputs(
    outputs: dict[str, Path],
    sources: list[dict[str, str]],
    pack: list[dict[str, str]],
    worldtube: list[dict[str, str]],
    orbit: list[dict[str, str]],
    material: list[dict[str, str]],
    force: list[dict[str, str]],
    xhat: list[dict[str, str]],
    fallback: list[dict[str, str]],
    predictions: list[dict[str, str]],
    bounds: list[dict[str, str]],
    product_status: dict[str, Any],
    claims: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []

    def add(check_id: str, condition: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "result": "pass" if condition else "fail", "detail": detail, "generated_utc": stamp()})

    add("V1068_1_sources_exist_and_needles", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "every cited source path exists and every source needle was found")
    add("V1068_2_pack_components_written", len(pack) >= 7 and all(row["valid_for_claim"] == "false" for row in pack), "tau_WEP acquisition pack components are written as nonclaim rows")
    add("V1068_3_worldtube_missing_explicit", any(row["worldtube_id"] == "SWT1068_5_verdict" and row["current_status"] == "SOURCE_WORLDTUBE_NOT_ACQUIRED" for row in worldtube), "source worldtube remains explicitly missing")
    add("V1068_4_orbit_readout_missing_explicit", any(row["orbit_id"] == "ORB1068_5_verdict" and row["current_status"] == "ORBIT_READOUT_NOT_ACQUIRED" for row in orbit), "orbit/readout pack remains explicitly missing")
    add("V1068_5_material_response_guarded", any(row["material_id"] == "MAT1068_5_verdict" and row["current_status"] == "NOT_ACQUIRED" for row in material), "material tensor is not claim-ready")
    add("V1068_6_force_map_missing", any(row["force_id"] == "FRM1068_5_verdict" and row["current_status"] == "FORCE_MAP_NOT_DERIVED" for row in force), "observed-frame force map is not derived")
    add("V1068_7_xhat_missing", any(row["xhat_id"] == "XHN1068_4_verdict" and row["current_status"] == "NOT_ACQUIRED" for row in xhat), "Xhat normalization pack remains missing")
    add("V1068_8_direct_product_fallback_written", any(row["fallback_id"] == "DPF1068_0_preferred_route" and "MISSING" in row["current_status"] for row in fallback), "direct product fallback is written and missing")
    add("V1068_9_prediction_nonclaim", len(predictions) == 1 and "MISSING" in predictions[0]["product_value"] and predictions[0]["valid_for_claim"] == "false", "WEP tau acquisition prediction remains nonclaim")
    try:
        bound_numeric = len(bounds) == 1 and float(bounds[0]["bound_value"]) > 0
    except (KeyError, ValueError):
        bound_numeric = False
    add("V1068_10_bound_anchor_numeric", bound_numeric and bounds[0]["valid_for_claim"] == "true", "WEP bound anchor is numeric")
    add("V1068_11_runner_refuses_placeholder", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "strict runner refuses missing tau acquisition product")
    add("V1068_12_claim_gates_blocked", bool(claims) and all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims), "all tau/WEP/local-GR claim gates remain blocked")
    add("V1068_13_next_target_written", bool(next_rows) and next_rows[0]["next_target"].startswith("1069-Y5-R10-direct-WEP-product-theorem"), "next target selects direct WEP theorem or first real tau source row")
    generated_inside = all(ROOT in path.resolve().parents or path.resolve() == ROOT for path in outputs.values())
    add("V1068_14_generated_files_in_post_checkpoint", generated_inside, "all generated files are under post-checkpoint-work")
    formalization_count = count_formalization_modified_since_start()
    add("V1068_15_formalization_untouched", formalization_count == 0, f"formalization-workbench modified-file count since script start is {formalization_count}")
    summary_pass = all(row["result"] == "pass" for row in checks)
    checks.insert(0, {"check_id": "V1068_SUMMARY", "result": "pass" if summary_pass else "fail", "detail": "1068 WEP tau source-worldtube/orbit/readout acquisition-pack validation summary", "generated_utc": stamp()})
    return checks


def write_doc(
    sources: list[dict[str, str]],
    pack: list[dict[str, str]],
    worldtube: list[dict[str, str]],
    orbit: list[dict[str, str]],
    material: list[dict[str, str]],
    force: list[dict[str, str]],
    xhat: list[dict[str, str]],
    fallback: list[dict[str, str]],
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
            "# 1068 — WEP tau Source-Worldtube / Orbit / Readout Acquisition Pack",
            "",
            "**Current verdict:** `tau_WEP` is now decomposed into concrete acquisition components. None are claim-ready, and `tau_WEP=1` remains forbidden.",
            "",
            "**Best route:** derive `P_WEP_relative_source_weight` directly from parent variation if possible; otherwise source every tau component before scoring.",
            "",
            "**Runner result:** the strict WEP runner still refuses the placeholder with `valid_prediction_rows=0`.",
            "",
            "## Acquisition Pack",
            md_table(pack, ["pack_id", "component", "needed_for", "required_artifact", "current_status", "claim_policy", "valid_for_claim"]),
            "",
            "## Earth / Source Worldtube",
            md_table(worldtube, ["worldtube_id", "required_input", "purpose", "accepted_form", "current_status", "blocks", "valid_for_claim"]),
            "",
            "## MICROSCOPE Orbit / Readout",
            md_table(orbit, ["orbit_id", "required_input", "purpose", "accepted_form", "current_status", "blocks", "valid_for_claim"]),
            "",
            "## Material Response",
            md_table(material, ["material_id", "quantity", "value_or_status", "source", "current_status", "blocks", "valid_for_claim"]),
            "",
            "## Observed-Frame Force Map",
            md_table(force, ["force_id", "required_clause", "formula_or_rule", "current_status", "blocks", "valid_for_claim"]),
            "",
            "## Xhat Normalization",
            md_table(xhat, ["xhat_id", "quantity", "required_form", "current_status", "risk", "valid_for_claim"]),
            "",
            "## Direct Product Fallback",
            md_table(fallback, ["fallback_id", "route", "accepted_evidence", "current_status", "why_it_matters", "valid_for_claim"]),
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
    pack = acquisition_pack_rows()
    worldtube = source_worldtube_rows()
    orbit = orbit_readout_rows()
    material = material_response_rows()
    force = force_map_rows()
    xhat = xhat_normalization_rows()
    fallback = direct_product_fallback_rows()
    predictions = prediction_rows()
    bounds = bound_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs: dict[str, Path] = {
        "source_register": OUT / "P8_Y5_R10_1068_SOURCE_REGISTER.csv",
        "pack": OUT / "P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv",
        "worldtube": OUT / "P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv",
        "orbit": OUT / "P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv",
        "material": OUT / "P8_Y5_R10_1068_MATERIAL_RESPONSE_REQUIREMENTS.csv",
        "force": OUT / "P8_Y5_R10_1068_OBSERVED_FRAME_FORCE_MAP.csv",
        "xhat": OUT / "P8_Y5_R10_1068_XHAT_NORMALIZATION_LEDGER.csv",
        "fallback": OUT / "P8_Y5_R10_1068_DIRECT_PRODUCT_FALLBACK.csv",
        "predictions": PREDICTION_TEMPLATE,
        "bounds": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1068_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1068_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1068_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1068_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1068_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1068_VALIDATION.csv",
        "doc": DOC,
    }

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["pack"], pack)
    write_csv(outputs["worldtube"], worldtube)
    write_csv(outputs["orbit"], orbit)
    write_csv(outputs["material"], material)
    write_csv(outputs["force"], force)
    write_csv(outputs["xhat"], xhat)
    write_csv(outputs["fallback"], fallback)
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
        pack,
        worldtube,
        orbit,
        material,
        force,
        xhat,
        fallback,
        predictions,
        bounds,
        product_status,
        claims,
        next_rows,
    )
    write_csv(outputs["validation"], validation)
    write_doc(
        sources,
        pack,
        worldtube,
        orbit,
        material,
        force,
        xhat,
        fallback,
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
