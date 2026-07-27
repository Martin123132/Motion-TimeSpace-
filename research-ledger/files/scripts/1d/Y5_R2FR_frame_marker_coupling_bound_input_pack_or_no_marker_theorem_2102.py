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


DOC = ROOT / "2102-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

SRC_2101_DOC = ROOT / "2101-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"
CSV_2101_QBAR = OUT / "P8_Y5_PARENT_QLOC_2101_QBARXT_COUPLING_ROWS.csv"
CSV_2101_DEC = OUT / "P8_Y5_PARENT_QLOC_2101_DECISION_LEDGER.csv"
CSV_2101_NEXT = OUT / "P8_Y5_PARENT_QLOC_2101_NEXT_TARGET.csv"
CSV_2101_VAL = OUT / "P8_Y5_BRR545_2101_VALIDATION.csv"

SRC_1850_DOC = ROOT / "1850-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md"
CSV_1850_NMT = OUT / "P8_Y5_PARENT_QLOC_1850_NO_MARKER_THEOREM_ATTEMPT.csv"
CSV_1850_BOUND = OUT / "P8_Y5_PARENT_QLOC_1850_FRAME_MARKER_BOUND_INPUT_PACK.csv"
CSV_1850_SURV = OUT / "P8_Y5_PARENT_QLOC_1850_SURVIVING_MARKER_FAMILY_AUDIT.csv"
CSV_1850_ARENA = OUT / "P8_Y5_PARENT_QLOC_1850_ARENA_PROJECTION_ROWS.csv"
CSV_1850_DEP = OUT / "P8_Y5_PARENT_QLOC_1850_DEPENDENCY_LINKS.csv"
CSV_1850_GATE = OUT / "P8_Y5_PARENT_QLOC_1850_CLAIM_GATE.csv"
CSV_1850_VAL = OUT / "P8_Y5_BRR545_1850_VALIDATION.csv"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed", "selected"}


