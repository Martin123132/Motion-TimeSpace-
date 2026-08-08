from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3703"
BRANCH_ID = "MTS_R2FR_Y5_MTS_RHO_NEWTON_Z2BOUND_MUH_NUMERIC_OR_SYMBOLIC_BOUND_3703"
DOC = ROOT / "3703-Y5-R2FR-MTS-rho-Newton-z2bound-muH-numeric-or-symbolic-bound.md"

R10_CANDIDATE_CURVE = RESIDUALS / "P8_Y5_R2FR_3702_R10_BOUND_CURVE_CANDIDATE.csv"
R10_BINDER_3702 = RESIDUALS / "P8_Y5_R2FR_3702_MTS_ALPHA_LAMBDA_BINDER_ROWS.csv"
ARENA_3700 = RESIDUALS / "P8_Y5_R2FR_3700_ARENA_RUNNER_ROWS.csv"
TENSOR_3700 = RESIDUALS / "P8_Y5_R2FR_3700_RESIDUAL_TENSOR_ROWS.csv"
RESIDUAL_3699 = RESIDUALS / "P8_Y5_R2FR_3699_RESIDUAL_BOUND_ROWS.csv"

ANCHOR_LAMBDA_M = 38.6e-6


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("curve_3702", R10_CANDIDATE_CURVE, "alpha_bound_abs", "private candidate R10 curve from 3702"),
        ("binder_3702", R10_BINDER_3702, "alpha_eff", "MTS alpha/lambda binder from 3702"),
        ("arena_3700", ARENA_3700, "alpha_eff(lambda_H)", "R10 arena bridge from 3700"),
        ("tensor_3700", TENSOR_3700, "z2_bound", "second-order amplitude and residual tensor definitions"),
        ("residual_3699", RESIDUAL_3699, "R_iAB", "Fisher source-silence residual rows"),
        ("doc_3700", ROOT / "3700-Y5-R2FR-second-order-source-residual-vector-and-local-test-runner.md", "alpha_eff(lambda_H)", "human-readable 3700 derivation"),
        ("doc_3702", ROOT / "3702-Y5-R2FR-R10-bound-curve-digitizer-and-MTS-alpha-lambda-binder.md", "38.6 micrometer", "human-readable 3702 R10 extraction"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                **base(timestamp),
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
            }
        )
    return rows


def derivation_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "DER3703_0_R10_arena",
            "alpha_eff(lambda_H)=K_N * 0.5*rho_Newton*z0^2 + alpha_edge + alpha_proj",
            "3700 R10 arena row",
            "start from the already-derived second-order source-silence bridge",
            "DERIVED_INPUT",
        ),
        (
            "DER3703_1_amplitude",
            "z0^2 <= (C_H ||J_y+B_y||/mu_H^2)^2 + B_edge^2 + B_boundary^2",
            "3700 amplitude row plus local static kernel",
            "replace unsourced z0 by the mass-gap/source amplitude bound",
            "DERIVED_INPUT",
        ),
        (
            "DER3703_2_range",
            "lambda_H = 1/mu_H",
            "3702 lambda binder",
            "turn the mass gap into the R10 force range",
            "DERIVED_INPUT",
        ),
        (
            "DER3703_3_substitution",
            "alpha_eff(lambda_H) <= 0.5*K_N*rho_Newton*C_H^2||J_y+B_y||^2*lambda_H^4 + alpha_nuisance",
            "substitute DER3703_1 and DER3703_2 into DER3703_0",
            "this is the useful compression: R10 sees a lambda^4 source-product plus nuisance leakage",
            "NEW_3703_RESULT",
        ),
        (
            "DER3703_4_parent_product",
            "P_N := K_N*rho_Newton*C_H^2||J_y+B_y||^2",
            "definition",
            "collapses K_N, rho_Newton, source norm, and horizontal Green constant into one parent-owned product with units m^-4",
            "NEW_3703_RESULT",
        ),
        (
            "DER3703_5_nuisance",
            "alpha_nuisance := 0.5*K_N*rho_Newton*(B_edge^2+B_boundary^2) + alpha_edge + alpha_proj",
            "definition",
            "keeps edge/projection/boundary leakage visible instead of hiding it inside P_N",
            "NEW_3703_RESULT",
        ),
        (
            "DER3703_6_R10_gate",
            "0.5*P_N*lambda_H^4 + alpha_nuisance <= alpha_bound_R10(lambda_H)",
            "R10 pass inequality",
            "this is now the exact nonclaim local-Newton gate produced by the 3699-3702 chain",
            "NEW_3703_RESULT",
        ),
        (
            "DER3703_7_product_bound",
            "P_N <= 2*(alpha_bound_R10(lambda_H)-alpha_nuisance)/lambda_H^4",
            "solve DER3703_6 for P_N",
            "if alpha_nuisance is zero or separately bounded, the candidate R10 curve directly bounds the parent source product",
            "NEW_3703_RESULT",
        ),
        (
            "DER3703_8_budget_fraction",
            "if alpha_nuisance <= eta_R10*alpha_bound_R10, then P_N <= 2*(1-eta_R10)*alpha_bound_R10/lambda_H^4",
            "non-tuning budget split",
            "gives a fair future scoring route without pretending nuisance leakage is absent",
            "NEW_3703_RESULT",
        ),
    ]
    return [
        {
            **base(timestamp),
            "derivation_id": derivation_id,
            "formula": formula,
            "source": source,
            "meaning": meaning,
            "status": status,
            "claim_allowed": False,
        }
        for derivation_id, formula, source, meaning, status in specs
    ]


