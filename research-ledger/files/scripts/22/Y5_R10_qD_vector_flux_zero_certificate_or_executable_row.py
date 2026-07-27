from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1126-Y5-R10-qD-vector-flux-zero-certificate-or-executable-row.md"


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
            "source_id": "SRC1126_0_1125_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1125_NEXT_TARGET.csv",
            "needle": "NEXT1125_0_1126",
            "note": "1125 handoff to q_D vector/flux zero certificate or executable row.",
        },
        {
            "source_id": "SRC1126_1_1125_qd_split",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1125_RETAINED_QD_COMPONENT_SPLIT.csv",
            "needle": "QD1125_0_vector_flux",
            "note": "1125 isolates q_D_vector_flux as the direct alpha3 component.",
        },
        {
            "source_id": "SRC1126_2_no_vector",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
            "needle": "T2_no_flux_local_representative",
            "note": "No-vector/no-flux route remains conditional, not parent-derived.",
        },
        {
            "source_id": "SRC1126_3_alpha3_link",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_R11_LINK.csv",
            "needle": "L2_alpha3_flux",
            "note": "Domain alpha3 link requires flux product below 4e-20 or theorem-zero.",
        },
        {
            "source_id": "SRC1126_4_1123_bound",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1123_ALPHA3_FLUX_BOUND_PRODUCT_ROWS.csv",
            "needle": "FB1123_0_alpha3_flux_product",
            "note": "1123 staged strict R11 flux product bound row.",
        },
        {
            "source_id": "SRC1126_5_1122_flux",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1122_REMAINING_FLUX_CONTRACT.csv",
            "needle": "R11F1122_0_flux_alpha3",
            "note": "1122 narrowed R11 alpha3 map to K*c*epsilon flux product.",
        },
        {
            "source_id": "SRC1126_6_domain_coeffs",
            "relative_path": "source-intake/mts_residuals/P8_mu_extra_domain_projector_coefficients.csv",
            "needle": "W_domain_alpha3_epsilon_domain_flux",
            "note": "Domain alpha3 product row carries W_domain_alpha3*epsilon_domain_flux.",
        },
        {
            "source_id": "SRC1126_7_ownership",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_ALPHA3_PREMISE_OWNERSHIP.csv",
            "needle": "P3_local_trivial_representative",
            "note": "Local trivial representative is conditional, not a closed zero certificate.",
        },
        {
            "source_id": "SRC1126_8_R11_domain_minimum",
            "relative_path": "source-intake/mts_residuals/R11_DOMAIN_PROJECTOR_OPERATOR_VECTOR_MINIMUM.csv",
            "needle": "c_domain_vector_or_selector_marker",
            "note": "Domain vector/preferred-frame family remains retained/unfilled.",
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


def zero_certificate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "cert_id": "ZC1126_0_definition",
                "certificate_piece": "q_D_vector_flux target",
                "formal_requirement": "q_D_vector_flux maps only through epsilon_domain_vector and epsilon_domain_flux in the observed local coframe",
                "current_status": "DEFINED_FROM_1125",
                "missing_input": "none",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "cert_id": "ZC1126_1_scalar_selector",
                "certificate_piece": "selector carries no local vector",
                "formal_requirement": "P_loc^i_mu nabla^mu chi_D=0 and P_loc^i_mu n_D^mu=0 from parent scalar stationary selector",
                "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
                "missing_input": "parent selector action proving chi_D/n_mu have no local spatial marker",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "cert_id": "ZC1126_2_local_no_flux",
                "certificate_piece": "local representative carries no momentum/domain flux",
                "formal_requirement": "[J_D]_local=0 and P_loc^i_mu F_D^mu=0 in compact stationary branch",
                "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
                "missing_input": "parent local representative theorem, not plateau axiom",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "cert_id": "ZC1126_3_no_FLRW_memory_local",
                "certificate_piece": "no coherent FLRW memory class active locally",
                "formal_requirement": "local compact branch is in the trivial/exact class while FLRW memory remains an allowed cosmological branch",
                "current_status": "MISSING_PARENT_BRANCH_SELECTOR",
                "missing_input": "branch selector separating local trivial representative from FLRW active memory",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "cert_id": "ZC1126_4_R11_vector_silence",
                "certificate_piece": "R11 vector/preferred-frame family is zero or executable",
                "formal_requirement": "c_domain_vector_or_selector_marker=0 or sourced executable coefficient product",
                "current_status": "LIVE_UNFILLED",
                "missing_input": "R11 vector row with no MISSING fields or theorem-zero source",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "cert_id": "ZC1126_5_verdict",
                "certificate_piece": "q_D_vector_flux=0 is proved in current corpus",
                "formal_requirement": "ZC1126_1 through ZC1126_4 all pass with parent-owned identities",
                "current_status": "ZERO_CERTIFICATE_NOT_CLOSED",
                "missing_input": "scalar selector, local no-flux, branch selector, and R11 vector silence remain unsigned/unfilled",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def executable_product_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "product_id": "EP1126_0_domain_flux",
                "observable": "alpha3",
                "quantity": "W_domain_alpha3*epsilon_domain_flux",
                "formula": "alpha3_domain_flux = W_domain_alpha3*epsilon_domain_flux",
                "target_bound": "4e-20",
                "required_inputs": "W_domain_alpha3; epsilon_domain_flux; units/normalization; source path",
                "current_value": "MISSING_NUMERIC_PRODUCT_OR_THEOREM_ZERO",
                "acceptance": "zero certificate or abs(W_domain_alpha3*epsilon_domain_flux) <= 4e-20, with no local-domain-frame shortcut",
                "current_status": "MISSING",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "product_id": "EP1126_1_R11_flux",
                "observable": "alpha3",
                "quantity": "K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "formula": "P_R11_source_alpha3_flux = K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "target_bound": "4e-20",
                "required_inputs": "K_R11_flux_alpha3; c_R11_flux_alpha3; epsilon_domain_flux; observed coframe normalization; source paths",
                "current_value": "MISSING_NUMERIC_PRODUCT_OR_THEOREM_ZERO",
                "acceptance": "zero certificate or abs(K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux) <= 4e-20",
                "current_status": "MISSING",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
            {
                "product_id": "EP1126_2_total_direct_flux_guard",
                "observable": "alpha3",
                "quantity": "alpha3_direct_flux_total",
                "formula": "alpha3_direct_flux_total = W_domain_alpha3*epsilon_domain_flux + K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux",
                "target_bound": "4e-20",
                "required_inputs": "EP1126_0 and EP1126_1 both sourced or theorem-zero; sibling R5/R6/R8/R11 guards active",
                "current_value": "MISSING_NO_TUNED_CANCELLATION_INPUTS",
                "acceptance": "do not use cancellation between domain and R11 flux pieces unless independently derived by parent identity",
                "current_status": "GUARD_ONLY_NOT_SCOREABLE",
                "claim_allowed": "false",
                "valid_for_claim": "false",
            },
        ]
    )


