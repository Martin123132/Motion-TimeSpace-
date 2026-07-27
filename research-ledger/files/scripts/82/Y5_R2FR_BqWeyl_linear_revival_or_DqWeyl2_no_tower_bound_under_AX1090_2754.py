from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2754-Y5-R2FR-BqWeyl-linear-revival-or-DqWeyl2-no-tower-bound-under-AX1090.md"
BRANCH_ID = "MTS_R2FR_AX1090_BQWEYL_DQWEYL2_2754"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2754_SOURCE_REGISTER.csv",
    "linear": RESIDUALS / "P8_Y5_R2FR_2754_LINEAR_BQWEYL_REVIVAL_GATE.csv",
    "tower": RESIDUALS / "P8_Y5_R2FR_2754_DQWEYL2_NO_TOWER_ZERO_ATTEMPT.csv",
    "projection": RESIDUALS / "P8_Y5_R2FR_2754_SCHWARZSCHILD_WEYL2_PROJECTION_GATE.csv",
    "input": RESIDUALS / "P8_Y5_R2FR_2754_DQWEYL2_INPUT_CONTRACT.csv",
    "refusal": RESIDUALS / "P8_Y5_R2FR_2754_REFUSAL_RUNNER_NONCLAIM.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2754_CLAIM_GATES.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2754_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2754_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2754_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2754_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "dqweyl2_local": LOCAL_BOUNDS / "DqWeyl2_no_tower_input_contract_2754_NONCLAIM.csv",
    "linear_source_weight": SOURCE_WEIGHT / "BqWeyl_linear_revival_gate_2754_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2754_Q_OPERATOR_OR_INDEPENDENT_HESSIAN_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()}:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing empty CSV: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], cols: list[str]) -> str:
    header = "| " + " | ".join(cols) + " |"
    sep = "| " + " | ".join("---" for _ in cols) + " |"
    body = ["| " + " | ".join(md(row.get(col, "")) for col in cols) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def local_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["numeric_value_present"] = False
    row["source_backed"] = False
    row["score_ready"] = False
    row["valid_prediction_row"] = False
    row["valid_for_claim"] = False
    row["claim_allowed"] = False
    return row


def source_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": "SRC2754_0_2753_doc",
            "description": "2753 first finite q_R component handoff.",
            "source_path": "2753-Y5-R2FR-first-finite-qR-component-bound-or-source-zero-theorem-under-AX1090.md",
            "required_needles": "NEXT2753_0_2754;FC2753_1_DqWeyl2;VAL2753_OVERALL",
        },
        {
            "source_id": "SRC2754_1_2753_validation",
            "description": "2753 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2753_VALIDATION.csv",
            "required_needles": "VAL2753_OVERALL;True",
        },
        {
            "source_id": "SRC2754_2_2305_doc",
            "description": "prior linear B_qWeyl demotion and D_qWeyl2 residual handoff.",
            "source_path": "2305-Y5-R2FR-BqWeyl-linear-zero-typed-grammar-signature-or-quadratic-Weyl-residual-row.md",
            "required_needles": "LINEAR_BQWEYL_ROUTE_DEMOTED_TO_CLOSURE_ONLY;D_qWeyl2;VAL2305_OVERALL",
        },
        {
            "source_id": "SRC2754_3_2306_doc",
            "description": "prior D_qWeyl2 zero-theorem attempt and Schwarzschild projection law.",
            "source_path": "2306-Y5-R2FR-DqWeyl2-higher-curvature-tower-zero-or-first-local-bound-row.md",
            "required_needles": "ZERO2306_4_verdict;C_{abcd}C^{abcd}=48;VAL2306_OVERALL",
        },
        {
            "source_id": "SRC2754_4_2306_bound",
            "description": "prior D_qWeyl2 first local bound row.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2306_DQWEYL2_FIRST_LOCAL_BOUND_ROW.csv",
            "required_needles": "BOUND2306_0_coefficient;MISSING_PARENT_COEFFICIENT",
        },
        {
            "source_id": "SRC2754_5_2307_doc",
            "description": "prior D_qWeyl2 projection smoke contract.",
            "source_path": "2307-Y5-R2FR-DqWeyl2-projection-smoke-runner-input-contract-or-parent-coefficient-source.md",
            "required_needles": "PARENT_COEFFICIENT_NOT_FOUND;DRYRUN_KERNEL_ONLY_NOT_OBSERVABLE;VAL2307_OVERALL",
        },
        {
            "source_id": "SRC2754_6_2308_doc",
            "description": "prior D_qWeyl2 coefficient and q-operator normalization source hunt.",
            "source_path": "2308-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md",
            "required_needles": "D_QWEYL2_COEFFICIENT_NOT_SOURCED;Q_OPERATOR_CAN_NOT_BORROW_X_YET;VAL2308_OVERALL",
        },
    ]
    for row in rows:
        path = local_path(row["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles = [needle for needle in row["required_needles"].split(";") if needle]
        missing = [needle for needle in needles if needle not in text]
        row["exists"] = path.exists()
        row["needles_present"] = len(missing) == 0
        row["missing_needles"] = ";".join(missing)
        nonclaim(row)
    return rows


def linear_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "LIN2754_0_index_theorem",
            "linear B_qWeyl zero by index/type",
            "scalar/quotient q cannot form q*C_abcd scalar from one Weyl tensor without a Weyl-type spurion/projector",
            "EXACT_CONDITIONAL_THEOREM",
            "MISSING_PARENT_Q_REPRESENTATION_NO_SPURION_SIGNATURE",
        ),
        (
            "LIN2754_1_revival_test",
            "new parent signature since 2305",
            "no new parent-signed no-Weyl-spurion/q-representation certificate is present in the current 2753 handoff",
            "NO_NEW_EVIDENCE",
            "linear route remains closure-only",
        ),
        (
            "LIN2754_2_verdict",
            "linear B_qWeyl status",
            "do not rerun the same closure candidate without new parent source text",
            "DEMOTE_TO_CLOSURE_ONLY_UNTIL_PARENT_SIGNED",
            "MISSING_PARENT_OBJECT_LANGUAGE_SIGNATURE",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "linear_id": lid,
                "test": test,
                "statement": statement,
                "current_status": status,
                "missing_for_claim": missing,
            }
        )
        for lid, test, statement, status, missing in specs
    ]


