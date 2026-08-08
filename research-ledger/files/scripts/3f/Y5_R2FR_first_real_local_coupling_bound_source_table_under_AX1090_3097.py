from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3097"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "3097-Y5-R2FR-first-real-local-coupling-bound-source-table-under-AX1090.md"

SOURCES: dict[str, dict[str, Any]] = {
    "SRC3097_00_3096_next": {
        "path": RESIDUALS / "P8_Y5_R2FR_3096_NEXT_TARGET.csv",
        "needles": ["NEXT3096_0_primary", "first-real-local-coupling-bound-source-table"],
        "role": "3096 selects first real local coupling bound source table.",
    },
    "SRC3097_01_3096_doc": {
        "path": ROOT / "3096-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem-under-AX1090.md",
        "needles": ["first real local coupling bound inputs", "FMB3096_10_total_qbarXT_envelope"],
        "role": "3096 establishes the bound pack and asks for real source rows.",
    },
    "SRC3097_02_1851_doc": {
        "path": ROOT / "1851-Y5-R2FR-first-real-local-coupling-bound-source-table.md",
        "needles": ["genuine source-acquisition win", "MTS component bound still waits"],
        "role": "1851 precedent for real source anchors with blocked MTS translations.",
    },
    "SRC3097_03_1851_sources": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1851_OBSERVABLE_BOUND_SOURCE_TABLE.csv",
        "needles": ["OBS1851_2_PPN_CASSINI_2003", "source_backed_observable"],
        "role": "1851 observable source-bound table.",
    },
    "SRC3097_04_1851_translation": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1851_MTS_TRANSLATION_GATES.csv",
        "needles": ["TRG1851_0_cg_to_PPN", "MISSING_MTS_TO_PPN_MAP"],
        "role": "1851 translation gates block direct MTS component bounds.",
    },
    "SRC3097_05_1851_component": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1851_COMPONENT_BOUND_STATUS.csv",
        "needles": ["CBS1851_6_total_qbarXT", "SOURCE_TABLE_READY_COMPONENT_CLAIM_BLOCKED"],
        "role": "1851 component status table.",
    },
    "SRC3097_06_1851_local_matrix": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1851_LOCAL_TEST_MATRIX.csv",
        "needles": ["LTM1851_0_R10", "SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING"],
        "role": "1851 local test matrix with real anchors.",
    },
    "SRC3097_07_1851_next": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1851_NEXT_TARGET.csv",
        "needles": ["NEXT1851_0_primary", "PPN-common-frame-cg-translation-gate"],
        "role": "1851 selects PPN/common-frame translation gate.",
    },
    "SRC3097_08_1029_ppn": {
        "path": RESIDUALS / "P8_Y5_R10_1029_TAU_PROJECTION_REQUIREMENTS.csv",
        "needles": ["TAU1029_1_PPN_gamma_beta", "MISSING_PPN_RESPONSE_MATRIX"],
        "role": "1029 precedent for c_g to PPN translation requirements.",
    },
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3097_SOURCE_REGISTER.csv",
    "observable_bounds": RESIDUALS / "P8_Y5_R2FR_3097_OBSERVABLE_BOUND_SOURCE_TABLE.csv",
    "translation_gates": RESIDUALS / "P8_Y5_R2FR_3097_MTS_TRANSLATION_GATES.csv",
    "conditional_translations": RESIDUALS / "P8_Y5_R2FR_3097_CONDITIONAL_BOUND_TRANSLATIONS.csv",
    "component_status": RESIDUALS / "P8_Y5_R2FR_3097_COMPONENT_BOUND_STATUS.csv",
    "local_matrix": RESIDUALS / "P8_Y5_R2FR_3097_LOCAL_TEST_MATRIX.csv",
    "claim_gate": RESIDUALS / "P8_Y5_R2FR_3097_CLAIM_GATE.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3097_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3097_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3097_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3097_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "observable_bounds_copy": LOCAL_BOUNDS / "observable_bound_source_table_3097_NONCLAIM.csv",
    "translation_gates_copy": LOCAL_BOUNDS / "mts_translation_gates_3097_NONCLAIM.csv",
    "component_status_copy": LOCAL_BOUNDS / "component_bound_status_3097_NONCLAIM.csv",
    "local_matrix_copy": LOCAL_BOUNDS / "local_test_matrix_3097_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3097_PPN_common_frame_cg_translation_NEXT_NONCLAIM.csv",
}


