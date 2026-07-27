from __future__ import annotations

import csv
import io
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4300"
CLAIM_ID = "L-141"
BRANCH = "MTS_R2FR_Y5_DVGAMMA_M_LCG_ZERO_OR_FIRST_COEFFICIENT_SOURCE_ROW_4300"
DECISION = "VERTICAL_DOUBLE_ZERO_KILLS_DVGAMMA_CONDITIONALLY_FIRST_COEFFICIENT_DEMOTED_TO_SECOND_ORDER_NONCLAIM"
MARKER = "PPC4161_DVGAMMA_M_LCG_ZERO_OR_FIRST_COEFFICIENT_SOURCE_ROW_4300"
PACKET_MARKER = "PPC4161_PACKET_DVGAMMA_M_LCG_ZERO_OR_FIRST_COEFFICIENT_SOURCE_ROW_4300"
NEXT_TARGET = "4301-Y5-R2FR-parent-double-zero-lock-or-second-order-DvGamma-bound-row.md"

FORMAL_PATH = FORMAL / "316-PPC4161-DvGamma-m-Lcg-zero-or-first-coefficient-source-row.md"
DOC_PATH = POST / "4300-Y5-R2FR-DvGamma-m-Lcg-zero-or-first-coefficient-source-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4300_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4300_00_4299_formal": (
        FORMAL / "315-PPC4161-DvGamma-DvKhat-first-source-coefficient-or-QAP-parent-signature.md",
        "D_v Gamma_eff = L_cg^-2 F_m D_v m - 2 Gamma_eff D_v ln L_cg.",
        "4299 exact D_v Gamma_eff chain rule.",
    ),
    "SRC4300_01_4299_dvgamma": (
        SOURCE_DIR / "P8_Y5_R2FR_4299_DVGAMMA_REDUCTION_ROWS.csv",
        "DVG4299_2_Lcg_zero_clause",
        "4299 direct q-basic/zero clauses for D_v m and D_v ln L_cg.",
    ),
    "SRC4300_02_4299_coeff": (
        SOURCE_DIR / "P8_Y5_R2FR_4299_FIRST_SOURCE_COEFFICIENT_TEMPLATE.csv",
        "C4299_DVGAMMA_TOTAL",
        "4299 first D_v Gamma coefficient template.",
    ),
    "SRC4300_03_1290_double_zero": (
        POST / "1290-Y5-R10-RAB-m-Lcg-metric-kernel-source-or-fixed-point-chain-zero.md",
        "MKA1290_3_strict_double_zero_branch",
        "1290 strict double-zero branch that kills algebraic m/Lcg first variations.",
    ),
    "SRC4300_04_1532_double_zero": (
        POST / "1532-Y5-Lcg-parent-ownership-and-fixed-scale-silence-audit.md",
        "ZLCG1532_3_double_zero_sufficient",
        "1532 selects F(m_*)=0 and F_prime(m_*)=0 as the clean Lcg/m chain route.",
    ),
    "SRC4300_05_828_baseline_lock": (
        POST / "828-Y5-R10-XB-Lcg-local-constancy-or-Khat-owner-theorem.md",
        "BL828_2_local_baseline_lock",
        "828 baseline-lock theorem: remove linear trace drift by parent coefficient relation.",
    ),
    "SRC4300_06_1370_fixed_Lcg": (
        POST / "1370-Y5-R10-RAB-parent-Lcg-contract-or-q_loc-weak-field-response-coefficient.md",
        "LCC1370_0_fixed_scalar_parameter",
        "1370 fixed L0 branch supplies a direct Lcg silence alternative.",
    ),
    "SRC4300_07_3521_QAP": (
        POST / "3521-Y5-R2FR-MTS-primitives-to-quotient-action-principle-or-explicit-adoption-gate.md",
        "QAP_NOT_PARENT_DERIVED_YET_EXPLICIT_ADOPTION_GATE_REQUIRED",
        "3521 blocks using quotient identity as an unlabelled hidden axiom.",
    ),
    "SRC4300_08_4293_requirements": (
        SOURCE_DIR / "P8_Y5_R2FR_4293_REQUIRED_SUPPRESSION_ROWS.csv",
        "REQ4293_WEP",
        "4293 imported local precision thresholds.",
    ),
}

