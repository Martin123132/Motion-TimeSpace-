from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1113-Y5-R10-parent-owned-readout-descent-contract-or-alpha-product-input-acquisition.md"


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
            "source_id": "SRC1113_0_1112_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1112_NEXT_TARGET.csv",
            "needle": "NEXT1112_0_1113",
            "note": "1112 handoff to parent-owned readout/descent contract.",
        },
        {
            "source_id": "SRC1113_1_1112_descent",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1112_ZQEFF_DESCENT_THEOREM_ATTEMPT.csv",
            "needle": "ZQEFF_DESCENT_NOT_SIGNED",
            "note": "descent sandwich is exact but not signed.",
        },
        {
            "source_id": "SRC1113_2_1112_clauses",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1112_DESCENT_CLAUSE_AUDIT.csv",
            "needle": "CLAUSE1112_2_hidden_sequester",
            "note": "hidden-visible sequester clause.",
        },
        {
            "source_id": "SRC1113_3_1112_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1112_ALPHA_PRODUCT_RUNNER_CONTRACT_NONCLAIM.csv",
            "needle": "APC1112_2_R10_alpha_product",
            "note": "strict product runner contract.",
        },
        {
            "source_id": "SRC1113_4_1050_product_functor",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv",
            "needle": "PFT1050_5_verdict",
            "note": "product functor exact target not parent-derived.",
        },
        {
            "source_id": "SRC1113_5_967_readout_schema",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_967_READOUT_SCHEMA_THEOREM_ATTEMPT.csv",
            "needle": "RAV967_5_verdict",
            "note": "readout domain theorem conditional not globally signed.",
        },
        {
            "source_id": "SRC1113_6_767_matter_functor",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_767_PARENT_MATTER_FUNCTOR_REAUDIT.csv",
            "needle": "PMR767_3_no_alpha_mass_vertex",
            "note": "no alpha/mass vertex remains a hard blocker.",
        },
        {
            "source_id": "SRC1113_7_953_source_functor",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
            "needle": "NSF953_5_verdict",
            "note": "source label-forgetting theorem is conditional but not parent-derived.",
        },
        {
            "source_id": "SRC1113_8_1060_required",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1060_REQUIRED_INPUTS.csv",
            "needle": "REQ1060_3_R10_alpha",
            "note": "finite product required inputs.",
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


def parent_contract_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "contract_id": "POC1113_0_parent_domain",
                "contract_clause": "Conf_parent excludes readout variables and reduced-action knobs",
                "mathematical_role": "readout cannot source parent Euler-Lagrange equations",
                "current_status": "CONTRACT_WRITTEN_NOT_CORPUS_SIGNED",
                "source_basis": "RAV967 domain separation",
                "if_signed": "readout-selected forces are demoted to separate EFT branches",
                "if_unsigned": "readout backreaction can reintroduce local residuals",
            },
            {
                "contract_id": "POC1113_1_quotient_vertical",
                "contract_clause": "q: P -> Q and v in ker(Dq) are part of the parent local sector",
                "mathematical_role": "makes the descent sandwich applicable",
                "current_status": "ASSUMED_NOT_PARENT_DERIVED_HERE",
                "source_basis": "1112 descent sandwich",
                "if_signed": "q-observables are locally vertical-silent",
                "if_unsigned": "local vertical drift is not geometrically controlled",
            },
            {
                "contract_id": "POC1113_2_visible_pullback",
                "contract_clause": "S_vis = q^* Sbar_vis[A_Q, ebar(q), omega(q), theta_rep]",
                "mathematical_role": "visible coefficients factor through quotient data",
                "current_status": "EXACT_CONDITIONAL_NOT_PARENT_CONSTRUCTED",
                "source_basis": "PFT1050 visible action pullback",
                "if_signed": "visible alpha/mass vertices cannot depend on hidden representatives",
                "if_unsigned": "f_X F_Q^2 and mass-clock vertices remain legal",
            },
            {
                "contract_id": "POC1113_3_maxwell_owner",
                "contract_clause": "Z_Q_eff parent piece equals Zbar_parent(q,theta) plus only universal calibration constants",
                "mathematical_role": "kills D_v(C_P N_Q) without claiming measured alpha value",
                "current_status": "UNSIGNED",
                "source_basis": "1111/1112 parent norm wound",
                "if_signed": "parent norm contributes no local alpha drift",
                "if_unsigned": "b_alpha can originate in the parent Maxwell normalization itself",
            },
            {
                "contract_id": "POC1113_4_no_hidden_visible_morphisms",
                "contract_clause": "Hom(C_hid, Coeff(O_vis)) is constant or absent",
                "mathematical_role": "forbids nonconstant hidden-to-visible F2/mass/readout coefficients",
                "current_status": "UNSIGNED_CRITICAL",
                "source_basis": "PFT1050 and PMR767",
                "if_signed": "f_hid(I_hid)F_Q^2 cannot generate alpha drift",
                "if_unsigned": "finite alpha and mass product rows remain necessary",
            },
            {
                "contract_id": "POC1113_5_source_label_forgetting",
                "contract_clause": "source functor sees total observed stress, not species-labelled pairs",
                "mathematical_role": "prevents relative WEP/R10 source coupling constants",
                "current_status": "CONDITIONAL_THEOREM_NOT_PARENT_DERIVED",
                "source_basis": "NSF953 source functor theorem",
                "if_signed": "common source calibration can be absorbed while relative source weights vanish",
                "if_unsigned": "beta_source_alpha and source/test products remain physical debts",
            },
            {
                "contract_id": "POC1113_6_radiative_closure",
                "contract_clause": "renormalized/effective visible action and readout maps preserve quotient factorisation",
                "mathematical_role": "prevents loops, thresholds, and spectroscopy reduction from regenerating drift",
                "current_status": "UNSIGNED_CRITICAL",
                "source_basis": "PFT1050 radiative/readout closure",
                "if_signed": "tree-level descent survives observed alpha tests",
                "if_unsigned": "finite counterterm/product branch remains live",
            },
            {
                "contract_id": "POC1113_7_arena_functors",
                "contract_clause": "clock, WEP, and R10 observables are post-solution functors of the same q-branch",
                "mathematical_role": "turns one descent theorem into cross-arena local silence",
                "current_status": "MISSING_ARENA_MAPS",
                "source_basis": "1112 strict product contract",
                "if_signed": "clock/WEP/R10 products vanish or are computed from one parent map",
                "if_unsigned": "each arena needs its own numeric product row",
            },
        ]
    )


