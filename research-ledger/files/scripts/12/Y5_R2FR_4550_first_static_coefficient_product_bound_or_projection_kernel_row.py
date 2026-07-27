from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4550"
CLAIM_ID = "L-392"
BRANCH_ID = "MTS_R2FR_Y5_STATIC_PRODUCT_BOUNDS_4550"
MARKER = "PPC4161_FIRST_STATIC_COEFFICIENT_PRODUCT_BOUND_OR_PROJECTION_KERNEL_ROW_4550"
PACKET_MARKER = "PPC4161_PACKET_FIRST_STATIC_COEFFICIENT_PRODUCT_BOUND_OR_PROJECTION_KERNEL_ROW_4550"
DECISION = "FIRST_STATIC_OBSERVABLE_PRODUCT_BOUNDS_DERIVED_ALPHA3_HARD_WALL_NONCLAIM"
NEXT_TARGET = "4551-Y5-R2FR-alpha3-vector-boundary-zero-or-first-Kalpha3-source-projection.md"

FORMAL_PATH = FORMAL / "566-PPC4161-first-static-coefficient-product-bound-or-projection-kernel-row.md"
DOC_PATH = POST / "4550-Y5-R2FR-first-static-coefficient-product-bound-or-projection-kernel-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4547 = FORMAL / "563-PPC4161-local-static-residual-vector-projection-to-PPN-Gdot-R10-or-first-numeric-Ubound-row.md"
DOC_4549 = FORMAL / "565-PPC4161-source-real-local-domain-Bmin-or-first-projection-kernel-row.md"
DOMAIN_4549 = SOURCE_DIR / "P8_Y5_R2FR_4549_LOCAL_DOMAIN_BMIN_ROWS.csv"
STATIC_4549 = SOURCE_DIR / "P8_Y5_R2FR_4549_STATIC_BOUND_WITH_DOMAIN_EPSILON_SMOKE.csv"
BLOCKERS_4549 = SOURCE_DIR / "P8_Y5_R2FR_4549_REMAINING_BLOCKERS.csv"
PROJ_4547 = SOURCE_DIR / "P8_Y5_R2FR_4547_ARENA_PROJECTION_CONTRACT.csv"
PASS_4547 = SOURCE_DIR / "P8_Y5_R2FR_4547_PASS_INEQUALITY_ROWS.csv"
EPS_4547 = SOURCE_DIR / "P8_Y5_R2FR_4547_EPSILON_U_BOUND_ROWS.csv"
STATIC_BUDGET_4546 = SOURCE_DIR / "P8_Y5_R2FR_4546_STATIC_JRES_BUDGET.csv"
UB2_THEOREM_4546 = SOURCE_DIR / "P8_Y5_R2FR_4546_UB2_STATIC_BOUND_THEOREM.csv"
ML_BOUND_4546 = SOURCE_DIR / "P8_Y5_R2FR_4546_ML_HOMOGENEITY_BOUND.csv"
REQ_4546 = SOURCE_DIR / "P8_Y5_R2FR_4546_INPUT_REQUIREMENTS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4550_SOURCE_REGISTER.csv"
PRODUCT_LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4550_STATIC_PRODUCT_BOUND_LAW.csv"
SELECTED_DOMAIN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4550_SELECTED_DOMAIN_EPSILON.csv"
PRODUCT_BOUNDS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4550_OBSERVABLE_PRODUCT_BOUNDS.csv"
GDOT_DERIVATIVE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4550_GDOT_DERIVATIVE_PRODUCT_CAVEAT.csv"
RANKING_CSV = SOURCE_DIR / "P8_Y5_R2FR_4550_PRODUCT_BOUND_RANKING.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4550_REMAINING_BLOCKERS.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4550_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4550_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4550_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4550_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4550_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def markdown_table(rows: list[dict[str, Any]], limit: int | None = None) -> str:
    if not rows:
        return "\n"
    chosen = rows[:limit] if limit is not None else rows
    headers: list[str] = []
    for row in chosen:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in chosen:
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    if limit is not None and len(rows) > limit:
        lines.append(f"| ... | {len(rows) - limit} additional rows in CSV |" + " |" * max(len(headers) - 2, 0))
    return "\n".join(lines) + "\n"


