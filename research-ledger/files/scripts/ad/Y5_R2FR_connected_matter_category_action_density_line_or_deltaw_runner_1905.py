from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1905"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1905-Y5-R2FR-connected-matter-category-action-density-line-or-deltaw-runner.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1904_doc": ROOT / "1904-Y5-R2FR-parent-action-constructor-exhaustion-or-action-scale-owner.md",
    "1904_validation": OUT / "P8_Y5_BRR545_1904_VALIDATION.csv",
    "1904_constructor": OUT / "P8_Y5_PARENT_QLOC_1904_PARENT_ACTION_CONSTRUCTOR_EXHAUSTION_ATTEMPT.csv",
    "1904_action_owner": OUT / "P8_Y5_PARENT_QLOC_1904_ACTION_SCALE_OWNER_ATTEMPT.csv",
    "1904_residual": OUT / "P8_Y5_PARENT_QLOC_1904_FINITE_SOURCE_WEIGHT_RESIDUAL_BRANCH_NONCLAIM.csv",
    "1904_next": OUT / "P8_Y5_PARENT_QLOC_1904_NEXT_TARGET.csv",
    "1230_action_scale": OUT / "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv",
    "1231_connectedness": OUT / "P8_Y5_R10_1231_MATTER_CATEGORY_CONNECTEDNESS_ATTEMPT.csv",
    "1464_connected_proof": OUT / "P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv",
    "1465_vertices": OUT / "P8_Y5_R10_1465_ORDINARY_MATTER_GRAPH_VERTICES.csv",
    "1465_edges": OUT / "P8_Y5_R10_1465_ORDINARY_MATTER_GRAPH_EDGES.csv",
    "1465_paths": OUT / "P8_Y5_R10_1465_ORDINARY_MATTER_GRAPH_PATH_CERTIFICATE.csv",
    "1477_graph_certificate": OUT / "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_CERTIFICATE.csv",
    "1897_projection_matrix": OUT / "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv",
    "1897_projection_requirements": OUT / "P8_Y5_PARENT_QLOC_1897_DELTAW_PROJECTION_REQUIREMENTS.csv",
    "1888_finite_intake": OUT / "P8_Y5_PARENT_QLOC_1888_FINITE_DELTAW_VECTOR_ROW_INTAKE.csv",
    "1889_basis_acquisition": OUT / "P8_Y5_PARENT_QLOC_1889_REAL_DELTAW_COMPONENT_BASIS_ACQUISITION.csv",
    "1896_basis": OUT / "P8_Y5_PARENT_QLOC_1896_FINITE_DELTAW_COMPONENT_BASIS_NONCLAIM.csv",
    "1488_lock": OUT / "P8_Y5_R10_1488_WA_DELTAW_RESIDUAL_LOCK.csv",
    "1901_gm_guard": OUT / "P8_Y5_PARENT_QLOC_1901_COMMON_MODE_ABSORPTION_ALGEBRA.csv",
    "1694_variation_identity": OUT / "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv",
}


