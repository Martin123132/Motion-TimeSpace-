from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_R10_KERNEL_CMETRIC_EGK_DERIVATION_OR_BLOCKER_2566"
CHECKPOINT_ID = "2566"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

DOC = ROOT / "2566-Y5-R2FR-R10-kernel-Cmetric-EGK-derivation-or-blocker.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2566_SOURCE_REGISTER.csv",
    "derivation_verdict": OUT / "P8_Y5_NO_SHADOW_2566_DERIVATION_VERDICT.csv",
    "cmetric_factor_chain": OUT / "P8_Y5_NO_SHADOW_2566_CMETRIC_FACTOR_CHAIN.csv",
    "egk_gap_map": OUT / "P8_Y5_NO_SHADOW_2566_EGK_GAP_MAP.csv",
    "bridge_blockers": OUT / "P8_Y5_NO_SHADOW_2566_BRIDGE_BLOCKERS.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2566_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2566_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2566_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2566_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2566_VALIDATION.csv",
}

COPY_TARGETS = {
    "bridge_verdict": LOCAL_BOUNDS / "R10_Cmetric_EGK_bridge_verdict_2566_NONCLAIM.csv",
    "cmetric_factor_chain": LOCAL_BOUNDS / "Cmetric_factor_chain_2566_NONCLAIM.csv",
    "next_queue": QUEUE / "JR2566_NON_EGK_ZERO_CERTIFICATES_OR_EXTENDED_NORM_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2566_00_2565_doc",
        "source_path": ROOT / "2565-Y5-R2FR-first-real-local-bound-source-and-parent-coefficient-blocker.md",
        "needles": ["NEXT2565_0_selected", "BLOCK2565_0_EGK", "BLOCK2565_1_Cmetric", "VAL2565_OVERALL"],
        "role": "current-branch handoff selecting R10/Cmetric/EGK derivation attempt",
    },
    {
        "source_id": "SRC2566_01_2565_bound_control",
        "source_path": OUT / "P8_Y5_NO_SHADOW_2565_BOUND_CONTROL_ROWS.csv",
        "needles": ["BOUND2565_R10_ANCHOR_ALPHA1_38P6UM", "CONTROL2565_R10_NEWTON_GR_ALPHA_ZERO", "3.86e-05"],
        "role": "real R10 external bound/control rows",
    },
    {
        "source_id": "SRC2566_02_2477_cmetric",
        "source_path": LOCAL_BOUNDS / "Cmetric_factorisation_2477_NONCLAIM.csv",
        "needles": ["CM2477_3_Cmetric", "C_metric=(2/c^2)*C_obs*C_Green*C_res", "FORMAL_FACTORISATION_ONLY"],
        "role": "non-circular C_metric factorisation from earlier weak-field theorem attempt",
    },
    {
        "source_id": "SRC2566_03_2478_green",
        "source_path": LOCAL_BOUNDS / "Cmetric_residual_Green_candidate_2478_NONCLAIM.csv",
        "needles": ["CMET2478_0_formal_metric_bound", "C_metric=(2/c^2)*C_obs*C_Green*C_res", "FORMAL_CANDIDATE_NONCLAIM"],
        "role": "conditional Green-bound and Cmetric candidate shapes",
    },
    {
        "source_id": "SRC2566_04_2479_residual_map",
        "source_path": LOCAL_BOUNDS / "Residual_sector_to_EGK_norm_map_2479_NONCLAIM.csv",
        "needles": ["COEF2479_C_HD", "COEF2479_C_norm", "MISSING_PARENT_GRAMMAR_OR_EMPIRICAL_COEFFICIENT_BOUND"],
        "role": "residual-sector map showing current E_GK is too narrow",
    },
    {
        "source_id": "SRC2566_05_2479_blocker",
        "source_path": LOCAL_BOUNDS / "Local_residual_norm_extension_blocker_2479_NONCLAIM.csv",
        "needles": ["BLK2479_0_EGK_insufficient", "full residual norm basis", "select zero-certificate vs extended-norm route"],
        "role": "blocker proving E_GK-only bridge is insufficient",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row() -> dict[str, Any]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        missing: list[str] = []
        if exists:
            text = read_text(path)
            missing = [needle for needle in source["needles"] if needle not in text]
        else:
            missing = list(source["needles"])
        rows.append(
            {
                **base_row(),
                "source_id": source["source_id"],
                "source_path": str(path),
                "exists": exists,
                "missing_needles": ";".join(missing),
                "source_pass": exists and not missing,
                "role": source["role"],
            }
        )
    return rows


def derivation_verdict_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DER2566_0_external_bound",
            "R10 alpha_bound source",
            "BOUND2565_R10_ANCHOR_ALPHA1_38P6UM: alpha_bound=1 at lambda=3.86e-05 m",
            "PASS_SOURCE_ONLY",
            "external local bound/control side is real enough for a threshold smoke input",
            "ANCHOR_ONLY_NONCURVE;NO_MTS_ALPHA_PREDICTION",
        ),
        (
            "DER2566_1_Cmetric_factorisation",
            "C_metric",
            "C_metric=(2/c^2)*C_obs*C_Green*C_res",
            "PARTIAL_DERIVATION_CONDITIONAL",
            "2477/2478 give a non-circular weak-field residual lane instead of borrowing GR as proof",
            "C_res;C_Green;C_obs remain symbolic",
        ),
        (
            "DER2566_2_R10_kernel",
            "K_R10(lambda,geometry)",
            "K_R10 is the R10 apparatus/observable projection part of C_obs, not the parent metric response itself",
            "BLOCKED_DOWNSTREAM_OF_COBS",
            "R10 geometry kernel can only be meaningful after residual source and Green/domain package are fixed",
            "MISSING_R10_APPARATUS_KERNEL;MISSING_COBS_R10",
        ),
        (
            "DER2566_3_EGK_current_basis",
            "E_GK_bound",
            "current E_GK_bound=C_B boundary_flux+C_S source_tail+C_X negative_mode_defect+C_H topology_hair+C_P projector_leak",
            "INSUFFICIENT_FOR_FULL_SRES",
            "2479 shows S_res has non-EGK slots: HD curvature, source normalization, background subtraction, species-shadow and auxiliary/frame tails",
            "MISSING_ZERO_CERTIFICATES_OR_EXTENDED_ELOCAL",
        ),
        (
            "DER2566_4_bridge_shape",
            "alpha_pred(lambda)",
            "alpha_pred(lambda)=K_R10(lambda,geometry)*(2/c^2)*C_Green*C_res*E_local_res",
            "CONDITIONAL_BRIDGE_WRITTEN_NOT_CLOSED",
            "this is the honest bridge from parent residuals to R10 once C_obs/K_R10 and E_local_res are sourced",
            "MISSING_CRES;MISSING_CGREEN;MISSING_KR10;MISSING_ELOCAL",
        ),
        (
            "DER2566_5_local_GR_route",
            "local Newton/GR limit",
            "if all residual slots vanish or are bounded to zero and EH-leading operator is parent-signed, then S_res -> 0 and the Newton lane closes",
            "PREFERRED_DERIVATION_ROUTE_BUT_UNSIGNED",
            "this is the clean path the user wants: derive residual silence, not tune a local bound",
            "MISSING_PARENT_ZERO_CERTIFICATES;MISSING_EH_ORIGIN_CERTIFICATE",
        ),
    ]
    return [
        {
            **base_row(),
            "derivation_id": derivation_id,
            "object": obj,
            "candidate_relation": relation,
            "status": status,
            "why_it_matters": why,
            "blocking_input": blocker,
        }
        for derivation_id, obj, relation, status, why, blocker in rows
    ]


