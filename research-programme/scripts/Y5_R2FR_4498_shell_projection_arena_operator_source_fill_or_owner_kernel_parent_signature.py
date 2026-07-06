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

CHECKPOINT = "4498"
CLAIM_ID = "L-340"
MARKER = "PPC4161_SHELL_PROJECTION_ARENA_OPERATOR_SOURCE_FILL_OR_OWNER_KERNEL_PARENT_SIGNATURE_4498"
PACKET_MARKER = "PPC4161_PACKET_SHELL_PROJECTION_ARENA_OPERATOR_SOURCE_FILL_OR_OWNER_KERNEL_PARENT_SIGNATURE_4498"
DECISION = "PPN_OPERATOR_FILLED_NUMERIC_OTHER_ARENAS_SOURCE_NORMALIZED_CONTRACTS_STAGED_PARENT_KERNEL_UNSIGNED_NONCLAIM"
NEXT_TARGET = "4499-Y5-R2FR-J2-shell-transfer-operator-first-source-row-or-parent-kernel-signature.md"

FORMAL_PATH = FORMAL / "514-PPC4161-shell-projection-arena-operator-source-fill-or-owner-kernel-parent-signature.md"
DOC_PATH = POST / "4498-Y5-R2FR-shell-projection-arena-operator-source-fill-or-owner-kernel-parent-signature.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4498_VALIDATION.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4498_SOURCE_REGISTER.csv"
PARENT_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4498_PARENT_SIGNATURE_AUDIT.csv"
TAIL_BASIS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4498_SHELL_TAIL_VECTOR_BASIS.csv"
OPERATOR_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4498_ARENA_OPERATOR_SOURCE_CONTRACT.csv"
NUMERIC_PPN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4498_NUMERIC_PPN_OPERATOR_ROWS.csv"
CROSS_ARENA_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4498_CROSS_ARENA_OPERATOR_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4498_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4498_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4498_NEXT_TARGET.csv"

FORMAL_513 = FORMAL / "513-PPC4161-nonlocal-owner-kernel-theorem-or-shell-projection-arena-transfer-matrix.md"
POST_4497 = POST / "4497-Y5-R2FR-nonlocal-owner-kernel-theorem-or-shell-projection-arena-transfer-matrix.md"
SCRIPT_4497 = SCRIPT_DIR / "Y5_R2FR_4497_nonlocal_owner_kernel_theorem_or_shell_projection_arena_transfer_matrix.py"
ARENA_4497 = SOURCE_DIR / "P8_Y5_R2FR_4497_SHELL_PROJECTION_ARENA_TRANSFER_MATRIX.csv"
COMPARATOR_4496 = SOURCE_DIR / "P8_Y5_R2FR_4496_SHELL_PROJECTION_COMPARATOR.csv"
CONTRACT_4334 = SOURCE_DIR / "P8_Y5_R2FR_4334_PROJECTION_MATRIX_SOURCE_CONTRACT.csv"
OPEN_TAIL_4334 = SOURCE_DIR / "P8_Y5_R2FR_4334_OPEN_TAIL_VECTOR_BASIS.csv"
PPN_ZERO_4335 = SOURCE_DIR / "P8_Y5_R2FR_4335_STANDARD_ZERO_PIPPN_ROW.csv"
J2_4483 = SOURCE_DIR / "P8_Y5_R2FR_4483_PI_J2_METRIC_OWNER_CLAUSES.csv"
EM_POYNTING_4312 = SOURCE_DIR / "P8_Y5_R2FR_4312_EM_POYNTING_CANCELLATION_THEOREM.csv"
EM_WARD_4313 = SOURCE_DIR / "P8_Y5_R2FR_4313_EM_WARD_CURRENT_THEOREM.csv"
EM_NOFLUX_4314 = SOURCE_DIR / "P8_Y5_R2FR_4314_RADIATIVE_NOFLUX_THEOREM.csv"
EM_HODGE_4315 = SOURCE_DIR / "P8_Y5_R2FR_4315_SAME_HODGE_THEOREM.csv"
TAU_LOCK_4325 = SOURCE_DIR / "P8_Y5_R2FR_4325_TAU_LOCK_AUDIT.csv"
EM_HODGE_ZERO_4329 = SOURCE_DIR / "P8_Y5_R2FR_4329_EM_HODGE_ZERO_ROWS.csv"

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


def csv_by_key(path: Path, key: str) -> Dict[str, Dict[str, str]]:
    if not path.exists():
        return {}
    return {row[key]: row for row in read_csv(path) if key in row}


