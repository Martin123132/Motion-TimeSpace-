import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3810"
BRANCH = "MTS_R2FR_Y5_PARENT_OWNED_ZQEFF_READOUT_DESCENT_OR_ALPHA_PRODUCT_INPUTS_3810"
ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework"
    r"\Motion-TimeSpace--main"
)
PCW = ROOT / "post-checkpoint-work"
FWB = ROOT / "formalization-workbench"
RESIDUALS = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3810-Y5-R2FR-parent-owned-ZQeff-readout-descent-contract-or-alpha-product-inputs.md"
SCRIPT_PATH = PCW / "scripts" / "Y5_R2FR_3810_parent_owned_ZQeff_readout_descent_contract_or_alpha_product_inputs.py"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3809 = PCW / "3809-Y5-R2FR-Maxwell-normalization-from-parent-inner-product-or-alpha-finite-branch.md"
P_1112 = PCW / "1112-Y5-R10-ZQeff-descent-clause-audit-or-alpha-product-runner-contract.md"
P_1113 = PCW / "1113-Y5-R10-parent-owned-readout-descent-contract-or-alpha-product-input-acquisition.md"
P_1050 = PCW / "1050-Y5-R10-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md"
P_3792 = PCW / "3792-Y5-R2FR-same-current-Ward-Hilbert-stress-owner-or-epsilonJ-bound.md"
P_1052 = PCW / "1052-Y5-R10-tau-clock-Xhat-normalization-or-alpha-WEP-R10-projection-source.md"
P_1060 = PCW / "1060-Y5-R10-alpha-product-prediction-stub-runner-and-required-inputs.md"
P_967 = RESIDUALS / "P8_Y5_R10_967_READOUT_SCHEMA_THEOREM_ATTEMPT.csv"
P_1111_TERMS = RESIDUALS / "P8_Y5_R10_1111_ZQEFF_TERM_AUDIT.csv"
P_1099_EXCLUSION = RESIDUALS / "P8_Y5_R10_1099_NO_EXTRA_F2_EXCLUSION_AUDIT.csv"
P_1060_REQUIRED = RESIDUALS / "P8_Y5_R10_1060_REQUIRED_INPUTS.csv"
P_1060_SCHEMA = RESIDUALS / "P8_Y5_R10_1060_PRODUCT_PREDICTION_SCHEMA.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3810_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3810_PARENT_OWNED_ZQEFF_READOUT_THEOREM.csv",
    "contract": RESIDUALS / "P8_Y5_R2FR_3810_PARENT_OWNED_ZQEFF_READOUT_CONTRACT.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_3810_CONTRACT_CLAUSE_AUDIT.csv",
    "products": RESIDUALS / "P8_Y5_R2FR_3810_ALPHA_PRODUCT_INPUT_ACQUISITION.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_3810_STRICT_PRODUCT_RUNNER_CONTRACT.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3810_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3810_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3810_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3810_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3810_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3810_0_3809", P_3809, "MNT3809_4_ZQeff_descent", "3809 effective Maxwell normalization descent theorem"),
    ("SRC3810_1_1112", P_1112, "CLAUSE1112_1_parent_norm_descent", "1112 Z_Q_eff descent clause audit"),
    ("SRC3810_2_1113", P_1113, "POC1113_4_no_hidden_visible_morphisms", "1113 parent-owned readout contract prototype"),
    ("SRC3810_3_1050", P_1050, "PFT1050_3_radiative_readout_closure", "1050 visible-hidden product functor and radiative/readout blocker"),
    ("SRC3810_4_3792", P_3792, "SCW3792_1_same_current_definition", "3792 same-current Ward/Hilbert source owner"),
    ("SRC3810_5_1052", P_1052, "TCN1052_4_verdict", "1052 clock product is not standalone b_alpha"),
    ("SRC3810_6_1060_doc", P_1060, "REQ1060_3_R10_alpha", "1060 alpha product runner required inputs"),
    ("SRC3810_7_967_readout", P_967, "RAV967_5_verdict", "967 readout schema theorem attempt"),
    ("SRC3810_8_1111_terms", P_1111_TERMS, "ZQ1111_4_readout", "1111 Z_Q_eff term audit"),
    ("SRC3810_9_1099_exclusion", P_1099_EXCLUSION, "EXC1099_5_radiative", "1099 no-extra-F2 exclusion audit"),
    ("SRC3810_10_1060_required", P_1060_REQUIRED, "REQ1060_3_R10_alpha", "1060 required alpha product inputs"),
    ("SRC3810_11_1060_schema", P_1060_SCHEMA, "product_value", "1060 strict product prediction schema"),
    ("SRC3810_12_spine", SPINE_PATH, "3810-Y5-R2FR-parent-owned-ZQeff-readout-descent-contract-or-alpha-product-inputs.md", "live spine handoff from 3809"),
]


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path):
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def bool_text(value):
    return str(bool(value)).lower()


