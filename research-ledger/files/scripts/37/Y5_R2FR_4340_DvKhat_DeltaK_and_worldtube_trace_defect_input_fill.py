from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4340"
CLAIM_ID = "L-181"
BRANCH = "MTS_R2FR_Y5_DVKHAT_DELTAK_AND_WORLDTUBE_TRACE_DEFECT_INPUT_FILL_4340"
DECISION = "GAMMA_KHAT_RIGHT_INVERSE_CANCELLATION_DERIVED_DELTAK_DIVERGENCE_AND_TRACE_DEFECT_INPUTS_RETAINED_NONCLAIM"
MARKER = "PPC4161_DVKHAT_DELTAK_AND_WORLDTUBE_TRACE_DEFECT_INPUT_FILL_4340"
PACKET_MARKER = "PPC4161_PACKET_DVKHAT_DELTAK_AND_WORLDTUBE_TRACE_DEFECT_INPUT_FILL_4340"
NEXT_TARGET = "4341-Y5-R2FR-Khat-right-inverse-parent-signature-or-DeltaK-divergence-bound.md"

FORMAL_PATH = FORMAL / "356-PPC4161-DvKhat-DeltaK-and-worldtube-trace-defect-input-fill.md"
DOC_PATH = POST / "4340-Y5-R2FR-DvKhat-DeltaK-and-worldtube-trace-defect-input-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4340_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")

Y_GAMMA_LIMIT = 0.0002739826487147268
Y_BETA_LIMIT = 0.0009529831259642674
Y_CLOCK_LIMIT = 0.0006134828873394971


