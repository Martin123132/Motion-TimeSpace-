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
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2758-Y5-R2FR-q-zero-selector-source-current-or-Green-domain-second-fill-under-AX1090.md"
BRANCH_ID = "MTS_R2FR_AX1090_Q_ZERO_SELECTOR_GREEN_DOMAIN_2758"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2758_SOURCE_REGISTER.csv",
    "selector": RESIDUALS / "P8_Y5_R2FR_2758_SELECTOR_REENTRY_AUDIT.csv",
    "green": RESIDUALS / "P8_Y5_R2FR_2758_GREEN_DOMAIN_SECOND_FILL.csv",
    "formula": RESIDUALS / "P8_Y5_R2FR_2758_FINITE_RESIDUAL_FORMULA_UPDATE.csv",
    "arena": RESIDUALS / "P8_Y5_R2FR_2758_ARENA_READINESS_UPDATE.csv",
    "zero": RESIDUALS / "P8_Y5_R2FR_2758_ZERO_THEOREM_LADDER.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2758_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2758_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_R2FR_2758_REFUSAL_RUNNER_NONCLAIM.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2758_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2758_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2758_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "selector_queue": QUEUE / "JR2758_Q_ZERO_SELECTOR_REENTRY_AUDIT_NONCLAIM.csv",
    "green_beta": BETA_DOCS / "Q_GREEN_DOMAIN_SECOND_FILL_2758_NONCLAIM.csv",
    "formula_queue": QUEUE / "JR2758_FINITE_RESIDUAL_FORMULA_UPDATE_NONCLAIM.csv",
    "arena_local": LOCAL_BOUNDS / "q_green_domain_arena_readiness_2758_NONCLAIM.csv",
    "next_queue": QUEUE / "JR2758_JQ_SOURCE_LEG_ZERO_NEXT.csv",
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
            "source_id": "SRC2758_0_2757_doc",
            "description": "AX1090 q operator/range handoff selecting q-zero selector or Green-domain fill.",
            "source_path": "2757-Y5-R2FR-independent-q-Hessian-operator-source-or-bound-runner-first-fill-under-AX1090.md",
            "required_needles": "NEXT2757_0_2758;FF2757_2_lambda;VAL2757_OVERALL",
        },
        {
            "source_id": "SRC2758_1_2757_validation",
            "description": "2757 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2757_VALIDATION.csv",
            "required_needles": "VAL2757_OVERALL;True",
        },
        {
            "source_id": "SRC2758_2_2315_doc",
            "description": "prior q-zero selector re-entry and Green-domain second fill.",
            "source_path": "2315-Y5-R2FR-q-zero-selector-source-current-or-Green-domain-second-fill.md",
            "required_needles": "SEL2315_4_verdict;GD2315_0_massive_kernel;FORM2315_2_qR;VAL2315_OVERALL",
        },
        {
            "source_id": "SRC2758_3_2315_validation",
            "description": "2315 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2315_VALIDATION.csv",
            "required_needles": "VAL2315_OVERALL;PASS",
        },
        {
            "source_id": "SRC2758_4_2283_doc",
            "description": "radial observer-cell owner exhaustion and closure finalizer.",
            "source_path": "2283-Y5-R2FR-radial-observer-cell-current-owner-or-q-closure-finalizer.md",
            "required_needles": "RCO2283_1_ordinary_current;QCF2283_0_finalizer;VAL2283_OVERALL",
        },
        {
            "source_id": "SRC2758_5_2283_validation",
            "description": "2283 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2283_VALIDATION.csv",
            "required_needles": "VAL2283_OVERALL;PASS",
        },
        {
            "source_id": "SRC2758_6_2316_doc",
            "description": "j_q source-leg zero theorem and finite source-pack precedent.",
            "source_path": "2316-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack.md",
            "required_needles": "JQZ2316_0_definition;JQPACK2316_0_total;VAL2316_OVERALL",
        },
        {
            "source_id": "SRC2758_7_2316_validation",
            "description": "2316 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2316_VALIDATION.csv",
            "required_needles": "VAL2316_OVERALL;PASS",
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


def selector_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SEL2758_0_identity",
            "q=0 / radial observer-cell reciprocity identity",
            "EXACT_TARGET_IDENTITY",
            "q=0 iff T^2S=1 iff R_AB=0",
            "identity locates the target but does not parent-select it",
        ),
        (
            "SEL2758_1_ordinary_current",
            "conserved radial source/current",
            "REJECTED_BY_EXISTING_NO_CHARGE_OBSTRUCTION",
            "2283 shows partial_r(W partial_r R_AB)=0 gives W R_AB'=Q_R, so Q_R hair survives unless a no-charge theorem is added.",
            "do not loop this route without new parent no-charge evidence",
        ),
        (
            "SEL2758_2_topological_no_charge",
            "topological/source representation zero charge",
            "POSSIBLE_BUT_UNSUPPLIED",
            "Q_R=0 remains a future contract; no cohomology/source-representation theorem is present.",
            "eligible re-entry only if a concrete source-current theorem appears",
        ),
        (
            "SEL2758_3_first_class_or_psi",
            "first-class/gauge or psi quotient",
            "CONTRACT_ONLY_NOT_PRESENT",
            "requires generator, bracket, degree count, matter descent, or psi covariance quotient; current corpus does not supply them.",
            "keep closure label and finite-residual branch",
        ),
        (
            "SEL2758_4_verdict",
            "q-zero selector source/current re-entry",
            "NO_NEW_SELECTOR_SOURCE_FOUND_USE_GREEN_DOMAIN_FILL",
            "no post-2283 source-current theorem is found; 2757/2315 provide useful Green-domain structure instead.",
            "advance numerator/source-zero work; do not claim derived local GR",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "selector_id": row_id,
                "selector_route": route,
                "status": status,
                "evidence": evidence,
                "decision": decision,
            }
        )
        for row_id, route, status, evidence, decision in specs
    ]


