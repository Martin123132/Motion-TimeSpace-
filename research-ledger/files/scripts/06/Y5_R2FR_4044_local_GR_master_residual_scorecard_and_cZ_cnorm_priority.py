from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4044-Y5-R2FR-local-GR-master-residual-scorecard-and-cZ-cnorm-priority.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4044_SOURCE_REGISTER.csv",
    "master_scorecard": SOURCE_DIR / "P8_Y5_R2FR_4044_MASTER_RESIDUAL_SCORECARD.csv",
    "claim_ladder": SOURCE_DIR / "P8_Y5_R2FR_4044_SELECTED_BRANCH_CLAIM_LADDER.csv",
    "priority_matrix": SOURCE_DIR / "P8_Y5_R2FR_4044_CZ_CNORM_PRIORITY_MATRIX.csv",
    "local_gr_gate": SOURCE_DIR / "P8_Y5_R2FR_4044_LOCAL_GR_GATE_STATUS.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4044_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4044_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4044_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4044_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4044_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4044_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty rows for {path}")
    fields: List[str] = []
    for item in rows:
        for key in item:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_rows(ts: str) -> List[Dict[str, object]]:
    specs = [
        ("SRC4044_0", ROOT / "4037-Y5-R2FR-minimal-parent-packet-signature-or-cT-cEM-bound-smoke.md", "MINIMAL_SOURCE_CLEAN_LOCAL_PACKET_SIGNED_INTERNALLY", "selected local packet and direct source-only coupling zeros"),
        ("SRC4044_1", ROOT / "4038-Y5-R2FR-Poynting-no-flux-and-boundary-reference-theorem-or-flux-bound.md", "C_POYNTING_AND_C_B_ZERO_IN_SELECTED_LOCAL_BRANCH", "Poynting/boundary no-flux branch"),
        ("SRC4044_2", ROOT / "4039-Y5-R2FR-hidden-current-fixed-point-silence-or-cZ-bound.md", "C_Z_NARROWED_NOT_FULLY_ZEROED", "hidden-current split and partial zero"),
        ("SRC4044_3", ROOT / "4040-Y5-R2FR-local-memory-tail-selector-wall-silence-or-cZ-envelope.md", "TAIL_WALL_SILENCE_NOT_PROVED_CZ_ENVELOPE_ACTIVE", "cZ tail/wall active envelope"),
        ("SRC4044_4", ROOT / "4041-Y5-R2FR-cnorm-common-mode-into-kappa-obs-or-Gdot-bound.md", "COMMON_MODE_ROUTED_TO_KAPPA_OBS_DERIVATIVE_HAIR_RETAINED", "c_norm common-mode routing and derivative hair"),
        ("SRC4044_5", ROOT / "4042-Y5-R2FR-nonEH-operator-decoupling-or-PPN-bound-vector.md", "STANDALONE_C_NONEH_DECOMPOSED", "nonEH family decomposition"),
        ("SRC4044_6", ROOT / "4043-Y5-R2FR-projector-domain-stress-silence-or-alpha-xi-bound-vector.md", "PROJECTOR_DOMAIN_STRESS_ZERO_IN_PRIVATE_SELECTED_BRANCH", "projector/domain alpha-xi selected-branch zero"),
        ("SRC4044_7", SOURCE_DIR / "P8_Y5_R2FR_4040_REMAINING_LOCAL_RESIDUAL_VECTOR.csv", "Delta_cZ_envelope", "cZ residual CSV"),
        ("SRC4044_8", SOURCE_DIR / "P8_Y5_R2FR_4041_DRIFT_BOUND_TEMPLATE.csv", "DB4041_0_Gdot", "c_norm derivative bound template"),
        ("SRC4044_9", SOURCE_DIR / "P8_Y5_R2FR_4043_ALPHA_XI_BOUND_VECTOR.csv", "Delta_PPN_projector_stress", "projector/domain fallback vector"),
        ("SRC4044_10", SOURCE_DIR / "P8_Y5_R2FR_4043_REMAINING_LOCAL_RESIDUAL_VECTOR.csv", "Parent_packet_adoption", "latest remaining residuals"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": ts,
            }
        )
    return rows


