from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_Hamiltonian_to_Poisson_Gauss_MHref_bridge_conditional_residual_bound_row_unfilled_nonclaim"
CLAIM_CEILING = "PG_MHref_calibration_attempt_only_no_MHref_value_no_measured_GM_no_Newton_no_PPN_no_R10_no_local_GR_claim"
NEXT_TARGET = "699-Y5-R10-PG-calibration-residual-bound-source-row-or-EH-coefficient-proof.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "698-Y5-R10-Hamiltonian-charge-to-Poisson-Gauss-MHref-calibration-or-residual-bound.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "450_doc": ROOT / "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
    "458_doc": ROOT / "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
    "459_doc": ROOT / "459-PG-calibration-residual-mapper.md",
    "523_doc": ROOT / "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
    "529_doc": ROOT / "529-Y5-source-calibrated-EH-family-proof-stack-or-R11-beta-fill.md",
    "532_doc": ROOT / "532-Y5-measured-GM-source-current-closure-or-first-input-fill.md",
    "540_doc": ROOT / "540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md",
    "541_doc": ROOT / "541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md",
    "657_doc": ROOT / "657-Y5-R10-source-normalization-family-first-real-R11-fill.md",
    "659_doc": ROOT / "659-Y5-R10-parent-source-identity-for-closed-PiM-flux-or-radial-profile-fill.md",
    "683_doc": ROOT / "683-Y5-R10-MH-ref-same-frame-denominator-or-Qedge-numerator-source.md",
    "696_doc": ROOT / "696-Y5-R10-MHref-same-frame-denominator-or-BTF-product-bound-guard.md",
    "697_doc": ROOT / "697-Y5-R10-MHref-source-normalization-certificate-or-denominator-fill-row.md",
    "657_validation": RESIDUALS / "P8_Y5_BRR545_657_VALIDATION.csv",
    "659_validation": RESIDUALS / "P8_Y5_BRR545_659_VALIDATION.csv",
    "683_validation": RESIDUALS / "P8_Y5_BRR545_683_VALIDATION.csv",
    "696_validation": RESIDUALS / "P8_Y5_BRR545_696_VALIDATION.csv",
    "697_validation": RESIDUALS / "P8_Y5_BRR545_697_VALIDATION.csv",
    "pg_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    "hilbert_contract": RESIDUALS / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
    "hsm_contract": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
    "hsm_scorecard": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_SCORECARD.csv",
    "gauss_ppn_test": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_GAUSS_PPN_TEST.csv",
    "source_norm_scorecard": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
    "657_cmu_fill": RESIDUALS / "P8_Y5_R10_657_CMU_SOURCE_NORMALIZATION_FILL.csv",
    "657_channels": RESIDUALS / "P8_Y5_R10_657_CMU_EIGHT_CHANNEL_VECTOR.csv",
    "659_closure": RESIDUALS / "P8_Y5_R10_659_CLOSURE_IDENTITY.csv",
    "659_obstructions": RESIDUALS / "P8_Y5_R10_659_OBSTRUCTION_AUDIT.csv",
    "683_denominator": RESIDUALS / "P8_Y5_R10_683_MH_REF_DENOMINATOR_ATTEMPT.csv",
    "683_same_frame_gate": RESIDUALS / "P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv",
    "696_denominator_audit": RESIDUALS / "P8_Y5_R10_696_MHREF_DENOMINATOR_AUDIT.csv",
    "697_certificate": RESIDUALS / "P8_Y5_R10_697_MHREF_SOURCE_NORMALIZATION_CERTIFICATE.csv",
    "697_derivation": RESIDUALS / "P8_Y5_R10_697_CONDITIONAL_DERIVATION_CHAIN.csv",
    "697_fill": RESIDUALS / "P8_Y5_R10_697_DENOMINATOR_FILL_ROW.csv",
    "boundary_reference_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures_for(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "MISSING_VALIDATION_FILE", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def first_row_with(rows: list[dict[str, str]], field: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(field) == value:
            return row
    return {}


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate_path in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate_path.is_file()
        and datetime.fromtimestamp(candidate_path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "450_doc": "Hilbert source to measured monopole calibration predecessor",
        "458_doc": "Hamiltonian charge to Poisson/Gauss calibration gate",
        "459_doc": "PG calibration residual mapper predecessor",
        "523_doc": "Gauss/orbital source-normalization residual score predecessor",
        "529_doc": "source-calibrated EH proof-stack predecessor",
        "532_doc": "measured-GM source-current closure predecessor",
        "540_doc": "Hamiltonian PiM source-measure and PPN readout test",
        "541_doc": "Hamiltonian PiM source-measure contract and residual scorecard",
        "657_doc": "source-normalization eight-channel decomposition",
        "659_doc": "closed PiM flux conditional identity",
        "683_doc": "prior M_H_ref denominator anti-circularity attempt",
        "696_doc": "M_H_ref denominator/product-bound guard",
        "697_doc": "M_H_ref source-normalization certificate predecessor",
        "657_validation": "657 validation gate",
        "659_validation": "659 validation gate",
        "683_validation": "683 validation gate",
        "696_validation": "696 validation gate",
        "697_validation": "697 validation gate",
        "pg_contract": "PG0-PG10 calibration contract",
        "hilbert_contract": "Hilbert monopole calibration contract",
        "hsm_contract": "HSM541 source-measure contract",
        "hsm_scorecard": "HSM541 source-measure residual scorecard",
        "gauss_ppn_test": "GPT540 Gauss/PPN readout tests",
        "source_norm_scorecard": "source-normalization residual scorecard",
        "657_cmu_fill": "exact c_mu decomposition row",
        "657_channels": "eight retained source-normalization channels",
        "659_closure": "exact PiM flux obstruction identity",
        "659_obstructions": "PiM flux obstruction audit",
        "683_denominator": "M_H_ref denominator attempt",
        "683_same_frame_gate": "same-frame GM gate",
        "696_denominator_audit": "current M_H_ref blocker audit",
        "697_certificate": "source-normalization certificate rows",
        "697_derivation": "conditional M_H_ref derivation chain",
        "697_fill": "unfilled denominator fill row",
        "boundary_reference_status": "claim-valid M_H_ref status",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def bridge_theorem_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        (
            "BT698_0_charge_input",
            "well-defined Hamiltonian charge in observed time",
            "H_tau[S]=int_S(Q_tau-i_tau B_ref), delta H_tau integrable, tau=tau_obs",
            "PG0 and HSM541_1 conditional/not derived",
            "conditional_not_claim",
            "Delta_symp;B_zero_flux;tau_frame_residual",
            "458_doc;541_doc;697_certificate",
        ),
        (
            "BT698_1_charge_equals_projected_Hilbert_source",
            "Hamiltonian charge equals projected Hilbert mass current",
            "H_tau/G_ref = int_S Pi_M J_H with fixed Pi_M and no projector variation stress",
            "PG1/HM1/HM2 not parent-derived; 659 obstruction identity remains open",
            "fail_current_corpus",
            "Delta_charge_current;epsilon_radial_Meff;I_commutator",
            "pg_contract;hilbert_contract;659_closure;659_obstructions",
        ),
        (
            "BT698_2_same_frame_potential",
            "same observed metric potential acts on matter and is sourced by J_H",
            "g_00=-1+2 Phi/c^2 and a=-grad Phi in the same e_obs frame",
            "PG2 and same-frame gate conditional/not derived",
            "fail_current_corpus",
            "Delta_frame;Delta_cal",
            "pg_contract;683_same_frame_gate;697_certificate",
        ),
        (
            "BT698_3_EH_to_Poisson_coefficient",
            "weak-field 00 equation reduces to Poisson with standard coefficient",
            "nabla^2 Phi=(kappa_eff c^4/2)rho_H=4*pi*G_ref*rho_H",
            "PG3 conditional from EH branch; non-EH/source residuals not cleared",
            "conditional_not_claim",
            "epsilon_operator;epsilon_nonEH_source;source_coefficient_residual",
            "pg_contract;529_doc;657_channels",
        ),
        (
            "BT698_4_Gauss_surface_integral",
            "Poisson source integrates to the same enclosed Hamiltonian/Hilbert charge",
            "surface_integral grad Phi dot dS=4*pi*G_ref M_H_ref with no residual volume/boundary term",
            "PG4 not parent-derived; radial/source/boundary hair live",
            "fail_current_corpus",
            "Delta_Gauss;epsilon_radial_Meff;epsilon_boundary",
            "pg_contract;hsm_scorecard;659_obstructions",
        ),
        (
            "BT698_5_orbital_inverse_square_readout",
            "test bodies read the same monopole as pure inverse-square acceleration",
            "a_r=-G_ref M_H_ref/r^2 and v^2 r=G_ref M_H_ref",
            "PG5 not derived; fifth-force/radial/source-charge channels live",
            "fail_current_corpus",
            "alpha_lambda;partial_r_ln_mu_obs;eta_source_AB",
            "pg_contract;gauss_ppn_test;657_channels",
        ),
        (
            "BT698_6_constant_universal_G",
            "G_ref is constant, universal, source-blind, range-blind, and frame-blind",
            "partial_t,r,A,lambda,frame G_ref=0",
            "PG7/HM4 conditional not parent-derived",
            "fail_current_corpus",
            "dln_Geff_dt;source_charge;range_dependence",
            "pg_contract;hilbert_contract;657_channels",
        ),
        (
            "BT698_7_zero_extra_source_channels",
            "all unowned monopole/source-normalization channels vanish or are bounded",
            "mu_obs=G_ref M_H_ref + mu_extra with mu_extra=0 or explicit bounded residual",
            "657 gives exact channel decomposition but every channel remains unfilled",
            "fail_current_corpus",
            "mu_extra_over_GM;channelwise_source_residuals",
            "657_cmu_fill;657_channels;source_norm_scorecard",
        ),
        (
            "BT698_8_MHref_calibration",
            "derived measured-GM denominator equality",
            "BT698_0...BT698_7 => GM_orbit=G_ref M_H_ref and M_H_ref>0",
            "multiple arrows are conditional or failed",
            "fail_current_corpus",
            "epsilon_PG_MHref_abs",
            "697_derivation;697_fill;boundary_reference_status",
        ),
        (
            "BT698_9_PPN_followthrough_guard",
            "first-order source calibration survives second-order PPN",
            "delta_beta_source=0 and gamma/beta/source terms use the same denominator",
            "PG9/HM7 not derived; epsilon_TF remains blocked",
            "not_reached",
            "delta_beta_source;gamma_minus_one;epsilon_TF",
            "pg_contract;696_denominator_audit;gauss_ppn_test",
        ),
    ]
    return [
        {
            "theorem_id": theorem_id,
            "bridge_clause": bridge_clause,
            "mathematical_form": mathematical_form,
            "observed_state": observed_state,
            "result": result,
            "residual_if_fail": residual_if_fail,
            "valid_for_claim": "false",
            "source_paths": source_list(*source_ids.split(";")),
            "generated_utc": now,
        }
        for theorem_id, bridge_clause, mathematical_form, observed_state, result, residual_if_fail, source_ids in rows
    ]


