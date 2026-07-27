from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1309"
TITLE = "1309-Y5-R10-RAB-matter-descent-constant-marker-theorem-or-qc-residual"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
THEOREM_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_QC_ZERO_THEOREM_ATTEMPT.csv"
PREMISE_GATE_PATH = OUT_DIR / f"{PACK_ID}_MATTER_CONSTANT_PREMISE_GATE.csv"
COUNTEREXAMPLE_PATH = OUT_DIR / f"{PACK_ID}_QC_COUNTEREXAMPLE_LEDGER.csv"
QC_RESIDUAL_VECTOR_PATH = OUT_DIR / f"{PACK_ID}_QC_RESIDUAL_VECTOR_NONCLAIM.csv"
R10_TEMPLATE_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_R10_TEMPLATE_UPDATE_NONCLAIM.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1309_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    return all(
        is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
        for rows in tables
        for row in rows
    )


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        THEOREM_ATTEMPT_PATH,
        PREMISE_GATE_PATH,
        COUNTEREXAMPLE_PATH,
        QC_RESIDUAL_VECTOR_PATH,
        R10_TEMPLATE_UPDATE_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1309_0_1308_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1308_NEXT_TARGET.csv",
            "needle": "NEXT1308_0_1309",
            "role": "handoff into q_c matter descent theorem/residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1309_1_1308_qc_input",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1308_CANONICAL_ALPHA_INPUTS_NONCLAIM.csv",
            "needle": "CAI1308_2_qc",
            "role": "canonical test charge missing input",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1309_2_618_qbar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_618_SOURCE_ZERO_CERTIFICATE_AUDIT.csv",
            "needle": "valid_conditional_theorem_not_parent_signed",
            "role": "conditional qbar_XT chain-rule theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1309_3_670_matter_descent",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
            "needle": "constant/material-marker ownership and no-extension theorem",
            "role": "matter descent route is constants-open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1309_4_670_effect",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_670_R10_R11_ZERO_OR_RESIDUAL_EFFECT.csv",
            "needle": "MISSING_MATTER_CONSTANT_OWNERSHIP",
            "role": "qbar_XT zero blocked by constant/material ownership",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1309_5_constant_contract",
            "local_path": "source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv",
            "needle": "C1_superselection_independence",
            "role": "constant-sector universality contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1309_6_no_species_contract",
            "local_path": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
            "needle": "S3_no_material_marker_extension",
            "role": "no species/source charge contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1309_7_1046_marker_split",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv",
            "needle": "FAIL_CURRENT_CLAIM_CONSTANT_MARKER_ZERO_NOT_SIGNED",
            "role": "marker/constant zero theorem failed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1309_8_1046_qbar_rows",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1046_QBAR_CONSTANTS_COEFFICIENT_ROWS.csv",
            "needle": "QCC1046_3_qbar_constants_abs",
            "role": "constant qbar residual component rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1309_9_1097_theorem",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1097_CONSTANT_SECTOR_UNIVERSALITY_THEOREM_ATTEMPT.csv",
            "needle": "CONSTANT_SECTOR_UNIVERSALITY_NOT_DERIVED",
            "role": "constant-sector theorem route not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1309_10_1098_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
            "needle": "OWNER_ACTION_SIGNATURE_NOT_DERIVED",
            "role": "ordinary constant owner signature not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1309_11_1046_R10_template",
            "local_path": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_1046_MARKER_CONSTANT_TEMPLATE_NONCLAIM.csv",
            "needle": "MTS_1046_QBAR_CONSTANTS_TEMPLATE",
            "role": "existing nonclaim R10 marker/constant fallback template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    theorem_attempt = [
        {
            "step_id": "QZT1309_0_target",
            "claim_piece": "canonical test charge zero",
            "mathematical_statement": "q_c^T = delta S_matter / delta m_c = 0 for ordinary test bodies in the compact local branch",
            "derivation_status": "TARGET_SHARP",
            "proof_or_obstruction": "this would kill R10 alpha through the test factor, independent of source charge size",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "QZT1309_1_chain_rule",
            "claim_piece": "matter descends through observed quotient",
            "mathematical_statement": "S_matter = Sbar_m[psi, e_obs(q(Phi)), omega(q(Phi)), theta_A] and Dq[v_c]=0",
            "derivation_status": "CONDITIONAL_MATH_VALID",
            "proof_or_obstruction": "if theta_A is inert, Lie_vc S_matter = 0 by chain rule",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "QZT1309_2_constant_marker_clause",
            "claim_piece": "ordinary constants and material labels are inert",
            "mathematical_statement": "Lie_vc theta_A = 0; no m_c-dependent masses, alpha_EM, binding data, source weights, marker masks, or shadow readouts",
            "derivation_status": "NOT_PARENT_SIGNED",
            "proof_or_obstruction": "1046/1097/1098 retain alpha, mass, marker, source-weight, and readout counterexamples",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "QZT1309_3_qc_result",
            "claim_piece": "q_c^T=0 promotion",
            "mathematical_statement": "q_c^T=0 follows only if QZT1309_1 and QZT1309_2 are jointly parent-signed",
            "derivation_status": "CONDITIONAL_THEOREM_NOT_PROMOTED",
            "proof_or_obstruction": "matter descent is conditional and constant/material ownership is not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "QZT1309_4_verdict",
            "claim_piece": "R10/local test-charge silence",
            "mathematical_statement": "canonical q_c theorem-zero remains unsigned; q_c residual vector must stay active",
            "derivation_status": "FAIL_CURRENT_CLAIM_STAGE_QC_RESIDUAL",
            "proof_or_obstruction": "direct coframe WEP and Z_m canonicalization do not remove q_c constants/marker/source-weight terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    premise_gate = [
        {
            "premise_id": "MCG1309_0_observed_coframe",
            "required_identity": "one observed coframe and spin connection for all ordinary matter",
            "mathematical_form": "S_m=sum_A S_A[Psi_A,e_obs(q),omega[e_obs(q)],theta_A]",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "if_missing": "direct frame/source calibration residuals remain active",
            "source_path": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
            "source_anchor": "S0_one_observed_coframe_parent_selected",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "MCG1309_1_constant_superselection",
            "required_identity": "ordinary constants are representation/topological data independent of memory/hidden invariants",
            "mathematical_form": "partial_m theta_A=partial_IQ theta_A=partial_Z theta_A=0",
            "current_status": "NOT_PARENT_DERIVED",
            "if_missing": "qbar_constants_abs and clock/WEP/R10 rows remain live",
            "source_path": "source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_1097_CONSTANT_SECTOR_UNIVERSALITY_THEOREM_ATTEMPT.csv",
            "source_anchor": "C1_superselection_independence;CSU1097_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "MCG1309_2_no_direct_constant_vertices",
            "required_identity": "no direct memory/hidden-field vertices in alpha_EM, masses, binding, clocks, or source weights",
            "mathematical_form": "forbid f_X F^2, m_A(Xhat), y_A(Xhat), w_A(Xhat)S_A, kappa_A(Xhat)T_A",
            "current_status": "OWNER_SIGNATURE_NOT_DERIVED",
            "if_missing": "b_alpha, b_mA, b_clock, and qbar_source_weight remain live",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
            "source_anchor": "OCS1098_1_unique_EM_owner;OCS1098_2_matter_spectrum_owner;OCS1098_4_source_weight_exclusion;OCS1098_6_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "MCG1309_3_no_material_marker_extension",
            "required_identity": "material markers and post-readout masks are absent, pure gauge, or explicitly residualized",
            "mathematical_form": "partial_m S_parent=0 and P_active notin args(S_parent)",
            "current_status": "NO_MARKER_THEOREM_NOT_PARENT_SIGNED",
            "if_missing": "qbar_marker_abs remains live",
            "source_path": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv",
            "source_anchor": "S3_no_material_marker_extension;CMA1046_3_material_markers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "MCG1309_4_radiative_readout_closure",
            "required_identity": "forbidden vertices do not re-enter through effective action or readout-after-variation",
            "mathematical_form": "S_eff/readout maps factor through q and fixed theta_rep",
            "current_status": "RADIATIVE_READOUT_UNSIGNED",
            "if_missing": "bare action silence cannot promote observed q_c zero",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
            "source_anchor": "OCS1098_5_radiative_readout_closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    counterexamples = [
        {
            "counterexample_id": "QCE1309_0_hidden_alpha",
            "form": "S_EM=-1/4 f_X(Xhat) F^2 with e_obs fixed",
            "why_allowed_if_unsigned": "metric/coframe descent can hold while alpha_EM varies with hidden/memory direction",
            "residual_opened": "b_alpha; clock; WEP EM binding; R10",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
            "source_anchor": "OCS1098_1_unique_EM_owner",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "QCE1309_1_mass_ratio",
            "form": "m_A(Xhat), y_A(Xhat), Lambda_QCD(Xhat), or binding B_A(Xhat)",
            "why_allowed_if_unsigned": "dimensionful unit rescaling cannot remove all mass ratios and composition-dependent binding fractions",
            "residual_opened": "b_mA; mass_ratio; WEP composition; clock; R10",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_1097_CONSTANT_SECTOR_UNIVERSALITY_THEOREM_ATTEMPT.csv",
            "source_anchor": "CMA1046_1_particle_masses;CSU1097_2_dimensionless_guard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "QCE1309_2_marker_shadow",
            "form": "co-moving material marker, preparation label, isotope fraction, or shadow/readout slot depends on Xhat",
            "why_allowed_if_unsigned": "species/source labels can preserve covariance while producing composition-dependent qbar charge",
            "residual_opened": "qbar_marker_abs; eta_source_AB; R10 marker alpha",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv",
            "source_anchor": "CMA1046_3_material_markers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "QCE1309_3_source_weight",
            "form": "w_A(Xhat)S_A or kappa_A(Xhat)T_A source-only prefactor",
            "why_allowed_if_unsigned": "Ward conservation of total stress does not force species-blind source normalization",
            "residual_opened": "qbar_source_weight; R1 WEP source charge; measured GM split",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_950_SOURCE_NORMALIZATION_LEMMA_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
            "source_anchor": "SNL950_4_countermodel;OCS1098_4_source_weight_exclusion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    qc_residual_vector = [
        {
            "residual_id": "QCR1309_0_qbar_constants_abs",
            "symbol": "qbar_constants_abs",
            "definition": "no-cancellation envelope for alpha/mass/clock/source constants coupled to the canonical memory direction",
            "formula_or_bound": "|qbar_constants| <= |s_alpha b_alpha| + sum_A |s_mA b_mA| + sum_i |s_clock_i b_clock_i| + retained charge/source constants",
            "current_value": "MISSING_COMPONENT_VALUES",
            "units": "dimensionless_or_declared_clock_units",
            "observable_links": "WEP;clock;R10;EM;local_GR",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1046_QBAR_CONSTANTS_COEFFICIENT_ROWS.csv",
            "source_anchor": "QCC1046_3_qbar_constants_abs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "QCR1309_1_qbar_marker_abs",
            "symbol": "qbar_marker_abs",
            "definition": "absolute material/preparation/shadow-frame marker sensitivity to canonical memory direction",
            "formula_or_bound": "sum over marker/species/preparation sensitivities with no cancellation unless parent identity supplies it",
            "current_value": "MISSING_MARKER_THEOREM_OR_COEFFICIENTS",
            "units": "dimensionless",
            "observable_links": "WEP_source_charge;R10;clock;composition",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv;source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_1046_MARKER_CONSTANT_TEMPLATE_NONCLAIM.csv",
            "source_anchor": "CMA1046_3_material_markers;MTS_1046_QBAR_MARKER_TEMPLATE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "QCR1309_2_qbar_source_weight",
            "symbol": "qbar_source_weight",
            "definition": "species/source-only gravitational prefactor or kappa_A sensitivity",
            "formula_or_bound": "qbar_source_weight = partial_X ln kappa_A or equivalent source-only weight derivative",
            "current_value": "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT",
            "units": "dimensionless",
            "observable_links": "R1_WEP_source_charge;Newton_GM;R10;R11",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_950_SOURCE_NORMALIZATION_LEMMA_ATTEMPT.csv",
            "source_anchor": "CMA1046_4_source_only_weights;SNL950_4_countermodel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "QCR1309_3_qc_total",
            "symbol": "q_c^T_abs",
            "definition": "total canonical test charge envelope for ordinary matter after matter descent/constant-marker audit",
            "formula_or_bound": "q_c^T_abs <= qbar_constants_abs + qbar_marker_abs + qbar_source_weight + readout/radiative residual terms",
            "current_value": "MISSING_COMPONENT_VALUES_AND_THEOREM_ZERO",
            "units": "canonical_test_charge_units_required",
            "observable_links": "R10;R1_WEP;R2_clock;local_GR",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1308_CANONICAL_ALPHA_INPUTS_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_1046_QBAR_CONSTANTS_COEFFICIENT_ROWS.csv",
            "source_anchor": "CAI1308_2_qc;QCC1046_3_qbar_constants_abs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    r10_template_update = [
        {
            "update_id": "RTU1309_0_marker_template",
            "prior_template": "R10_alpha_lambda_curve_MTS_1046_MARKER_CONSTANT_TEMPLATE_NONCLAIM.csv::MTS_1046_QBAR_MARKER_TEMPLATE",
            "canonical_update": "replace qbar_marker/shadow-frame test factor with q_c marker component after Z_m canonicalization",
            "status": "TEMPLATE_RETAINED_NONCLAIM_MISSING_COEFFICIENTS",
            "runner_effect": "runner must reject until lambda_c, Q_c/Pi_M, qbar_marker_abs, and bound curve are real",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "update_id": "RTU1309_1_constants_template",
            "prior_template": "R10_alpha_lambda_curve_MTS_1046_MARKER_CONSTANT_TEMPLATE_NONCLAIM.csv::MTS_1046_QBAR_CONSTANTS_TEMPLATE",
            "canonical_update": "replace qbar_constants test factor with q_c constants component after Z_m canonicalization",
            "status": "TEMPLATE_RETAINED_NONCLAIM_MISSING_COEFFICIENTS",
            "runner_effect": "runner must reject until b_alpha/b_mA/b_clock/source constants are theorem-zero or numeric",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1309_0_qc_zero",
            "claim": "q_c^T=0 for ordinary matter",
            "current_status": "BLOCKED_CONSTANT_MARKER_OWNER_UNSIGNED",
            "reason": "chain-rule matter descent is conditional but constant/material/source-weight clauses are not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1309_1_direct_WEP_proxy",
            "claim": "direct coframe WEP implies q_c^T=0",
            "current_status": "REJECTED_PROXY_INSUFFICIENT",
            "reason": "direct geometry WEP does not clear constants, material markers, source weights, or readout vertices",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1309_2_qc_residual",
            "claim": "q_c residual vector is executable",
            "current_status": "BLOCKED_COMPONENT_VALUES_MISSING",
            "reason": "qbar_constants_abs, qbar_marker_abs, qbar_source_weight, and readout/radiative terms are missing theorem-zero or numeric values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1309_3_R10",
            "claim": "R10/local fifth-force pass",
            "current_status": "BLOCKED_NO_R10_CLAIM",
            "reason": "test charge is explicit but not zeroed or bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1309_0_theorem_not_promoted",
            "decision": "do not promote q_c^T=0",
            "because": "constant/material/source-marker owner clauses are unsigned and counterexamples remain legal",
            "next_action": "repair parent ordinary-constant owner signature or source q_c residual components",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1309_1_best_next",
            "decision": "attack owner signature before numeric residuals",
            "because": "one parent action signature could zero alpha/mass/source-weight/marker q_c components together",
            "next_action": "try ordinary constant owner signature repair; if it fails, import source-backed q_c residual coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1309_0_1310",
            "target_file": "1310-Y5-R10-RAB-ordinary-constant-owner-signature-repair-or-qc-coefficients.md",
            "target_script": "scripts/Y5_R10_RAB_ordinary_constant_owner_signature_repair_or_qc_coefficients.py",
            "task": "try to parent-sign the ordinary constant owner/action signature that forbids alpha/mass/source-weight/marker q_c vertices; if it fails, import/stage source-backed q_c residual coefficients",
            "success_condition": "q_c component theorem-zero clauses are parent-signed, or q_c residual coefficients become explicit nonclaim inputs with source paths and units",
            "do_not": "do not use matter coframe descent alone as source/test charge zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(THEOREM_ATTEMPT_PATH, theorem_attempt)
    write_csv(PREMISE_GATE_PATH, premise_gate)
    write_csv(COUNTEREXAMPLE_PATH, counterexamples)
    write_csv(QC_RESIDUAL_VECTOR_PATH, qc_residual_vector)
    write_csv(R10_TEMPLATE_UPDATE_PATH, r10_template_update)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1309_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1309_1_qc_theorem_conditional",
            "q_c zero theorem is written but not promoted",
            any(row["step_id"] == "QZT1309_4_verdict" and row["derivation_status"] == "FAIL_CURRENT_CLAIM_STAGE_QC_RESIDUAL" for row in theorem_attempt),
            ";".join(str(row["step_id"]) + "=" + str(row["derivation_status"]) for row in theorem_attempt),
        )
    )
    validations.append(
        validation_row(
            "VAL1309_2_premise_gate_blocks",
            "matter/constant premise gates remain unsigned",
            len(premise_gate) == 5 and all(str(row["current_status"]) not in {"PASS", "PARENT_SIGNED"} for row in premise_gate),
            ";".join(str(row["premise_id"]) + "=" + str(row["current_status"]) for row in premise_gate),
        )
    )
    validations.append(
        validation_row(
            "VAL1309_3_counterexamples_retained",
            "counterexamples cover alpha, mass, marker, and source-weight channels",
            {row["counterexample_id"] for row in counterexamples}
            == {"QCE1309_0_hidden_alpha", "QCE1309_1_mass_ratio", "QCE1309_2_marker_shadow", "QCE1309_3_source_weight"},
            ";".join(str(row["counterexample_id"]) for row in counterexamples),
        )
    )
    validations.append(
        validation_row(
            "VAL1309_4_qc_residual_vector_staged",
            "q_c residual vector is staged with missing values and nonclaim status",
            len(qc_residual_vector) == 4 and all("MISSING" in str(row["current_value"]) for row in qc_residual_vector),
            ";".join(str(row["residual_id"]) + "=" + str(row["current_value"]) for row in qc_residual_vector),
        )
    )
    validations.append(
        validation_row(
            "VAL1309_5_claim_gates_block",
            "claim gates block q_c/R10 promotion",
            len(claim_gates) == 4 and all(str(row["current_status"]).startswith(("BLOCKED", "REJECTED")) for row in claim_gates),
            ";".join(str(row["gate_id"]) + "=" + str(row["current_status"]) for row in claim_gates),
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        THEOREM_ATTEMPT_PATH,
        PREMISE_GATE_PATH,
        COUNTEREXAMPLE_PATH,
        QC_RESIDUAL_VECTOR_PATH,
        R10_TEMPLATE_UPDATE_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    parse_ok = True
    parse_details: list[str] = []
    for table_path in generated_tables:
        try:
            parse_details.append(f"{table_path.name}:{len(read_csv(table_path))}")
        except Exception as error:
            parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{error}")
    validations.append(validation_row("VAL1309_6_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1309_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1309_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, theorem_attempt, premise_gate, counterexamples, qc_residual_vector, r10_template_update, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1309_9_next_target_1310",
            "next target routes to ordinary constant owner signature repair or q_c coefficients",
            next_target[0]["next_id"] == "NEXT1309_0_1310" and "ordinary-constant-owner" in str(next_target[0]["target_file"]),
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1309_10_overall",
            "overall 1309 validation",
            overall_pass,
            "1309 proves q_c zero only conditionally, keeps counterexamples and q_c residual vector active, blocks R10/local-GR claims, and routes to owner-signature repair or coefficient fill",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1309 Y5 R10 RAB matter descent constant marker theorem or qc residual

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** `q_c^T=0` is a valid conditional theorem, but it is **not parent-signed**. Matter coframe/quotient descent kills the geometric pullback part, but constants, material markers, source-only weights, and readout/radiative re-entry remain open.

**Main progress:** the exact theorem contract is now written: `S_matter` must factor through the observed quotient and all ordinary constants/material labels must be inert along the canonical memory direction. If any of those clauses fails, `q_c^T` becomes an explicit residual vector.

**Decision:** keep `q_c^T` live. The next best derivation attempt is to repair the ordinary-constant owner/action signature; if that fails, import source-backed `q_c` coefficient rows rather than claiming R10 silence.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## `q_c^T=0` Theorem Attempt

{markdown_table(theorem_attempt, ["step_id", "claim_piece", "mathematical_statement", "derivation_status", "proof_or_obstruction", "valid_for_claim", "claim_allowed"])}

## Matter/Constant Premise Gate

{markdown_table(premise_gate, ["premise_id", "required_identity", "mathematical_form", "current_status", "if_missing", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"])}

## Counterexample Ledger

{markdown_table(counterexamples, ["counterexample_id", "form", "why_allowed_if_unsigned", "residual_opened", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"])}

## `q_c` Residual Vector

{markdown_table(qc_residual_vector, ["residual_id", "symbol", "definition", "formula_or_bound", "current_value", "units", "observable_links", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"])}

## R10 Template Update

{markdown_table(r10_template_update, ["update_id", "prior_template", "canonical_update", "status", "runner_effect", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "current_status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
