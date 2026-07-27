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


DOC = ROOT / "2090-Y5-R2FR-selector-cross-term-parent-origin-or-object-language-closure-lock.md"
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


def formalization_has_2090_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2090-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2090*",
        "*Y5_R2FR_selector_cross_term_parent_origin_or_object_language_closure_lock_2090*",
        "*AFRAME_SELECTOR_CANONICAL_PAIR_2090*",
        "*JR2090_RADIAL_CANONICAL_PAIR*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2090_00_2089_handoff",
            ROOT / "2089-Y5-R2FR-parent-Euler-source-map-contract-integration-or-finite-trace-input-lock.md",
            ["NEXT2089_0_2090", "CER2089_2_selector_cross_term_contract", "VAL2089_OVERALL"],
            "2089 extracts the exact selector cross-term target.",
        ),
        (
            "SRC2090_01_radial_cell",
            ROOT / "09-hamiltonian-radial-cell-derivation.md",
            ["generic symplectic or Liouville phase-volume preservation does not derive p=1", "radial observer cell", "local GR branch remains promising but conditional"],
            "radial-cell derivation shows the target is separate observer-cell preservation, not full phase-volume preservation.",
        ),
        (
            "SRC2090_02_observer_contract",
            ROOT / "10-observer-map-symplectic-contract.md",
            ["a genuine constraint whose multiplier has a parent origin", "contract not satisfied", "main-workbench promotion not allowed"],
            "observer-map contract states the no-smuggling parent-action conditions.",
        ),
        (
            "SRC2090_03_1866_selector",
            ROOT / "1866-Y5-R2FR-reciprocity-selector-operator-or-Hcore-source-equation.md",
            ["RSA1866_5_verdict", "LOG1866_4_verdict", "VAL1866_OVERALL"],
            "prior reciprocity selector/Hcore attempt keeps the parent origin unsigned.",
        ),
        (
            "SRC2090_04_1257_selector_clauses",
            OUT / "P8_Y5_R10_1257_ZR_LAMBDAR_SELECTOR_CLAUSES.csv",
            ["SEL1257_0_field_exclusion", "SEL1257_1_multiplier_origin"],
            "field-exclusion and multiplier-origin clauses for R_AB/C_R.",
        ),
        (
            "SRC2090_05_1273_Dirac",
            OUT / "P8_Y5_R10_1273_DIRAC_PRESERVATION_AUDIT.csv",
            ["DPA1273_2_preservation", "DPA1273_5_conditional_theorem"],
            "Dirac preservation audit blocks multiplier promotion without H_core/bracket data.",
        ),
        (
            "SRC2090_06_1248_Dirac",
            OUT / "P8_Y5_R10_1248_DIRAC_CHECK.csv",
            ["DIR1248_2_preservation", "DIR1248_4_boundary"],
            "minimal multiplier Dirac check keeps preservation and boundary gates open.",
        ),
        (
            "SRC2090_07_1622_lambda_origin",
            OUT / "P8_Y5_PARENT_QLOC_1622_LAMBDAR_PARENT_ORIGIN_AUDIT.csv",
            ["ORG1622_4_second_class_auxiliary", "ORG1622_6_verdict"],
            "lambda_R origin audit identifies the auxiliary route as strong but unsigned.",
        ),
        (
            "SRC2090_08_1564_presymplectic",
            ROOT / "1564-Y5-RAB-vertical-null-presymplectic-degeneracy-or-finite-ZR-intake.md",
            ["NULL1564_0_parent_L_theta", "NULL1564_5_verdict", "VAL1564_OVERALL"],
            "presymplectic-null route lacks parent L/theta/Omega and v_R generator.",
        ),
        (
            "SRC2090_09_1007_symplectic",
            ROOT / "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md",
            ["HTA1007_1_parent_theta_Qtau", "SRS1007_0_integrability_formula", "CG1007_0_Htau_integrability"],
            "symplectic/H_tau integrability remains a source-ready residual, not a parent proof.",
        ),
        (
            "SRC2090_10_1577_current",
            ROOT / "1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md",
            ["RCC1577_0_current_equation", "NCA1577_4_verdict", "VAL1577_OVERALL"],
            "radial cell-current route leaves Q_R hair unless no-charge is parent-signed.",
        ),
        (
            "SRC2090_11_1819_charge",
            ROOT / "1819-Y5-R2FR-local-EH-symplectic-charge-inheritance-or-Cterm-residual-vector.md",
            ["EHC1819_0_target", "EHC1819_6_verdict", "CTA1819_5_verdict"],
            "EH charge inheritance is exact conditional but current corpus still has C-term residuals.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle_found = exists and all(needle in text for needle in needles)
        rows.append(
            row(
                source_id=source_id,
                source_kind="parent_origin_evidence",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=needle_found,
                use_in_2090=role,
                valid_for_claim=False,
                claim_allowed=False,
            )
        )
    return rows


def selector_canonical_rows() -> list[dict[str, object]]:
    return [
        row(
            theorem_id="SCT2090_0_canonical_rewrite",
            statement="The 2089 selector is exactly a radial first-order canonical term when P_R=V_R/2.",
            calculation="L_sel=1/2 V_R(partial_r C_R-S_R)=P_R(partial_r C_R-S_R).",
            implication="the missing object is a parent radial canonical pair (C_R,P_R), not an arbitrary phenomenological coupling",
            proof_status="EXACT_ALGEBRAIC_REWRITE",
            missing_parent_input="theta_R=int P_R delta C_R and H_R=P_R S_R must be parent-owned",
            selector_signed=False,
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            theorem_id="SCT2090_1_Euler_selector",
            statement="If the parent reduced action contains L_sel and no extra V_R source terms, then the V_R Euler equation gives D_R[MTS].",
            calculation="E_V=partial L_sel/partial V_R=1/2(partial_r C_R-S_R); with 2089 E_time-E_radial=2E_V, E_time-E_radial=partial_r C_R-S_R.",
            implication="the derivation target is now a single checkable parent term plus a no-extra-V_R-source clause",
            proof_status="EXACT_CONDITIONAL_VARIATION",
            missing_parent_input="parent source for V_R partial_r C_R, V_R S_R, and silence of other V_R terms",
            selector_signed=False,
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            theorem_id="SCT2090_2_companion_equation",
            statement="The same first-order package also generates a companion C_R equation, so it is not harmless bookkeeping.",
            calculation="delta_C L_sel gives -partial_r P_R minus any P_R partial_C S_R plus boundary P_R delta C_R.",
            implication="a real parent action must explain the P_R equation, boundary class, and whether P_R carries reciprocal charge",
            proof_status="EXACT_CONDITIONAL_VARIATION",
            missing_parent_input="H_core/bracket/source dependence of S_R and boundary/corner conditions",
            selector_signed=False,
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            theorem_id="SCT2090_3_boundary_term",
            statement="The first-order term carries a boundary variation P_R delta C_R.",
            calculation="delta int P_R partial_r C_R = -int partial_r P_R delta C_R + [P_R delta C_R]_boundary.",
            implication="local GR requires either fixed C_R reference, P_R=0/no-charge, or a parent boundary counterterm; otherwise reciprocal hair remains",
            proof_status="EXACT_BOUNDARY_WARNING",
            missing_parent_input="boundary zero-flux/no-charge theorem or finite Q_R/P_R row",
            selector_signed=False,
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            theorem_id="SCT2090_4_exact_conditional_theorem",
            statement="If theta_R=int P_R delta C_R, H_R=P_R S_R, no extra V_R/C_R sources, and boundary no-charge are all parent-signed, then D_R is derived without importing GR.",
            calculation="S_Rad=int dr [P_R partial_r C_R-H_R]+boundary with H_R=P_R S_R; vary P_R and rotate Euler variables using 2089.",
            implication="this is the cleanest exact local-GR bridge currently available, but it remains unsigned",
            proof_status="EXACT_CONDITIONAL_THEOREM_NOT_CURRENT_PROOF",
            missing_parent_input="parent L/theta/Omega, canonical bracket, object-language type, H_core, source map, boundary no-charge",
            selector_signed=False,
            valid_for_claim=False,
            claim_allowed=False,
        ),
    ]


def parent_package_rows() -> list[dict[str, object]]:
    return [
        row(
            package_id="PKG2090_0_parent_theta",
            required_object="theta_R=int P_R delta C_R or equivalent presymplectic potential",
            role="owns V_R partial_r C_R as a radial canonical one-form",
            current_evidence="1564 and 1007 both record parent theta/Omega or theta/Q_tau as missing",
            status="MISSING_PARENT_THETA_OMEGA",
            next_action="hunt explicit parent L/theta/Omega for the radial observer-cell variables",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            package_id="PKG2090_1_parent_HR",
            required_object="H_R=P_R S_R plus declared source/residual decomposition",
            role="owns the -V_R S_R/2 term and defines what counts as local vacuum source",
            current_evidence="1865/1866/2089 define S_R as residual ledger but do not source it from H_core",
            status="MISSING_PARENT_HCORE",
            next_action="derive H_R from object-language radial-cell preservation or keep S_R as residual",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            package_id="PKG2090_2_no_extra_VR_terms",
            required_object="no a V_R^2, V_R J_hidden, V_R boundary/readout, or V_R q_loc terms outside S_R",
            role="prevents E_V from being shifted away from 1/2(partial_r C_R-S_R)",
            current_evidence="q_loc, source-map, coefficient-variation, and boundary slots remain live in 2089",
            status="NO_EXTRA_VR_SOURCE_UNSIGNED",
            next_action="treat every extra V_R term as Delta_sel unless parent-zeroed",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            package_id="PKG2090_3_Dirac_preservation",
            required_object="closed bracket/preservation chain for C_R/P_R or multiplier constraints",
            role="stops a formal multiplier from being a post-hoc closure axiom",
            current_evidence="1248/1273 block preservation on missing H_core/brackets/boundary",
            status="DIRAC_CHAIN_BLOCKED",
            next_action="source canonical variables, bracket table, constraint class, and boundary class",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            package_id="PKG2090_4_object_language",
            required_object="typed parent constructor list saying C_R is compatibility data, not an independent scalar",
            role="forbids Z_R/J_R/kinetic reciprocal hair before local readout",
            current_evidence="1257/1622/1866 mark this as best route but not parent-derived",
            status="OBJECT_LANGUAGE_UNSIGNED",
            next_action="write or source the allowed-object grammar; otherwise finite Z_R/J_R rows remain necessary",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            package_id="PKG2090_5_boundary_no_charge",
            required_object="P_R delta C_R boundary silence and Q_R=0/no reciprocal charge theorem",
            role="turns C_R'=S_R with local source silence into C_R=0 in the protected exterior",
            current_evidence="1577 and 1819 retain no-charge/C-term residuals",
            status="BOUNDARY_NO_CHARGE_UNSIGNED",
            next_action="prove no-charge from parent boundary class or keep Q_R/q_R_hat finite row",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            package_id="PKG2090_6_arena_projection",
            required_object="finite residual map to R10/PPN/clock/orbital if exact package is not signed",
            role="prevents theorem failure from becoming untestable rhetoric",
            current_evidence="2089 finite trace branch refuses scoring above q_R_hat ceiling without source-backed rows",
            status="FINITE_BRANCH_INPUTS_MISSING",
            next_action="source Z_R/M_R2/J_R/Q_R/S_R/tau arena rows if 2091 cannot sign the exact package",
            valid_for_claim=False,
            claim_allowed=False,
        ),
    ]


def route_audit_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="ROUTE2090_0_canonical_pair",
            route="derive selector from radial canonical pair",
            best_possible_result="D_R[MTS]=partial_r C_R-S_R from parent symplectic/Hamiltonian package",
            actual_status="EXACT_PACKAGE_DEFINED_NOT_SOURCED",
            obstruction="MISSING_THETA_R_HR_AND_NO_EXTRA_VR_SOURCE",
            decision="promote to next derivation target only",
            selector_signed=False,
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            route_id="ROUTE2090_1_multiplier",
            route="treat V_R or lambda_R as multiplier for radial compatibility",
            best_possible_result="C_R'=S_R or C_R=0 as a primary/secondary constraint",
            actual_status="FORMAL_PASS_NOT_PARENT_SIGNED",
            obstruction="Dirac preservation, H_core, constraint class, and boundary not supplied",
            decision="keep as closure template, not proof",
            selector_signed=False,
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            route_id="ROUTE2090_2_object_language",
            route="typed radial-cell object-language excludes independent reciprocal scalar",
            best_possible_result="Z_R/J_R/direct reciprocal hair forbidden by grammar",
            actual_status="BEST_LOW_SCRUTINY_ROUTE_UNSIGNED",
            obstruction="constructor list and allowed contractions are not parent-signed",
            decision="hunt this together with canonical theta_R in 2091",
            selector_signed=False,
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            route_id="ROUTE2090_3_current_nocharge",
            route="cell-current plus no-charge",
            best_possible_result="current conservation with Q_R=0 gives C_R constant/zero",
            actual_status="CONSERVATION_ONLY_LEAVES_HAIR",
            obstruction="Q_R=0 no-charge theorem missing",
            decision="fallback finite Q_R/q_R_hat row if exact package fails",
            selector_signed=False,
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            route_id="ROUTE2090_4_EH_import",
            route="use GR radial/time equation difference",
            best_possible_result="reciprocity follows in GR vacuum",
            actual_status="FORBIDDEN_SHORTCUT",
            obstruction="imports the theorem being derived",
            decision="reject as MTS derivation evidence",
            selector_signed=False,
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            route_id="ROUTE2090_5_finite_branch",
            route="score residual reciprocal field against local tests",
            best_possible_result="R10/PPN/clock/orbital safe despite finite C_R/q_R",
            actual_status="SOURCE_READY_ONLY",
            obstruction="Z_R/M_R2/J_R/Q_R/S_R/projection rows not source-backed",
            decision="do not score until exact package fails or source rows exist",
            selector_signed=False,
            valid_for_claim=False,
            claim_allowed=False,
        ),
    ]