SOURCES = [
    (
        "SRC4340_00_4339_next",
        FORMAL / "355-PPC4161-PnonHilbert-and-worldtube-transition-leak-zero-proof-or-bound-runner.md",
        "4340-Y5-R2FR-DvKhat-DeltaK-and-worldtube-trace-defect-input-fill.md",
        "4339 handoff selecting Delta_K and trace-defect inputs.",
    ),
    (
        "SRC4340_01_qtr_definition",
        FORMAL / "313-PPC4161-qtr-vertical-or-topological-rest-proof-attempt-for-PnonHilbert.md",
        "q_tr^nu = nabla^nu Gamma_eff - nabla_mu K_hat^(mu nu).",
        "Raw transition-current identity to be simplified.",
    ),
    (
        "SRC4340_02_Dv_qtr",
        FORMAL / "314-PPC4161-Gamma-Khat-hidden-dependence-factorization-or-first-Dv-qtr-bound-row.md",
        "D_v q_tr^nu =",
        "Vertical q_tr identity before the new cancellation split.",
    ),
    (
        "SRC4340_03_DeltaK_split",
        FORMAL / "315-PPC4161-DvGamma-DvKhat-first-source-coefficient-or-QAP-parent-signature.md",
        "Delta_K := K_hat - K_metric[Gamma_eff],",
        "Existing Khat residual split.",
    ),
    (
        "SRC4340_04_DvKhat_split",
        FORMAL / "315-PPC4161-DvGamma-DvKhat-first-source-coefficient-or-QAP-parent-signature.md",
        "D_v K_hat = D_v Delta_K + D_v K_metric[Gamma_eff].",
        "Existing D_v Khat split.",
    ),
    (
        "SRC4340_05_longitudinal_identity",
        FORMAL / "352-PPC4161-open-tail-PiPPN-metric-transfer-derivation-or-R10-parent-alpha-fill.md",
        "partial_mu K_L^{mu nu}=-q_loc^nu",
        "Algebraic divergence-right-inverse precedent.",
    ),
    (
        "SRC4340_06_metric_response_slot",
        FORMAL / "352-PPC4161-open-tail-PiPPN-metric-transfer-derivation-or-R10-parent-alpha-fill.md",
        "h_MTS,mu nu=G_metric^bc C_gK P_E[K_L+K_perp]_mu nu",
        "Metric-response slot that must be parent-owned, not fitted.",
    ),
    (
        "SRC4340_07_cGamma_profile",
        FORMAL / "353-PPC4161-source-Sq-qprofile-kernel-and-metric-green-coupling-or-R10-alpha-parent-pivot.md",
        "q_loc^nu=P_loc[nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}]",
        "Gamma/Khat q-profile source being reduced.",
    ),
    (
        "SRC4340_08_double_zero_fallback",
        FORMAL / "316-PPC4161-DvGamma-m-Lcg-zero-or-first-coefficient-source-row.md",
        "D_v Gamma_eff|_* = 0",
        "Double-zero remains a fallback if Khat right-inverse ownership does not close.",
    ),
    (
        "SRC4340_09_trace_identity",
        FORMAL / "324-PPC4161-smooth-Hilbert-volume-domain-parent-signature-or-worldtube-flux-profile-row.md",
        "mu_tr := weak-lim_epsilon_to_0 g_in,epsilon dSigma,",
        "Trace-defect measure definition.",
    ),
    (
        "SRC4340_10_trace_bound",
        FORMAL / "324-PPC4161-smooth-Hilbert-volume-domain-parent-signature-or-worldtube-flux-profile-row.md",
        "N_inner <= ||mu_tr|| + ||B_src^A||",
        "Exterior/worldtube trace-defect envelope.",
    ),
    (
        "SRC4340_11_collar_lambda",
        FORMAL / "326-PPC4161-collar-no-concentration-signature-or-trace-bound-inputs.md",
        "A_U <= C_col (R_U + N_N + N_boundary) / lambda_*.",
        "Coercive no-concentration route.",
    ),
    (
        "SRC4340_12_inner_bound_inputs",
        FORMAL / "333-PPC4161-nonEM-inner-charge-domain-zero-or-QmH-bound-values.md",
        "lambda_* = Z_min lambda_1(D_loc)+M2_min-Eta_H > 0",
        "Trace-bound input schema.",
    ),
    (
        "SRC4340_13_single_count_budget",
        FORMAL / "334-PPC4161-nonHilbert-support-drift-history-bound-prioritizer.md",
        "N_rest_nonEM^canon := N_src_nonHilbert + N_drift_selector + N_history_transition + N_boundary_domain + N_N",
        "Single-count source budget downstream of N_inner.",
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


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "TH4340_0_define_KGamma",
            "name": "Gamma right-inverse metric lift",
            "statement": "Define K_Gamma[Gamma_eff] by nabla_mu K_Gamma[Gamma_eff]^(mu nu)=nabla^nu Gamma_eff on the chosen local collar with fixed gauge/boundary ownership.",
            "derivation": "Insert K_hat=K_Gamma+Delta_K into q_tr^nu=nabla^nu Gamma_eff-nabla_mu K_hat^(mu nu).",
            "result": "q_tr^nu=-nabla_mu Delta_K^(mu nu) up to connection/domain/boundary commutator terms.",
            "status": "DERIVED_IDENTITY_PARENT_SIGNATURE_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4340_1_primary_cancellation",
            "name": "Gamma/Khat paired cancellation",
            "statement": "If K_hat is the parent-owned K_Gamma right-inverse and gauge/domain variations commute with the right-inverse, then the Gamma trace leg cancels the metric-lift divergence before local projection.",
            "derivation": "D_v q_tr^nu=-nabla_mu D_v Delta_K^(mu nu)+C_RI^nu+C_conn^nu+B_boundary^nu, not a standalone D_v Gamma_eff bound.",
            "result": "The harsh linear D_v Gamma channel is bypassed on this branch; only Delta_K divergence and commutators remain.",
            "status": "REAL_ROUTE_ADVANCE_CONDITIONAL",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4340_2_kernel_zero_weaker_than_DeltaK_zero",
            "name": "DeltaK divergence-kernel zero",
            "statement": "Delta_K itself need not vanish; it is enough that P_loc nabla_mu D_v Delta_K^(mu nu)=0 and boundary/domain commutators vanish.",
            "derivation": "P_nonHilbert acts through q_tr, and q_tr sees the divergence of Delta_K, not its full tensor norm.",
            "result": "TT/radiative/harmonic or boundary-routed pieces may be harmless for static local PPN/R10 if they sit in the tested divergence/projection kernel.",
            "status": "DERIVED_WEAKER_ZERO_CONDITION",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4340_3_double_zero_fallback",
            "name": "Fallback if Khat right-inverse fails",
            "statement": "If K_hat is not parent-signed as K_Gamma, retain the 4300 double-zero Gamma route and the direct C_DvKhat coefficient route.",
            "derivation": "Use D_v Gamma_eff=L_cg^-2 F_m D_v m-2Gamma_eff D_vlnL_cg and the F=F_m=0 branch.",
            "result": "D_v Gamma is second order only after the parent lock signs F=F_m=0.",
            "status": "FALLBACK_RETAINED_NOT_PRIMARY",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4340_4_worldtube_readout_order_zero",
            "name": "Full-domain-before-readout worldtube zero",
            "statement": "If variation is performed on the smooth full Hilbert domain before exterior restriction, the artificial worldtube interface cancels in the weak form.",
            "derivation": "Interior and exterior normal traces have opposite signs; exterior readout is postprocessing, not a prevariation source excision.",
            "result": "P_off_worldtube_readout_order=0 on the full-domain/post-solve restriction branch.",
            "status": "CONDITIONAL_BRANCH_THEOREM",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4340_5_trace_defect_commutator",
            "name": "Trace-defect as readout-order commutator",
            "statement": "If exterior restriction/excision is taken before or during variation, the defect is mu_tr plus B_src^A.",
            "derivation": "mu_tr=weak-lim g_in,epsilon dSigma measures failure of smooth full-domain limiting to commute with exterior source readout.",
            "result": "N_inner<=||mu_tr||+||B_src^A||, with no cancellation credit.",
            "status": "DERIVED_BOUND_ROUTE_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "TH4340_6_lambda_no_concentration",
            "name": "Trace no-concentration input law",
            "statement": "If lambda_*>0 and S_U_not_inner, R_U and B_src^A vanish or are bounded, the trace defect is controlled by the collar elliptic estimate.",
            "derivation": "A_U<=C_col S_U_not_inner/lambda_* and N_inner<=C_N[K_U A_U+R_U]+||B_src^A||.",
            "result": "N_inner<=C_N[K_U C_col S_U_not_inner/lambda_*+R_U]+||B_src^A||.",
            "status": "DERIVED_REDUCED_BOUND_VALUES_MISSING",
            "valid_for_claim": "False",
        },
    ]


