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

CHECKPOINT = "4609"
CLAIM_ID = "L-451"
BRANCH_ID = "MTS_R2FR_Y5_QEDGE_SOURCE_WORLDTUBE_BOUNDARY_GATE_4609"
MARKER = "PPC4161_QEDGE_SOURCE_WORLDTUBE_BOUNDARY_ZERO_OR_SHELL_FLUX_FIRST_ROW_4609"
PACKET_MARKER = "PPC4161_PACKET_QEDGE_SOURCE_WORLDTUBE_BOUNDARY_GATE_4609"
DECISION = "QEDGE_WORLDTUBE_BOUNDARY_ZERO_OR_SHELL_FLUX_ROWS_READY_NONCLAIM"
NEXT_TARGET = "4610-Y5-R2FR-Qshadow-source-map-normal-form-zero-or-nonHilbert-first-row.md"

DOC_PATH = POST / "4609-Y5-R2FR-Qedge-source-worldtube-boundary-zero-or-shell-flux-first-row.md"
FORMAL_PATH = FORMAL / "625-PPC4161-Qedge-source-worldtube-boundary-zero-or-shell-flux-first-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4609_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4609_QEDGE_WORLDTUBE_BOUNDARY_THEOREM.csv"
SHELL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4609_QEDGE_REYNOLDS_SHELL_ROWS.csv"
BOUNDARY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4609_QEDGE_BOUNDARY_FLUX_ROWS.csv"
UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4609_QEDGE_QBARXH_UPDATE_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4609_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4609_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4609_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4609_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4609_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4609_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4609_VALIDATION.csv"

