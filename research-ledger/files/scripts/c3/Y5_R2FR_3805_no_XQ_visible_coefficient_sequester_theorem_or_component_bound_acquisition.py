import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3805"
BRANCH = "MTS_R2FR_Y5_NO_XQ_VISIBLE_COEFFICIENT_SEQUESTER_OR_COMPONENT_BOUND_3805"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
FWB = ROOT / "formalization-workbench"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3805-Y5-R2FR-no-XQ-visible-coefficient-sequester-theorem-or-component-bound-acquisition.md"
SCRIPT_PATH = PCW / "scripts" / "Y5_R2FR_3805_no_XQ_visible_coefficient_sequester_theorem_or_component_bound_acquisition.py"

P_1046 = PCW / "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md"
P_1050 = PCW / "1050-Y5-R10-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md"
P_1051 = PCW / "1051-Y5-R10-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md"
P_3791 = PCW / "3791-Y5-R2FR-ZEM-fixed-normalization-or-betaZ-bound.md"
P_3803 = PCW / "3803-Y5-R2FR-qX-same-source-no-extra-force-closure-or-epsilon-sourceXQ-bound.md"
P_3804 = PCW / "3804-Y5-R2FR-qX-calibration-companion-closure-or-local-bound-runner.md"
P_SPINE = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

C_1050_THEOREM = RESIDUALS / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv"
C_1050_OBSTRUCTION = RESIDUALS / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_OBSTRUCTION_LEDGER.csv"
C_1051_NO_MIXED = RESIDUALS / "P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv"
C_1051_SCALAR = RESIDUALS / "P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv"
C_1051_B_ALPHA = RESIDUALS / "P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv"
C_988_CLOCK = RESIDUALS / "P8_Y5_R10_988_CLOCK_PRODUCT_IMPORT.csv"
C_3804_INPUT = RESIDUALS / "P8_Y5_R2FR_3804_COMPANION_INPUT_VECTOR.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3805_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3805_SEQUESTER_THEOREM_ATTEMPT.csv",
    "counterexamples": RESIDUALS / "P8_Y5_R2FR_3805_VISIBLE_COEFFICIENT_COUNTEREXAMPLES.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3805_CURRENT_CORPUS_SEQUESTER_AUDIT.csv",
    "priorities": RESIDUALS / "P8_Y5_R2FR_3805_COMPONENT_BOUND_ACQUISITION_PRIORITY.csv",
    "alpha_product": RESIDUALS / "P8_Y5_R2FR_3805_B_ALPHA_PRODUCT_IMPORT_NONCLAIM.csv",
    "refusal": RESIDUALS / "P8_Y5_R2FR_3805_SEQUESTER_REFUSAL_RUNNER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3805_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3805_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3805_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3805_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3805_VALIDATION.csv",
}

