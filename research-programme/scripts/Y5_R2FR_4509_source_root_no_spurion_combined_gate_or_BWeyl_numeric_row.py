from __future__ import annotations

import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deltaktf_shell_profile_gate import read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4509"
CLAIM_ID = "L-351"
MARKER = "PPC4161_SOURCE_ROOT_NO_SPURION_COMBINED_GATE_OR_BWEYL_NUMERIC_ROW_4509"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_ROOT_NO_SPURION_COMBINED_GATE_OR_BWEYL_NUMERIC_ROW_4509"
DECISION = "COMBINED_SOURCE_ROOT_NO_SPURION_KHAT_GATE_EXACT_BWEYL_ZERO_UNSIGNED_NUMERIC_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4510-Y5-R2FR-parent-source-root-lock-or-first-BWeyl-input-fill.md"

FORMAL_PATH = FORMAL / "525-PPC4161-source-root-no-spurion-combined-gate-or-BWeyl-numeric-row.md"
DOC_PATH = POST / "4509-Y5-R2FR-source-root-no-spurion-combined-gate-or-BWeyl-numeric-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4509_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4509_SOURCE_REGISTER.csv"
COMBINED_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4509_COMBINED_ZERO_THEOREM.csv"
SOURCE_ROOT = SOURCE_DIR / "P8_Y5_R2FR_4509_SOURCE_ROOT_GATE.csv"
NO_SPURION = SOURCE_DIR / "P8_Y5_R2FR_4509_NO_SPURION_GATE.csv"
KHAT_TRACE = SOURCE_DIR / "P8_Y5_R2FR_4509_KHAT_TRACE_GATE.csv"
BOUNDARY_GATE = SOURCE_DIR / "P8_Y5_R2FR_4509_BOUNDARY_DOMAIN_READOUT_GATE.csv"
BWEYL_NUMERIC = SOURCE_DIR / "P8_Y5_R2FR_4509_BWEYL_NUMERIC_ACQUISITION_ROW.csv"
PARENT_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4509_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4509_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4509_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4509_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4509_DECISION.csv"

FORMAL_524 = FORMAL / "524-PPC4161-memory-Weyl-response-tail-or-Bmem-finite-bound-row.md"
POST_4508 = POST / "4508-Y5-R2FR-memory-Weyl-response-tail-or-Bmem-finite-bound-row.md"
STATUS_4508 = SOURCE_DIR / "P8_Y5_R2FR_4508_STATUS.csv"
ZERO_4508 = SOURCE_DIR / "P8_Y5_R2FR_4508_THETAWM_ZERO_GATE.csv"
FINITE_4508 = SOURCE_DIR / "P8_Y5_R2FR_4508_BWEYL_FINITE_BOUND_ROW.csv"

POST_4300 = POST / "4300-Y5-R2FR-DvGamma-m-Lcg-zero-or-first-coefficient-source-row.md"
VDZ_4300 = SOURCE_DIR / "P8_Y5_R2FR_4300_VERTICAL_DOUBLE_ZERO_THEOREM.csv"
POST_4301 = POST / "4301-Y5-R2FR-parent-double-zero-lock-or-second-order-DvGamma-bound-row.md"
PLC_4301 = SOURCE_DIR / "P8_Y5_R2FR_4301_PARENT_LOCK_CONTRACT.csv"
ELD_4301 = SOURCE_DIR / "P8_Y5_R2FR_4301_EULER_LOCK_DERIVATION.csv"
BOUNDS_4301 = SOURCE_DIR / "P8_Y5_R2FR_4301_SECOND_ORDER_DVGAMMA_BOUND_ROWS.csv"