def source_rows(timestamp):
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def theorem_rows(timestamp):
    rows = [
        (
            "ZRT3810_0_descent_readout_theorem",
            "parent-owned Z_Q_eff and alpha readout descent",
            "Let q_obs: P -> O be the observed quotient, v in ker(Dq_obs), and theta_rep, mu_rep fixed representation/readout-scale data. If Z_Q_eff(Phi)=Zbar(q_obs(Phi),theta_rep,mu_rep) with Z_Q_eff>0 and alpha_read(Phi)=Abar(q_obs(Phi),theta_rep,mu_rep,Zbar), then D_v ln Z_Q_eff=0 and D_v ln alpha_read=0.",
            "EXACT_CONDITIONAL_CHAIN_RULE_THEOREM",
            "D_v ln Z_Q_eff = D ln Zbar[Dq_obs(v),Dtheta(v),Dmu(v)]/Zbar = 0. The readout derivative vanishes by the same factorisation. No cancellation or fitting is used.",
            "This is the clean theorem-zero route for local alpha drift and readout drift.",
            "parent-owned q_obs; fixed theta/mu; full Z_Q_eff factorisation; readout factorisation",
        ),
        (
            "ZRT3810_1_same_current_extension",
            "source/current readout must be the same branch",
            "If S_src descends through q_obs and J_Q is obtained by varying that same descended action with respect to A_Q before readout, then source alpha coefficients cannot be introduced as separate readout-only couplings.",
            "EXACT_CONDITIONAL_VARIATIONAL_EXTENSION",
            "A single action gives one Maxwell source current and one Hilbert stress owner; a separate source-only normalisation would define a different branch.",
            "This is what prevents WEP/R10 alpha products from being silently imported from the clock branch.",
            "single descended total source action; same A_Q/g_obs/coframe variation; boundary/domain silence",
        ),
        (
            "ZRT3810_2_radiative_naturality_extension",
            "effective action and spectroscopy reduction must be natural on quotient objects",
            "If RG/matching/readout maps are natural transformations on the quotient category, then renormalized Z_Q_eff^eff and alpha spectra still factor through q_obs and fixed representation data.",
            "EXACT_CONDITIONAL_EFT_EXTENSION",
            "A quotient-only input to a natural functor cannot acquire hidden representative dependence; any non-natural threshold/readout term is a retained residual, not a theorem-zero.",
            "This blocks the common cheat where a clean bare action is used while loop/readout terms reopen alpha drift.",
            "radiative closure; threshold-source ownership; clock/material spectroscopy readout factorisation",
        ),
        (
            "ZRT3810_3_no_free_absolute_alpha",
            "absolute alpha is not predicted by the descent theorem",
            "The theorem zeros D_v ln alpha_read. It does not determine the universal measured value of alpha unless C_P, N_Q, lambda_A, current normalisation, hbar*c convention, and readout convention are all parent-fixed.",
            "EXACT_SCOPE_GUARD",
            "A universal constant can be calibrated without local drift. A value prediction needs more parent data than a drift-zero theorem.",
            "Keeps the branch serious: local tests can close before absolute alpha is derived, but cannot be advertised as alpha prediction.",
            "parent value of C_P N_Q; no/fixed lambda_A; current/readout convention; spectrum/hbar*c descent",
        ),
        (
            "ZRT3810_4_strict_current_verdict",
            "contract written but not strict-current signed",
            "The sufficient contract is now exact, but the current corpus does not sign parent norm descent, no hidden-visible coefficient morphisms, radiative/readout naturality, same-current total source ownership, or arena projection maps.",
            "PASS_NONCLAIM_CONTRACT_DERIVED_NOT_SIGNED",
            "The proof is real; the missing signatures are not cosmetic. Adopting them without derivation would be a closure axiom.",
            "Therefore local alpha/WEP/R10/clock claims stay closed; finite product acquisition remains the fallback.",
            "MISSING_PARENT_NORM;MISSING_NO_HIDDEN_VISIBLE_COEFF;MISSING_RADIOUT_CLOSURE;MISSING_SAME_CURRENT;MISSING_ARENA_PRODUCTS",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "formal_statement": statement,
            "status": status,
            "proof_or_reason": proof,
            "consequence": consequence,
            "missing_for_claim": missing,
            "valid_for_claim": "false",
        }
        for theorem_id, claim_piece, statement, status, proof, consequence, missing in rows
    ]


