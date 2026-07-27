from __future__ import annotations

import csv
import math
import shutil
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3389-Y5-R2FR-finite-epsilon-scale-input-runner-or-compact-kernel-adoption-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3389_SOURCE_REGISTER.csv",
    "compact_audit": OUT / "P8_Y5_R2FR_3389_COMPACT_KERNEL_ADOPTION_AUDIT.csv",
    "scale_schema": OUT / "P8_Y5_R2FR_3389_SCALE_INPUT_SCHEMA.csv",
    "target_summary": OUT / "P8_Y5_R2FR_3389_TARGET_REQUIREMENT_SUMMARY.csv",
    "scenario_runner": OUT / "P8_Y5_R2FR_3389_SCALE_SCENARIO_RUNNER_NONCLAIM.csv",
    "acquisition": OUT / "P8_Y5_R2FR_3389_INPUT_ACQUISITION_LEDGER.csv",
    "runner": OUT / "P8_Y5_R2FR_3389_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3389_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3389_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3389_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3389_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3389_0_3388_doc", ROOT / "3388-Y5-R2FR-smoothing-projector-parent-owner-or-epsilon-scale-inputs-under-AX1090.md", "3388 smoothing/projector handoff"),
    ("SRC3389_1_3388_targets", OUT / "P8_Y5_R2FR_3388_SCALE_TARGET_REQUIREMENTS.csv", "scale target requirements"),
    ("SRC3389_2_3388_inputs", OUT / "P8_Y5_R2FR_3388_FIRST_SCALE_INPUT_ROWS_NONCLAIM.csv", "finite scale input rows"),
    ("SRC3389_3_3388_package", OUT / "P8_Y5_R2FR_3388_ADMISSIBLE_PACKAGE_CONTRACT.csv", "admissible package contract"),
    ("SRC3389_4_3388_zero", OUT / "P8_Y5_R2FR_3388_ZERO_IMPLICATIONS_AND_REDUCED_EPSILON.csv", "zero and finite implications"),
    ("SRC3389_5_3387_boundary", OUT / "P8_Y5_R2FR_3387_BOUNDARY_COLLAR_TAIL_LAW.csv", "boundary collar-tail law"),
    ("SRC3389_6_3387_kernel", OUT / "P8_Y5_R2FR_3387_KERNEL_PROJECTOR_COMMUTATOR_LAW.csv", "kernel projector commutator law"),
    ("SRC3389_7_3321_kernel", OUT / "P8_Y5_R2FR_3321_KERNEL_TRANSFER_LAW.csv", "Gaussian kernel transfer law"),
    ("SRC3389_8_3320_doc", ROOT / "3320-Y5-R2FR-local-first-gradient-silence-or-gradient-envelope-under-AX1090.md", "compact-kernel stationarity route"),
    ("SRC3389_9_3376_doc", ROOT / "3376-Y5-R2FR-boundary-zero-flux-or-Bzero-first-row-under-AX1090.md", "boundary zero-flux package"),
]


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
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def compact_audit_rows() -> list[dict[str, str]]:
    return [
        {
            "audit_id": "CK3389_0_mathematical_existence",
            "question": "Can an isotropic compact bump kernel with zero first moment exist?",
            "result": "YES_MATHEMATICALLY",
            "detail": "In a local normal/Fermi patch one can choose a normalized radial compact bump K_ell with int z^i K_ell dV=0 up to curvature correction terms.",
            "blocks_current_adoption": "parent MTS has not selected this kernel branch before tests",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CK3389_1_boundary_zero",
            "question": "Would compact/interior support zero epsilon_boundary_tail?",
            "result": "YES_CONDITIONALLY",
            "detail": "If d_collar >= rho_K ell_s and the 3376 physical/reference/topology flux package is zero, boundary leakage vanishes structurally.",
            "blocks_current_adoption": "d_collar/ell_s, rho_K, and 3376 zero-flux clauses are not parent-signed",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CK3389_2_transfer_replacement",
            "question": "Can compact kernel replace Gaussian without changing earlier transfer rows?",
            "result": "NO_REQUIRES_TRANSFER_REDERIVATION",
            "detail": "3321 Gaussian T_grad samples use exp[-ell_s^2/(2 lambda^2)]; a compact bump needs its own |Khat(k ell_s)| bound and constants.",
            "blocks_current_adoption": "compact branch must regenerate T_grad and threshold tables before empirical scoring",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CK3389_3_projector_commutation",
            "question": "Does compact/isotropic smoothing solve kernel anisotropy?",
            "result": "ONLY_WITH_CONSTANT_PROJECTOR",
            "detail": "Any scalar isotropic kernel commutes with a constant P0, but variable P_PPN still has [P,S]f=int K[P(x)-P(y)]f.",
            "blocks_current_adoption": "real-patch projector constancy or finite gradient bounds remain required",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CK3389_4_current_verdict",
            "question": "Is compact kernel adopted for current MTS?",
            "result": "CURRENTLY_NOT_ADOPTED",
            "detail": "Compact branch is a clean theorem route, but switching from Gaussian to compact would be a parent-action/readout choice requiring explicit adoption and transfer-law replacement.",
            "blocks_current_adoption": "no parent-signed smoothing branch declaration",
            "valid_for_claim": "false",
        },
    ]


