from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3286-Y5-R2FR-Hodge-Poynting-factor-owner-or-first-CH-CS-slope-row-under-AX1090.md"

SRC_3285_DOC = ROOT / "3285-Y5-R2FR-public-readout-functor-zero-proof-or-first-CR-factor-slope-under-AX1090.md"
SRC_3285_NEXT = OUT / "P8_Y5_R2FR_3285_NEXT_TARGET.csv"
SRC_3285_SIG = OUT / "P8_Y5_R2FR_3285_FACTOR_THROUGH_Q_SIGNATURE_MATRIX.csv"
SRC_3285_POYNTING = OUT / "P8_Y5_R2FR_3285_POYNTING_QBASIC_LEMMA.csv"
SRC_3285_FINITE = OUT / "P8_Y5_R2FR_3285_FIRST_CR_FACTOR_SLOPE_ROWS_NONCLAIM.csv"
SRC_3285_VALIDATION = OUT / "P8_Y5_BRR545_3285_VALIDATION.csv"
SRC_3274_POYNTING = OUT / "P8_Y5_R2FR_3274_EM_STRESS_POYNTING_EXCHANGE_LAW.csv"
SRC_3105_DOC = ROOT / "3105-Y5-R2FR-EM-wave-Poynting-public-geometry-route-under-AX1090.md"
SRC_3106_DOC = ROOT / "3106-Y5-R2FR-constitutive-Hodge-star-derivation-or-EM-medium-residual-under-AX1090.md"
SRC_1100_DOC = ROOT / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"
SRC_1056_DOC = ROOT / "1056-Y5-R10-alpha-owner-from-vertical-generator-norm-or-topological-level.md"
SRC_3273_ALPHA = OUT / "P8_Y5_R2FR_3273_ALPHA_COEFFICIENT_DECOMPOSITION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3286_SOURCE_REGISTER.csv",
    "owner": OUT / "P8_Y5_R2FR_3286_HODGE_POYNTING_OWNER_THEOREM.csv",
    "audit": OUT / "P8_Y5_R2FR_3286_CHI_TO_HODGE_PREMISE_AUDIT.csv",
    "branches": OUT / "P8_Y5_R2FR_3286_POYNTING_BRANCH_DECISION_TABLE.csv",
    "formula": OUT / "P8_Y5_R2FR_3286_CH_CS_SLOPE_FORMULA_ROWS.csv",
    "finite": OUT / "P8_Y5_R2FR_3286_FIRST_CH_CS_SLOPE_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3286_CH_CS_BOUND_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3286_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3286_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3286_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3286_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
DEFAULT_BOUND = 1.389797711495e-12


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def fmt(value: float) -> str:
    return f"{value:.12e}"


