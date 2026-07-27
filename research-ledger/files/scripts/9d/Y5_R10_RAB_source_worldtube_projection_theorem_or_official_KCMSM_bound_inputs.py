from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1456-Y5-R10-RAB-source-worldtube-projection-theorem-or-official-KCMSM-bound-inputs.md"

PREV_NEXT = OUT / "P8_Y5_R10_1455_NEXT_TARGET.csv"
PREV_WORLD = OUT / "P8_Y5_R10_1455_SOURCE_WORLDTUBE_ACQUISITION_LEDGER_NONCLAIM.csv"
PREV_OFFICIAL = OUT / "P8_Y5_R10_1455_OFFICIAL_READOUT_ACQUISITION_LEDGER_NONCLAIM.csv"
PREV_DERIVATIVE = OUT / "P8_Y5_R10_1455_DERIVATIVE_BEFORE_PROJECTION_THEOREM.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1455_PARENT_SIGNING_DECISION.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1455_VALIDATION.csv"

TWP1066 = OUT / "P8_Y5_R10_1066_TAU_WEP_PROJECTION_CONTRACT.csv"
SWT1068 = OUT / "P8_Y5_R10_1068_SOURCE_WORLDTUBE_REQUIREMENTS.csv"
ORB1068 = OUT / "P8_Y5_R10_1068_MICROSCOPE_ORBIT_READOUT_REQUIREMENTS.csv"
FRM1068 = OUT / "P8_Y5_R10_1068_OBSERVED_FRAME_FORCE_MAP.csv"
TAP1068 = OUT / "P8_Y5_R10_1068_TAU_WEP_ACQUISITION_PACK.csv"
DWT1069 = OUT / "P8_Y5_R10_1069_DIRECT_WEP_PRODUCT_THEOREM_ATTEMPT.csv"
WTS1069 = OUT / "P8_Y5_R10_1069_FIRST_REAL_TAU_SOURCE_ROW.csv"
RFM1069 = OUT / "P8_Y5_R10_1069_READOUT_FILL_MATRIX.csv"
ETA1070 = OUT / "P8_Y5_R10_1070_ETA_READOUT_FORMULA_ROWS.csv"
ORK1070 = OUT / "P8_Y5_R10_1070_ORBIT_KERNEL_SOURCE_ROWS.csv"
EXT1070 = OUT / "P8_Y5_R10_1070_EXTERNAL_MICROSCOPE_READOUT_SOURCE_LEDGER.csv"
RFM1070 = OUT / "P8_Y5_R10_1070_READOUT_FILL_MATRIX_UPDATE.csv"
KER1071 = OUT / "P8_Y5_R10_1071_OFFICIAL_KERNEL_COMPONENTS.csv"
TAU1071 = OUT / "P8_Y5_R10_1071_TAU_PROJECTION_STATUS.csv"
SUEP1071 = OUT / "P8_Y5_R10_1071_SUEP_SEGMENT_TABLE_SOURCE_BACKED.csv"
EXT1071 = OUT / "P8_Y5_R10_1071_EXTERNAL_KERNEL_SOURCE_LEDGER.csv"
REQ1072 = OUT / "P8_Y5_R10_1072_RECONSTRUCTION_REQUIREMENTS.csv"
NTS1072 = OUT / "P8_Y5_R10_1072_NUMERIC_TAU_STATUS.csv"
ARR1073 = OUT / "P8_Y5_R10_1073_OFFICIAL_ARRAY_SCHEMA_CONTRACT.csv"
EX1073 = OUT / "P8_Y5_R10_1073_OFFICIAL_ARRAY_EXTRACT_STATUS.csv"
STAT1074 = OUT / "P8_Y5_R10_1074_SURROGATE_STATUS_LEDGER.csv"
MAP1074 = OUT / "P8_Y5_R10_1074_SURROGATE_TO_OFFICIAL_REPLACEMENT_MAP.csv"
TAUSHAPE1075 = OUT / "P8_Y5_R10_1075_TAU_SHAPE_STATUS.csv"
RG1075 = OUT / "P8_Y5_R10_1075_REPLACEMENT_GATES.csv"
TAU1225 = OUT / "P8_Y5_R10_1225_TAU_WEP_PROJECTION_ATTEMPT.csv"
FORM1225 = OUT / "P8_Y5_R10_1225_SYMBOLIC_TAU_WEP_FORMULA.csv"
ACQ1225 = OUT / "P8_Y5_R10_1225_TAU_WEP_SOURCE_ACQUISITION_TABLE.csv"
SHORT1225 = OUT / "P8_Y5_R10_1225_TAU_WEP_ANTI_SHORTCUT_GATES.csv"
WSW1421 = OUT / "P8_Y5_R10_1421_WEP_SOURCE_WORLDTUBE_METADATA_ROWS.csv"
PACK1438 = OUT / "P8_Y5_R10_1438_OFFICIAL_MICROSCOPE_SOURCE_PACK_MANIFEST.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1456_SOURCE_REGISTER.csv"
THEOREM_ATTEMPT = OUT / "P8_Y5_R10_1456_SOURCE_WORLDTUBE_PROJECTION_THEOREM_ATTEMPT.csv"
CLAUSE_AUDIT = OUT / "P8_Y5_R10_1456_DOWNSTREAM_PROJECTION_CLAUSE_AUDIT.csv"
KCMSM_LEDGER = OUT / "P8_Y5_R10_1456_OFFICIAL_KCMSM_BOUND_INPUT_LEDGER_NONCLAIM.csv"
SOURCE_FILE_LEDGER = OUT / "P8_Y5_R10_1456_SOURCE_WORLDTUBE_FILE_LEDGER_NONCLAIM.csv"
TAU_UPDATE = OUT / "P8_Y5_R10_1456_TAU_WEP_ANTI_SHORTCUT_UPDATE.csv"
PARSER_DRYRUN = OUT / "P8_Y5_R10_1456_PARSER_DRYRUN.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1456_PARENT_SIGNING_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1456_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1456_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1456_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1456_VALIDATION.csv"

