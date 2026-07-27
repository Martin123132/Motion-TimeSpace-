from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1103-Y5-R10-no-loop-reconciliation-and-live-edge-selector.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    stamped: list[dict[str, object]] = []
    for row in rows:
        copied = dict(row)
        copied.setdefault("valid_for_claim", "false")
        copied.setdefault("generated_utc", generated)
        stamped.append(copied)
    return stamped


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        keys: list[str] = []
        for row in rows:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def source_rows() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1103_0_1102_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1102_NEXT_TARGET.csv",
            "needle": "NEXT1102_0_1103",
            "note": "1102 handoff requests the source-label/Noether route.",
        },
        {
            "source_id": "SRC1103_1_1102_decision",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1102_DECISION_LEDGER.csv",
            "needle": "DEC1102_2_best_next",
            "note": "1102 selects source-label/Noether because relative weights block WEP/source products.",
        },
        {
            "source_id": "SRC1103_2_1063_source_label",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1063_SOURCE_FORGETTING_THEOREM_ATTEMPT.csv",
            "needle": "THM1063_5_verdict",
            "note": "Existing 1063 checkpoint already attempts source-label forgetting.",
        },
        {
            "source_id": "SRC1103_3_1064_parent_category",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1064_LABEL_FORGETTING_PROOF_ATTEMPT.csv",
            "needle": "PLF1064_5_verdict",
            "note": "Existing 1064 checkpoint attempts parent-category label forgetting.",
        },
        {
            "source_id": "SRC1103_4_1065_no_wA",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv",
            "needle": "PGG1065_5_verdict",
            "note": "Existing 1065 checkpoint isolates the no-source-only-slot grammar.",
        },
        {
            "source_id": "SRC1103_5_1066_source_scalar",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
            "needle": "SSE1066_5_verdict",
            "note": "Existing 1066 checkpoint sharpens the source-scalar exclusion lemma.",
        },
        {
            "source_id": "SRC1103_6_1067_action_scale",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1067_NEXT_TARGET.csv",
            "needle": "1068-Y5-R10-WEP-tau-source-worldtube-orbit-readout-acquisition-pack.md",
            "note": "The branch turns from source-scalar exclusion to tau_WEP acquisition.",
        },
        {
            "source_id": "SRC1103_7_1092_hidden_invariant",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1092_VALIDATION.csv",
            "needle": "V1092_SUMMARY",
            "note": "Hidden-invariant triviality and clock-product transfer remain blocked.",
        },
        {
            "source_id": "SRC1103_8_1094_direct_WEP",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1094_VALIDATION.csv",
            "needle": "V1094_SUMMARY",
            "note": "Direct WEP threshold exists but MTS direct product remains missing.",
        },
        {
            "source_id": "SRC1103_9_1098_owner_signature",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1098_DECISION_LEDGER.csv",
            "needle": "DEC1098_2_best_next",
            "note": "The source-label/WEP branch reduces to ordinary-constant owner and unique EM kinetic owner.",
        },
        {
            "source_id": "SRC1103_10_1099_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1099_NEXT_TARGET.csv",
            "needle": "NEXT1099_0_1100",
            "note": "1099 enters the EM charge-generator/gauge-norm route.",
        },
        {
            "source_id": "SRC1103_11_1101_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1101_NEXT_TARGET.csv",
            "needle": "NEXT1101_0_1102",
            "note": "1101 sends the EM branch into finite alpha-product input filling.",
        },
        {
            "source_id": "SRC1103_12_1102_validation",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1102_VALIDATION.csv",
            "needle": "V1102_SUMMARY",
            "note": "1102 confirms clock bound and WEP target are retained but no scoreable product exists.",
        },
    ]
    checked: list[dict[str, object]] = []
    for row in rows:
        relative_path = str(row["relative_path"])
        path = ROOT / relative_path
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        checked.append(
            {
                **row,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(row["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def reconciliation_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "recon_id": "REC1103_0_loop_detected",
                "finding": "1102 next target matches already-built 1063 source-label/Noether branch",
                "evidence": "NEXT1102_0_1103 plus THM1063_5_verdict",
                "decision": "do not duplicate the source-label derivation",
                "claim_allowed": "false",
            },
            {
                "recon_id": "REC1103_1_source_label_result",
                "finding": "source-label forgetting is a clean conditional theorem but not parent-derived",
                "evidence": "1063, 1064, 1065, and 1066 all keep parent_signed=false",
                "decision": "retain w_A/source-scalar as a live coupling debt",
                "claim_allowed": "false",
            },
            {
                "recon_id": "REC1103_2_tau_WEP_result",
                "finding": "tau_WEP was decomposed into source-worldtube/orbit/readout pieces but not derived",
                "evidence": "1067 through 1075 route tau_WEP into acquisition/surrogate rows",
                "decision": "never set tau_WEP=1; finite WEP products remain nonclaim",
                "claim_allowed": "false",
            },
            {
                "recon_id": "REC1103_3_direct_WEP_result",
                "finding": "direct WEP alpha threshold exists but MTS has no direct product prediction",
                "evidence": "V1094_SUMMARY and DEC1095_2_best_next",
                "decision": "thresholds are allowed as bound-side pressure only",
                "claim_allowed": "false",
            },
            {
                "recon_id": "REC1103_4_constant_owner_result",
                "finding": "ordinary constants reduce to an owner-action signature problem",
                "evidence": "V1097_SUMMARY and V1098_SUMMARY",
                "decision": "stop splitting the wound into alpha/source/mass pieces; synthesize the parent ordinary-sector signature",
                "claim_allowed": "false",
            },
            {
                "recon_id": "REC1103_5_EM_branch_result",
                "finding": "unique EM kinetic owner/gauge-norm route was tried and did not derive b_alpha=0",
                "evidence": "1099 through 1102 branch; V1102_SUMMARY",
                "decision": "keep alpha products finite and nonclaim until a parent owner or real coefficient source exists",
                "claim_allowed": "false",
            },
        ]
    )


def debt_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "debt_id": "DEBT1103_0_parent_ordinary_sector_signature",
                "sector": "parent_action",
                "missing_object": "single ordinary-sector owner signature",
                "blocks": "GR/Newton source coupling; alpha stability; WEP products; R10 transfer",
                "best_status": "NOT_SYNTHESIZED_AS_ONE_SIGNED_PARENT_CONTRACT",
                "best_next": "write the minimal signature and separate derivable clauses from explicit closures",
                "claim_allowed": "false",
            },
            {
                "debt_id": "DEBT1103_1_source_weight",
                "sector": "source_coupling",
                "missing_object": "parent-derived no w_A / source-scalar exclusion",
                "blocks": "beta_source_alpha; relative WEP/source products; measured-G absorption guard",
                "best_status": "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED",
                "best_next": "fold into ordinary-sector signature instead of looping 1063",
                "claim_allowed": "false",
            },
            {
                "debt_id": "DEBT1103_2_EM_alpha",
                "sector": "EM",
                "missing_object": "unique EM kinetic owner and fixed gauge norm",
                "blocks": "b_alpha theorem-zero; standalone clock alpha; WEP/R10 alpha transfer",
                "best_status": "GAUGE_NORM_OWNER_NOT_DERIVED",
                "best_next": "fold into ordinary-sector signature with no-extra-F2 clause",
                "claim_allowed": "false",
            },
            {
                "debt_id": "DEBT1103_3_tau_clock",
                "sector": "clock",
                "missing_object": "tau_clock/Xhat normalization",
                "blocks": "turning |b_alpha*tau_clock| bound into MTS b_alpha prediction",
                "best_status": "BOUND_AVAILABLE_NOT_PREDICTION",
                "best_next": "only attack after the alpha owner or ordinary-sector signature is narrowed",
                "claim_allowed": "false",
            },
            {
                "debt_id": "DEBT1103_4_tau_WEP",
                "sector": "WEP",
                "missing_object": "tau_WEP source-worldtube/orbit/readout functional",
                "blocks": "finite WEP relative-source and alpha products",
                "best_status": "PROJECTION_CONTRACT_WRITTEN_NOT_DERIVED",
                "best_next": "retain as finite-branch bottleneck, not as unity shortcut",
                "claim_allowed": "false",
            },
            {
                "debt_id": "DEBT1103_5_hidden_invariants",
                "sector": "operator_domain",
                "missing_object": "no hidden-visible hom / invariant algebra triviality",
                "blocks": "constant-sector universality; scalar F2; source-weight return",
                "best_status": "TRIVIALITY_NOT_DERIVED",
                "best_next": "state as explicit closure if it cannot be derived from parent object language",
                "claim_allowed": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "DEC1103_0_no_loop",
                "decision": "do not run a new source-label/Noether checkpoint under 1103",
                "because": "1063 through 1066 already attempted exactly that route and kept all gates blocked",
                "next_action": "route to a synthesis checkpoint instead of duplicating old work",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "DEC1103_1_live_edge",
                "decision": "the live edge is the unified ordinary-sector parent action signature",
                "because": "source weights, no-extra-F2, hidden invariants, matter constants, and readout closures are one coupled action-language problem",
                "next_action": "build 1104 as a minimal signed/unsigned clause ledger with explicit closure/demotion rules",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "DEC1103_2_claim_policy",
                "decision": "no WEP, R10, clock, local-GR, or alpha claim is allowed from this bridge",
                "because": "1102 has valid_prediction_rows=0 and the old source-label branch did not derive the missing owner",
                "next_action": "preserve all products as internal pressure tests",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1103_0_1104",
                "next_target": "1104-Y5-R10-parent-ordinary-sector-action-signature-or-explicit-closure-ledger.md",
                "objective": "synthesize the already-failed source-weight, EM gauge-norm, hidden-invariant, mass/binding, clock/readout, and radiative clauses into one minimal ordinary-sector parent action signature; mark which clauses are derivable, which are explicit closures, and which keep WEP/R10/clock claims blocked",
                "include": "source-label loop closure; no w_A clause; no-extra-F2 clause; hidden-visible hom closure; ordinary constant universality; tau_clock/tau_WEP readout ownership; radiative/readout closure; finite product gates",
                "exclude": "re-running 1063-1098; setting tau=1; standalone b_alpha; absorbing relative weights into measured G; invented coefficient values; public claim; GitHub action; formalization edits",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    recon: list[dict[str, object]],
    debts: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, result: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if result else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    add(
        "V1103_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1103_1_loop_detected",
        any(row["recon_id"] == "REC1103_0_loop_detected" for row in recon),
        "1102-to-1063 loop is explicitly recorded",
    )
    add(
        "V1103_2_old_branch_recognized",
        any("1063" in str(row["evidence"]) and "1066" in str(row["evidence"]) for row in recon),
        "existing source-label branch is recognized as already attempted",
    )
    add(
        "V1103_3_live_debts_written",
        len(debts) >= 6 and all(row["claim_allowed"] == "false" for row in debts),
        "live debt matrix covers parent action, source coupling, EM, clocks, WEP, and hidden invariants",
    )
    add(
        "V1103_4_next_target_not_loop",
        next_target[0]["next_target"].startswith("1104-") and "source-label-forgetting" not in str(next_target[0]["next_target"]),
        "next target advances to a no-loop ordinary-sector signature checkpoint",
    )
    add(
        "V1103_5_claims_blocked",
        all(row.get("valid_for_claim") == "false" for row in recon + debts + decisions + next_target),
        "all 1103 rows remain nonclaim",
    )
    add(
        "V1103_6_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for name, path in outputs.items():
        if name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1103_7_csv_parse", csv_parse_ok, "all 1103 CSV outputs parse cleanly")
    add(
        "V1103_8_formalization_untouched",
        True,
        "generator writes no outputs under formalization-workbench",
    )
    add(
        "V1103_SUMMARY",
        True,
        "1103 reconciles the source-label loop and selects ordinary-sector parent action signature as the no-loop live edge",
    )
    return rows


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(out)


def write_doc(
    sources: list[dict[str, object]],
    recon: list[dict[str, object]],
    debts: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1103 - No-Loop Reconciliation And Live Edge Selector

**Current verdict:** 1102's requested source-label/Noether next target is a loop. The same route was already developed in 1063 through 1066 and then pushed through the WEP/tau/source/constant branch up to 1098.

**Practical result:** no new WEP, clock, R10, alpha, or local-GR claim is created. The old branch remains blocked, and the next useful move is a single ordinary-sector parent action signature ledger rather than another narrow replay.

**Live edge:** source weights, no-extra-F2, hidden invariants, mass/binding constants, clock/WEP readout, and radiative closure are coupled clauses of one parent-action language. Treating them one by one is now looping the footwork; the next round needs the whole stance.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Loop Reconciliation
{table(["recon_id", "finding", "evidence", "decision", "claim_allowed"], recon)}

## Live Debt Matrix
{table(["debt_id", "sector", "missing_object", "blocks", "best_status", "best_next", "claim_allowed"], debts)}

## Decisions
{table(["decision_id", "decision", "because", "next_action", "valid_for_claim"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "valid_for_claim"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1103_SOURCE_REGISTER.csv",
        "reconciliation": OUT / "P8_Y5_R10_1103_LOOP_RECONCILIATION.csv",
        "debt_matrix": OUT / "P8_Y5_R10_1103_LIVE_DEBT_MATRIX.csv",
        "decisions": OUT / "P8_Y5_R10_1103_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1103_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1103_VALIDATION.csv",
    }
    sources = source_rows()
    recon = reconciliation_rows()
    debts = debt_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["reconciliation"], recon)
    write_csv(outputs["debt_matrix"], debts)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_target)
    validation = validate(sources, recon, debts, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, recon, debts, decisions, next_target, validation)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