def formalization_has_2102_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2102-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2102*",
        "*Y5_R2FR_frame_marker_coupling_bound_input_pack_or_no_marker_theorem_2102*",
        "*AFRAME_FRAME_MARKER_COUPLING_2102*",
        "*JR2102_FIRST_FRAME_MARKER*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2102_00_2101_current_handoff",
            SRC_2101_DOC,
            ["NEXT2101_0_2102", "FRAME_MARKER_COUPLING_BOUND_INPUT_PACK_OR_NO_MARKER_THEOREM_NEXT", "VAL2101_OVERALL"],
            "2101 makes frame/marker coupling the current pressure point after the GR/Newton source-owner ladder.",
        ),
        (
            "SRC2102_01_2101_qbar_rows",
            CSV_2101_QBAR,
            ["QBR2101_2_marker", "QBR2101_5_total_guard", "MISSING"],
            "2101 decomposes qbar_XT into marker, constants, source-weight, non-Hilbert and total-guard rows.",
        ),
        (
            "SRC2102_02_2101_decision",
            CSV_2101_DEC,
            ["DEC2101_3_best_next", "FRAME_MARKER_COUPLING_BOUND_INPUT_PACK_OR_NO_MARKER_THEOREM_NEXT"],
            "2101 decision says to attempt no-marker theorem or build coupling bound inputs.",
        ),
        (
            "SRC2102_03_2101_next",
            CSV_2101_NEXT,
            ["NEXT2101_0_2102", "2102-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md"],
            "2101 next-target row points exactly at this checkpoint.",
        ),
        (
            "SRC2102_04_2101_validation",
            CSV_2101_VAL,
            ["VAL2101_OVERALL", "PASS", "blocks local-GR promotion"],
            "2101 validation proves the previous gate is clean and nonclaim.",
        ),
        (
            "SRC2102_05_1850_prior_attempt_doc",
            SRC_1850_DOC,
            ["Current verdict", "full no-marker theorem", "FMB1850_0_cg", "VAL1850_OVERALL"],
            "1850 is the older same-target attempt: useful partial theorem, then bound-pack route.",
        ),
        (
            "SRC2102_06_1850_no_marker_rows",
            CSV_1850_NMT,
            ["NMT1850_1_fixed_spurion_exclusion", "NMT1850_6_verdict", "NO_MARKER_THEOREM_NOT_CLOSED"],
            "1850 no-marker theorem rows identify which clauses closed and which stayed unsigned.",
        ),
        (
            "SRC2102_07_1850_bound_pack",
            CSV_1850_BOUND,
            ["FMB1850_0_cg", "FMB1850_10_total_qbarXT_envelope", "MISSING_COMPONENT_VALUES"],
            "1850 bound pack provides the component symbols and nonclaim schema.",
        ),
        (
            "SRC2102_08_1850_survivors",
            CSV_1850_SURV,
            ["SMF1850_3_material_constants", "SMF1850_5_source_boundary_tail", "LIVE_UNLESS"],
            "1850 survivor audit keeps material constants, clock constants and source/boundary tails live.",
        ),
        (
            "SRC2102_09_1850_arena_rows",
            CSV_1850_ARENA,
            ["APR1850_0_tau_R10", "APR1850_3_tau_orbital", "MISSING_ARENA_PROJECTION"],
            "1850 arena rows map coupling components into R10, PPN, clock, orbital, WEP and EM tests.",
        ),
        (
            "SRC2102_10_1850_dependencies",
            CSV_1850_DEP,
            ["DEP1850_0_no_marker_to_qbar_zero", "DEP1850_2_local_GR_to_zero_or_bounds"],
            "1850 dependencies block qbar/local-GR claims until theorem-zero or sourced bounds exist.",
        ),
        (
            "SRC2102_11_1850_claim_gate",
            CSV_1850_GATE,
            ["CG1850_1_no_marker_full", "False", "claim_allowed"],
            "1850 claim gates block full no-marker and local-GR promotion.",
        ),
        (
            "SRC2102_12_1850_validation",
            CSV_1850_VAL,
            ["VAL1850_OVERALL", "PASS", "frame/marker coupling bound input pack"],
            "1850 validation proves the older frame/marker pass was internally clean.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, use in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2102_frame_marker_current_refresh",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2102=use,
                valid_for_claim=False,
            )
        )
    return rows


