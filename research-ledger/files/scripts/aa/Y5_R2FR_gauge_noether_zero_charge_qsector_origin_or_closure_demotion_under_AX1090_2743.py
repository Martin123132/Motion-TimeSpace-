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

DOC = ROOT / "2743-Y5-R2FR-gauge-noether-zero-charge-qsector-origin-or-closure-demotion-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2743_SOURCE_REGISTER.csv",
    "routes": RESIDUALS / "P8_Y5_R2FR_2743_GAUGE_NOETHER_ROUTE_AUDIT.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_2743_FIRST_CLASS_CONSTRAINT_CONTRACT.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2743_ZERO_CHARGE_RUNNER_NONCLAIM.csv",
    "closure": RESIDUALS / "P8_Y5_R2FR_2743_LOCAL_CLOSURE_LEDGER.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2743_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2743_CLAIM_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2743_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2743_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2743_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "routes": SOURCE_WEIGHT / "gauge_noether_zero_charge_audit_2743_NONCLAIM.csv",
    "closure": LOCAL_BOUNDS / "local_closure_ledger_2743_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2743_LOCAL_CLOSURE_PPN_BENCHMARK_NEXT.csv",
}

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


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


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = ["| " + " | ".join(md(row.get(col, "")) for col in cols) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def local_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["theorem_zero_adopted"] = False
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2743_0_2742_doc",
            "description": "2742 selects live gauge/Noether zero-charge route.",
            "source_path": "2742-Y5-R2FR-phase-volume-nonpropagating-qsector-origin-or-rejection-under-AX1090.md",
            "required_needles": "NEXT2742_0_2743;ORG2742_4_cell_current;VAL2742_OVERALL",
        },
        {
            "source_id": "SRC2743_1_2742_validation",
            "description": "2742 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2742_VALIDATION.csv",
            "required_needles": "VAL2742_OVERALL;True;no-charge route next",
        },
        {
            "source_id": "SRC2743_2_1555_doc",
            "description": "prior gauge/Noether zero-charge audit.",
            "source_path": "1555-Y5-gauge-noether-zero-charge-qsector-origin-audit.md",
            "required_needles": "GAUGE1555_4_first_class_constraint;RUN1555_3_current;NEXT1555_0_1556",
        },
        {
            "source_id": "SRC2743_3_1555_routes",
            "description": "machine-readable prior route audit.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1555_GAUGE_NOETHER_ROUTE_AUDIT.csv",
            "required_needles": "GAUGE1555_0_radial_coordinate_gauge;GAUGE1555_4_first_class_constraint;GAUGE1555_5_current_verdict",
        },
        {
            "source_id": "SRC2743_4_1555_contract",
            "description": "machine-readable first-class constraint contract.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1555_FIRST_CLASS_CONSTRAINT_CONTRACT.csv",
            "required_needles": "FCC1555_0_parent_phase_space;FCC1555_3_boundary_charge;FCC1555_7_no_GR_import",
        },
        {
            "source_id": "SRC2743_5_12_gauge_noether",
            "description": "source text for gauge/Noether warning.",
            "source_path": "12-gauge-noether-origin-audit.md",
            "required_needles": "gauge_noether_origin_not_derived_closure_only;Noether identity;local reciprocity route must be treated as a",
        },
        {
            "source_id": "SRC2743_6_11_cell_current",
            "description": "source text for no-charge obstruction.",
            "source_path": "11-cell-current-origin-attempt.md",
            "required_needles": "cell_current_origin_no_charge_obstruction;Q_R = constant;R_AB = -Q_R/r",
        },
        {
            "source_id": "SRC2743_7_10_observer_contract",
            "description": "observer-map symplectic contract and no-GR-import rules.",
            "source_path": "10-observer-map-symplectic-contract.md",
            "required_needles": "observer_map_contract_written_not_satisfied;must preserve or constrain the radial observer configuration cell separately;R_AB = ln(T^2 S) = 0",
        },
        {
            "source_id": "SRC2743_8_2742_queue",
            "description": "live acquisition queue into this checkpoint.",
            "source_path": "source-intake/rab-sector/acquisition-queue/JR2742_GAUGE_NOETHER_ZERO_CHARGE_NEXT.csv",
            "required_needles": "NEXT2742_0_2743;first-class/no-charge route",
        },
    ]
    for row in rows:
        path = local_path(row["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = [needle for needle in row["required_needles"].split(";") if needle]
        missing = [needle for needle in needles if needle not in text]
        row["exists"] = path.exists()
        row["needles_present"] = len(missing) == 0
        row["missing_needles"] = ";".join(missing)
        nonclaim(row)
    return rows


def route_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "GAUGE2743_0_radial_coordinate_gauge",
            "radial coordinate gauge",
            "use radial coordinate freedom to set T^2 S=1",
            "REJECTED_COORDINATE_IMPORT",
            "areal radius fixes r through sphere area; using this as AB=1 imports GR-like gauge logic",
        ),
        (
            "GAUGE2743_1_cell_scale_gauge",
            "cell-scale gauge",
            "treat T sqrt(S) as pure observer-splitting gauge",
            "REJECTED_OBSERVABLE_CHANGE",
            "T and S remain clock/routing observables unless a new matter/readout map proves otherwise",
        ),
        (
            "GAUGE2743_2_reciprocal_split_gauge",
            "reciprocal split gauge",
            "T -> exp(sigma)T and sqrt(S)->exp(-sigma)sqrt(S)",
            "REJECTED_IRRELEVANT_TO_RAB",
            "this leaves T sqrt(S) unchanged and cannot impose R_AB=0",
        ),
        (
            "GAUGE2743_3_noether_identity",
            "generic Noether identity",
            "sum_i E_i delta phi_i + divergence = 0",
            "REJECTED_IDENTITY_NOT_CONSTRAINT",
            "a Ward/Noether identity relates equations; it does not set a physical strain to zero without a constraint",
        ),
        (
            "GAUGE2743_4_cell_current",
            "cell-current conservation",
            "partial_r(W partial_r R_AB)=0 => W partial_r R_AB=Q_R",
            "REJECTED_NO_CHARGE_OBSTRUCTION",
            "conservation gives Q_R constant, not Q_R=0, so reciprocal hair survives",
        ),
        (
            "GAUGE2743_5_first_class_constraint",
            "first-class parent constraint",
            "G_R[epsilon]=int epsilon C_R + Q_R with C_R containing R_AB",
            "POSSIBLE_IN_PRINCIPLE_NOT_PRESENT",
            "requires parent symplectic potential, differentiable generator, boundary charge, bracket closure, degree count, and matter descent",
        ),
        (
            "GAUGE2743_6_boundary_charge_route",
            "proper/zero boundary charge route",
            "Q_R exact/proper/zero on local branch without deleting mass/time charges",
            "POSSIBLE_IN_PRINCIPLE_NOT_PRESENT",
            "no boundary term proof exists; deleting Q_R by hand would be the same closure axiom in disguise",
        ),
        (
            "GAUGE2743_7_current_verdict",
            "accepted gauge/Noether zero-charge origin",
            "derive Q_R=0 and R_AB=0 without importing GR",
            "NO_ACCEPTED_ORIGIN",
            "all current routes are rejected or future-contract only",
        ),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "route_id": rid,
                "route": route,
                "test": test,
                "result": result,
                "reason": reason,
                "accepted_zero_charge_origin": False,
                "source_paths": "1555-Y5-gauge-noether-zero-charge-qsector-origin-audit.md; 12-gauge-noether-origin-audit.md; 11-cell-current-origin-attempt.md",
            }
        )
        for rid, route, test, result, reason in specs
    ]