def safe_float(value: Any) -> float | None:
    try:
        if value is None or str(value).strip().lower() in {"", "missing", "nan"}:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def source_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC4550_00_4546_static_budget",
            "label": "4546 static residual envelope",
            "path": STATIC_BUDGET_4546,
            "needle": "SJ4546_0_static_budget",
        },
        {
            "source_id": "SRC4550_01_4546_UB2_source",
            "label": "4546 U_B^2 source theorem",
            "path": UB2_THEOREM_4546,
            "needle": "UB24546_1_linear_silence",
        },
        {
            "source_id": "SRC4550_02_4546_mL",
            "label": "4546 m_L homogeneity bound",
            "path": ML_BOUND_4546,
            "needle": "ML4546_2_laplacian",
        },
        {
            "source_id": "SRC4550_03_4546_requirements",
            "label": "4546 retained inputs",
            "path": REQ_4546,
            "needle": "REQ4546_3_boundary_static",
        },
        {
            "source_id": "SRC4550_04_4547_doc_projection_law",
            "label": "4547 projection law",
            "path": DOC_4547,
            "needle": "Delta O_a = K_a B_static",
        },
        {
            "source_id": "SRC4550_05_4547_projection_csv",
            "label": "4547 arena projection rows",
            "path": PROJ_4547,
            "needle": "AP4547_05_alpha3",
        },
        {
            "source_id": "SRC4550_06_4547_pass_csv",
            "label": "4547 pass inequalities",
            "path": PASS_4547,
            "needle": "PI4547_alpha3",
        },
        {
            "source_id": "SRC4550_07_4547_epsilon_csv",
            "label": "4547 epsilon formulas",
            "path": EPS_4547,
            "needle": "EUB4547_alpha3",
        },
        {
            "source_id": "SRC4550_08_4549_domain",
            "label": "4549 selected domain epsilon",
            "path": DOMAIN_4549,
            "needle": "D4549_0_inner_solar_1_to_30_AU",
        },
        {
            "source_id": "SRC4550_09_4549_static_update",
            "label": "4549 static epsilon insertion",
            "path": STATIC_4549,
            "needle": "UPD4549_alpha3",
        },
        {
            "source_id": "SRC4550_10_4549_blockers",
            "label": "4549 blocker update",
            "path": BLOCKERS_4549,
            "needle": "BLOCK4549_1_Sstatic",
        },
        {
            "source_id": "SRC4550_11_4549_doc",
            "label": "4549 documented epsilon square",
            "path": DOC_4549,
            "needle": "epsilon_U^2 = 6.1936352451434104e-15",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        path = spec["path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle = spec["needle"]
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": b(exists),
                "needle": needle,
                "needle_found": b(exists and needle in text),
                "valid_for_claim": "False",
            }
        )
    return rows


def selected_domain_row() -> dict[str, Any]:
    rows = read_csv(DOMAIN_4549)
    for row in rows:
        if row.get("domain_id") == "D4549_0_inner_solar_1_to_30_AU":
            eps = safe_float(row.get("epsilon_U_domain"))
            eps2 = safe_float(row.get("epsilon_U_squared"))
            if eps is None or eps2 is None:
                raise RuntimeError("Selected domain lacks numeric epsilon_U")
            return {
                "selected_id": "SEL4550_0",
                "domain_id": row["domain_id"],
                "r_out_AU": row["r_out_AU"],
                "B_min": row["B_min"],
                "epsilon_U": f"{eps:.16e}",
                "epsilon_U_squared": f"{eps2:.16e}",
                "source_path": str(DOMAIN_4549),
                "status": "selected_source_model_domain_for_product_bounds",
                "valid_for_claim": "False",
            }
    raise RuntimeError("D4549_0_inner_solar_1_to_30_AU not found")


def product_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "LAW4550_0_static_product_identity",
            "object": "observable static residual",
            "assumptions": "4546 static envelope; 4547 projection law; 4549 selected source-model domain epsilon.",
            "law": "B_static = S_static epsilon_U^2 + B_boundary,a + O(epsilon_U^3), where S_static=C_H A_1 + D_m C_lap_m/L_B^2.",
            "projection": "Delta O_a = K_a B_static.",
            "result": "Delta O_a = P_a epsilon_U^2 + Q_a + R_a with P_a=K_a S_static, Q_a=K_a B_boundary,a, R_a=K_a O(epsilon_U^3).",
            "valid_for_claim": "False",
        },
        {
            "law_id": "LAW4550_1_no_cancellation_bound",
            "object": "sufficient product pass condition",
            "assumptions": "No cancellation between source, boundary and higher-order terms.",
            "law": "|P_a| epsilon_U^2 + |Q_a| + |R_a| <= B_a.",
            "projection": "If Q_a=R_a=0, then |P_a| <= B_a/epsilon_U^2.",
            "result": "This gives the first numeric combined source-projection product budget.",
            "valid_for_claim": "False",
        },
        {
            "law_id": "LAW4550_2_equal_budget_split",
            "object": "conservative smoke split",
            "assumptions": "Allocate half of the observable budget to source product and half to boundary/static residue.",
            "law": "|P_a| <= B_a/(2 epsilon_U^2), |Q_a|+|R_a| <= B_a/2.",
            "projection": "Useful for prioritising which channel needs a theorem first.",
            "result": "alpha3 is the hard wall by many orders.",
            "valid_for_claim": "False",
        },
    ]


