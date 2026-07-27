from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = Path("source-intake/mts_residuals")

DOC_PATH = Path("1397-Y5-R10-RAB-unique-Maxwell-F2-proof-or-lambdaA-source-row.md")
SOURCE_REGISTER_PATH = SRC_DIR / "P8_Y5_R10_1397_SOURCE_REGISTER.csv"
PROOF_AUDIT_PATH = SRC_DIR / "P8_Y5_R10_1397_UNIQUE_MAXWELL_F2_PROOF_AUDIT.csv"
LAMBDA_SOURCE_PATH = SRC_DIR / "P8_Y5_R10_1397_LAMBDA_A_SOURCE_ROW.csv"
ARENA_GATE_PATH = SRC_DIR / "P8_Y5_R10_1397_LAMBDA_A_ALPHAEM_ARENA_GATE.csv"
CLAIM_GATE_PATH = SRC_DIR / "P8_Y5_R10_1397_CLAIM_GATE.csv"
DECISION_LEDGER_PATH = SRC_DIR / "P8_Y5_R10_1397_DECISION_LEDGER.csv"
NEXT_TARGET_PATH = SRC_DIR / "P8_Y5_R10_1397_NEXT_TARGET.csv"
VALIDATION_PATH = SRC_DIR / "P8_Y5_BRR545_1397_VALIDATION.csv"

STATUS = (
    "Y5_R10_1397_unique_Maxwell_F2_proof_attempt_fails_current_corpus_"
    "lambda_A_source_row_written_nonclaim"
)
CLAIM_CEILING = (
    "unique_F2_or_lambda_A_source_row_only_no_EM_lock_zero_no_alphaEM_bound_"
    "no_WEP_no_clock_no_R10_no_PPN_no_Newton_no_local_GR_pass"
)

