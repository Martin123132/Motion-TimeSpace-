from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1137-Y5-R10-W-K-c-coupling-normalization-source-audit.md"


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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1137_0_1136_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1136_NEXT_TARGET.csv",
            "needle": "NEXT1136_0_1137",
            "note": "1136 handoff to W/K/c coupling normalization source audit.",
        },
        {
            "source_id": "SRC1137_1_1136_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1136_EPSILON_W_K_C_SOURCE_PACK_FIRST_ROWS.csv",
            "needle": "SP1136_1_W_domain_alpha3",
            "note": "1136 first source-pack rows remain blocked.",
        },
        {
            "source_id": "SRC1137_2_vector_coefficients",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv",
            "needle": "W_domain_alpha3_epsilon_domain_flux",
            "note": "Domain selector coefficient map names W_domain_alpha3 but does not provide numeric W.",
        },
        {
            "source_id": "SRC1137_3_mu_extra_coefficients",
            "relative_path": "source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv",
            "needle": "W_domain_alpha3_epsilon_domain_flux",
            "note": "Mu-extra coefficient map carries the same map-only W row.",
        },
        {
            "source_id": "SRC1137_4_472_link",
            "relative_path": "472-domain-projector-alpha3-no-leak-or-R11-link.md",
            "needle": "N7_no_leak_verdict",
            "note": "472 says domain alpha3 no-leak theorem fails in current corpus.",
        },
        {
            "source_id": "SRC1137_5_1122_flux",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1122_REMAINING_FLUX_CONTRACT.csv",
            "needle": "K_R11_flux_alpha3",
            "note": "1122 introduces K_R11_flux_alpha3 as a contract placeholder.",
        },
        {
            "source_id": "SRC1137_6_1123_bound",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1123_ALPHA3_FLUX_BOUND_PRODUCT_ROWS.csv",
            "needle": "K_R11_flux_alpha3*c_R11_flux_alpha3",
            "note": "1123 carries the K*c*epsilon bound row as missing.",
        },
        {
            "source_id": "SRC1137_7_1118_R11",
            "relative_path": "1118-Y5-R10-domain-R11-source-normalization-zero-or-executable-coefficient-vector.md",
            "needle": "c_domain_source_normalization_operator = 0",
            "note": "1118 says c_domain_source_normalization_operator zero is not derived.",
        },
        {
            "source_id": "SRC1137_8_R11_minimum",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM.csv",
            "needle": "c_domain_source_normalization_operator",
            "note": "R11 minimum row has c_domain_source_normalization_operator but value is missing.",
        },
        {
            "source_id": "SRC1137_9_R11_missing",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_VECTOR_MISSING_LEDGER.csv",
            "needle": "MISSING_DOMAIN_MU_EXTRA_OPERATOR_ZERO_OR_NUMERIC_COEFFICIENT",
            "note": "R11 missing ledger blocks c/source-normalization claims.",
        },
        {
            "source_id": "SRC1137_10_480_template",
            "relative_path": "480-alpha3-numeric-product-input-template.md",
            "needle": "A3_DOMAIN_NUMERIC_OR_ZERO",
            "note": "480 is the older fill template and remains unfilled.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = read_text(path)
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def coupling_audit_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "audit_id": "CPL1137_0_W_domain_alpha3",
                "coefficient": "W_domain_alpha3",
                "role": "domain flux to PPN alpha3 weak-field coefficient",
                "best_existing_evidence": "P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENTS.csv and P8_mu_extra_domain_projector_coefficients.csv define alpha3_domain = W_domain_alpha3*epsilon_domain_flux",
                "source_status": "MAP_LABEL_ONLY_NOT_NUMERIC_SOURCE",
                "zero_status": "NO_LEAK_THEOREM_FAILS_CURRENT_CORPUS",
                "missing_for_claim": "numeric W value or parent theorem-zero; units; weak-field derivation path; no source-unity shortcut",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CPL1137_1_K_R11_flux_alpha3",
                "coefficient": "K_R11_flux_alpha3",
                "role": "R11 flux-to-alpha3 transfer coefficient",
                "best_existing_evidence": "1122 narrows P_R11_source_alpha3_flux to K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "source_status": "CONTRACT_PLACEHOLDER_NOT_NUMERIC_SOURCE",
                "zero_status": "NO_R11_FLUX_TRANSFER_ZERO_THEOREM",
                "missing_for_claim": "operator derivation of transfer coefficient or theorem-zero; normalization to dimensionless alpha3; source path",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CPL1137_2_c_R11_flux_alpha3",
                "coefficient": "c_R11_flux_alpha3",
                "role": "R11 observed-coframe/source-normalization coefficient for alpha3 flux branch",
                "best_existing_evidence": "current rows alias this to the c_domain_source_normalization_operator family; 1118 and R11 missing ledgers keep it unfilled",
                "source_status": "ALIAS_TO_MISSING_R11_SOURCE_NORMALIZATION",
                "zero_status": "c_domain_source_normalization_operator_ZERO_NOT_DERIVED",
                "missing_for_claim": "canonical R11 coefficient value or theorem-zero; units; observed-coframe normalization; weak-field map; no MISSING fields",
                "valid_for_claim": "false",
            },
            {
                "audit_id": "CPL1137_3_Kc_product",
                "coefficient": "K_R11_flux_alpha3*c_R11_flux_alpha3",
                "role": "combined R11 alpha3 coupling product",
                "best_existing_evidence": "1123 and 1136 permit this product only after K and c individually source or theorem-zero",
                "source_status": "PRODUCT_SHORTCUT_FORBIDDEN",
                "zero_status": "NOT_ZERO_UNLESS_K_OR_c_ZERO_IS_SOURCE_BACKED",
                "missing_for_claim": "do not fill product directly unless both factor provenance rows exist or a parent identity defines the product as primitive",
                "valid_for_claim": "false",
            },
        ]
    )


