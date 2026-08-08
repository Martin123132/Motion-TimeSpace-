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

DOC = ROOT / "2757-Y5-R2FR-independent-q-Hessian-operator-source-or-bound-runner-first-fill-under-AX1090.md"
BRANCH_ID = "MTS_R2FR_AX1090_INDEPENDENT_Q_OPERATOR_FILL_2757"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2757_SOURCE_REGISTER.csv",
    "hunt": RESIDUALS / "P8_Y5_R2FR_2757_Q_OPERATOR_SOURCE_HUNT.csv",
    "first_fill": RESIDUALS / "P8_Y5_R2FR_2757_Q_OPERATOR_FIRST_FILL_ROWS.csv",
    "green": RESIDUALS / "P8_Y5_R2FR_2757_GREEN_FUNCTION_NORMALIZATION_CONTRACT.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2757_BOUND_RUNNER_UPDATE.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_2757_DECISION_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2757_CLAIM_GATES.csv",
    "refusal": RESIDUALS / "P8_Y5_R2FR_2757_REFUSAL_RUNNER_NONCLAIM.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2757_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2757_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2757_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "first_fill_queue": QUEUE / "JR2757_Q_OPERATOR_FIRST_FILL_CONDITIONAL_NONCLAIM.csv",
    "green_beta": BETA_DOCS / "Q_GREEN_FUNCTION_NORMALIZATION_CONTRACT_2757_NONCLAIM.csv",
    "runner_local": LOCAL_BOUNDS / "q_bound_runner_update_2757_NONCLAIM.csv",
    "next_queue": QUEUE / "JR2757_Q_ZERO_SELECTOR_OR_GREEN_DOMAIN_NEXT.csv",
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
            "source_id": "SRC2757_0_2756_doc",
            "description": "AX1090 independent-q operator source first-fill handoff.",
            "source_path": "2756-Y5-R2FR-parent-q-removal-certificate-single-branch-saturation-or-independent-q-Hessian-source-pack-under-AX1090.md",
            "required_needles": "NEXT2756_0_2757;FB2756_1_Zq;VAL2756_OVERALL",
        },
        {
            "source_id": "SRC2757_1_2756_validation",
            "description": "2756 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2756_VALIDATION.csv",
            "required_needles": "VAL2756_OVERALL;True",
        },
        {
            "source_id": "SRC2757_2_2314_doc",
            "description": "prior conditional q Hessian/operator first-fill.",
            "source_path": "2314-Y5-R2FR-independent-q-Hessian-operator-source-or-bound-runner-first-fill.md",
            "required_needles": "HUNT2314_1_conditional_mass;HUNT2314_2_conditional_stiffness;FF2314_2_lambda;VAL2314_OVERALL",
        },
        {
            "source_id": "SRC2757_3_2314_validation",
            "description": "2314 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2314_VALIDATION.csv",
            "required_needles": "VAL2314_OVERALL;PASS",
        },
        {
            "source_id": "SRC2757_4_2281_doc",
            "description": "covariance Hessian conditional q stiffness derivation.",
            "source_path": "2281-Y5-R2FR-q-stiffness-parent-sector-or-no-go.md",
            "required_needles": "QSD2281_2_transverse_q_mass;QSD2281_3_gradient_expansion;VAL2281_OVERALL",
        },
        {
            "source_id": "SRC2757_5_2281_validation",
            "description": "2281 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2281_VALIDATION.csv",
            "required_needles": "VAL2281_OVERALL;PASS",
        },
        {
            "source_id": "SRC2757_6_2282_doc",
            "description": "q=0 selector equivalence and closure guard.",
            "source_path": "2282-Y5-R2FR-covariance-equilibrium-selector-or-q-closure-declaration.md",
            "required_needles": "QOE2282_1_q_zero_to_reciprocity;QCD2282_0_status;VAL2282_OVERALL",
        },
        {
            "source_id": "SRC2757_7_2282_validation",
            "description": "2282 validation output.",
            "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2282_VALIDATION.csv",
            "required_needles": "VAL2282_OVERALL;PASS",
        },
        {
            "source_id": "SRC2757_8_2308_normal",
            "description": "formal q action/equation normal form and range formula.",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2308_Q_LOCAL_ACTION_NORMAL_FORM_CONTRACT.csv",
            "required_needles": "NF2308_0_minimal_action;NF2308_2_range",
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


def hunt_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "HUNT2757_0_prior_gap",
            "q Hessian/operator first fill",
            "PRIOR_RUNNER_GAP_CONFIRMED",
            "2756 marks Z_q and M_q^2/lambda_q missing and selects operator ownership first.",
            "continue independent-q bound runner as private nonclaim lane",
        ),
        (
            "HUNT2757_1_conditional_mass",
            "M_q^2",
            "CONDITIONAL_FORMULA_FOUND",
            "2281 derives M_q^2=n_q^A H_AB n_q^B if q=0 is a parent-selected covariance equilibrium and H is positive on the transverse quotient.",
            "fills operator shape symbolically, not numerically",
        ),
        (
            "HUNT2757_2_conditional_stiffness",
            "Z_q",
            "CONDITIONAL_FORMULA_FOUND",
            "2281 derives Z_q=xi_q^2 n_q^A H_AB n_q^B from finite smoothing/correlation length.",
            "gives a finite-range denominator only if xi_q and the boundary/domain are sourced",
        ),
        (
            "HUNT2757_3_range_ratio",
            "lambda_q",
            "EXACT_CONDITIONAL_RATIO",
            "Combining 2308 lambda_q=sqrt(Z_q/M_q^2) with 2281 Z_q=xi_q^2 M_q^2 gives lambda_q=xi_q in the same normalization.",
            "range is not a free fit parameter on the activated covariance-Hessian branch",
        ),
        (
            "HUNT2757_4_selector_block",
            "parent q=0 selector",
            "SELECTOR_NOT_PARENT_SIGNED",
            "2282 proves q=0 is equivalent to radial observer-cell reciprocity but declares q-stiffness closure-only until the selector theorem is supplied.",
            "operator first fill remains closure/conditional, not local-GR derivation",
        ),
        (
            "HUNT2757_5_verdict",
            "claim-grade operator source",
            "CONDITIONAL_OPERATOR_FILL_IMPORTED_NOT_CLAIM_GRADE",
            "operator shape is stronger than blank placeholder, but q=0 selector, H_AB, xi_q, units, and boundary class are not source-backed.",
            "runner updates from missing operator to partial conditional operator; scoring remains blocked",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "hunt_id": row_id,
                "target": target,
                "result": result,
                "evidence": evidence,
                "route_effect": effect,
            }
        )
        for row_id, target, result, evidence, effect in specs
    ]


