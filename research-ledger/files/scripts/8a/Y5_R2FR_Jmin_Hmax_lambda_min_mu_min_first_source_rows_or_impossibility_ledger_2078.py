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


DOC = ROOT / "2078-Y5-R2FR-Jmin-Hmax-lambda-min-mu-min-first-source-rows-or-impossibility-ledger.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2078_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2078-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2078*",
        "*Y5_R2FR_Jmin_Hmax_lambda_min_mu_min_first_source_rows_or_impossibility_ledger_2078*",
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
            "SRC2078_00_2077_doc",
            ROOT / "2077-Y5-R2FR-Jtau-cap-norm-Hstar-lambdaC-source-owner-or-energy-input-acquisition.md",
            ["NEXT2077_0_2078", "J_min", "H_max", "lambda_min", "mu_min"],
            "2077 handoff to first lower-bound source rows.",
        ),
        (
            "SRC2078_01_2077_theorem",
            OUT / "P8_Y5_PARENT_QLOC_2077_KC_MIN_LOWER_BOUND_THEOREM.csv",
            ["LBT2077_2_strict_bound", "KC_MIN_FORMULA_DERIVED_INPUTS_MISSING", "STRICT_COERCIVITY_NOT_AUTOMATIC"],
            "k_C_min formula and vanishing-current failure mode.",
        ),
        (
            "SRC2078_02_2077_acquisition",
            OUT / "P8_Y5_PARENT_QLOC_2077_ENERGY_INPUT_ACQUISITION.csv",
            ["ACQ2077_0_Jmin", "ACQ2077_4_kC_formula", "ACQ2077_12_qRceiling"],
            "source acquisition rows for J/H/lambda/mu and policy ceiling.",
        ),
        (
            "SRC2078_03_1720_current_norm",
            ROOT / "1720-Y5-R2FR-observed-Hilbert-current-norm-source-row-or-matter-functor-signature.md",
            ["JHT1720_4_verdict", "CONDITIONAL_THEOREM_ONLY_NORM_NOT_SOURCED", "JHN1720_0_observed_Hilbert_current_norm_candidate"],
            "current norm route remains a template without norm/value/tau/source closure.",
        ),
        (
            "SRC2078_04_1519_mhref",
            OUT / "P8_Y5_PARENT_FRAME_1519_MHREF_FIRST_ROW_SCHEMA.csv",
            ["MHR1519_7_MHref", "MISSING_M_H_REF", "CLAIM_BLOCKED"],
            "Hstar/Hmax denominator source remains missing.",
        ),
        (
            "SRC2078_05_2062_boundary",
            OUT / "P8_Y5_PARENT_QLOC_2062_BOUNDARY_FUNCTIONAL_GRAMMAR.csv",
            ["BGA2062_4_orientation", "UNSIGNED_FOR_FINITE_SCORING", "Q_R = W_R n^mu partial_mu R_AB"],
            "mu_C orientation and finite scoring convention remain unsigned.",
        ),
        (
            "SRC2078_06_1008_variation",
            OUT / "P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv",
            ["PVA1008_2_J_tau", "formal_shape_no_owner", "piece_split_not_promoted"],
            "J_tau is formal only; parent theta/Q_tau is not extracted.",
        ),
        (
            "SRC2078_07_1101_level",
            ROOT / "1101-Y5-R10-gauge-fibre-level-index-monopole-Ward-owner-or-alpha-product-route.md",
            ["GNO1101_1_topological_level", "NO_EM_LEVEL_SOURCE", "GNO1101_4_Ward_identity"],
            "level/current-owner analogues are useful but not sourced as a cap stiffness owner.",
        ),
        (
            "SRC2078_08_1904_constructor",
            ROOT / "1904-Y5-R2FR-parent-action-constructor-exhaustion-or-action-scale-owner.md",
            ["CE1904_0_target", "PARENT_ACTION_CONSTRUCTOR_EXHAUSTION_NOT_DERIVED", "topological level"],
            "parent constructor exhaustion could allow fixed levels, but is not derived.",
        ),
        (
            "SRC2078_09_qrhat_policy",
            OUT / "P8_Y5_R10_1249_FINITE_QRHAT_CANDIDATE_RESULTS.csv",
            ["QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM", "4.6e-05", "ACCEPTED_NONCLAIM_FINITE_QRHAT"],
            "q_R_hat policy ceiling remains nonclaim comparator only.",
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


def first_source_attempt_rows() -> list[dict[str, object]]:
    data = [
        (
            "FSA2078_0_Jmin",
            "J_min",
            "positive lower bound for ||J_tau^cap||_h",
            "attempt theorem from positivity of norm",
            "fails: a norm is nonnegative but can vanish for a silent/stationary cap or zero cap-current branch",
            "GENERIC_POSITIVE_LOWER_BOUND_IMPOSSIBLE_WITHOUT_NONZERO_CURRENT_SOURCE",
            "need explicit nonzero cap-current support theorem or numeric source row",
        ),
        (
            "FSA2078_1_Hmax",
            "H_max",
            "finite upper bound for positive H_*",
            "search M_H_ref/H_tau/H_ref schemas",
            "1519 keeps H_tau,H_ref,M_H_ref and tau/frame lock missing",
            "MISSING_HSTAR_DENOMINATOR_SOURCE",
            "need same-frame H_tau/H_ref or H_* source row with fixed reference",
        ),
        (
            "FSA2078_2_lambda_min",
            "lambda_min",
            "positive lower bound for lambda_C",
            "search level/topological/coefficient owner routes",
            "level analogues exist in EM audits, but no cap-stiffness lambda_C source exists",
            "MISSING_LAMBDA_C_LEVEL_OR_COEFFICIENT",
            "need parent level/coefficient fixed before readout",
        ),
        (
            "FSA2078_3_mu_min",
            "mu_min",
            "positive lower bound for oriented cap measure",
            "compact geometry theorem: continuous positive measure density on fixed compact cap has positive infimum",
            "conditional theorem only; cap orientation/normal/corner/source split remains unsigned",
            "CONDITIONAL_GEOMETRIC_BOUND_NOT_PARENT_SIGNED",
            "need fixed cap geometry and orientation row",
        ),
        (
            "FSA2078_4_kCmin",
            "k_C_min",
            "lambda_min*mu_min*J_min^2/H_max^2",
            "formula evaluator",
            "blocked because J_min,Hmax,lambda_min,mu_min are not sourced and J_min may be zero",
            "FORMULA_READY_INPUTS_BLOCKED",
            "do not score until all four source rows are claim-ready",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, target, attempt, result, status, next_action in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "target": target,
                "attempt": attempt,
                "result": result,
                "status": status,
                "next_action": next_action,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def impossibility_rows() -> list[dict[str, object]]:
    data = [
        (
            "IMP2078_0_norm_zero",
            "J_min theorem from norm positivity",
            "||J||_h^2 >= 0 does not imply ||J||_h >= J_min>0",
            "zero current is legal unless parent action forbids silent cap current or supplies nonzero source support",
            "REJECT_GENERIC_JMIN_THEOREM",
        ),
        (
            "IMP2078_1_current_driven_stiffness",
            "strict stiffness from current density alone",
            "k_C=lambda_C mu_C ||J_tau^cap||^2/H_*^2 can vanish when J_tau^cap=0",
            "positive-density route signs nonnegativity, not strict Robin coercivity",
            "CURRENT_DENSITY_ALONE_NOT_STRICT",
        ),
        (
            "IMP2078_2_measure_only",
            "mu_min geometry as full solution",
            "mu_min>0 cannot compensate for J_min=0 or lambda_min missing",
            "geometry can support the formula but cannot generate current or level",
            "MEASURE_BOUND_INSUFFICIENT",
        ),
        (
            "IMP2078_3_policy_ceiling",
            "using QRHAT1255 as prediction",
            "4.6e-05 is an external ceiling, not q_R_hat[MTS]",
            "comparison may only occur after theory-side q_R_hat exists",
            "REJECT_POLICY_AS_PREDICTION",
        ),
        (
            "IMP2078_4_verdict",
            "strict current-density route",
            "unless J_min is sourced nonzero, strict Robin stiffness needs a separate floor/topological stiffness or finite noncoercive energy-bound branch",
            "this is a route-selection result, not a failure of the whole framework",
            "STRICT_CURRENT_ROUTE_BLOCKED_SELECT_FLOOR_OR_FINITE_BRANCH",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_id, reason, implication, verdict in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object_id": object_id,
                "reason": reason,
                "implication": implication,
                "verdict": verdict,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def floor_route_rows() -> list[dict[str, object]]:
    data = [
        (
            "KFR2078_0_floor_ansatz",
            "additive floor stiffness",
            "k_C := k_floor + lambda_C mu_C ||J_tau^cap||_h^2/H_*^2",
            "if k_floor>=k_floor_min>0, strict coercivity survives even when J_tau^cap=0",
            "BEST_REPAIR_CANDIDATE_NOT_SOURCED",
        ),
        (
            "KFR2078_1_topological_level",
            "topological/level floor",
            "k_floor could be a positive parent level, index, or protected cap modulus",
            "1101/1056 show level-style routes are possible analogues, but no cap-stiffness level source exists",
            "MISSING_CAP_LEVEL_SOURCE",
        ),
        (
            "KFR2078_2_mass_gap_floor",
            "local branch Hessian floor",
            "k_floor could descend from a parent Hessian/gap for R_AB-R_star",
            "would avoid relying on nonzero current; needs parent action Hessian source",
            "MISSING_PARENT_HESSIAN_FLOOR",
        ),
        (
            "KFR2078_3_finite_branch",
            "no strict floor",
            "set k_C_min=0 and use finite energy bound with outer boundary/Poincare/source norms",
            "valid as nonclaim fallback; cannot activate Robin zero theorem by cap stiffness alone",
            "FINITE_NONCOERCIVE_BRANCH_AVAILABLE",
        ),
        (
            "KFR2078_4_verdict",
            "route selection",
            "best next target is k_floor/topological-level owner first; if absent, continue finite energy input acquisition with k_C_min=0",
            "keeps derivation-first stance without smuggling current nonzero",
            "SELECT_KFLOOR_OR_FINITE_BRANCH_NEXT",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, route, formula, requirement, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "route": route,
                "formula": formula,
                "requirement": requirement,
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
        ("ACQ2078_0_Jmin", "J_min", "nonzero lower bound for cap current norm", "IMPOSSIBLE_AS_GENERIC_THEOREM", "needs nonzero source/support theorem or numeric row", "current norm units"),
        ("ACQ2078_1_Hmax", "H_max", "upper bound for positive H_*", "MISSING", "source H_tau/H_ref/M_H_ref with fixed reference", "energy units"),
        ("ACQ2078_2_lambda_min", "lambda_min", "positive lower bound for lambda_C", "MISSING", "source parent level/coefficient", "W_R/length per I_tau/mu_C"),
        ("ACQ2078_3_mu_min", "mu_min", "positive cap measure lower bound", "CONDITIONAL_GEOMETRY_ONLY", "source fixed cap geometry/orientation", "cap measure units"),
        ("ACQ2078_4_kfloor", "k_floor_min", "additive strict stiffness floor", "MISSING_REPAIR_INPUT", "source topological/level/Hessian floor or reject route", "W_R/length units"),
        ("ACQ2078_5_Wmin", "W_R_min", "bulk reciprocal lower bound", "MISSING", "source parent reciprocal kinetic lower bound", "W_R units"),
        ("ACQ2078_6_KqR", "K_qR", "energy norm to q_R_hat map", "MISSING", "source normalization chain", "dimensionless per norm"),
        ("ACQ2078_7_qRceiling", "q_R_hat_policy_ceiling", "external nonclaim q_R_hat ceiling", "4.6e-05", str(q_source), "dimensionless"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, definition, current_status, next_action, units in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "definition": definition,
                "current_status": current_status,
                "next_action": next_action,
                "units": units,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def dry_run_rows() -> list[dict[str, object]]:
    data = [
        (
            "RUN2078_0_four_sources",
            "J_min,H_max,lambda_min,mu_min source attempt",
            "FAIL_STRICT_ROUTE",
            "J_min is generically zero-allowed; Hmax/lambda_min missing; mu_min only conditional geometry",
            False,
        ),
        (
            "RUN2078_1_kfloor",
            "k_floor repair",
            "PASS_AS_NEXT_CANDIDATE_ONLY",
            "additive floor can repair strict coercivity if parent-sourced; no source yet",
            False,
        ),
        (
            "RUN2078_2_finite",
            "finite noncoercive branch",
            "PASS_SCHEMA_ONLY",
            "if k_floor fails, use k_C_min=0 with finite residual inputs and no zero theorem",
            False,
        ),
        (
            "RUN2078_VERDICT",
            "first source rows or impossibility ledger",
            "CURRENT_DENSITY_STRICT_ROUTE_BLOCKED_KFLOOR_OR_FINITE_NEXT",
            "2079 should try k_floor/topological/Hessian owner or explicitly demote strict Robin activation",
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
        ("GATE2078_0_Jmin", "J_min>0 sourced or derived", "FAIL_BLOCKED", "generic norm positivity cannot prove nonzero current"),
        ("GATE2078_1_Hmax", "Hmax sourced", "FAIL_BLOCKED", "Hstar/M_H_ref source remains missing"),
        ("GATE2078_2_lambda", "lambda_min sourced", "FAIL_BLOCKED", "no parent cap level/coefficient row exists"),
        ("GATE2078_3_mu", "mu_min parent-signed", "FAIL_BLOCKED", "only conditional compact-geometry theorem; orientation/cap source missing"),
        ("GATE2078_4_kfloor", "strict floor stiffness sourced", "FAIL_BLOCKED", "repair route selected but unsourced"),
        ("GATE2078_5_runner", "finite runner can score", "FAIL_BLOCKED", "theory-side q_R_hat prediction inputs missing"),
        ("GATE2078_6_local_claim", "local GR/Newton/PPN/R10 claim", "FAIL_BLOCKED", "no strict Robin activation or finite prediction"),
        ("GATE2078_7_formalization", "formalization-workbench edit allowed", "PASS_NO_EDIT", "2078 stays in post-checkpoint-work"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, gate, status, detail in data:
        row = base_row()
        row.update({"row_id": row_id, "gate": gate, "status": status, "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2078_0_Jmin", "DO_NOT_PRETEND_JMIN_POSITIVE", "a positive norm can vanish; strict current-density stiffness is not generic"),
        ("DEC2078_1_mu", "MU_MIN_IS_CONDITIONAL_GEOMETRY_ONLY", "compact positive measure can give a bound only after cap orientation/geometry is parent-signed"),
        ("DEC2078_2_repair", "SELECT_KFLOOR_REPAIR_OR_FINITE_BRANCH", "strict coercivity needs an additive floor/topological/Hessian owner or demotion to finite noncoercive bound"),
        ("DEC2078_3_claim", "NO_LOCAL_CLAIM", "q_R policy ceiling is still only a comparator"),
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
            "target_id": "NEXT2078_0_2079",
            "target_doc": "2079-Y5-R2FR-kfloor-topological-Hessian-owner-or-finite-noncoercive-Robin-demotion.md",
            "objective": "try to derive/source an additive strict floor stiffness k_floor from a topological level, parent Hessian/gap, or protected cap modulus; if no owner exists, demote strict Robin activation and keep only finite noncoercive energy-bound rows",
            "must_include": "k_floor ansatz; topological/level owner audit; parent Hessian/gap owner audit; cap geometry/orientation; k_C_min with floor; finite branch with k_C_min=0; q_R policy comparator guard",
            "excluded": "pretending J_min>0 follows from a norm; using QRHAT1255 as prediction; post-fit beta/lambda sign; raw Xi_tau; local-GR/PPN/R10 claim; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    source_attempts: list[dict[str, object]],
    impossibility: list[dict[str, object]],
    floor: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    dry: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2078_0_source_weight_attempts", SOURCE_WEIGHT_DOCS / "AFRAME_JMIN_HMAX_LAMBDA_MU_SOURCE_ATTEMPT_2078_NONCLAIM.csv", source_attempts),
        ("COPY2078_1_source_weight_impossibility", SOURCE_WEIGHT_DOCS / "AFRAME_JMIN_IMPOSSIBILITY_LEDGER_2078_NONCLAIM.csv", impossibility),
        ("COPY2078_2_source_weight_kfloor", SOURCE_WEIGHT_DOCS / "AFRAME_KFLOOR_REPAIR_ROUTE_2078_NONCLAIM.csv", floor),
        ("COPY2078_3_source_weight_acquisition", SOURCE_WEIGHT_DOCS / "AFRAME_2078_ENERGY_INPUT_ACQUISITION_NONCLAIM.csv", acquisition),
        ("COPY2078_4_wep_dry", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2078_DRY_RUN_NONCLAIM.csv", dry),
        ("COPY2078_5_queue_next", QUEUE / "JR2078_KFLOOR_OR_FINITE_BRANCH_NEXT_NONCLAIM.csv", next_rows_),
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
    attempts: list[dict[str, object]],
    impossibility: list[dict[str, object]],
    floor: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    dry: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    jmin_ok = any(row["row_id"] == "FSA2078_0_Jmin" and row["status"] == "GENERIC_POSITIVE_LOWER_BOUND_IMPOSSIBLE_WITHOUT_NONZERO_CURRENT_SOURCE" for row in attempts)
    mu_ok = any(row["row_id"] == "FSA2078_3_mu_min" and row["status"] == "CONDITIONAL_GEOMETRIC_BOUND_NOT_PARENT_SIGNED" for row in attempts)
    imp_ok = any(row["row_id"] == "IMP2078_4_verdict" and row["verdict"] == "STRICT_CURRENT_ROUTE_BLOCKED_SELECT_FLOOR_OR_FINITE_BRANCH" for row in impossibility)
    floor_ok = any(row["row_id"] == "KFR2078_4_verdict" and row["status"] == "SELECT_KFLOOR_OR_FINITE_BRANCH_NEXT" for row in floor)
    acq_ok = any(row["row_id"] == "ACQ2078_7_qRceiling" and row["current_status"] == "4.6e-05" for row in acquisition) and all(
        row["ready_for_scoring"] is False for row in acquisition
    )
    dry_ok = any(row["run_id"] == "RUN2078_VERDICT" and row["verdict"] == "CURRENT_DENSITY_STRICT_ROUTE_BLOCKED_KFLOOR_OR_FINITE_NEXT" for row in dry)
    gates_ok = all(row["claim_allowed"] is False and row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2078_0_2079"
    copies_ok = all(Path(str(row["path"])).exists() and csv_rows_parse(Path(str(row["path"]))) for row in copies)
    no_claim = all(
        not bool(row.get("claim_allowed", False)) and not bool(row.get("valid_for_claim", False))
        for group in [sources, attempts, impossibility, floor, acquisition, dry, gates, next_rows_, copies]
        for row in group
    )
    checks = [
        ("VAL2078_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2078_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2078_02_Jmin_impossibility", jmin_ok, "J_min generic positive lower bound is rejected without nonzero source support"),
        ("VAL2078_03_mu_conditional", mu_ok, "mu_min compact-geometry route is conditional but not parent signed"),
        ("VAL2078_04_impossibility_verdict", imp_ok, "strict current-density route is blocked"),
        ("VAL2078_05_kfloor_selected", floor_ok, "k_floor or finite branch selected next"),
        ("VAL2078_06_acquisition_rows", acq_ok, "acquisition rows remain nonclaim and preserve q_R policy ceiling as comparator"),
        ("VAL2078_07_dry_verdict", dry_ok, "dry run refuses scoring"),
        ("VAL2078_08_claim_gates_blocked", gates_ok, "all claim gates remain blocked/nonclaim"),
        ("VAL2078_09_next_selected", next_ok, "2079 k_floor/topological/Hessian route selected"),
        ("VAL2078_10_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2078_11_no_claim_flags", no_claim, "no generated row allows a claim"),
        ("VAL2078_12_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"),
        ("VAL2078_13_no_formalization_artifacts", not formalization_has_2078_artifacts(), "no 2078 artifacts were written under formalization-workbench"),
        ("VAL2078_14_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"),
    ]
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2078_OVERALL", overall, "2078 blocks strict current-density route and selects k_floor or finite branch"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    impossibility: list[dict[str, object]],
    floor: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    dry: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2078 Y5 R2FR Jmin Hmax Lambda Min Mu Min First Source Rows Or Impossibility Ledger",
        "",
        "## Current Verdict",
        "",
        "2078 tests the four-number contract from 2077. The result is useful but not claim-ready: `H_max`, `lambda_min`, and parent-signed `mu_min` are missing, while `J_min>0` is not generically derivable from a norm at all.",
        "",
        "A norm gives `||J_tau^cap||_h >= 0`, not `||J_tau^cap||_h >= J_min>0`. If the cap current can vanish on a silent/stationary branch, then the positive-density stiffness gives `k_C>=0` but no strict `k_C_min>0`. So the strict current-density Robin route is blocked unless a parent theorem or real source row forces nonzero cap current.",
        "",
        "The repair route is now explicit:",
        "",
        "`k_C := k_floor + lambda_C mu_C ||J_tau^cap||_h^2/H_*^2`.",
        "",
        "If `k_floor>=k_floor_min>0` comes from a parent topological level, Hessian/gap, or protected cap modulus, strict coercivity can survive even when `J_tau^cap=0`. If no such owner exists, the branch must be demoted to the finite noncoercive energy-bound route with `k_C_min=0`.",
        "",
        "The `q_R_hat_policy_ceiling=4.6e-05` remains only a nonclaim comparator. It is not an MTS prediction.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, Kcap, q_R, or public claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## First Source Attempt",
        md_table(attempts, ["row_id", "quantity", "target", "attempt", "result", "status", "next_action", "ready_for_scoring", "claim_allowed"]),
        "## Impossibility Ledger",
        md_table(impossibility, ["row_id", "object_id", "reason", "implication", "verdict", "claim_allowed"]),
        "## k_floor Repair Route",
        md_table(floor, ["row_id", "route", "formula", "requirement", "status", "ready_for_scoring", "claim_allowed"]),
        "## Acquisition Rows",
        md_table(acquisition, ["row_id", "quantity", "definition", "current_status", "next_action", "units", "ready_for_scoring", "claim_allowed"]),
        "## Dry Run",
        md_table(dry, ["run_id", "target", "verdict", "reason", "accepted_for_scoring", "claim_allowed"]),
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
    attempts = first_source_attempt_rows()
    impossibility = impossibility_rows()
    floor = floor_route_rows()
    acquisition = acquisition_rows()
    dry = dry_run_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2078_SOURCE_REGISTER.csv",
        "attempts": OUT / "P8_Y5_PARENT_QLOC_2078_FIRST_SOURCE_ATTEMPT.csv",
        "impossibility": OUT / "P8_Y5_PARENT_QLOC_2078_IMPOSSIBILITY_LEDGER.csv",
        "floor": OUT / "P8_Y5_PARENT_QLOC_2078_KFLOOR_REPAIR_ROUTE.csv",
        "acquisition": OUT / "P8_Y5_PARENT_QLOC_2078_ACQUISITION_ROWS.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2078_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2078_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2078_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2078_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2078_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2078_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["attempts"], attempts)
    write_csv(paths["impossibility"], impossibility)
    write_csv(paths["floor"], floor)
    write_csv(paths["acquisition"], acquisition)
    write_csv(paths["dry"], dry)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(attempts, impossibility, floor, acquisition, dry, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(row["path"])) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, attempts, impossibility, floor, acquisition, dry, gates, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, attempts, impossibility, floor, acquisition, dry, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
