from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4337"
CLAIM_ID = "L-178"
BRANCH = "MTS_R2FR_Y5_SOURCE_SQ_QPROFILE_KERNEL_AND_METRIC_GREEN_COUPLING_OR_R10_ALPHA_PARENT_PIVOT_4337"
DECISION = "ORDINARY_COUPLING_IMPORTED_AS_CALIBRATED_KAPPA_EFF_OPEN_TAIL_COUPLING_REDUCED_TO_CGAMMA_PROFILE_COEFFICIENT_NONCLAIM"
MARKER = "PPC4161_SOURCE_SQ_QPROFILE_KERNEL_AND_METRIC_GREEN_COUPLING_OR_R10_ALPHA_PARENT_PIVOT_4337"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_SQ_QPROFILE_KERNEL_AND_METRIC_GREEN_COUPLING_OR_R10_ALPHA_PARENT_PIVOT_4337"
NEXT_TARGET = "4338-Y5-R2FR-cGamma-transition-source-kernel-coefficient-fill-or-metric-null-proof.md"

FORMAL_PATH = FORMAL / "353-PPC4161-source-Sq-qprofile-kernel-and-metric-green-coupling-or-R10-alpha-parent-pivot.md"
DOC_PATH = POST / "4337-Y5-R2FR-source-Sq-qprofile-kernel-and-metric-green-coupling-or-R10-alpha-parent-pivot.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4337_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")

AU_M = 1.495978707e11
SUN_GM_OVER_C2_M = 1.47662504e3
U_SHELL = SUN_GM_OVER_C2_M / AU_M
S_GATE = 1.0e-5
LINEAR_M_TR = 1.0e-9
LINEAR_S_UNIT = LINEAR_M_TR / U_SHELL
LINEAR_CGAMMA_MAX = S_GATE / LINEAR_S_UNIT
QUADRATIC_S_UNIT = 1.4327492214684143e-6
QUADRATIC_CGAMMA_MAX = S_GATE / QUADRATIC_S_UNIT


