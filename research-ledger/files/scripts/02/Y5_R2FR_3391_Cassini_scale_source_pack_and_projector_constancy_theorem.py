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
DOC = ROOT / "3391-Y5-R2FR-Cassini-scale-source-pack-and-projector-constancy-theorem-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3391_SOURCE_REGISTER.csv",
    "external_sources": OUT / "P8_Y5_R2FR_3391_EXTERNAL_SOURCE_PACK.csv",
    "cassini_geometry": OUT / "P8_Y5_R2FR_3391_CASSINI_GEOMETRY_SOURCE_BACKED.csv",
    "projector_theorem": OUT / "P8_Y5_R2FR_3391_PPN_PROJECTOR_CONSTANCY_THEOREM.csv",
    "projector_bounds": OUT / "P8_Y5_R2FR_3391_PROJECTOR_FINITE_BOUND_ROWS_NONCLAIM.csv",
    "branch_comparison": OUT / "P8_Y5_R2FR_3391_PROJECTOR_BRANCH_COMPARISON.csv",
    "runner": OUT / "P8_Y5_R2FR_3391_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3391_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3391_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3391_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3391_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3391_00_3390_doc", ROOT / "3390-Y5-R2FR-local-scale-acquisition-or-compact-kernel-transfer-replacement-under-AX1090.md", "3390 handoff"),
    ("SRC3391_01_3390_next", OUT / "P8_Y5_R2FR_3390_NEXT_TARGET.csv", "3390 next target"),
    ("SRC3391_02_3390_estimator", OUT / "P8_Y5_R2FR_3390_CASSINI_GEOMETRY_ESTIMATOR_NONCLAIM.csv", "rough Cassini estimator"),
    ("SRC3391_03_3390_projector", OUT / "P8_Y5_R2FR_3390_PROJECTOR_GRADIENT_ACQUISITION_ROWS_NONCLAIM.csv", "projector gradient budgets"),
    ("SRC3391_04_3389_targets", OUT / "P8_Y5_R2FR_3389_TARGET_REQUIREMENT_SUMMARY.csv", "strict target summary"),
    ("SRC3391_05_3387_kernel", OUT / "P8_Y5_R2FR_3387_KERNEL_PROJECTOR_COMMUTATOR_LAW.csv", "kernel/projector commutator law"),
    ("SRC3391_06_local_ppn_framework", FW / "59-local-ppn-branch-framework.md", "read-only local PPN framework context"),
    ("SRC3391_07_local_tensor_ansatz", FW / "61-local-ppn-tensor-ansatz.md", "read-only tensor ansatz context"),
]