FORMAL_624 = FORMAL / "624-PPC4161-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md"
CSV_4608_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4608_NEXT_TARGET.csv"
CSV_4608_UPDATE = SOURCE_DIR / "P8_Y5_R2FR_4608_QBULK_RETAINED_UPDATE_ROWS.csv"
CSV_4605_QEDGE = SOURCE_DIR / "P8_Y5_R2FR_4605_QEDGE_COMPONENT_ROWS.csv"
CSV_4605_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4605_SOURCE_NUMERATOR_THEOREM.csv"
CSV_4588_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4588_REYNOLDS_SUPPORT_THEOREM.csv"
CSV_4588_CLAUSES = SOURCE_DIR / "P8_Y5_R2FR_4588_REGULAR_SUPPORT_ZERO_CLAUSES.csv"
CSV_4588_SHELL = SOURCE_DIR / "P8_Y5_R2FR_4588_REYNOLDS_SHELL_BOUND_ROWS.csv"
CSV_4586_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4586_SOURCE_WORLDTUBE_KERNEL_THEOREM.csv"
CSV_4586_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4586_SOURCE_WORLDTUBE_OPERATOR_VECTOR.csv"
CSV_4586_CLAUSES = SOURCE_DIR / "P8_Y5_R2FR_4586_ZERO_CERTIFICATE_CLAUSES.csv"
CSV_4576_WORLDTUBE = SOURCE_DIR / "P8_Y5_R2FR_4576_SAME_WORLDTUBE_LOCK_THEOREM.csv"
CSV_4572_SHELL = SOURCE_DIR / "P8_Y5_R2FR_4572_TRANSITION_SHELL_PROFILE_ROWS.csv"
CSV_2642_BOUND = SOURCE_DIR / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_COMPONENT_BOUND_PACK.csv"
CSV_2664_QBAR = SOURCE_DIR / "P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664_QBARXH_FIRST_SOURCE_ROW_NONCLAIM.csv"
CSV_2664_AUDIT = SOURCE_DIR / "P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664_ZERO_PROOF_AUDIT.csv"
CSV_2466_WORLDTUBE = SOURCE_DIR / "P8_Y5_SOURCE_BRIDGE_2466_WORLDTUBE_BRIDGE.csv"
CSV_2467_SURFACE = SOURCE_DIR / "P8_Y5_HILBERT_CURRENT_2467_WORLDTUBE_SURFACE_GATE.csv"
CSV_3427_BOUNDARY = SOURCE_DIR / "P8_Y5_R2FR_3427_BOUNDARY_FLUX_THEOREM.csv"
CSV_4217_COMPONENTS = SOURCE_DIR / "P8_Y5_R2FR_4217_BOUNDARY_FLUX_COMPONENTS.csv"
CSV_4314_RAD = SOURCE_DIR / "P8_Y5_R2FR_4314_BOUNDARY_FLUX_BOUND_ROW.csv"
CSV_4552_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4552_BOUNDARY_FLUX_OWNER_CONTRACT.csv"
CSV_4605_QSHADOW = SOURCE_DIR / "P8_Y5_R2FR_4605_QSHADOW_COMPONENT_ROWS.csv"

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
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(out)


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
        "claim": "4609 decomposes the Q_edge source numerator into Reynolds shell motion and Hamiltonian boundary/corner/reference flux; exact zero requires fixed q-basic source worldtube support, zero boundary trace/no birth shell, source-free no-flux collar and fixed reference/projector data in one parent branch.",
        "current_evidence": "Generated Q_edge theorem rows, Reynolds shell rows, boundary flux rows, Qbar_XH update rows, blockers, controls and validation.",
        "status": "Qedge_worldtube_boundary_zero_or_shell_flux_rows_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Calling a source compact or exterior by inspection while the support boundary, birth shell, sidewall/radiative flux, corner/reference class or fitted source mask still moves.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No R10, PPN, clock, orbital or local-GR claim until Q_edge, Q_shadow, denominator/projector, qbar_XT and arena kernels are exact zero or source-backed numeric rows.",
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
        ("SRC4609_00_4608_handoff", CSV_4608_NEXT, "4609-Y5-R2FR-Qedge-source-worldtube-boundary-zero-or-shell-flux-first-row.md", "4608 hands off to the Q_edge/source-worldtube boundary gate."),
        ("SRC4609_01_4608_qbar", CSV_4608_UPDATE, "QBR4608_2_QbarXH", "4608 keeps Q_edge open inside Qbar_XH."),
        ("SRC4609_02_4605_qedge_shell", CSV_4605_QEDGE, "QE4605_0_Reynolds_shell", "4605 names the Reynolds shell Q_edge component."),
        ("SRC4609_03_4605_qedge_boundary", CSV_4605_QEDGE, "QE4605_1_boundary_flux", "4605 names the boundary flux Q_edge component."),
        ("SRC4609_04_4605_qedge_total", CSV_4605_QEDGE, "QE4605_TOTAL", "4605 total Q_edge absolute envelope."),
        ("SRC4609_05_4605_edge_theorem", CSV_4605_THEOREM, "NUM4605_2_edge_zero", "4605 conditional edge zero theorem."),
        ("SRC4609_06_4588_reynolds", CSV_4588_THEOREM, "RST4588_0_Reynolds_identity", "4588 derives the Reynolds support boundary identity."),
        ("SRC4609_07_4588_zero_trace", CSV_4588_THEOREM, "RST4588_1_zero_trace_support", "4588 zero-trace/no-shell condition."),
        ("SRC4609_08_4588_shell_bound", CSV_4588_THEOREM, "RST4588_2_shell_bound", "4588 shell bound formula."),
        ("SRC4609_09_4588_clauses", CSV_4588_CLAUSES, "ZSR4588_6_bounded_test_functions", "4588 lists the regular support zero clauses."),
        ("SRC4609_10_4588_shell_rows", CSV_4588_SHELL, "RSB4588_5_total", "4588 gives shell bound input rows."),
        ("SRC4609_11_4586_kernel", CSV_4586_THEOREM, "SWK4586_2_operator_vector", "4586 source-worldtube operator vector fallback."),
        ("SRC4609_12_4586_boundary_birth", CSV_4586_VECTOR, "CKSW4586_1_E_boundary_birth", "4586 boundary birth operator component."),
        ("SRC4609_13_4586_support_clause", CSV_4586_CLAUSES, "ZC4586_2_regular_support", "4586 regular-support clause remains unsigned."),
        ("SRC4609_14_4576_worldtube", CSV_4576_WORLDTUBE, "SWL4576_1_same_worldtube_before_readout", "4576 same-worldtube-before-readout lock."),
        ("SRC4609_15_4576_lock", CSV_4576_WORLDTUBE, "SWL4576_4_lock_result", "4576 full source-lock contract."),
        ("SRC4609_16_4572_shell", CSV_4572_SHELL, "TS4572_metric_source_lift", "4572 keeps transition-shell source lift open."),
        ("SRC4609_17_2642_boundary", CSV_2642_BOUND, "SCB2642_3_eps_B_abs", "2642 boundary/source-worldtube residual bound."),
        ("SRC4609_18_2664_edge", CSV_2664_QBAR, "QXH2664_1_edge_charge", "2664 first Qbar source row carries edge charge."),
        ("SRC4609_19_2664_projector", CSV_2664_AUDIT, "SCZ2664_4_projector_boundary_zero", "2664 projector/boundary zero remains conditional."),
        ("SRC4609_20_2466_gauss", CSV_2466_WORLDTUBE, "WT2466_2_surface_independence", "2466 Gauss/worldtube surface independence condition."),
        ("SRC4609_21_2466_external", CSV_2466_WORLDTUBE, "WT2466_3_external_vacuum", "2466 external-vacuum compact-support clause."),
        ("SRC4609_22_2467_sideflux", CSV_2467_SURFACE, "WTG2467_0_surface_difference", "2467 side-flux surface-difference identity."),
        ("SRC4609_23_2467_exterior", CSV_2467_SURFACE, "WTG2467_4_external_vacuum", "2467 exterior local-zero condition up to boundary tails."),
        ("SRC4609_24_3427_flux", CSV_3427_BOUNDARY, "BFT3427_5_verdict", "3427 boundary-flux theorem verdict."),
        ("SRC4609_25_4217_components", CSV_4217_COMPONENTS, "BCB4217_6_M_H_ref", "4217 boundary component vector includes denominator/reference."),
        ("SRC4609_26_4314_rad", CSV_4314_RAD, "BF4314_1_energy_bound", "4314 radiative Poynting boundary flux bound."),
        ("SRC4609_27_4552_owner", CSV_4552_OWNER, "BF4552_4_contract_verdict", "4552 boundary flux owner contract verdict."),
        ("SRC4609_28_formal_624", FORMAL_624, "PPC4161_RETAINED_BULK_SOURCE_CURRENT_ZERO_OR_JDIRECT_JMEM_JREADOUT_FIRST_ROW_4608", "formal handoff from 4608."),
        ("SRC4609_29_next_qshadow", CSV_4605_QSHADOW, "QS4605_TOTAL", "Q_shadow is the next numerator gate after Q_edge."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in sources:
        source_line = line_of(path, needle)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "source_path": str(path),
            "source_line": source_line,
            "needle": needle,
            "path_exists": path.exists(),
            "needle_found": source_line > 0,
            "role": role,
            "generated_utc": now,
            "valid_for_claim": False,
        })
    return rows


def theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "QE4609_0_decomposition",
            "component": "Q_edge",
            "derived_relation": "Q_edge := Q_edge_Reynolds_shell + Q_edge_boundary_flux",
            "zero_condition": "Q_edge_Reynolds_shell=0 and Q_edge_boundary_flux=0 in the same parent branch",
            "fallback_bound": "|Q_edge|_abs <= |Q_edge_shell| + |Q_edge_boundary|",
            "current_status": "DERIVED_EDGE_SPLIT_NO_CANCELLATION",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "QE4609_1_reynolds_shell_zero",
            "component": "Q_edge_Reynolds_shell",
            "derived_relation": "For I_phi=int_W phi rho_H dV, the edge term is int_partialW phi rho_H^tr V_n dSigma + <phi,mu_birth>.",
            "zero_condition": "fixed q-basic collar, compact regular support, rho_H^tr|partialW=0, mu_birth=0 and bounded arena tests",
            "fallback_bound": "|Q_edge_shell| <= W_lambda_edge_max Phi_edge (rho_H_trace_norm V_n_bound + mu_birth_TV)",
            "current_status": "REYNOLDS_ZERO_OR_SHELL_BOUND_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "QE4609_2_boundary_flux_zero",
            "component": "Q_edge_boundary_flux",
            "derived_relation": "Boundary charge is the Hamiltonian/corner/reference/sidewall flux left after the source collar is separated from the bulk current.",
            "zero_condition": "proper compact generator, source-free exterior collar, fixed boundary/corner/reference class, no sidewall/radiative/source crossing and fixed projector",
            "fallback_bound": "|Q_edge_boundary| <= |B_X_flux|+|C_corner|+|E_reference_edge|+|F_side_source|+|F_rad|+|E_projector_edge|",
            "current_status": "BOUNDARY_ZERO_OR_FLUX_BOUND_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "QE4609_3_anti_circularity",
            "component": "worldtube/source normalization",
            "derived_relation": "W_H must be closure(supp J_H,total) before readout and M_H_ref must not be fitted from local GM/orbit residuals.",
            "zero_condition": "source support, boundary class, Pi_M and M_H_ref are parent-owned before arena scoring",
            "fallback_bound": "retain E_reference_edge, E_projector_edge and M_lower firewall rows",
            "current_status": "ANTI_CIRCULARITY_FIREWALL_ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "QE4609_4_Qbar_update",
            "component": "Qbar_XH source numerator",
            "derived_relation": "|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/M_lower",
            "zero_condition": "Q_bulk, Q_edge, Q_shadow and projector/denominator rows vanish or are source-backed in the same branch",
            "fallback_bound": "Q_edge_abs feeds the existing Qbar_XH absolute numerator envelope",
            "current_status": "QEDGE_INSERTED_QSHADOW_STILL_OPEN",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def shell_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "row_id": "QES4609_0_trace", "quantity": "rho_H_trace_norm", "definition": "int_partialW |rho_H^tr| dSigma", "zero_route": "Hilbert density has zero normal trace on the compact support edge", "bound_formula": "source-backed trace density or zero certificate", "current_status": "MISSING_ZERO_TRACE_CERTIFICATE_OR_VALUE", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QES4609_1_velocity", "quantity": "V_n_bound", "definition": "sup_partialW |V_n| under the source-vertical probe", "zero_route": "support boundary fixed by q-basic Hilbert source collar", "bound_formula": "source-backed normal support velocity", "current_status": "MISSING_SUPPORT_VARIATION_BOUND", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QES4609_2_birth", "quantity": "mu_birth_TV", "definition": "total variation norm of distributional source birth/death shell", "zero_route": "no source layer born or killed by the vertical probe", "bound_formula": "||mu_birth||_TV", "current_status": "MISSING_NO_SHELL_CERTIFICATE_OR_VALUE", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QES4609_3_test", "quantity": "Phi_edge", "definition": "sup_partialW |phi_edge| for the declared edge/source arena", "zero_route": "bounded arena kernels on the boundary collar", "bound_formula": "finite arena test ceiling", "current_status": "MISSING_ARENA_TEST_BOUND", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QES4609_4_kernel", "quantity": "W_lambda_edge_max", "definition": "finite-range kernel ceiling on the source boundary", "zero_route": "declared bounded kernel in the source collar", "bound_formula": "sup_partialW |W_lambda|", "current_status": "KERNEL_BOUND_SCHEMA_READY_VALUE_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QES4609_5_total", "quantity": "Q_edge_shell_abs", "definition": "Reynolds shell contribution to Q_edge", "zero_route": "rho_H_trace_norm=0 and mu_birth_TV=0 in same q-basic collar", "bound_formula": "|Q_edge_shell| <= W_lambda_edge_max Phi_edge (rho_H_trace_norm V_n_bound + mu_birth_TV)", "current_status": "FORMULA_READY_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
    ]


