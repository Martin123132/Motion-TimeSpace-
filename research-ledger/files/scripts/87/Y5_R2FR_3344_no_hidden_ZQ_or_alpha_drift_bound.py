from __future__ import annotations

import csv
import hashlib
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

DOC = ROOT / "3344-Y5-R2FR-no-hidden-ZQ-or-alpha-drift-bound-under-AX1090.md"

SOURCES = [
    {
        "source_id": "SRC3344_0_3343_doc",
        "path": ROOT / "3343-Y5-R2FR-epsilon-EM-public-Hodge-Poynting-zero-or-bound-under-AX1090.md",
        "role": "3343 handoff selecting no-hidden Z_Q / b_alpha first",
    },
    {
        "source_id": "SRC3344_1_3343_residuals",
        "path": OUT / "P8_Y5_R2FR_3343_EPSILON_EM_RESIDUAL_DECOMPOSITION.csv",
        "role": "epsilon_EM residual decomposition",
    },
    {
        "source_id": "SRC3344_2_3343_component_rows",
        "path": OUT / "P8_Y5_R2FR_3343_FRV3340_EPSILON_EM_COMPONENT_ROWS.csv",
        "role": "3343 nonclaim epsilon_EM component rows",
    },
    {
        "source_id": "SRC3344_3_3289_qbasic_zq",
        "path": OUT / "P8_Y5_R2FR_3289_QBASIC_ZQ_THEOREM.csv",
        "role": "Z_Q decomposition and alpha relation",
    },
    {
        "source_id": "SRC3344_4_3290_no_hidden_zq",
        "path": OUT / "P8_Y5_R2FR_3290_NO_HIDDEN_ZQ_COEFFICIENT_THEOREM.csv",
        "role": "no-hidden Z_Q theorem and scalar counterexample",
    },
    {
        "source_id": "SRC3344_5_3117_alpha_priority",
        "path": OUT / "P8_Y5_R2FR_3117_EM_COUPLING_OWNER_ALPHA_PRIORITY.csv",
        "role": "alpha value versus hidden local derivative split",
    },
    {
        "source_id": "SRC3344_6_2659_domain_theorem",
        "path": OUT / "P8_Y5_NO_HIDDEN_VISIBLE_HOM_2659_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
        "role": "ordinary coefficient-domain no-hidden-visible-hom theorem",
    },
    {
        "source_id": "SRC3344_7_1051_product_chain",
        "path": OUT / "P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv",
        "role": "source-backed b_alpha*tau_clock product rows",
    },
    {
        "source_id": "SRC3344_8_1051_projection_readiness",
        "path": OUT / "P8_Y5_R10_1051_B_ALPHA_PROJECTION_READINESS.csv",
        "role": "clock/WEP/R10/PPN projection readiness",
    },
    {
        "source_id": "SRC3344_9_1052_clock_product_bounds",
        "path": OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv",
        "role": "clock product bound ledger",
    },
    {
        "source_id": "SRC3344_10_1059_product_pack",
        "path": OUT / "P8_Y5_R10_1059_ALPHA_PRODUCT_PRIOR_PACK.csv",
        "role": "alpha product prior pack",
    },
    {
        "source_id": "SRC3344_11_1111_alpha_zero_attempt",
        "path": OUT / "P8_Y5_R10_1111_ALPHA_DRIFT_ZERO_THEOREM_ATTEMPT.csv",
        "role": "alpha drift zero theorem attempt",
    },
    {
        "source_id": "SRC3344_12_1112_product_contract",
        "path": OUT / "P8_Y5_R10_1112_ALPHA_PRODUCT_RUNNER_CONTRACT_NONCLAIM.csv",
        "role": "alpha product runner contract",
    },
    {
        "source_id": "SRC3344_13_1113_input_ledger",
        "path": OUT / "P8_Y5_R10_1113_ALPHA_PRODUCT_INPUT_ACQUISITION_LEDGER.csv",
        "role": "alpha product missing input ledger",
    },
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3344_SOURCE_REGISTER.csv",
    "zq_decomposition": OUT / "P8_Y5_R2FR_3344_ZQ_DECOMPOSITION_AND_VERTICAL_DERIVATIVE.csv",
    "no_hidden_theorem": OUT / "P8_Y5_R2FR_3344_NO_HIDDEN_ZQ_THEOREM_OR_COUNTERMODEL.csv",
    "alpha_relation": OUT / "P8_Y5_R2FR_3344_ALPHA_READOUT_RELATION.csv",
    "product_bounds": OUT / "P8_Y5_R2FR_3344_B_ALPHA_PRODUCT_BOUND_ROWS.csv",
    "standalone_refusal": OUT / "P8_Y5_R2FR_3344_STANDALONE_BALPHA_REFUSAL.csv",
    "epsilon_subcomponent": OUT / "P8_Y5_R2FR_3344_EPSILON_EM_BALPHA_SUBCOMPONENT_UPDATE.csv",
    "cross_arena_guard": OUT / "P8_Y5_R2FR_3344_CROSS_ARENA_TRANSFER_GUARD.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3344_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3344_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3344_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3344_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()
BEST_PRODUCT_BOUND = 2.1e-18
BEST_PRODUCT_BOUND_2SIGMA = 3.2e-18


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def compact(value: Any, limit: int = 1800) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: compact(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def sha256_prefix(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()[:16]


def snapshot_tree(path: Path) -> dict[str, tuple[int, int]]:
    if not path.exists():
        return {}
    result: dict[str, tuple[int, int]] = {}
    for item in path.rglob("*"):
        if item.is_file():
            try:
                stat = item.stat()
            except OSError:
                continue
            result[str(item.relative_to(path))] = (stat.st_size, stat.st_mtime_ns)
    return result


def changed_count(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> int:
    keys = set(before) | set(after)
    return sum(1 for key in keys if before.get(key) != after.get(key))


def parse_float(value: str) -> float | None:
    try:
        if value == "" or value.startswith("MISSING"):
            return None
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["path"]
        rows.append(
            {
                "source_id": source["source_id"],
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "sha256_prefix": sha256_prefix(path),
                "role": source["role"],
                "valid_for_claim": "false",
            }
        )
    return rows


def product_bound_from_ledger() -> float:
    path = OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"
    if not path.exists():
        return BEST_PRODUCT_BOUND
    for row in read_csv(path):
        if row.get("bound_id") == "ACB1052_2":
            value = parse_float(row.get("product_bound_1sigma_yr_inv", ""))
            if value is not None:
                return value
    return BEST_PRODUCT_BOUND


def zq_decomposition_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "ZQD3344_0_decomposition",
            "object": "Z_Q_eff",
            "formula": "Z_Q_eff = C_P N_Q + lambda_A0 + f_X(I_hid) + Delta_rad(mu,X) + Delta_readout(rho,X)",
            "derivation": "This separates calibrated constant normalization from hidden, radiative, and readout drift channels.",
            "zero_condition": "L_v(C_P N_Q)=L_v lambda_A0=L_v f_X=L_v Delta_rad=L_v Delta_readout=0",
            "status": "EXACT_DECOMPOSITION_CONTRACT",
            "valid_for_claim": "false",
        },
        {
            "row_id": "ZQD3344_1_vertical_derivative",
            "object": "L_v ln Z_Q_eff",
            "formula": "L_v ln Z_Q_eff = Z_Q_eff^{-1}[L_v(C_P N_Q)+L_v lambda_A0+L_v f_X+L_v Delta_rad+L_v Delta_readout]",
            "derivation": "Chain rule for a finite nonzero gauge normalization.",
            "zero_condition": "every bracketed drift term is zero independently; no unrelated cancellations",
            "status": "EXACT_CHAIN_RULE_THEOREM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "ZQD3344_2_constant_allowed",
            "object": "lambda_A0",
            "formula": "L_v lambda_A0=0",
            "derivation": "A universal hidden-independent constant changes the calibrated alpha value but does not create a local derivative residual.",
            "zero_condition": "lambda_A0 is fixed representation/calibration data, not f_X(I_hid)",
            "status": "PARTIAL_ZERO_DERIVED_ALPHA_VALUE_NOT_PREDICTED",
            "valid_for_claim": "false",
        },
    ]


def no_hidden_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "NHZ3344_0_target",
            "claim_piece": "no hidden Z_Q coefficient",
            "statement": "Forbid or constantize Hom(C_hid,Coeff(F_Q^2)); equivalently f_X(I_hid) is absent or L_v f_X=0 on every local vertical fibre.",
            "proof_status": "TARGET_SHARP",
            "payoff": "removes the dangerous hidden contribution to b_alpha without requiring numerical alpha prediction",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NHZ3344_1_typed_domain_route",
            "claim_piece": "ordinary coefficient domain exclusion",
            "statement": "If Allowed[S_ord] has coefficient algebra A_ord=q^*A_Q + A_fixed, then any hidden-to-visible coefficient map f_X:I_hid->Coeff(F_Q^2) is not well typed.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "payoff": "would set L_v f_X=0 by domain exclusion rather than smallness",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NHZ3344_2_trivial_hidden_invariant_route",
            "claim_piece": "constant hidden invariant algebra",
            "statement": "If O(C_hid)^inv=R, every natural scalar coefficient from the hidden fibre is constant, so L_v f_X=0.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "payoff": "would close hidden Z_Q drift structurally",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NHZ3344_3_countermodel",
            "claim_piece": "ordinary symmetry is insufficient",
            "statement": "If a surviving hidden scalar I_hid exists, f_X=f0+epsilon I_hid is diffeomorphism and U(1)-gauge allowed and gives L_v f_X=epsilon L_v I_hid.",
            "proof_status": "COUNTERMODEL_RETAINED",
            "payoff": "current corpus cannot claim no-hidden-Z_Q from covariance or gauge symmetry alone",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "NHZ3344_4_verdict",
            "claim_piece": "current no-hidden Z_Q status",
            "statement": "The theorem shape is exact, but the parent ordinary coefficient domain is not signed, so b_alpha theorem-zero is not promoted.",
            "proof_status": "NOT_PROMOTED",
            "payoff": "b_alpha remains a finite/product-bound branch, not a local-GR failure by itself",
            "valid_for_claim": "false",
        },
    ]


