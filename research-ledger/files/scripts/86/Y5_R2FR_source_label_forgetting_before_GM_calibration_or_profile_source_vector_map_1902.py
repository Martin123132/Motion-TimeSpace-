from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1902"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1902-Y5-R2FR-source-label-forgetting-before-GM-calibration-or-profile-source-vector-map.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()


INPUTS = {
    "1901_doc": ROOT / "1901-Y5-R2FR-measured-G-common-mode-guard-or-source-vector-fill.md",
    "1901_validation": OUT / "P8_Y5_BRR545_1901_VALIDATION.csv",
    "1901_gm_guard": OUT / "P8_Y5_PARENT_QLOC_1901_MEASURED_G_COMMON_MODE_GUARD_ATTEMPT.csv",
    "1901_source_vector": OUT / "P8_Y5_PARENT_QLOC_1901_SOURCE_VECTOR_FILL_NONCLAIM.csv",
    "1901_next": OUT / "P8_Y5_PARENT_QLOC_1901_NEXT_TARGET.csv",
    "1603_source_label": OUT / "P8_Y5_PARENT_QLOC_1603_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv",
    "1684_source_label": OUT / "P8_Y5_PARENT_QLOC_1684_SOURCE_LABEL_FORGETTING_PROOF_ATTEMPT.csv",
    "1838_source_gate": OUT / "P8_Y5_PARENT_QLOC_1838_SOURCE_LABEL_FORGETTING_GATE.csv",
    "1893_source_functor": OUT / "P8_Y5_PARENT_QLOC_1893_SOURCE_FUNCTOR_LABEL_FORGETTING_ATTEMPT.csv",
    "1450_hilbert_label": OUT / "P8_Y5_R10_1450_HILBERT_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv",
    "1461_no_relative": OUT / "P8_Y5_R10_1461_NO_RELATIVE_SOURCE_LABEL_AUDIT.csv",
    "1461_countermodel": OUT / "P8_Y5_R10_1461_SOURCE_LABEL_COUNTERMODEL_AUDIT.csv",
    "1476_label_proof": OUT / "P8_Y5_R10_1476_SOURCE_LABEL_FORGETTING_PROOF_ATTEMPT.csv",
    "1476_premise_audit": OUT / "P8_Y5_R10_1476_SOURCE_LABEL_PREMISE_AUDIT.csv",
    "1695_no_source_slot": OUT / "P8_Y5_PARENT_QLOC_1695_NO_SOURCE_ONLY_SLOT_THEOREM_AUDIT.csv",
    "1886_no_source_slot": OUT / "P8_Y5_PARENT_QLOC_1886_NO_SOURCE_ONLY_SLOT_PROOF_AUDIT.csv",
    "1895_no_source_prefactor": OUT / "P8_Y5_PARENT_QLOC_1895_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_ATTEMPT.csv",
    "1896_nohom": OUT / "P8_Y5_PARENT_QLOC_1896_PARENT_SORT_DISJOINTNESS_NOHOM_ATTEMPT.csv",
    "1896_nohom_gate": OUT / "P8_Y5_PARENT_QLOC_1896_NOHOM_GATE.csv",
    "1084_profile_gates": OUT / "P8_Y5_R10_1084_PROFILE_CLOSURE_GATES.csv",
    "1084_profile_kernel": OUT / "P8_Y5_R10_1084_SOURCE_PROFILE_KERNEL_DERIVATION_LEDGER.csv",
    "1084_profile_grid": OUT / "P8_Y5_R10_1084_SOURCE_PROFILE_WEIGHTING_GRID_NONCLAIM.csv",
    "1085_profile_readout": OUT / "P8_Y5_R10_1085_PROFILE_INFLUENCE_READOUT.csv",
    "1083_dd_earth": OUT / "P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv",
    "1083_caveat": OUT / "P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv",
    "1424_source_contract": OUT / "P8_Y5_R10_1424_SOURCE_VECTOR_CONTRACT.csv",
    "local_bound_claims": LOCAL_BOUNDS / "local_bound_claims.csv",
}


