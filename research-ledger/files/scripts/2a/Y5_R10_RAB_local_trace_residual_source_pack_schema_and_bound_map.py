from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
BRANCH_ROOT = ROOT / "source-intake" / "microscope" / "branch_locked_wep"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1434-Y5-R10-RAB-local-trace-residual-source-pack-schema-and-bound-map.md"
BRANCH_ID_FILE = BRANCH_ROOT / "branch_id.csv"
RESIDUAL_ACTIVATION_FILE = BRANCH_ROOT / "residuals" / "local_trace_residual_activation.csv"
RESIDUAL_SOURCE_PACK_SCHEMA_FILE = BRANCH_ROOT / "residuals" / "local_trace_residual_source_pack_schema.csv"
LOCAL_TRACE_BOUND_MAP_FILE = BRANCH_ROOT / "residuals" / "local_trace_bound_map.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1434_SOURCE_REGISTER.csv"
RESIDUAL_COMPONENTS = OUT / "P8_Y5_R10_1434_RESIDUAL_COMPONENTS.csv"
ARENA_BOUND_MAP = OUT / "P8_Y5_R10_1434_ARENA_BOUND_MAP.csv"
REQUIRED_INPUTS_LEDGER = OUT / "P8_Y5_R10_1434_REQUIRED_INPUTS_LEDGER.csv"
SOURCE_PACK_SCHEMA = OUT / "P8_Y5_R10_1434_SOURCE_PACK_SCHEMA.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_R10_1434_RUNNER_REFUSAL_STATUS.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1434_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1434_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1434_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1434_VALIDATION.csv"


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


def branch_id() -> str:
    rows = read_csv(BRANCH_ID_FILE)
    if len(rows) != 1:
        raise ValueError(f"expected one branch row, got {len(rows)}")
    value = rows[0].get("same_parent_branch_id", "").strip()
    if not value:
        raise ValueError("same_parent_branch_id missing")
    return value


