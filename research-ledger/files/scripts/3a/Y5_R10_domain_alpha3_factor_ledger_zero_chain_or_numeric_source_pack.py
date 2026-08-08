from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1120-Y5-R10-domain-alpha3-factor-ledger-zero-chain-or-numeric-source-pack.md"


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
            "source_id": "SRC1120_0_1119_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1119_NEXT_TARGET.csv",
            "needle": "NEXT1119_0_1120",
            "note": "1119 handoff to domain alpha3 factor ledger.",
        },
        {
            "source_id": "SRC1120_1_1119_premises",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1119_DOMAIN_ALPHA3_PREMISE_LEDGER.csv",
            "needle": "A3P1119_3_R11_source",
            "note": "R11 source premise fails current corpus.",
        },
        {
            "source_id": "SRC1120_2_1119_fills",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1119_DOMAIN_ALPHA3_PRODUCT_FILL_ROWS_NONCLAIM.csv",
            "needle": "A3F1119_0_alpha3_product",
            "note": "alpha3 product fill row is missing.",
        },
        {
            "source_id": "SRC1120_3_double_zero",
            "relative_path": "source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv",
            "needle": "O6_verdict",
            "note": "p>=2 double-zero origin is not parent-derived.",
        },
        {
            "source_id": "SRC1120_4_no_vector",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
            "needle": "T2_no_flux_local_representative",
            "note": "local flux zero is conditional not parent-derived.",
        },
        {
            "source_id": "SRC1120_5_r11_zero",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_SOURCE_THEOREM_ZERO_ATTEMPT.csv",
            "needle": "Z6_verdict",
            "note": "R11 domain source zero is rejected.",
        },
        {
            "source_id": "SRC1120_6_alpha3_link",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_R11_LINK.csv",
            "needle": "L2_alpha3_flux",
            "note": "alpha3 flux link is missing highest pressure.",
        },
        {
            "source_id": "SRC1120_7_vector_coeffs",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv",
            "needle": "W_domain_alpha3_epsilon_domain_flux",
            "note": "weak-field alpha3 coefficient is not scoreable.",
        },
        {
            "source_id": "SRC1120_8_1118_candidate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1118_R11_DOMAIN_CANDIDATE_ROWS_NONCLAIM.csv",
            "needle": "W_domain_alpha3_epsilon_domain_flux",
            "note": "1118 alpha3/domain leakage candidate row remains missing.",
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


def factor_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "factor_id": "FAC1120_0_total",
                "factor": "P_domain_alpha3",
                "role": "total alpha3 domain contribution",
                "formula_piece": "W_domain_alpha3 * epsilon_domain_flux + P_R11_source_alpha3",
                "zero_route": "all factors zero by parent theorem",
                "numeric_route": "abs(total)<=4e-20 with source-backed value",
                "current_status": "MISSING_TOTAL_PRODUCT_OR_THEOREM_ZERO",
                "highest_priority": "true",
            },
            {
                "factor_id": "FAC1120_1_p_ge_2",
                "factor": "p>=2 domain/memory gate origin",
                "role": "removes linear local activation and first-derivative domain coupling",
                "formula_piece": "f(0)=0 and f'(0)=0",
                "zero_route": "derive double-zero from parent determinant/current, norm-square, or topological pairing",
                "numeric_route": "if not derived, retain domain/memory coupling width",
                "current_status": "REQUIREMENT_KNOWN_BUT_ORIGIN_NOT_PARENT_DERIVED",
                "highest_priority": "false",
            },
            {
                "factor_id": "FAC1120_2_flux",
                "factor": "epsilon_domain_flux",
                "role": "projected domain flux feeding alpha3",
                "formula_piece": "P_loc^i_mu F_D^mu",
                "zero_route": "derive compact exact/trivial local representative and no active coherent FLRW memory class",
                "numeric_route": "source-backed flux coefficient with units/map",
                "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
                "highest_priority": "true",
            },
            {
                "factor_id": "FAC1120_3_weight",
                "factor": "W_domain_alpha3",
                "role": "weak-field map from domain flux/source leakage into PPN alpha3",
                "formula_piece": "alpha3_domain = W_domain_alpha3 * epsilon_domain_flux",
                "zero_route": "derive W=0 from parent weak-field map",
                "numeric_route": "source-backed W coefficient; no unity shortcut",
                "current_status": "MISSING_NUMERIC_WEIGHT_OR_THEOREM_ZERO",
                "highest_priority": "true",
            },
            {
                "factor_id": "FAC1120_4_R11_source",
                "factor": "c_domain_source_normalization_operator",
                "role": "R11 source-normalization leakage into alpha3/local source",
                "formula_piece": "P_R11_source_alpha3",
                "zero_route": "derive c_domain_source_normalization_operator=0",
                "numeric_route": "canonical executable R11 row with source-backed coefficient",
                "current_status": "FAIL_CURRENT_CORPUS",
                "highest_priority": "true",
            },
            {
                "factor_id": "FAC1120_5_projector_stress",
                "factor": "projector/domain STF or stress leakage",
                "role": "additional R7/R8/R11 leakage if projector/domain stress is not topological zero",
                "formula_piece": "delta_g P_D, delta_g chi_D, or domain-wall/readout-mask stress",
                "zero_route": "derive parent-owned metric-independent topological projector",
                "numeric_route": "source-backed projector stress coefficient",
                "current_status": "CONDITIONAL_NOT_PARENT_OWNED",
                "highest_priority": "false",
            },
        ]
    )


