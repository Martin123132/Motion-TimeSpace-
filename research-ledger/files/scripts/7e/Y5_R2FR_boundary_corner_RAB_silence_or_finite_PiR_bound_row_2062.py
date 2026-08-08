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


DOC = ROOT / "2062-Y5-R2FR-boundary-corner-RAB-silence-or-finite-PiR-bound-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2062_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2062-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2062*",
            "*Y5_R2FR_boundary_corner_RAB_silence_or_finite_PiR_bound_row_2062*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2062_00_2061_doc",
            ROOT / "2061-Y5-R2FR-PiR-boundary-current-zero-theorem-or-CR-profile-first-row.md",
            ["NEXT2061_0_2062", "boundary/corner/worldtube `R_AB` silence", "bulk auxiliary status alone"],
            "2061 selects boundary/corner silence as the next dominant zero-theorem clause.",
        ),
        (
            "SRC2062_01_2061_next",
            OUT / "P8_Y5_PARENT_QLOC_2061_NEXT_TARGET.csv",
            ["NEXT2061_0_2062", "boundary functional grammar", "finite Pi_R^tot fallback"],
            "machine-readable 2062 handoff.",
        ),
        (
            "SRC2062_02_2061_clauses",
            OUT / "P8_Y5_PARENT_QLOC_2061_ZERO_THEOREM_CLAUSES.csv",
            ["ZC2061_1_boundary_corner", "UNSIGNED_DOMINANT_BLOCKER", "PROT1566_1_BR_boundary"],
            "zero-theorem clause ledger.",
        ),
        (
            "SRC2062_03_06_boundary",
            ROOT / "06-reciprocal-charge-source-neutrality.md",
            ["free source-boundary variation gives W R_AB'=0", "fixed source R_AB boundary", "Q_R neutrality is the missing source theorem"],
            "original free-versus-fixed boundary variation warning.",
        ),
        (
            "SRC2062_04_1265_protection",
            OUT / "P8_Y5_R10_1265_AUXILIARY_PROTECTION_AUDIT.csv",
            ["AP1265_3_boundary_silence", "Parent boundary/corner grammar contains no `B_R(R_AB)`", "UNSIGNED_BOUNDARY_PROTECTION"],
            "auxiliary protection audit naming the boundary/corner clause.",
        ),
        (
            "SRC2062_05_1265_risk",
            OUT / "P8_Y5_R10_1265_REGENERATION_RISK_LEDGER.csv",
            ["RR1265_1_boundary_operator", "boundary/corner `B_R(R_AB)` source", "UNSIGNED"],
            "boundary operator regeneration risk.",
        ),
        (
            "SRC2062_06_1562_boundary",
            OUT / "P8_Y5_PARENT_QLOC_1562_BOUNDARY_DEGREE_COUNT_GATE.csv",
            ["BD1562_0_no_QR", "UNSIGNED", "no boundary/corner variational class proves this"],
            "boundary degree/charge gate.",
        ),
        (
            "SRC2062_07_1566_protection",
            OUT / "P8_Y5_PARENT_QLOC_1566_PROTECTION_PROOF_AUDIT.csv",
            ["PROT1566_1_BR_boundary", "UNSIGNED_BOUNDARY_SILENCE", "bulk auxiliary status does not exclude corner/source-worldtube hair"],
            "latest boundary/source/readout protection audit.",
        ),
        (
            "SRC2062_08_1566_gate",
            OUT / "P8_Y5_PARENT_QLOC_1566_CLAIM_GATE.csv",
            ["GATE1566_1_BR", "B_R=Pi_Rn=0 boundary theorem", "boundary/corner no-hair is unsigned"],
            "claim gate for boundary no-hair.",
        ),
        (
            "SRC2062_09_1001_corner",
            ROOT / "1001-Y5-R10-Bref-radius-surface-term-theorem-or-Delta-ref-radial-profile-row.md",
            ["MISSING_CLOSED_BREF_AND_CORNER_CERTIFICATE", "Stokes/homology route is viable only conditionally", "corner certificates are absent"],
            "older surface/corner certificate blocker, useful for boundary grammar discipline.",
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


def boundary_grammar_rows() -> list[dict[str, object]]:
    data = [
        (
            "BGA2062_0_boundary_split",
            "boundary functional split",
            "B_total = B_GR[q,theta,top] + B_ref[q,theta,top] + B_corner[q,theta,top] + B_R[R_AB,Lambda_R]",
            "boundary silence requires B_R=constant or absent, not merely small",
            "ACCOUNTING_IDENTITY",
            "not a zero proof yet",
        ),
        (
            "BGA2062_1_natural_variation",
            "free natural R_AB variation",
            "delta R_AB|_Sigma is allowed inside the auxiliary variational class",
            "if B_R is absent then W_R n^mu partial_mu R_AB=0 and Q_R=0",
            "EXACT_IF_BOUNDARY_CLASS_PARENT_SIGNED",
            "best zero route",
        ),
        (
            "BGA2062_2_fixed_boundary_rejection",
            "fixed R_AB boundary condition",
            "delta R_AB|_Sigma=0",
            "removes the equation rather than proving Q_R=0; fixed nonzero data can encode reciprocal hair",
            "REJECT_AS_NO_HAIR_PROOF",
            "only acceptable if parent separately fixes R_AB=0/asymptotic GR and no source/corner term exists",
        ),
        (
            "BGA2062_3_corner_worldtube",
            "corner/worldtube term",
            "Pi_R^corner := delta B_corner/delta R_AB plus source-worldtube endpoint contributions",
            "must be zero by grammar or bounded as part of Pi_R^tot",
            "UNSIGNED_DOMINANT_BLOCKER",
            "current corpus has no parent corner certificate",
        ),
        (
            "BGA2062_4_orientation",
            "orientation/sign convention",
            "Q_R = W_R n^mu partial_mu R_AB = -Pi_R^tot",
            "zero theorem is sign-insensitive, but finite scoring needs normal direction, W_R, N_sphere, Z_R_infty",
            "UNSIGNED_FOR_FINITE_SCORING",
            "not enough for a claim",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, clause, statement, consequence, status, note in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "clause": clause,
                "statement": statement,
                "consequence": consequence,
                "status": status,
                "note": note,
                "parent_signed": False,
                "claim_allowed": False,
            }
        )
        return_row_status = row["status"]
        if return_row_status == "REJECT_AS_NO_HAIR_PROOF":
            row["parent_signed"] = False
        rows.append(row)
    return rows


def proof_attempt_rows() -> list[dict[str, object]]:
    data = [
        (
            "BSP2062_0_theorem_statement",
            "Boundary/corner R_AB silence theorem",
            "If the parent boundary/corner/worldtube grammar factors only through q(Phi), theta and topological data, and natural R_AB variation is allowed, then delta B_total/delta R_AB=0 and Pi_R^corner=0.",
            "delta B_R/delta R_AB + Pi_R^corner = 0",
            "THEOREM_EXACT_IF_PARENT_GRAMMAR_SIGNED",
            "this would close the dominant 2061 clause",
        ),
        (
            "BSP2062_1_current_evidence",
            "current proof state",
            "1265/1562/1566 all record the clause as unsigned; 1001 records missing corner certificate in a related surface theorem",
            "no parent-signed grammar exists in current corpus",
            "NOT_PARENT_SIGNED",
            "cannot promote Pi_R=0",
        ),
        (
            "BSP2062_2_countermodel",
            "legal countermodel if grammar is not signed",
            "B_R = integral_Sigma beta_R R_AB dSigma or a corner term beta_corner R_AB|_corner",
            "delta B_R/delta R_AB = beta_R or Pi_R^corner=beta_corner, so Q_R=-Pi_R^tot can be nonzero",
            "COUNTERMODEL_OPEN",
            "bulk auxiliary elimination does not remove this boundary source",
        ),
        (
            "BSP2062_3_verdict",
            "proof verdict",
            "the silence route is mathematically clean but remains conditional",
            "finite Pi_R^tot intake is mandatory until boundary/corner grammar is parent-owned",
            "CONDITIONAL_PROOF_ONLY",
            "no local GR/Newton or Cassini claim",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, target, proof_content, implication, status, note in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "target": target,
                "proof_content": proof_content,
                "implication": implication,
                "status": status,
                "note": note,
                "accepted_as_parent_proof": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def finite_pir_schema_rows() -> list[dict[str, object]]:
    data = [
        (
            "PIR2062_0_total",
            "Pi_R^tot",
            "Pi_R^matter + Pi_R^boundary + Pi_R^corner + Pi_R^readout",
            "boundary-current units",
            "each component zero theorem or finite numeric bound with source path/equation anchor",
            "MISSING_COMPONENT_ZERO_OR_BOUND",
        ),
        (
            "PIR2062_1_boundary",
            "Pi_R^boundary",
            "delta B_R/delta R_AB on the chosen worldtube surface",
            "boundary-current units",
            "parent boundary functional grammar or finite boundary coefficient beta_R",
            "MISSING_BOUNDARY_FUNCTIONAL_GRAMMAR_OR_COEFFICIENT",
        ),
        (
            "PIR2062_2_corner",
            "Pi_R^corner",
            "corner/endpoint contribution from radial/source-worldtube cuts",
            "boundary-current units",
            "corner certificate or finite corner coefficient beta_corner",
            "MISSING_CORNER_CERTIFICATE_OR_COEFFICIENT",
        ),
        (
            "PIR2062_3_orientation",
            "orientation/sign",
            "Q_R=-Pi_R^tot with declared normal, W_R convention and reference subtraction",
            "dimensionless sign/orientation metadata",
            "worldtube orientation, exterior side, reference subtraction and sign convention",
            "MISSING_ORIENTATION_CONVENTION",
        ),
        (
            "PIR2062_4_qR_conversion",
            "q_R^PPN",
            "Pi_R^tot/(N_sphere Z_R_infty r_s)",
            "dimensionless",
            "N_sphere, Z_R_infty, same-frame r_s, source mass calibration",
            "MISSING_NORMALIZATION_CHAIN",
        ),
        (
            "PIR2062_5_tail_guard",
            "Cassini guard",
            "|q_R^PPN| + B_tail_abs <= 6.70e-05",
            "dimensionless",
            "absolute tail/readout/gauge/source budget; no cancellation credit",
            "MISSING_ABSOLUTE_TAIL_BUDGET",
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


def dry_run_rows(
    grammar: list[dict[str, object]],
    proof: list[dict[str, object]],
    schema: list[dict[str, object]],
) -> list[dict[str, object]]:
    unsigned_grammar = [row for row in grammar if not bool(row["parent_signed"])]
    data = [
        (
            "RUN2062_0_natural_boundary_route",
            "natural boundary zero theorem",
            "CONDITIONAL_ROUTE_VALID",
            "free variation plus no R_AB boundary/corner functional would imply Q_R=0",
            False,
        ),
        (
            "RUN2062_1_fixed_boundary_route",
            "fixed R_AB boundary condition",
            "REJECTED_AS_NO_HAIR_PROOF",
            "fixed boundary data removes the variation equation and can encode reciprocal hair",
            False,
        ),
        (
            "RUN2062_2_current_parent_status",
            "current parent proof state",
            "BOUNDARY_SILENCE_NOT_PARENT_SIGNED",
            f"unsigned_boundary_grammar_count={len(unsigned_grammar)}; proof_rows={len(proof)}",
            False,
        ),
        (
            "RUN2062_3_finite_schema",
            "finite Pi_R^tot fallback schema",
            "SOURCE_READY_SCHEMA_WRITTEN_NOT_SCORABLE",
            f"schema_rows={len(schema)}; no numeric/theorem-zero component rows supplied",
            False,
        ),
        (
            "RUN2062_VERDICT",
            "boundary/corner silence or finite Pi_R row",
            "CONDITIONAL_SILENCE_FINITE_PIR_ROW_REQUIRED",
            "proof remains conditional; finite Pi_R^tot component schema is installed and unscored",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for run_id, target, verdict, reason, accepted_for_scoring in data:
        row = base_row()
        row.update(
            {
                "run_id": run_id,
                "target": target,
                "verdict": verdict,
                "reason": reason,
                "unsigned_boundary_grammar_count": len(unsigned_grammar),
                "accepted_for_scoring": accepted_for_scoring,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2062_0_boundary_silence", "boundary/corner R_AB silence parent theorem", "FAIL_BLOCKED", "boundary grammar theorem is conditional, not parent-signed"),
        ("GATE2062_1_fixed_boundary", "fixed R_AB boundary as proof", "FAIL_REJECTED", "fixed data can hide hair and is not a no-charge theorem"),
        ("GATE2062_2_finite_PiR", "finite Pi_R^tot scoring", "FAIL_BLOCKED", "component bounds/zero theorems and normalization chain are missing"),
        ("GATE2062_3_Cassini", "Cassini/local PPN pass", "FAIL_BLOCKED", "no Pi_R zero theorem and no finite q_R prediction"),
        ("GATE2062_4_local_GR", "derived local GR/Newton claim", "FAIL_BLOCKED", "boundary/corner silence remains unsigned"),
        ("GATE2062_5_formalization", "formalization-workbench edit allowed", "PASS_NO_EDIT", "no formalization-workbench edit is made"),
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
            "DEC2062_0_proof_shape",
            "NATURAL_BOUNDARY_ROUTE_IS_THE_RIGHT_ZERO_PROOF",
            "Free R_AB variation plus no R_AB boundary/corner functional gives Q_R=0 without smuggling in closure.",
        ),
        (
            "DEC2062_1_reject_fixed",
            "FIXED_RAB_BOUNDARY_IS_NOT_A_PROOF",
            "Dirichlet/fixed data suppresses the boundary equation; it cannot be used as no-hair unless the fixed value is parent-derived as zero.",
        ),
        (
            "DEC2062_2_current_status",
            "BOUNDARY_CORNER_SILENCE_REMAINS_CONDITIONAL",
            "The corpus has no parent-signed boundary object-exhaustion/corner certificate.",
        ),
        (
            "DEC2062_3_next",
            "BOUNDARY_OBJECT_EXHAUSTION_OR_COMPONENT_BOUND",
            "Next attack should try a parent boundary object-exhaustion theorem; if it fails, fill finite Pi_R^boundary/Pi_R^corner component rows.",
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
            "target_id": "NEXT2062_0_2063",
            "target_doc": "2063-Y5-R2FR-boundary-object-exhaustion-or-PiR-component-bound-intake.md",
            "objective": "try to prove parent boundary object-exhaustion excludes B_R(R_AB) and R_AB corner terms; if it fails, create finite Pi_R^boundary and Pi_R^corner component-bound intake rows",
            "must_include": "allowed boundary objects; GHY/reference/topological split; corner functional grammar; worldtube endpoint terms; free variation class; finite component schema; no-cancellation guard",
            "excluded": "fixed R_AB boundary as no-hair proof; closure as proof; Cassini scoring; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    grammar: list[dict[str, object]],
    proof: list[dict[str, object]],
    schema: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2062_0_source_weight_boundary_silence",
            SOURCE_WEIGHT_DOCS / "AFRAME_BOUNDARY_CORNER_RAB_SILENCE_2062_CONDITIONAL_NONCLAIM.csv",
            grammar + proof,
        ),
        (
            "COPY2062_1_source_weight_finite_pir_schema",
            SOURCE_WEIGHT_DOCS / "AFRAME_FINITE_PIR_TOT_2062_SOURCE_ROW_SCHEMA_NONCLAIM.csv",
            schema,
        ),
        (
            "COPY2062_2_wep_dry_run",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2062_BOUNDARY_SILENCE_DRY_RUN_NONCLAIM.csv",
            dry_rows_,
        ),
        (
            "COPY2062_3_queue_next",
            QUEUE / "JR2062_BOUNDARY_OBJECT_EXHAUSTION_OR_PIR_COMPONENT_ROW_NEXT_NONCLAIM.csv",
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
    grammar: list[dict[str, object]],
    proof: list[dict[str, object]],
    schema: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    grammar_ok = (
        any(row["row_id"] == "BGA2062_1_natural_variation" for row in grammar)
        and any(row["row_id"] == "BGA2062_2_fixed_boundary_rejection" for row in grammar)
        and all(not bool(row["parent_signed"]) for row in grammar)
    )
    proof_verdict = next(row for row in proof if row["row_id"] == "BSP2062_3_verdict")
    proof_ok = proof_verdict["status"] == "CONDITIONAL_PROOF_ONLY" and all(not bool(row["accepted_as_parent_proof"]) for row in proof)
    schema_ok = len(schema) >= 6 and all(bool(row["source_ready_schema"]) and not bool(row["ready_for_scoring"]) for row in schema)
    dry_verdict = next(row for row in dry_rows_ if row["run_id"] == "RUN2062_VERDICT")
    dry_ok = dry_verdict["verdict"] == "CONDITIONAL_SILENCE_FINITE_PIR_ROW_REQUIRED"
    gates_ok = all(row["claim_allowed"] is False for row in gates) and all(row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2062_0_2063"
    no_claim = all(not bool(row.get("claim_allowed", False)) for group in [sources, grammar, proof, schema, dry_rows_, gates, next_rows_] for row in group)
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2062_00_local_sources_exist", source_ok, "all cited source paths and needles exist"))
    checks.append(("VAL2062_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2062_02_boundary_grammar", grammar_ok, "natural/free variation route and fixed-boundary rejection are explicit"))
    checks.append(("VAL2062_03_proof_verdict", proof_ok, "boundary silence proof remains conditional and not parent-accepted"))
    checks.append(("VAL2062_04_finite_schema", schema_ok, "finite Pi_R^tot component schema is source-ready but unscored"))
    checks.append(("VAL2062_05_dry_verdict", dry_ok, "dry run selects conditional silence plus finite Pi_R row"))
    checks.append(("VAL2062_06_claim_gates_blocked", gates_ok, "all claim gates remain blocked/nonclaim"))
    checks.append(("VAL2062_07_next_selected", next_ok, "2063 boundary object-exhaustion target selected"))
    checks.append(("VAL2062_08_no_claim_flags", no_claim, "no generated row allows a claim"))
    checks.append(("VAL2062_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2062_10_no_formalization_artifacts", not formalization_has_2062_artifacts(), "no 2062 artifacts were written under formalization-workbench"))
    checks.append(("VAL2062_11_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2062_OVERALL", overall, "2062 tests boundary/corner R_AB silence and installs finite Pi_R^tot fallback without claims"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    grammar: list[dict[str, object]],
    proof: list[dict[str, object]],
    schema: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2062 Y5 R2FR Boundary/Corner R_AB Silence Or Finite Pi_R Bound Row",
        "",
        "## Current Verdict",
        "",
        "2062 proves the shape of the boundary/corner zero route, but not the route itself. The valid theorem is: with free natural `R_AB` variation and a parent boundary/corner/worldtube grammar containing no `R_AB` functional, `delta B_R/delta R_AB + Pi_R^corner = 0`, so the boundary part of `Pi_R^tot` vanishes.",
        "",
        "The route is not parent-signed in the current corpus. Fixed `R_AB` boundary data is explicitly rejected as a no-hair proof because it removes the boundary equation and can hide reciprocal hair. Bulk auxiliary elimination is also insufficient because a boundary/corner functional can source `Q_R` even when the bulk has no propagating `R_AB` mode.",
        "",
        "The finite fallback is now source-ready but unscored: decompose `Pi_R^tot` into matter, boundary, corner, and readout components, then convert only after `N_sphere`, `Z_R_infty`, same-frame `r_s`, orientation, and absolute tails are supplied.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, clock, orbital, or finite-residual claim is allowed. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Boundary Functional Grammar",
        md_table(grammar, ["row_id", "clause", "statement", "consequence", "status", "note", "parent_signed", "claim_allowed"]),
        "## Silence Proof Attempt",
        md_table(proof, ["row_id", "target", "proof_content", "implication", "status", "note", "accepted_as_parent_proof", "claim_allowed"]),
        "## Finite Pi_R^tot Bound Row Schema",
        md_table(schema, ["row_id", "quantity", "formula", "units", "required_input", "blocker", "source_ready_schema", "ready_for_scoring", "claim_allowed"]),
        "## Dry Run",
        md_table(dry_rows_, ["run_id", "target", "verdict", "reason", "unsigned_boundary_grammar_count", "accepted_for_scoring", "claim_allowed"]),
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
    grammar = boundary_grammar_rows()
    proof = proof_attempt_rows()
    schema = finite_pir_schema_rows()
    dry_rows_ = dry_run_rows(grammar, proof, schema)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2062_SOURCE_REGISTER.csv",
        "grammar": OUT / "P8_Y5_PARENT_QLOC_2062_BOUNDARY_FUNCTIONAL_GRAMMAR.csv",
        "proof": OUT / "P8_Y5_PARENT_QLOC_2062_BOUNDARY_SILENCE_PROOF_ATTEMPT.csv",
        "schema": OUT / "P8_Y5_PARENT_QLOC_2062_FINITE_PIR_TOT_BOUND_ROW_SCHEMA.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2062_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2062_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2062_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2062_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2062_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2062_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["grammar"], grammar)
    write_csv(paths["proof"], proof)
    write_csv(paths["schema"], schema)
    write_csv(paths["dry"], dry_rows_)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(grammar, proof, schema, dry_rows_, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, grammar, proof, schema, dry_rows_, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, grammar, proof, schema, dry_rows_, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, grammar, proof, schema, dry_rows_, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