SOURCE_SPECS = [
    {"source_id": "SRC3805_0_3804_handoff", "path": P_3804, "needle": "visible-coefficient issue", "role": "3804 selected no-XQ visible-coefficient sequester theorem or component bounds"},
    {"source_id": "SRC3805_1_1050_product_functor_doc", "path": P_1050, "needle": "visible-hidden product functor", "role": "earlier product-functor theorem shape"},
    {"source_id": "SRC3805_2_1051_no_mixed_doc", "path": P_1051, "needle": "surviving hidden scalar", "role": "earlier no-mixed morphism obstruction"},
    {"source_id": "SRC3805_3_1046_forbidden_vertices", "path": P_1046, "needle": "alpha_EM(Xhat) F_munu F^munu", "role": "forbidden vertex catalog for constants, masses, clocks, and source weights"},
    {"source_id": "SRC3805_4_3791_ZEM", "path": P_3791, "needle": "f(Xhat)F^2", "role": "Z_EM/lambda_A counterexample guard"},
    {"source_id": "SRC3805_5_3803_source_safety", "path": P_3803, "needle": "partial L_matter/partial X_Q=0", "role": "q_X direct source derivative theorem"},
    {"source_id": "SRC3805_6_1050_theorem_csv", "path": C_1050_THEOREM, "needle": "PFT1050_2_forbidden_mixed_hom", "role": "product functor no mixed hom clause"},
    {"source_id": "SRC3805_7_1050_obstruction_csv", "path": C_1050_OBSTRUCTION, "needle": "OBS1050_0_scalar_invariant", "role": "scalar invariant obstruction ledger"},
    {"source_id": "SRC3805_8_1051_no_mixed_csv", "path": C_1051_NO_MIXED, "needle": "NMM1051_2_scalar_counterexample", "role": "no-mixed counterexample proof"},
    {"source_id": "SRC3805_9_1051_scalar_csv", "path": C_1051_SCALAR, "needle": "ISO1051_1_Xhat_value", "role": "Xhat visible coefficient obstruction"},
    {"source_id": "SRC3805_10_1051_balpha_csv", "path": C_1051_B_ALPHA, "needle": "BAP1051_2_best_current_product", "role": "source-backed nonclaim b_alpha*tau_clock product"},
    {"source_id": "SRC3805_11_988_clock_csv", "path": C_988_CLOCK, "needle": "CLOCK988_CAS646_1_YbE3E2", "role": "clock product import source row"},
    {"source_id": "SRC3805_12_3804_input_vector", "path": C_3804_INPUT, "needle": "R3804_1_epsilon_ZEM_XQ", "role": "3804 companion input vector"},
    {"source_id": "SRC3805_13_spine", "path": P_SPINE, "needle": "3805-Y5-R2FR-no-XQ-visible-coefficient-sequester-theorem-or-component-bound-acquisition.md", "role": "live spine target"},
]


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


def load_csv(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path):
    try:
        load_csv(path)
        return True
    except Exception:
        return False


def bool_text(value):
    return "true" if value else "false"