def obstruction_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        ("OBS698_0_integrability_reference", "Delta_symp + B_zero_flux", "H_tau not integrable/fixed-reference", "M_H_ref is convention-sensitive", "MISSING_REFERENCE_LOCK_OR_BOUND", "hsm_contract;boundary_reference_status"),
        ("OBS698_1_charge_current_split", "Delta_charge_current", "Hamiltonian charge not proved equal to Pi_M J_H", "measured source mass not derived", "MISSING_CHARGE_CURRENT_EQUALITY", "pg_contract;hilbert_contract"),
        ("OBS698_2_frame_split", "Delta_frame + Delta_cal", "orbit/potential/source frames not proved identical", "GM readout can differ from source charge", "MISSING_SAME_FRAME_CALIBRATION", "683_same_frame_gate;697_certificate"),
        ("OBS698_3_operator_coefficient", "epsilon_operator", "EH-to-Poisson coefficient conditional and non-EH terms retained", "wrong Poisson coefficient or extra potential possible", "MISSING_EH_ONLY_SOURCE_COEFFICIENT_PROOF", "pg_contract;529_doc;657_channels"),
        ("OBS698_4_gauss_surface", "Delta_Gauss", "Poisson volume/source not proved equal to Hamiltonian surface charge", "surface integral cannot calibrate M_H_ref", "MISSING_GAUSS_SURFACE_CALIBRATION", "pg_contract;hsm_scorecard"),
        ("OBS698_5_orbital_readout", "alpha_lambda + partial_r_ln_mu_obs", "pure inverse-square geodesic readout not derived", "orbital GM may include fifth-force/radial terms", "MISSING_ORBITAL_READOUT_THEOREM_OR_BOUND", "pg_contract;gauss_ppn_test"),
        ("OBS698_6_universal_coupling", "dln_Geff_dt + source/range drift", "G_ref not parent-fixed universal", "GM_orbit/G_ref cannot be used as fixed mass", "MISSING_CONSTANT_UNIVERSAL_GREF_CERTIFICATE", "hilbert_contract;657_channels"),
        ("OBS698_7_extra_source_channels", "mu_extra_over_GM", "source-normalization channels named but unfilled", "hidden channels can contaminate denominator", "MISSING_MU_EXTRA_ZERO_OR_CHANNEL_BOUNDS", "657_cmu_fill;657_channels"),
        ("OBS698_8_second_order_source", "delta_beta_source + gamma/shear", "PPN order not reached", "Newton-looking bridge cannot claim local GR", "MISSING_SECOND_ORDER_SOURCE_STABILITY", "pg_contract;696_denominator_audit"),
    ]
    return [
        {
            "obstruction_id": obstruction_id,
            "residual_quantity": residual_quantity,
            "failure_mode": failure_mode,
            "effect_on_MHref": effect_on_mhref,
            "current_status": current_status,
            "valid_for_claim": "false",
            "source_paths": source_list(*source_ids.split(";")),
            "generated_utc": now,
        }
        for obstruction_id, residual_quantity, failure_mode, effect_on_mhref, current_status, source_ids in rows
    ]