def meta() -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def remove_pycache() -> None:
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def file_hash(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def source_parse_ok(path: Path) -> bool:
    return csv_ok(path) if path.suffix.lower() == ".csv" else path.exists()


def with_meta(output_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    base = meta()
    return [{**base, **row} for row in output_rows]


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in output_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in output_rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def source_rows() -> list[dict[str, Any]]:
    output_rows = []
    for source_id, source in SOURCES.items():
        path = Path(source["path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        output_rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "parse_ok": source_parse_ok(path),
                "sha256": file_hash(path),
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
            }
        )
    return with_meta(output_rows)


def observable_bound_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "bound_id": "OBS3097_0_R10_EOTWASH_2020",
                "arena": "R10_short_range",
                "observable": "Yukawa alpha(lambda) gravitational-strength threshold",
                "central_value": "",
                "one_sigma": "",
                "conservative_bound_value": 1.0,
                "bound_rule": "95pct anchor: alpha=1 excluded for lambda >= 38.6 micrometer; not a full digitized curve",
                "lambda_value": 38.6,
                "lambda_units": "micrometer",
                "observable_units": "dimensionless",
                "confidence": "95pct",
                "source_id": "SRC3097_EOTWASH_2020",
                "source_url": "https://arxiv.org/abs/2002.11761",
                "extraction_method": "abstract_threshold_anchor",
                "full_curve": False,
                "source_backed_observable": True,
                "direct_mts_component_bound": False,
            },
            {
                "bound_id": "OBS3097_1_WEP_MICROSCOPE_2022",
                "arena": "WEP",
                "observable": "Eotvos eta(Ti,Pt)",
                "central_value": -1.5e-15,
                "one_sigma": 2.745906043549196e-15,
                "conservative_bound_value": 6.991812087098392e-15,
                "bound_rule": "|central| + 2*sqrt(stat^2+syst^2)",
                "lambda_value": "",
                "lambda_units": "",
                "observable_units": "dimensionless",
                "confidence": "derived_conservative_2sigma_from_reported_1sigma",
                "source_id": "SRC3097_MICROSCOPE_2022",
                "source_url": "https://arxiv.org/abs/2209.15487",
                "extraction_method": "abstract_reported_central_stat_syst",
                "full_curve": "",
                "source_backed_observable": True,
                "direct_mts_component_bound": False,
            },
            {
                "bound_id": "OBS3097_2_PPN_CASSINI_2003",
                "arena": "PPN",
                "observable": "gamma_minus_1",
                "central_value": 2.1e-05,
                "one_sigma": 2.3e-05,
                "conservative_bound_value": 6.7e-05,
                "bound_rule": "|central| + 2*sigma",
                "lambda_value": "",
                "lambda_units": "",
                "observable_units": "dimensionless",
                "confidence": "derived_conservative_2sigma_from_reported_1sigma",
                "source_id": "SRC3097_CASSINI_2003",
                "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
                "extraction_method": "abstract_reported_gamma_minus_one",
                "full_curve": "",
                "source_backed_observable": True,
                "direct_mts_component_bound": False,
            },
            {
                "bound_id": "OBS3097_3_CLOCK_ROSENBAND_2008",
                "arena": "clock_fine_structure",
                "observable": "alpha_dot_over_alpha",
                "central_value": -1.6e-17,
                "one_sigma": 2.3e-17,
                "conservative_bound_value": 6.2e-17,
                "bound_rule": "|central| + 2*sigma",
                "lambda_value": "",
                "lambda_units": "",
                "observable_units": "per_year",
                "confidence": "derived_conservative_2sigma_from_reported_preliminary_1sigma",
                "source_id": "SRC3097_ROSENBAND_2008",
                "source_url": "https://tf.nist.gov/general/pdf/2280.pdf",
                "extraction_method": "paper_text_reported_alpha_drift",
                "full_curve": "",
                "source_backed_observable": True,
                "direct_mts_component_bound": False,
            },
            {
                "bound_id": "OBS3097_4_ORBITAL_LLR_GDOT_2018",
                "arena": "orbital_Gdot",
                "observable": "Gdot_over_G",
                "central_value": 7.1e-14,
                "one_sigma": 7.6e-14,
                "conservative_bound_value": 2.23e-13,
                "bound_rule": "|central| + 2*sigma",
                "lambda_value": "",
                "lambda_units": "",
                "observable_units": "per_year",
                "confidence": "derived_conservative_2sigma_from_reported_1sigma",
                "source_id": "SRC3097_LLR_HOFMANN_2018",
                "source_url": "https://ui.adsabs.harvard.edu/abs/2018CQGra..35c5015H",
                "extraction_method": "ADS_abstract_reported_result",
                "full_curve": "",
                "source_backed_observable": True,
                "direct_mts_component_bound": False,
            },
            {
                "bound_id": "OBS3097_5_ORBITAL_LLR_EP_2012",
                "arena": "orbital_EP",
                "observable": "Earth-Moon differential acceleration toward Sun",
                "central_value": "",
                "one_sigma": "",
                "conservative_bound_value": 1.4e-13,
                "bound_rule": "reported EP upper-bound anchor",
                "lambda_value": "",
                "lambda_units": "",
                "observable_units": "dimensionless",
                "confidence": "reported_upper_bound_anchor",
                "source_id": "SRC3097_LLR_EP_2012",
                "source_url": "https://arxiv.org/abs/1203.2150",
                "extraction_method": "reported_bound_anchor",
                "full_curve": "",
                "source_backed_observable": True,
                "direct_mts_component_bound": False,
            },
        ]
    )


