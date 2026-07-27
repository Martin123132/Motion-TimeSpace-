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


DOC = ROOT / "2110-Y5-R2FR-Gamma-Khat-q_loc-parent-action-owner-or-DqZ-GK-tail-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()

SRC_2109_DOC = ROOT / "2109-Y5-R2FR-extra-sector-natural-bundle-lift-or-finite-DqZ-tail-row.md"
CSV_2109_GK = OUT / "P8_Y5_PARENT_QLOC_2109_GK_ACTION_NATURALITY_TEST.csv"
CSV_2109_DQZ = OUT / "P8_Y5_PARENT_QLOC_2109_DQZ_FINITE_TAIL_ROWS.csv"
CSV_2109_NEXT = OUT / "P8_Y5_PARENT_QLOC_2109_NEXT_TARGET.csv"
CSV_2109_VAL = OUT / "P8_Y5_BRR545_2109_VALIDATION.csv"

SRC_1010_DOC = ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md"
CSV_1010_THEOREM = OUT / "P8_Y5_R10_1010_THEOREM_ATTEMPT.csv"
CSV_1010_GATE = OUT / "P8_Y5_R10_1010_CLAIM_GATE.csv"
CSV_1010_DEC = OUT / "P8_Y5_R10_1010_DECISION_LEDGER.csv"

SRC_1351_DOC = ROOT / "1351-Y5-R10-RAB-Gamma-Khat-Ploc-owner-bundle-or-q_loc-bound-row-fill.md"
CSV_1351_AUDIT = OUT / "P8_Y5_R10_1351_OWNER_BUNDLE_AUDIT.csv"
CSV_1351_THEOREM = OUT / "P8_Y5_R10_1351_CONDITIONAL_OPERATOR_BUNDLE_THEOREM.csv"

SRC_1366_DOC = ROOT / "1366-Y5-R10-RAB-Gamma-eff-scalar-density-definition-hunt-or-q_loc-envelope.md"
CSV_1366_HUNT = OUT / "P8_Y5_R10_1366_GAMMA_EFF_SCALAR_DENSITY_HUNT_LEDGER.csv"
CSV_1366_KMATCH = OUT / "P8_Y5_R10_1366_KMETRIC_KHAT_MATCH_LEDGER.csv"

SRC_1371_DOC = ROOT / "1371-Y5-R10-RAB-fixed-Lcg-parent-action-insertion-or-Cqgamma-norm-bound.md"
CSV_1371_ACTION = OUT / "P8_Y5_R10_1371_FIXED_L0_PARENT_ACTION_INSERTION.csv"
CSV_1371_RESIDUAL = OUT / "P8_Y5_R10_1371_LOCAL_RESIDUAL_ZERO_OR_BOUND_LEDGER.csv"
CSV_1371_NORM = OUT / "P8_Y5_R10_1371_CQGAMMA_NORM_BOUND_INPUT_TABLE.csv"

SRC_1372_DOC = ROOT / "1372-Y5-R10-RAB-fixed-L0-double-zero-local-residual-theorem-or-Qnorm-bound.md"
CSV_1372_THEOREM = OUT / "P8_Y5_R10_1372_LOCAL_RESIDUAL_THEOREM_ATTEMPT.csv"
CSV_1372_QNORM = OUT / "P8_Y5_R10_1372_QNORM_DECOMPOSITION_BOUND.csv"
CSV_1372_FEED = OUT / "P8_Y5_R10_1372_CQGAMMA_RUNNER_FEED.csv"

SRC_1590_DOC = ROOT / "1590-Y5-R2FR-Gamma-Khat-Ploc-owner-bundle-or-cR2-finite-coefficient-row.md"
CSV_1590_OWNER = OUT / "P8_Y5_PARENT_QLOC_1590_OWNER_BUNDLE_SYNTHESIS.csv"
CSV_1590_FIXED = OUT / "P8_Y5_PARENT_QLOC_1590_FIXED_L0_DOUBLE_ZERO_CONTRACT_GATE.csv"

SRC_1039_DOC = ROOT / "1039-Y5-R10-boundary-charge-QX-Kboundary-zero-or-beta-bound-first-row.md"


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid", "claim_allowed", "selected"}


