from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3137_CONSTANT_STANDARD_INPUTS.csv"
THEOREM = OUT / "P8_Y5_R2FR_3137_MATERIAL_STANDARD_SUPERSELECTION_THEOREM.csv"
REDUCTION = OUT / "P8_Y5_R2FR_3137_REPRESENTATION_LABEL_REDUCTION.csv"
FALLBACK = OUT / "P8_Y5_R2FR_3137_CONSTANT_STANDARD_RESIDUAL_FALLBACK.csv"
GATE = OUT / "P8_Y5_R2FR_3137_GATE.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3137_VALIDATION.csv"


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
    sources = [
        ("SRC3137_0", "3136_clock_owner", "3136-Y5-R2FR-observed-coframe-clock-functional-owner-under-AX1090.md", "clock functional theorem handoff"),
        ("SRC3137_1", "3136_residuals", "source-intake\\mts_residuals\\P8_Y5_R2FR_3136_CLOCK_OWNER_RESIDUALS.csv", "b_clock/b_mass/b_alpha residual rows"),
        ("SRC3137_2", "949_parent_constant_clause", "949-Y5-R10-parent-constant-sector-superselection-action-clause-or-finite-source-coefficient-input.md", "constant/source parent clause candidate"),
        ("SRC3137_3", "948_superselection_attempt", "source-intake\\mts_residuals\\P8_Y5_R10_948_CONSTANT_SUPERSELECTION_THEOREM_ATTEMPT.csv", "constant superselection theorem attempt"),
        ("SRC3137_4", "no_species_contract", "source-intake\\mts_residuals\\P8_no_species_source_charge_CONTRACT.csv", "S0-S7 no-species/source-charge contract"),
        ("SRC3137_5", "763_no_marker_spurion", "source-intake\\mts_residuals\\P8_Y5_R10_763_NO_MARKER_SPURION_THEOREM_ATTEMPT.csv", "no marker/spurion theorem attempt"),
        ("SRC3137_6", "953_no_species_functor", "953-Y5-R10-no-species-label-source-functor-theorem-or-filled-coefficient-intake-review.md", "source-functor label-forgetting theorem"),
        ("SRC3137_7", "988_alpha_joint_gate", "988-Y5-R10-alphaEM-WEP-clock-joint-prior-or-EM-lock-theorem.md", "joint alpha clock/WEP/EM gate"),
        ("SRC3137_8", "989_EM_lock", "source-intake\\mts_residuals\\P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv", "EM-lock signature audit"),
        ("SRC3137_9", "988_clock_product_import", "source-intake\\mts_residuals\\P8_Y5_R10_988_CLOCK_PRODUCT_IMPORT.csv", "clock alpha product bound import"),
        ("SRC3137_10", "988_WEP_alpha_pressure", "source-intake\\mts_residuals\\P8_Y5_R10_988_WEP_ALPHA_PRESSURE_IMPORT.csv", "WEP alpha pressure import"),
        ("SRC3137_11", "990_parent_action_contract", "990-Y5-R10-minimal-parent-action-coupling-contract-EM-matter-GR-reentry.md", "minimal parent action coupling contract"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, role, source_file, evidence_use in sources:
        path = source_path(source_file)
        rows.append(
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
    return rows


def theorem_rows() -> list[dict[str, Any]]:
    now = stamp()
    return [
        {
            "theorem_id": "MST3137_0_target",
            "statement": "Material clock constants are theorem-zero if they are representation/superselection labels of the quotient matter bundle, not fields on the parent configuration.",
            "mathematical_form": "theta_A in Rep(Q_obs) with d_parent theta_A=0 and Lie_v theta_A=0 for v in ker(Dq)",
            "proof_status": "target_sharpened",
            "what_closes_if_signed": "b_clock,b_mass,b_alpha vanish at the material-standard level",
            "blocking_gap": "parent Rep(Q_obs) construction and no-marker clause are not signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MST3137_1_chain_rule",
            "statement": "If S_matter descends through q and theta_A are external quotient labels, vertical variations cannot change material constants.",
            "mathematical_form": "Lie_v S_matter = <delta Sbar/delta q,Dq[v]> + partial_theta Sbar Lie_v theta_A = 0",
            "proof_status": "formal_pass_conditional",
            "what_closes_if_signed": "clock matter action remains blind to internal-flow sign",
            "blocking_gap": "matter functor and theta silence remain unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MST3137_2_clock_standard",
            "statement": "Clock transition frequencies are quotient-owned if the transition Hamiltonian uses only e_obs and theta_A.",
            "mathematical_form": "nu_A=nu_A(theta_A,e_obs local tetrad); Lie_v nu_A=0 if Lie_v theta_A=Lie_v e_obs=0",
            "proof_status": "formal_pass_conditional",
            "what_closes_if_signed": "b_clock=0 and kappa_alpha*tau_clock_time has no marker contribution",
            "blocking_gap": "constant-sector universality and observed coframe descent are not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MST3137_3_mass_standard",
            "statement": "Rest masses and material mass ratios are quotient-owned only if mass labels are representation data, not marker fields.",
            "mathematical_form": "m_A=m_A(theta_A) with Lie_v m_A=0; no m_A(Xhat,m_marker)",
            "proof_status": "conditional_but_countermodel_open",
            "what_closes_if_signed": "b_mass=0 and WEP/clock mass-standard drift is killed",
            "blocking_gap": "species_internal_constants countermodel remains legal until no-marker parent clause closes",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MST3137_4_alpha_EM",
            "statement": "alpha_EM is quotient-owned if the parent signs charge lattice, unique Maxwell F2 normalization, current owner, and readout descent.",
            "mathematical_form": "Lie_v ln alpha_EM=0 from T_Q owner + unique F_Q^2 + quotient Hodge/coframe readout",
            "proof_status": "conditional_exact_but_EM_lock_unsigned",
            "what_closes_if_signed": "b_alpha=0 across clocks, WEP/Coulomb, R10, and EM stress",
            "blocking_gap": "EM-lock signature audit remains unsigned and unique-F2 counterexample is active",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MST3137_5_source_label_forgetting",
            "statement": "Universal source normalization follows only after the source functor forgets species labels.",
            "mathematical_form": "F_src(T_H)=kappa_univ T_H; labelled F_src({(T_A,A)})=sum_A kappa_A T_A remains a countermodel",
            "proof_status": "conditional_theorem_countermodel_retained",
            "what_closes_if_signed": "source-normalization species split and beta_source can collapse structurally",
            "blocking_gap": "parent source category label-forgetting quotient is not derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MST3137_6_verdict",
            "statement": "The material-standard zero route is mathematically clean but still not parent-owned.",
            "mathematical_form": "q/e_obs/S_matter/Rep(Q_obs)/EM-lock/source-label-forgetting signed => b_clock=b_mass=b_alpha=0",
            "proof_status": "not_parent_signed_current_corpus",
            "what_closes_if_signed": "3136 clock theorem becomes much closer to an actual local SR/GR clock reduction",
            "blocking_gap": "requires one parent action branch containing all clauses, not separate closure contracts",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def reduction_rows() -> list[dict[str, Any]]:
    now = stamp()
    rows = [
        ("REP3137_0_not_a_field", "theta_A not in Field(S_parent)", "insufficient_alone", "prevents direct Euler variation only", "theta_A could still be marker-dependent metadata unless parent grammar excludes it"),
        ("REP3137_1_rep_label", "theta_A is a label of a quotient matter representation", "best_zero_route", "Lie_v theta_A=0 follows if v acts only in ker(Dq) and representation labels are fixed", "must construct Rep(Q_obs) and forbid marker-indexed representation choice"),
        ("REP3137_2_charge_lattice", "charge and alpha normalization fixed by parent charge lattice and unique F2", "best_alpha_route", "b_alpha=0 if EM-lock is parent-signed", "unique Maxwell F2 and current normalization remain unsigned"),
        ("REP3137_3_material_marker", "theta_A=theta_A(marker,Xhat)", "countermodel_active", "explains why metric/coframe descent alone does not kill clock constants", "must be forbidden by no-marker/no-shadow theorem or bounded"),
        ("REP3137_4_labelled_source", "source functor sees labelled species currents", "countermodel_active", "allows kappa_A while preserving covariance/additivity", "must prove source-domain label forgetting"),
        ("REP3137_5_finite_fallback", "retain b_clock,b_mass,b_alpha,beta_source if signatures fail", "executable_nonclaim", "gives empirical route without pretending zero", "needs numeric source-backed rows or theorem-zero"),
    ]
    return [
        {
            "reduction_id": row_id,
            "route": route,
            "status": status,
            "what_it_buys": buys,
            "remaining_gap": gap,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for row_id, route, status, buys, gap in rows
    ]


def fallback_rows() -> list[dict[str, Any]]:
    now = stamp()
    rows = [
        ("CFR3137_0_b_clock", "b_clock", "Lie_v ln nu_A", "clock/redshift/alpha drift", "MISSING_REP_LABEL_CLOCK_STANDARD_ZERO_OR_BOUND", "3136 residual RES3136_0"),
        ("CFR3137_1_b_mass", "b_mass", "Lie_v ln m_A", "WEP/clock/source normalization", "MISSING_REP_LABEL_MASS_STANDARD_ZERO_OR_BOUND", "3136 residual RES3136_1"),
        ("CFR3137_2_b_alpha", "b_alpha", "Lie_v ln alpha_EM", "alpha-sensitive clocks; WEP/Coulomb; EM stress", "MISSING_EM_LOCK_ZERO_OR_ALPHA_PRODUCT_INPUT", "3136 residual RES3136_2 and 988 joint alpha gate"),
        ("CFR3137_3_beta_source_alpha", "beta_source_alpha", "source-normalized alpha/Coulomb force coupling", "MICROSCOPE/WEP", "MISSING_SOURCE_LABEL_FORGETTING_OR_BETA_SOURCE_INPUT", "988 WEP alpha pressure import"),
        ("CFR3137_4_kappa_alpha_tau", "kappa_alpha_tau_clock_time", "clock product entering alpha-sensitive frequency ratios", "Yb/AlHg clock bounds", "MISSING_CLOCK_PRODUCT_ZERO_OR_PARENT_INPUT", "949/988 clock product rows"),
        ("CFR3137_5_species_kappa", "Delta_kappa_AB", "relative source weight if labels survive", "WEP/source normalization/Newton GM", "MISSING_LABEL_FORGETTING_OR_FINITE_SOURCE_WEIGHT_BOUND", "953 labelled source countermodel"),
    ]
    return [
        {
            "fallback_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "observable_link": observable,
            "current_status": status,
            "lineage": lineage,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "next_action": "prove parent zero route or provide numeric source-backed finite row",
            "generated_utc": now,
        }
        for row_id, symbol, definition, observable, status, lineage in rows
    ]


def gate_rows(theorems: list[dict[str, Any]], fallbacks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    now = stamp()
    conditional_rows = sum(1 for row in theorems if "conditional" in row.get("proof_status", ""))
    fallback_missing = sum(1 for row in fallbacks if "MISSING" in row.get("current_status", ""))
    return [
        {
            "gate_id": "MSG3137_0_material_standard_zero",
            "gate": "b_clock_b_mass_zero",
            "status": "formal_pass_conditional_not_parent_signed",
            "claim_allowed": "false",
            "reason": "representation-label route would kill clock/mass standard drift, but Rep(Q_obs) and no-marker grammar are unsigned",
            "next_action": "construct Rep(Q_obs) parent clause or fill b_clock/b_mass bound rows",
            "generated_utc": now,
        },
        {
            "gate_id": "MSG3137_1_alpha_EM_zero",
            "gate": "b_alpha_zero",
            "status": "conditional_exact_but_EM_lock_unsigned",
            "claim_allowed": "false",
            "reason": "charge lattice/unique-F2/current/readout descent would lock alpha_EM, but EM-lock signature is not parent-signed",
            "next_action": "attack unique Maxwell F2/current owner or keep b_alpha finite",
            "generated_utc": now,
        },
        {
            "gate_id": "MSG3137_2_source_label_forgetting",
            "gate": "no_relative_source_weights",
            "status": "conditional_theorem_countermodel_retained",
            "claim_allowed": "false",
            "reason": "no-label source functor gives one kappa_univ, but labelled additive functor remains legal",
            "next_action": "derive source-domain label forgetting or bound Delta_kappa_AB",
            "generated_utc": now,
        },
        {
            "gate_id": "MSG3137_3_total",
            "gate": "clock_constants_parent_ownership",
            "status": "not_claim_ready",
            "claim_allowed": "false",
            "reason": f"{conditional_rows} theorem rows are conditional and {fallback_missing} finite fallback rows remain missing",
            "next_action": "3138 should attack explicit q/Obs_e/Rep(Q_obs) construction or unique Maxwell F2 inheritance",
            "generated_utc": now,
        },
    ]


def validation_rows(inputs: list[dict[str, Any]], theorems: list[dict[str, Any]], reductions: list[dict[str, Any]], fallbacks: list[dict[str, Any]], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    now = stamp()
    all_sources = all(row["exists"] == "true" for row in inputs)
    has_core_residuals = {"b_clock", "b_mass", "b_alpha"}.issubset({row["symbol"] for row in fallbacks})
    has_countermodels = any(row["status"] == "countermodel_active" for row in reductions)
    no_claim = all(str(row.get("claim_allowed", "")).lower() == "false" and str(row.get("valid_for_claim", "false")).lower() == "false" for row in theorems + reductions + fallbacks)
    gates_no_claim = all(str(row.get("claim_allowed", "")).lower() == "false" for row in gates)
    return [
        {
            "check_id": "VAL3137_0_sources_exist",
            "status": "pass" if all_sources else "fail",
            "details": json.dumps({row["source_id"]: {"exists": row["exists"], "path": row["resolved_path"]} for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3137_1_theorem_reduction_written",
            "status": "pass" if len(theorems) >= 7 and any(row["theorem_id"] == "MST3137_4_alpha_EM" for row in theorems) else "fail",
            "details": f"theorem_rows={len(theorems)}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3137_2_countermodels_retained",
            "status": "pass" if has_countermodels else "fail",
            "details": f"reduction_rows={len(reductions)}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3137_3_core_residuals_retained",
            "status": "pass" if has_core_residuals and len(fallbacks) >= 6 else "fail",
            "details": json.dumps([row["symbol"] for row in fallbacks], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3137_4_no_claim_leak",
            "status": "pass" if no_claim and gates_no_claim else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    theorems = theorem_rows()
    reductions = reduction_rows()
    fallbacks = fallback_rows()
    gates = gate_rows(theorems, fallbacks)
    validations = validation_rows(inputs, theorems, reductions, fallbacks, gates)
    write_csv(INPUTS, inputs)
    write_csv(THEOREM, theorems)
    write_csv(REDUCTION, reductions)
    write_csv(FALLBACK, fallbacks)
    write_csv(GATE, gates)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()

