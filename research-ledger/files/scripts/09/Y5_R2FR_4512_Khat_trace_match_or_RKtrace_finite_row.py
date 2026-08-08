from __future__ import annotations

import csv
import io
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from deltaktf_shell_profile_gate import read_csv, write_csv  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4512"
CLAIM_ID = "L-354"
MARKER = "PPC4161_KHAT_TRACE_MATCH_OR_RKTRACE_FINITE_ROW_4512"
PACKET_MARKER = "PPC4161_PACKET_KHAT_TRACE_MATCH_OR_RKTRACE_FINITE_ROW_4512"
DECISION = "KHAT_TRACE_MATCH_THEOREM_DERIVED_CONDITIONALLY_RKTRACE_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4513-Y5-R2FR-boundary-domain-readout-tail-or-final-BWeyl-vector.md"

FORMAL_PATH = FORMAL / "528-PPC4161-Khat-trace-match-or-RKtrace-finite-row.md"
DOC_PATH = POST / "4512-Y5-R2FR-Khat-trace-match-or-RKtrace-finite-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4512_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4512_SOURCE_REGISTER.csv"
TRACE_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4512_KHAT_TRACE_MATCH_THEOREM.csv"
DECOMP_CLASSIFIER = SOURCE_DIR / "P8_Y5_R2FR_4512_KHAT_DECOMPOSITION_CLASSIFIER.csv"
RKTRACE_FILL = SOURCE_DIR / "P8_Y5_R2FR_4512_RKTRACE_INPUT_FILL_ROWS.csv"
RKTRACE_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4512_RKTRACE_FINITE_BOUND_ROWS.csv"
PARENT_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4512_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES = SOURCE_DIR / "P8_Y5_R2FR_4512_CLAIM_GATES.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4512_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4512_NEXT_TARGET.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4512_DECISION.csv"

FORMAL_527 = FORMAL / "527-PPC4161-no-spurion-readout-grammar-or-WFm-finite-row.md"
POST_4511 = POST / "4511-Y5-R2FR-no-spurion-readout-grammar-or-WFm-finite-row.md"
KTG_4509 = SOURCE_DIR / "P8_Y5_R2FR_4509_KHAT_TRACE_GATE.csv"
BWEYL_NUMERIC_4509 = SOURCE_DIR / "P8_Y5_R2FR_4509_BWEYL_NUMERIC_ACQUISITION_ROW.csv"
THETAW_4508 = SOURCE_DIR / "P8_Y5_R2FR_4508_THETAWM_DECOMPOSITION.csv"
MRD_3627 = SOURCE_DIR / "P8_Y5_R2FR_3627_GAMMA_KHAT_METRIC_RESPONSE_DERIVATION.csv"
KMC_3628 = SOURCE_DIR / "P8_Y5_R2FR_3628_KMETRIC_KHAT_COMPARISON.csv"
KMC_4115 = SOURCE_DIR / "P8_Y5_R2FR_4115_KMETRIC_KHAT_COMPARISON.csv"
QBR_4115 = SOURCE_DIR / "P8_Y5_R2FR_4115_BOUND_RUNNER_ROWS.csv"
CAN_3689 = SOURCE_DIR / "P8_Y5_R2FR_3689_CANONICAL_GAMMA_KHAT_BRANCH_ROWS.csv"
LEGACY_3689 = SOURCE_DIR / "P8_Y5_R2FR_3689_LEGACY_SYMBOL_QUARANTINE.csv"
RES_3689 = SOURCE_DIR / "P8_Y5_R2FR_3689_RESIDUAL_ROWS.csv"
TF_4138 = SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_SIGNING_AUDIT.csv"
TB_4138 = SOURCE_DIR / "P8_Y5_R2FR_4138_TRACEFREE_ZERO_THEOREM_OR_BOUND.csv"
KTS_793 = SOURCE_DIR / "P8_Y5_R10_793_KHAT_TRACE_STATUS_GATE.csv"
KMTS_1349 = SOURCE_DIR / "P8_Y5_R10_1349_KMTS_TRACE_PROJECTION_OWNER_ATTEMPT.csv"

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


