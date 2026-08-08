from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2732-Y5-R2FR-local-GR-route-rollup-after-memory-closure-only-or-next-derivation-branch.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2732_SOURCE_REGISTER.csv",
    "rollup": RESIDUALS / "P8_Y5_R2FR_2732_LOCAL_GR_ROUTE_ROLLUP.csv",
    "ranking": RESIDUALS / "P8_Y5_R2FR_2732_BRANCH_RANKING.csv",
    "no_circling": RESIDUALS / "P8_Y5_R2FR_2732_NO_CIRCLING_RULES.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2732_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2732_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2732_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2732_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2732_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "rollup": LOCAL_BOUNDS / "local_GR_route_rollup_2732_NONCLAIM.csv",
    "selection": SOURCE_WEIGHT / "local_GR_next_derivation_selection_2732_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2732_KHAT_KMETRIC_DELTAK_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
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
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = [
        "| " + " | ".join(str(row.get(col, "")).replace("\n", " ") for col in cols) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def source_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC2732_0_2731_memory_closure",
            "memory route closure-only handoff",
            DOC.parent / "2731-Y5-R2FR-parent-action-deep-memory-Hessian-source-hunt-or-closure-only-declaration-under-AX1090.md",
            ["CLOS2731_0_scope", "NEXT2731_0_selected", "VAL2731_OVERALL"],
        ),
        (
            "SRC2732_1_2711_AX1090",
            "parent object closure axiom status",
            DOC.parent / "2711-Y5-R2FR-AX1090-parent-object-derivation-from-MTS-primitives-or-explicit-closure.md",
            ["AX1090_0_LC", "DER2711_6_verdict", "EXPLICIT_CLOSURE_REQUIRED_NOT_CLAIM"],
        ),
        (
            "SRC2732_2_2712_Khat_q_loc",
            "A511/q_loc/Khat rollforward status",
            DOC.parent / "2712-Y5-R2FR-A511-local-EH-fixed-point-rollforward-under-AX1090-closure.md",
            ["QDK2712_0_vector_shell", "QDK2712_2_DeltaK", "A511R2712_6_verdict"],
        ),
        (
            "SRC2732_3_2713_KL00",
            "KL00 phiR improvement route",
            DOC.parent / "2713-Y5-R2FR-KL00-phiR-improvement-or-lambda-boundary-gate-under-AX1090-closure.md",
            ["lambda_phi", "Khat", "Delta_K"],
        ),
        (
            "SRC2732_4_2714_lambda_phi",
            "lambda_phi zero/bound and Khat adoption gate",
            DOC.parent / "2714-Y5-R2FR-lambda-phi-zero-bound-or-Khat-adoption-under-AX1090-closure.md",
            ["Khat adoption remains staged", "weak-field auxiliary action gate"],
        ),
        (
            "SRC2732_5_2716_RAB_finite",
            "finite R_AB operator route",
            DOC.parent / "2716-Y5-R2FR-parent-protection-contract-or-finite-ZR-row-under-AX1090-closure.md",
            ["finite reciprocal residual countermodel survives", "(-Z_R Delta_h + M_R^2) R_AB = J_eff"],
        ),
        (
            "SRC2732_6_2718_Jeff",
            "J_eff source-norm split",
            DOC.parent / "2718-Y5-R2FR-Jeff-source-norm-split-or-ZR-theorem-zero-under-AX1090-closure.md",
            ["J_eff = J_matter + J_boundary + J_harmonic + J_readout + J_shadow + J_norm", "E_Jeff"],
        ),
        (
            "SRC2732_7_2721_source_norm",
            "no fitted GM/source-normalization gate",
            DOC.parent / "2721-Y5-R2FR-source-normalization-no-fitted-GM-or-finite-EJeff-vector-under-AX1090-closure.md",
            ["No observed orbital `GM`", "parent Hilbert source mass plus a fixed parent metric coupling"],
        ),
        (
            "SRC2732_8_2722_Newton_bridge",
            "Poisson/Gauss Newton coefficient bridge",
            DOC.parent / "2722-Y5-R2FR-Poisson-Gauss-Newton-coefficient-bridge-or-Enorm-bound-under-AX1090-closure.md",
            ["parent metric coefficient `kappa0` plus parent Hilbert source", "**not** a Newton/GR claim"],
        ),
        (
            "SRC2732_9_2724_EH_operator",
            "EH weak-field operator/gauge domain",
            DOC.parent / "2724-Y5-R2FR-EH-left-hand-weak-field-operator-gauge-domain-or-Poisson-residual-row-under-AX1090-closure.md",
            ["E_Poisson_residual", "No EH-left-hand"],
        ),
        (
            "SRC2732_10_2725_Lovelock",
            "metric-only second-order Levi-Civita gate",
            DOC.parent / "2725-Y5-R2FR-metric-only-second-order-Levi-Civita-operator-gate-or-Eoperator-bound-under-AX1090-closure.md",
            ["Lovelock/EH operator follows", "MTS parent has not yet earned those premises"],
        ),
        (
            "SRC2732_11_2726_no_extension",
            "parent no-extension/minimality and LC descent",
            DOC.parent / "2726-Y5-R2FR-parent-no-extension-minimality-and-LC-descent-or-Eoperator-bound-under-AX1090-closure.md",
            ["conditional/residualized", "readout-after-variation"],
        ),
        (
            "SRC2732_12_2727_readout",
            "readout-after-variation generator attempt",
            DOC.parent / "2727-Y5-R2FR-readout-after-variation-no-reduced-action-backreaction-or-generator-row-under-AX1090-closure.md",
            ["not eliminated at theorem-zero level", "E_readout_reentry"],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, description, path, needles in specs:
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="ignore") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": source_id,
                "description": description,
                "source_path": str(path),
                "exists": exists,
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
            }
        )
    return rows


