from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2675"
BRANCH_ID = "Y5_R2FR_SPECIES_CLOCK_CHANNEL_ZERO_OR_FIRST_BOUND_FILL_2675"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
WEP_COEFF = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "coefficients"

DOC_PATH = ROOT / "2675-Y5-R2FR-species-clock-channel-zero-or-first-bound-fill.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2675_SOURCE_REGISTER.csv",
    "proof_audit": RESIDUALS / "P8_Y5_R2FR_2675_SPECIES_CLOCK_ZERO_PROOF_AUDIT.csv",
    "species_residual": RESIDUALS / "P8_species_source_charge_residual_or_zero.csv",
    "clock_residual": RESIDUALS / "P8_Y5_R2FR_2675_CLOCK_TAU_READOUT_RESIDUAL_OR_ZERO.csv",
    "first_bound_fill": RESIDUALS / "P8_Y5_R2FR_2675_SPECIES_CLOCK_FIRST_BOUND_FILL_NONCLAIM.csv",
    "runner_results": RESIDUALS / "P8_Y5_R2FR_2675_SPECIES_CLOCK_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2675_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2675_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2675_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2675_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2675_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "wep_sources": SOURCE_INTAKE / "wep-sources" / "P8_species_source_charge_residual_or_zero.csv",
    "microscope_coefficients": WEP_COEFF / "species_clock_first_bound_fill_nonclaim_2675.csv",
    "clock_branch": SOURCE_INTAKE / "clocks" / "branch_locked_local" / "P8_Y5_2675_CLOCK_READOUT_ROWS_NONCLAIM.csv",
    "local_bounds": SOURCE_INTAKE / "local_bounds" / "Species_clock_channel_first_bound_fill_2675_NONCLAIM.csv",
    "source_weight": SOURCE_INTAKE / "source-weight" / "SPECIES_CLOCK_CHANNEL_FIRST_BOUND_FILL_2675_NONCLAIM.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2675_2674_BOUND_TEMPLATE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2674_QBARXT_BOUND_TEMPLATE_NONCLAIM.csv",
        "required_needles": ["BND2674_1_clock", "BND2674_2_species", "2.8e-15", "template_nonclaim"],
        "purpose": "inherits species/clock channel split from 2674",
    },
    {
        "source_id": "SRC2675_2674_CHANNEL_AUDIT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2674_MATTER_CHANNEL_DESCENT_AUDIT.csv",
        "required_needles": ["CH2674_1_rods_clocks_photons", "CH2674_2_atomic_masses_species", "MISSING_NO_SPECIES_MARKER_THEOREM"],
        "purpose": "records why species and clock channels were selected",
    },
    {
        "source_id": "SRC2675_NO_SPECIES_CONTRACT",
        "relative_path": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
        "required_needles": ["S1_matter_factorization", "S2_constant_sector_universality", "S4_source_normalization_species_blind", "S5_no_bulk_boundary_composition_charge", "S7_R1_empirical_fallback"],
        "purpose": "states sufficient no-species-source-charge theorem and fallback",
    },
    {
        "source_id": "SRC2675_CONSTANT_SECTOR",
        "relative_path": "source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv",
        "required_needles": ["C4_no_constant_running_from_local_MTS", "C6_measured_GM_absolute_calibration", "C7_empirical_fallback"],
        "purpose": "keeps constants/source normalization separate from ordinary representation data",
    },
    {
        "source_id": "SRC2675_CHANNEL_OWNER_LEDGER",
        "relative_path": "source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_OWNER_LEDGER.csv",
        "required_needles": ["species_source_charge", "epsilon_species_A", "retained_coefficient_required"],
        "purpose": "identifies species_source_charge as retained coefficient until zero or bound",
    },
    {
        "source_id": "SRC2675_CHANNEL_BOUND_SUMMARY",
        "relative_path": "source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv",
        "required_needles": ["species_source_charge", "2.8e-15", "dimensionless", "not_claimable"],
        "purpose": "imports existing nonclaim WEP/source-charge bound scale",
    },
    {
        "source_id": "SRC2675_WEP_REQUIREMENTS_1451",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/epsilon_A_bound_input_requirements_1451.csv",
        "required_needles": ["REQ1451_0_definition", "REQ1451_1_WEP", "REQ1451_4_clocks", "MISSING_CLOCK_SOURCE_MAP"],
        "purpose": "lists missing inputs for epsilon_A scoring across WEP and clock arenas",
    },
    {
        "source_id": "SRC2675_WEP_MINIMAL_CLAUSE",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_minimal_parent_clause.csv",
        "required_needles": ["MPC1439_0_clause", "MPC1439_1_formal_zero", "MPC1439_4_verdict", "NOT_ADOPTED_NOT_ZERO_CERTIFIED"],
        "purpose": "provides exact conditional WEP/source zero theorem shape",
    },
    {
        "source_id": "SRC2675_COMMON_MEASURE",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv",
        "required_needles": ["CMT1452_0_target", "CMT1452_3_species_jacobian_countermodel", "CMT1452_6_verdict", "FAIL_CURRENT_PROOF_NOT_PARENT_SIGNED"],
        "purpose": "shows why common measure/current owner is the core unsigned clause",
    },
    {
        "source_id": "SRC2675_CURRENT_OWNER",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/current_source_normalization_owner_theorem_attempt_1453.csv",
        "required_needles": ["CSO1453_1_hilbert_variation", "CSO1453_5_pre_variation_weight", "CSO1453_6_nonhilbert_bypass", "CSO1453_7_verdict"],
        "purpose": "separates useful Hilbert/Ward subtheorems from surviving source-owner loopholes",
    },
    {
        "source_id": "SRC2675_COUPLING_DERIVATION",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_coupling_derivation_attempt_nonclaim_1484.csv",
        "required_needles": ["CPD1484_2_double_zero_route", "CPD1484_3_finite_route", "CPD1484_5_verdict", "NOT_CLOSED"],
        "purpose": "keeps WEP finite coefficient route nonclaim unless parent coefficient exists",
    },
    {
        "source_id": "SRC2675_FINITE_CX_CONTRACT",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_finite_CX_contract_1911_nonclaim.csv",
        "required_needles": ["CX1911_electron", "CX1911_EM", "MISSING_PARENT_COEFFICIENT", "FINITE_CX_CONTRACT_ONLY_NOT_FILLED"],
        "purpose": "lists allowed finite parent coefficient forms and forbids bound inversion",
    },
    {
        "source_id": "SRC2675_CLOCK_FILL_TEMPLATE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1321_CLOCK_FIRST_FILL_TEMPLATE.csv",
        "required_needles": ["CLK1321_0_direct_product", "CLK1321_1_factorized_product", "CLK1321_2_tau_readout", "CLK1321_3_clock_model"],
        "purpose": "defines first clock rows that can eventually be scored",
    },
    {
        "source_id": "SRC2675_CLOCK_GAP",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1322_CLOCK_READOUT_GAP_LEDGER.csv",
        "required_needles": ["GAP1322_0_chix_parent", "GAP1322_1_local_time_projection", "GAP1322_3_balpha", "GAP1322_4_stationary_tau"],
        "purpose": "records missing clock readout and tau-theorem pieces",
    },
    {
        "source_id": "SRC2675_ALPHAEM_WEP_CLOCK_GATE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1396_ALPHAEM_WEP_CLOCK_R10_GATE.csv",
        "required_needles": ["EMG1396_1_WEP", "EMG1396_2_clock", "BLOCKED_WEP_SOURCE_NORMALIZATION_MISSING", "BLOCKED_CLOCK_PRODUCT_NONCLAIM"],
        "purpose": "joint WEP/clock gate keeps both channels nonclaim",
    },
    {
        "source_id": "SRC2675_ALPHA_CLOCK_PRODUCT",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/alpha_product_source_fill_nonclaim_1470.csv",
        "required_needles": ["APR1470_0_alpha_clock", "2.1e-18", "MISSING_MTS_VALUE_AND_DYNAMICS", "COMPARISON_SIDE_FILLED_ONLY"],
        "purpose": "imports comparison-side clock bound as nonclaim only",
    },
    {
        "source_id": "SRC2675_CLOCK_COMPONENTS",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/alpha_product_prediction_components_nonclaim_1471.csv",
        "required_needles": ["DeltaK_alpha(YbE3/YbE2)", "-6.95", "MISSING_PARENT_TAU_CLOCK_XHAT_MAP", "MISSING_PARENT_ALPHA_OWNER_OR_THEOREM_ZERO"],
        "purpose": "provides one source-backed clock sensitivity component but missing MTS dynamics",
    },
    {
        "source_id": "SRC2675_CLOCK_SHARED_QUEUE",
        "relative_path": "source-intake/clocks/branch_locked_local/shared_local_arena_projection_queue_nonclaim_2443.csv",
        "required_needles": ["SAP2443_2_clocks", "PARTIAL_SENSITIVITY_NONCLAIM", "NEXT_TARGET_SOURCE_LEG_OWNER"],
        "purpose": "connects clock row to the shared local source-leg problem",
    },
    {
        "source_id": "SRC2675_MICROSCOPE_FINAL_RESULTS_LOCAL",
        "relative_path": "source-intake/wep-sources/1899/MICROSCOPE_final_results_arxiv_2209_15487.pdf",
        "required_needles": [],
        "purpose": "local empirical provenance file for future WEP source row extraction; not parsed here",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_text(path: Path) -> str:
    if not path.exists() or path.suffix.lower() == ".pdf":
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = []
        for header in headers:
            value = str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def proof_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "Z2675_0_species_conditional_theorem",
            "channel": "species/source charge",
            "candidate_theorem": "If S_matter=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_univ] with one parent measure/action scale, source current varied before readout, no pre-variation weights, no non-Hilbert bypass, and no boundary/domain composition charge, then epsilon_species_A=0 and eta_source_AB=0.",
            "exact_consequence": "delta_vA S_matter=0 and partial_A ln(mu_obs/M_inertial)=0, so the source-side WEP residual vanishes.",
            "current_status": "CONDITIONAL_THEOREM_CLEAN_NOT_PARENT_SIGNED",
            "blocking_clauses": "hbar_parent/measure owner unsigned; source current owner only conditional; pre-action weights survive; non-Hilbert bypass open; source-label forgetting not signed",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_minimal_parent_clause.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/current_source_normalization_owner_theorem_attempt_1453.csv")),
                ]
            ),
            "theorem_zero": "false",
            "first_bound_fill_needed": "true",
            "valid_for_claim": "false",
            "next_action": "attack parent action-scale/measure owner rather than importing epsilon_A=0",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "Z2675_1_species_countermodel_filter",
            "channel": "species/source charge",
            "candidate_theorem": "Forbid species-only source slots and relative measure/current weights in the parent object language.",
            "exact_consequence": "epsilon_A, J_A, c_A, zeta_A and species Jacobian rows would be illegal rather than merely small.",
            "current_status": "COUNTERMODELS_SURVIVE_CURRENT_CORPUS",
            "blocking_clauses": "species Jacobian, pre-variation weight, source rescaling before readout, non-Hilbert current and boundary/source labels remain legal in the current grammar",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_no_source_slot_signing_decision_1451.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_source_factorization_signing_decision_1461.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_coupling_derivation_attempt_nonclaim_1484.csv")),
                ]
            ),
            "theorem_zero": "false",
            "first_bound_fill_needed": "true",
            "valid_for_claim": "false",
            "next_action": "write the exact parent object-language exclusion or keep epsilon_A finite/nonclaim",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "Z2675_2_clock_conditional_theorem",
            "channel": "clock/tau readout",
            "candidate_theorem": "If the same parent tau fixes source, charge, clock and boundary readout, and either tau_clock_time=0 or b_alpha=0 by parent descent, then P_clock_alpha=0.",
            "exact_consequence": "Delta ln R_clock = DeltaK_alpha*b_alpha*tau_clock_time + other sourced mass/nuclear products; the alpha product vanishes when b_alpha or tau_clock_time is theorem-zero.",
            "current_status": "CONDITIONAL_THEOREM_CLEAN_NOT_PARENT_SIGNED",
            "blocking_clauses": "chi_X parent state missing; local time projection missing; b_alpha owner unsigned; stationary tau silence unsigned; MTS readout kernel missing",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/mts_residuals/P8_Y5_R10_1321_CLOCK_FIRST_FILL_TEMPLATE.csv")),
                    str(path_for("source-intake/mts_residuals/P8_Y5_R10_1322_CLOCK_READOUT_GAP_LEDGER.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/alpha_product_prediction_components_nonclaim_1471.csv")),
                ]
            ),
            "theorem_zero": "false",
            "first_bound_fill_needed": "true",
            "valid_for_claim": "false",
            "next_action": "keep clock comparison side; derive tau/readout kernel before scoring MTS clock prediction",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "Z2675_3_shared_species_clock_owner",
            "channel": "shared local source leg",
            "candidate_theorem": "One parent source-leg owner fixes both species source charge and clock source-potential readout.",
            "exact_consequence": "the same object would feed WEP, clocks, R10 and PPN; no arena-specific tau/source screens are allowed.",
            "current_status": "BEST_NEXT_THEOREM_TARGET",
            "blocking_clauses": "source-leg owner and material/nuclear matrices are not closed; shared local projection queue selects this as next owner target",
            "source_paths": str(path_for("source-intake/clocks/branch_locked_local/shared_local_arena_projection_queue_nonclaim_2443.csv")),
            "theorem_zero": "false",
            "first_bound_fill_needed": "true",
            "valid_for_claim": "false",
            "next_action": "derive parent action-scale/measure/source-leg owner first",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "Z2675_4_verdict",
            "channel": "species plus clock",
            "candidate_theorem": "species_source_charge=0 and P_clock_alpha=0 are derived local-GR branch consequences",
            "exact_consequence": "R1 WEP and R2 clock channel no longer carry active qbar_XT debt",
            "current_status": "SPECIES_CLOCK_ZERO_NOT_PARENT_DERIVED",
            "blocking_clauses": "common measure/current owner; parent action scale; non-Hilbert bypass; tau/readout kernel; b_alpha owner",
            "source_paths": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2674_QBARXT_BOUND_TEMPLATE_NONCLAIM.csv")),
            "theorem_zero": "false",
            "first_bound_fill_needed": "true",
            "valid_for_claim": "false",
            "next_action": "repair missing species residual row and stage nonclaim clock product row",
            "timestamp_utc": stamp(),
        },
    ]


