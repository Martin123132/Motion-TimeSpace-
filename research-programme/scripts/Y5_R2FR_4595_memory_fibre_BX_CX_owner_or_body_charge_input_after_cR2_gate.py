from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4595"
CLAIM_ID = "L-437"
BRANCH_ID = "MTS_R2FR_Y5_MEMORY_FIBRE_BC_AFTER_CR2_4595"
MARKER = "PPC4161_MEMORY_FIBRE_BX_CX_OWNER_OR_BODY_CHARGE_INPUT_AFTER_CR2_GATE_4595"
PACKET_MARKER = "PPC4161_PACKET_MEMORY_FIBRE_BX_CX_OWNER_OR_BODY_CHARGE_INPUT_AFTER_CR2_GATE_4595"
DECISION = "MEMORY_FIBRE_BC_ZERO_SWITCH_AND_BODY_CHARGE_BOUND_INTEGRATED_AFTER_CR2_NONCLAIM"
NEXT_TARGET = "4596-Y5-R2FR-memory-fibre-source-functor-signature-or-first-body-charge-coefficient-row.md"

DOC_PATH = POST / "4595-Y5-R2FR-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md"
FORMAL_PATH = FORMAL / "611-PPC4161-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4595_SOURCE_REGISTER.csv"
ZERO_SWITCH_CSV = SOURCE_DIR / "P8_Y5_R2FR_4595_OWNER_ZERO_SWITCH.csv"
MEMORY_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4595_MEMORY_BODY_CHARGE_BOUND.csv"
FIBRE_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4595_FIBRE_BODY_CHARGE_BOUND.csv"
BMEM_INSERTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4595_BMEM_EFF_INSERTION.csv"
FINITE_SCHEMA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4595_FINITE_INPUT_SCHEMA.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4595_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4595_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4595_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4595_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4595_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4595_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4595_VALIDATION.csv"

DOC_4594 = POST / "4594-Y5-R2FR-cR2-MR-parent-scale-gap-or-full-finite-range-bound-after-torsion.md"
FORMAL_610 = FORMAL / "610-PPC4161-cR2-MR-parent-scale-gap-or-full-finite-range-bound-after-torsion.md"
CSV_4594_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4594_NEXT_TARGET.csv"
CSV_4594_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4594_CR2_ZERO_BOUND_THEOREM.csv"
CSV_4594_PROFILE = SOURCE_DIR / "P8_Y5_R2FR_4594_FINITE_RANGE_PROFILE_LAW.csv"
DOC_4506 = POST / "4506-Y5-R2FR-memory-fibre-BX-CX-owner-or-body-charge-input-row.md"
FORMAL_522 = FORMAL / "522-PPC4161-memory-fibre-BX-CX-owner-or-body-charge-input-row.md"
CSV_4506_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4506_OWNER_ROUTE_AUDIT.csv"
CSV_4506_OPERATOR = SOURCE_DIR / "P8_Y5_R2FR_4506_MEMORY_OPERATOR_SIGNATURE.csv"
CSV_4506_EXTREMUM = SOURCE_DIR / "P8_Y5_R2FR_4506_MEMORY_EXTREMUM_TEST.csv"
CSV_4506_FIBRE = SOURCE_DIR / "P8_Y5_R2FR_4506_FIBRE_OWNER_GATE.csv"
CSV_4506_BODY = SOURCE_DIR / "P8_Y5_R2FR_4506_BODY_CHARGE_INPUT_ROW.csv"
CSV_4506_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4506_STATUS.csv"
DOC_4514 = POST / "4514-Y5-R2FR-BWeyl-vector-insertion-into-Bmem-eff-or-body-charge-bound.md"
FORMAL_530 = FORMAL / "530-PPC4161-BWeyl-vector-insertion-into-Bmem-eff-or-body-charge-bound.md"
CSV_4514_BMEM = SOURCE_DIR / "P8_Y5_R2FR_4514_BMEM_EFFECTIVE_COMPONENT_VECTOR.csv"
CSV_4514_BODY = SOURCE_DIR / "P8_Y5_R2FR_4514_BODY_CHARGE_INSERTION_BOUND.csv"
CSV_4514_TAIL = SOURCE_DIR / "P8_Y5_R2FR_4514_REMAINING_SOURCE_TAIL_LEDGER.csv"
CSV_4514_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4514_STATUS.csv"
DOC_4515 = POST / "4515-Y5-R2FR-Y5-Y6-source-trace-tail-or-Cmem-Jmem-source-coupling-vector.md"
CSV_4515_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4515_SOURCE_FUNCTOR_DESCENT_THEOREM.csv"
CSV_4515_Y5 = SOURCE_DIR / "P8_Y5_R2FR_4515_Y5_SOURCE_TRACE_VECTOR.csv"
CSV_4515_Y6 = SOURCE_DIR / "P8_Y5_R2FR_4515_Y6_EXTRA_STRESS_TRACE_VECTOR.csv"
CSV_4515_CMEM = SOURCE_DIR / "P8_Y5_R2FR_4515_CMEM_JMEM_COUPLING_VECTOR.csv"
CSV_4515_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4515_SOURCE_COUPLING_BOUND.csv"
CSV_4515_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4515_STATUS.csv"
DOC_4516 = POST / "4516-Y5-R2FR-source-functor-parent-signature-or-first-Y5-coefficient-fill.md"
CSV_4516_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4516_STATUS.csv"
CSV_4516_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4516_NEXT_TARGET.csv"
CLAIM_436_NEEDLE = "L-436"