def compact(value: Any, limit: int = 420) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
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
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def evidence_hits(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered = [needle.lower() for needle in needles]
    hits: list[str] = []
    for idx, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered):
            hits.append(f"L{idx}:{compact(line, 260)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    snapshot: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            stat = item.stat()
            snapshot[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return snapshot


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def bound_from_3285() -> float:
    if not SRC_3285_FINITE.exists():
        return DEFAULT_BOUND
    for row in read_csv(SRC_3285_FINITE):
        if row.get("row_id") == "CRF3285_1_selected_hodge_poynting_slope":
            try:
                return float(row["C_R_abs_bound"])
            except (KeyError, ValueError):
                return DEFAULT_BOUND
    return DEFAULT_BOUND


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3285_DOC, "3285 handoff to Hodge/Poynting first factor", ["first finite factor target", "Hodge/impedance plus Poynting"]),
        (SRC_3285_NEXT, "3285 next-target contract", ["Hodge/impedance", "C_H/C_S"]),
        (SRC_3285_SIG, "Hodge/Poynting factor-through-q blockers", ["SIG3285_impedance", "SIG3285_standard"]),
        (SRC_3285_POYNTING, "Poynting q-basic lemma", ["L_v S_EM", "no_double_count"]),
        (SRC_3285_FINITE, "selected finite C_H/C_S row", ["n_H*C_H + n_S*C_S"]),
        (SRC_3285_VALIDATION, "3285 validation", ["VAL3285_11_overall", "true"]),
        (SRC_3274_POYNTING, "EM stress/Poynting exchange law", ["S_EM", "Q_Z", "q_loc"]),
        (SRC_3105_DOC, "public-vs-background Poynting fork", ["Double-Counting Guard", "Branch B"]),
        (SRC_3106_DOC, "constitutive Hodge-star premise list", ["CHS3106_0", "Delta_chi"]),
        (SRC_1100_DOC, "charge/current/readout owner guard", ["readout", "T_Q"]),
        (SRC_1056_DOC, "alpha readout/Hodge descent guard", ["Hodge", "readout"]),
        (SRC_3273_ALPHA, "alpha coefficient decomposition", ["C_R", "C_Z"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3286_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def owner_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "HP3286_0_premetric_owner",
            "claim_piece": "one constitutive owner for Hodge and Poynting",
            "statement": "Start with dF=0, dH=J, and H^{mu nu}=1/2 chi^{mu nu alpha beta}F_{alpha beta}; Hodge/impedance and Poynting are downstream of chi plus the public observer coframe.",
            "derivation_status": "DEFINITION_AND_BRANCH_COMPRESSION",
            "payoff": "C_H and C_S are not independent leaks once chi is owned.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "HP3286_1_metric_Hodge_branch",
            "claim_piece": "metric Hodge specialization",
            "statement": "If chi^{mu nu alpha beta}=Z_Q sqrt(-g_pub)(g_pub^{mu alpha}g_pub^{nu beta}-g_pub^{mu beta}g_pub^{nu alpha}), then H=Z_Q *_{g_pub}F.",
            "derivation_status": "STANDARD_CONDITIONAL_REDUCTION",
            "payoff": "finite Hodge drift is reduced to Z_Q, g_pub, and any nonmetric Delta_chi.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "HP3286_2_vertical_zero",
            "claim_piece": "Hodge and Poynting zero law",
            "statement": "If chi=q^*bar_chi, F=q^*bar_F, u=q^*bar_u, h=q^*bar_h, and v in ker(Dq), then L_v chi=L_v F=L_v u=L_v h=0, hence L_v H=0, L_v T_EM^{mu nu}=0, and L_v S_EM^a=0.",
            "derivation_status": "EXACT_CHAIN_RULE_AND_LEIBNIZ_THEOREM",
            "payoff": "C_H=0 and C_S=0 inside the public Maxwell/Hodge branch.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "HP3286_3_Hodge_derivative_identity",
            "claim_piece": "explicit derivative identity",
            "statement": "For H=Z_Q *_{g_pub}F, L_v H=(L_v Z_Q)*F+Z_Q(L_v *_{g_pub})F+Z_Q *_{g_pub}(L_v F); q-basic Z_Q, g_pub, and F force L_v H=0.",
            "derivation_status": "EXACT_LOCAL_VARIATION_IDENTITY",
            "payoff": "the missing coupling is now the parent ownership of Z_Q/g_pub/F or Delta_chi, not an unspecified EM intuition.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "HP3286_4_finite_escape",
            "claim_piece": "only honest finite Hodge/Poynting escape",
            "statement": "If chi=chi_metric(g_pub,Z_Q)+Delta_chi and L_v Delta_chi is not zero, then C_H and C_S must be computed as projections of L_v Delta_chi and any nonpublic coframe drift.",
            "derivation_status": "FINITE_RESIDUAL_ROUTE_DERIVED",
            "payoff": "the next numeric target is a sourced Delta_chi slope/projection row.",
            "valid_for_claim": "false",
        },
    ]


def premise_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("CHS3106_0_local_linear", "chi is local, linear, and fixed before readout", "needed for H=chi F without post-fit medium response", "not parent-derived here"),
        ("CHS3106_1_reciprocal", "chi has reciprocal/action symmetry", "needed for EM action and Hilbert stress", "not parent-derived here"),
        ("CHS3106_2_no_skewon", "skewon/dissipative part vanishes", "needed to avoid non-Hilbert EM stress and preferred-frame leakage", "not parent-derived here"),
        ("CHS3106_3_nonbirefringent", "Fresnel quartic is a double light cone", "needed to reconstruct one conformal public metric", "not parent-derived here"),
        ("CHS3106_4_positive_energy", "EM energy density and Poynting flux have physical sign", "needed to fix time orientation/source sign", "not parent-derived here"),
        ("CHS3106_5_impedance_owner", "Z_Q is quotient-owned or fixed representation data", "needed to stop alpha/impedance drift", "blocked by prior EM-owner work"),
        ("CHS3106_6_same_public_metric", "EM Hodge metric equals matter/clock/source metric", "needed to avoid optical-metric split", "needs public geometry rule"),
        ("CHS3106_7_radiative_readout", "radiative/readout reductions do not regenerate f(Xhat)F^2", "needed to protect tree-level q-basic route", "unsigned in prior alpha-owner work"),
    ]
    return [
        {
            "premise_id": premise_id,
            "premise": premise,
            "why_needed": why_needed,
            "current_status": "UNSIGNED",
            "source_status": source_status,
            "blocks_zero_claim": "true",
            "valid_for_claim": "false",
        }
        for premise_id, premise, why_needed, source_status in rows
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "HPB3286_0_public_metric_Hodge",
            "route": "public Maxwell/Hodge stress",
            "condition": "chi=chi_metric(g_pub,Z_Q), Z_Q/g_pub/F/u/h all q-basic",
            "consequence": "L_v H=0 and L_v S_EM^a=0, so C_H=C_S=0",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "double_counting": "safe: Poynting belongs only to T_EM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "HPB3286_1_finite_constitutive_medium",
            "route": "Delta_chi medium residual",
            "condition": "chi has hidden/domain dependence not forced through q",
            "consequence": "C_H/C_S are projections of L_v Delta_chi and must be sourced or bounded",
            "status": "LIVE_FINITE_ROUTE",
            "double_counting": "safe only if counted as EM constitutive residual, not also hidden E_res flux",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "HPB3286_2_independent_background_flux",
            "route": "separate MTS background energy flux",
            "condition": "background carries energy not equal to public EM Poynting flux",
            "consequence": "route belongs to E_res_munu/stress conservation, not to the public C_H/C_S readout factor",
            "status": "SEPARATE_BRANCH",
            "double_counting": "safe only if named separately and never duplicated as T_EM flux",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "HPB3286_3_forbidden_double_count",
            "route": "same Poynting flux used twice",
            "condition": "EM flux is both public T_EM and hidden background source",
            "consequence": "source equation is overcounted",
            "status": "FORBIDDEN",
            "double_counting": "forbidden by 3105/3285 guard",
            "valid_for_claim": "false",
        },
    ]


