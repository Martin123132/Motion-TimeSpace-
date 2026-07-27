from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "source_measure_Meff_flux_closure_contract_built_conditional_current_MTS_not_derived_residual_map_written"
CLAIM_CEILING = "conditional_source_measure_flux_only_no_measured_GM_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "510-worldtube-source-measure-glue-or-Meff-residual-runner.md"

DOC_PATH = Path("509-source-measure-Meff-flux-closure-after-kappa-gate.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_SOURCE_REGISTER.csv")
THEOREM_PATH = Path("source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv")
CLAUSES_PATH = Path("source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv")
RESIDUAL_MAP_PATH = Path("source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv")
GATE_TESTS_PATH = Path("source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_GATE_TESTS.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_ROUTE_UPDATE.csv")

SOURCE_REGISTER = [
    {
        "source_file": "508-constant-kappa-superselection-or-drift-residual.md",
        "role": "conditional constant-kappa gate carried forward, but measured GM still open",
    },
    {
        "source_file": "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md",
        "role": "conditional parent Noether mass-charge closure theorem and open premises",
    },
    {
        "source_file": "504-parent-Hilbert-worldtube-glue-or-external-radial-input-plan.md",
        "role": "worldtube/Hilbert glue decomposition and C-term ledger path",
    },
    {
        "source_file": "501-topological-Hilbert-current-equality-or-radial-bound-runner.md",
        "role": "Hilbert-current equality attempt and radial-bound fallback",
    },
    {
        "source_file": "498-source-normalization-radial-and-calibration-theorem-attempt.md",
        "role": "source-normalized Newton branch stack and radial/calibration blockers",
    },
    {
        "source_file": "451-mass-flux-projector-Euler-calibration-attempt.md",
        "role": "mass-flux projector/Euler calibration contract",
    },
    {
        "source_file": "454-PiM-parent-symplectic-projector-algebra-attempt.md",
        "role": "Pi_M parent symplectic projector algebra attempt",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "role": "MF0-MF8 mass-flux source/projector/calibration requirements",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_charge_current_equality_DIRECT_ATTEMPT.csv",
        "role": "CC0-CC8 direct source-charge equality blockers",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv",
        "role": "Delta_frame, Delta_nonEH, Delta_symp, Delta_PiM, Delta_extra, Delta_flux, Delta_G, Delta_cal, Delta_PPN residuals",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv",
        "role": "SN3/SN4/SN8/SN9/SN10 open Newton-source branch rungs",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
        "role": "worldtube source-measure equality and calibration clauses",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
        "role": "local residual runner input showing M_eff conservation is not currently scoreable",
    },
    {
        "source_file": "scripts/source_measure_Meff_flux_closure_after_kappa_gate.py",
        "role": "this checkpoint generator",
    },
]

THEOREM_ROWS = [
    {
        "theorem_id": "T509_0_charge_identity_needed",
        "statement": "After the conditional kappa gate, measured GM still requires M_eff to be the same parent source charge seen by the exterior Hilbert/Noether flux.",
        "mathematical_form": "M_eff[W] = M_source[W] = integral_S Q_M[tau] = (4*pi*G_ref)^-1 integral_S Pi_M J_H",
        "result": "source measure and exterior mass flux are the same object only if the parent action owns the projector, observed time generator, and source pullback",
        "status": "conditional_required_identity",
        "MTS_current_status": "not_parent_derived",
    },
    {
        "theorem_id": "T509_1_flux_closure",
        "statement": "If the projected Hilbert mass current is closed in the source-free exterior, then M_eff cannot drift radially between linked spheres.",
        "mathematical_form": "M_eff(S2)-M_eff(S1) = integral_A d(Pi_M J_H); d(Pi_M J_H)=0 => epsilon_radial_Meff=0",
        "result": "radial measured-mass leakage is zero only under the parent Ward/Euler/topological closure premise",
        "status": "conditional_corollary",
        "MTS_current_status": "closure_not_derived_for_current_MTS",
    },
    {
        "theorem_id": "T509_2_no_extra_mass_channel",
        "statement": "The flux equality is invalid if non-EH, symplectic-boundary, projector-stress, memory, domain, range, or frame channels carry mass charge.",
        "mathematical_form": "d(Pi_M J_H) = Delta_nonEH + Delta_symp + Delta_PiM + Delta_extra + Delta_frame + Delta_cal + Delta_PPN",
        "result": "all Delta terms must be derived zero or bounded before Newton/PPN/local-GR promotion",
        "status": "necessary_no_cheat_clause",
        "MTS_current_status": "residual_map_active",
    },
]

