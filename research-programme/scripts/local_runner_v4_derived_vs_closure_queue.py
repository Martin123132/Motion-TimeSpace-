from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-runner-v4-derived-vs-closure-queue"
CHECKPOINT_DOC = "406-local-runner-v4-derived-vs-closure-queue.md"
STATUS = "local_runner_v4_derived_vs_closure_queue_written_no_theorem_zero_rows_closure_conditional_retained_unscored_rows_separated_no_local_GR_pass"
CLAIM_CEILING = "local_runner_v4_state_queue_only_no_WEP_EH_Newton_PPN_flux_fifth_force_or_local_GR_pass"
NEXT_TARGET = "407-primitive-relational-quotient-action-sketch.md"


SOURCE_DOCS = [
    {
        "path": "397-local-bound-runner-v3-from-identity-stack.md",
        "role": "runner-v3 row/state matrix",
    },
    {
        "path": "400-runner-v3-numeric-smoke-extension.md",
        "role": "channel-level numeric smoke extension",
    },
    {
        "path": "401-parent-matter-selector-theorem-attempt.md",
        "role": "selector-blind matter theorem attempt and R0/R1/R2 transitions",
    },
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source transition decisions",
    },
    {
        "path": "403-boundary-domain-flux-nohair-numeric-contract.md",
        "role": "boundary/domain/flux hard-channel contract",
    },
    {
        "path": "404-selector-blind-matter-axiom-origin.md",
        "role": "primitive-origin audit and postulate options",
    },
    {
        "path": "405-same-frame-EH-source-derived-stack-audit.md",
        "role": "derived-vs-closure local-GR stack audit",
    },
    {
        "path": "runs/20260602-033500-local-bound-runner-v3-from-identity-stack/results/runner_v3_matrix.csv",
        "role": "machine-readable runner-v3 matrix",
    },
    {
        "path": "runs/20260602-041500-runner-v3-numeric-smoke-extension/results/aggregate_channel_bounds.csv",
        "role": "machine-readable tightest source-lock channel bounds",
    },
    {
        "path": "runs/20260602-050500-same-frame-EH-source-derived-stack-audit/results/local_GR_stack_rung_status.csv",
        "role": "machine-readable local-GR stack rung states",
    },
]


RUNNER_V4_STATE_DEFINITIONS = [
    {
        "runner_v4_state": "theorem_zero",
        "meaning": "parent action derives the row contribution is exactly zero or physically gauge/topological",
        "score_policy": "may be set to zero with theorem source path",
        "claim_policy": "eligible only if coupled rows are also closed",
    },
    {
        "runner_v4_state": "postulate_zero",
        "meaning": "zero by explicit new physical postulate, not yet derived",
        "score_policy": "evaluate only inside named postulate branch",
        "claim_policy": "no public derivation claim",
    },
    {
        "runner_v4_state": "closure_zero",
        "meaning": "zero by branch closure assumption or test condition",
        "score_policy": "evaluate only inside labelled closure branch",
        "claim_policy": "closure benchmark only",
    },
    {
        "runner_v4_state": "conditional_theorem",
        "meaning": "mathematical theorem works if extra premises are assumed",
        "score_policy": "emit premise list and fallback rows",
        "claim_policy": "not promoted until premises are parent-derived",
    },
    {
        "runner_v4_state": "retained_budget",
        "meaning": "numeric source lock exists but coefficient/no-hair theorem is missing",
        "score_policy": "evaluate residual against source lock when coefficient is supplied",
        "claim_policy": "budget is not a pass",
    },
    {
        "runner_v4_state": "retained_contingent_budget",
        "meaning": "numeric guardrail applies only if a channel exists",
        "score_policy": "score only after branch predicts the channel",
        "claim_policy": "no pass/fail without channel relevance theorem",
    },
    {
        "runner_v4_state": "retained_residual",
        "meaning": "operator/stress family remains explicitly in the modified-gravity ledger",
        "score_policy": "map to observables or keep symbolic",
        "claim_policy": "blocks local-GR promotion",
    },
    {
        "runner_v4_state": "unscored_parameterized",
        "meaning": "range/coupling/profile/source charge is missing",
        "score_policy": "retain force-law/profile contract without scalar score",
        "claim_policy": "no fifth-force pass",
    },
    {
        "runner_v4_state": "baseline_sanity",
        "meaning": "same evaluator checks a GR/null comparator",
        "score_policy": "pipeline sanity only",
        "claim_policy": "not MTS evidence",
    },
    {
        "runner_v4_state": "promotion_blocked",
        "meaning": "rollup row or stack gate cannot promote while dependencies remain non-derived",
        "score_policy": "report blockers",
        "claim_policy": "no local-GR claim",
    },
]