def green_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "GD2758_0_massive_kernel",
            "massive covariance-Hessian branch",
            "L_q=-Z_q Delta+M_q^2, G_q(r)=exp(-r/xi_q)/(4*pi*Z_q*r) when Z_q=xi_q^2 M_q^2",
            "lambda_q is promoted from missing range input to exact conditional lambda_q=xi_q",
            "xi_q numeric/source; Z_q normalization; source vector S_q; boundary/domain; P_obs",
        ),
        (
            "GD2758_1_compact_source_profile",
            "compact source Green response",
            "q(x)=int_D G_q(x,x') S_q(x') dV'; far field scales as Q_q^eff exp(-r/xi_q)/(4*pi Z_q r)",
            "profile shape is determined once xi_q and the effective source charge are parent-owned",
            "Q_q^eff from D_qWeyl2 C^2, J_q, boundary_tail with no-cancellation envelope",
        ),
        (
            "GD2758_2_algebraic_limit",
            "algebraic/auxiliary limit",
            "if Z_q=0, q=S_q/M_q^2 and q_R=j_q/M_q^2 for weak-field source J_q=j_q L+O(L^2)",
            "using M_q^2=n_q H n_q gives q_R=j_q/(n_q H n_q) if the same branch is sourced",
            "j_q source leg, H_AB value, q normalization, source-normalization guard",
        ),
        (
            "GD2758_3_boundary_hair",
            "boundary/hair branch",
            "if reciprocal boundary momentum survives, R_AB has Q_R/r or Yukawa-tail hair depending on Z_q,M_q^2",
            "hair is an explicit source channel, not hidden inside q=0 closure",
            "boundary variational class, Pi_R/Q_R source theorem or bound",
        ),
        (
            "GD2758_4_closure_control",
            "explicit q=0 closure benchmark",
            "q=0 remains a runnable regression control only",
            "closure control separated from Green-domain finite residual predictions",
            "not scoreable as derivation; use only as labelled benchmark",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "green_id": row_id,
                "domain_piece": piece,
                "formula": formula,
                "new_fill": fill,
                "missing_for_score": missing,
                "score_ready": False,
            }
        )
        for row_id, piece, formula, fill, missing in specs
    ]


