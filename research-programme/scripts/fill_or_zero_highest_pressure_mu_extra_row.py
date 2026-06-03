from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "highest_pressure_mu_extra_alpha3_gate_written_zero_theorem_not_derived_bound_product_skeleton_written_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "alpha3_mu_extra_pressure_gate_only_no_mu_extra_zero_constant_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "470-boundary-alpha3-zero-theorem-or-numeric-coefficient.md"

DOC_PATH = Path("469-fill-or-zero-highest-pressure-mu-extra-row.md")
SCORECARD_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_LOCAL_BOUND_SCORECARD.csv")
SUMMARY_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_CHANNEL_BOUND_SUMMARY.csv")
REQUIRED_INPUTS_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_SCORECARD_REQUIRED_INPUTS.csv")

SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_ALPHA3_SOURCE_REGISTER.csv")
PRESSURE_GATE_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_HIGHEST_PRESSURE_R7_ALPHA3_GATE.csv")
ZERO_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_ALPHA3_ZERO_ATTEMPT.csv")
INPUT_SKELETON_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_ALPHA3_FILL_INPUT_SKELETON.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_ALPHA3_PRESSURE_DECISION.csv")


SOURCE_REGISTER = [
    {
        "path": "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "role": "Ward/Bianchi identity shows owned hidden flux is not automatically zero",
    },
    {
        "path": "435-exterior-extra-source-nohair-owner-gate.md",
        "role": "exterior no-hair owner gate keeps alpha3 boundary/projector rows retained",
    },
    {
        "path": "467-mu-extra-zero-owner-or-source-normalization-coefficient-vector.md",
        "role": "eight-channel mu_extra coefficient vector and owner ledger",
    },
    {
        "path": "468-mu-extra-coefficient-vector-to-local-bound-scorecard.md",
        "role": "local-bound scorecard identifying R7_alpha3 as the tightest pressure row",
    },
    {
        "path": str(SCORECARD_PATH),
        "role": "machine-readable alpha3 rows and pass locks",
    },
    {
        "path": str(SUMMARY_PATH),
        "role": "channel summary showing boundary and domain tied at 4e-20",
    },
    {
        "path": str(REQUIRED_INPUTS_PATH),
        "role": "required input priorities for boundary and domain coefficient artifacts",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with (ROOT / path).open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns = list(rows[0].keys())
    with out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    columns = list(rows[0].keys())
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, str]]:
    rows = []
    for item in SOURCE_REGISTER:
        rows.append(
            {
                "source_file": item["path"],
                "exists": str((ROOT / item["path"]).exists()),
                "role": item["role"],
            }
        )
    return rows


def alpha3_rows() -> list[dict[str, str]]:
    return [row for row in read_csv(SCORECARD_PATH) if row["target_row"] == "R7_alpha3"]


def pressure_summary_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(SUMMARY_PATH)
        if row["tightest_numeric_row"] == "R7_alpha3" and row["tightest_numeric_bound"] == "4e-20"
    ]


def required_input_rows() -> list[dict[str, str]]:
    priority_channels = {"boundary_monopole_shift", "domain_projector_mass"}
    return [row for row in read_csv(REQUIRED_INPUTS_PATH) if row["unblocks_channels"] in priority_channels]