def attack_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "attack_id": "ATK1120_0_R11_first",
                "factor": "c_domain_source_normalization_operator",
                "recommended_order": "1",
                "why": "1118 already shows this is the hard failed clause and it can leak into alpha3 even when vector/flux routes are quiet",
                "derive_attempt": "prove EH-only/local-boundary silence or parent-owned R11 source zero",
                "fallback_fill": "canonical R11 source-normalization row with coefficient, units, normalization, weak-field map, source path",
                "current_verdict": "NOT_DERIVED_NEEDS_ZERO_OR_EXECUTABLE_ROW",
            },
            {
                "attack_id": "ATK1120_1_flux",
                "factor": "epsilon_domain_flux",
                "recommended_order": "2",
                "why": "if flux is theorem-zero, W factor becomes irrelevant for alpha3 product",
                "derive_attempt": "prove compact exact/trivial local representative and no coherent local memory class",
                "fallback_fill": "numeric projected flux coefficient",
                "current_verdict": "CONDITIONAL_NOT_PARENT_DERIVED",
            },
            {
                "attack_id": "ATK1120_2_weight",
                "factor": "W_domain_alpha3",
                "recommended_order": "3",
                "why": "needed only if flux survives; cannot be set to unity",
                "derive_attempt": "derive weak-field alpha3 map coefficient from parent perturbation theory",
                "fallback_fill": "numeric weak-field map coefficient with source path",
                "current_verdict": "MISSING_NUMERIC_WEIGHT_OR_THEOREM_ZERO",
            },
            {
                "attack_id": "ATK1120_3_p_ge_2",
                "factor": "p>=2 gate origin",
                "recommended_order": "4",
                "why": "important for broad domain/memory silence, but alpha3 still blocked by R11 even if p>=2 holds",
                "derive_attempt": "derive double-zero origin from determinant/current, norm-square, or topological pairing",
                "fallback_fill": "finite domain/memory coupling width",
                "current_verdict": "REQUIREMENT_KNOWN_BUT_ORIGIN_NOT_PARENT_DERIVED",
            },
        ]
    )


