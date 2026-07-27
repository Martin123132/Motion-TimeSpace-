from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_FIRST_DELTA_REF_BOUND_VALUE_RUNNER_OR_SAME_FRAME_DENOMINATOR_SOURCE_2459"
CHECKPOINT_ID = "2459"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
HAMILTONIAN = ROOT / "source-intake" / "hamiltonian-source"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2459-Y5-R2FR-first-Delta-ref-bound-value-runner-or-same-frame-denominator-source.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2459_SOURCE_REGISTER.csv",
    "denominator_gate": OUT / "P8_Y5_PARENT_QLOC_2459_DENOMINATOR_SOURCE_GATE.csv",
    "bound_values": OUT / "P8_Y5_PARENT_QLOC_2459_BOUND_VALUE_CANDIDATES.csv",
    "runner_results": OUT / "P8_Y5_PARENT_QLOC_2459_NO_CANCELLATION_RUNNER_RESULTS.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2459_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2459_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2459_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2459_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2459_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_denominator": QUEUE / "JR2459_DENOMINATOR_SOURCE_GATE_NONCLAIM.csv",
    "queue_runner": QUEUE / "JR2459_NO_CANCELLATION_RUNNER_RESULTS_NONCLAIM.csv",
    "hamiltonian_runner": HAMILTONIAN / "Delta_ref_no_cancellation_runner_2459_NONCLAIM.csv",
    "local_bound_runner": LOCAL_BOUNDS / "Delta_ref_no_cancellation_runner_2459_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2459_00_2458_doc",
        "source_path": ROOT / "2458-Y5-R2FR-parent-action-signature-hunt-or-reference-route-demotion.md",
        "needles": ["REFERENCE_ZERO_ROUTE_DEMOTED_TO_EXPLICIT_CLOSURE_FOR_CURRENT_MTS", "BND2458_4_same_frame_denominator", "NEXT2458_0_selected", "VAL2458_OVERALL"],
        "role": "handoff selecting finite Delta_ref bound path",
    },
    {
        "source_id": "SRC2459_01_2458_bound_ledger",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2458_DELTA_REF_BOUND_ACQUISITION_LEDGER.csv",
        "needles": ["BND2458_4_same_frame_denominator", "MISSING_VALUE", "BND2458_5_no_cancellation_total"],
        "role": "machine-readable finite bound targets",
    },
    {
        "source_id": "SRC2459_02_2456_bound_rows",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2456_FIRST_DELTA_REF_BOUND_ROWS.csv",
        "needles": ["DBR2456_0_partial_q_Bref_bound", "MISSING_BOUND_INPUTS", "DBR2456_5_total_Delta_ref_bound"],
        "role": "component formulas for boundary leak residual",
    },
    {
        "source_id": "SRC2459_03_2457_bound_inputs",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2457_DELTA_REF_BOUND_VALUE_INPUTS.csv",
        "needles": ["BVI2457_1_metric_norm_value", "BVI2457_4_total_first_bound_value", "MISSING_VALUE"],
        "role": "bound value input schema",
    },
    {
        "source_id": "SRC2459_04_1006_denominator",
        "source_path": ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md",
        "needles": ["MHS1006_0_Htau_minus_Href", "CG1006_0_MHref_positive_same_frame", "ORBITAL_GM_SUBSTITUTION_REJECTED", "V1006_SUMMARY"],
        "role": "H_tau-H_ref denominator schema and orbital-GM rejection",
    },
    {
        "source_id": "SRC2459_05_1017_reference_lock",
        "source_path": ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
        "needles": ["HRL1017_5_MHref_denominator", "MHR1017_0_M_H_ref_denominator", "CG1017_4_MHref_claim"],
        "role": "Hamiltonian/source charge denominator blocker",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: bool) -> str:
    return "True" if value else "False"


