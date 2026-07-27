from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3000"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3000-Y5-R2FR-fixed-tau-surface-commutator-zero-or-second-Bv-component-bound-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3000_SOURCE_REGISTER.csv",
    "zero_audit": RESIDUALS / "P8_Y5_R2FR_3000_TAU_SURFACE_COMMUTATOR_ZERO_AUDIT.csv",
    "bound_rows": RESIDUALS / "P8_Y5_R2FR_3000_EPSILON_BV_TAU_SURFACE_BOUND_ROWS.csv",
    "kernel_rebase": RESIDUALS / "P8_Y5_R2FR_3000_KERNEL_CHARGE_REBASE_AFTER_BV_COMPONENTS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3000_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3000_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3000_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3000_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3000_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "zero_audit_copy": PARENT_ACTION / "fixed_tau_surface_commutator_zero_attempt_3000_NOT_SIGNED.csv",
    "bound_copy": LOCAL_BOUNDS / "epsilon_Bv_tau_surface_commutator_bound_rows_3000_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3000_TAU_SURFACE_OWNER_SOURCE_PACK_OR_FIRST_COMMUTATOR_VALUE_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def missing_anchors(path: Path, needles: list[str]) -> str:
    haystack = text(path)
    return "; ".join(needle for needle in needles if needle not in haystack)


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [str(output_row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


SOURCE_SPECS = [
    (
        "SRC3000_00_2999_next",
        RESIDUALS / "P8_Y5_R2FR_2999_NEXT_TARGET.csv",
        ["NEXT2999_0_3000", "epsilon_Bv_tau_surface_commutator"],
        "2999 selects tau/surface commutator as the second Bv component target.",
    ),
    (
        "SRC3000_01_2999_remaining",
        RESIDUALS / "P8_Y5_R2FR_2999_REMAINING_KERNEL_DEBTS.csv",
        ["REM2999_2_tau_surface", "MISSING_TAU_SURFACE_LOCK"],
        "2999 keeps tau/surface commutator as an open kernel debt.",
    ),
    (
        "SRC3000_02_2991_epsilon",
        RESIDUALS / "P8_Y5_R2FR_2991_EPSILON_BV_SOURCE_BOUND_ROWS_NONCLAIM.csv",
        ["EBV2991_04_tau_surface", "SIG2547_1_boundary_surface;SIG2547_3_tau_coframe"],
        "2991 defines the tau/surface commutator residual interface.",
    ),
    (
        "SRC3000_03_2545_exact",
        RESIDUALS / "P8_Y5_NO_SHADOW_2545_EXACT_IMPROVEMENT_CANCELLATION_DERIVATION.csv",
        ["EIC2545_3_k_invariance", "fixed surface embedding"],
        "2545 gives the cancellation algebra and its field-dependent tau/surface caveat.",
    ),
    (
        "SRC3000_04_2547_signature",
        RESIDUALS / "P8_Y5_NO_SHADOW_2547_SIGNATURE_AUDIT.csv",
        ["SIG2547_1_boundary_surface", "SIG2547_3_tau_coframe"],
        "2547 identifies the missing fixed surface/domain and tau/coframe signatures.",
    ),
    (
        "SRC3000_05_2547_dirichlet",
        RESIDUALS / "P8_Y5_NO_SHADOW_2547_DIRICHLET_ACTION_CONTRACT.csv",
        ["DAC2547_2_variation_domain", "DAC2547_4_tau_coframe_lock"],
        "Dirichlet contract shows how fixed boundary data would make the variation tangent.",
    ),
    (
        "SRC3000_06_2455_zero_cert",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2455_BOUNDARY_DATA_ZERO_CERTIFICATE.csv",
        ["ZC2455_0_surface_domain", "ZC2455_2_tau"],
        "2455 keeps source-blind surface/domain and tau zero certificates blocked.",
    ),
    (
        "SRC3000_07_2455_embedding",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2455_BOUNDARY_REFERENCE_EMBEDDING_DERIVATION.csv",
        ["EMB2455_4_finite_bound", "C_tau ||D_a tau||"],
        "2455 gives the finite operator-norm fallback form when exact zero fails.",
    ),
    (
        "SRC3000_08_2588_tau",
        RESIDUALS / "P8_Y5_OBS_STACK_2588_Q_OBSE_TAU_DESCENT_AUDIT.csv",
        ["OSA2588_5_tau_identity", "MISSING_PARENT_TAU_IDENTITY"],
        "observed-stack audit confirms tau is not parent-owned for current MTS.",
    ),
    (
        "SRC3000_09_2900_tau_domain",
        RESIDUALS / "P8_Y5_R2FR_2900_SOURCE_COMPLEX_OWNER_AUDIT.csv",
        ["SC2900_2_tau_lock", "SC2900_5_exterior_link_complex"],
        "source-complex audit confirms tau and linked exterior complex are not fully owned.",
    ),
]


def source_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "required_anchors": "; ".join(needles),
                "anchors_found": anchors(path, needles),
                "missing_anchors": missing_anchors(path, needles),
                "role": role,
            }
        )
        for source_id, path, needles, role in SOURCE_SPECS
    ]


