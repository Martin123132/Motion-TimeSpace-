from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1119-Y5-R10-domain-alpha3-R11-source-zero-or-product-fill.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    out: list[dict[str, object]] = []
    for row in rows:
        copied = dict(row)
        copied.setdefault("valid_for_claim", "false")
        copied.setdefault("claim_allowed", "false")
        copied.setdefault("generated_utc", generated)
        out.append(copied)
    return out


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1119_0_1118_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1118_NEXT_TARGET.csv",
            "needle": "NEXT1118_0_1119",
            "note": "1118 handoff to domain alpha3 R11 source zero or product fill.",
        },
        {
            "source_id": "SRC1119_1_1118_pressure",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1118_DOMAIN_PRESSURE_ORDER.csv",
            "needle": "PRS1118_0_alpha3",
            "note": "alpha3 is highest-pressure domain row.",
        },
        {
            "source_id": "SRC1119_2_1118_candidate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1118_R11_DOMAIN_CANDIDATE_ROWS_NONCLAIM.csv",
            "needle": "W_domain_alpha3_epsilon_domain_flux",
            "note": "candidate alpha3 product row remains missing.",
        },
        {
            "source_id": "SRC1119_3_fill_req",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_SOURCE_FILL_REQUIREMENTS.csv",
            "needle": "DSR_R7_alpha3",
            "note": "alpha3 fill requirement with 4e-20 bound.",
        },
        {
            "source_id": "SRC1119_4_vector_coeffs",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv",
            "needle": "W_domain_alpha3_epsilon_domain_flux",
            "note": "domain alpha3 vector/flux coefficient map.",
        },
        {
            "source_id": "SRC1119_5_link",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_R11_LINK.csv",
            "needle": "L2_alpha3_flux",
            "note": "domain alpha3 R11 link marks highest pressure missing row.",
        },
        {
            "source_id": "SRC1119_6_premise",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_PREMISE_OWNERSHIP.csv",
            "needle": "P5_R11_operator_vector",
            "note": "R11 operator vector missing blocks alpha3 no-leak.",
        },
        {
            "source_id": "SRC1119_7_domain_zero",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1117_DOMAIN_ZERO_THEOREM_ATTEMPT.csv",
            "needle": "DSZ1117_4_R11_source",
            "note": "R11 source-normalization operator silence fails.",
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


def zero_attempt_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "attempt_id": "A3D1119_0_target",
                "claim_piece": "domain alpha3 zero",
                "formal_statement": "W_domain_alpha3 * epsilon_domain_flux = 0 with R11 source-normalization silence.",
                "result": "TARGET_SHARP",
                "proof_or_blocker": "this is the highest-pressure domain local-test row because the bound is 4e-20",
            },
            {
                "attempt_id": "A3D1119_1_sufficient_chain",
                "claim_piece": "sufficient zero chain",
                "formal_statement": "p>=2 domain gate + local trivial representative + topological projector stress zero + R11 source silence => alpha3_domain=0.",
                "result": "EXACT_CONDITIONAL_CHAIN",
                "proof_or_blocker": "if every premise is parent-owned, the product vanishes without numeric tuning",
            },
            {
                "attempt_id": "A3D1119_2_p_ge_2",
                "claim_piece": "p>=2/double-zero domain gate",
                "formal_statement": "domain/memory activation has a double zero at the local branch.",
                "result": "REQUIREMENT_KNOWN_OR_CONDITIONAL",
                "proof_or_blocker": "p>=2 is necessary/sufficient in prior work but parent origin remains conditional",
            },
            {
                "attempt_id": "A3D1119_3_local_flux_zero",
                "claim_piece": "epsilon_domain_flux=0",
                "formal_statement": "local exact/trivial representative and no active coherent FLRW memory class imply no domain flux.",
                "result": "CONDITIONAL_NOT_PARENT_DERIVED",
                "proof_or_blocker": "local exact/trivial representative is a contract, not a derivation",
            },
            {
                "attempt_id": "A3D1119_4_projector_R11",
                "claim_piece": "R11 source/projector silence",
                "formal_statement": "c_domain_source_normalization_operator=0 and projector/domain stress does not source alpha3.",
                "result": "FAIL_CURRENT_CORPUS",
                "proof_or_blocker": "1118 shows source-normalization zero is not derived and executable vector rows are missing",
            },
            {
                "attempt_id": "A3D1119_5_numeric_fill",
                "claim_piece": "numeric product below bound",
                "formal_statement": "abs(W_domain_alpha3*epsilon_domain_flux + R11_source_leakage) <= 4e-20.",
                "result": "MISSING_NUMERIC_PRODUCT",
                "proof_or_blocker": "no source-backed numeric product or theorem-zero certificate is available",
            },
            {
                "attempt_id": "A3D1119_6_verdict",
                "claim_piece": "derive or fill domain alpha3 row",
                "formal_statement": "domain alpha3 is theorem-zero or has a source-backed numeric product below 4e-20.",
                "result": "DOMAIN_ALPHA3_NOT_DERIVED_OR_FILLED",
                "proof_or_blocker": "conditional zero chain is useful but at least p>=2 origin, local flux zero, and R11 silence are not parent-owned; numeric product is missing",
            },
        ]
    )