def formalization_has_2110_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2110-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2110*",
        "*Y5_R2FR_Gamma_Khat_q_loc_parent_action_owner_or_DqZ_GK_tail_bound_2110*",
        "*AFRAME_GK_OWNER_2110*",
        "*JR2110_FIXED_L0*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs: list[tuple[str, Path, list[str], str]] = [
        (
            "SRC2110_00_2109_doc",
            SRC_2109_DOC,
            ["NEXT2109_0_2110", "GK_OWNER_BUNDLE_FIRST", "VAL2109_OVERALL"],
            "2109 selects the Gamma/Khat/q_loc owner bundle as the next proof fork.",
        ),
        (
            "SRC2110_01_2109_GK",
            CSV_2109_GK,
            ["GK2109_7_owner_verdict", "OWNER_BUNDLE_NOT_CLOSED_CURRENT_CORPUS"],
            "2109 GK table keeps owner bundle nonclaim.",
        ),
        (
            "SRC2110_02_2109_DQZ",
            CSV_2109_DQZ,
            ["DQZ2109_1_GK_q_loc", "MISSING_SGK_OWNER_OR_NUMERIC_BOUND", "DQZ2109_6_total_abs"],
            "2109 finite-tail rows retain the GK/q_loc residual if owner proof fails.",
        ),
        (
            "SRC2110_03_2109_next",
            CSV_2109_NEXT,
            ["NEXT2109_0_2110", "Gamma-Khat-q_loc-parent-action-owner", "finite GK/q_loc tail"],
            "2109 next-target row points exactly at this checkpoint.",
        ),
        (
            "SRC2110_04_2109_validation",
            CSV_2109_VAL,
            ["VAL2109_OVERALL", "PASS", "GK owner bundle next"],
            "2109 validation passed cleanly.",
        ),
        (
            "SRC2110_05_1010_doc",
            SRC_1010_DOC,
            ["q_loc is retained", "GKT1010_6_verdict", "fail_current_claim"],
            "1010 wrote the original action-existence/Helmholtz gate.",
        ),
        (
            "SRC2110_06_1010_theorem",
            CSV_1010_THEOREM,
            ["GKT1010_0_variational_route", "GKT1010_6_verdict", "fail_current_claim"],
            "1010 theorem attempt keeps q_loc zero nonclaim.",
        ),
        (
            "SRC2110_07_1010_gate",
            CSV_1010_GATE,
            ["CG1010_0_S_GK_action", "CG1010_6_residual_retention", "true"],
            "1010 claim gate blocks S_GK action promotion and retains residual.",
        ),
        (
            "SRC2110_08_1010_decision",
            CSV_1010_DEC,
            ["DEC1010_0_derivation_route_precise", "DEC1010_2_residual_kept_honest"],
            "1010 decision says the route is precise but not currently proved.",
        ),
        (
            "SRC2110_09_1351_doc",
            SRC_1351_DOC,
            ["q_loc^nu -> 0", "OB1351_7_verdict", "OWNER_BUNDLE_NOT_CLOSED"],
            "1351 proves the conditional operator-bundle theorem but blocks current claim.",
        ),
        (
            "SRC2110_10_1351_audit",
            CSV_1351_AUDIT,
            ["OB1351_0_action_existence", "OB1351_7_verdict", "OWNER_BUNDLE_NOT_CLOSED"],
            "1351 owner-bundle audit lists missing action, Khat, Ploc, Euler and boundary inputs.",
        ),
        (
            "SRC2110_11_1351_theorem",
            CSV_1351_THEOREM,
            ["THM1351_0_define_stress", "THM1351_3_verdict", "NOT_PARENT_SIGNED_CURRENT_CORPUS"],
            "1351 theorem shape is mathematically sharp but unsigned.",
        ),
        (
            "SRC2110_12_1366_doc",
            SRC_1366_DOC,
            ["Gamma_eff=L_cg^-2F(m)", "CLAIM_BLOCKED"],
            "1366 finds the first useful scalar-density shape but not claim-grade ownership.",
        ),
        (
            "SRC2110_13_1366_hunt",
            CSV_1366_HUNT,
            ["HUNT1366_0_memory_scalar_formula_shape", "HUNT1366_6_overall", "NO_CLAIM_GRADE_SCALAR_DENSITY_FOUND"],
            "1366 hunt finds formula shape but no claim-grade scalar-density definition.",
        ),
        (
            "SRC2110_14_1366_kmatch",
            CSV_1366_KMATCH,
            ["MATCH1366_3_live_Khat_comparison", "MATCH1366_4_acceptance", "CLAIM_BLOCKED"],
            "1366 Kmetric/Khat ledger keeps live Khat comparison missing.",
        ),
        (
            "SRC2110_15_1371_doc",
            SRC_1371_DOC,
            ["Fixed `L_cg=L0`", "Fhat(m;m_*)", "C_qgamma"],
            "1371 derives the fixed-L0/double-zero closure branch and symbolic gamma bound lane.",
        ),
        (
            "SRC2110_16_1371_action",
            CSV_1371_ACTION,
            ["PAI1371_2_strict_double_zero", "PAI1371_5_action_insertion_verdict", "CLOSURE_BRANCH_READY_NOT_LIVE_CLAIM"],
            "1371 action insertion gives real algebraic closure under strict clauses.",
        ),
        (
            "SRC2110_17_1371_residual",
            CSV_1371_RESIDUAL,
            ["LRZ1371_3_gradient_source", "LRZ1371_4_cdb_terms", "LRZ1371_5_memory_stress"],
            "1371 residual ledger separates closed algebraic chain from open CDB/memory channels.",
        ),
        (
            "SRC2110_18_1371_norm",
            CSV_1371_NORM,
            ["CQN1371_5_qloc_norm", "CQN1371_7_pass_threshold", "SYMBOLIC_ACCEPTANCE_RULE_READY"],
            "1371 norm-bound inputs show the gamma lane is symbolic but not numeric.",
        ),
        (
            "SRC2110_19_1372_doc",
            SRC_1372_DOC,
            ["Q_norm <= Q_alg + Q_cdb + Q_mem + Q_bdy + Q_trans + Q_proj", "ZERO_THEOREM_NOT_DERIVED"],
            "1372 tries and fails to close the full local residual theorem.",
        ),
        (
            "SRC2110_20_1372_theorem",
            CSV_1372_THEOREM,
            ["LRT1372_0_algebraic_fixed_L0_double_zero", "LRT1372_5_zero_theorem_verdict", "ZERO_THEOREM_NOT_DERIVED"],
            "1372 theorem attempt confirms algebraic closure but live CDB/memory/source residuals.",
        ),
        (
            "SRC2110_21_1372_qnorm",
            CSV_1372_QNORM,
            ["QNB1372_0_total_decomposition", "QNB1372_7_no_cancellation_policy", "SYMBOLIC_DECOMPOSITION_DERIVED"],
            "1372 Qnorm table supplies the no-cancellation residual decomposition.",
        ),
        (
            "SRC2110_22_1372_feed",
            CSV_1372_FEED,
            ["QGF1372_1_gamma_bound", "SYMBOLIC_CASSINI_BOUND_READY", "PROXY_NOT_IMPORTED"],
            "1372 runner feed gives the symbolic Cassini/gamma formula and rejects old proxy import.",
        ),
        (
            "SRC2110_23_1590_doc",
            SRC_1590_DOC,
            ["fixed `L0`", "Q_norm <= Q_alg+Q_cdb+Q_mem+Q_bdy+Q_trans+Q_proj", "No R2/fR"],
            "1590 synthesizes the current best GK owner status.",
        ),
        (
            "SRC2110_24_1590_owner",
            CSV_1590_OWNER,
            ["OBS1590_0_conditional_theorem", "OBS1590_5_owner_verdict", "OWNER_BUNDLE_NOT_CLOSED_CURRENT_CORPUS"],
            "1590 owner synthesis says the route guides derivation but cannot promote local GR.",
        ),
        (
            "SRC2110_25_1590_fixed",
            CSV_1590_FIXED,
            ["FLG1590_0_parent_action_branch", "FLG1590_5_verdict", "ZERO_THEOREM_NOT_DERIVED"],
            "1590 fixed-L0 gate keeps algebraic branch nonclaim because cdb/memory residuals survive.",
        ),
        (
            "SRC2110_26_1039_boundary",
            SRC_1039_DOC,
            ["proper compact representative-X transformations", "full_boundary_claim_not_promoted"],
            "1039 supplies only a narrow boundary sublemma, not full source/test boundary silence.",
        ),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needles, use in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            row(
                source_id=source_id,
                source_kind="2110_GK_owner_or_tail_bound",
                source_path=str(path),
                path_exists=exists,
                needles="; ".join(needles),
                needle_found=exists and all(needle in text for needle in needles),
                use_in_2110=use,
                valid_for_claim=False,
            )
        )
    return rows


