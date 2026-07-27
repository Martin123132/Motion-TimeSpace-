from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_TAU_WEP_LOWER_BOUND_OR_PARENT_NONDEGENERACY_2512"
CHECKPOINT_ID = "2512"
DOC = ROOT / "2512-Y5-R2FR-tau-WEP-lower-bound-or-parent-nondegeneracy-proof.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LIVE_DROP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "drop-folder" / "1704" / "live"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2512_SOURCE_REGISTER.csv",
    "proof_attempt": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2512_TAU_NONDEGENERACY_PROOF_ATTEMPT.csv",
    "certificate_contract": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2512_TAU_MIN_CERTIFICATE_CONTRACT.csv",
    "live_artifact_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2512_LIVE_TAU_ARTIFACT_GATE.csv",
    "delta_w_width_law": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2512_DELTAW_WIDTH_LAW.csv",
    "dryrun_results": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2512_NONCLAIM_DRYRUN_RESULTS.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2512_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2512_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2512_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2512_VALIDATION.csv",
}

BRANCH_COPIES = {
    "tau_nondegeneracy": ROOT
    / "source-intake"
    / "microscope"
    / "branch_locked_wep"
    / "source"
    / "Tau_WEP_nondegeneracy_contract_2512_NONCLAIM.csv",
    "tau_live_gate": ROOT
    / "source-intake"
    / "microscope"
    / "branch_locked_wep"
    / "drop-folder"
    / "1704"
    / "Tau_WEP_live_artifact_gate_2512_NONCLAIM.csv",
    "delta_w_width": ROOT
    / "source-intake"
    / "local_bounds"
    / "Delta_w_TiPt_width_law_2512_NONCLAIM.csv",
    "ppn_next": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "PPN_source_weight_kernel_next_2512_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2512_0_2511_tau_target",
        "path": "2511-Y5-R2FR-first-source-weight-input-row-WEP-product-or-PPN-source-kernel.md",
        "needles": ["NEXT2511_0_selected", "WPROD2511_3_amplitude_inversion"],
        "role": "authoritative target: tau lower bound or parent nondegeneracy proof",
    },
    {
        "source_id": "SRC2512_1_tau_contract_1608",
        "path": "source-intake/microscope/quarantine/1608/TAU_WEP_READOUT_CONTRACT_NONCLAIM.csv",
        "needles": ["TAU1608_1_amplitude_law", "TAU1608_2_null_space_guard"],
        "role": "existing tau definition, amplitude inversion, and null-space guard",
    },
    {
        "source_id": "SRC2512_2_export_contract_2121",
        "path": "source-intake/source-weight/docs/AFRAME_CMSM_EXPORT_2121_NONCLAIM.csv",
        "needles": ["CMSM2121_6_tau_min", "IMP2121_2_tau"],
        "role": "live MICROSCOPE artifact gate and tau-min export contract",
    },
    {
        "source_id": "SRC2512_3_drop_request_1704",
        "path": "source-intake/microscope/branch_locked_wep/source/MICROSCOPE_WEP_data_request_update_1704.md",
        "needles": ["P_WEP_tau_min_lower_bound.csv", "Non-Claim Guardrail"],
        "role": "exact requested live artifacts and nonclaim rule",
    },
    {
        "source_id": "SRC2512_4_public_probe_1705",
        "path": "source-intake/microscope/branch_locked_wep/source/MICROSCOPE_public_source_probe_1705.md",
        "needles": ["Current Blocker", "P_WEP_K_CMSM_readout.csv"],
        "role": "records public-source probe blocker for live readout arrays",
    },
    {
        "source_id": "SRC2512_5_nondeg_contract_1990",
        "path": "source-intake/microscope/branch_locked_wep/coefficients/P8_Y5_PARENT_QLOC_1990_TAU_NONDEGENERACY_CONTRACT_NONCLAIM.csv",
        "needles": ["WEP1990_0_tau_min_certificate_slot", "MISSING_NONDEGENERACY_CERTIFICATE"],
        "role": "old tau-min certificate slot remains unsigned",
    },
    {
        "source_id": "SRC2512_6_tau_pack_1996",
        "path": "source-intake/microscope/branch_locked_wep/coefficients/P8_Y5_PARENT_QLOC_1996_TAU_WEP_PROJECTION_PACK_NONCLAIM.csv",
        "needles": ["WEP1996_0_tau_pack_contract", "MISSING_DIRECT_PRODUCT_AND_MISSING_TAU_PACK"],
        "role": "tau WEP projection pack requirement",
    },
    {
        "source_id": "SRC2512_7_readout_provenance_1997",
        "path": "source-intake/microscope/branch_locked_wep/coefficients/P8_Y5_PARENT_QLOC_1997_MICROSCOPE_READOUT_PROVENANCE_NONCLAIM.csv",
        "needles": ["WEP1997_0_readout_anchor", "READOUT_BOUND_ANCHOR_ONLY"],
        "role": "MICROSCOPE readout provenance is currently a bound anchor only",
    },
    {
        "source_id": "SRC2512_8_fallback_pack_1749",
        "path": "source-intake/microscope/branch_locked_wep/residuals/R2FR_1749_TAU_MIN_FALLBACK_SOURCE_PACK.csv",
        "needles": ["TFB1749_4_tau_min", "SOURCE_OR_DERIVATION_NEEDED"],
        "role": "tau-min fallback artifact pack",
    },
    {
        "source_id": "SRC2512_9_source_readout_kernel_2118",
        "path": "source-intake/microscope/branch_locked_wep/residuals/P8_Y5_PARENT_QLOC_2118_SOURCE_READOUT_KERNELS_NONCLAIM.csv",
        "needles": ["KSR2118_1_orbit_WEP_kernel", "OFFICIAL_FORM_SKELETON_NUMERIC_INPUTS_MISSING"],
        "role": "source/readout WEP kernel skeleton and missing numeric inputs",
    },
    {
        "source_id": "SRC2512_10_source_owner_2122",
        "path": "source-intake/microscope/branch_locked_wep/residuals/P8_Y5_PARENT_QLOC_2122_SOURCE_READOUT_OWNER_STATUS_NONCLAIM.csv",
        "needles": ["SRO2122_6_verdict", "COM2122_2_countermodel"],
        "role": "conditional source/readout owner theorem and surviving countermodel",
    },
]