def formula_rows() -> list[dict[str, Any]]:
    specs = [
        ("FORM2758_0_Mq2", "M_q^2", "M_q^2=n_q^A H_AB n_q^B", "2757 import of 2281 transverse Hessian", "missing parent Hessian", "H_AB and q=0 selector not parent-signed"),
        ("FORM2758_1_Zq", "Z_q", "Z_q=xi_q^2 n_q^A H_AB n_q^B", "2757 import of 2281 finite smoothing expansion", "missing range/operator input", "xi_q/smoothing kernel not source-backed"),
        ("FORM2758_2_qR", "q_R", "q_R=j_q/M_q^2=j_q/(n_q^A H_AB n_q^B)", "2284/2315 q_R ratio plus 2757 M_q^2 fill", "ratio known but denominator/numerator not numeric", "j_q numerator/source leg is still missing; denominator not numeric"),
        ("FORM2758_3_zero_condition", "q_R=0", "if M_q^2>0 and j_q=0 in the same normalization, then q_R=0", "algebraic residual formula", "vague finite residual zero condition", "need parent source-current/matter-descent theorem for j_q=0"),
        ("FORM2758_4_R10_range", "R10 lambda input", "lambda_R10=xi_q for the massive covariance-Hessian q branch", "2757 lambda_q=xi_q", "lambda_q missing range input", "R10 coupling K_q Qbar_qH qbar_qT and xi_q numeric/source still missing"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "formula_id": row_id,
                "quantity": quantity,
                "formula": formula,
                "source_basis": basis,
                "upgrade_from": upgrade,
                "remaining_gap": gap,
            }
        )
        for row_id, quantity, formula, basis, upgrade, gap in specs
    ]


def arena_rows() -> list[dict[str, Any]]:
    specs = [
        ("ARENA2758_0_PPN_gamma", "PPN gamma/light/Shapiro", "gamma-1=q_R=j_q/(nHn) plus retained q_loc/source channels", "operator denominator now has conditional formula", "j_q, source normalization, q_loc projection"),
        ("ARENA2758_1_PPN_beta_orbital", "PPN beta/perihelion/orbital", "perihelion keeps q_R and delta_beta channels; q_R denominator can be nHn conditionally", "finite q channel is less foggy", "delta_beta parent weak-field completion and Newton/source normalization"),
        ("ARENA2758_2_R10", "R10 short-range alpha(lambda)", "lambda_q=xi_q conditionally; alpha_q(lambda)=K_q Qbar_qH qbar_qT remains symbolic", "range owner is narrowed to parent smoothing/correlation length", "xi_q numeric/source, K_q, Qbar/qbar couplings, real bound curve/comparator"),
        ("ARENA2758_3_clocks_WEP", "clocks/WEP/matter", "matter q-source numerator j_q is now the highest-value zero theorem target", "clear numerator-denominator split", "matter/coframe descent and universal source-current theorem"),
        ("ARENA2758_4_local_GR", "derived local GR/Newton limit", "local residual vector keeps q_R, q_loc, Q_R/boundary, delta_beta, delta_GM, curvature tail, hidden-visible hom terms", "residual vector is sharper, not empty", "j_q/source leg, boundary hair, beta/source normalization, curvature and hidden-visible channels"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "arena_id": row_id,
                "arena": arena,
                "updated_input": updated,
                "improvement": improvement,
                "still_blocked_by": blocked,
                "score_ready": False,
            }
        )
        for row_id, arena, updated, improvement, blocked in specs
    ]


