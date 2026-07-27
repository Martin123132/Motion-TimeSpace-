from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "field_specific_silence_queue_built_kappa_Geff_first"
CLAIM_CEILING = "queue_only_no_sector_silence_or_local_GR_promotion"
NEXT_TARGET = "508-constant-kappa-superselection-or-drift-residual.md"

DOC_PATH = Path("507-field-specific-silence-queue-kappa-domain-memory-motion.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_QUEUE_SOURCE_REGISTER.csv")
QUEUE_PATH = Path("source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_QUEUE.csv")
DEPENDENCIES_PATH = Path("source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_DEPENDENCIES.csv")
ACCEPTANCE_GATES_PATH = Path("source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_ACCEPTANCE_GATES.csv")
FIRST_TARGET_PATH = Path("source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_FIRST_TARGET.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_QUEUE_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_FIELD_SPECIFIC_SILENCE_QUEUE_ROUTE_UPDATE.csv")

SOURCE_REGISTER = [
    {
        "source_file": "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
        "role": "establishes the positive-operator/no-source/zero-boundary silence mechanism and leaves sector debts",
    },
    {
        "source_file": "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md",
        "role": "conditional mass-charge closure theorem requiring EH-plus-silent exterior",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MTS_SECTOR_SILENCE_STATUS.csv",
        "role": "six sector debts from checkpoint 506",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv",
        "role": "constant measured-GM theorem attempt and kappa/G_eff blocker",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_constant_universal_Geff_kappa_CONTRACT.csv",
        "role": "constant universal kappa/G_eff contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_constant_sector_universality_CONTRACT.csv",
        "role": "constant-sector independence contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_PREMISE_OWNERSHIP.csv",
        "role": "domain/projector ownership blockers",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_DECISION.csv",
        "role": "memory double-zero status",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_YLOC_SOURCE_DEBT_LEDGER.csv",
        "role": "motion/time/flow source-current debt ledger",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_BOUNDARY_SCALAR_PREMISE_REPAIR_LEDGER.csv",
        "role": "boundary scalar/no-flux premise debt",
    },
    {
        "source_file": "source-intake/mts_residuals/R11_OPERATOR_VECTOR_FILL_QUEUE.csv",
        "role": "existing R11 operator-vector priority queue",
    },
    {
        "source_file": "scripts/field_specific_silence_queue_kappa_domain_memory_motion.py",
        "role": "this checkpoint generator",
    },
]

