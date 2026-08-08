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


DOC = ROOT / "2091-Y5-R2FR-radial-canonical-pair-source-hunt-or-finite-residual-lock.md"
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


def formalization_has_2091_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2091-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2091*",
        "*Y5_R2FR_radial_canonical_pair_source_hunt_or_finite_residual_lock_2091*",
        "*AFRAME_RADIAL_CANONICAL_PAIR_SOURCE_HUNT_2091*",
        "*JR2091_FINITE_RESIDUAL_INPUT_LOCK*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2091_00_2090_handoff",
            ROOT / "2090-Y5-R2FR-selector-cross-term-parent-origin-or-object-language-closure-lock.md",
            ["NEXT2090_0_2091", "PKG2090_0_parent_theta", "VAL2090_OVERALL"],
            "2090 selects radial canonical pair source hunt.",
        ),
        (
            "SRC2091_01_2089_selector",
            ROOT / "2089-Y5-R2FR-parent-Euler-source-map-contract-integration-or-finite-trace-input-lock.md",
            ["CER2089_2_selector_cross_term_contract", "PEG2089_1_selector_cross_term", "VAL2089_OVERALL"],
            "2089 extracts the selector cross-term before canonical rewrite.",
        ),
        (
            "SRC2091_02_1008_theta",
            ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            ["PVA1008_1_theta_MTS", "PVA1008_6_verdict", "CG1008_0_parent_theta"],
            "parent theta_MTS extraction attempted and refused as incomplete.",
        ),
        (
            "SRC2091_03_1009_current_chain",
            ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            ["PCS1009_9_total_parent_contract", "SVC1009_6_total_parent_switch_unsigned", "CG1009_1_theta_MTS"],
            "parent current-chain action contract exists as unsigned sector variation contract.",
        ),
        (
            "SRC2091_04_1564_presymplectic",
            ROOT / "1564-Y5-RAB-vertical-null-presymplectic-degeneracy-or-finite-ZR-intake.md",
            ["NULL1564_0_parent_L_theta", "NULL1564_5_verdict", "VAL1564_OVERALL"],
            "vertical-null/presymplectic route shows missing L/theta/Omega and v_R.",
        ),
        (
            "SRC2091_05_1273_Hcore",
            ROOT / "1273-Y5-R10-RAB-parent-Hcore-radial-cell-owner-or-finite-residual-source-acquisition.md",
            ["HCO1273_0_u_absent", "HCO1273_6_classification_verdict", "VAL1273_11_overall"],
            "ordinary H_core classification rejects theorem-zero without constraint/multiplier/unimodular grammar.",
        ),
        (
            "SRC2091_06_1248_Dirac",
            ROOT / "1248-Y5-R10-minimal-lambdaR-parent-action-ansatz-and-Dirac-check.md",
            ["DIR1248_2_preservation", "DEC1248_0_ansatz_not_enough", "DEC1248_2_keep_parent_repair_path"],
            "minimal multiplier ansatz passes formally but cannot be parent-promoted.",
        ),
        (
            "SRC2091_07_1273_Dirac_csv",
            OUT / "P8_Y5_R10_1273_DIRAC_PRESERVATION_AUDIT.csv",
            ["DPA1273_2_preservation", "DPA1273_5_conditional_theorem"],
            "machine-readable Dirac preservation blocker.",
        ),
        (
            "SRC2091_08_1866_selector",
            ROOT / "1866-Y5-R2FR-reciprocity-selector-operator-or-Hcore-source-equation.md",
            ["RSA1866_5_verdict", "CG1866_0_selector", "VAL1866_OVERALL"],
            "reciprocity selector remains nonclaim.",
        ),
        (
            "SRC2091_09_1577_current",
            ROOT / "1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md",
            ["RCC1577_0_current_equation", "NCA1577_4_verdict", "VAL1577_OVERALL"],
            "cell-current route preserves hair without no-charge theorem.",
        ),
        (
            "SRC2091_10_1819_charge",
            ROOT / "1819-Y5-R2FR-local-EH-symplectic-charge-inheritance-or-Cterm-residual-vector.md",
            ["EHC1819_0_target", "EHC1819_6_verdict", "CTA1819_5_verdict"],
            "EH charge inheritance remains exact conditional with C-term residuals.",
        ),
        (
            "SRC2091_11_1622_lambda",
            OUT / "P8_Y5_PARENT_QLOC_1622_LAMBDAR_PARENT_ORIGIN_AUDIT.csv",
            ["ORG1622_4_second_class_auxiliary", "ORG1622_6_verdict"],
            "lambda_R parent origin audit names the strongest auxiliary route but keeps it unsigned.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="radial_canonical_pair_source_hunt",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2091=note,
                valid_for_claim=False,
                claim_allowed=False,
            )
        )
    return rows


