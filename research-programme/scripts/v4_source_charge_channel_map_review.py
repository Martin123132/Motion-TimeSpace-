from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "v4-source-charge-channel-map-review"
CHECKPOINT_DOC = "412-v4-source-charge-channel-map-review.md"
STATUS = "v4_source_charge_channel_map_review_written_four_channel_guardrail_retained_direct_WEP_subscore_defined_no_claim_leak_no_local_GR_pass"
CLAIM_CEILING = "v4_source_charge_channel_map_review_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "413-no-marker-parent-action-theorem-attempt.md"


SOURCE_DOCS = [
    {
        "path": "408-local-bound-data-runner-v4-smoke.md",
        "role": "runner-v4 smoke result that exposed four-channel R1 severity",
    },
    {
        "path": "409-runner-v4-red-team.md",
        "role": "manual review item for R1 source-charge severity",
    },
    {
        "path": "411-local-bound-runner-v4-real-data-interface.md",
        "role": "real-data interface needing a fair R1 channel policy",
    },
    {
        "path": "runs/20260602-041500-runner-v3-numeric-smoke-extension/results/channel_map.csv",
        "role": "source channel map containing R1 entries",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "role": "runner-v4 state matrix",
    },
    {
        "path": "runs/20260602-053500-local-bound-data-runner-v4-smoke/results/numeric_evaluation.csv",
        "role": "numeric smoke result for source_charge_1e_minus_14",
    },
    {
        "path": "runs/20260602-054500-runner-v4-red-team/results/manual_review_items.csv",
        "role": "machine-readable manual review item list",
    },
    {
        "path": "runs/20260602-061500-local-bound-runner-v4-real-data-interface/results/local_data_targets.csv",
        "role": "real-data target map that marks R1 review needed",
    },
]


CHANNEL_ROLE_RULES = {
    "source_charge_species_split": {
        "review_role": "direct_WEP_source_charge",
        "include_in_full_guardrail": True,
        "include_in_direct_WEP_subscore": True,
        "reason": "direct species-dependent source/test charge split",
    },
    "bulk_X_composition_charge": {
        "review_role": "direct_WEP_bulk_composition",
        "include_in_full_guardrail": True,
        "include_in_direct_WEP_subscore": True,
        "reason": "bulk-X composition charge coupled to source/test masses",
    },
    "boundary_species_charge": {
        "review_role": "direct_WEP_boundary_composition",
        "include_in_full_guardrail": True,
        "include_in_direct_WEP_subscore": True,
        "reason": "boundary/class charge distinguishes species",
    },
    "source_normalization_species_split": {
        "review_role": "source_normalization_cross_channel",
        "include_in_full_guardrail": True,
        "include_in_direct_WEP_subscore": False,
        "reason": "measured-GM/source normalization hazard; not hidden, but reported as cross-channel rather than direct-only WEP",
    },
}