PUBLIC_STAGE = Path("D:/Users/ollet/Desktop/Motion-TimeSpace-public-stage")
BACKUP_REPO = Path("D:/Users/ollet/Desktop/laptop-back-up-")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return line_number
    return 0


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = []
        for key in headers:
            value = str(row.get(key, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    write_text(path, text.rstrip() + "\n\n" + block.strip() + "\n")


def append_claim_once() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else [
        "claim_id",
        "domain",
        "claim",
        "current_evidence",
        "status",
        "next_test",
        "key_risk",
        "sector",
        "evidence",
        "next_action",
        "risk",
    ]
    claim_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4595 integrates the memory/fibre B_X,C_X,J_X,boundary owner problem after the c_R2/M_R gate: positive memory/fibre operators close only when the curvature, matter, direct-current and boundary charges vanish in the same parent branch, otherwise the branch must be scored by an explicit body-charge bound.",
        "current_evidence": "Generated owner zero switch, B_mem_eff insertion, memory and fibre body-charge bounds, finite-input schema, controls and validation.",
        "status": "memory_fibre_bc_zero_switch_and_body_charge_bound_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating a positive operator, exterior source-free equation, fitted G, or source-functor assumption as if it erased B_mem/C_mem/J_mem/Q_boundary or B_h/C_h/J_h/Q_boundary_h.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No public local-GR/R10/PPN claim until the zero switch is parent-signed or all finite body-charge coefficients and arena projections are sourced.",
    }
    rows.append({key: claim_row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def git_clean(path: Path) -> bool:
    if not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--short"], capture_output=True, text=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4595_00_4594_doc", DOC_4594, "memory/class scalar", "4594 selected memory/class scalar and finite-cell fibre source-charge owners as the next direct pressure row."),
        ("SRC4595_01_610_formal", FORMAL_610, "c_R2/M_R", "formal 610 cR2 finite-range gate."),
        ("SRC4595_02_4594_next", CSV_4594_NEXT, "4595-Y5-R2FR-memory-fibre-BX-CX-owner-or-body-charge-input-after-cR2-gate.md", "machine-readable handoff from 4594."),
        ("SRC4595_03_4594_theorem", CSV_4594_THEOREM, "TH4594_2_positive_hidden_obstruction", "positive hidden obstruction requiring B_X zero or bound."),
        ("SRC4595_04_4594_profile", CSV_4594_PROFILE, "FR4594_2_hidden_memory_fibre", "cR2 hidden memory/fibre profile row."),
        ("SRC4595_05_4506_doc", DOC_4506, "memory/fibre", "original memory/fibre owner checkpoint."),
        ("SRC4595_06_522_formal", FORMAL_522, "memory/fibre", "formal memory/fibre owner checkpoint."),
        ("SRC4595_07_4506_owner", CSV_4506_OWNER, "OR4506_0_memory_B", "memory B route audit."),
        ("SRC4595_08_4506_operator", CSV_4506_OPERATOR, "MOP4506_1", "positive memory operator signature."),
        ("SRC4595_09_4506_extremum", CSV_4506_EXTREMUM, "MEXT4506_1", "F0_prime zero condition for B_mem."),
        ("SRC4595_10_4506_fibre", CSV_4506_FIBRE, "FIB4506_0", "finite-cell fibre equation and source-charge form."),
        ("SRC4595_11_4506_body", CSV_4506_BODY, "BCIN4506_0_memory_density", "memory body-charge input row."),
        ("SRC4595_12_4506_status", CSV_4506_STATUS, "not_derived", "4506 remaining unsigned rows."),
        ("SRC4595_13_4514_doc", DOC_4514, "B_mem_eff", "B_Weyl vector inserted into B_mem_eff."),
        ("SRC4595_14_530_formal", FORMAL_530, "B_mem_eff", "formal Bmem effective vector source."),
        ("SRC4595_15_4514_bmem", CSV_4514_BMEM, "BMV4514_6_combined", "B_mem_eff component vector."),
        ("SRC4595_16_4514_body", CSV_4514_BODY, "BCB4514_3_amplitude", "A_mem source amplitude bound."),
        ("SRC4595_17_4514_tail", CSV_4514_TAIL, "STL4514_0_Y5_priority", "remaining source-tail ledger."),
        ("SRC4595_18_4514_status", CSV_4514_STATUS, "B_Weyl vector insertion", "4514 status."),
        ("SRC4595_19_4515_doc", DOC_4515, "EM/Poynting flow", "source functor and Poynting guard."),
        ("SRC4595_20_4515_theorem", CSV_4515_THEOREM, "SFT4515_1_single_source_functor_zero", "single source-functor conditional zero theorem."),
        ("SRC4595_21_4515_y5", CSV_4515_Y5, "Y5V4515_8_total", "Y5 source-normalization vector."),
        ("SRC4595_22_4515_y6", CSV_4515_Y6, "Y6V4515_4_total", "Y6 extra-stress vector."),
        ("SRC4595_23_4515_cmem", CSV_4515_CMEM, "SCV4515_0_Cmem", "C_mem/J_mem/Poynting vector."),
        ("SRC4595_24_4515_bound", CSV_4515_BOUND, "SB4515_3_nohair", "source-coupling no-hair row."),
        ("SRC4595_25_4515_status", CSV_4515_STATUS, "SOURCE_FUNCTOR_DESCENT_THEOREM", "4515 status."),
        ("SRC4595_26_4516_doc", DOC_4516, "stationary Hilbert", "first source-functor parent signature attempt."),
        ("SRC4595_27_4516_status", CSV_4516_STATUS, "LOCAL_STATIONARY_HILBERT_SOURCE_SUBTHEOREM", "4516 status."),
        ("SRC4595_28_4516_next", CSV_4516_NEXT, "4517-Y5-R2FR-domain-bulk-species-source-tail-or-coefficient-fill.md", "old next target after partial source-functor closure."),
        ("SRC4595_29_claim_436", CLAIMS_PATH, CLAIM_436_NEEDLE, "claim-register handoff from 4594."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": bool(line),
                "line_number": line,
                "role": role,
                "generated_utc": now,
                "valid_for_claim": False,
            }
        )
    return rows


def zero_switch_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "switch_id": "ZS4595_0_common_operator",
            "object": "X in {memory m, finite-cell fibre h}",
            "equation": "L_X delta_X = (-Z_X nabla^2 + M_X^2) delta_X = rho_X",
            "rho_definition": "rho_X = B_X R_obs + C_X T + J_X",
            "zero_switch": "Z_X>0; M_X^2>0; zero modes removed; B_X=C_X=J_X=Q_boundary_X=0 in the same parent branch => delta_X=0 and A_X=0",
            "finite_exit": "|A_X| <= [exp(R_body/lambda_X) int_body |rho_X| dV + |Q_boundary_X|]/(4*pi |Z_X|)",
            "status": "DERIVED_COMMON_ZERO_OR_BOUND_LAW",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "switch_id": "ZS4595_1_memory",
            "object": "memory/class scalar m",
            "equation": "L_mem delta_m = rho_mem; lambda_mem=sqrt(Z_mem/M2_mem)",
            "rho_definition": "rho_mem = B_mem_eff R_obs + C_mem T + J_mem",
            "zero_switch": "B_mem_eff=C_mem=J_mem=Q_boundary_mem=0 plus positive L_mem and zero-mode removal => A_mem=0",
            "finite_exit": "use absolute B_mem_eff/C_mem/J_mem/Q_boundary_mem source envelope; no cancellation credit",
            "status": "MEMORY_ZERO_SWITCH_DERIVED_CONDITIONAL_UNSIGNED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "switch_id": "ZS4595_2_fibre",
            "object": "finite-cell fibre h",
            "equation": "L_h delta_h = rho_h; lambda_h=sqrt(Z_h/M2_h)",
            "rho_definition": "rho_h = B_h R_obs + C_h T + J_h",
            "zero_switch": "B_h=C_h=J_h=Q_boundary_h=0 plus positive L_h and zero-mode removal => A_h=0",
            "finite_exit": "source Z_h,M2_h,B_h,C_h,J_h,Q_boundary_h and body profile; then compare induced alpha(lambda_h)",
            "status": "FIBRE_ZERO_SWITCH_DERIVED_CONDITIONAL_UNSIGNED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "switch_id": "ZS4595_3_no_smuggling",
            "object": "positive hidden/memory/fibre operator",
            "equation": "0.5 B^T L^-1 B = 0.5 ||L^-1/2 B||^2",
            "rho_definition": "nonzero B_X or nonzero C_X/J_X/boundary creates a body charge even with positive L_X",
            "zero_switch": "positive L_X is useful only after source silence is signed",
            "finite_exit": "0.5 ||B_X||^2/lambda_min(L_X) plus body-charge bound",
            "status": "COUNTERMODEL_GUARD_RETAINED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def bmem_insertion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "component_id": "BM4595_0_B826",
            "component": "B_826",
            "zero_condition": "earlier parent trace/branch extremum coefficient is theorem-zero in the same memory branch",
            "finite_bound": "|B_826| retained as absolute coefficient if not zero",
            "source": str(CSV_4514_BMEM),
            "status": "IMPORTED_COMPONENT_UNSIGNED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "component_id": "BM4595_1_BWeyl",
            "component": "B_Weyl_vec",
            "zero_condition": "source-root/no-spurion/Khat gate zeros the Weyl-response tail",
            "finite_bound": "||B_Weyl_vec|| retained from the 4514 vector",
            "source": str(CSV_4514_BMEM),
            "status": "IMPORTED_COMPONENT_UNSIGNED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "component_id": "BM4595_2_Y5",
            "component": "B_Y5_trace",
            "zero_condition": "single q-basic Hilbert mass-current/source functor with universal calibration",
            "finite_bound": "||B_Y5_trace|| <= sum_i ||j_Z,Y5_i|| ||P_i||",
            "source": str(CSV_4515_Y5),
            "status": "VECTOR_IMPORTED_PARTIAL_STATIONARY_CLOSURE_ONLY",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "component_id": "BM4595_3_Y6",
            "component": "B_Y6_trace",
            "zero_condition": "extra stress is topological/invisible, EH-owned metric response, or exchange-even",
            "finite_bound": "||B_Y6_trace|| <= sum_j ||j_Z,Y6_j|| ||X_j||",
            "source": str(CSV_4515_Y6),
            "status": "VECTOR_IMPORTED_UNSIGNED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "component_id": "BM4595_4_boundary_readout",
            "component": "B_src_boundary + B_src_readout",
            "zero_condition": "no source boundary/readout leakage through the local worldtube and same observed frame",
            "finite_bound": "absolute boundary/readout coefficients remain in Sigma_B",
            "source": str(CSV_4514_TAIL),
            "status": "TAIL_IMPORTED_UNSIGNED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "component_id": "BM4595_5_combined",
            "component": "B_mem_eff",
            "zero_condition": "B_826=B_Weyl_vec=B_Y5_trace=B_Y6_trace=B_src_boundary=B_src_readout=0 in the same parent branch",
            "finite_bound": "||B_mem_eff|| <= ||B_826||+||B_Weyl_vec||+||B_Y5_trace||+||B_Y6_trace||+||B_src_boundary||+||B_src_readout||",
            "source": f"{CSV_4514_BMEM};{CSV_4515_BOUND}",
            "status": "ABSOLUTE_SUM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def memory_bound_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "MEM4595_0_density",
            "target": "memory source density",
            "formula": "rho_mem = B_mem_eff R_obs + C_mem T + J_mem",
            "zero_condition": "B_mem_eff=C_mem=J_mem=0",
            "bound": "||rho_mem|| <= ||B_mem_eff|| ||R_obs|| + ||C_mem|| ||T|| + ||J_mem||",
            "needed_inputs": "B_mem_eff;C_mem;J_mem;R_obs;T;source units;source paths",
            "status": "DENSITY_BOUND_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "MEM4595_1_body_charge",
            "target": "memory body charge",
            "formula": "Q_mem0=4*pi int_0^R dr r^2 rho_mem(r) sinh(r/lambda_mem)/(r/lambda_mem)+Q_boundary_mem",
            "zero_condition": "rho_mem=0 and Q_boundary_mem=0, or exact weighted cancellation explicitly parent-owned",
            "bound": "|Q_mem0| <= exp(R_body/lambda_mem) int_body ||rho_mem|| dV + ||Q_boundary_mem||",
            "needed_inputs": "lambda_mem;R_body;rho_mem profile;Q_boundary_mem",
            "status": "BODY_CHARGE_BOUND_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "MEM4595_2_amplitude",
            "target": "exterior memory amplitude",
            "formula": "|A_mem| <= [exp(R_body/lambda_mem) int_body (||B_mem_eff||||R_obs||+||C_mem||||T||+||J_mem||) dV + ||Q_boundary_mem||]/(4*pi ||Z_mem||)",
            "zero_condition": "positive L_mem plus B_mem_eff=C_mem=J_mem=Q_boundary_mem=0",
            "bound": "if nonzero, map A_mem/lambda_mem to alpha_mem(lambda_mem), R10/orbital/PPN residual",
            "needed_inputs": "Z_mem;M2_mem;lambda_mem;B_mem_eff;C_mem;J_mem;Q_boundary_mem;arena projection",
            "status": "AMPLITUDE_BOUND_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "MEM4595_3_poynting_guard",
            "target": "J_mem EM/Poynting subchannel",
            "formula": "J_mem = J_nonHilbert + J_EM_flux; J_EM_flux=0 only under same_Hodge + same_current_owner + stationary_tau + no_radiative_boundary_flux",
            "zero_condition": "EM stress is inside common Hilbert T_tot and no Poynting flux crosses the local worldtube boundary",
            "bound": "||J_EM_flux|| <= ||Phi_EM_rad||+||W_public_exchange||+||C_EM_surface_gauge||",
            "needed_inputs": "same-Hodge/current owner certificate; Poynting flux collar; boundary/source paths",
            "status": "POYNTING_CHANNEL_KEPT_NOT_HIDDEN",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def fibre_bound_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "FIB4595_0_density",
            "target": "finite-cell fibre source density",
            "formula": "rho_h = B_h R_obs + C_h T + J_h",
            "zero_condition": "B_h=C_h=J_h=0",
            "bound": "||rho_h|| <= ||B_h||||R_obs|| + ||C_h||||T|| + ||J_h||",
            "needed_inputs": "B_h;C_h;J_h;R_obs;T;source units;source paths",
            "status": "FIBRE_DENSITY_BOUND_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "FIB4595_1_body_charge",
            "target": "finite-cell fibre body charge",
            "formula": "Q_h0=4*pi int_0^R dr r^2 rho_h(r) sinh(r/lambda_h)/(r/lambda_h)+Q_boundary_h",
            "zero_condition": "rho_h=0 and Q_boundary_h=0, or exact weighted cancellation explicitly parent-owned",
            "bound": "|Q_h0| <= exp(R_body/lambda_h) int_body ||rho_h|| dV + ||Q_boundary_h||",
            "needed_inputs": "lambda_h;R_body;rho_h profile;Q_boundary_h",
            "status": "FIBRE_BODY_CHARGE_BOUND_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "FIB4595_2_amplitude",
            "target": "exterior fibre amplitude",
            "formula": "|A_h| <= [exp(R_body/lambda_h) int_body (||B_h||||R_obs||+||C_h||||T||+||J_h||) dV + ||Q_boundary_h||]/(4*pi ||Z_h||)",
            "zero_condition": "positive L_h plus B_h=C_h=J_h=Q_boundary_h=0",
            "bound": "if nonzero, map A_h/lambda_h to alpha_h(lambda_h), R10/orbital/PPN residual",
            "needed_inputs": "Z_h;M2_h;lambda_h;B_h;C_h;J_h;Q_boundary_h;arena projection",
            "status": "FIBRE_AMPLITUDE_BOUND_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def finite_schema_rows(now: str) -> list[dict[str, Any]]:
    fields = [
        ("schema4595_0_memory_Z", "memory", "Z_mem", "operator normalization", "positive numeric/source-backed value"),
        ("schema4595_1_memory_M2", "memory", "M2_mem", "operator mass gap", "positive numeric/source-backed value"),
        ("schema4595_2_memory_B", "memory", "B_mem_eff components", "curvature-linear source vector", "component values or theorem-zero source paths"),
        ("schema4595_3_memory_C", "memory", "C_mem", "matter-trace coupling", "source-functor zero or finite coefficient"),
        ("schema4595_4_memory_J", "memory", "J_mem", "direct/non-Hilbert/Poynting current", "zero certificate or finite flux profile"),
        ("schema4595_5_memory_boundary", "memory", "Q_boundary_mem", "worldtube/boundary charge", "no-flux theorem or finite boundary integral"),
        ("schema4595_6_fibre_Z", "fibre", "Z_h", "operator normalization", "positive numeric/source-backed value"),
        ("schema4595_7_fibre_M2", "fibre", "M2_h", "operator mass gap", "positive numeric/source-backed value"),
        ("schema4595_8_fibre_B", "fibre", "B_h", "curvature-linear fibre vertex", "parent action exclusion or finite coefficient"),
        ("schema4595_9_fibre_C", "fibre", "C_h", "matter-trace fibre coupling", "h-blind matter functor or finite coefficient"),
        ("schema4595_10_fibre_J", "fibre", "J_h", "direct fibre current", "zero certificate or source profile"),
        ("schema4595_11_fibre_boundary", "fibre", "Q_boundary_h", "fibre boundary charge", "no-flux theorem or finite boundary integral"),
        ("schema4595_12_projection", "arena", "Pi_R10/Pi_PPN/Pi_orbital", "observable projection", "alpha(lambda), PPN and orbital maps"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "input_id": input_id,
            "sector": sector,
            "symbol": symbol,
            "role": role,
            "required_for_claim": requirement,
            "current_status": "MISSING_PARENT_SIGNED_OR_NUMERIC_SOURCE_ROW",
            "valid_for_claim": False,
            "generated_utc": now,
        }
        for input_id, sector, symbol, role, requirement in fields
    ]


def survivor_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4595_0_EH_principal",
            "residual_family": "EH/Palatini selector",
            "status_after_4595": "unchanged public parent-adoption blocker",
            "next_action": "retain parent selector/adoption gate",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4595_1_cGamma",
            "residual_family": "c_Gamma local memory coupling",
            "status_after_4595": "coupled to memory source-charge gate; not closed here",
            "next_action": "reuse B_mem_eff/C_mem/J_mem/Q_boundary rows in cGamma residual vector",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4595_2_cR2_MR",
            "residual_family": "c_R2/M_R finite-range branch",
            "status_after_4595": "direct pressure rows reduced to zero-switch or explicit body-charge finite-input schema",
            "next_action": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4595_3_cT_spin",
            "residual_family": "spin/torsion contact channel",
            "status_after_4595": "unchanged from 4593",
            "next_action": "do not reopen unless polarized/contact torsion selected",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4595_4_material_projection_global",
            "residual_family": "Lambda/material/projection/global parent",
            "status_after_4595": "unchanged broad blocker",
            "next_action": "keep promotion firewall active",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4595_positive_operator_nonzero_B",
            "input_branch": "Z_X>0,M_X^2>0 but B_X != 0",
            "expected_result": "body charge remains live; no local-GR closure",
            "control_status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4595_source_functor_unsigned",
            "input_branch": "source-functor descent assumed but not parent-signed",
            "expected_result": "C_mem/J_mem/Y5 rows remain conditional/nonclaim",
            "control_status": "COUNTERMODEL_CAUGHT",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4595_poynting_flux_open",
            "input_branch": "EM/Poynting flux crosses local worldtube boundary",
            "expected_result": "J_mem receives absolute flux contribution",
            "control_status": "POYNTING_NOT_HIDDEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4595_exact_cancellation",
            "input_branch": "weighted body charge cancels by tuning only",
            "expected_result": "no zero credit unless cancellation is parent-owned identity",
            "control_status": "NO_TUNING_CREDIT",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "common_zero_switch_written": True,
            "memory_body_charge_bound_written": True,
            "fibre_body_charge_bound_written": True,
            "poynting_guard_inserted": True,
            "parent_zero_or_numeric_bound_signed": False,
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "common memory/fibre zero switch; B_mem_eff absolute-sum insertion; A_mem and A_h body-charge bounds; finite-input schema; Poynting guard",
            "not_derived": "parent-signed B_mem_eff=C_mem=J_mem=Q_boundary_mem=0; parent-signed B_h=C_h=J_h=Q_boundary_h=0; numeric Z/M2/source coefficients; arena projections",
            "claim_status": "PRIVATE_NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "4595 reduces the memory/fibre cR2 pressure rows to a concrete zero switch or finite body-charge coefficient schema.",
            "derive_first": "parent-sign the common source functor for C_mem/J_mem/Y5 and the fibre h-blind action route; also prove no Poynting/worldtube flux contribution",
            "fallback": "fill the first real body-charge coefficient row: Z_X,M_X^2,B_X,C_X,J_X,Q_boundary_X plus R10/PPN/orbital projection",
            "valid_for_claim": False,
        }
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4595_0_sources_exist",
            "claim": "all cited source paths exist",
            "passed": False,
            "valid_for_claim": False,
            "detail": "validated after source register generation",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4595_1_needles_found",
            "claim": "all cited source needles found",
            "passed": False,
            "valid_for_claim": False,
            "detail": "validated after source register generation",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4595_2_zero_switch_written",
            "claim": "memory/fibre zero switch is written",
            "passed": True,
            "valid_for_claim": False,
            "detail": "B_X=C_X=J_X=Q_boundary_X=0 plus positive operator and zero-mode removal",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4595_3_body_bounds_written",
            "claim": "A_mem and A_h body-charge bounds are written",
            "passed": True,
            "valid_for_claim": False,
            "detail": "memory and fibre amplitude envelopes generated",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4595_4_poynting_guard",
            "claim": "EM/Poynting flux is not hidden",
            "passed": True,
            "valid_for_claim": False,
            "detail": "Poynting is zero only under same owner plus no worldtube flux; otherwise it remains J_mem",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4595_5_no_public_claim",
            "claim": "no local-GR/R10/PPN claim emitted",
            "passed": True,
            "valid_for_claim": False,
            "detail": "parent signatures and numeric coefficients remain missing",
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4595_6_next_target_written",
            "claim": "next coefficient/signature target selected",
            "passed": True,
            "valid_for_claim": False,
            "detail": NEXT_TARGET,
            "generated_utc": now,
        },
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4595 Y5 R2FR memory/fibre B_X C_X owner or body-charge input after cR2 gate