def cmetric_factor_chain_rows() -> list[dict[str, Any]]:
    rows = [
        ("FAC2566_0_Sres", "S_res", "residual weak-field Poisson source", "DeltaE_MTS+DeltaE_boundary+J_shadow+delta_G_source+Lambda/background", "FORMAL_DECOMPOSITION", "not a numeric coefficient"),
        ("FAC2566_1_Cres", "C_res", "||S_res||_dual <= C_res*E_local_res", "residual-sector coefficient map and norm basis", "BLOCKED_SYMBOLIC", "requires zero certificates or source-backed coefficient rows"),
        ("FAC2566_2_CGreen", "C_Green", "||deltaU|| <= C_Green*||S_res||_dual", "local collar domain, gauge, boundary and harmonic mode package", "CONDITIONAL_GREEN_SHAPE", "mathematical form exists; arena domain constants missing"),
        ("FAC2566_3_Cobs_R10", "C_obs_R10", "projection from deltaU/delta g_00 to R10 torsion observable", "R10 geometry, source separation, observable functional", "MISSING_ARENA_PROJECTION", "do not build until C_res/C_Green are sourced"),
        ("FAC2566_4_Cmetric", "C_metric", "(2/c^2)*C_obs*C_Green*C_res", "FAC2566_1_Cres;FAC2566_2_CGreen;FAC2566_3_Cobs_R10", "PARTIAL_CONDITIONAL_FACTORISATION", "valid as formula only"),
        ("FAC2566_5_KR10", "K_R10(lambda,geometry)", "arena-specific alpha(lambda) readout kernel folded into C_obs_R10", "R10 apparatus convolution and alpha convention", "MISSING_R10_KERNEL", "external bound exists; prediction kernel missing"),
        ("FAC2566_6_Elocal", "E_local_res", "E_GK_bound plus any non-EGK residual slots not proved zero", "2479 residual map", "EXTENDED_NORM_OR_ZERO_CERTIFICATE_REQUIRED", "current E_GK alone is insufficient"),
    ]
    return [
        {
            **base_row(),
            "factor_id": factor_id,
            "symbol": symbol,
            "definition": definition,
            "depends_on": depends_on,
            "status": status,
            "units_role": units_role,
        }
        for factor_id, symbol, definition, depends_on, status, units_role in rows
    ]