def source_register(timestamp):
    rows = []
    for spec in SOURCE_SPECS:
        exists = spec["path"].exists()
        needle_found = False
        if exists:
            needle_found = spec["needle"] in read_text(spec["path"])
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "source_id": spec["source_id"],
                "source_path": str(spec["path"]),
                "exists": bool_text(exists),
                "needle": spec["needle"],
                "needle_found": bool_text(needle_found),
                "role": spec["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def theorem_rows(timestamp):
    specs = [
        (
            "SQT3805_0_typed_subquotient_sequester",
            "typed coefficient subquotient",
            "Let q_X=(q_obs,X_Q) and pi_obs(q_X)=q_obs. A clean sequester branch requires visible coefficient functors Coeff_vis for F^2, masses, Yukawas, kappa, source weights, clock markers, and boundary weights to factor through pi_obs(q_X) and fixed representation data theta_rep, while the only allowed X_Q morphism into the visible sector is X_Q -> Y_Q -> B_Q -> A_Q,F_Q.",
            "EXACT_CONDITIONAL_OBJECT_LANGUAGE",
            "If signed, X_Q owns EM geometry through B_Q without becoming a visible coefficient dial.",
            "parent action has not signed this typed subquotient rule",
        ),
        (
            "SQT3805_1_chain_rule_zero",
            "visible coefficient derivative zero",
            "If c_vis(Phi)=cbar(pi_obs(q_X(Phi)),theta_rep) for every visible coefficient c_vis, then partial_XQ c_vis=0 at fixed q_obs,theta_rep. Therefore partial_XQ Z_EM, partial_XQ m_A, partial_XQ kappa_eff, partial_XQ w_source, partial_XQ nu_clock, and partial_XQ D_boundary vanish outside the declared B_Q path.",
            "EXACT_CONDITIONAL_CHAIN_RULE_ZERO",
            "This would set the visible-coefficient pieces of epsilon_ZEM_XQ, epsilon_theta_XQ, epsilon_kappa_XQ, epsilon_source_XQ, and epsilon_boundary_XQ to zero.",
            "factorization through pi_obs(q_X), not full q_X, is unsigned",
        ),
        (
            "SQT3805_2_qX_visibility_obstruction",
            "why quotient closure alone fails",
            "Because X_Q is deliberately part of q_X, any smooth scalar f(X_Q) is q_X-basic. Thus q_X-basicness permits DeltaS=-1/4 int sqrt(-g) f(X_Q) F^2, m_A(X_Q) psi_bar_A psi_A, kappa(X_Q)R, w_A(X_Q)S_A, or D(X_Q) boundary weights unless the typed coefficient functor forbids them.",
            "COUNTEREXAMPLE_FROM_QX_VISIBILITY",
            "The q_X route cannot prove local GR by saying coefficients are q_X-owned; that is exactly what allows f(X_Q).",
            "need typed sequester or numeric component bounds",
        ),
        (
            "SQT3805_3_imported_no_mixed_limit",
            "no-mixed morphism limit",
            "The earlier no-mixed theorem is exact only if the hidden/extra invariant algebra has no nonconstant scalar maps into visible coefficient objects, or if Hom(C_XQ,Coeff_vis)=Const or 0. In the q_X branch, X_Q itself is a candidate scalar unless the parent declares Coeff_vis to ignore X_Q.",
            "EXACT_CONDITIONAL_WITH_ACTIVE_OBSTRUCTION",
            "This imports the 1050/1051 lesson into the local q_X route without pretending old R10 rows prove the new theorem.",
            "hidden-to-visible coefficient morphisms are not parent-excluded",
        ),
        (
            "SQT3805_4_radiative_readout_closure",
            "bare sequester is not enough",
            "Even if the bare parent action omits f(X_Q)F^2 and m_A(X_Q), the sequester theorem needs radiative/effective-action and clock/readout closure: S_eff and readout maps must still factor through pi_obs(q_X), theta_rep, and the declared B_Q path.",
            "REQUIRED_EFT_READOUT_GUARD",
            "Prevents loop/readout re-entry of alpha, clock, mass, or source weights after a clean bare action.",
            "radiative/readout closure is not signed",
        ),
        (
            "SQT3805_5_current_verdict",
            "sequester theorem promotion",
            "SQT3805_0 through SQT3805_4 would prove no-X_Q visible coefficient leakage. The current corpus supports the theorem shape but does not sign the typed subquotient, no-mixed morphism, or radiative/readout closure clauses. Therefore the strict-current proof is rejected and component-bound acquisition is required.",
            "FAIL_CURRENT_CLAIM_COMPONENT_BOUNDS_REQUIRED",
            "The route is sharper: prove coefficient subquotient ownership next, or start filling epsilon_ZEM_XQ, epsilon_theta_XQ, and epsilon_source_XQ with source-backed rows.",
            "visible coefficient sequester remains unsigned",
        ),
    ]
    rows = []
    for theorem_id, claim_piece, mathematical_form, derivation_status, result_if_signed, missing in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "theorem_id": theorem_id,
                "claim_piece": claim_piece,
                "mathematical_form": mathematical_form,
                "derivation_status": derivation_status,
                "result_if_signed": result_if_signed,
                "missing_for_current_claim": missing,
                "valid_for_claim": "false",
            }
        )
    return rows


def counterexample_rows(timestamp):
    specs = [
        ("VCX3805_0_fX_F2", "f(X_Q)F_obs^2", "epsilon_ZEM_XQ", "diffeomorphism and U1 gauge invariant if X_Q is scalar/q_X data", "changes alpha, clocks, WEP, R10", "forbid Coeff(F2) from reading X_Q or source beta_Z/lambda bound"),
        ("VCX3805_1_mass", "m_A(X_Q) psi_bar_A psi_A", "epsilon_theta_XQ", "ordinary scalar mass/Yukawa coefficient if matter functor can read X_Q", "changes mass ratios, WEP, clocks, source charge", "constant/material superselection or mass sensitivity bounds"),
        ("VCX3805_2_kappa", "kappa(X_Q) R[g_obs]", "epsilon_kappa_XQ", "local scalar multiplier of EH term unless kappa is global/superselected", "changes Gdot, PPN, orbital GM calibration", "kappa q_obs/global owner theorem or Gdot/PPN bound"),
        ("VCX3805_3_source_weight", "w_A(X_Q) S_A or kappa_A(X_Q)J_A", "epsilon_source_XQ", "source-action weight can preserve matter EOM while changing Hilbert source", "WEP/source normalization/Newton active mass leak", "no-source-weight object language or WEP/source bound"),
        ("VCX3805_4_clock_marker", "nu_i(X_Q) or clock readout marker", "epsilon_theta_XQ", "clock readout can depend on dimensionless X_Q coefficient", "clock drift/redshift and alpha-like leakage", "clock readout descent or b_clock/b_alpha product constraints"),
        ("VCX3805_5_boundary_weight", "D_boundary(X_Q) n.T.xi", "epsilon_boundary_XQ", "boundary/corner weight can be q_X-basic while altering flux", "domain, orbital, R10, clock tail leakage", "boundary no-flux theorem or finite flux bound"),
    ]
    rows = []
    for row_id, vertex, residual, why_allowed, observable_damage, repair in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "counterexample_id": row_id,
                "visible_coefficient_vertex": vertex,
                "feeds_residual": residual,
                "why_quotient_allows_it": why_allowed,
                "observable_damage": observable_damage,
                "repair_needed": repair,
                "claim_allowed": "false",
                "valid_for_claim": "false",
            }
        )
    return rows


