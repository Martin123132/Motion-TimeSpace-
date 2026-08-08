from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3163_INPUTS.csv"
THEOREM = OUT / "P8_Y5_R2FR_3163_MLAMBDA_PULLBACK_THEOREM.csv"
GATES = OUT / "P8_Y5_R2FR_3163_MLAMBDA_CLAUSE_GATES.csv"
CLOSURE = OUT / "P8_Y5_R2FR_3163_CLOSURE_PRODUCT_CONTRACT.csv"
DECISION = OUT / "P8_Y5_R2FR_3163_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3163_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def fmt(value: float) -> str:
    return f"{value:.15e}"


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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def internal(relative: str) -> str:
    return str((ROOT / relative).resolve())


def mlambda_cap_l2() -> float:
    for row in read_csv(OUT / "P8_Y5_R2FR_3162_MLAMBDA_COEFFICIENT_CONTRACT.csv"):
        if row.get("contract_id") == "MC3162_3_LWphys_MLambda_cap_l2":
            return float(row["reference_M1_LWphys_cap"])
    raise KeyError("missing MC3162_3_LWphys_MLambda_cap_l2")


def mlambda_cap_general() -> float:
    for row in read_csv(OUT / "P8_Y5_R2FR_3162_MLAMBDA_COEFFICIENT_CONTRACT.csv"):
        if row.get("contract_id") == "MC3162_4_LWphys_MLambda_cap_general":
            return float(row["reference_M1_LWphys_cap"])
    raise KeyError("missing MC3162_4_LWphys_MLambda_cap_general")


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        ("3162-Y5-R2FR-parent-Lambda-map-for-public-l2-boundary-profile-under-AX1090.md", "3162 M_Lambda map coefficient"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3162_MLAMBDA_COEFFICIENT_CONTRACT.csv", "M_Lambda product caps"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3162_PARENT_LAMBDA_MAP_AUDIT.csv", "parent map audit"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3140_THETA_DESCENT_THEOREM.csv", "strong q-basic action pullback theorem shape"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3141_TOTAL_ACTION_CONTRACT.csv", "total action boundary sector contract"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3132_PARENT_BOUNDARY_PRIMITIVE_OUTPUT.csv", "boundary primitive formula and blockers"),
    ]
    return [
        {
            "input_id": f"IN3163_{index}",
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
            "theorem_id": "MT3163_0_public_boundary_chart",
            "statement": "Let A_public be the Q_obs boundary coordinate for the public l=2 metric profile A_public P2(cos theta).",
            "proof_step": "This is a chart declaration for the selected first-domain l=2 boundary sector.",
            "status": "definition_if_q_boundary_chart_owned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MT3163_1_public_primitive",
            "statement": "Define the public boundary primitive Lambdabar_Q(A_public)=A_public P2(cos theta) in the same metric-component convention as 3159.",
            "proof_step": "The 3161 l=2 identities prove this has exact derivative d_S Lambdabar_Q and no harmonic 1-form ambiguity on S2.",
            "status": "exact_math_if_public_primitive_owned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MT3163_2_qbasic_boundary_pullback",
            "statement": "If the parent boundary primitive is q^*Lambdabar_Q with no extra scale/counterterm/residual in this channel, then Lambda_parent=q^*Lambdabar_Q.",
            "proof_step": "This is functorial pullback of the boundary primitive under the q-basic boundary sector.",
            "status": "conditional_theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MT3163_3_MLambda_equals_one",
            "statement": "Under MT3163_0 through MT3163_2, Lambda_parent=A_public P2(cos theta), so M_Lambda=1.",
            "proof_step": "Compare Lambda_parent=M_Lambda A_public P2 with Lambda_parent=A_public P2 on the same nonzero l=2 chart.",
            "status": "exact_conditional_result_not_parent_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MT3163_4_no_claim",
            "statement": "Current corpus has not parent-signed the q-basic boundary primitive or residual-silence clauses, so M_Lambda=1 is not promoted.",
            "proof_step": "3132, 3140, 3141 and 3162 retain parent primitive, boundary sector and residual/counterterm blockers.",
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
            "gate_id": "G3163_0_public_l2_chart",
            "gate": "Q_obs owns the public l=2 metric boundary chart",
            "status": "declared_not_parent_signed",
            "detail": "q(Phi) includes g_obs/boundary_class_obs but q remains candidate, not parent-owned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3163_1_public_primitive_math",
            "gate": "public l=2 primitive exactness",
            "status": "pass_nonclaim",
            "detail": "3161 proves exact l=2 surface identities on S2",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3163_2_qbasic_boundary_primitive",
            "gate": "parent boundary primitive is q-pullback of public primitive",
            "status": "fail_for_claim",
            "detail": "3132 says parent primitive is formula-shaped but not derived; 3141 boundary sector not signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3163_3_no_extra_scale",
            "gate": "no independent M_Lambda scale or nonlinear reparameterization",
            "status": "fail_for_claim",
            "detail": "current parent grammar does not forbid a scale in the boundary primitive map",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3163_4_no_reference_residual_mixing",
            "gate": "counterterm/reference/corner/residual silence",
            "status": "fail_for_claim",
            "detail": "3162 countermodels remain live",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3163_5_MLambda_one",
            "gate": "M_Lambda=1 promotion",
            "status": "blocked_for_claim",
            "detail": "conditional theorem is exact but premises are not parent-signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def closure_rows(l2_cap: float, general_cap: float) -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "closure_id": "KC3163_0_if_MLambda_signed",
            "quantity": "L_W_phys",
            "condition": "if M_Lambda=1 is parent-signed",
            "required_bound_l2": fmt(l2_cap),
            "required_bound_general": fmt(general_cap),
            "formula": "L_W_phys <= cap because |M_Lambda|=1",
            "status": "conditional_bound_not_claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "closure_id": "KC3163_1_closure_product",
            "quantity": "K_LambdaW",
            "condition": "if M_Lambda is not parent-signed",
            "required_bound_l2": fmt(l2_cap),
            "required_bound_general": fmt(general_cap),
            "formula": "K_LambdaW := L_W_phys |M_Lambda| <= cap",
            "status": "closure_product_contract",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "closure_id": "KC3163_2_reciprocal_MLambda_cap",
            "quantity": "|M_Lambda|",
            "condition": "if L_W_phys is independently derived or bounded",
            "required_bound_l2": "1.661478072732745e20 / L_W_phys",
            "required_bound_general": "9.592548125449111e19 / L_W_phys",
            "formula": "|M_Lambda| <= cap/L_W_phys",
            "status": "reciprocal_contract_ready",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "closure_id": "KC3163_3_reciprocal_LWphys_cap",
            "quantity": "L_W_phys",
            "condition": "if |M_Lambda| is independently derived or bounded",
            "required_bound_l2": "1.661478072732745e20 / |M_Lambda|",
            "required_bound_general": "9.592548125449111e19 / |M_Lambda|",
            "formula": "L_W_phys <= cap/|M_Lambda|",
            "status": "reciprocal_contract_ready",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows(l2_cap: float) -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "D3163_0_theorem_status",
            "decision": "M_Lambda=1 is exactly derivable from a q-basic boundary primitive, but that primitive is not parent-signed",
            "evidence": "MT3163_3 exact conditional result plus G3163_2/G3163_3/G3163_4 fail_for_claim",
            "effect": "do not use M_Lambda=1 as a claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3163_1_closure_status",
            "decision": "the honest local branch object is K_LambdaW := L_W_phys |M_Lambda| until parent boundary primitive closes",
            "evidence": f"K_LambdaW <= {fmt(l2_cap)} under the l=2 first-domain cap",
            "effect": "testing can proceed only as closure/finite-product branch if M_Lambda remains unsigned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3163_2_next_attack",
            "decision": "move to Wbar sensitivity/product closure rather than circling M_Lambda again",
            "evidence": "M_Lambda theorem premises require the broad parent boundary sector already known unsigned",
            "effect": "next checkpoint should derive/bound L_W_phys or create an empirical closure lane for K_LambdaW",
            "next_action": "3164-Y5-R2FR-Wbar-sensitivity-bound-or-KLambdaW-closure-lane-under-AX1090",
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
    theorem_has_exact = any(row["status"] == "exact_conditional_result_not_parent_signed" for row in theorems)
    gates_block_claim = any(row["status"] == "fail_for_claim" for row in gates) and any(row["status"] == "blocked_for_claim" for row in gates)
    closure_ready = any(row["quantity"] == "K_LambdaW" and row["status"] == "closure_product_contract" for row in closures)
    no_claim = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for rows in [inputs, theorems, gates, closures, decisions]
        for row in rows
    )
    return [
        {
            "check_id": "V3163_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3163_1_conditional_theorem_present",
            "status": "pass" if theorem_has_exact else "fail",
            "detail": "M_Lambda=1 exact conditional theorem present",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3163_2_claim_blockers_retained",
            "status": "pass" if gates_block_claim else "fail",
            "detail": "fail_for_claim and blocked_for_claim gates retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3163_3_closure_product_ready",
            "status": "pass" if closure_ready else "fail",
            "detail": "K_LambdaW closure product contract exists",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3163_4_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "all 3163 rows valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    l2_cap = mlambda_cap_l2()
    general_cap = mlambda_cap_general()
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
        raise SystemExit(f"3163 validation failed: {failures}")


if __name__ == "__main__":
    main()
