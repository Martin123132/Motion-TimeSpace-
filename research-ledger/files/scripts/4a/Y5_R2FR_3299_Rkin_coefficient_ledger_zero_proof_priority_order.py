from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3299-Y5-R2FR-Rkin-coefficient-ledger-zero-proof-priority-order-under-AX1090.md"

SRC_3298_DOC = ROOT / "3298-Y5-R2FR-Rkin-coefficient-source-sweep-and-zero-gate-under-AX1090.md"
SRC_3298_NEXT = OUT / "P8_Y5_R2FR_3298_NEXT_TARGET.csv"
SRC_3298_SWEEP = OUT / "P8_Y5_R2FR_3298_RKIN_COEFFICIENT_SOURCE_SWEEP.csv"
SRC_3298_GATE = OUT / "P8_Y5_R2FR_3298_COEFFICIENT_ZERO_OR_SOURCE_GATE.csv"
SRC_3298_VALIDATION = OUT / "P8_Y5_BRR545_3298_VALIDATION.csv"
SRC_3297_BASIS = OUT / "P8_Y5_R2FR_3297_FIRST_RKIN_COEFFICIENT_BASIS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3299_SOURCE_REGISTER.csv",
    "priority": OUT / "P8_Y5_R2FR_3299_RKIN_PRIORITY_LEDGER.csv",
    "zero_routes": OUT / "P8_Y5_R2FR_3299_ZERO_PROOF_ROUTE_LEDGER.csv",
    "finite_routes": OUT / "P8_Y5_R2FR_3299_FINITE_SOURCE_ROUTE_LEDGER.csv",
    "arena": OUT / "P8_Y5_R2FR_3299_FIRST_BOUND_ARENA_LEDGER.csv",
    "runner": OUT / "P8_Y5_R2FR_3299_PRIORITY_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3299_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3299_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3299_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3299_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()

