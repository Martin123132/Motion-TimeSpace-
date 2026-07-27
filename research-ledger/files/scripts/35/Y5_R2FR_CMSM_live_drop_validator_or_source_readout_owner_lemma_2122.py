from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2122-Y5-R2FR-CMSM-live-drop-validator-or-source-readout-owner-lemma.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DROP_ROOT = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "drop-folder" / "1704"
DROP_LIVE = DROP_ROOT / "live"

CSV_2121_NEXT = OUT / "P8_Y5_PARENT_QLOC_2121_NEXT_TARGET.csv"
CSV_2121_VAL = OUT / "P8_Y5_BRR545_2121_VALIDATION.csv"
CSV_2121_FORK = OUT / "P8_Y5_PARENT_QLOC_2121_THEOREM_DATA_FORK.csv"
CSV_2121_IMPORT = OUT / "P8_Y5_PARENT_QLOC_2121_IMPORT_STATUS.csv"
CSV_2118_ZERO = OUT / "P8_Y5_PARENT_QLOC_2118_SOURCE_READOUT_ZERO_THEOREM_ATTEMPT.csv"
CSV_2118_KERNELS = OUT / "P8_Y5_PARENT_QLOC_2118_EXPLICIT_EXCEPTION_KERNELS.csv"
CSV_1963_ACTION = OUT / "P8_Y5_PARENT_QLOC_1963_MINIMAL_PARENT_ACTION_SIGNATURE.csv"
CSV_1963_NO_GAMMA = OUT / "P8_Y5_PARENT_QLOC_1963_NO_GAMMA_THEOREM.csv"
CSV_1898_COMM = OUT / "P8_Y5_PARENT_QLOC_1898_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv"
CSV_1899_OWNER = OUT / "P8_Y5_PARENT_QLOC_1899_ACTION_CURRENT_OWNER_LEMMA_ATTEMPT.csv"
CSV_1900_POINT = OUT / "P8_Y5_PARENT_QLOC_1900_WEP_SOURCE_WORLDTUBE_POINT_SOURCE_REDUCTION_ATTEMPT.csv"
CSV_1900_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1900_WEP_POINT_SOURCE_RESIDUAL_LEDGER_NONCLAIM.csv"
CSV_2117_EXCEPT = OUT / "P8_Y5_PARENT_QLOC_2117_SECTOR_EXCEPTION_LEDGER.csv"
CSV_2099_MAP = OUT / "P8_Y5_PARENT_QLOC_2099_DELTAGAMMA_COMPONENT_MAP.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed"}