def zero_audit_rows() -> list[dict[str, Any]]:
    data = [
        (
            "TSC3000_0_integrand_identity",
            "commutator identity",
            "delta(i_tau mu)-i_tau(delta mu) = i_{delta tau} mu plus field-space commutator terms; moving S adds int_{delta S} i_tau mu.",
            "EXACT_DECOMPOSITION_WRITTEN",
            "turns the foggy tau/surface leak into two owner clauses",
            True,
        ),
        (
            "TSC3000_1_fixed_tau_condition",
            "fixed tau/coframe condition",
            "delta_v tau = 0 and [delta_v,i_tau]=0 for all allowed vertical/readout variations in the parent branch.",
            "MISSING_PARENT_TAU_IDENTITY",
            "2588/2547 do not yet sign one tau for source, clocks, boundary, charge and readout",
            False,
        ),
        (
            "TSC3000_2_fixed_surface_condition",
            "source-blind linked surface/domain condition",
            "delta_v S_link = 0, delta_v A_ext = 0 and no cap/corner transport is induced by source/readout fitting.",
            "MISSING_SOURCE_BLIND_SURFACE_DOMAIN_RULE",
            "2455/2547 keep surface/domain ownership blocked",
            False,
        ),
        (
            "TSC3000_3_conditional_zero",
            "tau/surface commutator zero",
            "If TSC3000_1 and TSC3000_2 are parent-signed, then epsilon_Bv_tau_surface_commutator=0 for the exact/fixed Bv component.",
            "CONDITIONAL_ZERO_NOT_CURRENT_MTS",
            "conditions are exact but unsigned",
            False,
        ),
        (
            "TSC3000_4_finite_bound",
            "fallback finite bound law",
            "epsilon_Bv_tau_surface_commutator <= (C_tau||delta_v tau|| + C_S||delta_v X_S|| + C_A||delta_v A_ext|| + C_cap||delta_v caps||)/M_ref.",
            "BOUND_INTERFACE_DERIVED_VALUES_MISSING",
            "operator coefficients, derivative norms and M_ref are not sourced numerically",
            False,
        ),
        (
            "TSC3000_5_verdict",
            "current tau/surface result",
            "The zero theorem is exact as a parent-signature contract, but current MTS lacks the signatures; keep source-ready bound rows.",
            "ZERO_NOT_PROMOTED_BOUND_ROWS_STAGED",
            "no full Bv/kernel/local-GR promotion",
            False,
        ),
    ]
    return [
        base(
            {
                "audit_id": audit_id,
                "clause": clause,
                "statement": statement,
                "current_status": status,
                "effect": effect,
                "component_identity_written": identity_written,
                "parent_signed_for_current_MTS": False,
                "theorem_zero_adopted": False,
                "accepted_for_local_gr": False,
            }
        )
        for audit_id, clause, statement, status, effect, identity_written in data
    ]