def build_pressure_gate() -> list[dict[str, Any]]:
    a_rows = alpha3_rows()
    p_rows = pressure_summary_rows()
    source_missing = [row["source_file"] for row in source_register_rows() if row["exists"] != "True"]
    channels = ";".join(row["epsilon_channel"] for row in a_rows)
    return [
        {
            "gate_id": "HP0_sources_exist",
            "result": "pass" if not source_missing else "fail",
            "evidence": "all cited 429/435/467/468 and scorecard paths exist" if not source_missing else ";".join(source_missing),
            "required_for_pass": "every cited source path exists",
            "current_decision": "usable_input_set",
        },
        {
            "gate_id": "HP1_highest_pressure_group_identified",
            "result": "pass",
            "evidence": f"{len(a_rows)} R7_alpha3 rows at bound 4e-20: {channels}",
            "required_for_pass": "tightest numeric lock selected from scorecard",
            "current_decision": "R7_alpha3 is the active pressure lock",
        },
        {
            "gate_id": "HP2_tied_group_not_singleton",
            "result": "pass" if len(p_rows) == 2 else "warn",
            "evidence": "boundary_monopole_shift and domain_projector_mass both hit alpha3=4e-20",
            "required_for_pass": "all tied channels remain active unless theorem-zero or scored",
            "current_decision": "must close both channels; no tuned cancellation allowed",
        },
        {
            "gate_id": "HP3_operational_first_row",
            "result": "pass",
            "evidence": "P8_mu_extra_boundary_coefficients.csv is priority 1 and does not require R11 operator vector",
            "required_for_pass": "choose tractable first row without dropping tied domain row",
            "current_decision": "start with boundary_monopole_shift -> R7_alpha3",
        },
        {
            "gate_id": "HP4_zero_theorem_attempt",
            "result": "fail",
            "evidence": "Ward/Bianchi ownership plus no-hair routing does not prove zero boundary or domain momentum flux",
            "required_for_pass": "derive F_alpha3[epsilon_boundary]=0 and F_alpha3[epsilon_domain_projector]=0 from parent action",
            "current_decision": "theorem-zero unavailable",
        },
        {
            "gate_id": "HP5_bound_product_skeleton",
            "result": "pass",
            "evidence": "explicit product bounds and missing coefficient inputs written",
            "required_for_pass": "write numeric/theorem-zero acceptance route without placeholder promotion",
            "current_decision": "score path exists but has no numeric prediction",
        },
        {
            "gate_id": "HP6_promotion_guard",
            "result": "pass",
            "evidence": "score_ready_rows=0 and both alpha3 predictions remain missing",
            "required_for_pass": "no Newton/PPN/local-GR claim from target-only rows",
            "current_decision": "no promotion",
        },
    ]


def build_zero_attempt() -> list[dict[str, Any]]:
    return [
        {
            "condition_id": "ZA0_alpha3_exchange_owner",
            "channel": "both",
            "exact_zero_condition": "P_loc^nu_rho (nabla^rho Gamma_eff_i - nabla_mu K_i^{mu rho}) has no local momentum-flux/vector projection",
            "theorem_status": "conditional_identity_only",
            "evidence": "429 gives the owner identity but not absence",
            "failure_mode": "owned hidden flux can still source alpha3",
            "next_action": "convert q_i^nu owner identity into channel-specific flux theorem or coefficient",
        },
        {
            "condition_id": "ZA1_boundary_flux_zero",
            "channel": "boundary_monopole_shift",
            "exact_zero_condition": "F_boundary_alpha3 := lim_S r^2 n_mu P_loc_nu K_boundary^{mu nu}/(G_eff M_eff) = 0",
            "theorem_status": "not_derived",
            "evidence": "435 keeps R7_alpha3 retained_contingent for boundary/projector exchange",
            "failure_mode": "boundary term can carry a preferred momentum flux while remaining Ward-owned",
            "next_action": "prove boundary no-hair/no-flux from parent variation or supply W_boundary_alpha3 epsilon_boundary_flux",
        },
        {
            "condition_id": "ZA2_boundary_metric_variation_silent",
            "channel": "boundary_monopole_shift",
            "exact_zero_condition": "delta_g S_boundary is pure universal scalar calibration with zero vector, shear, time, and radial derivative pieces",
            "theorem_status": "not_derived",
            "evidence": "467 marks boundary_monopole_shift retained_coefficient_required",
            "failure_mode": "dropped boundary stress would fake local GR",
            "next_action": "derive boundary no-hair or fill P8_mu_extra_boundary_coefficients.csv",
        },
        {
            "condition_id": "ZA3_domain_projector_no_leak",
            "channel": "domain_projector_mass",
            "exact_zero_condition": "F_domain_alpha3 := lim_S r^2 n_mu P_loc_nu K_domain^{mu nu}/(G_eff M_eff) = 0",
            "theorem_status": "not_derived",
            "evidence": "429 C2_projector_covariant is conditional_open for preferred-frame/location and alpha3 flux channels",
            "failure_mode": "domain/projector mass channel can leak preferred-frame momentum",
            "next_action": "derive projector no-leak theorem or supply W_domain_alpha3 epsilon_domain_flux",
        },
        {
            "condition_id": "ZA4_no_preferred_vector",
            "channel": "domain_projector_mass",
            "exact_zero_condition": "projector/domain sector contains no surviving local vector u_D^mu, gradient, or frame selector in the compact vacuum branch",
            "theorem_status": "not_derived",
            "evidence": "468 requires R11 vector artifact for the domain channel",
            "failure_mode": "a covariantly owned vector can still generate alpha1/alpha2/alpha3/xi rows",
            "next_action": "tie domain no-leak to R11 operator vector or prove domain sector exact/topological locally",
        },
        {
            "condition_id": "ZA5_no_tuned_cancellation",
            "channel": "both",
            "exact_zero_condition": "alpha3_boundary and alpha3_domain must individually vanish or score below lock unless a parent identity forces cancellation",
            "theorem_status": "policy_pass",
            "evidence": "separate source-normalization channels block cancellation-by-fit",
            "failure_mode": "opposite hidden fluxes could be tuned after the fact",
            "next_action": "score each channel separately before any total-alpha3 claim",
        },
        {
            "condition_id": "ZA6_bound_if_not_zero",
            "channel": "both",
            "exact_zero_condition": "abs(W_i_alpha3 epsilon_i_flux) <= 4e-20 for each active channel",
            "theorem_status": "bound_product_only",
            "evidence": "468 scorecard gives the alpha3 lock but no response weight",
            "failure_mode": "epsilon_i alone is meaningless without W_i_alpha3",
            "next_action": "derive or measure response weights W_boundary_alpha3 and W_domain_alpha3",
        },
        {
            "condition_id": "ZA7_conclusion",
            "channel": "both",
            "exact_zero_condition": "alpha3_mu_extra = 0 requires zero boundary flux plus zero domain/projector flux",
            "theorem_status": "fail_current_corpus",
            "evidence": "no parent no-flux theorem or numeric coefficient exists in 468 inputs",
            "failure_mode": "local PPN branch remains retained, not derived GR",
            "next_action": NEXT_TARGET,
        },
    ]


