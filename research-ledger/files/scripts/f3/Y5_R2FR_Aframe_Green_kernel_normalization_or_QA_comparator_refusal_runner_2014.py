from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
DOC = ROOT / "2014-Y5-R2FR-Aframe-Green-kernel-normalization-or-QA-comparator-refusal-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, object]:
    return {
        "branch_id": BRANCH_ID,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        "generated_utc": stamp(),
    }


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_rows_parse(path: Path) -> bool:
    try:
        read_csv(path)
    except csv.Error:
        return False
    return True


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2014_00_2013_handoff",
            "2013-Y5-R2FR-Aframe-finite-QA-bound-source-acquisition-or-boundary-neutrality-proof.md",
            ["NEXT2013_0_2014", "ACQ2013_0_QA_parent", "VAL2013_OVERALL"],
            "2013 selected A-frame Green-kernel normalization or comparator refusal.",
        ),
        (
            "SRC2014_01_1035_kernel_analogy",
            "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
            ["KXF1035_4_total", "DEC1035_0_kernel_status", "V1035_SUMMARY"],
            "existing R10 Green-kernel/profile normalization contract to adapt for Q_A.",
        ),
        (
            "SRC2014_02_1034_R10_curve",
            "1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md",
            ["R10P1034_0_alpha_bound_curve", "CGATE1034_1_external_curve", "DEC1034_2_projection_status"],
            "R10 external curve/projection pack remains nonclaim and theory-side prediction missing.",
        ),
        (
            "SRC2014_03_2012_finite_QA",
            "2012-Y5-R2FR-Aframe-current-nohair-source-neutrality-theorem-or-finite-QA-row.md",
            ["FQA2012_2_CA", "FQA2012_5_alpha", "VAL2012_OVERALL"],
            "finite Q_A rows define C_A/lambda_A/alpha_A needs.",
        ),
        (
            "SRC2014_04_PPN_QR_schema",
            "1240-Y5-R10-PPN-QR-residual-bound-schema-or-zero-charge-theorem.md",
            ["QMAP1240_3_gamma_projection", "COMP1240_0_gamma_Cassini", "VAL1240_12_overall"],
            "finite-charge to PPN comparator analogy and Cassini source anchor.",
        ),
        (
            "SRC2014_05_clock_WEP",
            "948-Y5-R10-clock-WEP-product-bound-runner-or-constant-superselection-no-marker-theorem.md",
            ["CLK948_1_CAS646_1_YbE3E2", "WEP948_1_WAS651_1_surface_binding", "CGATE948_0_constant_superselection"],
            "clock/WEP comparator ledgers exist but MTS source prediction is missing.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, relative_path, needles, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in needles if needle not in text]
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "needed_for": "2014 A-frame Green-kernel normalization or Q_A comparator refusal runner",
                "needles": ";".join(needles),
                "exists": str(exists),
                "anchor_found": str(exists and not missing),
                "missing_needles": ";".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "note": note,
            }
        )
        rows.append(row)
    return rows


