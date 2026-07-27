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


DOC = ROOT / "2064-Y5-R2FR-corner-free-worldtube-certificate-or-PiR-corner-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2064_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2064-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2064*",
            "*Y5_R2FR_corner_free_worldtube_certificate_or_PiR_corner_bound_2064*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2064_00_2063_doc",
            ROOT / "2063-Y5-R2FR-boundary-object-exhaustion-or-PiR-component-bound-intake.md",
            ["NEXT2063_0_2064", "The finite fallback is now componentized", "countermodels remain simple"],
            "2063 handoff into corner-free worldtube certificate or Pi_R corner bound.",
        ),
        (
            "SRC2064_01_2063_next",
            OUT / "P8_Y5_PARENT_QLOC_2063_NEXT_TARGET.csv",
            ["NEXT2063_0_2064", "actual boundary surface class", "beta_corner finite bound"],
            "machine-readable 2064 target.",
        ),
        (
            "SRC2064_02_2063_intake",
            OUT / "P8_Y5_PARENT_QLOC_2063_FINITE_PIR_COMPONENT_INTAKE.csv",
            ["PCI2063_2_corner_zero_switch", "PCI2063_3_corner_bound", "MISSING_CORNER_CERTIFICATE"],
            "finite Pi_R corner zero/bound schema.",
        ),
        (
            "SRC2064_03_2062_grammar",
            OUT / "P8_Y5_PARENT_QLOC_2062_BOUNDARY_FUNCTIONAL_GRAMMAR.csv",
            ["BGA2062_3_corner_worldtube", "Pi_R^corner", "UNSIGNED_DOMINANT_BLOCKER"],
            "corner/worldtube term remains unsigned.",
        ),
        (
            "SRC2064_04_1166_doc",
            ROOT / "1166-Y5-R10-JC-from-Q-parent-variation-or-local-corner-certificate.md",
            ["LC1166_0_boundary_of_boundary", "CONDITIONAL_MATH_ZERO_NOT_ARENA_CERTIFIED", "LC1166_1_regulator_joints"],
            "conditional boundary-of-boundary corner zero and regulator-joint blocker.",
        ),
        (
            "SRC2064_05_1165_corner_csv",
            OUT / "P8_Y5_R10_1165_CCORNER_DSF_EPSILON_CERTIFICATE_ROWS.csv",
            ["CCZ1165_0_surface_without_corners", "MISSING_LOCAL_SURFACE_CERTIFICATE", "CCZ1165_6_finite_bound"],
            "corner-free/fallback certificate rows.",
        ),
        (
            "SRC2064_06_1020_doc",
            ROOT / "1020-Y5-R10-boundary-cohomology-domain-certificate-or-source-pack-first-row.md",
            ["BDC1020_0_surface_manifold", "partial S_edge = empty", "Stokes zero can hide corner charge"],
            "boundary domain/corner certificate precedent.",
        ),
        (
            "SRC2064_07_1001_doc",
            ROOT / "1001-Y5-R10-Bref-radius-surface-term-theorem-or-Delta-ref-radial-profile-row.md",
            ["MISSING_CLOSED_BREF_AND_CORNER_CERTIFICATE", "corner certificates are absent", "zero-by-boundary-silence and zero-by-fixed-radius are rejected"],
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


def corner_certificate_rows() -> list[dict[str, object]]:
    data = [
        (
            "CFC2064_0_math_boundary_of_boundary",
            "pure topology theorem",
            "If S=partial D is a smooth closed boundary of a smooth local/source domain D, then partial S=partial(partial D)=empty.",
            "pure Stokes corner contribution is zero",
            "EXACT_IF_ACTUAL_SURFACE_CERTIFIED",
            "mathematics is fine; arena certificate is missing",
        ),
        (
            "CFC2064_1_actual_surface_class",
            "actual boundary surface class",
            "the local/source readout surface must be identified as the same smooth closed S=partialD used by action, readout, source and finite bound rows",
            "without this, corner-free math does not attach to the physical row",
            "MISSING_ACTUAL_BOUNDARY_SURFACE_CLASS",
            "dominant blocker",
        ),
        (
            "CFC2064_2_regulator_joints",
            "regulator/cutoff/excision joints",
            "annuli, excised source interiors, matched patches, finite cutoffs, or numerical/readout regulators introduce joints C_i",
            "each joint must be absent, R_AB-silent, or finite-bounded",
            "MISSING_REGULATOR_JOINT_LEDGER",
            "cannot assume smoothness",
        ),
        (
            "CFC2064_3_source_worldtube_endpoints",
            "source-worldtube endpoints",
            "finite source worldtubes may have caps/endpoints where corner terms live",
            "endpoint R_AB dependence contributes to Pi_R^corner unless excluded",
            "MISSING_SOURCE_WORLDTUBE_ENDPOINT_LEDGER",
            "local compact-source route still needs it",
        ),
        (
            "CFC2064_4_RAB_silent_corner_grammar",
            "R_AB-silent corner grammar",
            "if corners exist, their allowed functionals must be q/theta/top/matter-descended only",
            "then beta_corner=0 for those corners",
            "MISSING_RAB_SILENT_CORNER_GRAMMAR",
            "inherits 2063 object-exhaustion gap",
        ),
        (
            "CFC2064_5_verdict",
            "corner-free certificate verdict",
            "partial partial D=0 is a conditional theorem, not an arena-certified local-Pi_R result",
            "Pi_R^corner remains zero-switch or finite-bound input",
            "CONDITIONAL_MATH_ZERO_NOT_ARENA_CERTIFIED",
            "finite beta_corner schema required",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, target, certificate_statement, implication, status, note in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "target": target,
                "certificate_statement": certificate_statement,
                "implication": implication,
                "status": status,
                "note": note,
                "accepted_as_parent_certificate": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def finite_corner_bound_rows() -> list[dict[str, object]]:
    data = [
        (
            "PCB2064_0_corner_zero_switch",
            "Pi_R^corner_zero",
            "true only if actual_surface_class=smooth_closed_partialD and regulator_joint_count=0, or every listed joint is R_AB-silent",
            "boolean theorem gate",
            "actual surface certificate plus joint ledger",
            "MISSING_ACTUAL_SURFACE_AND_JOINT_CERTIFICATE",
        ),
        (
            "PCB2064_1_joint_ledger",
            "corner/joint ledger",
            "list every active C_i from regulators, cutoffs, caps, patch joins, source-worldtube endpoints",
            "ledger metadata",
            "corner_id; surface_id; role; active; source path; equation anchor",
            "MISSING_CORNER_JOINT_LEDGER",
        ),
        (
            "PCB2064_2_beta_corner",
            "beta_corner_i",
            "delta B_corner_i/delta R_AB at each active C_i",
            "boundary-current units",
            "numeric bound/value or theorem-zero for each active corner coefficient",
            "MISSING_BETA_CORNER_VALUES",
        ),
        (
            "PCB2064_3_component_abs_sum",
            "Pi_R^corner_abs",
            "sum_i |beta_corner_i| * measure_or_weight_i",
            "boundary-current units",
            "nonnegative measure/weight convention and no-cancellation sum",
            "MISSING_CORNER_MEASURES_OR_WEIGHTS",
        ),
        (
            "PCB2064_4_join_PiRtot",
            "Pi_R^tot_abs join",
            "|Pi_R^matter| + |Pi_R^boundary| + |Pi_R^corner| + |Pi_R^readout|",
            "boundary-current units",
            "component absolute rows; no sign cancellation",
            "MISSING_COMPONENT_ABSOLUTE_SUM",
        ),
        (
            "PCB2064_5_qR_guard",
            "q_R^PPN guard",
            "|Pi_R^tot/(N_sphere Z_R_infty r_s)| + B_tail_abs <= 6.70e-05",
            "dimensionless",
            "normalization chain, same-frame r_s, orientation, absolute tails",
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


def dry_run_rows(certificates: list[dict[str, object]], bounds: list[dict[str, object]]) -> list[dict[str, object]]:
    verdict = next(row for row in certificates if row["row_id"] == "CFC2064_5_verdict")
    data = [
        (
            "RUN2064_0_boundary_of_boundary",
            "partial partial D corner theorem",
            "CONDITIONAL_MATH_ZERO_AVAILABLE",
            "works only after actual smooth closed boundary surface is certified",
            False,
        ),
        (
            "RUN2064_1_actual_arena",
            "actual local/source worldtube certificate",
            "REFUSED_ARENA_CERTIFICATE_MISSING",
            str(verdict["status"]),
            False,
        ),
        (
            "RUN2064_2_finite_corner",
            "finite Pi_R^corner bound row",
            "SOURCE_READY_SCHEMA_WRITTEN_NOT_SCORABLE",
            f"bound_rows={len(bounds)}; beta_corner values and joint ledger missing",
            False,
        ),
        (
            "RUN2064_VERDICT",
            "corner-free worldtube or Pi_R corner bound",
            "CORNER_ZERO_CONDITIONAL_PIR_CORNER_BOUND_REQUIRED",
            "no corner zero claim; next step must construct actual surface/joint ledger or source beta_corner",
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
        ("GATE2064_0_corner_zero", "Pi_R^corner=0 theorem", "FAIL_BLOCKED", "boundary-of-boundary math is not attached to actual arena surface"),
        ("GATE2064_1_joint_ledger", "actual regulator/cutoff/source endpoint ledger", "FAIL_BLOCKED", "active corners/joints are not enumerated"),
        ("GATE2064_2_finite_corner_bound", "finite Pi_R^corner bound scores", "FAIL_BLOCKED", "beta_corner values/bounds and measures are missing"),
        ("GATE2064_3_PiRtot", "Pi_R^tot join scores", "FAIL_BLOCKED", "corner plus other components and normalization chain are missing"),
        ("GATE2064_4_Cassini", "Cassini/local PPN pass", "FAIL_BLOCKED", "no q_R prediction or theorem-zero"),
        ("GATE2064_5_local_GR", "derived local GR/Newton claim", "FAIL_BLOCKED", "corner route remains conditional"),
        ("GATE2064_6_formalization", "formalization-workbench edit allowed", "PASS_NO_EDIT", "no formalization-workbench edit is made"),
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
            "DEC2064_0_math_result",
            "BOUNDARY_OF_BOUNDARY_THEOREM_IS_VALID",
            "For a smooth closed S=partialD, pure Stokes corner charge vanishes.",
        ),
        (
            "DEC2064_1_current_status",
            "ACTUAL_ARENA_CERTIFICATE_MISSING",
            "The current corpus does not prove local/readout/source surfaces have no regulator/cutoff/source-worldtube joints.",
        ),
        (
            "DEC2064_2_no_shortcut",
            "DO_NOT_ASSUME_SMOOTH_CORNERS",
            "Assuming a smooth surface without the arena certificate would be another closure axiom.",
        ),
        (
            "DEC2064_3_next",
            "SURFACE_CLASS_OR_JOINT_LEDGER_FIRST",
            "Next step should build the actual worldtube surface-class certificate; failing that, create the first beta_corner finite row.",
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
            "target_id": "NEXT2064_0_2065",
            "target_doc": "2065-Y5-R2FR-actual-worldtube-surface-class-or-regulator-joint-ledger.md",
            "objective": "construct the actual local/source worldtube surface class used by the PPN/local branch; prove it is a smooth closed partialD or enumerate regulator/cutoff/source endpoint joints for finite beta_corner bounds",
            "must_include": "surface_id; domain D; S=partialD certificate; excision/cutoff/regulator ledger; source-worldtube caps; active corner list; beta_corner placeholder rows; no-cancellation Pi_Rtot join",
            "excluded": "assuming smoothness; fixed R_AB boundary as proof; closure as proof; Cassini scoring; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    certificates: list[dict[str, object]],
    bounds: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2064_0_source_weight_corner_certificate",
            SOURCE_WEIGHT_DOCS / "AFRAME_CORNER_FREE_WORLDTUBE_2064_CONDITIONAL_NONCLAIM.csv",
            certificates,
        ),
        (
            "COPY2064_1_source_weight_corner_bound",
            SOURCE_WEIGHT_DOCS / "AFRAME_PIR_CORNER_BOUND_2064_SOURCE_ROW_SCHEMA_NONCLAIM.csv",
            bounds,
        ),
        (
            "COPY2064_2_wep_dry_run",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2064_CORNER_DRY_RUN_NONCLAIM.csv",
            dry_rows_,
        ),
        (
            "COPY2064_3_queue_next",
            QUEUE / "JR2064_ACTUAL_WORLDTUBE_SURFACE_OR_JOINT_LEDGER_NEXT_NONCLAIM.csv",
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
    certificates: list[dict[str, object]],
    bounds: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    cert_verdict = next(row for row in certificates if row["row_id"] == "CFC2064_5_verdict")
    cert_ok = (
        any(row["row_id"] == "CFC2064_0_math_boundary_of_boundary" for row in certificates)
        and cert_verdict["status"] == "CONDITIONAL_MATH_ZERO_NOT_ARENA_CERTIFIED"
        and all(not bool(row["accepted_as_parent_certificate"]) for row in certificates)
    )
    bound_ok = len(bounds) >= 6 and all(bool(row["source_ready_schema"]) and not bool(row["ready_for_scoring"]) for row in bounds)
    dry_verdict = next(row for row in dry_rows_ if row["run_id"] == "RUN2064_VERDICT")
    dry_ok = dry_verdict["verdict"] == "CORNER_ZERO_CONDITIONAL_PIR_CORNER_BOUND_REQUIRED"
    gates_ok = all(row["claim_allowed"] is False for row in gates) and all(row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2064_0_2065"
    no_claim = all(not bool(row.get("claim_allowed", False)) for group in [sources, certificates, bounds, dry_rows_, gates, next_rows_] for row in group)
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2064_00_local_sources_exist", source_ok, "all cited source paths and needles exist"))
    checks.append(("VAL2064_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2064_02_corner_certificate", cert_ok, "boundary-of-boundary theorem is present but not arena-certified"))
    checks.append(("VAL2064_03_finite_corner_bound", bound_ok, "finite Pi_R^corner bound rows are source-ready but unscored"))
    checks.append(("VAL2064_04_dry_verdict", dry_ok, "dry run refuses corner-zero claim and requires finite corner bound or surface certificate"))
    checks.append(("VAL2064_05_claim_gates_blocked", gates_ok, "all claim gates remain blocked/nonclaim"))
    checks.append(("VAL2064_06_next_selected", next_ok, "2065 actual worldtube surface/joint target selected"))
    checks.append(("VAL2064_07_no_claim_flags", no_claim, "no generated row allows a claim"))
    checks.append(("VAL2064_08_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2064_09_no_formalization_artifacts", not formalization_has_2064_artifacts(), "no 2064 artifacts were written under formalization-workbench"))
    checks.append(("VAL2064_10_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2064_OVERALL", overall, "2064 tests corner-free worldtube certificate and stages Pi_R^corner bound without claims"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    certificates: list[dict[str, object]],
    bounds: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2064 Y5 R2FR Corner-Free Worldtube Certificate Or Pi_R Corner Bound",
        "",
        "## Current Verdict",
        "",
        "2064 proves the useful mathematical sub-lemma but does not certify the physical arena. If the actual local/source boundary is a smooth closed `S=partial D`, then `partial S=partial(partial D)=empty` and the pure corner term vanishes.",
        "",
        "The present corpus does not prove that the PPN/local readout surface has that form. Excision surfaces, finite cutoffs, regulator seams, matched patches, and source-worldtube caps can all create active joints. So `Pi_R^corner=0` remains conditional, not a local-GR result.",
        "",
        "The finite fallback is now sharpened to a joint ledger and `beta_corner` row: enumerate active corners, zero or bound each coefficient, sum by absolute value, then join into `Pi_R^tot` without cancellation.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, clock, orbital, corner-zero, or finite-residual claim is allowed. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Corner-Free Certificate Attempt",
        md_table(certificates, ["row_id", "target", "certificate_statement", "implication", "status", "note", "accepted_as_parent_certificate", "claim_allowed"]),
        "## Finite Pi_R^corner Bound Schema",
        md_table(bounds, ["row_id", "quantity", "formula", "units", "required_input", "blocker", "source_ready_schema", "ready_for_scoring", "claim_allowed"]),
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
    certificates = corner_certificate_rows()
    bounds = finite_corner_bound_rows()
    dry_rows_ = dry_run_rows(certificates, bounds)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2064_SOURCE_REGISTER.csv",
        "certificates": OUT / "P8_Y5_PARENT_QLOC_2064_CORNER_FREE_CERTIFICATE_ATTEMPT.csv",
        "bounds": OUT / "P8_Y5_PARENT_QLOC_2064_FINITE_PIR_CORNER_BOUND_SCHEMA.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2064_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2064_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2064_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2064_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2064_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2064_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["certificates"], certificates)
    write_csv(paths["bounds"], bounds)
    write_csv(paths["dry"], dry_rows_)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(certificates, bounds, dry_rows_, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, certificates, bounds, dry_rows_, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, certificates, bounds, dry_rows_, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, certificates, bounds, dry_rows_, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