ZERO_ROUTES = [
    (
        "ZR4300_0_direct_qbasic",
        "direct q-basic m and L_cg",
        "D_v m=0 and D_v ln L_cg=0",
        "D_v Gamma_eff=0 for any F(m)",
        "Requires QAP/readout-invariance parent signature; still unsigned.",
        "CONDITIONAL_UNSIGNED",
    ),
    (
        "ZR4300_1_fixed_L0_plus_stationary_m",
        "fixed L0 plus stationary m",
        "D_v ln L_cg=0 and F_m(m_*)=0",
        "D_v Gamma_eff=0 if local branch also sits at m=m_*",
        "Cleaner than metric-composite Lcg, but fixed L0 remains a closure candidate.",
        "CONDITIONAL_UNSIGNED",
    ),
    (
        "ZR4300_2_vertical_double_zero",
        "vertical double-zero branch",
        "F(m_*)=0 and F_m(m_*)=0 with finite L_cg and finite D_v m,D_v ln L_cg",
        "D_v Gamma_eff=0 without needing D_v m=0 or D_v ln L_cg=0 separately",
        "Best low-smuggling Gamma route; parent must derive the local lock m=m_*.",
        "EXACT_CONDITIONAL_THEOREM_PARENT_LOCK_UNSIGNED",
    ),
    (
        "ZR4300_3_baseline_lock_generalisation",
        "baseline lock",
        "Gamma_eff=L_cg^-2F(m)=Lambda_loc constant on local branch",
        "D_v Gamma_eff=0 along allowed local branch directions if the lock is a parent relation",
        "More general than strict double zero, but easier to abuse as fitted cancellation.",
        "CONDITIONAL_HIGHER_SCRUTINY",
    ),
    (
        "ZR4300_4_compensated_cancellation",
        "compensated cancellation",
        "L_cg^-2 F_m D_v m = 2 Gamma_eff D_v ln L_cg",
        "D_v Gamma_eff=0 by cancellation",
        "Forbidden unless a parent identity enforces it; no tuning/cancellation credit.",
        "REJECTED_WITHOUT_PARENT_IDENTITY",
    ),
    (
        "ZR4300_5_numeric_source_bound",
        "first numeric coefficient fallback",
        "C_DvGamma_total <= imported 4293 local threshold",
        "D_v Gamma_eff need not vanish if the sourced coefficient is tiny enough",
        "No numeric/source row exists yet; this remains fallback after proof route.",
        "MISSING_SOURCE_ROW",
    ),
]

DOUBLE_ZERO_THEOREM = [
    (
        "DZT4300_0_chain_identity",
        "Start from Gamma_eff=L_cg^-2F(m).",
        "For any vertical v, D_v Gamma_eff=L_cg^-2 F_m D_v m - 2 Gamma_eff D_v ln L_cg.",
        "DERIVED_FROM_4299",
    ),
    (
        "DZT4300_1_double_zero_insert",
        "Impose local branch lock m=m_* with F(m_*)=0 and F_m(m_*)=0.",
        "Then both terms in D_v Gamma_eff vanish at m_* for finite L_cg, D_v m and D_v ln L_cg.",
        "EXACT_CONDITIONAL_ZERO",
    ),
    (
        "DZT4300_2_no_qbasic_needed",
        "The double-zero route does not require D_v m=0 or D_v ln L_cg=0 individually.",
        "It kills the coefficients multiplying those variations.",
        "REAL_ALGEBRAIC_PROGRESS",
    ),
    (
        "DZT4300_3_parent_lock_required",
        "The theorem fires only if the parent action locks the tested local branch to m=m_*.",
        "Without branch lock, F and F_m are evaluated away from the double zero and linear leakage returns.",
        "PARENT_LOCK_UNSIGNED",
    ),
    (
        "DZT4300_4_scope_guard",
        "This theorem only targets the Gamma trace vertical channel.",
        "It does not kill D_v K_hat, C_conn, B_boundary, Delta_K or matter/readout couplings.",
        "NO_LOCAL_GR_CLAIM",
    ),
]