def contract_rows(timestamp):
    rows = [
        (
            "POC3810_0_parent_domain",
            "parent/readout domain separation",
            "Conf_parent contains dynamical parent fields and representation labels only; clock/spectrum/material readouts are maps on solutions, not variational arguments.",
            "prevents readout-selected Euler-Lagrange forces",
            "CONDITIONAL_SCHEMA_SUPPORTED_BY_967_NOT_GLOBAL",
            "readout variables can re-enter as parent forces or new EFT branches",
            "derive Conf_parent exclusion in the parent action, not only in the audit grammar",
        ),
        (
            "POC3810_1_quotient_vertical",
            "observed quotient and vertical generator",
            "q_obs is the physical observed quotient and local hidden variations satisfy v in ker(Dq_obs).",
            "makes the chain-rule zero theorem applicable",
            "CANDIDATE_ROUTE_NOT_FULLY_PARENT_SIGNED",
            "the vertical direction being silenced may not be the physical local residual",
            "keep q_obs kernel-null/source/readout certificates live",
        ),
        (
            "POC3810_2_parent_norm_descent",
            "C_P N_Q is quotient/representation owned",
            "The parent Maxwell inner-product coefficient obeys C_P N_Q=Zbar_parent(q_obs,theta_rep) with fixed nonrescalable generator norm.",
            "zeros the parent Maxwell normalization drift",
            "UNSIGNED_CRITICAL",
            "the parent norm itself can generate b_alpha",
            "hunt for parent-fixed T_Q, fibre norm, level/index, or charge-lattice normalisation",
        ),
        (
            "POC3810_3_no_hidden_visible_coefficients",
            "no hidden-to-visible coefficient morphisms",
            "Hom(C_hid,Coeff_vis) is constant/absent; forbidden visible slots include Z_EM, masses, source weights, kappa, clock markers, boundary weights, and readout coefficients.",
            "forbids f_hid(I_hid)F_Q^2 and related mass/source leaks",
            "UNSIGNED_CRITICAL",
            "q_X-basic local scalars can legally feed visible coefficients",
            "try a true object-language/type proof; otherwise source finite coefficient rows",
        ),
        (
            "POC3810_4_radiative_naturality",
            "effective/running action descends",
            "RG, matching, threshold, and counterterm maps act on quotient-owned visible objects and fixed representation data only.",
            "keeps tree-level zeros from reopening after EFT reduction",
            "UNSIGNED_CRITICAL",
            "loop or threshold terms can regenerate alpha drift",
            "derive naturality of the effective readout functor or bound counterterm products",
        ),
        (
            "POC3810_5_readout_closure",
            "clock/spectrum/material readouts descend",
            "Observed alpha, transition frequencies, material response, and apparatus maps factor through q_obs, theta_rep, and the same Z_Q_eff branch after variation.",
            "turns abstract Z_EM silence into observed alpha/readout silence",
            "UNSIGNED_CRITICAL",
            "spectroscopy or material response can carry representative dependence",
            "derive readout functor or keep clock/WEP/R10 products nonclaim",
        ),
        (
            "POC3810_6_same_current_owner",
            "one source action owns J_Q and stress",
            "Charged matter, EM, binding, apparatus, interactions, and boundary bookkeeping are varied in one q_obs-descended total source action using the same A_Q and observed coframe.",
            "prevents source-only alpha or Poynting/Hilbert mismatch channels",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "WEP/R10 source weights and EM stress leakage remain live",
            "derive the total source action or source epsilon_J/beta_source products",
        ),
        (
            "POC3810_7_arena_projection_maps",
            "clock/WEP/R10 products are same-branch functors",
            "P_clock, P_WEP, and P_R10 either vanish by the same theorem-zero branch or are computed as finite products with sourced tau, beta, K_X, lambda, and tail inputs.",
            "prevents transferring a clock bound into WEP/R10 by hand",
            "MISSING_NUMERIC_OR_THEOREM_INPUTS",
            "each arena remains an unscored placeholder",
            "fill one full finite product row or derive the common readout functor",
        ),
        (
            "POC3810_8_no_closure_credit",
            "closure axiom guard",
            "If POC3810_0 through POC3810_7 are adopted without a parent derivation, the result is a closure branch, not a derived MTS local-GR pass.",
            "protects the programme from smuggling in the answer",
            "CLAIM_GUARD_ACTIVE",
            "the theory would merely assume the hard coupling theorem",
            "label closure explicitly or keep deriving/source-bounding",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "clause_id": clause_id,
            "clause": clause,
            "formal_requirement": requirement,
            "proof_role": proof_role,
            "current_signature": signature,
            "failure_if_unsigned": failure,
            "next_action": action,
            "valid_for_claim": "false",
        }
        for clause_id, clause, requirement, proof_role, signature, failure, action in rows
    ]