def semicolon_paths(paths: Iterable[Path]) -> str:
    return "; ".join(str(path) for path in paths)


def source_rows() -> List[Dict[str, object]]:
    specs = [
        ("SRC4498_00_formal513", "4497 formal theorem handoff", FORMAL_513, "P4497_4_conditional_kernel_theorem", "conditional kernel theorem row"),
        ("SRC4498_01_post4497", "4497 post mirror", POST_4497, "A4497_7_EM_Poynting", "EM/Poynting arena included in shell transfer matrix"),
        ("SRC4498_02_arena4497", "4497 arena transfer matrix", ARENA_4497, "A4497_0_PPN_bare", "PPN numeric factor and other arena blockers"),
        ("SRC4498_03_comparator4496", "4496 shell comparator", COMPARATOR_4496, "DSP4496_COMP4284_0_bare", "real PPN shell projection factor"),
        ("SRC4498_04_projection4334", "4334 projection source contract", CONTRACT_4334, "PI4334_1_PPN", "arena projection contract skeleton"),
        ("SRC4498_05_open_tail4334", "4334 open-tail basis", OPEN_TAIL_4334, "T4334_0_Xi", "tail vector basis imported into shell vector"),
        ("SRC4498_06_ppnzero4335", "4335 standard PPN zero row", PPN_ZERO_4335, "PIPPN4335_0_standard_zero_gamma_beta", "closed standard branch PPN zero comparator"),
        ("SRC4498_07_j24483", "4483 J2 owner clauses", J2_4483, "MOC4483_1_public_metric_projection", "J2 transfer operator source clauses"),
        ("SRC4498_08_em4312", "4312 EM/Poynting theorem", EM_POYNTING_4312, "EC4312_1_poynting_identity", "Poynting is Hilbert EM flux, not extra source"),
        ("SRC4498_09_emward4313", "4313 EM Ward theorem", EM_WARD_4313, "WT4313_3_exchange_identity", "same-current Ward exchange cancellation contract"),
        ("SRC4498_10_emnoflux4314", "4314 radiative no-flux theorem", EM_NOFLUX_4314, "NF4314_1_power_definition", "Poynting boundary flux row"),
        ("SRC4498_11_emhodge4315", "4315 same-Hodge theorem", EM_HODGE_4315, "HT4315_0_unique_hodge", "Hodge uniqueness and constitutive countermodel"),
        ("SRC4498_12_tau4325", "4325 tau lock audit", TAU_LOCK_4325, "AUD4325_0_single_tau", "clock/orbit/source tau lock"),
        ("SRC4498_13_emzero4329", "4329 EM Hodge zero rows", EM_HODGE_ZERO_4329, "ZERO4329_0_Delta_Hodge_EM", "EM zero rows imported as conditional branch"),
        ("SRC4498_14_script4497", "4497 generator", SCRIPT_4497, 'CHECKPOINT = "4497"', "reproducible predecessor generator"),
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


def parent_signature_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "PS4498_0_q_descent",
            "parent_clause": "public response descends through parent quotient q",
            "needed_signature": "O_A[Phi] = Obar_A(q(Phi)) + B_A[Phi] for each local arena A through the required weak-field order",
            "current_status": "CONDITIONAL_TEMPLATE_PRESENT",
            "source_basis": str(FORMAL_513),
            "unsigned_residue": "generic DeltaKTF shell response has not been shown to be q-basic for all arenas",
            "if_signed": "bulk arena response sees only q(Phi), not representative shell data",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PS4498_1_shell_verticality",
            "parent_clause": "DeltaKTF transition shell is vertical",
            "needed_signature": "Dq[DeltaPhi_shell] = 0",
            "current_status": "UNSIGNED",
            "source_basis": str(ARENA_4497),
            "unsigned_residue": "no parent-owned kernel membership theorem for DeltaKTF_shell",
            "if_signed": "all Pi_A Dq_shell terms vanish simultaneously",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PS4498_2_boundary_silence",
            "parent_clause": "boundary/exact-current shell silence",
            "needed_signature": "delta_shell B_A = 0 for local collar/readout boundary terms in PPN, J2, clock, orbital, R10 and EM",
            "current_status": "UNSIGNED_GENERICALLY",
            "source_basis": str(FORMAL_513),
            "unsigned_residue": "support-separated collar zero is not generic transition-shell zero",
            "if_signed": "no integration-by-parts shell edge leaks into observables",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PS4498_3_no_rep_coefficients",
            "parent_clause": "no representative shell coefficients",
            "needed_signature": "C_DeltaKTF, epsilon_shell, Weyl/disformal/source-shadow and arena-tau coefficients are absent or pure gauge before readout",
            "current_status": "UNSIGNED",
            "source_basis": str(CONTRACT_4334),
            "unsigned_residue": "open-tail vector still contains projection, tau, EM and source-label slots",
            "if_signed": "explicit tiny projection factors no longer need phenomenological sourcing",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PS4498_4_owner_kernel_verdict",
            "parent_clause": "owner-kernel route",
            "needed_signature": "PS4498_0 through PS4498_3 close together",
            "current_status": "NOT_PARENT_SIGNED",
            "source_basis": semicolon_paths([FORMAL_513, CONTRACT_4334, J2_4483, EM_POYNTING_4312, TAU_LOCK_4325]),
            "unsigned_residue": "use arena operator contracts until parent signature exists",
            "if_signed": "T_shell=0 and all arena residuals vanish without tuning",
            "valid_for_claim": False,
        },
    ]


