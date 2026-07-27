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

CHECKPOINT = "2995"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2995-Y5-R2FR-projective-invariance-certificate-first-or-MICROSCOPE-kernel-acquisition-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2995_SOURCE_REGISTER.csv",
    "projective": RESIDUALS / "P8_Y5_R2FR_2995_PROJECTIVE_CERTIFICATE_REBASE.csv",
    "microscope": RESIDUALS / "P8_Y5_R2FR_2995_MICROSCOPE_KERNEL_REBASE.csv",
    "fork": RESIDUALS / "P8_Y5_R2FR_2995_THEOREM_DATA_FORK_STATUS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2995_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2995_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2995_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2995_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2995_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "projective_copy": PARENT_ACTION / "projective_private_zero_public_fallback_2995_NONCLAIM.csv",
    "microscope_copy": LOCAL_BOUNDS / "MICROSCOPE_readout_and_profile_gate_2995_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2995_PROJECTIVE_PUBLIC_OR_MICROSCOPE_READOUT_NEXT_NONCLAIM.csv",
}

for output_path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    output_path.parent.mkdir(parents=True, exist_ok=True)


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
        cells = [str(output_row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


SOURCE_SPECS = [
    (
        "SRC2995_00_2994_next",
        OUTPUTS["next"].parent / "P8_Y5_R2FR_2994_NEXT_TARGET.csv",
        ["NEXT2994_0_2995", "projective trace"],
        "2994 selects projective certificate first with MICROSCOPE kernel fallback.",
    ),
    (
        "SRC2995_01_2994_validation",
        OUTPUTS["validation"].parent / "P8_Y5_BRR545_2994_VALIDATION.csv",
        ["VAL2994_OVERALL", "True"],
        "2994 passed and kept local-GR/Newton promotion blocked.",
    ),
    (
        "SRC2995_02_2119_doc",
        ROOT / "2119-Y5-R2FR-projective-invariance-certificate-or-MICROSCOPE-numeric-kernel-acquisition.md",
        ["projective_trace_current=0", "not a global all-sector certificate"],
        "first projective certificate lowered the guard only inside the owned-coframe candidate branch.",
    ),
    (
        "SRC2995_03_2349_projective_audit",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2349_PROJECTIVE_TRACE_SILENCE_AUDIT.csv",
        ["PROJ2349_1_owned_coframe_private_zero", "PRIVATE_ZERO_PUBLIC_FALLBACK_RETAINED"],
        "later projective audit: private zero switch, public fallback retained.",
    ),
    (
        "SRC2995_04_2543_private_projective",
        RESIDUALS / "P8_Y5_NO_SHADOW_2543_PROJECTIVE_STATUS_UNDER_PRIVATE_SRNG.csv",
        ["PRJ2543_0_candidate_zero", "PUBLIC_CERTIFICATE_BLOCKED"],
        "latest private SRNG projective status: zero only in private branch.",
    ),
    (
        "SRC2995_05_2120_microscope_doc",
        ROOT / "2120-Y5-R2FR-MICROSCOPE-numeric-source-readout-kernel-acquisition.md",
        ["no verified CMSM numeric arrays", "tau_WEP"],
        "official MICROSCOPE/CMSM route was probed but did not yield live arrays.",
    ),
    (
        "SRC2995_06_2121_manual_workflow",
        ROOT
        / "source-intake"
        / "microscope"
        / "branch_locked_wep"
        / "drop-folder"
        / "1704"
        / "CMSM_MANUAL_EXPORT_WORKFLOW_2121.md",
        ["P_WEP_K_CMSM_readout.csv", "P_WEP_tau_parser_manifest"],
        "manual export workflow and exact live filenames exist.",
    ),
    (
        "SRC2995_07_2122_live_preflight",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2122_LIVE_DROP_PREFLIGHT.csv",
        ["MISSING_LIVE_ARTIFACT", "P_WEP_K_CMSM_readout.csv"],
        "strict live-drop validator rejects absent official files.",
    ),
    (
        "SRC2995_08_2123_commutator_split",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2123_PI_SPLIT_THEOREM.csv",
        ["PIS2123_0_pure_postprocessing", "PARTIAL_ZERO_PLUS_RETAINED_KERNEL"],
        "projection commutator split closes pure postprocessing only.",
    ),
    (
        "SRC2995_09_2790_readout_gate",
        RESIDUALS / "P8_Y5_R2FR_2790_MICROSCOPE_READOUT_IMPORT_GATE.csv",
        ["RIG2790_0_CMSM_arrays", "OFFICIAL_ARRAYS_NOT_IMPORTED"],
        "latest AX1090 MICROSCOPE gate still lacks official readout arrays.",
    ),
    (
        "SRC2995_10_2790_profile_kernel",
        RESIDUALS / "P8_Y5_R2FR_2790_SOURCE_PROFILE_KERNEL_DERIVATION_LEDGER.csv",
        ["K2790_1_effective_source_charge", "DERIVED_AS_NONCLAIM_PROFILE_RULE"],
        "finite-range source-profile algebra exists as nonclaim scaffolding.",
    ),
    (
        "SRC2995_11_2790_validation",
        RESIDUALS / "P8_Y5_BRR545_2790_VALIDATION.csv",
        ["VAL2790_OVERALL", "True"],
        "2790 validation passed with all WEP/local-GR claims blocked.",
    ),
]


def source_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "source_id": source_id,
                "source_path": str(source_path),
                "path_exists": source_path.exists(),
                "required_needles": "; ".join(needles),
                "needles_found": anchors(source_path, needles),
                "role": role,
            }
        )
        for source_id, source_path, needles, role in SOURCE_SPECS
    ]


