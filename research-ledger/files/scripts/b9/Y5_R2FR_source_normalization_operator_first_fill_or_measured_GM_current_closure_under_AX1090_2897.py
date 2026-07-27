from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2897-Y5-R2FR-source-normalization-operator-first-fill-or-measured-GM-current-closure-under-AX1090.md"

SRC_2896_DOC = ROOT / "2896-Y5-R2FR-source-normalized-Newton-beta-envelope-or-first-R11-fill-under-AX1090.md"
SRC_2896_NEXT = RESIDUALS / "P8_Y5_R2FR_2896_NEXT_TARGET.csv"
SRC_2896_NEWTON = RESIDUALS / "P8_Y5_R2FR_2896_SOURCE_NORMALIZED_NEWTON_PRECONDITION_GATE.csv"
SRC_2896_FIRSTFILL = RESIDUALS / "P8_Y5_R2FR_2896_FIRST_R11_FILL_QUEUE.csv"
SRC_532_DOC = ROOT / "532-Y5-measured-GM-source-current-closure-or-first-input-fill.md"
SRC_523_DOC = ROOT / "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md"
SRC_520_DOC = ROOT / "520-Y5-source-current-Ward-closure-or-bound-row.md"
SRC_522_DOC = ROOT / "522-Y5-extra-mass-projection-silence-or-channelwise-bound.md"
SRC_505_DOC = ROOT / "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md"
SRC_499_DOC = ROOT / "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md"
SRC_SOURCE_SCORE = RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv"
SRC_R11_STATUS = RESIDUALS / "R11_EXECUTABLE_VECTOR_STATUS.csv"
SRC_R11_SKELETON = RESIDUALS / "R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv"
SRC_WARD_BRIDGE = RESIDUALS / "P8_Y5_SOURCE_CURRENT_WARD_BRIDGE.csv"
SRC_WARD_OBSTRUCTION = RESIDUALS / "P8_Y5_WARD_TO_MASS_FLUX_OBSTRUCTION.csv"
SRC_MEFF_UPDATE = RESIDUALS / "P8_Y5_MEFF_FLUX_BOUND_UPDATE.csv"
SRC_PIM_INPUT = RESIDUALS / "P8_Y5_PIM_RADIAL_BOUND_INPUT.csv"
SRC_EXTRA_MASS = RESIDUALS / "P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv"
SRC_PG_CONTRACT = RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv"
SRC_SN_STACK = RESIDUALS / "P8_source_normalized_Newton_branch_STACK.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2897_SOURCE_REGISTER.csv",
    "closure": RESIDUALS / "P8_Y5_R2FR_2897_MEASURED_GM_CLOSURE_ATTEMPT.csv",
    "operator": RESIDUALS / "P8_Y5_R2FR_2897_SOURCE_NORMALIZATION_OPERATOR_ROW_NONCLAIM.csv",
    "residuals": RESIDUALS / "P8_Y5_R2FR_2897_SOURCE_RESIDUAL_FIRST_FILL_ROWS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2897_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2897_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2897_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2897_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2897_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2897_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "operator_copy": BETA_DOCS / "RAB_SOURCE_NORMALIZATION_OPERATOR_ROW_2897_NONCLAIM.csv",
    "residuals_copy": BETA_DOCS / "RAB_SOURCE_RESIDUAL_FIRST_FILL_ROWS_2897_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2897_epsilon_charge_theorem_or_component_envelope_NEXT.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2897_0_2896_doc", SRC_2896_DOC, "source-normalization operator / measured-GM current chain;NEXT2896_0_2897", "2896 selected source-normalization as the first-fill target"),
        ("SRC2897_1_2896_next", SRC_2896_NEXT, "NEXT2896_0_2897;source-normalization", "machine-readable 2897 handoff"),
        ("SRC2897_2_2896_newton_gate", SRC_2896_NEWTON, "NG2896_1_measured_GM;FAIL", "source-normalized Newton precondition currently fails closed"),
        ("SRC2897_3_2896_firstfill", SRC_2896_FIRSTFILL, "FILL2896_0_source_normalization_operator;highest", "source-normalization operator is highest-priority R11 family"),
        ("SRC2897_4_532_doc", SRC_532_DOC, "epsilon_charge = (B_xi/G_eff - M_H[Pi_M J_H]) / M_H;Current MTS does not yet satisfy that route", "exact epsilon_charge closure attempt and first input slot"),
        ("SRC2897_5_523_doc", SRC_523_DOC, "mu_obs=G_eff M_H + mu_extra + Delta_mu_Gauss + Delta_mu_readout;SRC523_0_charge_current_normalization", "Gauss/orbital source-normalization chain and scorecard"),
        ("SRC2897_6_520_doc", SRC_520_DOC, "d(Pi_M J_H)=0;Ward conservation alone does not prove that", "Ward bridge and projected mass-current obstruction"),
        ("SRC2897_7_522_doc", SRC_522_DOC, "Pi_M dJ_extra = 0;not_derived_not_filled", "extra projected mass-channel obstruction"),
        ("SRC2897_8_505_doc", SRC_505_DOC, "T505_conditional_Noether_mass_charge_closure;premises_not_yet_parent_derived", "conditional Noether mass-charge closure theorem"),
        ("SRC2897_9_499_doc", SRC_499_DOC, "d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent", "source identity decomposition for closed Pi_M flux"),
        ("SRC2897_10_source_score", SRC_SOURCE_SCORE, "SRC523_0_charge_current_normalization;SRC523_11_total_no_cancellation_score", "canonical source-normalization residual scorecard"),
        ("SRC2897_11_r11_status", SRC_R11_STATUS, "source_normalization_operator;template_only_retained_core_blocker", "R11 status keeps source-normalization as retained core blocker"),
        ("SRC2897_12_r11_skeleton", SRC_R11_SKELETON, "source_normalization_operator;MISSING_MU_EXTRA_OVER_GEFF_MEFF_AND_DERIVATIVE_NORMALIZATION", "minimum executable vector skeleton"),
        ("SRC2897_13_ward_bridge", SRC_WARD_BRIDGE, "WB520_3_projected_mass_current;WB520_4_exact_product_obstruction", "machine-readable Ward bridge"),
        ("SRC2897_14_ward_obstruction", SRC_WARD_OBSTRUCTION, "WO520_1_PiM_not_parent_owned;WO520_3_extra_mass_projection", "machine-readable obstruction ledger"),
        ("SRC2897_15_meff_update", SRC_MEFF_UPDATE, "Y5B_1_Meff_conservation;Y5B_2_radial_source_hair", "M_eff flux bound update rows"),
        ("SRC2897_16_pim_input", SRC_PIM_INPUT, "PI521_0_Delta_PiM;PI521_4_radial_decision", "Pi_M radial/projector input slots"),
        ("SRC2897_17_extra_mass", SRC_EXTRA_MASS, "EX522_0_boundary_improvement;EX522_7_parent_anomaly_multiplier", "extra mass channelwise inputs"),
        ("SRC2897_18_pg_contract", SRC_PG_CONTRACT, "PG1_charge_equals_projected_Hilbert_source;PG4_Gauss_surface_integral", "Hamiltonian charge to Poisson/Gauss contract"),
        ("SRC2897_19_sn_stack", SRC_SN_STACK, "SN3_charge_equals_Hilbert_mass_current;SN11", "source-normalized Newton theorem stack"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def closure_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "GM2897_0_observed_time_charge",
            "observed-time Hamiltonian charge exists before orbit fitting",
            "H_xi = B_xi on shell, xi normalized in observed frame",
            "SN2;PG0;SC532_0",
            "conditional_not_parent_derived",
            "without this, B_xi/G_eff is not a measured source mass candidate",
        ),
        (
            "GM2897_1_same_frame_Hilbert_source",
            "same observed coframe defines the Hilbert source current",
            "J_H[tau] = T_m^{mu nu}[e_obs] tau_nu dSigma_mu",
            "WB520_0;SC532_1",
            "conditional_source_current_defined_not_mass_flux_closed",
            "gives a real source current but not a closed mass channel",
        ),
        (
            "GM2897_2_charge_current_equality",
            "Hamiltonian charge equals projected Hilbert mass current",
            "B_xi/G_eff = M_H[Pi_M J_H]",
            "PG1;SN3;SRC523_0;SC532_2",
            "not_parent_derived",
            "this is exactly epsilon_charge=0 and is the first active blocker",
        ),
        (
            "GM2897_3_parent_owned_PiM",
            "Pi_M is parent-owned charge data, not a post-readout mask",
            "Pi_M J = ell_M(J) omega_M_top or equivalent parent projector",
            "SC532_3;WO520_1;PI521_0",
            "not_parent_derived",
            "a readout projector cannot explain the measured source charge",
        ),
        (
            "GM2897_4_projector_commutator_silence",
            "projected current has no product-rule leakage",
            "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H with [d,Pi_M]J_H=0",
            "SC532_4;WB520_4;PI521_1",
            "not_derived",
            "commutator leakage becomes radial source hair and projector stress",
        ),
        (
            "GM2897_5_zero_extra_projection",
            "non-Hilbert/boundary/domain/memory/non-EH/coupling/frame/projector/anomaly channels carry no Pi_M mass projection",
            "Pi_M dJ_extra_i=0 channelwise",
            "SC532_5;EM522_0..EM522_4;EX522_0..EX522_7",
            "not_derived_channelwise_inputs_unfilled",
            "mu_extra can shift the denominator used by beta and local Newton tests",
        ),
        (
            "GM2897_6_constant_universal_coupling",
            "G_eff is fixed before fitting and has no source/range/time/frame/domain derivative",
            "partial_{t,r,A,lambda,frame,domain} G_eff=0",
            "SC532_6;SRC523_5",
            "not_parent_derived",
            "otherwise measured GM can hide a coupling drift",
        ),
        (
            "GM2897_7_EH_Poisson_coefficient",
            "same-frame local 00 equation has the standard Poisson coefficient",
            "nabla^2 Phi = 4 pi G_eff rho_H + S_res with S_res=0",
            "PG3;SN1;SRC523_1;R11",
            "conditional_R11_vector_unfilled",
            "charge equality is still not Newton unless the weak-field operator coefficient is standard",
        ),
        (
            "GM2897_8_Gauss_surface_no_residual",
            "surface Gauss mass equals enclosed parent source mass",
            "int_S grad Phi dS = 4 pi G_eff M_H with Delta_mu_Gauss=0",
            "PG4;SN4;SRC523_2",
            "not_parent_derived",
            "volume, boundary, domain and projector residuals can shift the surface mass",
        ),
        (
            "GM2897_9_orbital_readout_inverse_square",
            "slow orbital readout is pure inverse square in the same observed frame",
            "mu_obs = r^2 |a_r| = G_eff M_H",
            "PG5;SRC523_3",
            "not_derived",
            "test particles may see readout/range/frame/source-force corrections",
        ),
        (
            "GM2897_10_second_order_PPN_survival",
            "first-order measured-GM calibration survives beta/gamma/preferred-frame order",
            "delta_beta_source=0; gamma-1=0; alpha_i=0; xi=0 after measured-GM normalization",
            "PG9;SN11;SRC523_10;2894;2895;2896",
            "missing_A_B_R11_beta_source_rows",
            "a Newton denominator is not yet a local-GR/PPN theorem",
        ),
        (
            "GM2897_11_verdict",
            "measured-GM/source-current closure for current MTS",
            "all GM2897_0..GM2897_10 parent-signed and no missing rows",
            "all_above",
            "FAIL_CURRENT_MTS_CLOSURE_NOT_DERIVED",
            "closure route is exact, but the current corpus does not own enough premises",
        ),
    ]
    return [
        add_common(
            {
                "rung_id": rung_id,
                "required_identity": identity,
                "math_form": math_form,
                "source_rows": source_rows,
                "current_status": current_status,
                "why_needed": why_needed,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for rung_id, identity, math_form, source_rows, current_status, why_needed in specs
    ]


def operator_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "row_id": "SNO2897_0_source_normalization_operator",
                "model_id": "MTS_source_normalized_Newton_branch",
                "operator_family": "source_normalization_operator",
                "coefficient_symbol": "mu_extra_or_delta_GM_operator_vector",
                "coefficient_value": "MISSING_NUMERIC_OR_THEOREM_ZERO_COEFFICIENT",
                "coefficient_units": "dimensionless_epsilon_SN_or_declared_operator_units",
                "normalization": "relative_to_observed_mu_obs_and_parent_G_eff_M_H",
                "operator_form": "mu_obs = G_eff*M_H + mu_extra + Delta_mu_Gauss + Delta_mu_readout",
                "exact_no_cancellation_envelope": "|epsilon_SN| <= |epsilon_charge|+|epsilon_Poisson_or_c_nonEH|+|epsilon_Gauss|+|epsilon_orbit|+|epsilon_mu_extra_total|+|dln_Geff_and_Meff_hair|+|eta_source_AB|+|partial_r_ln_mu_obs|+|alpha(lambda)|+|delta_beta_source_vector|",
                "weak_field_map": "blocks Newton denominator, A_source/B_source beta law, R10 finite-range rows, Gdot rows, and local PPN source rows",
                "affected_rows": "R1;R4;R9;R10;R11;beta_source;source_normalized_Newton",
                "induced_observable": "epsilon_SN;delta_beta_source;gamma_minus_1;alpha(lambda);Gdot_over_G;eta_source_AB;partial_r_ln_mu_obs",
                "predicted_residual_or_bound_source": "MISSING_SOURCE_NORMALIZATION_THEOREM_OR_COMPONENT_ENVELOPE",
                "derivation_status": "retained_unfilled_after_2897_closure_attempt",
                "formula_reference": "2897 GM2897 closure chain; 532 epsilon_charge; 523 source-normalization scorecard",
                "source_file": str(DOC),
                "assumptions": "observed coframe fixed; compact local branch; no measured-GM absorption shortcut; no tuned cancellation; no GR reference A/B fill",
                "notes": "This is the row to replace with a real theorem-zero certificate or sourced component envelope; it is not evidence for a pass.",
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
    ]


def residual_first_fill_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2897_0_epsilon_charge", "SRC523_0_charge_current_normalization", "epsilon_charge", "(B_xi/G_eff - M_H[Pi_M J_H])/M_H", "MISSING_THEOREM_OR_COMPONENT_ENVELOPE", "primary_next", "first row: must close SC532_0..SC532_6 or fill absolute component envelope"),
        ("SRC2897_1_epsilon_Poisson", "SRC523_1_Poisson_operator_source", "epsilon_Poisson_or_c_nonEH", "deviation of local 00 coefficient from 4 pi G_eff rho_H", "MISSING_EH_ONLY_OR_R11_OPERATOR_VECTOR", "held_after_epsilon_charge", "downstream: only meaningful after charge-current normalization is owned"),
        ("SRC2897_2_epsilon_Gauss", "SRC523_2_Gauss_volume_boundary", "epsilon_Gauss", "Delta_mu_Gauss/(G_eff M_H)", "MISSING_GAUSS_NO_RESIDUAL_THEOREM_OR_INTEGRAL", "held_after_epsilon_charge", "surface mass can carry volume/boundary/projector/domain residuals"),
        ("SRC2897_3_epsilon_orbit", "SRC523_3_orbital_readout", "epsilon_orbit", "(r^2 |a_r|-mu_Gauss)/mu_Gauss", "MISSING_SAME_FRAME_SLOW_PARTICLE_READOUT_PROOF_OR_PROFILE", "held_after_epsilon_charge", "readout can carry direct force/range/frame corrections"),
        ("SRC2897_4_epsilon_mu_extra_total", "SRC523_4_extra_mass_channels_total", "epsilon_mu_extra_total", "sum_i |epsilon_extra_i| over boundary/domain/bulk/nonEH/kappa/frame/species/projector/anomaly/calibration channels", "MISSING_CHANNELWISE_ZERO_OR_BOUNDS", "active_guard", "large open channels cannot be hidden by cancellation"),
        ("SRC2897_5_Geff_derivatives", "SRC523_5_Geff_time_or_range_drift", "dln_Geff_dt;partial_r_Geff;partial_lambda_Geff", "derivatives of effective coupling after source normalization", "MISSING_CONSTANT_COUPLING_THEOREM_OR_DERIVATIVE_ROWS", "active_guard", "coupling drift would invalidate measured-GM absorption"),
        ("SRC2897_6_Meff_derivatives", "SRC523_6_Meff_flux_derivative", "dln_Meff_dt;partial_r_ln_Meff", "time/radial derivative of projected Hilbert mass flux", "MISSING_CLOSED_PIM_FLUX_OR_PROFILE", "active_guard", "radial/time hair is the explicit projected-flux obstruction"),
        ("SRC2897_7_eta_source_AB", "SRC523_7_species_source_charge", "eta_source_AB", "composition/source dependence of active gravitational source charge", "MISSING_SELECTOR_BLIND_SOURCE_THEOREM_OR_BOUND", "active_guard", "species dependence breaks universal source normalization"),
        ("SRC2897_8_radial_source_hair", "SRC523_8_radial_source_hair", "partial_r_ln_mu_obs", "radial derivative/envelope of measured source strength outside compact support", "MISSING_RADIAL_NO_HAIR_THEOREM_OR_PROFILE", "active_guard", "radial hair maps into PPN/fifth-force/orbital residuals"),
        ("SRC2897_9_alpha_lambda", "SRC523_9_range_dependence", "alpha(lambda)", "finite-range/Yukawa or non-Yukawa source-normalization correction curve", "MISSING_NO_RANGE_THEOREM_OR_R10_ALPHA_CURVE", "active_guard", "range dependence links local Newton to R10"),
        ("SRC2897_10_second_order_PPN_source", "SRC523_10_second_order_PPN_source", "delta_beta_source;gamma_minus_1;c_nonEH_operator_vector", "PPN source/operator residue after measured-GM normalization", "MISSING_SECOND_ORDER_SOURCE_OPERATOR_DERIVATION", "held_after_epsilon_charge", "beta route cannot claim until this is sourced"),
        ("SRC2897_11_epsilon_SN_envelope", "SRC523_11_total_no_cancellation_score", "epsilon_SN_envelope", "sum of absolute source-normalization residuals", "NOT_COMPUTED_PRECONDITIONS_UNFILLED", "blocked_until_components", "strict envelope refuses open/missing components"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, scorecard_row, symbol, formula, current_value, fill_priority, next_action in specs:
        rows.append(
            add_common(
                {
                    "row_id": row_id,
                    "scorecard_row": scorecard_row,
                    "symbol": symbol,
                    "formula": formula,
                    "current_value": current_value,
                    "units": "dimensionless_or_declared_profile_units_required_before_scoring",
                    "normalization": "observed_mu_obs_vs_parent_G_eff_M_H",
                    "source_path": str(SRC_SOURCE_SCORE),
                    "source_checkpoint": str(SRC_523_DOC),
                    "fill_priority": fill_priority,
                    "next_action": next_action,
                    "parent_signed": False,
                    "theorem_zero_adopted": False,
                    "finite_value_present": False,
                    "prediction_source_backed": False,
                    "accepted_for_scoring": False,
                }
            )
        )
    return rows


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2897_0_sources", "all source paths and anchors exist", "PASS", "source register validation covers cited inputs", True),
        ("GATE2897_1_closure_chain_written", "measured-GM/source-current closure chain is exact", "PASS_NONCLAIM", "the theorem route is explicit from B_xi/G_eff to mu_obs", False),
        ("GATE2897_2_epsilon_charge_zero", "epsilon_charge is theorem-zero or source-backed numeric below lock", "FAIL", "SC532_0..SC532_6 remain unsigned and no numeric component envelope exists", False),
        ("GATE2897_3_no_GM_absorption", "measured GM is not used to hide source/range/time coefficients", "PASS_GUARD", "all source-normalization rows are explicit and nonclaim", False),
        ("GATE2897_4_Poisson_Gauss_orbit", "charge passes through Poisson/Gauss/orbital readout", "FAIL", "PG3/PG4/PG5 remain conditional/open", False),
        ("GATE2897_5_second_order_PPN", "source-normalized Newton survives beta/gamma/preferred-frame order", "FAIL", "A/B and R11 beta source rows are still missing", False),
        ("GATE2897_6_operator_row", "source_normalization_operator row is staged", "PASS_NONCLAIM", "canonical nonclaim row written with missing theorem/value markers", False),
        ("GATE2897_7_next_target", "next target selects first real fill", "PASS_NONCLAIM", "epsilon_charge theorem certificate or component envelope selected", False),
        ("GATE2897_8_local_GR", "local GR/Newton branch closes", "FAIL_CLOSED", "measured-GM denominator and beta envelope remain blocked", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": gate_passed,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for gate_id, criterion, result, reason, gate_passed in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2897_0_measured_GM_closure_runner",
                "status": "REFUSED_MISSING_THEOREM_PREMISES",
                "required_components": "SC532_0..SC532_6 plus PG3/PG4/PG5/SN11 for Newton/local-GR promotion",
                "components_evaluable": 0,
                "diagnostic_components_evaluable": 0,
                "reason": "charge-current equality, parent Pi_M ownership, commutator silence, extra projection silence, and constant coupling are not parent-signed",
                "runner_ready": False,
            }
        ),
        add_common(
            {
                "runner_id": "RUN2897_1_source_residual_first_fill_rows",
                "status": "STAGED_NONCLAIM_ROWS",
                "required_components": "12 source-normalization scorecard rows",
                "components_evaluable": 0,
                "diagnostic_components_evaluable": 0,
                "reason": "rows are parseable and prioritized but still need theorem-zero certificates or source-backed numeric component envelopes",
                "runner_ready": False,
            }
        ),
        add_common(
            {
                "runner_id": "RUN2897_2_next_epsilon_charge",
                "status": "NEXT_TARGET_SELECTED",
                "required_components": "epsilon_charge certificate or component envelope",
                "components_evaluable": 0,
                "diagnostic_components_evaluable": 0,
                "reason": "epsilon_charge is the first denominator lock; downstream Poisson/Gauss/beta work is less meaningful before it is owned",
                "runner_ready": False,
            }
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2897_0_core_result", "MEASURED_GM_CLOSURE_ROUTE_EXACT_BUT_NOT_DERIVED", "the chain from Hamiltonian charge to mu_obs is written, but current MTS lacks parent-signed charge-current/Pi_M/commutator/extra-projection/coupling premises", "do not claim source-normalized Newton"),
        ("DEC2897_1_no_absorption", "REJECT_MEASURED_GM_ABSORPTION_SHORTCUT", "absorbing source-normalization into measured GM would hide derivative/range/species/domain/R11 beta residuals", "keep every source-normalization component explicit"),
        ("DEC2897_2_operator", "STAGE_SOURCE_NORMALIZATION_OPERATOR_NONCLAIM_ROW", "this is the shared bottleneck for Newton denominator, beta A/B, R10, Gdot, and local PPN", "replace only with theorem-zero or real numeric component envelope"),
        ("DEC2897_3_first_fill", "SELECT_EPSILON_CHARGE_FIRST", "epsilon_charge is the earliest source-current equality row and already has exact 532 component decomposition", "build 2898 epsilon_charge theorem certificate or component-envelope runner"),
        ("DEC2897_4_downstream", "HOLD_R2FR_SCALAR_AND_PPN_ROWS", "R2/fR and beta rows need the denominator convention fixed before their amplitudes are physically interpretable", "return after source-normalization status is explicit"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2897_0_2898",
                "status": "selected_primary",
                "target_doc": "2898-Y5-R2FR-epsilon-charge-theorem-certificate-or-component-envelope-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_epsilon_charge_theorem_certificate_or_component_envelope_under_AX1090_2898.py",
                "mission": "try to prove epsilon_charge=0 from SC532_0..SC532_6; if proof fails, stage a strict component-envelope input row for epsilon_Hamiltonian_norm, epsilon_PiM_equality, epsilon_commutator, epsilon_extra_projection, epsilon_boundary_anomaly, and epsilon_Geff_abs",
                "forbidden": "measured-GM absorption; source-unity shortcut; closure multiplier; cancellation between open components; local-GR/Newton/beta claim; GitHub action; formalization-workbench edit",
                "selected": True,
            }
        ),
        add_common(
            {
                "next_id": "NEXT2897_1_held_R2_fR",
                "status": "held_until_epsilon_charge_status",
                "target_doc": "2897b-Y5-R2FR-R2-fR-scalar-beta-row-or-nohair-proof.md",
                "target_script": "scripts/Y5_R2FR_R2_fR_scalar_beta_row_or_nohair_proof_2897b.py",
                "mission": "fill the first metric-operator R11 beta row only after the source-normalization denominator is explicit",
                "forbidden": "use reference GR A/B; ignore source-normalization denominator; local-GR claim",
                "selected": False,
            }
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("BR2897_0_operator_copy", OUTPUTS["operator"], BRANCH_OUTPUTS["operator_copy"], "beta-source copy of source-normalization operator row"),
        ("BR2897_1_residuals_copy", OUTPUTS["residuals"], BRANCH_OUTPUTS["residuals_copy"], "beta-source copy of first-fill residual rows"),
        ("BR2897_2_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB acquisition queue next target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def formalization_touched() -> bool:
    if not FORMALIZATION.exists():
        return False
    start_ts = SCRIPT_START_UTC.timestamp()
    for path in FORMALIZATION.rglob("*"):
        try:
            if path.is_file() and path.stat().st_mtime >= start_ts:
                return True
        except OSError:
            return True
    return False


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    closure_rows_ = all_rows["closure"]
    operator_rows_ = all_rows["operator"]
    residual_rows = all_rows["residuals"]
    gate_rows_ = all_rows["gates"]
    next_rows_ = all_rows["next"]
    branch_rows = all_rows["branches"]

    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("VAL2897_0_sources_exist", all(row["path_exists"] for row in source_rows), "all registered source paths exist"),
        ("VAL2897_1_source_anchors", all(row["anchors_found"] for row in source_rows), "all registered source anchors were found"),
        ("VAL2897_2_closure_refused", any(row["rung_id"] == "GM2897_11_verdict" and "FAIL" in row["current_status"] for row in closure_rows_), "measured-GM closure is refused for current MTS"),
        ("VAL2897_3_operator_nonclaim", all(not row["valid_for_claim"] and "MISSING" in row["coefficient_value"] for row in operator_rows_), "source-normalization operator row remains nonclaim with missing value marker"),
        ("VAL2897_4_residual_rows_nonclaim", all(not row["valid_for_claim"] and not row["accepted_for_scoring"] for row in residual_rows), "all first-fill residual rows are explicit nonclaim rows"),
        ("VAL2897_5_epsilon_charge_primary", any(row["symbol"] == "epsilon_charge" and row["fill_priority"] == "primary_next" for row in residual_rows), "epsilon_charge is selected as first fill row"),
        ("VAL2897_6_absorption_guard", any(row["gate_id"] == "GATE2897_3_no_GM_absorption" and row["result"] == "PASS_GUARD" for row in gate_rows_), "measured-GM absorption shortcut is rejected"),
        ("VAL2897_7_local_gr_fail_closed", any(row["gate_id"] == "GATE2897_8_local_GR" and row["result"] == "FAIL_CLOSED" for row in gate_rows_), "local GR/Newton branch remains fail-closed"),
        ("VAL2897_8_next_target_2898", any(row["next_id"] == "NEXT2897_0_2898" and row["selected"] for row in next_rows_), "2898 epsilon_charge target selected"),
        ("VAL2897_9_branch_copies_exist", all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2897_10_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs), "all generated CSV outputs parse cleanly"),
        ("VAL2897_11_formalization_untouched_during_run", not formalization_touched(), "formalization-workbench was not touched during this run"),
    ]
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL2897_OVERALL", overall, "2897 validation overall"))
    return [
        {
            "check_id": check_id,
            "passed": passed,
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, passed, detail in checks
    ]


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2897 - Y5 R2FR Source-Normalization Operator First Fill or Measured-GM Current Closure Under AX1090",
        "",
        f"Run: `runs/{SCRIPT_START_UTC.strftime('%Y%m%d-%H%M%S')}-Y5-R2FR-source-normalization-operator-first-fill-or-measured-GM-current-closure-under-AX1090`",
        "Status: `Y5_R2FR_2897_measured_GM_closure_attempt_refused_source_normalization_operator_nonclaim_row_staged_epsilon_charge_2898_next`",
        "Claim ceiling: `source_normalization_operator_first_fill_only_no_measured_GM_Newton_beta_PPN_local_GR_R10_or_GitHub_claim`",
        "",
        "## Summary",
        "",
        "The 2896 beta envelope pointed at the real lock: the observed Newtonian denominator `mu_obs=GM` is not automatically the parent source charge. This checkpoint attacks that lock directly.",
        "",
        "The exact chain is now:",
        "",
        "`H_xi -> B_xi/G_eff -> M_H[Pi_M J_H] -> Phi -> Gauss surface mass -> mu_obs=r^2 |a_r|`.",
        "",
        "Current MTS does not yet derive the chain. The first obstruction remains the source-current equality",
        "",
        "`epsilon_charge = (B_xi/G_eff - M_H[Pi_M J_H]) / M_H`.",
        "",
        "If `epsilon_charge` is not theorem-zero or source-backed numeric, the later beta/A-B/R11 rows do not have a clean physical denominator. So 2897 does not promote Newton or local GR; it stages the source-normalization operator as the primary nonclaim row and selects the `epsilon_charge` certificate/component-envelope run next.",
        "",
        "## Source Register",
        "",
        md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"]),
        "",
        "## Measured-GM Closure Attempt",
        "",
        md_table(all_rows["closure"], ["rung_id", "required_identity", "math_form", "source_rows", "current_status", "why_needed", "valid_for_claim"]),
        "",
        "## Source-Normalization Operator Row",
        "",
        md_table(all_rows["operator"], ["row_id", "operator_family", "coefficient_symbol", "coefficient_value", "normalization", "operator_form", "weak_field_map", "derivation_status", "valid_for_claim"]),
        "",
        "## First-Fill Residual Rows",
        "",
        md_table(all_rows["residuals"], ["row_id", "scorecard_row", "symbol", "formula", "current_value", "fill_priority", "next_action", "valid_for_claim"]),
        "",
        "## Acceptance Gates",
        "",
        md_table(all_rows["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"]),
        "",
        "## Runner Status",
        "",
        md_table(all_rows["runner"], ["runner_id", "status", "required_components", "components_evaluable", "reason", "runner_ready", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(all_rows["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(all_rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(all_rows["validation"], ["check_id", "passed", "detail", "generated_utc"]),
        "",
        "## Working Read",
        "",
        "This is progress, but it is progress of the unromantic kind: the coupling/normalization problem has been turned into a finite theorem-or-data slot. That is exactly what we need. If `epsilon_charge` closes, the Newton branch becomes materially stronger. If it fails, the theory does not collapse; it carries a visible source-charge residual instead of smuggling it into `GM`.",
        "",
        "## Forbidden Claims From 2897",
        "",
        "- MTS has derived `B_xi/G_eff = M_H[Pi_M J_H]`.",
        "- MTS has filled `epsilon_charge`.",
        "- MTS has derived measured `GM`, source-normalized Newton, beta, PPN, R10, or local GR.",
        "- MTS may absorb source-normalization into measured `GM` without a parent theorem proving universal, derivative-silent, range-silent, species-silent behavior.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {}
    all_rows["sources"] = source_register_rows()
    all_rows["closure"] = closure_rows()
    all_rows["operator"] = operator_rows()
    all_rows["residuals"] = residual_first_fill_rows()
    all_rows["gates"] = gate_rows()
    all_rows["runner"] = runner_rows()
    all_rows["decision"] = decision_rows()
    all_rows["next"] = next_rows()

    for key in ["sources", "closure", "operator", "residuals", "gates", "runner", "decision", "next"]:
        write_csv(OUTPUTS[key], all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_doc(all_rows)

    overall = next(row["passed"] for row in all_rows["validation"] if row["check_id"] == "VAL2897_OVERALL")
    print(f"2897 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()
