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

CHECKPOINT = "4611"
CLAIM_ID = "L-453"
BRANCH_ID = "MTS_R2FR_Y5_QBARXH_FULL_SOURCE_ENVELOPE_ROLLUP_4611"
MARKER = "PPC4161_QBARXH_FULL_SOURCE_ENVELOPE_ROLLUP_OR_FIRST_SOURCE_BACKED_INPUT_4611"
PACKET_MARKER = "PPC4161_PACKET_QBARXH_FULL_SOURCE_ENVELOPE_ROLLUP_4611"
DECISION = "QBARXH_FULL_SOURCE_ENVELOPE_ROLLUP_READY_FIRST_SOURCE_BACKED_QUEUE_NONCLAIM"
NEXT_TARGET = "4612-Y5-R2FR-qbarXT-test-body-response-envelope-or-first-source-backed-input.md"

DOC_PATH = POST / "4611-Y5-R2FR-QbarXH-full-source-envelope-rollup-or-first-source-backed-input.md"
FORMAL_PATH = FORMAL / "627-PPC4161-QbarXH-full-source-envelope-rollup-or-first-source-backed-input.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4611_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4611_QBARXH_SOURCE_ENVELOPE_THEOREM.csv"
QBULK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4611_QBULK_ROLLUP_ROWS.csv"
QEDGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4611_QEDGE_ROLLUP_ROWS.csv"
QSHADOW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4611_QSHADOW_ROLLUP_ROWS.csv"
DENOMINATOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4611_QBARXH_DENOMINATOR_PROJECTOR_ROWS.csv"
PRIORITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4611_FIRST_SOURCE_BACKED_PRIORITY_QUEUE.csv"
PRODUCT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4611_PRODUCT_HANDOFF_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4611_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4611_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4611_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4611_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4611_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4611_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4611_VALIDATION.csv"

CSV_4610_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4610_NEXT_TARGET.csv"
CSV_4610_UPDATE = SOURCE_DIR / "P8_Y5_R2FR_4610_QSHADOW_QBARXH_UPDATE_ROWS.csv"
CSV_4610_ACTION = SOURCE_DIR / "P8_Y5_R2FR_4610_QSHADOW_ACTION_ROWS.csv"
CSV_4610_PROJECTOR = SOURCE_DIR / "P8_Y5_R2FR_4610_QSHADOW_PROJECTOR_ROWS.csv"
CSV_4610_NONVAR = SOURCE_DIR / "P8_Y5_R2FR_4610_QSHADOW_NONVARIATIONAL_ROWS.csv"
CSV_4609_UPDATE = SOURCE_DIR / "P8_Y5_R2FR_4609_QEDGE_QBARXH_UPDATE_ROWS.csv"
CSV_4609_SHELL = SOURCE_DIR / "P8_Y5_R2FR_4609_QEDGE_REYNOLDS_SHELL_ROWS.csv"
CSV_4609_BOUNDARY = SOURCE_DIR / "P8_Y5_R2FR_4609_QEDGE_BOUNDARY_FLUX_ROWS.csv"
CSV_4608_UPDATE = SOURCE_DIR / "P8_Y5_R2FR_4608_QBULK_RETAINED_UPDATE_ROWS.csv"
CSV_4608_JDIRECT = SOURCE_DIR / "P8_Y5_R2FR_4608_JDIRECT_ROWS.csv"
CSV_4608_JMEM = SOURCE_DIR / "P8_Y5_R2FR_4608_JMEM_ROWS.csv"
CSV_4608_JREADOUT = SOURCE_DIR / "P8_Y5_R2FR_4608_JREADOUT_ROWS.csv"
CSV_4607_UPDATE = SOURCE_DIR / "P8_Y5_R2FR_4607_EM_BULK_BOUND_UPDATE_ROWS.csv"
CSV_4607_POYNTING = SOURCE_DIR / "P8_Y5_R2FR_4607_POYNTING_FLUX_ROWS.csv"
CSV_4606_UPDATE = SOURCE_DIR / "P8_Y5_R2FR_4606_QBULK_UPDATE_ROWS.csv"
CSV_4606_HILBERT = SOURCE_DIR / "P8_Y5_R2FR_4606_QBULK_HILBERT_ROWS.csv"
CSV_4606_RETAINED = SOURCE_DIR / "P8_Y5_R2FR_4606_QBULK_RETAINED_ROWS.csv"
CSV_4605_NUMERATOR = SOURCE_DIR / "P8_Y5_R2FR_4605_QBARXH_NUMERATOR_UPDATE_ROWS.csv"
CSV_4605_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4605_SOURCE_NUMERATOR_THEOREM.csv"
CSV_4604_QBAR = SOURCE_DIR / "P8_Y5_R2FR_4604_QBARXH_FIRST_FILL_ROWS.csv"
CSV_4604_MHREF = SOURCE_DIR / "P8_Y5_R2FR_4604_MHREF_DENOMINATOR_INPUT_ROWS.csv"
CSV_4604_PIM = SOURCE_DIR / "P8_Y5_R2FR_4604_PIM_PROJECTOR_INPUT_ROWS.csv"

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
    for number, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return number
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
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    suffix = "\n" if text.endswith("\n") or not text else "\n\n"
    write_text(path, text + suffix + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not path.exists() or not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--porcelain"], text=True, capture_output=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def append_claim_once() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = [
        "claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk",
        "sector", "evidence", "next_action", "risk",
    ]
    rows.append({
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4611 assembles the full Qbar_XH source envelope from bulk, edge and shadow numerator rows, then installs the denominator/projector firewall before qbar_XT or arena testing.",
        "current_evidence": "Generated Qbar_XH source-envelope theorem rows, bulk/edge/shadow rollups, denominator/projector rows, first source-backed priority queue, handoff rows and validation.",
        "status": "QbarXH_full_source_envelope_rollup_ready_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating a symbolic source envelope as a local-GR pass before M_lower, Pi_M, Qbar_XH, qbar_XT, Z_X and arena tau inputs are source-backed.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No R10, PPN, clock, orbital, Newton or local-GR claim until source and test-body factors are numeric/source-backed or exact-zero signed by the parent action.",
    })
    existing = list(rows[0].keys()) if rows else fieldnames
    for name in fieldnames:
        if name not in existing:
            existing.append(name)
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=existing)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in existing})


