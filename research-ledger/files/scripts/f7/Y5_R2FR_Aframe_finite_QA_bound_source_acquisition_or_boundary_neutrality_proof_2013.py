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
DOC = ROOT / "2013-Y5-R2FR-Aframe-finite-QA-bound-source-acquisition-or-boundary-neutrality-proof.md"
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
            "SRC2013_00_2012_handoff",
            "2012-Y5-R2FR-Aframe-current-nohair-source-neutrality-theorem-or-finite-QA-row.md",
            ["NEXT2012_0_2013", "NHA2012_7_verdict", "VAL2012_OVERALL"],
            "2012 selected finite Q_A bound acquisition or boundary neutrality proof.",
        ),
        (
            "SRC2013_01_source_neutrality",
            "06-reciprocal-charge-source-neutrality.md",
            ["reciprocal_charge_neutrality_conditional_not_parent_derived", "Pi_R = 0 -> Q_R = 0", "Q_R neutrality is the missing source theorem"],
            "analogue for boundary/source neutrality and conjugate charge.",
        ),
        (
            "SRC2013_02_current_obstruction",
            "11-cell-current-origin-attempt.md",
            ["cell_current_origin_no_charge_obstruction", "Q_R = constant.", "ordinary cell-current conservation does not close"],
            "current conservation does not kill exterior charge hair.",
        ),
        (
            "SRC2013_03_R10_curve_pack",
            "1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md",
            ["R10B1034_3_vector_review_candidate_summary", "CGATE1034_1_external_curve", "DEC1034_2_projection_status"],
            "R10 external bound side has nonclaim review candidate and missing projection pack.",
        ),
        (
            "SRC2013_04_R10_anchor_pack",
            "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
            ["R10_ANCHOR_EOTWASH_2020_ALPHA1_38P6UM", "B563_1_no_numeric_MTS_alpha", "V563_10_no_overclaim"],
            "source-backed Eot-Wash anchors exist but are anchor-only/nonclaim.",
        ),
        (
            "SRC2013_05_PPN_QR_schema",
            "1240-Y5-R10-PPN-QR-residual-bound-schema-or-zero-charge-theorem.md",
            ["QB1240_2_gamma_comparator", "COMP1240_0_gamma_Cassini", "VAL1240_12_overall"],
            "finite charge to PPN gamma schema and Cassini comparator anchor.",
        ),
        (
            "SRC2013_06_clock_WEP",
            "948-Y5-R10-clock-WEP-product-bound-runner-or-constant-superselection-no-marker-theorem.md",
            ["CLK948_1_CAS646_1_YbE3E2", "WEP948_1_WAS651_1_surface_binding", "DEC948_1_clock_runner"],
            "clock/WEP source-side bound runners exist, but MTS product/source prediction is missing.",
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
                "needed_for": "2013 A-frame finite Q_A bound acquisition or boundary neutrality proof",
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


def boundary_neutrality_rows() -> list[dict[str, object]]:
    specs = [
        (
            "BNA2013_0_target",
            "Pi_A^{n a}=0 -> Q_A^a=0",
            "Prove source/boundary neutrality for the A-frame conjugate momentum, not just current conservation.",
            "TARGET_EXACT",
            "needs parent source action and boundary variation",
            "false",
        ),
        (
            "BNA2013_1_variation_formula",
            "delta S_boundary = integral_{partial Sigma} Pi_A^{n a} delta A_a + ...",
            "This is the exact object needed to decide whether source matter carries A-charge.",
            "FORMAL_FORMULA_WRITTEN",
            "Pi_A is not calculated from a parent boundary/source action",
            "false",
        ),
        (
            "BNA2013_2_free_boundary",
            "free A variation at compact source boundary",
            "If the source action has no A-representative dependence, stationarity forces Pi_A^n=0.",
            "CONDITIONAL_ZERO_ROUTE",
            "requires no-spurion matter/source action, not currently signed",
            "false",
        ),
        (
            "BNA2013_3_fixed_boundary_risk",
            "fixed or source-coupled A boundary",
            "If the source fixes A or couples to A directly, nonzero Pi_A and exterior Q_A hair are legal.",
            "LEGAL_COUNTERMODEL",
            "must be excluded by parent matter/source grammar",
            "false",
        ),
        (
            "BNA2013_4_source_neutrality_analogy",
            "Pi_A^n=0 analogous to Pi_R=0",
            "The reciprocal branch already showed that zero charge needs a source-neutrality theorem.",
            "ANALOGY_SUPPORTS_ROUTE_NOT_PROOF",
            "analogy does not sign A-specific source neutrality",
            "false",
        ),
        (
            "BNA2013_5_matter_no_spurion",
            "S_source[e,omega,Psi] no direct X,A,Phi_MTS,q_loc markers",
            "Would make A-boundary charge vanish or become pure gauge in ordinary matter.",
            "MISSING_PARENT_SIGNATURE",
            "no source-side A no-spurion audit is signed",
            "false",
        ),
        (
            "BNA2013_6_verdict",
            "boundary/source neutrality proof",
            "The proof does not close from current sources; finite Q_A remains live.",
            "BOUNDARY_NEUTRALITY_NOT_DERIVED",
            "move to finite-bound acquisition while keeping Pi_A^n=0 as the clean theorem target",
            "false",
        ),
    ]
    rows: list[dict[str, object]] = []
    for proof_id, clause, result, status, missing_before_claim, parent_signed in specs:
        row = base_row()
        row.update(
            {
                "proof_id": proof_id,
                "clause": clause,
                "result": result,
                "status": status,
                "missing_before_claim": missing_before_claim,
                "parent_signed": parent_signed,
            }
        )
        rows.append(row)
    return rows


def finite_bound_acquisition_rows() -> list[dict[str, object]]:
    specs = [
        (
            "ACQ2013_0_QA_parent",
            "Q_A",
            "finite A-current charge",
            "MTS side",
            "MISSING_PARENT_BOUNDARY_VARIATION",
            "MISSING",
            "A-charge units",
            "derive Pi_A^n or source Q_A from parent action",
        ),
        (
            "ACQ2013_1_CA",
            "C_A",
            "A-frame metric response amplitude",
            "MTS side",
            "MISSING_KAPPA_A_QA_NORMALIZATION",
            "MISSING",
            "dimensionless or declared",
            "derive C_A=N_A kappa_A Q_A with fixed normalization",
        ),
        (
            "ACQ2013_2_lambda_A",
            "lambda_A",
            "range/screening length",
            "MTS side",
            "MISSING_GREEN_KERNEL_OR_SCREENING_MAP",
            "MISSING",
            "m",
            "derive A Green kernel pole or support scale",
        ),
        (
            "ACQ2013_3_R10_external_curve",
            "alpha_bound(lambda)",
            "short-range external comparator curve",
            "external bound side",
            "REVIEW_CANDIDATE_PRESENT_NONCLAIM",
            "source-intake/local_bounds/R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
            "dimensionless over m",
            "official supplement or QA promotion still required before claim scoring",
        ),
        (
            "ACQ2013_4_R10_anchor",
            "alpha=1 at 38.6 micrometers",
            "source-backed threshold anchor",
            "external bound side",
            "ANCHOR_ONLY_NONCLAIM",
            "1034/563 Eot-Wash 2020 rows",
            "dimensionless at m",
            "usable for smoke/provenance only, not interpolation",
        ),
        (
            "ACQ2013_5_alpha_A",
            "alpha_A(lambda_A)",
            "A-hair Yukawa-equivalent prediction",
            "join row",
            "MISSING_A_MATCHING_AND_PARENT_COEFFICIENTS",
            "MISSING",
            "dimensionless",
            "requires Q_A,C_A,lambda_A,profile and source-normalized matching",
        ),
        (
            "ACQ2013_6_PPN_gamma",
            "gamma_minus_1_A",
            "finite A-charge PPN gamma comparator path",
            "external comparator side",
            "COMPARATOR_AVAILABLE_PREDICTION_MISSING",
            "1240 Cassini gamma comparator ledger",
            "dimensionless",
            "requires A-to-PPN projection and pass policy before scoring",
        ),
        (
            "ACQ2013_7_clock",
            "delta_clock_A",
            "finite A clock/redshift response",
            "external comparator side",
            "CLOCK_BOUNDS_AVAILABLE_PREDICTION_MISSING",
            "948 clock product runner rows",
            "dimensionless/frequency ratio",
            "requires A clock coupling/projection coefficient",
        ),
        (
            "ACQ2013_8_WEP",
            "eta_A or beta_source_A",
            "finite A source/composition response",
            "external comparator side",
            "WEP_CAPS_AVAILABLE_SOURCE_PREDICTION_MISSING",
            "948 WEP source-product runner rows",
            "dimensionless",
            "requires source-normalized A matter coupling and no-spurion decision",
        ),
        (
            "ACQ2013_9_orbital",
            "delta_orbit_A",
            "finite A orbital/light-time response",
            "external comparator side",
            "MISSING_ORBITAL_BOUND_LEDGER_AND_PROJECTION",
            "MISSING",
            "observable-specific",
            "requires trajectory kernel and primary bound source",
        ),
    ]
    rows: list[dict[str, object]] = []
    for acq_id, symbol, meaning, side, status, local_or_source, units, next_action in specs:
        row = base_row()
        row.update(
            {
                "acq_id": acq_id,
                "symbol": symbol,
                "meaning": meaning,
                "side": side,
                "status": status,
                "local_or_source": local_or_source,
                "numeric_value": "MISSING" if "MISSING" in status else "NONCLAIM_SOURCE_AVAILABLE",
                "units": units,
                "next_action": next_action,
                "score_ready": "false",
            }
        )
        rows.append(row)
    return rows


def comparator_refusal_rows() -> list[dict[str, object]]:
    specs = [
        (
            "REF2013_0_R10",
            "abs(alpha_A(lambda_A)) <= alpha_bound(lambda_A)",
            "REFUSE",
            "alpha_A missing; lambda_A missing; external curve review candidate nonclaim; official/full promoted curve missing",
        ),
        (
            "REF2013_1_PPN",
            "abs(gamma_minus_1_A) <= gamma comparator policy",
            "REFUSE",
            "A-to-PPN projection missing; C_A/Q_A missing; statistical policy missing",
        ),
        (
            "REF2013_2_clock",
            "abs(delta_clock_A) <= clock product bounds",
            "REFUSE",
            "A clock coupling/projection missing; source prediction missing",
        ),
        (
            "REF2013_3_WEP",
            "A composition/source response <= WEP cap",
            "REFUSE",
            "source-normalized A matter coupling missing; no-spurion status unsigned",
        ),
        (
            "REF2013_4_orbital",
            "orbital/light-time residual <= bound",
            "REFUSE",
            "trajectory kernel and primary bound ledger missing",
        ),
        (
            "REF2013_5_local_GR",
            "finite Q_A branch compatible with local GR",
            "REFUSE",
            "Q_A not zero, not bounded, and not mapped through all local arenas",
        ),
    ]
    rows: list[dict[str, object]] = []
    for refusal_id, attempted_score, runner_status, refusal_reasons in specs:
        row = base_row()
        row.update(
            {
                "refusal_id": refusal_id,
                "attempted_score": attempted_score,
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
        ("CG2013_0_boundary_attempt", "Pi_A boundary/source neutrality proof attempted", "PASS_NONCLAIM", "proof clauses written but unsigned"),
        ("CG2013_1_PiA_zero", "Pi_A^n=0 parent-derived", "FAIL_BLOCKED", "parent source/boundary action and no-spurion signature missing"),
        ("CG2013_2_finite_QA_source_pack", "finite Q_A acquisition pack staged", "PASS_NONCLAIM", "source/comparator rows exist but missing theory coefficients"),
        ("CG2013_3_R10_score", "finite Q_A R10 score-ready", "FAIL_BLOCKED", "alpha_A and promoted full curve missing"),
        ("CG2013_4_PPN_clock_WEP_score", "finite Q_A PPN/clock/WEP score-ready", "FAIL_BLOCKED", "projection coefficients and source predictions missing"),
        ("CG2013_5_orbital_score", "finite Q_A orbital score-ready", "FAIL_BLOCKED", "orbital projection and bound ledger missing"),
        ("CG2013_6_local_GR_Newton", "local GR/Newton derived", "FAIL_BLOCKED", "Q_A, q_loc, R11, matter silence, and A ownership remain open"),
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
            "DEC2013_0_result",
            "BOUNDARY_NEUTRALITY_NOT_DERIVED_FINITE_QA_PACK_STAGED",
            "Pi_A^n=0 is the clean zero theorem, but current sources do not sign the parent boundary/source action.",
            "retain finite Q_A and use acquisition rows for C_A, lambda_A, R10, PPN, clock, WEP, and orbital routes",
        ),
        (
            "DEC2013_1_external_bounds_status",
            "EXTERNAL_COMPARATORS_EXIST_BUT_DO_NOT_SCORE_MTS",
            "R10 has a nonclaim review candidate and anchors; PPN/clock/WEP comparators exist; none substitutes for Q_A/C_A/lambda_A.",
            "do not score until theory-side prediction and promotion gates exist",
        ),
        (
            "DEC2013_2_next_attack",
            "FIRST_REAL THEORY-SIDE INPUT IS NOW THE BOTTLENECK",
            "The bound side is better organized than the A-hair prediction side.",
            "derive C_A/lambda_A/profile from A Green kernel or run a strict placeholder-refusal comparator",
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
            "target_id": "NEXT2013_0_2014",
            "selected": "true",
            "next_doc": "2014-Y5-R2FR-Aframe-Green-kernel-normalization-or-QA-comparator-refusal-runner.md",
            "next_script": "scripts/Y5_R2FR_Aframe_Green_kernel_normalization_or_QA_comparator_refusal_runner_2014.py",
            "objective": "derive or source the A-frame Green-kernel normalization that maps Q_A to C_A, lambda_A, profile, and alpha_A(lambda); if missing, run a strict comparator refusal against existing nonclaim bound ledgers",
            "include": "A Green kernel; C_A=N_A kappa_A Q_A; lambda_A range rule; profile f_A(r); alpha_A matching; R10/PPN/clock/WEP/orbital refusal gates",
            "exclude": "claim from external bounds alone; anchor-only interpolation; ordinary current conservation as zero proof; local-GR claim; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update(
            {
                "copy_id": f"COPY2013_{idx}",
                "copy_path": str(path),
                "exists": str(path.exists()),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    boundary_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    refusal_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    checks = [
        ("VAL2013_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"),
        ("VAL2013_01_boundary_not_promoted", any(row["status"] == "BOUNDARY_NEUTRALITY_NOT_DERIVED" for row in boundary_rows) and all(row["parent_signed"] == "false" for row in boundary_rows), "Pi_A boundary neutrality not falsely promoted"),
        ("VAL2013_02_acquisition_core_slots", {"ACQ2013_0_QA_parent", "ACQ2013_1_CA", "ACQ2013_2_lambda_A", "ACQ2013_3_R10_external_curve", "ACQ2013_6_PPN_gamma"}.issubset({row["acq_id"] for row in acquisition_rows}), "acquisition rows cover Q_A/C_A/lambda_A/R10/PPN"),
        ("VAL2013_03_no_scores_ready", all(row["score_ready"] == "false" for row in acquisition_rows), "no finite Q_A acquisition row is score-ready"),
        ("VAL2013_04_refusals_active", all(row["runner_status"] == "REFUSE" and row["accepted_for_claim"] == "false" for row in refusal_rows), "comparator runner refuses missing inputs"),
        ("VAL2013_05_claim_gates_blocked", all(row["passed_for_claim"] == "false" for row in claim_gates), "all claim gates remain blocked"),
        ("VAL2013_06_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2013_07_branch_copies", all(path.exists() for path in branch_paths), "branch-copy CSVs exist"),
        ("VAL2013_08_no_formalization_edits", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains 0 for this run"),
        ("VAL2013_09_output_scope", all(ROOT in [path, *path.parents] for path in [*output_paths, *branch_paths, DOC]), "all outputs are under post-checkpoint-work"),
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
            "check_id": "VAL2013_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2013 A-frame finite Q_A bound acquisition or boundary neutrality proof",
        }
    )
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    boundary_rows: list[dict[str, object]],
    acquisition_rows: list[dict[str, object]],
    refusal_rows: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 2013 Y5 R2FR: A-Frame Finite Q_A Bound Source Acquisition Or Boundary Neutrality Proof

Private checkpoint. This makes one focused attempt to derive `Pi_A^n=0`; when that does not sign, it stages the finite `Q_A` bound-source acquisition rows without scoring them.

## Current Verdict

The boundary/source-neutrality proof still does **not** close. The exact zero theorem is clear: derive the source-boundary variation and show `Pi_A^n=0`, so `Q_A=0`. But the current corpus does not parent-sign the source/boundary action or no-spurion source neutrality needed to enforce that.

The fallback is now cleaner. Finite `Q_A` has a bound-source acquisition ledger: theory-side rows for `Q_A`, `C_A`, `lambda_A`, profile and `alpha_A(lambda_A)`; external-side rows for R10, PPN, clock, WEP, and orbital comparators. Existing R10/PPN/clock/WEP sources help, but they cannot score MTS without the missing theory-side prediction and promotion gates.

No local-GR/Newton/WEP/R10 claim is promoted.

## Source Register
{md_table(sources, ["source_id", "source_path", "status", "needles", "note"])}

## Boundary Neutrality Attempt
{md_table(boundary_rows, ["proof_id", "clause", "status", "missing_before_claim", "parent_signed"])}

## Finite Q_A Bound Acquisition Ledger
{md_table(acquisition_rows, ["acq_id", "symbol", "meaning", "side", "status", "local_or_source", "numeric_value", "units", "score_ready"])}

## Comparator Refusal Runner
{md_table(refusal_rows, ["refusal_id", "attempted_score", "runner_status", "refusal_reasons", "score_ready", "accepted_for_claim"])}

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
    boundary_rows = boundary_neutrality_rows()
    acquisition_rows = finite_bound_acquisition_rows()
    refusal_rows = comparator_refusal_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2013_SOURCE_REGISTER.csv",
        "boundary": OUT / "P8_Y5_PARENT_QLOC_2013_BOUNDARY_NEUTRALITY_ATTEMPT.csv",
        "acquisition": OUT / "P8_Y5_PARENT_QLOC_2013_FINITE_QA_BOUND_ACQUISITION_LEDGER.csv",
        "refusals": OUT / "P8_Y5_PARENT_QLOC_2013_COMPARATOR_REFUSAL_RUNNER.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2013_CLAIM_GATE.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2013_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2013_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["boundary"], boundary_rows)
    write_csv(output_map["acquisition"], acquisition_rows)
    write_csv(output_map["refusals"], refusal_rows)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "AFRAME_QA_BOUNDARY_NEUTRALITY_2013_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2013_FINITE_QA_BOUND_STATUS_NONCLAIM.csv",
        QUEUE / "JR2013_AFRAME_QA_BOUND_ACQUISITION_QUEUE.csv",
    ]
    for path in branch_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["boundary"], branch_paths[0])
    shutil.copyfile(output_map["acquisition"], branch_paths[1])
    shutil.copyfile(output_map["refusals"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "A-frame Q_A boundary neutrality attempt nonclaim copy",
            "finite Q_A bound acquisition status nonclaim copy",
            "finite Q_A comparator refusal/acquisition queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2013_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, boundary_rows, acquisition_rows, refusal_rows, claim_gates, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2013_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, boundary_rows, acquisition_rows, refusal_rows, claim_gates, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2013_OVERALL"][0]["status"]
    print(f"VAL2013_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