SOURCE_NEEDLES = {
    "1901_doc": ["GUARD_ALGEBRA_DERIVED_RELATIVE_ZERO_NOT_DERIVED", "NEXT1901_0_primary"],
    "1901_validation": ["VAL1901_OVERALL,PASS"],
    "1901_gm_guard": ["GMG1901_5_verdict", "GUARD_ALGEBRA_DERIVED_RELATIVE_ZERO_NOT_DERIVED"],
    "1901_source_vector": ["SVF1901_6_verdict", "SOURCE_VECTOR_NOT_EXECUTABLE_NONCLAIM"],
    "1901_next": ["NEXT1901_0_primary", "source-label forgetting/no-source-slot theorem"],
    "1603_source_label": ["SLF1603_5_verdict", "SOURCE_LABEL_FORGETTING_NOT_DERIVED"],
    "1684_source_label": ["SLF1684_5_verdict", "PROOF_NOT_CLOSED"],
    "1838_source_gate": ["SLG1838_5_verdict", "SOURCE_LABEL_FORGETTING_NOT_DERIVED"],
    "1893_source_functor": ["SFL1893_5_verdict", "SOURCE_FUNCTOR_LABEL_FORGETTING_NOT_PARENT_DERIVED"],
    "1450_hilbert_label": ["HT1450_6_verdict", "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED"],
    "1461_no_relative": ["NRS1461_5_delta_q_zero_decision", "DELTA_Q_ZERO_NOT_PROMOTED"],
    "1461_countermodel": ["CM1461_0_relative_wA", "RETAIN_LIVE_NONCLAIM"],
    "1476_label_proof": ["SLF1476_4_verdict", "NOT_PARENT_DERIVED_EMIT_DELTA_W_INPUT_ROW"],
    "1476_premise_audit": ["SLP1476_5_readout_no_reentry", "CONDITIONAL_SOURCE_FILES_MISSING"],
    "1695_no_source_slot": ["NST1695_7_verdict", "NO_SOURCE_ONLY_SLOT_NOT_DERIVED_TAU_ROUTE_RETAINED"],
    "1886_no_source_slot": ["NSS1886_7_verdict", "NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED"],
    "1895_no_source_prefactor": ["NSP1895_5_verdict", "NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_PROOF_NOT_PARENT_DERIVED"],
    "1896_nohom": ["NH1896_5_verdict", "PARENT_SORT_DISJOINTNESS_NOHOM_NOT_DERIVED"],
    "1896_nohom_gate": ["NHG1896_4_verdict", "NOHOM_CLAIM_BLOCKED"],
    "1084_profile_gates": ["PCG1084_2_source_charge_basis", "PARENT_TO_DD_MAP_NOT_DERIVED"],
    "1084_profile_kernel": ["K1084_1_effective_source_charge", "FINITE_RANGE_PROFILE_DEPENDENCY_RETAINED"],
    "1084_profile_grid": ["PROFILE1084_lambda_over_RE_1", "NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM"],
    "1085_profile_readout": ["INF1085_lambda_over_RE_1", "finite_profile_live"],
    "1083_dd_earth": ["DD_EARTH1083_0_bulk_weighted", "NUMERIC_BULK_EARTH_DD_SOURCE_VECTOR_NONCLAIM"],
    "1083_caveat": ["SCG1083_3_no_measured_G_absorption", "NO_ABSORPTION_SHORTCUT_ALLOWED"],
    "1424_source_contract": ["SRCMAP1424_0_R_source", "MISSING_SOURCE_VECTOR"],
    "local_bound_claims": ["R1_WEP_source_charge", "2.8e-15"],
}


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1902_SOURCE_REGISTER.csv",
    "label_forgetting_attempt": OUT / "P8_Y5_PARENT_QLOC_1902_SOURCE_LABEL_FORGETTING_BEFORE_GM_ATTEMPT.csv",
    "no_source_slot_gate": OUT / "P8_Y5_PARENT_QLOC_1902_NO_SOURCE_SLOT_GATE.csv",
    "profile_source_map": OUT / "P8_Y5_PARENT_QLOC_1902_PROFILE_SOURCE_VECTOR_MAP_NONCLAIM.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1902_LABEL_PROFILE_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1902_LABEL_PROFILE_DRYRUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1902_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1902_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1902_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1902_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1902_VALIDATION.csv",
}