def tower_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "TOWER2754_0_no_bare_weyl2",
            "no bare q C^2 or q C*C operator",
            "would remove D_qWeyl2 at the parent action level",
            "UNSIGNED",
            "MISSING_PARENT_HIGHER_CURVATURE_INVENTORY",
        ),
        (
            "TOWER2754_1_no_integrated_tower",
            "no eliminated field/projector/memory sector regenerates Weyl2/R2/nonlocal curvature tower",
            "would block radiative/readout regeneration of D_qWeyl2",
            "UNSIGNED",
            "NO_TOWER_THEOREM_NOT_DERIVED",
        ),
        (
            "TOWER2754_2_no_curvature_morphism",
            "hidden invariants cannot feed curvature coefficients",
            "would prevent F(I_hidden)C^2 coefficient drift",
            "UNSIGNED",
            "CURVATURE_MORPHISM_NOT_EXCLUDED",
        ),
        (
            "TOWER2754_3_verdict",
            "D_qWeyl2=0 theorem",
            "zero route is exact if all no-tower clauses are parent-signed, but current evidence does not sign them",
            "ZERO_THEOREM_NOT_DERIVED",
            "RETAIN_FINITE_DQWEYL2_ROW",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "tower_id": tid,
                "zero_clause": clause,
                "would_supply": supply,
                "current_status": status,
                "missing_for_claim": missing,
                "theorem_zero": False,
            }
        )
        for tid, clause, supply, status, missing in specs
    ]


def projection_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PROJ2754_0_schwarzschild_C2",
            "C2_Schw",
            "C_abcd C^abcd = 48 (GM/c^2)^2 / r^6",
            "EXACT_BACKGROUND_IDENTITY_NONCLAIM",
            "useful projection identity, not a proof of GR or a source coefficient",
        ),
        (
            "PROJ2754_1_source_integral_scaling",
            "K_C2_ext",
            "K_C2_ext = 64*pi*(GM/c^2)^2/R_body^3 for exterior finite-radius scaling in the 2306 convention",
            "ANALYTIC_KERNEL_READY_NONCLAIM",
            "requires finite source radius/interior matching; point-particle shortcut rejected",
        ),
        (
            "PROJ2754_2_far_field",
            "q_far",
            "q(r) ~ D_qWeyl2*K_C2_ext/(4*pi*Z_q*r) in massless scaffold; Yukawa branch adds exp(-r/lambda_q)",
            "SCALING_CONTRACT_READY_INPUTS_MISSING",
            "D_qWeyl2, Z_q, lambda_q, boundary condition, and observable projection missing",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "projection_id": pid,
                "quantity": quantity,
                "formula": formula,
                "current_status": status,
                "claim_guard": guard,
            }
        )
        for pid, quantity, formula, status, guard in specs
    ]


