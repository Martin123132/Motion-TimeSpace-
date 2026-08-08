from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3222-Y5-R2FR-defect-norm-parent-action-contract-or-finite-alpha-coefficient-runner-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3222_INPUTS.csv"
CONTRACT = OUT / "P8_Y5_R2FR_3222_PARENT_ACTION_DEFECT_NORM_CONTRACT.csv"
CANDIDATES = OUT / "P8_Y5_R2FR_3222_RQ_CANDIDATE_ROUTES.csv"
VARIATION = OUT / "P8_Y5_R2FR_3222_VARIATION_AND_MAXWELL_LIMIT_PROOF.csv"
STRESS = OUT / "P8_Y5_R2FR_3222_STRESS_POYNTING_AND_READOUT_GUARDS.csv"
RUNNER = OUT / "P8_Y5_R2FR_3222_FINITE_ALPHA_RUNNER_SPEC.csv"
DECISION = OUT / "P8_Y5_R2FR_3222_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3222_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def resolve(location: str, relative_path: str) -> Path:
    if location == "post_checkpoint":
        return ROOT / relative_path
    if location == "mts_residuals":
        return OUT / relative_path
    if location == "formalization":
        return FW / relative_path
    raise ValueError(location)


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:190]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


SOURCES = [
    {
        "input_id": "SRC3222_00_3221_doc",
        "location": "post_checkpoint",
        "relative_path": "3221-Y5-R2FR-EM-source-root-owner-hunt-or-finite-coefficient-row-promotion-under-AX1090.md",
        "role": "defect-norm mechanism handoff",
        "terms": ["Delta Z_A", "R_Q", "DEFECT_NORM_SOURCE_ROOT", "Poynting"],
    },
    {
        "input_id": "SRC3222_01_3221_defect_csv",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3221_DEFECT_NORM_SOURCE_ROOT_THEOREM.csv",
        "role": "exact defect-norm first derivative theorem",
        "terms": ["DN3221_1_first_derivative_zero", "DN3221_2_second_variation_debt", "DN3221_5_verdict"],
    },
    {
        "input_id": "SRC3222_02_3221_phase_csv",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3221_PHASE_CURRENT_TO_EM_SOURCE_ROOT_GATE.csv",
        "role": "phase-current to defect bridge",
        "terms": ["PC3221_1_defect_bridge", "PC3221_2_no_penalty_cheat", "PC3221_3_wave_channel"],
    },
    {
        "input_id": "SRC3222_03_1055_contract",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
        "role": "single parent action contract",
        "terms": ["PAC1055_1_EM_owner", "PAC1055_5_radiative_readout_closure", "PAC1055_6_single_parent_action"],
    },
    {
        "input_id": "SRC3222_04_990_contract",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv",
        "role": "local GR/EM parent contract gates",
        "terms": ["PAC990_3_EM_lock", "PAC990_5_Ward_Bianchi", "PAC990_6_PPN_readout"],
    },
    {
        "input_id": "SRC3222_05_642_descent",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv",
        "role": "Maxwell equation and current descent attempt",
        "terms": ["MD642_1_Gauss_Ampere", "MD642_2_current_conservation", "MD642_4_alpha_constant"],
    },
    {
        "input_id": "SRC3222_06_765_mki",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv",
        "role": "Maxwell kinetic inheritance gates",
        "terms": ["MKI765_1_norm", "MKI765_2_unique_F2", "MKI765_4_readout"],
    },
    {
        "input_id": "SRC3222_07_988_emlock",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv",
        "role": "EM lock/readout descent gate",
        "terms": ["EMLOCK988_1_unique_Maxwell_F2", "EMLOCK988_3_readout_descent", "EMLOCK988_5_theorem_verdict"],
    },
    {
        "input_id": "SRC3222_08_1057_unique",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv",
        "role": "unique Maxwell subblock obstruction",
        "terms": ["UMS1057_2_no_independent_F2", "UMS1057_3_no_hidden_coefficient", "UMS1057_5_verdict"],
    },
    {
        "input_id": "SRC3222_09_1058_domain",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
        "role": "visible operator-domain exhaustion obstruction",
        "terms": ["VOE1058_2_product_functor", "VOE1058_3_no_hidden_visible_hom", "VOE1058_5_verdict"],
    },
    {
        "input_id": "SRC3222_10_1091_domain",
        "location": "post_checkpoint",
        "relative_path": "1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md",
        "role": "hidden-visible scalar obstruction",
        "terms": ["ODH1091_2_scalar_obstruction", "ODH1091_6_verdict", "FR1091_0_b_alpha"],
    },
    {
        "input_id": "SRC3222_11_459B_phase",
        "location": "post_checkpoint",
        "relative_path": "459B-Andersen-charge-amplitude-phase-current-gate.md",
        "role": "phase-current conservation clue",
        "terms": ["theta_Q", "J_Q", "Maxwell", "Lorentz"],
    },
    {
        "input_id": "SRC3222_12_287_current",
        "location": "post_checkpoint",
        "relative_path": "287-boundary-current-charge-owner-attempt.md",
        "role": "relative boundary-current conservation",
        "terms": ["d_rel J_B", "Q_B", "No promotion yet"],
    },
    {
        "input_id": "SRC3222_13_3219_hessian",
        "location": "post_checkpoint",
        "relative_path": "3219-Y5-R2FR-EM-F2-strict-double-zero-source-root-or-balpha-m-finite-bound-under-AX1090.md",
        "role": "Hessian and off-root b_alpha guard",
        "terms": ["G_eff", "HES3219_1_coercivity_floor", "ORB3219_0_balpha_offroot"],
    },
]


