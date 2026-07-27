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


DOC = ROOT / "2089-Y5-R2FR-parent-Euler-source-map-contract-integration-or-finite-trace-input-lock.md"
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


def formalization_has_2089_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2089-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2089*",
        "*Y5_R2FR_parent_Euler_source_map_contract_integration_or_finite_trace_input_lock_2089*",
        "*AFRAME_PARENT_EULER_SOURCE_MAP_2089*",
        "*JR2089_SELECTOR_CROSS_TERM*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2089_00_2088_handoff",
            ROOT / "2088-Y5-R2FR-boundary-source-silence-and-coefficient-variation-owner-or-trace-score-runner.md",
            ["NEXT2088_0_2089", "RUN2088_4_GR_style_equation_difference", "VAL2088_OVERALL"],
            "2088 selects parent Euler/source-map integration rather than another trace-score loop.",
        ),
        (
            "SRC2089_01_1276_contract",
            ROOT / "1276-Y5-R10-RAB-parent-Euler-source-map-contract-or-closure-baseline-scorecard.md",
            ["ESC1276_4_difference_operator", "ESC1276_5_source_map", "VAL1276_11_overall"],
            "older executable parent Euler/source-map contract.",
        ),
        (
            "SRC2089_02_1864_theorem_csv",
            OUT / "P8_Y5_PARENT_QLOC_1864_LOCAL_GR_REDUCTION_THEOREM.csv",
            ["LGT1864_2_DR_normal_form", "LGT1864_4_boundary_no_charge", "LGT1864_6_verdict"],
            "local-GR reduction theorem target in machine-readable form.",
        ),
        (
            "SRC2089_03_1865_euler_difference",
            ROOT / "1865-Y5-R2FR-parent-Euler-difference-normal-form-or-SR-residual-decomposition.md",
            ["DRA1865_0_target", "VOA1865_1_generic_Euler_difference", "VAL1865_OVERALL"],
            "generic Euler-difference no-go and S_R residual decomposition.",
        ),
        (
            "SRC2089_04_1866_selector",
            ROOT / "1866-Y5-R2FR-reciprocity-selector-operator-or-Hcore-source-equation.md",
            ["RSA1866_5_verdict", "CG1866_0_selector", "VAL1866_OVERALL"],
            "reciprocity selector/Hcore source-equation attempt.",
        ),
        (
            "SRC2089_05_1860_qloc_bridge",
            ROOT / "1860-Y5-R2FR-Gamma-Khat-q-loc-action-existence-bridge-to-local-EH-fixed-point.md",
            ["EHB1860_2_Euler_difference", "RET1860_0_epsilon_GK_q_loc", "VAL1860_OVERALL"],
            "q_loc bridge showing the Euler-difference source side remains contaminated unless q_loc is zero or bounded.",
        ),
        (
            "SRC2089_06_1955_same_source",
            ROOT / "1955-Y5-R2FR-local-EH-same-source-map-or-residual-l2-bound.md",
            ["EH1955_6_zero_verdict", "RB1955_0_residual_bound_formula", "VAL1955_OVERALL"],
            "local EH same-source/no-extra-boundary theorem contract.",
        ),
        (
            "SRC2089_07_1957_source_signature",
            ROOT / "1957-Y5-R2FR-source-map-signature-or-residual-current-bound.md",
            ["SM1957_6_verdict", "CUR1957_1_DeltaT_w", "VAL1957_OVERALL"],
            "source-map theorem attempt and residual current ledger.",
        ),
        (
            "SRC2089_08_1289_kmetric",
            ROOT / "1289-Y5-R10-RAB-KL00-response-matrix-source-or-Kmetric-derivative-expansion.md",
            ["KVE1289_2_metric_response_kernels", "DTC1289_2_DeltaK00_template", "VAL1289_10_overall"],
            "most concrete Kmetric/DeltaK derivative expansion status.",
        ),
        (
            "SRC2089_09_observer_contract",
            ROOT / "10-observer-map-symplectic-contract.md",
            ["derive R_AB=0 from the parent theory", "contract not satisfied", "main-workbench promotion not allowed"],
            "observer-map parent-action contract and no-smuggling warning.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path) if path.exists() else ""
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            row(
                source_id=source_id,
                source_path=str(path),
                exists=path.exists(),
                needle_count=len(needles),
                missing_needles=";".join(missing),
                status="EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "SOURCE_OR_NEEDLE_MISSING",
                role=role,
                claim_allowed=False,
            )
        )
    return rows