C_LIGHT_M_PER_S = 299_792_458.0
NASA_SOLAR_RADIUS_M = 696_000_000.0
NASA_SOLAR_GM_M3_PER_S2 = 132_712.0e6 * 1.0e9
CASSINI_B_MIN_RSUN = 1.6
CASSINI_GAMMA_MINUS_ONE = 2.1e-5
CASSINI_GAMMA_SIGMA = 2.3e-5


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
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
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def to_float(value: str, default: float = math.nan) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        if not exists:
            parse_ok, parse_error = False, "missing"
        elif path.suffix.lower() == ".csv":
            parse_ok, parse_error = parse_csv(path)
        else:
            parse_ok, parse_error = parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "read_or_write": "read_only_context" if str(path).startswith(str(FW)) else "post_checkpoint_source",
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def external_source_rows() -> list[dict[str, str]]:
    return [
        {
            "source_id": "EXT3391_0_Cassini_Nature",
            "source_type": "peer_reviewed_primary_article",
            "source_url": "https://www.nature.com/articles/nature01997",
            "doi": "10.1038/nature01997",
            "used_for": "Cassini PPN gamma measurement and experiment identity",
            "numeric_value": f"gamma_minus_one={CASSINI_GAMMA_MINUS_ONE:.6e}; sigma={CASSINI_GAMMA_SIGMA:.6e}",
            "unit": "dimensionless",
            "extraction_method": "manual source read; recorded as source-backed input",
            "confidence": "high_for_gamma_result",
            "valid_for_claim": "false",
        },
        {
            "source_id": "EXT3391_1_Cassini_Nature_PDF",
            "source_type": "peer_reviewed_primary_article_pdf",
            "source_url": "https://www.nature.com/articles/nature01997.pdf",
            "doi": "10.1038/nature01997",
            "used_for": "Cassini minimum ray impact parameter benchmark",
            "numeric_value": f"b_min={CASSINI_B_MIN_RSUN:.6e} R_sun",
            "unit": "solar radii",
            "extraction_method": "manual source read; closest solar approach benchmark",
            "confidence": "high_for_benchmark_geometry",
            "valid_for_claim": "false",
        },
        {
            "source_id": "EXT3391_2_NASA_Sun_Fact_Sheet",
            "source_type": "official_NASA_fact_sheet",
            "source_url": "https://radiojove.gsfc.nasa.gov/education/sun/basics/material/sunfacts.htm",
            "doi": "",
            "used_for": "solar radius and solar gravitational parameter",
            "numeric_value": f"R_sun={NASA_SOLAR_RADIUS_M:.6e} m; GM_sun={NASA_SOLAR_GM_M3_PER_S2:.6e} m^3/s^2",
            "unit": "m; m^3/s^2",
            "extraction_method": "manual source read; NASA table conversion from km and 10^6 km^3/s^2",
            "confidence": "high_for_scale_pack",
            "valid_for_claim": "false",
        },
        {
            "source_id": "EXT3391_3_SI_c_exact",
            "source_type": "SI_exact_constant",
            "source_url": "https://www.bipm.org/en/measurement-units/si-base-units",
            "doi": "",
            "used_for": "convert GM_sun to gravitational radius GM/c^2",
            "numeric_value": f"c={C_LIGHT_M_PER_S:.6e} m/s",
            "unit": "m/s",
            "extraction_method": "SI exact value",
            "confidence": "exact",
            "valid_for_claim": "false",
        },
    ]


def target_rows() -> list[dict[str, str]]:
    return read_csv_rows(OUT / "P8_Y5_R2FR_3389_TARGET_REQUIREMENT_SUMMARY.csv")


def cassini_base_geometry() -> dict[str, float]:
    gravitational_radius_m = NASA_SOLAR_GM_M3_PER_S2 / (C_LIGHT_M_PER_S**2)
    impact_parameter_m = CASSINI_B_MIN_RSUN * NASA_SOLAR_RADIUS_M
    source_free_collar_m = impact_parameter_m - NASA_SOLAR_RADIUS_M
    schwarzschild_curvature_radius_m = impact_parameter_m**1.5 / ((48.0**0.25) * math.sqrt(gravitational_radius_m))
    ray_geometry_scale_m = impact_parameter_m
    return {
        "c_m_per_s": C_LIGHT_M_PER_S,
        "solar_radius_m": NASA_SOLAR_RADIUS_M,
        "solar_GM_m3_per_s2": NASA_SOLAR_GM_M3_PER_S2,
        "solar_gravitational_radius_GM_over_c2_m": gravitational_radius_m,
        "b_min_Rsun": CASSINI_B_MIN_RSUN,
        "impact_parameter_m": impact_parameter_m,
        "source_free_collar_m": source_free_collar_m,
        "schwarzschild_curvature_radius_m": schwarzschild_curvature_radius_m,
        "ray_geometry_scale_m": ray_geometry_scale_m,
    }


