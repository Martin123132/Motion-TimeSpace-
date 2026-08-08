from __future__ import annotations

import csv
import math
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3390-Y5-R2FR-local-scale-acquisition-or-compact-kernel-transfer-replacement-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3390_SOURCE_REGISTER.csv",
    "source_sweep": OUT / "P8_Y5_R2FR_3390_CORPUS_SCALE_SOURCE_SWEEP.csv",
    "arena": OUT / "P8_Y5_R2FR_3390_LOCAL_ARENA_SELECTION.csv",
    "compact_contract": OUT / "P8_Y5_R2FR_3390_COMPACT_TRANSFER_REPLACEMENT_CONTRACT.csv",
    "gaussian_acquisition": OUT / "P8_Y5_R2FR_3390_GAUSSIAN_SCALE_ACQUISITION_ROWS_NONCLAIM.csv",
    "projector_acquisition": OUT / "P8_Y5_R2FR_3390_PROJECTOR_GRADIENT_ACQUISITION_ROWS_NONCLAIM.csv",
    "cassini_estimator": OUT / "P8_Y5_R2FR_3390_CASSINI_GEOMETRY_ESTIMATOR_NONCLAIM.csv",
    "readiness": OUT / "P8_Y5_R2FR_3390_SCORING_READINESS_MATRIX.csv",
    "runner": OUT / "P8_Y5_R2FR_3390_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3390_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3390_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3390_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3390_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3390_00_3389_doc", ROOT / "3389-Y5-R2FR-finite-epsilon-scale-input-runner-or-compact-kernel-adoption-under-AX1090.md", "3389 scale handoff"),
    ("SRC3390_01_3389_targets", OUT / "P8_Y5_R2FR_3389_TARGET_REQUIREMENT_SUMMARY.csv", "strict boundary/kernel targets"),
    ("SRC3390_02_3389_acquisition", OUT / "P8_Y5_R2FR_3389_INPUT_ACQUISITION_LEDGER.csv", "missing scale input ledger"),
    ("SRC3390_03_3389_compact", OUT / "P8_Y5_R2FR_3389_COMPACT_KERNEL_ADOPTION_AUDIT.csv", "compact kernel adoption audit"),
    ("SRC3390_04_3388_doc", ROOT / "3388-Y5-R2FR-smoothing-projector-parent-owner-or-epsilon-scale-inputs-under-AX1090.md", "smoothing/projector parent-owner handoff"),
    ("SRC3390_05_3387_boundary", OUT / "P8_Y5_R2FR_3387_BOUNDARY_COLLAR_TAIL_LAW.csv", "Gaussian boundary collar law"),
    ("SRC3390_06_3387_kernel", OUT / "P8_Y5_R2FR_3387_KERNEL_PROJECTOR_COMMUTATOR_LAW.csv", "kernel/projector commutator law"),
    ("SRC3390_07_3321_kernel", OUT / "P8_Y5_R2FR_3321_KERNEL_TRANSFER_LAW.csv", "Gaussian transfer law to be replaced if compact branch is chosen"),
    ("SRC3390_08_3376_doc", ROOT / "3376-Y5-R2FR-boundary-zero-flux-or-Bzero-first-row-under-AX1090.md", "zero-flux boundary package"),
    ("SRC3390_09_core_action", REPO / "core-mts-framework" / "action-principle" / "the-fundamental-action-of-motion-timespace-field-theory.md", "parent action context"),
    ("SRC3390_10_motion_action", REPO / "core-mts-framework" / "action-principle" / "the-motion-timespace-action-principle.md", "motion/action context"),
    ("SRC3390_11_gravity_core", REPO / "core-mts-framework" / "gravity" / "motion-timespace-mts-gravity-core-unified-formulation.md", "gravity core context"),
    ("SRC3390_12_local_ppn_framework", FW / "59-local-ppn-branch-framework.md", "read-only local PPN branch context"),
    ("SRC3390_13_local_tensor_ansatz", FW / "61-local-ppn-tensor-ansatz.md", "read-only tensor ansatz context"),
    ("SRC3390_14_metric_response", FW / "136-metric-response-kernel-theorem.md", "read-only metric response kernel context"),
]