def egk_gap_map_rows() -> list[dict[str, Any]]:
    rows = [
        ("EGK2566_0_current", "E_GK_bound", "boundary_flux;source_tail;negative_mode_defect;topology_hair_amplitude;projector_leak", "current 2563/2479 basis", "INSUFFICIENT_FOR_FULL_SRES", "keep but do not use as full residual denominator"),
        ("EGK2566_1_HD", "e_HD_curvature_operator", "higher-derivative curvature residual", "not in current E_GK", "MISSING_ZERO_OR_SLOT", "try zero certificate first"),
        ("EGK2566_2_aux", "e_aux_constraint_stress", "auxiliary/constraint stress tails", "partial negative-mode overlap only", "MISSING_ZERO_OR_SLOT", "separate true negative modes from auxiliary stress"),
        ("EGK2566_3_tau", "e_tau_clock_frame_leak", "tau/coframe/current-chain preferred-frame leakage", "source_tail partial only", "MISSING_ZERO_OR_SLOT", "needs clock/current vertical silence or bound"),
        ("EGK2566_4_qspur", "e_q_weyl_spurion", "q/Weyl/Ricci spurion or reciprocal-source tail", "source_tail/topology/projector partial only", "MISSING_ZERO_OR_SLOT", "needs q first-class/no-spurion theorem"),
        ("EGK2566_5_shadow", "e_species_shadow_or_zero", "non-Hilbert species/source-shadow residual", "source_tail partial only", "MISSING_ZERO_OR_SLOT", "prefer zero via matter descent"),
        ("EGK2566_6_norm", "e_source_norm_gap", "kappa0/G_ref/Hilbert source normalization mismatch", "none", "MISSING_ZERO_OR_SLOT", "cannot be fitted by orbital GM"),
        ("EGK2566_7_background", "e_background_subtraction", "local Lambda/reference background subtraction", "none", "MISSING_ZERO_OR_SLOT", "declare subtraction convention or bounded slot"),
    ]
    return [
        {
            **base_row(),
            "gap_id": gap_id,
            "slot": slot,
            "meaning": meaning,
            "current_coverage": coverage,
            "status": status,
            "next_action": next_action,
        }
        for gap_id, slot, meaning, coverage, status, next_action in rows
    ]