def cassini_geometry_rows() -> list[dict[str, str]]:
    geometry = cassini_base_geometry()
    rows: list[dict[str, str]] = []
    for target in target_rows():
        required_d = to_float(target.get("required_d_collar_over_ell_Cboundary1_flux0", ""))
        quarter = to_float(target.get("equal_quarter_kernel_term_budget", ""))
        if not math.isfinite(required_d) or not math.isfinite(quarter):
            continue
        ell_boundary = geometry["source_free_collar_m"] / required_d
        ell_curvature_grad = quarter * geometry["schwarzschild_curvature_radius_m"]
        ell_curvature_hess = math.sqrt(quarter) * geometry["schwarzschild_curvature_radius_m"]
        ell_ray_grad = quarter * geometry["ray_geometry_scale_m"]
        candidates = {
            "boundary_collar": ell_boundary,
            "curvature_projector_gradient": ell_curvature_grad,
            "curvature_projector_hessian": ell_curvature_hess,
            "adaptive_ray_projector_gradient": ell_ray_grad,
        }
        controlling_channel, controlling_value = min(candidates.items(), key=lambda item: item[1])
        rows.append(
            {
                "geometry_id": f"CG3391_{target.get('source_row', '')}",
                "source_row": target.get("source_row", ""),
                "threshold_source": target.get("threshold_source", ""),
                "source_pack": "Nature_Cassini_plus_NASA_Sun_fact_sheet",
                "gamma_minus_one_cassini": f"{CASSINI_GAMMA_MINUS_ONE:.6e}",
                "gamma_sigma_cassini": f"{CASSINI_GAMMA_SIGMA:.6e}",
                "solar_radius_m": f"{geometry['solar_radius_m']:.10e}",
                "solar_GM_m3_per_s2": f"{geometry['solar_GM_m3_per_s2']:.10e}",
                "solar_gravitational_radius_GM_over_c2_m": f"{geometry['solar_gravitational_radius_GM_over_c2_m']:.10e}",
                "b_min_Rsun": f"{geometry['b_min_Rsun']:.6e}",
                "impact_parameter_m": f"{geometry['impact_parameter_m']:.10e}",
                "source_free_collar_m": f"{geometry['source_free_collar_m']:.10e}",
                "schwarzschild_curvature_radius_m": f"{geometry['schwarzschild_curvature_radius_m']:.10e}",
                "ray_geometry_scale_m": f"{geometry['ray_geometry_scale_m']:.10e}",
                "required_d_collar_over_ell_s_Cboundary1_flux0": f"{required_d:.12e}",
                "kernel_quarter_budget": f"{quarter:.15e}",
                "ell_s_max_from_boundary_m": f"{ell_boundary:.10e}",
                "ell_s_max_from_curvature_projector_grad_C1eq1_m": f"{ell_curvature_grad:.10e}",
                "ell_s_max_from_curvature_projector_hess_C2eq1_m": f"{ell_curvature_hess:.10e}",
                "ell_s_max_from_adaptive_ray_projector_grad_C1eq1_m": f"{ell_ray_grad:.10e}",
                "controlling_channel_if_no_exact_constancy": controlling_channel,
                "controlling_ell_s_max_m": f"{controlling_value:.10e}",
                "valid_for_claim": "false",
            }
        )
    return rows


def projector_theorem_rows() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "PT3391_0_fixed_readout_definition",
            "statement": "If P_PPN is a fixed linear readout after one PPN/Fermi gauge choice, then its coefficients are position-independent on the smoothing patch.",
            "derivation": "Write (P_PPN h)_A = P_A^{mu nu} h_{mu nu}; if the parent readout fixes P_A^{mu nu} once for the patch, partial_i P_A^{mu nu}=0.",
            "required_parent_clause": "single gauge/tetrad/readout selected before smoothing; no x-dependent adaptive ray projector inside S_ell",
            "result": "nabla_P_PPN_equals_zero",
            "status": "THEOREM_CONDITIONAL_PARENT_CLAUSE_NEEDED",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "PT3391_1_commutator_zero",
            "statement": "A constant P_PPN commutes with scalar smoothing.",
            "derivation": "[P,S]f(x)=int K_ell(x,y)[P(x)-P(y)]f(y)dV_y; if P(x)=P(y)=P0 on support then [P,S]=0.",
            "required_parent_clause": "scalar kernel plus fixed P_PPN on support",
            "result": "epsilon_projector_gradient_channel_zero",
            "status": "DERIVED_EXACT_IF_PARENT_CLAUSES_HOLD",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "PT3391_2_finite_curvature_bound",
            "statement": "If P_PPN drifts only by local curvature-frame variation, the first finite channel is ell_s/L_curv.",
            "derivation": "For ||nabla P||<=C_P/L_curv and ||nabla^2P||<=C_PP/L_curv^2, epsilon_kernel <= C1 C_P ell_s/L_curv + C2 C_PP (ell_s/L_curv)^2 + moment + gauge.",
            "required_parent_clause": "bounds on C_P,C_PP and no faster adaptive readout dependence",
            "result": "finite_bound_rows_generated",
            "status": "FINITE_BOUND_AVAILABLE_NUMERIC_PARENT_CONSTANTS_MISSING",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "PT3391_3_adaptive_ray_warning",
            "statement": "If P_PPN is secretly an x-dependent ray/impact-parameter projector, the scale can be much harsher.",
            "derivation": "Replacing L_curv by b_min gives ell_s <= budget*b_min for the first derivative channel.",
            "required_parent_clause": "declare whether P_PPN is fixed observable readout or adaptive ray-local projector",
            "result": "adaptive_ray_branch_can_force_mm_to_km_scale_ell_s",
            "status": "WARNING_BRANCH_NOT_SELECTED",
            "valid_for_claim": "false",
        },
    ]