def boundary_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "row_id": "QEB4609_0_boundary_primitive", "quantity": "B_X_flux_abs", "definition": "Hamiltonian boundary primitive/source-normal flux amplitude", "zero_route": "proper compact generator and no boundary source charge in the collar", "bound_formula": "|B_X_flux|", "current_status": "BOUNDARY_PRIMITIVE_VALUE_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QEB4609_1_corner", "quantity": "C_corner_abs", "definition": "corner/boost/orientation/improvement edge class", "zero_route": "fixed boundary and corner convention; no live corner edge mode", "bound_formula": "|C_corner|", "current_status": "CORNER_CLASS_VALUE_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QEB4609_2_reference", "quantity": "E_reference_edge_abs", "definition": "reference subtraction or H_ref edge leakage", "zero_route": "same-frame reference and M_H_ref fixed before source variation", "bound_formula": "|E_reference_edge|", "current_status": "REFERENCE_EDGE_VALUE_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QEB4609_3_sidewall", "quantity": "F_side_source_abs", "definition": "matter/apparatus/source current crossing the side boundary", "zero_route": "no source crossing through the local collar sidewall", "bound_formula": "|F_side_source|", "current_status": "SIDEWALL_SOURCE_FLUX_VALUE_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QEB4609_4_radiative", "quantity": "F_rad_abs", "definition": "radiative EM/gravity/Poynting boundary flux through the collar", "zero_route": "closed stationary no-radiation collar or radiative flux routed into explicit EM/boundary row", "bound_formula": "|int_DeltaTau int_partialW S dot n dA dtau|", "current_status": "RADIATIVE_FLUX_VALUE_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QEB4609_5_projector", "quantity": "E_projector_edge_abs", "definition": "Pi_M/P_loc/projector edge commutator leakage", "zero_route": "projector fixed and commutes with boundary/reference variation", "bound_formula": "|E_projector_edge|", "current_status": "PROJECTOR_EDGE_VALUE_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QEB4609_6_total", "quantity": "Q_edge_boundary_abs", "definition": "total Hamiltonian boundary/corner/reference/sidewall/radiative edge contribution", "zero_route": "all boundary flux subcomponents vanish in one parent branch", "bound_formula": "|Q_edge_boundary| <= |B_X_flux|+|C_corner|+|E_reference_edge|+|F_side_source|+|F_rad|+|E_projector_edge|", "current_status": "FORMULA_READY_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
    ]


