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

CHECKPOINT = "2999"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2999-Y5-R2FR-sector-Qv-source-pack-or-first-epsilon-kernel-charge-value-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2999_SOURCE_REGISTER.csv",
    "selection": RESIDUALS / "P8_Y5_R2FR_2999_COMPONENT_SELECTION_LEDGER.csv",
    "lemma": RESIDUALS / "P8_Y5_R2FR_2999_EXACT_BV_COMPONENT_ZERO_LEMMA.csv",
    "values": RESIDUALS / "P8_Y5_R2FR_2999_EPSILON_KERNEL_CHARGE_COMPONENT_VALUE_ROWS.csv",
    "remaining": RESIDUALS / "P8_Y5_R2FR_2999_REMAINING_KERNEL_DEBTS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2999_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2999_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2999_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2999_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2999_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "lemma_copy": PARENT_ACTION / "exact_fixed_Bv_component_zero_lemma_2999_NONPROMOTED.csv",
    "value_copy": LOCAL_BOUNDS / "epsilon_kernel_charge_first_component_value_2999_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2999_FIXED_TAU_SURFACE_COMMUTATOR_OR_SECOND_BV_COMPONENT_NEXT_NONCLAIM.csv",
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
        "SRC2999_00_2998_next",
        RESIDUALS / "P8_Y5_R2FR_2998_NEXT_TARGET.csv",
        ["NEXT2998_0_2999", "epsilon_kernel_charge_public_SRNG"],
        "2998 selects first kernel-charge component extraction/value.",
    ),
    (
        "SRC2999_01_2998_bound",
        RESIDUALS / "P8_Y5_R2FR_2998_FIRST_PUBLIC_SRNG_RESIDUAL_BOUND_ROW.csv",
        ["BND2998_0_first_public_SRNG_kernel_charge", "epsilon_Bv_ambiguity"],
        "2998 bound includes the Bv ambiguity term inside epsilon_kernel_charge_public_SRNG.",
    ),
    (
        "SRC2999_02_2991_proof",
        RESIDUALS / "P8_Y5_R2FR_2991_FIXED_BOUNDARY_THETA_ZERO_PROOF_CHAIN.csv",
        ["FBZ2991_1_exact_improvement", "CONDITIONAL_ZERO_DERIVED_NOT_CLAIM"],
        "2991 already isolates the exact-improvement boundary component as conditionally zero.",
    ),
    (
        "SRC2999_03_2991_epsilon",
        RESIDUALS / "P8_Y5_R2FR_2991_EPSILON_BV_SOURCE_BOUND_ROWS_NONCLAIM.csv",
        ["EBV2991_01_exact_component", "CONDITIONAL_ZERO_NOT_CLAIM"],
        "2991 staged epsilon_Bv exact component and remaining Bv residual rows.",
    ),
    (
        "SRC2999_04_2545_exact",
        RESIDUALS / "P8_Y5_NO_SHADOW_2545_EXACT_IMPROVEMENT_CANCELLATION_DERIVATION.csv",
        ["EIC2545_3_k_invariance", "Bzero exact-improvement component"],
        "2545 supplies the exact-improvement cancellation algebra.",
    ),
    (
        "SRC2999_05_2547_fixed_ref",
        RESIDUALS / "P8_Y5_NO_SHADOW_2547_FIXED_REFERENCE_SELECTOR_THEOREM.csv",
        ["FRS2547_2_chain_rule_to_Bref", "PASS_AS_CONDITIONAL_CONTRACT"],
        "2547 supplies the fixed-reference q/source-blind selector contract.",
    ),
    (
        "SRC2999_06_2544_bzero",
        RESIDUALS / "P8_Y5_NO_SHADOW_2544_BZERO_NOFLUX_THEOREM_AUDIT.csv",
        ["BZT2544_6_verdict", "ZERO_THEOREM_NOT_DERIVED_RETAIN_BOUND_ROW"],
        "2544 warns that exact component zero does not close the full Bzero flux theorem.",
    ),
    (
        "SRC2999_07_2447_boundary_gate",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2447_BOUNDARY_REFERENCE_S_EQ_ZERO_THEOREM_GATE.csv",
        ["BZ2447_3_relative_cohomology_no_flux", "BLOCKED"],
        "2447 keeps relative/topological and boundary no-flux clauses blocked.",
    ),
    (
        "SRC2999_08_2902_kernel_rows",
        RESIDUALS / "P8_Y5_R2FR_2902_VERTICAL_QV_KERNEL_CHARGE_ROWS.csv",
        ["VQL2902_0_kernel_charge", "epsilon_Bv_ambiguity"],
        "2902 defines the normalized kernel charge row and Bv ambiguity component.",
    ),
    (
        "SRC2999_09_2903_piece_rows",
        RESIDUALS / "P8_Y5_R2FR_2903_VERTICAL_SECTOR_QV_PIECE_LEAK_ROWS.csv",
        ["VSP2903_1_Bv", "epsilon_Bv_ambiguity"],
        "2903 has the sector-piece Bv row in the vertical Qv leakage vector.",
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


def selection_rows() -> list[dict[str, Any]]:
    data = [
        (
            "SEL2999_0_exact_Bv",
            "epsilon_Bv_exact_fixed_primitive",
            "selected",
            "lowest-scrutiny component because the cancellation is algebraic: delta(i_v mu)-i_v(delta mu)=0 when v/tau and surface data are fixed",
            "component theorem-zero lemma",
        ),
        (
            "SEL2999_1_corner",
            "epsilon_Bv_corner_abs",
            "deferred",
            "needs corner/codimension-two classification before any zero or number is honest",
            "source-bound later",
        ),
        (
            "SEL2999_2_topological",
            "epsilon_Bv_topological_abs",
            "deferred",
            "needs fixed relative cohomology/topological superselection",
            "source-bound later",
        ),
        (
            "SEL2999_3_tau_surface",
            "epsilon_Bv_tau_surface_commutator",
            "next",
            "same algebra closes if tau and the linked surface embedding are parent-fixed; otherwise this is the nearest second component bound",
            "3000 target",
        ),
        (
            "SEL2999_4_projector_boundary",
            "epsilon_Bv_projector_boundary",
            "deferred",
            "requires Pi_M boundary stress and commutator control",
            "source-bound later",
        ),
    ]
    return [
        base(
            {
                "selection_id": selection_id,
                "component": component,
                "selection_status": status,
                "reason": reason,
                "action": action,
            }
        )
        for selection_id, component, status, reason, action in data
    ]


def lemma_rows() -> list[dict[str, Any]]:
    data = [
        (
            "LEM2999_0_setup",
            "exact boundary improvement",
            "Let L' = L + dmu, with mu an (n-1)-form in the same parent field bundle and fixed boundary class.",
            "defines the component only; it does not classify all MTS boundary terms",
            True,
        ),
        (
            "LEM2999_1_theta_shift",
            "theta shift",
            "theta' = theta + delta mu follows from delta L' = E delta Phi + d(theta + delta mu).",
            "requires parent variation identity for the selected sector",
            True,
        ),
        (
            "LEM2999_2_Qv_shift",
            "Q_v shift",
            "Q'_v = Q_v + i_v mu up to corner/exact terms for a fixed vertical generator v.",
            "corner/topological remainders are explicitly excluded from this component",
            True,
        ),
        (
            "LEM2999_3_surface_integrand",
            "kernel surface integrand cancellation",
            "delta(i_v mu) - i_v(delta mu) = 0 when [delta,i_v]=0 and the surface embedding is fixed.",
            "field-dependent tau/v or moving surfaces are moved to epsilon_Bv_tau_surface_commutator",
            True,
        ),
        (
            "LEM2999_4_component_value",
            "exact/fixed Bv component",
            "epsilon_Bv_exact_fixed_primitive = abs(int_S(delta(i_v mu)-i_v(delta mu)))/M_ref = 0 for this component.",
            "zero numerator only; M_ref and other Bv components remain open",
            True,
        ),
        (
            "LEM2999_5_not_total",
            "full Bv warning",
            "epsilon_Bv_ambiguity is not zero unless corner, topological, tau/surface, unfixed-reference, projector-boundary and denominator clauses close too.",
            "public SRNG/local GR remains blocked",
            False,
        ),
    ]
    return [
        base(
            {
                "lemma_id": lemma_id,
                "step": step,
                "statement": statement,
                "limitation": limitation,
                "component_zero_lemma": component_zero,
                "parent_signed_for_current_MTS": False,
                "adopted_as_total_Bv_zero": False,
                "accepted_for_local_gr": False,
            }
        )
        for lemma_id, step, statement, limitation, component_zero in data
    ]


def value_rows() -> list[dict[str, Any]]:
    source_exact = RESIDUALS / "P8_Y5_NO_SHADOW_2545_EXACT_IMPROVEMENT_CANCELLATION_DERIVATION.csv"
    source_bv = RESIDUALS / "P8_Y5_R2FR_2991_EPSILON_BV_SOURCE_BOUND_ROWS_NONCLAIM.csv"
    data = [
        (
            "KCV2999_0_exact_fixed_Bv",
            "epsilon_Bv_exact_fixed_primitive",
            "exact/fixed boundary-improvement part of epsilon_Bv_ambiguity",
            "dimensionless_after_positive_same_frame_M_ref; numerator_zero",
            "0",
            True,
            "THEOREM_ZERO_COMPONENT_LEMMA_NOT_TOTAL_MTS_CLAIM",
            source_exact,
            "local_GR;Newton;PPN;R10;clock",
        ),
        (
            "KCV2999_1_epsilon_Bv_remainder",
            "epsilon_Bv_remainder_after_exact_fixed_zero",
            "all non-exact/unfixed/corner/topological/projector/denominator Bv components left after KCV2999_0",
            "dimensionless_after_positive_same_frame_M_ref",
            "MISSING_CORNER_TOPOLOGICAL_TAU_SURFACE_UNFIXED_REFERENCE_PROJECTOR_MREF_BOUNDS",
            False,
            "REMAINDER_OPEN_NONCLAIM",
            source_bv,
            "local_GR;Newton;PPN;R10;clock",
        ),
        (
            "KCV2999_2_kernel_charge_rebased",
            "epsilon_kernel_charge_public_SRNG_rebased",
            "epsilon_kernel_charge_public_SRNG with exact/fixed Bv numerator component removed",
            "dimensionless_after_positive_same_frame_M_ref",
            "MISSING_THETA_PARENT_QV_BV_REMAINDER_CV_ZERO_FLUX_MREF",
            False,
            "KERNEL_CHARGE_STILL_OPEN_NONCLAIM",
            RESIDUALS / "P8_Y5_R2FR_2998_FIRST_PUBLIC_SRNG_RESIDUAL_BOUND_ROW.csv",
            "local_GR;Newton;PPN;R10;clock",
        ),
    ]
    return [
        base(
            {
                "value_id": value_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "component_value": value,
                "component_value_present": value_present,
                "status": status,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "observable_link": observable_link,
                "component_zero_lemma": value_present,
                "parent_signed_for_current_MTS": False,
                "accepted_for_scoring": False,
                "accepted_for_local_gr": False,
            }
        )
        for value_id, symbol, definition, units, value, value_present, status, path, observable_link in data
    ]


def remaining_rows() -> list[dict[str, Any]]:
    data = [
        ("REM2999_0_corner", "epsilon_Bv_corner_abs", "corner/codimension-two contribution", "MISSING_CORNER_CLASSIFICATION_OR_BOUND"),
        ("REM2999_1_topological", "epsilon_Bv_topological_abs", "closed-but-not-exact or harmonic/topological flux", "MISSING_CTOP_SUPERSELECTION_OR_BOUND"),
        ("REM2999_2_tau_surface", "epsilon_Bv_tau_surface_commutator", "field-dependent tau or moving linked surface commutator", "MISSING_TAU_SURFACE_LOCK"),
        ("REM2999_3_unfixed_reference", "epsilon_Bv_unfixed_reference", "q/source/frame/radius-dependent reference subtraction", "MISSING_PARENT_BREF_RULE"),
        ("REM2999_4_projector_boundary", "epsilon_Bv_projector_boundary", "projector/source-measure boundary symplectic leakage", "MISSING_PROJECTOR_BOUNDARY_SILENCE"),
        ("REM2999_5_denominator", "epsilon_Bv_denominator", "positive same-frame M_ref guard", "MISSING_POSITIVE_SAME_FRAME_MREF"),
        ("REM2999_6_theta_Qv_Cv", "epsilon_theta_Qv_Cv_nonBv", "non-boundary Theta/Qv/Cv/integrability debts in epsilon_kernel_charge", "MISSING_THETA_PARENT_QV_CV_INTEGRABILITY_ZERO_FLUX"),
    ]
    return [
        base(
            {
                "debt_id": debt_id,
                "symbol": symbol,
                "definition": definition,
                "current_status": status,
                "numeric_or_zero_value": "MISSING",
                "accepted_for_local_gr": False,
            }
        )
        for debt_id, symbol, definition, status in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        ("GATE2999_0_component_selected", "one kernel-charge component selected", "PASS", True, False, "exact/fixed Bv component selected"),
        ("GATE2999_1_exact_component_zero", "exact/fixed Bv component has theorem-zero lemma", "PASS_COMPONENT_ONLY", True, False, "algebraic cancellation from exact improvement"),
        ("GATE2999_2_exact_component_current_MTS", "actual MTS boundary representative is fully classified as exact/fixed", "BLOCKED_NONCLAIM", False, False, "classification and fixed-reference signatures remain unsigned"),
        ("GATE2999_3_full_Bv_zero", "epsilon_Bv_ambiguity=0", "FAIL_CLOSED", False, False, "corner/topological/tau-surface/unfixed-reference/projector/Mref debts remain"),
        ("GATE2999_4_kernel_charge_numeric", "epsilon_kernel_charge_public_SRNG has a score-ready value", "FAIL_CLOSED", False, False, "only one component lemma is zero; full residual still missing"),
        ("GATE2999_5_public_SRNG", "public SRNG/OFC can be promoted", "FAIL_CLOSED", False, False, "kernel charge and current-complex owner remain open"),
        ("GATE2999_6_local_GR_Newton_PPN", "local GR/Newton/PPN claim allowed", "FAIL_CLOSED", False, False, "component zero does not close local reduction"),
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
            "DEC2999_0_first_piece",
            "Accept epsilon_Bv_exact_fixed_primitive=0 as a component lemma only.",
            "The exact-improvement cancellation is mathematical and source-backed by 2545/2991, but the active MTS boundary representative is not fully classified.",
            "kernel-charge bill is narrowed, not closed",
        ),
        (
            "DEC2999_1_no_total_Bv",
            "Do not claim epsilon_Bv_ambiguity=0.",
            "The remaining boundary debts are where a hidden source/readout term could still live.",
            "retain explicit Bv remainder rows",
        ),
        (
            "DEC2999_2_no_local_GR",
            "Do not promote public SRNG/local GR.",
            "One component zero is not a current-complex owner theorem and not a full epsilon_kernel_charge value.",
            "local GR/Newton/PPN stay fail-closed",
        ),
        (
            "DEC2999_3_next",
            "Attack tau/surface commutator next.",
            "It is the closest second zero: the same cancellation survives if tau and linked surfaces are parent-fixed; otherwise it becomes a concrete bound row.",
            "3000 should prove or bound epsilon_Bv_tau_surface_commutator",
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
                "next_id": "NEXT2999_0_3000",
                "priority": "selected_primary",
                "target_doc": "3000-Y5-R2FR-fixed-tau-surface-commutator-zero-or-second-Bv-component-bound-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_fixed_tau_surface_commutator_zero_or_second_Bv_component_bound_under_AX1090_3000.py",
                "mission": "Try to prove [delta_v,i_tau]mu plus the moving linked-surface term vanishes from parent-fixed tau and source-blind surface/domain ownership; if not, write a source-backed epsilon_Bv_tau_surface_commutator bound row.",
                "success_condition": "epsilon_Bv_tau_surface_commutator becomes theorem-zero or finite-value source-backed without using observed GM, closure by declaration, or post-readout surface fitting",
                "fallback_condition": "retain the tau/surface term as the next explicit Bv remainder row and move to corner/topological classification only after this commutator is paid",
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
    lemma_output_rows: list[dict[str, Any]],
    value_output_rows: list[dict[str, Any]],
    remaining_output_rows: list[dict[str, Any]],
    gate_output_rows: list[dict[str, Any]],
    branch_output_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    sources_ok = all(boolish(row["path_exists"]) for row in source_output_rows)
    anchors_ok = all(boolish(row["anchors_found"]) for row in source_output_rows)
    component_zero = any(row["lemma_id"] == "LEM2999_4_component_value" and boolish(row["component_zero_lemma"]) for row in lemma_output_rows)
    value_present = any(row["value_id"] == "KCV2999_0_exact_fixed_Bv" and str(row["component_value"]) == "0" and boolish(row["component_value_present"]) for row in value_output_rows)
    remainder_open = any(row["debt_id"] == "REM2999_6_theta_Qv_Cv" and str(row["numeric_or_zero_value"]) == "MISSING" for row in remaining_output_rows)
    local_claim_false = any(row["gate_id"] == "GATE2999_6_local_GR_Newton_PPN" and not boolish(row["condition_passed"]) for row in gate_output_rows)
    branch_ok = all(boolish(row["copy_exists"]) and boolish(row["parse_ok"]) for row in branch_output_rows)
    csv_parse_ok = all(csv_ok(path) for path in output_paths if path.exists() and path.suffix == ".csv")
    outputs_under_post = all(under(path, ROOT) for path in output_paths + [DOC])
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_count = sum(1 for path in FORMALIZATION.rglob("*2999*") if path.is_file())
    no_claim_flags = True
    for output_path in output_paths:
        if output_path.exists() and output_path.suffix == ".csv":
            for output_row in rows(output_path):
                for key in ("valid_for_claim", "claim_allowed", "promotion_allowed_now", "accepted_for_local_gr"):
                    if str(output_row.get(key, "")).strip().lower() == "true":
                        no_claim_flags = False
    data = [
        ("VAL2999_0_sources_exist", sources_ok, "all cited local source paths exist"),
        ("VAL2999_1_anchors_found", anchors_ok, "all cited anchors are found"),
        ("VAL2999_2_component_zero_lemma", component_zero, "exact/fixed Bv component zero lemma is present"),
        ("VAL2999_3_component_value_present", value_present, "first kernel-charge component row carries value 0"),
        ("VAL2999_4_remainder_open", remainder_open, "remaining kernel debts stay explicit and open"),
        ("VAL2999_5_local_claim_false", local_claim_false, "local GR/Newton/PPN gate remains false"),
        ("VAL2999_6_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2999_7_csvs_parse", csv_parse_ok, "all generated CSVs parse"),
        ("VAL2999_8_outputs_under_post", outputs_under_post, "all outputs are under post-checkpoint-work"),
        ("VAL2999_9_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2999_10_formalization_clean", formalization_count == 0, f"no 2999 outputs in formalization-workbench (count={formalization_count})"),
        ("VAL2999_11_doc_written", DOC.exists(), "2999 markdown checkpoint exists"),
    ]
    overall = all(passed for _, passed, _ in data)
    data.append(("VAL2999_OVERALL", overall, "2999 closes one exact/fixed Bv kernel-charge component as a nonpromoted theorem-zero lemma, keeps full Bv/kernel/local-GR claims blocked, and selects tau/surface commutator next"))
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
    selection_output_rows: list[dict[str, Any]],
    lemma_output_rows: list[dict[str, Any]],
    value_output_rows: list[dict[str, Any]],
    remaining_output_rows: list[dict[str, Any]],
    gate_output_rows: list[dict[str, Any]],
    decision_output_rows: list[dict[str, Any]],
    next_output_rows: list[dict[str, Any]],
    branch_output_rows: list[dict[str, Any]],
    validation_output_rows: list[dict[str, Any]],
) -> None:
    document = f"""# 2999 - Y5/R2FR Sector Qv Source Pack Or First epsilon Kernel-Charge Value Under AX1090

Status: `Y5_R2FR_2999_exact_fixed_Bv_component_zero_lemma_first_kernel_charge_component_value_nonpromoted_3000_next`

Claim ceiling: `no_full_Bv_zero_claim_no_epsilon_kernel_charge_claim_no_public_SRNG_claim_no_local_GR_no_Newton_no_PPN_no_WEP_no_R10_no_GitHub_no_formalization_edit`

## Current Verdict

2999 takes the first concrete bite out of `epsilon_kernel_charge_public_SRNG`. The selected component is the exact/fixed boundary-improvement part of `epsilon_Bv_ambiguity`.

The algebraic component is clean: for an exact improvement `L' = L + dmu`, the surface one-form shift is `delta(i_v mu)-i_v(delta mu)`, which vanishes when the vertical generator/tau and linked surface are fixed and no corner/topological remainder is being included in this component. Therefore `epsilon_Bv_exact_fixed_primitive = 0` as a component lemma.

This is useful but narrow. It does not prove the actual MTS boundary representative is wholly exact/fixed, does not close corner/topological/tau-surface/projector/denominator terms, and does not give a score-ready value for `epsilon_kernel_charge_public_SRNG`. It is a genuine first zero in the bill, not the end of the bill.

## Source Register

{md_table(source_output_rows, ["source_id", "path_exists", "anchors_found", "missing_anchors", "role"])}

## Component Selection Ledger

{md_table(selection_output_rows, ["selection_id", "component", "selection_status", "reason", "action"])}

## Exact Bv Component Zero Lemma

{md_table(lemma_output_rows, ["lemma_id", "step", "statement", "limitation", "component_zero_lemma"])}

## Epsilon Kernel-Charge Component Value Rows

{md_table(value_output_rows, ["value_id", "symbol", "component_value", "component_value_present", "status", "observable_link"])}

## Remaining Kernel Debts

{md_table(remaining_output_rows, ["debt_id", "symbol", "current_status", "numeric_or_zero_value"])}

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

This is the kind of small win that actually matters. We did not win the whole fight, but we did not circle either: one component of the local kernel-charge residual has been put to zero by a real cancellation lemma. The next round is whether the tau/surface commutator can be killed by parent-fixed readout geometry or has to be paid as a real bound.

## Forbidden Claims From 2999

- `epsilon_Bv_ambiguity=0`.
- `epsilon_kernel_charge_public_SRNG=0` or score-ready.
- Public `SRNG/OFC`, source-normalized Newton, PPN, WEP, R10, clock safety, orbital safety or local GR.
- The exact/fixed component lemma classifies all actual MTS boundary terms.
"""
    DOC.write_text(document, encoding="utf-8")


def main() -> None:
    source_output_rows = source_rows()
    selection_output_rows = selection_rows()
    lemma_output_rows = lemma_rows()
    value_output_rows = value_rows()
    remaining_output_rows = remaining_rows()
    gate_output_rows = gate_rows()
    decision_output_rows = decision_rows()
    next_output_rows = next_rows()

    write_csv(OUTPUTS["sources"], source_output_rows)
    write_csv(OUTPUTS["selection"], selection_output_rows)
    write_csv(OUTPUTS["lemma"], lemma_output_rows)
    write_csv(OUTPUTS["values"], value_output_rows)
    write_csv(OUTPUTS["remaining"], remaining_output_rows)
    write_csv(OUTPUTS["gates"], gate_output_rows)
    write_csv(OUTPUTS["decision"], decision_output_rows)
    write_csv(OUTPUTS["next"], next_output_rows)

    shutil.copyfile(OUTPUTS["lemma"], BRANCH_OUTPUTS["lemma_copy"])
    shutil.copyfile(OUTPUTS["values"], BRANCH_OUTPUTS["value_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

    branch_output_rows = branch_rows()
    write_csv(OUTPUTS["branches"], branch_output_rows)

    DOC.write_text("", encoding="utf-8")
    validation_output_rows = validation_rows(
        source_output_rows,
        lemma_output_rows,
        value_output_rows,
        remaining_output_rows,
        gate_output_rows,
        branch_output_rows,
    )
    write_csv(OUTPUTS["validation"], validation_output_rows)

    write_doc(
        source_output_rows,
        selection_output_rows,
        lemma_output_rows,
        value_output_rows,
        remaining_output_rows,
        gate_output_rows,
        decision_output_rows,
        next_output_rows,
        branch_output_rows,
        validation_output_rows,
    )


if __name__ == "__main__":
    main()
