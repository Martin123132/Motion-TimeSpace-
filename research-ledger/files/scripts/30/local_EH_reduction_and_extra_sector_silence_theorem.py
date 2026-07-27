from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "local_EH_reduction_silence_theorem_attempt_conditional_energy_identity_derived_MTS_sector_premises_open"
CLAIM_CEILING = "conditional_extra_sector_silence_test_no_full_MTS_EH_reduction_or_local_GR_promotion"
NEXT_TARGET = "507-field-specific-silence-queue-kappa-domain-memory-motion.md"

DOC_PATH = Path("506-local-EH-reduction-and-extra-sector-silence-theorem.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_LOCAL_EH_REDUCTION_SOURCE_REGISTER.csv")
THEOREM_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_LOCAL_EH_REDUCTION_THEOREM_ATTEMPT.csv")
ENERGY_IDENTITY_PATH = Path("source-intake/mts_residuals/P8_EXTRA_SECTOR_SILENCE_ENERGY_IDENTITY.csv")
OPERATOR_REQUIREMENTS_PATH = Path("source-intake/mts_residuals/P8_OPERATOR_CLASSIFICATION_REQUIREMENTS.csv")
SECTOR_STATUS_PATH = Path("source-intake/mts_residuals/P8_MTS_SECTOR_SILENCE_STATUS.csv")
FAILURE_LEDGER_PATH = Path("source-intake/mts_residuals/P8_LOCAL_EH_REDUCTION_FAILURE_LEDGER.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_LOCAL_EH_REDUCTION_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_LOCAL_EH_REDUCTION_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_LOCAL_EH_REDUCTION_ROUTE_UPDATE.csv")

SOURCE_REGISTER = [
    {
        "source_file": "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md",
        "role": "sets local EH-plus-silent exterior as the premise needed for Noether mass-charge closure",
    },
    {
        "source_file": "504-parent-Hilbert-worldtube-glue-or-external-radial-input-plan.md",
        "role": "parent charge closure route and C-term decomposition",
    },
    {
        "source_file": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "operator-retention gate for local EH reduction",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_EH_ONLY_OR_EXECUTABLE_VECTOR_GATE.csv",
        "role": "EH-only or executable operator-vector gate",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_MU_EXTRA_SOURCE_NORMALIZATION_LINK.csv",
        "role": "non-EH/operator leakage source-normalization link",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_YLOC_NO_SOURCE_THEOREM.csv",
        "role": "prior local source-silence theorem attempt",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_YLOC_NO_LINEAR_SOURCE_THEOREM.csv",
        "role": "prior no-linear-source local branch attempt",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_YLOC_SOURCE_DEBT_LEDGER.csv",
        "role": "existing local source debt ledger",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_DECISION.csv",
        "role": "memory double-zero decision rows relevant to silent-sector premises",
    },
    {
        "source_file": "scripts/local_EH_reduction_and_extra_sector_silence_theorem.py",
        "role": "this checkpoint generator",
    },
]

THEOREM_ATTEMPT_ROWS = [
    {
        "theorem_id": "T506_EH_plus_silent_reduction",
        "statement": "A compact local exterior reduces to EH if every non-EH/local-extra sector is either topological/exact with zero flux, frozen to a constant by a positive source-free equation, or retained as an explicit bounded residual.",
        "derived_part": "positive source-free elliptic/proca-type energy identity gives field silence under no-charge and zero-boundary/decay premises",
        "not_derived_part": "MTS parent action has not yet supplied the field-specific operators, signs, masses, source charges, and boundary data for every sector",
        "claim_status": "conditional_theorem_not_MTS_promotion",
    },
    {
        "theorem_id": "T506_nonEH_operator_filter",
        "statement": "Curvature/operator terms beyond EH must be zero, topological in four dimensions, field-redefinition redundant, or mapped to an executable residual vector below local locks.",
        "derived_part": "operator-classification rule is exact as a consistency gate",
        "not_derived_part": "retained R11/operator rows are not yet all zeroed or scored",
        "claim_status": "gate_not_passed",
    },
    {
        "theorem_id": "T506_local_GR_bridge_condition",
        "statement": "If T506_EH_plus_silent_reduction and T505 source-measure matching both pass, the local GR/Newton bridge becomes derivable through Q_M closure.",
        "derived_part": "logical implication from 505 plus the silence theorem",
        "not_derived_part": "premises remain open sector-by-sector",
        "claim_status": "conditional_bridge_only",
    },
]

