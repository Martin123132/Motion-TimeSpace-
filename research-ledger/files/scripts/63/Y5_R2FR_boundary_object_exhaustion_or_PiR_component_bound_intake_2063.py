from __future__ import annotations

from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2063-Y5-R2FR-boundary-object-exhaustion-or-PiR-component-bound-intake.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2063_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2063-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2063*",
            "*Y5_R2FR_boundary_object_exhaustion_or_PiR_component_bound_intake_2063*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2063_00_2062_doc",
            ROOT / "2062-Y5-R2FR-boundary-corner-RAB-silence-or-finite-PiR-bound-row.md",
            ["NEXT2062_0_2063", "Fixed `R_AB` boundary data is explicitly rejected", "finite fallback is now source-ready"],
            "2062 handoff into boundary object-exhaustion or finite Pi_R component rows.",
        ),
        (
            "SRC2063_01_2062_next",
            OUT / "P8_Y5_PARENT_QLOC_2062_NEXT_TARGET.csv",
            ["NEXT2062_0_2063", "allowed boundary objects", "finite component schema"],
            "machine-readable 2063 target.",
        ),
        (
            "SRC2063_02_2062_grammar",
            OUT / "P8_Y5_PARENT_QLOC_2062_BOUNDARY_FUNCTIONAL_GRAMMAR.csv",
            ["BGA2062_0_boundary_split", "BGA2062_2_fixed_boundary_rejection", "BGA2062_3_corner_worldtube"],
            "boundary grammar split and fixed-boundary rejection.",
        ),
        (
            "SRC2063_03_2062_schema",
            OUT / "P8_Y5_PARENT_QLOC_2062_FINITE_PIR_TOT_BOUND_ROW_SCHEMA.csv",
            ["PIR2062_1_boundary", "PIR2062_2_corner", "MISSING_COMPONENT_ZERO_OR_BOUND"],
            "finite Pi_R component schema inherited from 2062.",
        ),
        (
            "SRC2063_04_1265_protection",
            OUT / "P8_Y5_R10_1265_AUXILIARY_PROTECTION_AUDIT.csv",
            ["AP1265_3_boundary_silence", "Parent boundary/corner grammar contains no `B_R(R_AB)`", "UNSIGNED_BOUNDARY_PROTECTION"],
            "AP1265 boundary-silence clause.",
        ),
        (
            "SRC2063_05_1269_object",
            OUT / "P8_Y5_R10_1269_OPERATOR_EXCLUSION_PARENT_SORT_ATTEMPT.csv",
            ["OP1269_2_object_exhaustion", "Allowed[S_parent]", "EXACT_CONDITIONAL_NOT_DERIVED"],
            "operator/object-exhaustion precedent.",
        ),
        (
            "SRC2063_06_1269_gates",
            OUT / "P8_Y5_R10_1269_CLAIM_GATES.csv",
            ["GATE1269_0_AP1265_1", "object-language exhaustion", "BLOCKED"],
            "object-exhaustion claim gate remains blocked.",
        ),
        (
            "SRC2063_07_1566_protection",
            OUT / "P8_Y5_PARENT_QLOC_1566_PROTECTION_PROOF_AUDIT.csv",
            ["PROT1566_1_BR_boundary", "UNSIGNED_BOUNDARY_SILENCE", "bulk auxiliary status does not exclude corner/source-worldtube hair"],
            "latest boundary protection blocker.",
        ),
        (
            "SRC2063_08_1020_boundary",
            ROOT / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            ["BDC1020_0_surface_manifold", "ETB1020_2_zero_conditions", "ETB1020_3_residual_bound"],
            "boundary/corner/cohomology zero-or-bound precedent.",
        ),
        (
            "SRC2063_09_1165_corner",
            ROOT / "1165-Y5-R10-lifted-C-sector-parent-action-contract-or-Ccorner-zero-bound.md",
            ["CCZ1165_0_surface_without_corners", "CCZ1165_6_finite_bound", "MISSING_LOCAL_SURFACE_CERTIFICATE"],
            "corner certificate and finite-bound precedent.",
        ),
        (
            "SRC2063_10_1001_surface",
            ROOT / "1001-Y5-R10-Bref-radius-surface-term-theorem-or-Delta-ref-radial-profile-row.md",
            ["MISSING_CLOSED_BREF_AND_CORNER_CERTIFICATE", "zero-by-boundary-silence and zero-by-fixed-radius are rejected", "corner certificates are absent"],
            "surface/corner guardrail precedent.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needles, note in specs:
        exists = source_path.exists()
        text = read_text(source_path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_path": str(source_path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def allowed_boundary_object_rows() -> list[dict[str, object]]:
    data = [
        (
            "ABO2063_0_GHY_public_metric",
            "GHY/public metric boundary term",
            "B_GHY[q,theta,top] or equivalent public coframe metric term",
            "ALLOWED_IF_Q_ONLY",
            "no explicit R_AB/Lambda_R dependence and no hidden representative marker",
        ),
        (
            "ABO2063_1_reference_fixed",
            "reference/counterterm class",
            "B_ref[q,theta,top; fixed class]",
            "ALLOWED_IF_FIXED_NO_RETUNE",
            "must be fixed before readout and cannot absorb Pi_R after the fact",
        ),
        (
            "ABO2063_2_topological_exact",
            "topological/exact boundary class",
            "B_top[class] or d_boundary b with certified corners/harmonic sector",
            "ALLOWED_IF_CLASS_CERTIFIED",
            "needs corner, cohomology and no-retune certificates",
        ),
        (
            "ABO2063_3_matter_worldtube",
            "matter/source worldtube boundary",
            "B_matter[Psi,q(Phi),theta]",
            "ALLOWED_IF_MATTER_DESCENDS",
            "no direct R_AB/Lambda_R source vertex",
        ),
        (
            "ABO2063_4_RAB_boundary",
            "R_AB boundary functional",
            "B_R[R_AB] or beta_R integral_S R_AB",
            "FORBIDDEN_NEEDED_BUT_NOT_PARENT_SIGNED",
            "this is exactly the term object-exhaustion must exclude",
        ),
        (
            "ABO2063_5_RAB_corner",
            "R_AB corner/worldtube endpoint functional",
            "B_corner contains beta_corner R_AB|_corner",
            "FORBIDDEN_NEEDED_BUT_NOT_PARENT_SIGNED",
            "corner certificate is not in the current corpus",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_class, allowed_form, status, condition in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object_class": object_class,
                "allowed_or_forbidden_form": allowed_form,
                "status": status,
                "condition_or_gap": condition,
                "parent_signed": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def exhaustion_attempt_rows() -> list[dict[str, object]]:
    data = [
        (
            "BOE2063_0_theorem_contract",
            "boundary object-exhaustion theorem",
            "AllowedBoundary[S_parent] = {B_GHY[q,theta,top], B_ref[q,theta,top], B_top[class], B_matter[Psi,q,theta]} and excludes any local functional of R_AB or Lambda_R.",
            "would imply delta B_total/delta R_AB = 0 and Pi_R^corner = 0",
            "EXACT_IF_PARENT_OBJECT_LANGUAGE_SIGNED",
            "the needed theorem is clear",
        ),
        (
            "BOE2063_1_parent_sort_dependency",
            "dependency on R_AB sort",
            "R_AB must be parent auxiliary compatibility data, not a boundary observable or hidden scalar.",
            "otherwise B_R[R_AB] is a legal boundary observable",
            "NOT_PARENT_SIGNED",
            "inherits OP1269_0 and AP1265_0 uncertainty",
        ),
        (
            "BOE2063_2_boundary_generator_dependency",
            "dependency on boundary generator list",
            "the parent action must enumerate all allowed boundary/corner generators and show none accept R_AB arguments.",
            "absence by not-writing-it is not proof",
            "MISSING_BOUNDARY_GENERATOR_EXHAUSTION",
            "current corpus has no complete boundary object language",
        ),
        (
            "BOE2063_3_countermodel_boundary",
            "boundary countermodel",
            "Add B_R = integral_S beta_R R_AB dSigma while keeping the bulk auxiliary block unchanged.",
            "delta B_R/delta R_AB=beta_R and Q_R=-Pi_R^tot can be nonzero",
            "COUNTERMODEL_OPEN",
            "bulk auxiliary elimination alone cannot exclude boundary hair",
        ),
        (
            "BOE2063_4_countermodel_corner",
            "corner countermodel",
            "Add B_corner = beta_corner R_AB|_C at a joint/regulator/source-worldtube endpoint.",
            "Pi_R^corner=beta_corner unless a corner certificate forbids or bounds it",
            "COUNTERMODEL_OPEN",
            "smooth-corner-free assumptions are not arena-certified",
        ),
        (
            "BOE2063_5_verdict",
            "object-exhaustion verdict",
            "The proof route is coherent but not parent-derived; finite Pi_R^boundary and Pi_R^corner rows remain mandatory.",
            "no Pi_R=0, Q_R=0, Cassini, or local-GR claim follows",
            "CONDITIONAL_PROOF_ONLY",
            "move to component bound/certificate intake",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, target, statement, implication, status, note in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "target": target,
                "statement": statement,
                "implication": implication,
                "status": status,
                "note": note,
                "accepted_as_parent_proof": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def finite_component_intake_rows() -> list[dict[str, object]]:
    data = [
        (
            "PCI2063_0_boundary_zero_switch",
            "Pi_R^boundary_zero",
            "theorem_zero=true only if boundary_object_exhaustion_parent_signed=true",
            "boolean theorem gate",
            "source path/equation proving AllowedBoundary excludes B_R(R_AB)",
            "MISSING_BOUNDARY_OBJECT_EXHAUSTION_THEOREM",
        ),
        (
            "PCI2063_1_boundary_bound",
            "Pi_R^boundary_abs",
            "|delta B_R/delta R_AB| on declared worldtube surface",
            "boundary-current units",
            "beta_R value/bound, surface measure, units, source path, equation anchor",
            "MISSING_BOUNDARY_COEFFICIENT_BETA_R",
        ),
        (
            "PCI2063_2_corner_zero_switch",
            "Pi_R^corner_zero",
            "theorem_zero=true only if actual readout/source worldtube has no active corners or every corner term is R_AB-silent",
            "boolean theorem gate",
            "corner-free surface certificate or R_AB-silent corner grammar",
            "MISSING_CORNER_CERTIFICATE",
        ),
        (
            "PCI2063_3_corner_bound",
            "Pi_R^corner_abs",
            "|beta_corner| summed over joints/endpoints/regulators",
            "boundary-current units",
            "corner ledger, beta_corner values/bounds, units, source path, equation anchor",
            "MISSING_CORNER_COEFFICIENT_BETA_CORNER",
        ),
        (
            "PCI2063_4_total_join",
            "Pi_R^tot_abs",
            "|Pi_R^matter| + |Pi_R^boundary| + |Pi_R^corner| + |Pi_R^readout|",
            "boundary-current units",
            "component values or zero theorems with no cancellation",
            "MISSING_COMPONENT_ABSOLUTE_SUM",
        ),
        (
            "PCI2063_5_qR_Cassini_join",
            "q_R^PPN guard",
            "|Pi_R^tot/(N_sphere Z_R_infty r_s)| + B_tail_abs <= 6.70e-05",
            "dimensionless",
            "N_sphere, Z_R_infty, same-frame r_s, absolute tails, orientation convention",
            "MISSING_NORMALIZATION_AND_TAILS",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, formula, units, required_input, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "formula": formula,
                "units": units,
                "required_input": required_input,
                "blocker": blocker,
                "source_ready_schema": True,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def dry_run_rows(objects: list[dict[str, object]], attempt: list[dict[str, object]], intake: list[dict[str, object]]) -> list[dict[str, object]]:
    forbidden_unclosed = [row for row in objects if "FORBIDDEN_NEEDED" in str(row["status"])]
    verdict = next(row for row in attempt if row["row_id"] == "BOE2063_5_verdict")
    data = [
        (
            "RUN2063_0_allowed_objects",
            "allowed boundary object list",
            "OBJECT_LIST_WRITTEN_NONCLAIM",
            f"forbidden_unclosed_count={len(forbidden_unclosed)}",
            False,
        ),
        (
            "RUN2063_1_object_exhaustion",
            "boundary object-exhaustion theorem",
            "REFUSED_NOT_PARENT_SIGNED",
            str(verdict["status"]),
            False,
        ),
        (
            "RUN2063_2_countermodels",
            "B_R and corner countermodels",
            "COUNTERMODELS_REMAIN_LEGAL_UNTIL_GRAMMAR_CLOSES",
            "beta_R and beta_corner rows must be zeroed or bounded",
            False,
        ),
        (
            "RUN2063_3_finite_components",
            "finite Pi_R component intake",
            "SOURCE_READY_SCHEMA_WRITTEN_NOT_SCORABLE",
            f"intake_rows={len(intake)}; no numeric/theorem-zero component rows supplied",
            False,
        ),
        (
            "RUN2063_VERDICT",
            "boundary object-exhaustion or component bounds",
            "OBJECT_EXHAUSTION_CONDITIONAL_COMPONENT_INTAKE_REQUIRED",
            "no Pi_R zero/local-GR claim; proceed to first component certificate or bound",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for run_id, target, verdict_text, reason, accepted_for_scoring in data:
        row = base_row()
        row.update(
            {
                "run_id": run_id,
                "target": target,
                "verdict": verdict_text,
                "reason": reason,
                "accepted_for_scoring": accepted_for_scoring,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2063_0_object_exhaustion", "parent boundary object-exhaustion excludes B_R/R_AB corner terms", "FAIL_BLOCKED", "no parent-signed boundary generator exhaustion exists"),
        ("GATE2063_1_countermodel", "boundary/corner countermodels excluded", "FAIL_BLOCKED", "beta_R and beta_corner terms remain legal countermodels until grammar closes"),
        ("GATE2063_2_component_bounds", "finite Pi_R boundary/corner components score", "FAIL_BLOCKED", "component values, zero certificates, units and sources are missing"),
        ("GATE2063_3_Cassini", "Cassini/local PPN pass", "FAIL_BLOCKED", "Pi_R^tot and normalization/tail chain remain missing"),
        ("GATE2063_4_local_GR", "derived local GR/Newton claim", "FAIL_BLOCKED", "Pi_R/Q_R zero theorem remains conditional"),
        ("GATE2063_5_formalization", "formalization-workbench edit allowed", "PASS_NO_EDIT", "no formalization-workbench edit is made"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update({"row_id": row_id, "gate": gate, "status": status, "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2063_0_theorem_shape",
            "BOUNDARY_OBJECT_EXHAUSTION_WOULD_CLOSE_THE_BOUNDARY_CLAUSE",
            "If the parent boundary object list is exhaustive and R_AB-free, Pi_R^boundary and Pi_R^corner vanish.",
        ),
        (
            "DEC2063_1_current_status",
            "OBJECT_EXHAUSTION_NOT_PARENT_SIGNED",
            "The corpus has no complete boundary generator theorem; absence of B_R in a candidate action is not a proof.",
        ),
        (
            "DEC2063_2_countermodel_policy",
            "KEEP_BETA_R_AND_BETA_CORNER_VISIBLE",
            "A linear R_AB boundary or corner functional is the simplest legal countermodel until excluded.",
        ),
        (
            "DEC2063_3_next",
            "FIRST_COMPONENT_CERTIFICATE_OR_BOUND",
            "The next productive step is to attack the corner-free/worldtube certificate or fill Pi_R^corner/Pi_R^boundary component bounds.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update({"row_id": row_id, "decision": decision, "rationale": rationale, "claim_allowed": False})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2063_0_2064",
            "target_doc": "2064-Y5-R2FR-corner-free-worldtube-certificate-or-PiR-corner-bound.md",
            "objective": "try to certify the actual local/source worldtube has no active R_AB corner term; if that fails, fill the finite Pi_R^corner bound-row schema before Pi_R^boundary scoring",
            "must_include": "actual boundary surface class; regulator/cutoff joints; source-worldtube endpoints; corner-free theorem switch; beta_corner finite bound; no-cancellation join into Pi_R^tot",
            "excluded": "assuming smooth corners without arena certificate; fixed R_AB boundary as proof; closure as proof; Cassini scoring; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    objects: list[dict[str, object]],
    attempt: list[dict[str, object]],
    intake: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2063_0_source_weight_object_exhaustion",
            SOURCE_WEIGHT_DOCS / "AFRAME_BOUNDARY_OBJECT_EXHAUSTION_2063_CONDITIONAL_NONCLAIM.csv",
            objects + attempt,
        ),
        (
            "COPY2063_1_source_weight_pir_components",
            SOURCE_WEIGHT_DOCS / "AFRAME_PIR_COMPONENT_BOUNDS_2063_SOURCE_ROW_SCHEMA_NONCLAIM.csv",
            intake,
        ),
        (
            "COPY2063_2_wep_dry_run",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2063_OBJECT_EXHAUSTION_DRY_RUN_NONCLAIM.csv",
            dry_rows_,
        ),
        (
            "COPY2063_3_queue_next",
            QUEUE / "JR2063_CORNER_FREE_WORLDTUBE_OR_PIR_CORNER_BOUND_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update({"copy_id": copy_id, "path": str(path), "rows": len(data), "status": "WRITTEN_NONCLAIM_COPY", "claim_allowed": False})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    objects: list[dict[str, object]],
    attempt: list[dict[str, object]],
    intake: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    objects_ok = (
        any(row["row_id"] == "ABO2063_4_RAB_boundary" for row in objects)
        and any(row["row_id"] == "ABO2063_5_RAB_corner" for row in objects)
        and all(not bool(row["parent_signed"]) for row in objects)
    )
    verdict = next(row for row in attempt if row["row_id"] == "BOE2063_5_verdict")
    countermodels_ok = any(row["row_id"] == "BOE2063_3_countermodel_boundary" for row in attempt) and any(
        row["row_id"] == "BOE2063_4_countermodel_corner" for row in attempt
    )
    attempt_ok = verdict["status"] == "CONDITIONAL_PROOF_ONLY" and all(not bool(row["accepted_as_parent_proof"]) for row in attempt) and countermodels_ok
    intake_ok = len(intake) >= 6 and all(bool(row["source_ready_schema"]) and not bool(row["ready_for_scoring"]) for row in intake)
    dry_verdict = next(row for row in dry_rows_ if row["run_id"] == "RUN2063_VERDICT")
    dry_ok = dry_verdict["verdict"] == "OBJECT_EXHAUSTION_CONDITIONAL_COMPONENT_INTAKE_REQUIRED"
    gates_ok = all(row["claim_allowed"] is False for row in gates) and all(row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2063_0_2064"
    no_claim = all(not bool(row.get("claim_allowed", False)) for group in [sources, objects, attempt, intake, dry_rows_, gates, next_rows_] for row in group)
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2063_00_local_sources_exist", source_ok, "all cited source paths and needles exist"))
    checks.append(("VAL2063_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2063_02_allowed_objects", objects_ok, "allowed/forbidden boundary object list keeps R_AB terms unsigned"))
    checks.append(("VAL2063_03_countermodels", attempt_ok, "object-exhaustion remains conditional and countermodels are explicit"))
    checks.append(("VAL2063_04_finite_intake", intake_ok, "finite Pi_R component rows are schema-ready but unscored"))
    checks.append(("VAL2063_05_dry_verdict", dry_ok, "dry run refuses object-exhaustion claim and keeps component intake"))
    checks.append(("VAL2063_06_claim_gates_blocked", gates_ok, "all claim gates remain blocked/nonclaim"))
    checks.append(("VAL2063_07_next_selected", next_ok, "2064 corner-free worldtube target selected"))
    checks.append(("VAL2063_08_no_claim_flags", no_claim, "no generated row allows a claim"))
    checks.append(("VAL2063_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2063_10_no_formalization_artifacts", not formalization_has_2063_artifacts(), "no 2063 artifacts were written under formalization-workbench"))
    checks.append(("VAL2063_11_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2063_OVERALL", overall, "2063 tests boundary object-exhaustion and installs Pi_R component-bound intake without claims"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    objects: list[dict[str, object]],
    attempt: list[dict[str, object]],
    intake: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2063 Y5 R2FR Boundary Object-Exhaustion Or Pi_R Component Bound Intake",
        "",
        "## Current Verdict",
        "",
        "2063 gives the exact boundary object-exhaustion theorem shape but does not close it. If the parent boundary object list is exhaustive and contains only `q/theta/top/matter-descended` objects, with no `R_AB` or `Lambda_R` arguments, then `B_R(R_AB)` and `R_AB` corner terms are illegal and the boundary/corner part of `Pi_R^tot` vanishes.",
        "",
        "The present corpus does not parent-sign that exhaustion. The countermodels remain simple: `B_R = integral beta_R R_AB` or `B_corner = beta_corner R_AB|_C` can source reciprocal hair while leaving the bulk auxiliary block untouched. So absence of such terms in a candidate action is not enough.",
        "",
        "The finite fallback is now componentized: `Pi_R^boundary`, `Pi_R^corner`, and their zero switches/bounds must be filled or theorem-zeroed before joining into `Pi_R^tot`, `q_R^PPN`, and the Cassini guard.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, clock, orbital, boundary-zero, or finite-residual claim is allowed. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Allowed Boundary Object List",
        md_table(objects, ["row_id", "object_class", "allowed_or_forbidden_form", "status", "condition_or_gap", "parent_signed", "claim_allowed"]),
        "## Object-Exhaustion Attempt",
        md_table(attempt, ["row_id", "target", "statement", "implication", "status", "note", "accepted_as_parent_proof", "claim_allowed"]),
        "## Finite Pi_R Component Intake",
        md_table(intake, ["row_id", "quantity", "formula", "units", "required_input", "blocker", "source_ready_schema", "ready_for_scoring", "claim_allowed"]),
        "## Dry Run",
        md_table(dry_rows_, ["run_id", "target", "verdict", "reason", "accepted_for_scoring", "claim_allowed"]),
        "## Claim Gate",
        md_table(gates, ["row_id", "gate", "status", "detail", "claim_allowed"]),
        "## Decision Ledger",
        md_table(decisions, ["row_id", "decision", "rationale", "claim_allowed"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "objective", "must_include", "excluded", "claim_allowed"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    objects = allowed_boundary_object_rows()
    attempt = exhaustion_attempt_rows()
    intake = finite_component_intake_rows()
    dry_rows_ = dry_run_rows(objects, attempt, intake)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2063_SOURCE_REGISTER.csv",
        "objects": OUT / "P8_Y5_PARENT_QLOC_2063_ALLOWED_BOUNDARY_OBJECTS.csv",
        "attempt": OUT / "P8_Y5_PARENT_QLOC_2063_BOUNDARY_OBJECT_EXHAUSTION_ATTEMPT.csv",
        "intake": OUT / "P8_Y5_PARENT_QLOC_2063_FINITE_PIR_COMPONENT_INTAKE.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2063_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2063_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2063_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2063_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2063_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2063_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["objects"], objects)
    write_csv(paths["attempt"], attempt)
    write_csv(paths["intake"], intake)
    write_csv(paths["dry"], dry_rows_)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(objects, attempt, intake, dry_rows_, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, objects, attempt, intake, dry_rows_, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, objects, attempt, intake, dry_rows_, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, objects, attempt, intake, dry_rows_, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
