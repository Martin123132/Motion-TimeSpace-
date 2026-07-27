from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2191"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2191-Y5-R2FR-q_loc-component-projection-runner-and-theorem-zero-certificate.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2191_SOURCE_REGISTER.csv",
    "component_schema": OUT / "P8_Y5_PARENT_QLOC_2191_QLOC_COMPONENT_SCHEMA.csv",
    "theorem_certificate": OUT / "P8_Y5_PARENT_QLOC_2191_THEOREM_ZERO_CERTIFICATE.csv",
    "projection_runner": OUT / "P8_Y5_PARENT_QLOC_2191_PROJECTION_RUNNER_SPEC.csv",
    "dry_run": OUT / "P8_Y5_PARENT_QLOC_2191_DRY_RUN_RESULTS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2191_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2191_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2191_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2191_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2191_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2191_QLOC_COMPONENT_PROJECTION_RUNNER_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2191_QLOC_COMPONENT_SCHEMA_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PARENT_QLOC_THEOREM_ZERO_CERTIFICATE_2191_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


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
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        values = []
        for column in columns:
            values.append(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|"))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2191_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2191-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2191*",
        "*P8_Y5_BRR545_2191*",
        "*Y5_R2FR_q_loc_component_projection_runner_and_theorem_zero_certificate_2191*",
        "*JR2191*",
        "*PARENT_QLOC_THEOREM_ZERO_CERTIFICATE_2191*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2190_handoff",
            ROOT / "2190-Y5-R2FR-GammaKhat-q_loc-coupling-double-zero-or-residual-lock.md",
            ["NEXT2190_0_2191", "q_loc residual components=11", "projection arenas covered=6/6"],
            "2190 selects an executable q_loc component projection runner and keeps theorem-zero false.",
        ),
        (
            "2190_residual_lock",
            OUT / "P8_Y5_PARENT_QLOC_2190_QLOC_RESIDUAL_LOCK_INTERFACE.csv",
            ["q_action_owner_defect", "q_loc_residual_vector_abs", "MISSING_COMPONENT_INPUTS"],
            "2190 residual lock supplies the component families carried into the runner.",
        ),
        (
            "2190_projection_queue",
            OUT / "P8_Y5_PARENT_QLOC_2190_LOCAL_TEST_PROJECTION_QUEUE.csv",
            ["PPN", "R10_short_range", "orbital_systems"],
            "2190 projection queue supplies the local arenas.",
        ),
        (
            "2190_derivation_gate",
            OUT / "P8_Y5_PARENT_QLOC_2190_DERIVATION_GATE.csv",
            ["S_GK exists", "Khat equals metric response", "q_loc theorem-zero status"],
            "2190 derivation gate supplies the all-or-nothing theorem-zero clauses.",
        ),
        (
            "1189_doc",
            ROOT / "1189-Y5-R10-q_loc-component-residual-pack-or-profile-theorem-zero-certificate.md",
            ["q_loc component residual pack", "theorem-zero certificate", "No claim"],
            "1189 provides the earlier component-template discipline and no-scalar-proxy rule.",
        ),
        (
            "1189_input_pack",
            OUT / "P8_Y5_R10_1189_QLOC_COMPONENT_RESIDUAL_INPUT_PACK.csv",
            ["QPACK1189_0_PPN_component_template", "QPACK1189_4_theorem_zero_override"],
            "1189 input pack provides component columns and theorem-zero override shape.",
        ),
        (
            "1189_theorem_certificate",
            OUT / "P8_Y5_R10_1189_THEOREM_ZERO_CERTIFICATE_TEMPLATE.csv",
            ["metric_response_owner", "P_loc_parent_domain", "arena_projection_silence"],
            "1189 theorem certificate confirms all current theorem clauses fail.",
        ),
        (
            "1191_old_projection_slots",
            ROOT / "1191-Y5-R10-curved-Khat-P_loc-commutator-bound-pack-or-parent-zero.md",
            ["Arena projection slots", "APS1191_2_R10", "MISSING_ARENA_PROJECTION_OPERATORS"],
            "older 1191 identifies exact residual leftovers and missing arena response operators.",
        ),
        (
            "q_loc_bound_spec",
            OUT / "P8_QLOC_BOUND_RUNNER_SPEC.csv",
            ["QB516_0_compact_shell_budget", "QB516_3_PPN_metric_tail", "QB516_4_R11_operator"],
            "q_loc bound spec supplies nonclaim smoke anchors and fallback arena meanings.",
        ),
    ]
    rows = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def component_schema_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QCS2191_0_common_schema",
            "all_arenas",
            "required_columns",
            "sample_id;domain_id;weight_dV;frame_convention;u0;u1;u2;u3;q0;q1;q2;q3;q_T;q_x;q_y;q_z;q_units;boundary_tag;boundary_condition;source_path;response_operator_id;theorem_zero_certificate_id",
            "component vector data in observed frame, not scalar proxy",
            "MISSING_REAL_QLOC_PROFILE;MISSING_OBSERVED_FRAME;MISSING_DOMAIN_MEASURE;MISSING_SOURCE_PATH",
            "template_only_not_scoreable",
        ),
        (
            "QCS2191_1_PPN",
            "PPN",
            "component_template",
            "q_T;q_L;q_TF;q_alpha_i;weak_field_gauge;source_normalization",
            "Delta_PPN_q = R_PPN[q_components]",
            "MISSING_PPN_RESPONSE_OPERATOR;MISSING_WEAK_FIELD_GREEN_OPERATOR;MISSING_COMPONENT_PROFILE",
            "template_only_not_scoreable",
        ),
        (
            "QCS2191_2_R10",
            "R10_short_range",
            "finite_range_kernel_template",
            "lambda_value;q_profile_lambda;c_q_alpha_lambda;range_kernel;bound_curve_id",
            "alpha_R10_q(lambda)=c_q_alpha(lambda)*q_profile(lambda)",
            "MISSING_RANGE_KERNEL;MISSING_CQ_ALPHA_LAMBDA;MISSING_REAL_BOUND_CURVE;MISSING_COMPONENT_PROFILE",
            "template_only_not_scoreable",
        ),
        (
            "QCS2191_3_R11",
            "R11_source_normalization",
            "operator_vector_template",
            "lambda_value;c_GK_operator_vector;source_measure_map;PiM_link;normalization",
            "c_GK_operator_vector(lambda)=R_R11[q_loc]",
            "MISSING_R11_OPERATOR_MAP;MISSING_SOURCE_MEASURE_NORMALIZATION;MISSING_PIM_LINK",
            "template_only_not_scoreable",
        ),
        (
            "QCS2191_4_clock",
            "clock_time",
            "clock_response_template",
            "q_T;q_frame_leak;b_clock_i;readout_frame;constant_marker_class",
            "Delta_clock_q=b_clock_i*Q_clock[q_components]",
            "MISSING_CLOCK_RESPONSE_COEFFICIENTS;MISSING_CLOCK_FRAME;MISSING_COMPONENT_PROFILE",
            "template_only_not_scoreable",
        ),
        (
            "QCS2191_5_orbital",
            "orbital_systems",
            "force_source_template",
            "q_r;q_t;force_to_acceleration;radial_profile;source_charge_equality",
            "a_q^i=R_orb^i_mu q_loc^mu or dlnmu_obs_dt=R_mu q_loc",
            "MISSING_ORBITAL_FORCE_MAP;MISSING_RADIAL_PROFILE;MISSING_SOURCE_CHARGE_EQUALITY",
            "template_only_not_scoreable",
        ),
        (
            "QCS2191_6_shell_smoke",
            "compact_shell_smoke",
            "nonclaim_smoke_template",
            "compact_shell_budget;domain;component_interpretation;do_not_promote",
            "dry-run only: confirms runner rejects smoke rows as claims",
            "NONCLAIM_SMOKE_ONLY;MISSING_ARENA_PROJECTION",
            "smoke_only_not_scoreable",
        ),
    ]
    return [
        base_row(schema_id=schema_id, arena=arena, row_kind=row_kind, required_fields=required_fields, projection_form=projection_form, missing_fields=missing_fields, row_status=row_status, score_ready=False)
        for schema_id, arena, row_kind, required_fields, projection_form, missing_fields, row_status in rows
    ]