def route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "ROUTE2732_0_Khat_q_loc_tensor",
            "route": "Khat/Kmetric/DeltaK/q_loc tensor branch",
            "current_status": "LIVE_CONCRETE_BUT_BLOCKED",
            "best_progress": "Gamma_eff shape, KL00/phiR improvement path, and q_loc formula shell are already localized",
            "blocking_gap": "lambda_phi stress, full Kmetric derivative/domain/boundary terms, current-MTS Khat adoption, and Delta_K amplitude are missing",
            "next_testable_output": "Delta_K00/q_loc residual vector or a zero theorem for lambda_phi/Khat mismatch",
            "do_next": True,
            "valid_for_claim": False,
        },
        {
            "route_id": "ROUTE2732_1_source_Newton",
            "route": "source-normalized Newton/Poisson-Gauss bridge",
            "current_status": "STRUCTURALLY_STRONG_CONDITIONAL",
            "best_progress": "2721/2722 block fitted-GM cheating and state the parent Hilbert-source plus kappa0 coefficient map",
            "blocking_gap": "kappa0/G_ref parent ownership, fixed reference, Hilbert/worldtube equality, extra stress silence, and orbital readout map remain unsigned",
            "next_testable_output": "source-normalization residual vector E_norm/E_Jeff or fixed-before-readout coefficient row",
            "do_next": False,
            "valid_for_claim": False,
        },
        {
            "route_id": "ROUTE2732_2_EH_Lovelock_operator",
            "route": "EH/Lovelock metric-only second-order branch",
            "current_status": "RELATIVE_THEOREM_STRONG_PREMISES_UNSIGNED",
            "best_progress": "2724/2725 make the Lovelock/EH filter exact under metric-only 4D local second-order Levi-Civita premises",
            "blocking_gap": "no-extension/minimality, LC descent, hidden generator exclusion, R2/fR/nonlocal tower ban, and readout reentry remain open",
            "next_testable_output": "E_operator/E_Poisson residual rows or one killed generator certificate",
            "do_next": False,
            "valid_for_claim": False,
        },
        {
            "route_id": "ROUTE2732_3_AX1090_parent_object",
            "route": "AX1090 parent action object from primitives",
            "current_status": "FOUNDATIONAL_EXPLICIT_CLOSURE_NOT_IMMEDIATE",
            "best_progress": "2711 turns the hidden parent-object assumption into explicit local-transition closure AX1090_0_LC",
            "blocking_gap": "no single primitive source constructs Conf_parent, L_parent, q, matter descent, boundary class and variation order as one parent object",
            "next_testable_output": "new primitive parent-action source text or keep as closure ledger only",
            "do_next": False,
            "valid_for_claim": False,
        },
        {
            "route_id": "ROUTE2732_4_RAB_finite_residual",
            "route": "finite reciprocal R_AB Green-kernel branch",
            "current_status": "EMPIRICAL_BACKSTOP_READY_IN_FORM_NOT_VALUES",
            "best_progress": "finite operator (-Z_R Delta_h + M_R^2)R_AB=J_eff and source split are now explicit",
            "blocking_gap": "Z_R, M_R^2, J_eff component norms, boundary/harmonic/readout/source-normalization projections are missing",
            "next_testable_output": "first numeric/source-backed Z_R/M_R^2/J_eff/projection row",
            "do_next": False,
            "valid_for_claim": False,
        },
        {
            "route_id": "ROUTE2732_5_memory_positive_operator",
            "route": "memory positive-operator local silence",
            "current_status": "CLOSURE_ONLY_UNDER_CURRENT_CORPUS",
            "best_progress": "relative theorem is valid and finite memory residual interface is safe",
            "blocking_gap": "parent-signed memory Hessian/action/source/boundary owner absent after 2731",
            "next_testable_output": "none unless reopen conditions are supplied",
            "do_next": False,
            "valid_for_claim": False,
        },
        {
            "route_id": "ROUTE2732_6_empirical_local_bounds",
            "route": "R10/PPN/clock/orbital empirical local bounds",
            "current_status": "USEFUL_AFTER_PROJECTION_ROWS",
            "best_progress": "refusal machinery exists and finite residual schemas know what to reject",
            "blocking_gap": "arena projection coefficients and source-backed residual amplitudes are still placeholders",
            "next_testable_output": "dry-run local bounds only after one real residual coefficient row exists",
            "do_next": False,
            "valid_for_claim": False,
        },
    ]