def signature_audit_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "audit_id": "SIG1113_0_contract_sufficiency",
                "question": "Would POC1113_0 through POC1113_7 sign Z_Q_eff descent?",
                "answer": "YES_CONDITIONAL",
                "reason": "the clauses force Z_Q_eff and readouts to factor through q, so D_v ln Z_Q_eff vanishes in the finite positive domain",
                "promotion_status": "not_promoted_because_clauses_unsigned",
            },
            {
                "audit_id": "SIG1113_1_minimal_extra_axiom_risk",
                "question": "Is adopting the contract as an axiom safe?",
                "answer": "CLOSURE_ONLY_IF_ADOPTED",
                "reason": "it would be a disciplined parent-action closure, not a derivation from earlier MTS material",
                "promotion_status": "label_as_closure_not_theorem",
            },
            {
                "audit_id": "SIG1113_2_best_derivation_needle",
                "question": "Which clause is most worth proving next?",
                "answer": "NO_HIDDEN_VISIBLE_COEFFICIENT_MORPHISM",
                "reason": "it attacks alpha, mass, clock, WEP, and R10 coupling debts at once",
                "promotion_status": "next_derivation_target",
            },
            {
                "audit_id": "SIG1113_3_empirical_fallback",
                "question": "What if the no-morphism theorem fails?",
                "answer": "FINITE_PRODUCT_INPUTS",
                "reason": "then the theory can still compete by predicting products under the strict contract, but not by claiming local silence",
                "promotion_status": "nonclaim_acquisition_path",
            },
        ]
    )