SOURCE_NEEDLES = {
    "1904_doc": ["NEXT1904_0_primary", "1905-Y5-R2FR-connected-matter-category-action-density-line-or-deltaw-runner.md"],
    "1904_validation": ["VAL1904_OVERALL,PASS"],
    "1904_constructor": ["CE1904_5_verdict", "PARENT_ACTION_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED"],
    "1904_action_owner": ["ASO1904_5_verdict", "ACTION_SCALE_OWNER_THEOREM_NOT_DERIVED"],
    "1904_residual": ["FR1904_5_verdict", "FINITE_RESIDUAL_BRANCH_RETAINED_NONCLAIM"],
    "1904_next": ["NEXT1904_0_primary", "connected ordinary matter category"],
    "1230_action_scale": ["UAS1230_5_verdict", "CONDITIONAL_THEOREM_ONLY_NOT_CLAIMABLE"],
    "1231_connectedness": ["CMC1231_5_verdict", "CONDITIONAL_ONLY_RESIDUAL_MAP_REQUIRED"],
    "1464_connected_proof": ["CON1464_5_verdict", "PROOF_NOT_CLOSED"],
    "1465_vertices": ["V1465_6_measure_readout", "CANDIDATE_VERTEX_NOT_PARENT_SIGNED"],
    "1465_edges": ["E1465_7_measure_all", "PHYSICAL_EDGE_TEMPLATE_NOT_PARENT_CERTIFICATE"],
    "1465_paths": ["PATH1465_4_measure_to_all", "one or more edges lack parent-owned nonzero action-density/source certificate"],
    "1477_graph_certificate": ["GRC1477_1_parent_owned_connectivity", "FAIL_NOT_PARENT_SIGNED"],
    "1897_projection_matrix": ["DPM1897_6_no_cancellation_policy", "NO_CANCELLATION_POLICY_ENFORCED_NONCLAIM"],
    "1897_projection_requirements": ["DPR1897_0_parent_zero_or_values", "MISSING_PARENT_DELTAW_VALUES"],
    "1888_finite_intake": ["FDV1888_0_core_vector", "MISSING_PARENT_COMPONENT_BASIS"],
    "1889_basis_acquisition": ["CB1889_1_pre_action_species_prefactor", "LIVE_COUNTERMODEL_COMPONENT"],
    "1896_basis": ["DWB1896_6_no_cancellation_policy", "POLICY_WRITTEN_NONCLAIM"],
    "1488_lock": ["WA1488_7_lock_verdict", "NONCLAIM_LOCK"],
    "1901_gm_guard": ["ALG1901_3_claim_limit", "NO_CLAIM_PROMOTION"],
    "1694_variation_identity": ["VAR1694_5_identity_verdict", "source-weight variation identity"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1905_SOURCE_REGISTER.csv",
    "connected_category": OUT / "P8_Y5_PARENT_QLOC_1905_CONNECTED_MATTER_CATEGORY_ATTEMPT.csv",
    "action_density_line": OUT / "P8_Y5_PARENT_QLOC_1905_ACTION_DENSITY_LINE_OWNER_GATE.csv",
    "deltaw_runner": OUT / "P8_Y5_PARENT_QLOC_1905_DELTAW_RUNNER_CONTRACT_NONCLAIM.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1905_CONNECTED_DELTW_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1905_CONNECTED_DELTW_DRYRUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1905_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1905_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1905_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1905_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1905_VALIDATION.csv",
}


BRANCH_COPIES = {
    "connected_category": SOURCE_WEIGHT_DOCS / "CONNECTED_MATTER_CATEGORY_1905_NONCLAIM.csv",
    "action_density_line": MICROSCOPE_RESIDUALS / OUTPUTS["action_density_line"].name,
    "deltaw_runner": QUEUE / "JR1905_DELTAW_RUNNER_CONTRACT_NONCLAIM.csv",
    "dryrun_results": QUARANTINE / OUTPUTS["dryrun_results"].name,
}


def ensure_dirs() -> None:
    for path in [OUT, MICROSCOPE_RESIDUALS, QUEUE, SOURCE_WEIGHT_DOCS, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value).strip().lower()


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        missing = [needle for needle in SOURCE_NEEDLES[source_id] if needle not in text]
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle_count": len(SOURCE_NEEDLES[source_id]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "SOURCE_OR_NEEDLE_MISSING",
                "valid_for_claim": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def connected_category_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "CMC1905_0_target",
            "claim_piece": "connected ordinary matter category",
            "formal_statement": "C_ord is connected for source/action normalization: every source-relevant ordinary sector is linked by parent-owned nonzero action-density/source morphisms.",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "this is the graph theorem that would turn many possible w_A into one common w_*",
            "source_anchor": "P8_Y5_PARENT_QLOC_1904_NEXT_TARGET.csv:NEXT1904_0_primary; P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv:CON1464_0_target",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "CMC1905_1_naturality",
            "claim_piece": "connected naturality collapse",
            "formal_statement": "For any nonzero parent-owned morphism f:A->B, naturality w_B F(f)=F(f)w_A implies w_A=w_B; connectedness propagates w_A=w_*.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "the category-theoretic step is clean once the graph and action-density functor are parent-owned",
            "source_anchor": "P8_Y5_R10_1231_MATTER_CATEGORY_CONNECTEDNESS_ATTEMPT.csv:CMC1231_1_interaction_graph_lemma; P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv:CON1464_1_naturality_lemma",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "CMC1905_2_physical_template",
            "claim_piece": "ordinary matter physical graph",
            "formal_statement": "Electrons, photons, quarks, gluons, nuclear binding, and material response form a connected physical interaction template for Ti/Pt ordinary matter.",
            "status": "PHYSICAL_TEMPLATE_CONNECTED_NOT_PARENT_CERTIFICATE",
            "proof_or_obstruction": "the template is good physics guidance, but not a parent-owned source-normalization morphism certificate",
            "source_anchor": "P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_CERTIFICATE.csv:GRC1477_0_template_connectivity; P8_Y5_R10_1465_ORDINARY_MATTER_GRAPH_EDGES.csv:E1465_0_electron_photon through E1465_7_measure_all",
            "conditional_theorem": False,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "CMC1905_3_parent_edge_gap",
            "claim_piece": "parent-owned nonzero edge certificate",
            "formal_statement": "Each graph edge must be a parent-owned nonzero morphism on the action-density/source functor, not just a known physical interaction.",
            "status": "PARENT_OWNED_EDGES_NOT_SIGNED",
            "proof_or_obstruction": "all candidate vertices/edges/paths remain marked not parent-signed and not countable for connected graph proof",
            "source_anchor": "P8_Y5_R10_1465_ORDINARY_MATTER_GRAPH_VERTICES.csv:V1465_0_electron_lepton; P8_Y5_R10_1465_ORDINARY_MATTER_GRAPH_PATH_CERTIFICATE.csv:PATH1465_4_measure_to_all",
            "conditional_theorem": False,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "CMC1905_4_direct_sum_countermodel",
            "claim_piece": "disconnected component obstruction",
            "formal_statement": "If C_ord splits into disconnected source-normalization components C_i, then independent w_i constants preserve naturality inside each component.",
            "status": "COUNTERMODEL_RETAINED",
            "proof_or_obstruction": "connectedness must be parent-signed; it cannot be assumed from phenomenological ordinary-matter familiarity",
            "source_anchor": "P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv:CON1464_3_direct_sum_obstruction",
            "conditional_theorem": False,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "CMC1905_5_verdict",
            "claim_piece": "promote connected category theorem",
            "formal_statement": "Current MTS parent primitives prove C_ord connected for action-density/source-normalization naturality.",
            "status": "CONNECTED_MATTER_CATEGORY_NOT_PARENT_DERIVED",
            "proof_or_obstruction": "naturality is exact conditionally and the physical template is connected, but parent-owned vertices/edges/action-density morphisms remain unsigned",
            "source_anchor": "CMC1905_0_target through CMC1905_4_direct_sum_countermodel",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def action_density_line_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "ADL1905_0_line_owner", "required_clause": "one parent action-density line L_action for ordinary matter", "current_status": "FAIL_LINE_OWNER_UNSIGNED", "if_pass": "relative action/source weights are automorphisms of one line and collapse to common mode under connectedness", "if_fail": "sector action normalizations remain live residuals", "source_anchor": "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv:UAS1230_0_target; P8_Y5_R10_1477_CONNECTED_MATTER_GRAPH_CERTIFICATE.csv:GRC1477_2_action_density_line", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "ADL1905_1_common_factor", "required_clause": "connected naturality gives w_A=w_*", "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED", "if_pass": "1901 measured-G guard may absorb only this common factor", "if_fail": "Delta_w_AB remains explicit", "source_anchor": "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv:UAS1230_1_connected_naturality_lemma; P8_Y5_PARENT_QLOC_1901_COMMON_MODE_ABSORPTION_ALGEBRA.csv:ALG1901_3_claim_limit", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "ADL1905_2_measure_current", "required_clause": "same owner fixes hbar, measure, current, and species-blind Jacobian", "current_status": "FAIL_MEASURE_CURRENT_EXTENSION_UNSIGNED", "if_pass": "J_A/hbar_A cannot recreate w_A after syntax proof", "if_fail": "measure/current residual rows remain live", "source_anchor": "P8_Y5_R10_1230_ACTION_SCALE_OWNER_THEOREM_ATTEMPT.csv:UAS1230_3_measure_owner_extension", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "ADL1905_3_source_readout", "required_clause": "source-label forgetting and readout descent preserve the line owner", "current_status": "FAIL_SOURCE_READOUT_DESCENT_UNSIGNED", "if_pass": "tree-level common owner reaches WEP/R10/PPN/clocks/orbits", "if_fail": "post-variation source/readout transfer remains finite residual", "source_anchor": "P8_Y5_R10_1464_CONNECTED_MATTER_CATEGORY_PROOF_ATTEMPT.csv:CON1464_4_source_label_forgetting_dependency", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "ADL1905_4_eom_shortcut", "required_clause": "classical EOM division is not used as source proof", "current_status": "PASS_SHORTCUT_REJECTED", "if_pass": "Hilbert/coframe source seam stays visible", "if_fail": "false local-GR pass would be possible", "source_anchor": "P8_Y5_PARENT_QLOC_1694_SOURCE_WEIGHT_VARIATION_IDENTITY.csv:VAR1694_5_identity_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "ADL1905_5_verdict", "required_clause": "one action-density line owner is parent-signed", "current_status": "ACTION_DENSITY_LINE_OWNER_NOT_DERIVED", "if_pass": "relative source weights become theorem-zero up to common calibration", "if_fail": "finite Delta_w runner contract remains required", "source_anchor": "ADL1905_0_line_owner through ADL1905_4_eom_shortcut", "gate_pass": False, "valid_for_claim": False},
    ]


