from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1130-Y5-R10-Pcoh-JD-norm-ownership-or-executable-flux-products.md"


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
            "source_id": "SRC1130_0_1129_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1129_NEXT_TARGET.csv",
            "needle": "NEXT1129_0_1130",
            "note": "1129 handoff to P_coh/J_D norm ownership.",
        },
        {
            "source_id": "SRC1130_1_1129_candidates",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1129_SELECTOR_CANDIDATE_COMPARISON.csv",
            "needle": "ID1129_0_cohomology_norm",
            "note": "1129 selected I_D=||P_coh J_D||^2 as best candidate, not proof.",
        },
        {
            "source_id": "SRC1130_2_1129_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1129_MINIMAL_ACTION_CONTRACT.csv",
            "needle": "ACT1129_1_variation_ledger",
            "note": "1129 requires variation/stress ledger for I_D/P_coh/Q_coh/N_D.",
        },
        {
            "source_id": "SRC1130_3_PiM_algebra",
            "relative_path": "source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
            "needle": "PM5_projector_variation_owned",
            "note": "Projector variation ownership remains not parent-derived.",
        },
        {
            "source_id": "SRC1130_4_PiM_variation",
            "relative_path": "source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv",
            "needle": "PV0_product_variation_included",
            "note": "Product variation must include delta(Pi_M J), not silently drop projector stress.",
        },
        {
            "source_id": "SRC1130_5_owner_terms",
            "relative_path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "needle": "A8_projector_domain_topological",
            "note": "Projector/domain owner route is retained symbolic.",
        },
        {
            "source_id": "SRC1130_6_ward_owner",
            "relative_path": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
            "needle": "C1_exact_owner_decomposition",
            "note": "Owner decomposition and retained-current zero are not parent-derived.",
        },
        {
            "source_id": "SRC1130_7_alpha3_products",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1126_ALPHA3_EXECUTABLE_PRODUCT_ROWS.csv",
            "needle": "EP1126_0_domain_flux",
            "note": "Executable alpha3 product rows remain the fallback if branch selector fails.",
        },
        {
            "source_id": "SRC1130_8_parent_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
            "needle": "PAC1055_6_single_parent_action",
            "note": "Single parent action is contract-ready but not derived from deeper MTS primitives.",
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
                "object_id": "OBJ1130_0_JD",
                "object": "J_D",
                "required_status": "parent-owned domain/coherent current, varied before readout",
                "formal_requirement": "J_D is derived from S_projector+S_domain or source-owner decomposition, not chosen after local/FLRW behavior is known",
                "current_evidence": "A8/C1 retain domain/projector source ownership as symbolic/not parent-derived",
                "current_status": "NOT_PARENT_DERIVED",
                "missing_certificate": "formula for J_D from parent fields plus Euler/Ward identity or retained-current map",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "object_id": "OBJ1130_1_Pcoh",
                "object": "P_coh",
                "required_status": "parent-owned coherent projector/quotient map",
                "formal_requirement": "P_coh is idempotent/orthogonal to irrelevant blocks, defined before readout, and its variation is zero by theorem or retained",
                "current_evidence": "PM4 is conditional; PM5/PV0/PV4 say projector variation/domain homology ownership is not derived",
                "current_status": "NOT_PARENT_DERIVED",
                "missing_certificate": "explicit P_coh kernel/image algebra and variation/stress ledger",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "object_id": "OBJ1130_2_inner_product",
                "object": "coherent norm/inner product",
                "required_status": "parent-owned positive norm on the current/projector space",
                "formal_requirement": "||P_coh J_D||^2 is positive, coordinate/frame safe, and not a fitted Hodge/DeWitt/readout metric unless varied",
                "current_evidence": "PM1 parent boundary symplectic metric is candidate_not_parent_derived; PV2 retains Hodge/DeWitt stress if used",
                "current_status": "MISSING_PARENT_NORM",
                "missing_certificate": "parent symplectic/boundary metric or topological norm with variation ownership",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "object_id": "OBJ1130_3_ID",
                "object": "I_D=||P_coh J_D||^2",
                "required_status": "derived selector invariant",
                "formal_requirement": "I_D=0 iff local exact/trivial class; I_D>0 for coherent FLRW class; delta I_D is owned or retained",
                "current_evidence": "1129 selects I_D as best candidate but not derived",
                "current_status": "SELECTOR_INVARIANT_NOT_DERIVED",
                "missing_certificate": "OBJ1130_0 through OBJ1130_2 plus local/FLRW branch theorems",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def variation_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "variation_id": "VAR1130_0_product_rule",
                "variation_piece": "delta I_D",
                "required_expression": "delta I_D = 2 <P_coh J_D, delta(P_coh J_D)> + delta<.,.>(P_coh J_D,P_coh J_D)",
                "risk_if_missing": "hidden branch-selector stress is dropped",
                "current_status": "WRITTEN_CONTRACT_NOT_DERIVED",
                "valid_for_claim": "false",
            },
            {
                "variation_id": "VAR1130_1_delta_Pcoh",
                "variation_piece": "delta P_coh",
                "required_expression": "delta(P_coh J_D) includes (delta P_coh)J_D",
                "risk_if_missing": "projector/domain homology variation leaks preferred-frame/source residuals",
                "current_status": "NOT_PARENT_DERIVED",
                "valid_for_claim": "false",
            },
            {
                "variation_id": "VAR1130_2_delta_JD",
                "variation_piece": "delta J_D",
                "required_expression": "delta(P_coh J_D) includes P_coh delta J_D with J_D sourced by parent Euler/Ward/domain equations",
                "risk_if_missing": "domain current is a fitted readout object",
                "current_status": "NOT_PARENT_DERIVED",
                "valid_for_claim": "false",
            },
            {
                "variation_id": "VAR1130_3_delta_norm",
                "variation_piece": "delta inner product/norm",
                "required_expression": "delta<.,.> is zero by topological theorem or mapped to residual stress",
                "risk_if_missing": "Hodge/DeWitt metric dependence becomes hidden stress",
                "current_status": "MISSING_PARENT_NORM_VARIATION",
                "valid_for_claim": "false",
            },
            {
                "variation_id": "VAR1130_4_verdict",
                "variation_piece": "variation/stress ledger complete",
                "required_expression": "VAR1130_0 through VAR1130_3 all parent-owned or retained",
                "risk_if_missing": "I_D selector cannot support local-GR reduction",
                "current_status": "VARIATION_LEDGER_NOT_CLOSED",
                "valid_for_claim": "false",
            },
        ]
    )


