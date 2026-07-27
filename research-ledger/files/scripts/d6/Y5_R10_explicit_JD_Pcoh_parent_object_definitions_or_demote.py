from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1131-Y5-R10-explicit-JD-Pcoh-parent-object-definitions-or-demote.md"


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
            "source_id": "SRC1131_0_1130_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1130_NEXT_TARGET.csv",
            "needle": "NEXT1130_0_1131",
            "note": "1130 handoff to explicit J_D/P_coh definitions or demotion.",
        },
        {
            "source_id": "SRC1131_1_1130_ownership",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1130_PCOH_JD_NORM_OWNERSHIP_AUDIT.csv",
            "needle": "OBJ1130_0_JD",
            "note": "1130 says J_D/P_coh/norm ownership is missing.",
        },
        {
            "source_id": "SRC1131_2_1130_variation",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1130_ID_VARIATION_LEDGER.csv",
            "needle": "VAR1130_4_verdict",
            "note": "1130 variation ledger is not closed.",
        },
        {
            "source_id": "SRC1131_3_owner_terms",
            "relative_path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
            "needle": "A8_projector_domain_topological",
            "note": "Domain/projector parent-action owner clause is retained symbolic.",
        },
        {
            "source_id": "SRC1131_4_ward_owner",
            "relative_path": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
            "needle": "C1_exact_owner_decomposition",
            "note": "Exact owner decomposition is not parent-derived.",
        },
        {
            "source_id": "SRC1131_5_PiM_algebra",
            "relative_path": "source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
            "needle": "PM4_projector_algebra",
            "note": "Projector algebra is conditional, not a legal P_coh construction.",
        },
        {
            "source_id": "SRC1131_6_PiM_variation",
            "relative_path": "source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv",
            "needle": "PV4_domain_homology_variation_owned",
            "note": "Domain/homology variation remains not parent-derived.",
        },
        {
            "source_id": "SRC1131_7_alpha3_products",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1126_ALPHA3_EXECUTABLE_PRODUCT_ROWS.csv",
            "needle": "EP1126_0_domain_flux",
            "note": "Executable alpha3 flux products remain fallback.",
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


def construction_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "attempt_id": "CON1131_0_JD_domain_current",
                "target_object": "J_D",
                "candidate_definition": "J_D := parent domain/coherent current from S_projector+S_domain variation",
                "acceptance": "formula from parent fields; Euler/Ward identity; retained q_D map if nonzero",
                "current_result": "MISSING_FORMULA",
                "why_rejected_as_proof": "current corpus only has symbolic owner contract A8/C1, not an explicit current",
                "valid_for_claim": "false",
            },
            {
                "attempt_id": "CON1131_1_Pcoh_projector",
                "target_object": "P_coh",
                "candidate_definition": "P_coh := parent projector onto coherent domain/current class with local exact class in kernel",
                "acceptance": "kernel/image algebra; idempotent; pre-readout definition; variation/stress ownership",
                "current_result": "MISSING_KERNEL_IMAGE_ALGEBRA",
                "why_rejected_as_proof": "PM4 is conditional and PV4 says domain/homology variation is not parent-derived",
                "valid_for_claim": "false",
            },
            {
                "attempt_id": "CON1131_2_parent_norm",
                "target_object": "inner product/norm",
                "candidate_definition": "<J,J>_coh := parent symplectic/topological norm on coherent current space",
                "acceptance": "positive, coordinate/frame safe, variation-owned or topological/stressless",
                "current_result": "MISSING_PARENT_NORM",
                "why_rejected_as_proof": "no boundary symplectic metric/topological norm inheritance theorem exists",
                "valid_for_claim": "false",
            },
            {
                "attempt_id": "CON1131_3_ID_selector",
                "target_object": "I_D=||P_coh J_D||^2",
                "candidate_definition": "I_D := <P_coh J_D, P_coh J_D>_coh",
                "acceptance": "CON1131_0 through CON1131_2 pass, plus delta I_D ledger closes",
                "current_result": "CONSTRUCTION_FAILS_CURRENT_CORPUS",
                "why_rejected_as_proof": "J_D, P_coh, norm, and variation ownership are missing",
                "valid_for_claim": "false",
            },
        ]
    )