def theorem_certificate_rows() -> list[dict[str, Any]]:
    rows = [
        ("TZ2191_0_action_owner", "S_GK_parent_action", "S_GK[g,Phi] is a source-signed local diffeomorphism-invariant action for Gamma/Khat", "MISSING_PARENT_S_GK", False),
        ("TZ2191_1_metric_response", "metric_response_owner", "K_hat equals the metric response of sqrt(-g)Gamma_eff with boundary convention declared", "MISSING_METRIC_RESPONSE_CERTIFICATE", False),
        ("TZ2191_2_Helmholtz", "Helmholtz_integrability", "second metric variation is symmetric up to allowed boundary terms", "MISSING_HELMHOLTZ_CERTIFICATE", False),
        ("TZ2191_3_Euler", "Euler_Ward_closure", "compact local vacuum Euler equations make nabla_mu T_GK^{mu nu}=0 up to included residual rows", "MISSING_EULER_CLOSURE_CERTIFICATE", False),
        ("TZ2191_4_double_zero", "T_GK_double_zero", "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0", "MISSING_DOUBLE_ZERO_CERTIFICATE", False),
        ("TZ2191_5_Ploc", "P_loc_parent_domain", "P_loc is parent-defined before readout and derivative commutator is zero or included", "MISSING_PARENT_PLOC_DOMAIN_CERTIFICATE", False),
        ("TZ2191_6_boundary", "boundary_no_flux", "theta_GK/Q_GK boundary and symplectic flux vanish or are included", "MISSING_BOUNDARY_NO_FLUX_CERTIFICATE", False),
        ("TZ2191_7_arenas", "arena_projection_silence", "same theorem silences or bounds PPN, R10, R11, clock and orbital projections", "MISSING_ARENA_PROJECTION_CERTIFICATES", False),
        ("TZ2191_8_all_or_nothing", "theorem_zero_status", "q_loc=0 is claimable only if every TZ2191_0..TZ2191_7 clause passes", "THEOREM_ZERO_FALSE", False),
    ]
    return [
        base_row(certificate_id=certificate_id, clause=clause, required_statement=required_statement, current_status=current_status, passes_now=passes_now)
        for certificate_id, clause, required_statement, current_status, passes_now in rows
    ]