def residual_bound_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "bound_id": "PGB698_0_epsilon_PG_MHref_abs",
            "quantity": "epsilon_PG_MHref_abs",
            "definition": "abs(GM_orbit/G_ref - M_H_ref)/M_H_ref",
            "expanded_bound": "abs(Delta_charge_current)+abs(Delta_frame)+abs(Delta_Poisson)+abs(Delta_Gauss)+abs(Delta_orbit)+abs(Delta_G)+abs(mu_extra_over_GM)+abs(delta_beta_source_guard)",
            "M_H_ref": "MISSING_CERTIFIED_POSITIVE_M_H_REF",
            "GM_orbit": "MISSING_DERIVED_ORBITAL_GM",
            "G_ref": "MISSING_CONSTANT_UNIVERSAL_GREF",
            "Delta_charge_current": "MISSING_CHARGE_CURRENT_EQUALITY_OR_BOUND",
            "Delta_frame": "MISSING_SAME_FRAME_CALIBRATION_OR_BOUND",
            "Delta_Poisson": "MISSING_EH_POISSON_COEFFICIENT_OR_BOUND",
            "Delta_Gauss": "MISSING_GAUSS_SURFACE_CALIBRATION_OR_BOUND",
            "Delta_orbit": "MISSING_ORBITAL_READOUT_OR_ALPHA_LAMBDA_BOUND",
            "Delta_G": "MISSING_GREF_DRIFT_SOURCE_RANGE_BOUND",
            "mu_extra_over_GM": "MISSING_MU_EXTRA_ZERO_OR_CHANNEL_BOUNDS",
            "delta_beta_source_guard": "MISSING_SECOND_ORDER_SOURCE_STABILITY_BOUND",
            "units": "dimensionless_after_dividing_by_M_H_ref",
            "source_path": "MISSING_SOURCE_PATH",
            "derivation_status": "unfilled_after_PG_bridge_failure",
            "valid_for_claim": "false",
            "source_paths": source_list("pg_contract", "697_fill", "hsm_scorecard"),
            "generated_utc": now,
        }
    ]