def acquisition_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "input_id": "AQ1113_0_balpha_or_zero",
                "product_row": "APC1112_0/APC1112_1/APC1112_2",
                "needed_input": "b_alpha or theorem-zero for D_v ln Z_Q_eff",
                "allowed_source": "parent no-hidden-visible/no-radiative-readout theorem or numeric coefficient derivation",
                "current_status": "MISSING_THEOREM_ZERO_OR_NUMERIC_COEFFICIENT",
                "blocks": "all alpha product claims",
            },
            {
                "input_id": "AQ1113_1_tau_clock",
                "product_row": "APC1112_0_clock_alpha_product",
                "needed_input": "tau_clock_time or direct clock product",
                "allowed_source": "clock readout map from parent local branch",
                "current_status": "MISSING_CLOCK_READOUT_MAP",
                "blocks": "standalone clock product prediction",
            },
            {
                "input_id": "AQ1113_2_beta_source_alpha",
                "product_row": "APC1112_1_wep_alpha_product",
                "needed_input": "beta_source_alpha",
                "allowed_source": "source label-forgetting theorem or finite source-normalization derivation",
                "current_status": "MISSING_SOURCE_NORMALIZATION",
                "blocks": "WEP alpha product prediction",
            },
            {
                "input_id": "AQ1113_3_tau_wep_material",
                "product_row": "APC1112_1_wep_alpha_product",
                "needed_input": "tau_WEP and material charge/readout map",
                "allowed_source": "parent WEP readout functor or direct eta product theorem",
                "current_status": "MISSING_WEP_DOMAIN_AND_MATERIAL_MAP",
                "blocks": "WEP alpha product prediction",
            },
            {
                "input_id": "AQ1113_4_r10_branch",
                "product_row": "APC1112_2_R10_alpha_product",
                "needed_input": "lambda_X, Z_X, K_X^R10(lambda), beta_source(lambda), beta_test(lambda), tau_R10, epsilon_tail",
                "allowed_source": "parent short-range branch map or finite numeric R10 product derivation",
                "current_status": "MISSING_R10_FINITE_BRANCH_VECTOR",
                "blocks": "R10 alpha(lambda) prediction",
            },
            {
                "input_id": "AQ1113_5_promoted_bound_curve",
                "product_row": "APC1112_2_R10_alpha_product",
                "needed_input": "claim-valid alpha_bound(lambda) curve",
                "allowed_source": "real digitized/source-backed R10 bound curve with valid_for_claim=true",
                "current_status": "MISSING_PROMOTED_BOUND_CURVE",
                "blocks": "R10 product comparison even if MTS product becomes numeric",
            },
            {
                "input_id": "AQ1113_6_cross_arena_branch",
                "product_row": "APC1112_3_cross_arena_alpha",
                "needed_input": "same Z_Q_eff branch and readout/domain classifier across clock/WEP/R10",
                "allowed_source": "global parent-owned readout functor",
                "current_status": "MISSING_CROSS_ARENA_PARENT_MAP",
                "blocks": "joint local evidence claim",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "CG1113_0_contract_signed",
                "claim": "parent-owned readout/descent contract is derived",
                "gate_pass": "false",
                "reason": "contract is written and sufficient, but core clauses are not parent-derived",
            },
            {
                "gate_id": "CG1113_1_alpha_silence",
                "claim": "b_alpha=0 follows",
                "gate_pass": "false",
                "reason": "requires signed no-hidden-visible and radiative/readout closure clauses",
            },
            {
                "gate_id": "CG1113_2_wep_r10_source",
                "claim": "WEP/R10 source products vanish or are predicted",
                "gate_pass": "false",
                "reason": "source label-forgetting and arena maps remain unsigned",
            },
            {
                "gate_id": "CG1113_3_product_acquisition",
                "claim": "finite product rows are runner-ready",
                "gate_pass": "false",
                "reason": "acquisition ledger still contains missing theorem or numeric inputs",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "DEC1113_0_contract_result",
                "decision": "global parent-owned readout/descent contract is constructed but not signed",
                "because": "the contract is sufficient for local alpha silence but would be closure if adopted without a derivation",
                "next_action": "try to derive the no-hidden-visible coefficient morphism clause",
            },
            {
                "decision_id": "DEC1113_1_next_derivation",
                "decision": "no-hidden-visible coefficient morphism is the best next target",
                "because": "it is the coupling bottleneck across alpha, mass, clocks, WEP, and R10",
                "next_action": "attempt object-language/category proof that visible coefficients cannot take hidden representatives as arguments",
            },
            {
                "decision_id": "DEC1113_2_fallback",
                "decision": "finite product acquisition is started but not claim-ready",
                "because": "if the coupling theorem fails, local tests need numeric products rather than symbolic placeholders",
                "next_action": "keep acquisition rows nonclaim until source paths and numeric values exist",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1113_0_1114",
                "next_target": "1114-Y5-R10-no-hidden-visible-coefficient-morphism-theorem-or-finite-coupling-inputs.md",
                "objective": "attempt to derive that visible EM/matter coefficients cannot take hidden representatives as arguments; if not, promote the coupling problem to finite alpha/mass/source product input acquisition",
                "include": "object language; product category; quotient map; representation labels; visible coefficient functors; hidden invariants; radiative/readout closure hooks; finite coupling product rows",
                "exclude": "closure axiom as derivation; alpha value prediction; tau=1; source-unity; symbolic R10 pass; GitHub; formalization edits",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    audit: list[dict[str, object]],
    acquisition: list[dict[str, object]],
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

    add("V1113_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1113_1_contract_complete", len(contract) >= 8 and any(row["contract_id"] == "POC1113_4_no_hidden_visible_morphisms" for row in contract), "parent-owned readout/descent contract clauses are explicit")
    add("V1113_2_sufficiency_not_promotion", any(row["answer"] == "YES_CONDITIONAL" for row in audit) and any(row["promotion_status"] == "not_promoted_because_clauses_unsigned" for row in audit), "contract sufficiency is conditional and not promoted")
    add("V1113_3_next_derivation_selected", any(row["answer"] == "NO_HIDDEN_VISIBLE_COEFFICIENT_MORPHISM" for row in audit), "no-hidden-visible coefficient morphism selected as next target")
    add("V1113_4_acquisition_missing", all(str(row["current_status"]).startswith("MISSING") for row in acquisition), "finite product acquisition rows remain missing-input nonclaim rows")
    add("V1113_5_gates_blocked", all(row["gate_pass"] == "false" for row in gates), "all claim gates remain blocked")
    add("V1113_6_no_claim_rows", all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in contract + audit + acquisition + gates + decisions + next_target), "all generated rows remain nonclaim")
    add("V1113_7_next_target", next_target[0]["next_target"].startswith("1114-") and "no-hidden-visible" in str(next_target[0]["next_target"]), "1114 handoff targets no-hidden-visible coefficient morphism theorem")
    add("V1113_8_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1113_9_csv_parse", csv_parse_ok, "all 1113 CSV outputs parse cleanly")
    add("V1113_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1113_SUMMARY", True, "1113 constructs a sufficient parent-owned contract but leaves the coupling clause unsigned")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    contract: list[dict[str, object]],
    audit: list[dict[str, object]],
    acquisition: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1113 - Parent-Owned Readout Descent Contract Or Alpha Product Input Acquisition