def green_kernel_rows() -> list[dict[str, object]]:
    specs = [
        (
            "AGK2014_0_parent_operator",
            "L_A^{a mu}{}_{b nu} delta A^b_nu = kappa_A J_A^{a mu}",
            "A parent quadratic action must define the A-frame response operator and source current.",
            "FORMAL_OPERATOR_TARGET",
            "missing S_A, Z_A, M_A/lambda_A, gauge constraints, and source current units",
            "false",
        ),
        (
            "AGK2014_1_static_projected_mode",
            "(nabla^2 - lambda_A^-2) chi_A = -S_A Q_A delta^3(x)",
            "If a single static scalarized A projection dominates, the Yukawa Green function is fixed up to source normalization.",
            "CONDITIONAL_KERNEL_FORM",
            "projection chi_A=P_A deltaA and source strength S_A are not parent-derived",
            "false",
        ),
        (
            "AGK2014_2_solution_profile",
            "chi_A(r)=S_A Q_A exp(-r/lambda_A)/(4 pi r)",
            "This gives the profile shape only after lambda_A and normalization are known.",
            "SYMBOLIC_PROFILE_ONLY",
            "lambda_A, S_A, and finite-source corrections are missing",
            "false",
        ),
        (
            "AGK2014_3_metric_projection",
            "h_A00(r)=P_00^A chi_A(r)",
            "A-frame hair becomes observable only through a metric/readout projection.",
            "MISSING_PROJECTION",
            "P_00^A and no-spurion matter/readout rules are missing",
            "false",
        ),
        (
            "AGK2014_4_C_A_relation",
            "C_A = N_A kappa_A Q_A/(4 pi Z_A) times projection/support factors",
            "This is the normalization bridge from charge hair to a dimensionless local metric amplitude.",
            "CONDITIONAL_FACTORISATION",
            "N_A, kappa_A, Q_A, Z_A, and support factors are all unsourced",
            "false",
        ),
        (
            "AGK2014_5_alpha_matching",
            "alpha_A(lambda_A) from matching h_A00 to 2 G M alpha_A exp(-r/lambda_A)/(c^2 r)",
            "R10 can only use A-hair after the weak-field Yukawa convention and measured-G normalization are fixed.",
            "MISSING_ALPHA_MATCH",
            "measured source mass, P_00^A, C_A, lambda_A, and promoted alpha_bound curve are missing",
            "false",
        ),
        (
            "AGK2014_6_massless_or_long_range",
            "lambda_A -> infinity",
            "A massless branch is not R10-only; it is immediately PPN/orbital/clock sensitive.",
            "LONG_RANGE_BRANCH_BLOCKED",
            "needs PPN/orbital projection and is not rescued by short-range anchors",
            "false",
        ),
        (
            "AGK2014_7_pure_gauge_branch",
            "L_A has only gauge kernel and no physical pole",
            "If true and matter/readout are invariant, finite Q_A may be quotient-trivial.",
            "POSSIBLE_ZERO_ROUTE_NOT_SIGNED",
            "requires first-class gauge/no-spurion proof, not current source rows",
            "false",
        ),
        (
            "AGK2014_8_verdict",
            "A-frame Green-kernel normalization",
            "Only conditional symbolic formulas are available; no numeric or claim-grade kernel normalization is derived.",
            "GREEN_KERNEL_NOT_NUMERIC",
            "derive parent quadratic action/residue/range/source charge next or keep refusing comparator scores",
            "false",
        ),
    ]
    rows: list[dict[str, object]] = []
    for kernel_id, object_text, meaning, status, missing_before_claim, parent_signed in specs:
        row = base_row()
        row.update(
            {
                "kernel_id": kernel_id,
                "object": object_text,
                "meaning": meaning,
                "status": status,
                "missing_before_claim": missing_before_claim,
                "parent_signed": parent_signed,
            }
        )
        rows.append(row)
    return rows


def factorization_rows() -> list[dict[str, object]]:
    specs = [
        ("FAC2014_0_QA", "Q_A", "finite A exterior/source charge", "MISSING_PARENT_BOUNDARY_VARIATION", "A-charge units"),
        ("FAC2014_1_kappaA", "kappa_A", "A-source coupling in E_A=kappa_A J_A", "MISSING_PARENT_COUPLING", "model-dependent"),
        ("FAC2014_2_ZA", "Z_A", "quadratic residue/kinetic normalization of A mode", "MISSING_PARENT_RESIDUE", "model-dependent"),
        ("FAC2014_3_lambdaA", "lambda_A", "range from A pole or screening map", "MISSING_MASS_OR_SCREENING_RULE", "m"),
        ("FAC2014_4_P00", "P_00^A", "projection from A mode to h_00", "MISSING_METRIC_PROJECTION", "dimensionless"),
        ("FAC2014_5_profile", "f_A(r)", "normalized finite-source radial/profile shape", "MISSING_PROFILE_SOLUTION", "dimensionless"),
        ("FAC2014_6_NA", "N_A", "Newton/measured-G normalization converting A potential to alpha convention", "MISSING_NEWTON_NORMALIZATION", "dimensionless"),
        ("FAC2014_7_CA", "C_A", "N_A kappa_A Q_A P_00^A support/(4 pi Z_A)", "CONDITIONAL_SYMBOLIC_ONLY", "dimensionless_or_declared"),
        ("FAC2014_8_alphaA", "alpha_A(lambda_A)", "Yukawa-equivalent A strength after matching h_A00", "MISSING_JOIN_INPUTS", "dimensionless"),
        ("FAC2014_9_total", "R_A(Q_A)", "total finite-Q_A local response vector", "NOT_SCORE_READY", "mixed"),
    ]
    rows: list[dict[str, object]] = []
    for factor_id, symbol, definition, status, units in specs:
        row = base_row()
        row.update(
            {
                "factor_id": factor_id,
                "symbol": symbol,
                "definition": definition,
                "status": status,
                "numeric_value": "MISSING",
                "units": units,
                "score_ready": "false",
            }
        )
        rows.append(row)
    return rows