def formalization_has_2122_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2122-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2122*",
        "*Y5_R2FR_CMSM_live_drop_validator_or_source_readout_owner_lemma_2122*",
        "*AFRAME_SOURCE_READOUT_OWNER_2122*",
        "*JR2122_SOURCE_READOUT*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2122_00_2121_next",
            CSV_2121_NEXT,
            ["NEXT2121_0_2122", "source/readout owner lemma"],
            "2121 handoff selects either strict live-drop validation or owner-lemma derivation.",
        ),
        (
            "SRC2122_01_2121_validation",
            CSV_2121_VAL,
            ["VAL2121_OVERALL", "PASS"],
            "2121 validation passed and kept tau_WEP blocked.",
        ),
        (
            "SRC2122_02_2121_fork",
            CSV_2121_FORK,
            ["THC2121_0_owned_readout_route", "THEOREM_ROUTE_OPEN_NOT_SIGNED", "THC2121_2_verdict"],
            "the data/theorem fork is explicit before 2122.",
        ),
        (
            "SRC2122_03_2121_import",
            CSV_2121_IMPORT,
            ["IMP2121_2_tau", "TAU_WEP_NOT_RUNNABLE"],
            "no live CMSM import is available yet.",
        ),
        (
            "SRC2122_04_2118_zero",
            CSV_2118_ZERO,
            ["SRZ2118_6_verdict", "ZERO_THEOREM_NOT_CLOSED"],
            "source/readout zero theorem was not closed in 2118.",
        ),
        (
            "SRC2122_05_2118_kernels",
            CSV_2118_KERNELS,
            ["KSR2118_0_source_worldtube_kernel", "KSR2118_7_total_no_cancellation"],
            "explicit source/readout residual kernels are already staged.",
        ),
        (
            "SRC2122_06_1963_action",
            CSV_1963_ACTION,
            ["ACT1963_4_matter_functor", "ACT1963_5_no_independent_Gamma_clause"],
            "owned-coframe candidate action supplies the conditional no-Gamma route.",
        ),
        (
            "SRC2122_07_1963_no_gamma",
            CSV_1963_NO_GAMMA,
            ["NGT1963_0_theorem", "NGT1963_2_q_vertical_silence"],
            "vertical q-silence theorem is available inside the candidate branch.",
        ),
        (
            "SRC2122_08_1898_commutator",
            CSV_1898_COMM,
            ["RVC1898_2_projection_commutator_survives", "COUNTERMODEL_ACTIVE"],
            "projection/source-worldtube commutator is the active obstruction.",
        ),
        (
            "SRC2122_09_1899_owner",
            CSV_1899_OWNER,
            ["ACO1899_0_target", "ACO1899_5_wep_readout_limit", "ACTION_CURRENT_OWNER_NOT_PARENT_DERIVED"],
            "action/current ownership route is sharp but not parent-derived.",
        ),
        (
            "SRC2122_10_1900_point_source",
            CSV_1900_POINT,
            ["PSR1900_3_source_composition_obstruction", "PSR1900_4_finite_source_multipole"],
            "source composition and finite-source multipoles block point-source shortcut.",
        ),
        (
            "SRC2122_11_1900_residual",
            CSV_1900_LEDGER,
            ["PSE1900_5_kernel_nullspace", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
            "WEP projection nullspace still lacks official arrays.",
        ),
        (
            "SRC2122_12_2117_exceptions",
            CSV_2117_EXCEPT,
            ["SEC2117_4_source_worldtube", "SEC2117_9_verdict", "PROMOTION_BLOCKED"],
            "sector exceptions block full owned-coframe promotion.",
        ),
        (
            "SRC2122_13_2099_map",
            CSV_2099_MAP,
            ["DGM2099_2_source_support", "DGM2099_5_orbital_readout"],
            "Delta_Gamma component map identifies readout/source operators still missing.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                path_exists=exists,
                expected_needles="; ".join(needles),
                needles_found=exists and all(needle in text for needle in needles),
                role=role,
            )
        )
    return rows