def translation_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("TRG3097_0_cg_to_PPN", "c_g", "OBS3097_2_PPN_CASSINI_2003", "derive tau_PPN and show c_g is the scalar/common-frame parameter entering gamma_minus_1", "MISSING_MTS_TO_PPN_MAP"),
        ("TRG3097_1_cg_to_R10", "c_g", "OBS3097_0_R10_EOTWASH_2020", "derive alpha_R10(lambda_X)=K_X Qbar_XH qbar_XT tau_R10 and map c_g contribution", "MISSING_TAU_R10_AND_KX_QBAR_LAMBDA"),
        ("TRG3097_2_bA_to_WEP", "b_A", "OBS3097_1_WEP_MICROSCOPE_2022", "derive material sensitivity vector s_A(Ti,Pt) and source/test charge projection", "MISSING_MATERIAL_SENSITIVITY_MAP"),
        ("TRG3097_3_balpha_to_clock", "b_alpha", "OBS3097_3_CLOCK_ROSENBAND_2008", "derive Xdot or environmental X-profile coupling to clock/fine-structure residual", "MISSING_X_PROFILE_OR_TIME_PROJECTION"),
        ("TRG3097_4_delta_kappa_to_orbital_EP", "delta_kappa_A", "OBS3097_5_ORBITAL_LLR_EP_2012", "derive Earth/Moon source-current composition projection", "MISSING_SOURCE_COMPOSITION_MAP"),
        ("TRG3097_5_qnonH_support_to_Gdot", "q_nonH;Delta_W_support;q_boundary", "OBS3097_4_ORBITAL_LLR_GDOT_2018", "derive non-Hilbert/support/source-tail projection into secular GM or Gdot", "MISSING_ORBITAL_SOURCE_SUPPORT_MAP"),
    ]
    return with_meta(
        [
            {
                "gate_id": gate_id,
                "mts_component": component,
                "observable_bound_id": observable,
                "needed_translation": needed,
                "current_translation_status": status,
                "source_bound_available": True,
                "direct_component_bound_now": False,
            }
            for gate_id, component, observable, needed, status in gates
        ]
    )


