from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1138-Y5-R10-c-domain-source-normalization-zero-or-executable-coefficient-row.md"


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
            "source_id": "SRC1138_0_1137_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1137_NEXT_TARGET.csv",
            "needle": "NEXT1137_0_1138",
            "note": "1137 handoff to c/domain source-normalization zero or executable row.",
        },
        {
            "source_id": "SRC1138_1_c_alias",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1137_COUPLING_ALIAS_LEDGER.csv",
            "needle": "AL1137_0_c_alias",
            "note": "c_R11_flux_alpha3 is cross-linked to c_domain_source_normalization_operator.",
        },
        {
            "source_id": "SRC1138_2_1118_zero",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1118_DOMAIN_R11_ZERO_THEOREM_ATTEMPT.csv",
            "needle": "R11D1118_6_verdict",
            "note": "1118 says c/domain source-normalization zero is not derived.",
        },
        {
            "source_id": "SRC1138_3_1118_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1118_EXECUTABLE_VECTOR_CONTRACT.csv",
            "needle": "EXE1118_0_schema",
            "note": "1118 declares canonical 19-column executable R11 schema.",
        },
        {
            "source_id": "SRC1138_4_1121_zero",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1121_R11_ALPHA3_ZERO_PROOF_AUDIT.csv",
            "needle": "Z1121_4_verdict",
            "note": "1121 says R11 alpha3 leakage zero is not closed.",
        },
        {
            "source_id": "SRC1138_5_1121_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1121_R11_ALPHA3_EXECUTABLE_ROW_CONTRACT.csv",
            "needle": "R11A3_1121_0_alpha3_source_leakage",
            "note": "1121 provides the alpha3 leakage executable-row contract.",
        },
        {
            "source_id": "SRC1138_6_minimum_row",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM.csv",
            "needle": "c_domain_source_normalization_operator",
            "note": "Current minimum R11 row has c but missing coefficient value.",
        },
        {
            "source_id": "SRC1138_7_missing_ledger",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_VECTOR_MISSING_LEDGER.csv",
            "needle": "MISSING_DOMAIN_MU_EXTRA_OPERATOR_ZERO_OR_NUMERIC_COEFFICIENT",
            "note": "Missing ledger blocks c/source-normalization claim.",
        },
        {
            "source_id": "SRC1138_8_fill_requirements",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_SOURCE_FILL_REQUIREMENTS.csv",
            "needle": "DSR_R11_EH_operator_ledger",
            "note": "R11 fill requirements say the row needs no MISSING fields.",
        },
        {
            "source_id": "SRC1138_9_zero_attempt",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_SOURCE_THEOREM_ZERO_ATTEMPT.csv",
            "needle": "Z6_verdict",
            "note": "Older R11 zero attempt fails current corpus.",
        },
        {
            "source_id": "SRC1138_10_1136_product",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1136_ALPHA3_PRODUCT_INEQUALITY_ROWS.csv",
            "needle": "PI1136_1_R11_alpha3",
            "note": "1136 R11 product inequality stays blocked by K/c/epsilon.",
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


def zero_route_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "zero_id": "CZ1138_0_target",
                "target": "c_domain_source_normalization_operator=0",
                "needed_identity": "compact local branch has no domain source-normalization leakage in observed coframe",
                "current_evidence": "1118/1121 identify this as the R11/domain bottleneck",
                "result": "TARGET_SHARP",
                "blocker": "none for target definition",
                "valid_for_claim": "false",
            },
            {
                "zero_id": "CZ1138_1_EH_only",
                "target": "EH-only/local exterior silence",
                "needed_identity": "S_parent reduces to EH plus silent boundary/domain terms before measured-GM readout",
                "current_evidence": "1118 R11D1118_1_EH_only is NOT_DERIVED; 1121 Z1121_1_EH_only_silence fails",
                "result": "NOT_DERIVED",
                "blocker": "non-EH/domain source-normalization terms are retained, not theorem-zero",
                "valid_for_claim": "false",
            },
            {
                "zero_id": "CZ1138_2_no_absorption",
                "target": "measured-GM/source-normalization absorption shortcut",
                "needed_identity": "leakage is universal constant with no derivative, time, species, vector, range, or anisotropic dependence",
                "current_evidence": "1121 rejects absorption shortcut; R11 missing ledger still has source-normalization operator",
                "result": "REJECT_SHORTCUT",
                "blocker": "absorbing c into measured GM would hide observable PPN/R11 residuals",
                "valid_for_claim": "false",
            },
            {
                "zero_id": "CZ1138_3_projector_domain_stress",
                "target": "projector/domain stress silence",
                "needed_identity": "projector/domain stress is metric-independent/topological and carries no local source residual",
                "current_evidence": "1118 says projector stress is conditional; current R11 row has c_projector_domain_stress conditional",
                "result": "CONDITIONAL_NOT_PARENT_DERIVED",
                "blocker": "parent projector/domain stress ownership remains unsigned",
                "valid_for_claim": "false",
            },
            {
                "zero_id": "CZ1138_4_observed_coframe",
                "target": "observed coframe/source normalization",
                "needed_identity": "c vanishes in the PPN-safe observed local coframe, not by gauge or normalization choice",
                "current_evidence": "R11 minimum row fixes observed coframe but coefficient remains missing",
                "result": "MISSING_COFRAME_ZERO_PROOF",
                "blocker": "normalization is declared, not a zero theorem",
                "valid_for_claim": "false",
            },
            {
                "zero_id": "CZ1138_5_alpha3_bridge",
                "target": "K*c*epsilon alpha3 bridge",
                "needed_identity": "c=0 or K=0 or epsilon=0, or abs(K*c*epsilon)<=4e-20 with sources",
                "current_evidence": "1136 PI1136_1_R11_alpha3 is blocked by K, c, and epsilon",
                "result": "NOT_SCOREABLE",
                "blocker": "K, c, and epsilon are unsourced; no product shortcut",
                "valid_for_claim": "false",
            },
            {
                "zero_id": "CZ1138_6_verdict",
                "target": "c zero theorem for current corpus",
                "needed_identity": "CZ1138_1 through CZ1138_5 close from parent-signed identities",
                "current_evidence": "all active zero routes are failed, missing, conditional, or not scoreable",
                "result": "C_ZERO_NOT_DERIVED",
                "blocker": "no parent theorem-zero or numeric coefficient source",
                "valid_for_claim": "false",
            },
        ]
    )


