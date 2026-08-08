from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_FINITE_Q_RESIDUAL_COEFFICIENT_SOURCE_OR_LOCAL_BENCHMARK_RUNNER_2424"
CHECKPOINT_ID = "2424"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2424-Y5-R2FR-finite-q-residual-coefficient-source-or-local-benchmark-runner.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2424_SOURCE_REGISTER.csv",
    "branch_state": OUT / "P8_Y5_PARENT_QLOC_2424_FINITE_Q_BRANCH_STATE.csv",
    "missing_inputs": OUT / "P8_Y5_PARENT_QLOC_2424_MISSING_INPUT_STACK.csv",
    "projection_gates": OUT / "P8_Y5_PARENT_QLOC_2424_PROJECTION_SCORE_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2424_REFUSAL_RUNNER.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2424_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2424_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2424_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2424_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue": QUEUE / "JR2424_FINITE_Q_RESIDUAL_BRIDGE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "P8_Y5_PARENT_QLOC_2424_LOCAL_GR_REFUSAL_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_FINITE_Q_RESIDUAL_DECISION_2424_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2424_00_2423_current_handoff",
        "source_path": ROOT / "2423-Y5-R2FR-phase-lock-distribution-or-q-residual-operator-owner.md",
        "needles": ["PLO2423_5_verdict", "SCF2423_5_finalizer", "NEXT2423_0_selected", "VAL2423_OVERALL"],
        "role": "current 24xx handoff: phase-lock demoted and finite q residual runner selected",
    },
    {
        "source_id": "SRC2424_01_2284_finite_runner",
        "source_path": ROOT / "2284-Y5-R2FR-finite-q-residual-coefficient-source-or-local-benchmark-runner.md",
        "needles": ["QRF2284_0_algebraic_parent_block", "POB2284_2_R10", "VAL2284_OVERALL"],
        "role": "earlier finite-q algebraic/gradient/closure benchmark runner",
    },
    {
        "source_id": "SRC2424_02_2285_projection_pack",
        "source_path": ROOT / "2285-Y5-R2FR-finite-q-PPN-R10-projection-matrix-or-input-source-pack.md",
        "needles": ["POBS2285_0_gamma", "POBS2285_10_R10", "VAL2285_OVERALL"],
        "role": "local observable projection/source pack with PPN and R10 channels",
    },
    {
        "source_id": "SRC2424_03_2286_weak_field",
        "source_path": ROOT / "2286-Y5-R2FR-parent-weak-field-Mq-jq-delta-beta-source-or-zero-theorem.md",
        "needles": ["NF2286_1_algebraic_q_sector", "COEF2286_2_qR", "VAL2286_OVERALL"],
        "role": "weak-field normal form q_R=j_q/M_q^2 and delta_beta coefficient ledger",
    },
    {
        "source_id": "SRC2424_04_2287_selector_fork",
        "source_path": ROOT / "2287-Y5-R2FR-q-sector-parent-coefficient-extraction-or-selector-fork.md",
        "needles": ["DEC2287_0_verdict", "NEXT2287_0_primary", "VAL2287_OVERALL"],
        "role": "q-sector route fork: auxiliary zero route vs finite residual route",
    },
    {
        "source_id": "SRC2424_05_2288_auxiliary_contract",
        "source_path": ROOT / "2288-Y5-R2FR-RAB-auxiliary-parent-sort-no-derivative-or-finite-Zq-intake.md",
        "needles": ["AUX2288_2_second_class", "CON2288_6_joint_contract", "VAL2288_OVERALL"],
        "role": "second-class auxiliary route clarified but parent protection contract unsigned",
    },
    {
        "source_id": "SRC2424_06_2289_protection_or_live_row",
        "source_path": ROOT / "2289-Y5-R2FR-parent-protection-contract-derivation-from-MTS-primitives-or-first-live-Zq-row.md",
        "needles": ["PRIM2289_4_verdict", "COEFF2289_5_verdict", "VAL2289_OVERALL"],
        "role": "primitive protection contract rejected under current evidence; no internal coefficient row ready",
    },
    {
        "source_id": "SRC2424_07_2290_zq_tau",
        "source_path": ROOT / "2290-Y5-R2FR-first-internal-Zq-or-tauR10-projection-row.md",
        "needles": ["ZQ2290_3_verdict", "TAU2290_4_verdict", "VAL2290_OVERALL"],
        "role": "Z_q/tau_R10 internal row still missing; source/test product law refined",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [stringify(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                source_path=path,
                path_exists=path.exists(),
                required_needles="; ".join(needles),
                found_needles="; ".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=source["role"],
            )
        )
    return rows


def branch_state_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            state_id="STATE2424_0_closure_benchmark",
            branch="q=0 / R_AB=0 closure benchmark",
            status="RUNNABLE_AS_CONTROL_ONLY",
            what_is_known="q=0 iff R_AB=0 iff J_q=1 and can be used as a labelled GR-lane control",
            what_is_missing="parent selector theorem",
            score_ready=False,
        ),
        base_row(
            state_id="STATE2424_1_algebraic_finite_q",
            branch="finite nonpropagating q residual",
            status="FORMAL_NORMAL_FORM_READY_INPUTS_MISSING",
            what_is_known="L_q=-1/2 M_q^2 q^2 + (j_q L+...)q gives q_R=j_q/M_q^2 if M_q^2 is nonzero",
            what_is_missing="M_q^2, j_q, compatible units, source normalization and no-gradient guard",
            score_ready=False,
        ),
        base_row(
            state_id="STATE2424_2_gradient_massive_q",
            branch="finite range or boundary-hair q residual",
            status="RETAINED_NONCLAIM_BOUND_BRANCH",
            what_is_known="Z_q box q - M_q^2 q + J_q=0 would yield lambda_q=sqrt(Z_q/M_q^2) or hair",
            what_is_missing="Z_q, M_q^2, boundary charge class, range kernel, R10 projection",
            score_ready=False,
        ),
        base_row(
            state_id="STATE2424_3_projection_pack",
            branch="P_obs local observable map",
            status="TRANSLATION_LANGUAGE_EXISTS_PARENT_VALUES_MISSING",
            what_is_known="q_R maps to gamma/light/Shapiro/perihelion translations; R10 needs alpha(lambda) product form",
            what_is_missing="parent q_R/delta_beta/source-normalization values and R10 source/test kernel",
            score_ready=False,
        ),
        base_row(
            state_id="STATE2424_4_source_test_coupling",
            branch="R10/two-body coupling",
            status="PRODUCT_LAW_REQUIRED_NOT_FILLED",
            what_is_known="alpha_R10(lambda) must be K_q(lambda) beta_source beta_test + epsilon_tail, not one-leg magic c_g",
            what_is_missing="beta_source, beta_test, K_q, lambda_q and normalization",
            score_ready=False,
        ),
    ]


