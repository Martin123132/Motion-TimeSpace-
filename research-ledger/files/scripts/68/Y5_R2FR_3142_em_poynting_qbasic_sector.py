from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3142_INPUTS.csv"
THEOREM = OUT / "P8_Y5_R2FR_3142_EM_QBASIC_THEOREM.csv"
STRESS = OUT / "P8_Y5_R2FR_3142_POYNTING_STRESS_READOUT.csv"
RESIDUAL = OUT / "P8_Y5_R2FR_3142_EM_ZERO_OR_RESIDUAL_ROW.csv"
GATE = OUT / "P8_Y5_R2FR_3142_GATE.csv"
DECISION = OUT / "P8_Y5_R2FR_3142_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3142_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(relative: str) -> str:
    return str((ROOT / relative).resolve())


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def input_rows() -> list[dict[str, str]]:
    now = stamp()
    rows = [
        {
            "source_id": "SRC3142_0_3141_doc",
            "path": source_path("3141-Y5-R2FR-strong-qbasic-total-action-clause-under-AX1090.md"),
            "role": "selects EM/Poynting q-basic sector theorem",
        },
        {
            "source_id": "SRC3142_1_3141_contract",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R2FR_3141_TOTAL_ACTION_CONTRACT.csv"
            ),
            "role": "EM sector total-action contract",
        },
        {
            "source_id": "SRC3142_2_642_maxwell",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv"),
            "role": "Maxwell descent gates and alpha blocker",
        },
        {
            "source_id": "SRC3142_3_765_norm",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R10_765_VERTICAL_GENERATOR_NORM_THEOREM_ATTEMPT.csv"
            ),
            "role": "vertical generator norm theorem attempt",
        },
        {
            "source_id": "SRC3142_4_1057_unique",
            "path": source_path(
                "1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md"
            ),
            "role": "unique Maxwell subblock/no independent F2 attempt",
        },
        {
            "source_id": "SRC3142_5_1058_operator",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv"
            ),
            "role": "visible operator-domain exhaustion attempt",
        },
        {
            "source_id": "SRC3142_6_1099_EM_owner",
            "path": source_path(
                "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md"
            ),
            "role": "unique EM kinetic owner and alpha coefficient row",
        },
        {
            "source_id": "SRC3142_7_1100_TQ",
            "path": source_path(
                "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"
            ),
            "role": "T_Q/gauge norm and charge lattice owner attempt",
        },
        {
            "source_id": "SRC3142_8_1101_gauge_owner",
            "path": source_path(
                "1101-Y5-R10-gauge-fibre-level-index-monopole-Ward-owner-or-alpha-product-route.md"
            ),
            "role": "gauge norm owner hunt and no-go shortcut ledger",
        },
        {
            "source_id": "SRC3142_9_alpha_clock",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"
            ),
            "role": "finite alpha clock product bound",
        },
        {
            "source_id": "SRC3142_10_alpha_wep",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R10_1052_ALPHA_WEP_PROJECTION_LEDGER.csv"
            ),
            "role": "finite alpha WEP product target",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def theorem_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "theorem_id": "EMQ3142_0_qbasic_sector",
            "statement": "Assume L_EM=q^*(-1/4 Z_Q mu_obs F_Q^2)+dB_EM, with Z_Q=C_P N_Q fixed by parent/representation data.",
            "proof_or_status": "definition of q-basic EM sector; Z_Q must be q-owned or representation-fixed",
            "current_status": "conditional_premise_not_parent_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "EMQ3142_1_no_extra_F2",
            "statement": "No independent lambda_A F_Q^2, f_X(Xhat)F_Q^2, or radiative/readout regenerated F_Q^2 is allowed.",
            "proof_or_status": "required by operator-domain exhaustion; ordinary covariance and U(1) do not supply it",
            "current_status": "not_parent_signed_counterterms_retained",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "EMQ3142_2_balpha_zero",
            "statement": "If EMQ3142_0 and EMQ3142_1 hold and hbar,c/readout are quotient-fixed, then b_alpha=Lie_v ln alpha_EM=0 for v in ker(Dq).",
            "proof_or_status": "chain rule: Lie_v Z_Q=0 and no non-q-owned EM coefficient remains",
            "current_status": "exact_conditional_theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "EMQ3142_3_Maxwell_equations",
            "statement": "Variation of the q-basic Maxwell sector gives dF_Q=0 and d*_obs(Z_Q F_Q)=J_Q if A_Q/current owner is included.",
            "proof_or_status": "standard Maxwell variation on observed coframe with fixed Z_Q; current owner still required",
            "current_status": "conditional_theorem_current_owner_unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "EMQ3142_4_Hilbert_stress",
            "statement": "Hilbert variation gives T_EM^{mu nu}=Z_Q(F^{mu rho}F^nu_rho - 1/4 g_obs^{mu nu}F^2).",
            "proof_or_status": "metric variation of the owned Maxwell scalar density; projector/readout dependence excluded by q-basic premise",
            "current_status": "conditional_theorem_poynting_readout_available",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "EMQ3142_5_Poynting",
            "statement": "Observed Poynting flux is the spatial energy-flux component of T_EM in the observed tetrad: S^i=-T_EM^{i}_{ 0}.",
            "proof_or_status": "readout from Hilbert stress in e_obs; no separate Poynting axiom is needed",
            "current_status": "conditional_theorem_if_EM_sector_owned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "EMQ3142_6_verdict",
            "statement": "The EM/Poynting readout is derivable from a q-basic Maxwell sector, but that sector is not parent-owned in the current corpus.",
            "proof_or_status": "1057/1099/1100/1101 keep T_Q norm, no-extra-F2, current owner, and readout/radiative guard unsigned",
            "current_status": "not_claim_ready",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def stress_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "readout_id": "EMS3142_0_action",
            "object": "owned Maxwell action",
            "formula": "S_EM=-1/4 int mu_obs Z_Q F_Q^{mu nu}F^Q_{mu nu}",
            "requires": "Z_Q fixed by parent T_Q/gauge norm and no independent F2 slots",
            "status": "conditional",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "readout_id": "EMS3142_1_stress",
            "object": "Hilbert EM stress tensor",
            "formula": "T_EM^{mu nu}=Z_Q(F^{mu rho}F^nu_rho - 1/4 g_obs^{mu nu}F^2)",
            "requires": "same observed coframe and q-basic Z_Q",
            "status": "conditional_derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "readout_id": "EMS3142_2_poynting",
            "object": "Poynting flux",
            "formula": "S^i=-T_EM^i_0 in an observed tetrad; equivalent to observed E x H with the same Z_Q convention",
            "requires": "observed tetrad e_obs and owned Maxwell stress",
            "status": "conditional_derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "readout_id": "EMS3142_3_source",
            "object": "EM current/source",
            "formula": "J_Q=delta S_matter/delta A_Q, with charge labels fixed in Rep(Q_obs)",
            "requires": "same T_Q current owner and no q_A(Xhat)/c_A current weights",
            "status": "conditional_current_owner_unsigned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def residual_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "row_id": "EMR3142_0_theorem_zero_candidate",
            "quantity": "b_alpha_EM",
            "definition": "Lie_v ln alpha_EM from EM kinetic/readout sector",
            "value_or_status": "0_if_EMQ3142_0_to_1_and_readout_guard_signed_else_MISSING",
            "units": "dimensionless vertical derivative",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3142_EM_QBASIC_THEOREM.csv"),
            "generated_utc": now,
        },
        {
            "row_id": "EMR3142_1_finite_Z_residual",
            "quantity": "zeta_EM",
            "definition": "Lie_v ln Z_EM_total where Z_EM_total=C_P N_Q + lambda_A + f_X + delta_lambda_rad + readout",
            "value_or_status": "MISSING_PARENT_COEFFICIENT_OR_ZERO_THEOREM",
            "units": "dimensionless vertical derivative",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_path": source_path("1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"),
            "generated_utc": now,
        },
        {
            "row_id": "EMR3142_2_poynting_residual",
            "quantity": "Delta_T_EM",
            "definition": "non-q-basic correction to Hilbert EM stress/Poynting readout from hidden F2 coefficient or readout re-entry",
            "value_or_status": "MISSING_OPERATOR_DOMAIN_OR_READOUT_CLOSURE",
            "units": "stress-energy density scale times dimensionless coefficient",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_path": source_path("1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md"),
            "generated_utc": now,
        },
        {
            "row_id": "EMR3142_3_current_residual",
            "quantity": "beta_source_alpha",
            "definition": "source/test EM current normalization residual if the same T_Q current owner is unsigned",
            "value_or_status": "MISSING_CURRENT_OWNER_AND_ARENA_PROJECTION",
            "units": "dimensionless",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "source_path": source_path("1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"),
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "gate_id": "EMG3142_0_conditional_theorem",
            "gate": "EM_qbasic_to_Maxwell_stress_Poynting",
            "status": "pass_conditional_theorem",
            "claim_allowed": "false",
            "reason": "Hilbert stress/Poynting readout follows if the EM sector is q-basic",
            "generated_utc": now,
        },
        {
            "gate_id": "EMG3142_1_parent_EM_sector",
            "gate": "parent_TQ_norm_no_extra_F2_current_readout_signed",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": "T_Q norm, no-extra-F2, same current owner, and readout/radiative guard remain unsigned",
            "generated_utc": now,
        },
        {
            "gate_id": "EMG3142_2_balpha",
            "gate": "b_alpha_zero_or_finite_prediction",
            "status": "not_claim_ready",
            "claim_allowed": "false",
            "reason": "zero theorem not signed and finite zeta_EM coefficient is missing",
            "generated_utc": now,
        },
        {
            "gate_id": "EMG3142_3_WEP_R10_clock",
            "gate": "clock_WEP_R10_alpha_transfer",
            "status": "not_claim_ready",
            "claim_allowed": "false",
            "reason": "tau/source-test/material projection inputs remain missing for finite alpha products",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "decision_id": "EMD3142_0_derivation",
            "decision": "EM_Poynting_readout_derived_conditionally_from_qbasic_Maxwell_sector",
            "reason": "Hilbert variation of owned q-basic Maxwell action gives stress tensor; Poynting is its observed energy-flux component",
            "effect": "Poynting is not a separate axiom if EM sector ownership closes",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "EMD3142_1_zero_claim",
            "decision": "do_not_claim_balpha_zero",
            "reason": "no-extra-F2 and gauge-norm owner are not derived in current corpus",
            "effect": "retain zeta_EM/b_alpha_EM finite residual rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "EMD3142_2_next",
            "decision": "fill_first_finite_alpha_product_or_source_current_owner",
            "reason": "zero route has been sharpened; next empirical/theory discipline is either zeta_EM product inputs or same-current source owner",
            "effect": "3143 should choose finite alpha product input fill unless user wants another zero-owner hunt",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    theorem: list[dict[str, str]],
    stress: list[dict[str, str]],
    residual: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    conditional_theorem = any(
        row["theorem_id"] == "EMQ3142_4_Hilbert_stress"
        and row["current_status"] == "conditional_theorem_poynting_readout_available"
        for row in theorem
    )
    poynting_written = any(row["readout_id"] == "EMS3142_2_poynting" for row in stress)
    residuals_retained = {"b_alpha_EM", "zeta_EM", "Delta_T_EM", "beta_source_alpha"}.issubset(
        {row["quantity"] for row in residual}
    )
    gates_block = all(row["claim_allowed"] == "false" for row in gates)
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decisions)
    return [
        {
            "check_id": "V3142_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3142_1_conditional_theorem_written",
            "status": "pass" if conditional_theorem else "fail",
            "details": f"theorem_rows={len(theorem)}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3142_2_poynting_readout_written",
            "status": "pass" if poynting_written else "fail",
            "details": f"stress_rows={len(stress)}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3142_3_residual_rows_retained",
            "status": "pass" if residuals_retained else "fail",
            "details": json.dumps([row["quantity"] for row in residual], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3142_4_no_claim_leak",
            "status": "pass" if gates_block and decisions_nonclaim else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    theorem = theorem_rows()
    stress = stress_rows()
    residual = residual_rows()
    gates = gate_rows()
    decisions = decision_rows()
    validations = validation_rows(inputs, theorem, stress, residual, gates, decisions)
    write_csv(INPUTS, inputs)
    write_csv(THEOREM, theorem)
    write_csv(STRESS, stress)
    write_csv(RESIDUAL, residual)
    write_csv(GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
