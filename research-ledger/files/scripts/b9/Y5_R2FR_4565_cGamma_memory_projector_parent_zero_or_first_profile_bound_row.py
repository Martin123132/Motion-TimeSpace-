from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4565"
CLAIM_ID = "L-407"
BRANCH_ID = "MTS_R2FR_Y5_CGAMMA_PROJECTOR_PROFILE_BOUND_4565"
MARKER = "PPC4161_CGAMMA_MEMORY_PROJECTOR_PARENT_ZERO_OR_FIRST_PROFILE_BOUND_ROW_4565"
PACKET_MARKER = "PPC4161_PACKET_CGAMMA_PROJECTOR_PROFILE_BOUND_4565"
DECISION = "CGAMMA_PARENT_ZERO_NOT_CLOSED_FIRST_GDOT_PROFILE_PRODUCT_BOUND_ROW_PROMOTED_NONCLAIM"
NEXT_TARGET = "4566-Y5-R2FR-DtXi0-memory-stationarity-zero-or-cGamma-normalization-source-row.md"

FORMAL_PATH = FORMAL / "581-PPC4161-cGamma-memory-projector-parent-zero-or-first-profile-bound-row.md"
DOC_PATH = POST / "4565-Y5-R2FR-cGamma-memory-projector-parent-zero-or-first-profile-bound-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4564 = FORMAL / "580-PPC4161-cD-deltaKappa-cGamma-root-ownership-zero-law-or-bound-interface.md"
CSV_4564_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4564_NEXT_TARGET.csv"
POST_4187 = POST / "4187-Y5-R2FR-local-memory-support-projector-zero-law-for-cGamma-or-PPN-clock-bound.md"
CSV_4187_PROJECTOR = SOURCE_DIR / "P8_Y5_R2FR_4187_MEMORY_SUPPORT_PROJECTOR_CONTRACT.csv"
CSV_4187_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4187_CGAMMA_ZERO_ROUTE_AUDIT.csv"
CSV_4188_PRODUCT_LAW = SOURCE_DIR / "P8_Y5_R2FR_4188_CGAMMA_PRODUCT_LAW.csv"
CSV_4188_STRICTEST = SOURCE_DIR / "P8_Y5_R2FR_4188_STRICTEST_PRODUCT_BOUNDS.csv"
CSV_4189_GRAMMAR = SOURCE_DIR / "P8_Y5_R2FR_4189_PROJECTION_GRAMMAR.csv"
CSV_4189_FILL = SOURCE_DIR / "P8_Y5_R2FR_4189_FIRST_COEFFICIENT_FILL.csv"
CSV_4194_BUDGETS = SOURCE_DIR / "P8_Y5_R2FR_4194_NORMALIZED_BUDGET_REQUIREMENTS.csv"
CSV_4235_PROFILE = SOURCE_DIR / "P8_Y5_R2FR_4235_CGAMMA_FULL_BUDGET_PROFILE_TABLE.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4565_SOURCE_REGISTER.csv"
ZERO_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4565_PARENT_ZERO_ATTEMPT_AUDIT.csv"
PROFILE_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4565_FIRST_PROFILE_PRODUCT_BOUND_ROW.csv"
PROFILE_REQUIREMENTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4565_PROFILE_BOUND_REQUIREMENTS.csv"
NEXT_PROOF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4565_NEXT_PROOF_TARGETS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4565_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4565_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4565_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4565_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4565_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC4565_00_4564_formal", "4564 selected cGamma", DOC_4564, "c_Gamma is not zero from same-coframe or source-coupling laws."),
        ("SRC4565_01_4564_next", "4564 next target CSV", CSV_4564_NEXT, "4565-Y5-R2FR-cGamma-memory-projector-parent-zero-or-first-profile-bound-row.md"),
        ("SRC4565_02_4187_doc", "4187 projector zero route", POST_4187, "requires vertical silence, compact support silence"),
        ("SRC4565_03_4187_projector", "4187 memory support projector", CSV_4187_PROJECTOR, "SP4187_2_exact_zero"),
        ("SRC4565_04_4187_audit", "4187 zero route audit", CSV_4187_AUDIT, "ZR4187_3_positive_no_hair"),
        ("SRC4565_05_4188_product_law", "4188 cGamma product law", CSV_4188_PRODUCT_LAW, "LAW4188_1_linear_bound"),
        ("SRC4565_06_4188_strictest", "4188 strictest product bounds", CSV_4188_STRICTEST, "C_Gamma_Gdot"),
        ("SRC4565_07_4189_grammar", "4189 projection grammar", CSV_4189_GRAMMAR, "C_Gamma_Gdot = c_Gamma D_t Xi_0"),
        ("SRC4565_08_4189_fill", "4189 first coefficient fill", CSV_4189_FILL, "FCF4189_0_CGamma_Gdot"),
        ("SRC4565_09_4194_budget", "4194 normalized budget", CSV_4194_BUDGETS, "NB4194_strong_local_Gdot"),
        ("SRC4565_10_4235_profile", "4235 full cGamma profile table", CSV_4235_PROFILE, "CGFB4235_B4173_10_Gdot"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in specs:
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": b(path.exists()),
                "needle": needle,
                "needle_found": b(needle in text),
                "role": "4565 cGamma parent-zero attempt and first profile/product bound",
                "valid_for_claim": "False",
            }
        )
    return rows