def source_register_rows(branch: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC1434_0_1433_next", OUT / "P8_Y5_R10_1433_NEXT_TARGET.csv", "NEXT1433_0_1434", "1433 handoff selecting local trace residual source-pack schema."),
        ("SRC1434_1_1433_validation", OUT / "P8_Y5_BRR545_1433_VALIDATION.csv", "VAL1433_7_overall", "1433 validation summary."),
        ("SRC1434_2_branch_id", BRANCH_ID_FILE, branch, "branch lock row."),
        ("SRC1434_3_residual_activation", RESIDUAL_ACTIVATION_FILE, "RESIDUAL_ACTIVE_NONCLAIM", "active local trace residual branch."),
        ("SRC1434_4_871_bound_candidates", OUT / "P8_Y5_R10_871_BOUND_SOURCE_CANDIDATES.csv", "SRC871_WEP_MICROSCOPE_FINAL", "bound source candidates for local tests."),
        ("SRC1434_5_871_projection_contract", OUT / "P8_Y5_R10_871_CT_PROJECTION_CONTRACT.csv", "PC871_2_clock_WEP", "missing c_T projection contracts."),
        ("SRC1434_6_871_bound_rows", OUT / "P8_Y5_R10_871_CT_BOUND_ROWS.csv", "CT871_WEP_MICROSCOPE_ETA_PROXY", "source-backed/nonclaim bound rows."),
        ("SRC1434_7_921_arena_map", OUT / "P8_Y5_R10_921_LOCAL_BOUND_ARENA_MAP.csv", "BAM921_9_R10", "local bound arena map."),
        ("SRC1434_8_C_parent_schema", BRANCH_ROOT / "coefficients" / "C_parent_import_schema.csv", "zero_certificate_status", "strict C_parent import schema."),
        ("SRC1434_9_product_guard", BRANCH_ROOT / "product" / "eta_product_convention.csv", "tau_eff=1 is forbidden", "branch-locked product convention guard."),
        ("SRC1434_10_measured_G_guard", BRANCH_ROOT / "guards" / "measured_G_guard.csv", "do not absorb Ti/Pt relative acceleration", "measured-G relative absorption guard."),
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


def residual_component_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "component_id": "LTRC1434_0_trace_scalar",
            "residual_component": "trace_scalar",
            "coefficient_symbol": "Q_T_over_m;Z_T;lambda_T",
            "physical_meaning": "finite-range scalar trace leakage after local quotient zero fails",
            "primary_arenas": "R10;PPN_gamma_beta;clock_redshift",
            "required_projection": "P_trace_to_alpha;P_trace_to_metric;P_trace_to_clock",
            "current_status": "ACTIVE_MISSING_PROJECTION_AND_COEFFICIENTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "component_id": "LTRC1434_1_coframe_pullback",
            "residual_component": "coframe_pullback",
            "coefficient_symbol": "C_T_metric",
            "physical_meaning": "trace dependence of local observed metric/coframe",
            "primary_arenas": "PPN_gamma_beta;clock_redshift;light_cone",
            "required_projection": "P_metric_response;gauge_fixing;source_normalization_split",
            "current_status": "ACTIVE_MISSING_METRIC_RESPONSE_OPERATOR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "component_id": "LTRC1434_2_boundary_hair",
            "residual_component": "boundary_hair",
            "coefficient_symbol": "B_T;B_TF;B_0i",
            "physical_meaning": "trace boundary/exact current leaks into compact local projection",
            "primary_arenas": "PPN_alpha1_alpha2_alpha3_xi;orbital",
            "required_projection": "P_loc_boundary;shear_vector_decomposition;boundary_nohair_source",
            "current_status": "ACTIVE_MISSING_BOUNDARY_PROJECTION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "component_id": "LTRC1434_3_marker_constant",
            "residual_component": "marker_constant",
            "coefficient_symbol": "theta_T;alpha_EM_T;mass_ratio_T",
            "physical_meaning": "species, clock, EM, binding, or material labels carry trace charge",
            "primary_arenas": "WEP_MICROSCOPE;clock_redshift;EM",
            "required_projection": "P_species_marker;P_clock_functional;P_EM_charge_normalization",
            "current_status": "ACTIVE_MISSING_NO_MARKER_THEOREM_OR_SOURCE_ROWS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "component_id": "LTRC1434_4_source_normalization",
            "residual_component": "source_normalization",
            "coefficient_symbol": "mu_T;C_T_source;G_eff_T",
            "physical_meaning": "trace leakage into measured source strength, G, or GM",
            "primary_arenas": "Newton_source_normalization;orbital_Gdot;R10_source_geometry",
            "required_projection": "P_GM;P_Gdot;P_source_worldtube",
            "current_status": "ACTIVE_MISSING_SOURCE_NORMALIZATION_MAP",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def arena_bound_map_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "arena_id": "ABM1434_0_R10",
            "arena": "R10_short_range_inverse_square",
            "observable": "alpha(lambda)",
            "bound_source_anchor": "CT871_R10_EOTWASH_2020_ALPHA1_38P6UM_ANCHOR;CT871_R10_EOTWASH_2007_ALPHA1_56UM_ANCHOR",
            "source_status": "ANCHOR_ONLY_NONCURVE",
            "required_projection": "alpha_T(lambda)=F[Q_T_over_m,Z_T,lambda_T,R_source,K_R10]",
            "missing_inputs": "full alpha(lambda) curve; lambda_T; Z_T; source geometry; projection normalization",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "arena_id": "ABM1434_1_WEP",
            "arena": "WEP_MICROSCOPE",
            "observable": "eta_Ti_Pt",
            "bound_source_anchor": "CT871_WEP_MICROSCOPE_ETA_PROXY;SRC871_WEP_MICROSCOPE_FINAL",
            "source_status": "NUMERIC_BOUND_SOURCE_AVAILABLE_PROXY_NONCLAIM",
            "required_projection": "eta_AB=P_WEP[C_parent,R_source,R_material,K_CMSM,eta_product_convention]",
            "missing_inputs": "C_parent numeric/zero; full material tensor; source worldtube; official K_CMSM; official sign convention",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "arena_id": "ABM1434_2_PPN",
            "arena": "PPN_radio_and_ephemerides",
            "observable": "gamma_minus_one;beta_minus_one;alpha1;alpha2;alpha3;xi",
            "bound_source_anchor": "CT871_PPN_CASSINI_GAMMA_SIGMA;CT871_PPN_INPOP20A_BETA_INTERVAL;BAM921_4_alpha1;BAM921_5_alpha2;BAM921_6_alpha3;BAM921_7_xi",
            "source_status": "BOUND_SOURCES_OR_LOCAL_LIMITS_AVAILABLE_NONCLAIM",
            "required_projection": "PPN_vector=P_PPN[C_T_metric,B_TF,B_0i,source_normalization]",
            "missing_inputs": "metric response operator; gauge fixing; boundary shear/vector projection; source normalization split",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "arena_id": "ABM1434_3_CLOCK",
            "arena": "clock_redshift",
            "observable": "redshift_fractional_deviation",
            "bound_source_anchor": "CT871_CLOCK_GALILEO_REDSHIFT_SIGMA;BAM921_1_clock",
            "source_status": "NUMERIC_BOUND_SOURCE_AVAILABLE_NONCLAIM",
            "required_projection": "delta_nu/nu=P_clock[theta_T,C_T_metric,clock_functional]",
            "missing_inputs": "clock functional; marker/constant-sector trace derivative; metric clock split",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "arena_id": "ABM1434_4_ORBITAL_NEWTON",
            "arena": "orbital_and_Newton_source_normalization",
            "observable": "Gdot_over_G;delta_GM;anomalous_radial_acceleration",
            "bound_source_anchor": "SRC871_ORBITAL_LLR_REVIEW;BAM921_8_Gdot",
            "source_status": "REVIEW_OR_LOCAL_BOUND_MAP_NONCLAIM",
            "required_projection": "delta_mu/mu=P_GM[C_T_source,G_eff_T,source_worldtube,time_dependence]",
            "missing_inputs": "selected numeric orbital observable; C_T_source; source-worldtube weighting; time/radial dependence law",
            "score_status": "NOT_SCOREABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def required_inputs_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "input_id": "REQ1434_0_C_parent",
            "required_input": "C_parent numeric/zero coupling vector",
            "current_path": str(BRANCH_ROOT / "coefficients" / "C_parent.csv"),
            "current_status": "PLACEHOLDER_REFUSAL_ONLY",
            "blocks": "all residual projections",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "input_id": "REQ1434_1_projection_matrices",
            "required_input": "P_R10;P_WEP;P_PPN;P_clock;P_orbital;P_GM",
            "current_path": str(BRANCH_ROOT / "residuals"),
            "current_status": "MISSING_PROJECTION_MATRICES",
            "blocks": "mapping residual components to observables",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "input_id": "REQ1434_2_MICROSCOPE_pack",
            "required_input": "R_source;R_material;K_CMSM;eta_product_convention;measured_G_guard",
            "current_path": str(BRANCH_ROOT),
            "current_status": "PRODUCT_AND_G_GUARDS_EXIST_OTHER_INPUTS_MISSING",
            "blocks": "WEP score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "input_id": "REQ1434_3_R10_curve",
            "required_input": "full alpha(lambda) bound curve and trace lambda_T/source projection",
            "current_path": str(OUT / "P8_Y5_R10_871_CT_BOUND_ROWS.csv"),
            "current_status": "ANCHORS_ONLY_FULL_CURVE_MISSING",
            "blocks": "R10 claim score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "input_id": "REQ1434_4_PPN_clock_orbital_sources",
            "required_input": "PPN, clock, orbital selected bounds plus residual response coefficients",
            "current_path": str(OUT / "P8_Y5_R10_871_BOUND_SOURCE_CANDIDATES.csv"),
            "current_status": "BOUND_SOURCES_STAGED_PROJECTIONS_MISSING",
            "blocks": "PPN/clock/orbital score",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def source_pack_schema_rows(branch: str) -> list[dict[str, Any]]:
    fields = [
        ("same_parent_branch_id", branch, "must match branch lock"),
        ("residual_component", "trace_scalar|coframe_pullback|boundary_hair|marker_constant|source_normalization", "component class"),
        ("coefficient_symbol", "Q_T_over_m|Z_T|lambda_T|C_T_metric|B_T|theta_T|mu_T", "coefficient slot"),
        ("value_or_bound", "numeric|DERIVED_ZERO|MISSING", "no claim if missing"),
        ("uncertainty", "numeric|exact|MISSING", "uncertainty or theorem exactness"),
        ("units", "SI_or_declared_natural_units", "dimension control"),
        ("projection_matrix_id", "P_R10|P_WEP|P_PPN|P_clock|P_orbital|P_GM", "observable map"),
        ("arena", "R10|WEP_MICROSCOPE|PPN|clock|orbital|Newton", "test arena"),
        ("source_path", "local path, URL, DOI, or theorem certificate", "provenance"),
        ("parent_status", "PARENT_DERIVED|SOURCE_BACKED|DERIVED_ZERO|CLOSURE_ONLY|MISSING", "promotion status"),
        ("valid_for_claim", "false until full arena row passes", "claim guard"),
        ("claim_allowed", "false until runner accepts", "claim guard"),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "schema_field": field,
            "required_value_or_policy": policy,
            "purpose": purpose,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for field, policy, purpose in fields
    ]


def write_manifest_files(schema: list[dict[str, Any]], arena_map: list[dict[str, Any]]) -> None:
    write_csv(RESIDUAL_SOURCE_PACK_SCHEMA_FILE, schema)
    write_csv(LOCAL_TRACE_BOUND_MAP_FILE, arena_map)


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN1434_0_residual_pack",
            "target": "local trace residual source-pack runner",
            "input_status": "SCHEMA_AND_BOUND_MAP_READY_SOURCE_ROWS_MISSING",
            "runner_status": "REFUSE_NUMERIC_SCORE",
            "score_ready": False,
            "reason": "component schema and bound map exist, but projection matrices and source-backed residual coefficients are missing",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1434_1_arena_bounds",
            "target": "R10/WEP/PPN/clock/orbital/Newton arena map",
            "input_status": "BOUND_SOURCES_STAGED_PROJECTIONS_MISSING",
            "runner_status": "WAIT_FOR_PROJECTION_ROWS",
            "score_ready": False,
            "reason": "bounds alone do not constrain MTS until residual-to-observable projections are derived or sourced",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1434_0_schema",
            "claim_component": "local trace residual source-pack schema",
            "gate_pass": True,
            "claim_allowed": False,
            "reason": "schema exists, but schema is not evidence",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1434_1_bound_map",
            "claim_component": "arena bound map",
            "gate_pass": True,
            "claim_allowed": False,
            "reason": "bound map exists, but projections and coefficients are missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1434_2_residual_score",
            "claim_component": "numeric local trace residual score",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "no source-backed residual rows or projection matrices",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1434_3_local_GR",
            "claim_component": "local-GR/Newton reduction",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "residual branch active; no theorem-zero or numeric pass",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1434_0_bound_map",
            "decision": "map active residuals to test arenas before scoring",
            "because": "bounds only matter after residual components have projection matrices",
            "effect": "future runner can identify exactly which missing input blocks each arena",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1434_1_no_score",
            "decision": "do not score residuals from bound sources alone",
            "because": "the MTS residual-to-observable map is still missing",
            "effect": "R10/WEP/PPN/clock/orbital rows remain nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1434_2_next",
            "decision": "build a dry-run residual runner and missing-input dashboard next",
            "because": "the schema is ready; the next value is executable refusal and gap reporting",
            "effect": "1435 should parse the schema/map and report blocked arenas without long computation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1434_0_1435",
            "next_target": "1435-Y5-R10-RAB-local-trace-residual-runner-dryrun-and-missing-input-dashboard.md",
            "script": "scripts/Y5_R10_RAB_local_trace_residual_runner_dryrun_and_missing_input_dashboard.py",
            "objective": "build a dry-run runner that parses the local trace residual source-pack schema and arena bound map, then reports every missing projection/source input while refusing numeric claims.",
            "include": "schema parser; bound-map parser; missing-input matrix; claim refusal; branch-id audit",
            "exclude": "long data run; numeric claim scoring; fitted coupling; local-GR claim; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    components: list[dict[str, Any]],
    arena_map: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        RESIDUAL_COMPONENTS,
        ARENA_BOUND_MAP,
        REQUIRED_INPUTS_LEDGER,
        SOURCE_PACK_SCHEMA,
        RUNNER_REFUSAL,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        RESIDUAL_SOURCE_PACK_SCHEMA_FILE,
        LOCAL_TRACE_BOUND_MAP_FILE,
    ]
    parse_ok = True
    parse_errors: list[str] = []
    truthy_claim_flags: list[str] = []
    missing_markers = 0
    for path in csvs:
        try:
            rows = read_csv(path)
        except Exception as exc:
            parse_ok = False
            parse_errors.append(f"{path.name}:{type(exc).__name__}")
            continue
        for index, row in enumerate(rows, start=2):
            row_text = " ".join(row.values())
            if "MISSING" in row_text or "NOT_SCOREABLE" in row_text:
                missing_markers += 1
            for key in ("claim_allowed", "valid_for_claim", "valid_prediction_row"):
                if (row.get(key) or "").strip().lower() == "true":
                    truthy_claim_flags.append(f"{path.name}:{index}:{key}=true")
    sources_ok = all(row["path_exists"] and row["anchor_found"] for row in sources)
    component_count_ok = len(components) == 5
    arena_count_ok = len(arena_map) == 5
    schema_written = RESIDUAL_SOURCE_PACK_SCHEMA_FILE.exists() and len(read_csv(RESIDUAL_SOURCE_PACK_SCHEMA_FILE)) == len(schema)
    bound_map_written = LOCAL_TRACE_BOUND_MAP_FILE.exists() and len(read_csv(LOCAL_TRACE_BOUND_MAP_FILE)) == len(arena_map)
    claims_safe = all(str(row.get("claim_allowed")).lower() == "false" for row in claims) and not truthy_claim_flags
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1434_0_sources", sources_ok, "all 1434 cited source paths and anchors resolve"),
        ("VAL1434_1_components", component_count_ok, "five local trace residual components mapped"),
        ("VAL1434_2_arena_map", arena_count_ok, "five arena bound-map rows written"),
        ("VAL1434_3_manifest_files", schema_written and bound_map_written, "branch-locked residual schema and bound map files written"),
        ("VAL1434_4_missing_inputs_visible", missing_markers > 0, "MISSING/NOT_SCOREABLE markers remain visible"),
        ("VAL1434_5_claim_gates", claims_safe, "all claim/valid/prediction flags remain false"),
        ("VAL1434_6_csv_parse", parse_ok, "all generated 1434 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1434_7_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1434_8_next_target", True, "1435 handoff written"),
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
            "check_id": "VAL1434_9_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1434 maps active local trace residual components to bound arenas as a nonclaim source-pack schema",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1434 - Local trace residual source-pack schema and bound map",
            "**Current verdict:** the local trace residual branch is source-pack ready, not score-ready. 1434 maps active residual components to R10, WEP, PPN, clocks, orbital, and Newton/source-normalization arenas without allowing a claim.",
            "**Main progress:** the branch now has a residual component table, arena bound map, required-input ledger, and local schema files under `source-intake/microscope/branch_locked_wep/residuals`.",
            "## Source register\n" + md_table(sections["sources"]),
            "## Residual components\n" + md_table(sections["components"]),
            "## Arena bound map\n" + md_table(sections["arena_map"]),
            "## Required inputs ledger\n" + md_table(sections["inputs"]),
            "## Source pack schema\n" + md_table(sections["schema"]),
            "## Runner refusal status\n" + md_table(sections["runner"]),
            "## Claim gates\n" + md_table(sections["claims"]),
            "## Decision ledger\n" + md_table(sections["decisions"]),
            "## Validation\n" + md_table(sections["validation"]),
            "## Next target\n" + md_table(sections["next"]),
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    branch = branch_id()
    sources = source_register_rows(branch)
    components = residual_component_rows(branch)
    arena_map = arena_bound_map_rows(branch)
    inputs = required_inputs_rows(branch)
    schema = source_pack_schema_rows(branch)
    write_manifest_files(schema, arena_map)
    runner = runner_refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(RESIDUAL_COMPONENTS, components)
    write_csv(ARENA_BOUND_MAP, arena_map)
    write_csv(REQUIRED_INPUTS_LEDGER, inputs)
    write_csv(SOURCE_PACK_SCHEMA, schema)
    write_csv(RUNNER_REFUSAL, runner)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)

    validation = validation_rows(sources, components, arena_map, schema, claims)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "components": components,
            "arena_map": arena_map,
            "inputs": inputs,
            "schema": schema,
            "runner": runner,
            "claims": claims,
            "decisions": decisions,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1434_local_trace_residual_source_pack_schema_bound_map_nonclaim")


if __name__ == "__main__":
    main()