def comparator_refusal_rows() -> list[dict[str, object]]:
    specs = [
        (
            "CMP2014_0_R10",
            "alpha_A(lambda_A) vs alpha_bound(lambda)",
            "REFUSE",
            "Q_A,C_A,lambda_A,alpha_A missing; R10 curve review-candidate/nonclaim; official/promotion gate missing",
        ),
        (
            "CMP2014_1_PPN",
            "gamma_minus_1_A vs Cassini/PPN comparator",
            "REFUSE",
            "A-to-gamma projection missing; C_A/Q_A missing; pass policy missing",
        ),
        (
            "CMP2014_2_clock",
            "delta_clock_A vs clock bounds",
            "REFUSE",
            "A clock coupling and source profile missing",
        ),
        (
            "CMP2014_3_WEP",
            "eta_A or beta_source_A vs WEP caps",
            "REFUSE",
            "source-normalized A matter coupling missing; no-spurion still unsigned",
        ),
        (
            "CMP2014_4_orbital",
            "delta_orbit_A vs orbital/light-time bounds",
            "REFUSE",
            "A profile along trajectory and primary orbital bound ledger missing",
        ),
        (
            "CMP2014_5_local_GR",
            "finite Q_A branch compatible with local GR/Newton",
            "REFUSE",
            "A kernel not normalized, Q_A not zero/bounded, q_loc/R11/matter-silence still open",
        ),
    ]
    rows: list[dict[str, object]] = []
    for refusal_id, comparator, runner_status, refusal_reasons in specs:
        row = base_row()
        row.update(
            {
                "refusal_id": refusal_id,
                "comparator": comparator,
                "runner_status": runner_status,
                "refusal_reasons": refusal_reasons,
                "score_ready": "false",
                "accepted_for_claim": "false",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("CG2014_0_kernel_form", "A Green-kernel form written", "PASS_NONCLAIM", "conditional symbolic formulas exist"),
        ("CG2014_1_parent_quadratic", "parent quadratic A action supplies Z_A,M_A,kappa_A", "FAIL_BLOCKED", "no parent action/residue/range/source coupling"),
        ("CG2014_2_CA_lambda_alpha", "C_A, lambda_A, alpha_A are numeric and sourced", "FAIL_BLOCKED", "all theory-side factors missing"),
        ("CG2014_3_R10_score", "R10 comparator can score finite Q_A", "FAIL_BLOCKED", "alpha_A missing and external curve nonclaim"),
        ("CG2014_4_PPN_clock_WEP_orbit", "PPN/clock/WEP/orbital comparators can score finite Q_A", "FAIL_BLOCKED", "projection/source coefficients missing"),
        ("CG2014_5_local_GR_Newton", "local GR/Newton derived", "FAIL_BLOCKED", "Q_A, q_loc, R11, matter silence, and A ownership remain open"),
    ]
    rows: list[dict[str, object]] = []
    for gate_id, gate, status, reason in specs:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "gate": gate,
                "status": status,
                "reason": reason,
                "passed_for_claim": "false",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DEC2014_0_result",
            "A_GREEN_KERNEL_FORM_SYMBOLIC_NOT_NUMERIC",
            "A Yukawa/Green-kernel shape can be written conditionally, but Z_A, M_A/lambda_A, kappa_A, Q_A, projection, and source support are missing.",
            "do not score; derive parent quadratic A action/residue/range/source charge next",
        ),
        (
            "DEC2014_1_external_bounds_status",
            "COMPARATORS_REFUSE_CORRECTLY",
            "R10/PPN/clock/WEP sources are useful ledgers, but external bounds alone are not an MTS prediction.",
            "keep refusal runner until theory-side rows are sourced",
        ),
        (
            "DEC2014_2_next_attack",
            "PARENT_QUADRATIC_A_ROW_IS_THE BOTTLENECK",
            "The first real leap is a parent action clause for the finite A mode: residue, range, source coupling, gauge constraints, and projection.",
            "target Z_A, lambda_A, kappa_A, J_A, and P_00^A explicitly",
        ),
    ]
    rows: list[dict[str, object]] = []
    for decision_id, verdict, rationale, next_action in specs:
        row = base_row()
        row.update(
            {
                "decision_id": decision_id,
                "verdict": verdict,
                "rationale": rationale,
                "next_action": next_action,
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2014_0_2015",
            "selected": "true",
            "next_doc": "2015-Y5-R2FR-Aframe-parent-quadratic-action-ZA-lambdaA-source-charge-or-finite-prior-envelope.md",
            "next_script": "scripts/Y5_R2FR_Aframe_parent_quadratic_action_ZA_lambdaA_source_charge_or_finite_prior_envelope_2015.py",
            "objective": "derive or reject a parent quadratic A-frame action row that supplies Z_A, lambda_A/M_A, kappa_A, J_A/source charge, gauge constraints, and P_00 projection; if missing, build a finite prior envelope for Q_A/C_A/lambda_A without scoring claims",
            "include": "S_A quadratic operator; residue sign; range relation; source current units; metric projection P_00; no-extra-mode constraints; finite prior envelope rows",
            "exclude": "invented numeric C_A/lambda_A; claim from external bounds alone; anchor-only interpolation; local-GR claim; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update(
            {
                "copy_id": f"COPY2014_{idx}",
                "copy_path": str(path),
                "exists": str(path.exists()),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    kernel_rows: list[dict[str, object]],
    factor_rows: list[dict[str, object]],
    refusal_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    checks = [
        ("VAL2014_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"),
        ("VAL2014_01_kernel_conditional", any(row["status"] == "CONDITIONAL_KERNEL_FORM" for row in kernel_rows), "conditional A Green-kernel formula written"),
        ("VAL2014_02_kernel_not_numeric", any(row["status"] == "GREEN_KERNEL_NOT_NUMERIC" for row in kernel_rows) and all(row["parent_signed"] == "false" for row in kernel_rows), "kernel normalization not falsely promoted"),
        ("VAL2014_03_factor_slots", {"FAC2014_0_QA", "FAC2014_2_ZA", "FAC2014_3_lambdaA", "FAC2014_7_CA", "FAC2014_8_alphaA"}.issubset({row["factor_id"] for row in factor_rows}), "factor rows cover Q_A/Z_A/lambda_A/C_A/alpha_A"),
        ("VAL2014_04_factor_rows_missing", all(row["numeric_value"] == "MISSING" and row["score_ready"] == "false" for row in factor_rows), "all factor rows remain missing/nonclaim"),
        ("VAL2014_05_refusals_active", all(row["runner_status"] == "REFUSE" and row["accepted_for_claim"] == "false" for row in refusal_rows), "comparator refusal runner rejects all arenas"),
        ("VAL2014_06_claim_gates_blocked", all(row["passed_for_claim"] == "false" for row in claim_gates), "all claim gates remain blocked"),
        ("VAL2014_07_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2014_08_branch_copies", all(path.exists() for path in branch_paths), "branch-copy CSVs exist"),
        ("VAL2014_09_no_formalization_edits", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains 0 for this run"),
        ("VAL2014_10_output_scope", all(ROOT in [path, *path.parents] for path in [*output_paths, *branch_paths, DOC]), "all outputs are under post-checkpoint-work"),
    ]
    rows: list[dict[str, object]] = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    overall = all(row["status"] == "PASS" for row in rows)
    row = base_row()
    row.update(
        {
            "check_id": "VAL2014_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2014 A-frame Green-kernel normalization or Q_A comparator refusal runner",
        }
    )
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    kernel_rows: list[dict[str, object]],
    factor_rows: list[dict[str, object]],
    refusal_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 2014 Y5 R2FR: A-Frame Green-Kernel Normalization Or Q_A Comparator Refusal Runner

Private checkpoint. This tries to turn finite `Q_A` into an actual A-frame prediction: `C_A`, `lambda_A`, profile `f_A(r)`, and `alpha_A(lambda)`.

## Current Verdict

The Green-kernel shape can be written only conditionally. If a parent quadratic A action supplies an operator `L_A`, residue `Z_A`, range `lambda_A`, source coupling `kappa_A`, and current `J_A`, then a static projected Yukawa form follows. But those parent inputs are not present.

So `Q_A -> C_A -> alpha_A(lambda_A)` is not score-ready. The comparator runner correctly refuses R10, PPN, clock, WEP, orbital, and local-GR scoring. The external bound ledgers are useful, especially the R10 review candidate and PPN/clock/WEP comparator rows, but they are not an MTS prediction and cannot replace the missing A-kernel normalization.

No local-GR/Newton/WEP/R10 claim is promoted.

## Source Register
{md_table(sources, ["source_id", "source_path", "status", "needles", "note"])}

## A-Frame Green-Kernel Attempt
{md_table(kernel_rows, ["kernel_id", "object", "status", "missing_before_claim", "parent_signed"])}

## Q_A To Alpha Factorization
{md_table(factor_rows, ["factor_id", "symbol", "definition", "status", "numeric_value", "units", "score_ready"])}

## Comparator Refusal Runner
{md_table(refusal_rows, ["refusal_id", "comparator", "runner_status", "refusal_reasons", "score_ready", "accepted_for_claim"])}

## Claim Gates
{md_table(claim_gates, ["gate_id", "gate", "status", "reason", "passed_for_claim"])}

## Decision Ledger
{md_table(decisions, ["decision_id", "verdict", "rationale", "next_action"])}

## Branch Copies
{md_table(branch_copies, ["copy_id", "copy_path", "exists", "note"])}

## Next Target
{md_table(next_target, ["target_id", "next_doc", "objective", "include", "exclude"])}

## Validation
{md_table(validation, ["check_id", "status", "detail"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    kernel_rows = green_kernel_rows()
    factor_rows = factorization_rows()
    refusal_rows = comparator_refusal_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2014_SOURCE_REGISTER.csv",
        "kernel": OUT / "P8_Y5_PARENT_QLOC_2014_AFRAME_GREEN_KERNEL_ATTEMPT.csv",
        "factors": OUT / "P8_Y5_PARENT_QLOC_2014_QA_TO_ALPHA_FACTORIZATION.csv",
        "refusals": OUT / "P8_Y5_PARENT_QLOC_2014_COMPARATOR_REFUSAL_RUNNER.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2014_CLAIM_GATE.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2014_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2014_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["kernel"], kernel_rows)
    write_csv(output_map["factors"], factor_rows)
    write_csv(output_map["refusals"], refusal_rows)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "AFRAME_GREEN_KERNEL_2014_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2014_QA_ALPHA_FACTOR_STATUS_NONCLAIM.csv",
        QUEUE / "JR2014_AFRAME_QA_COMPARATOR_REFUSAL_QUEUE.csv",
    ]
    for path in branch_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["kernel"], branch_paths[0])
    shutil.copyfile(output_map["factors"], branch_paths[1])
    shutil.copyfile(output_map["refusals"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "A-frame Green-kernel attempt nonclaim copy",
            "Q_A to alpha factorization status nonclaim copy",
            "A-frame comparator refusal queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2014_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, kernel_rows, factor_rows, refusal_rows, claim_gates, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2014_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, kernel_rows, factor_rows, refusal_rows, claim_gates, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2014_OVERALL"][0]["status"]
    print(f"VAL2014_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
