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

CHECKPOINT = "4605"
CLAIM_ID = "L-447"
BRANCH_ID = "MTS_R2FR_Y5_QBULK_QEDGE_QSHADOW_NUMERATOR_GATE_4605"
MARKER = "PPC4161_QBULK_QEDGE_QSHADOW_SOURCE_CURRENT_ZERO_OR_QBARXH_COMPONENT_FIRST_FILL_4605"
PACKET_MARKER = "PPC4161_PACKET_QBULK_QEDGE_QSHADOW_NUMERATOR_GATE_4605"
DECISION = "SOURCE_NUMERATOR_ZERO_OR_COMPONENT_BOUND_SCHEMA_READY_NONCLAIM"
NEXT_TARGET = "4606-Y5-R2FR-Qbulk-Hilbert-EM-Poynting-source-current-zero-or-first-coefficient-row.md"

DOC_PATH = POST / "4605-Y5-R2FR-Qbulk-Qedge-Qshadow-source-current-zero-or-QbarXH-component-first-fill.md"
FORMAL_PATH = FORMAL / "621-PPC4161-Qbulk-Qedge-Qshadow-source-current-zero-or-QbarXH-component-first-fill.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4605_SOURCE_REGISTER.csv"
NUMERATOR_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4605_SOURCE_NUMERATOR_THEOREM.csv"
BULK_COMPONENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4605_QBULK_COMPONENT_ROWS.csv"
EDGE_COMPONENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4605_QEDGE_COMPONENT_ROWS.csv"
SHADOW_COMPONENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4605_QSHADOW_COMPONENT_ROWS.csv"
QBAR_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4605_QBARXH_NUMERATOR_UPDATE_ROWS.csv"
PRODUCT_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4605_IXST_PRODUCT_UPDATE_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4605_CLAIM_BLOCKERS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4605_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4605_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4605_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4605_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4605_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4605_VALIDATION.csv"