LCG_1369 = SOURCE_DIR / "P8_Y5_R10_1369_LCG_METRIC_RESPONSE_DERIVATION_LEDGER.csv"
LCG_2734 = SOURCE_DIR / "P8_Y5_R2FR_2734_LCG_METRIC_SILENCE_AUDIT.csv"
MRD_3627 = SOURCE_DIR / "P8_Y5_R2FR_3627_GAMMA_KHAT_METRIC_RESPONSE_DERIVATION.csv"
KMC_3628 = SOURCE_DIR / "P8_Y5_R2FR_3628_KMETRIC_KHAT_COMPARISON.csv"
KMC_4115 = SOURCE_DIR / "P8_Y5_R2FR_4115_KMETRIC_KHAT_COMPARISON.csv"
WEYL_3606 = SOURCE_DIR / "P8_Y5_R2FR_3606_BQWEYL_NO_SPURION_THEOREM.csv"
WEYL_BOUND_3606 = SOURCE_DIR / "P8_Y5_R2FR_3606_BQWEYL_BOUND_ROWS.csv"
WEYL_ACQ_3607 = SOURCE_DIR / "P8_Y5_R2FR_3607_BQWEYL_FINITE_ACQUISITION_ROWS.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def md(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def table(rows: Sequence[Mapping[str, object]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        output.append("| " + " | ".join(md(row.get(header, "")) for header in headers) + " |")
    return "\n".join(output)


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4509_00_formal524", "4508 formal handoff", FORMAL_524, "Theta_W,m", "Weyl trace tail formula"),
        ("SRC4509_01_post4508", "4508 post mirror", POST_4508, "B_Weyl", "finite B_Weyl bound row"),
        ("SRC4509_02_status4508", "4508 status", STATUS_4508, "PRIVATE_NONCLAIM", "predecessor status"),
        ("SRC4509_03_zero4508", "4508 zero gate", ZERO_4508, "ZG4508_3_combined", "combined zero target"),
        ("SRC4509_04_finite4508", "4508 finite bound", FINITE_4508, "BW4508_0_total", "B_Weyl total bound"),
        ("SRC4509_05_post4300", "4300 double-zero theorem", POST_4300, "D_v Gamma_eff", "vertical double-zero identity"),
        ("SRC4509_06_vdz4300", "4300 theorem csv", VDZ_4300, "DZT4300_1_double_zero_insert", "source-root double zero"),
        ("SRC4509_07_post4301", "4301 parent-lock gate", POST_4301, "L_m delta m", "positive operator route"),
        ("SRC4509_08_plc4301", "4301 parent-lock contract", PLC_4301, "PLC4301_3_local_lock_operator", "operator clause"),
        ("SRC4509_09_eld4301", "4301 Euler derivation", ELD_4301, "EL4301_3_exact_nohair", "no-hair branch"),
        ("SRC4509_10_bounds4301", "4301 second-order bounds", BOUNDS_4301, "BQ4301_3_DvGamma_quad", "finite fallback"),
        ("SRC4509_11_lcg1369", "1369 Lcg chain zero", LCG_1369, "ML1369_3_chain_zero_gate_update", "chain response gate"),
        ("SRC4509_12_lcg2734", "2734 source-root audit", LCG_2734, "LCGMS2734_3_source_root_coefficient_kill", "coefficient kill route"),
        ("SRC4509_13_weyl3606_index", "3606 one-Weyl index lemma", WEYL_3606, "BQW3606_1_metric_trace_index_lemma", "metric-only Weyl zero"),
        ("SRC4509_14_weyl3606_spurion", "3606 spurion necessity", WEYL_3606, "BQW3606_3_spurion_necessity", "parent grammar gate"),
        ("SRC4509_15_weyl3606_bound", "3606 Weyl finite bound", WEYL_3606, "BQW3606_5_finite_bound_law", "finite Weyl law"),
        ("SRC4509_16_weylbound3606", "3606 Weyl bound rows", WEYL_BOUND_3606, "BQB3606_1_BqWeyl", "first numeric coefficient row"),
        ("SRC4509_17_weylacq3607", "3607 Weyl acquisition gate", WEYL_ACQ_3607, "BACQ3607_11_acceptance_rule", "acceptance rule"),
        ("SRC4509_18_mrd3627", "3627 Gamma/Khat metric response", MRD_3627, "MRD3627_1_metric_response", "Kmetric definition"),
        ("SRC4509_19_kmc3628", "3628 Kmetric/Khat comparison", KMC_3628, "KMC3628_5_verdict", "Khat match missing"),
        ("SRC4509_20_kmc4115", "4115 latest Kmetric comparison", KMC_4115, "KMC4115_5_verdict", "current Khat residual"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, role, path, needle, note in specs:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text(path),
                "line": line_of(path, needle),
                "note": note,
                "valid_for_claim": False,
            }
        )
    return rows