def no_free_lunch_rows() -> list[dict[str, object]]:
    return [
        row(
            theorem_id="NFL2091_0_required_parent_package",
            statement="A derived selector requires a parent-owned radial canonical package, not only the algebraic identity L_sel=P_R(C_R'-S_R).",
            proof_or_reason="The algebra fixes what would work; derivation requires delta L_parent=E_A delta Phi^A+d theta_MTS with theta_R=int P_R delta C_R as a sector of theta_MTS.",
            status="EXACT_REQUIREMENT",
            missing_or_blocked="MISSING_PARENT_L_THETA_OMEGA",
            consequence="2091 cannot promote D_R without a source path for theta_R",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            theorem_id="NFL2091_1_full_phase_volume_no_owner",
            statement="Full radial phase-volume preservation still does not own theta_R.",
            proof_or_reason="J_q J_p=1 holds for any p, so Liouville/canonical particle phase-volume cancels the radial cell factor instead of selecting C_R=ln(T^2S).",
            status="NO_GO_RETAINED",
            missing_or_blocked="SEPARATE_CONFIGURATION_CELL_THEOREM_MISSING",
            consequence="do not use generic symplectic preservation as parent source for P_R delta C_R",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            theorem_id="NFL2091_2_covariant_phase_space_no_owner",
            statement="Covariant phase-space language can host theta_R only after the parent sector variation is explicit.",
            proof_or_reason="1008/1009 keep theta_MTS and sector charges as contracts; EH theta alone is a reference pattern, not the MTS radial sector.",
            status="HOST_AVAILABLE_NOT_EXTRACTED",
            missing_or_blocked="MISSING_SECTOR_VARIATION_AND_THETA_R_COMPONENT",
            consequence="theta_R cannot be imported from EH or generic CPS formalism",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            theorem_id="NFL2091_3_first_order_ansatz_no_owner",
            statement="The first-order action S=int(P_R C_R'-P_R S_R) proves the equation only inside the ansatz.",
            proof_or_reason="Variation in P_R gives C_R'=S_R, but the ansatz itself supplies the wanted canonical one-form and Hamiltonian by hand.",
            status="FORMAL_PASS_NOT_DERIVATION",
            missing_or_blocked="MISSING_PARENT_NECESSITY_OF_FIRST_ORDER_BLOCK",
            consequence="closure template only until parent object-language or Dirac chain signs it",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            theorem_id="NFL2091_4_Hcore_classification",
            statement="An ordinary unconstrained H_core does not derive C_R=0 or C_R'=S_R exactly.",
            proof_or_reason="1273 classifies ordinary H_core: u absent gives no equation, smooth potential gives finite residual, kinetic/current terms give hair, multiplier/unimodular routes remain conditional.",
            status="ORDINARY_HCORE_REJECTED_FOR_THEOREM_ZERO",
            missing_or_blocked="MISSING_CONSTRAINT_OR_OBJECT_LANGUAGE_OR_AUXILIARY_ORIGIN",
            consequence="do not keep circling ordinary H_core as if it will magically become GR",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            theorem_id="NFL2091_5_boundary_nocharge_separate",
            statement="Even with theta_R and H_R, local GR needs boundary/no-charge silence.",
            proof_or_reason="The variation carries [P_R delta C_R]_boundary and the current branch leaves Q_R hair unless source-neutral boundary class is proven.",
            status="SEPARATE_REQUIRED_GATE",
            missing_or_blocked="MISSING_BOUNDARY_NO_CHARGE_THEOREM",
            consequence="exact branch must still prove Q_R=0 or finite branch must bound q_R_hat/Q_R",
            valid_for_claim=False,
            claim_allowed=False,
        ),
    ]