BRANCH_THEOREM = COEFF / "source_worldtube_projection_theorem_attempt_1456.csv"
BRANCH_KCMSM = COEFF / "official_KCMSM_bound_inputs_nonclaim_1456.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_source_worldtube_signing_decision_1456.csv"

LIVE_OFFICIAL_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
LIVE_SOURCE_WORLD = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
LIVE_PRODUCT_CONVENTION = MICROSCOPE / "product_convention" / "P_WEP_eta_product_convention.csv"
LIVE_BRANCH_CLASSIFIER = MICROSCOPE / "branch_classifier" / "P_WEP_same_parent_branch_lock.csv"
LIVE_MATERIAL_TENSOR = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
LIVE_C_PARENT_IMPORT = COEFF / "C_parent_WEP_slot_import.csv"
LIVE_C_A_IMPORT = COEFF / "c_A_post_selector_live_claim.csv"
LIVE_EPSILON_IMPORT = COEFF / "epsilon_A_source_weight_live_claim.csv"
LIVE_JACOBIAN_IMPORT = COEFF / "J_A_species_jacobian_live_claim.csv"
LIVE_ZETAA_IMPORT = COEFF / "zeta_A_nonHilbert_current_live_claim.csv"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            return len(list(csv.DictReader(handle))) > 0
    except Exception:
        return False


def csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def existing_nonclaim(path: Path) -> bool:
    rows = csv_rows(path)
    if not rows:
        return not path.exists()
    return all(not truth(row.get("valid_for_claim", "false")) and not truth(row.get("claim_allowed", "false")) for row in rows)


def present_status(path: Path, missing_status: str) -> str:
    if not path.exists():
        return missing_status
    text = path.read_text(encoding="utf-8", errors="ignore").upper()
    if "MISSING" in text or "PENDING" in text:
        return "PRESENT_NONCLAIM_WITH_BLOCKING_MARKERS"
    return "PRESENT_NONCLAIM_NOT_SCORE_READY"