def first_fill_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "FF2757_0_Zq",
            "Z_q",
            "Z_q = xi_q^2 n_q^A H_AB n_q^B",
            "2281 QSD2281_3 gradient expansion",
            "normalization_dependent",
            "CONDITIONAL_FROM_2281_NOT_SOURCE_BACKED",
            "parent xi_q/smoothing kernel, q units, positive quotient Hessian, boundary/domain",
        ),
        (
            "FF2757_1_Mq2",
            "M_q^2",
            "M_q^2 = n_q^A H_AB n_q^B",
            "2281 QSD2281_2 transverse q mass",
            "normalization_dependent",
            "CONDITIONAL_FROM_2281_NOT_SOURCE_BACKED",
            "parent-selected q=0 equilibrium and actual H_AB around the local branch",
        ),
        (
            "FF2757_2_lambda",
            "lambda_q",
            "lambda_q = sqrt(Z_q/M_q^2) = xi_q when the 2281 branch is activated",
            "2308 range formula plus 2281 Hessian/stiffness ratio",
            "length_if_xi_q_is_parent_correlation_length",
            "EXACT_CONDITIONAL_RATIO_NOT_NUMERIC",
            "source-backed xi_q and same-normalization proof",
        ),
        (
            "FF2757_3_q_units",
            "q units/normalization",
            "q=C_R-C_T/(1-C_T) is dimensionless in the 2281/2282 covariance map unless parent rescaling is introduced",
            "2281/2282 covariance-observer map",
            "dimensionless_pending_parent_normalization",
            "CONDITIONAL_COORDINATE_NORMALIZATION",
            "single parent convention connecting q action, source vector, and observable projection",
        ),
        (
            "FF2757_4_domain_boundary",
            "boundary/domain",
            "local quotient domain with boundary term int_boundary Z_q q n^i nabla_i q = 0 or bounded",
            "2281 QOC2281_2 boundary and 2296 no-hair identity",
            "domain_dependent",
            "MISSING_BOUNDARY_CLASS",
            "no-flux/no-hair theorem for local cell/worldtube boundary",
        ),
        (
            "FF2757_5_Gq_norm",
            "G_q response norm",
            "||G_q|| <= 1/lambda_min(L_q); massive constant branch uses Yukawa kernel",
            "2281 residual bound ledger and 2313 bound-runner contract",
            "operator_norm_in_arena_units",
            "FORMAL_CONTRACT_NO_NUMERIC_BOUND",
            "lambda_min or xi_q, arena domain, source vector norm",
        ),
        (
            "FF2757_6_selector",
            "q=0 selector",
            "q=0 iff T^2S=1 iff R_AB=0",
            "2282 observer-cell equivalence",
            "dimensionless",
            "TARGET_IDENTIFIED_SELECTOR_NOT_DERIVED",
            "non-circular radial-cell current, constraint multiplier, gauge quotient, entropy, or source-consistency theorem",
        ),
    ]
    return [
        nonclaim(
            {
                "branch_id": BRANCH_ID,
                "fill_id": row_id,
                "input": input_name,
                "first_fill_value": value,
                "source_basis": basis,
                "units_status": units,
                "claim_status": status,
                "next_evidence_needed": needed,
            }
        )
        for row_id, input_name, value, basis, units, status, needed in specs
    ]