def audit_rows(timestamp):
    rows = [
        (
            "AUD3810_0_theorem_exists",
            "Can a clean local alpha/readout zero theorem be written?",
            "YES_CONDITIONAL",
            "ZRT3810_0 gives the exact chain-rule theorem on the finite positive branch.",
            "not enough for claim without clause signatures",
        ),
        (
            "AUD3810_1_parent_norm",
            "Is C_P N_Q parent-fixed and vertically silent in the strict corpus?",
            "NO_UNSIGNED",
            "3809 gives the candidate subblock but not the fixed generator norm/coefficient owner.",
            "retain b_alpha parent-norm term",
        ),
        (
            "AUD3810_2_hidden_visible",
            "Are hidden-to-visible coefficient morphisms forbidden?",
            "NO_UNSIGNED_CRITICAL",
            "1050/1099 keep f_X F_Q^2 legal unless a stronger object-language proof is signed.",
            "this is the coupling throat",
        ),
        (
            "AUD3810_3_radiative",
            "Does EFT/running/readout preserve descent?",
            "NO_UNSIGNED_CRITICAL",
            "Tree-level quotient pullback is insufficient without naturality of loops and reductions.",
            "retain counterterm/product branch",
        ),
        (
            "AUD3810_4_readout",
            "Does observed alpha/spectroscopy factor through the same quotient branch?",
            "NO_UNSIGNED",
            "967/1113 support the domain schema but not a global parent-signed readout functor.",
            "retain clock/material/readout products",
        ),
        (
            "AUD3810_5_same_current",
            "Is the source/current/stress branch single-owned?",
            "NO_CONDITIONAL_ONLY",
            "3792 proves the variational identity if the single total source action exists.",
            "retain epsilon_J and beta_source rows",
        ),
        (
            "AUD3810_6_product_fallback",
            "Can the finite alpha products be scored today?",
            "NO_PLACEHOLDER_ONLY",
            "1060 runner schema exists, but MTS numerator/projection rows are missing.",
            "valid_for_claim remains false for every row",
        ),
        (
            "AUD3810_7_best_next",
            "Which route moves the project forward most?",
            "DERIVE_COUPLING_MORPHISM_FIRST",
            "A no-hidden-visible coefficient theorem would collapse alpha, mass, source, clock, and kappa leakage at once.",
            "next target is parent signature for the coupling morphism or one real product row",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "audit_id": audit_id,
            "question": question,
            "answer": answer,
            "reason": reason,
            "consequence": consequence,
            "valid_for_claim": "false",
        }
        for audit_id, question, answer, reason, consequence in rows
    ]