def formula_rows(bound: float) -> list[dict[str, Any]]:
    return [
        {
            "formula_id": "HPC3286_0_metric_decomposition",
            "object": "constitutive split",
            "formula": "chi = chi_metric(g_pub,Z_Q) + Delta_chi",
            "meaning": "all finite nonpublic Hodge/Poynting drift is assigned to Delta_chi after the public metric/Z_Q branch is separated.",
            "required_inputs": "parent chi, public metric g_pub, Z_Q normalization, sign convention",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "HPC3286_1_CH_projection",
            "object": "Hodge/impedance slope",
            "formula": "C_H = Pi_H[L_v Delta_chi + L_v chi_metric]/N_H; public branch sets L_v chi_metric=0 and leaves C_H=Pi_H[L_v Delta_chi]/N_H",
            "meaning": "C_H is not free; it is the readout projection of the vertical constitutive residual.",
            "required_inputs": "projection Pi_H, normalisation N_H, sourced L_v Delta_chi",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "HPC3286_2_CS_projection",
            "object": "Poynting flux slope",
            "formula": "C_S = Pi_S[L_v Delta_chi, L_v u, L_v h]/N_S; public branch sets L_v Delta_chi=L_v u=L_v h=0",
            "meaning": "Poynting drift is downstream of the constitutive residual and observer coframe residual.",
            "required_inputs": "projection Pi_S, N_S, observer/coframe ownership, sourced L_v Delta_chi",
            "valid_for_claim": "false",
        },
        {
            "formula_id": "HPC3286_3_alpha_factor_bound",
            "object": "first Hodge/Poynting alpha readout factor",
            "formula": "C_R^(HP)=n_H C_H+n_S C_S with |C_R^(HP)| <= " + fmt(bound),
            "meaning": "under C_J=C_Z=other C_R factors=0, this is the finite envelope for the selected factor.",
            "required_inputs": "n_H,n_S,C_H,C_S and all no-double-counting/source certificates",
            "valid_for_claim": "false",
        },
    ]