ROW_V4_MAP = [
    {
        "row_id": "R0_identity_coframe_direct",
        "runner_v4_state": "closure_zero",
        "zero_kind": "closure_zero_not_theorem_zero",
        "linked_stack_rungs": "G1_selector_blind_matter;G2_one_observed_coframe",
        "upgrade_condition": "derive selector-blind matter or primitive quotient/readout parent theorem",
        "score_policy": "closure branch may set residual to zero, but theorem_zero is forbidden",
        "claim_allowed": False,
    },
    {
        "row_id": "R1_WEP_source_charge",
        "runner_v4_state": "retained_contingent_budget",
        "zero_kind": "not_zero",
        "linked_stack_rungs": "G3_species_source_charge_universality;G7_source_normalized_measured_GM",
        "upgrade_condition": "derive species/source/bulk/boundary charge universality or theorem-zero channel absence",
        "score_policy": "score only if source-charge channel exists; retain 2.8e-15 guardrail",
        "claim_allowed": False,
    },
    {
        "row_id": "R2_clock_redshift",
        "runner_v4_state": "retained_budget",
        "zero_kind": "not_zero",
        "linked_stack_rungs": "G1_selector_blind_matter;G3_species_source_charge_universality;G7_source_normalized_measured_GM",
        "upgrade_condition": "derive selector-independent clock constants and no source/normalization drift",
        "score_policy": "score supplied clock/source drift coefficient against redshift source lock",
        "claim_allowed": False,
    },
    {
        "row_id": "R3_gamma",
        "runner_v4_state": "retained_budget",
        "zero_kind": "not_zero",
        "linked_stack_rungs": "G5_EH_operator_selection;G6_nonEH_operator_elimination;G8_boundary_bulk_radial_nohair;G9_domain_projector_nohair",
        "upgrade_condition": "derive EH-only same-frame exterior and no boundary/bulk/domain slip",
        "score_policy": "score non-EH/slip/hair coefficients against gamma source lock",
        "claim_allowed": False,
    },
    {
        "row_id": "R4_beta",
        "runner_v4_state": "retained_budget",
        "zero_kind": "not_zero",
        "linked_stack_rungs": "G7_source_normalized_measured_GM;G8_boundary_bulk_radial_nohair",
        "upgrade_condition": "derive constant measured GM and no nonlinear source/radial hair",
        "score_policy": "score beta/source hair coefficients against beta source lock",
        "claim_allowed": False,
    },
    {
        "row_id": "R5_alpha1",
        "runner_v4_state": "retained_budget",
        "zero_kind": "not_zero",
        "linked_stack_rungs": "G9_domain_projector_nohair",
        "upgrade_condition": "derive no boundary/domain/projector vector leakage",
        "score_policy": "score vector leakage coefficients against alpha1 source lock",
        "claim_allowed": False,
    },
    {
        "row_id": "R6_alpha2",
        "runner_v4_state": "retained_budget",
        "zero_kind": "not_zero",
        "linked_stack_rungs": "G9_domain_projector_nohair",
        "upgrade_condition": "derive no domain anisotropy or vector/projector leakage",
        "score_policy": "score vector/anisotropy coefficients against alpha2 source lock",
        "claim_allowed": False,
    },
    {
        "row_id": "R7_alpha3",
        "runner_v4_state": "retained_contingent_budget",
        "zero_kind": "not_zero",
        "linked_stack_rungs": "G10_Ward_flux_silence",
        "upgrade_condition": "derive exact Ward-owned flux silence or channel absence",
        "score_policy": "score only if flux/nonconservation channel exists; 4e-20 ceiling is not tunable evidence",
        "claim_allowed": False,
    },
    {
        "row_id": "R8_xi",
        "runner_v4_state": "retained_budget",
        "zero_kind": "not_zero",
        "linked_stack_rungs": "G9_domain_projector_nohair",
        "upgrade_condition": "derive no boundary/domain/topology preferred-location anisotropy",
        "score_policy": "score anisotropy coefficients against xi source lock",
        "claim_allowed": False,
    },
    {
        "row_id": "R9_Gdot",
        "runner_v4_state": "retained_contingent_budget",
        "zero_kind": "not_zero",
        "linked_stack_rungs": "G7_source_normalized_measured_GM;G10_Ward_flux_silence;G11_Gdot_drift_silence",
        "upgrade_condition": "derive no secular G_eff M_eff, memory, flux, or domain drift",
        "score_policy": "score only if drift channel exists; retain yr^-1 source lock",
        "claim_allowed": False,
    },
    {
        "row_id": "R10_fifth_force",
        "runner_v4_state": "unscored_parameterized",
        "zero_kind": "not_zero",
        "linked_stack_rungs": "G8_boundary_bulk_radial_nohair;G12_fifth_force_law_or_zero",
        "upgrade_condition": "derive theorem-zero finite-range channels or alpha(lambda), charges, range, screening",
        "score_policy": "do not scalar-score until alpha(lambda) profile exists",
        "claim_allowed": False,
    },
    {
        "row_id": "R11_EH_operator_ledger",
        "runner_v4_state": "retained_residual",
        "zero_kind": "not_zero",
        "linked_stack_rungs": "G5_EH_operator_selection;G6_nonEH_operator_elimination",
        "upgrade_condition": "derive metric-only local second-order same-frame exterior or retain each coefficient",
        "score_policy": "symbolic operator ledger; no EH pass",
        "claim_allowed": False,
    },
]