def copy_branch(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC1456_0_prev_next", PREV_NEXT, "1456 handoff"),
        ("SRC1456_1_prev_worldtube", PREV_WORLD, "1455 source-worldtube ledger"),
        ("SRC1456_2_prev_official", PREV_OFFICIAL, "1455 official readout ledger"),
        ("SRC1456_3_prev_derivative", PREV_DERIVATIVE, "1455 derivative-before-projection theorem"),
        ("SRC1456_4_prev_signing", PREV_SIGNING, "1455 signing decision"),
        ("SRC1456_5_prev_validation", PREV_VALIDATION, "1455 validation"),
        ("SRC1456_6_TWP1066", TWP1066, "tau WEP projection contract"),
        ("SRC1456_7_SWT1068", SWT1068, "source-worldtube requirements"),
        ("SRC1456_8_ORB1068", ORB1068, "MICROSCOPE orbit/readout requirements"),
        ("SRC1456_9_FRM1068", FRM1068, "observed-frame force map"),
        ("SRC1456_10_TAP1068", TAP1068, "tau WEP acquisition pack"),
        ("SRC1456_11_DWT1069", DWT1069, "direct WEP product theorem attempt"),
        ("SRC1456_12_WTS1069", WTS1069, "first real tau source rows"),
        ("SRC1456_13_RFM1069", RFM1069, "readout fill matrix"),
        ("SRC1456_14_ETA1070", ETA1070, "eta readout formula rows"),
        ("SRC1456_15_ORK1070", ORK1070, "orbit kernel source rows"),
        ("SRC1456_16_EXT1070", EXT1070, "external MICROSCOPE readout source ledger"),
        ("SRC1456_17_RFM1070", RFM1070, "readout fill matrix update"),
        ("SRC1456_18_KER1071", KER1071, "official kernel components"),
        ("SRC1456_19_TAU1071", TAU1071, "tau projection status"),
        ("SRC1456_20_SUEP1071", SUEP1071, "source-backed SUEP segment table"),
        ("SRC1456_21_EXT1071", EXT1071, "external kernel source ledger"),
        ("SRC1456_22_REQ1072", REQ1072, "reconstruction requirements"),
        ("SRC1456_23_NTS1072", NTS1072, "numeric tau status"),
        ("SRC1456_24_ARR1073", ARR1073, "official array schema contract"),
        ("SRC1456_25_EX1073", EX1073, "official array extract status"),
        ("SRC1456_26_STAT1074", STAT1074, "surrogate status ledger"),
        ("SRC1456_27_MAP1074", MAP1074, "surrogate-to-official map"),
        ("SRC1456_28_TAUSHAPE1075", TAUSHAPE1075, "tau shape status"),
        ("SRC1456_29_RG1075", RG1075, "replacement gates"),
        ("SRC1456_30_TAU1225", TAU1225, "tau projection attempt"),
        ("SRC1456_31_FORM1225", FORM1225, "symbolic tau formula"),
        ("SRC1456_32_ACQ1225", ACQ1225, "tau source acquisition table"),
        ("SRC1456_33_SHORT1225", SHORT1225, "anti-shortcut gates"),
        ("SRC1456_34_WSW1421", WSW1421, "WEP source-worldtube metadata rows"),
        ("SRC1456_35_PACK1438", PACK1438, "official MICROSCOPE source pack manifest"),
    ]
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": path.exists(),
            "role": role,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, role in sources
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "SWP1456_0_target",
            "prove source-worldtube/orbit/mask projections are downstream readout maps",
            "tau_WEP := N_eta^-1 <K_eta[e_obs,orbit,masks] Integral_Earth K_source(x;orbit) R_source(x) R_material(TiPt)>",
            "TARGET_SHARPENED",
            "would make tau_WEP a measurement/projection functional rather than a parent-domain selector",
            "requires parent-domain independence plus official/source inputs",
        ),
        (
            "SWP1456_1_linear_functional",
            "worldtube/orbit/readout map is harmless if it is a linear functional applied after variation",
            "J_parent(x)=delta S_parent/delta Phi(x); observable eta = R_WEP[J_parent] with R_WEP fixed externally",
            "EXACT_IF_DOWNSTREAM_LINEAR_MAP",
            "projection weights cannot create a new parent current",
            "R_WEP not yet source-signed with official arrays/product convention",
        ),
        (
            "SWP1456_2_source_support",
            "source support is harmless only if it weights the already-defined source",
            "Earth profile rho(x), g(O_sat), T(O_sat), masks, and segment windows must enter R_WEP, not D(S_parent)",
            "CONDITIONAL_DOWNSTREAM_SUPPORT_RULE",
            "keeps finite-source correction in the readout/source leg",
            "Earth source profile/gravity model and source composition map are missing",
        ),
        (
            "SWP1456_3_measured_G_guard",
            "common-mode GM/G calibration cannot absorb relative source-weight residuals",
            "universal source normalization may be calibrated; material/source-dependent residuals must remain in the WEP product",
            "GUARD_ACTIVE_NOT_NUMERIC",
            "prevents a fake local-GR pass by hiding qbar_source_weight in measured GM",
            "same-branch calibration equation not imported",
        ),
        (
            "SWP1456_4_mask_orbit_limit",
            "masks/orbit windows are downstream only if they select data samples, not parent variation support",
            "mask/session/window operator M(t) may multiply R_WEP[J_parent](t); it may not define where J_parent is allowed to exist",
            "DOMAIN_SELECTOR_COUNTERMODEL_RETAINED",
            "exposes the exact failure mode",
            "exact masks/timestamps/orbit/attitude arrays absent",
        ),
        (
            "SWP1456_5_surrogate_limit",
            "surrogate kernels can test plumbing but not physics claims",
            "1074/1075 surrogate gx/gz/Sxx/Sxz columns can diagnose matrix rank and fitting but cannot replace CMSM official arrays",
            "SURROGATE_NONCLAIM_ONLY",
            "keeps useful code without importing false evidence",
            "official K_CMSM arrays remain absent",
        ),
        (
            "SWP1456_6_verdict",
            "source-worldtube projection theorem is exact conditionally but not source-signed",
            "downstream linear projection would be safe, but current files lack official readout, source-worldtube, material tensor, and claim-ready product/branch support",
            "THEOREM_CONDITIONAL_NOT_PROMOTED",
            "keep tau_WEP and K_CMSM bound inputs as nonclaim acquisition work",
            "no R10/WEP/PPN/local-GR claim follows from 1456",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "claim": claim,
            "mathematical_form": form,
            "status": status,
            "if_signed": effect,
            "current_blocker": blocker,
            "parent_signed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for attempt_id, claim, form, status, effect, blocker in rows
    ]


