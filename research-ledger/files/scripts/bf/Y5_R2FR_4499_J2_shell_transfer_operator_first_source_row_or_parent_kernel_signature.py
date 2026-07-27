from __future__ import annotations

import csv
import math
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

CHECKPOINT = "4499"
CLAIM_ID = "L-341"
MARKER = "PPC4161_J2_SHELL_TRANSFER_OPERATOR_FIRST_SOURCE_ROW_OR_PARENT_KERNEL_SIGNATURE_4499"
PACKET_MARKER = "PPC4161_PACKET_J2_SHELL_TRANSFER_OPERATOR_FIRST_SOURCE_ROW_OR_PARENT_KERNEL_SIGNATURE_4499"
DECISION = "PUBLIC_J2_METRIC_TRANSFER_DERIVED_ORBITAL_FORMULAS_STAGED_SHELL_AMPLITUDE_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4500-Y5-R2FR-J2-shell-surface-amplitude-source-row-or-parent-kernel-zero.md"

FORMAL_PATH = FORMAL / "515-PPC4161-J2-shell-transfer-operator-first-source-row-or-parent-kernel-signature.md"
DOC_PATH = POST / "4499-Y5-R2FR-J2-shell-transfer-operator-first-source-row-or-parent-kernel-signature.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4499_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4499_SOURCE_REGISTER.csv"
PUBLIC_J2_CSV = SOURCE_DIR / "P8_Y5_R2FR_4499_PUBLIC_J2_TRANSFER_DERIVATION.csv"
J2_OPERATOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4499_J2_SHELL_TRANSFER_OPERATOR.csv"
ORBITAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4499_ORBITAL_PRECESSION_TRANSFER.csv"
PARENT_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4499_PARENT_SIGNATURE_AUDIT.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4499_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4499_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4499_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4499_NEXT_TARGET.csv"

FORMAL_514 = FORMAL / "514-PPC4161-shell-projection-arena-operator-source-fill-or-owner-kernel-parent-signature.md"
POST_4498 = POST / "4498-Y5-R2FR-shell-projection-arena-operator-source-fill-or-owner-kernel-parent-signature.md"
SCRIPT_4498 = SCRIPT_DIR / "Y5_R2FR_4498_shell_projection_arena_operator_source_fill_or_owner_kernel_parent_signature.py"
OPERATOR_4498 = SOURCE_DIR / "P8_Y5_R2FR_4498_ARENA_OPERATOR_SOURCE_CONTRACT.csv"
STATUS_4498 = SOURCE_DIR / "P8_Y5_R2FR_4498_STATUS.csv"
J2_CLAUSES_4483 = SOURCE_DIR / "P8_Y5_R2FR_4483_PI_J2_METRIC_OWNER_CLAUSES.csv"
PIJ2_4484 = SOURCE_DIR / "P8_Y5_R2FR_4484_PIJ2METRIC_TRANSFER_ROWS.csv"
J2_SCORER_4482 = SOURCE_DIR / "P8_Y5_R2FR_4482_UPSILON_J2_TRANSFER_SCORER.csv"
J2_NORM_3170 = SOURCE_DIR / "P8_Y5_R2FR_3170_SOLAR_J2_NORMALIZATION_DERIVATION.csv"
J2_BOUNDS_3170 = SOURCE_DIR / "P8_Y5_R2FR_3170_CORRECTED_J2EFF_K2_BOUNDS.csv"
EXTRACTOR_3173 = SOURCE_DIR / "P8_Y5_R2FR_3173_OPERATOR_MATCH_DERIVATION.csv"
EXTRACTOR_CONTRACT_3173 = SOURCE_DIR / "P8_Y5_R2FR_3173_PIJ2_EXTRACTOR_CONTRACT.csv"
FINITE_BRIDGE_4482 = SOURCE_DIR / "P8_Y5_R2FR_4482_FINITE_L2_SCORER_BRIDGE.csv"
RESIDUAL_L2_1955 = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1955_RESIDUAL_L2_BOUND_LEDGER.csv"
FORMAL_496 = FORMAL / "496-PPC4161-orientation-carrier-zero-proof-or-quadrupole-residual-scorer.md"
FORMAL_506 = FORMAL / "506-PPC4161-gluing-multiplier-parent-origin-or-PPN-transfer-matrix.md"

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