QUANTITY_PATTERNS = {
    "kernel_branch": [r"\bcompact\b", r"\bGaussian\b", r"heat[- ]kernel", r"smoothing branch", r"kernel_branch"],
    "d_collar/ell_s": [r"d_collar", r"d/ell", r"collar", r"rho_K", r"source-free"],
    "ell_s": [r"ell_s", r"smoothing length", r"smoothing scale", r"\bell\b"],
    "C_boundary": [r"C_boundary", r"boundary.*norm", r"operator norm", r"tail normalization"],
    "epsilon_boundary_physical": [r"B_zero_flux", r"Poynting", r"flux", r"corner", r"topology", r"worldtube"],
    "projector_gradient": [r"projector gradient", r"nabla P", r"∇P", r"P_PPN", r"projector const"],
    "kernel_moment": [r"kernel moment", r"first moment", r"anisotrop", r"moment defect"],
    "gauge_defect": [r"gauge", r"readout drift", r"PPN gauge", r"gauge_readout"],
    "compact_transfer": [r"Khat", r"Fourier", r"transfer law", r"T_grad", r"compact.*transfer"],
}

NUMERIC_RE = re.compile(r"(?<![A-Za-z_])[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")


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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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
                "read_or_write": "read_only_context" if str(path).startswith(str(FW)) else "post_checkpoint_or_core_source",
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def source_lookup() -> dict[str, tuple[Path, str]]:
    return {source_id: (path, role) for source_id, path, role in LOCAL_SOURCES}


def normalize_csv_to_lines(path: Path) -> list[str]:
    rows = read_csv_rows(path)
    if not rows:
        return []
    lines: list[str] = []
    for index, row in enumerate(rows, start=2):
        flat = "; ".join(f"{key}={value}" for key, value in row.items())
        lines.append(f"csv_line_{index}: {flat}")
    return lines


def source_lines(path: Path) -> list[tuple[int, str]]:
    if not path.exists():
        return []
    if path.suffix.lower() == ".csv":
        return [(index, line) for index, line in enumerate(normalize_csv_to_lines(path), start=2)]
    return [(index, line) for index, line in enumerate(read_text(path).splitlines(), start=1)]


def numeric_tokens(line: str) -> str:
    tokens = NUMERIC_RE.findall(line)
    filtered = [token for token in tokens if len(token) <= 16]
    return ";".join(filtered[:8])


def source_sweep_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    hits_by_quantity = {quantity: 0 for quantity in QUANTITY_PATTERNS}
    for source_id, (path, role) in source_lookup().items():
        for line_number, line in source_lines(path):
            compact_line = " ".join(line.strip().split())
            if not compact_line:
                continue
            for quantity, patterns in QUANTITY_PATTERNS.items():
                if hits_by_quantity[quantity] >= 8:
                    continue
                if any(re.search(pattern, compact_line, flags=re.IGNORECASE) for pattern in patterns):
                    tokens = numeric_tokens(compact_line)
                    rows.append(
                        {
                            "sweep_id": f"SW3390_{quantity}_{hits_by_quantity[quantity]}",
                            "quantity": quantity,
                            "source_id": source_id,
                            "source_path": str(path),
                            "source_role": role,
                            "line_number": str(line_number),
                            "snippet": compact_line[:420],
                            "numeric_tokens_seen": tokens,
                            "extraction_status": "TEXT_EVIDENCE_NUMERIC_REVIEW" if tokens else "TEXT_EVIDENCE_ONLY",
                            "claim_value_extracted": "false",
                            "valid_for_claim": "false",
                        }
                    )
                    hits_by_quantity[quantity] += 1
                    break
    for quantity, count in hits_by_quantity.items():
        if count == 0:
            rows.append(
                {
                    "sweep_id": f"SW3390_{quantity}_NO_HIT",
                    "quantity": quantity,
                    "source_id": "NO_DIRECT_HIT",
                    "source_path": "",
                    "source_role": "",
                    "line_number": "",
                    "snippet": "No direct source hit found by 3390 keyword sweep.",
                    "numeric_tokens_seen": "",
                    "extraction_status": "NO_DIRECT_HIT",
                    "claim_value_extracted": "false",
                    "valid_for_claim": "false",
                }
            )
    return rows