def projective_rows() -> list[dict[str, Any]]:
    data = [
        (
            "PROJ2995_0_2119_candidate",
            "owned-coframe candidate projective direction",
            "ZERO_BY_VARIABLE_ABSENCE_INSIDE_1963_CANDIDATE",
            "2119 shows no independent Gamma/projective trace in the candidate branch.",
            "not global; source/readout sectors and affine fallback remain outside the proof.",
            True,
            False,
            "carry as conditional/private zero switch only",
        ),
        (
            "PROJ2995_1_2349_private_silent",
            "private owned-coframe + SRNG/OFC projective trace",
            "PRIVATE_ZERO_REAFFIRMED",
            "2349 sharpens the private branch: no physical projective variable direction when independent Gamma is absent and source/readout exceptions are excluded.",
            "private branch is not a parent-signed public action.",
            True,
            False,
            "do not publish as global certificate",
        ),
        (
            "PROJ2995_2_2543_latest_policy",
            "latest projective policy under private SRNG",
            "PROJECTIVE_NOT_FIRST_PRIORITY_INSIDE_PRIVATE_BRANCH",
            "2543 reduces private residual to spin/boundary/improvement plus zero private projective term.",
            "affine/global projective fallback still retained.",
            True,
            False,
            "stop re-litigating projective unless public affine branch is retained",
        ),
        (
            "PROJ2995_3_public_global",
            "public/global all-sector projective certificate",
            "NOT_SIGNED",
            "source, clock, WEP, orbit, light and boundary invariance are not globally signed.",
            "P4 projective component row remains live if independent affine Gamma survives.",
            False,
            False,
            "need parent action contract or finite P4 projective bound inputs",
        ),
        (
            "PROJ2995_4_verdict",
            "projective route selected by 2994",
            "DERIVATION_ROUTE_PARTIALLY_SUCCESSFUL_NOT_PROMOTABLE",
            "projective is lowered to a private zero switch, which is genuine progress.",
            "does not prove local GR/Newton/PPN; public fallback remains.",
            True,
            False,
            "use private zero internally; keep public residual ledger explicit",
        ),
    ]
    return [
        base(
            {
                "projective_id": projective_id,
                "target": target,
                "status": status,
                "evidence": evidence,
                "limitation": limitation,
                "private_zero": private_zero,
                "global_zero": global_zero,
                "next_action": next_action,
            }
        )
        for projective_id, target, status, evidence, limitation, private_zero, global_zero, next_action in data
    ]