def master_scorecard_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "MRS4044_0_source_clean_packet",
            "channel": "direct source-only vertices",
            "symbols": "c_T, c_EM, C_XF2_direct",
            "current_result": "zero in selected private local packet",
            "evidence": "4037 source-clean packet",
            "blocks_public_local_GR": False,
            "fallback_if_reopened": "finite c_T/c_EM bound vector",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "row_id": "MRS4044_1_boundary_poynting",
            "channel": "Poynting/boundary/reference leakage",
            "symbols": "c_Poynting, c_B",
            "current_result": "zero in stationary compact no-flux collar with fixed source-blind reference",
            "evidence": "4038 local Poynting and boundary theorem",
            "blocks_public_local_GR": False,
            "fallback_if_reopened": "boundary flux and reference-charge bound",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "row_id": "MRS4044_2_cZ_core",
            "channel": "owned hidden-current core",
            "symbols": "J_Z^direct, J_Z^boundary, J_Z^Gamma",
            "current_result": "narrowed / zeroed for owned fixed-point pieces",
            "evidence": "4039 split plus positive double-zero Gamma route",
            "blocks_public_local_GR": False,
            "fallback_if_reopened": "component bound rows",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "row_id": "MRS4044_3_cZ_tail_wall",
            "channel": "memory tail and selector wall",
            "symbols": "Delta_cZ_envelope",
            "current_result": "live no-cancellation envelope",
            "evidence": "4040 cZ envelope",
            "blocks_public_local_GR": True,
            "fallback_if_reopened": "kernel support/gap/no-wall theorem or numeric tail/wall bound",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "row_id": "MRS4044_4_cnorm_common",
            "channel": "constant common source/action normalization",
            "symbols": "c_norm_common, kappa_obs, G_obs",
            "current_result": "routed into observed Newton coupling",
            "evidence": "4041 kappa_obs routing",
            "blocks_public_local_GR": False,
            "fallback_if_reopened": "calibration consistency audit",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "row_id": "MRS4044_5_cnorm_derivative",
            "channel": "nonconstant source-normalization derivative hair",
            "symbols": "Delta_cnorm_envelope",
            "current_result": "live no-cancellation derivative envelope",
            "evidence": "4041 Gdot/radial/range/species/source-measure split",
            "blocks_public_local_GR": True,
            "fallback_if_reopened": "Gdot, radial, R10, WEP/source species, and M_eff flux bound rows",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "row_id": "MRS4044_6_nonEH_direct",
            "channel": "standalone non-EH operator families",
            "symbols": "c_nonEH, Delta_PPN_abs_nonEH",
            "current_result": "decomposed: direct absent/topological/double-zero/rerouted/live projector pieces",
            "evidence": "4042 R11 family classification",
            "blocks_public_local_GR": False,
            "fallback_if_reopened": "PPN no-cancellation operator vector",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "row_id": "MRS4044_7_projector_domain",
            "channel": "projector/domain preferred-frame stress",
            "symbols": "Delta_PPN_projector_stress, alpha_i, xi",
            "current_result": "zero in selected private branch; fallback vector retained if 3929 signature rejected",
            "evidence": "4043 alpha-xi stress theorem",
            "blocks_public_local_GR": False,
            "fallback_if_reopened": "alpha1/alpha2/alpha3/xi/zeta product rows",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "row_id": "MRS4044_8_parent_adoption",
            "channel": "final parent action adoption",
            "symbols": "Parent_packet_adoption",
            "current_result": "private selected branch not yet a public final parent action theorem",
            "evidence": "4043 remaining vector",
            "blocks_public_local_GR": True,
            "fallback_if_reopened": "formal parent action variation audit",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def claim_ladder_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "ladder_id": "LAD4044_0_newton_leading_order",
            "claim_level": "Newton leading order in selected branch",
            "current_status": "plausible_private_conditional",
            "needed_for_upgrade": "cZ/cnorm envelopes do not feed Poisson source or are bounded below Newton/orbital sensitivity",
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "ladder_id": "LAD4044_1_ppn_local_gr",
            "claim_level": "PPN/local-GR through required order",
            "current_status": "blocked_private_nonclaim",
            "needed_for_upgrade": "Delta_cZ_envelope=0/bounded, Delta_cnorm_envelope=0/bounded, parent packet adopted, and second-order beta/gamma source stability checked",
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "ladder_id": "LAD4044_2_public_unified_field_spine",
            "claim_level": "public competitive unified-field framework",
            "current_status": "not_yet",
            "needed_for_upgrade": "local GR/Newton/Maxwell limit plus empirical cosmology/galaxy/EM pillars with no hidden closure assumptions",
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def priority_matrix_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "priority_id": "PRI4044_0_cZ_kernel",
            "rank": 1,
            "target": "Delta_cZ_envelope",
            "why_first": "it is the most direct remaining local-force/current leak and can also seed c_norm/Gdot-like hair",
            "derive_route": "prove local memory kernel has no compact support/projection or has positive gap with exp(-L_collar/ell_mem) suppression plus zero wall jump",
            "bound_route": "fill C_mem, ell_mem, wall jump, and Green-operator constants in the 4040 envelope",
            "success_condition": "A_tail=A_wall=0 in selected branch, or numeric absolute envelope below PPN/R10/orbital locks",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "priority_id": "PRI4044_1_cnorm_derivative",
            "rank": 2,
            "target": "Delta_cnorm_envelope",
            "why_first": "it is next hardest for local GR but cleaner empirically once cZ is controlled",
            "derive_route": "prove D_a ln G_obs=D_a ln M_eff=D_a ln(1+epsilon_mu)=0 in compact local branch",
            "bound_route": "Gdot/radial/R10/species/source-measure derivative rows from 4041",
            "success_condition": "all derivative hair rows zero or below local-GR/Newton/clock/WEP bounds",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "priority_id": "PRI4044_2_parent_adoption",
            "rank": 3,
            "target": "Parent_packet_adoption",
            "why_first": "needed to turn private branch theorem stack into a serious formal parent-action claim",
            "derive_route": "assemble selected local packet as a parent action and vary every active field/readout once",
            "bound_route": "not a numeric bound; this is a formal action audit",
            "success_condition": "same action yields EH/Newton/Maxwell local limit and allows cosmology/galaxy branch without arena-fitted switches",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def local_gr_gate_rows(ts: str, scorecard: List[Dict[str, object]]) -> List[Dict[str, object]]:
    blockers = [item["row_id"] for item in scorecard if item["blocks_public_local_GR"] is True]
    return [
        {
            "gate_id": "LGG4044_0_private_selected_branch",
            "gate": "private selected local branch coherence",
            "status": "IMPROVED_BUT_NOT_FINAL",
            "blocking_rows": ";".join(blockers),
            "explanation": "direct source, EM/boundary, nonEH direct, and projector/domain stress are controlled in the selected branch; cZ, c_norm, and parent adoption remain",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "LGG4044_1_public_local_GR",
            "gate": "public local-GR/PPN claim",
            "status": "BLOCKED",
            "blocking_rows": ";".join(blockers),
            "explanation": "no public local-GR claim until every blocking row has zero theorem or sourced bound",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "gate_id": "LGG4044_2_next_best_attack",
            "gate": "next derivation target",
            "status": "ATTACK_CZ_FIRST",
            "blocking_rows": "MRS4044_3_cZ_tail_wall",
            "explanation": "cZ is both conceptually central and upstream of some derivative-hair contamination",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def evaluator_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "case_id": "CASE4044_0_project_state",
            "verdict": "LOCAL_BRANCH_SUBSTANTIALLY_NARROWED_NOT_CLAIMED",
            "result": "The local-GR route is now concentrated into cZ tail/wall, c_norm derivative hair, and parent packet adoption rather than broad unresolved c_nonEH/projector/source clutter.",
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4044_1_next_attack",
            "verdict": "CZ_KERNEL_WALL_ROUTE_IS_NEXT",
            "result": "Attack cZ first because it is a direct current/force residual and may source apparent normalization drift if left open.",
            "public_claim_allowed": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def decision_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4044_0_no_github_no_public",
            "decision": "keep checkpoint private and nonclaim",
            "reason": "local GR is closer but not public-ready while cZ/cnorm/adoption remain",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4044_1_no_more_generic_nonEH",
            "decision": "do not treat nonEH/projector stress as the main live blocker unless the selected branch is rejected",
            "reason": "4042/4043 decomposed and controlled those channels in the private branch",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4044_2_next",
            "decision": "derive or bound cZ kernel/wall first",
            "reason": "it is the highest-value remaining local-force leak",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def claim_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4044_0_progress",
            "claim": "local branch residual vector has been sharply narrowed",
            "allowed": True,
            "public_claim_allowed": False,
            "scope": "private internal progress statement",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4044_1_local_GR",
            "claim": "MTS derives local GR/PPN fully",
            "allowed": False,
            "public_claim_allowed": False,
            "scope": "blocked by cZ/cnorm/parent adoption",
            "timestamp_utc": ts,
        },
    ]


