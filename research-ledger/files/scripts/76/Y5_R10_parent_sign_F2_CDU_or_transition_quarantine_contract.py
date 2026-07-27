from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST_CHECKPOINT = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"

OUTPUT_DOC = POST_CHECKPOINT / "840-Y5-R10-parent-sign-F2-CDU-or-transition-quarantine-contract.md"
SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_840_SOURCE_REGISTER.csv"
PARENT_SIGN_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_840_PARENT_SIGN_AUDIT.csv"
QUARANTINE_CONTRACT_PATH = RESIDUALS / "P8_Y5_R10_840_QUARANTINE_PARENT_CONTRACT.csv"
ROUTE_RANKING_PATH = RESIDUALS / "P8_Y5_R10_840_ROUTE_RANKING.csv"
CLAIM_GUARD_PATH = RESIDUALS / "P8_Y5_R10_840_CLAIM_GUARD.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_840_DECISION.csv"
NEXT_TARGET_PATH = RESIDUALS / "P8_Y5_R10_840_NEXT_TARGET.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_840_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_840_VALIDATION.csv"

STATUS = "Y5_R10_840_parent_sign_attempt_routes_ranked_quarantine_projector_next_nonclaim"
CLAIM_CEILING = "parent_sign_contract_and_route_ranking_only_no_local_GR_pass"
NEXT_TARGET = "841-Y5-R10-quarantine-projector-parent-origin-or-far-local-closure-label.md"