def owner_bundle_rows() -> list[dict[str, object]]:
    specs = [
        (
            "GKO2110_0_target",
            "S_GK/Khat/q_loc owner bundle",
            "A single parent branch supplies S_GK, Gamma_eff, K_hat=K_metric, Helmholtz integrability, Euler closure, P_loc ownership and boundary no-flux.",
            "TARGET_SHARP",
            "would turn q_loc into an on-shell Ward/Euler residual, not a plateau axiom",
            "all rows below must close together",
        ),
        (
            "GKO2110_1_action_existence",
            "S_GK[g,Phi]",
            "local diffeomorphism-invariant scalar-density action exists for the GK sector",
            "NOT_SUPPLIED_CURRENT_CLAIM",
            "without S_GK, Gamma/Khat are bookkeeping",
            "parent source path, field list, boundary terms, sign convention",
        ),
        (
            "GKO2110_2_gamma_formula",
            "Gamma_eff",
            "Gamma_eff=L_cg^-2 F(m) or fixed-L0 Fhat branch is a parent scalar density with units and q-owned profiles",
            "FORMULA_SHAPE_FOUND_NOT_CLAIMABLE_DENSITY",
            "useful seed, not yet a varied density",
            "m, L_cg/L0, F units, local profile and branch convention",
        ),
        (
            "GKO2110_3_Khat_match",
            "K_hat=K_metric[Gamma_eff]",
            "live K_hat equals the metric response of sqrt(-g)Gamma_eff including volume, derivative, connection, domain and boundary terms",
            "MISSING_EXPLICIT_GAMMA_KGAMMA_MATCH",
            "q_loc keeps -P_loc div Delta_K if missing",
            "term-by-term Kmetric/Khat comparison under fixed-L0 branch",
        ),
        (
            "GKO2110_4_Helmholtz",
            "variational stress integrability",
            "delta(sqrt(-g)T_GK)/delta g has second-variation symmetry up to boundary terms",
            "NOT_CHECKED",
            "no action exists for claimed stress if it fails",
            "Helmholtz/second-variation calculation",
        ),
        (
            "GKO2110_5_Euler_Ward",
            "Euler/source closure",
            "nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A + boundary/source tails and vanishes on compact local vacuum shell",
            "NOT_DERIVED",
            "stress divergence remains physical source-exchange residual",
            "Euler equations, source silence and no external bath/spurion current",
        ),
        (
            "GKO2110_6_Ploc_owner",
            "P_loc",
            "P_loc is parent-owned, fixed before readout and commutes with local fixed-point limit",
            "OPEN",
            "projector can hide/tune force components",
            "parent projector source and commutator proof",
        ),
        (
            "GKO2110_7_boundary_no_flux",
            "theta_GK/Q_GK/boundary",
            "GK boundary and symplectic terms vanish or are fixed topological/proper subtractions on local linking surfaces",
            "OPEN_NARROW_PROPER_SUBLEMMA_ONLY",
            "bulk zero can still leak through boundary charge/mass flux",
            "full source/test boundary class; 1039 only handles proper compact representative subbranch",
        ),
        (
            "GKO2110_8_verdict",
            "owner bundle current claim",
            "GKO2110_1 through GKO2110_7 are parent-signed on the same branch",
            "FAIL_CURRENT_CLAIM",
            "local GR/Newton/PPN cannot reopen from GK owner yet",
            "retain Q_norm/GK tail rows",
        ),
    ]
    return [
        row(
            owner_id=owner_id,
            object=object_,
            required_statement=required_statement,
            current_status=current_status,
            consequence=consequence,
            missing_for_claim=missing_for_claim,
            valid_for_claim=False,
        )
        for owner_id, object_, required_statement, current_status, consequence, missing_for_claim in specs
    ]


