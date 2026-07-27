from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2674"
BRANCH_ID = "Y5_R2FR_MATTER_MARKER_CHANNEL_DESCENT_OR_QBARXT_BOUND_ROW_2674"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"

DOC_PATH = ROOT / "2674-Y5-R2FR-matter-marker-channel-descent-or-qbarXT-bound-row.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2674_MATTER_CHANNEL_SOURCE_REGISTER.csv",
    "channel_audit": RESIDUALS / "P8_Y5_R2FR_2674_MATTER_CHANNEL_DESCENT_AUDIT.csv",
    "bound_template": RESIDUALS / "P8_Y5_R2FR_2674_QBARXT_BOUND_TEMPLATE_NONCLAIM.csv",
    "runner_results": RESIDUALS / "P8_Y5_R2FR_2674_CHANNEL_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2674_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2674_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2674_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2674_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2674_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "wep_queue": SOURCE_INTAKE / "wep-sources" / "P8_Y5_2674_SPECIES_CLOCK_CHANNEL_QUEUE_NONCLAIM.csv",
    "local_bounds": SOURCE_INTAKE / "local_bounds" / "Matter_marker_channel_qbarXT_2674_NONCLAIM.csv",
    "source_weight": SOURCE_INTAKE / "source-weight" / "MATTER_CHANNEL_QBARXT_BOUND_TEMPLATE_2674_NONCLAIM.csv",
    "microscope": SOURCE_INTAKE / "microscope" / "P8_Y5_2674_MATTER_CHANNELS.csv",
    "r10": SOURCE_INTAKE / "r10" / "P8_Y5_2674_CHANNEL_RUNNER_RESULTS.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2674_2673_CHANNEL_GAP",
        "relative_path": "2673-Y5-R2FR-JX-source-zero-or-qbarXT-first-coefficient-row.md",
        "required_needles": [
            "MAT2673_1_atomic_masses",
            "MAT2673_2_EM",
            "MAT2673_3_hidden_frame",
            "MAT2673_4_domain_projector",
            "QXT2673_0_qbarXT",
            "NEXT2673_0_selected",
        ],
        "purpose": "inherits the exact channel split and qbar_XT/J_X row contract from 2673",
        "used_for": "all 2674 matter-marker channel rows",
        "confidence": "local checkpoint source",
    },
    {
        "source_id": "SRC2674_WORLD_SOURCE_MEASURE",
        "relative_path": "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        "required_needles": [
            "PSC1016_1_single_observed_coframe",
            "PSC1016_7_coupling_descent_silence",
            "FIS1016_3_Delta_frame_source",
            "FIS1016_6_coupling_descent_certificate",
            "CG1016_5_coupling_descent_zero",
        ],
        "purpose": "tracks source/readout coframe mismatch and coupling descent leakage",
        "used_for": "source-measure/frame and hidden source rows",
        "confidence": "local checkpoint source",
    },
    {
        "source_id": "SRC2674_CLOCK_TAU_LOCK",
        "relative_path": "1002-Y5-R10-Bref-stationary-tau-theorem-or-Delta-ref-time-profile-row.md",
        "required_needles": [
            "STA1002_1_tau_identity",
            "STA1002_4_hamiltonian_clock_lock",
            "TPT1002_5_missing_clock_hamiltonian_lock",
            "CG1002_0_partial_t_Delta_ref_zero",
        ],
        "purpose": "prevents clock silence from being assumed without parent tau/clock lock",
        "used_for": "clock and tau_clock matter-channel rows",
        "confidence": "local checkpoint source",
    },
    {
        "source_id": "SRC2674_CONSTANT_SECTOR",
        "relative_path": "source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv",
        "required_needles": [
            "C0_constant_sector_definition",
            "C2_no_direct_constant_vertices",
            "C4_no_constant_running_from_local_MTS",
            "C6_measured_GM_absolute_calibration",
            "C7_empirical_fallback",
        ],
        "purpose": "separates ordinary representation constants from active source charges",
        "used_for": "atomic masses, alpha_EM, clock and source-normalization rows",
        "confidence": "source-intake contract",
    },
    {
        "source_id": "SRC2674_NO_SPECIES_SOURCE_CHARGE",
        "relative_path": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
        "required_needles": [
            "S1_matter_factorization",
            "S2_constant_sector_universality",
            "S4_source_normalization_species_blind",
            "S5_no_bulk_boundary_composition_charge",
        ],
        "purpose": "states the exact no-species-source-charge theorem that is still unsigned",
        "used_for": "WEP/species and atomic-mass channel rows",
        "confidence": "source-intake contract",
    },
    {
        "source_id": "SRC2674_EXTRA_CHANNEL_OWNER",
        "relative_path": "source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_OWNER_LEDGER.csv",
        "required_needles": [
            "species_source_charge",
            "epsilon_species_A",
            "domain_projector_mass",
            "retained_coefficient_required",
        ],
        "purpose": "identifies extra source channels that must be theorem-zero or bounded",
        "used_for": "species and domain/projector coefficient rows",
        "confidence": "source-intake ledger",
    },
    {
        "source_id": "SRC2674_EXTRA_CHANNEL_BOUNDS",
        "relative_path": "source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv",
        "required_needles": [
            "species_source_charge",
            "2.8e-15",
            "domain_projector_mass",
            "4e-20",
            "not_claimable",
        ],
        "purpose": "imports current nonclaim bound scales for source-side WEP and domain projector pressure",
        "used_for": "species and domain/projector bound template rows",
        "confidence": "source-intake bound summary",
    },
    {
        "source_id": "SRC2674_CLOCK_FILL_TEMPLATE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1321_CLOCK_FIRST_FILL_TEMPLATE.csv",
        "required_needles": [
            "CLK1321_0_direct_product",
            "CLK1321_1_factorized_product",
            "CLK1321_2_tau_readout",
            "CLK1321_3_clock_model",
        ],
        "purpose": "defines the first clock product formats that can eventually be scored",
        "used_for": "clock qbar_XT/tau_clock rows",
        "confidence": "source-intake template",
    },
    {
        "source_id": "SRC2674_CLOCK_GAP_LEDGER",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1322_CLOCK_READOUT_GAP_LEDGER.csv",
        "required_needles": [
            "GAP1322_0_chix_parent",
            "GAP1322_1_local_time_projection",
            "GAP1322_3_balpha",
            "GAP1322_4_stationary_tau",
        ],
        "purpose": "records missing alpha/clock readout descent pieces",
        "used_for": "clock and alpha_EM rows",
        "confidence": "source-intake gap ledger",
    },
    {
        "source_id": "SRC2674_ALPHAEM_CLOCK_GATE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1396_ALPHAEM_WEP_CLOCK_R10_GATE.csv",
        "required_needles": [
            "EMG1396_0_alphaEM",
            "EMG1396_2_clock",
            "BLOCKED_ALPHAEM_LOCK_UNSIGNED",
            "BLOCKED_CLOCK_PRODUCT_NONCLAIM",
        ],
        "purpose": "keeps alpha_EM and clock rows blocked until descent/product is real",
        "used_for": "EM/fine-structure and clock rows",
        "confidence": "source-intake gate",
    },
    {
        "source_id": "SRC2674_DOMAIN_NOVECTOR_ATTEMPT",
        "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
        "required_needles": [
            "T0_define_selector_vector_residual",
            "T4_R11_operator_silence",
            "T6_no_vector_verdict",
            "fail_current_corpus",
        ],
        "purpose": "prevents projector/domain selector silence from being smuggled in",
        "used_for": "domain/projector and preferred-frame rows",
        "confidence": "source-intake theorem attempt",
    },
    {
        "source_id": "SRC2674_DOMAIN_ALPHA_TEMPLATE",
        "relative_path": "source-intake/mts_residuals/P8_ALPHA3_DOMAIN_SIBLING_INPUT_TEMPLATE.csv",
        "required_needles": [
            "DSR_R5_alpha1_NUMERIC_OR_ZERO",
            "DSR_R6_alpha2_NUMERIC_OR_ZERO",
            "DSR_R7_alpha3_NUMERIC_OR_ZERO",
            "DSR_R8_xi_NUMERIC_OR_ZERO",
            "DSR_R11_EH_operator_ledger_NUMERIC_OR_ZERO",
        ],
        "purpose": "gives concrete domain/projector sibling coefficient slots and bounds",
        "used_for": "domain/projector bound template rows",
        "confidence": "source-intake template",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty table: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover - deliberately reports all parse failures.
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
            value = str(row.get(header, ""))
            value = value.replace("|", "\\|").replace("\n", "<br>")
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
                "used_for": spec["used_for"],
                "confidence": spec["confidence"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def channel_descent_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "CH2674_0_contract",
            "channel": "matter-channel theorem contract",
            "candidate_zero_statement": "For each matter/readout channel C, Lie_vX S_matter^C=0 at fixed q(Phi), e_obs, theta_univ and fixed source measure",
            "current_evidence": "2673 split qbar_XT/J_X into clocks, masses, EM, hidden frame and domain/projector channels",
            "missing_or_failure": "MISSING_PARENT_MATTER_DESCENT_FOR_EACH_CHANNEL",
            "source_paths": str(path_for("2673-Y5-R2FR-JX-source-zero-or-qbarXT-first-coefficient-row.md")),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "split qbar_XT into sourced channel coefficients instead of one vague coupling",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "CH2674_1_rods_clocks_photons",
            "channel": "rods/clocks/photons observed-frame channel",
            "candidate_zero_statement": "clock and photon readouts descend through the same observed coframe/metric and the same parent tau",
            "current_evidence": "single observed coframe is a contract; stationary tau and clock lock are unsigned",
            "missing_or_failure": "MISSING_TAU_CLOCK_LOCK_AND_FRAME_DESCENT",
            "source_paths": ";".join(
                [
                    str(path_for("1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md")),
                    str(path_for("1002-Y5-R10-Bref-stationary-tau-theorem-or-Delta-ref-time-profile-row.md")),
                    str(path_for("source-intake/mts_residuals/P8_Y5_R10_1321_CLOCK_FIRST_FILL_TEMPLATE.csv")),
                ]
            ),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "derive tau_source=tau_clock or fill tau_clock_time/b_alpha product with source path and units",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "CH2674_2_atomic_masses_species",
            "channel": "atomic masses, material constants, source composition",
            "candidate_zero_statement": "material constants and source normalization are species-blind representation data, not active X charges",
            "current_evidence": "no-species-source-charge contract exists; species_source_charge remains not parent-derived with 2.8e-15 nonclaim scale",
            "missing_or_failure": "MISSING_NO_SPECIES_MARKER_THEOREM",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv")),
                    str(path_for("source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_OWNER_LEDGER.csv")),
                    str(path_for("source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv")),
                ]
            ),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "attack species_source_charge first because it has the cleanest current bound pressure",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "CH2674_3_EM_fine_structure",
            "channel": "electromagnetic and fine-structure channel",
            "candidate_zero_statement": "alpha_EM and EM readout descend without an independent X-dependent alpha or F^2 vertex",
            "current_evidence": "alpha_EM gate says EM lock/readout descent and no-alpha vertex are unsigned",
            "missing_or_failure": "MISSING_EM_DESCENT_CERTIFICATE",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv")),
                    str(path_for("source-intake/mts_residuals/P8_Y5_R10_1396_ALPHAEM_WEP_CLOCK_R10_GATE.csv")),
                    str(path_for("source-intake/mts_residuals/P8_Y5_R10_1322_CLOCK_READOUT_GAP_LEDGER.csv")),
                ]
            ),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "either prove no alpha_EM(X) vertex from parent action or use clock/fine-structure coefficient row",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "CH2674_4_hidden_frame",
            "channel": "hidden conformal/disformal matter frame",
            "candidate_zero_statement": "the matter frame has no independent conformal/disformal X derivative beyond e_obs",
            "current_evidence": "source-measure contract admits hidden coupling descent leakage as a bound schema only",
            "missing_or_failure": "MISSING_HIDDEN_FRAME_ZERO_OR_COEFFICIENT",
            "source_paths": ";".join(
                [
                    str(path_for("2673-Y5-R2FR-JX-source-zero-or-qbarXT-first-coefficient-row.md")),
                    str(path_for("1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md")),
                ]
            ),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "write F_X_prime/disformal coefficient row unless parent action forbids the frame",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "CH2674_5_domain_projector",
            "channel": "domain/projector/source-label channel",
            "candidate_zero_statement": "domain selector produces no local vector, flux, anisotropy, or source-normalization operator",
            "current_evidence": "domain no-vector theorem attempt fails current corpus; alpha1/alpha2/alpha3/xi/R11 rows are templates",
            "missing_or_failure": "MISSING_DOMAIN_PROJECTOR_NO_LEAK_THEOREM",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv")),
                    str(path_for("source-intake/mts_residuals/P8_ALPHA3_DOMAIN_SIBLING_INPUT_TEMPLATE.csv")),
                ]
            ),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "keep domain projector rows nonclaim until vector/flux/aniso/operator coefficients are numeric or theorem-zero",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "CH2674_6_source_measure_frame",
            "channel": "source measure and readout-frame channel",
            "candidate_zero_statement": "source mass, matter stress, clocks, rods and orbital readout share one parent-selected frame and measure",
            "current_evidence": "Delta_frame_source and coupling_descent_certificate are explicit first-input placeholders",
            "missing_or_failure": "MISSING_SAME_FRAME_SOURCE_MEASURE_THEOREM",
            "source_paths": str(path_for("1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md")),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "derive same-frame measure from parent symplectic/Hilbert source or fill Delta_frame_source bound",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "CH2674_7_verdict",
            "channel": "all matter-marker channels",
            "candidate_zero_statement": "qbar_XT=0 and J_X=0 follow from channel descent",
            "current_evidence": "every channel has a precise owner but at least one parent signature is missing in each route",
            "missing_or_failure": "MATTER_CHANNEL_DESCENT_NOT_PARENT_DERIVED",
            "source_paths": str(path_for("2673-Y5-R2FR-JX-source-zero-or-qbarXT-first-coefficient-row.md")),
            "theorem_zero": "false",
            "bound_row_required": "true",
            "valid_for_claim": "false",
            "next_action": "move to species/clock channel first because it has existing WEP/clock pressure rows",
            "timestamp_utc": stamp(),
        },
    ]