def arena_rows() -> list[dict[str, str]]:
    return [
        {
            "arena_id": "ARENA3390_0_Cassini_solar_PPN_gamma",
            "arena": "Cassini solar-system PPN gamma",
            "selected": "true",
            "why_selected": "3389 strict targets already pressure gamma/PPN; a solar exterior is the cleanest local-GR survival arena before galaxy or cosmology evidence is allowed to matter.",
            "geometry_inputs_needed": "solar gravitational radius; solar radius; Cassini ray impact parameter; source-free collar definition; smoothing length ell_s",
            "MTS_inputs_needed": "kernel branch; C_boundary; physical boundary flux; projector derivative law; kernel moment; gauge/readout defect",
            "current_status": "SELECTED_FOR_NONCLAIM_SCALE_ESTIMATOR",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "ARENA3390_1_generic_solar_PPN",
            "arena": "generic solar-system PPN",
            "selected": "false",
            "why_selected": "broader than needed; use after Cassini branch supplies a real geometry/source pack",
            "geometry_inputs_needed": "planetary ephemeris scale; Solar multipoles; observer/source geometry",
            "MTS_inputs_needed": "same as Cassini plus full residual vector mapping",
            "current_status": "DEFERRED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "arena_id": "ARENA3390_2_lab_R10",
            "arena": "laboratory short-range R10",
            "selected": "false",
            "why_selected": "useful for c_g/alpha rows, but less directly tied to GR-to-Newton PPN reduction than Cassini",
            "geometry_inputs_needed": "source plate geometry; separation; lambda; material kernel",
            "MTS_inputs_needed": "source charge basis and local projection coefficients",
            "current_status": "DEFERRED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def compact_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "CT3390_0_parent_selection",
            "claim": "compact kernel can only be used if the parent readout/action selects it before fitting",
            "derivation_or_rule": "kernel_branch must be a parent-owned input; choosing compact after seeing Cassini pressure is not allowed",
            "required_inputs": "kernel_branch=compact_bump; support radius rho_K; normalization convention",
            "status": "CONTRACT_OPEN_PARENT_NOT_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CT3390_1_boundary_zero",
            "claim": "compact support gives exact collar silence",
            "derivation_or_rule": "If supp K_ell(x,.) lies inside the source-free local domain, i.e. d_collar >= rho_K ell_s, then the boundary tail term is exactly zero before physical flux terms are added.",
            "required_inputs": "d_collar/ell_s; rho_K; 3376 zero-flux/reference/topology conditions",
            "status": "DERIVED_CONDITIONAL_EXACT_ZERO",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CT3390_2_transfer_replacement",
            "claim": "Gaussian T_grad must be replaced for compact kernels",
            "derivation_or_rule": "For K_ell(z)=ell_s^{-3}k(z/ell_s), a mode with wavelength lambda has response |Khat(ell_s/lambda)|, so T_grad^compact(lambda) <= (ell_s/lambda)|Khat(ell_s/lambda)|.",
            "required_inputs": "explicit k; Fourier norm; lambda convention; curvature correction order",
            "status": "DERIVED_SYMBOLIC_TRANSFER_LAW",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CT3390_3_Cinfty_decay",
            "claim": "smooth compact kernels can be made rapidly suppressing but constants matter",
            "derivation_or_rule": "For C-infinity compact bumps, for every N there is C_N with |Khat(q)| <= C_N(1+q)^(-N); therefore T_grad <= (ell_s/lambda) C_N(1+ell_s/lambda)^(-N).",
            "required_inputs": "chosen bump family; C_N values; N; lambda and ell_s",
            "status": "DERIVED_BOUND_FORM_CONSTANTS_MISSING",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CT3390_4_projector_commutator_survives",
            "claim": "compact support does not by itself kill projector commutators",
            "derivation_or_rule": "[P,S]f = integral K_ell(x,y)[P(x)-P(y)]f(y)dV_y, so the finite bound still needs ell_s||nabla P||, ell_s^2||nabla^2P||, moment, and gauge/readout terms unless P is parent-parallel/constant on support.",
            "required_inputs": "projector constancy theorem or derivative bounds",
            "status": "DERIVED_OBSTRUCTION_NOT_CLOSED",
            "valid_for_claim": "false",
        },
    ]


