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

CHECKPOINT = "4604"
CLAIM_ID = "L-446"
BRANCH_ID = "MTS_R2FR_Y5_MHREF_PIM_QBARXH_LOCK_GATE_4604"
MARKER = "PPC4161_MHREF_PIM_DENOMINATOR_LOCK_OR_QBARXH_FIRST_FILL_4604"
PACKET_MARKER = "PPC4161_PACKET_MHREF_PIM_QBARXH_LOCK_GATE_4604"
DECISION = "MHREF_PIM_LOCK_THEOREM_AND_QBARXH_BOUND_ROW_READY_NONCLAIM"
NEXT_TARGET = "4605-Y5-R2FR-Qbulk-Qedge-Qshadow-source-current-zero-or-QbarXH-component-first-fill.md"

DOC_PATH = POST / "4604-Y5-R2FR-MHref-PiM-denominator-lock-or-QbarXH-first-fill.md"
FORMAL_PATH = FORMAL / "620-PPC4161-MHref-PiM-denominator-lock-or-QbarXH-first-fill.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4604_SOURCE_REGISTER.csv"
DENOM_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4604_MHREF_DENOMINATOR_THEOREM.csv"
PIM_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4604_PIM_PROJECTOR_THEOREM.csv"
DENOM_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4604_MHREF_DENOMINATOR_INPUT_ROWS.csv"
PIM_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4604_PIM_PROJECTOR_INPUT_ROWS.csv"
QBAR_FILL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4604_QBARXH_FIRST_FILL_ROWS.csv"
PRODUCT_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4604_IXST_PRODUCT_UPDATE_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4604_CLAIM_BLOCKERS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4604_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4604_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4604_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4604_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4604_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4604_VALIDATION.csv"