def read_curve_rows() -> list[dict[str, str]]:
    rows = parse_csv(R10_CANDIDATE_CURVE)
    filtered = []
    for row in rows:
        try:
            lambda_m = float(row["lambda_m"])
            alpha_bound = float(row["alpha_bound_abs"])
        except (KeyError, ValueError):
            continue
        if lambda_m > 0 and alpha_bound > 0:
            filtered.append(row)
    return sorted(filtered, key=lambda item: float(item["lambda_m"]))


def product_bound_rows(timestamp: str, curve_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for idx, curve in enumerate(curve_rows):
        lambda_m = float(curve["lambda_m"])
        alpha_bound = float(curve["alpha_bound_abs"])
        p_zero = 2.0 * alpha_bound / lambda_m**4
        p_eta_10 = 2.0 * 0.90 * alpha_bound / lambda_m**4
        p_eta_50 = alpha_bound / lambda_m**4
        mu_h = 1.0 / lambda_m
        rows.append(
            {
                **base(timestamp),
                "bound_row_id": f"PN3703_{idx:03d}",
                "curve_row_id": curve.get("curve_row_id", ""),
                "lambda_m": f"{lambda_m:.12e}",
                "lambda_um": f"{lambda_m * 1e6:.6f}",
                "mu_H_m_inv": f"{mu_h:.12e}",
                "alpha_bound_abs": f"{alpha_bound:.12e}",
                "P_N_max_zero_nuisance_m4": f"{p_zero:.12e}",
                "log10_P_N_max_zero_nuisance": f"{math.log10(p_zero):.9f}",
                "P_N_max_eta10_m4": f"{p_eta_10:.12e}",
                "P_N_max_eta50_m4": f"{p_eta_50:.12e}",
                "formula": "P_N_max(eta)=2*(1-eta_R10)*alpha_bound_R10(lambda_H)/lambda_H^4",
                "source_curve_status": curve.get("confidence", "candidate_manual_review_required"),
                "score_role": "nonclaim candidate curve product-bound row",
                "claim_allowed": False,
            }
        )
    return rows


def anchor_rows(timestamp: str) -> list[dict[str, object]]:
    mu_anchor = 1.0 / ANCHOR_LAMBDA_M
    p_anchor = 2.0 / ANCHOR_LAMBDA_M**4
    return [
        {
            **base(timestamp),
            "anchor_id": "ANCH3703_0_alpha1_range",
            "lambda_anchor_m": f"{ANCHOR_LAMBDA_M:.12e}",
            "lambda_anchor_um": f"{ANCHOR_LAMBDA_M * 1e6:.6f}",
            "mu_H_lower_bound_m_inv_for_alpha1": f"{mu_anchor:.12e}",
            "P_N_max_zero_nuisance_at_anchor_m4": f"{p_anchor:.12e}",
            "log10_P_N_max_zero_nuisance_at_anchor": f"{math.log10(p_anchor):.9f}",
            "statement": "If the branch behaves like gravitational-strength Yukawa alpha_eff~1, R10 demands lambda_H < 38.6 micrometer, equivalently mu_H > 2.59067e4 m^-1.",
            "status": "ANCHOR_ONLY_NONCLAIM",
            "claim_allowed": False,
        }
    ]


def missing_parent_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "MISS3703_0_P_N",
            "P_N",
            "K_N*rho_Newton*C_H^2||J_y+B_y||^2",
            "derive from parent source coupling, Fisher residual tensor, horizontal Green constant, and source norm",
            "single dominant parent source-product now isolated",
        ),
        (
            "MISS3703_1_lambda_H",
            "lambda_H",
            "1/mu_H",
            "derive mu_H from horizontal mass gap, Hessian/Fisher eigenvalue, or source-sector stability operator",
            "R10 cannot choose a range by fit; it must be inherited from the parent branch",
        ),
        (
            "MISS3703_2_alpha_nuisance",
            "alpha_nuisance",
            "0.5*K_N*rho_Newton*(B_edge^2+B_boundary^2)+alpha_edge+alpha_proj",
            "prove zero by boundary/projection theorem or allocate a sourced eta_R10 budget",
            "must remain explicit because nuisance terms can dominate the R10 bound",
        ),
        (
            "MISS3703_3_curve_review",
            "alpha_bound_R10(lambda)",
            "candidate curve from fig5b1",
            "replace by official supplemental table or manually reviewed digitization before claims",
            "current curve is good for private smoke only",
        ),
    ]
    return [
        {
            **base(timestamp),
            "missing_id": missing_id,
            "quantity": quantity,
            "definition": definition,
            "needed_action": needed_action,
            "why_it_matters": why_it_matters,
            "status": "MISSING_PARENT_INPUT_OR_REVIEW",
            "claim_allowed": False,
        }
        for missing_id, quantity, definition, needed_action, why_it_matters in specs
    ]


