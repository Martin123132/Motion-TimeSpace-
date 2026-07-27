from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4336"
CLAIM_ID = "L-177"
BRANCH = "MTS_R2FR_Y5_OPEN_TAIL_PIPPN_METRIC_TRANSFER_DERIVATION_OR_R10_PARENT_ALPHA_FILL_4336"
DECISION = "OPEN_TAIL_PIPPN_OPERATOR_FACTORISATION_DERIVED_NUMERIC_MATRIX_BLOCKED_BY_Q_PROFILE_METRIC_COUPLING_AND_BOUNDARY_DATA_NONCLAIM"
MARKER = "PPC4161_OPEN_TAIL_PIPPN_METRIC_TRANSFER_DERIVATION_OR_R10_PARENT_ALPHA_FILL_4336"
PACKET_MARKER = "PPC4161_PACKET_OPEN_TAIL_PIPPN_METRIC_TRANSFER_DERIVATION_OR_R10_PARENT_ALPHA_FILL_4336"
NEXT_TARGET = "4337-Y5-R2FR-source-Sq-qprofile-kernel-and-metric-green-coupling-or-R10-alpha-parent-pivot.md"

FORMAL_PATH = FORMAL / "352-PPC4161-open-tail-PiPPN-metric-transfer-derivation-or-R10-parent-alpha-fill.md"
DOC_PATH = POST / "4336-Y5-R2FR-open-tail-PiPPN-metric-transfer-derivation-or-R10-parent-alpha-fill.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4336_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")


SOURCES = [
    (
        "SRC4336_00_next",
        SOURCE_DIR / "P8_Y5_R2FR_4335_NEXT_TARGET.csv",
        "open-tail Pi_PPN",
        "4335 handoff: derive open-tail Pi_PPN before R10 pivot.",
    ),
    (
        "SRC4336_01_4334_Topen",
        FORMAL / "350-PPC4161-local-test-projection-matrix-source-contract-or-R10-PPN-smoke-runner.md",
        "T_open :=",
        "Open-tail vector basis feeding local arena projections.",
    ),
    (
        "SRC4336_02_4335_metric_blocker",
        FORMAL / "351-PPC4161-first-source-backed-PiPPN-or-R10-alpha-lambda-projection-row.md",
        "MISSING_LOCAL_METRIC_TRANSFER_MATRIX",
        "Open-tail PPN numeric scoring blocker from 4335.",
    ),
    (
        "SRC4336_03_59_chain",
        FORMAL / "59-local-ppn-branch-framework.md",
        "q_loc^nu nonzero -> K_tr,loc",
        "Local branch chain from q_loc to tensor source to metric observables.",
    ),
    (
        "SRC4336_04_61_K_ansatz",
        FORMAL / "61-local-ppn-tensor-ansatz.md",
        "K_L,loc^{mu nu}[A] =",
        "Longitudinal symmetric tensor ansatz.",
    ),
    (
        "SRC4336_05_61_box",
        FORMAL / "61-local-ppn-tensor-ansatz.md",
        "Box A_loc^nu = q_loc^nu.",
        "Green-function equation for the longitudinal owner field.",
    ),
    (
        "SRC4336_06_61_boundary",
        FORMAL / "61-local-ppn-tensor-ansatz.md",
        "inner and outer boundary conditions",
        "Boundary data warning for A_loc Green solution.",
    ),
    (
        "SRC4336_07_63_qbound",
        FORMAL / "63-local-q-profile-bound.md",
        "|q_loc|",
        "Physical q_loc source-amplitude bound.",
    ),
    (
        "SRC4336_08_63_sppn",
        FORMAL / "63-local-q-profile-bound.md",
        "S_PPN ~ |q_loc| R_shell ell_tr^2 / u_shell.",
        "Shell-scale PPN residual source proxy.",
    ),
    (
        "SRC4336_09_64_limits",
        FORMAL / "64-local-q-profile-bound-first-results.md",
        "tightest_linear_M_tr_max_for_phi",
        "Numerical pressure on linear and quadratic local memory profiles.",
    ),
    (
        "SRC4336_10_66_extremum",
        FORMAL / "66-local-extremum-amplitude-law-first-results.md",
        "F_1 = F'(m_L) = 0",
        "Conditional survival route for the q_loc source profile.",
    ),
    (
        "SRC4336_11_79_double_zero",
        FORMAL / "79-local-fixed-point-mechanism.md",
        "This gives the required double zeros.",
        "Conditional fixed-point mechanism that could source the local double zeros.",
    ),
    (
        "SRC4336_12_88_lcg",
        FORMAL / "88-Lcg-rule-gate.md",
        "conditional_pass_count = 3",
        "Coarse-graining rule gate relevant to ell_tr/L_cg.",
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


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path)
    if CLAIM_ID in existing:
        return
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                CLAIM_ID,
                "local_gr",
                "4336 derives the open-tail Pi_PPN transfer as a symbolic weak-field operator factorisation rather than an identity or fitted matrix. In the local branch, T_open first sources q_loc through an arena source kernel S_q; the longitudinal owner field then solves Box A_loc=q_loc; K_L[A]=-(partial^mu A^nu+partial^nu A^mu)+eta^{mu nu}partial_alpha A^alpha has divergence -q_loc; the metric perturbation must come from a parent-signed metric Green operator and coupling C_gK applied to K_L plus any transverse K_perp; and the PPN residual vector is the PPN projection of that metric. Thus Pi_PPN = P_PPN G_metric C_gK [K_L G_Box S_q + S_perp] is derived as the required transfer envelope. Numeric gamma/beta/preferred-frame scoring remains blocked by missing S_q kernel, Green/boundary constants, metric-response coupling, K_perp control, and PPN normalization. R10 alpha(lambda) remains a fallback, still blocked by parent alpha coefficients and claim-valid bound curve inputs.",
                "4336 source register, operator factorisation rows, transfer-bound rows, nonclaim smoke rows, blocker rows, runner, firewall, decision, status, next-target and validation CSV.",
                "private_open_tail_PiPPN_operator_factorisation_derived_numeric_matrix_blocked_nonclaim",
                "Source the S_q q-profile kernel and metric Green/coupling constants, or pivot to R10 parent alpha(lambda) coefficients if Pi_PPN numeric transfer remains unavailable.",
                "Using the symbolic operator as a numeric PPN pass; fitting Pi_PPN after seeing residuals; setting C_gK=1 without parent normalization; dropping K_perp by assumption; scoring R10 with missing parent coefficients or anchor-only alpha(lambda) bounds.",
            ]
        )