def fixed_l0_rows() -> list[dict[str, object]]:
    specs = [
        ("FL02110_0_action_branch", "S_GK^0=-int sqrt(-g)L0^-2 Fhat(m;m*)", "PARENT_ACTION_CLOSURE_BRANCH_WRITTEN", "candidate action branch exists as closure contract", "parent adoption; sign convention; global subtraction"),
        ("FL02110_1_volume", "Fhat(m*)=0 or source-independent background subtraction", "CLOSED_UNDER_STRICT_DOUBLE_ZERO_CLOSURE", "volume metric response can vanish under strict clauses", "parent signature; source-independent m*"),
        ("FL02110_2_m_chain", "Fhat_prime(m*)=0 plus fixed/locked m", "CLOSED_UNDER_FIXED_FIELD_DOUBLE_ZERO_CLOSURE", "first m-chain variation can vanish", "parent m fixed-field signature and local lock"),
        ("FL02110_3_L_chain", "L_cg=L0 fixed under Hilbert variation", "CLOSED_UNDER_FIXED_L0_CLOSURE", "old M_L chain is closed in this branch", "parent adoption and separation from readout lengths"),
        ("FL02110_4_gradient_source", "nabla Gamma_eff quadratic in delta m near m*", "REDUCED_TO_QUADRATIC_NORM_BOUND", "source vector starts at second order if m locks", "Delta_m, Delta_grad_m, transition/support/no-hair theorem"),
        ("FL02110_5_cdb", "K_conn/K_domain/K_boundary", "OPEN_RETAINED_RESIDUAL", "connection/domain/boundary response is independent of algebraic closure", "no-flux/commutator theorem or component bounds"),
        ("FL02110_6_memory", "memory kinetic/source/bath/boundary stress", "OPEN_RETAINED_RESIDUAL", "algebraic subtraction does not delete memory stress", "constant-m no-hair/source/bath/boundary theorem or finite bounds"),
        ("FL02110_7_verdict", "fixed-L0 double-zero local residual theorem", "ZERO_THEOREM_NOT_DERIVED", "best branch closes algebraic sector but not full local residual", "carry Q_norm bound or derive residual theorem"),
    ]
    return [
        row(
            fixed_id=fixed_id,
            channel=channel,
            current_status=current_status,
            what_is_proved=what_is_proved,
            still_missing=still_missing,
            valid_for_claim=False,
        )
        for fixed_id, channel, current_status, what_is_proved, still_missing in specs
    ]