def ranking_rows() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "route_id": "ROUTE2732_0_Khat_q_loc_tensor",
            "selection": "PRIMARY_NEXT",
            "why": "most concrete non-closure derivation target; directly touches q_loc and local PPN residuals",
            "risk": "may still become finite residual rather than zero theorem",
            "expected_checkpoint": "2733 Khat/Kmetric/DeltaK00 amplitude-response or first q_loc residual bound",
            "valid_for_claim": False,
        },
        {
            "rank": 2,
            "route_id": "ROUTE2732_1_source_Newton",
            "selection": "SECONDARY_NEXT",
            "why": "best GR/Newton bridge discipline because it prevents fitted-GM backfill",
            "risk": "depends on kappa0/source/Hilbert/worldtube certificates",
            "expected_checkpoint": "source-normalization E_norm/E_Jeff row after Khat/q_loc branch",
            "valid_for_claim": False,
        },
        {
            "rank": 3,
            "route_id": "ROUTE2732_2_EH_Lovelock_operator",
            "selection": "KEEP_AS_THEOREM_BACKBONE",
            "why": "powerful if premises close, but too broad for immediate next shot",
            "risk": "easy to circle by restating Lovelock premises",
            "expected_checkpoint": "only revisit with one concrete generator kill or residual row",
            "valid_for_claim": False,
        },
        {
            "rank": 4,
            "route_id": "ROUTE2732_4_RAB_finite_residual",
            "selection": "EMPIRICAL_BACKSTOP",
            "why": "ready shape for eventual tests but not derivation-first",
            "risk": "can become data plumbing without parent coefficient source",
            "expected_checkpoint": "defer until source-backed coefficient acquisition",
            "valid_for_claim": False,
        },
        {
            "rank": 5,
            "route_id": "ROUTE2732_3_AX1090_parent_object",
            "selection": "FOUNDATIONAL_REOPEN_ONLY",
            "why": "important but currently closure-labelled; requires new primitive source text",
            "risk": "retreading this without new material circles",
            "expected_checkpoint": "reopen only if new parent action primitive is supplied",
            "valid_for_claim": False,
        },
        {
            "rank": 6,
            "route_id": "ROUTE2732_5_memory_positive_operator",
            "selection": "DO_NOT_REPEAT_NOW",
            "why": "2731 already exhausted the parent-source hunt and scoped closure-only result",
            "risk": "repeating it would burn work without new parent action text",
            "expected_checkpoint": "none unless reopen conditions are met",
            "valid_for_claim": False,
        },
    ]