def source_rows() -> List[Dict[str, str]]:
    rows = []
    for source_id, path, needle, role in SOURCES:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(needle in text),
                "line_number": find_line(path, needle),
                "role": role,
            }
        )
    return rows


def operator_rows() -> List[Dict[str, str]]:
    return [
        {
            "operator_id": "OP4336_0_tail_to_q",
            "stage": "open tail to local current",
            "operator_statement": "q_loc^nu(x)=S_q^nu[T_open](x)",
            "derived_from": "4334 T_open vector plus 63 q_loc profile definition",
            "numeric_status": "symbolic_only",
            "blocking_input": "MISSING_SQ_QLOC_KERNEL",
            "valid_for_claim": "False",
        },
        {
            "operator_id": "OP4336_1_q_to_A",
            "stage": "local current to longitudinal owner field",
            "operator_statement": "A_loc^nu=G_Box^bc q_loc^nu, with Box A_loc^nu=q_loc^nu",
            "derived_from": "61 longitudinal tensor ansatz",
            "numeric_status": "operator_derived_boundary_constants_missing",
            "blocking_input": "MISSING_BOX_GREEN_BOUNDARY_CONSTANT",
            "valid_for_claim": "False",
        },
        {
            "operator_id": "OP4336_2_A_to_KL",
            "stage": "owner field to longitudinal tensor",
            "operator_statement": "K_L^{mu nu}[A]=-(partial^mu A^nu+partial^nu A^mu)+eta^{mu nu}partial_alpha A^alpha; partial_mu K_L^{mu nu}=-q_loc^nu",
            "derived_from": "61 algebraic divergence identity",
            "numeric_status": "algebraic_operator_derived",
            "blocking_input": "NONE_FOR_LONGITUDINAL_IDENTITY",
            "valid_for_claim": "False",
        },
        {
            "operator_id": "OP4336_3_K_to_metric",
            "stage": "local tensor to metric perturbation",
            "operator_statement": "h_MTS,mu nu=G_metric^bc C_gK P_E[K_L+K_perp]_mu nu",
            "derived_from": "59 metric-observable contract plus 61 Green-function warning",
            "numeric_status": "parent_coupling_and_metric_green_open",
            "blocking_input": "MISSING_METRIC_GREEN_OPERATOR_AND_CgK_COUPLING",
            "valid_for_claim": "False",
        },
        {
            "operator_id": "OP4336_4_metric_to_PPN",
            "stage": "metric perturbation to PPN residual vector",
            "operator_statement": "R_PPN=P_PPN[h_MTS;U,frame,clock,rods]",
            "derived_from": "59 PPN metric contract",
            "numeric_status": "projection_defined_normalization_missing",
            "blocking_input": "MISSING_PPN_PROJECTION_NORMALIZATION",
            "valid_for_claim": "False",
        },
        {
            "operator_id": "OP4336_5_combined_PiPPN",
            "stage": "combined open-tail transfer matrix",
            "operator_statement": "Pi_PPN=P_PPN G_metric^bc C_gK P_E[(K_L G_Box^bc S_q)+S_perp]",
            "derived_from": "composition of OP4336_0 through OP4336_4",
            "numeric_status": "symbolic_factorisation_derived_numeric_matrix_blocked",
            "blocking_input": "MISSING_SQ_QLOC_KERNEL;MISSING_METRIC_GREEN_OPERATOR_AND_CgK_COUPLING;MISSING_KPERP_SOURCE_OR_ZERO",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> List[Dict[str, str]]:
    return [
        {
            "bound_id": "BND4336_0_q_profile_source_bound",
            "quantity": "abs(q_loc)",
            "bound_statement": "abs(q_loc)<=P_loc{L_cg^-2[abs(F1)M_tr/ell_tr+0.5abs(F2)M_tr^2/ell_tr]+C_K abs(b_mem)M_tr^2/ell_tr^3}",
            "source_basis": "63 local q_profile bound",
            "numeric_status": "formula_source_backed_inputs_not_derived",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4336_1_shell_SPPN",
            "quantity": "S_PPN",
            "bound_statement": "S_PPN~abs(q_loc) R_shell ell_tr^2/u_shell",
            "source_basis": "63 shell-scale PPN residual estimate",
            "numeric_status": "order_bound_only",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4336_2_linear_danger",
            "quantity": "linear source branch",
            "bound_statement": "S_PPN,linear~abs(F1)M_tr/u_shell; internal gate requires abs(F1)M_tr<=9.87e-14 at AU benchmark",
            "source_basis": "64 first q-profile results",
            "numeric_status": "benchmark_pressure_not_parent_derivation",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4336_3_quadratic_survival",
            "quantity": "quadratic fixed-point branch",
            "bound_statement": "if F1=0 then M_tr<=sqrt(S_gate u/[P_loc C_quad(e)]), with e=ell_tr/L_cg and C_quad=0.5abs(F2)re+C_Kabs(b_mem)r/e",
            "source_basis": "65/66 extremum amplitude law",
            "numeric_status": "conditional_survival_envelope",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4336_4_PPN_residual_norm",
            "quantity": "R_PPN_open",
            "bound_statement": "||R_PPN_open||<=||P_PPN||||G_metric C_gK P_E||[||K_L||||G_Box||||S_q||+||S_perp||]||T_open||",
            "source_basis": "4336 operator factorisation",
            "numeric_status": "operator_norm_envelope_no_constants",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "BND4336_5_gamma_beta_envelope",
            "quantity": "delta_gamma and delta_beta",
            "bound_statement": "abs(delta_gamma)<=C_gamma C_metric abs(C_gK)(C_KL C_Box ||S_q T_open||+||Kperp||); abs(delta_beta)<=C_beta times same source envelope plus second-order normalization terms",
            "source_basis": "59 PPN contract plus 61/63 transfer chain",
            "numeric_status": "coefficient_envelope_only",
            "valid_for_claim": "False",
        },
    ]


def smoke_rows() -> List[Dict[str, str]]:
    return [
        {
            "smoke_id": "SMK4336_0_symbolic_factorisation",
            "arena": "open-tail PPN",
            "input_status": "source-backed equations present",
            "test": "combined operator contains S_q, G_Box, K_L, G_metric, C_gK, P_PPN",
            "result": "PASS_NONCLAIM_SYMBOLIC_DERIVATION",
            "numeric_score": "not_run",
            "valid_for_claim": "False",
        },
        {
            "smoke_id": "SMK4336_1_numeric_gamma_beta",
            "arena": "open-tail PPN",
            "input_status": "missing source kernels/constants",
            "test": "score delta_gamma/delta_beta from Pi_PPN T_open",
            "result": "BLOCKED",
            "numeric_score": "not_run",
            "valid_for_claim": "False",
        },
        {
            "smoke_id": "SMK4336_2_R10_alpha_pivot",
            "arena": "R10 alpha(lambda)",
            "input_status": "parent alpha coefficients and claim-valid bound curve still absent",
            "test": "score alpha_pred(lambda)<=alpha_bound(lambda)",
            "result": "BLOCKED",
            "numeric_score": "not_run",
            "valid_for_claim": "False",
        },
    ]


def blocker_rows() -> List[Dict[str, str]]:
    return [
        {
            "blocker_id": "BLK4336_0_Sq_kernel",
            "blocked_route": "numeric Pi_PPN open-tail matrix",
            "missing_input": "MISSING_SQ_QLOC_KERNEL",
            "needed_for_release": "source-backed map from T_open components to q_loc^nu(x), including local profile, shell width, boundary amplitude and sector weights",
            "status": "blocked",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK4336_1_box_green",
            "blocked_route": "q_loc to A_loc amplitude",
            "missing_input": "MISSING_BOX_GREEN_BOUNDARY_CONSTANT",
            "needed_for_release": "static/retarded Green-function choice and inner/outer boundary conditions for A_loc^nu",
            "status": "blocked",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK4336_2_metric_coupling",
            "blocked_route": "K_tr to metric perturbation",
            "missing_input": "MISSING_METRIC_GREEN_OPERATOR_AND_CgK_COUPLING",
            "needed_for_release": "parent-signed weak-field equation fixing how K_tr,loc sources h_mu_nu and its coupling normalization",
            "status": "blocked",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK4336_3_Kperp",
            "blocked_route": "transverse/homogeneous source safety",
            "missing_input": "MISSING_KPERP_SOURCE_OR_ZERO",
            "needed_for_release": "derive K_perp=0, order-three suppression, or independent PPN-safe bound",
            "status": "blocked",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK4336_4_ppn_normalization",
            "blocked_route": "gamma/beta/preferred-frame readout",
            "missing_input": "MISSING_PPN_PROJECTION_NORMALIZATION",
            "needed_for_release": "same metric/clock/rod normalization against Newtonian U used by local tests",
            "status": "blocked",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK4336_5_R10_parent",
            "blocked_route": "R10 alpha(lambda) fallback",
            "missing_input": "MISSING_R10_PARENT_ALPHA_COEFFICIENTS_AND_CLAIM_VALID_BOUND_CURVE",
            "needed_for_release": "Z_X, M_X^2, K_X, Qbar_XH, qbar_XT/P_A plus full source-backed alpha(lambda) curve",
            "status": "blocked",
            "valid_for_claim": "False",
        },
    ]


def formula_rows() -> List[Dict[str, str]]:
    return [
        {
            "formula_id": "F4336_0_Topen_to_q",
            "name": "source-kernel definition",
            "formula": "q_loc^nu(x)=S_q^nu[T_open](x)",
            "status": "DERIVED_INTERFACE_NUMERIC_KERNEL_OPEN",
        },
        {
            "formula_id": "F4336_1_longitudinal_green",
            "name": "owner-field equation",
            "formula": "Box A_loc^nu=q_loc^nu; A_loc^nu=G_Box^bc q_loc^nu",
            "status": "SOURCE_BACKED_FROM_61",
        },
        {
            "formula_id": "F4336_2_K_identity",
            "name": "longitudinal tensor identity",
            "formula": "K_L^{mu nu}=-(partial^mu A^nu+partial^nu A^mu)+eta^{mu nu}partial_alpha A^alpha => partial_mu K_L^{mu nu}=-q_loc^nu",
            "status": "ALGEBRAIC_IDENTITY",
        },
        {
            "formula_id": "F4336_3_metric_response",
            "name": "metric-response coupling slot",
            "formula": "h_MTS=G_metric^bc C_gK P_E[K_L+Kperp]",
            "status": "DERIVED_SLOT_PARENT_COUPLING_OPEN",
        },
        {
            "formula_id": "F4336_4_PiPPN",
            "name": "combined open-tail PPN transfer",
            "formula": "Pi_PPN=P_PPN G_metric^bc C_gK P_E[(K_L G_Box^bc S_q)+S_perp]",
            "status": "SYMBOLIC_FACTORISATION_DERIVED_NUMERIC_MATRIX_BLOCKED",
        },
        {
            "formula_id": "F4336_5_RPPN",
            "name": "open-tail residual",
            "formula": "R_PPN_open=Pi_PPN T_open",
            "status": "NONCLAIM_OPERATOR_STATEMENT",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4336_0_symbolic_operator",
            "branch_input": "source-backed local q/A/K equations plus 4334 T_open",
            "action": "RUN_SYMBOLIC_FACTORISATION_CHECK",
            "output": "operator chain derived and recorded",
            "claim_policy": "valid_for_claim=false; no numeric PPN claim",
        },
        {
            "runner_id": "RUN4336_1_numeric_PPN",
            "branch_input": "open-tail T_open with missing S_q/G_metric/C_gK/Kperp constants",
            "action": "BLOCK_NUMERIC_SCORE",
            "output": "blocked_missing_q_profile_metric_coupling_boundary_data",
            "claim_policy": "no local PPN claim",
        },
        {
            "runner_id": "RUN4336_2_R10_fallback",
            "branch_input": "R10 alpha(lambda) fallback",
            "action": "BLOCK_NUMERIC_SCORE",
            "output": "blocked_missing_parent_alpha_coefficients_and_claim_valid_bound_curve",
            "claim_policy": "no R10 claim",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4336_0_symbolic_overclaim",
            "forbidden_shortcut": "treat symbolic Pi_PPN factorisation as numeric PPN pass",
            "reason": "operator constants and source kernels are not filled",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4336_1_coupling_guess",
            "forbidden_shortcut": "set C_gK=1 or absorb it into G_N without parent derivation",
            "reason": "this is the coupling bottleneck and cannot be guessed",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4336_2_identity_projection",
            "forbidden_shortcut": "use identity Pi_PPN or fitted arena matrix",
            "reason": "Pi_PPN must be derived from q profile, Green operators, coupling, metric and PPN projection",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4336_3_drop_Kperp",
            "forbidden_shortcut": "delete K_perp because longitudinal identity works",
            "reason": "K_perp must be zero by parent law or separately bounded",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4336_4_R10_anchor_claim",
            "forbidden_shortcut": "pivot to R10 using symbolic alpha rows or anchor-only bounds",
            "reason": "R10 still needs parent coefficients and a claim-valid alpha(lambda) curve",
            "status": "BLOCK",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "summary": "Open-tail Pi_PPN is now a derived symbolic operator factorisation, not a mystery placeholder. Numeric scoring remains blocked because the q-profile kernel, metric Green/coupling normalization, boundary constants, K_perp control and PPN normalization are not source-backed.",
            "next_action": NEXT_TARGET,
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4336_0_operator",
            "item": "open-tail Pi_PPN transfer",
            "status": "SYMBOLIC_FACTORISATION_DERIVED",
            "notes": "Pi_PPN=P_PPN G_metric C_gK P_E[(K_L G_Box S_q)+S_perp]",
        },
        {
            "status_id": "STAT4336_1_coupling",
            "item": "metric response coupling",
            "status": "OPEN_CRITICAL",
            "notes": "C_gK and G_metric are the coupling/metric-response bottleneck",
        },
        {
            "status_id": "STAT4336_2_q_profile",
            "item": "S_q q-profile kernel",
            "status": "OPEN_CRITICAL",
            "notes": "needs physical q_loc(x), amplitude, boundary profile and source weights",
        },
        {
            "status_id": "STAT4336_3_R10",
            "item": "R10 alpha(lambda) fallback",
            "status": "BLOCKED",
            "notes": "parent alpha coefficients and claim-valid bound curve still missing",
        },
        {
            "status_id": "STAT4336_4_next",
            "item": "next target",
            "status": "NEXT_TARGET",
            "notes": "source S_q and metric coupling first; pivot to R10 only if that stalls",
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4336_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can S_q and C_gK/G_metric be derived or source-filled enough to make Pi_PPN numeric, or must the work pivot to R10 parent alpha coefficients?",
            "preferred_route": "derive/source the q-profile kernel S_q and weak-field metric coupling C_gK from the parent local equations, then compute gamma/beta/preferred-frame rows",
            "fallback_route": "fill R10 Z_X, M_X^2, K_X, Qbar_XH, qbar_XT/P_A and alpha_bound(lambda) rows for a nonclaim alpha smoke score",
        }
    ]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 352 - PPC4161 open-tail PiPPN metric-transfer derivation or R10 parent-alpha fill

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4336 does **not** prove public local GR, PPN, R10, WEP, clock safety, orbital safety, Newtonian recovery, Maxwell/QED, charge normalization, `G_N`, or any empirical local-test pass.

It does move the work forward: the open-tail PPN matrix is no longer an empty placeholder. Under the weak-field local branch already developed in files 59, 61, 63 and 64, the transfer must factor through:

```text
T_open
  -> q_loc^nu(x)=S_q^nu[T_open](x)
  -> A_loc^nu=G_Box^bc q_loc^nu
  -> K_L^{{mu nu}}[A]
  -> h_MTS,mu nu=G_metric^bc C_gK P_E[K_L+Kperp]_mu nu
  -> R_PPN=P_PPN[h_MTS;U,frame,clock,rods].
```

So the open-tail transfer operator is:

```text
Pi_PPN =
  P_PPN G_metric^bc C_gK P_E[
    (K_L G_Box^bc S_q) + S_perp
  ].
```

That is a real derivation of the transfer envelope. It is not yet a numeric matrix.

The important exposed bottleneck is the coupling slot:

```text
C_gK = local metric-response normalization from K_tr,loc into h_mu_nu.
```

This cannot be guessed, hidden in `G_N`, or fitted after seeing residuals.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role"])}

## Operator Factorisation

{md_table(tables["operators"], ["operator_id", "stage", "operator_statement", "derived_from", "numeric_status", "blocking_input", "valid_for_claim"])}

## Transfer Bounds

{md_table(tables["bounds"], ["bound_id", "quantity", "bound_statement", "source_basis", "numeric_status", "valid_for_claim"])}

## Smoke Rows

{md_table(tables["smoke"], ["smoke_id", "arena", "input_status", "test", "result", "numeric_score", "valid_for_claim"])}

## Blockers

{md_table(tables["blockers"], ["blocker_id", "blocked_route", "missing_input", "needed_for_release", "status", "valid_for_claim"])}

## Formula Rows

{md_table(tables["formulas"], ["formula_id", "name", "formula", "status"])}

## Runner

{md_table(tables["runner"], ["runner_id", "branch_input", "action", "output", "claim_policy"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "forbidden_shortcut", "reason", "status"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "notes"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4336 Y5-R2FR open-tail PiPPN metric-transfer derivation or R10 parent-alpha fill

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

The open-tail PPN transfer is now derived as a symbolic operator factorisation:

```text
Pi_PPN=P_PPN G_metric^bc C_gK P_E[(K_L G_Box^bc S_q)+S_perp].
```

This is progress, but it is nonclaim. The numeric matrix remains blocked by the q-profile kernel, metric Green/coupling normalization, boundary constants, `K_perp`, and PPN normalization.

## Bottleneck

{md_table(tables["status"], ["item", "status", "notes"])}

## Blockers

{md_table(tables["blockers"], ["blocked_route", "missing_input", "needed_for_release", "status"])}

## Next

{md_table(tables["next"], ["next_target", "target_question", "preferred_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


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

    all_ops = " ".join(row["operator_statement"] for row in tables["operators"])
    combined = next(row for row in tables["operators"] if row["operator_id"] == "OP4336_5_combined_PiPPN")
    required_factors = ["P_PPN", "G_metric", "C_gK", "K_L", "G_Box", "S_q", "S_perp"]

    add("VAL4336_sources_exist", "all source paths exist", all(r["path_exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4336_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4336_operator_factors", "combined Pi_PPN contains all required factors", all(factor in combined["operator_statement"] for factor in required_factors), combined["operator_statement"])
    add("VAL4336_q_to_K_chain", "q_loc to A_loc to K_L chain present", all(token in all_ops for token in ["q_loc", "A_loc", "K_L"]), "operators")
    add("VAL4336_metric_coupling_exposed", "C_gK coupling blocker exists", any(r["missing_input"] == "MISSING_METRIC_GREEN_OPERATOR_AND_CgK_COUPLING" for r in tables["blockers"]), "blockers")
    add("VAL4336_Sq_blocked", "S_q q-profile kernel blocker exists", any(r["missing_input"] == "MISSING_SQ_QLOC_KERNEL" for r in tables["blockers"]), "blockers")
    add("VAL4336_Kperp_blocked", "K_perp blocker exists", any(r["missing_input"] == "MISSING_KPERP_SOURCE_OR_ZERO" for r in tables["blockers"]), "blockers")
    add("VAL4336_R10_blocked", "R10 fallback remains blocked", any("R10" in r["blocked_route"] and r["status"] == "blocked" for r in tables["blockers"]), "blockers")
    add("VAL4336_symbolic_smoke_pass", "symbolic factorisation smoke passes nonclaim", any(r["result"] == "PASS_NONCLAIM_SYMBOLIC_DERIVATION" for r in tables["smoke"]), "smoke")
    add("VAL4336_numeric_smoke_blocked", "numeric PPN smoke is blocked", any(r["arena"] == "open-tail PPN" and r["result"] == "BLOCKED" for r in tables["smoke"]), "smoke")
    add("VAL4336_bound_envelope", "R_PPN bound envelope exists", any(r["quantity"] == "R_PPN_open" and "||R_PPN_open||" in r["bound_statement"] for r in tables["bounds"]), "bounds")
    add("VAL4336_gamma_beta_envelope", "gamma/beta envelope exists", any(r["quantity"] == "delta_gamma and delta_beta" for r in tables["bounds"]), "bounds")
    add("VAL4336_coupling_firewall", "coupling guess firewall exists", any("C_gK=1" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4336_all_claim_flags_false", "all rows with valid_for_claim keep false", all(r.get("valid_for_claim", "False") == "False" for table in tables.values() for r in table if "valid_for_claim" in r), "all_tables")
    add("VAL4336_next_names_Sq_and_coupling", "next target names S_q and metric coupling", any("S_q" in r["target_question"] and "C_gK" in r["target_question"] for r in tables["next"]), "next")
    add("VAL4336_docs_exist", "formal and post docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4336_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4336_post_formula", "post doc contains combined formula", "Pi_PPN=P_PPN G_metric" in read_text(DOC_PATH), "post")
    add("VAL4336_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4336_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4336_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4336_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4336_SOURCE_REGISTER.csv",
        "operators": SOURCE_DIR / "P8_Y5_R2FR_4336_PIPPN_OPERATOR_FACTORISATION.csv",
        "bounds": SOURCE_DIR / "P8_Y5_R2FR_4336_TRANSFER_BOUNDS.csv",
        "smoke": SOURCE_DIR / "P8_Y5_R2FR_4336_NONCLAIM_SMOKE_ROWS.csv",
        "blockers": SOURCE_DIR / "P8_Y5_R2FR_4336_NUMERIC_MATRIX_BLOCKERS.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4336_FORMULA_ROWS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4336_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4336_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4336_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4336_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4336_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "operators": operator_rows(),
        "bounds": bound_rows(),
        "smoke": smoke_rows(),
        "blockers": blocker_rows(),
        "formulas": formula_rows(),
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
## PPC4161 4336 open-tail PiPPN operator factorisation

Marker: `{MARKER}`

4336 derives the open-tail PPN transfer as a symbolic weak-field operator envelope:

```text
Pi_PPN=P_PPN G_metric^bc C_gK P_E[(K_L G_Box^bc S_q)+S_perp].
```

This is a real narrowing: the missing object is no longer a vague `Pi_PPN`; it is the q-profile kernel `S_q`, the metric Green/coupling normalization `G_metric C_gK`, boundary constants, `K_perp` control and PPN normalization. Numeric scoring remains blocked and `valid_for_claim=false`.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4336 packet open-tail PiPPN factorisation

Marker: `{PACKET_MARKER}`

Packet update: the open-tail PPN matrix has been factorised into source-kernel, longitudinal-owner, metric-response and PPN-projection operators. The coupling slot `C_gK` is now explicitly exposed as a critical local-GR bottleneck rather than hidden in a placeholder projection matrix.
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
