from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_R10_KERNEL_AND_CMETRIC_SOURCE_MAP_OR_BLOCKER_2476"
CHECKPOINT_ID = "2476"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2476-Y5-R2FR-R10-kernel-and-Cmetric-source-map-or-blocker.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R10_KERNEL_CMETRIC_2476_SOURCE_REGISTER.csv",
    "derivation_audit": OUT / "P8_Y5_R10_KERNEL_CMETRIC_2476_DERIVATION_AUDIT.csv",
    "blocker_ledger": OUT / "P8_Y5_R10_KERNEL_CMETRIC_2476_BLOCKER_LEDGER.csv",
    "conditional_maps": OUT / "P8_Y5_R10_KERNEL_CMETRIC_2476_CONDITIONAL_MAP_ROWS.csv",
    "claim_gates": OUT / "P8_Y5_R10_KERNEL_CMETRIC_2476_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R10_KERNEL_CMETRIC_2476_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R10_KERNEL_CMETRIC_2476_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_R10_KERNEL_CMETRIC_2476_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2476_VALIDATION.csv",
}

COPY_TARGETS = {
    "conditional_maps": LOCAL_BOUNDS / "R10_kernel_Cmetric_source_map_2476_NONCLAIM.csv",
    "blocker_ledger": LOCAL_BOUNDS / "R10_kernel_Cmetric_blocker_ledger_2476_NONCLAIM.csv",
    "acquisition_queue": QUEUE / "JR2476_WEAK_FIELD_METRIC_RESPONSE_THEOREM_OR_BLOCKER.csv",
}

SOURCES = [
    {
        "source_id": "SRC2476_00_2475_doc",
        "source_path": ROOT / "2475-Y5-R2FR-first-real-local-arena-coefficient-source-acquisition.md",
        "needles": ["NEXT2475_0_selected", "MISSING_C_METRIC", "MISSING_K_R10", "VAL2475_OVERALL"],
        "role": "handoff selecting R10 K_R10/C_metric source-map gate",
    },
    {
        "source_id": "SRC2476_01_2473_doc",
        "source_path": ROOT / "2473-Y5-R2FR-GK-stress-bound-local-arena-projection-runner.md",
        "needles": ["alpha_GK(lambda)=K_R10(lambda)*E_GK_bound", "C_metric", "MISS2473_6_Karena"],
        "role": "stress-bound runner schema and missing kernel ledger",
    },
    {
        "source_id": "SRC2476_02_2475_bounds",
        "source_path": OUT / "P8_Y5_GK_BOUND_SOURCE_2475_CANDIDATE_BOUND_ROWS.csv",
        "needles": ["BOUND2475_R10_ANCHOR_ALPHA1_38P6UM", "3.86e-05", "anchor_only_non_curve"],
        "role": "R10 external bound side, nonclaim anchor/review rows",
    },
    {
        "source_id": "SRC2476_03_2475_runner_inputs",
        "source_path": OUT / "P8_Y5_GK_BOUND_SOURCE_2475_RUNNER_INPUT_CANDIDATES.csv",
        "needles": ["RUN2475_R10_ANCHOR_INPUT", "MISSING_C_METRIC", "MISSING_K_R10"],
        "role": "runner rows showing missing MTS-side coefficients",
    },
    {
        "source_id": "SRC2476_04_2475_validation",
        "source_path": OUT / "P8_Y5_BRR545_2475_VALIDATION.csv",
        "needles": ["VAL2475_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as exc:  # pragma: no cover - diagnostic path
        return False, 0, str(exc)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                }
            )
        )
    return rows