def smoke_rows(timestamp: str, product_bounds: list[dict[str, object]], anchors: list[dict[str, object]]) -> list[dict[str, object]]:
    min_row = min(product_bounds, key=lambda row: float(row["P_N_max_zero_nuisance_m4"]))
    max_row = max(product_bounds, key=lambda row: float(row["P_N_max_zero_nuisance_m4"]))
    return [
        {
            **base(timestamp),
            "smoke_id": "SMOKE3703_0_product_curve_schema",
            "result": f"derived {len(product_bounds)} P_N bound rows from the 3702 candidate R10 curve",
            "score_ready": True,
            "blocker": "candidate curve remains manual-review-only; MTS P_N/lambda_H/alpha_nuisance are not sourced",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "smoke_id": "SMOKE3703_1_tightest_private_row",
            "result": f"tightest zero-nuisance candidate row is lambda={min_row['lambda_um']} um with log10(P_N_max)={min_row['log10_P_N_max_zero_nuisance']}",
            "score_ready": False,
            "blocker": "cannot score until MTS predicts lambda_H and P_N independently",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "smoke_id": "SMOKE3703_2_largest_private_row",
            "result": f"loosest zero-nuisance candidate row is lambda={max_row['lambda_um']} um with log10(P_N_max)={max_row['log10_P_N_max_zero_nuisance']}",
            "score_ready": False,
            "blocker": "large allowed P_N at short range does not help unless mu_H places the branch there",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "smoke_id": "SMOKE3703_3_anchor_muH",
            "result": anchors[0]["statement"],
            "score_ready": False,
            "blocker": "anchor constrains gravitational-strength alpha_eff only; arbitrary alpha_eff needs full curve and MTS values",
            "claim_allowed": False,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3703_0",
            "R10 missing-input set is reduced to a source-product gate.",
            "The chain now says exactly what must be true: 0.5*P_N*lambda_H^4 + alpha_nuisance must sit below the R10 bound curve.",
            "DERIVATION_ADVANCES",
        ),
        (
            "DEC3703_1",
            "Do not claim R10/local-Newton recovery.",
            "P_N, lambda_H, and alpha_nuisance are still not parent-sourced, and the R10 curve is candidate-only.",
            "CLAIM_BLOCKED",
        ),
        (
            "DEC3703_2",
            "Next attack should be edge/projection/boundary cleanup before chasing more public data.",
            "Without alpha_nuisance=0 or alpha_nuisance <= eta_R10 alpha_bound, no finite P_N result can be trusted.",
            "NEXT_TARGET_SELECTED",
        ),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "status": status,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale, status in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3703_0_curve", "official/reviewed alpha_bound_R10(lambda) curve", "BLOCKED"),
        ("CG3703_1_parent_range", "parent-derived numeric lambda_H=1/mu_H", "BLOCKED"),
        ("CG3703_2_parent_product", "parent-derived numeric or bounded P_N", "BLOCKED"),
        ("CG3703_3_nuisance", "alpha_nuisance proved zero or bounded by sourced eta_R10 budget", "BLOCKED"),
        ("CG3703_4_score", "0.5*P_N*lambda_H^4+alpha_nuisance <= alpha_bound_R10(lambda_H) evaluated", "BLOCKED"),
        ("CG3703_5_public", "public R10/local-Newton claim allowed", "BLOCKED"),
    ]
    return [
        {
            **base(timestamp),
            "claim_gate_id": gate_id,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
        }
        for gate_id, requirement, status in specs
    ]