def csv_line(values: Sequence[object]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer)
    writer.writerow(values)
    return buffer.getvalue().strip("\r\n")


def falseish(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "none", ""}


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4512_00_formal527", "4511 formal handoff", FORMAL_527, "No-Spurion Readout Grammar", "previous B_Weyl leg"),
        ("SRC4512_01_post4511", "4511 post handoff", POST_4511, "NT4511_0", "declares Khat trace next target"),
        ("SRC4512_02_ktg4509", "4509 Khat trace gate", KTG_4509, "KTG4509_2_trace_zero", "trace-zero target"),
        ("SRC4512_03_numeric4509", "4509 B_Weyl numeric row", BWEYL_NUMERIC_4509, "BWN4509_09_RKtrace", "R_K trace missing row"),
        ("SRC4512_04_theta4508", "4508 Theta_W,m split", THETAW_4508, "TW4508_4_Khat_match", "Khat trace-assignment mismatch"),
        ("SRC4512_05_mrd3627", "3627 metric-response derivation", MRD_3627, "MRD3627_1_metric_response", "K_metric definition"),
        ("SRC4512_06_kmc3628", "3628 Kmetric/Khat comparison", KMC_3628, "KMC3628_5_verdict", "Khat match not claimed"),
        ("SRC4512_07_kmc4115", "4115 active Kmetric comparison", KMC_4115, "KMC4115_5_verdict", "active residual retained"),
        ("SRC4512_08_qbr4115", "4115 residual runner", QBR_4115, "QBR4115_0_RK", "R_K finite row route"),
        ("SRC4512_09_can3689_khat", "3689 canonical Khat", CAN_3689, "CAN3689_3_Khat", "canonical metric response"),
        ("SRC4512_10_can3689_deltak", "3689 canonical DeltaK", CAN_3689, "CAN3689_5_DeltaK", "canonical zero / legacy residual"),
        ("SRC4512_11_legacy3689", "3689 legacy Khat quarantine", LEGACY_3689, "LQ3689_1_Khat_legacy", "legacy Khat residual"),
        ("SRC4512_12_res3689", "3689 residual envelope", RES_3689, "RES3689_1_legacy_DeltaK", "legacy DeltaK bound row"),
        ("SRC4512_13_tf4138", "4138 tracefree signing audit", TF_4138, "TF4138_0_tensor_shape", "tracefree projector identity"),
        ("SRC4512_14_tb4138", "4138 tracefree zero theorem", TB_4138, "TB4138_0_zero_theorem", "conditional TF zero theorem"),
        ("SRC4512_15_kts793", "793 Khat trace status", KTS_793, "KTS793_1_tracefree_status", "trace shortcut blocked"),
        ("SRC4512_16_kmts1349", "1349 trace projection owner attempt", KMTS_1349, "KMTS1349_2_Khat_metric_response", "older owner gap"),
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