def derivation_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "derivation_id": "DER2476_0_external_yukawa_observable",
            "object": "R10 alpha(lambda) observable",
            "candidate_relation": "Delta V=-G*m1*m2*alpha*exp(-r/lambda)/r; point-force ratio Delta F/F_N=alpha*(1+r/lambda)*exp(-r/lambda)",
            "status": "KNOWN_BACKGROUND_NOT_MTS_KERNEL",
            "why_it_matters": "This identifies what alpha means, but it is not the Eot-Wash extended-apparatus response kernel.",
            "blocking_input": "MISSING_R10_APPARATUS_CONVOLUTION",
            "claim_allowed": False,
        },
        {
            "derivation_id": "DER2476_1_external_bound_side",
            "object": "alpha_bound(lambda)",
            "candidate_relation": "2475 supplies alpha=1 at lambda=38.6 micrometers as a source-backed threshold anchor, plus a review-candidate curve.",
            "status": "PARTIAL_BOUND_SIDE_ONLY",
            "why_it_matters": "The experimental side is no longer empty, but the anchor alone cannot replace a full bound curve.",
            "blocking_input": "ANCHOR_ONLY_NONCURVE;REVIEW_CURVE_NOT_CLAIM_READY",
            "claim_allowed": False,
        },
        {
            "derivation_id": "DER2476_2_parent_metric_response",
            "object": "C_metric",
            "candidate_relation": "||delta g||_obs <= C_metric * E_GK_bound",
            "status": "BLOCKED_PARENT_WEAK_FIELD_RESPONSE",
            "why_it_matters": "A stress norm only becomes a local observable after the parent action gives a signed weak-field metric equation.",
            "blocking_input": "MISSING_PARENT_LINEARIZED_METRIC_OPERATOR",
            "claim_allowed": False,
        },
        {
            "derivation_id": "DER2476_3_r10_kernel",
            "object": "K_R10(lambda)",
            "candidate_relation": "alpha_pred(lambda)=K_R10(lambda)*C_metric*E_GK_bound",
            "status": "BLOCKED_NO_ARENA_KERNEL",
            "why_it_matters": "The short-range torsion-balance observable is an apparatus-weighted force/torque residual, not a naked point-particle potential.",
            "blocking_input": "MISSING_R10_GEOMETRY_KERNEL",
            "claim_allowed": False,
        },
        {
            "derivation_id": "DER2476_4_circular_GR_response_check",
            "object": "no circular GR assumption",
            "candidate_relation": "Do not set the metric Green function equal to the GR/Einstein-Poisson response unless that response has already been derived from the parent MTS action.",
            "status": "FORBIDDEN_AS_PROOF",
            "why_it_matters": "Using local GR to prove local GR would make the R10 pass circular.",
            "blocking_input": "DERIVE_NOT_ASSUME_LOCAL_GR_GREEN_FUNCTION",
            "claim_allowed": False,
        },
        {
            "derivation_id": "DER2476_5_units_and_norm_contract",
            "object": "dimensionless alpha bridge",
            "candidate_relation": "E_GK_bound -> metric residual -> force/torque residual -> alpha_pred(lambda), with units carried at every arrow.",
            "status": "CONTRACT_WRITTEN_NOT_CLOSED",
            "why_it_matters": "This is the exact bridge future work must close before any local bound comparison is meaningful.",
            "blocking_input": "MISSING_E_GK_NUMERIC_BOUND;MISSING_SOURCE_NORMALIZATION",
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def blocker_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "blocker_id": "BLOCK2476_0_KR10",
            "missing_object": "K_R10(lambda)",
            "blocked_claim": "R10 alpha prediction",
            "required_evidence": "source-backed or derived Eot-Wash geometry response converting a metric/force residual into alpha(lambda)",
            "current_evidence": "external alpha bound anchor exists; apparatus projection from MTS residual does not",
            "status": "BLOCKED",
            "next_action": "derive or source R10 geometry kernel only after parent metric response is specified",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLOCK2476_1_Cmetric",
            "missing_object": "C_metric",
            "blocked_claim": "stress residual to local metric residual",
            "required_evidence": "parent weak-field metric operator, gauge choice, boundary conditions, norm inequality, and sign/positivity control",
            "current_evidence": "2473 schema names C_metric but no numeric or derived coefficient exists",
            "status": "BLOCKED",
            "next_action": "attempt parent weak-field metric-response theorem",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLOCK2476_2_EGK",
            "missing_object": "E_GK_bound",
            "blocked_claim": "numeric local residual",
            "required_evidence": "sourced coefficients for boundary flux, source tail, negative-mode defect, topology hair, and projector leak",
            "current_evidence": "stress-bound branch remains symbolic",
            "status": "BLOCKED",
            "next_action": "keep E_GK rows nonclaim until parent coefficients are signed or bounded",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLOCK2476_3_bound_curve",
            "missing_object": "claim-ready alpha_bound(lambda) curve",
            "blocked_claim": "broad R10 comparison over lambda",
            "required_evidence": "official supplemental table or human-reviewed digitization with uncertainty and provenance",
            "current_evidence": "source-backed alpha=1 threshold anchor and review-candidate curve only",
            "status": "BLOCKED_FOR_FULL_CURVE",
            "next_action": "do not promote review candidate to live claim file",
            "valid_for_claim": False,
        },
        {
            "blocker_id": "BLOCK2476_4_no_GR_shortcut",
            "missing_object": "non-circular local weak-field response",
            "blocked_claim": "derived local GR/Newton limit",
            "required_evidence": "derive the weak-field Poisson/metric response from MTS parent action, not from assumed GR",
            "current_evidence": "borrowing GR response would be circular",
            "status": "GUARDRAIL_ACTIVE",
            "next_action": "move the next checkpoint one rung upstream to the parent metric equation",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def conditional_map_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "map_id": "MAP2476_0_formal_runner_schema",
            "arena": "R10_short_range",
            "relation": "alpha_pred(lambda)=K_R10(lambda)*C_metric*E_GK_bound",
            "input_status": "MISSING_K_R10;MISSING_C_METRIC;MISSING_E_GK_BOUND",
            "units_status": "dimensionless_output_if_inputs_are_normalized",
            "source_path": str(ROOT / "2473-Y5-R2FR-GK-stress-bound-local-arena-projection-runner.md"),
            "valid_for_claim": False,
            "notes": "This is the correct runner shape, not a closed physical prediction.",
        },
        {
            "map_id": "MAP2476_1_point_yukawa_background",
            "arena": "R10_short_range",
            "relation": "Delta F/F_N=alpha*(1+r/lambda)*exp(-r/lambda) for ideal point masses",
            "input_status": "BACKGROUND_ONLY",
            "units_status": "dimensionless",
            "source_path": "standard Yukawa-potential definition; not a live MTS source row",
            "valid_for_claim": False,
            "notes": "Useful sanity algebra, but too weak for Eot-Wash apparatus comparison.",
        },
        {
            "map_id": "MAP2476_2_parent_weak_field_contract",
            "arena": "local_metric_response",
            "relation": "Parent action -> linearized metric operator L_MTS[delta g]=S_GK[T_GK,J_M,boundary] -> Green bound C_metric",
            "input_status": "PARENT_THEOREM_REQUIRED",
            "units_status": "not_yet_closed",
            "source_path": "future 2477 target",
            "valid_for_claim": False,
            "notes": "This is the non-circular route that can actually help derive GR/Newton.",
        },
        {
            "map_id": "MAP2476_3_2475_anchor_runner_row",
            "arena": "R10_short_range",
            "relation": "RUN2475_R10_ANCHOR_INPUT uses alpha_bound=1 at lambda=3.86e-05 m but has blank MTS-side coefficients",
            "input_status": "RUNNER_BLOCKED",
            "units_status": "bound units ok; prediction units absent",
            "source_path": str(OUT / "P8_Y5_GK_BOUND_SOURCE_2475_RUNNER_INPUT_CANDIDATES.csv"),
            "valid_for_claim": False,
            "notes": "The external bound row is real; the MTS prediction side is not yet real.",
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2476_0_external_bound_anchor",
            "claim": "R10 source-backed alpha=1 threshold anchor exists.",
            "gate_status": "PASS_SOURCE_ONLY",
            "reason": "2475 recorded the 38.6 micrometer alpha=1 threshold with PubMed/arXiv/DOI provenance.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2476_1_KR10",
            "claim": "K_R10(lambda) is sourced or derived.",
            "gate_status": "BLOCKED",
            "reason": "No apparatus-weighted kernel from MTS metric/stress residual to alpha(lambda) is available.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2476_2_Cmetric",
            "claim": "C_metric maps GK stress to local metric response.",
            "gate_status": "BLOCKED",
            "reason": "Parent weak-field metric operator and norm theorem are missing.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2476_3_EGK",
            "claim": "E_GK_bound is numeric and sourced.",
            "gate_status": "BLOCKED",
            "reason": "Stress-bound coefficients remain symbolic.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2476_4_no_circular_GR",
            "claim": "No GR/Einstein response is assumed to prove local GR.",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "2476 explicitly rejects using GR Green functions as proof of local GR.",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2476_5_R10_claim",
            "claim": "MTS passes R10/local inverse-square test.",
            "gate_status": "BLOCKED",
            "reason": "External bound exists but the MTS prediction map is not closed.",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2476_6_local_GR_Newton",
            "claim": "MTS derives local GR/Newton limit.",
            "gate_status": "BLOCKED",
            "reason": "Need parent weak-field metric-response theorem before local-limit claim.",
            "gate_pass": False,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2476_0_no_R10_claim",
            "decision": "Do not promote the 2475 R10 anchor into a local-test claim.",
            "reason": "The source-backed bound side is real, but the MTS-side kernel and metric response are missing.",
            "effect": "R10 stays nonclaim and private.",
        },
        {
            "decision_id": "DEC2476_1_do_not_borrow_GR",
            "decision": "Reject the shortcut C_metric=GR weak-field response as a proof step.",
            "reason": "That would assume the local GR/Newton reduction we are trying to derive.",
            "effect": "The next derivation target moves upstream to the parent metric equation.",
        },
        {
            "decision_id": "DEC2476_2_select_2477",
            "decision": "Select parent weak-field metric-response theorem or no-go as next target.",
            "reason": "Without C_metric, every local arena kernel is floating.",
            "effect": "2477 should derive or explicitly bound the non-circular local metric response.",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2476_0_selected",
            "selection_status": "selected",
            "target_file": "2477-Y5-R2FR-parent-weak-field-metric-response-theorem-or-no-go.md",
            "target_script": "scripts/Y5_R2FR_parent_weak_field_metric_response_theorem_or_no_go_2477.py",
            "task": "derive the local weak-field metric response from the MTS parent action without assuming GR; if impossible, write the exact no-go/closure contract",
            "acceptance_target": "signed linearized metric operator, source coupling, Green/norm bound, gauge and boundary conditions, C_metric candidate or explicit blocker",
            "guardrails": "no GR shortcut; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "conditional_maps": OUTPUTS["conditional_maps"],
        "blocker_ledger": OUTPUTS["blocker_ledger"],
        "acquisition_queue": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2476_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(
            stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": notes,
                    "detail": detail,
                }
            )
        )

    sources_ok = all(row["source_pass"] is True for row in data["sources"])
    add("VAL2476_00_sources_exist", sources_ok, "all cited local source paths exist and needles are present")

    blockers = {row["blocker_id"]: row for row in data["blockers"]}
    add("VAL2476_01_KR10_blocked", blockers["BLOCK2476_0_KR10"]["status"] == "BLOCKED", "K_R10 remains explicitly blocked")
    add("VAL2476_02_Cmetric_blocked", blockers["BLOCK2476_1_Cmetric"]["status"] == "BLOCKED", "C_metric remains explicitly blocked")
    add("VAL2476_03_no_GR_shortcut", blockers["BLOCK2476_4_no_GR_shortcut"]["status"] == "GUARDRAIL_ACTIVE", "circular GR shortcut is forbidden")

    all_maps_nonclaim = all(row["valid_for_claim"] is False for row in data["maps"])
    add("VAL2476_04_maps_nonclaim", all_maps_nonclaim, "all conditional map rows remain nonclaim")

    no_claim_allowed = all(row["claim_allowed"] is False for row in data["gates"])
    add("VAL2476_05_claim_gates_safe", no_claim_allowed, "no gate allows an R10/local-GR claim")

    next_ok = any(row["route_id"] == "NEXT2476_0_selected" for row in data["next"])
    add("VAL2476_06_next_target_written", next_ok, "2477 parent weak-field metric response target selected")

    copies_ok = all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"])
    add("VAL2476_07_branch_copies", copies_ok, "nonclaim branch copies exist")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2476*", "*P8_Y5_R10_KERNEL_CMETRIC_2476*", "*JR2476*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2476_08_no_formalization_artifacts", not formalization_artifacts, "no 2476 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2476_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2476_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2476_OVERALL",
        overall,
        "2476 blocks the R10 kernel/C_metric claim path and selects the non-circular parent weak-field metric-response derivation",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2476 Y5 R2FR R10 Kernel and Cmetric Source Map or Blocker",
        "",
        "**Status:** R10 external-bound evidence is now source-backed, but the MTS prediction bridge is not closed. `K_R10(lambda)`, `C_metric`, and `E_GK_bound` remain missing, so no R10/local-GR/local-Newton claim is allowed.",
        "",
        "**Main result:** the tempting shortcut is rejected. We cannot set `C_metric` equal to the GR weak-field Green response in order to prove that MTS reduces to GR; that would be circular. The clean next target is the parent weak-field metric-response theorem.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Derivation Audit",
        markdown_table(data["audit"], ["derivation_id", "object", "candidate_relation", "status", "why_it_matters", "blocking_input", "claim_allowed"]),
        "",
        "## Blocker Ledger",
        markdown_table(data["blockers"], ["blocker_id", "missing_object", "blocked_claim", "required_evidence", "current_evidence", "status", "next_action", "valid_for_claim"]),
        "",
        "## Conditional Map Rows",
        markdown_table(data["maps"], ["map_id", "arena", "relation", "input_status", "units_status", "source_path", "valid_for_claim", "notes"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register_rows(),
        "audit": derivation_audit_rows(),
        "blockers": blocker_rows(),
        "maps": conditional_map_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["derivation_audit"], data["audit"])
    write_csv(OUTPUTS["blocker_ledger"], data["blockers"])
    write_csv(OUTPUTS["conditional_maps"], data["maps"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