def live_artifact_specs() -> list[dict[str, object]]:
    return [
        {
            "artifact_id": "LIVE2122_0_readout",
            "filename": "P_WEP_K_CMSM_readout.csv",
            "role": "official CMSM readout arrays",
            "required_columns": [
                "same_parent_branch_id",
                "session_id",
                "segment_id",
                "time_s",
                "sample_index",
                "gx",
                "gz",
                "Sxx",
                "Sxz",
                "mask_flag",
                "calibration_flag",
                "frame",
                "axis_sign",
                "units",
                "source_path",
                "valid_for_claim",
                "claim_allowed",
            ],
            "numeric_columns": ["time_s", "gx", "gz", "Sxx", "Sxz"],
        },
        {
            "artifact_id": "LIVE2122_1_source",
            "filename": "P_WEP_R_source_Earth_worldtube.csv",
            "role": "Earth/source worldtube or source-profile weighting",
            "required_columns": [
                "same_parent_branch_id",
                "source_model_id",
                "profile_coordinate",
                "density_or_weight",
                "composition_basis_id",
                "frame",
                "units",
                "source_path",
                "valid_for_claim",
                "claim_allowed",
            ],
            "numeric_columns": ["profile_coordinate", "density_or_weight"],
        },
        {
            "artifact_id": "LIVE2122_2_material",
            "filename": "P_WEP_TiPt_material_response_tensor.csv",
            "role": "TA6V/PtRh10 material response tensor",
            "required_columns": [
                "same_parent_branch_id",
                "test_body",
                "material",
                "parent_basis_id",
                "response_value",
                "response_units",
                "source_path",
                "valid_for_claim",
                "claim_allowed",
            ],
            "numeric_columns": ["response_value"],
        },
        {
            "artifact_id": "LIVE2122_3_eta",
            "filename": "P_WEP_eta_product_convention.csv",
            "role": "reported eta convention and normalization",
            "required_columns": [
                "same_parent_branch_id",
                "eta_definition",
                "axis_sign",
                "absolute_value_rule",
                "orbit_average_rule",
                "normalization",
                "units",
                "source_path",
                "valid_for_claim",
                "claim_allowed",
            ],
            "numeric_columns": [],
        },
        {
            "artifact_id": "LIVE2122_4_branch_lock",
            "filename": "P_WEP_same_parent_branch_lock.csv",
            "role": "same-parent branch guard",
            "required_columns": [
                "same_parent_branch_id",
                "artifact_name",
                "artifact_hash",
                "branch_role",
                "source_path",
                "valid_for_claim",
                "claim_allowed",
            ],
            "numeric_columns": [],
        },
        {
            "artifact_id": "LIVE2122_5_parent",
            "filename": "P_WEP_C_parent_or_zero_certificate.csv",
            "role": "finite same-branch parent coefficient or zero certificate",
            "required_columns": [
                "same_parent_branch_id",
                "coefficient_id",
                "coefficient_value",
                "coefficient_units",
                "zero_certificate",
                "derivation_path",
                "source_path",
                "valid_for_claim",
                "claim_allowed",
            ],
            "numeric_columns": ["coefficient_value"],
        },
        {
            "artifact_id": "LIVE2122_6_tau_min",
            "filename": "P_WEP_tau_min_lower_bound.csv",
            "role": "strict tau nondegeneracy lower bound",
            "required_columns": [
                "same_parent_branch_id",
                "tau_min",
                "units",
                "derivation_or_data_method",
                "source_path",
                "valid_for_claim",
                "claim_allowed",
            ],
            "numeric_columns": ["tau_min"],
        },
        {
            "artifact_id": "LIVE2122_7_manifest",
            "filename": "P_WEP_tau_parser_manifest.json",
            "role": "parser manifest with source hashes, schemas, units and no-shortcut assertions",
            "required_columns": [],
            "numeric_columns": [],
        },
    ]


def contains_placeholder(value: object) -> bool:
    text = str(value).strip().upper()
    markers = ["MISSING", "PENDING", "FILL_ME", "TEMPLATE", "SURROGATE", "PLACEHOLDER", "TODO"]
    return any(marker in text for marker in markers)


def finite_number(value: object) -> bool:
    try:
        number = float(str(value).strip())
    except Exception:
        return False
    return math.isfinite(number)


def validate_live_csv(path: Path, required_columns: list[str], numeric_columns: list[str]) -> tuple[bool, str, int]:
    try:
        rows = read_csv_rows(path)
    except Exception as exc:
        return False, f"CSV_PARSE_ERROR:{exc}", 0
    if not rows:
        return False, "EMPTY_LIVE_CSV", 0
    columns = set(rows[0].keys())
    missing = [column for column in required_columns if column not in columns]
    if missing:
        return False, "MISSING_COLUMNS:" + ";".join(missing), len(rows)
    for live_row in rows:
        for key, value in live_row.items():
            if contains_placeholder(value):
                return False, f"PLACEHOLDER_MARKER:{key}", len(rows)
        for flag in ("valid_for_claim", "claim_allowed"):
            if flag in live_row and truthy(live_row[flag]):
                return False, f"CLAIM_FLAG_TRUE:{flag}", len(rows)
        for numeric_column in numeric_columns:
            if numeric_column in live_row and not finite_number(live_row[numeric_column]):
                return False, f"NONFINITE_NUMERIC:{numeric_column}", len(rows)
    return True, "LIVE_CSV_SCHEMA_VALID_NONCLAIM", len(rows)


def validate_live_manifest(path: Path) -> tuple[bool, str, int]:
    try:
        data = json.loads(read_text(path))
    except Exception as exc:
        return False, f"JSON_PARSE_ERROR:{exc}", 0
    text = json.dumps(data, sort_keys=True)
    if contains_placeholder(text):
        return False, "PLACEHOLDER_MARKER:manifest", 1
    required = ["same_parent_branch_id", "artifacts", "hashes", "schemas", "units", "sign_conventions", "no_shortcut_assertions"]
    missing = [key for key in required if key not in data]
    if missing:
        return False, "MISSING_MANIFEST_KEYS:" + ";".join(missing), 1
    return True, "LIVE_MANIFEST_SCHEMA_VALID_NONCLAIM", 1