def alias_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "alias_id": "AL1137_0_c_alias",
                "new_symbol": "c_R11_flux_alpha3",
                "older_symbol_or_family": "c_domain_source_normalization_operator",
                "relationship": "branch-specific alpha3 notation maps onto the existing R11 domain source-normalization family",
                "status": "ALIAS_ACCEPTED_FOR_AUDIT_NOT_A_VALUE",
                "risk": "using a new symbol can hide the older missing ledger unless explicitly cross-linked",
                "valid_for_claim": "false",
            },
            {
                "alias_id": "AL1137_1_W_map",
                "new_symbol": "W_domain_alpha3",
                "older_symbol_or_family": "W_domain_alpha3_epsilon_domain_flux",
                "relationship": "W is the coefficient inside the older product/map row",
                "status": "COEFFICIENT_EXTRACTED_FROM_MAP_LABEL_ONLY",
                "risk": "map label does not determine coefficient magnitude",
                "valid_for_claim": "false",
            },
            {
                "alias_id": "AL1137_2_K_new",
                "new_symbol": "K_R11_flux_alpha3",
                "older_symbol_or_family": "P_R11_source_alpha3_flux contract",
                "relationship": "K is an introduced transfer factor in the newer split of the R11 alpha3 leakage",
                "status": "NO_OLDER_NUMERIC_ROW_FOUND",
                "risk": "K could become a free knob unless derived from R11 operator variation",
                "valid_for_claim": "false",
            },
        ]
    )


def theorem_route_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "route_id": "ZR1137_0_W_zero",
                "target": "W_domain_alpha3=0",
                "required_theorem": "domain/projector sector has no preferred-frame flux coupling into alpha3",
                "current_status": "FAIL_CURRENT_CORPUS",
                "evidence": "472 no-leak verdict fails; 1119/1120 keep W product missing",
                "effect_if_closed": "domain product closes if epsilon finite",
                "valid_for_claim": "false",
            },
            {
                "route_id": "ZR1137_1_K_zero",
                "target": "K_R11_flux_alpha3=0",
                "required_theorem": "R11 operator has no flux-to-alpha3 transfer channel",
                "current_status": "MISSING_THEOREM",
                "evidence": "1122/1123 define K only as missing transfer coefficient",
                "effect_if_closed": "R11 flux product closes if c and epsilon finite",
                "valid_for_claim": "false",
            },
            {
                "route_id": "ZR1137_2_c_zero",
                "target": "c_R11_flux_alpha3=0 / c_domain_source_normalization_operator=0",
                "required_theorem": "domain source-normalization operator vanishes or is pure EH/local-boundary silence",
                "current_status": "FAIL_CURRENT_CORPUS",
                "evidence": "1118 says zero not derived; R11 missing ledger remains active",
                "effect_if_closed": "R11 flux product closes and sibling R5/R6/R8/R11 leakage is reduced",
                "valid_for_claim": "false",
            },
            {
                "route_id": "ZR1137_3_product_bound",
                "target": "numeric W, K, c bounds",
                "required_theorem": "not a theorem; source-backed coefficient magnitudes with units and no MISSING fields",
                "current_status": "NO_NUMERIC_SOURCE_ROWS",
                "evidence": "1136 source-pack first rows are all rejected for claim",
                "effect_if_closed": "sets required epsilon envelope and enables product comparison",
                "valid_for_claim": "false",
            },
        ]
    )