def audit_rows(timestamp):
    specs = [
        ("AUD3805_0_product_functor", "visible/hidden product functor", "1050 proves exact conditional theorem shape.", "CONDITIONAL_ONLY", "parent product category and no mixed morphisms unsigned"),
        ("AUD3805_1_no_mixed", "no-mixed morphism", "1051 proves scalar counterexample if nonconstant invariant survives.", "CURRENT_ZERO_REJECTED", "q_X exposes X_Q as a candidate visible scalar"),
        ("AUD3805_2_qX_specific", "q_X branch", "q_X=(q_obs,X_Q) deliberately declares X_Q physical/visible for EM geometry.", "SEQUESTER_NEEDS_SUBQUOTIENT", "coefficients must factor through pi_obs(q_X), not full q_X"),
        ("AUD3805_3_ZEM", "Z_EM/lambda", "3791 keeps f(Xhat)F2/lambda_A legal unless parent-excluded.", "ACTIVE_COUNTEREXAMPLE", "no independent F2 theorem missing"),
        ("AUD3805_4_theta_source", "theta/source markers", "1046/3771 keep alpha, masses, clock markers, source weights live.", "ACTIVE_COUNTEREXAMPLES", "constant/source marker superselection missing"),
        ("AUD3805_5_bound_chain", "first numeric chain", "1051/988 provide |b_alpha*tau_clock_time| <= 2.1e-18 yr^-1 nonclaim.", "SOURCE_BACKED_PRODUCT_ONLY", "tau_clock/X_Q normalization and WEP/R10 projections missing"),
    ]
    rows = []
    for audit_id, item, current_evidence, status, missing in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "audit_id": audit_id,
                "item": item,
                "current_evidence": current_evidence,
                "status": status,
                "missing_for_claim": missing,
                "valid_for_claim": "false",
            }
        )
    return rows


def priority_rows(timestamp):
    specs = [
        ("CBP3805_0_epsilon_ZEM_XQ", "epsilon_ZEM_XQ", "highest", "f(X_Q)F2 is the sharpest legal counterexample and feeds alpha/clocks/WEP/R10", "no-F2/operator-domain theorem or beta_Z/lambda/b_alpha product chain", "clock product row exists for b_alpha*tau only; standalone and cross-arena projections missing"),
        ("CBP3805_1_epsilon_theta_XQ", "epsilon_theta_XQ", "high", "masses/material/clock/source markers can re-enter after metric descent", "constant/material/source-marker superselection or sensitivity matrix", "WEP/clock anchors exist but MTS coefficients missing"),
        ("CBP3805_2_epsilon_source_XQ", "epsilon_source_XQ", "high", "source weights can change active source without obvious matter EOM change", "no-source-weight object language or source-action derivative bound", "WEP/source normalization bound interface exists, coefficient missing"),
        ("CBP3805_3_epsilon_kappa_XQ", "epsilon_kappa_XQ", "medium", "kappa(X_Q) is a direct local GR/Newton calibration leak", "global/superselected kappa theorem or Gdot/PPN bound", "Gdot anchor exists but X_Q derivative missing"),
        ("CBP3805_4_epsilon_boundary_XQ", "epsilon_boundary_XQ", "medium", "boundary weights can defeat local source/domain closure", "no-flux theorem or finite boundary flux source", "domain map exists, component bound missing"),
    ]
    rows = []
    for priority_id, symbol, priority, rationale, required, current_status in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "priority_id": priority_id,
                "symbol": symbol,
                "priority": priority,
                "rationale": rationale,
                "required_source_or_zero": required,
                "current_status": current_status,
                "valid_for_claim": "false",
                "blocks_claim": "true",
            }
        )
    return rows