def missing_input_rows() -> list[dict[str, Any]]:
    return [
        base_row(input_id="MISS2424_0_Zq", quantity="Z_q", needed_for="gradient/range branch and theorem-zero route", current_status="MISSING_THEOREM_ZERO_OR_NUMERIC_VALUE", next_gate="derive operator exclusion or finite coefficient"),
        base_row(input_id="MISS2424_1_Mq2", quantity="M_q^2", needed_for="algebraic residual q_R and range lambda_q", current_status="MISSING_PARENT_HESSIAN_OR_MASS_GAP", next_gate="derive parent second variation in q normalization"),
        base_row(input_id="MISS2424_2_jq", quantity="j_q", needed_for="source numerator q_R=j_q/M_q^2", current_status="MISSING_PARENT_SOURCE_COEFFICIENT", next_gate="derive matter/source q-current or theorem-zero"),
        base_row(input_id="MISS2424_3_boundary", quantity="B_R / Pi_q / Q_R", needed_for="no-hair guard or exterior hair branch", current_status="MISSING_BOUNDARY_CHARGE_CLASS", next_gate="derive source-worldtube/corner no-hair class"),
        base_row(input_id="MISS2424_4_beta_split", quantity="beta_source and beta_test", needed_for="R10 two-body alpha(lambda) product", current_status="MISSING_SOURCE_TEST_CHARGE_SPLIT", next_gate="derive source/test leg normalization before R10 scoring"),
        base_row(input_id="MISS2424_5_Pobs", quantity="P_obs", needed_for="PPN, R10, clock, WEP, orbital readout", current_status="MISSING_ARENA_PROJECTION_VALUES", next_gate="keep translations separate from parent predictions"),
        base_row(input_id="MISS2424_6_source_norm", quantity="Newton/source normalization", needed_for="prevent fitted GM hiding q effects", current_status="RETAINED_UNFILLED_SOURCE_NORMALIZATION_VECTOR", next_gate="worldtube/Hilbert source equality or explicit residual"),
        base_row(input_id="MISS2424_7_bound_curve", quantity="external alpha_bound(lambda)", needed_for="R10 comparator only after theory prediction exists", current_status="METADATA_ONLY_OR_CURVE_NOT_LIVE_FOR_CLAIM", next_gate="digitize later; not a substitute for MTS-side coefficients"),
    ]