def float_from_row(path: Path, key: str, key_value: str, column: str) -> float:
    row = rows_by(path, key).get(key_value, {})
    value = row.get(column, "")
    if value == "":
        raise ValueError(f"missing {column} in {path.name}:{key_value}")
    return float(value)


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4499_00_formal514", "4498 formal handoff", FORMAL_514, "OP4498_2_J2", "4498 selected J2 as first non-PPN operator target"),
        ("SRC4499_01_post4498", "4498 post mirror", POST_4498, "R_A=Pi_A T_shell", "common shell operator law"),
        ("SRC4499_02_operator4498", "4498 operator source contract", OPERATOR_4498, "OP4498_2_J2", "J2 source-normalized contract row"),
        ("SRC4499_03_status4498", "4498 status", STATUS_4498, "4499-Y5-R2FR-J2-shell-transfer-operator-first-source-row-or-parent-kernel-signature.md", "4498 next target points to 4499"),
        ("SRC4499_04_j2clauses4483", "4483 J2 owner clauses", J2_CLAUSES_4483, "MOC4483_1_public_metric_projection", "public metric projection was the named missing kernel"),
        ("SRC4499_05_pij24484", "4484 PiJ2 transfer rows", PIJ2_4484, "PI4484_2_finite_source_functional", "finite source functional for public quadrupole amplitude"),
        ("SRC4499_06_j2scorer4482", "4482 Upsilon/J2 scorer", J2_SCORER_4482, "J2T4482_2_corrected_J2eff", "corrected J2_eff transfer formula"),
        ("SRC4499_07_norm3170", "3170 solar J2 normalization", J2_NORM_3170, "JN3170_1_corrected_J2eff_map", "two-epsilon surface normalization"),
        ("SRC4499_08_bounds3170", "3170 corrected J2 bounds", J2_BOUNDS_3170, "CJ3170_2_Rozelot_half_range_proxy", "rough half-range pressure row"),
        ("SRC4499_09_extractor3173", "3173 exact Upsilon formula", EXTRACTOR_3173, "OP3173_3_exact_Upsilon_formula", "non-fitted parent extractor contract"),
        ("SRC4499_10_excontract3173", "3173 extractor contract", EXTRACTOR_CONTRACT_3173, "EX3173_4_compute_kernel", "machine-readable PiJ2 extractor contract"),
        ("SRC4499_11_bridge4482", "4482 finite l2 bridge", FINITE_BRIDGE_4482, "FLS4482_0_marker_amplitude_to_J2", "generic amplitude to J2 bridge"),
        ("SRC4499_12_residual1955", "1955 residual l2 scorer", RESIDUAL_L2_1955, "RB1955_0_residual_bound_formula", "fair GR-baseline residual fallback"),
        ("SRC4499_13_formal496", "4480 orbital quadrupole gate", FORMAL_496, "QRS4480_5_orbital_quadrupole_gate", "orbital precession arena needs transfer"),
        ("SRC4499_14_formal506", "4490 symbolic J2 transfer", FORMAL_506, "J2_eff = A_g00_l2/(2*epsilon_surface)", "existing symbolic transfer now made source-row explicit"),
        ("SRC4499_15_script4498", "4498 generator", SCRIPT_4498, 'CHECKPOINT = "4498"', "reproducible predecessor generator"),
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


def constants() -> Dict[str, float]:
    two_epsilon = float_from_row(J2_NORM_3170, "derivation_id", "JN3170_1_corrected_J2eff_map", "two_epsilon_sun_surface")
    c_k2_unit = float_from_row(J2_BOUNDS_3170, "bound_id", "CJ3170_2_Rozelot_half_range_proxy", "C_K2_unit")
    j2_half_bound = float_from_row(J2_BOUNDS_3170, "bound_id", "CJ3170_2_Rozelot_half_range_proxy", "J2_eff_bound")
    a_metric_bound = float_from_row(J2_BOUNDS_3170, "bound_id", "CJ3170_2_Rozelot_half_range_proxy", "A_metric_bound_surface")
    k2_bound = float_from_row(J2_BOUNDS_3170, "bound_id", "CJ3170_2_Rozelot_half_range_proxy", "K2_corrected_surface_bound")
    return {
        "two_epsilon": two_epsilon,
        "inv_two_epsilon": 1.0 / two_epsilon,
        "c_k2_unit": c_k2_unit,
        "j2_half_bound": j2_half_bound,
        "a_metric_bound": a_metric_bound,
        "k2_bound": k2_bound,
        "k2_to_j2_u1": c_k2_unit / two_epsilon,
    }