def alpha_product_rows(timestamp):
    rows = []
    if C_1051_B_ALPHA.exists():
        for source in load_csv(C_1051_B_ALPHA):
            if source.get("chain_id") == "BAP1051_2_best_current_product":
                rows.append(
                    {
                        "timestamp_utc": timestamp,
                        "branch_id": BRANCH,
                        "checkpoint_id": CHECKPOINT,
                        "import_id": "BAP3805_0_import_1051_best_balpha_tau",
                        "source_chain_id": source["chain_id"],
                        "clock_pair": source["clock_pair"],
                        "product_bound_1sigma_yr_inv": source["product_bound_1sigma_yr_inv"],
                        "product_bound_2sigma_yr_inv": source["product_bound_2sigma_yr_inv"],
                        "formula": source["formula"],
                        "usable_component": "b_alpha*tau_clock_time",
                        "feeds": "epsilon_ZEM_XQ;epsilon_theta_XQ;clock",
                        "standalone_balpha_ready": "false",
                        "missing_for_promotion": source.get("missing_for_standalone", "derive tau_clock_time from MTS local state"),
                        "valid_for_claim": "false",
                    }
                )
    if not rows:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "import_id": "BAP3805_0_import_1051_best_balpha_tau",
                "source_chain_id": "MISSING_BAP1051_2",
                "clock_pair": "MISSING",
                "product_bound_1sigma_yr_inv": "MISSING",
                "product_bound_2sigma_yr_inv": "MISSING",
                "formula": "MISSING",
                "usable_component": "b_alpha*tau_clock_time",
                "feeds": "epsilon_ZEM_XQ;epsilon_theta_XQ;clock",
                "standalone_balpha_ready": "false",
                "missing_for_promotion": "MISSING_SOURCE_ROW",
                "valid_for_claim": "false",
            }
        )
    return rows


def refusal_rows(timestamp):
    specs = [
        ("REF3805_0_sequester_claim", "no-X_Q visible coefficient theorem", "REFUSED_CURRENT_CLAIM", "q_X exposes X_Q; typed subquotient rule and radiative/readout closure not signed"),
        ("REF3805_1_ZEM_zero", "epsilon_ZEM_XQ=0", "REFUSED_CURRENT_CLAIM", "f(X_Q)F2/lambda_A counterexample remains legal"),
        ("REF3805_2_theta_zero", "epsilon_theta_XQ=0", "REFUSED_CURRENT_CLAIM", "m_A(X_Q), clock markers, material/source labels remain legal"),
        ("REF3805_3_source_zero", "epsilon_source_XQ=0", "REFUSED_CURRENT_CLAIM", "source weights and direct source derivative certificate unsigned"),
        ("REF3805_4_balpha_standalone", "standalone b_alpha bound", "REFUSED_PROMOTION", "clock data bound b_alpha*tau_clock_time only; tau_clock/X_Q normalization missing"),
    ]
    rows = []
    for refusal_id, object_name, refusal_status, failure_reasons in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "refusal_id": refusal_id,
                "object": object_name,
                "refusal_status": refusal_status,
                "failure_reasons": failure_reasons,
                "score_eligible": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            }
        )
    return rows