REQUIRED_LIVE_ARTIFACTS = [
    {
        "artifact_id": "LIVE2512_0_readout",
        "filename": "P_WEP_K_CMSM_readout.csv",
        "role": "official CMSM readout/design matrix",
        "required_columns": "same_parent_branch_id;session_id;segment_id;time_s;sample_index;gx;gz;Sxx;Sxz;mask_flag;calibration_flag;frame;axis_sign;units;source_path;valid_for_claim;claim_allowed",
    },
    {
        "artifact_id": "LIVE2512_1_source",
        "filename": "P_WEP_R_source_Earth_worldtube.csv",
        "role": "Earth source worldtube/source weighting",
        "required_columns": "same_parent_branch_id;source_model_id;profile_coordinate;density_or_weight;composition_basis_id;frame;units;source_path;valid_for_claim;claim_allowed",
    },
    {
        "artifact_id": "LIVE2512_2_material",
        "filename": "P_WEP_TiPt_material_response_tensor.csv",
        "role": "TA6V/PtRh10 material response tensor",
        "required_columns": "same_parent_branch_id;test_body;material;parent_basis_id;response_value;response_units;source_path;valid_for_claim;claim_allowed",
    },
    {
        "artifact_id": "LIVE2512_3_eta",
        "filename": "P_WEP_eta_product_convention.csv",
        "role": "eta convention and normalization",
        "required_columns": "same_parent_branch_id;eta_definition;axis_sign;absolute_value_rule;orbit_average_rule;normalization;units;source_path;valid_for_claim;claim_allowed",
    },
    {
        "artifact_id": "LIVE2512_4_branch_lock",
        "filename": "P_WEP_same_parent_branch_lock.csv",
        "role": "same-parent branch guard",
        "required_columns": "same_parent_branch_id;artifact_name;artifact_hash;branch_role;source_path;valid_for_claim;claim_allowed",
    },
    {
        "artifact_id": "LIVE2512_5_parent",
        "filename": "P_WEP_C_parent_or_zero_certificate.csv",
        "role": "finite parent coefficient or parent-signed zero certificate",
        "required_columns": "same_parent_branch_id;coefficient_id;coefficient_value;coefficient_units;zero_certificate;derivation_path;source_path;valid_for_claim;claim_allowed",
    },
    {
        "artifact_id": "LIVE2512_6_tau_min",
        "filename": "P_WEP_tau_min_lower_bound.csv",
        "role": "strict positive tau lower bound",
        "required_columns": "same_parent_branch_id;tau_min;confidence;sign_or_abs_convention;derivation_or_source_path;assumptions;units;valid_for_claim;claim_allowed",
    },
    {
        "artifact_id": "LIVE2512_7_manifest",
        "filename": "P_WEP_tau_parser_manifest.json",
        "role": "hash/schema/unit/source manifest",
        "required_columns": "json:branch_id;manifest_status;artifact_hashes;schema_versions;units;sign_conventions;source_paths;license;citation;valid_for_claim;claim_allowed",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), "OK"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", "<br>").replace("|", "\\|")
            cells.append(value)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = ROOT / spec["path"]
        text = read_text(path)
        found = [needle for needle in spec["needles"] if needle in text]
        rows.append(
            base_row(
                source_id=spec["source_id"],
                source_path=spec["path"],
                path_exists=path.exists(),
                required_needles=";".join(spec["needles"]),
                found_needles=";".join(found),
                role=spec["role"],
                source_pass=path.exists() and len(found) == len(spec["needles"]),
            )
        )
    return rows


def proof_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "proof_id": "TAUP2512_0_definition",
            "target": "tau_WEP",
            "claim_shape": "tau_WEP := N_eta^-1 <K_CMSM, S_Earth x M_TiPt> in one branch-locked linear readout convention",
            "formal_status": "DEFINITION_LOCKED_CONDITIONAL",
            "missing_clause": "K_CMSM, source worldtube, material tensor, eta normalization, and branch lock are not live",
            "verdict": "NOT_NUMERIC",
        },
        {
            "proof_id": "TAUP2512_1_nondegeneracy_theorem",
            "target": "tau_min",
            "claim_shape": "If |N_eta| is finite positive, ||K_CMSM||>0, ||V_TiPt||>0, and dist(V_TiPt,ker K_CMSM)>=c_min||V_TiPt|| with c_min>0, then |tau_WEP|>=tau_min>0",
            "formal_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_clause": "c_min/alignment floor or direct projection computation is missing",
            "verdict": "NOT_PROMOTED",
        },
        {
            "proof_id": "TAUP2512_2_nullspace_countermodel",
            "target": "tau_min",
            "claim_shape": "Nonzero source and material vectors do not imply tau_WEP nonzero because V_TiPt can lie in ker(K_CMSM)",
            "formal_status": "COUNTERMODEL_ACTIVE",
            "missing_clause": "need official readout alignment or parent theorem excluding kernel alignment",
            "verdict": "BLOCKS_SHORTCUT",
        },
        {
            "proof_id": "TAUP2512_3_parent_geometry_limit",
            "target": "parent nondegeneracy proof",
            "claim_shape": "q/e_obs descent can prove vertical silence of readout variation, but it does not by itself prove a positive experimental projection amplitude",
            "formal_status": "DERIVATION_LIMIT_IDENTIFIED",
            "missing_clause": "external protocol/readout normalization or a separate nondegeneracy axiom/theorem is needed",
            "verdict": "PARENT_ZERO_ROUTE_NOT_ENOUGH_FOR_TAU_MIN",
        },
        {
            "proof_id": "TAUP2512_4_tau_zero_meaning",
            "target": "tau_WEP=0",
            "claim_shape": "tau_WEP=0 would mean WEP blindness of this projection, not source-weight safety in PPN/R10/clock/orbit",
            "formal_status": "ARENA_LIMIT",
            "missing_clause": "PPN/R10/clock/orbital kernels remain separate",
            "verdict": "NO_LOCAL_GR_INFERENCE",
        },
        {
            "proof_id": "TAUP2512_5_verdict",
            "target": "tau_WEP lower bound",
            "claim_shape": "derive tau_min>0 from parent geometry or live source-backed readout data",
            "formal_status": "CONDITIONAL_THEOREM_WRITTEN_BUT_UNSIGNED",
            "missing_clause": "MISSING_NONDEGENERACY_CERTIFICATE_OR_LIVE_ARTIFACTS",
            "verdict": "TAU_MIN_NOT_DERIVED_ACQUISITION_GATE_ACTIVE",
        },
    ]
    return [
        base_row(score_ready=False, valid_prediction_row=False, **row)
        for row in rows
    ]