def combined_zero_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "CZT4509_0_start",
            "object": "memory Weyl trace tail",
            "formula": "Theta_W,m = -2 L_cg^-3(F_m W_L + F W_L,m) + L_cg^-2 W_F,m + W_boundary,m + W_domain,m + R_K_trace,m",
            "derivation": "4508 product rule plus explicit Khat trace-assignment residual",
            "status": "DERIVED_INPUT_FROM_4508",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CZT4509_1_source_root_clause",
            "object": "Lcg chain response",
            "formula": "F(m_*)=0 and F_m(m_*)=0 imply -2 L_cg^-3(F_m W_L + F W_L,m)=0",
            "derivation": "coefficient kill; no need to assume W_L=0 or W_L,m=0",
            "status": "EXACT_IF_PARENT_SOURCE_ROOT_LOCK_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CZT4509_2_no_spurion_clause",
            "object": "linear Weyl metric response",
            "formula": "W_F,m=0 if the parent object language has only metric/epsilon contractions and no P^{abcd}C_abcd spurion/readout kernel",
            "derivation": "metric-only one-Weyl scalar traces vanish; nonzero linear Weyl requires a Weyl-type spurion",
            "status": "EXACT_IF_PARENT_GRAMMAR_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CZT4509_3_khat_clause",
            "object": "trace-assignment residual",
            "formula": "R_K_trace,m=0 if K_hat=K_metric[Gamma_eff]+K_TF with partial_m Tr(K_TF)=0 under one sign/volume convention",
            "derivation": "metric-response ownership converts Khat trace into the same variational stress channel",
            "status": "EXACT_IF_KHAT_MATCH_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CZT4509_4_boundary_clause",
            "object": "boundary/domain/readout tail",
            "formula": "W_boundary,m=W_domain,m=W_readout,m=0 under fixed boundary class, variation-before-readout, and no source-reference flux",
            "derivation": "prevents a hidden surface/readout Weyl coefficient from replacing the bulk spurion",
            "status": "EXACT_IF_BOUNDARY_DOMAIN_READOUT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "CZT4509_5_combined",
            "object": "B_Weyl",
            "formula": "CZT4509_1 + CZT4509_2 + CZT4509_3 + CZT4509_4 in the same parent branch imply Theta_W,m=0 and B_Weyl=-Theta_W,m/4=0",
            "derivation": "this is a real theorem shape, not a cancellation: each term is individually killed by an owned clause",
            "status": "CONDITIONAL_THEOREM_EXACT_BUT_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def source_root_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "SRG4509_0_Fm_WL",
            "term": "-2 L^-3 F_m W_L",
            "zero_condition": "F_m(m_*)=0",
            "owner_route": "4300 vertical double-zero theorem plus 4301 parent-lock contract",
            "current_status": "ALGEBRAIC_ZERO_ROUTE_EXISTS_PARENT_LOCK_UNSIGNED",
            "needed_next": "derive or source V'(m_*)=0 and the physical identification F_m=V'_m in the active memory branch",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "SRG4509_1_F_WLm",
            "term": "-2 L^-3 F W_L,m",
            "zero_condition": "F(m_*)=0",
            "owner_route": "source-root coefficient kill from 2734 and 4300",
            "current_status": "BEST_ROUTE_BECAUSE_IT_KILLS_COEFFICIENT_NOT_KERNEL",
            "needed_next": "prove F is vacuum-subtracted in the same branch rather than fitted per system",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "SRG4509_2_branch_lock",
            "term": "m_L-m_*",
            "zero_condition": "delta m=0 or bounded by positive local operator",
            "owner_route": "L_m delta m=(-Z_m box+mu_m^2)delta m=J_m+B_m+N(delta m)",
            "current_status": "PROOF_OBJECT_WRITTEN_NUMERIC_PARENT_INPUTS_MISSING",
            "needed_next": "lambda_m, J_m, B_m, boundary class, zero-mode exclusion",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "SRG4509_3_fallback",
            "term": "quadratic source-root leakage",
            "zero_condition": "not zero; bound instead",
            "owner_route": "C_quad <= N_P/a_ref Lmin^-2 |F_2|(Delta_m Delta_Dv_m + Delta_m^2 Delta_Dv_ln_Lcg) plus derivative/projector terms",
            "current_status": "BOUND_TEMPLATE_EXISTS_BUT_SOURCE_ROWS_MISSING",
            "needed_next": "F_2, Lmin, projector norm, Delta_m, Delta_Dv_m, Delta_Dv_ln_Lcg",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def no_spurion_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "NSG4509_0_metric_only_index",
            "target": "linear Weyl scalar from metric alone",
            "result": "zero",
            "argument": "C_abcd is trace-free, so metric contractions reduce to traces such as g^{ac}g^{bd}C_abcd=0",
            "current_status": "EXACT_INDEX_LEMMA_AVAILABLE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "NSG4509_1_spurion_exclusion",
            "target": "parent-owned no-spurion grammar",
            "result": "not yet signed",
            "argument": "a nonzero term q P^{abcd}C_abcd is possible if the parent/readout owns a Weyl-type projector P^{abcd}",
            "current_status": "GRAMMAR_SIGNATURE_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "NSG4509_2_readout_kernel",
            "target": "readout/projector cannot reintroduce a Weyl spurion",
            "result": "not yet signed",
            "argument": "even if the bulk parent grammar is clean, detector/source/readout kernels can act as P^{abcd}",
            "current_status": "READOUT_SILENCE_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "NSG4509_3_finite_fallback",
            "target": "W_F,m if no-spurion remains unsigned",
            "result": "bound required",
            "argument": "E_BqWeyl[arena] <= tau_BqWeyl_arena ||G_q|| |B_qWeyl| ||C_Weyl|| plus boundary/source tails",
            "current_status": "FINITE_ROW_EXISTS_SYMBOLIC_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def khat_trace_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "KTG4509_0_response_definition",
            "target": "K_metric[Gamma_eff]",
            "formula": "K_metric^{mn}:= -2 delta Gamma_eff/delta g_mn - convention_terms; equivalently T_GK^{mn}=Gamma_eff g^{mn}-K_metric^{mn}",
            "current_status": "DEFINITION_AVAILABLE_FROM_3627",
            "needed_next": "declare one sign/volume/derivative convention and map current K_hat to it",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "KTG4509_1_current_match",
            "target": "K_hat=K_metric",
            "formula": "K_hat^{mn}=K_metric^{mn}+R_K^{mn}",
            "current_status": "R_K_RETAINED_BY_3628_AND_4115",
            "needed_next": "explicit tensor equality or sourced residual norm R_K_trace,m",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "KTG4509_2_trace_zero",
            "target": "R_K_trace,m",
            "formula": "partial_m Tr(R_K)=0 if R_K is tracefree or absent in the active branch",
            "current_status": "ZERO_ROUTE_UNSIGNED",
            "needed_next": "parent tensor decomposition K_hat=K_metric+K_TF with Tr(K_TF)=0 before readout",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "KTG4509_3_finite_fallback",
            "target": "R_K_trace,m bound",
            "formula": "|B_Weyl| receives 1/4 |R_K_trace,m|",
            "current_status": "NUMERIC_ROW_MISSING",
            "needed_next": "R_K trace derivative coefficient, units, local arena projection, source path",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def boundary_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "BDR4509_0_boundary",
            "target": "W_boundary,m",
            "zero_condition": "fixed boundary class and no memory-dependent boundary flux",
            "current_status": "UNSIGNED",
            "fallback_input": "B_boundary_m coefficient and source path",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "BDR4509_1_domain",
            "target": "W_domain,m",
            "zero_condition": "variation domain fixed before source/readout projection",
            "current_status": "UNSIGNED",
            "fallback_input": "B_domain_m coefficient and source path",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "BDR4509_2_readout",
            "target": "W_readout,m",
            "zero_condition": "readout does not contain a Weyl-type projector or source-reference flux",
            "current_status": "UNSIGNED",
            "fallback_input": "B_readout_m coefficient and readout kernel source",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def bweyl_numeric_rows() -> List[Dict[str, object]]:
    specs = [
        ("BWN4509_00_F_root", "F(m_*)", "dimensionless_or_parent_units", "source-root value", "MISSING_PARENT_SOURCE_ROOT", "4300/4301 parent V/F source"),
        ("BWN4509_01_Fm_root", "F_m(m_*)", "per_m", "source-root derivative", "MISSING_PARENT_SOURCE_ROOT", "4300/4301 parent V/F source"),
        ("BWN4509_02_Lcg", "L_cg", "length", "coarse-graining length", "MISSING_NUMERIC_LOCAL_SCALE", "local branch scale source"),
        ("BWN4509_03_WL", "W_L", "length_per_Weyl_generator", "unit Weyl response of L_cg", "MISSING_METRIC_RESPONSE", "Lcg metric response source"),
        ("BWN4509_04_WLm", "W_L,m", "length_per_m_per_Weyl_generator", "memory derivative of Lcg Weyl response", "MISSING_METRIC_RESPONSE", "Lcg metric response source"),
        ("BWN4509_05_WFm", "W_F,m", "parent_units_per_m", "memory derivative of F Weyl response", "MISSING_NO_SPURION_OR_COEFFICIENT", "no-spurion theorem or B_qWeyl finite row"),
        ("BWN4509_06_BqWeyl", "B_qWeyl", "parent_normalized", "linear q-Weyl/tidal coefficient fallback", "MISSING_PARENT_COEFFICIENT", "3606/3607 coefficient source"),
        ("BWN4509_07_Gq", "G_q", "operator_norm", "q source operator norm", "MISSING_OPERATOR_NORM", "3606/3607 finite row pack"),
        ("BWN4509_08_CWeyl", "C_Weyl", "curvature", "local Weyl profile/norm", "MISSING_ARENA_PROFILE", "R10/PPN/clock/orbital source profile"),
        ("BWN4509_09_RKtrace", "R_K_trace,m", "same_as_ThetaWm", "Khat trace residual derivative", "MISSING_KHAT_MATCH_OR_BOUND", "3627/3628/4115 residual source"),
        ("BWN4509_10_Bboundary", "B_boundary,m", "same_as_ThetaWm", "boundary memory-response tail", "MISSING_BOUNDARY_CERTIFICATE", "boundary/source path"),
        ("BWN4509_11_Bdomain", "B_domain,m", "same_as_ThetaWm", "domain motion memory-response tail", "MISSING_DOMAIN_CERTIFICATE", "domain/source path"),
        ("BWN4509_12_Breadout", "B_readout,m", "same_as_ThetaWm", "readout/projector memory-response tail", "MISSING_READOUT_CERTIFICATE", "readout kernel source"),
        ("BWN4509_13_tau_R10", "tau_R10", "arena_projection", "R10 transfer from B_Weyl to observable", "MISSING_ARENA_PROJECTION", "R10 projection source"),
        ("BWN4509_14_tau_PPN", "tau_PPN", "arena_projection", "PPN transfer from B_Weyl to observable", "MISSING_ARENA_PROJECTION", "PPN projection source"),
        ("BWN4509_15_tau_clock", "tau_clock", "arena_projection", "clock transfer from B_Weyl to observable", "MISSING_ARENA_PROJECTION", "clock projection source"),
        ("BWN4509_16_tau_orbital", "tau_orbital", "arena_projection", "orbital transfer from B_Weyl to observable", "MISSING_ARENA_PROJECTION", "orbital projection source"),
    ]
    rows: List[Dict[str, object]] = []
    for row_id, symbol, units, role, status, source_hint in specs:
        rows.append(
            {
                "row_id": row_id,
                "symbol": symbol,
                "units": units,
                "role": role,
                "current_value": "MISSING_NUMERIC_SOURCE_ROW",
                "status": status,
                "source_hint": source_hint,
                "source_path": "MISSING_PARENT_OR_ARENA_SOURCE",
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PA4509_0_actual_progress",
            "claim": "B_Weyl zero route is now a four-clause theorem, not a vibes ledger",
            "status": "DERIVED_CONDITIONAL_THEOREM",
            "effect": "source-root, no-spurion, Khat trace, and boundary/readout are separated into exact term-killers",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4509_1_source_root",
            "claim": "source-root/double-zero kills both Lcg chain terms",
            "status": "EXACT_IF_PARENT_LOCK_SIGNED",
            "effect": "best next route because it does not require proving W_L or W_L,m individually zero",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4509_2_no_spurion",
            "claim": "linear Weyl response is absent",
            "status": "INDEX_LEMMA_EXACT_GRAMMAR_UNSIGNED",
            "effect": "bulk metric-only scalar is safe, but readout/projector spurions are not yet excluded",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4509_3_khat",
            "claim": "Khat trace tail is absent",
            "status": "MATCH_MISSING",
            "effect": "R_K_trace,m remains a live finite bound component",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4509_4_numeric",
            "claim": "B_Weyl finite bound is score-ready",
            "status": "NOT_SCORE_READY",
            "effect": "source/root, response, Khat, and arena projection rows are staged but numeric values are missing",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {"gate_id": "CG4509_0_combined_zero", "gate": "B_Weyl=0 by combined theorem", "derived_now": False, "blocked_by": "parent source-root lock, no-spurion grammar, Khat trace match, and boundary/readout silence are not all signed", "claim_allowed": False},
        {"gate_id": "CG4509_1_numeric_bound", "gate": "B_Weyl finite bound score-ready", "derived_now": False, "blocked_by": "numeric/source-backed rows and arena projections are missing", "claim_allowed": False},
        {"gate_id": "CG4509_2_Bmem", "gate": "B_mem_eff cleared for body-charge row", "derived_now": False, "blocked_by": "B_Weyl plus Y5/Y6/source/readout tails remain live", "claim_allowed": False},
        {"gate_id": "CG4509_3_local_GR", "gate": "local GR/PPN/R10 promotion", "derived_now": False, "blocked_by": "local source couplings and Khat metric-response ownership remain unsigned", "claim_allowed": False},
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "conditional combined B_Weyl zero theorem and concrete numeric acquisition row",
            "not_derived": "parent-signed source-root lock, no-spurion/readout grammar, Khat trace match, boundary/domain silence, numeric arena projections",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated": STAMP,
        }
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4509_0",
            "decision": DECISION,
            "because": "B_Weyl can be killed without tuning if four independent parent clauses hold; currently those clauses are exact theorem targets but unsigned",
            "effect": "next work should attack the source-root parent lock first, because it kills two Lcg-chain terms at coefficient level and is less scrutinizable than assuming Lcg silence",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4509_0",
            "target_file": NEXT_TARGET,
            "task": "try to close the parent source-root lock F(m_*)=F_m(m_*)=0 in the active memory branch; if it fails, fill the first numeric B_Weyl input row",
            "success_condition": "either F and F_m are parent-signed zero in the same branch, or the fallback B_Weyl row has sourced values for the first live component",
            "do_not": "treat the combined theorem as a local-GR pass until all four clauses are signed in the same parent branch",
            "valid_for_claim": False,
        }
    ]


