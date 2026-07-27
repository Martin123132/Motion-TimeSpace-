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

DOC = ROOT / "3290-Y5-R2FR-no-hidden-ZQ-coefficient-or-source-current-universality-under-AX1090.md"

SRC_3289_DOC = ROOT / "3289-Y5-R2FR-qbasic-ZQ-vertical-silence-or-alpha-product-residual-under-AX1090.md"
SRC_3289_NEXT = OUT / "P8_Y5_R2FR_3289_NEXT_TARGET.csv"
SRC_3289_THEOREM = OUT / "P8_Y5_R2FR_3289_QBASIC_ZQ_THEOREM.csv"
SRC_3289_PIECES = OUT / "P8_Y5_R2FR_3289_ZQ_PIECE_VERTICAL_AUDIT.csv"
SRC_3289_PRODUCTS = OUT / "P8_Y5_R2FR_3289_ALPHA_ZQ_PRODUCT_RESIDUAL_ROWS_NONCLAIM.csv"
SRC_3289_VALIDATION = OUT / "P8_Y5_BRR545_3289_VALIDATION.csv"
SRC_1049_DOC = ROOT / "1049-Y5-R10-parent-operator-classification-symmetry-ban-or-residual-coefficient-prior.md"
SRC_1050_DOC = ROOT / "1050-Y5-R10-visible-hidden-product-functor-derivation-or-prior-width-source-pack.md"
SRC_1051_DOC = ROOT / "1051-Y5-R10-no-mixed-hidden-visible-morphism-lemma-or-first-prior-width-chain.md"
SRC_1054_DOC = ROOT / "1054-Y5-R10-beta-source-alpha-zero-theorem-or-first-numeric-prior-width.md"
SRC_1062_DOC = ROOT / "1062-Y5-R10-parent-source-normalization-tauWEP-product-theorem-or-WEP-alpha-closure.md"
SRC_1100_DOC = ROOT / "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"
SRC_953_SOURCE_FUNCTOR = OUT / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv"
SRC_1054_ZERO = OUT / "P8_Y5_R10_1054_FORMAL_ZERO_PROOF_ATTEMPT.csv"
SRC_1054_WIDTH = OUT / "P8_Y5_R10_1054_NUMERIC_PRIOR_WIDTH_LEDGER.csv"
SRC_1051_CLOCK_CHAIN = OUT / "P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3290_SOURCE_REGISTER.csv",
    "hidden": OUT / "P8_Y5_R2FR_3290_NO_HIDDEN_ZQ_COEFFICIENT_THEOREM.csv",
    "source": OUT / "P8_Y5_R2FR_3290_SOURCE_CURRENT_UNIVERSALITY_THEOREM.csv",
    "obstructions": OUT / "P8_Y5_R2FR_3290_COUNTEREXAMPLE_OBSTRUCTION_SPLIT.csv",
    "residuals": OUT / "P8_Y5_R2FR_3290_HIDDEN_ZQ_SOURCE_ALPHA_RESIDUAL_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3290_SPLIT_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3290_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3290_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3290_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3290_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
DEFAULT_BOUND = 1.389797711495e-12


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def fmt(value: float) -> str:
    return f"{value:.12e}"


def compact(value: Any, limit: int = 460) -> str:
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
            hits.append(f"L{idx}:{compact(line, 285)}")
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