Private checkpoint generated at `{now}`.

Marker: `{MARKER}`
Branch: `{BRANCH_ID}`
Decision: `{DECISION}`
Claim register: `{CLAIM_ID}`

## Result

4595 does not reopen the whole local-GR ladder. It takes the exact pressure row exposed by 4594 and turns it into the sharp memory/fibre contract.

For each retained local memory/fibre field `X in {{m,h}}`,

```text
L_X delta_X = (-Z_X nabla^2 + M_X^2) delta_X = rho_X,
rho_X = B_X R_obs + C_X T + J_X,
lambda_X = sqrt(Z_X/M_X^2).
```

The strict local zero route is:

```text
Z_X>0, M_X^2>0, zero modes removed,
B_X=C_X=J_X=Q_boundary_X=0 in the same parent branch
=> delta_X=0, A_X=0.
```

For memory the curvature vertex is the already-built effective vector:

```text
B_mem_eff = B_826 + B_Weyl_vec + B_Y5_trace + B_Y6_trace
          + B_src_boundary + B_src_readout.
```

So memory silence requires:

```text
B_mem_eff=C_mem=J_mem=Q_boundary_mem=0.
```

If that is not parent-signed, the branch is finite and must be scored by the body-charge envelope:

```text
|A_mem| <= [exp(R_body/lambda_mem) int_body
 (||B_mem_eff||||R_obs|| + ||C_mem||||T|| + ||J_mem||) dV
 + ||Q_boundary_mem||] / (4*pi ||Z_mem||).
```

