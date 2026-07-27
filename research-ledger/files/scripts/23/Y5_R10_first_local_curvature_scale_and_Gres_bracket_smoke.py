from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1210"
TITLE = "1210-Y5-R10-first-local-curvature-scale-and-Gres-bracket-smoke"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
ASSUMPTIONS_PATH = OUT_DIR / f"{PACK_ID}_BRACKET_ASSUMPTIONS.csv"
FERMI_GRID_PATH = OUT_DIR / f"{PACK_ID}_FERMI_BRACKET_GRID.csv"
RADIUS_GRID_PATH = OUT_DIR / f"{PACK_ID}_REQUIRED_RADIUS_GRID.csv"
INTERPRETATION_PATH = OUT_DIR / f"{PACK_ID}_INTERPRETATION_LEDGER.csv"
SOURCE_GAPS_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_GAPS.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1210_VALIDATION.csv"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = ROOT / relative_path
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def fmt(value: object) -> str:
    if isinstance(value, float):
        if value == 0:
            return "0"
        return f"{value:.12g}"
    return str(value)


def md_escape(value: object) -> str:
    return fmt(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str], limit: int | None = None) -> str:
    selected = rows[:limit] if limit is not None else rows
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in selected:
        lines.append("| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |")
    if limit is not None and len(rows) > limit:
        omitted = len(rows) - limit
        lines.append("| " + " | ".join(["..."] * (len(fields) - 1) + [f"{omitted} rows omitted; see CSV"]) + " |")
    return "\n".join(lines)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def classify_allowed_product(allowed: float) -> str:
    if allowed >= 1e12:
        return "VERY_LOOSE_FOR_NORMALIZED_PRODUCT"
    if allowed >= 1e6:
        return "LOOSE_FOR_NORMALIZED_PRODUCT"
    if allowed >= 1:
        return "POSSIBLY_FEASIBLE_IF_NORMALIZED_PRODUCT_ORDER_UNITY"
    if allowed >= 1e-6:
        return "TIGHT_REQUIRES_SMALL_CP_GRES_PRODUCT"
    return "EXTREMELY_TIGHT_OR_BAD_SCALE"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1210_0_1209_next",
            "local_path": "1209-Y5-R10-local-Fermi-domain-curvature-source-pack-or-domain-motion-lock.md",
            "needle": "NEXT1209_0_1210",
            "purpose": "handoff to first local curvature and G_res bracket smoke",
        },
        {
            "source_id": "SRC1210_1_1209_pressure_clean",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1209_PRESSURE_SMOKE_SCHEMA.csv",
            "needle": "PSC1209_0_clean_fermi_projector",
            "purpose": "clean Fermi projector pressure formula",
        },
        {
            "source_id": "SRC1210_2_1209_pressure_full",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1209_PRESSURE_SMOKE_SCHEMA.csv",
            "needle": "PSC1209_1_full_projector_budget",
            "purpose": "full projector pressure formula with blockers",
        },
        {
            "source_id": "SRC1210_3_1209_CP",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1209_UNIFIED_SOURCE_PACK.csv",
            "needle": "USP1209_6_CP",
            "purpose": "C_P remains an unsourced operator constant",
        },
        {
            "source_id": "SRC1210_4_1209_Gres",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1209_UNIFIED_SOURCE_PACK.csv",
            "needle": "USP1209_7_Gres",
            "purpose": "G_res_norm remains an unsourced local residual norm",
        },
        {
            "source_id": "SRC1210_5_1209_domain_motion",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1209_DOMAIN_MOTION_PROJECTOR_STRESS_AUDIT.csv",
            "needle": "DMP1209_1_non_geodesic_lab_bound",
            "purpose": "domain motion must stay explicit",
        },
        {
            "source_id": "SRC1210_6_1208_fermi_requirement",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1208_PRESSURE_COMPARISON.csv",
            "needle": "CMP1208_2_fermi_curvature_requirement",
            "purpose": "earlier Fermi curvature requirement",
        },
        {
            "source_id": "SRC1210_7_1207_target",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1207_PRESSURE_AND_ABSORPTION_GATE.csv",
            "needle": "PGA1207_0_total_formula",
            "purpose": "harsh projector target",
        },
    ]

    source_rows: list[dict[str, object]] = []
    for spec in source_specs:
        path_exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_rows.append(
            {
                **spec,
                "path_exists": path_exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    pressure_in = load_csv(OUT_DIR / "P8_Y5_R10_1209_PRESSURE_SMOKE_SCHEMA.csv")
    target = float(next(row for row in pressure_in if row["pressure_id"] == "PSC1209_0_clean_fermi_projector")["target"])

    length_grid_m = [1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0, 1000.0]
    curvature_grid_m2 = [1e-30, 1e-27, 1e-24, 1e-21]
    effective_fermi_constant_grid = [1.0, 10.0, 100.0]
    normalized_cp_gres_grid = [1.0, 1e3, 1e6, 1e9, 1e12]

    assumptions = [
        {
            "assumption_id": "ASM1210_0_clean_branch_only",
            "assumption": "Bracket grid evaluates only the clean Fermi curvature projector drift term.",
            "status": "NONCLAIM_SANDBOX",
            "consequence": "domain_motion_Linf and projector_stress_Linf remain separate blockers, not silently zeroed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "assumption_id": "ASM1210_1_effective_constant",
            "assumption": "C_eff represents C_Fermi plus any retained second-order curvature-gradient allowance.",
            "status": "BRACKET_PARAMETER_NOT_SOURCED",
            "consequence": "C_eff grid is a sensitivity scan, not evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "assumption_id": "ASM1210_2_allowed_product",
            "assumption": "Allowed product is S_allowed = target/(C_eff*L_D*Riemann_norm), where S=C_P*G_res_norm in the normalized pressure schema.",
            "status": "ALGEBRAIC_REARRANGEMENT",
            "consequence": "large S_allowed means the clean curvature drift is not the limiting piece; small S_allowed means C_P*G_res must be correspondingly tiny",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "assumption_id": "ASM1210_3_units_guard",
            "assumption": "C_P*G_res_norm may carry norm-dependent units until the operator norm is sourced.",
            "status": "UNITS_NOT_CLAIM_READY",
            "consequence": "all numeric rows are feasibility bookkeeping only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    grid_rows: list[dict[str, object]] = []
    for length_m in length_grid_m:
        for curvature in curvature_grid_m2:
            for c_eff in effective_fermi_constant_grid:
                fermi_drift = c_eff * length_m * curvature
                allowed_product = target / fermi_drift if fermi_drift > 0 else math.inf
                grid_rows.append(
                    {
                        "grid_id": f"FBG1210_{len(grid_rows):03d}",
                        "L_D_m": length_m,
                        "Riemann_norm_m2": curvature,
                        "C_eff": c_eff,
                        "fermi_projector_drift": fermi_drift,
                        "target": target,
                        "allowed_CpGres_product": allowed_product,
                        "classification": classify_allowed_product(allowed_product),
                        "omitted_terms": "domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf;curvature_gradient_explicit_row",
                        "valid_for_claim": False,
                        "claim_allowed": False,
                    }
                )

    radius_rows: list[dict[str, object]] = []
    for curvature in curvature_grid_m2:
        for c_eff in effective_fermi_constant_grid:
            for product in normalized_cp_gres_grid:
                max_radius = target / (c_eff * curvature * product)
                radius_rows.append(
                    {
                        "radius_id": f"RRG1210_{len(radius_rows):03d}",
                        "Riemann_norm_m2": curvature,
                        "C_eff": c_eff,
                        "assumed_CpGres_product": product,
                        "max_L_D_m_clean_branch": max_radius,
                        "target": target,
                        "classification": "CLEAN_BRANCH_RADIUS_REQUIREMENT_NONCLAIM",
                        "omitted_terms": "domain_motion_Linf;projector_stress_Linf;coframe_lock_Linf",
                        "valid_for_claim": False,
                        "claim_allowed": False,
                    }
                )

    allowed_values = [float(row["allowed_CpGres_product"]) for row in grid_rows]
    fermi_drifts = [float(row["fermi_projector_drift"]) for row in grid_rows]
    interpretation = [
        {
            "interpretation_id": "INT1210_0_range",
            "statement": "Clean Fermi curvature drift spans the generated grid.",
            "evidence": f"min_drift={fmt(min(fermi_drifts))}; max_drift={fmt(max(fermi_drifts))}; rows={len(grid_rows)}",
            "meaning": "the finite-domain curvature part alone can be made tiny for small domains/weak curvature, but this says nothing about G_res or hidden projector/domain terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "interpretation_id": "INT1210_1_allowed_product",
            "statement": "The clean branch converts the pressure target into an allowed C_P*G_res_norm product.",
            "evidence": f"min_allowed={fmt(min(allowed_values))}; max_allowed={fmt(max(allowed_values))}",
            "meaning": "this is the first useful design map: source C_P and G_res_norm, then see which domain/curvature rows survive",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "interpretation_id": "INT1210_2_no_pass",
            "statement": "No row is a pass row.",
            "evidence": "all rows have valid_for_claim=false and claim_allowed=false",
            "meaning": "this is a feasibility smoke map, not a local-GR/R10 claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    source_gaps = [
        {
            "gap_id": "GAP1210_0_CP",
            "missing_object": "C_P",
            "why_it_matters": "multiplies every projector leakage term before scoring q_projector",
            "best_next_source": "derive same-norm operator bound from D_T adjoint and projector leakage estimate",
            "status": "MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gap_id": "GAP1210_1_Gres",
            "missing_object": "G_res_norm",
            "why_it_matters": "sets whether small geometry drift actually produces a small residual response",
            "best_next_source": "derive from parent GR-reduction residual profile or prove theorem-zero in local branch",
            "status": "MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gap_id": "GAP1210_2_real_curvature_profile",
            "missing_object": "Riemann_norm;nabla_Riemann_norm;L_D",
            "why_it_matters": "turns bracket grid into a source-backed local arena row",
            "best_next_source": "choose explicit local arena/domain and compute curvature/domain scale under the same norm",
            "status": "MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gap_id": "GAP1210_3_domain_stress",
            "missing_object": "domain_motion_Linf;projector_stress_Linf",
            "why_it_matters": "can dominate clean curvature drift if not theorem-zero or bounded",
            "best_next_source": "parent-signed domain/readout lock or non-geodesic/stress finite-bound row",
            "status": "MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1210_0_grid_not_claim",
            "gate": "bracket grid as evidence",
            "status": "BLOCKED",
            "reason": "grid values are sensitivity parameters, not sourced physical rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1210_1_clean_branch_only",
            "gate": "clean Fermi branch pass",
            "status": "BLOCKED",
            "reason": "domain_motion, projector_stress, C_P, and G_res_norm are not sourced or theorem-zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1210_2_local_GR_R10",
            "gate": "local-GR/R10 pass",
            "status": "BLOCKED",
            "reason": "1210 is a feasibility map only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_rows = [
        {
            "next_id": "NEXT1210_0_1211",
            "target_file": "1211-Y5-R10-Gres-norm-source-or-local-residual-zero-theorem.md",
            "target_script": "scripts/Y5_R10_Gres_norm_source_or_local_residual_zero_theorem.py",
            "task": "derive or source G_res_norm for the local GR-reduction branch, because the 1210 map shows curvature-domain leakage cannot be scored without C_P*G_res_norm",
            "success_condition": "G_res_norm is theorem-zero, reduced to parent GR-limit residual terms, or staged as a same-norm source row that can feed the 1210 bracket",
            "do_not_do": "do not call bracket rows evidence; do not hide C_P or domain/stress blockers; do not edit formalization-workbench; do not push GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    source_fields = ["source_id", "local_path", "needle", "purpose", "path_exists", "needle_found", "valid_for_claim", "claim_allowed"]
    assumptions_fields = ["assumption_id", "assumption", "status", "consequence", "valid_for_claim", "claim_allowed"]
    grid_fields = ["grid_id", "L_D_m", "Riemann_norm_m2", "C_eff", "fermi_projector_drift", "target", "allowed_CpGres_product", "classification", "omitted_terms", "valid_for_claim", "claim_allowed"]
    radius_fields = ["radius_id", "Riemann_norm_m2", "C_eff", "assumed_CpGres_product", "max_L_D_m_clean_branch", "target", "classification", "omitted_terms", "valid_for_claim", "claim_allowed"]
    interpretation_fields = ["interpretation_id", "statement", "evidence", "meaning", "valid_for_claim", "claim_allowed"]
    gaps_fields = ["gap_id", "missing_object", "why_it_matters", "best_next_source", "status", "valid_for_claim", "claim_allowed"]
    gate_fields = ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]
    next_fields = ["next_id", "target_file", "target_script", "task", "success_condition", "do_not_do", "valid_for_claim", "claim_allowed"]

    write_csv(SOURCE_REGISTER_PATH, source_rows, source_fields)
    write_csv(ASSUMPTIONS_PATH, assumptions, assumptions_fields)
    write_csv(FERMI_GRID_PATH, grid_rows, grid_fields)
    write_csv(RADIUS_GRID_PATH, radius_rows, radius_fields)
    write_csv(INTERPRETATION_PATH, interpretation, interpretation_fields)
    write_csv(SOURCE_GAPS_PATH, source_gaps, gaps_fields)
    write_csv(CLAIM_GATES_PATH, claim_gates, gate_fields)
    write_csv(NEXT_PATH, next_rows, next_fields)

    formalization_recent = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            if path.is_file():
                mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                if mtime >= RUN_STARTED_UTC:
                    formalization_recent.append(path)

    csvs_to_parse = [
        SOURCE_REGISTER_PATH,
        ASSUMPTIONS_PATH,
        FERMI_GRID_PATH,
        RADIUS_GRID_PATH,
        INTERPRETATION_PATH,
        SOURCE_GAPS_PATH,
        CLAIM_GATES_PATH,
        NEXT_PATH,
    ]
    csv_parse_ok = True
    parse_details: list[str] = []
    for csv_path in csvs_to_parse:
        try:
            rows = load_csv(csv_path)
            parse_details.append(f"{csv_path.name}:{len(rows)}")
        except Exception as exc:  # noqa: BLE001
            csv_parse_ok = False
            parse_details.append(f"{csv_path.name}:ERROR:{exc}")

    all_sources_exist = all(bool(row["path_exists"]) for row in source_rows)
    all_needles_found = all(bool(row["needle_found"]) for row in source_rows)
    grid_count_ok = len(grid_rows) == len(length_grid_m) * len(curvature_grid_m2) * len(effective_fermi_constant_grid)
    radius_count_ok = len(radius_rows) == len(curvature_grid_m2) * len(effective_fermi_constant_grid) * len(normalized_cp_gres_grid)
    numeric_positive = all(float(row["fermi_projector_drift"]) > 0 and float(row["allowed_CpGres_product"]) > 0 for row in grid_rows)
    radius_positive = all(float(row["max_L_D_m_clean_branch"]) > 0 for row in radius_rows)
    target_preserved = abs(target - 1.17233215026e-05) < 1e-16
    omitted_terms_visible = all("domain_motion_Linf" in row["omitted_terms"] and "projector_stress_Linf" in row["omitted_terms"] for row in grid_rows + radius_rows)
    gaps_include_gres = any(row["missing_object"] == "G_res_norm" for row in source_gaps)
    no_claim = all(
        not bool(row.get("valid_for_claim")) and not bool(row.get("claim_allowed"))
        for row in assumptions + grid_rows + radius_rows + interpretation + source_gaps + claim_gates + next_rows
    )
    formalization_untouched = len(formalization_recent) == 0
    next_1211 = next_rows[0]["target_file"].startswith("1211-")

    validation_rows = [
        validation_row("VAL1210_0_sources_exist", "all cited local sources exist", all_sources_exist, f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"),
        validation_row("VAL1210_1_needles_found", "all cited source needles found", all_needles_found, f"{sum(bool(row['needle_found']) for row in source_rows)}/{len(source_rows)} needles found"),
        validation_row("VAL1210_2_grid_count", "Fermi bracket grid has expected row count", grid_count_ok, f"rows={len(grid_rows)}"),
        validation_row("VAL1210_3_radius_grid_count", "radius requirement grid has expected row count", radius_count_ok, f"rows={len(radius_rows)}"),
        validation_row("VAL1210_4_numeric_positive", "grid numeric values are positive", numeric_positive and radius_positive, "positive drift, allowed product, and max radius values"),
        validation_row("VAL1210_5_target_preserved", "1209 projector target is preserved", target_preserved, f"target={fmt(target)}"),
        validation_row("VAL1210_6_omitted_terms_visible", "domain/stress omitted terms are visible", omitted_terms_visible, "domain_motion_Linf and projector_stress_Linf retained in grid rows"),
        validation_row("VAL1210_7_gres_gap_visible", "G_res_norm source gap remains explicit", gaps_include_gres, "GAP1210_1_Gres present"),
        validation_row("VAL1210_8_nonclaim_policy", "all generated rows remain nonclaim", no_claim, "valid_for_claim=false and claim_allowed=false throughout"),
        validation_row("VAL1210_9_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(parse_details)),
        validation_row("VAL1210_10_formalization_untouched", "formalization-workbench untouched during run", formalization_untouched, f"formalization_recent_after_run_start_count={len(formalization_recent)}"),
        validation_row("VAL1210_11_next_target", "next target is staged", next_1211, next_rows[0]["target_file"]),
    ]
    validation_pass = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1210_12_overall",
            "overall 1210 validation",
            validation_pass,
            "1210 bracket smoke map is reproducible and nonclaim" if validation_pass else "one or more validation checks failed",
        )
    )
    validation_fields = ["check_id", "check", "status", "details", "valid_for_claim", "claim_allowed"]
    write_csv(VALIDATION_PATH, validation_rows, validation_fields)

    doc = f"""# 1210 Y5/R10 First Local Curvature Scale And Gres Bracket Smoke

**Current verdict:** 1210 still makes **no local-GR/R10 claim**. It gives the first algebraic feasibility map for the clean Fermi projector branch by solving the harsh target for the allowed `C_P*G_res_norm` product.

**Main progress:** using the clean branch `q_projector <= C_P*C_eff*L_D*Riemann_norm*G_res_norm`, the generated grid computes `allowed_CpGres_product = target/(C_eff*L_D*Riemann_norm)`. This tells us where the next pain is: `G_res_norm` and `C_P`, not the curvature scale by itself.

**Guardrail:** every grid row omits `domain_motion_Linf`, `projector_stress_Linf`, and the explicit curvature-gradient row, so every row remains nonclaim.

## Source Register

{markdown_table(source_rows, source_fields)}

## Bracket Assumptions

{markdown_table(assumptions, assumptions_fields)}

## Fermi Bracket Grid Preview

Full grid is in `{FERMI_GRID_PATH.name}`.

{markdown_table(grid_rows, grid_fields, limit=18)}

## Required Radius Grid Preview

Full grid is in `{RADIUS_GRID_PATH.name}`.

{markdown_table(radius_rows, radius_fields, limit=18)}

## Interpretation Ledger

{markdown_table(interpretation, interpretation_fields)}

## Source Gaps

{markdown_table(source_gaps, gaps_fields)}

## Claim Gates

{markdown_table(claim_gates, gate_fields)}

## Next Target

{markdown_table(next_rows, next_fields)}

## Validation

{markdown_table(validation_rows, validation_fields)}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"validation_pass={validation_pass}")
    print(f"grid_rows={len(grid_rows)}")
    print(f"radius_rows={len(radius_rows)}")
    print(f"target={fmt(target)}")
    print(f"allowed_CpGres_min={fmt(min(allowed_values))}")
    print(f"allowed_CpGres_max={fmt(max(allowed_values))}")
    print("local_GR_R10_claimed=false")


if __name__ == "__main__":
    main()
