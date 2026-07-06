from __future__ import annotations

import csv
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

CHECKPOINT = "4500"
CLAIM_ID = "L-342"
MARKER = "PPC4161_J2_SHELL_SURFACE_AMPLITUDE_SOURCE_ROW_OR_PARENT_KERNEL_ZERO_4500"
PACKET_MARKER = "PPC4161_PACKET_J2_SHELL_SURFACE_AMPLITUDE_SOURCE_ROW_OR_PARENT_KERNEL_ZERO_4500"
DECISION = "A_SHELL_SURFACE_ZERO_CONDITIONAL_AND_FINITE_SOURCE_ROW_EXACT_PRESSURE_BOUND_IMPORTED_NONCLAIM"
NEXT_TARGET = "4501-Y5-R2FR-A-shell-component-source-coefficient-fill-or-kernel-zero.md"

FORMAL_PATH = FORMAL / "516-PPC4161-J2-shell-surface-amplitude-source-row-or-parent-kernel-zero.md"
DOC_PATH = POST / "4500-Y5-R2FR-J2-shell-surface-amplitude-source-row-or-parent-kernel-zero.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4500_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4500_SOURCE_REGISTER.csv"
ZERO_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4500_A_SHELL_ZERO_THEOREM.csv"
SOURCE_COMPONENTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4500_A_SHELL_SOURCE_COMPONENTS.csv"
FINITE_AMPLITUDE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4500_FINITE_A_SHELL_SOURCE_ROW.csv"
PRESSURE_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4500_J2_PRESSURE_BOUND_ROWS.csv"
PARENT_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4500_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4500_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4500_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4500_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4500_NEXT_TARGET.csv"

FORMAL_515 = FORMAL / "515-PPC4161-J2-shell-transfer-operator-first-source-row-or-parent-kernel-signature.md"
POST_4499 = POST / "4499-Y5-R2FR-J2-shell-transfer-operator-first-source-row-or-parent-kernel-signature.md"
SCRIPT_4499 = SCRIPT_DIR / "Y5_R2FR_4499_J2_shell_transfer_operator_first_source_row_or_parent_kernel_signature.py"
J2_OPERATOR_4499 = SOURCE_DIR / "P8_Y5_R2FR_4499_J2_SHELL_TRANSFER_OPERATOR.csv"
PUBLIC_J2_4499 = SOURCE_DIR / "P8_Y5_R2FR_4499_PUBLIC_J2_TRANSFER_DERIVATION.csv"
STATUS_4499 = SOURCE_DIR / "P8_Y5_R2FR_4499_STATUS.csv"
K2_SOURCE_4484 = SOURCE_DIR / "P8_Y5_R2FR_4484_K2_SOURCE_OWNER_ROWS.csv"
K2_ZERO_4485 = SOURCE_DIR / "P8_Y5_R2FR_4485_K2_SOURCE_SILENCE_THEOREM.csv"
K2_FINITE_4485 = SOURCE_DIR / "P8_Y5_R2FR_4485_FINITE_QUADRUPOLE_AMPLITUDE_ROWS.csv"
K2_AUDIT_4485 = SOURCE_DIR / "P8_Y5_R2FR_4485_CURRENT_K2_SOURCE_AUDIT.csv"
PARENT_AUDIT_4498 = SOURCE_DIR / "P8_Y5_R2FR_4498_PARENT_SIGNATURE_AUDIT.csv"
EXTRACTOR_3173 = SOURCE_DIR / "P8_Y5_R2FR_3173_OPERATOR_MATCH_DERIVATION.csv"
J2_BOUNDS_3170 = SOURCE_DIR / "P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv"
RESIDUAL_L2_1955 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1955_RESIDUAL_L2_BOUND_LEDGER.csv"

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


def rows_by(path: Path, key: str) -> Dict[str, Dict[str, str]]:
    if not path.exists():
        return {}
    return {row[key]: row for row in read_csv(path) if key in row}


