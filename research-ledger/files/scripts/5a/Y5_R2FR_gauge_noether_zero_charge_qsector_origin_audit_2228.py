from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "2228-Y5-R2FR-gauge-noether-zero-charge-qsector-origin-audit.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_GAUGE_NOETHER_ZERO_CHARGE_2228"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2227_doc": ROOT / "2227-Y5-R2FR-phase-volume-nonpropagating-qsector-origin-or-rejection.md",
    "2227_validation": OUT / "P8_Y5_BRR545_2227_VALIDATION.csv",
    "2227_next": OUT / "P8_Y5_PARENT_QLOC_2227_NEXT_TARGET.csv",
    "1555_doc": ROOT / "1555-Y5-gauge-noether-zero-charge-qsector-origin-audit.md",
    "1555_validation": OUT / "P8_Y5_BRR545_1555_VALIDATION.csv",
    "1555_route": OUT / "P8_Y5_PARENT_QLOC_1555_GAUGE_NOETHER_ROUTE_AUDIT.csv",
    "1555_contract": OUT / "P8_Y5_PARENT_QLOC_1555_FIRST_CLASS_CONSTRAINT_CONTRACT.csv",
    "1555_runner": OUT / "P8_Y5_PARENT_QLOC_1555_ZERO_CHARGE_RUNNER_NONCLAIM.csv",
    "1555_closure": OUT / "P8_Y5_PARENT_QLOC_1555_LOCAL_CLOSURE_LEDGER.csv",
    "1555_decision": OUT / "P8_Y5_PARENT_QLOC_1555_DECISION.csv",
    "1555_next": OUT / "P8_Y5_PARENT_QLOC_1555_NEXT_TARGET.csv",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2228_SOURCE_REGISTER.csv"
ROUTE_AUDIT = OUT / "P8_Y5_PARENT_QLOC_2228_GAUGE_NOETHER_ROUTE_AUDIT.csv"
FIRST_CLASS_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_2228_FIRST_CLASS_CONSTRAINT_CONTRACT.csv"
ZERO_CHARGE_RUNNER = OUT / "P8_Y5_PARENT_QLOC_2228_ZERO_CHARGE_RUNNER_NONCLAIM.csv"
LOCAL_CLOSURE_LEDGER = OUT / "P8_Y5_PARENT_QLOC_2228_LOCAL_CLOSURE_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_2228_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2228_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2228_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2228_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2228_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2228_GAUGE_NOETHER_ZERO_CHARGE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "gauge_noether_zero_charge_nonclaim_2228.csv",
    "beta_docs": BETA_DOCS / "GAUGE_NOETHER_ZERO_CHARGE_2228_NONCLAIM.csv",
}


GENERATED = [
    SOURCE_REGISTER,
    ROUTE_AUDIT,
    FIRST_CLASS_CONTRACT,
    ZERO_CHARGE_RUNNER,
    LOCAL_CLOSURE_LEDGER,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
    BRANCH_COPIES,
    VALIDATION,
]


def flags() -> dict[str, bool]:
    return {
        "theorem_zero_adopted": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key) == "PASS" for row in overall_rows)
    return all(row.get(result_key) == "PASS" for row in rows)


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    keys = [
        "theorem_zero_adopted",
        "numeric_value_present",
        "source_backed",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_2228_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and "2228" in path.name for path in FORMALIZATION.rglob("*"))


def formalization_untouched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*"))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        role = "current phase-volume handoff" if key.startswith("2227") else "older gauge/Noether zero-charge evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2228_{index}_{key}",
                "source_path": rel(path),
                "path_exists": path.exists(),
                "validation_overall_pass": validation_pass(path) if key.endswith("validation") else "",
                "role": role,
                **flags(),
            }
        )
    return rows


def route_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "GAUGE2228_0_radial_coordinate_gauge",
            "radial coordinate gauge",
            "use radial coordinate freedom to set T^2 S=1",
            "REJECTED_COORDINATE_IMPORT",
            "areal radius fixes r by sphere area; using this as AB=1 imports GR-like gauge logic",
        ),
        (
            "GAUGE2228_1_cell_scale_gauge",
            "cell-scale gauge",
            "treat T sqrt(S) as pure observer-splitting gauge",
            "REJECTED_OBSERVABLE_CHANGE",
            "T and S are clock/routing observables unless a new matter map proves otherwise",
        ),
        (
            "GAUGE2228_2_reciprocal_split_gauge",
            "reciprocal split gauge",
            "T -> exp(sigma)T and sqrt(S)->exp(-sigma)sqrt(S)",
            "REJECTED_IRRELEVANT_TO_RAB",
            "this leaves T sqrt(S) unchanged and cannot impose R_AB=0",
        ),
        (
            "GAUGE2228_3_noether_identity",
            "generic Noether identity",
            "use symmetry identity to force R_AB=0",
            "REJECTED_IDENTITY_NOT_CONSTRAINT",
            "Noether identities relate equations; they do not set a field to zero without a constraint equation",
        ),
        (
            "GAUGE2228_4_first_class_constraint",
            "first-class parent constraint",
            "parent action supplies C_R=R_AB with proper/zero boundary charge and degree-count closure",
            "POSSIBLE_IN_PRINCIPLE_NOT_PRESENT",
            "requires parent symplectic potential, generator, Q_R boundary term, bracket closure, and degree count",
        ),
        (
            "GAUGE2228_5_current_verdict",
            "accepted gauge/Noether zero-charge origin",
            "derive Q_R=0 and R_AB=0 without importing GR",
            "NO_ACCEPTED_ORIGIN",
            "all current routes are rejected or future-contract only",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "route": route,
            "test": test,
            "result": result,
            "reason": reason,
            **flags(),
        }
        for route_id, route, test, result, reason in entries
    ]