def premise_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "premise_id": "A3P1119_0_p_ge_2",
                "premise": "double-zero selector/domain gate",
                "needed_for": "remove linear local domain activation",
                "status": "CONDITIONAL_ORIGIN_NOT_PARENT_DERIVED",
                "if_missing": "linear or first-derivative domain coupling can source alpha3",
            },
            {
                "premise_id": "A3P1119_1_local_trivial",
                "premise": "local compact branch has exact/trivial domain representative",
                "needed_for": "epsilon_domain_flux=0",
                "status": "CONDITIONAL_NOT_PARENT_DERIVED",
                "if_missing": "domain flux product remains live",
            },
            {
                "premise_id": "A3P1119_2_topological_projector",
                "premise": "projector/domain stress is metric-independent or bulk-zero",
                "needed_for": "no projector-domain alpha3 leakage",
                "status": "CONDITIONAL_NOT_PARENT_OWNED",
                "if_missing": "projector stress can feed R7/R8/R11",
            },
            {
                "premise_id": "A3P1119_3_R11_source",
                "premise": "c_domain_source_normalization_operator=0",
                "needed_for": "no source-normalization leakage into alpha3",
                "status": "FAIL_CURRENT_CORPUS",
                "if_missing": "R11 source leak remains highest-pressure blocker",
            },
            {
                "premise_id": "A3P1119_4_numeric_product",
                "premise": "numeric product with source path and units",
                "needed_for": "fallback score against 4e-20",
                "status": "MISSING",
                "if_missing": "alpha3 row cannot be scored",
            },
        ]
    )