def observable_leakage_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        ("OL698_0_MHref_denominator", "M_H_ref", "epsilon_PG_MHref_abs blocks denominator fill", "B_TF_over_MH and epsilon_TF remain unscoreable", "697_fill;696_denominator_audit"),
        ("OL698_1_Newton", "source-normalized Newton", "Poisson/Gauss/orbit bridge not derived", "no Newton recovery claim", "458_doc;540_doc"),
        ("OL698_2_R10", "alpha(lambda)", "Delta_orbit/range source residual can mimic fifth force", "no R10 pass; source row required", "657_channels;pg_contract"),
        ("OL698_3_PPN_beta_gamma", "beta/gamma", "source calibration and epsilon_TF are not fixed", "no PPN score or local-GR promotion", "gauss_ppn_test;696_denominator_audit"),
        ("OL698_4_Gdot", "Gdot/G", "G_ref and source strength derivative hair remain live", "Gdot residual retained", "hilbert_contract;657_channels"),
        ("OL698_5_WEP_clock", "eta/source/clock rows", "same-frame/source-blind matter coupling not proved", "WEP/clock source-side residuals retained", "657_channels;683_same_frame_gate"),
        ("OL698_6_unification_spine", "GR reduction spine", "first-order measured mass bridge remains conditional", "local-GR branch still closure-gated", "697_derivation;pg_contract"),
    ]
    return [
        {
            "leak_id": leak_id,
            "target": target,
            "leakage": leakage,
            "claim_effect": claim_effect,
            "valid_for_claim": "false",
            "source_paths": source_list(*source_ids.split(";")),
            "generated_utc": now,
        }
        for leak_id, target, leakage, claim_effect, source_ids in rows
    ]