PRIORITY_SPEC = {
    "c_R2": {
        "priority_rank": 1,
        "cluster": "curvature_squared",
        "why_first": "one curvature-linear/second-order parent syntax theorem can zero c_R2 and c_Ric together; failure maps directly to Yukawa/PPN/orbital tests",
        "zero_route": "prove parent kinetic grammar permits only A R + B plus silent boundary/topological terms; equivalently no bulk R^2/f(R) operator in local branch",
        "finite_route": "derive c_R2 normalization and scalar-mode range/amplitude, then map to alpha_0/lambda_0 Yukawa plus PPN gamma/beta",
        "first_bound_arena": "R10/Yukawa plus solar-system PPN",
        "missing_parent_input": "curvature-linear kinetic grammar or c_R2 coefficient with units",
    },
    "c_Ric": {
        "priority_rank": 2,
        "cluster": "curvature_squared",
        "why_first": "same parent syntax theorem as c_R2; generic Ricci/Weyl terms create spin-2/high-derivative local gravity residuals",
        "zero_route": "prove no independent Ricci^2/Weyl^2 bulk operator except exact silent topological combination",
        "finite_route": "derive c_Ric/c_Weyl normalization and massive spin-2 range/amplitude, then map to light-bending/orbital/Yukawa signatures",
        "first_bound_arena": "solar-system PPN and orbital precession; R10/Yukawa if finite range",
        "missing_parent_input": "Ricci/Weyl operator exclusion or coefficient with units",
    },
    "delta_A": {
        "priority_rank": 3,
        "cluster": "common_G_silence",
        "why_first": "local GR can tolerate calibrated G, but not hidden/time/range/source drift in the Einstein coefficient",
        "zero_route": "prove A is one q-basic universal constant in the local branch, independent of hidden variables, source composition, time, range, and frame",
        "finite_route": "derive derivatives of A(x,I_hid) and project to Gdot, fifth-force range dependence, and source/environment drift",
        "first_bound_arena": "Gdot/orbital ephemerides plus WEP/source tests",
        "missing_parent_input": "q-basic Einstein coefficient theorem or A drift coefficients",
    },
    "c_mem": {
        "priority_rank": 4,
        "cluster": "memory_locality",
        "why_first": "MTS has memory/cosmology motivation, so local memory silence cannot be assumed",
        "zero_route": "prove local memory kernel collapses to constant Lambda/G_cal or is exponentially/screened silent in local vacuum",
        "finite_route": "derive K_memory local kernel and project to G_eff(t,r,environment)",
        "first_bound_arena": "orbital ephemerides, Gdot, clocks, and environment/range tests",
        "missing_parent_input": "local memory separation theorem or kernel with units",
    },
    "c_phi": {
        "priority_rank": 5,
        "cluster": "extra_scalar",
        "why_first": "hidden scalar branch overlaps fifth-force/WEP/R10 constraints and local source coupling",
        "zero_route": "prove scalar is gauge/auxiliary/q-basic constant or infinitely massive in local branch",
        "finite_route": "derive scalar kinetic norm, mass/range, and Hilbert-source coupling beta_phi",
        "first_bound_arena": "R10/Yukawa, WEP, Gdot, PPN gamma",
        "missing_parent_input": "scalar lane closure or mass/coupling coefficients",
    },
    "c_VT": {
        "priority_rank": 6,
        "cluster": "frame_connection",
        "why_first": "vector/torsion/frame terms hit preferred-frame PPN and can break local Lorentz/source universality",
        "zero_route": "prove connection is Levi-Civita and frame/torsion/vector variables are gauge, auxiliary, or silent",
        "finite_route": "derive vector/torsion kinetic coefficients and matter spin/source couplings",
        "first_bound_arena": "preferred-frame PPN alpha_i, spin/torsion, gravitational-wave polarization",
        "missing_parent_input": "Levi-Civita/coframe descent theorem or vector/torsion coefficients",
    },
    "c_top": {
        "priority_rank": 7,
        "cluster": "boundary_topological",
        "why_first": "topological terms are often locally harmless, but only if coefficients are constant/uncoupled and boundary flux is silent",
        "zero_route": "prove topological/boundary coefficients are constant and uncoupled in the 4D local branch with harmless boundary variation",
        "finite_route": "derive coupling gradient or boundary/domain map and project to spin/parity/orbital precession",
        "first_bound_arena": "spin/precession/orbital parity tests",
        "missing_parent_input": "topological coefficient silence theorem or boundary/domain coefficient",
    },
}


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 540) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def evidence_hits(path: Path, needles: list[str], limit: int = 5) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    for idx, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered):
            hits.append(f"L{idx}:{compact(line, 340)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    snapshot: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            stat = item.stat()
            snapshot[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3298_DOC, "3298 source sweep handoff", ["No R_kin coefficient is promoted", "coefficient debt"]),
        (SRC_3298_NEXT, "3298 next target", ["Rkin-coefficient-ledger", "priority"]),
        (SRC_3298_SWEEP, "3298 sweep table", ["c_R2", "delta_A"]),
        (SRC_3298_GATE, "3298 zero/source gate", ["BLOCKED_MIXED_LANGUAGE_NEEDS_ADJUDICATION", "c_Ric"]),
        (SRC_3298_VALIDATION, "3298 validation", ["VAL3298_11_overall", "true"]),
        (SRC_3297_BASIS, "3297 coefficient basis", ["BAS3297_0_R2_scalar", "BAS3297_6_Einstein_coefficient_drift"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3299_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def priority_rows() -> list[dict[str, Any]]:
    sweep_by_coeff = {row["coefficient"]: row for row in read_csv(SRC_3298_SWEEP)}
    gate_by_coeff = {row["coefficient"]: row for row in read_csv(SRC_3298_GATE)}
    rows: list[dict[str, Any]] = []
    for coeff, spec in sorted(PRIORITY_SPEC.items(), key=lambda item: item[1]["priority_rank"]):
        sweep = sweep_by_coeff.get(coeff, {})
        gate = gate_by_coeff.get(coeff, {})
        rows.append(
            {
                "priority_rank": spec["priority_rank"],
                "coefficient": coeff,
                "cluster": spec["cluster"],
                "sweep_status": sweep.get("status", "MISSING_SWEEP_ROW"),
                "gate_status": gate.get("gate_status", "MISSING_GATE_ROW"),
                "why_this_priority": spec["why_first"],
                "missing_parent_input": spec["missing_parent_input"],
                "valid_for_claim": "false",
            }
        )
    return rows


def zero_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "coefficient": coeff,
            "priority_rank": spec["priority_rank"],
            "zero_proof_route": spec["zero_route"],
            "proof_type": "shared_curvature_linear" if spec["cluster"] == "curvature_squared" else "sector_specific_silence",
            "current_status": "NOT_PARENT_SIGNED",
            "valid_for_claim": "false",
        }
        for coeff, spec in sorted(PRIORITY_SPEC.items(), key=lambda item: item[1]["priority_rank"])
    ]


def finite_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "coefficient": coeff,
            "priority_rank": spec["priority_rank"],
            "finite_source_route": spec["finite_route"],
            "required_before_scoring": "coefficient value or symbolic expression; units; source path; linearized projection; bound source",
            "current_status": "MISSING_NUMERIC_OR_SYMBOLIC_PARENT_COEFFICIENT",
            "valid_for_claim": "false",
        }
        for coeff, spec in sorted(PRIORITY_SPEC.items(), key=lambda item: item[1]["priority_rank"])
    ]