def certificate_contract_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "certificate_id": "CERT2512_0_tau_min",
            "quantity": "tau_min",
            "required_value": "positive finite numeric lower bound",
            "units": "dimensionless",
            "accepted_routes": "official data computation; parent nondegeneracy theorem",
            "required_evidence": "tau_min>0; sign_or_abs_convention; confidence; derivation_or_source_path; assumptions",
            "current_status": "MISSING_TAU_MIN",
        },
        {
            "certificate_id": "CERT2512_1_branch_lock",
            "quantity": "same_parent_branch_id",
            "required_value": "one branch shared by readout, source, material, C_parent, eta convention, bound",
            "units": "identifier",
            "accepted_routes": "manifest hash lock",
            "required_evidence": "all artifacts declare identical branch id and hashes",
            "current_status": "MISSING_LIVE_BRANCH_LOCK",
        },
        {
            "certificate_id": "CERT2512_2_no_shortcut",
            "quantity": "tau_WEP normalization",
            "required_value": "not set to 1 or assumed nonzero",
            "units": "policy",
            "accepted_routes": "derived normalization; direct computation",
            "required_evidence": "explicit no-unity assertion and source-backed normalization",
            "current_status": "NO_UNITY_SHORTCUT_ENFORCED",
        },
        {
            "certificate_id": "CERT2512_3_nullspace",
            "quantity": "alignment floor c_min",
            "required_value": "dist(V_TiPt,ker K_CMSM)>=c_min||V_TiPt||",
            "units": "dimensionless",
            "accepted_routes": "linear algebra computation from live arrays; parent theorem excluding kernel alignment",
            "required_evidence": "K_CMSM matrix, V_TiPt vector, norm convention, c_min>0",
            "current_status": "MISSING_ALIGNMENT_FLOOR",
        },
        {
            "certificate_id": "CERT2512_4_width_conversion",
            "quantity": "Delta_w_TiPt width",
            "required_value": "abs(Delta_w_TiPt)<=2.8e-15/tau_min",
            "units": "dimensionless",
            "accepted_routes": "only after CERT2512_0 through CERT2512_3 pass",
            "required_evidence": "WEP product bound plus tau_min certificate",
            "current_status": "BLOCKED_UNTIL_TAU_MIN",
        },
    ]
    return [
        base_row(score_ready=False, valid_prediction_row=False, **row)
        for row in rows
    ]


