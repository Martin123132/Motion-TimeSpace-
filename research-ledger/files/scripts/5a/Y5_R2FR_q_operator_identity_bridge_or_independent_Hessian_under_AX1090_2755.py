from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2755-Y5-R2FR-q-operator-identity-bridge-or-independent-Hessian-under-AX1090.md"
BRANCH_ID = "MTS_R2FR_AX1090_Q_OPERATOR_BRANCH_2755"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2755_SOURCE_REGISTER.csv",
    "no_pole": RESIDUALS / "P8_Y5_R2FR_2755_NO_POLE_ACTIVATION_GATE.csv",
    "bridge": RESIDUALS / "P8_Y5_R2FR_2755_QX_BRIDGE_GATE.csv",
    "independent": RESIDUALS / "P8_Y5_R2FR_2755_INDEPENDENT_Q_HESSIAN_SOURCE_PACK.csv",
    "activation": RESIDUALS / "P8_Y5_R2FR_2755_DQWEYL2_RUNNER_ACTIVATION_GATE.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2755_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2755_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_R2FR_2755_REFUSAL_RUNNER_NONCLAIM.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2755_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2755_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2755_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "decision_queue": QUEUE / "JR2755_Q_OPERATOR_BRANCH_DECISION_NONCLAIM.csv",
    "independent_local": LOCAL_BOUNDS / "q_independent_hessian_source_pack_2755_NONCLAIM.csv",
    "no_pole_beta": BETA_DOCS / "Q_NO_POLE_ACTIVATION_GATE_2755_NONCLAIM.csv",
    "bridge_source_weight": SOURCE_WEIGHT / "QX_BRIDGE_PULLBACK_BLOCK_2755_NONCLAIM.csv",
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
            "source_id": "SRC2755_0_2754_doc",
            "description": "2754 selected q operator ownership as the active bottleneck.",
            "source_path": "2754-Y5-R2FR-BqWeyl-linear-revival-or-DqWeyl2-no-tower-bound-under-AX1090.md",
            "required_needles": "NEXT2754_0_2755;IN2754_1_Zq;DEC2754_3_next",
        },
        {
            "source_id": "SRC2755_1_2754_validation",
            "description": "2754 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2754_VALIDATION.csv",
            "required_needles": "VAL2754_OVERALL;True",
        },
        {
            "source_id": "SRC2755_2_2309_doc",
            "description": "prior q-X trichotomy and independent q Hessian row.",
            "source_path": "2309-Y5-R2FR-q-X-operator-identity-bridge-or-independent-q-Hessian.md",
            "required_needles": "TRI2309_4_verdict;QX_BRIDGE_NOT_ACTIVATED;IQH2309_0_Zq;VAL2309_OVERALL",
        },
        {
            "source_id": "SRC2755_3_2309_validation",
            "description": "2309 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2309_VALIDATION.csv",
            "required_needles": "VAL2309_OVERALL;PASS",
        },
        {
            "source_id": "SRC2755_4_2310_doc",
            "description": "prior no-pole primary route and fallback q Hessian source pack.",
            "source_path": "2310-Y5-R2FR-q-branch-selection-no-pole-or-independent-Hessian-first-source-row.md",
            "required_needles": "NP2310_6_activation_verdict;NO_POLE_NOT_ACTIVATED_CURRENT;IQSRC2310_1_Zq;NEXT2310_0",
        },
        {
            "source_id": "SRC2755_5_2310_validation",
            "description": "2310 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2310_VALIDATION.csv",
            "required_needles": "VAL2310_OVERALL;PASS",
        },
        {
            "source_id": "SRC2755_6_2308_doc",
            "description": "minimal q local action normal form and unsourced operator verdict.",
            "source_path": "2308-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md",
            "required_needles": "QOP2308_4_verdict;Q_OPERATOR_UNSOURCED;NF2308_0_minimal_action",
        },
        {
            "source_id": "SRC2755_7_2753_doc",
            "description": "first finite q_R component handoff into Weyl residual accounting.",
            "source_path": "2753-Y5-R2FR-first-finite-qR-component-bound-or-source-zero-theorem-under-AX1090.md",
            "required_needles": "FC2753_1_DqWeyl2;PBOUND2753_0_qR;VAL2753_OVERALL",
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


def no_pole_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "NP2755_0_exact_contract",
            "conditional q no-pole theorem",
            "If the parent action, matter action, readouts, measure/coframe, and boundary term descend through a quotient pi, and q lies only in the removed vertical/first-class directions, then the reduced physical Hessian has no q row/column and physical Green functions contain no q pole.",
            "EXACT_CONDITIONAL_THEOREM",
            "one-branch parent certificate",
        ),
        (
            "NP2755_1_parent_quotient_object",
            "q/quotient map is parent-defined before variation",
            "q(Phi) or pi: Y -> Y_red must be a real parent object with units/domain, not a post-hoc residual label.",
            "NOT_SIGNED",
            "parent quotient map source",
        ),
        (
            "NP2755_2_vertical_generator_degree_count",
            "actual vertical generator and degree count",
            "The local q direction must be generated by a first-class/vertical vector in ker(Dpi), with symplectic bracket closure and removed canonical pair count.",
            "NOT_SIGNED",
            "Omega, generator, bracket, and degree-count package",
        ),
        (
            "NP2755_3_action_matter_readout_descent",
            "action, matter, and observables factor through the quotient",
            "S=Sbar∘pi, S_matter=Sbar_matter∘pi, and observable maps O=Obar∘pi must all use the same branch.",
            "NOT_SIGNED",
            "single-branch descent certificate",
        ),
        (
            "NP2755_4_boundary_source_silence",
            "boundary/local projection silence",
            "Removed q directions must not leave boundary charges, source tails, or local projection/readout remnants.",
            "NOT_SIGNED",
            "theta-boundary-source neutrality proof",
        ),
        (
            "NP2755_5_activation_verdict",
            "activate no-pole branch",
            "All no-pole clauses must pass together before D_qWeyl2 and q Green rows can be deleted rather than bounded.",
            "NO_POLE_NOT_ACTIVATED_CURRENT",
            "NP2755_1 through NP2755_4 remain unsigned",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "no_pole_id": row_id,
                "clause": clause,
                "content": content,
                "current_status": status,
                "needed_to_close": needed,
                "theorem_activated": False,
            }
        )
        for row_id, clause, content, status, needed in specs
    ]