def product_rows(timestamp):
    rows = [
        (
            "API3810_0_clock",
            "clock",
            "P_clock_alpha=b_alpha*tau_clock_time or direct theorem-zero",
            "b_alpha theorem-zero or numeric counterterm; tau_clock_time or direct product; clock readout map",
            "clock bound 2.1e-18 yr^-1 exists from 1052; MTS product missing",
            "MISSING_MTS_CLOCK_PRODUCT",
            "yr^-1",
            "false",
        ),
        (
            "API3810_1_WEP_alpha",
            "MICROSCOPE_WEP",
            "P_WEP_alpha=beta_source_alpha*b_alpha*tau_WEP or direct theorem-zero",
            "beta_source_alpha; b_alpha or theorem-zero; tau_WEP/material map; WEP readout domain",
            "schema only; no parent source-normalisation or tau_WEP",
            "MISSING_BETA_SOURCE_ALPHA_AND_TAU_WEP",
            "dimensionless eta contribution",
            "false",
        ),
        (
            "API3810_2_WEP_surface",
            "MICROSCOPE_WEP",
            "P_WEP_surface=beta_binding*b_A*tau_WEP or direct theorem-zero",
            "binding/surface source owner; material response; tau_WEP; transfer coefficient",
            "schema only; source/binding owner not signed",
            "MISSING_BINDING_OWNER_AND_MATERIAL_MAP",
            "dimensionless eta contribution",
            "false",
        ),
        (
            "API3810_3_R10_alpha",
            "R10_short_range",
            "P_R10_alpha(lambda)=K_X^R10(lambda)*beta_s(lambda)*beta_t(lambda)*tau_R10*tail(lambda)",
            "lambda_X; Z_X; K_X^R10(lambda); beta_s; beta_t; tau_R10; epsilon_tail; claim-valid alpha_bound(lambda)",
            "required-input schema exists; MTS numerator and promoted bound curve not claim-valid",
            "MISSING_R10_FINITE_BRANCH_VECTOR",
            "dimensionless alpha(lambda) convention",
            "false",
        ),
        (
            "API3810_4_cross_arena",
            "cross_arena",
            "same Z_Q_eff/readout/current branch feeds clock, WEP, and R10",
            "global readout functor; same-current owner; arena classifiers; no clock-to-WEP shortcut",
            "contract written but not signed",
            "MISSING_CROSS_ARENA_PARENT_MAP",
            "dimensionless consistency",
            "false",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "input_id": input_id,
            "arena": arena,
            "product_symbol": symbol,
            "required_inputs": required,
            "currently_available": available,
            "missing_status": missing,
            "units": units,
            "valid_for_claim": valid,
        }
        for input_id, arena, symbol, required, available, missing, units, valid in rows
    ]


def runner_rows(timestamp):
    rows = [
        (
            "SPRC3810_0_no_symbolic_predictions",
            "product_value must be numeric or theorem_zero; symbolic products are not score rows",
            "MISSING_NUMERIC_PRODUCT",
            "runner refuses placeholder MTS rows",
        ),
        (
            "SPRC3810_1_no_bound_division",
            "bounds may not be divided by guessed tau, beta_source, K_X, or lambda factors",
            "MISSING_PROJECTION_FACTOR",
            "clock bounds do not become WEP/R10 predictions",
        ),
        (
            "SPRC3810_2_same_branch_required",
            "cross-arena comparisons require the same Z_Q_eff/current/readout branch id",
            "MISSING_CROSS_ARENA_BRANCH",
            "prevents mixing unrelated closure assumptions",
        ),
        (
            "SPRC3810_3_bound_side_claim_validity",
            "R10 alpha_bound(lambda) rows must be source-backed, numeric, unit-declared, and valid_for_claim=true before scoring",
            "MISSING_PROMOTED_BOUND_CURVE",
            "anchor-only or candidate curves remain smoke data",
        ),
        (
            "SPRC3810_4_theorem_zero_exception",
            "a row can pass without numeric product only if the theorem-zero path signs all relevant clauses for that arena",
            "MISSING_THEOREM_ZERO_SIGNATURE",
            "the descent contract is not enough unless readout/current/projection clauses are signed",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "runner_rule_id": rule_id,
            "rule": rule,
            "failure_marker": marker,
            "claim_effect": effect,
            "valid_for_claim": "false",
        }
        for rule_id, rule, marker, effect in rows
    ]


def gate_rows(timestamp, grouped):
    all_sources = all(row["exists"] == "true" and row["needle_found"] == "true" for row in grouped["sources"])
    theorem_exists = any(row["theorem_id"] == "ZRT3810_0_descent_readout_theorem" for row in grouped["theorem"])
    critical_unsigned = any("UNSIGNED_CRITICAL" in row["current_signature"] for row in grouped["contract"])
    products_nonclaim = all(row["valid_for_claim"] == "false" for row in grouped["products"])
    rows = [
        ("CG3810_0_sources", all_sources, False, "all cited source paths and needles resolve" if all_sources else "source/needle blocker"),
        ("CG3810_1_theorem_written", theorem_exists, False, "parent-owned readout/descent theorem emitted conditionally"),
        ("CG3810_2_contract_complete", True, False, "contract clauses cover parent norm, hidden-visible, radiative/readout, same-current, and arenas"),
        ("CG3810_3_critical_clauses_signed", False, False, "parent norm/no-hidden-visible/radiative/readout clauses remain unsigned"),
        ("CG3810_4_no_closure_credit", True, False, "contract cannot be counted as derived if merely adopted"),
        ("CG3810_5_product_rows_score_ready", False, False, "finite rows still contain missing MTS inputs"),
        ("CG3810_6_products_nonclaim", products_nonclaim, False, "all product acquisition rows remain valid_for_claim=false"),
        ("CG3810_7_claims_closed", critical_unsigned, False, "alpha/local-GR/WEP/R10/clock claims remain closed"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": gate_id,
            "pass": bool_text(passed),
            "claim_allowed": bool_text(claim_allowed),
            "details": details,
            "valid_for_claim": "false",
        }
        for gate_id, passed, claim_allowed, details in rows
    ]


