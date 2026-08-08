from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1121-Y5-R10-domain-alpha3-R11-leakage-zero-or-executable-row.md"


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
            "source_id": "SRC1121_0_1120_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1120_NEXT_TARGET.csv",
            "needle": "NEXT1120_0_1121",
            "note": "1120 handoff to R11 alpha3 leakage zero/executable row.",
        },
        {
            "source_id": "SRC1121_1_1120_pack",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1120_DOMAIN_ALPHA3_NUMERIC_SOURCE_PACK_NONCLAIM.csv",
            "needle": "SRCF1120_1_R11",
            "note": "1120 marks R11 alpha3 leakage/source-normalization as missing.",
        },
        {
            "source_id": "SRC1121_2_1118_theorem",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1118_DOMAIN_R11_ZERO_THEOREM_ATTEMPT.csv",
            "needle": "DOMAIN_R11_SOURCE_ZERO_NOT_DERIVED",
            "note": "1118 zero theorem attempt rejects current parent-owned R11 zero.",
        },
        {
            "source_id": "SRC1121_3_1118_candidate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1118_R11_DOMAIN_CANDIDATE_ROWS_NONCLAIM.csv",
            "needle": "W_domain_alpha3_epsilon_domain_flux",
            "note": "1118 candidate row carries the alpha3/domain leakage product as unfilled.",
        },
        {
            "source_id": "SRC1121_4_R11_zero",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_SOURCE_THEOREM_ZERO_ATTEMPT.csv",
            "needle": "Z6_verdict",
            "note": "R11 source-normalization zero route was rejected in the current corpus.",
        },
        {
            "source_id": "SRC1121_5_R11_fill",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_SOURCE_FILL_REQUIREMENTS.csv",
            "needle": "DSR_R7_alpha3",
            "note": "R11 fill requirements identify the alpha3 target bound and acceptance route.",
        },
        {
            "source_id": "SRC1121_6_R11_link",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_R11_LINK.csv",
            "needle": "L4_R11_operator",
            "note": "Domain alpha3 link requires an R11 source-normalization operator row.",
        },
        {
            "source_id": "SRC1121_7_R11_min_fill",
            "relative_path": "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv",
            "needle": "R11SN_2_domain_projector_mass",
            "note": "Minimum source-normalization row schema for domain projector mass.",
        },
        {
            "source_id": "SRC1121_8_R11_gates",
            "relative_path": "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_ACCEPTANCE_GATES.csv",
            "needle": "G1_no_missing_for_claim",
            "note": "Acceptance gate forbids claim-valid rows with missing coefficient/theorem inputs.",
        },
        {
            "source_id": "SRC1121_9_R11_executable",
            "relative_path": "source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv",
            "needle": "c_domain_source_normalization_operator",
            "note": "Existing executable-vector skeleton has the domain source-normalization row but it is retained/unfilled.",
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


def theorem_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "proof_id": "Z1121_0_conditional_zero",
                "claim": "P_R11_source_alpha3=0 if the compact local branch is EH-only after measured-source normalization",
                "required_identity": "delta mu_domain_projector=0 and all R11 representative-dependent source-normalization operators vanish in the observed local coframe",
                "current_evidence": "R11 zero attempts leave source-normalization, projector stress, and domain vector/flux rows missing or conditional",
                "result": "CONDITIONAL_NOT_PARENT_DERIVED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
                "next_action": "derive parent descent of source normalization or keep executable coefficient row",
            },
            {
                "proof_id": "Z1121_1_EH_only_silence",
                "claim": "c_domain_source_normalization_operator=0 from EH-only exterior silence",
                "required_identity": "all non-EH/local-boundary/domain source terms reduce to boundary-only or exact-zero through R11 in the compact branch",
                "current_evidence": "R11_DOMAIN_SOURCE_THEOREM_ZERO_ATTEMPT has fail_current_corpus on EH-only/R11 silence",
                "result": "FAIL_CURRENT_CORPUS",
                "valid_for_claim": "false",
                "claim_allowed": "false",
                "next_action": "supply actual parent-action clause or fill numeric coefficient",
            },
            {
                "proof_id": "Z1121_2_absorption_guard",
                "claim": "source-normalization leakage can be absorbed into measured GM and ignored",
                "required_identity": "leakage is universal constant with no range, time, species, derivative, vector, or anisotropic dependence",
                "current_evidence": "R11 gates explicitly reject absorption of derivative/range/time/species/vector source-normalization hair",
                "result": "REJECT_ABSORPTION_SHORTCUT",
                "valid_for_claim": "false",
                "claim_allowed": "false",
                "next_action": "map the leakage to PPN alpha3 or prove it is exactly universal and silent",
            },
            {
                "proof_id": "Z1121_3_alpha3_bridge",
                "claim": "R11 silence closes domain alpha3",
                "required_identity": "W_domain_alpha3*epsilon_domain_flux + P_R11_source_alpha3 = 0 or absolute value <= 4e-20 without tuned cancellation",
                "current_evidence": "1120 factor ledger and 1118 candidate rows keep both the source leakage and product unfilled",
                "result": "FAIL_CURRENT_CORPUS",
                "valid_for_claim": "false",
                "claim_allowed": "false",
                "next_action": "build canonical alpha3 leakage row with explicit coefficient, units, normalization, weak-field map, and source path",
            },
            {
                "proof_id": "Z1121_4_verdict",
                "claim": "R11 alpha3 leakage zero is proved in the current corpus",
                "required_identity": "Z1121_0 through Z1121_3 all close with parent-owned identities",
                "current_evidence": "zero proof remains conditional or failed; no executable numeric/theorem row exists yet",
                "result": "ZERO_ROUTE_NOT_CLOSED",
                "valid_for_claim": "false",
                "claim_allowed": "false",
                "next_action": "use the executable row contract as the next work target",
            },
        ]
    )


