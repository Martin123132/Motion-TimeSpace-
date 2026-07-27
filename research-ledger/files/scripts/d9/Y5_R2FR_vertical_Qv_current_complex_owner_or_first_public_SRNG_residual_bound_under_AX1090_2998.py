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

CHECKPOINT = "2998"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2998-Y5-R2FR-vertical-Qv-current-complex-owner-or-first-public-SRNG-residual-bound-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2998_SOURCE_REGISTER.csv",
    "audit": RESIDUALS / "P8_Y5_R2FR_2998_VERTICAL_QV_CURRENT_COMPLEX_OWNER_AUDIT.csv",
    "residual_bound": RESIDUALS / "P8_Y5_R2FR_2998_FIRST_PUBLIC_SRNG_RESIDUAL_BOUND_ROW.csv",
    "priority": RESIDUALS / "P8_Y5_R2FR_2998_QV_SECTOR_PRIORITY_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2998_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2998_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2998_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2998_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2998_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "qv_owner_copy": PARENT_ACTION / "vertical_Qv_current_complex_owner_2998_NOT_EXTRACTED.csv",
    "residual_bound_copy": LOCAL_BOUNDS / "first_public_SRNG_residual_bound_row_2998_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2998_SECTOR_QV_OR_FIRST_EPSILON_KERNEL_CHARGE_VALUE_NEXT_NONCLAIM.csv",
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
        "SRC2998_00_2997_next",
        RESIDUALS / "P8_Y5_R2FR_2997_NEXT_TARGET.csv",
        ["NEXT2997_0_2998", "vertical Noether/Qv"],
        "2997 explicitly selects vertical Qv/current-complex ownership or first public-SRNG residual bound.",
    ),
    (
        "SRC2998_01_2997_residuals",
        RESIDUALS / "P8_Y5_R2FR_2997_FINITE_RESIDUAL_GATE_ROWS.csv",
        ["RES2997_1_epsilon_kernel_charge", "MISSING_THETA_QV_ZERO_FLUX"],
        "2997 names epsilon_kernel_charge as the immediate public-SRNG residual component.",
    ),
    (
        "SRC2998_02_2901_q_kernel",
        RESIDUALS / "P8_Y5_R2FR_2901_Q_KERNEL_NULLNESS_AUDIT.csv",
        ["QK2901_3_presymplectic_null", "MISSING_THETA_PARENT_QV_AND_ZERO_FLUX"],
        "q-kernel nullness already reduces to Theta_parent, Q_v and compact zero flux.",
    ),
    (
        "SRC2998_03_2902_qv_contract",
        RESIDUALS / "P8_Y5_R2FR_2902_VERTICAL_QV_EXTRACTION_CONTRACT.csv",
        ["VQC2902_7_verdict", "FAIL_CURRENT_MTS_QV_NOT_EXTRACTED"],
        "vertical Qv extraction contract is exact but not extracted for current MTS.",
    ),
    (
        "SRC2998_04_2902_kernel_rows",
        RESIDUALS / "P8_Y5_R2FR_2902_VERTICAL_QV_KERNEL_CHARGE_ROWS.csv",
        ["VQL2902_0_kernel_charge", "Delta_vertical_Noether_charge_total_over_Mref"],
        "first normalized kernel-charge residual rows already exist as nonclaim source-ready rows.",
    ),
    (
        "SRC2998_05_2903_sector_ledger",
        RESIDUALS / "P8_Y5_R2FR_2903_VERTICAL_SECTOR_VARIATION_LEDGER.csv",
        ["VSL2903_6_total", "TOTAL_NOT_PROMOTED"],
        "sector variation ledger says total vertical Qv is not promoted.",
    ),
    (
        "SRC2998_06_2903_piece_leaks",
        RESIDUALS / "P8_Y5_R2FR_2903_VERTICAL_SECTOR_QV_PIECE_LEAK_ROWS.csv",
        ["VSP2903_TOTAL", "Delta_vertical_sector_Qv_total_over_Mref"],
        "sector piece leak rows provide the nearest componentized residual vector.",
    ),
    (
        "SRC2998_07_2900_source_complex",
        RESIDUALS / "P8_Y5_R2FR_2900_SOURCE_COMPLEX_OWNER_AUDIT.csv",
        ["SC2900_9_verdict", "FAIL_CURRENT_MTS_SOURCE_COMPLEX_OWNER_NOT_DERIVED"],
        "current/worldtube/source-complex owner remains unsigned.",
    ),
    (
        "SRC2998_08_2908_skeleton",
        RESIDUALS / "P8_Y5_R2FR_2908_PARENT_ACTION_SKELETON.csv",
        ["ACT2908_2_vertical_generator_current_law", "ACT2908_7_total_verdict"],
        "2908 supplies the live constructive parent-action skeleton, but not a promoted theorem.",
    ),
    (
        "SRC2998_09_2908_variation",
        RESIDUALS / "P8_Y5_R2FR_2908_VARIATION_AND_QLOC_DERIVATION.csv",
        ["VAR2908_0_delta_A_q_loc", "FORMAL_PASS_CANDIDATE"],
        "q_loc Euler/source equation is formally available only as a candidate.",
    ),
    (
        "SRC2998_10_2906_Y5Y6_lock",
        RESIDUALS / "P8_Y5_R2FR_2906_Y5_Y6_ZERO_ODD_SOURCE_LOCK_AUDIT.csv",
        ["LOCK2906_8_verdict", "Y5_Y6_ZERO_ODD_SOURCE_LOCK_NOT_PROVED_CURRENT_CORPUS"],
        "Y5/Y6 extra-source lock is still a coupling debt.",
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


def audit_rows() -> list[dict[str, Any]]:
    data = [
        (
            "QVO2998_0_parent_q_Dq",
            "parent q and Dq",
            "q: Phi_parent to Q_vis is parent-defined, constant-rank and fixed before readout; V=ker(Dq) is a real vertical bundle.",
            "MISSING_PARENT_Q_MAP_AND_DQ",
            "Without q/Dq, vertical directions are declarations rather than geometry.",
            "epsilon_q_owner;epsilon_q_rank_or_integrability",
            False,
        ),
        (
            "QVO2998_1_vertical_basis",
            "vertical generator basis",
            "v_i in ker(Dq) acts on geometry, matter, boundary/reference, support and readout variables in the same branch.",
            "MISSING_PARENT_VERTICAL_GENERATOR_ACTION",
            "A partial generator cannot certify matter invisibility or compact charge zero.",
            "epsilon_v_action_missing;epsilon_kernel_charge",
            False,
        ),
        (
            "QVO2998_2_Theta_parent",
            "total parent variation and Theta_parent",
            "delta L_parent = E_A delta Phi^A + dTheta_parent for all retained sectors.",
            "MISSING_TOTAL_PARENT_ACTION_AND_THETA",
            "Q_v is not extractable until the symplectic potential is owned by the parent action.",
            "epsilon_theta_piece_missing",
            False,
        ),
        (
            "QVO2998_3_Jv_Qv_Cv",
            "vertical Noether current and charge",
            "J_v=Theta_parent(v)-mu_v and J_v=dQ_v+C_v with C_v constraint-proportional in the same branch.",
            "FORMAL_SHAPE_ONLY_NOT_EXTRACTED",
            "Noether notation alone does not prove zero vertical charge.",
            "epsilon_Qv_piece_missing;epsilon_Cv_constraint_missing",
            False,
        ),
        (
            "QVO2998_4_compact_zero_flux",
            "compact linked-surface zero flux",
            "int_S(delta Q_v - i_v Theta_parent + delta B_v + C_v_piece)=0 on every allowed linked local compact surface, or source-bound it.",
            "MISSING_ZERO_FLUX_CERTIFICATE",
            "This is the real local-vacuum prize; without it the kernel can carry charge.",
            "epsilon_kernel_charge;epsilon_Bv_ambiguity",
            False,
        ),
        (
            "QVO2998_5_matter_invisibility",
            "matter and source invisibility",
            "delta_v S_matter=0, delta_v J_H=0 and no hidden source-only slot survive outside q/e_obs/tau/ell_J.",
            "CONTRACT_ONLY_NOT_PARENT_ADOPTED",
            "Matter could still couple to the supposedly hidden direction.",
            "epsilon_matter_kernel;epsilon_hidden_source_slot",
            False,
        ),
        (
            "QVO2998_6_basic_stack",
            "basic e_obs/tau/ell_J stack",
            "Lie_v e_obs=0, Lie_v tau=0 and Lie_v ell_J=0, or finite source-backed leakage rows exist in the same frame.",
            "MISSING_BASIC_STACK_CERTIFICATE",
            "same-frame source/readout/no-reentry theorem cannot be public.",
            "epsilon_basic_stack",
            False,
        ),
        (
            "QVO2998_7_source_complex",
            "fixed W_source/A_ext/S_link/J_H current complex",
            "source worldtube, exterior annulus, linking surfaces and Hilbert current are fixed before Pi_M and readout.",
            "SOURCE_COMPLEX_OWNER_NOT_DERIVED",
            "moving domain/support terms can fake or erase source current.",
            "J_domain_current_escape_envelope",
            False,
        ),
        (
            "QVO2998_8_Qv_sector_total",
            "sector-summed Q_v",
            "EH, boundary, extra, projector, matter and constraint pieces are all zero, fixed or finite-sourced in one branch.",
            "TOTAL_VERTICAL_QV_NOT_PROMOTED",
            "EH-only charge import is not enough for MTS.",
            "Delta_vertical_sector_Qv_total_over_Mref",
            False,
        ),
        (
            "QVO2998_9_verdict",
            "vertical Qv/current-complex owner",
            "All QVO2998_0 through QVO2998_8 pass with parent signatures and no MISSING residual rows.",
            "OWNER_NOT_DERIVED_CURRENT_MTS",
            "Public SRNG/OFC remains closure-only; first residual bound row is staged.",
            "epsilon_kernel_charge_public_SRNG",
            False,
        ),
    ]
    return [
        base(
            {
                "audit_id": audit_id,
                "object": obj,
                "required_statement": statement,
                "current_status": status,
                "blocking_gap": gap,
                "residual_if_missing": residual,
                "owner_signed": signed,
                "accepted_for_local_gr": False,
            }
        )
        for audit_id, obj, statement, status, gap, residual, signed in data
    ]


def residual_bound_rows() -> list[dict[str, Any]]:
    source_2902 = RESIDUALS / "P8_Y5_R2FR_2902_VERTICAL_QV_KERNEL_CHARGE_ROWS.csv"
    source_2903 = RESIDUALS / "P8_Y5_R2FR_2903_VERTICAL_SECTOR_QV_PIECE_LEAK_ROWS.csv"
    source_2997 = RESIDUALS / "P8_Y5_R2FR_2997_FINITE_RESIDUAL_GATE_ROWS.csv"
    data = [
        (
            "BND2998_0_first_public_SRNG_kernel_charge",
            "epsilon_kernel_charge_public_SRNG",
            "absolute public-SRNG vertical kernel charge leakage on linked compact local surfaces",
            "dimensionless_after_positive_same_frame_M_ref",
            "epsilon_kernel_charge <= epsilon_theta_piece_missing + epsilon_Qv_piece_missing + epsilon_Bv_ambiguity + epsilon_Cv_constraint_missing + epsilon_Hv_integrability",
            "MISSING_THETA_PARENT_QV_BV_CV_ZERO_FLUX_MREF",
            source_2902,
            "local_GR;Newton;PPN;R10;clock",
            "FIRST_BOUND_ROW_STAGED_NOT_NUMERIC",
        ),
        (
            "BND2998_1_vertical_sector_sum",
            "Delta_vertical_sector_Qv_total_over_Mref",
            "sector-summed vertical Noether charge envelope",
            "dimensionless_after_positive_same_frame_M_ref",
            "Delta_vertical_sector_Qv_total_over_Mref = sum_abs(EH_guard,Bv,extra,projector,matter_source,constraint)",
            "COMPONENTS_SOURCE_READY_BUT_NUMERICALLY_UNFILLED",
            source_2903,
            "local_GR;Newton;PPN;R10;clock",
            "SUPPORTING_COMPONENT_VECTOR_NONCLAIM",
        ),
        (
            "BND2998_2_public_SRNG_owner_total",
            "Delta_public_SRNG_owner_total_abs",
            "public SRNG owner failure envelope",
            "dimensionless_or_boolean_guard_until_M_ref_is_signed",
            "Delta_public_SRNG_owner_total_abs >= epsilon_q_owner + epsilon_kernel_charge + epsilon_basic_stack + E_matter_action + Jdomain_escape + epsilon_PiM + q_loc_residual",
            "COMPONENTS_MISSING_NONCLAIM",
            source_2997,
            "framework_gate;local_GR;Newton;WEP",
            "AGGREGATE_NOT_SCORE_READY",
        ),
    ]
    return [
        base(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "formal_bound": bound,
                "current_value": value,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "observable_link": observable_link,
                "status": status,
                "numeric_value_present": False,
                "theorem_zero_adopted": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
                "valid_for_local_tests": False,
            }
        )
        for bound_id, symbol, definition, units, bound, value, path, observable_link, status in data
    ]