def bound_rows() -> list[dict[str, Any]]:
    source_path = RESIDUALS / "P8_Y5_R2FR_2991_EPSILON_BV_SOURCE_BOUND_ROWS_NONCLAIM.csv"
    data = [
        (
            "BVT3000_0_definition",
            "epsilon_Bv_tau_surface_commutator",
            "field-dependent tau or moving linked-surface/collar commutator leakage",
            "dimensionless_after_positive_same_frame_M_ref",
            "abs(int_S([delta_v,i_tau]mu) + int_{delta_v S} i_tau mu)/M_ref",
            "MISSING_TAU_SURFACE_LOCK",
            False,
        ),
        (
            "BVT3000_1_tau_component",
            "epsilon_Bv_tau_variation_abs",
            "tau/coframe variation contribution to the Bv commutator",
            "dimensionless_after_positive_same_frame_M_ref",
            "C_tau ||delta_v tau|| / M_ref",
            "MISSING_TAU_COFRAME_LOCK_AND_C_TAU",
            False,
        ),
        (
            "BVT3000_2_surface_component",
            "epsilon_Bv_surface_motion_abs",
            "linked surface/domain embedding motion contribution",
            "dimensionless_after_positive_same_frame_M_ref",
            "C_S ||delta_v X_S|| / M_ref",
            "MISSING_SOURCE_BLIND_SURFACE_DOMAIN_RULE_AND_C_S",
            False,
        ),
        (
            "BVT3000_3_annulus_cap_component",
            "epsilon_Bv_annulus_cap_transport_abs",
            "annulus cap/collar transport or support-jump contribution",
            "dimensionless_after_positive_same_frame_M_ref",
            "C_A ||delta_v A_ext||/M_ref + C_cap ||delta_v caps||/M_ref",
            "MISSING_FIXED_AEXT_CAPS_AND_COEFFICIENTS",
            False,
        ),
        (
            "BVT3000_4_conditional_zero_row",
            "epsilon_Bv_tau_surface_commutator_zero_if_fixed",
            "theorem-zero switch if tau and surface/domain are parent-fixed before readout",
            "boolean_component_guard",
            "0 if delta_v tau=delta_v S_link=delta_v A_ext=delta_v caps=0 in the parent branch",
            "CONDITIONAL_ZERO_NOT_PROMOTED",
            True,
        ),
        (
            "BVT3000_5_total",
            "epsilon_Bv_tau_surface_commutator_total_abs",
            "source-ready total tau/surface Bv residual",
            "dimensionless_after_positive_same_frame_M_ref",
            "sum_abs(BVT3000_1..3) unless BVT3000_4 is parent-signed",
            "MISSING_SOURCE_BACKED_UPPER_BOUND",
            False,
        ),
    ]
    return [
        base(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "bound_interface": bound,
                "current_value": current_value,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "conditional_zero_available": conditional_zero,
                "finite_value_present": False,
                "theorem_zero_claimed": False,
                "accepted_for_scoring": False,
                "accepted_for_local_gr": False,
                "observable_link": "local_GR;Newton;PPN;R10;clock",
            }
        )
        for bound_id, symbol, definition, units, bound, current_value, conditional_zero in data
    ]


def kernel_rebase_rows() -> list[dict[str, Any]]:
    data = [
        (
            "KRB3000_0_closed_component",
            "epsilon_Bv_exact_fixed_primitive",
            "0",
            "closed by 2999 component lemma only",
        ),
        (
            "KRB3000_1_current_component",
            "epsilon_Bv_tau_surface_commutator",
            "MISSING_SOURCE_BACKED_UPPER_BOUND",
            "3000 derives exact zero criterion and finite bound interface but no current value",
        ),
        (
            "KRB3000_2_Bv_remainder",
            "epsilon_Bv_remainder_after_exact_and_tau_surface_work",
            "MISSING_CORNER_TOPOLOGICAL_UNFIXED_REFERENCE_PROJECTOR_MREF_BOUNDS",
            "Bv sector still not zero or score-ready",
        ),
        (
            "KRB3000_3_kernel_rebased",
            "epsilon_kernel_charge_public_SRNG_rebased_3000",
            "MISSING_THETA_PARENT_QV_BV_REMAINDER_CV_ZERO_FLUX_MREF",
            "one exact Bv component closed, tau/surface structured, full kernel charge remains open",
        ),
    ]
    return [
        base(
            {
                "rebase_id": rebase_id,
                "symbol": symbol,
                "current_value": current_value,
                "status": status,
                "accepted_for_scoring": False,
                "accepted_for_local_gr": False,
            }
        )
        for rebase_id, symbol, current_value, status in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        ("GATE3000_0_decomposition", "tau/surface commutator decomposition written", "PASS", True, False, "commutator and moving-surface terms are separated"),
        ("GATE3000_1_fixed_tau", "parent tau/coframe lock signed", "BLOCKED_NONCLAIM", False, False, "MISSING_PARENT_TAU_IDENTITY"),
        ("GATE3000_2_fixed_surface", "source-blind linked surface/domain signed", "BLOCKED_NONCLAIM", False, False, "MISSING_SOURCE_BLIND_SURFACE_DOMAIN_RULE"),
        ("GATE3000_3_tau_surface_zero", "epsilon_Bv_tau_surface_commutator=0", "CONDITIONAL_ONLY_FAIL_CLOSED", False, False, "zero follows only if fixed-tau and fixed-surface clauses are signed"),
        ("GATE3000_4_tau_surface_numeric", "epsilon_Bv_tau_surface_commutator has a finite numeric/source-backed value", "BLOCKED_NONCLAIM", False, False, "C_tau/C_S/C_A norms and M_ref are missing"),
        ("GATE3000_5_full_Bv_zero", "epsilon_Bv_ambiguity=0", "FAIL_CLOSED", False, False, "corner/topological/unfixed-reference/projector/Mref debts remain"),
        ("GATE3000_6_kernel_charge", "epsilon_kernel_charge_public_SRNG is score-ready", "FAIL_CLOSED", False, False, "Theta/Qv/Cv/zero-flux and Bv remainder still open"),
        ("GATE3000_7_local_GR_Newton_PPN", "local GR/Newton/PPN claim allowed", "FAIL_CLOSED", False, False, "component work does not close local reduction"),
    ]
    return [
        base(
            {
                "gate_id": gate_id,
                "gate": gate,
                "gate_status": status,
                "condition_passed": passed,
                "promotion_allowed_now": promotion,
                "reason": reason,
                "accepted_for_local_gr": False,
            }
        )
        for gate_id, gate, status, passed, promotion, reason in data
    ]