def semicolon_paths(paths: Iterable[Path]) -> str:
    return "; ".join(str(path) for path in paths)


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4500_00_formal515", "4499 formal handoff", FORMAL_515, "J2OP4499_3_finite_source_functional", "finite source functional row from 4499"),
        ("SRC4500_01_post4499", "4499 post mirror", POST_4499, "A_shell_surface is parent-owned or zero", "4499 says amplitude is the remaining blocker"),
        ("SRC4500_02_j2op4499", "4499 J2 operator rows", J2_OPERATOR_4499, "J2OP4499_4_surface_pressure_bound", "numeric surface pressure bound row"),
        ("SRC4500_03_public4499", "4499 public J2 derivation", PUBLIC_J2_4499, "PJ4499_4_half_range_surface_pressure", "direct A_shell bound"),
        ("SRC4500_04_status4499", "4499 status", STATUS_4499, "source or zero A_shell_surface", "sharpest open clause"),
        ("SRC4500_05_k2owner4484", "4484 K2 source owner rows", K2_SOURCE_4484, "KSO4484_0_Hilbert_source_derivative", "four source derivative slots"),
        ("SRC4500_06_k2zero4485", "4485 source-silence theorem", K2_ZERO_4485, "KZS4485_1_clean_zero_theorem", "conditional zero theorem"),
        ("SRC4500_07_k2finite4485", "4485 finite amplitude rows", K2_FINITE_4485, "FQA4485_0_general_functional", "exact finite amplitude functional"),
        ("SRC4500_08_k2audit4485", "4485 current K2 audit", K2_AUDIT_4485, "CSA4485_1_Hilbert_source", "current owned source derivative audit"),
        ("SRC4500_09_parent4498", "4498 parent shell audit", PARENT_AUDIT_4498, "PS4498_1_shell_verticality", "parent shell kernel still unsigned"),
        ("SRC4500_10_extractor3173", "3173 parent extractor", EXTRACTOR_3173, "OP3173_3_exact_Upsilon_formula", "exact non-fitted Upsilon formula"),
        ("SRC4500_11_bounds3170", "3170 J2 bounds", J2_BOUNDS_3170, "CJ3170_2_Rozelot_half_range_proxy", "surface amplitude pressure bound"),
        ("SRC4500_12_residual1955", "1955 residual l2 fallback", RESIDUAL_L2_1955, "RB1955_0_residual_bound_formula", "finite residual scorer fallback"),
        ("SRC4500_13_script4499", "4499 generator", SCRIPT_4499, 'CHECKPOINT = "4499"', "reproducible predecessor generator"),
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


def constants() -> Dict[str, str]:
    j2_bound = rows_by(J2_BOUNDS_3170, "bound_id").get("CJ3170_2_Rozelot_half_range_proxy", {})
    j2_operator = rows_by(J2_OPERATOR_4499, "operator_id").get("J2OP4499_4_surface_pressure_bound", {})
    return {
        "a_shell_bound": j2_bound.get("A_metric_bound_surface", "1.400851696295935e-13"),
        "j2_half_bound": j2_bound.get("J2_eff_bound", "3.300000000000000e-08"),
        "k2_product_bound": j2_bound.get("K2_corrected_surface_bound", "3.898004369090586e+10"),
        "operator_bound": j2_operator.get("numeric_coefficient_rho1_abs", "1.400851696295935e-13"),
    }