def bridge_blocker_rows() -> list[dict[str, Any]]:
    rows = [
        ("BLK2566_0_Cres", "C_res", "residual source coefficient is symbolic", "derive zero certificates or source-backed coefficients for every S_res sector", "BLOCKED"),
        ("BLK2566_1_Elocal", "E_local_res or full zero theorem", "current E_GK does not cover full S_res", "prove non-EGK slots zero or define extended norm with source paths", "BLOCKED"),
        ("BLK2566_2_CGreen", "C_Green", "local domain/gauge/boundary constants are not fixed", "build local collar Green certificate after residual norm basis is chosen", "BLOCKED"),
        ("BLK2566_3_KR10", "K_R10/C_obs_R10", "R10 apparatus projection is downstream of metric response and residual norm", "do not source geometry kernel before response variable is fixed", "BLOCKED"),
        ("BLK2566_4_full_curve", "alpha_bound(lambda)", "source-backed threshold exists but broad curve remains review-candidate only", "obtain official table or human-reviewed digitization", "BLOCKED_FOR_FULL_CURVE"),
        ("BLK2566_5_EH_origin", "EH-leading weak-field operator origin", "candidate Poisson lane is not yet parent-signed from deeper MTS primitives", "promote parent action normal form or keep EH lane conditional", "BLOCKED_FOR_LOCAL_GR_CLAIM"),
    ]
    return [
        {
            **base_row(),
            "blocker_id": blocker_id,
            "missing_object": missing_object,
            "why_it_blocks": why,
            "next_action": next_action,
            "status": status,
        }
        for blocker_id, missing_object, why, next_action, status in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2566_0_real_R10_bound", "R10 source-backed threshold/control row exists.", "PASS_SOURCE_ONLY", "2565 bound/control rows are carried forward", True, False),
        ("GATE2566_1_Cmetric_factor", "C_metric has a non-circular formal factorisation.", "PASS_CONDITIONAL_NONCLAIM", "2477/2478 factor C_metric through C_obs, C_Green and C_res", True, False),
        ("GATE2566_2_EGK_full_cover", "Current E_GK covers full weak-field residual source.", "BLOCKED", "2479 proves current E_GK is too narrow for full S_res", False, False),
        ("GATE2566_3_Cres_numeric", "C_res is numeric/source-backed.", "BLOCKED", "residual-sector coefficients remain symbolic", False, False),
        ("GATE2566_4_KR10", "K_R10 is sourced or derived.", "BLOCKED", "R10 kernel remains downstream of C_obs/domain package", False, False),
        ("GATE2566_5_R10_prediction", "MTS can make an R10 alpha(lambda) prediction.", "BLOCKED", "bridge shape exists but C_res, C_Green, K_R10 and E_local_res are missing", False, False),
        ("GATE2566_6_local_GR_Newton", "MTS derives local Newton/GR limit.", "BLOCKED", "requires residual zero certificates plus parent-signed EH/weak-field operator", False, False),
        ("GATE2566_7_no_shortcuts", "No GR shortcut, fitted GM, M_H_ref reuse or plateau axiom.", "PASS_GUARDRAIL", "all shortcut routes remain explicit blockers", True, False),
        ("GATE2566_8_no_GitHub", "No public/GitHub update.", "PASS_GUARDRAIL", "private derivation checkpoint only", True, False),
    ]
    return [
        {
            **base_row(),
            "gate_id": gate_id,
            "claim": claim,
            "gate_status": gate_status,
            "reason": reason,
            "gate_pass": gate_pass,
            "claim_allowed": claim_allowed,
        }
        for gate_id, claim, gate_status, reason, gate_pass, claim_allowed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2566_0_gain", "Promote the bridge from vague blocker to conditional formula.", "C_metric factorisation and Green-bound shapes exist in earlier chain", "R10 path is sharper but still nonclaim"),
        ("DEC2566_1_do_not_chase_R10_kernel_first", "Do not prioritize K_R10 geometry next.", "a geometry kernel cannot help while C_res and E_local_res are undefined", "move upstream to residual zero/norm basis"),
        ("DEC2566_2_prefer_zero_certificates", "Try zero certificates before enlarging the residual norm.", "a serious GR/Newton reduction should remove residual sectors where possible", "cleaner than patching with many empirical slots"),
        ("DEC2566_3_keep_private", "No local-test or local-GR claim.", "bridge is structural, not numeric or fully sourced", "private checkpoint only"),
    ]
    return [
        {
            **base_row(),
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "effect": effect,
        }
        for decision_id, decision, reason, effect in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            **base_row(),
            "route_id": "NEXT2566_0_selected",
            "selection_status": "selected",
            "target_file": "2567-Y5-R2FR-non-EGK-residual-zero-certificates-or-extended-local-norm.md",
            "target_script": "scripts/Y5_R2FR_non_EGK_residual_zero_certificates_or_extended_local_norm_2567.py",
            "task": "attempt zero certificates for e_HD, e_aux, e_tau, e_qspur, e_shadow, e_norm and e_background; if any fail, define an extended E_local_res norm vector while keeping C_res and local-GR claims blocked",
            "acceptance_target": "zero/retain decision for every non-EGK slot, extended norm vector if needed, C_res status, local-GR/R10 claim gates",
            "guardrails": "no GR shortcut; no fitted GM; no M_H_ref reuse; no plateau axiom; no GitHub",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    for target in COPY_TARGETS.values():
        target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(OUTPUTS["derivation_verdict"], COPY_TARGETS["bridge_verdict"])
    shutil.copyfile(OUTPUTS["cmetric_factor_chain"], COPY_TARGETS["cmetric_factor_chain"])
    shutil.copyfile(OUTPUTS["next_target"], COPY_TARGETS["next_queue"])
    source_map = {
        "bridge_verdict": OUTPUTS["derivation_verdict"],
        "cmetric_factor_chain": OUTPUTS["cmetric_factor_chain"],
        "next_queue": OUTPUTS["next_target"],
    }
    return [
        {
            **base_row(),
            "copy_id": copy_id,
            "source_path": str(source_map[copy_id]),
            "target_path": str(target),
            "source_exists": source_map[copy_id].exists(),
            "target_exists": target.exists(),
        }
        for copy_id, target in COPY_TARGETS.items()
    ]


def csv_row_count(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        return len(list(csv.DictReader(handle)))


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, notes: str, detail: str = "") -> None:
        rows.append({**base_row(), "check_id": check_id, "status": "PASS" if status else "FAIL", "notes": notes, "detail": detail})

    verdict_statuses = {row["derivation_id"]: row["status"] for row in data["verdict"]}
    factor_symbols = {row["symbol"] for row in data["factors"]}
    gap_slots = {row["slot"] for row in data["gaps"]}
    add("VAL2566_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    add("VAL2566_01_real_bound_carried", verdict_statuses.get("DER2566_0_external_bound") == "PASS_SOURCE_ONLY", "real R10 external bound/control row carried forward")
    add("VAL2566_02_cmetric_factorised", verdict_statuses.get("DER2566_1_Cmetric_factorisation") == "PARTIAL_DERIVATION_CONDITIONAL" and "C_metric" in factor_symbols, "C_metric conditional factorisation recorded")
    add("VAL2566_03_egk_insufficient", verdict_statuses.get("DER2566_3_EGK_current_basis") == "INSUFFICIENT_FOR_FULL_SRES", "current E_GK insufficiency recorded")
    add("VAL2566_04_missing_slots_named", all(slot in gap_slots for slot in ["e_HD_curvature_operator", "e_source_norm_gap", "e_background_subtraction"]), "non-EGK residual slots named")
    add("VAL2566_05_bridge_nonclaim", all(row["claim_allowed"] is False for row in data["verdict"]), "all derivation verdict rows remain nonclaim")
    add("VAL2566_06_claim_gates_safe", all(row["claim_allowed"] is False for row in data["gates"]), "no claim gate allows R10/local-GR claim")
    add("VAL2566_07_next_target_written", bool(data["next"]) and data["next"][0]["route_id"] == "NEXT2566_0_selected", "2567 zero-certificate or extended-norm target selected")
    add("VAL2566_08_branch_copies", all(row["source_exists"] and row["target_exists"] for row in data["copies"]), "nonclaim branch copies exist")
    markers = ("2566-Y5", "P8_Y5_NO_SHADOW_2566", "P8_Y5_BRR545_2566", "JR2566")
    formal_hits = [path for path in FORMALIZATION.rglob("*") if path.is_file() and any(marker in path.name for marker in markers)] if FORMALIZATION.exists() else []
    add("VAL2566_09_no_formalization_artifacts", not formal_hits, "no 2566 artifacts were written to formalization-workbench", ";".join(str(path) for path in formal_hits))
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            count = csv_row_count(path)
            add(f"VAL2566_CSV_{path.stem}", count > 0, f"CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2566_CSV_{path.stem}", False, f"CSV parse failed: {exc}", str(path))
    for copy_id, path in COPY_TARGETS.items():
        try:
            count = csv_row_count(path)
            add(f"VAL2566_COPY_CSV_{copy_id}", count > 0, f"copy CSV parses with {count} rows", str(path))
        except Exception as exc:
            add(f"VAL2566_COPY_CSV_{copy_id}", False, f"copy CSV parse failed: {exc}", str(path))
    add("VAL2566_OVERALL", all(row["status"] == "PASS" for row in rows), "2566 closes the current bridge shape conditionally, blocks numeric R10/local-GR claims, and selects non-EGK zero certificates or extended norm next")
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2566 Y5 R2FR R10 Kernel Cmetric EGK Derivation Or Blocker",
        "",
        "**Status:** conditional bridge sharpened, not claimed. The R10 external bound/control row is real, and `C_metric` now has a non-circular factorisation inherited from the weak-field residual lane: `C_metric=(2/c^2) C_obs C_Green C_res`. But the current `E_GK_bound` is too narrow for the full residual source, and `K_R10/C_obs_R10` is still downstream of unresolved residual and Green/domain data.",
        "",
        "**Main result:** the bridge is no longer fog: `alpha_pred(lambda)=K_R10(lambda,geometry)*(2/c^2)*C_Green*C_res*E_local_res`. The next derivation target is not R10 geometry first; it is zero certificates for the non-EGK residual slots, or an explicit extended local residual norm.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Derivation Verdict",
        markdown_table(data["verdict"], ["derivation_id", "object", "candidate_relation", "status", "why_it_matters", "blocking_input", "claim_allowed"]),
        "",
        "## Cmetric Factor Chain",
        markdown_table(data["factors"], ["factor_id", "symbol", "definition", "depends_on", "status", "units_role"]),
        "",
        "## EGK Gap Map",
        markdown_table(data["gaps"], ["gap_id", "slot", "meaning", "current_coverage", "status", "next_action"]),
        "",
        "## Bridge Blockers",
        markdown_table(data["blockers"], ["blocker_id", "missing_object", "why_it_blocks", "next_action", "status"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register_rows(),
        "verdict": derivation_verdict_rows(),
        "factors": cmetric_factor_chain_rows(),
        "gaps": egk_gap_map_rows(),
        "blockers": bridge_blocker_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["derivation_verdict"], data["verdict"])
    write_csv(OUTPUTS["cmetric_factor_chain"], data["factors"])
    write_csv(OUTPUTS["egk_gap_map"], data["gaps"])
    write_csv(OUTPUTS["bridge_blockers"], data["blockers"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