def residual_rows() -> List[Dict[str, str]]:
    return [
        {
            "residual_id": "RES4340_0_primary_qtr",
            "branch": "Khat right-inverse signed",
            "formula": "q_tr^nu=-nabla_mu Delta_K^(mu nu)+C_RI^nu+C_conn^nu+B_boundary^nu",
            "remaining_inputs": "Delta_K divergence kernel, right-inverse commutator C_RI, connection, boundary",
            "gain": "Gamma trace no longer scored as independent linear source",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RES4340_1_observable_DeltaK",
            "branch": "projected local tests",
            "formula": "Y_DeltaK<=C_obs||P_loc nabla_mu D_v Delta_K^(mu nu)||/a_ref + C_comm(||C_RI||+||C_conn||+||B_boundary||)",
            "remaining_inputs": "C_obs, C_comm, P_loc kernel certificate or finite norm",
            "gain": "tests only need projected divergence, not full Delta_K=0",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RES4340_2_fallback_DvGamma",
            "branch": "Khat right-inverse unsigned",
            "formula": "Y_Gamma<=C_gamma_quad[Delta_m Delta_Dv_m+Delta_m^2 Delta_DvlnL]+C_DvKhat_total",
            "remaining_inputs": "F_2, lambda_m, Delta_m, Delta_Dv_m, Delta_DvlnL, C_DvKhat_total",
            "gain": "keeps double-zero fallback without using it as the primary route",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RES4340_3_worldtube_zero_branch",
            "branch": "full-domain before exterior readout",
            "formula": "N_inner=0 if D_m includes W_H, no direct m-boundary charge, and restriction happens after variation",
            "remaining_inputs": "parent source-domain signature, same-worldtube readout-order contract",
            "gain": "kills P_off_worldtube without numeric fitting",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RES4340_4_worldtube_bound_branch",
            "branch": "exterior/worldtube trace defect",
            "formula": "N_inner<=C_N[K_U C_col S_U_not_inner/lambda_*+R_U]+||B_src^A||",
            "remaining_inputs": "lambda_*, C_N, K_U, C_col, S_U_not_inner, R_U, B_src^A",
            "gain": "source-domain ambiguity becomes a scoreable finite row",
            "valid_for_claim": "False",
        },
        {
            "residual_id": "RES4340_5_first_local_bound_vector",
            "branch": "combined first two P_leak channels",
            "formula": f"Y_4340<=Y_DeltaK+Y_trace, require PPN_gamma<={Y_GAMMA_LIMIT}, PPN_beta<={Y_BETA_LIMIT}, clock<={Y_CLOCK_LIMIT} after arena projection",
            "remaining_inputs": "arena projection matrices plus all rows above",
            "gain": "first two P_leak channels can now feed a no-cancellation local-bound runner",
            "valid_for_claim": "False",
        },
    ]