def first_class_rows() -> list[dict[str, Any]]:
    entries = [
        ("FCC2228_0_parent_phase_space", "parent phase space", "fields, symplectic potential, and boundary variables include q/R_AB sector", "MISSING"),
        ("FCC2228_1_constraint", "constraint equation", "C_R=0 or equivalent must contain R_AB=ln(T^2 S) as a primary/secondary constraint", "MISSING"),
        ("FCC2228_2_generator", "differentiable generator", "delta G_R[epsilon]=Omega(delta Phi,v_epsilon), G_R=int epsilon C_R+Q_R", "MISSING"),
        ("FCC2228_3_boundary_charge", "zero/proper boundary charge", "Q_R is zero, exact, or proper on local branch without deleting physical mass/time charges", "MISSING"),
        ("FCC2228_4_bracket_closure", "first-class algebra", "constraint bracket closes with no anomaly/central edge cocycle", "MISSING"),
        ("FCC2228_5_degree_count", "degree count", "constraint removes reciprocal strain pair rather than hiding a physical mode", "MISSING"),
        ("FCC2228_6_matter_map", "matter/readout map", "matter observables descend through the constrained observer split without shadow frames", "MISSING"),
        ("FCC2228_7_no_GR_import", "no GR import", "proof does not use Schwarzschild AB=1 or Einstein vacuum equations", "PASS_GUARD_NONCLAIM"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "needed_object": needed_object,
            "acceptance_requirement": requirement,
            "current_status": status,
            **flags(),
        }
        for contract_id, needed_object, requirement, status in entries
    ]