def decision_rows(timestamp):
    rows = [
        (
            "DEC3810_0_result",
            "The Z_Q_eff/readout zero route is mathematically real.",
            "One parent-owned quotient/readout functor would zero local alpha drift, clock readout drift, and source-normalisation side channels by chain rule plus single-action variation.",
            "Preserve this as the preferred derivation route.",
        ),
        (
            "DEC3810_1_not_claim",
            "The strict corpus has not signed the hard coupling clauses.",
            "The missing pieces are exactly the visible coefficient morphism ban, parent norm owner, radiative/readout naturality, same-current total source, and arena maps.",
            "No local-GR/alpha/R10/WEP/clock claim from this checkpoint.",
        ),
        (
            "DEC3810_2_product_fallback",
            "The fallback is finite products, not symbolic placeholders.",
            "The 1060 runner already says every arena needs full numeric/source-backed product inputs or a theorem-zero certificate.",
            "If the coupling theorem fails, source one complete product row rather than circling the ledger.",
        ),
        (
            "DEC3810_3_next",
            "The best next target is the no-hidden-visible coupling morphism proof.",
            "That single clause is the bottleneck for alpha, mass, kappa, source weights, clocks, WEP, R10, and local-GR safety.",
            "Move to 3811 parent-signature hunt for the coefficient morphism, with first alpha product row as fallback.",
        ),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "decision_id": decision_id,
            "decision": decision,
            "because": because,
            "next_action": action,
            "valid_for_claim": "false",
        }
        for decision_id, decision, because, action in rows
    ]