def coordinate_euler_rotation_rows() -> list[dict[str, object]]:
    return [
        row(
            derivation_id="CER2089_0_variable_definitions",
            statement="Use x=ln(T), y=ln(sqrt(S)), C_R=2(x+y)=ln(T^2 S), and V_R=x-y.",
            derivation="delta x=1/4 delta C_R + 1/2 delta V_R; delta y=1/4 delta C_R - 1/2 delta V_R",
            result="C_R is the reciprocal product variable; V_R is the cone-skew/orientation variable.",
            status="EXACT_CHANGE_OF_VARIABLES",
            implication="the named time/radial Euler difference is tied to V_R variation, not automatically to C_R variation",
            claim_allowed=False,
        ),
        row(
            derivation_id="CER2089_1_Euler_rotation",
            statement="For any reduced local slice S=int dr L(x,y,x',y',...), the Euler variations rotate as E_C=(E_x+E_y)/4 and E_V=(E_x-E_y)/2.",
            derivation="delta S=int dr [E_x delta x + E_y delta y]=int dr [((E_x+E_y)/4)delta C_R + ((E_x-E_y)/2)delta V_R]",
            result="E_time-E_radial=2 E_V in this convention.",
            status="EXACT_VARIATIONAL_IDENTITY",
            implication="a parent V_R equation can legitimately produce the desired E_time-E_radial relation, but only if the parent action has the right V_R selector term",
            claim_allowed=False,
        ),
        row(
            derivation_id="CER2089_2_selector_cross_term_contract",
            statement="A minimal first-order selector L_sel=1/2 V_R(partial_r C_R-S_R) gives E_time-E_radial=partial_r C_R-S_R if no other unsourced V_R terms survive.",
            derivation="E_V=partial L_sel/partial V_R=1/2(partial_r C_R-S_R); since E_time-E_radial=2E_V, D_R[MTS]=partial_r C_R-S_R.",
            result="this is the exact cross-term parent action contract 2089 extracts",
            status="EXACT_IF_PARENT_CROSS_TERM_SIGNED",
            implication="the missing gear is no longer vague: find a parent origin for V_R partial_r C_R and V_R S_R, or keep D_R closure-only",
            claim_allowed=False,
        ),
        row(
            derivation_id="CER2089_3_generic_no_go_retained",
            statement="A generic L(x,y,x',y') does not force E_x-E_y=partial_r C_R-S_R.",
            derivation="generic E_x-E_y=(partial_x-partial_y)L-d/dr[(partial_xprime-partial_yprime)L], matching 1865",
            result="the selector/cross-term is a special parent structure, not a generic variational fact",
            status="NO_GO_GUARD_ACTIVE",
            implication="no GR identity, plateau axiom, or generic-action handwave may promote local GR",
            claim_allowed=False,
        ),
        row(
            derivation_id="CER2089_4_second_order_alternative",
            statement="The second-order route partial_r(W_R partial_r C_R)=J_R remains possible but becomes a finite/no-hair problem.",
            derivation="without a first-order V_R selector, C_R may be governed by an elliptic/current equation requiring W_R>0, source silence, and Q_R=0",
            result="use only with Z/W/J/B/Q/source rows and boundary no-charge theorem",
            status="ALTERNATIVE_CONDITIONAL_NOT_CLOSED",
            implication="second-order branch is not derived local GR unless no-hair and source/boundary gates close",
            claim_allowed=False,
        ),
    ]