QUEUE_ROWS = [
    {
        "priority": "1",
        "sector": "kappa_Geff_source_normalization",
        "why_first": "largest Newton/GR bridge blocker: measured GM, Gdot, radial hair, and source-normalization all depend on constant universal G_eff/kappa",
        "required_theorem": "kappa_eff is a parent global coupling or superselection label with D_X kappa_eff=0 for time, radius, species, range, frame, and domain directions",
        "acceptance_gate": "derive global-coupling superselection from parent action or keep dln_Geff_dt/dln_Geff_dr/source/range residual rows",
        "mapped_rows": "R1;R4;R9;R10;R11;P8_Geff_time_drift;P8_radial_source_hair",
        "next_target": NEXT_TARGET,
        "claim_status": "open",
    },
    {
        "priority": "2",
        "sector": "source_measure_and_Meff_flux",
        "why_first": "constant kappa is not enough unless M_eff is the conserved parent source charge",
        "required_theorem": "M_eff = M_source[W] = integral_S Q_M and d(Pi_M J_H)=0 in compact exterior",
        "acceptance_gate": "derive worldtube source-measure matching and Pi_M/Q_M flux closure, or retain radial/time mass flux residuals",
        "mapped_rows": "R4;R9;R11;P8_Meff_conservation;P8_radial_source_hair",
        "next_target": "after_508_source_measure_flux_closure",
        "claim_status": "open",
    },
    {
        "priority": "3",
        "sector": "domain_projector_selector",
        "why_first": "domain/vector/projector rows hit alpha1/alpha2/alpha3/xi and R11 hard",
        "required_theorem": "domain selector carries no preferred vector, no projector stress, no anisotropy, and no source-normalization monopole",
        "acceptance_gate": "derive parent-owned topological P_D plus no-vector/no-stress theorem, or fill coefficient products",
        "mapped_rows": "R5;R6;R7;R8;R11",
        "next_target": "domain_projector_no_vector_no_stress_theorem",
        "claim_status": "open",
    },
    {
        "priority": "4",
        "sector": "memory_kernel",
        "why_first": "cosmology-friendly memory cannot be imported into local systems without a compact-local silence theorem",
        "required_theorem": "local memory kernel is causal, stable, source-free, and becomes constant universal or zero in compact local exterior",
        "acceptance_gate": "derive compact-local kernel energy/Lyapunov identity or fill alpha3/Gdot/alpha(lambda) map",
        "mapped_rows": "R7;R9;R10;R11",
        "next_target": "compact_local_memory_kernel_silence_or_residual_map",
        "claim_status": "open",
    },
    {
        "priority": "5",
        "sector": "motion_time_flow_modes",
        "why_first": "Y_loc positive Euler route exists, but source currents are not zeroed",
        "required_theorem": "motion/time/flow auxiliary modes have positive operator, no linear source, and zero boundary current",
        "acceptance_gate": "derive parent Z2/no-linear-source symmetry and component map, or retain Yloc closure rows",
        "mapped_rows": "Yloc;R11;P8_source_current",
        "next_target": "Yloc_component_zero_or_closure_fill_resume",
        "claim_status": "open",
    },
    {
        "priority": "6",
        "sector": "boundary_topological_terms",
        "why_first": "boundary flux can make a divergence physically visible in mass/PPN rows",
        "required_theorem": "boundary action is parent-owned scalar/topological with zero linking-sphere flux or fixed background subtraction",
        "acceptance_gate": "derive no-flux/homogeneous scalar collar theorem including beta/xi/Gdot, or retain boundary coefficient map",
        "mapped_rows": "R3;R4;R7;R8;R9;R11",
        "next_target": "boundary_no_flux_full_channel_after_core_sectors",
        "claim_status": "open",
    },
    {
        "priority": "7",
        "sector": "metric_EH_operator_core",
        "why_first": "final local GR promotion requires EH-only or executable non-EH operator vector",
        "required_theorem": "local metric/coframe operator reduces to EH plus allowed Lambda/background subtraction",
        "acceptance_gate": "derive Lovelock/metric-only/second-order/local branch premises or fill R11 vector",
        "mapped_rows": "R2;R3;R4;R8;R10;R11",
        "next_target": "EH_operator_core_after_source_normalization_and_silence",
        "claim_status": "open",
    },
]

DEPENDENCY_ROWS = [
    {
        "dependency_id": "DEP507_0_kappa_before_GM",
        "from_sector": "kappa_Geff_source_normalization",
        "to_sector": "source_measure_and_Meff_flux",
        "reason": "measured GM cannot be constant if G_eff can drift independently of M_eff",
    },
    {
        "dependency_id": "DEP507_1_source_measure_before_Newton",
        "from_sector": "source_measure_and_Meff_flux",
        "to_sector": "metric_EH_operator_core",
        "reason": "EH weak-field equations need the same source charge that orbital readout calls M_eff",
    },
    {
        "dependency_id": "DEP507_2_domain_memory_boundary_before_extra_zero",
        "from_sector": "domain_projector_selector;memory_kernel;boundary_topological_terms",
        "to_sector": "source_measure_and_Meff_flux",
        "reason": "all can contribute mu_extra or source-current leakage unless theorem-zeroed or bounded",
    },
    {
        "dependency_id": "DEP507_3_Yloc_before_double_zero",
        "from_sector": "motion_time_flow_modes",
        "to_sector": "metric_EH_operator_core",
        "reason": "double-zero operator suppression works only if the local silence multiplet is actually zero",
    },
]

ACCEPTANCE_GATE_ROWS = [
    {
        "gate_id": "G507_0_theorem_zero",
        "required_evidence": "parent action equation, Euler/Noether identity, zero source charge, zero boundary flux, and explicit mapped residual rows",
        "claim_credit": "derived_zero",
        "forbidden_shortcut": "closure assumption or fit-level cancellation",
    },
    {
        "gate_id": "G507_1_numeric_bound",
        "required_evidence": "source-backed coefficient/residual with units, normalization, path, assumptions, and local-bound comparison",
        "claim_credit": "derived_bound_or_numeric_residual",
        "forbidden_shortcut": "template row, symbolic coefficient, missing source path, or total cancellation without individual channel passes",
    },
    {
        "gate_id": "G507_2_demote",
        "required_evidence": "no theorem-zero and no source-backed bound available",
        "claim_credit": "closure_only",
        "forbidden_shortcut": "local GR/Newton/PPN promotion",
    },
]