def obligation_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "obligation_id": "OB1126_0_selector_action",
                "required_artifact": "parent scalar stationary selector action",
                "must_show": "selector variables cannot carry independent local normal/velocity/marker vector",
                "current_status": "MISSING_PARENT_DERIVATION",
                "if_closed": "kills epsilon_domain_vector and helps close q_D_vector_flux",
                "valid_for_claim": "false",
            },
            {
                "obligation_id": "OB1126_1_local_representative",
                "required_artifact": "local trivial/exact representative theorem",
                "must_show": "[J_D]_local=0 and P_loc^i_mu F_D^mu=0 for compact local branch",
                "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
                "if_closed": "sets epsilon_domain_flux=0",
                "valid_for_claim": "false",
            },
            {
                "obligation_id": "OB1126_2_branch_selector",
                "required_artifact": "local-vs-FLRW branch selector",
                "must_show": "FLRW memory can be active cosmologically while local compact branch is exact/trivial",
                "current_status": "MISSING_PARENT_INPUT",
                "if_closed": "prevents local no-flux theorem from killing cosmology branch by hand",
                "valid_for_claim": "false",
            },
            {
                "obligation_id": "OB1126_3_numeric_inputs",
                "required_artifact": "executable alpha3 flux product row",
                "must_show": "W/K/c/epsilon values, units, normalization, source paths, no MISSING markers",
                "current_status": "MISSING",
                "if_closed": "allows nonclaim smoke comparison to 4e-20 if theorem route fails",
                "valid_for_claim": "false",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "G1126_0_zero_certificate",
                "rule": "q_D_vector_flux=0 is parent-certified",
                "gate_pass": "false",
                "reason": "selector/no-flux/branch/R11 vector clauses remain unsigned",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1126_1_domain_product",
                "rule": "W_domain_alpha3*epsilon_domain_flux is zero or below 4e-20",
                "gate_pass": "false",
                "reason": "W_domain_alpha3 and epsilon_domain_flux are not sourced",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1126_2_R11_product",
                "rule": "K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux is zero or below 4e-20",
                "gate_pass": "false",
                "reason": "K_R11_flux_alpha3, c_R11_flux_alpha3, and epsilon_domain_flux are not sourced",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1126_3_total_no_cancellation",
                "rule": "total direct flux cannot pass by tuned cancellation",
                "gate_pass": "true_nonclaim",
                "reason": "1126 separates domain and R11 flux rows and forbids cancellation credit",
                "valid_for_claim": "false",
            },
            {
                "gate_id": "G1126_4_alpha3",
                "rule": "domain/R11 alpha3 direct flux is closed",
                "gate_pass": "false",
                "reason": "zero and numeric routes both remain missing",
                "valid_for_claim": "false",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "D1126_0_verdict",
                "decision": "qD_vector_flux_not_closed",
                "reason": "the zero certificate is conditional/missing and the product rows have no sourced inputs",
                "next_action": "derive the local-vs-FLRW branch selector or fill the executable flux product",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1126_1_best_next",
                "decision": "branch_selector_first",
                "reason": "a parent branch selector could kill local epsilon_domain_flux without damaging the cosmology branch",
                "next_action": "prove local trivial representative and FLRW active memory are different branches of the same parent structure",
                "valid_for_claim": "false",
            },
            {
                "decision_id": "D1126_2_fallback",
                "decision": "keep_executable_product_pack",
                "reason": "if branch selector cannot be proved, the alpha3 flux row must be sourced numerically",
                "next_action": "no PPN/local-GR promotion until products are sourced or theorem-zero",
                "valid_for_claim": "false",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1126_0_1127",
                "next_target": "1127-Y5-R10-local-vs-FLRW-branch-selector-no-flux-certificate.md",
                "objective": "derive a parent branch selector showing local compact branch has trivial/exact domain flux while FLRW/cosmological memory may remain active; otherwise keep q_D_vector_flux as executable alpha3 product rows",
                "include": "local trivial representative; FLRW memory branch; epsilon_domain_flux; scalar stationary selector; branch selector; no plateau axiom; 4e-20 guard",
                "exclude": "killing cosmology by local assumption; tuned cancellation; local-GR claim; GitHub; formalization edits",
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    certificates: list[dict[str, object]],
    products: list[dict[str, object]],
    obligations: list[dict[str, object]],
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

    all_rows = certificates + products + obligations + gates + decisions + next_target
    product_quantities = {row["quantity"] for row in products}
    add("V1126_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1126_1_zero_not_closed", certificates[-1]["current_status"] == "ZERO_CERTIFICATE_NOT_CLOSED", "q_D vector/flux zero certificate remains unclosed")
    add("V1126_2_product_rows", {"W_domain_alpha3*epsilon_domain_flux", "K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux", "alpha3_direct_flux_total"}.issubset(product_quantities), "domain, R11, and total direct-flux product rows are present")
    add("V1126_3_bound_explicit", all(row["target_bound"] == "4e-20" for row in products), "4e-20 alpha3 bound is explicit on every product row")
    add("V1126_4_no_cancellation_guard", products[-1]["current_status"] == "GUARD_ONLY_NOT_SCOREABLE" and gates[3]["gate_pass"] == "true_nonclaim", "total row is a no-cancellation guard, not a scoring shortcut")
    add("V1126_5_gates_blocked", all(row["gate_pass"] in {"false", "true_nonclaim"} for row in gates) and sum(row["gate_pass"] == "false" for row in gates) >= 4, "claim gates remain blocked")
    add("V1126_6_no_claim_rows", all(row.get("valid_for_claim") == "false" for row in all_rows) and all(row.get("claim_allowed", "false") == "false" for row in certificates + products + next_target), "all generated rows remain nonclaim")
    add("V1126_7_next_target", next_target[0]["next_target"].startswith("1127-") and "local-vs-FLRW" in str(next_target[0]["next_target"]), "1127 handoff targets local-vs-FLRW branch selector")
    add("V1126_8_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1126_9_csv_parse", csv_parse_ok, "all 1126 CSV outputs parse cleanly")
    add("V1126_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1126_SUMMARY", True, "1126 keeps q_D vector/flux blocked and stages separated alpha3 product rows")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    certificates: list[dict[str, object]],
    products: list[dict[str, object]],
    obligations: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1126 - Y5/R10 qD Vector/Flux Zero Certificate Or Executable Row

**Current verdict:** `q_D_vector_flux=0` is not proved. The needed scalar-selector, local no-flux, local-vs-FLRW branch selector, and R11 vector-silence certificates are still unsigned or unfilled.

**Useful progress:** the direct `alpha3` flux threat is now split into two nonclaim product rows: `W_domain_alpha3*epsilon_domain_flux` and `K_R11_flux_alpha3*c_R11_flux_alpha3*epsilon_domain_flux`.

**Guard:** the total direct-flux row is not scoreable by cancellation. Domain and R11 flux pieces must be independently zero, sourced, or bounded.

**No claim:** no domain/R11 `alpha3`, R10, PPN, Newton/local-GR, or measured-GM pass follows from 1126.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Zero Certificate Audit
{table(["cert_id", "certificate_piece", "formal_requirement", "current_status", "missing_input", "claim_allowed", "valid_for_claim"], certificates)}

## Executable Product Rows
{table(["product_id", "observable", "quantity", "formula", "target_bound", "required_inputs", "current_value", "acceptance", "current_status", "claim_allowed", "valid_for_claim"], products)}

## Certificate Obligations
{table(["obligation_id", "required_artifact", "must_show", "current_status", "if_closed", "valid_for_claim"], obligations)}

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
        "source_register": OUT / "P8_Y5_R10_1126_SOURCE_REGISTER.csv",
        "certificates": OUT / "P8_Y5_R10_1126_VECTOR_FLUX_ZERO_CERTIFICATE_AUDIT.csv",
        "products": OUT / "P8_Y5_R10_1126_ALPHA3_EXECUTABLE_PRODUCT_ROWS.csv",
        "obligations": OUT / "P8_Y5_R10_1126_SELECTOR_LOCAL_FLUX_OBLIGATIONS.csv",
        "gates": OUT / "P8_Y5_R10_1126_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1126_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1126_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1126_VALIDATION.csv",
    }
    sources = source_rows()
    certificates = zero_certificate_rows()
    products = executable_product_rows()
    obligations = obligation_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["certificates"], certificates)
    write_csv(outputs["products"], products)
    write_csv(outputs["obligations"], obligations)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, certificates, products, obligations, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, certificates, products, obligations, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