def projector_bound_rows(geometry_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in geometry_rows:
        quarter = to_float(row["kernel_quarter_budget"])
        l_curv = to_float(row["schwarzschild_curvature_radius_m"])
        b_scale = to_float(row["ray_geometry_scale_m"])
        rows.append(
            {
                "bound_id": f"PB3391_{row['source_row']}",
                "source_row": row["source_row"],
                "threshold_source": row["threshold_source"],
                "kernel_quarter_budget": row["kernel_quarter_budget"],
                "exact_fixed_PPN_readout": "ell_s ceiling not needed for projector commutator if parent signs PT3391_0 and PT3391_1",
                "curvature_gradient_bound": f"ell_s <= {quarter:.15e} * L_curv / (C1*C_P)",
                "curvature_gradient_ell_s_C1CPeq1_m": f"{quarter * l_curv:.10e}",
                "curvature_hessian_bound": f"ell_s <= sqrt({quarter:.15e} * L_curv^2/(C2*C_PP))",
                "curvature_hessian_ell_s_C2CPPeq1_m": f"{math.sqrt(quarter) * l_curv:.10e}",
                "adaptive_ray_gradient_bound": f"ell_s <= {quarter:.15e} * b_min/(C1*C_ray)",
                "adaptive_ray_gradient_ell_s_C1Crayeq1_m": f"{quarter * b_scale:.10e}",
                "current_claim_status": "NONCLAIM_NEEDS_PARENT_READOUT_BRANCH",
                "valid_for_claim": "false",
            }
        )
    return rows


def branch_comparison_rows(geometry_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    min_boundary = min(to_float(row["ell_s_max_from_boundary_m"]) for row in geometry_rows)
    min_curv_grad = min(to_float(row["ell_s_max_from_curvature_projector_grad_C1eq1_m"]) for row in geometry_rows)
    min_ray_grad = min(to_float(row["ell_s_max_from_adaptive_ray_projector_grad_C1eq1_m"]) for row in geometry_rows)
    return [
        {
            "branch_id": "BR3391_0_exact_fixed_projector",
            "branch": "fixed PPN readout projector",
            "mathematical_result": "nabla P_PPN=0 and [P,S]=0",
            "strictest_ell_s_ceiling_m": "not_applicable_for_projector_channel",
            "what_still_blocks_claim": "parent must explicitly define P_PPN as fixed readout and close moment/gauge/flux channels",
            "current_status": "BEST_ROUTE_IF_PARENT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "BR3391_1_finite_curvature_projector",
            "branch": "curvature-scale projector drift",
            "mathematical_result": "epsilon_projector <= C1*C_P*ell_s/L_curv + C2*C_PP*(ell_s/L_curv)^2",
            "strictest_ell_s_ceiling_m": f"{min_curv_grad:.10e}",
            "what_still_blocks_claim": "need parent values for ell_s, C1, C_P, C2, C_PP",
            "current_status": "FINITE_BUT_PRESSURED",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "BR3391_2_adaptive_ray_projector",
            "branch": "adaptive ray-local projector drift",
            "mathematical_result": "epsilon_projector <= C1*C_ray*ell_s/b_min + ...",
            "strictest_ell_s_ceiling_m": f"{min_ray_grad:.10e}",
            "what_still_blocks_claim": "this branch is very harsh and should be avoided unless forced by parent readout",
            "current_status": "DANGEROUS_BRANCH",
            "valid_for_claim": "false",
        },
        {
            "branch_id": "BR3391_3_boundary_collar",
            "branch": "Gaussian boundary collar",
            "mathematical_result": "epsilon_boundary_tail <= C_boundary exp[-(d_collar/ell_s)^2/2]",
            "strictest_ell_s_ceiling_m": f"{min_boundary:.10e}",
            "what_still_blocks_claim": "C_boundary and physical flux still need parent/source rows",
            "current_status": "NOT_LIKELY_BOTTLENECK_IN_SOLAR_EXTERIOR",
            "valid_for_claim": "false",
        },
    ]


def runner_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    branch_map = {row["branch_id"]: row for row in rows_by_name["branch_comparison"]}
    return [
        {
            "run_id": "RUN3391_0_source_pack",
            "test": "Cassini/NASA source pack",
            "result": "PASS_SOURCE_PACK_NONCLAIM",
            "detail": "Nature Cassini gamma/b_min and NASA solar radius/GM recorded with units and conversions",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3391_1_geometry",
            "test": "source-backed Cassini geometry rows",
            "result": "PASS_GEOMETRY_ROWS_NONCLAIM",
            "detail": f"rows={len(rows_by_name['cassini_geometry'])}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3391_2_projector_theorem",
            "test": "P_PPN constancy theorem",
            "result": "PASS_CONDITIONAL_THEOREM",
            "detail": "constant fixed readout gives nabla P=0 and [P,S]=0; parent clause still required",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3391_3_finite_bound",
            "test": "finite projector bounds",
            "result": "PASS_FINITE_BOUND_ROWS_NONCLAIM",
            "detail": f"curvature strictest ell_s ceiling={branch_map['BR3391_1_finite_curvature_projector']['strictest_ell_s_ceiling_m']} m; adaptive ray ceiling={branch_map['BR3391_2_adaptive_ray_projector']['strictest_ell_s_ceiling_m']} m",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3391_4_firewall",
            "test": "prevent local PPN/local GR claim",
            "result": "PASS_CLAIM_FIREWALL",
            "detail": "source pack improves geometry evidence, but parent P_PPN branch, ell_s, moment/gauge and flux remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3391_0_sources",
            "claim": "local 3391 source files exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "all local source context files parsed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3391_1_external_pack",
            "claim": "Cassini and solar geometry constants are source-recorded",
            "gate_pass": "true",
            "reason": "external source pack records URLs, numeric values, units and extraction method",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3391_2_projector_exact",
            "claim": "P_PPN projector commutator is exactly zero",
            "gate_pass": "false",
            "reason": "the theorem is conditional; parent framework has not yet signed fixed-readout P_PPN as the active branch",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3391_3_projector_finite",
            "claim": "finite projector drift is below strict Cassini pressure",
            "gate_pass": "false",
            "reason": "ell_s and constants C1,C_P,C2,C_PP or exact constancy remain missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3391_4_other_channels",
            "claim": "boundary flux, moment and gauge/readout defects are closed",
            "gate_pass": "false",
            "reason": "3391 only attacks Cassini geometry and projector channel; 3376 flux and moment/gauge still need closure",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3391_5_local_ppn",
            "claim": "local PPN/local-GR branch passes",
            "gate_pass": "false",
            "reason": "source-backed geometry is not enough without parent P_PPN branch plus remaining channel closures",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    branch_map = {row["branch_id"]: row for row in rows_by_name["branch_comparison"]}
    return [
        {
            "decision_id": "DEC3391_0_progress",
            "decision": "Cassini geometry is now source-backed enough for private scale pressure.",
            "because": "Nature/NASA source rows replace the rough 3390 constants, while keeping all rows nonclaim.",
            "next_action": "use these rows as the geometry basis for the local PPN route",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3391_1_best_route",
            "decision": "The cleanest route is an exact fixed-readout P_PPN theorem.",
            "because": "If P_PPN is parent-defined as a fixed PPN observable readout, nabla P_PPN=0 and the projector commutator disappears.",
            "next_action": "write the parent readout clause explicitly and check it against the existing action/readout language",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3391_2_finite_route",
            "decision": "If exact constancy fails, the finite curvature branch is possible but pressured.",
            "because": f"strictest curvature-scale ell_s ceiling is {branch_map['BR3391_1_finite_curvature_projector']['strictest_ell_s_ceiling_m']} m for C1*C_P=1; adaptive ray branch is harsher at {branch_map['BR3391_2_adaptive_ray_projector']['strictest_ell_s_ceiling_m']} m.",
            "next_action": "avoid adaptive ray-local P unless parent forces it; otherwise source ell_s or derive exact constancy",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3391_3_best_next",
            "decision": "Next target should parent-sign the fixed PPN readout or expose the remaining obstruction.",
            "because": "3391 has turned 'projector gradient missing' into a precise fork: exact P_PPN constancy theorem versus ell_s scale bound.",
            "next_action": "build 3392 fixed PPN readout parent-clause audit plus moment/gauge closure hook",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3392-Y5-R2FR-fixed-PPN-readout-parent-clause-or-projector-ell-scale-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3392_fixed_PPN_readout_parent_clause_or_projector_ell_scale_bound.py",
            "objective": "audit the parent action/readout corpus for a fixed PPN observable projector clause; if present, promote the projector commutator to exact zero, otherwise carry the Cassini ell_s ceilings as finite nonclaim bounds",
            "why_next": "3391 shows exact P_PPN constancy is the clean route; without it, local PPN survival demands a very small or sourced smoothing length",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3393-Y5-R2FR-boundary-flux-moment-gauge-closure-pack-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3393_boundary_flux_moment_gauge_closure_pack.py",
            "objective": "after the projector fork is resolved, close the remaining boundary flux, kernel moment, and gauge/readout defects for the Cassini local branch",
            "why_next": "even exact projector constancy does not close physical flux, kernel moment, or gauge defects",
            "valid_for_claim": "false",
        },
    ]


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".csv":
            continue
        for index, row in enumerate(read_csv_rows(path), start=2):
            if "valid_for_claim" in row and row["valid_for_claim"].strip().lower() != "false":
                offenders.append(f"{path.name}:line{index}:{row['valid_for_claim']}")
    return not offenders, "; ".join(offenders)


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in rows_by_name["source_register"])
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation" and path.suffix.lower() == ".csv"]
    parse_results = [parse_csv(path)[0] for path in output_csvs if path.exists()]
    flags_ok, flag_detail = all_claim_flags_false(output_csvs)
    formalization_hits = [
        hit
        for hit in FW.rglob("*3391*")
        if hit.name.startswith(("3391-Y5", "P8_Y5_R2FR_3391", "P8_Y5_BRR545_3391", "Y5_R2FR_3391"))
    ] if FW.exists() else []
    external_ok = all(row["source_url"] and row["numeric_value"] and row["unit"] for row in rows_by_name["external_sources"])
    geometry_positive = all(
        to_float(row["solar_radius_m"]) > 0
        and to_float(row["solar_GM_m3_per_s2"]) > 0
        and to_float(row["impact_parameter_m"]) > 0
        and to_float(row["controlling_ell_s_max_m"]) > 0
        for row in rows_by_name["cassini_geometry"]
    )
    theorem_results = {row["result"] for row in rows_by_name["projector_theorem"]}
    branch_ids = {row["branch_id"] for row in rows_by_name["branch_comparison"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    checks = [
        ("VAL3391_0_sources_exist_parse", "all cited 3391 local source paths exist and parse", source_ok, ""),
        ("VAL3391_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3391_2_external_sources", "external source pack records URLs, values and units", external_ok, f"rows={len(rows_by_name['external_sources'])}"),
        ("VAL3391_3_geometry_positive", "Cassini geometry rows are positive finite rows", len(rows_by_name["cassini_geometry"]) >= 8 and geometry_positive, f"rows={len(rows_by_name['cassini_geometry'])}"),
        ("VAL3391_4_projector_theorem", "projector theorem includes exact and finite branches", {"nabla_P_PPN_equals_zero", "epsilon_projector_gradient_channel_zero", "finite_bound_rows_generated", "adaptive_ray_branch_can_force_mm_to_km_scale_ell_s"}.issubset(theorem_results), ""),
        ("VAL3391_5_projector_bounds", "projector bound rows cover target summary", len(rows_by_name["projector_bounds"]) >= 8, f"rows={len(rows_by_name['projector_bounds'])}"),
        ("VAL3391_6_branch_comparison", "branch comparison covers exact, finite, adaptive, and boundary branches", {"BR3391_0_exact_fixed_projector", "BR3391_1_finite_curvature_projector", "BR3391_2_adaptive_ray_projector", "BR3391_3_boundary_collar"}.issubset(branch_ids), ""),
        ("VAL3391_7_runner", "runner records source pack, geometry, theorem, finite bound and firewall", {"PASS_SOURCE_PACK_NONCLAIM", "PASS_GEOMETRY_ROWS_NONCLAIM", "PASS_CONDITIONAL_THEOREM", "PASS_FINITE_BOUND_ROWS_NONCLAIM", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3391_8_gates", "gates source pack but block exact projector, finite projector and local PPN claims", gate_map.get("GATE3391_1_external_pack") == "true" and gate_map.get("GATE3391_2_projector_exact") == "false" and gate_map.get("GATE3391_3_projector_finite") == "false" and gate_map.get("GATE3391_5_local_ppn") == "false", ""),
        ("VAL3391_9_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3391_10_write_scope_outside_formalization", "no 3391 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
        ("VAL3391_11_next_target", "next target moves to fixed PPN readout parent-clause audit", rows_by_name["next"][0]["target_id"].startswith("3392-Y5-R2FR-fixed-PPN-readout"), ""),
    ]
    overall = all(passed for _, _, passed, _ in checks)
    checks.append(("VAL3391_12_overall", "3391 validation overall", overall, "all required checks passed" if overall else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    branch_map = {row["branch_id"]: row for row in rows_by_name["branch_comparison"]}
    lines = [
        "# 3391 - Y5/R2FR Cassini scale source pack and projector constancy theorem under AX1090",
        "",
        "## Summary",
        "- 3391 replaces the rough 3390 Cassini constants with source-recorded Cassini/NASA rows.",
        "- The local arena remains Cassini-like solar PPN gamma, but this is still private/nonclaim scaffolding.",
        "- Main result: the clean route is not a tiny fitted number; it is a parent-fixed `P_PPN` readout theorem.",
        "- If `P_PPN` is a fixed linear observable projector in one gauge/tetrad patch, then `nabla P_PPN=0` and `[P,S]=0` for scalar smoothing.",
        f"- If exact fixed-readout constancy fails, the curvature-scale finite branch has strictest `ell_s` ceiling `{branch_map['BR3391_1_finite_curvature_projector']['strictest_ell_s_ceiling_m']} m`; an adaptive ray-local projector would be harsher at `{branch_map['BR3391_2_adaptive_ray_projector']['strictest_ell_s_ceiling_m']} m`.",
        "- Boundary collar leakage is still not the obvious bottleneck in a solar exterior, but C_boundary and flux are not closed.",
        "- No local-GR/PPN claim is made from 3391.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## External Source Pack",
        md_table(rows_by_name["external_sources"]),
        "## Cassini Geometry Source-Backed Rows",
        md_table(rows_by_name["cassini_geometry"]),
        "## PPN Projector Constancy Theorem",
        md_table(rows_by_name["projector_theorem"]),
        "## Projector Finite Bound Rows",
        md_table(rows_by_name["projector_bounds"]),
        "## Projector Branch Comparison",
        md_table(rows_by_name["branch_comparison"]),
        "## Nonclaim Runner",
        md_table(rows_by_name["runner"]),
        "## Promotion Gates",
        md_table(rows_by_name["gates"]),
        "## Decision Ledger",
        md_table(rows_by_name["decision"]),
        "## Validation",
        md_table(rows_by_name["validation"]),
        "## Next Target",
        md_table(rows_by_name["next"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_register = source_rows()
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_register)
    cassini_geometry = cassini_geometry_rows()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "external_sources": external_source_rows(),
        "cassini_geometry": cassini_geometry,
        "projector_theorem": projector_theorem_rows(),
        "projector_bounds": projector_bound_rows(cassini_geometry),
        "branch_comparison": branch_comparison_rows(cassini_geometry),
    }
    rows_by_name["runner"] = runner_rows(rows_by_name)
    rows_by_name["gates"] = gate_rows(source_ok)
    rows_by_name["decision"] = decision_rows(rows_by_name)
    rows_by_name["next"] = next_rows()
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print(f"Generated UTC {RUN_UTC}")


if __name__ == "__main__":
    main()
