from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1400-Y5-R10-RAB-joined-EM-coupling-owner-contract-or-finite-local-residual-vector.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1400_SOURCE_REGISTER.csv"
JOINED_CONTRACT_PATH = SRC_DIR / "P8_Y5_R10_1400_JOINED_EM_OWNER_CONTRACT.csv"
THEOREM_ATTEMPT_PATH = SRC_DIR / "P8_Y5_R10_1400_JOINED_EM_THEOREM_ATTEMPT.csv"
LOCAL_RESIDUAL_PATH = SRC_DIR / "P8_Y5_R10_1400_FINITE_EM_LOCAL_RESIDUAL_VECTOR.csv"
ARENA_GATE_PATH = SRC_DIR / "P8_Y5_R10_1400_EM_LOCAL_ARENA_PROJECTION_GATES.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1400_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1400_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1400_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1400_VALIDATION.csv"

STATUS = (
    "Y5_R10_1400_joined_EM_owner_theorem_conditional_only_"
    "finite_EM_local_residual_vector_written_nonclaim"
)
CLAIM_CEILING = (
    "joined_EM_owner_contract_and_finite_residual_vector_only_no_lambda_A_zero_no_unique_F2_"
    "no_EM_lock_zero_no_alphaEM_bound_no_WEP_no_clock_no_R10_no_PPN_no_Newton_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1400_0_1399_doc",
        "source_path": "1399-Y5-R10-RAB-gauge-level-index-owner-for-lambdaA-or-finite-alphaEM-prior-vector.md",
        "required_anchor": "NEXT1399_0_1400",
        "purpose": "handoff selecting joined EM owner contract or finite local residual vector",
    },
    {
        "source_id": "SRC1400_1_1399_owner_vector",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1399_LAMBDA_A_OWNER_VECTOR.csv",
        "required_anchor": "LOV1399_4_lambda_A",
        "purpose": "lambda_A owner vector remains missing/nonclaim",
    },
    {
        "source_id": "SRC1400_2_1399_finite",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1399_FINITE_ALPHAEM_PRIOR_VECTOR.csv",
        "required_anchor": "FAP1399_3_local_vector",
        "purpose": "finite EM local residual vector is incomplete",
    },
    {
        "source_id": "SRC1400_3_1398_contract",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1398_PARENT_ACTION_SELECTION_CONTRACT.csv",
        "required_anchor": "PAC1398_5_matter_current_readout_join",
        "purpose": "joined parent action clauses after pullback no-go",
    },
    {
        "source_id": "SRC1400_4_1397_proof",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1397_UNIQUE_MAXWELL_F2_PROOF_AUDIT.csv",
        "required_anchor": "UMF1397_2_operator_basis_uniqueness",
        "purpose": "unique F2 proof still fails current corpus",
    },
    {
        "source_id": "SRC1400_5_1396_repair",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1396_EM_LOCK_REPAIR_ATTEMPT.csv",
        "required_anchor": "ELR1396_6_current_verdict",
        "purpose": "EM-lock repair remains blocked",
    },
    {
        "source_id": "SRC1400_6_989_audit",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv",
        "required_anchor": "ELA989_5_total",
        "purpose": "T_Q/F2/current/readout/no-alpha signature audit",
    },
    {
        "source_id": "SRC1400_7_765_counter",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv",
        "required_anchor": "RCE765_0_lambda_F2",
        "purpose": "lambda/current/readout counterexamples",
    },
    {
        "source_id": "SRC1400_8_1396_beta_template",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1396_BETA_EM_SOURCE_BOUND_TEMPLATE.csv",
        "required_anchor": "BEM1396_6_template_verdict",
        "purpose": "finite beta_EM template to integrate into local residual vector",
    },
    {
        "source_id": "SRC1400_9_1398_prior",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1398_LAMBDA_A_PRIOR_BOUND_VECTOR.csv",
        "required_anchor": "LAP1398_4_WEP_bound_channel",
        "purpose": "lambda_A finite prior/bound vector",
    },
    {
        "source_id": "SRC1400_10_this_script",
        "source_path": "scripts/Y5_R10_RAB_joined_EM_coupling_owner_contract_or_finite_local_residual_vector.py",
        "required_anchor": "STATUS",
        "purpose": "1400 generator",
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


def joined_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "JEO1400_0_parent_charge_generator",
            "joined_owner_clause": "T_Q exists as a compact vertical generator in the varied parent action",
            "mathematical_form": "A_Q=A^Q T_Q, exp(2*pi*T_Q)=1, and T_Q is not a post-readout label",
            "current_status": "UNSIGNED",
            "blocker": "T_Q is still template/closure-level rather than a parent-action object",
            "finite_residual_if_missing": "charge-unit and A_Q normalization rescalings",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "clause_id": "JEO1400_1_fixed_norm",
            "joined_owner_clause": "T_Q has a fixed non-rescalable parent norm",
            "mathematical_form": "N_Q=<T_Q,T_Q>_P, Lie_v N_Q=0, and T_Q -> s T_Q is not an allowed representative change",
            "current_status": "UNSIGNED",
            "blocker": "no parent metric/symplectic/lattice derivation fixes N_Q",
            "finite_residual_if_missing": "rho_NQ := partial_phi_c ln N_Q",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "clause_id": "JEO1400_2_no_pullback_unique_F2",
            "joined_owner_clause": "the two-derivative operator basis forbids independent q^*(F_Q^2)",
            "mathematical_form": "Allowed_2der(parent,U1_Q)=span{<F,F>_P}; DeltaS_lambda=-(lambda_A/4)int q^*(F_Q^2) inadmissible",
            "current_status": "FAILS_CURRENT_CORPUS",
            "blocker": "1398 proves locality/gauge covariance alone do not exclude pullback counterterms",
            "finite_residual_if_missing": "lambda_A and partial_phi_c lambda_A",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "clause_id": "JEO1400_3_same_current_owner",
            "joined_owner_clause": "matter charge labels, source current, and Maxwell source normalization descend from the same T_Q owner",
            "mathematical_form": "S_int=sum_A n_A int A_Q J_A with Lie_v n_A=0 and no independent beta_source_alpha",
            "current_status": "UNSIGNED",
            "blocker": "current rescaling and beta_source_alpha remain unowned",
            "finite_residual_if_missing": "beta_source_alpha and WEP/R10 source-test strength",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "clause_id": "JEO1400_4_readout_descent",
            "joined_owner_clause": "Hodge star, coframe, and hbar*c readout are quotient-fixed for dimensionless alpha_EM",
            "mathematical_form": "Lie_v ln(*_obs)=Lie_v ln(hbar*c)=0 or all readout factors cancel in alpha_EM",
            "current_status": "UNSIGNED",
            "blocker": "coframe/Hodge/readout leakage remains possible",
            "finite_residual_if_missing": "rho_readout and clock/fine-structure drift",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "clause_id": "JEO1400_5_no_alpha_matter_vertex",
            "joined_owner_clause": "ordinary matter functor has no alpha_EM(chi_X), f_A(chi_X)F^2, m_A(chi_X), or binding-response vertex",
            "mathematical_form": "delta S_matter/dchi_X|ehat,theta_A=0 and Lie_v theta_A=0 in the observed matter branch",
            "current_status": "UNSIGNED",
            "blocker": "composition-dependent Coulomb/mass/binding channels remain physical fallback rows",
            "finite_residual_if_missing": "beta_EM(lambda_A), material binding response, and composition charges",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "clause_id": "JEO1400_6_radiative_stability",
            "joined_owner_clause": "the no-lambda/no-alpha rule is stable under projection and effective reduction",
            "mathematical_form": "delta lambda_A=0 or generated terms are absorbed into fixed C_P N_Q with no local derivative",
            "current_status": "UNSIGNED",
            "blocker": "no parent RG/threshold/non-renormalization rule has been supplied",
            "finite_residual_if_missing": "effective alphaEM residual after thresholds",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "clause_id": "JEO1400_7_joined_verdict",
            "joined_owner_clause": "all EM coupling owners close together",
            "mathematical_form": "JEO1400_0 through JEO1400_6 all parent-signed",
            "current_status": "JOINED_OWNER_NOT_CLOSED",
            "blocker": "unique F2 fails current corpus and all other clauses remain unsigned",
            "finite_residual_if_missing": "R_EM_local vector required",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def theorem_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "JET1400_0_lambda_zero",
            "candidate_statement": "if fixed T_Q norm and no-pullback unique F2 close, then lambda_A=0 or is absorbed into fixed C_P N_Q",
            "derivation_status": "EXACT_CONDITIONAL_ONLY",
            "current_blocker": "JEO1400_1 and JEO1400_2 are not signed; JEO1400_2 currently fails",
            "if_closed": "g_EM^{-2}=C_P N_Q with no independent lambda_A derivative",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "theorem_id": "JET1400_1_alpha_silence",
            "candidate_statement": "if lambda route, readout descent, and radiative stability close, then b_alpha_EM=0",
            "derivation_status": "EXACT_CONDITIONAL_ONLY",
            "current_blocker": "lambda_A, readout, and RG/threshold owners missing",
            "if_closed": "clock/fine-structure alpha drift closes structurally",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "theorem_id": "JET1400_2_source_silence",
            "candidate_statement": "if current owner and no-alpha matter vertex close, then beta_source_alpha and beta_EM binding response are theorem-zero",
            "derivation_status": "EXACT_CONDITIONAL_ONLY",
            "current_blocker": "current/source normalization and no-alpha matter functor unsigned",
            "if_closed": "WEP/R10 source-test EM channels close structurally",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "theorem_id": "JET1400_3_local_residual_zero",
            "candidate_statement": "if JET1400_0 through JET1400_2 close, then R_EM_local=0 for the EM coupling branch",
            "derivation_status": "EXACT_CONDITIONAL_ONLY",
            "current_blocker": "none of the three sub-theorems is promoted",
            "if_closed": "EM coupling branch stops blocking local GR/Newton reentry",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "theorem_id": "JET1400_4_current_verdict",
            "candidate_statement": "joined EM-coupling owner theorem status",
            "derivation_status": "JOINED_THEOREM_NOT_PROMOTED_FINITE_RESIDUAL_VECTOR_REQUIRED",
            "current_blocker": "T_Q norm, no-pullback, current owner, readout descent, no-alpha vertex, and radiative stability remain unsigned or failed",
            "if_closed": "reopen beta_EM zero and local GR reentry route",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def local_residual_rows() -> list[dict[str, str]]:
    return [
        {
            "residual_id": "REM1400_0_lambda_A",
            "quantity": "lambda_A",
            "definition": "standalone Maxwell kinetic counterterm coefficient",
            "formula": "DeltaS_lambda=-(lambda_A/4)int q^*(dmu_obs F_Q^2)",
            "needed_input": "parent coefficient, theorem-zero, or empirical prior",
            "current_value": "MISSING_PARENT_COEFFICIENT_OR_ZERO_THEOREM",
            "feeds": "b_alpha_EM; beta_EM; R_EM_local",
            "status": "FINITE_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "residual_id": "REM1400_1_norm_drift",
            "quantity": "rho_NQ",
            "definition": "local drift of charge-generator norm",
            "formula": "rho_NQ=partial_phi_c ln N_Q",
            "needed_input": "fixed parent norm or derivative map",
            "current_value": "MISSING_FIXED_N_Q",
            "feeds": "g_EM^{-2}; alphaEM drift",
            "status": "FINITE_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "residual_id": "REM1400_2_readout",
            "quantity": "rho_readout",
            "definition": "Hodge/coframe/hbar*c readout derivative in dimensionless alpha_EM",
            "formula": "rho_readout=partial_phi_c ln(hbar*c/readout factors)",
            "needed_input": "quotient-fixed coframe/Hodge/readout theorem or derivative map",
            "current_value": "MISSING_READOUT_DESCENT",
            "feeds": "clock/fine-structure drift; local metric readout residual",
            "status": "FINITE_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "residual_id": "REM1400_3_b_alpha_EM",
            "quantity": "b_alpha_EM",
            "definition": "canonical finite alphaEM drift",
            "formula": "b_alpha_EM=-partial_phi_c ln(C_P N_Q+lambda_A)-rho_readout",
            "needed_input": "C_P, N_Q, lambda_A, derivative map, readout descent",
            "current_value": "MISSING_DERIVATIVE_MAP",
            "feeds": "clock; WEP; R10; EM binding",
            "status": "FINITE_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "residual_id": "REM1400_4_beta_source_alpha",
            "quantity": "beta_source_alpha",
            "definition": "source/force normalization multiplying finite alpha WEP branch",
            "formula": "eta_AB_alpha=DeltaQ_alpha_AB beta_source_alpha b_alpha_EM tau_WEP",
            "needed_input": "same-owner current/source theorem or numeric source map",
            "current_value": "TARGET_ONLY_alpha<=4.797780522732e-05_robust<=2.887280314062e-05",
            "feeds": "WEP; R10 source-test response",
            "status": "TARGET_ONLY_NOT_DERIVED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "residual_id": "REM1400_5_clock",
            "quantity": "C_clock_EM",
            "definition": "clock/fine-structure residual product",
            "formula": "C_clock_EM=K_alpha b_alpha_EM tau_clock",
            "needed_input": "clock sensitivity, tau_clock, and b_alpha_EM source map",
            "current_value": "PRODUCT_BOUND_ONLY",
            "feeds": "clock/fine-structure tests",
            "status": "CLOCK_NOT_STANDALONE_BOUND",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "residual_id": "REM1400_6_WEP",
            "quantity": "C_WEP_EM",
            "definition": "finite EM/Coulomb WEP residual",
            "formula": "C_WEP_EM=DeltaQ_alpha_AB beta_source_alpha b_alpha_EM tau_WEP + binding terms",
            "needed_input": "normalized composition charges, beta_source_alpha, tau_WEP, binding map",
            "current_value": "MISSING_SOURCE_TAU_BINDING_MAP",
            "feeds": "WEP gate and local equivalence-principle residual",
            "status": "FINITE_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "residual_id": "REM1400_7_beta_EM",
            "quantity": "beta_EM(lambda_A)",
            "definition": "EM binding contribution to material mass response",
            "formula": "beta_bind,A includes f_EM,A beta_EM(lambda_A)",
            "needed_input": "no-alpha matter theorem or material binding sensitivity map",
            "current_value": "MISSING_BINDING_MAP",
            "feeds": "bulk beta; R10; WEP; local source composition",
            "status": "FINITE_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "residual_id": "REM1400_8_R10",
            "quantity": "C_R10_EM(lambda)",
            "definition": "short-range force residual from finite EM coupling branch",
            "formula": "C_R10_EM=K_bulk_ST(lambda) beta_bulk,S(lambda_A) beta_bulk,T(lambda_A)+epsilon_tail",
            "needed_input": "K_bulk_ST(lambda), beta maps, tail, real bound curve",
            "current_value": "MISSING_KERNEL_TAIL_REAL_BOUND_CURVE",
            "feeds": "R10 alpha(lambda) comparator",
            "status": "R10_NOT_SCOREABLE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "residual_id": "REM1400_9_local_PPN",
            "quantity": "R_EM_local",
            "definition": "combined EM coupling residual entering local PPN/Newton/GR reduction gates",
            "formula": "R_EM_local=(lambda_A,rho_NQ,rho_readout,b_alpha_EM,beta_source_alpha,C_clock_EM,C_WEP_EM,beta_EM,C_R10_EM)",
            "needed_input": "all prior residual entries zero-certified or bounded with local projection maps",
            "current_value": "LOCAL_VECTOR_EXPLICIT_BUT_UNBOUNDED",
            "feeds": "PPN/Newton/local-GR reentry",
            "status": "LOCAL_GR_BLOCKED_BY_UNBOUNDED_EM_VECTOR",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def arena_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "ELG1400_0_joined_theorem",
            "arena": "joined EM owner theorem",
            "required_input": "JEO1400_0 through JEO1400_6 all parent-signed",
            "current_blocker": "joined contract fails current corpus",
            "status": "BLOCKED_JOINED_OWNER_NOT_CLOSED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "ELG1400_1_alphaEM_clock",
            "arena": "alphaEM/clock",
            "required_input": "b_alpha_EM and tau_clock or theorem-zero",
            "current_blocker": "REM1400_3 and REM1400_5 missing/product-only",
            "status": "BLOCKED_ALPHA_CLOCK_NOT_SCOREABLE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "ELG1400_2_WEP",
            "arena": "WEP/Coulomb",
            "required_input": "beta_source_alpha, tau_WEP, composition charges, binding map",
            "current_blocker": "REM1400_4 and REM1400_6 target-only/missing",
            "status": "BLOCKED_WEP_NOT_SCOREABLE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "ELG1400_3_R10",
            "arena": "R10 alpha(lambda)",
            "required_input": "beta_EM(lambda_A), K_bulk_ST(lambda), tail, real bound curve",
            "current_blocker": "REM1400_7 and REM1400_8 missing",
            "status": "BLOCKED_R10_NOT_SCOREABLE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "ELG1400_4_local_PPN",
            "arena": "local PPN/Newton/GR",
            "required_input": "R_EM_local zero-certified or bounded below local thresholds",
            "current_blocker": "REM1400_9 explicit but unbounded",
            "status": "BLOCKED_LOCAL_GR_BY_EM_VECTOR",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "ELG1400_5_verdict",
            "arena": "all EM coupling gates",
            "required_input": "theorem-zero or source-backed finite residual vector",
            "current_blocker": "neither exists",
            "status": "ARENA_SCORING_BLOCKED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "claim_id": "GATE1400_0_joined_owner",
            "claim": "joined EM-coupling owner theorem is proved",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "contract clauses are unsigned and unique F2/no-pullback currently fails",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1400_1_lambda_unique_F2",
            "claim": "lambda_A=0 and unique Maxwell F2",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "lambda_A remains explicit in finite residual vector",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1400_2_EM_lock",
            "claim": "EM-lock sets beta_EM=0",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "no-alpha matter vertex/current/readout owner remain unsigned",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1400_3_empirical",
            "claim": "alphaEM, WEP, clock, or R10 pass",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1400 writes residual vector only; no data score is performed",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1400_4_local_GR",
            "claim": "local GR/Newton/PPN reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "R_EM_local is explicit but unbounded",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1400_0_theorem",
            "decision": "do not promote joined EM owner theorem",
            "reason": "the exact conditional theorem exists, but the current corpus does not sign its premises",
            "consequence": "EM coupling branch remains finite/nonclaim",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1400_1_residual",
            "decision": "use R_EM_local as the explicit local residual vector",
            "reason": "this prevents hidden alphaEM/WEP/R10/PPN claims while preserving a testable route",
            "consequence": "next work should source or bound each residual entry",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1400_2_next",
            "decision": "build finite EM residual source map and PPN pressure gate",
            "reason": "after theorem failure, the least-cheaty progress is bounding the finite vector",
            "consequence": "next target 1401",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1400_0_1401",
            "target_doc": "1401-Y5-R10-RAB-finite-EM-local-residual-source-map-and-PPN-pressure-gate.md",
            "target_script": "scripts/Y5_R10_RAB_finite_EM_local_residual_source_map_and_PPN_pressure_gate.py",
            "task": "source, bound, or explicitly block each R_EM_local component, then route the surviving finite EM vector into clock, WEP, R10, and local PPN pressure gates",
            "success_condition": "every residual component has either theorem-zero status, source-backed numeric input, or explicit blocker; no local-GR claim is allowed from missing entries",
            "do_not_claim": "lambda_A=0;unique F2;EM-lock beta_EM=0;alphaEM bound;WEP pass;clock pass;R10 pass;PPN pass;Newton limit;local GR;q_loc=0;GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: list[dict[str, str]],
    contract: list[dict[str, str]],
    theorem: list[dict[str, str]],
    residuals: list[dict[str, str]],
    arenas: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    joined_blocked = any(
        row["clause_id"] == "JEO1400_7_joined_verdict"
        and row["current_status"] == "JOINED_OWNER_NOT_CLOSED"
        for row in contract
    ) and any(
        row["clause_id"] == "JEO1400_2_no_pullback_unique_F2"
        and row["current_status"] == "FAILS_CURRENT_CORPUS"
        for row in contract
    )
    theorem_blocked = any(
        row["theorem_id"] == "JET1400_4_current_verdict"
        and row["derivation_status"] == "JOINED_THEOREM_NOT_PROMOTED_FINITE_RESIDUAL_VECTOR_REQUIRED"
        for row in theorem
    )
    residual_nonclaim = all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in residuals)
    residual_has_missing = any(
        "MISSING" in row["current_value"]
        or "TARGET_ONLY" in row["current_value"]
        or "PRODUCT_BOUND_ONLY" in row["current_value"]
        or "UNBOUNDED" in row["current_value"]
        for row in residuals
    )
    local_vector_present = any(
        row["residual_id"] == "REM1400_9_local_PPN"
        and row["status"] == "LOCAL_GR_BLOCKED_BY_UNBOUNDED_EM_VECTOR"
        for row in residuals
    )
    arenas_blocked = all(
        row["claim_allowed"] == "False"
        and (row["status"].startswith("BLOCKED") or row["status"] == "ARENA_SCORING_BLOCKED")
        for row in arenas
    )
    gates_blocked = all(row["claim_allowed"] == "False" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        JOINED_CONTRACT_PATH,
        THEOREM_ATTEMPT_PATH,
        LOCAL_RESIDUAL_PATH,
        ARENA_GATE_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    scope_ok = all("formalization-workbench" not in str(ROOT / path) for path in output_paths)
    all_ok = (
        source_ok
        and joined_blocked
        and theorem_blocked
        and residual_nonclaim
        and residual_has_missing
        and local_vector_present
        and arenas_blocked
        and gates_blocked
        and scope_ok
    )
    now = datetime.now(timezone.utc).isoformat()
    return [
        {
            "check_id": "VAL1400_0_sources",
            "status": "PASS" if source_ok else "FAIL",
            "detail": "all cited source paths exist and anchors are present",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1400_1_joined_contract",
            "status": "PASS" if joined_blocked else "FAIL",
            "detail": "joined EM owner contract is explicit and remains blocked by unique F2/no-pullback failure",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1400_2_theorem_attempt",
            "status": "PASS" if theorem_blocked else "FAIL",
            "detail": "joined theorem is exact conditional only and not promoted",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1400_3_local_residual_vector",
            "status": "PASS" if residual_nonclaim and residual_has_missing and local_vector_present else "FAIL",
            "detail": "finite EM local residual vector is explicit, nonclaim, and unbounded",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1400_4_arena_claim_gates",
            "status": "PASS" if arenas_blocked and gates_blocked else "FAIL",
            "detail": "alphaEM, WEP, clock, R10, PPN, Newton, and local-GR claims remain blocked",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1400_5_scope",
            "status": "PASS" if scope_ok else "FAIL",
            "detail": "outputs are confined to post-checkpoint-work paths",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1400_6_overall",
            "status": "PASS" if all_ok else "FAIL",
            "detail": "1400 writes the joined EM contract and finite local residual vector without promoting claims",
            "generated_utc": now,
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    contract: list[dict[str, str]],
    theorem: list[dict[str, str]],
    residuals: list[dict[str, str]],
    arenas: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    body = f"""# 1400 Y5 R10 RAB: Joined EM Coupling Owner Contract Or Finite Local Residual Vector

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

**Current verdict:** the joined EM-coupling owner theorem is the right shape, but it is not proved in the current corpus. The theorem needs fixed `T_Q`, fixed `N_Q`, no-pullback/unique `F^2`, same-owner current, quotient-fixed readout, no-alpha matter vertex, and radiative stability all at once; the unique-`F^2` clause still fails and the rest remain unsigned.

**Discipline move:** the finite EM coupling branch is now represented by one explicit local residual vector `R_EM_local`. This is the object that must be zero-certified or bounded before any local GR/Newton/PPN claim can honestly proceed.

## Source Register

{md_table(sources)}

## Joined EM Owner Contract

{md_table(contract)}

## Joined EM Theorem Attempt

{md_table(theorem)}

## Finite EM Local Residual Vector

{md_table(residuals)}

## EM Local Arena Projection Gates

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
    contract = joined_contract_rows()
    theorem = theorem_attempt_rows()
    residuals = local_residual_rows()
    arenas = arena_gate_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, contract, theorem, residuals, arenas, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(JOINED_CONTRACT_PATH, contract)
    write_csv(THEOREM_ATTEMPT_PATH, theorem)
    write_csv(LOCAL_RESIDUAL_PATH, residuals)
    write_csv(ARENA_GATE_PATH, arenas)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, contract, theorem, residuals, arenas, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1400 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