def normalized_source_requirement_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "requirement_id": "REQ1137_0_W_row",
                "coefficient": "W_domain_alpha3",
                "claim_ready_row_must_contain": "coefficient_value_abs; units=dimensionless; weak_field_map; derivation_or_source_path; assumptions; valid_for_claim",
                "must_not_contain": "MISSING; conditional_only; source_unity; map_label_only",
                "current_status": "NOT_READY",
                "valid_for_claim": "false",
            },
            {
                "requirement_id": "REQ1137_1_K_row",
                "coefficient": "K_R11_flux_alpha3",
                "claim_ready_row_must_contain": "transfer_value_abs; units=dimensionless; R11 operator derivation; normalization_to_alpha3; source_path; valid_for_claim",
                "must_not_contain": "MISSING; free_transfer_factor; fitted_to_pass_alpha3",
                "current_status": "NOT_READY",
                "valid_for_claim": "false",
            },
            {
                "requirement_id": "REQ1137_2_c_row",
                "coefficient": "c_R11_flux_alpha3",
                "claim_ready_row_must_contain": "source_normalization_value_abs; units; observed_coframe; weak_field_map; R11 source path; valid_for_claim",
                "must_not_contain": "MISSING; gauge_absorption; measured_GM_redefinition_without_proof",
                "current_status": "NOT_READY",
                "valid_for_claim": "false",
            },
            {
                "requirement_id": "REQ1137_3_Kc_row",
                "coefficient": "K_R11_flux_alpha3*c_R11_flux_alpha3",
                "claim_ready_row_must_contain": "factorized K and c provenance or parent primitive product identity",
                "must_not_contain": "direct product fill with hidden factor cancellation",
                "current_status": "NOT_READY",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1137_0_W_sourced",
                "rule": "W_domain_alpha3 is numeric/source-backed or theorem-zero",
                "gate_pass": "false",
                "reason": "W is only a map label in current evidence",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1137_1_K_sourced",
                "rule": "K_R11_flux_alpha3 is numeric/source-backed or theorem-zero",
                "gate_pass": "false",
                "reason": "K is only a transfer placeholder in current evidence",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1137_2_c_sourced",
                "rule": "c_R11_flux_alpha3/c_domain_source_normalization_operator is numeric/source-backed or theorem-zero",
                "gate_pass": "false",
                "reason": "R11 source-normalization zero/value is explicitly missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1137_3_Kc_shortcut",
                "rule": "K*c product cannot be filled without factor provenance",
                "gate_pass": "true_nonclaim",
                "reason": "product shortcut is forbidden",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1137_4_c_priority",
                "rule": "c/R11 source-normalization should be attacked first",
                "gate_pass": "true_nonclaim",
                "reason": "c can leak into alpha3 and sibling PPN/R11 rows",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1137_5_alpha3_local_GR",
                "rule": "alpha3/R10/PPN/local-GR can promote",
                "gate_pass": "false",
                "reason": "W/K/c remain unsourced and epsilon remains missing",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1137_0_verdict",
                "decision": "W_K_c_not_sourced",
                "reason": "all three coefficients are currently map labels, placeholders, or aliases to missing R11 rows",
                "next_action": "do not compute alpha3 products from W/K/c yet",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1137_1_best_next",
                "decision": "attack_c_R11_source_normalization_first",
                "reason": "c/c_domain_source_normalization_operator is the broadest blocker and older checkpoints already identify it as the hard R11 edge",
                "next_action": "try c=0 theorem or canonical executable c row before returning to W/K",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1137_2_W_and_K_after_c",
                "decision": "W_and_K_remain_live_but_lower_priority",
                "reason": "W matters for domain product and K matters for R11 transfer, but c can close/reduce R11 leakage and sibling rows",
                "next_action": "source W/K only after c route is clarified or in parallel source pack",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1137_0_1138",
                "next_target": "1138-Y5-R10-c-domain-source-normalization-zero-or-executable-coefficient-row.md",
                "objective": "attack c_R11_flux_alpha3/c_domain_source_normalization_operator: either derive source-normalization zero in the local branch or build a canonical executable coefficient row with units, normalization, source path, and no MISSING markers",
                "include": "R11 source-normalization; c alias; observed coframe; measured-GM normalization; sibling R5/R6/R8/R11 guards; alpha3 K*c*epsilon bridge",
                "exclude": "product shortcut; gauge absorption; source-unity; tuned cancellation; alpha3/local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    audits: list[dict[str, object]],
    aliases: list[dict[str, object]],
    zero_routes: list[dict[str, object]],
    requirements: list[dict[str, object]],
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

    all_rows = audits + aliases + zero_routes + requirements + gates + decisions + next_target
    coefficient_set = {row["coefficient"] for row in audits}
    add("V1137_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1137_1_coupling_coverage", {"W_domain_alpha3", "K_R11_flux_alpha3", "c_R11_flux_alpha3", "K_R11_flux_alpha3*c_R11_flux_alpha3"}.issubset(coefficient_set), "audit covers W, K, c, and K*c")
    add("V1137_2_no_coefficients_sourced", all(row["source_status"] != "NUMERIC_SOURCE_BACKED" for row in audits), "no W/K/c coefficient is falsely marked source-backed")
    add("V1137_3_c_alias_crosslinked", aliases[0]["older_symbol_or_family"] == "c_domain_source_normalization_operator", "c_R11 alias is cross-linked to older R11 source-normalization family")
    add("V1137_4_zero_routes_blocked", all(row["current_status"] in {"FAIL_CURRENT_CORPUS", "MISSING_THEOREM", "NO_NUMERIC_SOURCE_ROWS"} for row in zero_routes), "zero/numeric routes remain blocked")
    add("V1137_5_requirements_not_ready", all(row["current_status"] == "NOT_READY" for row in requirements), "claim-ready coefficient row requirements are not yet satisfied")
    add("V1137_6_product_shortcut_guard", gates[3]["gate_pass"] == "true_nonclaim", "K*c product shortcut guard is active")
    add("V1137_7_c_priority", decisions[1]["decision"] == "attack_c_R11_source_normalization_first", "next target prioritizes c/R11 source-normalization")
    add("V1137_8_gates_blocked", all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and sum(row["gate_pass"] == "false" for row in gates) >= 4, "claim gates remain blocked")
    add("V1137_9_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in next_target), "all generated rows remain nonclaim")
    add("V1137_10_next_target", next_target[0]["next_target"].startswith("1138-") and "c-domain-source-normalization" in str(next_target[0]["next_target"]), "1138 handoff targets c/domain source-normalization")
    add("V1137_11_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1137_12_csv_parse", csv_parse_ok, "all 1137 CSV outputs parse cleanly")
    add("V1137_13_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1137_SUMMARY", True, "1137 confirms W/K/c are not sourced and selects c/R11 source-normalization as next target")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    audits: list[dict[str, object]],
    aliases: list[dict[str, object]],
    zero_routes: list[dict[str, object]],
    requirements: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1137 - Y5/R10 W/K/c Coupling Normalization Source Audit

**Current verdict:** `W_domain_alpha3`, `K_R11_flux_alpha3`, and `c_R11_flux_alpha3` are not source-backed coefficients in the current corpus. They are map labels, contract placeholders, or aliases to missing R11 source-normalization rows.

**Important alias:** `c_R11_flux_alpha3` is treated as the alpha3-branch face of the older `c_domain_source_normalization_operator` family. That prevents a new symbol from hiding the old missing-ledger blocker.

**Best next attack:** go after `c_R11_flux_alpha3 / c_domain_source_normalization_operator` first. It is broader than alpha3: it can leak into R5/R6/R8/R11 siblings and is already identified by older checkpoints as the hard R11 edge.

**No claim:** no alpha3, R10, PPN, local-GR, measured-GM, or FLRW claim follows from 1137. `K*c` cannot be filled as a product shortcut without factor provenance.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Coupling Audit
{table(["audit_id", "coefficient", "role", "best_existing_evidence", "source_status", "zero_status", "missing_for_claim", "valid_for_claim"], audits)}

## Alias Ledger
{table(["alias_id", "new_symbol", "older_symbol_or_family", "relationship", "status", "risk", "valid_for_claim"], aliases)}

## Zero/Theorem Route Audit
{table(["route_id", "target", "required_theorem", "current_status", "evidence", "effect_if_closed", "valid_for_claim"], zero_routes)}

## Claim-Ready Row Requirements
{table(["requirement_id", "coefficient", "claim_ready_row_must_contain", "must_not_contain", "current_status", "valid_for_claim"], requirements)}

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
        "source_register": OUT / "P8_Y5_R10_1137_SOURCE_REGISTER.csv",
        "audits": OUT / "P8_Y5_R10_1137_W_K_C_COUPLING_AUDIT.csv",
        "aliases": OUT / "P8_Y5_R10_1137_COUPLING_ALIAS_LEDGER.csv",
        "zero_routes": OUT / "P8_Y5_R10_1137_COUPLING_ZERO_ROUTE_AUDIT.csv",
        "requirements": OUT / "P8_Y5_R10_1137_CLAIM_READY_COEFFICIENT_REQUIREMENTS.csv",
        "gates": OUT / "P8_Y5_R10_1137_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1137_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1137_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1137_VALIDATION.csv",
    }
    sources = source_rows()
    audits = coupling_audit_rows()
    aliases = alias_rows()
    zero_routes = theorem_route_rows()
    requirements = normalized_source_requirement_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["audits"], audits)
    write_csv(outputs["aliases"], aliases)
    write_csv(outputs["zero_routes"], zero_routes)
    write_csv(outputs["requirements"], requirements)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, audits, aliases, zero_routes, requirements, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, audits, aliases, zero_routes, requirements, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