def parent_euler_gate_rows() -> list[dict[str, object]]:
    return [
        row(
            gate_id="PEG2089_0_parent_local_action",
            required_object="explicit S_parent^local or H_core",
            needed_for="compute E_time and E_radial without importing GR",
            current_evidence="1276/1865/1866 all record L_MTS_core/H_core as missing or formal-only.",
            status="MISSING_PARENT_LOCAL_ACTION",
            claim_effect="D_R cannot be a derived parent equation",
            next_action="source a real parent local action block or keep selector contract conditional",
            claim_allowed=False,
        ),
        row(
            gate_id="PEG2089_1_selector_cross_term",
            required_object="parent-owned L_sel=1/2 V_R(partial_r C_R-S_R) or equivalent constraint orientation",
            needed_for="make E_time-E_radial select the reciprocal product variable C_R",
            current_evidence="2089 derives the exact contract; 1866 found no signed selector origin.",
            status="CONTRACT_EXTRACTED_NOT_PARENT_SIGNED",
            claim_effect="local GR route has a precise missing parent term",
            next_action="hunt this term in observer-map symplectic/object-language/multiplier sectors",
            claim_allowed=False,
        ),
        row(
            gate_id="PEG2089_2_source_map_SR",
            required_object="S_R[source,residual,boundary,readout] decomposition with zero or bounded components",
            needed_for="integrate D_R to C_R=0 rather than source-driven reciprocal hair",
            current_evidence="1865 decomposes S_R; 2088 shows J_R/B_R/coefficient gates block scoring.",
            status="DECOMPOSED_NOT_ZERO_OR_BOUNDED",
            claim_effect="S_R remains an explicit residual vector",
            next_action="carry all S_R components with no-cancellation absolute envelope",
            claim_allowed=False,
        ),
        row(
            gate_id="PEG2089_3_q_loc_slot",
            required_object="epsilon_GK_q_loc theorem-zero or source-backed bound inside S_R",
            needed_for="prevent extra-sector force residual from contaminating Euler difference",
            current_evidence="1860 and 1289 keep q_loc/Kmetric/DeltaK live but nonclaim.",
            status="QLOC_RETAINED_NONCLAIM",
            claim_effect="EH/local-GR inheritance cannot reopen while q_loc is unzeroed/unbounded",
            next_action="map q_loc into S_R coefficient or prove parent-zero via Gamma/Khat metric response",
            claim_allowed=False,
        ),
        row(
            gate_id="PEG2089_4_same_source_map",
            required_object="same EH/GR source map for ordinary matter plus non-Hilbert silence",
            needed_for="make the GR baseline source side fair and non-patchwork",
            current_evidence="1955 theorem contract exact but unsigned; 1957 source-map theorem fails cleanly.",
            status="SOURCE_MAP_SIGNATURE_UNSIGNED",
            claim_effect="source side remains residual-current bounded, not a theorem",
            next_action="attack current-owner/non-Hilbert/readout no-reentry clauses",
            claim_allowed=False,
        ),
        row(
            gate_id="PEG2089_5_boundary_no_charge",
            required_object="Q_R=0, B_R/Pi_R silence, reference subtraction and boundary symplectic no-flux",
            needed_for="turn C_R constant/source-free into C_R=0",
            current_evidence="10/1865/1866/2088 all keep no-charge/boundary class unsigned.",
            status="BOUNDARY_NO_CHARGE_UNSIGNED",
            claim_effect="reciprocal hair or boundary flux remains possible",
            next_action="keep boundary as explicit term in S_R and finite branch",
            claim_allowed=False,
        ),
        row(
            gate_id="PEG2089_6_finite_trace_input_lock",
            required_object="all finite rows for Z_R/M_R/J_R/B_R/Q_R/K_qR/domain constants/q_loc/source currents",
            needed_for="score the finite residual branch without cheating",
            current_evidence="2088 and 1866 keep finite rows source-ready only; no claim-valid coefficients exist.",
            status="FINITE_BRANCH_LOCKED",
            claim_effect="no R10/PPN/clock/orbital/local-GR score",
            next_action="do not run local tests until theorem route or source-backed finite rows exist",
            claim_allowed=False,
        ),
    ]


