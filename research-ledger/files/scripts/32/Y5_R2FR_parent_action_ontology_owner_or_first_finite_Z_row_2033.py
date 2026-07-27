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


DOC = ROOT / "2033-Y5-R2FR-parent-action-ontology-owner-or-first-finite-Z-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def formalization_has_2033_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2033*owner*")) or any(FORMALIZATION.rglob("*2033*finite*Z*"))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2033_00_2032_handoff",
            ROOT / "2032-Y5-R2FR-primitive-operator-grammar-derivation-or-finite-Z-source-runner.md",
            ["NEXT2032_0_2033", "GRAM2032_7_verdict", "VAL2032_OVERALL"],
            "2032 selects the parent action ontology owner row or finite Z fallback.",
        ),
        (
            "SRC2033_01_2032_next",
            OUT / "P8_Y5_PARENT_QLOC_2032_NEXT_TARGET.csv",
            ["NEXT2032_0_2033"],
            "machine-readable 2033 target.",
        ),
        (
            "SRC2033_02_1009_parent_contract",
            ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            ["PCS1009_9_total_parent_contract", "DEC1009_0_contract_not_parent_action"],
            "earlier total-parent-current contract and explicit not-yet-parent-action verdict.",
        ),
        (
            "SRC2033_03_1248_lambdaR_ansatz",
            ROOT / "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check.md",
            ["ANS1248_0_fields", "DIR1248_2_preservation", "FAIL1248_0_origin", "VAL1248_13_overall"],
            "minimal lambda_R C_R ansatz and the exact reason it remains unsigned.",
        ),
        (
            "SRC2033_04_1267_auxiliary_route",
            ROOT / "1267-Y5-R10-first-class-RAB-parent-constraint-synthesis-or-finite-ZR-source-acquisition.md",
            ["SEL1267_1_second_class_auxiliary", "AP1265_0_auxiliary_signature", "DEC1267_1_best_derivation_route", "VAL1267_12_overall"],
            "refocuses hard R_AB=0 to second-class/algebraic auxiliary compatibility.",
        ),
        (
            "SRC2033_05_1868_candidate_grammar",
            ROOT / "source-intake" / "microscope" / "quarantine" / "1868" / "P8_Y5_PARENT_QLOC_1868_CANDIDATE_PARENT_GRAMMAR.csv",
            ["CPG1868_0_parent_primitives", "CPG1868_2_no_independent_RAB", "CPG1868_4_constraint_admission"],
            "candidate grammar for primitives, R_AB exclusion, and Lambda_R C_R admission.",
        ),
        (
            "SRC2033_06_721_parent_template",
            OUT / "P8_Y5_R10_721_PARENT_ZM_TEMPLATE.csv",
            ["PZT721_0_parent_action", "PZT721_1_field_list", "PZT721_2_kinetic_tensor"],
            "finite retained-field template that defines what source-backed Z/M entries would require.",
        ),
        (
            "SRC2033_07_721_blocker",
            OUT / "P8_Y5_R10_721_CLAIM_BLOCKER_LEDGER.csv",
            ["CB721_0_no_multifield_parent_action"],
            "blocks Z/M claims until a real parent action and field list exist.",
        ),
        (
            "SRC2033_08_10_observer",
            ROOT / "10-observer-map-symplectic-contract.md",
            ["R_AB = ln(T^2 S) = 2 ln(J_q).", "all matter sectors couple to the same observer coframe."],
            "observer/readout equation and universal coframe-coupling target.",
        ),
    ]
    rows = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def owner_certificate_rows() -> list[dict[str, object]]:
    data = [
        (
            "OWN2033_0_typed_parent_field_list",
            "Phi_parent=(T,S,e_pub,theta,connection/transport,matter,boundary/domain,auxiliaries)",
            "declares what can be varied and what cannot",
            "CANDIDATE_FROM_1009_1248_1868",
            "not one signed parent action",
        ),
        (
            "OWN2033_1_action_owner",
            "S_parent[Phi_parent]=integral L_core + L_aux + L_matter + L_boundary",
            "owns the Euler equations, stress tensor, theta/current, and operator admission",
            "NORMAL_FORM_WRITTEN_NOT_SOURCED",
            "L_core and boundary functional are still schematic",
        ),
        (
            "OWN2033_2_variation_owner",
            "delta S_parent=E_A delta Phi^A + d theta_MTS",
            "fixes the symplectic/current chain and stops ad hoc closures",
            "REQUIRED_OWNER_ROW",
            "theta_MTS is not extracted for the whole action",
        ),
        (
            "OWN2033_3_readout_status",
            "R_AB=ln(T^2 S)=2 ln(J_q) is a derived readout/compatibility scalar",
            "blocks treating R_AB as a primitive unless the action promotes it",
            "DERIVED_STATUS_CONFIRMED",
            "derived status alone does not ban projected primitive gradients",
        ),
        (
            "OWN2033_4_auxiliary_block",
            "Lambda_R C_R is admissible only as parent-owned auxiliary compatibility",
            "would eliminate R_AB without scalar hair if signed",
            "BEST_EXACT_ROUTE_CONDITIONAL",
            "origin, preservation, matter descent, and boundary silence are not signed",
        ),
        (
            "OWN2033_5_operator_policy",
            "D acts on primitives; raw D R_AB operators require promotion to finite branch",
            "separates exact-removal branch from finite scalar branch",
            "OPERATOR_POLICY_CONDITIONAL",
            "needs S_parent owner row to become a theorem",
        ),
        (
            "OWN2033_6_matter_boundary_owner",
            "S_matter and boundary terms descend through the same public coframe/readout",
            "would set J_R=0 and Q_R=0 in the auxiliary branch",
            "TARGET_CLAUSE_NOT_SIGNED",
            "universal matter descent and boundary no-charge remain missing",
        ),
        (
            "OWN2033_7_certificate_verdict",
            "the owner certificate is now exact as a contract but not activated as a theorem",
            "we know what one row must prove before local GR can be claimed",
            "OWNER_CONTRACT_READY_PARENT_SIGNATURE_MISSING",
            "must either fill OWN2033_1/2/4/6 or run finite Z acquisition",
        ),
    ]
    rows = []
    for row_id, clause, role, status, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "clause": clause,
                "role": role,
                "status": status,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def derivation_attempt_rows() -> list[dict[str, object]]:
    data = [
        (
            "DER2033_0_owner_normal_form",
            "S_parent = integral sqrt(-g_pub)[L_core(T,S,e,theta,conn) + Lambda_R ln(T^2 S) + L_matter(Psi,e_pub,theta) + L_boundary]",
            "This is the minimal object that would own the local branch without importing GR as the starting axiom.",
            "NORMAL_FORM_CONSTRUCTED_NONCLAIM",
            "L_core is not extracted from a parent manuscript/source row.",
        ),
        (
            "DER2033_1_delta_Lambda",
            "delta_Lambda S gives C_R=ln(T^2 S)=0.",
            "The desired reciprocal fixed point follows formally inside the normal form.",
            "FORMAL_PASS_WITHIN_NORMAL_FORM",
            "only valid if Lambda_R is parent-owned rather than inserted by closure.",
        ),
        (
            "DER2033_2_no_R_kinetic",
            "No independent K_R (nabla R_AB)^2 term is admitted in the exact branch.",
            "This would set Z_R=0 by object language, not tuning.",
            "PASS_IF_OWNER_POLICY_SIGNED",
            "operator policy is conditional until S_parent owns the grammar.",
        ),
        (
            "DER2033_3_elimination",
            "R_AB/Lambda_R form an auxiliary compatibility sector; after solving algebraic equations no R_AB propagator, theta_R, or Pi_R remains.",
            "This is the non-circular local-GR route.",
            "PROMISING_CONDITIONAL_THEOREM",
            "preservation/bracket and determinant/readout-remnant checks still missing.",
        ),
        (
            "DER2033_4_matter_descent",
            "Matter couples to e_pub/theta only, not to a hidden reciprocal frame or direct R_AB source.",
            "Would kill J_R and composition-dependent fifth-force leakage.",
            "TARGET_NOT_DERIVED",
            "universal coframe descent is stated as target, not proved from parent action.",
        ),
        (
            "DER2033_5_boundary_silence",
            "Boundary variation has no independent R_AB charge or exact local flux in compact exterior cells.",
            "Would kill Q_R/B_R leakage.",
            "TARGET_NOT_DERIVED",
            "boundary functional and reference convention are not supplied.",
        ),
        (
            "DER2033_6_verdict",
            "The parent owner row was not found in the corpus, but its exact theorem contract is now narrow: S_parent owner + theta/current + auxiliary preservation + matter/boundary descent.",
            "This is a leap from vague coupling worry to a single missing ownership certificate.",
            "OWNER_ROW_NOT_FOUND_CURRENT_CORPUS",
            "build the owner certificate or source finite Z_R/M_R2/J_R/Q_R/B_R rows.",
        ),
    ]
    rows = []
    for row_id, statement, implication, status, missing in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "statement": statement,
                "implication": implication,
                "status": status,
                "missing": missing,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def operator_ownership_rows() -> list[dict[str, object]]:
    data = [
        ("OP2033_0_Dprimitive", "D T, D S, D e, D theta, D connection", "OWNED_IF_IN_FIELD_LIST", "primitive operator", "requires S_parent field list"),
        ("OP2033_1_R_definition", "R_AB=ln(T^2 S)", "READOUT_COMPATIBILITY", "definition/readout", "not a source by itself"),
        ("OP2033_2_lambda_constraint", "Lambda_R C_R", "ADMIT_IF_PARENT_AUXILIARY", "exact branch candidate", "needs origin and Dirac preservation"),
        ("OP2033_3_DR_raw", "K_R (nabla R_AB)^2", "REJECT_EXACT_BRANCH_OR_PROMOTE_FINITE", "scalar hair fork", "source Z_R if retained"),
        ("OP2033_4_mass_raw", "M_R^2 R_AB^2", "REJECT_EXACT_BRANCH_OR_PROMOTE_FINITE", "massive scalar fork", "source M_R^2 if retained"),
        ("OP2033_5_source_raw", "J_R R_AB", "REJECT_EXACT_BRANCH_OR_PROMOTE_FINITE", "matter/source leak", "derive descent or source J_R"),
        ("OP2033_6_boundary_raw", "Q_R/B_R", "REJECT_EXACT_BRANCH_OR_PROMOTE_FINITE", "boundary charge leak", "derive silence or source Q_R/B_R"),
    ]
    rows = []
    for row_id, operator, decision, classification, next_action in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "operator": operator,
                "decision": decision,
                "classification": classification,
                "next_action": next_action,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def finite_z_rows() -> list[dict[str, object]]:
    data = [
        ("FZ2033_0_ZR", "Z_R", "coefficient of (nabla R_AB)^2 if raw readout kinetic survives", "dimensionless_or_parent_units", "MISSING_SOURCE_BACKED_VALUE", "source parent Hessian/kinetic coefficient or prove operator forbidden"),
        ("FZ2033_1_MR2", "M_R^2", "mass/Hessian for finite R_AB residual", "1/length^2_or_parent_units", "MISSING_SOURCE_BACKED_VALUE", "source parent Hessian or prove absent"),
        ("FZ2033_2_JR", "J_R", "direct matter/source projection onto R_AB", "source_units", "MISSING_MATTER_DESCENT_OR_VALUE", "derive universal descent or source coupling coefficient"),
        ("FZ2033_3_QR", "Q_R", "boundary/exterior charge for R_AB", "charge_units", "MISSING_BOUNDARY_SILENCE_OR_VALUE", "derive no-charge theorem or source boundary coefficient"),
        ("FZ2033_4_BR", "B_R", "boundary functional residue", "action_boundary_units", "MISSING_BOUNDARY_FUNCTIONAL", "write boundary/reference convention"),
        ("FZ2033_5_tau_R10", "tau_R10", "R10 projection/tolerance map", "arena_units", "MISSING_ARENA_PROJECTION", "map finite residual to alpha(lambda) bound"),
        ("FZ2033_6_tau_PPN", "tau_PPN", "PPN gamma/beta/preferred-frame projection", "arena_units", "MISSING_ARENA_PROJECTION", "map finite residual to PPN vector"),
        ("FZ2033_7_tau_clock_orbital", "tau_clock_orbital", "clock and orbital projection map", "arena_units", "MISSING_ARENA_PROJECTION", "map finite residual to clock/orbital tolerances"),
        ("FZ2033_8_claim", "finite Z branch claim", "allowed only when all values/projections are sourced and below bounds", "boolean", "FAIL_BLOCKED", "do not claim local GR/R10/PPN/clock/orbital"),
    ]
    rows = []
    for row_id, symbol, definition, units, status, next_action in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "status": status,
                "next_action": next_action,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2033_0_owner_contract", "owner contract exists", "PASS_NONCLAIM", "the exact required clauses are now written"),
        ("GATE2033_1_parent_action_owner", "S_parent owner row is source-signed", "FAIL_UNSIGNED", "L_core/action field list not parent-signed"),
        ("GATE2033_2_theta_current", "theta/current chain extracted from the same action", "FAIL_MISSING", "theta_MTS and current split not filled"),
        ("GATE2033_3_auxiliary_elimination", "R_AB auxiliary preservation and no remnant proven", "FAIL_MISSING", "preservation/bracket/readout-remnant checks not done"),
        ("GATE2033_4_matter_boundary", "J_R=Q_R=B_R=0 derived", "FAIL_MISSING", "matter descent and boundary silence not derived"),
        ("GATE2033_5_finite_values", "finite branch has sourced coefficients/projections", "FAIL_MISSING", "Z_R/M_R2/J_R/Q_R/B_R/tau rows are missing"),
        ("GATE2033_6_local_GR_claim", "local GR/Newton/PPN/R10 pass", "FAIL_BLOCKED", "neither exact owner theorem nor finite residual bound is claim-valid"),
    ]
    rows = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "gate": gate,
                "status": status,
                "detail": detail,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2033_0_not_circling",
            "This step compresses the repeated local-GR blockers into one owner certificate.",
            "The missing coupling is not a vague hand wave anymore: it is the parent action/variation/current owner of R_AB and matter/boundary descent.",
            "false",
        ),
        (
            "DEC2033_1_best_route",
            "The best derivation route is still auxiliary compatibility, not a physical R_AB scalar.",
            "If S_parent signs OWN2033_1/2/4/6, the exact route can set Z_R=J_R=Q_R=0 without tuning.",
            "false",
        ),
        (
            "DEC2033_2_honest_fallback",
            "If any raw R_AB kinetic/source/boundary operator survives, stop trying to prove zero and score finite residuals.",
            "Populate FZ2033 rows from parent coefficients or empirical bound maps before any claim.",
            "false",
        ),
        (
            "DEC2033_3_next",
            "Next target should try to fill L_core/theta_current for the owner normal form before another broad audit.",
            "If L_core cannot be filled, acquire the first real finite Z_R or J_R source row.",
            "false",
        ),
    ]
    rows = []
    for row_id, decision, rationale, claim_allowed in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "decision": decision,
                "rationale": rationale,
                "claim_allowed": claim_allowed,
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2033_0_2034",
            "target_doc": "2034-Y5-R2FR-Lcore-theta-current-fill-or-first-finite-Z-source.md",
            "objective": "attempt to fill the concrete L_core/theta-current owner for the parent normal form; if impossible, populate the first real finite Z_R/M_R2/J_R/Q_R/B_R source row without accepting placeholders",
            "must_include": "L_core terms; typed field list; variation variables; theta_MTS; current/Q split; auxiliary preservation; matter descent; boundary convention; finite coefficient source paths if owner fails",
            "excluded": "local-GR claim; closure-only lambda_R insertion; GR import as parent action; raw R_AB kinetic in exact branch; cancellation-only pass; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    owner_rows: list[dict[str, object]],
    operator_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2033_0_source_weight_owner",
            SOURCE_WEIGHT_DOCS / "AFRAME_PARENT_ACTION_OWNER_2033_NONCLAIM.csv",
            owner_rows,
        ),
        (
            "COPY2033_1_wep_operator",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2033_OPERATOR_OWNERSHIP_MATRIX_NONCLAIM.csv",
            operator_rows,
        ),
        (
            "COPY2033_2_rab_queue_finite",
            QUEUE / "JR2033_FIRST_FINITE_Z_ROW_NONCLAIM.csv",
            finite_rows,
        ),
    ]
    rows = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update(
            {
                "copy_id": copy_id,
                "path": str(path),
                "rows": len(data),
                "status": "WRITTEN_NONCLAIM_COPY",
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    source_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    operator_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(
        (
            "VAL2033_00_sources_exist",
            all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows),
            "all cited source paths and needles exist",
        )
    )
    checks.append(
        (
            "VAL2033_01_csv_parse",
            all(csv_rows_parse(path) for path in csv_paths),
            "all generated CSV files parse cleanly",
        )
    )
    owner_verdict = next(row for row in owner_rows if row["row_id"] == "OWN2033_7_certificate_verdict")
    checks.append(
        (
            "VAL2033_02_owner_contract_ready",
            owner_verdict["status"] == "OWNER_CONTRACT_READY_PARENT_SIGNATURE_MISSING",
            "owner contract exists but is not theorem-active",
        )
    )
    derivation_verdict = next(row for row in derivation_rows if row["row_id"] == "DER2033_6_verdict")
    checks.append(
        (
            "VAL2033_03_owner_row_not_found",
            derivation_verdict["status"] == "OWNER_ROW_NOT_FOUND_CURRENT_CORPUS",
            "corpus does not yet contain the signed owner row",
        )
    )
    raw_operator = next(row for row in operator_rows if row["row_id"] == "OP2033_3_DR_raw")
    checks.append(
        (
            "VAL2033_04_raw_R_operator_rejected",
            raw_operator["decision"] == "REJECT_EXACT_BRANCH_OR_PROMOTE_FINITE",
            "raw R_AB kinetic term is not allowed inside exact branch",
        )
    )
    finite_claim = next(row for row in finite_rows if row["row_id"] == "FZ2033_8_claim")
    checks.append(
        (
            "VAL2033_05_finite_branch_blocked",
            finite_claim["status"] == "FAIL_BLOCKED",
            "finite branch remains nonclaim until real values/projections exist",
        )
    )
    checks.append(
        (
            "VAL2033_06_claims_blocked",
            all(str(row.get("claim_allowed", "")).lower() == "false" for row in gate_rows),
            "all claim gates remain false",
        )
    )
    checks.append(
        (
            "VAL2033_07_next_selected",
            next_rows[0]["target_id"] == "NEXT2033_0_2034",
            "next target is selected",
        )
    )
    checks.append(
        (
            "VAL2033_08_formalization_unchanged",
            count_formalization_modified() == 0,
            "formalization-workbench modified-file count remains 0",
        )
    )
    checks.append(
        (
            "VAL2033_09_no_formalization_2033_artifacts",
            not formalization_has_2033_artifacts(),
            "no 2033 owner/finite-Z artifacts were written under formalization-workbench",
        )
    )
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(
        (
            "VAL2033_OVERALL",
            overall_ok,
            "2033 owner-certificate checkpoint is internally valid and nonclaim",
        )
    )
    rows = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update(
            {
                "check_id": check_id,
                "status": "PASS" if ok else "FAIL",
                "detail": detail,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    derivation_rows: list[dict[str, object]],
    operator_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    sections = [
        "# 2033 Y5 R2FR Parent Action Ontology Owner Or First Finite Z Row",
        "",
        "## Current Verdict",
        "",
        "This is the non-circular leap: the local-GR problem has been compressed to a single owner certificate. The exact branch needs one parent action to own the field list, variation, theta/current chain, auxiliary R_AB compatibility block, matter descent, and boundary silence. Without that owner row, raw R_AB kinetic/source/boundary terms must be treated as finite residuals and sent to the Z_R/M_R2/J_R/Q_R/B_R source runner.",
        "",
        "No local-GR, Newton, R10, PPN, clock, orbital, or WEP claim is made here.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "note", "valid_for_claim"]),
        "## Parent Action Owner Certificate",
        md_table(owner_rows, ["row_id", "clause", "role", "status", "blocker", "claim_allowed"]),
        "## Derivation Attempt",
        md_table(derivation_rows, ["row_id", "statement", "implication", "status", "missing", "claim_allowed"]),
        "## Operator Ownership Matrix",
        md_table(operator_rows, ["row_id", "operator", "decision", "classification", "next_action", "claim_allowed"]),
        "## First Finite Z Row",
        md_table(finite_rows, ["row_id", "symbol", "definition", "units", "status", "next_action", "claim_allowed"]),
        "## Claim Gate",
        md_table(gate_rows, ["row_id", "gate", "status", "detail", "claim_allowed"]),
        "## Decision Ledger",
        md_table(decision_rows_, ["row_id", "decision", "rationale", "claim_allowed"]),
        "## Next Target",
        md_table(next_rows, ["target_id", "target_doc", "objective", "must_include", "excluded", "claim_allowed"]),
        "## Branch Copies",
        md_table(branch_rows, ["copy_id", "path", "rows", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation_rows_, ["check_id", "status", "detail", "claim_allowed"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    owner_rows = owner_certificate_rows()
    derivation_rows = derivation_attempt_rows()
    operator_rows = operator_ownership_rows()
    finite_rows = finite_z_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2033_SOURCE_REGISTER.csv",
        "owner": OUT / "P8_Y5_PARENT_QLOC_2033_PARENT_ACTION_OWNER_CERTIFICATE.csv",
        "derivation": OUT / "P8_Y5_PARENT_QLOC_2033_OWNER_DERIVATION_ATTEMPT.csv",
        "operator": OUT / "P8_Y5_PARENT_QLOC_2033_OPERATOR_OWNERSHIP_MATRIX.csv",
        "finite": OUT / "P8_Y5_PARENT_QLOC_2033_FIRST_FINITE_Z_ROW.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2033_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2033_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2033_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2033_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2033_VALIDATION.csv",
    }
    write_csv(paths["sources"], source_rows)
    write_csv(paths["owner"], owner_rows)
    write_csv(paths["derivation"], derivation_rows)
    write_csv(paths["operator"], operator_rows)
    write_csv(paths["finite"], finite_rows)
    write_csv(paths["gates"], gate_rows)
    write_csv(paths["decision"], decision_rows_)
    write_csv(paths["next"], next_rows)
    branch_rows = write_branch_copies(owner_rows, operator_rows, finite_rows)
    write_csv(paths["branch"], branch_rows)
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        owner_rows,
        derivation_rows,
        operator_rows,
        finite_rows,
        gate_rows,
        next_rows,
        csv_paths_without_validation,
    )
    write_csv(paths["validation"], validation_rows_)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        owner_rows,
        derivation_rows,
        operator_rows,
        finite_rows,
        gate_rows,
        next_rows,
        csv_paths,
    )
    write_csv(paths["validation"], validation_rows_)
    write_doc(
        source_rows,
        owner_rows,
        derivation_rows,
        operator_rows,
        finite_rows,
        gate_rows,
        decision_rows_,
        next_rows,
        branch_rows,
        validation_rows_,
    )
    remove_pycache()


if __name__ == "__main__":
    main()