def source_rows(now: str) -> list[dict[str, Any]]:
    sources = [
        ("SRC4611_00_4610_handoff", CSV_4610_NEXT, "4611-Y5-R2FR-QbarXH-full-source-envelope-rollup-or-first-source-backed-input.md", "4610 requested full Qbar_XH source-envelope rollup."),
        ("SRC4611_01_4610_qbar", CSV_4610_UPDATE, "QSU4610_2_QbarXH", "4610 Qbar_XH update row."),
        ("SRC4611_02_4610_shadow_total", CSV_4610_UPDATE, "QSU4610_0_shadow_total", "4610 shadow total row."),
        ("SRC4611_03_4610_qtot", CSV_4610_UPDATE, "QSU4610_1_Qtot", "4610 full numerator split row."),
        ("SRC4611_04_4610_action", CSV_4610_ACTION, "QSA4610_0_total", "4610 action shadow row."),
        ("SRC4611_05_4610_projector", CSV_4610_PROJECTOR, "QSP4610_0_total", "4610 projector shadow row."),
        ("SRC4611_06_4610_nonvar", CSV_4610_NONVAR, "QSN4610_0_total", "4610 nonvariational shadow row."),
        ("SRC4611_07_4609_edge_total", CSV_4609_UPDATE, "QEU4609_0_edge_total", "4609 edge total row."),
        ("SRC4611_08_4609_shell", CSV_4609_SHELL, "QES4609_5_total", "4609 Reynolds/source shell row."),
        ("SRC4611_09_4609_boundary", CSV_4609_BOUNDARY, "QEB4609_0_boundary_primitive", "4609 boundary flux row."),
        ("SRC4611_10_4608_bulk_total", CSV_4608_UPDATE, "QBR4608_1_bulk_total", "4608 bulk total row."),
        ("SRC4611_11_4608_retained", CSV_4608_UPDATE, "QBR4608_0_retained", "4608 retained source-current row."),
        ("SRC4611_12_4608_direct", CSV_4608_JDIRECT, "JD4608_0_total", "4608 direct retained source row."),
        ("SRC4611_13_4608_mem", CSV_4608_JMEM, "JM4608_0_total", "4608 memory retained source row."),
        ("SRC4611_14_4608_readout", CSV_4608_JREADOUT, "JR4608_0_total", "4608 readout retained source row."),
        ("SRC4611_15_4607_em_update", CSV_4607_UPDATE, "EB4607_1_bound_route", "4607 EM/Poynting bound row."),
        ("SRC4611_16_4607_poynting", CSV_4607_POYNTING, "FX4607_1_wall_flux_bound", "4607 Poynting wall-flux row."),
        ("SRC4611_17_4606_bulk_update", CSV_4606_UPDATE, "BU4606_1_absolute_bound", "4606 bulk bound row."),
        ("SRC4611_18_4606_hilbert", CSV_4606_HILBERT, "H4606_TOTAL", "4606 Hilbert bulk row."),
        ("SRC4611_19_4606_retained", CSV_4606_RETAINED, "R4606_TOTAL", "4606 retained current placeholder row."),
        ("SRC4611_20_4605_numerator", CSV_4605_NUMERATOR, "QU4605_0_numerator_abs", "4605 numerator absolute-sum row."),
        ("SRC4611_21_4605_theorem", CSV_4605_THEOREM, "NUM4605_4_absolute_numerator_bound", "4605 source numerator theorem."),
        ("SRC4611_22_4604_qbar_bound", CSV_4604_QBAR, "QF4604_1_absolute_Qbar_bound", "4604 Qbar_XH denominator/projector bound."),
        ("SRC4611_23_4604_mlower", CSV_4604_MHREF, "MD4604_2_M_lower", "4604 positive denominator input row."),
        ("SRC4611_24_4604_pim_norm", CSV_4604_PIM, "PM4604_1_operator_norm", "4604 projector operator norm row."),
        ("SRC4611_25_4604_pim_comm", CSV_4604_PIM, "PM4604_2_commutator", "4604 projector commutator row."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in sources:
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": line_of(path, needle) > 0,
            "line": line_of(path, needle),
            "role": role,
            "valid_for_claim": False,
            "generated_utc": now,
        })
    return rows


def theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QBAR4611_0_full_source_envelope",
            "quantity": "Q_tot_XH_abs",
            "formula": "|Q_tot_XH| <= |Q_bulk|_abs + |Q_edge|_abs + |Q_shadow|_abs",
            "zero_condition": "Q_bulk=Q_edge=Q_shadow=0 in the same parent branch",
            "source_anchor": "QBR4608_1_bulk_total;QEU4609_0_edge_total;QSU4610_0_shadow_total;QSU4610_1_Qtot",
            "current_status": "FULL_SOURCE_ENVELOPE_ASSEMBLED_SYMBOLIC_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QBAR4611_1_QbarXH_projection_bound",
            "quantity": "Qbar_XH_abs",
            "formula": "|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|_abs+|Q_edge|_abs+|Q_shadow|_abs)+|E_PiM_comm|)/M_lower",
            "zero_condition": "full numerator zero, fixed projector commutes and M_lower>0",
            "source_anchor": "QF4604_1_absolute_Qbar_bound;QU4605_1_Qbar_insert;QSU4610_2_QbarXH",
            "current_status": "DENOMINATOR_PROJECTOR_FIREWALL_INSTALLED_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QBAR4611_2_no_cancellation_rule",
            "quantity": "Qbar_XH_claim_firewall",
            "formula": "all source pieces are absolute-sum rows; cross-cancellation and measured-G absorption are forbidden unless source-backed",
            "zero_condition": "each named component is exact-zero signed or explicitly bounded",
            "source_anchor": "4604..4610 rollup",
            "current_status": "FIREWALL_READY_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QBAR4611_3_first_source_backed_queue",
            "quantity": "source_backed_priority_order",
            "formula": "attack M_lower/Pi_M first, then edge shell, Poynting wall flux, epsilon_source_shadow and retained currents",
            "zero_condition": "first numeric/source-backed rows replace MISSING symbolic rows",
            "source_anchor": "priority_queue_4611",
            "current_status": "QUEUE_READY_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QBAR4611_4_product_handoff",
            "quantity": "I_X^ST(lambda)",
            "formula": "|I_X^ST| <= |Qbar_XH| |qbar_XT|/(4*pi |Z_X| G_N M_H_ref m_T)",
            "zero_condition": "source side Qbar_XH zero/bounded and test side qbar_XT/Z_X/tau rows source-backed",
            "source_anchor": "QEU4609_2_product",
            "current_status": "SOURCE_SIDE_ROLLUP_READY_TEST_SIDE_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def bulk_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BROLL4611_0_bulk_total",
            "quantity": "Q_bulk_abs",
            "formula": "|Q_bulk| <= |Q_bulk_Hilbert| + |Q_bulk_EM/Poynting| + |Q_bulk_retained|",
            "inputs": "Q_bulk_Hilbert_abs;Q_bulk_EM_Poynting_abs;Q_bulk_retained_abs",
            "current_status": "BULK_ROLLUP_SYMBOLIC_VALUES_MISSING",
            "source_anchor": "BU4606_1_absolute_bound;QBR4608_1_bulk_total",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BROLL4611_1_Hilbert",
            "quantity": "Q_bulk_Hilbert_abs",
            "formula": "same-frame Hilbert source component; zero only if ordinary Hilbert stress is the sole branch owner",
            "inputs": "H4606_TOTAL",
            "current_status": "HILBERT_ROUTE_CONDITIONAL_NOT_LOCAL_CLAIM",
            "source_anchor": "P8_Y5_R2FR_4606_QBULK_HILBERT_ROWS.csv",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BROLL4611_2_EM_Poynting",
            "quantity": "Q_bulk_EM_Poynting_abs",
            "formula": "|Q_bulk_EM/Poynting| <= W_lambda_max(M_ref|Delta_Hodge_EM|+|c_Poynt_extra Phi_wall|+|Phi_wall_Poynting|+M_ref|epsilon_nonminimal_EM|)",
            "inputs": "Delta_Hodge_EM;c_Poynt_extra;Phi_wall_Poynting;epsilon_nonminimal_EM;W_lambda_max",
            "current_status": "POYNTING_ROUTE_PHYSICALLY_PROMISING_VALUES_MISSING",
            "source_anchor": "EB4607_1_bound_route;FX4607_1_wall_flux_bound",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BROLL4611_3_retained",
            "quantity": "Q_bulk_retained_abs",
            "formula": "|Q_bulk_retained| <= W_lambda_max(|J_direct|+|J_mem|+|J_marker|+|J_readout|)",
            "inputs": "J_direct_abs;J_mem_abs;J_marker_abs;J_readout_abs;W_lambda_max;R4606_TOTAL",
            "current_status": "RETAINED_SOURCE_CURRENT_VALUES_MISSING",
            "source_anchor": "QBR4608_0_retained",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
    ]