def public_j2_rows(c: Mapping[str, float]) -> List[Dict[str, object]]:
    return [
        {
            "derivation_id": "PJ4499_0_public_p2_amplitude",
            "object": "A_shell_surface",
            "statement": "Represent the surviving shell/public l=2 metric perturbation as h00_P2(r)=A_shell_surface*rho^-3*P2(cos theta)",
            "formula": "A_shell(r)=A_shell_surface*rho^-3, rho=r/R_source",
            "numeric_value": "",
            "units": "dimensionless metric amplitude",
            "status": "DEFINITION_READY",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PJ4499_1_standard_j2_amplitude",
            "object": "A_J2_surface",
            "statement": "Use the 3170 project convention for the solar exterior J2 metric amplitude.",
            "formula": "A_J2(r)=two_epsilon_surface*J2*rho^-3",
            "numeric_value": f"two_epsilon_surface={c['two_epsilon']:.15e}",
            "units": "dimensionless metric amplitude",
            "status": "SOURCE_BACKED_BY_3170",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PJ4499_2_shell_to_j2",
            "object": "DeltaJ2_shell",
            "statement": "Equating the shell P2 amplitude to the standard J2 amplitude gives the public metric transfer row.",
            "formula": "DeltaJ2_shell = s_J2*A_shell_surface*rho^3/two_epsilon_surface",
            "numeric_value": f"1/two_epsilon_surface={c['inv_two_epsilon']:.15e}",
            "units": "dimensionless J2",
            "status": "PUBLIC_METRIC_TRANSFER_NUMERIC_SIGN_CONVENTION_EXPLICIT",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PJ4499_3_k2_composite",
            "object": "DeltaJ2_K2",
            "statement": "If the shell amplitude is the K2 composite amplitude from the existing Upsilon lane, the corrected J2 map follows.",
            "formula": "DeltaJ2_K2 = s_J2*Upsilon_J2*K2*C_K2_unit*rho^3/two_epsilon_surface",
            "numeric_value": f"C_K2_unit/two_epsilon_surface={c['k2_to_j2_u1']:.15e}",
            "units": "dimensionless J2 per K2 per Upsilon at rho=1",
            "status": "COMPOSITE_TRANSFER_DERIVED_UPSILON_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "PJ4499_4_half_range_surface_pressure",
            "object": "A_shell_surface_bound",
            "statement": "The 3170 half-range proxy translates into a direct bound on public shell P2 surface amplitude.",
            "formula": "|A_shell_surface| <= two_epsilon_surface*J2_half_range_bound",
            "numeric_value": f"{c['a_metric_bound']:.15e}",
            "units": "dimensionless metric amplitude",
            "status": "NUMERIC_PRESSURE_ROW_AVAILABLE_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def j2_operator_rows(c: Mapping[str, float]) -> List[Dict[str, object]]:
    return [
        {
            "operator_id": "J2OP4499_0_public_metric_conversion",
            "input_symbol": "A_shell_surface",
            "output_symbol": "DeltaJ2_shell",
            "operator_formula": "Pi_J2_public[A_shell_surface] = s_J2*A_shell_surface*rho^3/two_epsilon_surface",
            "numeric_coefficient_rho1_abs": f"{c['inv_two_epsilon']:.15e}",
            "source_paths": semicolon_paths([J2_NORM_3170, J2_SCORER_4482, FINITE_BRIDGE_4482]),
            "numeric_ready": True,
            "claim_effect": "fills the public metric conversion, not the MTS parent amplitude",
            "status": "FIRST_J2_TRANSFER_ROW_FILLED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "operator_id": "J2OP4499_1_k2_to_j2_composite",
            "input_symbol": "Upsilon_J2*K2*C_K2_unit",
            "output_symbol": "DeltaJ2_K2",
            "operator_formula": "DeltaJ2_K2=s_J2*Upsilon_J2*K2*C_K2_unit*rho^3/two_epsilon_surface",
            "numeric_coefficient_rho1_abs": f"{c['k2_to_j2_u1']:.15e}",
            "source_paths": semicolon_paths([PIJ2_4484, EXTRACTOR_3173, EXTRACTOR_CONTRACT_3173, J2_BOUNDS_3170]),
            "numeric_ready": False,
            "claim_effect": "Upsilon_J2 remains parent-unsigned",
            "status": "COMPOSITE_READY_UPSILON_VALUE_MISSING",
            "valid_for_claim": False,
        },
        {
            "operator_id": "J2OP4499_2_zero_branch",
            "input_symbol": "A_shell_surface",
            "output_symbol": "DeltaJ2_shell",
            "operator_formula": "A_shell_surface=0 from parent kernel/source silence => DeltaJ2_shell=0",
            "numeric_coefficient_rho1_abs": "0",
            "source_paths": semicolon_paths([FORMAL_514, PIJ2_4484, J2_CLAUSES_4483]),
            "numeric_ready": False,
            "claim_effect": "zero branch needs parent signature, not normalization",
            "status": "ZERO_ROUTE_EXACT_IF_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "operator_id": "J2OP4499_3_finite_source_functional",
            "input_symbol": "deltaT_H_K2+deltaE_res_K2+deltaB_l2+deltaReadout_l2",
            "output_symbol": "A_shell_surface",
            "operator_formula": "A_shell_surface=P_surf,l2 G_EH[kappa_eff deltaT_H_K2 + deltaE_res_K2 + deltaB_l2 + deltaReadout_l2]",
            "numeric_coefficient_rho1_abs": "MISSING_SOURCE_FUNCTIONAL_INPUTS",
            "source_paths": semicolon_paths([PIJ2_4484, EXTRACTOR_3173, RESIDUAL_L2_1955]),
            "numeric_ready": False,
            "claim_effect": "finite source branch is exact-formula-ready but coefficient-empty",
            "status": "FINITE_SOURCE_FUNCTIONAL_AVAILABLE_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "operator_id": "J2OP4499_4_surface_pressure_bound",
            "input_symbol": "A_shell_surface",
            "output_symbol": "J2 half-range pressure",
            "operator_formula": f"|A_shell_surface| <= {c['a_metric_bound']:.15e}; equivalently |Upsilon_J2*K2| <= {c['k2_bound']:.15e} at rho=1",
            "numeric_coefficient_rho1_abs": f"{c['a_metric_bound']:.15e}",
            "source_paths": semicolon_paths([J2_BOUNDS_3170, J2_SCORER_4482]),
            "numeric_ready": True,
            "claim_effect": "scoring pressure exists once A_shell_surface or Upsilon_J2*K2 is parent-owned",
            "status": "BOUND_READY_SOURCE_AMPLITUDE_MISSING",
            "valid_for_claim": False,
        },
    ]


def orbital_rows(c: Mapping[str, float]) -> List[Dict[str, object]]:
    return [
        {
            "orbital_id": "ORB4499_0_nodal_precession",
            "observable": "nodal precession",
            "formula": "DeltaOmega_dot = -(3/2)*n*(R_source/[a*(1-e^2)])^2*cos(i)*DeltaJ2_shell",
            "substitution": "DeltaJ2_shell=s_J2*A_shell_surface*rho^3/two_epsilon_surface",
            "numeric_j2_coefficient": "requires orbit n,a,e,i,R_source",
            "source_status": "STANDARD_J2_ORBIT_AVERAGE_FORMULA_STAGED",
            "numeric_ready": False,
            "valid_for_claim": False,
        },
        {
            "orbital_id": "ORB4499_1_pericenter_precession",
            "observable": "argument of pericenter precession",
            "formula": "Deltaomega_dot = (3/4)*n*(R_source/[a*(1-e^2)])^2*(5*cos(i)^2-1)*DeltaJ2_shell",
            "substitution": "DeltaJ2_shell=s_J2*A_shell_surface*rho^3/two_epsilon_surface",
            "numeric_j2_coefficient": "requires orbit n,a,e,i,R_source",
            "source_status": "STANDARD_J2_ORBIT_AVERAGE_FORMULA_STAGED",
            "numeric_ready": False,
            "valid_for_claim": False,
        },
        {
            "orbital_id": "ORB4499_2_bound_inversion",
            "observable": "orbit-specific shell amplitude bound",
            "formula": "|A_shell_surface| <= two_epsilon_surface*|tau_orbital_Q|/|C_orbit_J2|",
            "substitution": "C_orbit_J2 is the nodal/pericenter coefficient multiplying DeltaJ2_shell",
            "numeric_j2_coefficient": f"two_epsilon_surface={c['two_epsilon']:.15e}",
            "source_status": "INVERSION_DERIVED_ALLOWANCE_MISSING",
            "numeric_ready": False,
            "valid_for_claim": False,
        },
    ]


def parent_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "JA4499_0_public_conversion",
            "clause": "public l=2 metric amplitude converts to J2",
            "current_status": "DERIVED_NUMERIC_IN_3170_CONVENTION",
            "evidence": semicolon_paths([J2_NORM_3170, J2_SCORER_4482]),
            "remaining_unsigned": "sign convention is explicit; source amplitude still absent",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "JA4499_1_shell_surface_amplitude",
            "clause": "A_shell_surface is parent-owned or zero",
            "current_status": "UNSIGNED",
            "evidence": semicolon_paths([FORMAL_514, PIJ2_4484, EXTRACTOR_3173]),
            "remaining_unsigned": "no parent-owned value for A_shell_surface or Upsilon_J2*K2",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "JA4499_2_source_domain_radius",
            "clause": "same source radius/coframe/rho convention",
            "current_status": "PARAMETERIZED_NOT_SIGNED",
            "evidence": semicolon_paths([J2_NORM_3170, PIJ2_4484]),
            "remaining_unsigned": "rho and R_source must match the source-domain transfer",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "JA4499_3_orbital_allowance",
            "clause": "orbit-specific comparator allowance",
            "current_status": "FORMULA_READY_NUMERIC_ALLOWANCE_MISSING",
            "evidence": semicolon_paths([FORMAL_496, RESIDUAL_L2_1955]),
            "remaining_unsigned": "need a chosen orbit/data comparator and covariance/allowance",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "JA4499_4_local_gr_verdict",
            "clause": "J2/local-GR branch",
            "current_status": "NOT_CLAIMED",
            "evidence": semicolon_paths([SOURCE_REGISTER, J2_OPERATOR_CSV]),
            "remaining_unsigned": "public conversion is filled but parent amplitude/kernel is not",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "G4499_0_public_j2_conversion",
            "gate": "public P2 metric amplitude to J2 conversion is numeric",
            "passed": True,
            "claim_allowed": False,
            "detail": "DeltaJ2_shell=A_shell_surface/two_epsilon_surface in 3170 convention",
            "valid_for_claim": False,
        },
        {
            "gate_id": "G4499_1_parent_shell_amplitude",
            "gate": "A_shell_surface or Upsilon_J2*K2 is parent-owned",
            "passed": False,
            "claim_allowed": False,
            "detail": "4499 deliberately does not invent the parent amplitude",
            "valid_for_claim": False,
        },
        {
            "gate_id": "G4499_2_orbital_transfer_formula",
            "gate": "J2 to nodal/pericenter transfer formulas are staged",
            "passed": True,
            "claim_allowed": False,
            "detail": "formula-ready but orbit/covariance allowance missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "G4499_3_scoring_ready",
            "gate": "J2/orbital branch has numeric source amplitude and allowance",
            "passed": False,
            "claim_allowed": False,
            "detail": "need A_shell_surface or parent zero plus orbit-specific allowance",
            "valid_for_claim": False,
        },
        {
            "gate_id": "G4499_4_local_GR_promotion",
            "gate": "local GR/Newton/J2 promotion",
            "passed": False,
            "claim_allowed": False,
            "detail": "public transfer row is necessary but not sufficient",
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
            "what_moved_forward": "4499 fills the first J2 shell transfer operator row: public P2 metric amplitude maps to DeltaJ2 with numeric coefficient 1/two_epsilon_surface",
            "what_is_derived": "DeltaJ2_shell=s_J2*A_shell_surface*rho^3/two_epsilon_surface and the nodal/pericenter precession transfer formulas are staged",
            "what_remains_blocked": "A_shell_surface or Upsilon_J2*K2 is not parent-owned, and no orbit-specific allowance is selected",
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
            "public_j2_transfer_numeric": True,
            "orbital_transfer_formula_ready": True,
            "parent_shell_amplitude_ready": False,
            "orbit_allowance_ready": False,
            "local_GR_claim": False,
            "sharpest_open_clause": "source or zero A_shell_surface/Upsilon_J2*K2 before scoring J2/orbital residuals",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4499_0",
            "target": NEXT_TARGET,
            "preferred_route": "derive A_shell_surface=0 from the parent shell-kernel/source-silence theorem",
            "fallback_route": "fill a source-backed finite A_shell_surface or Upsilon_J2*K2 row and score it through the 4499 J2 transfer operator",
            "do_not_do": "treat the public conversion coefficient as the missing parent amplitude",
            "valid_for_claim": False,
        }
    ]