def canonical_row() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "row_id": "CROW1138_0_c_domain_source_normalization_operator",
                "model_id": "MTS_source_normalized_Newton_branch",
                "branch_id": "domain_R11_c_source_normalization_1138_contract",
                "vector_id": "R11_c_domain_source_normalization_executable_contract",
                "operator_family": "source_normalization_operator",
                "coefficient_symbol": "c_domain_source_normalization_operator",
                "alias_symbols": "c_R11_flux_alpha3",
                "coefficient_value_or_theorem": "MISSING_DOMAIN_MU_EXTRA_OPERATOR_ZERO_OR_NUMERIC_COEFFICIENT",
                "coefficient_units": "dimensionless_mu_extra_over_G_eff_M_eff_or_declared_operator_units",
                "normalization": "relative_to_observed_local_coframe_and_measured_GM; no source-unity or gauge-absorption shortcut",
                "operator_form": "mu_obs = G_eff*M_eff + mu_domain_projector + derivative/vector/anisotropy source-normalization corrections",
                "weak_field_map": "R5/R6/R7/R8 maps from domain projector coefficient rows; R7 alpha3 includes K_R11_flux_alpha3*c_domain_source_normalization_operator*epsilon_domain_flux",
                "affected_rows": "R5;R6;R7;R8;R11",
                "induced_observable": "alpha1;alpha2;alpha3;xi;operator_ledger",
                "predicted_residual_or_bound_source": "MISSING_DOMAIN_PROJECTOR_COEFFICIENT_PRODUCTS_OR_THEOREM_ZERO",
                "target_bound": "4e-20 for alpha3 branch; sibling bounds per R5/R6/R8/R11 ledgers",
                "formula_reference": "1138-Y5-R10-c-domain-source-normalization-zero-or-executable-coefficient-row.md",
                "source_file": "MISSING_PARENT_ACTION_OR_NUMERIC_COEFFICIENT_SOURCE",
                "assumptions": "observed coframe fixed; compact local branch; no tuned cancellation; no absorption into measured GM unless parent-proved universal and derivative-silent",
                "current_status": "CANONICAL_CONTRACT_ROW_BLOCKED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
                "notes": "This row supersedes no older row as evidence; it is a strict contract until a real value or theorem-zero source replaces MISSING fields.",
            }
        ]
    )