def bridge_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "QXB2755_0_q_equals_X_map",
            "q=aX identity/projection",
            "Parent source must identify q with X on the same local branch, not merely show Dq[v_X]=0 for a vertical direction.",
            "NOT_SIGNED",
            "q=aX source row with nonzero scale a",
        ),
        (
            "QXB2755_1_scale_units",
            "scale and units",
            "The bridge scale a must carry units so Z_q=Z_X/a^2, M_q^2=M_X^2/a^2, D_qWeyl2=D_XWeyl2/a can be used consistently.",
            "MISSING_PARENT_SCALE",
            "scale a, units, uncertainty, sign convention",
        ),
        (
            "QXB2755_2_same_domain_boundary",
            "same domain and boundary problem",
            "q and X must share boundary terms, branch domain, and source/readout convention.",
            "NOT_SIGNED",
            "domain/boundary/readout bridge",
        ),
        (
            "QXB2755_3_X_operator_owned",
            "X operator values parent-owned",
            "Even if q=aX were signed, Z_X, M_X^2, lambda_X, K_X, and source charges are not claim-grade in the current corpus.",
            "NOT_SIGNED",
            "X Hessian/operator source pack",
        ),
        (
            "QXB2755_4_activation_verdict",
            "activate q-X operator bridge",
            "Current evidence cannot copy L_X to L_q; the pullback formulas remain exact but inactive.",
            "QX_BRIDGE_NOT_ACTIVATED",
            "QXB2755_0 through QXB2755_3",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "bridge_id": row_id,
                "gate": gate,
                "content": content,
                "current_status": status,
                "needed_to_close": needed,
                "bridge_activated": False,
            }
        )
        for row_id, gate, content, status, needed in specs
    ]