SOURCE_ROWS = [
    {
        "source_id": "SRC1397_0_1396_doc",
        "source_path": "1396-Y5-R10-RAB-beta-EM-lock-repair-or-finite-alphaEM-source-bound.md",
        "required_anchor": "NEXT1396_0_1397",
        "purpose": "handoff selecting unique Maxwell F2 proof or lambda_A source row",
    },
    {
        "source_id": "SRC1397_1_1396_repair",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1396_EM_LOCK_REPAIR_ATTEMPT.csv",
        "required_anchor": "ELR1396_1_unique_Maxwell_F2",
        "purpose": "unique F2 is the active EM-lock blocker",
    },
    {
        "source_id": "SRC1397_2_1396_template",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_1396_BETA_EM_SOURCE_BOUND_TEMPLATE.csv",
        "required_anchor": "BEM1396_1_b_alpha_EM",
        "purpose": "finite alphaEM template that lambda_A must feed if proof fails",
    },
    {
        "source_id": "SRC1397_3_765_doc",
        "source_path": "765-Y5-R10-parent-vertical-generator-norm-and-Maxwell-kinetic-inheritance-or-alpha-source-fill.md",
        "required_anchor": "RCE765_0_lambda_F2",
        "purpose": "original lambda_A F_Q^2 counterexample and parent norm theorem shape",
    },
    {
        "source_id": "SRC1397_4_765_gate",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv",
        "required_anchor": "MKI765_2_unique_F2",
        "purpose": "machine-readable unique F2 failure gate",
    },
    {
        "source_id": "SRC1397_5_765_counter",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv",
        "required_anchor": "RCE765_0_lambda_F2",
        "purpose": "lambda_A counterexample ledger",
    },
    {
        "source_id": "SRC1397_6_989_doc",
        "source_path": "989-Y5-R10-EM-lock-signature-input-or-alpha-source-normalization-owner.md",
        "required_anchor": "ELA989_1_unique_F2",
        "purpose": "EM-lock audit says unique F2 fails current corpus",
    },
    {
        "source_id": "SRC1397_7_989_audit",
        "source_path": "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv",
        "required_anchor": "ELA989_1_unique_F2",
        "purpose": "CSV audit row for failed unique F2 clause",
    },
    {
        "source_id": "SRC1397_8_988_doc",
        "source_path": "988-Y5-R10-alphaEM-WEP-clock-joint-prior-or-EM-lock-theorem.md",
        "required_anchor": "EMLOCK988_1_unique_Maxwell_F2",
        "purpose": "joint alphaEM/WEP/clock route keeps EM-lock conditional",
    },
    {
        "source_id": "SRC1397_9_this_script",
        "source_path": "scripts/Y5_R10_RAB_unique_Maxwell_F2_proof_or_lambdaA_source_row.py",
        "required_anchor": "STATUS",
        "purpose": "1397 generator",
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


def proof_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "proof_id": "UMF1397_0_parent_connection_projection",
            "clause": "observed EM connection is a parent projection",
            "required_statement": "A_Q is the T_Q component of one parent connection before any observed-sector readout is chosen",
            "mathematical_form": "A_parent = A_Q T_Q + A_perp; F_parent contains F_Q T_Q as a literal subblock",
            "current_evidence": "765 gives this as template only, not a signed parent-action object",
            "current_status": "UNSIGNED",
            "if_closed": "prevents appending an arbitrary observed EM field after quotienting",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "proof_id": "UMF1397_1_fixed_parent_norm",
            "clause": "parent norm fixes the charge-generator length",
            "required_statement": "the bilinear form on the T_Q direction is fixed by parent geometry, lattice, or symplectic data",
            "mathematical_form": "N_Q=<T_Q,T_Q>_P with Lie_v N_Q=0 and no T_Q -> s T_Q freedom",
            "current_evidence": "765 records norm analogies but no parent-fixed EM charge-generator norm",
            "current_status": "UNSIGNED",
            "if_closed": "sets the inherited part of g_EM^{-2}=C_P N_Q",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "proof_id": "UMF1397_2_operator_basis_uniqueness",
            "clause": "no independent Maxwell quadratic invariant",
            "required_statement": "the parent operator basis forbids every observed-only F_Q^2 term not inherited from <F,F>_P",
            "mathematical_form": "Allowed_2der(parent, U(1)_Q) = {<F,F>_P subblock} and not {<F,F>_P, F_Q^2}",
            "current_evidence": "RCE765_0 and ELA989_1 keep DeltaS=-(lambda_A/4) int dmu_obs F_Q^2 legal",
            "current_status": "FAILS_CURRENT_CORPUS",
            "if_closed": "would remove the independent lambda_A coefficient",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "proof_id": "UMF1397_3_no_observed_counterterm_principle",
            "clause": "no quotient-only counterterms in the parent action",
            "required_statement": "the action principle is parent-local only and cannot contain extra terms written solely in observed quotient fields",
            "mathematical_form": "S_parent[Phi] is varied upstairs; DeltaS[q(Phi)] with independent coefficient is not an allowed primitive",
            "current_evidence": "current corpus uses this as desired discipline but has not promoted it to a theorem or symmetry",
            "current_status": "UNSIGNED",
            "if_closed": "would turn lambda_A into an illegal closure appendage rather than a missing coefficient",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "proof_id": "UMF1397_4_renormalized_coefficient_owner",
            "clause": "radiative/renormalized Maxwell coefficient has the same parent owner",
            "required_statement": "renormalization cannot regenerate a separately running lambda_A after quotienting",
            "mathematical_form": "d ln(g_EM^{-2})/d phi_c = d ln(C_P N_Q)/d phi_c, not d ln(C_P N_Q+lambda_A)/d phi_c",
            "current_evidence": "no parent RG/threshold rule has been supplied; finite alpha source branch remains live",
            "current_status": "UNSIGNED",
            "if_closed": "clock and WEP alpha pressure cannot re-enter through effective couplings",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "proof_id": "UMF1397_5_measure_boundary_silence",
            "clause": "measure, Hodge star, and boundary projection add no F_Q^2 residue",
            "required_statement": "projection to observed measure/coframe does not create an independent Maxwell kinetic density",
            "mathematical_form": "dmu_obs * F_Q^2 coefficient is only the projection of dmu_P <F,F>_P",
            "current_evidence": "765 and 989 leave coframe/Hodge/readout leakage as separate unsigned clauses",
            "current_status": "UNSIGNED",
            "if_closed": "blocks an apparent lambda_A sourced by readout rather than by action",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "proof_id": "UMF1397_6_exact_conditional_theorem",
            "clause": "unique Maxwell F2 theorem",
            "required_statement": "if UMF1397_0 through UMF1397_5 are all parent-signed, then lambda_A=0 and unique F2 holds",
            "mathematical_form": "g_EM^{-2}=C_P N_Q; partial_phi_c ln g_EM^{-2}=partial_phi_c ln(C_P N_Q)",
            "current_evidence": "exact conditional theorem is available, but UMF1397_2 fails and the other clauses are unsigned",
            "current_status": "EXACT_CONDITIONAL_THEOREM_READY_NOT_PROMOTED",
            "if_closed": "returns EM-lock to the T_Q/current/readout/no-alpha clauses",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "proof_id": "UMF1397_7_current_verdict",
            "clause": "unique Maxwell F2 proof status",
            "required_statement": "promote Z_unique_F2 only if the lambda_A counterterm is forbidden by parent structure",
            "mathematical_form": "Z_unique_F2 = false while DeltaS_lambda is allowed",
            "current_evidence": "lambda_A F_Q^2 remains gauge invariant, diffeomorphism invariant, and not excluded by current parent contract",
            "current_status": "PROOF_FAILS_CURRENT_CORPUS_LAMBDA_A_SOURCE_ROW_REQUIRED",
            "if_closed": "would allow beta_EM theorem-zero attempt to continue",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def lambda_source_rows() -> list[dict[str, str]]:
    return [
        {
            "row_id": "LAM1397_0_lambda_A",
            "quantity": "lambda_A",
            "definition": "coefficient of a standalone observed Maxwell kinetic counterterm",
            "formula": "DeltaS_lambda = -(lambda_A/4) int dmu_obs F_Q^{mu nu} F^Q_{mu nu}",
            "units": "same convention as g_EM^{-2}; dimensionless in natural 4D normalization after readout is fixed",
            "required_parent_input": "parent theorem forbidding standalone F_Q^2, or a sourced numeric coefficient and derivative",
            "current_value": "MISSING_PARENT_ACTION_COEFFICIENT",
            "provenance": "765::RCE765_0_lambda_F2; 989::ELA989_1_unique_F2; 1396::ELR1396_1_unique_Maxwell_F2",
            "current_status": "SOURCE_ROW_NONCLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "row_id": "LAM1397_1_gEM_inverse",
            "quantity": "g_EM_inverse_squared",
            "definition": "effective inverse electromagnetic coupling after parent norm plus lambda_A",
            "formula": "g_EM^{-2}=C_P N_Q + lambda_A",
            "units": "inverse gauge coupling convention",
            "required_parent_input": "C_P, N_Q, lambda_A, and observed readout normalization",
            "current_value": "MISSING_C_P_N_Q_LAMBDA_A_READOUT",
            "provenance": "765::VGN765_2_unique_curvature_subblock",
            "current_status": "MISSING_NUMERIC_AND_DERIVATIVE_OWNER",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "row_id": "LAM1397_2_alphaEM_drift",
            "quantity": "b_alpha_EM_from_lambda_A",
            "definition": "canonical local alphaEM drift induced by any finite lambda_A branch",
            "formula": "b_alpha_EM = -partial_phi_c ln(C_P N_Q + lambda_A) - partial_phi_c ln(readout factors)",
            "units": "dimensionless derivative per canonical phi_c",
            "required_parent_input": "partial_phi_c C_P, partial_phi_c N_Q, partial_phi_c lambda_A, and readout descent",
            "current_value": "MISSING_DERIVATIVE_MAP",
            "provenance": "1396::BEM1396_1_b_alpha_EM; 988::JAV988_1_clock_product",
            "current_status": "ALPHAEM_SOURCE_DERIVATIVE_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "row_id": "LAM1397_3_EM_binding_feed",
            "quantity": "beta_EM(lambda_A)",
            "definition": "EM binding contribution to material mass response if lambda_A is finite",
            "formula": "beta_bind,A includes f_EM,A * beta_EM(lambda_A)",
            "units": "dimensionless material beta contribution",
            "required_parent_input": "EM binding sensitivity, f_EM,A, b_alpha_EM map, and material composition source",
            "current_value": "MISSING_BINDING_MAP",
            "provenance": "1394::BBR1394_2_beta_EM; 1395::SBP1395_2_beta_EM",
            "current_status": "BULK_BINDING_FEED_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "row_id": "LAM1397_4_clock_product",
            "quantity": "clock_alpha_product",
            "definition": "clock/fine-structure observable product for finite lambda_A alphaEM route",
            "formula": "Delta nu/nu ~ K_alpha * b_alpha_EM * tau_clock",
            "units": "dimensionless fractional clock drift product",
            "required_parent_input": "b_alpha_EM and tau_clock from same parent domain map",
            "current_value": "PRODUCT_BOUND_ONLY",
            "provenance": "988::JAV988_1_clock_product",
            "current_status": "CLOCK_NOT_STANDALONE_B_ALPHA_BOUND",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "row_id": "LAM1397_5_WEP_source_product",
            "quantity": "WEP_alpha_source_product",
            "definition": "WEP source/test response for finite lambda_A alphaEM branch",
            "formula": "eta_AB_alpha = DeltaQ_alpha_AB * beta_source_alpha * b_alpha_EM * tau_WEP",
            "units": "dimensionless Eotvos response",
            "required_parent_input": "beta_source_alpha, b_alpha_EM, tau_WEP, and normalized composition charges",
            "current_value": "TARGET_ONLY_alpha<=4.797780522732e-05_robust<=2.887280314062e-05",
            "provenance": "988::WEP988_WAS651_0_alpha_Coulomb; 989::BSO989_1/2",
            "current_status": "NUMERIC_TARGET_ONLY_NOT_DERIVED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "row_id": "LAM1397_6_R10_material_leg",
            "quantity": "R10_alpha_bulk_lambda_A_leg",
            "definition": "R10 material leg contribution sourced by finite lambda_A/alphaEM response",
            "formula": "alpha_bulk,ST(lambda) includes K_bulk_ST(lambda) beta_bulk,S beta_bulk,T + epsilon_tail",
            "units": "dimensionless Yukawa alpha(lambda)",
            "required_parent_input": "beta_EM(lambda_A), f_EM,S/T, K_bulk_ST(lambda), tail, and real bound curve",
            "current_value": "MISSING_R10_KERNEL_AND_BOUND_INPUTS",
            "provenance": "1392::bulk alpha template; 1396::BEM1396_4_R10_material_leg",
            "current_status": "R10_NOT_SCOREABLE",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "row_id": "LAM1397_7_lambdaA_verdict",
            "quantity": "lambda_A_fallback_status",
            "definition": "fallback state if unique Maxwell F2 cannot be proved",
            "formula": "retain lambda_A as explicit nonclaim source coefficient until forbidden or sourced",
            "units": "ledger status",
            "required_parent_input": "no MISSING markers across LAM1397_0 through LAM1397_6 before any score",
            "current_value": "LAMBDA_A_SOURCE_ROW_READY_NONCLAIM",
            "provenance": "1397 checkpoint",
            "current_status": "FINITE_ROUTE_EXPLICIT_SCORING_BLOCKED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def arena_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "LAG1397_0_EM_lock",
            "arena": "EM-lock theorem",
            "lambda_A_dependency": "unique F2 must set lambda_A=0 or forbid standalone F_Q^2",
            "current_blocker": "UMF1397_2 fails current corpus and UMF1397_3 is unsigned",
            "status": "BLOCKED_UNIQUE_F2_NOT_SIGNED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "LAG1397_1_alphaEM",
            "arena": "fine-structure/readout",
            "lambda_A_dependency": "b_alpha_EM depends on derivative of C_P N_Q + lambda_A plus readout factors",
            "current_blocker": "lambda_A and readout descent derivatives missing",
            "status": "BLOCKED_ALPHAEM_DERIVATIVE_OWNER_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "LAG1397_2_clock",
            "arena": "clock/fine-structure tests",
            "lambda_A_dependency": "clock constrains K_alpha b_alpha_EM tau_clock",
            "current_blocker": "only product-level clock constraint is present",
            "status": "BLOCKED_CLOCK_PRODUCT_ONLY",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "LAG1397_3_WEP",
            "arena": "WEP/Coulomb composition",
            "lambda_A_dependency": "WEP needs beta_source_alpha b_alpha_EM tau_WEP with normalized charges",
            "current_blocker": "source normalization owner and tau_WEP map missing",
            "status": "BLOCKED_WEP_SOURCE_MAP_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "LAG1397_4_R10",
            "arena": "R10 short-range alpha(lambda)",
            "lambda_A_dependency": "finite lambda_A feeds beta_EM then bulk material kernel",
            "current_blocker": "beta_EM map, K_bulk,ST(lambda), tail, and real bound curve not all claim-ready",
            "status": "BLOCKED_R10_MATERIAL_KERNEL_MISSING",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "LAG1397_5_local_GR",
            "arena": "local GR/Newton reduction",
            "lambda_A_dependency": "finite EM residual must vanish or be bounded as part of the local residual vector",
            "current_blocker": "R_EM_local incomplete and EM-lock not signed",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "LAG1397_6_verdict",
            "arena": "all alphaEM/local arenas",
            "lambda_A_dependency": "unique F2 proof or complete lambda_A finite source map",
            "current_blocker": "neither proof nor sourced finite map exists",
            "status": "ARENA_SCORING_BLOCKED",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "claim_id": "GATE1397_0_unique_F2",
            "claim": "unique Maxwell F2 is parent-proved",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "lambda_A F_Q^2 remains a legal invariant in current corpus",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1397_1_lambda_A_zero",
            "claim": "lambda_A=0",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "zero would require no-counterterm theorem, symmetry, or sourced parent coefficient",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1397_2_alphaEM_bound",
            "claim": "b_alpha_EM is bounded or zero",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "b_alpha_EM derivative map and tau/readout factors are missing",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1397_3_WEP_clock_R10",
            "claim": "WEP, clock, or R10 alphaEM branch passes",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "all three arenas still depend on missing source/tau/material maps",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "claim_id": "GATE1397_4_local_GR",
            "claim": "local GR/Newton reduction can be claimed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "1397 only isolates one EM coupling blocker and does not derive the local limit",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1397_0_proof_attempt",
            "decision": "do not promote unique Maxwell F2",
            "reason": "the standalone lambda_A F_Q^2 term is still invariant and not forbidden by a parent theorem",
            "consequence": "EM-lock remains conditional; beta_EM zero remains unsigned",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1397_1_fallback",
            "decision": "write lambda_A as an explicit source coefficient",
            "reason": "if it cannot be killed derivably, it must be visible in alphaEM/WEP/clock/R10/local gates",
            "consequence": "finite EM route is source-ready but nonclaim",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC1397_2_next",
            "decision": "attack the deeper no-observed-counterterm action principle",
            "reason": "that is the least-scrutiny route to killing lambda_A without fitting it",
            "consequence": "next target 1398 tries to prove no quotient-only counterterms or keeps lambda_A finite",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1397_0_1398",
            "target_doc": "1398-Y5-R10-RAB-no-observed-counterterm-action-principle-or-lambdaA-prior-bound.md",
            "target_script": "scripts/Y5_R10_RAB_no_observed_counterterm_action_principle_or_lambdaA_prior_bound.py",
            "task": "try to prove that the parent action forbids observed quotient-only counterterms like lambda_A F_Q^2; if it fails, turn lambda_A into a finite prior/bound coefficient across alphaEM gates",
            "success_condition": "either a parent-signed no-counterterm principle closes UMF1397_3 or lambda_A remains explicit as a nonclaim coefficient with no hidden EM-lock claim",
            "do_not_claim": "unique F2;lambda_A=0;alphaEM bound;WEP pass;clock pass;R10 pass;PPN pass;Newton limit;local GR;q_loc=0;GitHub-ready result",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: list[dict[str, str]],
    proof: list[dict[str, str]],
    lambda_rows: list[dict[str, str]],
    arenas: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "True" and row["anchor_found"] == "True" for row in sources)
    proof_has_failure = any(
        row["proof_id"] == "UMF1397_2_operator_basis_uniqueness"
        and row["current_status"] == "FAILS_CURRENT_CORPUS"
        for row in proof
    )
    proof_has_verdict = any(
        row["proof_id"] == "UMF1397_7_current_verdict"
        and row["current_status"] == "PROOF_FAILS_CURRENT_CORPUS_LAMBDA_A_SOURCE_ROW_REQUIRED"
        for row in proof
    )
    lambda_nonclaim = all(
        row["valid_for_claim"] == "False"
        and row["claim_allowed"] == "False"
        and row["current_status"] not in {"CLAIM_READY", "PASS", "PROMOTED"}
        for row in lambda_rows
    )
    lambda_has_missing = any("MISSING" in row["current_value"] or "TARGET_ONLY" in row["current_value"] for row in lambda_rows)
    arenas_blocked = all(
        row["claim_allowed"] == "False"
        and (row["status"].startswith("BLOCKED") or row["status"] == "ARENA_SCORING_BLOCKED")
        for row in arenas
    )
    gates_blocked = all(row["claim_allowed"] == "False" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    output_paths = [
        DOC_PATH,
        SOURCE_REGISTER_PATH,
        PROOF_AUDIT_PATH,
        LAMBDA_SOURCE_PATH,
        ARENA_GATE_PATH,
        CLAIM_GATE_PATH,
        DECISION_LEDGER_PATH,
        NEXT_TARGET_PATH,
        VALIDATION_PATH,
    ]
    scope_ok = all("formalization-workbench" not in str(ROOT / path) for path in output_paths)
    all_ok = (
        source_ok
        and proof_has_failure
        and proof_has_verdict
        and lambda_nonclaim
        and lambda_has_missing
        and arenas_blocked
        and gates_blocked
        and scope_ok
    )
    now = datetime.now(timezone.utc).isoformat()
    return [
        {
            "check_id": "VAL1397_0_sources",
            "status": "PASS" if source_ok else "FAIL",
            "detail": "all cited local source paths exist and anchors are present",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1397_1_unique_F2_proof",
            "status": "PASS" if proof_has_failure and proof_has_verdict else "FAIL",
            "detail": "proof attempt records exact conditional theorem but current corpus still fails unique F2",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1397_2_lambda_A_source_row",
            "status": "PASS" if lambda_nonclaim and lambda_has_missing else "FAIL",
            "detail": "lambda_A source rows are explicit, nonclaim, and retain missing parent inputs",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1397_3_arena_gates",
            "status": "PASS" if arenas_blocked else "FAIL",
            "detail": "alphaEM, WEP, clock, R10, and local gates remain blocked",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1397_4_claim_refusal",
            "status": "PASS" if gates_blocked else "FAIL",
            "detail": "unique F2, lambda_A zero, alphaEM bound, empirical, and local-GR claims all refused",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1397_5_scope",
            "status": "PASS" if scope_ok else "FAIL",
            "detail": "outputs are confined to post-checkpoint-work paths",
            "generated_utc": now,
        },
        {
            "check_id": "VAL1397_6_overall",
            "status": "PASS" if all_ok else "FAIL",
            "detail": "1397 turns unique F2 into a failed proof gate plus explicit lambda_A nonclaim source row",
            "generated_utc": now,
        },
    ]


def write_doc(
    sources: list[dict[str, str]],
    proof: list[dict[str, str]],
    lambda_rows: list[dict[str, str]],
    arenas: list[dict[str, str]],
    gates: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    body = f"""# 1397 Y5 R10 RAB: Unique Maxwell F2 Proof Or LambdaA Source Row

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

**Current verdict:** the clean unique-Maxwell-`F^2` route does not close in the current corpus. The exact theorem is sharp, but the standalone `lambda_A F_Q^2` counterterm is still a legal invariant unless a deeper parent no-counterterm principle forbids quotient-only appendages.

**Discipline move:** expose `lambda_A` as a finite nonclaim source coefficient. This prevents a fake EM-lock win: alphaEM, WEP, clocks, R10, and local-GR gates must now either kill `lambda_A` derivably or carry it visibly.

## Source Register

{md_table(sources)}

## Unique Maxwell `F^2` Proof Audit

{md_table(proof)}

## `lambda_A` Source Row

{md_table(lambda_rows)}

## AlphaEM / WEP / Clock / R10 / Local Gates

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
    proof = proof_audit_rows()
    lambda_rows = lambda_source_rows()
    arenas = arena_gate_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, proof, lambda_rows, arenas, gates)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(PROOF_AUDIT_PATH, proof)
    write_csv(LAMBDA_SOURCE_PATH, lambda_rows)
    write_csv(ARENA_GATE_PATH, arenas)
    write_csv(CLAIM_GATE_PATH, gates)
    write_csv(DECISION_LEDGER_PATH, decisions)
    write_csv(NEXT_TARGET_PATH, next_target)
    write_csv(VALIDATION_PATH, validation)
    write_doc(sources, proof, lambda_rows, arenas, gates, decisions, next_target, validation)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"1397 validation failed: {failed}")
    print(STATUS)
    print(ROOT / DOC_PATH)
    print(ROOT / VALIDATION_PATH)


if __name__ == "__main__":
    main()