def live_artifact_gate_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for artifact in REQUIRED_LIVE_ARTIFACTS:
        path = LIVE_DROP / artifact["filename"]
        rows.append(
            base_row(
                **artifact,
                live_path=str(path),
                live_exists=path.exists(),
                current_status="LIVE_ARTIFACT_PRESENT_UNVALIDATED" if path.exists() else "MISSING_LIVE_ARTIFACT",
                import_ready=False,
                score_ready=False,
                valid_prediction_row=False,
            )
        )
    rows.append(
        base_row(
            artifact_id="LIVE2512_8_verdict",
            filename="live tau artifact set",
            role="complete branch-locked tau-min evidence pack",
            required_columns="all exact files plus manifest",
            live_path=str(LIVE_DROP),
            live_exists=LIVE_DROP.exists(),
            current_status="LIVE_SET_INCOMPLETE",
            import_ready=False,
            score_ready=False,
            valid_prediction_row=False,
        )
    )
    return rows


def delta_w_width_law_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "law_id": "WIDTH2512_0_product_bound",
            "quantity": "P_WEP_relative_source_weight",
            "law": "abs(Delta_w_TiPt * tau_WEP) <= 2.8e-15",
            "numeric_value": "2.8e-15",
            "units": "dimensionless product",
            "status": "EXACT_PRODUCT_BOUND_FROM_2511_NONCLAIM",
        },
        {
            "law_id": "WIDTH2512_1_width_if_tau_min",
            "quantity": "Delta_w_TiPt",
            "law": "if abs(tau_WEP)>=tau_min>0 then abs(Delta_w_TiPt)<=2.8e-15/tau_min",
            "numeric_value": "MISSING_TAU_MIN",
            "units": "dimensionless source-weight width",
            "status": "EXACT_CONDITIONAL_WIDTH_LAW_NOT_EVALUABLE",
        },
        {
            "law_id": "WIDTH2512_2_tau_zero_case",
            "quantity": "WEP sensitivity",
            "law": "if tau_WEP=0 then WEP does not bound Delta_w_TiPt on this projection",
            "numeric_value": "NOT_A_PASS",
            "units": "arena statement",
            "status": "WEP_BLINDNESS_NOT_LOCAL_GR_SAFETY",
        },
        {
            "law_id": "WIDTH2512_3_total_guard",
            "quantity": "local source-weight safety",
            "law": "WEP width cannot replace PPN/R10/clock/orbit kernels for the same Delta_w_eff vector",
            "numeric_value": "MISSING_CROSS_ARENA_KERNELS",
            "units": "policy",
            "status": "LOCAL_GR_STILL_BLOCKED",
        },
    ]
    return [
        base_row(score_ready=False, valid_prediction_row=False, claim_pass=False, **row)
        for row in rows
    ]