def scale_schema_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in read_csv_rows(OUT / "P8_Y5_R2FR_3388_FIRST_SCALE_INPUT_ROWS_NONCLAIM.csv"):
        rows.append(
            {
                "input_id": row.get("input_id", ""),
                "quantity": row.get("quantity", ""),
                "definition": row.get("definition", ""),
                "needed_for": row.get("needed_for", ""),
                "current_value": row.get("current_value", ""),
                "runner_role": "required input for exact compact branch or Gaussian finite bound",
                "status": "MISSING_NONCLAIM_INPUT",
                "valid_for_claim": "false",
            }
        )
    return rows


def target_summary_rows() -> list[dict[str, str]]:
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in read_csv_rows(OUT / "P8_Y5_R2FR_3388_SCALE_TARGET_REQUIREMENTS.csv"):
        key = (
            row.get("threshold_source", ""),
            row.get("source_row", ""),
            row.get("A_gamma_or_PPN_times_Cmetric", ""),
        )
        grouped[key].append(row)

    summaries: list[dict[str, str]] = []
    for (threshold_source, source_row, response), rows in grouped.items():
        boundary_targets = [to_float(row.get("epsilon_boundary_target", "")) for row in rows]
        kernel_targets = [to_float(row.get("epsilon_kernel_target", "")) for row in rows]
        required_d = [to_float(row.get("required_d_collar_over_ell_if_Cboundary_1_and_flux_zero", "")) for row in rows]
        boundary_min = min(value for value in boundary_targets if math.isfinite(value))
        kernel_min = min(value for value in kernel_targets if math.isfinite(value))
        d_max = max(value for value in required_d if math.isfinite(value))
        kernel_quarter = kernel_min / 4.0
        summaries.append(
            {
                "summary_id": f"TS3389_{source_row}",
                "threshold_source": threshold_source,
                "source_row": source_row,
                "A_gamma_or_PPN_times_Cmetric": response,
                "min_epsilon_boundary_target": f"{boundary_min:.15e}",
                "required_d_collar_over_ell_Cboundary1_flux0": f"{d_max:.12e}",
                "min_epsilon_kernel_target": f"{kernel_min:.15e}",
                "equal_quarter_kernel_term_budget": f"{kernel_quarter:.15e}",
                "interpretation": "target only; no current source-backed scale input",
                "valid_for_claim": "false",
            }
        )
    return summaries


def strict_targets() -> tuple[float, float]:
    summaries = target_summary_rows()
    boundary = min(to_float(row["min_epsilon_boundary_target"]) for row in summaries)
    kernel = min(to_float(row["min_epsilon_kernel_target"]) for row in summaries)
    return boundary, kernel