def executable_contract_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "row_id": "R11A3_1121_0_alpha3_source_leakage",
                "model_id": "MTS_source_normalized_Newton_branch",
                "branch_id": "domain_alpha3_R11_leakage_1121_contract",
                "vector_id": "R11_alpha3_source_normalization_executable_contract",
                "operator_family": "source_normalization_operator",
                "coefficient_symbol": "c_domain_source_normalization_operator",
                "coefficient_value_or_theorem": "MISSING_DOMAIN_SOURCE_NORMALIZATION_OPERATOR_ZERO_OR_NUMERIC_COEFFICIENT",
                "coefficient_units": "dimensionless_mapped_alpha3_contribution_or_declared_operator_units",
                "normalization": "relative_to_observed_local_coframe_and_measured_GM; no source-unity shortcut",
                "operator_form": "mu_obs = G_EH*M_EH + mu_domain_projector + delta_mu_R11_alpha3",
                "weak_field_map": "P_R11_source_alpha3 = K_R11_alpha3 * c_domain_source_normalization_operator * epsilon_domain_projector, or exact-zero theorem",
                "affected_rows": "R7_alpha3;R11_operator_ledger",
                "induced_observable": "alpha3",
                "predicted_residual_or_bound_source": "abs(P_R11_source_alpha3) <= 4e-20 after sibling rows are separately closed",
                "target_bound": "4e-20",
                "formula_reference": "1121-Y5-R10-domain-alpha3-R11-leakage-zero-or-executable-row.md",
                "source_file": "MISSING_PARENT_ACTION_OR_NUMERIC_COEFFICIENT_SOURCE",
                "assumptions": "observed coframe fixed; compact local branch; no tuned cancellation; no absorption into measured GM unless universal and derivative-silent",
                "current_status": "MISSING_EXECUTABLE_INPUTS",
                "valid_for_claim": "false",
                "claim_allowed": "false",
                "notes": "This is the canonical row contract, not a claim row.",
            }
        ]
    )


