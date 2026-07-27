from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3619"
BRANCH_ID = "MTS_R2FR_Y5_VISIBLE_EM_ACTION_DOMAIN_OR_SCREEN_COEFFICIENT_3619"
DOC = ROOT / "3619-Y5-R2FR-visible-EM-action-domain-exhaustion-or-screen-coefficient-row.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def output_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3619_SOURCE_REGISTER.csv",
        "domain_theorem": RESIDUALS / "P8_Y5_R2FR_3619_VISIBLE_EM_DOMAIN_EXHAUSTION_THEOREM.csv",
        "exclusion_matrix": RESIDUALS / "P8_Y5_R2FR_3619_EM_OPERATOR_EXCLUSION_MATRIX.csv",
        "screen_coefficient_rows": RESIDUALS / "P8_Y5_R2FR_3619_FIRST_SCREEN_COEFFICIENT_ROWS.csv",
        "zero_branch_promotion_gate": RESIDUALS / "P8_Y5_R2FR_3619_ZERO_BRANCH_PROMOTION_GATE.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3619_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3619_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3619_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_visible_EM_action_domain_or_screen_coefficient_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3619_VALIDATION.csv",
    }


def source_map() -> dict[str, tuple[Path, str]]:
    return {
        "handoff_3618": (
            RESIDUALS / "P8_Y5_R2FR_3618_NEXT_TARGET.csv",
            "3619-Y5-R2FR-visible-EM-action-domain-exhaustion-or-screen-coefficient-row.md",
        ),
        "screen_zero_3618": (
            RESIDUALS / "P8_Y5_R2FR_3618_SCREEN_SPLIT_ZERO_THEOREM.csv",
            "no_chi_EM",
        ),
        "operator_gate_3618": (
            RESIDUALS / "P8_Y5_R2FR_3618_OPERATOR_DIMENSION_ENERGY_SCALING_GATE.csv",
            "two-derivative independent principal constitutive tensor",
        ),
        "branch_packet_3618": (
            RESIDUALS / "P8_Y5_R2FR_3618_SCREEN_BRANCH_PACKET.csv",
            "MISSING_PARENT_AMPLITUDE",
        ),
        "visible_em_3505": (
            RESIDUALS / "P8_Y5_R2FR_3505_VISIBLE_EM_ACTION_DOMAIN_THEOREM.csv",
            "typed-domain exclusion theorem",
        ),
        "action_domain_vector_3505": (
            RESIDUALS / "P8_EM_visible_action_domain_exhaustion_no_chiEM_bound_vector.csv",
            "Delta_chi_principal",
        ),
        "observed_hodge_3503": (
            RESIDUALS / "P8_Y5_R2FR_3503_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv",
            "observed Hodge/coframe owner",
        ),
        "hodge_uniqueness_3504": (
            RESIDUALS / "P8_Y5_R2FR_3504_HODGE_UNIQUENESS_THEOREM.csv",
            "unique Hodge star",
        ),
        "em_owner_3465": (
            RESIDUALS / "P8_Y5_R2FR_3465_EM_OWNER_PACKAGE_AUDIT.csv",
            "unique Maxwell curvature norm",
        ),
        "no_hidden_visible_2659": (
            RESIDUALS / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
            "typed-domain exclusion lemma",
        ),
        "unique_f2_1235": (
            RESIDUALS / "P8_Y5_R10_1235_UNIQUE_F2_TYPED_COEFFICIENT_DOMAIN_PROOF_ATTEMPT.csv",
            "UNIQUE_F2_NOT_CLOSED_DEMOTE_TO_FINITE_RESIDUAL",
        ),
        "readout_2637": (
            RESIDUALS / "P8_Y5_READOUT_EREADOUT_CERTIFICATE_2637_CONDITIONAL_READOUT_LEMMA.csv",
            "readout theorem",
        ),
        "f2_gates_3212": (
            RESIDUALS / "P8_Y5_R2FR_3212_NO_EXTRA_F2_THEOREM_GATES.csv",
            "F2G3212_1_no_independent_F2",
        ),
    }