CLAUSE_ROWS = [
    {
        "clause_id": "SM509_0_observed_generator",
        "required_clause": "The same observed time/translation generator tau is used in matter source variation, exterior Hilbert charge, and orbital readout.",
        "mathematical_form": "tau_source = tau_Hilbert = tau_orbit",
        "if_missing": "measured GM may be a frame-mixed calibration rather than a derived source charge",
        "current_status": "not_parent_derived",
    },
    {
        "clause_id": "SM509_1_source_current",
        "required_clause": "The parent matter action defines a source current J_H from the observed coframe/metric variation before phenomenological readout.",
        "mathematical_form": "J_H[tau] = delta S_matter / delta e_obs contracted with tau",
        "if_missing": "M_eff can be fitted to matter rather than derived from matter",
        "current_status": "conditional",
    },
    {
        "clause_id": "SM509_2_parent_mass_projector",
        "required_clause": "Pi_M is fixed by the parent symplectic/projector algebra and is not tuned separately per source, radius, or test arena.",
        "mathematical_form": "Pi_M: parent currents -> scalar mass charge",
        "if_missing": "projector freedom can absorb failures and becomes a patch",
        "current_status": "not_parent_derived",
    },
    {
        "clause_id": "SM509_3_flux_closure",
        "required_clause": "The projected Hilbert mass current is closed in compact source-free exterior domains by a Ward/Euler/topological identity.",
        "mathematical_form": "d(Pi_M J_H)=0 outside W",
        "if_missing": "dln_Meff_dt and epsilon_radial_Meff remain physical residuals",
        "current_status": "not_parent_derived",
    },
    {
        "clause_id": "SM509_4_worldtube_source_measure",
        "required_clause": "The worldtube source measure equals the exterior parent charge on any linking sphere.",
        "mathematical_form": "M_source[W] = integral_S Q_M[tau] = (4*pi*G_ref)^-1 integral_S Pi_M J_H",
        "if_missing": "orbital mass is not yet proven to be the same as source mass",
        "current_status": "not_parent_derived",
    },
    {
        "clause_id": "SM509_5_no_extra_channel",
        "required_clause": "Boundary, non-Hilbert, projector-stress, memory, domain, range, and connection terms carry no independent mass charge.",
        "mathematical_form": "Delta_nonEH = Delta_symp = Delta_PiM = Delta_extra = Delta_frame = 0",
        "if_missing": "local-GR branch needs residual bounds rather than a theorem",
        "current_status": "not_parent_derived",
    },
    {
        "clause_id": "SM509_6_Gauss_orbital_calibration",
        "required_clause": "The closed charge normalizes to the orbital inverse-square coefficient with one reference zero and one universal G_ref.",
        "mathematical_form": "a_r = -G_ref M_source/r^2 + higher-order controlled terms",
        "if_missing": "Newton recovery remains a readout assumption",
        "current_status": "not_parent_derived",
    },
    {
        "clause_id": "SM509_7_second_order_PPN_stability",
        "required_clause": "The same source charge remains stable through the beta/gamma PPN expansion and cannot hide second-order derivative hair.",
        "mathematical_form": "gamma-1, beta-1, alpha_i, zeta_i residuals depend only on explicit Delta rows",
        "if_missing": "local Newton may pass while local GR still fails",
        "current_status": "not_parent_derived",
    },
]

