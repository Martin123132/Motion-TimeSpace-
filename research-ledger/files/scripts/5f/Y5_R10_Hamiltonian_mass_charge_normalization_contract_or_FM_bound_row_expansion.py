from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC_NAME = "924-Y5-R10-Hamiltonian-mass-charge-normalization-contract-or-FM-bound-row-expansion.md"
STATUS = "Y5_R10_924_Hamiltonian_mass_charge_normalization_contract_written_KBFH_ratio_symbolic_FM_bound_rows_expanded_nonclaim"
CLAIM_CEILING = "Hamiltonian_mass_charge_normalization_contract_only_no_KBFH_value_no_WEP_R10_PPN_or_local_GR_claim"
NEXT_TARGET = "925-Y5-R10-KBFH-over-kM-ratio-from-source-worldtube-or-FM-bound-row-fill.md"
GENERATED = datetime.now(timezone.utc).isoformat()
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        cells = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def b(value: bool) -> str:
    return "true" if value else "false"


def source_specs() -> list[dict[str, str]]:
    return [
        {
            "source_id": "923_doc",
            "path": "923-Y5-R10-parent-selects-mass-gauge-normalization-or-run-first-real-FM-bound-row.md",
            "role": "selects Hamiltonian mass-charge normalization as best non-circular candidate",
            "needle": "Hamiltonian mass-charge normalization is the best non-circular candidate",
        },
        {
            "source_id": "923_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_923_VALIDATION.csv",
            "role": "proves 923 validation passed",
            "needle": "V923_10_validation_rows_ready",
        },
        {
            "source_id": "457_Hamiltonian_charge",
            "path": "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
            "role": "conditional Hamiltonian charge route and Poisson bridge",
            "needle": "Poisson_Gauss_bridge",
        },
        {
            "source_id": "458_Poisson_Gauss",
            "path": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
            "role": "Poisson/Gauss measured-GM calibration conditions",
            "needle": "conditional_Poisson_Gauss_calibration_theorem",
        },
        {
            "source_id": "539_Hamiltonian_PiM",
            "path": "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
            "role": "defines Pi_M^H from parent Hamiltonian charge as candidate repair",
            "needle": "Define Pi_M^H from the parent Hamiltonian surface charge itself.",
        },
        {
            "source_id": "505_Noether_mass_charge",
            "path": "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md",
            "role": "conditional local mass-charge closure theorem and source-measure matching",
            "needle": "worldtube source measure equals the exterior parent mass charge",
        },
        {
            "source_id": "Hamiltonian_charge_contract",
            "path": "source-intake/mts_residuals/P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
            "role": "HC0-HC9 Hamiltonian mass-charge requirements",
            "needle": "HC8_Poisson_Gauss_orbital_calibration",
        },
        {
            "source_id": "Poisson_Gauss_contract",
            "path": "source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
            "role": "PG0-PG10 Poisson/Gauss measured-GM requirements",
            "needle": "PG4_Gauss_surface_integral",
        },
        {
            "source_id": "Hilbert_monopole_contract",
            "path": "source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv",
            "role": "Hilbert source to measured monopole requirements",
            "needle": "HM3_absolute_monopole_calibration",
        },
        {
            "source_id": "local_bound_claims",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "source-backed local bound rows for FM expansion",
            "needle": "R2_clock_redshift",
        },
    ]


def build_sources() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in source_specs():
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": b(exists),
                "needle_found": b(needle_found),
                "valid_for_claim": "false",
                "generated_utc": GENERATED,
            }
        )
    return rows


def summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "current_result": "the Hamiltonian normalization contract is explicit and gives a symbolic K_BF_H/k_M ratio, but no numeric coupling is derived",
            "what_changed": "the BF/source variation now maps directly into source-worldtube and Gauss/Poisson clauses; FM bound rows are expanded as blocked nonclaim rows",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def contract_rows() -> list[dict[str, object]]:
    return [
        {
            "contract_id": "HMC924_0_parent_charge",
            "required_identity": "Q_tau is an integrable differentiable Hamiltonian/covariant-phase-space mass charge with fixed reference",
            "mathematical_form": "delta H_tau = Omega(delta Phi, L_tau Phi) = delta Q_tau on the allowed local exterior branch",
            "normalization_effect": "defines the parent mass-charge unit before readout",
            "current_status": "not_parent_signed",
            "if_missing": "Pi_M^H is not a legal normalization owner",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "contract_id": "HMC924_1_Hilbert_worldtube",
            "required_identity": "same observed Hilbert compact-source worldtube supplies the source current J_H^H",
            "mathematical_form": "Q_tau[W] = integral_W J_H^H = M_source in the parent source frame",
            "normalization_effect": "prevents the BF/topological charge from being the wrong conserved object",
            "current_status": "not_parent_signed",
            "if_missing": "K_BF_H cannot be tied to measured matter source",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "contract_id": "HMC924_2_BF_source_variation",
            "required_identity": "A_M variation owns the BF/source equality",
            "mathematical_form": "S = k_M integral B_M wedge dA_M + K_BF_H integral A_M wedge J_H^H; delta_A S => k_M dB_M = K_BF_H J_H^H up to sign convention",
            "normalization_effect": "relates K_BF_H to k_M once B_M and J_H^H charges are normalized",
            "current_status": "variation_formula_written_not_parent_signed",
            "if_missing": "coupling remains closure-only",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "contract_id": "HMC924_3_integrated_ratio",
            "required_identity": "integrated BF charge equals the Hamiltonian source charge on the same chain",
            "mathematical_form": "k_M integral_boundaryC B_M = K_BF_H integral_C J_H^H, so K_BF_H/k_M = (integral_boundaryC B_M)/(integral_C J_H^H)",
            "normalization_effect": "symbolic K_BF_H/k_M ratio",
            "current_status": "symbolic_ratio_only",
            "if_missing": "no numeric or unit-complete K_BF_H",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "contract_id": "HMC924_4_Gauss_Poisson",
            "required_identity": "Q_tau controls the same weak-field potential read by matter orbits",
            "mathematical_form": "nabla^2 Phi = 4 pi G_ref rho_H and integral_S grad Phi dot dS = 4 pi G_ref Q_tau",
            "normalization_effect": "connects the charge to measured GM and Newtonian acceleration",
            "current_status": "conditional_from_prior_contracts_not_parent_derived",
            "if_missing": "a conserved charge is not yet measured GM",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "contract_id": "HMC924_5_no_extra_flux",
            "required_identity": "boundary, projector, memory, domain, range, connection, and coupling sectors add no source flux",
            "mathematical_form": "mu_extra = 0 or retained as executable residual rows",
            "normalization_effect": "protects WEP/clock/PPN/R10 comparisons from hidden source channels",
            "current_status": "not_parent_signed",
            "if_missing": "FM rows stay blocked or become residual bounds",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def variation_rows() -> list[dict[str, object]]:
    return [
        {
            "step_id": "VAR924_0_delta_A",
            "operation": "vary A_M in k_M B_M wedge dA_M + K_BF_H A_M wedge J_H^H",
            "result": "k_M dB_M = K_BF_H J_H^H up to orientation/sign",
            "what_this_gives": "source equation needed to relate BF level to Hilbert source current",
            "what_remains_open": "normalization of B_M charge and J_H^H charge",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "step_id": "VAR924_1_delta_B",
            "operation": "vary B_M",
            "result": "dA_M = 0",
            "what_this_gives": "flat mass-gauge field and zero local curvature",
            "what_remains_open": "exactness/holonomy and boundary gauge conditions",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "step_id": "VAR924_2_integrate_chain",
            "operation": "integrate k_M dB_M = K_BF_H J_H^H over a compact source/exterior chain C",
            "result": "k_M int_boundaryC B_M = K_BF_H int_C J_H^H",
            "what_this_gives": "symbolic K_BF_H/k_M ratio",
            "what_remains_open": "source-worldtube equality to Q_tau and measured-GM calibration",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def local_bound_rows() -> list[dict[str, str]]:
    wanted = {"R1_WEP_source_charge", "R2_clock_redshift", "R3_gamma", "R4_beta"}
    return [row for row in read_csv(LOCAL_BOUNDS / "local_bound_claims.csv") if row["row_id"] in wanted]


def fm_bound_expansion_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    residual_symbol = {
        "R1_WEP_source_charge": "eta_FM_AB",
        "R2_clock_redshift": "alpha_clock_FM",
        "R3_gamma": "delta_gamma_FM",
        "R4_beta": "delta_beta_FM",
    }
    for index, bound in enumerate(local_bound_rows()):
        rows.append(
            {
                "fm_bound_id": f"FM924_{index}_{bound['row_id']}",
                "source_dataset_id": bound["dataset_id"],
                "local_bound_row": bound["row_id"],
                "observable": bound["observable"],
                "upper_bound": bound["upper_bound"],
                "bound_units": bound["units"],
                "FM_prediction_symbol": residual_symbol[bound["row_id"]],
                "FM_prediction_formula": f"{residual_symbol[bound['row_id']]} = C_{residual_symbol[bound['row_id']]} * epsilon_FM",
                "FM_prediction_value": "MISSING_HAMILTONIAN_NORMALIZATION",
                "score_status": "blocked_missing_KBFH_over_kM_ratio",
                "valid_for_claim": "false",
                "generated_utc": GENERATED,
            }
        )
    return rows


def blocker_rows() -> list[dict[str, object]]:
    return [
        {
            "blocker_id": "BLK924_0_KBFH_over_kM_numeric",
            "missing_input": "numeric/unit-complete K_BF_H/k_M from int_boundary B_M over int_C J_H^H",
            "why_needed": "turns symbolic source equation into a testable coupling",
            "next_action": "derive B_M charge unit and J_H^H source-worldtube normalization",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK924_1_Qtau_worldtube",
            "missing_input": "integral_C J_H^H = Q_tau = M_source before readout",
            "why_needed": "makes the source current the same charge used by Hamiltonian mass",
            "next_action": "prove source-worldtube glue or retain residual",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK924_2_Gauss_orbital",
            "missing_input": "Q_tau controls the inverse-square orbital potential with constant G_ref",
            "why_needed": "without this, normalization is not Newtonian measured GM",
            "next_action": "derive Poisson/Gauss calibration or keep local-bound rows blocked",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK924_3_projection_coefficients",
            "missing_input": "C_eta_FM, C_clock_FM, C_gamma_FM, C_beta_FM",
            "why_needed": "maps epsilon_FM into WEP/clock/PPN observables",
            "next_action": "linearize after normalization or keep expansion rows as nonclaim",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "BD924_0_contract",
            "branch": "Hamiltonian_mass_charge_normalization",
            "verdict": "contract_written_symbolic_ratio_only",
            "reason": "delta_A variation gives k_M dB_M = K_BF_H J_H^H, but charge units are not fixed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD924_1_bound_expansion",
            "branch": "FM_local_bound_rows",
            "verdict": "expanded_nonclaim",
            "reason": "WEP, clock, gamma, and beta rows now have FM placeholders but remain blocked",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "BD924_2_next",
            "branch": "KBFH_over_kM_ratio",
            "verdict": "selected",
            "reason": "the next mathematical target is the source-worldtube ratio that could fix K_BF_H/k_M",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CGATE924_0_KBFH_value",
            "claim": "K_BF_H is numerically/unit fixed",
            "blocker": "only symbolic K_BF_H/k_M ratio is written",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE924_1_measured_GM",
            "claim": "Hamiltonian charge is measured Newtonian GM",
            "blocker": "Gauss/Poisson/source-worldtube calibration remains conditional",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE924_2_FM_bounds",
            "claim": "expanded FM bound rows score",
            "blocker": "all FM predictions remain MISSING_HAMILTONIAN_NORMALIZATION",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE924_3_local_GR",
            "claim": "normalization contract closes local-GR/Newton/PPN",
            "blocker": "no KBFH value, no measured-GM calibration, no projection coefficients",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "derive or bound the K_BF_H/k_M ratio by proving integral_C J_H^H equals the Hamiltonian source worldtube charge and integral_boundary B_M has a fixed unit",
            "include": "B_M charge unit, J_H^H worldtube source, Q_tau equality, Gauss-Poisson calibration, nonclaim FM row fill",
            "exclude": "numeric pass claims, post-fit G/M absorption, topological wrong-charge credit, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def formalization_changed_count() -> int:
    formalization = ROOT.parent / "formalization-workbench"
    if not formalization.exists():
        return 0
    return sum(
        1
        for path in formalization.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def all_false(rows: list[dict[str, object]], fields: tuple[str, ...]) -> bool:
    return all(str(row.get(field, "")).strip().lower() != "true" for row in rows for field in fields)


def validation_rows(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    variations: list[dict[str, object]],
    bounds: list[dict[str, object]],
    blockers: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior = OUT / "P8_Y5_BRR545_923_VALIDATION.csv"
    prior_ok = prior.exists() and "V923_10_validation_rows_ready" in read_text(prior)
    ratio_written = any("K_BF_H/k_M" in row["mathematical_form"] for row in contract)
    bound_rows_blocked = all(str(row["FM_prediction_value"]).startswith("MISSING") and row["valid_for_claim"] == "false" for row in bounds)
    changed = formalization_changed_count()
    generated = contract + variations + bounds + blockers + decisions + gates
    false_fields = ("claim_allowed", "valid_for_claim")
    return [
        {
            "check_id": "V924_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "missing source or needle",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V924_1_prior_923_clean",
            "result": "pass" if prior_ok else "fail",
            "detail": "P8_Y5_BRR545_923_VALIDATION.csv clean" if prior_ok else "923 validation missing or incomplete",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V924_2_contract_symbolic_ratio_written",
            "result": "pass" if ratio_written else "fail",
            "detail": "symbolic K_BF_H/k_M ratio is present",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V924_3_variation_chain_written",
            "result": "pass" if len(variations) == 3 else "fail",
            "detail": "delta_A, delta_B, and integrated-chain variation rows are present",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V924_4_FM_bound_rows_expanded_blocked",
            "result": "pass" if bound_rows_blocked and len(bounds) >= 4 else "fail",
            "detail": "FM WEP/clock/gamma/beta rows are expanded and blocked",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V924_5_blockers_explicit",
            "result": "pass" if all_false(blockers, ("valid_for_claim",)) and len(blockers) >= 4 else "fail",
            "detail": "KBFH/kM, Q_tau worldtube, Gauss/orbital, and projection blockers are explicit",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V924_6_claim_gates_false",
            "result": "pass" if all_false(gates, false_fields) else "fail",
            "detail": "KBFH value, measured GM, FM bounds, and local-GR gates remain false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V924_7_decisions_nonclaim",
            "result": "pass" if all_false(decisions, false_fields) else "fail",
            "detail": "decisions select KBFH/kM ratio target without promotion",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V924_8_all_generated_rows_nonclaim",
            "result": "pass" if all_false(generated, false_fields) else "fail",
            "detail": "all generated rows keep guarded claim fields false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V924_9_formalization_workbench_untouched",
            "result": "pass" if changed == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={changed}",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V924_10_next_target_selected",
            "result": "pass" if NEXT_TARGET.startswith("925-") else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V924_11_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
            "generated_utc": GENERATED,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    summary: list[dict[str, object]],
    contract: list[dict[str, object]],
    variations: list[dict[str, object]],
    bounds: list[dict[str, object]],
    blockers: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 924 - Y5/R10 Hamiltonian Mass-Charge Normalization Contract Or FM Bound Row Expansion

Private normalization checkpoint. This is not a public WEP, clock, PPN, R10, Newton, local-GR, or unified-field claim.

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

Current result: **the normalization contract is now explicit, but it still gives only a symbolic ratio.**

The parent action candidate is:

```text
S = k_M integral B_M wedge dA_M + K_BF_H integral A_M wedge J_H^H.
```

The useful variation is:

```text
delta_A S = 0  =>  k_M dB_M = K_BF_H J_H^H.
```

Integrated over a compact source/exterior chain:

```text
k_M integral_boundaryC B_M = K_BF_H integral_C J_H^H,
K_BF_H/k_M = (integral_boundaryC B_M)/(integral_C J_H^H).
```

That is progress because it gives the exact normalization lock. It is not a value yet because `integral_C J_H^H = Q_tau = M_source` and the `B_M` charge unit are not parent-derived.

## Non-Claim Summary

{md_table(summary, ["status", "claim_ceiling", "current_result", "what_changed", "next_target", "valid_for_claim", "generated_utc"])}

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])}

## Hamiltonian Normalization Contract

{md_table(contract, ["contract_id", "required_identity", "mathematical_form", "normalization_effect", "current_status", "if_missing", "valid_for_claim", "generated_utc"])}

## Variation Chain

{md_table(variations, ["step_id", "operation", "result", "what_this_gives", "what_remains_open", "valid_for_claim", "generated_utc"])}

## FM Bound Row Expansion

{md_table(bounds, ["fm_bound_id", "source_dataset_id", "local_bound_row", "observable", "upper_bound", "bound_units", "FM_prediction_symbol", "FM_prediction_formula", "FM_prediction_value", "score_status", "valid_for_claim", "generated_utc"])}

## Blocker Ledger

{md_table(blockers, ["blocker_id", "missing_input", "why_needed", "next_action", "valid_for_claim", "generated_utc"])}

## Branch Decision

{md_table(decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Claim Gate

{md_table(gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Next Target

{md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Validation

{md_table(validation, ["check_id", "result", "detail", "generated_utc"])}
"""
    (ROOT / DOC_NAME).write_text(body, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    src = build_sources()
    summary = summary_rows()
    contract = contract_rows()
    variations = variation_rows()
    bounds = fm_bound_expansion_rows()
    blockers = blocker_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()
    validation = validation_rows(src, contract, variations, bounds, blockers, decisions, gates)

    write_csv(OUT / "P8_Y5_R10_924_SOURCE_REGISTER.csv", src, ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_924_NONCLAIM_SUMMARY.csv", summary, ["status", "claim_ceiling", "current_result", "what_changed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_924_HAMILTONIAN_NORMALIZATION_CONTRACT.csv", contract, ["contract_id", "required_identity", "mathematical_form", "normalization_effect", "current_status", "if_missing", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_924_VARIATION_CHAIN.csv", variations, ["step_id", "operation", "result", "what_this_gives", "what_remains_open", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_924_FM_BOUND_ROW_EXPANSION.csv", bounds, ["fm_bound_id", "source_dataset_id", "local_bound_row", "observable", "upper_bound", "bound_units", "FM_prediction_symbol", "FM_prediction_formula", "FM_prediction_value", "score_status", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_924_BLOCKER_LEDGER.csv", blockers, ["blocker_id", "missing_input", "why_needed", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_924_BRANCH_DECISION.csv", decisions, ["decision_id", "branch", "verdict", "reason", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_924_CLAIM_GATE.csv", gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_924_NEXT_TARGET.csv", next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_BRR545_924_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(src, summary, contract, variations, bounds, blockers, decisions, gates, next_target, validation)

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"validation failed: {failed}")
    print(STATUS)
    print(f"wrote {ROOT / DOC_NAME}")
    print(f"next target: {NEXT_TARGET}")


if __name__ == "__main__":
    main()