def zero_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "ZA4565_0_exact_projector",
            "parent_zero_clause": "exact local memory projector",
            "required_statement": "E_Gamma^loc := P_loc(delta S_Gamma / delta O_loc) = 0",
            "current_evidence": "4187/4564 write the projector and exact zero contract.",
            "verdict": "CONTRACT_WRITTEN_NOT_PARENT_CLOSED",
            "missing_input": "parent-owned Gamma_mem equation and proof every projected term vanishes",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "ZA4565_1_parent_operator",
            "parent_zero_clause": "positive/no-hair memory equation",
            "required_statement": "L_Gamma Gamma_mem = J_Gamma with positive/coercive L_Gamma, zero ordinary compact J_Gamma and routed boundary data",
            "current_evidence": "4188 support/no-hair sweep says parent operator/sign/source/boundary data are not found.",
            "verdict": "FAIL_PARENT_OPERATOR_UNSIGNED",
            "missing_input": "L_Gamma, sign/coercivity, source term, domain and boundary data",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "ZA4565_2_vertical_split",
            "parent_zero_clause": "vertical/readout silence",
            "required_statement": "Gamma_mem = Gamma_vert + Gamma_hor with Dq Gamma_vert=0 and P_loc Gamma_hor=0 or bounded",
            "current_evidence": "Known local readouts are vertical-silent, but Gamma_mem itself is not proven vertical.",
            "verdict": "PARTIAL_NOT_CLOSED",
            "missing_input": "proof Gamma_hor absent or a finite horizontal-profile row",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "ZA4565_3_support_source",
            "parent_zero_clause": "compact support and ordinary source silence",
            "required_statement": "P_loc Gamma_mem=0 and J_Gamma_bulk=0 for ordinary compact matter in the local collar",
            "current_evidence": "Same-coframe/Hilbert source descent closes source coupling drift, not memory excitation by I_local.",
            "verdict": "FAIL_SUPPORT_SOURCE_UNSIGNED",
            "missing_input": "support separation/screening law and J_Gamma_bulk=0 from parent variation",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "ZA4565_4_boundary_tensor",
            "parent_zero_clause": "boundary routing and homogeneous tensor no-hair",
            "required_statement": "F_Gamma is boundary/Hamiltonian only with no compact side flux, and Gamma_perp/K_perp has no surviving local projection",
            "current_evidence": "Boundary routing templates exist, but Gamma-specific no-flux and tensor no-hair are not parent-signed.",
            "verdict": "FAIL_BOUNDARY_TENSOR_UNSIGNED",
            "missing_input": "Gamma boundary charge owner plus tensor no-hair or finite tensor profile bound",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "ZA4565_5_decision",
            "parent_zero_clause": "c_Gamma parent zero",
            "required_statement": "All zero clauses pass together without cancellation",
            "current_evidence": "At least four parent clauses remain unsigned.",
            "verdict": "CGAMMA_PARENT_ZERO_FALSE_CURRENTLY",
            "missing_input": "use profile/product bound branch now",
            "valid_for_claim": "False",
        },
    ]


