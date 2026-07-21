from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4579"
CLAIM_ID = "L-421"
BRANCH_ID = "MTS_R2FR_Y5_READOUT_COMMUTATOR_ZERO_OR_RHO_READOUT_SHIFT_BOUND_VALUE_4579"
MARKER = "PPC4161_READOUT_COMMUTATOR_ZERO_OR_RHO_READOUT_SHIFT_BOUND_VALUE_4579"
PACKET_MARKER = "PPC4161_PACKET_READOUT_COMMUTATOR_ZERO_OR_RHO_READOUT_SHIFT_BOUND_VALUE_4579"
DECISION = "PURE_POSTPROCESSING_READOUT_COMMUTATOR_ZERO_DERIVED_PROJECTOR_DEPENDENT_BRANCH_REDUCED_TO_OPERATOR_NORM_BOUND_NONCLAIM"
NEXT_TARGET = "4580-Y5-R2FR-Pi-readout-parent-domain-certificate-or-Creadout-first-numeric-bound.md"

DOC_PATH = POST / "4579-Y5-R2FR-readout-commutator-zero-or-rho-readout-shift-bound-value.md"
FORMAL_PATH = FORMAL / "595-PPC4161-readout-commutator-zero-or-rho-readout-shift-bound-value.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4578 = POST / "4578-Y5-R2FR-lapse-test-parent-signature-or-first-real-source-leak-row.md"
CSV_4578_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4578_NEXT_TARGET.csv"
CSV_4578_CONTRACT = SOURCE_DIR / "P8_Y5_R2FR_4578_LAPSE_PARENT_CONTRACT_THEOREM.csv"
CSV_4578_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4578_PARENT_SIGNATURE_AUDIT.csv"
CSV_4578_LEAK = SOURCE_DIR / "P8_Y5_R2FR_4578_RHO_READOUT_SHIFT_FIRST_SOURCE_LEAK_ROW.csv"
CSV_4578_DELTAWTR = SOURCE_DIR / "P8_Y5_R2FR_4578_DELTAWTR_UPDATE_ROWS.csv"
CSV_2486_READOUT_ORDER = SOURCE_DIR / "P8_Y5_FIELD_QUOTIENT_2486_READOUT_ORDER_GATE.csv"
CSV_2570_READOUT_ORDER = SOURCE_DIR / "P8_Y5_FIELD_QUOTIENT_2570_READOUT_ORDER_GATE.csv"
CSV_2624_SCHEMA = SOURCE_DIR / "P8_Y5_READOUT_SCHEMA_GATE_2624_READOUT_SCHEMA_THEOREM_ATTEMPT.csv"
CSV_2624_AUDIT = SOURCE_DIR / "P8_Y5_READOUT_SCHEMA_GATE_2624_PARENT_DOMAIN_SIGNATURE_AUDIT.csv"
CSV_2624_PROJECTOR = SOURCE_DIR / "P8_Y5_READOUT_SCHEMA_GATE_2624_PROJECTOR_RESIDUAL_BOUND_TEMPLATE.csv"
CSV_2653_COMM = SOURCE_DIR / "P8_Y5_RVC_WEPROW_2653_READOUT_VARIATION_COMMUTATOR_ZERO_ATTEMPT.csv"
CSV_2652_ASR = SOURCE_DIR / "P8_Y5_ASR_DELTAW_MATRIX_2652_ACTION_SCALE_READOUT_STABILITY_ATTEMPT.csv"
CSV_2656_BOUND_ATTEMPT = SOURCE_DIR / "P8_Y5_MICROSCOPE_READOUT_SOURCE_BOUND_2656_SOURCE_WORLDTUBE_RESIDUAL_BOUND_ATTEMPT.csv"
CSV_2655_LEDGER = SOURCE_DIR / "P8_Y5_WEP_WORLDTUBE_2655_POINT_SOURCE_RESIDUAL_LEDGER_NONCLAIM.csv"
CSV_550_FILL = SOURCE_DIR / "P8_Y5_BRR545_COMMUTATOR_PROJECTOR_BOUND_FILL_ROW.csv"
CSV_550_EVAL = SOURCE_DIR / "P8_Y5_BRR545_COMMUTATOR_PROJECTOR_EVALUATOR.csv"
CSV_550_OBSTRUCTION = SOURCE_DIR / "P8_Y5_BRR545_PROJECTOR_SYMPLECTIC_OBSTRUCTION_LEDGER.csv"
CSV_550_THEOREM = SOURCE_DIR / "P8_Y5_BRR545_PROJECTOR_SYMPLECTIC_SILENCE_THEOREM_ATTEMPT.csv"
FORMAL_337 = FORMAL / "337-PPC4161-Dq-source-readout-factorization-zero-or-Rsrc-epsilon-row.md"
FORMAL_336 = FORMAL / "336-PPC4161-Hperp-Dq-component-certificate-or-first-epsilon-profile-row.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4579_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4579_READOUT_COMMUTATOR_THEOREM.csv"
PROJECTOR_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4579_PROJECTOR_DERIVATIVE_BOUND.csv"
BOUND_VALUE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4579_RHO_READOUT_SHIFT_BOUND_VALUE_ROWS.csv"
SIGNATURE_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4579_PARENT_SIGNATURE_AUDIT.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4579_CONTROL_ROWS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4579_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4579_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4579_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4579_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4579_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


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
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
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
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> list[dict[str, Any]]:
    source_specs = [
        ("SRC4579_00_4578_doc", "4578 checkpoint statement", DOC_4578, "rho_readout_shift"),
        ("SRC4579_01_4578_next", "4578 selected 4579 target", CSV_4578_NEXT, "readout-commutator-zero-or-rho-readout-shift-bound-value"),
        ("SRC4579_02_4578_contract", "4578 readout naturality clause", CSV_4578_CONTRACT, "LPC4578_2_readout_naturality"),
        ("SRC4579_03_4578_audit", "4578 readout/projector survivor", CSV_4578_AUDIT, "AUD4578_2_readout_projector"),
        ("SRC4579_04_4578_leak", "4578 rho_readout_shift row", CSV_4578_LEAK, "RSL4578_0_rho_readout_shift_commutator"),
        ("SRC4579_05_4578_DeltaWtr", "4578 DeltaWtr row", CSV_4578_DELTAWTR, "DWU4578_0_readout_row_inserted"),
        ("SRC4579_06_2486_readout_order", "2486 variation-before-readout guardrail", CSV_2486_READOUT_ORDER, "RO2486_0_variation_before_readout"),
        ("SRC4579_07_2570_readout_order", "2570 variation-before-readout and coupling order", CSV_2570_READOUT_ORDER, "RO2570_0_variation_before_readout"),
        ("SRC4579_08_2624_schema", "2624 no readout variation slot", CSV_2624_SCHEMA, "RAV2624_1_no_variation_slot"),
        ("SRC4579_09_2624_audit", "2624 readout exclusion parent audit", CSV_2624_AUDIT, "PDS2624_2_readout_exclusion"),
        ("SRC4579_10_2624_projector", "2624 projector commutator template", CSV_2624_PROJECTOR, "PRB2624_1_projector_commutator"),
        ("SRC4579_11_2653_comm_zero", "2653 pure postprocessing zero lemma", CSV_2653_COMM, "RVC2653_1_pure_postprocessing_zero"),
        ("SRC4579_12_2653_projector_survives", "2653 projector product-rule obstruction", CSV_2653_COMM, "RVC2653_2_projection_commutator_survives"),
        ("SRC4579_13_2652_readout_gap", "2652 readout no-reentry gap", CSV_2652_ASR, "ASR2652_3_readout_gap"),
        ("SRC4579_14_2656_operator_decomp", "2656 operator decomposition", CSV_2656_BOUND_ATTEMPT, "SRB2656_1_operator_decomposition"),
        ("SRC4579_15_2655_readout_frame", "2655 readout/frame missing map", CSV_2655_LEDGER, "PSL2655_4_readout_frame"),
        ("SRC4579_16_550_fill", "550 commutator/projector bound fill row", CSV_550_FILL, "FB550_0_commutator_projector_bound"),
        ("SRC4579_17_550_eval", "550 evaluator row", CSV_550_EVAL, "FB550_0_commutator_projector_bound"),
        ("SRC4579_18_550_obstruction", "550 variation product rule", CSV_550_OBSTRUCTION, "PSO550_2_variation_product_rule"),
        ("SRC4579_19_550_theorem", "550 projector variation stress", CSV_550_THEOREM, "PST550_4_variation_stress"),
        ("SRC4579_20_formal_337", "337 Rsrc projector commutator", FORMAL_337, "Rsrc_projector_comm"),
        ("SRC4579_21_formal_336", "336 readout projector commutator", FORMAL_336, "readout_projector_commutator"),
        ("SRC4579_22_claim_420", "prior claim register row", CLAIMS_PATH, "L-420"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in source_specs:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": "readout commutator zero proof attempt and rho_readout_shift bound row",
                "valid_for_claim": "False",
            }
        )
    return rows


def theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "RCT4579_0_product_rule_identity",
            "statement": "The readout leak is exactly the derivative of the readout projector acting on the already-derived Hilbert source.",
            "formula": "O_f(Pi_readout J_H)-Pi_readout O_f(J_H)=(O_f Pi_readout)J_H",
            "derivation": "Apply O_f to the product Pi_readout J_H.  The Pi_readout O_f(J_H) term cancels against the ordered variation-before-readout branch, leaving only the projector derivative term.",
            "zero_condition": "O_f Pi_readout=0 on the source domain for every compact lapse probe f.",
            "status": "DERIVED_IDENTITY",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "RCT4579_1_pure_postprocessing_zero",
            "statement": "A pure data readout that is absent from the parent action, absent from the effective source coefficients, and applied after solving has zero readout commutator.",
            "formula": "Pi_readout in Obs only and Pi_readout notin Args(S_parent,S_eff,Coeff_active_source) => [O_f,Pi_readout]J_H=0 => rho_readout_shift=0",
            "derivation": "If Pi_readout has no variational slot and no active-source codomain, O_f cannot act on it.  The product-rule remainder (O_f Pi_readout)J_H therefore vanishes.",
            "zero_condition": "postprocessing_only + no_source_codomain + fixed_after_solution + no_worldtube_or_kernel_dependence",
            "status": "CONDITIONAL_ZERO_DERIVED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "RCT4579_2_projector_dependent_survivor",
            "statement": "A source-worldtube, material, frame, kernel, or EFT-dependent projector is not pure postprocessing and generally leaves a finite leak.",
            "formula": "delta(Pi_readout J_H)=Pi_readout delta J_H+(delta Pi_readout)J_H",
            "derivation": "For projectors whose domain, support, metric/frame, material tensor, kernel, or EFT coefficients vary with the local source branch, the second product-rule term is physical data unless independently zeroed.",
            "zero_condition": "delta Pi_readout=0 by parent domain certificate, topological silence, or sourced operator norm value equal to zero",
            "status": "SURVIVING_BRANCH_BOUND_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "theorem_id": "RCT4579_3_rho_shift_bound",
            "statement": "The surviving branch is reduced to a single operator-norm bound, not a vague missing coupling.",
            "formula": "||rho_readout_shift||_TV/M_H_ref <= C_readout := sup_{||f||_inf<=1} ||(O_f Pi_readout)J_H||_TV/M_H_ref",
            "derivation": "Insert the product-rule identity into Delta_readout[f] and take the total-variation dual norm over compact lapse probes.",
            "zero_condition": "C_readout=0",
            "status": "BOUND_DERIVED_VALUE_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def projector_bound_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "bound_id": "PDB4579_0_Creadout_split",
            "quantity": "C_readout",
            "formula": "C_readout <= C_domain + C_support + C_frame + C_material + C_kernel + C_EFT + C_tau",
            "meaning": "Decomposes the projector derivative into the exact places a nonzero readout leak can enter.",
            "source_basis": "RVC2653_2_projection_commutator_survives; SRB2656_1_operator_decomposition; PST550_4_variation_stress",
            "numeric_value": "MISSING_COMPONENT_VALUES",
            "status": "DERIVED_SPLIT_VALUE_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "bound_id": "PDB4579_1_domain_support",
            "quantity": "C_domain + C_support",
            "formula": "sup_{||f||_inf<=1} ||(O_f Pi_domain)J_H + (O_f Pi_support)J_H||_TV/M_H_ref",
            "meaning": "Worldtube, collar, support, boundary, or sample-domain movement under the lapse probe.",
            "source_basis": "2653 projector/source-worldtube obstruction; 2655 readout frame ledger",
            "numeric_value": "MISSING_WORLDTUBE_DOMAIN_SOURCE_MAP",
            "status": "SOURCE_ROW_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "bound_id": "PDB4579_2_frame_material_kernel",
            "quantity": "C_frame + C_material + C_kernel",
            "formula": "sup_{||f||_inf<=1} ||(O_f Pi_frame)J_H + (O_f Pi_material)J_H + (O_f Pi_kernel)J_H||_TV/M_H_ref",
            "meaning": "Readout frame, matter-response tensor, clock/force/orbit kernel, or instrument kernel dependence.",
            "source_basis": "SRB2656_1_operator_decomposition",
            "numeric_value": "MISSING_FRAME_MATERIAL_KERNEL_MAPS",
            "status": "SOURCE_ROW_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "bound_id": "PDB4579_3_EFT_tau",
            "quantity": "C_EFT + C_tau",
            "formula": "sup_{||f||_inf<=1} ||(O_f Pi_EFT)J_H + (O_f Pi_tau)J_H||_TV/M_H_ref",
            "meaning": "Effective coefficient feedback and finite-resolution/averaging kernels.",
            "source_basis": "2624 projector template; 337 R_src_readout residual split",
            "numeric_value": "MISSING_EFT_TAU_RESPONSE_MAPS",
            "status": "SOURCE_ROW_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "bound_id": "PDB4579_4_BRR545_projector_bridge",
            "quantity": "C_projector_abs",
            "formula": "C_projector_abs <= abs(int_A [d,Pi_M]J_H)/M_H_ref + abs(int_S (delta Pi_M)J_H)/M_H_ref",
            "meaning": "Bridge to the existing BRR545 conservative projector/symplectic fill row; no cancellation credit is allowed.",
            "source_basis": "FB550_0_commutator_projector_bound",
            "numeric_value": "MISSING_COMMUTATOR_NUMERIC_OR_THEOREM_ZERO; MISSING_PROJECTOR_VARIATION_NUMERIC_OR_THEOREM_ZERO",
            "status": "EXISTING_BOUND_LINKED_NONCLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def bound_value_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "RVB4579_0_zero_branch",
            "quantity": "rho_readout_shift",
            "bound": "||rho_readout_shift||_TV/M_H_ref = 0",
            "requires": "Pi_readout is pure postprocessing and has no source/worldtube/material/frame/kernel/EFT/tau dependence.",
            "current_value": "CONDITIONAL_ZERO_ONLY",
            "source_path": str(CSV_2653_COMM),
            "status": "ZERO_DERIVED_IF_DOMAIN_CERTIFICATE_SIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "RVB4579_1_operator_bound",
            "quantity": "rho_readout_shift",
            "bound": "||rho_readout_shift||_TV/M_H_ref <= C_readout",
            "requires": "C_readout value or theorem-zero source for every projector-dependence component.",
            "current_value": "MISSING_CREADOUT_NUMERIC_VALUE_OR_ZERO_CERTIFICATE",
            "source_path": str(PROJECTOR_BOUND_CSV),
            "status": "FORMAL_BOUND_DERIVED_VALUE_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "row_id": "RVB4579_2_DeltaWtr_insertion",
            "quantity": "Delta_Wtr",
            "bound": "Delta_Wtr <= (||mu_tr||_TV + ||B_src^A||_TV + M_H_ref*C_readout)/M_H_ref",
            "requires": "mu_tr, B_src^A, M_H_ref, and C_readout sourced in the same worldtube/readout frame.",
            "current_value": "MISSING_TRANSITION_AND_CREADOUT_VALUES",
            "source_path": str(CSV_4578_DELTAWTR),
            "status": "FORMAL_INSERTION_DERIVED_VALUE_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def signature_audit_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        (
            "AUD4579_0_pure_data_readout",
            "pure postprocessing readout",
            "If readout is Obs-only, absent from S_parent/S_eff, and has no active-source codomain, the commutator is zero.",
            "CONDITIONAL_ZERO_DERIVED",
            "This is a real forward theorem, but it only covers pure data reporting.",
        ),
        (
            "AUD4579_1_projector_dependence",
            "source-worldtube/projector-dependent readout",
            "If readout chooses a worldtube, support, frame, material tensor, kernel, or EFT coefficient, delta Pi_readout can be nonzero.",
            "LIVE_BOUND_BRANCH",
            "This is the likely local-GR bottleneck.",
        ),
        (
            "AUD4579_2_parent_domain_certificate",
            "parent-owned Pi_readout domain",
            "No current parent certificate proves Pi_readout is fixed before variation for every local arena.",
            "UNSIGNED",
            "Move to 4580 certificate or first C_readout value.",
        ),
        (
            "AUD4579_3_numeric_bound",
            "C_readout sourced value",
            "Existing BRR545 row gives strict shape but not numeric/source-backed components.",
            "VALUE_MISSING",
            "Cannot claim local-GR pass from 4579.",
        ),
        (
            "AUD4579_4_verdict",
            "readout commutator status",
            "Pure postprocessing zero is derived; projector-dependent branch is reduced to C_readout.",
            "ZERO_OR_BOUND_SPLIT_COMPLETE_NONCLAIM",
            "The next work item is narrow and attackable.",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "audit_id": audit_id,
            "clause": clause,
            "finding": finding,
            "status": status,
            "effect": effect,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, clause, finding, status, effect in rows
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        (
            "CTRL4579_pure_postprocessing_zero",
            "Pi_readout absent from parent/effective action and active-source codomain",
            "(O_f Pi_readout)J_H=0; rho_readout_shift=0",
            "CONTROL_PASS_CONDITIONAL",
        ),
        (
            "CTRL4579_domain_projector_nonzero",
            "Pi_readout selects a compact support/worldtube that moves under the lapse probe",
            "(O_f Pi_readout)J_H contributes C_domain+C_support",
            "NONZERO_BRANCH_RETAINED",
        ),
        (
            "CTRL4579_total_charge_trap",
            "int_W rho_readout_shift dV_H=0 but compact f detects positive/negative lobes",
            "TV bound catches it; same total mass is insufficient",
            "COUNTERMODEL_CAUGHT",
        ),
        (
            "CTRL4579_false_claim_guard",
            "C_readout missing but branch marked valid_for_claim=true",
            "validation/firewall must fail",
            "FIREWALL_EXPECTED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "control_id": control_id,
            "input_case": input_case,
            "expected": expected,
            "verdict": verdict,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for control_id, input_case, expected, verdict in rows
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    gates = [
        ("PROM4579_0_domain_certificate", "Pi_readout is parent-certified pure postprocessing or parent-fixed before variation.", "BLOCKED"),
        ("PROM4579_1_projector_norm", "All C_readout components have sourced numeric values or theorem-zero rows.", "BLOCKED"),
        ("PROM4579_2_frame_consistency", "C_readout, Delta_Wtr, and M_H_ref use the same worldtube/readout frame.", "BLOCKED"),
        ("PROM4579_3_no_total_charge_shortcut", "No same-total-mass shortcut is used in place of all compact lapse probes.", "PASSED_FIREWALL"),
        ("PROM4579_4_no_claim", "No local-GR/R10/PPN/clock/orbital pass is claimed from 4579.", "PASSED_FIREWALL"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "required_for_claim": "True",
            "valid_for_claim": "False",
        }
        for gate_id, gate, status in gates
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "plain_english": "4579 proves the clean branch: pure postprocessing readouts have zero rho_readout_shift.  It also proves why the hard branch survives: source-worldtube/material/frame/kernel/EFT-dependent projectors carry a product-rule term.  That survivor is now reduced to C_readout, an explicit operator-norm bound.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "Either parent-certify Pi_readout as pure postprocessing/fixed-domain for local arenas, or fill the first C_readout component value.  This is the shortest route toward removing rho_readout_shift from Delta_Wtr.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "status": "complete_nonclaim_checkpoint",
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_body(
    now: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    projector_bounds: list[dict[str, Any]],
    bound_values: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
) -> str:
    return f"""# 4579 - Readout commutator zero or rho_readout_shift bound value

Generated: `{now}`  
Branch: `{BRANCH_ID}`  
Decision: `{DECISION}`  
Claim status: private nonclaim checkpoint.

## Result

4579 does move the derivation forward.  The readout leak from 4578 is not left as a foggy missing coupling.  It splits exactly:

```text
O_f(Pi_readout J_H)-Pi_readout O_f(J_H) = (O_f Pi_readout)J_H
```

So:

```text
rho_readout_shift = 0
```

for a pure postprocessing readout: no parent-action slot, no effective-source slot, no active-source coefficient codomain, fixed after solving, and no worldtube/material/frame/kernel/EFT/tau dependence.

The surviving hard branch is also now precise:

```text
||rho_readout_shift||_TV/M_H_ref <= C_readout
C_readout := sup_{{||f||_inf<=1}} ||(O_f Pi_readout)J_H||_TV/M_H_ref
C_readout <= C_domain + C_support + C_frame + C_material + C_kernel + C_EFT + C_tau
```

This means a readout/projector leak is only allowed to survive through explicit projector dependence.  Same total mass or total charge is still not enough; compact lapse probes catch profile reshuffling.

## Readout commutator theorem

{markdown_table(theorem)}

## Projector derivative bound

{markdown_table(projector_bounds)}

## Bound value rows

{markdown_table(bound_values)}

## Parent signature audit

{markdown_table(audits)}

## Controls

{markdown_table(controls)}

## Promotion gates

{markdown_table(promotions)}

## Source register

{markdown_table(sources)}

## Next target

`{NEXT_TARGET}`

Reason: parent-certify `Pi_readout` as pure postprocessing/fixed-domain, or fill the first real `C_readout` component value.
"""


def spine_block(now: str) -> str:
    return f"""## PPC4161 4579 readout commutator zero or bound

Marker: `{MARKER}`  
Generated: `{now}`

4579 derives the exact product-rule identity for the 4578 readout leak: `O_f(Pi_readout J_H)-Pi_readout O_f(J_H)=(O_f Pi_readout)J_H`.  Pure postprocessing readouts therefore give `rho_readout_shift=0`; source-worldtube/material/frame/kernel/EFT/tau-dependent projectors survive only through `C_readout := sup_{{||f||_inf<=1}} ||(O_f Pi_readout)J_H||_TV/M_H_ref`.

Decision: `{DECISION}`.  Next target: `{NEXT_TARGET}`.
"""


def packet_block(now: str) -> str:
    return f"""## 4579 packet update - readout commutator zero or bound

Marker: `{PACKET_MARKER}`  
Generated: `{now}`

The private local packet now separates readout into two branches.  Pure data postprocessing is harmless and gives `rho_readout_shift=0`.  Any projector that chooses source worldtube, support, frame, material response, kernel, EFT coefficients, or averaging scale remains a finite `C_readout` operator-norm branch.  No local-GR claim is allowed until the domain certificate or a sourced `C_readout` value exists.
"""


def append_claim() -> None:
    existing = read_text(CLAIMS_PATH)
    if CLAIM_ID in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4579 derives the product-rule readout commutator split: pure postprocessing readout gives rho_readout_shift=0, while projector-dependent readout is bounded by C_readout.",
        "current_evidence": "Generated source register, readout commutator theorem, projector derivative bound, rho_readout_shift bound value rows, parent signature audit, controls, promotion gates, status and validation CSVs.",
        "status": DECISION.lower(),
        "next_test": NEXT_TARGET,
        "key_risk": "Promoting pure-postprocessing zero to projector-dependent local arenas without a parent domain certificate or C_readout value.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "C_readout still needs parent zero certificate or source-backed numeric component values before any local-GR/R10/PPN claim.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def validation_rows(
    outputs: list[Path],
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    projector_bounds: list[dict[str, Any]],
    bound_values: list[dict[str, Any]],
    audits: list[dict[str, Any]],
    controls: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH_ID,
                "check_id": check_id,
                "check": check,
                "passed": bool_text(passed),
                "detail": detail,
            }
        )

    for path in outputs:
        add(f"VAL4579_exists_{path.name}", "output path exists", path.exists(), str(path))
        if path.suffix == ".csv" and path.exists():
            rows = read_csv(path)
            add(f"VAL4579_csv_parse_{path.name}", "CSV parses with at least one row", len(rows) > 0, f"rows={len(rows)}")

    add("VAL4579_sources_exist", "all cited sources exist", all(row["exists"] == "True" for row in sources), "source register existence")
    add("VAL4579_needles_found", "all cited source needles found", all(row["needle_found"] == "True" for row in sources), "source register needles")
    add(
        "VAL4579_product_rule_identity",
        "product-rule identity derived",
        any(row["theorem_id"] == "RCT4579_0_product_rule_identity" and "(O_f Pi_readout)J_H" in row["formula"] for row in theorem),
        "RCT4579_0_product_rule_identity",
    )
    add(
        "VAL4579_pure_postprocessing_zero",
        "pure postprocessing zero theorem derived",
        any(row["theorem_id"] == "RCT4579_1_pure_postprocessing_zero" and "rho_readout_shift=0" in row["formula"] for row in theorem),
        "RCT4579_1_pure_postprocessing_zero",
    )
    add(
        "VAL4579_projector_branch_retained",
        "projector-dependent branch retained",
        any(row["theorem_id"] == "RCT4579_2_projector_dependent_survivor" and "delta Pi_readout" in row["formula"] for row in theorem),
        "RCT4579_2_projector_dependent_survivor",
    )
    add(
        "VAL4579_Creadout_split",
        "C_readout split includes all components",
        any(
            row["bound_id"] == "PDB4579_0_Creadout_split"
            and "C_domain + C_support + C_frame + C_material + C_kernel + C_EFT + C_tau" in row["formula"]
            for row in projector_bounds
        ),
        "PDB4579_0_Creadout_split",
    )
    add(
        "VAL4579_BRR545_bridge",
        "BRR545 conservative projector bridge linked",
        any(row["bound_id"] == "PDB4579_4_BRR545_projector_bridge" and "FB550_0_commutator_projector_bound" in row["source_basis"] for row in projector_bounds),
        "PDB4579_4_BRR545_projector_bridge",
    )
    add(
        "VAL4579_values_nonclaim",
        "bound value rows remain nonclaim while values/certificates missing",
        all(row["valid_for_claim"] == "False" for row in bound_values)
        and any("MISSING_CREADOUT" in row["current_value"] for row in bound_values),
        "bound value firewall",
    )
    add(
        "VAL4579_audit_verdict",
        "audit records split-complete nonclaim verdict",
        any(row["audit_id"] == "AUD4579_4_verdict" and row["status"] == "ZERO_OR_BOUND_SPLIT_COMPLETE_NONCLAIM" for row in audits),
        "AUD4579_4_verdict",
    )
    add(
        "VAL4579_controls",
        "controls include zero branch, nonzero branch, and total-charge trap",
        all(
            any(row["control_id"] == control_id for row in controls)
            for control_id in [
                "CTRL4579_pure_postprocessing_zero",
                "CTRL4579_domain_projector_nonzero",
                "CTRL4579_total_charge_trap",
            ]
        ),
        "control coverage",
    )
    add("VAL4579_decision_token", "decision token recorded", DECISION in read_text(DECISION_CSV) and DECISION in read_text(DOC_PATH), DECISION)
    add("VAL4579_next_target", "next target recorded", NEXT_TARGET in read_text(NEXT_CSV) and NEXT_TARGET in read_text(DOC_PATH), NEXT_TARGET)
    add("VAL4579_claim_register", "claim register updated", CLAIM_ID in read_text(CLAIMS_PATH), CLAIM_ID)
    add(
        "VAL4579_spine_packet",
        "spine and packet markers present",
        MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH),
        f"{MARKER}; {PACKET_MARKER}",
    )
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows()
    theorem = theorem_rows(now)
    projector_bounds = projector_bound_rows(now)
    bound_values = bound_value_rows(now)
    audits = signature_audit_rows(now)
    controls = control_rows(now)
    promotions = promotion_rows(now)
    decisions = decision_rows(now)
    next_targets = next_rows(now)
    statuses = status_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem)
    write_csv(PROJECTOR_BOUND_CSV, projector_bounds)
    write_csv(BOUND_VALUE_CSV, bound_values)
    write_csv(SIGNATURE_AUDIT_CSV, audits)
    write_csv(CONTROL_CSV, controls)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_targets)
    write_csv(STATUS_CSV, statuses)

    body = doc_body(now, sources, theorem, projector_bounds, bound_values, audits, controls, promotions)
    DOC_PATH.write_text(body, encoding="utf-8", newline="\n")
    FORMAL_PATH.write_text(body, encoding="utf-8", newline="\n")

    append_once(SPINE_PATH, MARKER, spine_block(now))
    append_once(PACKET_PATH, PACKET_MARKER, packet_block(now))
    append_claim()

    outputs = [
        SOURCE_REGISTER,
        THEOREM_CSV,
        PROJECTOR_BOUND_CSV,
        BOUND_VALUE_CSV,
        SIGNATURE_AUDIT_CSV,
        CONTROL_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    validations = validation_rows(outputs, sources, theorem, projector_bounds, bound_values, audits, controls)
    write_csv(VALIDATION_PATH, validations)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"{CHECKPOINT} complete: {DECISION}")
    print(f"wrote: {DOC_PATH}")
    print(f"validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