def finite_rows(bound: float) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "HPR3286_0_public_Hodge_Poynting_zero_conditional",
            "factor_target": "Hodge/impedance plus Poynting flux",
            "C_R_HP_prediction": "0",
            "C_R_HP_abs_bound": fmt(bound),
            "source_status": "THEOREM_CONDITIONAL",
            "result": "PASS_NUMERIC_NONCLAIM_IF_ALL_CHS_PREMISES_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "HPR3286_1_Delta_chi_finite_slope",
            "factor_target": "finite constitutive medium residual",
            "C_R_HP_prediction": "n_H*Pi_H[L_v Delta_chi]/N_H + n_S*Pi_S[L_v Delta_chi,L_vu,L_vh]/N_S",
            "C_R_HP_abs_bound": fmt(bound),
            "source_status": "MISSING_NUMERIC_DELTA_CHI_PROJECTION",
            "result": "REFUSE_MISSING_SOURCE_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "HPR3286_2_missing_parent_chi_source",
            "factor_target": "parent-owned chi to metric-Hodge theorem",
            "C_R_HP_prediction": "MISSING_PARENT_CHI_SIGNATURE",
            "C_R_HP_abs_bound": fmt(bound),
            "source_status": "CHS3106_0_TO_7_UNSIGNED",
            "result": "REFUSE_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "HPR3286_3_half_bound_smoke",
            "factor_target": "numeric runner smoke inside envelope",
            "C_R_HP_prediction": fmt(0.5 * bound),
            "C_R_HP_abs_bound": fmt(bound),
            "source_status": "SMOKE_ONLY",
            "result": "SMOKE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "HPR3286_4_twice_bound_smoke",
            "factor_target": "numeric runner smoke outside envelope",
            "C_R_HP_prediction": fmt(2.0 * bound),
            "C_R_HP_abs_bound": fmt(bound),
            "source_status": "SMOKE_ONLY",
            "result": "SMOKE",
            "valid_for_claim": "false",
        },
    ]


def is_number(text: str) -> bool:
    try:
        value = float(text)
    except ValueError:
        return False
    return math.isfinite(value)


def runner_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    expected = {
        "HPR3286_0_public_Hodge_Poynting_zero_conditional": "PASS_NUMERIC_NONCLAIM",
        "HPR3286_1_Delta_chi_finite_slope": "REFUSE_MISSING_SOURCE_NONCLAIM",
        "HPR3286_2_missing_parent_chi_source": "REFUSE_MISSING_SOURCE_NONCLAIM",
        "HPR3286_3_half_bound_smoke": "PASS_NUMERIC_NONCLAIM",
        "HPR3286_4_twice_bound_smoke": "FAIL_BOUND",
    }
    for row in rows:
        prediction = str(row["C_R_HP_prediction"])
        bound = float(row["C_R_HP_abs_bound"])
        if row["source_status"].startswith("MISSING") or "UNSIGNED" in row["source_status"]:
            result = "REFUSE_MISSING_SOURCE_NONCLAIM"
            ratio = "N/A"
        elif is_number(prediction):
            value = abs(float(prediction))
            ratio = fmt(value / bound)
            result = "PASS_NUMERIC_NONCLAIM" if value <= bound else "FAIL_BOUND"
        else:
            result = "SYMBOLIC_NONNUMERIC_NONCLAIM"
            ratio = "N/A"
        output.append(
            {
                "row_id": row["row_id"],
                "C_R_HP_prediction": prediction,
                "prediction_over_bound": ratio,
                "result": result,
                "expected_result": expected[row["row_id"]],
                "expectation_met": bool_str(result == expected[row["row_id"]]),
                "valid_for_claim": "false",
            }
        )
    return output


def promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3286_0_owner_compression",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "Hodge and Poynting slopes collapse to one constitutive owner object chi plus public observer coframe.",
        },
        {
            "gate_id": "GATE3286_1_zero_law",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "If chi/F/u/h are q-basic, L_v H=0 and L_v S_EM^a=0 by chain rule/Leibniz.",
        },
        {
            "gate_id": "GATE3286_2_CHS_premises_signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "CHS3106_0..7 remain unsigned in the current corpus.",
        },
        {
            "gate_id": "GATE3286_3_numeric_Delta_chi_sourced",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "No numeric/source-backed Pi_H or Pi_S projection row for L_v Delta_chi exists.",
        },
        {
            "gate_id": "GATE3286_4_no_double_count",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "Public EM Poynting flux and independent background flux are separated; duplicate source use is forbidden.",
        },
        {
            "gate_id": "GATE3286_5_no_local_claim",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "No Maxwell/local-GR/alpha/PPN/clock claim is allowed from this checkpoint.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3286_0_progress",
            "decision": "C_H and C_S are reduced to a single chi/Delta_chi ownership problem.",
            "why_it_moves_forward": "we are no longer chasing two loose couplings; the finite branch has one sourceable vertical constitutive residual.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3286_1_zero_route",
            "decision": "The public Maxwell/Hodge branch gives an exact conditional zero law.",
            "why_it_moves_forward": "a future parent action only has to sign chi/F/u/h through q, not invent separate Poynting cancellation.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3286_2_failure_route",
            "decision": "If chi cannot be parent-signed as metric Hodge, the branch becomes a finite Delta_chi slope test.",
            "why_it_moves_forward": "the fallback is empirical/sourceable instead of closure-only hand waving.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3286_3_next_work",
            "decision": "Attack CHS3106_0..7 directly or source the first Delta_chi projection row.",
            "why_it_moves_forward": "this is the least-scattered next target and directly addresses the missing coupling.",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3286_0_3287",
            "target_doc": "3287-Y5-R2FR-chi-to-metric-Hodge-premise-proof-or-DeltaChi-slope-source-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3287_chi_to_metric_Hodge_premise_proof_or_DeltaChi_slope_source_row.py",
            "objective": "Prove or reject the chi-to-metric-Hodge premise stack: local linear, reciprocal, no-skewon, nonbirefringent, positive, same-public-metric, q-basic impedance, and radiative/readout protection; if not parent-signed, source the first finite Delta_chi projection row.",
            "guardrail": "Do not score C_H/C_S as evidence, do not claim EM/local-GR, do not double-count Poynting, and do not reopen all readout factors.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    fw_before: dict[str, tuple[int, int]],
    sources: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    formula: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    non_validation_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(fw_before, snapshot_tree(FW))
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append(
            {
                "check_id": check_id,
                "check": check,
                "passed": bool_str(passed),
                "detail": compact(detail, 600),
            }
        )

    add("VAL3286_0_sources_exist", "all cited source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3286_1_sources_parse", "all cited source paths parse", all(row["parse_ok"] == "true" for row in sources))
    add(
        "VAL3286_2_outputs_parse",
        "all 3286 non-validation output CSVs parse",
        all(csv_parse_ok(path) for path in non_validation_outputs),
        "non-validation outputs parsed before validation write",
    )
    add(
        "VAL3286_3_zero_law_present",
        "owner theorem includes L_v H and L_v S_EM zero law",
        any("L_v H=0" in row["statement"] and "L_v S_EM" in row["statement"] for row in owner),
    )
    add(
        "VAL3286_4_premise_stack_covered",
        "CHS3106_0..7 premise stack is represented and unsigned",
        len(audit) == 8 and all(row["current_status"] == "UNSIGNED" for row in audit),
    )
    add(
        "VAL3286_5_Delta_chi_formula_present",
        "finite fallback is explicitly Delta_chi based",
        any("Delta_chi" in row["formula"] and "C_H" in row["formula"] for row in formula)
        and any("Delta_chi" in row["formula"] and "C_S" in row["formula"] for row in formula),
    )
    add(
        "VAL3286_6_no_double_count_guard",
        "Poynting double-count branch is forbidden",
        any(row["branch_id"] == "HPB3286_3_forbidden_double_count" and row["status"] == "FORBIDDEN" for row in branches),
    )
    add(
        "VAL3286_7_runner_expectations",
        "C_H/C_S runner expectations all match",
        all(row["expectation_met"] == "true" for row in runner),
        ";".join(f"{row['row_id']}={row['result']}" for row in runner),
    )
    add(
        "VAL3286_8_claim_gates_false",
        "no 3286 gate allows local-GR/alpha/Maxwell claim",
        all(row["claim_allowed"] == "false" for row in promotion),
    )
    add(
        "VAL3286_9_next_target_focused",
        "next target focuses chi-to-Hodge proof or Delta_chi source row",
        any("3287" in row["target_doc"] and "Delta_chi" in row["objective"] for row in next_target),
    )
    add(
        "VAL3286_10_formalization_untouched",
        "formalization-workbench modified-file count remains zero by this script",
        fw_changed == 0,
        f"formalization_changed_count={fw_changed}",
    )
    overall = all(row["passed"] == "true" for row in checks)
    add(
        "VAL3286_11_overall",
        "3286 validation overall",
        overall,
        "all required checks passed" if overall else "one or more checks failed",
    )
    return checks


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(col, "")) for col in columns) + " |")
    return "\n".join(lines)


