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


DOC = ROOT / "2076-Y5-R2FR-positive-current-density-cap-functional-or-first-numeric-energy-bound-inputs.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2076_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2076-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2076*",
        "*Y5_R2FR_positive_current_density_cap_functional_or_first_numeric_energy_bound_inputs_2076*",
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
            "SRC2076_00_2075_doc",
            ROOT / "2075-Y5-R2FR-Xi-tau-current-owner-kC-positivity-or-Robin-energy-bound-runner.md",
            ["NEXT2075_0_2076", "I_tau>=0", "lambda_C"],
            "2075 handoff: construct positive current-density cap functional or fill first energy-bound inputs.",
        ),
        (
            "SRC2076_01_2075_density",
            OUT / "P8_Y5_PARENT_QLOC_2075_POSITIVE_CURRENT_DENSITY_CONTRACT.csv",
            ["PDC2075_0_density", "PDC2075_5_verdict", "CANDIDATE_PARENT_FUNCTIONAL_NOT_ADOPTED"],
            "positive-density cap contract from 2075.",
        ),
        (
            "SRC2076_02_2075_inputs",
            OUT / "P8_Y5_PARENT_QLOC_2075_ROBIN_ENERGY_BOUND_INPUT_TEMPLATE.csv",
            ["EBI2075_0_Wmin", "EBI2075_1_kmin", "EBI2075_8_qRlimit"],
            "energy-bound input placeholders from 2075.",
        ),
        (
            "SRC2076_03_2075_runner",
            OUT / "P8_Y5_PARENT_QLOC_2075_ROBIN_ENERGY_BOUND_RUNNER.csv",
            ["EBR2075_0_symbolic_law", "BLOCKED_MISSING_NUMERIC_INPUTS", "STRICT_NONCLAIM_UNTIL_INPUTS_FILLED"],
            "symbolic runner law and fail-closed claim rule.",
        ),
        (
            "SRC2076_04_1008_variation",
            OUT / "P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv",
            ["PVA1008_0_parent_action", "PVA1008_2_J_tau", "fail_current_claim"],
            "parent theta/J_tau extraction still not closed.",
        ),
        (
            "SRC2076_05_1007_symplectic",
            OUT / "P8_Y5_R10_1007_SYMPLECTIC_RESIDUAL_SCHEMA.csv",
            ["SRS1007_0_integrability_formula", "parent theta/Q_tau", "no MISSING markers"],
            "H_tau/fixed-reference residual schema requires parent theta/Q_tau and sourced denominator.",
        ),
        (
            "SRC2076_06_1519_mhref",
            OUT / "P8_Y5_PARENT_FRAME_1519_MHREF_FIRST_ROW_SCHEMA.csv",
            ["MHR1519_3_theta", "MHR1519_7_MHref", "CLAIM_BLOCKED"],
            "positive same-frame H_* denominator remains missing.",
        ),
        (
            "SRC2076_07_1519_lock",
            OUT / "P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv",
            ["OCF1519_4_tau_lock", "OCF1519_6_MHref_denominator", "COFRAME_TAU_LOCK_NOT_PROVED"],
            "tau/frame lock and denominator source are not parent signed.",
        ),
        (
            "SRC2076_08_2062_boundary",
            OUT / "P8_Y5_PARENT_QLOC_2062_BOUNDARY_FUNCTIONAL_GRAMMAR.csv",
            ["BGA2062_3_corner_worldtube", "BGA2062_4_orientation", "UNSIGNED_FOR_FINITE_SCORING"],
            "cap orientation/corner grammar remains unsigned.",
        ),
        (
            "SRC2076_09_1249_qrhat",
            OUT / "P8_Y5_R10_1249_FINITE_QRHAT_CANDIDATE_RESULTS.csv",
            ["QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM", "4.6e-05", "ACCEPTED_NONCLAIM_FINITE_QRHAT"],
            "first numeric policy ceiling for later q_R_hat comparison, not a theory prediction.",
        ),
        (
            "SRC2076_10_1720_current_norm",
            ROOT / "1720-Y5-R2FR-observed-Hilbert-current-norm-source-row-or-matter-functor-signature.md",
            ["JHT1720_4_verdict", "CONDITIONAL_THEOREM_ONLY_NORM_NOT_SOURCED", "observed Hilbert current norm"],
            "current/source norm route is conditional and unsourced.",
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


def positive_density_sign_rows() -> list[dict[str, object]]:
    data = [
        (
            "PDS2076_0_parent_current",
            "J_tau^cap",
            "J_tau^cap := pull_C(i_n J_tau) after fixed reference subtraction",
            "requires parent theta_MTS, L_parent, tau action, cap normal and reference lock",
            "CONDITIONAL_OBJECT_NOT_EXTRACTED",
            False,
        ),
        (
            "PDS2076_1_positive_inner_product",
            "h_C",
            "I_tau := <J_tau^cap,J_tau^cap>_{h_C}/H_*^2",
            "if h_C is a positive cap inner product and H_*>0, then I_tau>=0",
            "SIGN_THEOREM_CONDITIONAL",
            True,
        ),
        (
            "PDS2076_2_stiffness",
            "k_C",
            "k_C := lambda_C mu_C I_tau",
            "if lambda_C>=0 and mu_C is a positive oriented measure density, then k_C>=0",
            "NONNEGATIVE_STIFFNESS_CONDITIONAL",
            True,
        ),
        (
            "PDS2076_3_strict_lower_bound",
            "k_C_min",
            "k_C>=k_C_min>0 requires lambda_C_min>0, mu_C_min>0 and I_tau_min>0 on the cap",
            "I_tau may vanish for a silent/stationary cap, so nonnegative does not automatically mean strictly coercive",
            "STRICT_POSITIVITY_NOT_DERIVED",
            False,
        ),
        (
            "PDS2076_4_robin_use",
            "Robin fixed-point activation",
            "nonnegative k_C is useful in the energy identity; strict cap coercivity or fixed outer boundary is still needed to kill constant modes",
            "prevents overstating the positive-density route as a local-GR proof",
            "THEOREM_USE_LIMIT_IDENTIFIED",
            False,
        ),
        (
            "PDS2076_5_verdict",
            "positive-density sign theorem",
            "2076 derives the conditional sign-safe mechanism but cannot parent-adopt it or source k_C_min",
            "move to source rows for J_tau cap norm, H_*, lambda_C, mu_C orientation and geometry constants",
            "CONDITIONAL_SIGN_MECHANISM_DERIVED_PARENT_OWNER_MISSING",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_id, formula, condition, status, theorem_step_valid in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object_id": object_id,
                "formula": formula,
                "condition": condition,
                "status": status,
                "conditional_theorem_step_valid": theorem_step_valid,
                "parent_signed": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def parent_owner_audit_rows() -> list[dict[str, object]]:
    data = [
        (
            "POA2076_0_Jtau",
            "J_tau cap current",
            "theta_MTS/L_parent/tau action/source-reference subtraction",
            "1008 marks J_tau formal-shape-only and total parent action unpromoted",
            "MISSING_PARENT_JTAU_OWNER",
        ),
        (
            "POA2076_1_hC",
            "positive cap inner product h_C",
            "cap metric/coframe, normal, measure and positive norm convention",
            "no parent cap norm row exists; 2062 orientation/corner remains unsigned",
            "MISSING_CAP_NORM_OWNER",
        ),
        (
            "POA2076_2_Hstar",
            "positive denominator H_*",
            "same-frame H_tau/H_ref or M_H_ref source row",
            "1006/1519 keep M_H_ref positive same-frame denominator missing",
            "MISSING_POSITIVE_HSTAR_DENOMINATOR",
        ),
        (
            "POA2076_3_lambdaC",
            "lambda_C level/unit coefficient",
            "fixed before readout, nonnegative, unit-compatible conversion to W_R/length",
            "no lambda_C parent level/coefficient source row exists",
            "MISSING_LAMBDA_C_SOURCE",
        ),
        (
            "POA2076_4_muC",
            "mu_C positive orientation",
            "cap measure density, normal convention and corner joins",
            "2062 marks orientation and corner/worldtube terms unsigned",
            "MISSING_MU_C_ORIENTATION",
        ),
        (
            "POA2076_5_kmin",
            "strict k_C_min",
            "positive lower bound on lambda_C mu_C I_tau across cap support",
            "I_tau can be zero; no lower-bound theorem or numeric row exists",
            "MISSING_STRICT_KC_LOWER_BOUND",
        ),
        (
            "POA2076_6_verdict",
            "parent owner status",
            "all positive-density owner inputs are currently missing or conditional",
            "the sign theorem is a mechanism contract, not a local-GR activation certificate",
            "PARENT_OWNER_NOT_CLOSED",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_id, required_owner, evidence, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object_id": object_id,
                "required_owner": required_owner,
                "evidence": evidence,
                "status": status,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def first_energy_input_rows() -> list[dict[str, object]]:
    q_source = OUT / "P8_Y5_R10_1249_FINITE_QRHAT_CANDIDATE_RESULTS.csv"
    data = [
        ("FEI2076_0_Wmin", "W_R_min", "positive reciprocal bulk lower bound", "", "W_R units", "MISSING_PARENT_W_R_MIN", "MISSING", False),
        ("FEI2076_1_kmin", "k_C_min", "strict positive Robin stiffness lower bound", "", "W_R/length units", "MISSING_STRICT_KC_LOWER_BOUND", "MISSING", False),
        ("FEI2076_2_Imin", "I_tau_min", "positive current-density lower bound on cap support", "", "dimensionless after H_* normalization", "MISSING_I_TAU_LOWER_BOUND", "MISSING", False),
        ("FEI2076_3_lambdaC", "lambda_C", "nonnegative level/unit coefficient for cap stiffness", "", "W_R/length per I_tau/mu_C", "MISSING_LAMBDA_C_SOURCE", "MISSING", False),
        ("FEI2076_4_Hstar", "H_star", "positive same-frame denominator for current norm", "", "energy units", "MISSING_POSITIVE_HSTAR_DENOMINATOR", "MISSING", False),
        ("FEI2076_5_muC", "mu_C_orientation", "positive cap measure/orientation certificate", "", "area or cap measure units", "MISSING_CAP_ORIENTATION", "MISSING", False),
        ("FEI2076_6_CP", "C_Poincare", "annulus Poincare/coercivity constant", "", "geometry units", "MISSING_GEOMETRY_CONSTANT", "MISSING", False),
        ("FEI2076_7_CT", "C_trace", "cap trace constant", "", "geometry units", "MISSING_TRACE_CONSTANT", "MISSING", False),
        ("FEI2076_8_rho", "rho_R_norm", "bulk reciprocal source dual norm", "", "dual source units", "MISSING_BULK_SOURCE_NORM", "MISSING", False),
        ("FEI2076_9_bC", "b_C_norm", "cap boundary/source-reference residue norm", "", "dual boundary units", "MISSING_BOUNDARY_RESIDUE_NORM", "MISSING", False),
        ("FEI2076_10_Fouter", "F_outer_abs", "absolute outer/asymptotic flux", "", "energy-like units", "MISSING_OUTER_FLUX_BOUND", "MISSING", False),
        ("FEI2076_11_KqR", "K_qR", "map from reciprocal energy norm to q_R_hat", "", "dimensionless per norm", "MISSING_QRHAT_MAP", "MISSING", False),
        ("FEI2076_12_qRceiling", "q_R_hat_policy_ceiling", "external nonclaim q_R_hat comparison ceiling", "4.6e-05", "dimensionless", "SOURCE_BACKED_NONCLAIM_POLICY_CEILING", str(q_source), False),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, definition, value, units, status, source_path, ready in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "definition": definition,
                "value": value,
                "units": units,
                "status": status,
                "source_path": source_path,
                "ready_for_scoring": ready,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def symbolic_runner_rows(inputs: list[dict[str, object]]) -> list[dict[str, object]]:
    missing = [row["quantity"] for row in inputs if str(row["status"]).startswith("MISSING_")]
    data = [
        (
            "SRR2076_0_bound_law",
            "X_E bound",
            "a := C_Poincare*rho_R_norm + C_trace*b_C_norm; X_E <= 0.5*(a + sqrt(a^2 + 4*F_outer_abs))",
            "law retained from 2075",
            "SYMBOLIC_ONLY",
            False,
        ),
        (
            "SRR2076_1_policy_ceiling",
            "q_R_hat policy ceiling",
            "q_R_hat_policy_ceiling = 4.6e-05 from QRHAT1255 nonclaim policy row",
            "numeric comparison ceiling exists, but it is not an MTS prediction",
            "NUMERIC_POLICY_CEILING_AVAILABLE_NONCLAIM",
            False,
        ),
        (
            "SRR2076_2_missing_inputs",
            "runner input completeness",
            ";".join(str(item) for item in missing),
            "all listed quantities must be numeric/source-backed before scoring",
            "RUNNER_BLOCKED_MISSING_INPUTS",
            False,
        ),
        (
            "SRR2076_3_verdict",
            "dry-run verdict",
            "do not compute q_R_hat_predicted until W_R_min,k_C_min,source norms, geometry constants and K_qR are filled",
            "strict nonclaim runner output",
            "REFUSE_NUMERIC_SCORING",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for run_id, target, formula_or_value, note, status, accepted_for_scoring in data:
        row = base_row()
        row.update(
            {
                "run_id": run_id,
                "target": target,
                "formula_or_value": formula_or_value,
                "note": note,
                "status": status,
                "accepted_for_scoring": accepted_for_scoring,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2076_0_sign_theorem", "positive-density sign theorem", "PASS_CONDITIONAL_ONLY", "I_tau>=0 and k_C>=0 follow only if parent owns norm, denominator, lambda_C and cap orientation."),
        ("GATE2076_1_parent_adoption", "positive-density cap functional adopted by parent action", "FAIL_BLOCKED", "J_tau cap current, h_C, H_*, lambda_C and mu_C are not parent signed."),
        ("GATE2076_2_strict_kmin", "strict k_C_min>0 exists", "FAIL_BLOCKED", "nonnegative stiffness is not enough; I_tau may vanish and no lower-bound row exists."),
        ("GATE2076_3_numeric_runner", "Robin energy-bound runner can score", "FAIL_BLOCKED", "only q_R policy ceiling is numeric; theory-side prediction inputs are missing."),
        ("GATE2076_4_local_claim", "local GR/Newton/PPN/R10 claim", "FAIL_BLOCKED", "no activated zero theorem and no finite q_R_hat prediction."),
        ("GATE2076_5_formalization", "formalization-workbench edit allowed", "PASS_NO_EDIT", "2076 stays in post-checkpoint-work."),
    ]
    rows: list[dict[str, object]] = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update({"row_id": row_id, "gate": gate, "status": status, "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2076_0_mechanism", "POSITIVE_DENSITY_SIGN_MECHANISM_CONDITIONAL", "The positive-density route is mathematically cleaner than raw signed Xi_tau."),
        ("DEC2076_1_lower_bound", "NONNEGATIVE_IS_NOT_STRICT_COERCIVITY", "k_C>=0 does not by itself provide k_C_min>0 because I_tau can vanish."),
        ("DEC2076_2_first_numeric", "FIRST_NUMERIC_POLICY_CEILING_STAGED", "q_R_hat_policy_ceiling=4.6e-05 is carried as a nonclaim comparator, not a prediction."),
        ("DEC2076_3_next", "SOURCE_OWNER_INPUTS_NEXT", "The highest-value next target is J_tau cap norm, H_*, lambda_C and mu_C orientation."),
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
            "target_id": "NEXT2076_0_2077",
            "target_doc": "2077-Y5-R2FR-Jtau-cap-norm-Hstar-lambdaC-source-owner-or-energy-input-acquisition.md",
            "objective": "try to source or derive the four owner inputs that would adopt the positive-density cap functional: J_tau cap norm, positive H_*, nonnegative lambda_C, and mu_C orientation; otherwise acquire first numeric theory-side energy-bound rows",
            "must_include": "J_tau cap pullback; h_C norm convention; H_tau/H_ref or H_* denominator; lambda_C sign/units; mu_C orientation; k_C_min lower-bound test; W_R_min source; K_qR source; runner dry refusal",
            "excluded": "raw Xi_tau sign choice; non-smooth absolute value without norm; q_R_hat=0 closure; using policy ceiling as prediction; local-GR/PPN/R10 claim; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    sign_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    input_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2076_0_source_weight_sign", SOURCE_WEIGHT_DOCS / "AFRAME_POSITIVE_DENSITY_SIGN_THEOREM_2076_NONCLAIM.csv", sign_rows),
        ("COPY2076_1_source_weight_owner", SOURCE_WEIGHT_DOCS / "AFRAME_POSITIVE_DENSITY_PARENT_OWNER_AUDIT_2076_NONCLAIM.csv", owner_rows),
        ("COPY2076_2_source_weight_inputs", SOURCE_WEIGHT_DOCS / "AFRAME_ROBIN_FIRST_ENERGY_INPUTS_2076_NONCLAIM.csv", input_rows),
        ("COPY2076_3_wep_runner", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2076_SYMBOLIC_RUNNER_DRY_RUN_NONCLAIM.csv", runner_rows),
        ("COPY2076_4_queue_next", QUEUE / "JR2076_JTAU_HSTAR_LAMBDAC_OR_INPUTS_NEXT_NONCLAIM.csv", next_rows_),
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
    sign_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    input_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    sign_ok = any(row["row_id"] == "PDS2076_1_positive_inner_product" and row["status"] == "SIGN_THEOREM_CONDITIONAL" for row in sign_rows) and any(
        row["row_id"] == "PDS2076_3_strict_lower_bound" and row["status"] == "STRICT_POSITIVITY_NOT_DERIVED" for row in sign_rows
    )
    owner_ok = any(row["row_id"] == "POA2076_6_verdict" and row["status"] == "PARENT_OWNER_NOT_CLOSED" for row in owner_rows)
    q_numeric_ok = any(row["row_id"] == "FEI2076_12_qRceiling" and row["value"] == "4.6e-05" and row["status"] == "SOURCE_BACKED_NONCLAIM_POLICY_CEILING" for row in input_rows)
    missing_theory_inputs_ok = all(
        str(row["status"]).startswith("MISSING_")
        for row in input_rows
        if row["row_id"] != "FEI2076_12_qRceiling"
    )
    runner_ok = any(row["run_id"] == "SRR2076_3_verdict" and row["status"] == "REFUSE_NUMERIC_SCORING" for row in runner_rows)
    gates_ok = all(row["claim_allowed"] is False and row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2076_0_2077"
    copies_ok = all(Path(str(row["path"])).exists() and csv_rows_parse(Path(str(row["path"]))) for row in copies)
    no_claim = all(
        not bool(row.get("claim_allowed", False)) and not bool(row.get("valid_for_claim", False))
        for group in [sources, sign_rows, owner_rows, input_rows, runner_rows, gates, next_rows_, copies]
        for row in group
    )
    checks = [
        ("VAL2076_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2076_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2076_02_sign_theorem", sign_ok, "positive-density sign theorem is conditional and strict positivity is not derived"),
        ("VAL2076_03_parent_owner_blocked", owner_ok, "parent owner inputs remain missing"),
        ("VAL2076_04_qr_policy_numeric", q_numeric_ok, "first numeric q_R_hat policy ceiling is staged as nonclaim"),
        ("VAL2076_05_theory_inputs_missing", missing_theory_inputs_ok, "theory-side energy-bound inputs remain missing"),
        ("VAL2076_06_runner_refuses", runner_ok, "symbolic runner refuses numeric scoring"),
        ("VAL2076_07_claim_gates_blocked", gates_ok, "all claim gates remain blocked/nonclaim"),
        ("VAL2076_08_next_selected", next_ok, "2077 source-owner target selected"),
        ("VAL2076_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2076_10_no_claim_flags", no_claim, "no generated row allows a claim"),
        ("VAL2076_11_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"),
        ("VAL2076_12_no_formalization_artifacts", not formalization_has_2076_artifacts(), "no 2076 artifacts were written under formalization-workbench"),
        ("VAL2076_13_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"),
    ]
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2076_OVERALL", overall, "2076 derives the conditional positive-density sign mechanism and stages first nonclaim energy inputs"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    sign_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    input_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2076 Y5 R2FR Positive Current Density Cap Functional Or First Numeric Energy Bound Inputs",
        "",
        "## Current Verdict",
        "",
        "2076 gets one real mathematical step and one hard refusal. The sign-safe coupling mechanism is valid conditionally: if the parent action owns a cap current `J_tau^cap`, a positive cap inner product `h_C`, a positive same-frame denominator `H_*`, a nonnegative unit coefficient `lambda_C`, and a positive oriented cap measure `mu_C`, then",
        "",
        "`I_tau := <J_tau^cap,J_tau^cap>_{h_C}/H_*^2 >= 0` and `k_C := lambda_C mu_C I_tau >= 0`.",
        "",
        "That is cleaner than raw signed `Xi_tau`, but it still does not activate local GR. Nonnegative stiffness is not strict coercivity: `I_tau` can vanish, so `k_C_min>0` requires an additional lower-bound theorem or sourced row. Without that, the Robin theorem remains conditional and the finite energy-bound route remains the honest fallback.",
        "",
        "The first numeric row staged here is only a policy ceiling: `q_R_hat_policy_ceiling = 4.6e-05` from the existing QRHAT1255 nonclaim comparator. This is not an MTS prediction. All theory-side inputs such as `W_R_min`, `k_C_min`, `rho_R_norm`, `b_C_norm`, `F_outer_abs`, and `K_qR` remain missing.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, Kcap, q_R, or public claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Positive Density Sign Theorem",
        md_table(sign_rows, ["row_id", "object_id", "formula", "condition", "status", "conditional_theorem_step_valid", "parent_signed", "claim_allowed"]),
        "## Parent Owner Audit",
        md_table(owner_rows, ["row_id", "object_id", "required_owner", "evidence", "status", "ready_for_scoring", "claim_allowed"]),
        "## First Energy Bound Inputs",
        md_table(input_rows, ["row_id", "quantity", "definition", "value", "units", "status", "source_path", "ready_for_scoring", "claim_allowed"]),
        "## Symbolic Runner Dry Run",
        md_table(runner_rows, ["run_id", "target", "formula_or_value", "note", "status", "accepted_for_scoring", "claim_allowed"]),
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
    sign_rows = positive_density_sign_rows()
    owner_rows = parent_owner_audit_rows()
    input_rows = first_energy_input_rows()
    runner_rows = symbolic_runner_rows(input_rows)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2076_SOURCE_REGISTER.csv",
        "sign": OUT / "P8_Y5_PARENT_QLOC_2076_POSITIVE_DENSITY_SIGN_THEOREM.csv",
        "owner": OUT / "P8_Y5_PARENT_QLOC_2076_PARENT_OWNER_AUDIT.csv",
        "inputs": OUT / "P8_Y5_PARENT_QLOC_2076_FIRST_ENERGY_BOUND_INPUTS.csv",
        "runner": OUT / "P8_Y5_PARENT_QLOC_2076_SYMBOLIC_RUNNER_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2076_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2076_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2076_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2076_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2076_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["sign"], sign_rows)
    write_csv(paths["owner"], owner_rows)
    write_csv(paths["inputs"], input_rows)
    write_csv(paths["runner"], runner_rows)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(sign_rows, owner_rows, input_rows, runner_rows, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(row["path"])) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, sign_rows, owner_rows, input_rows, runner_rows, gates, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, sign_rows, owner_rows, input_rows, runner_rows, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
