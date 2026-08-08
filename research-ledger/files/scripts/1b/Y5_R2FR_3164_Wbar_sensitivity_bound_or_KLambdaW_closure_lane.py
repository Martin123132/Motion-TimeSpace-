from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3164_INPUTS.csv"
THEOREM = OUT / "P8_Y5_R2FR_3164_RESTRICTED_WBAR_SENSITIVITY_THEOREM.csv"
GATES = OUT / "P8_Y5_R2FR_3164_WBAR_GATE_STATUS.csv"
CLOSURE = OUT / "P8_Y5_R2FR_3164_KLAMBDAW_CLOSURE_LANE.csv"
DECISION = OUT / "P8_Y5_R2FR_3164_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3164_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def internal(relative: str) -> str:
    return str((ROOT / relative).resolve())


def cap_value(closure_id: str, column: str) -> str:
    for row in read_csv(OUT / "P8_Y5_R2FR_3163_CLOSURE_PRODUCT_CONTRACT.csv"):
        if row.get("closure_id") == closure_id:
            return row[column]
    raise KeyError(f"missing {closure_id}.{column}")


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        ("3163-Y5-R2FR-MLambda-scale-from-qbasic-boundary-primitive-or-closure-under-AX1090.md", "3163 M_Lambda theorem/closure product"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3163_CLOSURE_PRODUCT_CONTRACT.csv", "K_LambdaW cap"),
        ("3152-Y5-R2FR-kernel-closedness-chain-rule-or-first-norm-factor-bound-under-AX1090.md", "chain-rule definition of L_W"),
        ("3154-Y5-R2FR-Wbar-basic-quotient-theorem-or-Bphys-first-component-bound-under-AX1090.md", "pure gauge Wbar basicness theorem and physical drift guard"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3154_WBAR_BASIC_QUOTIENT_THEOREM.csv", "Wbar quotient theorem rows"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3161_BEXACT_SOURCE_BOUND_ROWS.csv", "first-domain l=2 physical mode rows"),
    ]
    return [
        {
            "input_id": f"IN3164_{index}",
            "path": internal(path),
            "exists": str((ROOT / path).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (path, role) in enumerate(rows)
    ]


def theorem_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "theorem_id": "WT3164_0_l2_subspace",
            "object": "physical_l2_boundary_lane",
            "statement": "Restrict the physical boundary drift to the one-dimensional span e2:=P2(cos theta) in the first Earth-domain metric-component chart.",
            "formula": "delta z_phys = delta A e2",
            "proof_content": "3161 supplies the exact l=2 mode and 3154 forbids erasing metric multipole/tide drift as pure gauge.",
            "status": "definition_pass_nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "WT3164_1_restricted_derivative",
            "object": "restricted_Wbar_derivative",
            "statement": "If Wbar is Frechet differentiable on the selected boundary chart, its derivative restricted to span(e2) is multiplication by one scalar W_2.",
            "formula": "D_z Wbar[delta A e2] = W_2 delta A",
            "proof_content": "Any linear map from a one-dimensional vector space to R is determined by its value on a basis element.",
            "status": "exact_conditional_math",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "WT3164_2_restricted_operator_norm",
            "object": "L_W_phys_on_l2",
            "statement": "In the amplitude-normalized l=2 chart, the restricted physical sensitivity is |W_2|.",
            "formula": "L_W_phys,l2 = |W_2|",
            "proof_content": "The operator norm of delta A -> W_2 delta A with norm |delta A| is |W_2|.",
            "status": "exact_conditional_math",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "WT3164_3_projection_owner_route",
            "object": "candidate_projection_Wbar",
            "statement": "If Wbar is parent-owned as the normalized l=2 projection coefficient Wbar[f]=<f,e2>/<e2,e2>, then W_2=1.",
            "formula": "Wbar[A e2] = A => W_2=1",
            "proof_content": "Orthogonal projection onto a normalized coordinate returns the coefficient of the basis mode.",
            "status": "exact_if_projection_owner_parent_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "WT3164_4_annihilator_route",
            "object": "physical_l2_annihilator",
            "statement": "If D_z Wbar annihilates the physical l=2 lane, then W_2=0 and the local product vanishes on this lane.",
            "formula": "D_z Wbar[e2]=0 => W_2=0",
            "proof_content": "This is the physical-kernel-zero route from 3157 restricted to the l=2 lane.",
            "status": "conditional_not_parent_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "WT3164_5_no_claim",
            "object": "parent_Wbar_owner",
            "statement": "Current corpus still has not supplied the parent Wbar functional or tangent-domain owner, so W_2 is not claimed numeric.",
            "formula": "W_2 := D_z Wbar[e2]",
            "proof_content": "3152/3154 identify the missing owner and only prove the pure-gauge quotient theorem, not the physical l=2 sensitivity.",
            "status": "blocked_for_claim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "gate_id": "G3164_0_l2_lane_defined",
            "gate": "physical l=2 lane defined",
            "status": "pass_nonclaim",
            "detail": "3161 gives the l=2 metric-component boundary mode and exact norms",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3164_1_restricted_math",
            "gate": "restricted derivative theorem",
            "status": "pass_conditional_math",
            "detail": "on a one-dimensional lane D_z Wbar is a scalar W_2",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3164_2_projection_owner",
            "gate": "Wbar is normalized l=2 projection coefficient",
            "status": "not_parent_signed",
            "detail": "would give W_2=1, but current corpus has no parent Wbar functional",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3164_3_physical_annihilator",
            "gate": "Wbar annihilates physical l=2 drift",
            "status": "fail_for_claim",
            "detail": "pure gauge annihilator exists conditionally; physical l=2 annihilator is not signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3164_4_KLambdaW_lane",
            "gate": "closure lane K_2=|W_2 M_Lambda|",
            "status": "pass_nonclaim",
            "detail": "local test can carry K_2 explicitly instead of pretending Wbar/M_Lambda are derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def closure_rows(l2_cap: str, general_cap: str) -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "closure_id": "KW3164_0_restricted_coefficient",
            "quantity": "W_2",
            "definition": "W_2 := D_z Wbar[e2] on the first physical l=2 boundary lane",
            "claim_status": "missing_parent_Wbar_functional",
            "required_bound_l2": "1.661478072732745e20 / |M_Lambda|",
            "required_bound_general": "9.592548125449111e19 / |M_Lambda|",
            "formula": "|W_2| <= cap/|M_Lambda|",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "closure_id": "KW3164_1_combined_lane_product",
            "quantity": "K_2",
            "definition": "K_2 := |W_2 M_Lambda|",
            "claim_status": "closure_lane_ready",
            "required_bound_l2": l2_cap,
            "required_bound_general": general_cap,
            "formula": "K_2 <= cap",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "closure_id": "KW3164_2_projection_owner_case",
            "quantity": "K_2_if_projection_Wbar",
            "definition": "If Wbar is the normalized l=2 projection coefficient, W_2=1",
            "claim_status": "conditional_case_not_parent_signed",
            "required_bound_l2": l2_cap,
            "required_bound_general": general_cap,
            "formula": "K_2=|M_Lambda|, and if also M_Lambda=1 then K_2=1",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "closure_id": "KW3164_3_empirical_local_lane",
            "quantity": "empirical_K_2",
            "definition": "single closure coefficient for first-domain local l=2 testing",
            "claim_status": "test_lane_only",
            "required_bound_l2": l2_cap,
            "required_bound_general": general_cap,
            "formula": "fit/test K_2 directly; no local-GR claim unless parent Wbar and M_Lambda close",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows(l2_cap: str) -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "D3164_0_Wbar_status",
            "decision": "full L_W_phys cannot be derived because parent Wbar is still unsigned",
            "evidence": "3152/3154 and WT3164_5",
            "effect": "do not claim local closure from Wbar sensitivity",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3164_1_restricted_progress",
            "decision": "the first local l=2 lane reduces Wbar uncertainty to one scalar W_2",
            "evidence": "WT3164_1 and WT3164_2",
            "effect": "replace broad L_W_phys fog with K_2=|W_2 M_Lambda| for first-domain tests",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3164_2_closure_lane",
            "decision": "open a nonclaim empirical closure lane for K_2",
            "evidence": f"K_2 <= {l2_cap} under the l=2 first-domain cap",
            "effect": "local testing can proceed with an explicit finite closure parameter instead of hidden assumptions",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3164_3_next_attack",
            "decision": "move from local coefficient derivation to local PPN/clock/orbital residual using K_2 as explicit nonclaim parameter",
            "evidence": "all upstream coefficients are now either derived or named as K_2",
            "effect": "next checkpoint should build the K_2 residual vector and acceptance thresholds",
            "next_action": "3165-Y5-R2FR-K2-local-residual-vector-and-PPN-clock-orbital-gate-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    theorems: list[dict[str, object]],
    gates: list[dict[str, object]],
    closures: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    input_ok = all(row["exists"] == "true" for row in inputs)
    restricted_math = any(row["theorem_id"] == "WT3164_2_restricted_operator_norm" for row in theorems)
    claim_block = any(row["status"] == "blocked_for_claim" for row in theorems) and any(row["status"] == "fail_for_claim" for row in gates)
    closure_ready = any(row["quantity"] == "K_2" for row in closures)
    no_claim = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for rows in [inputs, theorems, gates, closures, decisions]
        for row in rows
    )
    return [
        {
            "check_id": "V3164_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3164_1_restricted_math_present",
            "status": "pass" if restricted_math else "fail",
            "detail": "restricted l=2 Wbar operator norm theorem present",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3164_2_claim_blockers_retained",
            "status": "pass" if claim_block else "fail",
            "detail": "blocked_for_claim parent Wbar and fail_for_claim physical annihilator retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3164_3_closure_lane_ready",
            "status": "pass" if closure_ready else "fail",
            "detail": "K_2 closure lane exists",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3164_4_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "all 3164 rows valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    l2_cap = cap_value("KC3163_1_closure_product", "required_bound_l2")
    general_cap = cap_value("KC3163_1_closure_product", "required_bound_general")
    inputs = input_rows()
    theorems = theorem_rows()
    gates = gate_rows()
    closures = closure_rows(l2_cap, general_cap)
    decisions = decision_rows(l2_cap)
    validations = validation_rows(inputs, theorems, gates, closures, decisions)
    write_csv(INPUTS, inputs)
    write_csv(THEOREM, theorems)
    write_csv(GATES, gates)
    write_csv(CLOSURE, closures)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)
    failures = [row for row in validations if row["status"] != "pass"]
    if failures:
        raise SystemExit(f"3164 validation failed: {failures}")


if __name__ == "__main__":
    main()
