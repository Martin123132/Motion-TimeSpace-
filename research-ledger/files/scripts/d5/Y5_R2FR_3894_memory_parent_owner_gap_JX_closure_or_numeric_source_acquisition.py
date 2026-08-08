from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3894"
BRANCH = "MTS_R2FR_Y5_MEMORY_PARENT_OWNER_GAP_JX_CLOSURE_OR_NUMERIC_SOURCE_ACQUISITION_3894"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3894-Y5-R2FR-memory-parent-owner-gap-JX-closure-or-numeric-source-acquisition.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3893_NEXT = OUT / "P8_Y5_R2FR_3893_NEXT_TARGET.csv"
CSV_3893_MEMORY = OUT / "P8_Y5_R2FR_3893_MEMORY_SILENCE_THEOREM_OR_BOUND.csv"
CSV_3893_FILL = OUT / "P8_Y5_R2FR_3893_NUMERIC_SOURCE_FILL_QUEUE.csv"
CSV_3893_VALIDATION = OUT / "P8_Y5_BRR545_3893_VALIDATION.csv"
CSV_MEM_OWNER = OUT / "P8_Y5_MEMORY_OWNER_GATE_2626_PARENT_MEMORY_OPERATOR_OWNER_AUDIT.csv"
CSV_MEM_POS = OUT / "P8_Y5_MEMORY_OWNER_GATE_2626_POSITIVE_OPERATOR_ZERO_THEOREM_ATTEMPT.csv"
CSV_MEM_JX = OUT / "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_JX_COMPONENT_ZERO_GATE.csv"
CSV_MEM_BOUND = OUT / "P8_Y5_MEMORY_SOURCE_BOUNDARY_2627_FINITE_RESIDUAL_BOUND_PACK.csv"
CSV_3887_YLOC = OUT / "P8_Y5_R2FR_3887_YLOC_COMPONENT_CLOSURE_MATRIX.csv"
CSV_3890_ZERO = OUT / "P8_Y5_R2FR_3890_DIRECT_SOURCE_ZERO_UPDATE.csv"
CSV_3891_LOCK = OUT / "P8_Y5_R2FR_3891_RESIDUAL_LOCK_MAP.csv"
CSV_3892_FILL = OUT / "P8_Y5_R2FR_3892_ALPHA3_PROJECTOR_NUMERIC_FILL_ROWS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3894_SOURCE_REGISTER.csv",
    "owner": OUT / "P8_Y5_R2FR_3894_MEMORY_PARENT_OWNER_INSERTION.csv",
    "jx": OUT / "P8_Y5_R2FR_3894_MEMORY_JX_COMPONENT_CLOSURE_GATE.csv",
    "gap": OUT / "P8_Y5_R2FR_3894_MEMORY_GAP_BOUND_AND_PROJECTION_ACQUISITION.csv",
    "gate": OUT / "P8_Y5_R2FR_3894_LOCAL_GR_DECISION_GATE.csv",
    "runner": OUT / "P8_Y5_R2FR_3894_RUNNER_UPDATE.csv",
    "next": OUT / "P8_Y5_R2FR_3894_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3894_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3894_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3894_00_next", CSV_3893_NEXT, "NEXT3893_0", "3893 selected memory owner/gap/JX target"),
    ("SRC3894_01_memory", CSV_3893_MEMORY, "MEM3893_5_verdict", "3893 memory verdict"),
    ("SRC3894_02_fill", CSV_3893_FILL, "SRCF3893_0_memory_gap", "3893 source fill queue"),
    ("SRC3894_03_validation", CSV_3893_VALIDATION, "VAL3893_14_next_target", "3893 validation"),
    ("SRC3894_04_owner", CSV_MEM_OWNER, "MOA2626_0_parent_X", "memory parent owner audit"),
    ("SRC3894_05_positive", CSV_MEM_POS, "ZPT2626_1_energy_identity", "positive operator theorem"),
    ("SRC3894_06_jx", CSV_MEM_JX, "JX2627_6_total_verdict", "JX source component gate"),
    ("SRC3894_07_bound", CSV_MEM_BOUND, "RBP2627_4_local_projection", "memory finite residual bound"),
    ("SRC3894_08_yloc", CSV_3887_YLOC, "YLC3887_5_nonlocal_memory", "Yloc memory component"),
    ("SRC3894_09_direct_zero", CSV_3890_ZERO, "DZU3890_1_delta_w", "direct source zero update"),
    ("SRC3894_10_lock", CSV_3891_LOCK, "RLM3891_4_memory", "memory residual lock status"),
    ("SRC3894_11_3892_fill", CSV_3892_FILL, "AF3892_3_Gdot_boundary", "Gdot/boundary fill context"),
]