def no_marker_contract_rows() -> list[dict[str, object]]:
    specs = [
        (
            "NMC2102_0_target",
            "ordinary matter has no independent X-marker",
            "For every ordinary matter system A, the vertical derivative of its matter/readout sector vanishes: delta_v S_matter,A = 0 after quotient descent.",
            "would imply b_A=b_alpha=b_marker=delta_kappa_A=q_domain=0 for ordinary matter",
            "NOT_PROVED_CURRENTLY",
            "requires all clauses below, not just absence of an explicit field label",
        ),
        (
            "NMC2102_1_descended_matter_functor",
            "matter action descends through q",
            "S_matter[Phi,Psi_A,theta_A]=Sbar_matter[q(Phi),Psi_A,thetabar_A] with no representative-only X dependence.",
            "removes direct representative marker channels",
            "UNSIGNED_PARENT_CLAUSE",
            "current corpus does not yet sign the full matter functor descent for all ordinary sectors",
        ),
        (
            "NMC2102_2_no_fixed_spurion",
            "fixed active covectors/labels are illegal",
            "No nondynamical active spurion n_A, xi_A, or labelled covector may appear in ordinary matter couplings.",
            "excludes the easiest fake marker route",
            "PARTIAL_THEOREM_SUPPORTED",
            "supported by older object-language hygiene rows but not sufficient for material constants",
        ),
        (
            "NMC2102_3_constant_descent",
            "ordinary constants are vertically silent",
            "Lie_v theta_A=0 for masses, charges, alpha_EM, binding coefficients, clock transition constants and composition labels.",
            "would remove b_A, b_alpha and clock/readout marker channels",
            "UNSIGNED_PARENT_CLAUSE",
            "this is the live coupling gap: constants may hide X-dependence unless parent action forbids it",
        ),
        (
            "NMC2102_4_source_weight_descent",
            "source weights and domain classes descend",
            "kappa_A, chi_D, source supports and preparation/domain selectors are functions only of quotient observables, not hidden X representatives.",
            "would remove delta_kappa_A, q_domain and support-shift marker routes",
            "UNSIGNED_PARENT_CLAUSE",
            "source/support terms are exactly where WEP, R10 and orbital channels can leak",
        ),
        (
            "NMC2102_5_boundary_current_silence",
            "boundary, connection and non-Hilbert tails are silent or bounded",
            "Projected boundary/non-Hilbert current satisfies P_loc(nabla^nu Gamma_eff - nabla_mu Khat^{mu nu})=0 or has sourced absolute bounds.",
            "would remove q_nonH and q_boundary from local residuals",
            "UNSIGNED_PARENT_CLAUSE",
            "previous local branch repeatedly found this is conditional, not established",
        ),
        (
            "NMC2102_6_readout_frame_lock",
            "clocks/rulers use the same descended frame",
            "The operational metric/coframe and calibration constants used by clocks, rods and charge readout are the same quotient-descended structure.",
            "prevents measured-G or calibration absorption from hiding frame coupling",
            "UNSIGNED_PARENT_CLAUSE",
            "without this, c_g and b_dis can masquerade as unit/readout choices",
        ),
        (
            "NMC2102_7_verdict",
            "full no-marker theorem",
            "NMC2102_1 through NMC2102_6 must all close in the parent action before qbar_XT=0 can be promoted.",
            "current theorem is conditional only",
            "CONDITIONAL_NOT_CURRENT_THEOREM",
            "do not loop here again without a new parent-action signature; use bounded component rows next",
        ),
    ]
    return [
        row(
            clause_id=clause_id,
            clause=clause,
            formal_statement=formal_statement,
            consequence_if_signed=consequence,
            status=status,
            blocker_or_note=blocker,
            valid_for_claim=False,
        )
        for clause_id, clause, formal_statement, consequence, status, blocker in specs
    ]


def conditional_theorem_rows() -> list[dict[str, object]]:
    specs = [
        (
            "CT2102_0_theorem_statement",
            "Conditional frame-marker silence theorem",
            "If ordinary matter functor descent, constant descent, source-weight descent, boundary-current silence and readout frame lock are all signed, then ordinary matter carries no independent X-marker in local tests.",
            "qbar_marker=qbar_constants=delta_kappa_A=q_domain=q_nonH=q_boundary=0, with c_g=b_dis=0 for the operational frame",
            "CONDITIONAL_THEOREM_ONLY",
            "not a current MTS claim",
        ),
        (
            "CT2102_1_proof_skeleton",
            "vertical derivative chain rule",
            "Under S_matter=Sbar[q(Phi),Psi,thetabar] and Dq[v_X]=0, delta_v S_matter=(delta Sbar/dq)Dq[v_X]+(partial Sbar/partial thetabar)Lie_v thetabar=0.",
            "all marker terms vanish only because every theta/source/readout channel is also vertically silent",
            "FORMAL_SKELETON_VALID",
            "skeleton becomes proof only after parent action signs the hypotheses",
        ),
        (
            "CT2102_2_countermodel_guard",
            "one unsigned channel defeats the theorem",
            "If any theta_A, kappa_A, readout frame or boundary tail depends on X, the chain-rule zero is false even when Dq[v_X]=0.",
            "surviving component must be bounded rather than cancelled",
            "COUNTERMODEL_OPEN",
            "this is why local-GR cannot be claimed from quotient descent alone",
        ),
        (
            "CT2102_3_current_status",
            "present theorem status",
            "The fixed-spurion/no-empty-linear-marker parts are useful partial wins, but material constants, source weights, frame/readout and boundary tails remain unsigned.",
            "move to component rows, not a fresh global no-marker loop",
            "NOT_CLOSED",
            "current next step should be a first sourced bound or parent-action signature row",
        ),
    ]
    return [
        row(
            theorem_id=theorem_id,
            theorem_piece=piece,
            statement=statement,
            implication=implication,
            status=status,
            limitation=limitation,
            valid_for_claim=False,
        )
        for theorem_id, piece, statement, implication, status, limitation in specs
    ]