def gate_rows(timestamp, grouped):
    sources_ok = all(row["exists"] == "true" for row in grouped["sources"])
    needles_ok = all(row["needle_found"] == "true" for row in grouped["sources"])
    priorities_ok = all(row["valid_for_claim"] == "false" and row["blocks_claim"] == "true" for row in grouped["priorities"])
    alpha_product_present = any(row["product_bound_1sigma_yr_inv"] == "2.1e-18" for row in grouped["alpha_product"])
    specs = [
        ("CG3805_0_sources", sources_ok and needles_ok, "all source paths and needles found"),
        ("CG3805_1_conditional_sequester", True, "typed subquotient sequester theorem emitted"),
        ("CG3805_2_qX_counterexample", True, "q_X visibility counterexample emitted"),
        ("CG3805_3_current_sequester_signed", False, "typed coefficient subquotient and radiative/readout closure not parent-signed"),
        ("CG3805_4_component_priorities", priorities_ok, "component-bound priority rows emitted as blockers"),
        ("CG3805_5_balpha_product_import", alpha_product_present, "best 2.1e-18 yr^-1 b_alpha*tau product imported as nonclaim"),
        ("CG3805_6_balpha_standalone", False, "standalone b_alpha and WEP/R10 transfer remain blocked"),
        ("CG3805_7_local_GR_claim", False, "no local-GR/Newton/EM/PPN/R10/clock/orbital claim allowed"),
    ]
    rows = []
    for gate_id, passed, details in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "gate_id": gate_id,
                "pass": bool_text(passed),
                "claim_allowed": "false",
                "details": details,
                "valid_for_claim": "false",
            }
        )
    return rows


def decision_rows(timestamp):
    specs = [
        ("DEC3805_0_derivation_result", "The sequester theorem is exact only as a typed subquotient action rule.", "Because X_Q is part of q_X, f(X_Q) is q_X-basic and legal unless coefficient functors are forbidden from reading X_Q.", "Do not rely on quotient closure; derive an action-level coefficient subquotient clause."),
        ("DEC3805_1_current_failure", "Strict-current no-X_Q visible coefficient zero is rejected.", "The current corpus has conditional product-functor/no-mixed theorem shapes but no signed parent sequester or radiative/readout closure.", "Keep epsilon_ZEM_XQ, epsilon_theta_XQ, and epsilon_source_XQ live."),
        ("DEC3805_2_first_bound_progress", "A source-backed nonclaim clock product bound is retained.", "The 1051/988 chain gives |b_alpha*tau_clock_time| <= 2.1e-18 yr^-1, but not standalone b_alpha or R10/WEP transfer.", "Use it only after tau_clock/X_Q normalization or as a bound-side prior row."),
        ("DEC3805_3_best_next", "Next target should write the q_X coefficient-subquotient action clause or normalize the alpha product chain.", "This is the constructive fork: either parent action forbids X_Q visible coefficients, or the first component bound must be promoted carefully.", "Move to 3806 qX coefficient subquotient action clause or b_alpha tau normalization."),
    ]
    rows = []
    for decision_id, decision, rationale, action in specs:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "decision_id": decision_id,
                "decision": decision,
                "rationale": rationale,
                "action": action,
                "valid_for_claim": "false",
            }
        )
    return rows


def next_target_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_doc": "3806-Y5-R2FR-qX-coefficient-subquotient-action-clause-or-balpha-tau-normalization.md",
            "target_script": "scripts/Y5_R2FR_3806_qX_coefficient_subquotient_action_clause_or_balpha_tau_normalization.py",
            "objective": "Try to write a parent action clause in which visible coefficient functors factor through pi_obs(q_X)=q_obs while only B_Q reads X_Q; if not parent-signable, normalize the imported b_alpha*tau_clock_time product by deriving tau_clock/X_Q or keep it as a nonclaim component-bound row.",
            "avoid": "do not use q_X-basicness itself as evidence that f(X_Q) visible coefficients are absent",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_TYPED_SEQUESTER_THEOREM_REJECTS_STRICT_CURRENT_AND_IMPORTS_B_ALPHA_PRODUCT",
            "headline": "No-X_Q visible-coefficient sequester is exact only if coefficient functors factor through pi_obs(q_X); q_X-basicness alone fails, and the best current numeric input is a nonclaim b_alpha*tau_clock product bound.",
            "claim_allowed": "false",
            "next_target": "3806 qX coefficient subquotient action clause or b_alpha tau normalization",
        }
    ]