def edge_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EROLL4611_0_edge_total",
            "quantity": "Q_edge_abs",
            "formula": "|Q_edge| <= |Q_edge_shell| + |Q_edge_boundary|",
            "inputs": "Q_edge_shell_abs;Q_edge_boundary_abs",
            "current_status": "EDGE_ROLLUP_SYMBOLIC_VALUES_MISSING",
            "source_anchor": "QEU4609_0_edge_total",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EROLL4611_1_shell",
            "quantity": "Q_edge_shell_abs",
            "formula": "|Q_edge_shell| <= W_lambda_edge_max Phi_edge (rho_H_trace_norm V_n_bound + mu_birth_TV)",
            "inputs": "rho_H_trace_norm;V_n_bound;mu_birth_TV;Phi_edge;W_lambda_edge_max",
            "current_status": "CLEAN_FIRST_SOURCE_BACKED_TARGET_VALUES_MISSING",
            "source_anchor": "QES4609_5_total",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EROLL4611_2_boundary",
            "quantity": "Q_edge_boundary_abs",
            "formula": "|Q_edge_boundary| <= |B_X_flux|+|C_corner|+|E_reference_edge|+|Phi_sidewall|+|Phi_radiative|+|E_projector_edge|",
            "inputs": "boundary primitive;corner/reference;sidewall/radiative/projector edge rows",
            "current_status": "BOUNDARY_FLUX_COMPONENT_VALUES_MISSING",
            "source_anchor": "QEB4609_0_boundary_primitive",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
    ]


