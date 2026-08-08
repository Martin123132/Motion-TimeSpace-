from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3413-Y5-R2FR-response-doublet-Gamma-density-construction-test-under-AX1090.md"

SOURCES = {
    "doc_3412": ROOT / "3412-Y5-R2FR-GammaKhat-symbol-match-extractor-for-Khat-response-under-AX1090.md",
    "next_3412": OUT / "P8_Y5_R2FR_3412_NEXT_TARGET.csv",
    "ranking_3412": OUT / "P8_Y5_R2FR_3412_CONSTRUCTION_CANDIDATE_RANKING.csv",
    "verdict_3412": OUT / "P8_Y5_R2FR_3412_SYMBOL_MATCH_VERDICT.csv",
    "response_tests_3412": OUT / "P8_Y5_R2FR_3412_RESPONSE_PAIR_TEST_MATRIX.csv",
    "doc_516": ROOT / "516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md",
    "doc_517": ROOT / "517-response-doublet-action-variation-ledger-or-run-q_loc-bound.md",
    "doc_493": ROOT / "493-odd-residual-parentization-or-closure-fill.md",
    "doc_494": ROOT / "494-exchange-doublet-component-map-or-coefficient-branch.md",
    "yloc_euler": OUT / "P8_YLOC_EULER_SYSTEM.csv",
    "doublet_ledger": OUT / "P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv",
    "qloc_residual_3064": OUT / "P8_Y5_R2FR_3064_QLOC_RESIDUAL_INTERFACE.csv",
    "r11_beta_vector": OUT / "P8_Y5_R11_BETA_COMPONENT_VECTOR.csv",
    "alpha_bound_3410": OUT / "P8_Y5_R2FR_3410_ALPHA_VECTOR_PRODUCT_BOUND.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3413_SOURCE_REGISTER.csv",
    "response_doublet_action": OUT / "P8_Y5_R2FR_3413_RESPONSE_DOUBLET_ACTION.csv",
    "metric_response_template": OUT / "P8_Y5_R2FR_3413_METRIC_RESPONSE_TEMPLATE.csv",
    "double_zero_proof": OUT / "P8_Y5_R2FR_3413_DOUBLE_ZERO_PROOF.csv",
    "component_coverage_matrix": OUT / "P8_Y5_R2FR_3413_COMPONENT_COVERAGE_MATRIX.csv",
    "source_neutrality_gates": OUT / "P8_Y5_R2FR_3413_SOURCE_NEUTRALITY_GATES.csv",
    "construction_verdict": OUT / "P8_Y5_R2FR_3413_CONSTRUCTION_VERDICT.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3413_PROMOTION_GATES.csv",
    "next_target": OUT / "P8_Y5_R2FR_3413_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3413_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3413_VALIDATION.csv",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_optional(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return read_csv(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fields = list(rows[0].keys())
    clean = lambda value: str(value).replace("\n", " ").replace("|", "/")
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


YLOC_ROWS = load_optional(SOURCES["yloc_euler"])
DOUBLET_LEDGER = load_optional(SOURCES["doublet_ledger"])


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3412": "symbol extractor verdict selecting response-doublet construction",
        "next_3412": "declared 3413 construction target",
        "ranking_3412": "response-doublet ranked first",
        "verdict_3412": "no current match, but construction route retained",
        "response_tests_3412": "current match failed; construction target passed conditionally",
        "doc_516": "Gamma_eff owner candidate and response-doublet contract",
        "doc_517": "response-doublet first-variation and metric-response ledger",
        "doc_493": "odd residual parentization requirements",
        "doc_494": "exchange-doublet component map and Y5/Y6 blocker context",
        "yloc_euler": "Y0-Y6 local Euler component system",
        "doublet_ledger": "Y0-Y6 source problem ledger",
        "qloc_residual_3064": "retained q_loc/Delta_K/H_GK/J_GK/B_GK/P_loc residuals",
        "r11_beta_vector": "local PPN/source/operator residual vector",
        "alpha_bound_3410": "alpha3 pressure bound motivating structural zero",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def response_doublet_action() -> list[dict[str, Any]]:
    return [
        {
            "action_id": "RDA3413_0_doublet_variables",
            "object": "exchange doublets",
            "definition": "R_+^A, R_-^A with Z^A=(R_+^A-R_-^A)/2 and R_even^A=(R_+^A+R_-^A)/2",
            "role": "Z^A is intended to represent odd local residual/leakage directions",
            "claim_status": "FORMAL_VARIABLES_NOT_FULLY_COMPONENT_LOCKED",
            "valid_for_claim": False,
        },
        {
            "action_id": "RDA3413_1_density",
            "object": "Gamma_eff density",
            "definition": "Gamma_eff=Gamma0+1/2 M_AB(g,R_even,D,...) Z^A Z^B+O(Z^4)",
            "role": "even scalar density with no linear Z term",
            "claim_status": "CONSTRUCTION_TEMPLATE",
            "valid_for_claim": False,
        },
        {
            "action_id": "RDA3413_2_action",
            "object": "S_GK",
            "definition": "S_GK=int sqrt(-g) Gamma_eff + int_boundary B_GK, with fixed sign/volume convention still to be locked",
            "role": "would make T_GK a Hilbert stress if adopted and Helmholtz/boundary gates pass",
            "claim_status": "CANDIDATE_PARENT_CLAUSE_NOT_CURRENT_DERIVATION",
            "valid_for_claim": False,
        },
        {
            "action_id": "RDA3413_3_Kmetric",
            "object": "K_metric[Gamma_eff]",
            "definition": "K_metric^{mu nu}:=2/sqrt(-g) delta[sqrt(-g) Gamma_eff]/delta g_{mu nu} plus integration-by-parts boundary terms",
            "role": "defines the Khat target by construction; still must reproduce live K_hat symbols",
            "claim_status": "TARGET_RESPONSE_NOT_MATCHED",
            "valid_for_claim": False,
        },
    ]


def metric_response_template() -> list[dict[str, Any]]:
    return [
        {
            "term_id": "MRT3413_0_volume",
            "variation_piece": "delta sqrt(-g)",
            "schematic_result": "volume term proportional to Gamma_eff g^{mu nu}",
            "order_in_Z": "Gamma0 + O(Z^2)",
            "risk": "Gamma0 must be background/cosmological subtraction, not local source mass",
            "current_status": "CONVENTION_AND_SUBTRACTION_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "term_id": "MRT3413_1_MAB",
            "variation_piece": "delta_g M_AB",
            "schematic_result": "1/2 (delta_g M_AB) Z^A Z^B",
            "order_in_Z": "O(Z^2) if M_AB finite",
            "risk": "M_AB must be parent-owned, covariant, positive and nonsingular",
            "current_status": "FORMAL_SAFE_TO_LINEAR_ORDER_ONLY",
            "valid_for_claim": False,
        },
        {
            "term_id": "MRT3413_2_Z_metric",
            "variation_piece": "delta_g Z^A",
            "schematic_result": "M_AB Z^A delta_g Z^B",
            "order_in_Z": "O(Z) if delta_g Z is finite",
            "risk": "linear metric-response leakage returns if Z/readout/projector variation is singular or source-weighted",
            "current_status": "PPN_READOUT_LOCK_OPEN",
            "valid_for_claim": False,
        },
        {
            "term_id": "MRT3413_3_derivatives_boundary",
            "variation_piece": "derivative, projector, domain and integration-by-parts terms",
            "schematic_result": "boundary/collar/domain response terms B_GK and P_loc commutators",
            "order_in_Z": "can be O(Z) or boundary-supported",
            "risk": "alpha3/source-measure leakage if boundary odd charge or projector flux survives",
            "current_status": "BOUNDARY_PROJECTOR_OPEN",
            "valid_for_claim": False,
        },
        {
            "term_id": "MRT3413_4_live_Khat_compare",
            "variation_piece": "compare K_metric[Gamma_eff] to live K_hat",
            "schematic_result": "Delta_K:=K_hat-K_metric[Gamma_eff]",
            "order_in_Z": "unknown",
            "risk": "construction is only useful if Delta_K=0 or bounded",
            "current_status": "DELTA_K_RETAINED",
            "valid_for_claim": False,
        },
    ]


def double_zero_proof() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "DZ3413_0_value",
            "statement": "At Z=0, Gamma_eff-Gamma0=0.",
            "calculation": "Gamma_eff-Gamma0=1/2 M_AB Z^A Z^B+O(Z^4)",
            "passes_if": "Gamma0 is constant/background-subtracted and Z=0 is the physical local residual state",
            "current_result": "PASS_FORMAL_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "proof_id": "DZ3413_1_first_variation",
            "statement": "The first residual variation vanishes at Z=0.",
            "calculation": "partial Gamma_eff/partial Z^A=M_AB Z^B+O(Z^3), so partial_A Gamma_eff|Z=0=0",
            "passes_if": "no linear source term J_A Z^A or boundary term B_A Z^A is present",
            "current_result": "PASS_FORMAL_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "proof_id": "DZ3413_2_Euler",
            "statement": "The Euler equation can force Z=0 on compact local domains only if the operator is positive and source-free.",
            "calculation": "L_AB Z^B=J_A+B_A; positivity gives Z=0 only when J_A=B_A=0",
            "passes_if": "M_AB/L_AB positive after constraints and every local source/boundary charge vanishes",
            "current_result": "FAIL_CURRENT_SOURCE_NEUTRALITY",
            "valid_for_claim": False,
        },
        {
            "proof_id": "DZ3413_3_physical_lock",
            "statement": "The formal Z zero must be the physical q_loc/PPN/source residual zero.",
            "calculation": "Z^A=Y_loc^A through beta/gamma/alpha_i/xi/Gdot/R11 order",
            "passes_if": "component map covers Y0-Y6 and observed readout/source normalization",
            "current_result": "FAIL_CURRENT_COMPONENT_LOCK",
            "valid_for_claim": False,
        },
    ]


def ledger_status(component_id: str) -> dict[str, str]:
    for row in DOUBLET_LEDGER:
        if row.get("component_id") == component_id:
            return row
    return {}


def coverage_status(component_id: str, y_status: str, variation_status: str) -> tuple[str, str]:
    if component_id in {"Y2_boundary_flux", "Y3_domain_vector"} and "conditional" in variation_status:
        return "CONDITIONAL_ROUTE", "could be covered by odd-boundary/vector zero theorem, not yet parent-signed"
    if component_id == "Y5_source_normalization":
        return "HARD_FAIL_CURRENT", "measured GM/source normalization is exchange-even and not killed by odd quadratic density"
    if component_id == "Y6_stress_Bianchi":
        return "RETAINED_DEBT", "extra conserved stress can be exchange-even and nonzero under Ward/Bianchi ownership"
    if "retained" in y_status or "not_zeroed" in variation_status or "not_parent" in y_status:
        return "NOT_COVERED_CURRENT", "requires a separate theorem or residual bound"
    return "PARTIAL_OR_UNCLEAR", "not enough evidence for claim"


def component_coverage_matrix() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for yrow in YLOC_ROWS:
        component_id = yrow.get("component_id", "")
        ledger = ledger_status(component_id)
        coverage, reason = coverage_status(component_id, yrow.get("current_status", ""), ledger.get("variation_status", ""))
        rows.append(
            {
                "component_id": component_id,
                "Y_component": yrow.get("Y_component", ""),
                "candidate_Euler_equation": yrow.get("candidate_Euler_equation", ""),
                "zero_conditions": yrow.get("zero_conditions", ""),
                "source_problem": ledger.get("source_problem", "MISSING_LEDGER_ROW"),
                "variation_status": ledger.get("variation_status", "MISSING"),
                "doublet_coverage": coverage,
                "reason": reason,
                "valid_for_claim": False,
            }
        )
    return rows or [
        {
            "component_id": "MISSING_YLOC_ROWS",
            "Y_component": "",
            "candidate_Euler_equation": "",
            "zero_conditions": "",
            "source_problem": "P8_YLOC_EULER_SYSTEM missing",
            "variation_status": "MISSING",
            "doublet_coverage": "FAIL",
            "reason": "cannot test coverage",
            "valid_for_claim": False,
        }
    ]


def source_neutrality_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "SNG3413_0_no_linear_J",
            "gate": "No linear source term J_A Z^A appears in the local branch.",
            "needed_for": "double-zero promotion from formal to physical",
            "current_result": "FAIL_FOR_Y5_AND_Y6",
            "blocker": "source normalization and extra stress can be exchange-even",
            "valid_for_claim": False,
        },
        {
            "gate_id": "SNG3413_1_boundary_odd_charge",
            "gate": "Boundary/collar odd charge vanishes.",
            "needed_for": "alpha3/vector silence and no local force flux",
            "current_result": "CONDITIONAL_ONLY",
            "blocker": "Y2 boundary flux and P_loc/boundary terms not parent-signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "SNG3413_2_domain_vector",
            "gate": "Domain vector is absent, topological, pure gauge, or dynamically zero.",
            "needed_for": "alpha1/alpha2/alpha3/xi silence",
            "current_result": "CONDITIONAL_ONLY",
            "blocker": "Y3 domain vector no-source theorem not parent-signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "SNG3413_3_physical_residual_lock",
            "gate": "Z^A equals the physical q_loc and local residual basis, not an auxiliary shadow.",
            "needed_for": "q_loc local-GR promotion",
            "current_result": "FAIL_CURRENT",
            "blocker": "Y0-Y6 component map and PPN/source-normalization readout are not fully locked",
            "valid_for_claim": False,
        },
        {
            "gate_id": "SNG3413_4_positive_operator",
            "gate": "M_AB/L_AB is positive after gauge/constraint quotient.",
            "needed_for": "Z=0 no-hair from energy identity",
            "current_result": "UNSIGNED",
            "blocker": "operator positivity and constraint quotient not supplied",
            "valid_for_claim": False,
        },
    ]


