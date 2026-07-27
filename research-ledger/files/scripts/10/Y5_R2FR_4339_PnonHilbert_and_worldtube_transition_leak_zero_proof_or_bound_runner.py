from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4339"
CLAIM_ID = "L-180"
BRANCH = "MTS_R2FR_Y5_PNONHILBERT_AND_WORLDTUBE_TRANSITION_LEAK_ZERO_PROOF_OR_BOUND_RUNNER_4339"
DECISION = "FIRST_TWO_PLEAK_ZERO_PROOFS_FAIL_BUT_REDUCED_TO_DVQTR_AND_WORLDTUBE_TRACE_DEFECT_BOUND_MACHINERY_NONCLAIM"
MARKER = "PPC4161_PNONHILBERT_AND_WORLDTUBE_TRANSITION_LEAK_ZERO_PROOF_OR_BOUND_RUNNER_4339"
PACKET_MARKER = "PPC4161_PACKET_PNONHILBERT_AND_WORLDTUBE_TRANSITION_LEAK_ZERO_PROOF_OR_BOUND_RUNNER_4339"
NEXT_TARGET = "4340-Y5-R2FR-DvKhat-DeltaK-and-worldtube-trace-defect-input-fill.md"

FORMAL_PATH = FORMAL / "355-PPC4161-PnonHilbert-and-worldtube-transition-leak-zero-proof-or-bound-runner.md"
DOC_PATH = POST / "4339-Y5-R2FR-PnonHilbert-and-worldtube-transition-leak-zero-proof-or-bound-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4339_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")

Y_GAMMA_LIMIT = 0.0002739826487147268
Y_BETA_LIMIT = 0.0009529831259642674
Y_CLOCK_LIMIT = 0.0006134828873394971