def next_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_doc": "3811-Y5-R2FR-no-hidden-visible-coupling-morphism-signature-or-first-alpha-product-row.md",
            "target_script": "scripts/Y5_R2FR_3811_no_hidden_visible_coupling_morphism_signature_or_first_alpha_product_row.py",
            "objective": "Try to parent-sign the object-language/type theorem forbidding nonconstant hidden-to-visible coefficient morphisms for Z_EM, masses, kappa, source weights, clock markers, and readout coefficients; if it fails, source one complete finite alpha product row under the 3810 strict runner contract.",
            "avoid": "do not adopt the readout/descent contract as closure; do not claim absolute alpha; do not transfer clock bounds to WEP/R10; do not edit formalization-workbench; do not use GitHub",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp):
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_PARENT_OWNED_ZQEFF_READOUT_DESCENT_CONTRACT_DERIVED_NOT_SIGNED",
            "summary": "3810 derives the exact parent-owned Z_Q_eff/readout descent theorem and the full sufficient contract, but keeps all claims closed because parent norm, no-hidden-visible coefficient morphisms, radiative/readout naturality, same-current source ownership, and arena projection maps remain unsigned.",
            "valid_for_claim": "false",
        }
    ]


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
        "# 3810 - Parent-Owned ZQeff Readout Descent Contract Or Alpha Product Inputs",
        "",
        "## Status",
        "",
        "`PASS_NONCLAIM_PARENT_OWNED_ZQEFF_READOUT_DESCENT_CONTRACT_DERIVED_NOT_SIGNED`.",
        "",
        "3810 does the actual forward step rather than another loose missing-list: it writes the sufficient theorem and contract for local alpha/readout silence. If `Z_Q_eff` and observed alpha readout both factor through the same parent-owned quotient/readout branch, then local vertical drift vanishes by the chain rule.",
        "",
        "The theorem is useful because it tells us exactly what has to be derived from a future parent action. The bad news is also precise: parent norm ownership, hidden-visible coefficient sequester, radiative/readout naturality, same-current total source ownership, and arena projection maps are not strict-current signed.",
        "",
        "Therefore the branch is still nonclaim. We either derive the coupling morphism ban next, or we stop pretending symbolic local rows are tests and fill one complete finite alpha product row.",
        "",
    ]
    sections = [
        ("Source Register", "sources", ["source_id"]),
        ("Parent-Owned Readout Theorem", "theorem", ["theorem_id", "claim_piece"]),
        ("Contract Clauses", "contract", ["clause_id", "clause"]),
        ("Clause Audit", "audit", ["audit_id"]),
        ("Alpha Product Input Acquisition", "products", ["input_id", "arena"]),
        ("Strict Product Runner Contract", "runner", ["runner_rule_id"]),
        ("Claim Gates", "gates", ["gate_id"]),
        ("Decision Rows", "decisions", ["decision_id"]),
        ("Next Target", "next_target", ["target_doc"]),
        ("Validation", "validation", ["check_id", "result"]),
    ]
    for title, key, key_fields in sections:
        lines.append(f"## {title}")
        for row in grouped[key]:
            lines.append(row_bullet(row, key_fields))
        lines.append("")
    DOC_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def update_spine():
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    lines = text.splitlines()
    if lines and lines[0].startswith("# Local GR Coupling Spine - Current State After "):
        lines[0] = "# Local GR Coupling Spine - Current State After 3810"
        text = "\n".join(lines) + "\n"

    paragraph = (
        "`3810` writes the full parent-owned `Z_Q_eff`/readout descent contract. "
        "The exact theorem is now explicit: if `Z_Q_eff=Zbar(q_obs,theta_rep,mu_rep)` and observed alpha/readout maps factor through the same branch, then `D_v ln Z_Q_eff=0` and local alpha/readout drift vanishes for `v in ker(Dq_obs)`. "
        "This is still nonclaim because parent norm ownership, no hidden-visible coefficient morphisms, radiative/readout naturality, same-current total source ownership, and arena projection maps are not strict-current signed."
    )
    if "`3810` writes the full parent-owned `Z_Q_eff`/readout descent contract." not in text:
        marker = "`3809` folds the older alpha-normalization chain back into the current local-GR spine."
        idx = text.find(marker)
        if idx >= 0:
            next_blank = text.find("\n\n", idx)
            if next_blank >= 0:
                text = text[: next_blank + 2] + paragraph + "\n\n" + text[next_blank + 2 :]

    bullet = "- `3810 Z_Q_eff/readout contract`: alpha/readout silence follows by chain rule only if the full effective normalization, readout map, same-current source branch, and arena projections descend through the same parent-owned quotient."
    if bullet not in text:
        anchor = "- `3809 alpha two-track split`: absolute measured `alpha` is calibration unless the parent predicts `C_P N_Q` and forbids/fixes `lambda_A`; local tests are drift/product gates for `b_alpha=-D_v ln Z_Q_eff`."
        text = text.replace(anchor, anchor + "\n" + bullet)

    nonclaim = "- The 3810 parent-owned Z_Q_eff/readout contract is nonclaim for the strict current corpus; it gives the exact theorem-zero contract, but parent norm descent, no hidden-visible coefficient morphisms, radiative/readout naturality, same-current source ownership, and arena maps remain unsigned."
    if nonclaim not in text:
        anchor = "- The 3809 Maxwell-normalization theorem is nonclaim for the strict current corpus; `C_P/N_Q` descent, no-extra-`F^2`, hidden-visible sequester, radiative/readout closure, and same-current arena maps remain unsigned."
        text = text.replace(anchor, anchor + "\n" + nonclaim)

    old_target = (
        "`3810-Y5-R2FR-parent-owned-ZQeff-readout-descent-contract-or-alpha-product-inputs.md`\n\n"
        "Target: try to construct the global parent-owned readout/descent contract that makes `Z_Q_eff=Zbar(q_obs,theta_rep)` and keeps alpha readout, same current, and radiative reductions inside the same branch; if it fails, begin finite alpha product input acquisition under the strict 3809 contract.\n\n"
        "This is the best next move because 3809 shows that the parent inner-product subblock is not enough by itself. The local alpha branch closes only if the whole effective/readout normalization descends, or else the clock/WEP/R10 products need real source-backed inputs."
    )
    new_target = (
        "`3811-Y5-R2FR-no-hidden-visible-coupling-morphism-signature-or-first-alpha-product-row.md`\n\n"
        "Target: try to parent-sign the object-language/type theorem forbidding nonconstant hidden-to-visible coefficient morphisms for `Z_EM`, masses, kappa, source weights, clock markers, and readout coefficients; if it fails, source one complete finite alpha product row under the 3810 strict runner contract.\n\n"
        "This is the best next move because 3810 shows the global descent/readout contract is sufficient but unsigned. The hardest live clause is the coupling morphism ban: without it, `f(X_Q)F^2`, mass/source/clock coefficient leaks, and arena products remain legal."
    )
    if old_target in text:
        text = text.replace(old_target, new_target)

    artifacts = [
        "P8_Y5_R2FR_3810_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_3810_PARENT_OWNED_ZQEFF_READOUT_THEOREM.csv",
        "P8_Y5_R2FR_3810_PARENT_OWNED_ZQEFF_READOUT_CONTRACT.csv",
        "P8_Y5_R2FR_3810_CONTRACT_CLAUSE_AUDIT.csv",
        "P8_Y5_R2FR_3810_ALPHA_PRODUCT_INPUT_ACQUISITION.csv",
        "P8_Y5_R2FR_3810_STRICT_PRODUCT_RUNNER_CONTRACT.csv",
        "P8_Y5_R2FR_3810_CLAIM_GATES.csv",
        "P8_Y5_R2FR_3810_DECISION_ROWS.csv",
        "P8_Y5_R2FR_3810_NEXT_TARGET.csv",
        "P8_Y5_R2FR_3810_STATUS.csv",
        "P8_Y5_BRR545_3810_VALIDATION.csv",
    ]
    for artifact in artifacts:
        entry = f"- `source-intake\\mts_residuals\\{artifact}`"
        if entry not in text:
            text = text.rstrip() + "\n" + entry + "\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def cleanup_pycache():
    pycache = PCW / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(timestamp, grouped):
    for key, path in OUTPUTS.items():
        if key != "validation":
            if not path.exists():
                raise AssertionError(f"missing output {path}")
            load_csv(path)
    fwb_hits = list(FWB.rglob("*3810*")) if FWB.exists() else []
    pycache = PCW / "scripts" / "__pycache__"
    bad_chars_clean = all("\ufffd" not in read_text(path) for path in [DOC_PATH, SCRIPT_PATH, SPINE_PATH] if path.exists())
    spine_text = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    checks = [
        ("sources_exist", all(row["exists"] == "true" for row in grouped["sources"]), "every cited source path exists"),
        ("needles_found", all(row["needle_found"] == "true" for row in grouped["sources"]), "every cited source needle was found"),
        ("csv_outputs_parse", True, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3810 markdown document written"),
        ("theorem_present", any(row["theorem_id"] == "ZRT3810_0_descent_readout_theorem" for row in grouped["theorem"]), "parent-owned Z_Q_eff/readout theorem emitted"),
        ("contract_clauses_present", len(grouped["contract"]) >= 9, "full contract clause set emitted"),
        ("critical_clauses_unsigned", any("UNSIGNED_CRITICAL" in row["current_signature"] for row in grouped["contract"]), "critical unsigned clauses explicitly retained"),
        ("product_rows_nonclaim", all(row["valid_for_claim"] == "false" for row in grouped["products"]), "all finite product rows remain nonclaim"),
        ("claim_gates_closed", all(row["claim_allowed"] == "false" for row in grouped["gates"]), "no claim gate allows a claim"),
        ("spine_updated", "Current State After 3810" in spine_text and "3811-Y5-R2FR-no-hidden-visible-coupling-morphism-signature-or-first-alpha-product-row.md" in spine_text, "live spine updated to 3810 and 3811 target"),
        ("formalization_clean", not fwb_hits, "no 3810 files written under formalization-workbench"),
        ("pycache_removed", not pycache.exists(), "scripts __pycache__ removed"),
        ("bad_chars_clean", bad_chars_clean, "new doc/script/spine contain no mojibake replacement characters"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def main():
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    grouped = {
        "sources": source_rows(timestamp),
        "theorem": theorem_rows(timestamp),
        "contract": contract_rows(timestamp),
        "audit": audit_rows(timestamp),
        "products": product_rows(timestamp),
        "runner": runner_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["gates"] = gate_rows(timestamp, grouped)
    for key, path in OUTPUTS.items():
        if key != "validation":
            write_csv(path, grouped[key])
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
    update_spine()
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