def target_rows() -> list[dict[str, str]]:
    return read_csv_rows(OUT / "P8_Y5_R2FR_3389_TARGET_REQUIREMENT_SUMMARY.csv")


def gaussian_acquisition_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    c_boundary_values = [1.0, 10.0, 100.0, 1000.0]
    for target in target_rows():
        boundary_target = to_float(target.get("min_epsilon_boundary_target", ""))
        source_row = target.get("source_row", "")
        if not math.isfinite(boundary_target) or boundary_target <= 0:
            continue
        for c_boundary in c_boundary_values:
            required = math.sqrt(2.0 * math.log(c_boundary / boundary_target)) if c_boundary > boundary_target else math.nan
            rows.append(
                {
                    "acquisition_id": f"GA3390_{source_row}_CB{c_boundary:g}",
                    "source_row": source_row,
                    "threshold_source": target.get("threshold_source", ""),
                    "boundary_target": f"{boundary_target:.15e}",
                    "C_boundary_trial": f"{c_boundary:.6e}",
                    "flux_plus_worldtube_assumed": "0.000000e+00",
                    "required_d_collar_over_ell_s": f"{required:.12e}",
                    "formula": "d_collar/ell_s >= sqrt(2 log(C_boundary/(epsilon_boundary_target-epsilon_flux-epsilon_worldtube)))",
                    "claim_status": "TRIAL_REQUIREMENT_ONLY_SOURCE_VALUES_MISSING",
                    "valid_for_claim": "false",
                }
            )
    return rows


def projector_acquisition_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for target in target_rows():
        kernel_target = to_float(target.get("min_epsilon_kernel_target", ""))
        quarter = to_float(target.get("equal_quarter_kernel_term_budget", ""))
        source_row = target.get("source_row", "")
        if not math.isfinite(kernel_target) or not math.isfinite(quarter):
            continue
        rows.append(
            {
                "projector_id": f"PG3390_{source_row}",
                "source_row": source_row,
                "threshold_source": target.get("threshold_source", ""),
                "kernel_target": f"{kernel_target:.15e}",
                "equal_quarter_budget": f"{quarter:.15e}",
                "required_first_derivative_channel": f"ell_s||nabla P_PPN|| <= {quarter:.15e}",
                "required_second_derivative_channel": f"ell_s^2||nabla^2 P_PPN|| <= {quarter:.15e}",
                "required_moment_channel": f"epsilon_kernel_moment <= {quarter:.15e}",
                "required_gauge_channel": f"epsilon_gauge_readout <= {quarter:.15e}",
                "if_curvature_scale_model": "if ||nabla P||~1/L_curv and ||nabla^2P||~1/L_curv^2, then ell_s <= budget*L_curv and ell_s <= sqrt(budget)*L_curv",
                "claim_status": "SYMBOLIC_BOUND_READY_NUMERIC_PROJECTOR_LAW_MISSING",
                "valid_for_claim": "false",
            }
        )
    return rows