RESIDUAL_ORDER_ROWS = [
    (
        "ROR4300_0_linear_before_lock",
        "linear Gamma vertical coefficient before parent lock",
        "C_DvGamma_total := |P_obs nabla(L_cg^-2 F_m D_v m - 2 Gamma_eff D_v ln L_cg)|/a_ref",
        "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW",
        "4299 first coefficient remains live if no zero route is signed.",
    ),
    (
        "ROR4300_1_second_order_after_double_zero",
        "second-order Gamma residual after double-zero lock",
        "If m=m_*+delta_m and F=1/2 F_2 delta_m^2+O(delta_m^3), then D_v Gamma_eff=L_cg^-2 F_2 delta_m D_v delta_m - L_cg^-2 F_2 delta_m^2 D_v ln L_cg + O(delta_m^2D_vdelta_m,delta_m^3D_vlnL).",
        "DERIVED_CONDITIONAL_ORDER_REDUCTION",
        "The first Gamma source row is demoted from linear to quadratic only after parent lock is signed.",
    ),
    (
        "ROR4300_2_second_order_bound_template",
        "quadratic fallback bound",
        "C_DvGamma_quad <= ||P_obs nabla[L_cg^-2 F_2 delta_m D_v delta_m - L_cg^-2 F_2 delta_m^2 D_v ln L_cg]||/a_ref",
        "MISSING_DELTA_M_AND_F2_SOURCE_ROWS",
        "Next empirical fallback needs delta_m, D_v delta_m, D_v ln L_cg, F_2, L_cg, P_obs and a_ref.",
    ),
    (
        "ROR4300_3_no_cancellation_credit",
        "no cancellation between m and Lcg legs",
        "Use absolute/component bounds unless parent identity forces cancellation.",
        "GUARDRAIL_ACTIVE",
        "Prevents fitting the two legs against each other to dodge WEP.",
    ),
]

SOURCE_COEFFICIENT_ROWS = [
    (
        "SC4300_0_C_DvGamma_linear",
        "C4299_DVGAMMA_TOTAL",
        "linear pre-lock source coefficient",
        "BLOCKED_UNLESS_ZERO_ROUTE_FAILS_AND_NUMERIC_SOURCE_EXISTS",
        "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW",
    ),
    (
        "SC4300_1_C_DvGamma_quad",
        "C4300_DVGAMMA_QUAD",
        "post-double-zero quadratic source coefficient",
        "PREFERRED_FALLBACK_IF_PARENT_LOCK_SIGNED_BUT_RESIDUAL_DELTA_M_SURVIVES",
        "MISSING_DELTA_M_F2_VERTICAL_PROFILE_ROWS",
    ),
    (
        "SC4300_2_C_m_qbasic",
        "C4300_DVM_QBASIC_DEFECT",
        "defect if m is not q-basic",
        "OPTIONAL_DIAGNOSTIC_IF_DOUBLE_ZERO_NOT_SIGNED",
        "MISSING_D_v_m_SOURCE_ROW",
    ),
    (
        "SC4300_3_C_Lcg_qbasic",
        "C4300_DVLNLCG_QBASIC_DEFECT",
        "defect if L_cg is not q-basic",
        "OPTIONAL_DIAGNOSTIC_IF_DOUBLE_ZERO_NOT_SIGNED",
        "MISSING_D_v_ln_Lcg_SOURCE_ROW",
    ),
]


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
            writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_line(values: List[str]) -> str:
    handle = io.StringIO()
    writer = csv.writer(handle, lineterminator="")
    writer.writerow(values)
    return handle.getvalue()