def bound_from_3289() -> float:
    if not SRC_3289_PRODUCTS.exists():
        return DEFAULT_BOUND
    for row in read_csv(SRC_3289_PRODUCTS):
        if row.get("row_id") == "AZQ3289_2_hidden_ZQ_drift":
            try:
                return float(row["abs_bound"])
            except (KeyError, ValueError):
                return DEFAULT_BOUND
    return DEFAULT_BOUND


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (SRC_3289_DOC, "3289 handoff", ["hidden", "source/current"]),
        (SRC_3289_NEXT, "3289 next target", ["no-hidden-ZQ", "source-current"]),
        (SRC_3289_THEOREM, "q-basic Z_Q theorem", ["L_v ln Z_Q", "f_X"]),
        (SRC_3289_PIECES, "Z_Q piece vertical audit", ["ZQP3289_2_hidden_scalar", "ZQP3289_5_source_current"]),
        (SRC_3289_PRODUCTS, "alpha/Z_Q residual rows", ["AZQ3289_5_WEP_R10", "beta_source_alpha"]),
        (SRC_3289_VALIDATION, "3289 validation", ["VAL3289_12_overall", "true"]),
        (SRC_1049_DOC, "operator classification and symmetry limits", ["f_X", "DOES_NOT_FORBID"]),
        (SRC_1050_DOC, "visible-hidden product functor", ["Hom(C_hid", "source labels"]),
        (SRC_1051_DOC, "no-mixed morphism obstruction", ["NMM1051_2_scalar_counterexample", "b_alpha"]),
        (SRC_1054_DOC, "beta_source_alpha zero theorem", ["beta_source_alpha=0", "source-label"]),
        (SRC_1062_DOC, "WEP source/current theorem attempt", ["source-label forgetting", "Noether current"]),
        (SRC_1100_DOC, "T_Q/gauge norm and current owner", ["same_current", "Z_A"]),
        (SRC_953_SOURCE_FUNCTOR, "source functor theorem attempt", ["NSF953", "verdict"]),
        (SRC_1054_ZERO, "formal beta_source_alpha zero proof", ["beta_source_alpha", "CONDITIONAL"]),
        (SRC_1054_WIDTH, "numeric WEP product target", ["4.797780522732e-05", "beta_source_alpha"]),
        (SRC_1051_CLOCK_CHAIN, "clock product chain", ["BAP1051_2_best_current_product", "2.1e-18"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3290_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def hidden_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "NHZ3290_0_target",
            "claim_piece": "no hidden Z_Q coefficient",
            "statement": "Forbid or constantize Hom(C_hid,Coeff(F_Q^2)); equivalently f_X(I_hid) is absent or L_v f_X=0 on every vertical fibre.",
            "proof_status": "TARGET_SHARP",
            "payoff": "removes the dangerous f_X contribution to L_v Z_Q without requiring numerical alpha prediction.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NHZ3290_1_trivial_hidden_invariant_case",
            "claim_piece": "hidden invariant algebra route",
            "statement": "If O(C_hid)^inv=R, then any natural scalar coefficient c:C_hid->R is constant, so L_v f_X=0.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "payoff": "would close hidden Z_Q drift structurally.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NHZ3290_2_product_functor_case",
            "claim_piece": "visible-hidden product functor route",
            "statement": "If S_vis factors only through q(Phi), theta_rep, and fixed parent gauge data, then f_X(I_hid)F_Q^2 is outside the visible coefficient domain.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "payoff": "would make L_v f_X=0 by domain exclusion rather than tuning.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NHZ3290_3_scalar_counterexample",
            "claim_piece": "why ordinary symmetry is insufficient",
            "statement": "If a surviving invariant scalar I_hid exists, then f_X=f0+epsilon I_hid is diffeomorphism and U(1)-gauge allowed, giving L_v f_X=epsilon L_v I_hid.",
            "proof_status": "COUNTEREXAMPLE_RETAINED",
            "payoff": "current corpus cannot claim no-hidden-Z_Q without product/sequester/trivial-invariant proof.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NHZ3290_4_current_verdict",
            "claim_piece": "hidden Z_Q status",
            "statement": "The no-hidden-Z_Q theorem is coherent but unsigned; retain hidden-Z_Q residual rows.",
            "proof_status": "NOT_PROMOTED",
            "payoff": "separates hidden drift from source-current universality.",
            "valid_for_claim": "false",
        },
    ]