def independent_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "IQH2755_0_Zq",
            "Z_q",
            "q kinetic Hessian/operator normalization",
            "delta_q^2 S_parent contains 1/2 Z_q |nabla q|^2 in a sourced q normalization",
            "MISSING_PARENT_HESSIAN",
        ),
        (
            "IQH2755_1_Mq2_lambda",
            "M_q^2/lambda_q",
            "q mass/gap and range",
            "lambda_q=sqrt(Z_q/M_q^2) for positive massive branch; massless branch needs a domain/no-hair theorem",
            "MISSING_PARENT_HESSIAN_OR_RANGE",
        ),
        (
            "IQH2755_2_DqWeyl2",
            "D_qWeyl2",
            "q coupling to Weyl-squared curvature source",
            "parent action coefficient for q C_abcd C^abcd or theorem-zero/no-tower proof in the same normalization",
            "MISSING_PARENT_COEFFICIENT",
        ),
        (
            "IQH2755_3_Jq_boundary",
            "J_q and boundary/source tail",
            "non-Weyl source, boundary tail, and matter/readout residues",
            "matter/coframe descent or bounded source rows",
            "MISSING_SOURCE_ZERO_OR_BOUND",
        ),
        (
            "IQH2755_4_Parena",
            "P_arena[q]",
            "observable projection into PPN/R10/orbital/clocks",
            "arena-specific projection from q profile into metric potentials, acceleration, clock/alpha, or short-range alpha(lambda)",
            "MISSING_OBSERVABLE_MAP",
        ),
        (
            "IQH2755_5_claim_gate",
            "independent q Hessian branch",
            "fallback branch if no-pole and q-X bridge both fail",
            "all preceding rows numeric/source-backed or theorem-zero in one normalization",
            "CLAIM_BLOCKED",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "hessian_id": row_id,
                "symbol": symbol,
                "role": role,
                "required_source_or_formula": required,
                "current_status": status,
            }
        )
        for row_id, symbol, role, required, status in specs
    ]


def activation_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DACT2755_0_runner_status",
            "D_qWeyl2 projection/scoring runner",
            "NOT_EXECUTABLE",
            "q operator ownership is not resolved: no-pole inactive, q-X bridge inactive, independent Hessian inputs missing",
        ),
        (
            "DACT2755_1_delete_route",
            "delete q rows by no-pole",
            "BLOCKED",
            "NP2755_5 is not activated",
        ),
        (
            "DACT2755_2_borrow_route",
            "borrow X/L_X operator",
            "BLOCKED",
            "QXB2755_4 is not activated and X-side values are missing",
        ),
        (
            "DACT2755_3_bound_route",
            "bound independent q residual",
            "BLOCKED",
            "IQH2755 source pack is missing Z_q, M_q^2/lambda_q, D_qWeyl2, J_q, and P_arena",
        ),
        (
            "DACT2755_4_local_GR_status",
            "derived local GR/Newton from q branch",
            "BLOCKED_NO_CLAIM",
            "the clean route is identified, but the parent q-removal certificate is not signed",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "activation_id": row_id,
                "target": target,
                "current_status": status,
                "reason": reason,
            }
        )
        for row_id, target, status, reason in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2755_0_no_pole",
            "no-pole/quotient removal route",
            "PRIMARY_DERIVATION_TARGET_NOT_CLAIM",
            "least-scrutiny route to local GR because it removes the q pole rather than tuning a new scalar",
        ),
        (
            "DEC2755_1_qX_bridge",
            "q-X operator bridge",
            "INACTIVE_EXACT_FORMULAS_ONLY",
            "pullback laws are ready, but bridge scale/domain/source and X values are unsigned",
        ),
        (
            "DEC2755_2_independent",
            "independent q Hessian",
            "FALLBACK_SOURCE_PACK_ONLY",
            "honest bound route if q is physical, but no claim-grade inputs exist yet",
        ),
        (
            "DEC2755_3_dqweyl2",
            "D_qWeyl2 runner",
            "KEEP_SYMBOLIC_DO_NOT_SCORE",
            "operator ownership is unresolved",
        ),
        (
            "DEC2755_4_next",
            "next target",
            "NEXT_2756_PARENT_Q_REMOVAL_CERTIFICATE_OR_Q_HESSIAN_SOURCE_PACK",
            "try to sign the parent q-removal certificate in one branch; if any clause fails, immediately emit the fallback q-Hessian bound pack",
        ),
    ]
    return [nonclaim({"branch_id": BRANCH_ID, "decision_id": row_id, "decision": decision, "result": result, "reason": reason}) for row_id, decision, result, reason in specs]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2755_0_no_pole", "q no-pole activation", "BLOCKED_NO_CLAIM", "parent quotient/vertical/descent/boundary package unsigned"),
        ("GATE2755_1_qX_bridge", "q-X bridge activation", "BLOCKED_NO_CLAIM", "q=aX scale/domain/source bridge unsigned"),
        ("GATE2755_2_independent_hessian", "independent q Hessian source pack", "BLOCKED_NO_CLAIM", "Z_q/M_q^2/D_qWeyl2/J_q/P_arena missing"),
        ("GATE2755_3_dqweyl2_runner", "D_qWeyl2 local runner", "BLOCKED_NO_CLAIM", "operator branch unresolved"),
        ("GATE2755_4_local_GR", "derived local GR/Newton", "BLOCKED_NO_CLAIM", "q-removal not parent-signed"),
        ("GATE2755_5_public", "public/GitHub update", "BLOCKED_NO_CLAIM", "private derivability checkpoint only"),
    ]
    return [nonclaim({"claim_gate_id": row_id, "claim_gate": gate, "status": status, "reason": reason}) for row_id, gate, status, reason in specs]