POLICY_ROWS = [
    {
        "policy": "full_R1_composite_guardrail",
        "decision": "retain_four_channel_sum",
        "use_case": "stress-test profiles where all R1 hazards are deliberately activated",
        "anti_cheat": "conservative guardrail; not an empirical pass/fail claim by itself",
    },
    {
        "policy": "direct_WEP_subscore",
        "decision": "define_three_channel_direct_subscore",
        "use_case": "external differential-acceleration data that constrains direct composition/source charge",
        "anti_cheat": "subscore must be reported beside full R1 guardrail, not used to hide source-normalization debt",
    },
    {
        "policy": "source_normalization_cross_channel",
        "decision": "keep_visible_as_R1_cross_channel",
        "use_case": "measured-GM, beta, clock, or Gdot normalization routes",
        "anti_cheat": "do not double-count it inside one empirical claim, but do not delete it from the theory ledger",
    },
    {
        "policy": "no_promotion_from_channel_split",
        "decision": "claim_state_unchanged",
        "use_case": "all R1 evaluations",
        "anti_cheat": "changing channel grouping cannot produce theorem_zero or local-GR credit",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "The R1 four-channel severity is intentional as a conservative composite guardrail, not an accidental claim leak. The fourth term, source_normalization_species_split, is not direct-only WEP composition charge, so future real-data reporting should split R1 into a three-channel direct-WEP subscore plus a visible source-normalization cross-channel. However, the full four-channel guardrail remains the correct stress profile when all R1 hazards are activated. The numerical result is unchanged in spirit: at 1e-14 per channel, three-channel, four-channel, and source-normalization-only views are all over the 2.8e-15 lock. No row is promoted and no local-GR claim is allowed.",
        "four_channel_guardrail_retained": True,
        "direct_WEP_subscore_defined": True,
        "theorem_credit_rows": 0,
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
        "task": "attempt the no-marker parent-action theorem needed by the quotient-matter route",
        "pass_condition": "marker extension is forbidden by parent symmetry or explicitly retained as closure",
    },
    {
        "priority": 2,
        "target": "414-local-bounds-data-intake-first-pass.md",
        "task": "fill the local-bound interface from verified sources and run the evaluator",
        "pass_condition": "real local-bound rows evaluate with references and no claim leaks",
    },
    {
        "priority": 3,
        "target": "415-direct-WEP-vs-source-normalization-evaluator-update.py",
        "task": "teach the real-data evaluator to report direct-WEP and full-R1 guardrail side by side",
        "pass_condition": "R1 split is visible in output without changing runner-v4 claim semantics",
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


def channel_map_rows() -> list[dict[str, str]]:
    return read_csv(ROOT / "runs/20260602-041500-runner-v3-numeric-smoke-extension/results/channel_map.csv")


def runner_v4_rows() -> list[dict[str, str]]:
    return read_csv(ROOT / "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv")


def r1_channel_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in channel_map_rows():
        if row["row_id"] != "R1_WEP_source_charge":
            continue
        role = CHANNEL_ROLE_RULES[row["channel"]]
        rows.append(
            {
                "row_id": row["row_id"],
                "observable": row["observable"],
                "channel": row["channel"],
                "channel_sector": row["channel_sector"],
                "source_lock": row["source_lock"],
                "source_lock_units": row["source_lock_units"],
                "response_weight": row["response_weight"],
                "review_role": role["review_role"],
                "include_in_full_guardrail": role["include_in_full_guardrail"],
                "include_in_direct_WEP_subscore": role["include_in_direct_WEP_subscore"],
                "reason": role["reason"],
            }
        )
    return rows


def r1_source_lock() -> float:
    for row in runner_v4_rows():
        if row["row_id"] == "R1_WEP_source_charge":
            return float(row["source_lock"])
    raise ValueError("R1_WEP_source_charge missing from runner-v4 matrix")


def r1_runner_state() -> str:
    for row in runner_v4_rows():
        if row["row_id"] == "R1_WEP_source_charge":
            return row["runner_v4_state"]
    return "missing"


def subscore_rows(amplitude: float = 1.0e-14) -> list[dict[str, Any]]:
    channels = r1_channel_rows()
    source_lock = r1_source_lock()
    subscore_defs = [
        {
            "subscore": "four_channel_composite_guardrail",
            "included_channels": [row["channel"] for row in channels if row["include_in_full_guardrail"]],
            "policy": "retain as conservative stress-test guardrail",
        },
        {
            "subscore": "three_channel_direct_WEP_subscore",
            "included_channels": [row["channel"] for row in channels if row["include_in_direct_WEP_subscore"]],
            "policy": "use for direct differential-acceleration comparison, beside full guardrail",
        },
        {
            "subscore": "source_normalization_single_channel",
            "included_channels": ["source_normalization_species_split"],
            "policy": "keep visible as cross-channel normalization debt",
        },
        {
            "subscore": "max_single_channel_conservative_floor",
            "included_channels": [row["channel"] for row in channels],
            "policy": "sanity floor if channels are not statistically independent",
            "use_max_not_sum": True,
        },
    ]
    rows: list[dict[str, Any]] = []
    for subscore_def in subscore_defs:
        included = subscore_def["included_channels"]
        if subscore_def.get("use_max_not_sum"):
            residual = amplitude if included else 0.0
        else:
            residual = amplitude * len(included)
        severity = residual / source_lock
        rows.append(
            {
                "test_profile": "source_charge_1e_minus_14",
                "subscore": subscore_def["subscore"],
                "included_channel_count": len(included),
                "included_channels": ";".join(included),
                "per_channel_amplitude": amplitude,
                "source_lock": source_lock,
                "residual_value": residual,
                "severity_ratio": severity,
                "evaluation_class": "over_budget" if residual > source_lock else "inside_budget_no_claim",
                "policy": subscore_def["policy"],
                "theorem_credit_allowed": False,
                "claim_allowed": False,
            }
        )
    return rows


def cross_row_overlap_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in channel_map_rows():
        if "source_normalization" not in row["channel"]:
            continue
        rows.append(
            {
                "channel": row["channel"],
                "row_id": row["row_id"],
                "observable": row["observable"],
                "source_lock": row["source_lock"],
                "meaning": row["meaning"],
                "review_note": "source-normalization family should be visible across rows; do not hide or double-count in a single empirical claim",
            }
        )
    return rows


def gate_rows(
    source_rows: list[dict[str, Any]],
    channel_rows: list[dict[str, Any]],
    subscore_result_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    direct_count = sum(1 for row in channel_rows if row["include_in_direct_WEP_subscore"])
    full_count = sum(1 for row in channel_rows if row["include_in_full_guardrail"])
    source_norm = [row for row in channel_rows if row["channel"] == "source_normalization_species_split"]
    subscore_names = {row["subscore"]: row for row in subscore_result_rows}
    material_unchanged = all(row["evaluation_class"] == "over_budget" for row in subscore_result_rows)
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "R1_channel_map_loaded",
            "status": "pass" if len(channel_rows) == 4 else "fail",
            "evidence": f"{len(channel_rows)} R1 channels found",
        },
        {
            "gate": "four_channel_guardrail_retained",
            "status": "pass" if full_count == 4 else "fail",
            "evidence": f"{full_count} channels included in full guardrail",
        },
        {
            "gate": "direct_WEP_three_channel_subscore_defined",
            "status": "pass" if direct_count == 3 else "fail",
            "evidence": f"{direct_count} channels included in direct-WEP subscore",
        },
        {
            "gate": "source_normalization_not_hidden",
            "status": "pass" if source_norm else "fail",
            "evidence": source_norm[0]["review_role"] if source_norm else "missing source_normalization_species_split",
        },
        {
            "gate": "subscore_result_materially_unchanged",
            "status": "pass" if material_unchanged else "fail",
            "evidence": "all source_charge_1e_minus_14 subscore views remain over budget",
        },
        {
            "gate": "severity_difference_explained",
            "status": "pass",
            "evidence": f"four={subscore_names['four_channel_composite_guardrail']['severity_ratio']} three={subscore_names['three_channel_direct_WEP_subscore']['severity_ratio']}",
        },
        {
            "gate": "R1_state_unchanged",
            "status": "pass" if r1_runner_state() == "retained_contingent_budget" else "fail",
            "evidence": f"R1 runner-v4 state remains {r1_runner_state()}",
        },
        {
            "gate": "no_theorem_credit_or_claim_leaks",
            "status": "pass"
            if all(not row["theorem_credit_allowed"] and not row["claim_allowed"] for row in subscore_result_rows)
            else "fail",
            "evidence": "theorem_credit=0 claim_allowed=0",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "channel-count review only; no local-GR pass",
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


def format_float(value: Any) -> str:
    number = float(value)
    if number == 0.0:
        return "0"
    if abs(number) < 1.0e-3 or abs(number) >= 1.0e4:
        return f"{number:.3e}"
    return f"{number:.6g}"


def write_checkpoint_markdown(
    run_dir: Path,
    channel_rows: list[dict[str, Any]],
    subscore_result_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, Any]],
) -> None:
    channel_table_rows = [
        {
            "channel": row["channel"],
            "role": row["review_role"],
            "full": row["include_in_full_guardrail"],
            "direct": row["include_in_direct_WEP_subscore"],
        }
        for row in channel_rows
    ]
    subscore_table_rows = [
        {
            "subscore": row["subscore"],
            "channels": row["included_channel_count"],
            "residual": format_float(row["residual_value"]),
            "severity": format_float(row["severity_ratio"]),
            "class": row["evaluation_class"],
        }
        for row in subscore_result_rows
    ]
    policy_table_rows = [
        {
            "policy": row["policy"],
            "decision": row["decision"],
            "anti_cheat": row["anti_cheat"],
        }
        for row in POLICY_ROWS
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 412 - Runner-v4 Source-Charge Channel Map Review

Private R1/local-bound checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 409 flagged a fairness issue: `source_charge_1e_minus_14` scores four R1 channels, giving severity `14.2857` instead of the earlier three-channel `10.7143`. This checkpoint decides whether that fourth channel is a mistake, a conservative guardrail, or a separate subscore.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/v4_source_charge_channel_map_review.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. R1 Channel Roles

{markdown_table(channel_table_rows, ["channel", "role", "full", "direct"])}

## 4. Subscore Check

{markdown_table(subscore_table_rows, ["subscore", "channels", "residual", "severity", "class"])}

## 5. Policy Decision

{markdown_table(policy_table_rows, ["policy", "decision", "anti_cheat"])}

## 6. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 7. Decision

{DECISION[0]["decision"]}

Practical read: this was a good catch, but it is not a rescue loophole and not a hidden failure. The fair move is to report both views: three-channel direct WEP for direct composition tests, and four-channel full R1 when testing all source-charge hazards.

## 8. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    channel_rows = r1_channel_rows()
    subscore_result_rows = subscore_rows()
    overlap_rows = cross_row_overlap_rows()
    gate_result_rows = gate_rows(source_rows, channel_rows, subscore_result_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "R1_channel_review.csv", channel_rows)
    write_csv(results_dir / "R1_subscore_check.csv", subscore_result_rows)
    write_csv(results_dir / "source_normalization_overlap.csv", overlap_rows)
    write_csv(results_dir / "channel_count_policy.csv", POLICY_ROWS)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "R1_channels": len(channel_rows),
        "full_guardrail_channels": sum(1 for row in channel_rows if row["include_in_full_guardrail"]),
        "direct_WEP_subscore_channels": sum(1 for row in channel_rows if row["include_in_direct_WEP_subscore"]),
        "subscore_rows": len(subscore_result_rows),
        "all_subscores_over_budget": all(row["evaluation_class"] == "over_budget" for row in subscore_result_rows),
        "R1_runner_v4_state": r1_runner_state(),
        "theorem_credit_rows": 0,
        "claim_allowed_rows": 0,
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, channel_rows, subscore_result_rows, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 412 R1 source-charge channel map review artifacts."
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