def trace_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "KTM4512_0_define_residual",
            "object": "R_K^{mu nu}",
            "statement": "With one sign/volume convention, define R_K^{mu nu}:=K_hat^{mu nu}-K_metric^{mu nu}[Gamma_eff]. The B_Weyl trace-assignment tail only needs D_m Tr(R_K), not full tensor equality.",
            "formula": "R_K_trace,m := D_m(g_mu_nu R_K^{mu nu})",
            "result": "full Khat match is stronger than necessary for this gate",
            "status": "DERIVED_TRACE_REDUCTION",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "KTM4512_1_trace_only_zero",
            "object": "R_K_trace,m",
            "statement": "If K_hat=K_metric+K_TF+K_bdry+K_readout with Tr(K_TF)=0 for all m and D_m Tr(K_bdry+K_readout)=0, then D_m Tr(R_K)=0.",
            "formula": "D_m Tr(K_hat-K_metric)=D_m Tr(K_TF)+D_m Tr(K_bdry+K_readout)=0",
            "result": "the Khat trace obstruction is killed without requiring every tracefree component to vanish",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "KTM4512_2_canonical_branch",
            "object": "K_can",
            "statement": "Inside the canonical 3689 branch, K_can is K_metric[Gamma_can] by definition, hence Delta_K^can=0 and the trace residual derivative vanishes in the canonical variables.",
            "formula": "K_can^{mu nu}=K_metric^{mu nu}[Gamma_can] => D_m Tr(K_can-K_metric[Gamma_can])=0",
            "result": "canonical branch closes this trace leg internally",
            "status": "CANONICAL_ZERO_BRANCH_DERIVED_PRIVATE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "KTM4512_3_tracefree_projector",
            "object": "K_TF",
            "statement": "A projector-defined tracefree improvement has identically zero trace before and after m-variation, provided the projector identity is parent-owned and not applied after readout.",
            "formula": "g_mu_nu Pi_TF[X]^{mu nu}=0 => D_m Tr(Pi_TF[X])=0",
            "result": "4138 tracefree shape is enough for the trace channel if it is genuinely the only leftover Khat piece",
            "status": "PROJECTOR_TRACE_IDENTITY_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "KTM4512_4_failure_identity",
            "object": "finite R_K trace",
            "statement": "If any convention, scalar trace, boundary/improvement, or readout tail survives, it must be carried as an absolute no-cancellation trace derivative.",
            "formula": "|R_K_trace,m| <= |D_m Tr(Delta_K_legacy)| + |C_conv,m| + |C_scalar_trace,m| + |C_boundary_trace,m| + |C_improvement_trace,m| + |C_readout_trace,m|",
            "result": "fallback is a finite B_Weyl_RK row, not a closure axiom",
            "status": "FINITE_BOUND_LAW_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "KTM4512_5_BWeyl_insertion",
            "object": "B_Weyl_RK",
            "statement": "The 4509 Khat term enters the memory-Weyl body-charge channel with the inherited quarter factor.",
            "formula": "|B_Weyl_RK| <= 1/4 |R_K_trace,m|",
            "result": "R_K trace is now wired to a concrete finite component if the theorem-zero branch is not parent-signed",
            "status": "BWeyl_COMPONENT_BOUND_INSERTED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decomposition_classifier_rows() -> List[Dict[str, object]]:
    return [
        {
            "class_id": "KDC4512_0_canonical_metric_response",
            "branch": "K_hat=K_metric[Gamma_eff]",
            "trace_result": "ZERO_IF_LIVE_MAP_SIGNED",
            "why": "no residual tensor exists in the canonical branch",
            "live_status": "PRIVATE_CANONICAL_BRANCH_NOT_PUBLIC_MAP",
            "finite_fallback": "legacy DeltaK trace row",
            "valid_for_claim": False,
        },
        {
            "class_id": "KDC4512_1_tracefree_residual",
            "branch": "K_hat=K_metric+Pi_TF[U]",
            "trace_result": "ZERO_IF_PROJECTOR_PARENT_OWNED",
            "why": "tracefree identity holds pointwise for all m",
            "live_status": "FORMAL_SHAPE_EXISTS_LIVE_ADOPTION_UNSIGNED",
            "finite_fallback": "A_TF/L_TF bound from 4138 does not affect trace but adoption tails do",
            "valid_for_claim": False,
        },
        {
            "class_id": "KDC4512_2_scalar_trace_reentry",
            "branch": "K_hat=K_metric+S_trace g",
            "trace_result": "LIVE_TRACE_RESIDUAL",
            "why": "any independent scalar trace creates D_m Tr(R_K)=4 D_m S_trace in four dimensions",
            "live_status": "FORBIDDEN_UNLESS_PARENT_ZERO_OR_BOUND",
            "finite_fallback": "C_scalar_trace,m",
            "valid_for_claim": False,
        },
        {
            "class_id": "KDC4512_3_boundary_improvement",
            "branch": "K_hat=K_metric+div B_imp",
            "trace_result": "ZERO_ONLY_WITH_FIXED_BOUNDARY_OR_TOTAL-DERIVATIVE_HANDOFF",
            "why": "bulk trace can be an exact divergence but local collars/readouts can still see a boundary trace",
            "live_status": "UNSIGNED",
            "finite_fallback": "C_boundary_trace,m + C_improvement_trace,m",
            "valid_for_claim": False,
        },
        {
            "class_id": "KDC4512_4_flux_or_Poynting",
            "branch": "physical wave/EM flux stress",
            "trace_result": "NOT_A_FREE_LOCAL_GR_ZERO",
            "why": "Maxwell-like stress is a valid action branch but must be counted as physical stress/current exchange, not hidden in Khat closure",
            "live_status": "ROUTE_RETAINED_FOR_EM_BRANCH",
            "finite_fallback": "R_flux/current/source-normalization row",
            "valid_for_claim": False,
        },
        {
            "class_id": "KDC4512_5_legacy_Khat",
            "branch": "old K_hat symbol without canonical equality",
            "trace_result": "RESIDUAL_RETAINED",
            "why": "3689 quarantines legacy Khat until mapped into K_can",
            "live_status": "CURRENT_PUBLIC_SAFE_STATUS",
            "finite_fallback": "D_m Tr(Delta_K_legacy)",
            "valid_for_claim": False,
        },
    ]