def runner_rows() -> list[dict[str, Any]]:
    entries = [
        ("RUN2228_0_coordinate", "coordinate gauge sets R_AB=0", "REFUSED_COORDINATE_IMPORT", "areal scaffold already fixes radial coordinate"),
        ("RUN2228_1_observer_split", "observer split gauge sets R_AB=0", "REFUSED_OBSERVABLE_CHANGE", "requires new matter map not present"),
        ("RUN2228_2_noether", "Noether identity sets R_AB=0", "REFUSED_IDENTITY_NOT_CONSTRAINT", "identity is not a constraint equation"),
        ("RUN2228_3_current", "cell current conservation sets Q_R=0", "REFUSED_NO_CHARGE_OBSTRUCTION", "current gives constant Q_R not zero"),
        ("RUN2228_4_first_class", "first-class parent constraint exists", "REFUSED_MISSING_PARENT_CONSTRAINT", "contract is known but not supplied"),
        ("RUN2228_5_closure", "closure benchmark status", "PASS_NONCLAIM", "R_AB=0 may be used only as explicit benchmark closure"),
        ("RUN2228_6_score_status", "local GR/Newton claim", "REFUSED_NOT_SCORE_READY", "no gauge/Noether zero-charge origin closes"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "check": check,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for runner_id, check, status, reason in entries
    ]


def closure_rows() -> list[dict[str, Any]]:
    entries = [
        ("CL2228_0_closure_statement", "explicit local closure", "assume R_AB=ln(T^2 S)=0 only as a benchmark closure", "ALLOWED_NONCLAIM"),
        ("CL2228_1_what_it_tests", "test use", "separate whether MTS can match local PPN/solar-system conditions under the closure", "BENCHMARK_ONLY"),
        ("CL2228_2_what_it_does_not_prove", "derivation limit", "does not prove parent q-sector, zero charge, q-norm, beta, conservation, or matter universality", "LIMIT_EXPLICIT"),
        ("CL2228_3_no_public_claim", "claim policy", "do not advertise local GR/Newton reduction as derived from this branch", "PASS_GUARD_NONCLAIM"),
        ("CL2228_4_reentry", "future reentry", "only a first-class constraint/no-charge theorem can promote closure to derivation", "REENTRY_CONTRACT"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "closure_id": closure_id,
            "item": item,
            "statement": statement,
            "current_status": status,
            **flags(),
        }
        for closure_id, item, statement, status in entries
    ]


def claim_rows() -> list[dict[str, Any]]:
    entries = [
        ("CG2228_0_route_audit", "gauge/Noether route audit", "PASS_NONCLAIM", "route failures and first-class contract are explicit"),
        ("CG2228_1_coordinate_gauge", "coordinate gauge derivation", "BLOCKED_REJECTED", "would import GR-like areal gauge logic"),
        ("CG2228_2_observer_gauge", "observer split gauge derivation", "BLOCKED_REJECTED", "T and S remain observable without a new matter map"),
        ("CG2228_3_noether_identity", "Noether identity zero", "BLOCKED_REJECTED", "identity is not a constraint equation"),
        ("CG2228_4_first_class_constraint", "first-class zero-charge theorem", "BLOCKED", "parent phase space/generator/boundary charge/bracket/degree count missing"),
        ("CG2228_5_closure_benchmark", "R_AB=0 closure benchmark", "PASS_NONCLAIM", "allowed only as explicit benchmark, not derivation"),
        ("CG2228_6_local_GR", "derived GR/Newton/PPN recovery", "BLOCKED_NO_CLAIM", "zero-charge origin remains missing"),
        ("CG2228_7_GitHub", "public/GitHub update", "BLOCKED_NONCLAIM", "private proof line remains mid-derivation"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in entries
    ]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        (
            "DEC2228_0_result",
            "Gauge/Noether zero-charge origin is not derived.",
            "NO_ACCEPTED_ZERO_CHARGE_ORIGIN",
            "coordinate, cell-scale, reciprocal split, Noether, and current routes all fail",
        ),
        (
            "DEC2228_1_contract",
            "Retain first-class constraint as the only honest promotion route.",
            "FIRST_CLASS_CONTRACT_ONLY",
            "a real parent generator with zero/proper boundary charge could still derive closure, but it is not supplied",
        ),
        (
            "DEC2228_2_closure",
            "Use R_AB=0 only as an explicit local closure benchmark.",
            "CLOSURE_BENCHMARK_NEXT",
            "this preserves empirical testing without overclaiming derivation",
        ),
        (
            "DEC2228_3_next",
            "Move to local closure PPN benchmark.",
            "NEXT_2229_LOCAL_CLOSURE_PPN",
            "compute what the closure would need for gamma, beta, conservation, and matter universality",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in entries
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2228_0_2229",
            "target_file": "2229-Y5-R2FR-local-closure-PPN-benchmark-and-derived-vs-assumed-ledger.md",
            "target_script": "scripts/Y5_R2FR_local_closure_PPN_benchmark_and_derived_vs_assumed_ledger_2229.py",
            "objective": "formalize the honest R_AB=0 closure benchmark and separate derived, assumed, and test-required PPN/Newton conditions",
            "success_condition": "closure benchmark states exactly what follows from R_AB=0, what remains assumed, and what must be tested for gamma, beta, conservation and matter universality",
            "do_not": "do not claim the closure is derived; do not skip beta/conservation/matter-universality gates; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target in COPY_TARGETS.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(FIRST_CLASS_CONTRACT, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(FIRST_CLASS_CONTRACT),
                "target_path": rel(target),
                "copied": target.exists(),
                "parse_ok": parse_csv(target),
                **flags(),
            }
        )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    source: list[dict[str, Any]],
    route: list[dict[str, Any]],
    first_class: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    closure: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2228 - Y5/R2FR Gauge/Noether Zero-Charge q-sector Origin Audit",
            "## Verdict\n"
            "- 2228 imports the old `1555` gauge/Noether zero-charge audit into the current R2FR line.\n"
            "- Coordinate gauge is rejected: using radial freedom to impose `T^2 S=1` would import GR-like areal gauge logic rather than derive MTS closure.\n"
            "- Observer-split gauge is rejected unless a new matter/readout map proves `T` and `S` are not physical observables.\n"
            "- Generic Noether identity and cell-current conservation fail: identities are not constraints, and current conservation leaves a constant `Q_R` hair unless a no-charge theorem kills it.\n"
            "- Only a parent first-class constraint with zero/proper boundary charge could promote `R_AB=0` from closure to derivation; that structure is not present yet.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Gauge/Noether Route Audit\n"
            + md_table(route, ["route_id", "route", "test", "result", "reason"]),
            "## First-Class Constraint Contract\n"
            + md_table(first_class, ["contract_id", "needed_object", "acceptance_requirement", "current_status"]),
            "## Zero-Charge Runner\n"
            + md_table(runner, ["runner_id", "check", "current_status", "reason"]),
            "## Local Closure Ledger\n"
            + md_table(closure, ["closure_id", "item", "statement", "current_status"]),
            "## Claim Gate\n"
            + md_table(claim, ["gate_id", "claim", "status", "reason"]),
            "## Decision Ledger\n"
            + md_table(decision, ["decision_id", "decision", "result", "rationale"]),
            "## Next Target\n"
            + md_table(next_target, ["next_id", "target_file", "target_script", "objective", "success_condition", "do_not"]),
            "## Branch Copies\n"
            + md_table(copies, ["copy_id", "source_path", "target_path", "copied", "parse_ok"]),
            "## Validation\n"
            + md_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\n"
            "This is the point where the local route becomes honest enough to benchmark. We did not derive `R_AB=0`; the proposed gauge/Noether shortcuts fail. But we now know the exact promotion contract: a parent phase space, first-class reciprocal constraint, differentiable generator, zero/proper `Q_R` boundary charge, bracket closure, degree count, and matter map. Until that exists, `R_AB=0` can be used only as an explicit local PPN closure benchmark.",
            "",
        ]
    )


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2228_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) else "FAIL",
            "detail": "all cited 2228 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2228_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2227_validation"]) and validation_pass(SOURCE_FILES["1555_validation"]) else "FAIL",
            "detail": "2227 and 1555 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2228_02_no_origin",
            "result": "PASS" if any(row["result"] == "NO_ACCEPTED_ORIGIN" for row in read_csv(ROUTE_AUDIT)) else "FAIL",
            "detail": "gauge/Noether audit records no accepted zero-charge origin",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2228_03_first_class_contract",
            "result": "PASS" if len(read_csv(FIRST_CLASS_CONTRACT)) >= 8 else "FAIL",
            "detail": "first-class zero-charge contract written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2228_04_runner_refuses_claim",
            "result": "PASS" if any(row["current_status"] == "REFUSED_NOT_SCORE_READY" for row in read_csv(ZERO_CHARGE_RUNNER)) else "FAIL",
            "detail": "zero-charge runner refuses local claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2228_05_closure_ledger",
            "result": "PASS" if any(row["current_status"] == "ALLOWED_NONCLAIM" for row in read_csv(LOCAL_CLOSURE_LEDGER)) else "FAIL",
            "detail": "closure benchmark ledger written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2228_06_claim_gates_block",
            "result": "PASS" if all("BLOCKED" in row["status"] or row["status"].startswith("PASS") for row in read_csv(CLAIM_GATE)) else "FAIL",
            "detail": "GR/Newton and public claims remain blocked/nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2228_07_decision_next",
            "result": "PASS" if any(row["result"] == "NEXT_2229_LOCAL_CLOSURE_PPN" for row in read_csv(DECISION)) else "FAIL",
            "detail": "decision selects local closure PPN benchmark next",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2228_08_next_target",
            "result": "PASS" if read_csv(NEXT_TARGET)[0]["target_file"].startswith("2229-Y5-R2FR-local-closure-PPN") else "FAIL",
            "detail": "next target is current-numbered local closure PPN benchmark",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2228_09_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2228 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2228_10_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated flags remain nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2228_11_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch copies written and parse",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2228_12_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2228_13_formalization_no_2228",
            "result": "PASS" if formalization_2228_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no 2228 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2228_14_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2228 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2228_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2228 imports the gauge/Noether zero-charge audit, rejects shortcut origins, keeps first-class constraint as the promotion contract, and selects local closure PPN benchmark next",
        }
    )
    return rows


def main() -> None:
    source = source_rows()
    route = route_rows()
    first_class = first_class_rows()
    runner = runner_rows()
    closure = closure_rows()
    claim = claim_rows()
    decision = decision_rows()
    next_target = next_rows()

    write_csv(SOURCE_REGISTER, source)
    write_csv(ROUTE_AUDIT, route)
    write_csv(FIRST_CLASS_CONTRACT, first_class)
    write_csv(ZERO_CHARGE_RUNNER, runner)
    write_csv(LOCAL_CLOSURE_LEDGER, closure)
    write_csv(CLAIM_GATE, claim)
    write_csv(DECISION, decision)
    write_csv(NEXT_TARGET, next_target)
    copies = copy_rows()
    write_csv(BRANCH_COPIES, copies)

    remove_pycache()
    generated_before_validation = [path for path in GENERATED if path != VALIDATION]
    validation = validation_rows(generated_before_validation)
    write_csv(VALIDATION, validation)
    remove_pycache()

    DOC.write_text(
        build_doc(
            source,
            route,
            first_class,
            runner,
            closure,
            claim,
            decision,
            next_target,
            copies,
            validation,
        ),
        encoding="utf-8",
    )

    if not validation_pass(VALIDATION):
        raise SystemExit(f"2228 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