FIRST_TARGET_ROWS = [
    {
        "target_id": "FT507_0",
        "target": NEXT_TARGET,
        "sector": "kappa_Geff_source_normalization",
        "attempt_question": "Can kappa_eff be made a parent global coupling/superselection label rather than a local field?",
        "success_condition": "D_X kappa_eff=0 is derived for all local/source/range/frame/domain directions before readout",
        "failure_condition": "kappa depends on MTS invariants or local fields, requiring drift/range/source residual rows",
        "why_this_is_first": "without constant G_eff/kappa, even a closed M_eff charge does not give Newton/GR measured GM",
    }
]

ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RU507_0",
        "status": "queue_built",
        "update": "sector debts are ordered by their ability to unlock source-normalized Newton and local GR",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RU507_1",
        "status": "claim_ceiling_retained",
        "update": "no sector is promoted; each must pass theorem-zero or numeric-bound gates",
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
    first_priority = [row for row in QUEUE_ROWS if row["priority"] == "1" and row["sector"] == "kappa_Geff_source_normalization"]
    return [
        {
            "check_id": "V507_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V507_1_sector_coverage",
            "result": "pass",
            "detail": f"sector_rows={len(QUEUE_ROWS)}",
        },
        {
            "check_id": "V507_2_first_target_selected",
            "result": "pass" if first_priority else "fail",
            "detail": "priority_1=kappa_Geff_source_normalization",
        },
        {
            "check_id": "V507_3_acceptance_gates_explicit",
            "result": "pass",
            "detail": f"gates={len(ACCEPTANCE_GATE_ROWS)}",
        },
        {
            "check_id": "V507_4_local_GR_claim_blocked",
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
    return f"""# 507 — Field-Specific Silence Queue: Kappa, Domain, Memory, Motion

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The next work should **not** try to solve every sector at once.

The first target is `kappa/G_eff` because it controls whether measured `GM` can be constant before we even worry about the detailed extra-field operator zoo.

If `G_eff` is not parent-fixed, then the local Newton/GR bridge inherits time drift, radial hair, source dependence, range dependence, and frame/domain dependence. If it is parent-fixed, one major blocker is removed and the remaining work can focus on `M_eff`, `mu_extra`, and EH/operator silence.

## 2. Ordered Queue

{markdown_table(QUEUE_ROWS)}

## 3. Dependencies

{markdown_table(DEPENDENCY_ROWS)}

## 4. Acceptance Gates

{markdown_table(ACCEPTANCE_GATE_ROWS)}

## 5. First Target

{markdown_table(FIRST_TARGET_ROWS)}

## 6. Source Register

{markdown_table(sources)}

## 7. Validation

{markdown_table(validations)}

## 8. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 9. Claim Ceiling

Allowed:

```text
MTS has a field-specific silence queue.
MTS has selected kappa/G_eff as the first local-GR bridge blocker to attack.
```

Forbidden:

```text
MTS has proved any sector is silent.
MTS has proved G_eff/kappa is constant.
MTS has derived local GR or Newtonian recovery.
```

## 10. Next Target

`{NEXT_TARGET}`

Try to derive `kappa_eff` as a parent global coupling/superselection label. If that fails, write the residual contract for `dln_Geff_dt`, radial/range/source dependence, and frame/domain dependence instead of hiding it inside measured `GM`.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-field-specific-silence-queue-kappa-domain-memory-motion"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (QUEUE_PATH, QUEUE_ROWS),
        (DEPENDENCIES_PATH, DEPENDENCY_ROWS),
        (ACCEPTANCE_GATES_PATH, ACCEPTANCE_GATE_ROWS),
        (FIRST_TARGET_PATH, FIRST_TARGET_ROWS),
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
        "queue": str(ROOT / QUEUE_PATH),
        "dependencies": str(ROOT / DEPENDENCIES_PATH),
        "acceptance_gates": str(ROOT / ACCEPTANCE_GATES_PATH),
        "first_target": str(ROOT / FIRST_TARGET_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "sector_queue_rows": len(QUEUE_ROWS),
        "first_sector": "kappa_Geff_source_normalization",
        "kappa_Geff_silence_derived": False,
        "domain_projector_silence_derived": False,
        "memory_kernel_silence_derived": False,
        "motion_time_flow_silence_derived": False,
        "boundary_flux_zero_derived": False,
        "metric_EH_operator_core_derived": False,
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