def countermodel_rows() -> list[dict[str, object]]:
    return [
        row(
            countermodel_id="CM2090_0_extra_VR_potential",
            allowed_if_not_forbidden="Delta L=a V_R^2 or V_R J_hidden",
            effect="E_time-E_radial gains 4a V_R or J_hidden terms",
            killed_by="no-extra-V_R-source theorem from parent action",
            current_status="RETAINED_COUNTERMODEL",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            countermodel_id="CM2090_1_reciprocal_kinetic",
            allowed_if_not_forbidden="Delta L=1/2 Z_R (partial C_R)^2",
            effect="local exterior can carry reciprocal hair or Yukawa residuals",
            killed_by="object-language exclusion, presymplectic nullness, or sourced finite local-test bound",
            current_status="RETAINED_COUNTERMODEL",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            countermodel_id="CM2090_2_boundary_charge",
            allowed_if_not_forbidden="nonzero [P_R delta C_R]_boundary or Q_R",
            effect="C_R can be nonzero even when local bulk source is silent",
            killed_by="parent boundary no-charge theorem or source-backed q_R_hat bound",
            current_status="RETAINED_COUNTERMODEL",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            countermodel_id="CM2090_3_readout_regeneration",
            allowed_if_not_forbidden="readout/projector creates effective Delta_sel after variation",
            effect="closure equation is not stable under observable map",
            killed_by="variation-before-readout and no-reentry theorem",
            current_status="RETAINED_COUNTERMODEL",
            valid_for_claim=False,
            claim_allowed=False,
        ),
        row(
            countermodel_id="CM2090_4_GR_coordinate_shortcut",
            allowed_if_not_forbidden="set T^2 S=1 by Schwarzschild-like gauge choice",
            effect="would fake the result by coordinate/GR import",
            killed_by="no-GR-import guard and parent observer-cell derivation",
            current_status="FORBIDDEN_NOT_EVIDENCE",
            valid_for_claim=False,
            claim_allowed=False,
        ),
    ]