def tail_basis_rows() -> List[Dict[str, object]]:
    return [
        {
            "tail_id": "T4498_0_Dq_shell",
            "symbol": "Dq_shell",
            "definition": "Dq[DeltaPhi_shell]",
            "operator_role": "bulk quotient-visibility defect",
            "imported_basis": "K4497_1_shell_verticality; T4334_3_projection",
            "zero_condition": "DeltaPhi_shell in ker(Dq)",
            "bound_condition": "arena-specific |Pi_A Dq_shell| <= allowance_A",
            "units": "arena dependent after projection",
            "valid_for_claim": False,
        },
        {
            "tail_id": "T4498_1_boundary_shell",
            "symbol": "B_boundary_shell",
            "definition": "delta_shell B_A plus exact-current collar flux",
            "operator_role": "boundary/local projection re-entry",
            "imported_basis": "K4497_2_boundary_silence; T4334_6_domain",
            "zero_condition": "support and no-flux selector signed for the generic shell",
            "bound_condition": "boundary flux translated into each arena residual",
            "units": "arena dependent boundary flux",
            "valid_for_claim": False,
        },
        {
            "tail_id": "T4498_2_rep_coeff_shell",
            "symbol": "C_rep_shell",
            "definition": "representative-level Weyl/disformal/source-shadow coefficient multiplying shell response",
            "operator_role": "forbidden-if-parent-owned coefficient slot",
            "imported_basis": "K4497_3_no_representative_coefficients; T4334_0_Xi; T4334_2_coeff",
            "zero_condition": "parent action has no representative coefficient after quotient selection",
            "bound_condition": "|C_rep_shell| below the tightest arena projection factor",
            "units": "dimensionless envelope unless tied to a source scale",
            "valid_for_claim": False,
        },
        {
            "tail_id": "T4498_3_metric_green_shell",
            "symbol": "R_metric_shell",
            "definition": "local metric Green response to the shell after public projection",
            "operator_role": "PPN/Newton/J2 metric response carrier",
            "imported_basis": "PI4334_1_PPN; PIPPN4335_0_standard_zero_gamma_beta",
            "zero_condition": "standard closed branch T_open=0 or shell kernel theorem",
            "bound_condition": "epsilon_shell_PPN <= imported 4496 projection factors",
            "units": "dimensionless PPN residual",
            "valid_for_claim": False,
        },
        {
            "tail_id": "T4498_4_J2_shell",
            "symbol": "R_J2_shell",
            "definition": "l=2 public metric projection of finite shell/STF response",
            "operator_role": "J2/quadrupole orbital transfer carrier",
            "imported_basis": "MOC4483_1_public_metric_projection",
            "zero_condition": "parent l=2 operator and public projection kernel signed",
            "bound_condition": "|Pi_J2_metric T_source G_ext_l2_surface| below J2/orbital allowance",
            "units": "dimensionless quadrupole or mapped orbital residual",
            "valid_for_claim": False,
        },
        {
            "tail_id": "T4498_5_tau_shell",
            "symbol": "R_tau_shell",
            "definition": "clock/orbit/source tau split induced by shell or representative choice",
            "operator_role": "clock, redshift and orbital timing carrier",
            "imported_basis": "AUD4325_0_single_tau; T4334_5_tau",
            "zero_condition": "single parent-owned time generator and pre-fit reference selection",
            "bound_condition": "species/time-transfer sensitivity matrix times tau residual",
            "units": "clock/orbit dependent",
            "valid_for_claim": False,
        },
        {
            "tail_id": "T4498_6_R10_shell",
            "symbol": "R_R10_shell",
            "definition": "short-range alpha(lambda) shell residual",
            "operator_role": "R10/fifth-force transfer carrier",
            "imported_basis": "PI4334_0_R10",
            "zero_condition": "same source coupling and shell kernel theorem",
            "bound_condition": "|K_X Qbar_XH(lambda) P_A qbarXT_vec + tail terms| <= alpha_bound(lambda)",
            "units": "dimensionless alpha(lambda)",
            "valid_for_claim": False,
        },
        {
            "tail_id": "T4498_7_EM_shell",
            "symbol": "R_EM_shell",
            "definition": "EM/Hodge/Poynting/Ward residual sourced by shell or readout mismatch",
            "operator_role": "EM stress and Poynting no-double-count carrier",
            "imported_basis": "EC4312_1_poynting_identity; WT4313_3_exchange_identity; ZERO4329_0_Delta_Hodge_EM",
            "zero_condition": "same Hodge owner, same current, no extra Poynting source, no radiative collar flux",
            "bound_condition": "Delta_Ward + Delta_Hodge + Phi_rad + constitutive tails bounded as explicit residual",
            "units": "stress/flux or dimensionless after arena normalization",
            "valid_for_claim": False,
        },
    ]


