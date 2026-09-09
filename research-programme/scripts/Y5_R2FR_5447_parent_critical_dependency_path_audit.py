from __future__ import annotations

import csv
import ctypes
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from typing import Any


os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

POST = Path(__file__).resolve().parents[1]
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5447"
FORMALIZATION = POST.parent / "formalization-workbench"

SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
DOC_5336 = POST / "5336-Y5-R2FR-fold-pair-equivalence-and-incremental-ownership-gate.md"
DOC_5344 = POST / "5344-Y5-R2FR-closed-parent-local-vacuum-attractor-no-go-and-minimal-reduced-dynamics-contract.md"
DOC_5393 = POST / "5393-Y5-R2FR-D4-parent-frozen-mapped-away-atlas-and-W3-owner-decomposition.md"
OWNER_5393 = FUNCTIONAL_RG / "5393" / "D4_W3_owner_decomposition.csv"
RESULT_5391 = FUNCTIONAL_RG / "5391" / "D4_uniform_full_H3_result.json"
RESULT_5392 = FUNCTIONAL_RG / "5392" / "D4_endpoint_G3_result.json"
RESULT_5395 = FUNCTIONAL_RG / "5395" / "D4_correlated_material_residue_result.json"
RESULT_5446 = FUNCTIONAL_RG / "5446" / "SX007_TOP_additional_progress_and_priority_result.json"

DOCUMENT = POST / "5447-Y5-R2FR-parent-critical-dependency-path-audit-and-D4-owner-preemption.md"
MATRIX = OUTPUT / "parent_critical_dependency_matrix.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5447_VALIDATION.csv"
RESULT = OUTPUT / "parent_critical_dependency_path_result.json"

CHECKPOINT = 5447
REVISION = "parent-critical-dependency-path-v1"


def set_below_normal_priority() -> None:
    try:
        ctypes.windll.kernel32.SetPriorityClass(
            ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000
        )
    except (AttributeError, OSError):
        pass


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    fields = list(rows[0])
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def source_rows() -> list[dict[str, Any]]:
    rows = []
    for path in (
        SPINE,
        DOC_5336,
        DOC_5344,
        DOC_5393,
        OWNER_5393,
        RESULT_5391,
        RESULT_5392,
        RESULT_5395,
        RESULT_5446,
    ):
        rows.append(
            {
                "source_path": str(path.relative_to(POST)),
                "source_exists": path.is_file(),
            }
        )
    return rows


def dependency_rows() -> list[dict[str, Any]]:
    return [
        {
            "layer": "L0_TWO_DERIVATIVE_LOCAL_LIMIT",
            "required_result": "one parent metric residue gives Einstein, Newton, geodesic/PPN and Maxwell stress/Poynting",
            "status": "DERIVED_ON_SELECTED_SILENT_BRANCH",
            "D4_regular_away_required": False,
            "independent_open_owner": "rho_local=rho_0 preparation remains boundary/state data",
            "source_paths": "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md|5344-Y5-R2FR-closed-parent-local-vacuum-attractor-no-go-and-minimal-reduced-dynamics-contract.md",
            "next_action": "preserve exact scoped claim; do not reopen source-coupling inventory",
            "valid_for_full_MTS_claim": False,
        },
        {
            "layer": "L1_LOCAL_STATE_PREPARATION",
            "required_result": "derive rho_local=rho_0 as an attractor from the parent",
            "status": "CLOSED_UNITARY_ATTRACTOR_NO_GO__BOUNDARY_STATE_RETAINED",
            "D4_regular_away_required": False,
            "independent_open_owner": "a reduced open-system history would need a parent-derived retarded/noise kernel",
            "source_paths": "5344-Y5-R2FR-closed-parent-local-vacuum-attractor-no-go-and-minimal-reduced-dynamics-contract.md",
            "next_action": "keep closure explicit unless a genuinely new parent reduced dynamics is derived",
            "valid_for_full_MTS_claim": False,
        },
        {
            "layer": "L2_FIRST_MTS_P8_MATCHED_EXCESS",
            "required_result": "finite M_D4=max(H3,G3+W3)/6 and regulator-zero coefficient",
            "status": "IN_PROGRESS",
            "D4_regular_away_required": True,
            "independent_open_owner": "W_EVENT_LOCAL_REMAINDER is untouched even if all 240 regular paths finish",
            "source_paths": "5393-Y5-R2FR-D4-parent-frozen-mapped-away-atlas-and-W3-owner-decomposition.md|source-intake/functional_rg/5393/D4_W3_owner_decomposition.csv",
            "next_action": "derive and interval-enclose the event-local remainder before further long regular-away enumeration",
            "valid_for_full_MTS_claim": False,
        },
        {
            "layer": "L3_GALAXY_STATE_FROM_PARENT_HESSIAN",
            "required_result": "derive occupation, source/stress and phase-flow rather than import q",
            "status": "OPEN__FOLD_CARRIER_DERIVED_BUT_Q_AND_PREPARATION_NOT_SELECTED",
            "D4_regular_away_required": False,
            "independent_open_owner": "parent state preparation and nonlinear occupied-state closure",
            "source_paths": "5336-Y5-R2FR-fold-pair-equivalence-and-incremental-ownership-gate.md|LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md",
            "next_action": "return only after the finite D4 owner test or a new parent state mechanism",
            "valid_for_full_MTS_claim": False,
        },
        {
            "layer": "L4_ABSOLUTE_COUPLING_NORMALIZATIONS",
            "required_result": "numerical G_N and visible U1 charge from motion alone",
            "status": "CALIBRATIONS__NOT_CURRENT_PREDICTIONS",
            "D4_regular_away_required": False,
            "independent_open_owner": "microscopic normalization/representation principle",
            "source_paths": "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md",
            "next_action": "count once as calibrated constants; do not disguise them as derived",
            "valid_for_full_MTS_claim": False,
        },
    ]