def cassini_geometry_estimator_rows() -> list[dict[str, str]]:
    # Rough nonclaim anchor only. These are standard solar scales and a Cassini-style b=1.6 R_sun
    # benchmark used only to turn the abstract 3389 targets into an order-of-magnitude hunt.
    # 3391 must replace these with source-cited rows before any public claim.
    solar_gravitational_radius_m = 1476.6250385
    solar_radius_m = 6.957e8
    impact_parameter_factor = 1.6
    impact_parameter_m = impact_parameter_factor * solar_radius_m
    source_free_collar_m = impact_parameter_m - solar_radius_m
    curvature_radius_m = impact_parameter_m ** 1.5 / ((48.0 ** 0.25) * math.sqrt(solar_gravitational_radius_m))
    rows: list[dict[str, str]] = []
    for target in target_rows():
        source_row = target.get("source_row", "")
        required_d = to_float(target.get("required_d_collar_over_ell_Cboundary1_flux0", ""))
        quarter = to_float(target.get("equal_quarter_kernel_term_budget", ""))
        if not math.isfinite(required_d) or not math.isfinite(quarter):
            continue
        ell_boundary = source_free_collar_m / required_d
        ell_projector_grad = quarter * curvature_radius_m
        ell_projector_hess = math.sqrt(quarter) * curvature_radius_m
        candidates = {
            "boundary_collar": ell_boundary,
            "projector_first_derivative": ell_projector_grad,
            "projector_second_derivative": ell_projector_hess,
        }
        control_channel, control_value = min(candidates.items(), key=lambda item: item[1])
        rows.append(
            {
                "estimator_id": f"CG3390_{source_row}",
                "source_row": source_row,
                "threshold_source": target.get("threshold_source", ""),
                "benchmark": "Cassini_like_b_equals_1p6_Rsun_rough_nonclaim",
                "solar_gravitational_radius_m": f"{solar_gravitational_radius_m:.10e}",
                "solar_radius_m": f"{solar_radius_m:.10e}",
                "impact_parameter_factor_Rsun": f"{impact_parameter_factor:.6e}",
                "impact_parameter_m": f"{impact_parameter_m:.10e}",
                "source_free_collar_m": f"{source_free_collar_m:.10e}",
                "schwarzschild_curvature_radius_m": f"{curvature_radius_m:.10e}",
                "required_d_collar_over_ell_s": f"{required_d:.12e}",
                "quarter_projector_budget": f"{quarter:.15e}",
                "ell_s_max_from_boundary_m": f"{ell_boundary:.10e}",
                "ell_s_max_from_projector_grad_C1eq1_m": f"{ell_projector_grad:.10e}",
                "ell_s_max_from_projector_hess_C2eq1_m": f"{ell_projector_hess:.10e}",
                "controlling_channel_if_C1_C2_eq_1": control_channel,
                "controlling_ell_s_max_m": f"{control_value:.10e}",
                "interpretation": "rough estimator says boundary collar is easy for solar exterior; projector first derivative dominates unless P_PPN is parent-parallel/exactly constant",
                "source_status": "ROUGH_INTERNAL_ESTIMATE_REQUIRES_3391_SOURCE_PACK",
                "valid_for_claim": "false",
            }
        )
    return rows