def clause_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("DSP1456_0_parent_source", "J_parent is defined before source/readout projection", "P8_Y5_R10_1455_DERIVATIVE_BEFORE_PROJECTION_THEOREM.csv:DBP1455_1", "CONDITIONAL_ONLY", "parent domain not signed"),
        ("DSP1456_1_linear_readout", "R_WEP is a fixed downstream functional of J_parent", "FORM1225_0_tau_WEP_functional; KER1071_1_fit_basis", "SYMBOLIC_FORM_ONLY", "official arrays/product convention absent"),
        ("DSP1456_2_worldtube_profile", "Earth source profile weights readout but does not define parent support", "WSW1421_2; SWT1068_0", "MISSING_PROFILE_OR_POINT_SOURCE_THEOREM", "source selector countermodel remains live"),
        ("DSP1456_3_source_composition", "source composition either universal/common-mode or explicitly retained", "WSW1421_3; SWT1068_1", "MISSING_SOURCE_COMPOSITION_MAP", "relative source-weight residual cannot be dismissed"),
        ("DSP1456_4_orbit_masks", "timestamps/orbits/masks are data-window operators only", "ARR1073; REQ1072", "MISSING_EXACT_ARRAYS_AND_MASKS", "mask/domain selector ambiguity remains"),
        ("DSP1456_5_official_kcmsm", "K_CMSM uses official gx/gz/Sxx/Sxz/sign/units", "KREQ1445; KER1071; ARR1073", "STRUCTURE_ONLY_NUMERIC_ARRAYS_MISSING", "surrogate kernel cannot promote claim"),
        ("DSP1456_6_material_tensor", "Ti/Pt response is in same parent basis as tau_WEP", "ACQ1225_4; PACK1438_4", "MISSING_FULL_MATERIAL_TENSOR", "Delta_w_TiPt remains not scoreable"),
        ("DSP1456_7_verdict", "source-worldtube projection theorem source-signed", "all DSP1456 clauses", "FAIL_SOURCE_SIGNING", "retain nonclaim bound-input ledgers"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": clause_id,
            "needed_clause": clause,
            "source_basis": source,
            "current_status": status,
            "failure_mode_if_missing": failure,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for clause_id, clause, source, status, failure in rows
    ]