def render_document(payload: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    lines = [
        "# 5447: Parent critical-dependency path audit and D4 owner preemption",
        "",
        "## Decision",
        "",
        "**KEEP THE 5396 REGULAR-AWAY STATE RESUME-SAFE; PREEMPT FURTHER BRUTE ENUMERATION WITH THE INDEPENDENT EVENT-LOCAL W3 OWNER.**",
        "",
        "The audit separates the already-derived leading local branch from the higher-order MTS matching problem. The selected two-derivative branch already gives Einstein response, Newtonian gravity, geodesic/PPN behaviour and Maxwell/Lorentz/Hilbert/Poynting structure from one action and one metric residue. D4 is not a prerequisite for that reduction.",
        "",
        "D4 is instead the first complete MTS-specific `p8` matched-excess calculation. It remains important, but the current `31/240` regular contour jobs are only one of three `W3` owners. The pole primitive is complete, the regular-away owner is partial, and `W_EVENT_LOCAL_REMAINDER` has not been enclosed. Finishing the other `209` regular jobs first would therefore spend the longest numerical leg without testing the independent analytic leg that can still block combined `W3`.",
        "",
        "## Dependency matrix",
        "",
        "| layer | status | D4 regular-away required | immediate action |",
        "|---|---|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['layer']}` | `{row['status']}` | `{str(row['D4_regular_away_required']).lower()}` | {row['next_action']} |"
        )
    lines.extend(
        [
            "",
            "## D4 owner state",
            "",
            f"- `H3`: certified (`{payload['H3_box_count']}` boxes);",
            f"- `G3`: certified (`{payload['G3_box_count']}` desingularized boxes);",
            "- away pole primitive: certified numeric bound;",
            f"- away regular contour: `{payload['completed_regular_path_jobs']}/{payload['total_regular_path_jobs']}` complete, saved resume-safe;",
            "- event-local analytic remainder: open and independent;",
            "- combined `W3`, regulator-zero D4 coefficient, all-operator local GR and full MTS: not claimed.",
            "",
            "## Next derivation",
            "",
            "Use the checkpoint-5392 `v=epsilon h` atlas to construct, event by event,",
            "",
            "```text",
            "R_e(epsilon)=I_tube,e(epsilon)-H_e(epsilon) Log(epsilon/epsilon_ref)-G_e(epsilon).",
            "```",
            "",
            "First prove that `R_e` is single-valued and analytic on the common complex regulator strip after the collision primitive is subtracted. Then build a finite interval/Cauchy bound for `sup |R_e'''|`. A failed analyticity or finite-bound gate is a genuine D4 obstruction; a pass completes the missing owner and makes resuming the 5396 atlas worthwhile.",
            "",
            "## Claim boundary",
            "",
            "This checkpoint changes scheduling, not physics claims. The exact two-derivative local branch remains scoped and retained. No event-local `W3`, combined `W3`, regulator limit, all-operator local-GR or full-MTS claim is made.",
            "",
        ]
    )
    atomic_text(DOCUMENT, "\n".join(lines))


def run() -> dict[str, Any]:
    set_below_normal_priority()
    started = datetime.now(timezone.utc)
    sources = source_rows()
    rows = dependency_rows()
    spine_text = SPINE.read_text(encoding="utf-8")
    fold_text = DOC_5336.read_text(encoding="utf-8")
    state_text = DOC_5344.read_text(encoding="utf-8")
    owners = {row["owner_id"]: row for row in read_csv(OWNER_5393)}
    h3 = read_json(RESULT_5391)
    g3 = read_json(RESULT_5392)
    pole = read_json(RESULT_5395)
    progress = read_json(RESULT_5446)

    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": "PREEMPT_REGULAR_AWAY_BRUTE_ENUMERATION_WITH_EVENT_LOCAL_OWNER",
        "H3_box_count": int(h3["box_bound_count"]),
        "G3_box_count": int(g3["certified_ratio_box_count"]),
        "pole_primitive_complete": bool(pole["numeric_pole_primitive_W3_complete"]),
        "completed_regular_path_jobs": int(progress["completed_path_jobs"]),
        "total_regular_path_jobs": int(progress["total_path_jobs"]),
        "regular_state_resume_safe": bool(progress["runner_resume_safe"]),
        "event_local_owner_status": owners["W_EVENT_LOCAL_REMAINDER"]["third_derivative_status"],
        "next_target": "D4_EVENT_LOCAL_REMAINDER_ANALYTICITY_AND_FINITE_CAUCHY_BOUND",
        "valid_for_two_derivative_local_GR_dependency_audit": True,
        "valid_for_D4_critical_path_preemption": True,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_D4_numeric_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }

    validations = [
        check("all_cited_sources_exist", all(row["source_exists"] for row in sources), sources),
        check(
            "two_derivative_local_branch_is_explicitly_derived",
            "exact nonlinear two-derivative local GR branch   = yes" in spine_text
            and "Einstein -> Newton/geodesic/PPN chain             = derived" in spine_text
            and "metric Maxwell/Lorentz/stress/Poynting chain      = derived" in spine_text,
            "spine lines 110-112",
        ),
        check(
            "state_preparation_is_not_silently_promoted",
            "unconditional parent preparation theorem              = not claimed" in state_text,
            "checkpoint 5344 claim boundary",
        ),
        check(
            "fold_route_does_not_select_q",
            "history source derives state preparation              = false" in fold_text
            and "galaxy or full-MTS claim                               = false" in fold_text,
            "checkpoint 5336 decision",
        ),
        check("H3_is_certified", h3.get("validation_passed") is True, h3.get("decision")),
        check("G3_is_certified", g3.get("validation_passed") is True, g3.get("decision")),
        check(
            "pole_primitive_is_certified",
            pole.get("validation_passed") is True
            and pole.get("numeric_pole_primitive_W3_complete") is True,
            pole.get("decision"),
        ),
        check(
            "regular_away_state_is_incomplete_and_resume_safe",
            progress.get("runner_resume_safe") is True
            and int(progress["completed_path_jobs"]) < int(progress["total_path_jobs"]),
            f"{progress['completed_path_jobs']}/{progress['total_path_jobs']}",
        ),
        check(
            "event_local_owner_is_independently_open",
            owners["W_EVENT_LOCAL_REMAINDER"]["third_derivative_status"]
            == "DESINGULARIZED_COORDINATES_EXIST__REMAINDER_ENCLOSURE_PENDING",
            owners["W_EVENT_LOCAL_REMAINDER"]["next_action"],
        ),
        check(
            "all_broad_claims_remain_false",
            not any(
                payload[key]
                for key in (
                    "valid_for_D4_event_local_W3_bound",
                    "valid_for_D4_numeric_W3_bound",
                    "valid_for_all_operator_local_GR_claim",
                    "valid_for_full_MTS_claim",
                )
            ),
            "event-local and combined W3 remain open",
        ),
    ]

    formalization_touches = [
        path
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
        and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > started
    ]
    validations.append(
        check(
            "formalization_workbench_untouched",
            not formalization_touches,
            f"modified_file_count={len(formalization_touches)}",
        )
    )
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(not row["passed"] for row in validations)
    atomic_csv(OUTPUT / "source_register.csv", sources)
    atomic_csv(MATRIX, rows)
    atomic_csv(VALIDATION, validations)
    render_document(payload, rows)
    atomic_json(RESULT, payload)
    return payload


def main() -> int:
    payload = run()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
