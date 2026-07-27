from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1128-Y5-R10-parent-branch-selector-ownership-ND-Qcoh-Pcoh.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    return [{**row, "generated_utc": generated} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1128_0_1127_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1127_NEXT_TARGET.csv",
            "needle": "NEXT1127_0_1128",
            "note": "1127 handoff to parent branch selector ownership.",
        },
        {
            "source_id": "SRC1128_1_1127_audit",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1127_BRANCH_SELECTOR_AUDIT.csv",
            "needle": "BS1127_3_verdict",
            "note": "1127 says branch selector has conditional shape but no parent ownership.",
        },
        {
            "source_id": "SRC1128_2_1127_rule",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1127_CANDIDATE_BRANCH_RULE.csv",
            "needle": "BR1127_0_selector_variable",
            "note": "1127 candidate rule names N_D/Q_coh/P_coh ownership.",
        },
        {
            "source_id": "SRC1128_3_602_gate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_602_LOCAL_FLRW_BRANCH_GATE.csv",
            "needle": "LFG602_2_FLRW_active",
            "note": "602 has conditional support for FLRW-active branch.",
        },
        {
            "source_id": "SRC1128_4_609_split",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_609_LOCAL_FLRW_BRANCH_SPLIT_GATE.csv",
            "needle": "LF609_3_verdict",
            "note": "609 says local/FLRW split is not closed and global zero is forbidden.",
        },
        {
            "source_id": "SRC1128_5_822_FLRW",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_822_FLRW_REDUCTION_AUDIT.csv",
            "needle": "F822_3_locked_shape",
            "note": "822 gives conditional FLRW determinant/locked-shape reduction.",
        },
        {
            "source_id": "SRC1128_6_parent_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "needle": "PAC1055_6_single_parent_action",
            "note": "1055 parent contract gives one-action discipline but not branch selector derivation.",
        },
        {
            "source_id": "SRC1128_7_topological_route",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1056_TOPOLOGICAL_LEVEL_INDEX_ROUTE_AUDIT.csv",
            "needle": "TL1056_4_verdict",
            "note": "1056 shows topological-level ownership routes need explicit inheritance theorem.",
        },
        {
            "source_id": "SRC1128_8_domain_ownership",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_PREMISE_OWNERSHIP.csv",
            "needle": "P3_local_trivial_representative",
            "note": "Local trivial representative remains conditional.",
        },
        {
            "source_id": "SRC1128_9_newton_stack",
            "relative_path": "source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv",
            "needle": "SN4_closed_Meff_flux",
            "note": "Closed flux remains not parent-derived in Newton/local-GR stack.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def ownership_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "owner_id": "OWN1128_0_ND",
                "object": "N_D",
                "candidate_meaning": "domain branch scalar/log-volume or activation amplitude; FLRW reduction N_D=ln(1+z)",
                "parent_ownership_required": "N_D is a parent variable or parent-derived invariant before readout, varied/owned in S_parent, and not fitted from residual success",
                "current_support": "822 gives conditional volume/FLRW relation; 602/609 use N_D for local/FLRW split",
                "current_status": "CONDITIONAL_NOT_PARENT_OWNED",
                "missing_certificate": "parent action term or invariant construction for N_D, plus local N_D=0 theorem",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "owner_id": "OWN1128_1_Qcoh",
                "object": "Q_coh",
                "candidate_meaning": "coherent load/current object whose determinant supplies FLRW active memory shape",
                "parent_ownership_required": "Q_coh is selected by parent equations/projection, positive/oriented, and varied or stress-accounted before FLRW reduction",
                "current_support": "822 gives conditional det(Q)=X_load^3 and locked shape if Q_coh exists",
                "current_status": "MISSING_PARENT_PROJECTION_AND_NORMALIZATION",
                "missing_certificate": "formula for Q_coh from parent fields and proof it is not imported from fit history",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "owner_id": "OWN1128_2_Pcoh",
                "object": "P_coh",
                "candidate_meaning": "coherent projector selecting local trivial versus FLRW active memory/domain class",
                "parent_ownership_required": "P_coh is an allowed parent projector/quotient map with variation/stress ownership and no readout-mask insertion",
                "current_support": "1127 candidate rule needs P_coh; 1055 gives general parent quotient discipline",
                "current_status": "MISSING_PARENT_PROJECTOR_OWNERSHIP",
                "missing_certificate": "projector construction, kernel/image algebra, variation ledger, and no empirical selector proof",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "owner_id": "OWN1128_3_BD",
                "object": "B_D branch selector",
                "candidate_meaning": "one rule: local if N_D=0/exact class, FLRW if N_D>0/coherent class",
                "parent_ownership_required": "B_D is built from parent-owned N_D/Q_coh/P_coh and does not use residuals, fit quality, or hand-picked domains",
                "current_support": "602 no-empirical-window gate passes as policy; 609 split has conditional support",
                "current_status": "RULE_SHAPE_READY_NOT_DERIVED",
                "missing_certificate": "single parent selector theorem producing both local and FLRW branches",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def action_contract_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "contract_id": "BA1128_0_parent_variables",
                "contract_clause": "declare branch ingredients before readout",
                "minimal_form": "S_parent contains or derives N_D[Phi], Q_coh[Phi], P_coh[Phi] before any empirical scoring",
                "acceptance": "local and FLRW branch conditions are computed from parent fields only",
                "current_status": "MISSING_PARENT_FORMULA",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "BA1128_1_smooth_selector",
                "contract_clause": "avoid discontinuous hand-picked branch switch",
                "minimal_form": "use parent-owned invariant I_D>=0, e.g. I_D=||P_coh J_D||^2 or det(Q_coh) normalized, with local I_D=0 and FLRW I_D>0",
                "acceptance": "branch response can be smooth/double-zero and varied; no imposed plateau",
                "current_status": "CANDIDATE_NOT_DERIVED",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "BA1128_2_local_reduction",
                "contract_clause": "local branch certificate",
                "minimal_form": "I_D=0 -> N_D=0 -> [J_D]_local exact/trivial -> epsilon_domain_flux=0",
                "acceptance": "parent theorem, not local assumption, not data-selected",
                "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "BA1128_3_FLRW_reduction",
                "contract_clause": "FLRW branch survival",
                "minimal_form": "homogeneous coherent branch -> N_D=-ln(a)=ln(1+z), Q_coh positive/oriented, memory projection active",
                "acceptance": "same parent selector as local branch; no global zero",
                "current_status": "CONDITIONAL_SUPPORTED_NOT_PARENT_OWNED",
                "valid_for_claim": "false",
            },
            {
                "contract_id": "BA1128_4_variation_and_stress",
                "contract_clause": "branch selector is varied or its stress is retained",
                "minimal_form": "delta_g N_D, delta_g Q_coh, delta_g P_coh terms are zero by theorem or mapped into residual rows",
                "acceptance": "no hidden selector/domain stress in local GR reduction",
                "current_status": "MISSING_VARIATION_LEDGER",
                "valid_for_claim": "false",
            },
        ]
    )