def validate(all_rows: Mapping[str, Sequence[Mapping[str, object]]]) -> List[Dict[str, object]]:
    csv_files = [
        SOURCE_REGISTER,
        COMBINED_ZERO,
        SOURCE_ROOT,
        NO_SPURION,
        KHAT_TRACE,
        BOUNDARY_GATE,
        BWEYL_NUMERIC,
        PARENT_AUDIT,
        CLAIM_GATES,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]
    parsed = True
    details: List[str] = []
    for path in csv_files:
        try:
            rows = read_csv(path)
            parsed = parsed and bool(rows)
            details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:
            parsed = False
            details.append(f"{path.name}:ERROR:{exc}")

    source_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in all_rows["sources"])
    theorem_ok = any(row.get("theorem_id") == "CZT4509_5_combined" for row in all_rows["combined"])
    source_root_ok = any("F(m_*)=0" in str(row.get("zero_condition", "")) for row in all_rows["source_root"])
    no_spurion_ok = any(row.get("gate_id") == "NSG4509_1_spurion_exclusion" for row in all_rows["no_spurion"])
    khat_ok = any(row.get("gate_id") == "KTG4509_1_current_match" for row in all_rows["khat"])
    numeric_blocked = all(row.get("valid_for_claim") is False and str(row.get("current_value", "")).startswith("MISSING") for row in all_rows["numeric"])
    claim_gates_blocked = all(row.get("derived_now") is False and row.get("claim_allowed") is False for row in all_rows["gates"])
    nonclaim_ok = all(
        str(value).lower() != "true"
        for rows in all_rows.values()
        for row in rows
        for key, value in row.items()
        if key in {"valid_for_claim", "claim_allowed"}
    )
    next_ok = all_rows["next"][0]["target_file"] == NEXT_TARGET
    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()

    checks = [
        ("VAL4509_00_sources", source_ok, "all source paths exist and source needles are found"),
        ("VAL4509_01_combined_theorem", theorem_ok, "combined B_Weyl zero theorem row exists"),
        ("VAL4509_02_source_root_gate", source_root_ok, "source-root coefficient kill is recorded"),
        ("VAL4509_03_no_spurion_gate", no_spurion_ok, "no-spurion grammar gate is recorded"),
        ("VAL4509_04_khat_gate", khat_ok, "Khat trace residual gate is recorded"),
        ("VAL4509_05_numeric_blocked", numeric_blocked, "all B_Weyl numeric acquisition rows remain missing/nonclaim"),
        ("VAL4509_06_claims_blocked", claim_gates_blocked, "all claim gates remain blocked"),
        ("VAL4509_07_nonclaim_flags", nonclaim_ok, "all generated valid_for_claim/claim_allowed flags remain false"),
        ("VAL4509_08_csv_parse", parsed, ";".join(details)),
        ("VAL4509_09_next_target", next_ok, NEXT_TARGET),
        ("VAL4509_10_pycache_absent", pycache_absent, "scripts __pycache__ absent after cleanup"),
    ]
    rows = [
        {
            "validation_id": check_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL4509_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "4509 source-root/no-spurion combined gate or B_Weyl numeric row",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def append_claim_once() -> None:
    existing = text(CLAIMS_PATH)
    if CLAIM_ID in existing or MARKER in existing:
        return
    row = ",".join(
        [
            CLAIM_ID,
            "local_gr_newton_r2fr_memory_weyl_combined_gate",
            '"4509 derives the conditional combined zero theorem for B_Weyl: source-root/double-zero kills the Lcg-chain terms, no-spurion grammar kills linear Weyl response, Khat trace match kills the trace-assignment tail, and boundary/domain/readout silence kills surface/readout tails. The theorem is exact but unsigned, so a B_Weyl numeric acquisition row is staged as nonclaim."',
            '"4509 source register, combined zero theorem, source-root gate, no-spurion gate, Khat trace gate, boundary/domain/readout gate, B_Weyl numeric acquisition rows, parent audit, claim gates, status and validation."',
            "private_combined_BWeyl_zero_gate_or_numeric_row_nonclaim",
            NEXT_TARGET,
            "treating a conditional four-clause theorem as a local-GR/PPN/R10 pass, or using no-spurion without readout/Khat/source-root signatures.",
            "local_gr_newton_r2fr_memory_weyl_combined_gate",
            str(FORMAL_PATH),
            NEXT_TARGET,
            '"attack the parent source-root lock first; otherwise fill the first sourced B_Weyl finite component row."',
        ]
    )
    CLAIMS_PATH.write_text(existing.rstrip() + "\n" + row + "\n", encoding="utf-8")


def build_doc(
    sources: Sequence[Mapping[str, object]],
    combined: Sequence[Mapping[str, object]],
    source_root: Sequence[Mapping[str, object]],
    no_spurion: Sequence[Mapping[str, object]],
    khat: Sequence[Mapping[str, object]],
    boundary: Sequence[Mapping[str, object]],
    numeric: Sequence[Mapping[str, object]],
    parent: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    validation: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4509 - Source-Root No-Spurion Combined Gate Or B_Weyl Numeric Row

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Verdict

4509 takes a leap forward on the Weyl tail rather than just circling it. Starting from

`Theta_W,m = -2 L_cg^-3(F_m W_L + F W_L,m) + L_cg^-2 W_F,m + W_boundary,m + W_domain,m + R_K_trace,m`,

the exact non-cancellation route is now:

1. `F(m_*)=0` and `F_m(m_*)=0` kill both Lcg-chain terms.
2. no parent/readout Weyl spurion kills the linear Weyl piece `W_F,m`.
3. `K_hat=K_metric[Gamma_eff]+K_TF` with tracefree residual kills `R_K_trace,m`.
4. fixed boundary/domain/readout class kills the surface/readout tails.

If those four clauses are parent-signed in one branch, then `Theta_W,m=0` and `B_Weyl=-Theta_W,m/4=0`. That is a genuine theorem shape. It is not claimed yet because the parent signatures are not all present, so the same checkpoint stages the concrete numeric/source rows needed if the theorem route fails.

## Source Register

{table(sources)}

## Combined Zero Theorem

{table(combined)}

## Source-Root Gate

{table(source_root)}

## No-Spurion Gate

{table(no_spurion)}

## Khat Trace Gate

{table(khat)}

## Boundary Domain Readout Gate

{table(boundary)}

## B_Weyl Numeric Acquisition Row

{table(numeric)}

## Parent Signature Audit

{table(parent)}

## Claim Gates

{table(gates)}

## Status

{table(status)}

## Decision

{table(decisions)}

## Next Target

{table(next_target)}

## Validation

{table(validation)}
"""


def main() -> None:
    sources = source_rows()
    combined = combined_zero_rows()
    source_root = source_root_gate_rows()
    no_spurion = no_spurion_rows()
    khat = khat_trace_rows()
    boundary = boundary_gate_rows()
    numeric = bweyl_numeric_rows()
    parent = parent_audit_rows()
    gates = claim_gate_rows()
    status = status_rows()
    decisions = decision_rows()
    next_target = next_rows()

    all_rows = {
        "sources": sources,
        "combined": combined,
        "source_root": source_root,
        "no_spurion": no_spurion,
        "khat": khat,
        "boundary": boundary,
        "numeric": numeric,
        "parent": parent,
        "gates": gates,
        "status": status,
        "decisions": decisions,
        "next": next_target,
    }

    write_csv(SOURCE_REGISTER, sources)
    write_csv(COMBINED_ZERO, combined)
    write_csv(SOURCE_ROOT, source_root)
    write_csv(NO_SPURION, no_spurion)
    write_csv(KHAT_TRACE, khat)
    write_csv(BOUNDARY_GATE, boundary)
    write_csv(BWEYL_NUMERIC, numeric)
    write_csv(PARENT_AUDIT, parent)
    write_csv(CLAIM_GATES, gates)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_CSV, next_target)
    write_csv(DECISION_CSV, decisions)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(all_rows)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(
        sources,
        combined,
        source_root,
        no_spurion,
        khat,
        boundary,
        numeric,
        parent,
        gates,
        status,
        decisions,
        next_target,
        validation,
    )
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4509 Source-Root No-Spurion Combined Gate Or B_Weyl Numeric Row

Marker: `{MARKER}`  
4509 turns the Weyl tail into a four-clause theorem gate. `F=F_m=0` kills the Lcg-chain terms, no-spurion grammar kills `W_F,m`, Khat metric-response ownership kills `R_K_trace,m`, and boundary/domain/readout silence kills the remaining tails. The combined theorem is exact but unsigned; if it does not close, the staged `B_Weyl` numeric acquisition row gives the finite-bound route.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4509 Packet Integration

Marker: `{PACKET_MARKER}`  
The packet now has a real `B_Weyl` fork: prove the parent source-root/no-spurion/Khat/boundary clauses in one branch, or fill the first numeric/source-backed `B_Weyl` component row before any local-GR/PPN/R10 scoring.
""",
    )
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
