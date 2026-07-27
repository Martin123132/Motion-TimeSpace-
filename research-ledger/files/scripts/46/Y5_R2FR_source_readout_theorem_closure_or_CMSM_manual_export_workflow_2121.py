from __future__ import annotations

import json
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


DOC = ROOT / "2121-Y5-R2FR-source-readout-theorem-closure-or-CMSM-manual-export-workflow.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DROP_ROOT = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "drop-folder" / "1704"
DROP_LIVE = DROP_ROOT / "live"
DROP_TEMPLATES = DROP_ROOT / "templates"
WORKFLOW_DOC = DROP_ROOT / "CMSM_MANUAL_EXPORT_WORKFLOW_2121.md"
READOUT_SCHEMA = DROP_TEMPLATES / "P_WEP_K_CMSM_readout_SCHEMA_2121.csv"
MANIFEST_TEMPLATE = DROP_TEMPLATES / "P_WEP_tau_parser_manifest_TEMPLATE_2121.json"

CSV_2120_NEXT = OUT / "P8_Y5_PARENT_QLOC_2120_NEXT_TARGET.csv"
CSV_2120_VAL = OUT / "P8_Y5_BRR545_2120_VALIDATION.csv"
CSV_2120_REQ = OUT / "P8_Y5_PARENT_QLOC_2120_NUMERIC_KERNEL_REQUIREMENTS.csv"
CSV_2120_INV = OUT / "P8_Y5_PARENT_QLOC_2120_LOCAL_DATA_INVENTORY.csv"
CSV_2120_STATUS = OUT / "P8_Y5_PARENT_QLOC_2120_ACQUISITION_STATUS.csv"
CSV_1084_READOUT = OUT / "P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv"
CSV_2118_KERNELS = OUT / "P8_Y5_PARENT_QLOC_2118_EXPLICIT_EXCEPTION_KERNELS.csv"
CSV_2118_ZERO = OUT / "P8_Y5_PARENT_QLOC_2118_SOURCE_READOUT_ZERO_THEOREM_ATTEMPT.csv"
CSV_1963_ACTION = OUT / "P8_Y5_PARENT_QLOC_1963_MINIMAL_PARENT_ACTION_SIGNATURE.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed"}


def formalization_has_2121_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2121-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2121*",
        "*Y5_R2FR_source_readout_theorem_closure_or_CMSM_manual_export_workflow_2121*",
        "*AFRAME_CMSM_EXPORT_2121*",
        "*JR2121_CMSM*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2121_00_2120_next", CSV_2120_NEXT, ["NEXT2120_0_2121", "manual CMSM export workflow"], "2120 selects source/readout theorem closure or CMSM manual export workflow."),
        ("SRC2121_01_2120_validation", CSV_2120_VAL, ["VAL2120_OVERALL", "PASS"], "2120 validation passed."),
        ("SRC2121_02_2120_requirements", CSV_2120_REQ, ["REQ2120_7_tau_kernel_verdict", "BLOCKED_OFFICIAL_ARRAYS_AND_SOURCE_WORLDTUBE_MISSING"], "2120 numeric kernel requirements."),
        ("SRC2121_03_2120_inventory", CSV_2120_INV, ["INV2120_4_drop_live_readout", "MISSING_UNLESS_USER_EXPORTS"], "2120 local data inventory."),
        ("SRC2121_04_2120_status", CSV_2120_STATUS, ["STAT2120_3_tau", "TAU_WEP_BLOCKED"], "2120 acquisition status."),
        ("SRC2121_05_1084_readout", CSV_1084_READOUT, ["RIG1084_0_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"], "1084 readout import gate."),
        ("SRC2121_06_2118_kernels", CSV_2118_KERNELS, ["KSR2118_1_orbit_WEP_kernel", "KSR2118_7_total_no_cancellation"], "2118 source/readout kernel suite."),
        ("SRC2121_07_2118_zero", CSV_2118_ZERO, ["SRZ2118_6_verdict", "ZERO_THEOREM_NOT_CLOSED"], "2118 source/readout zero theorem status."),
        ("SRC2121_08_1963_action", CSV_1963_ACTION, ["ACT1963_5_no_independent_Gamma_clause", "NO_GAMMA_BY_VARIABLE_SIGNATURE"], "1963 owned-coframe candidate variable signature."),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, expected_needles="; ".join(needles), needles_found=exists and all(needle in text for needle in needles), role=role))
    return rows