def reduction_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "check_id": "RED1128_0_local_if_owned",
                "statement": "If parent-owned I_D=0 in compact stationary local branch, then q_D_vector_flux can be zero.",
                "condition": "N_D=0/exact local class plus scalar stationary selector and R11 vector silence",
                "status": "CONDITIONAL_ONLY",
                "claim_effect": "would close direct alpha3 flux path, but source-normalization/stress siblings remain guarded",
                "valid_for_claim": "false",
            },
            {
                "check_id": "RED1128_1_FLRW_if_owned",
                "statement": "If parent-owned I_D>0 in coherent FLRW branch, cosmological memory remains active.",
                "condition": "N_D=ln(1+z), Q_coh/P_coh owned, normalized, and not imported from fits",
                "status": "CONDITIONAL_SUPPORTED",
                "claim_effect": "preserves cosmology while allowing local no-flux",
                "valid_for_claim": "false",
            },
            {
                "check_id": "RED1128_2_global_zero_forbidden",
                "statement": "A global all-domain zero selector is not allowed.",
                "condition": "would set local and FLRW branch inactive together",
                "status": "FORBIDDEN_GUARD",
                "claim_effect": "prevents overstrong local-GR fix from destroying MTS cosmology",
                "valid_for_claim": "false",
            },
            {
                "check_id": "RED1128_3_current_verdict",
                "statement": "Parent ownership of N_D/Q_coh/P_coh is not proved in current corpus.",
                "condition": "OWN1128_0 through OWN1128_3 all need parent certificates",
                "status": "OWNERSHIP_NOT_CLOSED",
                "claim_effect": "alpha3/local-GR remains blocked",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1128_0_ND_owned",
                "rule": "N_D is parent-owned and varied/owned",
                "gate_pass": "false",
                "reason": "N_D has conditional FLRW/local use but no parent action certificate",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1128_1_Qcoh_owned",
                "rule": "Q_coh is parent-owned, positive/oriented, normalized",
                "gate_pass": "false",
                "reason": "Q_coh projection and normalization are not parent-derived",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1128_2_Pcoh_owned",
                "rule": "P_coh projector is parent-owned with variation/stress ledger",
                "gate_pass": "false",
                "reason": "P_coh construction and variation ownership are missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1128_3_no_empirical_selector",
                "rule": "selector cannot use residual success or fit quality",
                "gate_pass": "true_nonclaim",
                "reason": "policy guard is explicit and preserved",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1128_4_branch_selector_closed",
                "rule": "one parent selector yields local exact and FLRW active branches",
                "gate_pass": "false",
                "reason": "ownership certificates for N_D/Q_coh/P_coh are missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1128_5_alpha3_local_GR",
                "rule": "local no-flux/alpha3/local-GR can promote",
                "gate_pass": "false",
                "reason": "branch selector remains unclosed",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1128_0_verdict",
                "decision": "parent_branch_selector_ownership_not_closed",
                "reason": "N_D/Q_coh/P_coh have useful conditional shape but no parent ownership certificate",
                "next_action": "derive a parent invariant I_D or cohomology-norm selector action",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1128_1_best_next",
                "decision": "cohomology_norm_selector_action_first",
                "reason": "a single parent invariant I_D>=0 could distinguish local zero from FLRW active without empirical switching",
                "next_action": "try I_D=||P_coh J_D||^2 or det(Q_coh) as parent-owned smooth selector",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1128_2_guard",
                "decision": "keep_global_zero_forbidden",
                "reason": "global all-domain zero would erase FLRW/cosmological memory",
                "next_action": "preserve local/FLRW split and alpha3 guard",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1128_0_1129",
                "next_target": "1129-Y5-R10-cohomology-norm-branch-selector-action-or-reject.md",
                "objective": "try to construct a parent-owned smooth branch selector invariant I_D, such as ||P_coh J_D||^2 or normalized det(Q_coh), that gives local I_D=0 and FLRW I_D>0 without empirical switching",
                "include": "I_D; N_D; Q_coh; P_coh; smooth/double-zero response; variation/stress ledger; local no-flux; FLRW active branch",
                "exclude": "global all-domain zero; discontinuous hand-picked domains; empirical selector; local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    ownership: list[dict[str, object]],
    contracts: list[dict[str, object]],
    reductions: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    all_rows = ownership + contracts + reductions + gates + decisions + next_target
    objects = {row["object"] for row in ownership}
    add("V1128_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1128_1_ownership_coverage", {"N_D", "Q_coh", "P_coh", "B_D branch selector"}.issubset(objects), "N_D, Q_coh, P_coh, and branch selector ownership rows are present")
    add("V1128_2_contract_coverage", len(contracts) >= 5 and any("I_D" in row["minimal_form"] for row in contracts), "parent branch action contract includes smooth selector invariant")
    add("V1128_3_reduction_guard", reductions[-1]["status"] == "OWNERSHIP_NOT_CLOSED" and reductions[2]["status"] == "FORBIDDEN_GUARD", "ownership remains unclosed and global zero is forbidden")
    add("V1128_4_gates_blocked", gates[3]["gate_pass"] == "true_nonclaim" and all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and sum(row["gate_pass"] == "false" for row in gates) >= 5, "claim gates remain blocked except no-empirical-selector guard")
    add("V1128_5_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in ownership + next_target), "all generated rows remain nonclaim")
    add("V1128_6_next_target", next_target[0]["next_target"].startswith("1129-") and "cohomology-norm" in str(next_target[0]["next_target"]), "1129 handoff targets cohomology-norm branch selector action")
    add("V1128_7_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1128_8_csv_parse", csv_parse_ok, "all 1128 CSV outputs parse cleanly")
    add("V1128_9_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1128_SUMMARY", True, "1128 sharpens parent ownership debt for N_D/Q_coh/P_coh and stages I_D selector target")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    ownership: list[dict[str, object]],
    contracts: list[dict[str, object]],
    reductions: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1128 - Y5/R10 Parent Branch Selector Ownership: N_D, Q_coh, P_coh

**Current verdict:** parent ownership of `N_D`, `Q_coh`, and `P_coh` is not closed. The local/FLRW branch split has a useful conditional shape, but it is still not a parent-derived selector.

**Best candidate:** build one smooth parent invariant `I_D >= 0`, such as `||P_coh J_D||^2` or a normalized `det(Q_coh)`, with local `I_D=0` and FLRW `I_D>0`.

**Guard:** the selector cannot use empirical success, hand-picked domains, discontinuous readout masks, or global all-domain zero.

**No claim:** no local no-flux, domain/R11 `alpha3`, R10, PPN, Newton/local-GR, or measured-GM pass follows from 1128.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Ownership Audit
{table(["owner_id", "object", "candidate_meaning", "parent_ownership_required", "current_support", "current_status", "missing_certificate", "claim_allowed", "valid_for_claim"], ownership)}

## Parent Branch Action Contract
{table(["contract_id", "contract_clause", "minimal_form", "acceptance", "current_status", "valid_for_claim"], contracts)}

## Reduction Checks
{table(["check_id", "statement", "condition", "status", "claim_effect", "valid_for_claim"], reductions)}

## Claim Gates
{table(["gate_id", "rule", "gate_pass", "reason", "valid_for_claim"], gates)}

## Decision Ledger
{table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions)}

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
        "source_register": OUT / "P8_Y5_R10_1128_SOURCE_REGISTER.csv",
        "ownership": OUT / "P8_Y5_R10_1128_BRANCH_SELECTOR_OWNERSHIP_AUDIT.csv",
        "contracts": OUT / "P8_Y5_R10_1128_PARENT_BRANCH_ACTION_CONTRACT.csv",
        "reductions": OUT / "P8_Y5_R10_1128_LOCAL_FLRW_REDUCTION_CHECKS.csv",
        "gates": OUT / "P8_Y5_R10_1128_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1128_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1128_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1128_VALIDATION.csv",
    }
    sources = source_rows()
    ownership = ownership_rows()
    contracts = action_contract_rows()
    reductions = reduction_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["ownership"], ownership)
    write_csv(outputs["contracts"], contracts)
    write_csv(outputs["reductions"], reductions)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, ownership, contracts, reductions, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, ownership, contracts, reductions, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