def input_rows() -> List[Dict[str, str]]:
    return [
        {
            "input_id": "IN4340_0_KGamma_parent",
            "symbol": "K_hat=K_Gamma[Gamma_eff]",
            "definition": "parent-signed metric-lift/right-inverse ownership satisfying nabla_mu K_Gamma^(mu nu)=nabla^nu Gamma_eff",
            "status": "MISSING_PARENT_SIGNATURE",
            "next_action": "prove Khat is constrained/defined by the same right-inverse used in the local metric response",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4340_1_CRI",
            "symbol": "C_RI",
            "definition": "commutator of D_v, nabla, boundary/gauge choice and the K_Gamma right-inverse",
            "status": "MISSING_COMMUTATOR_ZERO_OR_BOUND",
            "next_action": "prove q-owned gauge/domain stability or source finite commutator norm",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4340_2_DeltaK_div",
            "symbol": "P_loc div D_v Delta_K",
            "definition": "observable projected divergence of the metric-response mismatch tensor",
            "status": "MISSING_KERNEL_CERTIFICATE_OR_BOUND",
            "next_action": "prove TT/radiative/boundary-routed kernel membership or fill C_DeltaK_div",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4340_3_lambda_star",
            "symbol": "lambda_*",
            "definition": "positive collar coercivity floor, lambda_*=Z_min lambda_1(D_loc)+M2_min-Eta_H",
            "status": "FORMULA_READY_VALUE_UNSOURCED",
            "next_action": "derive/source Z_min, lambda_1(D_loc), M2_min, Eta_H and prove positivity",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4340_4_SU_not_inner",
            "symbol": "S_U_not_inner",
            "definition": "collar forcing numerator with N_inner excluded to prevent circular trace bounds",
            "status": "FORMULA_READY_COMPONENT_VALUES_MISSING",
            "next_action": "assemble non-inner residual components from N_rest_nonEM, R_U, N_N and boundary rows",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4340_5_mu_tr_BsrcA",
            "symbol": "mu_tr, B_src^A",
            "definition": "trace-defect measure and exterior source-boundary injection",
            "status": "MISSING_ZERO_THEOREM_OR_VALUE",
            "next_action": "prove full-domain post-solve restriction branch or source finite trace/profile row",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4340_6_arena_projection",
            "symbol": "Pi_4340_to_local_tests",
            "definition": "PPN/R10/clock/orbital/WEP projection constants for DeltaK divergence and trace-defect rows",
            "status": "MISSING_ARENA_PROJECTION",
            "next_action": "build first nonclaim local-bound runner only after symbolic rows are source-backed",
            "valid_for_claim": "False",
        },
    ]


