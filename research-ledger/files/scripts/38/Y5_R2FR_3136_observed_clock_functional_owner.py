from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3136_CLOCK_OWNER_INPUTS.csv"
THEOREM = OUT / "P8_Y5_R2FR_3136_OBSERVED_CLOCK_FUNCTIONAL_THEOREM.csv"
DERIVATION = OUT / "P8_Y5_R2FR_3136_CLOCK_MATTER_DERIVATION_CHAIN.csv"
RESIDUALS = OUT / "P8_Y5_R2FR_3136_CLOCK_OWNER_RESIDUALS.csv"
GATE = OUT / "P8_Y5_R2FR_3136_GATE.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3136_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path_text


def input_rows() -> list[dict[str, Any]]:
    rows = [
        ("SRC3136_0", "3135_readout_gate", "3135-Y5-R2FR-clock-readout-chain-sign-quarantine-and-limit-gate-under-AX1090.md", "readout-chain predecessor"),
        ("SRC3136_1", "3135_gate", "source-intake\\mts_residuals\\P8_Y5_R2FR_3135_GATE.csv", "sign quarantine and R_clock/q gate"),
        ("SRC3136_2", "3135_limits", "source-intake\\mts_residuals\\P8_Y5_R2FR_3135_SR_GR_LIMIT_EXPANSION.csv", "SR/GR/Newton/null/EM limit rows"),
        ("SRC3136_3", "155_clock_owner", "155-redshift-projection-clock-map-owner.md", "observer-clock map owner warning"),
        ("SRC3136_4", "156_clock_functional", "156-clock-projection-functional-theorem-or-demotion.md", "clock functional target and matter-clock coupling gap"),
        ("SRC3136_5", "943_coframe_contract", "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md", "single observed coframe matter coupling contract"),
        ("SRC3136_6", "944_quotient_descent", "944-Y5-R10-quotient-observed-coframe-descent-proof-or-frame-leak-source-bounds.md", "quotient observed-coframe descent proof gate"),
        ("SRC3136_7", "3134_reduction", "source-intake\\mts_residuals\\P8_Y5_R2FR_3134_PROOF_REDUCTION_MATRIX.csv", "matter pullback chain-rule predecessor"),
        ("SRC3136_8", "3135_residual_vector", "source-intake\\mts_residuals\\P8_Y5_R2FR_3135_TIME_SIGN_RESIDUAL_VECTOR.csv", "clock/readout residual vector"),
    ]
    annotated: list[dict[str, Any]] = []
    for source_id, role, source_file, evidence_use in rows:
        path = source_path(source_file)
        annotated.append(
            {
                "source_id": source_id,
                "role": role,
                "source_file": source_file,
                "resolved_path": str(path),
                "exists": str(path.exists()).lower(),
                "row_count": len(read_csv(path)) if path.exists() and path.suffix.lower() == ".csv" else "",
                "evidence_use": evidence_use,
                "valid_for_claim": "false",
            }
        )
    return annotated


