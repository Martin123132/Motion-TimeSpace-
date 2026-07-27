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

DOC_PATH = ROOT / "1967-Y5-R2FR-parent-minimality-or-R2FR-coefficient-origin.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1967_VALIDATION.csv"

SOURCES = {
    "1966_doc": {
        "path": ROOT / "1966-Y5-R2FR-R2FR-bound-curve-and-parent-coefficient-smoke-runner.md",
        "needles": ["MTS1966_0_parent_coefficient_required", "DEC1966_0_verdict", "NEXT1966_0_primary"],
    },
    "1966_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1966_VALIDATION.csv",
        "needles": ["VAL1966_OVERALL", "PASS"],
    },
    "963_derivative_order": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_963_DERIVATIVE_ORDER_AUDIT.csv",
        "needles": ["DO963_0_962_relative_theorem", "DO963_6_verdict"],
    },
    "964_minimality": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv",
        "needles": ["MIN964_1_primitive_quotient", "MIN964_2_no_integrated_out_tower", "MIN964_5_verdict"],
    },
    "826_parent_action": {
        "path": MTS_RESIDUALS / "P8_Y5_R10_826_PARENT_ACTION_ANSATZ.csv",
        "needles": ["AA826_0_closed_parent_template", "AA826_1_memory_sector", "AA826_2_trace_projection_lock"],
    },
    "1965_doc": {
        "path": ROOT / "1965-Y5-R2FR-R2-fR-zero-proof-or-executable-R11-bound-row.md",
        "needles": ["ZP1965_3_minimality_route", "ZP1965_6_verdict", "SM1965_1_scalar_mass"],
    },
    "1340_interface": {
        "path": ROOT / "1340-Y5-R10-RAB-EH-core-selection-or-first-executable-R11-residual-interface.md",
        "needles": ["R11SCHEMA1340_1_R2FR", "ZERO1340_0_R2FR", "BOUND1340_0_R2FR"],
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
                "purpose": "1967 parent minimality or R2/fR coefficient origin",
                "required_needles": ";".join(needles),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "missing_needles": ";".join(missing),
            }
        )
        rows.append(row)
    return rows


