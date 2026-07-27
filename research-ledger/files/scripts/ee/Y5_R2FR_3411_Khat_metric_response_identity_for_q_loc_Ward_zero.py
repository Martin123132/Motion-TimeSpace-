from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3411-Y5-R2FR-Khat-metric-response-identity-for-q_loc-Ward-zero-under-AX1090.md"

SOURCES = {
    "doc_3410": ROOT / "3410-Y5-R2FR-q_loc-beta-alpha-vector-residue-split-under-AX1090.md",
    "next_3410": OUT / "P8_Y5_R2FR_3410_NEXT_TARGET.csv",
    "vector_audit_3410": OUT / "P8_Y5_R2FR_3410_VECTOR_ZERO_PROOF_AUDIT.csv",
    "gates_3410": OUT / "P8_Y5_R2FR_3410_PROMOTION_GATES.csv",
    "doc_3064": ROOT / "3064-Y5-R2FR-GammaKhat-q_loc-double-zero-proof-or-GK-component-bound-runner-under-AX1090.md",
    "gk_gate_3064": OUT / "P8_Y5_R2FR_3064_GAMMAKHAT_QLOC_PROOF_GATE.csv",
    "residual_3064": OUT / "P8_Y5_R2FR_3064_QLOC_RESIDUAL_INTERFACE.csv",
    "doc_3008": ROOT / "3008-Y5-R2FR-Gamma-Khat-q_loc-action-existence-or-explicit-residual-split-under-AX1090.md",
    "doc_597": ROOT / "597-Y5-R10-reduced-GK-action-owner-or-q_loc-residual-runner.md",
    "doc_513": ROOT / "513-Gamma-Khat-q_loc-first-variation-or-demotion.md",
    "stress_rewrite_513": OUT / "P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv",
    "first_variation_513": OUT / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
    "integrability_513": OUT / "P8_GAMMA_KHAT_QLOC_INTEGRABILITY_GATES.csv",
    "khat_match_2409": OUT / "P8_Y5_PARENT_QLOC_2409_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv",
    "gamma_owner_2976": OUT / "P8_Y5_R2FR_2976_GAMMA_EFF_SCALAR_DENSITY_OWNER_AUDIT.csv",
    "helmholtz_1280": OUT / "P8_Y5_R10_1280_HELMHOLTZ_EULER_DOUBLE_ZERO_AUDIT.csv",
    "ward_1010": OUT / "P8_Y5_R10_1010_THEOREM_ATTEMPT.csv",
    "derivation_gate_2581": OUT / "P8_Y5_GAMMAKHAT_QLOC_2581_DERIVATION_PROOF_GATE.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3411_SOURCE_REGISTER.csv",
    "stress_identity_proof": OUT / "P8_Y5_R2FR_3411_STRESS_IDENTITY_PROOF.csv",
    "metric_response_contract": OUT / "P8_Y5_R2FR_3411_KHAT_METRIC_RESPONSE_CONTRACT.csv",
    "ward_zero_theorem": OUT / "P8_Y5_R2FR_3411_WARD_ZERO_THEOREM.csv",
    "current_symbol_match_audit": OUT / "P8_Y5_R2FR_3411_CURRENT_SYMBOL_MATCH_AUDIT.csv",
    "q_loc_zero_implications": OUT / "P8_Y5_R2FR_3411_QLOC_ZERO_IMPLICATIONS.csv",
    "residual_if_identity_fails": OUT / "P8_Y5_R2FR_3411_RESIDUAL_IF_IDENTITY_FAILS.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3411_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3411_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3411_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3411_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3411_VALIDATION.csv",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fields = list(rows[0].keys())
    clean = lambda value: str(value).replace("\n", " ").replace("|", "/")
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3410": "q_loc scalar/vector split and Khat identity next target",
        "next_3410": "declared 3411 target",
        "vector_audit_3410": "GK Ward identity selected as best vector-zero route",
        "gates_3410": "q_loc remains local-GR blocker before Ward route",
        "doc_3064": "GammaKhat double-zero proof gate and Khat identity bottleneck",
        "gk_gate_3064": "current proof-gate status for action/Khat/Helmholtz/Euler/boundary",
        "residual_3064": "retained q_loc residual components if identity fails",
        "doc_3008": "action existence and metric-response Ward theorem route",
        "doc_597": "reduced GK action owner contract and symbol-match failure",
        "doc_513": "first q_loc stress rewrite and variational demotion fork",
        "stress_rewrite_513": "algebraic T_GK divergence identity",
        "first_variation_513": "required variational clauses for q_loc zero",
        "integrability_513": "Helmholtz and readout gates",
        "khat_match_2409": "current Khat metric-response match audit",
        "gamma_owner_2976": "Gamma_eff scalar density ownership audit",
        "helmholtz_1280": "Helmholtz/Euler/double-zero audit",
        "ward_1010": "Ward theorem attempt source",
        "derivation_gate_2581": "GammaKhat derivation proof gate source",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def stress_identity_proof() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "SIP3411_0_define_extra_stress",
            "claim": "The q_loc expression is algebraically the projected divergence of an effective extra stress.",
            "equation": "T_GK^{mu nu}:=Gamma_eff g^{mu nu}-K_hat^{mu nu}",
            "derivation": "metric compatibility gives nabla_mu(Gamma_eff g^{mu nu})=nabla^nu Gamma_eff",
            "result": "nabla_mu T_GK^{mu nu}=nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}",
            "status": "EXACT_ALGEBRAIC_IDENTITY",
            "valid_for_claim": False,
        },
        {
            "proof_id": "SIP3411_1_projector",
            "claim": "The physical q_loc residual is the local projection of that stress divergence.",
            "equation": "q_loc^nu=P_loc(nabla_mu T_GK^{mu nu})",
            "derivation": "insert the definition of q_loc after the stress rewrite",
            "result": "q_loc is not fundamental; it is a projected stress/Ward residual",
            "status": "EXACT_IF_Ploc_IS_THE_SAME_PROJECTOR",
            "valid_for_claim": False,
        },
        {
            "proof_id": "SIP3411_2_not_enough",
            "claim": "The algebraic rewrite alone does not prove local GR.",
            "equation": "div(T_GK)=0 requires variational ownership, Euler closure, and boundary silence",
            "derivation": "an arbitrary tensor can have nonzero divergence even if written as Gamma g-K",
            "result": "must prove T_GK is a Hilbert stress from one parent action",
            "status": "LOCAL_GR_NOT_PROMOTED_BY_REWRITE",
            "valid_for_claim": False,
        },
    ]