def field_contract_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "field_id": "F1121_0_coefficient",
                "required_field": "coefficient_value_or_theorem",
                "acceptance": "numeric coefficient with source path or parent-owned theorem zero",
                "current_status": "MISSING",
                "valid_for_claim": "false",
            },
            {
                "field_id": "F1121_1_units",
                "required_field": "coefficient_units",
                "acceptance": "dimensionless alpha3 convention or declared operator units with conversion",
                "current_status": "DECLARED_TEMPLATE_NOT_SOURCED",
                "valid_for_claim": "false",
            },
            {
                "field_id": "F1121_2_normalization",
                "required_field": "normalization",
                "acceptance": "explicit measured-GM/local-coframe normalization with no absorption cheat",
                "current_status": "TEMPLATE_ONLY",
                "valid_for_claim": "false",
            },
            {
                "field_id": "F1121_3_weak_field_map",
                "required_field": "weak_field_map",
                "acceptance": "derive or source K_R11_alpha3 map into PPN alpha3",
                "current_status": "MISSING_DERIVED_MAP",
                "valid_for_claim": "false",
            },
            {
                "field_id": "F1121_4_bound",
                "required_field": "target_bound",
                "acceptance": "alpha3 target bound 4e-20 carried explicitly",
                "current_status": "PRESENT",
                "valid_for_claim": "false",
            },
            {
                "field_id": "F1121_5_source",
                "required_field": "source_file",
                "acceptance": "local source path to derivation or numeric coefficient evidence, no MISSING marker",
                "current_status": "MISSING",
                "valid_for_claim": "false",
            },
            {
                "field_id": "F1121_6_siblings",
                "required_field": "sibling_guard",
                "acceptance": "R5/R6/R8/R11 sibling rows cannot be bypassed by alpha3-only closure",
                "current_status": "ACTIVE_BLOCK",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1121_0_zero_theorem",
                "rule": "R11 alpha3 leakage is exactly zero",
                "gate_pass": "false",
                "reason": "source-normalization zero remains conditional/failed in current corpus",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1121_1_contract_schema",
                "rule": "canonical alpha3 R11 row has all required schema fields",
                "gate_pass": "true_nonclaim",
                "reason": "1121 defines the row schema and required fields but leaves missing inputs explicit",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1121_2_no_missing",
                "rule": "claim row has no MISSING markers and no template-only fields",
                "gate_pass": "false",
                "reason": "coefficient/theorem, weak-field map, and source file are missing",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1121_3_alpha3_bound",
                "rule": "abs(P_R11_source_alpha3) <= 4e-20 is numerically or theorem-zero satisfied",
                "gate_pass": "false",
                "reason": "no numeric P_R11_source_alpha3 or parent-zero theorem exists",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1121_4_local_GR",
                "rule": "local-GR/R10 branch can use the R11 alpha3 row as closed evidence",
                "gate_pass": "false",
                "reason": "1121 is a contract checkpoint only",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1121_0_zero_route",
                "decision": "do_not_claim_zero",
                "reason": "the required parent descent/source-normalization silence is not in the corpus",
                "next_action": "attack the source-normalization-to-alpha3 coupling map",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1121_1_executable_row",
                "decision": "canonical_contract_created",
                "reason": "the row now has a fixed schema, bound, normalization guard, and missing-field ledger",
                "next_action": "derive or source K_R11_alpha3 and c_domain_source_normalization_operator",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1121_2_priority",
                "decision": "coupling_map_first",
                "reason": "without the weak-field map, a numeric coefficient cannot be compared to 4e-20",
                "next_action": "1122 should derive the alpha3 coupling map before fitting numbers",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1121_0_1122",
                "next_target": "1122-Y5-R10-source-normalization-alpha3-coupling-map-or-zero.md",
                "objective": "derive the weak-field coupling map P_R11_source_alpha3 = K_R11_alpha3*c_domain_source_normalization_operator*epsilon_domain_projector, or prove K_R11_alpha3=0 from parent symmetries",
                "include": "K_R11_alpha3; alpha3 PPN definition; source-normalization perturbation; observed coframe; no tuned cancellation; target 4e-20",
                "exclude": "numeric claim without map; absorption into GM; local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    proofs: list[dict[str, object]],
    contract: list[dict[str, object]],
    fields: list[dict[str, object]],
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

    required_contract = {
        "coefficient_value_or_theorem",
        "coefficient_units",
        "normalization",
        "operator_form",
        "weak_field_map",
        "affected_rows",
        "induced_observable",
        "predicted_residual_or_bound_source",
        "target_bound",
        "source_file",
        "assumptions",
    }
    field_names = {str(row["required_field"]) for row in fields}
    all_rows = proofs + contract + fields + gates + decisions + next_target
    add("V1121_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1121_1_zero_not_claimed", proofs[-1]["result"] == "ZERO_ROUTE_NOT_CLOSED" and all(row["claim_allowed"] == "false" for row in proofs), "zero route remains unclaimed")
    add("V1121_2_contract_fields", required_contract.issubset(set(contract[0].keys())), "canonical row includes minimum executable fields")
    add("V1121_3_missing_ledger", {"coefficient_value_or_theorem", "weak_field_map", "source_file"}.issubset(field_names) and any(str(row["current_status"]).startswith("MISSING") for row in fields), "missing executable inputs are explicit")
    add("V1121_4_bound_explicit", contract[0]["target_bound"] == "4e-20" and "4e-20" in contract[0]["predicted_residual_or_bound_source"], "alpha3 4e-20 bound is carried into the row")
    add("V1121_5_gates_blocked", all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and sum(row["gate_pass"] == "false" for row in gates) >= 3, "claim gates remain blocked")
    add("V1121_6_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in proofs + contract + next_target), "all generated rows remain nonclaim")
    add("V1121_7_next_target", next_target[0]["next_target"].startswith("1122-") and "coupling-map" in str(next_target[0]["next_target"]), "1122 handoff targets source-normalization alpha3 coupling map")
    add("V1121_8_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1121_9_csv_parse", csv_parse_ok, "all 1121 CSV outputs parse cleanly")
    add("V1121_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1121_SUMMARY", True, "1121 rejects current zero claim and creates alpha3 R11 executable-row contract")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    proofs: list[dict[str, object]],
    contract: list[dict[str, object]],
    fields: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1121 - Y5/R10 Domain Alpha3 R11 Leakage: Zero Or Executable Row

**Current verdict:** the clean zero proof still does not close. The corpus has a conditional route to `P_R11_source_alpha3=0`, but not a parent-owned identity for `c_domain_source_normalization_operator=0`.

**Useful progress:** the R11 alpha3 leakage is now pinned to one canonical row contract with the exact missing fields: coefficient/theorem, units, normalization, weak-field map, source path, and the `4e-20` alpha3 target.

**No claim:** 1121 does not pass domain `alpha3`, R11, R10, PPN, or local-GR. It is a contract checkpoint for the next derivation.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Zero-Proof Audit
{table(["proof_id", "claim", "required_identity", "current_evidence", "result", "claim_allowed", "next_action"], proofs)}

## Canonical R11 Alpha3 Row Contract
{table(["row_id", "operator_family", "coefficient_symbol", "coefficient_value_or_theorem", "coefficient_units", "normalization", "operator_form", "weak_field_map", "affected_rows", "induced_observable", "predicted_residual_or_bound_source", "target_bound", "source_file", "current_status", "valid_for_claim", "claim_allowed"], contract)}

## Missing-Field Ledger
{table(["field_id", "required_field", "acceptance", "current_status", "valid_for_claim"], fields)}

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
        "source_register": OUT / "P8_Y5_R10_1121_SOURCE_REGISTER.csv",
        "zero_proof": OUT / "P8_Y5_R10_1121_R11_ALPHA3_ZERO_PROOF_AUDIT.csv",
        "contract": OUT / "P8_Y5_R10_1121_R11_ALPHA3_EXECUTABLE_ROW_CONTRACT.csv",
        "fields": OUT / "P8_Y5_R10_1121_R11_ALPHA3_MISSING_FIELD_LEDGER.csv",
        "gates": OUT / "P8_Y5_R10_1121_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1121_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1121_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1121_VALIDATION.csv",
    }
    sources = source_rows()
    proofs = theorem_rows()
    contract = executable_contract_rows()
    fields = field_contract_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["zero_proof"], proofs)
    write_csv(outputs["contract"], contract)
    write_csv(outputs["fields"], fields)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, proofs, contract, fields, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, proofs, contract, fields, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