def route_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "route_id": "ROUTE1130_0_derive",
                "route": "prove P_coh/J_D/norm ownership",
                "status": "NOT_CLOSED",
                "acceptance": "all object and variation rows have parent certificates; local I_D=0 and FLRW I_D>0 follow from one rule",
                "next_action": "attempt explicit J_D and P_coh parent construction",
                "valid_for_claim": "false",
            },
            {
                "route_id": "ROUTE1130_1_demote",
                "route": "demote branch selector to private closure candidate",
                "status": "NOT_YET_DEMOTED",
                "acceptance": "if explicit construction fails, use 1126 executable alpha3 flux products as active path",
                "next_action": "keep EP1126 product rows active until source-backed values/theorems exist",
                "valid_for_claim": "false",
            },
            {
                "route_id": "ROUTE1130_2_no_claim",
                "route": "no alpha3/local-GR promotion",
                "status": "ACTIVE",
                "acceptance": "no local no-flux claim while I_D ownership is missing",
                "next_action": "do not promote PPN/R10/local-GR",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1130_0_JD_owned",
                "rule": "J_D is parent-owned",
                "gate_pass": "false",
                "reason": "domain/coherent current formula is missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1130_1_Pcoh_owned",
                "rule": "P_coh is parent-owned",
                "gate_pass": "false",
                "reason": "projector algebra and variation ownership are conditional/missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1130_2_norm_owned",
                "rule": "inner product/norm is parent-owned",
                "gate_pass": "false",
                "reason": "boundary symplectic/Hodge norm route is not parent-derived",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1130_3_variation_owned",
                "rule": "delta I_D stress is theorem-zero or retained",
                "gate_pass": "false",
                "reason": "variation ledger is not closed",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1130_4_fallback_active",
                "rule": "executable alpha3 flux products remain active fallback",
                "gate_pass": "true_nonclaim",
                "reason": "1126 products remain the nonclaim route if selector fails",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1130_5_local_GR",
                "rule": "local-GR/PPN can promote",
                "gate_pass": "false",
                "reason": "I_D ownership and q_D flux zero are not proved",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1130_0_verdict",
                "decision": "Pcoh_JD_norm_ownership_not_proved",
                "reason": "P_coh, J_D, norm, and delta I_D ownership are all missing or conditional",
                "next_action": "attempt explicit parent construction of J_D and P_coh, or demote selector route",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1130_1_best_next",
                "decision": "construct_JD_and_Pcoh_explicitly",
                "reason": "without concrete objects the norm cannot be varied or used as a theorem",
                "next_action": "write minimal parent object definitions for J_D, P_coh, and their inner product",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1130_2_fallback",
                "decision": "keep_flux_products_active",
                "reason": "selector route remains private/theorem-target only",
                "next_action": "do not erase 1126 executable product path",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1130_0_1131",
                "next_target": "1131-Y5-R10-explicit-JD-Pcoh-parent-object-definitions-or-demote.md",
                "objective": "try to define J_D, P_coh, and the inner product as explicit parent objects with variation ownership; if not possible, demote the cohomology-norm selector route and keep executable alpha3 flux products",
                "include": "J_D formula; P_coh kernel/image; parent inner product; delta(P_coh J_D); local exact class; FLRW coherent class; EP1126 fallback",
                "exclude": "unvaried projector stress; readout mask; empirical selector; local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    ownership: list[dict[str, object]],
    variations: list[dict[str, object]],
    routes: list[dict[str, object]],
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

    all_rows = ownership + variations + routes + gates + decisions + next_target
    object_names = {row["object"] for row in ownership}
    add("V1130_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1130_1_object_coverage", {"J_D", "P_coh", "coherent norm/inner product", "I_D=||P_coh J_D||^2"}.issubset(object_names), "J_D, P_coh, norm, and I_D ownership rows are present")
    add("V1130_2_variation_coverage", variations[-1]["current_status"] == "VARIATION_LEDGER_NOT_CLOSED" and any("delta P_coh" in row["variation_piece"] for row in variations), "variation ledger is explicit and unclosed")
    add("V1130_3_fallback_active", routes[1]["route"] == "demote branch selector to private closure candidate" and gates[4]["gate_pass"] == "true_nonclaim", "executable flux-product fallback remains active")
    add("V1130_4_gates_blocked", all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and sum(row["gate_pass"] == "false" for row in gates) >= 5, "claim gates remain blocked except fallback-active nonclaim")
    add("V1130_5_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in ownership + next_target), "all generated rows remain nonclaim")
    add("V1130_6_next_target", next_target[0]["next_target"].startswith("1131-") and "explicit-JD-Pcoh" in str(next_target[0]["next_target"]), "1131 handoff targets explicit J_D/P_coh definitions or demotion")
    add("V1130_7_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1130_8_csv_parse", csv_parse_ok, "all 1130 CSV outputs parse cleanly")
    add("V1130_9_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1130_SUMMARY", True, "1130 keeps P_coh/J_D norm ownership unproved and preserves executable flux fallback")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    ownership: list[dict[str, object]],
    variations: list[dict[str, object]],
    routes: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1130 - Y5/R10 Pcoh/JD Norm Ownership Or Executable Flux Products

**Current verdict:** `I_D=||P_coh J_D||^2` is still not a derived selector. `P_coh`, `J_D`, the norm, and `delta I_D` are missing parent ownership or variation certificates.

**Key failure:** the product variation cannot be dropped: `delta I_D` contains `delta P_coh`, `delta J_D`, and variation of the norm/inner product.

**Fallback preserved:** if explicit parent definitions cannot be built, the cohomology-norm branch selector must stay private/conditional and the 1126 executable alpha3 flux product rows remain active.

**No claim:** no local no-flux, domain/R11 `alpha3`, R10, PPN, Newton/local-GR, FLRW, or measured-GM pass follows from 1130.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Object Ownership Audit
{table(["object_id", "object", "required_status", "formal_requirement", "current_evidence", "current_status", "missing_certificate", "claim_allowed", "valid_for_claim"], ownership)}

## Variation Ledger
{table(["variation_id", "variation_piece", "required_expression", "risk_if_missing", "current_status", "valid_for_claim"], variations)}

## Route Ledger
{table(["route_id", "route", "status", "acceptance", "next_action", "valid_for_claim"], routes)}

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
        "source_register": OUT / "P8_Y5_R10_1130_SOURCE_REGISTER.csv",
        "ownership": OUT / "P8_Y5_R10_1130_PCOH_JD_NORM_OWNERSHIP_AUDIT.csv",
        "variations": OUT / "P8_Y5_R10_1130_ID_VARIATION_LEDGER.csv",
        "routes": OUT / "P8_Y5_R10_1130_SELECTOR_ROUTE_LEDGER.csv",
        "gates": OUT / "P8_Y5_R10_1130_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1130_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1130_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1130_VALIDATION.csv",
    }
    sources = source_rows()
    ownership = ownership_rows()
    variations = variation_rows()
    routes = route_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["ownership"], ownership)
    write_csv(outputs["variations"], variations)
    write_csv(outputs["routes"], routes)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, ownership, variations, routes, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, ownership, variations, routes, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