def arena_rows() -> list[dict[str, Any]]:
    return [
        {
            "coefficient": coeff,
            "priority_rank": spec["priority_rank"],
            "first_bound_arena": spec["first_bound_arena"],
            "why_arena": "chosen for highest sensitivity to the leading weak-field signature of this coefficient",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        }
        for coeff, spec in sorted(PRIORITY_SPEC.items(), key=lambda item: item[1]["priority_rank"])
    ]


def runner_rows(priority: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rank_ok = [int(row["priority_rank"]) for row in priority] == list(range(1, len(PRIORITY_SPEC) + 1))
    all_blocked = all(row["valid_for_claim"] == "false" for row in priority)
    return [
        {
            "run_id": "RUN3299_0_rank_order",
            "check": "priority ranks are complete and ordered",
            "observed_status": "PASS_NONCLAIM" if rank_ok else "FAIL_RANKS",
            "expectation_match": bool_str(rank_ok),
            "claim_allowed": "false",
        },
        {
            "run_id": "RUN3299_1_all_nonclaim",
            "check": "all coefficient priorities remain nonclaim",
            "observed_status": "REFUSE_CLAIM_NONCLAIM" if all_blocked else "FAIL_GATE",
            "expectation_match": bool_str(all_blocked),
            "claim_allowed": "false",
        },
        {
            "run_id": "RUN3299_2_top_target_curvature",
            "check": "top target is curvature-squared shared zero proof",
            "observed_status": "PASS_NONCLAIM" if priority[0]["cluster"] == "curvature_squared" else "FAIL_TOP_TARGET",
            "expectation_match": bool_str(priority[0]["cluster"] == "curvature_squared"),
            "claim_allowed": "false",
        },
    ]


def promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3299_0_priority_ledger_complete",
            "gate": "every R_kin coefficient has priority, zero route, finite route, and first arena",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "ledger is actionable but not evidential proof.",
        },
        {
            "gate_id": "GATE3299_1_any_coefficient_closed",
            "gate": "any coefficient theorem-zero or finite sourced",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "3299 ranks work; it does not close coefficients.",
        },
        {
            "gate_id": "GATE3299_2_local_GR_kinetic_claim",
            "gate": "local-GR kinetic side claimed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "claim remains blocked until c_R2/c_Ric/etc. are zero or bounded.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3299_0_priority_result",
            "finding": "Top priority is the curvature-squared pair c_R2/c_Ric because one parent curvature-linear syntax theorem can close both.",
            "consequence": "next derivation should attack bulk R^2/Ricci^2/Weyl^2 exclusion, not scatter across all coefficients.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3299_1_testing_result",
            "finding": "If the curvature-linear proof fails, c_R2/c_Ric already have a first finite test route through Yukawa/PPN/orbital signatures.",
            "consequence": "failure becomes test work rather than a dead end.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3299_2_remaining_order",
            "finding": "After curvature-squared, priority is delta_A, c_mem, c_phi, c_VT, then c_top.",
            "consequence": "this order protects the local-GR common-G and memory-sensitive branches before lower-priority boundary/topological leakage.",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3299_0_3300",
            "target_doc": "3300-Y5-R2FR-curvature-squared-zero-proof-or-Yukawa-basis-fill-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3300_curvature_squared_zero_proof_or_Yukawa_basis_fill.py",
            "objective": "attack c_R2/c_Ric directly: prove parent kinetic syntax excludes bulk R^2/Ricci^2/Weyl^2 terms, or fill the first Yukawa/PPN/orbital coefficient basis without claiming a pass.",
            "guardrails": "do not use Lovelock theorem unless second-order/curvature-linear syntax is parent-signed; do not set c_R2/c_Ric to zero by taste; do not use Yukawa placeholders as predictions.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    priority: list[dict[str, Any]],
    zero_routes: list[dict[str, Any]],
    finite_routes: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    formalization_changed_count: int,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append({"check_id": check_id, "check": check, "passed": bool_str(passed), "detail": detail})

    add("VAL3299_0_sources_exist", "all cited source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3299_1_sources_parse", "all cited source paths parse", all(row["parse_ok"] == "true" for row in sources))
    add("VAL3299_2_outputs_parse", "all 3299 non-validation output CSVs parse", all(csv_parse_ok(path) for key, path in OUTPUTS.items() if key != "validation"))

    coeffs = set(PRIORITY_SPEC)
    add("VAL3299_3_priority_complete", "priority ledger covers all coefficients", {row["coefficient"] for row in priority} == coeffs)
    add("VAL3299_4_zero_routes_complete", "zero route ledger covers all coefficients", {row["coefficient"] for row in zero_routes} == coeffs)
    add("VAL3299_5_finite_routes_complete", "finite route ledger covers all coefficients", {row["coefficient"] for row in finite_routes} == coeffs)
    add("VAL3299_6_arenas_complete", "first bound arena ledger covers all coefficients", {row["coefficient"] for row in arenas} == coeffs)
    add(
        "VAL3299_7_top_priority_curvature_squared",
        "top two coefficients are c_R2 and c_Ric in curvature-squared cluster",
        [row["coefficient"] for row in priority[:2]] == ["c_R2", "c_Ric"] and all(row["cluster"] == "curvature_squared" for row in priority[:2]),
    )
    add("VAL3299_8_runner_expectations", "runner expectations all match", all(row["expectation_match"] == "true" for row in runner), ";".join(f"{row['run_id']}={row['observed_status']}" for row in runner))
    add("VAL3299_9_claim_gates_false", "no 3299 gate allows local GR/R_kin claim", all(row["claim_allowed"] == "false" for row in promotion))
    add(
        "VAL3299_10_next_target_curvature_squared",
        "next target focuses curvature-squared zero proof or Yukawa basis",
        len(next_target) == 1 and "curvature-squared-zero-proof" in next_target[0]["target_doc"],
    )
    add(
        "VAL3299_11_formalization_untouched",
        "formalization-workbench modified-file count remains zero by this script",
        formalization_changed_count == 0,
        f"formalization_changed_count={formalization_changed_count}",
    )
    overall = all(row["passed"] == "true" for row in checks)
    add("VAL3299_12_overall", "3299 validation overall", overall, "all required checks passed" if overall else "one or more checks failed")
    return checks


def md_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, Any]],
    priority: list[dict[str, Any]],
    zero_routes: list[dict[str, Any]],
    finite_routes: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 3299 - R_kin coefficient ledger zero-proof priority order under AX1090