ENERGY_IDENTITY_ROWS = [
    {
        "identity_id": "E506_scalar_positive_operator",
        "field_class": "scalar_or_amplitude_mode_chi",
        "operator_form": "(-Delta_A + m_chi^2) chi = 0 with m_chi^2 > 0",
        "energy_identity": "integral_A (|grad chi|^2 + m_chi^2 chi^2) = boundary_flux",
        "zero_condition": "boundary_flux=0 and no source charge imply chi=0",
        "failure_modes": "massless zero mode; negative mass squared; exterior source; nonzero boundary value; noncompact memory kernel",
    },
    {
        "identity_id": "E506_vector_tensor_positive_operator",
        "field_class": "vector_tensor_projector_or_flow_mode_X",
        "operator_form": "self-adjoint positive operator L_X X = 0 with gauge fixed and no charge",
        "energy_identity": "integral_A <X,L_X X> = norm_positive[X] + boundary_flux",
        "zero_condition": "positive norm plus zero boundary flux gives X=0 modulo pure gauge/topological class",
        "failure_modes": "gauge zero mode; topological charge; nonzero source current; sign-indefinite kinetic term; boundary hair",
    },
    {
        "identity_id": "E506_memory_kernel_silence",
        "field_class": "compact_local_memory_or_history_mode",
        "operator_form": "memory response is local, causal, source-free, and has stable positive kernel in the local exterior",
        "energy_identity": "memory energy or Lyapunov functional decreases to constant/silent state",
        "zero_condition": "no local source and no boundary/history injection leaves only constant universal calibration",
        "failure_modes": "long nonlocal tail; history-dependent source; time drift; Gdot leakage",
    },
    {
        "identity_id": "E506_boundary_topological_silence",
        "field_class": "topological_or_exact_boundary_sector",
        "operator_form": "L_top = dB or topological density with no metric/source variation in A",
        "energy_identity": "bulk Euler variation vanishes and surface flux is separately evaluated",
        "zero_condition": "linking-sphere flux is zero or fixed background subtraction",
        "failure_modes": "finite surface charge; angular/radial boundary hair; wrong measured-mass readout",
    },
]

OPERATOR_REQUIREMENTS_ROWS = [
    {
        "operator_class": "EH_core",
        "allowed_if": "normalization G_ref fixed and local exterior equations reduce to Einstein tensor plus allowed Lambda/background subtraction",
        "forbidden_if": "G_eff or kappa varies radially/time-dependently in local exterior",
        "maps_to": "R3;R4;R9;R11",
    },
    {
        "operator_class": "topological_exact",
        "allowed_if": "metric/source variation is zero in A or surface flux is exactly zero/background-subtracted",
        "forbidden_if": "exact term carries finite linking-sphere charge",
        "maps_to": "R3;R4;R7;R8;R11",
    },
    {
        "operator_class": "auxiliary_positive_massive",
        "allowed_if": "positive source-free operator plus no charge/no boundary value proves field zero",
        "forbidden_if": "massless, tachyonic, sourced, or finite-range profile survives",
        "maps_to": "R4;R9;R10;R11",
    },
    {
        "operator_class": "field_redefinition_redundant",
        "allowed_if": "term can be removed without changing observables and without moving leakage into source normalization",
        "forbidden_if": "redefinition changes measured mass, clock, or PPN readout",
        "maps_to": "R1;R2;R3;R4;R11",
    },
    {
        "operator_class": "retained_residual",
        "allowed_if": "explicit coefficient vector exists and is bounded by local data",
        "forbidden_if": "coefficient is symbolic and unbounded",
        "maps_to": "R10;R11;P8_radial_source_hair",
    },
]