def conditional_translation_rows() -> list[dict[str, Any]]:
    translations = [
        ("CBT3097_0_scalar_tensor_cg_proxy", "If MTS c_g exactly reduces to a massless scalar-tensor alpha0 with gamma-1=-2 alpha0^2/(1+alpha0^2)", "OBS3097_2_PPN_CASSINI_2003", "alpha0_abs_proxy", 0.005787918451395113, "dimensionless", "MTS has not derived this scalar-tensor reduction or tau_PPN normalization"),
        ("CBT3097_1_R10_alpha_anchor_proxy", "If the MTS R10 branch produces a single Yukawa alpha(lambda) with lambda_X=38.6 micrometer", "OBS3097_0_R10_EOTWASH_2020", "abs_alpha_R10_proxy", 1.0, "dimensionless_at_lambda_38p6um", "only an alpha=1 threshold anchor, not a digitized curve or MTS K_X Qbar_XH qbar_XT product"),
        ("CBT3097_2_WEP_differential_charge_proxy", "If eta_AB maps directly to a differential material coupling with unit source normalization", "OBS3097_1_WEP_MICROSCOPE_2022", "abs_delta_q_material_proxy", 6.991812087098392e-15, "dimensionless", "MTS material sensitivity and source-current normalization are not derived"),
        ("CBT3097_3_clock_alpha_proxy", "If b_alpha couples to monotonic time drift with unit Xdot per year", "OBS3097_3_CLOCK_ROSENBAND_2008", "abs_balpha_time_proxy", 6.2e-17, "per_year", "MTS X-profile/time projection is not derived"),
    ]
    return with_meta(
        [
            {
                "conditional_id": conditional_id,
                "assumption": assumption,
                "input_bound_id": input_bound_id,
                "derived_proxy_quantity": quantity,
                "derived_proxy_bound": bound,
                "units": units,
                "translation_valid_for_MTS": False,
                "why_not_claim": why,
            }
            for conditional_id, assumption, input_bound_id, quantity, bound, units, why in translations
        ]
    )


def component_status_rows() -> list[dict[str, Any]]:
    statuses = [
        ("CBS3097_0_cg", "c_g", "OBS3097_2_PPN_CASSINI_2003;OBS3097_0_R10_EOTWASH_2020", "MISSING_MTS_PROJECTION", "OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING"),
        ("CBS3097_1_bdis", "b_dis", "OBS3097_2_PPN_CASSINI_2003;OBS3097_3_CLOCK_ROSENBAND_2008", "MISSING_DISFORMAL_PROJECTION", "OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING"),
        ("CBS3097_2_bA", "b_A", "OBS3097_1_WEP_MICROSCOPE_2022;OBS3097_5_ORBITAL_LLR_EP_2012", "MISSING_MATERIAL_SENSITIVITY_MAP", "OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING"),
        ("CBS3097_3_balpha", "b_alpha", "OBS3097_3_CLOCK_ROSENBAND_2008", "MISSING_X_PROFILE_OR_TIME_PROJECTION", "OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING"),
        ("CBS3097_4_delta_kappa_A", "delta_kappa_A", "OBS3097_1_WEP_MICROSCOPE_2022;OBS3097_5_ORBITAL_LLR_EP_2012", "MISSING_SOURCE_COMPOSITION_MAP", "OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING"),
        ("CBS3097_5_qnonH_support_boundary", "q_nonH;Delta_W_support;q_boundary", "OBS3097_4_ORBITAL_LLR_GDOT_2018;OBS3097_5_ORBITAL_LLR_EP_2012", "MISSING_ORBITAL_SOURCE_SUPPORT_MAP", "OBSERVABLE_BOUNDS_EXIST_TRANSLATION_MISSING"),
        ("CBS3097_6_total_qbarXT", "qbar_XT_bound_abs", "OBS3097_0_R10_EOTWASH_2020;OBS3097_1_WEP_MICROSCOPE_2022;OBS3097_2_PPN_CASSINI_2003;OBS3097_3_CLOCK_ROSENBAND_2008;OBS3097_4_ORBITAL_LLR_GDOT_2018;OBS3097_5_ORBITAL_LLR_EP_2012", "MISSING_ALL_TRANSLATION_GATES", "SOURCE_TABLE_READY_COMPONENT_CLAIM_BLOCKED"),
    ]
    return with_meta(
        [
            {
                "component_id": component_id,
                "symbol": symbol,
                "source_backed_observable_anchors": anchors,
                "component_numeric_bound": bound,
                "best_current_status": status,
                "claim_allowed": False,
            }
            for component_id, symbol, anchors, bound, status in statuses
        ]
    )