def rktrace_fill_rows() -> List[Dict[str, object]]:
    return [
        {
            "input_id": "RKF4512_00_RKtrace",
            "source_4509_row": "BWN4509_09_RKtrace",
            "symbol": "R_K_trace,m",
            "filled_value": "0",
            "fill_type": "CONDITIONAL_THEOREM_ZERO",
            "condition": "one metric-response convention; K_hat=K_metric+tracefree parent-owned residual; no scalar trace, boundary/improvement trace, or readout trace tail",
            "source_path": str(DOC_PATH),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "RKF4512_01_trace_only_switch",
            "source_4509_row": "KTG4509_2_trace_zero",
            "symbol": "Z_RK_trace",
            "filled_value": "TRUE_CONDITIONAL",
            "fill_type": "ZERO_SWITCH_IF_PARENT_SIGNATURES_PASS",
            "condition": "D_m Tr(K_hat-K_metric)=0 in the active branch",
            "source_path": str(DOC_PATH),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "RKF4512_02_DeltaKlegacy",
            "source_4509_row": "",
            "symbol": "Delta_K_legacy_trace,m",
            "filled_value": "RETAINED_IF_LEGACY_MAP_UNSIGNED",
            "fill_type": "FINITE_RESIDUAL_SLOT",
            "condition": "legacy Khat not mapped to K_can",
            "source_path": str(LEGACY_3689),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def rktrace_bound_rows() -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "RKB4512_0_trace_identity",
            "quantity": "R_K_trace,m",
            "formula": "|R_K_trace,m| <= |D_m Tr(Delta_K_legacy)| + |C_conv,m| + |C_scalar_trace,m| + |C_boundary_trace,m| + |C_improvement_trace,m| + |C_readout_trace,m|",
            "required_inputs": "Delta_K_legacy trace profile; convention certificate; scalar-trace exclusion/value; boundary/improvement/readout trace tails; units; source paths",
            "current_status": "MISSING_PARENT_SIGNATURE_OR_NUMERIC_TRACE_INPUTS",
            "valid_for_claim": False,
        },
        {
            "bound_id": "RKB4512_1_BWeyl_component",
            "quantity": "B_Weyl_RK",
            "formula": "|B_Weyl_RK| <= 1/4 |R_K_trace,m|",
            "required_inputs": "R_K_trace,m theorem-zero certificate or sourced finite value; common B_Weyl normalization",
            "current_status": "FORMULA_READY_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "RKB4512_2_arena_projection",
            "quantity": "E_RKtrace[arena]",
            "formula": "E_RKtrace[arena] <= tau_RK_arena |B_Weyl_RK| + source/readout tails",
            "required_inputs": "tau_R10; tau_PPN; tau_clock; tau_orbital; no-cancellation envelope; arena profile",
            "current_status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "bound_id": "RKB4512_3_scalar_trace_counterbranch",
            "quantity": "C_scalar_trace,m",
            "formula": "C_scalar_trace,m = D_m Tr(S_trace g) = 4 D_m S_trace in four dimensions",
            "required_inputs": "proof S_trace absent/constant or numeric D_m S_trace profile",
            "current_status": "COUNTERBRANCH_RETAINED",
            "valid_for_claim": False,
        },
        {
            "bound_id": "RKB4512_4_boundary_readout",
            "quantity": "C_boundary_trace,m+C_readout_trace,m",
            "formula": "trace tail is zero only if boundary/domain/readout are fixed before variation and carry no memory/source-reference flux",
            "required_inputs": "fixed boundary certificate; readout order certificate; domain-motion bound",
            "current_status": "HANDOFF_TO_4513",
            "valid_for_claim": False,
        },
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PA4512_0_trace_theorem",
            "claim": "R_K_trace,m has an exact trace-only zero theorem",
            "status": "DERIVED_CONDITIONALLY",
            "effect": "full Khat tensor match is no longer required for this B_Weyl leg; trace equality is enough",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4512_1_canonical",
            "claim": "canonical Gamma/Khat branch closes trace residual internally",
            "status": "DERIVED_PRIVATE_CANONICAL",
            "effect": "K_can=K_metric gives Delta_K^can=0; live legacy/public map remains separate",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4512_2_live_map",
            "claim": "current active K_hat is parent-signed as K_metric plus tracefree residual only",
            "status": "NOT_PROVEN",
            "effect": "4512 cannot claim B_Weyl zero, local GR, PPN, R10, clock, or orbital pass",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4512_3_tracefree_shape",
            "claim": "tracefree improvement shape is a legal zero-trace leftover",
            "status": "HELPFUL_BUT_LIVE_ADOPTION_UNSIGNED",
            "effect": "4138 supports the trace-only route, but does not sign current Khat adoption or boundary silence",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4512_4_next_tail",
            "claim": "boundary/domain/readout trace tails are now the next B_Weyl obstruction",
            "status": "NEXT_TARGET_SELECTED",
            "effect": "move to 4513 final tail vector rather than looping on generic Khat",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4512_0_RKtrace_zero",
            "gate": "R_K_trace,m=0 live in active branch",
            "derived_now": False,
            "blocked_by": "parent signature for Khat=Kmetric+tracefree residual and boundary/readout trace silence is unsigned",
            "claim_allowed": False,
        },
        {
            "gate_id": "CG4512_1_BWeyl_RK_zero",
            "gate": "B_Weyl_RK component zero",
            "derived_now": False,
            "blocked_by": "R_K trace theorem not live-signed or numerically bounded",
            "claim_allowed": False,
        },
        {
            "gate_id": "CG4512_2_full_BWeyl_zero",
            "gate": "full B_Weyl=0",
            "derived_now": False,
            "blocked_by": "boundary/domain/readout tails remain open after source-root, no-spurion and Khat trace conditional rows",
            "claim_allowed": False,
        },
        {
            "gate_id": "CG4512_3_local_GR",
            "gate": "local GR/PPN/R10 promotion",
            "derived_now": False,
            "blocked_by": "source coupling, local projection, arena transfer and final tail vector remain unclosed",
            "claim_allowed": False,
        },
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "trace-only Khat theorem: D_m Tr(K_hat-Kmetric)=0 if the leftover is parent-owned tracefree plus silent boundary/readout tails; canonical branch closes internally",
            "not_derived": "live/public parent map that current Khat is exactly Kmetric plus tracefree residual and no trace tails",
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
            "decision_id": "DEC4512_0",
            "decision": DECISION,
            "because": "the Khat obstruction needed by B_Weyl is a trace derivative, and a tracefree residual theorem can close that narrower channel without solving every Khat component",
            "effect": "R_K_trace,m gets a conditional theorem-zero row and a finite fallback; the next live obstruction is boundary/domain/readout trace tails",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4512_0",
            "target_file": NEXT_TARGET,
            "task": "close or bound B_boundary,m, B_domain,m and B_readout,m so the B_Weyl vector has no hidden tail",
            "success_condition": "final B_Weyl component vector is either theorem-zero under one parent branch or has sourced finite rows for every remaining tail",
            "do_not": "claim full B_Weyl/local-GR from the trace-only Khat theorem before final tails are closed",
            "valid_for_claim": False,
        }
    ]