def sr_residual_integration_rows() -> list[dict[str, object]]:
    return [
        row(
            residual_id="SRI2089_0_selector_defect",
            symbol="Delta_sel",
            definition="failure of the parent V_R equation to equal 1/2(partial_r C_R-S_R)",
            current_status="MISSING_PARENT_SELECTOR_CROSS_TERM",
            source_basis="1865 generic no-go; 1866 selector not derived; 2089 cross-term contract",
            handling="must be zero by parent action or retained as closure defect",
            claim_allowed=False,
        ),
        row(
            residual_id="SRI2089_1_JR_lambda",
            symbol="J_R + lambda_R",
            definition="linear reciprocal source/multiplier terms in the C_R/R_AB sector",
            current_status="MISSING_MATTER_DESCENT_OR_MULTIPLIER_ORIGIN",
            source_basis="1256/1268/1866/2088",
            handling="zero theorem, auxiliary elimination, or absolute source norm required",
            claim_allowed=False,
        ),
        row(
            residual_id="SRI2089_2_q_loc",
            symbol="epsilon_GK_q_loc",
            definition="norm/projection of P_loc(nabla Gamma_eff - div K_hat)",
            current_status="RETAINED_NONCLAIM",
            source_basis="1010/1280/1860/1289",
            handling="q_loc parent-zero theorem or arena-bound profile before local claims",
            claim_allowed=False,
        ),
        row(
            residual_id="SRI2089_3_source_current",
            symbol="DeltaT_source",
            definition="ordinary-matter/source-map residual current after EH/GR baseline subtraction",
            current_status="SOURCE_MAP_SIGNATURE_UNSIGNED",
            source_basis="1955/1957",
            handling="same-source theorem or residual-current envelopes",
            claim_allowed=False,
        ),
        row(
            residual_id="SRI2089_4_extra_stress_l2",
            symbol="P_2 R_extra",
            definition="extra-sector metric residual/stress projected into local observable multipoles",
            current_status="EXTRA_SOURCE_SILENCE_UNSIGNED",
            source_basis="1279/1860/1955",
            handling="on-shell vertical/descent proof or finite l=2 envelope",
            claim_allowed=False,
        ),
        row(
            residual_id="SRI2089_5_boundary_flux",
            symbol="Q_R + Pi_R + B_R",
            definition="reciprocal boundary/no-charge/reference residual",
            current_status="BOUNDARY_CLASS_UNSIGNED",
            source_basis="10/1865/1866/2088",
            handling="boundary object-exhaustion/no-charge theorem or absolute flux rows",
            claim_allowed=False,
        ),
        row(
            residual_id="SRI2089_6_coefficient_variation",
            symbol="Delta_coeff",
            definition="Schur/cross-Hessian/coefficient-variation source terms",
            current_status="PARENT_SECOND_VARIATION_MISSING",
            source_basis="2088",
            handling="Schur complement sign proof or explicit residual component",
            claim_allowed=False,
        ),
        row(
            residual_id="SRI2089_7_readout_projector",
            symbol="Delta_readout",
            definition="readout/projector/mass-normalization leakage after parent variation",
            current_status="READOUT_NO_REENTRY_UNSIGNED",
            source_basis="1276/1860/1957",
            handling="variation-before-readout/no-reentry theorem or finite calibration residual",
            claim_allowed=False,
        ),
    ]