def live_drop_preflight_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in live_artifact_specs():
        path = DROP_LIVE / str(spec["filename"])
        exists = path.exists()
        if not exists:
            schema_valid = False
            status = "MISSING_LIVE_ARTIFACT"
            row_count = 0
        elif path.suffix.lower() == ".json":
            schema_valid, status, row_count = validate_live_manifest(path)
        else:
            schema_valid, status, row_count = validate_live_csv(
                path,
                list(spec["required_columns"]),
                list(spec["numeric_columns"]),
            )
        rows.append(
            row(
                artifact_id=spec["artifact_id"],
                filename=spec["filename"],
                role=spec["role"],
                live_path=str(path),
                live_exists=exists,
                row_count=row_count,
                required_columns="; ".join(spec["required_columns"]),
                numeric_columns="; ".join(spec["numeric_columns"]),
                schema_valid=schema_valid,
                validation_status=status,
                usable_for_tau=exists and schema_valid,
            )
        )
    return rows


def owner_lemma_rows() -> list[dict[str, object]]:
    return [
        row(
            lemma_id="SRO2122_0_exact_conditional",
            target="source/readout Gamma-current zero",
            proof_or_requirement="If every source/readout object is R_i(Phi)=Rbar_i(q(Phi), e_obs, A_owned, theta) and every projector/support map Pi_i also descends through q/e_obs, then for v in ker(Dq), delta_v R_i=0 and delta_v(Pi_i J_i)=0.",
            source_evidence="ACT1963_4_matter_functor; ACT1963_5_no_independent_Gamma_clause; NGT1963_2_q_vertical_silence",
            current_status="CONDITIONAL_PROOF_VALID",
            closes_kernel="only under full q/e_obs descent of projectors, support and readout weights",
            zero_ready=False,
            next_action="prove the descent clauses sector by sector or keep finite kernels",
        ),
        row(
            lemma_id="SRO2122_1_source_worldtube",
            target="source support and source weights",
            proof_or_requirement="Need S_source, density/profile weights, composition basis, support tube and GM normalization to be common owned-coframe data, not representative- or species-relative couplings.",
            source_evidence="SRZ2118_0_source_worldtube_zero; SEC2117_4_source_worldtube; PSR1900_3_source_composition_obstruction",
            current_status="OWNER_CLAUSE_UNSIGNED",
            closes_kernel="KSR2118_0_source_worldtube_kernel remains",
            zero_ready=False,
            next_action="prove source-profile q-descent or acquire finite source kernel",
        ),
        row(
            lemma_id="SRO2122_2_clock_light",
            target="clock, rod and lightcone readout",
            proof_or_requirement="Need clock/rod/light response functionals to read only g_obs=e_obs^T eta e_obs and owned gauge data.",
            source_evidence="SRZ2118_1_clock_rod_zero; SRZ2118_2_lightcone_zero; DGM2099_3_clock_rods; DGM2099_4_photon_lightcone",
            current_status="RESPONSE_OPERATOR_UNSIGNED",
            closes_kernel="KSR2118_2_clock_redshift_kernel and KSR2118_3_lightcone_kernel remain",
            zero_ready=False,
            next_action="derive metric-only readout operators or fill response-operator bounds",
        ),
        row(
            lemma_id="SRO2122_3_orbit_GM",
            target="orbital and Newton/GM readout",
            proof_or_requirement="Need orbit/GM readout to be a downstream functor of source measure, Poisson/Gauss calibration and g_obs geodesic motion, with no fitted-G absorption.",
            source_evidence="SRZ2118_3_orbital_GM_zero; SEC2117_6_orbital_readout; DGM2099_5_orbital_readout",
            current_status="GM_TRANSFER_UNSIGNED",
            closes_kernel="KSR2118_1_orbit_WEP_kernel and KSR2118_4_orbital_GM_kernel remain",
            zero_ready=False,
            next_action="prove GM transfer convention from parent action or keep nonclaim orbit kernels",
        ),
        row(
            lemma_id="SRO2122_4_boundary_projector",
            target="boundary/domain/support projector",
            proof_or_requirement="Need domain, boundary transport, central worldline, support weight and projector stress to be fixed by the same parent readout map.",
            source_evidence="SRZ2118_4_boundary_domain_zero; SEC2117_7_boundary_nonHilbert; RVC1898_2_projection_commutator_survives",
            current_status="PROJECTOR_DESCENT_UNSIGNED",
            closes_kernel="KSR2118_5_boundary_domain_kernel remains",
            zero_ready=False,
            next_action="prove delta Pi=0 by q/e_obs descent or bound the commutator kernel",
        ),
        row(
            lemma_id="SRO2122_5_projective_trace",
            target="projective trace and source/readout trace coupling",
            proof_or_requirement="Need every sector to be projectively invariant, or the trace mode fixed before matter/readout coupling.",
            source_evidence="SRZ2118_5_projective_zero; 2119 candidate branch projective absence; SEC2117_9_verdict",
            current_status="GLOBAL_CERTIFICATE_UNSIGNED",
            closes_kernel="KSR2118_6_projective_trace_kernel remains globally",
            zero_ready=False,
            next_action="retain candidate-branch zero but keep global trace-coupling fallback",
        ),
        row(
            lemma_id="SRO2122_6_verdict",
            target="source/readout owner lemma",
            proof_or_requirement="The exact theorem exists, but the corpus has not signed the projector/support/readout descent assumptions needed to apply it.",
            source_evidence="1898 commutator, 1900 finite source obstruction, 2118 kernels, 2121 no live data",
            current_status="CONDITIONAL_THEOREM_BLOCKED_BY_COMMUTATOR_AND_SOURCE_SUPPORT",
            closes_kernel="none claimed",
            zero_ready=False,
            next_action="attack readout projection commutator directly in 2123",
        ),
    ]