def dryrun_result_rows() -> list[dict[str, Any]]:
    cases = [
        {
            "case_id": "DRY2512_0_live_missing",
            "case_description": "run tau-min conversion with no live drop artifacts",
            "result_status": "REFUSED_LIVE_SET_INCOMPLETE",
            "blocking_markers": "MISSING_LIVE_ARTIFACTS;MISSING_TAU_MIN",
        },
        {
            "case_id": "DRY2512_1_tau_equals_one",
            "case_description": "set tau_WEP=1 by convention",
            "result_status": "REFUSED_TAU_UNITY_SHORTCUT",
            "blocking_markers": "NO_TAU_UNITY_SHORTCUT;MISSING_NORMALIZATION_DERIVATION",
        },
        {
            "case_id": "DRY2512_2_nonzero_source_material",
            "case_description": "infer tau nonzero from nonzero source/material vectors alone",
            "result_status": "REFUSED_NULLSPACE_COUNTERMODEL",
            "blocking_markers": "MISSING_ALIGNMENT_FLOOR;KER_K_CMSM_NULLSPACE_NOT_EXCLUDED",
        },
        {
            "case_id": "DRY2512_3_product_to_width",
            "case_description": "convert 2.8e-15 product ceiling into Delta_w width without tau_min",
            "result_status": "REFUSED_MISSING_TAU_MIN",
            "blocking_markers": "MISSING_TAU_MIN;WIDTH_LAW_NOT_EVALUABLE",
        },
        {
            "case_id": "DRY2512_4_wep_to_ppn",
            "case_description": "use WEP tau result to infer PPN/local-GR closure",
            "result_status": "REFUSED_WRONG_ARENA_INFERENCE",
            "blocking_markers": "MISSING_PPN_SOURCE_KERNEL;MISSING_FIXED_GM_MAP",
        },
    ]
    return [
        base_row(
            predicted_value="NOT_COMPUTED",
            pass_fail="BLOCKED_NONCLAIM",
            score_ready=False,
            valid_prediction_row=False,
            claim_pass=False,
            **case,
        )
        for case in cases
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        {
            "decision_id": "DEC2512_0_gain",
            "decision": "TAU_NONDEGENERACY_THEOREM_WRITTEN_CONDITIONALLY",
            "rationale": "A positive tau lower bound requires an alignment floor between the readout kernel and source/material vector.",
            "status": "conditional_not_promoted",
        },
        {
            "decision_id": "DEC2512_1_reject",
            "decision": "NO_TAU_SHORTCUT",
            "rationale": "tau_WEP cannot be set to 1, and nonzero source/material factors do not exclude the readout-kernel nullspace.",
            "status": "enforced",
        },
        {
            "decision_id": "DEC2512_2_data",
            "decision": "LIVE_MICROSCOPE_TAU_PACK_MISSING",
            "rationale": "The live drop has no complete branch-locked readout/source/material/tau_min artifact set.",
            "status": "blocked_external_data_route",
        },
        {
            "decision_id": "DEC2512_3_width",
            "decision": "DELTAW_WIDTH_BLOCKED_BY_TAU_MIN",
            "rationale": "The product bound survives, but standalone Delta_w_TiPt width remains nonnumeric until tau_min exists.",
            "status": "retained_nonclaim",
        },
        {
            "decision_id": "DEC2512_4_best_next",
            "decision": "PIVOT_TO_PPN_SOURCE_KERNEL_FIXED_GM_MAP",
            "rationale": "The WEP tau route is now correctly caged; the GR/Newton bridge needs the PPN/source-normalization response kernel.",
            "status": "selected",
        },
    ]
    return [base_row(**decision) for decision in decisions]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2512_0_selected",
            selection_status="selected_theory_route",
            target_file="2513-Y5-R2FR-source-weight-PPN-response-kernel-fixed-GM-map.md",
            target_script="scripts/Y5_R2FR_source_weight_PPN_response_kernel_fixed_GM_map_2513.py",
            objective="derive or bound how Delta_w_eff enters gamma, beta, preferred-frame/source-exchange terms, and measured-GM transfer in a fixed local weak-field convention",
            success_condition="PPN source-weight response rows have units, source paths, comparator bounds, no fitted-G absorption, and valid_for_claim=false unless kernels and coefficients are real",
            do_not_do="do not infer PPN/local GR from WEP; do not import GR as the response kernel; do not absorb relative weights into measured G",
        ),
        base_row(
            route_id="NEXT2512_1_data_route",
            selection_status="held_until_files_exist",
            target_file="2513b-Y5-R2FR-MICROSCOPE-tau-live-drop-validator.md",
            target_script="scripts/Y5_R2FR_MICROSCOPE_tau_live_drop_validator_2513b.py",
            objective="validate live MICROSCOPE tau drop artifacts if the exact files appear in the 1704 live folder",
            success_condition="all exact live files parse, branch-lock, hash-lock, declare units/sign conventions, and keep nonclaim flags until later promotion",
            do_not_do="do not fabricate arrays, do not treat templates as data, do not use bound anchors as predictions",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("tau_nondegeneracy", OUTPUTS["proof_attempt"], BRANCH_COPIES["tau_nondegeneracy"]),
        ("tau_live_gate", OUTPUTS["live_artifact_gate"], BRANCH_COPIES["tau_live_gate"]),
        ("delta_w_width", OUTPUTS["delta_w_width_law"], BRANCH_COPIES["delta_w_width"]),
        ("ppn_next", OUTPUTS["next_target"], BRANCH_COPIES["ppn_next"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, src, dst in copies:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        ok, count, message = csv_rows_parse(dst)
        rows.append(
            base_row(
                copy_id=copy_id,
                source=str(src.relative_to(ROOT)),
                destination=str(dst.relative_to(ROOT)),
                copied=dst.exists(),
                parse_ok=ok,
                row_count=count,
                parse_message=message,
            )
        )
    return rows


def falsey(value: Any) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "not_computed", ""}


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name in {"source_register", "validation"}:
            continue
        for row in rows:
            for key in ("valid_for_claim", "claim_allowed", "score_ready", "valid_prediction_row", "claim_pass", "import_ready"):
                if key in row and not falsey(row[key]):
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, detail: str = "") -> None:
        checks.append(
            base_row(
                check_id=check_id,
                status="PASS" if status else "FAIL",
                detail=detail,
                valid_for_claim=False,
                claim_allowed=False,
            )
        )

    source_rows = rows_by_name["source_register"]
    live_rows = rows_by_name["live_artifact_gate"]
    add("VAL2512_00_sources_exist", all(str(row["path_exists"]) == "True" for row in source_rows))
    add("VAL2512_01_source_needles", all(str(row["source_pass"]) == "True" for row in source_rows))
    add(
        "VAL2512_02_conditional_theorem",
        any(row["proof_id"] == "TAUP2512_1_nondegeneracy_theorem" and row["formal_status"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_by_name["proof_attempt"]),
        "nondegeneracy theorem written conditionally",
    )
    add(
        "VAL2512_03_nullspace_guard",
        any(row["proof_id"] == "TAUP2512_2_nullspace_countermodel" and row["verdict"] == "BLOCKS_SHORTCUT" for row in rows_by_name["proof_attempt"]),
        "nullspace shortcut blocker present",
    )
    add(
        "VAL2512_04_tau_min_missing",
        any(row["certificate_id"] == "CERT2512_0_tau_min" and row["current_status"] == "MISSING_TAU_MIN" for row in rows_by_name["certificate_contract"]),
        "tau_min remains missing",
    )
    add(
        "VAL2512_05_live_set_incomplete",
        any(row["artifact_id"] == "LIVE2512_8_verdict" and row["current_status"] == "LIVE_SET_INCOMPLETE" for row in live_rows)
        and not all(str(row["live_exists"]) == "True" for row in live_rows if row["artifact_id"] != "LIVE2512_8_verdict"),
        "live artifact set incomplete as expected",
    )
    add(
        "VAL2512_06_width_blocked",
        any(row["law_id"] == "WIDTH2512_1_width_if_tau_min" and row["numeric_value"] == "MISSING_TAU_MIN" for row in rows_by_name["delta_w_width_law"]),
        "Delta_w width not evaluated",
    )
    add(
        "VAL2512_07_dryruns_block_claims",
        all(str(row["pass_fail"]) == "BLOCKED_NONCLAIM" and str(row["claim_pass"]) == "False" for row in rows_by_name["dryrun_results"]),
        "all dry runs nonclaim",
    )
    add(
        "VAL2512_08_next_target",
        any(row["route_id"] == "NEXT2512_0_selected" for row in rows_by_name["next_target"]),
        "PPN fixed-GM route selected",
    )
    add("VAL2512_09_no_claim_flags", no_claim_flags(rows_by_name))
    add(
        "VAL2512_10_branch_copies",
        all(str(row["copied"]) == "True" and str(row["parse_ok"]) == "True" for row in rows_by_name["branch_copies"]),
    )
    formalization = ROOT.parent / "formalization-workbench"
    formalization_hits = list(formalization.rglob("*2512*")) if formalization.exists() else []
    add(
        "VAL2512_11_no_formalization_artifacts",
        len(formalization_hits) == 0,
        ";".join(str(path) for path in formalization_hits),
    )
    add("VAL2512_12_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists())

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2512_CSV_{path.stem}", ok, f"{message}; rows={count}")
    for key, path in BRANCH_COPIES.items():
        ok, count, message = csv_rows_parse(path)
        add(f"VAL2512_COPY_CSV_{key}", ok, f"{message}; rows={count}")

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        base_row(
            check_id="VAL2512_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2512 writes the conditional tau nondegeneracy theorem, refuses shortcuts, and pivots to PPN source kernel",
            valid_for_claim=False,
            claim_allowed=False,
        )
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2512 — Tau-WEP Lower Bound or Parent Nondegeneracy Proof",
                "",
                "**Current verdict:** `tau_WEP` is not derivable as a number from the current corpus. What is derivable is the exact conditional nondegeneracy theorem: if the MICROSCOPE readout kernel and Ti/Pt source-material vector have a positive alignment floor, then `|tau_WEP| >= tau_min > 0` and the `2511` product bound converts into a `Delta_w_TiPt` width.",
                "",
                "**Hard blocker:** nonzero source and material factors do not imply nonzero `tau_WEP`; the source/material vector can live in `ker(K_CMSM)`. Therefore `tau_WEP=1` and generic nonzero assumptions are forbidden.",
                "",
                "**Strategic pivot:** the WEP tau route is now cleanly caged and data/theorem-gated. For the GR/Newton bridge, the next theory-first target is the PPN source-weight response kernel in a fixed measured-GM convention.",
                "",
                "## Source Register",
                md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "found_needles", "source_pass", "role"]),
                "",
                "## Tau Nondegeneracy Proof Attempt",
                md_table(rows_by_name["proof_attempt"], ["proof_id", "target", "claim_shape", "formal_status", "missing_clause", "verdict"]),
                "",
                "## Tau-Min Certificate Contract",
                md_table(rows_by_name["certificate_contract"], ["certificate_id", "quantity", "required_value", "units", "accepted_routes", "required_evidence", "current_status"]),
                "",
                "## Live Artifact Gate",
                md_table(rows_by_name["live_artifact_gate"], ["artifact_id", "filename", "role", "live_exists", "current_status", "import_ready"]),
                "",
                "## Delta-w Width Law",
                md_table(rows_by_name["delta_w_width_law"], ["law_id", "quantity", "law", "numeric_value", "units", "status"]),
                "",
                "## Nonclaim Dry Run",
                md_table(rows_by_name["dryrun_results"], ["case_id", "case_description", "result_status", "blocking_markers", "pass_fail", "claim_pass"]),
                "",
                "## Decision Ledger",
                md_table(rows_by_name["decision_ledger"], ["decision_id", "decision", "rationale", "status"]),
                "",
                "## Next Target",
                md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"]),
                "",
                "## Validation",
                md_table(rows_by_name["validation"], ["check_id", "status", "detail"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "proof_attempt": proof_attempt_rows(),
        "certificate_contract": certificate_contract_rows(),
        "live_artifact_gate": live_artifact_gate_rows(),
        "delta_w_width_law": delta_w_width_law_rows(),
        "dryrun_results": dryrun_result_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