def residual_bound_rows() -> list[dict[str, object]]:
    specs = [
        ("QNR2110_0_total", "Q_norm", "Q_norm <= Q_alg + Q_cdb + Q_mem + Q_bdy + Q_trans + Q_proj", "SYMBOLIC_DECOMPOSITION_DERIVED", "component bounds plus A_ref/norm/domain convention", "total nonclaim no-cancellation residual"),
        ("QNR2110_1_Q_alg", "Q_alg", "A_ref^-1 L0^-2 |Fhat''(m*)| Delta_m Delta_grad_m + O(Delta_m^2 Delta_grad_m)", "SYMBOLIC_BOUND_FORM_DERIVED", "Delta_m; Delta_grad_m; Fhat''; L0; A_ref", "algebraic quadratic source bound"),
        ("QNR2110_2_Q_cdb", "Q_cdb", "A_ref^-1 N_div (K_conn_norm + K_domain_norm + K_boundary_norm + K_comm_norm)", "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING", "N_div and CDB component norms", "main live non-algebraic local-theorem blocker"),
        ("QNR2110_3_Q_mem", "Q_mem", "A_ref^-1 (N_kin K_mem_kin + N_pot K_mem_drift + N_src J_mem + N_bath B_mem)", "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING", "memory no-hair/source/bath norms", "memory stress cannot be hidden in Gamma closure"),
        ("QNR2110_4_Q_bdy", "Q_bdy", "A_ref^-1 N_bdy ||pullback(B_C)||_partialD plus corner/reference terms", "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING", "boundary primitive/measure/no-flux or edge bound", "local topology alone is insufficient"),
        ("QNR2110_5_Q_trans", "Q_trans", "A_ref^-1 (U_B^(2pS)C_S/L_tr + U_B^pL C_L/L_tr + U_B^pT C_T/L_tr)", "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING", "U_B;pS;pL;pT;L_tr;C_S;C_L;C_T", "transition/support scaling channel"),
        ("QNR2110_6_Q_proj", "Q_proj", "A_ref^-1 ||[P_loc, divergence/trace/readout] K_res||", "SYMBOLIC_BOUND_FORM_DERIVED_INPUTS_MISSING", "P_loc definition; readout convention; commutator norm", "projector/readout leakage channel"),
        ("QNR2110_7_gamma_feed", "B_gamma", "B_gamma <= (c^2/(2U_min)) N_G N_D Q_norm", "SYMBOLIC_CASSINI_BOUND_READY", "U_min,N_G,N_D and Q_i values", "local PPN gamma lane, nonclaim"),
        ("QNR2110_8_no_cancellation", "policy", "every Q_i is bounded independently; no cancellation between channels", "GUARD_READY", "source-backed component rows before pass", "prevents tuned residual cancellation"),
    ]
    return [
        row(
            residual_id=residual_id,
            quantity=quantity,
            bound_formula=bound_formula,
            current_status=current_status,
            needed_inputs=needed_inputs,
            claim_effect=claim_effect,
            score_ready=False,
            valid_for_claim=False,
        )
        for residual_id, quantity, bound_formula, current_status, needed_inputs, claim_effect in specs
    ]