For the finite-cell fibre:

```text
|A_h| <= [exp(R_body/lambda_h) int_body
 (||B_h||||R_obs|| + ||C_h||||T|| + ||J_h||) dV
 + ||Q_boundary_h||] / (4*pi ||Z_h||).
```

This is a forward step, not another audit loop: the missing objects are now exactly the source coefficients or parent-zero certificates needed to run a real R10/PPN/orbital finite comparison.

EM/Poynting flow is kept live in `J_mem`. It is zero only if it belongs to the same Hilbert/Hodge/current owner and no radiative/current flux crosses the local worldtube boundary. Otherwise it remains an absolute source term.

No local-GR, R10, PPN or orbital pass is claimed from this checkpoint.

## Source Register

{markdown_table(tables["sources"])}

## Owner Zero Switch

{markdown_table(tables["zero_switch"])}

## Bmem Effective Insertion

{markdown_table(tables["bmem"])}

## Memory Body-Charge Bound

{markdown_table(tables["memory"])}

## Fibre Body-Charge Bound

{markdown_table(tables["fibre"])}

## Finite Input Schema

{markdown_table(tables["schema"])}

## Survivor Update

{markdown_table(tables["survivors"])}

## Controls

{markdown_table(tables["controls"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Decision

{markdown_table(tables["decision"])}

## Status

{markdown_table(tables["status"])}

## Next Target

{markdown_table(tables["next"])}
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 611 - Memory/Fibre B_X C_X Owner Or Body-Charge Input After cR2 Gate

Generated: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Claim register: `{CLAIM_ID}`

## Formal Claim

After the cR2/MR finite-range gate, each retained memory/fibre field `X` is locally silent only under the same-branch zero switch:

```text
L_X delta_X = (-Z_X nabla^2 + M_X^2) delta_X,
rho_X = B_X R_obs + C_X T + J_X,
Z_X>0, M_X^2>0, zero modes removed,
B_X=C_X=J_X=Q_boundary_X=0
=> delta_X=0 and A_X=0.
```

For memory:

```text
B_X = B_mem_eff
    = B_826 + B_Weyl_vec + B_Y5_trace + B_Y6_trace
      + B_src_boundary + B_src_readout.
```

For finite-cell fibre:

```text
B_X = B_h.
```

If any zero-switch clause is unsigned, the branch remains finite:

```text
|A_X| <= [exp(R_body/lambda_X) int_body |rho_X| dV + |Q_boundary_X|] / (4*pi |Z_X|).
```

This formal note blocks three common shortcuts:

1. positive `L_X` does not erase a nonzero source vertex;
2. exterior source-free equations do not erase body charge;
3. fitted `G`, EM/Poynting flow or source calibration cannot be hidden outside `C_X/J_X`.

## Status

Private nonclaim. The next target is `{NEXT_TARGET}`.
"""


def update_promotion_with_sources(rows: list[dict[str, Any]], sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    all_paths = all(row["path_exists"] for row in sources)
    all_needles = all(row["needle_found"] for row in sources)
    for row in rows:
        if row["gate_id"] == "PROM4595_0_sources_exist":
            row["passed"] = all_paths
            row["detail"] = "all source paths found" if all_paths else "one or more source paths missing"
        if row["gate_id"] == "PROM4595_1_needles_found":
            row["passed"] = all_needles
            row["detail"] = "all source needles found" if all_needles else "one or more source needles missing"
    return rows


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validation: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    add("VAL4595_00_sources_exist", all(row["path_exists"] for row in tables["sources"]), "all cited source paths exist")
    add("VAL4595_01_needles_found", all(row["needle_found"] for row in tables["sources"]), "all cited source needles found")

    csv_paths = [
        SOURCE_REGISTER,
        ZERO_SWITCH_CSV,
        MEMORY_BOUND_CSV,
        FIBRE_BOUND_CSV,
        BMEM_INSERTION_CSV,
        FINITE_SCHEMA_CSV,
        SURVIVOR_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    csv_details = []
    csv_ok = True
    for path in csv_paths:
        rows = read_csv(path)
        csv_details.append(f"{path.name}:{len(rows)}")
        csv_ok = csv_ok and bool(rows)
    add("VAL4595_02_csv_parse", csv_ok, ";".join(csv_details))

    zero_text = "\n".join(str(row) for row in tables["zero_switch"])
    add("VAL4595_03_zero_switch", "B_X=C_X=J_X=Q_boundary_X=0" in zero_text, "common zero switch has all source terms")

    memory_text = "\n".join(str(row) for row in tables["memory"])
    add("VAL4595_04_memory_bound", "B_mem_eff" in memory_text and "A_mem" in memory_text, "memory body-charge bound includes B_mem_eff and A_mem")

    fibre_text = "\n".join(str(row) for row in tables["fibre"])
    add("VAL4595_05_fibre_bound", "B_h" in fibre_text and "A_h" in fibre_text, "fibre body-charge bound includes B_h and A_h")

    bmem_text = "\n".join(str(row) for row in tables["bmem"])
    add("VAL4595_06_bmem_abs_sum", "B_mem_eff" in bmem_text and "B_Y5_trace" in bmem_text and "B_Y6_trace" in bmem_text, "B_mem_eff absolute-sum vector written")

    poynting_text = memory_text + "\n" + read_text(DOC_PATH)
    add("VAL4595_07_poynting_guard", "Poynting" in poynting_text and "J_mem" in poynting_text, "Poynting channel retained inside J_mem guard")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "local_GR_public_claim", "parent_zero_or_numeric_bound_signed"} and value is True:
                    all_false = False
    add("VAL4595_08_no_claim_true", all_false, "no generated table promotes claim_allowed/valid_for_claim")

    add("VAL4595_09_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4595_10_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4595_11_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4595_12_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4595_13_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4595_14_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4595_15_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4595_16_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))

    overall = all(row["status"] == "PASS" for row in validation)
    add("VAL4595_OVERALL", overall, "4595 memory/fibre B/C owner zero-or-bound gate")
    return validation


def main() -> None:
    now = utc_now()

    tables = {
        "sources": source_rows(now),
        "zero_switch": zero_switch_rows(now),
        "bmem": bmem_insertion_rows(now),
        "memory": memory_bound_rows(now),
        "fibre": fibre_bound_rows(now),
        "schema": finite_schema_rows(now),
        "survivors": survivor_rows(now),
        "controls": control_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = update_promotion_with_sources(promotion_rows(now), tables["sources"])

    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(ZERO_SWITCH_CSV, tables["zero_switch"])
    write_csv(BMEM_INSERTION_CSV, tables["bmem"])
    write_csv(MEMORY_BOUND_CSV, tables["memory"])
    write_csv(FIBRE_BOUND_CSV, tables["fibre"])
    write_csv(FINITE_SCHEMA_CSV, tables["schema"])
    write_csv(SURVIVOR_CSV, tables["survivors"])
    write_csv(CONTROL_CSV, tables["controls"])
    write_csv(PROMOTION_CSV, tables["promotion"])
    write_csv(DECISION_CSV, tables["decision"])
    write_csv(STATUS_CSV, tables["status"])
    write_csv(NEXT_CSV, tables["next"])

    write_text(DOC_PATH, build_doc(now, tables))
    write_text(FORMAL_PATH, build_formal(now))
    append_claim_once()

    spine_block = f"""
## PPC4161 Local Addendum - Memory/Fibre B/C Zero Or Body-Charge Gate After cR2

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

After the c_R2/M_R finite-range gate, the memory/fibre pressure rows are no longer loose missing terms. For `X in {{memory,fibre}}`, local silence requires a positive massive operator plus `B_X=C_X=J_X=Q_boundary_X=0` in the same parent branch. Otherwise the branch is finite and must be scored by the `A_mem`/`A_h` body-charge envelopes. EM/Poynting flux is retained inside `J_mem` unless the same Hilbert/Hodge/current owner and no-flux worldtube collar are signed.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""
## PPC4161 Packet Addendum - Memory/Fibre B/C Gate After cR2

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private local packet now has a concrete memory/fibre zero switch instead of another broad source-tail phrase. The next useful move is to parent-sign or numerically fill one of: `B_mem_eff,C_mem,J_mem,Q_boundary_mem,B_h,C_h,J_h,Q_boundary_h,Z_X,M_X^2`, then project it into R10/PPN/orbital scoring. No local-GR pass is emitted.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    validation_rows = validate(tables)
    write_csv(VALIDATION_CSV, validation_rows)

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4595 validation failed: {failed}")
    print(f"4595 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