def local_matrix_rows() -> list[dict[str, Any]]:
    matrix = [
        ("LTM3097_0_R10", "short_range_R10", "OBS3097_0_R10_EOTWASH_2020", "lambda_X;K_X;Qbar_XH;qbar_XT_bound_abs;tau_R10"),
        ("LTM3097_1_WEP", "WEP", "OBS3097_1_WEP_MICROSCOPE_2022;OBS3097_5_ORBITAL_LLR_EP_2012", "material sensitivities;source-current composition;delta_kappa_A;b_A;b_marker"),
        ("LTM3097_2_PPN", "PPN", "OBS3097_2_PPN_CASSINI_2003", "tau_PPN;c_g;b_dis;q_nonH;support/boundary mapping"),
        ("LTM3097_3_clock_EM", "clock_fine_structure_EM", "OBS3097_3_CLOCK_ROSENBAND_2008", "Xdot/profile;b_alpha;b_A;clock sensitivity map"),
        ("LTM3097_4_orbital", "orbital_source_support", "OBS3097_4_ORBITAL_LLR_GDOT_2018;OBS3097_5_ORBITAL_LLR_EP_2012", "q_nonH;Delta_W_support;q_boundary;source support and GM calibration mapping"),
    ]
    return with_meta(
        [
            {
                "arena_id": arena_id,
                "arena": arena,
                "real_source_bound": source_bound,
                "mts_inputs_needed": inputs,
                "status": "SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING",
                "claim_allowed": False,
            }
            for arena_id, arena, source_bound, inputs in matrix
        ]
    )


def claim_gate_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "gate_id": "CG3097_0_real_sources",
                "claim": "real local observable bound sources exist",
                "gate_pass": True,
                "reason": "R10, WEP, PPN, clock and orbital anchors are recorded with numeric observable bounds",
                "source_backed_observable": True,
                "claim_allowed_for_physics": False,
            },
            {
                "gate_id": "CG3097_1_direct_mts_component_bounds",
                "claim": "MTS component bounds are numeric",
                "gate_pass": False,
                "reason": "all direct MTS component translations remain missing",
                "source_backed_observable": True,
                "claim_allowed_for_physics": False,
            },
            {
                "gate_id": "CG3097_2_local_GR_claim",
                "claim": "local GR recovered from bounded couplings",
                "gate_pass": False,
                "reason": "qbar_XT_bound_abs cannot be evaluated until translation/projection gates close",
                "source_backed_observable": True,
                "claim_allowed_for_physics": False,
            },
            {
                "gate_id": "CG3097_3_no_public_claim",
                "claim": "R10/WEP/PPN/clock/orbital local pass",
                "gate_pass": False,
                "reason": "observable anchors are evidence inputs only; MTS map is missing",
                "source_backed_observable": True,
                "claim_allowed_for_physics": False,
            },
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "decision_id": "DEC3097_0_source_table_win",
                "decision": "3097 succeeds as real source acquisition, not as an MTS pass.",
                "because": "local observable bounds are explicit, numeric and source-linked across R10/WEP/PPN/clock/orbital arenas",
                "next_action": "derive the MTS projection maps that turn those observable bounds into component bounds",
            },
            {
                "decision_id": "DEC3097_1_translation_status",
                "decision": "Every MTS component bound remains blocked by translation gates.",
                "because": "c_g, b_A, b_alpha, q_nonH and total qbarXT require tau/projection/normalization maps",
                "next_action": "start with the PPN/common-frame c_g translation gate",
            },
            {
                "decision_id": "DEC3097_2_best_next",
                "decision": "Next target should derive the PPN/common-frame translation gate.",
                "because": "Cassini gives the cleanest weak-field common-frame anchor and can reject over-large c_g branches quickly",
                "next_action": "3098-Y5-R2FR-PPN-common-frame-cg-translation-gate-under-AX1090.md",
            },
        ]
    )