def green_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "GF2757_0_constant_massive_kernel",
            "constant-coefficient massive kernel",
            "for Z_q>0, M_q^2>0, L_q=-Z_q Delta+M_q^2 gives G_q(r)=exp(-r/lambda_q)/(4*pi*Z_q*r), lambda_q=sqrt(Z_q/M_q^2)",
            "only after Z_q, M_q^2, units, sign convention, and boundary/domain are source-backed",
            "FORMAL_KERNEL_CONDITIONAL",
        ),
        (
            "GF2757_1_covariance_range",
            "range under 2281 Hessian branch",
            "if M_q^2=n_q H n_q and Z_q=xi_q^2 n_q H n_q in the same normalization, then lambda_q=xi_q",
            "xi_q must be a parent smoothing/correlation length, not a fitted Yukawa range",
            "EXACT_CONDITIONAL_RATIO_NONCLAIM",
        ),
        (
            "GF2757_2_energy_norm",
            "coercive response norm",
            "||q|| <= ||L_q^{-1}|| ||source_q|| <= ||source_q||/lambda_min(L_q)",
            "lambda_min requires positive Hessian on the quotient, boundary class, and zero-mode removal",
            "CONDITIONAL_BOUND_FROM_2281",
        ),
        (
            "GF2757_3_algebraic_schur",
            "auxiliary Schur branch",
            "if Z_q=0, q=-(D_qWeyl2 C^2 + D_qWeylDual CstarC + J_q + boundary_tail)/M_q^2",
            "contact/higher-curvature terms must be theorem-zero or bounded; no Yukawa interpretation",
            "EXACT_CONDITIONAL_FORMULA_INPUTS_MISSING",
        ),
        (
            "GF2757_4_massless_guard",
            "massless guard",
            "M_q^2=0 requires source-free/no-hair and boundary-zero theorem, otherwise long-range residuals survive",
            "no local-GR claim from massless q unless J_q=0, boundary=0, and zero modes are removed",
            "GUARD_READY_PREMISES_UNSIGNED",
        ),
    ]
    return [nonclaim({"branch_id": BRANCH_ID, "green_id": row_id, "contract_item": item, "formula": formula, "acceptance_rule": rule, "current_status": status}) for row_id, item, formula, rule, status in specs]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "RUN2757_0_operator",
            "Z_q, M_q^2, lambda_q, q units",
            "MISSING_PARENT_HESSIAN",
            "PARTIAL_CONDITIONAL_FILL_NOT_SCORE_READY",
            "operator denominator can be written symbolically from covariance Hessian: M_q^2=nHn, Z_q=xi_q^2 nHn, lambda_q=xi_q",
        ),
        (
            "RUN2757_1_selector",
            "q=0 parent selector",
            "MISSING_PARENT_SELECTOR",
            "UNCHANGED_SELECTOR_BLOCK",
            "q=0 is identified with radial observer-cell reciprocity but not parent-selected",
        ),
        (
            "RUN2757_2_green_norm",
            "G_q response norm",
            "OPERATOR_DEPENDENT_SCHEMA",
            "FORMAL_GREEN_CONTRACT_READY_NO_NUMERIC_NORM",
            "massive/Yukawa, algebraic/Schur, and massless guards are split",
        ),
        (
            "RUN2757_3_curvature_source",
            "D_qWeyl2 and D_qWeylDual",
            "MISSING_PARENT_COEFFICIENT",
            "UNCHANGED_MISSING_PARENT_COEFFICIENT",
            "Schwarzschild Weyl2 kernel stays a background shape only",
        ),
        (
            "RUN2757_4_source_vector",
            "J_q, body/boundary/tails",
            "MISSING_SOURCE_ZERO_OR_BOUND",
            "UNCHANGED_MISSING_SOURCE_ZERO_OR_BOUND",
            "no exterior-vacuum shortcut; source channels still need zero theorem or absolute bound",
        ),
        (
            "RUN2757_5_projection",
            "P_arena[q]",
            "MISSING_ARENA_PROJECTION",
            "UNCHANGED_MISSING_ARENA_PROJECTION",
            "no R10/PPN/clock/orbital score",
        ),
        (
            "RUN2757_6_score_gate",
            "score permission",
            "CLAIM_AND_SCORE_BLOCKED",
            "CLAIM_AND_SCORE_BLOCKED",
            "partial conditional operator fill reduces fog but does not permit a pass/fail claim",
        ),
    ]
    return [nonclaim({"branch_id": BRANCH_ID, "runner_id": row_id, "runner_input": target, "previous_status": previous, "updated_status": updated, "effect": effect}) for row_id, target, previous, updated, effect in specs]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2757_0_operator",
            "conditional q operator fill imported",
            "CONDITIONAL_OPERATOR_SHAPE_READY_NOT_CLAIM_GRADE",
            "2281 supplies M_q^2=nHn and Z_q=xi_q^2 nHn if q=0 is parent-selected and the Hessian is positive",
        ),
        (
            "DEC2757_1_range",
            "range rule",
            "LAMBDAQ_EQUALS_XIQ_CONDITIONALLY",
            "lambda_q is not a free Yukawa fit parameter on the covariance-Hessian branch",
        ),
        (
            "DEC2757_2_selector",
            "selector block",
            "Q_ZERO_SELECTOR_STILL_MISSING",
            "2282 identifies q=0 with radial observer-cell reciprocity but does not parent-select it",
        ),
        (
            "DEC2757_3_score",
            "runner status",
            "PARTIAL_OPERATOR_FILL_SCORE_BLOCKED",
            "D coefficients, source vector, boundary/domain, and arena projection remain missing",
        ),
        (
            "DEC2757_4_next",
            "next target",
            "NEXT_2758_Q_ZERO_SELECTOR_SOURCE_CURRENT_OR_GREEN_DOMAIN_SECOND_FILL",
            "try the q=0 selector/source-current route; if not, fill Green-domain/source-bound rows before any score",
        ),
    ]
    return [nonclaim({"branch_id": BRANCH_ID, "decision_id": row_id, "decision": decision, "result": result, "reason": reason}) for row_id, decision, result, reason in specs]


def gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("GATE2757_0_sources", "all source paths/needles valid", "PASS_NONCLAIM", "audit is reproducible"),
        ("GATE2757_1_conditional_operator", "2281 conditional q operator imported", "PASS_NONCLAIM", "operator shape first-fill exists"),
        ("GATE2757_2_selector", "parent q=0 selector sourced", "BLOCKED_NO_CLAIM", "radial-cell current/constraint/gauge owner missing"),
        ("GATE2757_3_numeric_operator", "Z_q, M_q^2, xi_q numeric/source-backed", "BLOCKED_NO_CLAIM", "no numeric Green response"),
        ("GATE2757_4_boundary_domain", "boundary/domain/no-hair signed", "BLOCKED_NO_CLAIM", "no local plateau/no-hair claim"),
        ("GATE2757_5_source_projection", "source vector and arena projection source-backed", "BLOCKED_NO_CLAIM", "no R10/PPN/clock/orbital score"),
        ("GATE2757_6_local_GR", "derived local GR/Newton", "BLOCKED_NO_CLAIM", "selector and Newton source normalization remain open"),
    ]
    return [nonclaim({"claim_gate_id": row_id, "claim_gate": gate, "status": status, "reason": reason}) for row_id, gate, status, reason in specs]


def refusal_rows() -> list[dict[str, Any]]:
    specs = [
        ("REF2757_0_operator_claim", "q operator is parent-derived claim-grade", "BLOCKED", "2281 formula is conditional and 2282 declares selector missing"),
        ("REF2757_1_lambda_claim", "lambda_q=xi_q is a numeric prediction", "BLOCKED", "ratio is exact conditionally but xi_q is not sourced numerically"),
        ("REF2757_2_score_runner", "run/pass local empirical q residual tests now", "BLOCKED", "D_qWeyl2, source vector, boundary/domain, and arena projection remain missing"),
        ("REF2757_3_local_gr", "MTS derives local GR/Newton from this checkpoint", "BLOCKED", "q=0 equivalence is not a parent selector and Newton source normalization remains open"),
        ("REF2757_4_public", "publish as local-GR proof", "BLOCKED", "private operator first-fill only; no public claim allowed"),
    ]
    return [nonclaim({"branch_id": BRANCH_ID, "refusal_id": row_id, "attempted_claim": claim, "status": status, "reason": reason, "runner_allows_claim": False}) for row_id, claim, status, reason in specs]