def surviving_component_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SCC2102_0_cg",
            "c_g",
            "common conformal/Weyl matter-frame derivative",
            "LIVE_UNSIGNED",
            "could enter every local arena while being partly absorbed into measured units unless frame/readout lock is signed",
            "source c_g bound or prove common-frame descent",
        ),
        (
            "SCC2102_1_bdis",
            "b_dis",
            "disformal/profile-dependent matter-frame derivative",
            "LIVE_UNSIGNED",
            "can create PPN/lightcone/clock residuals not killed by scalar quotient silence",
            "source representative disformal bound row",
        ),
        (
            "SCC2102_2_bA",
            "b_A",
            "vertical derivative of mass/species/material constants",
            "LIVE_UNSIGNED",
            "composition dependence is the WEP/R10 danger channel",
            "source material-constant bound or parent constant-descent clause",
        ),
        (
            "SCC2102_3_balpha",
            "b_alpha",
            "vertical derivative of alpha_EM/gauge/binding/clock constants",
            "LIVE_UNSIGNED",
            "EM/clocks can see this even when metric-only tests look quiet",
            "source fine-structure/clock bound mapping",
        ),
        (
            "SCC2102_4_bmarker",
            "b_marker",
            "preparation, material label or readout marker derivative",
            "LIVE_UNSIGNED",
            "a hidden marker can reintroduce qbar_XT without an explicit new field",
            "prove no-marker for preparation labels or bound it",
        ),
        (
            "SCC2102_5_delta_kappa_A",
            "delta_kappa_A",
            "species/source-only current prefactor",
            "LIVE_UNSIGNED",
            "source/test asymmetry can fake or hide fifth-force charge",
            "source WEP/R10 component row",
        ),
        (
            "SCC2102_6_q_nonH",
            "q_nonH",
            "non-Hilbert, connection, torsion or current tail projection",
            "LIVE_UNSIGNED",
            "local vacuum silence fails if this tail survives projection",
            "source non-Hilbert/current residual row",
        ),
        (
            "SCC2102_7_support_boundary",
            "Delta_W_support;q_boundary;q_domain",
            "support, boundary and domain-selector shifts",
            "LIVE_UNSIGNED",
            "finite-size/orbital/domain terms can survive where point-body intuition says zero",
            "source support/boundary envelope rows",
        ),
    ]
    return [
        row(
            component_id=component_id,
            symbol=symbol,
            meaning=meaning,
            current_status=status,
            why_it_matters=why,
            next_action=next_action,
            valid_for_claim=False,
        )
        for component_id, symbol, meaning, status, why, next_action in specs
    ]


