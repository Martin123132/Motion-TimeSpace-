from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "1965-Y5-R2FR-R2-fR-zero-proof-or-executable-R11-bound-row.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1965_VALIDATION.csv"

SOURCES = {
    "1964_doc": {
        "path": ROOT / "1964-Y5-R2FR-owned-coframe-legitimacy-and-EH-second-order-gate.md",
        "needles": ["R11X1964_0_R2_fR_scalar", "EH2_1964_2_central_blocker", "NEXT1964_0_primary"],
    },
    "1964_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1964_VALIDATION.csv",
        "needles": ["VAL1964_OVERALL", "PASS"],
    },
    "1339_eh_gate": {
        "path": ROOT / "1339-Y5-R10-RAB-source-closure-to-EH-left-hand-local-GR-reduction-gate.md",
        "needles": ["R11V1339_0_R2_fR_scalar", "EHGate1339_2_second_order", "SHORT1339_1_no_Lovelock_without_premises"],
    },
    "1340_interface": {
        "path": ROOT / "1340-Y5-R10-RAB-EH-core-selection-or-first-executable-R11-residual-interface.md",
        "needles": ["EH1340_2_R2FR_obstruction", "R11SCHEMA1340_1_R2FR", "ZERO1340_0_R2FR"],
    },
    "958_premise_csv": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_958_EH_PREMISE_AUDIT.csv",
        "needles": ["EHP958_P6_second_order"],
    },
    "960_attempt_csv": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_960_R2_FR_ZERO_OR_BOUND_ATTEMPT.csv",
        "needles": ["R2FR960_1_second_order_filter", "R2FR960_4_verdict"],
    },
    "960_bound_pack": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_960_PRIORITY_BOUND_PACK.csv",
        "needles": ["BPACK960_0", "R2_fR_scalar_mode"],
    },
    "963_runner_spec": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_963_R2FR_BOUND_RUNNER_SPEC.csv",
        "needles": ["R2RUN963_4_decision_logic"],
    },
    "964_minimality": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv",
        "needles": ["MIN964_5_verdict", "THEOREM_NOT_PROVEN_CURRENT_CORPUS"],
    },
    "964_runner": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_964_R2FR_NONCLAIM_RUNNER_RESULT.csv",
        "needles": ["R2RUN964_VERDICT", "R2FR_BRANCH_BLOCKED_NONCLAIM"],
    },
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for directory in (MTS_RESIDUALS, SOURCE_WEIGHT_DOCS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def base(row_id: str) -> dict[str, object]:
    return {
        "branch": BRANCH,
        "row_id": row_id,
        "valid_for_claim": False,
        "public_claim": False,
        "created_utc": stamp(),
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_id, source_spec in SOURCES.items():
        path = source_spec["path"]
        needles = source_spec["needles"]
        exists = path.exists()
        text = path.read_text(encoding="utf-8", errors="replace") if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base(source_id)
        row.update(
            {
                "source_path": str(path),
                "purpose": "1965 R2/fR zero proof or executable R11 bound row",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def zero_proof_rows() -> list[dict[str, object]]:
    entries = [
        (
            "ZP1965_0_target",
            "derive c_R2=c_fR=0 for the compact local exterior, or retain R2/fR as a scalar-mode R11 residual",
            "S_ext includes sqrt(-g)(R - 2 Lambda + c_R2 R^2 + higher f_extra(R)); target c_R2=f_RR=0",
            "TARGET_EXACT",
            "This is the central second-order bridge to EH.",
            "parent zero theorem or executable scalar bound row",
        ),
        (
            "ZP1965_1_second_order_filter",
            "R^2/generic f(R) produces fourth-order metric equations or an equivalent scalaron unless its coefficient is zero/redundant",
            "delta int sqrt(-g) R^2 contains derivatives of R; f_RR != 0 gives scalar degree",
            "FILTER_CLEAN",
            "The filter tells us what must vanish; it is not by itself a parent derivation.",
            "need coefficient origin",
        ),
        (
            "ZP1965_2_topological_escape",
            "R^2 and generic f(R) are not the 4D topological Gauss-Bonnet invariant",
            "R^2 != Euler density; f_RR scalar mode remains unless special redundancy is proved",
            "TOPOLOGICAL_ESCAPE_REJECTED",
            "Cannot hide this residual as a harmless boundary term.",
            "only a true field-redefinition or boundary proof would remove observables",
        ),
        (
            "ZP1965_3_minimality_route",
            "A parent minimality/no-extension theorem would kill R2/fR if the primitive MTS quotient admits no curvature-square invariant generator and no integrated-out scalar tower",
            "Primitive MTS quotient + local first-jet/coframe action + no hidden integrated-out tower => c_R2=f_RR=0",
            "POSSIBLE_ZERO_ROUTE_NOT_PARENT_SIGNED",
            "This is the cleanest derivation route, but 964 says the theorem is not proven.",
            "derive primitive quotient/invariant algebra minimality",
        ),
        (
            "ZP1965_4_integrated_out_blocker",
            "Even if R2/fR is absent in the primitive ansatz, hidden sectors can generate it after reduction",
            "integrating out Xi may yield Delta S_eff[g] with R^2, f(R), Yukawa scalar, or nonlocal kernel",
            "ZERO_PROOF_BLOCKED_BY_EFFECTIVE_ACTION",
            "Need no-tower/no-scalar-pole theorem, not just a clean starting Lagrangian.",
            "prove Xi has no local scalar pole and no curvature-square counterterm",
        ),
        (
            "ZP1965_5_stability_blocker",
            "Ostrogradsky or stability intuition is insufficient because R^2/f(R) can be recast as scalar-tensor dynamics",
            "R + c_R2 R^2 <-> GR plus scalaron for c_R2 > 0 in the usual normalization",
            "STABILITY_NOT_ZERO_CERTIFICATE",
            "Stability can constrain sign/mass but does not erase the scalar mode.",
            "need a parent constraint, gauge redundancy, or measured bound",
        ),
        (
            "ZP1965_6_verdict",
            "Current corpus does not prove c_R2=f_RR=0",
            "ZP1965_3 through ZP1965_5 remain unsigned",
            "ZERO_PROOF_FAILED_CLEANLY",
            "Do not claim EH second-order selection; move to executable scalar residual unless the minimality theorem is strengthened.",
            "build scalaron alpha(lambda)/PPN/R10 row",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, clause, math_form, status, implication, required_fix in entries:
        row = base(row_id)
        row.update(
            {
                "clause": clause,
                "math_form": math_form,
                "status": status,
                "implication": implication,
                "required_fix": required_fix,
            }
        )
        rows.append(row)
    return rows


def scalar_map_rows() -> list[dict[str, object]]:
    entries = [
        (
            "SM1965_0_normalization",
            "R_plus_cR2R2",
            "S=(1/2kappa) int sqrt(-g)(R + c_R2 R^2)",
            "c_R2 has length^2 in c=1 units; f_RR=2 c_R2 at R=0 for this normalization",
            "NORMALIZATION_DECLARED_NONCLAIM",
            "all future coefficients must state normalization before comparison",
        ),
        (
            "SM1965_1_scalar_mass",
            "scalaron_mass",
            "m_s^2 = 1/(6 c_R2) for R + c_R2 R^2 with c_R2>0",
            "lambda_s = 1/m_s = sqrt(6 c_R2) in c=hbar=1 units",
            "FORMULA_ROUTE_DECLARED",
            "requires numeric c_R2 with units and sign",
        ),
        (
            "SM1965_2_yukawa_alpha",
            "unscreened_metric_fR_yukawa",
            "Phi(r) = -G M/r * (1 + alpha_s exp(-r/lambda_s))",
            "alpha_s = 1/3 for the standard unscreened metric f(R) scalar branch",
            "FORMULA_ROUTE_DECLARED",
            "screening and branch context must be explicit; do not infer alpha if parent model differs",
        ),
        (
            "SM1965_3_PPN_regime",
            "long_range_scalar_PPN",
            "gamma_eff(r) approximately (1 - alpha_s exp(-r/lambda_s))/(1 + alpha_s exp(-r/lambda_s)) in simple Yukawa scalar limit",
            "maps to Cassini/gamma only when scalar range and environment match the solar-system regime",
            "PPN_MAP_CONDITIONAL",
            "requires range, screening, source model, and regime certificate",
        ),
        (
            "SM1965_4_R10_regime",
            "finite_range_R10",
            "compare alpha_s at lambda_s to source-backed alpha_bound(lambda)",
            "pass only if full bound curve is valid_for_claim and abs(alpha_s)<=alpha_bound(lambda_s)",
            "R10_MAP_CONDITIONAL",
            "anchor-only rows are smoke data, not evidence",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, map_id, formula, units_or_regime, status, required_fix in entries:
        row = base(row_id)
        row.update(
            {
                "map_id": map_id,
                "formula": formula,
                "units_or_regime": units_or_regime,
                "status": status,
                "required_fix": required_fix,
            }
        )
        rows.append(row)
    return rows


def executable_bound_rows() -> list[dict[str, object]]:
    entries = [
        (
            "EXR1965_0_zero_switch",
            "zero_theorem",
            "c_R2=f_RR=0",
            "parent_minimality_no_extension_and_no_integrated_out_tower_signed",
            "REJECTED_ZERO_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim only if zero certificate cites parent action clauses",
        ),
        (
            "EXR1965_1_mts_prediction",
            "numeric_prediction",
            "c_R2_or_fRR; coefficient_units; normalization; sign; scalar_mass_or_lambda; alpha_s; screening_flag",
            "MISSING_PARENT_NUMERIC_COEFFICIENT",
            "REJECTED_MISSING_EXECUTABLE_INPUTS",
            "MTS must predict coefficient, not fit it to the bound",
        ),
        (
            "EXR1965_2_R10_bound_curve",
            "external_bound_curve",
            "lambda_value; lambda_units; alpha_bound; source_url_or_path; extraction_method; full_curve=true",
            "MISSING_VALID_FULL_CURVE",
            "REJECTED_MISSING_FULL_CURVE",
            "anchor-only threshold rows are permitted for smoke tests only",
        ),
        (
            "EXR1965_3_PPN_bound",
            "PPN_gamma_beta",
            "gamma_predicted; beta_predicted; scalar_range_regime; screening_context; source_bound_path",
            "MISSING_SOLAR_SYSTEM_REGIME_MAP",
            "REJECTED_MISSING_PPN_PROJECTION",
            "long-range scalar cannot be scored without regime map",
        ),
        (
            "EXR1965_4_decision_logic",
            "claim_gate",
            "zero_theorem_signed OR numeric_prediction_complete AND bound_curve_valid AND PPN_regime_valid_if_applicable",
            "CURRENTLY_FALSE",
            "R2FR_BRANCH_BLOCKED_NONCLAIM",
            "no EH/local-GR claim while false",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, row_type, required_fields, missing_now, runner_status, acceptance_rule in entries:
        row = base(row_id)
        row.update(
            {
                "row_type": row_type,
                "required_fields": required_fields,
                "missing_now": missing_now,
                "runner_status": runner_status,
                "acceptance_rule": acceptance_rule,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        (
            "RUN1965_0_zero_switch",
            "EXR1965_0_zero_switch",
            False,
            "REJECTED_ZERO_THEOREM_NOT_PARENT_SIGNED",
            "parent minimality/no-extension/no-tower theorem not signed",
        ),
        (
            "RUN1965_1_numeric_prediction",
            "EXR1965_1_mts_prediction",
            False,
            "REJECTED_MISSING_EXECUTABLE_INPUTS",
            "coefficient, units, sign, mass/range, alpha, source path missing",
        ),
        (
            "RUN1965_2_R10_curve",
            "EXR1965_2_R10_bound_curve",
            False,
            "REJECTED_MISSING_FULL_CURVE",
            "current prior rows include anchor-only/full-curve-missing status",
        ),
        (
            "RUN1965_3_PPN_projection",
            "EXR1965_3_PPN_bound",
            False,
            "REJECTED_MISSING_PPN_PROJECTION",
            "solar-system scalar regime and screening certificate missing",
        ),
        (
            "RUN1965_VERDICT",
            "all_rows",
            False,
            "R2FR_BRANCH_BLOCKED_NONCLAIM",
            "zero proof failed and executable finite scalar row is not populated",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, input_row, accepted, runner_status, reason in entries:
        row = base(row_id)
        row.update(
            {
                "input_row": input_row,
                "accepted": accepted,
                "runner_status": runner_status,
                "reason": reason,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1965_0_filter", "R2/fR is identified as a non-EH scalar-mode obstruction.", "PASS_NONCLAIM", "filter only"),
        ("CG1965_1_zero", "c_R2=f_RR=0 is parent-derived.", "FAIL_BLOCKED", "minimality/no-extension/no-tower theorem missing"),
        ("CG1965_2_bound", "finite scalar residual is executable.", "FAIL_BLOCKED", "MTS coefficient and full bound curve missing"),
        ("CG1965_3_EH_second_order", "EH second-order premise is proven.", "FAIL_BLOCKED", "R2/fR zero-or-bound unresolved"),
        ("CG1965_4_local_GR_Newton", "local GR/Newton derived.", "FAIL_BLOCKED", "EH, GM-transfer, PPN gates remain"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, claim, status, reason in entries:
        row = base(row_id)
        row.update({"claim": claim, "status": status, "reason": reason})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    entries = [
        (
            "DEC1965_0_verdict",
            "R2FR_ZERO_PROOF_FAILED_EXECUTABLE_BOUND_ROUTE_READY_BUT_EMPTY",
            "The derivative-order/topology filter is clean, but the parent coefficient zero is not derived; scalaron residual rows now state exact coefficient, mass/range, alpha, PPN, and R10 requirements.",
            "do not claim EH; populate the finite scalar branch or strengthen minimality",
        ),
        (
            "DEC1965_1_next",
            "SOURCE_BACKED_R2FR_BOUND_INPUTS_OR_PARENT_MINIMALITY",
            "The fastest empirical route is to acquire a real full alpha(lambda) curve and keep MTS coefficient rows nonclaim until parent coefficients exist.",
            "build 1966 data acquisition/smoke runner or derive E[q(Phi_MTS)]/minimality if staying theoretical",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1965_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1966-Y5-R2FR-R2FR-bound-curve-and-parent-coefficient-smoke-runner.md",
            "target_script": "scripts/Y5_R2FR_R2FR_bound_curve_and_parent_coefficient_smoke_runner_1966.py",
            "objective": "acquire or stage source-backed full R2/fR scalar alpha(lambda) bound inputs and keep MTS coefficient predictions nonclaim until parent coefficients exist",
            "acceptance_output": "full-curve acquisition ledger, MTS coefficient placeholder refusal, alpha(lambda)/PPN smoke runner, no EH claim",
            "nonclaim_rule": "anchor-only bounds and missing parent coefficients cannot score the branch",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1965_0_project_position")
    row.update(
        {
            "strongest_result": "R2/fR is no longer vague: if it survives, it is a scalaron/Yukawa residual with explicit mass/range/coupling and R10/PPN interfaces.",
            "what_improved": "The EH second-order obstruction is now executable rather than merely named.",
            "still_missing": "parent minimality/no-extension proof, no integrated-out scalar tower, numeric c_R2/f_RR, valid full alpha(lambda) bound curve, PPN regime map, GM transfer",
            "claim_status": "R2/fR zero not proven and scalar residual not scoreable yet; no EH/local-GR/Newton claim",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1965_SOURCE_REGISTER.csv",
    "zero_proof": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1965_R2FR_ZERO_PROOF_ATTEMPT.csv",
    "scalar_map": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1965_R2FR_SCALARON_MAP.csv",
    "executable_bound": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1965_R2FR_EXECUTABLE_BOUND_SCHEMA.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1965_R2FR_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1965_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1965_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1965_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1965_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "R2FR_ZERO_OR_SCALAR_BOUND_1965_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1965_R2FR_BOUND_CURVE_PARENT_COEFFICIENT_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1965_0_nonclaim_weight"),
            "artifact": "1965 R2/fR zero proof or executable scalar bound row",
            "weight": "ZERO_FAILED_EXECUTABLE_INTERFACE_READY_EMPTY",
            "reason": "filter and scalar map are useful, but no parent zero or numeric score row exists",
        }
    ]
    queue = [
        {
            **base("AQ1965_0_bound_curve"),
            "target": "full alpha(lambda) bound curve for scalar fifth-force/R10 branch",
            "needed_inputs": "lambda; alpha_bound; units; source path/url; extraction method; full_curve flag; valid_for_claim",
            "priority": "HIGH",
        },
        {
            **base("AQ1965_1_parent_coefficient"),
            "target": "MTS c_R2/f_RR parent coefficient",
            "needed_inputs": "coefficient; units; normalization; branch context; sign; source equation; scalar mass/range map",
            "priority": "HIGHEST_FOR_CLAIM",
        },
    ]
    return {
        "source_register": source_register(),
        "zero_proof": zero_proof_rows(),
        "scalar_map": scalar_map_rows(),
        "executable_bound": executable_bound_rows(),
        "runner": runner_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
        "snapshot": snapshot_rows(),
        "source_weight": source_weight,
        "queue": queue,
    }


def validation_row(validation_id: str, status: str, detail: str) -> dict[str, object]:
    return {
        "validation_id": validation_id,
        "status": status,
        "detail": detail,
        "valid_for_claim": False,
        "public_claim": False,
    }


def formalization_hits() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = ("1965-", "*_1965_*", "*Y5*1965*", "*VAL1965*", "*P8*1965*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1965_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    filter_ok = any(row["row_id"] == "ZP1965_1_second_order_filter" and row["status"] == "FILTER_CLEAN" for row in tables["zero_proof"])
    zero_fail_ok = any(row["row_id"] == "ZP1965_6_verdict" and row["status"] == "ZERO_PROOF_FAILED_CLEANLY" for row in tables["zero_proof"])
    rows.append(validation_row("VAL1965_01_zero_attempt", "PASS" if filter_ok and zero_fail_ok else "FAIL", "R2/fR filter clean and zero proof not claimed"))

    scalar_map_ok = any(row["row_id"] == "SM1965_1_scalar_mass" and "1/(6 c_R2)" in row["formula"] for row in tables["scalar_map"])
    alpha_ok = any(row["row_id"] == "SM1965_2_yukawa_alpha" and "1/3" in row["units_or_regime"] for row in tables["scalar_map"])
    rows.append(validation_row("VAL1965_02_scalar_map", "PASS" if scalar_map_ok and alpha_ok else "FAIL", "scalaron mass and alpha map recorded"))

    executable_ok = any(row["row_id"] == "EXR1965_1_mts_prediction" and row["runner_status"] == "REJECTED_MISSING_EXECUTABLE_INPUTS" for row in tables["executable_bound"])
    curve_ok = any(row["row_id"] == "EXR1965_2_R10_bound_curve" and row["runner_status"] == "REJECTED_MISSING_FULL_CURVE" for row in tables["executable_bound"])
    rows.append(validation_row("VAL1965_03_executable_schema", "PASS" if executable_ok and curve_ok else "FAIL", "executable scalar bound schema rejects missing inputs"))

    runner_ok = any(row["row_id"] == "RUN1965_VERDICT" and row["runner_status"] == "R2FR_BRANCH_BLOCKED_NONCLAIM" for row in tables["runner"])
    rows.append(validation_row("VAL1965_04_runner", "PASS" if runner_ok else "FAIL", "runner dryrun blocks branch"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1965_3_EH_second_order" and row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1965_05_claim_gates", "PASS" if gate_ok else "FAIL", "EH/local-GR claims remain blocked"))

    decision_ok = any(row["decision"] == "R2FR_ZERO_PROOF_FAILED_EXECUTABLE_BOUND_ROUTE_READY_BUT_EMPTY" for row in tables["decision"])
    rows.append(validation_row("VAL1965_06_decision", "PASS" if decision_ok else "FAIL", "zero failed and bound route selected"))

    next_ok = tables["next"][0]["target_doc"] == "1966-Y5-R2FR-R2FR-bound-curve-and-parent-coefficient-smoke-runner.md"
    rows.append(validation_row("VAL1965_07_next_target", "PASS" if next_ok else "FAIL", "1966 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1965_08_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1965_09_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1965_10_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1965_11_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1965_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1965_OVERALL", overall, "1965 R2/fR zero proof or executable R11 bound row"))
    return rows


def markdown_table(rows: list[dict[str, object]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, object]]], validation_rows: list[dict[str, object]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("R2/fR Zero Proof Attempt", tables["zero_proof"]),
        ("Scalaron Map", tables["scalar_map"]),
        ("Executable Bound Schema", tables["executable_bound"]),
        ("Runner Dryrun", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1965 Y5 R2FR: R2/fR Zero Proof Or Executable R11 Bound Row",
        "",
        "Private checkpoint. This attacks the central second-order obstruction directly: can the local exterior forbid R2/fR scalar curvature corrections, or must they become a scoreable scalar fifth-force residual?",
        "",
        "Verdict: the zero proof fails cleanly. The second-order filter is valid, but the parent minimality/no-extension/no-integrated-out-tower theorem is not signed. The fallback is now explicit: R2/fR maps to a scalaron/Yukawa branch with coefficient, mass/range, alpha(lambda), PPN, and bound-curve requirements.",
        "",
        "No EH, Newton, or local-GR claim follows from this checkpoint.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1965_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