def validation_rows(timestamp, grouped):
    sources_ok = all(row["exists"] == "true" for row in grouped["sources"])
    needles_ok = all(row["needle_found"] == "true" for row in grouped["sources"])
    csv_ok = all(csv_parses(path) for key, path in OUTPUTS.items() if key != "validation")
    theorem_text = "\n".join(row["mathematical_form"] for row in grouped["theorem"])
    counter_text = "\n".join(row["visible_coefficient_vertex"] for row in grouped["counterexamples"])
    priorities_ok = all(row["valid_for_claim"] == "false" and row["blocks_claim"] == "true" for row in grouped["priorities"])
    alpha_product_nonclaim = any(row["product_bound_1sigma_yr_inv"] == "2.1e-18" and row["standalone_balpha_ready"] == "false" for row in grouped["alpha_product"])
    refusals_closed = all(row["claim_allowed"] == "false" for row in grouped["refusal"])
    gates_closed = all(row["claim_allowed"] == "false" for row in grouped["gates"])
    fwb_patterns = ("*Y5_R2FR_3805*", "*3805-Y5*", "*P8_Y5*3805*")
    fwb_hits = []
    if FWB.exists():
        for pattern in fwb_patterns:
            fwb_hits.extend(FWB.rglob(pattern))
    fwb_clean = not fwb_hits
    pycache_clean = not (PCW / "scripts" / "__pycache__").exists()
    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    script_text = read_text(SCRIPT_PATH) if SCRIPT_PATH.exists() else ""
    mojibake_c2 = chr(0x00C2)
    replacement_char = chr(0xFFFD)
    bad_chars_clean = mojibake_c2 not in doc_text + script_text and replacement_char not in doc_text + script_text
    checks = [
        ("sources_exist", sources_ok, "every cited source path exists"),
        ("needles_found", needles_ok, "every cited source needle was found"),
        ("csv_outputs_parse", csv_ok, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3805 markdown document written"),
        ("typed_subquotient_present", "pi_obs(q_X)" in theorem_text and "only allowed X_Q morphism" in theorem_text, "typed coefficient subquotient theorem emitted"),
        ("qX_counterexample_present", "f(X_Q)" in theorem_text and "f(X_Q)F_obs^2" in counter_text, "q_X visibility counterexample emitted"),
        ("component_priorities_nonclaim", priorities_ok, "component-bound priority rows remain blockers"),
        ("alpha_product_import_nonclaim", alpha_product_nonclaim, "2.1e-18 b_alpha*tau product imported as nonclaim"),
        ("refusals_closed", refusals_closed, "refusal runner keeps claims closed"),
        ("claims_closed", gates_closed, "no claim gate allows a claim"),
        ("formalization_clean", fwb_clean, "no 3805 files written under formalization-workbench"),
        ("pycache_removed", pycache_clean, "scripts __pycache__ removed"),
        ("bad_chars_clean", bad_chars_clean, "new doc/script contain no mojibake replacement characters"),
    ]
    rows = []
    for check_id, passed, detail in checks:
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "check_id": check_id,
                "result": "PASS" if passed else "FAIL",
                "detail": detail,
            }
        )
    return rows


def row_bullet(row, key_fields):
    label = " ".join(f"`{row[field]}`" for field in key_fields if field in row and row[field])
    rest = "; ".join(
        f"{key}: {value}"
        for key, value in row.items()
        if key not in key_fields and key not in {"timestamp_utc", "branch_id", "checkpoint_id"}
    )
    return f"- {label}: {rest}"


