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


DOC = ROOT / "2061-Y5-R2FR-PiR-boundary-current-zero-theorem-or-CR-profile-first-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2061_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2061-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2061*",
            "*Y5_R2FR_PiR_boundary_current_zero_theorem_or_CR_profile_first_row_2061*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2061_00_2060_doc",
            ROOT / "2060-Y5-R2FR-first-finite-qR-PiR-source-row-or-parent-owner-reopen.md",
            ["NEXT2060_0_2061", "Pi_R=0/Q_R=0", "No local-GR/Newton"],
            "2060 handoff into Pi_R/Q_R boundary-current zero theorem attempt.",
        ),
        (
            "SRC2061_01_2060_next",
            OUT / "P8_Y5_PARENT_QLOC_2060_NEXT_TARGET.csv",
            ["NEXT2060_0_2061", "boundary variation", "worldtube orientation"],
            "machine-readable 2061 target.",
        ),
        (
            "SRC2061_02_2060_schema",
            OUT / "P8_Y5_PARENT_QLOC_2060_QR_PIR_SOURCE_ROW_SCHEMA.csv",
            ["SRCROW2060_1_PiR_chain", "MISSING_PIR_VALUE_OR_ZERO_THEOREM", "MISSING_SAME_FRAME_RS"],
            "Pi_R chain and first finite source-row contract.",
        ),
        (
            "SRC2061_03_06_boundary",
            ROOT / "06-reciprocal-charge-source-neutrality.md",
            ["delta S_boundary = [W R_AB' + Pi_R]", "Q_R = -Pi_R", "Pi_R = 0 -> Q_R = 0"],
            "original reciprocal boundary-current relation.",
        ),
        (
            "SRC2061_04_1268_candidate",
            OUT / "P8_Y5_R10_1268_COMPATIBILITY_ACTION_CANDIDATE.csv",
            ["CAC1268_4_boundary_readout", "delta B_R/delta R_AB=0", "REQUIRED_BUT_UNSIGNED"],
            "second-class compatibility action and unsigned boundary/readout silence.",
        ),
        (
            "SRC2061_05_1268_variation",
            OUT / "P8_Y5_R10_1268_VARIATIONAL_ELIMINATION_AUDIT.csv",
            ["VAR1268_1_E_R", "Lambda_R + J_R", "PASS_ONLY_IF_SOURCES_ZERO"],
            "E_R variation shows which source terms must vanish.",
        ),
        (
            "SRC2061_06_1565_elim",
            OUT / "P8_Y5_PARENT_QLOC_1565_SECOND_CLASS_ELIMINATION_CONDITIONS.csv",
            ["ELIM1565_1_E_R", "delta B_R/delta R_AB", "PASS_ONLY_IF_SOURCES_ZERO"],
            "source-free algebraic elimination condition.",
        ),
        (
            "SRC2061_07_1565_theta",
            OUT / "P8_Y5_PARENT_QLOC_1565_THETA_OMEGA_FILL.csv",
            ["TO1565_2_boundary_momentum", "Pi_R^n = 0", "EXACT_IF_NO_BOUNDARY_RAB_FUNCTIONAL"],
            "conditional boundary momentum zero inside algebraic block.",
        ),
        (
            "SRC2061_08_1566_protection",
            OUT / "P8_Y5_PARENT_QLOC_1566_PROTECTION_PROOF_AUDIT.csv",
            ["PROT1566_1_BR_boundary", "UNSIGNED_BOUNDARY_SILENCE", "finite B_R/Pi_Rn bound"],
            "source/boundary/readout protection audit.",
        ),
        (
            "SRC2061_09_1566_gate",
            OUT / "P8_Y5_PARENT_QLOC_1566_CLAIM_GATE.csv",
            ["GATE1566_1_BR", "B_R=Pi_Rn=0 boundary theorem", "BLOCKED_NO_CLAIM"],
            "claim gate proving boundary no-hair remains unsigned.",
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


def boundary_derivation_rows() -> list[dict[str, object]]:
    data = [
        (
            "DER2061_0_boundary_identity",
            "boundary variation",
            "delta S_boundary = [W_R n^mu partial_mu R_AB + Pi_R^tot] delta R_AB|_Sigma",
            "Pi_R^tot := delta B_R/delta R_AB + Pi_R^matter + Pi_R^readout + Pi_R^corner",
            "EXACT_ACCOUNTING_IDENTITY",
            "splits source/corner/readout terms instead of hiding them inside Pi_R",
        ),
        (
            "DER2061_1_charge_relation",
            "exterior conserved charge",
            "Q_R := W_R n^mu partial_mu R_AB on the exterior side",
            "stationarity with free delta R_AB gives Q_R = -Pi_R^tot",
            "EXACT_CONDITIONAL_ON_ORIENTATION",
            "orientation/sign convention must be fixed before numeric scoring",
        ),
        (
            "DER2061_2_zero_theorem",
            "Pi_R/Q_R zero theorem",
            "If Pi_R^matter=delta B_R/delta R_AB=Pi_R^readout=Pi_R^corner=0 and no legal derivative/counterterm regenerates R_AB hair, then Pi_R^tot=Q_R=0",
            "with asymptotic regularity this collapses the 1/r reciprocal hair and blocks q_R^PPN",
            "THEOREM_EXACT_IF_ALL_CLAUSES_PARENT_SIGNED",
            "not a current claim because clauses are unsigned",
        ),
        (
            "DER2061_3_failure_mode",
            "finite branch if any clause fails",
            "Q_R = -Pi_R^tot != 0 and C_R(r)=q_R^PPN r_s/r + tails remains the correct local residual row",
            "q_R^PPN = Pi_R^tot/(N_sphere Z_R_infty r_s) only after normalization and source mass close",
            "FINITE_PROFILE_REQUIRED_IF_UNSIGNED",
            "do not use closure or cancellation to pass Cassini",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_name, identity, consequence, status, note in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object": object_name,
                "identity_or_theorem": identity,
                "consequence": consequence,
                "status": status,
                "note": note,
                "accepted_as_parent_proof": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def zero_clause_rows() -> list[dict[str, object]]:
    data = [
        (
            "ZC2061_0_matter_descent",
            "Pi_R^matter=0",
            "S_matter factors through q(Phi), theta, top and carries no hidden R_AB marker",
            "UNSIGNED",
            "PROT1566_0_JR_matter remains unsigned",
        ),
        (
            "ZC2061_1_boundary_corner",
            "delta B_R/delta R_AB + Pi_R^corner=0",
            "boundary/corner/worldtube grammar contains no R_AB functional and no R_AB counterterm",
            "UNSIGNED_DOMINANT_BLOCKER",
            "PROT1566_1_BR_boundary and GATE1566_1_BR are blocked",
        ),
        (
            "ZC2061_2_readout_regen",
            "Pi_R^readout=0",
            "effective/readout map remains inside ParentGenerate[q,theta,top]",
            "UNSIGNED",
            "readout/EFT closure remains unsigned",
        ),
        (
            "ZC2061_3_operator",
            "no derivative/counterterm regeneration",
            "ParentGenerate excludes D R_AB, D Lambda_R, vertical metric, vertical connection and boundary derivative terms",
            "UNSIGNED",
            "operator-exclusion remains exact-conditional only",
        ),
        (
            "ZC2061_4_orientation",
            "Q_R=-Pi_R^tot sign and units",
            "worldtube normal, W_R convention, N_sphere and Z_R_infty are fixed in one frame",
            "UNSIGNED_FOR_SCORING",
            "normalization/sign not enough to prove zero but needed for finite fallback",
        ),
        (
            "ZC2061_5_asymptotic",
            "zero exterior integration constant",
            "regular/asymptotically GR branch with AB -> 1 and no independent reciprocal source",
            "CONDITIONAL",
            "becomes useful only after source terms vanish",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, zero_clause, required_statement, status, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "zero_clause": zero_clause,
                "required_statement": required_statement,
                "status": status,
                "blocker": blocker,
                "parent_signed": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def fallback_profile_rows() -> list[dict[str, object]]:
    data = [
        (
            "FB2061_0_total_PiR",
            "Pi_R^tot",
            "Pi_R^matter + delta B_R/delta R_AB + Pi_R^readout + Pi_R^corner",
            "boundary-current units",
            "finite Pi_R bound/value or theorem-zero for each component",
            "MISSING_COMPONENT_ZERO_OR_BOUND",
        ),
        (
            "FB2061_1_qR_conversion",
            "q_R^PPN",
            "Pi_R^tot/(N_sphere Z_R_infty r_s)",
            "dimensionless",
            "N_sphere, Z_R_infty, same-frame r_s, sign/orientation convention",
            "MISSING_NORMALIZATION_CHAIN",
        ),
        (
            "FB2061_2_CR_profile",
            "C_R(r)",
            "q_R^PPN r_s/r + delta_tail(r) + O(r_s^2/r^2)",
            "dimensionless profile",
            "profile source row and absolute tail budget",
            "MISSING_PROFILE_AND_TAIL_BUDGET",
        ),
        (
            "FB2061_3_Cassini_guard",
            "PPN gamma guard",
            "|q_R^PPN| + B_tail_abs <= 6.70e-05",
            "dimensionless",
            "no-cancellation absolute residual vector",
            "MISSING_ABSOLUTE_PRODUCT_GUARD",
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
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def dry_run_rows(clauses: list[dict[str, object]]) -> list[dict[str, object]]:
    unsigned = [row for row in clauses if not bool(row["parent_signed"])]
    data = [
        (
            "RUN2061_0_conditional_theorem",
            "Pi_R=0/Q_R=0 theorem",
            "CONDITIONAL_THEOREM_WRITTEN",
            "the logic closes if all zero clauses are parent-signed",
            False,
        ),
        (
            "RUN2061_1_current_parent_status",
            "current corpus proof status",
            "THEOREM_NOT_PARENT_SIGNED",
            f"unsigned_clause_count={len(unsigned)}",
            False,
        ),
        (
            "RUN2061_2_Cassini_status",
            "Cassini/local PPN status",
            "REFUSED_MISSING_PIR_ZERO_OR_FINITE_PROFILE",
            "no Pi_R zero theorem and no finite C_R/q_R profile row can score",
            False,
        ),
        (
            "RUN2061_VERDICT",
            "local GR/Newton reduction lane",
            "BOUNDARY_ZERO_THEOREM_CONDITIONAL_FINITE_BRANCH_STILL_OPEN",
            "dominant next blocker is boundary/corner R_AB silence or a finite Pi_R bound row",
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
                "unsigned_clause_count": len(unsigned),
                "accepted_for_scoring": accepted_for_scoring,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2061_0_PiR_zero", "Pi_R=0/Q_R=0 parent theorem", "FAIL_BLOCKED", "boundary/corner/matter/readout/operator clauses remain unsigned"),
        ("GATE2061_1_finite_profile", "finite C_R/q_R profile scoring", "FAIL_BLOCKED", "Pi_R^tot, normalization chain, same-frame r_s and tails remain missing"),
        ("GATE2061_2_Cassini", "Cassini/local PPN pass", "FAIL_BLOCKED", "no theorem-zero and no finite prediction"),
        ("GATE2061_3_local_GR", "derived local GR/Newton claim", "FAIL_BLOCKED", "conditional auxiliary route not parent-signed"),
        ("GATE2061_4_formalization", "formalization-workbench edit allowed", "PASS_NO_EDIT", "no formalization-workbench edit is made"),
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
            "DEC2061_0_progress",
            "CONDITIONAL_ZERO_THEOREM_EXACT",
            "The Pi_R/Q_R zero theorem is now a precise contract, not an axiom: kill matter, boundary/corner, readout, and operator regeneration terms.",
        ),
        (
            "DEC2061_1_not_claimed",
            "CURRENT_CORPUS_DOES_NOT_PROVE_ZERO",
            "Boundary/corner R_AB silence is the dominant unsigned clause; matter/readout/operator clauses also remain open.",
        ),
        (
            "DEC2061_2_best_next",
            "BOUNDARY_CORNER_SILENCE_FIRST",
            "This is narrower than attacking all local GR at once and has the highest chance of converting Pi_R=0 from conditional to derived.",
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
            "target_id": "NEXT2061_0_2062",
            "target_doc": "2062-Y5-R2FR-boundary-corner-RAB-silence-or-finite-PiR-bound-row.md",
            "objective": "try to prove boundary/corner/worldtube R_AB silence so delta B_R/delta R_AB + Pi_R^corner = 0; if it fails, write the finite Pi_R^tot bound-row intake schema",
            "must_include": "boundary functional grammar; corner/worldtube terms; free versus fixed R_AB variation; orientation/sign convention; finite Pi_R^tot fallback; no-cancellation guard",
            "excluded": "claiming Pi_R=0 from bulk auxiliary status alone; using closure as proof; scoring Cassini; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    derivation: list[dict[str, object]],
    clauses: list[dict[str, object]],
    fallback: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2061_0_source_weight_zero_contract",
            SOURCE_WEIGHT_DOCS / "AFRAME_PIR_BOUNDARY_ZERO_2061_CONDITIONAL_NONCLAIM.csv",
            derivation + clauses,
        ),
        (
            "COPY2061_1_wep_finite_profile_fallback",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2061_FINITE_PROFILE_FALLBACK_NONCLAIM.csv",
            fallback,
        ),
        (
            "COPY2061_2_wep_dry_run",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2061_DRY_RUN_NONCLAIM.csv",
            dry_rows_,
        ),
        (
            "COPY2061_3_queue_next",
            QUEUE / "JR2061_BOUNDARY_CORNER_SILENCE_OR_FINITE_PIR_ROW_NEXT_NONCLAIM.csv",
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
    derivation: list[dict[str, object]],
    clauses: list[dict[str, object]],
    fallback: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    derivation_ok = any(row["row_id"] == "DER2061_2_zero_theorem" for row in derivation) and all(
        not bool(row["accepted_as_parent_proof"]) for row in derivation
    )
    clauses_ok = len(clauses) >= 6 and all(not bool(row["parent_signed"]) for row in clauses)
    fallback_ok = len(fallback) >= 4 and all(not bool(row["ready_for_scoring"]) for row in fallback)
    verdict = next(row for row in dry_rows_ if row["run_id"] == "RUN2061_VERDICT")
    dry_ok = verdict["verdict"] == "BOUNDARY_ZERO_THEOREM_CONDITIONAL_FINITE_BRANCH_STILL_OPEN"
    gates_ok = all(row["claim_allowed"] is False for row in gates) and all(row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2061_0_2062"
    no_claim = all(not bool(row.get("claim_allowed", False)) for group in [sources, derivation, clauses, fallback, dry_rows_, gates, next_rows_] for row in group)
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2061_00_local_sources_exist", source_ok, "all cited source paths and needles exist"))
    checks.append(("VAL2061_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"))
    checks.append(("VAL2061_02_conditional_derivation", derivation_ok, "conditional Pi_R/Q_R zero theorem is written but not parent-accepted"))
    checks.append(("VAL2061_03_unsigned_clauses_visible", clauses_ok, "all zero-theorem clauses remain explicitly unsigned"))
    checks.append(("VAL2061_04_finite_fallback_blocked", fallback_ok, "finite C_R/q_R profile fallback remains unscored"))
    checks.append(("VAL2061_05_dry_verdict", dry_ok, "dry runner keeps theorem conditional and finite branch open"))
    checks.append(("VAL2061_06_claim_gates_blocked", gates_ok, "all claim gates remain blocked/nonclaim"))
    checks.append(("VAL2061_07_next_selected", next_ok, "2062 boundary/corner silence target selected"))
    checks.append(("VAL2061_08_no_claim_flags", no_claim, "no generated row allows a claim"))
    checks.append(("VAL2061_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2061_10_no_formalization_artifacts", not formalization_has_2061_artifacts(), "no 2061 artifacts were written under formalization-workbench"))
    checks.append(("VAL2061_11_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2061_OVERALL", overall, "2061 derives the exact conditional Pi_R/Q_R zero contract and blocks all local claims"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    derivation: list[dict[str, object]],
    clauses: list[dict[str, object]],
    fallback: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2061 Y5 R2FR Pi_R Boundary-Current Zero Theorem Or C_R Profile First Row",
        "",
        "## Current Verdict",
        "",
        "2061 gets a real derivation result, but not a claim. The exact conditional theorem is: if matter, boundary/corner, readout, and derivative-regeneration channels are all parent-silent, then `Pi_R^tot=0`, hence `Q_R=0`, hence the exterior reciprocal `1/r` hair is killed.",
        "",
        "The present corpus does not yet sign those clauses. The dominant blocker is boundary/corner/worldtube `R_AB` silence: bulk auxiliary status alone does not prove `delta B_R/delta R_AB + Pi_R^corner = 0`. Therefore the local branch still cannot claim derived GR/Newton or Cassini safety.",
        "",
        "The fallback is also now exact: if any zero clause fails, use `Pi_R^tot`, `N_sphere`, `Z_R_infty`, same-frame `r_s`, and an absolute tail budget to build `C_R(r)=q_R^PPN r_s/r + tails`, with no cancellation credit.",
        "",
        "No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Boundary-Current Derivation",
        md_table(derivation, ["row_id", "object", "identity_or_theorem", "consequence", "status", "note", "accepted_as_parent_proof", "claim_allowed"]),
        "## Zero-Theorem Clauses",
        md_table(clauses, ["row_id", "zero_clause", "required_statement", "status", "blocker", "parent_signed", "claim_allowed"]),
        "## Finite C_R/q_R Fallback",
        md_table(fallback, ["row_id", "quantity", "formula", "units", "required_input", "blocker", "ready_for_scoring", "claim_allowed"]),
        "## Dry Run",
        md_table(dry_rows_, ["run_id", "target", "verdict", "reason", "unsigned_clause_count", "accepted_for_scoring", "claim_allowed"]),
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
    derivation = boundary_derivation_rows()
    clauses = zero_clause_rows()
    fallback = fallback_profile_rows()
    dry_rows_ = dry_run_rows(clauses)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2061_SOURCE_REGISTER.csv",
        "derivation": OUT / "P8_Y5_PARENT_QLOC_2061_BOUNDARY_CURRENT_DERIVATION.csv",
        "clauses": OUT / "P8_Y5_PARENT_QLOC_2061_ZERO_THEOREM_CLAUSES.csv",
        "fallback": OUT / "P8_Y5_PARENT_QLOC_2061_FINITE_CR_QR_FALLBACK.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2061_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2061_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2061_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2061_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2061_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2061_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["derivation"], derivation)
    write_csv(paths["clauses"], clauses)
    write_csv(paths["fallback"], fallback)
    write_csv(paths["dry"], dry_rows_)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(derivation, clauses, fallback, dry_rows_, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, derivation, clauses, fallback, dry_rows_, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, derivation, clauses, fallback, dry_rows_, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, derivation, clauses, fallback, dry_rows_, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