def construction_verdict() -> list[dict[str, Any]]:
    return [
        {
            "verdict_id": "CV3413_0_formal_double_zero",
            "question": "Does the response-doublet density prove F1=0 formally?",
            "answer": "YES_CONDITIONALLY",
            "evidence": "Gamma_eff-Gamma0=O(Z^2) and partial_A Gamma_eff|Z=0=0",
            "claim_effect": "good mechanism shape, not a current MTS promotion",
            "valid_for_claim": False,
        },
        {
            "verdict_id": "CV3413_1_component_coverage",
            "question": "Does it cover the live q_loc/Y0-Y6 residual basis?",
            "answer": "NO_NOT_CURRENTLY",
            "evidence": "Y5 source normalization hard-fails and Y6 extra stress remains retained debt; several other Y rows are conditional/open",
            "claim_effect": "q_loc/local-GR remains blocked",
            "valid_for_claim": False,
        },
        {
            "verdict_id": "CV3413_2_metric_response",
            "question": "Does it match the existing live K_hat symbols?",
            "answer": "NO_MATCH_NOT_PROVED",
            "evidence": "construction defines a K_metric target but Delta_K remains retained unless live symbols match it",
            "claim_effect": "cannot claim Ward-zero route yet",
            "valid_for_claim": False,
        },
        {
            "verdict_id": "CV3413_3_best_next",
            "question": "What is the next derivation-first target?",
            "answer": "Y5_SOURCE_NORMALIZATION_AND_Y6_EXTRA_STRESS_OWNER_GATE",
            "evidence": "these are the hard rows that stop formal double-zero from becoming physical local GR",
            "claim_effect": "attack source coupling/Newton normalization instead of looping on q_loc algebra",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3413_0_formal_double_zero",
            "gate": "response-doublet density gives F1=0 at Z=0",
            "current_result": "PASS_FORMAL_CONDITIONAL",
            "promotes_if": "not a claim gate",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3413_1_component_coverage",
            "gate": "Z^A covers all physical local residual components Y0-Y6",
            "current_result": "FAIL_Y5_Y6_AND_OPEN_ROWS",
            "promotes_if": "Y0-Y6 all become theorem-zero/source-neutral or explicitly bounded",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3413_2_metric_response_match",
            "gate": "K_metric from constructed density equals live K_hat",
            "current_result": "FAIL_DELTA_K_RETAINED",
            "promotes_if": "Delta_K=0 by symbol match or is bounded below local locks",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3413_3_source_neutrality",
            "gate": "linear source/boundary terms J_A and B_A vanish",
            "current_result": "FAIL_Y5_SOURCE_AND_Y6_STRESS",
            "promotes_if": "source-normalization and extra-stress owner theorems pass",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3413_4_q_loc_local_GR",
            "gate": "q_loc no longer blocks local GR",
            "current_result": "BLOCKED",
            "promotes_if": "PG3413_1, PG3413_2 and PG3413_3 pass",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3414-Y5-R2FR-Y5-source-normalization-and-Y6-extra-stress-owner-gate-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3414_Y5_source_normalization_and_Y6_extra_stress_owner_gate.py",
            "objective": "try to prove that measured-GM source normalization and extra Bianchi-owned stress are either EH-only/even-public objects or vanish/topological in the response-doublet parent branch",
            "why_next": "3413 shows the formal double-zero works, but Y5 and Y6 are the hard rows preventing physical q_loc/local-GR promotion",
            "valid_for_claim": False,
        },
        {
            "target_id": "3415-Y5-R2FR-q_loc-residual-bound-demotion-after-Y5Y6-failure-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3415_q_loc_residual_bound_demotion_after_Y5Y6_failure.py",
            "objective": "if Y5/Y6 cannot be theorem-zeroed, demote q_loc to explicit residual components and source-backed empirical bound rows",
            "why_next": "this prevents the response-doublet construction from becoming a hidden closure assumption",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3413_0",
            "script": str(Path(__file__).resolve()),
            "claim_status": "FORMAL_CONSTRUCTION_TEST_ONLY",
            "main_result": "response-doublet density gives formal F1=0 but does not cover Y5/Y6 or live Khat match",
            "valid_for_claim": False,
        }
    ]


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = generated["source_register"]
    coverage_rows = generated["component_coverage_matrix"]
    verdict_rows = generated["construction_verdict"]
    gates = generated["promotion_gates"]
    output_paths = list(OUTPUTS.values()) + [DOC]
    source_exists = all(str(row["exists"]).lower() == "true" for row in source_rows)
    no_workbench = all("formalization-workbench" not in str(path) for path in output_paths)
    all_nonclaim = all(
        str(row.get("valid_for_claim", "False")).lower() == "false"
        for rows in generated.values()
        for row in rows
    )
    y_rows_complete = {row.get("component_id") for row in coverage_rows} >= {
        "Y0_trace_expansion",
        "Y1_coherent_projector",
        "Y2_boundary_flux",
        "Y3_domain_vector",
        "Y4_domain_STF_stress",
        "Y5_source_normalization",
        "Y6_stress_Bianchi",
    }
    y5_hard = any(row.get("component_id") == "Y5_source_normalization" and row.get("doublet_coverage") == "HARD_FAIL_CURRENT" for row in coverage_rows)
    y6_debt = any(row.get("component_id") == "Y6_stress_Bianchi" and row.get("doublet_coverage") == "RETAINED_DEBT" for row in coverage_rows)
    formal_pass = any(row.get("verdict_id") == "CV3413_0_formal_double_zero" and row.get("answer") == "YES_CONDITIONALLY" for row in verdict_rows)
    blocked = any(row.get("gate_id") == "PG3413_4_q_loc_local_GR" and row.get("current_result") == "BLOCKED" for row in gates)
    next_y5y6 = "Y5-source-normalization" in generated["next_target"][0]["target_id"]
    rows = [
        {
            "check_id": "VAL3413_0_sources_exist",
            "check": "every cited local source path exists",
            "passed": source_exists,
            "detail": f"{sum(str(row['exists']).lower() == 'true' for row in source_rows)}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3413_1_scope",
            "check": "no output path targets formalization-workbench",
            "passed": no_workbench,
            "detail": "all outputs are under post-checkpoint-work",
        },
        {
            "check_id": "VAL3413_2_all_nonclaim",
            "check": "all rows keep valid_for_claim=false",
            "passed": all_nonclaim,
            "detail": "3413 is a formal construction test, not a claim",
        },
        {
            "check_id": "VAL3413_3_formal_double_zero",
            "check": "formal double-zero proof is present",
            "passed": formal_pass,
            "detail": "CV3413_0 passes conditionally",
        },
        {
            "check_id": "VAL3413_4_component_coverage",
            "check": "Y0-Y6 coverage matrix is complete",
            "passed": y_rows_complete,
            "detail": f"{len(coverage_rows)} Y rows written",
        },
        {
            "check_id": "VAL3413_5_hard_rows_retained",
            "check": "Y5/Y6 hard blockers are not hidden",
            "passed": y5_hard and y6_debt,
            "detail": "Y5 HARD_FAIL_CURRENT and Y6 RETAINED_DEBT",
        },
        {
            "check_id": "VAL3413_6_q_loc_blocked",
            "check": "q_loc local-GR promotion remains blocked",
            "passed": blocked,
            "detail": "PG3413_4_q_loc_local_GR remains BLOCKED",
        },
        {
            "check_id": "VAL3413_7_next_target",
            "check": "next target attacks Y5/Y6 instead of circling q_loc",
            "passed": next_y5y6,
            "detail": generated["next_target"][0]["target_id"],
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "check_id": "VAL3413_8_overall",
            "check": "3413 response-doublet construction test is internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return rows


def build_doc(generated: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join(
        [
            "# 3413 - Response-Doublet Gamma Density Construction Test",
            "## Summary\n"
            "- This checkpoint tests the best derivation-first repair from 3412: a response-doublet `Gamma_eff` density.\n"
            "- The formal double-zero works: `Gamma_eff-Gamma0=O(Z^2)` and `partial_A Gamma_eff|Z=0=0`.\n"
            "- The physical construction does not close yet because `Z^A` is not locked to every local residual component and the hard rows `Y5_source_normalization` and `Y6_stress_Bianchi` survive.\n"
            "- Therefore q_loc is not promoted, but the next bottleneck is sharper: source normalization and extra-stress ownership.",
            "## Response-Doublet Action\n" + md_table(generated["response_doublet_action"]),
            "## Metric-Response Template\n" + md_table(generated["metric_response_template"]),
            "## Double-Zero Proof\n" + md_table(generated["double_zero_proof"]),
            "## Component Coverage Matrix\n" + md_table(generated["component_coverage_matrix"]),
            "## Source Neutrality Gates\n" + md_table(generated["source_neutrality_gates"]),
            "## Construction Verdict\n" + md_table(generated["construction_verdict"]),
            "## Promotion Gates\n" + md_table(generated["promotion_gates"]),
            "## Next Target\n" + md_table(generated["next_target"]),
            "## Runner Nonclaim\n" + md_table(generated["runner_nonclaim"]),
            "## Validation\n" + md_table(generated["validation"]),
            "## Bottom Line\n"
            "The response-doublet idea is not empty theatre: it gives the right formal zero mechanism. But it does not yet solve source coupling. "
            "The real next fight is Y5/Y6: measured-GM normalization and extra conserved stress. That is exactly the Newton/GR coupling hinge.",
        ]
    ) + "\n"


def main() -> None:
    if "formalization-workbench" in str(ROOT):
        raise RuntimeError(f"Refusing to run from formalization-workbench: {ROOT}")

    generated: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "response_doublet_action": response_doublet_action(),
        "metric_response_template": metric_response_template(),
        "double_zero_proof": double_zero_proof(),
        "component_coverage_matrix": component_coverage_matrix(),
        "source_neutrality_gates": source_neutrality_gates(),
        "construction_verdict": construction_verdict(),
        "promotion_gates": promotion_gates(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    generated["validation"] = validation_rows(generated)

    for key, rows in generated.items():
        write_csv(OUTPUTS[key], rows)

    DOC.write_text(build_doc(generated), encoding="utf-8")

    if not all(str(row["passed"]).lower() == "true" for row in generated["validation"]):
        failed = [row for row in generated["validation"] if str(row["passed"]).lower() != "true"]
        raise SystemExit(f"3413 validation failed: {failed}")

    print(f"wrote {len(generated)} CSV artefacts and {DOC}")


if __name__ == "__main__":
    main()