def write_doc(
    bound: float,
    owner: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    formula: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 3286 - Hodge/Poynting factor owner or first C_H/C_S slope row under AX1090

## Summary

3286 gets past the loose-coupling stage: the Hodge/impedance slope `C_H` and the Poynting-flux slope `C_S` are not treated as independent mystery knobs. They collapse to one owner problem:

`H^{{mu nu}} = 1/2 chi^{{mu nu alpha beta}} F_{{alpha beta}}`

with the metric-Hodge branch

`chi = chi_metric(g_pub,Z_Q) = Z_Q sqrt(-g_pub)(g_pub g_pub - g_pub g_pub)`.

If `chi`, `F`, the observer velocity `u`, and the spatial projector/coframe `h` are all pulled back from the public quotient, then `v in ker(Dq)` gives

`L_v H = 0`, `L_v T_EM^{{mu nu}} = 0`, and `L_v S_EM^a = 0`.

So the clean branch gives `C_H=0` and `C_S=0` without a hand-tuned plateau.

The current corpus still does **not** sign the full `chi -> metric Hodge` premise stack from `3106`, so this is not a Maxwell/local-GR claim. But the fallback is now sharper: define

`Delta_chi = chi - chi_metric(g_pub,Z_Q)`

and source or bound `L_v Delta_chi`. Under the pure readout envelope, the selected factor must satisfy

`|C_R^(HP)| = |n_H C_H+n_S C_S| <= {fmt(bound)}`.

## Hodge/Poynting Owner Theorem
{md_table(owner, ["theorem_id", "claim_piece", "derivation_status", "payoff"])}

## Chi-To-Hodge Premise Audit
{md_table(audit, ["premise_id", "premise", "current_status", "source_status", "blocks_zero_claim"])}

## Poynting Branch Decision Table
{md_table(branches, ["branch_id", "route", "condition", "consequence", "status", "double_counting"])}

## C_H/C_S Formula Rows
{md_table(formula, ["formula_id", "object", "formula", "required_inputs"])}

## First C_H/C_S Slope Rows
{md_table(finite, ["row_id", "factor_target", "C_R_HP_prediction", "C_R_HP_abs_bound", "source_status", "result", "valid_for_claim"])}

## C_H/C_S Bound Runner
{md_table(runner, ["row_id", "C_R_HP_prediction", "prediction_over_bound", "result", "expectation_met", "valid_for_claim"])}

## Promotion Gates
{md_table(promotion, ["gate_id", "passed", "claim_allowed", "detail"])}

## Decisions
{md_table(decision, ["decision_id", "decision", "why_it_moves_forward", "claim_allowed"])}

## Next Target
{md_table(next_target, ["next_id", "target_doc", "objective", "guardrail"])}

## Validation
{md_table(validation, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    fw_before = snapshot_tree(FW)
    bound = bound_from_3285()
    sources = source_register_rows()
    owner = owner_theorem_rows()
    audit = premise_audit_rows()
    branches = branch_rows()
    formula = formula_rows(bound)
    finite = finite_rows(bound)
    runner = runner_rows(finite)
    promotion = promotion_rows()
    decision = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["owner"], owner)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["branches"], branches)
    write_csv(OUTPUTS["formula"], formula)
    write_csv(OUTPUTS["finite"], finite)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)

    validation = validate(fw_before, sources, owner, audit, branches, formula, runner, promotion, next_target)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(bound, owner, audit, branches, formula, finite, runner, promotion, decision, next_target, validation)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