BRANCH_COPIES = {
    "label_forgetting_attempt": MICROSCOPE_RESIDUALS / OUTPUTS["label_forgetting_attempt"].name,
    "profile_source_map": SOURCE_WEIGHT_DOCS / "PROFILE_SOURCE_VECTOR_MAP_1902_NONCLAIM.csv",
    "no_source_slot_gate": QUEUE / "JR1902_NO_SOURCE_SLOT_GATE_NONCLAIM.csv",
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
        for row in rows:
            writer.writerow(row)


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
        needles = SOURCE_NEEDLES[source_id]
        missing_needles = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle_count": len(needles),
                "missing_needles": "; ".join(missing_needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing_needles else "SOURCE_OR_NEEDLE_MISSING",
                "valid_for_claim": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def label_forgetting_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "SLG1902_0_target",
            "claim_piece": "source labels forgotten before measured-G calibration",
            "formal_statement": "q_src({(T_A,A)}) = T_total must occur before any measured-G calibration, so calibration only sees one total source and cannot hide label-relative weights.",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "this is the actual local-GR source route: first forget labels, then absorb the one common scalar",
            "source_anchor": "P8_Y5_PARENT_QLOC_1901_MEASURED_G_COMMON_MODE_GUARD_ATTEMPT.csv:GMG1901_5_verdict; P8_Y5_PARENT_QLOC_1893_SOURCE_FUNCTOR_LABEL_FORGETTING_ATTEMPT.csv:SFL1893_0_target",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "SLG1902_1_label_forgotten_uniqueness",
            "claim_piece": "label-forgotten source map uniqueness",
            "formal_statement": "If the source functor domain is Stress_total and the local covariant additive source map has one calibrated normalization, then F_src(T_total)=kappa_univ T_total.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_obstruction": "once species labels are absent, kappa_A or w_A cannot be formed; only the common scalar remains, which measured-G guard handles",
            "source_anchor": "P8_Y5_PARENT_QLOC_1893_SOURCE_FUNCTOR_LABEL_FORGETTING_ATTEMPT.csv:SFL1893_3_conditional_uniqueness; P8_Y5_R10_1450_HILBERT_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv:HT1450_2_covariant_additive_uniqueness",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "SLG1902_2_same_action_not_enough",
            "claim_piece": "same Hilbert action seam",
            "formal_statement": "Same-action Hilbert variation gives T_total only after assuming no pre-action w_A; S_matter=sum_A w_A S_A remains a covariant same-action countermodel.",
            "status": "COUNTERMODEL_ACTIVE",
            "proof_or_obstruction": "same action, Ward conservation, covariance, and additivity do not themselves choose the source functor domain",
            "source_anchor": "P8_Y5_PARENT_QLOC_1684_SOURCE_LABEL_FORGETTING_PROOF_ATTEMPT.csv:SLF1684_2_same_action; P8_Y5_R10_1461_SOURCE_LABEL_COUNTERMODEL_AUDIT.csv:CM1461_0_relative_wA",
            "conditional_theorem": False,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "SLG1902_3_no_source_slot_missing",
            "claim_piece": "no-source-only slot / no-Hom",
            "formal_statement": "Hom_parent(SpeciesLabel, Coeff_active_source)=empty and no w_A S_A source-only prefactor slot must be parent-derived, not adopted.",
            "status": "NO_SOURCE_SLOT_NOHOM_NOT_PARENT_DERIVED",
            "proof_or_obstruction": "typed exclusion is exact conditionally, but parent sort/object-language derivation and readout stability are unsigned",
            "source_anchor": "P8_Y5_PARENT_QLOC_1895_NO_SOURCE_PREFACTOR_OBJECT_LANGUAGE_ATTEMPT.csv:NSP1895_5_verdict; P8_Y5_PARENT_QLOC_1896_PARENT_SORT_DISJOINTNESS_NOHOM_ATTEMPT.csv:NH1896_5_verdict",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "SLG1902_4_measure_current_missing",
            "claim_piece": "common measure/current owner",
            "formal_statement": "One action measure, one hbar, one species-blind Jacobian, and one Hilbert/coframe current owner must prevent source weights from returning before calibration.",
            "status": "COMMON_MEASURE_CURRENT_OWNER_UNSIGNED",
            "proof_or_obstruction": "species-dependent Jacobians/current rescalings survive as finite source-vector components",
            "source_anchor": "P8_Y5_R10_1476_SOURCE_LABEL_PREMISE_AUDIT.csv:SLP1476_2_action_measure_owner;SLP1476_3_current_owner",
            "conditional_theorem": False,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "SLG1902_5_readout_nonhilbert_missing",
            "claim_piece": "readout/no-reentry and non-Hilbert silence",
            "formal_statement": "J_NH must be zero/exact/projected-silent and source-worldtube/readout kernels must not recreate species labels after variation.",
            "status": "READOUT_NONHILBERT_GATES_UNSIGNED",
            "proof_or_obstruction": "non-Hilbert source current and readout selector reentry are live countermodels",
            "source_anchor": "P8_Y5_R10_1461_NO_RELATIVE_SOURCE_LABEL_AUDIT.csv:NRS1461_3_nonHilbert_current_silence;NRS1461_4_readout_no_reentry",
            "conditional_theorem": False,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "attempt_id": "SLG1902_6_verdict",
            "claim_piece": "promote source-label forgetting before GM",
            "formal_statement": "Current MTS parent primitives prove source labels are forgotten before measured-G calibration, making relative source weights theorem-zero.",
            "status": "SOURCE_LABEL_FORGETTING_BEFORE_GM_NOT_PARENT_DERIVED",
            "proof_or_obstruction": "the local-GR source route is exact conditionally, but source functor domain, no-source-slot/no-Hom, common measure/current owner, non-Hilbert silence, and readout no-reentry are not all parent-signed",
            "source_anchor": "SLG1902_0_target through SLG1902_5_readout_nonhilbert_missing",
            "conditional_theorem": True,
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def no_source_slot_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "NSG1902_0_source_domain", "required_clause": "source functor domain is Stress_total, not labelled pairs", "current_status": "FAIL_CONDITIONAL_NOT_PARENT_SIGNED", "if_pass": "relative source weights cannot be formed after variation", "if_fail": "finite source-vector branch remains live", "source_anchor": "P8_Y5_PARENT_QLOC_1838_SOURCE_LABEL_FORGETTING_GATE.csv:SLG1838_0_total_Hilbert_source", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "NSG1902_1_no_slot", "required_clause": "no source-only species prefactor slot / no Hom to active-source coefficients", "current_status": "FAIL_NO_SOURCE_SLOT_NOHOM_NOT_DERIVED", "if_pass": "pre-action w_A becomes ill-typed", "if_fail": "relative w_A countermodel survives", "source_anchor": "P8_Y5_PARENT_QLOC_1695_NO_SOURCE_ONLY_SLOT_THEOREM_AUDIT.csv:NST1695_7_verdict; P8_Y5_PARENT_QLOC_1896_NOHOM_GATE.csv:NHG1896_4_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "NSG1902_2_measure_current", "required_clause": "one action-measure/current owner", "current_status": "FAIL_MISSING_AXIOM_NOT_REDUCED", "if_pass": "Jacobian/current rescale cannot reintroduce labels", "if_fail": "current/source normalization residual remains", "source_anchor": "P8_Y5_R10_1476_SOURCE_LABEL_PREMISE_AUDIT.csv:SLP1476_2_action_measure_owner", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "NSG1902_3_readout_nonhilbert", "required_clause": "non-Hilbert current silence plus readout no-reentry", "current_status": "FAIL_READOUT_NONHILBERT_GATES_UNSIGNED", "if_pass": "downstream worldtube/readout cannot manufacture source labels", "if_fail": "profile/readout source-vector map remains necessary", "source_anchor": "P8_Y5_R10_1461_NO_RELATIVE_SOURCE_LABEL_AUDIT.csv:NRS1461_3_nonHilbert_current_silence;NRS1461_4_readout_no_reentry", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "NSG1902_4_measured_G_order", "required_clause": "measured-G calibration occurs after label forgetting", "current_status": "PASS_GUARD_ORDER_WRITTEN_NONCLAIM", "if_pass": "common scalar only may be absorbed", "if_fail": "measured-G hiding refused", "source_anchor": "P8_Y5_PARENT_QLOC_1901_COMMON_MODE_ABSORPTION_ALGEBRA.csv:ALG1901_3_claim_limit", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "NSG1902_5_verdict", "required_clause": "relative source label zero claim", "current_status": "SOURCE_LABEL_FORGETTING_CLAIM_BLOCKED", "if_pass": "move toward local-GR source theorem", "if_fail": "build profile/worldtube source-vector map", "source_anchor": "NSG1902_0_source_domain through NSG1902_4_measured_G_order", "gate_pass": False, "valid_for_claim": False},
    ]


def profile_source_map_rows() -> list[dict[str, Any]]:
    return [
        {"map_id": "PSM1902_0_bulk_context", "object": "bulk Earth DD context", "formula_or_value": "Q_alpha=1.691260686750872e-03; Q_surface=-1.211918219995745e-02", "current_status": "NUMERIC_BULK_EARTH_DD_SOURCE_VECTOR_NONCLAIM", "missing_for_claim": "profile/worldtube weighting and parent-to-DD map", "source_anchor": "P8_Y5_R10_1083_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv:DD_EARTH1083_0_bulk_weighted", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"map_id": "PSM1902_1_profile_kernel", "object": "profile-weighted effective source charge", "formula_or_value": "Q_eff(lambda)=int rho(r) q(r) W_lambda(r) dr / int rho(r) W_lambda(r) dr; W_lambda=4*pi*r^2*sinh(r/lambda)/(r/lambda)", "current_status": "DERIVED_AS_NONCLAIM_PROFILE_RULE", "missing_for_claim": "lambda_WEP owner, sourced rho(r), q(r), parent source basis", "source_anchor": "P8_Y5_R10_1084_SOURCE_PROFILE_KERNEL_DERIVATION_LEDGER.csv:K1084_1_effective_source_charge", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"map_id": "PSM1902_2_long_range_limit", "object": "bulk vector as long-range limit", "formula_or_value": "lambda >> R_E gives Q_eff -> mass-weighted bulk average plus O(R_E^2/lambda^2)", "current_status": "LONG_RANGE_LIMIT_CONDITIONALLY_DERIVED_NOT_PARENT_SIGNED", "missing_for_claim": "parent proof that WEP source carrier/range is long compared with Earth radius", "source_anchor": "P8_Y5_R10_1084_SOURCE_PROFILE_KERNEL_DERIVATION_LEDGER.csv:K1084_2_long_range_limit; P8_Y5_R10_1084_PROFILE_CLOSURE_GATES.csv:PCG1084_0_long_range_bulk_limit", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"map_id": "PSM1902_3_finite_profile_smoke", "object": "two-layer profile weighting grid", "formula_or_value": "PROFILE1084 grid shows finite-range shifts up to ~1e-3 in smoke rows", "current_status": "NUMERIC_PROFILE_WEIGHTING_SMOKE_NONCLAIM", "missing_for_claim": "PREM/shell composition import, lambda owner, source paths, material/readout match", "source_anchor": "P8_Y5_R10_1084_SOURCE_PROFILE_WEIGHTING_GRID_NONCLAIM.csv:PROFILE1084_lambda_over_RE_0p03; P8_Y5_R10_1085_PROFILE_INFLUENCE_READOUT.csv:INF1085_lambda_over_RE_0p03", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"map_id": "PSM1902_4_parent_basis_map", "object": "parent-to-DD/source basis map", "formula_or_value": "M_parent_to_source_basis maps Delta_w_eff to DD/profile source charges", "current_status": "PARENT_TO_DD_MAP_NOT_DERIVED", "missing_for_claim": "operator basis map from parent residuals to source/material response basis", "source_anchor": "P8_Y5_R10_1084_PROFILE_CLOSURE_GATES.csv:PCG1084_2_source_charge_basis; P8_Y5_R10_1083_SOURCE_VECTOR_CAVEAT_GATE.csv:SCG1083_1_parent_to_DD_map", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"map_id": "PSM1902_5_measured_G_guard", "object": "no measured-G hiding guard", "formula_or_value": "bulk/common scalar may be calibrated only after source-label forgetting; profile-relative residual remains explicit", "current_status": "GUARD_ENFORCED_NONCLAIM", "missing_for_claim": "relative zero theorem or executable profile vector", "source_anchor": "P8_Y5_PARENT_QLOC_1901_MEASURED_G_COMMON_MODE_GUARD_ATTEMPT.csv:GMG1901_5_verdict", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
        {"map_id": "PSM1902_6_verdict", "object": "profile/worldtube source-vector map", "formula_or_value": "source-vector profile map can become executable only after PSM1902_1 through PSM1902_5 are sourced/theorem-signed", "current_status": "PROFILE_SOURCE_VECTOR_MAP_NOT_EXECUTABLE_NONCLAIM", "missing_for_claim": "lambda owner, profile data, parent basis map, material/readout match, no-GM-hiding certificate", "source_anchor": "PSM1902_0_bulk_context through PSM1902_5_measured_G_guard", "score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False},
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY1902_0_label_unsigned", "label_forgetting_signed": False, "no_source_slot_signed": False, "profile_map_filled": False, "uses_bulk_as_profile": False, "uses_gm_hiding": False, "score_attempt": False, "expected_status": "REFUSED_SOURCE_LABEL_FORGETTING_NOT_PARENT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY1902_1_no_slot_unsigned", "label_forgetting_signed": True, "no_source_slot_signed": False, "profile_map_filled": False, "uses_bulk_as_profile": False, "uses_gm_hiding": False, "score_attempt": False, "expected_status": "REFUSED_NO_SOURCE_SLOT_NOT_PARENT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY1902_2_bulk_as_profile", "label_forgetting_signed": True, "no_source_slot_signed": True, "profile_map_filled": False, "uses_bulk_as_profile": True, "uses_gm_hiding": False, "score_attempt": False, "expected_status": "REFUSED_BULK_VECTOR_AS_PROFILE_SOURCE", "valid_for_claim": False},
        {"case_id": "DRY1902_3_gm_hiding", "label_forgetting_signed": True, "no_source_slot_signed": True, "profile_map_filled": False, "uses_bulk_as_profile": False, "uses_gm_hiding": True, "score_attempt": False, "expected_status": "REFUSED_MEASURED_G_HIDING", "valid_for_claim": False},
        {"case_id": "DRY1902_4_profile_missing_score", "label_forgetting_signed": True, "no_source_slot_signed": True, "profile_map_filled": False, "uses_bulk_as_profile": False, "uses_gm_hiding": False, "score_attempt": True, "expected_status": "REFUSED_PROFILE_SOURCE_MAP_NOT_EXECUTABLE", "valid_for_claim": False},
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    label_forgetting_signed = bool_string(row["label_forgetting_signed"]) == "true"
    no_source_slot_signed = bool_string(row["no_source_slot_signed"]) == "true"
    profile_map_filled = bool_string(row["profile_map_filled"]) == "true"
    uses_bulk_as_profile = bool_string(row["uses_bulk_as_profile"]) == "true"
    uses_gm_hiding = bool_string(row["uses_gm_hiding"]) == "true"
    score_attempt = bool_string(row["score_attempt"]) == "true"
    if not label_forgetting_signed:
        status = "REFUSED_SOURCE_LABEL_FORGETTING_NOT_PARENT_DERIVED"
    elif not no_source_slot_signed:
        status = "REFUSED_NO_SOURCE_SLOT_NOT_PARENT_DERIVED"
    elif uses_bulk_as_profile:
        status = "REFUSED_BULK_VECTOR_AS_PROFILE_SOURCE"
    elif uses_gm_hiding:
        status = "REFUSED_MEASURED_G_HIDING"
    elif score_attempt and not profile_map_filled:
        status = "REFUSED_PROFILE_SOURCE_MAP_NOT_EXECUTABLE"
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
        {"gate_id": "CG1902_0_label", "condition": "source labels are forgotten before measured-G calibration", "current_status": "FAIL_SOURCE_LABEL_FORGETTING_BEFORE_GM_NOT_PARENT_DERIVED", "source_anchor": "P8_Y5_PARENT_QLOC_1902_SOURCE_LABEL_FORGETTING_BEFORE_GM_ATTEMPT.csv:SLG1902_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1902_1_no_slot", "condition": "no-source-only slot/no-Hom theorem is parent-signed", "current_status": "FAIL_SOURCE_LABEL_FORGETTING_CLAIM_BLOCKED", "source_anchor": "P8_Y5_PARENT_QLOC_1902_NO_SOURCE_SLOT_GATE.csv:NSG1902_5_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1902_2_profile_map", "condition": "profile/worldtube source-vector map is executable if source labels are not zero", "current_status": "FAIL_PROFILE_SOURCE_VECTOR_MAP_NOT_EXECUTABLE_NONCLAIM", "source_anchor": "P8_Y5_PARENT_QLOC_1902_PROFILE_SOURCE_VECTOR_MAP_NONCLAIM.csv:PSM1902_6_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG1902_3_verdict", "condition": "1902 branch supports WEP/local-GR source claim", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG1902_0_label through CG1902_2_profile_map", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC1902_0_theorem", "decision": "do not promote source-label forgetting", "reason": "conditional theorem is exact, but no-source-slot/no-Hom, common measure/current owner, non-Hilbert silence, and readout no-reentry are not parent-signed", "status": "SOURCE_LABEL_ROUTE_SHARP_BUT_UNSIGNED", "next_dependency": "derive no-source-only slot from parent action grammar", "valid_for_claim": False},
        {"decision_id": "DEC1902_1_profile", "decision": "stage profile/worldtube source-vector map nonclaim", "reason": "bulk DD vector and profile kernel exist as context, but lambda owner, PREM/profile data, parent basis map, and material/readout matching are missing", "status": "PROFILE_SOURCE_MAP_STAGED_NONCLAIM", "next_dependency": "no-source-slot derivation or profile map input fill", "valid_for_claim": False},
        {"decision_id": "DEC1902_2_next", "decision": "attack no-source-only slot parent grammar next", "reason": "this is the minimal theorem that would turn measured-G guard plus source-label forgetting into local-GR source universality", "status": "NEXT_TARGET_SELECTED", "next_dependency": "1903 no-source-only slot parent grammar or profile map fill", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1902_0_primary",
            "selection_status": "selected",
            "target_doc": "1903-Y5-R2FR-no-source-only-slot-parent-grammar-or-profile-map-input-fill.md",
            "target_script": "scripts/Y5_R2FR_no_source_only_slot_parent_grammar_or_profile_map_input_fill_1903.py",
            "objective": "try to derive the no-source-only slot/no-Hom parent grammar that forbids w_A before variation; if it fails, fill profile-map input rows as nonclaim",
            "success_condition": "parent-signed no-source-only slot theorem, or source-vector profile map inputs with lambda/profile/basis/readout dependencies explicit",
            "do_not": "do not claim local-GR/WEP from conditional source-label forgetting, do not use bulk DD vector as profile source, and do not hide relative source weights in measured GM",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT1902_0_theory", "area": "source-label forgetting", "summary": "the label-forgotten Hilbert source theorem is exact conditionally but not parent-signed", "risk_level": "MINIMAL_PARENT_GRAMMAR_GAP", "project_meaning": "we know the route to GR-like source universality: no labels before calibration", "next_action": "derive no-source-only slot/no-Hom grammar", "valid_for_claim": False},
        {"status_id": "STAT1902_1_empirical", "area": "profile source-vector fallback", "summary": "profile kernel and smoke grid exist, but source-vector profile map is not executable", "risk_level": "TEST_FALLBACK_STRUCTURED_NOT_SCORE_READY", "project_meaning": "if derivation fails, the finite source branch now has a precise profile-map input contract", "next_action": "fill lambda/profile/basis/material/readout inputs", "valid_for_claim": False},
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    return {
        "source_register": source_register_rows(),
        "label_forgetting_attempt": label_forgetting_attempt_rows(),
        "no_source_slot_gate": no_source_slot_gate_rows(),
        "profile_source_map": profile_source_map_rows(),
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
    markers = ["MISSING", "UNSIGNED", "NOT_DERIVED", "NOT_PARENT", "BLOCKED", "FAIL", "COUNTER", "SMOKE", "NONCLAIM", "CLAIM_BLOCKED", "NOT_EXECUTABLE", "REFUSED"]
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
    checks.append({"validation_id": "VAL1902_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows_loaded) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False})
    label_rows = csv_rows(OUTPUTS["label_forgetting_attempt"])
    checks.append({"validation_id": "VAL1902_01_label_verdict", "status": "PASS" if any(row["attempt_id"] == "SLG1902_6_verdict" and row["status"] == "SOURCE_LABEL_FORGETTING_BEFORE_GM_NOT_PARENT_DERIVED" for row in label_rows) else "FAIL", "detail": "source-label forgetting remains unsigned", "valid_for_claim": False})
    profile_rows = csv_rows(OUTPUTS["profile_source_map"])
    checks.append({"validation_id": "VAL1902_02_profile_map", "status": "PASS" if len(profile_rows) >= 7 and all(row["score_ready"] == "False" and row["valid_prediction_row"] == "False" for row in profile_rows) else "FAIL", "detail": "profile source-vector map is nonclaim/not executable", "valid_for_claim": False})
    dry_rows = csv_rows(OUTPUTS["dryrun_results"])
    checks.append({"validation_id": "VAL1902_03_dryrun", "status": "PASS" if all(row["status_match"] == "True" and row["claim_allowed"] == "False" for row in dry_rows) else "FAIL", "detail": "dry-run refuses unsigned label/no-slot, bulk-as-profile, GM hiding, and unfilled profile scoring", "valid_for_claim": False})
    gate_rows = csv_rows(OUTPUTS["claim_gate"])
    checks.append({"validation_id": "VAL1902_04_claim_gate", "status": "PASS" if any(row["gate_id"] == "CG1902_3_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in gate_rows) else "FAIL", "detail": "claim remains blocked", "valid_for_claim": False})
    next_rows = csv_rows(OUTPUTS["next_target"])
    checks.append({"validation_id": "VAL1902_05_next_target", "status": "PASS" if any(row["route_id"] == "NEXT1902_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL", "detail": "1903 target selected", "valid_for_claim": False})
    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append({"validation_id": "VAL1902_06_claim_flags_false", "status": "PASS" if flags_ok else "FAIL", "detail": flags_detail, "valid_for_claim": False})
    blocked_ok, blocked_detail = blocked_rows_not_ready(generated_without_validation)
    checks.append({"validation_id": "VAL1902_07_blocked_markers_not_ready", "status": "PASS" if blocked_ok else "FAIL", "detail": blocked_detail, "valid_for_claim": False})
    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append({"validation_id": "VAL1902_08_csv_parse", "status": "PASS" if parse_ok else "FAIL", "detail": parse_detail, "valid_for_claim": False})
    checks.append({"validation_id": "VAL1902_09_branch_copies", "status": "PASS" if all(path.exists() for path in BRANCH_COPIES.values()) else "FAIL", "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()), "valid_for_claim": False})
    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append({"validation_id": "VAL1902_10_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False})
    formalization_hits = list(FORMALIZATION.rglob("*1902*")) if FORMALIZATION.exists() else []
    checks.append({"validation_id": "VAL1902_11_formalization_untouched", "status": "PASS" if not formalization_hits else "FAIL", "detail": f"formalization_1902_count={len(formalization_hits)}", "valid_for_claim": False})
    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append({"validation_id": "VAL1902_OVERALL", "status": "PASS" if fail_count == 0 else "FAIL", "detail": "1902 source-label forgetting before GM calibration or profile source-vector map", "valid_for_claim": False})
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1902 - Source-Label Forgetting Before GM Calibration Or Profile Source-Vector Map

## Purpose

This checkpoint tries to prove that source labels are forgotten before measured-`GM` calibration. If that proof does not close, it builds the profile/worldtube source-vector map as a nonclaim fallback.

## Result

- The source-label-forgotten Hilbert source route is exact conditionally.
- It would combine cleanly with the measured-`GM` guard from 1901.
- It is not parent-derived because no-source-only slot/no-Hom, common measure/current owner, non-Hilbert silence, and readout no-reentry remain unsigned.
- The profile source-vector map is staged, but bulk Earth DD values remain context only and cannot be treated as profile/worldtube source data.
- No WEP/local-GR claim is made.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Source-Label Forgetting Attempt

{markdown_table(rows_by_name["label_forgetting_attempt"])}

## No-Source Slot Gate

{markdown_table(rows_by_name["no_source_slot_gate"])}

## Profile Source-Vector Map

{markdown_table(rows_by_name["profile_source_map"])}

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