def no_circling_rows() -> list[dict[str, Any]]:
    return [
        {
            "rule_id": "NC2732_0_memory",
            "rule": "do not rerun memory positive-operator proof",
            "unless": "a new parent-action source signs the 2731 reopen conditions",
            "reason": "route is closure-only under current corpus",
            "valid_for_claim": False,
        },
        {
            "rule_id": "NC2732_1_AX1090",
            "rule": "do not retest AX1090 parent object from the same primitive files",
            "unless": "new primitive source text or a formal parent action object is supplied",
            "reason": "2711 already converted it to explicit closure AX1090_0_LC",
            "valid_for_claim": False,
        },
        {
            "rule_id": "NC2732_2_EH",
            "rule": "do not do another broad EH/Lovelock recap",
            "unless": "one generator/no-extension/LC premise is actually killed or bounded",
            "reason": "2724-2726 already wrote the relative theorem and residual rows",
            "valid_for_claim": False,
        },
        {
            "rule_id": "NC2732_3_Khat",
            "rule": "next Khat/q_loc attempt must produce an object",
            "unless": "it explicitly demotes to a finite residual row",
            "reason": "we need Delta_K/q_loc amplitude, source path, or closure; not another narrative bridge",
            "valid_for_claim": False,
        },
        {
            "rule_id": "NC2732_4_data",
            "rule": "do not score R10/PPN/clock/orbital rows from placeholders",
            "unless": "source-backed residual coefficients and projection kernels exist",
            "reason": "current local-bound machinery correctly refuses fake passes",
            "valid_for_claim": False,
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("GATE2732_0_local_GR", "local GR derived", "all surviving routes have unsigned premises"),
        ("GATE2732_1_Newton", "Newton/Poisson pass", "source/kappa/EH/readout bridge remains conditional"),
        ("GATE2732_2_PPN", "PPN pass", "q_loc/Khat/DeltaK and projection rows missing"),
        ("GATE2732_3_R10", "R10 pass", "no source-backed alpha/range coefficient row"),
        ("GATE2732_4_memory_zero", "memory theorem-zero", "closure-only under 2731"),
        ("GATE2732_5_public", "public claim", "private route-selection checkpoint only"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": False,
            "reason": reason,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for gate_id, claim, reason in claims
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2732_0_no_more_memory_loop",
            "decision": "STOP_REPEATING_MEMORY_ZERO_ROUTE",
            "because": "2731 scoped it closure-only and retained finite residual interface",
            "effect": "memory can re-enter only with new parent action/source rows",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2732_1_primary_route",
            "decision": "SELECT_KHAT_KMETRIC_DELTAK_QLOC",
            "because": "it is the most concrete live derivation route and directly controls local residual vector",
            "effect": "next work must compute/bound Delta_K00 or q_loc, or explicitly demote it to residual",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2732_2_secondary_route",
            "decision": "KEEP_SOURCE_NORMALIZED_NEWTON_SECOND",
            "because": "it is the strongest anti-posthoc GR/Newton discipline once q_loc/Khat is not hiding a source term",
            "effect": "return to source-normalization after Khat/q_loc branch yields an object",
            "valid_for_claim": False,
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2732_0_selected",
            "status": "selected_primary",
            "target_doc": "2733-Y5-R2FR-Khat-Kmetric-DeltaK00-amplitude-response-or-first-q_loc-residual-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_Khat_Kmetric_DeltaK00_amplitude_response_or_first_q_loc_residual_bound_under_AX1090_2733.py",
            "mission": "take the Khat/q_loc tensor branch forward by deriving or bounding Delta_K00/q_loc from the staged Kmetric, KL00, lambda_phi and Gamma_eff pieces",
            "acceptance": "one of: parent-signed silence clause; source-backed amplitude/bound row; or explicit finite residual row with missing coefficients named",
            "forbidden": "another broad EH recap; memory-positive-operator repeat; placeholder local-test score; GitHub action; formalization-workbench edits",
            "selected": True,
            "valid_for_claim": False,
        }
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "COPY2732_0_rollup",
            "source_table": str(OUTPUTS["rollup"]),
            "copy_path": str(BRANCH_OUTPUTS["rollup"]),
            "purpose": "local-bounds branch sees route status and no-claim state",
            "exists": BRANCH_OUTPUTS["rollup"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2732_1_selection",
            "source_table": str(OUTPUTS["ranking"]),
            "copy_path": str(BRANCH_OUTPUTS["selection"]),
            "purpose": "source-weight branch receives next derivation selection",
            "exists": BRANCH_OUTPUTS["selection"].exists(),
            "valid_for_claim": False,
        },
        {
            "copy_id": "COPY2732_2_next_queue",
            "source_table": str(OUTPUTS["next"]),
            "copy_path": str(BRANCH_OUTPUTS["next_queue"]),
            "purpose": "queues Khat/Kmetric/DeltaK q_loc target",
            "exists": BRANCH_OUTPUTS["next_queue"].exists(),
            "valid_for_claim": False,
        },
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    ranking: list[dict[str, Any]],
    no_circling: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    route_ok = len(routes) >= 6 and sum(row["do_next"] is True for row in routes) == 1
    ranking_ok = ranking[0]["route_id"] == "ROUTE2732_0_Khat_q_loc_tensor" and ranking[0]["selection"] == "PRIMARY_NEXT"
    no_circling_ok = len(no_circling) >= 5 and any(row["rule_id"] == "NC2732_0_memory" for row in no_circling)
    gates_false = all(row["gate_pass"] is False and row["claim_allowed"] is False for row in gates)
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    formalization_ok = formalization_recent_count() == 0
    csv_ok = True
    csv_bits = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    rows = [
        {"validation_id": "VAL2732_0_sources", "passed": source_ok, "detail": "all source paths exist and needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2732_1_route_selection_unique", "passed": route_ok, "detail": "exactly one route selected as immediate next", "timestamp_utc": ts()},
        {"validation_id": "VAL2732_2_ranking_primary", "passed": ranking_ok, "detail": "Khat/Kmetric/DeltaK/q_loc selected as primary next branch", "timestamp_utc": ts()},
        {"validation_id": "VAL2732_3_no_circling_rules", "passed": no_circling_ok, "detail": "memory/AX1090/EH/data rerun rules recorded", "timestamp_utc": ts()},
        {"validation_id": "VAL2732_4_claim_gates_false", "passed": gates_false, "detail": "all claim gates remain false", "timestamp_utc": ts()},
        {"validation_id": "VAL2732_5_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2732_6_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2732_7_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_recent_count()}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2732_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2732 rolls up local-GR routes, freezes memory-repeat loops, and selects Khat/Kmetric/DeltaK/q_loc as the next concrete branch",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2732 - Y5 R2/f(R): Local-GR Route Rollup After Memory Closure-Only Or Next Derivation Branch

Status: `Y5_R2FR_2732_local_GR_route_rollup_selects_Khat_Kmetric_DeltaK_q_loc_next_nonclaim`

## Private Verdict

2732 is the anti-circling checkpoint. After 2731, the memory positive-operator zero route is closure-only under the current corpus, so it should not keep eating the project unless new parent-action text appears.

The surviving live branch with the most concrete mathematical handle is the `Khat/Kmetric/DeltaK/q_loc` tensor route. It is not claim-ready, but it has actual pieces on the board: `Gamma_eff`, `K_L^00`, `phi R`/lambda_phi machinery, and a defined q_loc residual shell. That makes it a better next shot than another broad EH recap or another AX1090 parent-object hunt from the same files.

No local-GR, Newton, PPN, R10, WEP, clock, orbital, memory-zero, or public claim follows from this checkpoint.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Local-GR Route Rollup

{markdown_table(data["rollup"], ["route_id", "route", "current_status", "best_progress", "blocking_gap", "next_testable_output", "do_next", "valid_for_claim"])}

## Branch Ranking

{markdown_table(data["ranking"], ["rank", "route_id", "selection", "why", "risk", "expected_checkpoint", "valid_for_claim"])}

## No-Circling Rules

{markdown_table(data["no_circling"], ["rule_id", "rule", "unless", "reason", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decision"], ["decision_id", "decision", "because", "effect", "valid_for_claim"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

Best route now: take the Khat/q_loc tensor branch and force it to produce something concrete. Either it gives a parent-signed silence clause, or it gives a finite residual vector, or it admits exactly which coefficient is missing. That is the least circular next punch.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    rollup = route_rows()
    ranking = ranking_rows()
    no_circling = no_circling_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["rollup"], rollup)
    write_csv(OUTPUTS["ranking"], ranking)
    write_csv(OUTPUTS["no_circling"], no_circling)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["rollup"], rollup)
    write_csv(BRANCH_OUTPUTS["selection"], ranking)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    validation = validation_rows(sources, rollup, ranking, no_circling, gates)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "rollup": rollup,
        "ranking": ranking,
        "no_circling": no_circling,
        "gates": gates,
        "decision": decisions,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2732 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