RESIDUAL_MAP_ROWS = [
    {
        "residual_id": "SMR509_0_Delta_flux",
        "if_theorem_missing": "M_eff has time/radial leakage",
        "symbol": "dln_Meff_dt; epsilon_radial_Meff",
        "observable_lock": "Gdot/GMdot, orbital residuals, radial source normalization",
        "required_artifact": "P8_time_drift_residual_or_zero.csv and/or P8_radial_mu_profile_or_zero.csv",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "SMR509_1_Delta_PiM",
        "if_theorem_missing": "mass projector carries unowned variation",
        "symbol": "Delta_PiM",
        "observable_lock": "source-normalized Newton branch, PPN projector hair",
        "required_artifact": "parent projector variation ledger or explicit Delta_PiM coefficient",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "SMR509_2_Delta_symp",
        "if_theorem_missing": "boundary symplectic/reference term shifts exterior mass",
        "symbol": "Delta_symp",
        "observable_lock": "worldtube boundary/reference zero and orbital calibration",
        "required_artifact": "boundary charge reference-zero theorem or bound",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "SMR509_3_Delta_extra",
        "if_theorem_missing": "non-EH/domain/memory/range/connection sector carries mass charge",
        "symbol": "Delta_extra; mu_extra",
        "observable_lock": "local PPN, fifth-force, source universality, clocks",
        "required_artifact": "extra-sector silence theorem by field or residual coefficient matrix",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "SMR509_4_Delta_cal",
        "if_theorem_missing": "closed charge does not calibrate to observed inverse-square orbital GM",
        "symbol": "Delta_cal",
        "observable_lock": "Kepler/Newton readout and absolute mass normalization",
        "required_artifact": "Gauss/orbital calibration theorem or external calibration ledger",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "SMR509_5_Delta_frame",
        "if_theorem_missing": "source frame and orbital/clock frame disagree",
        "symbol": "Delta_frame_source",
        "observable_lock": "WEP, frame preferred effects, clock/local source tests",
        "required_artifact": "single observed source-frame theorem or frame residual bound",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "SMR509_6_Delta_nonEH",
        "if_theorem_missing": "operator charge differs from EH/Hilbert charge",
        "symbol": "Delta_nonEH",
        "observable_lock": "GR limit, PPN gamma/beta, non-EH force channels",
        "required_artifact": "local EH reduction and non-EH charge silence theorem",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "SMR509_7_Delta_PPN",
        "if_theorem_missing": "source equality holds only at leading order",
        "symbol": "Delta_PPN",
        "observable_lock": "beta, gamma, perihelion, Shapiro, light bending, preferred-frame tests",
        "required_artifact": "second-order source-charge PPN expansion or explicit residual vector",
        "valid_for_claim": "false",
    },
]

GATE_TEST_ROWS = [
    {
        "gate_id": "G509_0_kappa_carried_conditionally",
        "gate": "constant kappa from 508 can be carried only as a conditional/global premise",
        "result": "pass_conditional",
        "evidence": "508 status keeps kappa_Geff_silence_derived_for_MTS=false",
    },
    {
        "gate_id": "G509_1_source_measure_equality",
        "gate": "M_source[W] equals exterior parent mass charge before readout",
        "result": "fail_for_current_claim",
        "evidence": "CC3/CC4/CC7 and W504_4 remain not parent-derived",
    },
    {
        "gate_id": "G509_2_flux_closure",
        "gate": "d(Pi_M J_H)=0 is derived from parent Ward/Euler/topological structure",
        "result": "fail_for_current_claim",
        "evidence": "MF2/MF4/MF6 and SN4 remain conditional/not parent-derived",
    },
    {
        "gate_id": "G509_3_residual_map_complete",
        "gate": "failed source-measure identities are mapped to explicit residual rows",
        "result": "pass",
        "evidence": f"residual_rows={len(RESIDUAL_MAP_ROWS)}",
    },
    {
        "gate_id": "G509_4_no_local_GR_claim",
        "gate": "no measured-GM/Newton/PPN/local-GR promotion is made from conditional source flux",
        "result": "pass",
        "evidence": "claim ceiling blocks promotion until source measure and PPN residuals close",
    },
]