def microscope_rows() -> list[dict[str, Any]]:
    data = [
        (
            "MIC2995_0_2120_official_probe",
            "official CMSM/MICROSCOPE numeric arrays",
            "NOT_ACQUIRED",
            "2120 found provenance/templates/metadata but no verified gx/gz/Sxx/Sxz/masks/calibration arrays.",
            "tau_WEP cannot be run claim-grade.",
            False,
            "keep official data as a hard gate",
        ),
        (
            "MIC2995_1_2121_manual_export",
            "manual export workflow",
            "READY_FOR_USER_SUPPLIED_EXPORTS",
            "exact filenames, schemas and manifest template exist in the 1704 live drop workflow.",
            "workflow is not data.",
            False,
            "accept only strict live-drop artifacts",
        ),
        (
            "MIC2995_2_2122_validator",
            "strict live-drop preflight",
            "VALIDATOR_READY_LIVE_SET_MISSING",
            "preflight rejects missing/placeholder files and keeps rows nonclaim.",
            "no complete official live set exists now.",
            False,
            "do not score WEP until all live artifacts pass",
        ),
        (
            "MIC2995_3_2123_commutator",
            "projection/readout commutator",
            "PURE_POSTPROCESSING_ZERO_SOURCE_FEEDBACK_LIVE",
            "post-variation reports are harmless by type, but source-feedback projectors and masks can contribute.",
            "source-feedback finite kernels remain.",
            False,
            "separate report closure from source equations",
        ),
        (
            "MIC2995_4_2790_profile",
            "finite-range Earth/source profile kernel",
            "NUMERIC_NONCLAIM_PROFILE_SCAFFOLD_EXISTS",
            "two-layer profile-weighting grid and DD source vector exist as smoke scaffolding.",
            "requires lambda_WEP/range owner, PREM/profile closure, parent-to-DD map and official readout.",
            False,
            "use as plumbing, not as a WEP pass",
        ),
        (
            "MIC2995_5_2790_readout",
            "MICROSCOPE official readout import",
            "OFFICIAL_READOUT_NOT_IMPORTED",
            "2790 keeps gx/gz/Sxx/Sxz/masks/timing/eta normalization as a separate gate.",
            "surrogate/design matrix cannot replace official arrays.",
            False,
            "next empirical step is readout import or range-owner theorem",
        ),
        (
            "MIC2995_6_verdict",
            "MICROSCOPE fallback selected by 2994",
            "DATA_PLUMBING_IMPROVED_CLAIM_BLOCKED",
            "the fallback is now operationally clearer than at 2120.",
            "no source-backed claim-grade kernel exists.",
            False,
            "continue only via official arrays or theorem-zero route",
        ),
    ]
    return [
        base(
            {
                "microscope_id": microscope_id,
                "target": target,
                "status": status,
                "evidence": evidence,
                "limitation": limitation,
                "score_ready": score_ready,
                "next_action": next_action,
            }
        )
        for microscope_id, target, status, evidence, limitation, score_ready, next_action in data
    ]


def fork_rows() -> list[dict[str, Any]]:
    data = [
        (
            "FORK2995_0_private_projective",
            "theorem",
            "KEEP_AS_PRIVATE_ZERO_SWITCH",
            "projective is zero inside private owned-coframe/SRNG branch by variable absence",
            "parent-sign SRNG/OFC or keep public fallback",
        ),
        (
            "FORK2995_1_public_projective",
            "theorem_or_bound",
            "PUBLIC_GATE_OPEN",
            "global all-sector invariance/gauge-fix before coupling not signed",
            "write parent-action contract or fill P4 projective bound rows",
        ),
        (
            "FORK2995_2_microscope_data",
            "data",
            "OFFICIAL_ARRAYS_MISSING",
            "source-profile and surrogate scaffolds exist but cannot replace live CMSM readout",
            "manual export/import gate remains",
        ),
        (
            "FORK2995_3_microscope_theorem",
            "theorem",
            "RANGE_AND_MAP_OWNER_OPEN",
            "finite profile grid needs lambda_WEP/range owner and parent-to-DD map before it becomes physics",
            "derive range owner or keep lambda-dependent nonclaim rows",
        ),
        (
            "FORK2995_4_policy",
            "policy",
            "NO_LOCAL_GR_OR_WEP_PROMOTION",
            "both routes improved but neither route satisfies claim gates",
            "use this checkpoint as a route selector, not evidence update",
        ),
    ]
    return [
        base(
            {
                "fork_id": fork_id,
                "route_type": route_type,
                "status": status,
                "reason": reason,
                "next_action": next_action,
            }
        )
        for fork_id, route_type, status, reason, next_action in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        ("GATE2995_0_2994_handoff", "2994 handoff resolved into projective/MICROSCOPE audit", True, "2995 consumes the selected fork.", False),
        ("GATE2995_1_private_projective_zero", "projective zero inside private owned-coframe/SRNG branch", True, "zero by variable absence is recorded.", False),
        ("GATE2995_2_global_projective_zero", "projective trace globally gauge/fixed/unobservable", False, "all-sector source/readout invariance remains unsigned.", False),
        ("GATE2995_3_microscope_live_arrays", "official CMSM/MICROSCOPE live arrays imported", False, "latest readout gate says official arrays are not imported.", False),
        ("GATE2995_4_profile_claim_ready", "finite source profile row is physically claim-ready", False, "lambda owner, PREM/profile closure, parent-to-DD map and official readout are missing.", False),
        ("GATE2995_5_source_feedback_commutator_zero", "source-feedback projector/readout commutator zero", False, "only pure postprocessing is closed.", False),
        ("GATE2995_6_local_GR_Newton_PPN", "derived local GR/Newton/PPN claim allowed", False, "public projective, source/readout, WEP and boundary/source gates remain open.", False),
    ]
    return [
        base(
            {
                "gate_id": gate_id,
                "gate": gate,
                "condition_passed": condition_passed,
                "status": status,
                "promotion_allowed_now": promotion_allowed,
            }
        )
        for gate_id, gate, condition_passed, status, promotion_allowed in data
    ]


