from __future__ import annotations

import csv
import importlib.util
import json
import math
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4549"
CLAIM_ID = "L-391"
BRANCH_ID = "MTS_R2FR_Y5_LOCAL_DOMAIN_BMIN_4549"
MARKER = "PPC4161_SOURCE_REAL_LOCAL_DOMAIN_BMIN_OR_FIRST_PROJECTION_KERNEL_ROW_4549"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_REAL_LOCAL_DOMAIN_BMIN_OR_FIRST_PROJECTION_KERNEL_ROW_4549"
DECISION = "POINT_MASS_DOMAIN_BMIN_EPSILONU_ROWS_DERIVED_SOURCE_MODEL_NUMERIC_NONCLAIM_KERNELS_AND_COEFFICIENTS_STILL_MISSING"
NEXT_TARGET = "4550-Y5-R2FR-first-static-coefficient-product-bound-or-projection-kernel-row.md"

FORMAL_PATH = FORMAL / "565-PPC4161-source-real-local-domain-Bmin-or-first-projection-kernel-row.md"
DOC_PATH = POST / "4549-Y5-R2FR-source-real-local-domain-Bmin-or-first-projection-kernel-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_MODEL_SCRIPT = FORMAL / "scripts" / "source_model_curvature_Lcg_test.py"
SOURCE_MODEL_DOC = FORMAL / "89-source-model-curvature-Lcg-test.md"
SOURCE_MODEL_SUMMARY = FORMAL / "runs" / "source_model_curvature_Lcg_20260527-211932" / "summary.csv"
SOURCE_MODEL_STATUS = FORMAL / "runs" / "source_model_curvature_Lcg_20260527-211932" / "status.json"
RANGE_DOC_4548 = FORMAL / "564-PPC4161-fill-first-epsilonU-local-range-row-or-static-bound-runner-smoke.md"
RANGE_LAW_4548 = SOURCE_DIR / "P8_Y5_R2FR_4548_EPSILON_U_LOGISTIC_RANGE_LAW.csv"
LOCAL_RANGE_4548 = SOURCE_DIR / "P8_Y5_R2FR_4548_EPSILON_U_LOCAL_RANGE_ROW.csv"
SMOKE_4548 = SOURCE_DIR / "P8_Y5_R2FR_4548_STATIC_BOUND_SMOKE_RUNNER.csv"
BLOCKERS_4548 = SOURCE_DIR / "P8_Y5_R2FR_4548_NUMERIC_BLOCKERS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4549_SOURCE_REGISTER.csv"
DOMAIN_LAW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4549_POINT_MASS_DOMAIN_BMIN_LAW.csv"
DOMAIN_ROWS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4549_LOCAL_DOMAIN_BMIN_ROWS.csv"
MONOTONICITY_GRID_CSV = SOURCE_DIR / "P8_Y5_R2FR_4549_DOMAIN_MONOTONICITY_GRID.csv"
STATIC_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4549_STATIC_BOUND_WITH_DOMAIN_EPSILON_SMOKE.csv"
BLOCKER_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4549_REMAINING_BLOCKERS.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4549_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4549_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4549_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4549_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4549_VALIDATION.csv"


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