def zero_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "AZ4500_0_master_functional",
            "target": "A_shell_surface",
            "statement": "The J2 shell surface amplitude is the public l=2 projection of the parent source/residual/boundary/readout response.",
            "formula": "A_shell_surface=P_surf,l2 G_EH[kappa_eff deltaT_H_shell + deltaE_res_shell + deltaB_l2_shell + deltaReadout_l2_shell]",
            "result": "EXACT_FUNCTIONAL_FORM",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "AZ4500_1_zero_condition",
            "target": "source-silent shell",
            "statement": "If all four derivative channels vanish in the same source/coframe/radius convention, the shell has no public J2 amplitude.",
            "formula": "deltaT_H_shell=deltaE_res_shell=deltaB_l2_shell=deltaReadout_l2_shell=0 => A_shell_surface=0",
            "result": "CONDITIONAL_ZERO_THEOREM",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "AZ4500_2_current_owned_K2_lane",
            "target": "current owned K2 bookkeeping lane",
            "statement": "The current owned K2 artifact has no source-owned Hilbert/residual/boundary/readout derivative in 4485.",
            "formula": "current_owned(deltaT_H_K2,deltaE_res_K2,deltaB_l2_K2,deltaReadout_l2_K2)=0/absent",
            "result": "CURRENT_OWNED_RESPONSE_ZERO_NONCLAIM",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "AZ4500_3_generic_shell_blocker",
            "target": "generic DeltaKTF/shell branch",
            "statement": "Current-owned K2 silence does not prove the generic shell/kernel zero; 4498 shell verticality and boundary silence remain unsigned.",
            "formula": "generic_A_shell_zero requires Dq_shell=0 plus boundary/readout/source silence",
            "result": "GLOBAL_PARENT_ZERO_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "AZ4500_4_finite_fallback",
            "target": "finite shell amplitude",
            "statement": "If any derivative channel survives, it must enter the finite amplitude row and satisfy the J2 pressure bound.",
            "formula": "|A_H|+|A_E|+|A_B|+|A_R| <= tau_A_shell_surface",
            "result": "FINITE_ROW_READY_COMPONENT_VALUES_MISSING",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def source_component_rows() -> List[Dict[str, object]]:
    return [
        {
            "component_id": "ASC4500_0_Hilbert",
            "symbol": "A_H",
            "definition": "Hilbert/coframe stress contribution to the public shell quadrupole amplitude",
            "formula": "A_H=P_surf,l2 G_EH[kappa_eff deltaT_H_shell]",
            "zero_condition": "deltaT_H_shell=0 from matter/source descent or no source slot",
            "finite_condition": "source-backed tracefree l=2 Hilbert stress derivative with support and units",
            "source_basis": str(K2_SOURCE_4484),
            "status": "CURRENT_K2_ZERO_GENERIC_SHELL_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "component_id": "ASC4500_1_residual",
            "symbol": "A_E",
            "definition": "extra MTS residual equation contribution after EH baseline subtraction",
            "formula": "A_E=P_surf,l2 G_EH[deltaE_res_shell]",
            "zero_condition": "extra-sector l=2 residual is parent-zero or on-shell silent",
            "finite_condition": "operator coefficients and residual l=2 envelope are sourced",
            "source_basis": semicolon_paths([K2_SOURCE_4484, RESIDUAL_L2_1955]),
            "status": "FINITE_RESIDUAL_ROUTE_RETAINED",
            "valid_for_claim": False,
        },
        {
            "component_id": "ASC4500_2_boundary",
            "symbol": "A_B",
            "definition": "l=2 boundary/matching data contribution",
            "formula": "A_B=P_surf,l2 G_EH[deltaB_l2_shell]",
            "zero_condition": "fixed/asymptotically flat/no-flux boundary data independent of shell",
            "finite_condition": "boundary l=2 amplitude and radius normalization are sourced",
            "source_basis": str(K2_SOURCE_4484),
            "status": "BOUNDARY_DERIVATIVE_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "component_id": "ASC4500_3_readout",
            "symbol": "A_R",
            "definition": "public readout/coframe deformation contribution not already in g_obs",
            "formula": "A_R=P_surf,l2[deltaReadout_l2_shell]",
            "zero_condition": "same observed metric/coframe readout with no shell-dependent shadow/disformal term",
            "finite_condition": "readout l=2 projector coefficient is source-backed and bounded",
            "source_basis": semicolon_paths([K2_SOURCE_4484, PARENT_AUDIT_4498]),
            "status": "READOUT_ZERO_CONDITIONAL_PARENT_ROLE_UNSIGNED",
            "valid_for_claim": False,
        },
    ]