def commutator_rows() -> list[dict[str, object]]:
    return [
        row(
            obstruction_id="COM2122_0_identity",
            obstruction="readout/source projection variation",
            mathematical_form="delta(Pi J)=Pi delta J + (delta Pi)J",
            source_anchor="RVC1898_2_projection_commutator_survives",
            current_status="IDENTITY_REGISTERED",
            zero_condition="delta Pi=0 and delta support/weight/boundary maps=0 along ker(Dq)",
            residual_if_not_zero="K_comm or sector-specific source/readout kernel",
        ),
        row(
            obstruction_id="COM2122_1_when_zero",
            obstruction="owner-lemma sufficient condition",
            mathematical_form="Pi_i=Pi_bar_i(q(Phi),e_obs,A_owned,theta) and J_i=Jbar_i(q(Phi),e_obs,A_owned,theta) implies delta_v(Pi_i J_i)=0 for v in ker(Dq)",
            source_anchor="NGT1963_2_q_vertical_silence; ACT1963_4_matter_functor",
            current_status="CONDITIONAL_ZERO_ROUTE",
            zero_condition="every readout projector and source support descends through q/e_obs",
            residual_if_not_zero="no zero claim; keep absolute residual sum",
        ),
        row(
            obstruction_id="COM2122_2_countermodel",
            obstruction="field/support/boundary/projector dependence",
            mathematical_form="If Pi depends on source worldtube, material channel, mask/orbit window or boundary transport not fixed by q/e_obs, then (delta Pi)J can be nonzero.",
            source_anchor="RVC1898_2_projection_commutator_survives; PSR1900_4_finite_source_multipole",
            current_status="COUNTERMODEL_ACTIVE",
            zero_condition="prove those dependencies are data-only descendants of the owned coframe branch",
            residual_if_not_zero="finite commutator kernels required before WEP/local-GR scoring",
        ),
        row(
            obstruction_id="COM2122_3_no_tau_shortcut",
            obstruction="empirical tau cannot prove theorem",
            mathematical_form="tau_WEP data can estimate P_inst[Delta a] but cannot prove parent source/readout ownership",
            source_anchor="ACO1899_5_wep_readout_limit; IMP2121_2_tau",
            current_status="DATA_ROUTE_SEPARATE",
            zero_condition="independent derivation of owner clauses",
            residual_if_not_zero="tau_WEP remains not runnable without live official arrays",
        ),
    ]


