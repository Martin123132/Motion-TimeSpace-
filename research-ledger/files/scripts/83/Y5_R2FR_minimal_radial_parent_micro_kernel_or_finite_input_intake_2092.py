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


DOC = ROOT / "2092-Y5-R2FR-minimal-radial-parent-micro-kernel-or-finite-input-intake.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
Q_R_HAT_POLICY_CEILING = 4.6e-05


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "claim_allowed", "valid"}


def formalization_has_2092_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2092-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2092*",
        "*Y5_R2FR_minimal_radial_parent_micro_kernel_or_finite_input_intake_2092*",
        "*AFRAME_MINIMAL_RADIAL_MICRO_KERNEL_2092*",
        "*JR2092_FINITE_LOCAL_INPUT_INTAKE*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2092_00_2091_handoff",
            ROOT / "2091-Y5-R2FR-radial-canonical-pair-source-hunt-or-finite-residual-lock.md",
            ["NEXT2091_0_2092", "LOCK2091_0_selector_status", "VAL2091_OVERALL"],
            "2091 locks selector as closure-only and selects parent micro-kernel attempt.",
        ),
        (
            "SRC2092_01_2090_kernel_target",
            ROOT / "2090-Y5-R2FR-selector-cross-term-parent-origin-or-object-language-closure-lock.md",
            ["SCT2090_4_exact_conditional_theorem", "PKG2090_0_parent_theta", "VAL2090_OVERALL"],
            "2090 defines the exact radial canonical package target.",
        ),
        (
            "SRC2092_02_2089_selector",
            ROOT / "2089-Y5-R2FR-parent-Euler-source-map-contract-integration-or-finite-trace-input-lock.md",
            ["CER2089_2_selector_cross_term_contract", "SRI2089_0_selector_defect", "VAL2089_OVERALL"],
            "2089 extracts the selector cross-term and residual selector defect.",
        ),
        (
            "SRC2092_03_1008_theta",
            ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            ["PVA1008_1_theta_MTS", "PVA1008_6_verdict", "CG1008_0_parent_theta"],
            "theta_MTS extraction remains a contract, not a source.",
        ),
        (
            "SRC2092_04_1009_current_chain",
            ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            ["PCS1009_9_total_parent_contract", "SVC1009_6_total_parent_switch_unsigned", "CG1009_1_theta_MTS"],
            "total current-chain action remains unsigned.",
        ),
        (
            "SRC2092_05_1273_Hcore",
            ROOT / "1273-Y5-R10-RAB-parent-Hcore-radial-cell-owner-or-finite-residual-source-acquisition.md",
            ["HCO1273_6_classification_verdict", "DEC1273_0_no_ordinary_Hcore", "VAL1273_11_overall"],
            "ordinary H_core route cannot give theorem-zero.",
        ),
        (
            "SRC2092_06_1248_Dirac",
            ROOT / "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check.md",
            ["DIR1248_2_preservation", "DEC1248_0_ansatz_not_enough", "DEC1248_2_keep_parent_repair_path"],
            "multiplier ansatz is formal only without parent H_core/brackets.",
        ),
        (
            "SRC2092_07_1564_presymplectic",
            ROOT / "1564-Y5-RAB-vertical-null-presymplectic-degeneracy-or-finite-ZR-intake.md",
            ["NULL1564_0_parent_L_theta", "NULL1564_5_verdict", "VAL1564_OVERALL"],
            "presymplectic-null route lacks parent L/theta/Omega and boundary zero.",
        ),
        (
            "SRC2092_08_1577_current",
            ROOT / "1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md",
            ["RCC1577_0_current_equation", "NCA1577_4_verdict", "VAL1577_OVERALL"],
            "radial current leaves Q_R hair without no-charge theorem.",
        ),
        (
            "SRC2092_09_1819_charge",
            ROOT / "1819-Y5-R2FR-local-EH-symplectic-charge-inheritance-or-Cterm-residual-vector.md",
            ["EHC1819_0_target", "EHC1819_6_verdict", "CTA1819_5_verdict"],
            "EH charge route remains conditional with C-term residuals.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="minimal_radial_micro_kernel_evidence",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2092=note,
                valid_for_claim=False,
                claim_allowed=False,
            )
        )
    return rows