SECTOR_STATUS_ROWS = [
    {
        "sector": "metric_EH_core",
        "needed_silence_or_reduction": "local operator equals EH plus allowed Lambda/background subtraction",
        "current_status": "conditional_not_parent_derived",
        "main_open_row": "R11_operator_vector",
        "next_action": "derive EH-only local exterior operator or keep executable non-EH vector",
    },
    {
        "sector": "kappa_Geff_source_normalization",
        "needed_silence_or_reduction": "G_eff/kappa constant in compact local exterior and calibrated before readout",
        "current_status": "open",
        "main_open_row": "R9_Gdot;P8_Meff_conservation;P8_radial_source_hair",
        "next_action": "derive constant-kappa no-hair or retain dln_Geff and dln_Meff residuals",
    },
    {
        "sector": "motion_time_flow_modes",
        "needed_silence_or_reduction": "flow/time modes are pure gauge, topological, or positive source-free with no local charge",
        "current_status": "open",
        "main_open_row": "Yloc source/current debts",
        "next_action": "write field-specific operator and source-current equation for each mode",
    },
    {
        "sector": "domain_projector_selector",
        "needed_silence_or_reduction": "domain/projector sector freezes without vector/preferred-frame leakage",
        "current_status": "open",
        "main_open_row": "alpha3;xi;R11_domain_projector",
        "next_action": "derive no-vector/no-leak domain selector theorem",
    },
    {
        "sector": "memory_kernel",
        "needed_silence_or_reduction": "memory is local-silent or constant universal in compact local systems",
        "current_status": "open",
        "main_open_row": "Gdot;alpha3;double_zero_memory",
        "next_action": "derive positive/stable kernel silence or mark memory residual executable",
    },
    {
        "sector": "boundary_topological_terms",
        "needed_silence_or_reduction": "surface flux through linking spheres is zero or fixed background subtraction",
        "current_status": "open",
        "main_open_row": "boundary_alpha3;radial_source_hair",
        "next_action": "prove no-flux for compact local exterior or retain boundary flux residual",
    },
]

FAILURE_LEDGER_ROWS = [
    {
        "failure_id": "F506_0_positive_operator_missing",
        "failure": "field-specific local operator is not written or has unknown sign",
        "effect": "no no-hair/silence theorem can be claimed",
        "repair": "derive Euler-Lagrange operator and energy identity",
    },
    {
        "failure_id": "F506_1_source_charge_missing",
        "failure": "no proof that exterior source/current charge vanishes",
        "effect": "field can carry radial/fifth-force hair",
        "repair": "derive compact support/worldtube source law or bound channel numerically",
    },
    {
        "failure_id": "F506_2_boundary_flux_missing",
        "failure": "boundary or exact term has no zero-flux theorem",
        "effect": "divergence can become observable mass/PPN flux",
        "repair": "prove linking-sphere flux zero or add residual row",
    },
    {
        "failure_id": "F506_3_calibration_missing",
        "failure": "constant charge not proven to equal measured GM",
        "effect": "local Newton recovery is not established",
        "repair": "derive source-measure/Gauss/Poisson normalization",
    },
]