def species_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SSC2675_0_definition",
            "observable": "species_source_charge",
            "symbol": "epsilon_species_A",
            "formula": "epsilon_species_A := partial_A ln(mu_obs/M_inertial) after removing common-mode unit calibration",
            "candidate_value": "MISSING_PARENT_ZERO_OR_NUMERIC_EPSILON_A",
            "bound_or_scale": "2.8e-15",
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv")),
            "empirical_provenance": str(path_for("source-intake/wep-sources/1899/MICROSCOPE_final_results_arxiv_2209_15487.pdf")),
            "status": "DEFINITION_AND_BOUND_SCALE_NONCLAIM",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "choose reference/sum convention and derive parent zero or fill numeric epsilon_A with a source-independent parent coefficient",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "SSC2675_1_conditional_zero",
            "observable": "eta_source_AB",
            "symbol": "eta_source_AB",
            "formula": "eta_source_AB = epsilon_species_A - epsilon_species_B",
            "candidate_value": "ZERO_IF_PARENT_MEASURE_CURRENT_SOURCE_LABEL_THEOREM_SIGNED",
            "bound_or_scale": "2.8e-15",
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_minimal_parent_clause.csv")),
            "empirical_provenance": str(path_for("source-intake/wep-sources/1899/MICROSCOPE_final_results_arxiv_2209_15487.pdf")),
            "status": "CONDITIONAL_ZERO_ONLY",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "prove parent clause rather than importing the zero",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "SSC2675_2_TiPt_first_fill",
            "observable": "MICROSCOPE_WEP_TiPt",
            "symbol": "Delta_epsilon_TiPt",
            "formula": "Delta_epsilon_TiPt = sum_i DeltaQ_i(TiPt)*C_i + direct_source_shadow_projector_terms",
            "candidate_value": "MISSING_C_i_AND_OFFICIAL_SENSITIVITY_MAP",
            "bound_or_scale": "2.8e-15",
            "units": "dimensionless",
            "source_path": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/epsilon_A_bound_input_requirements_1451.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_finite_CX_contract_1911_nonclaim.csv")),
                ]
            ),
            "empirical_provenance": str(path_for("source-intake/wep-sources/1899/MICROSCOPE_final_results_arxiv_2209_15487.pdf")),
            "status": "FIRST_BOUND_FILL_NONCLAIM_MISSING_THEORY_VALUE",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "fill official Ti/Pt sensitivity map only after C_i parent coefficients are derived/declared",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "SSC2675_3_no_bound_inversion_guard",
            "observable": "species_source_charge",
            "symbol": "C_parent_WEP",
            "formula": "C_parent_WEP := normalized parent functional derivative or DERIVED_ZERO",
            "candidate_value": "MISSING_PARENT_COEFFICIENT",
            "bound_or_scale": "empirical bound cannot define C_parent_WEP",
            "units": "declared parent WEP basis",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_coupling_theorem_contract.csv")),
            "empirical_provenance": str(path_for("source-intake/wep-sources/1899/MICROSCOPE_final_results_arxiv_2209_15487.pdf")),
            "status": "BOUND_INVERSION_FORBIDDEN",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive C_parent_WEP from parent action object language or keep finite route nonclaim",
            "timestamp_utc": stamp(),
        },
    ]


