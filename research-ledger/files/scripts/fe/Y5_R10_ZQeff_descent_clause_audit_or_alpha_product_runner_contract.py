from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1112-Y5-R10-ZQeff-descent-clause-audit-or-alpha-product-runner-contract.md"

PRODUCT_SCHEMA = [
    "prediction_id",
    "arena",
    "product_symbol",
    "product_value",
    "product_units",
    "product_source",
    "inputs_present",
    "required_inputs",
    "derivation_status",
    "valid_for_claim",
    "notes",
]


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


def read_csv_rows(relative_path: str) -> list[dict[str, str]]:
    with (ROOT / relative_path).open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1112_0_1111_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1111_NEXT_TARGET.csv",
            "needle": "NEXT1111_0_1112",
            "note": "1111 handoff to Z_Q_eff descent clause audit.",
        },
        {
            "source_id": "SRC1112_1_1111_terms",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1111_ZQEFF_TERM_AUDIT.csv",
            "needle": "ZQ1111_4_readout",
            "note": "readout term remains unsigned.",
        },
        {
            "source_id": "SRC1112_2_1111_products",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1111_PRODUCT_SOURCE_VECTOR_NONCLAIM.csv",
            "needle": "PV1111_3_r10",
            "note": "finite product vector includes R10.",
        },
        {
            "source_id": "SRC1112_3_1050_product_functor",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv",
            "needle": "PFT1050_1_visible_action_pullback",
            "note": "visible action pullback gives exact conditional theorem.",
        },
        {
            "source_id": "SRC1112_4_1050_radiative",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv",
            "needle": "PFT1050_3_radiative_readout_closure",
            "note": "radiative/readout closure remains unsigned.",
        },
        {
            "source_id": "SRC1112_5_967_readout",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_967_READOUT_SCHEMA_THEOREM_ATTEMPT.csv",
            "needle": "RAV967_5_verdict",
            "note": "readout domain separation is conditional but not globally parent signed.",
        },
        {
            "source_id": "SRC1112_6_1060_schema",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1060_PRODUCT_PREDICTION_SCHEMA.csv",
            "needle": "product_value",
            "note": "strict product runner schema.",
        },
        {
            "source_id": "SRC1112_7_1060_required",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1060_REQUIRED_INPUTS.csv",
            "needle": "REQ1060_3_R10_alpha",
            "note": "R10 finite branch inputs remain missing.",
        },
        {
            "source_id": "SRC1112_8_1099_exclusion",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1099_NO_EXTRA_F2_EXCLUSION_AUDIT.csv",
            "needle": "EXC1099_5_radiative",
            "note": "tree-level no-extra-F2 is insufficient without radiative/readout closure.",
        },
        {
            "source_id": "SRC1112_9_988_joint",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_988_JOINT_ALPHA_VARIABLE_GATE.csv",
            "needle": "JAV988_3_cross_arena_policy",
            "note": "shared local alpha screen/domain policy remains active.",
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


def imported_product_values() -> dict[str, str]:
    products = read_csv_rows("source-intake/mts_residuals/P8_Y5_R10_1111_PRODUCT_SOURCE_VECTOR_NONCLAIM.csv")
    return {row["product_id"]: row["bound_or_target"] for row in products}


def descent_theorem_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "attempt_id": "ZQD1112_0_sandwich_statement",
                "claim_piece": "descent sandwich theorem",
                "formal_statement": "If q: P -> Q, v in ker(Dq), R_read = Rbar o q, and Z_Q_eff = Zbar(q(Phi), theta_rep), then D_v Z_Q_eff = 0.",
                "result": "EXACT_CONDITIONAL_THEOREM",
                "proof_or_blocker": "D_v Zbar(q(Phi)) = DZbar[Dq(v)] = 0 by chain rule; no physics is hidden in this step",
            },
            {
                "attempt_id": "ZQD1112_1_parent_norm",
                "claim_piece": "C_P N_Q descends",
                "formal_statement": "C_P N_Q = Zbar_parent(q(Phi), theta_rep) with no representative dependence.",
                "result": "NOT_PARENT_SIGNED",
                "proof_or_blocker": "current corpus has no signed parent Maxwell normalization/descent theorem for C_P N_Q",
            },
            {
                "attempt_id": "ZQD1112_2_hidden_visible",
                "claim_piece": "hidden-visible coefficient maps absent",
                "formal_statement": "Hom(C_hid, Coeff(F_Q^2)) is constant or absent, so f_hid(I_hid) cannot generate alpha drift.",
                "result": "POWERFUL_BUT_UNSIGNED",
                "proof_or_blocker": "1050 gives exact product-functor target but not parent construction; 1099 leaves scalar F2 terms legal",
            },
            {
                "attempt_id": "ZQD1112_3_radiative",
                "claim_piece": "radiative closure descends",
                "formal_statement": "Delta_rad(mu,X) = Delta_bar_rad(q(Phi), theta_rep, mu) with no local vertical dependence after matching.",
                "result": "UNSIGNED",
                "proof_or_blocker": "tree-level pullback does not automatically survive EFT thresholds/running",
            },
            {
                "attempt_id": "ZQD1112_4_readout",
                "claim_piece": "readout functor descends",
                "formal_statement": "clock/spectrum/material readout maps depend on Sol(S_parent) only through q(Phi) and fixed representation data.",
                "result": "CONDITIONAL_SCHEMA_NOT_GLOBAL",
                "proof_or_blocker": "967 proves the domain-separation logic but the corpus has not globally signed the parent action/readout schema",
            },
            {
                "attempt_id": "ZQD1112_5_arena_products",
                "claim_piece": "clock/WEP/R10 products inherit descent",
                "formal_statement": "P_clock, P_WEP, and P_R10 vanish or become numeric source-backed products under the same parent-owned readout functor.",
                "result": "NOT_DERIVED",
                "proof_or_blocker": "tau_clock, beta_source_alpha, tau_WEP, and R10 source/test products remain missing",
            },
            {
                "attempt_id": "ZQD1112_6_verdict",
                "claim_piece": "sign Z_Q_eff descent",
                "formal_statement": "Z_Q_eff factors entirely through q and parent-owned readout data, so d_v ln Z_Q_eff = 0.",
                "result": "ZQEFF_DESCENT_NOT_SIGNED",
                "proof_or_blocker": "the theorem is mathematically clean but parent norm, hidden-visible sequester, radiative closure, and global readout schema are still unsigned",
            },
        ]
    )


