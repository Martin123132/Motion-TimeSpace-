from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1238"
TITLE = "1238-Y5-R10-first-class-RAB-constraint-or-local-GR-closure-benchmark-scorecard"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
FIRST_CLASS_PATH = OUT_DIR / f"{PACK_ID}_FIRST_CLASS_RAB_CONSTRAINT_ATTEMPT.csv"
BENCHMARK_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_GR_CLOSURE_BENCHMARK_SCORECARD.csv"
RESIDUAL_VECTOR_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_RESIDUAL_VECTOR_MAP.csv"
TEST_PRIORITY_PATH = OUT_DIR / f"{PACK_ID}_EMPIRICAL_TEST_PRIORITY_LEDGER.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1238_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def is_false(row: dict[str, object], key: str) -> bool:
    return not parse_bool(row.get(key, False))


def source_ref(relative_path: str, needle: str) -> str:
    return f"{relative_path}:{needle}"


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > RUN_STARTED_UTC
    )


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1238_0_1237_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1237_NEXT_TARGET.csv",
            "needle": "NEXT1237_0_1238",
            "purpose": "1237 handoff to first-class R_AB constraint or closure benchmark",
        },
        {
            "source_id": "SRC1238_1_1237_local_GR",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1237_LOCAL_GR_CONNECTION_STATUS.csv",
            "needle": "LGR1237_5_verdict",
            "purpose": "local GR/Newton reduction remains not derived",
        },
        {
            "source_id": "SRC1238_2_1237_closure",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1237_CLOSURE_DEMOTION_LEDGER.csv",
            "needle": "CLOSE1237_1_local_reciprocity",
            "purpose": "R_AB=0 closure demotion",
        },
        {
            "source_id": "SRC1238_3_1237_residuals",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1237_FINITE_RESIDUAL_TEST_TRACK.csv",
            "needle": "TEST1237_0_QR_hair",
            "purpose": "finite residual test track with Q_R",
        },
        {
            "source_id": "SRC1238_4_gauge_noether",
            "local_path": "12-gauge-noether-origin-audit.md",
            "needle": "first-class parent constraint",
            "purpose": "first-class constraint remains possible in principle",
        },
        {
            "source_id": "SRC1238_5_cell_current",
            "local_path": "11-cell-current-origin-attempt.md",
            "needle": "cell_current_origin_no_charge_obstruction",
            "purpose": "cell-current route permits reciprocal hair",
        },
        {
            "source_id": "SRC1238_6_observer_contract",
            "local_path": "10-observer-map-symplectic-contract.md",
            "needle": "derive R_AB=0 from the parent theory",
            "purpose": "observer-map no-smuggling contract",
        },
        {
            "source_id": "SRC1238_7_parent_action_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1009_CLAIM_GATE.csv",
            "needle": "CG1009_0_total_parent_action",
            "purpose": "total parent action gate remains false",
        },
        {
            "source_id": "SRC1238_8_source_scalar",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
            "needle": "SSE1066_5_verdict",
            "purpose": "source-label/source-scalar exclusion remains conditional",
        },
        {
            "source_id": "SRC1238_9_1236_certificate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
            "needle": "CERT1236_6_current_verdict",
            "purpose": "typed grammar certificate remains closure-only",
        },
    ]

    source_register = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "absolute_path": str(source_path(spec["local_path"])),
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    first_class_attempt = [
        {
            "attempt_id": "FCR1238_0_target",
            "claim_piece": "first-class parent constraint for R_AB=0",
            "formal_test": "Find a parent constraint C_R=R_AB with multiplier generated by a parent gauge symmetry, first-class algebra, no boundary charge Q_R, and matter/readout invariance.",
            "result": "TARGET_SHARP",
            "gap": "must be more than adding lambda_R R_AB by hand",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "FCR1238_1_multiplier_only",
            "claim_piece": "lambda_R R_AB term",
            "formal_test": "S -> S + int lambda_R R_AB imposes R_AB=0 on-shell.",
            "result": "CLOSURE_NOT_DERIVATION",
            "gap": "the multiplier origin is not parent-derived; this is exactly the closure axiom in action form",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "FCR1238_2_gauge_generator",
            "claim_piece": "observer-cell scaling gauge",
            "formal_test": "A gauge generator G_R would make R_AB pure gauge while leaving matter clocks, rods, spectra, and source coupling invariant.",
            "result": "FAILS_CURRENT_SCAFFOLD",
            "gap": "12 shows cell-scale changes affect observables unless a new matter/readout map is built",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "FCR1238_3_constraint_algebra",
            "claim_piece": "first-class closure",
            "formal_test": "{C_R,H_parent}=0 modulo constraints and boundary terms; C_R carries no exterior Q_R charge.",
            "result": "NOT_AVAILABLE",
            "gap": "no total H_parent/action, no Poisson algebra, and 11 leaves Q_R hair",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "FCR1238_4_source_label_forgetting",
            "claim_piece": "total Hilbert source with no species source labels",
            "formal_test": "The same parent constraint/action must make the matter source functor return T_total before readout or material labels.",
            "result": "NOT_DERIVED",
            "gap": "source scalar exclusion remains conditional and total parent action gate is false",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "FCR1238_5_verdict",
            "claim_piece": "derive R_AB=0 and source-label forgetting",
            "formal_test": "FCR1238_1 through FCR1238_4 close without importing GR or adopting closure.",
            "result": "FIRST_CLASS_ROUTE_NOT_CONSTRUCTED",
            "gap": "no parent gauge generator/constraint algebra/source functor exists in current corpus",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    benchmark_scorecard = [
        {
            "branch_id": "BGR1238_0_derived_target",
            "branch": "derived local GR target",
            "assumptions": "none beyond parent MTS action",
            "what_it_would_buy": "Newtonian limit, gamma=1, beta=1, EP, Bianchi/conservation, and no finite source residuals",
            "current_score": "NOT_AVAILABLE",
            "reason": "first-class route and total source functor are not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "BGR1238_1_closure_GR",
            "branch": "local-GR closure benchmark",
            "assumptions": "R_AB=0, typed visible coefficient grammar, unique F_Q^2, source-label forgetting, readout closure",
            "what_it_would_buy": "internal best-case GR-like benchmark for comparison against finite residual branches",
            "current_score": "USEFUL_PRIVATE_BASELINE_ONLY",
            "reason": "assumptions are explicit closures, not derivations",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "BGR1238_2_finite_residual",
            "branch": "finite residual local branch",
            "assumptions": "retain Q_R, alpha, source, readout, and QCD component residuals as bounded parameters",
            "what_it_would_buy": "testable nonclaim bridge to PPN/WEP/R10/clock/material data without pretending theorem-zeroes",
            "current_score": "BEST_EMPIRICAL_TRACK",
            "reason": "derivation is incomplete but residuals can be bounded and compared",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "BGR1238_3_public_status",
            "branch": "public physics claim",
            "assumptions": "none",
            "what_it_would_buy": "serious external claim of derived local GR/source universality",
            "current_score": "BLOCKED",
            "reason": "current evidence supports disciplined private benchmarks only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    residual_vector = [
        {
            "residual_id": "RV1238_0_QR",
            "symbol": "Q_R",
            "meaning": "reciprocal hair / R_AB exterior charge",
            "why_live": "cell-current conservation leaves Q_R constant rather than zero",
            "primary_arena": "PPN gamma, light bending, Shapiro delay, orbital tests",
            "closure_value": "0",
            "nonclaim_status": "BOUND_OR_FIRST_CLASS_PROOF_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "RV1238_1_beta_PPN",
            "symbol": "beta_PPN-1",
            "meaning": "second-order local metric residual",
            "why_live": "closure R_AB=0 does not by itself build full second-order PPN solution",
            "primary_arena": "perihelion/orbital timing/local metric tests",
            "closure_value": "0",
            "nonclaim_status": "FIELD_EQUATION_AND_CONSERVATION_PROOF_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "RV1238_2_alpha",
            "symbol": "b_alpha or c_alpha_DD",
            "meaning": "EM kinetic/hidden-visible coefficient residual",
            "why_live": "unique F_Q^2 and typed grammar are not parent-derived",
            "primary_arena": "clock alpha, WEP/R10 alpha channel",
            "closure_value": "0",
            "nonclaim_status": "BOUND_OR_EM_LOCK_PROOF_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "RV1238_3_source_alpha",
            "symbol": "beta_source_alpha",
            "meaning": "EM current/source normalization residual",
            "why_live": "source-label forgetting/current owner are unsigned",
            "primary_arena": "R10/WEP composition tests",
            "closure_value": "0",
            "nonclaim_status": "BOUND_OR_SOURCE_FUNCTOR_PROOF_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "RV1238_4_readout",
            "symbol": "tau_clock, tau_WEP, tau_readout",
            "meaning": "readout/radiative transfer residual",
            "why_live": "readout closure is not derived",
            "primary_arena": "clock/spectroscopy/transfer kernels",
            "closure_value": "0 or fixed kernel",
            "nonclaim_status": "TRANSFER_SOURCE_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "RV1238_5_QCD",
            "symbol": "F_B,q, F_B,g, delta w_q, delta w_g",
            "meaning": "QCD/material component source residual",
            "why_live": "QCD color owner and bound-state/source transfer are not signed",
            "primary_arena": "WEP/R10 material source vectors",
            "closure_value": "0 for delta w; sourced fractions for F_B",
            "nonclaim_status": "COMPONENT_SOURCE_ROWS_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    test_priority = [
        {
            "priority_id": "TP1238_0_PPN_QR",
            "rank": 1,
            "target": "Q_R / gamma residual",
            "why_first": "if reciprocal hair is nonzero, local GR reduction fails before subtle source-composition tests",
            "next_input_needed": "derive first-class zero theorem or build nonclaim PPN residual bound schema",
            "status": "HIGHEST_PRIORITY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority_id": "TP1238_1_source_WEP",
            "rank": 2,
            "target": "beta_source_alpha and Delta_w material residuals",
            "why_first": "source universality is the bridge from field grammar to R10/WEP/local GR",
            "next_input_needed": "component vectors and source-label forgetting proof or finite priors",
            "status": "HIGH_PRIORITY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority_id": "TP1238_2_clock_alpha",
            "rank": 3,
            "target": "alpha/readout residuals",
            "why_first": "EM lock and readout closure are unproved and feed clock/WEP transfer",
            "next_input_needed": "readout kernels or finite b_alpha/c_alpha_DD priors",
            "status": "HIGH_PRIORITY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority_id": "TP1238_3_QCD_components",
            "rank": 4,
            "target": "QCD quark/gluon component fractions",
            "why_first": "QCD source fractions determine whether material tests can be scored honestly",
            "next_input_needed": "claim-grade F_B,q/F_B,g source rows or closure proof",
            "status": "MEDIUM_PRIORITY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "priority_id": "TP1238_4_cosmology",
            "rank": 5,
            "target": "cosmology robustness branch",
            "why_first": "important empirical pillar but not the current local-GR derivation blocker",
            "next_input_needed": "separate robustness runner/results, not mixed into local source closure",
            "status": "SEPARATE_TRACK",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1238_0_first_class_not_constructed",
            "decision": "do not claim first-class R_AB constraint",
            "because": "no parent gauge generator, constraint algebra, boundary zero-charge theorem, or source functor is supplied",
            "next_action": "use explicit closure benchmark or build a future parent constrained action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1238_1_benchmark_written",
            "decision": "use local-GR closure benchmark only as private baseline",
            "because": "it is useful for comparing finite residual branches but not proof of derived GR",
            "next_action": "label closure rows clearly in any runner or report",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1238_2_residual_vector_selected",
            "decision": "carry Q_R, beta_PPN-1, alpha, source, readout, and QCD residuals forward",
            "because": "these are the live gaps after closure demotion",
            "next_action": "turn the residual vector into runner inputs and source requirements",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1238_0_first_class_RAB",
            "claim": "R_AB=0 first-class parent constraint",
            "status": "BLOCKED",
            "reason": "FCR1238_5 result=FIRST_CLASS_ROUTE_NOT_CONSTRUCTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1238_1_derived_local_GR",
            "claim": "derived local GR/Newton reduction",
            "status": "BLOCKED",
            "reason": "only closure benchmark and finite residual branches are available",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1238_2_WEP_R10_PPN_clock",
            "claim": "WEP/R10/PPN/clock structural pass",
            "status": "BLOCKED",
            "reason": "residual vector remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1238_3_public_claim",
            "claim": "public local-GR victory claim",
            "status": "BLOCKED",
            "reason": "closure assumptions cannot be advertised as derivations",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1238_0_1239",
            "target_file": "1239-Y5-R10-local-residual-vector-runner-input-schema-and-source-priority.md",
            "target_script": "scripts/Y5_R10_local_residual_vector_runner_input_schema_and_source_priority.py",
            "task": "convert the 1238 residual vector into a nonclaim runner-input schema and source-priority checklist for PPN/Q_R, WEP/R10 source beta, clock alpha/readout, and QCD component fractions",
            "success_condition": "future testing can distinguish closure benchmark rows from finite residual rows without promoting either to a claim",
            "do_not_do": "do not run long data jobs, claim derived GR, or treat closure values as evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_paths = [
        SOURCE_REGISTER_PATH,
        FIRST_CLASS_PATH,
        BENCHMARK_PATH,
        RESIDUAL_VECTOR_PATH,
        TEST_PRIORITY_PATH,
        DECISION_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(FIRST_CLASS_PATH, first_class_attempt)
    write_csv(BENCHMARK_PATH, benchmark_scorecard)
    write_csv(RESIDUAL_VECTOR_PATH, residual_vector)
    write_csv(TEST_PRIORITY_PATH, test_priority)
    write_csv(DECISION_PATH, decisions)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(NEXT_PATH, next_target)

    parsed_counts: list[str] = []
    csv_parse_ok = True
    for path in generated_paths:
        try:
            parsed_counts.append(f"{path.name}:{len(read_csv(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_counts.append(f"{path.name}:ERROR:{exc}")

    all_sources_exist = all(parse_bool(row["path_exists"]) for row in source_register)
    all_needles_found = all(parse_bool(row["needle_found"]) for row in source_register)
    all_generated_nonclaim = all(
        is_false(row, "valid_for_claim") and is_false(row, "claim_allowed")
        for table in [
            source_register,
            first_class_attempt,
            benchmark_scorecard,
            residual_vector,
            test_priority,
            decisions,
            claim_gates,
            next_target,
        ]
        for row in table
    )
    first_class_failed = any(
        row["attempt_id"] == "FCR1238_5_verdict"
        and row["result"] == "FIRST_CLASS_ROUTE_NOT_CONSTRUCTED"
        for row in first_class_attempt
    )
    benchmark_ready = any(
        row["branch_id"] == "BGR1238_1_closure_GR"
        and row["current_score"] == "USEFUL_PRIVATE_BASELINE_ONLY"
        for row in benchmark_scorecard
    )
    residual_vector_ready = len(residual_vector) == 6 and any(row["symbol"] == "Q_R" for row in residual_vector)
    priority_ready = len(test_priority) == 5 and test_priority[0]["target"] == "Q_R / gamma residual"
    gates_blocked = all(row["status"] == "BLOCKED" and is_false(row, "claim_allowed") for row in claim_gates)
    next_is_1239 = next_target[0]["target_file"].startswith("1239-Y5-R10-local-residual-vector")
    fw_recent = formalization_recent_count()

    validation = [
        validation_row(
            "VAL1238_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(parse_bool(row['path_exists']) for row in source_register)}/{len(source_register)} sources exist",
        ),
        validation_row(
            "VAL1238_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(parse_bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        ),
        validation_row(
            "VAL1238_2_first_class_failed",
            "first-class R_AB route is not constructed",
            first_class_failed,
            "FCR1238_5 result=FIRST_CLASS_ROUTE_NOT_CONSTRUCTED",
        ),
        validation_row(
            "VAL1238_3_benchmark_ready",
            "closure benchmark scorecard is available",
            benchmark_ready,
            "BGR1238_1 current_score=USEFUL_PRIVATE_BASELINE_ONLY",
        ),
        validation_row(
            "VAL1238_4_residual_vector_ready",
            "local residual vector is mapped",
            residual_vector_ready,
            f"residual_rows={len(residual_vector)} including Q_R",
        ),
        validation_row(
            "VAL1238_5_priority_ready",
            "empirical test priority is written",
            priority_ready,
            "rank 1 target=Q_R / gamma residual",
        ),
        validation_row(
            "VAL1238_6_claim_gates_blocked",
            "all claim gates remain blocked",
            gates_blocked,
            f"blocked_gates={sum(row['status'] == 'BLOCKED' for row in claim_gates)}/{len(claim_gates)}",
        ),
        validation_row(
            "VAL1238_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            all_generated_nonclaim,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1238_8_next_target_1239",
            "next target is residual-vector runner input schema",
            next_is_1239,
            next_target[0]["target_file"],
        ),
        validation_row(
            "VAL1238_9_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_counts),
        ),
        validation_row(
            "VAL1238_10_formalization_untouched",
            "formalization-workbench untouched during run",
            fw_recent == 0,
            f"formalization_recent_write_count_since_run_start={fw_recent}",
        ),
    ]
    validation.append(
        validation_row(
            "VAL1238_11_overall",
            "overall 1238 validation",
            all(row["status"] == "PASS" for row in validation),
            "1238 fails the first-class R_AB derivation honestly, writes the local-GR closure benchmark, and maps the finite residual vector for testing",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    sections = [
        f"# {TITLE}",
        "",
        "**Current verdict:** 1238 does **not** construct a first-class parent constraint for `R_AB=0`. The honest outcome is a local-GR closure benchmark plus a finite residual vector for testing.",
        "",
        "**Main progress:** the local route is now split into three clean lanes: derived target unavailable, closure-GR private benchmark available, and finite residual empirical track ready to be schema-mapped.",
        "",
        "**No-claim guard:** no derived GR, EM lock, graph connectedness, `Delta_w=0`, R10, WEP, PPN, clock, orbital, local-GR, or public source-coupling claim is promoted.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Source Register",
        markdown_table(source_register, list(source_register[0].keys())),
        "",
        "## First-Class RAB Constraint Attempt",
        markdown_table(first_class_attempt, list(first_class_attempt[0].keys())),
        "",
        "## Local GR Closure Benchmark Scorecard",
        markdown_table(benchmark_scorecard, list(benchmark_scorecard[0].keys())),
        "",
        "## Local Residual Vector Map",
        markdown_table(residual_vector, list(residual_vector[0].keys())),
        "",
        "## Empirical Test Priority Ledger",
        markdown_table(test_priority, list(test_priority[0].keys())),
        "",
        "## Decision Ledger",
        markdown_table(decisions, list(decisions[0].keys())),
        "",
        "## Claim Gates",
        markdown_table(claim_gates, list(claim_gates[0].keys())),
        "",
        "## Next Target",
        markdown_table(next_target, list(next_target[0].keys())),
        "",
        "## Validation",
        markdown_table(validation, list(validation[0].keys())),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