def theorem_closure_rows() -> list[dict[str, object]]:
    return [
        row(
            theorem_id="THC2121_0_owned_readout_route",
            target="source/readout Gamma silence",
            candidate_statement="If source worldtube, clocks, light, orbit, boundary and projective readouts are functionals only of q/e_obs plus owned gauge data, independent Gamma/readout currents vanish by variable absence.",
            current_status="THEOREM_ROUTE_OPEN_NOT_SIGNED",
            blocker="2120 shows numeric data are absent; 2118 shows source/readout clauses are not parent-signed.",
            next_derivation_input="canonical source/readout functor in the owned-coframe parent branch",
            zero_ready=False,
        ),
        row(
            theorem_id="THC2121_1_empirical_route",
            target="tau_WEP and WEP source/readout kernel",
            candidate_statement="If CMSM arrays and source-worldtube files are supplied, tau_WEP can be validated as an empirical projection kernel, not as a theorem.",
            current_status="MANUAL_EXPORT_REQUIRED",
            blocker="official arrays and source worldtube missing locally",
            next_derivation_input="none; this is an empirical acquisition route",
            zero_ready=False,
        ),
        row(
            theorem_id="THC2121_2_verdict",
            target="2121 fork",
            candidate_statement="Derivation route and data route must remain separate: theorem closure can claim zeros, data import can only run nonclaim projections.",
            current_status="FORK_SEPARATED",
            blocker="neither route is complete yet",
            next_derivation_input="source/readout owner lemma or CMSM live exports",
            zero_ready=False,
        ),
    ]


def required_artifact_rows() -> list[dict[str, object]]:
    artifacts = [
        (
            "CMSM2121_0_readout",
            "P_WEP_K_CMSM_readout.csv",
            "official CMSM readout arrays",
            "same_parent_branch_id;session_id;segment_id;time_s;sample_index;gx;gz;Sxx;Sxz;mask_flag;calibration_flag;frame;axis_sign;units;source_path;valid_for_claim;claim_allowed",
            "gx/gz finite m s^-2; Sxx/Sxz finite s^-2; masks boolean; no template/surrogate rows",
        ),
        (
            "CMSM2121_1_source",
            "P_WEP_R_source_Earth_worldtube.csv",
            "Earth/source worldtube or source-profile weighting",
            "same_parent_branch_id;source_model_id;profile_coordinate;density_or_weight;composition_basis_id;frame;units;source_path;valid_for_claim;claim_allowed",
            "source profile or theorem-reduced point-source convention; finite-source support and frame units",
        ),
        (
            "CMSM2121_2_material",
            "P_WEP_TiPt_material_response_tensor.csv",
            "TA6V/PtRh10 material response tensor",
            "same_parent_branch_id;test_body;material;parent_basis_id;response_value;response_units;source_path;valid_for_claim;claim_allowed",
            "same parent basis as source and C_parent; no proxy-only tensor promoted",
        ),
        (
            "CMSM2121_3_eta",
            "P_WEP_eta_product_convention.csv",
            "reported eta convention and normalization",
            "same_parent_branch_id;eta_definition;axis_sign;absolute_value_rule;orbit_average_rule;normalization;units;source_path;valid_for_claim;claim_allowed",
            "maps acceleration/readout product into dimensionless eta_AB without fitted-G absorption",
        ),
        (
            "CMSM2121_4_branch_lock",
            "P_WEP_same_parent_branch_lock.csv",
            "same-parent branch guard",
            "same_parent_branch_id;artifact_name;artifact_hash;branch_role;source_path;valid_for_claim;claim_allowed",
            "ties source, material, readout, convention, parent coefficient and bound comparator to one branch",
        ),
        (
            "CMSM2121_5_parent",
            "P_WEP_C_parent_or_zero_certificate.csv",
            "finite same-branch parent coefficient or zero certificate",
            "same_parent_branch_id;coefficient_id;coefficient_value;coefficient_units;zero_certificate;derivation_path;source_path;valid_for_claim;claim_allowed",
            "must be parent-signed or explicitly nonclaim; no fitted residual values",
        ),
        (
            "CMSM2121_6_tau_min",
            "P_WEP_tau_min_lower_bound.csv",
            "strict tau nondegeneracy lower bound",
            "same_parent_branch_id;tau_min;units;derivation_or_data_method;source_path;valid_for_claim;claim_allowed",
            "strictly positive abs(tau_WEP)>=tau_min>0, not tau=1 shortcut",
        ),
        (
            "CMSM2121_7_manifest",
            "P_WEP_tau_parser_manifest.json",
            "parser manifest",
            "same_parent_branch_id;artifacts;hashes;schemas;units;sign_conventions;license;citations;no_shortcut_assertions",
            "machine-readable manifest for validation before any runner import",
        ),
    ]
    rows: list[dict[str, object]] = []
    for artifact_id, filename, role, required_columns, acceptance_rule in artifacts:
        live_path = DROP_LIVE / filename
        rows.append(
            row(
                artifact_id=artifact_id,
                filename=filename,
                role=role,
                live_path=str(live_path),
                live_exists=live_path.exists(),
                required_columns=required_columns,
                acceptance_rule=acceptance_rule,
                usable_now=False,
            )
        )
    return rows