**Run UTC:** {RUN_UTC}

3299 converts the 3298 sweep into an action order. It does not promote any coefficient.

Top priority is `c_R2/c_Ric`: one parent kinetic syntax theorem can kill both. If that proof fails, the fallback is already finite and test-shaped: Yukawa/PPN/orbital signatures.

## Source Register

{md_table(sources)}

## R_kin Priority Ledger

{md_table(priority)}

## Zero-Proof Route Ledger

{md_table(zero_routes)}

## Finite-Source Route Ledger

{md_table(finite_routes)}

## First Bound Arena Ledger

{md_table(arenas)}

## Nonclaim Runner

{md_table(runner)}

## Promotion Gates

{md_table(promotion)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    before_fw = snapshot_tree(FW)

    sources = source_register_rows()
    priority = priority_rows()
    zero_routes = zero_route_rows()
    finite_routes = finite_route_rows()
    arenas = arena_rows()
    runner = runner_rows(priority)
    promotion = promotion_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["priority"], priority)
    write_csv(OUTPUTS["zero_routes"], zero_routes)
    write_csv(OUTPUTS["finite_routes"], finite_routes)
    write_csv(OUTPUTS["arena"], arenas)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    after_fw = snapshot_tree(FW)
    validation = validate(sources, priority, zero_routes, finite_routes, arenas, runner, promotion, decisions, next_target, changed_count(before_fw, after_fw))
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, priority, zero_routes, finite_routes, arenas, runner, promotion, decisions, next_target, validation)

    if PYCACHE.exists():
        for item in PYCACHE.iterdir():
            if item.is_file():
                item.unlink()
        try:
            PYCACHE.rmdir()
        except OSError:
            pass


if __name__ == "__main__":
    main()