def next_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NEXT4044_0",
            "next_doc": "4045-Y5-R2FR-cZ-kernel-wall-zero-theorem-or-first-bound-values.md",
            "next_script": "scripts/Y5_R2FR_4045_cZ_kernel_wall_zero_theorem_or_first_bound_values.py",
            "why": "cZ tail/wall is now the top-ranked derivation target for local GR",
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STAT4044",
            "status": "LOCAL_GR_ROUTE_NARROWED_CZ_CNORM_PARENT_ADOPTION_REMAIN",
            "public_claim": False,
            "timestamp_utc": ts,
        }
    ]


def render_doc(ts: str, sources: List[Dict[str, object]]) -> str:
    source_hits = sum(1 for item in sources if item["exists"] and item["needle_found"])
    return "\n".join(
        [
            "# 4044 - Local-GR Master Residual Scorecard And cZ/cnorm Priority",
            "",
            f"- Timestamp: `{ts}`",
            "- Status: `private_nonclaim_checkpoint`",
            "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
            f"- Source needles found: `{source_hits}/{len(sources)}`.",
            "",
            "## What Actually Moved",
            "",
            "4044 consolidates the 4037-4043 local branch instead of adding another loose checkpoint.",
            "",
            "The local branch is now much narrower: direct source-only couplings, local Poynting/boundary leakage, standalone non-EH operators, and projector/domain alpha-xi stress are controlled in the selected private branch.",
            "",
            "The honest live blockers are now:",
            "",
            "- `Delta_cZ_envelope`: memory tail / selector wall / hidden-current residual;",
            "- `Delta_cnorm_envelope`: nonconstant source-normalization derivative hair;",
            "- `Parent_packet_adoption`: the selected local packet still needs final parent-action adoption.",
            "",
            "## Current Read",
            "",
            "This is not a public local-GR win yet, but it is not sprawling chaos anymore. The route has narrowed to two physics envelopes plus one formal adoption gate.",
            "",
            "## Next Attack",
            "",
            "Attack `Delta_cZ_envelope` first. If the local memory kernel/wall current can be zeroed or bounded, `c_norm` becomes a cleaner derivative-hair problem rather than a mixed current-normalization mess.",
            "",
            "Next checkpoint:",
            "",
            "- `4045-Y5-R2FR-cZ-kernel-wall-zero-theorem-or-first-bound-values.md`",
            "- `scripts/Y5_R2FR_4045_cZ_kernel_wall_zero_theorem_or_first_bound_values.py`",
            "",
        ]
    )


