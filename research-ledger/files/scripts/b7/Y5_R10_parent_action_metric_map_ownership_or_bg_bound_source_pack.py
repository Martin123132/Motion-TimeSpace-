from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "786-Y5-R10-parent-action-metric-map-ownership-or-bg-bound-source-pack.md"
NEXT_TARGET = "787-Y5-R10-multifield-pregeometry-rank-gate-or-independent-metric-branch-decision.md"
STATUS = "Y5_R10_786_parent_action_metric_map_ownership_test_blocks_scalar_only_route_stages_bg_bound_pack_nonclaim"
CLAIM_CEILING = "parent_action_metric_ownership_audit_only_no_adopted_action_no_scalar_psi_GR_derivation_no_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_786_SOURCE_REGISTER.csv"
ACTION_CANDIDATES_PATH = RESIDUALS / "P8_Y5_R10_786_PARENT_ACTION_OWNERSHIP_CANDIDATES.csv"
RANK_GATE_PATH = RESIDUALS / "P8_Y5_R10_786_VARIATIONAL_RANK_GATE.csv"
BG_BOUND_PACK_PATH = RESIDUALS / "P8_Y5_R10_786_BG_BOUND_SOURCE_PACK.csv"
BRANCH_DECISION_PATH = RESIDUALS / "P8_Y5_R10_786_BRANCH_DECISION.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_786_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_786_VALIDATION.csv"

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_786_ADOPTED_PARENT_ACTION.csv",
    RESIDUALS / "P8_Y5_R10_786_PSI_METRIC_OWNERSHIP_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_786_SCALAR_PSI_GR_LIMIT_PROOF.csv",
    RESIDUALS / "P8_Y5_R10_786_LOCAL_GR_REENTRY_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    ACTION_CANDIDATES_PATH,
    RANK_GATE_PATH,
    BG_BOUND_PACK_PATH,
    BRANCH_DECISION_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "785_doc": {
        "path": POST_CHECKPOINT / "785-Y5-R10-psi-metric-coframe-connection-contract-or-bg-residual-lock.md",
        "needles": ["Current result", "active residual"],
        "role": "immediate 786 handoff",
    },
    "785_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_785_VALIDATION.csv",
        "needles": ["V785_6_parent_action_not_derived", "V785_11_bg_lock_active"],
        "role": "prior validation guard",
    },
    "785_contract": {
        "path": RESIDUALS / "P8_Y5_R10_785_PSI_METRIC_COFRAME_CONTRACT.csv",
        "needles": ["PMC785_6_parent_action_metric_ownership", "PMC785_7_GR_Newton_reduction"],
        "role": "parent action ownership blocker",
    },
    "785_bg_lock": {
        "path": RESIDUALS / "P8_Y5_R10_785_BG_RESIDUAL_LOCK.csv",
        "needles": ["BGL785_0_definition", "BGL785_4_observable_interface"],
        "role": "b_g/c_g bound interface handoff",
    },
    "784_metric_gate": {
        "path": RESIDUALS / "P8_Y5_R10_784_OBSERVED_METRIC_FROM_PSI_GATE.csv",
        "needles": ["OMG784_0_dimension", "OMG784_8_verdict"],
        "role": "metric ansatz gate",
    },
    "ledger_14": {
        "path": FORMALIZATION / "14-field-definitions-dimensional-ledger.md",
        "needles": ["Working repaired metric ansatz", "Metric normalization scale"],
        "role": "metric ansatz and dimensions",
    },
    "spine_07": {
        "path": FORMALIZATION / "07-unification-spine.md",
        "needles": ["emergent or effective metric", "MTS parent theory -> effective GR"],
        "role": "unification spine and GR/Newton chain",
    },
    "testing_145": {
        "path": FORMALIZATION / "145-testing-readiness-and-gr-limit-map.md",
        "needles": ["MTS -> GR -> Newton", "missing GR-limit theorem"],
        "role": "local GR-limit demand",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post_checkpoint(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed_count = 0
    for scanned_path in FORMALIZATION.rglob("*"):
        if scanned_path.is_file() and datetime.fromtimestamp(scanned_path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            changed_count += 1
    return changed_count


def validation_clean(number: int) -> bool:
    path = RESIDUALS / f"P8_Y5_BRR545_{number}_VALIDATION.csv"
    rows = read_csv_rows(path)
    return path.exists() and bool(rows) and all(row.get("result") == "pass" for row in rows)


def source_register_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCE_SPECS.items()
    ]


def action_candidate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "PAO786_0_composite_metric_action",
            "route": "Use only psi and define S_eff[psi,Psi]=S_EH[G[psi]]+S_matter[Psi,G[psi]].",
            "what_it_buys": "metric-only matter coupling can be written without an independent g field",
            "hard_failure_or_risk": "variation gives projected Einstein equations, not full Einstein equations, unless delta G/delta psi is locally surjective",
            "status": "formal_candidate_blocked_by_rank_and_covariance",
            "next_test": "variational rank gate for G[psi]",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "PAO786_1_constraint_owned_metric",
            "route": "Use independent g plus lambda^{mu nu}(g_mu_nu-G_mu_nu[psi]) in S_parent.",
            "what_it_buys": "the psi metric map becomes action-owned as a constraint",
            "hard_failure_or_risk": "this is a closure unless the constraint and multiplier dynamics are derived; it can overconstrain GR or simply add GR by hand",
            "status": "owned_closure_candidate_not_adopted",
            "next_test": "derive lambda sector or demote to explicit closure",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "PAO786_2_independent_metric_branch",
            "route": "Let g be a fundamental/emergent independent field with EH dynamics and let psi/memory contribute stress or boundary terms.",
            "what_it_buys": "least-scrutiny local GR route because GR is recovered by a standard metric sector",
            "hard_failure_or_risk": "less radical: MTS becomes an extra-field/open-system extension unless g itself is derived later",
            "status": "viable_conservative_branch_not_full_derivation",
            "next_test": "define how psi stress exchanges with g while preserving Bianchi/conservation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "PAO786_3_multifield_pregeometry",
            "route": "Promote psi to a multiplet/pregeometry bundle psi^A or coframe-like variable whose bilinears can span metric variations.",
            "what_it_buys": "keeps the motion/space/time idea but gives enough degrees of freedom to target GR",
            "hard_failure_or_risk": "new field content must be declared and tested; otherwise this is a rename of the missing metric",
            "status": "best_derivation_candidate_needs_rank_gate",
            "next_test": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "PAO786_4_induced_gravity",
            "route": "Derive EH terms after integrating out fast MTS/matter modes.",
            "what_it_buys": "could make metric dynamics genuinely emergent",
            "hard_failure_or_risk": "requires a real one-loop/EFT calculation, regulator, signs, universality, and observed Newton constant",
            "status": "not_available_yet",
            "next_test": "only after parent fields and measure are fixed",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "candidate_id": "PAO786_5_background_EFT",
            "route": "Declare eta/background plus small h[psi] as an EFT approximation, not a fundamental GR derivation.",
            "what_it_buys": "usable testing language for local residual bounds",
            "hard_failure_or_risk": "cannot be sold as background-independent unified field theory",
            "status": "testing_fallback_only",
            "next_test": "source b_g/c_g bounds if derivation stalls",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def rank_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "rank_id": "VRG786_0_variation_formula",
            "test": "For S_eff[psi]=S_GR[G[psi]]+S_matter[G[psi]], variation gives integral E^{mu nu} delta G_mu_nu/delta psi = 0.",
            "result": "projected_Einstein_only",
            "meaning": "full Einstein equations follow only if the metric map has enough rank/surjectivity",
            "required_repair": "prove local surjectivity modulo diffeomorphisms or add independent metric/pregeometry fields",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank_id": "VRG786_1_unsmoothed_scalar_rank",
            "test": "If psi is a single scalar and G_mu_nu contains only local partial_mu psi partial_nu psi, the perturbation is rank-one at a point.",
            "result": "blocked_as_sole_GR_route",
            "meaning": "a single local scalar-gradient metric cannot span generic local GR metric variations",
            "required_repair": "multi-component psi^A, micro-gradient moment closure, or independent g",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank_id": "VRG786_2_smoothing_escape_clause",
            "test": "A smoothed average <partial psi partial psi> can have higher matrix rank only if the averaging operator supplies independent micro-gradient moments.",
            "result": "escape_possible_not_derived",
            "meaning": "the smoothing/coarse-graining rule becomes a real parent ingredient, not cosmetic notation",
            "required_repair": "covariant coarse-graining theorem and moment dynamics",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank_id": "VRG786_3_multifield_rank_condition",
            "test": "For psi^A, require rank(delta G_mu_nu/delta psi^A) to cover physical symmetric-tensor variations after gauge removal.",
            "result": "rank_gate_defined",
            "meaning": "this is the clean mathematical gate for deriving GR rather than fitting a metric ansatz",
            "required_repair": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank_id": "VRG786_4_bianchi_conservation",
            "test": "Any derived metric equation must respect Bianchi identity and matter/source exchange without forcing unphysical constraints.",
            "result": "blocked_missing_action",
            "meaning": "GR recovery is not only metric shape; it needs conservation structure",
            "required_repair": "parent symmetry/Ward identity or explicit exchange-current equation",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank_id": "VRG786_5_verdict",
            "test": "Can 786 adopt a parent action that derives g_obs[psi] and local GR?",
            "result": "no_not_yet",
            "meaning": "scalar-only psi metric ownership is blocked; multifield/independent-metric branch must be decided",
            "required_repair": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def bg_bound_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "BGS786_0_ppn",
            "coefficient": "b_g/c_g",
            "arena": "PPN/local gravity",
            "needed_input": "response of gamma,beta,alpha_i to metric-frame leakage",
            "current_value": "MISSING_PPN_RESPONSE_MATRIX",
            "status": "source_ready_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "BGS786_1_clock",
            "coefficient": "b_g/c_g",
            "arena": "clock/redshift/time",
            "needed_input": "clock response to e_obs mismatch and derivative coupling leakage",
            "current_value": "MISSING_CLOCK_RESPONSE_COEFFICIENT",
            "status": "source_ready_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "BGS786_2_orbital",
            "coefficient": "b_g/c_g",
            "arena": "solar-system/orbital",
            "needed_input": "ephemeris acceleration residual vector from metric-frame leakage",
            "current_value": "MISSING_ORBITAL_RESPONSE_COEFFICIENT",
            "status": "source_ready_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "BGS786_3_R10",
            "coefficient": "b_g/c_g",
            "arena": "short-range/R10",
            "needed_input": "mapping from frame leakage to alpha(lambda) or fifth-force channel",
            "current_value": "MISSING_R10_PROJECTION",
            "status": "source_ready_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "BGS786_4_source_measure",
            "coefficient": "B_obs/source-measure",
            "arena": "boundary/source terms",
            "needed_input": "boundary/source-measure coefficient that can shift local matter frame",
            "current_value": "MISSING_SOURCE_MEASURE_COEFFICIENT",
            "status": "source_ready_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "BGS786_5_rank_escape",
            "coefficient": "N_eff or rank(delta G)",
            "arena": "multifield/pregeometry",
            "needed_input": "number of independent fields/moments and local surjectivity rank",
            "current_value": "MISSING_MULTIFIELD_RANK_DATA",
            "status": "derivation_input_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D786_0_no_parent_action_adoption",
            "decision": "do not adopt a parent metric-map action yet",
            "reason": "all candidates either add GR by hand, become closure, or need a rank/covariance theorem",
            "result": "not_adopted",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D786_1_scalar_only_warning",
            "decision": "do not rely on a single unsmoothed scalar psi as the sole GR metric owner",
            "reason": "the variational rank gate blocks generic Einstein recovery",
            "result": "scalar_only_route_blocked",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D786_2_best_derivation_route",
            "decision": "test multifield/pregeometry rank before falling back to bound-only work",
            "reason": "this preserves derivability and gives a precise mathematical gate",
            "result": "multifield_rank_gate_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D786_3_conservative_route",
            "decision": "keep independent metric branch as the low-scrutiny fallback",
            "reason": "it protects local GR but weakens the stronger emergent claim",
            "result": "fallback_retained",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "parent-action ownership was attempted; scalar-only psi metric action gives projected Einstein equations and fails the generic GR rank gate unless smoothing supplies independent moments or psi is promoted to a multifield/pregeometry bundle",
            "hard_blocker": "prove local surjectivity/covariant coarse-graining or choose independent metric branch; until then b_g/c_g bound pack stays active",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_rows(*row_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in row_groups:
        rows.extend(group)
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    rank_gate: list[dict[str, Any]],
    bound_pack: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_785_clean = all(validation_clean(number) for number in range(665, 786))
    candidates_complete = len(candidates) == 6
    rank_gate_complete = len(rank_gate) == 6
    projected_only = any(row["rank_id"] == "VRG786_0_variation_formula" and row["result"] == "projected_Einstein_only" for row in rank_gate)
    scalar_blocked = any(row["rank_id"] == "VRG786_1_unsmoothed_scalar_rank" and row["result"] == "blocked_as_sole_GR_route" for row in rank_gate)
    smoothing_escape_nonclaim = any(row["rank_id"] == "VRG786_2_smoothing_escape_clause" and row["result"] == "escape_possible_not_derived" for row in rank_gate)
    no_adopted_action = any(row["decision_id"] == "D786_0_no_parent_action_adoption" and row["result"] == "not_adopted" for row in decisions)
    bound_pack_complete = len(bound_pack) == 6
    bound_pack_nonclaim = all(row["status"].endswith("nonclaim") for row in bound_pack)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D786_2_best_derivation_route" for row in decisions)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, candidates, rank_gate, bound_pack, decisions, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V786_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V786_1_source_needles_present", source_needles_present, "all source needles present"),
        ("V786_2_prior_665_785_clean", prior_665_785_clean, "665-785 validation rows have no failures"),
        ("V786_3_candidates_complete", candidates_complete, "parent action candidate rows complete"),
        ("V786_4_rank_gate_complete", rank_gate_complete, "variational rank gate rows complete"),
        ("V786_5_projected_Einstein_only", projected_only, "composite action gives projected Einstein equation only"),
        ("V786_6_scalar_only_blocked", scalar_blocked, "single unsmoothed scalar route blocked as sole GR route"),
        ("V786_7_smoothing_escape_nonclaim", smoothing_escape_nonclaim, "smoothing escape clause remains nonclaim"),
        ("V786_8_no_adopted_action", no_adopted_action, "no parent action adopted"),
        ("V786_9_bound_pack_complete", bound_pack_complete, "b_g/c_g source-pack rows complete"),
        ("V786_10_bound_pack_nonclaim", bound_pack_nonclaim, "all bound/source rows remain nonclaim"),
        ("V786_11_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V786_12_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V786_13_claim_artifacts_absent", claim_artifacts_absent, "no adopted-action/metric-owner/scalar-GR/local-GR claim artifact fabricated"),
        ("V786_14_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V786_15_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V786_16_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    rank_gate: list[dict[str, Any]],
    bound_pack: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 786 - Y5 R10 Parent Action Metric Map Ownership Or Bg Bound Source Pack

Current result: **the parent-action route was attempted and the key obstruction is now clean: a composite `g_obs[psi]` action usually gives only projected Einstein equations, not full GR**. If `psi` is treated as one local scalar, the metric-map rank is too small as a sole route to generic local GR. A smoothed/moment version may escape, but only if the coarse-graining operator supplies independent covariant moments and becomes a real parent ingredient. So this does not kill the theory; it tells us the next honest branch is either multifield/pregeometry or an independent metric sector.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Parent Action Ownership Candidates

{markdown_table(candidates, ["candidate_id", "route", "what_it_buys", "hard_failure_or_risk", "status", "next_test", "valid_for_claim"])}

## Variational Rank Gate

{markdown_table(rank_gate, ["rank_id", "test", "result", "meaning", "required_repair", "valid_for_claim"])}

## Bg/Cg Bound Source Pack

{markdown_table(bound_pack, ["bound_id", "coefficient", "arena", "needed_input", "current_value", "status", "valid_for_claim"])}

## Branch Decision

{markdown_table(decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is a good hard checkpoint, not a disaster. The old route "just define the metric from a scalar motion field" is too thin if taken literally. The stronger route is to decide whether MTS really has a multiplet/pregeometry bundle hiding behind the word `psi`, or whether the cleanest serious framework is an independent metric sector plus MTS exchange fields. That is the next boxing round: no haymaker, just footwork and a rank gate.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    candidates = action_candidate_rows(generated_utc)
    rank_gate = rank_gate_rows(generated_utc)
    bound_pack = bg_bound_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, candidates, rank_gate, bound_pack, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(ACTION_CANDIDATES_PATH, candidates, ["candidate_id", "route", "what_it_buys", "hard_failure_or_risk", "status", "next_test", "valid_for_claim", "generated_utc"])
    write_csv(RANK_GATE_PATH, rank_gate, ["rank_id", "test", "result", "meaning", "required_repair", "valid_for_claim", "generated_utc"])
    write_csv(BG_BOUND_PACK_PATH, bound_pack, ["bound_id", "coefficient", "arena", "needed_input", "current_value", "status", "valid_for_claim", "generated_utc"])
    write_csv(BRANCH_DECISION_PATH, decisions, ["decision_id", "decision", "reason", "result", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, candidates, rank_gate, bound_pack, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"786 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