def projection_runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN2191_0_PPN", "PPN", "Delta_PPN_q", "requires QCS2191_1_PPN plus response operator R_PPN and real q components", "blocked_missing_inputs", "MISSING_PPN_RESPONSE_OPERATOR;MISSING_COMPONENT_PROFILE", False),
        ("RUN2191_1_R10", "R10_short_range", "alpha_R10_q(lambda)", "requires QCS2191_2_R10 plus c_q_alpha(lambda), range kernel and real bound curve", "blocked_missing_inputs", "MISSING_RANGE_KERNEL;MISSING_CQ_ALPHA_LAMBDA;MISSING_REAL_BOUND_CURVE", False),
        ("RUN2191_2_R11", "R11_source_normalization", "c_GK_operator_vector(lambda)", "requires QCS2191_3_R11 plus source normalization and PiM link", "blocked_missing_inputs", "MISSING_R11_OPERATOR_MAP;MISSING_SOURCE_MEASURE_NORMALIZATION", False),
        ("RUN2191_3_clock", "clock_time", "Delta_clock_q", "requires QCS2191_4_clock plus clock coefficients and readout frame", "blocked_missing_inputs", "MISSING_CLOCK_RESPONSE_COEFFICIENTS;MISSING_CLOCK_FRAME", False),
        ("RUN2191_4_orbital", "orbital_systems", "Delta_orbital_q", "requires QCS2191_5_orbital plus force map and source charge equality", "blocked_missing_inputs", "MISSING_ORBITAL_FORCE_MAP;MISSING_SOURCE_CHARGE_EQUALITY", False),
        ("RUN2191_5_shell_smoke", "compact_shell_smoke", "compact_shell_budget", "accepts QB516_0 only as a dry-run nonclaim placeholder", "smoke_nonclaim_only", "NONCLAIM_SMOKE_ONLY;MISSING_ARENA_PROJECTION", False),
        ("RUN2191_6_theorem_zero", "all_local_arenas", "q_loc_zero_override", "requires every theorem certificate row to pass", "blocked_theorem_zero_false", "THEOREM_ZERO_FALSE", False),
    ]
    return [
        base_row(runner_id=runner_id, arena=arena, output_quantity=output_quantity, input_contract=input_contract, runner_status=runner_status, failure_reasons=failure_reasons, score_ready=score_ready)
        for runner_id, arena, output_quantity, input_contract, runner_status, failure_reasons, score_ready in rows
    ]