def finite_tail_rows() -> list[dict[str, object]]:
    specs = [
        ("GKT2110_0_GK_tail", "epsilon_GK", "||delta_v Gamma_eff|| + ||delta_v K_hat|| + ||q_loc||", "MISSING_SGK_OWNER_OR_NUMERIC_BOUND", "finite GK/q_loc tail if owner bundle fails"),
        ("GKT2110_1_Delta_K", "Delta_K^{mu nu}", "K_hat^{mu nu}-K_metric^{mu nu}[Gamma_eff]", "MISSING_EXPLICIT_GAMMA_KGAMMA_MATCH", "metric-response mismatch drives q_loc"),
        ("GKT2110_2_Q_alg", "Q_alg", "quadratic fixed-L0 algebraic source bound", "MISSING_AMPLITUDE_GRADIENT_LAW", "needs Delta_m and gradient law"),
        ("GKT2110_3_Q_cdb", "Q_cdb", "connection/domain/boundary divergence residual", "MISSING_CDB_COMPONENT_BOUNDS", "main non-algebraic local residual"),
        ("GKT2110_4_Q_mem", "Q_mem", "memory kinetic/source/bath stress residual", "MISSING_MEMORY_STRESS_ZERO_OR_BOUND", "cosmology-memory/local-stress bridge remains live"),
        ("GKT2110_5_Q_proj", "Q_proj", "P_loc/projector/readout commutator residual", "MISSING_PLOC_OWNER_OR_BOUND", "projector can hide force components"),
        ("GKT2110_6_Q_total", "Q_norm", "Q_alg+Q_cdb+Q_mem+Q_bdy+Q_trans+Q_proj", "MISSING_COMPONENT_VALUES_AND_COMMON_NORM", "absolute-sum local residual envelope"),
        ("GKT2110_7_arena", "tau_R10,tau_PPN,tau_clock,tau_orbital", "observable response maps from Q_norm/epsilon_GK", "MISSING_ARENA_PROJECTION", "needed before any local-test score"),
    ]
    return [
        row(
            tail_id=tail_id,
            retained_tail=retained_tail,
            finite_formula=finite_formula,
            current_status=current_status,
            meaning=meaning,
            score_ready=False,
            valid_prediction_row=False,
            valid_for_claim=False,
        )
        for tail_id, retained_tail, finite_formula, current_status, meaning in specs
    ]


def gate_rows() -> list[dict[str, object]]:
    specs = [
        ("GATE2110_0_conditional_theorem", "S_GK/Khat/q_loc conditional theorem is written", True, "1351/2110 give the exact Ward/Euler contract"),
        ("GATE2110_1_fixed_L0_progress", "fixed-L0 double-zero closes algebraic chain under strict closure", True, "1371/1590 establish real algebraic progress"),
        ("GATE2110_2_parent_action_promoted", "S_GK^0 is accepted as parent MTS action branch", False, "parent adoption, sign convention and source-independent m* are missing"),
        ("GATE2110_3_Khat_match", "live K_hat equals metric response of S_GK^0", False, "Delta_K/Kmetric comparison and CDB kernels remain missing"),
        ("GATE2110_4_zero_theorem", "full q_loc zero theorem closes", False, "K_conn/K_domain/K_boundary and memory stress remain live"),
        ("GATE2110_5_finite_tail_policy", "Q_norm/GK finite tail retained", True, "symbolic residual envelope and no-cancellation policy are installed"),
        ("GATE2110_6_local_GR_Newton", "derived local GR/Newton follows", False, "GK owner bundle is not parent-signed"),
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
            "DEC2110_0_result",
            "GK_OWNER_BUNDLE_NOT_CLOSED",
            "The conditional theorem is sharp and fixed-L0/double-zero closes the algebraic chain, but live Khat matching, CDB, memory, P_loc and boundary debts block promotion.",
            "no local-GR/Newton/PPN claim from 2110",
        ),
        (
            "DEC2110_1_real_progress",
            "ALGEBRAIC_CHAIN_CLOSED_UNDER_STRICT_CLOSURE",
            "Volume, m-chain and L-chain are no longer vague blockers under fixed L0, Fhat(m*)=0 and Fhat_prime(m*)=0.",
            "treat Q_alg as quadratic/norm-bound rather than first-order source if m-lock is later sourced",
        ),
        (
            "DEC2110_2_best_next",
            "FIXED_L0_KHAT_METRIC_RESPONSE_MATCH_FIRST",
            "The owner bundle cannot be parent-signed until K_metric from S_GK^0 is compared to the live K_hat and the CDB residual is isolated.",
            "compute or reject Khat=Kmetric under fixed-L0 branch; otherwise fill Q_cdb/Delta_K row",
        ),
        (
            "DEC2110_3_fallback",
            "Q_NORM_TAIL_RETAINED",
            "If the Khat match fails or remains unsourced, the local branch must carry Q_alg+Q_cdb+Q_mem+Q_bdy+Q_trans+Q_proj with no cancellation.",
            "no empirical local pass until component values, units and arena projections exist",
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
            route_id="NEXT2110_0_2111",
            next_target="2111-Y5-R2FR-fixed-L0-Khat-metric-response-match-or-Qcdb-bound.md",
            script="scripts/Y5_R2FR_fixed_L0_Khat_metric_response_match_or_Qcdb_bound_2111.py",
            objective="Under the fixed-L0 double-zero branch, compute or reject the live K_hat = K_metric[Gamma_eff] match: separate closed algebraic volume/m/L terms from K_conn, K_domain, K_boundary and projector commutator terms; if no match closes, retain Q_cdb/Delta_K finite bound rows with source paths, units and no-cancellation.",
            forbidden_shortcuts="declaring Khat equal by notation; ignoring volume term; using fixed-L0 to delete derivative/domain/boundary kernels; importing old compact-shell proxy as Q_norm; local-GR/Newton/PPN claim; formalization-workbench edits; GitHub action",
            valid_for_claim=False,
        )
    ]