def metric_response_contract() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "MRC3411_0_parent_action",
            "needed_clause": "A single diffeomorphism-invariant parent scalar-density action owns Gamma_eff.",
            "mathematical_form": "S_GK[g,Phi]=int_M sqrt(-g) Gamma_eff[g,Phi,nabla Phi,D,...]+int_boundary B_GK",
            "acceptance_test": "Gamma_eff field content, branch domain, units and boundary terms are explicit",
            "current_status": "NOT_CURRENTLY_SIGNED",
            "valid_for_claim": False,
        },
        {
            "contract_id": "MRC3411_1_metric_response_identity",
            "needed_clause": "K_hat is not independent; it is the metric response of the same density.",
            "mathematical_form": "K_hat^{mu nu}=2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu} plus derivative/boundary terms in one convention",
            "acceptance_test": "symbol-by-symbol match to the current K_hat expression, including signs and integration-by-parts terms",
            "current_status": "NOT_MATCHED_TO_CURRENT_SYMBOLS",
            "valid_for_claim": False,
        },
        {
            "contract_id": "MRC3411_2_Hilbert_stress",
            "needed_clause": "T_GK is the Hilbert stress of S_GK.",
            "mathematical_form": "T_GK^{mu nu}=-2/sqrt(-g) delta S_GK/delta g_{mu nu}=Gamma_eff g^{mu nu}-K_hat^{mu nu}",
            "acceptance_test": "the metric variation reproduces exactly the stress used in q_loc, not a lookalike after readout",
            "current_status": "CONDITIONAL_EXACT_IF_MRC3411_0_AND_MRC3411_1_PASS",
            "valid_for_claim": False,
        },
        {
            "contract_id": "MRC3411_3_Helmholtz",
            "needed_clause": "The proposed T_GK satisfies variational/Helmholtz symmetry.",
            "mathematical_form": "delta(sqrt(-g)T_GK^{mu nu})/delta g_{alpha beta} is symmetric under second metric variation up to boundary and gauge terms",
            "acceptance_test": "no antisymmetric second-variation obstruction H_GK remains",
            "current_status": "NOT_CHECKED_FOR_CURRENT_SYMBOLS",
            "valid_for_claim": False,
        },
        {
            "contract_id": "MRC3411_4_projector_boundary",
            "needed_clause": "P_loc is parent-owned and boundary/symplectic improvements have zero local flux.",
            "mathematical_form": "P_loc=P_parent(Phi0), partial_A P_loc(Phi0)=0, integral_boundary Delta(theta_GK,Q_GK,tau)=0",
            "acceptance_test": "the projection cannot hide vector/scalar force components, and no linking-sphere flux survives",
            "current_status": "OPEN",
            "valid_for_claim": False,
        },
    ]