def qbarxt_bound_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "BND2674_0_qbarXT_master",
            "channel": "master test-body coupling",
            "coefficient_symbol": "qbar_XT",
            "prediction_form": "alpha_R10(lambda_X)=K_X*Qbar_XH(lambda_X)*qbar_XT*tau_R10 + alpha_tail_abs + alpha_hidden_abs + alpha_shadow_abs",
            "observable_family": "R10 fifth force; local-GR coupling silence",
            "required_parent_zero": "Lie_vX S_matter=0 for all active matter-marker channels",
            "required_numeric_inputs": "K_X; Qbar_XH(lambda_X); qbar_XT; tau_R10; alpha_tail_abs; bound_curve(lambda_X); normalization",
            "current_bound_or_scale": "MISSING_FULL_NUMERIC_PRODUCT",
            "units": "dimensionless unless declared otherwise by parent normalization",
            "source_paths": str(path_for("2673-Y5-R2FR-JX-source-zero-or-qbarXT-first-coefficient-row.md")),
            "status": "template_nonclaim",
            "valid_for_claim": "false",
            "next_action": "fill channel coefficients or prove all channel zeros",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "BND2674_1_clock",
            "channel": "clock/time readout",
            "coefficient_symbol": "b_alpha*tau_clock_time or P_clock_alpha",
            "prediction_form": "Delta clock ratio = P_clock_alpha or b_alpha*tau_clock_time in the same readout convention as the source bound",
            "observable_family": "R2 clock redshift; alpha drift/fine-structure clocks",
            "required_parent_zero": "tau_source=tau_clock and stationary local readout silence",
            "required_numeric_inputs": "clock pair; DeltaK_alpha; b_alpha; tau_clock_time; units; source path; equation ref",
            "current_bound_or_scale": "bound-row template exists; MTS product missing",
            "units": "clock/frequency fractional units or declared readout units",
            "source_paths": ";".join(
                [
                    str(path_for("1002-Y5-R10-Bref-stationary-tau-theorem-or-Delta-ref-time-profile-row.md")),
                    str(path_for("source-intake/mts_residuals/P8_Y5_R10_1321_CLOCK_FIRST_FILL_TEMPLATE.csv")),
                    str(path_for("source-intake/mts_residuals/P8_Y5_R10_1322_CLOCK_READOUT_GAP_LEDGER.csv")),
                ]
            ),
            "status": "template_nonclaim",
            "valid_for_claim": "false",
            "next_action": "derive clock tau lock or fill direct/factorized clock product",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "BND2674_2_species",
            "channel": "species/source-composition",
            "coefficient_symbol": "epsilon_species_A or eta_source_AB",
            "prediction_form": "eta_source_AB = Delta_A ln(mu_obs/M_inertial) - Delta_B ln(mu_obs/M_inertial)",
            "observable_family": "R1 WEP source charge; source-side WEP",
            "required_parent_zero": "source normalization species-blind and no bulk/boundary composition charge",
            "required_numeric_inputs": "test compositions; epsilon_species_A; epsilon_species_B; normalization; source path; equation ref",
            "current_bound_or_scale": "2.8e-15 dimensionless scale from existing nonclaim bound summary",
            "units": "dimensionless",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv")),
                    str(path_for("source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_OWNER_LEDGER.csv")),
                    str(path_for("source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv")),
                ]
            ),
            "status": "template_nonclaim",
            "valid_for_claim": "false",
            "next_action": "this is the best next bite: prove species-blind source action or fill epsilon_species_A",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "BND2674_3_EM_alpha",
            "channel": "EM/fine-structure",
            "coefficient_symbol": "b_alpha_EM or partial_X ln(alpha_EM)",
            "prediction_form": "Delta alpha_EM/alpha_EM = b_alpha_EM * tau_clock_time or direct EM readout kernel",
            "observable_family": "fine-structure clocks; EM descent",
            "required_parent_zero": "no alpha_EM(X)F^2 vertex and EM readout descends through e_obs/q(Phi)",
            "required_numeric_inputs": "b_alpha_EM; tau_clock_time; readout kernel; units; clock sensitivity; source path",
            "current_bound_or_scale": "BLOCKED_ALPHAEM_LOCK_UNSIGNED",
            "units": "fractional alpha or declared readout units",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/mts_residuals/P8_Y5_R10_1396_ALPHAEM_WEP_CLOCK_R10_GATE.csv")),
                    str(path_for("source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv")),
                ]
            ),
            "status": "template_nonclaim",
            "valid_for_claim": "false",
            "next_action": "prove EM descent or keep alpha_EM as a separate coefficient row",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "BND2674_4_hidden_frame",
            "channel": "hidden conformal/disformal frame",
            "coefficient_symbol": "F_X_prime; D_X; C_X",
            "prediction_form": "qbar_XT_hidden = d ln C_X/dX + matter-stress projection of D_X plus normalization terms",
            "observable_family": "R10; PPN; WEP; clock readouts",
            "required_parent_zero": "matter frame equals observed frame with no independent X derivative",
            "required_numeric_inputs": "C_X derivative; D_X coefficient; stress projection; units; source path",
            "current_bound_or_scale": "MISSING_HIDDEN_FRAME_COEFFICIENT",
            "units": "declared frame-normalization units",
            "source_paths": ";".join(
                [
                    str(path_for("2673-Y5-R2FR-JX-source-zero-or-qbarXT-first-coefficient-row.md")),
                    str(path_for("1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md")),
                ]
            ),
            "status": "template_nonclaim",
            "valid_for_claim": "false",
            "next_action": "derive absence of hidden frame or fill frame derivative coefficient",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "BND2674_5_domain_projector",
            "channel": "domain/projector preferred-frame/location",
            "coefficient_symbol": "W_domain_alpha1; W_domain_alpha2; W_domain_alpha3; W_domain_xi; c_domain_source_normalization_operator",
            "prediction_form": "PPN/operator rows = domain coefficient times vector/flux/aniso/source-normalization selector residual",
            "observable_family": "R5 alpha1; R6 alpha2; R7 alpha3; R8 xi; R11 operator ledger",
            "required_parent_zero": "domain selector has no local vector, flux, anisotropy, or source-normalization operator",
            "required_numeric_inputs": "domain coefficient; selector residual; normalization; source path; formula reference",
            "current_bound_or_scale": "alpha3 sibling bound scale 4e-20; all template_unfilled",
            "units": "dimensionless_or_declared_operator_units",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv")),
                    str(path_for("source-intake/mts_residuals/P8_ALPHA3_DOMAIN_SIBLING_INPUT_TEMPLATE.csv")),
                    str(path_for("source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv")),
                ]
            ),
            "status": "template_nonclaim",
            "valid_for_claim": "false",
            "next_action": "do not use covariance alone; prove no-vector/no-flux/no-aniso or fill coefficients",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "BND2674_6_source_frame",
            "channel": "source-measure/readout-frame",
            "coefficient_symbol": "Delta_frame_source; B_obs_source_measure_over_MH",
            "prediction_form": "epsilon_selector includes absolute source-frame and coupling-descent leakage terms",
            "observable_family": "Newton/PPN/local-GR source normalization",
            "required_parent_zero": "same observed frame/measure for matter source, clocks, rods, orbit and source mass",
            "required_numeric_inputs": "source_frame; readout_frame; Delta_frame_source; M_H_ref; local lock; source path",
            "current_bound_or_scale": "MISSING_FRAME_BOUND_OR_THEOREM",
            "units": "dimensionless or normalized by M_H_ref",
            "source_paths": str(path_for("1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md")),
            "status": "template_nonclaim",
            "valid_for_claim": "false",
            "next_action": "derive same-frame Hilbert/Hamiltonian source measure or fill frame leakage row",
            "timestamp_utc": stamp(),
        },
        {
            "row_id": "BND2674_7_no_cancellation",
            "channel": "absolute no-cancellation envelope",
            "coefficient_symbol": "abs_channel_sum",
            "prediction_form": "abs_total >= abs(clock)+abs(species)+abs(EM)+abs(hidden_frame)+abs(domain)+abs(source_frame)+abs(tail)",
            "observable_family": "all local arenas",
            "required_parent_zero": "every non-GR channel individually theorem-zero",
            "required_numeric_inputs": "absolute value of every channel coefficient and bound curve/arena threshold",
            "current_bound_or_scale": "NOT_COMPUTED_COMPONENTS_MISSING",
            "units": "arena-dependent, with explicit normalization",
            "source_paths": str(path_for("2673-Y5-R2FR-JX-source-zero-or-qbarXT-first-coefficient-row.md")),
            "status": "template_nonclaim",
            "valid_for_claim": "false",
            "next_action": "score only after each channel has a sourced coefficient or theorem-zero",
            "timestamp_utc": stamp(),
        },
    ]