DOC_4603 = POST / "4603-Y5-R2FR-source-test-charge-invariant-product-or-first-numeric-bound-row.md"
FORMAL_619 = FORMAL / "619-PPC4161-source-test-charge-invariant-product-or-first-numeric-bound-row.md"
CSV_4603_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4603_NEXT_TARGET.csv"
CSV_4603_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4603_CLAIM_BLOCKERS.csv"
CSV_4603_PRODUCT = SOURCE_DIR / "P8_Y5_R2FR_4603_IXST_PRODUCT_BOUND_ROWS.csv"
CSV_4603_QH = SOURCE_DIR / "P8_Y5_R2FR_4603_QBARXH_FACTOR_ROWS.csv"
CSV_2664_QBAR = SOURCE_DIR / "P8_Y5_R10_QBARXH_SOURCE_CURRENT_2664_QBARXH_FIRST_SOURCE_ROW_NONCLAIM.csv"
CSV_2665_LOCK = SOURCE_DIR / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv"
CSV_2665_DENOM = SOURCE_DIR / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_PROJECTOR_DENOMINATOR_GATE.csv"
CSV_2665_TEMPLATE = SOURCE_DIR / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_QBARXH_LOCK_TEMPLATE_NONCLAIM.csv"
CSV_2938_GATE = SOURCE_DIR / "P8_Y5_R2FR_2938_QBAR_TAU_FIRST_VALUE_GATE.csv"
CSV_4587_DENSITY = SOURCE_DIR / "P8_Y5_R2FR_4587_DENSITY_QBASIC_THEOREM.csv"
CSV_4588_REYNOLDS = SOURCE_DIR / "P8_Y5_R2FR_4588_REYNOLDS_SUPPORT_THEOREM.csv"
CSV_4589_MHREF = SOURCE_DIR / "P8_Y5_R2FR_4589_MHREF_QBASIC_THEOREM.csv"
CSV_4589_CLAUSES = SOURCE_DIR / "P8_Y5_R2FR_4589_SOURCE_BLIND_REFERENCE_CLAUSES.csv"
CSV_4589_DRIFT = SOURCE_DIR / "P8_Y5_R2FR_4589_DENOMINATOR_DRIFT_BOUND_ROWS.csv"
CSV_4590_DQ = SOURCE_DIR / "P8_Y5_R2FR_4590_DQ_VERTICAL_THEOREM.csv"
CSV_4590_READOUT = SOURCE_DIR / "P8_Y5_R2FR_4590_READOUT_MASK_THEOREM.csv"
CSV_4591_TAU = SOURCE_DIR / "P8_Y5_R2FR_4591_TAU_EOBS_LOCK_THEOREM.csv"
CSV_4418_GM = SOURCE_DIR / "P8_Y5_R2FR_4418_MASS_FLUX_GM_CLOSURE_OUTPUT.csv"
CSV_4440_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4440_SOURCE_CHARGE_CLOSURE_OUTPUT.csv"
CSV_4462_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4462_SOURCE_COUPLING_THEOREM.csv"

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
        "claim": "4604 welds the M_H_ref denominator and Pi_M projector locks into the Qbar_XH source amplitude: if the same-frame Hamiltonian reference, positive lower bound and fixed projector commute with the parent vertical direction, Qbar_XH is an owned source factor; otherwise it has an explicit absolute bound row.",
        "current_evidence": "Generated denominator theorem rows, Pi_M theorem rows, M_H_ref/Pi_M input rows, Qbar_XH first-fill bound rows, product-update rows, blockers, controls and validation.",
        "status": "MHref_PiM_lock_and_QbarXH_bound_row_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Dividing by an unowned or non-positive M_H_ref, letting Pi_M absorb reference/mask/boundary variation, or treating a symbolic Qbar_XH_abs row as a numeric R10/PPN/local-GR pass.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No R10, PPN, clock, orbital or local-GR claim until M_lower, Pi_M norm/commutator, Q_bulk/Q_edge/Q_shadow, qbar_XT and arena kernels are exact zero or source-backed numeric rows.",
    }
    rows.append({key: row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4604_00_4603_doc", DOC_4603, "M_H_ref/Pi_M", "4603 selected denominator/projector lock."),
        ("SRC4604_01_619_formal", FORMAL_619, "I_X^ST(lambda_X)", "formal source/test product handoff."),
        ("SRC4604_02_4603_next", CSV_4603_NEXT, "4604-Y5-R2FR-MHref-PiM-denominator-lock-or-QbarXH-first-fill.md", "machine next target."),
        ("SRC4604_03_4603_blocker", CSV_4603_BLOCKERS, "MIS4603_0_MHref_PiM_lock", "4603 named missing source-side lock."),
        ("SRC4604_04_4603_product", CSV_4603_PRODUCT, "IX4603_1_absolute_product_bound", "I_X^ST product bound requiring Qbar_XH."),
        ("SRC4604_05_4603_qh", CSV_4603_QH, "QH4603_3_projected_source_charge", "Qbar_XH source factor row."),
        ("SRC4604_06_2664_qbar", CSV_2664_QBAR, "QXH2664_3_projected_Qbar", "old projected Qbar row."),
        ("SRC4604_07_2665_mhref", CSV_2665_LOCK, "HLOCK2665_3_MHref", "Hamiltonian denominator lock input."),
        ("SRC4604_08_2665_pim", CSV_2665_LOCK, "HLOCK2665_4_PiM", "Pi_M projector lock input."),
        ("SRC4604_09_2665_comm", CSV_2665_LOCK, "HLOCK2665_5_commutator_stress", "Pi_M commutator obstruction."),
        ("SRC4604_10_2665_denom_gate", CSV_2665_DENOM, "PDG2665_0_same_frame", "same-frame denominator gate."),
        ("SRC4604_11_2665_template", CSV_2665_TEMPLATE, "QbarXH_locked", "Qbar lock template."),
        ("SRC4604_12_2938_mhref", CSV_2938_GATE, "FVG2938_0_MHref", "first-value MHref gate."),
        ("SRC4604_13_4587_density", CSV_4587_DENSITY, "DQT4587_1_qbasic_density_zero", "density q-basic component."),
        ("SRC4604_14_4588_reynolds", CSV_4588_REYNOLDS, "RST4588_1_zero_trace_support", "support boundary component."),
        ("SRC4604_15_4589_definition", CSV_4589_MHREF, "MHR4589_0_definition", "M_H_ref definition."),
        ("SRC4604_16_4589_bound", CSV_4589_MHREF, "MHR4589_2_no_cancellation_bound", "denominator drift bound."),
        ("SRC4604_17_4589_positive", CSV_4589_MHREF, "MHR4589_3_positive_denominator_guard", "positive lower-bound guard."),
        ("SRC4604_18_4589_clauses", CSV_4589_CLAUSES, "MHC4589_4_positive_lower_bound", "source-blind reference clauses."),
        ("SRC4604_19_4589_drift", CSV_4589_DRIFT, "epsilon_MHref", "denominator drift input rows."),
        ("SRC4604_20_4590_dq", CSV_4590_DQ, "DQV4590_1_qbasic_bundle_zero", "q-basic bundle zero."),
        ("SRC4604_21_4590_readout", CSV_4590_READOUT, "ROM4590_0_fixed_protocol_zero", "fixed readout/mask zero."),
        ("SRC4604_22_4591_tau", CSV_4591_TAU, "TE4591_1_chain_rule_zero", "same tau/e_obs chain-rule zero."),
        ("SRC4604_23_4418_gm", CSV_4418_GM, "Poisson", "Newton/GM anti-circularity context."),
        ("SRC4604_24_4440_source", CSV_4440_SOURCE, "SOURCE_CHARGE_REDUCED_TO_ACTION_MEASURE_CURRENT_CONTRACT", "source-charge closure context."),
        ("SRC4604_25_4462_theorem", CSV_4462_THEOREM, "SCT4462_7_no_absorption_guard", "no absorption guard."),
        ("SRC4604_26_claim_445", CLAIMS_PATH, "L-445", "claim-register handoff from 4603."),
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


def denominator_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "MHR4604_0_same_frame_denominator_definition",
            "statement": "The source denominator is the same-frame Hamiltonian/reference difference, not an orbital GM or fitted acceleration mass.",
            "formula": "M_H_ref := H_tau[S_outer;tau_*,e_*] - H_ref[Sigma_ref;tau_*,e_*]",
            "derivation": "Use the 4589 definition with the 4591 common tau/e_obs branch and fixed source/readout protocol before any local residual is inspected.",
            "consequence": "Qbar_XH cannot be normalized by a post-fit G, GM, source mask or readout convention.",
            "status": "DENOMINATOR_OBJECT_DERIVED_CONDITIONAL",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "MHR4604_1_vertical_silence",
            "statement": "If H_tau, H_ref, tau_*, e_*, surfaces and reference subtraction all descend through q, then M_H_ref is vertically silent.",
            "formula": "D_v M_H_ref = D_v H_tau - D_v H_ref = 0 for v in ker(Dq)",
            "derivation": "H_tau=Hbar_tau(q(Phi)) and H_ref=Hbar_ref(q(Phi)) imply D_vH_tau=D_vH_ref=0 by the chain rule.",
            "consequence": "The denominator introduces no hidden source/test coupling on the strict q-basic branch.",
            "status": "EXACT_CONDITIONAL_ZERO_THEOREM_NOT_GLOBAL_PARENT_SIGNED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "MHR4604_2_inverse_denominator_lock",
            "statement": "A normalized source charge may divide by M_H_ref only after a positive same-frame lower bound is signed or sourced.",
            "formula": "M_H_ref >= M_lower > 0; if M_H_ref=M_0+deltaM and |deltaM|<=epsilon_abs M_0 with epsilon_abs<1, then M_lower=M_0(1-epsilon_abs)",
            "derivation": "This is the 4589 positivity guard recast as the Qbar_XH denominator gate.",
            "consequence": "Without M_lower, Qbar_XH_abs and I_X^ST are formal rows only.",
            "status": "POSITIVITY_GUARD_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "MHR4604_3_denominator_drift_bound",
            "statement": "If q-basicness is unsigned, denominator drift is retained as a no-cancellation residual.",
            "formula": "epsilon_MHref <= (|D_vH_tau|+|D_vH_ref|+|E_symp|+|E_ref|+|E_frame|+|E_mask|)/M_lower",
            "derivation": "Apply the triangle inequality to the Hamiltonian/reference difference and append symplectic, reference, frame and mask leakage from 4589-4591.",
            "consequence": "Denominator leakage cannot be hidden in calibration; it remains a sourceable input row.",
            "status": "BOUND_FORMULA_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def pim_theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "PIM4604_0_fixed_projector_definition",
            "statement": "Pi_M^H is a fixed-variable projector only after its held-fixed list is selected before source variation.",
            "formula": "Pi_M^H[f]=partial f/partial M_H_ref |_{tau_*,S_outer,S_ref,H_ref,C_top,chi_B,protocol}",
            "derivation": "Use 2665's Pi_M contract but make the fixed list explicit so the projector cannot absorb residual-dependent reference choices.",
            "consequence": "Pi_M algebra is not enough; the fixed-variable list must itself be q-basic or bounded.",
            "status": "PROJECTOR_CONTRACT_DERIVED_CONDITIONAL",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "PIM4604_1_projector_vertical_silence",
            "statement": "If the fixed-variable list is q-basic and Pi_M is selected before readout, the projector commutes with vertical variation.",
            "formula": "[D_v,Pi_M^H]f=0 and D_v Pi_M^H[f]=Pi_M^H[D_v f] for v in ker(Dq)",
            "derivation": "The derivative at fixed q-basic protocol data has no hidden D_v fixed-list term.",
            "consequence": "Projected source charge is owned by the parent source current rather than by a moving mass/reference convention.",
            "status": "EXACT_CONDITIONAL_COMMUTATOR_ZERO_NOT_GLOBAL_PARENT_SIGNED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "PIM4604_2_projector_commutator_bound",
            "statement": "If projector silence is unsigned, its commutator stress is an explicit additive source-charge residual.",
            "formula": "|Pi_M^H Q_tot| <= ||Pi_M^H|| (|Q_bulk|+|Q_edge|+|Q_shadow|) + |E_PiM_comm|",
            "derivation": "Apply an operator-norm bound to the projected bulk/edge/shadow source vector and retain the commutator separately.",
            "consequence": "Pi_M cannot be used as a free cancellation or normalization knob.",
            "status": "BOUND_FORMULA_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def denominator_input_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "input_id": "MD4604_0_M0",
            "quantity": "M_0 or M_EH",
            "definition": "baseline same-frame Hamiltonian/Hilbert source denominator before residual corrections",
            "required_inputs": "H_tau[S_outer]; H_ref[S_ref]; tau_*; e_*; surface family; units",
            "current_status": "MISSING_SOURCE_BACKED_BASELINE_DENOMINATOR",
            "bound_role": "M_lower=M_0(1-epsilon_abs)",
            "units": "mass_or_energy_over_c2",
            "source_paths": f"{CSV_4589_MHREF}; {CSV_2938_GATE}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "MD4604_1_epsilon_abs",
            "quantity": "epsilon_abs",
            "definition": "absolute fractional denominator drift from Hamiltonian/reference/frame/boundary/mask leakage",
            "required_inputs": "D_vH_tau; D_vH_ref; E_symp; E_ref; E_frame; E_mask; M_0",
            "current_status": "MISSING_DENOMINATOR_DRIFT_COMPONENT_VALUES",
            "bound_role": "requires epsilon_abs<1 for division",
            "units": "dimensionless",
            "source_paths": f"{CSV_4589_DRIFT}; {CSV_4591_TAU}; {CSV_4590_READOUT}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "MD4604_2_M_lower",
            "quantity": "M_lower",
            "definition": "positive lower bound for M_H_ref in the selected source branch",
            "required_inputs": "M_0>0; 0<=epsilon_abs<1; same-frame units",
            "current_status": "MISSING_POSITIVE_LOWER_BOUND",
            "bound_role": "denominator for Qbar_XH_abs",
            "units": "mass_or_energy_over_c2",
            "source_paths": f"{CSV_4589_MHREF}; {CSV_4589_CLAUSES}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def pim_input_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "input_id": "PM4604_0_fixed_list",
            "quantity": "Pi_M fixed-variable list",
            "definition": "tau_*, surfaces, reference, topological sector, background labels and readout protocol held fixed before variation",
            "required_inputs": "q-basic certificates or bounds for every fixed variable",
            "current_status": "MISSING_FIXED_LIST_PARENT_SIGNATURE",
            "bound_role": "needed for [D_v,Pi_M]=0",
            "units": "projector_protocol",
            "source_paths": f"{CSV_2665_LOCK}; {CSV_4590_READOUT}; {CSV_4591_TAU}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "PM4604_1_operator_norm",
            "quantity": "||Pi_M^H||",
            "definition": "operator norm of the mass projector on the source-charge vector space",
            "required_inputs": "source vector norm; projector definition; units ledger",
            "current_status": "MISSING_PROJECTOR_OPERATOR_NORM",
            "bound_role": "multiplies |Q_bulk|+|Q_edge|+|Q_shadow|",
            "units": "dimensionless_or_declared_projector_units",
            "source_paths": f"{CSV_2665_LOCK}; {CSV_2665_DENOM}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "PM4604_2_commutator",
            "quantity": "E_PiM_comm",
            "definition": "commutator/projector-stress residual when Pi_M does not commute with vertical variation or exterior/source derivative",
            "required_inputs": "[D_v,Pi_M]Q_tot or [d,Pi_M]J_H component bound",
            "current_status": "MISSING_PROJECTOR_COMMUTATOR_ZERO_OR_BOUND",
            "bound_role": "additive numerator residual for Qbar_XH_abs",
            "units": "parent_X_charge",
            "source_paths": f"{CSV_2665_LOCK}; {CSV_2665_TEMPLATE}",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def qbar_fill_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QF4604_0_strict_zero_lock",
            "quantity": "Qbar_XH",
            "formula": "if Q_bulk=Q_edge=Q_shadow=0, M_H_ref>=M_lower>0, and [D_v,Pi_M]=0, then Qbar_XH=0",
            "required_inputs": "source-current zero; edge zero; shadow zero; M_lower; Pi_M commutator zero",
            "current_status": "CONDITIONAL_ZERO_ROUTE_NOT_PARENT_SIGNED",
            "numeric_value": "MISSING",
            "units": "parent_X_charge_per_mass",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QF4604_1_absolute_Qbar_bound",
            "quantity": "Qbar_XH_abs",
            "formula": "|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/M_lower",
            "required_inputs": "M_lower; Pi_M_op_norm; Q_bulk_abs; Q_edge_abs; Q_shadow_abs; E_PiM_comm",
            "current_status": "BOUND_ROW_DERIVED_VALUES_MISSING",
            "numeric_value": "MISSING",
            "units": "parent_X_charge_per_mass",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QF4604_2_denominator_drift_guard",
            "quantity": "Qbar_denominator_drift_abs",
            "formula": "|delta Qbar_den| <= |Pi_M Q_tot| epsilon_MHref/M_lower",
            "required_inputs": "Pi_M Q_tot bound; epsilon_MHref; M_lower",
            "current_status": "DRIFT_GUARD_DERIVED_VALUES_MISSING",
            "numeric_value": "MISSING",
            "units": "parent_X_charge_per_mass",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QF4604_3_claim_ready_gate",
            "quantity": "Qbar_XH_claim_gate",
            "formula": "claim-ready only if no MISSING inputs, M_lower>0, units declared, source paths exist and edge/shadow/commutator pieces are zero or bounded",
            "required_inputs": "all QF4604 rows plus source/test branch identity",
            "current_status": "CLAIM_BLOCKED",
            "numeric_value": "MISSING",
            "units": "gate",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def product_update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "PU4604_0_I_product_update",
            "quantity": "|I_X^ST|",
            "updated_formula": "|I_X^ST| <= Qbar_XH_abs qbar_XT_abs/(4*pi |Z_X| G_N m_T)",
            "inserted_object": "Qbar_XH_abs from QF4604_1, already normalized by M_H_ref lower bound",
            "current_status": "PRODUCT_SCHEMA_REFINED_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "PU4604_1_alpha_update",
            "quantity": "|alpha_R10|",
            "updated_formula": "|alpha_R10| <= |K_X| Qbar_XH_abs qbar_XT_abs |tau_R10| + |alpha_tail_abs|",
            "inserted_object": "M_H_ref/Pi_M protected source charge row",
            "current_status": "R10_SCHEMA_REFINED_NOT_SCORE_READY",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4604_0_M_lower",
            "missing_object": "positive numeric/source-backed M_lower",
            "why_it_matters": "without a positive lower bound, Qbar_XH cannot safely divide by M_H_ref",
            "best_next_action": "source M_0 and epsilon_abs, or prove denominator exact q-basic with M_0>0",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4604_1_PiM_norm_commutator",
            "missing_object": "Pi_M operator norm and commutator zero/bound",
            "why_it_matters": "without this, the projector can absorb reference, boundary, support or mask variation",
            "best_next_action": "prove fixed-list q-basic projector silence or fill ||Pi_M|| and E_PiM_comm",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4604_2_Q_components",
            "missing_object": "Q_bulk, Q_edge and Q_shadow zero/bound rows",
            "why_it_matters": "4604 supplies the denominator/projector envelope, but the numerator source-current pieces still need values",
            "best_next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4604_3_downstream_qbar_tau",
            "missing_object": "qbar_XT, K_X, tau_R10 and tail rows",
            "why_it_matters": "Qbar_XH alone is not an empirical local-GR or R10 pass",
            "best_next_action": "defer until source numerator row is live",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4604_0_no_division_without_lower_bound",
            "control": "Any Qbar_XH row with M_lower missing or non-positive remains valid_for_claim=false.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4604_1_no_moving_projector",
            "control": "Pi_M may not be chosen after seeing residuals; moving-projector terms become E_PiM_comm.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4604_2_no_GM_backfill",
            "control": "Orbital GM, fitted G or acceleration data cannot define M_H_ref for the source-charge row.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4604_3_no_claim_from_schema",
            "control": "Qbar_XH_abs schema rows do not imply R10, PPN, clock, orbital or local-GR success.",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4604_0_denominator",
            "promotion_requirement": "M_H_ref has same-frame q-basic definition and M_lower>0 with source-backed units.",
            "current_status": "FAIL_M_LOWER_VALUES_MISSING",
            "source_count": len(sources),
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4604_1_projector",
            "promotion_requirement": "Pi_M fixed-variable list is parent-owned and commutator stress is zero or bounded.",
            "current_status": "FAIL_PIM_NORM_COMMUTATOR_MISSING",
            "source_count": len(sources),
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4604_2_QbarXH",
            "promotion_requirement": "Qbar_XH_abs has M_lower, Pi_M norm, Q_bulk/Q_edge/Q_shadow and commutator rows with no placeholders.",
            "current_status": "FAIL_Q_NUMERATOR_COMPONENTS_MISSING",
            "source_count": len(sources),
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4604_3_empirical",
            "promotion_requirement": "Downstream I_X^ST and arena kernels are numeric/source-backed and below empirical bounds.",
            "current_status": "FAIL_DO_NOT_CLAIM_EMPIRICAL_PASS",
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
            "reason": "The denominator/projector lock is now explicitly derived and inserted into Qbar_XH_abs, but M_lower, Pi_M norm/commutator and Q numerator pieces remain unfilled.",
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
            "what_moved": "Qbar_XH is now a locked denominator/projector amplitude problem with an explicit absolute source-charge bound row.",
            "what_did_not_move": "No source-charge numerator value, R10 alpha, PPN residual or local-GR pass is claimed.",
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
            "reason": "After 4604, the denominator/projector envelope exists. The next physical numerator is Q_bulk+Q_edge+Q_shadow.",
            "derive_first": "prove source-current/edge/shadow zero in the same parent branch",
            "fallback": "fill Q_bulk_abs, Q_edge_abs and Q_shadow_abs as nonclaim component rows under the 4604 Qbar_XH_abs formula",
            "valid_for_claim": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4604 - Y5 R2FR MHref/PiM Denominator Lock Or QbarXH First Fill

Generated: `{now}`

Marker: `{MARKER}`
Branch: `{BRANCH_ID}`
Claim register row: `{CLAIM_ID}`
Previous target: `{DOC_4603}`

## Result

4603 showed that the finite-range source/test product lives or dies on `Qbar_XH qbar_XT/Z_X`.

4604 welds the source-side denominator and projector into that object:

```text
M_H_ref := H_tau[S_outer; tau_*, e_*] - H_ref[Sigma_ref; tau_*, e_*]
```

and:

```text
Pi_M^H[f] = partial f/partial M_H_ref
            |_{{tau_*, S_outer, S_ref, H_ref, C_top, chi_B, protocol}}.
```

If the same-frame Hamiltonian/reference branch is q-basic, `M_H_ref >= M_lower > 0`, and the fixed-variable list of `Pi_M^H` is q-basic, then:

```text
D_v M_H_ref = 0,
D_v(1/M_H_ref) = 0,
[D_v, Pi_M^H] = 0.
```

So the strict clean route is:

```text
Q_bulk = Q_edge = Q_shadow = 0
and M_lower > 0
and [D_v,Pi_M^H]=0
    => Qbar_XH = 0.
```

If that route is not parent-signed, the claim-safe fallback is:

```text
|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|+|Q_edge|+|Q_shadow|)
              + |E_PiM_comm|) / M_lower.
```

This is a real forward move: the source amplitude is no longer "find a coupling"; it is a denominator, projector and three numerator components.

## Private Decision

`{DECISION}`

No R10, PPN, clock, orbital, EM, Newton or local-GR pass is claimed. The immediate best target is `{NEXT_TARGET}`.

## Source Register

{markdown_table(tables["sources"])}

## MHref Denominator Theorem

{markdown_table(tables["denom_theorem"])}

## PiM Projector Theorem

{markdown_table(tables["pim_theorem"])}

## MHref Denominator Input Rows

{markdown_table(tables["denom_inputs"])}

## PiM Projector Input Rows

{markdown_table(tables["pim_inputs"])}

## QbarXH First Fill Rows

{markdown_table(tables["qbar_fill"])}

## Product Update Rows

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
    return f"""# PPC4161 620 - MHref/PiM Denominator Lock Or QbarXH First Fill

Generated: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Claim register: `{CLAIM_ID}`

## Formal Statement

Define the source denominator in the same observed branch:

```text
M_H_ref := H_tau[S_outer;tau_*,e_*] - H_ref[Sigma_ref;tau_*,e_*].
```

If `H_tau`, `H_ref`, `tau_*`, `e_*`, surfaces and reference subtraction descend through `q`, then for `v in ker(Dq)`:

```text
D_v M_H_ref = 0.
```

If additionally `M_H_ref >= M_lower > 0`, division is allowed. The source projector is fixed before readout:

```text
Pi_M^H[f]=partial f/partial M_H_ref |_{{tau_*,S_outer,S_ref,H_ref,C_top,chi_B,protocol}}.
```

If the held-fixed list is q-basic:

```text
[D_v,Pi_M^H] = 0.
```

The nonclaim source amplitude row is:

```text
|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/M_lower.
```

Private nonclaim. The next target is `{NEXT_TARGET}`.
"""


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False})

    add("VAL4604_00_sources_exist", all(row["path_exists"] for row in tables["sources"]), "all cited source paths exist")
    missing_needles = [row["source_id"] for row in tables["sources"] if not row["needle_found"]]
    add("VAL4604_01_needles_found", not missing_needles, "missing needles: " + ",".join(missing_needles) if missing_needles else "all cited source needles found")

    csv_paths = [SOURCE_REGISTER, DENOM_THEOREM_CSV, PIM_THEOREM_CSV, DENOM_INPUT_CSV, PIM_INPUT_CSV, QBAR_FILL_CSV, PRODUCT_UPDATE_CSV, BLOCKERS_CSV, CONTROL_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    details = []
    csv_ok = True
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4604_02_csv_parse", csv_ok, ";".join(details))

    denom_text = "\n".join(str(row) for row in tables["denom_theorem"])
    pim_text = "\n".join(str(row) for row in tables["pim_theorem"])
    fill_text = "\n".join(str(row) for row in tables["qbar_fill"])
    add("VAL4604_03_mhref_definition", "M_H_ref :=" in denom_text and "M_lower > 0" in denom_text, "denominator definition and positivity guard present")
    add("VAL4604_04_pim_commutator", "Pi_M^H" in pim_text and "[D_v,Pi_M^H]" in pim_text, "projector/commutator theorem present")
    add("VAL4604_05_qbar_bound", "|Qbar_XH|" in fill_text and "Q_bulk" in fill_text and "Q_shadow" in fill_text, "QbarXH absolute bound present")

    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "empirical_pass_claimed", "score_ready", "numeric_value_present"} and value is True:
                    all_false = False
    add("VAL4604_06_no_claim_true", all_false, "no generated table promotes a claim")
    add("VAL4604_07_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4604_08_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4604_09_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4604_10_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4604_11_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4604_12_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4604_13_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4604_14_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4604_OVERALL", all(row["status"] == "PASS" for row in rows), "4604 MHref/PiM QbarXH lock gate")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "denom_theorem": denominator_theorem_rows(now),
        "pim_theorem": pim_theorem_rows(now),
        "denom_inputs": denominator_input_rows(now),
        "pim_inputs": pim_input_rows(now),
        "qbar_fill": qbar_fill_rows(now),
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
    write_csv(DENOM_THEOREM_CSV, tables["denom_theorem"])
    write_csv(PIM_THEOREM_CSV, tables["pim_theorem"])
    write_csv(DENOM_INPUT_CSV, tables["denom_inputs"])
    write_csv(PIM_INPUT_CSV, tables["pim_inputs"])
    write_csv(QBAR_FILL_CSV, tables["qbar_fill"])
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
## PPC4161 Local Addendum - MHref/PiM QbarXH Lock Gate

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The source-side amplitude now passes through a same-frame denominator/projector lock: `M_H_ref := H_tau-H_ref`, a positive lower bound `M_lower`, a fixed `Pi_M^H`, and the nonclaim bound `|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/M_lower`.
""",
    )

    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - MHref/PiM QbarXH Lock Gate

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private packet now has the source-side denominator/projector gate needed before `I_X^ST` can be numeric. Missing `M_lower`, `Pi_M` norm/commutator and source-current numerator pieces keep every empirical claim blocked.
""",
    )

    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4604 validation failed: {failed}")
    print(f"4604 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