def metadata(valid_for_claim: bool = False, claim_allowed: bool = False) -> dict[str, str]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": truth(valid_for_claim),
        "claim_allowed": truth(claim_allowed),
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def cell(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def table(columns: list[str], rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                **metadata(),
                "source_id": source["source_id"],
                "source_path": str(path),
                "exists": truth(path.exists()),
                "needles": ";".join(source["needles"]),
                "missing_needles": ";".join(missing),
                "source_pass": truth(path.exists() and not missing),
                "role": source["role"],
            }
        )
    return rows


def denominator_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "denominator_id": "DEN2459_0_live_MHref_schema",
            "quantity": "M_H_ref",
            "method": "positive dressed same-frame Hamiltonian/Noether charge",
            "value": "MISSING_STABLE_MH_REF",
            "units": "MISSING_UNITS",
            "source_path": str(ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md"),
            "equation_ref": "MHR1017_0_M_H_ref_denominator",
            "same_frame": "False",
            "positive": "False",
            "orbital_gm_import": "False",
            "status": "BLOCKED_MISSING_STABLE_MH_REF",
            "valid_for_claim": "False",
        },
        {
            "denominator_id": "DEN2459_1_live_Htau_minus_Href_schema",
            "quantity": "M_H_ref",
            "method": "H_tau[S_link]-H_ref",
            "value": "MISSING_H_TAU_AND_H_REF",
            "units": "MISSING_UNITS",
            "source_path": str(ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md"),
            "equation_ref": "MHS1006_0_Htau_minus_Href",
            "same_frame": "False",
            "positive": "False",
            "orbital_gm_import": "False",
            "status": "BLOCKED_MISSING_HAMILTONIAN_VALUES",
            "valid_for_claim": "False",
        },
        {
            "denominator_id": "DEN2459_2_rejected_orbital_GM",
            "quantity": "GM_orbit/G_ref",
            "method": "observed orbital readout substitution",
            "value": "REJECTED",
            "units": "mass",
            "source_path": str(ROOT / "1006-Y5-R10-MHref-positive-same-frame-denominator-or-Htau-source-row.md"),
            "equation_ref": "MHR1006_3_orbital_GM_substitution",
            "same_frame": "False",
            "positive": "UNKNOWN",
            "orbital_gm_import": "True",
            "status": "REJECTED_CIRCULAR_DENOMINATOR",
            "valid_for_claim": "False",
        },
        {
            "denominator_id": "DEN2459_3_toy_smoke_denominator",
            "quantity": "N_E_smoke",
            "method": "internal smoke denominator only",
            "value": "1.0",
            "units": "arb",
            "source_path": "SELF_TEST_ONLY",
            "equation_ref": "SMOKE2459",
            "same_frame": "True",
            "positive": "True",
            "orbital_gm_import": "False",
            "status": "SCHEMA_SMOKE_ONLY",
            "valid_for_claim": "False",
        },
    ]
    return [{**metadata(), **row, "claim_allowed": "False"} for row in rows]