def scenario_rows() -> list[dict[str, str]]:
    strict_boundary, strict_kernel = strict_targets()
    scenarios = [
        ("SC3389_0_compact_exact_unsigned", "compact exact if parent signed", "compact", False, math.inf, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, "hypothetical exact branch; parent not signed"),
        ("SC3389_1_gaussian_d4_loose", "Gaussian collar d/ell=4 with mild projector", "gaussian", False, 4.0, 1.0, 0.0, 1e-6, 1e-6, 0.0, 0.0, 0.0, "useful for loose bounds, fails harsh local PPN targets"),
        ("SC3389_2_gaussian_d6_mid", "Gaussian collar d/ell=6 with tiny projector", "gaussian", False, 6.0, 1.0, 0.0, 1e-10, 1e-10, 0.0, 0.0, 0.0, "near harsh boundary pressure but projector still too large for strict target"),
        ("SC3389_3_gaussian_d7p2_clean", "Gaussian collar d/ell=7.2 clean projector", "gaussian", False, 7.2, 1.0, 0.0, 1e-12, 1e-12, 1e-12, 1e-12, 0.0, "passes strict smoke if flux/gauge remain zero-level"),
        ("SC3389_4_gaussian_flux_fail", "Gaussian collar good but physical flux 1e-9", "gaussian", False, 7.2, 1.0, 1e-9, 1e-12, 1e-12, 1e-12, 1e-12, 0.0, "shows 3376 flux rows can dominate even with excellent collar"),
        ("SC3389_5_gaussian_gauge_fail", "Gaussian collar good but gauge defect 1e-8", "gaussian", False, 7.2, 1.0, 0.0, 1e-12, 1e-12, 1e-12, 1e-8, 0.0, "shows gauge/readout defect can dominate kernel channel"),
        ("SC3389_6_high_Cboundary", "Gaussian collar d/ell=7.2 but C_boundary=1e3", "gaussian", False, 7.2, 1e3, 0.0, 1e-12, 1e-12, 1e-12, 1e-12, 0.0, "operator normalization can erase apparent tail safety"),
    ]
    rows: list[dict[str, str]] = []
    for scenario_id, label, branch, parent_signed, d_over_ell, c_boundary, flux, ell_grad, ell2_hess, moment, gauge, worldtube, note in scenarios:
        if math.isinf(d_over_ell):
            tail = 0.0
        else:
            tail = c_boundary * math.exp(-0.5 * d_over_ell * d_over_ell)
        boundary_total = tail + flux + worldtube
        kernel_total = ell_grad + ell2_hess + moment + gauge
        rows.append(
            {
                "scenario_id": scenario_id,
                "label": label,
                "kernel_branch": branch,
                "parent_signed": bool_text(parent_signed),
                "d_collar_over_ell": "inf" if math.isinf(d_over_ell) else f"{d_over_ell:.6e}",
                "C_boundary": f"{c_boundary:.6e}",
                "flux_envelope": f"{flux:.6e}",
                "epsilon_worldtube_mismatch": f"{worldtube:.6e}",
                "epsilon_boundary_tail": f"{tail:.15e}",
                "epsilon_boundary_total": f"{boundary_total:.15e}",
                "ell_gradP": f"{ell_grad:.6e}",
                "ell2_hessP": f"{ell2_hess:.6e}",
                "epsilon_kernel_moment": f"{moment:.6e}",
                "epsilon_gauge_readout": f"{gauge:.6e}",
                "epsilon_kernel_total": f"{kernel_total:.15e}",
                "strict_boundary_target": f"{strict_boundary:.15e}",
                "strict_kernel_target": f"{strict_kernel:.15e}",
                "strict_boundary_pass_like": bool_text(boundary_total <= strict_boundary),
                "strict_kernel_pass_like": bool_text(kernel_total <= strict_kernel),
                "why_nonclaim": note,
                "valid_for_claim": "false",
            }
        )
    return rows