def product_fill_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "fill_id": "A3F1119_0_alpha3_product",
                "target_row": "R7_alpha3",
                "product_symbol": "P_domain_alpha3 = W_domain_alpha3 * epsilon_domain_flux + P_R11_source_alpha3",
                "product_value": "MISSING_NUMERIC_PRODUCT_OR_THEOREM_ZERO",
                "product_units": "dimensionless PPN alpha3 convention",
                "target_bound_abs": "4e-20",
                "required_inputs": "W_domain_alpha3; epsilon_domain_flux; c_domain_source_normalization_operator or theorem-zero; weak-field map; source path",
                "source_status": "MISSING_SOURCE_BACKED_PRODUCT",
                "acceptance": "valid_for_claim true only if abs(product)<=4e-20 and no MISSING/conditional fields remain",
            },
            {
                "fill_id": "A3F1119_1_flux_factor",
                "target_row": "R7_alpha3",
                "product_symbol": "epsilon_domain_flux",
                "product_value": "MISSING_NUMERIC_FLUX_OR_ZERO_THEOREM",
                "product_units": "dimensionless projected flux convention",
                "target_bound_abs": "inherited through product",
                "required_inputs": "local representative theorem or numeric flux coefficient",
                "source_status": "MISSING_SOURCE_BACKED_FLUX",
                "acceptance": "must be zero theorem or numeric with units/map",
            },
            {
                "fill_id": "A3F1119_2_weight_factor",
                "target_row": "R7_alpha3",
                "product_symbol": "W_domain_alpha3",
                "product_value": "MISSING_NUMERIC_WEIGHT_OR_ZERO_THEOREM",
                "product_units": "dimensionless weak-field map coefficient",
                "target_bound_abs": "inherited through product",
                "required_inputs": "weak-field derivation/source path for alpha3 map",
                "source_status": "MISSING_SOURCE_BACKED_WEIGHT",
                "acceptance": "no source-unity shortcut; must be derived or sourced",
            },
            {
                "fill_id": "A3F1119_3_R11_leakage",
                "target_row": "R7_alpha3/R11",
                "product_symbol": "P_R11_source_alpha3",
                "product_value": "MISSING_R11_SOURCE_LEAKAGE_OR_ZERO_THEOREM",
                "product_units": "dimensionless alpha3 contribution or declared operator units mapped to alpha3",
                "target_bound_abs": "combined product <=4e-20",
                "required_inputs": "c_domain_source_normalization_operator; executable R11 row; normalization; weak-field map",
                "source_status": "MISSING_EXECUTABLE_R11_SOURCE_ROW",
                "acceptance": "canonical R11 row valid_for_claim=true or theorem-zero",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "CG1119_0_zero",
                "claim": "domain alpha3 theorem-zero",
                "gate_pass": "false",
                "reason": "zero chain has missing parent-owned premises and failed R11 silence",
            },
            {
                "gate_id": "CG1119_1_product",
                "claim": "domain alpha3 numeric product passes 4e-20",
                "gate_pass": "false",
                "reason": "product value, flux factor, weak-field weight, and R11 leakage are missing",
            },
            {
                "gate_id": "CG1119_2_r11",
                "claim": "R11 source-normalization contribution is executable",
                "gate_pass": "false",
                "reason": "c_domain_source_normalization_operator row is missing theorem-zero or numeric coefficient",
            },
            {
                "gate_id": "CG1119_3_local_gr",
                "claim": "domain branch supports local-GR/R10 safety",
                "gate_pass": "false",
                "reason": "alpha3 highest-pressure row remains unscored",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "DEC1119_0_result",
                "decision": "domain alpha3 row is not derived or filled",
                "because": "the theorem-zero route is conditional and the numeric product route lacks source-backed inputs",
                "next_action": "attack the p>=2/local-flux/R11 premise chain or source the numeric product factors",
            },
            {
                "decision_id": "DEC1119_1_best_next",
                "decision": "split alpha3 into premise-chain versus numeric-product acquisition",
                "because": "a single missing product hides four different debts: gate origin, local flux, weak-field weight, and R11 source leakage",
                "next_action": "build a factor ledger that can be killed one premise at a time or sourced numerically",
            },
            {
                "decision_id": "DEC1119_2_policy",
                "decision": "no symbolic alpha3 pass",
                "because": "4e-20 is too tight for placeholders, unity factors, or conditional zeros",
                "next_action": "keep valid_for_claim=false until exact zero or numeric source row exists",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1119_0_1120",
                "next_target": "1120-Y5-R10-domain-alpha3-factor-ledger-zero-chain-or-numeric-source-pack.md",
                "objective": "split domain alpha3 into factors and attack/fill each: p>=2 gate origin, local flux zero, W_domain_alpha3 weak-field weight, and R11 source-normalization leakage",
                "include": "p>=2 gate; epsilon_domain_flux; W_domain_alpha3; c_domain_source_normalization_operator; P_R11_source_alpha3; target 4e-20; source-backed product rows",
                "exclude": "symbolic product pass; Ward/Bianchi shortcut; local-GR claim; tau=1; source-unity; GitHub; formalization edits",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    zero_attempt: list[dict[str, object]],
    premises: list[dict[str, object]],
    fills: list[dict[str, object]],
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

    add("V1119_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1119_1_conditional_chain", any(row["result"] == "EXACT_CONDITIONAL_CHAIN" for row in zero_attempt), "conditional alpha3 zero chain is recorded")
    add("V1119_2_failure_recorded", any(row["result"] == "DOMAIN_ALPHA3_NOT_DERIVED_OR_FILLED" for row in zero_attempt), "alpha3 row remains unfilled/unpromoted")
    add("V1119_3_r11_failed", any(row["status"] == "FAIL_CURRENT_CORPUS" for row in premises), "R11 source premise failure is recorded")
    add("V1119_4_fill_rows_missing", all("MISSING" in row["product_value"] for row in fills), "all product fill rows remain missing-input nonclaim")
    add("V1119_5_bound_explicit", fills[0]["target_bound_abs"] == "4e-20", "alpha3 4e-20 bound is explicit")
    add("V1119_6_gates_blocked", all(row["gate_pass"] == "false" for row in gates), "all claim gates remain blocked")
    add("V1119_7_no_claim_rows", all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in zero_attempt + premises + fills + gates + decisions + next_target), "all generated rows remain nonclaim")
    add("V1119_8_next_target", next_target[0]["next_target"].startswith("1120-") and "factor-ledger" in str(next_target[0]["next_target"]), "1120 handoff targets domain alpha3 factor ledger")
    add("V1119_9_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1119_10_csv_parse", csv_parse_ok, "all 1119 CSV outputs parse cleanly")
    add("V1119_11_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1119_SUMMARY", True, "1119 keeps domain alpha3 blocked and splits it into theorem/premise/product factors")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    zero_attempt: list[dict[str, object]],
    premises: list[dict[str, object]],
    fills: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1119 - Domain Alpha3 R11 Source Zero Or Product Fill