def bound_value_rows() -> list[dict[str, Any]]:
    live_source = str(OUT / "P8_Y5_PARENT_QLOC_2458_DELTA_REF_BOUND_ACQUISITION_LEDGER.csv")
    rows = [
        {
            "candidate_id": "BVC2459_0_live_metric_leak",
            "quantity": "C_sigma*max(||D_q sigma_AB||,||D_source sigma_AB||)",
            "component_group": "live",
            "value": "MISSING_VALUE",
            "units": "MISSING_UNITS",
            "denominator_id": "DEN2459_0_live_MHref_schema",
            "source_path": live_source,
            "equation_ref": "BND2458_0_metric_leak",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "BVC2459_1_live_tau_leak",
            "quantity": "C_tau*max(||D_q tau||,||D_source tau||)",
            "component_group": "live",
            "value": "MISSING_VALUE",
            "units": "MISSING_UNITS",
            "denominator_id": "DEN2459_0_live_MHref_schema",
            "source_path": live_source,
            "equation_ref": "BND2458_1_tau_leak",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "BVC2459_2_live_counterterm_leak",
            "quantity": "max(|D_q B_ct|,|D_source B_ct|)",
            "component_group": "live",
            "value": "MISSING_VALUE",
            "units": "MISSING_UNITS",
            "denominator_id": "DEN2459_0_live_MHref_schema",
            "source_path": live_source,
            "equation_ref": "BND2458_2_counterterm_leak",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "BVC2459_3_live_topological_leak",
            "quantity": "C_top*max(|D_q C_top|,|D_source C_top|)",
            "component_group": "live",
            "value": "MISSING_VALUE",
            "units": "MISSING_UNITS",
            "denominator_id": "DEN2459_0_live_MHref_schema",
            "source_path": live_source,
            "equation_ref": "BND2458_3_topological_leak",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "BVC2459_4_smoke_metric_leak",
            "quantity": "C_sigma*max(||D_q sigma_AB||,||D_source sigma_AB||)",
            "component_group": "smoke",
            "value": "1.0e-8",
            "units": "arb",
            "denominator_id": "DEN2459_3_toy_smoke_denominator",
            "source_path": "SELF_TEST_ONLY",
            "equation_ref": "SMOKE2459",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "BVC2459_5_smoke_tau_leak",
            "quantity": "C_tau*max(||D_q tau||,||D_source tau||)",
            "component_group": "smoke",
            "value": "2.0e-8",
            "units": "arb",
            "denominator_id": "DEN2459_3_toy_smoke_denominator",
            "source_path": "SELF_TEST_ONLY",
            "equation_ref": "SMOKE2459",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "BVC2459_6_smoke_counterterm_leak",
            "quantity": "max(|D_q B_ct|,|D_source B_ct|)",
            "component_group": "smoke",
            "value": "3.0e-9",
            "units": "arb",
            "denominator_id": "DEN2459_3_toy_smoke_denominator",
            "source_path": "SELF_TEST_ONLY",
            "equation_ref": "SMOKE2459",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "BVC2459_7_smoke_topological_leak",
            "quantity": "C_top*max(|D_q C_top|,|D_source C_top|)",
            "component_group": "smoke",
            "value": "0.0",
            "units": "arb",
            "denominator_id": "DEN2459_3_toy_smoke_denominator",
            "source_path": "SELF_TEST_ONLY",
            "equation_ref": "SMOKE2459",
            "valid_for_claim": "False",
        },
    ]
    return [{**metadata(), **row, "claim_allowed": "False"} for row in rows]