def acquisition_rows() -> list[dict[str, str]]:
    return [
        {
            "acquisition_id": "ACQ3389_0_kernel_branch",
            "quantity": "kernel_branch",
            "derive_or_source": "derive from parent readout/action, not from posterior test pressure",
            "acceptance_rule": "branch declared before using 3321/3387/3388 thresholds; compact branch regenerates transfer law",
            "current_status": "MISSING_PARENT_DECLARATION",
            "next_action": "choose/adopt compact local bump or keep Gaussian heat-kernel branch with tail scoring",
            "valid_for_claim": "false",
        },
        {
            "acquisition_id": "ACQ3389_1_d_over_ell",
            "quantity": "d_collar/ell_s",
            "derive_or_source": "same-frame local geometry: source-free collar radius divided by parent smoothing length",
            "acceptance_rule": "numeric positive value with source path and unit convention; for strict target with C_B=1 flux=0, d/ell must exceed target row",
            "current_status": "MISSING_NUMERIC_SCALE",
            "next_action": "define local PPN arena and smoothing length before scoring",
            "valid_for_claim": "false",
        },
        {
            "acquisition_id": "ACQ3389_2_C_boundary",
            "quantity": "C_boundary",
            "derive_or_source": "operator norm of boundary readout relative to EH PPN response",
            "acceptance_rule": "dimensionless bound; if >1, required d/ell increases by sqrt(2 log C_B) in quadrature",
            "current_status": "MISSING_OPERATOR_NORM",
            "next_action": "derive from readout map or keep conservative symbol in runner",
            "valid_for_claim": "false",
        },
        {
            "acquisition_id": "ACQ3389_3_flux_envelope",
            "quantity": "epsilon_boundary_physical",
            "derive_or_source": "3376 B_zero_flux/Delta_symp/Phi_Poynting/corner/M_H_ref rows",
            "acceptance_rule": "zero theorem or finite absolute no-cancellation sum below remaining boundary target",
            "current_status": "MISSING_3376_FINITE_ROWS",
            "next_action": "route through 3376 package; do not hide Poynting/physical flux as gauge boundary",
            "valid_for_claim": "false",
        },
        {
            "acquisition_id": "ACQ3389_4_projector_gradients",
            "quantity": "ell_s||nabla P_PPN|| and ell_s^2||nabla^2P_PPN||",
            "derive_or_source": "UOC normal-frame/PPN gauge readout derivative bounds",
            "acceptance_rule": "each term or their absolute sum below epsilon_kernel target after moment/gauge allocations",
            "current_status": "MISSING_PROJECTOR_DERIVATIVE_BOUNDS",
            "next_action": "derive P_PPN constancy through smoothing support or source gradient norms",
            "valid_for_claim": "false",
        },
        {
            "acquisition_id": "ACQ3389_5_moment_gauge",
            "quantity": "epsilon_kernel_moment and epsilon_gauge_readout",
            "derive_or_source": "kernel moment calculation and fixed PPN gauge/readout theorem",
            "acceptance_rule": "zero theorem or finite additive values below remaining kernel target",
            "current_status": "MISSING_MOMENT_AND_GAUGE_BOUNDS",
            "next_action": "prove normalized isotropic zero-moment kernel and fixed gauge/readout, or source values",
            "valid_for_claim": "false",
        },
    ]