def bound_input_rows() -> list[dict[str, object]]:
    specs = [
        ("FMB2102_0_cg", "c_g", "common Weyl/conformal matter-frame derivative d ln A_g/dXhat", "|c_g| <= tau_cg", "dimensionless or inverse normalized Xhat", CSV_1850_BOUND, "R10;PPN;clock;orbital;WEP", "MISSING_NUMERIC_BOUND"),
        ("FMB2102_1_bdis", "b_dis", "representative disformal/profile-normalized matter-frame derivative", "|b_dis| <= tau_dis", "dimensionless or profile-normalized", CSV_1850_BOUND, "PPN;clock;light propagation", "MISSING_NUMERIC_BOUND"),
        ("FMB2102_2_bA", "b_A", "vertical derivative of material mass/species constants d ln m_A/dXhat", "|b_A| <= tau_A", "dimensionless or inverse normalized Xhat", CSV_1850_BOUND, "WEP;R10;orbital", "MISSING_NUMERIC_BOUND"),
        ("FMB2102_3_balpha", "b_alpha", "vertical derivative of alpha_EM/gauge/binding/clock constants", "|b_alpha| <= tau_alpha", "dimensionless or inverse normalized Xhat", CSV_1850_BOUND, "clock;EM;fine-structure", "MISSING_NUMERIC_BOUND"),
        ("FMB2102_4_bmarker", "b_marker", "vertical derivative of preparation/material/readout marker channel", "|b_marker| <= tau_marker", "dimensionless or inverse normalized Xhat", CSV_1850_BOUND, "WEP;clock;R10", "MISSING_NUMERIC_BOUND"),
        ("FMB2102_5_delta_kappa_A", "delta_kappa_A", "relative source-only matter prefactor/species current weight", "|delta_kappa_A| <= tau_kappa", "dimensionless", CSV_1850_BOUND, "WEP;R10;source tests", "MISSING_NUMERIC_BOUND"),
        ("FMB2102_6_qnonH", "q_nonH", "ordinary source projection from non-Hilbert current, torsion/connection tail, or boundary current", "|q_nonH| <= tau_nonH", "arena-normalized source charge", CSV_1850_BOUND, "PPN;orbital;local vacuum", "MISSING_NUMERIC_BOUND"),
        ("FMB2102_7_Delta_W_support", "Delta_W_support", "worldtube/support/domain shift under local projection or observed-frame change", "|Delta_W_support| <= tau_support", "length or dimensionless support fraction", CSV_1850_BOUND, "orbital;WEP;finite-size", "MISSING_NUMERIC_BOUND"),
        ("FMB2102_8_qdomain", "q_domain", "domain class or chi_D selector contribution to source/test normalization", "|q_domain| <= tau_domain", "dimensionless source charge", CSV_1850_BOUND, "domain/orbital/source tests", "MISSING_NUMERIC_BOUND"),
        ("FMB2102_9_qboundary", "q_boundary", "boundary/local projection flux contribution to qbar_XT", "|q_boundary| <= tau_boundary", "arena-normalized source charge", CSV_1850_BOUND, "PPN;orbital;R10", "MISSING_NUMERIC_BOUND"),
        ("FMB2102_10_total_qbarXT_envelope", "qbar_XT_bound_abs", "absolute no-cancellation envelope over all surviving frame/marker/source/boundary components", "sum_i |projected_component_i| <= tau_arena", "arena-normalized source charge", CSV_2101_QBAR, "all local arenas", "MISSING_COMPONENT_VALUES"),
    ]
    return [
        row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            bound_formula=formula,
            current_value="",
            units=units,
            source_path=str(source_path),
            source_path_exists=source_path.exists(),
            observable_link=observable,
            status=status,
            score_ready=False,
            valid_for_claim=False,
        )
        for row_id, symbol, definition, formula, units, source_path, observable, status in specs
    ]