def shadow_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SROLL4611_0_shadow_total",
            "quantity": "Q_shadow_abs",
            "formula": "|Q_shadow| <= |Q_shadow_action| + |Q_shadow_projector| + |Q_shadow_nonvariational|",
            "inputs": "Q_shadow_action_abs;Q_shadow_projector_abs;Q_shadow_nonvariational_abs",
            "current_status": "SHADOW_ROLLUP_SYMBOLIC_VALUES_MISSING",
            "source_anchor": "QSU4610_0_shadow_total",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SROLL4611_1_action",
            "quantity": "Q_shadow_action_abs",
            "formula": "|Q_shadow_action| <= |delta DeltaS_shadow/delta X|+|c_nonminimal|+|c_boundary|+|c_frame_shadow|",
            "inputs": "action inventory;operator basis;boundary double-count firewall;frame owner",
            "current_status": "ACTION_CLASSIFICATION_VALUES_MISSING",
            "source_anchor": "QSA4610_0_total",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SROLL4611_2_projector",
            "quantity": "Q_shadow_projector_abs",
            "formula": "|Q_shadow_projector| <= |C0_common_unowned| ||T_H|| + epsilon_source_shadow ||T_H|| + |E_projector_source| + |E_readout_return|",
            "inputs": "C0_common_unowned;epsilon_source_shadow;E_projector_source;E_readout_return",
            "current_status": "PROJECTOR_VALUES_MISSING_ONE_WEP_SMOKE_ONLY",
            "source_anchor": "QSP4610_0_total;QSP4610_2_relative_projector",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "SROLL4611_3_nonvariational",
            "quantity": "Q_shadow_nonvariational_abs",
            "formula": "|Q_shadow_nonvariational| <= |E_decoupled|+|Q_conserved_extra|+|Q_inconsistency_repair|",
            "inputs": "E_decoupled;Q_conserved_extra;Q_inconsistency_repair",
            "current_status": "BIANCHI_IS_FILTER_NOT_ZERO_VALUE",
            "source_anchor": "QSN4610_0_total",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
    ]


def denominator_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "DPROJ4611_0_M_lower",
            "quantity": "M_lower",
            "formula": "M_lower = M_0(1-epsilon_abs), with M_0>0 and 0<=epsilon_abs<1",
            "required_inputs": "M_0;epsilon_abs;same-frame source units",
            "current_status": "MISSING_POSITIVE_LOWER_BOUND",
            "source_anchor": "MD4604_2_M_lower",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "DPROJ4611_1_PiM_norm",
            "quantity": "||Pi_M^H||",
            "formula": "operator norm of fixed mass/source projector on Q_tot vector space",
            "required_inputs": "source vector norm;projector definition;units ledger",
            "current_status": "MISSING_PROJECTOR_OPERATOR_NORM",
            "source_anchor": "PM4604_1_operator_norm",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "DPROJ4611_2_commutator",
            "quantity": "E_PiM_comm",
            "formula": "E_PiM_comm bounds [D_v,Pi_M]Q_tot or [d,Pi_M]J_H",
            "required_inputs": "commutator zero certificate or numeric residual bound",
            "current_status": "MISSING_PROJECTOR_COMMUTATOR_ZERO_OR_BOUND",
            "source_anchor": "PM4604_2_commutator",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "DPROJ4611_3_firewall",
            "quantity": "Qbar_XH_claim_firewall",
            "formula": "no division by symbolic M_lower; no measured-G absorption of relative/projector/source residuals",
            "required_inputs": "all DPROJ4611 rows source-backed or exact-zero signed",
            "current_status": "FIREWALL_ACTIVE",
            "source_anchor": "QF4604_1_absolute_Qbar_bound",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
    ]