def branch_runner_rows() -> list[dict[str, object]]:
    return [
        row(
            run_id="RUN2089_0_selector_cross_term",
            branch="exact first-order selector",
            contract="L_sel=1/2 V_R(partial_r C_R-S_R); E_time-E_radial=partial_r C_R-S_R",
            input_status="REFUSED_MISSING_PARENT_CROSS_TERM_OR_OBJECT_LANGUAGE_OWNER",
            missing_inputs="parent source path for V_R partial_r C_R; V_R S_R coupling; no extra V_R source; variation convention",
            result="EXACT_CONDITIONAL_NEW_CONTRACT_ONLY",
            pass_status="NO_CLAIM",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2089_1_EH_inheritance",
            branch="local EH fixed-point inheritance",
            contract="A511_0..6 parent-signed with silent extras/source/readout/boundary",
            input_status="REFUSED_A511_NOT_PARENT_SIGNED",
            missing_inputs="EH action ownership; q_loc zero/bound; source map; readout/projector; boundary reference",
            result="BLOCKED_BY_1277_1860_1955_1957",
            pass_status="NO_CLAIM",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2089_2_same_source_theorem",
            branch="EH same-source/no-extra-boundary theorem",
            contract="same source map + extra source silence + no extra boundary l=2 -> residual local-GR branch",
            input_status="REFUSED_SOURCE_MAP_SIGNATURE_UNSIGNED",
            missing_inputs="graph/current owner; non-Hilbert silence; readout no-reentry; boundary uniqueness",
            result="CONTRACT_EXACT_BUT_UNSIGNED",
            pass_status="NO_CLAIM",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2089_3_q_loc_formal_mechanism",
            branch="Gamma/Khat q_loc parent-zero",
            contract="S_GK + metric-response K_hat + Helmholtz + Euler/double-zero + boundary/projector silence",
            input_status="REFUSED_LIVE_GAMMA_KHAT_ADOPTION_NOT_CLOSED",
            missing_inputs="Gamma_eff scalar density; K_hat metric response; DeltaK kernels; source/boundary lock; observable lock",
            result="FORMAL_MECHANISM_RETAINED_NOT_ACTIVATED",
            pass_status="NO_CLAIM",
            claim_allowed=False,
        ),
        row(
            run_id="RUN2089_4_finite_trace_residual",
            branch="finite residual / trace score",
            contract="absolute no-cancellation envelope with sourced coefficients and arena projections",
            input_status="REFUSED_SOURCE_BACKED_FINITE_ROWS_MISSING",
            missing_inputs="Z_R;M_R^2;J_R;B_R;Q_R;K_qR;C_tr;C_P;GM_source;q_loc/source-current envelopes",
            result="LOCKED_INPUT_ONLY",
            pass_status="NO_SCORE",
            q_R_hat_policy_ceiling=Q_R_HAT_POLICY_CEILING,
            claim_allowed=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("GATE2089_0_sources", "all cited sources and needles exist", "PASS_SOURCE_ONLY", "source audit complete for this checkpoint"),
        ("GATE2089_1_selector_contract", "selector cross-term contract is mathematically extracted", "PASS_NONCLAIM", "new exact conditional contract is written"),
        ("GATE2089_2_selector_parent_signed", "selector cross-term is parent-signed", "FAIL_BLOCKED", "no parent source path or object-language owner yet"),
        ("GATE2089_3_DR_derived", "D_R[MTS]=partial_r C_R-S_R is derived", "FAIL_BLOCKED", "selector, source map, q_loc, boundary and readout gates remain open"),
        ("GATE2089_4_source_map_zero", "S_R=0 or bounded", "FAIL_BLOCKED", "S_R components are named but not theorem-zero/source-backed"),
        ("GATE2089_5_local_GR_Newton", "local GR/Newton/PPN/R10 branch can claim pass", "FAIL_BLOCKED", "exact and finite branches remain nonclaim"),
    ]
    return [
        row(
            gate_id=gate_id,
            condition=condition,
            status=status,
            reason=reason,
            claim_allowed=False,
        )
        for gate_id, condition, status, reason in specs
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2089_0_real_progress",
            decision="Promote the selector cross-term to the next exact derivation target, not to a claim.",
            because="2089 derives the coordinate/Euler rotation showing exactly what parent term would make E_time-E_radial select C_R.",
            next_action="hunt parent origin for L_sel=1/2 V_R(partial_r C_R-S_R)",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2089_1_DR_status",
            decision="Keep D_R as an exact conditional contract, not a derived equation.",
            because="the selector term, source map, q_loc, boundary, coefficient variation and readout gates remain unsigned.",
            next_action="use D_R to organize residuals but do not score local tests",
            claim_allowed=False,
        ),
        row(
            decision_id="DEC2089_2_best_route",
            decision="Attack object-language/symplectic origin of the V_R selector next.",
            because="this is now the smallest single parent object that can turn the GR-style route from closure into derivation.",
            next_action="build 2090 selector cross-term parent-origin or closure-lock checkpoint",
            claim_allowed=False,
        ),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2089_0_2090",
            target_doc="2090-Y5-R2FR-selector-cross-term-parent-origin-or-object-language-closure-lock.md",
            target_script="scripts/Y5_R2FR_selector_cross_term_parent_origin_or_object_language_closure_lock_2090.py",
            objective="hunt the parent origin of L_sel=1/2 V_R(partial_r C_R-S_R) in observer-map symplectic structure, object-language radial-cell constraints, multiplier/Dirac preservation, or H_core/L_core; if absent, lock D_R as closure-only and keep finite residual inputs explicit",
            success_condition="source-backed parent selector term or clean closure-only refusal with finite input requirements",
            exclusions="GR radial identity import; Schwarzschild gauge shortcut; plateau axiom; closure q_R=0 as proof; finite trace score with missing rows; GitHub; formalization-workbench edits",
            claim_allowed=False,
        )
    ]