def micro_kernel_rows() -> list[dict[str, object]]:
    return [
        row(
            kernel_id="MK2092_0_variables",
            object="radial compatibility pair",
            statement="Use C_R=ln(T^2 S) and P_R=V_R/2 as a proposed parent radial canonical pair.",
            calculation_or_variation="theta_R=P_R delta C_R; Omega_R=delta P_R wedge delta C_R.",
            result="MICRO_KERNEL_DECLARED",
            parent_status="NEW_PARENT_BLOCK_NOT_DERIVED_FROM_EXISTING_CORPUS",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            kernel_id="MK2092_1_action",
            object="minimal first-order radial sector",
            statement="S_micro[I]=int_I dr P_R(partial_r C_R-S_R[C_R,source,q_loc,boundary,readout]) + B_R.",
            calculation_or_variation="equivalently L_micro=P_R C_R' - H_R with H_R=P_R S_R.",
            result="OWNS_THETA_R_AND_HR_IF_ADOPTED",
            parent_status="AXIOMATIC_MICRO_KERNEL_CANDIDATE",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            kernel_id="MK2092_2_delta_PR",
            object="P_R variation",
            statement="Variation with respect to P_R gives the desired radial selector equation.",
            calculation_or_variation="delta_{P_R} S_micro = int dr delta P_R (C_R'-S_R), so C_R'=S_R.",
            result="D_R_FORMAL_PASS_INSIDE_MICRO_KERNEL",
            parent_status="CONDITIONAL_ON_ADOPTING_MICRO_KERNEL",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            kernel_id="MK2092_3_delta_CR",
            object="C_R variation",
            statement="The companion equation controls P_R and exposes source/boundary dependence.",
            calculation_or_variation="delta_{C_R} S_micro = int dr [-P_R' - P_R partial_{C_R}S_R + E_C^extra] delta C_R + [P_R delta C_R + delta B_R]_{boundary}.",
            result="COMPANION_EQUATION_AND_BOUNDARY_NOT_OPTIONAL",
            parent_status="REQUIRES_BOUNDARY_AND_SOURCE_MAP",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            kernel_id="MK2092_4_local_zero_corollary",
            object="local vacuum reduction",
            statement="If S_R=0 in the protected exterior, C_R is fixed to zero on one reference surface, and boundary/no-charge blocks reciprocal hair, then C_R=0.",
            calculation_or_variation="C_R'=0 plus C_R(r_ref)=0 gives C_R=0; P_R boundary term must be silent.",
            result="LOCAL_GR_RECIPROCITY_CONDITIONAL",
            parent_status="NOT_CURRENT_CLAIM",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            kernel_id="MK2092_5_status",
            object="micro-kernel verdict",
            statement="The micro-kernel is the smallest exact block that would make the 2089/2090 selector work.",
            calculation_or_variation="It is internally variationally consistent, but the current corpus does not force this block from deeper primitives.",
            result="MINIMAL_AXIOM_OR_CLOSURE_NOT_DERIVATION",
            parent_status="USER_CAN_CHOOSE_AS_NEW_POSTULATE_BUT_NOT_AS_DERIVED_RESULT",
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def axiom_cost_rows() -> list[dict[str, object]]:
    return [
        row(
            cost_id="COST2092_0_new_canonical_pair",
            added_assumption="C_R/P_R is a parent radial compatibility pair with theta_R=P_R delta C_R.",
            why_needed="owns the V_R partial_r C_R term without importing GR",
            scrutiny_risk="adds a new parent sector unless derived from object-language",
            mitigation="declare it as compatibility/constraint data, not propagating matter",
            status="AXIOM_COST_EXPLICIT",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            cost_id="COST2092_1_no_extra_VR",
            added_assumption="no V_R^2, V_R J_hidden, V_R q_loc, or readout-generated V_R term outside S_R.",
            why_needed="keeps E_V equal to 1/2(C_R'-S_R)",
            scrutiny_risk="generic local effective actions permit extra terms unless grammar forbids them",
            mitigation="typed object-language or residual Delta_sel ledger",
            status="AXIOM_COST_EXPLICIT",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            cost_id="COST2092_2_source_silence",
            added_assumption="S_R=0 or source-backed bounded in protected local vacuum.",
            why_needed="C_R'=S_R only gives C_R=0 if the source side is zero or controlled",
            scrutiny_risk="matter descent, q_loc, boundary, readout and coefficient variations can re-enter",
            mitigation="source map theorem or finite no-cancellation envelope",
            status="AXIOM_COST_EXPLICIT",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            cost_id="COST2092_3_boundary_class",
            added_assumption="P_R delta C_R boundary term is fixed, zero, or cancelled by parent-owned B_R.",
            why_needed="prevents reciprocal charge/hair from surviving outside sources",
            scrutiny_risk="asymptotic flatness alone does not kill Q_R",
            mitigation="boundary no-charge theorem or finite Q_R/q_R_hat row",
            status="AXIOM_COST_EXPLICIT",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            cost_id="COST2092_4_foundational_choice",
            added_assumption="accepting the micro-kernel is a new parent postulate unless a deeper derivation is supplied.",
            why_needed="current corpus source hunt did not derive theta_R/H_R",
            scrutiny_risk="would weaken the 'fully derived' ambition if presented as proof",
            mitigation="label as explicit parent axiom or continue deriving object-language",
            status="AXIOM_COST_EXPLICIT",
            valid_for_claim=False,
            claim_allowed=False,
        ),
    ]


def countermodel_rows() -> list[dict[str, object]]:
    return [
        row(
            countermodel_id="CM2092_0_extra_quadratic",
            countermodel="L_extra=a V_R^2",
            effect="E_time-E_radial gains a V_R response and no longer equals C_R'-S_R",
            blocked_by="no-extra-V_R object-language theorem or finite Delta_sel row",
            status="RETAINED_UNLESS_FORBIDDEN",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            countermodel_id="CM2092_1_kinetic_CR",
            countermodel="L_extra=1/2 Z_R (partial C_R)^2",
            effect="C_R becomes finite elliptic/propagating residual with local-test hair",
            blocked_by="Z_R=0 theorem from compatibility grammar or source-backed Z_R/M_R2 branch",
            status="RETAINED_UNLESS_FORBIDDEN",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            countermodel_id="CM2092_2_nonzero_SR",
            countermodel="S_R contains matter, q_loc, readout or coefficient source",
            effect="C_R'=S_R produces local reciprocal response instead of GR reciprocity",
            blocked_by="same-source/q_loc/boundary/readout zero theorem or finite source envelope",
            status="RETAINED_UNLESS_FORBIDDEN",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            countermodel_id="CM2092_3_boundary_hair",
            countermodel="P_R boundary flux or Q_R charge is allowed",
            effect="exterior C_R can carry reciprocal hair even when bulk S_R=0",
            blocked_by="boundary no-charge theorem or q_R_hat bound",
            status="RETAINED_UNLESS_FORBIDDEN",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            countermodel_id="CM2092_4_readout_reentry",
            countermodel="observable map regenerates C_R/V_R after parent variation",
            effect="closure equation is not stable under clocks/rods/source readout",
            blocked_by="variation-before-readout and no-reentry theorem",
            status="RETAINED_UNLESS_FORBIDDEN",
            valid_for_claim=False,
            claim_allowed=False,
        ),
    ]


def finite_intake_rows() -> list[dict[str, object]]:
    specs = [
        ("INT2092_0_ZR_MR2", "Z_R;M_R^2", "finite range/kinetic operator", "positive sourced values or theorem-zero/no-pole certificate"),
        ("INT2092_1_JR_SR", "J_R;S_R components", "source side of C_R'=S_R or finite elliptic equation", "source-map/q_loc/boundary/readout decomposition with units"),
        ("INT2092_2_QR", "Q_R;q_R_hat", "exterior reciprocal hair amplitude", "no-charge theorem or same-frame numeric bound"),
        ("INT2092_3_boundary", "B_R;Pi_R;alpha_boundary_tail", "boundary/corner/local tail", "parent boundary class or absolute finite envelope"),
        ("INT2092_4_tau_R10", "tau_R10;K_R10(lambda)", "short-range alpha(lambda) projection", "kernel, source/test charges and promoted bound curve"),
        ("INT2092_5_tau_PPN", "tau_PPN;C_gamma;C_beta", "PPN residual vector", "weak-field map and same-frame source normalization"),
        ("INT2092_6_tau_clock", "tau_clock", "clock/redshift residual", "clock readout kernel and units"),
        ("INT2092_7_tau_orbital", "tau_orbital", "orbital/precession/timing residual", "orbital response map"),
        ("INT2092_8_no_cancellation", "absolute envelope policy", "prevents tuned cancellations", "all siblings separately bounded or theorem-zero"),
    ]
    return [
        row(
            intake_id=intake_id,
            required_quantity=quantity,
            role=role,
            acceptance_requirement=requirement,
            current_status="SOURCE_BACKED_ROW_MISSING",
            score_ready=False,
            valid_for_claim=False,
            claim_allowed=False,
        )
        for intake_id, quantity, role, requirement in specs
    ]


def branch_dry_run_rows() -> list[dict[str, object]]:
    return [
        row(
            run_id="RUN2092_0_internal_variation",
            branch="micro-kernel algebra",
            input_status="PASS_FORMAL_VARIATION",
            missing_inputs="none for internal variation only",
            result="C_R'=S_R follows inside S_micro",
            pass_status="FORMAL_ONLY_NO_PARENT_CLAIM",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            run_id="RUN2092_1_parent_necessity",
            branch="derive micro-kernel from existing corpus",
            input_status="REFUSED_PARENT_NECESSITY_NOT_DERIVED",
            missing_inputs="object-language constructor list; parent theta/Omega; H_core; Dirac chain; boundary class",
            result="MICRO_KERNEL_IS_NEW_AXIOM_OR_CLOSURE",
            pass_status="NO_CLAIM",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            run_id="RUN2092_2_local_GR",
            branch="C_R=0 local protected exterior",
            input_status="REFUSED_SOURCE_BOUNDARY_GATES_OPEN",
            missing_inputs="S_R zero/bound; q_loc zero/bound; boundary no-charge; reference lock; beta/conservation",
            result="LOCAL_GR_NOT_CLAIMED",
            pass_status="NO_CLAIM",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            run_id="RUN2092_3_finite_intake",
            branch="finite local tests",
            input_status="REFUSED_SOURCE_BACKED_INPUTS_MISSING",
            missing_inputs="Z_R;M_R2;J_R;Q_R;B_R;tau_R10;tau_PPN;tau_clock;tau_orbital",
            result="INTAKE_READY_NO_SCORE",
            pass_status="NO_SCORE",
            q_R_hat_policy_ceiling=str(Q_R_HAT_POLICY_CEILING),
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    gates = [
        ("GATE2092_0_micro_kernel_internal", "micro-kernel variational algebra works", "PASS_FORMAL_NONCLAIM", "internal variation only, not parent derivation"),
        ("GATE2092_1_parent_derived", "micro-kernel is derived from existing MTS corpus", "FAIL_BLOCKED", "parent necessity/object-language not derived"),
        ("GATE2092_2_new_postulate", "micro-kernel may be adopted as explicit new parent postulate", "AVAILABLE_AS_THEORY_CHOICE_NOT_PROOF", "would need user/theory decision and public labeling"),
        ("GATE2092_3_DR", "D_R is parent-derived", "FAIL_BLOCKED", "micro-kernel source remains axiom/closure"),
        ("GATE2092_4_local_GR", "local GR/Newton branch is derived", "FAIL_BLOCKED", "source/boundary/q_loc/beta/conservation gates open"),
        ("GATE2092_5_finite_score", "finite local branch can be scored", "FAIL_BLOCKED", "finite input rows not source-backed"),
    ]
    return [
        row(
            gate_id=gate_id,
            claim=claim,
            status=status,
            reason=reason,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2092_0_result",
            decision="MICRO_KERNEL_FORMAL_PASS_PARENT_DERIVATION_FAIL",
            basis="S_micro=int P_R(C_R'-S_R)dr+B_R has the correct variation, but current evidence does not force it from deeper MTS primitives",
            consequence="do not claim derived local GR from this route",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2092_1_theory_choice",
            decision="MICRO_KERNEL_CAN_BE_AN_EXPLICIT_PARENT_AXIOM_IF_CHOSEN",
            basis="it is minimal, mathematically clean, and directly targets the missing coupling",
            consequence="if adopted, label it as a foundational postulate and still prove source/boundary/no-extra terms",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2092_2_next",
            decision="PIVOT_TO_AXIOM_REVIEW_OR_FINITE_INTAKE",
            basis="the derivation-first route has reached a clean axiom boundary",
            consequence="next checkpoint should either write the explicit axiom-review page or start sourcing finite local-test inputs",
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2092_0_2093",
            target_doc="2093-Y5-R2FR-radial-micro-kernel-axiom-review-or-finite-local-input-runner.md",
            target_script="scripts/Y5_R2FR_radial_micro_kernel_axiom_review_or_finite_local_input_runner_2093.py",
            objective="decide whether the minimal radial micro-kernel is acceptable as an explicit parent postulate, with its axiom cost and countermodels, or pivot to finite local-test input acquisition for Z_R/M_R2/J_R/Q_R/S_R and arena projections",
            success_condition="clear axiom/adoption ledger or strict source-backed finite input runner; no local-GR claim unless parent derivation or complete finite evidence exists",
            forbidden_shortcuts="calling the micro-kernel derived; hiding axiom cost; GR import; Schwarzschild gauge; plateau axiom; placeholder finite scores; GitHub; formalization-workbench edits",
            claim_allowed=False,
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    kernel: list[dict[str, object]],
    costs: list[dict[str, object]],
    counters: list[dict[str, object]],
    finite: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            SOURCE_WEIGHT_DOCS / "AFRAME_MINIMAL_RADIAL_MICRO_KERNEL_2092_NONCLAIM.csv",
            kernel + costs + counters,
            "source_weight_docs",
        ),
        (
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2092_MICRO_KERNEL_NONCLAIM.csv",
            kernel + counters + finite,
            "branch_locked_wep",
        ),
        (
            QUEUE / "JR2092_FINITE_LOCAL_INPUT_INTAKE_QUEUE.csv",
            costs + finite + decisions + next_rows_,
            "rab_acquisition_queue",
        ),
    ]
    rows: list[dict[str, object]] = []
    for path, data_rows, copy_kind in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=f"COPY2092_{len(rows)}",
                copy_kind=copy_kind,
                path=str(path),
                rows=len(data_rows),
                parses=csv_rows_parse(path),
                valid_for_claim=False,
                claim_allowed=False,
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    kernel: list[dict[str, object]],
    costs: list[dict[str, object]],
    counters: list[dict[str, object]],
    finite: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(truthy(r["path_exists"]) and truthy(r["needle_found"]) for r in sources)
    kernel_action_ok = any(
        r["kernel_id"] == "MK2092_1_action"
        and "P_R(partial_r C_R-S_R" in str(r["statement"])
        and "H_R=P_R S_R" in str(r["calculation_or_variation"])
        for r in kernel
    )
    variation_ok = any(r["kernel_id"] == "MK2092_2_delta_PR" and "C_R'=S_R" in str(r["calculation_or_variation"]) for r in kernel)
    status_ok = any(r["kernel_id"] == "MK2092_5_status" and r["result"] == "MINIMAL_AXIOM_OR_CLOSURE_NOT_DERIVATION" for r in kernel)
    costs_ok = len(costs) >= 5 and all(str(r["status"]) == "AXIOM_COST_EXPLICIT" for r in costs)
    counters_ok = all(str(r["status"]) == "RETAINED_UNLESS_FORBIDDEN" for r in counters)
    finite_ok = len(finite) >= 8 and all(not truthy(r["score_ready"]) for r in finite)
    formal_pass_nonclaim = any(r["run_id"] == "RUN2092_0_internal_variation" and r["input_status"] == "PASS_FORMAL_VARIATION" for r in runs)
    parent_refused = any(r["run_id"] == "RUN2092_1_parent_necessity" and str(r["input_status"]).startswith("REFUSED") for r in runs)
    gates_safe = all(not truthy(r["claim_allowed"]) for r in gates) and any(r["gate_id"] == "GATE2092_1_parent_derived" and str(r["status"]).startswith("FAIL_BLOCKED") for r in gates)
    decision_ok = any(r["decision_id"] == "DEC2092_0_result" for r in decisions)
    next_ok = next_rows_[0]["target_id"] == "NEXT2092_0_2093"
    copies_ok = all(truthy(r["parses"]) and Path(str(r["path"])).exists() for r in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(r.get("claim_allowed")) and not truthy(r.get("valid_for_claim"))
        for group in [sources, kernel, costs, counters, finite, runs, gates, decisions, next_rows_, copies]
        for r in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2092_artifacts()
    pycache_clean = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2092_00_sources", source_ok, "all cited sources exist and contain required needles"),
        ("VAL2092_01_kernel_action", kernel_action_ok, "minimal micro-kernel action is present"),
        ("VAL2092_02_variation", variation_ok, "P_R variation gives C_R'=S_R"),
        ("VAL2092_03_status", status_ok, "micro-kernel is not promoted as derivation"),
        ("VAL2092_04_axiom_cost", costs_ok, "axiom costs are explicit"),
        ("VAL2092_05_countermodels", counters_ok, "countermodels remain retained unless forbidden"),
        ("VAL2092_06_finite_intake", finite_ok, "finite local input rows are non-score-ready"),
        ("VAL2092_07_formal_pass_nonclaim", formal_pass_nonclaim, "internal variation pass remains nonclaim"),
        ("VAL2092_08_parent_refused", parent_refused, "parent necessity is refused"),
        ("VAL2092_09_claim_gates", gates_safe, "claim gates do not allow local claims"),
        ("VAL2092_10_decision", decision_ok, "decision ledger records formal-pass/derivation-fail"),
        ("VAL2092_11_next", next_ok, "next target is 2093 axiom review or finite input runner"),
        ("VAL2092_12_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2092_13_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2092_14_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2092_15_formalization_clean", formalization_clean, "formalization-workbench untouched by 2092"),
        ("VAL2092_16_no_pycache", pycache_clean, "scripts __pycache__ removed"),
    ]
    rows = [
        row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail, claim_allowed=False, valid_for_claim=False)
        for check_id, passed, detail in checks
    ]
    overall = all(r["status"] == "PASS" for r in rows)
    rows.append(
        row(
            check_id="VAL2092_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2092 constructs the minimal radial micro-kernel, records formal-pass/parent-derivation-fail, and keeps finite local intake nonclaim" if overall else "one or more 2092 validation gates failed",
            claim_allowed=False,
            valid_for_claim=False,
        )
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    kernel: list[dict[str, object]],
    costs: list[dict[str, object]],
    counters: list[dict[str, object]],
    finite: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 2092 - Y5/R2FR Minimal Radial Parent Micro-Kernel Or Finite Input Intake",
            "## Current Verdict\n\n2092 constructs the smallest honest block that would make the local reciprocity selector real: `S_micro=int dr P_R(partial_r C_R-S_R)+B_R`, with `C_R=ln(T^2S)` and `P_R=V_R/2`. The variation works: `delta P_R` gives `C_R'=S_R`, and with `S_R=0`, a fixed reference, and boundary no-charge, the protected local exterior gives `C_R=0`.\n\nBut this is not yet a derivation from the existing corpus. It is a clean parent micro-kernel candidate. To use it honestly, MTS must either adopt it as an explicit foundational postulate and pay the axiom cost, or derive it from a deeper object-language/constraint grammar. Otherwise the only honest route is finite residual input acquisition for R10/PPN/clock/orbital tests.",
            "## Source Register",
            md_table(sources, ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_2092", "valid_for_claim", "claim_allowed"]),
            "## Minimal Micro-Kernel",
            md_table(kernel, ["kernel_id", "object", "statement", "calculation_or_variation", "result", "parent_status", "claim_allowed", "valid_for_claim"]),
            "## Axiom Cost Ledger",
            md_table(costs, ["cost_id", "added_assumption", "why_needed", "scrutiny_risk", "mitigation", "status", "valid_for_claim"]),
            "## Countermodel Audit",
            md_table(counters, ["countermodel_id", "countermodel", "effect", "blocked_by", "status", "valid_for_claim"]),
            "## Finite Input Intake",
            md_table(finite, ["intake_id", "required_quantity", "role", "acceptance_requirement", "current_status", "score_ready", "valid_for_claim"]),
            "## Branch Dry Runs",
            md_table(runs, ["run_id", "branch", "input_status", "missing_inputs", "result", "pass_status", "q_R_hat_policy_ceiling", "claim_allowed", "valid_for_claim"]),
            "## Claim Gates",
            md_table(gates, ["gate_id", "claim", "status", "reason", "claim_allowed", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "basis", "consequence", "claim_allowed", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows_, ["target_id", "target_doc", "target_script", "objective", "success_condition", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "copy_kind", "path", "rows", "parses", "valid_for_claim", "claim_allowed"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
        ]
    )
    DOC.write_text(text + "\n", encoding="utf-8")


def main() -> None:
    remove_pycache()
    sources = source_register_rows()
    kernel = micro_kernel_rows()
    costs = axiom_cost_rows()
    counters = countermodel_rows()
    finite = finite_intake_rows()
    runs = branch_dry_run_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2092_SOURCE_REGISTER.csv",
        "kernel": OUT / "P8_Y5_PARENT_QLOC_2092_MINIMAL_MICRO_KERNEL.csv",
        "costs": OUT / "P8_Y5_PARENT_QLOC_2092_AXIOM_COST_LEDGER.csv",
        "counters": OUT / "P8_Y5_PARENT_QLOC_2092_COUNTERMODEL_AUDIT.csv",
        "finite": OUT / "P8_Y5_PARENT_QLOC_2092_FINITE_INPUT_INTAKE.csv",
        "runs": OUT / "P8_Y5_PARENT_QLOC_2092_BRANCH_DRY_RUNS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2092_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2092_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2092_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2092_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2092_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["kernel"], kernel)
    write_csv(paths["costs"], costs)
    write_csv(paths["counters"], counters)
    write_csv(paths["finite"], finite)
    write_csv(paths["runs"], runs)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(kernel, costs, counters, finite, decisions, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, kernel, costs, counters, finite, runs, gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, kernel, costs, counters, finite, runs, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