def build_input_skeleton() -> list[dict[str, Any]]:
    return [
        {
            "skeleton_id": "S0_boundary_alpha3",
            "coefficient_artifact": "P8_mu_extra_boundary_coefficients.csv",
            "channel": "boundary_monopole_shift",
            "target_row": "R7_alpha3",
            "observable": "alpha3",
            "coefficient_symbol": "epsilon_boundary_flux",
            "alpha3_map": "alpha3_boundary = W_boundary_alpha3 * epsilon_boundary_flux",
            "required_input": "W_boundary_alpha3 and epsilon_boundary_flux, or theorem-zero source proving their product is zero",
            "target_bound": "4e-20 dimensionless",
            "acceptance_gate": "abs(alpha3_boundary) <= 4e-20 with source path, units, and no hidden cancellation",
            "current_value": "MISSING_NUMERIC_OR_DERIVED_ZERO",
            "score_ready": "false",
            "next_action": "derive boundary no-hair/no-flux first because this is priority 1",
        },
        {
            "skeleton_id": "S1_domain_alpha3",
            "coefficient_artifact": "P8_mu_extra_domain_projector_coefficients.csv",
            "channel": "domain_projector_mass",
            "target_row": "R7_alpha3",
            "observable": "alpha3",
            "coefficient_symbol": "epsilon_domain_flux",
            "alpha3_map": "alpha3_domain = W_domain_alpha3 * epsilon_domain_flux",
            "required_input": "W_domain_alpha3 and epsilon_domain_flux, or theorem-zero source proving their product is zero",
            "target_bound": "4e-20 dimensionless",
            "acceptance_gate": "abs(alpha3_domain) <= 4e-20 and R11/vector rows are zero or scored",
            "current_value": "MISSING_NUMERIC_OR_DERIVED_ZERO",
            "score_ready": "false",
            "next_action": "derive projector no-leak theorem or connect to executable R11 vector",
        },
        {
            "skeleton_id": "S2_total_alpha3_guard",
            "coefficient_artifact": "P8_MU_EXTRA_ALPHA3_FILL_INPUT_SKELETON.csv",
            "channel": "combined_mu_extra_alpha3",
            "target_row": "R7_alpha3",
            "observable": "alpha3",
            "coefficient_symbol": "alpha3_mu_extra_total",
            "alpha3_map": "alpha3_mu_extra = alpha3_boundary + alpha3_domain + other scored alpha3 channels",
            "required_input": "individual channel values, no post-fit cancellation, and parent identity if cancellation is claimed",
            "target_bound": "4e-20 dimensionless",
            "acceptance_gate": "total and every active channel pass unless parent identity enforces exact cancellation",
            "current_value": "MISSING_CHANNEL_VALUES",
            "score_ready": "false",
            "next_action": "do not total-score until S0 and S1 are theorem-zero or numeric",
        },
    ]