def deltaw_runner_rows() -> list[dict[str, Any]]:
    return [
        {"runner_id": "DWR1905_0_core_vector", "arena": "core", "formula": "Delta_w_eff = P_perp(Delta_w_species + c_A_current_rescale + Delta_w_marker_hidden + J_NH_retained + Delta_mu_projector)", "required_inputs": "parent values/bounds or theorem-zero certificates for each component; common-mode projector; norm", "current_status": "MISSING_PARENT_DELTAW_VALUES", "source_anchor": "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv:DPM1897_0_core_vector; P8_Y5_PARENT_QLOC_1897_DELTAW_PROJECTION_REQUIREMENTS.csv:DPR1897_0_parent_zero_or_values", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"runner_id": "DWR1905_1_WEP", "arena": "WEP_MICROSCOPE_TiPt", "formula": "eta_TiPt = tau_WEP K_WEP[Ti,Pt,Earth,readout] dot Delta_w_eff", "required_inputs": "official material tensor, Earth source worldtube, tau_WEP, readout convention, parent Delta_w_eff", "current_status": "KERNEL_STUB_NONCLAIM_MATERIAL_TENSOR_AND_PARENT_VALUES_MISSING", "source_anchor": "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv:DPM1897_1_WEP_MICROSCOPE; P8_Y5_PARENT_QLOC_1888_FINITE_DELTAW_VECTOR_ROW_INTAKE.csv:FDV1888_2_WEP_MICROSCOPE", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"runner_id": "DWR1905_2_R10", "arena": "R10_short_range", "formula": "alpha_Delta_w(lambda)=tau_R10(lambda) K_R10(lambda) Qbar_source_test(lambda) dot Delta_w_eff", "required_inputs": "range kernel, source/test composition, digitized alpha bound curve, parent Delta_w_eff", "current_status": "KERNEL_STUB_NONCLAIM_RANGE_KERNEL_AND_PARENT_VALUES_MISSING", "source_anchor": "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv:DPM1897_2_R10; P8_Y5_PARENT_QLOC_1888_FINITE_DELTAW_VECTOR_ROW_INTAKE.csv:FDV1888_3_R10", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"runner_id": "DWR1905_3_PPN", "arena": "PPN_beta_gamma_source", "formula": "[Delta gamma, Delta beta, alpha_i, xi]_source = M_PPN dot Delta_w_eff + retained legs", "required_inputs": "weak-field solution, PPN operator matrix, GR-limit matching, parent Delta_w_eff", "current_status": "KERNEL_STUB_NONCLAIM_OPERATOR_MATRIX_AND_GR_LIMIT_MISSING", "source_anchor": "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv:DPM1897_3_PPN", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"runner_id": "DWR1905_4_clock_orbit", "arena": "clock_and_orbital", "formula": "Delta ln nu_i = K_clock_i dot Delta_w_eff; Delta ln(GM)_obs = K_orbital dot Delta_w_eff + retained source/projector terms", "required_inputs": "clock sensitivities, orbital source map, GM convention, tau_clock, tau_orbital, parent Delta_w_eff", "current_status": "KERNEL_STUB_NONCLAIM_CLOCK_ORBITAL_INPUTS_MISSING", "source_anchor": "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv:DPM1897_4_clock;DPM1897_5_orbital", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"runner_id": "DWR1905_5_no_cancellation", "arena": "all", "formula": "observable envelope uses sum_i |K_i Delta_w_i| unless a parent identity proves signed cancellation", "required_inputs": "no-cancellation envelope or sourced covariance, not fitted cancellation", "current_status": "NO_CANCELLATION_POLICY_ENFORCED_NONCLAIM", "source_anchor": "P8_Y5_PARENT_QLOC_1897_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv:DPM1897_6_no_cancellation_policy; P8_Y5_PARENT_QLOC_1896_FINITE_DELTAW_COMPONENT_BASIS_NONCLAIM.csv:DWB1896_6_no_cancellation_policy", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"runner_id": "DWR1905_6_verdict", "arena": "runner", "formula": "finite Delta_w runner is schema-only until parent vector values/theorem-zero and arena kernels are filled", "required_inputs": "DWR1905_0 through DWR1905_5 pass with numeric/sourced values or theorem-zero certificates", "current_status": "DELTAW_RUNNER_CONTRACT_NONCLAIM_NOT_EXECUTABLE", "source_anchor": "DWR1905_0_core_vector through DWR1905_5_no_cancellation", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY1905_0_connected_unsigned", "connected_parent_graph": False, "line_owner": False, "measure_current": False, "readout_descent": False, "parent_deltaw_values": False, "arena_kernels": False, "uses_physical_template_as_proof": False, "uses_eom_division": False, "expected_status": "REFUSED_CONNECTED_CATEGORY_NOT_PARENT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY1905_1_template_as_proof", "connected_parent_graph": False, "line_owner": False, "measure_current": False, "readout_descent": False, "parent_deltaw_values": False, "arena_kernels": False, "uses_physical_template_as_proof": True, "uses_eom_division": False, "expected_status": "REFUSED_PHYSICAL_TEMPLATE_NOT_PARENT_CERTIFICATE", "valid_for_claim": False},
        {"case_id": "DRY1905_2_eom_division", "connected_parent_graph": False, "line_owner": False, "measure_current": False, "readout_descent": False, "parent_deltaw_values": False, "arena_kernels": False, "uses_physical_template_as_proof": False, "uses_eom_division": True, "expected_status": "REFUSED_EOM_DIVISION_FALSE_POSITIVE", "valid_for_claim": False},
        {"case_id": "DRY1905_3_line_unsigned", "connected_parent_graph": True, "line_owner": False, "measure_current": False, "readout_descent": False, "parent_deltaw_values": False, "arena_kernels": False, "uses_physical_template_as_proof": False, "uses_eom_division": False, "expected_status": "REFUSED_ACTION_DENSITY_LINE_OWNER_NOT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY1905_4_values_missing", "connected_parent_graph": True, "line_owner": True, "measure_current": True, "readout_descent": True, "parent_deltaw_values": False, "arena_kernels": False, "uses_physical_template_as_proof": False, "uses_eom_division": False, "expected_status": "REFUSED_PARENT_DELTAW_VALUES_MISSING", "valid_for_claim": False},
        {"case_id": "DRY1905_5_kernels_missing", "connected_parent_graph": True, "line_owner": True, "measure_current": True, "readout_descent": True, "parent_deltaw_values": True, "arena_kernels": False, "uses_physical_template_as_proof": False, "uses_eom_division": False, "expected_status": "REFUSED_ARENA_KERNELS_MISSING", "valid_for_claim": False},
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    if bool_string(row["uses_eom_division"]) == "true":
        status = "REFUSED_EOM_DIVISION_FALSE_POSITIVE"
    elif bool_string(row["uses_physical_template_as_proof"]) == "true":
        status = "REFUSED_PHYSICAL_TEMPLATE_NOT_PARENT_CERTIFICATE"
    elif bool_string(row["connected_parent_graph"]) != "true":
        status = "REFUSED_CONNECTED_CATEGORY_NOT_PARENT_DERIVED"
    elif bool_string(row["line_owner"]) != "true":
        status = "REFUSED_ACTION_DENSITY_LINE_OWNER_NOT_DERIVED"
    elif bool_string(row["measure_current"]) != "true":
        status = "REFUSED_MEASURE_CURRENT_EXTENSION_UNSIGNED"
    elif bool_string(row["readout_descent"]) != "true":
        status = "REFUSED_SOURCE_READOUT_DESCENT_UNSIGNED"
    elif bool_string(row["parent_deltaw_values"]) != "true":
        status = "REFUSED_PARENT_DELTAW_VALUES_MISSING"
    elif bool_string(row["arena_kernels"]) != "true":
        status = "REFUSED_ARENA_KERNELS_MISSING"
    else:
        status = "WOULD_REQUIRE_FULL_NUMERIC_NONCLAIM_REVIEW"
    return {
        "case_id": row["case_id"],
        "computed_status": status,
        "expected_status": row["expected_status"],
        "status_match": status == row["expected_status"],
        "claim_allowed": False,
        "valid_for_claim": False,
        "generated_utc": GENERATED_UTC,
    }


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [validate_dryrun_case(row) for row in cases]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CG1905_0_connected", "condition": "parent-owned ordinary matter graph is connected", "current_status": "FAIL_CONNECTED_MATTER_CATEGORY_NOT_PARENT_DERIVED", "source_anchor": "P8_Y5_PARENT_QLOC_1905_CONNECTED_MATTER_CATEGORY_ATTEMPT.csv:CMC1905_5_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1905_1_line", "condition": "one action-density line/measure/current/readout owner is signed", "current_status": "FAIL_ACTION_DENSITY_LINE_OWNER_NOT_DERIVED", "source_anchor": "P8_Y5_PARENT_QLOC_1905_ACTION_DENSITY_LINE_OWNER_GATE.csv:ADL1905_5_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1905_2_runner", "condition": "finite Delta_w runner is executable if theorem route fails", "current_status": "FAIL_DELTAW_RUNNER_CONTRACT_NONCLAIM_NOT_EXECUTABLE", "source_anchor": "P8_Y5_PARENT_QLOC_1905_DELTAW_RUNNER_CONTRACT_NONCLAIM.csv:DWR1905_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1905_3_verdict", "condition": "1905 supports local-GR source universality or claim-grade residual score", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG1905_0_connected through CG1905_2_runner", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC1905_0_connected", "decision": "do not promote connected matter category", "reason": "connected naturality theorem is exact, but physical graph edges are not parent-owned action-density/source morphisms", "status": "CONNECTED_ROUTE_SHARP_BUT_UNSIGNED", "next_dependency": "parent-owned graph edge certificate", "valid_for_claim": False},
        {"decision_id": "DEC1905_1_line", "decision": "do not promote action-density-line owner", "reason": "one-line owner would collapse weights to common calibration, but measure/current/readout descent is unsigned", "status": "LINE_OWNER_ROUTE_SHARP_BUT_UNSIGNED", "next_dependency": "L_action plus hbar/measure/current/readout owner", "valid_for_claim": False},
        {"decision_id": "DEC1905_2_runner", "decision": "emit Delta_w runner contract only as nonclaim", "reason": "parent Delta_w values and arena kernels are still missing", "status": "DELTAW_RUNNER_STAGED_NONCLAIM", "next_dependency": "parent values/theorem-zero plus WEP/R10/PPN/clock/orbit kernels", "valid_for_claim": False},
        {"decision_id": "DEC1905_3_next", "decision": "attack parent-owned matter graph edges next", "reason": "this is the most derivation-first route to killing relative source weights without empirical tuning", "status": "NEXT_TARGET_SELECTED", "next_dependency": "1906 parent-owned matter graph edge certificate or Delta_w runner input fill", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1905_0_primary",
            "selection_status": "selected",
            "target_doc": "1906-Y5-R2FR-parent-owned-matter-graph-edge-certificate-or-deltaw-runner-input-fill.md",
            "target_script": "scripts/Y5_R2FR_parent_owned_matter_graph_edge_certificate_or_deltaw_runner_input_fill_1906.py",
            "objective": "try to certify ordinary matter graph vertices/edges as parent-owned nonzero action-density/source morphisms; if not, fill Delta_w runner inputs as nonclaim",
            "success_condition": "parent-owned connected graph certificate, or explicit missing parent values/kernels for finite Delta_w runner",
            "do_not": "do not confuse physical interactions with parent source-normalization morphisms, do not use EOM division, and do not claim local-GR/WEP pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT1905_0_theory", "area": "connected source category", "summary": "connected naturality is mathematically clean, but the graph must be parent-owned on the source/action-density functor", "risk_level": "PARENT_GRAPH_CERTIFICATE_MISSING", "project_meaning": "the GR-source route is not dead; its exact missing certificate is now isolated", "next_action": "prove parent-owned edges or keep residuals", "valid_for_claim": False},
        {"status_id": "STAT1905_1_coupling", "area": "action-density owner", "summary": "one L_action owner would turn relative weights into common calibration, but measure/current/readout descent is not signed", "risk_level": "ACTION_LINE_OWNER_UNSIGNED", "project_meaning": "the coupling problem is now about ownership, not vague handwaving", "next_action": "derive L_action/hbar/current/readout owner", "valid_for_claim": False},
        {"status_id": "STAT1905_2_empirical", "area": "finite Delta_w runner", "summary": "runner schema covers WEP, R10, PPN, clocks, and orbital arenas but is not executable without parent values and kernels", "risk_level": "RUNNER_SCHEMA_ONLY", "project_meaning": "if derivation fails, testing route stays honest and visible", "next_action": "fill parent Delta_w values or theorem-zero rows", "valid_for_claim": False},
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    return {
        "source_register": source_register_rows(),
        "connected_category": connected_category_rows(),
        "action_density_line": action_density_line_rows(),
        "deltaw_runner": deltaw_runner_rows(),
        "dryrun_cases": cases,
        "dryrun_results": dryrun_result_rows(cases),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def copy_branch_artifacts() -> None:
    for key, target in BRANCH_COPIES.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUTPUTS[key], target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in fields.intersection(row.keys()):
                if bool_string(row[field]) == "true":
                    bad.append(f"{path.name}:{index}:{field}=true")
    return not bad, "; ".join(bad) if bad else "all generated claim/scoring/signature flags remain false"


def blocked_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    markers = ["MISSING", "UNSIGNED", "NOT_DERIVED", "NOT_PARENT", "BLOCKED", "FAIL", "COUNTER", "NONCLAIM", "NOT_EXECUTABLE", "REFUSED"]
    fields = {"valid_for_claim", "claim_allowed", "valid_prediction_row", "score_ready", "gate_pass", "parent_signed"}
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            text = " ".join(str(value) for value in row.values())
            if any(marker in text for marker in markers):
                for field in fields.intersection(row.keys()):
                    if bool_string(row[field]) == "true":
                        bad.append(f"{path.name}:{index}:{field}=true despite blocked marker")
    return not bad, "; ".join(bad) if bad else "blocked/unsigned/nonclaim rows are not score-ready"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        try:
            rows = csv_rows(path)
            if not rows:
                bad.append(f"{path.name}:empty")
        except Exception as exc:
            bad.append(f"{path.name}:{exc}")
    return not bad, "; ".join(bad) if bad else f"parsed {len(paths)} csv files"


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []
    source_rows_loaded = csv_rows(OUTPUTS["source_register"])
    checks.append({"validation_id": "VAL1905_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False})
    connected_rows = csv_rows(OUTPUTS["connected_category"])
    checks.append({"validation_id": "VAL1905_01_connected_verdict", "status": "PASS" if any(row["attempt_id"] == "CMC1905_5_verdict" and row["status"] == "CONNECTED_MATTER_CATEGORY_NOT_PARENT_DERIVED" for row in connected_rows) else "FAIL", "detail": "connected matter category remains unsigned", "valid_for_claim": False})
    line_rows = csv_rows(OUTPUTS["action_density_line"])
    checks.append({"validation_id": "VAL1905_02_line_verdict", "status": "PASS" if any(row["gate_id"] == "ADL1905_5_verdict" and row["current_status"] == "ACTION_DENSITY_LINE_OWNER_NOT_DERIVED" for row in line_rows) else "FAIL", "detail": "action-density line owner remains unsigned", "valid_for_claim": False})
    runner_rows = csv_rows(OUTPUTS["deltaw_runner"])
    checks.append({"validation_id": "VAL1905_03_runner", "status": "PASS" if any(row["runner_id"] == "DWR1905_6_verdict" and row["current_status"] == "DELTAW_RUNNER_CONTRACT_NONCLAIM_NOT_EXECUTABLE" for row in runner_rows) and all(bool_string(row["valid_prediction_row"]) == "false" for row in runner_rows) else "FAIL", "detail": "Delta_w runner remains schema-only/nonclaim", "valid_for_claim": False})
    dry_rows = csv_rows(OUTPUTS["dryrun_results"])
    checks.append({"validation_id": "VAL1905_04_dryrun", "status": "PASS" if all(bool_string(row["status_match"]) == "true" and bool_string(row["claim_allowed"]) == "false" for row in dry_rows) else "FAIL", "detail": "dry-run refuses physical-template proof, EOM shortcut, unsigned graph, and missing runner inputs", "valid_for_claim": False})
    gate_rows = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1905_05_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1905_3_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1905_06_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1905_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL", "detail": "1906 target selected", "valid_for_claim": False})
    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1905_07_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1905_08_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1905_09_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1905_10_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1905_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = []
    if FORMALIZATION.exists():
        artifact_needles = [
            "1905-Y5-R2FR-connected-matter-category",
            "P8_Y5_PARENT_QLOC_1905",
            "Y5_R2FR_connected_matter_category_action_density_line_or_deltaw_runner_1905",
        ]
        formalization_hits = [
            path
            for path in FORMALIZATION.rglob("*")
            if path.is_file() and any(needle in path.name for needle in artifact_needles)
        ]
    checks.append({"validation_id": "VAL1905_12_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1905_artifact_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1905_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1905 connected matter category action-density line or Delta_w runner", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1905 - Connected Matter Category / Action-Density Line Or Delta_w Runner

## Purpose

This checkpoint tries the cleanest remaining source-coupling derivation: prove ordinary matter is one parent-owned connected action-density/source category. If not, it emits a finite `Delta_w` runner contract as nonclaim.

## Result

- Connected naturality is exact conditionally: a parent-owned connected matter graph collapses relative weights to one common factor.
- The physical ordinary-matter graph is connected as a template, but it is not yet a parent-owned source-normalization morphism certificate.
- One action-density-line owner remains unsigned because measure/current/readout descent is not parent-signed.
- The finite `Delta_w` runner is schema-only: parent component values and arena kernels are missing.
- No WEP, local-GR, Newtonian-limit, or claim-grade residual score is promoted.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Connected Matter Category Attempt

{markdown_table(rows_by_name["connected_category"])}

## Action-Density Line Owner Gate

{markdown_table(rows_by_name["action_density_line"])}

## Delta_w Runner Contract

{markdown_table(rows_by_name["deltaw_runner"])}

## Dry-Run Cases

{markdown_table(rows_by_name["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows_by_name["dryrun_results"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