def source_model_module() -> Any:
    spec = importlib.util.spec_from_file_location("source_model_curvature_Lcg_test", SOURCE_MODEL_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {SOURCE_MODEL_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def default_params(module: Any) -> Any:
    h_bg = 70.0 * 1000.0 / module.MPC_M
    return module.Parameters(
        h_bg=h_bg,
        alpha_k=1.0 / 9.0,
        eta_h=1.0,
        w_c=1.0 / math.sqrt(48.0),
        w_r=1.0,
        b_star=1.0,
        delta_b=0.5,
        w_theta=2.0,
    )


def source_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC4549_00_source_model_script",
            "label": "source model script formulas",
            "path": SOURCE_MODEL_SCRIPT,
            "needle": "c_abs = math.sqrt(48.0) * G * mass_kg / (C * C * radius_m**3)",
        },
        {
            "source_id": "SRC4549_01_source_model_lcg",
            "label": "source model L_cg rule",
            "path": SOURCE_MODEL_SCRIPT,
            "needle": "return 1.0 / math.sqrt(1.0 / (l_h * l_h) + params.alpha_k * g_k * g_k)",
        },
        {
            "source_id": "SRC4549_02_source_model_screening",
            "label": "source model B_env/Pi_B/U_B",
            "path": SOURCE_MODEL_SCRIPT,
            "needle": "b_env = math.log1p(max(a_curv, 0.0)) - params.w_theta * math.log1p(max(e_theta, 0.0))",
        },
        {
            "source_id": "SRC4549_03_transition_solver",
            "label": "source model transition solver",
            "path": SOURCE_MODEL_SCRIPT,
            "needle": "def find_solar_transition_radius(params: Parameters) -> float:",
        },
        {
            "source_id": "SRC4549_04_source_model_doc",
            "label": "89 documented point-mass source model",
            "path": SOURCE_MODEL_DOC,
            "needle": "C_abs = sqrt(48) G M_sun / (c^2 r^3)",
        },
        {
            "source_id": "SRC4549_05_source_model_summary",
            "label": "source model summary rows",
            "path": SOURCE_MODEL_SUMMARY,
            "needle": "solar_transition_shell_point_mass",
        },
        {
            "source_id": "SRC4549_06_source_model_status",
            "label": "source model status parameters",
            "path": SOURCE_MODEL_STATUS,
            "needle": "\"b_star\": 1.0",
        },
        {
            "source_id": "SRC4549_07_4548_range_law",
            "label": "4548 epsilon_U range law",
            "path": RANGE_DOC_4548,
            "needle": "epsilon_U(D_loc) := sup_Dloc U_B",
        },
        {
            "source_id": "SRC4549_08_4548_range_csv",
            "label": "4548 range law CSV",
            "path": RANGE_LAW_4548,
            "needle": "LAW4548_1_domain_sup",
        },
        {
            "source_id": "SRC4549_09_4548_local_rows",
            "label": "4548 local range rows",
            "path": LOCAL_RANGE_4548,
            "needle": "LR4548_1_sun_1AU_point_anchor",
        },
        {
            "source_id": "SRC4549_10_4548_smoke",
            "label": "4548 static smoke runner",
            "path": SMOKE_4548,
            "needle": "SMOKE4548_alpha3",
        },
        {
            "source_id": "SRC4549_11_4548_blockers",
            "label": "4548 blockers",
            "path": BLOCKERS_4548,
            "needle": "MISSING_DOMAIN_INFIMUM",
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


def law_rows() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "LAW4549_0_point_mass_source_model",
            "object": "Solar point-mass B_env(r)",
            "assumptions": "Schwarzschild-vacuum proxy, E_theta=0, source model 89, default universal parameters b_*=1 and Delta_B=0.5.",
            "law": "C_abs=sqrt(48)GM/(c^2 r^3); K_B=w_C C_abs+eta_H H_bg^2/c^2; G_K=|d_r ln K_B|; L_cg=(L_H^-2+alpha_K G_K^2)^-1/2; A_curv=c L_cg w_C C_abs/H_bg; B_env=ln(1+A_curv).",
            "result": "If B_env is monotone non-increasing on [r_in,r_out], then B_min=B_env(r_out).",
            "status": "derived_from_existing_source_model",
            "valid_for_claim": "False",
        },
        {
            "law_id": "LAW4549_1_domain_epsilon",
            "object": "epsilon_U([r_in,r_out])",
            "assumptions": "B_env monotone non-increasing; r_out remains inside the quarantined transition radius.",
            "law": "epsilon_U = sup U_B = U_B(B_min) = 1/(1+exp[(B_min-B_*)/Delta_B]).",
            "result": "A named source-model domain now has numeric B_min and epsilon_U, but this is still a source-model row rather than a full PPN/R10 claim.",
            "status": "numeric_domain_row_ready_nonclaim",
            "valid_for_claim": "False",
        },
        {
            "law_id": "LAW4549_2_transition_guard",
            "object": "transition exclusion",
            "assumptions": "Solar transition radius is solved by B_env(r_tr)=B_* in source model 89.",
            "law": "A local suppression domain must satisfy r_out << r_tr or carry a separate transition-current/routing proof.",
            "result": "Rows ending near r_tr are retained as warnings and not promoted.",
            "status": "anti_smuggling_guard",
            "valid_for_claim": "False",
        },
    ]