def write_branch_copies(
    coord: list[dict[str, object]],
    gates: list[dict[str, object]],
    sr_rows: list[dict[str, object]],
    runs: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2089_0_source_weight_euler_map",
            SOURCE_WEIGHT_DOCS / "AFRAME_PARENT_EULER_SOURCE_MAP_2089_NONCLAIM.csv",
            coord + gates + sr_rows + runs,
        ),
        (
            "COPY2089_1_wep_euler_map",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2089_EULER_SOURCE_MAP_NONCLAIM.csv",
            gates + sr_rows + runs,
        ),
        (
            "COPY2089_2_queue_2090",
            QUEUE / "JR2089_SELECTOR_CROSS_TERM_OR_CLOSURE_LOCK_QUEUE.csv",
            coord + gates + next_rows_,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, data_rows in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=copy_id,
                path=str(path),
                rows_written=len(data_rows),
                status="WRITTEN_NONCLAIM_COPY",
                claim_allowed=False,
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    coord: list[dict[str, object]],
    gates: list[dict[str, object]],
    sr_rows: list[dict[str, object]],
    runs: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(r["status"] == "EXISTS_NEEDLES_CONFIRMED" for r in sources)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    euler_rotation_ok = any(r["derivation_id"] == "CER2089_1_Euler_rotation" and "E_time-E_radial=2 E_V" in str(r["result"]) for r in coord)
    selector_contract_ok = any(
        r["derivation_id"] == "CER2089_2_selector_cross_term_contract"
        and "L_sel=1/2 V_R" in str(r["statement"])
        and r["status"] == "EXACT_IF_PARENT_CROSS_TERM_SIGNED"
        for r in coord
    )
    generic_guard_ok = any(r["derivation_id"] == "CER2089_3_generic_no_go_retained" for r in coord)
    parent_blockers_ok = all(not truthy(r.get("claim_allowed")) and str(r["status"]) != "PASS_CLAIM" for r in gates)
    sr_components_ok = len(sr_rows) >= 8 and any(r["residual_id"] == "SRI2089_2_q_loc" for r in sr_rows)
    dry_refused = all(str(r["input_status"]).startswith("REFUSED") for r in runs)
    claim_safe = all(not truthy(r.get("claim_allowed")) and not str(r["status"]).startswith("PASS_CLAIM") for r in claim_gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2089_0_2090"
    copies_ok = all(Path(str(r["path"])).exists() and csv_rows_parse(Path(str(r["path"]))) for r in copies)
    no_claims = all(
        not truthy(item.get("claim_allowed")) and not truthy(item.get("valid_for_claim"))
        for collection in [coord, gates, sr_rows, runs, claim_gates, decisions, next_rows_]
        for item in collection
    )
    formalization_clean = count_formalization_modified() == 0
    no_formalization_artifacts = not formalization_has_2089_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()

    checks = [
        ("VAL2089_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2089_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2089_02_euler_rotation", euler_rotation_ok, "C_R/V_R Euler rotation is derived"),
        ("VAL2089_03_selector_contract", selector_contract_ok, "minimal V_R selector cross-term contract is extracted"),
        ("VAL2089_04_generic_no_go", generic_guard_ok, "generic Euler-difference no-go guard remains active"),
        ("VAL2089_05_parent_blockers", parent_blockers_ok, "parent Euler gates remain nonclaim/blocked where unsigned"),
        ("VAL2089_06_sr_components", sr_components_ok, "S_R residual integration includes q_loc/source/boundary/readout slots"),
        ("VAL2089_07_dry_refusal", dry_refused, "all branch dry runs refuse missing inputs"),
        ("VAL2089_08_claim_gates_safe", claim_safe, "claim gates allow no derived local-GR or finite local-test claim"),
        ("VAL2089_09_next_selected", next_ok, "2090 selector cross-term origin target selected"),
        ("VAL2089_10_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2089_11_no_claim_flags", no_claims, "no generated row allows a claim"),
        ("VAL2089_12_formalization_unchanged", formalization_clean, "formalization-workbench modified-file count remains 0"),
        ("VAL2089_13_no_formalization_artifacts", no_formalization_artifacts, "no 2089 artifacts were written under formalization-workbench"),
        ("VAL2089_14_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(status for _, status, _ in checks)
    checks.append(
        (
            "VAL2089_OVERALL",
            overall,
            "2089 integrates parent Euler/source-map work, derives the exact V_R selector cross-term contract, keeps D_R nonclaim, and selects parent-origin hunt for 2090",
        )
    )
    return [
        row(
            check_id=check_id,
            status="PASS" if status else "FAIL",
            detail=detail,
            claim_allowed=False,
        )
        for check_id, status, detail in checks
    ]


def write_doc(
    sources: list[dict[str, object]],
    coord: list[dict[str, object]],
    gates: list[dict[str, object]],
    sr_rows: list[dict[str, object]],
    runs: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2089 Y5 R2FR Parent Euler Source Map Contract Integration Or Finite Trace Input Lock",
        "",
        "## Current Verdict",
        "",
        "2089 makes real mathematical progress but not a claim. In the variables `x=ln(T)`, `y=ln(sqrt(S))`, `C_R=2(x+y)`, and `V_R=x-y`, the time/radial Euler difference is the `V_R` Euler equation: `E_time-E_radial=2E_V`. Therefore the exact parent object we need is a selector/cross term such as `L_sel=1/2 V_R(partial_r C_R-S_R)`.",
        "",
        "If that cross term is parent-signed and no extra `V_R` source survives, then `E_time-E_radial=partial_r C_R-S_R` follows without importing GR. That is the cleanest derivation path found here. Current corpus does not yet source that parent term, so `D_R` remains an exact conditional contract, not a derived local-GR theorem.",
        "",
        "This checkpoint also folds in the newer 2088 source/boundary/coefficient gates and the older 1860/1865/1866/1955/1957 chain. The result is a sharper target: prove the selector cross-term from parent object-language/symplectic/multiplier structure, or lock the local branch as closure-only plus finite residual inputs.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, or public claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "exists", "needle_count", "missing_needles", "status", "role", "claim_allowed", "valid_for_claim"]),
        "## Coordinate Euler Rotation",
        md_table(coord, ["derivation_id", "statement", "derivation", "result", "status", "implication", "claim_allowed", "valid_for_claim"]),
        "## Parent Euler Gates",
        md_table(gates, ["gate_id", "required_object", "needed_for", "current_evidence", "status", "claim_effect", "next_action", "claim_allowed", "valid_for_claim"]),
        "## S_R Residual Integration",
        md_table(sr_rows, ["residual_id", "symbol", "definition", "current_status", "source_basis", "handling", "claim_allowed", "valid_for_claim"]),
        "## Branch Dry Runs",
        md_table(runs, ["run_id", "branch", "contract", "input_status", "missing_inputs", "result", "pass_status", "q_R_hat_policy_ceiling", "claim_allowed", "valid_for_claim"]),
        "## Claim Gates",
        md_table(claim_gates, ["gate_id", "condition", "status", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decisions",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "claim_allowed", "valid_for_claim"]),
        "## Next Target",
        md_table(next_rows_, ["target_id", "target_doc", "target_script", "objective", "success_condition", "exclusions", "claim_allowed", "valid_for_claim"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "path", "rows_written", "status", "claim_allowed", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    coord = coordinate_euler_rotation_rows()
    gates = parent_euler_gate_rows()
    sr_rows = sr_residual_integration_rows()
    runs = branch_runner_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2089_SOURCE_REGISTER.csv",
        "coord": OUT / "P8_Y5_PARENT_QLOC_2089_COORDINATE_EULER_ROTATION.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2089_PARENT_EULER_GATES.csv",
        "sr_rows": OUT / "P8_Y5_PARENT_QLOC_2089_SR_RESIDUAL_INTEGRATION.csv",
        "runs": OUT / "P8_Y5_PARENT_QLOC_2089_BRANCH_DRY_RUNS.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2089_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2089_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2089_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2089_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2089_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["coord"], coord)
    write_csv(paths["gates"], gates)
    write_csv(paths["sr_rows"], sr_rows)
    write_csv(paths["runs"], runs)
    write_csv(paths["claim_gates"], claim_gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(coord, gates, sr_rows, runs, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, coord, gates, sr_rows, runs, claim_gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, coord, gates, sr_rows, runs, claim_gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