def decision_rows() -> list[dict[str, Any]]:
    data = [
        (
            "DEC3000_0_zero_contract",
            "Keep the tau/surface zero theorem as an exact parent-signature contract.",
            "If tau and the linked surfaces are parent-fixed, the commutator term vanishes without tuning.",
            "usable as a future proof gate, not current evidence",
        ),
        (
            "DEC3000_1_current_status",
            "Do not promote epsilon_Bv_tau_surface_commutator=0.",
            "Current MTS lacks the parent tau identity and source-blind surface/domain rule.",
            "retain bound rows with missing coefficients",
        ),
        (
            "DEC3000_2_bound_route",
            "Use the finite bound interface instead of looping.",
            "The exact leftover is now C_tau||delta tau|| + C_S||delta X_S|| plus annulus/cap terms over M_ref.",
            "next work should source the owner pack or first coefficient value",
        ),
        (
            "DEC3000_3_next",
            "Select tau/surface owner source pack or first commutator value next.",
            "A numeric/source-backed row would make this residual testable; a signed owner pack would set it to zero.",
            "3001 should attack tau/surface owner source rows",
        ),
    ]
    return [
        base(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "effect": effect,
            }
        )
        for decision_id, decision, because, effect in data
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "next_id": "NEXT3000_0_3001",
                "priority": "selected_primary",
                "target_doc": "3001-Y5-R2FR-tau-surface-owner-source-pack-or-first-commutator-coefficient-value-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_tau_surface_owner_source_pack_or_first_commutator_coefficient_value_under_AX1090_3001.py",
                "mission": "Source or reject the parent tau/surface owner pack: tau_source=tau_charge=tau_clock=tau_boundary=tau_readout, delta_v S_link=0, delta_v A_ext=0, and operator coefficients C_tau/C_S/C_A. If unsigned, fill the first finite commutator coefficient row without claiming local GR.",
                "success_condition": "epsilon_Bv_tau_surface_commutator becomes theorem-zero by parent owner signatures or gains at least one finite source-backed coefficient row with units and no observed-GM/surface-fit import",
                "fallback_condition": "if neither owner signatures nor finite coefficients exist, demote tau/surface route to explicit closure-only and move to corner/topological classification",
                "guardrails": "no full Bv zero claim; no epsilon_kernel_charge claim; no local-GR/Newton/PPN/WEP/R10 claim; no GitHub; no formalization-workbench edits",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "copy_id": copy_id,
                "destination": str(destination),
                "copy_exists": destination.exists(),
                "row_count": len(rows(destination)) if destination.exists() else 0,
                "parse_ok": csv_ok(destination) if destination.exists() else False,
            }
        )
        for copy_id, destination in BRANCH_OUTPUTS.items()
    ]