def evaluate_radius(module: Any, params: Any, radius_m: float, name: str) -> dict[str, Any]:
    profile = module.point_mass_profile(module.M_SUN_KG)
    return module.radial_evaluate(name, profile, radius_m, "local_point_mass", params, "4549 domain-bound evaluation.")


def domain_specs(module: Any, params: Any) -> tuple[float, list[dict[str, Any]]]:
    transition_radius = float(module.find_solar_transition_radius(params))
    au = float(module.AU_M)
    return transition_radius, [
        {
            "domain_id": "D4549_0_inner_solar_1_to_30_AU",
            "label": "inner source-model Solar exterior",
            "r_in_m": 1.0 * au,
            "r_out_m": 30.0 * au,
            "r_out_definition": "30 AU chosen finite inner-Solar source-model interval; not a planet-data claim",
        },
        {
            "domain_id": "D4549_1_outer_solar_1_to_100_AU",
            "label": "extended source-model Solar exterior",
            "r_in_m": 1.0 * au,
            "r_out_m": 100.0 * au,
            "r_out_definition": "100 AU conservative finite local exterior smoke interval; not a full PPN domain claim",
        },
        {
            "domain_id": "D4549_2_guarded_0p1_transition",
            "label": "ten-percent transition guard domain",
            "r_in_m": 1.0 * au,
            "r_out_m": 0.1 * transition_radius,
            "r_out_definition": "r_out=0.1*r_transition using source-model transition solver",
        },
        {
            "domain_id": "D4549_3_half_transition_warning",
            "label": "half-transition warning domain",
            "r_in_m": 1.0 * au,
            "r_out_m": 0.5 * transition_radius,
            "r_out_definition": "r_out=0.5*r_transition; included as warning because suppression weakens near transition",
        },
    ]


def sample_domain(module: Any, params: Any, spec: dict[str, Any], transition_radius: float) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    r_in = float(spec["r_in_m"])
    r_out = float(spec["r_out_m"])
    sample_count = 17
    grid: list[dict[str, Any]] = []
    previous_b: float | None = None
    monotone = True
    min_b = float("inf")
    min_row: dict[str, Any] | None = None
    for index in range(sample_count):
        t = index / (sample_count - 1)
        radius = math.exp(math.log(r_in) * (1.0 - t) + math.log(r_out) * t)
        row = evaluate_radius(module, params, radius, f"{spec['domain_id']}_sample_{index:02d}")
        b_env = float(row["B_env"])
        u_b = float(row["U_B"])
        if previous_b is not None and b_env > previous_b + 1.0e-9:
            monotone = False
        previous_b = b_env
        if b_env < min_b:
            min_b = b_env
            min_row = row
        grid.append(
            {
                "domain_id": spec["domain_id"],
                "sample_index": index,
                "radius_m": f"{radius:.16e}",
                "radius_AU": f"{radius / module.AU_M:.16e}",
                "B_env": f"{b_env:.16e}",
                "U_B": f"{u_b:.16e}",
                "A_curv": f"{float(row['A_curv']):.16e}",
                "Pi_B": f"{float(row['Pi_B']):.16e}",
                "trace_warning": b(bool(row["trace_warning"])),
                "valid_for_claim": "False",
            }
        )

    endpoint = evaluate_radius(module, params, r_out, f"{spec['domain_id']}_endpoint")
    b_min = float(endpoint["B_env"])
    eps = float(endpoint["U_B"])
    b_star = float(params.b_star)
    delta_b = float(params.delta_b)
    recomputed = 1.0 / (1.0 + math.exp((b_min - b_star) / delta_b))
    transition_ratio = r_out / transition_radius
    strong = b_min - b_star >= 3.0
    guarded = transition_ratio <= 0.1
    weak_transition = transition_ratio > 0.1
    status = (
        "source_model_domain_bound_strong_nonclaim"
        if monotone and strong and guarded
        else "source_model_domain_bound_numeric_but_transition_margin_warning"
        if monotone and b_min > b_star
        else "not_local_suppression_domain"
    )
    summary = {
        "domain_id": spec["domain_id"],
        "label": spec["label"],
        "r_in_m": f"{r_in:.16e}",
        "r_out_m": f"{r_out:.16e}",
        "r_out_AU": f"{r_out / module.AU_M:.16e}",
        "r_transition_m": f"{transition_radius:.16e}",
        "r_out_over_r_transition": f"{transition_ratio:.16e}",
        "r_out_definition": spec["r_out_definition"],
        "monotone_Benv_nonincreasing": b(monotone),
        "B_min": f"{b_min:.16e}",
        "B_star": f"{b_star:.16e}",
        "Delta_B": f"{delta_b:.16e}",
        "margin_Bmin_minus_Bstar": f"{(b_min - b_star):.16e}",
        "epsilon_U_domain": f"{eps:.16e}",
        "epsilon_U_squared": f"{(eps * eps):.16e}",
        "epsilon_U_recomputed_from_Bmin": f"{recomputed:.16e}",
        "endpoint_A_curv": f"{float(endpoint['A_curv']):.16e}",
        "endpoint_Pi_B": f"{float(endpoint['Pi_B']):.16e}",
        "endpoint_trace_warning": b(bool(endpoint["trace_warning"])),
        "source_path": str(SOURCE_MODEL_SCRIPT),
        "status": status,
        "numeric_ready_for_smoke": b(monotone and b_min > b_star),
        "valid_for_claim": "False",
        "claim_guard": "source-model domain row only; still needs PPN/R10 domain justification, S_static, K_a and boundary rows",
        "warning": "near transition; do not use as local suppression proof" if weak_transition else "",
    }
    if min_row is not None and abs(float(min_row["B_env"]) - b_min) > 1.0e-6:
        summary["warning"] = (summary["warning"] + "; " if summary["warning"] else "") + "sample_min_not_endpoint_check"
    return summary, grid