DOC_4604 = POST / "4604-Y5-R2FR-MHref-PiM-denominator-lock-or-QbarXH-first-fill.md"
FORMAL_620 = FORMAL / "620-PPC4161-MHref-PiM-denominator-lock-or-QbarXH-first-fill.md"
CSV_4604_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4604_NEXT_TARGET.csv"
CSV_4604_QBAR = SOURCE_DIR / "P8_Y5_R2FR_4604_QBARXH_FIRST_FILL_ROWS.csv"
CSV_4604_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4604_CLAIM_BLOCKERS.csv"
CSV_4604_PRODUCT = SOURCE_DIR / "P8_Y5_R2FR_4604_IXST_PRODUCT_UPDATE_ROWS.csv"
CSV_2664_QBAR = SOURCE_DIR / "P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664_QBARXH_FIRST_SOURCE_ROW_NONCLAIM.csv"
CSV_2664_ZERO = SOURCE_DIR / "P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664_ZERO_PROOF_AUDIT.csv"
CSV_2664_RUNNER = SOURCE_DIR / "P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664_SOURCE_CURRENT_RUNNER_RESULTS.csv"
CSV_2642_PROOF = SOURCE_DIR / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_PROOF_ATTEMPT.csv"
CSV_2642_BOUND = SOURCE_DIR / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_COMPONENT_BOUND_PACK.csv"
CSV_2617_IDENTITY = SOURCE_DIR / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SINGLE_SOURCE_MAP_IDENTITY_THEOREM.csv"
CSV_2617_SHADOW = SOURCE_DIR / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SOURCE_SHADOW_ZERO_ATTEMPT.csv"
CSV_4520_SILENCE = SOURCE_DIR / "P8_Y5_R2FR_4520_RANK_ZERO_SOURCE_CURRENT_SILENCE_THEOREM.csv"
CSV_4530_DESCENT = SOURCE_DIR / "P8_Y5_R2FR_4530_SOURCE_CURRENT_DESCENT_IDENTITY.csv"
CSV_4569_COVARIANCE = SOURCE_DIR / "P8_Y5_R2FR_4569_SOURCE_CURRENT_COVARIANCE_THEOREM.csv"
CSV_4514_TAILS = SOURCE_DIR / "P8_Y5_R2FR_4514_REMAINING_SOURCE_TAIL_LEDGER.csv"
CSV_4587_DENSITY = SOURCE_DIR / "P8_Y5_R2FR_4587_DENSITY_QBASIC_THEOREM.csv"
CSV_4587_POYNTING = SOURCE_DIR / "P8_Y5_R2FR_4587_POYNTING_OWNER_LOCK.csv"
CSV_4588_REYNOLDS = SOURCE_DIR / "P8_Y5_R2FR_4588_REYNOLDS_SUPPORT_THEOREM.csv"
CSV_EM_ELLJ = SOURCE_DIR / "P8_EM_ellJ_source_current_owner_residual_law.csv"
CSV_WARD_CONTRACT = SOURCE_DIR / "P8_source_current_Ward_universality_CONTRACT.csv"
CSV_WARD_BRIDGE = SOURCE_DIR / "P8_Y5_SOURCE_CURRENT_WARD_BRIDGE.csv"
CSV_4440_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4440_SOURCE_CHARGE_CLOSURE_OUTPUT.csv"

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
        lines.append("| " + " | ".join(str(row.get(key, "")).replace("\n", " ").replace("|", "\\|") for key in headers) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    write_text(path, text.rstrip() + "\n\n" + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--short"], capture_output=True, text=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


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
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4605 decomposes the Qbar_XH numerator into bulk Hilbert/EM/Poynting source current, edge/worldtube-boundary charge, and shadow/non-Hilbert source-map charge; exact zero requires all three to vanish in the same parent branch, otherwise Qbar_XH uses a no-cancellation component envelope.",
        "current_evidence": "Generated source numerator theorem rows, Q_bulk/Q_edge/Q_shadow component rows, Qbar_XH numerator update rows, I_X^ST product update rows, blockers, controls and validation.",
        "status": "source_numerator_zero_or_component_bound_schema_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Using Ward conservation, Poynting bookkeeping, boundary falloff, or source-map identity as if they zero the full numerator without same-branch parent signatures.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No R10, PPN, clock, orbital or local-GR claim until Q_bulk/Q_edge/Q_shadow, denominator/projector, qbar_XT and arena kernels are exact zero or source-backed numeric rows.",
    }
    rows.append({key: row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4605_00_4604_doc", DOC_4604, "Q_bulk+Q_edge+Q_shadow", "4604 selected source numerator as next target."),
        ("SRC4605_01_620_formal", FORMAL_620, "|Qbar_XH|", "formal Qbar bound handoff."),
        ("SRC4605_02_4604_next", CSV_4604_NEXT, "4605-Y5-R2FR-Qbulk-Qedge-Qshadow-source-current-zero-or-QbarXH-component-first-fill.md", "machine next target."),
        ("SRC4605_03_4604_qbar", CSV_4604_QBAR, "QF4604_1_absolute_Qbar_bound", "Qbar numerator envelope requiring components."),
        ("SRC4605_04_4604_blocker", CSV_4604_BLOCKERS, "MIS4604_2_Q_components", "component blocker."),
        ("SRC4605_05_4604_product", CSV_4604_PRODUCT, "PU4604_0_I_product_update", "I product update."),
        ("SRC4605_06_2664_bulk", CSV_2664_QBAR, "QXH2664_0_bulk_source_current", "old Q_bulk source row."),
        ("SRC4605_07_2664_edge", CSV_2664_QBAR, "QXH2664_1_edge_charge", "old Q_edge source row."),
        ("SRC4605_08_2664_shadow", CSV_2664_QBAR, "QXH2664_2_shadow_source", "old Q_shadow source row."),
        ("SRC4605_09_2664_zero", CSV_2664_ZERO, "SCZ2664_7_verdict", "source-current zero verdict."),
        ("SRC4605_10_2664_runner", CSV_2664_RUNNER, "RUN2664_QXH2664_2_shadow_source", "runner rejects unfilled components."),
        ("SRC4605_11_2642_JH", CSV_2642_PROOF, "SCI2642_1_JH_descent", "Hilbert current descent."),
        ("SRC4605_12_2642_JNH", CSV_2642_PROOF, "SCI2642_2_JNH_channels", "non-Hilbert/shadow source component."),
        ("SRC4605_13_2642_boundary", CSV_2642_PROOF, "SCI2642_3_boundary", "boundary edge component."),
        ("SRC4605_14_2642_bound", CSV_2642_BOUND, "SCB2642_7_no_cancellation_policy", "component no-cancellation policy."),
        ("SRC4605_15_2617_identity", CSV_2617_IDENTITY, "SMI2617_2_shadow_trichotomy", "source-shadow trichotomy."),
        ("SRC4605_16_2617_shadow", CSV_2617_SHADOW, "SSZ2617_4_current_verdict", "shadow zero verdict."),
        ("SRC4605_17_4520_poynting", CSV_4520_SILENCE, "RZSC4520_3_poynting", "EM/Poynting zero route."),
        ("SRC4605_18_4530_full", CSV_4530_DESCENT, "J4530_0_full_variation_decomposition", "full source current chain rule."),
        ("SRC4605_19_4569_standard", CSV_4569_COVARIANCE, "SC4569_5_Asrc_standard_zero", "conditional standard source zero."),
        ("SRC4605_20_4514_tails", CSV_4514_TAILS, "STL4514_3_Jmem", "live direct/source current tail."),
        ("SRC4605_21_4587_density", CSV_4587_DENSITY, "DQT4587_1_qbasic_density_zero", "density q-basic zero."),
        ("SRC4605_22_4587_poynting", CSV_4587_POYNTING, "Poynting", "Poynting owner lock."),
        ("SRC4605_23_4588_shell", CSV_4588_REYNOLDS, "RST4588_2_shell_bound", "edge/support shell bound."),
        ("SRC4605_24_EM_ellJ", CSV_EM_ELLJ, "EJR3513_2_R_Ward", "EM/Ward/source-current owner residual."),
        ("SRC4605_25_Ward_contract", CSV_WARD_CONTRACT, "SC4_no_nonHilbert_source_current", "Ward universality source contract."),
        ("SRC4605_26_Ward_bridge", CSV_WARD_BRIDGE, "WB520_4_exact_product_obstruction", "projection commutator obstruction."),
        ("SRC4605_27_4440_source", CSV_4440_SOURCE, "SOURCE_CHARGE_REDUCED_TO_ACTION_MEASURE_CURRENT_CONTRACT", "source-charge action-measure context."),
        ("SRC4605_28_claim_446", CLAIMS_PATH, "L-446", "claim-register handoff from 4604."),
    ]
    rows = []
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


def numerator_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NUM4605_0_decomposition",
            "statement": "The Qbar_XH numerator splits into bulk, edge and shadow pieces before projection.",
            "formula": "Q_tot_XH(lambda)=Q_bulk_XH(lambda)+Q_edge_XH(lambda)+Q_shadow_XH(lambda)",
            "derivation": "Use the 2664 Qbar row, the 2642 source-current identity stack, and the 2617 source-shadow trichotomy.",
            "consequence": "There is no allowed cancellation credit between bulk, edge and shadow channels.",
            "status": "NUMERATOR_SPLIT_DERIVED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NUM4605_1_bulk_zero",
            "statement": "Bulk source current vanishes only on the same q-basic ordinary-source branch, including EM/Poynting stress.",
            "formula": "Q_bulk=0 if D_v S_src=0, Dq[v_X]=0, Lie_v theta=0, no direct source weights, and stationary no-flux EM/Poynting support",
            "derivation": "Apply the chain rule to S_src=Sbar_src[q(Phi),Psi,A,theta]; Poynting is treated as Hilbert EM stress flux, not a separate magic source.",
            "consequence": "Poynting enters the source-current proof honestly: it zeroes only as Hilbert EM stress with no-flux/support conditions, otherwise it is bounded.",
            "status": "CONDITIONAL_BULK_ZERO_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NUM4605_2_edge_zero",
            "statement": "Edge/source-worldtube charge vanishes only with compact regular support, zero trace/no shell, proper boundary generator and fixed reference/projector data.",
            "formula": "Q_edge=0 if rho_H trace on boundary=0, shell birth measure=0, boundary flux=0, and reference/corner/projector edge terms are silent",
            "derivation": "Combine the 4588 Reynolds identity with the 2642 boundary leg and the 4604 fixed denominator/projector firewall.",
            "consequence": "Boundary/source-wall motion is not erased by calling the source compact; it needs the zero-trace/no-shell/proper-boundary clauses.",
            "status": "CONDITIONAL_EDGE_ZERO_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NUM4605_3_shadow_zero",
            "statement": "Shadow source charge is zero only if the parent admits a single identity source map and no non-Hilbert/projector/source-shadow residual block.",
            "formula": "Q_shadow=0 if T_active=T_H, every DeltaS shadow is reclassified as real parent content or boundary-improvement, and nonvariational conserved blocks are absent",
            "derivation": "Use the 2617 trichotomy: a shadow is an action term, boundary/improvement term, or nonvariational/separately conserved residual requiring a bound.",
            "consequence": "The source-shadow route is squeezed into explicit parent-action grammar or finite residuals; it cannot hide as an RHS knob.",
            "status": "CONDITIONAL_SHADOW_ZERO_THEOREM_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "NUM4605_4_absolute_numerator_bound",
            "statement": "If any zero clause is unsigned, the numerator is bounded componentwise.",
            "formula": "|Q_tot_XH| <= |Q_bulk|_abs + |Q_edge|_abs + |Q_shadow|_abs",
            "derivation": "Triangle inequality; cancellations between ordinary Hilbert, Poynting, edge and shadow pieces are forbidden.",
            "consequence": "4605 gives Qbar_XH a real numerator envelope ready for coefficient filling.",
            "status": "BOUND_FORMULA_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def bulk_component_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "component_id": "QB4605_0_Hilbert",
            "component": "Q_bulk_Hilbert",
            "zero_route": "S_src descends through q, Dq[v_X]=0, Lie_v theta=0, no source-only weights",
            "bound_formula": "|Q_bulk_H| <= W_lambda_max M_ref epsilon_JH_X",
            "required_inputs": "common matter action; no-marker theorem; source weight ban; J_H_ref; W_lambda_max",
            "current_status": "CONDITIONAL_ZERO_VALUES_MISSING",
            "units": "parent_X_charge",
            "source_paths": f"{CSV_2642_PROOF}; {CSV_4530_DESCENT}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "component_id": "QB4605_1_EM_Poynting",
            "component": "Q_bulk_EM_Poynting",
            "zero_route": "EM action is q-basic and Poynting flux through the source worldtube wall vanishes or is stationary/topological",
            "bound_formula": "|Q_bulk_EM| <= W_lambda_max (|epsilon_EM_source| + |Phi_wall_Poynting| + |epsilon_Hodge|)",
            "required_inputs": "same Hodge/coframe; EM stress owner; wall flux bound; support/kernel units",
            "current_status": "POYNTING_ZERO_CONDITIONAL_BOUND_VALUES_MISSING",
            "units": "parent_X_charge",
            "source_paths": f"{CSV_4520_SILENCE}; {CSV_4587_DENSITY}; {CSV_EM_ELLJ}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "component_id": "QB4605_2_retained",
            "component": "Q_bulk_retained",
            "zero_route": "no direct retained source current, no memory kernel source slot, no material/readout source marker",
            "bound_formula": "|Q_bulk_retained| <= W_lambda_max (|J_direct|+|J_mem|+|J_marker|+|J_readout|)",
            "required_inputs": "retained current inventory; memory/source kernel rows; readout-before-variation proof or bounds",
            "current_status": "RETAINED_SOURCE_TAIL_VALUES_MISSING",
            "units": "parent_X_charge",
            "source_paths": f"{CSV_4514_TAILS}; {CSV_2642_PROOF}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "component_id": "QB4605_TOTAL",
            "component": "Q_bulk_abs",
            "zero_route": "all bulk components vanish in the same parent branch",
            "bound_formula": "|Q_bulk|_abs <= |Q_bulk_Hilbert|+|Q_bulk_EM_Poynting|+|Q_bulk_retained|",
            "required_inputs": "component zeros or source-backed numeric bounds",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "units": "parent_X_charge",
            "source_paths": f"{CSV_2664_QBAR}; {CSV_4520_SILENCE}; {CSV_4530_DESCENT}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def edge_component_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "component_id": "QE4605_0_Reynolds_shell",
            "component": "Q_edge_Reynolds_shell",
            "zero_route": "zero source-density trace on boundary and no birth/death shell",
            "bound_formula": "|Q_edge_shell| <= W_lambda_max (int_boundary |rho_H_trace| |V_n| dSigma + ||mu_birth||_TV)",
            "required_inputs": "trace density; normal support velocity; shell measure; arena kernel ceiling",
            "current_status": "SHELL_BOUND_FORM_VALUES_MISSING",
            "units": "parent_X_charge",
            "source_paths": f"{CSV_4588_REYNOLDS}; {CSV_2642_PROOF}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "component_id": "QE4605_1_boundary_flux",
            "component": "Q_edge_boundary_flux",
            "zero_route": "proper compact generator and no Hamiltonian boundary/corner charge in the source collar",
            "bound_formula": "|Q_edge_boundary| <= |B_X_flux| + |C_corner| + |E_reference_edge|",
            "required_inputs": "boundary primitive; corner class; source/reference edge lock",
            "current_status": "BOUNDARY_FLUX_VALUES_MISSING",
            "units": "parent_X_charge",
            "source_paths": f"{CSV_2642_BOUND}; {CSV_2664_ZERO}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "component_id": "QE4605_TOTAL",
            "component": "Q_edge_abs",
            "zero_route": "all edge/shell/boundary pieces vanish in the same parent branch",
            "bound_formula": "|Q_edge|_abs <= |Q_edge_shell| + |Q_edge_boundary|",
            "required_inputs": "shell and boundary flux zeros or source-backed bounds",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "units": "parent_X_charge",
            "source_paths": f"{CSV_2664_QBAR}; {CSV_4588_REYNOLDS}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def shadow_component_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "component_id": "QS4605_0_action_shadow",
            "component": "Q_shadow_action",
            "zero_route": "every apparent shadow is reclassified as ordinary parent action content already counted in bulk or forbidden by object language",
            "bound_formula": "|Q_shadow_action| <= |delta DeltaS_shadow/delta X|",
            "required_inputs": "parent action normal-form inventory; classification of every DeltaS candidate",
            "current_status": "PARENT_ACTION_CLASSIFICATION_MISSING",
            "units": "parent_X_charge",
            "source_paths": f"{CSV_2617_IDENTITY}; {CSV_2617_SHADOW}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "component_id": "QS4605_1_projector_shadow",
            "component": "Q_shadow_projector",
            "zero_route": "post-variation material/source projector equals identity or is fixed q-basic before readout",
            "bound_formula": "|Q_shadow_projector| <= ||P_material-I|| ||T_H|| + |E_projector_source|",
            "required_inputs": "identity source-map proof; projector norm; source-current commutator bound",
            "current_status": "PROJECTOR_SHADOW_ZERO_OR_BOUND_MISSING",
            "units": "parent_X_charge",
            "source_paths": f"{CSV_2617_SHADOW}; {CSV_WARD_BRIDGE}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "component_id": "QS4605_2_nonvariational_shadow",
            "component": "Q_shadow_nonvariational",
            "zero_route": "nonvariational independently conserved source blocks are absent",
            "bound_formula": "|Q_shadow_nonvar| <= |Q_conserved_extra| + |Q_inconsistency_repair|",
            "required_inputs": "Bianchi/Noether rejection or separately conserved residual inventory and bound",
            "current_status": "NONVARIATIONAL_BLOCK_ABSENCE_MISSING",
            "units": "parent_X_charge",
            "source_paths": f"{CSV_2617_IDENTITY}; {CSV_WARD_CONTRACT}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "component_id": "QS4605_TOTAL",
            "component": "Q_shadow_abs",
            "zero_route": "all shadow routes are absent, reclassified or boundary-silent in the same branch",
            "bound_formula": "|Q_shadow|_abs <= |Q_shadow_action|+|Q_shadow_projector|+|Q_shadow_nonvariational|",
            "required_inputs": "shadow component zeros or source-backed numeric bounds",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "units": "parent_X_charge",
            "source_paths": f"{CSV_2664_QBAR}; {CSV_2617_SHADOW}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def qbar_update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QU4605_0_numerator_abs",
            "quantity": "Q_tot_XH_abs",
            "formula": "|Q_tot_XH| <= |Q_bulk|_abs + |Q_edge|_abs + |Q_shadow|_abs",
            "required_inputs": "Q_bulk_abs; Q_edge_abs; Q_shadow_abs",
            "current_status": "BOUND_FORMULA_DERIVED_VALUES_MISSING",
            "numeric_value": "MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QU4605_1_Qbar_insert",
            "quantity": "Qbar_XH_abs",
            "formula": "|Qbar_XH| <= (||Pi_M^H|| Q_tot_XH_abs + |E_PiM_comm|)/M_lower",
            "required_inputs": "4604 denominator/projector rows plus Q_tot_XH_abs",
            "current_status": "QBAR_SCHEMA_REFINED_VALUES_MISSING",
            "numeric_value": "MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def product_update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "PU4605_0_I_product_source_insert",
            "quantity": "|I_X^ST|",
            "updated_formula": "|I_X^ST| <= ((||Pi_M|| Q_tot_XH_abs + |E_PiM_comm|)/M_lower) qbar_XT_abs/(4*pi |Z_X| G_N m_T)",
            "current_status": "PRODUCT_SCHEMA_REFINED_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "PU4605_1_zero_route",
            "quantity": "I_X^ST zero",
            "updated_formula": "if Q_bulk=Q_edge=Q_shadow=0 or qbar_XT=0 in the same branch, then I_X^ST=0",
            "current_status": "CONDITIONAL_ZERO_ROUTE_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4605_0_Qbulk",
            "missing_object": "Q_bulk Hilbert/EM/Poynting/retained component zeros or bounds",
            "why_it_matters": "bulk source current is the dominant numerator route and includes the Poynting/EM stress question",
            "best_next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4605_1_Qedge",
            "missing_object": "Q_edge shell/boundary/corner/reference zero or bound rows",
            "why_it_matters": "source-worldtube edge charge can mimic a local residual even if bulk current descends",
            "best_next_action": "fill shell trace, wall velocity, boundary flux and corner/reference rows",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4605_2_Qshadow",
            "missing_object": "Q_shadow action/projector/nonvariational classification and bounds",
            "why_it_matters": "shadow source maps are the route by which a hidden coupling can re-enter after Hilbert descent",
            "best_next_action": "classify every source-shadow candidate against parent action grammar",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4605_3_denominator_test_arena",
            "missing_object": "M_lower/Pi_M, qbar_XT, K_X, tau_R10 and empirical arena rows",
            "why_it_matters": "a numerator envelope alone is not a local-GR or R10 pass",
            "best_next_action": "return to denominator/test/arena rows after numerator components are live",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4605_0_no_cancellation",
            "control": "Bulk, edge and shadow components are absolute-summed; no cancellation is credited.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4605_1_poynting_not_magic",
            "control": "Poynting is handled as Hilbert EM stress flux or a bounded wall/source term, not an untracked background-field escape hatch.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4605_2_shadow_no_rhs_knob",
            "control": "A source shadow must be parent action content, boundary/improvement content, or a finite residual; it cannot be a hidden RHS knob.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4605_3_no_claim_from_schema",
            "control": "Q numerator component schemas do not imply empirical success without numeric/source-backed rows.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4605_0_bulk",
            "promotion_requirement": "Q_bulk_Hilbert, Q_bulk_EM_Poynting and Q_bulk_retained are zero or bounded with source-backed rows.",
            "current_status": "FAIL_QBULK_VALUES_MISSING",
            "source_count": len(sources),
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4605_1_edge",
            "promotion_requirement": "Q_edge shell and boundary/corner/reference pieces are zero or bounded.",
            "current_status": "FAIL_QEDGE_VALUES_MISSING",
            "source_count": len(sources),
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4605_2_shadow",
            "promotion_requirement": "Q_shadow action/projector/nonvariational pieces are eliminated or source-backed.",
            "current_status": "FAIL_QSHADOW_VALUES_MISSING",
            "source_count": len(sources),
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4605_3_Qbar_product",
            "promotion_requirement": "Q_tot_XH_abs plus 4604 denominator/projector plus qbar/arena rows make I_X^ST claim-ready.",
            "current_status": "FAIL_DOWNSTREAM_INPUTS_MISSING",
            "source_count": len(sources),
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
            "decision": DECISION,
            "reason": "The source numerator is now decomposed into bulk, edge and shadow zero/bound routes, but no component has claim-grade numeric/source-backed values.",
            "claim": "no R10/PPN/local-GR pass",
            "next_target": NEXT_TARGET,
            "generated_utc": now,
            "valid_for_claim": False,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "status": DECISION,
            "what_moved": "The source coupling numerator is now a concrete three-piece object: bulk Hilbert/EM/Poynting, edge/source-worldtube, and shadow/source-map residuals.",
            "what_did_not_move": "No numeric source amplitude, R10 alpha, PPN residual or local-GR pass is claimed.",
            "generated_utc": now,
            "valid_for_claim": False,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "Q_bulk is the largest and most physical numerator route, and it contains the Hilbert/EM/Poynting source-current question.",
            "derive_first": "prove Q_bulk_Hilbert and Q_bulk_EM_Poynting vanish under one q-basic source functor/no-flux branch",
            "fallback": "fill Q_bulk_Hilbert_abs, Q_bulk_EM_Poynting_abs and Q_bulk_retained_abs as nonclaim coefficient rows",
            "valid_for_claim": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4605 - Y5 R2FR Qbulk/Qedge/Qshadow Source-Current Zero Or QbarXH Component First Fill

Generated: `{now}`

Marker: `{MARKER}`
Branch: `{BRANCH_ID}`
Claim register row: `{CLAIM_ID}`
Previous target: `{DOC_4604}`

## Result

4604 locked the denominator/projector side of `Qbar_XH`. 4605 now opens the numerator itself:

```text
Q_tot_XH(lambda) = Q_bulk_XH(lambda) + Q_edge_XH(lambda) + Q_shadow_XH(lambda).
```

The strict clean route is:

```text
Q_bulk = 0,
Q_edge = 0,
Q_shadow = 0
    => Q_tot_XH = 0
    => Qbar_XH = 0
```

provided the 4604 denominator/projector clauses also hold.

If any zero clause is unsigned, the nonclaim numerator row is:

```text
|Q_tot_XH| <= |Q_bulk|_abs + |Q_edge|_abs + |Q_shadow|_abs.
```

Then 4604 inserts it into:

```text
|Qbar_XH| <= (||Pi_M^H|| Q_tot_XH_abs + |E_PiM_comm|)/M_lower.
```

Important: the bulk route now explicitly includes EM/Poynting stress. Poynting is not hand-waved as a background field; it is either Hilbert EM stress flux with stationary/no-flux support, or a bounded source-wall/current term.

## Private Decision

`{DECISION}`

No R10, PPN, clock, orbital, EM, Newton or local-GR pass is claimed. The immediate best target is `{NEXT_TARGET}`.

## Source Register

{markdown_table(tables["sources"])}

## Source Numerator Theorem

{markdown_table(tables["numerator_theorem"])}

## Qbulk Component Rows

{markdown_table(tables["bulk_components"])}

## Qedge Component Rows

{markdown_table(tables["edge_components"])}

## Qshadow Component Rows

{markdown_table(tables["shadow_components"])}

## QbarXH Numerator Update Rows

{markdown_table(tables["qbar_update"])}

## IXST Product Update Rows

{markdown_table(tables["product_update"])}

## Claim Blockers

{markdown_table(tables["blockers"])}

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
    return f"""# PPC4161 621 - Qbulk/Qedge/Qshadow Source-Current Zero Or QbarXH Component First Fill

Generated: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Claim register: `{CLAIM_ID}`

## Formal Statement

The source-side numerator is decomposed before projection:

```text
Q_tot_XH(lambda)=Q_bulk_XH(lambda)+Q_edge_XH(lambda)+Q_shadow_XH(lambda).
```

Bulk zero requires source-functor descent, verticality, no marker/source weights, and EM/Poynting Hilbert-stress no-flux support:

```text
Q_bulk=0 on the same q-basic ordinary-source plus EM/Poynting branch.
```

Edge zero requires regular support and boundary/reference silence:

```text
Q_edge=0 when boundary trace, shell birth, boundary flux, corner and reference edge terms vanish.
```

Shadow zero requires identity source map and no hidden non-Hilbert/projector source:

```text
Q_shadow=0 when every source shadow is absent, reclassified as parent action content, or boundary-silent.
```

Fallback:

```text
|Q_tot_XH| <= |Q_bulk|_abs + |Q_edge|_abs + |Q_shadow|_abs.
```

Inserted into 4604:

```text
|Qbar_XH| <= (||Pi_M^H|| Q_tot_XH_abs + |E_PiM_comm|)/M_lower.
```

Private nonclaim. The next target is `{NEXT_TARGET}`.
"""


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False})

    add("VAL4605_00_sources_exist", all(row["path_exists"] for row in tables["sources"]), "all cited source paths exist")
    missing_needles = [row["source_id"] for row in tables["sources"] if not row["needle_found"]]
    add("VAL4605_01_needles_found", not missing_needles, "missing needles: " + ",".join(missing_needles) if missing_needles else "all cited source needles found")

    csv_paths = [SOURCE_REGISTER, NUMERATOR_THEOREM_CSV, BULK_COMPONENT_CSV, EDGE_COMPONENT_CSV, SHADOW_COMPONENT_CSV, QBAR_UPDATE_CSV, PRODUCT_UPDATE_CSV, BLOCKERS_CSV, CONTROL_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    details = []
    csv_ok = True
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4605_02_csv_parse", csv_ok, ";".join(details))

    theorem_text = "\n".join(str(row) for row in tables["numerator_theorem"])
    bulk_text = "\n".join(str(row) for row in tables["bulk_components"])
    edge_text = "\n".join(str(row) for row in tables["edge_components"])
    shadow_text = "\n".join(str(row) for row in tables["shadow_components"])
    qbar_text = "\n".join(str(row) for row in tables["qbar_update"])
    add("VAL4605_03_numerator_split", "Q_bulk_XH" in theorem_text and "Q_edge_XH" in theorem_text and "Q_shadow_XH" in theorem_text, "numerator split present")
    add("VAL4605_04_poynting_in_bulk", "Q_bulk_EM_Poynting" in bulk_text and "Poynting" in theorem_text, "EM/Poynting routed through bulk")
    add("VAL4605_05_edge_shadow_rows", "Q_edge_abs" in edge_text and "Q_shadow_abs" in shadow_text, "edge and shadow component totals present")
    add("VAL4605_06_qbar_update", "Q_tot_XH_abs" in qbar_text and "M_lower" in qbar_text, "Qbar numerator update present")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "empirical_pass_claimed", "score_ready", "numeric_value_present"} and value is True:
                    all_false = False
    add("VAL4605_07_no_claim_true", all_false, "no generated table promotes a claim")
    add("VAL4605_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4605_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4605_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4605_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4605_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4605_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4605_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4605_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4605_OVERALL", all(row["status"] == "PASS" for row in rows), "4605 Qbulk/Qedge/Qshadow numerator gate")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "numerator_theorem": numerator_theorem_rows(now),
        "bulk_components": bulk_component_rows(now),
        "edge_components": edge_component_rows(now),
        "shadow_components": shadow_component_rows(now),
        "qbar_update": qbar_update_rows(now),
        "product_update": product_update_rows(now),
        "blockers": blocker_rows(now),
        "controls": control_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])

    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(NUMERATOR_THEOREM_CSV, tables["numerator_theorem"])
    write_csv(BULK_COMPONENT_CSV, tables["bulk_components"])
    write_csv(EDGE_COMPONENT_CSV, tables["edge_components"])
    write_csv(SHADOW_COMPONENT_CSV, tables["shadow_components"])
    write_csv(QBAR_UPDATE_CSV, tables["qbar_update"])
    write_csv(PRODUCT_UPDATE_CSV, tables["product_update"])
    write_csv(BLOCKERS_CSV, tables["blockers"])
    write_csv(CONTROL_CSV, tables["controls"])
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
## PPC4161 Local Addendum - Qbulk/Qedge/Qshadow Numerator Gate

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The source numerator of `Qbar_XH` now splits into `Q_bulk`, `Q_edge` and `Q_shadow`. The bulk piece explicitly includes EM/Poynting stress as Hilbert flux or a bounded wall/source residual. The no-cancellation row is `|Q_tot_XH| <= |Q_bulk|_abs + |Q_edge|_abs + |Q_shadow|_abs`.
""",
    )

    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Qbulk/Qedge/Qshadow Numerator Gate

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private packet now has a concrete numerator gate for source coupling: prove `Q_bulk=Q_edge=Q_shadow=0` in one parent branch, or fill each component as a nonclaim source-backed bound before using `Qbar_XH` in `I_X^ST`.
""",
    )

    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4605 validation failed: {failed}")
    print(f"4605 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