def runner_rows(scenarios: list[dict[str, str]]) -> list[dict[str, str]]:
    pass_like = sum(1 for row in scenarios if row["strict_boundary_pass_like"] == "true" and row["strict_kernel_pass_like"] == "true")
    return [
        {
            "run_id": "RUN3389_0_compact_audit",
            "test": "compact-kernel exact-zero adoption audit",
            "result": "PASS_CONDITIONAL_ROUTE_BLOCKED_CURRENT",
            "detail": "compact bump can exist and zero collar tail, but branch switch requires parent declaration and transfer replacement",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3389_1_scale_schema",
            "test": "finite scale inputs represented",
            "result": "PASS_SCHEMA_NONCLAIM",
            "detail": "kernel branch, d/ell, C_boundary, flux, projector gradients, moment and gauge rows exist",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3389_2_target_summary",
            "test": "target requirements summarized",
            "result": "PASS_TARGET_SUMMARY_NONCLAIM",
            "detail": f"unique_targets={len(target_summary_rows())}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3389_3_scenario_runner",
            "test": "placeholder scale scenarios evaluated against strict target",
            "result": "PASS_SMOKE_NONCLAIM",
            "detail": f"scenarios={len(scenarios)} strict_pass_like={pass_like}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3389_4_firewall",
            "test": "prevent boundary/kernel or local-GR claim",
            "result": "PASS_CLAIM_FIREWALL",
            "detail": "pass-like scenario rows are hypothetical/nonclaim until inputs are source-backed or parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3389_0_sources",
            "claim": "all 3389 source paths exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "source register validates 3388/3387/3376/3321/3320 inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3389_1_compact_adopted",
            "claim": "compact kernel branch is parent-adopted",
            "gate_pass": "false",
            "reason": "compact branch is mathematically available but not parent-declared and would require transfer-law replacement",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3389_2_gaussian_values",
            "claim": "Gaussian branch finite scale values are source-backed",
            "gate_pass": "false",
            "reason": "d/ell, C_boundary, flux, projector gradients, moment and gauge values remain missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3389_3_runner_executes",
            "claim": "scale scenario runner executes",
            "gate_pass": "true",
            "reason": "placeholder scenarios evaluate boundary/kernel totals against strict targets",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3389_4_boundary_kernel_pass",
            "claim": "epsilon_boundary and epsilon_kernel are claim-valid",
            "gate_pass": "false",
            "reason": "no source-backed exact-zero or finite values; scenarios are nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3389_5_local_ppn",
            "claim": "local PPN/local-GR branch passes from 3389",
            "gate_pass": "false",
            "reason": "3389 is a scale-input runner and compact-kernel audit only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    summaries = target_summary_rows()
    max_d = max(to_float(row["required_d_collar_over_ell_Cboundary1_flux0"]) for row in summaries)
    min_kernel = min(to_float(row["min_epsilon_kernel_target"]) for row in summaries)
    return [
        {
            "decision_id": "DEC3389_0_progress",
            "decision": "Boundary/kernel epsilons are now executable scale constraints.",
            "because": f"strict rows require d_collar/ell_s up to about {max_d:.3f} for C_boundary=1, flux=0, and kernel terms down to {min_kernel:.3e}.",
            "next_action": "source or derive actual scale inputs, or parent-adopt compact kernel and replace Gaussian transfer law",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3389_1_compact",
            "decision": "Compact kernel is a clean exact-zero theorem route but cannot be silently swapped in.",
            "because": "it changes the Gaussian transfer law used by 3321/3386/3388 and needs parent declaration.",
            "next_action": "if compact is chosen, build compact-kernel transfer replacement before scoring",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3389_2_gaussian",
            "decision": "Gaussian branch remains viable only as a finite scale-separation claim.",
            "because": "collar tail can be tiny at d/ell around 7 for C_boundary=1, but flux, C_boundary, projector, moment and gauge defects can dominate.",
            "next_action": "define local PPN arena and get d/ell, C_boundary, projector derivative and gauge/moment values",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3389_3_best_next",
            "decision": "Best next move is a concrete local-arena scale acquisition pass, not background-gradient yet.",
            "because": "without actual d/ell and projector-gradient values, epsilon_boundary/kernel cannot be inserted into the Cassini-style runner.",
            "next_action": "build 3390 local scale acquisition or compact transfer replacement",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3390-Y5-R2FR-local-scale-acquisition-or-compact-kernel-transfer-replacement-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3390_local_scale_acquisition_or_compact_kernel_transfer_replacement.py",
            "objective": "choose a concrete local PPN arena and source/derive d_collar/ell_s, C_boundary, projector-gradient norms, kernel moment and gauge defect; if compact kernel is adopted, replace Gaussian T_grad/threshold rows with compact-kernel transfer bounds",
            "why_next": "3389 runner shows these concrete values decide whether boundary/kernel epsilon channels can enter a real Cassini/local-GR pass",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3391-Y5-R2FR-background-gradient-and-Tgrad-scale-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3391_background_gradient_and_Tgrad_scale_bound.py",
            "objective": "derive or source epsilon_bg_PPN and ell_s/lambda_PPN after boundary/kernel scale inputs are handled",
            "why_next": "once boundary/kernel are zeroed or bounded, epsilon_bg*T_grad is the remaining epsilon_eff channel",
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
        for hit in FW.rglob("*3389*")
        if hit.name.startswith(("3389-Y5", "P8_Y5_R2FR_3389", "P8_Y5_BRR545_3389", "Y5_R2FR_3389"))
    ] if FW.exists() else []
    compact_results = {row["result"] for row in rows_by_name["compact_audit"]}
    schema_quantities = {row["quantity"] for row in rows_by_name["scale_schema"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    scenario_ids = {row["scenario_id"] for row in rows_by_name["scenario_runner"]}
    checks = [
        ("VAL3389_0_sources_exist_parse", "all cited 3389 source paths exist and parse", source_ok, ""),
        ("VAL3389_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3389_2_compact_audit", "compact audit allows route but blocks current adoption", {"YES_MATHEMATICALLY", "NO_REQUIRES_TRANSFER_REDERIVATION", "CURRENTLY_NOT_ADOPTED"}.issubset(compact_results), ""),
        ("VAL3389_3_scale_schema", "scale schema covers all required 3388 scale inputs", {"kernel_branch", "d_collar/ell_s", "C_boundary", "epsilon_boundary_physical", "ell_s ||nabla P_PPN||", "ell_s^2 ||nabla^2 P_PPN||", "epsilon_kernel_moment", "epsilon_gauge_readout"}.issubset(schema_quantities), ""),
        ("VAL3389_4_target_summary", "target summary rows exist for response products", len(rows_by_name["target_summary"]) >= 8, f"rows={len(rows_by_name['target_summary'])}"),
        ("VAL3389_5_scenarios", "scenario runner includes compact, clean Gaussian, and failure modes", {"SC3389_0_compact_exact_unsigned", "SC3389_3_gaussian_d7p2_clean", "SC3389_4_gaussian_flux_fail", "SC3389_5_gaussian_gauge_fail"}.issubset(scenario_ids), ""),
        ("VAL3389_6_runner", "runner records compact audit, schema, target summary, smoke scenarios and firewall", {"PASS_CONDITIONAL_ROUTE_BLOCKED_CURRENT", "PASS_SCHEMA_NONCLAIM", "PASS_TARGET_SUMMARY_NONCLAIM", "PASS_SMOKE_NONCLAIM", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3389_7_gates", "gates block compact adoption, Gaussian values, boundary/kernel claim and local PPN while runner executes", gate_map.get("GATE3389_1_compact_adopted") == "false" and gate_map.get("GATE3389_2_gaussian_values") == "false" and gate_map.get("GATE3389_3_runner_executes") == "true" and gate_map.get("GATE3389_4_boundary_kernel_pass") == "false" and gate_map.get("GATE3389_5_local_ppn") == "false", ""),
        ("VAL3389_8_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3389_9_next_target", "next target moves to local scale acquisition or compact transfer replacement", rows_by_name["next"][0]["target_id"].startswith("3390-Y5-R2FR-local-scale-acquisition"), ""),
        ("VAL3389_10_write_scope_outside_formalization", "no 3389 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
    ]
    overall = all(passed for _, _, passed, _ in checks)
    checks.append(("VAL3389_11_overall", "3389 validation overall", overall, "all required checks passed" if overall else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    summaries = rows_by_name["target_summary"]
    max_d = max(to_float(row["required_d_collar_over_ell_Cboundary1_flux0"]) for row in summaries)
    min_kernel = min(to_float(row["min_epsilon_kernel_target"]) for row in summaries)
    lines = [
        "# 3389 - Y5/R2FR finite epsilon scale-input runner or compact-kernel adoption under AX1090",
        "",
        "## Summary",
        "- 3389 turns the 3388 scale requirements into an executable nonclaim runner.",
        "- Compact-kernel route: mathematically clean and can zero the collar tail, but it is not currently adopted because it needs a parent smoothing declaration and a replacement for the Gaussian transfer law.",
        "- Gaussian route: still testable; strict rows require large enough `d_collar/ell_s`, small enough physical flux, and tiny projector/moment/gauge defects.",
        f"- Current strict scale lesson: with `C_boundary=1` and zero flux, the harsh rows require `d_collar/ell_s` up to about `{max_d:.3f}`; kernel additive terms can need budgets down to `{min_kernel:.3e}`.",
        "- Scenario runner result: pass-like rows exist only as hypothetical/nonclaim rows; flux or gauge defects easily dominate.",
        "- No local-GR/PPN claim is allowed from 3389; the next step must source or derive the actual local scale inputs.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Compact Kernel Adoption Audit",
        md_table(rows_by_name["compact_audit"]),
        "## Scale Input Schema",
        md_table(rows_by_name["scale_schema"]),
        "## Target Requirement Summary",
        md_table(rows_by_name["target_summary"]),
        "## Scale Scenario Runner",
        md_table(rows_by_name["scenario_runner"]),
        "## Input Acquisition Ledger",
        md_table(rows_by_name["acquisition"]),
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
    scenarios = scenario_rows()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "compact_audit": compact_audit_rows(),
        "scale_schema": scale_schema_rows(),
        "target_summary": target_summary_rows(),
        "scenario_runner": scenarios,
        "acquisition": acquisition_rows(),
        "runner": runner_rows(scenarios),
        "gates": gate_rows(source_ok),
        "decision": decision_rows(),
        "next": next_rows(),
    }
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
