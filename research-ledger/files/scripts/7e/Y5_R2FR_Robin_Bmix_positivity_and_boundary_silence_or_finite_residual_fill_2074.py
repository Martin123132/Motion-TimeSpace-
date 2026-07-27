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


DOC = ROOT / "2074-Y5-R2FR-Robin-Bmix-positivity-and-boundary-silence-or-finite-residual-fill.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()


def formalization_has_2074_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2074-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2074*",
        "*Y5_R2FR_Robin_Bmix_positivity_and_boundary_silence_or_finite_residual_fill_2074*",
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
            "SRC2074_00_2073_doc",
            ROOT / "2073-Y5-R2FR-reciprocal-fixed-point-and-quadratic-Bmix-origin-or-finite-cap-residual.md",
            ["NEXT2073_0_2074", "W_R>0", "k_C>=0", "finite residual rows"],
            "2073 handoff to Robin activation certificates or finite residual fill.",
        ),
        (
            "SRC2074_01_2073_theorem",
            OUT / "P8_Y5_PARENT_QLOC_2073_ROBIN_FIXED_POINT_THEOREM.csv",
            ["RFT2073_4_energy_identity", "CONDITIONAL_RECIPROCAL_FIXED_POINT_THEOREM", "THEOREM_SHAPE_DERIVED_PARENT_CERTIFICATES_MISSING"],
            "conditional Robin fixed-point theorem and its missing parent certificates.",
        ),
        (
            "SRC2074_02_2073_origin",
            OUT / "P8_Y5_PARENT_QLOC_2073_BMIX_ORIGIN_AUDIT.csv",
            ["BOA2073_0_bulk_owner", "BOA2073_3_kC_positivity", "PARENT_ORIGIN_NOT_CLOSED"],
            "machine-readable list of parent-origin blockers.",
        ),
        (
            "SRC2074_03_vacuum_contract",
            ROOT / "04-vacuum-reciprocity-action-contract.md",
            ["d/dr [ W(r,L,fields) dR_AB/dr ] = J_R", "W > 0", "attempt the reciprocal-strain theorem"],
            "legacy reciprocal-strain contract provides the operator shape but not a parent sign certificate.",
        ),
        (
            "SRC2074_04_reciprocity_attempt",
            ROOT / "05-reciprocity-theorem-attempt.md",
            ["S_R = integral dr [0.5 W(r) (R_AB')^2 + J_R R_AB].", "W R_AB' = Q_R.", "Asymptotic flatness alone does not kill"],
            "strain-action attempt shows why Q_R hair survives without a no-charge theorem.",
        ),
        (
            "SRC2074_05_cell_current",
            ROOT / "11-cell-current-origin-attempt.md",
            ["W partial_r R_AB = Q_R.", "R_AB = -Q_R/r.", "gives a Ward identity, not R_AB=0."],
            "ordinary current conservation is insufficient for local GR.",
        ),
        (
            "SRC2074_06_noether_guard",
            ROOT / "12-gauge-noether-origin-audit.md",
            ["Noether identity", "parent action", "closure benchmark"],
            "Noether identities do not set the reciprocal charge to zero without a parent constraint.",
        ),
        (
            "SRC2074_07_theta_qtau",
            OUT / "P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv",
            ["QTA1008_0_L_parent", "QTA1008_2_J_tau", "QTA1008_8_Q_total"],
            "theta/Q_tau ownership remains unpromoted; this blocks Xi_tau.",
        ),
        (
            "SRC2074_08_boundary_grammar",
            OUT / "P8_Y5_PARENT_QLOC_2062_BOUNDARY_FUNCTIONAL_GRAMMAR.csv",
            ["BGA2062_0_boundary_split", "BGA2062_3_corner_worldtube", "BGA2062_4_orientation"],
            "boundary split, corner/worldtube and orientation blockers.",
        ),
        (
            "SRC2074_09_qrhat_policy",
            OUT / "P8_Y5_R10_1249_FINITE_QRHAT_CANDIDATE_RESULTS.csv",
            ["QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM", "ACCEPTED_NONCLAIM_FINITE_QRHAT", "REJECT_ZERO_THEOREM_UNDERIVED"],
            "finite q_R_hat policy row exists as an external nonclaim ceiling, not a theory prediction.",
        ),
        (
            "SRC2074_10_hcore_charge",
            OUT / "P8_Y5_R10_1253_NO_CHARGE_THEOREM_CANDIDATE.csv",
            ["NCT1253_0_ordinary_conservation", "NCT1253_2_topological_neutrality", "NCT1253_4_compact_boundary_silence"],
            "no-charge theorem candidates remain conditional/rejected rather than parent signed.",
        ),
        (
            "SRC2074_11_missing_parent_euler",
            OUT / "P8_Y5_R10_1275_MISSING_PARENT_EULER_SOURCE_MAP.csv",
            ["MPE1275_3_W_positive", "MPE1275_4_boundary_no_charge", "MPE1275_5_import_guard"],
            "R_AB local branch still lacks the positive W and no-charge parent map.",
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


def activation_certificate_rows() -> list[dict[str, object]]:
    data = [
        (
            "ACT2074_0_bulk_W",
            "W_R positive bulk operator",
            "Need a parent-owned reciprocal kinetic term with W_R>=W_min>0 on the local exterior annulus.",
            "04/05/1275 contain the contract and sign requirement, but not the parent coefficient derivation.",
            "CANDIDATE_CONTRACT_ONLY",
            False,
        ),
        (
            "ACT2074_1_cap_stiffness",
            "k_C nonnegative Robin stiffness",
            "Need k_C=2 beta_mix c2 Xi_tau mu_C>=k_min>=0 with units, orientation and source/reference split fixed.",
            "2072/2073 select quadratic Bmix, but beta_mix, Xi_tau and mu_C sign are not parent signed.",
            "FAIL_UNSIGNED_PRODUCT_POSITIVITY",
            False,
        ),
        (
            "ACT2074_2_Xi_tau",
            "Xi_tau current scalar",
            "Need Xi_tau to descend from theta_MTS/Q_tau^MTS or a named source-current owner.",
            "1008 marks parent action variation missing, J_tau formal only, and Q_tau^MTS not promoted.",
            "FAIL_MISSING_THETA_QTAU_OWNER",
            False,
        ),
        (
            "ACT2074_3_bulk_silence",
            "rho_R=0 or bounded",
            "Need a no-source theorem in the local exterior or a sourced norm row for rho_R.",
            "11/1253 show ordinary conservation leaves Q_R hair; no topological neutrality proof is signed.",
            "FAIL_NO_CHARGE_THEOREM_UNSIGNED",
            False,
        ),
        (
            "ACT2074_4_boundary_silence",
            "b_C=0 and outer flux silence",
            "Need corner/worldtube/source/reference terms either absent by grammar or absolute-bounded.",
            "2062 identifies corner/worldtube and orientation as dominant unsigned blockers.",
            "FAIL_BOUNDARY_CORNER_SILENCE_UNSIGNED",
            False,
        ),
        (
            "ACT2074_5_qR_policy",
            "DeltaR to q_R_hat score map",
            "Need a dimensionless q_R_hat map from DeltaR/flux plus a comparison policy that does not import closure zero.",
            "1249 supplies an external nonclaim q_R_hat ceiling only; the theory prediction chain is missing.",
            "FAIL_QRHAT_PREDICTION_CHAIN_MISSING",
            False,
        ),
        (
            "ACT2074_6_verdict",
            "Robin fixed-point activation",
            "The conditional theorem is mathematically useful but cannot be activated as local GR yet.",
            "At least five parent certificates remain unsigned; route converts to finite residual bound acquisition.",
            "ROBIN_ACTIVATION_BLOCKED_USE_FINITE_RESIDUAL_FILL",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, certificate, required_signature, evidence_status, verdict, parent_signed in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "certificate": certificate,
                "required_signature": required_signature,
                "evidence_status": evidence_status,
                "verdict": verdict,
                "parent_signed": parent_signed,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def w_bulk_operator_rows() -> list[dict[str, object]]:
    data = [
        (
            "WRA2074_0_operator_shape",
            "partial_r[W_R partial_r DeltaR]=rho_R",
            "04 and 05 contain the reciprocal-strain operator/action template.",
            "OPERATOR_SHAPE_EXISTS",
            False,
        ),
        (
            "WRA2074_1_positive_requirement",
            "W_R>=W_min>0",
            "04 explicitly lists W>0 and 2073 needs it for coercivity.",
            "SIGN_REQUIREMENT_WRITTEN_NOT_DERIVED",
            False,
        ),
        (
            "WRA2074_2_parent_owner",
            "W_R = delta^2 S_parent/d(grad R_AB)^2 or equivalent",
            "1275 still lists MPE1275_3_W_positive as a missing parent object.",
            "PARENT_OWNER_MISSING",
            False,
        ),
        (
            "WRA2074_3_source_silence",
            "rho_R=0 in the local exterior",
            "05 and 11 show Q_R survives unless J_R/rho_R and boundary charge are killed.",
            "SOURCE_SILENCE_NOT_PROVED",
            False,
        ),
        (
            "WRA2074_4_verdict",
            "W_R activation",
            "Use W_R as a candidate coefficient in the finite energy-bound template; do not use it as a signed theorem-zero input.",
            "W_R_CANDIDATE_ONLY_FINITE_ROW_REQUIRED",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_id, evidence, status, parent_signed in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object_id": object_id,
                "evidence": evidence,
                "status": status,
                "parent_signed": parent_signed,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def kc_xitau_positivity_rows() -> list[dict[str, object]]:
    data = [
        (
            "KXP2074_0_formula",
            "k_C = 2 beta_mix c2 Xi_tau mu_C",
            "inherited from 2072/2073 quadratic Bmix cap term",
            "FORMULA_SELECTED_CONDITIONALLY",
            False,
        ),
        (
            "KXP2074_1_c2",
            "c2>0",
            "positive quadratic minimum can be chosen as a stability design condition",
            "DESIGN_SIGN_ALLOWED_NOT_PARENT_DERIVED",
            False,
        ),
        (
            "KXP2074_2_beta_mix",
            "beta_mix sign and units",
            "no parent mixed-coupling coefficient row exists",
            "MISSING_PARENT_BETA_MIX",
            False,
        ),
        (
            "KXP2074_3_Xi_tau",
            "Xi_tau sign and current ownership",
            "1008 says parent action variation missing, J_tau formal only, Q_tau^MTS not promoted",
            "MISSING_PARENT_XI_TAU",
            False,
        ),
        (
            "KXP2074_4_mu_C",
            "cap measure/orientation mu_C",
            "2062 leaves normal direction, corner joins and source/reference split unsigned",
            "MISSING_CAP_MEASURE_ORIENTATION",
            False,
        ),
        (
            "KXP2074_5_verdict",
            "k_C>=0 activation",
            "product positivity cannot be claimed until every factor has a source row and the cap orientation is fixed",
            "KC_POSITIVITY_BLOCKED",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, factor, evidence, status, parent_signed in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "factor": factor,
                "evidence": evidence,
                "status": status,
                "parent_signed": parent_signed,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def boundary_silence_rows() -> list[dict[str, object]]:
    data = [
        (
            "BSA2074_0_split",
            "B_total = B_GR + B_ref + B_corner + B_R",
            "2062 grammar says boundary silence requires B_R absent/constant and all other terms accounted.",
            "ACCOUNTING_SPLIT_EXISTS",
            False,
        ),
        (
            "BSA2074_1_natural_variation",
            "if B_R absent then W_R n^mu partial_mu R_AB=0",
            "This is the clean zero route only if the boundary class is parent signed.",
            "CONDITIONAL_ZERO_ROUTE",
            False,
        ),
        (
            "BSA2074_2_corner_worldtube",
            "Pi_R^corner and source-worldtube endpoint terms",
            "2062 labels this the dominant unsigned blocker.",
            "UNSIGNED_DOMINANT_BLOCKER",
            False,
        ),
        (
            "BSA2074_3_orientation",
            "Q_R = W_R n^mu partial_mu R_AB = -Pi_R^tot",
            "finite scoring needs normal direction, W_R, N_sphere and Z_R_infty.",
            "UNSIGNED_FOR_FINITE_SCORING",
            False,
        ),
        (
            "BSA2074_4_residue",
            "b_C and outer_flux",
            "must be zero by theorem or retained as absolute residual rows; cancellation is forbidden.",
            "FINITE_RESIDUAL_ROWS_REQUIRED",
            False,
        ),
        (
            "BSA2074_5_verdict",
            "boundary silence",
            "not activated; use b_C, outer_flux and corner/source rows in the finite bound template.",
            "BOUNDARY_SILENCE_BLOCKED",
            False,
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, object_id, evidence, status, parent_signed in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "object_id": object_id,
                "evidence": evidence,
                "status": status,
                "parent_signed": parent_signed,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def finite_residual_fill_rows() -> list[dict[str, object]]:
    data = [
        (
            "FRF2074_0_energy_identity",
            "E_R",
            "E_R := integral_A W_R |grad DeltaR|^2 + integral_C k_C DeltaR^2",
            "energy-like reciprocal units",
            "E_R = F_outer + <DeltaR,rho_R>_A + <DeltaR,b_C>_C",
            "DERIVED_CONDITIONAL_IDENTITY",
        ),
        (
            "FRF2074_1_coercivity",
            "c_E",
            "c_E from W_R_min, k_C_min, C_Poincare and C_trace",
            "positive energy constant",
            "E_R >= c_E ||DeltaR||_E^2 if W_R_min>0 and boundary/reference class is fixed",
            "MISSING_NUMERIC_COERCIVITY_CONSTANTS",
        ),
        (
            "FRF2074_2_bulk_norm",
            "rho_R_norm",
            "||rho_R||_{H^{-1}(A)} or sourced equivalent",
            "dual reciprocal-source norm",
            "|<DeltaR,rho_R>| <= ||DeltaR||_{H^1(A)} ||rho_R||_{H^{-1}(A)}",
            "MISSING_BULK_SOURCE_NORM",
        ),
        (
            "FRF2074_3_boundary_norm",
            "b_C_norm",
            "||b_C||_{H^{-1/2}(C)} plus corner/source-reference residue",
            "dual boundary-current norm",
            "|<DeltaR,b_C>| <= ||DeltaR||_{H^{1/2}(C)} ||b_C||_{H^{-1/2}(C)}",
            "MISSING_BOUNDARY_RESIDUE_NORM",
        ),
        (
            "FRF2074_4_outer_flux",
            "F_outer_abs",
            "absolute outer/asymptotic reciprocal flux after reference subtraction",
            "reciprocal-energy flux",
            "must be zero by boundary class or bounded as |F_outer|",
            "MISSING_OUTER_FLUX_BOUND",
        ),
        (
            "FRF2074_5_deltaR_bound",
            "DeltaR_bound",
            "||DeltaR||_E <= function(W_R_min,k_C_min,C_P,C_T,rho_R_norm,b_C_norm,F_outer_abs)",
            "dimensionless or reciprocal strain after normalization",
            "turns failed zero theorem into a finite PPN/R10 residual input",
            "BOUND_FORM_DERIVED_NUMERIC_INPUTS_MISSING",
        ),
        (
            "FRF2074_6_qR_feed",
            "q_R_hat_feed",
            "map exterior DeltaR/flux amplitude to q_R_hat without closure-zero import",
            "dimensionless",
            "compare finite prediction to 1249 policy only after parent coefficients exist",
            "MISSING_QRHAT_MAP",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, quantity, definition, units, bound_rule, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "quantity": quantity,
                "definition": definition,
                "units": units,
                "bound_rule": bound_rule,
                "status": status,
                "ready_for_scoring": False,
                "claim_allowed": False,
            }
        )
        rows.append(row)
    return rows


def qrhat_policy_rows() -> list[dict[str, object]]:
    data = [
        (
            "QPF2074_0_external_ceiling",
            "QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM",
            "q_R_hat=4.6e-05, gamma contribution=-2.3e-05",
            "external nonclaim ceiling from 1249 runner",
            "CAN_COMPARE_LATER_NOT_A_PREDICTION",
        ),
        (
            "QPF2074_1_theory_prediction",
            "q_R_hat[MTS]",
            "requires DeltaR/flux normalization, Z_R_infty, source mass convention and parent coefficients",
            "not present in 2074",
            "MISSING_THEORY_PREDICTION_CHAIN",
        ),
        (
            "QPF2074_2_closure_guard",
            "q_R_hat=0 closure",
            "zero can be a private closure benchmark but not a derived prediction",
            "1249 rejects zero theorem underived",
            "REJECT_ZERO_THEOREM_UNDERIVED",
        ),
        (
            "QPF2074_3_policy_verdict",
            "finite q_R policy",
            "hold all q_R/R10/PPN local claims until finite residual rows are numeric and parent-sourced",
            "nonclaim only",
            "LOCAL_SCORE_BLOCKED",
        ),
    ]
    rows: list[dict[str, object]] = []
    for row_id, policy_object, value_or_requirement, evidence, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "policy_object": policy_object,
                "value_or_requirement": value_or_requirement,
                "evidence": evidence,
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
            "RUN2074_0_activation_attempt",
            "activate Robin fixed-point theorem",
            "FAIL_PARENT_CERTIFICATES_UNSIGNED",
            "W_R shape exists but W_R owner, k_C positivity, Xi_tau, rho_R silence, b_C silence and q_R map are not signed.",
            False,
        ),
        (
            "RUN2074_1_finite_residual_fill",
            "convert theorem failure to finite residual acquisition",
            "PASS_SCHEMA_ONLY",
            "energy-bound template names W_R_min, k_C_min, rho_R_norm, b_C_norm, F_outer_abs, C_Poincare, C_trace and q_R_hat feed.",
            False,
        ),
        (
            "RUN2074_2_claim_policy",
            "local GR/PPN/R10 claim",
            "FAIL_BLOCKED_NONCLAIM",
            "No local branch claim may be made until activation certificates or numeric finite residual rows are sourced.",
            False,
        ),
        (
            "RUN2074_VERDICT",
            "Robin activation or finite residual fill",
            "ROBIN_ZERO_PROOF_NOT_ACTIVATED_FINITE_BOUND_CONTRACT_WRITTEN",
            "2075 should attack Xi_tau/k_C ownership first, then turn the energy-bound contract into a runner.",
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
        (
            "GATE2074_0_internal_robin_theorem",
            "conditional Robin theorem remains usable internally",
            "PASS_CONDITIONAL_ONLY",
            "2073 energy identity is kept as a derivation target, not evidence.",
        ),
        (
            "GATE2074_1_W_R_parent",
            "W_R positive operator parent signed",
            "FAIL_BLOCKED",
            "operator shape/sign requirement exists but parent kinetic coefficient is missing.",
        ),
        (
            "GATE2074_2_kC_parent",
            "k_C>=0 parent signed",
            "FAIL_BLOCKED",
            "beta_mix, Xi_tau, mu_C/orientation and units are missing.",
        ),
        (
            "GATE2074_3_source_silence",
            "rho_R=b_C=F_outer=0",
            "FAIL_BLOCKED",
            "ordinary conservation leaves Q_R hair and boundary/corner silence is unsigned.",
        ),
        (
            "GATE2074_4_finite_numeric",
            "finite residual bound can score",
            "FAIL_BLOCKED",
            "bound schema exists but lacks W_R_min,k_C_min,norm constants and q_R_hat normalization.",
        ),
        (
            "GATE2074_5_local_claim",
            "local GR/Newton/PPN/R10 claim",
            "FAIL_BLOCKED",
            "no theorem-zero activation and no finite prediction row.",
        ),
        (
            "GATE2074_6_formalization",
            "formalization-workbench edit allowed",
            "PASS_NO_EDIT",
            "2074 stays in post-checkpoint-work.",
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
            "DEC2074_0_activation_failed_cleanly",
            "DO_NOT_CLAIM_ROBIN_ZERO",
            "2074 cannot sign the parent certificates; that is useful because it prevents a fake local-GR pass.",
        ),
        (
            "DEC2074_1_W_shape_survives",
            "KEEP_W_R_OPERATOR_CONTRACT",
            "The reciprocal-strain operator shape and energy identity remain a valid derivation scaffold.",
        ),
        (
            "DEC2074_2_coupling_bottleneck",
            "COUPLING_IS_THE_NEXT_LOCK",
            "k_C positivity collapses to beta_mix, Xi_tau and cap measure/orientation ownership.",
        ),
        (
            "DEC2074_3_finite_fallback",
            "BUILD_ENERGY_BOUND_RUNNER_AFTER_XITAU",
            "If Xi_tau/k_C cannot be signed, the honest route is a finite residual bound feeding q_R_hat.",
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
            "target_id": "NEXT2074_0_2075",
            "target_doc": "2075-Y5-R2FR-Xi-tau-current-owner-kC-positivity-or-Robin-energy-bound-runner.md",
            "objective": "try to derive/source Xi_tau from theta_MTS/Q_tau and sign k_C=2 beta_mix c2 Xi_tau mu_C; if not, convert the 2074 energy-bound contract into a finite residual runner",
            "must_include": "theta/Q_tau source owner; beta_mix sign and units; c2 stability sign; cap measure/orientation; W_R_min and k_C_min placeholders; C_Poincare/C_trace; rho_R_norm; b_C_norm; F_outer_abs; q_R_hat feed",
            "excluded": "calling q_R_hat=0 a theorem; importing GR radial equations as proof; fitted boundary cancellation; ratio-only Kcap scoring; local-GR/PPN/R10 claim; GitHub; formalization-workbench edits",
            "claim_allowed": False,
        }
    )
    return [row]


def write_branch_copies(
    activation: list[dict[str, object]],
    w_rows: list[dict[str, object]],
    kc_rows: list[dict[str, object]],
    boundary_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    qr_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        (
            "COPY2074_0_source_weight_activation",
            SOURCE_WEIGHT_DOCS / "AFRAME_ROBIN_BMIX_ACTIVATION_CERTIFICATE_AUDIT_2074_NONCLAIM.csv",
            activation,
        ),
        (
            "COPY2074_1_source_weight_W_R",
            SOURCE_WEIGHT_DOCS / "AFRAME_ROBIN_BMIX_WR_BULK_OPERATOR_AUDIT_2074_NONCLAIM.csv",
            w_rows,
        ),
        (
            "COPY2074_2_source_weight_kC_Xi",
            SOURCE_WEIGHT_DOCS / "AFRAME_ROBIN_BMIX_KC_XITAU_POSITIVITY_AUDIT_2074_NONCLAIM.csv",
            kc_rows,
        ),
        (
            "COPY2074_3_source_weight_boundary",
            SOURCE_WEIGHT_DOCS / "AFRAME_ROBIN_BMIX_BOUNDARY_SILENCE_AUDIT_2074_NONCLAIM.csv",
            boundary_rows,
        ),
        (
            "COPY2074_4_source_weight_finite_residual",
            SOURCE_WEIGHT_DOCS / "AFRAME_ROBIN_BMIX_FINITE_RESIDUAL_FILL_2074_NONCLAIM.csv",
            residual_rows,
        ),
        (
            "COPY2074_5_wep_dry_run",
            BRANCH_WEP / "P8_Y5_PARENT_QLOC_2074_ROBIN_ACTIVATION_DRY_RUN_NONCLAIM.csv",
            dry_rows_,
        ),
        (
            "COPY2074_6_queue_next",
            QUEUE / "JR2074_XITAU_KC_OR_ROBIN_ENERGY_BOUND_NEXT_NONCLAIM.csv",
            next_rows_,
        ),
        (
            "COPY2074_7_queue_qrhat_policy",
            QUEUE / "JR2074_QRHAT_POLICY_FEED_NONCLAIM.csv",
            qr_rows,
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
    activation: list[dict[str, object]],
    w_rows: list[dict[str, object]],
    kc_rows: list[dict[str, object]],
    boundary_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    qr_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources)
    csv_ok = all(csv_rows_parse(path) for path in csv_paths)
    activation_ok = any(
        row["row_id"] == "ACT2074_6_verdict"
        and row["verdict"] == "ROBIN_ACTIVATION_BLOCKED_USE_FINITE_RESIDUAL_FILL"
        and not bool(row["parent_signed"])
        for row in activation
    )
    w_ok = any(row["row_id"] == "WRA2074_0_operator_shape" and row["status"] == "OPERATOR_SHAPE_EXISTS" for row in w_rows) and any(
        row["row_id"] == "WRA2074_4_verdict" and row["status"] == "W_R_CANDIDATE_ONLY_FINITE_ROW_REQUIRED" for row in w_rows
    )
    kc_ok = any(row["row_id"] == "KXP2074_5_verdict" and row["status"] == "KC_POSITIVITY_BLOCKED" for row in kc_rows)
    boundary_ok = any(row["row_id"] == "BSA2074_5_verdict" and row["status"] == "BOUNDARY_SILENCE_BLOCKED" for row in boundary_rows)
    residual_keys = {"W_R_min", "k_C_min", "rho_R_norm", "b_C_norm", "F_outer_abs", "C_Poincare", "C_trace", "q_R_hat"}
    residual_text = "\n".join(str(value) for row in residual_rows for value in row.values())
    residual_ok = all(key in residual_text for key in residual_keys) and any(
        row["row_id"] == "FRF2074_5_deltaR_bound" and row["status"] == "BOUND_FORM_DERIVED_NUMERIC_INPUTS_MISSING" for row in residual_rows
    )
    qr_ok = any(row["row_id"] == "QPF2074_0_external_ceiling" and row["status"] == "CAN_COMPARE_LATER_NOT_A_PREDICTION" for row in qr_rows) and any(
        row["row_id"] == "QPF2074_2_closure_guard" and row["status"] == "REJECT_ZERO_THEOREM_UNDERIVED" for row in qr_rows
    )
    dry_ok = any(
        row["run_id"] == "RUN2074_VERDICT"
        and row["verdict"] == "ROBIN_ZERO_PROOF_NOT_ACTIVATED_FINITE_BOUND_CONTRACT_WRITTEN"
        and not bool(row["accepted_for_scoring"])
        for row in dry_rows_
    )
    gates_ok = all(row["claim_allowed"] is False and row["status"] != "PASS_CLAIM" for row in gates)
    next_ok = next_rows_[0]["target_id"] == "NEXT2074_0_2075"
    copies_ok = all(Path(str(row["path"])).exists() and csv_rows_parse(Path(str(row["path"]))) for row in copies)
    no_claim = all(
        not bool(row.get("claim_allowed", False)) and not bool(row.get("valid_for_claim", False))
        for group in [sources, activation, w_rows, kc_rows, boundary_rows, residual_rows, qr_rows, dry_rows_, gates, next_rows_, copies]
        for row in group
    )
    checks = [
        ("VAL2074_00_local_sources_exist", source_ok, "all cited source paths and needles exist"),
        ("VAL2074_01_csv_parse", csv_ok, "all generated CSV files parse cleanly"),
        ("VAL2074_02_activation_refused", activation_ok, "Robin theorem activation is refused because parent certificates remain unsigned"),
        ("VAL2074_03_W_R_candidate_only", w_ok, "W_R operator shape is preserved as candidate-only finite input"),
        ("VAL2074_04_kC_Xi_blocked", kc_ok, "k_C/Xi_tau positivity is explicitly blocked"),
        ("VAL2074_05_boundary_blocked", boundary_ok, "boundary/corner silence is explicitly blocked"),
        ("VAL2074_06_finite_residual_contract", residual_ok, "finite energy-bound contract includes required residual and coercivity inputs"),
        ("VAL2074_07_qrhat_policy", qr_ok, "q_R_hat policy feed is nonclaim and rejects closure-zero as theorem"),
        ("VAL2074_08_dry_verdict", dry_ok, "dry run records no zero proof and stages finite-bound route"),
        ("VAL2074_09_claim_gates_blocked", gates_ok, "all local claim gates remain blocked/nonclaim"),
        ("VAL2074_10_next_selected", next_ok, "2075 Xi_tau/kC or energy-bound runner target selected"),
        ("VAL2074_11_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2074_12_no_claim_flags", no_claim, "no generated row allows a claim"),
        ("VAL2074_13_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"),
        ("VAL2074_14_no_formalization_artifacts", not formalization_has_2074_artifacts(), "no 2074 artifacts were written under formalization-workbench"),
        ("VAL2074_15_no_pycache", not scripts_pycache_exists(), "scripts __pycache__ removed"),
    ]
    overall = all(ok for _, ok, _ in checks)
    checks.append(("VAL2074_OVERALL", overall, "2074 blocks Robin zero-proof activation and writes the finite residual fill contract"))
    rows: list[dict[str, object]] = []
    for check_id, ok, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "claim_allowed": False})
        rows.append(row)
    return rows


def write_doc(
    sources: list[dict[str, object]],
    activation: list[dict[str, object]],
    w_rows: list[dict[str, object]],
    kc_rows: list[dict[str, object]],
    boundary_rows: list[dict[str, object]],
    residual_rows: list[dict[str, object]],
    qr_rows: list[dict[str, object]],
    dry_rows_: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 2074 Y5 R2FR Robin Bmix Positivity And Boundary Silence Or Finite Residual Fill",
        "",
        "## Current Verdict",
        "",
        "2074 tries to activate the 2073 Robin fixed-point theorem rather than circling it. The result is a clean no-claim: the theorem shape survives, but the activation certificates do not yet sign. The branch therefore moves from `DeltaR=0` theorem-zero to a finite residual energy-bound contract.",
        "",
        "The strongest retained derivation scaffold is the energy identity",
        "",
        "`E_R = integral_A W_R |grad DeltaR|^2 + integral_C k_C DeltaR^2 = F_outer + <DeltaR,rho_R>_A + <DeltaR,b_C>_C`.",
        "",
        "If a later parent action supplies `W_R>=W_R_min>0`, `k_C>=k_C_min>=0`, `rho_R=0`, `b_C=0`, outer flux silence, and fixed cap geometry, the 2073 fixed-point theorem can activate. If not, the same identity becomes a finite residual bound using `rho_R_norm`, `b_C_norm`, `F_outer_abs`, `C_Poincare`, `C_trace`, and a `q_R_hat` feed.",
        "",
        "The bottleneck is now the coupling: `k_C = 2 beta_mix c2 Xi_tau mu_C`. The positive quadratic shape can choose `c2>0`, but `beta_mix`, `Xi_tau`, cap measure/orientation and units are not parent signed. This is why 2075 should attack `Xi_tau` and `k_C` first.",
        "",
        "No local-GR/Newton, Cassini, PPN, R10, WEP, clock, orbital, Kcap, q_R, or public claim is made. No GitHub action and no `formalization-workbench` edit is made.",
        "",
        "## Source Register",
        md_table(sources, ["source_id", "source_kind", "source_path", "status", "note", "valid_for_claim"]),
        "## Activation Certificate Audit",
        md_table(activation, ["row_id", "certificate", "required_signature", "evidence_status", "verdict", "parent_signed", "claim_allowed"]),
        "## W_R Bulk Operator Audit",
        md_table(w_rows, ["row_id", "object_id", "evidence", "status", "parent_signed", "ready_for_scoring", "claim_allowed"]),
        "## k_C / Xi_tau Positivity Audit",
        md_table(kc_rows, ["row_id", "factor", "evidence", "status", "parent_signed", "ready_for_scoring", "claim_allowed"]),
        "## Boundary Silence Audit",
        md_table(boundary_rows, ["row_id", "object_id", "evidence", "status", "parent_signed", "ready_for_scoring", "claim_allowed"]),
        "## Finite Residual Fill Contract",
        md_table(residual_rows, ["row_id", "quantity", "definition", "units", "bound_rule", "status", "ready_for_scoring", "claim_allowed"]),
        "## q_R_hat Policy Feed",
        md_table(qr_rows, ["row_id", "policy_object", "value_or_requirement", "evidence", "status", "ready_for_scoring", "claim_allowed"]),
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
    activation = activation_certificate_rows()
    w_rows = w_bulk_operator_rows()
    kc_rows = kc_xitau_positivity_rows()
    boundary_rows = boundary_silence_rows()
    residual_rows = finite_residual_fill_rows()
    qr_rows = qrhat_policy_rows()
    dry_rows_ = dry_run_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows_ = next_target_rows()
    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2074_SOURCE_REGISTER.csv",
        "activation": OUT / "P8_Y5_PARENT_QLOC_2074_ACTIVATION_CERTIFICATE_AUDIT.csv",
        "w": OUT / "P8_Y5_PARENT_QLOC_2074_W_R_BULK_OPERATOR_AUDIT.csv",
        "kc": OUT / "P8_Y5_PARENT_QLOC_2074_KC_XITAU_POSITIVITY_AUDIT.csv",
        "boundary": OUT / "P8_Y5_PARENT_QLOC_2074_BOUNDARY_SILENCE_AUDIT.csv",
        "residual": OUT / "P8_Y5_PARENT_QLOC_2074_FINITE_RESIDUAL_FILL_TEMPLATE.csv",
        "qr": OUT / "P8_Y5_PARENT_QLOC_2074_QRHAT_POLICY_FEED.csv",
        "dry": OUT / "P8_Y5_PARENT_QLOC_2074_DRY_RUN.csv",
        "gates": OUT / "P8_Y5_PARENT_QLOC_2074_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2074_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2074_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2074_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2074_VALIDATION.csv",
    }
    write_csv(paths["sources"], sources)
    write_csv(paths["activation"], activation)
    write_csv(paths["w"], w_rows)
    write_csv(paths["kc"], kc_rows)
    write_csv(paths["boundary"], boundary_rows)
    write_csv(paths["residual"], residual_rows)
    write_csv(paths["qr"], qr_rows)
    write_csv(paths["dry"], dry_rows_)
    write_csv(paths["gates"], gates)
    write_csv(paths["decision"], decisions)
    write_csv(paths["next"], next_rows_)
    copies = write_branch_copies(activation, w_rows, kc_rows, boundary_rows, residual_rows, qr_rows, dry_rows_, next_rows_)
    write_csv(paths["branch"], copies)
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(row["path"])) for row in copies]
    remove_pycache()
    validation = validation_rows(
        sources,
        activation,
        w_rows,
        kc_rows,
        boundary_rows,
        residual_rows,
        qr_rows,
        dry_rows_,
        gates,
        next_rows_,
        copies,
        csv_paths,
    )
    write_csv(paths["validation"], validation)
    write_doc(sources, activation, w_rows, kc_rows, boundary_rows, residual_rows, qr_rows, dry_rows_, gates, decisions, next_rows_, copies, validation)
    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