def next_rows() -> list[dict[str, Any]]:
    return [
        nonclaim(
            {
                "next_id": "NEXT2757_0_2758",
                "status": "selected_primary",
                "target_doc": "2758-Y5-R2FR-q-zero-selector-source-current-or-Green-domain-second-fill-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_q_zero_selector_source_current_or_Green_domain_second_fill_under_AX1090_2758.py",
                "mission": "attempt the non-circular q=0 selector through radial-cell current, constraint multiplier, gauge quotient, entropy, or source consistency; if not source-signed, fill Green-domain/boundary/source second-fill rows for the independent-q runner",
                "acceptance": "either parent-signed q=0 selector/current or a nonclaim second-fill ledger for boundary/domain, xi_q, Green norm, and source envelopes; no scoring without all claim gates",
                "forbidden": "do not use EH/GR vacuum as parent proof, do not claim local GR/Newton, do not score DqWeyl2, do not edit formalization-workbench, no GitHub action",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"copy_id": "BR2757_0_first_fill_queue", "source_table": rel(OUTPUTS["first_fill"]), "copy_path": rel(BRANCH_OUTPUTS["first_fill_queue"]), "purpose": "RAB queue for q operator first-fill", "exists": BRANCH_OUTPUTS["first_fill_queue"].exists()}),
        nonclaim({"copy_id": "BR2757_1_green_beta", "source_table": rel(OUTPUTS["green"]), "copy_path": rel(BRANCH_OUTPUTS["green_beta"]), "purpose": "Green function normalization contract", "exists": BRANCH_OUTPUTS["green_beta"].exists()}),
        nonclaim({"copy_id": "BR2757_2_runner_local", "source_table": rel(OUTPUTS["runner"]), "copy_path": rel(BRANCH_OUTPUTS["runner_local"]), "purpose": "local-bound q runner update", "exists": BRANCH_OUTPUTS["runner_local"].exists()}),
        nonclaim({"copy_id": "BR2757_3_next_queue", "source_table": rel(OUTPUTS["next"]), "copy_path": rel(BRANCH_OUTPUTS["next_queue"]), "purpose": "RAB queue for q-zero selector or Green-domain second fill", "exists": BRANCH_OUTPUTS["next_queue"].exists()}),
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
    hunt: list[dict[str, Any]],
    first_fill: list[dict[str, Any]],
    green: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["exists"] is True and row["needles_present"] is True for row in sources)
    formula_ok = any(row["hunt_id"] == "HUNT2757_5_verdict" and row["result"] == "CONDITIONAL_OPERATOR_FILL_IMPORTED_NOT_CLAIM_GRADE" for row in hunt)
    fill_ok = {"Z_q", "M_q^2", "lambda_q", "q units/normalization", "boundary/domain", "G_q response norm", "q=0 selector"}.issubset({row["input"] for row in first_fill})
    lambda_ok = any(row["fill_id"] == "FF2757_2_lambda" and "xi_q" in row["first_fill_value"] for row in first_fill)
    green_ok = any(row["green_id"] == "GF2757_1_covariance_range" and "lambda_q=xi_q" in row["formula"] for row in green)
    runner_ok = any(row["runner_id"] == "RUN2757_0_operator" and row["updated_status"] == "PARTIAL_CONDITIONAL_FILL_NOT_SCORE_READY" for row in runner) and any(row["runner_id"] == "RUN2757_6_score_gate" and row["updated_status"] == "CLAIM_AND_SCORE_BLOCKED" for row in runner)
    decision_ok = any(row["decision_id"] == "DEC2757_4_next" and row["result"] == "NEXT_2758_Q_ZERO_SELECTOR_SOURCE_CURRENT_OR_GREEN_DOMAIN_SECOND_FILL" for row in decisions)
    gates_ok = any(row["claim_gate_id"] == "GATE2757_6_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates)
    refusal_ok = all(row["runner_allows_claim"] is False for row in refusal)
    next_ok = next_target[0]["selected"] is True and "2758" in next_target[0]["target_doc"]
    no_claim_flags_ok = all(
        row.get("valid_for_claim") is False and row.get("claim_allowed") is False
        for block in [hunt, first_fill, green, runner, decisions, gates, refusal, next_target]
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
        {"validation_id": "VAL2757_0_sources", "passed": source_ok, "detail": "all source paths exist and needles are present", "timestamp_utc": ts()},
        {"validation_id": "VAL2757_1_conditional_formula", "passed": formula_ok, "detail": "conditional q operator fill imported but not claim-grade", "timestamp_utc": ts()},
        {"validation_id": "VAL2757_2_first_fill", "passed": fill_ok, "detail": "first-fill rows include Zq, Mq2, lambda, units, domain, Gq norm, selector", "timestamp_utc": ts()},
        {"validation_id": "VAL2757_3_lambda_ratio", "passed": lambda_ok and green_ok, "detail": "lambda_q=xi_q ratio recorded conditionally", "timestamp_utc": ts()},
        {"validation_id": "VAL2757_4_runner_update", "passed": runner_ok, "detail": "runner updates operator from missing to partial conditional fill while score remains blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2757_5_next", "passed": decision_ok and next_ok, "detail": "2758 q-zero selector or Green-domain second-fill selected", "timestamp_utc": ts()},
        {"validation_id": "VAL2757_6_claim_gates", "passed": gates_ok and no_claim_flags_ok, "detail": "local GR/Newton and all generated claim flags remain blocked", "timestamp_utc": ts()},
        {"validation_id": "VAL2757_7_refusal_runner", "passed": refusal_ok, "detail": "refusal runner blocks operator/lambda/scoring/local-GR claims", "timestamp_utc": ts()},
        {"validation_id": "VAL2757_8_branch_outputs", "passed": branch_ok, "detail": "branch copies exist", "timestamp_utc": ts()},
        {"validation_id": "VAL2757_9_csv_parse", "passed": csv_ok, "detail": "; ".join(csv_bits), "timestamp_utc": ts()},
        {"validation_id": "VAL2757_10_pycache_absent", "passed": pycache_ok, "detail": f"scripts __pycache__ absent={pycache_ok}", "timestamp_utc": ts()},
        {"validation_id": "VAL2757_11_formalization_untouched", "passed": formalization_ok, "detail": f"formalization-workbench recent modified-file count since script start = {formalization_count}", "timestamp_utc": ts()},
    ]
    rows.append(
        {
            "validation_id": "VAL2757_OVERALL",
            "passed": all(row["passed"] is True for row in rows),
            "detail": "2757 imports the 2281 conditional q Hessian as the first operator fill, derives lambda_q=xi_q under the same-normalization branch, keeps the 2282 q=0 selector block active, blocks scoring/local-GR claims, and selects q-zero selector or Green-domain second-fill next.",
            "timestamp_utc": ts(),
        }
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        f"""# 2757 - Y5 R2/f(R): Independent q Hessian Operator Source Or Bound-Runner First Fill Under AX1090

Status: `Y5_R2FR_2757_partial_conditional_q_operator_fill_no_claim`

## Private Verdict

2757 finds a real nontrivial tightening.

The independent-q route is no longer a blank operator placeholder. On the covariance-Hessian branch, if the parent theory selects the local covariance equilibrium `q=0` and the transverse Hessian is positive, then:

`M_q^2 = n_q^A H_AB n_q^B`

`Z_q = xi_q^2 n_q^A H_AB n_q^B`

so

`lambda_q = sqrt(Z_q/M_q^2) = xi_q`

That is useful because the q range is not arbitrary on this branch. But it is still not claim-grade: `q=0` is identified with radial observer-cell reciprocity, not parent-selected; `H_AB`, `xi_q`, units, boundary/domain, source vector, and observable projections are not sourced.

## Source Register

{markdown_table(data["sources"], ["source_id", "description", "source_path", "exists", "needles_present", "missing_needles", "valid_for_claim"])}

## q Operator Source Hunt

{markdown_table(data["hunt"], ["hunt_id", "target", "result", "evidence", "route_effect", "valid_for_claim"])}

## q Operator First-Fill Rows

{markdown_table(data["first_fill"], ["fill_id", "input", "first_fill_value", "source_basis", "units_status", "claim_status", "next_evidence_needed", "valid_for_claim"])}

## Green Function Normalization Contract

{markdown_table(data["green"], ["green_id", "contract_item", "formula", "acceptance_rule", "current_status", "valid_for_claim"])}

## Bound Runner Update

{markdown_table(data["runner"], ["runner_id", "runner_input", "previous_status", "updated_status", "effect", "valid_for_claim"])}

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

This is a good kind of progress. We have not derived local GR, but we have turned one foggy missing operator into a conditional formula with a sharp selector debt. The next test is whether the theory can non-circularly select `q=0` / radial observer-cell reciprocity. If not, we fill Green-domain and source-bound rows before any empirical score.
""",
        encoding="utf-8",
    )


def main() -> None:
    ensure_dirs()
    sources = source_rows()
    hunt = hunt_rows()
    first_fill = first_fill_rows()
    green = green_rows()
    runner = runner_rows()
    decisions = decision_rows()
    gates = gate_rows()
    refusal = refusal_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["hunt"], hunt)
    write_csv(OUTPUTS["first_fill"], first_fill)
    write_csv(OUTPUTS["green"], green)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["next"], next_target)

    write_csv(BRANCH_OUTPUTS["first_fill_queue"], first_fill)
    write_csv(BRANCH_OUTPUTS["green_beta"], green)
    write_csv(BRANCH_OUTPUTS["runner_local"], runner)
    write_csv(BRANCH_OUTPUTS["next_queue"], next_target)
    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)

    remove_pycache()
    validation = validation_rows(sources, hunt, first_fill, green, runner, decisions, gates, refusal, next_target)
    write_csv(OUTPUTS["validation"], validation)

    data = {
        "sources": sources,
        "hunt": hunt,
        "first_fill": first_fill,
        "green": green,
        "runner": runner,
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
        raise SystemExit(f"2757 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