def anti_circularity_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        ("AC698_0_no_GM_substitution", "Do not set M_H_ref=GM_orbit/G_ref until BT698_0...BT698_7 are derived", "prevents Newton/orbit readout being used to prove Newton/orbit readout", "guard_active", "683_denominator;697_fill"),
        ("AC698_1_no_Poisson_only_local_GR", "Poisson/Gauss bridge is first-order only and cannot imply local GR without PPN followthrough", "prevents GR reduction overclaim", "guard_active", "pg_contract;gauss_ppn_test"),
        ("AC698_2_no_residual_cancellation", "No cancellation credit between charge, frame, Gauss, orbit, coupling, and mu_extra residuals", "keeps residual bound conservative", "guard_active", "hsm_scorecard;657_channels"),
        ("AC698_3_no_product_bound_backfill", "PPN/product bounds cannot backfill the missing denominator", "prevents external bound laundering", "guard_active", "696_doc;697_doc"),
        ("AC698_4_smoke_only_empirical_row", "A private empirical GM row is allowed only with valid_for_claim=false", "keeps future numerical tests useful but non-evidential", "guard_active", "697_fill;pg_contract"),
    ]
    return [
        {
            "guard_id": guard_id,
            "rule": rule,
            "reason": reason,
            "current_status": current_status,
            "valid_for_claim": "false",
            "source_paths": source_list(*source_ids.split(";")),
            "generated_utc": now,
        }
        for guard_id, rule, reason, current_status, source_ids in rows
    ]