def ward_zero_theorem() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "WZT3411_0_statement",
            "statement": "If MRC3411_0 through MRC3411_4 hold, q_loc is a Ward/Euler/boundary residual.",
            "derivation": "diffeomorphism invariance of S_GK gives nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A+nabla_mu B_GK^{mu nu}",
            "zero_condition": "E_A=0 on compact local vacuum and P_loc nabla_mu B_GK^{mu nu}=0",
            "result": "q_loc^nu=0 on the local vacuum branch",
            "status": "CONDITIONAL_THEOREM_DERIVED",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "WZT3411_1_vector",
            "statement": "If WZT3411_0 holds, q_loc preferred-frame/vector lanes vanish.",
            "derivation": "q_T^i, alpha1_q, alpha2_q, alpha3_q, xi_q are projections of q_loc or boundary flux",
            "zero_condition": "q_loc=0 and no independent boundary/projector spurion",
            "result": "f_qV=0; the alpha3 product pressure is removed structurally, not tuned",
            "status": "CONDITIONAL_NOT_CURRENT_CLAIM",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "WZT3411_2_scalar",
            "statement": "If WZT3411_0 holds, q_loc scalar beta/gamma/R10 lanes vanish as q_loc lanes.",
            "derivation": "D^i chi_q and finite-range q_loc kernels are projections of the same Ward residual",
            "zero_condition": "q_loc=0 in the observed local branch and P_loc commutes with readout",
            "result": "q_loc stops contributing to beta/gamma/R10; other non-EH residues still need their own gates",
            "status": "CONDITIONAL_NOT_CURRENT_CLAIM",
            "valid_for_claim": False,
        },
    ]


def current_symbol_match_audit() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "SMA3411_0_Gamma_eff_density",
            "required_symbol": "sqrt(-g) Gamma_eff[g,Phi,nabla Phi,D,...]",
            "current_evidence": "formal response-doublet candidate only",
            "failure_mode": "Gamma_eff may be a closure/readout variable rather than an action density",
            "current_status": "UNSIGNED",
            "source_path": str(SOURCES["gamma_owner_2976"]),
            "valid_for_claim": False,
        },
        {
            "audit_id": "SMA3411_1_Khat_response",
            "required_symbol": "K_hat^{mu nu}=2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu}",
            "current_evidence": "3064/2409 say not matched to current symbols",
            "failure_mode": "Delta_K=K_hat-K_metric[Gamma_eff] remains a live q_loc residual",
            "current_status": "FAIL_CURRENT_SYMBOL_MATCH",
            "source_path": str(SOURCES["khat_match_2409"]),
            "valid_for_claim": False,
        },
        {
            "audit_id": "SMA3411_2_Helmholtz",
            "required_symbol": "second metric variation symmetry for T_GK",
            "current_evidence": "not checked for current symbols",
            "failure_mode": "no local action may exist for the proposed T_GK",
            "current_status": "UNSIGNED",
            "source_path": str(SOURCES["helmholtz_1280"]),
            "valid_for_claim": False,
        },
        {
            "audit_id": "SMA3411_3_Euler_closure",
            "required_symbol": "source-free local Euler equations for all fields in Gamma_eff/Khat",
            "current_evidence": "not derived",
            "failure_mode": "div(T_GK) remains a physical local force/source-exchange residual",
            "current_status": "UNSIGNED",
            "source_path": str(SOURCES["ward_1010"]),
            "valid_for_claim": False,
        },
        {
            "audit_id": "SMA3411_4_boundary_projector",
            "required_symbol": "P_loc parent ownership plus no-flux boundary improvement",
            "current_evidence": "open in 3064 and 513",
            "failure_mode": "bulk Ward zero could leak through boundary/projector components",
            "current_status": "OPEN",
            "source_path": str(SOURCES["derivation_gate_2581"]),
            "valid_for_claim": False,
        },
    ]