STATE_PROMOTION_RULES = [
    {
        "from_state": "closure_zero",
        "to_state": "theorem_zero",
        "allowed_only_if": "parent action derives zero without using branch closure",
    },
    {
        "from_state": "postulate_zero",
        "to_state": "theorem_zero",
        "allowed_only_if": "postulate is derived from primitive variational/configuration-space principle",
    },
    {
        "from_state": "conditional_theorem",
        "to_state": "theorem_zero",
        "allowed_only_if": "all theorem premises are parent-derived and coupled rows close",
    },
    {
        "from_state": "retained_budget",
        "to_state": "theorem_zero",
        "allowed_only_if": "coefficient map derives exact zero/no-hair, not merely small value",
    },
    {
        "from_state": "retained_contingent_budget",
        "to_state": "theorem_zero",
        "allowed_only_if": "channel absence or exact Ward cancellation is derived",
    },
    {
        "from_state": "unscored_parameterized",
        "to_state": "retained_budget",
        "allowed_only_if": "alpha(lambda), source/test charges, range, and screening profile are supplied",
    },
]


CLAIM_POLICY = [
    {
        "claim": "runner-v4 emitted",
        "allowed": True,
        "reason": "state separation is a tooling/discipline improvement",
    },
    {
        "claim": "GR/null baseline sanity",
        "allowed": True,
        "reason": "pipeline sanity only, not MTS proof",
    },
    {
        "claim": "MTS has theorem-zero WEP row",
        "allowed": False,
        "reason": "R0 is closure_zero and G1 is not parent-derived",
    },
    {
        "claim": "MTS has EH/Newton local reduction",
        "allowed": False,
        "reason": "EH/source rungs are conditional/retained",
    },
    {
        "claim": "MTS passes local PPN",
        "allowed": False,
        "reason": "all non-baseline local rows have claim_allowed=false",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Runner-v4 is now a state discipline layer, not a new physics pass. It maps every runner-v3 row into a derived-vs-closure-aware state. There are no theorem_zero rows. R0 is closure_zero, R1/R7/R9 are retained contingent budgets, R10 remains unscored parameterized, and R11 remains a retained operator ledger. This makes future local-bound tests safer: they can evaluate closure branches and retained residuals without accidentally promoting them to GR/Newton/PPN evidence.",
        "runner_v4_rows": 12,
        "theorem_zero_rows": 0,
        "closure_zero_rows": 1,
        "claim_allowed_rows": 0,
        "local_GR_claim_allowed": False,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "attempt a formal primitive relational quotient/readout parent action sketch",
        "pass_condition": "selector-blind matter/domain silence has a variational route or stays postulate-labelled",
    },
    {
        "priority": 2,
        "target": "408-local-bound-data-runner-v4-smoke.py",
        "task": "run local residual profiles with runner-v4 state labels",
        "pass_condition": "closure_zero, retained, contingent, and unscored rows are evaluated without false promotion",
    },
    {
        "priority": 3,
        "target": "409-runner-v4-red-team.md",
        "task": "red-team whether runner-v4 hides any closure as theorem or misses any coupled row",
        "pass_condition": "no state can promote without a theorem source and dependency closure",
    },
]


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
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        rows.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return rows