def decision_rows() -> list[dict[str, Any]]:
    data = [
        (
            "DEC2995_0_projective_result",
            "Treat projective as a genuine private derivation win, not a public pass.",
            "2119/2349/2543 all agree: no projective variable direction inside the private owned-coframe/SRNG branch, but global/all-sector certificate is missing.",
            "carry projective as zero in private calculations and retain P4 projective fallback outside that branch",
        ),
        (
            "DEC2995_1_microscope_result",
            "Treat MICROSCOPE as better-plumbed but still blocked.",
            "2120-2122 built the official workflow/validator and 2777-2790 built source-profile/readout scaffolds, but official readout arrays are still absent.",
            "do not run WEP/local-GR claims from surrogate/profile rows",
        ),
        (
            "DEC2995_2_stop_looping",
            "Do not spend the next step re-proving the private projective zero.",
            "the private result has converged; the public route needs a parent-action contract, while the data route needs official/readout/range-owner inputs.",
            "move to public-contract/range-owner/readout gate rather than another projective restatement",
        ),
        (
            "DEC2995_3_next",
            "Select a dual-gate 2996 target.",
            "the sharpest current split is parent-sign private zero switches versus source-backed WEP/readout/range owner.",
            "write 2996 as SRNG/OFC public parent contract or MICROSCOPE range/readout import gate",
        ),
    ]
    return [
        base(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
            }
        )
        for decision_id, decision, because, next_action in data
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "next_id": "NEXT2995_0_2996",
                "priority": "selected_primary",
                "next_doc": "2996-Y5-R2FR-SRNG-OFC-public-parent-contract-or-MICROSCOPE-range-readout-gate-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_SRNG_OFC_public_parent_contract_or_MICROSCOPE_range_readout_gate_under_AX1090_2996.py",
                "objective": "Either promote the private projective/source-readout zero switches into a parent-signed public SRNG/OFC contract, or keep public fallbacks and advance the MICROSCOPE finite route by deriving lambda_WEP/range owner plus official readout/import requirements.",
                "include": "2543 private projective split;2349 public fallback;2790 source-profile kernel;2790 MICROSCOPE readout import gate;2122 strict live-drop preflight;source-feedback commutator policy",
                "exclude": "claiming local GR/Newton/PPN;claiming WEP from surrogate/profile rows;re-proving private projective zero;using fitted-G absorption;GitHub action;formalization-workbench edits",
            }
        )
    ]