def input_rows() -> list[dict[str, Any]]:
    specs = [
        ("IN2754_0_DqWeyl2", "D_qWeyl2", "parent coefficient of q C^2", "MISSING_PARENT_COEFFICIENT_OR_ZERO_THEOREM", "source path, sign, units, action normalization"),
        ("IN2754_1_Zq", "Z_q", "q kinetic/operator normalization", "MISSING_Q_OPERATOR_NORMALIZATION", "q local action Hessian or q-X bridge"),
        ("IN2754_2_Mq2_lambda", "M_q^2/lambda_q", "range/mass gap", "MISSING_RANGE_OR_NO_POLE_THEOREM", "same normalization as Z_q"),
        ("IN2754_3_body_cutoff", "R_body/interior matching", "finite source model for C^2 integral", "MISSING_SOURCE_MODEL_FOR_C2_BOUND", "body radius/density/cutoff convention"),
        ("IN2754_4_Parena", "P_arena[q]", "observable projection into PPN/orbital/R10/clock", "MISSING_OBSERVABLE_MAP", "metric/readout/backreaction projection"),
        ("IN2754_5_q_absent", "q first-class/no-pole alternative", "removes D_qWeyl2 branch instead of bounding it", "MISSING_Q_REMOVAL_CERTIFICATE", "Omega/DCq/bracket/degree/matter/boundary package"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "input_id": iid,
                "symbol": symbol,
                "role": role,
                "current_status": status,
                "needed_to_promote": needed,
            }
        )
        for iid, symbol, role, status, needed in specs
    ]


def refusal_rows() -> list[dict[str, Any]]:
    specs = [
        ("REF2754_0_linear", "claim linear B_qWeyl=0", "BLOCKED", "no new parent no-spurion/q-representation signature"),
        ("REF2754_1_tower", "claim D_qWeyl2=0", "BLOCKED", "no no-tower/higher-curvature parent theorem"),
        ("REF2754_2_projection", "claim projection law is a bound", "BLOCKED", "projection identity lacks D_qWeyl2/Z_q/P_arena inputs"),
        ("REF2754_3_local_GR", "claim local GR/Newton", "BLOCKED", "Weyl residual is only one gate; source/readout/EH/Newton gates remain open"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": rid,
                "attempted_claim": claim,
                "status": status,
                "reason": reason,
                "runner_allows_claim": False,
            }
        )
        for rid, claim, status, reason in specs
    ]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2754_0_linear_BqWeyl", "linear B_qWeyl theorem-zero", "BLOCKED_NO_CLAIM", "closure-only without parent signature"),
        ("GATE2754_1_DqWeyl2_zero", "D_qWeyl2 theorem-zero", "BLOCKED_NO_CLAIM", "no-tower theorem unsigned"),
        ("GATE2754_2_DqWeyl2_bound", "D_qWeyl2 finite bound score-ready", "BLOCKED_NO_CLAIM", "coefficient/operator/projection inputs missing"),
        ("GATE2754_3_q_absent", "q no-pole/first-class removal", "BLOCKED_NO_CLAIM", "canonical package missing"),
        ("GATE2754_4_local_GR", "derived local GR/Newton", "BLOCKED_NO_CLAIM", "Weyl source branch unresolved"),
    ]
    return [nonclaim({"claim_gate_id": gid, "claim_gate": gate, "status": status, "reason": reason}) for gid, gate, status, reason in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2754_0_linear",
            "linear B_qWeyl route",
            "REMAINS_CLOSURE_ONLY",
            "no new parent-signed q representation/no-spurion evidence appears after 2305",
        ),
        (
            "DEC2754_1_DqWeyl2",
            "quadratic Weyl residual",
            "ZERO_THEOREM_NOT_DERIVED_RETAIN_ROW",
            "no higher-curvature/no-tower parent signature exists in current evidence",
        ),
        (
            "DEC2754_2_projection",
            "Schwarzschild Weyl2 projection",
            "ANALYTIC_KERNEL_READY_NONCLAIM",
            "the C^2 scaling is concrete, but physical scoring waits on D_qWeyl2/Z_q/P_arena",
        ),
        (
            "DEC2754_3_next",
            "next target",
            "NEXT_2755_Q_OPERATOR_IDENTITY_OR_INDEPENDENT_HESSIAN",
            "the bottleneck is now q operator normalization: q-X bridge/no-pole certificate or independent q Hessian",
        ),
    ]
    return [nonclaim({"decision_id": did, "decision": decision, "result": result, "reason": reason}) for did, decision, result, reason in specs]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2754_0_2755",
                "status": "selected_primary",
                "target_doc": "2755-Y5-R2FR-q-operator-identity-bridge-or-independent-Hessian-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_q_operator_identity_bridge_or_independent_Hessian_under_AX1090_2755.py",
                "mission": "before scoring D_qWeyl2, prove q is absent/no-pole, prove q uses an existing X/L_X operator by signed bridge, or source an independent q Hessian/operator normalization; otherwise keep D_qWeyl2 as symbolic residual only",
                "acceptance": "q no-pole certificate, q-X bridge, or independent Z_q/M_q^2/Hessian source row; if none close, emit exact missing operator inputs without scoring",
                "forbidden": "do not copy X coefficients without bridge; do not score D_qWeyl2 projection; do not claim local GR; do not edit formalization-workbench; no GitHub action",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2754_0_dqweyl2_local", "source_table": rel(OUTPUTS["input"]), "copy_path": rel(BRANCH_OUTPUTS["dqweyl2_local"]), "purpose": "local-bound DqWeyl2 input contract", "exists": BRANCH_OUTPUTS["dqweyl2_local"].exists()}),
        nonclaim({"copy_id": "BR2754_1_linear_source_weight", "source_table": rel(OUTPUTS["linear"]), "copy_path": rel(BRANCH_OUTPUTS["linear_source_weight"]), "purpose": "source-weight linear BqWeyl closure status", "exists": BRANCH_OUTPUTS["linear_source_weight"].exists()}),
        nonclaim({"copy_id": "BR2754_2_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB queue for q operator bridge/Hessian", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
    ]


def pycache_path() -> Path:
    return Path(__file__).resolve().parent / "__pycache__"


def remove_pycache() -> None:
    pycache = pycache_path()
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_recent_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    start = SCRIPT_START_UTC.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start)


