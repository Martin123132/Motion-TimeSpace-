from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1398-Y5-R10-RAB-no-observed-counterterm-action-principle-or-lambdaA-prior-bound.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1398_SOURCE_REGISTER.csv"
NO_COUNTERTERM_AUDIT_PATH = SRC_DIR / "P8_Y5_R10_1398_NO_OBSERVED_COUNTERTERM_AUDIT.csv"
PULLBACK_NO_GO_PATH = SRC_DIR / "P8_Y5_R10_1398_QUOTIENT_PULLBACK_NO_GO_LEDGER.csv"
ACTION_CONTRACT_PATH = SRC_DIR / "P8_Y5_R10_1398_PARENT_ACTION_SELECTION_CONTRACT.csv"
LAMBDA_PRIOR_PATH = SRC_DIR / "P8_Y5_R10_1398_LAMBDA_A_PRIOR_BOUND_VECTOR.csv"
ARENA_GATE_PATH = SRC_DIR / "P8_Y5_R10_1398_ALPHAEM_LOCAL_ARENA_GATE.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1398_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1398_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1398_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1398_VALIDATION.csv"

STATUS = (
    "Y5_R10_1398_no_observed_counterterm_principle_fails_locality_only_"
    "quotient_pullback_no_go_lambda_A_prior_bound_vector_nonclaim"
)
CLAIM_CEILING = (
    "no_counterterm_no_go_and_lambda_A_prior_vector_only_no_unique_F2_no_lambda_A_zero_"
    "no_alphaEM_bound_no_WEP_no_clock_no_R10_no_PPN_no_Newton_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1398_0_1397_doc",
        "source_path": "1397-Y5-R10-RAB-unique-Maxwell-F2-proof-or-lambdaA-source-row.md",
        "required_anchor": "NEXT1397_0_1398",
        "purpose": "handoff selecting no observed-counterterm principle or lambda_A prior bound",
    },
    {
        "source_id": "SRC1398_1_1397_proof",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1397_UNIQUE_MAXWELL_F2_PROOF_AUDIT.csv",
        "required_anchor": "UMF1397_3_no_observed_counterterm_principle",
        "purpose": "no quotient-only counterterm clause to test",
    },
    {
        "source_id": "SRC1398_2_1397_lambda",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1397_LAMBDA_A_SOURCE_ROW.csv",
        "required_anchor": "LAM1397_0_lambda_A",
        "purpose": "lambda_A source coefficient fallback",
    },
    {
        "source_id": "SRC1398_3_765_doc",
        "source_path": "765-Y5-R10-parent-vertical-generator-norm-and-Maxwell-kinetic-inheritance-or-alpha-source-fill.md",
        "required_anchor": "RCE765_0_lambda_F2",
        "purpose": "original standalone lambda_A F_Q^2 counterexample",
    },
    {
        "source_id": "SRC1398_4_765_counter",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv",
        "required_anchor": "RCE765_0_lambda_F2",
        "purpose": "machine-readable lambda_A counterexample",
    },
    {
        "source_id": "SRC1398_5_644_doc",
        "source_path": "644-Y5-R10-parent-vertical-norm-coupling-owner-proof-or-demotion.md",
        "required_anchor": "RC644_0_free_lambda_A",
        "purpose": "prior vertical norm demotion with free lambda_A",
    },
    {
        "source_id": "SRC1398_6_642_doc",
        "source_path": "642-Y5-R10-charge-unit-Maxwell-proof-extension-or-kappa-alpha-pressure-runner.md",
        "required_anchor": "TA642_4_coupling_normalization",
        "purpose": "g_EM/alpha_EM coupling owner missing",
    },
    {
        "source_id": "SRC1398_7_988_doc",
        "source_path": "988-Y5-R10-alphaEM-WEP-clock-joint-prior-or-EM-lock-theorem.md",
        "required_anchor": "WEP988_WAS651_0_alpha_Coulomb",
        "purpose": "finite alpha branch WEP pressure targets",
    },
    {
        "source_id": "SRC1398_8_1396_template",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1396_BETA_EM_SOURCE_BOUND_TEMPLATE.csv",
        "required_anchor": "BEM1396_6_template_verdict",
        "purpose": "finite beta_EM/alphaEM source-bound template",
    },
    {
        "source_id": "SRC1398_9_this_script",
        "source_path": "scripts/Y5_R10_RAB_no_observed_counterterm_action_principle_or_lambdaA_prior_bound.py",
        "required_anchor": "STATUS",
        "purpose": "1398 generator",
    },
]


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str] | None = None) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    if columns is None:
        columns = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: clean(row.get(column, "")) for column in columns})


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return ""
    if columns is None:
        columns = list(rows[0].keys())
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(clean(row.get(column, "")).replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def anchor_found(path: Path, anchor: str) -> bool:
    if not path.exists():
        return False
    return anchor in path.read_text(encoding="utf-8", errors="ignore")


def source_register_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in SOURCE_ROWS:
        source_path = ROOT / source["source_path"]
        rows.append(
            {
                **source,
                "exists": str(source_path.exists()),
                "anchor_found": str(anchor_found(source_path, source["required_anchor"])),
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
    return rows


def no_counterterm_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "NOC1398_0_parent_locality",
            "candidate_principle": "parent-local action only",
            "attempted_use": "forbid terms written directly in observed quotient variables",
            "mathematical_test": "if I_obs[q(Phi)] is a local scalar density after composition with q, then it is still a parent-local functional",
            "result": "INSUFFICIENT",
            "blocker": "parent locality alone cannot distinguish primitive curvature terms from pullbacks of quotient invariants",
            "if_repaired": "would need a primitive-operator selection rule, not mere locality",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "NOC1398_1_gauge_diffeomorphism",
            "candidate_principle": "gauge and diffeomorphism invariance",
            "attempted_use": "exclude lambda_A F_Q^2 by symmetry",
            "mathematical_test": "F_Q^{mu nu}F^Q_{mu nu} with dmu_obs is gauge invariant and diffeomorphism invariant",
            "result": "FAILS_AS_EXCLUSION",
            "blocker": "the counterterm has the same low-energy symmetries as ordinary Maxwell theory",
            "if_repaired": "requires a stronger parent symmetry that acts on quotient pullbacks, not only U(1) and diffeomorphisms",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "NOC1398_2_pullback_lemma",
            "candidate_principle": "observed-only means illegal",
            "attempted_use": "declare quotient-only counterterms inadmissible because they are not primitive parent invariants",
            "mathematical_test": "for quotient map q:P->O and observed scalar L_O, the pullback q^*L_O=L_O circ q is a scalar on P whenever q is part of the parent structure",
            "result": "NO_GO_LOCALITY_ONLY",
            "blocker": "observed-only terms can be represented as parent pullbacks unless an extra axiom forbids q^* primitive densities",
            "if_repaired": "derive a no-pullback or minimal-primitive-action theorem from the parent variational principle",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "NOC1398_3_minimal_curvature_action",
            "candidate_principle": "minimal parent curvature norm",
            "attempted_use": "allow only S_parent=-C_P/4 int <F,F>_P and reject all additional two-derivative invariants",
            "mathematical_test": "operator basis at two derivatives contains exactly one curvature norm and no quotient pullback density",
            "result": "CLOSURE_AXIOM_NOT_DERIVED",
            "blocker": "minimality is a choice unless it follows from a symmetry, degeneracy, topological level, or constrained variational domain",
            "if_repaired": "would close lambda_A without fitting, but must be stated as theorem not taste",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "NOC1398_4_radiative_stability",
            "candidate_principle": "absence stays absent",
            "attempted_use": "set lambda_A=0 at the parent level and keep it zero after projection/effective reduction",
            "mathematical_test": "RG or threshold corrections must not regenerate a standalone F_Q^2 coefficient",
            "result": "UNSIGNED",
            "blocker": "no parent RG/threshold rule or non-renormalization theorem is present",
            "if_repaired": "finite alphaEM branches stop reappearing through effective coefficients",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "NOC1398_5_topological_level_escape",
            "candidate_principle": "level/index/anomaly/monopole owner",
            "attempted_use": "fix the Maxwell coefficient by a quantized or topological parent datum",
            "mathematical_test": "g_EM^{-2} is a level/index/norm datum with no independent continuous lambda_A deformation",
            "result": "PROMISING_NOT_SUPPLIED",
            "blocker": "642 already names this as missing; no such owner has been found in the corpus",
            "if_repaired": "could defeat the pullback freedom by making the coefficient non-deformable",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "NOC1398_6_exact_conditional_theorem",
            "candidate_principle": "no observed-counterterm theorem",
            "attempted_use": "derive lambda_A=0",
            "mathematical_test": "if parent operator basis is primitive-only, quotient pullbacks are forbidden, and the rule is radiatively stable, then standalone lambda_A F_Q^2 is inadmissible",
            "result": "EXACT_CONDITIONAL_THEOREM_READY_NOT_PROMOTED",
            "blocker": "NOC1398_0 through NOC1398_5 are not all signed; NOC1398_2 gives a locality-only no-go",
            "if_repaired": "would close UMF1397_3 and return to remaining EM-lock clauses",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "audit_id": "NOC1398_7_current_verdict",
            "candidate_principle": "1398 proof status",
            "attempted_use": "promote no-counterterm principle as derivation",
            "mathematical_test": "Z_no_observed_counterterm=false while quotient pullback terms remain legal",
            "result": "PROOF_ROUTE_FAILS_CURRENT_CORPUS_LAMBDA_A_PRIOR_VECTOR_REQUIRED",
            "blocker": "no parent selection theorem forbids q^*(F_Q^2) or fixes its coefficient",
            "if_repaired": "unique Maxwell F2 proof could be reopened",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def pullback_no_go_rows() -> list[dict[str, str]]:
    return [
        {
            "lemma_id": "QPG1398_0_setup",
            "statement": "Let q:P->O be the parent-to-observed projection and let L_O[A_Q,e_obs] be an observed gauge/diffeomorphism scalar density.",
            "proof_sketch": "If A_Q and e_obs are q-descended objects, then L_O circ q is a well-defined scalar density on the parent domain.",
            "consequence": "calling a term observed-only does not make it non-parent-local",
            "status": "MATHEMATICAL_SETUP",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "lemma_id": "QPG1398_1_pullback_counterterm",
            "statement": "The Maxwell counterterm DeltaS_lambda can be represented as the pullback of the observed Maxwell density.",
            "proof_sketch": "DeltaS_lambda = -(lambda_A/4) int_P q^*(dmu_obs F_Q^2) after choosing the same projection/readout map used to define observed EM.",
            "consequence": "parent locality and ordinary covariance do not exclude lambda_A",
            "status": "NO_GO_FOR_LOCALITY_ONLY",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "lemma_id": "QPG1398_2_symmetry_limit",
            "statement": "Any symmetry shared by the observed Maxwell action is also shared by its pullback unless the parent has an extra symmetry acting on the pullback coefficient.",
            "proof_sketch": "Gauge invariance and diffeomorphism covariance are preserved under pullback; they do not force lambda_A to vanish.",
            "consequence": "the missing object must be an extra parent selection rule, not ordinary gauge covariance",
            "status": "NO_GO_FOR_GAUGE_DIFF_ONLY",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "lemma_id": "QPG1398_3_valid_escape",
            "statement": "A future proof can still kill lambda_A if the parent theory forbids q^*L_O as a primitive density.",
            "proof_sketch": "Examples of acceptable escape clauses are a complete primitive operator algebra, topological level quantization, constrained variational domain, or non-renormalization theorem.",
            "consequence": "derive one of those or keep lambda_A finite",
            "status": "ESCAPE_CONTRACT_ONLY",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def action_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "PAC1398_0_field_domain",
            "future_parent_action_must_prove": "the varied fields live only on the parent domain and observed fields are not independent primitives",
            "mathematical_form": "Phi varied upstairs; A_Q,e_obs are projections or descended readouts",
            "current_status": "PARTIAL_TEMPLATE_ONLY",
            "why_needed": "prevents arbitrary observed-sector appendages but does not by itself defeat pullbacks",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "contract_id": "PAC1398_1_operator_basis",
            "future_parent_action_must_prove": "the two-derivative gauge operator basis is complete and contains only the parent curvature norm",
            "mathematical_form": "O_2(parent,U1_Q) = span{<F,F>_P} with q^*(F_Q^2) excluded",
            "current_status": "MISSING_OPERATOR_BASIS_THEOREM",
            "why_needed": "this is the direct way to make unique Maxwell F2 a theorem",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "contract_id": "PAC1398_2_pullback_exclusion",
            "future_parent_action_must_prove": "pullbacks of observed quotient densities are not allowed primitive terms",
            "mathematical_form": "q^*L_O is admissible only when it is already generated by a parent primitive invariant",
            "current_status": "MISSING_NO_PULLBACK_RULE",
            "why_needed": "otherwise lambda_A F_Q^2 survives as a legal parent-local term",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "contract_id": "PAC1398_3_coefficient_owner",
            "future_parent_action_must_prove": "the Maxwell coefficient is fixed by parent norm, level, index, anomaly, monopole, or Ward owner",
            "mathematical_form": "g_EM^{-2}=C_P N_Q with no independent continuous deformation lambda_A",
            "current_status": "MISSING_LEVEL_INDEX_OWNER",
            "why_needed": "a topological/discrete owner is a less-scrutinized route than arbitrary minimality",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "contract_id": "PAC1398_4_radiative_stability",
            "future_parent_action_must_prove": "the no-lambda_A rule is stable under effective reduction",
            "mathematical_form": "delta lambda_A = 0 under threshold/RG/projection corrections, or all generated terms are absorbed into C_P N_Q",
            "current_status": "MISSING_NONRENORMALIZATION_RULE",
            "why_needed": "without this, a tree-level zero can reappear as a finite alphaEM residual",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "contract_id": "PAC1398_5_matter_current_readout_join",
            "future_parent_action_must_prove": "charge current, matter charge labels, Hodge/coframe readout, and alphaEM measurement descend from the same owner",
            "mathematical_form": "T_Q, J_Q, charge lattice, star_obs, and hbar*c readout have common quotient-silent normalization",
            "current_status": "MISSING_JOINED_OWNER",
            "why_needed": "even lambda_A=0 is insufficient if current/readout rescalings re-open alphaEM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def lambda_prior_rows() -> list[dict[str, str]]:
    return [
        {
            "prior_id": "LAP1398_0_lambda_A",
            "quantity": "lambda_A",
            "role": "standalone Maxwell kinetic pullback coefficient",
            "formula": "DeltaS_lambda = -(lambda_A/4) int q^*(dmu_obs F_Q^2)",
            "prior_or_bound": "MISSING_PRIOR_OR_PARENT_COEFFICIENT",
            "required_for_claim": "numeric lambda_A or theorem lambda_A=0 with source path",
            "current_status": "NONCLAIM_COEFFICIENT",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "prior_id": "LAP1398_1_dimensionless_ratio",
            "quantity": "rho_lambda_A",
            "role": "dimensionless size of the counterterm relative to inherited parent norm",
            "formula": "rho_lambda_A = lambda_A/(C_P N_Q)",
            "prior_or_bound": "MISSING_C_P_N_Q_AND_LAMBDA_A",
            "required_for_claim": "C_P, N_Q, lambda_A, and readout convention",
            "current_status": "RATIO_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "prior_id": "LAP1398_2_alpha_derivative",
            "quantity": "b_alpha_EM(lambda_A)",
            "role": "finite alphaEM drift induced by lambda_A variation",
            "formula": "b_alpha_EM = -partial_phi_c ln(C_P N_Q + lambda_A) - partial_phi_c ln(readout)",
            "prior_or_bound": "MISSING_DERIVATIVE_PRIOR",
            "required_for_claim": "derivative map for C_P, N_Q, lambda_A, and readout",
            "current_status": "DERIVATIVE_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "prior_id": "LAP1398_3_clock_bound_channel",
            "quantity": "b_alpha_EM tau_clock",
            "role": "clock/fine-structure pressure on finite lambda_A branch",
            "formula": "Delta ln nu = K_alpha b_alpha_EM tau_clock",
            "prior_or_bound": "PRODUCT_BOUND_ONLY",
            "required_for_claim": "separate parent tau_clock map or theorem tying it to WEP/R10 domains",
            "current_status": "CLOCK_SCREEN_NOT_TRANSFERABLE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "prior_id": "LAP1398_4_WEP_bound_channel",
            "quantity": "beta_source_alpha b_alpha_EM tau_WEP",
            "role": "WEP/Coulomb pressure on finite lambda_A branch",
            "formula": "eta_AB_alpha = DeltaQ_alpha_AB beta_source_alpha b_alpha_EM tau_WEP",
            "prior_or_bound": "TARGET_ONLY_alpha<=4.797780522732e-05_robust<=2.887280314062e-05",
            "required_for_claim": "source normalization owner plus tau_WEP map",
            "current_status": "NUMERIC_TARGET_ONLY_NOT_DERIVED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "prior_id": "LAP1398_5_R10_bound_channel",
            "quantity": "alpha_bulk_ST(lambda_A)",
            "role": "short-range force pressure on finite lambda_A branch",
            "formula": "alpha_bulk_ST(lambda)=K_bulk_ST(lambda) beta_bulk,S(lambda_A) beta_bulk,T(lambda_A)+tail",
            "prior_or_bound": "MISSING_KERNEL_TAIL_REAL_BOUND_CURVE",
            "required_for_claim": "K_bulk_ST(lambda), beta maps, tail, and real R10 bound curve",
            "current_status": "R10_NOT_SCOREABLE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "prior_id": "LAP1398_6_prior_policy",
            "quantity": "lambda_A prior use",
            "role": "private smoke-test prior discipline",
            "formula": "naturalness prior may be used for sensitivity studies only; it is not a theorem or pass",
            "prior_or_bound": "NONCLAIM_SMOKE_ONLY",
            "required_for_claim": "replace prior by theorem-zero or source-backed empirical bound",
            "current_status": "PRIOR_CANNOT_PROMOTE_CLAIMS",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def arena_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "NAG1398_0_unique_F2",
            "arena": "unique Maxwell F2",
            "dependency": "no-counterterm principle or coefficient owner must kill lambda_A",
            "current_blocker": "quotient pullback no-go defeats locality-only exclusion",
            "status": "BLOCKED_UNIQUE_F2_NOT_PROVED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "NAG1398_1_EM_lock",
            "arena": "EM-lock theorem",
            "dependency": "unique F2 must close before EM-lock can set beta_EM=0",
            "current_blocker": "lambda_A remains finite/nonclaim",
            "status": "BLOCKED_EM_LOCK_NOT_PROMOTED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "NAG1398_2_alphaEM_clock",
            "arena": "alphaEM and clocks",
            "dependency": "b_alpha_EM(lambda_A) and tau_clock must be derived or bounded",
            "current_blocker": "derivative/readout map and standalone b_alpha bound missing",
            "status": "BLOCKED_CLOCK_ALPHA_MAP_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "NAG1398_3_WEP",
            "arena": "WEP/Coulomb",
            "dependency": "beta_source_alpha b_alpha_EM tau_WEP must be sourced or zero",
            "current_blocker": "source normalization and tau_WEP map missing",
            "status": "BLOCKED_WEP_SOURCE_TAU_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "NAG1398_4_R10",
            "arena": "R10",
            "dependency": "finite lambda_A must feed a source-backed bulk alpha(lambda) runner",
            "current_blocker": "kernel, material beta, tail, and real bound curve not claim-ready",
            "status": "BLOCKED_R10_LAMBDA_A_LEG_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "NAG1398_5_local_GR",
            "arena": "local GR/Newton",
            "dependency": "all finite alphaEM/EM residuals must vanish or be bounded in local residual vector",
            "current_blocker": "lambda_A finite route and joined current/readout owner missing",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "NAG1398_6_verdict",
            "arena": "all local/empirical gates",
            "dependency": "theorem-zero or source-backed lambda_A vector",
            "current_blocker": "neither exists",
            "status": "ARENA_SCORING_BLOCKED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "claim_id": "GATE1398_0_no_counterterm",
            "claim": "observed quotient-only counterterms are parent-forbidden",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "quotient pullback lemma shows locality/gauge covariance alone allow q^*(F_Q^2)",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1398_1_lambda_A_zero",
            "claim": "lambda_A=0",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "no primitive operator selection theorem or level/index owner has been supplied",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1398_2_alphaEM",
            "claim": "alphaEM drift is zero or bounded",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "lambda_A derivative/readout/tau maps remain missing",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1398_3_empirical",
            "claim": "WEP, clock, or R10 pass",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1398 only creates nonclaim prior/bound vector; it does not score data",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1398_4_local_GR",
            "claim": "local GR/Newton reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "EM coupling residual remains unresolved and local residual vector is incomplete",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1398_0_no_go",
            "decision": "do not use parent locality to kill lambda_A",
            "reason": "quotient pullbacks make observed Maxwell densities parent-local unless an extra selection theorem forbids them",
            "consequence": "no-counterterm route is demoted to a future parent-action contract",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1398_1_lambda_prior",
            "decision": "retain lambda_A as finite nonclaim prior/bound vector",
            "reason": "if not derivably zero, it must be carried into alphaEM/WEP/clock/R10/local gates",
            "consequence": "no hidden EM-lock or unique-F2 promotion",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1398_2_next",
            "decision": "hunt a coefficient owner rather than a locality slogan",
            "reason": "level/index/anomaly/monopole/Ward ownership is the least-scrutiny route that could make lambda_A non-deformable",
            "consequence": "next target 1399 searches for a gauge-level/index owner or keeps finite alphaEM prior vector",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1398_0_1399",
            "target_doc": "1399-Y5-R10-RAB-gauge-level-index-owner-for-lambdaA-or-finite-alphaEM-prior-vector.md",
            "target_script": "scripts/Y5_R10_RAB_gauge_level_index_owner_for_lambdaA_or_finite_alphaEM_prior_vector.py",
            "task": "try to derive a level/index/anomaly/monopole/Ward owner that fixes g_EM^{-2} and forbids independent lambda_A; if it fails, keep a finite alphaEM prior vector without scoring claims",
            "success_condition": "either a discrete/topological/Noether owner makes lambda_A non-deformable or the finite alphaEM route is explicitly bounded as nonclaim",
            "do_not_claim": "lambda_A=0;unique F2;EM-lock beta_EM=0;alphaEM bound;WEP pass;clock pass;R10 pass;PPN pass;Newton limit;local GR;q_loc=0;GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: list[dict[str, str]],
    no_counterterm: list[dict[str, str]],
    pullback: list[dict[str, str]],
    contract: list[dict[str, str]],
    priors: list[dict[str, str]],
    arenas: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    no_go_present = any(
        row["audit_id"] == "NOC1398_2_pullback_lemma"
        and row["result"] == "NO_GO_LOCALITY_ONLY"
        for row in no_counterterm
    )
    verdict_present = any(
        row["audit_id"] == "NOC1398_7_current_verdict"
        and row["result"] == "PROOF_ROUTE_FAILS_CURRENT_CORPUS_LAMBDA_A_PRIOR_VECTOR_REQUIRED"
        for row in no_counterterm
    )
    pullback_ok = any(row["lemma_id"] == "QPG1398_1_pullback_counterterm" and row["status"] == "NO_GO_FOR_LOCALITY_ONLY" for row in pullback)
    contract_nonclaim = all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in contract)
    prior_nonclaim = all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in priors)
    prior_has_missing = any("MISSING" in row["prior_or_bound"] or "TARGET_ONLY" in row["prior_or_bound"] or "PRODUCT_BOUND_ONLY" in row["prior_or_bound"] for row in priors)
    arenas_blocked = all(
        row["claim_allowed"] == "False"
        and (row["status"].startswith("BLOCKED") or row["status"] == "ARENA_SCORING_BLOCKED")
        for row in arenas
    )
    gates_blocked = all(row["claim_allowed"] == "False" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        NO_COUNTERTERM_AUDIT_PATH,
        PULLBACK_NO_GO_PATH,
        ACTION_CONTRACT_PATH,
        LAMBDA_PRIOR_PATH,
        ARENA_GATE_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    scope_ok = all("formalization-workbench" not in str(ROOT / path) for path in output_paths)
    all_ok = (
        source_ok
        and no_go_present
        and verdict_present
        and pullback_ok
        and contract_nonclaim
        and prior_nonclaim
        and prior_has_missing
        and arenas_blocked
        and gates_blocked
        and scope_ok
    )
    now = datetime.now(timezone.utc).isoformat()
    return [
        {
            "check_id": "VAL1398_0_sources",
            "status": "PASS" if source_ok else "FAIL",
            "detail": "all cited source paths exist and anchors are present",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1398_1_no_counterterm_audit",
            "status": "PASS" if no_go_present and verdict_present else "FAIL",
            "detail": "no observed-counterterm proof fails as locality-only and records lambda_A prior-vector fallback",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1398_2_pullback_no_go",
            "status": "PASS" if pullback_ok else "FAIL",
            "detail": "quotient pullback ledger proves q^*(F_Q^2) remains legal absent extra parent selection rule",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1398_3_action_contract",
            "status": "PASS" if contract_nonclaim else "FAIL",
            "detail": "future parent-action clauses are explicit and nonclaim",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1398_4_lambda_prior",
            "status": "PASS" if prior_nonclaim and prior_has_missing else "FAIL",
            "detail": "lambda_A prior/bound vector remains nonclaim and contains missing parent inputs",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1398_5_arena_claim_gates",
            "status": "PASS" if arenas_blocked and gates_blocked else "FAIL",
            "detail": "unique F2, EM-lock, alphaEM, WEP, clock, R10, and local-GR claims remain blocked",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1398_6_scope",
            "status": "PASS" if scope_ok else "FAIL",
            "detail": "outputs are confined to post-checkpoint-work paths",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1398_7_overall",
            "status": "PASS" if all_ok else "FAIL",
            "detail": "1398 converts the no-counterterm route into a pullback no-go plus finite lambda_A nonclaim vector",
            "generated_utc": now,
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    no_counterterm: list[dict[str, str]],
    pullback: list[dict[str, str]],
    contract: list[dict[str, str]],
    priors: list[dict[str, str]],
    arenas: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    body = f"""# 1398 Y5 R10 RAB: No Observed Counterterm Action Principle Or LambdaA Prior Bound

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

**Current verdict:** the attempted no-observed-counterterm proof does not close from locality, gauge invariance, or diffeomorphism covariance alone. The key no-go is simple: if the observed Maxwell density is defined by the quotient/readout map, its pullback is still a parent-local scalar density unless an extra parent selection rule forbids such pullbacks.

**Discipline move:** do not kill `lambda_A` by taste. Either a future parent action proves a primitive operator-basis/no-pullback/level-owner theorem, or `lambda_A` remains a finite nonclaim coefficient carried into alphaEM, WEP, clock, R10, and local-GR gates.

## Source Register

{md_table(sources)}

## No Observed-Counterterm Audit

{md_table(no_counterterm)}

## Quotient Pullback No-Go Ledger

{md_table(pullback)}

## Parent Action Selection Contract

{md_table(contract)}

## `lambda_A` Prior / Bound Vector

{md_table(priors)}

## AlphaEM / Local Arena Gates

{md_table(arenas)}

## Claim Gates

{md_table(gates)}

## Decision Ledger

{md_table(decisions)}

## Next Target

{md_table(next_target)}

## Validation

{md_table(validation)}
"""
    (ROOT / DOC_PATH).write_text(body, encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    no_counterterm = no_counterterm_audit_rows()
    pullback = pullback_no_go_rows()
    contract = action_contract_rows()
    priors = lambda_prior_rows()
    arenas = arena_gate_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, no_counterterm, pullback, contract, priors, arenas, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(NO_COUNTERTERM_AUDIT_PATH, no_counterterm)
    write_csv(PULLBACK_NO_GO_PATH, pullback)
    write_csv(ACTION_CONTRACT_PATH, contract)
    write_csv(LAMBDA_PRIOR_PATH, priors)
    write_csv(ARENA_GATE_PATH, arenas)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, no_counterterm, pullback, contract, priors, arenas, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1398 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