def runner_v3_rows() -> list[dict[str, Any]]:
    return read_csv(ROOT / "runs/20260602-033500-local-bound-runner-v3-from-identity-stack/results/runner_v3_matrix.csv")


def aggregate_bounds() -> list[dict[str, str]]:
    return read_csv(ROOT / "runs/20260602-041500-runner-v3-numeric-smoke-extension/results/aggregate_channel_bounds.csv")


def stack_rungs() -> list[dict[str, str]]:
    return read_csv(ROOT / "runs/20260602-050500-same-frame-EH-source-derived-stack-audit/results/local_GR_stack_rung_status.csv")


def runner_v4_matrix_rows() -> list[dict[str, Any]]:
    v3_by_row = {row["row_id"]: row for row in runner_v3_rows()}
    rows: list[dict[str, Any]] = []
    for mapping in ROW_V4_MAP:
        v3 = v3_by_row[mapping["row_id"]]
        rows.append(
            {
                "row_id": mapping["row_id"],
                "observable": v3["observable"],
                "runner_v3_state": v3["state"],
                "runner_v4_state": mapping["runner_v4_state"],
                "zero_kind": mapping["zero_kind"],
                "source_lock": v3["source_lock"],
                "source_lock_units": v3["source_lock_units"],
                "linked_stack_rungs": mapping["linked_stack_rungs"],
                "upgrade_condition": mapping["upgrade_condition"],
                "score_policy": mapping["score_policy"],
                "claim_allowed": mapping["claim_allowed"],
            }
        )
    return rows


def row_bound_pressure_rows() -> list[dict[str, Any]]:
    bounds = aggregate_bounds()
    rows: list[dict[str, Any]] = []
    for row in runner_v4_matrix_rows():
        linked = [
            bound for bound in bounds
            if bound["tightest_row"] == row["row_id"]
        ]
        if not linked:
            rows.append(
                {
                    "row_id": row["row_id"],
                    "observable": row["observable"],
                    "runner_v4_state": row["runner_v4_state"],
                    "tightest_channel": "unscored_or_symbolic",
                    "tightest_bound": row["source_lock"],
                    "bound_units": row["source_lock_units"],
                    "pressure_policy": row["score_policy"],
                }
            )
            continue
        tightest = min(linked, key=lambda item: float(item["tightest_solo_bound"]))
        rows.append(
            {
                "row_id": row["row_id"],
                "observable": row["observable"],
                "runner_v4_state": row["runner_v4_state"],
                "tightest_channel": tightest["channel"],
                "tightest_bound": tightest["tightest_solo_bound"],
                "bound_units": tightest["bound_units"],
                "pressure_policy": row["score_policy"],
            }
        )
    return rows


def stack_to_row_dependency_rows() -> list[dict[str, Any]]:
    rung_by_name = {row["rung"]: row for row in stack_rungs()}
    rows: list[dict[str, Any]] = []
    for row in runner_v4_matrix_rows():
        for rung in row["linked_stack_rungs"].split(";"):
            stack_row = rung_by_name.get(rung)
            rows.append(
                {
                    "row_id": row["row_id"],
                    "observable": row["observable"],
                    "runner_v4_state": row["runner_v4_state"],
                    "linked_stack_rung": rung,
                    "rung_current_status": stack_row["current_status"] if stack_row else "missing",
                    "rung_runner_v4_state": stack_row["runner_v4_state"] if stack_row else "missing",
                    "rung_blocks_promotion": stack_row["blocks_promotion"] if stack_row else "missing",
                }
            )
    return rows


def state_summary_rows() -> list[dict[str, Any]]:
    rows = runner_v4_matrix_rows()
    states = sorted({row["runner_v4_state"] for row in rows})
    summary = [
        {
            "runner_v4_state": state,
            "rows": sum(1 for row in rows if row["runner_v4_state"] == state),
            "claim_allowed_rows": sum(
                1
                for row in rows
                if row["runner_v4_state"] == state and str(row["claim_allowed"]) == "True"
            ),
        }
        for state in states
    ]
    summary.append(
        {
            "runner_v4_state": "theorem_zero",
            "rows": 0,
            "claim_allowed_rows": 0,
        }
    )
    return summary