def contract_rows() -> list[dict[str, Any]]:
    specs = [
        ("FCC2743_0_parent_phase_space", "parent phase space", "fields, symplectic potential, and boundary variables include q/R_AB sector", "MISSING", "without this there is no generator or charge to compute"),
        ("FCC2743_1_constraint", "constraint equation", "C_R=0 or equivalent contains R_AB=ln(T^2 S) as primary/secondary constraint", "MISSING", "ordinary coordinate gauge and Noether identities do not supply it"),
        ("FCC2743_2_generator", "differentiable generator", "delta G_R[epsilon]=Omega(delta Phi,v_epsilon), G_R=int epsilon C_R+Q_R", "MISSING", "no parent symplectic potential or Hamiltonian generator is present"),
        ("FCC2743_3_boundary_charge", "zero/proper boundary charge", "Q_R is zero, exact, or proper on local branch without deleting physical mass/time charges", "MISSING", "this is the core no-charge theorem still absent"),
        ("FCC2743_4_bracket_closure", "first-class algebra", "constraint bracket closes with no anomaly or central edge cocycle", "MISSING", "no bracket algebra has been supplied"),
        ("FCC2743_5_degree_count", "degree count", "constraint removes reciprocal strain pair rather than hiding a physical mode", "MISSING", "no canonical degree-count proof exists"),
        ("FCC2743_6_matter_map", "matter/readout map", "matter observables descend through constrained observer split without shadow frames", "MISSING", "cell-scale gauge would change observables otherwise"),
        ("FCC2743_7_qnorm_descent", "q-norm/source descent", "same parent structure supplies E_q, J_q, and Dq[v_m] in one norm", "MISSING", "zero charge alone is not enough for local residual scoring"),
        ("FCC2743_8_no_GR_import", "no GR import", "proof does not use Schwarzschild AB=1 or Einstein vacuum equations", "PASS_GUARD_NONCLAIM", "guard is explicit and must remain enforced"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "contract_id": cid,
                "needed_object": needed,
                "acceptance_requirement": req,
                "current_status": status,
                "why_needed": why,
                "source_paths": "1555-Y5-gauge-noether-zero-charge-qsector-origin-audit.md; 10-observer-map-symplectic-contract.md",
            }
        )
        for cid, needed, req, status, why in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2743_0_coordinate", "coordinate gauge sets R_AB=0", "REFUSED_COORDINATE_IMPORT", "areal radial scaffold already fixes radial coordinate"),
        ("RUN2743_1_observer_split", "observer split gauge sets R_AB=0", "REFUSED_OBSERVABLE_CHANGE", "requires new matter/readout map not present"),
        ("RUN2743_2_reciprocal_split", "reciprocal split gauge sets R_AB=0", "REFUSED_IRRELEVANT_TO_RAB", "the proposed split leaves T sqrt(S) invariant"),
        ("RUN2743_3_noether", "Noether identity sets R_AB=0", "REFUSED_IDENTITY_NOT_CONSTRAINT", "identity is not a constraint equation"),
        ("RUN2743_4_current", "cell current conservation sets Q_R=0", "REFUSED_NO_CHARGE_OBSTRUCTION", "current gives constant Q_R not zero"),
        ("RUN2743_5_first_class", "first-class parent constraint exists", "REFUSED_MISSING_PARENT_CONSTRAINT", "contract is known but not supplied"),
        ("RUN2743_6_closure", "closure benchmark status", "PASS_NONCLAIM", "R_AB=0 may be used only as explicit benchmark closure"),
        ("RUN2743_7_score_status", "local GR/Newton claim", "REFUSED_NOT_SCORE_READY", "no gauge/Noether zero-charge origin closes"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "runner_id": rid,
                "check": check,
                "current_status": status,
                "reason": reason,
                "accepted_for_scoring": False,
            }
        )
        for rid, check, status, reason in specs
    ]