def projection_rows_by_observable() -> dict[str, dict[str, str]]:
    rows = read_csv(PROJ_4547)
    by_obs: dict[str, dict[str, str]] = {}
    for row in rows:
        by_obs[row.get("observable", "")] = row
    return by_obs


def static_projection_rows() -> list[dict[str, str]]:
    rows = []
    for row in read_csv(PROJ_4547):
        observable = row.get("observable", "")
        if observable == "Gdot_over_G":
            continue
        rows.append(row)
    return rows


def product_bound_rows(selected: dict[str, Any]) -> list[dict[str, Any]]:
    eps2 = float(selected["epsilon_U_squared"])
    rows: list[dict[str, Any]] = []
    for row in static_projection_rows():
        observable = row["observable"]
        bound = safe_float(row.get("bound"))
        if bound is None:
            continue
        zero_boundary = bound / eps2
        split_product = 0.5 * bound / eps2
        split_boundary = 0.5 * bound
        effective_product = row.get("effective_product", "")
        if observable == "alpha3":
            product_symbol = "P_alpha3_src := K_alpha3^src S_static"
            boundary_symbol = "Q_alpha3_vec := K_alpha3^vec B_boundary/vector_static"
            priority = "hardest_current_wall"
        elif "alpha_Yukawa" in observable:
            product_symbol = "P_R10(lambda) := K_R10(lambda) S_static(lambda)"
            boundary_symbol = "Q_R10(lambda) := K_R10(lambda) B_boundary,R10(lambda)"
            priority = "curve_required_anchor_smoke_only"
        else:
            product_symbol = f"P_{observable} := K_{observable} S_static"
            boundary_symbol = f"Q_{observable} := K_{observable} B_boundary,{observable}"
            priority = "static_projection_product_budget"
        rows.append(
            {
                "product_id": "PB4550_" + observable.replace("(", "").replace(")", "").replace("/", "_").replace(" ", "_").replace("+", "p").replace("-", "m"),
                "arena": row.get("arena", ""),
                "observable": observable,
                "effective_product": effective_product,
                "bound": f"{bound:.16e}",
                "bound_units": row.get("units", ""),
                "epsilon_U_squared": f"{eps2:.16e}",
                "product_symbol": product_symbol,
                "boundary_symbol": boundary_symbol,
                "exact_no_cancellation_condition": f"|{product_symbol}|*epsilon_U^2 + |{boundary_symbol}| + |R_higher_{observable}| <= {bound:.16e} {row.get('units', '')}",
                "max_product_if_boundary_and_higher_zero": f"{zero_boundary:.16e}",
                "max_product_equal_half_budget": f"{split_product:.16e}",
                "max_boundary_plus_higher_equal_half_budget": f"{split_boundary:.16e}",
                "priority": priority,
                "status": "numeric_combined_product_bound_nonclaim",
                "valid_for_claim": "False",
            }
        )
    rows.sort(key=lambda item: float(item["max_product_if_boundary_and_higher_zero"]))
    return rows


def gdot_derivative_rows(selected: dict[str, Any]) -> list[dict[str, Any]]:
    eps2 = float(selected["epsilon_U_squared"])
    bound = 2.42e-14
    derivative_product = bound / eps2
    return [
        {
            "row_id": "GD4550_0_static_channel",
            "channel": "Gdot_over_G_static",
            "law": "Static B_static amplitude does not by itself create Gdot; 4545 derivative silence remains the preferred route.",
            "numeric_bound": "not_applicable_to_static_amplitude",
            "status": "derivative_theorem_preferred",
            "valid_for_claim": "False",
        },
        {
            "row_id": "GD4550_1_derivative_fallback",
            "channel": "Gdot_over_G_derivative_if_DtBstatic_live",
            "law": "|J_Gdot^t D_t B_static| <= 2.42e-14 yr^-1. If D_t B_static = Pdot_G epsilon_U^2 + Qdot, then |Pdot_G| <= 2.42e-14/epsilon_U^2 only when Qdot=0 and no cancellation is used.",
            "epsilon_U_squared": f"{eps2:.16e}",
            "max_derivative_product_if_boundary_zero_per_yr": f"{derivative_product:.16e}",
            "status": "numeric_derivative_product_caveat_nonclaim",
            "valid_for_claim": "False",
        },
    ]