def build_decision() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D0_highest_pressure",
            "status": "identified",
            "evidence": "R7_alpha3 has the tightest numeric lock at 4e-20 for boundary and domain channels",
            "next_action": "work alpha3 before weaker beta/xi/Gdot rows",
        },
        {
            "decision_id": "D1_zero_attempt",
            "status": "not_derived",
            "evidence": "Ward/Bianchi ownership and no-hair ledgers do not prove boundary/domain momentum flux zero",
            "next_action": "attempt boundary no-flux theorem or fill coefficient product",
        },
        {
            "decision_id": "D2_bound_form",
            "status": "bound_product_only",
            "evidence": "abs(W_i_alpha3 epsilon_i_flux) <= 4e-20 is the current executable form",
            "next_action": "derive W_i and epsilon_i or theorem-zero",
        },
        {
            "decision_id": "D3_score_ready",
            "status": "false",
            "evidence": "no numeric coefficient, response weight, or theorem-zero source supplied",
            "next_action": "write 470 boundary-alpha3 theorem/coefficient artifact",
        },
        {
            "decision_id": "D4_promotion",
            "status": "forbidden",
            "evidence": "alpha3 row remains retained; mu_extra zero and local GR are not promoted",
            "next_action": "keep claim ceiling active",
        },
    ]


def build_doc(run_dir: Path) -> str:
    source_rows = read_csv(SOURCE_REGISTER_PATH)
    pressure_rows = read_csv(PRESSURE_GATE_PATH)
    zero_rows = read_csv(ZERO_ATTEMPT_PATH)
    skeleton_rows = read_csv(INPUT_SKELETON_PATH)
    decision_rows = read_csv(DECISION_PATH)
    a_rows = alpha3_rows()
    req_rows = required_input_rows()
    return f"""# 469 - Fill Or Zero Highest-Pressure `mu_extra` Row

Private local-GR/Newton source-normalization checkpoint. This is not a public PPN, Newtonian-limit, local-GR, measured-GM, EM, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint `468` turned the `mu_extra` coefficient vector into a local-bound scorecard. The tightest numeric pressure is:

```text
R7_alpha3 <= 4e-20
```

and it appears in two tied channels:

```text
boundary_monopole_shift
domain_projector_mass
```

This checkpoint asks whether we can zero those rows from the current parent corpus. If not, it writes the exact coefficient/bound skeleton needed to score them.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/fill_or_zero_highest_pressure_mu_extra_row.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{md_table(source_rows)}

## 4. Highest-Pressure Rows

{md_table(a_rows)}

Required inputs:

{md_table(req_rows)}

## 5. Pressure Gate

{md_table(pressure_rows)}

The important decision is:

```text
R7_alpha3 is not one row to hand-wave away.
It is a tied boundary/domain momentum-flux problem.
```

The boundary row is operationally first because it is priority 1 and does not require the R11 operator vector, but the domain row remains live.

## 6. Zero-Theorem Attempt

The physical object that must vanish is not merely `epsilon_boundary` or `epsilon_domain_projector` as scalar names. It is the local preferred-momentum projection:

```text
q_i^nu = P_loc^nu_rho (nabla^rho Gamma_eff_i - nabla_mu K_i^(mu rho))
```

For the `alpha3` row, the dangerous part is the flux/vector projection:

```text
F_i,alpha3 = lim_S r^2 n_mu P_loc_nu K_i^(mu nu)/(G_eff M_eff)
```

The row is safe only if:

```text
F_boundary,alpha3 = 0
F_domain,alpha3 = 0
```

or if each product is numerically below the lock:

```text
abs(W_i,alpha3 epsilon_i,flux) <= 4e-20.
```

{md_table(zero_rows)}

Verdict:

```text
The current corpus gives Ward/Bianchi ownership, not a theorem-zero.
```

That is not catastrophic, but it is brutally constraining. We now know exactly what has to be proved or filled.

## 7. Input Skeleton

{md_table(skeleton_rows)}

No tuned cancellation is allowed:

```text
alpha3_boundary + alpha3_domain ~= 0
```

does not pass unless a parent identity forces that cancellation before data.

## 8. Decision

{md_table(decision_rows)}

Plain-English status:

```text
The local branch is still alive, but not promoted.
The alpha3 pressure row demands either a real no-flux/no-leak theorem or an explicit tiny coefficient product.
```

Boxing-score version:

```text
We found the judge's most dangerous scorecard.
Now we train the exact counter: boundary alpha3 no-flux first, then domain projector no-leak.
```

## 9. Claim Ceiling

Allowed:

```text
The highest-pressure mu_extra obstruction is the R7_alpha3 boundary/domain flux pair.
```

Allowed:

```text
The required bound is abs(W_i,alpha3 epsilon_i,flux) <= 4e-20 per active channel, unless theorem-zero is derived.
```

Forbidden:

```text
MTS derives mu_extra=0.
```

Forbidden:

```text
MTS passes PPN alpha3, Newton, or local GR.
```

## 10. Next Queue

| Rank | Target | Why |
| ---: | --- | --- |
| 1 | `470-boundary-alpha3-zero-theorem-or-numeric-coefficient.md` | boundary channel is priority 1 and does not require R11 first |
| 2 | `471-domain-projector-alpha3-no-leak-or-R11-link.md` | domain channel is tied at the same 4e-20 lock |
| 3 | `472-alpha3-channel-evaluator.md` | only useful after theorem-zero or numeric coefficient products exist |
"""