def source_hunt_rows() -> list[dict[str, object]]:
    return [
        row(
            hunt_id="HUNT2091_0_parent_theta",
            target="theta_R=int P_R delta C_R",
            candidate_source="parent theta_MTS extraction",
            current_evidence="1008 PVA1008_1 and 1009 PCS1009_9 define a total parent theta contract but do not extract sector theta_R",
            verdict="NOT_FOUND_CURRENT_CORPUS",
            required_to_close="explicit parent Lagrangian, field list, variation variables, sector theta_R component, source/equation path",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            hunt_id="HUNT2091_1_parent_HR",
            target="H_R=P_R S_R",
            candidate_source="H_core/L_core radial-cell owner",
            current_evidence="1273 rejects ordinary H_core theorem-zero; 1866 marks signed Hcore missing; 2089 treats S_R as residual ledger",
            verdict="NOT_FOUND_CURRENT_CORPUS",
            required_to_close="parent H_core term linear in P_R with S_R decomposed into source, q_loc, boundary, readout and coefficient slots",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            hunt_id="HUNT2091_2_object_language",
            target="C_R is compatibility data, not independent scalar",
            candidate_source="typed parent constructor list",
            current_evidence="1257/1622/1866 select this as low-scrutiny route but mark constructor list unsigned",
            verdict="BEST_ROUTE_STILL_UNSIGNED",
            required_to_close="allowed primitives, allowed contractions, allowed measures, forbidden derivative terms, source/matter descent and readout stability",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            hunt_id="HUNT2091_3_Dirac",
            target="closed preservation chain for C_R/P_R or lambda_R",
            candidate_source="multiplier/Dirac preservation",
            current_evidence="1248 and 1273 pass only inside ansatz; preservation, class and boundary are blocked",
            verdict="FORMAL_ONLY_NOT_PARENT_SIGNED",
            required_to_close="canonical bracket table, H_core, constraint class, degree count, matter/source and boundary compatibility",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            hunt_id="HUNT2091_4_presymplectic_null",
            target="R_AB/C_R is vertical-null representative",
            candidate_source="ker(Dq)=ker(Omega_parent) with v_R generator",
            current_evidence="1564 gives conditional contradiction but lacks L/theta/Omega, v_R, no-vertical-metric and boundary-zero proofs",
            verdict="CONDITIONAL_FOOTHOLD_NOT_PARENT_PROOF",
            required_to_close="parent Omega, field-by-field v_R, no vertical metric/connection, zero boundary charge, readout stability",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            hunt_id="HUNT2091_5_current_nocharge",
            target="Q_R=0 after cell-current equation",
            candidate_source="radial observer-cell current",
            current_evidence="1577 derives conserved charge only; no-charge theorem not derived",
            verdict="CURRENT_ROUTE_FAILS_EXACT_CLAIM",
            required_to_close="source-neutral boundary class, auxiliary elimination before current formation, or parent cell grammar",
            valid_for_claim=False,
            claim_allowed=False,
        ),
    ]


def closure_lock_rows() -> list[dict[str, object]]:
    return [
        row(
            lock_id="LOCK2091_0_selector_status",
            object="L_sel=P_R(C_R'-S_R)",
            status="CLOSURE_TEMPLATE_ONLY",
            reason="exact conditional action works, but no parent source path for theta_R/H_R is present",
            allowed_use="organize residuals and define what future parent action must prove",
            forbidden_use="local-GR/Newton derivation claim",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            lock_id="LOCK2091_1_Delta_sel",
            object="Delta_sel",
            status="RETAINED_RESIDUAL",
            reason="all departures from parent-owned theta_R/H_R/no-extra-V_R are collected as selector defect",
            allowed_use="finite residual accounting",
            forbidden_use="set to zero by notation or plateau axiom",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            lock_id="LOCK2091_2_DR",
            object="D_R[MTS]=partial_r C_R-S_R",
            status="EXACT_CONDITIONAL_NOT_DERIVED",
            reason="D_R follows from closure template but not from current parent action",
            allowed_use="benchmark equation for theorem route and residual decomposition",
            forbidden_use="parent Euler equation claim",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            lock_id="LOCK2091_3_local_branch",
            object="local GR/Newton/R10/PPN/clock/orbital",
            status="BLOCKED_NONCLAIM",
            reason="selector, q_loc, source-map, boundary, beta/conservation, and arena projection gates remain open",
            allowed_use="private derivation discipline and finite input planning",
            forbidden_use="public pass or benchmark win",
            valid_for_claim=False,
            claim_allowed=False,
        ),
    ]


