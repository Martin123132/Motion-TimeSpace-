from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "787-Y5-R10-multifield-pregeometry-rank-gate-or-independent-metric-branch-decision.md"
NEXT_TARGET = "788-Y5-R10-nonholonomic-coframe-or-moment-closure-parent-action.md"
STATUS = "Y5_R10_787_multifield_pregeometry_rank_gate_passes_conditionally_but_integrability_curvature_blocks_local_GR_claim"
CLAIM_CEILING = "rank_gate_and_branch_decision_only_no_adopted_pregeometry_no_parent_action_no_local_GR_Newton_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_787_SOURCE_REGISTER.csv"
RANK_SMOKE_PATH = RESIDUALS / "P8_Y5_R10_787_NUMERICAL_RANK_SMOKE.csv"
PREGEO_RANK_GATE_PATH = RESIDUALS / "P8_Y5_R10_787_MULTIFIELD_PREGEOMETRY_RANK_GATE.csv"
CURVATURE_GATE_PATH = RESIDUALS / "P8_Y5_R10_787_CURVATURE_INTEGRABILITY_GATE.csv"
BRANCH_DECISION_PATH = RESIDUALS / "P8_Y5_R10_787_BRANCH_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_787_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_787_VALIDATION.csv"

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_787_ADOPTED_MULTIFIELD_PREGEOMETRY.csv",
    RESIDUALS / "P8_Y5_R10_787_PARENT_ACTION_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_787_LOCAL_GR_REENTRY_CANDIDATE.csv",
    RESIDUALS / "P8_Y5_R10_787_NEWTON_LIMIT_PROOF.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    RANK_SMOKE_PATH,
    PREGEO_RANK_GATE_PATH,
    CURVATURE_GATE_PATH,
    BRANCH_DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "786_doc": {
        "path": POST_CHECKPOINT / "786-Y5-R10-parent-action-metric-map-ownership-or-bg-bound-source-pack.md",
        "needles": ["Current result", "multifield/pregeometry"],
        "role": "immediate 787 handoff",
    },
    "786_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_786_VALIDATION.csv",
        "needles": ["V786_6_scalar_only_blocked", "V786_11_next_target_selected"],
        "role": "prior validation guard",
    },
    "786_candidates": {
        "path": RESIDUALS / "P8_Y5_R10_786_PARENT_ACTION_OWNERSHIP_CANDIDATES.csv",
        "needles": ["PAO786_3_multifield_pregeometry", "PAO786_2_independent_metric_branch"],
        "role": "candidate branch inputs",
    },
    "786_rank_gate": {
        "path": RESIDUALS / "P8_Y5_R10_786_VARIATIONAL_RANK_GATE.csv",
        "needles": ["VRG786_1_unsmoothed_scalar_rank", "VRG786_3_multifield_rank_condition"],
        "role": "rank obstruction input",
    },
    "785_contract": {
        "path": RESIDUALS / "P8_Y5_R10_785_PSI_METRIC_COFRAME_CONTRACT.csv",
        "needles": ["PMC785_2_local_coframe_existence", "PMC785_6_parent_action_metric_ownership"],
        "role": "coframe and parent-action contract",
    },
    "spine_07": {
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["emergent or effective metric", "MTS parent theory -> effective GR"],
        "role": "unification spine and GR/Newton chain",
    },
    "testing_145": {
        "path": FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md",
        "needles": ["MTS -> GR -> Newton", "missing GR-limit theorem"],
        "role": "local GR-limit demand",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def matrix_rank(matrix: list[list[float]], tolerance: float = 1e-10) -> int:
    rows = [row[:] for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    col_count = len(rows[0])
    rank = 0
    pivot_col = 0
    while rank < row_count and pivot_col < col_count:
        pivot_row = max(range(rank, row_count), key=lambda row_index: abs(rows[row_index][pivot_col]))
        if abs(rows[pivot_row][pivot_col]) <= tolerance:
            pivot_col += 1
            continue
        rows[rank], rows[pivot_row] = rows[pivot_row], rows[rank]
        pivot = rows[rank][pivot_col]
        rows[rank] = [value / pivot for value in rows[rank]]
        for row_index in range(row_count):
            if row_index == rank:
                continue
            factor = rows[row_index][pivot_col]
            if abs(factor) > tolerance:
                rows[row_index] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(rows[row_index], rows[rank], strict=True)
                ]
        rank += 1
        pivot_col += 1
    return rank


def coefficient_matrix_for_variation(field_count: int) -> list[list[float]]:
    symmetric_pairs = [(mu, nu) for mu in range(4) for nu in range(mu, 4)]
    variable_pairs = [(alpha, field) for alpha in range(4) for field in range(field_count)]
    h_diag = [-1.0] + [1.0 for _ in range(max(0, field_count - 1))]
    matrix: list[list[float]] = []
    for mu, nu in symmetric_pairs:
        row: list[float] = []
        for alpha, field in variable_pairs:
            coefficient = 0.0
            if field < 4:
                if alpha == mu and field == nu:
                    coefficient += h_diag[field]
                if alpha == nu and field == mu:
                    coefficient += h_diag[field]
            row.append(coefficient)
        matrix.append(row)
    return matrix


def under_post_checkpoint(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed_count = 0
    for scanned_path in FORMALIZATION.rglob("*"):
        if scanned_path.is_file() and datetime.fromtimestamp(scanned_path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            changed_count += 1
    return changed_count


def validation_clean(number: int) -> bool:
    path = RESIDUALS / f"P8_Y5_BRR545_{number}_VALIDATION.csv"
    rows = read_csv_rows(path)
    return path.exists() and bool(rows) and all(row.get("result") == "pass" for row in rows)


def source_register_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCE_SPECS.items()
    ]


def rank_smoke_rows(generated_utc: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for field_count in [1, 2, 3, 4, 5, 6]:
        matrix = coefficient_matrix_for_variation(field_count)
        rank = matrix_rank(matrix)
        rows.append(
            {
                "smoke_id": f"N{field_count}_rank",
                "field_count_N": field_count,
                "linearized_map": "deltaG_mu_nu = deltaV_muA H_AB V_nuB + V_muA H_AB deltaV_nuB at V=[I_4,0]",
                "rank": rank,
                "target_symmetric_metric_components": 10,
                "rank_full": bool_string(rank == 10),
                "interpretation": "full local symmetric-tensor span" if rank == 10 else "insufficient local metric-variation span",
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def pregeometry_rank_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "MPR787_0_scalar_route",
            "question": "Can one scalar psi own generic local GR metric variations?",
            "result": "no",
            "argument": "rank(deltaG/delta psi) is at most four local directions and the 786 scalar-gradient map is rank-one at a point",
            "repair_needed": "multifield psi^A, independent moment tensor, coframe variable, or independent metric",
            "branch_effect": "scalar-only psi demoted as sole GR owner",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MPR787_1_minimal_multifield_rank",
            "question": "How many independent pregeometry directions are needed for first-order metric-variation rank?",
            "result": "N_at_least_4_conditional",
            "argument": "for G=VHV^T, if V has rank four and H is nondegenerate on that image, deltaV spans all ten symmetric metric components",
            "repair_needed": "declare what the four directions physically are and why they are not arbitrary labels",
            "branch_effect": "multifield/pregeometry remains alive",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MPR787_2_surjectivity_condition",
            "question": "What exact theorem must a future parent action prove?",
            "result": "local_surjectivity_contract",
            "argument": "rank(delta G_mu_nu / delta psi^A) must cover symmetric tensor variations modulo diffeomorphism/gauge directions in the local GR domain",
            "repair_needed": "prove rank condition from parent background/coarse-grained state, not by tuning after the fact",
            "branch_effect": "precise acceptance gate set",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MPR787_3_internal_signature",
            "question": "Can positive scalar covariance alone supply a Lorentzian metric?",
            "result": "not_without_signature_structure",
            "argument": "a positive Gram correction alone does not own Lorentzian signature; an internal Lorentzian metric, background, or coframe signature rule is required",
            "repair_needed": "derive or declare internal signature and prove stability of local Lorentzian domain",
            "branch_effect": "signature remains a live gate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MPR787_4_matter_coupling",
            "question": "Does passing the rank gate prove matter-frame blindness?",
            "result": "no",
            "argument": "rank only says metric variations can be represented; matter could still see psi^A, moments, or frame representatives directly",
            "repair_needed": "parent-signed S_matter[e_obs,omega,owned gauge fields] and no-spurion audit",
            "branch_effect": "b_g/c_g remains active",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "MPR787_5_rank_gate_verdict",
            "question": "Can multifield/pregeometry rescue the 786 rank obstruction?",
            "result": "yes_conditionally_not_adopted",
            "argument": "N>=4 full-rank pregeometry can pass first-order rank, but curvature/integrability/action ownership still block local GR",
            "repair_needed": NEXT_TARGET,
            "branch_effect": "continue derivation via nonholonomic coframe or moment closure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def curvature_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CIG787_0_flat_pullback_trap",
            "issue": "If e^a_mu = partial_mu psi^a and internal H_ab is constant, g_mu_nu is locally the pullback of a flat target metric.",
            "result": "curvature_block",
            "why_it_matters": "an invertible exact-gradient coframe is just a coordinate pullback and cannot produce generic curved GR geometry",
            "escape_route": "nonholonomic coframe, nonconstant/internal curved metric, or coarse-grained independent moment tensor",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CIG787_1_nonholonomic_coframe",
            "issue": "Promote e^a_mu or distortion E^a_mu to a field not constrained to be d psi^a.",
            "result": "viable_low_scrutiny_branch",
            "why_it_matters": "generic tetrads can carry curvature and recover standard GR machinery",
            "escape_route": "derive e from motion/time/space parent variables or accept independent tetrad/metric branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CIG787_2_moment_closure",
            "issue": "Treat <partial psi^A partial psi^B> as a coarse-grained covariance/moment field with independent dynamics.",
            "result": "viable_but_unsigned",
            "why_it_matters": "this preserves the motion-flow intuition while escaping the exact-gradient flatness trap",
            "escape_route": "derive a covariant moment evolution equation and closure from parent dynamics",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CIG787_3_independent_metric",
            "issue": "Keep g_mu_nu as independent/effective metric with psi/memory as stress-exchange fields.",
            "result": "conservative_fallback",
            "why_it_matters": "this most cleanly protects local GR and Newton but weakens the pure-emergent claim",
            "escape_route": "write standard EH metric sector plus MTS exchange stress and prove conservation/limits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CIG787_4_curvature_verdict",
            "issue": "Does the multifield rank gate alone derive GR?",
            "result": "no",
            "why_it_matters": "rank solves one algebraic obstruction but not curvature, dynamics, covariance, or coupling ownership",
            "escape_route": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def branch_decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D787_0_scalar_only_demoted",
            "decision": "demote single-scalar psi as sole local-GR owner",
            "reason": "fails rank and exact-gradient curvature tests",
            "result": "demoted_not_dead_as_component",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D787_1_multifield_kept",
            "decision": "keep multifield/pregeometry route alive",
            "reason": "N>=4 full-rank bundle can pass local variation rank if the field content and signature are real",
            "result": "conditional_route_retained",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D787_2_no_adoption",
            "decision": "do not adopt multifield pregeometry yet",
            "reason": "curvature, covariance, parent action, and matter coupling are not derived",
            "result": "not_adopted",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D787_3_fallback",
            "decision": "retain independent metric/tetrad as fallback",
            "reason": "it is the least-scrutiny path to local GR/Newton if emergent ownership keeps failing",
            "result": "fallback_retained",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D787_4_next_target",
            "decision": "try nonholonomic coframe or moment-closure parent action next",
            "reason": "that is the smallest route that can pass rank without falling into flat pullback geometry",
            "result": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "multifield/pregeometry with N>=4 can conditionally solve the first-order metric-variation rank problem, but exact-gradient scalar/coframe maps with constant internal metric fall into a flat pullback trap",
            "hard_blocker": "need nonholonomic coframe, covariant moment closure, or independent metric/tetrad branch plus parent action and matter-coupling proof",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_rows(*row_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in row_groups:
        rows.extend(group)
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    rank_smoke: list[dict[str, Any]],
    rank_gate: list[dict[str, Any]],
    curvature_gate: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_786_clean = all(validation_clean(number) for number in range(665, 787))
    rank_smoke_complete = len(rank_smoke) == 6
    scalar_rank_insufficient = any(row["field_count_N"] == 1 and row["rank_full"] == "false" for row in rank_smoke)
    n4_rank_full = any(row["field_count_N"] == 4 and row["rank_full"] == "true" for row in rank_smoke)
    rank_gate_complete = len(rank_gate) == 6
    multifield_conditional = any(row["gate_id"] == "MPR787_5_rank_gate_verdict" and row["result"] == "yes_conditionally_not_adopted" for row in rank_gate)
    curvature_gate_complete = len(curvature_gate) == 5
    flat_pullback_block = any(row["gate_id"] == "CIG787_0_flat_pullback_trap" and row["result"] == "curvature_block" for row in curvature_gate)
    no_adoption = any(row["decision_id"] == "D787_2_no_adoption" and row["result"] == "not_adopted" for row in decisions)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D787_4_next_target" for row in decisions)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, rank_smoke, rank_gate, curvature_gate, decisions, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V787_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V787_1_source_needles_present", source_needles_present, "all source needles present"),
        ("V787_2_prior_665_786_clean", prior_665_786_clean, "665-786 validation rows have no failures"),
        ("V787_3_rank_smoke_complete", rank_smoke_complete, "numerical rank smoke rows complete"),
        ("V787_4_scalar_rank_insufficient", scalar_rank_insufficient, "N=1 does not span ten metric components"),
        ("V787_5_N4_rank_full", n4_rank_full, "N=4 full-rank bundle spans ten metric components in smoke gate"),
        ("V787_6_rank_gate_complete", rank_gate_complete, "multifield rank gate rows complete"),
        ("V787_7_multifield_conditional", multifield_conditional, "multifield route retained conditionally, not adopted"),
        ("V787_8_curvature_gate_complete", curvature_gate_complete, "curvature/integrability rows complete"),
        ("V787_9_flat_pullback_block", flat_pullback_block, "exact-gradient flat pullback trap recorded"),
        ("V787_10_no_adoption", no_adoption, "no multifield/pregeometry branch adopted"),
        ("V787_11_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V787_12_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V787_13_claim_artifacts_absent", claim_artifacts_absent, "no adopted-pregeometry/parent-action/local-GR/Newton claim artifact fabricated"),
        ("V787_14_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V787_15_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V787_16_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    rank_smoke: list[dict[str, Any]],
    rank_gate: list[dict[str, Any]],
    curvature_gate: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 787 - Y5 R10 Multifield Pregeometry Rank Gate Or Independent Metric Branch Decision

Current result: **the multifield/pregeometry route survives the algebraic rank problem, but only conditionally**. A single scalar `psi` cannot own generic local GR metric variations. A rank-four bundle `psi^A` or equivalent pregeometry can span the ten local symmetric metric components at first order, but an exact-gradient coframe with constant internal metric falls into the flat-pullback trap. So the next derivation must use a nonholonomic coframe, a covariant moment closure, or the conservative independent metric/tetrad branch.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Numerical Rank Smoke

{markdown_table(rank_smoke, ["smoke_id", "field_count_N", "linearized_map", "rank", "target_symmetric_metric_components", "rank_full", "interpretation", "valid_for_claim"])}

## Multifield Pregeometry Rank Gate

{markdown_table(rank_gate, ["gate_id", "question", "result", "argument", "repair_needed", "branch_effect", "valid_for_claim"])}

## Curvature Integrability Gate

{markdown_table(curvature_gate, ["gate_id", "issue", "result", "why_it_matters", "escape_route", "valid_for_claim"])}

## Branch Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is a real improvement in the map. The route "motion/time/space only" is not dead, but it cannot mean one thin scalar doing all the metric work. It must mean a rank-carrying pregeometry: at least four independent directions, plus a nonholonomic or moment-based mechanism so the metric can actually curve. If that cannot be derived, the serious field-theory route is to keep a standard metric/tetrad sector and let MTS enter through controlled stress, memory, and exchange terms.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    rank_smoke = rank_smoke_rows(generated_utc)
    rank_gate = pregeometry_rank_gate_rows(generated_utc)
    curvature_gate = curvature_gate_rows(generated_utc)
    decisions = branch_decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, rank_smoke, rank_gate, curvature_gate, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(RANK_SMOKE_PATH, rank_smoke, ["smoke_id", "field_count_N", "linearized_map", "rank", "target_symmetric_metric_components", "rank_full", "interpretation", "valid_for_claim", "generated_utc"])
    write_csv(PREGEO_RANK_GATE_PATH, rank_gate, ["gate_id", "question", "result", "argument", "repair_needed", "branch_effect", "valid_for_claim", "generated_utc"])
    write_csv(CURVATURE_GATE_PATH, curvature_gate, ["gate_id", "issue", "result", "why_it_matters", "escape_route", "valid_for_claim", "generated_utc"])
    write_csv(BRANCH_DECISION_PATH, decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, rank_smoke, rank_gate, curvature_gate, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"787 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