def validation_rows(
    sources: list[dict[str, Any]],
    linear: list[dict[str, Any]],
    tower: list[dict[str, Any]],
    projection: list[dict[str, Any]],
    input_contract: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    linear_ok = any(row["linear_id"] == "LIN2754_2_verdict" and row["current_status"] == "DEMOTE_TO_CLOSURE_ONLY_UNTIL_PARENT_SIGNED" for row in linear)
    tower_ok = any(row["tower_id"] == "TOWER2754_3_verdict" and row["current_status"] == "ZERO_THEOREM_NOT_DERIVED" for row in tower)
    projection_ok = any(row["projection_id"] == "PROJ2754_0_schwarzschild_C2" for row in projection) and any(row["projection_id"] == "PROJ2754_2_far_field" and row["current_status"] == "SCALING_CONTRACT_READY_INPUTS_MISSING" for row in projection)
    input_ok = {"D_qWeyl2", "Z_q", "M_q^2/lambda_q", "R_body/interior matching", "P_arena[q]", "q first-class/no-pole alternative"}.issubset({row["symbol"] for row in input_contract})
    refusal_ok = all(row["runner_allows_claim"] is False for row in refusal)
    gate_ok = all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in gates) and any(row["claim_gate_id"] == "GATE2754_4_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    decision_ok = any(row["decision_id"] == "DEC2754_3_next" and row["result"] == "NEXT_2755_Q_OPERATOR_IDENTITY_OR_INDEPENDENT_HESSIAN" for row in decisions)
    next_ok = next_target[0]["selected"] is True and "2755" in next_target[0]["target_doc"]
    no_claim_flags_ok = all(
        row.get("valid_for_claim") is False and row.get("claim_allowed") is False
        for block in [linear, tower, projection, input_contract, refusal, gates, decisions, next_target]
        for row in block
    )
    branch_ok = all(path.exists() for path in BRANCH_OUTPUTS.values())
    csv_ok = True
    csv_bits: list[str] = []
    for key, path in {**OUTPUTS, **BRANCH_OUTPUTS}.items():
        if key == "validation":
            continue
        try:
            rows = read_csv(path)
            csv_bits.append(f"{path.name}:{len(rows)}:ok")
        except Exception as exc:
            csv_ok = False
            csv_bits.append(f"{path.name}:ERROR:{exc}")
    pycache_ok = not pycache_path().exists()
    formalization_count = formalization_recent_count()
    formalization_ok = formalization_count == 0
    rows = [
        {"validation_id": "VAL2754_0_sources", "passed": source_ok, "detail": "all source paths exist and needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2754_1_linear_demoted", "passed": linear_ok, "detail": "linear BqWeyl remains closure-only without new parent signature", "timestamp_utc": ts()},
        {"validation_id": "VAL2754_2_tower_zero_failed", "passed": tower_ok, "detail": "DqWeyl2 no-tower zero theorem not derived", "timestamp_utc": ts()},
        {"validation_id": "VAL2754_3_projection_contract", "passed": projection_ok, "detail": "Schwarzschild C2 projection/scaling contract retained nonclaim", "timestamp_utc": ts()},
        {"validation_id": "VAL2754_4_input_contract", "passed": input_ok, "detail": "DqWeyl2 coefficient/operator/projection input contract complete", "timestamp_utc": ts()},
        {"validation_id": "VAL2754_5_refusal_runner", "passed": refusal_ok, "detail": "refusal runner blocks all attempted claims", "timestamp_utc": ts()},
        {"validation_id": "VAL2754_6_claim_gates", "passed": gate_ok and no_claim_flags_ok, "detail": "claim gates remain closed and flags false", "timestamp_utc": ts()},
        {"validation_id": "VAL2754_7_decision_next", "passed": decision_ok and next_ok, "detail": "2755 q operator bridge or independent Hessian selected", "timestamp_utc": ts()},
        {"validation_id": "VAL2754_8_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2754_9_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2754_10_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2754_11_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2754_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2754 keeps linear BqWeyl closure-only, rejects DqWeyl2 no-tower zero under current evidence, retains projection contract, and selects q operator bridge/Hessian next",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2754 - Y5 R2/f(R): BqWeyl Linear Revival Or DqWeyl2 No-Tower Bound Under AX1090

Status: `Y5_R2FR_2754_linear_BqWeyl_closure_only_DqWeyl2_operator_inputs_next`

## Private Verdict

2754 checks whether the linear `B_qWeyl` zero route can be revived. It cannot under the current corpus.

The index theorem is still good: scalar/quotient `q` cannot form a linear `q C_abcd` scalar without a Weyl-type spurion/projector. But there is no new parent-signed q-representation/no-spurion signature after the prior demotion. So the linear branch remains closure-only.

That leaves the honest residual:

`D_qWeyl2 q C_abcd C^abcd`

The no-tower zero route also does not close: no bare Weyl2, no integrated higher-curvature tower, and no hidden curvature morphism are all still unsigned. The Schwarzschild projection law is useful and concrete, but it is not evidence of a bound until `D_qWeyl2`, `Z_q`, range/operator normalization, body cutoff, and observable projection are supplied.

So the next bottleneck is not more Weyl prose. It is q-operator ownership: either q is absent/no-pole, q is signed as the existing X/L_X operator, or q needs its own Hessian.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Linear BqWeyl Revival Gate

{markdown_table(data["linear"], ["linear_id", "test", "statement", "current_status", "missing_for_claim", "valid_for_claim"])}

## DqWeyl2 No-Tower Zero Attempt

{markdown_table(data["tower"], ["tower_id", "zero_clause", "would_supply", "current_status", "missing_for_claim", "theorem_zero", "valid_for_claim"])}

## Schwarzschild Weyl2 Projection Gate

{markdown_table(data["projection"], ["projection_id", "quantity", "formula", "current_status", "claim_guard", "valid_for_claim"])}

## DqWeyl2 Input Contract

{markdown_table(data["input"], ["input_id", "symbol", "role", "current_status", "needed_to_promote", "valid_for_claim"])}

## Refusal Runner

{markdown_table(data["refusal"], ["refusal_id", "attempted_claim", "status", "reason", "runner_allows_claim", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim_gate", "status", "reason", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "result", "reason", "valid_for_claim"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is a useful narrowing again. Linear Weyl is not where to spend more time unless new parent-action evidence appears. Quadratic Weyl is now the active residual, but it cannot be tested until we know what q's operator actually is. The next honest lock is `q`: absent, same as X, or independent Hessian.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    linear = linear_rows()
    tower = tower_rows()
    projection = projection_rows()
    input_contract = input_rows()
    refusal = refusal_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["linear"], linear)
    write_csv(OUTPUTS["tower"], tower)
    write_csv(OUTPUTS["projection"], projection)
    write_csv(OUTPUTS["input"], input_contract)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["dqweyl2_local"], input_contract)
    write_csv(BRANCH_OUTPUTS["linear_source_weight"], linear)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, linear, tower, projection, input_contract, refusal, gates, decisions, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "linear": linear,
        "tower": tower,
        "projection": projection,
        "input": input_contract,
        "refusal": refusal,
        "gates": gates,
        "decisions": decisions,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    remove_pycache()

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2754 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