def branch_dry_run_rows() -> list[dict[str, object]]:
    return [
        row(
            run_id="RUN2090_0_canonical_package",
            branch="exact radial canonical pair",
            contract="theta_R=int P_R delta C_R; H_R=P_R S_R; P_R=V_R/2",
            input_status="REFUSED_MISSING_PARENT_THETA_HR",
            missing_inputs="parent L/theta/Omega; bracket table; H_core; no-extra-V_R source; boundary class",
            result="EXACT_CONDITIONAL_NEW_PACKAGE_ONLY",
            pass_status="NO_CLAIM",
            q_R_hat_policy_ceiling="",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            run_id="RUN2090_1_object_language",
            branch="typed radial-cell compatibility",
            contract="C_R is compatibility data rather than propagating scalar",
            input_status="REFUSED_MISSING_TYPED_CONSTRUCTOR_LIST",
            missing_inputs="allowed primitives; contractions; measures; source couplings; forbidden derivative grammar",
            result="LOW_SCRUTINY_ROUTE_RETAINED_UNSIGNED",
            pass_status="NO_CLAIM",
            q_R_hat_policy_ceiling="",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            run_id="RUN2090_2_Dirac_multiplier",
            branch="constraint/multiplier preservation",
            contract="primary/secondary constraint chain preserves C_R or C_R'=S_R",
            input_status="REFUSED_MISSING_HCORE_BRACKETS_BOUNDARY",
            missing_inputs="canonical algebra; H_core; constraint class; matter/source/boundary compatibility",
            result="FORMAL_MULTIPLIER_ONLY",
            pass_status="NO_CLAIM",
            q_R_hat_policy_ceiling="",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            run_id="RUN2090_3_current_nocharge",
            branch="cell-current route",
            contract="partial_r(W_R partial_r C_R)=0 plus Q_R=0",
            input_status="REFUSED_MISSING_NO_CHARGE_THEOREM",
            missing_inputs="Q_R=0 theorem; boundary class; source neutrality; finite Q_R value if nonzero",
            result="CONSERVATION_LEAVES_HAIR",
            pass_status="NO_CLAIM",
            q_R_hat_policy_ceiling=str(Q_R_HAT_POLICY_CEILING),
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            run_id="RUN2090_4_finite_residual",
            branch="finite trace/residual local tests",
            contract="absolute no-cancellation envelope with source-backed rows",
            input_status="REFUSED_SOURCE_BACKED_FINITE_ROWS_MISSING",
            missing_inputs="Z_R; M_R2; J_R; B_R; Q_R; S_R; tau_R10; tau_PPN; tau_clock; tau_orbital",
            result="LOCKED_INPUT_ONLY",
            pass_status="NO_SCORE",
            q_R_hat_policy_ceiling=str(Q_R_HAT_POLICY_CEILING),
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    gates = [
        ("GATE2090_0_selector", "parent selector cross-term is derived", "FAIL_BLOCKED", "theta_R/H_R/no-extra-V_R package not parent-signed"),
        ("GATE2090_1_DR", "D_R[MTS]=partial_r C_R-S_R is a derived parent Euler equation", "FAIL_BLOCKED", "canonical package is exact conditional only"),
        ("GATE2090_2_CR_zero", "C_R=0/R_AB=0 follows in local vacuum", "FAIL_BLOCKED", "S_R silence and boundary no-charge are unsigned"),
        ("GATE2090_3_local_GR_Newton", "local GR/Newton/PPN reduction is derived", "FAIL_BLOCKED", "D_R, q_loc, source map, beta, conservation and boundary gates remain open"),
        ("GATE2090_4_R10_PPN_clock_orbital", "local empirical arenas can be scored", "FAIL_BLOCKED", "finite residual inputs/projections missing"),
        ("GATE2090_5_public", "public/local-GR claim allowed", "FAIL_BLOCKED", "private derivation gate only; no claim-valid rows"),
    ]
    return [
        row(
            gate_id=gate_id,
            claim=claim,
            status=status,
            blocking_reason=reason,
            required_before_claim="parent-signed exact package or source-backed finite residual rows",
            claim_allowed=False,
            valid_for_claim=False,
        )
        for gate_id, claim, status, reason in gates
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(
            decision_id="DEC2090_0_progress",
            decision="CANONICAL_PAIR_PACKAGE_EXTRACTED",
            basis="L_sel rewrites as P_R(C_R'-S_R) with P_R=V_R/2, giving a precise symplectic/Hamiltonian target.",
            consequence="the parent-origin hunt is now for theta_R and H_R, not a vague coupling",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2090_1_no_promotion",
            decision="SELECTOR_NOT_PARENT_SIGNED",
            basis="all available symplectic, multiplier, object-language, current, and charge routes remain unsigned or conditional",
            consequence="no D_R/local-GR/Newton/R10/PPN/clock/orbital claim from 2090",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2090_2_best_next",
            decision="HUNT_RADIAL_CANONICAL_PAIR_SOURCE_FIRST",
            basis="theta_R/H_R source would close the exact route with less scrutiny than finite fifth-force tuning",
            consequence="2091 should attempt parent theta/Omega/H_core sourcing before moving to finite rows",
            claim_allowed=False,
            valid_for_claim=False,
        ),
        row(
            decision_id="DEC2090_3_fallback",
            decision="FINITE_BRANCH_REMAINS_REQUIRED_IF_2091_FAILS",
            basis="countermodels with Z_R, Q_R, boundary, readout and q_loc residuals remain legal unless forbidden",
            consequence="finite residual row acquisition cannot be avoided if exact package is not sourced",
            claim_allowed=False,
            valid_for_claim=False,
        ),
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            target_id="NEXT2090_0_2091",
            target_doc="2091-Y5-R2FR-radial-canonical-pair-source-hunt-or-finite-residual-lock.md",
            target_script="scripts/Y5_R2FR_radial_canonical_pair_source_hunt_or_finite_residual_lock_2091.py",
            objective="hunt a parent source for theta_R=int P_R delta C_R and H_R=P_R S_R in the MTS object-language, coframe/symplectic packet, multiplier/Dirac chain, or H_core/L_core; if absent, lock the selector as closure-only and prepare finite residual input acquisition",
            success_condition="source-backed parent radial canonical package, or clean refusal plus explicit finite Z_R/M_R2/J_R/Q_R/S_R/projection requirements",
            forbidden_shortcuts="GR radial identity import; Schwarzschild gauge shortcut; plateau axiom; closure q_R=0 as proof; finite trace score with missing rows; GitHub; formalization-workbench edits",
            claim_allowed=False,
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    selector: list[dict[str, object]],
    package: list[dict[str, object]],
    routes: list[dict[str, object]],
    counters: list[dict[str, object]],
    runs: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            SOURCE_WEIGHT_DOCS / "AFRAME_SELECTOR_CANONICAL_PAIR_2090_NONCLAIM.csv",
            selector + package + routes,
            "source_weight_docs",
        ),
        (
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2090_SELECTOR_CANONICAL_PAIR_NONCLAIM.csv",
            selector + package + counters + runs,
            "branch_locked_wep",
        ),
        (
            QUEUE / "JR2090_RADIAL_CANONICAL_PAIR_OR_CLOSURE_LOCK_QUEUE.csv",
            package + routes + next_rows_,
            "rab_acquisition_queue",
        ),
    ]
    rows: list[dict[str, object]] = []
    for path, data_rows, copy_kind in copies:
        write_csv(path, data_rows)
        rows.append(
            row(
                copy_id=f"COPY2090_{len(rows)}",
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
    selector: list[dict[str, object]],
    package: list[dict[str, object]],
    routes: list[dict[str, object]],
    counters: list[dict[str, object]],
    runs: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(truthy(r["path_exists"]) and truthy(r["needle_found"]) for r in sources)
    canonical_rewrite_ok = any(
        r["theorem_id"] == "SCT2090_0_canonical_rewrite"
        and "P_R=V_R/2" in str(r["statement"])
        and "P_R(partial_r C_R-S_R)" in str(r["calculation"])
        for r in selector
    )
    euler_selector_ok = any(
        r["theorem_id"] == "SCT2090_1_Euler_selector"
        and "E_time-E_radial=partial_r C_R-S_R" in str(r["calculation"])
        for r in selector
    )
    exact_conditional_only = any(
        r["theorem_id"] == "SCT2090_4_exact_conditional_theorem"
        and r["proof_status"] == "EXACT_CONDITIONAL_THEOREM_NOT_CURRENT_PROOF"
        for r in selector
    )
    package_blocked = all("MISSING" in str(r["status"]) or "UNSIGNED" in str(r["status"]) or "BLOCKED" in str(r["status"]) for r in package)
    routes_nonclaim = all(not truthy(r.get("selector_signed")) and not truthy(r.get("claim_allowed")) for r in routes)
    counters_retained = all(not truthy(r.get("claim_allowed")) and str(r["current_status"]) in {"RETAINED_COUNTERMODEL", "FORBIDDEN_NOT_EVIDENCE"} for r in counters)
    dry_refused = all(str(r["input_status"]).startswith("REFUSED") for r in runs)
    gates_block = all(str(r["status"]).startswith("FAIL_BLOCKED") and not truthy(r["claim_allowed"]) for r in claim_gates)
    decisions_ok = any(r["decision_id"] == "DEC2090_2_best_next" for r in decisions)
    next_ok = next_rows_[0]["target_id"] == "NEXT2090_0_2091"
    copies_ok = all(truthy(r["parses"]) and Path(str(r["path"])).exists() for r in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(r.get("claim_allowed")) and not truthy(r.get("valid_for_claim"))
        for group in [sources, selector, package, routes, counters, runs, claim_gates, decisions, next_rows_, copies]
        for r in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2090_artifacts()
    pycache_clean = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2090_00_sources", source_ok, "all cited sources exist and contain required needles"),
        ("VAL2090_01_canonical_rewrite", canonical_rewrite_ok, "selector rewrites as radial canonical pair with P_R=V_R/2"),
        ("VAL2090_02_Euler_selector", euler_selector_ok, "Euler rotation gives D_R under exact conditional selector"),
        ("VAL2090_03_exact_conditional_only", exact_conditional_only, "canonical theorem remains nonclaim conditional"),
        ("VAL2090_04_parent_package_blocked", package_blocked, "all parent package requirements remain missing/unsigned/blocked"),
        ("VAL2090_05_routes_nonclaim", routes_nonclaim, "no route marks selector as parent-signed"),
        ("VAL2090_06_countermodels_retained", counters_retained, "countermodels remain retained or forbidden, not erased"),
        ("VAL2090_07_dry_refusal", dry_refused, "dry runs refuse missing parent/source inputs"),
        ("VAL2090_08_claim_gates", gates_block, "all claim gates remain blocked"),
        ("VAL2090_09_decision_next", decisions_ok, "decision ledger selects radial canonical pair source hunt"),
        ("VAL2090_10_next_target", next_ok, "next target is 2091 radial canonical pair source hunt"),
        ("VAL2090_11_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2090_12_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2090_13_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2090_14_formalization_clean", formalization_clean, "formalization-workbench untouched by 2090"),
        ("VAL2090_15_no_pycache", pycache_clean, "scripts __pycache__ removed"),
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
            check_id="VAL2090_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2090 extracts the radial canonical-pair parent package, keeps selector/local-GR nonclaim, and selects 2091 source hunt" if overall else "one or more 2090 validation gates failed",
            claim_allowed=False,
            valid_for_claim=False,
        )
    )
    return rows


def write_doc(
    sources: list[dict[str, object]],
    selector: list[dict[str, object]],
    package: list[dict[str, object]],
    routes: list[dict[str, object]],
    counters: list[dict[str, object]],
    runs: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = "\n\n".join(
        [
            "# 2090 - Y5/R2FR Selector Cross-Term Parent Origin Or Object-Language Closure Lock",
            "## Current Verdict\n\n2090 makes the local-GR bridge sharper again, but still does not claim it. The 2089 selector `L_sel=1/2 V_R(partial_r C_R-S_R)` is exactly a radial first-order canonical package if `P_R=V_R/2`: `L_sel=P_R(partial_r C_R-S_R)`. So the missing parent object is no longer merely \"a coupling\"; it is the package `theta_R=int P_R delta C_R` plus `H_R=P_R S_R`, with no extra `V_R` source terms and a boundary no-charge class.\n\nIf a future parent action signs that package, `E_time-E_radial=partial_r C_R-S_R` follows without importing GR. The current corpus does not yet sign `theta_R`, `H_R`, the Dirac/object-language grammar, or the boundary/no-charge clauses, so `D_R` remains exact conditional/closure-only and all local-GR/Newton/R10/PPN/clock/orbital claims remain blocked.",
            "## Source Register",
            md_table(sources, ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_2090", "valid_for_claim", "claim_allowed"]),
            "## Selector Canonical Pair Extraction",
            md_table(selector, ["theorem_id", "statement", "calculation", "implication", "proof_status", "missing_parent_input", "selector_signed", "valid_for_claim"]),
            "## Parent Package Requirements",
            md_table(package, ["package_id", "required_object", "role", "current_evidence", "status", "next_action", "valid_for_claim"]),
            "## Parent-Origin Route Audit",
            md_table(routes, ["route_id", "route", "best_possible_result", "actual_status", "obstruction", "decision", "selector_signed", "valid_for_claim"]),
            "## Countermodel Ledger",
            md_table(counters, ["countermodel_id", "allowed_if_not_forbidden", "effect", "killed_by", "current_status", "valid_for_claim"]),
            "## Branch Dry Runs",
            md_table(runs, ["run_id", "branch", "contract", "input_status", "missing_inputs", "result", "pass_status", "q_R_hat_policy_ceiling", "claim_allowed", "valid_for_claim"]),
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
    selector = selector_canonical_rows()
    package = parent_package_rows()
    routes = route_audit_rows()
    counters = countermodel_rows()
    runs = branch_dry_run_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2090_SOURCE_REGISTER.csv",
        "selector": OUT / "P8_Y5_PARENT_QLOC_2090_SELECTOR_CANONICAL_PAIR_EXTRACTION.csv",
        "package": OUT / "P8_Y5_PARENT_QLOC_2090_PARENT_PACKAGE_REQUIREMENTS.csv",
        "routes": OUT / "P8_Y5_PARENT_QLOC_2090_PARENT_ORIGIN_ROUTE_AUDIT.csv",
        "counters": OUT / "P8_Y5_PARENT_QLOC_2090_COUNTERMODEL_LEDGER.csv",
        "runs": OUT / "P8_Y5_PARENT_QLOC_2090_BRANCH_DRY_RUNS.csv",
        "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2090_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2090_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2090_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2090_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2090_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["selector"], selector)
    write_csv(paths["package"], package)
    write_csv(paths["routes"], routes)
    write_csv(paths["counters"], counters)
    write_csv(paths["runs"], runs)
    write_csv(paths["claim_gates"], claim_gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(selector, package, routes, counters, runs, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["path"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, selector, package, routes, counters, runs, claim_gates, decisions, next_rows_, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, selector, package, routes, counters, runs, claim_gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