def refusal_rows() -> list[dict[str, Any]]:
    specs = [
        ("REF2755_0_score", "score D_qWeyl2 residual now", "BLOCKED", "no q operator branch is claim-grade"),
        ("REF2755_1_delete", "delete q residual by no-pole theorem", "BLOCKED", "no-pole certificate not signed"),
        ("REF2755_2_borrow", "copy X/L_X values into q", "BLOCKED", "q-X bridge inactive and X values missing"),
        ("REF2755_3_public", "claim derived local GR/Newton", "BLOCKED", "q branch is a route decision, not a proof"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row_id,
                "attempted_claim": claim,
                "status": status,
                "reason": reason,
                "runner_allows_claim": False,
            }
        )
        for row_id, claim, status, reason in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2755_0_2756",
                "status": "selected_primary",
                "target_doc": "2756-Y5-R2FR-parent-q-removal-certificate-single-branch-saturation-or-independent-q-Hessian-source-pack-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_parent_q_removal_certificate_single_branch_saturation_or_independent_q_Hessian_source_pack_under_AX1090_2756.py",
                "mission": "attempt the one-branch q-removal certificate: parent quotient object, actual vertical generator, first-class degree count, action/matter/readout descent, and boundary/source neutrality; if any clause stays unsigned, emit the independent q Hessian bound-source pack without scoring",
                "acceptance": "either no-pole theorem activated by a single signed parent certificate, or a complete nonclaim fallback pack listing Z_q, M_q^2/lambda_q, D_qWeyl2, J_q, P_arena, and source paths still missing",
                "forbidden": "do not score D_qWeyl2, do not borrow X operator values, do not claim local GR/Newton, do not edit formalization-workbench, no GitHub action",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2755_0_decision_queue", "source_table": rel(OUTPUTS["decisions"]), "copy_path": rel(BRANCH_OUTPUTS["decision_queue"]), "purpose": "RAB queue for q branch decision", "exists": BRANCH_OUTPUTS["decision_queue"].exists()}),
        nonclaim({"copy_id": "BR2755_1_independent_local", "source_table": rel(OUTPUTS["independent"]), "copy_path": rel(BRANCH_OUTPUTS["independent_local"]), "purpose": "local-bound independent q Hessian source pack", "exists": BRANCH_OUTPUTS["independent_local"].exists()}),
        nonclaim({"copy_id": "BR2755_2_no_pole_beta", "source_table": rel(OUTPUTS["no_pole"]), "copy_path": rel(BRANCH_OUTPUTS["no_pole_beta"]), "purpose": "no-pole theorem gate handoff", "exists": BRANCH_OUTPUTS["no_pole_beta"].exists()}),
        nonclaim({"copy_id": "BR2755_3_bridge_source_weight", "source_table": rel(OUTPUTS["bridge"]), "copy_path": rel(BRANCH_OUTPUTS["bridge_source_weight"]), "purpose": "source-weight q-X bridge block", "exists": BRANCH_OUTPUTS["bridge_source_weight"].exists()}),
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
    no_pole: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    independent: list[dict[str, Any]],
    activation: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    no_pole_ok = any(row["no_pole_id"] == "NP2755_5_activation_verdict" and row["current_status"] == "NO_POLE_NOT_ACTIVATED_CURRENT" for row in no_pole)
    bridge_ok = any(row["bridge_id"] == "QXB2755_4_activation_verdict" and row["current_status"] == "QX_BRIDGE_NOT_ACTIVATED" for row in bridge)
    independent_ok = {"Z_q", "M_q^2/lambda_q", "D_qWeyl2", "J_q and boundary/source tail", "P_arena[q]"}.issubset({row["symbol"] for row in independent})
    activation_ok = any(row["activation_id"] == "DACT2755_0_runner_status" and row["current_status"] == "NOT_EXECUTABLE" for row in activation) and any(row["activation_id"] == "DACT2755_4_local_GR_status" and row["current_status"] == "BLOCKED_NO_CLAIM" for row in activation)
    decision_ok = any(row["decision_id"] == "DEC2755_4_next" and row["result"] == "NEXT_2756_PARENT_Q_REMOVAL_CERTIFICATE_OR_Q_HESSIAN_SOURCE_PACK" for row in decisions)
    gates_ok = all(row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    refusal_ok = all(row["runner_allows_claim"] is False for row in refusal)
    next_ok = next_target[0]["selected"] is True and "2756" in next_target[0]["target_doc"]
    no_claim_flags_ok = all(
        row.get("valid_for_claim") is False and row.get("claim_allowed") is False
        for block in [no_pole, bridge, independent, activation, decisions, gates, refusal, next_target]
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
        {"validation_id": "VAL2755_0_sources", "passed": source_ok, "detail": "all source paths exist and needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2755_1_no_pole_not_activated", "passed": no_pole_ok, "detail": "q no-pole theorem remains exact-conditional but not parent-signed", "timestamp_utc": ts()},
        {"validation_id": "VAL2755_2_qx_bridge_blocked", "passed": bridge_ok, "detail": "q-X bridge remains inactive", "timestamp_utc": ts()},
        {"validation_id": "VAL2755_3_independent_pack", "passed": independent_ok, "detail": "independent q Hessian fallback source pack is complete and nonclaim", "timestamp_utc": ts()},
        {"validation_id": "VAL2755_4_runner_blocked", "passed": activation_ok, "detail": "DqWeyl2 runner and local GR claim remain blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2755_5_decision_next", "passed": decision_ok and next_ok, "detail": "2756 q-removal certificate or independent Hessian pack selected", "timestamp_utc": ts()},
        {"validation_id": "VAL2755_6_claim_gates", "passed": gates_ok and no_claim_flags_ok, "detail": "all claim gates remain closed and all generated rows are nonclaim", "timestamp_utc": ts()},
        {"validation_id": "VAL2755_7_refusal_runner", "passed": refusal_ok, "detail": "refusal runner blocks scoring/deleting/borrowing/public claims", "timestamp_utc": ts()},
        {"validation_id": "VAL2755_8_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2755_9_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2755_10_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2755_11_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2755_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2755 blocks q-X borrowing, keeps no-pole as the primary derivation target but not activated, stages independent q Hessian fallback inputs, and selects the 2756 single-branch q-removal certificate attempt.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2755 - Y5 R2/f(R): q Operator Identity Bridge Or Independent Hessian Under AX1090

Status: `Y5_R2FR_2755_q_operator_branch_unresolved_no_claim`

## Private Verdict

2755 turns the q-operator bottleneck into a clean branch decision.

There are only three honest routes:

1. `q` has no physical pole because it is removed by a parent quotient/first-class reduction.
2. `q=aX` is parent-signed, so the existing `X/L_X` operator can be pulled back with a real scale and shared boundary/source convention.
3. `q` is an independent physical variable and must carry its own Hessian block: `Z_q`, `M_q^2/lambda_q`, `D_qWeyl2`, `J_q`, and `P_arena[q]`.

Current corpus status: route 1 is the best derivation target but is not activated; route 2 is blocked; route 3 is only a fallback source pack. Therefore `D_qWeyl2` remains symbolic and no local-GR/Newton claim is allowed.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## No-Pole Activation Gate

{markdown_table(data["no_pole"], ["no_pole_id", "clause", "content", "current_status", "needed_to_close", "theorem_activated", "valid_for_claim"])}

## q-X Bridge Gate

{markdown_table(data["bridge"], ["bridge_id", "gate", "content", "current_status", "needed_to_close", "bridge_activated", "valid_for_claim"])}

## Independent q Hessian Source Pack

{markdown_table(data["independent"], ["hessian_id", "symbol", "role", "required_source_or_formula", "current_status", "valid_for_claim"])}

## DqWeyl2 Runner Activation Gate

{markdown_table(data["activation"], ["activation_id", "target", "current_status", "reason", "valid_for_claim"])}

## Decision Ledger

{markdown_table(data["decisions"], ["decision_id", "decision", "result", "reason", "valid_for_claim"])}

## Claim Gates

{markdown_table(data["gates"], ["claim_gate_id", "claim_gate", "status", "reason", "valid_for_claim"])}

## Refusal Runner

{markdown_table(data["refusal"], ["refusal_id", "attempted_claim", "status", "reason", "runner_allows_claim", "valid_for_claim"])}

## Next Target

{markdown_table(data["next"], ["next_id", "status", "target_doc", "target_script", "mission", "acceptance", "forbidden", "selected", "valid_for_claim"])}

## Branch Copies

{markdown_table(data["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{markdown_table(data["validation"], ["validation_id", "passed", "detail", "timestamp_utc"])}

## Plain-English Read

This is not a victory lap, but it is a real sharpening. The q problem has stopped being foggy. We now know exactly what must happen: either prove q disappears before local physics, prove q is the same operator as X, or give q its own sourced Hessian. The best route is the first one. The next step is to try to sign the parent q-removal certificate in one branch; if it refuses to sign, we fall back to the independent Hessian pack rather than smuggling anything in.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    no_pole = no_pole_rows()
    bridge = bridge_rows()
    independent = independent_rows()
    activation = activation_rows()
    decisions = decision_rows()
    gates = gate_rows()
    refusal = refusal_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["no_pole"], no_pole)
    write_csv(OUTPUTS["bridge"], bridge)
    write_csv(OUTPUTS["independent"], independent)
    write_csv(OUTPUTS["activation"], activation)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["decision_queue"], decisions)
    write_csv(BRANCH_OUTPUTS["independent_local"], independent)
    write_csv(BRANCH_OUTPUTS["no_pole_beta"], no_pole)
    write_csv(BRANCH_OUTPUTS["bridge_source_weight"], bridge)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, no_pole, bridge, independent, activation, decisions, gates, refusal, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "no_pole": no_pole,
        "bridge": bridge,
        "independent": independent,
        "activation": activation,
        "decisions": decisions,
        "gates": gates,
        "refusal": refusal,
        "next": next_target,
        "branches": branches,
        "validation": validation,
    }
    write_doc(data)

    remove_pycache()

    if not all(row["passed"] is True for row in validation):
        failed = [row for row in validation if row["passed"] is not True]
        raise SystemExit(f"2755 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