def branch_rows() -> List[Dict[str, str]]:
    return [
        {
            "branch_id": "BR4340_0_best_clean",
            "branch": "Khat right-inverse plus full-domain source",
            "conditions": "K_hat=K_Gamma, C_RI=C_conn=B_boundary=0, P_loc div D_v Delta_K=0, full-domain readout before restriction",
            "output": "first two P_leak channels vanish conditionally",
            "status": "BEST_DERIVATION_ROUTE_PARENT_SIGNATURE_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BR4340_1_metric_kernel",
            "branch": "nonzero Delta_K but divergence/projection silent",
            "conditions": "Delta_K lies in static local test divergence kernel or boundary-routed sector",
            "output": "P_nonHilbert channel quiet even with Delta_K tensor nonzero",
            "status": "WEAKER_THAN_DELTAK_ZERO",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BR4340_2_right_inverse_unsigned",
            "branch": "Khat ownership not signed",
            "conditions": "K_Gamma parent identity missing",
            "output": "fall back to D_v Gamma double-zero plus direct D_v Khat coefficient",
            "status": "FALLBACK_NOT_CLAIM",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BR4340_3_exterior_trace",
            "branch": "exterior/worldtube readout used before variation",
            "conditions": "source excision or restriction fails to commute with variation/limit",
            "output": "N_inner trace-defect bound retained",
            "status": "FINITE_BOUND_ROUTE",
            "valid_for_claim": "False",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4340_0_current",
            "branch_input": "current corpus",
            "action": "USE_DERIVED_SPLIT_KEEP_CLAIM_FALSE",
            "output": "primary route becomes Khat right-inverse cancellation plus trace-defect bound inputs",
            "claim_policy": "no local-GR/R10/PPN/clock/orbital claim",
        },
        {
            "runner_id": "RUN4340_1_parent_signature_future",
            "branch_input": "Khat right-inverse and full-domain readout signed",
            "action": "ALLOW_CONDITIONAL_FIRST_TWO_PLEAK_ZERO",
            "output": "P_nonHilbert and P_off_worldtube both quiet conditionally",
            "claim_policy": "still not full local GR until remaining five P_leak/source/projection gates close",
        },
        {
            "runner_id": "RUN4340_2_bound_future",
            "branch_input": "finite DeltaK divergence and trace-defect inputs sourced",
            "action": "ALLOW_NONCLAIM_LOCAL_BOUND_VECTOR",
            "output": "score Y_4340 against PPN/R10/clock/orbital budgets without cancellation",
            "claim_policy": "claim only if all projection constants and rows are real and below budgets",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4340_0",
            "forbidden_shortcut": "Demanding Delta_K=0 when only projected divergence silence is needed",
            "reason": "the local q_tr channel sees div Delta_K, not the full tensor",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4340_1",
            "forbidden_shortcut": "Claiming Gamma is harmless without Khat right-inverse ownership",
            "reason": "the cancellation requires K_hat=K_Gamma plus commutator/boundary silence",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4340_2",
            "forbidden_shortcut": "Using full-domain interface cancellation after choosing an exterior-only variational problem",
            "reason": "exterior solves must retain mu_tr/B_srcA trace defect rows",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4340_3",
            "forbidden_shortcut": "Treating lambda_* as positive because the formula exists",
            "reason": "positivity needs Z_min, lambda_1(D_loc), M2_min and Eta_H source/theorem rows",
            "status": "ACTIVE",
        },
        {
            "firewall_id": "FW4340_4",
            "forbidden_shortcut": "Promoting the first-two-channel closure to local GR",
            "reason": "remaining P_leak components and source equality/projection gates are still open",
            "status": "ACTIVE",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4340_0",
            "decision": DECISION,
            "reason": "the cleanest route is not tiny Gamma by itself; it is paired Gamma/Khat right-inverse cancellation plus a trace-defect readout-order theorem",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4340_0",
            "item": "Delta_K route",
            "status": "UPGRADED_TO_DIVERGENCE_KERNEL_PROBLEM",
            "notes": "need Khat right-inverse parent signature or projected div DeltaK bound",
        },
        {
            "status_id": "STAT4340_1",
            "item": "Gamma trace route",
            "status": "BYPASSED_ON_PRIMARY_BRANCH",
            "notes": "D_v Gamma cancels against div D_v K_Gamma if right-inverse branch signs",
        },
        {
            "status_id": "STAT4340_2",
            "item": "worldtube route",
            "status": "UPGRADED_TO_READOUT_ORDER_COMMUTATOR",
            "notes": "full-domain post-solve readout gives zero; exterior variational readout keeps trace defect",
        },
        {
            "status_id": "STAT4340_3",
            "item": "next target",
            "status": "PARENT_SIGNATURE_OR_FIRST_BOUND",
            "notes": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4340_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can K_hat be parent-signed as the Gamma right-inverse metric lift, or must C_DeltaK_div become the first source-backed finite local row?",
            "preferred_route": "prove K_hat=K_Gamma[Gamma_eff], right-inverse commutator silence, and projected div Delta_K=0",
            "fallback_route": "fill C_DeltaK_div, C_RI, C_conn, B_boundary, lambda_*, S_U_not_inner, mu_tr and B_srcA as nonclaim finite rows",
        }
    ]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 356 PPC4161 DvKhat DeltaK and worldtube trace-defect input fill

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove local GR, Newton, R10, PPN, clock safety, orbital safety, WEP safety, or full source-kernel membership for raw transition shells.