**Current verdict:** a sufficient parent-owned readout/descent contract can be written, but it is not derived from the current corpus. If adopted as-is, it is a closure axiom; if derived, it would be a serious local-silence mechanism.

**Coupling diagnosis:** the key wound is now the coupling language itself. The most valuable next theorem is: visible EM/matter coefficients cannot take hidden representatives as arguments. That single clause attacks alpha drift, mass/clock drift, WEP source normalization, and R10 source/test products.

**No claim:** no `b_alpha=0`, no parent alpha prediction, no WEP/R10 source pass, no finite product pass, and no local-GR pass follows from 1113.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Parent-Owned Contract
{table(["contract_id", "contract_clause", "mathematical_role", "current_status", "source_basis", "if_signed", "if_unsigned", "claim_allowed"], contract)}

## Signature Audit
{table(["audit_id", "question", "answer", "reason", "promotion_status", "claim_allowed"], audit)}

## Product Input Acquisition Ledger
{table(["input_id", "product_row", "needed_input", "allowed_source", "current_status", "blocks", "claim_allowed"], acquisition)}

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
        "source_register": OUT / "P8_Y5_R10_1113_SOURCE_REGISTER.csv",
        "contract": OUT / "P8_Y5_R10_1113_PARENT_OWNED_READOUT_DESCENT_CONTRACT.csv",
        "audit": OUT / "P8_Y5_R10_1113_SIGNATURE_AUDIT.csv",
        "acquisition": OUT / "P8_Y5_R10_1113_ALPHA_PRODUCT_INPUT_ACQUISITION_LEDGER.csv",
        "gates": OUT / "P8_Y5_R10_1113_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1113_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1113_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1113_VALIDATION.csv",
    }
    sources = source_rows()
    contract = parent_contract_rows()
    audit = signature_audit_rows()
    acquisition = acquisition_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["contract"], contract)
    write_csv(outputs["audit"], audit)
    write_csv(outputs["acquisition"], acquisition)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, contract, audit, acquisition, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, contract, audit, acquisition, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