def write_markdown(grouped):
    lines = [
        "# 3805 - No-XQ Visible-Coefficient Sequester Theorem or Component Bound Acquisition",
        "",
        "## Status",
        "",
        "`PASS_NONCLAIM_TYPED_SEQUESTER_THEOREM_REJECTS_STRICT_CURRENT_AND_IMPORTS_B_ALPHA_PRODUCT`.",
        "",
        "3805 tries the proof. The important result is brutal but useful: because `X_Q` is part of `q_X`, any smooth `f(X_Q)` is already `q_X`-basic. So ordinary q_X ownership does **not** forbid visible coefficients like `f(X_Q)F^2`, `m_A(X_Q)`, `kappa(X_Q)`, source weights, clock markers, or boundary weights.",
        "",
        "The exact clean route is stronger:",
        "",
        "`Coeff_vis` must factor through `pi_obs(q_X)=q_obs` and fixed representation data, while the only allowed `X_Q` path into visible physics is `X_Q -> Y_Q -> B_Q -> A_Q,F_Q`.",
        "",
        "That typed subquotient theorem would kill the visible-coefficient leakage by chain rule. The current corpus does not parent-sign it, so strict-current sequester is rejected and component-bound acquisition stays live.",
        "",
        "## Result In Plain Terms",
        "",
        "This is a real step, not a circle: the obstacle is no longer just 'coupling missing'. It is specifically that `q_X` makes `X_Q` visible for the EM geometry, so the parent action must also say visible coefficients are **not** allowed to read that visibility.",
        "",
        "The first useful bound-side progress is retained: `|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1` from the imported clock product chain. It is not standalone `b_alpha`, and it is not a WEP/R10/local-GR claim.",
        "",
        "## Compact Result",
        "",
        "`q_X`-basic does not mean locally safe.",
        "",
        "Sequestering requires a typed coefficient subquotient: coefficients see `q_obs`, not full `q_X`.",
        "",
        "`f(X_Q)F^2` is the decisive counterexample unless parent-forbidden.",
        "",
        "The best current numeric component is only the nonclaim `b_alpha*tau_clock_time` product bound.",
        "",
    ]
    sections = [
        ("Source Register", "sources", ["source_id"]),
        ("Sequester Theorem Attempt", "theorem", ["theorem_id", "claim_piece"]),
        ("Visible-Coefficient Counterexamples", "counterexamples", ["counterexample_id", "visible_coefficient_vertex"]),
        ("Current Corpus Sequester Audit", "audit", ["audit_id", "item"]),
        ("Component Bound Acquisition Priority", "priorities", ["priority_id", "symbol"]),
        ("b_alpha Product Import Nonclaim", "alpha_product", ["import_id", "usable_component"]),
        ("Sequester Refusal Runner", "refusal", ["refusal_id", "object"]),
        ("Claim Gates", "gates", ["gate_id"]),
        ("Decisions", "decisions", ["decision_id"]),
        ("Next Target", "next_target", ["target_doc"]),
        ("Validation", "validation", ["check_id", "result"]),
    ]
    for title, key, key_fields in sections:
        lines.append(f"## {title}")
        for row in grouped[key]:
            lines.append(row_bullet(row, key_fields))
    DOC_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def cleanup_pycache():
    pycache = PCW / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def main():
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    grouped = {
        "sources": source_register(timestamp),
        "theorem": theorem_rows(timestamp),
        "counterexamples": counterexample_rows(timestamp),
        "audit": audit_rows(timestamp),
        "priorities": priority_rows(timestamp),
        "alpha_product": alpha_product_rows(timestamp),
        "refusal": refusal_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["gates"] = gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["theorem"], grouped["theorem"])
    write_csv(OUTPUTS["counterexamples"], grouped["counterexamples"])
    write_csv(OUTPUTS["audit"], grouped["audit"])
    write_csv(OUTPUTS["priorities"], grouped["priorities"])
    write_csv(OUTPUTS["alpha_product"], grouped["alpha_product"])
    write_csv(OUTPUTS["refusal"], grouped["refusal"])
    write_csv(OUTPUTS["gates"], grouped["gates"])
    write_csv(OUTPUTS["decisions"], grouped["decisions"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    grouped["validation"] = [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": "pending",
            "result": "PASS",
            "detail": "placeholder before final validation",
        }
    ]
    write_markdown(grouped)
    cleanup_pycache()
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    write_markdown(grouped)
    cleanup_pycache()

    failed = [row for row in grouped["validation"] if row["result"] != "PASS"]
    print(grouped["status"][0]["status"])
    print(f"wrote {DOC_PATH}")
    if failed:
        raise SystemExit(f"validation failed: {failed}")


if __name__ == "__main__":
    main()