def validation_rule_rows() -> list[dict[str, object]]:
    return [
        row(rule_id="VR2121_0_exact_names", rule="live files must use exact expected filenames", failure_mode="wrong or renamed files are ignored", severity="hard_fail"),
        row(rule_id="VR2121_1_no_placeholders", rule="reject MISSING/PENDING/FILL_ME/template/surrogate/nonclaim placeholders in live evidence rows", failure_mode="prevents template rows being treated as data", severity="hard_fail"),
        row(rule_id="VR2121_2_numeric_finite", rule="gx,gz,Sxx,Sxz,tau_min and coefficient numeric fields must be finite with declared units", failure_mode="blocks malformed numeric kernels", severity="hard_fail"),
        row(rule_id="VR2121_3_flags_false", rule="valid_for_claim=false and claim_allowed=false during import", failure_mode="keeps manual export private/nonclaim until a later validator promotes a complete set", severity="hard_fail"),
        row(rule_id="VR2121_4_same_branch", rule="same_parent_branch_id must match across all live artifacts", failure_mode="prevents mixing source/readout/material rows from different branches", severity="hard_fail"),
        row(rule_id="VR2121_5_hash_manifest", rule="manifest must list source paths, hashes, schemas, units and sign conventions", failure_mode="blocks unverifiable copied files", severity="hard_fail"),
        row(rule_id="VR2121_6_no_tau_shortcut", rule="tau_WEP cannot be set to 1 or assumed nonzero without data or theorem", failure_mode="prevents fake WEP projection pass", severity="hard_fail"),
        row(rule_id="VR2121_7_no_bound_prediction", rule="MICROSCOPE eta bound cannot be treated as an MTS prediction", failure_mode="bound anchor remains comparator only", severity="hard_fail"),
    ]