def source_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "SCU3290_0_target",
            "claim_piece": "source-current alpha universality",
            "statement": "The same parent T_Q owner must fix Maxwell normalization, matter current normalization, and source/test charge labels before readout.",
            "proof_status": "TARGET_SHARP",
            "payoff": "removes beta_source_alpha as an independent WEP/R10 source marker.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SCU3290_1_Noether_owner_case",
            "claim_piece": "same Noether current route",
            "statement": "If S_int=sum_A n_A int A_Q J_A with fixed representation labels n_A and J_Q=delta S_matter/delta A_Q from the same T_Q owner, then L_v n_A=L_v J_Q=0.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "payoff": "source/test alpha weights cannot vary independently of the universal current.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SCU3290_2_source_label_forgetting",
            "claim_piece": "species labels unavailable to source coupling",
            "statement": "If the source functor maps ordinary matter to T_total before coupling selection, not to species-labelled pairs (T_A,A), then relative source weights and beta_source_alpha slots are structurally absent.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "payoff": "kills WEP/R10 source-charge residual at the category level.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SCU3290_3_relative_weight_counterexample",
            "claim_piece": "why additivity is insufficient",
            "statement": "If species labels remain available, S_source=sum_A kappa_A T_A is additive/covariant and can carry composition-sensitive source weights.",
            "proof_status": "COUNTEREXAMPLE_RETAINED",
            "payoff": "source-current universality is not implied by covariance alone.",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "SCU3290_4_current_verdict",
            "claim_piece": "source-current status",
            "statement": "The source-current universality theorem is coherent but unsigned; retain beta_source_alpha/WEP/R10 residual rows.",
            "proof_status": "NOT_PROMOTED",
            "payoff": "keeps WEP/R10 separated from pure Z_Q vertical drift.",
            "valid_for_claim": "false",
        },
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    return [
        {
            "obstruction_id": "OBS3290_0_hidden_scalar",
            "sector": "hidden Z_Q",
            "counterexample": "I_hid survives and f_X=f0+epsilon I_hid multiplies F_Q^2",
            "why_allowed": "diffeomorphism and U(1) gauge invariance do not forbid scalar gauge kinetic functions",
            "repair": "prove trivial hidden invariant algebra or product/no-mixed visible coefficient domain",
            "valid_for_claim": "false",
        },
        {
            "obstruction_id": "OBS3290_1_radiative_reentry",
            "sector": "hidden Z_Q/readout",
            "counterexample": "tree-level no-mixed action but S_eff/readout regenerates delta f_X F_Q^2 or Hodge/hbar*c drift",
            "why_allowed": "effective reduction/readout closure is separate from bare action form",
            "repair": "radiative/readout closure theorem",
            "valid_for_claim": "false",
        },
        {
            "obstruction_id": "OBS3290_2_relative_source_weight",
            "sector": "source current",
            "counterexample": "S_source=sum_A kappa_A T_A or q_A(Xhat)A_QJ_A",
            "why_allowed": "covariant/additive if species labels are still visible to the source functor",
            "repair": "source-label forgetting plus same T_Q Noether owner",
            "valid_for_claim": "false",
        },
        {
            "obstruction_id": "OBS3290_3_arena_projection",
            "sector": "WEP/R10 transfer",
            "counterexample": "clock b_alpha product reused as WEP/R10 source prediction",
            "why_allowed": "tau_WEP/tau_R10 and source/test alpha charges are separate projections",
            "repair": "derive arena projection maps or keep product-only rows",
            "valid_for_claim": "false",
        },
    ]