def finite_lock_rows() -> list[dict[str, object]]:
    specs = [
        ("FIN2091_0_ZR", "Z_R", "reciprocal gradient/kinetic stiffness", "theorem Z_R=0 or positive numeric source with units and parent normalization"),
        ("FIN2091_1_MR2", "M_R^2", "mass/stiffness for finite suppression length", "theorem no-pole or numeric positive source with units"),
        ("FIN2091_2_JR", "J_R or S_R source", "bulk source term driving C_R/R_AB", "matter descent/source-map coefficient or zero theorem"),
        ("FIN2091_3_QR", "Q_R/q_R_hat", "exterior reciprocal hair amplitude", "boundary no-charge theorem or numeric same-frame bound"),
        ("FIN2091_4_boundary", "B_R/Pi_R/alpha_boundary_tail", "boundary/corner/readout tail", "parent boundary class or absolute finite bound"),
        ("FIN2091_5_q_loc", "epsilon_GK_q_loc", "Gamma/Khat local force residual inside S_R", "parent-zero theorem or arena-bound profile"),
        ("FIN2091_6_coeff_variation", "Delta_coeff/Schur terms", "coefficient variation and Hessian leakage", "parent second-variation source rows"),
        ("FIN2091_7_tau_R10", "tau_R10 and K_R10(lambda)", "short-range alpha(lambda) projection", "source-backed kernel and promoted bound curve"),
        ("FIN2091_8_tau_PPN", "tau_PPN/C_gamma/C_beta", "post-Newtonian residual vector", "same-frame weak-field map"),
        ("FIN2091_9_tau_clock", "tau_clock", "clock/redshift/frequency residual", "clock readout kernel and source units"),
        ("FIN2091_10_tau_orbital", "tau_orbital", "orbital/precession/timing residual", "same-frame orbital acceleration/precession map"),
    ]
    return [
        row(
            requirement_id=req_id,
            quantity=quantity,
            role=role,
            required_before_scoring=required,
            current_status="MISSING_SOURCE_BACKED_INPUT_OR_THEOREM_ZERO",
            score_ready=False,
            valid_for_claim=False,
            claim_allowed=False,
        )
        for req_id, quantity, role, required in specs
    ]