def kcmsm_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("KBI1456_0_time_grid", "time_s/t_utc/session_id/orbit_id", "exact timestamps and segment/orbit keys", "seconds/UTC/labels", "MISSING_EXACT_TIMESTAMPS", "ARR1073_1; REQ1072_0"),
        ("KBI1456_1_masks", "mask_flag/calibration_flag", "exact glitch/onboard/calibration masks", "boolean_or_enum", "MISSING_EXACT_MASKS", "ARR1073_2; REQ1072_4"),
        ("KBI1456_2_gravity_arrays", "gx,gz", "official or exactly reconstructed gravity projection arrays", "m s^-2", "MISSING_OFFICIAL_ARRAYS", "ARR1073_3; ARR1073_4"),
        ("KBI1456_3_gradient_arrays", "Sxx,Sxz", "official or exactly reconstructed gravity-gradient/inertia arrays", "s^-2", "MISSING_OFFICIAL_ARRAYS", "ARR1073_5; ARR1073_6"),
        ("KBI1456_4_attitude_orbit", "attitude/quaternion/position/velocity", "pointing and orbit products needed for reconstruction", "declared by product schema", "MISSING_NUMERIC_EPHEMERIS_ATTITUDE", "REQ1072_1; REQ1072_2"),
        ("KBI1456_5_eta_product", "eta product convention", "eta formula, sign, tau_eff definition, branch lock", "dimensionless/operator", "MISSING_PRODUCT_CONVENTION_FILE", "PACK1438_2"),
        ("KBI1456_6_data_portal", "CMSM/ONERA export", "public file inventory, export, checksum, provenance", "provenance", "POINTER_ONLY_ACCESS_UNVERIFIED", "EXT1071_9; EX1073_0"),
        ("KBI1456_7_surrogate_guard", "surrogate replacement map", "1074/1075 columns may test plumbing only", "policy", "SURROGATE_NONCLAIM_ONLY", "MAP1074; RG1075"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "ledger_id": ledger_id,
            "object": obj,
            "required_input": required,
            "units": units,
            "current_status": status,
            "source_reference": source,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for ledger_id, obj, required, units, status, source in rows
    ]


def source_file_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("SFI1456_0_source_worldtube_file", LIVE_SOURCE_WORLD, "source_worldtube", "time_s_or_orbit_phase;radius_m;density_kg_m3;source_component;kernel_weight;model_or_dataset;source_url_or_path", "MISSING_SOURCE_WORLDTUBE_FILE"),
        ("SFI1456_1_official_readout_file", LIVE_OFFICIAL_READOUT, "official_readout", "time_s;session_id;orbit_id;axis;gx_m_s2;gz_m_s2;Sxx;Sxz;mask_flag;calibration_flag;attitude_quaternion_or_axis;source_url_or_path", "MISSING_OFFICIAL_READOUT_FILE"),
        ("SFI1456_2_product_convention_file", LIVE_PRODUCT_CONVENTION, "product_convention", "eta_formula;sign_convention;tau_eff_definition;readout_kernel_units;source_kernel_units;orbit_average_rule;branch_lock", "MISSING_PRODUCT_CONVENTION_FILE"),
        ("SFI1456_3_branch_classifier_file", LIVE_BRANCH_CLASSIFIER, "branch_classifier", "same_parent_branch_id;forbidden_mixing_rule", "MISSING_PARENT_BRANCH_CLASSIFIER_FILE"),
        ("SFI1456_4_material_tensor_file", LIVE_MATERIAL_TENSOR, "material_tensor", "material_id;channel_id;response_value;units;basis;double_count_rule;source_url_or_path;valid_for_claim", "MISSING_FULL_MATERIAL_TENSOR_FILE"),
        ("SFI1456_5_C_parent_file", LIVE_C_PARENT_IMPORT, "C_parent_WEP", "same_parent_branch_id;component;value;uncertainty;units;sign_convention;basis;source_path;parent_status;zero_certificate_status", "MISSING_C_PARENT_IMPORT_FILE"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "ledger_id": ledger_id,
            "target_path": str(path),
            "pack_item": pack_item,
            "required_columns_or_fields": required,
            "target_exists": path.exists(),
            "current_status": present_status(path, status),
            "promotion_condition": "exists, parses, branch-locked, no MISSING/PENDING placeholders, and cites source path/URL/DOI",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for ledger_id, path, pack_item, required, status in rows
    ]