DECISION_ROWS = [
    {
        "decision_id": "D509_0",
        "decision": "source_measure_flux_is_the_next_true_blocker",
        "meaning": "constant kappa is not enough; M_eff must be shown to be the conserved parent source charge",
        "claim_status": "conditional_only",
    },
    {
        "decision_id": "D509_1",
        "decision": "current_MTS_has_not_earned_Meff_closure",
        "meaning": "the clean theorem is now written, but the present corpus still lacks the parent identity d(Pi_M J_H)=0 and worldtube source-measure glue",
        "claim_status": "Meff_conservation_derived_false",
    },
    {
        "decision_id": "D509_2",
        "decision": "do_not_smuggle_orbital_GM",
        "meaning": "orbital GM cannot be treated as proof of source matching; it is either a derived Gauss/readout theorem or an external calibration ledger",
        "claim_status": "Newton_promoted_false",
    },
    {
        "decision_id": "D509_3",
        "decision": "next_branch_is_theorem_or_runner",
        "meaning": "either derive worldtube source-measure glue directly or build a residual runner for Delta_flux, Delta_PiM, Delta_symp, Delta_extra, Delta_cal, Delta_frame, Delta_nonEH, and Delta_PPN",
        "claim_status": NEXT_TARGET,
    },
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RU509_0",
        "status": "source_measure_flux_contract_sharpened",
        "update": "measured GM is now split into a parent source-measure theorem plus explicit residual fallback",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU509_1",
        "status": "local_GR_still_blocked",
        "update": "without Pi_M current closure, worldtube source equality, and PPN stability, MTS cannot claim derived local GR",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU509_2",
        "status": "derivation_path_kept_alive",
        "update": "the path is not dead; it has been reduced to exact premises a parent action must satisfy instead of a vague plateau/source axiom",
        "next_target": NEXT_TARGET,
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        path = ROOT / item["source_file"]
        rows.append(
            {
                "source_file": item["source_file"],
                "role": item["role"],
                "exists": path.exists(),
            }
        )
    return rows


def validation_rows(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] != True]
    return [
        {
            "check_id": "V509_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V509_1_clause_stack_complete",
            "result": "pass",
            "detail": f"clause_rows={len(CLAUSE_ROWS)}",
        },
        {
            "check_id": "V509_2_residual_map_complete",
            "result": "pass",
            "detail": f"residual_rows={len(RESIDUAL_MAP_ROWS)}",
        },
        {
            "check_id": "V509_3_claim_ceiling_enforced",
            "result": "pass",
            "detail": "measured_GM_parent_derived=false; local_GR_claim_allowed=false",
        },
        {
            "check_id": "V509_4_next_target_set",
            "result": "pass",
            "detail": NEXT_TARGET,
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys())
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = []
        for header in headers:
            value = str(row.get(header, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        output.append("| " + " | ".join(values) + " |")
    return "\n".join(output)


def build_doc(
    timestamp: str,
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 509 - Source-Measure M_eff Flux Closure After Kappa Gate

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

This checkpoint answers the next honest question after the kappa gate:

```text
Even if kappa/G_eff is constant, what makes measured GM the parent source charge?
```

The answer cannot be "because orbits fit it". That would smuggle the calibration back in.

The clean derivation route is:

```text
M_eff[W] = M_source[W]
         = integral_S Q_M[tau]
         = (4*pi*G_ref)^-1 integral_S Pi_M J_H

M_eff(S2)-M_eff(S1) = integral_A d(Pi_M J_H)
```

So `epsilon_radial_Meff -> 0` follows only if the parent action gives `d(Pi_M J_H)=0` in the source-free exterior and all extra source/charge channels are zero.

That is a real theorem route, but it is still **not derived for current MTS**. The current status is therefore:

```text
conditional source-measure flux theorem written;
MTS parent derivation still missing;
residual map active;
no local GR claim.
```

## 2. Theorem Rows

{markdown_table(THEOREM_ROWS)}

## 3. Required Clauses

{markdown_table(CLAUSE_ROWS)}

## 4. Residual Map

{markdown_table(RESIDUAL_MAP_ROWS)}

## 5. Gate Tests

{markdown_table(GATE_TEST_ROWS)}

## 6. Decision

{markdown_table(DECISION_ROWS)}

## 7. Source Register

{markdown_table(sources)}

## 8. Validation

{markdown_table(validations)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
MTS has a precise conditional route for measured-GM/source-measure closure.
The missing identities are now localised to Pi_M current closure, worldtube glue, no-extra-channel silence, and PPN stability.
If those identities fail, each failure has a named residual.
```

Forbidden:

```text
MTS has derived measured GM.
MTS has derived Newtonian recovery from the current parent action.
MTS has derived local GR or PPN consistency.
MTS may hide M_eff drift inside orbital calibration.
```

## 11. What This Means

This is not a dead end. It is the opposite: the branch is now sharp enough to be falsifiable inside the formalism.

The local-GR route survives only if the next step can either:

```text
derive worldtube source-measure glue and d(Pi_M J_H)=0,
```

or, failing that,

```text
turn every nonzero Delta term into an explicit residual vector and show it is below local bounds.
```

## 12. Next Target

`{NEXT_TARGET}`
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-source-measure-Meff-flux-closure-after-kappa-gate"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (THEOREM_PATH, THEOREM_ROWS),
        (CLAUSES_PATH, CLAUSE_ROWS),
        (RESIDUAL_MAP_PATH, RESIDUAL_MAP_ROWS),
        (GATE_TESTS_PATH, GATE_TEST_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != True]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "theorem": str(ROOT / THEOREM_PATH),
        "clauses": str(ROOT / CLAUSES_PATH),
        "residual_map": str(ROOT / RESIDUAL_MAP_PATH),
        "gate_tests": str(ROOT / GATE_TESTS_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "conditional_constant_kappa_from_508": True,
        "conditional_source_measure_flux_theorem": True,
        "source_measure_Meff_flux_derived_for_MTS": False,
        "PiM_flux_closure_derived": False,
        "worldtube_source_measure_glue_derived": False,
        "Meff_conservation_derived": False,
        "epsilon_radial_Meff_zero_derived_for_MTS": False,
        "measured_GM_parent_derived": False,
        "source_normalized_Newton_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\nnext={NEXT_TARGET}\nlocal_GR_claim_allowed=false\n",
        encoding="utf-8",
    )
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