def residual_rows(bound: float) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "HSR3290_0_both_gates_zero_conditional",
            "target": "hidden Z_Q plus source-current alpha branch",
            "prediction": "0",
            "abs_bound": fmt(bound),
            "source_status": "THEOREM_CONDITIONAL_IF_NO_HIDDEN_AND_SOURCE_UNIVERSALITY_SIGNED",
            "result": "PASS_NUMERIC_NONCLAIM",
            "missing_for_claim": "parent-signed no-hidden-visible coefficient theorem; same T_Q Noether current owner; source-label forgetting; radiative/readout closure",
            "valid_for_claim": "false",
        },
        {
            "row_id": "HSR3290_1_hidden_ZQ_residual",
            "target": "hidden Z_Q coefficient",
            "prediction": "Z_Q^{-1} f_X'(I_hid) L_v I_hid",
            "abs_bound": fmt(bound),
            "source_status": "MISSING_NUMERIC_HIDDEN_ZQ_PROJECTION",
            "result": "REFUSE_MISSING_SOURCE_NONCLAIM",
            "missing_for_claim": "I_hid normalization, f_X derivative, vertical generator, arena map",
            "valid_for_claim": "false",
        },
        {
            "row_id": "HSR3290_2_WEP_beta_source_alpha_product",
            "target": "MICROSCOPE/WEP alpha source product",
            "prediction": "|beta_source_alpha*b_alpha*tau_WEP| <= 4.797780522732e-05 in 1054 smoke convention",
            "abs_bound": "4.797780522732e-05",
            "source_status": "PRODUCT_TARGET_AVAILABLE_NONCLAIM",
            "result": "PRODUCT_TARGET_AVAILABLE_STANDALONE_BLOCKED",
            "missing_for_claim": "standalone beta_source_alpha, standalone b_alpha, tau_WEP, material convention, shared domain map",
            "valid_for_claim": "false",
        },
        {
            "row_id": "HSR3290_3_R10_source_alpha_placeholder",
            "target": "R10 source/test alpha exchange",
            "prediction": "K_X(lambda)*beta_s(lambda)*beta_t(lambda)+epsilon_tail(lambda)",
            "abs_bound": fmt(bound),
            "source_status": "MISSING_R10_SOURCE_TEST_PROJECTION",
            "result": "REFUSE_MISSING_SOURCE_NONCLAIM",
            "missing_for_claim": "lambda_X, K_X, beta_s, beta_t, tau_R10, promoted bound curve",
            "valid_for_claim": "false",
        },
        {
            "row_id": "HSR3290_4_clock_product_retained",
            "target": "clock alpha product",
            "prediction": "|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1 best current imported row",
            "abs_bound": "2.1e-18",
            "source_status": "SOURCE_BACKED_PRODUCT_NONCLAIM",
            "result": "PRODUCT_BOUND_AVAILABLE_STANDALONE_BLOCKED",
            "missing_for_claim": "tau_clock_time and Xhat/Z_Q normalization; cannot transfer to WEP/R10",
            "valid_for_claim": "false",
        },
        {
            "row_id": "HSR3290_5_half_bound_smoke",
            "target": "numeric smoke inside envelope",
            "prediction": fmt(0.5 * bound),
            "abs_bound": fmt(bound),
            "source_status": "SMOKE_ONLY",
            "result": "SMOKE",
            "missing_for_claim": "none; schema test only",
            "valid_for_claim": "false",
        },
        {
            "row_id": "HSR3290_6_twice_bound_smoke",
            "target": "numeric smoke outside envelope",
            "prediction": fmt(2.0 * bound),
            "abs_bound": fmt(bound),
            "source_status": "SMOKE_ONLY",
            "result": "SMOKE",
            "missing_for_claim": "none; schema test only",
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
    expected = {
        "HSR3290_0_both_gates_zero_conditional": "PASS_NUMERIC_NONCLAIM",
        "HSR3290_1_hidden_ZQ_residual": "REFUSE_MISSING_SOURCE_NONCLAIM",
        "HSR3290_2_WEP_beta_source_alpha_product": "PRODUCT_TARGET_AVAILABLE_STANDALONE_BLOCKED",
        "HSR3290_3_R10_source_alpha_placeholder": "REFUSE_MISSING_SOURCE_NONCLAIM",
        "HSR3290_4_clock_product_retained": "PRODUCT_BOUND_AVAILABLE_STANDALONE_BLOCKED",
        "HSR3290_5_half_bound_smoke": "PASS_NUMERIC_NONCLAIM",
        "HSR3290_6_twice_bound_smoke": "FAIL_BOUND",
    }
    output: list[dict[str, Any]] = []
    for row in rows:
        prediction = str(row["prediction"])
        source_status = str(row["source_status"])
        if source_status.startswith("MISSING"):
            result = "REFUSE_MISSING_SOURCE_NONCLAIM"
            ratio = "N/A"
        elif source_status == "PRODUCT_TARGET_AVAILABLE_NONCLAIM":
            result = "PRODUCT_TARGET_AVAILABLE_STANDALONE_BLOCKED"
            ratio = "N/A"
        elif source_status == "SOURCE_BACKED_PRODUCT_NONCLAIM":
            result = "PRODUCT_BOUND_AVAILABLE_STANDALONE_BLOCKED"
            ratio = "N/A"
        elif is_number(prediction):
            bound = float(row["abs_bound"])
            value = abs(float(prediction))
            ratio = fmt(value / bound)
            result = "PASS_NUMERIC_NONCLAIM" if value <= bound else "FAIL_BOUND"
        else:
            result = "SYMBOLIC_NONNUMERIC_NONCLAIM"
            ratio = "N/A"
        output.append(
            {
                "row_id": row["row_id"],
                "prediction": prediction,
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
            "gate_id": "GATE3290_0_hidden_theorem_shape",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "no-hidden-Z_Q has exact conditional routes through trivial hidden invariant algebra or product functor.",
        },
        {
            "gate_id": "GATE3290_1_hidden_theorem_signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "surviving scalar invariant counterexample remains open; ordinary symmetries do not ban f_X F_Q^2.",
        },
        {
            "gate_id": "GATE3290_2_source_universality_shape",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "same T_Q Noether owner/source-label forgetting gives exact conditional beta_source_alpha zero.",
        },
        {
            "gate_id": "GATE3290_3_source_universality_signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "same current owner, source-label forgetting, and tau_WEP/R10 projections are unsigned.",
        },
        {
            "gate_id": "GATE3290_4_product_rows_nonclaim",
            "passed": "true_nonclaim_only",
            "claim_allowed": "false",
            "detail": "clock and WEP products are retained only as product pressure, not standalone b_alpha/beta_source_alpha.",
        },
        {
            "gate_id": "GATE3290_5_no_claim",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "no local-GR/Maxwell/alpha/WEP/R10/clock claim is allowed from 3290.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3290_0_split_result",
            "decision": "Hidden Z_Q drift and source-current alpha weights are distinct blockers.",
            "why_it_moves_forward": "we no longer blur f_X drift with beta_source_alpha/WEP source charge.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3290_1_hidden_result",
            "decision": "No-hidden-Z_Q is not proved because a hidden scalar coefficient counterexample survives.",
            "why_it_moves_forward": "the only clean proof routes are product/no-mixed functor or trivial hidden invariant algebra.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3290_2_source_result",
            "decision": "Source-current universality is not proved but has a precise Noether/source-label route.",
            "why_it_moves_forward": "the best next derivation target is same T_Q current owner plus source-label forgetting, not WEP fitting.",
            "claim_allowed": "false",
        },
        {
            "decision_id": "DEC3290_3_next_work",
            "decision": "Next attack should focus on T_Q Noether current owner/source-label forgetting first.",
            "why_it_moves_forward": "it is more concrete than trying to prove hidden invariant algebra triviality in one leap.",
            "claim_allowed": "false",
        },
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3290_0_3291",
            "target_doc": "3291-Y5-R2FR-TQ-Noether-current-owner-and-source-label-forgetting-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3291_TQ_Noether_current_owner_and_source_label_forgetting.py",
            "objective": "Try the most concrete source-coupling proof: derive same T_Q Noether current owner plus source-label forgetting so beta_source_alpha is structurally absent; if not, retain WEP/R10 source-current residual rows without transferring clock bounds.",
            "guardrail": "Do not claim WEP/R10/local-GR; do not use covariance/additivity alone as universality; do not transfer clock alpha products to source tests without tau/source projection maps.",
            "valid_for_claim": "false",
        }
    ]


