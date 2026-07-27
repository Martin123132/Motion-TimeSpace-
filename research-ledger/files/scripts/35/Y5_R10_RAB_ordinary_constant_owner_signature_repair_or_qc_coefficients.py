from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1310"
TITLE = "1310-Y5-R10-RAB-ordinary-constant-owner-signature-repair-or-qc-coefficients"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
OWNER_SIGNATURE_ATTEMPT_PATH = OUT_DIR / f"{PACK_ID}_OWNER_SIGNATURE_REPAIR_ATTEMPT.csv"
FORBIDDEN_VERTEX_GATE_PATH = OUT_DIR / f"{PACK_ID}_FORBIDDEN_VERTEX_GATE.csv"
QC_COEFFICIENT_ROWS_PATH = OUT_DIR / f"{PACK_ID}_QC_COEFFICIENT_ACQUISITION_NONCLAIM.csv"
R10_TEMPLATE_BRIDGE_PATH = OUT_DIR / f"{PACK_ID}_R10_QC_TEMPLATE_BRIDGE_NONCLAIM.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1310_VALIDATION.csv"


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
        OWNER_SIGNATURE_ATTEMPT_PATH,
        FORBIDDEN_VERTEX_GATE_PATH,
        QC_COEFFICIENT_ROWS_PATH,
        R10_TEMPLATE_BRIDGE_PATH,
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
            "source_id": "SRC1310_0_1309_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1309_NEXT_TARGET.csv",
            "needle": "NEXT1309_0_1310",
            "role": "handoff into ordinary constant owner signature repair",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1310_1_1309_theorem",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1309_QC_ZERO_THEOREM_ATTEMPT.csv",
            "needle": "FAIL_CURRENT_CLAIM_STAGE_QC_RESIDUAL",
            "role": "q_c zero theorem failed current claim and staged residual route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1310_2_1309_premise",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1309_MATTER_CONSTANT_PREMISE_GATE.csv",
            "needle": "MCG1309_2_no_direct_constant_vertices",
            "role": "prior premise gates for forbidden vertices",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1310_3_1309_residual",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1309_QC_RESIDUAL_VECTOR_NONCLAIM.csv",
            "needle": "QCR1309_3_qc_total",
            "role": "q_c residual vector being refined into coefficient-acquisition rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1310_4_1098_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
            "needle": "OWNER_ACTION_SIGNATURE_NOT_DERIVED",
            "role": "ordinary constant owner signature not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1310_5_1097_theorem",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1097_CONSTANT_SECTOR_UNIVERSALITY_THEOREM_ATTEMPT.csv",
            "needle": "CONSTANT_SECTOR_UNIVERSALITY_NOT_DERIVED",
            "role": "constant-sector universality theorem remains unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1310_6_1046_split",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv",
            "needle": "FAIL_CURRENT_CLAIM_CONSTANT_MARKER_ZERO_NOT_SIGNED",
            "role": "constant/marker zero failure and residual fallback symbols",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1310_7_1046_coefficients",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1046_QBAR_CONSTANTS_COEFFICIENT_ROWS.csv",
            "needle": "QCC1046_3_qbar_constants_abs",
            "role": "existing coefficient rows for constant qbar envelope",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1310_8_constant_contract",
            "local_path": "source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv",
            "needle": "C7_empirical_fallback",
            "role": "constant-sector empirical fallback policy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1310_9_no_species_contract",
            "local_path": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
            "needle": "S7_R1_empirical_fallback",
            "role": "species/source-charge fallback policy",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1310_10_R10_1046_template",
            "local_path": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_1046_MARKER_CONSTANT_TEMPLATE_NONCLAIM.csv",
            "needle": "MTS_1046_QBAR_MARKER_TEMPLATE",
            "role": "R10 marker/constant nonclaim template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1310_11_1309_R10_update",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1309_R10_TEMPLATE_UPDATE_NONCLAIM.csv",
            "needle": "RTU1309_1_constants_template",
            "role": "canonical q_c update to existing R10 templates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    owner_signature_attempt = [
        {
            "attempt_id": "OSA1310_0_parent_signature_candidate",
            "signature_piece": "parent action declares all ordinary constant slots before tests",
            "required_form": "S_parent[Phi,Psi]=S_geom[q(Phi)]+S_gauge[A,T_Q,q(Phi),theta_rep]+S_matter[Psi,e_obs(q),theta_rep]+S_top[theta_rep]",
            "repair_attempt": "adopt theta_rep as representation/topological data and forbid hidden Xhat/m_c arguments in ordinary matter/readout slots",
            "current_status": "CONTRACT_CANDIDATE_NOT_PARENT_SIGNED",
            "if_signed": "prevents adding arena-specific hidden constant/source vertices after the fact",
            "if_missing": "coefficient priors and q_c residual rows remain live",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv",
            "source_anchor": "OCS1098_0_parent_domain",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "OSA1310_1_unique_EM_owner",
            "signature_piece": "unique EM/gauge kinetic owner",
            "required_form": "allowed gauge kinetic norm is quotient/topological/representation-owned; forbidden: f_X(Xhat)F^2, lambda_A F^2",
            "repair_attempt": "try to classify alpha_EM as fixed theta_rep or quotient-owned gauge norm",
            "current_status": "FAIL_CURRENT_CORPUS_COUNTERTERM_LEGAL",
            "if_signed": "b_alpha theorem-zero",
            "if_missing": "b_alpha coefficient row remains live",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv",
            "source_anchor": "OCS1098_1_unique_EM_owner;CMA1046_0_alpha_EM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "OSA1310_2_matter_spectrum_owner",
            "signature_piece": "no Xhat-dependent masses/Yukawas/binding response",
            "required_form": "forbidden: m_A(Xhat), y_A(Xhat), Lambda_QCD(Xhat), B_A(Xhat), material response slots depending on Xhat",
            "repair_attempt": "try to classify mass ratios and binding fractions as theta_rep with trivial vertical action",
            "current_status": "NOT_PARENT_SIGNED",
            "if_signed": "b_mA, b_mass_ratio, b_nuc theorem-zero",
            "if_missing": "mass/binding/clock/WEP/R10 material coefficient rows remain live",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv",
            "source_anchor": "OCS1098_2_matter_spectrum_owner;CMA1046_1_particle_masses",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "OSA1310_3_source_weight_exclusion",
            "signature_piece": "no species/source-only gravitational weights",
            "required_form": "forbidden: w_A(Xhat)S_A, kappa_A(Xhat)T_A, source-only material multiplier before variation",
            "repair_attempt": "try to force one common Hilbert current and one universal/global kappa",
            "current_status": "UNSIGNED",
            "if_signed": "qbar_source_weight theorem-zero and source-normalization WEP route can advance",
            "if_missing": "R1/Newton-GM/R10 source-normalization remains live",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv",
            "source_anchor": "OCS1098_4_source_weight_exclusion;CMA1046_4_source_only_weights",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "OSA1310_4_marker_readout_radiative",
            "signature_piece": "no material marker, shadow-frame, clock/readout, or radiative re-entry",
            "required_form": "material markers absent/pure gauge; readout maps and S_eff factor through q and fixed theta_rep",
            "repair_attempt": "try to ban post-variation readout slots that reintroduce hidden invariant sensitivity",
            "current_status": "NO_MARKER_AND_RADIATIVE_READOUT_UNSIGNED",
            "if_signed": "qbar_marker_abs, b_clock_i, and readout residuals can be theorem-zero",
            "if_missing": "marker/readout q_c residual rows remain live",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv",
            "source_anchor": "OCS1098_3_clock_readout_owner;OCS1098_5_radiative_readout_closure;CMA1046_3_material_markers",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "OSA1310_5_verdict",
            "signature_piece": "ordinary constant owner/action signature",
            "required_form": "OSA1310_0 through OSA1310_4 all parent-signed together",
            "repair_attempt": "attempted repair from existing contracts and owner rows",
            "current_status": "OWNER_SIGNATURE_REPAIR_FAIL_STAGE_QC_COEFFICIENTS",
            "if_signed": "q_c components can be theorem-zero and R10 test-charge route can close",
            "if_missing": "explicit q_c coefficient acquisition is required",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1098_ORDINARY_CONSTANT_OWNER_SIGNATURE_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_R10_1309_QC_ZERO_THEOREM_ATTEMPT.csv",
            "source_anchor": "OCS1098_6_verdict;QZT1309_4_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    forbidden_vertex_gate = [
        {
            "gate_id": "FVG1310_0_alpha_vertex",
            "forbidden_vertex": "f_X(Xhat) F^2 or lambda_A F^2",
            "would_zero": "b_alpha",
            "current_status": "COUNTERTERM_LEGAL_UNTIL_OWNER_SIGNED",
            "residual_if_open": "QCA1310_0_b_alpha",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "FVG1310_1_mass_binding_vertex",
            "forbidden_vertex": "m_A(Xhat), y_A(Xhat), Lambda_QCD(Xhat), B_A(Xhat)",
            "would_zero": "b_mA;b_mass_ratio;b_nuc",
            "current_status": "MASS_SPECTRUM_OWNER_UNSIGNED",
            "residual_if_open": "QCA1310_1_b_mA",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "FVG1310_2_clock_readout_vertex",
            "forbidden_vertex": "nu_i(Xhat), Hodge/readout shadow slot, clock-specific hidden response",
            "would_zero": "b_clock_i",
            "current_status": "CLOCK_READOUT_OWNER_UNSIGNED",
            "residual_if_open": "QCA1310_2_b_clock_i",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "FVG1310_3_marker_vertex",
            "forbidden_vertex": "co-moving material marker, isotope/preparation mask, shadow-frame marker in S_parent or readout",
            "would_zero": "qbar_marker_abs",
            "current_status": "NO_MARKER_THEOREM_NOT_PARENT_SIGNED",
            "residual_if_open": "QCA1310_4_qbar_marker_abs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "FVG1310_4_source_weight_vertex",
            "forbidden_vertex": "w_A(Xhat)S_A, kappa_A(Xhat)T_A, source-only material multiplier",
            "would_zero": "qbar_source_weight",
            "current_status": "SOURCE_WEIGHT_EXCLUSION_UNSIGNED",
            "residual_if_open": "QCA1310_5_qbar_source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "FVG1310_5_radiative_reentry",
            "forbidden_vertex": "S_eff/readout reintroduces f_X, m_A(X), marker, or source-weight sensitivity",
            "would_zero": "readout/radiative residual terms",
            "current_status": "RADIATIVE_READOUT_UNSIGNED",
            "residual_if_open": "QCA1310_6_qc_total",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    qc_coefficient_rows = [
        {
            "coefficient_id": "QCA1310_0_b_alpha",
            "symbol": "b_alpha",
            "definition": "vertical derivative d ln alpha_EM/dm_c or equivalent EM/gauge kinetic marker",
            "formula_or_bound": "clock/WEP/R10 sensitivity contribution from EM/gauge kinetic response",
            "required_inputs": "b_alpha theorem-zero or value; m_c/Xhat normalization; clock/WEP sensitivities; source paths",
            "current_value": "MISSING_B_ALPHA_OR_THEOREM_ZERO",
            "units": "dimensionless",
            "observable_links": "clock;EM spectra;WEP;R10",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1046_QBAR_CONSTANTS_COEFFICIENT_ROWS.csv",
            "source_anchor": "QCC1046_0_b_alpha",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coefficient_id": "QCA1310_1_b_mA",
            "symbol": "b_mA",
            "definition": "vertical derivative of particle masses, mass ratios, Yukawa/binding constants, or nuclear response",
            "formula_or_bound": "|qbar_constants| contains sum_A |s_mA b_mA| over declared material/clock/source sensitivities",
            "required_inputs": "species/material sensitivities; b_mA values or theorem-zero source; normalization; source paths",
            "current_value": "MISSING_B_MASS_OR_THEOREM_ZERO",
            "units": "dimensionless",
            "observable_links": "WEP;composition;clock;source_charge;R10",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1046_QBAR_CONSTANTS_COEFFICIENT_ROWS.csv",
            "source_anchor": "QCC1046_1_b_mA",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coefficient_id": "QCA1310_2_b_clock_i",
            "symbol": "b_clock_i",
            "definition": "vertical derivative of a clock transition after alpha/mass/nuclear sensitivities project into readout",
            "formula_or_bound": "b_clock_i = K_alpha_i b_alpha + K_mu_i b_mu + K_nuc_i b_nuc + readout terms",
            "required_inputs": "clock sensitivity matrix; b_alpha/b_mu/b_nuc; local dXhat projection; source paths",
            "current_value": "MISSING_CLOCK_CONSTANT_PROJECTION",
            "units": "dimensionless",
            "observable_links": "R2_clock_redshift;alpha drift;clock comparison",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1046_QBAR_CONSTANTS_COEFFICIENT_ROWS.csv",
            "source_anchor": "QCC1046_2_b_clock_i",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coefficient_id": "QCA1310_3_qbar_constants_abs",
            "symbol": "qbar_constants_abs",
            "definition": "no-cancellation constant-sector envelope",
            "formula_or_bound": "|qbar_constants| <= |s_alpha b_alpha| + sum_A |s_mA b_mA| + sum_i |s_clock_i b_clock_i| + retained charge/source constants",
            "required_inputs": "all constant coefficients theorem-zero or numeric/source-backed with no-cancellation policy",
            "current_value": "MISSING_COMPONENT_VALUES",
            "units": "dimensionless_or_declared_clock_units",
            "observable_links": "WEP;clock;R10;EM;local_GR",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1046_QBAR_CONSTANTS_COEFFICIENT_ROWS.csv;source-intake/mts_residuals/P8_Y5_R10_1309_QC_RESIDUAL_VECTOR_NONCLAIM.csv",
            "source_anchor": "QCC1046_3_qbar_constants_abs;QCR1309_0_qbar_constants_abs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coefficient_id": "QCA1310_4_qbar_marker_abs",
            "symbol": "qbar_marker_abs",
            "definition": "absolute material/preparation/shadow-frame marker sensitivity",
            "formula_or_bound": "sum marker/species/preparation sensitivities with no cancellation unless parent identity supplies it",
            "required_inputs": "no-marker theorem or marker coefficients; marker normalization; source paths",
            "current_value": "MISSING_MARKER_THEOREM_OR_COEFFICIENTS",
            "units": "dimensionless",
            "observable_links": "WEP_source_charge;R10;clock;composition",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_1309_QC_RESIDUAL_VECTOR_NONCLAIM.csv",
            "source_anchor": "CMA1046_3_material_markers;QCR1309_1_qbar_marker_abs",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coefficient_id": "QCA1310_5_qbar_source_weight",
            "symbol": "qbar_source_weight",
            "definition": "species/source-only gravitational prefactor or kappa_A sensitivity",
            "formula_or_bound": "qbar_source_weight = partial_{m_c} ln kappa_A or equivalent source-only weight derivative",
            "required_inputs": "source-weight exclusion theorem or source-weight coefficient; material/source tags; source paths",
            "current_value": "MISSING_SOURCE_WEIGHT_EXCLUSION_OR_COEFFICIENT",
            "units": "dimensionless",
            "observable_links": "R1_WEP_source_charge;Newton_GM;R10;R11",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1046_CONSTANT_MARKER_SPLIT_AUDIT.csv;source-intake/mts_residuals/P8_Y5_R10_1309_QC_RESIDUAL_VECTOR_NONCLAIM.csv",
            "source_anchor": "CMA1046_4_source_only_weights;QCR1309_2_qbar_source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coefficient_id": "QCA1310_6_qc_total",
            "symbol": "q_c^T_abs",
            "definition": "total canonical test charge envelope for ordinary matter",
            "formula_or_bound": "q_c^T_abs <= qbar_constants_abs + qbar_marker_abs + qbar_source_weight + readout/radiative residual terms",
            "required_inputs": "component theorem-zero or numeric/source-backed coefficient rows; no-cancellation policy",
            "current_value": "MISSING_COMPONENT_VALUES_AND_THEOREM_ZERO",
            "units": "canonical_test_charge_units_required",
            "observable_links": "R10;R1_WEP;R2_clock;local_GR",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1309_QC_RESIDUAL_VECTOR_NONCLAIM.csv",
            "source_anchor": "QCR1309_3_qc_total",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    r10_template_bridge = [
        {
            "bridge_id": "RTB1310_0_constants_alpha",
            "branch_id": "q_c_constants_template",
            "alpha_formula": "alpha_c_constants(lambda)=s_c Pi_M^H[Q_c^H(lambda)] qbar_constants_abs/(4*pi*G_obs*M_H*m_T)",
            "required_inputs": "lambda_c;Pi_M^H[Q_c^H(lambda)];qbar_constants_abs;G_obs*M_H*m_T;alpha_bound(lambda)",
            "current_status": "TEMPLATE_NONCLAIM_MISSING_COEFFICIENTS",
            "source_path": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_1046_MARKER_CONSTANT_TEMPLATE_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_1309_R10_TEMPLATE_UPDATE_NONCLAIM.csv",
            "source_anchor": "MTS_1046_QBAR_CONSTANTS_TEMPLATE;RTU1309_1_constants_template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bridge_id": "RTB1310_1_marker_alpha",
            "branch_id": "q_c_marker_template",
            "alpha_formula": "alpha_c_marker(lambda)=s_c Pi_M^H[Q_c^H(lambda)] qbar_marker_abs/(4*pi*G_obs*M_H*m_T)",
            "required_inputs": "lambda_c;Pi_M^H[Q_c^H(lambda)];qbar_marker_abs;G_obs*M_H*m_T;alpha_bound(lambda)",
            "current_status": "TEMPLATE_NONCLAIM_MISSING_COEFFICIENTS",
            "source_path": "source-intake/mts_residuals/R10_alpha_lambda_curve_MTS_1046_MARKER_CONSTANT_TEMPLATE_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_1309_R10_TEMPLATE_UPDATE_NONCLAIM.csv",
            "source_anchor": "MTS_1046_QBAR_MARKER_TEMPLATE;RTU1309_0_marker_template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bridge_id": "RTB1310_2_source_weight_alpha",
            "branch_id": "q_c_source_weight_template",
            "alpha_formula": "alpha_c_source_weight(lambda)=s_c Pi_M^H[Q_c^H(lambda)] qbar_source_weight/(4*pi*G_obs*M_H*m_T)",
            "required_inputs": "lambda_c;Pi_M^H[Q_c^H(lambda)];qbar_source_weight;G_obs*M_H*m_T;alpha_bound(lambda)",
            "current_status": "TEMPLATE_NONCLAIM_SOURCE_WEIGHT_ROW_CREATED",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1309_QC_RESIDUAL_VECTOR_NONCLAIM.csv",
            "source_anchor": "QCR1309_2_qbar_source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bridge_id": "RTB1310_3_total_alpha_envelope",
            "branch_id": "q_c_total_envelope_template",
            "alpha_formula": "|alpha_c_total(lambda)| <= |s_c Pi_M^H[Q_c^H(lambda)]| q_c^T_abs/(4*pi*G_obs*M_H*m_T)",
            "required_inputs": "lambda_c;Pi_MQ envelope;q_c^T_abs;measured GM;bound curve;no-cancellation policy",
            "current_status": "TEMPLATE_NONCLAIM_TOTAL_ENVELOPE_CREATED",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1309_QC_RESIDUAL_VECTOR_NONCLAIM.csv;source-intake/mts_residuals/P8_Y5_R10_1308_CANONICAL_ALPHA_INPUTS_NONCLAIM.csv",
            "source_anchor": "QCR1309_3_qc_total;CAI1308_4_alpha_c",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1310_0_owner_signature",
            "claim": "ordinary constant owner/action signature is parent-signed",
            "current_status": "BLOCKED_CONTRACT_ONLY",
            "reason": "1098 remains OWNER_ACTION_SIGNATURE_NOT_DERIVED and 1310 only restates the sufficient contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1310_1_qc_zero",
            "claim": "q_c^T=0",
            "current_status": "BLOCKED_OWNER_SIGNATURE_FAILS",
            "reason": "forbidden alpha/mass/marker/source-weight/readout vertices are not excluded by parent proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1310_2_coefficients_executable",
            "claim": "q_c coefficient rows are executable",
            "current_status": "BLOCKED_VALUES_MISSING",
            "reason": "coefficient rows are explicit but contain missing theorem-zero/numeric values and source paths for values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1310_3_R10",
            "claim": "R10/local fifth-force pass",
            "current_status": "BLOCKED_NO_R10_CLAIM",
            "reason": "q_c alpha templates are nonclaim and not runner-executable",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1310_0_repair_failed",
            "decision": "do not parent-sign the ordinary constant owner signature",
            "because": "existing evidence keeps counterterms/source weights/markers/readout re-entry legal until a stronger parent action clause is derived",
            "next_action": "treat q_c coefficient rows as acquisition targets",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1310_1_coefficients_staged",
            "decision": "stage q_c coefficient rows and R10 template bridge as nonclaim",
            "because": "if theorem-zero fails, empirical/source-backed coefficients are the honest route to testability",
            "next_action": "try to source coefficient bounds or prove selected no-vertex clauses one by one",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1310_0_1311",
            "target_file": "1311-Y5-R10-RAB-qc-coefficient-source-acquisition-or-no-vertex-proof.md",
            "target_script": "scripts/Y5_R10_RAB_qc_coefficient_source_acquisition_or_no_vertex_proof.py",
            "task": "try to prove selected no-vertex clauses for b_alpha/b_mA/qbar_source_weight/qbar_marker, or source numeric/theorem-bound q_c coefficient rows with units and provenance",
            "success_condition": "at least one q_c component is theorem-zero or source-backed, or the exact coefficient acquisition blockers are recorded for R10/WEP testing",
            "do_not": "do not run or claim R10 until lambda_c, Pi_MQ, q_c coefficients, measured GM normalization, and bound curve are real",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(OWNER_SIGNATURE_ATTEMPT_PATH, owner_signature_attempt)
    write_csv(FORBIDDEN_VERTEX_GATE_PATH, forbidden_vertex_gate)
    write_csv(QC_COEFFICIENT_ROWS_PATH, qc_coefficient_rows)
    write_csv(R10_TEMPLATE_BRIDGE_PATH, r10_template_bridge)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations = []
    source_count = len(source_register)
    source_hits = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    validations.append(
        validation_row(
            "VAL1310_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_hits == source_count,
            f"{source_hits}/{source_count} source anchors found",
        )
    )
    validations.append(
        validation_row(
            "VAL1310_1_owner_repair_fails",
            "owner signature repair attempt does not parent-sign the contract",
            any(row["attempt_id"] == "OSA1310_5_verdict" and row["current_status"] == "OWNER_SIGNATURE_REPAIR_FAIL_STAGE_QC_COEFFICIENTS" for row in owner_signature_attempt),
            ";".join(str(row["attempt_id"]) + "=" + str(row["current_status"]) for row in owner_signature_attempt),
        )
    )
    validations.append(
        validation_row(
            "VAL1310_2_forbidden_vertices_covered",
            "forbidden vertex gate covers alpha, mass, clock, marker, source-weight, and radiative re-entry",
            {row["gate_id"] for row in forbidden_vertex_gate}
            == {"FVG1310_0_alpha_vertex", "FVG1310_1_mass_binding_vertex", "FVG1310_2_clock_readout_vertex", "FVG1310_3_marker_vertex", "FVG1310_4_source_weight_vertex", "FVG1310_5_radiative_reentry"},
            ";".join(str(row["gate_id"]) for row in forbidden_vertex_gate),
        )
    )
    required_coeffs = {"QCA1310_0_b_alpha", "QCA1310_1_b_mA", "QCA1310_2_b_clock_i", "QCA1310_3_qbar_constants_abs", "QCA1310_4_qbar_marker_abs", "QCA1310_5_qbar_source_weight", "QCA1310_6_qc_total"}
    validations.append(
        validation_row(
            "VAL1310_3_qc_coefficients_staged",
            "q_c coefficient acquisition rows exist and remain value-missing",
            required_coeffs.issubset({str(row["coefficient_id"]) for row in qc_coefficient_rows})
            and all("MISSING" in str(row["current_value"]) for row in qc_coefficient_rows),
            ";".join(str(row["coefficient_id"]) + "=" + str(row["current_value"]) for row in qc_coefficient_rows),
        )
    )
    validations.append(
        validation_row(
            "VAL1310_4_R10_templates_nonclaim",
            "R10 q_c template bridge rows remain nonclaim and non-executable",
            len(r10_template_bridge) == 4 and all(str(row["current_status"]).startswith("TEMPLATE_NONCLAIM") for row in r10_template_bridge),
            ";".join(str(row["bridge_id"]) + "=" + str(row["current_status"]) for row in r10_template_bridge),
        )
    )
    validations.append(
        validation_row(
            "VAL1310_5_claim_gates_block",
            "claim gates block owner/q_c/R10 promotion",
            len(claim_gates) == 4 and all(str(row["current_status"]).startswith("BLOCKED") for row in claim_gates),
            ";".join(str(row["gate_id"]) + "=" + str(row["current_status"]) for row in claim_gates),
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        OWNER_SIGNATURE_ATTEMPT_PATH,
        FORBIDDEN_VERTEX_GATE_PATH,
        QC_COEFFICIENT_ROWS_PATH,
        R10_TEMPLATE_BRIDGE_PATH,
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
    validations.append(validation_row("VAL1310_6_csv_parse", "all generated CSVs parse cleanly", parse_ok, "; ".join(parse_details)))
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1310_7_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1310_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_nonclaim([source_register, owner_signature_attempt, forbidden_vertex_gate, qc_coefficient_rows, r10_template_bridge, claim_gates, decision, next_target]),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )
    validations.append(
        validation_row(
            "VAL1310_9_next_target_1311",
            "next target routes to q_c coefficient source acquisition or no-vertex proof",
            next_target[0]["next_id"] == "NEXT1310_0_1311" and "qc-coefficient" in str(next_target[0]["target_file"]),
            str(next_target[0]["target_file"]),
        )
    )
    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1310_10_overall",
            "overall 1310 validation",
            overall_pass,
            "1310 fails to parent-sign the ordinary constant owner signature, stages q_c coefficients and R10 template bridges as nonclaim, blocks R10/local-GR claims, and routes to coefficient acquisition/no-vertex proof",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1310 Y5 R10 RAB ordinary constant owner signature repair or qc coefficients

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** the ordinary-constant owner/action signature is still **not parent-signed**. The clean signature is known, but current evidence still allows hidden `alpha_EM`, mass/binding, material-marker, source-weight, and readout/radiative vertices.

**Main progress:** the failure is now converted into explicit `q_c` coefficient acquisition rows: `b_alpha`, `b_mA`, `b_clock_i`, `qbar_constants_abs`, `qbar_marker_abs`, `qbar_source_weight`, and `q_c^T_abs`. These rows are nonclaim and value-missing, but they are now test-facing.

**Decision:** no `q_c^T=0`, no R10, and no local-GR claim from ordinary matter descent alone. Next step is either selected no-vertex proof repair or source-backed coefficient acquisition.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Owner Signature Repair Attempt

{markdown_table(owner_signature_attempt, ["attempt_id", "signature_piece", "required_form", "repair_attempt", "current_status", "if_signed", "if_missing", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"])}

## Forbidden Vertex Gate

{markdown_table(forbidden_vertex_gate, ["gate_id", "forbidden_vertex", "would_zero", "current_status", "residual_if_open", "valid_for_claim", "claim_allowed"])}

## `q_c` Coefficient Acquisition Rows

{markdown_table(qc_coefficient_rows, ["coefficient_id", "symbol", "definition", "formula_or_bound", "required_inputs", "current_value", "units", "observable_links", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"])}

## R10 `q_c` Template Bridge

{markdown_table(r10_template_bridge, ["bridge_id", "branch_id", "alpha_formula", "required_inputs", "current_status", "source_path", "source_anchor", "valid_for_claim", "claim_allowed"])}

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
