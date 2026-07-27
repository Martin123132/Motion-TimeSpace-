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


DOC = ROOT / "2050-Y5-R2FR-minimal-motion-load-radial-action-or-RAB-residual-runner.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2050_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        patterns = (
            "*2050-Y5-R2FR*",
            "*P8_Y5_PARENT_QLOC_2050*",
            "*Y5_R2FR_minimal_motion_load_radial_action_or_RAB_residual_runner_2050*",
        )
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2050_00_2049_doc",
            ROOT / "2049-Y5-R2FR-motion-load-parent-Euler-difference-or-RAB-finite-residual.md",
            ["NEXT2049_0_2050", "ECO2049_0_log_variables", "VAL2049_OVERALL"],
            "2049 handoff into minimal radial action or finite residual runner.",
        ),
        (
            "SRC2050_01_2049_next",
            OUT / "P8_Y5_PARENT_QLOC_2049_NEXT_TARGET.csv",
            ["NEXT2049_0_2050", "candidate S_rad", "finite residual runner refusal"],
            "machine-readable 2050 target.",
        ),
        (
            "SRC2050_02_04_contract",
            ROOT / "04-vacuum-reciprocity-action-contract.md",
            ["d/dr [ W(r,L,fields) dR_AB/dr ] = J_R", "derive the reciprocal-strain equation from motion-load variables"],
            "vacuum reciprocity action contract.",
        ),
        (
            "SRC2050_03_05_attempt",
            ROOT / "05-reciprocity-theorem-attempt.md",
            ["S_R = integral dr [0.5 W(r) (R_AB')^2 + J_R R_AB].", "W R_AB' = Q_R"],
            "reciprocal-strain action variation and Q_R obstruction.",
        ),
        (
            "SRC2050_04_06_neutrality",
            ROOT / "06-reciprocal-charge-source-neutrality.md",
            ["Pi_R = 0 -> Q_R = 0 -> R_AB = 0 -> AB = 1.", "|q_R| <= 1e-5"],
            "source neutrality and conservative PPN danger.",
        ),
        (
            "SRC2050_05_1859_noGR",
            ROOT / "1859-Y5-R2FR-motion-load-phase-volume-parent-origin-no-GR-import-derivation.md",
            ["NG1859_4_ordinary_current", "FRS1859_2_parent_Euler_difference", "VAL1859_OVERALL"],
            "no-GR-import route selection and current no-go.",
        ),
        (
            "SRC2050_06_1577_finite",
            ROOT / "1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md",
            ["FCF1577_0_qRhat", "ARI1577_0_PPN", "VAL1577_OVERALL"],
            "finite component fallback and arena interface source.",
        ),
        (
            "SRC2050_07_2049_finite",
            OUT / "P8_Y5_PARENT_QLOC_2049_FINITE_RAB_RESIDUAL_ROWS.csv",
            ["RAB2049_0_C_R_profile", "RAB2049_VERDICT"],
            "2049 finite R_AB residual rows.",
        ),
        (
            "SRC2050_08_2048_coframe",
            OUT / "P8_Y5_PARENT_QLOC_2048_MOTION_LOAD_COFRAME_CONSTRUCTION.csv",
            ["MLC2048_2_observed_coframe", "MLC2048_6_radial_cell_condition"],
            "motion-load coframe and exact R_AB identity source.",
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
                "source_kind": "local",
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def action_candidate_rows() -> list[dict[str, object]]:
    data = [
        (
            "ACT2050_0_identity_setup",
            "radial variables",
            "x=ln(T), y=ln(sqrt(S)), C_R=2(x+y), J_q=exp(x+y)",
            "EXACT_SETUP",
            "valid starting point",
            "none",
        ),
        (
            "ACT2050_1_multiplier_constraint",
            "S_lambda=int dr lambda_R C_R",
            "delta_lambda S gives C_R=0 directly; delta_x and delta_y source lambda_R equations.",
            "REJECT_AS_PARENT_DERIVATION_CURRENTLY",
            "would force p=1 if lambda_R is parent-owned",
            "lambda_R origin, constraint class, source compatibility and boundary algebra are not derived",
        ),
        (
            "ACT2050_2_strain_action",
            "S_strain=int dr [0.5 W_R (partial_r C_R)^2 + J_R C_R]",
            "variation gives -partial_r(W_R partial_r C_R)+J_R=0; vacuum gives W_R partial_r C_R=Q_R.",
            "VALID_CONDITIONAL_NOT_ZERO_PROOF",
            "gives R_AB=0 only if J_R=0, Q_R=0, W_R>0 and boundary normalization hold",
            "Q_R no-charge theorem and W_R parent sign are missing",
        ),
        (
            "ACT2050_3_first_order_constraint",
            "S_mu=int dr mu_R(partial_r C_R-S_R)",
            "variation can impose partial_r C_R=S_R, but mu_R is a constraint insertion unless parent-owned.",
            "REJECT_AS_CLOSURE_IF_UNOWNED",
            "would give C_R=0 if S_R=0 and boundary normalization hold",
            "mu_R origin and S_R source map are not derived",
        ),
        (
            "ACT2050_4_EH_inheritance",
            "S_EH[g_obs] after MTS fixed-point derivation",
            "if EH local fixed point is derived from MTS, the GR time-radial difference is legitimate inheritance.",
            "VALID_ROUTE_BLOCKED",
            "would avoid inventing a new R_AB action",
            "A511 extra-sector/source/boundary/readout silence remains unsigned",
        ),
        (
            "ACT2050_5_minimal_action_verdict",
            "minimal no-GR-import radial action",
            "No current candidate is both parent-owned and sufficient to force C_R=0. Multiplier/first-order routes are closure unless their origin is derived; strain route leaves Q_R hair.",
            "NO_PARENT_ACTION_DERIVED_CURRENT_CORPUS",
            "finite R_AB runner must remain active",
            "parent origin for constraint/current/source neutrality missing",
        ),
    ]
    rows = []
    for row_id, candidate, formula, status, if_closed, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "candidate": candidate,
                "formula": formula,
                "status": status,
                "if_closed": if_closed,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def variation_audit_rows() -> list[dict[str, object]]:
    data = [
        (
            "VAR2050_0_multiplier_delta_lambda",
            "delta_lambda S_lambda",
            "C_R=0",
            "EXACT_FORMAL",
            "proves the closure term works formally",
            "not evidence lambda_R is an MTS parent field",
        ),
        (
            "VAR2050_1_multiplier_delta_x_y",
            "delta_x,delta_y S_lambda",
            "both variations receive 2 lambda_R plus any parent coupling terms",
            "FORMAL_BACKREACTION",
            "would require a consistent constraint algebra/source map",
            "not supplied in current corpus",
        ),
        (
            "VAR2050_2_strain_delta_C",
            "delta_C S_strain",
            "-partial_r(W_R partial_r C_R)+J_R=0",
            "EXACT_FORMAL",
            "produces the known reciprocal current equation",
            "leaves Q_R unless no-charge theorem is signed",
        ),
        (
            "VAR2050_3_first_order_delta_mu",
            "delta_mu S_mu",
            "partial_r C_R-S_R=0",
            "EXACT_FORMAL",
            "would match the 2049 first-order route",
            "mu_R and S_R are closure objects unless parent-derived",
        ),
        (
            "VAR2050_4_claim_verdict",
            "variation audit",
            "formal variations exist but none currently supplies a parent-owned MTS derivation of R_AB=0",
            "FORMAL_SUCCESS_PARENT_FAILURE",
            "do not promote local GR",
            "parent origin and no-charge certificates missing",
        ),
    ]
    rows = []
    for row_id, variation, result, status, meaning, blocker in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "variation": variation,
                "result": result,
                "status": status,
                "meaning": meaning,
                "blocker": blocker,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def residual_runner_input_rows() -> list[dict[str, object]]:
    data = [
        (
            "RRUN2050_0_C_R_profile",
            "C_R_profile",
            "MISSING_PROFILE",
            "dimensionless",
            "PPN;light_bending;Shapiro;orbital;R10;clock",
            "RAB2049_0_C_R_profile",
        ),
        (
            "RRUN2050_1_q_R_hat",
            "q_R_hat_or_Q_R",
            "MISSING_QR_VALUE",
            "dimensionless_or_current_units",
            "PPN;orbital;R10",
            "FCF1577_0_qRhat",
        ),
        (
            "RRUN2050_2_S_R_source",
            "S_R_source",
            "MISSING_SOURCE_BALANCE_OR_NUMERIC_ROW",
            "declared_source_units",
            "Newton_GM;PPN_beta;WEP_source",
            "RAB2049_2_S_R_source",
        ),
        (
            "RRUN2050_3_boundary_tail",
            "B_R_or_Pi_R",
            "MISSING_BOUNDARY_CLASS_OR_NUMERIC_BOUND",
            "boundary_units",
            "orbital;clock;source_normalization;PPN",
            "RAB2049_3_boundary_tail",
        ),
        (
            "RRUN2050_4_tau_PPN",
            "tau_PPN_R",
            "MISSING_PPN_PROJECTION",
            "dimensionless_response",
            "PPN",
            "RAB2049_4_tau_PPN",
        ),
        (
            "RRUN2050_5_tau_R10_clock_orbit",
            "tau_R10_R_tau_clock_R_tau_orbital_R",
            "MISSING_ARENA_PROJECTIONS",
            "arena_kernels",
            "R10;clock;orbital",
            "RAB2049_5_tau_R10_clock_orbit",
        ),
    ]
    rows = []
    for row_id, quantity, current_value, units, observable_links, source_anchor in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "current_value": current_value,
                "units": units,
                "observable_links": observable_links,
                "source_anchor": source_anchor,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def runner_rows(inputs: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = []
    for item in inputs:
        missing = str(item["current_value"]).startswith("MISSING")
        row = base_row()
        row.update(
            {
                "run_id": "RUN_" + str(item["row_id"]),
                "input_id": item["row_id"],
                "quantity": item["quantity"],
                "accepted_for_scoring": False,
                "verdict": "REJECTED_PLACEHOLDER_INPUT" if missing else "REJECTED_NONCLAIM_INPUT",
                "reason": "finite R_AB residual runner requires theorem-zero or numeric/source-backed value, units, source path, projection kernel and no-cancellation policy",
                "claim_allowed": False,
            }
        )
        rows.append(row)
    verdict = base_row()
    verdict.update(
        {
            "run_id": "RUN2050_VERDICT",
            "input_id": "all_RAB_finite_rows",
            "quantity": "finite_R_AB_residual_branch",
            "accepted_for_scoring": False,
            "verdict": "FINITE_RAB_RUNNER_BLOCKED_NONCLAIM",
            "reason": "minimal action route is not parent-derived and all finite residual rows remain placeholder/nonclaim",
            "claim_allowed": False,
        }
    )
    rows.append(verdict)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2050_0_formal_variations", "formal radial actions vary correctly", "PASS_NONCLAIM", "multiplier/strain/first-order variations are mathematically understood"),
        ("GATE2050_1_parent_action_origin", "minimal radial action is parent-derived", "FAIL_BLOCKED", "lambda_R/mu_R/W_R/J_R origin not signed"),
        ("GATE2050_2_QR_nocharge", "Q_R=0 or source neutrality derived", "FAIL_BLOCKED", "reciprocal charge neutrality remains conditional"),
        ("GATE2050_3_RAB_zero", "R_AB=0/p=1 derived", "FAIL_BLOCKED", "all successful routes require unsigned parent certificates"),
        ("GATE2050_4_beta_local_GR", "beta=1 and local GR/Newton derived", "FAIL_BLOCKED", "gamma lane and formal actions do not close beta/source/conservation"),
        ("GATE2050_5_finite_runner", "finite R_AB runner scoreable", "FAIL_BLOCKED", "all residual inputs are placeholders"),
    ]
    rows = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update({"row_id": row_id, "gate": gate, "status": status, "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        (
            "DEC2050_0_minimal_action_result",
            "Formal minimal actions exist, but none is a parent derivation yet.",
            "A multiplier action gives the desired answer too directly; a strain action is honest but leaves Q_R hair; first-order constraint is closure unless mu_R is parent-owned.",
        ),
        (
            "DEC2050_1_best_theory_route",
            "Do not abandon derivation; shift to parent-origin certificates.",
            "The next useful proof target is the origin/classification of lambda_R or Q_R no-charge, not another restatement of R_AB=0.",
        ),
        (
            "DEC2050_2_best_testing_route",
            "If the parent-origin route stalls, the finite residual runner is ready to be filled.",
            "It now knows which rows block PPN/R10/clock/orbital scoring and refuses placeholders.",
        ),
        (
            "DEC2050_3_project_status",
            "This is not a collapse of the motion-load route.",
            "The route has a concrete coframe and a precise action gap; that is better than an intuitive GR analogy.",
        ),
    ]
    rows = []
    for row_id, decision, rationale in data:
        row = base_row()
        row.update({"row_id": row_id, "decision": decision, "rationale": rationale, "claim_allowed": False})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "target_id": "NEXT2050_0_2051",
            "target_doc": "2051-Y5-R2FR-lambdaR-origin-or-QR-nocharge-certificate.md",
            "objective": "try to derive the parent origin/class of lambda_R or an exact Q_R no-charge theorem; if neither closes, promote the finite R_AB residual runner from schema to source-acquisition mode",
            "must_include": "lambda_R constraint class; mu_R/first-order closure rejection; Q_R source neutrality; Pi_R boundary variation; W_R positivity; no-GR-import guard; finite residual source acquisition queue",
            "excluded": "declaring lambda_R by taste; using asymptotic flatness alone to kill Q_R; fitting p=1; claiming beta/local GR; invented residual values; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    action_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2050_0_source_weight_action_audit",
            SOURCE_WEIGHT_DOCS / "AFRAME_MINIMAL_RADIAL_ACTION_2050_NONCLAIM.csv",
            action_rows,
        ),
        (
            "COPY2050_1_wep_residual_runner_inputs",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2050_RAB_RESIDUAL_RUNNER_INPUTS_NONCLAIM.csv",
            residual_rows,
        ),
        (
            "COPY2050_2_rab_next",
            QUEUE / "JR2050_LAMBDAR_OR_QR_NOCHARGE_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
    ]
    rows = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update({"copy_id": copy_id, "path": str(path), "rows": len(data), "status": "WRITTEN_NONCLAIM_COPY"})
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    action_rows: list[dict[str, object]],
    variation_rows: list[dict[str, object]],
    residual_inputs: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    action_verdict = next(row for row in action_rows if row["row_id"] == "ACT2050_5_minimal_action_verdict")
    variation_verdict = next(row for row in variation_rows if row["row_id"] == "VAR2050_4_claim_verdict")
    runner_verdict = next(row for row in runner if row["run_id"] == "RUN2050_VERDICT")
    formal_gate = next(row for row in gates if row["row_id"] == "GATE2050_0_formal_variations")
    gr_gate = next(row for row in gates if row["row_id"] == "GATE2050_4_beta_local_GR")
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2050_00_local_sources_exist", source_ok, "all cited local source paths and needles exist"))
    checks.append(("VAL2050_01_csv_parse", all(csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2050_02_minimal_action_not_parent", action_verdict["status"] == "NO_PARENT_ACTION_DERIVED_CURRENT_CORPUS", "minimal action route is not promoted"))
    checks.append(("VAL2050_03_variations_formal_only", variation_verdict["status"] == "FORMAL_SUCCESS_PARENT_FAILURE", "formal variations do not become parent proof"))
    checks.append(("VAL2050_04_residual_inputs_nonclaim", all(not bool(row["ready_for_scoring"]) for row in residual_inputs), "finite residual inputs remain nonclaim"))
    checks.append(("VAL2050_05_runner_rejects", runner_verdict["verdict"] == "FINITE_RAB_RUNNER_BLOCKED_NONCLAIM", "finite residual runner refuses placeholders"))
    checks.append(("VAL2050_06_only_formal_gate_passes", formal_gate["status"] == "PASS_NONCLAIM", "only formal variation gate passes, nonclaim"))
    checks.append(("VAL2050_07_local_GR_blocked", gr_gate["status"] == "FAIL_BLOCKED", "local-GR/Newton gate remains blocked"))
    checks.append(("VAL2050_08_next_selected", next_rows_[0]["target_id"] == "NEXT2050_0_2051", "2051 lambda_R/Q_R no-charge target selected"))
    checks.append(("VAL2050_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2050_10_no_formalization_2050_artifacts", not formalization_has_2050_artifacts(), "no 2050 artifacts were written under formalization-workbench"))
    checks.append(("VAL2050_11_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"))
    overall_ok = all(ok for _, ok, _ in checks)
    checks.append(("VAL2050_OVERALL", overall_ok, "2050 audits minimal radial actions and blocks claims while preparing lambda_R/Q_R next target"))
    rows = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    action_rows: list[dict[str, object]],
    variation_rows: list[dict[str, object]],
    residual_inputs: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2050 Y5 R2FR Minimal Motion-Load Radial Action Or R_AB Residual Runner",
        "",
        "## Current Verdict",
        "",
        "2050 tests the tempting move: write the smallest radial action that forces `C_R=ln(T^2S)=0`. Formally this is easy. A multiplier `lambda_R C_R` forces the answer, a first-order multiplier can force `partial_r C_R=S_R`, and a strain action gives the known current equation. But none of these is a parent derivation unless the multiplier/current/source class is itself derived from MTS.",
        "",
        "So the result is disciplined: formal action routes are recorded, but `R_AB=0`, `p=1`, `beta=1`, local GR/Newton and PPN safety are not claimed. The finite `R_AB` runner is staged and refuses placeholders. No GitHub action and no `formalization-workbench` edits are made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Action Candidate Audit",
        md_table(action_rows, ["row_id", "candidate", "formula", "status", "if_closed", "blocker", "claim_allowed"]),
        "## Variation Audit",
        md_table(variation_rows, ["row_id", "variation", "result", "status", "meaning", "blocker", "claim_allowed"]),
        "## Finite Residual Runner Inputs",
        md_table(residual_inputs, ["row_id", "quantity", "current_value", "units", "observable_links", "source_anchor", "ready_for_scoring", "claim_allowed"]),
        "## Runner Refusals",
        md_table(runner, ["run_id", "input_id", "quantity", "accepted_for_scoring", "verdict", "reason", "claim_allowed"]),
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
    action_rows = action_candidate_rows()
    variation_rows = variation_audit_rows()
    residual_inputs = residual_runner_input_rows()
    runner = runner_rows(residual_inputs)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2050_SOURCE_REGISTER.csv",
        "action": OUT / "P8_Y5_PARENT_QLOC_2050_ACTION_CANDIDATE_AUDIT.csv",
        "variation": OUT / "P8_Y5_PARENT_QLOC_2050_VARIATION_AUDIT.csv",
        "residual_inputs": OUT / "P8_Y5_PARENT_QLOC_2050_RESIDUAL_RUNNER_INPUTS.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2050_RUNNER_REFUSALS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2050_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2050_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2050_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2050_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2050_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["action"], action_rows)
    write_csv(paths["variation"], variation_rows)
    write_csv(paths["residual_inputs"], residual_inputs)
    write_csv(paths["runner"], runner)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(action_rows, residual_inputs, next_rows_)
    write_csv(paths["branch"], copies)
    remove_pycache()
    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [Path(row["path"]) for row in copies]
    validation = validation_rows(sources, action_rows, variation_rows, residual_inputs, runner, gates, next_rows_, csv_paths_without_validation)
    write_csv(paths["validation"], validation)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, action_rows, variation_rows, residual_inputs, runner, gates, next_rows_, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, action_rows, variation_rows, residual_inputs, runner, gates, decisions, next_rows_, copies, validation)
    remove_pycache()


if __name__ == "__main__":
    main()