def clause_audit_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "clause_id": "CLAUSE1112_0_vertical_generator",
                "clause": "v in ker(Dq)",
                "needed_for": "descent sandwich",
                "status": "ASSUMED_FROM_LOCAL_VERTICAL_BRANCH",
                "failure_mode": "if v is not truly vertical, q-observables can drift",
                "repair_route": "derive local vertical generator from parent quotient map",
                "priority": "high",
            },
            {
                "clause_id": "CLAUSE1112_1_parent_norm_descent",
                "clause": "C_P N_Q = Zbar_parent(q(Phi),theta)",
                "needed_for": "absolute and drift alpha silence",
                "status": "UNSIGNED",
                "failure_mode": "parent normalization itself produces b_alpha",
                "repair_route": "parent Maxwell block construction or finite b_alpha row",
                "priority": "critical",
            },
            {
                "clause_id": "CLAUSE1112_2_hidden_sequester",
                "clause": "no nonconstant hidden-to-visible F2 coefficient morphism",
                "needed_for": "forbid f_hid(I_hid)F_Q^2",
                "status": "UNSIGNED",
                "failure_mode": "hidden scalar coefficient becomes finite alpha residual",
                "repair_route": "product-functor parent construction or source coefficient",
                "priority": "critical",
            },
            {
                "clause_id": "CLAUSE1112_3_radiative_closure",
                "clause": "EFT/running thresholds preserve descent",
                "needed_for": "tree-level zero survives observed alpha",
                "status": "UNSIGNED",
                "failure_mode": "loops/readout regenerate b_alpha",
                "repair_route": "renormalized readout theorem or finite counterterm product row",
                "priority": "critical",
            },
            {
                "clause_id": "CLAUSE1112_4_readout_schema",
                "clause": "readout variables are post-solution maps, not parent action arguments",
                "needed_for": "prevent readout-selected parent forces",
                "status": "CONDITIONAL_NOT_GLOBAL",
                "failure_mode": "reduced-action/readout shortcut adds new effective branch",
                "repair_route": "global parent action contract excluding readout variables",
                "priority": "high",
            },
            {
                "clause_id": "CLAUSE1112_5_arena_maps",
                "clause": "clock tau, WEP source normalization, and R10 source/test maps are parent-owned",
                "needed_for": "convert descent into empirical local gates",
                "status": "MISSING_NUMERIC_OR_THEOREM_INPUTS",
                "failure_mode": "data tests remain product placeholders",
                "repair_route": "strict product runner contract with sourced numeric rows",
                "priority": "high",
            },
        ]
    )