MEMORY_OWNER = "X_mem := y^memory is a parent auxiliary component of Y_loc^A in S_y, with Sigma_loc including G_mem X_mem^2 and K_history := K[X_mem]"
MEMORY_ACTION = "S_mem = -1/2 int_D sqrt(h) [A^ij_mem D_i X_mem D_j X_mem + m_mem^2 X_mem^2] + int_D sqrt(h) J_X X_mem + boundary_X"
MEMORY_BOUND = "||X_mem|| <= (||J_X|| + boundary_lift_norm)/lambda_gap, with lambda_gap := a_min lambda_1(D)+m_min^2"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return ""
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        cells = [str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_memory_parent_owner_gap_JX",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def owner_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("OWN3894_0_owner", "memory parent variable", MEMORY_OWNER, "CANDIDATE_OWNER_INSERTED", "candidate branch owns X_mem; historical corpus global adoption remains false"),
        ("OWN3894_1_action", "memory quadratic sector", MEMORY_ACTION, "CANDIDATE_ACTION_INSERTED", "sign/gap/source/boundary inputs still needed"),
        ("OWN3894_2_evenness", "zero origin/no affine source", "candidate S_mem is even in X_mem except explicit J_X and boundary_X terms; no hidden affine X0(q) shift is allowed unless scored", "CANDIDATE_NO_AFFINE_SHIFT", "must retain shifted-source norm if affine origin is later allowed"),
        ("OWN3894_3_Yloc", "residual-lock to Y_loc", "K_history and nonlocal memory kernel norm are physical Y_loc components, not post-hoc diagnostics", "PARTIAL_RESIDUAL_LOCK_CANDIDATE", "projection coefficients still needed for observables"),
        ("OWN3894_4_scope", "scope guard", "candidate ownership does not prove X_mem=0; it only makes the Euler problem well-typed", "NO_SILENCE_CLAIM", "local-GR remains blocked"),
    ]
    return [
        {
            "owner_id": row_id,
            "piece": piece,
            "statement_or_math": statement,
            "status": status,
            "remaining_failure": failure,
            "candidate_branch_signed": "CANDIDATE" in status or "PARTIAL" in status,
            "global_corpus_adopted": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, failure in raw_rows
    ]


def jx_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("JXG3894_0_kin_affine", "J_X^kin_affine", "zero if candidate no-affine-shift/even-origin clause holds", "PASS_CANDIDATE_BRANCH", "affine shift must be scored if later allowed"),
        ("JXG3894_1_matter", "J_X^matter", "zero for quotient-observed matter and 3890 no hidden source grammar", "PASS_CANDIDATE_BRANCH", "shadow/disformal extension would reopen row"),
        ("JXG3894_2_observed_slot", "J_X^obs", "zero if observed coupling is Sigma/Yloc-selected with no single-zero leak", "PASS_IF_SIGMA_SELECTED", "requires same Sigma selection as R11 and no wall motion"),
        ("JXG3894_3_chi_wall", "J_X^chi_wall", "zero only if local domain selector/wall is fixed, exact, or included in Yloc with double-zero stress", "FAIL_UNSIGNED", "domain-wall source remains possible"),
        ("JXG3894_4_boundary", "J_X^boundary", "zero only by boundary certificate/no-flux/topological clause", "FAIL_UNSIGNED", "boundary lift norm remains needed"),
        ("JXG3894_5_history", "J_X^history", "zero only if memory kernel is local, causal, stable, source-free and has no long tail", "FAIL_UNSIGNED", "history_tail_norm remains needed"),
        ("JXG3894_6_total", "J_X_total", "J_kin and J_matter candidate-zero; observed slot conditional; chi_wall/boundary/history open", "PARTIAL_JX_CLOSURE_ONLY", "finite memory residual remains active"),
    ]
    return [
        {
            "jx_id": row_id,
            "component": component,
            "zero_or_bound_rule": rule,
            "status": status,
            "remaining_failure": failure,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, component, rule, status, failure in raw_rows
    ]


def gap_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("ACQ3894_0_a_min", "a_min", "positive principal-symbol lower bound", "dimensionless_or_metric_units", "prove A^ij_mem >= a_min h^ij with a_min>0", "MISSING_SIGN_CERTIFICATE"),
        ("ACQ3894_1_lambda1", "lambda_1(D)", "first eigenvalue or zero-mode removal", "1/length^2", "derive selected compact domain spectrum or boundary condition removing constant mode", "MISSING_DOMAIN_SPECTRUM"),
        ("ACQ3894_2_m_min", "m_min^2", "mass/gap lower bound", "1/length^2", "derive m_mem^2>=m_min^2>=0 or prove universal constant calibration", "MISSING_MASS_GAP"),
        ("ACQ3894_3_JX", "||J_X||", "source norm", "operator-normalized source units", "fill J_chi_wall,J_boundary,J_history or theorem-zero each", "MISSING_OPEN_COMPONENT_NORMS"),
        ("ACQ3894_4_boundary_lift", "boundary_lift_norm", "boundary memory lift", "operator-normalized boundary units", "source boundary projection coefficient or topological/no-flux zero", "MISSING_BOUNDARY_LIFT"),
        ("ACQ3894_5_X_bound", "||X_mem||", "memory amplitude bound", "X units times sqrt(volume)", MEMORY_BOUND, "FORMULA_READY_INPUTS_MISSING"),
        ("ACQ3894_6_Gdot_projection", "K_Gdot;partial_t X_mem", "Gdot memory projection", "yr^-1 per X unit", "|Delta Gdot/G| <= 9.6e-15 yr^-1", "MISSING_GDOT_PROJECTION"),
        ("ACQ3894_7_R10_PPN_projection", "K_R10;K_PPN;K_clock;K_orbital;K_WEP", "arena projections", "arena-specific", "each arena residual below bound with no cancellation credit", "MISSING_ARENA_PROJECTIONS"),
    ]
    return [
        {
            "acquisition_id": row_id,
            "needed_input": needed,
            "meaning": meaning,
            "units": units,
            "required_derivation_or_data": required,
            "current_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, needed, meaning, units, required, status in raw_rows
    ]


def gate_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("LGG3894_0_owner", "parent memory owner", MEMORY_OWNER, "PASS_CANDIDATE_BRANCH_NONCLAIM"),
        ("LGG3894_1_action", "memory operator action", MEMORY_ACTION, "PASS_CANDIDATE_BRANCH_NONCLAIM"),
        ("LGG3894_2_sign_gap", "positive sign/gap", "a_min>0 and lambda_gap=a_min lambda_1(D)+m_min^2>0", "FAIL_INPUTS_MISSING"),
        ("LGG3894_3_JX", "J_X source zero", "all J_X components zero or bounded", "PARTIAL_FAIL_BOUNDARY_HISTORY_OPEN"),
        ("LGG3894_4_boundary", "boundary/zero-mode silence", "boundary_X=0 and constant mode removed/universal", "FAIL_UNSIGNED"),
        ("LGG3894_5_projection", "observable projections", "K_i maps to R10/PPN/clock/Gdot/orbital/WEP sourced", "FAIL_MISSING"),
        ("LGG3894_6_local_GR", "local-GR promotion", "memory plus boundary/projector/R11/residual-lock close", "BLOCKED_NO_CLAIM"),
    ]
    return [
        {
            "gate_id": row_id,
            "gate": gate,
            "requirement": req,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, req, status in raw_rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("RUNU3894_0_owner", "memory_owner", "X_mem is a candidate parent variable in Yloc, but this does not imply X_mem=0", "OWNER_ONLY"),
        ("RUNU3894_1_gap", "gap_guard", "do not evaluate memory bound without a_min, lambda_1(D), and m_min^2 or a zero-mode theorem", "NO_FAKE_GAP"),
        ("RUNU3894_2_JX", "JX_guard", "only J_kin and J_matter are candidate-zero; boundary/history/domain-wall components remain live", "PARTIAL_SOURCE_ZERO"),
        ("RUNU3894_3_projection", "projection_guard", "finite X bounds are not scoreable until K_i arena maps are sourced", "NO_UNITS_NO_SCORE"),
        ("RUNU3894_4_next", "next_attack", "derive boundary/history memory zero or fill a_min/lambda1/m_min/JX/K_i numeric rows", "NEXT_3895"),
    ]
    return [
        {
            "update_id": row_id,
            "runner_field": field,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, field, rule, status in raw_rows
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3894_0",
            "target_checkpoint": "3895-Y5-R2FR-memory-boundary-history-zero-or-first-numeric-memory-row.md",
            "script": "scripts/Y5_R2FR_3895_memory_boundary_history_zero_or_first_numeric_memory_row.py",
            "objective": "try to close memory boundary/history/domain-wall sources; if not, fill the first numeric memory rows a_min, lambda_1(D), m_min^2, J_X component norms and Gdot/R10/PPN projection coefficients",
            "why_next": "3894 candidate-owns the memory variable and zeros direct/matter J_X components, leaving sign/gap plus boundary/history/domain-wall and projection inputs as the active memory blockers",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3894_0",
            "branch": BRANCH,
            "summary": "memory variable X_mem is candidate-owned as a Yloc component and direct/matter J_X components are candidate-zero, but sign/gap, boundary/history/domain-wall sources and arena projections remain unsigned; no local-GR claim",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    owner: list[dict[str, object]],
    jx: list[dict[str, object]],
    gap: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3894 - Memory Parent Owner, Gap, JX Closure or Numeric Source Acquisition

Generated: `{timestamp}`

## Result

3894 gives the memory residual a candidate parent owner without pretending the memory field is zero.

Memory owner:

`{MEMORY_OWNER}`

Memory action:

`{MEMORY_ACTION}`

Memory bound:

`{MEMORY_BOUND}`

The win: memory is no longer just an orphan diagnostic in the candidate branch. It is a `Y_loc` component with an Euler equation. The non-win: sign/gap, boundary/history/domain-wall sources, zero-mode treatment, and arena projection coefficients remain missing, so memory remains a retained residual unless those inputs are derived or sourced.

## Memory Parent Owner Insertion

{markdown_table(owner, ["owner_id", "piece", "statement_or_math", "status", "remaining_failure"])}

## Memory JX Component Closure Gate

{markdown_table(jx, ["jx_id", "component", "zero_or_bound_rule", "status", "remaining_failure"])}

## Memory Gap/Bound and Projection Acquisition

{markdown_table(gap, ["acquisition_id", "needed_input", "meaning", "units", "required_derivation_or_data", "current_status"])}

## Local-GR Decision Gate

{markdown_table(gate, ["gate_id", "gate", "requirement", "status", "claim_allowed"])}

## Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

This is progress but not victory. The memory sector now has a candidate parent home, and two `J_X` pieces are candidate-zero. The live memory fight is now finite and concrete: prove or source the sign/gap, boundary/history/domain-wall source terms, zero-mode treatment, and arena projection coefficients.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3894 MEMORY OWNER GAP JX -->"
    end = "<!-- END 3894 MEMORY OWNER GAP JX -->"
    block = f"""{start}

## 3894 - Memory parent owner/gap/JX split

Memory owner:

`{MEMORY_OWNER}`

Memory action:

`{MEMORY_ACTION}`

Memory bound:

`{MEMORY_BOUND}`

Status: X_mem is candidate-owned as a Yloc component. Direct/matter J_X components are candidate-zero; sign/gap, boundary/history/domain-wall source terms, zero-mode treatment and arena projection coefficients remain open. Memory is retained as a finite residual unless these close.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3894_MEMORY_PARENT_OWNER_INSERTION.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3894_MEMORY_JX_COMPONENT_CLOSURE_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3894_MEMORY_GAP_BOUND_AND_PROJECTION_ACQUISITION.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3894_VALIDATION.csv`

Next gate: `3895`, memory boundary/history zero or first numeric memory row.

<!-- Generated by 3894 at {timestamp} -->
{end}
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if start in existing and end in existing:
        before = existing.split(start)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        new_text = f"{before}\n\n{block}\n\n{after}".rstrip() + "\n"
    else:
        new_text = existing.rstrip() + "\n\n" + block + "\n"
    SPINE_PATH.write_text(new_text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    owner: list[dict[str, object]],
    jx: list[dict[str, object]],
    gap: list[dict[str, object]],
    gate: list[dict[str, object]],
    runner: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    checks.append(("VAL3894_0_sources", "all cited source paths exist and needles are found", resolved == len(sources), f"{resolved}/{len(sources)} sources resolved"))
    checks.append(("VAL3894_1_owner", "memory owner insertion is explicit", any("X_mem := y^memory" in str(row["statement_or_math"]) for row in owner), "OWN3894_0"))
    checks.append(("VAL3894_2_action", "memory action is explicit", any("S_mem" in str(row["statement_or_math"]) for row in owner), "OWN3894_1"))
    expected_candidate = {"J_X^kin_affine", "J_X^matter"}
    found_candidate = {str(row["component"]) for row in jx if "PASS_CANDIDATE" in str(row["status"])}
    checks.append(("VAL3894_3_candidate_JX_zero", "direct/matter JX components are candidate-zero", expected_candidate.issubset(found_candidate), f"{len(found_candidate)} candidate JX rows"))
    expected_open = {"J_X^chi_wall", "J_X^boundary", "J_X^history"}
    found_open = {str(row["component"]) for row in jx if "FAIL" in str(row["status"])}
    checks.append(("VAL3894_4_open_JX", "boundary/history/domain-wall JX components remain open", expected_open.issubset(found_open), f"{len(found_open)} open JX rows"))
    required_inputs = {"a_min", "lambda_1(D)", "m_min^2", "||J_X||", "boundary_lift_norm", "||X_mem||", "K_Gdot;partial_t X_mem", "K_R10;K_PPN;K_clock;K_orbital;K_WEP"}
    found_inputs = {str(row["needed_input"]) for row in gap}
    checks.append(("VAL3894_5_acquisition", "gap/source/projection acquisition rows exist", required_inputs.issubset(found_inputs), f"{len(found_inputs)} acquisition rows"))
    checks.append(("VAL3894_6_local_gr_no_claim", "local GR remains blocked", any(row["gate_id"] == "LGG3894_6_local_GR" and "BLOCKED" in str(row["status"]) for row in gate), "LGG3894_6"))
    checks.append(("VAL3894_7_all_nonclaim", "all generated analytic rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [owner, jx, gap, gate, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3894_8_runner", "runner forbids fake gap", any(row["runner_field"] == "gap_guard" and "a_min" in str(row["rule"]) for row in runner), "RUNU3894_1"))
    checks.append(("VAL3894_9_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "memory sector now has a candidate parent home" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3894_10_spine", "spine updated with 3894 block", SPINE_PATH.exists() and "BEGIN 3894 MEMORY OWNER GAP JX" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3894_11_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    if FWB.exists():
        formalization_hits = [path for path in FWB.rglob("*3894*") if path.is_file() and ("3894-Y5" in path.name or "P8_Y5_R2FR_3894" in path.name or "P8_Y5_BRR545_3894" in path.name)]
    checks.append(("VAL3894_12_formalization_untouched", "no generated 3894 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3894_13_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3894_14_next_target", "next target attacks memory boundary/history or numeric memory row", any("memory-boundary-history" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3895 memory boundary/history"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    owner = owner_rows(timestamp)
    jx = jx_rows(timestamp)
    gap = gap_rows(timestamp)
    gate = gate_rows(timestamp)
    runner = runner_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["owner"], owner)
    write_csv(OUTPUTS["jx"], jx)
    write_csv(OUTPUTS["gap"], gap)
    write_csv(OUTPUTS["gate"], gate)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, owner, jx, gap, gate, runner, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, owner, jx, gap, gate, runner, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_MEMORY_OWNER_CANDIDATE_GAP_JX_OPEN")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