def body(
    sources: Sequence[Mapping[str, object]],
    public_j2: Sequence[Mapping[str, object]],
    operators: Sequence[Mapping[str, object]],
    orbitals: Sequence[Mapping[str, object]],
    parent_audit: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4499 - J2 Shell Transfer Operator First Source Row Or Parent Kernel Signature

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Result

4499 fills the first real J2 transfer row. It does **not** pretend the MTS parent has supplied the shell amplitude. It derives the public conversion that any surviving shell amplitude must pass through.

Using the existing 3170 convention,

`A_J2(r) = two_epsilon_surface * J2 * rho^-3`.

So a shell/public metric quadrupole amplitude

`A_shell(r) = A_shell_surface * rho^-3`

maps to

`DeltaJ2_shell = s_J2 * A_shell_surface * rho^3 / two_epsilon_surface`.

At `rho=1`, the absolute conversion coefficient is `1/two_epsilon_surface`. This fills `Pi_J2_public`; it does not fill `A_shell_surface`.

## Public J2 Transfer Derivation

{table(public_j2)}

## J2 Shell Transfer Operator

{table(operators)}

## Orbital Precession Transfer

{table(orbitals)}

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
                "local_gr_newton_j2_shell_transfer",
                "4499 derives the first J2 shell transfer operator row: public l=2 metric amplitude A_shell_surface maps to DeltaJ2_shell by the 3170 two-epsilon convention, and nodal/pericenter transfer formulas are staged; no parent shell amplitude or local-GR claim is promoted.",
                "4499 source register, public J2 transfer derivation, J2 shell transfer operator rows, orbital transfer formulas, parent audit, claim gates, status and validation.",
                "private_public_J2_transfer_nonclaim",
                NEXT_TARGET,
                "mistaking the public conversion coefficient for a parent-owned MTS shell amplitude.",
                "local_gr_newton_j2_shell_transfer",
                str(FORMAL_PATH),
                NEXT_TARGET,
                "source or zero A_shell_surface/Upsilon_J2*K2 before scoring J2/orbital residuals",
            ]
        )