def projection_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="PG2424_0_PPN_scalar", arena="PPN scalar gamma/beta/light/Shapiro/perihelion", translation_ready=True, parent_prediction_ready=False, blocker="q_R, delta_beta, source normalization and second-order beta completion missing"),
        base_row(gate_id="PG2424_1_R10", arena="short-range alpha(lambda)", translation_ready=False, parent_prediction_ready=False, blocker="Z_q/M_q^2/j_q/beta_source/beta_test/K_q/lambda_q and digitized curve missing"),
        base_row(gate_id="PG2424_2_clocks", arena="clock/redshift", translation_ready=False, parent_prediction_ready=False, blocker="matter/coframe descent and source-normalization readout missing"),
        base_row(gate_id="PG2424_3_WEP", arena="composition dependence", translation_ready=False, parent_prediction_ready=False, blocker="universal matter coupling/source-blind functor not public-derived"),
        base_row(gate_id="PG2424_4_orbital", arena="orbital/Newton mechanics", translation_ready=False, parent_prediction_ready=False, blocker="GM source bridge and beta/metric completion missing"),
        base_row(gate_id="PG2424_5_claim", arena="derived local GR/Newton", translation_ready=False, parent_prediction_ready=False, blocker="closure branch is explicit control; finite branch not coefficient-owned"),
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        base_row(refusal_id="REF2424_0_claim_closure", attempted_claim="q=0 closure proves local GR", result="REFUSED_CLOSURE_ONLY", reason="2423/2283 finalizers do not parent-sign the selector"),
        base_row(refusal_id="REF2424_1_score_placeholders", attempted_claim="score PPN/R10 with missing Z_q/M_q^2/j_q", result="REFUSED_PLACEHOLDER_INPUTS", reason="coefficients, units, source path and projection are missing"),
        base_row(refusal_id="REF2424_2_use_bounds_as_coefficients", attempted_claim="use R10/PPN bounds as MTS coefficients", result="REFUSED_COMPARATOR_NOT_THEORY", reason="external bounds screen predictions; they do not define them"),
        base_row(refusal_id="REF2424_3_linear_cg_shortcut", attempted_claim="one-leg c_g/tau_R10 row is scoreable", result="REFUSED_SOURCE_TEST_PRODUCT_MISSING", reason="R10 is a two-body source/test exchange unless one leg is explicitly packed into Qbar"),
        base_row(refusal_id="REF2424_4_public_claim", attempted_claim="public/GitHub local-GR update", result="REFUSED_PRIVATE_NONCLAIM", reason="this is a live derivation checkpoint with major gates still open"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2424_0_status", decision="FINITE_Q_RUNNER_REBASED_ON_CURRENT_2423", rationale="2423 demoted phase-locking and selected finite q residual physics; 2284-2290 already map the same battlefield", consequence="do not redo old loops blindly"),
        base_row(decision_id="DEC2424_1_best_leap", decision="ATTACK_PARENT_FINITE_QUADRATIC_ROW_AND_SOURCE_TEST_SPLIT", rationale="Z_q/M_q^2/j_q and beta_source/beta_test are the first inputs that can turn finite q into testable physics", consequence="next target should try the parent finite q quadratic row"),
        base_row(decision_id="DEC2424_2_auxiliary_zero", decision="AUXILIARY_ZERO_ROUTE_REMAINS_CLEAN_BUT_UNSIGNED", rationale="second-class auxiliary elimination would be the elegant GR route, but parent protection contract is not derived from primitives", consequence="retain as future theorem/closure, not as claim"),
        base_row(decision_id="DEC2424_3_claim_policy", decision="KEEP_PRIVATE_NONCLAIM", rationale="local-GR/Newton recovery is not proven and no finite coefficient row is live", consequence="no GitHub action and no public local-test claim"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2424_0_selected",
            selection_status="selected",
            target_file="2425-Y5-R2FR-parent-finite-quadratic-q-row-and-source-test-coupling-split.md",
            target_script="scripts/Y5_R2FR_parent_finite_quadratic_q_row_and_source_test_coupling_split_2425.py",
            objective="derive or demote the parent finite q/R_AB quadratic action row that supplies Z_q, M_q^2/lambda_q, j_q, beta_source, beta_test, and the c_g versus c_g^2 coupling law",
            success_condition="either a parent finite quadratic q-row becomes theorem-zero/source-backed nonclaim-ready, or the exact missing clauses are carried as coefficient-acquisition rows without scoring",
            do_not_do="do not digitize external curves as a substitute for MTS-side coefficients, set tau_R10=1, score linear c_g without identifying source/test legs, or edit formalization-workbench",
        ),
        base_row(
            route_id="NEXT2424_1_parallel",
            selection_status="held_parallel",
            target_file="2425b-Y5-R2FR-auxiliary-protection-contract-from-primitives-or-closure-label.md",
            target_script="scripts/Y5_R2FR_auxiliary_protection_contract_from_primitives_or_closure_label_2425b.py",
            objective="try one narrow derivation of the second-class auxiliary protection contract from motion/time/space primitives",
            success_condition="joint parent contract kills J_R/B_R/readout/Z_q, or remains explicit closure-only",
            do_not_do="do not spend zero-route credit from separate unsigned clauses",
        ),
    ]