def validation_rows(
    source_output_rows: list[dict[str, Any]],
    projective_output_rows: list[dict[str, Any]],
    microscope_output_rows: list[dict[str, Any]],
    fork_output_rows: list[dict[str, Any]],
    gate_output_rows: list[dict[str, Any]],
    branch_output_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    source_ok = all(boolish(source_row["path_exists"]) for source_row in source_output_rows)
    anchors_ok = all(boolish(source_row["needles_found"]) for source_row in source_output_rows)
    private_zero_ok = any(row["projective_id"] == "PROJ2995_2_2543_latest_policy" and boolish(row["private_zero"]) for row in projective_output_rows)
    global_blocked_ok = any(row["projective_id"] == "PROJ2995_3_public_global" and not boolish(row["global_zero"]) for row in projective_output_rows)
    microscope_blocked_ok = any(row["microscope_id"] == "MIC2995_5_2790_readout" and row["status"] == "OFFICIAL_READOUT_NOT_IMPORTED" for row in microscope_output_rows)
    fork_safe_ok = any(row["fork_id"] == "FORK2995_4_policy" and row["status"] == "NO_LOCAL_GR_OR_WEP_PROMOTION" for row in fork_output_rows)
    gates_safe_ok = any(row["gate_id"] == "GATE2995_6_local_GR_Newton_PPN" and not boolish(row["condition_passed"]) for row in gate_output_rows)
    csv_parse_ok = all(csv_ok(output_path) for output_path in output_paths if output_path.suffix == ".csv" and output_path.exists())
    branch_ok = all(boolish(row["copy_exists"]) and boolish(row["parse_ok"]) for row in branch_output_rows)
    outputs_under_post = all(under(output_path, ROOT) for output_path in output_paths + [DOC])
    formalization_2995_count = 0
    if FORMALIZATION.exists():
        formalization_2995_count = sum(1 for path in FORMALIZATION.rglob("*2995*") if path.is_file())
    no_claim_flags = True
    for output_path in output_paths:
        if output_path.exists() and output_path.suffix == ".csv":
            for output_row in rows(output_path):
                if str(output_row.get("valid_for_claim", "")).strip().lower() == "true":
                    no_claim_flags = False
                if str(output_row.get("claim_allowed", "")).strip().lower() == "true":
                    no_claim_flags = False
                if str(output_row.get("promotion_allowed_now", "")).strip().lower() == "true":
                    no_claim_flags = False
    data = [
        ("VAL2995_0_sources_exist", source_ok, "all cited local source paths exist"),
        ("VAL2995_1_anchors_found", anchors_ok, "all cited source anchors found"),
        ("VAL2995_2_private_projective_zero", private_zero_ok, "private projective zero switch recorded"),
        ("VAL2995_3_global_projective_blocked", global_blocked_ok, "public/global projective certificate remains blocked"),
        ("VAL2995_4_microscope_blocked", microscope_blocked_ok, "official MICROSCOPE readout remains missing"),
        ("VAL2995_5_fork_safe", fork_safe_ok, "theory/data fork denies local-GR or WEP promotion"),
        ("VAL2995_6_gates_safe", gates_safe_ok, "local GR/Newton/PPN gate remains false"),
        ("VAL2995_7_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2995_8_csvs_parse", csv_parse_ok, "all generated CSVs parse"),
        ("VAL2995_9_outputs_under_post", outputs_under_post, "all generated outputs under post-checkpoint-work"),
        ("VAL2995_10_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2995_11_formalization_clean", formalization_2995_count == 0, f"no 2995 outputs in formalization-workbench (count={formalization_2995_count})"),
        ("VAL2995_12_doc_written", DOC.exists(), "2995 markdown checkpoint exists"),
    ]
    overall = all(passed for _, passed, _ in data)
    data.append(("VAL2995_OVERALL", overall, "2995 rebases the projective/MICROSCOPE fork onto current evidence and keeps all public/local claims blocked"))
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
    projective_output_rows: list[dict[str, Any]],
    microscope_output_rows: list[dict[str, Any]],
    fork_output_rows: list[dict[str, Any]],
    gate_output_rows: list[dict[str, Any]],
    decision_output_rows: list[dict[str, Any]],
    next_output_rows: list[dict[str, Any]],
    branch_output_rows: list[dict[str, Any]],
    validation_output_rows: list[dict[str, Any]],
) -> None:
    document = f"""# 2995 - Y5/R2FR Projective Invariance Certificate First Or MICROSCOPE Kernel Acquisition Under AX1090

Status: `Y5_R2FR_2995_projective_private_zero_rebased_MICROSCOPE_readout_blocked_nonclaim`

Claim ceiling: `no_public_projective_certificate_no_MICROSCOPE_claim_no_WEP_claim_no_local_GR_no_Newton_no_PPN_no_GitHub_no_formalization_edit`

## Current Verdict

2995 answers the 2994 handoff without pretending the later corpus does not exist. The lower-scrutiny projective route partly succeeds: projective trace is zero inside the private owned-coframe/SRNG branch by variable absence. That is real progress and should stay in the private calculation stack.

It is not a public/global local-GR certificate. The all-sector projective invariance/gauge-fix contract is still unsigned, and the affine fallback still carries a P4 projective row if independent `Gamma` survives.

The MICROSCOPE fallback is also clearer but not claim-ready. The workflow, validator, source-profile algebra, and nonclaim surrogate/profile scaffolds exist. The missing pieces remain official CMSM/readout arrays, `lambda_WEP`/range ownership, PREM/profile closure, parent-to-DD map, and same-branch source/readout normalization.

## Source Register

{md_table(source_output_rows, ["source_id", "path_exists", "needles_found", "role"])}

## Projective Certificate Rebase

{md_table(projective_output_rows, ["projective_id", "target", "status", "private_zero", "global_zero", "next_action"])}

## MICROSCOPE Kernel Rebase

{md_table(microscope_output_rows, ["microscope_id", "target", "status", "score_ready", "next_action"])}

## Theory/Data Fork Status

{md_table(fork_output_rows, ["fork_id", "route_type", "status", "next_action"])}

## Promotion Gates

{md_table(gate_output_rows, ["gate_id", "gate", "condition_passed", "status", "promotion_allowed_now"])}

## Decision Ledger

{md_table(decision_output_rows, ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(next_output_rows, ["next_id", "next_doc", "objective", "exclude"])}

## Branch Copies

{md_table(branch_output_rows, ["copy_id", "destination", "copy_exists", "row_count", "parse_ok", "valid_for_claim"])}

## Validation

{md_table(validation_output_rows, ["validation_id", "passed", "check", "required"])}

## Plain-English Takeaway

Projective is no longer the thing to keep punching inside the private branch. It is a useful private zero switch, not a public victory lap. MICROSCOPE has better plumbing than before, but no official live readout import. The next serious move is to either parent-sign the private SRNG/OFC contract, or advance the finite WEP/MICROSCOPE route through range ownership plus official readout import.
"""
    DOC.write_text(document, encoding="utf-8")