def kernel_status_rows() -> list[dict[str, object]]:
    kernels = [
        ("KER2122_0_source", "KSR2118_0_source_worldtube_kernel", "source support/profile/composition q-descent unsigned", "RETAINED"),
        ("KER2122_1_wep_orbit", "KSR2118_1_orbit_WEP_kernel", "official arrays and source/readout projector missing", "RETAINED"),
        ("KER2122_2_clock", "KSR2118_2_clock_redshift_kernel", "clock/rod response operator unsigned", "RETAINED"),
        ("KER2122_3_light", "KSR2118_3_lightcone_kernel", "photon/lightcone response operator unsigned", "RETAINED"),
        ("KER2122_4_orbital_gm", "KSR2118_4_orbital_GM_kernel", "GM transfer and fitted-G guard unsigned", "RETAINED"),
        ("KER2122_5_boundary", "KSR2118_5_boundary_domain_kernel", "projector/domain/boundary descent unsigned", "RETAINED"),
        ("KER2122_6_projective", "KSR2118_6_projective_trace_kernel", "global all-sector certificate unsigned", "RETAINED_GLOBAL_FALLBACK"),
        ("KER2122_7_total", "KSR2118_7_total_no_cancellation", "at least one retained component remains, so absolute no-cancellation sum remains", "RETAINED"),
    ]
    return [
        row(
            kernel_status_id=kernel_status_id,
            source_kernel=source_kernel,
            reason=reason,
            status=status,
            zero_claimed=False,
            score_ready=False,
            next_action="prove owner/commutator zero or acquire finite bound input",
        )
        for kernel_status_id, source_kernel, reason, status in kernels
    ]