def profile_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "profile_bound_id": "PB4565_0_Gdot_time_profile",
            "selected_first": "True",
            "coefficient": "c_Gamma",
            "effective_product": "C_Gamma_Gdot",
            "profile_variable": "D_t Xi_0",
            "arena": "clock_orbital_Gdot",
            "observable": "Gdot_over_G",
            "product_law": "C_Gamma_Gdot = c_Gamma * D_t Xi_0",
            "source_backed_product_bound": "2.42e-14",
            "units": "yr^-1",
            "profile_bound_if_cGamma_known": "|D_t Xi_0| <= 2.42e-14/|c_Gamma| yr^-1",
            "source_bound_id": "B4173_10_Gdot",
            "source_id": "SRC4173_WEB_05_LLR_Gdot",
            "why_selected": "clean physical profile units and direct memory-stationarity meaning; it does not require transferring a vector/tensor PPN projection first",
            "standalone_cGamma_bound": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def profile_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement_id": "PR4565_0_cGamma_normalization",
            "needed_for": "standalone profile/coupling separation",
            "requirement": "parent normalization and natural-size/sign convention for c_Gamma",
            "current_status": "MISSING_PARENT_NORMALIZATION",
            "effect_if_missing": "only product bound C_Gamma_Gdot is claimable as nonclaim evidence; no standalone c_Gamma or D_t Xi_0 bound",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "PR4565_1_projection_jacobian",
            "needed_for": "non-unit runner",
            "requirement": "J_Gdot^Gamma mapping P_loc Gamma_mem profile into measured Gdot/G",
            "current_status": "UNIT_NORMALIZED_PLACEHOLDER_ONLY",
            "effect_if_missing": "bound remains |c_Gamma*D_t Xi_0| <= B, not a score-ready prediction",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "PR4565_2_stationarity_zero",
            "needed_for": "derivation branch",
            "requirement": "D_t Xi_0=0 from memory stationarity/no-hair on the compact local collar",
            "current_status": "OPEN_NEXT_DERIVATION",
            "effect_if_missing": "Gdot product row remains active",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "PR4565_3_no_cancellation",
            "needed_for": "arena comparison",
            "requirement": "channelwise comparison; no cancellation with delta_kappa, c_D, PPN vector, boundary or tensor rows",
            "current_status": "GUARD_INSTALLED",
            "effect_if_missing": "local-GR pass could be faked by trading residuals",
            "valid_for_claim": "False",
        },
        {
            "requirement_id": "PR4565_4_source_path_units",
            "needed_for": "usable nonclaim row",
            "requirement": "bound row has source id, observable, arena, numeric bound and units",
            "current_status": "PASS_FOR_PRODUCT_ROW",
            "effect_if_missing": "row would be schema-only",
            "valid_for_claim": "False",
        },
    ]


def next_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NT4565_0_stationarity",
            "target": "derive D_t Xi_0 = 0",
            "route": "memory stationarity / compact-collar no-hair",
            "success_condition": "parent Gamma_mem equation implies local stationary scalar profile in ordinary compact branch",
            "failure_fallback": "keep PB4565_0_Gdot_time_profile as product bound",
            "valid_for_claim": "False",
        },
        {
            "target_id": "NT4565_1_normalization",
            "target": "derive or source c_Gamma normalization",
            "route": "parent action coefficient or canonical field normalization",
            "success_condition": "convert product bound into profile or coefficient bound without unit-rescaling cheat",
            "failure_fallback": "retain product-only row",
            "valid_for_claim": "False",
        },
        {
            "target_id": "NT4565_2_jacobian",
            "target": "replace unit Jacobian",
            "route": "derive J_Gdot^Gamma from local field equations/readout map",
            "success_condition": "|c_Gamma profile| <= B/|J_Gdot^Gamma| with sourced J",
            "failure_fallback": "unit-normalized smoke row remains nonclaim",
            "valid_for_claim": "False",
        },
    ]


def promotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG4565_0_parent_zero",
            "requirement": "all c_Gamma zero clauses parent-signed",
            "status": "FAIL_PARENT_ZERO_OPEN",
            "claim_effect": "c_Gamma=0 not claimed",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4565_1_first_product_bound",
            "requirement": "first c_Gamma profile/product row has observable, arena, source-backed numeric bound and units",
            "status": "PASS_NONCLAIM_PRODUCT_ROW",
            "claim_effect": "usable internal bound row, not a theory pass",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4565_2_standalone_bound",
            "requirement": "standalone c_Gamma or D_t Xi_0 bound",
            "status": "FAIL_MISSING_CGAMMA_NORMALIZATION_OR_PROFILE",
            "claim_effect": "no standalone coefficient/profile claim",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4565_3_public_local_GR",
            "requirement": "local-GR/Newton/PPN/R10/clock pass",
            "status": "FAIL_PUBLIC_CLAIM_BLOCKED",
            "claim_effect": "memory hair remains live unless zero theorem or product row passes with real projection",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PG4565_4_next",
            "requirement": "next work attacks stationarity/normalization rather than relisting c_Gamma",
            "status": "PASS_NEXT_SELECTED",
            "claim_effect": f"next target = {NEXT_TARGET}",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4565_0_main",
            "decision": DECISION,
            "what_was_derived": "The exact parent-zero audit fails cleanly, and the first source-backed product/profile row is promoted: C_Gamma_Gdot = c_Gamma D_t Xi_0 with |C_Gamma_Gdot| <= 2.42e-14 yr^-1.",
            "what_failed": "No parent-owned Gamma_mem operator/sign/source/boundary/tensor no-hair proof exists, so c_Gamma=0 is not claimed.",
            "action_taken": "Keep c_Gamma active but bounded in a concrete nonclaim Gdot product row; next derive D_t Xi_0=0 or c_Gamma normalization/Jacobian.",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "best_forward_route",
            "why": "The first usable c_Gamma row is a time-profile product bound. The least-circular next move is to derive memory stationarity D_t Xi_0=0 or source the c_Gamma/J_Gdot normalization needed to split the product.",
            "success_condition": "Either prove D_t Xi_0=0 from parent memory stationarity/no-hair, or produce c_Gamma and J_Gdot^Gamma normalization rows that convert the product bound without unit laundering.",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "decision": DECISION,
            "c_Gamma_parent_zero": "False",
            "first_profile_product_bound_written": "True",
            "selected_product": "C_Gamma_Gdot",
            "selected_bound": "2.42e-14 yr^-1",
            "standalone_cGamma_bound": "False",
            "public_local_GR_claim_allowed": "False",
            "next_target": NEXT_TARGET,
            "timestamp_utc": utc_now(),
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    zero_audit: list[dict[str, Any]],
    profile_bound: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    next_proof: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    rows.append({"validation_id": "VAL4565_0_sources", "check": "all source paths and needles validate", "status": "PASS" if source_ok else "FAIL", "details": f"{len(sources)} sources"})

    audit_text = "\n".join(str(value) for row in zero_audit for value in row.values())
    audit_ok = all(token in audit_text for token in ["FAIL_PARENT_OPERATOR_UNSIGNED", "FAIL_SUPPORT_SOURCE_UNSIGNED", "CGAMMA_PARENT_ZERO_FALSE_CURRENTLY"])
    audit_ok = audit_ok and all(row["valid_for_claim"] == "False" for row in zero_audit)
    rows.append({"validation_id": "VAL4565_1_zero_audit", "check": "parent zero audit fails explicitly rather than silently", "status": "PASS" if audit_ok else "FAIL", "details": f"{len(zero_audit)} audit rows"})

    profile = profile_bound[0] if profile_bound else {}
    profile_ok = (
        profile.get("effective_product") == "C_Gamma_Gdot"
        and profile.get("source_backed_product_bound") == "2.42e-14"
        and profile.get("units") == "yr^-1"
        and profile.get("standalone_cGamma_bound") == "False"
        and profile.get("valid_for_claim") == "False"
    )
    rows.append({"validation_id": "VAL4565_2_profile_bound", "check": "first profile product bound is numeric, unitful, sourced and nonclaim", "status": "PASS" if profile_ok else "FAIL", "details": profile.get("profile_bound_if_cGamma_known", "missing")})

    req_text = "\n".join(str(value) for row in requirements for value in row.values())
    req_ok = all(token in req_text for token in ["MISSING_PARENT_NORMALIZATION", "UNIT_NORMALIZED_PLACEHOLDER_ONLY", "OPEN_NEXT_DERIVATION", "PASS_FOR_PRODUCT_ROW"])
    rows.append({"validation_id": "VAL4565_3_requirements", "check": "requirements distinguish product row from standalone cGamma/profile claim", "status": "PASS" if req_ok else "FAIL", "details": f"{len(requirements)} requirements"})

    next_text = "\n".join(str(value) for row in next_proof for value in row.values())
    next_ok = all(token in next_text for token in ["D_t Xi_0 = 0", "c_Gamma normalization", "J_Gdot^Gamma"])
    rows.append({"validation_id": "VAL4565_4_next_proof", "check": "next proof targets attack stationarity, normalization and Jacobian", "status": "PASS" if next_ok else "FAIL", "details": f"{len(next_proof)} next proof rows"})

    gates_text = "\n".join(str(value) for row in gates for value in row.values())
    gates_ok = all(token in gates_text for token in ["FAIL_PARENT_ZERO_OPEN", "PASS_NONCLAIM_PRODUCT_ROW", "FAIL_MISSING_CGAMMA_NORMALIZATION_OR_PROFILE", "FAIL_PUBLIC_CLAIM_BLOCKED"])
    gates_ok = gates_ok and all(row["valid_for_claim"] == "False" for row in gates)
    rows.append({"validation_id": "VAL4565_5_gates", "check": "promotion gates permit product row but block claims", "status": "PASS" if gates_ok else "FAIL", "details": f"{len(gates)} gates"})

    decision_ok = decision and decision[0]["decision"] == DECISION and decision[0]["valid_for_claim"] == "False"
    status_ok = status and status[0]["c_Gamma_parent_zero"] == "False" and status[0]["first_profile_product_bound_written"] == "True"
    next_ok2 = next_target and next_target[0]["next_target"] == NEXT_TARGET
    rows.append({"validation_id": "VAL4565_6_decision_status", "check": "decision/status select stationarity or normalization next", "status": "PASS" if decision_ok and status_ok and next_ok2 else "FAIL", "details": NEXT_TARGET})

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"validation_id": "VAL4565_7_overall", "check": "overall 4565 checkpoint validation", "status": "PASS" if overall else "FAIL", "details": "cGamma zero failed; first Gdot product/profile row written" if overall else "one or more validations failed"})
    return rows


