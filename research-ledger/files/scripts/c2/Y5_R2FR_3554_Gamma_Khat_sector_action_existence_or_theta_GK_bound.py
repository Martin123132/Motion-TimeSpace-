from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3554-Y5-R2FR-Gamma-Khat-sector-action-existence-or-theta-GK-bound.md"
CANONICAL_STATUS = OUT / "P8_Y5_Gamma_Khat_action_existence_theta_GK_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3554": {"path": Path(__file__).resolve(), "role": "3554 generator"},
    "doc_3553": {
        "path": ROOT / "3553-Y5-R2FR-parent-sector-current-chain-theta-source-pack.md",
        "role": "theta sector pack handoff",
    },
    "next_3553": {
        "path": OUT / "P8_Y5_R2FR_3553_NEXT_TARGET.csv",
        "role": "3553 selected Gamma/Khat target",
    },
    "theta_sector_3553": {
        "path": OUT / "P8_Y5_R2FR_3553_SECTOR_THETA_SOURCE_PACK.csv",
        "role": "Gamma/Khat theta slot",
    },
    "theta_leak_3553": {
        "path": OUT / "P8_Y5_R2FR_3553_THETA_LEAKAGE_VECTOR.csv",
        "role": "theta_MTS leakage vector",
    },
    "doc_1010": {
        "path": ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
        "role": "prior Gamma/Khat action-existence checkpoint",
    },
    "gk_first_variation": {
        "path": OUT / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
        "role": "Gamma/Khat/q_loc first-variation contract",
    },
    "gk_candidates": {
        "path": OUT / "P8_GK_STRESS_ACTION_CANDIDATES.csv",
        "role": "candidate S_GK action routes",
    },
    "gk_gate_tests": {
        "path": OUT / "P8_GK_STRESS_ACTION_GATE_TESTS.csv",
        "role": "GK action gate tests",
    },
    "metric_response_contract": {
        "path": OUT / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
        "role": "metric response contract",
    },
    "metric_response_audit": {
        "path": OUT / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
        "role": "metric response match audit",
    },
    "metric_response_pass_fail": {
        "path": OUT / "P8_GK_METRIC_RESPONSE_PASS_FAIL.csv",
        "role": "metric response pass/fail ledger",
    },
    "gamma_owner_candidates": {
        "path": OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
        "role": "Gamma owner candidate actions",
    },
    "gamma_owner_decision": {
        "path": OUT / "P8_GAMMA_OWNER_OR_QLOC_BOUND_DECISION.csv",
        "role": "Gamma owner or q_loc bound decision",
    },
    "gamma_owner_tests": {
        "path": OUT / "P8_GAMMA_OWNER_OR_QLOC_BOUND_FORK_TESTS.csv",
        "role": "Gamma owner fork tests",
    },
    "response_doublet_contract": {
        "path": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
        "role": "response doublet action contract",
    },
    "response_doublet_variation": {
        "path": OUT / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
        "role": "response doublet variation ledger",
    },
    "local_residual_vector": {
        "path": OUT / "P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv",
        "role": "local GR residual vector map",
    },
    "yloc_noether": {
        "path": OUT / "P8_YLOC_SOURCE_CURRENT_NOETHER_AUDIT.csv",
        "role": "Noether alone not zero theorem",
    },
    "first_variation_gates": {
        "path": OUT / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv",
        "role": "first-variation symbol gates",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv_rows(path)
    except (csv.Error, OSError, UnicodeDecodeError):
        return False
    return True


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    divider = "| " + " | ".join("---" for _ in fields) + " |"
    body = [
        "| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "GK3554_0_variational_stress_route",
            "claim_piece": "S_GK action owner",
            "statement": "If S_GK[g,Phi] is a local diffeomorphism-invariant scalar action, then delta S_GK=E_A delta Phi^A + 1/2 sqrt(-g) T_GK^{mu nu} delta g_{mu nu} + d theta_GK.",
            "proof_step": "This supplies theta_GK and the Hilbert stress of the Gamma/Khat sector from one parent object.",
            "condition_needed": "explicit scalar density, field list, variation variables, boundary terms and fixed sign convention.",
            "current_status": "EXACT_FORMULA_ACTION_NOT_SUPPLIED",
            "source_path": str(SOURCES["gk_first_variation"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "GK3554_1_metric_response_identity",
            "claim_piece": "q_loc stress divergence",
            "statement": "If T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_hat^{mu nu}, then q_loc^nu=P_loc(nabla_mu T_GK^{mu nu}).",
            "proof_step": "Metric compatibility gives nabla_mu(Gamma_eff g^{mu nu}-K_hat^{mu nu})=nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}.",
            "condition_needed": "K_hat must equal the metric response of sqrt(-g) Gamma_eff including derivative and boundary terms.",
            "current_status": "EXACT_IDENTITY_IF_MATCHED_NOT_LIVE",
            "source_path": str(SOURCES["metric_response_contract"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "GK3554_2_Ward_Euler_zero",
            "claim_piece": "q_loc zero theorem",
            "statement": "For diffeomorphism-invariant S_GK, nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A plus boundary/source terms; if E_A=0 and boundary/source terms vanish, q_loc^nu=0.",
            "proof_step": "The local force becomes an on-shell Ward/Euler residual rather than a plateau axiom.",
            "condition_needed": "Euler closure, source-current zero, boundary no-flux and P_loc ownership.",
            "current_status": "EXACT_CONDITIONAL_THEOREM_UNSIGNED",
            "source_path": str(SOURCES["yloc_noether"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "GK3554_3_Helmholtz_gate",
            "claim_piece": "action-existence test",
            "statement": "A proposed T_GK is action-derived only if its metric second variation satisfies Helmholtz symmetry up to fixed boundary terms.",
            "proof_step": "delta(sqrt(-g)T_GK^{mu nu})/delta g_{alpha beta} must have the symmetric second-variation structure of an action Hessian.",
            "condition_needed": "explicit T_GK formula, metric dependence, boundary variable domain and gauge constraints.",
            "current_status": "NOT_CHECKED_CURRENT_CLAIM",
            "source_path": str(SOURCES["gk_first_variation"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "GK3554_4_double_zero",
            "claim_piece": "local PPN/source silence",
            "statement": "If T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0 after constant-background subtraction, the GK sector has no linear local PPN/source-normalization hair.",
            "proof_step": "The first surviving local source stress is second order in the local residual amplitude.",
            "condition_needed": "Gamma/Khat fixed-point expansion, physical local branch Phi0, source-current zero and boundary no-flux.",
            "current_status": "CONDITIONAL_SHAPE_NOT_MTS_PROMOTED",
            "source_path": str(SOURCES["response_doublet_variation"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GKG3554_0_action_existence",
            "gate": "S_GK exists",
            "required": "local diffeomorphism-invariant scalar action S_GK[g,Phi] with declared units and no readout fitting",
            "current_evidence": "contract exists; no accepted parent action source for current MTS",
            "status": "NOT_SUPPLIED",
            "if_fail": "Gamma/Khat are bookkeeping and theta_GK is retained",
            "source_path": str(SOURCES["gk_first_variation"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GKG3554_1_metric_response",
            "gate": "K_hat metric response",
            "required": "K_hat equals metric variation of sqrt(-g) Gamma_eff under fixed convention",
            "current_evidence": "515 audit found no current derivation as delta[sqrt(-g)Gamma_eff]/delta g",
            "status": "FAIL_CURRENT_CLAIM",
            "if_fail": "Delta_K enters q_loc and PPN/source-normalization rows",
            "source_path": str(SOURCES["metric_response_audit"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GKG3554_2_Helmholtz",
            "gate": "variational integrability",
            "required": "symmetric second variation of proposed stress up to boundary terms",
            "current_evidence": "1010/513 mark Helmholtz not checked",
            "status": "NOT_CHECKED",
            "if_fail": "no action exists for the claimed stress",
            "source_path": str(SOURCES["doc_1010"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GKG3554_3_Euler_closure",
            "gate": "local Euler/source-current zero",
            "required": "fields building Gamma/Khat obey source-free local Euler equations and no retained source current",
            "current_evidence": "Noether audits provide ownership discipline, not zero-current theorem",
            "status": "UNSIGNED",
            "if_fail": "q_loc is physical local force/source-exchange residual",
            "source_path": str(SOURCES["yloc_noether"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GKG3554_4_double_zero",
            "gate": "T_GK and first variation vanish",
            "required": "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0 after constant subtraction",
            "current_evidence": "response-doublet candidate gives shape conditionally; not matched to full MTS sector",
            "status": "CONDITIONAL_NOT_PROMOTED",
            "if_fail": "linear PPN/fifth-force/source-normalization hair remains",
            "source_path": str(SOURCES["response_doublet_variation"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GKG3554_5_projector_boundary",
            "gate": "P_loc and boundary no-flux",
            "required": "P_loc is parent-owned and boundary/symplectic terms carry no extra force or mass flux",
            "current_evidence": "513/1010 keep projector ownership and boundary no-flux open",
            "status": "OPEN",
            "if_fail": "projection or boundary can hide/tune force components",
            "source_path": str(SOURCES["doc_1010"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GKG3554_6_units_readout",
            "gate": "units and observable projection",
            "required": "Gamma_eff/K_hat/q_loc normalized into local PPN, source-normalization, clock/orbital units",
            "current_evidence": "515 says current Gamma/Khat appearances are symbolic without unit-normalized stress/readout map",
            "status": "FAIL_CURRENT_CLAIM",
            "if_fail": "residual branch cannot score; remains symbolic nonclaim",
            "source_path": str(SOURCES["metric_response_audit"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "GKC3554_0_metric_response_scalar_density",
            "candidate": "S_GK=-int sqrt(-g) Gamma_eff",
            "why_promising": "would make Gamma_eff and K_hat one variational object and turn q_loc into stress divergence",
            "missing": "MISSING_GAMMA_SCALAR_DENSITY_OWNER; MISSING_KHAT_METRIC_RESPONSE_MATCH; MISSING_HELMHOLTZ_CHECK",
            "status": "BEST_CONTRACT_NOT_MATCHED",
            "source_path": str(SOURCES["gk_candidates"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "GKC3554_1_response_doublet_even_density",
            "candidate": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "why_promising": "even exchange-odd response doublet gives double-zero shape and local first-variation silence at Z=0",
            "missing": "MISSING_COMPONENT_MAP; MISSING_POSITIVE_OPERATOR_OWNER; MISSING_SOURCE_CURRENT_ZERO; MISSING_BOUNDARY_NO_FLUX",
            "status": "BEST_THEORY_ROUTE_CONDITIONAL",
            "source_path": str(SOURCES["gamma_owner_candidates"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "GKC3554_2_positive_auxiliary_energy",
            "candidate": "positive auxiliary local-silence fields Phi^A with V(Phi) and G_AB nabla Phi nabla Phi",
            "why_promising": "positive operator can force Phi=Phi0 under source-free/no-boundary conditions",
            "missing": "MISSING_SOURCE_CURRENT_ZERO; MISSING_OPERATOR_SPECTRUM; MISSING_SYMBOL_MATCH_TO_GAMMA_KHAT",
            "status": "CANDIDATE_NEEDS_SYMBOL_MATCH",
            "source_path": str(SOURCES["gk_candidates"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "GKC3554_3_topological_exact_sector",
            "candidate": "Gamma/Khat contribution is exact/topological or fixed boundary density",
            "why_promising": "can be bulk force-free without propagating local fields",
            "missing": "MISSING_BOUNDARY_FLUX_ZERO; MISSING_CHARGE_UNITS; MISSING_FIXED_TOPOLOGICAL_CLASS",
            "status": "BOUNDARY_FLUX_RISK_OPEN",
            "source_path": str(SOURCES["gamma_owner_candidates"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "candidate_id": "GKC3554_4_residual_branch",
            "candidate": "retain q_loc/theta_GK/T_GK as explicit residuals",
            "why_promising": "keeps local-GR/PPN/source testing honest if derivation fails",
            "missing": "MISSING_NUMERIC_OR_THEOREM_ZERO_OBSERVABLE_PROJECTION",
            "status": "FALLBACK_REQUIRED",
            "source_path": str(SOURCES["local_residual_vector"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def leakage_rows() -> list[dict[str, Any]]:
    return [
        {
            "leak_id": "GKL3554_0_theta_GK",
            "quantity": "theta_GK",
            "formula": "delta S_GK = E_A delta Phi^A + 1/2 sqrt(-g)T_GK^{mu nu}delta g_{mu nu}+d theta_GK",
            "non_cancellation_bound": "|i_tau Delta theta_GK| retained independently inside Delta theta_MTS",
            "needed_inputs": "S_GK action, field list, boundary terms, first variation, tau action and units",
            "current_value": "MISSING_THETA_GK_ACTION_EXISTENCE",
            "units": "Hamiltonian charge variation density",
            "arena": "D_X H_tau; H_tau integrability; local GR residuals",
            "source_path": str(SOURCES["theta_leak_3553"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "leak_id": "GKL3554_1_metric_response_gap",
            "quantity": "Delta_K",
            "formula": "Delta_K^{mu nu}:=K_hat^{mu nu}-K_metric^{mu nu}[Gamma_eff]",
            "non_cancellation_bound": "|P_loc nabla_mu Delta_K^{mu nu}| retained independently",
            "needed_inputs": "Gamma_eff scalar density and metric response calculation including derivative/boundary terms",
            "current_value": "MISSING_KHAT_METRIC_RESPONSE_MATCH",
            "units": "projected force density or normalized local residual",
            "arena": "q_loc; PPN alpha_i/xi; source normalization R11",
            "source_path": str(SOURCES["metric_response_audit"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "leak_id": "GKL3554_2_Helmholtz_obstruction",
            "quantity": "H_GK",
            "formula": "H_GK := antisymmetric second-variation obstruction of sqrt(-g)T_GK",
            "non_cancellation_bound": "|H_GK| retained independently; if nonzero no S_GK claim",
            "needed_inputs": "explicit T_GK(g,Phi) and second variation domain",
            "current_value": "MISSING_HELMHOLTZ_SECOND_VARIATION_CHECK",
            "units": "action Hessian obstruction units",
            "arena": "action-existence gate; local GR theorem status",
            "source_path": str(SOURCES["doc_1010"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "leak_id": "GKL3554_3_Euler_source",
            "quantity": "J_GK",
            "formula": "J_GK^nu := sum_A E_A nabla^nu Phi^A + source-current terms",
            "non_cancellation_bound": "|P_loc J_GK| retained independently",
            "needed_inputs": "Euler equations, positive operator, source-free compact collar and source-current zero theorem",
            "current_value": "MISSING_GK_EULER_SOURCE_CURRENT_ZERO",
            "units": "projected force density",
            "arena": "fifth-force; local force; PPN",
            "source_path": str(SOURCES["response_doublet_variation"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "leak_id": "GKL3554_4_double_zero_F1",
            "quantity": "F1_GK",
            "formula": "F1_GK := partial_A T_GK^{mu nu}(Phi0)",
            "non_cancellation_bound": "|F1_GK delta Phi^A| retained independently",
            "needed_inputs": "local fixed point Phi0, Gamma0 subtraction, response doublet component map and no linear source",
            "current_value": "MISSING_GK_DOUBLE_ZERO_CERTIFICATE",
            "units": "linear stress-response coefficient",
            "arena": "PPN/source-normalization linear hair",
            "source_path": str(SOURCES["response_doublet_variation"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "leak_id": "GKL3554_5_boundary_projector",
            "quantity": "B_GK + Delta_Ploc",
            "formula": "boundary/symplectic flux plus P_loc ownership failure",
            "non_cancellation_bound": "|P_loc B_GK| + |Delta_Ploc q_loc| retained independently",
            "needed_inputs": "boundary no-flux, fixed topological subtraction, parent P_loc and readout commutation",
            "current_value": "MISSING_GK_BOUNDARY_PLOC_CERTIFICATE",
            "units": "boundary force/mass-flux residual",
            "arena": "alpha3; source mass flux; local boundary terms",
            "source_path": str(SOURCES["doc_1010"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "QLOC3554_0_total",
            "residual_symbol": "q_loc^nu",
            "definition": "P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "retained_expression": "q_loc^nu = P_loc nabla_mu T_GK^{mu nu} + P_loc nabla_mu Delta_K^{mu nu} + projector/boundary terms",
            "observable_map": "PPN alpha_i/xi; alpha3; source-normalization R11; local force/fifth-force; clock/orbital residuals",
            "current_value": "MISSING_QLOC_NUMERIC_OR_THEOREM_ZERO_PROJECTION",
            "units": "projected force density or normalized dimensionless residual by arena",
            "status": "RETAINED_NONCLAIM",
            "source_path": str(SOURCES["local_residual_vector"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "QLOC3554_1_PPN_vector",
            "residual_symbol": "alpha_i_xi_from_q_loc",
            "definition": "q_loc projected into preferred-frame / anisotropic local residual channels",
            "retained_expression": "R_PPN_GK = W_GK_PPN * epsilon_q_loc",
            "observable_map": "alpha1; alpha2; alpha3; xi",
            "current_value": "MISSING_W_GK_PPN_EPSILON_QLOC",
            "units": "dimensionless PPN residual",
            "status": "BOUND_ROW_NONCLAIM",
            "source_path": str(SOURCES["local_residual_vector"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "QLOC3554_2_source_normalization",
            "residual_symbol": "c_GK_source_normalization_operator",
            "definition": "q_loc contribution to non-EH operator/source normalization ledger",
            "retained_expression": "R11_GK = c_GK_source_normalization_operator",
            "observable_map": "Newton source denominator; R11 EH-operator ledger; local-GR residual vector",
            "current_value": "MISSING_GK_SOURCE_NORMALIZATION_OPERATOR_VECTOR",
            "units": "dimensionless or declared operator units",
            "status": "BOUND_ROW_NONCLAIM",
            "source_path": str(SOURCES["local_residual_vector"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "QLOC3554_3_theta_feed",
            "residual_symbol": "Delta_theta_GK_to_DXHtau",
            "definition": "i_tau Delta theta_GK term retained in H_tau variation",
            "retained_expression": "|D_X H_tau| includes |i_tau Delta theta_GK|",
            "observable_map": "H_tau; M_H_ref; C_M; Newton/source coupling",
            "current_value": "MISSING_THETA_GK_TO_DXHTAU_PROJECTION",
            "units": "charge derivative contribution",
            "status": "BOUND_ROW_NONCLAIM",
            "source_path": str(SOURCES["theta_leak_3553"]["path"]),
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D3554_0_action_verdict",
            "question": "Did 3554 prove a live S_GK/theta_GK owner?",
            "decision": "No live claim. It proves the exact variational route but current MTS lacks scalar-density owner, metric-response match, Helmholtz check, Euler/source-zero and boundary/projector certificates.",
            "basis": "513/514/515/1010 all keep these gates unsigned; 3554 carries them into the current H_tau/local-GR spine.",
            "consequence": "theta_GK, T_GK and q_loc remain retained nonclaim residuals.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "D3554_1_best_constructive_route",
            "question": "What is the best derivation path?",
            "decision": "Response-doublet even scalar density remains the best candidate.",
            "basis": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B gives the desired double-zero shape if component map, positivity, source-current zero and boundary no-flux are signed.",
            "consequence": "The next derivation should attack response-doublet source-current/boundary zero rather than repeating GK audits.",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "D3554_2_no_plateau",
            "question": "Can q_loc be set zero by local plateau?",
            "decision": "No. Plateau/bookkeeping stress shortcuts remain rejected.",
            "basis": "q_loc zero is allowed only as on-shell divergence of action-owned stress with all gates signed.",
            "consequence": "Local GR/PPN/Newton source claims stay blocked until q_loc is theorem-zero or bounded.",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS3554_0",
            "checkpoint": "3554 Gamma/Khat sector action existence or theta_GK bound",
            "claim_allowed": "False",
            "S_GK_status": "EXACT_VARIATIONAL_ROUTE_WRITTEN; ACTION_OWNER_NOT_SUPPLIED",
            "theta_GK_status": "RETAINED_NONCLAIM_LEAKAGE_ROW",
            "q_loc_status": "RETAINED_NONCLAIM_LOCAL_RESIDUAL_UNTIL_METRIC_RESPONSE_HELMHOLTZ_EULER_DOUBLEZERO_BOUNDARY_CLOSE",
            "strongest_result": "q_loc is reduced to projected divergence of an action-owned stress if T_GK=Gamma g-Khat; current corpus has not matched that stress",
            "next_target": "3555-Y5-R2FR-response-doublet-Gamma-owner-source-current-zero-or-q_loc-bound-fill.md",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3554_0",
            "target_doc": "3555-Y5-R2FR-response-doublet-Gamma-owner-source-current-zero-or-q_loc-bound-fill.md",
            "target_script": "scripts/Y5_R2FR_3555_response_doublet_Gamma_owner_source_current_zero_or_q_loc_bound_fill.py",
            "objective": "try to prove the response-doublet Gamma_eff owner has zero local source current and boundary flux on the compact branch; if not, produce q_loc residual bound-fill rows with PPN/source-normalization projections",
            "success_gate": "either response-doublet S_GK closes Gamma_eff/Khat double-zero with source-current and boundary zero, or q_loc obtains source-ready nonclaim coefficient rows",
            "reason": "response doublet is the strongest constructive Gamma owner route; if it fails, q_loc must be scored rather than hidden",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(
    generated_csvs: list[Path],
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    leaks: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    all_sources_exist = all(row["exists"] == "True" for row in sources)
    csvs_parse = all(csv_parse_ok(path) for path in generated_csvs)
    qloc_theorem_present = any(row["theorem_id"] == "GK3554_1_metric_response_identity" for row in theorem)
    required_gates = {
        "GKG3554_0_action_existence",
        "GKG3554_1_metric_response",
        "GKG3554_2_Helmholtz",
        "GKG3554_3_Euler_closure",
        "GKG3554_4_double_zero",
        "GKG3554_5_projector_boundary",
    }
    gates_covered = required_gates.issubset({row["gate_id"] for row in gates})
    residual_retained = any(row["residual_id"] == "QLOC3554_0_total" and row["status"] == "RETAINED_NONCLAIM" for row in residuals)
    all_nonclaim = (
        all(row["valid_for_claim"] == "False" for row in theorem)
        and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in gates)
        and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in candidates)
        and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in leaks)
        and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in residuals)
        and all(row["valid_for_claim"] == "False" for row in decisions)
    )
    missing_markers_present = all("MISSING_" in row["current_value"] for row in leaks + residuals)
    no_formalization_outputs = all(not path.resolve().is_relative_to(FORMALIZATION.resolve()) for path in generated_csvs)

    return [
        {
            "validation_id": "VAL3554_0_sources_exist",
            "passes": bool_text(all_sources_exist),
            "status": "PASS" if all_sources_exist else "FAIL",
            "detail": f"{sum(row['exists'] == 'True' for row in sources)}/{len(sources)} cited source paths exist",
        },
        {
            "validation_id": "VAL3554_1_generated_csvs_parse",
            "passes": bool_text(csvs_parse),
            "status": "PASS" if csvs_parse else "FAIL",
            "detail": f"{len(generated_csvs)} generated CSV files parse with DictReader",
        },
        {
            "validation_id": "VAL3554_2_metric_response_qloc_theorem_present",
            "passes": bool_text(qloc_theorem_present),
            "status": "PASS" if qloc_theorem_present else "FAIL",
            "detail": "q_loc as projected stress divergence theorem is present",
        },
        {
            "validation_id": "VAL3554_3_required_gates_covered",
            "passes": bool_text(gates_covered),
            "status": "PASS" if gates_covered else "FAIL",
            "detail": "action, metric response, Helmholtz, Euler, double-zero and boundary/projector gates are covered",
        },
        {
            "validation_id": "VAL3554_4_residual_retained",
            "passes": bool_text(residual_retained),
            "status": "PASS" if residual_retained else "FAIL",
            "detail": "q_loc retained as explicit nonclaim residual",
        },
        {
            "validation_id": "VAL3554_5_all_rows_nonclaim_with_missing_markers",
            "passes": bool_text(all_nonclaim and missing_markers_present),
            "status": "PASS" if all_nonclaim and missing_markers_present else "FAIL",
            "detail": "all rows keep claims disabled and expose missing theorem/numeric inputs",
        },
        {
            "validation_id": "VAL3554_6_formalization_workbench_untouched",
            "passes": bool_text(no_formalization_outputs),
            "status": "PASS" if no_formalization_outputs else "FAIL",
            "detail": "3554 generated outputs only inside post-checkpoint-work",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3554 - Gamma/Khat sector action existence or theta_GK bound",
        "",
        "## Verdict",
        "",
        "- **Exact derivation route:** if `T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_hat^{mu nu}` is action-derived, then `q_loc^nu=P_loc nabla_mu T_GK^{mu nu}`.",
        "- **On-shell zero condition:** `q_loc` vanishes only if the GK Euler equations, source-current zero, boundary no-flux and `P_loc` ownership all close.",
        "- **Current status:** no live `S_GK/theta_GK` claim; scalar-density owner, metric-response match, Helmholtz check, double-zero and boundary/projector clauses are unsigned.",
        "- **Best route:** response-doublet even scalar density remains the strongest constructive candidate; otherwise `q_loc` must be bounded as a residual.",
        "",
        "## GK Theorem",
        "",
        markdown_table(
            rows_by_name["theorem"],
            ["theorem_id", "claim_piece", "statement", "current_status"],
        ),
        "",
        "## Action Gates",
        "",
        markdown_table(
            rows_by_name["gates"],
            ["gate_id", "gate", "required", "status", "if_fail"],
        ),
        "",
        "## Candidate Routes",
        "",
        markdown_table(
            rows_by_name["candidates"],
            ["candidate_id", "candidate", "why_promising", "status"],
        ),
        "",
        "## theta_GK / T_GK Leakage",
        "",
        markdown_table(
            rows_by_name["leaks"],
            ["leak_id", "quantity", "formula", "current_value", "arena"],
        ),
        "",
        "## q_loc Residual Rows",
        "",
        markdown_table(
            rows_by_name["residuals"],
            ["residual_id", "residual_symbol", "definition", "current_value", "status"],
        ),
        "",
        "## Decisions",
        "",
        markdown_table(
            rows_by_name["decisions"],
            ["decision_id", "question", "decision", "consequence"],
        ),
        "",
        "## Validation",
        "",
        markdown_table(
            rows_by_name["validation"],
            ["validation_id", "passes", "status", "detail"],
        ),
        "",
        "## Next target",
        "",
        "Move to `3555-Y5-R2FR-response-doublet-Gamma-owner-source-current-zero-or-q_loc-bound-fill.md`: try to close the response-doublet source-current/boundary zero; if not, fill q_loc residual coefficient rows.",
        "",
        f"Generated UTC: {datetime.now(timezone.utc).isoformat()}",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    theorem = theorem_rows()
    gates = gate_rows()
    candidates = candidate_rows()
    leaks = leakage_rows()
    residuals = residual_rows()
    decisions = decision_rows()
    status = status_rows()
    next_target = next_target_rows()

    outputs: dict[Path, tuple[list[dict[str, Any]], list[str]]] = {
        OUT / "P8_Y5_R2FR_3554_SOURCE_REGISTER.csv": (
            sources,
            ["source_id", "path", "exists", "role", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3554_GK_ACTION_THEOREM.csv": (
            theorem,
            [
                "theorem_id",
                "claim_piece",
                "statement",
                "proof_step",
                "condition_needed",
                "current_status",
                "source_path",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3554_GK_ACTION_GATE_AUDIT.csv": (
            gates,
            [
                "gate_id",
                "gate",
                "required",
                "current_evidence",
                "status",
                "if_fail",
                "source_path",
                "claim_allowed",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3554_GK_CANDIDATE_ROUTE_COMPARE.csv": (
            candidates,
            ["candidate_id", "candidate", "why_promising", "missing", "status", "source_path", "claim_allowed", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3554_THETA_GK_TGK_LEAKAGE_ROWS.csv": (
            leaks,
            [
                "leak_id",
                "quantity",
                "formula",
                "non_cancellation_bound",
                "needed_inputs",
                "current_value",
                "units",
                "arena",
                "source_path",
                "claim_allowed",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3554_QLOC_RESIDUAL_RETENTION_ROWS.csv": (
            residuals,
            [
                "residual_id",
                "residual_symbol",
                "definition",
                "retained_expression",
                "observable_map",
                "current_value",
                "units",
                "status",
                "source_path",
                "claim_allowed",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3554_DECISION_LEDGER.csv": (
            decisions,
            ["decision_id", "question", "decision", "basis", "consequence", "valid_for_claim"],
        ),
        OUT / "P8_Y5_R2FR_3554_STATUS.csv": (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "S_GK_status",
                "theta_GK_status",
                "q_loc_status",
                "strongest_result",
                "next_target",
                "valid_for_claim",
            ],
        ),
        OUT / "P8_Y5_R2FR_3554_NEXT_TARGET.csv": (
            next_target,
            ["next_id", "target_doc", "target_script", "objective", "success_gate", "reason", "valid_for_claim"],
        ),
        CANONICAL_STATUS: (
            status,
            [
                "status_id",
                "checkpoint",
                "claim_allowed",
                "S_GK_status",
                "theta_GK_status",
                "q_loc_status",
                "strongest_result",
                "next_target",
                "valid_for_claim",
            ],
        ),
    }

    generated_paths: list[Path] = []
    for path, (rows, fields) in outputs.items():
        write_csv(path, rows, fields)
        generated_paths.append(path)

    validation = validation_rows(generated_paths, sources, theorem, gates, candidates, leaks, residuals, decisions)
    validation_path = OUT / "P8_Y5_BRR545_3554_VALIDATION.csv"
    write_csv(validation_path, validation, ["validation_id", "passes", "status", "detail"])
    generated_paths.append(validation_path)

    write_doc(
        {
            "theorem": theorem,
            "gates": gates,
            "candidates": candidates,
            "leaks": leaks,
            "residuals": residuals,
            "decisions": decisions,
            "status": status,
            "next_target": next_target,
            "validation": validation,
        }
    )

    print(f"wrote {DOC}")
    for path in generated_paths:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