def to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def append_unique_block(path: Path, marker: str, heading: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    block = f"\n\n## {heading}\n\nMarker: `{marker}`\n\n{body}\n"
    write_text(path, text.rstrip() + block)


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if any(line.startswith(f"{CLAIM_ID},") for line in text.splitlines()):
        return
    row = csv_line(
        [
            CLAIM_ID,
            "local_gr",
            (
                "4300 derives the exact vertical double-zero route for the Gamma trace channel. From "
                "Gamma_eff=L_cg^-2F(m), D_v Gamma_eff=L_cg^-2F_mD_v m-2 Gamma_eff D_v ln L_cg. Therefore if the parent "
                "local branch locks m=m_* with F(m_*)=0 and F_m(m_*)=0, D_v Gamma_eff=0 even when D_v m and D_v ln L_cg "
                "are not individually zero. This demotes the first Gamma leakage from linear to quadratic residual order, "
                "but only conditionally because the parent double-zero lock remains unsigned."
            ),
            (
                "4300 source register, zero route map, double-zero vertical theorem, residual order reduction, source "
                "coefficient status, 4293 gate map, decision, firewall, status, next-target and validation CSV."
            ),
            "private_vertical_double_zero_gamma_channel_conditional_nonclaim",
            (
                "Derive the parent double-zero lock m=m_* with F=F_m=0, or fill the second-order D_v Gamma residual rows "
                "with sourced delta_m/F_2/vertical-profile inputs."
            ),
            (
                "Claiming local GR/PPN/WEP/R10 pass, treating the double zero as already parent-owned, cancelling m and Lcg "
                "legs by tuning, or erasing Khat/connection/boundary residuals."
            ),
        ]
    )
    path.write_text(text.rstrip() + "\n" + row + "\n", encoding="utf-8")


def requirement_rows() -> List[Dict[str, str]]:
    return csv_rows(SOURCE_DIR / "P8_Y5_R2FR_4293_REQUIRED_SUPPRESSION_ROWS.csv")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(needle in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def zero_route_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for route_id, route, conditions, effect, caveat, status in ZERO_ROUTES:
        rows.append(
            {
                **common(),
                "route_id": route_id,
                "route": route,
                "conditions": conditions,
                "effect_on_DvGamma": effect,
                "caveat": caveat,
                "status": status,
                "fires_now": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def double_zero_theorem_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for theorem_id, premise, derivation, status in DOUBLE_ZERO_THEOREM:
        rows.append(
            {
                **common(),
                "theorem_id": theorem_id,
                "premise_or_step": premise,
                "derivation_or_result": derivation,
                "status": status,
                "conditional_theorem": "True" if "CONDITIONAL" in status or status == "REAL_ALGEBRAIC_PROGRESS" else "False",
                "parent_signed": "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def residual_order_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for residual_id, name, formula, status, interpretation in RESIDUAL_ORDER_ROWS:
        rows.append(
            {
                **common(),
                "residual_id": residual_id,
                "name": name,
                "formula_or_bound": formula,
                "status": status,
                "interpretation": interpretation,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def source_coefficient_status_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for coefficient_status_id, coefficient_id, role, activation, status in SOURCE_COEFFICIENT_ROWS:
        rows.append(
            {
                **common(),
                "coefficient_status_id": coefficient_status_id,
                "coefficient_id": coefficient_id,
                "role": role,
                "activation_rule": activation,
                "current_value": "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW",
                "status": status,
                "source_path": "MISSING_SOURCE_PATH",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def coefficient_gate_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    coefficient_ids = ["C4300_DVGAMMA_QUAD", "C4300_DVM_QBASIC_DEFECT", "C4300_DVLNLCG_QBASIC_DEFECT"]
    for coefficient_id in coefficient_ids:
        for requirement in requirement_rows():
            required_value = requirement.get("required_value", "MISSING_REQUIRED_VALUE")
            required_numeric = to_float(required_value)
            rows.append(
                {
                    **common(),
                    "gate_id": f"G4300_{len(rows):03d}",
                    "coefficient_id": coefficient_id,
                    "arena_requirement": requirement.get("requirement_id", ""),
                    "arena": requirement.get("arena", ""),
                    "observable": requirement.get("observable", ""),
                    "required_value": required_value,
                    "units": requirement.get("units", ""),
                    "coefficient_value": "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW",
                    "required_value_positive_numeric": str(math.isfinite(required_numeric) and required_numeric > 0),
                    "comparison_status": "NOT_RUN_MISSING_COEFFICIENT",
                    "interpretation": "If the double-zero parent lock is signed, score the quadratic residual; otherwise fall back to 4299 linear C_DvGamma rows.",
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4300_0",
            "decision": "PROMOTE_VERTICAL_DOUBLE_ZERO_TO_NEXT_PROOF_TARGET",
            "why": "It kills the D_v Gamma trace channel without assuming m and L_cg are individually q-basic.",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4300_1",
            "decision": "DO_NOT_SCORE_LINEAR_C_DVGAMMA_YET",
            "why": "The proof route may demote the dangerous WEP-facing linear channel to a second-order residual.",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    forbidden = [
        ("FW4300_0", "Do not claim the double-zero theorem fires until parent lock m=m_* is derived."),
        ("FW4300_1", "Do not cancel m and Lcg legs by fitted tuning; only parent identities count."),
        ("FW4300_2", "Do not use Gamma trace silence to erase D_v K_hat, Delta_K, connection, boundary or matter-coupling residuals."),
        ("FW4300_3", "Do not score C4300_DVGAMMA_QUAD without sourced delta_m, F_2, L_cg, vertical profile, projection and a_ref rows."),
        ("FW4300_4", "Do not claim WEP, PPN, R10, clock, orbital, Newton or local-GR pass from 4300."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden_move,
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden_move in forbidden
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STAT4300_0",
            "object": "D_v Gamma_eff",
            "status": "CONDITIONAL_VERTICAL_DOUBLE_ZERO_DERIVED",
            "effect": "Gamma trace linear vertical leakage can vanish without q-basic m/Lcg if F=F_m=0 at a parent-locked local branch.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "status_id": "STAT4300_1",
            "object": "C4299_DVGAMMA_TOTAL",
            "status": "DEMOTABLE_TO_SECOND_ORDER_IF_PARENT_LOCK_SIGNED",
            "effect": "First source coefficient becomes C4300_DVGAMMA_QUAD rather than linear C_DvGamma.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "status_id": "STAT4300_2",
            "object": "parent_double_zero_lock",
            "status": "UNSIGNED_NEXT_TARGET",
            "effect": "Need parent action/Euler/source-lock proof for m=m_* and F=F_m=0.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "status_id": "STAT4300_3",
            "object": "local_precision_claim",
            "status": "BLOCKED_NONCLAIM",
            "effect": "Khat, connection, boundary and matter descent still block local-GR/PPN/WEP/R10 claims.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target_id": "NT4300_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the parent action derive the local branch lock m=m_* with F(m_*)=0 and F_m(m_*)=0, or must we source the second-order D_v Gamma residual?",
            "preferred_route": "derive parent double-zero lock from Euler/stability/vacuum-subtraction, not fixed by fit",
            "fallback_route": "fill C4300_DVGAMMA_QUAD with sourced delta_m, D_v delta_m, D_v ln L_cg, F_2, L_cg, P_obs and a_ref rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def markdown_table(rows: List[Dict[str, str]], columns: List[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _column in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(row.get(column, "").replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def formal_doc() -> str:
    requirements = {row.get("requirement_id", ""): row.get("required_value", "") for row in requirement_rows()}
    return f"""
# 316 PPC4161 DvGamma m/Lcg zero or first coefficient source row

Marker: `{MARKER}`

## Decision

`{DECISION}`

4300 takes the 4299 split seriously and tries to derive a zero, not merely list missing inputs.

## Exact identity

From:

```text
Gamma_eff = L_cg^-2 F(m),
```

we have:

```text
D_v Gamma_eff = L_cg^-2 F_m D_v m - 2 Gamma_eff D_v ln L_cg.
```

## Route map

{markdown_table(zero_route_rows(), ["route_id", "route", "conditions", "effect_on_DvGamma", "status"])}

## Vertical double-zero theorem

The important move is:

```text
if m=m_* and F(m_*)=0 and F_m(m_*)=0,
then D_v Gamma_eff|_* = 0
```

for finite `L_cg`, `D_v m`, and `D_v ln L_cg`. This is stronger than asking first for `D_v m=0` and `D_v ln L_cg=0`, because the coefficients multiplying those variations vanish.

{markdown_table(double_zero_theorem_rows(), ["theorem_id", "premise_or_step", "status", "parent_signed"])}

## Residual order reduction

{markdown_table(residual_order_rows(), ["residual_id", "name", "status", "interpretation"])}

## Source coefficient status

{markdown_table(source_coefficient_status_rows(), ["coefficient_status_id", "coefficient_id", "role", "status"])}

## 4293 pressure

The WEP-facing threshold is still brutal:

```text
Y_WEP <= {requirements.get("REQ4293_WEP", "MISSING")}
```

So the point of 4300 is not to score a pass. It is to avoid needing an absurdly tiny linear `C_DvGamma_total` if the parent can instead prove the double-zero lock and leave only a quadratic residual.

## Result

This is a genuine narrowing:

```text
Before 4300: prove D_v m=0 and D_v ln L_cg=0, or source a linear coefficient.
After 4300: prove parent double-zero lock F=F_m=0; then Gamma trace leakage is second order.
```

Next target: `{NEXT_TARGET}`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4300 Y5 R2FR DvGamma m/Lcg zero or first coefficient source row

## Outcome

The exact vertical double-zero theorem is derived conditionally:

```text
D_v Gamma_eff = L_cg^-2 F_m D_v m - 2 Gamma_eff D_v ln L_cg.
```

If the parent local branch locks to `m=m_*` with:

```text
F(m_*)=0,
F_m(m_*)=0,
```

then `D_v Gamma_eff=0` without needing `D_v m=0` or `D_v ln L_cg=0` separately.

## Nonclaim guard

The parent lock is not signed yet, and this only kills the Gamma trace vertical channel. `D_v K_hat`, `Delta_K`, connection, boundary and matter/readout residuals remain live.

## Next

Derive the parent double-zero lock or source the second-order `C4300_DVGAMMA_QUAD` residual.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    zero_routes = csv_rows(paths["zero_routes"])
    theorem = csv_rows(paths["double_zero_theorem"])
    residual_order = csv_rows(paths["residual_order"])
    coefficient_status = csv_rows(paths["source_coefficient_status"])
    gates = csv_rows(paths["coefficient_to_4293_gate"])
    no_claim_rows = True
    for key, path in paths.items():
        if key == "validation":
            continue
        for row in csv_rows(path):
            if row.get("claim_allowed") == "True" or row.get("valid_for_claim") == "True":
                no_claim_rows = False
    validations = [
        ("VAL4300_0_sources_exist", bool(sources) and all(row["exists"] == "True" for row in sources), "all cited local sources exist"),
        ("VAL4300_1_needles_found", bool(sources) and all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4300_2_double_zero_route_present",
            any(row["route_id"] == "ZR4300_2_vertical_double_zero" and row["status"] == "EXACT_CONDITIONAL_THEOREM_PARENT_LOCK_UNSIGNED" for row in zero_routes),
            "vertical double-zero route is recorded as exact conditional theorem, parent unsigned",
        ),
        (
            "VAL4300_3_theorem_steps",
            any(row["theorem_id"] == "DZT4300_1_double_zero_insert" and row["status"] == "EXACT_CONDITIONAL_ZERO" for row in theorem)
            and any(row["theorem_id"] == "DZT4300_3_parent_lock_required" and row["status"] == "PARENT_LOCK_UNSIGNED" for row in theorem),
            "the theorem has both exact zero step and parent-lock blocker",
        ),
        (
            "VAL4300_4_order_reduction",
            any(row["residual_id"] == "ROR4300_1_second_order_after_double_zero" and row["status"] == "DERIVED_CONDITIONAL_ORDER_REDUCTION" for row in residual_order)
            and any(row["residual_id"] == "ROR4300_2_second_order_bound_template" and row["status"] == "MISSING_DELTA_M_AND_F2_SOURCE_ROWS" for row in residual_order),
            "linear Gamma residual is demoted to second-order only conditionally",
        ),
        (
            "VAL4300_5_coefficient_status",
            any(row["coefficient_id"] == "C4300_DVGAMMA_QUAD" and row["status"] == "MISSING_DELTA_M_F2_VERTICAL_PROFILE_ROWS" for row in coefficient_status),
            "quadratic coefficient fallback exists and remains unscored",
        ),
        (
            "VAL4300_6_4293_gate_links",
            bool(gates)
            and any(row["coefficient_id"] == "C4300_DVGAMMA_QUAD" and row["arena_requirement"] == "REQ4293_WEP" for row in gates)
            and all(row["comparison_status"] == "NOT_RUN_MISSING_COEFFICIENT" for row in gates),
            "quadratic and defect coefficients are linked to 4293 gates but not scored",
        ),
        (
            "VAL4300_7_required_values_positive",
            bool(gates) and all(row["required_value_positive_numeric"] == "True" for row in gates),
            "all imported 4293 required values are positive numeric",
        ),
        ("VAL4300_8_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal document exists with marker"),
        ("VAL4300_9_checkpoint_doc", DOC_PATH.exists() and CHECKPOINT in read_text(DOC_PATH), "post-checkpoint document exists"),
        (
            "VAL4300_10_claim_row",
            any(line.startswith(f"{CLAIM_ID},") for line in read_text(FORMAL / "02-claims-register.csv").splitlines()),
            "claims register contains L-141 private nonclaim row",
        ),
        (
            "VAL4300_11_spine_packet",
            MARKER in read_text(FORMAL / "07-unification-spine.md")
            and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"),
            "spine and packet markers exist",
        ),
        ("VAL4300_12_no_claim_rows", no_claim_rows, "all generated rows remain nonclaim rows"),
    ]
    for name, path in paths.items():
        if name == "validation":
            continue
        validations.append((f"VAL4300_csv_{name}", bool(csv_rows(path)), f"{path.name} parses with rows"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4300_SOURCE_REGISTER.csv",
        "zero_routes": SOURCE_DIR / "P8_Y5_R2FR_4300_DVGAMMA_ZERO_ROUTE_MAP.csv",
        "double_zero_theorem": SOURCE_DIR / "P8_Y5_R2FR_4300_VERTICAL_DOUBLE_ZERO_THEOREM.csv",
        "residual_order": SOURCE_DIR / "P8_Y5_R2FR_4300_RESIDUAL_ORDER_REDUCTION.csv",
        "source_coefficient_status": SOURCE_DIR / "P8_Y5_R2FR_4300_SOURCE_COEFFICIENT_STATUS.csv",
        "coefficient_to_4293_gate": SOURCE_DIR / "P8_Y5_R2FR_4300_COEFFICIENT_TO_4293_GATE.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4300_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4300_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4300_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4300_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["zero_routes"], zero_route_rows())
    write_csv(paths["double_zero_theorem"], double_zero_theorem_rows())
    write_csv(paths["residual_order"], residual_order_rows())
    write_csv(paths["source_coefficient_status"], source_coefficient_status_rows())
    write_csv(paths["coefficient_to_4293_gate"], coefficient_gate_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()
    append_unique_block(
        FORMAL / "07-unification-spine.md",
        MARKER,
        "PPC4161 4300 DvGamma m/Lcg zero or first coefficient",
        (
            "4300 derives the conditional vertical double-zero theorem for the Gamma trace channel: from "
            "`D_v Gamma_eff=L_cg^-2 F_m D_v m-2 Gamma_eff D_v ln L_cg`, a parent-locked branch with "
            "`F(m_*)=F_m(m_*)=0` gives `D_v Gamma_eff=0` even if `m` and `L_cg` are not separately q-basic. "
            "The live burden shifts to deriving the parent double-zero lock or bounding the quadratic residual."
        ),
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4300 packet vertical double-zero Gamma route",
        (
            "Packet update: the dangerous Gamma trace leakage no longer has to start as a linear source coefficient if the "
            "parent can prove the double-zero local lock. This does not touch Khat, connection, boundary or matter descent."
        ),
    )
    write_csv(paths["validation"], validation_rows(paths))
    failed = [row for row in csv_rows(paths["validation"]) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths) - 1} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(paths['validation']))} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