def alpha_relation_rows() -> list[dict[str, Any]]:
    return [
        {
            "relation_id": "AR3344_0_alpha_to_ZQ",
            "statement": "In the selected readout convention alpha_EM is proportional to 1/(hbar c Z_Q_eff).",
            "formula": "b_alpha := L_v ln alpha_EM = -L_v ln Z_Q_eff - L_v ln(hbar c) + readout_terms",
            "condition": "if hbar, c, and readout standards are q-basic, b_alpha=-L_v ln Z_Q_eff",
            "status": "EXACT_CONDITIONAL_READOUT_RELATION",
            "valid_for_claim": "false",
        },
        {
            "relation_id": "AR3344_1_alpha_value_vs_drift",
            "statement": "MTS does not need to predict the numerical value of alpha to pass local Maxwell; it must prevent or bound local hidden derivative drift.",
            "formula": "lambda_A0 may calibrate alpha while L_v lambda_A0=0",
            "condition": "constant universal calibration is allowed; hidden-visible derivative is not",
            "status": "FAIR_STANDARD_DERIVED",
            "valid_for_claim": "false",
        },
    ]


def product_bound_rows() -> list[dict[str, Any]]:
    best = product_bound_from_ledger()
    return [
        {
            "bound_id": "BAP3344_0_best_clock_product",
            "arena": "clock",
            "product_symbol": "P_clock_alpha := b_alpha * tau_clock_time",
            "clock_pair": "171Yb+ E3 / 171Yb+ E2",
            "bound_value_1sigma": f"{best:.6e}",
            "bound_value_2sigma": f"{BEST_PRODUCT_BOUND_2SIGMA:.6e}",
            "bound_units": "yr^-1",
            "source_path": str(OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"),
            "source_row": "ACB1052_2",
            "source_urls": "https://oar.ptb.de/resources/show/10.7795/110.20211216; https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2023.1104848/full",
            "score_rule": "usable as source-backed product bound only; do not divide by tau_clock_time unless tau is parent-derived",
            "standalone_balpha_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "BAP3344_1_crosscheck_clock_product",
            "arena": "clock",
            "product_symbol": "P_clock_alpha := b_alpha * tau_clock_time",
            "clock_pair": "27Al+ / 199Hg+",
            "bound_value_1sigma": "3.900000e-17",
            "bound_value_2sigma": "6.200000e-17",
            "bound_units": "yr^-1",
            "source_path": str(OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"),
            "source_row": "ACB1052_0",
            "source_urls": "https://www.nist.gov/publications/frequency-ratio-al-and-hg-single-ion-optical-clocks-metrology-17th-decimal-place; https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2023.1104848/full",
            "score_rule": "weaker source-backed product cross-check only",
            "standalone_balpha_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def standalone_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "refusal_id": "REF3344_0_clock_product_not_standalone",
            "claim": "clock rows give a standalone b_alpha bound",
            "refused": "true",
            "reason": "clock rows bound b_alpha*tau_clock_time only; tau_clock_time, Xhat/chi_X normalization, and clock domain map are not derived",
            "required_exit": "derive tau_clock_time from MTS local state or derive direct theorem-zero for b_alpha",
            "valid_for_claim": "false",
        },
        {
            "refusal_id": "REF3344_1_no_tau_unity_shortcut",
            "claim": "set tau_clock_time=1 or H0 by convention",
            "refused": "true",
            "reason": "tau is a physical readout/projection coefficient, not a gauge choice; dividing product bounds by an assumed tau smuggles closure",
            "required_exit": "parent-owned clock readout map and normalization convention",
            "valid_for_claim": "false",
        },
        {
            "refusal_id": "REF3344_2_no_clock_to_R10_transfer",
            "claim": "transfer clock product bound directly to WEP/R10",
            "refused": "true",
            "reason": "WEP and R10 require beta_source_alpha, beta_test, material charges, tau_WEP/tau_R10, and the same branch/domain map",
            "required_exit": "cross-arena alpha product vector with source-backed arena projections",
            "valid_for_claim": "false",
        },
    ]


def epsilon_subcomponent_rows() -> list[dict[str, Any]]:
    return [
        {
            "subcomponent_id": "EEM3344_0_b_alpha_theorem_zero_unsigned",
            "parent_component": "FRV3340_4_epsilon_EM",
            "subterm": "b_alpha",
            "mode": "no_hidden_ZQ_theorem_zero",
            "theorem_zero": "true",
            "zero_authority": "CONDITIONAL_NO_HIDDEN_ZQ_NOT_PARENT_SIGNED",
            "component_value": "0.000000e+00",
            "component_units": "dimensionless_vertical_log_derivative",
            "source_path": str(OUTPUTS["no_hidden_theorem"]),
            "runner_acceptance": "false",
            "valid_for_claim": "false",
            "claim_blocker": "ordinary coefficient domain/no-hidden-visible Hom is exact but parent-unsigned",
        },
        {
            "subcomponent_id": "EEM3344_1_b_alpha_clock_product_bound",
            "parent_component": "FRV3340_4_epsilon_EM",
            "subterm": "b_alpha*tau_clock_time",
            "mode": "clock_product_bound_nonclaim",
            "theorem_zero": "false",
            "zero_authority": "NONE",
            "component_value": f"{product_bound_from_ledger():.6e}",
            "component_units": "yr^-1_product_bound",
            "source_path": str(OUTPUTS["product_bounds"]),
            "runner_acceptance": "false",
            "valid_for_claim": "false",
            "claim_blocker": "product-bound units and missing tau_clock_time do not supply standalone dimensionless epsilon_EM b_alpha",
        },
    ]


def cross_arena_guard_rows() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "XAG3344_0_same_alpha_branch",
            "rule": "The same Z_Q_eff/readout branch must feed clocks, WEP, R10, EM stress, and local PPN if b_alpha is used across arenas.",
            "status": "REQUIRED",
            "failure_mode": "clock-only screening or readout-only alpha drift can fake a pass in one arena and fail another",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "XAG3344_1_product_only",
            "rule": "Clock bounds constrain b_alpha*tau_clock_time, not standalone b_alpha.",
            "status": "ENFORCED",
            "failure_mode": "setting tau=1 or H0 without derivation creates a false source-coupling bound",
            "valid_for_claim": "false",
        },
        {
            "guard_id": "XAG3344_2_R10_WEP_projection",
            "rule": "WEP/R10 alpha products require material/source/test charge projections and tau_WEP/tau_R10.",
            "status": "OPEN",
            "failure_mode": "directly transferring clock products to WEP/R10 ignores source/test legs",
            "valid_for_claim": "false",
        },
    ]


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3344_0_chain_rule_theorem",
            "claim": "Z_Q vertical derivative and b_alpha relation are exact",
            "passed": "true",
            "reason": "3344 records decomposition, chain rule, and alpha readout relation.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3344_1_constant_alpha_calibration",
            "claim": "constant lambda_A0 is not a local residual",
            "passed": "true",
            "reason": "a universal hidden-independent constant has zero vertical derivative and only leaves alpha-value calibration debt.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3344_2_no_hidden_ZQ_parent_signed",
            "claim": "b_alpha=0 is parent-signed for MTS",
            "passed": "false",
            "reason": "hidden scalar and ordinary coefficient-domain countermodels survive until parent no-hidden-visible Hom is signed.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3344_3_clock_product_bound",
            "claim": "source-backed b_alpha*tau_clock product bound is staged",
            "passed": "true",
            "reason": "best clock product bound 2.1e-18 yr^-1 is retained as product-only nonclaim evidence.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3344_4_standalone_balpha_bound",
            "claim": "standalone b_alpha finite bound is score-ready",
            "passed": "false",
            "reason": "tau_clock_time and cross-arena projection map are missing.",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3344_5_epsilon_EM_claim",
            "claim": "epsilon_EM component is claim-ready",
            "passed": "false",
            "reason": "b_alpha is product-only or conditional, and delta_J/delta_star/DeltaT_EM/Poynting subterms remain open.",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3344_0",
            "question": "Does MTS need to derive the numerical value of alpha for local Maxwell/GR?",
            "answer": "no",
            "reason": "a constant universal alpha/EM normalization is calibration debt but not a hidden local derivative residual",
            "next_action": "focus on no-hidden drift and readout ownership, not alpha numerology",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3344_1",
            "question": "Did 3344 close b_alpha?",
            "answer": "not yet",
            "reason": "the zero theorem is exact but parent-unsigned; finite evidence is product-only",
            "next_action": "attack the parent ordinary coefficient-domain signature or derive tau_clock_time/direct product from local MTS",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3345-Y5-R2FR-ordinary-coefficient-domain-parent-signature-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3345_ordinary_coefficient_domain_parent_signature.py",
            "objective": "try to parent-sign A_ord=q^*A_Q + A_fixed for ordinary matter/readout coefficients, which would simultaneously zero hidden Z_Q drift, source-only species weights, and several local coupling leaks",
            "why_next": "this is the actual theorem lever behind no-hidden Z_Q and eta_species, not another local patch",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3345b-Y5-R2FR-tau-clock-readout-map-or-direct-alpha-product.md",
            "target_script": "scripts/Y5_R2FR_3345b_tau_clock_readout_map_or_direct_alpha_product.py",
            "objective": "derive tau_clock_time or a direct MTS clock product prediction so source-backed alpha clock bounds can become scoreable product evidence",
            "why_next": "needed if the parent no-hidden theorem remains unsigned and we continue the empirical product route",
            "valid_for_claim": "false",
        },
    ]