def evaluator_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "eval_id": "E698_0_bridge_theorem",
            "target": "GM_orbit=G_ref*M_H_ref",
            "observed_state": "bridge arrows written but BT698_1/2/4/5/6/7 fail current corpus",
            "result": "conditional_not_claimed",
            "claim_effect": "no measured-GM denominator",
            "valid_for_claim": "false",
            "source_paths": source_list("pg_contract", "697_certificate"),
            "generated_utc": now,
        },
        {
            "eval_id": "E698_1_residual_bound",
            "target": "epsilon_PG_MHref_abs",
            "observed_state": "bound row written with MISSING markers",
            "result": "unfilled_nonclaim",
            "claim_effect": "residual exists as exact debt, not a number",
            "valid_for_claim": "false",
            "source_paths": source_list("hsm_scorecard", "pg_contract"),
            "generated_utc": now,
        },
        {
            "eval_id": "E698_2_MHref_fill",
            "target": "M_H_ref",
            "observed_state": "MHR697 remains MISSING_CERTIFIED_POSITIVE_M_H_REF",
            "result": "fail_blocked",
            "claim_effect": "no B_TF_over_MH/e_TF/PPN/R10 score",
            "valid_for_claim": "false",
            "source_paths": source_list("697_fill", "696_denominator_audit"),
            "generated_utc": now,
        },
        {
            "eval_id": "E698_3_next",
            "target": "PG residual source row or EH coefficient proof",
            "observed_state": "PG3 conditional but PG4/PG5 unfilled",
            "result": "selected_next_target",
            "claim_effect": "make the residual bound executable or close one bridge arrow",
            "valid_for_claim": "false",
            "source_paths": source_list("pg_contract", "529_doc"),
            "generated_utc": now,
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    gates = [
        ("CG698_0_Hamiltonian_charge", "H_tau exists, integrable, fixed reference, observed tau", "conditional_from_457_not_parent_derived;not_derived_for_current_MTS", "fail_blocked", "no stable charge denominator", "pg_contract;hsm_contract"),
        ("CG698_1_charge_current_equality", "H_tau/G_ref equals projected Hilbert mass current", "not_parent_derived", "fail_blocked", "charge not measured source mass", "pg_contract;hilbert_contract"),
        ("CG698_2_same_frame_potential", "same Phi controls matter orbit and source equation", "conditional_not_parent_derived", "fail_blocked", "frame/readout split active", "pg_contract;683_same_frame_gate"),
        ("CG698_3_Poisson_coefficient", "EH weak-field coefficient fixed with no source residual", "conditional_from_424", "fail_conditional", "operator/source residual retained", "pg_contract;529_doc"),
        ("CG698_4_Gauss_surface", "surface integral equals M_H_ref with no residual", "not_parent_derived", "fail_blocked", "Delta_Gauss retained", "pg_contract;hsm_scorecard"),
        ("CG698_5_orbital_readout", "pure inverse-square orbital readout", "not_parent_derived", "fail_blocked", "alpha/radial residual retained", "pg_contract;gauss_ppn_test"),
        ("CG698_6_universal_G", "constant universal G_ref", "conditional_not_parent_derived", "fail_blocked", "coupling residual retained", "hilbert_contract;657_channels"),
        ("CG698_7_mu_extra", "all extra source channels zero or bounded", "EXACT_SUM_RULE_NON_NUMERIC_CHANNELS_UNFILLED", "fail_blocked", "hidden source-normalization channels retained", "657_cmu_fill;657_channels"),
        ("CG698_8_PPN_followthrough", "second-order PPN source stability", "not_derived_or_not_reached", "fail_blocked", "no local-GR claim", "pg_contract;gauss_ppn_test"),
        ("CG698_9_claim_fill", "M_H_ref denominator row filled claim-ready", "MISSING_CERTIFIED_POSITIVE_M_H_REF", "fail_blocked", "no M_H_ref value", "697_fill"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": observed_state,
            "result": result,
            "claim_effect": claim_effect,
            "valid_for_claim": "false",
            "source_paths": source_list(*source_ids.split(";")),
            "generated_utc": now,
        }
        for gate_id, gate, observed_state, result, claim_effect, source_ids in gates
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D698_0_bridge_attempt",
            "target": "Hamiltonian charge to Poisson/Gauss M_H_ref calibration",
            "result": "conditional_theorem_written_not_signed",
            "reason": "the arrow chain has the GR-like shape, but charge-current equality, same-frame readout, Gauss surface calibration, pure orbit, universal G, and source channels remain unsigned",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D698_1_residual_bound",
            "target": "epsilon_PG_MHref_abs",
            "result": "row_written_unfilled",
            "reason": "failed arrows are decomposed into a no-cancellation residual envelope, but no numeric/source rows exist yet",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D698_2_next",
            "target": "PG residual source row or EH coefficient proof",
            "result": "selected",
            "reason": "next work should either close the cleanest coefficient arrow or make Delta_Gauss/Delta_orbit executable as data",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S698_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "Hamiltonian-to-Poisson/Gauss bridge has a precise conditional theorem but no claim-ready calibration",
            "hardest_blocker": "Gauss/orbital equality without borrowing observed GM, plus universal G and source-channel silence",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def all_valid_for_claim_false(rows_by_name: dict[str, list[dict[str, str]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if row.get("valid_for_claim") == "true":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, str]],
    bridge_rows: list[dict[str, str]],
    obstruction_rows_: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    leakage_rows: list[dict[str, str]],
    anti_rows: list[dict[str, str]],
    evaluator_rows_: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows_by_name = {
        "bridge": bridge_rows,
        "obstruction": obstruction_rows_,
        "residual": residual_rows,
        "leakage": leakage_rows,
        "anti": anti_rows,
        "evaluator": evaluator_rows_,
        "gates": gate_rows,
        "decision": decision_rows_,
        "summary": summary_rows,
    }
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_ids = ["657_validation", "659_validation", "683_validation", "696_validation", "697_validation"]
    prior_failure_counts = {source_id: len(validation_failures_for(source_id)) for source_id in prior_ids}
    pg_rows = read_csv(SOURCE_PATHS["pg_contract"])
    pg_nonclaim = len(pg_rows) >= 10 and all(row.get("current_status") not in {"pass", "proved", "claim_valid"} for row in pg_rows[:10])
    snc_pg = first_row_with(read_csv(SOURCE_PATHS["697_certificate"]), "certificate_id", "SNC697_5_poisson_gauss_orbit")
    mh_fill = read_csv(SOURCE_PATHS["697_fill"])[0]
    bridge_complete = len(bridge_rows) == 10 and all(row["valid_for_claim"] == "false" for row in bridge_rows)
    bridge_failed = any(row["result"] == "fail_current_corpus" for row in bridge_rows)
    obstruction_complete = len(obstruction_rows_) == 9 and all(row["valid_for_claim"] == "false" for row in obstruction_rows_)
    residual_complete = len(residual_rows) == 1 and residual_rows[0]["valid_for_claim"] == "false"
    residual_missing_fields = [
        "M_H_ref",
        "GM_orbit",
        "G_ref",
        "Delta_charge_current",
        "Delta_frame",
        "Delta_Poisson",
        "Delta_Gauss",
        "Delta_orbit",
        "Delta_G",
        "mu_extra_over_GM",
        "delta_beta_source_guard",
        "source_path",
    ]
    residual_missing = all("MISSING_" in residual_rows[0][field] for field in residual_missing_fields)
    anti_active = len(anti_rows) == 5 and all(row["current_status"] == "guard_active" for row in anti_rows)
    leakage_complete = len(leakage_rows) == 7 and all(row["valid_for_claim"] == "false" for row in leakage_rows)
    gates_block = len(gate_rows) == 10 and all(row["result"].startswith("fail") for row in gate_rows)
    no_claim_rows = all_valid_for_claim_false(rows_by_name)
    snc_pg_blocked = snc_pg.get("result") == "fail_missing_PG_orbital_calibration"
    mh_fill_blocked = mh_fill.get("value") == "MISSING_CERTIFIED_POSITIVE_M_H_REF" and mh_fill.get("valid_for_claim") == "false"
    next_selected = any(row["next_action"] == NEXT_TARGET for row in decision_rows_) and any(
        row["next_target"] == NEXT_TARGET for row in summary_rows
    )
    formalization_count = formalization_changed_count()
    output_paths = [
        DOC_PATH,
        RESIDUALS / "P8_Y5_R10_698_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_698_PG_MHREF_BRIDGE_THEOREM_ATTEMPT.csv",
        RESIDUALS / "P8_Y5_R10_698_ARROW_OBSTRUCTION_AUDIT.csv",
        RESIDUALS / "P8_Y5_R10_698_CALIBRATION_RESIDUAL_BOUND_ROW.csv",
        RESIDUALS / "P8_Y5_R10_698_OBSERVABLE_LEAKAGE_MAP.csv",
        RESIDUALS / "P8_Y5_R10_698_ANTI_CIRCULARITY_GUARD.csv",
        RESIDUALS / "P8_Y5_R10_698_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_698_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_698_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_698_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_698_VALIDATION.csv",
    ]
    scoped_outputs = all(str(path).startswith(str(ROOT)) for path in output_paths)
    checks = [
        ("V698_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V698_1_prior_validations_clean", all(count == 0 for count in prior_failure_counts.values()), ";".join(f"{key}={value}" for key, value in prior_failure_counts.items())),
        ("V698_2_PG_contract_nonclaim", pg_nonclaim, f"pg_rows={len(pg_rows)}"),
        ("V698_3_697_PG_gate_blocked", snc_pg_blocked, f"SNC697_5={snc_pg.get('result', 'missing')}"),
        ("V698_4_bridge_theorem_complete_failed", bridge_complete and bridge_failed, f"bridge_rows={len(bridge_rows)}"),
        ("V698_5_obstruction_audit_complete", obstruction_complete, f"obstruction_rows={len(obstruction_rows_)}"),
        ("V698_6_residual_bound_unfilled", residual_complete and residual_missing, "epsilon_PG_MHref_abs row keeps missing markers"),
        ("V698_7_anti_circularity_active", anti_active, f"guard_rows={len(anti_rows)}"),
        ("V698_8_leakage_map_complete", leakage_complete, f"leakage_rows={len(leakage_rows)}"),
        ("V698_9_claim_gates_block", gates_block, f"gate_rows={len(gate_rows)}"),
        ("V698_10_MHref_fill_still_blocked", mh_fill_blocked, f"MHR697_value={mh_fill.get('value', 'missing')}"),
        ("V698_11_no_claim_rows_promoted", no_claim_rows, "all generated 698 rows remain valid_for_claim=false"),
        ("V698_12_next_target_selected", next_selected, NEXT_TARGET),
        ("V698_13_generated_outputs_scoped", scoped_outputs, "all 698 outputs target post-checkpoint-work"),
        ("V698_14_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V698_15_status_nonclaim", "no_MHref_value" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
    ]
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now,
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, divider, *body]) + "\n"


def write_doc(
    source_rows: list[dict[str, str]],
    bridge_rows: list[dict[str, str]],
    obstruction_rows_: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    leakage_rows: list[dict[str, str]],
    anti_rows: list[dict[str, str]],
    evaluator_rows_: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation_rows_: list[dict[str, str]],
) -> None:
    doc = f"""# 698 - Y5 R10 Hamiltonian Charge To Poisson Gauss MHref Calibration Or Residual Bound

## Verdict

698 tries to derive the denominator bridge:

```text
H_tau[S] - H_ref  ->  Pi_M J_H  ->  nabla^2 Phi = 4*pi*G_ref rho_H
                 ->  surface_integral grad Phi.dS = 4*pi*G_ref M_H_ref
                 ->  GM_orbit = G_ref M_H_ref
```

The bridge has the right GR-shaped chain, but the current corpus does not own the arrows. The cleanest obstruction is not algebraic; it is calibration ownership. We cannot use observed `GM_orbit` to define `M_H_ref` until the Poisson/Gauss/orbital readout is derived from the same Hamiltonian/Hilbert charge.

So 698 writes the exact conditional theorem and an explicit fallback residual:

```text
epsilon_PG_MHref_abs = |GM_orbit/G_ref - M_H_ref| / M_H_ref
```

That residual is still unfilled. No measured-GM, Newton, PPN, R10, or local-GR claim follows.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## PG MHref Bridge Theorem Attempt

{markdown_table(bridge_rows, ["theorem_id", "bridge_clause", "observed_state", "result", "residual_if_fail", "valid_for_claim"])}

## Arrow Obstruction Audit

{markdown_table(obstruction_rows_, ["obstruction_id", "residual_quantity", "failure_mode", "effect_on_MHref", "current_status", "valid_for_claim"])}

## Calibration Residual Bound Row

{markdown_table(residual_rows, ["bound_id", "quantity", "definition", "M_H_ref", "GM_orbit", "G_ref", "Delta_Gauss", "Delta_orbit", "valid_for_claim"])}

## Observable Leakage Map

{markdown_table(leakage_rows, ["leak_id", "target", "leakage", "claim_effect", "valid_for_claim"])}

## Anti-Circularity Guard

{markdown_table(anti_rows, ["guard_id", "rule", "reason", "current_status", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator_rows_, ["eval_id", "target", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gate_rows, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows_, ["check_id", "result", "detail"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    bridge_rows = bridge_theorem_rows()
    obstruction_rows_ = obstruction_rows()
    residual_rows = residual_bound_rows()
    leakage_rows = observable_leakage_rows()
    anti_rows = anti_circularity_rows()
    evaluator_rows_ = evaluator_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    summary_rows = nonclaim_summary_rows()
    validation_rows_ = validation_rows(
        source_rows,
        bridge_rows,
        obstruction_rows_,
        residual_rows,
        leakage_rows,
        anti_rows,
        evaluator_rows_,
        gate_rows,
        decision_rows_,
        summary_rows,
    )

    write_csv(RESIDUALS / "P8_Y5_R10_698_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_698_PG_MHREF_BRIDGE_THEOREM_ATTEMPT.csv", bridge_rows, ["theorem_id", "bridge_clause", "mathematical_form", "observed_state", "result", "residual_if_fail", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_698_ARROW_OBSTRUCTION_AUDIT.csv", obstruction_rows_, ["obstruction_id", "residual_quantity", "failure_mode", "effect_on_MHref", "current_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_698_CALIBRATION_RESIDUAL_BOUND_ROW.csv", residual_rows, ["bound_id", "quantity", "definition", "expanded_bound", "M_H_ref", "GM_orbit", "G_ref", "Delta_charge_current", "Delta_frame", "Delta_Poisson", "Delta_Gauss", "Delta_orbit", "Delta_G", "mu_extra_over_GM", "delta_beta_source_guard", "units", "source_path", "derivation_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_698_OBSERVABLE_LEAKAGE_MAP.csv", leakage_rows, ["leak_id", "target", "leakage", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_698_ANTI_CIRCULARITY_GUARD.csv", anti_rows, ["guard_id", "rule", "reason", "current_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_698_EVALUATOR.csv", evaluator_rows_, ["eval_id", "target", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_698_CLAIM_GATE_EVALUATION.csv", gate_rows, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_698_DECISION.csv", decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_698_NONCLAIM_SUMMARY.csv", summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_698_VALIDATION.csv", validation_rows_, ["check_id", "result", "detail", "generated_utc"])

    write_doc(source_rows, bridge_rows, obstruction_rows_, residual_rows, leakage_rows, anti_rows, evaluator_rows_, gate_rows, decision_rows_, summary_rows, validation_rows_)

    failures = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"bridge_rows={len(bridge_rows)}")
    print(f"obstruction_rows={len(obstruction_rows_)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