SOURCES = [
    (
        "SRC4339_00_4338_next_target",
        FORMAL / "354-PPC4161-cGamma-transition-source-kernel-coefficient-fill-or-metric-null-proof.md",
        "P_nonHilbert_action_domain and P_off_worldtube_readout_order",
        "4338 selects the first two raw transition-shell P_leak targets.",
    ),
    (
        "SRC4339_01_312_first_failure",
        FORMAL / "312-PPC4161-Pleak-transition-component-zero-attempts-or-bound-row-selection.md",
        "FIRST_TWO_PLEAK_COMPONENTS_NOT_ZERO_DERIVED_BOUND_ROWS_SELECTED_NONCLAIM",
        "Earlier first-pass result: neither first P_leak component was zero-derived.",
    ),
    (
        "SRC4339_02_313_qtr_definition",
        FORMAL / "313-PPC4161-qtr-vertical-or-topological-rest-proof-attempt-for-PnonHilbert.md",
        "q_tr^nu = nabla^nu Gamma_eff - nabla_mu K_hat^(mu nu).",
        "Raw transition-current definition used by the P_nonHilbert route.",
    ),
    (
        "SRC4339_03_314_Dv_qtr",
        FORMAL / "314-PPC4161-Gamma-Khat-hidden-dependence-factorization-or-first-Dv-qtr-bound-row.md",
        "D_v q_tr^nu =",
        "Vertical variation identity for the q_tr leak channel.",
    ),
    (
        "SRC4339_04_315_DeltaK",
        FORMAL / "315-PPC4161-DvGamma-DvKhat-first-source-coefficient-or-QAP-parent-signature.md",
        "D_v K_hat = D_v Delta_K + D_v K_metric[Gamma_eff].",
        "Khat residual split that keeps Delta_K as the next non-Hilbert target.",
    ),
    (
        "SRC4339_05_316_double_zero",
        FORMAL / "316-PPC4161-DvGamma-m-Lcg-zero-or-first-coefficient-source-row.md",
        "VERTICAL_DOUBLE_ZERO_KILLS_DVGAMMA_CONDITIONALLY_FIRST_COEFFICIENT_DEMOTED_TO_SECOND_ORDER_NONCLAIM",
        "Conditional double-zero theorem demoting D_v Gamma_eff from linear to quadratic.",
    ),
    (
        "SRC4339_06_318_lambda_m",
        FORMAL / "318-PPC4161-m-lock-coercivity-gap-and-DvGamma-quadratic-input-pack.md",
        "lambda_m = Z_min lambda_1(D_loc) + M2_min - Eta_H.",
        "Coercivity floor used in m-lock and trace-defect amplitude bounds.",
    ),
    (
        "SRC4339_07_323_smooth_domain",
        FORMAL / "323-PPC4161-source-domain-owner-or-inner-flux-profile-fill.md",
        "smooth Hilbert volume source domain:",
        "Worldtube/off-readout route: smooth full-domain branch has no inner boundary.",
    ),
    (
        "SRC4339_08_324_mu_tr",
        FORMAL / "324-PPC4161-smooth-Hilbert-volume-domain-parent-signature-or-worldtube-flux-profile-row.md",
        "mu_tr := weak-lim_epsilon_to_0 g_in,epsilon dSigma,",
        "Trace-defect row for exterior/worldtube readout branches.",
    ),
    (
        "SRC4339_09_326_collar_bound",
        FORMAL / "326-PPC4161-collar-no-concentration-signature-or-trace-bound-inputs.md",
        "A_U <= C_col (R_U + N_N + N_boundary) / lambda_*.",
        "No-concentration route reducing trace defect to a lambda floor and residual numerator.",
    ),
    (
        "SRC4339_10_332_visible_em_reduction",
        FORMAL / "332-PPC4161-visible-Hilbert-source-silence-integration-or-nonEM-residual-budget.md",
        "N_pair <= N_inner + N_rest_nonEM.",
        "Visible Hilbert and EM zero branches leave inner/non-EM budget.",
    ),
    (
        "SRC4339_11_333_inner_zero",
        FORMAL / "333-PPC4161-nonEM-inner-charge-domain-zero-or-QmH-bound-values.md",
        "partialD_in=empty and B_src=0 => N_inner=0",
        "Smooth full-domain source zero condition for inner/worldtube residual.",
    ),
    (
        "SRC4339_12_334_single_count",
        FORMAL / "334-PPC4161-nonHilbert-support-drift-history-bound-prioritizer.md",
        "N_rest_nonEM^canon := N_src_nonHilbert + N_drift_selector + N_history_transition + N_boundary_domain + N_N",
        "Single-count non-EM residual budget to avoid double-counting leak channels.",
    ),
    (
        "SRC4339_13_335_Hperp_bound",
        FORMAL / "335-PPC4161-nonHilbert-Hperp-source-support-zero-or-bound-row.md",
        "N_src_nonHilbert <= ||U_B||_inf (C_S C_perp E_Dq,Hperp + ||R_src_readout||).",
        "Finite Dq/Hperp source-support bound for non-Hilbert residuals.",
    ),
    (
        "SRC4339_14_336_component_rank",
        FORMAL / "336-PPC4161-Hperp-Dq-component-certificate-or-first-epsilon-profile-row.md",
        "Dq_source_readout[Hperp]",
        "Ranked Hperp Dq components feeding source/readout leakage.",
    ),
    (
        "SRC4339_15_339_marker_lift",
        FORMAL / "339-PPC4161-Dq-theta-marker-Hperp-zero-lift-or-marker-tail-bound.md",
        "THETA_MARKER_HPERP_ZERO_LIFTED_FOR_STANDARD_CALIBRATED_BRANCH_MARKER_TAIL_BOUND_RETAINED_NONCLAIM",
        "Standard theta-marker lift; hidden marker/source tails retained outside the branch.",
    ),
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return ""


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: str(row.get(key, "")) for key in fields})


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, path, needle, role in SOURCES:
        line_number = find_line(path, needle)
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
            }
        )
    return rows