def zero_rows() -> list[dict[str, Any]]:
    specs = [
        ("ZERO2758_0_selector", "q=0 from parent selector", "first-class/psi quotient or no-charge current theorem selects R_AB=0 before readout", "BLOCKED_BY_2283_NO_OWNER", "do not loop unless new parent theorem appears"),
        ("ZERO2758_1_source_numerator", "j_q=0", "matter/source/current descent has no q numerator in the same observed coframe", "OPEN_HIGHEST_VALUE_TARGET", "derive j_q source-leg zero or stage finite source pack"),
        ("ZERO2758_2_boundary_hair", "Q_R=0 / boundary q hair zero", "no-gradient/no-boundary-momentum theorem or source reciprocal neutrality", "OPEN_BOUNDARY_TARGET", "pair with j_q source-leg proof; otherwise bound Q_R separately"),
        ("ZERO2758_3_curvature_source", "D_qWeyl2=0 or bounded", "no higher-curvature tower theorem or source-backed coefficient below bounds", "OPEN_COEFFICIENT_TARGET", "do after j_q/Green-domain source channel or in parallel with R10"),
        ("ZERO2758_4_local_GR_Newton", "local GR/Newton residual vector", "selector or finite residual zeros plus source normalization and beta completion", "NOT_DERIVED", "derive numerator/source zero first, then beta/source normalization"),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "zero_id": row_id,
                "target_zero": target,
                "sufficient_conditions": conditions,
                "current_status": status,
                "next_best_attack": attack,
            }
        )
        for row_id, target, conditions, status, attack in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2758_0_selector", "selector re-entry", "NO_NEW_SELECTOR_SOURCE_FOUND", "ordinary current still leaves Q_R hair; no no-charge/first-class/psi theorem is new"),
        ("DEC2758_1_green", "Green-domain second fill", "WRITTEN_NONCLAIM", "lambda_q=xi_q and q_R=j_q/(nHn) sharpen finite residual lane"),
        ("DEC2758_2_numerator", "highest-value next derivation", "JQ_SOURCE_LEG_ZERO_OR_FINITE_PACK", "after denominator sharpening, numerator j_q controls the local residual amplitude"),
        ("DEC2758_3_scores", "empirical score status", "BLOCKED", "xi_q, j_q, D coefficients, boundary/domain, source normalization, and arena projection remain unsourced"),
        ("DEC2758_4_next", "next target", "NEXT_2759_JQ_SOURCE_LEG_ZERO_THEOREM_OR_FINITE_SOURCE_PACK", "transfer/test the conditional matter-source zero theorem in AX1090 notation and stage finite j_q channels"),
    ]
    return [nonclaim({"branch_id": BRANCH_ID, "decision_id": row_id, "decision": decision, "result": result, "reason": reason}) for row_id, decision, result, reason in specs]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2758_0_sources", "source paths and needles valid", "PASS_NONCLAIM", "audit reproducible"),
        ("GATE2758_1_selector_reentry", "new source-current selector found", "BLOCKED_NO_CLAIM", "q=0 remains closure/target, not parent theorem"),
        ("GATE2758_2_green_domain_fill", "Green-domain second fill written", "PASS_NONCLAIM", "workflow improves but remains nonclaim"),
        ("GATE2758_3_jq_numerator", "j_q zero or source-backed value", "BLOCKED_NO_CLAIM", "numerator is now the priority missing term"),
        ("GATE2758_4_arena_scores", "PPN/R10/clock/orbital score-ready", "BLOCKED_NO_CLAIM", "source/projection/coupling rows missing"),
        ("GATE2758_5_local_GR", "local GR/Newton recovery derived", "BLOCKED_NO_CLAIM", "residual vector not zeroed or bounded"),
    ]
    return [nonclaim({"claim_gate_id": row_id, "claim_gate": gate, "status": status, "reason": reason}) for row_id, gate, status, reason in specs]