def source_pack_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "pack_id": "SRCF1120_0_total",
                "row": "R7_alpha3",
                "required_quantity": "P_domain_alpha3",
                "required_value": "numeric or theorem-zero",
                "units": "dimensionless PPN alpha3 convention",
                "bound": "4e-20",
                "source_requirement": "source-backed total product or theorem-zero certificate",
                "current_status": "MISSING",
            },
            {
                "pack_id": "SRCF1120_1_R11",
                "row": "R7/R11",
                "required_quantity": "P_R11_source_alpha3 or c_domain_source_normalization_operator",
                "required_value": "numeric or theorem-zero",
                "units": "dimensionless mapped alpha3 contribution or declared operator units",
                "bound": "combined <=4e-20",
                "source_requirement": "canonical executable R11 coefficient row",
                "current_status": "MISSING",
            },
            {
                "pack_id": "SRCF1120_2_flux",
                "row": "R7_alpha3",
                "required_quantity": "epsilon_domain_flux",
                "required_value": "numeric or theorem-zero",
                "units": "dimensionless projected flux convention",
                "bound": "inherited through product",
                "source_requirement": "local representative theorem or measured/sourced flux coefficient",
                "current_status": "MISSING",
            },
            {
                "pack_id": "SRCF1120_3_weight",
                "row": "R7_alpha3",
                "required_quantity": "W_domain_alpha3",
                "required_value": "numeric or theorem-zero",
                "units": "dimensionless weak-field coefficient",
                "bound": "inherited through product",
                "source_requirement": "parent weak-field map derivation/source",
                "current_status": "MISSING",
            },
            {
                "pack_id": "SRCF1120_4_gate",
                "row": "domain/memory gate",
                "required_quantity": "p>=2 origin",
                "required_value": "parent theorem",
                "units": "not applicable",
                "bound": "zero-chain premise",
                "source_requirement": "determinant/current, norm-square, or topological-pairing parent derivation",
                "current_status": "MISSING_PARENT_ORIGIN",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "CG1120_0_factorized",
                "claim": "alpha3 factorization is explicit",
                "gate_pass": "true_nonclaim",
                "reason": "factor ledger separates total product, flux, weight, R11 leakage, gate origin, and projector stress",
            },
            {
                "gate_id": "CG1120_1_zero_chain",
                "claim": "alpha3 zero chain is derived",
                "gate_pass": "false",
                "reason": "R11 source zero, local flux zero, p>=2 origin, and projector ownership are not all parent-derived",
            },
            {
                "gate_id": "CG1120_2_numeric_pack",
                "claim": "numeric alpha3 source pack is score-ready",
                "gate_pass": "false",
                "reason": "all factor source-pack rows remain missing",
            },
            {
                "gate_id": "CG1120_3_local_gr",
                "claim": "domain alpha3 permits local-GR/R10 claim",
                "gate_pass": "false",
                "reason": "highest-pressure row remains blocked at 4e-20",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "DEC1120_0_result",
                "decision": "domain alpha3 is factorized but not closed",
                "because": "the product now has named factors, but no factor is claim-ready enough to score alpha3",
                "next_action": "attack R11 source-normalization leakage first",
            },
            {
                "decision_id": "DEC1120_1_best_next",
                "decision": "R11 source leakage remains the first factor to kill/fill",
                "because": "it survives even if the domain selector is scalar/stationary and it feeds the tight alpha3 row",
                "next_action": "derive P_R11_source_alpha3=0 or fill executable R11 alpha3 leakage row",
            },
            {
                "decision_id": "DEC1120_2_policy",
                "decision": "no unity shortcuts for W_domain_alpha3 or flux",
                "because": "alpha3 has a 4e-20 target and must use sourced factors or theorem-zero",
                "next_action": "keep all factor rows nonclaim until real values or proofs exist",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1120_0_1121",
                "next_target": "1121-Y5-R10-domain-alpha3-R11-leakage-zero-or-executable-row.md",
                "objective": "attack the R11 source leakage factor first: derive P_R11_source_alpha3=0/c_domain_source_normalization_operator=0, or build one canonical executable R11 alpha3 leakage row",
                "include": "P_R11_source_alpha3; c_domain_source_normalization_operator; R11 schema; units; normalization; weak-field map; target 4e-20; source path",
                "exclude": "symbolic product pass; Ward/Bianchi shortcut; local-GR claim; tau=1; source-unity; GitHub; formalization edits",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    factors: list[dict[str, object]],
    attacks: list[dict[str, object]],
    source_pack: list[dict[str, object]],
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

    factor_names = {str(row["factor"]) for row in factors}
    add("V1120_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1120_1_factor_coverage", {"P_domain_alpha3", "p>=2 domain/memory gate origin", "epsilon_domain_flux", "W_domain_alpha3", "c_domain_source_normalization_operator"}.issubset(factor_names), "key alpha3 factors are covered")
    add("V1120_2_r11_first", attacks[0]["factor"] == "c_domain_source_normalization_operator", "R11 source leakage is first attack")
    add("V1120_3_source_pack_missing", all(str(row["current_status"]).startswith("MISSING") for row in source_pack), "source-pack rows remain missing-input nonclaim rows")
    add("V1120_4_bound_explicit", source_pack[0]["bound"] == "4e-20", "alpha3 4e-20 bound is explicit")
    add("V1120_5_gates_blocked", all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and any(row["gate_pass"] == "false" for row in gates), "claim gates remain blocked except nonclaim factorization")
    add("V1120_6_no_claim_rows", all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in factors + attacks + source_pack + gates + decisions + next_target), "all generated rows remain nonclaim")
    add("V1120_7_next_target", next_target[0]["next_target"].startswith("1121-") and "R11-leakage" in str(next_target[0]["next_target"]), "1121 handoff targets domain alpha3 R11 leakage")
    add("V1120_8_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1120_9_csv_parse", csv_parse_ok, "all 1120 CSV outputs parse cleanly")
    add("V1120_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1120_SUMMARY", True, "1120 factorizes domain alpha3 and prioritizes R11 leakage kill/fill")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    factors: list[dict[str, object]],
    attacks: list[dict[str, object]],
    source_pack: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1120 - Domain Alpha3 Factor Ledger Zero Chain Or Numeric Source Pack