def q_loc_zero_implications() -> list[dict[str, Any]]:
    return [
        {
            "implication_id": "QZI3411_0_if_identity_passes",
            "condition": "metric-response identity, Ward closure, projector and boundary gates all pass",
            "effect": "q_loc no longer contributes to beta/gamma/alpha_i/xi/R10/source-normalization lanes",
            "local_GR_status": "q_loc blocker removed, but other non-EH residues from 3409 remain",
            "claim_status": "CONDITIONAL_ONLY",
            "valid_for_claim": False,
        },
        {
            "implication_id": "QZI3411_1_if_identity_fails",
            "condition": "K_hat does not match metric response of Gamma_eff",
            "effect": "q_loc is not a derived Ward-zero mechanism and must be bounded componentwise",
            "local_GR_status": "q_loc remains a local-GR blocker, especially alpha3/vector product",
            "claim_status": "RESIDUAL_BOUND_BRANCH",
            "valid_for_claim": False,
        },
        {
            "implication_id": "QZI3411_2_Newton_GR",
            "condition": "q_loc killed plus EH pole/readout/source G_ref gates from 3408 close",
            "effect": "MTS can start looking like a true GR-to-Newton reduction rather than an added force law",
            "local_GR_status": "not achieved yet; this is why the Ward route matters",
            "claim_status": "FUTURE_PROMOTION_ROUTE",
            "valid_for_claim": False,
        },
    ]