def update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "row_id": "QEU4609_0_edge_total", "quantity": "Q_edge_abs", "update_formula": "|Q_edge|_abs <= |Q_edge_shell| + |Q_edge_boundary|", "zero_condition": "Reynolds shell and boundary flux rows vanish in the same parent branch", "required_inputs": "Q_edge_shell_abs;Q_edge_boundary_abs", "current_status": "ABSOLUTE_SUM_SCHEMA_READY_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QEU4609_1_QbarXH", "quantity": "Qbar_XH_abs", "update_formula": "|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/M_lower", "zero_condition": "bulk, edge, shadow, denominator and projector rows all close", "required_inputs": "Q_bulk_abs;Q_edge_abs;Q_shadow_abs;Pi_M norm;E_PiM_comm;M_lower", "current_status": "QBARXH_STILL_BLOCKED_BY_QSHADOW_AND_DENOMINATOR", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QEU4609_2_product", "quantity": "I_X^ST(lambda)", "update_formula": "|I_X^ST| <= |Qbar_XH| |qbar_XT|/(4*pi |Z_X| G_N M_H_ref m_T)", "zero_condition": "Qbar_XH or qbar_XT zero, or all factors source-backed below arena bounds", "required_inputs": "Qbar_XH_abs;qbar_XT_abs;Z_X;M_H_ref;m_T;arena tau", "current_status": "PRODUCT_REMAINS_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4609_0_no_compact_slogan", "control": "Do not set Q_edge=0 by saying 'compact source'; require zero trace, no shell and no boundary flux.", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4609_1_no_fitted_GM", "control": "Do not choose W_H, M_H_ref or boundary class from fitted GM/orbital residuals.", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4609_2_no_cancellation", "control": "Use |Q_edge_shell|+|Q_edge_boundary|; no cancellation credit between edge subcomponents.", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4609_3_radiation_firewall", "control": "Radiative/Poynting flux is a boundary row unless the stationary closed collar is parent-signed.", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4609_4_no_claim_from_symbolic_rows", "control": "Symbolic Q_edge rows do not score R10, PPN, clocks, or orbits.", "valid_for_claim": False, "generated_utc": now},
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "blocker_id": "MIS4609_0_shell", "missing_object": "zero-trace/no-birth-shell certificate or numeric rho_H_trace_norm, V_n_bound, mu_birth_TV and Phi_edge", "why_it_matters": "support motion can create source charge even when bulk current is quiet", "best_next_action": "prove compact regular zero-trace source support or source shell profile rows", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "MIS4609_1_boundary_flux", "missing_object": "Hamiltonian boundary primitive, corner/reference, sidewall, radiative and projector edge values or zero theorem", "why_it_matters": "boundary flux is the exact loophole in exterior source coupling", "best_next_action": "prove no-flux fixed boundary collar or fill boundary component rows", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "MIS4609_2_worldtube_owner", "missing_object": "same parent-owned source worldtube and anti-circular M_H_ref/Pi_M support convention", "why_it_matters": "measured GM can otherwise hide the edge source charge", "best_next_action": "lock W_H=closure(supp J_H,total) before readout and bind M_H_ref to 4604 denominator rows", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "MIS4609_3_downstream", "missing_object": "Q_shadow, denominator/projector, qbar_XT and arena kernels", "why_it_matters": "Q_edge closure alone is not a local-GR/R10/PPN claim", "best_next_action": NEXT_TARGET, "valid_for_claim": False, "generated_utc": now},
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4609_0_sources", "promotion_requirement": "all cited sources exist and needles are found", "current_status": "PASS" if all(row["path_exists"] and row["needle_found"] for row in sources) else "FAIL", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4609_1_shell_zero", "promotion_requirement": "rho_H_trace_norm=0 and mu_birth_TV=0 in the same fixed q-basic collar", "current_status": "NOT_SATISFIED", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4609_2_boundary_zero", "promotion_requirement": "B_X_flux, C_corner, E_reference_edge, F_side_source, F_rad and E_projector_edge all zero or source-backed", "current_status": "NOT_SATISFIED_SYMBOLIC_ROWS_ONLY", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4609_3_empirical", "promotion_requirement": "Q_edge row joins Q_bulk/Q_shadow/denominator/qbar_XT/arena kernels before scoring", "current_status": "NOT_SATISFIED_DOWNSTREAM_OPEN", "valid_for_claim": False, "generated_utc": now},
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [{"checkpoint": CHECKPOINT, "branch": BRANCH_ID, "decision": DECISION, "reason": "Q_edge is now an auditable worldtube-boundary law: Reynolds shell plus Hamiltonian boundary flux, with anti-circularity and no-cancellation guards.", "valid_for_claim": False, "generated_utc": now}]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [{"checkpoint": CHECKPOINT, "branch": BRANCH_ID, "status": DECISION, "what_moved": "Q_edge changed from one placeholder into shell and boundary flux rows with exact zero clauses.", "what_did_not_move": "No R10/PPN/clock/orbit/local-GR pass; Q_shadow and numeric/source-backed edge values remain missing.", "valid_for_claim": False, "generated_utc": now}]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [{"checkpoint": CHECKPOINT, "branch": BRANCH_ID, "generated_utc": now, "next_target": NEXT_TARGET, "reason": "After bulk and edge numerator gates are split, Q_shadow is the remaining source-side numerator term blocking Qbar_XH.", "derive_first": "prove single source-map normal form: every shadow is parent action content, boundary/improvement, or absent; no post-Euler/nonvariational source block", "fallback": "fill Q_shadow_action, Q_shadow_projector and Q_shadow_nonvariational rows as nonclaim finite inputs", "valid_for_claim": False}]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4609 - `Q_edge` Source-Worldtube Boundary Zero Or Shell-Flux First Row

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register row: `{CLAIM_ID}`