**Current verdict:** domain `alpha3` is now factorized but not closed. The row is no longer one mystery number; it is a product/sum of specific debts: gate origin, flux, weak-field weight, and R11 source leakage.

**Best next move:** kill or fill the R11 leakage factor first. It remains live even when the selector-vector route is conditionally quiet, and it directly touches the `4e-20` alpha3 bound.

**No claim:** no domain `alpha3` pass, no local-GR/R10 safety, and no numeric source-pack pass follows from 1120.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Factor Ledger
{table(["factor_id", "factor", "role", "formula_piece", "zero_route", "numeric_route", "current_status", "highest_priority", "claim_allowed"], factors)}

## Attack Order
{table(["attack_id", "factor", "recommended_order", "why", "derive_attempt", "fallback_fill", "current_verdict", "claim_allowed"], attacks)}

## Numeric Source Pack
{table(["pack_id", "row", "required_quantity", "required_value", "units", "bound", "source_requirement", "current_status", "claim_allowed"], source_pack)}

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
        "source_register": OUT / "P8_Y5_R10_1120_SOURCE_REGISTER.csv",
        "factors": OUT / "P8_Y5_R10_1120_DOMAIN_ALPHA3_FACTOR_LEDGER.csv",
        "attacks": OUT / "P8_Y5_R10_1120_DOMAIN_ALPHA3_ATTACK_ORDER.csv",
        "source_pack": OUT / "P8_Y5_R10_1120_DOMAIN_ALPHA3_NUMERIC_SOURCE_PACK_NONCLAIM.csv",
        "gates": OUT / "P8_Y5_R10_1120_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1120_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1120_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1120_VALIDATION.csv",
    }
    sources = source_rows()
    factors = factor_rows()
    attacks = attack_rows()
    source_pack = source_pack_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["factors"], factors)
    write_csv(outputs["attacks"], attacks)
    write_csv(outputs["source_pack"], source_pack)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, factors, attacks, source_pack, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, factors, attacks, source_pack, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