def claim_gate_rows(live_rows: list[dict[str, object]], owner_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    live_complete = all(truthy(item["live_exists"]) and truthy(item["schema_valid"]) for item in live_rows)
    owner_closed = any(item["lemma_id"] == "SRO2122_6_verdict" and item["current_status"] == "OWNER_LEMMA_CLOSED" for item in owner_rows)
    return [
        row(gate_id="GATE2122_0_live_drop_validator_ready", gate="strict live-drop validator exists", gate_pass=True, rationale="exact filenames, schema checks, nonclaim flags, placeholder rejection and numeric checks are implemented"),
        row(gate_id="GATE2122_1_live_set_validated", gate="complete live CMSM/export set validates", gate_pass=live_complete, rationale="currently false unless all eight live artifacts exist and pass strict preflight"),
        row(gate_id="GATE2122_2_conditional_owner_theorem_written", gate="conditional source/readout owner theorem is explicit", gate_pass=True, rationale="chain-rule/q-descent condition is now written in theorem form"),
        row(gate_id="GATE2122_3_owner_clauses_signed", gate="source/readout owner clauses are parent signed", gate_pass=owner_closed, rationale="blocked by projection commutator, finite-source support and response-operator gaps"),
        row(gate_id="GATE2122_4_tau_WEP_runnable", gate="tau_WEP runner may score", gate_pass=False, rationale="no live official arrays and no zero theorem closure"),
        row(gate_id="GATE2122_5_local_GR_Newton_PPN_claim", gate="local GR/Newton/PPN claim allowed", gate_pass=False, rationale="source/readout kernels remain retained and nonclaim"),
    ]


def decision_rows(live_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    live_present = any(truthy(item["live_exists"]) for item in live_rows)
    return [
        row(
            decision_id="DEC2122_0",
            decision="LIVE_DROP_PREFLIGHT_ONLY" if live_present else "NO_LIVE_DROP_USE_DERIVATION_ROUTE",
            because="the live folder is checked strictly; absent or incomplete files cannot be promoted",
            next_action="keep validator in place, but do not score tau_WEP until a complete official set appears",
        ),
        row(
            decision_id="DEC2122_1",
            decision="OWNER_LEMMA_EXACT_BUT_CONDITIONAL",
            because="q/e_obs descent would kill source/readout Gamma currents by chain rule, but descent of projectors/support/readout weights is not signed",
            next_action="do not demote this to faith; attack the commutator directly",
        ),
        row(
            decision_id="DEC2122_2",
            decision="NO_LOCAL_GR_CLAIM",
            because="the no-Gamma candidate branch is promising but source/readout exception kernels still survive",
            next_action="2123 should prove delta Pi=0 or keep finite commutator kernels",
        ),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2122_0_2123",
            next_target="2123-Y5-R2FR-readout-projection-commutator-zero-or-finite-kernel-bound.md",
            script="scripts/Y5_R2FR_readout_projection_commutator_zero_or_finite_kernel_bound_2123.py",
            objective="Attack the exact obstruction left by 2122: prove the readout/source projection operator Pi, support weights, boundary transport and finite-source worldtube descend through q/e_obs so delta(Pi J)=Pi delta J, or retain finite commutator kernels for source/WEP/clock/light/orbit.",
            forbidden_shortcuts="assuming projector/support silence; using CMSM templates/surrogates as data; tau=1; fitted-G absorption; cancellation; local-GR/Newton/PPN claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(
    owner_rows: list[dict[str, object]],
    commutator: list[dict[str, object]],
    kernels: list[dict[str, object]],
    next_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2122_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_SOURCE_READOUT_OWNER_2122_NONCLAIM.csv", owner_rows + commutator + kernels),
        ("COPY2122_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2122_SOURCE_READOUT_OWNER_STATUS_NONCLAIM.csv", owner_rows + commutator + kernels),
        ("COPY2122_2_acquisition_queue", QUEUE / "JR2122_SOURCE_READOUT_OWNER_OR_LIVE_VALIDATOR_QUEUE.csv", next_rows + kernels),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    live_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    commutator: list[dict[str, object]],
    kernels: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    live_preflight_ok = len(live_rows) == 8 and all(item["validation_status"] in {"MISSING_LIVE_ARTIFACT", "LIVE_CSV_SCHEMA_VALID_NONCLAIM", "LIVE_MANIFEST_SCHEMA_VALID_NONCLAIM"} for item in live_rows)
    live_no_claim = all(not truthy(item.get("valid_for_claim", False)) and not truthy(item.get("claim_allowed", False)) for item in live_rows)
    owner_ok = any(item["lemma_id"] == "SRO2122_0_exact_conditional" and item["current_status"] == "CONDITIONAL_PROOF_VALID" for item in owner_rows) and any(item["lemma_id"] == "SRO2122_6_verdict" and item["current_status"] == "CONDITIONAL_THEOREM_BLOCKED_BY_COMMUTATOR_AND_SOURCE_SUPPORT" for item in owner_rows)
    commutator_ok = any(item["obstruction_id"] == "COM2122_2_countermodel" and item["current_status"] == "COUNTERMODEL_ACTIVE" for item in commutator)
    kernels_ok = any(item["kernel_status_id"] == "KER2122_7_total" and item["status"] == "RETAINED" for item in kernels) and all(not truthy(item["zero_claimed"]) and not truthy(item["score_ready"]) for item in kernels)
    gates_ok = any(item["gate_id"] == "GATE2122_0_live_drop_validator_ready" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2122_5_local_GR_Newton_PPN_claim" and not truthy(item["gate_pass"]) for item in gates)
    decisions_ok = any(item["decision_id"] == "DEC2122_1" and item["decision"] == "OWNER_LEMMA_EXACT_BUT_CONDITIONAL" for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2122_0_2123" for item in next_rows)
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, live_rows, owner_rows, commutator, kernels, gates, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2122_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, live_preflight_ok, live_no_claim, owner_ok, commutator_ok, kernels_ok, gates_ok, decisions_ok, next_ok, branch_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2122_00_sources", sources_ok, "all cited handoff/source files exist and contain expected needles"),
        ("VAL2122_01_live_preflight", live_preflight_ok, "live-drop preflight handles missing or valid nonclaim artifacts only"),
        ("VAL2122_02_live_no_claim", live_no_claim, "live rows remain nonclaim even if schemas validate"),
        ("VAL2122_03_owner_lemma", owner_ok, "conditional owner theorem is explicit and verdict remains blocked"),
        ("VAL2122_04_commutator", commutator_ok, "projection/source commutator obstruction is retained explicitly"),
        ("VAL2122_05_kernels", kernels_ok, "all source/readout kernels remain nonclaim and unscored"),
        ("VAL2122_06_gates", gates_ok, "validator-ready gate passes while local-GR/Newton/PPN claim gate fails"),
        ("VAL2122_07_decisions", decisions_ok, "decision ledger selects exact conditional theorem plus commutator attack"),
        ("VAL2122_08_next", next_ok, "next target is readout projection commutator zero or finite kernel bound"),
        ("VAL2122_09_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2122_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2122_11_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2122_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2122"),
        ("VAL2122_13_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2122_OVERALL", all_ok, "2122 builds the strict CMSM live-drop preflight, proves the exact conditional source/readout owner lemma, and keeps the branch blocked by the projection/source-support commutator."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    live_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    commutator: list[dict[str, object]],
    kernels: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2122 - Y5/R2FR CMSM Live-Drop Validator Or Source-Readout Owner Lemma",
            "## Current Verdict",
            "2122 makes forward progress, but it does not declare the local-GR bridge closed. The strict live-drop preflight is now encoded, so future CMSM files are either exact, source-backed and nonclaim, or rejected. In the current tree no complete live CMSM set is present, so the work proceeds along the derivation route.",
            "The derivation result is precise: if all source, support, projector, clock, light and orbit readouts descend through `q/e_obs`, then the source/readout Gamma-current vanishes by the same chain-rule logic as the 1963 no-Gamma theorem. The branch still fails as a claim because the projector/source-worldtube commutator is active: `delta(Pi J)=Pi delta J+(delta Pi)J`, and the corpus has not yet proven `delta Pi=0` for finite source, mask/orbit, boundary and response operators.",
            "So this is not a loop: the target has narrowed. The next fight is the commutator itself.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Live-Drop Preflight",
            md_table(live_rows, ["artifact_id", "filename", "live_path", "live_exists", "row_count", "schema_valid", "validation_status", "usable_for_tau", "valid_for_claim"]),
            "## Source/Readout Owner Lemma",
            md_table(owner_rows, ["lemma_id", "target", "current_status", "proof_or_requirement", "source_evidence", "closes_kernel", "zero_ready", "next_action"]),
            "## Commutator Obstruction",
            md_table(commutator, ["obstruction_id", "obstruction", "mathematical_form", "current_status", "zero_condition", "residual_if_not_zero", "valid_for_claim"]),
            "## Kernel Status",
            md_table(kernels, ["kernel_status_id", "source_kernel", "status", "reason", "zero_claimed", "score_ready", "next_action"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "gate", "gate_pass", "rationale", "valid_for_claim", "claim_allowed"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    DROP_LIVE.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    live_rows = live_drop_preflight_rows()
    owner_rows = owner_lemma_rows()
    commutator = commutator_rows()
    kernels = kernel_status_rows()
    gates = claim_gate_rows(live_rows, owner_rows)
    decisions = decision_rows(live_rows)
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2122_SOURCE_REGISTER.csv",
        "live": OUT / "P8_Y5_PARENT_QLOC_2122_LIVE_DROP_PREFLIGHT.csv",
        "owner": OUT / "P8_Y5_PARENT_QLOC_2122_SOURCE_READOUT_OWNER_LEMMA.csv",
        "commutator": OUT / "P8_Y5_PARENT_QLOC_2122_COMMUTATOR_OBSTRUCTION_LEDGER.csv",
        "kernels": OUT / "P8_Y5_PARENT_QLOC_2122_KERNEL_DEMOTION_OR_ZERO_STATUS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2122_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2122_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2122_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2122_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2122_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["live"], live_rows)
    write_csv(paths["owner"], owner_rows)
    write_csv(paths["commutator"], commutator)
    write_csv(paths["kernels"], kernels)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(owner_rows, commutator, kernels, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, live_rows, owner_rows, commutator, kernels, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, live_rows, owner_rows, commutator, kernels, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