def write_run(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-fill-or-zero-highest-pressure-mu-extra-row"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    write_csv(SOURCE_REGISTER_PATH, source_register_rows())
    write_csv(PRESSURE_GATE_PATH, build_pressure_gate())
    write_csv(ZERO_ATTEMPT_PATH, build_zero_attempt())
    write_csv(INPUT_SKELETON_PATH, build_input_skeleton())
    write_csv(DECISION_PATH, build_decision())

    for path in [SOURCE_REGISTER_PATH, PRESSURE_GATE_PATH, ZERO_ATTEMPT_PATH, INPUT_SKELETON_PATH, DECISION_PATH]:
        write_csv(Path(results_dir.relative_to(ROOT)) / path.name.lower(), read_csv(path))

    (ROOT / DOC_PATH).write_text(build_doc(run_dir), encoding="utf-8")

    source_rows = read_csv(SOURCE_REGISTER_PATH)
    pressure_rows = read_csv(PRESSURE_GATE_PATH)
    zero_rows = read_csv(ZERO_ATTEMPT_PATH)
    skeleton_rows = read_csv(INPUT_SKELETON_PATH)
    decision_rows = read_csv(DECISION_PATH)
    status = {
        "timestamp": timestamp,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "pressure_gate": str(ROOT / PRESSURE_GATE_PATH),
        "zero_attempt": str(ROOT / ZERO_ATTEMPT_PATH),
        "input_skeleton": str(ROOT / INPUT_SKELETON_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "source_rows": len(source_rows),
        "source_paths_missing": sum(1 for row in source_rows if row["exists"] != "True"),
        "alpha3_scorecard_rows_loaded": len(alpha3_rows()),
        "pressure_gate_rows": len(pressure_rows),
        "zero_attempt_rows": len(zero_rows),
        "input_skeleton_rows": len(skeleton_rows),
        "decision_rows": len(decision_rows),
        "highest_pressure_row": "R7_alpha3",
        "highest_pressure_bound": "4e-20 dimensionless",
        "highest_pressure_channels": "boundary_monopole_shift;domain_projector_mass",
        "zero_theorem_derived": False,
        "numeric_coefficients_supplied": False,
        "score_ready_rows": 0,
        "boundary_alpha3_promoted": False,
        "domain_alpha3_promoted": False,
        "mu_extra_zero_promoted": False,
        "Newtonian_reduction_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    return status


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()
    print(json.dumps(write_run(args.timestamp), indent=2))


if __name__ == "__main__":
    main()