def runner_results_rows(audit_rows: list[dict[str, Any]], bound_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in audit_rows:
        missing = row["theorem_zero"] != "true" or row["bound_row_required"] == "true"
        rows.append(
            {
                "runner_id": f"RUN2674_{row['audit_id']}",
                "target_id": row["audit_id"],
                "stage": "channel_descent_audit",
                "has_parent_zero": row["theorem_zero"],
                "has_numeric_bound": "false",
                "has_existing_source_path": as_bool(all(Path(p).exists() for p in row["source_paths"].split(";"))),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_CHANNEL_DESCENT_UNSIGNED" if missing else "REFUSED_NONCLAIM_GUARD",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    for row in bound_rows:
        rows.append(
            {
                "runner_id": f"RUN2674_{row['row_id']}",
                "target_id": row["row_id"],
                "stage": "qbarXT_bound_template",
                "has_parent_zero": "false",
                "has_numeric_bound": "false",
                "has_existing_source_path": as_bool(all(Path(p).exists() for p in row["source_paths"].split(";"))),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_TEMPLATE_NONCLAIM_MISSING_NUMERIC_PARENT_INPUTS",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2674_0_matter_channel_zero",
            "claim": "all matter-marker channels theorem-zero",
            "status": "FAIL_CHANNEL_DESCENT_UNSIGNED",
            "blocking_rows": "CH2674_1_rods_clocks_photons;CH2674_2_atomic_masses_species;CH2674_3_EM_fine_structure;CH2674_4_hidden_frame;CH2674_5_domain_projector;CH2674_6_source_measure_frame",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2674_1_qbarXT_bound_ready",
            "claim": "qbar_XT can be numerically scored",
            "status": "FAIL_BOUND_TEMPLATE_NONCLAIM",
            "blocking_rows": "BND2674_0_qbarXT_master;BND2674_7_no_cancellation",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2674_2_clock_WEP_EM_ready",
            "claim": "clock/WEP/EM local channels are silent or bounded",
            "status": "FAIL_CLOCK_SPECIES_EM_UNSIGNED",
            "blocking_rows": "BND2674_1_clock;BND2674_2_species;BND2674_3_EM_alpha",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2674_3_R10_alpha_ready",
            "claim": "R10 alpha row can score local fifth-force safety",
            "status": "FAIL_MISSING_KX_QBARXT_TAU_AND_NO_CANCELLATION",
            "blocking_rows": "BND2674_0_qbarXT_master;BND2674_4_hidden_frame;BND2674_7_no_cancellation",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2674_4_local_GR",
            "claim": "local GR/PPN branch follows from matter-channel silence",
            "status": "CLAIM_BLOCKED",
            "blocking_rows": "CH2674_7_verdict;CG2674_0_matter_channel_zero;CG2674_1_qbarXT_bound_ready",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2674_0_zero_proof_attempt",
            "question": "Can 2674 prove qbar_XT=0 by matter-channel descent?",
            "result": "no_current_parent_proof",
            "reason": "every route has a precise owner but the parent signatures for tau lock, species blindness, EM descent, hidden frame and domain/projector silence are not all present",
            "action": "do not promote local-GR or R10 pass",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2674_1_bound_route",
            "question": "Can 2674 improve the work anyway?",
            "result": "yes_channel_bound_rows_are_now_split",
            "reason": "qbar_XT is no longer one ghost variable; it is decomposed into clock, species, EM, hidden-frame, domain and source-frame rows",
            "action": "use these rows as the next runner interface",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2674_2_next_route",
            "question": "Which channel should be attacked first?",
            "result": "species_clock_first",
            "reason": "species_source_charge has an existing dimensionless nonclaim scale and clock rows already define product formats; this is the least foggy route",
            "action": "select 2675 species/clock zero-or-bound target",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2674_0_selected",
            "kind": "selected",
            "target_doc": "2675-Y5-R2FR-species-clock-channel-zero-or-first-bound-fill.md",
            "target_script": "scripts/Y5_R2FR_species_clock_channel_zero_or_first_bound_fill_2675.py",
            "purpose": "try to prove species_source_charge=0 and tau/clock silence first, or fill the first source-backed species/clock coefficient rows",
            "acceptance_gate": "either parent-signed species/clock zero theorem or nonclaim numeric rows with units, source paths, equation refs and no-cancellation guard",
            "forbidden_shortcuts": "universal WEP wording as proof; assuming clock tau lock; using alpha_EM lock as proof; invented coefficients; R10/local-GR claim; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "PS2674_0_scope",
            "field": "workspace_scope",
            "value": str(ROOT),
            "status": "private_post_checkpoint_only",
            "note": "no GitHub action and no formalization-workbench writes",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "PS2674_1_overall",
            "field": "local_GR_route",
            "value": "coupling/matter-channel route still blocked but now decomposed",
            "status": "improved_not_claimed",
            "note": "this is a real narrowing of the coupling gap, not a pass",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "PS2674_2_best_next_bite",
            "field": "next_derivation",
            "value": "species_clock_first",
            "status": "selected",
            "note": "strongest pressure and clearest rows are WEP/species and clock products",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2674_0_wep_queue",
            "branch": "wep-sources",
            "source_table": rel_path(OUTPUTS["bound_template"]),
            "destination": str(BRANCH_OUTPUTS["wep_queue"]),
            "contents": "species/clock subset queue retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2674_1_local_bounds",
            "branch": "local_bounds",
            "source_table": rel_path(OUTPUTS["bound_template"]),
            "destination": str(BRANCH_OUTPUTS["local_bounds"]),
            "contents": "all qbar_XT channel bound templates retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2674_2_source_weight",
            "branch": "source-weight",
            "source_table": rel_path(OUTPUTS["bound_template"]),
            "destination": str(BRANCH_OUTPUTS["source_weight"]),
            "contents": "source-weight/coupling coefficient template retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2674_3_microscope",
            "branch": "microscope",
            "source_table": rel_path(OUTPUTS["channel_audit"]),
            "destination": str(BRANCH_OUTPUTS["microscope"]),
            "contents": "matter-channel audit mirror retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2674_4_r10_runner",
            "branch": "r10",
            "source_table": rel_path(OUTPUTS["runner_results"]),
            "destination": str(BRANCH_OUTPUTS["r10"]),
            "contents": "channel runner refusals retained nonclaim",
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
            "validation_id": "VAL2674_sources_exist_and_needles_found",
            "passed": as_bool(source_ok),
            "details": "all cited local source paths exist and required needles are present",
        }
    )

    all_nonclaim = all(row.get("valid_for_claim") == "false" for table in rows.values() for row in table)
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2674_nonclaim_guard",
            "passed": as_bool(all_nonclaim),
            "details": "all generated evidence rows are valid_for_claim=false",
        }
    )

    channel_verdict = any(
        row["audit_id"] == "CH2674_7_verdict"
        and row["missing_or_failure"] == "MATTER_CHANNEL_DESCENT_NOT_PARENT_DERIVED"
        and row["valid_for_claim"] == "false"
        for row in rows["channel_audit"]
    )
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2674_channel_verdict_blocks_claim",
            "passed": as_bool(channel_verdict),
            "details": "matter-channel theorem zero is explicitly rejected as current claim",
        }
    )

    bound_rows_ok = (
        len(rows["bound_template"]) >= 8
        and all(row["status"] == "template_nonclaim" for row in rows["bound_template"])
        and any(row["row_id"] == "BND2674_2_species" and "2.8e-15" in row["current_bound_or_scale"] for row in rows["bound_template"])
        and any(row["row_id"] == "BND2674_7_no_cancellation" for row in rows["bound_template"])
    )
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2674_bound_templates_complete_nonclaim",
            "passed": as_bool(bound_rows_ok),
            "details": "qbar_XT master, clock, species, EM, hidden-frame, domain, source-frame and no-cancellation rows exist",
        }
    )

    runner_refuses = all(row["scored"] == "false" and row["claim_pass"] == "false" for row in rows["runner_results"])
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2674_runner_refuses_unsigned_rows",
            "passed": as_bool(runner_refuses),
            "details": "runner results refuse scoring while parent zero/numeric inputs are missing",
        }
    )

    gates_blocked = any(
        row["gate_id"] == "CG2674_4_local_GR" and row["status"] == "CLAIM_BLOCKED"
        for row in rows["claim_gates"]
    )
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2674_local_GR_gate_blocked",
            "passed": as_bool(gates_blocked),
            "details": "local-GR/PPN branch stays blocked by coupling descent",
        }
    )

    next_selected = any(
        row["target_id"] == "NEXT2674_0_selected"
        and "2675-Y5-R2FR-species-clock-channel-zero-or-first-bound-fill.md" in row["target_doc"]
        for row in rows["next_target"]
    )
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2674_next_target_selected",
            "passed": as_bool(next_selected),
            "details": "next target selects species/clock zero-or-bound fill",
        }
    )

    parse_results = [parse_csv(path) for path in csv_paths]
    csv_ok = all(result[0] and result[1] > 0 for result in parse_results)
    parse_detail = "; ".join(f"{path.name}:{result[2]}:{result[1]}" for path, result in zip(csv_paths, parse_results))
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2674_csv_parse",
            "passed": as_bool(csv_ok),
            "details": parse_detail,
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
            "validation_id": "VAL2674_branch_copies_parse",
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
            "validation_id": "VAL2674_formalization_write_guard",
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
            "validation_id": "VAL2674_pycache_absent_at_validation_time",
            "passed": as_bool(pycache_absent),
            "details": "scripts/__pycache__ absent when validation rows were produced",
        }
    )

    overall = all(row["passed"] == "true" for row in out if row["validation_id"] != "VAL2674_pycache_absent_at_validation_time")
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2674_OVERALL",
            "passed": as_bool(overall),
            "details": "2674 decomposes matter-marker qbar_XT channels, refuses claims, and selects species/clock as next derivation target",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        f"# {CHECKPOINT} — Matter-Marker Channel Descent Or qbar_XT Bound Row",
        "",
        "## Private Verdict",
        "",
        "This checkpoint does **not** prove local-GR recovery. It does something useful but less glamorous: it turns the vague coupling gap into named matter-channel owners. The boxer is still on his feet, but no belt is being claimed from this round.",
        "",
        "The attempted theorem-zero is:",
        "",
        "`For every matter/readout channel C, Lie_vX S_matter^C = 0 at fixed q(Phi), e_obs, theta_univ, source measure, and parent tau.`",
        "",
        "Current result: the theorem is clean as a contract, but it is not parent-signed in the corpus. Therefore `qbar_XT=0`, `J_X=0`, R10 safety, WEP safety, clock safety, and local-GR/PPN recovery stay blocked.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["source_register"]),
        "",
        "## Channel Descent Audit",
        "",
        markdown_table(rows["channel_audit"]),
        "",
        "## qbar_XT Bound Templates",
        "",
        markdown_table(rows["bound_template"]),
        "",
        "## Channel Runner Results",
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
    rows["channel_audit"] = channel_descent_audit_rows()
    rows["bound_template"] = qbarxt_bound_template_rows()
    rows["runner_results"] = runner_results_rows(rows["channel_audit"], rows["bound_template"])
    rows["claim_gates"] = claim_gate_rows()
    rows["decision_ledger"] = decision_rows()
    rows["next_target"] = next_target_rows()
    rows["project_status"] = project_status_rows()
    rows["branch_copies"] = branch_copy_rows()

    for name in [
        "source_register",
        "channel_audit",
        "bound_template",
        "runner_results",
        "claim_gates",
        "decision_ledger",
        "next_target",
        "project_status",
        "branch_copies",
    ]:
        write_csv(OUTPUTS[name], rows[name])

    write_csv(BRANCH_OUTPUTS["wep_queue"], [row for row in rows["bound_template"] if row["row_id"] in {"BND2674_1_clock", "BND2674_2_species"}])
    write_csv(BRANCH_OUTPUTS["local_bounds"], rows["bound_template"])
    write_csv(BRANCH_OUTPUTS["source_weight"], rows["bound_template"])
    write_csv(BRANCH_OUTPUTS["microscope"], rows["channel_audit"])
    write_csv(BRANCH_OUTPUTS["r10"], rows["runner_results"])

    csv_paths = [OUTPUTS[name] for name in OUTPUTS if name != "validation"]
    rows["validation"] = validation_rows(rows, csv_paths)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