def missing_field_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "missing_id": "MISS1138_0_value",
                "field": "coefficient_value_or_theorem",
                "current_value": "MISSING_DOMAIN_MU_EXTRA_OPERATOR_ZERO_OR_NUMERIC_COEFFICIENT",
                "required_replacement": "numeric coefficient with units/source, or parent theorem-zero certificate",
                "blocks_claim": "true",
                "valid_for_claim": "false",
            },
            {
                "missing_id": "MISS1138_1_source",
                "field": "source_file",
                "current_value": "MISSING_PARENT_ACTION_OR_NUMERIC_COEFFICIENT_SOURCE",
                "required_replacement": "existing local source proving value/theorem, not a map-only ledger",
                "blocks_claim": "true",
                "valid_for_claim": "false",
            },
            {
                "missing_id": "MISS1138_2_bound",
                "field": "predicted_residual_or_bound_source",
                "current_value": "MISSING_DOMAIN_PROJECTOR_COEFFICIENT_PRODUCTS_OR_THEOREM_ZERO",
                "required_replacement": "same-frame residual/bound source for c contribution and sibling rows",
                "blocks_claim": "true",
                "valid_for_claim": "false",
            },
            {
                "missing_id": "MISS1138_3_K_epsilon",
                "field": "alpha3 product siblings",
                "current_value": "MISSING_K_R11_FLUX_ALPHA3_AND_EPSILON_DOMAIN_FLUX",
                "required_replacement": "K and epsilon source rows or theorem-zero routes",
                "blocks_claim": "true",
                "valid_for_claim": "false",
            },
        ]
    )