def build_rows(now: str) -> tuple[list[dict[str, object]], ...]:
    input_rows: list[dict[str, object]] = []
    for source in SOURCES:
        path = resolve(source["location"], source["relative_path"])
        input_rows.append(
            {
                **source,
                "path": str(path),
                "exists": b(path.exists()),
                "evidence_hits": evidence(path, source["terms"]),
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )

    contract_rows = [
        {
            "clause_id": "DNC3222_0_parent_object",
            "contract_clause": "R_Q is a parent-action object",
            "minimal_form": "R_Q=R_Q[Phi,A_Q,J_Q,*_q,theta_Q] is defined before observed readout and before local scoring",
            "why_required": "prevents an after-the-fact penalty term from masquerading as a derivation",
            "current_status": "CONTRACT_WRITTEN_NOT_SOURCE_SIGNED",
            "missing_for_claim": "source path showing R_Q in S_parent or derived Euler/Ward complex",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "DNC3222_1_action_term",
            "contract_clause": "defect norm enters the EM kinetic coefficient",
            "minimal_form": "S_EM=-1/4 int sqrt(-g_q) [Z_* + lambda_D <R_Q,R_Q>_P] F_Q^2",
            "why_required": "attaches the double-zero to the EM F_Q^2 vertex rather than a generic GR/local chain",
            "current_status": "EXACT_CONTRACT_NOT_PARENT_SIGNED",
            "missing_for_claim": "lambda_D units/value/sign and parent inner product <.,.>_P",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "DNC3222_2_same_branch_root",
            "contract_clause": "local branch solves R_Q=0",
            "minimal_form": "R_Q(Phi_*)=0 follows from parent Euler/Ward/nohair equations on the same local branch",
            "why_required": "the zero must be dynamical, not fitted per test arena",
            "current_status": "ROOT_NOT_SOURCE_SIGNED",
            "missing_for_claim": "same-branch local root theorem and boundary/readout silence",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "DNC3222_3_no_linear_defect",
            "contract_clause": "no linear or independent EM coefficient survives",
            "minimal_form": "Delta Z_A has no a<R_Q> term and no independent lambda_A F_Q^2 or f(I_hid)F_Q^2 slot",
            "why_required": "a linear defect or independent scalar coefficient reintroduces b_alpha_m",
            "current_status": "UNSIGNED_DUE_TO_OPERATOR_DOMAIN_OBSTRUCTION",
            "missing_for_claim": "operator-domain exhaustion, exact symmetry, or finite retained coefficient row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "DNC3222_4_A_variation_safe",
            "contract_clause": "Maxwell limit is not spoiled at first variation",
            "minimal_form": "delta_A S_defect|_{R_Q=0}=0 even if R_Q depends on A_Q, because delta||R_Q||^2=2<R_Q,delta R_Q>",
            "why_required": "if R_Q contains A_Q or Hodge/current data, the defect term must not alter Maxwell equations on the exact root branch",
            "current_status": "EXACT_CONDITIONAL_GUARD",
            "missing_for_claim": "R_Q root and regular derivative domain",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "DNC3222_5_hessian_guard",
            "contract_clause": "second variation is bounded",
            "minimal_form": "G_eff >= G_mem - eta_D - eta_stress - eta_readout > 0",
            "why_required": "double-zero kills linear source but not quadratic/range corrections",
            "current_status": "FINITE_INPUTS_MISSING",
            "missing_for_claim": "lambda_D, ||dR_Q||, G_mem floor, stress/readout correction bounds",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "DNC3222_6_stress_readout",
            "contract_clause": "Poynting/Hodge/readout channels are separate",
            "minimal_form": "F_Q^2 source-root must be paired with T_EM/Hodge/current descent or finite residual bounds",
            "why_required": "null radiation can have F_Q^2=0 while T_EM and Poynting flux are nonzero",
            "current_status": "SEPARATE_GATE_REQUIRED",
            "missing_for_claim": "stress/Poynting residual theorem or bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "clause_id": "DNC3222_7_verdict",
            "contract_clause": "promote defect-norm EM source-root owner",
            "minimal_form": "DNC3222_0 through DNC3222_6 all source-signed",
            "why_required": "this is the full no-smuggling contract",
            "current_status": "CONTRACT_EXACT_NOT_LIVE",
            "missing_for_claim": "parent R_Q source and finite Hessian/stress/readout inputs",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    candidate_rows = [
        {
            "candidate_id": "RQ3222_0_Ward_current_mismatch",
            "candidate_RQ": "R_W^nu = nabla_mu(Z_* F_Q^{mu nu}) - J_Q^nu",
            "would_close": "on-shell Maxwell/Ward residual root gives ||R_W||^2 double-zero",
            "advantage": "connects directly to Maxwell equation and source-current normalization",
            "hazard": "contains A_Q/F_Q, so it is a higher-derivative/nonlinear residual unless first-variation and Hessian guards pass",
            "current_status": "PROMISING_CONTRACT_NOT_SOURCE_SIGNED",
            "needed_next": "derive R_W from parent Ward complex and prove R_W=0 on branch",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "RQ3222_1_phase_current_defect",
            "candidate_RQ": "R_theta = d_rel J_B or nabla_mu J_Q^mu",
            "would_close": "charge conservation defect root can give a squared scalar source-root",
            "advantage": "uses existing phase/current and boundary-current support",
            "hazard": "conservation alone does not own Z_A or alpha; must be tied to EM kinetic coefficient by parent action",
            "current_status": "CURRENT_SUPPORT_NOT_KINETIC_OWNER",
            "needed_next": "show S_EM coefficient depends on ||R_theta||^2, not arbitrary f(theta)",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "RQ3222_2_Hodge_descent_defect",
            "candidate_RQ": "R_H = *_obs(q(Phi)) - *_EM,parent or coframe/Hodge descent residual",
            "would_close": "readout/Hodge root can protect alpha readout and part of stress/Poynting channel",
            "advantage": "directly attacks the wave/Poynting guard rather than only scalar F^2",
            "hazard": "Hodge descent is currently unsigned and may duplicate metric/local-GR assumptions",
            "current_status": "NEEDED_FOR_STRESS_ROUTE_NOT_DERIVED",
            "needed_next": "define parent Hodge residual and prove quotient-fixed observed star",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "RQ3222_3_Maxwell_subblock_residual",
            "candidate_RQ": "R_Z = Z_A - C_P N_Q or projection residual of unique parent Maxwell subblock",
            "would_close": "if unique subblock residual vanishes, independent EM coefficient leakage becomes a squared defect",
            "advantage": "closest to alpha/coupling ownership",
            "hazard": "operator-domain exhaustion currently fails; defining R_Z can be circular if Z_A is fitted",
            "current_status": "BEST_ALPHA_OWNER_FORM_BUT_CIRCULAR_UNLESS_PARENT_DEFINED",
            "needed_next": "derive C_P,N_Q and residual from parent bundle, not observed alpha fit",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "candidate_id": "RQ3222_4_selected_target",
            "candidate_RQ": "two-lane target: R_Z for coefficient ownership plus R_H/R_W for stress-current safety",
            "would_close": "R_Z attacks b_alpha_m; R_H/R_W attacks Maxwell stress/Poynting/readout leakage",
            "advantage": "avoids pretending one scalar F^2 gate closes all EM physics",
            "hazard": "requires more than one sourced residual unless a single parent complex unifies them",
            "current_status": "BEST_NEXT_CONTRACT_TARGET",
            "needed_next": "3223 source search or finite runner: R_Z first, R_H/R_W guard second",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    variation_rows = [
        {
            "proof_id": "VAR3222_0_coefficient_first_variation",
            "object": "memory/source variation",
            "statement": "delta_m Delta Z_A = 2 lambda_D <R_Q, delta_m R_Q>_P, so delta_m Delta Z_A|_{R_Q=0}=0.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "claim_effect": "kills the linear b_alpha_m source if the root is parent-owned",
            "remaining_debt": "parent R_Q root, no linear/independent coefficient, finite denominator",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "proof_id": "VAR3222_1_A_variation",
            "object": "Maxwell equation first variation",
            "statement": "delta_A[-1/4 lambda_D ||R_Q||^2 F_Q^2] has terms proportional to ||R_Q||^2 delta_A F_Q^2 and 2<R_Q,delta_A R_Q>F_Q^2; both vanish on R_Q=0.",
            "result": "EXACT_CONDITIONAL_MAXWELL_LIMIT",
            "claim_effect": "permits R_Q to depend on A_Q without changing the exact-root Maxwell equation at first variation",
            "remaining_debt": "regular derivative domain and second-variation correction bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "proof_id": "VAR3222_2_second_variation",
            "object": "quadratic correction",
            "statement": "delta^2 Delta Z_A|root contains 2 lambda_D <delta R_Q,delta R_Q>_P and can shift propagation, memory Hessian, or effective range.",
            "result": "HESSIAN_DEBT_RETAINED",
            "claim_effect": "prevents overclaiming source silence as full local safety",
            "remaining_debt": "eta_D <= function(lambda_D, ||dR_Q||, ||F_Q^2||) and G_eff positivity",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "proof_id": "VAR3222_3_no_linear_defect_counterexample",
            "object": "why square matters",
            "statement": "If Delta Z_A=a<R_Q>+lambda_D||R_Q||^2, then delta_m Delta Z_A|root=a<delta_m R_Q> generically survives.",
            "result": "LINEAR_DEFECT_FORBIDDEN",
            "claim_effect": "forces squared/even defect dependence or exact symmetry",
            "remaining_debt": "operator-domain or symmetry proof excluding linear defect terms",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    stress_rows = [
        {
            "guard_id": "SPG3222_0_null_wave_guard",
            "channel": "null EM radiation",
            "problem": "F_Q^2=0 while T_EM and Poynting vector can be nonzero",
            "required_gate": "stress/Hodge/current residual R_T or finite T_EM projection bound",
            "current_status": "NOT_CLOSED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "guard_id": "SPG3222_1_readout_guard",
            "channel": "observed alpha/clocks/spectra",
            "problem": "bare coefficient root does not guarantee alpha_eff readout root",
            "required_gate": "effective/readout map preserves the same defect norm or has finite residual row",
            "current_status": "NOT_CLOSED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "guard_id": "SPG3222_2_current_normalization",
            "channel": "source/current coupling",
            "problem": "J_Q normalization can float even if Maxwell kinetic coefficient is locally stationary",
            "required_gate": "same T_Q/Ward owner for kinetic coefficient and matter current",
            "current_status": "NOT_CLOSED",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "guard_id": "SPG3222_3_local_GR_boundary",
            "channel": "local GR/Newton/PPN transfer",
            "problem": "EM defect norm does not prove EH source normalization, Poisson-Gauss, or PPN values",
            "required_gate": "separate local GR/Newton source-charge and PPN derivations",
            "current_status": "NO_TRANSFER_CLAIM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    runner_rows = [
        {
            "runner_input_id": "AR3222_0_theorem_zero_switch",
            "quantity": "b_alpha_m_zero_from_defect_norm",
            "required_value": "0",
            "activation_condition": "DNC3222_0..6 source-signed with no linear defect and finite Hessian/stress/readout guards",
            "current_status": "INACTIVE_NONCLAIM",
            "fallback_if_missing": "use finite b_alpha_m bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "runner_input_id": "AR3222_1_lambda_D",
            "quantity": "lambda_D",
            "required_value": "numeric or theorem-fixed coefficient",
            "activation_condition": "source-backed parent action term",
            "current_status": "MISSING",
            "fallback_if_missing": "claim blocked; smoke row only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "runner_input_id": "AR3222_2_RQ_norm_slope",
            "quantity": "||partial_m R_Q||",
            "required_value": "finite operator/support norm",
            "activation_condition": "linearized parent defect map exists",
            "current_status": "MISSING",
            "fallback_if_missing": "Hessian/off-root bound blocked",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "runner_input_id": "AR3222_3_delta_m_Zmin",
            "quantity": "Delta m and Z_min",
            "required_value": "local displacement amplitude and positive EM denominator",
            "activation_condition": "finite off-root b_alpha_m branch",
            "current_status": "MISSING",
            "fallback_if_missing": "no WEP/R10/clock transfer",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "runner_input_id": "AR3222_4_stress_readout_residual",
            "quantity": "eta_stress and eta_readout",
            "required_value": "finite bounds or theorem-zero switches",
            "activation_condition": "Maxwell stress/Poynting and alpha readout gates close",
            "current_status": "MISSING",
            "fallback_if_missing": "keep EM stress and observed alpha claims blocked",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "runner_input_id": "AR3222_5_arena_projection",
            "quantity": "tau_clock, tau_WEP, tau_R10, beta_source_alpha",
            "required_value": "source-backed projection factors for empirical arenas",
            "activation_condition": "finite b_alpha_m or theorem-zero switch is available",
            "current_status": "MISSING_FOR_CLAIM",
            "fallback_if_missing": "runner may smoke-test schema only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC3222_0_result",
            "decision": "DEFECT_NORM_PARENT_ACTION_CONTRACT_EXACT_BUT_NOT_SOURCE_SIGNED",
            "because": "the contract proves how a squared parent defect can preserve the Maxwell limit and kill b_alpha_m linearly, but no parent R_Q source row exists yet",
            "claim_status": "NO_BALPHA_M_ZERO_NO_MAXWELL_STRESS_NO_LOCAL_GR_CLAIM",
            "next_action": "source-search R_Z/R_W/R_H candidates; if none source-sign, implement finite alpha coefficient runner rows as nonclaim smoke inputs",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "DEC3222_1_next_target",
            "decision": "3223-Y5-R2FR-RQ-source-search-or-finite-alpha-runner-smoke-inputs-under-AX1090",
            "because": "the theorem shape is now sharp enough to search for concrete parent rows instead of circling the same coupling gap",
            "claim_status": "PRIVATE_NEXT_TARGET",
            "next_action": "try R_Z coefficient residual first, then R_W/R_H stress-current guards; otherwise build runner smoke rows with valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]

    return input_rows, contract_rows, candidate_rows, variation_rows, stress_rows, runner_rows, decision_rows


def validation_rows(
    now: str,
    input_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    variation_rows: list[dict[str, object]],
    stress_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    out_paths = [INPUTS, CONTRACT, CANDIDATES, VARIATION, STRESS, RUNNER, DECISION]
    all_inputs_exist = all(row["exists"] == "true" for row in input_rows)
    contract_verdict = next(row for row in contract_rows if row["clause_id"] == "DNC3222_7_verdict")
    first_variation = any(row["proof_id"] == "VAR3222_0_coefficient_first_variation" for row in variation_rows)
    maxwell_variation = any(row["proof_id"] == "VAR3222_1_A_variation" for row in variation_rows)
    linear_forbidden = any(row["proof_id"] == "VAR3222_3_no_linear_defect_counterexample" for row in variation_rows)
    stress_guard = any(row["guard_id"] == "SPG3222_0_null_wave_guard" for row in stress_rows)
    runner_nonclaim = len(runner_rows) >= 6
    claim_true_count = 0
    for rows in [input_rows, contract_rows, candidate_rows, variation_rows, stress_rows, runner_rows, decision_rows]:
        for row in rows:
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_true_count += 1
    no_fw_outputs = all(FW not in [path, *path.parents] for path in out_paths + [DOC])

    csv_parse_ok = True
    csv_parse_detail: list[str] = []
    for path in out_paths:
        try:
            parsed = read_csv(path)
            if not parsed:
                csv_parse_ok = False
            csv_parse_detail.append(path.name)
        except Exception as exc:
            csv_parse_ok = False
            csv_parse_detail.append(f"{path.name}:{exc}")

    return [
        {"check_id": "VAL3222_00_inputs_exist", "pass": b(all_inputs_exist), "detail": f"inputs={len(input_rows)}", "generated_utc": now},
        {"check_id": "VAL3222_01_contract_verdict", "pass": b(contract_verdict["current_status"] == "CONTRACT_EXACT_NOT_LIVE"), "detail": str(contract_verdict["current_status"]), "generated_utc": now},
        {"check_id": "VAL3222_02_first_variation_zero", "pass": b(first_variation), "detail": "delta_m Delta Z_A vanishes at R_Q=0", "generated_utc": now},
        {"check_id": "VAL3222_03_Maxwell_variation_guard", "pass": b(maxwell_variation), "detail": "delta_A defect term vanishes at R_Q=0 to first variation", "generated_utc": now},
        {"check_id": "VAL3222_04_linear_defect_forbidden", "pass": b(linear_forbidden), "detail": "linear defect term would reintroduce source", "generated_utc": now},
        {"check_id": "VAL3222_05_stress_guard_retained", "pass": b(stress_guard), "detail": "Poynting/null-wave channel not closed by scalar F2 root", "generated_utc": now},
        {"check_id": "VAL3222_06_runner_rows_nonclaim", "pass": b(runner_nonclaim), "detail": f"runner_rows={len(runner_rows)}", "generated_utc": now},
        {"check_id": "VAL3222_07_claims_blocked", "pass": b(claim_true_count == 0), "detail": f"claim_rows_true={claim_true_count}", "generated_utc": now},
        {"check_id": "VAL3222_08_no_formalization_workbench_edit", "pass": b(no_fw_outputs), "detail": "no formalization-workbench paths are output targets", "generated_utc": now},
        {"check_id": "VAL3222_09_csv_parse", "pass": b(csv_parse_ok), "detail": ";".join(csv_parse_detail), "generated_utc": now},
        {"check_id": "VAL3222_10_next_target", "pass": b(decision_rows[-1]["decision"].startswith("3223-")), "detail": str(decision_rows[-1]["decision"]), "generated_utc": now},
    ]


def write_doc(
    input_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    variation_rows: list[dict[str, object]],
    stress_rows: list[dict[str, object]],
    runner_rows: list[dict[str, object]],
    decision_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 3222 - Defect-Norm Parent-Action Contract Or Finite Alpha Coefficient Runner under AX1090

Private checkpoint. This is not a local-GR claim, Maxwell derivation claim, Newtonian-limit claim, WEP pass, R10 pass, clock pass, `b_alpha_m=0` claim, EM-lock claim, or public-facing result.

## Result

3222 turns the `R_Q` idea into an exact parent-action contract.

The allowed coupling shape is:

```text
S_EM = -1/4 int sqrt(-g_q) [Z_* + lambda_D <R_Q,R_Q>_P] F_Q^2
R_Q(Phi_*) = 0
```

Then:

```text
delta_m Delta Z_A | root = 2 lambda_D <R_Q, delta_m R_Q>_P | root = 0.
```

And if `R_Q` depends on `A_Q`/`F_Q`, the first Maxwell variation is still safe on the exact root branch:

```text
delta_A S_defect has terms proportional to ||R_Q||^2 and <R_Q,delta_A R_Q>,
so delta_A S_defect | root = 0.
```

That is the useful leap: the coupling can be real, and still locally source-silent to first variation.

But the contract is not live yet. Current MTS files do not source-sign `R_Q` as a parent object, do not prove the same-branch root, and do not bound the second variation/stress/readout debt. So the route is sharpened, not claimed.

Current verdict: `DEFECT_NORM_PARENT_ACTION_CONTRACT_EXACT_BUT_NOT_SOURCE_SIGNED`.

## Parent-Action Defect-Norm Contract

{md_table(contract_rows, ["clause_id", "contract_clause", "minimal_form", "current_status", "missing_for_claim", "valid_for_claim"])}

## RQ Candidate Routes

{md_table(candidate_rows, ["candidate_id", "candidate_RQ", "would_close", "advantage", "hazard", "current_status", "needed_next", "valid_for_claim"])}

## Variation And Maxwell-Limit Proof

{md_table(variation_rows, ["proof_id", "object", "statement", "result", "claim_effect", "remaining_debt", "valid_for_claim"])}

## Stress, Poynting, And Readout Guards

{md_table(stress_rows, ["guard_id", "channel", "problem", "required_gate", "current_status", "valid_for_claim"])}

## Finite Alpha Runner Spec

{md_table(runner_rows, ["runner_input_id", "quantity", "required_value", "activation_condition", "current_status", "fallback_if_missing", "valid_for_claim"])}

## Decision

{md_table(decision_rows, ["decision_id", "decision", "because", "claim_status", "next_action", "valid_for_claim"])}

## Generated Evidence

- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3222_INPUTS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3222_PARENT_ACTION_DEFECT_NORM_CONTRACT.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3222_RQ_CANDIDATE_ROUTES.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3222_VARIATION_AND_MAXWELL_LIMIT_PROOF.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3222_STRESS_POYNTING_AND_READOUT_GUARDS.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3222_FINITE_ALPHA_RUNNER_SPEC.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3222_DECISION.csv`
- `post-checkpoint-work/source-intake/mts_residuals/P8_Y5_R2FR_3222_VALIDATION.csv`

## Source Register

{md_table(input_rows, ["input_id", "relative_path", "exists", "role", "evidence_hits", "valid_for_claim"])}

## Validation

{md_table(validation, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    now = stamp()
    input_rows, contract_rows, candidate_rows, variation_rows, stress_rows, runner_rows, decision_rows = build_rows(now)
    for path, rows in [
        (INPUTS, input_rows),
        (CONTRACT, contract_rows),
        (CANDIDATES, candidate_rows),
        (VARIATION, variation_rows),
        (STRESS, stress_rows),
        (RUNNER, runner_rows),
        (DECISION, decision_rows),
    ]:
        write_csv(path, rows)
    validation = validation_rows(
        now,
        input_rows,
        contract_rows,
        candidate_rows,
        variation_rows,
        stress_rows,
        runner_rows,
        decision_rows,
    )
    write_csv(VALIDATION, validation)
    write_doc(input_rows, contract_rows, candidate_rows, variation_rows, stress_rows, runner_rows, decision_rows, validation)
    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")


if __name__ == "__main__":
    main()