def copy_branch_rows(
    branch_state: list[dict[str, Any]],
    projection_gates: list[dict[str, Any]],
    decision_ledger: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["branch_state"], COPY_TARGETS["queue"], branch_state),
        ("branch_wep", OUTPUTS["projection_gates"], COPY_TARGETS["branch_wep"], projection_gates),
        ("beta_docs", OUTPUTS["decision"], COPY_TARGETS["beta_docs"], decision_ledger),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, copied_rows in copy_specs:
        write_csv(target_path, copied_rows)
        rows.append(
            base_row(
                copy_id=f"BC2424_{copy_id}",
                source_path=source_path,
                target_path=target_path,
                target_exists=target_path.exists(),
                row_count=len(copied_rows),
                purpose="current finite-q residual nonclaim bridge",
            )
        )
    return rows


def formalization_has_2424_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2424-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2424*",
        "*P8_Y5_BRR545_2424*",
        "*Y5_R2FR_finite_q_residual_coefficient_source_or_local_benchmark_runner_2424*",
        "*JR2424*",
        "*PARENT_QLOC_FINITE_Q_RESIDUAL_DECISION_2424*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def claim_flags_safe(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            for key in ("valid_for_claim", "claim_allowed", "score_ready", "parent_prediction_ready"):
                value = row.get(key)
                if value is True or stringify(value).lower() == "true":
                    if key in {"valid_for_claim", "claim_allowed", "score_ready", "parent_prediction_ready"}:
                        if row.get("translation_ready") is True and key == "translation_ready":
                            continue
                        return False
    return True