def validate(
    fw_before: dict[str, tuple[int, int]],
    sources: list[dict[str, Any]],
    hidden: list[dict[str, Any]],
    source: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    non_validation_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    fw_changed = changed_count(fw_before, snapshot_tree(FW))
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        checks.append({"check_id": check_id, "check": check, "passed": bool_str(passed), "detail": compact(detail, 700)})

    add("VAL3290_0_sources_exist", "all cited source paths exist", all(row["exists"] == "true" for row in sources))
    add("VAL3290_1_sources_parse", "all cited source paths parse", all(row["parse_ok"] == "true" for row in sources))
    add("VAL3290_2_outputs_parse", "all 3290 non-validation output CSVs parse", all(csv_parse_ok(path) for path in non_validation_outputs), "non-validation outputs parsed before validation write")
    add("VAL3290_3_hidden_theorem_and_counterexample", "hidden theorem includes exact no-mixed route and scalar counterexample", any(row["theorem_id"] == "NHZ3290_1_trivial_hidden_invariant_case" for row in hidden) and any(row["theorem_id"] == "NHZ3290_3_scalar_counterexample" for row in hidden))
    add("VAL3290_4_source_theorem_and_counterexample", "source theorem includes Noether owner and relative-weight counterexample", any(row["theorem_id"] == "SCU3290_1_Noether_owner_case" for row in source) and any(row["theorem_id"] == "SCU3290_3_relative_weight_counterexample" for row in source))
    add("VAL3290_5_obstruction_split_complete", "obstructions split hidden, radiative, source, and arena projection", len(obstructions) == 4 and all(row["valid_for_claim"] == "false" for row in obstructions))
    add("VAL3290_6_product_rows_nonclaim", "WEP and clock product rows are retained but standalone blocked", any(row["row_id"] == "HSR3290_2_WEP_beta_source_alpha_product" and "standalone" in row["missing_for_claim"] for row in residuals) and any(row["row_id"] == "HSR3290_4_clock_product_retained" and "cannot transfer" in row["missing_for_claim"] for row in residuals))
    add("VAL3290_7_runner_expectations", "split runner expectations all match", all(row["expectation_met"] == "true" for row in runner), ";".join(f"{row['row_id']}={row['result']}" for row in runner))
    add("VAL3290_8_claim_gates_false", "no 3290 gate allows local-GR/alpha/WEP/R10 claim", all(row["claim_allowed"] == "false" for row in promotion) and all(row["valid_for_claim"] == "false" for row in residuals))
    add("VAL3290_9_next_target_focused", "next target focuses T_Q Noether current and source-label forgetting", any("TQ-Noether-current" in row["target_doc"] and "source-label-forgetting" in row["target_doc"] for row in next_target))
    add("VAL3290_10_formalization_untouched", "formalization-workbench modified-file count remains zero by this script", fw_changed == 0, f"formalization_changed_count={fw_changed}")
    overall = all(row["passed"] == "true" for row in checks)
    add("VAL3290_11_overall", "3290 validation overall", overall, "all required checks passed" if overall else "one or more checks failed")
    return checks


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(col, "")) for col in columns) + " |")
    return "\n".join(lines)