def source_register_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    rows = []
    for source_id, source_data in source_map().items():
        source_path, needle = source_data
        exists = source_path.exists()
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(source_path),
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(source_path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def domain_theorem_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "VED3619_0_domain_contract",
            "claim_piece": "visible EM object-language",
            "statement": "The local visible EM action-domain is exhausted if the only dynamical EM arguments are A_Q, F_Q=dA_Q, e_obs(q), fixed orientation and fixed representation/current data.",
            "formal_statement": "Args(S_EM^local)={A_Q,F_Q,e_obs(q),J_Q,Rep_fixed,orientation_fixed}; Coeff(S_EM) subset q^*A_Q plus A_fixed",
            "derivation": "This is the action grammar required to make Hodge uniqueness an actual theorem rather than a convention.",
            "result": "DOMAIN_CONTRACT_EXACT_NOT_PARENT_SIGNED",
            "source_path": str(sources["visible_em_3505"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "VED3619_1_two_derivative_basis",
            "claim_piece": "two-derivative local gauge invariant basis",
            "statement": "Given the domain contract and no extra tensor slots, the two-derivative local gauge/diffeomorphism invariant principal EM terms reduce to the observed-Hodge Maxwell term plus a constant/topological axion.",
            "formal_statement": "L_2 = -Z_Q/4 F_ab F_cd g_obs^{ac}g_obs^{bd} sqrt(-g_obs) + theta_0 F wedge F",
            "derivation": "Gauge invariance gives F=dA; the observed metric/coframe and orientation provide the only local index contractions; Hodge uniqueness fixes the contraction.",
            "result": "EXACT_CONDITIONAL_BASIS",
            "source_path": str(sources["hodge_uniqueness_3504"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "VED3619_2_skewon_absence",
            "claim_piece": "skewon/nonreciprocal exclusion",
            "statement": "A true local action contributes the reciprocal/symmetric principal constitutive part; skewon-like response is not an independent conservative action coefficient.",
            "formal_statement": "S=-1/4 int F_A chi^{AB} F_B only sees chi^{(AB)}; skewon belongs to non-Lagrangian/effective branch",
            "derivation": "The bilinear action symmetrizes exchange of the two F factors before variation.",
            "result": "EXACT_CONDITIONAL_ACTION_EXCLUSION",
            "source_path": str(sources["action_domain_vector_3505"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "VED3619_3_no_hidden_slots",
            "claim_piece": "no hidden Hodge/coefficient morphism",
            "statement": "If the coefficient algebra is q-pulled plus fixed data, a hidden-visible Hodge or coefficient map is ill-typed rather than small.",
            "formal_statement": "v in ker(Dq), c_vis in q^*A_Q plus A_fixed => D_v c_vis=0; Hom(C_hid,Coeff_EM) absent",
            "derivation": "The no-hidden-visible-hom theorem is exact relative to the typed domain premise.",
            "result": "EXACT_CONDITIONAL_NO_HIDDEN_SLOT",
            "source_path": str(sources["no_hidden_visible_2659"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "VED3619_4_readout_ordering",
            "claim_piece": "readout-after-variation discipline",
            "statement": "Post-solution EM readout cannot source the parent equations; if a readout-reduced action is varied, it is a separate effective branch that must carry a coefficient row.",
            "formal_statement": "R_EM:Sol(S_parent)->Obs is source-silent; varied S_red[A,g,chi_readout] implies E_readout != 0",
            "derivation": "Euler derivatives exist only for arguments of the action being varied.",
            "result": "EXACT_CONDITIONAL_WITH_COUNTERBRANCH",
            "source_path": str(sources["readout_2637"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "VED3619_5_screen_zero_if_domain_signed",
            "claim_piece": "h_split zero promotion",
            "statement": "If rows VED3619_0 through VED3619_4 are parent-signed on the same local branch and higher-derivative screen terms are absent, the 3618 zero branch is promoted: h_split=0.",
            "formal_statement": "domain_signed && no_HD_screen && constant_or_absent_axion_gradient => h_split=0, B_Fresnel_MTS=0, xi_MTS_eff=0",
            "derivation": "The only surviving principal local EM term is proportional to the observed-Hodge identity on the two-polarization screen.",
            "result": "PROMOTION_RULE_DERIVED_NOT_PROMOTED",
            "source_path": str(sources["screen_zero_3618"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "VED3619_6_verdict",
            "claim_piece": "visible EM action-domain verdict",
            "statement": "3619 gives an exact conditional local EM action-domain proof, but it does not pretend the parent has signed the domain; therefore nonzero coefficient rows remain necessary.",
            "formal_statement": "conditional_zero_available && parent_signature_missing => retain first screen coefficient rows",
            "derivation": "This preserves rigor while moving the coupling bottleneck to a single parent object-language signature.",
            "result": "EXACT_CONDITIONAL_THEOREM_PLUS_NONZERO_ROWS",
            "source_path": str(sources["visible_em_3505"][0]),
            "parent_signed": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def exclusion_matrix_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "exclusion_id": "EXM3619_0_independent_chi",
            "candidate_operator": "independent chi_EM principal tensor",
            "counterterm": "Delta S=-1/4 int F_ab chi_EM^{abcd} F_cd vol_obs",
            "exclusion_route": "Args(S_EM) excludes chi_EM and no hidden-visible coefficient target",
            "if_excluded": "h_split contribution zero",
            "if_not_excluded": "SCR3619_0_chi_aniso_s0 coefficient row is live",
            "current_status": "NOT_PARENT_EXCLUDED",
            "source_path": str(sources["visible_em_3505"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "exclusion_id": "EXM3619_1_hidden_hodge",
            "candidate_operator": "hidden/disformal Hodge map",
            "counterterm": "g_EM = g_obs + C_H u u + C_X X; *_EM=*(g_EM)",
            "exclusion_route": "no hidden-visible hom from motion/time representative data into visible EM Hodge",
            "if_excluded": "hidden-Hodge screen split zero",
            "if_not_excluded": "C_Hodge_hidden / screen coefficient row remains live",
            "current_status": "NOT_PARENT_EXCLUDED",
            "source_path": str(sources["no_hidden_visible_2659"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "exclusion_id": "EXM3619_2_extra_F2",
            "candidate_operator": "independent Maxwell kinetic multiplier",
            "counterterm": "Delta S=-1/4 int lambda_X F wedge *_obs F",
            "exclusion_route": "unique parent curvature norm plus no independent F_Q^2 slot",
            "if_excluded": "no source-normalization drift from F2 multiplier",
            "if_not_excluded": "not a screen split if scalar, but source/alpha/Newton coupling remains live",
            "current_status": "UNIQUE_F2_NOT_CLOSED",
            "source_path": str(sources["unique_f2_1235"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "exclusion_id": "EXM3619_3_readout_reentry",
            "candidate_operator": "readout-after-variation Hodge/coefficient",
            "counterterm": "S_red[A,g,chi_readout] varied after readout",
            "exclusion_route": "strict readout-after-solution discipline, no reduced-action claim credit",
            "if_excluded": "readout does not source h_split",
            "if_not_excluded": "readout branch gets finite coefficient row",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "source_path": str(sources["readout_2637"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "exclusion_id": "EXM3619_4_higher_derivative_screen",
            "candidate_operator": "dimension-five/six screen operator",
            "counterterm": "M_*^-n int F nabla^n F with parent-flow tensor",
            "exclusion_route": "local two-derivative branch restriction or explicit parent high-frequency operator row",
            "if_excluded": "HD screen split zero",
            "if_not_excluded": "SCR3619_1_dim5_s1 or SCR3619_2_dim6_s2 row is live",
            "current_status": "NOT_PARENT_EXCLUDED",
            "source_path": str(sources["operator_gate_3618"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "exclusion_id": "EXM3619_5_axion_gradient",
            "candidate_operator": "axion-gradient polarization rotation",
            "counterterm": "theta(Phi) F wedge F with dtheta != 0",
            "exclusion_route": "theta absent or fixed representation constant",
            "if_excluded": "no axion-gradient rotation branch",
            "if_not_excluded": "separate axion-gradient coefficient row, not B_Fresnel screen split",
            "current_status": "SEPARATE_GATE_LIVE",
            "source_path": str(sources["action_domain_vector_3505"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def screen_coefficient_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": "SCR3619_0_chi_aniso_s0",
            "operator_class": "two-derivative independent principal constitutive tensor",
            "coefficient_symbol": "C_chi_aniso",
            "schematic_action": "Delta S=-1/4 int F_ab chi_aniso^{abcd} F_cd vol_obs",
            "h_AB_projection": "h_AB=omega^-2 e_A^a delta P_ab[chi_aniso](k) e_B^b",
            "h_split_projection": "TF_2(h_AB)",
            "energy_power_s": 0,
            "M_star": "not_applicable_for_s0",
            "gamma0": "MISSING_PARENT_ROOT_NORMALIZATION",
            "C_screen": "MISSING_SCREEN_NORM",
            "B_Fresnel_MTS": "MISSING_PARENT_AMPLITUDE_OR_THEOREM_BAN",
            "source_path": str(sources["visible_em_3505"][0]),
            "score_status": "LIVE_COUNTERMODEL_ROW_NOT_PARENT_OWNED",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": "SCR3619_1_dim5_s1",
            "operator_class": "dimension-five parent-flow/high-frequency birefringent screen operator",
            "coefficient_symbol": "C_5_screen",
            "schematic_action": "Delta S~M_*^-1 int n^mu F_{mu alpha} nabla_beta F^{beta alpha} or parent-flow equivalent",
            "h_AB_projection": "diam_spec(h)<=C_screen B_Fresnel_MTS (k/M_*)",
            "h_split_projection": "linear-in-energy transverse spectral diameter",
            "energy_power_s": 1,
            "M_star": "MISSING_PARENT_SCALE",
            "gamma0": "MISSING_PARENT_ROOT_NORMALIZATION",
            "C_screen": "MISSING_SCREEN_NORM",
            "B_Fresnel_MTS": "MISSING_PARENT_AMPLITUDE",
            "source_path": str(sources["operator_gate_3618"][0]),
            "score_status": "TYPED_PROMISING_ROW_VALUES_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "coefficient_id": "SCR3619_2_dim6_s2",
            "operator_class": "dimension-six curvature/memory/two-extra-derivative screen operator",
            "coefficient_symbol": "C_6_screen",
            "schematic_action": "Delta S~M_*^-2 int F nabla^2 F or curvature/memory equivalent",
            "h_AB_projection": "diam_spec(h)<=C_screen B_Fresnel_MTS (k/M_*)^2",
            "h_split_projection": "quadratic-in-energy transverse spectral diameter",
            "energy_power_s": 2,
            "M_star": "MISSING_PARENT_SCALE",
            "gamma0": "MISSING_PARENT_ROOT_NORMALIZATION",
            "C_screen": "MISSING_SCREEN_NORM",
            "B_Fresnel_MTS": "MISSING_PARENT_AMPLITUDE",
            "source_path": str(sources["operator_gate_3618"][0]),
            "score_status": "TYPED_ALTERNATE_ROW_VALUES_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def zero_branch_promotion_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "ZPG3619_0_observed_Hodge",
            "required_clause": "S_EM uses only *_obs[e_obs(q)] for the principal Maxwell term",
            "current_evidence": "conditional theorem exists",
            "source_path": str(sources["observed_hodge_3503"][0]),
            "passes_now": False,
            "missing_for_promotion": "parent visible EM generator signature",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "ZPG3619_1_no_independent_chi",
            "required_clause": "Args(S_EM) excludes independent chi_EM/background constitutive tensors",
            "current_evidence": "typed-domain theorem exact conditionally",
            "source_path": str(sources["visible_em_3505"][0]),
            "passes_now": False,
            "missing_for_promotion": "parent object-language/action-domain certificate",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "ZPG3619_2_no_extra_F2",
            "required_clause": "unique parent Maxwell curvature norm/no independent F2",
            "current_evidence": "known blocker ledger says not closed",
            "source_path": str(sources["f2_gates_3212"][0]),
            "passes_now": False,
            "missing_for_promotion": "T_Q norm, unique curvature norm, current owner, radiative/readout closure",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "ZPG3619_3_no_HD_screen",
            "required_clause": "no dimension-five/six screen operator in the local branch",
            "current_evidence": "typed rows exist but no parent ban",
            "source_path": str(sources["operator_gate_3618"][0]),
            "passes_now": False,
            "missing_for_promotion": "local branch derivative-order theorem or explicit high-frequency sector split",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "ZPG3619_4_same_current_charge",
            "required_clause": "A_Q, J_Q, kinetic norm and alpha/current normalization share one owner",
            "current_evidence": "owner package says values missing",
            "source_path": str(sources["em_owner_3465"][0]),
            "passes_now": False,
            "missing_for_promotion": "charge/current normalization owner; source coupling calibration",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_gate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3619_0_conditional_domain_theorem",
            "decision": "Visible EM action-domain exhaustion is now written as an exact conditional theorem with explicit premises.",
            "status": "PASS_CONDITIONAL_NOT_PARENT_SIGNED",
            "next_action": "attempt parent visible generator signature, not a fit",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3619_1_nonzero_rows",
            "decision": "Because the parent signature is not closed, the first nonzero screen coefficient rows are produced with operator class, s, M_*, gamma0, C_screen and B_Fresnel_MTS fields.",
            "status": "PASS_TYPED_ROWS_VALUES_MISSING",
            "next_action": "either ban these operators or source their coefficients",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3619_2_dangerous_branch",
            "decision": "The dangerous branch remains s=0 independent chi_EM; it should be banned by parent grammar before spending effort fitting it.",
            "status": "DANGEROUS_BRANCH_EXPLICIT",
            "next_action": "prove no independent chi_EM / no hidden-visible coefficient slot",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3619_3_source_coupling_next",
            "decision": "The next practical local-GR target is the calibrated EM/source owner: unique F2 plus charge/current normalization.",
            "status": "NEXT_TARGET_SELECTED",
            "next_action": "3620-Y5-R2FR-EM-source-coupling-owner-or-F2-coefficient-bound.md",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS3619_0",
            "result": "CONDITIONAL_EM_DOMAIN_THEOREM_AND_FIRST_SCREEN_COEFFICIENT_ROWS",
            "summary": "3619 derives the visible EM action-domain exhaustion theorem conditionally and, because the parent signature is not closed, emits typed nonzero screen coefficient rows for s=0, s=1 and s=2 branches.",
            "zero_branch_promoted": False,
            "screen_coefficient_rows_written": True,
            "next_pressure_point": "unique F2 plus charge/current/source coupling owner",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3619_0",
            "target_doc": "3620-Y5-R2FR-EM-source-coupling-owner-or-F2-coefficient-bound.md",
            "target_script": "scripts/Y5_R2FR_3620_EM_source_coupling_owner_or_F2_coefficient_bound.py",
            "objective": "derive whether the same parent owner fixes the Maxwell kinetic norm, charge/current normalization and EM Hilbert source coupling; if not, produce the first calibrated F2/source-coupling coefficient bound row",
            "success_gate": "either unique F2 plus charge/current owner is promoted as a parent-signed local branch, or finite coefficient rows for lambda_F2, b_alpha/source coupling and current normalization are produced",
            "reason": "3619 compressed screen birefringence to action-domain and coefficient rows; source coupling calibration is now the local-GR/Newton pressure point.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "visible_EM_domain": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "screen_zero_branch": "READY_BUT_NOT_PROMOTED",
            "screen_coefficients": "S0_S1_S2_TYPED_VALUES_MISSING",
            "dangerous_branch": "independent_chi_EM_s0",
            "next_pressure_point": "EM_source_coupling_unique_F2_charge_current_owner",
            "claim_status": "NO_CLAIM",
            "valid_for_claim": False,
        }
    ]


def write_markdown() -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3619 Y5 R2FR: visible EM action-domain exhaustion or screen coefficient row",
                "",
                "## Verdict",
                "- The visible EM action-domain proof is now exact as a conditional theorem.",
                "- It is **not** promoted to a parent-signed claim, because the parent object-language/action-domain certificate is still missing.",
                "- Because of that, the first nonzero `h_AB` screen coefficient rows are now explicit instead of foggy.",
                "",
                "## Conditional action-domain theorem",
                "- Required local EM arguments: `{A_Q, F_Q=dA_Q, e_obs(q), J_Q, fixed representation/current data, fixed orientation}`.",
                "- Required coefficient algebra: `q^*A_Q + A_fixed`, with no hidden-visible coefficient slot.",
                "- Then the two-derivative local gauge/diffeomorphism invariant principal action reduces to observed-Hodge Maxwell plus constant/topological axion.",
                "- Therefore the two-polarization screen split vanishes:",
                "- `domain_signed && no_HD_screen && constant_or_absent_axion_gradient => h_split=0`.",
                "",
                "## What is still not closed",
                "- Independent `chi_EM` is not parent-forbidden yet.",
                "- Unique `F_Q^2` / Maxwell kinetic normalization is not parent-closed yet.",
                "- Higher-derivative screen terms are not parent-forbidden yet.",
                "- Charge/current normalization and source coupling still need the same owner.",
                "",
                "## First nonzero coefficient rows",
                "- `SCR3619_0_chi_aniso_s0`: dangerous two-derivative independent principal tensor, `s=0`.",
                "- `SCR3619_1_dim5_s1`: dimension-five parent-flow/high-frequency screen operator, `s=1`.",
                "- `SCR3619_2_dim6_s2`: dimension-six curvature/memory screen operator, `s=2`.",
                "- All are nonclaim and missing parent values: `M_*`, `gamma0`, `C_screen`, and `B_Fresnel_MTS` where applicable.",
                "",
                "## Practical read",
                "- Best route remains banning the `s=0` independent `chi_EM` branch by parent grammar.",
                "- If the theory wants a nonzero high-frequency EM effect, it must declare the operator dimension and source scale explicitly.",
                "- The local-GR/Newton bottleneck now shifts toward calibrated EM source coupling: unique `F2`, charge/current owner, and source normalization.",
                "",
                "## Next target",
                "- `3620-Y5-R2FR-EM-source-coupling-owner-or-F2-coefficient-bound.md`.",
                "- Aim: derive the common owner for Maxwell kinetic norm, charge/current normalization, and EM Hilbert source coupling; otherwise emit finite coefficient rows.",
                "",
                "## Claim status",
                "- `NO_CLAIM`: exact conditional theorem plus typed coefficient rows.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def validate() -> list[dict[str, object]]:
    timestamp = utc_now()
    paths = output_paths()
    results: list[tuple[str, bool, str]] = []

    sources = source_map()
    sources_exist = all(source_path.exists() for source_path, _needle in sources.values())
    needles_found = all(source_path.exists() and contains(source_path, needle) for source_path, needle in sources.values())
    results.append(("VAL3619_0_sources_exist", sources_exist, "all required 3619 source paths exist"))
    results.append(("VAL3619_1_needles_found", needles_found, "all selected 3619 source anchors found"))

    pre_validation_paths = [path for name, path in paths.items() if name != "validation"]
    outputs_exist = DOC.exists() and all(path.exists() for path in pre_validation_paths)
    results.append(("VAL3619_2_outputs_exist", outputs_exist, "all pre-validation 3619 outputs written"))

    parse_details: list[str] = []
    csv_parse_pass = True
    for name, path in paths.items():
        if name == "validation":
            continue
        try:
            parse_details.append(f"{name}:{len(read_csv(path))}")
        except Exception as exception:
            csv_parse_pass = False
            parse_details.append(f"{name}:ERROR:{exception}")
    results.append(("VAL3619_3_csv_parse", csv_parse_pass, "; ".join(parse_details)))

    theorem_rows = read_csv(paths["domain_theorem"]) if paths["domain_theorem"].exists() else []
    domain_contract_written = any("Args(S_EM^local)" in row["formal_statement"] for row in theorem_rows)
    promotion_rule_written = any("h_split=0" in row["formal_statement"] for row in theorem_rows)
    conditional_not_signed = bool(theorem_rows) and all(row["parent_signed"] == "False" for row in theorem_rows)
    results.append(("VAL3619_4_domain_contract_written", domain_contract_written, "visible EM domain contract written"))
    results.append(("VAL3619_5_promotion_rule_written", promotion_rule_written, "h_split zero promotion rule written"))
    results.append(("VAL3619_6_conditional_not_parent_signed", conditional_not_signed, "domain theorem remains conditional/nonclaim"))

    coefficient_rows = read_csv(paths["screen_coefficient_rows"]) if paths["screen_coefficient_rows"].exists() else []
    required_fields = {"operator_class", "energy_power_s", "M_star", "gamma0", "C_screen", "B_Fresnel_MTS", "source_path"}
    coeff_fields_ok = bool(coefficient_rows) and all(required_fields.issubset(row.keys()) for row in coefficient_rows)
    coeff_s_values = {str(row["energy_power_s"]) for row in coefficient_rows}
    coeff_nonclaim = bool(coefficient_rows) and all(
        row["score_ready"] == "False" and row["claim_allowed"] == "False" and row["valid_for_claim"] == "False"
        for row in coefficient_rows
    )
    results.append(("VAL3619_7_screen_coefficient_fields", coeff_fields_ok, "screen coefficient rows declare required bridge fields"))
    results.append(("VAL3619_8_s0_s1_s2_rows_present", coeff_s_values == {"0", "1", "2"}, "s=0, s=1 and s=2 coefficient rows present"))
    results.append(("VAL3619_9_coefficient_rows_nonclaim", coeff_nonclaim, "screen coefficient rows remain nonclaim/not score-ready"))

    promotion_rows = read_csv(paths["zero_branch_promotion_gate"]) if paths["zero_branch_promotion_gate"].exists() else []
    promotion_blocked = bool(promotion_rows) and all(row["passes_now"] == "False" for row in promotion_rows)
    results.append(("VAL3619_10_zero_branch_not_promoted", promotion_blocked, "zero branch promotion correctly remains blocked"))

    all_outputs_nonclaim = True
    for name, path in paths.items():
        if name == "validation" or not path.exists():
            continue
        for row in read_csv(path):
            if row.get("valid_for_claim") == "True" or row.get("claim_allowed") == "True":
                all_outputs_nonclaim = False
    results.append(("VAL3619_11_all_outputs_nonclaim", all_outputs_nonclaim, "all generated rows remain nonclaim"))

    formalization_clean = True
    formalization_detail = "formalization-workbench not found"
    if FORMALIZATION.exists():
        leaked_paths = list(FORMALIZATION.rglob("*3619*"))
        formalization_clean = len(leaked_paths) == 0
        formalization_detail = "no 3619 files in formalization-workbench" if formalization_clean else "; ".join(str(path) for path in leaked_paths[:5])
    results.append(("VAL3619_12_no_formalization_leak", formalization_clean, formalization_detail))

    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in results
    ]


def main() -> None:
    paths = output_paths()
    write_csv(paths["source_register"], source_register_rows())
    write_csv(paths["domain_theorem"], domain_theorem_rows())
    write_csv(paths["exclusion_matrix"], exclusion_matrix_rows())
    write_csv(paths["screen_coefficient_rows"], screen_coefficient_rows())
    write_csv(paths["zero_branch_promotion_gate"], zero_branch_promotion_rows())
    write_csv(paths["decision_gates"], decision_gate_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_csv(paths["canonical_status"], canonical_status_rows())
    write_markdown()
    write_csv(paths["validation"], validate())

    failed = [row for row in read_csv(paths["validation"]) if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3619 validation failed: {failed}")
    print(f"wrote 3619 checkpoint with {len(read_csv(paths['validation']))} validation checks")


if __name__ == "__main__":
    main()