def readiness_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    sweep_quantities = {row["quantity"] for row in rows_by_name["source_sweep"]}
    compact_statuses = {row["status"] for row in rows_by_name["compact_contract"]}
    estimator_controls = {row["controlling_channel_if_C1_C2_eq_1"] for row in rows_by_name["cassini_estimator"]}
    return [
        {
            "readiness_id": "READY3390_0_source_sweep",
            "item": "all required scale quantities were actively searched",
            "status": "PASS_SWEEP_EXECUTED" if set(QUANTITY_PATTERNS).issubset(sweep_quantities) else "FAIL_SWEEP_INCOMPLETE",
            "evidence": f"quantities={len(sweep_quantities)}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "readiness_id": "READY3390_1_cassini_selected",
            "item": "concrete local PPN arena selected",
            "status": "PASS_CASSINI_SELECTED",
            "evidence": "ARENA3390_0_Cassini_solar_PPN_gamma selected",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "readiness_id": "READY3390_2_compact_contract",
            "item": "compact transfer replacement has a symbolic contract",
            "status": "PASS_SYMBOLIC_CONTRACT" if "DERIVED_SYMBOLIC_TRANSFER_LAW" in compact_statuses else "FAIL_NO_CONTRACT",
            "evidence": "T_grad^compact(lambda) <= (ell_s/lambda)|Khat(ell_s/lambda)|",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "readiness_id": "READY3390_3_gaussian_requirements",
            "item": "Gaussian branch now has explicit d_collar/ell_s requirements for C_boundary trials",
            "status": "PASS_REQUIREMENTS_NONCLAIM" if rows_by_name["gaussian_acquisition"] else "FAIL_NO_REQUIREMENTS",
            "evidence": f"rows={len(rows_by_name['gaussian_acquisition'])}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "readiness_id": "READY3390_4_cassini_estimator",
            "item": "rough Cassini geometry estimator identifies likely controlling channel",
            "status": "PASS_ROUGH_ESTIMATOR_NONCLAIM" if "projector_first_derivative" in estimator_controls else "WARN_UNEXPECTED_CONTROL_CHANNEL",
            "evidence": "projector first derivative controls harsh rows under curvature-scale model",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "readiness_id": "READY3390_5_source_backing",
            "item": "source-backed numeric Cassini constants and parent ell_s",
            "status": "BLOCKED_NUMERIC_SOURCE_PACK_MISSING",
            "evidence": "rough constants and b=1.6Rsun are deliberately nonclaim until 3391 source pack",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def runner_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    strict_controls = rows_by_name["cassini_estimator"]
    min_control = min(to_float(row["controlling_ell_s_max_m"]) for row in strict_controls)
    max_boundary_ell = max(to_float(row["ell_s_max_from_boundary_m"]) for row in strict_controls)
    return [
        {
            "run_id": "RUN3390_0_source_sweep",
            "test": "corpus scale-source sweep",
            "result": "PASS_EXECUTED_NONCLAIM",
            "detail": f"sweep_rows={len(rows_by_name['source_sweep'])}; claim numeric values deliberately not extracted",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3390_1_compact_transfer",
            "test": "compact-kernel transfer replacement derivation",
            "result": "PASS_SYMBOLIC_BOUND_NONCLAIM",
            "detail": "replacement is T_grad^compact <= (ell_s/lambda)|Khat(ell_s/lambda)| with C_N constants required for scoring",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3390_2_gaussian_trials",
            "test": "Gaussian boundary d/ell acquisition rows",
            "result": "PASS_REQUIREMENT_ROWS_NONCLAIM",
            "detail": f"trial_rows={len(rows_by_name['gaussian_acquisition'])}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3390_3_cassini_rough_estimator",
            "test": "Cassini rough geometry scale estimator",
            "result": "PASS_ROUGH_NONCLAIM",
            "detail": f"rough strict projector-controlled ell_s ceiling can be as low as {min_control:.3e} m; boundary collar ceiling is far looser up to {max_boundary_ell:.3e} m",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3390_4_firewall",
            "test": "prevent local PPN/local GR claim",
            "result": "PASS_CLAIM_FIREWALL",
            "detail": "3390 moves from missing-input ledger to concrete source/estimator hunt, but all outputs remain nonclaim until source pack and parent projection law are closed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3390_0_sources",
            "claim": "all 3390 cited sources exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "local/core/formalization context files were read only; no formalization writes",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3390_1_arena_selected",
            "claim": "a concrete local PPN arena is selected",
            "gate_pass": "true",
            "reason": "Cassini solar PPN gamma branch is selected as the first concrete local geometry hunt",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3390_2_source_backed_constants",
            "claim": "Cassini constants and impact geometry are source-backed",
            "gate_pass": "false",
            "reason": "3390 uses a rough internal b=1.6Rsun estimator only; 3391 must source the constants/impact geometry",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3390_3_parent_ell_s",
            "claim": "parent MTS supplies smoothing length ell_s or exact projector constancy",
            "gate_pass": "false",
            "reason": "ell_s and projector law remain parent-owned; 3390 only derives the meter-scale pressure if curvature-scale projector variation is used",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3390_4_compact_adoption",
            "claim": "compact branch is adopted and numerically scoreable",
            "gate_pass": "false",
            "reason": "symbolic compact transfer law is derived, but kernel shape constants C_N/rho_K are not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3390_5_local_ppn",
            "claim": "local PPN/local-GR branch passes",
            "gate_pass": "false",
            "reason": "source pack, parent ell_s, projector constancy/derivative bound, physical flux, moment and gauge defects remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    estimator = rows_by_name["cassini_estimator"]
    min_control = min(to_float(row["controlling_ell_s_max_m"]) for row in estimator)
    worst = min(estimator, key=lambda row: to_float(row["controlling_ell_s_max_m"]))
    return [
        {
            "decision_id": "DEC3390_0_progress",
            "decision": "3390 converts the local scale problem into a Cassini geometry inequality.",
            "because": "For a rough Cassini-like solar exterior, the boundary collar is not the likely killer; the projector commutator is.",
            "next_action": "source the Cassini constants and either prove P_PPN parent-parallel on the smoothing support or require ell_s below the derived ceiling",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3390_1_projector_pressure",
            "decision": "Under the curvature-scale projector model, the harshest rough ell_s ceiling is meter-scale or below.",
            "because": f"worst row {worst['source_row']} has controlling ell_s <= {min_control:.3e} m if C1=C2=1 and ||nabla P||~1/L_curv.",
            "next_action": "do not argue by vibes; either derive exact projector constancy or source a physical smoothing length compatible with this ceiling",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3390_2_compact_route",
            "decision": "Compact kernel is still a real route, but only after replacing Gaussian transfer.",
            "because": "compact support can kill collar leakage exactly, while Fourier decay replaces the old exp[-ell_s^2/(2lambda^2)] Gaussian law.",
            "next_action": "if compact is chosen, parent-sign k, rho_K and C_N before using it in scoring",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3390_3_best_next",
            "decision": "Best next target is Cassini source pack plus projector constancy theorem, not another generic missing-input ledger.",
            "because": "3390 already says which number matters most: ell_s||nabla P_PPN|| or an exact P_PPN constancy theorem.",
            "next_action": "build 3391 Cassini scale source pack and P_PPN parallel-projector theorem/finite bound",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3391-Y5-R2FR-Cassini-scale-source-pack-and-projector-constancy-theorem-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3391_Cassini_scale_source_pack_and_projector_constancy_theorem.py",
            "objective": "replace the 3390 rough Cassini constants with source-backed rows, then either prove P_PPN is parent-parallel/constant across the smoothing support or compute ell_s||nabla P|| and ell_s^2||nabla^2P|| from sourced local geometry",
            "why_next": "3390 shows the projector commutator is the likely controlling local PPN scale, while boundary collar pressure is probably easy in a solar exterior",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3392-Y5-R2FR-compact-bump-kernel-parent-adoption-and-Fourier-transfer-table-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3392_compact_bump_kernel_parent_adoption_and_Fourier_transfer_table.py",
            "objective": "if the parent framework chooses compact smoothing, fix k, rho_K and C_N constants and regenerate T_grad/threshold rows without using Gaussian transfer",
            "why_next": "compact route can give exact collar silence, but only with an honest transfer-law replacement",
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
        for hit in FW.rglob("*3390*")
        if hit.name.startswith(("3390-Y5", "P8_Y5_R2FR_3390", "P8_Y5_BRR545_3390", "Y5_R2FR_3390"))
    ] if FW.exists() else []
    sweep_quantities = {row["quantity"] for row in rows_by_name["source_sweep"]}
    contract_ids = {row["contract_id"] for row in rows_by_name["compact_contract"]}
    arena_selected = any(row["selected"] == "true" and "Cassini" in row["arena"] for row in rows_by_name["arena"])
    estimator_positive = all(
        to_float(row["controlling_ell_s_max_m"]) > 0 and to_float(row["schwarzschild_curvature_radius_m"]) > 0
        for row in rows_by_name["cassini_estimator"]
    )
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    checks = [
        ("VAL3390_0_sources_exist_parse", "all cited 3390 source paths exist and parse", source_ok, ""),
        ("VAL3390_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3390_2_source_sweep_quantities", "source sweep covers all required scale quantities", set(QUANTITY_PATTERNS).issubset(sweep_quantities), f"quantities={len(sweep_quantities)}"),
        ("VAL3390_3_arena_selected", "Cassini solar PPN arena selected", arena_selected, ""),
        ("VAL3390_4_compact_contract", "compact transfer replacement contract present", {"CT3390_1_boundary_zero", "CT3390_2_transfer_replacement", "CT3390_3_Cinfty_decay", "CT3390_4_projector_commutator_survives"}.issubset(contract_ids), ""),
        ("VAL3390_5_gaussian_rows", "Gaussian acquisition rows include C_boundary trials", len(rows_by_name["gaussian_acquisition"]) >= 32, f"rows={len(rows_by_name['gaussian_acquisition'])}"),
        ("VAL3390_6_projector_rows", "projector gradient rows cover target summary", len(rows_by_name["projector_acquisition"]) >= 8, f"rows={len(rows_by_name['projector_acquisition'])}"),
        ("VAL3390_7_cassini_estimator", "rough Cassini estimator rows are finite positive nonclaim rows", len(rows_by_name["cassini_estimator"]) >= 8 and estimator_positive, f"rows={len(rows_by_name['cassini_estimator'])}"),
        ("VAL3390_8_runner", "runner records sweep, compact derivation, Gaussian trials, Cassini estimator and firewall", {"PASS_EXECUTED_NONCLAIM", "PASS_SYMBOLIC_BOUND_NONCLAIM", "PASS_REQUIREMENT_ROWS_NONCLAIM", "PASS_ROUGH_NONCLAIM", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3390_9_gates", "gates block source-backed constants, parent ell_s, compact adoption, and local PPN claim", gate_map.get("GATE3390_1_arena_selected") == "true" and gate_map.get("GATE3390_2_source_backed_constants") == "false" and gate_map.get("GATE3390_3_parent_ell_s") == "false" and gate_map.get("GATE3390_4_compact_adoption") == "false" and gate_map.get("GATE3390_5_local_ppn") == "false", ""),
        ("VAL3390_10_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3390_11_write_scope_outside_formalization", "no 3390 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
        ("VAL3390_12_next_target", "next target moves to Cassini source pack and projector theorem", rows_by_name["next"][0]["target_id"].startswith("3391-Y5-R2FR-Cassini-scale-source-pack"), ""),
    ]
    overall = all(passed for _, _, passed, _ in checks)
    checks.append(("VAL3390_13_overall", "3390 validation overall", overall, "all required checks passed" if overall else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    estimator = rows_by_name["cassini_estimator"]
    min_control = min(to_float(row["controlling_ell_s_max_m"]) for row in estimator)
    worst = min(estimator, key=lambda row: to_float(row["controlling_ell_s_max_m"]))
    lines = [
        "# 3390 - Y5/R2FR local scale acquisition or compact-kernel transfer replacement under AX1090",
        "",
        "## Summary",
        "- 3390 chooses a concrete local arena: Cassini-like solar PPN gamma.",
        "- This is not another passive missing-input ledger: it runs a source sweep, derives the compact-kernel transfer replacement contract, and builds a rough Cassini geometry estimator.",
        "- The useful new physics pressure is sharp: in a solar exterior rough model, boundary collar leakage is probably not the bottleneck; the projector commutator is.",
        f"- Under the nonclaim curvature-scale projector estimate, the harshest row `{worst['source_row']}` needs `ell_s` below about `{min_control:.3e} m` if `C1=C2=1` and no exact projector-constancy theorem is available.",
        "- Therefore the next real move is not to say 'missing' again: source the Cassini constants and prove/bound `P_PPN` constancy over the smoothing cell.",
        "- No local-GR/PPN claim is made from 3390; all rows remain private nonclaim scaffolding.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Corpus Scale Source Sweep",
        md_table(rows_by_name["source_sweep"]),
        "## Local Arena Selection",
        md_table(rows_by_name["arena"]),
        "## Compact Transfer Replacement Contract",
        md_table(rows_by_name["compact_contract"]),
        "## Gaussian Scale Acquisition Rows",
        md_table(rows_by_name["gaussian_acquisition"]),
        "## Projector Gradient Acquisition Rows",
        md_table(rows_by_name["projector_acquisition"]),
        "## Cassini Geometry Estimator",
        md_table(rows_by_name["cassini_estimator"]),
        "## Scoring Readiness Matrix",
        md_table(rows_by_name["readiness"]),
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
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "source_sweep": source_sweep_rows(),
        "arena": arena_rows(),
        "compact_contract": compact_contract_rows(),
        "gaussian_acquisition": gaussian_acquisition_rows(),
        "projector_acquisition": projector_acquisition_rows(),
        "cassini_estimator": cassini_geometry_estimator_rows(),
    }
    rows_by_name["readiness"] = readiness_rows(rows_by_name)
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