def zero_proof_rows() -> List[Dict[str, str]]:
    return [
        {
            "proof_id": "ZP4339_0_PnonHilbert_Hilbert_owner",
            "component": "P_nonHilbert_action_domain",
            "zero_condition": "q_tr = delta S_tr^H[g_obs,chi;tau]/delta g_obs inside the same Hilbert source block, with no representative-only source slot",
            "derived_result": "P_nonHilbert q_tr = 0 if the parent action signs this ownership",
            "current_status": "NOT_PARENT_SIGNED",
            "why_not_closed": "raw q_tr is defined by Gamma_eff and K_hat; the corpus has not signed it as a Hilbert-source functional derivative",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "ZP4339_1_PnonHilbert_vertical_silent",
            "component": "P_nonHilbert_action_domain",
            "zero_condition": "D_v q_tr=0 for every vertical representative direction v in ker(Dq), with fixed/routed boundary pullback",
            "derived_result": "P_nonHilbert q_tr has no representative-only bulk response",
            "current_status": "REDUCED_TO_DVQTR_BOUND",
            "why_not_closed": "D_v Gamma_eff, D_v K_hat, connection and boundary terms are not all parent-zero",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "ZP4339_2_PnonHilbert_topological_rest",
            "component": "P_nonHilbert_action_domain",
            "zero_condition": "q_tr^nu=nabla_mu U^[mu nu] with boundary support fixed/routed and zero local bulk Hilbert stress",
            "derived_result": "local non-Hilbert source projection vanishes by superpotential routing",
            "current_status": "OPEN_THEOREM_ROUTE",
            "why_not_closed": "no parent superpotential identity for the raw Gamma/Khat transition current is signed",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "ZP4339_3_DvGamma_double_zero",
            "component": "P_nonHilbert_action_domain",
            "zero_condition": "Gamma_eff=L_cg^-2 F(m), F(m_*)=0 and F_m(m_*)=0 on the local branch",
            "derived_result": "D_v Gamma_eff|_* = 0 at linear order; remaining Gamma leakage is quadratic in Delta_m and Delta_Dv_m",
            "current_status": "CONDITIONAL_THEOREM_PARENT_LOCK_UNSIGNED",
            "why_not_closed": "double-zero local branch lock and required quadratic input values are not parent-signed",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "ZP4339_4_DvKhat_DeltaK",
            "component": "P_nonHilbert_action_domain",
            "zero_condition": "Delta_K:=K_hat-K_metric[Gamma_eff]=0 and no memory-gradient/connection/boundary residue",
            "derived_result": "D_v K_hat reduces to the controlled metric-response derivative of Gamma_eff",
            "current_status": "NEXT_ZERO_PROOF_TARGET",
            "why_not_closed": "Delta_K and connection/domain terms are currently finite rows, not zero theorems",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "ZP4339_5_worldtube_full_domain",
            "component": "P_off_worldtube_readout_order",
            "zero_condition": "source is treated as a smooth full Hilbert volume before any exterior/worldtube split",
            "derived_result": "partialD_in=empty, artificial inner flux cancels, and N_inner=0",
            "current_status": "CONDITIONAL_EXACT_BRANCH_NOT_PARENT_SIGNED",
            "why_not_closed": "domain inclusion and smooth-to-exterior no-defect limit are not globally signed for raw transition readout",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "ZP4339_6_worldtube_trace_defect",
            "component": "P_off_worldtube_readout_order",
            "zero_condition": "mu_tr=0 and B_src^A=0 in the smooth-to-exterior limit",
            "derived_result": "N_inner=0 survives exterior readout without smuggling a boundary source",
            "current_status": "REDUCED_TO_TRACE_DEFECT_BOUND",
            "why_not_closed": "mu_tr zero is reduced to lambda_* and residual silence; those inputs are not sourced",
            "valid_for_claim": "False",
        },
        {
            "proof_id": "ZP4339_7_worldtube_same_readout_order",
            "component": "P_off_worldtube_readout_order",
            "zero_condition": "same W_H, same Hamiltonian mass readout, and readout applied after parent variation/quotient descent",
            "derived_result": "transition current cannot enter through a post-hoc off-worldtube readout-order leak",
            "current_status": "PARTIAL_BRANCH_CONTRACT",
            "why_not_closed": "same-worldtube and before-readout ownership are not signed for all raw transition-shell uses",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> List[Dict[str, str]]:
    return [
        {
            "bound_id": "BD4339_0_Dv_qtr_identity",
            "channel": "P_nonHilbert_action_domain",
            "formula": "D_v q_tr^nu = nabla^nu(D_v Gamma_eff)-nabla_mu(D_v K_hat^(mu nu))+C_conn^nu+B_boundary^nu",
            "interpretation": "non-Hilbert leakage is now a finite vertical-response vector, not a vague coupling complaint",
            "required_inputs": "D_v Gamma_eff, D_v K_hat, C_conn, B_boundary",
            "claim_status": "NONCLAIM_BOUND_MACHINE",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BD4339_1_DvGamma_quadratic",
            "channel": "P_nonHilbert_action_domain",
            "formula": "if F=F_m=0, C_DvGamma <= C_quad[Delta_m Delta_Dv_m + Delta_m^2 Delta_DvlnL] + C_proj",
            "interpretation": "the double-zero path avoids demanding an absurdly tiny first-order D_v Gamma coefficient",
            "required_inputs": "F_2, Delta_m, Delta_Dv_m, Delta_DvlnL, projection constants",
            "claim_status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BD4339_2_DvKhat_split",
            "channel": "P_nonHilbert_action_domain",
            "formula": "D_v K_hat = D_v Delta_K + K_metric'[Gamma_eff]D_v Gamma_eff + connection/domain/boundary kernels",
            "interpretation": "after the Gamma double-zero, the real remaining attack is Delta_K and the operator-domain tail",
            "required_inputs": "Delta_K zero theorem or C_DeltaK, K_metric response norm, connection/domain/boundary kernels",
            "claim_status": "NEXT_INPUT_TARGET",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BD4339_3_PnonHilbert_precision_budget",
            "channel": "P_nonHilbert_action_domain",
            "formula": f"Y_nonHilbert <= C_NH(C_DvGamma+C_DvKhat+C_conn+C_boundary), require Y_gamma<={Y_GAMMA_LIMIT}",
            "interpretation": "PPN gamma remains the harshest local precision budget for this branch",
            "required_inputs": "arena projection constant C_NH and all vertical-response components",
            "claim_status": "BOUND_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BD4339_4_worldtube_trace_defect",
            "channel": "P_off_worldtube_readout_order",
            "formula": "N_inner <= ||mu_tr|| + ||B_src^A|| <= C_0|Q_m^H| + C_perp||g_perp|| + ||B_src||",
            "interpretation": "exterior/worldtube readout must carry a real trace-defect row; it cannot borrow smooth-domain zero for free",
            "required_inputs": "mu_tr or Q_m^H/g_perp/B_src/C_0/C_perp plus B_src^A",
            "claim_status": "BOUND_ROUTE_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BD4339_5_worldtube_lambda_reduction",
            "channel": "P_off_worldtube_readout_order",
            "formula": "N_inner <= C_N[K_U C_col(S_U_not_inner)/lambda_* + R_U] + ||B_src^A||",
            "interpretation": "no-concentration is reduced to a positive lambda floor and a residual numerator that excludes N_inner itself",
            "required_inputs": "lambda_*, C_N, K_U, C_col, S_U_not_inner, R_U, B_src^A",
            "claim_status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BD4339_6_source_pair_handoff",
            "channel": "P_off_worldtube_readout_order",
            "formula": "N_pair <= N_rest_nonEM^canon + N_inner_bound",
            "interpretation": "visible/EM silence has already narrowed the problem to inner/worldtube plus canonical non-EM budget",
            "required_inputs": "N_rest_nonEM^canon, N_inner_bound, lambda/source-equality/projection gates",
            "claim_status": "HANDOFF_READY_NOT_SCORE_READY",
            "valid_for_claim": "False",
        },
    ]


def input_rows() -> List[Dict[str, str]]:
    return [
        {
            "input_id": "IN4339_0_C_DvGamma_quad",
            "symbol": "C_DvGamma_quad",
            "needed_for": "P_nonHilbert vertical-response bound after double-zero",
            "status": "MISSING_DELTA_M_F2_VERTICAL_PROFILE_ROWS",
            "next_action": "source F_2, Delta_m, Delta_Dv_m, Delta_DvlnL and projection constants",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4339_1_C_DeltaK",
            "symbol": "C_DeltaK",
            "needed_for": "D_v K_hat residual split",
            "status": "MISSING_DELTAK_ZERO_THEOREM_OR_BOUND",
            "next_action": "prove Delta_K=0 from Khat metric ownership or build first finite coefficient row",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4339_2_C_conn_boundary",
            "symbol": "C_conn + B_boundary",
            "needed_for": "D_v q_tr vertical-response closure",
            "status": "MISSING_OPERATOR_DOMAIN_BOUNDARY_ZERO_OR_BOUND",
            "next_action": "prove connection/domain commutator silence or source absolute envelope",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4339_3_lambda_star",
            "symbol": "lambda_*",
            "needed_for": "worldtube trace no-concentration",
            "status": "FORMULA_READY_VALUE_UNSOURCED",
            "next_action": "derive/source Z_min, lambda_1(D_loc), M2_min and Eta_H with positive floor",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4339_4_SU_not_inner",
            "symbol": "S_U_not_inner",
            "needed_for": "self-consistent worldtube trace bound",
            "status": "FORMULA_READY_COMPONENT_VALUES_MISSING",
            "next_action": "assemble residual numerator excluding N_inner itself",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4339_5_mu_tr",
            "symbol": "mu_tr",
            "needed_for": "exterior/worldtube defect route",
            "status": "MISSING_ZERO_THEOREM_OR_VALUE",
            "next_action": "prove no-concentration or bound Q_m^H/g_perp/B_src profile",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4339_6_Nsrc_nonHilbert",
            "symbol": "N_src_nonHilbert",
            "needed_for": "canonical non-EM budget after visible/EM reductions",
            "status": "BOUND_FORMULA_READY_VALUES_MISSING",
            "next_action": "fill Hperp/Dq epsilons or prove source/readout Hperp zero",
            "valid_for_claim": "False",
        },
    ]


def component_rows() -> List[Dict[str, str]]:
    return [
        {
            "component_id": "PLEAK4339_0",
            "component": "P_nonHilbert_action_domain",
            "priority": "P0",
            "zero_status_before": "NOT_PARENT_SIGNED",
            "zero_status_after": "NOT_ZERO_DERIVED_REDUCED_TO_DVQTR_BOUND",
            "main_formula": "D_v q_tr^nu = nabla^nu(D_v Gamma_eff)-nabla_mu(D_v K_hat^(mu nu))+C_conn^nu+B_boundary^nu",
            "next_input": "Delta_K zero/bound plus D_v Gamma quadratic values",
            "valid_for_claim": "False",
        },
        {
            "component_id": "PLEAK4339_1",
            "component": "P_off_worldtube_readout_order",
            "priority": "P0",
            "zero_status_before": "NOT_PARENT_SIGNED",
            "zero_status_after": "NOT_ZERO_DERIVED_REDUCED_TO_TRACE_DEFECT_BOUND",
            "main_formula": "N_inner <= ||mu_tr||+||B_src^A|| <= C_N[K_U C_col S_U_not_inner/lambda_*+R_U]+||B_src^A||",
            "next_input": "lambda_*, S_U_not_inner, mu_tr/B_srcA, same-worldtube readout-order contract",
            "valid_for_claim": "False",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4339_0_current",
            "branch_input": "current corpus with raw transition q_tr",
            "action": "REJECT_ZERO_CLAIM_USE_BOUND_MACHINERY",
            "output": "first two P_leak channels remain live but now have concrete zero-or-bound equations",
            "claim_policy": "no local-GR/R10/PPN/clock/orbital claim",
        },
        {
            "runner_id": "RUN4339_1_PnonHilbert_zero_future",
            "branch_input": "D_v Gamma_eff=D_v K_hat=C_conn=B_boundary=0 or Hilbert-owner/topological route signed",
            "action": "ALLOW_CONDITIONAL_ZERO",
            "output": "P_nonHilbert_action_domain q_tr=0",
            "claim_policy": "conditional private theorem only until all other P_leak components close",
        },
        {
            "runner_id": "RUN4339_2_worldtube_zero_future",
            "branch_input": "smooth full-domain source or mu_tr=B_src^A=0 with same-worldtube before-readout ownership",
            "action": "ALLOW_CONDITIONAL_ZERO",
            "output": "P_off_worldtube_readout_order q_tr=0",
            "claim_policy": "conditional private theorem only until non-EM/source-equality/projection gates close",
        },
        {
            "runner_id": "RUN4339_3_finite_local_test_future",
            "branch_input": "all vertical-response, trace-defect, non-EM and projection rows sourced",
            "action": "ALLOW_NONCLAIM_PRECISION_TEST",
            "output": "compare Y_gamma/Y_beta/Y_clock and R10/orbital envelopes without cancellation",
            "claim_policy": "claim only if all rows are real, source-backed and below arena budgets",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4339_0",
            "forbidden_shortcut": "Calling q_tr Hilbert-owned because ordinary matter has Hilbert coupling",
            "reason": "raw q_tr lives in the Gamma/Khat transition sector until the parent signs same action-domain ownership",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4339_1",
            "forbidden_shortcut": "Setting D_v q_tr=0 without proving D_v Gamma_eff, D_v K_hat, connection and boundary silence",
            "reason": "313/314 give an explicit hidden-dependence counterchannel",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4339_2",
            "forbidden_shortcut": "Using smooth-domain N_inner=0 inside an exterior/worldtube solve",
            "reason": "exterior branches require mu_tr/B_src or a no-concentration theorem",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4339_3",
            "forbidden_shortcut": "Letting N_inner appear in its own residual numerator",
            "reason": "use S_U_not_inner so the trace bound is not circular",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4339_4",
            "forbidden_shortcut": "Treating closure of these two P0 channels as local GR",
            "reason": "five other P_leak components, lambda/source equality, commutator and projection gates remain",
            "status": "ACTIVE",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4339_0",
            "decision": DECISION,
            "reason": "the zero proofs do not close for raw q_tr, but both components now reduce to explicit finite theorem/bound machinery",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4339_0",
            "item": "P_nonHilbert_action_domain",
            "status": "DVQTR_BOUND_MACHINE_READY_NOT_CLAIM_READY",
            "notes": "attack Delta_K and D_v Gamma quadratic inputs next",
        },
        {
            "status_id": "STAT4339_1",
            "item": "P_off_worldtube_readout_order",
            "status": "TRACE_DEFECT_BOUND_MACHINE_READY_NOT_CLAIM_READY",
            "notes": "attack lambda_*, S_U_not_inner and mu_tr/B_srcA next",
        },
        {
            "status_id": "STAT4339_2",
            "item": "raw transition shell",
            "status": "FIRST_TWO_PLEAK_CHANNELS_SHARPENED",
            "notes": "no local GR claim; route is now zero theorem or finite sourced bound",
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4339_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can Delta_K and the worldtube trace-defect inputs be zeroed or sourced enough to score the first local bound?",
            "preferred_route": "derive Delta_K=0 from Khat metric ownership while proving lambda_*>0 and S_U_not_inner/B_srcA/mu_tr silence",
            "fallback_route": "build nonclaim finite input rows for C_DeltaK, C_conn, B_boundary, lambda_*, S_U_not_inner, mu_tr and B_srcA",
        }
    ]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 355 PPC4161 PnonHilbert and worldtube transition leak zero proof or bound runner

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove local GR, Newton, R10, PPN, clock safety, orbital safety, WEP safety, or public source-kernel membership for raw transition shells.

## Result

4339 takes the first two `P_leak` components from 4338 and tries the zero route honestly.

The result is not a zero proof yet, but it is a real narrowing:

```text
P_nonHilbert_action_domain q_tr
  -> D_v q_tr bound machine
  -> D_v Gamma_eff, D_v K_hat, C_conn, B_boundary
  -> double-zero Gamma route plus Delta_K route

P_off_worldtube_readout_order q_tr
  -> source-domain / trace-defect bound machine
  -> N_inner, mu_tr, B_src^A, lambda_*, S_U_not_inner
```

So the work has moved from "maybe coupling" to two exact places where a future parent action must sign either zeros or finite coefficients.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role"])}

## Zero-Proof Audit

{md_table(tables["zero_proofs"], ["proof_id", "component", "zero_condition", "derived_result", "current_status", "why_not_closed", "valid_for_claim"])}

## Bound Machinery

{md_table(tables["bounds"], ["bound_id", "channel", "formula", "interpretation", "required_inputs", "claim_status", "valid_for_claim"])}

## Component Update

{md_table(tables["components"], ["component_id", "component", "priority", "zero_status_before", "zero_status_after", "main_formula", "next_input", "valid_for_claim"])}

## Required Inputs

{md_table(tables["inputs"], ["input_id", "symbol", "needed_for", "status", "next_action", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "branch_input", "action", "output", "claim_policy"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "forbidden_shortcut", "reason", "status"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "notes"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4339 Y5-R2FR PnonHilbert and worldtube transition leak zero proof or bound runner

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

The first two raw transition-shell leak channels are not zero-derived yet, but they are no longer vague:

```text
P_nonHilbert -> D_v q_tr = nabla(D_v Gamma_eff) - div(D_v K_hat) + connection/boundary
P_off_worldtube -> N_inner <= ||mu_tr|| + ||B_src^A||, reduced by lambda_* and S_U_not_inner
```

## Component Update

{md_table(tables["components"], ["component", "zero_status_after", "main_formula", "next_input"])}

## Next

{md_table(tables["next"], ["next_target", "target_question", "preferred_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path)
    if CLAIM_ID in existing:
        return
    with path.open("a", newline="", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        writer = csv.writer(handle)
        writer.writerow(
            [
                CLAIM_ID,
                "local_gr",
                (
                    "4339 attacks the first two raw transition-shell P_leak components instead of merely listing them. "
                    "P_nonHilbert_action_domain is reduced to the exact vertical-response identity "
                    "D_v q_tr=nabla(D_v Gamma_eff)-div(D_v K_hat)+connection+boundary, with the Gamma leg conditionally demoted by the double-zero branch and the remaining Khat leg pushed to Delta_K. "
                    "P_off_worldtube_readout_order is reduced to the source-domain/trace-defect law N_inner<=||mu_tr||+||B_src^A|| and the no-concentration bound using lambda_* and S_U_not_inner. "
                    "Neither zero proof is parent-signed for raw q_tr, so no local-GR/R10/PPN/clock/orbital claim fires."
                ),
                "4339 source register, zero-proof audit, bound machinery rows, component update, input rows, runner, firewall, decision, status, next-target and validation CSV.",
                "private_first_two_Pleak_channels_reduced_to_Dvqtr_and_trace_defect_bound_machinery_nonclaim",
                "Attack Delta_K/Khat metric ownership and worldtube trace-defect inputs: lambda_*, S_U_not_inner, mu_tr and B_srcA.",
                "Calling q_tr Hilbert-owned without parent action ownership; setting D_v q_tr=0 without proving all legs; using smooth-domain N_inner=0 inside an exterior solve; allowing circular N_inner numerator; or claiming local GR while remaining P_leak/source/projection gates are open.",
            ]
        )


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH,
                "generated_utc": GENERATED_UTC,
                "decision": DECISION,
                "claim_allowed": "False",
                "valid_for_claim": "False",
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "evidence": evidence,
            }
        )

    add("VAL4339_sources_exist", "all source paths exist", all(r["path_exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4339_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4339_two_components", "exactly the first two P0 components updated", len(tables["components"]) == 2 and {r["component"] for r in tables["components"]} == {"P_nonHilbert_action_domain", "P_off_worldtube_readout_order"}, "components")
    add("VAL4339_PnonHilbert_not_claimed", "PnonHilbert zero not claimed", any(r["component"] == "P_nonHilbert_action_domain" and "NOT_ZERO_DERIVED" in r["zero_status_after"] for r in tables["components"]), "components")
    add("VAL4339_worldtube_not_claimed", "worldtube zero not claimed", any(r["component"] == "P_off_worldtube_readout_order" and "NOT_ZERO_DERIVED" in r["zero_status_after"] for r in tables["components"]), "components")
    add("VAL4339_Dvqtr_formula", "D_v q_tr formula present", any("D_v q_tr" in r["formula"] for r in tables["bounds"]), "bounds")
    add("VAL4339_DeltaK_next", "Delta_K next input present", any(r["symbol"] == "C_DeltaK" for r in tables["inputs"]), "inputs")
    add("VAL4339_trace_defect", "trace-defect bound present", any("mu_tr" in r["formula"] and "B_src" in r["formula"] for r in tables["bounds"]), "bounds")
    add("VAL4339_lambda_reduction", "lambda trace reduction present", any("lambda_*" in r["formula"] and "S_U_not_inner" in r["formula"] for r in tables["bounds"]), "bounds")
    add("VAL4339_precision_budget", "local precision thresholds retained", any(str(Y_GAMMA_LIMIT) in r["formula"] for r in tables["bounds"]), "bounds")
    add("VAL4339_all_claim_flags_false", "all table claim flags remain false", all(r.get("valid_for_claim", "False") == "False" for table in tables.values() for r in table if "valid_for_claim" in r), "all_tables")
    add("VAL4339_runner_rejects_current", "current runner rejects zero claim", any(r["runner_id"] == "RUN4339_0_current" and "REJECT" in r["action"] for r in tables["runner"]), "runner")
    add("VAL4339_firewalls", "firewalls include smooth/exterior and Dv shortcuts", any("smooth-domain" in r["forbidden_shortcut"] for r in tables["firewall"]) and any("D_v q_tr=0" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4339_docs_exist", "formal and post docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4339_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4339_post_result", "post doc states both reductions", "P_nonHilbert -> D_v q_tr" in read_text(DOC_PATH) and "P_off_worldtube -> N_inner" in read_text(DOC_PATH), "post")
    add("VAL4339_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4339_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4339_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4339_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4339_SOURCE_REGISTER.csv",
        "zero_proofs": SOURCE_DIR / "P8_Y5_R2FR_4339_ZERO_PROOF_AUDIT.csv",
        "bounds": SOURCE_DIR / "P8_Y5_R2FR_4339_BOUND_MACHINERY.csv",
        "components": SOURCE_DIR / "P8_Y5_R2FR_4339_FIRST_TWO_PLEAK_COMPONENT_UPDATE.csv",
        "inputs": SOURCE_DIR / "P8_Y5_R2FR_4339_REQUIRED_INPUTS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4339_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4339_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4339_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4339_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4339_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "zero_proofs": zero_proof_rows(),
        "bounds": bound_rows(),
        "components": component_rows(),
        "inputs": input_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }
    for key, rows in tables.items():
        write_csv(paths[key], rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4339 first two P_leak channels reduced

Marker: `{MARKER}`

4339 attacks the first two raw transition-shell `P_leak` components.

```text
P_nonHilbert_action_domain q_tr
  -> D_v q_tr^nu = nabla^nu(D_v Gamma_eff)-nabla_mu(D_v K_hat^(mu nu))+C_conn^nu+B_boundary^nu.
```

The Gamma leg has a conditional double-zero demotion; the Khat leg is now the `Delta_K=K_hat-K_metric[Gamma_eff]` problem.

```text
P_off_worldtube_readout_order q_tr
  -> N_inner <= ||mu_tr|| + ||B_src^A||
  -> N_inner <= C_N[K_U C_col S_U_not_inner/lambda_* + R_U] + ||B_src^A||.
```

No local claim fires. The next move is to close or source `Delta_K`, `lambda_*`, `S_U_not_inner`, `mu_tr` and `B_src^A`.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4339 packet first two P_leak channels

Marker: `{PACKET_MARKER}`

Packet update: the first two raw transition-shell `P_leak` channels are not zero-derived, but both have been promoted from labels into working equations. `P_nonHilbert` is the `D_v q_tr`/`Delta_K` problem. `P_off_worldtube` is the source-domain/trace-defect problem controlled by `mu_tr`, `B_src^A`, `lambda_*` and `S_U_not_inner`.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} :: {row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