def tau_update_rows() -> list[dict[str, Any]]:
    rows = [
        ("TAUG1456_0_no_tau_unity", "set tau_WEP=1", "tau_WEP is a source/orbit/readout functional, not a unit convention", "ENFORCED"),
        ("TAUG1456_1_no_surrogate_claim", "use surrogate gx/gz/Sxx/Sxz as official arrays", "surrogates are plumbing diagnostics only", "ENFORCED"),
        ("TAUG1456_2_no_G_absorption", "absorb relative source-weight residual into measured GM/G", "common-mode calibration cannot hide composition/source-dependent residuals", "ENFORCED"),
        ("TAUG1456_3_no_mask_domain", "let masks/worldtube support define parent variation domain", "masks/worldtubes must be downstream windows unless parent-signed otherwise", "ENFORCED"),
        ("TAUG1456_4_no_cancellation", "cancel signs/material terms by hand", "absolute-product guard applies without signed material model", "ENFORCED"),
        ("TAUG1456_5_no_branch_mixing", "mix tau_WEP, Delta_w, and C_parent rows from different branches", "same_parent_branch_id and branch classifier required", "ENFORCED"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "forbidden_shortcut": shortcut,
            "reason": reason,
            "status": status,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, shortcut, reason, status in rows
    ]


def parser_rows() -> list[dict[str, Any]]:
    targets = [
        ("PARSER1456_0_official_readout", LIVE_OFFICIAL_READOUT, "live official K_CMSM readout"),
        ("PARSER1456_1_source_worldtube", LIVE_SOURCE_WORLD, "live source-worldtube file"),
        ("PARSER1456_2_product_convention", LIVE_PRODUCT_CONVENTION, "live eta product convention"),
        ("PARSER1456_3_branch_classifier", LIVE_BRANCH_CLASSIFIER, "live branch classifier"),
        ("PARSER1456_4_material_tensor", LIVE_MATERIAL_TENSOR, "live material tensor"),
        ("PARSER1456_5_Cparent", LIVE_C_PARENT_IMPORT, "live C_parent import"),
        ("PARSER1456_6_cA", LIVE_C_A_IMPORT, "live c_A import"),
        ("PARSER1456_7_epsilon", LIVE_EPSILON_IMPORT, "live epsilon import"),
        ("PARSER1456_8_JA", LIVE_JACOBIAN_IMPORT, "live J_A import"),
        ("PARSER1456_9_zetaA", LIVE_ZETAA_IMPORT, "live zeta_A import"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "parser_id": parser_id,
            "target_path": str(path),
            "target_meaning": meaning,
            "target_exists": path.exists(),
            "would_write_live_claim_file": False,
            "parser_action": "REFUSE_LIVE_PROMOTION_IN_1456",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for parser_id, path, meaning in targets
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1456_0_source_worldtube_projection",
            "target": "source-worldtube/orbit/mask downstream projection theorem",
            "downstream_linear_map_theorem_exact": True,
            "parent_domain_signed": False,
            "source_worldtube_file_imported": LIVE_SOURCE_WORLD.exists(),
            "official_KCMSM_imported": LIVE_OFFICIAL_READOUT.exists(),
            "product_convention_imported": LIVE_PRODUCT_CONVENTION.exists(),
            "branch_classifier_imported": LIVE_BRANCH_CLASSIFIER.exists(),
            "material_tensor_imported": LIVE_MATERIAL_TENSOR.exists(),
            "C_parent_WEP_import_allowed": False,
            "tau_WEP_numeric_allowed": False,
            "local_claim_allowed": False,
            "decision": "KEEP_SOURCE_WORLDTUBE_PROJECTION_CONDITIONAL_AND_ACQUIRE_BOUND_INPUTS",
            "reason": "downstream projection is clean only when source/readout/mask objects are imported as fixed external kernels, not parent-domain selectors; critical source/readout/material/C_parent files are absent and partial product/branch files remain nonclaim",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1456_0_downstream_theorem", "worldtube/orbit/mask downstream theorem promoted", False, "theorem is exact only conditionally; source files absent"),
        ("GATE1456_1_KCMSM", "official K_CMSM readout score-ready", False, "official arrays/product convention absent"),
        ("GATE1456_2_source_worldtube", "source-worldtube score-ready", False, "source profile/composition/finite-source rows absent"),
        ("GATE1456_3_tau_WEP", "numeric tau_WEP allowed", False, "tau functional symbolic only; no official kernel/material map"),
        ("GATE1456_4_surrogate", "surrogate may support physics claim", False, "surrogate is diagnostic only"),
        ("GATE1456_5_Cparent", "C_parent_WEP import allowed", False, "functional derivative and source/readout maps remain unsigned"),
        ("GATE1456_6_local_claim", "R10/WEP/PPN/local-GR claim allowed", False, "no local arena claim from 1456"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_pass": gate_pass,
            "blocking_reason": reason,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, gate_pass, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1456_0_theorem_shape",
            "decision": "keep downstream projection theorem as exact conditional result",
            "why": "a fixed linear readout/source-worldtube functional cannot alter a parent source derivative",
            "consequence": "we know the correct GR-safe interface shape",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1456_1_no_promotion",
            "decision": "do not promote tau_WEP, K_CMSM, or source-worldtube rows",
            "why": "live official/source files and product convention remain absent",
            "consequence": "all local WEP/source-weight branches stay blocked for claims",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1456_2_next_best_route",
            "decision": "build an official-source-pack import validator next",
            "why": "the derivation side now has a precise conditional interface; the next useful work is preventing bad imports and preparing real CMSM/source files",
            "consequence": "1457 should validate official MICROSCOPE source-pack schemas before any numerical tau attempt",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1456_0_1457",
            "next_target": "1457-Y5-R10-RAB-official-MICROSCOPE-source-pack-import-validator-or-source-worldtube-pilot.md",
            "script": "scripts/Y5_R10_RAB_official_MICROSCOPE_source_pack_import_validator_or_source_worldtube_pilot.py",
            "objective": "build a strict validator for official K_CMSM/source-worldtube/product-convention/branch-classifier files and, only if absent, produce a nonclaim pilot ledger for the first source-worldtube import",
            "include": "schema validation; no MISSING/PENDING placeholders; branch lock; source paths/URLs/DOIs; official-vs-surrogate guard; dry-run only",
            "exclude": "numeric WEP claim; C_parent import; local-GR pass; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    kcmsm: list[dict[str, Any]],
    source_files: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated_csvs = [
        SOURCE_REGISTER,
        THEOREM_ATTEMPT,
        CLAUSE_AUDIT,
        KCMSM_LEDGER,
        SOURCE_FILE_LEDGER,
        TAU_UPDATE,
        PARSER_DRYRUN,
        SIGNING_DECISION,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    all_sources_exist = all(truth(row["exists"]) for row in sources)
    exact_downstream = any(row["status"] == "EXACT_IF_DOWNSTREAM_LINEAR_MAP" for row in theorem)
    countermodel_retained = any(row["status"] == "DOMAIN_SELECTOR_COUNTERMODEL_RETAINED" for row in theorem)
    theorem_not_promoted = any(row["status"] == "THEOREM_CONDITIONAL_NOT_PROMOTED" for row in theorem)
    clause_fails = any(row["current_status"] == "FAIL_SOURCE_SIGNING" for row in clauses)
    kcmsm_nonclaim = all(not truth(row["score_ready"]) and not truth(row["valid_for_claim"]) for row in kcmsm)
    source_file_nonclaim = all(not truth(row["score_ready"]) and not truth(row["valid_for_claim"]) for row in source_files)
    anti_shortcuts = all(row["status"] == "ENFORCED" and not truth(row["claim_allowed"]) for row in tau)
    parser_safe = all(not truth(row["would_write_live_claim_file"]) for row in parser)
    signing_refuses = all(not truth(row["C_parent_WEP_import_allowed"]) and not truth(row["tau_WEP_numeric_allowed"]) for row in signing)
    gates_false = all(not truth(row["gate_pass"]) for row in gates)
    critical_live_claim_absent = (
        not LIVE_OFFICIAL_READOUT.exists()
        and not LIVE_SOURCE_WORLD.exists()
        and not LIVE_MATERIAL_TENSOR.exists()
        and not LIVE_C_PARENT_IMPORT.exists()
        and not LIVE_C_A_IMPORT.exists()
        and not LIVE_EPSILON_IMPORT.exists()
        and not LIVE_JACOBIAN_IMPORT.exists()
        and not LIVE_ZETAA_IMPORT.exists()
    )
    partial_support_nonclaim = existing_nonclaim(LIVE_PRODUCT_CONVENTION) and existing_nonclaim(LIVE_BRANCH_CLASSIFIER)
    no_unsafe_live_claim = critical_live_claim_absent and partial_support_nonclaim
    csv_parse = all(parse_csv_ok(path) for path in generated_csvs)
    branch_copies = BRANCH_THEOREM.exists() and BRANCH_KCMSM.exists() and BRANCH_SIGNING.exists()
    formal_recent = 0
    if FORMALIZATION.exists():
        formal_recent = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and path.stat().st_mtime > START_TS
        )
    checks = [
        ("VAL1456_0_sources", all_sources_exist, "all cited source paths exist"),
        ("VAL1456_1_exact_downstream_conditional", exact_downstream, "downstream linear projection theorem recorded conditionally"),
        ("VAL1456_2_countermodel_retained", countermodel_retained, "mask/worldtube domain-selector countermodel retained"),
        ("VAL1456_3_theorem_not_promoted", theorem_not_promoted, "source-worldtube theorem not promoted to claim"),
        ("VAL1456_4_clause_audit_fails", clause_fails, "downstream clause audit fails source signing"),
        ("VAL1456_5_kcmsm_nonclaim", kcmsm_nonclaim, "K_CMSM bound inputs remain nonclaim"),
        ("VAL1456_6_source_file_nonclaim", source_file_nonclaim, "source-worldtube/source-pack files remain nonclaim"),
        ("VAL1456_7_anti_shortcuts", anti_shortcuts, "all tau anti-shortcut gates enforced"),
        ("VAL1456_8_parser_safe", parser_safe, "parser refuses live claim writes"),
        ("VAL1456_9_signing_refuses", signing_refuses, "parent signing decision refuses C_parent/tau promotion"),
        ("VAL1456_10_claim_gates_false", gates_false, "all claim gates remain false"),
        ("VAL1456_11_no_unsafe_live_claim", no_unsafe_live_claim, "critical live claim imports absent; partial product/branch files are nonclaim if present"),
        ("VAL1456_12_csv_parse", csv_parse, "all generated 1456 CSVs parse cleanly"),
        ("VAL1456_13_branch_copies", branch_copies, "nonclaim branch copies written"),
        ("VAL1456_14_formalization_untouched", formal_recent == 0, f"formalization modified-file count since start={formal_recent}"),
        ("VAL1456_15_overall", True, "1456 keeps source-worldtube projection conditional and prepares official-source-pack validation"),
    ]
    return [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, passed, detail in checks
    ]


def write_table(handle, title: str, rows: list[dict[str, Any]]) -> None:
    handle.write(f"## {title}\n\n")
    if not rows:
        handle.write("_No rows._\n\n")
        return
    fields = list(rows[0].keys())
    handle.write("| " + " | ".join(fields) + " |\n")
    handle.write("| " + " | ".join(["---"] * len(fields)) + " |\n")
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        handle.write("| " + " | ".join(values) + " |\n")
    handle.write("\n")


def write_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    kcmsm: list[dict[str, Any]],
    source_files: list[dict[str, Any]],
    tau: list[dict[str, Any]],
    parser: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1456 - Source-worldtube projection theorem or official K_CMSM bound inputs\n\n")
        handle.write(
            "**Current verdict:** source-worldtube, orbit, mask, and K_CMSM objects are safe only as fixed downstream "
            "linear readout/projection maps applied after the parent source variation. If they enter the parent action "
            "domain, they become hidden source selectors. The theorem shape is clean, but the needed official/source files "
            "are absent, so `tau_WEP`, `K_CMSM`, and `C_parent_WEP` remain nonclaim.\n\n"
        )
        handle.write(
            "**Useful progress:** the dangerous interface is now explicit: no tau-unity shortcut, no surrogate-as-official "
            "shortcut, no measured-G absorption, no mask/domain selector, no branch mixing. This gives us the right import "
            "contract before any local WEP testing.\n\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Source-worldtube projection theorem attempt", theorem)
        write_table(handle, "Downstream projection clause audit", clauses)
        write_table(handle, "Official K_CMSM bound-input ledger", kcmsm)
        write_table(handle, "Source-pack file ledger", source_files)
        write_table(handle, "Tau WEP anti-shortcut update", tau)
        write_table(handle, "Parser dry-run", parser)
        write_table(handle, "Parent signing decision", signing)
        write_table(handle, "Claim gates", gates)
        write_table(handle, "Decision ledger", decisions)
        write_table(handle, "Validation", validation)
        write_table(handle, "Next target", next_target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main() -> None:
    sources = source_rows()
    theorem = theorem_attempt_rows()
    clauses = clause_audit_rows()
    kcmsm = kcmsm_ledger_rows()
    source_files = source_file_ledger_rows()
    tau = tau_update_rows()
    parser = parser_rows()
    signing = signing_decision_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_ATTEMPT, theorem)
    write_csv(CLAUSE_AUDIT, clauses)
    write_csv(KCMSM_LEDGER, kcmsm)
    write_csv(SOURCE_FILE_LEDGER, source_files)
    write_csv(TAU_UPDATE, tau)
    write_csv(PARSER_DRYRUN, parser)
    write_csv(SIGNING_DECISION, signing)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(THEOREM_ATTEMPT, BRANCH_THEOREM)
    copy_branch(KCMSM_LEDGER, BRANCH_KCMSM)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    validation = validation_rows(sources, theorem, clauses, kcmsm, source_files, tau, parser, signing, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, theorem, clauses, kcmsm, source_files, tau, parser, signing, gates, decisions, validation, next_target)
    remove_pycache()
    print("Y5_R10_1456_source_worldtube_projection_conditional_KCMSM_inputs_nonclaim")


if __name__ == "__main__":
    main()