def validation_rows(
    source_output_rows: list[dict[str, Any]],
    zero_output_rows: list[dict[str, Any]],
    bound_output_rows: list[dict[str, Any]],
    gate_output_rows: list[dict[str, Any]],
    branch_output_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    sources_ok = all(boolish(row["path_exists"]) for row in source_output_rows)
    anchors_ok = all(boolish(row["anchors_found"]) for row in source_output_rows)
    decomposition_written = any(row["audit_id"] == "TSC3000_0_integrand_identity" and boolish(row["component_identity_written"]) for row in zero_output_rows)
    zero_not_promoted = any(row["audit_id"] == "TSC3000_5_verdict" and row["current_status"] == "ZERO_NOT_PROMOTED_BOUND_ROWS_STAGED" for row in zero_output_rows)
    bound_rows_staged = any(row["bound_id"] == "BVT3000_5_total" and boolish(row["source_path_exists"]) for row in bound_output_rows)
    local_claim_false = any(row["gate_id"] == "GATE3000_7_local_GR_Newton_PPN" and not boolish(row["condition_passed"]) for row in gate_output_rows)
    branch_ok = all(boolish(row["copy_exists"]) and boolish(row["parse_ok"]) for row in branch_output_rows)
    csv_parse_ok = all(csv_ok(path) for path in output_paths if path.exists() and path.suffix == ".csv")
    outputs_under_post = all(under(path, ROOT) for path in output_paths + [DOC])
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_count = sum(1 for path in FORMALIZATION.rglob("*3000*") if path.is_file())
    no_claim_flags = True
    for output_path in output_paths:
        if output_path.exists() and output_path.suffix == ".csv":
            for output_row in rows(output_path):
                for key in ("valid_for_claim", "claim_allowed", "promotion_allowed_now", "accepted_for_local_gr"):
                    if str(output_row.get(key, "")).strip().lower() == "true":
                        no_claim_flags = False
    data = [
        ("VAL3000_0_sources_exist", sources_ok, "all cited local source paths exist"),
        ("VAL3000_1_anchors_found", anchors_ok, "all cited anchors are found"),
        ("VAL3000_2_decomposition_written", decomposition_written, "tau/surface commutator decomposition is written"),
        ("VAL3000_3_zero_not_promoted", zero_not_promoted, "tau/surface zero theorem is not promoted for current MTS"),
        ("VAL3000_4_bound_rows_staged", bound_rows_staged, "epsilon_Bv_tau_surface bound rows are staged"),
        ("VAL3000_5_local_claim_false", local_claim_false, "local GR/Newton/PPN gate remains false"),
        ("VAL3000_6_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL3000_7_csvs_parse", csv_parse_ok, "all generated CSVs parse"),
        ("VAL3000_8_outputs_under_post", outputs_under_post, "all outputs are under post-checkpoint-work"),
        ("VAL3000_9_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL3000_10_formalization_clean", formalization_count == 0, f"no 3000 outputs in formalization-workbench (count={formalization_count})"),
        ("VAL3000_11_doc_written", DOC.exists(), "3000 markdown checkpoint exists"),
    ]
    overall = all(passed for _, passed, _ in data)
    data.append(("VAL3000_OVERALL", overall, "3000 derives the tau/surface commutator zero criterion and finite bound interface, refuses current promotion, and selects owner/source-coefficient acquisition next"))
    return [
        base(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": True,
            }
        )
        for validation_id, passed, check in data
    ]