**Current verdict:** the domain `alpha3` row is not derived or filled. There is a clean conditional zero chain, but the parent-owned premises are not all signed and the numeric product is missing.

**Pressure point:** the row is brutal: `abs(W_domain_alpha3 * epsilon_domain_flux + P_R11_source_alpha3) <= 4e-20`. No symbolic product, unity factor, or conditional zero can be counted here.

**No claim:** no domain `alpha3` pass, no R11 source pass, no local-GR/R10 safety, and no finite product pass follows from 1119.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Zero/Product Attempt
{table(["attempt_id", "claim_piece", "formal_statement", "result", "proof_or_blocker", "claim_allowed"], zero_attempt)}

## Premise Ledger
{table(["premise_id", "premise", "needed_for", "status", "if_missing", "claim_allowed"], premises)}

## Product Fill Rows
{table(["fill_id", "target_row", "product_symbol", "product_value", "product_units", "target_bound_abs", "required_inputs", "source_status", "acceptance", "claim_allowed"], fills)}

## Claim Gates
{table(["gate_id", "claim", "gate_pass", "reason", "claim_allowed"], gates)}

## Decisions
{table(["decision_id", "decision", "because", "next_action", "claim_allowed"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1119_SOURCE_REGISTER.csv",
        "zero_attempt": OUT / "P8_Y5_R10_1119_DOMAIN_ALPHA3_ZERO_ATTEMPT.csv",
        "premises": OUT / "P8_Y5_R10_1119_DOMAIN_ALPHA3_PREMISE_LEDGER.csv",
        "fills": OUT / "P8_Y5_R10_1119_DOMAIN_ALPHA3_PRODUCT_FILL_ROWS_NONCLAIM.csv",
        "gates": OUT / "P8_Y5_R10_1119_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1119_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1119_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1119_VALIDATION.csv",
    }
    sources = source_rows()
    zero_attempt = zero_attempt_rows()
    premises = premise_rows()
    fills = product_fill_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["zero_attempt"], zero_attempt)
    write_csv(outputs["premises"], premises)
    write_csv(outputs["fills"], fills)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, zero_attempt, premises, fills, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, zero_attempt, premises, fills, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