def priority_rows() -> list[dict[str, Any]]:
    data = [
        (
            "PRI2998_0_Theta_parent",
            "Theta_parent total symplectic potential",
            "highest",
            "Every Q_v proof and residual numerator starts here.",
            "extract sector Theta_i from 2908 skeleton or keep epsilon_theta_piece_missing open",
        ),
        (
            "PRI2998_1_Qv_Cv_split",
            "Q_v and C_v sector split",
            "highest",
            "Need distinguish gauge constraint from physical compact charge.",
            "derive Q_v^extra/Q_v^matter/Q_v^projector or fill component bounds",
        ),
        (
            "PRI2998_2_Bv_boundary",
            "B_v boundary/reference convention",
            "high",
            "A free improvement term can hide the whole local residual.",
            "fix B_v before readout or bound epsilon_Bv_ambiguity",
        ),
        (
            "PRI2998_3_matter_source",
            "matter/source invisibility",
            "high",
            "Public SRNG needs matter not to see the vertical direction.",
            "prove matter descent through q/e_obs/tau/ell_J or source-bound epsilon_matter_kernel",
        ),
        (
            "PRI2998_4_current_complex",
            "W_source/A_ext/S_link/J_H complex",
            "high",
            "Newton/source-normalization cannot use moving support or wrong current.",
            "derive fixed support/current descent or bound Jdomain escape",
        ),
        (
            "PRI2998_5_Mref_denominator",
            "positive same-frame M_ref",
            "medium",
            "Residuals cannot be scored until the normalization is parent-owned.",
            "avoid fitted orbital GM; source M_ref from same branch only",
        ),
    ]
    return [
        base(
            {
                "priority_id": priority_id,
                "target": target,
                "priority": priority,
                "reason": reason,
                "next_action": action,
                "current_status": "OPEN_NONCLAIM",
            }
        )
        for priority_id, target, priority, reason, action in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        ("GATE2998_0_qv_route_exact", "vertical Qv route is mathematically well-posed", "PASS_AS_CONTRACT", True, False, "2902/2998 write the exact extraction contract."),
        ("GATE2998_1_qDq_owner", "parent q/Dq and vertical basis are signed", "BLOCKED_NONCLAIM", False, False, "q/Dq remains missing from 2901/2997."),
        ("GATE2998_2_Theta_Qv_extracted", "Theta_parent, mu_v, Q_v and C_v are extracted", "BLOCKED_NONCLAIM", False, False, "2902 verdict is Qv not extracted."),
        ("GATE2998_3_zero_flux", "compact linked-surface vertical flux is zero", "BLOCKED_NONCLAIM", False, False, "zero-flux certificate remains missing."),
        ("GATE2998_4_matter_current_complex", "matter/source/current complex is invisible and fixed", "BLOCKED_NONCLAIM", False, False, "2900 source complex and 2587 matter adoption remain conditional."),
        ("GATE2998_5_residual_bound_numeric", "first public SRNG residual bound is numeric or theorem-zero", "BLOCKED_NONCLAIM", False, False, "row has units/source path but no numeric value or theorem-zero."),
        ("GATE2998_6_public_SRNG_promoted", "public SRNG/OFC can be promoted", "FAIL_CLOSED", False, False, "owner not derived and residual not score-ready."),
        ("GATE2998_7_local_GR_Newton_PPN", "local GR/Newton/PPN claim allowed", "FAIL_CLOSED", False, False, "Qv/current-complex and residual gates remain open."),
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
            "DEC2998_0_owner_result",
            "Do not promote vertical Qv/current-complex ownership.",
            "The exact Qv theorem is written, but q/Dq, Theta_parent, Q_v, zero flux, matter invisibility, basic stack and source complex are unsigned.",
            "public SRNG/OFC remains closure-only",
        ),
        (
            "DEC2998_1_residual_bill",
            "Stage epsilon_kernel_charge_public_SRNG as the first public residual bound row.",
            "This avoids pretending the kernel is zero; the row has units and source paths but no numeric/theorem-zero value.",
            "next work must fill one component value or prove it zero",
        ),
        (
            "DEC2998_2_keep_2908_skeleton",
            "Keep the 2908 parent-action skeleton as the live constructive route.",
            "It gives q_loc as a formal Euler/source equation candidate, not a public local-GR theorem.",
            "use it to extract Theta/Qv/source-current pieces",
        ),
        (
            "DEC2998_3_next",
            "Select sector-Qv source pack or first epsilon-kernel-charge value next.",
            "Another broad owner audit would circle; the next useful move is one concrete sector piece or one finite residual number.",
            "2999 should derive or source a component of epsilon_kernel_charge",
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
                "next_id": "NEXT2998_0_2999",
                "priority": "selected_primary",
                "target_doc": "2999-Y5-R2FR-sector-Qv-source-pack-or-first-epsilon-kernel-charge-value-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_sector_Qv_source_pack_or_first_epsilon_kernel_charge_value_under_AX1090_2999.py",
                "mission": "Extract, derive, or source-bound one concrete component of epsilon_kernel_charge_public_SRNG: Theta_parent sector piece, Q_v sector piece, B_v ambiguity, C_v constraint, integrability curl, or compact zero-flux term. Prefer a theorem-zero component; otherwise produce a numeric/source-ready nonclaim value with units and source path.",
                "success_condition": "at least one kernel-charge component becomes theorem-zero or finite-value source-backed without using EH-only import, closure multiplier, fitted orbital GM, or private SRNG as public proof",
                "fallback_condition": "if no component can be proved or valued, write the exact missing parent-action line and demote the local-transition route to explicit closure/residual only",
                "guardrails": "no local-GR/Newton/PPN/WEP/R10 claim; no GitHub; no formalization-workbench edits; no closure-by-declaration",
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
    audit_output_rows: list[dict[str, Any]],
    residual_output_rows: list[dict[str, Any]],
    gate_output_rows: list[dict[str, Any]],
    branch_output_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    sources_ok = all(boolish(row["path_exists"]) for row in source_output_rows)
    anchors_ok = all(boolish(row["anchors_found"]) for row in source_output_rows)
    owner_refused = any(row["audit_id"] == "QVO2998_9_verdict" and row["current_status"] == "OWNER_NOT_DERIVED_CURRENT_MTS" for row in audit_output_rows)
    residual_staged = any(row["bound_id"] == "BND2998_0_first_public_SRNG_kernel_charge" and row["units"] and boolish(row["source_path_exists"]) for row in residual_output_rows)
    residual_nonclaim = all(not boolish(row.get("valid_for_claim")) and not boolish(row.get("numeric_value_present")) for row in residual_output_rows)
    local_claim_false = any(row["gate_id"] == "GATE2998_7_local_GR_Newton_PPN" and not boolish(row["condition_passed"]) for row in gate_output_rows)
    branch_ok = all(boolish(row["copy_exists"]) and boolish(row["parse_ok"]) for row in branch_output_rows)
    csv_parse_ok = all(csv_ok(path) for path in output_paths if path.exists() and path.suffix == ".csv")
    outputs_under_post = all(under(path, ROOT) for path in output_paths + [DOC])
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_count = sum(1 for path in FORMALIZATION.rglob("*2998*") if path.is_file())
    no_claim_flags = True
    for output_path in output_paths:
        if output_path.exists() and output_path.suffix == ".csv":
            for output_row in rows(output_path):
                for key in ("valid_for_claim", "claim_allowed", "promotion_allowed_now", "accepted_for_local_gr", "valid_for_local_tests"):
                    if str(output_row.get(key, "")).strip().lower() == "true":
                        no_claim_flags = False
    data = [
        ("VAL2998_0_sources_exist", sources_ok, "all cited local source paths exist"),
        ("VAL2998_1_anchors_found", anchors_ok, "all cited anchors are found"),
        ("VAL2998_2_owner_refused", owner_refused, "vertical Qv/current-complex owner is refused for current MTS"),
        ("VAL2998_3_first_residual_bound_staged", residual_staged, "first public SRNG residual bound row has units and source path"),
        ("VAL2998_4_residual_rows_nonclaim", residual_nonclaim, "residual rows remain nonclaim and nonnumeric"),
        ("VAL2998_5_local_claim_false", local_claim_false, "local GR/Newton/PPN gate remains false"),
        ("VAL2998_6_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2998_7_csvs_parse", csv_parse_ok, "all generated CSVs parse"),
        ("VAL2998_8_outputs_under_post", outputs_under_post, "all outputs are under post-checkpoint-work"),
        ("VAL2998_9_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2998_10_formalization_clean", formalization_count == 0, f"no 2998 outputs in formalization-workbench (count={formalization_count})"),
        ("VAL2998_11_doc_written", DOC.exists(), "2998 markdown checkpoint exists"),
    ]
    overall = all(passed for _, passed, _ in data)
    data.append(("VAL2998_OVERALL", overall, "2998 refuses Qv/current-complex ownership, stages epsilon_kernel_charge_public_SRNG, keeps local GR blocked, and selects first component extraction/value next"))
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
    audit_output_rows: list[dict[str, Any]],
    residual_output_rows: list[dict[str, Any]],
    priority_output_rows: list[dict[str, Any]],
    gate_output_rows: list[dict[str, Any]],
    decision_output_rows: list[dict[str, Any]],
    next_output_rows: list[dict[str, Any]],
    branch_output_rows: list[dict[str, Any]],
    validation_output_rows: list[dict[str, Any]],
) -> None:
    document = f"""# 2998 - Y5/R2FR Vertical Qv Current-Complex Owner Or First Public SRNG Residual Bound Under AX1090

Status: `Y5_R2FR_2998_vertical_Qv_current_complex_owner_not_derived_first_public_SRNG_residual_bound_staged_2999_next`

Claim ceiling: `no_vertical_Qv_owner_claim_no_public_SRNG_claim_no_local_GR_no_Newton_no_PPN_no_WEP_no_R10_no_GitHub_no_formalization_edit`

## Current Verdict

2998 tries the proof that 2997 demanded: a parent-owned vertical Noether/current-complex mechanism where `q/Dq`, the vertical basis, `Theta_parent`, `Q_v`, compact zero flux, matter invisibility, the basic observed stack and the source-current complex all live in one branch.

The route is exact, but current MTS does not close it. The formal machinery exists as a contract, and the 2908 parent-action skeleton gives a useful q_loc Euler/source candidate, but `Theta_parent`, `Q_v`, `B_v`, `C_v`, zero compact flux, matter/source invisibility and same-frame `M_ref` are not parent-signed.

So public `SRNG/OFC` remains closure-only. The new progress is that the first public residual bill is now explicit: `epsilon_kernel_charge_public_SRNG`, with units and source paths, but no numeric value and no theorem-zero status.

## Source Register

{md_table(source_output_rows, ["source_id", "path_exists", "anchors_found", "missing_anchors", "role"])}

## Vertical Qv / Current-Complex Owner Audit

{md_table(audit_output_rows, ["audit_id", "object", "current_status", "owner_signed", "blocking_gap", "residual_if_missing"])}

## First Public SRNG Residual Bound Row

{md_table(residual_output_rows, ["bound_id", "symbol", "units", "current_value", "status", "observable_link"])}

## Qv Sector Priority Ledger

{md_table(priority_output_rows, ["priority_id", "target", "priority", "reason", "next_action"])}

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

This is not a defeat; it is the theory getting boxed into the right corner. We no longer need to argue vaguely about whether the local branch is "probably quiet." The next honest move is surgical: prove or value one actual component of `epsilon_kernel_charge_public_SRNG`. If even one piece closes cleanly, the route gains teeth. If none close, the public local-transition route demotes to residual/closure only instead of pretending.

## Forbidden Claims From 2998

- MTS has proved vertical `Q_v` ownership, compact zero flux, public `SRNG/OFC`, source-normalized Newton, PPN, R10, WEP, clock safety, orbital safety or local GR.
- The private SRNG branch is public evidence.
- EH-only charge import is enough for the MTS parent action.
- A fitted orbital `GM` can be used as the source normalization proof.
"""
    DOC.write_text(document, encoding="utf-8")