def status_rows(timestamp: str, product_bounds: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3703_0",
            "status": "R10_MTS_SIDE_COMPRESSED_TO_PARENT_SOURCE_PRODUCT_GATE_NONCLAIM",
            "summary": (
                f"3703 derives alpha_eff(lambda_H) <= 0.5*P_N*lambda_H^4 + alpha_nuisance and converts the 3702 candidate curve into "
                f"{len(product_bounds)} private P_N bound rows. This is a real narrowing step: R10 now asks for parent-sourced P_N, lambda_H, "
                "and alpha_nuisance, not a scattered list of unrelated missing constants."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3703_0",
            "target_doc": "3704-Y5-R2FR-alpha-nuisance-zero-or-budget-boundary-projection-cleanup.md",
            "target_script": "scripts/Y5_R2FR_3704_alpha_nuisance_zero_or_budget_boundary_projection_cleanup.py",
            "objective": "prove alpha_edge/alpha_proj/boundary terms vanish for the local R10 branch, or derive a sourced eta_R10 budget that leaves a finite P_N bound",
            "success_gate": "alpha_nuisance is either parent-zero, bounded as eta_R10*alpha_bound_R10, or the R10 local branch remains explicitly closure-only",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    derivations: list[dict[str, object]],
    product_bounds: list[dict[str, object]],
    anchors: list[dict[str, object]],
    missing: list[dict[str, object]],
    smoke: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    tightest = min(product_bounds, key=lambda row: float(row["P_N_max_zero_nuisance_m4"]))
    lines = [
        "# 3703 Y5 R2FR MTS Rho-Newton Z2bound Muh Numeric Or Symbolic Bound",
        "",
        "Private checkpoint. No GitHub action. No public claim.",
        "",
        "## Status",
        "",
        f"- `{status[0]['status']}`",
        f"- {status[0]['summary']}",
        "",
        "## Main Result",
        "",
        "- This checkpoint stops the R10 branch from being a bag of missing symbols.",
        "- Starting from 3700, `alpha_eff(lambda_H)=K_N * 0.5*rho_Newton*z0^2 + alpha_edge + alpha_proj`.",
        "- Starting from the mass-gap amplitude bound, `z0^2 <= (C_H ||J_y+B_y||/mu_H^2)^2 + B_edge^2 + B_boundary^2`.",
        "- With `lambda_H=1/mu_H`, the R10 prediction compresses to `alpha_eff(lambda_H) <= 0.5*P_N*lambda_H^4 + alpha_nuisance`.",
        "- The parent source product is `P_N := K_N*rho_Newton*C_H^2||J_y+B_y||^2` with units `m^-4`.",
        "- The visible nuisance term is `alpha_nuisance := 0.5*K_N*rho_Newton*(B_edge^2+B_boundary^2)+alpha_edge+alpha_proj`.",
        "- Therefore R10 asks for `0.5*P_N*lambda_H^4 + alpha_nuisance <= alpha_bound_R10(lambda_H)`.",
        "- If nuisance leakage is zero, the private curve gives `P_N <= 2*alpha_bound_R10(lambda_H)/lambda_H^4`.",
        "- If nuisance leakage is budgeted, `alpha_nuisance <= eta_R10*alpha_bound_R10` gives `P_N <= 2*(1-eta_R10)*alpha_bound_R10/lambda_H^4`.",
        "",
        "## Anchor Consequence",
        "",
        f"- `{anchors[0]['anchor_id']}`: {anchors[0]['statement']}",
        f"- At the official alpha=1 anchor, zero-nuisance `P_N_max = {anchors[0]['P_N_max_zero_nuisance_at_anchor_m4']} m^-4`.",
        "",
        "## Product-Bound Curve",
        "",
        f"- Candidate product-bound rows generated: `{len(product_bounds)}`.",
        f"- Tightest zero-nuisance private row: `lambda={tightest['lambda_um']} um`, `log10(P_N_max)={tightest['log10_P_N_max_zero_nuisance']}`.",
        "- All rows remain `valid_for_claim=false` because the bound curve is still candidate/manual-review-only and MTS-side `P_N/lambda_H/alpha_nuisance` are not parent-sourced.",
        "",
        "## Derivation Rows",
        "",
    ]
    for row in derivations:
        lines.append(f"- `{row['derivation_id']}`: `{row['status']}` | {row['formula']} | {row['meaning']}")
    lines.extend(["", "## Missing Parent Inputs", ""])
    for row in missing:
        lines.append(f"- `{row['missing_id']}`: `{row['quantity']}` | {row['definition']} | next: {row['needed_action']}")
    lines.extend(["", "## Smoke Rows", ""])
    for row in smoke:
        lines.append(f"- `{row['smoke_id']}`: score_ready={row['score_ready']} claim=false | {row['result']} | blocker: {row['blocker']}")
    lines.extend(["", "## Decisions", ""])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` | {row['decision']} | {row['rationale']}")
    lines.extend(["", "## Claim Gates", ""])
    for row in claim_gates:
        lines.append(f"- `{row['claim_gate_id']}`: `{row['status']}` | {row['requirement']}")
    lines.extend(["", "## Source Register", ""])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: exists={row['exists']} needle_found={row['needle_found']} path=`{row['path']}`")
    lines.extend(["", "## Next Target", ""])
    lines.append(f"- `{next_target[0]['target_doc']}`")
    lines.append(f"- Objective: {next_target[0]['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    generated_paths: list[Path],
    sources: list[dict[str, object]],
    derivations: list[dict[str, object]],
    product_bounds: list[dict[str, object]],
    anchors: list[dict[str, object]],
    missing: list[dict[str, object]],
    smoke: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    timestamp = stamp()
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("sources_exist", "all cited local sources exist", all(bool(row["exists"]) for row in sources), ""))
    checks.append(("needles_found", "all source needles found", all(bool(row["needle_found"]) for row in sources), ""))
    checks.append(("outputs_exist", "all generated paths exist", all(path.exists() for path in generated_paths), ""))
    csv_parse_ok = True
    csv_error = ""
    try:
        for path in [path for path in generated_paths if path.suffix.lower() == ".csv"]:
            if not parse_csv(path):
                csv_parse_ok = False
                csv_error = f"empty csv: {path}"
                break
    except Exception as exc:  # pragma: no cover
        csv_parse_ok = False
        csv_error = str(exc)
    checks.append(("csv_parse", "all generated CSV files parse and are nonempty", csv_parse_ok, csv_error))
    formulas = " ".join(str(row["formula"]) for row in derivations)
    checks.append(("core_formula", "P_N and alpha_nuisance formulas are present", "P_N :=" in formulas and "alpha_nuisance :=" in formulas and "lambda_H^4" in formulas, ""))
    checks.append(("product_rows", "product-bound rows have at least 30 positive rows", len(product_bounds) >= 30 and all(float(row["lambda_m"]) > 0 and float(row["P_N_max_zero_nuisance_m4"]) > 0 for row in product_bounds), f"rows={len(product_bounds)}"))
    anchor_mu = float(anchors[0]["mu_H_lower_bound_m_inv_for_alpha1"])
    checks.append(("anchor_muH", "anchor mu_H lower bound is positive and near 25906 m^-1", 25000.0 < anchor_mu < 27000.0, f"mu_H={anchor_mu}"))
    checks.append(("nonclaim_rows", "all rows remain nonclaim", all(row["claim_allowed"] is False for row in [*derivations, *product_bounds, *anchors, *missing, *smoke, *decisions, *claim_gates, *next_target]), ""))
    checks.append(("missing_narrowed", "missing rows include P_N, lambda_H, and alpha_nuisance", all(any(row["quantity"] == quantity for row in missing) for quantity in ["P_N", "lambda_H", "alpha_nuisance"]), ""))
    checks.append(("smoke_schema", "smoke rows report product curve and anchor", any(row["smoke_id"] == "SMOKE3703_0_product_curve_schema" for row in smoke) and any(row["smoke_id"] == "SMOKE3703_3_anchor_muH" for row in smoke), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3704", "next target advances to nuisance cleanup", str(next_target[0]["target_doc"]).startswith("3704-") and "nuisance" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains core R10 gate terms", all(term in doc_text for term in ["P_N", "alpha_nuisance", "lambda_H^4", "38.6 micrometer", "valid_for_claim=false"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3703*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3703 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
    return [
        {
            **base(timestamp),
            "validation_id": check_id,
            "description": description,
            "result": "PASS" if passed else "FAIL",
            "details": details,
        }
        for check_id, description, passed, details in checks
    ]


def main() -> int:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    curve_rows = read_curve_rows()
    sources = source_register(timestamp)
    derivations = derivation_rows(timestamp)
    product_bounds = product_bound_rows(timestamp, curve_rows)
    anchors = anchor_rows(timestamp)
    missing = missing_parent_rows(timestamp)
    smoke = smoke_rows(timestamp, product_bounds, anchors)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp, product_bounds)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3703_SOURCE_REGISTER.csv",
        "derivations": RESIDUALS / "P8_Y5_R2FR_3703_DERIVATION_ROWS.csv",
        "product_bounds": RESIDUALS / "P8_Y5_R2FR_3703_R10_PRODUCT_BOUND_ROWS.csv",
        "anchors": RESIDUALS / "P8_Y5_R2FR_3703_ANCHOR_ROWS.csv",
        "missing": RESIDUALS / "P8_Y5_R2FR_3703_MISSING_PARENT_INPUT_ROWS.csv",
        "smoke": RESIDUALS / "P8_Y5_R2FR_3703_SMOKE_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3703_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3703_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3703_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3703_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3703_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["derivations"], derivations)
    write_csv(outputs["product_bounds"], product_bounds)
    write_csv(outputs["anchors"], anchors)
    write_csv(outputs["missing"], missing)
    write_csv(outputs["smoke"], smoke)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, derivations, product_bounds, anchors, missing, smoke, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, derivations, product_bounds, anchors, missing, smoke, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3703 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3703 checkpoint: R10 MTS-side inputs compressed to P_N/lambda_H/alpha_nuisance gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