def theorem_rows() -> list[dict[str, Any]]:
    now = stamp()
    return [
        {
            "theorem_id": "OCF3136_0_target",
            "clause": "observed clock functional",
            "statement": "R_clock is owned if ordinary clock matter is a local Lorentz matter system over e_obs and quotient-owned material constants.",
            "mathematical_form": "R_clock(q(Phi),gamma,A)=integral_gamma sqrt(-g_obs(dx,dx))/c plus species transition functional nu_A(theta_A)",
            "status": "theorem_target_sharp",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "OCF3136_1_WKB_phase",
            "clause": "clock phase from matter action",
            "statement": "For minimally coupled localized massive matter, the eikonal phase obeys the observed Hamilton-Jacobi equation.",
            "mathematical_form": "g_obs^{mu nu} partial_mu S partial_nu S + m_A(theta)^2 c^2 = 0",
            "status": "formal_pass_conditional",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "OCF3136_2_proper_time",
            "clause": "proper-time functional",
            "statement": "The worldline action/phase extremal gives the clock elapsed time functional.",
            "mathematical_form": "S_pp=-m_A c^2 integral d tau_clk; d tau_clk=sqrt(-g_obs_{mu nu} dx^mu dx^nu)/c",
            "status": "formal_pass_conditional",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "OCF3136_3_redshift_frequency",
            "clause": "redshift from clock phase",
            "statement": "Clock comparison is a ratio of observed proper-time phase rates, not the raw internal flow parameter.",
            "mathematical_form": "nu_A^obs ~ dS_A/dtau_clk; Delta nu/nu uses e_obs,g_obs and quotient-owned theta_A",
            "status": "formal_pass_conditional",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "OCF3136_4_material_constants",
            "clause": "constants and standards",
            "statement": "Masses, charges, alpha_EM, and transition constants must be quotient-owned/superselected, or clock residuals remain.",
            "mathematical_form": "Lie_v theta_A=0, Lie_v m_A=0, Lie_v alpha_EM=0; otherwise b_clock,b_mass,b_alpha retained",
            "status": "not_parent_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "OCF3136_5_parent_verdict",
            "clause": "current MTS clock owner verdict",
            "statement": "The clock functional theorem is mathematically clean under standard matter descent, but current parent ownership is not proven.",
            "mathematical_form": "q/e_obs/S_matter/theta descent => R_clock owned; missing any premise => residual vector active",
            "status": "conditional_theorem_not_promoted",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def derivation_rows() -> list[dict[str, Any]]:
    now = stamp()
    return [
        {
            "step_id": "DER3136_0_assume_coframe_descent",
            "step": "Assume e_obs=Obs_e(q(Phi)) and v in ker(Dq).",
            "result": "Lie_v e_obs=0 by chain rule.",
            "gap": "q and Obs_e are not parent-constructed in current corpus.",
            "status": "conditional_step",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "DER3136_1_assume_clock_matter_functor",
            "step": "Assume clock matter action depends on parent geometry only through e_obs and quotient-owned theta_A.",
            "result": "No internal-flow sign can enter the clock except through e_obs or theta_A.",
            "gap": "matter functor and theta_A silence remain unsigned.",
            "status": "conditional_step",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "DER3136_2_WKB_limit",
            "step": "Take the localized/eikonal limit of ordinary massive matter.",
            "result": "Hamilton-Jacobi equation gives observed timelike worldlines and proper time.",
            "gap": "requires ordinary matter minimal coupling and no representative mass marker.",
            "status": "formal_pass_conditional",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "DER3136_3_clock_functional",
            "step": "Define the clock observable as accumulated phase per quotient-owned transition frequency.",
            "result": "R_clock reduces to observed metric proper time plus material-constant residuals.",
            "gap": "transition constants/alpha/mass ratios need quotient ownership or bounds.",
            "status": "formal_pass_conditional",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "DER3136_4_sign_quarantine",
            "step": "Let tau_flow run with any internal sign convention.",
            "result": "Observable sign is controlled by e_obs proper time unless tau_flow leaks into e_obs or theta_A.",
            "gap": "direct readout/constant leakage heads from 3134/3135 remain active.",
            "status": "conditional_sign_quarantine_preserved",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "step_id": "DER3136_5_failure_mode",
            "step": "If m_A, alpha_EM, or transition constants depend on the internal flow/representative marker, the theorem fails cleanly.",
            "result": "The failure becomes b_clock,b_mass,b_alpha,or epsilon_clock_readout_direct.",
            "gap": "first finite source/bound row needed if no zero theorem.",
            "status": "fallback_residual_required",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    now = stamp()
    rows = [
        ("RES3136_0_b_clock", "b_clock", "Lie_v ln nu_A for a material clock transition", "clock/redshift/alpha drift", "MISSING_CONSTANT_DESCENT_OR_CLOCK_BOUND"),
        ("RES3136_1_b_mass", "b_mass", "Lie_v ln m_A for clock/rest-mass standard", "WEP/clock/source normalization", "MISSING_MASS_DESCENT_OR_BOUND"),
        ("RES3136_2_b_alpha", "b_alpha", "Lie_v ln alpha_EM or EM transition coupling", "alpha-sensitive clocks/EM", "MISSING_ALPHA_SUPERSELECTION_OR_PRODUCT_INPUT"),
        ("RES3136_3_delta_e_clock", "delta_e_clock", "representative leakage into observed coframe clock functional", "SR/GR/redshift/PPN", "MISSING_C_Obs_e_AND_C_shadow_abs_ZERO_OR_BOUND"),
        ("RES3136_4_nonminimal_clock", "epsilon_nonminimal_clock", "nonminimal curvature/flow coupling in clock matter action", "clock/PPN/local_GR", "MISSING_NO_NONMINIMAL_CLOCK_COUPLING_THEOREM"),
        ("RES3136_5_tau_role", "epsilon_tau_role", "same clock/source/charge/orbit/boundary tau mismatch", "Newton/Hamiltonian/clock", "MISSING_SAME_TAU_NORMALIZATION_THEOREM"),
    ]
    return [
        {
            "residual_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "observable_link": observable,
            "current_status": status,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "next_action": "prove theorem-zero from parent descent or provide source-backed finite bound",
            "generated_utc": now,
        }
        for row_id, symbol, definition, observable, status in rows
    ]


def gate_rows(theorems: list[dict[str, Any]], residuals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    now = stamp()
    conditional_passes = sum(1 for row in theorems if "conditional" in row.get("status", ""))
    missing_residuals = sum(1 for row in residuals if "MISSING" in row.get("current_status", ""))
    return [
        {
            "gate_id": "OCG3136_0_clock_functional",
            "gate": "R_clock_from_observed_coframe_matter",
            "status": "formal_pass_conditional",
            "claim_allowed": "false",
            "reason": "WKB/point-particle clock matter over e_obs gives observed proper time.",
            "next_action": "parent-sign q/e_obs/matter/theta descent.",
            "generated_utc": now,
        },
        {
            "gate_id": "OCG3136_1_parent_ownership",
            "gate": "parent_q_Obs_e_matter_theta_descent",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": "943/944/3134 keep q, Obs_e, matter functor, and constants/masses unsigned.",
            "next_action": "construct explicit q:Phi->Q_obs and Obs_e(q), or retain frame/clock residuals.",
            "generated_utc": now,
        },
        {
            "gate_id": "OCG3136_2_time_sign",
            "gate": "internal_flow_sign",
            "status": "quarantined_if_no_direct_leak",
            "claim_allowed": "false",
            "reason": "wrong-sign internal flow is harmless only if it does not enter e_obs or material constants.",
            "next_action": "attack b_clock/b_alpha/delta_e_clock zero theorem.",
            "generated_utc": now,
        },
        {
            "gate_id": "OCG3136_3_total",
            "gate": "clock_SR_GR_claim",
            "status": "not_claim_ready",
            "claim_allowed": "false",
            "reason": f"{conditional_passes} theorem rows are conditional and {missing_residuals} residual rows still carry missing markers.",
            "next_action": "3137 should target constants/material-standard quotient ownership or explicit q/Obs_e construction.",
            "generated_utc": now,
        },
    ]


def validation_rows(inputs: list[dict[str, Any]], theorems: list[dict[str, Any]], derivations: list[dict[str, Any]], residuals: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    now = stamp()
    all_sources_exist = all(row["exists"] == "true" for row in inputs)
    no_claim_leak = all(str(row.get("claim_allowed", "")).lower() == "false" and str(row.get("valid_for_claim", "false")).lower() == "false" for row in theorems + derivations + residuals)
    gates_false = all(str(row.get("claim_allowed", "")).lower() == "false" for row in gates)
    has_wkb = any(row.get("theorem_id") == "OCF3136_1_WKB_phase" for row in theorems)
    has_residuals = len(residuals) >= 6 and all("MISSING" in row.get("current_status", "") for row in residuals)
    return [
        {
            "check_id": "VAL3136_0_sources_exist",
            "status": "pass" if all_sources_exist else "fail",
            "details": json.dumps({row["source_id"]: {"exists": row["exists"], "path": row["resolved_path"]} for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3136_1_clock_theorem_has_WKB_and_proper_time",
            "status": "pass" if has_wkb and any(row.get("theorem_id") == "OCF3136_2_proper_time" for row in theorems) else "fail",
            "details": f"theorem_rows={len(theorems)}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3136_2_derivation_chain_complete",
            "status": "pass" if len(derivations) >= 6 else "fail",
            "details": f"derivation_rows={len(derivations)}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3136_3_residuals_retained",
            "status": "pass" if has_residuals else "fail",
            "details": f"residual_rows={len(residuals)}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3136_4_no_claim_leak",
            "status": "pass" if no_claim_leak and gates_false else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    theorems = theorem_rows()
    derivations = derivation_rows()
    residuals = residual_rows()
    gates = gate_rows(theorems, residuals)
    validations = validation_rows(inputs, theorems, derivations, residuals, gates)
    write_csv(INPUTS, inputs)
    write_csv(THEOREM, theorems)
    write_csv(DERIVATION, derivations)
    write_csv(RESIDUALS, residuals)
    write_csv(GATE, gates)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