def write_workflow_templates(artifacts: list[dict[str, object]], rules: list[dict[str, object]]) -> list[dict[str, object]]:
    DROP_TEMPLATES.mkdir(parents=True, exist_ok=True)
    DROP_LIVE.mkdir(parents=True, exist_ok=True)
    readout_schema = [
        {
            "column_name": name,
            "required": True,
            "expected_type": expected_type,
            "notes": notes,
            "valid_for_claim": False,
        }
        for name, expected_type, notes in [
            ("same_parent_branch_id", "string", "must match every other WEP live artifact"),
            ("session_id", "string", "CMSM/MICROSCOPE session or run id"),
            ("segment_id", "string", "e.g. SUEP segment number where available"),
            ("time_s", "float", "seconds in declared frame/convention"),
            ("sample_index", "integer", "monotonic within session/segment"),
            ("gx", "float", "official source-gravity/readout basis, m s^-2"),
            ("gz", "float", "official source-gravity/readout basis, m s^-2"),
            ("Sxx", "float", "official gradient/inertia basis, s^-2"),
            ("Sxz", "float", "official gradient/inertia basis, s^-2"),
            ("mask_flag", "boolean", "true if masked/excluded"),
            ("calibration_flag", "string", "calibration or correction status"),
            ("frame", "string", "instrument/source frame convention"),
            ("axis_sign", "string", "sensitive-axis sign convention"),
            ("units", "string", "must declare gx/gz and Sxx/Sxz units"),
            ("source_path", "string", "CMSM/export/source path"),
            ("valid_for_claim", "boolean", "must remain false at import"),
            ("claim_allowed", "boolean", "must remain false at import"),
        ]
    ]
    write_csv(READOUT_SCHEMA, readout_schema)
    manifest = {
        "same_parent_branch_id": "FILL_FROM_EXPORT_BUT_KEEP_NONCLAIM",
        "artifacts": [item["filename"] for item in artifacts],
        "hashes": {},
        "schemas": {"P_WEP_K_CMSM_readout.csv": str(READOUT_SCHEMA)},
        "units": {},
        "sign_conventions": {},
        "license": "FILL_OFFICIAL_CMSM_LICENSE_OR_ACCESS_NOTE",
        "citations": ["https://microscope.onera.fr/fr/publication/microscope-data-are-available"],
        "no_shortcut_assertions": [
            "no templates as evidence",
            "no surrogate arrays as official CMSM arrays",
            "no tau_WEP=1 shortcut",
            "no MICROSCOPE bound as MTS prediction",
            "valid_for_claim=false at import",
            "claim_allowed=false at import",
        ],
    }
    MANIFEST_TEMPLATE.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    workflow = "\n".join(
        [
            "# CMSM Manual Export Workflow - 2121",
            "",
            "Drop official MICROSCOPE/CMSM exports only into the `live` folder. Templates and surrogates are never evidence.",
            "",
            "## Required Live Files",
            *[f"- `{item['filename']}` — {item['role']}" for item in artifacts],
            "",
            "## Import Rules",
            *[f"- `{item['rule_id']}`: {item['rule']}" for item in rules],
            "",
            "## Current Status",
            "No live official readout file is present at this checkpoint. Keep all claim flags false.",
            "",
        ]
    )
    WORKFLOW_DOC.write_text(workflow, encoding="utf-8")
    outputs = [
        ("OUT2121_0_workflow_doc", WORKFLOW_DOC, "manual CMSM export workflow"),
        ("OUT2121_1_readout_schema", READOUT_SCHEMA, "strict readout schema"),
        ("OUT2121_2_manifest_template", MANIFEST_TEMPLATE, "parser manifest template"),
    ]
    return [
        row(output_id=output_id, path=str(path), role=role, path_exists=path.exists(), size_bytes=path.stat().st_size if path.exists() else 0, parse_ok=csv_rows_parse(path) if path.suffix.lower() == ".csv" else True)
        for output_id, path, role in outputs
    ]