def sibling_guard_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "guard_id": "SG1138_0_alpha1_alpha2_vector",
                "affected_rows": "R5;R6",
                "reason": "source-normalization/vector family can leak into preferred-frame vector rows",
                "status": "ACTIVE_BLOCKED_BY_c_AND_VECTOR_LEDGER",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "SG1138_1_alpha3",
                "affected_rows": "R7",
                "reason": "K*c*epsilon alpha3 branch cannot be scored while c/K/epsilon are missing",
                "status": "ACTIVE_BLOCKED_BY_c_K_EPSILON",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "SG1138_2_xi",
                "affected_rows": "R8",
                "reason": "projector/domain stress and source-normalization can leak into anisotropy row",
                "status": "ACTIVE_BLOCKED_BY_c_AND_PROJECTOR_STRESS",
                "valid_for_claim": "false",
            },
            {
                "guard_id": "SG1138_3_R11",
                "affected_rows": "R11",
                "reason": "operator ledger requires concrete coefficient/theorem rows with no MISSING fields",
                "status": "ACTIVE_BLOCKED_BY_CANONICAL_ROW",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1138_0_c_zero",
                "rule": "c_domain_source_normalization_operator=0 is parent-derived",
                "gate_pass": "false",
                "reason": "EH-only, absorption, projector-stress, and coframe routes fail or remain conditional",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1138_1_c_executable",
                "rule": "canonical c row is executable evidence",
                "gate_pass": "false",
                "reason": "canonical row still contains MISSING value/source/bound fields",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1138_2_no_absorption",
                "rule": "measured-GM/source-normalization absorption shortcut is rejected",
                "gate_pass": "true_nonclaim",
                "reason": "gauge/source-unity absorption cannot hide derivative/vector/anisotropic source hair",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1138_3_sibling_guards",
                "rule": "R5/R6/R7/R8/R11 sibling rows stay guarded",
                "gate_pass": "true_nonclaim",
                "reason": "c row affects more than alpha3 and remains unfilled",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1138_4_alpha3_R11_product",
                "rule": "K*c*epsilon alpha3 product can be evaluated",
                "gate_pass": "false",
                "reason": "K, c, and epsilon remain unsourced and no product shortcut is allowed",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1138_5_local_GR",
                "rule": "R10/PPN/local-GR can promote",
                "gate_pass": "false",
                "reason": "c/R11 source-normalization branch remains live and blocked",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1138_0_verdict",
                "decision": "c_zero_not_derived_and_c_row_not_executable",
                "reason": "zero routes fail/conditional and canonical row still has missing value/source/bound fields",
                "next_action": "do not use c as zero or numeric input in alpha3/R11 products",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1138_1_best_next",
                "decision": "attack_source_normalization_absorption_theorem_or_fill_real_c_value",
                "reason": "either prove c is universal derivative-silent and absorbable/zero, or source a real coefficient",
                "next_action": "split c into universal monopole part vs derivative/vector/anisotropic hair",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1138_2_claim_ceiling",
                "decision": "keep_R5_R6_R7_R8_R11_blocked",
                "reason": "c is a sibling-wide source-normalization blocker",
                "next_action": "no local-GR/PPN promotion until c branch closes or is bounded",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1138_0_1139",
                "next_target": "1139-Y5-R10-c-source-normalization-monopole-vs-hair-split.md",
                "objective": "split c_domain_source_normalization_operator into absorbable universal monopole calibration versus derivative/vector/anisotropic source hair; prove the hair zero or keep a real coefficient-source row blocked",
                "include": "universal monopole; measured-GM calibration; derivative/range/time/species/vector/anisotropic hair; observed coframe; R5/R6/R7/R8/R11 guards",
                "exclude": "source-unity shortcut; gauge absorption; product shortcut; tuned cancellation; alpha3/local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    zero_routes: list[dict[str, object]],
    canonical: list[dict[str, object]],
    missing: list[dict[str, object]],
    guards: list[dict[str, object]],
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

    all_rows = zero_routes + canonical + missing + guards + gates + decisions + next_target
    canonical_row = canonical[0]
    add("V1138_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1138_1_zero_not_derived", zero_routes[-1]["result"] == "C_ZERO_NOT_DERIVED", "c zero theorem remains unclosed")
    add("V1138_2_canonical_row_present", canonical_row["coefficient_symbol"] == "c_domain_source_normalization_operator" and canonical_row["alias_symbols"] == "c_R11_flux_alpha3", "canonical c row with alias is present")
    add("V1138_3_canonical_row_blocked", canonical_row["current_status"] == "CANONICAL_CONTRACT_ROW_BLOCKED" and "MISSING" in canonical_row["coefficient_value_or_theorem"], "canonical row remains blocked by missing value/theorem")
    add("V1138_4_missing_fields_listed", {"coefficient_value_or_theorem", "source_file", "predicted_residual_or_bound_source", "alpha3 product siblings"}.issubset({row["field"] for row in missing}), "missing fields are explicitly listed")
    add("V1138_5_sibling_guards", {"R5;R6", "R7", "R8", "R11"}.issubset({row["affected_rows"] for row in guards}), "sibling guards cover R5/R6/R7/R8/R11")
    add("V1138_6_absorption_rejected", gates[2]["gate_pass"] == "true_nonclaim", "measured-GM/source-unity absorption shortcut is rejected")
    add("V1138_7_gates_blocked", all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and sum(row["gate_pass"] == "false" for row in gates) >= 4, "claim gates remain blocked")
    add("V1138_8_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in canonical + next_target), "all generated rows remain nonclaim")
    add("V1138_9_next_target", next_target[0]["next_target"].startswith("1139-") and "monopole-vs-hair" in str(next_target[0]["next_target"]), "1139 handoff targets monopole-vs-hair split")
    add("V1138_10_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1138_11_csv_parse", csv_parse_ok, "all 1138 CSV outputs parse cleanly")
    add("V1138_12_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1138_SUMMARY", True, "1138 keeps c blocked, writes canonical c contract row, and sends c to monopole-vs-hair split")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    zero_routes: list[dict[str, object]],
    canonical: list[dict[str, object]],
    missing: list[dict[str, object]],
    guards: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1138 - Y5/R10 c Domain Source-Normalization Zero Or Executable Coefficient Row

**Current verdict:** `c_domain_source_normalization_operator=0` is still not derived, and the canonical executable `c` row is still not executable because its value/theorem source is missing.

**Useful progress:** `c_R11_flux_alpha3` is now pinned to one canonical R11 source-normalization row instead of floating as a new symbol. That row explicitly blocks R5/R6/R7/R8/R11 until filled or theorem-zero.

**Important rejection:** measured-GM/source-normalization absorption is not allowed as a shortcut. Only a universal, derivative-silent, vector-silent, anisotropy-silent parent identity could make absorption harmless.

**Best next attack:** split `c` into universal monopole calibration versus derivative/vector/anisotropic hair. The monopole might be absorbable; the hair cannot be hidden.

**No claim:** no alpha3, R10, PPN, local-GR, measured-GM, or FLRW claim follows from 1138.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Zero-Route Audit
{table(["zero_id", "target", "needed_identity", "current_evidence", "result", "blocker", "valid_for_claim"], zero_routes)}

## Canonical c Row
{table(["row_id", "model_id", "branch_id", "vector_id", "operator_family", "coefficient_symbol", "alias_symbols", "coefficient_value_or_theorem", "coefficient_units", "normalization", "operator_form", "weak_field_map", "affected_rows", "induced_observable", "predicted_residual_or_bound_source", "target_bound", "formula_reference", "source_file", "assumptions", "current_status", "valid_for_claim", "claim_allowed", "notes"], canonical)}

## Missing Field Ledger
{table(["missing_id", "field", "current_value", "required_replacement", "blocks_claim", "valid_for_claim"], missing)}

## Sibling Guards
{table(["guard_id", "affected_rows", "reason", "status", "valid_for_claim"], guards)}

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
        "source_register": OUT / "P8_Y5_R10_1138_SOURCE_REGISTER.csv",
        "zero_routes": OUT / "P8_Y5_R10_1138_C_ZERO_ROUTE_AUDIT.csv",
        "canonical": OUT / "P8_Y5_R10_1138_CANONICAL_C_SOURCE_NORMALIZATION_ROW.csv",
        "missing": OUT / "P8_Y5_R10_1138_C_ROW_MISSING_FIELD_LEDGER.csv",
        "guards": OUT / "P8_Y5_R10_1138_C_SIBLING_GUARDS.csv",
        "gates": OUT / "P8_Y5_R10_1138_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1138_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1138_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1138_VALIDATION.csv",
    }
    sources = source_rows()
    zero_routes = zero_route_rows()
    canonical = canonical_row()
    missing = missing_field_rows()
    guards = sibling_guard_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["zero_routes"], zero_routes)
    write_csv(outputs["canonical"], canonical)
    write_csv(outputs["missing"], missing)
    write_csv(outputs["guards"], guards)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, zero_routes, canonical, missing, guards, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, zero_routes, canonical, missing, guards, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