def row(check_id: str, passed: bool, detail: str) -> Dict[str, object]:
    return {"check_id": check_id, "passed": passed, "detail": detail}


def all_private(*tables: Iterable[Dict[str, object]]) -> bool:
    return all(item.get("valid_for_public_claim") is False for table in tables for item in table)


def validation_rows(
    sources: List[Dict[str, object]],
    scorecard: List[Dict[str, object]],
    ladder: List[Dict[str, object]],
    priority: List[Dict[str, object]],
    gates: List[Dict[str, object]],
    evaluator: List[Dict[str, object]],
    decisions: List[Dict[str, object]],
    claims: List[Dict[str, object]],
    next_target: List[Dict[str, object]],
    compile_ok: bool,
) -> List[Dict[str, object]]:
    output_paths = [str(path) for path in OUTPUTS.values()] + [str(DOC_PATH)]
    blockers = [item for item in scorecard if item["blocks_public_local_GR"] is True]
    return [
        row("VAL4044_00_sources_exist", all(item["exists"] for item in sources), "all cited source paths exist"),
        row("VAL4044_01_needles_found", all(item["needle_found"] for item in sources), "all source needles found"),
        row("VAL4044_02_scorecard_count", len(scorecard) == 9, "nine scorecard rows present"),
        row("VAL4044_03_cZ_blocker", any(item["symbols"] == "Delta_cZ_envelope" and item["blocks_public_local_GR"] is True for item in scorecard), "cZ blocker present"),
        row("VAL4044_04_cnorm_blocker", any(item["symbols"] == "Delta_cnorm_envelope" and item["blocks_public_local_GR"] is True for item in scorecard), "c_norm blocker present"),
        row("VAL4044_05_parent_blocker", any(item["symbols"] == "Parent_packet_adoption" and item["blocks_public_local_GR"] is True for item in scorecard), "parent adoption blocker present"),
        row("VAL4044_06_projector_not_blocker", any(item["symbols"] == "Delta_PPN_projector_stress, alpha_i, xi" and item["blocks_public_local_GR"] is False for item in scorecard), "projector stress controlled in selected branch"),
        row("VAL4044_07_nonEH_not_generic_blocker", any(item["symbols"] == "c_nonEH, Delta_PPN_abs_nonEH" and item["blocks_public_local_GR"] is False for item in scorecard), "generic nonEH no longer blocker"),
        row("VAL4044_08_claim_ladder_count", len(ladder) == 3, "claim ladder rows present"),
        row("VAL4044_09_public_blocked", any(item["claim_level"] == "PPN/local-GR through required order" and item["public_claim_allowed"] is False for item in ladder), "public local-GR ladder blocked"),
        row("VAL4044_10_priority_cZ_first", any(item["rank"] == 1 and item["target"] == "Delta_cZ_envelope" for item in priority), "cZ selected as first priority"),
        row("VAL4044_11_priority_cnorm_second", any(item["rank"] == 2 and item["target"] == "Delta_cnorm_envelope" for item in priority), "c_norm selected as second priority"),
        row("VAL4044_12_gate_blocked", any(item["gate_id"] == "LGG4044_1_public_local_GR" and item["status"] == "BLOCKED" for item in gates), "public local-GR gate blocked"),
        row("VAL4044_13_gate_attack_cZ", any(item["gate_id"] == "LGG4044_2_next_best_attack" and item["status"] == "ATTACK_CZ_FIRST" for item in gates), "next best attack is cZ"),
        row("VAL4044_14_evaluator_narrowed", any(item["verdict"] == "LOCAL_BRANCH_SUBSTANTIALLY_NARROWED_NOT_CLAIMED" for item in evaluator), "narrowed evaluator present"),
        row("VAL4044_15_evaluator_next", any(item["verdict"] == "CZ_KERNEL_WALL_ROUTE_IS_NEXT" for item in evaluator), "next attack evaluator present"),
        row("VAL4044_16_decision_next", any(item["decision_id"] == "DEC4044_2_next" for item in decisions), "next decision present"),
        row("VAL4044_17_progress_claim_scoped", any(item["claim_id"] == "CLAIM4044_0_progress" and item["allowed"] is True and item["public_claim_allowed"] is False for item in claims), "progress claim scoped private"),
        row("VAL4044_18_local_GR_claim_blocked", any(item["claim_id"] == "CLAIM4044_1_local_GR" and item["allowed"] is False for item in claims), "local-GR claim blocked"),
        row("VAL4044_19_blocker_count", len(blockers) == 3, "exactly three public local-GR blockers remain in scorecard"),
        row("VAL4044_20_next_target", bool(next_target and "4045" in str(next_target[0]["next_doc"])), "next target row present"),
        row("VAL4044_21_doc_written", DOC_PATH.exists(), "checkpoint doc written"),
        row("VAL4044_22_no_formalization_output", all(str(FORMALIZATION) not in path for path in output_paths), "no output targets formalization-workbench"),
        row("VAL4044_23_script_compiles", compile_ok, "script compiles"),
        row("VAL4044_24_private_guard", all_private(scorecard, ladder, priority, gates, evaluator, decisions), "public-claim guard retained"),
    ]