def priority_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "priority": 1,
            "target_quantity": "M_lower, ||Pi_M^H||, E_PiM_comm",
            "why_first": "every Qbar_XH claim divides by M_lower and multiplies by Pi_M; without this the whole source envelope is only symbolic",
            "candidate_sources": "4604 denominator/projector rows; Hamiltonian reference rows 4589/4590/4591/2665",
            "acceptance_gate": "positive M_lower, declared units, projector norm/commutator zero-or-bound, source paths exist",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "priority": 2,
            "target_quantity": "Q_edge_shell_abs",
            "why_first": "edge shell has the cleanest measurable-looking formula and can kill a large local-bound loophole without solving every shadow term",
            "candidate_sources": "QES4609_0..5 trace/velocity/birth/test/kernel rows",
            "acceptance_gate": "rho_H_trace_norm, V_n_bound, mu_birth_TV, Phi_edge and W_lambda_edge_max are numeric/source-backed or exact-zero signed",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "priority": 3,
            "target_quantity": "Phi_wall_Poynting_abs and EM/Hodge leakage",
            "why_first": "this is the user's Poynting-vector hunch translated into a source-side leakage row rather than ignored",
            "candidate_sources": "FX4607_1_wall_flux_bound;EB4607_1_bound_route",
            "acceptance_gate": "closed/stationary zero certificate or finite flux bound for the selected source collar",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "priority": 4,
            "target_quantity": "epsilon_source_shadow",
            "why_first": "projector/source-map shadow is a plausible local WEP/PPN killer if left free",
            "candidate_sources": "QSP4610_2_relative_projector;3347 epsilon rows",
            "acceptance_gate": "general source/projector bound beyond one WEP smoke row",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "priority": 5,
            "target_quantity": "J_direct_abs, J_mem_abs, J_readout_abs",
            "why_first": "retained currents may carry the real coupling physics, but they are harder than the denominator/edge rows",
            "candidate_sources": "JD4608_0_total;JM4608_0_total;JR4608_0_total",
            "acceptance_gate": "component values or exact-zero signatures for direct/memory/readout source currents",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "priority": 6,
            "target_quantity": "Q_shadow_action_abs and Q_shadow_nonvariational_abs",
            "why_first": "needed eventually, but most sensitive to parent-action inventory and overclaim risk",
            "candidate_sources": "QSA4610_0_total;QSN4610_0_total",
            "acceptance_gate": "operator basis, action owner and nonvariational exclusion/bound are source-backed",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def product_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "PROD4611_0_source_side",
            "quantity": "Qbar_XH_abs",
            "formula": "|Qbar_XH| <= (||Pi_M^H|| Q_tot_XH_abs + |E_PiM_comm|)/M_lower",
            "current_status": "SOURCE_SIDE_ROLLED_UP_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "PROD4611_1_test_side",
            "quantity": "qbar_XT_abs",
            "formula": "test-body response envelope still needs the same non-cancellation treatment",
            "current_status": "NEXT_TARGET_TEST_BODY_RESPONSE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "PROD4611_2_arena",
            "quantity": "R10/PPN/clock/orbital tau rows",
            "formula": "arena pass only after source side, test side, Z_X and tau projections are numeric/source-backed",
            "current_status": "ARENA_TESTING_NOT_READY",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4611_0_no_public_push",
            "rule": "work stays local/private; no GitHub push, no public repo mutation",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4611_1_no_symbolic_claim",
            "rule": "symbolic Qbar_XH rows are scaffolding only, not local-GR/R10/PPN evidence",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4611_2_no_cancellation",
            "rule": "no cancellation between Q_bulk, Q_edge and Q_shadow unless a parent-signed identity is supplied",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4611_3_no_measured_G_smuggling",
            "rule": "universal normalization can be tracked, but relative/range/species/time residuals cannot be absorbed into measured G_N",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4611_0_denominator",
            "blocks": "Qbar_XH claim",
            "missing": "M_lower positive source-backed lower bound",
            "resolution": "derive/source M_0 and epsilon_abs with same-frame units",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4611_1_projector",
            "blocks": "Qbar_XH claim",
            "missing": "||Pi_M^H|| and E_PiM_comm zero/bounds",
            "resolution": "prove fixed projector commute or keep additive commutator residual",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4611_2_source_values",
            "blocks": "source-side local-GR reduction",
            "missing": "numeric/source-backed values for Q_bulk, Q_edge and Q_shadow components",
            "resolution": "fill the 4611 priority queue in order",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4611_3_test_side",
            "blocks": "arena tests",
            "missing": "qbar_XT, Z_X and tau projections",
            "resolution": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4611_0_source_traceability",
            "requirement": "every cited 4604-4610 source path exists and every cited row needle is found",
            "current_status": "PASS" if all(row["path_exists"] and row["needle_found"] for row in sources) else "FAIL",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4611_1_denominator_projector",
            "requirement": "M_lower, ||Pi_M^H|| and E_PiM_comm are numeric/source-backed or exact-zero signed",
            "current_status": "BLOCKED_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4611_2_source_components",
            "requirement": "Q_bulk, Q_edge and Q_shadow are all exact-zero or bounded by source-backed rows",
            "current_status": "BLOCKED_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4611_3_product_ready",
            "requirement": "qbar_XT, Z_X, tau_R10/tau_PPN/tau_clock/tau_orbital are ready",
            "current_status": "BLOCKED_NEXT_TARGET",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "decision": DECISION,
        "meaning": "Qbar_XH has been collapsed into one source-envelope theorem and a ranked first-input acquisition queue; it remains nonclaim.",
        "next_target": NEXT_TARGET,
        "valid_for_claim": False,
        "generated_utc": now,
    }]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "status": DECISION,
        "what_moved": "The source side is no longer scattered across bulk/edge/shadow files; it is now one auditable Qbar_XH envelope plus a source-backed fill order.",
        "what_did_not_move": "No local-GR, R10, PPN, clock, orbital, Newton or Maxwell claim; all empirical arenas remain blocked until numeric/source-backed inputs exist.",
        "valid_for_claim": False,
        "generated_utc": now,
    }]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "generated_utc": now,
        "next_target": NEXT_TARGET,
        "reason": "Once source-side Qbar_XH is rolled up, the product still cannot be tested until qbar_XT/test-body response receives the same envelope treatment.",
        "derive_first": "derive qbar_XT as the test-body response analogue of Qbar_XH with no cancellation or measured-G smuggling",
        "fallback": "produce a nonclaim qbar_XT missing-input priority queue and arena tau handoff rows",
        "valid_for_claim": False,
    }]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4611 - `Qbar_XH` Full Source-Envelope Rollup Or First Source-Backed Input

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register row: `{CLAIM_ID}`

