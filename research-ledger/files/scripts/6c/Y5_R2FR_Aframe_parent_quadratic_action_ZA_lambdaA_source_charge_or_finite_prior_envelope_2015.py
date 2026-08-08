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
DOC = ROOT / "2015-Y5-R2FR-Aframe-parent-quadratic-action-ZA-lambdaA-source-charge-or-finite-prior-envelope.md"
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
            "SRC2015_00_2014_handoff",
            "2014-Y5-R2FR-Aframe-Green-kernel-normalization-or-QA-comparator-refusal-runner.md",
            ["NEXT2014_0_2015", "AGK2014_8_verdict", "VAL2014_OVERALL"],
            "2014 selected parent quadratic A action or finite prior envelope.",
        ),
        (
            "SRC2015_01_1036_X_analogy",
            "1036-Y5-R10-parent-X-quadratic-action-and-beta-source-test-split.md",
            ["PX1036_1_quadratic_residue", "BETA1036_1_two_body_exchange", "DEC1036_0_parent_row_status"],
            "finite-X quadratic row analogy: residue/range/source split remains unowned.",
        ),
        (
            "SRC2015_02_1035_kernel_contract",
            "1035-Y5-R10-KX-green-kernel-normalization-and-profile-integral.md",
            ["KXD1035_0_parent_quadratic_operator", "KXD1035_2_point_body_yukawa_match", "V1035_SUMMARY"],
            "conditional Green-kernel and Yukawa matching contract.",
        ),
        (
            "SRC2015_03_2012_QA_rows",
            "2012-Y5-R2FR-Aframe-current-nohair-source-neutrality-theorem-or-finite-QA-row.md",
            ["FQA2012_0_QA", "FQA2012_2_CA", "FQA2012_5_alpha"],
            "finite Q_A rows that require parent quadratic normalization.",
        ),
        (
            "SRC2015_04_2013_bound_pack",
            "2013-Y5-R2FR-Aframe-finite-QA-bound-source-acquisition-or-boundary-neutrality-proof.md",
            ["ACQ2013_0_QA_parent", "REF2013_0_R10", "VAL2013_OVERALL"],
            "finite Q_A bound pack and comparator refusal handoff.",
        ),
        (
            "SRC2015_05_1034_R10_curve",
            "1034-Y5-R10-alpha-bound-curve-digitization-and-projection-input-pack.md",
            ["R10P1034_0_alpha_bound_curve", "CGATE1034_1_external_curve", "DEC1034_2_projection_status"],
            "R10 curve/projection pack remains nonclaim.",
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
                "needed_for": "2015 A-frame parent quadratic action or finite prior envelope",
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


def quadratic_action_rows() -> list[dict[str, object]]:
    specs = [
        (
            "PQA2015_0_template",
            "S_A^(2)=1/2 int deltaA L_A deltaA + int kappa_A deltaA_a^mu J_A^a_mu + S_gauge + S_boundary",
            "candidate parent quadratic action row for finite A-frame hair",
            "FORMAL_TEMPLATE_ONLY",
            "parent action block and field normalization missing",
            "false",
        ),
        (
            "PQA2015_1_background_zero",
            "E_A[bar A]=0",
            "local GR background must solve the A equation before perturbing it",
            "MISSING_BACKGROUND_EQUATION",
            "no parent A Euler equation or background branch is signed",
            "false",
        ),
        (
            "PQA2015_2_residue",
            "Z_A",
            "quadratic residue/kinetic coefficient; must have healthy sign or be gauge/constraint-only",
            "MISSING_PARENT_RESIDUE",
            "ghost/anti-elliptic branches not excluded",
            "false",
        ),
        (
            "PQA2015_3_mass_range",
            "M_A^2 and lambda_A",
            "range rule lambda_A=sqrt(Z_A/M_A^2) or hbar/(M_A c) after units are declared",
            "MISSING_PARENT_RANGE_RELATION",
            "no mass gap, screening length, or compact support rule",
            "false",
        ),
        (
            "PQA2015_4_source_current",
            "J_A^a_mu",
            "source current that couples to A and defines Q_A/Pi_A boundary charge",
            "MISSING_SOURCE_CURRENT",
            "source units, boundary variation, and source neutrality not derived",
            "false",
        ),
        (
            "PQA2015_5_coupling",
            "kappa_A",
            "normalization coupling between J_A and A response",
            "MISSING_PARENT_COUPLING",
            "cannot map Q_A to C_A without kappa_A and convention",
            "false",
        ),
        (
            "PQA2015_6_gauge_constraints",
            "split-gauge/local-Lorentz/diffeomorphism constraints",
            "must remove unphysical A representatives and avoid extra local modes",
            "MISSING_CONSTRAINT_ALGEBRA",
            "no first-class/no-pole theorem signed",
            "false",
        ),
        (
            "PQA2015_7_metric_projection",
            "P_00^A and P_PPN^A",
            "projection from A perturbation to h_00 and PPN/vector observables",
            "MISSING_METRIC_PROJECTION",
            "cannot compare finite A hair to Newton/PPN/clock without this",
            "false",
        ),
        (
            "PQA2015_8_two_body_source_test",
            "source leg times test/readout leg",
            "R10/force comparisons require source and test charges unless Q_A already encodes a worldtube response",
            "COUPLING_SPLIT_REQUIRED",
            "source/test split or worldtube normalization not declared",
            "false",
        ),
        (
            "PQA2015_9_verdict",
            "parent quadratic A action row",
            "The action row is not owned by the current corpus; finite A remains a nonclaim prior/residual branch.",
            "PARENT_QUADRATIC_A_NOT_DERIVED",
            "try no-physical-A-pole theorem or finite prior envelope next",
            "false",
        ),
    ]
    rows: list[dict[str, object]] = []
    for action_id, object_text, role, status, missing_before_claim, parent_signed in specs:
        row = base_row()
        row.update(
            {
                "action_id": action_id,
                "object": object_text,
                "role": role,
                "status": status,
                "missing_before_claim": missing_before_claim,
                "parent_signed": parent_signed,
            }
        )
        rows.append(row)
    return rows


def branch_classification_rows() -> list[dict[str, object]]:
    specs = [
        (
            "BR2015_0_no_physical_A_pole",
            "A is pure gauge/constraint/quotient in the local GR exterior",
            "alpha_A=0 or not applicable if matter/readout are invariant",
            "BEST_LOCAL_GR_ROUTE_BUT_UNSIGNED",
            "requires first-class constraint, no-spurion matter, boundary silence, and no hidden pole",
        ),
        (
            "BR2015_1_sourcefree_massive_nohair",
            "Z_A>0, M_A^2>0, J_A=0, Pi_A^n=0",
            "finite A mode exists but has no compact local exterior hair",
            "CONDITIONAL_NOHAIR_UNSIGNED",
            "requires source-neutrality and boundary no-flux theorem",
        ),
        (
            "BR2015_2_sourced_finite_exchange",
            "physical finite A exchange with Q_A != 0",
            "alpha_A(lambda)=K_A(lambda) beta_source^A beta_test^A or worldtube-normalized equivalent",
            "SCOREABLE_STRUCTURE_INPUTS_MISSING",
            "requires Z_A, lambda_A, kappa_A, Q_A, projection, profile, promoted external bounds",
        ),
        (
            "BR2015_3_long_range_A",
            "lambda_A local/solar-system scale or infinite",
            "R10 is not sufficient; PPN/orbital/clock become primary",
            "LONG_RANGE_BRANCH_BLOCKED",
            "requires PPN/orbital projection before any local-GR claim",
        ),
        (
            "BR2015_4_verdict",
            "branch selection",
            "no-pole/nohair is cleaner but unsigned; finite exchange remains retained as a bounded residual branch",
            "BRANCHES_RETAINED_NONCLAIM",
            "do not collapse finite A into a claim without one branch signing",
        ),
    ]
    rows: list[dict[str, object]] = []
    for branch_id, branch, implication, status, next_requirement in specs:
        row = base_row()
        row.update(
            {
                "branch_row": branch_id,
                "branch": branch,
                "implication": implication,
                "status": status,
                "next_requirement": next_requirement,
            }
        )
        rows.append(row)
    return rows


def finite_prior_envelope_rows() -> list[dict[str, object]]:
    specs = [
        ("PRIOR2015_0_QA", "Q_A", "finite A charge amplitude", "MISSING_PRIOR_RANGE", "A-charge units"),
        ("PRIOR2015_1_ZA", "Z_A", "quadratic residue/sign", "MISSING_PRIOR_RANGE_AND_SIGN", "model-dependent"),
        ("PRIOR2015_2_lambdaA", "lambda_A", "finite range/screening length", "MISSING_PRIOR_RANGE", "m"),
        ("PRIOR2015_3_kappaA", "kappa_A", "source-current coupling", "MISSING_PRIOR_RANGE", "model-dependent"),
        ("PRIOR2015_4_P00", "P_00^A", "metric projection to h_00", "MISSING_PRIOR_RANGE", "dimensionless"),
        ("PRIOR2015_5_beta_source", "beta_source_A", "source leg if finite exchange is two-body", "MISSING_SOURCE_CHARGE_PRIOR", "dimensionless_or_declared"),
        ("PRIOR2015_6_beta_test", "beta_test_A", "test/readout leg if finite exchange is two-body", "MISSING_TEST_CHARGE_PRIOR", "dimensionless_or_declared"),
        ("PRIOR2015_7_profile", "F_ST^A(lambda)", "finite-size/profile/harmonic projection", "MISSING_PROFILE_PRIOR", "dimensionless"),
        ("PRIOR2015_8_alphaA", "alpha_A(lambda_A)", "Yukawa-equivalent prediction envelope", "MISSING_JOIN_PRIOR", "dimensionless"),
        ("PRIOR2015_9_total", "R_A_prior", "finite prior envelope for all A local residuals", "NOT_RUNNABLE_NO_PRIORS", "mixed"),
    ]
    rows: list[dict[str, object]] = []
    for prior_id, symbol, meaning, status, units in specs:
        row = base_row()
        row.update(
            {
                "prior_id": prior_id,
                "symbol": symbol,
                "meaning": meaning,
                "status": status,
                "prior_min": "MISSING",
                "prior_max": "MISSING",
                "units": units,
                "score_ready": "false",
            }
        )
        rows.append(row)
    return rows


def refusal_rows() -> list[dict[str, object]]:
    specs = [
        (
            "REF2015_0_parent_action",
            "promote parent quadratic A row",
            "REFUSE",
            "Z_A, M_A/lambda_A, kappa_A, J_A, gauge constraints, P_00, and boundary/source action are missing",
        ),
        (
            "REF2015_1_finite_prior",
            "run finite prior envelope",
            "REFUSE",
            "all prior ranges are missing; no conservative numerical envelope has been sourced",
        ),
        (
            "REF2015_2_R10",
            "score alpha_A(lambda) against R10 bound",
            "REFUSE",
            "alpha_A missing; external curve nonclaim; source/test/profile normalization missing",
        ),
        (
            "REF2015_3_PPN_clock_WEP",
            "score PPN/clock/WEP",
            "REFUSE",
            "A metric/matter projections and source/test charges missing",
        ),
        (
            "REF2015_4_local_GR",
            "claim local GR/Newton reduction",
            "REFUSE",
            "finite A branch, q_loc, R11, matter silence, and A ownership remain open",
        ),
    ]
    rows: list[dict[str, object]] = []
    for refusal_id, attempted_action, runner_status, refusal_reasons in specs:
        row = base_row()
        row.update(
            {
                "refusal_id": refusal_id,
                "attempted_action": attempted_action,
                "runner_status": runner_status,
                "refusal_reasons": refusal_reasons,
                "accepted_for_claim": "false",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("CG2015_0_template", "quadratic A action template written", "PASS_NONCLAIM", "formal row exists"),
        ("CG2015_1_parent_action", "parent action supplies Z_A, M_A, kappa_A, J_A, constraints", "FAIL_BLOCKED", "not parent-owned by current corpus"),
        ("CG2015_2_no_physical_pole", "finite A pole is absent/pure gauge", "FAIL_BLOCKED", "no first-class/no-spurion/no-boundary theorem"),
        ("CG2015_3_finite_prior", "finite prior envelope is runnable", "FAIL_BLOCKED", "all prior numeric ranges missing"),
        ("CG2015_4_R10_PPN_clock_WEP", "finite A branch score-ready", "FAIL_BLOCKED", "theory-side factors and promoted comparators missing"),
        ("CG2015_5_local_GR_Newton", "local GR/Newton derived", "FAIL_BLOCKED", "A, q_loc, R11, and matter-silence gates remain open"),
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
            "DEC2015_0_result",
            "PARENT_QUADRATIC_A_NOT_DERIVED",
            "The exact finite-A parent row is now written, but none of Z_A, M_A/lambda_A, kappa_A, J_A, constraints, or P_00 is parent-signed.",
            "do not score finite A; target no-physical-A-pole theorem or source finite priors",
        ),
        (
            "DEC2015_1_best_theory_route",
            "NO_PHYSICAL_A_POLE_IS_THE_CLEANEST_LOCAL_GR_ROUTE",
            "If A has no physical local pole or is pure gauge/constraint in the exterior, local GR is protected without tuning finite bounds.",
            "attempt first-class/no-pole theorem before numeric prior work",
        ),
        (
            "DEC2015_2_empirical_route",
            "FINITE_PRIOR_ENVELOPE_EXISTS_AS_SCHEMA_ONLY",
            "If no-pole fails, finite A must be bounded, but even the prior ranges are currently missing.",
            "source conservative prior ranges or derive them from a parent action before any comparator run",
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
            "target_id": "NEXT2015_0_2016",
            "selected": "true",
            "next_doc": "2016-Y5-R2FR-Aframe-no-physical-pole-gauge-constraint-theorem-or-finite-prior-runner.md",
            "next_script": "scripts/Y5_R2FR_Aframe_no_physical_pole_gauge_constraint_theorem_or_finite_prior_runner_2016.py",
            "objective": "try to prove the finite A mode has no physical local pole because it is gauge/constraint/quotient-null with matter/readout invariance; if not, build a strict finite-prior runner for Q_A, Z_A, lambda_A, kappa_A, and P_00 without scoring claims",
            "include": "first-class constraint; no-spurion matter/readout; boundary charge zero; no hidden pole; finite prior schema; comparator refusal gates",
            "exclude": "invented numeric priors; external-bound-only claims; anchor interpolation; local-GR claim; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def branch_copy_rows(paths: list[Path], notes: list[str]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for idx, (path, note) in enumerate(zip(paths, notes, strict=True)):
        row = base_row()
        row.update(
            {
                "copy_id": f"COPY2015_{idx}",
                "copy_path": str(path),
                "exists": str(path.exists()),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    action_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    prior_rows: list[dict[str, object]],
    refusals: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    output_paths: list[Path],
    branch_paths: list[Path],
) -> list[dict[str, object]]:
    checks = [
        ("VAL2015_00_sources", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources), "all cited source paths exist and needles are found"),
        ("VAL2015_01_parent_row_not_promoted", any(row["status"] == "PARENT_QUADRATIC_A_NOT_DERIVED" for row in action_rows) and all(row["parent_signed"] == "false" for row in action_rows), "parent quadratic A row not falsely promoted"),
        ("VAL2015_02_required_objects_present", {"PQA2015_2_residue", "PQA2015_3_mass_range", "PQA2015_4_source_current", "PQA2015_7_metric_projection"}.issubset({row["action_id"] for row in action_rows}), "Z_A/lambda_A/J_A/P_00 requirements are present"),
        ("VAL2015_03_branch_fork_recorded", any(row["status"] == "BEST_LOCAL_GR_ROUTE_BUT_UNSIGNED" for row in branch_rows) and any(row["status"] == "SCOREABLE_STRUCTURE_INPUTS_MISSING" for row in branch_rows), "no-pole and finite-exchange branches both recorded"),
        ("VAL2015_04_prior_rows_missing", all(row["prior_min"] == "MISSING" and row["prior_max"] == "MISSING" and row["score_ready"] == "false" for row in prior_rows), "finite prior envelope rows remain missing/nonclaim"),
        ("VAL2015_05_refusals_active", all(row["runner_status"] == "REFUSE" and row["accepted_for_claim"] == "false" for row in refusals), "refusal rows block promotion/scoring"),
        ("VAL2015_06_claim_gates_blocked", all(row["passed_for_claim"] == "false" for row in claim_gates), "all claim gates remain blocked"),
        ("VAL2015_07_csv_parse", all(path.exists() and csv_rows_parse(path) for path in output_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2015_08_branch_copies", all(path.exists() for path in branch_paths), "branch-copy CSVs exist"),
        ("VAL2015_09_no_formalization_edits", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains 0 for this run"),
        ("VAL2015_10_output_scope", all(ROOT in [path, *path.parents] for path in [*output_paths, *branch_paths, DOC]), "all outputs are under post-checkpoint-work"),
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
            "check_id": "VAL2015_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2015 A-frame parent quadratic action or finite prior envelope",
        }
    )
    rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    action_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    prior_rows: list[dict[str, object]],
    refusals: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    branch_copies: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 2015 Y5 R2FR: A-Frame Parent Quadratic Action Z_A Lambda_A Source Charge Or Finite Prior Envelope

Private checkpoint. This tries to make the finite A-frame residual a real parent-action object instead of a symbolic Green-kernel placeholder.

## Current Verdict

The parent quadratic A action row is **not derived yet**. The exact row is now explicit: `S_A^(2)` must supply the background equation, residue `Z_A`, range/mass `M_A` or `lambda_A`, source current `J_A`, coupling `kappa_A`, gauge/no-extra-mode constraints, boundary charge, and metric projection `P_00^A`.

The cleanest route remains a no-physical-A-pole theorem: if A is quotient-null, first-class gauge, or constraint-only in the local exterior and matter/readout are invariant, finite `Q_A` disappears without tuning. If that cannot be proven, finite A stays as a residual branch, but even the prior envelope is not runnable because every numerical prior range is missing.

No local-GR/Newton/WEP/R10 claim is promoted.

## Source Register
{md_table(sources, ["source_id", "source_path", "status", "needles", "note"])}

## Parent Quadratic A Action Attempt
{md_table(action_rows, ["action_id", "object", "role", "status", "missing_before_claim", "parent_signed"])}

## Branch Classification
{md_table(branch_rows, ["branch_row", "branch", "implication", "status", "next_requirement"])}

## Finite Prior Envelope Schema
{md_table(prior_rows, ["prior_id", "symbol", "meaning", "status", "prior_min", "prior_max", "units", "score_ready"])}

## Refusal Runner
{md_table(refusals, ["refusal_id", "attempted_action", "runner_status", "refusal_reasons", "accepted_for_claim"])}

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
    action_rows = quadratic_action_rows()
    branch_rows = branch_classification_rows()
    prior_rows = finite_prior_envelope_rows()
    refusals = refusal_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    output_map = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2015_SOURCE_REGISTER.csv",
        "action": OUT / "P8_Y5_PARENT_QLOC_2015_PARENT_QUADRATIC_A_ACTION_ATTEMPT.csv",
        "branches": OUT / "P8_Y5_PARENT_QLOC_2015_BRANCH_CLASSIFICATION.csv",
        "priors": OUT / "P8_Y5_PARENT_QLOC_2015_FINITE_PRIOR_ENVELOPE_SCHEMA.csv",
        "refusals": OUT / "P8_Y5_PARENT_QLOC_2015_REFUSAL_RUNNER.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2015_CLAIM_GATE.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2015_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_PARENT_QLOC_2015_NEXT_TARGET.csv",
    }
    write_csv(output_map["sources"], sources)
    write_csv(output_map["action"], action_rows)
    write_csv(output_map["branches"], branch_rows)
    write_csv(output_map["priors"], prior_rows)
    write_csv(output_map["refusals"], refusals)
    write_csv(output_map["claim_gates"], claim_gates)
    write_csv(output_map["decisions"], decisions)
    write_csv(output_map["next_target"], next_target)

    branch_paths = [
        SOURCE_WEIGHT_DOCS / "AFRAME_PARENT_QUADRATIC_2015_NONCLAIM.csv",
        BRANCH_WEP / "P8_Y5_PARENT_QLOC_2015_AFRAME_BRANCH_STATUS_NONCLAIM.csv",
        QUEUE / "JR2015_AFRAME_FINITE_PRIOR_ENVELOPE_QUEUE.csv",
    ]
    for path in branch_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(output_map["action"], branch_paths[0])
    shutil.copyfile(output_map["branches"], branch_paths[1])
    shutil.copyfile(output_map["priors"], branch_paths[2])

    branch_copies = branch_copy_rows(
        branch_paths,
        [
            "A-frame parent quadratic action attempt nonclaim copy",
            "A-frame branch classification status nonclaim copy",
            "A-frame finite prior envelope queue",
        ],
    )
    branch_copy_path = OUT / "P8_Y5_PARENT_QLOC_2015_BRANCH_COPIES.csv"
    write_csv(branch_copy_path, branch_copies)

    output_paths = [*output_map.values(), branch_copy_path]
    validation = validation_rows(sources, action_rows, branch_rows, prior_rows, refusals, claim_gates, output_paths, branch_paths)
    validation_path = OUT / "P8_Y5_BRR545_2015_VALIDATION.csv"
    write_csv(validation_path, validation)
    output_paths.append(validation_path)

    write_doc(sources, action_rows, branch_rows, prior_rows, refusals, claim_gates, decisions, branch_copies, next_target, validation)
    remove_pycache()

    overall = [row for row in validation if row["check_id"] == "VAL2015_OVERALL"][0]["status"]
    print(f"VAL2015_OVERALL={overall}")
    print(str(DOC))
    for path in output_paths:
        print(str(path))
    for path in branch_paths:
        print(str(path))


if __name__ == "__main__":
    main()