## Result

4340 makes a real step forward: `Delta_K=0` is stronger than the local problem actually needs.

Define a parent-owned metric lift `K_Gamma[Gamma_eff]` by:

```text
nabla_mu K_Gamma[Gamma_eff]^(mu nu) = nabla^nu Gamma_eff.
```

Then:

```text
K_hat = K_Gamma[Gamma_eff] + Delta_K

q_tr^nu
  = nabla^nu Gamma_eff - nabla_mu K_hat^(mu nu)
  = - nabla_mu Delta_K^(mu nu)
    + right-inverse/connection/boundary commutators.
```

So the primary route is not "make `D_v Gamma_eff` tiny". The cleaner route is **paired Gamma/Khat cancellation**. After that, local tests only see projected `div Delta_K` and commutator tails.

The parallel worldtube result is also sharper:

```text
full-domain variation before exterior readout -> interface flux cancels
exterior/worldtube variation/readout first -> N_inner <= ||mu_tr|| + ||B_src^A||
```

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role"])}

## Theorem Rows

{md_table(tables["theorems"], ["theorem_id", "name", "statement", "derivation", "result", "status", "valid_for_claim"])}

## Residual Rows

{md_table(tables["residuals"], ["residual_id", "branch", "formula", "remaining_inputs", "gain", "valid_for_claim"])}

## Input Rows

{md_table(tables["inputs"], ["input_id", "symbol", "definition", "status", "next_action", "valid_for_claim"])}

## Branch Runner