## Decision

`{DECISION}`

This checkpoint goes after the source-edge route directly. The edge numerator is no longer "some boundary thing". It is split as:

```text
Q_edge := Q_edge_Reynolds_shell + Q_edge_boundary_flux.
```

The exact local-zero route is:

```text
rho_H^tr|partial W_H = 0,  mu_birth = 0,  B_X_flux=C_corner=E_reference_edge=F_side_source=F_rad=E_projector_edge=0
```

all in the same parent-owned source worldtube, before readout or fitted `GM` calibration.

The fallback is:

```text
|Q_edge|_abs <= |Q_edge_shell| + |Q_edge_boundary|.
```

## Source Register

{markdown_table(tables["sources"])}

## `Q_edge` Theorem Rows

{markdown_table(tables["theorem"])}

## Reynolds Shell Rows

{markdown_table(tables["shell"])}

## Boundary Flux Rows

{markdown_table(tables["boundary"])}

## `Qbar_XH` Update Rows

{markdown_table(tables["update"])}

## Controls

{markdown_table(tables["controls"])}

## Claim Blockers

{markdown_table(tables["blockers"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Next Target

`{NEXT_TARGET}`

Bulk is split and edge is now split; the remaining source-numerator fog bank is `Q_shadow`.

Private nonclaim. No R10, PPN, clock, orbital, Newton or local-GR pass is claimed.
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 Formal Addendum 625 - `Q_edge` Source-Worldtube Boundary Gate

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

## Edge Split

The source-edge numerator is

```text
Q_edge := Q_edge_Reynolds_shell + Q_edge_boundary_flux.
```

The Reynolds part is governed by

```text
D I_phi = int_partialW phi rho_H^tr V_n dSigma + <phi,mu_birth>
```

after the q-basic bulk term is separated. Hence

```text
|Q_edge_shell| <= W_lambda_edge_max Phi_edge (rho_H_trace_norm V_n_bound + mu_birth_TV).
```

The Hamiltonian boundary part is bounded by

```text
|Q_edge_boundary| <= |B_X_flux|+|C_corner|+|E_reference_edge|+|F_side_source|+|F_rad|+|E_projector_edge|.
```

Therefore

```text
|Q_edge|_abs <= |Q_edge_shell| + |Q_edge_boundary|.
```

## Status

This checkpoint does not claim edge silence. It creates the exact contract a future parent action must satisfy: same q-basic source worldtube, regular compact support, zero density trace/no birth shell, source-free no-flux collar, fixed corner/reference/projector data, and no fitted `GM` support definition.

Next target: `{NEXT_TARGET}`.
"""


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False})

    add("VAL4609_00_sources_exist", all(row["path_exists"] for row in tables["sources"]), "all cited source paths exist")
    missing_needles = [row["source_id"] for row in tables["sources"] if not row["needle_found"]]
    add("VAL4609_01_needles_found", not missing_needles, "missing needles: " + ",".join(missing_needles) if missing_needles else "all cited source needles found")
    csv_paths = [SOURCE_REGISTER, THEOREM_CSV, SHELL_CSV, BOUNDARY_CSV, UPDATE_CSV, CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    details = []
    csv_ok = True
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4609_02_csv_parse", csv_ok, ";".join(details))
    theorem_text = "\n".join(str(row) for row in tables["theorem"])
    shell_text = "\n".join(str(row) for row in tables["shell"])
    boundary_text = "\n".join(str(row) for row in tables["boundary"])
    update_text = "\n".join(str(row) for row in tables["update"])
    add("VAL4609_03_edge_split", "Q_edge := Q_edge_Reynolds_shell + Q_edge_boundary_flux" in theorem_text, "edge split present")
    add("VAL4609_04_shell_rows", "rho_H_trace_norm" in shell_text and "mu_birth_TV" in shell_text and "Q_edge_shell_abs" in shell_text, "Reynolds shell rows present")
    add("VAL4609_05_boundary_rows", "B_X_flux_abs" in boundary_text and "F_rad_abs" in boundary_text and "Q_edge_boundary_abs" in boundary_text, "boundary flux rows present")
    add("VAL4609_06_update_rows", "Q_edge_abs" in update_text and "Qbar_XH_abs" in update_text, "Qedge/Qbar update present")
    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "empirical_pass_claimed", "score_ready", "numeric_value_present", "claim_pass"} and value is True:
                    all_false = False
    add("VAL4609_07_no_claim_true", all_false, "no generated table promotes a claim")
    add("VAL4609_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4609_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4609_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4609_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4609_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4609_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4609_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4609_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4609_OVERALL", all(row["status"] == "PASS" for row in rows), "4609 Qedge source-worldtube boundary gate")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "theorem": theorem_rows(now),
        "shell": shell_rows(now),
        "boundary": boundary_rows(now),
        "update": update_rows(now),
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
    write_csv(SHELL_CSV, tables["shell"])
    write_csv(BOUNDARY_CSV, tables["boundary"])
    write_csv(UPDATE_CSV, tables["update"])
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
## PPC4161 Local Addendum - Qedge Source-Worldtube Boundary Gate

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The source-edge numerator is now split as `Q_edge := Q_edge_Reynolds_shell + Q_edge_boundary_flux`. Edge silence requires zero density trace/no birth shell and a fixed no-flux Hamiltonian boundary/corner/reference collar; otherwise `Q_edge_abs` is a non-cancelling shell-plus-boundary envelope feeding `Qbar_XH`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Qedge Source-Worldtube Boundary Gate

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private packet now treats support motion, birth shells, sidewall/radiative flux, corner/reference terms and projector edge leakage as explicit Q_edge rows. The next numerator gate is Q_shadow.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4609 validation failed: {failed}")
    print(f"4609 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