def gate_rows(source_rows: list[dict[str, Any]], matrix_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    theorem_zero_rows = [row for row in matrix_rows if row["runner_v4_state"] == "theorem_zero"]
    closure_zero_rows = [row for row in matrix_rows if row["runner_v4_state"] == "closure_zero"]
    false_claim_rows = [row for row in matrix_rows if str(row["claim_allowed"]) == "True"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "runner_v4_states_defined",
            "status": "pass",
            "evidence": f"{len(RUNNER_V4_STATE_DEFINITIONS)} state definitions written",
        },
        {
            "gate": "runner_v4_matrix_written",
            "status": "pass" if len(matrix_rows) == 12 else "fail",
            "evidence": f"{len(matrix_rows)} runner rows emitted",
        },
        {
            "gate": "zero_kinds_separated",
            "status": "pass" if closure_zero_rows and not theorem_zero_rows else "fail",
            "evidence": f"{len(closure_zero_rows)} closure_zero rows and {len(theorem_zero_rows)} theorem_zero rows",
        },
        {
            "gate": "no_false_claim_rows",
            "status": "pass" if not false_claim_rows else "fail",
            "evidence": f"{len(false_claim_rows)} rows have claim_allowed=true",
        },
        {
            "gate": "promotion_rules_written",
            "status": "pass",
            "evidence": f"{len(STATE_PROMOTION_RULES)} state promotion rules written",
        },
        {
            "gate": "row_dependencies_written",
            "status": "pass",
            "evidence": f"{len(stack_to_row_dependency_rows())} row-rung dependencies written",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "runner-v4 is a state discipline layer, not a local-GR pass",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_checkpoint_markdown(
    run_dir: Path,
    matrix_rows: list[dict[str, Any]],
    summary_rows: list[dict[str, Any]],
    pressure_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, Any]],
) -> None:
    matrix_table_rows = [
        {
            "row": row["row_id"],
            "observable": row["observable"],
            "v4_state": row["runner_v4_state"],
            "zero_kind": row["zero_kind"],
        }
        for row in matrix_rows
    ]
    pressure_table_rows = [
        {
            "row": row["row_id"],
            "state": row["runner_v4_state"],
            "channel": row["tightest_channel"],
            "bound": row["tightest_bound"],
            "units": row["bound_units"],
        }
        for row in pressure_rows
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 406 - Local Runner v4 Derived-vs-Closure Queue

Private runner/state-discipline checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 405 said runner-v4 was ready. This checkpoint implements the state queue: no row may simply be called “zero.” It must be `theorem_zero`, `postulate_zero`, `closure_zero`, conditional, retained, contingent, or unscored.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/local_runner_v4_derived_vs_closure_queue.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Runner-v4 Matrix

{markdown_table(matrix_table_rows, ["row", "observable", "v4_state", "zero_kind"])}

## 4. State Summary

{markdown_table(summary_rows, ["runner_v4_state", "rows", "claim_allowed_rows"])}

## 5. Tightest Row Pressures

{markdown_table(pressure_table_rows, ["row", "state", "channel", "bound", "units"])}

## 6. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 7. Decision

{DECISION[0]["decision"]}

Practical read: this is exactly the anti-cheat layer we needed. A future data run can use the identity branch, but the machine will know it is a closure branch. No more accidentally giving closure the belt and calling it theorem-zero.

## 8. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    matrix_rows = runner_v4_matrix_rows()
    pressure_rows = row_bound_pressure_rows()
    summary_rows = state_summary_rows()
    gate_result_rows = gate_rows(source_rows, matrix_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "runner_v4_state_definitions.csv", RUNNER_V4_STATE_DEFINITIONS)
    write_csv(results_dir / "runner_v4_matrix.csv", matrix_rows)
    write_csv(results_dir / "state_summary.csv", summary_rows)
    write_csv(results_dir / "row_bound_pressure.csv", pressure_rows)
    write_csv(results_dir / "stack_to_row_dependencies.csv", stack_to_row_dependency_rows())
    write_csv(results_dir / "state_promotion_rules.csv", STATE_PROMOTION_RULES)
    write_csv(results_dir / "claim_policy.csv", CLAIM_POLICY)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    theorem_zero_rows = [row for row in matrix_rows if row["runner_v4_state"] == "theorem_zero"]
    closure_zero_rows = [row for row in matrix_rows if row["runner_v4_state"] == "closure_zero"]
    claim_allowed_rows = [row for row in matrix_rows if str(row["claim_allowed"]) == "True"]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "runner_v4_rows": len(matrix_rows),
        "theorem_zero_rows": len(theorem_zero_rows),
        "closure_zero_rows": len(closure_zero_rows),
        "claim_allowed_rows": len(claim_allowed_rows),
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, matrix_rows, summary_rows, pressure_rows, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 406 local runner-v4 derived-vs-closure queue artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