def write_doc(
    hidden: list[dict[str, Any]],
    source: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    promotion: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    text = f"""# 3290 - No-hidden Z_Q coefficient or source-current universality under AX1090

## Summary

3290 splits the remaining coupling problem into two separate gates:

1. **Hidden Z_Q coefficient gate:** forbid `f_X(I_hid)F_Q^2`, or prove it is constant on vertical fibres.
2. **Source-current universality gate:** prove the same parent `T_Q` Noether owner fixes Maxwell normalization, matter current normalization, and source/test charge labels.

This matters because a clean local Maxwell/GR limit can tolerate calibrated constants, but it cannot tolerate either hidden alpha drift or composition/source-dependent alpha weights.

The hidden route has an exact conditional theorem:

`O(C_hid)^inv = R` or `Hom(C_hid,Coeff(F_Q^2)) = Const/0` implies `L_v f_X=0`.

But the current corpus keeps the counterexample:

`f_X = f0 + epsilon I_hid`, so `L_v f_X = epsilon L_v I_hid`.

The source-current route also has an exact conditional theorem:

same `T_Q` owner plus fixed charge labels plus source-label forgetting implies `beta_source_alpha=0`.

But covariance/additivity alone still allows relative source weights if species labels remain available.

So 3290 does not claim local-GR, WEP, R10, or alpha silence. It narrows the next best attack to the more concrete source-current route.

## No-Hidden Z_Q Coefficient Theorem
{md_table(hidden, ["theorem_id", "claim_piece", "proof_status", "statement"])}

## Source-Current Universality Theorem
{md_table(source, ["theorem_id", "claim_piece", "proof_status", "statement"])}

## Counterexample Obstruction Split
{md_table(obstructions, ["obstruction_id", "sector", "counterexample", "repair"])}

## Hidden Z_Q / Source Alpha Residual Rows
{md_table(residuals, ["row_id", "target", "prediction", "source_status", "result", "valid_for_claim"])}

## Split Runner
{md_table(runner, ["row_id", "prediction", "prediction_over_bound", "result", "expectation_met", "valid_for_claim"])}

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
    bound = bound_from_3289()
    sources = source_register_rows()
    hidden = hidden_theorem_rows()
    source = source_theorem_rows()
    obstructions = obstruction_rows()
    residuals = residual_rows(bound)
    runner = runner_rows(residuals)
    promotion = promotion_rows()
    decision = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["hidden"], hidden)
    write_csv(OUTPUTS["source"], source)
    write_csv(OUTPUTS["obstructions"], obstructions)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["promotion"], promotion)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)

    validation = validate(fw_before, sources, hidden, source, obstructions, residuals, runner, promotion, next_target)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(hidden, source, obstructions, residuals, runner, promotion, decision, next_target, validation)

    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