def numeric_ppn_rows() -> List[Dict[str, object]]:
    comparator = csv_by_key(COMPARATOR_4496, "source_comparator_id")
    mapping = [
        ("PPN4498_0_bare", "COMP4284_0_bare", "epsilon_shell_PPN_bare", "bare transition shell"),
        ("PPN4498_1_U2", "COMP4284_1_U2", "epsilon_shell_PPN_U2", "U_B^2 transition shell"),
        ("PPN4498_2_wide", "COMP4284_2_wide", "epsilon_shell_PPN_wide", "wide transition shell width 100"),
    ]
    rows: List[Dict[str, object]] = []
    for row_id, source_id, epsilon, note in mapping:
        source = comparator.get(source_id, {})
        ratio = source.get("PPN_ratio_to_budget", "")
        required = source.get("required_projection_factor_to_pass", "")
        rows.append(
            {
                "ppn_row_id": row_id,
                "epsilon_symbol": epsilon,
                "source_comparator_id": source_id,
                "scenario": source.get("scenario", note),
                "raw_shell_response_S_PPN": source.get("S_PPN", ""),
                "ratio_to_ppn_budget": ratio,
                "required_projection_factor_to_pass": required,
                "inequality": f"{epsilon} <= {required}" if required else f"{epsilon} <= MISSING",
                "source_path": str(COMPARATOR_4496),
                "status": "NUMERIC_OPERATOR_REQUIREMENT_IMPORTED_NONCLAIM",
                "valid_for_claim": False,
            }
        )
    return rows