def all_generated_csvs() -> List[Path]:
    return [
        SOURCE_REGISTER,
        TRACE_THEOREM,
        DECOMP_CLASSIFIER,
        RKTRACE_FILL,
        RKTRACE_BOUND,
        PARENT_AUDIT,
        CLAIM_GATES,
        STATUS_CSV,
        NEXT_CSV,
        DECISION_CSV,
    ]


def validate(all_rows: Mapping[str, Sequence[Mapping[str, object]]]) -> List[Dict[str, object]]:
    parsed = True
    details: List[str] = []
    for path in all_generated_csvs():
        try:
            rows = read_csv(path)
            parsed = parsed and bool(rows)
            details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:
            parsed = False
            details.append(f"{path.name}:ERROR:{exc}")

    source_ok = all(bool(row["exists"]) and bool(row["needle_found"]) for row in all_rows["sources"])
    theorem_ok = any(row.get("theorem_id") == "KTM4512_1_trace_only_zero" for row in all_rows["theorem"])
    canonical_ok = any(row.get("theorem_id") == "KTM4512_2_canonical_branch" for row in all_rows["theorem"])
    fill_ok = any(row.get("input_id") == "RKF4512_00_RKtrace" and row.get("filled_value") == "0" for row in all_rows["fill"])
    bound_ok = any(row.get("bound_id") == "RKB4512_1_BWeyl_component" for row in all_rows["bound"])
    gates_blocked = all(falseish(row.get("claim_allowed")) for row in all_rows["gates"])
    flags_false = True
    for rows in all_rows.values():
        for row in rows:
            if "valid_for_claim" in row and not falseish(row["valid_for_claim"]):
                flags_false = False
            if "claim_allowed" in row and not falseish(row["claim_allowed"]):
                flags_false = False
    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()

    checks = [
        ("VAL4512_00_sources", source_ok, "all source paths exist and source needles are found"),
        ("VAL4512_01_trace_theorem", theorem_ok, "trace-only Khat theorem row exists"),
        ("VAL4512_02_canonical_branch", canonical_ok, "canonical internal zero branch recorded"),
        ("VAL4512_03_RKtrace_fill", fill_ok, "R_K_trace,m conditionally filled as theorem-zero row"),
        ("VAL4512_04_finite_bound", bound_ok, "B_Weyl_RK finite bound row staged"),
        ("VAL4512_05_claims_blocked", gates_blocked, "all claim gates remain blocked"),
        ("VAL4512_06_nonclaim_flags", flags_false, "all generated valid_for_claim/claim_allowed flags remain false"),
        ("VAL4512_07_csv_parse", parsed, ";".join(details)),
        ("VAL4512_08_next_target", all_rows["next"][0]["target_file"] == NEXT_TARGET, NEXT_TARGET),
        ("VAL4512_09_pycache_absent", pycache_absent, "scripts __pycache__ absent after cleanup"),
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
            "validation_id": "VAL4512_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "4512 Khat trace match or R_K trace finite row",
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
    row = csv_line(
        [
            CLAIM_ID,
            "local_gr_newton_r2fr_khat_trace_match",
            "4512 derives the trace-only Khat theorem for the B_Weyl obstruction: the live channel is D_m Tr(K_hat-K_metric), so full Khat tensor equality is stronger than necessary. If current Khat is Kmetric plus a parent-owned tracefree residual and silent boundary/readout tails, R_K_trace,m=0. Canonical Gamma/Khat closes internally, but the public/live map remains unsigned; finite R_K trace rows are staged.",
            "4512 source register, Khat trace theorem, decomposition classifier, R_K trace input fills, finite trace bound rows, parent audit, claim gates, status and validation.",
            "private_Khat_trace_match_conditional_RKtrace_nonclaim",
            NEXT_TARGET,
            "claiming full B_Weyl/local-GR from a trace-only theorem, treating legacy Khat as canonical without a map, or hiding boundary/readout trace tails.",
            "local_gr_newton_r2fr_khat_trace_match",
            str(FORMAL_PATH),
            NEXT_TARGET,
            "close boundary/domain/readout trace tails or stage the final finite B_Weyl vector.",
        ]
    )
    CLAIMS_PATH.write_text(existing.rstrip() + "\n" + row + "\n", encoding="utf-8")


def build_doc(
    sources: Sequence[Mapping[str, object]],
    theorem: Sequence[Mapping[str, object]],
    classifier: Sequence[Mapping[str, object]],
    fill: Sequence[Mapping[str, object]],
    bound: Sequence[Mapping[str, object]],
    parent: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    status: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    next_target: Sequence[Mapping[str, object]],
    validation: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4512 - Khat Trace Match Or R_K Trace Finite Row

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Verdict

4512 narrows the Khat problem instead of trying to win the whole tensor war in one swing.

For the `B_Weyl` obstruction, the needed object is not full `K_hat=K_metric`; it is the trace derivative:

`R_K_trace,m := D_m Tr(K_hat-K_metric[Gamma_eff])`.

Therefore the exact zero route is:

`K_hat = K_metric + K_TF + K_tail`, with `Tr(K_TF)=0` for all `m` and `D_m Tr(K_tail)=0`.

Then `R_K_trace,m=0`, even if the tracefree sector still has nonzero tidal/anisotropic pieces that must be handled elsewhere. The canonical 3689 branch closes this internally because `K_can=K_metric[Gamma_can]`; the live/public legacy map is still unsigned, so this is a private conditional theorem and not a local-GR/PPN/R10 claim.

If the trace theorem is not parent-signed, the honest fallback is:

`|B_Weyl_RK| <= 1/4 |R_K_trace,m|`.

## Source Register

{table(sources)}

## Khat Trace Match Theorem

{table(theorem)}

## Khat Decomposition Classifier

{table(classifier)}

## R_K Trace Input Fill Rows

{table(fill)}

## R_K Trace Finite Bound Rows

{table(bound)}

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
    theorem = trace_theorem_rows()
    classifier = decomposition_classifier_rows()
    fill = rktrace_fill_rows()
    bound = rktrace_bound_rows()
    parent = parent_audit_rows()
    gates = claim_gate_rows()
    status = status_rows()
    decisions = decision_rows()
    next_target = next_rows()

    all_rows = {
        "sources": sources,
        "theorem": theorem,
        "classifier": classifier,
        "fill": fill,
        "bound": bound,
        "parent": parent,
        "gates": gates,
        "status": status,
        "decisions": decisions,
        "next": next_target,
    }

    write_csv(SOURCE_REGISTER, sources)
    write_csv(TRACE_THEOREM, theorem)
    write_csv(DECOMP_CLASSIFIER, classifier)
    write_csv(RKTRACE_FILL, fill)
    write_csv(RKTRACE_BOUND, bound)
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
        theorem,
        classifier,
        fill,
        bound,
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
## 4512 Khat Trace Match Or R_K Trace Finite Row

Marker: `{MARKER}`  
4512 derives the trace-only Khat theorem needed by `B_Weyl`. The obstruction is `D_m Tr(K_hat-K_metric)`, not full tensor equality. If `K_hat=K_metric+K_TF+K_tail`, `Tr(K_TF)=0` identically, and the boundary/readout trace tail is silent, then `R_K_trace,m=0`. The canonical Gamma/Khat branch closes this internally, but the live legacy map is unsigned, so finite `R_K_trace,m` rows remain staged. The next obstruction is the boundary/domain/readout tail vector.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4512 Packet Integration

Marker: `{PACKET_MARKER}`  
The private packet now has conditional theorem-zero rows for source-root, no-spurion `W_F,m`, and the Khat trace derivative. The remaining `B_Weyl` obstruction is concentrated into boundary/domain/readout tails plus any unsigned legacy `Delta_K` trace map.
""",
    )
    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