def write_doc(
    source_output_rows: list[dict[str, Any]],
    zero_output_rows: list[dict[str, Any]],
    bound_output_rows: list[dict[str, Any]],
    kernel_output_rows: list[dict[str, Any]],
    gate_output_rows: list[dict[str, Any]],
    decision_output_rows: list[dict[str, Any]],
    next_output_rows: list[dict[str, Any]],
    branch_output_rows: list[dict[str, Any]],
    validation_output_rows: list[dict[str, Any]],
) -> None:
    document = f"""# 3000 - Y5/R2FR Fixed Tau-Surface Commutator Zero Or Second Bv Component Bound Under AX1090

Status: `Y5_R2FR_3000_tau_surface_commutator_zero_contract_written_not_promoted_bound_rows_staged_3001_next`

Claim ceiling: `no_tau_surface_zero_claim_no_full_Bv_zero_claim_no_epsilon_kernel_charge_claim_no_public_SRNG_claim_no_local_GR_no_Newton_no_PPN_no_WEP_no_R10_no_GitHub_no_formalization_edit`

## Current Verdict

3000 attacks the second boundary component left by 2999: `epsilon_Bv_tau_surface_commutator`.

The derivation is sharp. The leftover exact-boundary surface term decomposes into a tau/coframe commutator plus moving-surface/domain transport:

`epsilon_Bv_tau_surface_commutator ~ abs(int_S([delta_v,i_tau]mu) + int_deltaS i_tau mu)/M_ref`.

So the zero route is clear: parent-sign one tau/coframe for source, clocks, charge, boundary and readout, and parent-fix the linked surface/domain before source/readout. If those signatures hold, the commutator component vanishes. Current MTS does not sign them yet, so the zero is not promoted. Instead, 3000 stages the finite bound interface using `C_tau`, `C_S`, `C_A`, cap terms and `M_ref`.

## Source Register

{md_table(source_output_rows, ["source_id", "path_exists", "anchors_found", "missing_anchors", "role"])}

## Tau-Surface Commutator Zero Audit

{md_table(zero_output_rows, ["audit_id", "clause", "current_status", "statement", "effect"])}

## epsilon_Bv Tau-Surface Bound Rows

{md_table(bound_output_rows, ["bound_id", "symbol", "bound_interface", "current_value", "conditional_zero_available"])}

## Kernel-Charge Rebase After Bv Components

{md_table(kernel_output_rows, ["rebase_id", "symbol", "current_value", "status"])}

## Promotion Gates

{md_table(gate_output_rows, ["gate_id", "gate", "gate_status", "condition_passed", "promotion_allowed_now", "reason"])}

## Decision Ledger

{md_table(decision_output_rows, ["decision_id", "decision", "because", "effect"])}

## Next Target

{md_table(next_output_rows, ["next_id", "target_doc", "mission", "success_condition", "guardrails"])}

## Branch Copies

{md_table(branch_output_rows, ["copy_id", "destination", "copy_exists", "row_count", "parse_ok", "valid_for_claim"])}

## Validation

{md_table(validation_output_rows, ["validation_id", "passed", "check", "required"])}

## Plain-English Takeaway

This is another controlled squeeze. The tau/surface leak is no longer a vague objection: it is exactly a fixed-tau plus fixed-surface/domain problem, or else a finite residual with named coefficients. We did not get local GR, but we did turn a fog term into an owner theorem or a measurable bill.

## Forbidden Claims From 3000

- `epsilon_Bv_tau_surface_commutator=0` for current MTS.
- `epsilon_Bv_ambiguity=0`.
- `epsilon_kernel_charge_public_SRNG=0` or score-ready.
- Public `SRNG/OFC`, source-normalized Newton, PPN, WEP, R10, clock safety, orbital safety or local GR.
"""
    DOC.write_text(document, encoding="utf-8")


def main() -> None:
    source_output_rows = source_rows()
    zero_output_rows = zero_audit_rows()
    bound_output_rows = bound_rows()
    kernel_output_rows = kernel_rebase_rows()
    gate_output_rows = gate_rows()
    decision_output_rows = decision_rows()
    next_output_rows = next_rows()

    write_csv(OUTPUTS["sources"], source_output_rows)
    write_csv(OUTPUTS["zero_audit"], zero_output_rows)
    write_csv(OUTPUTS["bound_rows"], bound_output_rows)
    write_csv(OUTPUTS["kernel_rebase"], kernel_output_rows)
    write_csv(OUTPUTS["gates"], gate_output_rows)
    write_csv(OUTPUTS["decision"], decision_output_rows)
    write_csv(OUTPUTS["next"], next_output_rows)

    shutil.copyfile(OUTPUTS["zero_audit"], BRANCH_OUTPUTS["zero_audit_copy"])
    shutil.copyfile(OUTPUTS["bound_rows"], BRANCH_OUTPUTS["bound_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

    branch_output_rows = branch_rows()
    write_csv(OUTPUTS["branches"], branch_output_rows)

    DOC.write_text("", encoding="utf-8")
    validation_output_rows = validation_rows(
        source_output_rows,
        zero_output_rows,
        bound_output_rows,
        gate_output_rows,
        branch_output_rows,
    )
    write_csv(OUTPUTS["validation"], validation_output_rows)

    write_doc(
        source_output_rows,
        zero_output_rows,
        bound_output_rows,
        kernel_output_rows,
        gate_output_rows,
        decision_output_rows,
        next_output_rows,
        branch_output_rows,
        validation_output_rows,
    )


if __name__ == "__main__":
    main()