def clock_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLK2675_0_clock_alpha_product",
            "observable": "clock_fine_structure",
            "symbol": "P_clock_alpha",
            "formula": "P_clock_alpha = DeltaK_alpha*b_alpha*tau_clock_time",
            "candidate_value": "MISSING_B_ALPHA_AND_TAU_CLOCK_TIME",
            "comparison_bound": "2.1e-18",
            "units": "yr^-1",
            "source_path": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/alpha_product_source_fill_nonclaim_1470.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/alpha_product_prediction_components_nonclaim_1471.csv")),
                ]
            ),
            "status": "COMPARISON_SIDE_FILLED_ONLY_NONCLAIM",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive b_alpha or tau_clock_time zero, or source both with units and readout convention",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "CLK2675_1_tau_readout",
            "observable": "clock_tau_projection",
            "symbol": "tau_clock_time",
            "formula": "tau_clock_time := d chi_X/dt_obs in the parent-selected local time projection",
            "candidate_value": "MISSING_PARENT_TAU_CLOCK_XHAT_MAP",
            "comparison_bound": "not directly scoreable",
            "units": "yr^-1 per normalized Xhat unit",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R10_1322_CLOCK_READOUT_GAP_LEDGER.csv")),
            "status": "TAU_MAP_MISSING_NONCLAIM",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive parent-selected observed time vector and clock normalization theorem",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "CLK2675_2_balpha_owner",
            "observable": "alpha_EM_readout",
            "symbol": "b_alpha",
            "formula": "b_alpha := d ln(alpha_EM)/dXhat or theorem-zero EM owner",
            "candidate_value": "MISSING_PARENT_ALPHA_OWNER_OR_THEOREM_ZERO",
            "comparison_bound": "not directly scoreable",
            "units": "dimensionless vertical derivative",
            "source_path": str(path_for("source-intake/mts_residuals/P8_Y5_R10_1396_ALPHAEM_WEP_CLOCK_R10_GATE.csv")),
            "status": "ALPHA_OWNER_UNSIGNED_NONCLAIM",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "prove no alpha_EM(X) vertex or keep alpha product finite/nonclaim",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "CLK2675_3_shared_source_leg",
            "observable": "shared_clock_WEP_source_leg",
            "symbol": "source_leg_owner",
            "formula": "same source leg must feed WEP, clocks, R10 and PPN without arena-specific screens",
            "candidate_value": "NEXT_TARGET_SOURCE_LEG_OWNER",
            "comparison_bound": "not directly scoreable",
            "units": "schema",
            "source_path": str(path_for("source-intake/clocks/branch_locked_local/shared_local_arena_projection_queue_nonclaim_2443.csv")),
            "status": "SHARED_OWNER_TARGET_NONCLAIM",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive parent action-scale/measure/source-leg owner",
            "timestamp_utc": stamp(),
        },
    ]