SOURCES = [
    (
        "SRC4337_00_4336_next",
        SOURCE_DIR / "P8_Y5_R2FR_4336_NEXT_TARGET.csv",
        "S_q and C_gK/G_metric",
        "4336 handoff asking whether S_q and metric coupling can be filled.",
    ),
    (
        "SRC4337_01_4336_coupling",
        FORMAL / "352-PPC4161-open-tail-PiPPN-metric-transfer-derivation-or-R10-parent-alpha-fill.md",
        "C_gK = local metric-response normalization",
        "4336 exposed the C_gK coupling slot.",
    ),
    (
        "SRC4337_02_kappa_factor",
        FORMAL / "181-PPC4161-kappa-G-normalization-gate.md",
        "kappa_eff = kappa_* Z_H",
        "Existing calibrated source-coupling factorization.",
    ),
    (
        "SRC4337_03_newton_readout",
        FORMAL / "187-PPC4161-Poisson-Gauss-Newton-readout-from-Hamiltonian-source-charge.md",
        "G_munu = kappa_eff T_H_munu",
        "Weak-field EH/Newton source equation in the private packet.",
    ),
    (
        "SRC4337_04_calibrated_G",
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "G_cal := c^4 kappa_eff/(8*pi).",
        "Calibrated G bridge; numeric G is not predicted.",
    ),
    (
        "SRC4337_05_G_not_prediction",
        FORMAL / "222-PPC4161-calibrated-GN-bridge-and-source-charge-caveat.md",
        "MTS does not need to numerically predict G_N",
        "Clarifies that structural GR reduction may use calibrated universal G.",
    ),
    (
        "SRC4337_06_residual_cGamma",
        FORMAL / "294-PPC4161-left-hand-EH-Newton-limit-or-residual-EFT-bound-gate.md",
        "c_Gamma         memory/Gamma/Khat local coupling",
        "Residual EFT map identifying c_Gamma as the memory/Gamma/Khat local coupling.",
    ),
    (
        "SRC4337_07_private_zero_subset",
        FORMAL / "295-PPC4161-residual-EFT-coefficient-zero-or-local-test-bound-pack.md",
        "private-zero / routed subset:",
        "Residual split showing cGamma remains outside the private-zero subset.",
    ),
    (
        "SRC4337_08_cGamma_gate",
        FORMAL / "296-PPC4161-cGamma-parent-memory-equation-AJ-source-coefficient-or-profile-fill.md",
        "live cGamma local-memory amplitude gate is",
        "cGamma amplitude gate and remaining live pressure.",
    ),
    (
        "SRC4337_09_cGamma_profile",
        FORMAL / "303-PPC4161-cGamma-AJ-real-profile-or-parent-coefficient-derivation.md",
        "A_J,eff_private <=",
        "Later cGamma/AJ pressure law.",
    ),
    (
        "SRC4337_10_q_profile",
        FORMAL / "63-local-q-profile-bound.md",
        "q_loc^nu =",
        "q_profile kernel definition from Gamma_eff and K_hat.",
    ),
    (
        "SRC4337_11_q_first_results",
        FORMAL / "64-local-q-profile-bound-first-results.md",
        "M_tr <= 2.565e-7",
        "Quadratic-only local q-profile benchmark.",
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
                "4337 resolves part of the 4336 coupling bottleneck by splitting the metric response into an ordinary Hilbert-source coupling and an open-tail transition residual. The ordinary local matter branch already has a calibrated universal coupling kappa_eff=kappa_* Z_H=8*pi*G_cal/c^4, with G_cal empirical in the same honest sense as GR. The open-tail transition branch is not allowed to reuse this as a free pass; it reduces to a dimensionless residual coefficient c_Gamma multiplying the Gamma/Khat/q_profile metric-source lift. Thus C_gK for open tails becomes kappa_eff*c_Gamma, and the symbolic 4336 operator becomes Pi_PPN^Gamma=P_PPN G_EH kappa_eff c_Gamma P_E[(K_L G_Box S_q^Gamma)+S_perp]. Benchmarks show a generic AU linear memory profile with M_tr=1e-9 would need |c_Gamma|<=9.8706e-5, while the quadratic fixed-point benchmark with S_PPN=1.4327e-6 allows |c_Gamma| up to about 6.98 at the source-amplitude level. No local-GR/PPN claim is made because c_Gamma, S_q profile rows, and the metric-null theorem remain unsigned.",
                "4337 source register, coupling split rows, S_q reduction rows, cGamma benchmark rows, metric-null and direct-projection branch rows, blocker rows, runner, firewall, decision, status, next-target and validation CSV.",
                "private_coupling_split_kappa_eff_imported_open_tail_cGamma_reduction_nonclaim",
                "Attack cGamma directly: prove a metric-null/source-kernel zero theorem or fill cGamma, A_src/A_lap/A_drift, T_res/tau_L and arena profile coefficients.",
                "Treating calibrated ordinary G as a prediction of G_N; applying ordinary Hilbert coupling to open transition tails without cGamma; claiming the quadratic benchmark is a local-GR pass; or setting cGamma small by fit instead of parent theorem/source-backed profile.",
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


def coupling_rows() -> List[Dict[str, str]]:
    return [
        {
            "coupling_id": "CG4337_0_ordinary_Hilbert_source",
            "channel": "ordinary matter/source",
            "coupling_law": "C_matter=kappa_eff=kappa_* Z_H=8*pi*G_cal/c^4",
            "status": "STRUCTURAL_COUPLING_IMPORTED_CALIBRATED_NUMERIC_G_NOT_PREDICTED",
            "source_basis": "181;187;194;222",
            "remaining_gap": "source-charge caveat for public promotion; not an open-tail metric-source pass",
            "valid_for_claim": "False",
        },
        {
            "coupling_id": "CG4337_1_transition_open_tail",
            "channel": "Gamma/Khat/q_loc transition residual",
            "coupling_law": "C_gK^Gamma=kappa_eff*c_Gamma",
            "status": "DERIVED_NORMALIZED_RESIDUAL_SPLIT",
            "source_basis": "294 residual EFT map plus 4336 coupling slot",
            "remaining_gap": "c_Gamma parent-zero theorem or finite source-backed value/profile",
            "valid_for_claim": "False",
        },
        {
            "coupling_id": "CG4337_2_metric_null_branch",
            "channel": "metric-null transition theorem",
            "coupling_law": "c_Gamma=0 or Sigma_metric[q_tr]=0 => Pi_PPN^Gamma=0",
            "status": "LEGAL_ESCAPE_ROUTE_NOT_PARENT_SIGNED",
            "source_basis": "136-144 metric-null/source-lift contract imported through residual channel",
            "remaining_gap": "parent action/source-lift theorem",
            "valid_for_claim": "False",
        },
        {
            "coupling_id": "CG4337_3_direct_projection_branch",
            "channel": "direct visible transition source",
            "coupling_law": "c_Gamma=1 gives direct metric projection of the q_profile source",
            "status": "BENCHMARK_ONLY",
            "source_basis": "63/64 q_profile gate",
            "remaining_gap": "generic linear source fails; quadratic branch remains conditional on fixed-point/no-hair profile",
            "valid_for_claim": "False",
        },
    ]


def sq_rows() -> List[Dict[str, str]]:
    return [
        {
            "sq_id": "SQ4337_0_profile_kernel_definition",
            "source_kernel": "S_q^Gamma[T_open]",
            "formula": "q_loc^nu=P_loc[nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu}]",
            "reduction": "kernel acts only on the Gamma/Khat/local-memory open-tail channel after the coupling split",
            "status": "FORMULA_SOURCE_BACKED_PROFILE_INPUTS_OPEN",
            "valid_for_claim": "False",
        },
        {
            "sq_id": "SQ4337_1_trace_memory_part",
            "source_kernel": "S_Gamma",
            "formula": "Gamma_eff=L_cg^-2 F(m); abs(nabla Gamma_eff)<=L_cg^-2[abs(F1)M_tr/ell_tr+0.5abs(F2)M_tr^2/ell_tr]",
            "reduction": "linear term is fatal unless F1=0 or |c_Gamma| is very small",
            "status": "BOUND_SOURCE_BACKED_PARENT_DOUBLE_ZERO_OPEN",
            "valid_for_claim": "False",
        },
        {
            "sq_id": "SQ4337_2_Khat_part",
            "source_kernel": "S_Khat",
            "formula": "abs(nabla_mu K_hat^{mu nu})<=C_K abs(b_mem)M_tr^2/ell_tr^3",
            "reduction": "survives as quadratic gradient-stress source unless fixed-point/profile bounds suppress it",
            "status": "BOUND_SOURCE_BACKED_PROFILE_INPUTS_OPEN",
            "valid_for_claim": "False",
        },
        {
            "sq_id": "SQ4337_3_PiPPN_cGamma_reduction",
            "source_kernel": "Pi_PPN^Gamma",
            "formula": "Pi_PPN^Gamma=P_PPN G_EH^bc kappa_eff c_Gamma P_E[(K_L G_Box^bc S_q^Gamma)+S_perp]",
            "reduction": "4336 open-tail matrix now depends on c_Gamma times profile coefficients, not an arbitrary C_gK",
            "status": "OPERATOR_REDUCED_NUMERIC_PROFILE_ROWS_OPEN",
            "valid_for_claim": "False",
        },
    ]


def benchmark_rows() -> List[Dict[str, str]]:
    return [
        {
            "benchmark_id": "BM4337_0_AU_linear_generic",
            "branch": "direct linear q_profile",
            "inputs": f"M_tr={LINEAR_M_TR}; F1=1; u_shell={U_SHELL:.16e}; S_gate={S_GATE}",
            "S_PPN_unit_cGamma": f"{LINEAR_S_UNIT:.16e}",
            "cGamma_max_for_gate": f"{LINEAR_CGAMMA_MAX:.16e}",
            "unit_cGamma_status": "FAIL",
            "interpretation": "direct AU linear memory projection survives only if c_Gamma is below about 1e-4 or F1/M_tr is further suppressed",
            "valid_for_claim": "False",
        },
        {
            "benchmark_id": "BM4337_1_AU_quadratic_fixed_point",
            "branch": "quadratic fixed-point q_profile",
            "inputs": f"M_tr=1e-7; F1=0; ell_tr/L_cg~sqrt(2); S_gate={S_GATE}",
            "S_PPN_unit_cGamma": f"{QUADRATIC_S_UNIT:.16e}",
            "cGamma_max_for_gate": f"{QUADRATIC_CGAMMA_MAX:.16e}",
            "unit_cGamma_status": "CONDITIONAL_PASS_SOURCE_AMPLITUDE_ONLY",
            "interpretation": "quadratic branch can tolerate c_Gamma order unity at this source-amplitude proxy, but only if the fixed-point/no-hair profile is parent-owned",
            "valid_for_claim": "False",
        },
    ]


def branch_rows() -> List[Dict[str, str]]:
    return [
        {
            "branch_id": "BR4337_0_closed_Hilbert_GR",
            "branch": "closed ordinary Hilbert local source",
            "condition": "EH selector, Hilbert source descent, kappa_eff locally source-blind",
            "result": "ordinary Newton/PPN coupling structurally calibrated",
            "claim_policy": "private nonclaim; numeric G not predicted",
        },
        {
            "branch_id": "BR4337_1_open_metric_null",
            "branch": "open tail metric-null route",
            "condition": "Sigma_metric[q_tr]=0 or c_Gamma=0 parent-signed before scoring",
            "result": "open-tail Pi_PPN^Gamma vanishes",
            "claim_policy": "not active until parent theorem exists",
        },
        {
            "branch_id": "BR4337_2_open_direct_bound",
            "branch": "open tail direct finite residual",
            "condition": "c_Gamma finite and S_q/profile coefficients source-backed",
            "result": "score |c_Gamma profile_a| <= arena bound",
            "claim_policy": "no claim until all profile rows are numeric and source-backed",
        },
        {
            "branch_id": "BR4337_3_R10_fallback",
            "branch": "R10 alpha(lambda) pivot",
            "condition": "Pi_PPN route stalls and R10 parent coefficients/bound curve are filled",
            "result": "run nonclaim alpha smoke comparator",
            "claim_policy": "still blocked by parent alpha and claim-valid curve rows",
        },
    ]


def blocker_rows() -> List[Dict[str, str]]:
    return [
        {
            "blocker_id": "BLK4337_0_cGamma",
            "blocked_route": "numeric open-tail PPN matrix",
            "missing_input": "MISSING_CGAMMA_PARENT_ZERO_OR_FINITE_SOURCE_VALUE",
            "needed_for_release": "parent metric-null/source-kernel theorem or finite c_Gamma normalization fixed before local tests",
            "status": "blocked",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK4337_1_profile_coefficients",
            "blocked_route": "S_q profile scoring",
            "missing_input": "MISSING_A_SRC_A_LAP_A_DRIFT_TRES_TAUL_PROFILE_ROWS",
            "needed_for_release": "A_src, A_lap, A_drift, T_res/tau_L and arena projection coefficients from parent/profile source rows",
            "status": "blocked",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK4337_2_double_zero",
            "blocked_route": "quadratic fixed-point source-amplitude pass",
            "missing_input": "MISSING_PARENT_DOUBLE_ZERO_NOHAIR_PROFILE",
            "needed_for_release": "F1=0, bounded M_tr, ell_tr/L_cg and no unsuppressed boundary/source injection from parent law",
            "status": "blocked",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLK4337_3_R10",
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
            "formula_id": "F4337_0_kappa_eff",
            "name": "ordinary calibrated source coupling",
            "formula": "kappa_eff=kappa_* Z_H=8*pi*G_cal/c^4",
            "status": "IMPORTED_STRUCTURAL_COUPLING",
        },
        {
            "formula_id": "F4337_1_transition_coupling",
            "name": "open-tail residual coupling",
            "formula": "C_gK^Gamma=kappa_eff*c_Gamma",
            "status": "DERIVED_RESIDUAL_SPLIT",
        },
        {
            "formula_id": "F4337_2_open_tail_PPN",
            "name": "cGamma-reduced PPN transfer",
            "formula": "R_PPN^Gamma=c_Gamma P_PPN G_EH^bc kappa_eff P_E[(K_L G_Box^bc S_q^Gamma)+S_perp]T_open",
            "status": "OPERATOR_REDUCED_NUMERIC_SOURCE_ROWS_OPEN",
        },
        {
            "formula_id": "F4337_3_cGamma_bound",
            "name": "source-amplitude cGamma ceiling",
            "formula": "abs(c_Gamma)<=S_gate/S_PPN_unit",
            "status": "BENCHMARK_BOUND_TEMPLATE",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4337_0_coupling_split",
            "branch_input": "4336 C_gK slot plus 181/187/194/222 coupling bridge",
            "action": "IMPORT_ORDINARY_COUPLING_AND_SPLIT_OPEN_TAIL",
            "output": "ordinary C=kappa_eff; open-tail C=kappa_eff*c_Gamma",
            "claim_policy": "nonclaim structural reduction",
        },
        {
            "runner_id": "RUN4337_1_benchmark_linear",
            "branch_input": "AU linear q_profile with unit cGamma",
            "action": "COMPUTE_CGAMMA_CEILING",
            "output": f"unit fails; cGamma_max={LINEAR_CGAMMA_MAX:.6e}",
            "claim_policy": "benchmark only",
        },
        {
            "runner_id": "RUN4337_2_benchmark_quadratic",
            "branch_input": "quadratic fixed-point q_profile benchmark",
            "action": "COMPUTE_CGAMMA_CEILING",
            "output": f"unit source-amplitude passes conditionally; cGamma_max={QUADRATIC_CGAMMA_MAX:.6e}",
            "claim_policy": "conditional only; profile theorem still missing",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4337_0_G_prediction",
            "forbidden_shortcut": "claim numeric G_N is predicted from kappa_eff",
            "reason": "the imported coupling is calibrated, exactly like GR unless a parent scale law fixes kappa_*",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4337_1_transition_reuse",
            "forbidden_shortcut": "apply ordinary Hilbert coupling directly to open transition tails",
            "reason": "open transition tails require c_Gamma/source-lift ownership",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4337_2_fit_cGamma",
            "forbidden_shortcut": "choose c_Gamma after seeing PPN or R10 residuals",
            "reason": "c_Gamma must be parent-zero or source-backed before scoring",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4337_3_quadratic_overclaim",
            "forbidden_shortcut": "treat the quadratic benchmark as a local-GR pass",
            "reason": "F1=0, M_tr, ell_tr/L_cg and no-hair/profile inputs remain parent-unsigned",
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
            "summary": "4337 imports the already-existing calibrated ordinary coupling and reduces the open-tail metric coupling to kappa_eff*c_Gamma. The next real problem is no longer an undefined C_gK; it is c_Gamma plus S_q/profile rows.",
            "next_action": NEXT_TARGET,
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4337_0_ordinary_coupling",
            "item": "ordinary Hilbert coupling",
            "status": "STRUCTURALLY_FILLED",
            "notes": "kappa_eff=8*pi*G_cal/c^4; numeric G remains calibrated not predicted",
        },
        {
            "status_id": "STAT4337_1_open_tail_coupling",
            "item": "open-tail metric coupling",
            "status": "REDUCED_TO_CGAMMA",
            "notes": "C_gK^Gamma=kappa_eff*c_Gamma",
        },
        {
            "status_id": "STAT4337_2_linear_benchmark",
            "item": "AU linear q_profile",
            "status": "FAILS_FOR_UNIT_CGAMMA",
            "notes": f"requires |c_Gamma|<={LINEAR_CGAMMA_MAX:.3e} unless F1/M_tr is suppressed",
        },
        {
            "status_id": "STAT4337_3_quadratic_benchmark",
            "item": "quadratic fixed-point q_profile",
            "status": "CONDITIONAL_SOURCE_AMPLITUDE_SURVIVES",
            "notes": f"allows |c_Gamma|<={QUADRATIC_CGAMMA_MAX:.3e} at proxy level if parent profile clauses hold",
        },
        {
            "status_id": "STAT4337_4_next",
            "item": "next target",
            "status": "NEXT_TARGET",
            "notes": "prove metric-null/cGamma zero or fill cGamma/AJ/profile coefficients",
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4337_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can c_Gamma be parent-zero/metric-null, or can finite c_Gamma and S_q profile coefficients be source-filled enough to score PPN?",
            "preferred_route": "derive metric-null source-kernel theorem: Sigma_metric[q_tr]=0 or c_Gamma=0 in compact local collars",
            "fallback_route": "fill finite c_Gamma, A_src, A_lap, A_drift, T_res/tau_L and arena profile coefficients for PPN/R10/clock/orbital nonclaim scoring",
        }
    ]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 353 - PPC4161 source S_q q-profile kernel and metric Green coupling or R10 alpha parent pivot

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4337 does **not** prove public local GR, PPN, R10, WEP, clock safety, orbital safety, Newtonian recovery, Maxwell/QED, charge normalization, or a numerical prediction of `G_N`.

It does remove one foggy bottleneck from 4336. The metric coupling is not one undifferentiated mystery:

```text
ordinary Hilbert matter:
  C_matter = kappa_eff = kappa_* Z_H = 8*pi*G_cal/c^4

open transition/Gamma/Khat tail:
  C_gK^Gamma = kappa_eff c_Gamma.
```

So the live open-tail PPN transfer is:

```text
R_PPN^Gamma =
  c_Gamma P_PPN G_EH^bc kappa_eff P_E[
    (K_L G_Box^bc S_q^Gamma) + S_perp
  ] T_open.
```

The “coupling problem” is now the `c_Gamma`/profile problem. That is progress: a finite target coefficient is better than a vague missing map.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role"])}

## Coupling Split

{md_table(tables["coupling"], ["coupling_id", "channel", "coupling_law", "status", "source_basis", "remaining_gap", "valid_for_claim"])}

## S_q Reduction

{md_table(tables["sq"], ["sq_id", "source_kernel", "formula", "reduction", "status", "valid_for_claim"])}

## Benchmarks

{md_table(tables["benchmarks"], ["benchmark_id", "branch", "inputs", "S_PPN_unit_cGamma", "cGamma_max_for_gate", "unit_cGamma_status", "interpretation", "valid_for_claim"])}

## Branch Routes

{md_table(tables["branches"], ["branch_id", "branch", "condition", "result", "claim_policy"])}

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
    post = f"""# 4337 Y5-R2FR source S_q q-profile kernel and metric Green coupling or R10 alpha parent pivot

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

The 4336 coupling bottleneck has been split:

```text
C_matter = kappa_eff = 8*pi*G_cal/c^4
C_gK^Gamma = kappa_eff c_Gamma
```

Ordinary matter coupling is structurally imported as calibrated GR-like coupling. Open transition tails reduce to `c_Gamma` times the q-profile/source-kernel rows. So the next target is no longer “find the coupling”; it is “prove `c_Gamma=0`/metric-null, or source finite `c_Gamma` and profile coefficients.”

## Benchmarks

{md_table(tables["benchmarks"], ["branch", "S_PPN_unit_cGamma", "cGamma_max_for_gate", "unit_cGamma_status", "interpretation"])}

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

    formula_text = " ".join(row["formula"] for row in tables["formulas"])
    benchmark_map = {row["benchmark_id"]: row for row in tables["benchmarks"]}

    add("VAL4337_sources_exist", "all source paths exist", all(r["path_exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4337_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4337_kappa_imported", "ordinary coupling imports kappa_eff", any("kappa_eff" in r["coupling_law"] and r["channel"] == "ordinary matter/source" for r in tables["coupling"]), "coupling")
    add("VAL4337_cGamma_split", "open-tail coupling reduced to kappa_eff*c_Gamma", any("kappa_eff*c_Gamma" in r["coupling_law"] for r in tables["coupling"]), "coupling")
    add("VAL4337_Sq_defined", "S_q profile definition present", any("q_loc^nu=P_loc" in r["formula"] for r in tables["sq"]), "sq")
    add("VAL4337_PiPPN_reduced", "Pi_PPN/R_PPN formula contains c_Gamma and S_q", "c_Gamma" in formula_text and "S_q" in formula_text and "R_PPN" in formula_text, "formulas")
    add("VAL4337_linear_fails_unit", "linear benchmark fails for unit cGamma", benchmark_map["BM4337_0_AU_linear_generic"]["unit_cGamma_status"] == "FAIL" and float(benchmark_map["BM4337_0_AU_linear_generic"]["cGamma_max_for_gate"]) < 1.0, "benchmarks")
    add("VAL4337_quadratic_conditional", "quadratic benchmark allows unit cGamma only conditionally", benchmark_map["BM4337_1_AU_quadratic_fixed_point"]["unit_cGamma_status"] == "CONDITIONAL_PASS_SOURCE_AMPLITUDE_ONLY" and float(benchmark_map["BM4337_1_AU_quadratic_fixed_point"]["cGamma_max_for_gate"]) > 1.0, "benchmarks")
    add("VAL4337_cGamma_blocker", "cGamma blocker exists", any(r["missing_input"] == "MISSING_CGAMMA_PARENT_ZERO_OR_FINITE_SOURCE_VALUE" for r in tables["blockers"]), "blockers")
    add("VAL4337_profile_blocker", "profile coefficient blocker exists", any("A_SRC" in r["missing_input"] or "A_src" in r["needed_for_release"] for r in tables["blockers"]), "blockers")
    add("VAL4337_firewall_G", "G prediction firewall exists", any("G_N" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4337_all_claim_flags_false", "all rows with valid_for_claim keep false", all(r.get("valid_for_claim", "False") == "False" for table in tables.values() for r in table if "valid_for_claim" in r), "all_tables")
    add("VAL4337_next_cGamma", "next target attacks cGamma", any("c_Gamma" in r["target_question"] and ("source" in r["target_question"] or "source" in r["fallback_route"]) for r in tables["next"]), "next")
    add("VAL4337_docs_exist", "formal and post docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4337_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4337_post_split", "post doc contains coupling split", "C_gK^Gamma = kappa_eff c_Gamma" in read_text(DOC_PATH), "post")
    add("VAL4337_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4337_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4337_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4337_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4337_SOURCE_REGISTER.csv",
        "coupling": SOURCE_DIR / "P8_Y5_R2FR_4337_COUPLING_SPLIT.csv",
        "sq": SOURCE_DIR / "P8_Y5_R2FR_4337_SQ_QPROFILE_REDUCTION.csv",
        "benchmarks": SOURCE_DIR / "P8_Y5_R2FR_4337_CGAMMA_BENCHMARKS.csv",
        "branches": SOURCE_DIR / "P8_Y5_R2FR_4337_BRANCH_ROUTES.csv",
        "blockers": SOURCE_DIR / "P8_Y5_R2FR_4337_BLOCKERS.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4337_FORMULA_ROWS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4337_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4337_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4337_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4337_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4337_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "coupling": coupling_rows(),
        "sq": sq_rows(),
        "benchmarks": benchmark_rows(),
        "branches": branch_rows(),
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
## PPC4161 4337 coupling split into kappa_eff and cGamma

Marker: `{MARKER}`

4337 resolves part of the open-tail coupling bottleneck. The ordinary Hilbert source channel imports the calibrated structural coupling:

```text
kappa_eff = kappa_* Z_H = 8*pi*G_cal/c^4.
```

The transition/Gamma/Khat channel is not granted that as a pass. It reduces to:

```text
C_gK^Gamma = kappa_eff c_Gamma.
```

So the live local problem is now finite and attackable: prove `c_Gamma=0`/metric-null, or source finite `c_Gamma` plus `S_q` profile coefficients before any PPN/R10/clock/orbital score.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4337 packet coupling split

Marker: `{PACKET_MARKER}`

Packet update: the 4336 metric coupling slot is split into ordinary calibrated `kappa_eff` and open-tail residual `c_Gamma`. This recovers the older cGamma ledger as the live coupling target and prevents the open transition tail from borrowing ordinary Hilbert coupling as a silent local-GR pass.
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