def finite_amplitude_rows(c: Mapping[str, str]) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "FAS4500_0_master",
            "quantity": "A_shell_surface",
            "formula": "A_shell_surface=A_H+A_E+A_B+A_R",
            "source_components": "ASC4500_0_Hilbert;ASC4500_1_residual;ASC4500_2_boundary;ASC4500_3_readout",
            "bound_formula": "|A_H|+|A_E|+|A_B|+|A_R| <= tau_A_shell_surface",
            "numeric_bound": c["a_shell_bound"],
            "status": "EXACT_SOURCE_ROW_STAGED_COMPONENT_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "row_id": "FAS4500_1_current_owned_K2",
            "quantity": "A_surface_K2_current_owned",
            "formula": "A_surface_K2=0 for current owned K2 source response",
            "source_components": "CSA4485_1_Hilbert_source;CSA4485_2_residual_equation;CSA4485_3_boundary;CSA4485_4_readout",
            "bound_formula": "0 <= tau_A_shell_surface",
            "numeric_bound": c["a_shell_bound"],
            "status": "CURRENT_OWNED_RESPONSE_ZERO_NONCLAIM_NOT_GLOBAL_PARENT_ZERO",
            "valid_for_claim": False,
        },
        {
            "row_id": "FAS4500_2_hessian_counterroute",
            "quantity": "A_surface_K2_finite_candidate",
            "formula": "A_surface_K2=s_K2*C_K2_unit*M2_K2 with M2_K2=-(kappa_STF/5)I4[hat_R] on the adopted Hessian branch",
            "source_components": "FQA4485_1_signed_source_moment;FQA4485_2_hessian_projected_moment",
            "bound_formula": "|s_K2*M2_K2| <= k2_product_bound",
            "numeric_bound": c["k2_product_bound"],
            "status": "FINITE_COUNTERROUTE_AVAILABLE_PARENT_ADOPTION_UNSIGNED",
            "valid_for_claim": False,
        },
    ]