def first_bound_fill_rows(species_rows: list[dict[str, Any]], clock_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in species_rows:
        rows.append(
            {
                "fill_id": f"FILL2675_{row['row_id']}",
                "channel": "species_source_charge",
                "observable": row["observable"],
                "symbol": row["symbol"],
                "prediction_formula": row["formula"],
                "prediction_value": row["candidate_value"],
                "comparison_bound_or_scale": row["bound_or_scale"],
                "units": row["units"],
                "source_path": row["source_path"],
                "status": row["status"],
                "score_ready": row["score_ready"],
                "valid_prediction_row": row["valid_prediction_row"],
                "valid_for_claim": "false",
                "claim_allowed": "false",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    for row in clock_rows:
        rows.append(
            {
                "fill_id": f"FILL2675_{row['row_id']}",
                "channel": "clock_tau_readout",
                "observable": row["observable"],
                "symbol": row["symbol"],
                "prediction_formula": row["formula"],
                "prediction_value": row["candidate_value"],
                "comparison_bound_or_scale": row["comparison_bound"],
                "units": row["units"],
                "source_path": row["source_path"],
                "status": row["status"],
                "score_ready": row["score_ready"],
                "valid_prediction_row": row["valid_prediction_row"],
                "valid_for_claim": "false",
                "claim_allowed": "false",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    return rows


def runner_results_rows(proof_rows: list[dict[str, Any]], fill_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in proof_rows:
        rows.append(
            {
                "runner_id": f"RUN2675_{row['audit_id']}",
                "target_id": row["audit_id"],
                "stage": "zero_proof_audit",
                "has_parent_zero": row["theorem_zero"],
                "has_numeric_prediction": "false",
                "has_existing_source_path": as_bool(all(Path(p).exists() for p in row["source_paths"].split(";"))),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_ZERO_THEOREM_UNSIGNED",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    for row in fill_rows:
        rows.append(
            {
                "runner_id": f"RUN2675_{row['fill_id']}",
                "target_id": row["fill_id"],
                "stage": "first_bound_fill",
                "has_parent_zero": "false",
                "has_numeric_prediction": "false" if "MISSING" in row["prediction_value"] or "ZERO_IF" in row["prediction_value"] or "NEXT_TARGET" in row["prediction_value"] else "true",
                "has_existing_source_path": as_bool(all(Path(p).exists() for p in row["source_path"].split(";"))),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_NONCLAIM_MISSING_THEORY_VALUE_OR_PARENT_ZERO",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2675_0_species_zero",
            "claim": "epsilon_species_A=0 and eta_source_AB=0 are parent-derived",
            "status": "FAIL_COMMON_MEASURE_SOURCE_OWNER_UNSIGNED",
            "blocking_rows": "Z2675_0_species_conditional_theorem;Z2675_1_species_countermodel_filter",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2675_1_species_bound",
            "claim": "species source-charge row can be scored against WEP bound",
            "status": "FAIL_MISSING_PARENT_COEFFICIENT_AND_SENSITIVITY_MAP",
            "blocking_rows": "SSC2675_0_definition;SSC2675_2_TiPt_first_fill;SSC2675_3_no_bound_inversion_guard",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2675_2_clock_zero",
            "claim": "P_clock_alpha=0 is parent-derived",
            "status": "FAIL_TAU_READOUT_AND_ALPHA_OWNER_UNSIGNED",
            "blocking_rows": "Z2675_2_clock_conditional_theorem;CLK2675_1_tau_readout;CLK2675_2_balpha_owner",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2675_3_clock_bound",
            "claim": "clock product can be scored",
            "status": "FAIL_COMPARISON_SIDE_ONLY",
            "blocking_rows": "CLK2675_0_clock_alpha_product;CLK2675_1_tau_readout;CLK2675_2_balpha_owner",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2675_4_local_GR",
            "claim": "species/clock coupling silence supports local GR/PPN recovery",
            "status": "CLAIM_BLOCKED",
            "blocking_rows": "Z2675_4_verdict;CG2675_0_species_zero;CG2675_2_clock_zero",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2675_0_theorem_attempt",
            "question": "Can 2675 prove the species/clock local channel zeros?",
            "result": "no_current_parent_signature",
            "reason": "species route needs one parent action-scale/measure/current owner; clock route needs the same parent tau/readout kernel plus alpha owner",
            "action": "retain as conditional theorem only",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2675_1_missing_file_repair",
            "question": "Should the missing P8_species_source_charge_residual_or_zero.csv be created?",
            "result": "yes_nonclaim_row_created",
            "reason": "ledger referenced the row but it was absent; 2675 repairs plumbing while keeping claim gates closed",
            "action": str(OUTPUTS["species_residual"]),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2675_2_next_route",
            "question": "What is the best derivation target after 2675?",
            "result": "parent_action_scale_measure_owner",
            "reason": "this single theorem would kill species weights, source normalization leakage, and a major part of the clock/source-leg split",
            "action": "select 2676 parent action-scale/measure owner or countermodel bound",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2675_0_selected",
            "kind": "selected",
            "target_doc": "2676-Y5-R2FR-parent-action-scale-measure-owner-or-species-countermodel-bound.md",
            "target_script": "scripts/Y5_R2FR_parent_action_scale_measure_owner_or_species_countermodel_bound_2676.py",
            "purpose": "try to prove one parent action scale/measure/current owner for ordinary matter, or convert the surviving species countermodels into explicit nonclaim bound rows",
            "acceptance_gate": "parent-signed no independent species action weights/Jacobians/source rescalings/non-Hilbert bypass, or finite countermodel rows with units and source paths",
            "forbidden_shortcuts": "assuming EEP/WEP as an axiom; importing epsilon_A=0; using MICROSCOPE bound to define C_parent; assuming tau_clock=0; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "PS2675_0_scope",
            "field": "workspace_scope",
            "value": str(ROOT),
            "status": "private_post_checkpoint_only",
            "note": "no GitHub action and no formalization-workbench writes",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "PS2675_1_progress",
            "field": "coupling_gap",
            "value": "species/clock channel plumbing repaired and proof obligations sharpened",
            "status": "improved_not_claimed",
            "note": "missing species row is now present but nonclaim; clock has comparison side only",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "PS2675_2_next",
            "field": "next_derivation",
            "value": "parent_action_scale_measure_owner",
            "status": "selected",
            "note": "this is the central bottleneck for a derived local GR branch",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2675_0_wep_sources",
            "branch": "wep-sources",
            "source_table": rel_path(OUTPUTS["species_residual"]),
            "destination": str(BRANCH_OUTPUTS["wep_sources"]),
            "contents": "species source charge residual/zero file repaired as nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2675_1_microscope_coefficients",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["first_bound_fill"]),
            "destination": str(BRANCH_OUTPUTS["microscope_coefficients"]),
            "contents": "species/clock first bound fill rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2675_2_clock_branch",
            "branch": "clocks/branch_locked_local",
            "source_table": rel_path(OUTPUTS["clock_residual"]),
            "destination": str(BRANCH_OUTPUTS["clock_branch"]),
            "contents": "clock tau/readout residual rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2675_3_local_bounds",
            "branch": "local_bounds",
            "source_table": rel_path(OUTPUTS["first_bound_fill"]),
            "destination": str(BRANCH_OUTPUTS["local_bounds"]),
            "contents": "local species/clock bound-fill ledger retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2675_4_source_weight",
            "branch": "source-weight",
            "source_table": rel_path(OUTPUTS["first_bound_fill"]),
            "destination": str(BRANCH_OUTPUTS["source_weight"]),
            "contents": "source-weight species/clock bound-fill ledger retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    source_ok = all(row["exists"] == "true" and row["missing_needles"] == "" for row in rows["source_register"])
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2675_sources_exist_and_needles_found",
            "passed": as_bool(source_ok),
            "details": "all cited local source paths exist and required text needles are present; PDF source is existence-only",
        }
    )

    all_nonclaim = all(row.get("valid_for_claim") == "false" for table in rows.values() for row in table)
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2675_nonclaim_guard",
            "passed": as_bool(all_nonclaim),
            "details": "all generated rows carry valid_for_claim=false",
        }
    )

    proof_blocks = any(
        row["audit_id"] == "Z2675_4_verdict" and row["current_status"] == "SPECIES_CLOCK_ZERO_NOT_PARENT_DERIVED"
        for row in rows["proof_audit"]
    )
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2675_zero_proof_blocks_claim",
            "passed": as_bool(proof_blocks),
            "details": "species/clock zero theorem remains conditional-only",
        }
    )

    species_file_repaired = OUTPUTS["species_residual"].exists() and any(row["row_id"] == "SSC2675_2_TiPt_first_fill" for row in rows["species_residual"])
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2675_species_residual_file_repaired",
            "passed": as_bool(species_file_repaired),
            "details": "P8_species_source_charge_residual_or_zero.csv now exists with nonclaim first-fill row",
        }
    )

    clock_rows_ok = any(row["row_id"] == "CLK2675_0_clock_alpha_product" and row["comparison_bound"] == "2.1e-18" for row in rows["clock_residual"])
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2675_clock_comparison_side_retained_nonclaim",
            "passed": as_bool(clock_rows_ok),
            "details": "clock comparison side is retained while MTS b_alpha/tau value is missing",
        }
    )

    no_bound_inversion = any(row["row_id"] == "SSC2675_3_no_bound_inversion_guard" and row["status"] == "BOUND_INVERSION_FORBIDDEN" for row in rows["species_residual"])
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2675_no_bound_inversion_guard",
            "passed": as_bool(no_bound_inversion),
            "details": "empirical WEP bound is not used to define parent coefficient",
        }
    )

    runner_refuses = all(row["scored"] == "false" and row["claim_pass"] == "false" for row in rows["runner_results"])
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2675_runner_refuses_unsigned_rows",
            "passed": as_bool(runner_refuses),
            "details": "runner refuses scoring without parent zero or numeric MTS prediction",
        }
    )

    gates_blocked = any(row["gate_id"] == "CG2675_4_local_GR" and row["status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"])
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2675_local_GR_gate_blocked",
            "passed": as_bool(gates_blocked),
            "details": "local GR remains blocked by species/clock coupling gaps",
        }
    )

    next_selected = any(
        row["target_id"] == "NEXT2675_0_selected"
        and "2676-Y5-R2FR-parent-action-scale-measure-owner-or-species-countermodel-bound.md" in row["target_doc"]
        for row in rows["next_target"]
    )
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2675_next_target_selected",
            "passed": as_bool(next_selected),
            "details": "next target selects parent action-scale/measure owner",
        }
    )

    parse_results = [parse_csv(path) for path in csv_paths]
    csv_ok = all(result[0] and result[1] > 0 for result in parse_results)
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2675_csv_parse",
            "passed": as_bool(csv_ok),
            "details": "; ".join(f"{path.name}:{result[2]}:{result[1]}" for path, result in zip(csv_paths, parse_results)),
        }
    )

    branch_paths = [Path(row["destination"]) for row in rows["branch_copies"]]
    branch_parse = [parse_csv(path) for path in branch_paths]
    branch_ok = all(result[0] and result[1] > 0 for result in branch_parse)
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2675_branch_copies_parse",
            "passed": as_bool(branch_ok),
            "details": "; ".join(f"{path.name}:{result[2]}:{result[1]}" for path, result in zip(branch_paths, branch_parse)),
        }
    )

    generated_paths = [*csv_paths, *branch_paths, DOC_PATH]
    formalization_guard = all("formalization-workbench" not in str(path) for path in generated_paths)
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2675_formalization_write_guard",
            "passed": as_bool(formalization_guard),
            "details": "generated path allowlist excludes formalization-workbench",
        }
    )

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2675_pycache_absent_at_validation_time",
            "passed": as_bool(pycache_absent),
            "details": "scripts/__pycache__ absent when validation rows were produced",
        }
    )

    overall = all(row["passed"] == "true" for row in out if row["validation_id"] != "VAL2675_pycache_absent_at_validation_time")
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2675_OVERALL",
            "passed": as_bool(overall),
            "details": "2675 repairs the missing species residual file, keeps species/clock rows nonclaim, and selects parent action-scale/measure owner next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        f"# {CHECKPOINT} — Species/Clock Channel Zero Or First Bound Fill",
        "",
        "## Private Verdict",
        "",
        "This checkpoint tried the derivation path first. The clean theorem shape exists: one parent matter action, one measure/action scale, one source current, one clock/readout time. If that is parent-signed, species source charge and the clock alpha product can vanish for structural reasons.",
        "",
        "Current result: **not derived yet**. The species route is blocked by action-scale/measure/current ownership and non-Hilbert bypasses. The clock route is blocked by tau/readout and alpha-owner gaps. The useful progress is that the previously missing `P8_species_source_charge_residual_or_zero.csv` is now repaired as a nonclaim row, and the clock comparison side is kept separate from missing MTS dynamics.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["source_register"]),
        "",
        "## Zero Proof Audit",
        "",
        markdown_table(rows["proof_audit"]),
        "",
        "## Species Residual Or Zero",
        "",
        markdown_table(rows["species_residual"]),
        "",
        "## Clock Tau Readout Residual Or Zero",
        "",
        markdown_table(rows["clock_residual"]),
        "",
        "## First Bound Fill",
        "",
        markdown_table(rows["first_bound_fill"]),
        "",
        "## Runner Results",
        "",
        markdown_table(rows["runner_results"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(rows["claim_gates"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows["decision_ledger"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows["next_target"]),
        "",
        "## Project Status",
        "",
        markdown_table(rows["project_status"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(rows["branch_copies"]),
        "",
        "## Validation",
        "",
        markdown_table(rows["validation"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for path in [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)

    rows: dict[str, list[dict[str, Any]]] = {}
    rows["source_register"] = source_register_rows()
    rows["proof_audit"] = proof_audit_rows()
    rows["species_residual"] = species_residual_rows()
    rows["clock_residual"] = clock_residual_rows()
    rows["first_bound_fill"] = first_bound_fill_rows(rows["species_residual"], rows["clock_residual"])
    rows["runner_results"] = runner_results_rows(rows["proof_audit"], rows["first_bound_fill"])
    rows["claim_gates"] = claim_gate_rows()
    rows["decision_ledger"] = decision_rows()
    rows["next_target"] = next_target_rows()
    rows["project_status"] = project_status_rows()
    rows["branch_copies"] = branch_copy_rows()

    for name in [
        "source_register",
        "proof_audit",
        "species_residual",
        "clock_residual",
        "first_bound_fill",
        "runner_results",
        "claim_gates",
        "decision_ledger",
        "next_target",
        "project_status",
        "branch_copies",
    ]:
        write_csv(OUTPUTS[name], rows[name])

    write_csv(BRANCH_OUTPUTS["wep_sources"], rows["species_residual"])
    write_csv(BRANCH_OUTPUTS["microscope_coefficients"], rows["first_bound_fill"])
    write_csv(BRANCH_OUTPUTS["clock_branch"], rows["clock_residual"])
    write_csv(BRANCH_OUTPUTS["local_bounds"], rows["first_bound_fill"])
    write_csv(BRANCH_OUTPUTS["source_weight"], rows["first_bound_fill"])

    csv_paths = [OUTPUTS[name] for name in OUTPUTS if name != "validation"]
    rows["validation"] = validation_rows(rows, csv_paths)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