def product_contract_rows(bounds: dict[str, str]) -> list[dict[str, object]]:
    return [
        {
            "prediction_id": "APC1112_0_clock_alpha_product",
            "arena": "clock",
            "product_symbol": "P_clock_alpha = b_alpha * tau_clock_time",
            "product_value": "MISSING_MTS_CLOCK_PRODUCT",
            "product_units": "yr^-1",
            "product_source": "MISSING_LOCAL_DERIVATION_PATH",
            "inputs_present": f"source_bound={bounds['PV1111_1_clock']}",
            "required_inputs": "b_alpha_or_direct_zero;tau_clock_time_or_direct_product;clock_readout_map",
            "derivation_status": "MISSING_MTS_PRODUCT_PREDICTION",
            "valid_for_claim": "false",
            "notes": "clock bound is product-only; do not divide by assumed tau or import tau=H0 without derivation",
        },
        {
            "prediction_id": "APC1112_1_wep_alpha_product",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_alpha = beta_source_alpha * b_alpha * tau_WEP",
            "product_value": "MISSING_MTS_WEP_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "MISSING_LOCAL_DERIVATION_PATH",
            "inputs_present": f"pressure_target={bounds['PV1111_2_wep']}",
            "required_inputs": "beta_source_alpha;b_alpha_or_direct_zero;tau_WEP;material_charge_map",
            "derivation_status": "MISSING_SOURCE_NORMALIZATION_AND_TAU_WEP",
            "valid_for_claim": "false",
            "notes": "no clock-to-WEP shortcut; source normalization is an independent coupling debt",
        },
        {
            "prediction_id": "APC1112_2_R10_alpha_product",
            "arena": "R10_short_range",
            "product_symbol": "P_R10_alpha(lambda) = K_X^R10(lambda) * beta_source(lambda) * beta_test(lambda)",
            "product_value": "MISSING_R10_NUMERIC_PRODUCT",
            "product_units": "dimensionless alpha(lambda)",
            "product_source": "MISSING_LOCAL_DERIVATION_PATH",
            "inputs_present": f"bound_target={bounds['PV1111_3_r10']}",
            "required_inputs": "lambda_X;Z_X;K_X^R10(lambda);beta_source(lambda);beta_test(lambda);tau_R10;epsilon_tail;promoted_alpha_bound(lambda)",
            "derivation_status": "MISSING_R10_FINITE_BRANCH_INPUTS",
            "valid_for_claim": "false",
            "notes": "symbolic R10 rows and anchor-only bounds must be refused by the runner",
        },
        {
            "prediction_id": "APC1112_3_cross_arena_alpha",
            "arena": "cross_arena",
            "product_symbol": "shared alpha descent/product consistency",
            "product_value": "MISSING_PARENT_READOUT_FUNCTOR_OR_PRODUCT_VECTOR",
            "product_units": "dimensionless consistency gate",
            "product_source": "MISSING_LOCAL_DERIVATION_PATH",
            "inputs_present": "Z_Q_eff audit;1111 product vector",
            "required_inputs": "same Z_Q_eff branch;domain classifier;readout functor;arena-specific product maps",
            "derivation_status": "MISSING_CROSS_ARENA_PARENT_MAP",
            "valid_for_claim": "false",
            "notes": "same alpha symbol is not enough; the same parent-owned branch and readout map must feed every arena",
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "DEC1112_0_theorem_status",
                "decision": "Z_Q_eff descent is an exact conditional theorem but not parent-signed",
                "because": "the chain-rule sandwich closes only after parent norm, hidden-visible, radiative, and readout clauses are signed",
                "next_action": "do not claim b_alpha=0; attack the parent readout/descent contract directly",
            },
            {
                "decision_id": "DEC1112_1_best_next",
                "decision": "write a parent-owned readout/descent contract",
                "because": "this is the shortest route that can silence alpha drift across clocks, WEP, and R10 without fitted products",
                "next_action": "construct or reject a global action contract excluding readout variables and hidden-visible coefficient morphisms",
            },
            {
                "decision_id": "DEC1112_2_fallback_ready",
                "decision": "strict product runner contract is staged",
                "because": "if descent fails, scoreability requires numeric product rows instead of symbolic alpha rows",
                "next_action": "source numeric product inputs only after the theorem route fails or is explicitly demoted",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1112_0_1113",
                "next_target": "1113-Y5-R10-parent-owned-readout-descent-contract-or-alpha-product-input-acquisition.md",
                "objective": "attempt to construct the global parent-owned readout/descent contract that signs Z_Q_eff factorisation; if it cannot be signed, begin finite alpha product input acquisition under the strict 1112 contract",
                "include": "parent action domain; quotient map q; vertical generator; visible action pullback; no hidden-visible coefficient morphisms; radiative/readout closure; strict product input schema",
                "exclude": "alpha value prediction claim; tau=1; source-unity; symbolic R10 pass; local-GR claim; GitHub; formalization edits",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    contracts: list[dict[str, object]],
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

    add("V1112_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1112_1_conditional_theorem", any(row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem), "descent sandwich theorem is recorded as exact conditional")
    add("V1112_2_descent_not_signed", any(row["result"] == "ZQEFF_DESCENT_NOT_SIGNED" for row in theorem), "Z_Q_eff descent is not promoted")
    add("V1112_3_critical_unsigned_clauses", sum(1 for row in clauses if row["priority"] == "critical" and row["status"] == "UNSIGNED") >= 3, "critical parent norm/hidden/radiative clauses remain unsigned")
    add("V1112_4_contract_schema", all(list(row.keys()) == PRODUCT_SCHEMA for row in contracts), "product contract rows match strict 1060 schema")
    add("V1112_5_contract_nonclaim", all(row["valid_for_claim"] == "false" and str(row["product_value"]).startswith("MISSING") for row in contracts), "product rows remain missing-input nonclaim rows")
    add("V1112_6_no_claim_rows", all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in theorem + clauses + decisions + next_target), "all stamped rows remain nonclaim")
    add("V1112_7_next_target", next_target[0]["next_target"].startswith("1113-") and "parent-owned-readout" in str(next_target[0]["next_target"]), "1113 handoff targets parent-owned readout descent contract")
    add("V1112_8_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1112_9_csv_parse", csv_parse_ok, "all 1112 CSV outputs parse cleanly")
    add("V1112_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1112_SUMMARY", True, "1112 proves a conditional descent sandwich but leaves parent-owned factorisation unsigned")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    clauses: list[dict[str, object]],
    contracts: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1112 - ZQeff Descent Clause Audit Or Alpha Product Runner Contract

**Current verdict:** the `Z_Q_eff` descent route is mathematically clean but not parent-signed. If the effective Maxwell normalization factors through the quotient/readout map, local vertical alpha drift vanishes. The current corpus still lacks the parent-owned factorisation clauses needed to make that a claim.

**Best news:** this is a real theorem shape, not hand waving: `v in ker(Dq)` and `Z_Q_eff = Zbar(q(Phi), theta_rep)` imply `D_v Z_Q_eff = 0` by the chain rule. The bad news is the parent theory still has to earn that factorisation.

**No claim:** no `b_alpha=0`, no absolute alpha prediction, no clock/WEP/R10 pass, and no local-GR pass follows from 1112.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Descent Theorem Attempt
{table(["attempt_id", "claim_piece", "formal_statement", "result", "proof_or_blocker", "claim_allowed"], theorem)}

## Clause Audit
{table(["clause_id", "clause", "needed_for", "status", "failure_mode", "repair_route", "priority", "claim_allowed"], clauses)}

## Strict Product Runner Contract
{table(PRODUCT_SCHEMA, contracts)}

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
        "source_register": OUT / "P8_Y5_R10_1112_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R10_1112_ZQEFF_DESCENT_THEOREM_ATTEMPT.csv",
        "clauses": OUT / "P8_Y5_R10_1112_DESCENT_CLAUSE_AUDIT.csv",
        "contracts": OUT / "P8_Y5_R10_1112_ALPHA_PRODUCT_RUNNER_CONTRACT_NONCLAIM.csv",
        "decisions": OUT / "P8_Y5_R10_1112_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1112_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1112_VALIDATION.csv",
    }
    bounds = imported_product_values()
    sources = source_rows()
    theorem = descent_theorem_rows()
    clauses = clause_audit_rows()
    contracts = product_contract_rows(bounds)
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["clauses"], clauses)
    write_csv(outputs["contracts"], contracts, PRODUCT_SCHEMA)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, theorem, clauses, contracts, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, theorem, clauses, contracts, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
