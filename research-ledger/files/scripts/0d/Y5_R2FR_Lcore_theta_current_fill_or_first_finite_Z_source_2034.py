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


DOC = ROOT / "2034-Y5-R2FR-Lcore-theta-current-fill-or-first-finite-Z-source.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def formalization_has_2034_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2034*Lcore*")) or any(FORMALIZATION.rglob("*2034*theta*")) or any(FORMALIZATION.rglob("*2034*finite*Z*"))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2034_00_2033_handoff",
            ROOT / "2033-Y5-R2FR-parent-action-ontology-owner-or-first-finite-Z-row.md",
            ["NEXT2033_0_2034", "DER2033_6_verdict", "VAL2033_OVERALL"],
            "2033 selects L_core/theta-current fill or first finite Z source row.",
        ),
        (
            "SRC2034_01_2033_next",
            OUT / "P8_Y5_PARENT_QLOC_2033_NEXT_TARGET.csv",
            ["NEXT2033_0_2034"],
            "machine-readable 2034 target.",
        ),
        (
            "SRC2034_02_1264_aux_theta",
            ROOT / "1264-Y5-R10-RAB-parent-theta-vR-fill-or-finite-ZR-source-row.md",
            ["AUX1264_0_parent_block", "AUX1264_1_theta", "TVR1264_1_omega_candidate"],
            "candidate auxiliary block and theta_R/Omega_R zero shape.",
        ),
        (
            "SRC2034_03_1265_elimination",
            ROOT / "1265-Y5-R10-RAB-auxiliary-constraint-protection-or-finite-ZR-bound-runner.md",
            ["AET1265_0_auxiliary_elimination", "AP1265_1_no_derivatives", "RR1265_2_matter_source"],
            "conditional auxiliary-elimination theorem and regeneration risks.",
        ),
        (
            "SRC2034_04_1263_presymplectic",
            ROOT / "1263-Y5-R10-vertical-fibre-null-from-parent-presymplectic-degeneracy-or-RAB-prior-envelope-fill.md",
            ["KTC1263_1_null_contradiction", "PB1263_0_L_parent_theta", "PB1263_3_boundary_charge_zero"],
            "conditional contradiction: true vertical nullness forbids finite Z_R kinetic response.",
        ),
        (
            "SRC2034_05_728_omega",
            OUT / "P8_Y5_R10_728_PARENT_OMEGA_CANDIDATE.csv",
            ["OM728_0_covariant_variation_definition", "OM728_1_EH_metric_core", "OM728_2_extra_sector"],
            "covariant variation/theta/Omega candidate rows.",
        ),
        (
            "SRC2034_06_729_current",
            OUT / "P8_Y5_R10_729_PJ_PARENT_ORIGIN_ATTEMPT.csv",
            ["PJA729_6_current_verdict"],
            "Noether P/J current formula derived but not filled without explicit parent L/theta.",
        ),
        (
            "SRC2034_07_10_observer",
            ROOT / "10-observer-map-symplectic-contract.md",
            ["R_AB = ln(T^2 S) = 2 ln(J_q).", "all matter sectors couple to the same observer coframe."],
            "observer readout relation and matter coframe descent target.",
        ),
        (
            "SRC2034_08_1868_grammar",
            ROOT / "source-intake" / "microscope" / "quarantine" / "1868" / "P8_Y5_PARENT_QLOC_1868_CANDIDATE_PARENT_GRAMMAR.csv",
            ["CPG1868_3_derivative_permission", "CPG1868_4_constraint_admission"],
            "candidate derivative-permission and Lambda_R C_R admission grammar.",
        ),
        (
            "SRC2034_09_721_template",
            OUT / "P8_Y5_R10_721_PARENT_ZM_TEMPLATE.csv",
            ["PZT721_2_kinetic_tensor", "PZT721_4_mass_matrix"],
            "finite residual coefficient definitions from parent second variation.",
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


def lcore_fill_rows() -> list[dict[str, object]]:
    data = [
        (
            "LCORE2034_0_log_variables",
            "a=ln(T), b=ln(S), u=R_AB=2a+b=2ln(J_q)",
            "rewrite the reciprocal readout as one explicit coordinate u plus complementary primitive coordinates y^I",
            "EXACT_CHANGE_OF_VARIABLES",
            "choice of y^I is not unique but the u-row condition is coordinate invariant",
        ),
        (
            "LCORE2034_1_factorized_normal_form",
            "L_parent = L_phys[y,Dy,e_pub,omega,theta] + Lambda_R u + L_matter[psi,e_pub,theta] + dB[e_pub,theta]",
            "if true, u is auxiliary compatibility data, not a propagating scalar",
            "DERIVED_NORMAL_FORM_CONTRACT",
            "current corpus has this as a contract, not as a signed parent action",
        ),
        (
            "LCORE2034_2_first_variation",
            "delta L_parent = E_y delta y + E_e delta e + E_theta delta theta + u delta Lambda_R + Lambda_R delta u + d theta_phys",
            "the u/Lambda_R block carries no derivative symplectic potential when factorized",
            "FORMAL_DERIVATION",
            "requires no hidden u or Du dependence in L_phys, L_matter, and B",
        ),
        (
            "LCORE2034_3_auxiliary_solution",
            "E_Lambda=u=0 and E_u=Lambda_R=0",
            "after eliminating the pair, there is no R_AB momentum, no R_AB symplectic sector, and no exterior scalar hair",
            "FORMAL_PASS_IF_FACTORISED",
            "factorisation remains unsigned",
        ),
        (
            "LCORE2034_4_required_law",
            "partial L_phys/partial u = 0 and partial L_phys/partial(D_mu u) = 0; same for matter and boundary terms",
            "this is the exact local-GR owner condition, sharper than saying plateau",
            "NO_U_OR_DU_DEPENDENCE_REQUIRED",
            "must be proved by parent object-language exhaustion",
        ),
        (
            "LCORE2034_5_current_verdict",
            "the L_core/theta-current owner is filled as a mathematical normal form but not parent-signed by the current corpus",
            "we have the theorem target and the finite fallback formulas",
            "LCORE_OWNER_FORMULA_READY_SIGNATURE_MISSING",
            "next work must sign factorisation or source finite coefficients",
        ),
    ]
    rows = []
    for row_id, statement, implication, status, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "statement": statement,
                "implication": implication,
                "status": status,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def null_hessian_rows() -> list[dict[str, object]]:
    data = [
        (
            "HESS2034_0_parent_kinetic_hessian",
            "Z_AB^{mu nu}:= -1/sqrt(-g) delta^2 S_parent / [delta(D_mu x^A) delta(D_nu x^B)] evaluated on the local branch",
            "x^A are primitive log/coframe-routing variables before readout",
            "DEFINITION_EXACT",
        ),
        (
            "HESS2034_1_row_null_law",
            "J_u^A Z_AB^{mu nu}=0 for every B,mu,nu, where J_u^A=partial x^A/partial u",
            "no theta_u and no cross kinetic leakage into the reciprocal readout",
            "EXACT_ZERO_CONDITION_IF_FACTORISED",
        ),
        (
            "HESS2034_2_scalar_projection_not_enough",
            "Z_RR^{mu nu}=J_u^A Z_AB^{mu nu} J_u^B=0 alone is weaker than the row-null law",
            "cross terms Z_RY can still source a reciprocal response",
            "SCRUTINY_GUARD_ACTIVE",
        ),
        (
            "HESS2034_3_finite_Z_formula",
            "if row-null law fails, Z_RR^{mu nu}=J_u^A Z_AB^{mu nu}J_u^B and Z_RY^{mu nu}=J_u^A Z_AB^{mu nu}J_Y^B",
            "this is the first exact finite-Z source formula; numeric parent Hessian values are still missing",
            "SYMBOLIC_SOURCE_FORMULA_NOT_NUMERIC",
        ),
        (
            "HESS2034_4_source_formula",
            "J_R = [partial L/partial u - nabla_mu(partial L/partial(D_mu u))]_0",
            "direct source leakage is now a computable parent variation row, not a vague coupling worry",
            "SYMBOLIC_SOURCE_FORMULA_NOT_NUMERIC",
        ),
        (
            "HESS2034_5_boundary_formula",
            "Pi_R^n = n_mu partial L/partial(D_mu u) + partial B/partial u",
            "boundary hair is killed only by factorisation or by a real sourced boundary row",
            "SYMBOLIC_SOURCE_FORMULA_NOT_NUMERIC",
        ),
        (
            "HESS2034_6_verdict",
            "the exact branch requires row-null Hessian plus no source and no boundary momentum; otherwise finite-Z scoring is mandatory",
            "this is the cleanest technical gate so far for local GR",
            "NULL_HESSIAN_GATE_DERIVED_NONCLAIM",
        ),
    ]
    rows = []
    for row_id, formula, meaning, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "formula": formula,
                "meaning": meaning,
                "status": status,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def theta_current_rows() -> list[dict[str, object]]:
    data = [
        (
            "THETA2034_0_covariant_variation",
            "delta L = E_A delta Phi^A + d theta(delta Phi)",
            "imports the 728 definition into the current owner gate",
            "FORMAL_DEFINITION_OWNED_BY_SOURCE",
        ),
        (
            "THETA2034_1_primitive_momenta",
            "theta_log = Pi_a^mu delta a + Pi_b^mu delta b + theta_y",
            "reciprocal readout silence must be tested at the momentum row, not only equations of motion",
            "FORMAL_DECOMPOSITION",
        ),
        (
            "THETA2034_2_u_component",
            "theta_u^mu = Pi_A^mu J_u^A delta u",
            "theta_u=0 iff the u-row of the kinetic/current map vanishes",
            "DERIVED_COMPONENT_TEST",
        ),
        (
            "THETA2034_3_factorized_zero",
            "for L_phys independent of u and D_mu u, theta_u=0 and Omega_u=0",
            "this closes the R_AB symplectic leak inside the factorized theorem",
            "THETA_R_ZERO_IF_FACTORISED",
        ),
        (
            "THETA2034_4_current_blocker",
            "P/J current extraction remains unfilled without explicit L_parent, theta_Y, mu_X, v_X, and boundary representative",
            "729 is integrated as the exact blocker rather than rerun",
            "CURRENT_CHAIN_STILL_MISSING",
        ),
    ]
    rows = []
    for row_id, expression, role, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "expression": expression,
                "role": role,
                "status": status,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def factorization_theorem_rows() -> list[dict[str, object]]:
    data = [
        (
            "THM2034_0_assumptions",
            "parent variables split into (u,y); L_phys, S_matter, and B factor through y/e_pub/theta only; Lambda_R u is parent-owned",
            "ASSUMPTIONS_EXPLICIT",
            "not yet parent-signed",
        ),
        (
            "THM2034_1_variation",
            "E_Lambda=u=0, E_u=Lambda_R=0, theta_u=0",
            "FORMAL_PROOF_STEP",
            "passes inside the normal form",
        ),
        (
            "THM2034_2_reduction",
            "eliminate (u,Lambda_R) before local readout; reduced phase space has no R_AB propagator or boundary momentum",
            "FORMAL_PROOF_STEP",
            "requires no determinant/readout regeneration",
        ),
        (
            "THM2034_3_local_GR_gate",
            "Z_R=J_R=Q_R=B_R=0 follows only under the factorisation assumptions",
            "EXACT_IF_QUOTIENT_FACTORISATION_PARENT_SIGNED_NOT_CURRENT",
            "no local-GR/R10/PPN/clock/orbital claim",
        ),
        (
            "THM2034_4_failure_branch",
            "any u,Du,matter,or boundary dependence triggers finite residual scoring by HESS2034 formulas",
            "FINITE_BRANCH_TRIGGER",
            "requires parent coefficients or empirical bound maps",
        ),
    ]
    rows = []
    for row_id, theorem_step, status, caveat in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "theorem_step": theorem_step,
                "status": status,
                "caveat": caveat,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def finite_z_formula_rows() -> list[dict[str, object]]:
    data = [
        ("FZ2034_0_ZRR", "Z_RR^{mu nu}", "J_u^A Z_AB^{mu nu}J_u^B", "kinetic scalar projection if factorisation fails"),
        ("FZ2034_1_ZRY", "Z_RY^{mu nu}", "J_u^A Z_AB^{mu nu}J_Y^B", "cross kinetic source that scalar projection alone can miss"),
        ("FZ2034_2_MR2", "M_R^2", "partial^2 V_eff/partial u^2 at branch point", "mass/Hessian residual"),
        ("FZ2034_3_JR", "J_R", "[partial L/partial u - nabla_mu partial L/partial(D_mu u)]_0", "direct matter/core source residual"),
        ("FZ2034_4_QR", "Q_R", "integral over boundary of Pi_R^n", "exterior reciprocal charge"),
        ("FZ2034_5_BR", "B_R", "partial B/partial u", "boundary functional source"),
        ("FZ2034_6_arena_projection", "tau_R10,tau_PPN,tau_clock,tau_orbital", "maps finite residuals to R10/PPN/clock/orbital tolerances", "empirical scoring input"),
        ("FZ2034_7_claim", "finite-Z claim", "allowed only after all formulas have numeric sourced values and projections below bounds", "claim gate"),
    ]
    rows = []
    for row_id, symbol, formula, role in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "formula": formula,
                "role": role,
                "status": "FAIL_BLOCKED" if row_id == "FZ2034_7_claim" else "SYMBOLIC_SOURCE_FORMULA_NOT_NUMERIC",
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2034_0_lcore_formula", "L_core/theta normal form written", "PASS_NONCLAIM", "factorized theorem contract exists"),
        ("GATE2034_1_factorisation_signed", "L_phys/matter/boundary independent of u and Du", "FAIL_UNSIGNED", "parent object-language exhaustion not proved"),
        ("GATE2034_2_row_null_hessian", "J_u^A Z_AB=0 for all B", "FAIL_UNEVALUATED", "parent Hessian not available"),
        ("GATE2034_3_theta_current", "theta_u=Omega_u=0 from one parent action", "FAIL_CONDITIONAL", "true only if factorisation signed"),
        ("GATE2034_4_matter_boundary", "J_R=Q_R=B_R=0", "FAIL_UNSIGNED", "matter descent and boundary silence not parent-signed"),
        ("GATE2034_5_finite_values", "finite residual rows numeric and sourced", "FAIL_MISSING_VALUES", "only symbolic formulas are available"),
        ("GATE2034_6_local_GR_claim", "local GR/Newton/R10/PPN/clock/orbital pass", "FAIL_BLOCKED", "exact theorem and finite residual branch are both nonclaim"),
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
            "DEC2034_0_real_leap",
            "The route is no longer 'prove plateau'; it is prove quotient factorisation or compute the row-null Hessian failure.",
            "This gives a concrete algebraic target for the coupling problem.",
        ),
        (
            "DEC2034_1_best_route",
            "Best derivation route: prove L_phys, matter, and boundary factor through y/e_pub/theta and not u=R_AB.",
            "Then u/Lambda_R eliminate exactly with theta_u=0 and no scalar hair.",
        ),
        (
            "DEC2034_2_failure_policy",
            "If any u or Du dependence survives, stop trying to call it GR reduction and source finite Z/J/Q/B rows.",
            "The HESS2034 formulas define what must be measured or extracted.",
        ),
        (
            "DEC2034_3_next",
            "Next target is parent object-language exhaustion for the quotient factorisation clause.",
            "This is the least hand-wavy way to close local GR.",
        ),
    ]
    rows = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "decision": decision,
                "rationale": rationale,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2034_0_2035",
            "target_doc": "2035-Y5-R2FR-quotient-factorisation-exhaustion-or-row-null-hessian-source.md",
            "objective": "prove or reject the parent object-language exhaustion clause that removes u=R_AB and D_mu u from L_phys, matter, and boundary; if rejected, populate the row-null Hessian finite-source formulas with real parent coefficients or sourced bounds",
            "must_include": "u=2lnJq variable split; quotient map y; L_phys factorisation; matter coframe descent; boundary functional; row-null Hessian J_u^A Z_AB; theta_u current; finite Z_R/J_R/Q_R/B_R formulas; no-cancellation guard",
            "excluded": "local-GR claim; plateau axiom; closure-only lambda insertion; scalar-projection-only Z_R test; GR import as proof; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    theorem_rows: list[dict[str, object]],
    hessian_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2034_0_source_weight_theorem",
            SOURCE_WEIGHT_DOCS / "AFRAME_QUOTIENT_FACTORISATION_THEOREM_2034_NONCLAIM.csv",
            theorem_rows,
        ),
        (
            "COPY2034_1_wep_hessian",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2034_ROW_NULL_HESSIAN_GATE_NONCLAIM.csv",
            hessian_rows,
        ),
        (
            "COPY2034_2_rab_queue_finite",
            QUEUE / "JR2034_FINITE_Z_FORMULA_ROWS_NONCLAIM.csv",
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
    lcore_rows: list[dict[str, object]],
    hessian_rows: list[dict[str, object]],
    theta_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(
        (
            "VAL2034_00_sources_exist",
            all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows),
            "all cited source paths and needles exist",
        )
    )
    checks.append(
        (
            "VAL2034_01_csv_parse",
            all(csv_rows_parse(path) for path in csv_paths),
            "all generated CSV files parse cleanly",
        )
    )
    lcore_law = next(row for row in lcore_rows if row["row_id"] == "LCORE2034_4_required_law")
    checks.append(
        (
            "VAL2034_02_lcore_law",
            lcore_law["status"] == "NO_U_OR_DU_DEPENDENCE_REQUIRED",
            "exact L_core factorisation law is present",
        )
    )
    hessian_verdict = next(row for row in hessian_rows if row["row_id"] == "HESS2034_6_verdict")
    checks.append(
        (
            "VAL2034_03_null_hessian_gate",
            hessian_verdict["status"] == "NULL_HESSIAN_GATE_DERIVED_NONCLAIM",
            "row-null Hessian gate is derived as nonclaim",
        )
    )
    theta_zero = next(row for row in theta_rows if row["row_id"] == "THETA2034_3_factorized_zero")
    checks.append(
        (
            "VAL2034_04_theta_zero_conditional",
            theta_zero["status"] == "THETA_R_ZERO_IF_FACTORISED",
            "theta_R zero condition is tied to factorisation",
        )
    )
    theorem_claim = next(row for row in theorem_rows if row["row_id"] == "THM2034_3_local_GR_gate")
    checks.append(
        (
            "VAL2034_05_theorem_nonclaim",
            theorem_claim["status"] == "EXACT_IF_QUOTIENT_FACTORISATION_PARENT_SIGNED_NOT_CURRENT",
            "local-GR theorem remains conditional and nonclaim",
        )
    )
    finite_claim = next(row for row in finite_rows if row["row_id"] == "FZ2034_7_claim")
    checks.append(
        (
            "VAL2034_06_finite_blocked",
            finite_claim["status"] == "FAIL_BLOCKED",
            "finite branch remains blocked without numeric sourced rows",
        )
    )
    checks.append(
        (
            "VAL2034_07_claims_blocked",
            all(str(row.get("claim_allowed", "")).lower() == "false" for row in gate_rows),
            "all claim gates remain false",
        )
    )
    checks.append(
        (
            "VAL2034_08_next_selected",
            next_rows[0]["target_id"] == "NEXT2034_0_2035",
            "next target is selected",
        )
    )
    checks.append(
        (
            "VAL2034_09_formalization_unchanged",
            count_formalization_modified() == 0,
            "formalization-workbench modified-file count remains 0",
        )
    )
    checks.append(
        (
            "VAL2034_10_no_formalization_2034_artifacts",
            not formalization_has_2034_artifacts(),
            "no 2034 Lcore/theta/finite-Z artifacts were written under formalization-workbench",
        )
    )
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(
        (
            "VAL2034_OVERALL",
            overall_ok,
            "2034 L_core/theta-current checkpoint is internally valid and nonclaim",
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
    lcore_rows: list[dict[str, object]],
    hessian_rows: list[dict[str, object]],
    theta_rows: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    sections = [
        "# 2034 Y5 R2FR Lcore Theta Current Fill Or First Finite Z Source",
        "",
        "## Current Verdict",
        "",
        "This is the strongest local-GR route so far. The reciprocal variable is now treated as `u=R_AB=2ln(J_q)`. Exact local reduction requires a quotient-factorised parent core: `L_phys`, matter, and boundary terms must have no `u` or `D_mu u` dependence, with only the auxiliary block `Lambda_R u`. If that is parent-signed, `E_Lambda=u=0`, `E_u=Lambda_R=0`, `theta_u=Omega_u=0`, and no `Z_R/J_R/Q_R/B_R` hair survives. If any `u` or `D_mu u` term survives, the theory must enter finite residual scoring through the row-null Hessian formulas below.",
        "",
        "No local-GR, Newton, R10, PPN, clock, orbital, WEP, or public claim is made.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "note", "valid_for_claim"]),
        "## L Core Fill Attempt",
        md_table(lcore_rows, ["row_id", "statement", "implication", "status", "blocker", "claim_allowed"]),
        "## Row Null Hessian Gate",
        md_table(hessian_rows, ["row_id", "formula", "meaning", "status", "claim_allowed"]),
        "## Theta Current Fill",
        md_table(theta_rows, ["row_id", "expression", "role", "status", "claim_allowed"]),
        "## Quotient Factorisation Theorem",
        md_table(theorem_rows, ["row_id", "theorem_step", "status", "caveat", "claim_allowed"]),
        "## First Finite Z Source Formulas",
        md_table(finite_rows, ["row_id", "symbol", "formula", "role", "status", "claim_allowed"]),
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
    lcore_rows = lcore_fill_rows()
    hessian_rows = null_hessian_rows()
    theta_rows = theta_current_rows()
    theorem_rows = factorization_theorem_rows()
    finite_rows = finite_z_formula_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2034_SOURCE_REGISTER.csv",
        "lcore": OUT / "P8_Y5_PARENT_QLOC_2034_LCORE_THETA_FILL_ATTEMPT.csv",
        "hessian": OUT / "P8_Y5_PARENT_QLOC_2034_ROW_NULL_HESSIAN_GATE.csv",
        "theta": OUT / "P8_Y5_PARENT_QLOC_2034_THETA_CURRENT_FILL.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2034_QUOTIENT_FACTORISATION_THEOREM.csv",
        "finite": OUT / "P8_Y5_PARENT_QLOC_2034_FIRST_FINITE_Z_SOURCE_FORMULAS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2034_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2034_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2034_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2034_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2034_VALIDATION.csv",
    }
    write_csv(paths["sources"], source_rows)
    write_csv(paths["lcore"], lcore_rows)
    write_csv(paths["hessian"], hessian_rows)
    write_csv(paths["theta"], theta_rows)
    write_csv(paths["theorem"], theorem_rows)
    write_csv(paths["finite"], finite_rows)
    write_csv(paths["gates"], gate_rows)
    write_csv(paths["decision"], decision_rows_)
    write_csv(paths["next"], next_rows)
    branch_rows = write_branch_copies(theorem_rows, hessian_rows, finite_rows)
    write_csv(paths["branch"], branch_rows)
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        lcore_rows,
        hessian_rows,
        theta_rows,
        theorem_rows,
        finite_rows,
        gate_rows,
        next_rows,
        csv_paths_without_validation,
    )
    write_csv(paths["validation"], validation_rows_)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        lcore_rows,
        hessian_rows,
        theta_rows,
        theorem_rows,
        finite_rows,
        gate_rows,
        next_rows,
        csv_paths,
    )
    write_csv(paths["validation"], validation_rows_)
    write_doc(
        source_rows,
        lcore_rows,
        hessian_rows,
        theta_rows,
        theorem_rows,
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