def dry_run_rows(component_rows: list[dict[str, Any]], theorem_rows: list[dict[str, Any]], runner_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    theorem_passes = all(str(row["passes_now"]).lower() == "true" for row in theorem_rows)
    missing_component_rows = [row for row in component_rows if "MISSING_" in str(row.get("missing_fields", "")) or row.get("score_ready") is False]
    runnable_rows = [row for row in runner_rows if str(row.get("score_ready", "")).lower() == "true"]
    rows = [
        base_row(dryrun_id="DR2191_0_theorem_zero", check="all theorem certificate clauses pass", result="PASS_BLOCKED_EXPECTED" if not theorem_passes else "FAIL_UNEXPECTED_PROMOTION", detail="theorem_zero remains false because at least one certificate row is missing"),
        base_row(dryrun_id="DR2191_1_components", check="component rows have real q_loc profiles", result="PASS_BLOCKED_EXPECTED" if missing_component_rows else "FAIL_UNEXPECTED_SCORE_READY", detail=f"missing/template component rows={len(missing_component_rows)}"),
        base_row(dryrun_id="DR2191_2_runner", check="arena projections are executable", result="PASS_BLOCKED_EXPECTED" if not runnable_rows else "FAIL_UNEXPECTED_RUNNABLE", detail=f"score_ready runner rows={len(runnable_rows)}"),
        base_row(dryrun_id="DR2191_3_no_scalar_proxy", check="scalar proxy cannot pass as vector proof", result="PASS_GUARDRAIL", detail="component schema requires q0..q3/q_T/q_x/q_y/q_z and response operators, not q_proxy alone"),
        base_row(dryrun_id="DR2191_4_claim_status", check="no local-GR/q_loc/R10/PPN claim allowed", result="PASS_NONCLAIM", detail="all rows remain valid_for_claim=false and claim_allowed=false"),
    ]
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2191_0_schema", "q_loc component schema exists", "PASS_GUARDRAIL", "runner requires observed-frame vector/domain/source columns"),
        ("CG2191_1_no_scalar_proxy", "scalar q_proxy alone can score local tests", "BLOCKED_NONCLAIM", "schema requires vector components and arena operators"),
        ("CG2191_2_theorem_zero", "q_loc=0 theorem certificate passes", "BLOCKED_NONCLAIM", "all theorem certificate clauses currently fail"),
        ("CG2191_3_projection_runner", "PPN/R10/R11/clock/orbital runner is score-ready", "BLOCKED_NONCLAIM", "response operators and real q_loc inputs are missing"),
        ("CG2191_4_smoke", "compact-shell smoke row is evidence", "BLOCKED_NONCLAIM", "smoke budget is a nonclaim dry-run placeholder only"),
        ("CG2191_5_local_GR", "full local-GR reduction can be claimed", "BLOCKED_NONCLAIM", "q_loc residual interface is explicit but unbounded"),
        ("CG2191_6_GitHub", "public/github update is triggered", "BLOCKED_NONCLAIM", "private goal work only; no GitHub action"),
    ]
    return [base_row(gate_id=gate_id, gate=gate, status=status, implication=implication) for gate_id, gate, status, implication in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2191_0_gain",
            "QLOC_RUNNER_INTERFACE_WRITTEN",
            "The residual lock is now executable in shape: components, theorem certificate, arena projection specs, and dry-run guards exist.",
            "selected",
        ),
        (
            "DEC2191_1_limit",
            "NO_ARENA_SCORE_READY",
            "Every arena remains blocked because response operators, source paths, units and real component profiles are missing.",
            "selected",
        ),
        (
            "DEC2191_2_next",
            "FIRST_RESPONSE_OPERATOR_OR_COMPONENT_ROW_NEXT",
            "The next testing move is to fill exactly one nonclaim response operator/component row, preferably R10 or PPN, before any scoring.",
            "selected",
        ),
    ]
    return [base_row(decision_id=decision_id, decision=decision, rationale=rationale, selection_status=status) for decision_id, decision, rationale, status in specs]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2191_0_2192",
            selection_status="selected",
            target_file="2192-Y5-R2FR-first-q_loc-response-operator-or-component-row-fill.md",
            target_script="scripts/Y5_R2FR_first_q_loc_response_operator_or_component_row_fill_2192.py",
            objective="fill the first real nonclaim q_loc projection input: either an R10 alpha(lambda) response operator/curve link or a PPN component response operator with units, source path and missing-data guard",
            success_condition="one arena row has a source path, declared units, response operator schema and valid_for_claim=false; placeholders remain blocked and theorem-zero stays false",
            do_not_do="do not claim q_loc=0, do not score smoke rows as evidence, do not invent response coefficients, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2191_1_theory_parallel",
            selection_status="held_parallel",
            target_file="2192b-Y5-R2FR-GK-action-owner-certificate-attempt.md",
            target_script="scripts/Y5_R2FR_GK_action_owner_certificate_attempt_2192b.py",
            objective="parallel derivation route: attempt to source-sign S_GK and K_hat metric response/Helmholtz clauses",
            success_condition="one theorem certificate clause becomes source-signed or is explicitly demoted to residual-only",
            do_not_do="do not promote partial theorem clauses into q_loc zero",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["projection_runner"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["component_schema"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["theorem_certificate"], BRANCH_COPIES["source_weight"]),
    ]
    rows = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("claim_allowed", "")).lower() == "true":
                return False
            if str(row.get("valid_for_claim", "")).lower() == "true":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    sources = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2191_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in sources)}/{len(sources)} sources exist"))
    validations.append(base_row(validation_id="VAL2191_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in sources)}/{len(sources)} source needle sets found"))

    schema_rows = rows_by_name["component_schema"]
    schema_text = ";".join(str(row.get("required_fields", "")) for row in schema_rows)
    schema_pass = "q0;q1;q2;q3" in schema_text and "q_T;q_x;q_y;q_z" in schema_text and any(row["arena"] == "R10_short_range" for row in schema_rows)
    validations.append(base_row(validation_id="VAL2191_02_component_schema", status="PASS" if schema_pass else "FAIL", detail=f"component schema rows={len(schema_rows)} with vector fields and arena templates"))

    theorem_rows = rows_by_name["theorem_certificate"]
    theorem_false = all(str(row["passes_now"]).lower() == "false" for row in theorem_rows)
    validations.append(base_row(validation_id="VAL2191_03_theorem_zero_false", status="PASS" if theorem_false else "FAIL", detail="all theorem-zero certificate clauses remain false/nonclaim"))

    arenas = {row["arena"] for row in rows_by_name["projection_runner"]}
    required_arenas = {"PPN", "R10_short_range", "R11_source_normalization", "clock_time", "orbital_systems", "compact_shell_smoke", "all_local_arenas"}
    validations.append(base_row(validation_id="VAL2191_04_projection_runner_coverage", status="PASS" if required_arenas.issubset(arenas) else "FAIL", detail=f"projection runner arenas={len(required_arenas.intersection(arenas))}/{len(required_arenas)}"))

    dry_results = {row["result"] for row in rows_by_name["dry_run"]}
    validations.append(base_row(validation_id="VAL2191_05_dryrun_blocks", status="PASS" if "FAIL_UNEXPECTED_PROMOTION" not in dry_results and "FAIL_UNEXPECTED_RUNNABLE" not in dry_results else "FAIL", detail="dry-run blocks theorem-zero, placeholder components and arena scoring"))

    claim_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    validations.append(base_row(validation_id="VAL2191_06_claim_gate", status="PASS" if "PASS_GUARDRAIL" in claim_statuses and "BLOCKED_NONCLAIM" in claim_statuses else "FAIL", detail="claim gate blocks q_loc/local-GR while preserving runner interface"))

    decisions = {row["decision"] for row in rows_by_name["decision"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2191_07_decision", status="PASS" if "FIRST_RESPONSE_OPERATOR_OR_COMPONENT_ROW_NEXT" in decisions else "FAIL", detail="decision selects first sourced nonclaim response/component row next"))

    routes = {row["route_id"] for row in rows_by_name["next_target"] if row["selection_status"] == "selected"}
    validations.append(base_row(validation_id="VAL2191_08_next_target", status="PASS" if "NEXT2191_0_2192" in routes else "FAIL", detail="2192 first q_loc response/component fill selected"))

    validations.append(base_row(validation_id="VAL2191_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok and count > 0
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2191_10_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copies = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2191_11_branch_copies", status="PASS" if copies and all(row["copied"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    validations.append(base_row(validation_id="VAL2191_12_formalization_clean", status="PASS" if not formalization_has_2191_artifacts() else "FAIL", detail="formalization-workbench has no 2191 artifacts"))

    remove_pycache()
    validations.append(base_row(validation_id="VAL2191_13_pycache_absent", status="PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = "PASS" if all(row["status"] == "PASS" for row in validations) else "FAIL"
    validations.append(base_row(validation_id="VAL2191_OVERALL", status=overall, detail="2191 makes q_loc residual lock executable in schema/dry-run form, keeps theorem-zero false, and selects first sourced response/component row next"))
    return validations


def render_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    sections = [
        "# 2191 - Y5/R2FR q_loc Component Projection Runner And Theorem-Zero Certificate",
        "",
        "## Current Verdict",
        "",
        "2191 turns the `q_loc` residual lock into an executable interface shape. It does **not** score physics yet.",
        "",
        "The important guardrail is now mechanical: no scalar proxy and no smoke budget can pass as local GR. Either every theorem-zero certificate clause passes, or each arena needs real component data, units, source paths, and a response operator.",
        "",
        "## Source Register",
        "",
        md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## q_loc Component Schema",
        "",
        md_table(rows_by_name["component_schema"], ["schema_id", "arena", "row_kind", "required_fields", "projection_form", "missing_fields", "row_status", "score_ready", "valid_for_claim"]),
        "",
        "## Theorem-Zero Certificate",
        "",
        md_table(rows_by_name["theorem_certificate"], ["certificate_id", "clause", "required_statement", "current_status", "passes_now", "valid_for_claim"]),
        "",
        "## Projection Runner Spec",
        "",
        md_table(rows_by_name["projection_runner"], ["runner_id", "arena", "output_quantity", "input_contract", "runner_status", "failure_reasons", "score_ready", "valid_for_claim"]),
        "",
        "## Dry-Run Results",
        "",
        md_table(rows_by_name["dry_run"], ["dryrun_id", "check", "result", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Claim Gate",
        "",
        md_table(rows_by_name["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Interpretation",
        "",
        "This is where derivation and testing finally touch without cheating. The theory route can still prove `q_loc=0`, but the empirical route now knows exactly what it would need if the proof does not close.",
        "",
        "Next best move: fill one real nonclaim projection input, likely R10 or PPN, with source path, units, response operator, and a dry-run that still refuses claims.",
        "",
    ]
    return "\n".join(sections)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    component_rows = component_schema_rows()
    theorem_rows = theorem_certificate_rows()
    runner_rows = projection_runner_rows()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "component_schema": component_rows,
        "theorem_certificate": theorem_rows,
        "projection_runner": runner_rows,
        "dry_run": dry_run_rows(component_rows, theorem_rows, runner_rows),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])

    DOC.write_text(render_doc(rows_by_name), encoding="utf-8")
    remove_pycache()


if __name__ == "__main__":
    main()