def import_status_rows(artifacts: list[dict[str, object]]) -> list[dict[str, object]]:
    live_count = sum(1 for item in artifacts if truthy(item["live_exists"]))
    all_live = live_count == len(artifacts)
    return [
        row(status_id="IMP2121_0_live_files", status="LIVE_SET_INCOMPLETE", detail=f"{live_count} of {len(artifacts)} required live artifacts present", import_ready=all_live),
        row(status_id="IMP2121_1_readout", status="READOUT_MISSING", detail="P_WEP_K_CMSM_readout.csv is not present in live folder", import_ready=False),
        row(status_id="IMP2121_2_tau", status="TAU_WEP_NOT_RUNNABLE", detail="manual export workflow exists, but numeric tau remains blocked until live files validate", import_ready=False),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        row(gate_id="GATE2121_0_workflow_written", gate="manual CMSM workflow exists", gate_pass=True, rationale="workflow doc, readout schema and manifest template are generated"),
        row(gate_id="GATE2121_1_live_data_present", gate="complete live CMSM/export set present", gate_pass=False, rationale="required live files are absent"),
        row(gate_id="GATE2121_2_import_ready", gate="import validator may score tau_WEP", gate_pass=False, rationale="workflow is ready but data are not present"),
        row(gate_id="GATE2121_3_theorem_closed", gate="source/readout theorem closure achieved", gate_pass=False, rationale="owned-coframe source/readout functor remains unsigned"),
        row(gate_id="GATE2121_4_claim_allowed", gate="WEP/local-GR claim allowed", gate_pass=False, rationale="this checkpoint is workflow-only and theorem route is unclosed"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2121_0", decision="MANUAL_EXPORT_WORKFLOW_READY", because="the live artifact names, required columns, manifest and no-shortcut rules are now explicit.", next_action="if the user can export CMSM files, drop them into the live folder unchanged."),
        row(decision_id="DEC2121_1", decision="THEOREM_ROUTE_STILL_OPEN", because="data import can test a projection but cannot prove source/readout ownership.", next_action="continue deriving source/readout as owned-coframe functionals in parallel."),
        row(decision_id="DEC2121_2", decision="NO_CLAIM", because="no live official arrays and no source/readout theorem closure exist.", next_action="write a validator next, or keep deriving if no export is available."),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2121_0_2122",
            next_target="2122-Y5-R2FR-CMSM-live-drop-validator-or-source-readout-owner-lemma.md",
            script="scripts/Y5_R2FR_CMSM_live_drop_validator_or_source_readout_owner_lemma_2122.py",
            objective="Implement a strict validator for the CMSM live drop folder if files are present; otherwise continue the source/readout owner lemma route and try to theorem-zero the source/readout kernels without data.",
            forbidden_shortcuts="reading templates as data; accepting surrogate arrays; allowing tau=1; allowing claim flags true; fitted-G absorption; cancellation; local-GR/Newton/PPN claim; formalization-workbench edits; GitHub action",
        )
    ]


def write_branch_copies(artifacts: list[dict[str, object]], rules: list[dict[str, object]], status_rows: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2121_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_CMSM_EXPORT_2121_NONCLAIM.csv", artifacts + rules + status_rows),
        ("COPY2121_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2121_CMSM_EXPORT_WORKFLOW_NONCLAIM.csv", artifacts + rules + status_rows),
        ("COPY2121_2_acquisition_queue", QUEUE / "JR2121_CMSM_EXPORT_OR_SOURCE_READOUT_LEMMA_QUEUE.csv", next_rows + artifacts),
    ]
    result: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        result.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return result