def write_doc(
    path: Path,
    title: str,
    sources: list[dict[str, Any]],
    zero_audit: list[dict[str, Any]],
    profile_bound: list[dict[str, Any]],
    requirements: list[dict[str, Any]],
    next_proof: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# {title}

Branch: `{BRANCH_ID}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4565 tries the derivation route first. The exact target is:

```text
E_Gamma^loc := P_loc(delta S_Gamma / delta O_loc) = 0.
```

That parent-zero route still fails because the corpus does not yet supply the parent memory equation:

```text
L_Gamma Gamma_mem = J_Gamma
```

with sign/coercivity, ordinary-source silence, compact support/boundary data and homogeneous tensor no-hair.

So the checkpoint does the honest fallback: it promotes the first usable source-backed profile/product row:

```text
C_Gamma_Gdot = c_Gamma D_t Xi_0,
|C_Gamma_Gdot| <= 2.42e-14 yr^-1.
```

Equivalently, only if `c_Gamma` is later normalized:

```text
|D_t Xi_0| <= 2.42e-14 / |c_Gamma| yr^-1.
```

This is **not** a standalone `c_Gamma` bound and not a local-GR claim. It is the first clean unitful cGamma profile/product pressure row.

## Source Register

{markdown_table(sources)}

## Parent Zero Attempt Audit

{markdown_table(zero_audit)}

## First Profile Product Bound Row

{markdown_table(profile_bound)}

## Profile Bound Requirements

{markdown_table(requirements)}

## Next Proof Targets

{markdown_table(next_proof)}

## Promotion Gates

{markdown_table(gates)}

## Decision

{markdown_table(decision)}

## Next Target

{markdown_table(next_target)}

## Validation

{markdown_table(validation)}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH)
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4565 fails the c_Gamma parent-zero proof honestly and promotes the first source-backed Gdot profile/product bound row: C_Gamma_Gdot=c_Gamma D_t Xi_0 with |C_Gamma_Gdot|<=2.42e-14 yr^-1.",
        "current_evidence": "Generated source register, parent-zero audit, first profile/product bound row, requirements ledger, next proof targets, promotion gates, status and validation CSVs.",
        "status": "cGamma_parent_zero_failed_first_Gdot_product_bound_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating a product bound as a standalone c_Gamma or profile bound before normalization/Jacobian are supplied.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/PPN/clock/orbital/R10 claim; product row only.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    zero_audit = zero_audit_rows()
    profile_bound = profile_bound_rows()
    requirements = profile_requirement_rows()
    next_proof = next_proof_rows()
    gates = promotion_rows()
    decision = decision_rows()
    next_target = next_rows()
    status = status_rows()
    validation = validate(sources, zero_audit, profile_bound, requirements, next_proof, gates, decision, next_target, status)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_AUDIT_CSV, zero_audit)
    write_csv(PROFILE_BOUND_CSV, profile_bound)
    write_csv(PROFILE_REQUIREMENTS_CSV, requirements)
    write_csv(NEXT_PROOF_CSV, next_proof)
    write_csv(PROMOTION_CSV, gates)
    write_csv(DECISION_CSV, decision)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)
    write_csv(VALIDATION_PATH, validation)

    write_doc(FORMAL_PATH, "4565 - cGamma memory projector parent zero or first profile bound row", sources, zero_audit, profile_bound, requirements, next_proof, gates, decision, next_target, validation)
    write_doc(DOC_PATH, "4565 - Y5 R2FR cGamma Memory Projector Parent Zero Or First Profile Bound Row", sources, zero_audit, profile_bound, requirements, next_proof, gates, decision, next_target, validation)
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4565 cGamma Memory Projector Or First Profile Bound

Marker: `{MARKER}`  
The cGamma parent-zero route was attempted first and is not closed. The missing parent object is still a signed memory equation `L_Gamma Gamma_mem = J_Gamma` with positivity, compact support/source silence, routed boundary data and tensor no-hair.

The first usable cGamma profile/product pressure row is now:

```text
C_Gamma_Gdot = c_Gamma D_t Xi_0,
|C_Gamma_Gdot| <= 2.42e-14 yr^-1.
```

If `c_Gamma` is later normalized, this becomes `|D_t Xi_0| <= 2.42e-14/|c_Gamma| yr^-1`. Until then it is a source-backed product bound only, not a standalone coefficient/profile claim. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4565 Packet Integration - cGamma Projector/Profile Bound

Marker: `{PACKET_MARKER}`  
The packet keeps `c_Gamma_parent_zero=false`. The active cGamma row is the source-backed Gdot product bound `C_Gamma_Gdot=c_Gamma D_t Xi_0`, `|C_Gamma_Gdot|<=2.42e-14 yr^-1`; it is nonclaim until memory stationarity, cGamma normalization and `J_Gdot^Gamma` are supplied. Next target: `{NEXT_TARGET}`.
""",
    )

    cache_dir = Path(__file__).resolve().parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {FORMAL_PATH}")
    print(f"Wrote {VALIDATION_PATH}")
    print(f"Decision: {DECISION}")


if __name__ == "__main__":
    main()