def pressure_bound_rows(c: Mapping[str, str]) -> List[Dict[str, object]]:
    return [
        {
            "bound_id": "J2B4500_0_surface_amplitude",
            "quantity": "tau_A_shell_surface",
            "formula": "tau_A_shell_surface = two_epsilon_surface*J2_half_range_bound",
            "numeric_value": c["a_shell_bound"],
            "units": "dimensionless metric P2 amplitude",
            "source_path": str(J2_BOUNDS_3170),
            "status": "NUMERIC_IMPORTED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "bound_id": "J2B4500_1_j2_equivalent",
            "quantity": "tau_DeltaJ2_shell",
            "formula": "|DeltaJ2_shell| <= J2_half_range_bound",
            "numeric_value": c["j2_half_bound"],
            "units": "dimensionless J2",
            "source_path": str(J2_BOUNDS_3170),
            "status": "NUMERIC_IMPORTED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "bound_id": "J2B4500_2_composite_k2",
            "quantity": "tau_UpsilonK2",
            "formula": "|Upsilon_J2*K2| <= K2_corrected_surface_bound at rho=1",
            "numeric_value": c["k2_product_bound"],
            "units": "dimensionless K2 composite",
            "source_path": str(J2_BOUNDS_3170),
            "status": "NUMERIC_IMPORTED_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PA4500_0_current_owned_response",
            "clause": "current K2 source response",
            "current_status": "ZERO_OR_ABSENT_IN_CURRENT_ARTIFACTS",
            "evidence": semicolon_paths([K2_ZERO_4485, K2_AUDIT_4485]),
            "remaining_unsigned": "does not prove global parent shell zero",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4500_1_generic_shell_kernel",
            "clause": "generic shell verticality and boundary silence",
            "current_status": "UNSIGNED",
            "evidence": semicolon_paths([PARENT_AUDIT_4498, FORMAL_515]),
            "remaining_unsigned": "Dq_shell=0 and boundary/readout silence still need parent signature",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4500_2_finite_components",
            "clause": "finite amplitude components",
            "current_status": "EXACT_FORMULA_READY_VALUES_MISSING",
            "evidence": semicolon_paths([K2_FINITE_4485, RESIDUAL_L2_1955]),
            "remaining_unsigned": "A_H, A_E, A_B, A_R values or zero theorems missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "PA4500_3_pressure_bound",
            "clause": "J2 pressure bound",
            "current_status": "NUMERIC_READY_NONCLAIM",
            "evidence": semicolon_paths([J2_OPERATOR_4499, J2_BOUNDS_3170]),
            "remaining_unsigned": "bound cannot score until A_shell_surface is zeroed or valued",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4500_0_master_functional",
            "gate": "A_shell_surface master functional written",
            "passed": True,
            "claim_allowed": False,
            "detail": "A_H+A_E+A_B+A_R decomposition is explicit",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4500_1_current_owned_zero",
            "gate": "current owned K2 response is zero/absent",
            "passed": True,
            "claim_allowed": False,
            "detail": "useful for rejecting fake K2 pressure, not full local GR",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4500_2_global_parent_zero",
            "gate": "generic shell parent zero theorem",
            "passed": False,
            "claim_allowed": False,
            "detail": "shell verticality, boundary silence and source/readout descent remain unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4500_3_finite_source_score",
            "gate": "finite source components can be scored",
            "passed": False,
            "claim_allowed": False,
            "detail": "A_H/A_E/A_B/A_R component values or bounds still missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4500_4_local_GR_J2_promotion",
            "gate": "local GR/J2 promotion",
            "passed": False,
            "claim_allowed": False,
            "detail": "exact amplitude decomposition plus pressure bound is not a pass until zero/value rows close",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "what_moved_forward": "4500 writes the exact A_shell_surface source decomposition and imports the numeric J2 pressure bound",
            "what_is_derived": "A_shell_surface=0 follows if Hilbert, residual, boundary and readout l2 derivatives all vanish in the same source/coframe convention",
            "what_remains_blocked": "global parent shell zero is unsigned and finite component values A_H/A_E/A_B/A_R are still missing",
            "claim_status": "private_nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def status_rows() -> List[Dict[str, object]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "A_shell_master_functional_ready": True,
            "current_owned_K2_response_zero": True,
            "global_parent_zero_signed": False,
            "finite_component_values_ready": False,
            "J2_pressure_bound_ready": True,
            "local_GR_claim": False,
            "sharpest_open_clause": "derive or bound A_H, A_E, A_B, A_R; preferably prove all four vanish from parent kernel/source silence",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4500_0",
            "target": NEXT_TARGET,
            "preferred_route": "prove all A_shell_surface components vanish from parent source descent, residual silence, boundary silence and readout identity",
            "fallback_route": "fill the first finite component coefficient, starting with A_E residual or A_H Hilbert source, and compare against tau_A_shell_surface",
            "do_not_do": "promote current-owned K2 silence into a generic local-GR/J2 theorem",
            "valid_for_claim": False,
        }
    ]