def domain_rows_and_grid(module: Any, params: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    transition_radius, specs = domain_specs(module, params)
    summaries: list[dict[str, Any]] = []
    grid_rows: list[dict[str, Any]] = []
    for spec in specs:
        summary, grid = sample_domain(module, params, spec, transition_radius)
        summaries.append(summary)
        grid_rows.extend(grid)
    return summaries, grid_rows


def static_update_rows(domain_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    smoke_rows = read_csv(SMOKE_4548)
    preferred = next(row for row in domain_rows if row["domain_id"] == "D4549_0_inner_solar_1_to_30_AU")
    eps = preferred["epsilon_U_domain"]
    eps2 = preferred["epsilon_U_squared"]
    rows: list[dict[str, Any]] = []
    for row in smoke_rows:
        observable = row.get("observable", "")
        if observable == "Gdot_static_derivative":
            updated = "No epsilon_U-only static-amplitude pass. 4545 derivative silence or time-variation kernel still required."
            status = "domain_epsilon_not_sufficient_for_time_derivative_channel"
        else:
            updated = f"Using D4549_0 source-model domain: |Delta_{observable}| <= |K|*(S_static*{eps2} + B_boundary_{observable})"
            status = "domain_epsilon_inserted_coefficients_kernels_boundary_missing"
        rows.append(
            {
                "update_id": "UPD4549_" + observable.replace(" ", "_").replace("/", "_"),
                "observable": observable,
                "source_smoke_id": row.get("smoke_id", ""),
                "domain_epsilon_row": "D4549_0_inner_solar_1_to_30_AU",
                "epsilon_U_domain": eps,
                "epsilon_U_squared": eps2,
                "updated_static_formula": updated,
                "remaining_missing_inputs": "S_static=C_H A_1 + D_m C_lap_m/L_B^2; K_a; B_boundary,a",
                "status": status,
                "valid_for_claim": "False",
            }
        )
    return rows


def blocker_update_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker_id": "BLOCK4549_0_Dloc_Bmin",
            "previous_status": "MISSING_DOMAIN_INFIMUM",
            "new_status": "SOURCE_MODEL_NUMERIC_ROW_AVAILABLE_NONCLAIM",
            "what_changed": "The point-mass source model now gives B_min and epsilon_U for named finite domains.",
            "still_missing": "empirical/legal PPN/R10 domain adoption and transition-shell handling",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLOCK4549_1_Sstatic",
            "previous_status": "MISSING_COEFFICIENT_PRODUCTS",
            "new_status": "STILL_MISSING",
            "what_changed": "Domain epsilon can now be inserted into the formula.",
            "still_missing": "C_H A_1 and D_m C_lap_m/L_B^2, or a parent zero theorem",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLOCK4549_2_Kernels",
            "previous_status": "MISSING_ARENA_PROJECTION_KERNELS",
            "new_status": "STILL_MISSING",
            "what_changed": "Projection formulas now have a candidate epsilon input.",
            "still_missing": "K_alpha3, K_xi, K_R10(lambda), J_Gdot^t, orbital scalar kernel",
            "valid_for_claim": "False",
        },
        {
            "blocker_id": "BLOCK4549_3_Boundary",
            "previous_status": "MISSING_BOUNDARY_ZERO_OR_BOUND",
            "new_status": "STILL_MISSING",
            "what_changed": "Nothing in the domain epsilon row controls retained boundary/vector/shear channels.",
            "still_missing": "static boundary amplitude zero theorem or finite rows",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows(domain_rows: list[dict[str, Any]], monotonicity_grid: list[dict[str, Any]]) -> list[dict[str, Any]]:
    preferred = next(row for row in domain_rows if row["domain_id"] == "D4549_0_inner_solar_1_to_30_AU")
    return [
        {
            "gate_id": "GATE4549_0_source_model_load",
            "condition": "existing 89 source model script imported and evaluated without changing it",
            "status": "PASS",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4549_1_monotonicity",
            "condition": "B_env monotone non-increasing on sampled point-mass domains",
            "status": "PASS" if all(row["monotone_Benv_nonincreasing"] == "True" for row in domain_rows) else "FAIL",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4549_2_first_domain_numeric",
            "condition": "first finite inner-Solar source-model domain has positive margin B_min>B_* and numeric epsilon_U",
            "status": "PASS" if float(preferred["margin_Bmin_minus_Bstar"]) > 0 and float(preferred["epsilon_U_domain"]) > 0 else "FAIL",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4549_3_no_transition_smuggle",
            "condition": "rows near transition are warnings/nonclaim, not local suppression passes",
            "status": "PASS" if any(row["warning"] for row in domain_rows) else "FAIL",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "GATE4549_4_no_claim_until_kernels",
            "condition": "no PPN/R10/Gdot/local-GR claim before S_static, K_a and boundary rows exist",
            "status": "PASS",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "decision": DECISION,
            "summary": "4549 converts the 4548 epsilon_U law into named source-model point-mass domain rows. The inner 1-30 AU row supplies a numeric B_min and epsilon_U by monotonicity, but it remains nonclaim because projection kernels, S_static and boundary amplitudes are still absent.",
            "claim_id": CLAIM_ID,
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "route": "best_forward_route",
            "why": "D_loc/B_min is no longer purely missing. The next real blocker is turning B_static into an observable: either fill S_static coefficient products or derive the first projection kernel row.",
            "avoid": "Do not celebrate the small epsilon_U^2 number as a pass until S_static, K_a and B_boundary are real.",
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
    domains: list[dict[str, Any]],
    grid: list[dict[str, Any]],
    static_update: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append(
        {
            "validation_id": "VAL4549_00_sources",
            "status": "PASS" if source_ok else "FAIL",
            "detail": "all source paths exist and needles found" if source_ok else "source path or needle missing",
        }
    )

    law_ok = any(row["law_id"] == "LAW4549_0_point_mass_source_model" for row in laws) and any(
        row["law_id"] == "LAW4549_1_domain_epsilon" for row in laws
    )
    checks.append(
        {
            "validation_id": "VAL4549_01_law_rows",
            "status": "PASS" if law_ok else "FAIL",
            "detail": "point-mass domain and epsilon laws present",
        }
    )

    domain_ok = all(
        float(row["r_out_m"]) > float(row["r_in_m"])
        and float(row["B_min"]) > 0.0
        and float(row["epsilon_U_domain"]) > 0.0
        and row["valid_for_claim"] == "False"
        for row in domains
    )
    checks.append(
        {
            "validation_id": "VAL4549_02_domain_rows",
            "status": "PASS" if domain_ok else "FAIL",
            "detail": "domain rows have positive ranges, B_min and nonclaim epsilon_U",
        }
    )

    preferred = next(row for row in domains if row["domain_id"] == "D4549_0_inner_solar_1_to_30_AU")
    preferred_ok = (
        preferred["monotone_Benv_nonincreasing"] == "True"
        and float(preferred["margin_Bmin_minus_Bstar"]) > 3.0
        and float(preferred["epsilon_U_domain"]) < 1.0e-5
    )
    checks.append(
        {
            "validation_id": "VAL4549_03_first_domain_bound",
            "status": "PASS" if preferred_ok else "FAIL",
            "detail": "inner 1-30 AU source-model domain has strong positive screening margin",
        }
    )

    grid_ok = len(grid) >= 4 * 17 and all(row["valid_for_claim"] == "False" for row in grid)
    checks.append(
        {
            "validation_id": "VAL4549_04_monotonicity_grid",
            "status": "PASS" if grid_ok else "FAIL",
            "detail": "monotonicity grid present and nonclaim",
        }
    )

    static_ok = {"alpha3", "xi", "R10_alpha_anchor", "Gdot_static_derivative"}.issubset(
        {row["observable"] for row in static_update}
    ) and all(row["valid_for_claim"] == "False" for row in static_update)
    checks.append(
        {
            "validation_id": "VAL4549_05_static_update",
            "status": "PASS" if static_ok else "FAIL",
            "detail": "static smoke rows updated with domain epsilon and remain nonclaim",
        }
    )

    gate_ok = all(row["status"].startswith("PASS") for row in gates)
    checks.append(
        {
            "validation_id": "VAL4549_06_claim_gates",
            "status": "PASS" if gate_ok else "FAIL",
            "detail": "claim gates pass and retain nonclaim guard",
        }
    )

    generated = [
        SOURCE_REGISTER,
        DOMAIN_LAW_CSV,
        DOMAIN_ROWS_CSV,
        MONOTONICITY_GRID_CSV,
        STATIC_UPDATE_CSV,
        BLOCKER_UPDATE_CSV,
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
            "validation_id": "VAL4549_07_csv_parse",
            "status": "PASS" if csv_ok else "FAIL",
            "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(details),
        }
    )

    doc_ok = DOC_PATH.exists() and FORMAL_PATH.exists()
    checks.append(
        {
            "validation_id": "VAL4549_08_docs_written",
            "status": "PASS" if doc_ok else "FAIL",
            "detail": "post and formal checkpoint docs written",
        }
    )

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append(
        {
            "validation_id": "VAL4549_09_pycache_absent",
            "status": "PASS" if pycache_absent else "FAIL",
            "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present",
        }
    )

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        {
            "validation_id": "VAL4549_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "4549 local domain B_min and epsilon_U source-model bound",
        }
    )
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    laws: list[dict[str, Any]],
    domains: list[dict[str, Any]],
    grid: list[dict[str, Any]],
    static_update: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    generated = utc_now()
    preferred = next(row for row in domains if row["domain_id"] == "D4549_0_inner_solar_1_to_30_AU")
    return f"""# 4549 - Source real local-domain B_min or first projection-kernel row

Generated: `{generated}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4548 derived the range law but only had a single Sun-1AU point anchor. 4549 turns that into actual finite source-model domain rows.

For the existing point-mass source model:

```text
C_abs = sqrt(48) G M_sun/(c^2 r^3)
K_B   = w_C C_abs + eta_H H_bg^2/c^2
G_K   = |d_r ln K_B|
L_cg  = (L_H^-2 + alpha_K G_K^2)^(-1/2)
A_curv = c L_cg w_C C_abs / H_bg
B_env = ln(1 + A_curv)
U_B   = 1/(1 + exp[(B_env-B_*)/Delta_B]).
```

If `B_env(r)` is monotone decreasing on `[r_in,r_out]`, then the domain infimum is the endpoint:

```text
B_min = B_env(r_out),  epsilon_U([r_in,r_out]) = U_B(r_out).
```

The first useful row is `{preferred['domain_id']}`:

```text
r_out = {preferred['r_out_AU']} AU
B_min = {preferred['B_min']}
epsilon_U = {preferred['epsilon_U_domain']}
epsilon_U^2 = {preferred['epsilon_U_squared']}
```

That is real movement: `epsilon_U` is no longer only a missing symbol for this source-model domain. It is still not a PPN/R10/local-GR pass because `S_static`, `K_a`, and retained boundary amplitudes are not supplied.

## Point-Mass Domain Law

{markdown_table(laws)}

## Local Domain B_min Rows

{markdown_table(domains)}

## Static Bound With Domain epsilon_U

{markdown_table(static_update)}

## Remaining Blockers

{markdown_table(blockers)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_)}

## Monotonicity Grid Preview

{markdown_table(grid, limit=12)}

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
        "claim": "4549 derives source-model local-domain B_min and epsilon_U rows for finite Solar point-mass intervals, promoting epsilon_U from point-anchor to domain-bound form while keeping all PPN/R10/local-GR claims blocked.",
        "current_evidence": "Generated source register, point-mass domain law, local domain B_min rows, monotonicity grid, static update rows, blocker ledger, claim gates, status and validation CSVs.",
        "status": "source_model_domain_epsilon_bound_nonclaim",
        "next_test": NEXT_TARGET,
        "failure_mode": "Treating source-model domain epsilon_U as observable evidence before S_static, projection kernels and boundary amplitudes are real.",
        "sector": "local_gr",
        "source_path": str(DOC_PATH),
        "next_target": NEXT_TARGET,
        "notes": "The inner 1-30 AU row gives a strong source-model epsilon_U, but it is only an input to the scorer.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    module = source_model_module()
    params = default_params(module)
    sources = source_rows()
    laws = law_rows()
    domains, grid = domain_rows_and_grid(module, params)
    static_update = static_update_rows(domains)
    blockers = blocker_update_rows()
    gates = claim_gate_rows(domains, grid)
    decisions = decision_rows()
    next_ = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(DOMAIN_LAW_CSV, laws)
    write_csv(DOMAIN_ROWS_CSV, domains)
    write_csv(MONOTONICITY_GRID_CSV, grid)
    write_csv(STATIC_UPDATE_CSV, static_update)
    write_csv(BLOCKER_UPDATE_CSV, blockers)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_)
    write_csv(STATUS_CSV, status)

    pycache = SCRIPT_DIR / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    pending_doc = f"# 4549 - Source real local-domain B_min or first projection-kernel row\n\nMarker: `{MARKER}`\n\nValidation pending.\n"
    DOC_PATH.write_text(pending_doc, encoding="utf-8")
    FORMAL_PATH.write_text(pending_doc, encoding="utf-8")

    validation = validate(sources, laws, domains, grid, static_update, gates)
    write_csv(VALIDATION_PATH, validation)

    doc = build_doc(sources, laws, domains, grid, static_update, blockers, gates, decisions, next_, validation)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4549 Source-Model Local-Domain B_min Rows

Marker: `{MARKER}`  
4549 turns `epsilon_U` from a single point anchor into finite source-model domain rows. For the existing Solar point-mass source model, monotonic `B_env(r)` on `[r_in,r_out]` gives `B_min=B_env(r_out)` and `epsilon_U=U_B(r_out)`. The inner `1-30 AU` row gives a strong numeric source-model input, but no local-GR/PPN/R10 claim is made until `S_static`, projection kernels and boundary amplitudes are supplied. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4549 Packet Integration - Source-Model Domain epsilon_U

Marker: `{PACKET_MARKER}`  
The local packet now has a concrete source-model domain epsilon row rather than only a point anchor. The live bottleneck has moved to the observable side of the scorer: `S_static`, `K_a`, and retained boundary/vector/shear amplitudes.
""",
    )

    print(f"wrote {DOC_PATH}")
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    overall = next((row for row in validation if row["validation_id"] == "VAL4549_OVERALL"), {})
    print(f"overall={overall.get('status', 'UNKNOWN')} decision={DECISION}")


if __name__ == "__main__":
    main()