def next_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "route_id": "NEXT3097_0_primary",
                "next_checkpoint": "3098-Y5-R2FR-PPN-common-frame-cg-translation-gate-under-AX1090.md",
                "script": "scripts/Y5_R2FR_PPN_common_frame_cg_translation_gate_under_AX1090_3098.py",
                "objective": "derive or reject the mapping from MTS common frame coupling c_g into PPN gamma/tau_PPN, using Cassini as a real source-backed observable bound",
                "selection_status": "selected",
                "success_condition": "either c_g obtains a conditional/numeric PPN translation with clear assumptions, or the PPN/common-frame route is demoted to source-only closure",
            },
            {
                "route_id": "NEXT3097_1_parallel",
                "next_checkpoint": "3098b-Y5-R2FR-WEP-material-sensitivity-bA-translation-gate-under-AX1090.md",
                "script": "scripts/Y5_R2FR_WEP_material_sensitivity_bA_translation_gate_under_AX1090_3098b.py",
                "objective": "derive material sensitivity map from b_A/delta_kappa_A to MICROSCOPE/LLR WEP observables",
                "selection_status": "held",
                "success_condition": "material/source charge projection becomes explicit enough for a bound row",
            },
        ]
    )


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = {
        "observable_bounds_copy": OUTPUTS["observable_bounds"],
        "translation_gates_copy": OUTPUTS["translation_gates"],
        "component_status_copy": OUTPUTS["component_status"],
        "local_matrix_copy": OUTPUTS["local_matrix"],
        "next_copy": OUTPUTS["next"],
    }
    output_rows = []
    for key, source_path in copies.items():
        target_path = BRANCH_OUTPUTS[key]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        output_rows.append(
            {
                **meta(),
                "copy_id": f"COPY3097_{key}",
                "source_path": str(source_path),
                "target_path": str(target_path),
                "target_exists": target_path.exists(),
            }
        )
    write_csv(OUTPUTS["branches"], output_rows)
    return output_rows


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in output_rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 3097 Y5 R2FR first real local coupling bound source table under AX1090",
        "",
        "**Progress:** 3097 is a real source-acquisition checkpoint. R10, WEP, PPN, clock/fine-structure and orbital anchors now have source-linked numeric observable bounds in the current AX1090 branch.",
        "",
        "**Current verdict:** this is not an MTS physics pass. Every direct MTS component bound still waits on a translation/projection theorem, so `c_g`, `b_A`, `b_alpha`, `q_nonH`, `qbar_XT`, local GR and R10 pass claims remain blocked.",
        "",
        "**Claim ceiling:** no R10, WEP, clock, EM, PPN, orbital, local-GR/Newton, finite-alpha, or source-zero pass is allowed from 3097.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "parse_ok", "needles_present", "missing_needles", "role"]),
        "",
        "## Observable Bound Source Table",
        markdown_table(data["observable_bounds"], ["bound_id", "arena", "observable", "conservative_bound_value", "bound_rule", "lambda_value", "lambda_units", "observable_units", "source_url", "source_backed_observable", "direct_mts_component_bound", "valid_for_claim"]),
        "",
        "## MTS Translation Gates",
        markdown_table(data["translation_gates"], ["gate_id", "mts_component", "observable_bound_id", "needed_translation", "current_translation_status", "source_bound_available", "direct_component_bound_now", "valid_for_claim"]),
        "",
        "## Conditional Bound Translations",
        markdown_table(data["conditional_translations"], ["conditional_id", "assumption", "input_bound_id", "derived_proxy_quantity", "derived_proxy_bound", "units", "translation_valid_for_MTS", "why_not_claim", "valid_for_claim"]),
        "",
        "## Component Bound Status",
        markdown_table(data["component_status"], ["component_id", "symbol", "source_backed_observable_anchors", "component_numeric_bound", "best_current_status", "claim_allowed", "valid_for_claim"]),
        "",
        "## Local Test Matrix",
        markdown_table(data["local_matrix"], ["arena_id", "arena", "real_source_bound", "mts_inputs_needed", "status", "claim_allowed", "valid_for_claim"]),
        "",
        "## Claim Gate",
        markdown_table(data["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "source_backed_observable", "claim_allowed_for_physics", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "next_checkpoint", "script", "objective", "selection_status", "success_condition"]),
        "",
        "## Validation",
        markdown_table(data["validation"], ["validation_id", "check_pass", "detail", "artifact"]),
        "",
        "## Working Interpretation",
        "This is the Mayweather route: clean ropes, not a fake knockout. The project now has real local-test anchors around the coupling gap. The next fight is deriving one translation map cleanly enough that the first component can actually be constrained.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def contains_status(path: Path, field: str, expected: str) -> bool:
    return any(str(row.get(field, "")) == expected for row in rows(path))


def all_false(path: Path, field: str) -> bool:
    table = rows(path)
    return bool(table) and all(not boolish(row.get(field, "")) for row in table)


def positive_observable_bounds() -> bool:
    for row in rows(OUTPUTS["observable_bounds"]):
        try:
            value = float(row["conservative_bound_value"])
        except (KeyError, TypeError, ValueError):
            return False
        if value <= 0:
            return False
        if not row.get("source_url", "").startswith("http"):
            return False
        if not boolish(row.get("source_backed_observable")):
            return False
        if boolish(row.get("direct_mts_component_bound")):
            return False
    return True


def validation_rows() -> list[dict[str, Any]]:
    formalization_3097 = list(FORMALIZATION.rglob("*3097*")) if FORMALIZATION.exists() else []
    checks = [
        ("VAL3097_00_sources_csv", csv_ok(OUTPUTS["sources"]), "source register parses", OUTPUTS["sources"]),
        ("VAL3097_01_sources_exist", all(boolish(row["exists"]) for row in rows(OUTPUTS["sources"])), "every cited local source path exists", OUTPUTS["sources"]),
        ("VAL3097_02_sources_parse", all(boolish(row["parse_ok"]) for row in rows(OUTPUTS["sources"])), "every cited csv source parses", OUTPUTS["sources"]),
        ("VAL3097_03_needles_present", all(boolish(row["needles_present"]) for row in rows(OUTPUTS["sources"])), "all source needles found", OUTPUTS["sources"]),
        ("VAL3097_04_doc_created", DOC.exists(), "checkpoint markdown created", DOC),
        ("VAL3097_05_observable_bounds_parse", csv_ok(OUTPUTS["observable_bounds"]), "observable source table parses", OUTPUTS["observable_bounds"]),
        ("VAL3097_06_observable_bounds_numeric", positive_observable_bounds(), "observable bounds are positive, sourced and not direct MTS component claims", OUTPUTS["observable_bounds"]),
        ("VAL3097_07_translation_parse", csv_ok(OUTPUTS["translation_gates"]), "translation gates parse", OUTPUTS["translation_gates"]),
        ("VAL3097_08_translation_blocks", contains_status(OUTPUTS["translation_gates"], "current_translation_status", "MISSING_MTS_TO_PPN_MAP") and all_false(OUTPUTS["translation_gates"], "direct_component_bound_now"), "translation gates keep direct component bounds blocked", OUTPUTS["translation_gates"]),
        ("VAL3097_09_conditional_parse", csv_ok(OUTPUTS["conditional_translations"]), "conditional translations parse", OUTPUTS["conditional_translations"]),
        ("VAL3097_10_conditionals_nonclaim", all_false(OUTPUTS["conditional_translations"], "translation_valid_for_MTS"), "conditional proxy bounds remain nonclaim", OUTPUTS["conditional_translations"]),
        ("VAL3097_11_component_parse", csv_ok(OUTPUTS["component_status"]), "component status parses", OUTPUTS["component_status"]),
        ("VAL3097_12_component_blocked", contains_status(OUTPUTS["component_status"], "best_current_status", "SOURCE_TABLE_READY_COMPONENT_CLAIM_BLOCKED"), "component claims remain blocked", OUTPUTS["component_status"]),
        ("VAL3097_13_local_matrix_parse", csv_ok(OUTPUTS["local_matrix"]), "local test matrix parses", OUTPUTS["local_matrix"]),
        ("VAL3097_14_local_matrix_nonclaim", contains_status(OUTPUTS["local_matrix"], "status", "SOURCE_ANCHOR_READY_MTS_TRANSLATION_MISSING") and all_false(OUTPUTS["local_matrix"], "claim_allowed"), "local test matrix records real anchors but missing MTS translations", OUTPUTS["local_matrix"]),
        ("VAL3097_15_claim_gate_parse", csv_ok(OUTPUTS["claim_gate"]), "claim gate parses", OUTPUTS["claim_gate"]),
        ("VAL3097_16_physics_claims_blocked", all_false(OUTPUTS["claim_gate"], "claim_allowed_for_physics"), "all physics claims remain blocked", OUTPUTS["claim_gate"]),
        ("VAL3097_17_decisions_parse", csv_ok(OUTPUTS["decisions"]), "decision ledger parses", OUTPUTS["decisions"]),
        ("VAL3097_18_next_parse", csv_ok(OUTPUTS["next"]), "next target parses", OUTPUTS["next"]),
        ("VAL3097_19_next_selected", contains_status(OUTPUTS["next"], "selection_status", "selected"), "primary next target selected", OUTPUTS["next"]),
        ("VAL3097_20_branch_copies_parse", csv_ok(OUTPUTS["branches"]), "branch copy ledger parses", OUTPUTS["branches"]),
        ("VAL3097_21_branch_copies_exist", all(boolish(row["target_exists"]) for row in rows(OUTPUTS["branches"])), "all branch copies exist", OUTPUTS["branches"]),
        ("VAL3097_22_no_formalization_edit", len(formalization_3097) == 0, "no 3097 files created under formalization-workbench", FORMALIZATION),
        ("VAL3097_23_pycache_removed", not PYCACHE.exists(), "scripts __pycache__ absent after run", PYCACHE),
    ]
    return [
        {
            **meta(),
            "validation_id": validation_id,
            "check_pass": bool(check_pass),
            "detail": detail,
            "artifact": str(artifact),
        }
        for validation_id, check_pass, detail, artifact in checks
    ]


def main() -> None:
    remove_pycache()
    for directory in [RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_rows(),
        "observable_bounds": observable_bound_rows(),
        "translation_gates": translation_gate_rows(),
        "conditional_translations": conditional_translation_rows(),
        "component_status": component_status_rows(),
        "local_matrix": local_matrix_rows(),
        "claim_gate": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_rows(),
    }

    for key, output_rows in data.items():
        write_csv(OUTPUTS[key], output_rows)

    data["branches"] = copy_branch_outputs()
    data["validation"] = []
    write_doc(data)
    data["validation"] = validation_rows()
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    remove_pycache()

    passed = sum(1 for row in data["validation"] if boolish(row["check_pass"]))
    print(f"3097 first real source table checkpoint written: {passed}/{len(data['validation'])} validation checks passed")
    print(DOC)
    print(OUTPUTS["validation"])


if __name__ == "__main__":
    main()