def body(
    sources: Sequence[Mapping[str, object]],
    zero_rows: Sequence[Mapping[str, object]],
    components: Sequence[Mapping[str, object]],
    finite_rows: Sequence[Mapping[str, object]],
    bounds: Sequence[Mapping[str, object]],
    parent_audit: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4500 - J2 Shell Surface Amplitude Source Row Or Parent Kernel Zero

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Result

4500 attacks the amplitude that 4499 left unsigned. The public J2 conversion is no longer the fog. The real object is now

`A_shell_surface = A_H + A_E + A_B + A_R`,

with

`A_shell_surface=P_surf,l2 G_EH[kappa_eff deltaT_H_shell + deltaE_res_shell + deltaB_l2_shell + deltaReadout_l2_shell]`.

Therefore the parent-zero route is exact:

`deltaT_H_shell = deltaE_res_shell = deltaB_l2_shell = deltaReadout_l2_shell = 0 => A_shell_surface=0 => DeltaJ2_shell=0`.

The current owned K2 bookkeeping lane has zero/absent source derivatives in the present artifacts, but that is not promoted into a global shell theorem. If any component survives, it must satisfy the imported 4499/3170 pressure bound.

## Zero Theorem Rows

{table(zero_rows)}

## Source Components

{table(components)}

## Finite Amplitude Rows

{table(finite_rows)}

## J2 Pressure Bounds

{table(bounds)}

## Parent Signature Audit

{table(parent_audit)}

## Claim Gates

{table(gates)}

## Status

{table(statuses)}

## Next Target

{table(next_targets)}

## Source Register

{table(sources)}

## Decision Row

{table(decisions)}
"""


def append_claim_once() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                CLAIM_ID,
                "local_gr_newton_j2_shell_amplitude",
                "4500 derives the exact A_shell_surface source decomposition, proves the conditional zero law for simultaneous Hilbert/residual/boundary/readout silence, records current-owned K2 response as zero/absent without promoting a global theorem, and imports the numeric J2 pressure bound.",
                "4500 source register, A_shell zero theorem, source component rows, finite amplitude rows, pressure bounds, parent audit, claim gates, status and validation.",
                "private_A_shell_zero_or_finite_source_row_nonclaim",
                NEXT_TARGET,
                "promoting current-owned K2 source absence into generic shell/local-GR safety.",
                "local_gr_newton_j2_shell_amplitude",
                str(FORMAL_PATH),
                NEXT_TARGET,
                "derive or bound A_H/A_E/A_B/A_R component coefficients",
            ]
        )


def append_section_once(path: Path, marker: str, title: str, summary: str) -> None:
    current = text(path)
    if marker in current:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        handle.write(f"\n\n## {title}\n\nMarker: `{marker}`  \n{summary}\n")


def validate(
    c: Mapping[str, str],
    sources: Sequence[Mapping[str, object]],
    zero_rows: Sequence[Mapping[str, object]],
    components: Sequence[Mapping[str, object]],
    finite_rows: Sequence[Mapping[str, object]],
    bounds: Sequence[Mapping[str, object]],
    parent_audit: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    validations: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False})

    add("VAL4500_0_sources_exist_and_needles_found", all(row.get("exists") is True and row.get("needle_found") is True for row in sources), "all source-register paths exist and needles are found")
    add("VAL4500_1_master_functional_present", any(row.get("theorem_id") == "AZ4500_0_master_functional" and "A_shell_surface=P_surf" in str(row.get("formula")) for row in zero_rows), "master amplitude functional present")
    add("VAL4500_2_zero_theorem_present", any(row.get("theorem_id") == "AZ4500_1_zero_condition" and "=> A_shell_surface=0" in str(row.get("formula")) for row in zero_rows), "simultaneous derivative-zero theorem present")
    add("VAL4500_3_current_owned_zero_nonclaim", any(row.get("row_id") == "FAS4500_1_current_owned_K2" and "CURRENT_OWNED" in str(row.get("status")) for row in finite_rows), "current owned K2 zero row retained as nonclaim")
    add("VAL4500_4_four_source_components", len(components) == 4 and {row["symbol"] for row in components} == {"A_H", "A_E", "A_B", "A_R"}, "A_H/A_E/A_B/A_R source components present")
    add("VAL4500_5_pressure_bound_numeric", any(row.get("bound_id") == "J2B4500_0_surface_amplitude" and abs(float(row.get("numeric_value")) - float(c["a_shell_bound"])) < 1e-25 for row in bounds), f"A_shell_bound={c['a_shell_bound']}")
    add("VAL4500_6_global_parent_zero_unsigned", any(row.get("audit_id") == "PA4500_1_generic_shell_kernel" and row.get("current_status") == "UNSIGNED" for row in parent_audit), "global shell kernel remains unsigned")
    add("VAL4500_7_claim_gates_block_promotion", all(str(row.get("claim_allowed")).lower() == "false" for row in gates) and any(row.get("gate_id") == "CG4500_4_local_GR_J2_promotion" and str(row.get("passed")).lower() == "false" for row in gates), "claim gates block local-GR/J2 promotion")
    add("VAL4500_8_status_local_GR_false", bool(statuses) and str(statuses[0].get("local_GR_claim")).lower() == "false", "local_GR_claim remains false")
    add("VAL4500_9_next_target_selected", bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET, NEXT_TARGET)
    all_rows = [*sources, *zero_rows, *components, *finite_rows, *bounds, *parent_audit, *gates, *statuses, *next_targets]
    add("VAL4500_10_all_generated_rows_nonclaim", all(str(row.get("valid_for_claim")).lower() == "false" for row in all_rows), "all generated rows remain nonclaim")
    csv_ok = True
    csv_detail: List[str] = []
    for csv_path in csv_paths:
        try:
            parsed_rows = read_csv(csv_path)
            csv_detail.append(f"{csv_path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_ok = False
            csv_detail.append(f"{csv_path.name}:ERROR:{exc}")
    add("VAL4500_11_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4500_12_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add("VAL4500_13_claim_register_updated", any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), "claims register contains L-342")
    add("VAL4500_14_spine_and_packet_updated", MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH), "spine and packet contain 4500 markers")
    add("VAL4500_15_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    c = constants()
    sources = source_rows()
    zero_rows = zero_theorem_rows()
    components = source_component_rows()
    finite_rows = finite_amplitude_rows(c)
    bounds = pressure_bound_rows(c)
    parent_audit = parent_audit_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_THEOREM_CSV, zero_rows)
    write_csv(SOURCE_COMPONENTS_CSV, components)
    write_csv(FINITE_AMPLITUDE_CSV, finite_rows)
    write_csv(PRESSURE_BOUND_CSV, bounds)
    write_csv(PARENT_AUDIT_CSV, parent_audit)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    doc = body(sources, zero_rows, components, finite_rows, bounds, parent_audit, gates, decisions, statuses, next_targets)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_claim_once()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4500 J2 Shell Surface Amplitude Source Row Or Parent Kernel Zero",
        "4500 attacks the parent-owned J2 amplitude directly. It derives A_shell_surface=A_H+A_E+A_B+A_R, proves the conditional zero law if Hilbert/residual/boundary/readout l2 derivatives all vanish, imports the numeric J2 pressure bound, and refuses to promote current-owned K2 source absence into a generic local-GR theorem.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4500 Packet Integration",
        "The local packet now has a concrete amplitude object to kill or score: A_shell_surface. The next lever is not another broad audit; it is deriving or bounding the four components A_H, A_E, A_B and A_R.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        ZERO_THEOREM_CSV,
        SOURCE_COMPONENTS_CSV,
        FINITE_AMPLITUDE_CSV,
        PRESSURE_BOUND_CSV,
        PARENT_AUDIT_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(c, sources, zero_rows, components, finite_rows, bounds, parent_audit, gates, statuses, next_targets, csv_paths)
    write_csv(VALIDATION_PATH, validations)

    failed = [row for row in validations if str(row.get("passed")).lower() != "true"]
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Generated {CHECKPOINT}: {FORMAL_PATH}")
    print(f"Validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