def closure_rows() -> list[dict[str, Any]]:
    specs = [
        ("CL2743_0_closure_statement", "explicit local closure", "assume R_AB=ln(T^2 S)=0 only as a benchmark closure", "ALLOWED_NONCLAIM"),
        ("CL2743_1_what_it_tests", "test use", "separate whether MTS can match local PPN/solar-system conditions under the closure", "BENCHMARK_ONLY"),
        ("CL2743_2_what_it_does_not_prove", "derivation limit", "does not prove parent q-sector, zero charge, q-norm, beta, conservation, or matter universality", "LIMIT_EXPLICIT"),
        ("CL2743_3_no_public_claim", "claim policy", "do not advertise local GR/Newton reduction as derived from this branch", "PASS_GUARD_NONCLAIM"),
        ("CL2743_4_reentry", "future reentry", "only a first-class constraint/no-charge theorem can promote closure to derivation", "REENTRY_CONTRACT"),
        ("CL2743_5_next_use", "next benchmark use", "run derived-vs-assumed PPN ledger before any local-data scoring", "NEXT_LOCAL_CLOSURE_PPN"),
    ]
    return [
        nonclaim(
            {
                "same_parent_branch_id": BRANCH_ID,
                "closure_id": cid,
                "item": item,
                "statement": statement,
                "current_status": status,
            }
        )
        for cid, item, statement, status in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2743_0_result",
            "Gauge/Noether zero-charge origin is not derived.",
            "NO_ACCEPTED_ZERO_CHARGE_ORIGIN",
            "coordinate, observer-scale, reciprocal split, Noether identity, current, and first-class routes all fail current evidence",
        ),
        (
            "DEC2743_1_closure",
            "Use R_AB=0 only as an explicit local closure benchmark.",
            "CLOSURE_BENCHMARK_NEXT",
            "this preserves the p=1/GR-lane test without pretending it is parent-derived",
        ),
        (
            "DEC2743_2_next",
            "Next target is local closure PPN benchmark.",
            "NEXT_2744_LOCAL_CLOSURE_PPN",
            "compute exactly what closure assumes and what remains to be derived/tested for gamma, beta, conservation, and matter universality",
        ),
        (
            "DEC2743_3_reentry",
            "Future derivation reentry contract is first-class/no-charge only.",
            "REENTRY_CONTRACT",
            "only parent symplectic/generator/boundary/bracket/degree/matter-map evidence can reopen zero-charge as a derivation",
        ),
    ]
    return [nonclaim({"decision_id": did, "decision": decision, "result": result, "rationale": rationale}) for did, decision, result, rationale in specs]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2743_0_audit", "gauge/Noether route audit", True, "PASS_NONCLAIM", "routes are tested and rejected or quarantined"),
        ("GATE2743_1_contract", "first-class constraint contract", True, "PASS_NONCLAIM", "future proof requirements are explicit"),
        ("GATE2743_2_closure", "closure benchmark ledger", True, "PASS_NONCLAIM", "R_AB=0 closure use is explicit"),
        ("GATE2743_3_zero_charge", "Q_R=0 theorem", False, "BLOCKED", "no parent no-charge theorem exists"),
        ("GATE2743_4_parent_constraint", "first-class parent constraint", False, "BLOCKED", "not supplied"),
        ("GATE2743_5_qnorm_source", "E_q/J_q/C_qm source", False, "BLOCKED", "zero-charge route does not provide same-norm residual inputs"),
        ("GATE2743_6_local_tests", "local arena score", False, "BLOCKED_NO_CLAIM", "benchmark not yet computed here"),
        ("GATE2743_7_GR_Newton", "derived GR/Newton limit", False, "BLOCKED_NO_CLAIM", "closure is not derivation"),
    ]
    return [
        nonclaim(
            {
                "claim_gate_id": gid,
                "claim": claim,
                "gate_passed": passed,
                "status": status,
                "claim_allowed": False,
                "reason": reason,
            }
        )
        for gid, claim, passed, status, reason in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2743_0_2744",
                "status": "selected_primary",
                "target_doc": "2744-Y5-R2FR-local-closure-PPN-benchmark-derived-vs-assumed-ledger-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_local_closure_PPN_benchmark_derived_vs_assumed_ledger_under_AX1090_2744.py",
                "mission": "build the honest R_AB=0 closure benchmark: what it gives, what it assumes, and what PPN/Newton/local tests still require",
                "acceptance": "separate derived algebraic consequences from assumed closure and from still-missing beta, conservation, matter-universality, and arena-projection gates",
                "forbidden": "do not claim the closure is derived; do not hide beta/conservation/matter universality; do not edit formalization-workbench",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2743_0_routes", "source_table": rel(OUTPUTS["routes"]), "copy_path": rel(BRANCH_OUTPUTS["routes"]), "purpose": "source-weight gauge/Noether zero-charge route audit", "exists": BRANCH_OUTPUTS["routes"].exists()}),
        nonclaim({"copy_id": "BR2743_1_closure", "source_table": rel(OUTPUTS["closure"]), "copy_path": rel(BRANCH_OUTPUTS["closure"]), "purpose": "local-bound closure benchmark ledger", "exists": BRANCH_OUTPUTS["closure"].exists()}),
        nonclaim({"copy_id": "BR2743_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB acquisition queue for local closure PPN benchmark", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def pycache_path() -> Path:
    return Path(__file__).resolve().parent / "__pycache__"


def remove_pycache() -> None:
    pycache = pycache_path()
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    closure: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    routes_ok = any(row["route_id"] == "GAUGE2743_5_first_class_constraint" for row in routes) and any(row["route_id"] == "GAUGE2743_7_current_verdict" and row["result"] == "NO_ACCEPTED_ORIGIN" for row in routes)
    contract_ok = any(row["contract_id"] == "FCC2743_3_boundary_charge" and row["current_status"] == "MISSING" for row in contract) and any(row["contract_id"] == "FCC2743_8_no_GR_import" and row["current_status"] == "PASS_GUARD_NONCLAIM" for row in contract)
    runner_ok = any(row["runner_id"] == "RUN2743_6_closure" and row["current_status"] == "PASS_NONCLAIM" for row in runner) and any(row["runner_id"] == "RUN2743_7_score_status" and "REFUSED" in row["current_status"] for row in runner)
    closure_ok = any(row["closure_id"] == "CL2743_0_closure_statement" for row in closure) and any(row["closure_id"] == "CL2743_5_next_use" and row["current_status"] == "NEXT_LOCAL_CLOSURE_PPN" for row in closure)
    gates_ok = any(row["claim_gate_id"] == "GATE2743_2_closure" and row["gate_passed"] is True for row in gates) and all(row["claim_allowed"] is False for row in gates)
    no_claim_flags_ok = all(row.get("valid_for_claim") is False and row.get("claim_allowed") is False for block in [routes, contract, runner, closure, gates] for row in block)
    next_ok = next_target[0]["selected"] is True and "2744" in next_target[0]["target_doc"] and "PPN" in next_target[0]["target_doc"]
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    pycache_ok = not pycache_path().exists()
    formalization_count = formalization_recent_count()
    formalization_ok = formalization_count == 0
    csv_ok = True
    csv_bits: list[str] = []
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
        {"validation_id": "VAL2743_0_sources", "passed": source_ok, "detail": "all source paths exist and required anchors/needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2743_1_route_audit", "passed": routes_ok, "detail": "gauge/Noether routes audited and no origin accepted", "timestamp_utc": ts()},
        {"validation_id": "VAL2743_2_contract", "passed": contract_ok, "detail": "first-class/no-charge contract records missing boundary charge and no-GR guard", "timestamp_utc": ts()},
        {"validation_id": "VAL2743_3_runner_refuses", "passed": runner_ok, "detail": "runner passes only closure nonclaim and refuses local scoring", "timestamp_utc": ts()},
        {"validation_id": "VAL2743_4_closure_ledger", "passed": closure_ok, "detail": "closure ledger written and selects local closure PPN next", "timestamp_utc": ts()},
        {"validation_id": "VAL2743_5_claim_gates", "passed": gates_ok and no_claim_flags_ok, "detail": "claim gates keep all prediction/claim flags false", "timestamp_utc": ts()},
        {"validation_id": "VAL2743_6_next_target", "passed": next_ok, "detail": "next target is local closure PPN benchmark", "timestamp_utc": ts()},
        {"validation_id": "VAL2743_7_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2743_8_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2743_9_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2743_10_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2743_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2743 rejects current gauge/Noether zero-charge derivation, writes the first-class reentry contract, and selects local closure PPN benchmark next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2743 - Y5 R2/f(R): Gauge/Noether Zero-Charge q-sector Origin Or Closure Demotion Under AX1090

Status: `Y5_R2FR_2743_zero_charge_origin_not_derived_closure_benchmark_selected`

## Private Verdict

2743 tests the door we had to test: can symmetry or a Noether/current argument make `Q_R=0` a theorem rather than an assumption?

Current answer: no.

The clean obstruction is:

`partial_r(W partial_r R_AB)=0 => W partial_r R_AB=Q_R`.

That gives a conserved reciprocal charge. It does not set the charge to zero. With spherical exterior weight, that leaves the dangerous hair `R_AB=-Q_R/r` unless a parent no-charge theorem exists.

Coordinate gauge is refused because areal radius already fixes `r`. Generic Noether identity is refused because identities relate equations; they do not create the missing constraint. The only respectable derivation reentry is a first-class parent constraint with a differentiable generator, proper/zero boundary charge, bracket closure, degree count, and matter-map descent.

So we demote the local route honestly: `R_AB=0` is now an explicit closure benchmark, not a derived GR/Newton result. Next we test exactly what that benchmark gives and what it still assumes.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Gauge/Noether Route Audit

{markdown_table(data["routes"], ["route_id", "route", "test", "result", "reason", "accepted_zero_charge_origin", "valid_for_claim"])}

## First-Class Constraint Contract

{markdown_table(data["contract"], ["contract_id", "needed_object", "acceptance_requirement", "current_status", "why_needed", "valid_for_claim"])}

## Zero-Charge Runner

{markdown_table(data["runner"], ["runner_id", "check", "current_status", "reason", "accepted_for_scoring", "valid_for_claim"])}

## Local Closure Ledger

{markdown_table(data["closure"], ["closure_id", "item", "statement", "current_status", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "result", "rationale", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim", "gate_passed", "status", "claim_allowed", "valid_for_claim", "reason"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is not a defeat; it is a useful demotion. The theory still has a strong-looking local closure lane, but the current derivation route cannot honestly claim it. The next step is the Mayweather round: use the closure as a benchmark, separate assumed from derived, and see whether it can stand in the local PPN ring without overclaiming.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    routes = route_rows()
    contract = contract_rows()
    runner = runner_rows()
    closure = closure_rows()
    decisions = decision_rows()
    gates = gate_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["routes"], routes)
    write_csv(OUTPUTS["contract"], contract)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["closure"], closure)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["routes"], routes)
    write_csv(BRANCH_OUTPUTS["closure"], closure)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, routes, contract, runner, closure, gates, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "routes": routes,
        "contract": contract,
        "runner": runner,
        "closure": closure,
        "decisions": decisions,
        "gates": gates,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    remove_pycache()

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2743 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
