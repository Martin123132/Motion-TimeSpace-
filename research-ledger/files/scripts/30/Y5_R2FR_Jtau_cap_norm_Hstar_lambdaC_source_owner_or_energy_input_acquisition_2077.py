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


DOC = ROOT / "2077-Y5-R2FR-Jtau-cap-norm-Hstar-lambdaC-source-owner-or-energy-input-acquisition.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2077_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2077-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2077*",
        "*Y5_R2FR_Jtau_cap_norm_Hstar_lambdaC_source_owner_or_energy_input_acquisition_2077*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def scripts_pycache_exists() -> bool:
    return (SCRIPT_PATH.parent / "__pycache__").exists()


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2077_00_2076_doc",
            ROOT / "2076-Y5-R2FR-positive-current-density-cap-functional-or-first-numeric-energy-bound-inputs.md",
            ["NEXT2076_0_2077", "k_C_min>0", "q_R_hat_policy_ceiling = 4.6e-05"],
            "2076 handoff to J_tau/Hstar/lambda_C/mu_C source-owner inputs.",
        ),
        (
            "SRC2077_01_2076_sign",
            OUT / "P8_Y5_PARENT_QLOC_2076_POSITIVE_DENSITY_SIGN_THEOREM.csv",
            ["PDS2076_1_positive_inner_product", "PDS2076_3_strict_lower_bound", "STRICT_POSITIVITY_NOT_DERIVED"],
            "conditional sign theorem and strict lower-bound blocker.",
        ),
        (
            "SRC2077_02_2076_owner",
            OUT / "P8_Y5_PARENT_QLOC_2076_PARENT_OWNER_AUDIT.csv",
            ["POA2076_0_Jtau", "MISSING_LAMBDA_C_SOURCE", "PARENT_OWNER_NOT_CLOSED"],
            "owner audit for the four coupling inputs.",
        ),
        (
            "SRC2077_03_2076_inputs",
            OUT / "P8_Y5_PARENT_QLOC_2076_FIRST_ENERGY_BOUND_INPUTS.csv",
            ["FEI2076_0_Wmin", "FEI2076_12_qRceiling", "SOURCE_BACKED_NONCLAIM_POLICY_CEILING"],
            "first energy-bound input table with only policy ceiling numeric.",
        ),
        (
            "SRC2077_04_1008_variation",
            OUT / "P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv",
            ["PVA1008_2_J_tau", "formal_shape_no_owner", "PVA1008_6_verdict"],
            "J_tau is formal-shape only because parent theta/Q_tau extraction is not closed.",
        ),
        (
            "SRC2077_05_1519_mhref",
            OUT / "P8_Y5_PARENT_FRAME_1519_MHREF_FIRST_ROW_SCHEMA.csv",
            ["MHR1519_3_theta", "MHR1519_7_MHref", "CLAIM_BLOCKED"],
            "Hstar/M_H_ref denominator row remains missing.",
        ),
        (
            "SRC2077_06_1519_tau_lock",
            OUT / "P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv",
            ["OCF1519_4_tau_lock", "OCF1519_6_MHref_denominator", "COFRAME_TAU_LOCK_NOT_PROVED"],
            "same tau/frame lock needed for cap current and Hstar remains unsigned.",
        ),
        (
            "SRC2077_07_2062_boundary",
            OUT / "P8_Y5_PARENT_QLOC_2062_BOUNDARY_FUNCTIONAL_GRAMMAR.csv",
            ["BGA2062_4_orientation", "UNSIGNED_FOR_FINITE_SCORING", "Q_R = W_R n^mu partial_mu R_AB"],
            "mu_C/cap orientation and finite scoring sign convention remain unsigned.",
        ),
        (
            "SRC2077_08_1720_current_norm",
            ROOT / "1720-Y5-R2FR-observed-Hilbert-current-norm-source-row-or-matter-functor-signature.md",
            ["JHT1720_4_verdict", "CONDITIONAL_THEOREM_ONLY_NORM_NOT_SOURCED", "observed Hilbert current norm"],
            "current-norm sourcing is a known unresolved ordinary-matter blocker.",
        ),
        (
            "SRC2077_09_04_W_contract",
            ROOT / "04-vacuum-reciprocity-action-contract.md",
            ["d/dr [ W(r,L,fields) dR_AB/dr ] = J_R", "W > 0", "attempt the reciprocal-strain theorem"],
            "W_R positive operator is a contract, not a sourced lower-bound row.",
        ),
        (
            "SRC2077_10_qrhat_policy",
            OUT / "P8_Y5_R10_1249_FINITE_QRHAT_CANDIDATE_RESULTS.csv",
            ["QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM", "4.6e-05", "ACCEPTED_NONCLAIM_FINITE_QRHAT"],
            "numeric q_R_hat ceiling exists as nonclaim policy only.",
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


def lower_bound_theorem_rows() -> list[dict[str, object]]:
    data = [
        (
            "LBT2077_0_setup",
            "positive-density stiffness",
            "I_tau = ||J_tau^cap||_h^2/H_*^2 and k_C = lambda_C mu_C I_tau",
            "candidate positive-current-density cap functional from 2075/2076",
            "SETUP_CONDITIONAL",
            True,
        ),
        (
            "LBT2077_1_nonnegative",
            "nonnegative stiffness",
            "if h_C positive, H_*>0, lambda_C>=0 and mu_C>0, then k_C>=0",
            "sign-safe mechanism; not yet parent adopted",
            "NONNEGATIVE_THEOREM_CONDITIONAL",
            True,
        ),
        (
            "LBT2077_2_strict_bound",
            "strict stiffness lower bound",
            "if ||J_tau^cap||_h >= J_min>0, 0 < H_* <= H_max, lambda_C>=lambda_min>0, and mu_C>=mu_min>0, then k_C >= lambda_min*mu_min*J_min^2/H_max^2",
            "this is the exact source-row contract for k_C_min",
            "KC_MIN_FORMULA_DERIVED_INPUTS_MISSING",
            True,
        ),
        (
            "LBT2077_3_failure_mode",
            "vanishing current mode",
            "if J_min=0 or H_max/lambda_min/mu_min is missing, the branch has k_C>=0 but no k_C_min>0",
            "silent/stationary caps can make I_tau vanish",
            "STRICT_COERCIVITY_NOT_AUTOMATIC",
            True,
        ),
        (
            "LBT2077_4_energy_bound_join",
            "finite energy-bound join",
            "X_E <= 0.5*(a + sqrt(a^2 + 4*F_outer_abs)), q_R_hat <= K_qR*X_E",
            "requires W_R_min,k_C_min,C_Poincare,C_trace,rho_R_norm,b_C_norm,F_outer_abs,K_qR",
            "SYMBOLIC_JOIN_ONLY",
            True,
        ),
        (
            "LBT2077_5_verdict",
            "2077 theorem status",
            "the lower-bound law is derived, but every theory-side input is still missing except the nonclaim external q_R ceiling",
            "no local-GR/PPN/R10 scoring allowed",
            "DERIVED_FORMULA_PARENT_SOURCES_MISSING",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, theorem_piece, formula, condition, status, theorem_step_valid in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "theorem_piece": theorem_piece,
                "formula": formula,
                "condition": condition,
                "status": status,
                "conditional_theorem_step_valid": theorem_step_valid,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def owner_input_audit_rows() -> list[dict[str, object]]:
    data = [
        (
            "OIA2077_0_Jmin",
            "J_min",
            "positive lower bound for ||J_tau^cap||_h",
            "requires parent J_tau cap current, cap norm h_C, tau/frame lock and nonzero support theorem or numeric source row",
            "MISSING_JTAU_CAP_NORM_LOWER_BOUND",
        ),
        (
            "OIA2077_1_Hmax",
            "H_max",
            "finite upper bound for positive H_* denominator",
            "requires same-frame H_tau/H_ref/M_H_ref source row and fixed reference; 1519 has MISSING_M_H_REF",
            "MISSING_HSTAR_UPPER_BOUND",
        ),
        (
            "OIA2077_2_lambda_min",
            "lambda_min",
            "positive lower bound for lambda_C",
            "requires parent level/unit coefficient fixed before readout",
            "MISSING_LAMBDA_C_MIN",
        ),
        (
            "OIA2077_3_mu_min",
            "mu_min",
            "positive lower bound for oriented cap measure density",
            "requires cap orientation, normal convention, corner/source split and geometry",
            "MISSING_MU_C_MIN_AND_ORIENTATION",
        ),
        (
            "OIA2077_4_Wmin",
            "W_R_min",
            "positive lower bound for reciprocal bulk operator",
            "04 writes W>0 as contract, but no numeric/source lower-bound row exists",
            "MISSING_W_R_MIN",
        ),
        (
            "OIA2077_5_KqR",
            "K_qR",
            "map from reciprocal energy norm/DeltaR to q_R_hat",
            "needs N_sphere, Z_R_infty, same-frame r_s, source mass calibration and orientation",
            "MISSING_K_QR_MAP",
        ),
        (
            "OIA2077_6_verdict",
            "owner input status",
            "the formula is ready but no owner input is ready for theory-side scoring",
            "source acquisition, not claim promotion, is the next move",
            "ALL_THEORY_INPUTS_MISSING",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, definition, required_source, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "definition": definition,
                "required_source": required_source,
                "status": status,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def acquisition_rows() -> list[dict[str, object]]:
    q_source = OUT / "P8_Y5_R10_1249_FINITE_QRHAT_CANDIDATE_RESULTS.csv"
    data = [
        ("ACQ2077_0_Jmin", "J_min", "||J_tau^cap||_h lower bound", "MISSING", "current norm units", "MISSING_JTAU_CAP_NORM_LOWER_BOUND", "source row or theorem-zero/nonzero certificate required"),
        ("ACQ2077_1_Hmax", "H_max", "upper bound for positive H_*", "MISSING", "energy units", "MISSING_HSTAR_UPPER_BOUND", "H_tau/H_ref/M_H_ref source row required"),
        ("ACQ2077_2_lambda_min", "lambda_min", "lambda_C lower bound", "MISSING", "W_R/length per I_tau/mu_C", "MISSING_LAMBDA_C_MIN", "parent level/coefficient row required"),
        ("ACQ2077_3_mu_min", "mu_min", "oriented cap measure lower bound", "MISSING", "cap measure units", "MISSING_MU_C_MIN", "orientation/geometry row required"),
        ("ACQ2077_4_kC_formula", "k_C_min_formula", "lambda_min*mu_min*J_min^2/H_max^2", "FORMULA_ONLY", "W_R/length units", "FORMULA_DERIVED_INPUTS_MISSING", "computed only after ACQ2077_0-3 are sourced"),
        ("ACQ2077_5_Wmin", "W_R_min", "bulk reciprocal operator lower bound", "MISSING", "W_R units", "MISSING_W_R_MIN", "parent reciprocal kinetic row required"),
        ("ACQ2077_6_CP", "C_Poincare", "annulus Poincare constant", "MISSING", "geometry units", "MISSING_GEOMETRY_CONSTANT", "fixed annulus geometry required"),
        ("ACQ2077_7_CT", "C_trace", "cap trace constant", "MISSING", "geometry units", "MISSING_TRACE_CONSTANT", "fixed cap/annulus geometry required"),
        ("ACQ2077_8_rho", "rho_R_norm", "bulk reciprocal source norm", "MISSING", "dual source units", "MISSING_BULK_SOURCE_NORM", "zero theorem or source-backed norm required"),
        ("ACQ2077_9_bC", "b_C_norm", "boundary/corner residue norm", "MISSING", "dual boundary units", "MISSING_BOUNDARY_RESIDUE_NORM", "boundary/corner component bound required"),
        ("ACQ2077_10_Fouter", "F_outer_abs", "outer/asymptotic flux absolute bound", "MISSING", "energy-like units", "MISSING_OUTER_FLUX_BOUND", "fixed outer boundary or flux row required"),
        ("ACQ2077_11_KqR", "K_qR", "energy norm to q_R_hat map", "MISSING", "dimensionless per norm", "MISSING_K_QR_MAP", "normalization chain required"),
        ("ACQ2077_12_qRceiling", "q_R_hat_policy_ceiling", "external nonclaim q_R_hat ceiling", "4.6e-05", "dimensionless", "SOURCE_BACKED_NONCLAIM_POLICY_CEILING", str(q_source)),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, definition, current_value, units, status, next_action in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "definition": definition,
                "current_value": current_value,
                "units": units,
                "status": status,
                "next_action": next_action,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def dry_run_rows() -> list[dict[str, object]]:
    data = [
        (
            "RUN2077_0_kmin_formula",
            "k_C_min lower-bound law",
            "PASS_FORMULA_ONLY",
            "k_C_min=lambda_min*mu_min*J_min^2/H_max^2 is derived under explicit positivity/lower-bound assumptions",
            False,
        ),
        (
            "RUN2077_1_numeric_theory_inputs",
            "theory-side energy-bound inputs",
            "FAIL_MISSING_INPUTS",
            "J_min,H_max,lambda_min,mu_min,W_R_min,geometry constants,source norms,F_outer,K_qR are missing",
            False,
        ),
        (
            "RUN2077_2_policy_ceiling",
            "q_R_hat policy ceiling",
            "PASS_NONCLAIM_COMPARATOR_ONLY",
            "4.6e-05 is available from QRHAT1255 but cannot substitute for q_R_hat_predicted",
            False,
        ),
        (
            "RUN2077_VERDICT",
            "source-owner acquisition",
            "LOWER_BOUND_FORMULA_DERIVED_SCORING_BLOCKED",
            "2078 should source J_min/Hmax/lambda_min/mu_min first or explicitly declare which one is impossible",
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
                "accepted_for_scoring": accepted_for_scoring,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2077_0_lower_bound_formula", "k_C_min formula derived", "PASS_FORMULA_ONLY", "formula is conditional and source inputs are missing"),
        ("GATE2077_1_Jmin", "J_tau cap norm lower bound sourced", "FAIL_BLOCKED", "J_min is missing"),
        ("GATE2077_2_Hmax", "Hstar upper/positive denominator sourced", "FAIL_BLOCKED", "H_max/H_* source row is missing"),
        ("GATE2077_3_lambda_mu", "lambda_C and mu_C lower bounds sourced", "FAIL_BLOCKED", "lambda_min/mu_min and orientation are missing"),
        ("GATE2077_4_runner", "finite energy-bound runner can score", "FAIL_BLOCKED", "theory-side numeric inputs and K_qR are missing"),
        ("GATE2077_5_local_claim", "local GR/Newton/PPN/R10 claim", "FAIL_BLOCKED", "no activated zero theorem and no finite q_R_hat prediction"),
        ("GATE2077_6_formalization", "formalization-workbench edit allowed", "PASS_NO_EDIT", "2077 stays in post-checkpoint-work"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update({"row_id": row_id, "gate": gate, "status": status, "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2077_0_formula", "KC_MIN_FORMULA_IS_NOW_EXACT_CONTRACT", "source rows must target J_min,H_max,lambda_min,mu_min rather than vague k_C"),
        ("DEC2077_1_no_shortcut", "POLICY_CEILING_IS_NOT_THEORY_PREDICTION", "4.6e-05 is useful only after q_R_hat_predicted exists"),
        ("DEC2077_2_order", "SOURCE_JMIN_AND_HMAX_FIRST", "without current norm and denominator bounds the positive-density route cannot become coercive"),
        ("DEC2077_3_fallback", "FINITE_INPUT_ACQUISITION_CONTINUES", "the branch is ready for source acquisition but not scoring"),
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
            "target_id": "NEXT2077_0_2078",
            "target_doc": "2078-Y5-R2FR-Jmin-Hmax-lambda-min-mu-min-first-source-rows-or-impossibility-ledger.md",
            "objective": "source or derive the first four lower-bound inputs for k_C_min: J_min, H_max, lambda_min, and mu_min; if any cannot be sourced, write an impossibility/finite fallback ledger before attempting runner scoring",
            "must_include": "J_tau cap norm source row; Hstar/M_H_ref upper and positivity row; lambda_C sign/units row; mu_C orientation/measure lower bound; k_C_min formula evaluator dry-run; no policy-ceiling-as-prediction",
            "excluded": "q_R_hat=0 closure; using QRHAT1255 as theory prediction; post-fit sign choice; raw Xi_tau; local-GR/PPN/R10 claim; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    theorem_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2077_0_source_weight_theorem", SOURCE_WEIGHT_DOCS / "AFRAME_KC_MIN_LOWER_BOUND_THEOREM_2077_NONCLAIM.csv", theorem_rows),
        ("COPY2077_1_source_weight_owner", SOURCE_WEIGHT_DOCS / "AFRAME_JTAU_HSTAR_LAMBDAC_OWNER_AUDIT_2077_NONCLAIM.csv", owner_rows),
        ("COPY2077_2_source_weight_acquisition", SOURCE_WEIGHT_DOCS / "AFRAME_ROBIN_ENERGY_INPUT_ACQUISITION_2077_NONCLAIM.csv", acquisition),
        ("COPY2077_3_wep_dry_run", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2077_LOWER_BOUND_DRY_RUN_NONCLAIM.csv", dry_rows_),
        ("COPY2077_4_queue_next", QUEUE / "JR2077_JMIN_HMAX_LAMBDAMIN_MUMIN_NEXT_NONCLAIM.csv", next_rows_),
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
    theorem_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    theorem_ok = any(row["row_id"] == "LBT2077_2_strict_bound" and row["status"] == "KC_MIN_FORMULA_DERIVED_INPUTS_MISSING" for row in theorem_rows)
    owner_ok = any(row["row_id"] == "OIA2077_6_verdict" and row["status"] == "ALL_THEORY_INPUTS_MISSING" for row in owner_rows)
    acquisition_ok = (
        any(row["row_id"] == "ACQ2077_4_kC_formula" and row["status"] == "FORMULA_DERIVED_INPUTS_MISSING" for row in acquisition)
        and any(row["row_id"] == "ACQ2077_12_qRceiling" and row["current_value"] == "4.6e-05" for row in acquisition)
        and all(row["ready_for_scoring"] is False for row in acquisition)
    )
    dry_ok = any(row["run_id"] == "RUN2077_VERDICT" and row["verdict"] == "LOWER_BOUND_FORMULA_DERIVED_SCORING_BLOCKED" for row in dry_rows_)
    gates_ok = all(row["claim_allowed"] is False and row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2077_0_2078"
    copies_ok = all(Path(str(row["path"])).exists() and csv_rows_parse(Path(str(row["path"]))) for row in copies)
    no_claim = all(
        not bool(row.get("claim_allowed", False)) and not bool(row.get("valid_for_claim", False))
        for group in [sources, theorem_rows, owner_rows, acquisition, dry_rows_, gates, next_rows_, copies]
        for row in group
    )
    checks = [
        ("VAL2077_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2077_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2077_02_lower_bound_formula", theorem_ok, "k_C_min lower-bound formula is derived as an input contract"),
        ("VAL2077_03_owner_inputs_missing", owner_ok, "owner input audit keeps all theory-side quantities blocked"),
        ("VAL2077_04_acquisition_rows", acquisition_ok, "acquisition rows stage formula and q_R ceiling without scoring"),
        ("VAL2077_05_dry_verdict", dry_ok, "dry run refuses scoring"),
        ("VAL2077_06_claim_gates_blocked", gates_ok, "all claim gates remain blocked/nonclaim"),
        ("VAL2077_07_next_selected", next_ok, "2078 first source-row target selected"),
        ("VAL2077_08_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2077_09_no_claim_flags", no_claim, "no generated row allows a claim"),
        ("VAL2077_10_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"),
        ("VAL2077_11_no_formalization_artifacts", not formalization_has_2077_artifacts(), "no 2077 artifacts were written under formalization-workbench"),
        ("VAL2077_12_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"),
    ]
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2077_OVERALL", overall, "2077 derives k_C_min formula but blocks scoring until source inputs exist"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2077 Y5 R2FR Jtau Cap Norm Hstar LambdaC Source Owner Or Energy Input Acquisition",
        "",
        "## Current Verdict",
        "",
        "2077 derives the exact lower-bound contract for the positive-density coupling. If",
        "",
        "`||J_tau^cap||_h >= J_min > 0`, `0 < H_* <= H_max`, `lambda_C >= lambda_min > 0`, and `mu_C >= mu_min > 0`,",
        "",
        "then",
        "",
        "`k_C >= k_C_min := lambda_min * mu_min * J_min^2 / H_max^2`.",
        "",
        "That is the clean formula we needed. It turns the vague coupling problem into four source rows: `J_min`, `H_max`, `lambda_min`, and `mu_min`. The formula does not make a local-GR claim because all four source rows are currently missing, and `W_R_min`, geometry constants, source norms, boundary residues, and `K_qR` are also missing.",
        "",
        "The existing `q_R_hat_policy_ceiling = 4.6e-05` remains useful only as a later comparator. It is not an MTS prediction and cannot be used until a theory-side `q_R_hat_predicted` exists.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, Kcap, q_R, or public claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Lower Bound Theorem",
        md_table(theorem_rows, ["row_id", "theorem_piece", "formula", "condition", "status", "conditional_theorem_step_valid", "ready_for_scoring", "claim_allowed"]),
        "## Owner Input Audit",
        md_table(owner_rows, ["row_id", "quantity", "definition", "required_source", "status", "ready_for_scoring", "claim_allowed"]),
        "## Energy Input Acquisition",
        md_table(acquisition, ["row_id", "quantity", "definition", "current_value", "units", "status", "next_action", "ready_for_scoring", "claim_allowed"]),
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
    theorem_rows = lower_bound_theorem_rows()
    owner_rows = owner_input_audit_rows()
    acquisition = acquisition_rows()
    dry_rows_ = dry_run_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2077_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2077_KC_MIN_LOWER_BOUND_THEOREM.csv",
        "owner": OUT / "P8_Y5_PARENT_QLOC_2077_OWNER_INPUT_AUDIT.csv",
        "acquisition": OUT / "P8_Y5_PARENT_QLOC_2077_ENERGY_INPUT_ACQUISITION.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2077_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2077_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2077_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2077_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2077_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2077_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["theorem"], theorem_rows)
    write_csv(paths["owner"], owner_rows)
    write_csv(paths["acquisition"], acquisition)
    write_csv(paths["dry"], dry_rows_)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(theorem_rows, owner_rows, acquisition, dry_rows_, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(row["path"])) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, theorem_rows, owner_rows, acquisition, dry_rows_, gates, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, theorem_rows, owner_rows, acquisition, dry_rows_, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