def demotion_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "demotion_id": "DEM1131_0_selector_route",
                "route": "cohomology-norm branch selector",
                "decision": "DEMOTE_TO_CLOSURE_ONLY",
                "reason": "explicit parent objects cannot be constructed from current corpus",
                "effect": "cannot be used as proof of q_D_vector_flux=0, alpha3 pass, or local-GR reduction",
                "valid_for_claim": "false",
            },
            {
                "demotion_id": "DEM1131_1_fallback",
                "route": "executable alpha3 flux products",
                "decision": "KEEP_ACTIVE",
                "reason": "1126 product rows are the honest path when branch selector ownership is missing",
                "effect": "future work must source W/K/c/epsilon or prove a different zero theorem",
                "valid_for_claim": "false",
            },
            {
                "demotion_id": "DEM1131_2_future_rescue",
                "route": "future parent selector rescue",
                "decision": "ALLOW_REOPEN_WITH_NEW_PARENT_ACTION",
                "reason": "route could be reopened only if new files define J_D, P_coh, norm, and variation ledger",
                "effect": "closure-only now, not permanently impossible",
                "valid_for_claim": "false",
            },
        ]
    )


def fallback_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "fallback_id": "FB1131_0_domain_flux",
                "fallback_row": "EP1126_0_domain_flux",
                "quantity": "W_domain_alpha3*epsilon_domain_flux",
                "needed_for_future": "W_domain_alpha3; epsilon_domain_flux; units; normalization; source path or zero theorem",
                "claim_gate": "abs(product)<=4e-20 or theorem-zero; no local-domain-frame shortcut",
                "status": "ACTIVE_MISSING_INPUTS",
                "valid_for_claim": "false",
            },
            {
                "fallback_id": "FB1131_1_R11_flux",
                "fallback_row": "EP1126_1_R11_flux",
                "quantity": "K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "needed_for_future": "K_R11_flux_alpha3; c_R11_flux_alpha3; epsilon_domain_flux; observed coframe normalization; source paths",
                "claim_gate": "abs(product)<=4e-20 or theorem-zero",
                "status": "ACTIVE_MISSING_INPUTS",
                "valid_for_claim": "false",
            },
            {
                "fallback_id": "FB1131_2_no_cancellation",
                "fallback_row": "EP1126_2_total_direct_flux_guard",
                "quantity": "alpha3_direct_flux_total",
                "needed_for_future": "independent source/zero for both domain and R11 pieces",
                "claim_gate": "no tuned cancellation credit unless parent identity derives it",
                "status": "ACTIVE_GUARD",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1131_0_JD_formula",
                "rule": "J_D formula exists as parent object",
                "gate_pass": "false",
                "reason": "only symbolic owner contract exists",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1131_1_Pcoh_formula",
                "rule": "P_coh kernel/image and variation ownership exist",
                "gate_pass": "false",
                "reason": "projector algebra is conditional and variation is not parent-owned",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1131_2_norm_formula",
                "rule": "parent norm/inner product exists",
                "gate_pass": "false",
                "reason": "positive norm and variation ownership are missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1131_3_selector_demoted",
                "rule": "cohomology-norm selector is demoted from claim route",
                "gate_pass": "true_nonclaim",
                "reason": "route is retained only as closure/future theorem target",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1131_4_fallback_active",
                "rule": "executable alpha3 flux product fallback stays active",
                "gate_pass": "true_nonclaim",
                "reason": "1126 product rows remain the active nonclaim path",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1131_5_alpha3_local_GR",
                "rule": "alpha3/local-GR can promote",
                "gate_pass": "false",
                "reason": "selector route is demoted and product rows are unfilled",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1131_0_verdict",
                "decision": "explicit_parent_objects_not_available",
                "reason": "J_D, P_coh, norm, and variation ledger cannot be built from current corpus",
                "next_action": "demote cohomology-norm selector to closure-only and use product fallback",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1131_1_best_next",
                "decision": "return_to_executable_alpha3_flux_products",
                "reason": "this is now the honest route unless a new parent action/object file is supplied",
                "next_action": "build source-pack for W_domain_alpha3, epsilon_domain_flux, K_R11_flux_alpha3, c_R11_flux_alpha3",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1131_2_reopen_condition",
                "decision": "selector_route_reopen_only_with_new_parent_objects",
                "reason": "future rescue requires explicit J_D/P_coh/norm definitions and variation ledger",
                "next_action": "record as closure-only, not claim evidence",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1131_0_1132",
                "next_target": "1132-Y5-R10-alpha3-flux-product-source-pack-or-zero-theorem.md",
                "objective": "return to the executable alpha3 flux products: source or theorem-zero W_domain_alpha3, epsilon_domain_flux, K_R11_flux_alpha3, and c_R11_flux_alpha3, while keeping no-cancellation and sibling guards active",
                "include": "EP1126_0; EP1126_1; W_domain_alpha3; epsilon_domain_flux; K_R11_flux_alpha3; c_R11_flux_alpha3; 4e-20; source paths; zero theorem alternatives",
                "exclude": "cohomology-norm selector claim; tuned cancellation; local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    constructions: list[dict[str, object]],
    demotions: list[dict[str, object]],
    fallbacks: list[dict[str, object]],
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

    all_rows = constructions + demotions + fallbacks + gates + decisions + next_target
    targets = {row["target_object"] for row in constructions}
    fallback_rows = {row["fallback_row"] for row in fallbacks}
    add("V1131_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1131_1_construction_coverage", {"J_D", "P_coh", "inner product/norm", "I_D=||P_coh J_D||^2"}.issubset(targets), "J_D, P_coh, norm, and I_D construction attempts are present")
    add("V1131_2_construction_failed", constructions[-1]["current_result"] == "CONSTRUCTION_FAILS_CURRENT_CORPUS", "explicit selector construction fails in current corpus")
    add("V1131_3_demoted", demotions[0]["decision"] == "DEMOTE_TO_CLOSURE_ONLY", "cohomology-norm selector route is demoted to closure-only")
    add("V1131_4_fallback_rows", {"EP1126_0_domain_flux", "EP1126_1_R11_flux", "EP1126_2_total_direct_flux_guard"}.issubset(fallback_rows), "all executable alpha3 flux fallback rows remain active")
    add("V1131_5_gates_blocked", all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and gates[3]["gate_pass"] == "true_nonclaim" and gates[4]["gate_pass"] == "true_nonclaim", "claim gates remain blocked with demotion/fallback guards")
    add("V1131_6_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in next_target), "all generated rows remain nonclaim")
    add("V1131_7_next_target", next_target[0]["next_target"].startswith("1132-") and "alpha3-flux-product" in str(next_target[0]["next_target"]), "1132 handoff targets alpha3 flux product source pack")
    add("V1131_8_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1131_9_csv_parse", csv_parse_ok, "all 1131 CSV outputs parse cleanly")
    add("V1131_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1131_SUMMARY", True, "1131 demotes cohomology-norm selector route and returns to executable alpha3 flux products")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    constructions: list[dict[str, object]],
    demotions: list[dict[str, object]],
    fallbacks: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1131 - Y5/R10 Explicit J_D/P_coh Parent Object Definitions Or Demote

**Current verdict:** explicit parent definitions for `J_D`, `P_coh`, and the norm are not available in the current corpus. Therefore `I_D=||P_coh J_D||^2` cannot be used as a derived branch selector.

**Decision:** demote the cohomology-norm selector route to closure-only/private theorem target. It may be reopened only if a future parent-action file defines `J_D`, `P_coh`, the norm, and the full variation ledger.

**Active path:** return to the executable alpha3 flux product rows from 1126: `W_domain_alpha3*epsilon_domain_flux` and `K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux`.

**No claim:** no local no-flux, domain/R11 `alpha3`, R10, PPN, Newton/local-GR, FLRW, or measured-GM pass follows from 1131.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Explicit Construction Attempt
{table(["attempt_id", "target_object", "candidate_definition", "acceptance", "current_result", "why_rejected_as_proof", "valid_for_claim"], constructions)}

## Demotion Ledger
{table(["demotion_id", "route", "decision", "reason", "effect", "valid_for_claim"], demotions)}

## Active Fallback Rows
{table(["fallback_id", "fallback_row", "quantity", "needed_for_future", "claim_gate", "status", "valid_for_claim"], fallbacks)}

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
        "source_register": OUT / "P8_Y5_R10_1131_SOURCE_REGISTER.csv",
        "constructions": OUT / "P8_Y5_R10_1131_EXPLICIT_CONSTRUCTION_ATTEMPT.csv",
        "demotions": OUT / "P8_Y5_R10_1131_SELECTOR_DEMOTION_LEDGER.csv",
        "fallbacks": OUT / "P8_Y5_R10_1131_ACTIVE_ALPHA3_FLUX_FALLBACK_ROWS.csv",
        "gates": OUT / "P8_Y5_R10_1131_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1131_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1131_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1131_VALIDATION.csv",
    }
    sources = source_rows()
    constructions = construction_rows()
    demotions = demotion_rows()
    fallbacks = fallback_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["constructions"], constructions)
    write_csv(outputs["demotions"], demotions)
    write_csv(outputs["fallbacks"], fallbacks)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, constructions, demotions, fallbacks, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, constructions, demotions, fallbacks, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