def operator_contract_rows(ppn_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    bare_bound = next((row.get("required_projection_factor_to_pass", "") for row in ppn_rows if row.get("ppn_row_id") == "PPN4498_0_bare"), "")
    return [
        {
            "operator_id": "OP4498_0_universal_law",
            "arena": "all local arenas",
            "operator_statement": "T_shell=(Dq_shell,B_boundary_shell,C_rep_shell,R_metric_shell,R_J2_shell,R_tau_shell,R_R10_shell,R_EM_shell); R_A=Pi_A T_shell",
            "zero_branch": "if parent signs Dq_shell=0, B_boundary_shell=0, C_rep_shell=0 and same-owner arena clauses, then R_A=0 for every A",
            "bound_branch": "otherwise require ||Pi_A T_shell|| <= allowance_A with source-owned units",
            "source_paths": semicolon_paths([FORMAL_513, OPEN_TAIL_4334, CONTRACT_4334]),
            "numeric_ready": False,
            "source_backed": True,
            "status": "DERIVED_OPERATOR_NORMAL_FORM_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "operator_id": "OP4498_1_PPN",
            "arena": "PPN/local metric",
            "operator_statement": "R_PPN=Pi_PPN T_shell; closed standard branch gives R_PPN=0; shell branch requires explicit epsilon_shell_PPN",
            "zero_branch": "PIPPN4335_0 standard zero or 4497 kernel theorem parent-signed",
            "bound_branch": f"epsilon_shell_PPN_bare <= {bare_bound}; plus U2 and wide-shell rows in P8_Y5_R2FR_4498_NUMERIC_PPN_OPERATOR_ROWS.csv",
            "source_paths": semicolon_paths([ARENA_4497, COMPARATOR_4496, CONTRACT_4334, PPN_ZERO_4335]),
            "numeric_ready": True,
            "source_backed": True,
            "status": "NUMERIC_PPN_REQUIREMENTS_FILLED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "operator_id": "OP4498_2_J2",
            "arena": "J2/quadrupole orbital precession",
            "operator_statement": "R_J2=Pi_J2_metric T_source G_ext_l2_surface + Pi_J2_metric R_J2_shell",
            "zero_branch": "parent exterior l=2 operator, public metric projection kernel, source-domain transfer and boundary silence all signed",
            "bound_branch": "source Pi_J2_metric, T_source and residual l2 envelopes before comparing to J2/orbital allowances",
            "source_paths": semicolon_paths([J2_4483, CONTRACT_4334]),
            "numeric_ready": False,
            "source_backed": True,
            "status": "SOURCE_NORMALIZED_FIRST_NON_PPN_TARGET",
            "valid_for_claim": False,
        },
        {
            "operator_id": "OP4498_3_clock",
            "arena": "clock/redshift/fine-structure",
            "operator_statement": "R_clock=Pi_clock T_shell with species sensitivities to alpha_EM, mass ratios, tau reference and EM collar tails",
            "zero_branch": "single tau/source/clock/orbit/readout generator and same coframe branch",
            "bound_branch": "source species sensitivity matrix and tau/readout transfer before scoring clock residuals",
            "source_paths": semicolon_paths([TAU_LOCK_4325, CONTRACT_4334]),
            "numeric_ready": False,
            "source_backed": True,
            "status": "SOURCE_NORMALIZED_CLOCK_CONTRACT_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "operator_id": "OP4498_4_orbital",
            "arena": "orbital dynamics/ephemeris",
            "operator_statement": "R_orbital=Pi_orbital T_shell with GM convention, orbital frame, range/time transfer and source support",
            "zero_branch": "same tau and source-support branch plus metric shell kernel",
            "bound_branch": "source GM convention/orbital frame/range-time transfer and source-support map",
            "source_paths": semicolon_paths([TAU_LOCK_4325, CONTRACT_4334, J2_4483]),
            "numeric_ready": False,
            "source_backed": True,
            "status": "SOURCE_NORMALIZED_ORBITAL_CONTRACT_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "operator_id": "OP4498_5_R10",
            "arena": "R10/fifth-force alpha(lambda)",
            "operator_statement": "R_R10(lambda)=Pi_R10(lambda) T_shell; alpha_pred(lambda)=K_X Qbar_XH(lambda) P_A qbarXT_vec plus shell tails",
            "zero_branch": "source coupling and shell kernel zero leave no fifth-force alpha row",
            "bound_branch": "source K_X, Qbar_XH(lambda), P_A qbarXT_vec, lambda_X and alpha_bound(lambda)",
            "source_paths": semicolon_paths([CONTRACT_4334]),
            "numeric_ready": False,
            "source_backed": True,
            "status": "SOURCE_NORMALIZED_R10_CONTRACT_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "operator_id": "OP4498_6_EM_Poynting",
            "arena": "EM stress/Poynting",
            "operator_statement": "R_EM=Pi_EM T_shell, with Poynting counted as Hilbert EM flux S_i=-T_EM(n,e_i), not a standalone force source",
            "zero_branch": "same Hodge owner, same current Ward exchange, c_Poynt_extra=0, no XF2 and no radiative collar flux",
            "bound_branch": "if any clause fails, bound Delta_Ward + Delta_Hodge + Phi_rad + constitutive/readout tails explicitly",
            "source_paths": semicolon_paths([EM_POYNTING_4312, EM_WARD_4313, EM_NOFLUX_4314, EM_HODGE_4315, EM_HODGE_ZERO_4329]),
            "numeric_ready": False,
            "source_backed": True,
            "status": "EM_NO_DOUBLE_COUNT_OPERATOR_CONTRACT_DERIVED_NONCLAIM",
            "valid_for_claim": False,
        },
    ]


def cross_arena_gate_rows(operator_rows: Sequence[Mapping[str, object]], ppn_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    non_ppn_blockers = [row["operator_id"] for row in operator_rows if row.get("operator_id") not in {"OP4498_1_PPN"} and str(row.get("numeric_ready")).lower() != "true"]
    return [
        {
            "gate_id": "G4498_0_parent_kernel_signed",
            "gate": "parent signs Dq_shell=0, boundary silence and no representative coefficients",
            "passed": False,
            "evidence": "parent signature audit remains unsigned",
            "blocking_rows": "PS4498_1_shell_verticality;PS4498_2_boundary_silence;PS4498_3_no_rep_coefficients",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G4498_1_ppn_operator_numeric",
            "gate": "PPN shell projection requirements are numeric and source-backed",
            "passed": len(ppn_rows) == 3 and all(float(row["required_projection_factor_to_pass"]) < 1.0e-16 for row in ppn_rows),
            "evidence": "4496 comparator rows imported into 4498 numeric PPN operator rows",
            "blocking_rows": "",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G4498_2_all_arena_operators_source_normalized",
            "gate": "J2, clocks, orbital, R10 and EM have source-backed contracts",
            "passed": all(str(row.get("source_backed")).lower() == "true" for row in operator_rows),
            "evidence": "operator source contract rows include source paths for every local arena",
            "blocking_rows": "numeric matrices still absent for non-PPN arenas",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G4498_3_all_arena_operators_numeric",
            "gate": "all local arenas have numeric transfer matrices or parent zero signatures",
            "passed": False,
            "evidence": "PPN is numeric; other arenas are contract-ready but not numeric",
            "blocking_rows": ";".join(non_ppn_blockers),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G4498_4_em_poynting_double_count_guard",
            "gate": "Poynting vector is treated as EM Hilbert flux rather than extra source",
            "passed": True,
            "evidence": "4312/4313/4314/4315/4329 source rows define same-Hodge, same-current and no-flux branches",
            "blocking_rows": "EM zero branch still conditional; not a local-GR claim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G4498_5_local_GR_promotion",
            "gate": "local GR/Newton/PPN/R10 promotion",
            "passed": False,
            "evidence": "parent kernel unsigned and non-PPN numeric transfer matrices absent",
            "blocking_rows": "G4498_0_parent_kernel_signed;G4498_3_all_arena_operators_numeric",
            "claim_allowed": False,
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
            "what_moved_forward": "4498 replaces the loose arena fallback with a single shell-tail vector T_shell and source-backed operators R_A=Pi_A T_shell",
            "what_is_now_filled": "PPN numeric projection requirements are imported exactly from 4496, including bare, U_B^2 and wide-shell factors",
            "what_remains_blocked": "parent shell-kernel signature is unsigned and J2/clock/orbital/R10/EM transfer matrices are source-normalized but not numeric",
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
            "operator_normal_form": "T_shell vector plus R_A=Pi_A T_shell",
            "ppn_numeric_ready": True,
            "non_ppn_arenas_source_backed": True,
            "non_ppn_arenas_numeric_ready": False,
            "parent_kernel_signed": False,
            "local_GR_claim": False,
            "sharpest_open_clause": "source the J2 shell transfer row first or parent-sign the universal kernel theorem",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": STAMP,
        }
    ]


def next_rows() -> List[Dict[str, object]]:
    return [
        {
            "next_id": "NT4498_0",
            "target": NEXT_TARGET,
            "preferred_route": "try to source the J2 shell transfer operator because it is the first non-PPN public metric arena and shares the weak-field l=2 machinery",
            "fallback_route": "if J2 cannot be sourced, return to parent kernel signature and prove Dq_shell=0 plus boundary silence universally",
            "do_not_do": "call local GR closed from the PPN numeric factors alone",
            "valid_for_claim": False,
        }
    ]


def body(
    sources: Sequence[Mapping[str, object]],
    parent_rows: Sequence[Mapping[str, object]],
    tail_rows: Sequence[Mapping[str, object]],
    operator_rows: Sequence[Mapping[str, object]],
    ppn_rows: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    decisions: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
) -> str:
    return f"""# 4498 - Shell Projection Arena Operator Source Fill Or Owner Kernel Parent Signature

Marker: `{MARKER}`  
Claim: `{CLAIM_ID}`  
Decision: `{DECISION}`  
Generated: `{STAMP}`

## Result

4498 turns the 4497 fallback into an actual operator contract. The shell issue is now written as one shared tail vector

`T_shell = (Dq_shell, B_boundary_shell, C_rep_shell, R_metric_shell, R_J2_shell, R_tau_shell, R_R10_shell, R_EM_shell)`.

Every local arena is forced to use the same law:

`R_A = Pi_A T_shell`.

That matters because it removes the mush. Either the parent signs the universal zero route (`T_shell=0`), or each arena must carry a sourced transfer operator and an explicit bound. PPN is now numeric; the other arenas are source-normalized but not yet numeric.

## Derived Contract

From 4497,

`delta_shell O_A = D Obar_A[Dq(DeltaPhi_shell)] + delta_shell B_A`.

4498 packages every possible failure of that zero into `T_shell`. Thus:

1. If `Dq_shell=0`, `B_boundary_shell=0`, `C_rep_shell=0`, and the arena same-owner clauses hold, then `R_A=0` for PPN, J2, clocks, orbital, R10 and EM/Poynting simultaneously.
2. If any clause is unsigned, the theory must supply `Pi_A` and prove `||Pi_A T_shell|| <= allowance_A`.
3. Poynting is not allowed to become a secret extra force. It is EM Hilbert flux unless a sourced residual row explicitly opens a boundary/radiative branch.

## Parent Signature Audit

{table(parent_rows)}

## Shell Tail Vector

{table(tail_rows)}

## Arena Operator Source Contracts

{table(operator_rows)}

## Numeric PPN Operator Rows

{table(ppn_rows)}

## Cross-Arena Gates

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
                "local_gr_newton_r10_shell_operator",
                "4498 derives the common shell-tail operator normal form T_shell and R_A=Pi_A T_shell, imports numeric PPN shell projection requirements, and source-normalizes J2, clock, orbital, R10 and EM/Poynting operator contracts without promoting a local-GR claim.",
                "4498 source register, parent signature audit, shell-tail vector basis, arena operator contracts, numeric PPN rows, cross-arena gates, status and validation.",
                "private_operator_contract_nonclaim",
                NEXT_TARGET,
                "treating PPN numeric projection factors or EM/Poynting no-double-count rows as a full local-GR closure.",
                "local_gr_newton_r10_shell_operator",
                str(FORMAL_PATH),
                NEXT_TARGET,
                "source the J2 transfer operator first or parent-sign the universal shell kernel theorem",
            ]
        )


def append_section_once(path: Path, marker: str, title: str, summary: str) -> None:
    current = text(path)
    if marker in current:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        handle.write(f"\n\n## {title}\n\nMarker: `{marker}`  \n{summary}\n")


def parse_source_paths(value: str) -> List[Path]:
    return [Path(part.strip()) for part in value.split(";") if part.strip()]


def validate(
    sources: Sequence[Mapping[str, object]],
    parent_rows: Sequence[Mapping[str, object]],
    tail_rows: Sequence[Mapping[str, object]],
    operator_rows: Sequence[Mapping[str, object]],
    ppn_rows: Sequence[Mapping[str, object]],
    gates: Sequence[Mapping[str, object]],
    statuses: Sequence[Mapping[str, object]],
    next_targets: Sequence[Mapping[str, object]],
    csv_paths: Sequence[Path],
) -> List[Dict[str, object]]:
    validations: List[Dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validations.append({"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False})

    add("VAL4498_0_sources_exist_and_needles_found", all(row.get("exists") is True and row.get("needle_found") is True for row in sources), "all source-register paths exist and needles are found")
    add("VAL4498_1_parent_kernel_unsigned", any(str(row.get("current_status")).startswith("UNSIGNED") for row in parent_rows) and any(row.get("audit_id") == "PS4498_4_owner_kernel_verdict" and row.get("current_status") == "NOT_PARENT_SIGNED" for row in parent_rows), "parent shell-kernel is not signed")
    add("VAL4498_2_tail_basis_complete", len(tail_rows) == 8 and {row["tail_id"] for row in tail_rows} == {f"T4498_{index}_{name}" for index, name in enumerate(["Dq_shell", "boundary_shell", "rep_coeff_shell", "metric_green_shell", "J2_shell", "tau_shell", "R10_shell", "EM_shell"])}, "T_shell has eight named components")
    add("VAL4498_3_operator_normal_form_present", any(row.get("operator_id") == "OP4498_0_universal_law" and "R_A=Pi_A T_shell" in str(row.get("operator_statement")) for row in operator_rows), "common operator law present")
    add("VAL4498_4_ppn_numeric_rows_ready", len(ppn_rows) == 3 and all(float(row["required_projection_factor_to_pass"]) < 1.0e-16 for row in ppn_rows), "three numeric PPN shell projection factors imported")
    add("VAL4498_5_non_ppn_contracts_source_backed", all(str(row.get("source_backed")).lower() == "true" for row in operator_rows) and any(row.get("operator_id") == "OP4498_6_EM_Poynting" for row in operator_rows), "all operator contracts cite source-backed rows including EM/Poynting")
    source_paths_ok = True
    missing_paths: List[str] = []
    for row in operator_rows:
        for path in parse_source_paths(str(row.get("source_paths", ""))):
            if not path.exists():
                source_paths_ok = False
                missing_paths.append(str(path))
    add("VAL4498_6_operator_source_paths_exist", source_paths_ok, "missing: " + "; ".join(missing_paths) if missing_paths else "all operator source paths exist")
    add("VAL4498_7_non_ppn_numeric_not_ready", any(row.get("operator_id") != "OP4498_1_PPN" and str(row.get("numeric_ready")).lower() == "false" for row in operator_rows), "non-PPN arenas remain numeric-blocked")
    add("VAL4498_8_claim_gates_block_promotion", all(str(row.get("claim_allowed")).lower() == "false" for row in gates) and any(row.get("gate_id") == "G4498_5_local_GR_promotion" and str(row.get("passed")).lower() == "false" for row in gates), "claim gates block local-GR promotion")
    add("VAL4498_9_em_double_count_guard_present", any(row.get("gate_id") == "G4498_4_em_poynting_double_count_guard" and str(row.get("passed")).lower() == "true" for row in gates), "EM/Poynting double-count guard present")
    add("VAL4498_10_status_local_GR_false", bool(statuses) and str(statuses[0].get("local_GR_claim")).lower() == "false", "local_GR_claim remains false")
    add("VAL4498_11_next_target_selected", bool(next_targets) and next_targets[0].get("target") == NEXT_TARGET, NEXT_TARGET)
    all_rows = [*sources, *parent_rows, *tail_rows, *operator_rows, *ppn_rows, *gates, *statuses, *next_targets]
    add("VAL4498_12_all_generated_rows_nonclaim", all(str(row.get("valid_for_claim")).lower() == "false" for row in all_rows), "all generated rows are private/nonclaim")
    csv_ok = True
    csv_detail: List[str] = []
    for csv_path in csv_paths:
        try:
            parsed_rows = read_csv(csv_path)
            csv_detail.append(f"{csv_path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_ok = False
            csv_detail.append(f"{csv_path.name}:ERROR:{exc}")
    add("VAL4498_13_csvs_parse", csv_ok, "; ".join(csv_detail))
    add("VAL4498_14_docs_written", FORMAL_PATH.exists() and DOC_PATH.exists(), "formal and post checkpoint docs exist")
    add("VAL4498_15_claim_register_updated", any(row.get("claim_id") == CLAIM_ID for row in read_csv(CLAIMS_PATH)), "claims register contains L-340")
    add("VAL4498_16_spine_and_packet_updated", MARKER in text(SPINE_PATH) and PACKET_MARKER in text(PACKET_PATH), "spine and packet contain 4498 markers")
    add("VAL4498_17_pycache_removed", not (SCRIPT_DIR / "__pycache__").exists(), "scripts __pycache__ absent after generation")
    return validations


def main() -> None:
    sources = source_rows()
    parent_rows = parent_signature_rows()
    tail_rows = tail_basis_rows()
    ppn_rows = numeric_ppn_rows()
    operator_rows = operator_contract_rows(ppn_rows)
    gates = cross_arena_gate_rows(operator_rows, ppn_rows)
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PARENT_AUDIT_CSV, parent_rows)
    write_csv(TAIL_BASIS_CSV, tail_rows)
    write_csv(OPERATOR_CONTRACT_CSV, operator_rows)
    write_csv(NUMERIC_PPN_CSV, ppn_rows)
    write_csv(CROSS_ARENA_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, next_targets)

    doc = body(sources, parent_rows, tail_rows, operator_rows, ppn_rows, gates, decisions, statuses, next_targets)
    write_text(FORMAL_PATH, doc)
    write_text(DOC_PATH, doc)
    append_claim_once()

    append_section_once(
        SPINE_PATH,
        MARKER,
        "4498 Shell Projection Arena Operator Source Fill Or Owner Kernel Parent Signature",
        "4498 replaces the loose arena fallback with a common shell-tail vector T_shell and operator law R_A=Pi_A T_shell. PPN projection requirements are now numeric from 4496; J2, clock, orbital, R10 and EM/Poynting lanes are source-normalized but remain nonclaim until numeric transfer matrices or a parent shell-kernel signature exist.",
    )
    append_section_once(
        PACKET_PATH,
        PACKET_MARKER,
        "4498 Packet Integration",
        "The private local packet now has a unified shell operator contract. The local-GR route is cleaner: either prove the universal owner-kernel T_shell=0, or source the arena maps Pi_A one by one. The next best non-PPN target is J2 because it shares the weak-field public metric machinery.",
    )

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    csv_paths = [
        SOURCE_REGISTER,
        PARENT_AUDIT_CSV,
        TAIL_BASIS_CSV,
        OPERATOR_CONTRACT_CSV,
        NUMERIC_PPN_CSV,
        CROSS_ARENA_GATES_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    validations = validate(sources, parent_rows, tail_rows, operator_rows, ppn_rows, gates, statuses, next_targets, csv_paths)
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