def refusal_rows() -> list[dict[str, Any]]:
    specs = [
        ("REF2758_0_reloop_current", "ordinary conserved radial current derives q=0", "BLOCKED", "2283 already rejected this route because Q_R hair survives"),
        ("REF2758_1_claim_lambda_numeric", "lambda_q=xi_q is a numeric R10 prediction", "BLOCKED", "xi_q is not sourced numerically and couplings/projection are missing"),
        ("REF2758_2_score_ppn", "PPN/local tests can be scored now", "BLOCKED", "q_R numerator j_q and source-normalization channels remain missing"),
        ("REF2758_3_local_gr", "MTS derives local GR/Newton after Green-domain fill", "BLOCKED", "Green-domain fill is a residual workflow, not a selector/source-zero theorem"),
    ]
    return [nonclaim({"branch_id": BRANCH_ID, "refusal_id": row_id, "attempted_claim": claim, "status": status, "reason": reason, "runner_allows_claim": False}) for row_id, claim, status, reason in specs]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2758_0_2759",
                "status": "selected_primary",
                "target_doc": "2759-Y5-R2FR-jq-source-leg-zero-theorem-or-finite-source-pack-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_jq_source_leg_zero_theorem_or_finite_source_pack_under_AX1090_2759.py",
                "mission": "derive or reject j_q=0 in the current q_R=j_q/(nHn) branch; transfer the conditional MOMS matter-zero theorem if applicable, then stage finite j_q channels for constants, weights, shadow frames, readout, boundary, curvature, and hidden-visible maps",
                "acceptance": "either a parent-signed j_q zero theorem in the same branch or a complete nonclaim finite-source pack with all live numerator channels and claim gates blocked",
                "forbidden": "do not claim local GR/Newton, do not use experimental bounds as coefficients, do not score without sourced numerator/denominator/projection, do not edit formalization-workbench, no GitHub action",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2758_0_selector_queue", "source_table": rel(OUTPUTS["selector"]), "copy_path": rel(BRANCH_OUTPUTS["selector_queue"]), "purpose": "selector re-entry audit", "exists": BRANCH_OUTPUTS["selector_queue"].exists()}),
        nonclaim({"copy_id": "BR2758_1_green_beta", "source_table": rel(OUTPUTS["green"]), "copy_path": rel(BRANCH_OUTPUTS["green_beta"]), "purpose": "Green-domain second fill", "exists": BRANCH_OUTPUTS["green_beta"].exists()}),
        nonclaim({"copy_id": "BR2758_2_formula_queue", "source_table": rel(OUTPUTS["formula"]), "copy_path": rel(BRANCH_OUTPUTS["formula_queue"]), "purpose": "finite residual formula update", "exists": BRANCH_OUTPUTS["formula_queue"].exists()}),
        nonclaim({"copy_id": "BR2758_3_arena_local", "source_table": rel(OUTPUTS["arena"]), "copy_path": rel(BRANCH_OUTPUTS["arena_local"]), "purpose": "local-bound arena readiness update", "exists": BRANCH_OUTPUTS["arena_local"].exists()}),
        nonclaim({"copy_id": "BR2758_4_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB queue for j_q source-leg zero", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
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
    selector: list[dict[str, Any]],
    green: list[dict[str, Any]],
    formula: list[dict[str, Any]],
    arena: list[dict[str, Any]],
    zero: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    selector_ok = any(row["selector_id"] == "SEL2758_4_verdict" and row["status"] == "NO_NEW_SELECTOR_SOURCE_FOUND_USE_GREEN_DOMAIN_FILL" for row in selector)
    green_ok = any(row["green_id"] == "GD2758_0_massive_kernel" and "exp(-r/xi_q)" in row["formula"] for row in green)
    formula_ok = any(row["formula_id"] == "FORM2758_2_qR" and "j_q/(n_q^A H_AB n_q^B)" in row["formula"] for row in formula)
    arena_ok = all(row["score_ready"] is False for row in arena) and any(row["arena_id"] == "ARENA2758_4_local_GR" for row in arena)
    zero_ok = any(row["zero_id"] == "ZERO2758_1_source_numerator" and row["current_status"] == "OPEN_HIGHEST_VALUE_TARGET" for row in zero)
    decision_ok = any(row["decision_id"] == "DEC2758_4_next" and row["result"] == "NEXT_2759_JQ_SOURCE_LEG_ZERO_THEOREM_OR_FINITE_SOURCE_PACK" for row in decisions)
    gates_ok = any(row["claim_gate_id"] == "GATE2758_5_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    refusal_ok = all(row["runner_allows_claim"] is False for row in refusal)
    next_ok = next_target[0]["selected"] is True and "2759" in next_target[0]["target_doc"]
    no_claim_flags_ok = all(
        row.get("valid_for_claim") is False and row.get("claim_allowed") is False
        for block in [selector, green, formula, arena, zero, decisions, gates, refusal, next_target]
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
        {"validation_id": "VAL2758_0_sources", "passed": source_ok, "detail": "all source paths exist and needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2758_1_selector_reentry_blocked", "passed": selector_ok, "detail": "selector/current re-entry is blocked by existing evidence", "timestamp_utc": ts()},
        {"validation_id": "VAL2758_2_green_domain", "passed": green_ok, "detail": "Green-domain second fill records lambda_q=xi_q", "timestamp_utc": ts()},
        {"validation_id": "VAL2758_3_formula_update", "passed": formula_ok, "detail": "finite q residual formula updated to q_R=j_q/(nHn)", "timestamp_utc": ts()},
        {"validation_id": "VAL2758_4_arena_blocks", "passed": arena_ok, "detail": "all arena rows remain blocked/nonclaim", "timestamp_utc": ts()},
        {"validation_id": "VAL2758_5_zero_ladder", "passed": zero_ok, "detail": "j_q numerator is selected as highest-value zero theorem target", "timestamp_utc": ts()},
        {"validation_id": "VAL2758_6_next", "passed": decision_ok and next_ok, "detail": "2759 j_q source-leg zero theorem selected", "timestamp_utc": ts()},
        {"validation_id": "VAL2758_7_claim_gates", "passed": gates_ok and no_claim_flags_ok, "detail": "local GR/Newton and generated claim flags remain blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2758_8_refusal_runner", "passed": refusal_ok, "detail": "refusal runner blocks selector/lambda/scoring/local-GR claims", "timestamp_utc": ts()},
        {"validation_id": "VAL2758_9_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2758_10_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2758_11_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2758_12_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2758_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2758 refuses to re-loop the source-current selector without new evidence, uses lambda_q=xi_q to fill the Green-domain lane conditionally, updates q_R to j_q/(nHn), keeps all arena scores blocked, and selects the j_q source-leg zero theorem as the next derivation target.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2758 - Y5 R2/f(R): q-Zero Selector Source-Current Or Green-Domain Second Fill Under AX1090

Status: `Y5_R2FR_2758_selector_reentry_blocked_green_domain_second_fill_nonclaim`

## Private Verdict

2758 refuses the tempting loop. The ordinary radial-cell current route still gives `Q_R` hair, not `Q_R=0`, and there is no new no-charge, first-class, gauge-quotient, or psi-quotient theorem in the inspected chain. So `q=0` remains an explicit closure/target, not a derived local-GR selector.

The useful forward move is the finite residual lane. With the 2757 conditional operator fill,

`M_q^2 = n_q^A H_AB n_q^B`, `Z_q = xi_q^2 n_q^A H_AB n_q^B`, and `lambda_q = xi_q`.

That sharpens the local residual formula to:

`q_R = j_q / (n_q^A H_AB n_q^B)`.

So the numerator `j_q` is now the highest-value derivation target. If `j_q=0` closes in the same branch, the local residual shrinks sharply. If it does not, `j_q` becomes the finite source pack that must be bounded before PPN/R10/clock/orbital scoring.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## Selector Re-Entry Audit

{markdown_table(data["selector"], ["selector_id", "selector_route", "status", "evidence", "decision", "valid_for_claim"])}

## Green-Domain Second Fill

{markdown_table(data["green"], ["green_id", "domain_piece", "formula", "new_fill", "missing_for_score", "score_ready", "valid_for_claim"])}

## Finite Residual Formula Update

{markdown_table(data["formula"], ["formula_id", "quantity", "formula", "source_basis", "upgrade_from", "remaining_gap", "valid_for_claim"])}

## Arena Readiness Update

{markdown_table(data["arena"], ["arena_id", "arena", "updated_input", "improvement", "still_blocked_by", "score_ready", "valid_for_claim"])}

## Zero Theorem Ladder

{markdown_table(data["zero"], ["zero_id", "target_zero", "sufficient_conditions", "current_status", "next_best_attack", "valid_for_claim"])}

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

This is the numerator pivot. The denominator is now conditionally intelligible; the selector is still not derived. The next serious attack is `j_q`: prove the q source leg vanishes, or decompose every live coupling channel and carry it into finite residual tests.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    selector = selector_rows()
    green = green_rows()
    formula = formula_rows()
    arena = arena_rows()
    zero = zero_rows()
    decisions = decision_rows()
    gates = gate_rows()
    refusal = refusal_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["selector"], selector)
    write_csv(OUTPUTS["green"], green)
    write_csv(OUTPUTS["formula"], formula)
    write_csv(OUTPUTS["arena"], arena)
    write_csv(OUTPUTS["zero"], zero)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["selector_queue"], selector)
    write_csv(BRANCH_OUTPUTS["green_beta"], green)
    write_csv(BRANCH_OUTPUTS["formula_queue"], formula)
    write_csv(BRANCH_OUTPUTS["arena_local"], arena)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, selector, green, formula, arena, zero, decisions, gates, refusal, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "selector": selector,
        "green": green,
        "formula": formula,
        "arena": arena,
        "zero": zero,
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
        raise SystemExit(f"2758 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