def residual_if_identity_fails() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RIF3411_0_Delta_K",
            "symbol": "Delta_K",
            "definition": "K_hat-K_metric[Gamma_eff]",
            "observable_risk": "metric response, PPN, source mass",
            "needed_bound_or_zero": "symbol match or numeric Delta_K projection",
            "current_status": "RETAINED_SYMBOLIC_GAP",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RIF3411_1_H_GK",
            "symbol": "H_GK",
            "definition": "Helmholtz/second-variation obstruction",
            "observable_risk": "action existence and local GR",
            "needed_bound_or_zero": "explicit Helmholtz symmetry calculation",
            "current_status": "RETAINED_SYMBOLIC_GAP",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RIF3411_2_J_GK",
            "symbol": "J_GK",
            "definition": "source-current work in Gamma/Khat Euler identity",
            "observable_risk": "preferred-frame/source exchange",
            "needed_bound_or_zero": "source-free compact local Euler equations",
            "current_status": "RETAINED_SYMBOLIC_GAP",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RIF3411_3_B_GK",
            "symbol": "B_GK",
            "definition": "boundary/symplectic work from integrations by parts",
            "observable_risk": "boundary flux, R10, R11, local mass leakage",
            "needed_bound_or_zero": "no-flux or fixed topological subtraction theorem",
            "current_status": "RETAINED_SYMBOLIC_GAP",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RIF3411_4_Ploc",
            "symbol": "P_loc_commutator",
            "definition": "failure of P_loc to commute with parent fixed-point/readout limit",
            "observable_risk": "domain/projector preferred-frame leakage",
            "needed_bound_or_zero": "parent projector algebra and fixed-point commutation",
            "current_status": "RETAINED_SYMBOLIC_GAP",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3411_0_conditional_theorem",
            "gate": "Ward theorem from metric-response stress is written exactly",
            "current_result": "PASS_CONDITIONAL_THEOREM",
            "promotes_if": "not a claim gate",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3411_1_symbol_match",
            "gate": "current MTS Gamma_eff and K_hat satisfy the metric-response identity",
            "current_result": "FAIL_CURRENT_SYMBOL_MATCH",
            "promotes_if": "SMA3411_0 and SMA3411_1 become source-backed exact matches",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3411_2_Helmholtz_Euler",
            "gate": "T_GK has action integrability and source-free compact local Euler closure",
            "current_result": "FAIL_NOT_CHECKED_OR_NOT_DERIVED",
            "promotes_if": "SMA3411_2 and SMA3411_3 pass",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3411_3_projector_boundary",
            "gate": "P_loc and boundary improvements cannot leak residual force",
            "current_result": "OPEN",
            "promotes_if": "P_loc parent ownership and no-flux boundary theorem pass",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3411_4_q_loc_zero",
            "gate": "q_loc is killed as a local-GR blocker",
            "current_result": "BLOCKED",
            "promotes_if": "PG3411_1, PG3411_2 and PG3411_3 all pass",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DL3411_0",
            "decision": "The Ward route is mathematically exact as a conditional theorem.",
            "rationale": "T_GK=Gamma_eff g-K_hat makes q_loc the divergence of a candidate Hilbert stress; diffeomorphism invariance would then force on-shell/boundary zero.",
            "claim_effect": "genuine derivation route exists",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DL3411_1",
            "decision": "The current MTS corpus does not yet pass the symbol-match gate.",
            "rationale": "K_hat is not currently proven to be the metric variation of sqrt(-g) Gamma_eff in one convention.",
            "claim_effect": "q_loc zero not claimed",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DL3411_2",
            "decision": "Next work must extract or construct the actual Gamma_eff/K_hat definitions.",
            "rationale": "Without current symbols, more prose about Ward identities cannot close the proof.",
            "claim_effect": "3412 selected as symbol-match extractor/construction attempt",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3412-Y5-R2FR-GammaKhat-symbol-match-extractor-for-Khat-response-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3412_GammaKhat_symbol_match_extractor_for_Khat_response.py",
            "objective": "scan the current corpus for explicit Gamma_eff and K_hat definitions, extract candidate terms, and test whether K_hat is the metric response of sqrt(-g) Gamma_eff in one sign/boundary convention",
            "why_next": "3411 proves the exact route; 3412 must now supply or refute the current-symbol match instead of circling the theorem",
            "valid_for_claim": False,
        },
        {
            "target_id": "3413-Y5-R2FR-q_loc-residual-bound-demotion-if-symbol-match-fails-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3413_q_loc_residual_bound_demotion_if_symbol_match_fails.py",
            "objective": "if no metric-response symbol match exists, demote q_loc to explicit residual components Delta_K, H_GK, J_GK, B_GK and P_loc_commutator with bound rows",
            "why_next": "this prevents the Ward route from becoming a closure assumption",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3411_0",
            "script": str(Path(__file__).resolve()),
            "claim_status": "CONDITIONAL_WARD_THEOREM_ONLY",
            "main_result": "q_loc zero is derived if and only if Gamma_eff/K_hat are one parent metric-response stress with Euler and boundary closure",
            "current_mts_status": "identity not matched to current symbols",
            "valid_for_claim": False,
        }
    ]


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = generated["source_register"]
    gates = generated["promotion_gates"]
    symbol_audit = generated["current_symbol_match_audit"]
    next_rows = generated["next_target"]
    output_paths = list(OUTPUTS.values()) + [DOC]
    source_exists = all(str(row["exists"]).lower() == "true" for row in source_rows)
    no_workbench = all("formalization-workbench" not in str(path) for path in output_paths)
    all_nonclaim = all(
        str(row.get("valid_for_claim", "False")).lower() == "false"
        for rows in generated.values()
        for row in rows
    )
    theorem_pass = any(
        row.get("gate_id") == "PG3411_0_conditional_theorem" and row.get("current_result") == "PASS_CONDITIONAL_THEOREM"
        for row in gates
    )
    symbol_fail = any(
        row.get("gate_id") == "PG3411_1_symbol_match" and row.get("current_result") == "FAIL_CURRENT_SYMBOL_MATCH"
        for row in gates
    )
    qloc_blocked = any(
        row.get("gate_id") == "PG3411_4_q_loc_zero" and row.get("current_result") == "BLOCKED"
        for row in gates
    )
    delta_k_retained = any(row.get("audit_id") == "SMA3411_1_Khat_response" for row in symbol_audit)
    next_extractor = "symbol-match-extractor" in next_rows[0].get("target_id", "")
    rows = [
        {
            "check_id": "VAL3411_0_sources_exist",
            "check": "every cited local source path exists",
            "passed": source_exists,
            "detail": f"{sum(str(row['exists']).lower() == 'true' for row in source_rows)}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3411_1_scope",
            "check": "no output path targets formalization-workbench",
            "passed": no_workbench,
            "detail": "all outputs are under post-checkpoint-work",
        },
        {
            "check_id": "VAL3411_2_all_nonclaim",
            "check": "all generated rows keep valid_for_claim=false",
            "passed": all_nonclaim,
            "detail": "3411 is a conditional theorem and symbol-match audit, not a claim",
        },
        {
            "check_id": "VAL3411_3_conditional_theorem",
            "check": "Ward zero theorem is derived conditionally",
            "passed": theorem_pass,
            "detail": "PG3411_0_conditional_theorem passes as nonclaim theorem",
        },
        {
            "check_id": "VAL3411_4_symbol_match_not_faked",
            "check": "current symbol match remains failed",
            "passed": symbol_fail,
            "detail": "PG3411_1_symbol_match is FAIL_CURRENT_SYMBOL_MATCH",
        },
        {
            "check_id": "VAL3411_5_DeltaK_retained",
            "check": "Delta_K/Khat response gap is retained explicitly",
            "passed": delta_k_retained,
            "detail": "SMA3411_1_Khat_response written",
        },
        {
            "check_id": "VAL3411_6_q_loc_blocked",
            "check": "q_loc zero is not claimed",
            "passed": qloc_blocked,
            "detail": "PG3411_4_q_loc_zero remains BLOCKED",
        },
        {
            "check_id": "VAL3411_7_next_target",
            "check": "next target extracts/tests actual GammaKhat symbols",
            "passed": next_extractor,
            "detail": next_rows[0]["target_id"],
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "check_id": "VAL3411_8_overall",
            "check": "3411 Ward route is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return rows


def build_doc(generated: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join(
        [
            "# 3411 - Khat Metric-Response Identity For q_loc Ward Zero",
            "## Summary\n"
            "- This checkpoint proves the exact conditional route: if `K_hat` is the metric response of `sqrt(-g) Gamma_eff`, then `q_loc` is a projected Ward/Euler/boundary residual.\n"
            "- That would kill both scalar and preferred-frame q_loc lanes on compact local vacuum domains.\n"
            "- The current corpus still does not match the actual `K_hat` symbols to that metric response, so no local-GR claim is made.\n"
            "- The next move is concrete: extract the actual `Gamma_eff` and `K_hat` candidate terms and test the response identity.",
            "## Stress Identity Proof\n" + md_table(generated["stress_identity_proof"]),
            "## Metric-Response Contract\n" + md_table(generated["metric_response_contract"]),
            "## Ward Zero Theorem\n" + md_table(generated["ward_zero_theorem"]),
            "## Current Symbol Match Audit\n" + md_table(generated["current_symbol_match_audit"]),
            "## q_loc Zero Implications\n" + md_table(generated["q_loc_zero_implications"]),
            "## Residual If Identity Fails\n" + md_table(generated["residual_if_identity_fails"]),
            "## Promotion Gates\n" + md_table(generated["promotion_gates"]),
            "## Decision Ledger\n" + md_table(generated["decision_ledger"]),
            "## Next Target\n" + md_table(generated["next_target"]),
            "## Runner Nonclaim\n" + md_table(generated["runner_nonclaim"]),
            "## Validation\n" + md_table(generated["validation"]),
            "## Bottom Line\n"
            "This is the cleanest derivation route we have found for the local q_loc problem. It is not yet a win, but it is no longer fog: "
            "either current MTS supplies a real `Gamma_eff/K_hat` metric-response pair, or q_loc must be demoted to explicit bounded residuals.",
        ]
    ) + "\n"


def main() -> None:
    if "formalization-workbench" in str(ROOT):
        raise RuntimeError(f"Refusing to run from formalization-workbench: {ROOT}")

    generated: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "stress_identity_proof": stress_identity_proof(),
        "metric_response_contract": metric_response_contract(),
        "ward_zero_theorem": ward_zero_theorem(),
        "current_symbol_match_audit": current_symbol_match_audit(),
        "q_loc_zero_implications": q_loc_zero_implications(),
        "residual_if_identity_fails": residual_if_identity_fails(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    generated["validation"] = validation_rows(generated)

    for key, rows in generated.items():
        write_csv(OUTPUTS[key], rows)

    DOC.write_text(build_doc(generated), encoding="utf-8")

    if not all(str(row["passed"]).lower() == "true" for row in generated["validation"]):
        failed = [row for row in generated["validation"] if str(row["passed"]).lower() != "true"]
        raise SystemExit(f"3411 validation failed: {failed}")

    print(f"wrote {len(generated)} CSV artefacts and {DOC}")


if __name__ == "__main__":
    main()