## Decision

`{DECISION}`

This checkpoint turns the previous `4604-4610` ladder into one source-side contract:

```text
|Q_tot_XH| <= |Q_bulk|_abs + |Q_edge|_abs + |Q_shadow|_abs
```

and therefore

```text
|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|_abs+|Q_edge|_abs+|Q_shadow|_abs)+|E_PiM_comm|)/M_lower.
```

That is a useful move, but it is not a pass. The source side is now organized; it is not yet numerically/source-backed.

## Source Register

{markdown_table(tables["sources"])}

## `Qbar_XH` Source-Envelope Theorem

{markdown_table(tables["theorem"])}

## Bulk Rollup

{markdown_table(tables["bulk"])}

## Edge Rollup

{markdown_table(tables["edge"])}

## Shadow Rollup

{markdown_table(tables["shadow"])}

## Denominator/Projector Firewall

{markdown_table(tables["denominator"])}

## First Source-Backed Priority Queue

{markdown_table(tables["priority"])}

## Product Handoff

{markdown_table(tables["product"])}

## Controls

{markdown_table(tables["controls"])}

## Claim Blockers

{markdown_table(tables["blockers"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Next Target

`{NEXT_TARGET}`

The best next move is the test-body analogue: build the `qbar_XT` response envelope so the product `Qbar_XH*qbar_XT/(Z_X M_H_ref m_T)` cannot hide an arbitrary coupling.

Private nonclaim. No GitHub action. No R10, PPN, clock, orbital, Newton, Maxwell or local-GR pass is claimed.
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 Formal Addendum 627 - `Qbar_XH` Full Source-Envelope Rollup

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

## Source Envelope

The source numerator is now held as the absolute-sum envelope

```text
Q_tot_XH := Q_bulk + Q_edge + Q_shadow
```

with

```text
|Q_tot_XH| <= |Q_bulk|_abs + |Q_edge|_abs + |Q_shadow|_abs.
```

The normalized source charge obeys

```text
|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|_abs+|Q_edge|_abs+|Q_shadow|_abs)+|E_PiM_comm|)/M_lower.
```

The exact-zero branch is therefore

```text
Q_bulk=Q_edge=Q_shadow=0,  M_lower>0,  and  E_PiM_comm=0.
```

## Non-Cancellation Rule

This addendum forbids three shortcuts:

```text
Q_bulk + Q_edge + Q_shadow cancellations,
division by symbolic M_lower,
and absorbing relative/range/species/time source residuals into measured G_N.
```

## Status

The source side is now structurally compact enough to be attacked. It remains nonclaim until the priority queue receives exact-zero or source-backed numeric rows.

Next target: `{NEXT_TARGET}`.
"""


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        })

    missing_sources = [row["source_id"] for row in tables["sources"] if not row["path_exists"] or not row["needle_found"]]
    add("VAL4611_00_sources_exist_and_needles_found", not missing_sources, "missing: " + ",".join(missing_sources) if missing_sources else "all cited paths/needles found")

    csv_paths = [
        SOURCE_REGISTER, THEOREM_CSV, QBULK_CSV, QEDGE_CSV, QSHADOW_CSV, DENOMINATOR_CSV, PRIORITY_CSV,
        PRODUCT_CSV, CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV,
    ]
    csv_details = []
    csv_ok = True
    for path in csv_paths:
        parsed = read_csv(path)
        csv_details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4611_01_csv_parse", csv_ok, ";".join(csv_details))

    theorem_text = "\n".join(str(row) for row in tables["theorem"])
    priority_text = "\n".join(str(row) for row in tables["priority"])
    denominator_text = "\n".join(str(row) for row in tables["denominator"])
    product_text = "\n".join(str(row) for row in tables["product"])
    add("VAL4611_02_full_source_formula", "|Q_tot_XH| <= |Q_bulk|_abs + |Q_edge|_abs + |Q_shadow|_abs" in theorem_text, "source numerator formula present")
    add("VAL4611_03_qbar_formula", "|Qbar_XH| <= (||Pi_M^H||" in theorem_text, "Qbar_XH projection formula present")
    add("VAL4611_04_denominator_firewall", "M_lower" in denominator_text and "E_PiM_comm" in denominator_text, "denominator/projector firewall present")
    add("VAL4611_05_priority_queue", "Phi_wall_Poynting_abs" in priority_text and "epsilon_source_shadow" in priority_text, "Poynting and source-shadow targets present")
    add("VAL4611_06_product_handoff", "qbar_XT_abs" in product_text and "ARENA_TESTING_NOT_READY" in product_text, "test-side handoff present")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "claim_pass", "empirical_pass_claimed"} and value is True:
                    all_false = False
    add("VAL4611_07_no_claim_true", all_false, "no generated row promotes a claim")
    add("VAL4611_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4611_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4611_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4611_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4611_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4611_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4611_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4611_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4611_OVERALL", all(row["status"] == "PASS" for row in rows), "4611 Qbar_XH full source-envelope rollup")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "theorem": theorem_rows(now),
        "bulk": bulk_rows(now),
        "edge": edge_rows(now),
        "shadow": shadow_rows(now),
        "denominator": denominator_rows(now),
        "priority": priority_rows(now),
        "product": product_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(THEOREM_CSV, tables["theorem"])
    write_csv(QBULK_CSV, tables["bulk"])
    write_csv(QEDGE_CSV, tables["edge"])
    write_csv(QSHADOW_CSV, tables["shadow"])
    write_csv(DENOMINATOR_CSV, tables["denominator"])
    write_csv(PRIORITY_CSV, tables["priority"])
    write_csv(PRODUCT_CSV, tables["product"])
    write_csv(CONTROL_CSV, tables["controls"])
    write_csv(BLOCKERS_CSV, tables["blockers"])
    write_csv(PROMOTION_CSV, tables["promotion"])
    write_csv(DECISION_CSV, tables["decision"])
    write_csv(STATUS_CSV, tables["status"])
    write_csv(NEXT_CSV, tables["next"])
    write_text(DOC_PATH, build_doc(now, tables))
    write_text(FORMAL_PATH, build_formal(now))
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## PPC4161 Local Addendum - Qbar_XH Full Source-Envelope Rollup

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The source-side local-response numerator is now compacted as `|Q_tot_XH| <= |Q_bulk|_abs + |Q_edge|_abs + |Q_shadow|_abs`, and the normalized charge is firewalled as `|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|_abs+|Q_edge|_abs+|Q_shadow|_abs)+|E_PiM_comm|)/M_lower`. This is a nonclaim rollup: it gives the route to derivation/source rows without allowing cancellation, symbolic denominators or measured-G absorption.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Qbar_XH Full Source-Envelope Rollup

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private local-GR packet now has one source-side object to attack: Qbar_XH. The first source-backed input queue is ordered as denominator/projector, edge shell, Poynting wall flux, source-shadow projector, retained currents, then action/nonvariational shadows. Next packet target is qbar_XT.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4611 validation failed: {failed}")
    print(f"4611 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