{md_table(tables["branches"], ["branch_id", "branch", "conditions", "output", "status", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "branch_input", "action", "output", "claim_policy"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "forbidden_shortcut", "reason", "status"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "notes"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4340 Y5-R2FR DvKhat DeltaK and worldtube trace-defect input fill

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

This is the useful move:

```text
if K_hat = K_Gamma[Gamma_eff] and div K_Gamma = grad Gamma_eff,
then q_tr = - div Delta_K + commutators.
```

So `Delta_K=0` is not required; projected `div Delta_K=0` is enough for the local channel. Worldtube leakage is likewise a readout-order commutator: full-domain-before-readout is quiet, exterior-first readout keeps `mu_tr` and `B_src^A`.

## Handoff

{md_table(tables["next"], ["next_target", "target_question", "preferred_route", "fallback_route"])}
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
                    "4340 improves the first P_leak route by deriving a paired Gamma/Khat cancellation law. "
                    "If K_hat is parent-signed as the right-inverse metric lift K_Gamma satisfying div K_Gamma=grad Gamma_eff, then q_tr reduces to -div Delta_K plus right-inverse, connection and boundary commutators. "
                    "Thus Delta_K=0 is stronger than necessary; projected div Delta_K=0 is enough for the tested non-Hilbert channel. "
                    "For the worldtube channel, 4340 separates full-domain-before-readout interface cancellation from exterior-first trace-defect leakage, retaining N_inner<=||mu_tr||+||B_src^A|| and the lambda_*/S_U_not_inner no-concentration bound. "
                    "No local-GR/R10/PPN/clock/orbital claim fires because parent signature and finite input rows remain open."
                ),
                "4340 source register, theorem rows, residual rows, input rows, branch runner, firewall, decision, status, next-target and validation CSV.",
                "private_Gamma_Khat_right_inverse_cancellation_and_trace_defect_bound_route_nonclaim",
                "Prove K_hat=K_Gamma[Gamma_eff] and projected div Delta_K=0, or fill C_DeltaK_div/C_RI plus trace-defect finite rows.",
                "Demanding Delta_K=0 when projected divergence silence is enough; claiming Gamma cancellation without right-inverse ownership; using full-domain interface cancellation in exterior-first variational solves; treating lambda_* as positive without source rows; or claiming local GR while other P_leak/projection gates remain open.",
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

    add("VAL4340_sources_exist", "all source paths exist", all(r["path_exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4340_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4340_right_inverse_theorem", "right-inverse theorem row exists", any("right-inverse" in r["name"] and "q_tr^nu=-nabla_mu Delta_K" in r["result"] for r in tables["theorems"]), "theorems")
    add("VAL4340_bypasses_standalone_DvGamma", "primary route bypasses standalone DvGamma", any("Gamma trace no longer scored as independent linear source" in r["gain"] for r in tables["residuals"]), "residuals")
    add("VAL4340_weaker_than_DeltaK_zero", "projected divergence condition weaker than DeltaK zero", any("need not vanish" in r["statement"] for r in tables["theorems"]), "theorems")
    add("VAL4340_trace_commutator", "trace-defect commutator theorem exists", any("mu_tr" in r["statement"] and "B_src" in r["result"] for r in tables["theorems"]), "theorems")
    add("VAL4340_lambda_bound", "lambda no-concentration bound exists", any("lambda_*" in r["statement"] and "S_U_not_inner" in r["result"] for r in tables["theorems"]), "theorems")
    add("VAL4340_inputs_include_DeltaK", "DeltaK divergence input exists", any(r["symbol"] == "P_loc div D_v Delta_K" for r in tables["inputs"]), "inputs")
    add("VAL4340_inputs_include_trace", "trace input exists", any("mu_tr" in r["symbol"] and "B_src" in r["symbol"] for r in tables["inputs"]), "inputs")
    add("VAL4340_claim_flags_false", "all valid_for_claim flags false", all(r.get("valid_for_claim", "False") == "False" for table in tables.values() for r in table if "valid_for_claim" in r), "all_tables")
    add("VAL4340_current_runner_nonclaim", "current runner keeps claim false", any(r["runner_id"] == "RUN4340_0_current" and "CLAIM_FALSE" in r["action"] for r in tables["runner"]), "runner")
    add("VAL4340_firewalls", "firewalls cover DeltaK and exterior misuse", any("Delta_K=0" in r["forbidden_shortcut"] for r in tables["firewall"]) and any("exterior-only" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4340_docs_exist", "formal and post docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4340_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4340_post_result", "post doc states right-inverse result", "q_tr = - div Delta_K" in read_text(DOC_PATH), "post")
    add("VAL4340_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4340_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4340_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4340_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4340_SOURCE_REGISTER.csv",
        "theorems": SOURCE_DIR / "P8_Y5_R2FR_4340_THEOREM_ROWS.csv",
        "residuals": SOURCE_DIR / "P8_Y5_R2FR_4340_RESIDUAL_ROWS.csv",
        "inputs": SOURCE_DIR / "P8_Y5_R2FR_4340_REQUIRED_INPUTS.csv",
        "branches": SOURCE_DIR / "P8_Y5_R2FR_4340_BRANCH_RUNNER.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4340_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4340_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4340_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4340_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4340_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "theorems": theorem_rows(),
        "residuals": residual_rows(),
        "inputs": input_rows(),
        "branches": branch_rows(),
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
## PPC4161 4340 Gamma/Khat right-inverse cancellation

Marker: `{MARKER}`

4340 upgrades the first P_nonHilbert leak route. Define `K_Gamma[Gamma_eff]` by:

```text
nabla_mu K_Gamma[Gamma_eff]^(mu nu)=nabla^nu Gamma_eff.
```

Then, if `K_hat=K_Gamma+Delta_K`,

```text
q_tr^nu=-nabla_mu Delta_K^(mu nu)+C_RI^nu+C_conn^nu+B_boundary^nu.
```

This means `Delta_K=0` is stronger than needed: the local branch only needs projected divergence silence or a finite projected divergence bound.

The worldtube channel is also sharpened: full-domain variation before readout cancels artificial interface flux; exterior-first variation/readout retains `mu_tr` and `B_src^A`, bounded by the `lambda_*`/`S_U_not_inner` collar law.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4340 packet Gamma/Khat right-inverse cancellation

Marker: `{PACKET_MARKER}`

Packet update: the clean local route is paired Gamma/Khat cancellation. If Khat is the parent-owned right-inverse lift of Gamma, the open transition current is controlled by projected `div Delta_K` and commutator/boundary tails, not by an independent linear Gamma profile. Worldtube leakage is now a readout-order commutator: full-domain-before-readout zero, exterior-first trace-defect bound.
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