def branch_dry_run_rows() -> list[dict[str, object]]:
    return [
        row(
            run_id="RUN2091_0_parent_theta",
            branch="parent theta_R source",
            input_status="REFUSED_MISSING_PARENT_THETA_R",
            missing_inputs="explicit L_parent; theta_MTS; theta_R sector; field list; variation variables; source/equation path",
            result="NO_PARENT_SOURCE_FOUND",
            pass_status="NO_CLAIM",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            run_id="RUN2091_1_parent_HR",
            branch="parent H_R=P_R S_R source",
            input_status="REFUSED_MISSING_PARENT_HR",
            missing_inputs="H_core/L_core; S_R decomposition; q_loc/source/boundary/readout slots; no-extra-V_R clause",
            result="NO_PARENT_SOURCE_FOUND",
            pass_status="NO_CLAIM",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            run_id="RUN2091_2_object_language",
            branch="typed compatibility grammar",
            input_status="REFUSED_MISSING_CONSTRUCTOR_LIST",
            missing_inputs="allowed primitives; contractions; measures; forbidden derivative terms; readout stability",
            result="BEST_ROUTE_UNSIGNED",
            pass_status="NO_CLAIM",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            run_id="RUN2091_3_finite_residual",
            branch="finite local residual scoring",
            input_status="REFUSED_SOURCE_BACKED_FINITE_ROWS_MISSING",
            missing_inputs="Z_R;M_R2;J_R;Q_R;B_R;q_loc;tau_R10;tau_PPN;tau_clock;tau_orbital",
            result="LOCKED_INPUT_ONLY",
            pass_status="NO_SCORE",
            q_R_hat_policy_ceiling=str(Q_R_HAT_POLICY_CEILING),
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    gates = [
        ("GATE2091_0_theta", "theta_R is parent-derived", "FAIL_BLOCKED", "theta_MTS/theta_R extraction not found"),
        ("GATE2091_1_HR", "H_R=P_R S_R is parent-derived", "FAIL_BLOCKED", "H_core/L_core and S_R source map not found"),
        ("GATE2091_2_selector", "selector cross-term is parent-owned", "FAIL_BLOCKED", "theta_R and H_R both missing"),
        ("GATE2091_3_DR", "D_R is a derived parent Euler equation", "FAIL_BLOCKED", "selector remains closure template"),
        ("GATE2091_4_local_GR", "local GR/Newton branch is derived", "FAIL_BLOCKED", "selector, boundary, q_loc/source, beta/conservation gates open"),
        ("GATE2091_5_finite_score", "finite local residual branch can be scored", "FAIL_BLOCKED", "finite source-backed rows missing"),
        ("GATE2091_6_public", "public claim allowed", "FAIL_BLOCKED", "private nonclaim checkpoint only"),
    ]
    return [
        row(
            gate_id=gate_id,
            claim=claim,
            status=status,
            blocking_reason=reason,
            required_before_claim="parent-signed exact package or complete source-backed finite residual inputs",
            claim_allowed=False,
            valid_for_claim=False,
        )
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2091_0_source_hunt_result",
            decision="RADIAL_CANONICAL_PAIR_SOURCE_NOT_FOUND_CURRENT_CORPUS",
            basis="1008/1009/1564/1273/1248/1866/1577 provide contracts and conditional footholds but no parent theta_R/H_R source",
            consequence="selector is locked as closure template, not proof",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2091_1_progress_kept",
            decision="NO_FREE_LUNCH_LEMMA_RETAINED",
            basis="generic phase-volume, EH import, ordinary H_core, and bare multiplier are each insufficient for theorem-zero",
            consequence="future work cannot pretend the coupling is derived unless it supplies the exact package",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2091_2_next_best",
            decision="MOVE_TO_PARENT_ACTION_MICRO_KERNEL_OR_FINITE_INPUTS",
            basis="either construct a tiny parent micro-kernel containing theta_R/H_R, or stop derivation-first and source finite residual rows",
            consequence="2092 should attempt a minimal parent micro-kernel with explicit assumptions and countermodels",
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2091_0_2092",
            target_doc="2092-Y5-R2FR-minimal-radial-parent-micro-kernel-or-finite-input-intake.md",
            target_script="scripts/Y5_R2FR_minimal_radial_parent_micro_kernel_or_finite_input_intake_2092.py",
            objective="attempt a minimal parent micro-kernel that explicitly owns theta_R=int P_R delta C_R, H_R=P_R S_R, no-extra-V_R terms, and boundary class; if this cannot be justified, pivot to finite Z_R/M_R2/J_R/Q_R/S_R/tau input acquisition",
            success_condition="micro-kernel with declared primitives, variation, boundary, source-map and countermodel audit; or strict finite input intake pack with all rows nonclaim",
            forbidden_shortcuts="GR radial identity import; Schwarzschild gauge; plateau axiom; generic symplectic preservation; bare multiplier as proof; finite scoring with placeholders; GitHub; formalization-workbench edits",
            claim_allowed=False,
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    nfl: list[dict[str, object]],
    hunt: list[dict[str, object]],
    locks: list[dict[str, object]],
    finite: list[dict[str, object]],
    runs: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            SOURCE_WEIGHT_DOCS / "AFRAME_RADIAL_CANONICAL_PAIR_SOURCE_HUNT_2091_NONCLAIM.csv",
            nfl + hunt + locks,
            "source_weight_docs",
        ),
        (
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2091_RADIAL_CANONICAL_PAIR_NONCLAIM.csv",
            hunt + locks + finite + runs,
            "branch_locked_wep",
        ),
        (
            QUEUE / "JR2091_FINITE_RESIDUAL_INPUT_LOCK_QUEUE.csv",
            locks + finite + next_rows_,
            "rab_acquisition_queue",
        ),
    ]
    rows: list[dict[str, object]] = []
    for path, data_rows, copy_kind in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=f"COPY2091_{len(rows)}",
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
    nfl: list[dict[str, object]],
    hunt: list[dict[str, object]],
    locks: list[dict[str, object]],
    finite: list[dict[str, object]],
    runs: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(truthy(r["path_exists"]) and truthy(r["needle_found"]) for r in sources)
    no_free_lunch_ok = any(r["theorem_id"] == "NFL2091_0_required_parent_package" for r in nfl) and any(
        r["theorem_id"] == "NFL2091_4_Hcore_classification" for r in nfl
    )
    theta_refused = any(r["hunt_id"] == "HUNT2091_0_parent_theta" and r["verdict"] == "NOT_FOUND_CURRENT_CORPUS" for r in hunt)
    h_refused = any(r["hunt_id"] == "HUNT2091_1_parent_HR" and r["verdict"] == "NOT_FOUND_CURRENT_CORPUS" for r in hunt)
    closure_locked = any(r["lock_id"] == "LOCK2091_0_selector_status" and r["status"] == "CLOSURE_TEMPLATE_ONLY" for r in locks)
    finite_required = len(finite) >= 10 and all(str(r["current_status"]).startswith("MISSING") and not truthy(r["score_ready"]) for r in finite)
    dry_refused = all(str(r["input_status"]).startswith("REFUSED") for r in runs)
    gates_block = all(str(r["status"]).startswith("FAIL_BLOCKED") and not truthy(r["claim_allowed"]) for r in claim_gates)
    decision_ok = any(r["decision_id"] == "DEC2091_0_source_hunt_result" for r in decisions)
    next_ok = next_rows_[0]["target_id"] == "NEXT2091_0_2092"
    copies_ok = all(truthy(r["parses"]) and Path(str(r["path"])).exists() for r in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(r.get("claim_allowed")) and not truthy(r.get("valid_for_claim"))
        for group in [sources, nfl, hunt, locks, finite, runs, claim_gates, decisions, next_rows_, copies]
        for r in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2091_artifacts()
    pycache_clean = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2091_00_sources", source_ok, "all cited sources exist and contain required needles"),
        ("VAL2091_01_no_free_lunch", no_free_lunch_ok, "no-free-lunch/source requirement rows are present"),
        ("VAL2091_02_theta_refused", theta_refused, "theta_R source hunt is refused, not promoted"),
        ("VAL2091_03_HR_refused", h_refused, "H_R source hunt is refused, not promoted"),
        ("VAL2091_04_closure_locked", closure_locked, "selector is locked as closure template only"),
        ("VAL2091_05_finite_required", finite_required, "finite residual input rows are explicit and non-score-ready"),
        ("VAL2091_06_dry_refusal", dry_refused, "dry runs refuse missing parent/source inputs"),
        ("VAL2091_07_claim_gates", gates_block, "all claim gates remain blocked"),
        ("VAL2091_08_decision", decision_ok, "decision ledger records source hunt result"),
        ("VAL2091_09_next", next_ok, "next target is 2092 parent micro-kernel or finite intake"),
        ("VAL2091_10_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2091_11_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2091_12_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2091_13_formalization_clean", formalization_clean, "formalization-workbench untouched by 2091"),
        ("VAL2091_14_no_pycache", pycache_clean, "scripts __pycache__ removed"),
    ]
    rows = [
        row(
            check_id=check_id,
            status="PASS" if passed else "FAIL",
            detail=detail,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for check_id, passed, detail in checks
    ]
    overall = all(r["status"] == "PASS" for r in rows)
    rows.append(
        row(
            check_id="VAL2091_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2091 completes the radial canonical-pair source hunt, locks selector as closure-only, and routes to 2092 micro-kernel or finite input intake" if overall else "one or more 2091 validation gates failed",
            claim_allowed=False,
            valid_for_claim=False,
        )
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    nfl: list[dict[str, object]],
    hunt: list[dict[str, object]],
    locks: list[dict[str, object]],
    finite: list[dict[str, object]],
    runs: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 2091 - Y5/R2FR Radial Canonical Pair Source Hunt Or Finite Residual Lock",
            "## Current Verdict\n\n2091 takes the leap attempt seriously and then fences it honestly. The clean object from 2090, `theta_R=int P_R delta C_R` with `H_R=P_R S_R`, is the right target, but the current corpus does not yet contain a parent source for either piece. Generic phase-volume preservation cancels `J_q` against `J_p`; EH/covariant-phase-space language only gives a reference pattern; ordinary `H_core` makes finite residuals or hair; and the multiplier route works only after it is inserted as an ansatz.\n\nSo the selector is now locked as a closure template, not abandoned and not claimed. This is progress because the next fork is brutally clear: either construct a tiny parent radial micro-kernel that owns `theta_R/H_R/no-extra-V_R/boundary`, or stop derivation-first here and acquire finite residual inputs for R10/PPN/clock/orbital tests.",
            "## Source Register",
            md_table(sources, ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_2091", "valid_for_claim", "claim_allowed"]),
            "## No-Free-Lunch Lemma",
            md_table(nfl, ["theorem_id", "statement", "proof_or_reason", "status", "missing_or_blocked", "consequence", "valid_for_claim"]),
            "## Parent Source Hunt",
            md_table(hunt, ["hunt_id", "target", "candidate_source", "current_evidence", "verdict", "required_to_close", "valid_for_claim"]),
            "## Closure Lock",
            md_table(locks, ["lock_id", "object", "status", "reason", "allowed_use", "forbidden_use", "valid_for_claim"]),
            "## Finite Residual Input Lock",
            md_table(finite, ["requirement_id", "quantity", "role", "required_before_scoring", "current_status", "score_ready", "valid_for_claim"]),
            "## Branch Dry Runs",
            md_table(runs, ["run_id", "branch", "input_status", "missing_inputs", "result", "pass_status", "q_R_hat_policy_ceiling", "claim_allowed", "valid_for_claim"]),
            "## Claim Gates",
            md_table(claim_gates, ["gate_id", "claim", "status", "blocking_reason", "required_before_claim", "claim_allowed", "valid_for_claim"]),
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
    nfl = no_free_lunch_rows()
    hunt = source_hunt_rows()
    locks = closure_lock_rows()
    finite = finite_lock_rows()
    runs = branch_dry_run_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2091_SOURCE_REGISTER.csv",
        "nfl": OUT / "P8_Y5_PARENT_QLOC_2091_NO_FREE_LUNCH_LEMMA.csv",
        "hunt": OUT / "P8_Y5_PARENT_QLOC_2091_PARENT_SOURCE_HUNT.csv",
        "locks": OUT / "P8_Y5_PARENT_QLOC_2091_CLOSURE_LOCK.csv",
        "finite": OUT / "P8_Y5_PARENT_QLOC_2091_FINITE_RESIDUAL_INPUT_LOCK.csv",
        "runs": OUT / "P8_Y5_PARENT_QLOC_2091_BRANCH_DRY_RUNS.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2091_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2091_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2091_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2091_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2091_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["nfl"], nfl)
    write_csv(paths["hunt"], hunt)
    write_csv(paths["locks"], locks)
    write_csv(paths["finite"], finite)
    write_csv(paths["runs"], runs)
    write_csv(paths["claim_gates"], claim_gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(nfl, hunt, locks, finite, runs, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, nfl, hunt, locks, finite, runs, claim_gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, nfl, hunt, locks, finite, runs, claim_gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