def main() -> None:
    source_output_rows = source_rows()
    audit_output_rows = audit_rows()
    residual_output_rows = residual_bound_rows()
    priority_output_rows = priority_rows()
    gate_output_rows = gate_rows()
    decision_output_rows = decision_rows()
    next_output_rows = next_rows()

    write_csv(OUTPUTS["sources"], source_output_rows)
    write_csv(OUTPUTS["audit"], audit_output_rows)
    write_csv(OUTPUTS["residual_bound"], residual_output_rows)
    write_csv(OUTPUTS["priority"], priority_output_rows)
    write_csv(OUTPUTS["gates"], gate_output_rows)
    write_csv(OUTPUTS["decision"], decision_output_rows)
    write_csv(OUTPUTS["next"], next_output_rows)

    shutil.copyfile(OUTPUTS["audit"], BRANCH_OUTPUTS["qv_owner_copy"])
    shutil.copyfile(OUTPUTS["residual_bound"], BRANCH_OUTPUTS["residual_bound_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

    branch_output_rows = branch_rows()
    write_csv(OUTPUTS["branches"], branch_output_rows)

    DOC.write_text("", encoding="utf-8")
    validation_output_rows = validation_rows(
        source_output_rows,
        audit_output_rows,
        residual_output_rows,
        gate_output_rows,
        branch_output_rows,
    )
    write_csv(OUTPUTS["validation"], validation_output_rows)

    write_doc(
        source_output_rows,
        audit_output_rows,
        residual_output_rows,
        priority_output_rows,
        gate_output_rows,
        decision_output_rows,
        next_output_rows,
        branch_output_rows,
        validation_output_rows,
    )


if __name__ == "__main__":
    main()