def numeric(value: Any) -> float | None:
    try:
        parsed = float(str(value))
    except ValueError:
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def run_no_cancellation(denominators: list[dict[str, Any]], values: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_den = {row["denominator_id"]: row for row in denominators}
    groups = sorted({row["component_group"] for row in values})
    rows: list[dict[str, Any]] = []
    for group in groups:
        group_values = [row for row in values if row["component_group"] == group]
        denominator_ids = sorted({row["denominator_id"] for row in group_values})
        if len(denominator_ids) != 1:
            rows.append(
                {
                    **metadata(),
                    "result_id": f"RUN2459_{group}",
                    "component_group": group,
                    "denominator_id": ";".join(denominator_ids),
                    "status": "REFUSED_MULTIPLE_DENOMINATORS",
                    "component_sum_abs": "NOT_COMPUTED",
                    "denominator_value": "NOT_COMPUTED",
                    "Delta_ref_bound_over_denominator": "NOT_COMPUTED",
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                    "blockers": "MULTIPLE_DENOMINATORS",
                }
            )
            continue
        denominator = by_den.get(denominator_ids[0])
        denominator_value = numeric(denominator["value"]) if denominator else None
        numeric_components = [numeric(row["value"]) for row in group_values]
        missing_components = [row["candidate_id"] for row, value in zip(group_values, numeric_components) if value is None]
        blockers: list[str] = []
        if denominator is None:
            blockers.append("MISSING_DENOMINATOR_ROW")
        else:
            if denominator["valid_for_claim"] != "True":
                blockers.append("DENOMINATOR_VALID_FOR_CLAIM_FALSE")
            if denominator["same_frame"] != "True":
                blockers.append("DENOMINATOR_NOT_SAME_FRAME")
            if denominator["positive"] != "True":
                blockers.append("DENOMINATOR_NOT_POSITIVE")
            if denominator["orbital_gm_import"] == "True":
                blockers.append("ORBITAL_GM_DENOMINATOR_REJECTED")
        if denominator_value is None or denominator_value <= 0:
            blockers.append("MISSING_OR_NONPOSITIVE_DENOMINATOR_VALUE")
        if missing_components:
            blockers.append("MISSING_COMPONENT_VALUES:" + ";".join(missing_components))
        if any(row["valid_for_claim"] != "True" for row in group_values):
            blockers.append("COMPONENT_VALID_FOR_CLAIM_FALSE")

        if denominator_value is not None and denominator_value > 0 and not missing_components:
            component_sum = sum(abs(value or 0.0) for value in numeric_components)
            ratio = component_sum / denominator_value
            status = "COMPUTED_NONCLAIM" if blockers else "COMPUTED_CLAIM_CANDIDATE"
            component_sum_text = f"{component_sum:.16e}"
            ratio_text = f"{ratio:.16e}"
        else:
            status = "BLOCKED_NOT_COMPUTED"
            component_sum_text = "NOT_COMPUTED"
            ratio_text = "NOT_COMPUTED"

        rows.append(
            {
                **metadata(valid_for_claim=False, claim_allowed=False),
                "result_id": f"RUN2459_{group}",
                "component_group": group,
                "denominator_id": denominator_ids[0],
                "status": status,
                "component_sum_abs": component_sum_text,
                "denominator_value": str(denominator_value) if denominator_value is not None else "NOT_NUMERIC",
                "Delta_ref_bound_over_denominator": ratio_text,
                "claim_allowed": "False",
                "valid_for_claim": "False",
                "blockers": ";".join(blockers) if blockers else "NONE",
            }
        )
    return rows


def claim_gate_rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2459_0_runner_operational",
            "claim": "No-cancellation finite Delta_ref runner works on numeric schema rows.",
            "gate_status": "PASS",
            "reason": "smoke group computes a nonclaim absolute-sum residual",
            "gate_pass": "True",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2459_1_live_denominator",
            "claim": "Live same-frame N_E/M_H_ref denominator is available.",
            "gate_status": "BLOCKED",
            "reason": "1006/1017 denominator candidates remain missing or explicitly blocked",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2459_2_orbital_GM",
            "claim": "Orbital GM can fill the denominator.",
            "gate_status": "REFUSED",
            "reason": "orbital GM substitution is circular for a GR/Newton reduction proof",
            "gate_pass": "True",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2459_3_live_bound_values",
            "claim": "Live metric/tau/counterterm/topology leak values are sourced.",
            "gate_status": "BLOCKED",
            "reason": "component values are missing and valid_for_claim=false",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2459_4_local_GR",
            "claim": "Local GR/Newton/PPN branch passes from finite Delta_ref bound.",
            "gate_status": "BLOCKED",
            "reason": "live runner result is not computed and smoke result is nonclaim",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2459_0_denominator_first",
            "decision": "The finite Delta_ref path is denominator-first.",
            "reason": "all residual bounds divide by N_E/M_H_ref; without same-frame positivity the numbers would be meaningless",
            "effect": "do not collect component values as claim evidence until denominator is sourced",
        },
        {
            "decision_id": "DEC2459_1_orbital_GM_refused",
            "decision": "Reject orbital GM as denominator filler.",
            "reason": "that imports the Newton/GR readout into the theorem meant to derive it",
            "effect": "M_H_ref must come from parent Hamiltonian/source charge or remain blocked",
        },
        {
            "decision_id": "DEC2459_2_smoke_nonclaim",
            "decision": "Keep the numeric smoke row as schema validation only.",
            "reason": "it verifies the absolute-sum runner without pretending to measure MTS",
            "effect": "runner can be trusted to refuse live rows and compute future sourced rows",
        },
        {
            "decision_id": "DEC2459_3_next_derivation",
            "decision": "Next target should attack same-frame Hamiltonian denominator again, but with the 2458/2459 no-circularity contract in front.",
            "reason": "a sourced denominator unlocks both finite residual testing and any future zero route normalization",
            "effect": "2460 should derive or formally bound M_H_ref before component-value chasing",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2459_0_selected",
            "selection_status": "selected",
            "target_file": "2460-Y5-R2FR-same-frame-Hamiltonian-denominator-derivation-or-retain-local-bound-block.md",
            "target_script": "scripts/Y5_R2FR_same_frame_Hamiltonian_denominator_derivation_or_retain_local_bound_block_2460.py",
            "task": "derive a positive same-frame M_H_ref/N_E from parent Hamiltonian charge with fixed reference and tau/coframe lock, or prove why finite Delta_ref local scoring must remain blocked",
            "acceptance_target": "parent-owned H_tau/H_ref/tau/coframe/boundary/domain/source-path rows, or explicit denominator block that prevents local-GR scoring",
            "guardrails": "no orbital-GM denominator; no fitted mass; no reference-only normalization; no cancellation; no local-GR claim; no GitHub",
        }
    ]
    return [{**metadata(), **row} for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("queue_denominator", OUTPUTS["denominator_gate"], COPY_TARGETS["queue_denominator"]),
        ("queue_runner", OUTPUTS["runner_results"], COPY_TARGETS["queue_runner"]),
        ("hamiltonian_runner", OUTPUTS["runner_results"], COPY_TARGETS["hamiltonian_runner"]),
        ("local_bound_runner", OUTPUTS["runner_results"], COPY_TARGETS["local_bound_runner"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copy_specs:
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, target)
        rows.append(
            {
                **metadata(),
                "copy_id": copy_id,
                "source_path": str(source),
                "target_path": str(target),
                "source_exists": truth(source.exists()),
                "target_exists": truth(target.exists()),
            }
        )
    return rows


def csv_parse_status(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as exc:  # pragma: no cover - diagnostic only
        return False, 0, repr(exc)


def formalization_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return list(FORMALIZATION.rglob("*2459*"))


def validation_rows(
    source_rows: list[dict[str, Any]],
    denominators: list[dict[str, Any]],
    values: list[dict[str, Any]],
    results: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail})

    add(
        "VAL2459_00_sources_exist",
        all(row["source_pass"] == "True" for row in source_rows),
        "all cited source paths exist and needles are present",
        ";".join(row["source_id"] for row in source_rows if row["source_pass"] != "True"),
    )
    add(
        "VAL2459_01_denominator_gate_written",
        len(denominators) >= 4 and any(row["status"] == "REJECTED_CIRCULAR_DENOMINATOR" for row in denominators),
        "denominator candidates include live blockers, orbital-GM rejection, and smoke-only row",
    )
    add(
        "VAL2459_02_live_denominators_invalid",
        all(row["valid_for_claim"] == "False" for row in denominators if row["denominator_id"].startswith("DEN2459_0") or row["denominator_id"].startswith("DEN2459_1")),
        "live denominator rows remain invalid for claim",
    )
    add(
        "VAL2459_03_bound_values_written",
        len(values) >= 8 and all(row["valid_for_claim"] == "False" for row in values),
        "live and smoke component rows are present and nonclaim",
    )
    add(
        "VAL2459_04_live_runner_blocked",
        any(row["component_group"] == "live" and row["status"] == "BLOCKED_NOT_COMPUTED" for row in results),
        "live residual is blocked rather than computed",
    )
    add(
        "VAL2459_05_smoke_runner_computes_nonclaim",
        any(row["component_group"] == "smoke" and row["status"] == "COMPUTED_NONCLAIM" and row["Delta_ref_bound_over_denominator"] != "NOT_COMPUTED" for row in results),
        "smoke residual computes but stays nonclaim",
    )
    add(
        "VAL2459_06_claim_gates_safe",
        all(row["claim_allowed"] == "False" for row in gates) and any(row["gate_id"] == "GATE2459_4_local_GR" and row["gate_status"] == "BLOCKED" for row in gates),
        "local-GR/PPN/Newton claims remain blocked",
    )
    add(
        "VAL2459_07_next_target_written",
        len(next_rows) == 1 and next_rows[0]["route_id"] == "NEXT2459_0_selected",
        "2460 same-frame denominator derivation target selected",
    )
    add(
        "VAL2459_08_branch_copies",
        len(branch_rows) == 4 and all(row["target_exists"] == "True" for row in branch_rows),
        "nonclaim branch copies exist",
    )
    hits = formalization_hits()
    add(
        "VAL2459_09_no_formalization_artifacts",
        not hits,
        "no 2459 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in hits),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parse_status(path)
        add(
            f"VAL2459_CSV_{path.stem}",
            ok,
            f"CSV parses with {count} rows" if ok else "CSV parse failed",
            detail or str(path),
        )

    for key, path in COPY_TARGETS.items():
        ok, count, detail = csv_parse_status(path)
        add(
            f"VAL2459_COPY_CSV_{key}",
            ok,
            f"copy CSV parses with {count} rows" if ok else "copy CSV parse failed",
            detail or str(path),
        )

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2459_OVERALL",
        overall,
        "2459 installs a denominator-first no-cancellation runner; smoke computes, live claims remain blocked",
    )
    return [{**metadata(), **row} for row in rows]


def write_doc(
    sources: list[dict[str, Any]],
    denominators: list[dict[str, Any]],
    values: list[dict[str, Any]],
    results: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    doc = "\n\n".join(
        [
            "# 2459 Y5 R2FR First Delta-ref Bound Value Runner Or Same-frame Denominator Source",
            "**Status:** finite residual runner installed. It computes the no-cancellation absolute-sum residual for smoke rows, but refuses the live MTS rows because the same-frame denominator and component values are missing. No local-GR, Newton, PPN, or `Delta_ref` pass is claimed.",
            "**Private reading:** after 2458 demoted the current zero route, the denominator became the boss fight. The code now enforces that: no `M_H_ref`/`N_E`, no scoring. Orbital GM is explicitly rejected as circular.",
            "## Source Register\n" + table(["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"], sources),
            "## Denominator Source Gate\n" + table(["denominator_id", "quantity", "method", "value", "units", "equation_ref", "same_frame", "positive", "orbital_gm_import", "status", "valid_for_claim"], denominators),
            "## Bound Value Candidates\n" + table(["candidate_id", "quantity", "component_group", "value", "units", "denominator_id", "source_path", "equation_ref", "valid_for_claim"], values),
            "## No-cancellation Runner Results\n" + table(["result_id", "component_group", "denominator_id", "status", "component_sum_abs", "denominator_value", "Delta_ref_bound_over_denominator", "blockers", "claim_allowed"], results),
            "## Claim Gates\n" + table(["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"], gates),
            "## Decision Ledger\n" + table(["decision_id", "decision", "reason", "effect"], decisions),
            "## Next Target\n" + table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], next_rows),
            "## Branch Copies\n" + table(["copy_id", "source_path", "target_path", "source_exists", "target_exists"], branch_rows),
            "## Validation\n" + table(["check_id", "status", "notes", "detail"], validations),
        ]
    )
    DOC.write_text(doc + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    denominators = denominator_rows()
    values = bound_value_rows()
    results = run_no_cancellation(denominators, values)
    gates = claim_gate_rows(results)
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["denominator_gate"], denominators)
    write_csv(OUTPUTS["bound_values"], values)
    write_csv(OUTPUTS["runner_results"], results)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    validations = validation_rows(sources, denominators, values, results, gates, next_rows, branch_rows)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, denominators, values, results, gates, decisions, next_rows, branch_rows, validations)

    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
