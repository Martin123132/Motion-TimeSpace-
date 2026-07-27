from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "936-Y5-R10-Hamiltonian-PiM-integrability-or-N5-beta-coefficient-source-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "935_doc",
            "path": "935-Y5-R10-N5-projector-stress-zero-or-retained-beta-bound-input.md",
            "role": "N5 did not close and selected Hamiltonian PiM as next derivation route",
            "needle": "N5 does not close yet",
        },
        {
            "source_id": "935_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_935_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V935_11_validation_rows_ready",
        },
        {
            "source_id": "909_doc",
            "path": "909-Y5-R10-Hamiltonian-PiM-charge-map-or-retained-projector-PPN-source-pack.md",
            "role": "candidate Hamiltonian PiM definition",
            "needle": "Pi_M^H J_H := M_H[S,tau] omega_M^H",
        },
        {
            "source_id": "910_doc",
            "path": "910-Y5-R10-Hamiltonian-PiM-integrability-reference-subgate-or-retained-source-pack-fill.md",
            "role": "integrability one-form obstruction",
            "needle": "d alpha_tau = integral_S i_tau omega",
        },
        {
            "source_id": "911_doc",
            "path": "911-Y5-R10-parent-symplectic-current-minimal-contract-or-Delta-symp-bound-input.md",
            "role": "parent symplectic current contract",
            "needle": "parent_symplectic_current_contract_built_Delta_symp_bound_input_staged_nonclaim",
        },
        {
            "source_id": "663_pim_repair",
            "path": "source-intake/mts_residuals/P8_Y5_R10_663_PIM_REPAIR_OR_DEMOTION.csv",
            "role": "PiM repair route and residual fallback",
            "needle": "PR663_0_define_PiM_H",
        },
        {
            "source_id": "664_integrability",
            "path": "source-intake/mts_residuals/P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv",
            "role": "older integrability verdict",
            "needle": "HCI664_6_integrability_verdict",
        },
        {
            "source_id": "664_source_equality",
            "path": "source-intake/mts_residuals/P8_Y5_R10_664_SOURCE_EQUALITY_ATTEMPT.csv",
            "role": "older source-equality verdict",
            "needle": "HSE664_6_source_equality_verdict",
        },
        {
            "source_id": "910_obstruction_pack",
            "path": "source-intake/mts_residuals/P8_Y5_R10_910_OBSTRUCTION_PACK.csv",
            "role": "retained Delta_symp obstruction inputs",
            "needle": "OBS910_0_Delta_symp",
        },
        {
            "source_id": "909_retained_source_pack",
            "path": "source-intake/mts_residuals/P8_Y5_R10_909_RETAINED_PROJECTOR_SOURCE_PACK.csv",
            "role": "projector/source residual source pack",
            "needle": "RSP909_0_symplectic_integrability_residual",
        },
    ]
    rows = []
    for spec in specs:
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def integrability_audit() -> list[dict[str, str]]:
    specs = [
        (
            "HPI936_0_candidate_definition",
            "candidate_charge_map",
            "Pi_M^H J_H := M_H[S,tau] omega_M^H",
            "conditional_definition_only",
            "needs parent-owned M_H, surface S, generator tau, and mass one-form omega_M^H",
            "not_parent_owned",
        ),
        (
            "HPI936_1_integrability_one_form",
            "covariant_phase_space_integrability",
            "alpha_tau(delta Phi)=int_S(delta Q_tau-i_tau Theta); d alpha_tau=int_S i_tau omega + delta_tau/reference terms",
            "exact_obstruction_identified",
            "must prove int_S i_tau omega_total=0 on allowed local exterior variations with fixed tau/reference",
            "not_zeroed",
        ),
        (
            "HPI936_2_parent_omega",
            "parent_symplectic_current",
            "omega_total=omega_EH+omega_X+omega_boundary+omega_domain+omega_source",
            "open_blocker",
            "MTS has not supplied Theta/omega for every non-EH sector",
            "missing_parent_input",
        ),
        (
            "HPI936_3_fixed_reference_tau",
            "reference_and_time_generator_lock",
            "delta tau=0, delta H_ref=0, and fixed asymptotic/local observed-time normalization",
            "open_blocker",
            "reference rule and observed source/readout frame are not parent-signed",
            "missing_reference_input",
        ),
        (
            "HPI936_4_same_source_frame",
            "source_measure_equality",
            "Hamiltonian charge equals observed Hilbert/source mass in the same worldtube and readout frame",
            "open_blocker",
            "worldtube glue, measured-GM calibration, and source denominator policy are not derived",
            "missing_source_equality",
        ),
        (
            "HPI936_5_topological_equivalence",
            "old_PiM_to_Hamiltonian_PiM_equivalence",
            "Pi_M^top J_H = Pi_M^H J_H + dB with int_boundary dB=0",
            "open_blocker",
            "zero-flux topological equivalence and commutator silence are unsigned",
            "missing_zero_flux_equivalence",
        ),
        (
            "HPI936_6_verdict",
            "Hamiltonian_PiM_gate",
            "Pi_M^H would solve N5 at the root only if HPI936_1 through HPI936_5 close",
            "promising_but_blocked",
            "Delta_symp, B_zero_flux, fixed reference, tau frame, and same-source equality remain retained residuals",
            "not_parent_owned_current_claim_false",
        ),
    ]
    return [
        {
            "audit_id": audit_id,
            "gate": gate,
            "mathematical_content": mathematical_content,
            "status": status,
            "blocker": blocker,
            "verdict": verdict,
            "promotion_allowed_now": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for audit_id, gate, mathematical_content, status, blocker, verdict in specs
    ]


def n5_beta_coefficient_pack() -> list[dict[str, str]]:
    specs = [
        (
            "NBC936_0_Delta_symp",
            "Delta_symp",
            "normalized obstruction from int_S i_tau omega_total",
            "dimensionless_after_M_ref_or_beta_normalization",
            "MISSING_PARENT_OMEGA_OR_BOUND",
        ),
        (
            "NBC936_1_Delta_ref",
            "Delta_ref",
            "Hamiltonian reference/zero-point shift leaking into source mass or beta",
            "dimensionless_after_M_ref_normalization",
            "MISSING_FIXED_REFERENCE_RULE",
        ),
        (
            "NBC936_2_Delta_tau_frame",
            "Delta_tau_frame",
            "observed-time generator normalization mismatch",
            "dimensionless",
            "MISSING_TAU_NORMALIZATION",
        ),
        (
            "NBC936_3_Delta_cal",
            "Delta_cal",
            "Hamiltonian charge to observed Hilbert/source mass calibration tail",
            "dimensionless",
            "MISSING_SOURCE_CALIBRATION_INPUTS",
        ),
        (
            "NBC936_4_R_Htop",
            "R_Htop",
            "residual between old topological Pi_M and Hamiltonian Pi_M^H",
            "dimensionless_or_mass_charge_ratio",
            "MISSING_HTOP_ZERO_EQUIVALENCE",
        ),
        (
            "NBC936_5_B_zero_flux",
            "B_zero_flux",
            "compact boundary exact-form flux needed to silence topological representative drift",
            "boundary_charge_or_dimensionless_flux_ratio",
            "MISSING_ZERO_FLUX_THEOREM",
        ),
        (
            "NBC936_6_I_commutator",
            "I_commutator",
            "integral_A [d,Pi_M]J_H drift in projected source current",
            "projected_source_current_units",
            "MISSING_COMMUTATOR_ZERO_OR_NUMERIC_INTEGRAL",
        ),
        (
            "NBC936_7_c_PiM_g",
            "c_PiM_g",
            "metric projector-stress coefficient produced by Pi_M variation",
            "dimensionless_after_EH_normalization",
            "MISSING_PROJECTOR_STRESS_MAP",
        ),
        (
            "NBC936_8_q_P",
            "q_P^nu",
            "Bianchi-visible divergence/current from retained projector stress",
            "force_density_or_stress_divergence_units",
            "MISSING_EXCHANGE_CURRENT_AND_RESPONSE_MAP",
        ),
        (
            "NBC936_9_C_beta_N5",
            "C_beta_N5",
            "PPN beta projection coefficient for retained N5 residual vector",
            "dimensionless",
            "MISSING_SECOND_ORDER_PPN_PROJECTION",
        ),
        (
            "NBC936_10_X_N5",
            "X_N5",
            "source-normalized N5 amplitude entering beta response",
            "dimensionless_or_source_normalized_amplitude",
            "MISSING_SOURCE_NORMALIZED_N5_AMPLITUDE",
        ),
        (
            "NBC936_11_beta_bound_formula",
            "beta_minus_one_N5",
            "|beta-1|_N5 <= 7.8e-05; |K_BF_H| <= 7.8e-05/(|C_beta_N5| X_N5)",
            "dimensionless_bound",
            "MISSING_C_BETA_N5; MISSING_X_N5; MISSING_SOURCE_NORMALIZED_SECOND_ORDER_READOUT",
        ),
    ]
    return [
        {
            "input_id": input_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "missing_before_score": missing,
            "score_ready": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for input_id, symbol, definition, units, missing in specs
    ]


def residual_priority() -> list[dict[str, str]]:
    specs = [
        (
            "PRI936_0_integrability_reference",
            "first",
            "Delta_symp; B_zero_flux; H_ref_shift",
            "without this Pi_M^H is not a well-defined parent charge and N5 cannot be killed at source",
            "937-Y5-R10-parent-omega-Delta-symp-zero-or-N5-beta-source-row-fill.md",
        ),
        (
            "PRI936_1_source_frame",
            "second",
            "Delta_frame; Delta_cal; worldtube_domain_shift",
            "Hamiltonian mass must equal observed Hilbert/source mass before local bounds mean anything",
            "source-equality worldtube/readout certificate",
        ),
        (
            "PRI936_2_commutator_projector",
            "third",
            "I_commutator; T_PiM_munu; R_PiM",
            "if the projector does not commute with exterior/source restriction it remains Bianchi-visible",
            "projector stress and commutator source pack",
        ),
        (
            "PRI936_3_topological_equivalence",
            "fourth",
            "R_Htop; dB_Htop_flux; R_eq",
            "old topological PiM can only be retained if equivalent to Hamiltonian PiM up to zero-flux exact terms",
            "topological-to-Hamiltonian equivalence theorem",
        ),
        (
            "PRI936_4_beta_readout",
            "after_source_equality",
            "C_beta_N5; X_N5; beta_minus_one_N5",
            "PPN beta row should not be scored until source equality and Hamiltonian charge ownership exist",
            "N5 beta source-backed row fill",
        ),
    ]
    return [
        {
            "priority_id": priority_id,
            "rank": rank,
            "target_inputs": target_inputs,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for priority_id, rank, target_inputs, reason, next_action in specs
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC936_0_HPiM_route",
            "decision": "Hamiltonian_PiM_remains_best_derivation_route",
            "reason": "if Pi_M is a real covariant-phase-space charge, the N5 wrong-current/projector-stress problem can disappear at the source",
            "consequence": "continue derivation-first rather than immediately fitting a beta coefficient",
            "next_action": "attack Delta_symp and parent omega",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC936_1_integrability_status",
            "decision": "integrability_not_closed",
            "reason": "d alpha_tau obstruction is known, but parent omega_total, fixed reference, tau frame, and hidden flux silence are not signed",
            "consequence": "Pi_M^H cannot be claimed parent-owned",
            "next_action": "write parent-omega/Delta_symp zero proof gate",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC936_2_N5_beta_source_pack",
            "decision": "N5_beta_coefficient_pack_staged_nonclaim",
            "reason": "if the derivation fails, beta needs C_beta_N5, X_N5, and source-backed residual amplitudes",
            "consequence": "local beta/local-GR pass remains blocked",
            "next_action": "only score after source equality and real coefficients exist",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE936_0_integrable_Htau",
            "claim": "H_tau is integrable on the allowed local exterior phase space",
            "evidence": "d alpha_tau obstruction retained; parent omega_total and flux silence missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE936_1_PiM_H_parent_owned",
            "claim": "Pi_M^H is a parent-owned replacement for old topological Pi_M",
            "evidence": "fixed reference, tau frame, source equality, and topological zero-flux equivalence remain unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE936_2_N5_beta_score",
            "claim": "N5 beta residual is numeric and scoreable",
            "evidence": "C_beta_N5, X_N5, Delta_symp, R_Htop, and q_P inputs are placeholders",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE936_3_local_GR",
            "claim": "local GR/Newton limit follows from this branch",
            "evidence": "N5 remains retained and beta/EH exterior stack is not closed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "937-Y5-R10-parent-omega-Delta-symp-zero-or-N5-beta-source-row-fill.md",
            "objective": "prove Delta_symp=0 from parent omega_total/fixed-reference conditions or fill first source-backed N5 beta coefficient row",
            "include": "parent Theta/omega sector table, int_S i_tau omega_total zero conditions, fixed tau/reference clauses, zero-flux boundary condition, fallback C_beta_N5/X_N5 source rows",
            "exclude": "assuming integrability, assuming projector zero, beta pass claim, local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified > SCRIPT_START_UTC:
            changed += 1
    return changed


def validation(
    sources: list[dict[str, str]],
    audit_rows: list[dict[str, str]],
    coefficient_rows: list[dict[str, str]],
    priority_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    prior = read_csv(OUT / "P8_Y5_BRR545_935_VALIDATION.csv")
    prior_clean = prior and all(row.get("result") == "pass" for row in prior)
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    audit_blocked = any(row["audit_id"] == "HPI936_6_verdict" and row["verdict"] == "not_parent_owned_current_claim_false" for row in audit_rows)
    no_audit_promoted = all(row["promotion_allowed_now"] == "false" for row in audit_rows)
    coefficients_blocked = coefficient_rows and all(row["score_ready"] == "false" and row["claim_allowed"] == "false" for row in coefficient_rows)
    beta_formula_present = any(row["input_id"] == "NBC936_11_beta_bound_formula" and "7.8e-05" in row["definition"] for row in coefficient_rows)
    priority_selected = any(row["priority_id"] == "PRI936_0_integrability_reference" and "Delta_symp" in row["target_inputs"] for row in priority_rows)
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decision_rows)
    claims_false = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_rows)
    next_selected = any(row["next_target"].startswith("937-Y5-R10-parent-omega-Delta-symp-zero") for row in target_rows)
    no_claims = all(
        row.get("valid_for_claim") == "false"
        for row in sources + audit_rows + coefficient_rows + priority_rows + decision_rows + claim_rows + target_rows
    )
    formalization_changed = formalization_changed_after_start()

    add("V936_0_sources_exist_and_needles", sources_ok, "all 936 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V936_1_prior_935_clean", prior_clean, "P8_Y5_BRR545_935_VALIDATION.csv clean")
    add("V936_2_integrability_verdict_blocked", audit_blocked, "HPI936_6 keeps Pi_M^H promising but not parent-owned")
    add("V936_3_no_audit_promoted", no_audit_promoted, "no Hamiltonian PiM audit row promoted")
    add("V936_4_coefficient_pack_blocked", coefficients_blocked, "all N5 beta coefficient rows are non-scoreable placeholders")
    add("V936_5_beta_bound_formula_present", beta_formula_present, "retained 7.8e-05 beta bound formula present")
    add("V936_6_priority_selected", priority_selected, "Delta_symp/B_zero_flux/reference selected as first residual target")
    add("V936_7_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V936_8_claim_gates_false", claims_false, "all claim gates remain false")
    add("V936_9_next_target_selected", next_selected, "937 parent-omega Delta_symp gate selected")
    add("V936_10_no_claims_promoted", no_claims, "all generated rows are valid_for_claim=false")
    add("V936_11_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V936_12_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    audit_rows: list[dict[str, str]],
    coefficient_rows: list[dict[str, str]],
    priority_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 936 - Y5/R10 Hamiltonian PiM Integrability Or N5 Beta Coefficient Source Pack

Generated: `{stamp()}`

Status: `Y5_R10_936_Hamiltonian_PiM_integrability_not_closed_N5_beta_coefficient_pack_staged_nonclaim`

Claim ceiling: `Pi_M_integrability_contract_and_N5_beta_source_pack_only_no_local_GR_or_beta_pass`

## Result

The Hamiltonian/covariant-phase-space route is still the cleanest way to kill the N5 projector-stress problem at the root, but it does not close yet.

The candidate replacement is:

```text
Pi_M^H J_H := M_H[S,tau] omega_M^H
```

with charge one-form:

```text
alpha_tau(delta Phi) = int_S(delta Q_tau - i_tau Theta)
d alpha_tau = int_S i_tau omega_total + delta_tau/reference terms.
```

So the derivation target is precise: prove the obstruction vanishes on the allowed local exterior phase space:

```text
int_S i_tau omega_total = 0,
delta tau = 0,
delta H_ref = 0,
hidden/projector/boundary/domain/source flux = 0,
Pi_M^top = Pi_M^H + exact zero-flux representative.
```

Current MTS does not yet supply the full parent `Theta/omega_total`, fixed reference, same-source worldtube/readout frame, or topological zero-flux equivalence. That means `Pi_M^H` remains a promising repair route, not a parent-owned current claim.

The fallback N5 beta pack is staged but not scoreable:

```text
|beta-1|_N5 <= 7.8e-05,
|K_BF_H| <= 7.8e-05/(|C_beta_N5| X_N5).
```

`C_beta_N5`, `X_N5`, `Delta_symp`, `R_Htop`, `B_zero_flux`, `I_commutator`, `c_PiM_g`, and `q_P^nu` remain missing or symbolic.

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## Hamiltonian PiM Integrability Audit

{md_table(audit_rows, ["audit_id", "gate", "mathematical_content", "status", "blocker", "verdict"])}

## N5 Beta Coefficient Source Pack

{md_table(coefficient_rows, ["input_id", "symbol", "definition", "missing_before_score", "score_ready", "claim_allowed"])}

## Residual Priority

{md_table(priority_rows, ["priority_id", "rank", "target_inputs", "reason", "next_action"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows, ["gate_id", "claim", "evidence", "claim_allowed", "valid_for_claim"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(text, encoding="utf-8")


def ensure_csv_roundtrip(paths: list[Path]) -> None:
    for path in paths:
        rows = read_csv(path)
        if rows and any(None in row for row in rows):
            raise SystemExit(f"malformed CSV row in {path}")


def main() -> None:
    sources = source_register()
    audit_rows = integrability_audit()
    coefficient_rows = n5_beta_coefficient_pack()
    priority_rows = residual_priority()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, audit_rows, coefficient_rows, priority_rows, decision_rows, claim_rows, target_rows)

    output_specs = [
        (
            OUT / "P8_Y5_R10_936_SOURCE_REGISTER.csv",
            sources,
            ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_936_HAMILTONIAN_PIM_INTEGRABILITY_AUDIT.csv",
            audit_rows,
            ["audit_id", "gate", "mathematical_content", "status", "blocker", "verdict", "promotion_allowed_now", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_936_N5_BETA_COEFFICIENT_SOURCE_PACK.csv",
            coefficient_rows,
            ["input_id", "symbol", "definition", "units", "missing_before_score", "score_ready", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_936_RESIDUAL_PRIORITY.csv",
            priority_rows,
            ["priority_id", "rank", "target_inputs", "reason", "next_action", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_936_DECISION_LEDGER.csv",
            decision_rows,
            ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_936_CLAIM_GATE.csv",
            claim_rows,
            ["gate_id", "claim", "evidence", "claim_allowed", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_R10_936_NEXT_TARGET.csv",
            target_rows,
            ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
        ),
        (
            OUT / "P8_Y5_BRR545_936_VALIDATION.csv",
            validation_rows,
            ["check_id", "result", "detail", "generated_utc"],
        ),
    ]

    for path, rows, fieldnames in output_specs:
        write_csv(path, rows, fieldnames)

    ensure_csv_roundtrip([path for path, _rows, _fieldnames in output_specs])
    write_doc(sources, audit_rows, coefficient_rows, priority_rows, decision_rows, claim_rows, target_rows, validation_rows)

    failures = [row for row in validation_rows if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")

    print("Y5_R10_936_Hamiltonian_PiM_integrability_not_closed_N5_beta_coefficient_pack_staged_nonclaim")
    print(f"wrote {DOC}")
    print("next target: 937-Y5-R10-parent-omega-Delta-symp-zero-or-N5-beta-source-row-fill.md")


if __name__ == "__main__":
    main()