def main() -> None:
    ts = timestamp()
    sources = source_rows(ts)
    scorecard = master_scorecard_rows(ts)
    ladder = claim_ladder_rows(ts)
    priority = priority_matrix_rows(ts)
    gates = local_gr_gate_rows(ts, scorecard)
    evaluator = evaluator_rows(ts)
    decisions = decision_rows(ts)
    claims = claim_rows(ts)
    next_target = next_rows(ts)
    status = status_rows(ts)

    DOC_PATH.write_text(render_doc(ts, sources), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["master_scorecard"], scorecard)
    write_csv(OUTPUTS["claim_ladder"], ladder)
    write_csv(OUTPUTS["priority_matrix"], priority)
    write_csv(OUTPUTS["local_gr_gate"], gates)
    write_csv(OUTPUTS["evaluator"], evaluator)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["status"], status)

    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        compile_ok = True
    except py_compile.PyCompileError:
        compile_ok = False

    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    checks = validation_rows(sources, scorecard, ladder, priority, gates, evaluator, decisions, claims, next_target, compile_ok)
    write_csv(OUTPUTS["validation"], checks)
    passed = sum(1 for item in checks if item["passed"])
    total = len(checks)
    print(f"4044 validation: {passed}/{total} passed")
    if passed != total:
        for item in checks:
            if not item["passed"]:
                print(f"FAIL {item['check_id']}: {item['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