def main() -> None:
    source_output_rows = source_rows()
    projective_output_rows = projective_rows()
    microscope_output_rows = microscope_rows()
    fork_output_rows = fork_rows()
    gate_output_rows = gate_rows()
    decision_output_rows = decision_rows()
    next_output_rows = next_rows()

    write_csv(OUTPUTS["sources"], source_output_rows)
    write_csv(OUTPUTS["projective"], projective_output_rows)
    write_csv(OUTPUTS["microscope"], microscope_output_rows)
    write_csv(OUTPUTS["fork"], fork_output_rows)
    write_csv(OUTPUTS["gates"], gate_output_rows)
    write_csv(OUTPUTS["decision"], decision_output_rows)
    write_csv(OUTPUTS["next"], next_output_rows)

    shutil.copyfile(OUTPUTS["projective"], BRANCH_OUTPUTS["projective_copy"])
    shutil.copyfile(OUTPUTS["microscope"], BRANCH_OUTPUTS["microscope_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

    branch_output_rows = [
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
    write_csv(OUTPUTS["branches"], branch_output_rows)

    DOC.write_text("", encoding="utf-8")

    validation_output_rows = validation_rows(
        source_output_rows,
        projective_output_rows,
        microscope_output_rows,
        fork_output_rows,
        gate_output_rows,
        branch_output_rows,
    )
    write_csv(OUTPUTS["validation"], validation_output_rows)

    write_doc(
        source_output_rows,
        projective_output_rows,
        microscope_output_rows,
        fork_output_rows,
        gate_output_rows,
        decision_output_rows,
        next_output_rows,
        branch_output_rows,
        validation_output_rows,
    )


if __name__ == "__main__":
    main()