def arena_residual_rows() -> list[dict[str, object]]:
    specs = [
        (
            "ARM2102_0_R10",
            "R10 short-range alpha(lambda)",
            "c_g;b_dis;b_A;b_marker;delta_kappa_A;qboundary",
            "alpha_pred(lambda_X)=K_X(lambda_X)*Qbar_XH(lambda_X)*qbar_XT_bound_abs",
            "MISSING_K_X_Qbar_XH_qbar_bound",
        ),
        (
            "ARM2102_1_PPN",
            "local weak-field/PPN",
            "c_g;b_dis;q_nonH;Delta_W_support;q_boundary",
            "PPN_residual_vector <= tau_PPN(c_g,b_dis,q_nonH,Delta_W_support,q_boundary)",
            "MISSING_PPN_PROJECTION",
        ),
        (
            "ARM2102_2_clocks",
            "clock/fine-structure/EM readout",
            "c_g;b_A;b_alpha;b_marker;q_nonH",
            "clock_residual <= tau_clock(c_g,b_A,b_alpha,b_marker,q_nonH)",
            "MISSING_CLOCK_PROJECTION",
        ),
        (
            "ARM2102_3_orbital",
            "orbital/source-support systems",
            "delta_kappa_A;q_nonH;Delta_W_support;qboundary;qdomain",
            "orbital_residual <= tau_orbital(delta_kappa_A,q_nonH,Delta_W_support,qboundary,qdomain)",
            "MISSING_ORBITAL_PROJECTION",
        ),
        (
            "ARM2102_4_WEP",
            "composition/WEP",
            "b_A;b_marker;delta_kappa_A;qdomain",
            "eta_AB <= tau_WEP(b_A,b_marker,delta_kappa_A,qdomain)",
            "MISSING_WEP_COMPONENT_VALUES",
        ),
        (
            "ARM2102_5_EM",
            "EM/fine-structure",
            "b_alpha;b_A;b_marker;c_g",
            "alpha_EM_residual <= tau_EM(b_alpha,b_A,b_marker,c_g)",
            "MISSING_EM_PROJECTION",
        ),
    ]
    return [
        row(
            arena_id=arena_id,
            arena=arena,
            uses_components=components,
            formula_or_contract=formula,
            current_status="BLOCKED_VALUES_MISSING",
            blocker=blocker,
            valid_for_claim=False,
        )
        for arena_id, arena, components, formula, blocker in specs
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    specs = [
        ("GATE2102_0_fixed_spurions", "fixed active spurions excluded", True, "partial theorem stands but is not enough for local GR"),
        ("GATE2102_1_full_no_marker", "all ordinary frame/marker channels excluded", False, "constant/source/readout/boundary clauses remain unsigned"),
        ("GATE2102_2_bound_rows_numeric", "all coupling bound rows numeric and sourced", False, "FMB2102 rows are schema-ready but values-missing"),
        ("GATE2102_3_no_cancellation", "total qbar bound uses absolute envelope", True, "envelope rule is present, but values are missing"),
        ("GATE2102_4_arena_projection", "R10/PPN/clock/orbital projections score-ready", False, "projection coefficients and tolerances are not sourced"),
        ("GATE2102_5_local_GR", "derived local GR/Newton limit", False, "requires theorem-zero or bounded residual vector below local tests"),
    ]
    return [
        row(
            gate_id=gate_id,
            gate=gate,
            gate_pass=gate_pass,
            reason=reason,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for gate_id, gate, gate_pass, reason in specs
    ]


def decision_rows() -> list[dict[str, object]]:
    specs = [
        (
            "DEC2102_0_theorem_result",
            "NO_MARKER_THEOREM_CONDITIONAL_NOT_CURRENT",
            "The proof skeleton works only if matter functor, constants, source weights, boundary currents and readout frame all descend.",
            "do not claim qbar_XT=0 from quotient descent alone",
        ),
        (
            "DEC2102_1_bound_pack_result",
            "FRAME_MARKER_BOUND_PACK_IS_THE_CURRENT_WORKING_OBJECT",
            "The surviving physical gap is now a vector of coupling components, not one vague coupling.",
            "source or derive one component at a time with absolute no-cancellation envelopes",
        ),
        (
            "DEC2102_2_best_route",
            "FIRST_REAL_FRAME_MARKER_COMPONENT_SOURCE_ROW_NEXT",
            "A new global no-marker loop would mostly repeat 1850; the lower-scrutiny route is a concrete sourced bound or parent-action signature for c_g/b_A/b_alpha.",
            "start with c_g/common-frame because it touches GR/Newton, then material/alpha channels",
        ),
    ]
    return [
        row(
            decision_id=decision_id,
            decision=decision,
            because=because,
            next_action=next_action,
            valid_for_claim=False,
        )
        for decision_id, decision, because, next_action in specs
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2102_0_2103",
            next_target="2103-Y5-R2FR-first-real-frame-marker-component-source-row-cg-bA-balpha.md",
            script="scripts/Y5_R2FR_first_real_frame_marker_component_source_row_cg_bA_balpha_2103.py",
            objective="Build the first source-backed coupling component row: c_g first, with b_A and b_alpha queued; no local-GR claim unless bounds or parent signatures close.",
            forbidden_shortcuts="another global no-marker loop without new parent-action input; measured-G absorption; cancellation between components; source-free numeric bounds; GitHub/formalization edits",
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    contract: list[dict[str, object]],
    theorem: list[dict[str, object]],
    components: list[dict[str, object]],
    bounds: list[dict[str, object]],
    arenas: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2102_0_source_weight_docs",
            SOURCE_WEIGHT_DOCS / "AFRAME_FRAME_MARKER_COUPLING_2102_NONCLAIM.csv",
            contract + theorem + components + decisions,
        ),
        (
            "COPY2102_1_branch_locked_wep",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2102_FRAME_MARKER_STATUS_NONCLAIM.csv",
            components + bounds + arenas,
        ),
        (
            "COPY2102_2_acquisition_queue",
            QUEUE / "JR2102_FIRST_FRAME_MARKER_COMPONENT_SOURCE_ROW_QUEUE.csv",
            bounds + arenas + next_target,
        ),
    ]
    rows: list[dict[str, object]] = []
    for copy_id, path, copy_rows in copies:
        write_csv(path, copy_rows)
        rows.append(
            row(
                copy_id=copy_id,
                destination=str(path),
                path_exists=path.exists(),
                row_count=len(copy_rows),
                parse_ok=csv_rows_parse(path),
                valid_for_claim=False,
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    theorem: list[dict[str, object]],
    components: list[dict[str, object]],
    bounds: list[dict[str, object]],
    arenas: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(truthy(source.get("path_exists")) and truthy(source.get("needle_found")) for source in sources)
    contract_ok = any(row_.get("clause_id") == "NMC2102_7_verdict" and row_.get("status") == "CONDITIONAL_NOT_CURRENT_THEOREM" for row_ in contract)
    theorem_ok = any(row_.get("theorem_id") == "CT2102_0_theorem_statement" and row_.get("status") == "CONDITIONAL_THEOREM_ONLY" for row_ in theorem)
    components_ok = len(components) >= 8 and all(row_.get("current_status") == "LIVE_UNSIGNED" for row_ in components)
    bounds_ok = len(bounds) >= 11 and all(not truthy(row_.get("score_ready")) and not truthy(row_.get("valid_for_claim")) for row_ in bounds)
    arenas_ok = len(arenas) >= 6 and all(str(row_.get("current_status", "")).startswith("BLOCKED") for row_ in arenas)
    gates_ok = all(not truthy(row_.get("claim_allowed")) for row_ in gates) and any(not truthy(row_.get("gate_pass")) for row_ in gates)
    decision_ok = any(row_.get("decision") == "FIRST_REAL_FRAME_MARKER_COMPONENT_SOURCE_ROW_NEXT" for row_ in decisions)
    next_ok = any(row_.get("route_id") == "NEXT2102_0_2103" and "2103-Y5-R2FR" in str(row_.get("next_target")) for row_ in next_target)
    copies_ok = len(copies) == 3 and all(truthy(row_.get("path_exists")) and truthy(row_.get("parse_ok")) for row_ in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claims = all(
        not truthy(row_.get("valid_for_claim")) and not truthy(row_.get("claim_allowed"))
        for collection in (sources, contract, theorem, components, bounds, arenas, gates, decisions, next_target, copies)
        for row_ in collection
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2102_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2102_00_sources", source_ok, "all current and older source paths exist and contain required needles"),
        ("VAL2102_01_contract", contract_ok, "no-marker contract ends as conditional, not current theorem"),
        ("VAL2102_02_conditional_theorem", theorem_ok, "conditional theorem skeleton recorded without promotion"),
        ("VAL2102_03_surviving_components", components_ok, "surviving frame/marker components remain live unsigned rows"),
        ("VAL2102_04_bound_rows", bounds_ok, "bound input rows are schema-ready but nonclaim and not score-ready"),
        ("VAL2102_05_arena_rows", arenas_ok, "R10/PPN/clock/orbital/WEP/EM arena rows remain blocked"),
        ("VAL2102_06_claim_gates", gates_ok, "claim gates block local-GR/Newton promotion"),
        ("VAL2102_07_decision", decision_ok, "decision avoids another loop and selects first component source row"),
        ("VAL2102_08_next", next_ok, "next target is 2103 first real frame-marker component source row"),
        ("VAL2102_09_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2102_10_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2102_11_no_claim_flags", no_claims, "no generated row allows a claim"),
        ("VAL2102_12_formalization_clean", formalization_clean, "formalization-workbench untouched by 2102"),
        ("VAL2102_13_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(ok for _, ok, _ in checks)
    checks.append(
        (
            "VAL2102_OVERALL",
            overall,
            "2102 refreshes the frame/marker coupling gap, keeps theorem-zero conditional, and moves to first source-backed component row",
        )
    )
    return [
        row(
            check_id=check_id,
            status="PASS" if ok else "FAIL",
            detail=detail,
            claim_allowed=False,
            valid_for_claim=False,
        )
        for check_id, ok, detail in checks
    ]


def write_doc(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    theorem: list[dict[str, object]],
    components: list[dict[str, object]],
    bounds: list[dict[str, object]],
    arenas: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2102 - Y5/R2FR Frame Marker Coupling Bound Input Pack Or No-Marker Theorem",
        "",
        "## Current Verdict",
        "",
        "2102 does **not** close the local-GR/Newton route. It sharpens the missing coupling object. The no-marker theorem has a valid conditional proof skeleton: if ordinary matter, constants, source weights, boundary currents and readout frames all descend through the quotient, then ordinary matter carries no independent X-marker. But those clauses are not parent-signed in the current corpus.",
        "",
        "Therefore the disciplined route is not another global theorem loop. The current working object is a bounded component vector: `c_g`, `b_dis`, `b_A`, `b_alpha`, `b_marker`, `delta_kappa_A`, `q_nonH`, support/domain/boundary terms, and their absolute no-cancellation envelope.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "path_exists", "needle_found", "use_in_2102", "valid_for_claim"]),
        "## No-Marker Contract",
        md_table(contract, ["clause_id", "clause", "status", "consequence_if_signed", "blocker_or_note", "valid_for_claim"]),
        "## Conditional Theorem",
        md_table(theorem, ["theorem_id", "theorem_piece", "status", "statement", "limitation", "valid_for_claim"]),
        "## Surviving Coupling Components",
        md_table(components, ["component_id", "symbol", "current_status", "why_it_matters", "next_action", "valid_for_claim"]),
        "## Bound Input Rows",
        md_table(bounds, ["row_id", "symbol", "bound_formula", "current_value", "units", "source_path_exists", "observable_link", "status", "score_ready", "valid_for_claim"]),
        "## Arena Residual Map",
        md_table(arenas, ["arena_id", "arena", "uses_components", "formula_or_contract", "current_status", "blocker", "valid_for_claim"]),
        "## Claim Gates",
        md_table(gates, ["gate_id", "gate", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
        "## Decision Ledger",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "## Next Target",
        md_table(next_target, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
        "## Branch Copies",
        md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
        "## Validation",
        md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    contract = no_marker_contract_rows()
    theorem = conditional_theorem_rows()
    components = surviving_component_rows()
    bounds = bound_input_rows()
    arenas = arena_residual_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2102_SOURCE_REGISTER.csv",
        "contract": OUT / "P8_Y5_PARENT_QLOC_2102_NO_MARKER_CONTRACT.csv",
        "theorem": OUT / "P8_Y5_PARENT_QLOC_2102_CONDITIONAL_THEOREM.csv",
        "components": OUT / "P8_Y5_PARENT_QLOC_2102_SURVIVING_COUPLING_COMPONENTS.csv",
        "bounds": OUT / "P8_Y5_PARENT_QLOC_2102_BOUND_INPUT_ROWS.csv",
        "arenas": OUT / "P8_Y5_PARENT_QLOC_2102_ARENA_RESIDUAL_MAP.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2102_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2102_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2102_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2102_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2102_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["contract"], contract)
    write_csv(paths["theorem"], theorem)
    write_csv(paths["components"], components)
    write_csv(paths["bounds"], bounds)
    write_csv(paths["arenas"], arenas)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_target)
    copies = write_branch_copies(contract, theorem, components, bounds, arenas, decisions, next_target)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["destination"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, contract, theorem, components, bounds, arenas, gates, decisions, next_target, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, contract, theorem, components, bounds, arenas, gates, decisions, next_target, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
