from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1662"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1662-Y5-R2FR-q_loc-covariance-and-apparatus-transfer-map.md"

SOURCE_FILES = {
    "1661_doc": ROOT / "1661-Y5-R2FR-Fermi-projector-constant-theorem-or-frame-silence.md",
    "1661_validation": OUT / "P8_Y5_BRR545_1661_VALIDATION.csv",
    "1661_projector_bound": OUT / "P8_Y5_PARENT_QLOC_1661_PROJECTOR_BOUND.csv",
    "1661_frame_scales": OUT / "P8_Y5_PARENT_QLOC_1661_FRAME_SCALE_LEDGER.csv",
    "1661_frame_silence": OUT / "P8_Y5_PARENT_QLOC_1661_FRAME_SILENCE_GATE.csv",
    "469_q_source": ROOT / "469-fill-or-zero-highest-pressure-mu-extra-row.md",
    "1003_frame_guard": ROOT / "1003-Y5-R10-Bref-covariant-frame-theorem-or-Delta-ref-frame-profile-row.md",
    "474_covariant_counterexample": ROOT / "474-domain-selector-no-vector-theorem-or-coefficient.md",
}

NEEDLES = {
    "1661_doc": ["covariance-gated", "q_loc"],
    "1661_validation": ["VAL1661_OVERALL", "PASS"],
    "1661_projector_bound": ["PB1661_0_conditional_geodesic_Fermi_projector_bound", "1.23573661e-23"],
    "1661_frame_scales": ["FRAME_SCALE_DWARFS_CURVATURE_IF_UNSILENCED", "2.43238775e-13"],
    "1661_frame_silence": ["MISSING_PARENT_PROOF", "MISSING_ARENA_PROJECTION"],
    "469_q_source": ["q_i^nu = P_loc^nu_rho", "Ward/Bianchi ownership plus no-hair routing does not prove zero"],
    "1003_frame_guard": ["covariant-frame zero theorem attempted, not closed", "THEOREM_ZERO_REJECTED_WITHOUT_PARENT_SIGNED_COVARIANT_FRAME"],
    "474_covariant_counterexample": ["Ward ownership is necessary but permits covariant domain-vector counterexamples", "covariant_domain_vector counterexample"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1662_SOURCE_REGISTER.csv"
QLOC_COVARIANCE_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1662_QLOC_COVARIANCE_CONTRACT.csv"
COVARIANCE_THEOREM_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1662_COVARIANCE_THEOREM_ATTEMPT.csv"
APPARATUS_TRANSFER_MAP = OUT / "P8_Y5_PARENT_QLOC_1662_APPARATUS_TRANSFER_MAP.csv"
FRAME_LEAK_FALLBACK = OUT / "P8_Y5_PARENT_QLOC_1662_FRAME_LEAK_FALLBACK.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1662_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1662_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1662_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1662_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    QLOC_COVARIANCE_CONTRACT,
    COVARIANCE_THEOREM_ATTEMPT,
    APPARATUS_TRANSFER_MAP,
    FRAME_LEAK_FALLBACK,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    QLOC_COVARIANCE_CONTRACT,
    COVARIANCE_THEOREM_ATTEMPT,
    APPARATUS_TRANSFER_MAP,
    FRAME_LEAK_FALLBACK,
    CLAIM_GATE,
    DECISION,
    NEXT_TARGET,
]

COPY_TARGETS = {
    QLOC_COVARIANCE_CONTRACT: [
        QUARANTINE / "QLOC_COVARIANCE_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_qloc_covariance_contract_nonclaim_1662.csv",
        QUEUE / "JR1662_QLOC_COVARIANCE_CONTRACT_NONCLAIM.csv",
    ],
    APPARATUS_TRANSFER_MAP: [
        QUARANTINE / "APPARATUS_TRANSFER_MAP_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_apparatus_transfer_map_nonclaim_1662.csv",
        QUEUE / "JR1662_APPARATUS_TRANSFER_MAP_NONCLAIM.csv",
    ],
    FRAME_LEAK_FALLBACK: [
        QUARANTINE / "FRAME_LEAK_FALLBACK_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_frame_leak_fallback_nonclaim_1662.csv",
        QUEUE / "JR1662_FRAME_LEAK_FALLBACK_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1662.csv",
        QUEUE / "JR1662_NEXT_TARGET_NONCLAIM.csv",
    ],
}

CONDITIONAL_PROJECTOR_BOUND_M1 = 1.23573661e-23
ACCELERATION_FRAME_SCALE_M1 = 1.09039705e-16
ROTATION_FRAME_SCALE_M1 = 2.43238775e-13


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {
        "accepted_for_scoring",
        "claim_allowed",
        "claim_ready",
        "frame_silenced_for_claim",
        "score_allowed",
        "score_ready",
        "theorem_closed_for_claim",
        "transfer_signed_for_claim",
        "valid_for_claim",
        "valid_for_mts_claim",
        "valid_for_runner",
    }
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def find_line(path: Path, pattern: str) -> int:
    for index, line in enumerate(read_text(path).splitlines(), start=1):
        if pattern in line:
            return index
    return -1


def format_scientific(value: float) -> str:
    return f"{value:.8e}"


def source_register_rows() -> list[dict[str, object]]:
    rows = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1662 q_loc covariance and apparatus transfer map",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def qloc_covariance_contract_rows() -> list[dict[str, object]]:
    rows = [
        (
            "QC1662_0_object_definition",
            "q_loc^nu = P_loc^nu_rho (nabla^rho Gamma_eff - nabla_mu K_hat^{mu rho})",
            "DEFINITION_PRESENT",
            "469 supplies the working q_i^nu owner identity",
            "definition only; not a covariance proof",
            "469_q_source",
        ),
        (
            "QC1662_1_scalar_descent",
            "Gamma_eff is a scalar/quotient field on the parent configuration space",
            "MISSING_PARENT_SIGNATURE",
            "needed so nabla^rho Gamma_eff is a vector independent of coordinate frame",
            "Gamma_eff can otherwise carry representative/frame convention",
            "MISSING_PARENT_ACTION_CLAUSE",
        ),
        (
            "QC1662_2_current_descent",
            "K_hat^{mu nu} is a genuine tensor current from a covariant parent variation",
            "MISSING_PARENT_SIGNATURE",
            "needed so nabla_mu K_hat^{mu nu} is a vector/tensorial divergence",
            "Ward ownership alone does not prove the divergence is absent",
            "469_and_474",
        ),
        (
            "QC1662_3_projector_descent",
            "P_loc^nu_rho is built from a parent-owned observer/tetrad or quotient projector",
            "MISSING_PROJECTOR_CERTIFICATE",
            "needed to prevent P_loc from being an external Earth-frame filter",
            "external projector can inject preferred-frame leakage",
            "1003_frame_guard",
        ),
        (
            "QC1662_4_vertical_invariance",
            "Dq(v_frame)=0 implies Lie_v q_loc=0 for allowed frame/coframe changes",
            "CONDITIONAL_ONLY",
            "1003 has quotient coframe descent only conditionally",
            "zero switch is rejected without parent-signed covariant frame theorem",
            "1003_frame_guard",
        ),
        (
            "QC1662_5_covariant_counterexample_guard",
            "covariance/Ward ownership alone proves q_loc has no local vector leakage",
            "REJECTED_SHORTCUT",
            "474 explicitly allows covariant domain-vector counterexamples",
            "a covariant vector can still be physical and locally preferred",
            "474_covariant_counterexample",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": clause_id,
            "clause": clause,
            "status": status,
            "why_needed": why_needed,
            "failure_mode": failure_mode,
            "source_ref": source_ref,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for clause_id, clause, status, why_needed, failure_mode, source_ref in rows
    ]


def covariance_theorem_attempt_rows() -> list[dict[str, object]]:
    rows = [
        (
            "TH1662_0_conditional_success",
            "If Gamma_eff descends as scalar, K_hat descends as tensor current, P_loc descends as parent tetrad/projector, and Dq(v_frame)=0, then q_loc is a vector/tetrad component and coordinate inertial connection terms are not independent physical sources.",
            "CONDITIONAL_THEOREM",
            "mathematically plausible but only conditional",
            "missing parent signatures for Gamma_eff/K_hat/P_loc and vertical frame directions",
        ),
        (
            "TH1662_1_current_failure",
            "Ward/Bianchi ownership of total exchange current implies local q_loc vector flux is absent.",
            "FAILS_AS_SHORTCUT",
            "ownership is necessary bookkeeping, not absence",
            "469 and 474 retain covariant vector/flux counterexamples",
        ),
        (
            "TH1662_2_frame_failure",
            "Earth-fixed lab inertial terms can be dropped because a freefall Fermi frame exists.",
            "FAILS_AS_SHORTCUT",
            "freefall frame existence does not by itself transfer Earth-fixed observables",
            "missing apparatus transfer map and parent covariance certificate",
        ),
        (
            "TH1662_3_verdict",
            "q_loc observer-frame covariance is parent-derived for local observables.",
            "NOT_CLOSED_FOR_CLAIM",
            "the desired proof route is sharply specified",
            "must supply parent action clauses or retain frame-leak fallback",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "proposition": proposition,
            "status": status,
            "value": value,
            "blocker": blocker,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for attempt_id, proposition, status, value, blocker in rows
    ]


def apparatus_transfer_rows() -> list[dict[str, object]]:
    rows = [
        (
            "ATM1662_0_transfer_definition",
            "A_lab_to_Fermi maps Earth-fixed apparatus observables into nonrotating geodesic Fermi tetrad components",
            "MISSING_ARENA_PROJECTION",
            "without this, the Fermi curvature bound is not the same quantity the R10 apparatus measures",
        ),
        (
            "ATM1662_1_acceleration_calibration",
            "a_earth/c^2 term is universal coordinate/apparatus calibration and not q_loc source",
            "MISSING_TRANSFER_CERTIFICATE",
            "requires parent covariance plus explicit lab observable transfer",
        ),
        (
            "ATM1662_2_rotation_calibration",
            "Omega_earth/c term is a tetrad rotation/Sagnac-style transfer term and not q_loc source",
            "MISSING_TRANSFER_CERTIFICATE",
            "rotation scale is the larger fallback if not removed",
        ),
        (
            "ATM1662_3_same_quantity_contract",
            "the scalar/tetrad component bounded in the freefall frame equals the local source residual entering R10/PPN/WEP comparisons",
            "MISSING_OBSERVABLE_EQUIVALENCE",
            "otherwise a tiny curvature bound and a lab residual are being compared across different objects",
        ),
        (
            "ATM1662_4_no_cancellation_guard",
            "frame terms are individually projected out or individually bounded; no tuned cancellation credit",
            "POLICY_PASS",
            "keeps the route falsifiable and prevents after-the-fact fitting",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "map_id": map_id,
            "transfer_clause": clause,
            "status": status,
            "reason": reason,
            "transfer_signed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for map_id, clause, status, reason in rows
    ]


def frame_leak_fallback_rows() -> list[dict[str, object]]:
    retained_scale = max(ACCELERATION_FRAME_SCALE_M1, ROTATION_FRAME_SCALE_M1)
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FLF1662_0_retained_frame_leak_if_transfer_unsigned",
            "epsilon_frame_leak_m1": format_scientific(retained_scale),
            "source_component": "max(a_earth/c^2, Omega_earth/c)",
            "a_earth_over_c2_m1": format_scientific(ACCELERATION_FRAME_SCALE_M1),
            "Omega_earth_over_c_m1": format_scientific(ROTATION_FRAME_SCALE_M1),
            "conditional_curvature_bound_m1": format_scientific(CONDITIONAL_PROJECTOR_BOUND_M1),
            "ratio_to_curvature_bound": format_scientific(retained_scale / CONDITIONAL_PROJECTOR_BOUND_M1),
            "fallback_status": "RETAIN_IF_QLOC_COVARIANCE_OR_TRANSFER_UNSIGNED",
            "runner_use": "blocks local scoring; can become numeric penalty row if parent proof fails",
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def claim_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1662_0_q_loc_covariance", "q_loc is observer-frame covariant for local observables", False, "BLOCKED", "parent signatures for Gamma_eff/K_hat/P_loc and vertical frame directions missing"),
        ("CG1662_1_apparatus_transfer", "Earth-fixed apparatus terms are projected/transferred out", False, "BLOCKED", "A_lab_to_Fermi map and observable equivalence missing"),
        ("CG1662_2_frame_leak", "frame leak is zero for R10/PPN/WEP", False, "NO_CLAIM", "fallback epsilon_frame_leak retained if unsigned"),
        ("CG1662_3_projector_bound", "conditional Fermi projector bound is score-ready", False, "NO_CLAIM", "bound is conditional and not linked to apparatus observable"),
        ("CG1662_4_local", "local GR/Newton/PPN/R10/WEP follows", False, "NO_CLAIM", "no signed q_loc covariance, no transfer map, no M_H_ref denominator"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "status": status,
            "blocker": blocker,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, gate_pass, status, blocker in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("DEC1662_0_theorem_attempt", "QLOC_COVARIANCE_NOT_PARENT_CLOSED", "the desired covariance proof is now exact but lacks parent signatures", "write parent action clauses for Gamma_eff, K_hat, and P_loc descent"),
        ("DEC1662_1_transfer", "APPARATUS_TRANSFER_MAP_MISSING", "freefall Fermi bound and Earth-fixed R10 observable are not yet the same object", "derive A_lab_to_Fermi or retain frame leak row"),
        ("DEC1662_2_frame_fallback", "RETAIN_EPSILON_FRAME_LEAK", "Omega/c dominates if not projected out", "keep nonclaim fallback row with absolute no-cancellation guard"),
        ("DEC1662_3_next", "NEXT_1663_PARENT_QLOC_TENSOR_ACTION_CLAUSE", "least smuggly route is to make q_loc tensorial from the parent action", "attempt parent action clause before more numerical testing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1663-Y5-R2FR-parent-q_loc-tensor-action-clause-or-frame-leak-coefficient.md",
            "script": "scripts/Y5_R2FR_parent_q_loc_tensor_action_clause_or_frame_leak_coefficient.py",
            "objective": "write the exact parent action clauses that make Gamma_eff, K_hat, and P_loc descend tensorially and define A_lab_to_Fermi, or retain epsilon_frame_leak as a nonclaim coefficient",
            "success_condition": "q_loc covariance and apparatus transfer become parent-signed, or local GR/Newton branch is explicitly closure/coefficient-only",
            "forbidden_shortcuts": "no Ward-ownership-as-zero; no frame-choice-by-convention; no dropping Omega/c or a/c^2 without transfer map",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def validation_rows(source_rows, covariance, theorem, transfer, frame_leak, claim, decisions, next_targets):
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    formalization_dirty = any(FORMALIZATION.rglob("*1662*")) if FORMALIZATION.exists() else False
    theorem_not_closed = any(row["status"] == "NOT_CLOSED_FOR_CLAIM" for row in theorem)
    rejected_shortcuts = any(row["status"] == "REJECTED_SHORTCUT" for row in covariance) and any(row["status"] == "FAILS_AS_SHORTCUT" for row in theorem)
    transfer_blocked = any(str(row["status"]).startswith("MISSING") for row in transfer)
    leak_retained = frame_leak[0]["fallback_status"] == "RETAIN_IF_QLOC_COVARIANCE_OR_TRANSFER_UNSIGNED" and float(frame_leak[0]["ratio_to_curvature_bound"]) > 1.0

    checks = [
        ("VAL1662_0_sources_exist", all(row["path_exists"] and row["needles_found"] for row in source_rows), "all cited 1662 source paths exist and needles are present"),
        ("VAL1662_1_1661_passed", any(row["source_id"] == "1661_validation" and row["needles_found"] for row in source_rows), "1661 validation is source-registered as PASS"),
        ("VAL1662_2_covariance_clauses_present", len(covariance) >= 6 and any(row["clause_id"] == "QC1662_0_object_definition" for row in covariance), "q_loc covariance contract clauses are present"),
        ("VAL1662_3_shortcuts_rejected", rejected_shortcuts, "Ward/covariance/frame-choice shortcuts are rejected"),
        ("VAL1662_4_theorem_not_promoted", theorem_not_closed, "q_loc covariance theorem remains not closed for claim"),
        ("VAL1662_5_transfer_blocked", transfer_blocked, "apparatus transfer map remains explicitly blocked"),
        ("VAL1662_6_frame_leak_retained", leak_retained, "frame leak fallback is retained and exceeds curvature bound"),
        ("VAL1662_7_claim_gates_safe", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim), "all claim gates keep MTS claims false"),
        ("VAL1662_8_next_target_selected", next_targets[0]["next_target"] == "1663-Y5-R2FR-parent-q_loc-tensor-action-clause-or-frame-leak-coefficient.md", "next target selects parent q_loc tensor action clause"),
        ("VAL1662_9_csv_parse", generated_csv_parse, "all generated 1662 CSVs parse"),
        ("VAL1662_10_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1662 generated rows keep MTS claim/no-score flags false"),
        ("VAL1662_11_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)), "branch/quarantine copies exist"),
        ("VAL1662_12_queue_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)), "acquisition queue nonclaim copies exist"),
        ("VAL1662_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1662_14_formalization_untouched", not formalization_dirty, "no 1662 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1662_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1662 q_loc covariance and apparatus transfer validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(source_rows, covariance, theorem, transfer, frame_leak, claim, decisions, next_targets, validation) -> None:
    text = f"""# 1662 - q_loc Covariance And Apparatus Transfer Map

**Private status:** theorem-attempt checkpoint. No R10 pass, local-GR pass, Newton pass, PPN pass, WEP pass, or public claim is made.

## Verdict

`1662` gives the cleanest current statement of the problem:

```text
If Gamma_eff, K_hat, and P_loc descend as parent tensorial objects,
and if Earth-fixed lab observables are transferred into the same freefall Fermi residual,
then q_loc can be observer-frame covariant and inertial frame terms need not be physical sources.
```

But that is not parent-closed yet. The corpus already blocks the shortcut: Ward/Bianchi ownership is not absence, and a covariant vector can still be a real local preferred direction.

So the local branch is not dead, but it is now parent-action gated. Until that gate closes, the retained fallback is:

```text
epsilon_frame_leak = {frame_leak[0]["epsilon_frame_leak_m1"]} m^-1
ratio_to_curvature_bound = {frame_leak[0]["ratio_to_curvature_bound"]}
```

This is exactly why the next move must be parent-action structure, not another numerical patch.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## q_loc Covariance Contract

{markdown_table(covariance, ["clause_id", "clause", "status", "why_needed", "failure_mode", "source_ref"])}

## Covariance Theorem Attempt

{markdown_table(theorem, ["attempt_id", "proposition", "status", "value", "blocker"])}

## Apparatus Transfer Map

{markdown_table(transfer, ["map_id", "transfer_clause", "status", "reason"])}

## Frame Leak Fallback

{markdown_table(frame_leak, ["row_id", "epsilon_frame_leak_m1", "source_component", "conditional_curvature_bound_m1", "ratio_to_curvature_bound", "fallback_status", "runner_use"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

This is a useful narrowing. We are no longer asking vaguely whether the local branch can look like GR. We are asking whether the parent action can make `q_loc` a genuine quotient-tensor residual and define the apparatus transfer map. If yes, the large Earth-frame inertial terms become calibration/coordinate transfer terms. If no, the local branch remains closure/coefficient-only and cannot claim derived GR/Newton recovery.
"""
    DOC.write_text(text, encoding="utf-8")


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    covariance = qloc_covariance_contract_rows()
    theorem = covariance_theorem_attempt_rows()
    transfer = apparatus_transfer_rows()
    frame_leak = frame_leak_fallback_rows()
    claim = claim_rows()
    decisions = decision_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (QLOC_COVARIANCE_CONTRACT, covariance),
        (COVARIANCE_THEOREM_ATTEMPT, theorem),
        (APPARATUS_TRANSFER_MAP, transfer),
        (FRAME_LEAK_FALLBACK, frame_leak),
        (CLAIM_GATE, claim),
        (DECISION, decisions),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, covariance, theorem, transfer, frame_leak, claim, decisions, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, covariance, theorem, transfer, frame_leak, claim, decisions, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1662 validation failed; see P8_Y5_BRR545_1662_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1662 validation PASS")


if __name__ == "__main__":
    main()