def minimality_attempt_rows() -> list[dict[str, object]]:
    entries = [
        (
            "MIN1967_0_target",
            "prove parent minimality/no-extension strong enough to set c_R2=f_RR=0",
            "Q_MTS primitive + no natural curvature-square marker + no integrated-out scalar tower => c_R2=f_RR=0",
            "TARGET_EXACT",
            "This is the cleanest way to turn MTS into EH locally without fitting a coefficient.",
            "needs universal property of Q_MTS and invariant-algebra closure",
        ),
        (
            "MIN1967_1_primitive_quotient",
            "The MTS parent quotient is generated only by motion/time/space readout, the owned coframe, gauge fields, and constants.",
            "Allowed local exterior arguments: e_obs, R[e_obs], owned gauge curvature, topological/boundary terms, silent Xi constraints",
            "CANDIDATE_NOT_PARENT_SIGNED",
            "This is plausible after the owned-coframe route but not yet a theorem.",
            "derive Q_MTS universal property, not a design preference",
        ),
        (
            "MIN1967_2_invariant_algebra",
            "No independent scalar marker or invariant functor is available that can multiply R, generate f(R), or carry a scalaron.",
            "Algebra(A_local)^MTS = functions of EH density plus harmless Lambda/topological terms only",
            "NOT_DERIVED",
            "Current sources explicitly leave marker extensions legal.",
            "prove local invariant algebra triviality or list legal generators",
        ),
        (
            "MIN1967_3_derivative_order_constraint",
            "The parent action permits only first derivatives of the coframe or curvature-linear local terms in the compact exterior.",
            "L_ext depends on e and de through R linearly; no R^2, nabla R, or f_RR terms",
            "NOT_PARENT_SIGNED",
            "Regularity/stability intuition is not enough; R^2 can be stable as a scalar-tensor branch.",
            "derive derivative-order constraint from parent variational principle",
        ),
        (
            "MIN1967_4_no_integrated_out_tower",
            "Eliminating Xi_MTS, memory, projector, auxiliary, or bath variables cannot generate R2/fR/nonlocal terms in S_eff[e].",
            "delta S_eff/delta e has no scalar pole and no curvature-square counterterm from Schur complement/integration-out",
            "CENTRAL_BLOCKER_NOT_DERIVED",
            "826 includes candidate sectors; previous audits warn they can regenerate higher-curvature/Yukawa terms.",
            "need Hessian/mixing proof or explicit coefficient map",
        ),
        (
            "MIN1967_5_matter_blindness_to_scalar",
            "Ordinary matter and readout cannot couple to a hidden scalar/class label that re-enters as f(R) or scalar-tensor force.",
            "no A(phi)R, no B(phi)L_m, no local kinetic scalar with source charge in compact exterior",
            "CANDIDATE_ONLY",
            "Scalar/class descent clauses exist in prior work but remain unsigned.",
            "parent-sign scalar/class descent or retain scalar residuals",
        ),
        (
            "MIN1967_6_verdict",
            "Parent minimality/no-extension is not proven strongly enough to zero c_R2/f_RR.",
            "MIN1967_1 through MIN1967_5 remain candidate/unsigned/open",
            "ZERO_THEOREM_NOT_CLOSED",
            "The coefficient-origin route must be split into either a real parent coefficient calculation or closure-only zero assumption.",
            "move to coefficient-origin ledger",
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


def coefficient_origin_rows() -> list[dict[str, object]]:
    entries = [
        (
            "COEF1967_0_origin_fork",
            "c_R2/f_RR can be zero by parent minimality, calculable by integrating out Xi, or retained as a fitted/phenomenological closure parameter.",
            "ZERO_OR_CALCULABLE_OR_CLOSURE",
            "Only the first two are acceptable for derivable local GR; the third is modified-gravity phenomenology.",
            "choose route before scoring",
        ),
        (
            "COEF1967_1_tree_level_absence",
            "R2/fR is absent at tree level if S_parent local exterior is explicitly EH+Lambda plus silent Xi and no R^2/f(R) term.",
            "TREE_ABSENCE_CANDIDATE",
            "Helpful but insufficient because loops/effective reduction/integrated-out sectors can regenerate terms.",
            "must pair with no-generated-tower theorem",
        ),
        (
            "COEF1967_2_effective_generation",
            "If Xi couples to curvature or trace/source variables, integrating it out can generate c_R2, Yukawa scalar exchange, or nonlocal kernels.",
            "COEFFICIENT_ORIGIN_LIVE",
            "This is the most honest likely origin if minimality fails.",
            "need Xi-curvature/source mixing matrix and mass/gap",
        ),
        (
            "COEF1967_3_formula_template",
            "For a heavy scalar Xi with coupling beta_Xi Xi R and mass M_Xi, the effective local coefficient scales like beta_Xi^2/(2 M_Xi^2) up to normalization/sign conventions.",
            "TEMPLATE_ONLY_NOT_MTS_DERIVED",
            "This gives a route to c_R2 but not a value until beta_Xi and M_Xi are parent-derived.",
            "derive beta_Xi, M_Xi, normalization, sign",
        ),
        (
            "COEF1967_4_zero_by_symmetry",
            "A symmetry could set beta_Xi=0 or forbid the scalar curvature channel.",
            "SYMMETRY_ROUTE_OPEN",
            "This is more credible than merely saying higher derivatives are ugly.",
            "identify symmetry/selection rule in MTS variables",
        ),
        (
            "COEF1967_5_closure_flag",
            "Setting c_R2=f_RR=0 by declaration is closure-only unless backed by MIN1967 or a symmetry theorem.",
            "CLOSURE_ONLY_IF_UNDERIVED",
            "Prevents accidental EH claim from a chosen minimal ansatz.",
            "label as closure if used",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, clause, status, implication, required_fix in entries:
        row = base(row_id)
        row.update(
            {
                "clause": clause,
                "status": status,
                "implication": implication,
                "required_fix": required_fix,
            }
        )
        rows.append(row)
    return rows


def coefficient_schema_rows() -> list[dict[str, object]]:
    entries = [
        (
            "CS1967_0_minimality_zero",
            "zero_certificate",
            "parent_minimality_no_extension",
            "proof_id;source_path;allowed_invariants;forbidden_generators;no_integrated_out_tower;valid_for_claim",
            "MISSING_PARENT_PROOF",
            "REJECT_FOR_CLAIM",
        ),
        (
            "CS1967_1_integrated_out_scalar",
            "calculated_coefficient",
            "heavy_scalar_or_auxiliary_Xi",
            "field_id;coupling_beta;coupling_units;mass_or_gap;mass_units;normalization;sign;c_R2_value;c_R2_units;source_equation",
            "MISSING_BETA_AND_MASS",
            "REJECT_FOR_CLAIM",
        ),
        (
            "CS1967_2_symmetry_zero",
            "zero_certificate",
            "selection_rule",
            "symmetry_id;transformation;forbidden_operator;anomaly_or_breaking_status;source_path;valid_for_claim",
            "MISSING_SYMMETRY",
            "REJECT_FOR_CLAIM",
        ),
        (
            "CS1967_3_closure_parameter",
            "closure_parameter",
            "phenomenological_c_R2",
            "value;units;prior;fit_context;not_derivable_label;valid_for_claim=false",
            "CLOSURE_NOT_DERIVATION",
            "NONCLAIM_ONLY",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, row_type, route, required_fields, missing_now, runner_status in entries:
        row = base(row_id)
        row.update(
            {
                "row_type": row_type,
                "route": route,
                "required_fields": required_fields,
                "missing_now": missing_now,
                "runner_status": runner_status,
            }
        )
        rows.append(row)
    return rows


def runner_rows() -> list[dict[str, object]]:
    entries = [
        (
            "RUN1967_0_minimality_zero",
            "CS1967_0_minimality_zero",
            "REJECTED_MISSING_PARENT_PROOF",
            "minimality/no-extension/no-tower theorem missing",
        ),
        (
            "RUN1967_1_integrated_out_scalar",
            "CS1967_1_integrated_out_scalar",
            "REJECTED_MISSING_CALCULATED_COEFFICIENT",
            "beta_Xi, M_Xi, normalization, sign, and source equation missing",
        ),
        (
            "RUN1967_2_symmetry_zero",
            "CS1967_2_symmetry_zero",
            "REJECTED_MISSING_SYMMETRY",
            "no parent selection rule forbids scalar curvature channel",
        ),
        (
            "RUN1967_3_closure_parameter",
            "CS1967_3_closure_parameter",
            "ACCEPTED_NONCLAIM_CLOSURE_ONLY",
            "may be used for private sensitivity studies but not for derivable EH/GR claim",
        ),
        (
            "RUN1967_VERDICT",
            "all_routes",
            "R2FR_COEFFICIENT_ORIGIN_BLOCKED_NONCLAIM",
            "no derivable zero or coefficient exists yet",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, input_row, runner_status, reason in entries:
        row = base(row_id)
        row.update(
            {
                "input_row": input_row,
                "runner_status": runner_status,
                "reason": reason,
                "accepted_for_claim": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    entries = [
        ("CG1967_0_minimality_attempt", "Parent minimality theorem attempted.", "PASS_NONCLAIM", "attempt is useful but not proof"),
        ("CG1967_1_zero", "c_R2=f_RR=0 is parent-derived.", "FAIL_BLOCKED", "minimality/no-tower/symmetry not signed"),
        ("CG1967_2_coefficient", "c_R2/f_RR has a calculated MTS value.", "FAIL_BLOCKED", "mixing coefficient and mass/gap missing"),
        ("CG1967_3_closure", "c_R2=0 can be used as derivable EH premise.", "FAIL_BLOCKED", "closure-only if underived"),
        ("CG1967_4_EH", "EH second-order premise cleared.", "FAIL_BLOCKED", "R2/fR coefficient origin unresolved"),
        ("CG1967_5_Newton", "Newtonian mechanics derived.", "FAIL_BLOCKED", "EH, source-GM, PPN still open"),
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
            "DEC1967_0_verdict",
            "PARENT_MINIMALITY_NOT_PROVEN_COEFFICIENT_ORIGIN_BLOCKED",
            "The strongest route to c_R2=f_RR=0 needs a primitive quotient/no-extension/no-integrated-out-tower theorem; current evidence keeps each decisive clause unsigned.",
            "do not claim EH; either derive no-tower/minimality or calculate coefficient from Xi mixing",
        ),
        (
            "DEC1967_1_best_next",
            "NO_INTEGRATED_OUT_TOWER_IS_THE_NEXT_HARDEST_GATE",
            "Tree-level absence is not enough; hidden MTS sectors can regenerate R2/fR after reduction.",
            "try to prove no scalar pole/no curvature-square counterterm from Xi_MTS, memory, projector, and bath sectors",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, reason, next_action in entries:
        row = base(row_id)
        row.update({"decision": decision, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def next_rows() -> list[dict[str, object]]:
    row = base("NEXT1967_0_primary")
    row.update(
        {
            "priority": "selected",
            "target_doc": "1968-Y5-R2FR-no-integrated-out-curvature-tower-or-Xi-mixing-coefficient.md",
            "target_script": "scripts/Y5_R2FR_no_integrated_out_curvature_tower_or_Xi_mixing_coefficient_1968.py",
            "objective": "prove hidden MTS sectors cannot generate R2/fR after reduction, or derive the first Xi-mixing coefficient template for c_R2",
            "acceptance_output": "no-scalar-pole/no-curvature-square theorem attempt, or explicit beta_Xi/M_Xi coefficient-origin row",
            "nonclaim_rule": "no EH/R2fR pass unless the no-tower proof or coefficient row is parent-sourced",
        }
    )
    return [row]


def snapshot_rows() -> list[dict[str, object]]:
    row = base("SNAP1967_0_project_position")
    row.update(
        {
            "strongest_result": "The R2/fR problem is now localized to parent minimality/no-extension or effective coefficient generation from hidden MTS sectors.",
            "what_improved": "We no longer treat c_R2 as a mystery parameter; the exact acceptable origins are zero theorem, symmetry zero, or calculated Xi mixing.",
            "still_missing": "primitive quotient theorem, invariant algebra closure, no integrated-out tower, beta_Xi/M_Xi coefficient, full alpha(lambda) curve, GM/PPN completion",
            "claim_status": "no R2/fR zero, coefficient, EH, Newton, or local-GR claim",
        }
    )
    return [row]


OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1967_SOURCE_REGISTER.csv",
    "minimality": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1967_MINIMALITY_ATTEMPT.csv",
    "coefficient_origin": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1967_COEFFICIENT_ORIGIN_LEDGER.csv",
    "coefficient_schema": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1967_COEFFICIENT_SCHEMA.csv",
    "runner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1967_COEFFICIENT_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1967_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1967_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1967_NEXT_TARGET.csv",
    "snapshot": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1967_PROJECT_STATUS_SNAPSHOT.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "R2FR_COEFFICIENT_ORIGIN_1967_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1967_NO_TOWER_OR_XI_MIXING_QUEUE.csv",
}


def build_tables() -> dict[str, list[dict[str, object]]]:
    source_weight = [
        {
            **base("SW1967_0_nonclaim_weight"),
            "artifact": "1967 parent minimality or R2/fR coefficient origin",
            "weight": "COEFFICIENT_ORIGIN_GATE_NOT_CLOSED",
            "reason": "acceptable coefficient origins are now explicit but none are parent-signed",
        }
    ]
    queue = [
        {
            **base("AQ1967_0_no_tower"),
            "target": "no integrated-out curvature tower",
            "needed_inputs": "Xi field list; Hessian/mixing matrix; scalar pole absence; curvature counterterm absence; source/readout silence",
            "priority": "HIGHEST",
        },
        {
            **base("AQ1967_1_Xi_coefficient"),
            "target": "first calculated c_R2 coefficient row",
            "needed_inputs": "beta_Xi; beta units; M_Xi; normalization; sign; source equation; validity regime",
            "priority": "FALLBACK_HIGH",
        },
    ]
    return {
        "source_register": source_register(),
        "minimality": minimality_attempt_rows(),
        "coefficient_origin": coefficient_origin_rows(),
        "coefficient_schema": coefficient_schema_rows(),
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
    patterns = ("1967-", "*_1967_*", "*Y5*1967*", "*VAL1967*", "*P8*1967*")
    return sum(1 for path in FORMALIZATION.rglob("*") if any(Path(path.name).match(pattern) for pattern in patterns))


def validate(tables: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    sources_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in tables["source_register"])
    rows.append(validation_row("VAL1967_00_sources", "PASS" if sources_ok else "FAIL", "all source paths exist and needles found"))

    minimality_target_ok = any(row["row_id"] == "MIN1967_0_target" and row["status"] == "TARGET_EXACT" for row in tables["minimality"])
    minimality_fail_ok = any(row["row_id"] == "MIN1967_6_verdict" and row["status"] == "ZERO_THEOREM_NOT_CLOSED" for row in tables["minimality"])
    rows.append(validation_row("VAL1967_01_minimality_attempt", "PASS" if minimality_target_ok and minimality_fail_ok else "FAIL", "minimality attempted without claiming zero"))

    origin_ok = any(row["row_id"] == "COEF1967_2_effective_generation" and row["status"] == "COEFFICIENT_ORIGIN_LIVE" for row in tables["coefficient_origin"])
    template_ok = any(row["row_id"] == "COEF1967_3_formula_template" and row["status"] == "TEMPLATE_ONLY_NOT_MTS_DERIVED" for row in tables["coefficient_origin"])
    rows.append(validation_row("VAL1967_02_coefficient_origin", "PASS" if origin_ok and template_ok else "FAIL", "effective coefficient origin route retained"))

    schema_ok = any(row["row_id"] == "CS1967_1_integrated_out_scalar" and row["runner_status"] == "REJECT_FOR_CLAIM" for row in tables["coefficient_schema"])
    rows.append(validation_row("VAL1967_03_schema", "PASS" if schema_ok else "FAIL", "coefficient schema rejects missing beta/mass"))

    runner_ok = any(row["row_id"] == "RUN1967_VERDICT" and row["runner_status"] == "R2FR_COEFFICIENT_ORIGIN_BLOCKED_NONCLAIM" for row in tables["runner"])
    rows.append(validation_row("VAL1967_04_runner", "PASS" if runner_ok else "FAIL", "runner blocks coefficient origin claim"))

    gate_ok = all(row["status"] != "PASS_CLAIM" for row in tables["claim_gate"]) and any(row["row_id"] == "CG1967_4_EH" and row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    rows.append(validation_row("VAL1967_05_claim_gates", "PASS" if gate_ok else "FAIL", "EH/Newton claims remain blocked"))

    decision_ok = any(row["decision"] == "NO_INTEGRATED_OUT_TOWER_IS_THE_NEXT_HARDEST_GATE" for row in tables["decision"])
    rows.append(validation_row("VAL1967_06_decision", "PASS" if decision_ok else "FAIL", "no-tower gate selected"))

    next_ok = tables["next"][0]["target_doc"] == "1968-Y5-R2FR-no-integrated-out-curvature-tower-or-Xi-mixing-coefficient.md"
    rows.append(validation_row("VAL1967_07_next_target", "PASS" if next_ok else "FAIL", "1968 target selected"))

    flags_ok = all(not bool(row.get("valid_for_claim")) and not bool(row.get("public_claim")) for table in tables.values() for row in table)
    rows.append(validation_row("VAL1967_08_claim_flags_safe", "PASS" if flags_ok else "FAIL", "claim flags all false"))

    csv_ok = all(bool(read_csv(path)) for path in OUTPUTS.values())
    rows.append(validation_row("VAL1967_09_csv_parse", "PASS" if csv_ok else "FAIL", "all generated CSVs parse with rows"))

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    rows.append(validation_row("VAL1967_10_pycache_absent", "PASS" if not pycache.exists() else "FAIL", "scripts __pycache__ absent"))

    count = formalization_hits()
    rows.append(validation_row("VAL1967_11_formalization_untouched", "PASS" if count == 0 else "FAIL", f"formalization_1967_artifact_count={count}"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(validation_row("VAL1967_OVERALL", overall, "1967 parent minimality or R2/fR coefficient origin"))
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
        ("Minimality Attempt", tables["minimality"]),
        ("Coefficient Origin Ledger", tables["coefficient_origin"]),
        ("Coefficient Schema", tables["coefficient_schema"]),
        ("Runner Dryrun", tables["runner"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Project Status Snapshot", tables["snapshot"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1967 Y5 R2FR: Parent Minimality Or R2/fR Coefficient Origin",
        "",
        "Private checkpoint. This tries the parent-minimality route for killing `R2/fR`, then forces a coefficient-origin fork if the zero theorem cannot be signed.",
        "",
        "Verdict: parent minimality/no-extension is not yet strong enough to prove `c_R2=f_RR=0`. The acceptable origins are now explicit: a signed zero theorem, a signed symmetry zero, or a calculated coefficient from hidden-sector mixing. A closure value is not a derivation.",
        "",
        "No R2/fR, EH, Newton, or local-GR claim follows from this checkpoint.",
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
    print(f"VAL1967_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