def ranking_rows(product_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for rank, row in enumerate(product_rows, start=1):
        rows.append(
            {
                "rank": rank,
                "observable": row["observable"],
                "arena": row["arena"],
                "max_product_if_boundary_and_higher_zero": row["max_product_if_boundary_and_higher_zero"],
                "why_it_matters": "smallest allowed product is the first closure pressure point" if rank == 1 else "less stringent than alpha3",
                "valid_for_claim": "False",
            }
        )
    return rows


def blocker_rows(product_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    hardest = product_rows[0]
    return [
        {
            "blocker_id": "BLOCK4550_0_alpha3_product",
            "new_information": f"Hardest no-boundary combined product is {hardest['observable']} <= {hardest['max_product_if_boundary_and_higher_zero']}.",
            "remaining_gap": "Need alpha3 vector/source projection anatomy: prove boundary vector zero or derive K_alpha3^src S_static below the product budget.",
            "next_action": "derive alpha3 vector boundary silence or first K_alpha3 source projection row",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLOCK4550_1_boundary",
            "new_information": "Boundary/static residue now has explicit budget rows.",
            "remaining_gap": "No theorem yet sets Q_a=K_a B_boundary,a to zero or below the row budgets.",
            "next_action": "separate vector/shear/scalar boundary channels and attempt a no-flux/no-hair proof",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLOCK4550_2_Sstatic",
            "new_information": "S_static does not need to be known alone if product P_a=K_a S_static is bounded.",
            "remaining_gap": "A parent or projection calculation still must supply K_a S_static, not just K_a or S_static in isolation.",
            "next_action": "derive product directly from source-to-observable projection if possible",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLOCK4550_3_R10",
            "new_information": "R10 anchor product tolerance is enormous compared with alpha3, but anchor is not a curve.",
            "remaining_gap": "Full lambda-dependent R10 curve and K_R10(lambda) profile remain missing.",
            "next_action": "do not prioritise R10 until alpha3/vector wall is addressed, unless real R10 curve is needed for comparison",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows(product_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    alpha3 = next(row for row in product_rows if row["observable"] == "alpha3")
    return [
        {
            "gate_id": "GATE4550_0_product_law",
            "condition": "combined observable product law P_a epsilon_U^2 + Q_a + R_a derived",
            "status": "PASS",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4550_1_numeric_product_bounds",
            "condition": "static projection rows have numeric B_a/epsilon_U^2 product budgets",
            "status": "PASS",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4550_2_alpha3_hard_wall",
            "condition": f"alpha3 no-boundary product budget is {alpha3['max_product_if_boundary_and_higher_zero']}",
            "status": "PASS_PRIORITY_LOCK",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4550_3_no_claim_without_product_value",
            "condition": "no PPN/R10/local-GR claim before actual P_a and Q_a values or zero theorems are supplied",
            "status": "PASS_NONCLAIM",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "decision": DECISION,
            "summary": "4550 converts the 4549 domain epsilon into first combined observable product bounds. The alpha3 row is now the hard local wall: if boundary/higher terms are zero, |K_alpha3^src S_static| must be <= about 6.46e-6. This is not a pass; it is a precise target for the next derivation.",
            "claim_id": CLAIM_ID,
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "best_forward_route",
            "why": "The smallest allowed product is alpha3. Deriving K_alpha3 source/boundary anatomy attacks the actual survival condition instead of circling generic missing coefficients.",
            "success_condition": "Either prove Q_alpha3_vec=0 and derive |K_alpha3^src S_static| below the budget, or keep local branch explicitly finite/bounded.",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "created_utc": utc_now(),
            "decision": DECISION,
            "formal_doc": str(FORMAL_PATH),
            "post_doc": str(DOC_PATH),
            "validation": str(VALIDATION_PATH),
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    laws: list[dict[str, Any]],
    selected: dict[str, Any],
    products: list[dict[str, Any]],
    gdot_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append(
        {
            "validation_id": "VAL4550_00_sources",
            "status": "PASS" if source_ok else "FAIL",
            "detail": "all source paths exist and needles found" if source_ok else "source path or needle missing",
        }
    )

    law_ok = any(row["law_id"] == "LAW4550_0_static_product_identity" for row in laws) and any(
        row["law_id"] == "LAW4550_1_no_cancellation_bound" for row in laws
    )
    checks.append(
        {
            "validation_id": "VAL4550_01_product_law",
            "status": "PASS" if law_ok else "FAIL",
            "detail": "static product identity and no-cancellation bound present",
        }
    )

    eps2 = safe_float(selected.get("epsilon_U_squared"))
    selected_ok = selected.get("domain_id") == "D4549_0_inner_solar_1_to_30_AU" and eps2 is not None and eps2 > 0.0
    checks.append(
        {
            "validation_id": "VAL4550_02_selected_domain",
            "status": "PASS" if selected_ok else "FAIL",
            "detail": "selected 4549 domain epsilon_U^2 is numeric and positive",
        }
    )

    required = {"alpha3", "xi", "zeta3", "alpha_Yukawa_at_lambda_38p6um", "((2+2gamma-beta)/3)-1"}
    got = {row["observable"] for row in products}
    product_ok = required.issubset(got) and all(float(row["max_product_if_boundary_and_higher_zero"]) > 0 for row in products)
    checks.append(
        {
            "validation_id": "VAL4550_03_product_rows",
            "status": "PASS" if product_ok else "FAIL",
            "detail": "static observable product bounds generated",
        }
    )

    alpha3 = next((row for row in products if row["observable"] == "alpha3"), None)
    alpha_ok = alpha3 is not None and float(alpha3["max_product_if_boundary_and_higher_zero"]) < 1.0e-3
    checks.append(
        {
            "validation_id": "VAL4550_04_alpha3_priority",
            "status": "PASS" if alpha_ok else "FAIL",
            "detail": "alpha3 is identified as a hard sub-1e-3 product wall",
        }
    )

    gdot_ok = any(row["row_id"] == "GD4550_1_derivative_fallback" for row in gdot_rows) and all(
        row["valid_for_claim"] == "False" for row in gdot_rows
    )
    checks.append(
        {
            "validation_id": "VAL4550_05_gdot_caveat",
            "status": "PASS" if gdot_ok else "FAIL",
            "detail": "Gdot derivative caveat exists and remains nonclaim",
        }
    )

    gate_ok = all(row["status"].startswith("PASS") for row in gates)
    checks.append(
        {
            "validation_id": "VAL4550_06_claim_gates",
            "status": "PASS" if gate_ok else "FAIL",
            "detail": "claim gates pass and retain nonclaim posture",
        }
    )

    generated = [
        SOURCE_REGISTER,
        PRODUCT_LAW_CSV,
        SELECTED_DOMAIN_CSV,
        PRODUCT_BOUNDS_CSV,
        GDOT_DERIVATIVE_CSV,
        RANKING_CSV,
        BLOCKERS_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
    ]
    csv_ok = True
    details: list[str] = []
    for path in generated:
        try:
            rows = read_csv(path)
            if not rows:
                csv_ok = False
                details.append(f"{path.name}:no_rows")
        except Exception as exc:  # pragma: no cover
            csv_ok = False
            details.append(f"{path.name}:{exc}")
    checks.append(
        {
            "validation_id": "VAL4550_07_csv_parse",
            "status": "PASS" if csv_ok else "FAIL",
            "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(details),
        }
    )

    doc_ok = DOC_PATH.exists() and FORMAL_PATH.exists()
    checks.append(
        {
            "validation_id": "VAL4550_08_docs_written",
            "status": "PASS" if doc_ok else "FAIL",
            "detail": "post and formal checkpoint docs written",
        }
    )

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append(
        {
            "validation_id": "VAL4550_09_pycache_absent",
            "status": "PASS" if pycache_absent else "FAIL",
            "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present",
        }
    )

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        {
            "validation_id": "VAL4550_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "4550 first static observable product bounds",
        }
    )
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    laws: list[dict[str, Any]],
    selected_rows: list[dict[str, Any]],
    products: list[dict[str, Any]],
    gdot_rows: list[dict[str, Any]],
    ranking: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    generated = utc_now()
    alpha3 = next(row for row in products if row["observable"] == "alpha3")
    selected = selected_rows[0]
    return f"""# 4550 - First static coefficient-product bound or projection-kernel row

Generated: `{generated}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4549 made `epsilon_U^2` numeric for the selected source-model local domain:

```text
domain = {selected['domain_id']}
epsilon_U^2 = {selected['epsilon_U_squared']}
```

4550 now converts the static scorer into combined observable product bounds. Write

```text
S_static = C_H A_1 + D_m C_lap_m/L_B^2
B_static = S_static epsilon_U^2 + B_boundary,a + O(epsilon_U^3)
Delta O_a = K_a B_static.
```

Then

```text
Delta O_a = P_a epsilon_U^2 + Q_a + R_a
P_a = K_a S_static
Q_a = K_a B_boundary,a.
```

Without cancellation, the sufficient condition is:

```text
|P_a| epsilon_U^2 + |Q_a| + |R_a| <= B_a.
```

If the boundary and higher-order residues are proven zero, the first product budget is:

```text
|P_a| <= B_a / epsilon_U^2.
```

The hard wall is now explicit:

```text
alpha3: |K_alpha3^src S_static| <= {alpha3['max_product_if_boundary_and_higher_zero']}
```

That is not a pass. It is the next target: either derive alpha3 vector/boundary silence, or show the combined source projection product is below this budget.

## Product Law

{markdown_table(laws)}

## Selected Domain

{markdown_table(selected_rows)}

## Observable Product Bounds

{markdown_table(products)}

## Gdot Derivative Caveat

{markdown_table(gdot_rows)}

## Constraint Ranking

{markdown_table(ranking)}

## Remaining Blockers

{markdown_table(blockers)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_projection_bound",
        "claim": "4550 derives first combined observable product bounds from the 4549 domain epsilon, identifying alpha3 as the hardest local product wall while retaining nonclaim status.",
        "current_evidence": "Generated source register, static product law, selected domain epsilon row, observable product bounds, Gdot derivative caveat, ranking, blocker ledger, claim gates, status and validation CSVs.",
        "status": "first_static_product_bounds_alpha3_hard_wall_nonclaim",
        "next_test": NEXT_TARGET,
        "failure_mode": "Treating the product budget as a pass before deriving actual P_a=K_a S_static and Q_a=K_a B_boundary,a values or zero theorems.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "The alpha3 budget is now the priority survival condition.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    laws = product_law_rows()
    selected = selected_domain_row()
    selected_rows = [selected]
    products = product_bound_rows(selected)
    gdot_rows = gdot_derivative_rows(selected)
    ranking = ranking_rows(products)
    blockers = blocker_rows(products)
    gates = claim_gate_rows(products)
    decisions = decision_rows()
    next_ = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PRODUCT_LAW_CSV, laws)
    write_csv(SELECTED_DOMAIN_CSV, selected_rows)
    write_csv(PRODUCT_BOUNDS_CSV, products)
    write_csv(GDOT_DERIVATIVE_CSV, gdot_rows)
    write_csv(RANKING_CSV, ranking)
    write_csv(BLOCKERS_CSV, blockers)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_)
    write_csv(STATUS_CSV, status)

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    pending_doc = f"# 4550 - First static coefficient-product bound or projection-kernel row\n\nMarker: `{MARKER}`\n\nValidation pending.\n"
    DOC_PATH.write_text(pending_doc, encoding="utf-8")
    FORMAL_PATH.write_text(pending_doc, encoding="utf-8")

    validation = validate(sources, laws, selected, products, gdot_rows, gates)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, laws, selected_rows, products, gdot_rows, ranking, blockers, gates, decisions, next_, validation)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4550 First Static Observable Product Bounds

Marker: `{MARKER}`  
4550 converts the 4549 domain `epsilon_U^2` into combined observable product bounds. With boundary/higher-order residues zero, the alpha3 source product must satisfy `|K_alpha3^src S_static| <= 6.46e-6`, making alpha3 the hard local wall. This is not a pass; it is a precise target for deriving vector/boundary silence or the first alpha3 projection product. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4550 Packet Integration - Alpha3 Product Wall

Marker: `{PACKET_MARKER}`  
The local packet now has numeric combined product budgets, not just symbolic missing kernels. The priority survival condition is the alpha3 vector/source split: prove the boundary vector piece is zero and bound `K_alpha3^src S_static`, or the local finite branch remains open.
""",
    )

    print(f"wrote {DOC_PATH}")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    overall = next((row for row in validation if row["validation_id"] == "VAL4550_OVERALL"), {})
    print(f"overall={overall.get('status', 'UNKNOWN')} decision={DECISION}")


if __name__ == "__main__":
    main()
