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


DOC = ROOT / "2072-Y5-R2FR-Bmix-cap-functional-or-parent-current-chain-theta-Qtau.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2072_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2072-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2072*",
        "*Y5_R2FR_Bmix_cap_functional_or_parent_current_chain_theta_Qtau_2072*",
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
            "SRC2072_00_2071_doc",
            ROOT / "2071-Y5-R2FR-Bcap-same-parent-functional-or-theta-Qtau-denominator-route.md",
            ["NEXT2071_0_2072", "B_mix_cap[R_AB,tau,T_H]", "K_cap_to_PiR"],
            "2071 handoff to mixed cap functional or parent current-chain route.",
        ),
        (
            "SRC2072_01_2071_next",
            OUT / "P8_Y5_PARENT_QLOC_2071_NEXT_TARGET.csv",
            ["NEXT2071_0_2072", "B_mix_cap action term", "q_R normalization guard"],
            "machine-readable 2072 target.",
        ),
        (
            "SRC2072_02_2071_Bcap_ledger",
            OUT / "P8_Y5_PARENT_QLOC_2071_BCAP_FUNCTIONAL_CANDIDATE_LEDGER.csv",
            ["BFC2071_3_Bmix_required", "MISSING_PARENT_BMIX_CAP_FUNCTIONAL", "BCAP_ROUTE_BLOCKED_ON_BMIX_PARENT_FUNCTIONAL"],
            "Bmix cap requirement from 2071.",
        ),
        (
            "SRC2072_03_2071_same_parent",
            OUT / "P8_Y5_PARENT_QLOC_2071_SAME_PARENT_TEST.csv",
            ["SPT2071_4_theorem_zero_option", "SPT2071_6_verdict", "FAIL_CURRENT_CLAIM_BCAP_SAME_PARENT_UNSIGNED"],
            "same-parent test and theorem-zero refusal.",
        ),
        (
            "SRC2072_04_06_reciprocal_neutrality",
            ROOT / "06-reciprocal-charge-source-neutrality.md",
            ["Pi_R = 0 -> Q_R = 0 -> R_AB = 0 -> AB = 1.", "source reciprocal neutrality.", "R_AB = q_R L"],
            "legacy reciprocal neutrality and PPN q_R relation.",
        ),
        (
            "SRC2072_05_07_nonprop_constraint",
            ROOT / "07-nonpropagating-reciprocity-constraint.md",
            ["parent origin is still open", "R_AB = 0.", "constraint parent origin"],
            "nonpropagating constraint gives clean algebra only if parent-signed.",
        ),
        (
            "SRC2072_06_11_cell_current",
            ROOT / "11-cell-current-origin-attempt.md",
            ["W partial_r R_AB = Q_R.", "R_AB = -Q_R/r.", "gives a Ward identity, not R_AB=0."],
            "ordinary current conservation leaves reciprocal charge hair.",
        ),
        (
            "SRC2072_07_1238_first_class",
            ROOT / "1238-Y5-R10-first-class-RAB-constraint-or-local-GR-closure-benchmark-scorecard.md",
            ["FIRST_CLASS_ROUTE_NOT_CONSTRUCTED", "CLOSURE_NOT_DERIVATION", "USEFUL_PRIVATE_BASELINE_ONLY"],
            "first-class R_AB=0 route not constructed; closure benchmark remains private.",
        ),
        (
            "SRC2072_08_1246_QR_zero",
            ROOT / "1246-Y5-R10-parent-QR-zero-theorem-or-finite-residual-source-hunt.md",
            ["QTA1246_0_parent_zero_verdict", "NOT_DERIVED_CURRENT_CORPUS", "WORKS_ONLY_IF_PARENT_SIGNED"],
            "parent Q_R zero theorem remains missing; conditional route identified.",
        ),
        (
            "SRC2072_09_1008_piece_ledger",
            OUT / "P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv",
            ["QTA1008_0_L_parent", "QTA1008_8_Q_total", "not_promoted"],
            "theta/Q_tau charge pieces remain unpromoted.",
        ),
        (
            "SRC2072_10_1009_parent_contract",
            ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            ["PCS1009_9_total_parent_contract", "CG1009_0_total_parent_action", "Gamma_eff/K_hat/q_loc is the sharpest next derivation target"],
            "parent current-chain action contract remains unsigned.",
        ),
        (
            "SRC2072_11_2063_component_intake",
            OUT / "P8_Y5_PARENT_QLOC_2063_FINITE_PIR_COMPONENT_INTAKE.csv",
            ["PCI2063_3_corner_bound", "PCI2063_4_total_join", "PCI2063_5_qR_Cassini_join"],
            "finite Pi_R join and q_R guard.",
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


def bmix_variation_theorem_rows() -> list[dict[str, object]]:
    data = [
        (
            "BVT2072_0_generic_ansatz",
            "generic mixed cap functional",
            "B_mix_cap = integral_Ccap mu_C beta_mix f(R_AB-R_star) Xi_tau",
            "R_AB is the reciprocal variable; R_star is the local reciprocal fixed point; Xi_tau is a parent tau/current cap scalar.",
            "ANSATZ_CONTRACT_WRITTEN",
            True,
        ),
        (
            "BVT2072_1_R_variation",
            "R_AB variation",
            "pi_R^cap = beta_mix f_prime(R_AB-R_star) Xi_tau plus measure-variation terms",
            "if mu_C is R-independent or its R-variation is separately included, this is the Pi_R cap density generated by the same functional.",
            "EXACT_CONDITIONAL_VARIATION",
            True,
        ),
        (
            "BVT2072_2_tau_variation",
            "tau/current variation",
            "N_tau_cap = integral_Ccap mu_C beta_mix f(R_AB-R_star) D_tau Xi_tau plus tau-variation of mu_C/normal/source-reference pieces",
            "this is the cap-current side generated by the same B_mix_cap.",
            "EXACT_CONDITIONAL_VARIATION",
            True,
        ),
        (
            "BVT2072_3_local_silence_condition",
            "local cap silence",
            "Pi_R_time_caps=0 and N_tau_cap=0 at R_AB=R_star require f(0)=0 and f_prime(0)=0, assuming finite Xi_tau and D_tau Xi_tau",
            "this is the exact double-zero condition for the mixed cap route.",
            "DOUBLE_ZERO_SELECTION_LAW_DERIVED",
            True,
        ),
        (
            "BVT2072_4_quadratic_minimum",
            "lowest analytic safe choice",
            "f(Delta R)=c_2(Delta R)^2+O((Delta R)^3)",
            "constant and linear mixed couplings fail at least one cap-silence condition; quadratic is the lowest analytic local-safe shape.",
            "QUADRATIC_OR_HIGHER_REQUIRED",
            True,
        ),
        (
            "BVT2072_5_parent_not_signed",
            "parent adoption",
            "the theorem selects the required shape but does not prove the parent action contains this B_mix_cap or that R_AB=R_star locally",
            "the algebra is progress; it is not a local-GR claim.",
            "CONDITIONAL_THEOREM_ONLY",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_id, formula, derivation_note, status, theorem_valid in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object_id": object_id,
                "formula": formula,
                "derivation_note": derivation_note,
                "status": status,
                "conditional_theorem_valid": theorem_valid,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def double_zero_selection_rows() -> list[dict[str, object]]:
    data = [
        (
            "DZS2072_0_constant",
            "f(Delta R)=c0",
            "f(0)!=0 unless c0=0",
            "f_prime(0)=0",
            "fails N_tau silence; c0=0 removes the mixed term",
            "FAIL_LOCAL_CAP_SILENCE",
        ),
        (
            "DZS2072_1_linear",
            "f(Delta R)=c1 Delta R",
            "f(0)=0",
            "f_prime(0)=c1",
            "fails Pi_R silence unless c1=0",
            "FAIL_LOCAL_CAP_SILENCE",
        ),
        (
            "DZS2072_2_quadratic",
            "f(Delta R)=c2 Delta R^2",
            "f(0)=0",
            "f_prime(0)=0",
            "passes algebraic cap double-zero if parent signs R_star, Xi_tau, mu_C and beta_mix",
            "PASS_CONDITIONAL_DOUBLE_ZERO",
        ),
        (
            "DZS2072_3_higher_order",
            "f(Delta R)=O(Delta R^p), p>=2",
            "f(0)=0",
            "f_prime(0)=0",
            "passes the same algebra; p controls residual order away from the local branch",
            "PASS_CONDITIONAL_DOUBLE_ZERO",
        ),
        (
            "DZS2072_4_exact_topological",
            "B_mix_cap exact/topological with no cap variation",
            "effective f(0)=0",
            "effective f_prime(0)=0",
            "also acceptable if parent-fixed and not post-fit cancellation",
            "PASS_IF_PARENT_TOPOLOGICAL_CERTIFIED",
        ),
        (
            "DZS2072_5_selection_verdict",
            "mixed cap coupling law",
            "f(0)=0",
            "f_prime(0)=0",
            "local safety selects quadratic-or-higher or exact/topological mixed cap coupling",
            "DOUBLE_ZERO_LAW_DERIVED_PARENT_ORIGIN_MISSING",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, candidate, value_at_fixed_point, derivative_at_fixed_point, consequence, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "candidate": candidate,
                "value_at_fixed_point": value_at_fixed_point,
                "derivative_at_fixed_point": derivative_at_fixed_point,
                "consequence": consequence,
                "status": status,
                "valid_for_local_claim": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def finite_residual_rows() -> list[dict[str, object]]:
    data = [
        (
            "FRE2072_0_quadratic_PiR",
            "Pi_R_time_caps_abs",
            "for f=c2 DeltaR^2, Pi_R_time_caps_abs <= integral_Ccap mu_C |2 beta_mix c2 DeltaR Xi_tau| + measure terms",
            "O(|DeltaR|)",
            "beta_mix,c2,DeltaR,Xi_tau,mu_C,measure-variation bound",
            "local Pi_R cap residual is first order in the reciprocal displacement unless DeltaR is theorem-zero.",
        ),
        (
            "FRE2072_1_quadratic_Ntau",
            "N_tau_cap_abs",
            "N_tau_cap_abs <= integral_Ccap mu_C |beta_mix c2 DeltaR^2 D_tau Xi_tau| + normal/source-reference terms",
            "O(DeltaR^2)",
            "beta_mix,c2,DeltaR,D_tauXi_tau,mu_C,cap normal variation",
            "cap current leakage is second order for the quadratic route.",
        ),
        (
            "FRE2072_2_Kcap_ratio_warning",
            "K_cap_to_PiR",
            "K_cap_to_PiR = Pi_R_time_caps_abs/N_tau_cap_abs is generally O(1/|DeltaR|) near the double zero",
            "ratio can blow up while both absolute components vanish",
            "separate absolute Pi_R and N_tau bounds, not only their ratio",
            "near a double zero, K is a poor stability diagnostic unless denominator is independently bounded away from zero.",
        ),
        (
            "FRE2072_3_qR_guard",
            "q_R contribution",
            "q_R_cap enters only through absolute Pi_R component join and q_R normalization after all tails/source-reference pieces are included",
            "blocked until normalization inputs exist",
            "N_sphere,Z_R_infty,r_s,tail bounds,Pi_R total join",
            "prevents using the quadratic ansatz as a cap-only PPN pass.",
        ),
        (
            "FRE2072_4_finite_verdict",
            "finite residual branch",
            "if R_AB=R_star is not parent-derived, 2072 supplies residual scaling but no value",
            "source-ready but unscored",
            "numeric/source rows for DeltaR,beta_mix,Xi_tau,D_tauXi_tau,mu_C",
            "the route is testable once coefficients are sourced.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, bound_formula, order, required_inputs, note in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "bound_formula": bound_formula,
                "scaling_order": order,
                "required_inputs": required_inputs,
                "note": note,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def parent_contract_rows() -> list[dict[str, object]]:
    data = [
        (
            "PIC2072_0_Rstar",
            "R_star local reciprocal fixed point",
            "parent theorem that compact local exterior has R_AB=R_star, preferably R_star=0/AB=1",
            "MISSING_PARENT_FIXED_POINT_OR_QR_ZERO_THEOREM",
            "1238/1246 say this is currently closure-only or conditional.",
        ),
        (
            "PIC2072_1_Bmix_action",
            "B_mix_cap action term",
            "parent action contains integral_Ccap mu_C beta_mix f(R_AB-R_star) Xi_tau with f(0)=f_prime(0)=0",
            "MISSING_PARENT_BMIX_ACTION_SOURCE",
            "the shape is selected but not sourced.",
        ),
        (
            "PIC2072_2_Xi_tau",
            "Xi_tau current scalar",
            "Xi_tau is extracted from parent theta_MTS/Q_tau^MTS or source-current chain, not invented as a cap scalar",
            "MISSING_PARENT_THETA_QTAU_CURRENT_SCALAR",
            "1008/1009 keep theta/Q_tau/current chain unpromoted.",
        ),
        (
            "PIC2072_3_cap_geometry",
            "C_cap,mu_C,n_C",
            "cap surface, normal, measure, orientation and their variations are fixed or explicitly bounded",
            "MISSING_CAP_GEOMETRY_CERTIFICATE",
            "measure variations can otherwise reintroduce first-order terms.",
        ),
        (
            "PIC2072_4_beta_units",
            "beta_mix and units",
            "beta_mix has source path, dimensions, sign/positivity convention and sector universality",
            "MISSING_BETA_MIX_SOURCE_AND_UNITS",
            "without units the residual rows cannot be scored.",
        ),
        (
            "PIC2072_5_source_reference",
            "source/reference split",
            "B_source_caps and B_ref_caps are separated before absolute summing and fixed before readout",
            "MISSING_SOURCE_REFERENCE_CAP_SPLIT",
            "prevents fitted-reference cancellation.",
        ),
        (
            "PIC2072_6_qR_normalization",
            "q_R normalization",
            "Pi_R^tot_abs joins N_sphere,Z_R_infty,r_s and tail bounds before PPN/Cassini scoring",
            "MISSING_QR_NORMALIZATION_CHAIN",
            "2063 still blocks finite local scoring.",
        ),
        (
            "PIC2072_7_verdict",
            "2072 parent input contract",
            "double-zero law is derived, but the parent objects that would activate it are missing",
            "CONTRACT_WRITTEN_PARENT_INPUTS_MISSING",
            "next work should attack R_star/Bmix/Xi_tau ownership, not downstream data scoring.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_id, requirement, status, note in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object_id": object_id,
                "requirement": requirement,
                "status": status,
                "note": note,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def dry_run_rows() -> list[dict[str, object]]:
    data = [
        (
            "RUN2072_0_generic_variation",
            "generic Bmix variation",
            "PASS_CONDITIONAL_THEOREM",
            "same-parent variation algebra is written for B_mix_cap = integral beta f(R-Rstar) Xi_tau.",
            False,
        ),
        (
            "RUN2072_1_double_zero_law",
            "f(0)=0 and f_prime(0)=0",
            "PASS_SELECTION_LAW",
            "constant/linear couplings fail; quadratic-or-higher is the local-safe analytic class.",
            False,
        ),
        (
            "RUN2072_2_parent_origin",
            "parent-owned Bmix/Rstar/Xi_tau",
            "FAIL_PARENT_INPUTS_MISSING",
            "Rstar, Bmix action source, Xi_tau, cap geometry, beta units and q_R guard are not sourced.",
            False,
        ),
        (
            "RUN2072_VERDICT",
            "Bmix cap construction",
            "DOUBLE_ZERO_LAW_DERIVED_PARENT_OWNERSHIP_MISSING",
            "2073 should prove/source Rstar and the quadratic/topological Bmix origin, or convert the branch to finite residual coefficient acquisition.",
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
            "GATE2072_0_selection_law",
            "double-zero coupling selection law can be cited internally",
            "PASS_CONDITIONAL_THEOREM",
            "for the generic ansatz, local cap silence requires f(0)=f_prime(0)=0.",
        ),
        (
            "GATE2072_1_Bmix_parent",
            "Bmix cap term is parent-derived",
            "FAIL_BLOCKED",
            "no parent action source signs the quadratic/topological mixed cap term.",
        ),
        (
            "GATE2072_2_Rstar_parent",
            "R_AB=R_star local fixed point is parent-derived",
            "FAIL_BLOCKED",
            "R_AB=0/Q_R=0 remains closure-only or conditional in inspected sources.",
        ),
        (
            "GATE2072_3_Xi_tau_parent",
            "Xi_tau is extracted from theta_MTS/Q_tau^MTS",
            "FAIL_BLOCKED",
            "parent current-chain/theta-Qtau extraction remains unpromoted.",
        ),
        (
            "GATE2072_4_finite_score",
            "finite cap residual can be scored",
            "FAIL_BLOCKED",
            "DeltaR, beta_mix, Xi_tau, D_tauXi_tau, cap measure and q_R normalization are missing.",
        ),
        (
            "GATE2072_5_local_GR",
            "local GR/Newton/PPN/R10 branch can claim pass",
            "FAIL_BLOCKED",
            "the coupling law is conditional and the parent inputs are missing.",
        ),
        (
            "GATE2072_6_formalization",
            "formalization-workbench edit allowed",
            "PASS_NO_EDIT",
            "2072 is contained in post-checkpoint-work.",
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
            "DEC2072_0_real_progress",
            "BMIX_DOUBLE_ZERO_SELECTION_LAW_DERIVED",
            "The coupling gap is no longer arbitrary: local-safe mixed cap terms must be quadratic-or-higher or exact/topological at the local reciprocal fixed point.",
        ),
        (
            "DEC2072_1_linear_coupling_rejected",
            "LINEAR_BMIX_COUPLING_FAILS_LOCAL_CAP_SILENCE",
            "A linear mixed term gives nonzero Pi_R cap density at the local fixed point.",
        ),
        (
            "DEC2072_2_parent_debt",
            "PARENT_ORIGIN_REMAINS_THE_BLOCKER",
            "The theorem does not derive Rstar, beta_mix, Xi_tau, or the mixed cap term from the parent action.",
        ),
        (
            "DEC2072_3_best_next",
            "TARGET_RSTAR_AND_BMIX_OR_FINITE_RESIDUAL",
            "Best next route is to prove the reciprocal fixed point and quadratic/topological Bmix origin; fallback is finite coefficient acquisition.",
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
            "target_id": "NEXT2072_0_2073",
            "target_doc": "2073-Y5-R2FR-reciprocal-fixed-point-and-quadratic-Bmix-origin-or-finite-cap-residual.md",
            "objective": "prove/source the local reciprocal fixed point R_AB=R_star and the quadratic-or-topological Bmix cap origin, or stage finite residual coefficient acquisition for DeltaR, beta_mix, Xi_tau and q_R cap normalization",
            "must_include": "Rstar theorem; f_mix(0)=0; f_mix_prime(0)=0; parent Bmix action source; Xi_tau from theta_MTS/Q_tau; cap geometry; beta_mix units; source/reference split; finite residual fallback; q_R normalization guard",
            "excluded": "R_AB=0 closure as derivation; linear Bmix coupling; Kcap ratio-only scoring; fitted reference; orbital GM import; cancellation; local-GR/PPN/R10 claim; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    theorem_rows: list[dict[str, object]],
    selection_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2072_0_source_weight_theorem",
            SOURCE_WEIGHT_DOCS / "AFRAME_BMIX_DOUBLE_ZERO_THEOREM_2072_NONCLAIM.csv",
            theorem_rows,
        ),
        (
            "COPY2072_1_source_weight_selection",
            SOURCE_WEIGHT_DOCS / "AFRAME_BMIX_COUPLING_SELECTION_LAW_2072_NONCLAIM.csv",
            selection_rows,
        ),
        (
            "COPY2072_2_source_weight_residual",
            SOURCE_WEIGHT_DOCS / "AFRAME_BMIX_FINITE_RESIDUAL_EXPANSION_2072_NONCLAIM.csv",
            residual_rows,
        ),
        (
            "COPY2072_3_source_weight_parent_contract",
            SOURCE_WEIGHT_DOCS / "AFRAME_BMIX_PARENT_INPUT_CONTRACT_2072_NONCLAIM.csv",
            contract_rows,
        ),
        (
            "COPY2072_4_wep_dry_run",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2072_BMIX_DOUBLE_ZERO_DRY_RUN_NONCLAIM.csv",
            dry_rows_,
        ),
        (
            "COPY2072_5_queue_next",
            QUEUE / "JR2072_RSTAR_BMIX_OR_FINITE_RESIDUAL_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, data in copies:
        write_csv(path, data)
        row = base_row()
        row.update(
            {
                "copy_id": copy_id,
                "path": str(path),
                "rows": len(data),
                "status": "WRITTEN_NONCLAIM_COPY",
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    selection_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    theorem_ok = (
        any(row["row_id"] == "BVT2072_3_local_silence_condition" and row["status"] == "DOUBLE_ZERO_SELECTION_LAW_DERIVED" for row in theorem_rows)
        and any(row["row_id"] == "BVT2072_4_quadratic_minimum" and row["status"] == "QUADRATIC_OR_HIGHER_REQUIRED" for row in theorem_rows)
        and all(not bool(row["ready_for_scoring"]) for row in theorem_rows)
    )
    selection_ok = (
        any(row["row_id"] == "DZS2072_1_linear" and row["status"] == "FAIL_LOCAL_CAP_SILENCE" for row in selection_rows)
        and any(row["row_id"] == "DZS2072_2_quadratic" and row["status"] == "PASS_CONDITIONAL_DOUBLE_ZERO" for row in selection_rows)
        and any(row["row_id"] == "DZS2072_5_selection_verdict" and row["status"] == "DOUBLE_ZERO_LAW_DERIVED_PARENT_ORIGIN_MISSING" for row in selection_rows)
    )
    residual_ok = (
        any(row["row_id"] == "FRE2072_0_quadratic_PiR" and row["scaling_order"] == "O(|DeltaR|)" for row in residual_rows)
        and any(row["row_id"] == "FRE2072_1_quadratic_Ntau" and row["scaling_order"] == "O(DeltaR^2)" for row in residual_rows)
        and any(row["row_id"] == "FRE2072_2_Kcap_ratio_warning" for row in residual_rows)
        and all(not bool(row["ready_for_scoring"]) for row in residual_rows)
    )
    contract_ok = (
        any(row["row_id"] == "PIC2072_0_Rstar" and row["status"] == "MISSING_PARENT_FIXED_POINT_OR_QR_ZERO_THEOREM" for row in contract_rows)
        and any(row["row_id"] == "PIC2072_7_verdict" and row["status"] == "CONTRACT_WRITTEN_PARENT_INPUTS_MISSING" for row in contract_rows)
        and all(not bool(row["ready_for_scoring"]) for row in contract_rows)
    )
    dry_ok = any(
        row["run_id"] == "RUN2072_VERDICT"
        and row["verdict"] == "DOUBLE_ZERO_LAW_DERIVED_PARENT_OWNERSHIP_MISSING"
        and not bool(row["accepted_for_scoring"])
        for row in dry_rows_
    )
    gates_ok = all(row["claim_allowed"] is False and row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2072_0_2073"
    copies_ok = all(Path(str(row["path"])).exists() and csv_rows_parse(Path(str(row["path"]))) for row in copies)
    no_claim = all(
        not bool(row.get("claim_allowed", False)) and not bool(row.get("valid_for_claim", False))
        for group in [sources, theorem_rows, selection_rows, residual_rows, contract_rows, dry_rows_, gates, next_rows_, copies]
        for row in group
    )
    checks = [
        ("VAL2072_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2072_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2072_02_double_zero_theorem", theorem_ok, "generic Bmix variation derives f(0)=f_prime(0)=0 selection law"),
        ("VAL2072_03_shape_audit", selection_ok, "constant/linear fail and quadratic/higher pass conditionally"),
        ("VAL2072_04_finite_residual_expansion", residual_ok, "finite residual scaling and Kcap ratio warning are staged"),
        ("VAL2072_05_parent_contract", contract_ok, "parent inputs are explicitly missing and nonclaim"),
        ("VAL2072_06_dry_verdict", dry_ok, "dry run refuses scoring while preserving theorem progress"),
        ("VAL2072_07_claim_gates_blocked", gates_ok, "all local claim gates remain blocked/nonclaim"),
        ("VAL2072_08_next_selected", next_ok, "2073 Rstar/Bmix-or-finite-residual target selected"),
        ("VAL2072_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2072_10_no_claim_flags", no_claim, "no generated row allows a claim"),
        ("VAL2072_11_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"),
        ("VAL2072_12_no_formalization_artifacts", not formalization_has_2072_artifacts(), "no 2072 artifacts were written under formalization-workbench"),
        ("VAL2072_13_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"),
    ]
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2072_OVERALL", overall, "2072 derives the Bmix double-zero selection law without promoting local claims"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    theorem_rows: list[dict[str, object]],
    selection_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2072 Y5 R2FR Bmix Cap Functional Or Parent Current Chain Theta Qtau",
        "",
        "## Current Verdict",
        "",
        "2072 makes a real derivation step: for a same-parent mixed cap functional of the form `B_mix_cap = integral_Ccap mu_C beta_mix f(R_AB-R_star) Xi_tau`, local cap silence forces the double-zero conditions `f(0)=0` and `f_prime(0)=0`. A constant mixed coupling leaves tau/current cap leakage; a linear mixed coupling leaves a nonzero `Pi_R` cap density. The lowest analytic local-safe shape is therefore quadratic or higher.",
        "",
        "This does not yet close local GR. It converts the vague coupling problem into a sharp parent-action contract: prove/source `R_star`, prove/source the quadratic-or-topological `B_mix_cap`, extract `Xi_tau` from `theta_MTS/Q_tau^MTS`, fix cap geometry and units, and keep source/reference caps separated. Until those are supplied, the result is a conditional theorem and finite-residual scaling law, not evidence.",
        "",
        "The finite fallback is also clearer: for a quadratic cap term, `Pi_R_time_caps_abs` is generically `O(|DeltaR|)` while `N_tau_cap_abs` is `O(DeltaR^2)`. The ratio `K_cap_to_PiR` can therefore blow up near the double zero even when both absolute cap pieces vanish, so future scoring must track absolute components and q_R normalization, not only the ratio.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, Kcap, MHref, q_R, or public claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Bmix Generic Variation Theorem",
        md_table(theorem_rows, ["row_id", "object_id", "formula", "derivation_note", "status", "conditional_theorem_valid", "ready_for_scoring", "claim_allowed"]),
        "## Double Zero Selection Law",
        md_table(selection_rows, ["row_id", "candidate", "value_at_fixed_point", "derivative_at_fixed_point", "consequence", "status", "valid_for_local_claim", "claim_allowed"]),
        "## Finite Residual Expansion",
        md_table(residual_rows, ["row_id", "quantity", "bound_formula", "scaling_order", "required_inputs", "note", "ready_for_scoring", "claim_allowed"]),
        "## Parent Input Contract",
        md_table(contract_rows, ["row_id", "object_id", "requirement", "status", "note", "ready_for_scoring", "claim_allowed"]),
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
    theorem_rows = bmix_variation_theorem_rows()
    selection_rows = double_zero_selection_rows()
    residual_rows = finite_residual_rows()
    contract_rows = parent_contract_rows()
    dry_rows_ = dry_run_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2072_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2072_BMIX_GENERIC_VARIATION_THEOREM.csv",
        "selection": OUT / "P8_Y5_PARENT_QLOC_2072_DOUBLE_ZERO_SELECTION_LAW.csv",
        "residual": OUT / "P8_Y5_PARENT_QLOC_2072_FINITE_RESIDUAL_EXPANSION.csv",
        "contract": OUT / "P8_Y5_PARENT_QLOC_2072_PARENT_INPUT_CONTRACT.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2072_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2072_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2072_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2072_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2072_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2072_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["theorem"], theorem_rows)
    write_csv(paths["selection"], selection_rows)
    write_csv(paths["residual"], residual_rows)
    write_csv(paths["contract"], contract_rows)
    write_csv(paths["dry"], dry_rows_)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(theorem_rows, selection_rows, residual_rows, contract_rows, dry_rows_, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(row["path"])) for row in copies]
    remove_pycache()
    validation = validation_rows(
        sources,
        theorem_rows,
        selection_rows,
        residual_rows,
        contract_rows,
        dry_rows_,
        gates,
        next_rows_,
        copies,
        csv_paths,
    )
    write_csv(paths["validation"], validation)
    write_doc(sources, theorem_rows, selection_rows, residual_rows, contract_rows, dry_rows_, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