def build_validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    missing_rows = rows_by_name["missing_inputs"]
    projection_rows = rows_by_name["projection_gates"]
    decision_rows_local = rows_by_name["decision"]
    next_rows = rows_by_name["next_target"]

    csv_results = []
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        parses, row_count, message = csv_parses(path)
        csv_results.append((name, parses, row_count, message))
    for copy_key, copy_path in COPY_TARGETS.items():
        parses, row_count, message = csv_parses(copy_path)
        csv_results.append((f"copy_{copy_key}", parses, row_count, message))

    checks = [
        ("VAL2424_SOURCES_EXIST", all(row["path_exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL2424_NEEDLES_FOUND", all(row["needles_found"] for row in source_rows), "all source needles found"),
        ("VAL2424_OLD_CHAIN_IMPORTED", any(row["source_id"] == "SRC2424_07_2290_zq_tau" and row["needles_found"] for row in source_rows), "finite-q/R10 chain imported through 2290"),
        ("VAL2424_MISSING_STACK_COMPLETE", {row["input_id"] for row in missing_rows} >= {"MISS2424_0_Zq", "MISS2424_1_Mq2", "MISS2424_2_jq", "MISS2424_4_beta_split", "MISS2424_6_source_norm"}, "missing finite-q coefficient stack complete"),
        ("VAL2424_PROJECTIONS_BLOCKED", all(not row["parent_prediction_ready"] for row in projection_rows), "projection gates remain unscoreable"),
        ("VAL2424_NEXT_SELECTED", any(row["route_id"] == "NEXT2424_0_selected" and "finite-quadratic" in row["target_file"] for row in next_rows), "parent finite quadratic q-row selected next"),
        ("VAL2424_NO_PUBLIC_CLAIM", any(row["decision"] == "KEEP_PRIVATE_NONCLAIM" for row in decision_rows_local), "private nonclaim decision retained"),
        ("VAL2424_FLAGS_SAFE", claim_flags_safe(rows_by_name), "no generated row is valid_for_claim, claim_allowed, score_ready, or parent-prediction-ready"),
        ("VAL2424_BRANCH_COPIES", all(row["target_exists"] for row in branch_copy_rows), "branch copy files written"),
        ("VAL2424_CSV_PARSE", all(item[1] and item[2] > 0 for item in csv_results), "all generated CSV and branch copies parse with rows"),
        ("VAL2424_NO_FORMALIZATION_OUTPUT", not formalization_has_2424_artifacts(), "no 2424 artifacts written into formalization-workbench"),
    ]

    rows = [
        base_row(
            validation_id=validation_id,
            status="PASS" if passed else "FAIL",
            detail=detail,
            fatal=not passed,
        )
        for validation_id, passed, detail in checks
    ]
    overall_passed = all(row["status"] == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2424_OVERALL",
            status="PASS" if overall_passed else "FAIL",
            detail="2424 rebases the finite-q residual runner on the current 2423 handoff, imports the old 2284-2290 finite-q/R10 chain, keeps claims blocked, and selects parent finite quadratic q-row plus source/test coupling split next",
            fatal=not overall_passed,
        )
    )
    return rows


def write_document(rows_by_name: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> None:
    content = f"""# 2424 Y5 R2FR Finite q Residual Coefficient Source Or Local Benchmark Runner

## Result

This checkpoint rebases the old finite-`q` residual work onto the current 2423 coupling conclusion. The result is not a new local-GR claim; it is a cleaner route map.

The finite branch has a real normal form: if `q` is algebraic, `q_R=j_q/M_q^2`; if it has a gradient sector, `lambda_q=sqrt(Z_q/M_q^2)` or boundary hair must be projected. But none of `Z_q`, `M_q^2`, `j_q`, `B_R`, source normalization, or the R10 source/test split is parent-owned yet. So the next live target is the coupling row itself: a parent finite quadratic `q/R_AB` action row plus a source/test product law.

## Practical Status

- **Not circling:** 2424 imports the already-built 2284-2290 chain instead of rediscovering the same blockers.
- **Useful formula:** `q_R=j_q/M_q^2` is the algebraic finite residual relation, not a prediction until both coefficients are sourced.
- **R10 warning:** short-range scoring needs `alpha_R10(lambda)=K_q(lambda) beta_source beta_test + epsilon_tail`; a one-leg `c_g` shortcut is not scoreable.
- **Best next leap:** derive/source the finite quadratic `q` row and source/test coupling split.
- **Claim discipline:** local GR/Newton, R10, PPN, clock, WEP, and orbital passes remain blocked.

## Source Register

{table(["source_id", "source_path", "path_exists", "needles_found", "role"], rows_by_name["source_register"])}

## Finite q Branch State

{table(["state_id", "branch", "status", "what_is_known", "what_is_missing", "score_ready"], rows_by_name["branch_state"])}

## Missing Input Stack

{table(["input_id", "quantity", "needed_for", "current_status", "next_gate"], rows_by_name["missing_inputs"])}

## Projection Score Gates

{table(["gate_id", "arena", "translation_ready", "parent_prediction_ready", "blocker"], rows_by_name["projection_gates"])}

## Refusal Runner

{table(["refusal_id", "attempted_claim", "result", "reason"], rows_by_name["refusal"])}

## Decision Ledger

{table(["decision_id", "decision", "rationale", "consequence"], rows_by_name["decision"])}

## Next Target

{table(["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"], rows_by_name["next_target"])}

## Validation

{table(["validation_id", "status", "detail", "fatal"], validation_rows)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    rows_by_name = {
        "source_register": source_register_rows(),
        "branch_state": branch_state_rows(),
        "missing_inputs": missing_input_rows(),
        "projection_gates": projection_gate_rows(),
        "refusal": refusal_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    branch_copy_rows = copy_branch_rows(
        rows_by_name["branch_state"],
        rows_by_name["projection_gates"],
        rows_by_name["decision"],
    )
    rows_by_name["branch_copies"] = branch_copy_rows
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows)

    validation_rows = build_validation_rows(rows_by_name, branch_copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_document(rows_by_name, validation_rows)
    remove_pycache()

    overall = next(row for row in validation_rows if row["validation_id"] == "VAL2424_OVERALL")
    print(f"{DOC}")
    print(f"{OUTPUTS['validation']}")
    print(f"VAL2424_OVERALL={overall['status']}")


if __name__ == "__main__":
    main()