SOURCE_SPECS = [
    {
        "source_id": "839_doc",
        "path": POST_CHECKPOINT / "839-Y5-R10-F2-bound-DL-transfer-and-q-gradient-source-pack.md",
        "needles": [
            "closure-smoke coefficient pack",
            "F_2=a_F lambda_R",
            "840-Y5-R10-parent-sign-F2-CDU-or-transition-quarantine-contract.md",
        ],
        "role": "immediate source-pack handoff",
    },
    {
        "source_id": "839_validation",
        "path": RESIDUALS / "P8_Y5_BRR545_839_VALIDATION.csv",
        "needles": [
            "V839_2_F2_formula_found,pass",
            "V839_6_transition_shell_blocks_claim,pass",
            "V839_11_formalization_workbench_untouched,pass",
        ],
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "parent_R_normalization_contract",
        "path": POST_CHECKPOINT / "96-parent-R-normalization-contract.md",
        "needles": [
            "Ward_identity_available",
            "local_F2_guard_preserved",
            "`a_F=1` is clean bookkeeping, not physics.",
        ],
        "role": "a_F/lambda_R parent-sign contract and blocker",
    },
    {
        "source_id": "canonical_R_theorem_attempt",
        "path": POST_CHECKPOINT / "97-canonical-R-theorem-attempt.md",
        "needles": [
            "`a_F=1` is now officially demoted",
            "trace_projection_Ward_identity_derived",
            "R_rescaling_degeneracy_broken",
        ],
        "role": "failed parent theorem attempt for a_F=1",
    },
    {
        "source_id": "local_leakage_vector_invariant",
        "path": FORMALIZATION / "125-local-leakage-vector-invariant.md",
        "needles": [
            "D_L <= U_B",
            "H_L and G_AB = not parent-derived",
            "R1 = closure-only overall.",
        ],
        "role": "D_L/C_DU candidate and blocker",
    },
    {
        "source_id": "smooth_scalar_channel_repair",
        "path": FORMALIZATION / "130-smooth-scalar-channel-repair.md",
        "needles": [
            "D_L <= U_B.",
            "clean closure repair, not parent derivation.",
            "R1 = repaired closure, not derived local GR.",
        ],
        "role": "clean D_L closure but not parent derivation",
    },
    {
        "source_id": "repaired_local_gradient_power",
        "path": FORMALIZATION / "131-repaired-local-gradient-power.md",
        "needles": [
            "gradients inherit U_B^2 suppression.",
            "transition-shell gradients = open obstruction",
            "D_L <= U_B = repaired closure bound",
        ],
        "role": "far-local q-gradient status and transition-shell blocker",
    },
    {
        "source_id": "conservation_owned_quarantine",
        "path": FORMALIZATION / "134-conservation-owned-quarantine-equations.md",
        "needles": [
            "conservation_owned_quarantine_equations_clean_closure_not_parent_derived",
            "parent projector origin = fail_not_derived",
            "public local-GR claim = not allowed.",
            "135-quarantine-projector-parent-origin.md",
        ],
        "role": "clean quarantine closure and next parent-origin route",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def check_needles(path: Path, needles: list[str]) -> str:
    text = read_text(path)
    if not text:
        return "missing_path"
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return "missing_needles:" + ";".join(missing)
    return "pass"


def validation_file_clean(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, f"missing={path}"
    failures: list[str] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row.get("result") != "pass":
                failures.append(f"{row.get('check_id')}={row.get('result')}")
    if failures:
        return False, ";".join(failures)
    return True, f"{path.name} clean"


def formalization_workbench_modified_count() -> int:
    command = (
        "$fw='"
        + str(FORMALIZATION).replace("'", "''")
        + "'; "
        + "$cutoff=[datetime]'2026-05-31T14:42:00'; "
        + "(Get-ChildItem -LiteralPath $fw -Recurse -File | "
        + "Where-Object { $_.LastWriteTime -gt $cutoff }).Count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    return int(completed.stdout.strip() or "0")


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = spec["path"]
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": str(path),
                "exists": str(path.exists()).lower(),
                "needle_check": check_needles(path, spec["needles"]),
                "role": spec["role"],
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def parent_sign_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "audit_id": "PS840_0_F2_aF_lambdaR",
            "branch": "F2/a_F/lambda_R",
            "current_best": "F_2=a_F lambda_R; a_F=1 and lambda_R<=1 are disciplined closure-smoke choices",
            "parent_sign_status": "blocked",
            "blocking_clause": "missing trace-projection Ward identity and unbroken R-rescaling degeneracy",
            "promotion_contract": "derive normalized R charge plus Ward identity fixing partial Gamma_eff/partial R=L_cg^-2 and local lambda_R bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "PS840_1_DLU_CDU",
            "branch": "D_L/C_DU transfer",
            "current_best": "D_L<=U_B can be made algebraic in the Z_L/smooth scalar closure",
            "parent_sign_status": "blocked",
            "blocking_clause": "H_L/G_AB, scalar evenness, and smooth quadratic source map remain closure-level",
            "promotion_contract": "derive signed leakage frame, positive normalized G_AB, bounded H_L map, and scalar parity from parent invariants",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "PS840_2_far_local_gradient",
            "branch": "far-local q-gradient",
            "current_best": "far-local U_B^2 gradient suppression follows conditionally if log-gradients and coefficients are bounded",
            "parent_sign_status": "partial_closure",
            "blocking_clause": "transition shell has U_B=O(1); Khat divergence, L_cg gradients, and metric response remain open",
            "promotion_contract": "derive transition-shell projector/quarantine plus Khat/metric response from parent field equations",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "audit_id": "PS840_3_transition_quarantine",
            "branch": "transition-shell quarantine",
            "current_best": "conservation-owned quarantine equations are algebraically clean",
            "parent_sign_status": "blocked_but_highest_leverage_next",
            "blocking_clause": "parent projector origin and owner dynamics are not derived",
            "promotion_contract": "derive P_metric,loc=0/PPN-small and K_A ownership from parent invariants or coarse-graining theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def quarantine_contract_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "contract_id": "QC840_0_projector_origin",
            "required_parent_statement": "P_metric,loc q_tr^nu = 0 or PPN-small follows from a non-sector-label parent rule",
            "why_needed": "otherwise transition-shell current is hidden by hand",
            "current_status": "not_derived",
            "acceptable_evidence": "projector derived from X_B/D_L/U_B geometry, variational constraint, Bianchi identity, or coarse-graining theorem",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QC840_1_owner_dynamics",
            "required_parent_statement": "quarantined transition current is carried by explicit owner tensors K_A with total conservation",
            "why_needed": "quarantine must be current accounting, not deletion",
            "current_status": "algebraic_closure_only",
            "acceptable_evidence": "parent field equations for K_A plus conservation identity showing local metric projection silence",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "contract_id": "QC840_2_no_routing_cheat",
            "required_parent_statement": "transition shell cannot be routed to galaxy/cosmology merely because local projection fails",
            "why_needed": "protects test discipline and prevents sector-labelled escape hatch",
            "current_status": "guard_installed_not_theorem",
            "acceptable_evidence": "same parent projector works before arena labels and preserves observed local GR responses",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_ranking_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "rank": "1",
            "route": "derive quarantine projector parent origin",
            "why_ranked_here": "full local-GR claim is blocked by transition shell even after far-local coefficient scaffolding",
            "expected_output": NEXT_TARGET,
            "risk": "may demote full local branch to far-local conditional closure if no parent projector exists",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank": "2",
            "route": "derive H_L/G_AB parent origin",
            "why_ranked_here": "would promote C_DU=1 from clean closure to theorem, but still would not solve transition shell alone",
            "expected_output": "parent leakage-frame metric theorem or explicit closure label",
            "risk": "scalar evenness may remain closure-only",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank": "3",
            "route": "derive a_F/lambda_R Ward identity",
            "why_ranked_here": "important for public theory elegance, but prior theorem attempt already failed and local shell still blocks",
            "expected_output": "Ward identity or permanent canonical closure label",
            "risk": "R-rescaling degeneracy remains",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def claim_guard_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "guard_id": "CG840_0_no_parent_sign_claim",
            "claim": "F2/C_DU are parent-signed",
            "status": "forbidden",
            "reason": "840 finds contracts and route ranking, not parent signatures",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG840_1_no_local_GR_claim",
            "claim": "MTS locally reduces to GR/Newton",
            "status": "forbidden",
            "reason": "transition-shell projector/quarantine and Khat/metric response remain not parent-derived",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "guard_id": "CG840_2_allowed_private_result",
            "claim": "next highest-leverage theorem target is quarantine projector parent origin",
            "status": "allowed_private_nonclaim",
            "reason": "route ranking is based on current blockers and remains nonclaim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D840_0",
            "finding": "parent-sign attempt does not close F2 or C_DU",
            "reason": "a_F/lambda_R and H_L/G_AB remain disciplined closure inputs",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D840_1",
            "finding": "quarantine projector is now the best next derivation target",
            "reason": "far-local coefficient route is usable for plumbing, but transition shell blocks full local-GR recovery",
            "status": CLAIM_CEILING,
            "claim_allowed": "false",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "derive the quarantine projector from parent invariants or label local GR as far-local conditional plus quarantine closure",
            "include": "P_metric,loc origin, owner tensors K_A, conservation identity, no-sector-label guard, fail/demote criterion",
            "exclude": "local-GR claim, transition-shell handwave, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "ranked parent-sign routes and selected quarantine projector origin as next target",
            "what_is_not_claimed": "parent-signed F2/C_DU, transition-shell safety, q_loc pass, local GR/Newton",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_valid_for_claim_false(row_groups: list[list[dict[str, object]]]) -> bool:
    for rows in row_groups:
        for row in rows:
            if row.get("valid_for_claim") != "false":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    quarantine_rows: list[dict[str, object]],
    ranking_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
) -> list[dict[str, object]]:
    prior_clean, prior_detail = validation_file_clean(RESIDUALS / "P8_Y5_BRR545_839_VALIDATION.csv")
    formalization_count = formalization_workbench_modified_count()
    source_ok = all(row["exists"] == "true" and row["needle_check"] == "pass" for row in source_rows)
    f2_blocked = any(row["audit_id"] == "PS840_0_F2_aF_lambdaR" and row["parent_sign_status"] == "blocked" for row in parent_rows)
    dlu_blocked = any(row["audit_id"] == "PS840_1_DLU_CDU" and row["parent_sign_status"] == "blocked" for row in parent_rows)
    quarantine_selected = bool(ranking_rows) and ranking_rows[0]["route"] == "derive quarantine projector parent origin"
    quarantine_contract = len(quarantine_rows) >= 3
    guards_forbid = {"CG840_0_no_parent_sign_claim", "CG840_1_no_local_GR_claim"}.issubset(
        {row["guard_id"] for row in guard_rows if row["status"] == "forbidden"}
    )
    no_claim = not any(row["claim_allowed"] == "true" for row in decisions)
    nonclaim_ok = all_valid_for_claim_false([source_rows, parent_rows, quarantine_rows, ranking_rows, guard_rows, decisions, next_targets, nonclaim])
    next_selected = bool(next_targets) and next_targets[0]["next_target"] == NEXT_TARGET

    return [
        {
            "check_id": "V840_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "source register has missing path or needle",
        },
        {
            "check_id": "V840_1_prior_839_clean",
            "result": "pass" if prior_clean else "fail",
            "detail": prior_detail,
        },
        {
            "check_id": "V840_2_F2_parent_sign_blocked",
            "result": "pass" if f2_blocked else "fail",
            "detail": "F2/a_F/lambda_R remain closure-level",
        },
        {
            "check_id": "V840_3_DLU_parent_sign_blocked",
            "result": "pass" if dlu_blocked else "fail",
            "detail": "H_L/G_AB transfer remains closure-level",
        },
        {
            "check_id": "V840_4_quarantine_contract_written",
            "result": "pass" if quarantine_contract else "fail",
            "detail": "projector, owner, and no-routing-cheat clauses written",
        },
        {
            "check_id": "V840_5_quarantine_route_ranked_first",
            "result": "pass" if quarantine_selected else "fail",
            "detail": "quarantine projector parent origin selected as highest-leverage next route",
        },
        {
            "check_id": "V840_6_claim_guards_forbid_overclaim",
            "result": "pass" if guards_forbid and no_claim else "fail",
            "detail": "parent-sign and local-GR claims remain forbidden",
        },
        {
            "check_id": "V840_7_all_rows_nonclaim",
            "result": "pass" if nonclaim_ok else "fail",
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "V840_8_next_target_selected",
            "result": "pass" if next_selected else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V840_9_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V840_10_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]


def csv_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(text)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_document(
    source_rows: list[dict[str, object]],
    parent_rows: list[dict[str, object]],
    quarantine_rows: list[dict[str, object]],
    ranking_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    nonclaim: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    sections = [
        "# 840 - Y5 R10 Parent-Sign F2/CDU Or Transition-Quarantine Contract",
        "",
        "Current result: **the parent-sign attempt does not close `F_2` or `C_DU`, so the best next theorem target is the quarantine projector origin**. `F_2=a_F lambda_R` and `D_L<=U_B` are strong closure-smoke scaffolds, but `a_F/lambda_R`, `H_L/G_AB`, scalar evenness, `Khat` response, and transition-shell projection remain parent-unsigned. Full local GR is therefore still forbidden; the honest next move is to derive `P_metric,loc q_tr=0/PPN-small` from parent invariants or demote the local branch to far-local conditional plus quarantine closure.",
        "",
        "## Non-Claim Summary",
        "",
        csv_table(nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim"]),
        "",
        "## Parent-Sign Audit",
        "",
        csv_table(parent_rows, ["audit_id", "branch", "current_best", "parent_sign_status", "blocking_clause", "promotion_contract", "valid_for_claim"]),
        "",
        "## Quarantine Parent Contract",
        "",
        csv_table(quarantine_rows, ["contract_id", "required_parent_statement", "why_needed", "current_status", "acceptable_evidence", "valid_for_claim"]),
        "",
        "## Route Ranking",
        "",
        csv_table(ranking_rows, ["rank", "route", "why_ranked_here", "expected_output", "risk", "valid_for_claim"]),
        "",
        "## Claim Guard",
        "",
        csv_table(guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim"]),
        "",
        "## Decision",
        "",
        csv_table(decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        csv_table(next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
        "## Source Register",
        "",
        csv_table(source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        csv_table(validation, ["check_id", "result", "detail"]),
        "",
    ]
    OUTPUT_DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    generated_utc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    source_rows = source_register_rows(generated_utc)
    parent_rows = parent_sign_audit_rows(generated_utc)
    quarantine_rows = quarantine_contract_rows(generated_utc)
    ranking_rows = route_ranking_rows(generated_utc)
    guard_rows = claim_guard_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    next_targets = next_target_rows(generated_utc)
    nonclaim = nonclaim_summary_rows(generated_utc)
    validation = validation_rows(source_rows, parent_rows, quarantine_rows, ranking_rows, guard_rows, decisions, next_targets, nonclaim)

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(PARENT_SIGN_AUDIT_PATH, parent_rows, ["audit_id", "branch", "current_best", "parent_sign_status", "blocking_clause", "promotion_contract", "valid_for_claim", "generated_utc"])
    write_csv(QUARANTINE_CONTRACT_PATH, quarantine_rows, ["contract_id", "required_parent_statement", "why_needed", "current_status", "acceptable_evidence", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_RANKING_PATH, ranking_rows, ["rank", "route", "why_ranked_here", "expected_output", "risk", "valid_for_claim", "generated_utc"])
    write_csv(CLAIM_GUARD_PATH, guard_rows, ["guard_id", "claim", "status", "reason", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "finding", "reason", "status", "claim_allowed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NEXT_TARGET_PATH, next_targets, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, nonclaim, ["status", "claim_ceiling", "what_changed", "what_is_not_claimed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_document(source_rows, parent_rows, quarantine_rows, ranking_rows, guard_rows, decisions, next_targets, nonclaim, validation)

    print(f"wrote={OUTPUT_DOC}")
    print(f"wrote={VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"claim_ceiling={CLAIM_CEILING}")
    print(f"next_target={NEXT_TARGET}")


if __name__ == "__main__":
    main()