def validation_rows(
    sources: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    artifacts: list[dict[str, object]],
    rules: list[dict[str, object]],
    outputs: list[dict[str, object]],
    status_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    theorem_ok = any(item["theorem_id"] == "THC2121_2_verdict" and item["current_status"] == "FORK_SEPARATED" for item in theorem_rows)
    artifacts_ok = len(artifacts) == 8 and all(not truthy(item["usable_now"]) for item in artifacts)
    rules_ok = len(rules) >= 8 and any(item["rule_id"] == "VR2121_6_no_tau_shortcut" for item in rules)
    outputs_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in outputs)
    status_ok = any(item["status_id"] == "IMP2121_2_tau" and item["status"] == "TAU_WEP_NOT_RUNNABLE" for item in status_rows)
    gates_ok = any(item["gate_id"] == "GATE2121_0_workflow_written" and truthy(item["gate_pass"]) for item in gates) and any(item["gate_id"] == "GATE2121_2_import_ready" and not truthy(item["gate_pass"]) for item in gates)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, theorem_rows, artifacts, rules, outputs, status_rows, gates, decisions, next_rows, copies)
        for item in group
    )
    branch_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2121_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    next_ok = any(item["route_id"] == "NEXT2121_0_2122" for item in next_rows)
    all_ok = all([sources_ok, theorem_ok, artifacts_ok, rules_ok, outputs_ok, status_ok, gates_ok, no_claim_flags, branch_ok, csv_ok, formalization_clean, pycache_clean, next_ok])
    checks = [
        ("VAL2121_00_sources", sources_ok, "all cited 2120/source-readout files exist and contain expected needles"),
        ("VAL2121_01_theorem_fork", theorem_ok, "theorem/data fork is explicitly separated"),
        ("VAL2121_02_artifacts", artifacts_ok, "eight required live artifacts are listed and non-usable now"),
        ("VAL2121_03_rules", rules_ok, "strict import/no-shortcut rules are written"),
        ("VAL2121_04_outputs", outputs_ok, "workflow doc, readout schema and manifest template exist"),
        ("VAL2121_05_status", status_ok, "tau_WEP remains not runnable"),
        ("VAL2121_06_claim_gates", gates_ok, "workflow gate passes but import/theorem/claim gates fail"),
        ("VAL2121_07_no_claim_flags", no_claim_flags, "no generated row allows a claim or score"),
        ("VAL2121_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2121_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2121_10_formalization_clean", formalization_clean, "formalization-workbench untouched by 2121"),
        ("VAL2121_11_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2121_12_next", next_ok, "next target selects live-drop validator or source/readout owner lemma"),
        ("VAL2121_OVERALL", all_ok, "2121 writes the CMSM manual export/import workflow, keeps tau_WEP blocked, and preserves the derivation route."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    artifacts: list[dict[str, object]],
    rules: list[dict[str, object]],
    outputs: list[dict[str, object]],
    status_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2121 - Y5/R2FR Source-Readout Theorem Closure Or CMSM Manual Export Workflow",
            "## Current Verdict",
            "2121 separates the fork properly. The derivation route remains: prove source/readout objects are owned-coframe functionals, which would zero their independent Gamma currents. The data route is now operationally precise: if official CMSM exports are obtained manually, they have exact live filenames, strict columns, a manifest template and no-claim validation rules.",
            "No live official CMSM readout arrays are present yet, so `tau_WEP` remains not runnable. This checkpoint is still useful because it prevents the common failure mode: treating portal pointers, templates or surrogate arrays as empirical evidence.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Theorem/Data Fork",
            md_table(theorem_rows, ["theorem_id", "target", "current_status", "candidate_statement", "blocker", "next_derivation_input", "zero_ready", "valid_for_claim"]),
            "## Required Live Artifacts",
            md_table(artifacts, ["artifact_id", "filename", "role", "live_path", "live_exists", "acceptance_rule", "usable_now", "valid_for_claim"]),
            "## Import Validation Rules",
            md_table(rules, ["rule_id", "rule", "failure_mode", "severity", "valid_for_claim"]),
            "## Workflow Outputs",
            md_table(outputs, ["output_id", "path", "role", "path_exists", "size_bytes", "parse_ok", "valid_for_claim"]),
            "## Import Status",
            md_table(status_rows, ["status_id", "status", "detail", "import_ready", "valid_for_claim"]),
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
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    theorem_rows = theorem_closure_rows()
    artifacts = required_artifact_rows()
    rules = validation_rule_rows()
    outputs = write_workflow_templates(artifacts, rules)
    status_rows = import_status_rows(artifacts)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2121_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2121_THEOREM_DATA_FORK.csv",
        "artifacts": OUT / "P8_Y5_PARENT_QLOC_2121_REQUIRED_LIVE_ARTIFACTS.csv",
        "rules": OUT / "P8_Y5_PARENT_QLOC_2121_IMPORT_VALIDATION_RULES.csv",
        "outputs": OUT / "P8_Y5_PARENT_QLOC_2121_WORKFLOW_OUTPUTS.csv",
        "status": OUT / "P8_Y5_PARENT_QLOC_2121_IMPORT_STATUS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2121_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2121_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2121_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2121_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2121_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["theorem"], theorem_rows)
    write_csv(paths["artifacts"], artifacts)
    write_csv(paths["rules"], rules)
    write_csv(paths["outputs"], outputs)
    write_csv(paths["status"], status_rows)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(artifacts, rules, status_rows, next_rows)
    write_csv(paths["branch"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies] + [READOUT_SCHEMA]
    validation = validation_rows(sources, theorem_rows, artifacts, rules, outputs, status_rows, gates, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, theorem_rows, artifacts, rules, outputs, status_rows, gates, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
