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


DOC = ROOT / "2073-Y5-R2FR-reciprocal-fixed-point-and-quadratic-Bmix-origin-or-finite-cap-residual.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2073_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2073-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2073*",
        "*Y5_R2FR_reciprocal_fixed_point_and_quadratic_Bmix_origin_or_finite_cap_residual_2073*",
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
            "SRC2073_00_2072_doc",
            ROOT / "2072-Y5-R2FR-Bmix-cap-functional-or-parent-current-chain-theta-Qtau.md",
            ["NEXT2072_0_2073", "f_prime(0)=0", "K_cap_to_PiR"],
            "2072 handoff: reciprocal fixed point plus quadratic/topological Bmix origin or finite residual.",
        ),
        (
            "SRC2073_01_2072_next",
            OUT / "P8_Y5_PARENT_QLOC_2072_NEXT_TARGET.csv",
            ["NEXT2072_0_2073", "Rstar theorem", "finite residual fallback"],
            "machine-readable 2073 target.",
        ),
        (
            "SRC2073_02_2072_theorem",
            OUT / "P8_Y5_PARENT_QLOC_2072_BMIX_GENERIC_VARIATION_THEOREM.csv",
            ["BVT2072_3_local_silence_condition", "DOUBLE_ZERO_SELECTION_LAW_DERIVED", "BVT2072_4_quadratic_minimum"],
            "Bmix double-zero theorem.",
        ),
        (
            "SRC2073_03_2072_selection",
            OUT / "P8_Y5_PARENT_QLOC_2072_DOUBLE_ZERO_SELECTION_LAW.csv",
            ["DZS2072_1_linear", "FAIL_LOCAL_CAP_SILENCE", "DZS2072_2_quadratic"],
            "constant/linear fail and quadratic passes conditionally.",
        ),
        (
            "SRC2073_04_2072_residual",
            OUT / "P8_Y5_PARENT_QLOC_2072_FINITE_RESIDUAL_EXPANSION.csv",
            ["FRE2072_0_quadratic_PiR", "FRE2072_1_quadratic_Ntau", "FRE2072_2_Kcap_ratio_warning"],
            "finite scaling and ratio warning from quadratic Bmix.",
        ),
        (
            "SRC2073_05_1248_doc",
            ROOT / "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check.md",
            ["REJECT_ZERO_THEOREM_UNDERIVED", "H_core and canonical brackets", "Q_R=0 theorem accepted"],
            "lambda_R hard-constraint ansatz rejected as underived.",
        ),
        (
            "SRC2073_06_1248_ansatz",
            OUT / "P8_Y5_R10_1248_MINIMAL_PARENT_ACTION_ANSATZ.csv",
            ["ANS1248_1_action", "SCHEMATIC_ACTION_ONLY", "DESIGN_CHOICE_NOT_THEOREM"],
            "minimal lambda_R action rows.",
        ),
        (
            "SRC2073_07_1249_finite",
            ROOT / "1249-Y5-R10-finite-qRhat-source-acquisition-and-policy-runner.md",
            ["ACCEPTED_NONCLAIM_FINITE_QRHAT", "REJECT_ZERO_THEOREM_UNDERIVED", "MISSING_PARENT_COEFFICIENT_MAP"],
            "finite q_R_hat fallback is runnable but nonclaim.",
        ),
        (
            "SRC2073_08_cell_current",
            ROOT / "11-cell-current-origin-attempt.md",
            ["W partial_r R_AB = Q_R.", "R_AB = -Q_R/r.", "gives a Ward identity, not R_AB=0."],
            "ordinary conserved reciprocal current leaves Q_R hair.",
        ),
        (
            "SRC2073_09_boundary_grammar",
            OUT / "P8_Y5_PARENT_QLOC_2062_BOUNDARY_FUNCTIONAL_GRAMMAR.csv",
            ["BGA2062_1_natural_variation", "BGA2062_3_corner_worldtube", "BGA2062_4_orientation"],
            "boundary variation/orientation/corner debts.",
        ),
        (
            "SRC2073_10_qR_guard",
            OUT / "P8_Y5_PARENT_QLOC_2063_FINITE_PIR_COMPONENT_INTAKE.csv",
            ["PCI2063_3_corner_bound", "PCI2063_4_total_join", "PCI2063_5_qR_Cassini_join"],
            "Pi_R absolute join and q_R guard.",
        ),
        (
            "SRC2073_11_theta_Qtau",
            OUT / "P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv",
            ["QTA1008_0_L_parent", "QTA1008_2_J_tau", "QTA1008_8_Q_total"],
            "Xi_tau/theta-Q_tau current owner remains upstream.",
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


def robin_fixed_point_rows() -> list[dict[str, object]]:
    data = [
        (
            "RFT2073_0_setup",
            "local exterior reciprocal field",
            "DeltaR := R_AB - R_star on a compact-source exterior annulus A with cap C_cap and outer fixed/asymptotic boundary",
            "static/local elliptic branch; no source support in A",
            "SETUP_CONDITIONAL",
            True,
        ),
        (
            "RFT2073_1_bulk_equation",
            "positive reciprocal bulk operator",
            "div(W_R grad DeltaR)=rho_R with W_R>0; theorem route takes rho_R=0 in the local vacuum exterior",
            "if rho_R is nonzero, use finite residual row instead of zero theorem",
            "MISSING_PARENT_BULK_R_OPERATOR",
            False,
        ),
        (
            "RFT2073_2_quadratic_cap",
            "quadratic mixed cap term",
            "B_mix,C = 1/2 integral_Ccap k_C DeltaR^2 dSigma_C, with k_C = 2 beta_mix c2 Xi_tau mu_C in the 2072 notation",
            "parent signs k_C>=k_min>=0 and fixes source/reference cap split",
            "MISSING_PARENT_POSITIVE_BMIX_STIFFNESS",
            False,
        ),
        (
            "RFT2073_3_robin_boundary",
            "cap variation",
            "W_R n^a grad_a DeltaR + k_C DeltaR = b_C on C_cap",
            "zero theorem route uses b_C=0; finite route keeps b_C as residual boundary source",
            "ROBIN_CONDITION_DERIVED_IF_BULK_AND_CAP_PARENT_SIGNED",
            True,
        ),
        (
            "RFT2073_4_energy_identity",
            "Robin uniqueness identity",
            "integral_A W_R |grad DeltaR|^2 + integral_Ccap k_C DeltaR^2 = outer_flux + integral_A DeltaR rho_R + integral_Ccap DeltaR b_C",
            "with outer_flux=rho_R=b_C=0 and W_R,k_C nonnegative, DeltaR has zero gradient and zero cap value",
            "EXACT_CONDITIONAL_ENERGY_IDENTITY",
            True,
        ),
        (
            "RFT2073_5_fixed_point_result",
            "R_AB=R_star theorem",
            "if W_R>0, k_C>=0 with enough cap support, rho_R=0, b_C=0, and outer DeltaR=0, then DeltaR=0 throughout A",
            "this kills the conserved Q_R/r hair without inserting lambda_R C_R by hand",
            "CONDITIONAL_RECIPROCAL_FIXED_POINT_THEOREM",
            True,
        ),
        (
            "RFT2073_6_verdict",
            "2073 theorem status",
            "quadratic Bmix can provide a genuine Robin fixed-point mechanism, but the parent action has not signed W_R,k_C,Xi_tau,b_C=0 or cap geometry",
            "better than closure, not yet evidence",
            "THEOREM_SHAPE_DERIVED_PARENT_CERTIFICATES_MISSING",
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
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def bmix_origin_audit_rows() -> list[dict[str, object]]:
    data = [
        (
            "BOA2073_0_bulk_owner",
            "W_R positive bulk reciprocal operator",
            "source equation for positive reciprocal-energy sector and no kinetic sign ghost",
            "MISSING_PARENT_BULK_R_OPERATOR",
            "needed for energy identity positivity",
        ),
        (
            "BOA2073_1_Rstar_owner",
            "R_star fixed reference",
            "R_star is fixed before source/readout, ideally zero/asymptotic reciprocity with no Q_R hair",
            "MISSING_PARENT_RSTAR_REFERENCE",
            "1248 rejects closure zero; 1249 keeps finite fallback",
        ),
        (
            "BOA2073_2_Bmix_owner",
            "quadratic/topological Bmix origin",
            "parent action supplies B_mix,C=1/2 int k_C DeltaR^2 or an exact/topological equivalent",
            "MISSING_PARENT_BMIX_ACTION_SOURCE",
            "2072 selected shape but did not source it",
        ),
        (
            "BOA2073_3_kC_positivity",
            "cap stiffness k_C",
            "k_C=2 beta_mix c2 Xi_tau mu_C is nonnegative with units and lower-bound convention",
            "MISSING_KC_POSITIVITY_UNITS",
            "linear route fails; quadratic route needs sign and units",
        ),
        (
            "BOA2073_4_Xi_tau_owner",
            "Xi_tau current scalar",
            "Xi_tau descends from parent theta_MTS/Q_tau^MTS or source-current chain",
            "MISSING_PARENT_THETA_QTAU_CURRENT_SCALAR",
            "1008 charge pieces remain unpromoted",
        ),
        (
            "BOA2073_5_cap_geometry",
            "C_cap geometry and orientation",
            "cap surface, measure, normal, corner joins and source/reference split are fixed",
            "MISSING_CAP_GEOMETRY_AND_CORNER_AUDIT",
            "2062/2063 still block finite scoring",
        ),
        (
            "BOA2073_6_boundary_source_silence",
            "b_C and outer flux",
            "all boundary/source/reference residues vanish by theorem or are retained as finite residuals",
            "MISSING_BOUNDARY_SOURCE_SILENCE",
            "prevents hidden cancellation",
        ),
        (
            "BOA2073_7_verdict",
            "Bmix/Rstar origin",
            "current corpus supports the Robin theorem shape but not the parent certificates required to activate it",
            "PARENT_ORIGIN_NOT_CLOSED",
            "next target should source/derive W_R,k_C,Xi_tau,b_C and q_R normalization",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_id, required_evidence, status, note in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object_id": object_id,
                "required_evidence": required_evidence,
                "status": status,
                "note": note,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def finite_residual_template_rows() -> list[dict[str, object]]:
    data = [
        (
            "FCT2073_0_energy_residual",
            "E_R_cap",
            "E_R_cap := integral_A W_R |grad DeltaR|^2 + integral_Ccap k_C DeltaR^2",
            "reciprocal-energy units",
            "bounded by outer_flux + integral_A DeltaR rho_R + integral_Ccap DeltaR b_C",
            "MISSING_NUMERIC_RESIDUAL_SOURCES",
        ),
        (
            "FCT2073_1_bulk_source",
            "rho_R",
            "bulk reciprocal source in div(W_R grad DeltaR)=rho_R",
            "reciprocal-source units",
            "must be zero theorem or numeric/source bounded",
            "MISSING_BULK_R_SOURCE_BOUND",
        ),
        (
            "FCT2073_2_cap_source",
            "b_C",
            "uncancelled cap/source/reference boundary residue in Robin condition",
            "boundary-current units",
            "must be zero theorem or absolute-bounded",
            "MISSING_CAP_BOUNDARY_SOURCE_BOUND",
        ),
        (
            "FCT2073_3_cap_stiffness",
            "k_C",
            "positive cap stiffness from beta_mix,c2,Xi_tau,mu_C",
            "W_R/length units",
            "must include sign, lower bound, source path and equation ref",
            "MISSING_KC_SOURCE_ROW",
        ),
        (
            "FCT2073_4_DeltaR_to_qR",
            "DeltaR/q_R_hat",
            "map DeltaR exterior amplitude to dimensionless q_R_hat and PPN gamma projection",
            "dimensionless after GM/source convention",
            "must use 1249/1244 policy fields and reject closure zero",
            "MISSING_QR_NORMALIZATION_CHAIN",
        ),
        (
            "FCT2073_5_no_ratio_only",
            "K_cap_to_PiR guard",
            "track absolute Pi_R, N_tau and q_R components separately; do not score by K ratio only",
            "mixed",
            "2072 showed K can diverge near double zero",
            "RATIO_ONLY_SCORING_REJECTED",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, definition, units, scoring_rule, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "definition": definition,
                "units": units,
                "scoring_rule": scoring_rule,
                "status": status,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def dry_run_rows() -> list[dict[str, object]]:
    data = [
        (
            "RUN2073_0_robin_theorem",
            "quadratic Bmix Robin fixed-point theorem",
            "PASS_CONDITIONAL_THEOREM",
            "energy identity derives DeltaR=0 if W_R,k_C,rho_R,b_C,outer boundary and cap geometry are parent-signed",
            False,
        ),
        (
            "RUN2073_1_lambda_comparison",
            "lambda_R hard constraint comparison",
            "ROBIN_ROUTE_LESS_SMUGGLED_THAN_LAMBDAR",
            "does not insert C_R=0 directly; it stabilizes the reciprocal hair through a positive boundary operator",
            False,
        ),
        (
            "RUN2073_2_parent_origin",
            "parent certificates",
            "FAIL_PARENT_CERTIFICATES_MISSING",
            "W_R,k_C,Xi_tau,b_C=0, source/reference split and q_R normalization remain unsigned",
            False,
        ),
        (
            "RUN2073_VERDICT",
            "Rstar and quadratic Bmix origin",
            "ROBIN_FIXED_POINT_THEOREM_DERIVED_PARENT_ORIGIN_MISSING",
            "2074 should try to source W_R/k_C/Xi_tau positivity and boundary silence, or fill finite residual rows.",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for run_id, target, verdict, reason, accepted in data:
        row = base_row()
        row.update(
            {
                "run_id": run_id,
                "target": target,
                "verdict": verdict,
                "reason": reason,
                "accepted_for_scoring": accepted,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        (
            "GATE2073_0_robin_theorem",
            "Robin fixed-point theorem may be used internally",
            "PASS_CONDITIONAL_THEOREM",
            "the energy identity is a valid conditional derivation shape",
        ),
        (
            "GATE2073_1_parent_W_R",
            "positive W_R bulk reciprocal sector is parent-signed",
            "FAIL_BLOCKED",
            "bulk reciprocal operator and sign are not sourced",
        ),
        (
            "GATE2073_2_parent_kC",
            "positive quadratic Bmix cap stiffness is parent-signed",
            "FAIL_BLOCKED",
            "k_C/beta_mix/c2/Xi_tau/measure source and units are missing",
        ),
        (
            "GATE2073_3_boundary_silence",
            "rho_R,b_C,outer flux and corner terms vanish or are bounded",
            "FAIL_BLOCKED",
            "boundary/corner/source-reference audit remains open",
        ),
        (
            "GATE2073_4_qR_score",
            "finite q_R/PPN scoring can use the theorem branch",
            "FAIL_BLOCKED",
            "q_R normalization and absolute Pi_R component join remain incomplete",
        ),
        (
            "GATE2073_5_local_GR",
            "local GR/Newton/PPN/R10 branch can claim pass",
            "FAIL_BLOCKED",
            "conditional Robin theorem is not parent-signed and finite residual rows are missing",
        ),
        (
            "GATE2073_6_formalization",
            "formalization-workbench edit allowed",
            "PASS_NO_EDIT",
            "2073 is contained in post-checkpoint-work",
        ),
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
            "DEC2073_0_real_leap",
            "QUADRATIC_BMIX_CAN_DERIVE_RSTAR_CONDITIONALLY",
            "A positive quadratic cap term gives a Robin uniqueness theorem for the reciprocal fixed point.",
        ),
        (
            "DEC2073_1_better_than_lambda",
            "ROBIN_ROUTE_IS_LESS_CLOSURE_LIKE_THAN_LAMBDAR",
            "lambda_R inserts C_R=0 directly; Robin Bmix kills hair through positivity and boundary variation if parent-signed.",
        ),
        (
            "DEC2073_2_no_claim",
            "DO_NOT_PROMOTE_LOCAL_GR",
            "the parent action still has to source W_R,k_C,Xi_tau,boundary silence and q_R normalization.",
        ),
        (
            "DEC2073_3_best_next",
            "TARGET_POSITIVITY_AND_BOUNDARY_SILENCE",
            "the next highest-value move is to prove/source W_R>0, k_C>=0, Xi_tau ownership and b_C=0; fallback is finite residual acquisition.",
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
            "target_id": "NEXT2073_0_2074",
            "target_doc": "2074-Y5-R2FR-Robin-Bmix-positivity-and-boundary-silence-or-finite-residual-fill.md",
            "objective": "prove/source the parent certificates that activate the Robin fixed-point theorem: W_R>0, k_C>=0 from quadratic Bmix, Xi_tau ownership, rho_R=b_C=0 or bounded, cap geometry, and q_R normalization",
            "must_include": "bulk reciprocal operator W_R; positive cap stiffness k_C; Xi_tau from theta_MTS/Q_tau; cap orientation/measure; source/reference split; boundary/corner silence; finite residual rows for rho_R,b_C,DeltaR; q_R_hat policy feed",
            "excluded": "lambda_R closure as derivation; R_AB=0 by assertion; linear Bmix coupling; Kcap ratio-only scoring; fitted reference; orbital GM import; cancellation; local-GR/PPN/R10 claim; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    theorem_rows: list[dict[str, object]],
    origin_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2073_0_source_weight_robin_theorem",
            SOURCE_WEIGHT_DOCS / "AFRAME_ROBIN_BMIX_FIXED_POINT_THEOREM_2073_NONCLAIM.csv",
            theorem_rows,
        ),
        (
            "COPY2073_1_source_weight_origin_audit",
            SOURCE_WEIGHT_DOCS / "AFRAME_ROBIN_BMIX_ORIGIN_AUDIT_2073_NONCLAIM.csv",
            origin_rows,
        ),
        (
            "COPY2073_2_source_weight_residual_template",
            SOURCE_WEIGHT_DOCS / "AFRAME_ROBIN_BMIX_FINITE_RESIDUAL_TEMPLATE_2073_NONCLAIM.csv",
            residual_rows,
        ),
        (
            "COPY2073_3_wep_dry_run",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2073_ROBIN_BMIX_DRY_RUN_NONCLAIM.csv",
            dry_rows_,
        ),
        (
            "COPY2073_4_queue_next",
            QUEUE / "JR2073_ROBIN_BMIX_POSITIVITY_OR_FINITE_RESIDUAL_NEXT_NONCLAIM.csv",
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
    theorem_rows: list[dict[str, object]],
    origin_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    theorem_ok = (
        any(row["row_id"] == "RFT2073_4_energy_identity" and row["status"] == "EXACT_CONDITIONAL_ENERGY_IDENTITY" for row in theorem_rows)
        and any(row["row_id"] == "RFT2073_5_fixed_point_result" and row["status"] == "CONDITIONAL_RECIPROCAL_FIXED_POINT_THEOREM" for row in theorem_rows)
        and any(row["row_id"] == "RFT2073_6_verdict" and row["status"] == "THEOREM_SHAPE_DERIVED_PARENT_CERTIFICATES_MISSING" for row in theorem_rows)
    )
    origin_ok = (
        any(row["row_id"] == "BOA2073_0_bulk_owner" and row["status"] == "MISSING_PARENT_BULK_R_OPERATOR" for row in origin_rows)
        and any(row["row_id"] == "BOA2073_3_kC_positivity" and row["status"] == "MISSING_KC_POSITIVITY_UNITS" for row in origin_rows)
        and any(row["row_id"] == "BOA2073_7_verdict" and row["status"] == "PARENT_ORIGIN_NOT_CLOSED" for row in origin_rows)
        and all(not bool(row["ready_for_scoring"]) for row in origin_rows)
    )
    residual_ok = (
        any(row["row_id"] == "FCT2073_0_energy_residual" for row in residual_rows)
        and any(row["row_id"] == "FCT2073_5_no_ratio_only" and row["status"] == "RATIO_ONLY_SCORING_REJECTED" for row in residual_rows)
        and all(not bool(row["ready_for_scoring"]) for row in residual_rows)
    )
    dry_ok = any(
        row["run_id"] == "RUN2073_VERDICT"
        and row["verdict"] == "ROBIN_FIXED_POINT_THEOREM_DERIVED_PARENT_ORIGIN_MISSING"
        and not bool(row["accepted_for_scoring"])
        for row in dry_rows_
    )
    gates_ok = all(row["claim_allowed"] is False and row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2073_0_2074"
    copies_ok = all(Path(str(row["path"])).exists() and csv_rows_parse(Path(str(row["path"]))) for row in copies)
    no_claim = all(
        not bool(row.get("claim_allowed", False)) and not bool(row.get("valid_for_claim", False))
        for group in [sources, theorem_rows, origin_rows, residual_rows, dry_rows_, gates, next_rows_, copies]
        for row in group
    )
    checks = [
        ("VAL2073_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2073_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2073_02_robin_theorem", theorem_ok, "Robin energy identity and conditional fixed-point theorem are written"),
        ("VAL2073_03_origin_audit", origin_ok, "parent origin/positivity/Xi/cap debts are explicit and nonclaim"),
        ("VAL2073_04_finite_residual_template", residual_ok, "finite residual template and no-ratio-only guard are staged"),
        ("VAL2073_05_dry_verdict", dry_ok, "dry run refuses scoring while preserving theorem progress"),
        ("VAL2073_06_claim_gates_blocked", gates_ok, "all local claim gates remain blocked/nonclaim"),
        ("VAL2073_07_next_selected", next_ok, "2074 positivity/boundary-silence target selected"),
        ("VAL2073_08_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2073_09_no_claim_flags", no_claim, "no generated row allows a claim"),
        ("VAL2073_10_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"),
        ("VAL2073_11_no_formalization_artifacts", not formalization_has_2073_artifacts(), "no 2073 artifacts were written under formalization-workbench"),
        ("VAL2073_12_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"),
    ]
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2073_OVERALL", overall, "2073 derives a conditional Robin Bmix fixed-point mechanism without promoting local claims"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    origin_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2073 Y5 R2FR Reciprocal Fixed Point And Quadratic Bmix Origin Or Finite Cap Residual",
        "",
        "## Current Verdict",
        "",
        "2073 finds a better derivation route than the hard `lambda_R R_AB` closure. A positive quadratic `B_mix` cap term acts as a Robin boundary operator for `DeltaR = R_AB - R_star`. If the parent action signs a positive reciprocal bulk operator `W_R`, positive cap stiffness `k_C`, no local reciprocal source `rho_R`, no uncancelled boundary residue `b_C`, and fixed outer/cap geometry, the energy identity forces `DeltaR=0` in the local exterior.",
        "",
        "That is a genuine theorem-shaped mechanism: it kills the conserved `Q_R/r` reciprocal hair by positivity and boundary variation, not by directly inserting `R_AB=0` as a multiplier constraint. It is therefore a cleaner route than the lambda branch if the missing parent certificates can be supplied.",
        "",
        "It is still not a local-GR claim. The current corpus has not parent-signed `W_R`, `k_C=2 beta_mix c2 Xi_tau mu_C`, `Xi_tau` from `theta_MTS/Q_tau^MTS`, cap orientation/measure, source/reference split, or boundary/corner silence. If any of those remain unsigned, the branch becomes a finite residual acquisition problem rather than a theorem-zero.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, Kcap, MHref, q_R, or public claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Robin Fixed Point Theorem",
        md_table(theorem_rows, ["row_id", "object_id", "formula", "condition", "status", "conditional_theorem_step_valid", "ready_for_scoring", "claim_allowed"]),
        "## Bmix Origin Audit",
        md_table(origin_rows, ["row_id", "object_id", "required_evidence", "status", "note", "ready_for_scoring", "claim_allowed"]),
        "## Finite Cap Residual Template",
        md_table(residual_rows, ["row_id", "quantity", "definition", "units", "scoring_rule", "status", "ready_for_scoring", "claim_allowed"]),
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
    theorem_rows = robin_fixed_point_rows()
    origin_rows = bmix_origin_audit_rows()
    residual_rows = finite_residual_template_rows()
    dry_rows_ = dry_run_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2073_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2073_ROBIN_FIXED_POINT_THEOREM.csv",
        "origin": OUT / "P8_Y5_PARENT_QLOC_2073_BMIX_ORIGIN_AUDIT.csv",
        "residual": OUT / "P8_Y5_PARENT_QLOC_2073_FINITE_CAP_RESIDUAL_TEMPLATE.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2073_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2073_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2073_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2073_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2073_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2073_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["theorem"], theorem_rows)
    write_csv(paths["origin"], origin_rows)
    write_csv(paths["residual"], residual_rows)
    write_csv(paths["dry"], dry_rows_)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(theorem_rows, origin_rows, residual_rows, dry_rows_, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(row["path"])) for row in copies]
    remove_pycache()
    validation = validation_rows(sources, theorem_rows, origin_rows, residual_rows, dry_rows_, gates, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, theorem_rows, origin_rows, residual_rows, dry_rows_, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
