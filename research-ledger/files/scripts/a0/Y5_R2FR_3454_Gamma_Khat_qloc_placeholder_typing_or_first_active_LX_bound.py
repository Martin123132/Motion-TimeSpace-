from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3454-Y5-R2FR-Gamma-Khat-q_loc-placeholder-typing-or-first-active-LX-bound-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "script_3454": Path(__file__).resolve(),
    "doc_3453": ROOT / "3453-Y5-R2FR-MTS-residual-action-placeholder-expansion-or-first-LX-bound-input-under-AX1090.md",
    "next_3453": OUT / "P8_Y5_R2FR_3453_NEXT_TARGET.csv",
    "placeholder_3453": OUT / "P8_Y5_R2FR_3453_PLACEHOLDER_EXPANSION_MATRIX.csv",
    "first_lx_3453": OUT / "P8_Y5_R2FR_3453_FIRST_LX_BOUND_INPUT.csv",
    "gk_contract": OUT / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
    "gk_rewrite": OUT / "P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv",
    "gk_gates": OUT / "P8_GAMMA_KHAT_QLOC_GATE_TESTS.csv",
    "gk_integrability": OUT / "P8_GAMMA_KHAT_QLOC_INTEGRABILITY_GATES.csv",
    "gamma_owner": OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
    "symbol_match": OUT / "P8_Y5_R10_1281_GAMMA_KHAT_SYMBOL_MATCH_AUDIT.csv",
    "owner_audit": OUT / "P8_Y5_R10_1284_GAMMA_KHAT_OWNER_EXTRACTION_AUDIT.csv",
    "metric_response": OUT / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
    "proof_gate_3064": OUT / "P8_Y5_R2FR_3064_GAMMAKHAT_QLOC_PROOF_GATE.csv",
    "qnorm_bound_1371": OUT / "P8_Y5_R10_1371_CQGAMMA_NORM_BOUND_INPUT_TABLE.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3454_SOURCE_REGISTER.csv",
    "gk_placeholder_typing": OUT / "P8_Y5_R2FR_3454_GK_PLACEHOLDER_TYPING.csv",
    "metric_response_status": OUT / "P8_Y5_R2FR_3454_METRIC_RESPONSE_STATUS.csv",
    "first_active_lx_bound_input": OUT / "P8_Y5_R2FR_3454_FIRST_ACTIVE_LX_BOUND_INPUT.csv",
    "q_loc_residual_interface": OUT / "P8_Y5_R2FR_3454_QLOC_RESIDUAL_INTERFACE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3454_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3454_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3454_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3454_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3454_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "script_3454": "generator for this checkpoint",
        "doc_3453": "immediate handoff: type Gamma/Khat/q_loc placeholders",
        "next_3453": "machine-readable 3454 target",
        "placeholder_3453": "active S_MTS[psi,Gamma,...] placeholder",
        "first_lx_3453": "first L_X zero input and active remainder",
        "gk_contract": "Gamma/Khat/q_loc first-variation contract",
        "gk_rewrite": "q_loc as projected divergence of T_GK",
        "gk_gates": "prior gate tests",
        "gk_integrability": "integrability/action gates",
        "gamma_owner": "candidate action routes for Gamma_eff",
        "symbol_match": "symbol match audit for Gamma_eff/K_hat",
        "owner_audit": "owner extraction audit",
        "metric_response": "metric-response ledger",
        "proof_gate_3064": "later proof-gate audit",
        "qnorm_bound_1371": "q_loc/Cassini gamma bound input schema",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def gk_placeholder_typing() -> list[dict[str, Any]]:
    return [
        {
            "typing_id": "GKT3454_0_Gamma_qbasic_constant",
            "symbol": "Gamma_eff",
            "candidate_type": "q-basic constant/scalar density",
            "typing_rule": "Gamma_eff=Gamma_bar(q(Phi)) or fixed local reference constant",
            "vXrep_result": "delta_vXrep Gamma_eff=0",
            "classification": "THEOREM_ZERO_IF_SOURCE_SIGNED",
            "current_evidence_status": "not the live Gamma/Khat route unless formula is supplied",
            "feeds": "FLX3453_0 q-basic zero subblock",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "typing_id": "GKT3454_1_Gamma_metric_response_density",
            "symbol": "Gamma_eff",
            "candidate_type": "active variational scalar density S_GK",
            "typing_rule": "S_GK=-int sqrt(-g) Gamma_eff[g,Phi,nablaPhi,D,...]",
            "vXrep_result": "active unless Gamma_eff field content is q-basic or source-free double-zero",
            "classification": "ACTIVE_VARIATIONAL_CANDIDATE_NOT_PROMOTED",
            "current_evidence_status": "candidate route exists; live formula/units/field content are missing",
            "feeds": "first active L_X/q_loc bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "typing_id": "GKT3454_2_Khat_metric_response",
            "symbol": "K_hat^{mu nu}",
            "candidate_type": "metric response of Gamma_eff",
            "typing_rule": "K_hat^{mu nu}=2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_{mu nu} plus derivative/boundary convention",
            "vXrep_result": "safe only if K_hat equals K_metric in the same convention",
            "classification": "ACTIVE_METRIC_RESPONSE_GAP",
            "current_evidence_status": "not matched to current symbols; Delta_K retained",
            "feeds": "Delta_K residual interface",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "typing_id": "GKT3454_3_response_doublet_even_density",
            "symbol": "Gamma_eff response doublet",
            "candidate_type": "even quadratic density in exchange-odd residuals",
            "typing_rule": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "vXrep_result": "first variation zero at Z=0 if Z is the local active residual and Khat is matched",
            "classification": "BEST_FORMAL_DOUBLE_ZERO_CANDIDATE_NOT_LIVE",
            "current_evidence_status": "physical q_loc component map/source-free theorem not supplied",
            "feeds": "future double-zero proof or retained q_F1_defect",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "typing_id": "GKT3454_4_q_loc_residual",
            "symbol": "q_loc^nu",
            "candidate_type": "projected divergence residual, not fundamental field",
            "typing_rule": "q_loc^nu=P_loc nabla_mu(Gamma_eff g^{mu nu}-K_hat^{mu nu})",
            "vXrep_result": "retained residual unless S_GK/Khat/Euler/double-zero/P_loc/boundary clauses close",
            "classification": "EXPLICIT_ACTIVE_RESIDUAL_INTERFACE",
            "current_evidence_status": "algebraic rewrite passes; zero theorem not promoted",
            "feeds": "q_loc norm and PPN/source-normalization bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "typing_id": "GKT3454_5_plateau_and_bookkeeping",
            "symbol": "Gamma/Khat/q_loc shortcut",
            "candidate_type": "plateau axiom or bookkeeping stress",
            "typing_rule": "set q_loc=0 or treat Gamma/Khat as stress without action",
            "vXrep_result": "forbidden",
            "classification": "REJECTED_NOT_A_THEORY_ROUTE",
            "current_evidence_status": "explicitly rejected by 1010 and 513 gates",
            "feeds": "none",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def metric_response_status() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "MRS3454_0_volume_piece",
            "component": "Gamma_eff g^{mu nu}",
            "current_status": "FORMAL_KNOWN",
            "gap": "sign and volume convention must be locked to K_hat convention",
            "residual_if_open": "q_metric_response_defect",
            "source_path": str(SOURCES["metric_response"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "MRS3454_1_derivative_terms",
            "component": "metric response of nabla/Hodge/domain/projector dependence",
            "current_status": "OPEN",
            "gap": "derivative and boundary terms from Gamma_eff are not compared to live K_hat",
            "residual_if_open": "Delta_K_derivative_boundary",
            "source_path": str(SOURCES["metric_response"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "MRS3454_2_Khat_match",
            "component": "Delta_K^{mu nu}=K_hat^{mu nu}-K_metric^{mu nu}",
            "current_status": "MISSING_EXPLICIT_GAMMA_KGAMMA_MATCH",
            "gap": "no tensor component comparison with source path",
            "residual_if_open": "Delta_K_active",
            "source_path": str(SOURCES["symbol_match"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "status_id": "MRS3454_3_verdict",
            "component": "Gamma/Khat metric-response identity",
            "current_status": "NOT_PROMOTED",
            "gap": "Gamma formula, Khat tensor, variation computation and Delta_K ledger are missing",
            "residual_if_open": "q_loc retained",
            "source_path": str(OUTPUTS["metric_response_status"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def first_active_lx_bound_input() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "GKB3454_0_q_loc_norm_bound",
            "feeds": "LXB3452_0_explicit_Xrep_bulk;OB3449_0_surface_norm_bound;CQN1371_5_qloc_norm",
            "active_symbol": "q_loc^nu",
            "bound_formula": "Q_norm := ||P_loc nabla_mu(Gamma_eff g^{mu nu}-K_hat^{mu nu})||_{L2(BF x U,h_obs)}",
            "observable_envelope": "|delta gamma_PPN| <= (c^2/(2 U_min)) N_G N_D Q_norm",
            "units": "stress-divergence / force-density units before response normalization; PPN envelope dimensionless after N_G,N_D,U_min",
            "required_inputs": "Gamma_eff_formula;K_hat_formula;P_loc_operator;h_obs_norm;domain_U;BF_parameter;N_G;N_D;U_min;source_path",
            "current_status": "FIRST_ACTIVE_BOUND_FORMULA_READY_INPUTS_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "input_id": "GKB3454_1_DeltaK_bound",
            "feeds": "q_metric_response_defect",
            "active_symbol": "Delta_K^{mu nu}",
            "bound_formula": "Q_DeltaK <= ||P_loc nabla_mu Delta_K^{mu nu}||_{L2(BF x U,h_obs)}",
            "observable_envelope": "same response map as q_loc residual, with Q_norm replaced by Q_DeltaK",
            "units": "stress-divergence / force-density units before response normalization",
            "required_inputs": "K_hat_formula;K_metric_formula;derivative_boundary_terms;P_loc_operator;domain_U;units;source_path",
            "current_status": "METRIC_RESPONSE_GAP_BOUND_FORMULA_READY_INPUTS_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def q_loc_residual_interface() -> list[dict[str, Any]]:
    return [
        {
            "interface_id": "QRI3454_0_zero_route",
            "route": "derive q_loc zero",
            "requirements": "S_GK action; Khat=K_metric; Helmholtz; Euler closure; double-zero; P_loc parent ownership; boundary no-flux",
            "current_status": "NOT_CLOSED",
            "next_input": "Delta_K component ledger or response-doublet source-free proof",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "interface_id": "QRI3454_1_bound_route",
            "route": "retain q_loc and bound",
            "requirements": "Q_norm plus response operators N_G,N_D,U_min and observed-frame map to PPN/source-normalization arenas",
            "current_status": "SCHEMA_READY_NUMERIC_OR_THEOREM_INPUTS_MISSING",
            "next_input": "fill Gamma/Khat formula source or Delta_K bound row",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "interface_id": "QRI3454_2_type_verdict",
            "route": "placeholder typing verdict",
            "requirements": "Gamma/Khat/q_loc cannot be marked q-basic globally; it is active until metric-response/zero proof closes",
            "current_status": "ACTIVE_RESIDUAL_RETAINED",
            "next_input": "3455 Delta_K component ledger",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G3454_0_sources_exist",
            "gate": "all cited 3454 source paths exist",
            "status": "PRIVATE_CHECK_PASS",
            "blocks_claim": False,
            "needed_for_claim": "provenance only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3454_1_placeholder_typed",
            "gate": "Gamma/Khat/q_loc placeholder is typed",
            "status": "PASS_ACTIVE_INTERFACE",
            "blocks_claim": False,
            "needed_for_claim": "active interface must be zeroed or bounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3454_2_metric_response_gap",
            "gate": "Khat equals metric response of Gamma_eff",
            "status": "FAIL_NOT_MATCHED",
            "blocks_claim": True,
            "needed_for_claim": "Delta_K=0 or bound with derivative/boundary terms",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3454_3_first_active_bound",
            "gate": "first active q_loc/Delta_K bound formula exists",
            "status": "PASS_FORMULA_INPUTS_MISSING",
            "blocks_claim": True,
            "needed_for_claim": "source-backed Gamma/Khat/P_loc/response norm inputs",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3454_4_no_claim",
            "gate": "no local-GR/Newton/R10/PPN/clock/orbital pass from this checkpoint",
            "status": "ENFORCED",
            "blocks_claim": True,
            "needed_for_claim": "q_loc zero or bound must close first",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3454_0",
            "question": "Can Gamma/Khat/q_loc be classed as q-basic zero?",
            "answer": "Only for a supplied q-basic Gamma subblock; not for the live placeholder.",
            "reason": "The live route still needs S_GK, Khat metric-response identity, Helmholtz, Euler/double-zero and boundary no-flux.",
            "next_action": "build Delta_K component ledger or response-doublet proof",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3454_1",
            "question": "What did we gain?",
            "answer": "Gamma/Khat/q_loc is no longer a shapeless placeholder; it is either q-basic zero, variational active, or explicit q_loc/Delta_K residual.",
            "reason": "The first active bound formula is now source-ready, with units and required inputs listed.",
            "next_action": "3455 Delta_K component ledger",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3455-Y5-R2FR-DeltaK-component-ledger-or-q_loc-norm-first-fill-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3455_DeltaK_component_ledger_or_qloc_norm_first_fill.py",
            "objective": "Compare K_hat to the metric response of Gamma_eff component-by-component, including derivative and boundary terms, or fill the first q_loc/DeltaK norm input.",
            "start_from": "MRS3454_2_Khat_match and GKB3454_1_DeltaK_bound",
            "success_gate": "Either Delta_K is zero/exact/boundary-silent by component ledger, or Q_DeltaK receives real theorem/numeric source inputs.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3454_0",
            "mode": "private_nonclaim_checkpoint",
            "result": "Gamma/Khat/q_loc placeholder typed and first active q_loc/DeltaK bound staged",
            "claim_status": "NO_LOCAL_GR_NEWTON_R10_PPN_CLOCK_OR_ORBITAL_CLAIM",
            "reason": "metric-response identity and q_loc zero theorem remain unproved",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1
            for checked_path in FORMALIZATION.rglob("*")
            if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )

    nonclaim_ok = True
    for rows in rows_by_name.values():
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                nonclaim_ok = False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                nonclaim_ok = False

    parse_ok = True
    for output_name, path in OUTPUTS.items():
        if output_name == "validation":
            continue
        try:
            read_csv(path)
        except csv.Error:
            parse_ok = False

    classifications = {row["classification"] for row in rows_by_name["gk_placeholder_typing"]}
    bound_ids = {row["input_id"] for row in rows_by_name["first_active_lx_bound_input"]}

    validations = [
        {
            "check_id": "VAL3454_0_sources_exist",
            "condition": "all cited 3454 source paths exist",
            "passed": all(path.exists() for path in SOURCES.values()),
            "detail": f"{sum(1 for path in SOURCES.values() if path.exists())}/{len(SOURCES)} source paths exist",
        },
        {
            "check_id": "VAL3454_1_typing_classes",
            "condition": "Gamma/Khat/q_loc typed into zero, active, residual and rejected classes",
            "passed": "THEOREM_ZERO_IF_SOURCE_SIGNED" in classifications
            and "ACTIVE_METRIC_RESPONSE_GAP" in classifications
            and "EXPLICIT_ACTIVE_RESIDUAL_INTERFACE" in classifications
            and "REJECTED_NOT_A_THEORY_ROUTE" in classifications,
            "detail": f"classifications={';'.join(sorted(classifications))}",
        },
        {
            "check_id": "VAL3454_2_metric_response_not_promoted",
            "condition": "metric response gap remains explicit",
            "passed": any(
                row["status_id"] == "MRS3454_3_verdict" and row["current_status"] == "NOT_PROMOTED"
                for row in rows_by_name["metric_response_status"]
            ),
            "detail": "Delta_K retained",
        },
        {
            "check_id": "VAL3454_3_first_active_bounds",
            "condition": "first active q_loc and Delta_K bound formulas exist",
            "passed": bound_ids == {"GKB3454_0_q_loc_norm_bound", "GKB3454_1_DeltaK_bound"},
            "detail": f"{len(bound_ids)} active bound inputs",
        },
        {
            "check_id": "VAL3454_4_no_claims",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim_ok,
            "detail": "valid_for_claim=false and claim_allowed=false wherever present",
        },
        {
            "check_id": "VAL3454_5_generated_csv_parse",
            "condition": "generated CSV rows parse cleanly",
            "passed": parse_ok,
            "detail": "CSV reader pass for generated outputs present before validation write",
        },
        {
            "check_id": "VAL3454_6_next_target_3455",
            "condition": "next target is DeltaK component ledger or q_loc norm fill",
            "passed": rows_by_name["next_target"][0]["target_doc"].startswith("3455-Y5-R2FR-DeltaK-component-ledger"),
            "detail": rows_by_name["next_target"][0]["target_doc"],
        },
        {
            "check_id": "VAL3454_7_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3454_8_overall",
            "condition": "3454 Gamma/Khat/q_loc typing checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3454 - Gamma/Khat/q_loc Placeholder Typing or First Active L_X Bound

## Summary
- This checkpoint types the `Gamma/Khat/q_loc` placeholder instead of leaving it inside `S_MTS[...]`.
- Safe case: a supplied q-basic `Gamma_eff` subblock is theorem-zero under `v_Xrep`.
- Live case: the current `Gamma_eff/K_hat/q_loc` route is active, not q-basic, because `K_hat` is not matched to the metric response of a source-backed `Gamma_eff`.
- `q_loc` is therefore retained as an explicit projected-divergence residual, not a fundamental field and not a plateau axiom.
- First active bound formulas now exist for both `q_loc` and `Delta_K=K_hat-K_metric`, with units and required inputs stated.

## Source Register
{md_table(rows_by_name["source_register"])}

## Gamma/Khat/q_loc Placeholder Typing
{md_table(rows_by_name["gk_placeholder_typing"])}

## Metric Response Status
{md_table(rows_by_name["metric_response_status"])}

## First Active L_X Bound Input
{md_table(rows_by_name["first_active_lx_bound_input"])}

## q_loc Residual Interface
{md_table(rows_by_name["q_loc_residual_interface"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
The fog is thinner again: `Gamma/Khat/q_loc` is no longer an untyped placeholder. The active obstruction is now specifically `Delta_K`: does the live `K_hat` equal the metric response of a source-backed `Gamma_eff`, including derivative and boundary terms? If yes, the Ward route can advance; if not, `q_loc` must be bounded as a real local residual.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "gk_placeholder_typing": gk_placeholder_typing(),
        "metric_response_status": metric_response_status(),
        "first_active_lx_bound_input": first_active_lx_bound_input(),
        "q_loc_residual_interface": q_loc_residual_interface(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3454 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