def write_branch_copies(
    owner: list[dict[str, object]],
    fixed_l0: list[dict[str, object]],
    residuals: list[dict[str, object]],
    tails: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2110_0_source_weight_docs",
            SOURCE_WEIGHT_DOCS / "AFRAME_GK_OWNER_2110_NONCLAIM.csv",
            owner + fixed_l0 + residuals + decisions,
        ),
        (
            "COPY2110_1_branch_locked_wep",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2110_GK_OWNER_STATUS_NONCLAIM.csv",
            fixed_l0 + residuals + tails,
        ),
        (
            "COPY2110_2_acquisition_queue",
            QUEUE / "JR2110_FIXED_L0_KHAT_MATCH_OR_QCDB_QUEUE.csv",
            tails + next_target,
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
    owner: list[dict[str, object]],
    fixed_l0: list[dict[str, object]],
    residuals: list[dict[str, object]],
    tails: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(source.get("path_exists")) and truthy(source.get("needle_found")) for source in sources)
    owner_ok = any(row_.get("owner_id") == "GKO2110_8_verdict" and row_.get("current_status") == "FAIL_CURRENT_CLAIM" for row_ in owner)
    fixed_ok = (
        any(row_.get("fixed_id") == "FL02110_1_volume" and row_.get("current_status") == "CLOSED_UNDER_STRICT_DOUBLE_ZERO_CLOSURE" for row_ in fixed_l0)
        and any(row_.get("fixed_id") == "FL02110_7_verdict" and row_.get("current_status") == "ZERO_THEOREM_NOT_DERIVED" for row_ in fixed_l0)
    )
    residuals_ok = (
        any(row_.get("residual_id") == "QNR2110_0_total" and row_.get("current_status") == "SYMBOLIC_DECOMPOSITION_DERIVED" for row_ in residuals)
        and any(row_.get("residual_id") == "QNR2110_8_no_cancellation" and row_.get("current_status") == "GUARD_READY" for row_ in residuals)
    )
    tails_ok = (
        len(tails) >= 8
        and any(row_.get("tail_id") == "GKT2110_6_Q_total" and row_.get("current_status") == "MISSING_COMPONENT_VALUES_AND_COMMON_NORM" for row_ in tails)
        and all(not truthy(row_.get("valid_for_claim")) for row_ in tails)
    )
    gates_ok = (
        all(not truthy(row_.get("claim_allowed")) for row_ in gates)
        and any(row_.get("gate_id") == "GATE2110_6_local_GR_Newton" and not truthy(row_.get("gate_pass")) for row_ in gates)
        and any(row_.get("gate_id") == "GATE2110_5_finite_tail_policy" and truthy(row_.get("gate_pass")) for row_ in gates)
    )
    decision_ok = any(row_.get("decision") == "FIXED_L0_KHAT_METRIC_RESPONSE_MATCH_FIRST" for row_ in decisions)
    next_ok = any(row_.get("route_id") == "NEXT2110_0_2111" and "fixed-L0-Khat-metric-response-match" in str(row_.get("next_target")) for row_ in next_target)
    copies_ok = len(copies) == 3 and all(truthy(row_.get("path_exists")) and truthy(row_.get("parse_ok")) for row_ in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claims = all(
        not truthy(row_.get("valid_for_claim")) and not truthy(row_.get("claim_allowed")) and not truthy(row_.get("score_ready"))
        for collection in (sources, owner, fixed_l0, residuals, tails, gates, decisions, next_target, copies)
        for row_ in collection
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2110_artifacts()
    no_pycache = not (SCRIPT_PATH.parent / "__pycache__").exists()
    checks = [
        ("VAL2110_00_sources", sources_ok, "all cited source paths exist and contain expected GK/fixed-L0/Qnorm needles"),
        ("VAL2110_01_owner", owner_ok, "GK owner bundle is complete but fails current claim"),
        ("VAL2110_02_fixed_L0", fixed_ok, "fixed-L0 double-zero progress is separated from full zero-theorem failure"),
        ("VAL2110_03_residuals", residuals_ok, "Q_norm decomposition and no-cancellation policy are present"),
        ("VAL2110_04_tails", tails_ok, "finite GK/Qnorm tails are retained explicitly and unscoreable"),
        ("VAL2110_05_claim_gates", gates_ok, "local-GR/Newton gate remains blocked while finite-tail policy passes"),
        ("VAL2110_06_decision", decision_ok, "decision selects fixed-L0 Khat metric-response match next"),
        ("VAL2110_07_next", next_ok, "next target is 2111 fixed-L0 Khat metric-response match or Qcdb bound"),
        ("VAL2110_08_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2110_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2110_10_no_claim_flags", no_claims, "no generated row allows a claim or score"),
        ("VAL2110_11_formalization_clean", formalization_clean, "formalization-workbench untouched by 2110"),
        ("VAL2110_12_no_pycache", no_pycache, "scripts __pycache__ removed"),
    ]
    overall = all(ok for _, ok, _ in checks)
    checks.append(
        (
            "VAL2110_OVERALL",
            overall,
            "2110 tests the GK owner bundle, records fixed-L0 algebraic progress, blocks local-GR promotion, and selects Khat metric-response match next",
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
    owner: list[dict[str, object]],
    fixed_l0: list[dict[str, object]],
    residuals: list[dict[str, object]],
    tails: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2110 - Y5/R2FR Gamma-Khat-q_loc Parent Action Owner Or DqZ/GK Tail Bound",
        "",
        "## Current Verdict",
        "",
        "2110 separates real progress from overclaim. The `S_GK/Khat/q_loc` route is mathematically sharp: if one parent scalar-density action owns `Gamma_eff`, if live `K_hat` is its metric response, if Helmholtz/Euler/source/boundary clauses close, and if `P_loc` is parent-owned, then `q_loc` becomes an on-shell Ward/Euler residual rather than a plateau axiom.",
        "",
        "The fixed-`L0` double-zero branch is the strongest current candidate. It genuinely closes the algebraic volume, `m`-chain, and `L_cg`-chain under strict closure clauses. But it does not close the full local-GR branch: `K_conn`, `K_domain`, `K_boundary`, memory/source stress, transition support, `P_loc` commutators, and arena projections remain live.",
        "",
        "So 2110 does not promote local GR/Newton/PPN. It keeps the finite `Q_norm/GK` residual lane explicit and selects the next concrete derivation target: compute or reject the fixed-`L0` `K_hat=K_metric[Gamma_eff]` match, isolating `Q_cdb/Delta_K` if the match fails.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_path", "path_exists", "needle_found", "use_in_2110", "valid_for_claim"]),
        "## GK Owner Bundle Gate",
        md_table(owner, ["owner_id", "object", "current_status", "required_statement", "consequence", "missing_for_claim", "valid_for_claim"]),
        "## Fixed-L0 Double-Zero Ledger",
        md_table(fixed_l0, ["fixed_id", "channel", "current_status", "what_is_proved", "still_missing", "valid_for_claim"]),
        "## Qnorm Residual Bound Ledger",
        md_table(residuals, ["residual_id", "quantity", "current_status", "bound_formula", "needed_inputs", "claim_effect", "score_ready", "valid_for_claim"]),
        "## Finite GK Tail Rows",
        md_table(tails, ["tail_id", "retained_tail", "current_status", "finite_formula", "meaning", "score_ready", "valid_prediction_row", "valid_for_claim"]),
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
    owner = owner_bundle_rows()
    fixed_l0 = fixed_l0_rows()
    residuals = residual_bound_rows()
    tails = finite_tail_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2110_SOURCE_REGISTER.csv",
        "owner": OUT / "P8_Y5_PARENT_QLOC_2110_GK_OWNER_BUNDLE_GATE.csv",
        "fixed": OUT / "P8_Y5_PARENT_QLOC_2110_FIXED_L0_DOUBLE_ZERO_LEDGER.csv",
        "residuals": OUT / "P8_Y5_PARENT_QLOC_2110_QNORM_RESIDUAL_BOUND_LEDGER.csv",
        "tails": OUT / "P8_Y5_PARENT_QLOC_2110_FINITE_GK_TAIL_ROWS.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2110_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2110_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2110_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2110_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2110_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["owner"], owner)
    write_csv(paths["fixed"], fixed_l0)
    write_csv(paths["residuals"], residuals)
    write_csv(paths["tails"], tails)
    write_csv(paths["gates"], gates)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_target)
    copies = write_branch_copies(owner, fixed_l0, residuals, tails, decisions, next_target)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(r["destination"])) for r in copies]
    remove_pycache()
    validation = validation_rows(sources, owner, fixed_l0, residuals, tails, gates, decisions, next_target, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, owner, fixed_l0, residuals, tails, gates, decisions, next_target, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