def markdown_table(rows: list[dict[str, Any]], limit: int = 20) -> str:
    if not rows:
        return "_No rows._"
    fieldnames: list[str] = []
    for row in rows[:limit]:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows[:limit]:
        values = [compact(row.get(key, ""), 260).replace("|", "\\|") for key in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    if len(rows) > limit:
        lines.append(f"\n_Truncated in markdown: showing {limit} of {len(rows)} rows._")
    return "\n".join(lines)


def render_doc() -> str:
    return "\n\n".join(
        [
            "# 3344 — No-Hidden Z_Q Or Alpha Drift Bound Under AX1090",
            f"Generated: `{RUN_UTC}`",
            "## Summary\n"
            "- `alpha_EM` value prediction and `b_alpha` hidden drift are now separated: a constant universal `lambda_A0` may calibrate alpha without causing a local Maxwell/GR residual.\n"
            "- The no-hidden `Z_Q` theorem is exact if ordinary coefficients live only in `A_ord=q^*A_Q + A_fixed`, but the parent has not signed that domain.\n"
            "- The strongest current finite evidence is source-backed **product-only** clock evidence: `|b_alpha*tau_clock_time| <= 2.1e-18 yr^-1` at 1 sigma.\n"
            "- No standalone `b_alpha`, `epsilon_EM`, WEP/R10 transfer, or local-GR claim is made.",
            "## Z_Q Decomposition\n" + markdown_table(zq_decomposition_rows()),
            "## No-Hidden Z_Q Theorem Or Countermodel\n" + markdown_table(no_hidden_theorem_rows()),
            "## Alpha Readout Relation\n" + markdown_table(alpha_relation_rows()),
            "## b_alpha Product Bounds\n" + markdown_table(product_bound_rows()),
            "## Standalone b_alpha Refusals\n" + markdown_table(standalone_refusal_rows()),
            "## epsilon_EM b_alpha Subcomponent Update\n" + markdown_table(epsilon_subcomponent_rows()),
            "## Cross-Arena Transfer Guard\n" + markdown_table(cross_arena_guard_rows()),
            "## Promotion Gates\n" + markdown_table(promotion_gate_rows()),
            "## Decision Ledger\n" + markdown_table(decision_rows()),
            "## Next Target\n" + markdown_table(next_target_rows()),
        ]
    ) + "\n"


def validate_outputs(formalization_before: dict[str, tuple[int, int]]) -> list[dict[str, Any]]:
    sources = source_rows()
    zq_rows = zq_decomposition_rows()
    theorem_rows = no_hidden_theorem_rows()
    product_rows = product_bound_rows()
    refusals = standalone_refusal_rows()
    subcomponents = epsilon_subcomponent_rows()
    gates = promotion_gate_rows()
    output_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_changed = changed_count(formalization_before, snapshot_tree(FW))
    best_bound = parse_float(product_rows[0]["bound_value_1sigma"])
    checks = [
        {
            "check_id": "VAL3344_0_sources_exist",
            "check": "all cited local source paths exist",
            "passed": all(row["exists"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3344_1_sources_parse",
            "check": "all cited local source paths parse",
            "passed": all(row["parse_ok"] == "true" for row in sources),
            "detail": "",
        },
        {
            "check_id": "VAL3344_2_outputs_parse",
            "check": "all 3344 non-validation outputs parse",
            "passed": all(path.exists() and parse_ok(path) for path in output_paths),
            "detail": "",
        },
        {
            "check_id": "VAL3344_3_zq_chain_rule",
            "check": "Z_Q decomposition includes exact chain rule and constant-calibration partial zero",
            "passed": any(row["status"] == "EXACT_CHAIN_RULE_THEOREM" for row in zq_rows)
            and any(row["status"] == "PARTIAL_ZERO_DERIVED_ALPHA_VALUE_NOT_PREDICTED" for row in zq_rows),
            "detail": "",
        },
        {
            "check_id": "VAL3344_4_no_hidden_countermodel",
            "check": "no-hidden theorem has exact conditional route and retained scalar countermodel",
            "passed": any("CONDITIONAL" in row["proof_status"] for row in theorem_rows)
            and any(row["proof_status"] == "COUNTERMODEL_RETAINED" for row in theorem_rows)
            and any(row["proof_status"] == "NOT_PROMOTED" for row in theorem_rows),
            "detail": "",
        },
        {
            "check_id": "VAL3344_5_product_bound_numeric",
            "check": "best clock product bound is finite positive and product-only",
            "passed": best_bound is not None
            and best_bound > 0
            and product_rows[0]["bound_units"] == "yr^-1"
            and product_rows[0]["standalone_balpha_ready"] == "false",
            "detail": f"best_bound={product_rows[0]['bound_value_1sigma']} {product_rows[0]['bound_units']}",
        },
        {
            "check_id": "VAL3344_6_standalone_refused",
            "check": "standalone b_alpha, tau unity, and clock-to-R10 transfer shortcuts are refused",
            "passed": len(refusals) == 3 and all(row["refused"] == "true" for row in refusals),
            "detail": "",
        },
        {
            "check_id": "VAL3344_7_subcomponent_nonclaim",
            "check": "epsilon_EM b_alpha subcomponent rows remain nonclaim and runner-refused",
            "passed": all(row["valid_for_claim"] == "false" and row["runner_acceptance"] == "false" for row in subcomponents),
            "detail": "",
        },
        {
            "check_id": "VAL3344_8_no_claim",
            "check": "parent b_alpha zero, standalone b_alpha, and epsilon_EM gates remain false",
            "passed": all(
                row["passed"] == "false"
                for row in gates
                if row["gate_id"] in {"GATE3344_2_no_hidden_ZQ_parent_signed", "GATE3344_4_standalone_balpha_bound", "GATE3344_5_epsilon_EM_claim"}
            ),
            "detail": "",
        },
        {
            "check_id": "VAL3344_9_next_target",
            "check": "next target attacks parent coefficient domain and tau clock product route",
            "passed": any("A_ord" in row["objective"] for row in next_target_rows())
            and any("tau_clock_time" in row["objective"] for row in next_target_rows()),
            "detail": "",
        },
        {
            "check_id": "VAL3344_10_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": formalization_changed == 0,
            "detail": f"formalization_changed_count={formalization_changed}",
        },
    ]
    overall = all(bool(check["passed"]) for check in checks)
    checks.append(
        {
            "check_id": "VAL3344_11_overall",
            "check": "3344 validation overall",
            "passed": overall,
            "detail": "all required checks passed" if overall else "one or more checks failed",
        }
    )
    for check in checks:
        check["passed"] = bool_str(bool(check["passed"]))
    return checks


def main() -> None:
    formalization_before = snapshot_tree(FW)
    OUT.mkdir(parents=True, exist_ok=True)
    write_csv(OUTPUTS["sources"], source_rows())
    write_csv(OUTPUTS["zq_decomposition"], zq_decomposition_rows())
    write_csv(OUTPUTS["no_hidden_theorem"], no_hidden_theorem_rows())
    write_csv(OUTPUTS["alpha_relation"], alpha_relation_rows())
    write_csv(OUTPUTS["product_bounds"], product_bound_rows())
    write_csv(OUTPUTS["standalone_refusal"], standalone_refusal_rows())
    write_csv(OUTPUTS["epsilon_subcomponent"], epsilon_subcomponent_rows())
    write_csv(OUTPUTS["cross_arena_guard"], cross_arena_guard_rows())
    write_csv(OUTPUTS["promotion_gates"], promotion_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    DOC.write_text(render_doc(), encoding="utf-8")
    write_csv(OUTPUTS["validation"], validate_outputs(formalization_before))
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


if __name__ == "__main__":
    main()