def append_section_once(path: Path, marker: str, title: str, summary: str) -> None:
    current = text(path)
    if marker in current:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        handle.write(f"\n\n## {title}\n\nMarker: `{marker}`  \n{summary}\n")


def validate(
    c: Mapping[str, float],
    sources: Sequence[Mapping[str, object]],
    public_j2: Sequence[Mapping[str, object]],
    operators: Sequence[Mapping[str, object]],
    orbitals: Sequence[Mapping[str, object]],
    parent_audit: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    validations: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False})

    public_conversion = [row for row in operators if row.get("operator_id") == "J2OP4499_0_public_metric_conversion"]
    k2_composite = [row for row in operators if row.get("operator_id") == "J2OP4499_1_k2_to_j2_composite"]
    local_gate = [row for row in gates if row.get("gate_id") == "G4499_4_local_GR_promotion"]

    add("VAL4499_0_sources_exist_and_needles_found", all(row.get("exists") is True and row.get("needle_found") is True for row in sources), "all source-register paths exist and needles are found")
    add("VAL4499_1_two_epsilon_numeric", c["two_epsilon"] > 0.0 and math.isfinite(c["inv_two_epsilon"]), f"two_epsilon={c['two_epsilon']:.15e}")
    add("VAL4499_2_public_conversion_row_filled", bool(public_conversion) and str(public_conversion[0].get("numeric_ready")).lower() == "true" and abs(float(public_conversion[0]["numeric_coefficient_rho1_abs"]) - c["inv_two_epsilon"]) / c["inv_two_epsilon"] < 1e-12, "J2 public conversion numeric coefficient matches 1/two_epsilon")
    add("VAL4499_3_k2_composite_retains_unsigned_up", bool(k2_composite) and str(k2_composite[0].get("numeric_ready")).lower() == "false" and "UPSILON" in str(k2_composite[0].get("status")).upper(), "Upsilon_J2 remains unsigned")
    add("VAL4499_4_public_derivation_contains_shell_to_j2", any(row.get("derivation_id") == "PJ4499_2_shell_to_j2" and "DeltaJ2_shell" in str(row.get("formula")) for row in public_j2), "shell-to-J2 formula present")
    add("VAL4499_5_orbital_formulas_staged", len(orbitals) >= 3 and any("DeltaOmega_dot" in str(row.get("formula")) for row in orbitals) and any("Deltaomega_dot" in str(row.get("formula")) for row in orbitals), "nodal and pericenter transfer formulas present")
    add("VAL4499_6_parent_amplitude_unsigned", any(row.get("audit_id") == "JA4499_1_shell_surface_amplitude" and row.get("current_status") == "UNSIGNED" for row in parent_audit), "A_shell_surface remains unsigned")
    add("VAL4499_7_claim_gates_block_local_gr", bool(local_gate) and str(local_gate[0].get("passed")).lower() == "false" and all(str(row.get("claim_allowed")).lower() == "false" for row in gates), "claim gates block promotion")
    add("VAL4499_8_status_local_GR_false", bool(statuses) and str(statuses[0].get("local_GR_claim")).lower() == "false", "local_GR_claim remains false")
    add("VAL4499_9_next_target_selected", bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET, NEXT_TARGET)
    all_rows = [*sources, *public_j2, *operators, *orbitals, *parent_audit, *gates, *statuses, *next_targets]
    add("VAL4499_10_all_generated_rows_nonclaim", all(str(row.get("valid_for_claim")).lower() == "false" for row in all_rows), "all generated rows remain nonclaim")
    csv_ok = True
    csv_detail: List[str] = []
    for csv_path in csv_paths:
        try:
            parsed_rows = read_csv(csv_path)
            csv_detail.append(f"{csv_path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_ok = False
            csv_detail.append(f"{csv_path.name}:ERROR:{exc}")
    add("VAL4499_11_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4499_12_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add("VAL4499_13_claim_register_updated", any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), "claims register contains L-341")
    add("VAL4499_14_spine_and_packet_updated", MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH), "spine and packet contain 4499 markers")
    add("VAL4499_15_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    c = constants()
    sources = source_rows()
    public_j2 = public_j2_rows(c)
    operators = j2_operator_rows(c)
    orbitals = orbital_rows(c)
    parent_audit = parent_audit_rows()
    gates = gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PUBLIC_J2_CSV, public_j2)
    write_csv(J2_OPERATOR_CSV, operators)
    write_csv(ORBITAL_CSV, orbitals)
    write_csv(PARENT_AUDIT_CSV, parent_audit)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    doc = body(sources, public_j2, operators, orbitals, parent_audit, gates, decisions, statuses, next_targets)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_claim_once()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4499 J2 Shell Transfer Operator First Source Row Or Parent Kernel Signature",
        "4499 fills the first non-PPN public-metric transfer row: A_shell_surface maps to DeltaJ2_shell through the 3170 two-epsilon convention, and nodal/pericenter J2 orbital transfer formulas are staged. This gives the local branch a concrete J2 scoring pipe while keeping the MTS parent amplitude A_shell_surface/Upsilon_J2*K2 unsigned and nonclaim.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4499 Packet Integration",
        "The private packet now separates public J2 normalization from parent source ownership. We can no longer say only 'J2 missing': the public conversion is filled; the next exact target is the parent shell amplitude zero/source row.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        PUBLIC_J2_CSV,
        J2_OPERATOR_CSV,
        ORBITAL_CSV,
        PARENT_AUDIT_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(c, sources, public_j2, operators, orbitals, parent_audit, gates, statuses, next_targets, csv_paths)
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