DECISION_ROWS = [
    {
        "decision_id": "DEC506_0_partial_derivation",
        "decision": "positive_operator_silence_route_is_valid",
        "meaning": "extra-sector silence can be derived, but only field-by-field from positive source-free equations and zero boundary/source charge",
        "claim_status": "conditional",
    },
    {
        "decision_id": "DEC506_1_not_enough_for_MTS",
        "decision": "MTS_local_EH_reduction_not_yet_derived",
        "meaning": "the current corpus has the right gate but not all field-specific operators and source charges needed to pass it",
        "claim_status": "no_local_GR_claim",
    },
    {
        "decision_id": "DEC506_2_next_queue",
        "decision": "split_by_sector",
        "meaning": "attack kappa/G_eff, domain/projector, memory, motion/time/flow, and boundary sectors one at a time",
        "claim_status": NEXT_TARGET,
    },
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RU506_0",
        "status": "silence_mechanism_identified",
        "update": "the non-cheat mechanism is positive source-free operator plus no charge and zero boundary flux",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU506_1",
        "status": "sector_debt_explicit",
        "update": "local EH reduction remains open because each MTS extra sector needs its own operator/sign/source/boundary proof",
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
            "check_id": "V506_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V506_1_energy_identity_present",
            "result": "pass",
            "detail": f"energy_identity_rows={len(ENERGY_IDENTITY_ROWS)}",
        },
        {
            "check_id": "V506_2_sector_status_explicit",
            "result": "pass",
            "detail": f"sector_rows={len(SECTOR_STATUS_ROWS)}",
        },
        {
            "check_id": "V506_3_no_overclaim",
            "result": "pass",
            "detail": "local_EH_reduction_derived_for_MTS=false",
        },
        {
            "check_id": "V506_4_local_GR_claim_blocked",
            "result": "pass",
            "detail": "local_GR_claim_allowed=false",
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
    return f"""# 506 — Local EH Reduction and Extra-Sector Silence Theorem

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

We can derive the **shape** of the silence mechanism, but not yet prove MTS satisfies it.

The good mechanism is:

```text
extra field obeys a positive source-free local operator
+ no exterior source charge
+ zero boundary/linking-sphere flux
=> the field is zero, pure gauge, topological, or constant universal in the compact local exterior.
```

That is an honest route to EH-plus-silent reduction. It does **not** smuggle in a plateau. It says exactly what each non-GR sector must prove.

The bad news, kept clean:

```text
MTS has not yet supplied every sector-specific operator, sign, source-charge law, and boundary condition.
```

So the local branch is not dead, but it is not promoted. It now becomes a finite queue of field-specific silence proofs.

## 2. Theorem Attempt

{markdown_table(THEOREM_ATTEMPT_ROWS)}

## 3. Energy Identities

{markdown_table(ENERGY_IDENTITY_ROWS)}

## 4. Operator Classification Requirements

{markdown_table(OPERATOR_REQUIREMENTS_ROWS)}

## 5. MTS Sector Silence Status

{markdown_table(SECTOR_STATUS_ROWS)}

## 6. Failure Ledger

{markdown_table(FAILURE_LEDGER_ROWS)}

## 7. Decision

{markdown_table(DECISION_ROWS)}

## 8. Source Register

{markdown_table(sources)}

## 9. Validation

{markdown_table(validations)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. Claim Ceiling

Allowed:

```text
MTS has a clear conditional mechanism for extra-sector silence.
MTS can reduce local EH recovery to a finite set of field-specific operator/source/boundary proofs.
```

Forbidden:

```text
MTS has derived local EH reduction.
MTS has derived local GR.
MTS has derived Newtonian recovery.
MTS has proven kappa/domain/memory/motion/time/boundary sectors are all silent.
```

## 12. Next Target

`{NEXT_TARGET}`

Attack the sectors one at a time. Start with whichever sector has the cleanest parent equation: kappa/G_eff if available, otherwise domain/projector or memory. The pass/fail rule is now sharp: positive source-free operator plus no source charge plus zero boundary flux, or retained residual.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-local-EH-reduction-and-extra-sector-silence-theorem"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (THEOREM_ATTEMPT_PATH, THEOREM_ATTEMPT_ROWS),
        (ENERGY_IDENTITY_PATH, ENERGY_IDENTITY_ROWS),
        (OPERATOR_REQUIREMENTS_PATH, OPERATOR_REQUIREMENTS_ROWS),
        (SECTOR_STATUS_PATH, SECTOR_STATUS_ROWS),
        (FAILURE_LEDGER_PATH, FAILURE_LEDGER_ROWS),
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
        "theorem_attempt": str(ROOT / THEOREM_ATTEMPT_PATH),
        "energy_identity": str(ROOT / ENERGY_IDENTITY_PATH),
        "operator_requirements": str(ROOT / OPERATOR_REQUIREMENTS_PATH),
        "sector_status": str(ROOT / SECTOR_STATUS_PATH),
        "failure_ledger": str(ROOT / FAILURE_LEDGER_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "conditional_extra_sector_silence_mechanism": True,
        "positive_operator_energy_identity_derived": True,
        "local_EH_reduction_derived_for_MTS": False,
        "extra_sector_silence_derived_for_all_MTS_sectors": False,
        "kappa_Geff_silence_derived": False,
        "motion_time_flow_silence_derived": False,
        "domain_projector_silence_derived": False,
        "memory_kernel_silence_derived": False,
        "boundary_topological_flux_zero_derived": False,
        "operator_vector_zero_or_executable_complete": False,
        "source_measure_matching_derived": False,
        "parent_Noether_mass_charge_closure_derived_for_MTS": False,
        "epsilon_radial_Meff_zero_derived_for_MTS": False,
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
