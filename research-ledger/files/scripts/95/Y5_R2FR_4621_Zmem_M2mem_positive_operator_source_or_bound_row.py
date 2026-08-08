from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4621"
CLAIM_ID = "L-463"
BRANCH_ID = "MTS_R2FR_Y5_ZMEM_M2MEM_POSITIVE_OPERATOR_4621"
MARKER = "PPC4161_ZMEM_M2MEM_POSITIVE_OPERATOR_SOURCE_OR_BOUND_ROW_4621"
PACKET_MARKER = "PPC4161_PACKET_ZMEM_M2MEM_POSITIVE_OPERATOR_4621"
DECISION = "MEMORY_AMPLITUDE_NOHAIR_DERIVED_CONDITIONALLY_BOUND_ROW_READY_NONCLAIM"
NEXT_TARGET = "4622-Y5-R2FR-rho-mem-source-channel-zero-or-EM-Poynting-bound.md"

DOC_PATH = POST / "4621-Y5-R2FR-Zmem-M2mem-positive-operator-source-or-bound-row.md"
FORMAL_PATH = FORMAL / "637-PPC4161-Zmem-M2mem-positive-operator-source-or-bound-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4621_SOURCE_REGISTER.csv"
IDENTITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_POSITIVE_OPERATOR_IDENTITY.csv"
SOURCE_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4621_ZMEM_M2MEM_SOURCE_ROWS_NONCLAIM.csv"
BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_AMPLITUDE_BOUND_ROWS.csv"
CHANNEL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4621_RHOMEM_SOURCE_CHANNEL_AUDIT.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4621_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4621_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4621_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4621_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4621_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4621_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4621_VALIDATION.csv"

CSV_4620_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4620_NEXT_TARGET.csv"
CSV_4620_IMPACT = SOURCE_DIR / "P8_Y5_R2FR_4620_CMEMORY_BOUND_IMPACT_ROWS.csv"
CSV_4620_NUMERIC = SOURCE_DIR / "P8_Y5_R2FR_4620_KAPPA_MEMF2_FIRST_NUMERIC_ROW_NONCLAIM.csv"
CSV_4620_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4620_KAPPA_MEMF2_ZERO_ROUTES.csv"
CSV_4619_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4619_KAPPA_MEMF2_ZMEM_M2MEM_SOURCE_ROWS_NONCLAIM.csv"
CSV_4619_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4619_F2_MEMORY_OWNER_THEOREM.csv"
CSV_4618_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4618_MEMORY_CLASS_SCALAR_NOHAIR_THEOREM.csv"
CSV_4506_OPERATOR = SOURCE_DIR / "P8_Y5_R2FR_4506_MEMORY_OPERATOR_SIGNATURE.csv"
CSV_4506_BODY = SOURCE_DIR / "P8_Y5_R2FR_4506_BODY_CHARGE_INPUT_ROW.csv"
CSV_4506_EXTREMUM = SOURCE_DIR / "P8_Y5_R2FR_4506_MEMORY_EXTREMUM_TEST.csv"
CSV_630_MD = POST / "630-Y5-R10-WEP-coupling-cross-check.md"
CSV_627_MD = POST / "627-Y5-R10-cg-bound-source-acquisition-or-local-geometry-zero-proof.md"

PUBLIC_STAGE = Path("D:/Users/ollet/Desktop/Motion-TimeSpace-public-stage")
BACKUP_REPO = Path("D:/Users/ollet/Desktop/laptop-back-up-")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


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
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
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
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines)


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for number, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return number
    return 0


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    suffix = "\n" if text.endswith("\n") or not text else "\n\n"
    write_text(path, text + suffix + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not path.exists() or not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--porcelain"], text=True, capture_output=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def any_claim_true(rows: list[dict[str, Any]]) -> bool:
    return any(str(value).lower() == "true" for row in rows for key, value in row.items() if key in {"valid_for_claim", "claim_allowed"})


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4621_00_4620_next", CSV_4620_NEXT, "4621-Y5-R2FR-Zmem-M2mem-positive-operator-source-or-bound-row.md", "4620 selected the memory amplitude operator target."),
        ("SRC4621_01_4620_impact", CSV_4620_IMPACT, "IM4620_2_next_operator", "4620 amplitude impact row."),
        ("SRC4621_02_4620_numeric", CSV_4620_NUMERIC, "KNUM4620_0_first_numeric_template", "4620 kappa/F2 first numeric row."),
        ("SRC4621_03_4620_zero", CSV_4620_ZERO, "KZ4620_2_branch_extremum_zero", "4620 extremum route."),
        ("SRC4621_04_4619_source", CSV_4619_SOURCE, "KMF4619_2_Zmem", "4619 Zmem source row."),
        ("SRC4621_05_4619_source_M2", CSV_4619_SOURCE, "KMF4619_3_M2mem", "4619 M2mem source row."),
        ("SRC4621_06_4619_source_rho", CSV_4619_SOURCE, "KMF4619_4_rhomem", "4619 rhomem source row."),
        ("SRC4621_07_4619_source_boundary", CSV_4619_SOURCE, "KMF4619_5_Qboundary", "4619 boundary source row."),
        ("SRC4621_08_4619_law", CSV_4619_THEOREM, "FMO4619_3_finite_derivative_law", "4619 finite derivative law."),
        ("SRC4621_09_4618_nohair", CSV_4618_THEOREM, "MCS4618_1_positive_nohair_zero", "4618 positive-operator zero route."),
        ("SRC4621_10_4506_operator", CSV_4506_OPERATOR, "MOP4506_0_quadratic_action", "4506 memory operator signature."),
        ("SRC4621_11_4506_body", CSV_4506_BODY, "BCIN4506_0_memory_density", "4506 memory body-charge input row."),
        ("SRC4621_12_4506_extremum", CSV_4506_EXTREMUM, "MEXT4506_1_branch_extremum", "4506 branch extremum row."),
        ("SRC4621_13_630_coupling", CSV_630_MD, "coupling", "630 coupling audit, if present."),
        ("SRC4621_14_627_geometry", CSV_627_MD, "c_g", "627 local geometry/c_g audit, if present."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in specs:
        text = read_text(path)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": needle in text,
            "line": line_of(path, needle),
            "role": role,
            "valid_for_claim": False,
            "timestamp_utc": now,
        })
    return rows


def identity_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "identity_id": "MPI4621_0_local_memory_operator",
            "claim_piece": "local memory amplitude equation",
            "formal_statement": "On a local branch Ω, δm_mem obeys L_mem δm_mem = rho_mem with L_mem := -∇_i(Z_mem ∇^i) + M2_mem.",
            "derivation": "This is the Euler-Lagrange equation of the quadratic memory action S_mem^(2)=1/2∫(Z_mem |∇δm|^2 + M2_mem δm^2)dμ - ∫rho_mem δm dμ plus boundary flux.",
            "result": "OPERATOR_NORMAL_FORM_WRITTEN",
            "current_status": "PARENT_ZMEM_M2MEM_VALUES_UNSIGNED",
            "source_refs": "KMF4619_2_Zmem;KMF4619_3_M2mem;MOP4506_0_quadratic_action",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "identity_id": "MPI4621_1_energy_identity",
            "claim_piece": "positive operator energy identity",
            "formal_statement": "∫Ω Z_mem |∇δm|^2 dμ + ∫Ω M2_mem δm^2 dμ = ∫Ω rho_mem δm dμ + ∮∂Ω δm Z_mem n^i∇_iδm dΣ.",
            "derivation": "Multiply L_mem δm=rho_mem by δm, integrate by parts, and keep the boundary flux instead of assuming it vanishes.",
            "result": "EXACT_CONDITIONAL_IDENTITY",
            "current_status": "DERIVED_LOCAL_IDENTITY_NOT_PARENT_NUMERIC",
            "source_refs": "FMO4619_3_finite_derivative_law;MCS4618_1_positive_operator_zero",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "identity_id": "MPI4621_2_nohair_zero",
            "claim_piece": "derived local plateau/no-hair condition",
            "formal_statement": "If Z_mem≥Z0>0, M2_mem≥M0^2>0, rho_mem=0, and boundary flux or boundary value is zero on the same branch, then δm_mem=0 and Delta_v m_mem=0.",
            "derivation": "Under those signs and zero source/boundary conditions the energy identity has non-negative left side and zero right side, forcing ∇δm=0 and δm=0 when M0^2>0.",
            "result": "PLATEAU_DERIVED_CONDITIONALLY_NOT_AXIOMATIC",
            "current_status": "ZERO_SOURCE_AND_BOUNDARY_NOT_PARENT_SIGNED",
            "source_refs": "KMF4619_4_rhomem;KMF4619_5_Qboundary",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "identity_id": "MPI4621_3_finite_amplitude_bound",
            "claim_piece": "finite local amplitude bound",
            "formal_statement": "If source or boundary terms survive, ||δm||_H1(Ω) ≤ CΩ (||rho_mem||_H-1(Ω)+||q_boundary_mem||_H-1/2(∂Ω))/min(Z0,M0^2).",
            "derivation": "Cauchy-Schwarz and trace/Poincare inequalities turn the energy identity into a coercive elliptic estimate; an L∞/Delta_v bound needs an additional elliptic regularity constant.",
            "result": "BOUND_ROW_READY_NONCLAIM",
            "current_status": "GEOMETRY_CONSTANT_AND_SOURCE_NORMS_UNSIGNED",
            "source_refs": "IM4620_2_next_operator;KMF4619_4_rhomem;KMF4619_5_Qboundary",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def source_value_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "ZMR4621_0_Zmem_min",
            "symbol": "Z_mem_min",
            "quantity": "positive lower bound on local memory kinetic coefficient",
            "definition": "Z_mem_min := inf_Ω Z_mem on the selected local branch",
            "required_condition": "Z_mem_min > 0",
            "value": "MISSING_PARENT_HESSIAN_OR_MATCHING",
            "units": "memory kinetic coefficient units",
            "source_required": "parent quadratic memory action, branch Hessian, unit convention",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "ZMR4621_1_M2mem_min",
            "symbol": "M2_mem_min",
            "quantity": "positive lower bound on local memory mass/gap coefficient",
            "definition": "M2_mem_min := inf_Ω M2_mem",
            "required_condition": "M2_mem_min > 0, or zero-mode removed with boundary/mean condition",
            "value": "MISSING_PARENT_HESSIAN_OR_GAP_PROOF",
            "units": "memory mass-squared units",
            "source_required": "parent memory potential Hessian or no-zero-mode proof",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "ZMR4621_2_rhomem_norm",
            "symbol": "||rho_mem||_H-1",
            "quantity": "local memory source norm",
            "definition": "rho_mem := beta_R R_obs + beta_T T_obs + beta_F F_Q^2 + beta_S ∇_i S^i + beta_gw <dot h^2> + J_hidden",
            "required_condition": "rho_mem=0 for no-hair, otherwise a sourced norm and branch projection are required",
            "value": "MISSING_SOURCE_CHANNEL_ZERO_OR_VALUE",
            "units": "dual memory-source units",
            "source_required": "parent coupling coefficients beta_R,beta_T,beta_F,beta_S,beta_gw,J_hidden and local profiles",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "ZMR4621_3_boundary_flux",
            "symbol": "||q_boundary_mem||_H-1/2",
            "quantity": "memory boundary flux norm",
            "definition": "q_boundary_mem := Z_mem n^i∇_iδm on ∂Ω",
            "required_condition": "q_boundary_mem=0 for no-hair, otherwise a flux norm and boundary condition are required",
            "value": "MISSING_BOUNDARY_ZERO_OR_VALUE",
            "units": "memory boundary-flux units",
            "source_required": "local boundary condition, matching surface, radiative/readout flux rule",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "ZMR4621_4_geometry_constant",
            "symbol": "C_Omega_mem",
            "quantity": "local elliptic/trace/regularity constant",
            "definition": "C_Omega_mem maps H1 or H-1 memory bounds to Delta_v m_mem in the local body domain",
            "required_condition": "finite constant for the selected local geometry and coarse-graining scale",
            "value": "MISSING_LOCAL_GEOMETRY_CONSTANT",
            "units": "geometry-dependent",
            "source_required": "local domain size, boundary regularity, coarse-graining map and norm definition",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def bound_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "AMB4621_0_exact_zero",
            "quantity": "Delta_v m_mem",
            "condition": "Z_mem_min>0, M2_mem_min>0, rho_mem=0, q_boundary_mem=0",
            "bound": "Delta_v m_mem = 0",
            "consequence": "C_memory_F2=0 even if kappa_memF2 is finite, because the local memory profile vanishes.",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "AMB4621_1_finite_H1",
            "quantity": "||δm_mem||_H1",
            "condition": "Z_mem_min,M2_mem_min positive and source/boundary norms known",
            "bound": "||δm||_H1 ≤ CΩ (||rho_mem||_H-1+||q_boundary_mem||_H-1/2)/min(Z_mem_min,M2_mem_min)",
            "consequence": "Finite scoring becomes possible without pretending local no-hair is exact.",
            "status": "FINITE_BOUND_FORMULA_READY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "bound_id": "AMB4621_2_Cmemory_feed",
            "quantity": "C_memory_F2",
            "condition": "kappa_memF2/Z_Q_eff_min known plus Delta_v m_mem bound",
            "bound": "C_memory_F2 ≤ |kappa_memF2|/Z_Q_eff_min * Delta_v m_mem_bound",
            "consequence": "This is the first honest route from parent memory operator data to R10/PPN/clock/orbital residuals.",
            "status": "DEPENDENT_ON_4620_AND_4621_SOURCE_ROWS",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def channel_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "channel_id": "RHO4621_0_curvature",
            "source_channel": "beta_R R_obs",
            "why_it_matters": "Local vacuum/weak-field curvature could drive memory unless beta_R=0, R_obs is negligible by field equations, or the branch projection cancels it.",
            "zero_route": "parent coupling beta_R=0 or GR-local trace/source equation sends R_obs to a controlled small value",
            "finite_route": "source beta_R and local R_obs norm",
            "current_status": "MISSING_COUPLING_OWNER",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "channel_id": "RHO4621_1_matter_trace",
            "source_channel": "beta_T T_obs",
            "why_it_matters": "Matter trace is the obvious local source that can spoil a vacuum plateau inside bodies.",
            "zero_route": "local vacuum exterior only, beta_T=0, or screened quotient projection",
            "finite_route": "source beta_T and body T_obs profile",
            "current_status": "MISSING_BODY_PROJECTION",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "channel_id": "RHO4621_2_EM_invariant",
            "source_channel": "beta_F F_Q^2",
            "why_it_matters": "This keeps the EM/wave possibility live instead of silently discarding it.",
            "zero_route": "beta_F=0 by typed coefficient-domain/no-Hom, or null radiation F_Q^2=0 on the branch",
            "finite_route": "source beta_F and local E^2-B^2 invariant",
            "current_status": "MISSING_EM_SOURCE_PROJECTION",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "channel_id": "RHO4621_3_Poynting_flux",
            "source_channel": "beta_S ∇_i S^i or boundary S·n",
            "why_it_matters": "A Poynting-vector route naturally becomes a flux/boundary source, not a magic local volume source.",
            "zero_route": "stationary source-free EM has ∇·S=0 in the volume and zero net boundary flux on the chosen domain",
            "finite_route": "source beta_S and measured/calculated EM energy flux through ∂Ω",
            "current_status": "MISSING_POYNTING_BOUNDARY_RULE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "channel_id": "RHO4621_4_high_frequency_waves",
            "source_channel": "beta_gw <dot h^2>",
            "why_it_matters": "High-frequency gravitational or relic-wave ideas enter as an averaged stress/source term and must be bounded, not hand-waved.",
            "zero_route": "beta_gw=0, no local relic bath, or averaging projects it out of the memory scalar",
            "finite_route": "source beta_gw and wave energy-density envelope",
            "current_status": "MISSING_WAVE_ENVELOPE_AND_COUPLING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4621_0_no_plateau_axiom",
            "rule": "Do not assume Delta_v m_mem=0.",
            "reason": "4621 derives the zero only from positivity plus zero source and zero boundary flux.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4621_1_no_Poynting_silence",
            "rule": "Do not discard Poynting/vector-wave channels by omission.",
            "reason": "They must be typed as volume source, boundary flux, or projected-zero parent terms.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4621_2_same_branch",
            "rule": "All Z_mem, M2_mem, rho_mem and boundary rows must be on the same branch as kappa_memF2.",
            "reason": "Mixing a zero branch with a finite branch fabricates local-GR suppression.",
            "violation_blocks_claim": True,
            "timestamp_utc": now,
        },
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4621_0_positive_coefficients",
            "blocks": "exact local memory no-hair",
            "missing": "Z_mem_min>0 and M2_mem_min>0 parent-signed on the same local branch",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4621_1_source_channels",
            "blocks": "Delta_v m_mem=0",
            "missing": "rho_mem source-channel zero proof or finite source norms, including EM/Poynting/wave channels",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "BLK4621_2_boundary_flux",
            "blocks": "local-vacuum plateau",
            "missing": "q_boundary_mem=0 or source-backed boundary flux norm on ∂Ω",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": now,
        },
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4621_0_exact_nohair",
            "promotion_condition": "All source paths exist; Z_mem_min>0; M2_mem_min>0; rho_mem=0; q_boundary_mem=0; same branch as kappa_memF2.",
            "current_result": "blocked",
            "source_paths_ready": all(row["path_exists"] and row["needle_found"] for row in sources if not row["source_id"].endswith(("630_coupling", "627_geometry"))),
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "gate_id": "PROM4621_1_finite_bound",
            "promotion_condition": "If any source survives, provide numerical/source-backed Z_mem_min, M2_mem_min, rho norm, boundary norm and C_Omega_mem.",
            "current_result": "blocked",
            "source_paths_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4621_0",
            "decision": DECISION,
            "meaning": "The local memory plateau is now a derived conditional theorem: positivity plus zero source/boundary implies Delta_v m_mem=0. If not, a finite elliptic bound is the honest route.",
            "status": "NONCLAIM_PRIVATE_DERIVATION_STAGE",
            "best_route": "prove rho_mem and q_boundary_mem vanish by parent source-channel typing; otherwise source their norms",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "status": "PRIVATE_NONCLAIM_DERIVATION_ADVANCE",
            "summary": "Zmem/M2mem positive-operator identity and no-hair theorem written; EM/Poynting/wave source channels are explicit; next is rho_mem source-channel zero or finite bound.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": now,
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "timestamp_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "The amplitude theorem is now exact conditional; the live gap is whether rho_mem and boundary flux are parent-zero or finite sourced.",
            "derive_first": "prove each rho_mem channel is absent, projected-zero, or volume-to-boundary only",
            "fallback": "create source-backed finite beta_R/beta_T/beta_F/beta_S/beta_gw and boundary flux rows",
            "valid_for_claim": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    sections = [
        f"# 4621 - Zmem/M2mem Positive Operator Source Or Bound Row",
        "",
        f"Timestamp UTC: `{now}`",
        f"Branch: `{BRANCH_ID}`",
        f"Marker: `{MARKER}`",
        f"Decision: `{DECISION}`",
        "",
        "## Result",
        "",
        "4621 does **not** claim a local-GR/R10/PPN pass. It does move the route forward: the local memory plateau is no longer an axiom. It is an exact conditional theorem from the positive memory operator energy identity.",
        "",
        "Local memory equation:",
        "",
        "`L_mem δm_mem = rho_mem`, with `L_mem := -∇_i(Z_mem ∇^i) + M2_mem`.",
        "",
        "Energy identity:",
        "",
        "`∫Ω Z_mem |∇δm|^2 dμ + ∫Ω M2_mem δm^2 dμ = ∫Ω rho_mem δm dμ + ∮∂Ω δm Z_mem n^i∇_iδm dΣ`.",
        "",
        "Therefore, if `Z_mem>0`, `M2_mem>0`, `rho_mem=0`, and the boundary flux/value is zero on the same branch, then `δm_mem=0` and `Delta_v m_mem=0`.",
        "",
        "If any source survives, the honest finite route is:",
        "",
        "`||δm||_H1 ≤ CΩ (||rho_mem||_H-1 + ||q_boundary_mem||_H-1/2) / min(Z_mem_min,M2_mem_min)`.",
        "",
        "This explicitly keeps EM/Poynting/wave channels live: they are source or boundary rows, not silent assumptions.",
        "",
        "## Sources",
        markdown_table(tables["sources"]),
        "",
        "## Positive Operator Identity",
        markdown_table(tables["identity"]),
        "",
        "## Zmem/M2mem Source Rows",
        markdown_table(tables["source_values"]),
        "",
        "## Amplitude Bound Rows",
        markdown_table(tables["bounds"]),
        "",
        "## rho_mem Source Channel Audit",
        markdown_table(tables["channels"]),
        "",
        "## Controls",
        markdown_table(tables["controls"]),
        "",
        "## Blockers",
        markdown_table(tables["blockers"]),
        "",
        "## Promotion Gates",
        markdown_table(tables["promotion"]),
        "",
        "## Decision",
        markdown_table(tables["decision"]),
        "",
        "## Status",
        markdown_table(tables["status"]),
        "",
        "## Next Target",
        markdown_table(tables["next"]),
        "",
        "## Claim Safety",
        "",
        "All rows remain `valid_for_claim=false`. The branch is private/nonclaim until positivity, source-channel, boundary, and branch-coherence inputs are parent-signed or source-backed.",
    ]
    return "\n".join(sections).strip() + "\n"


def build_formal(now: str) -> str:
    return f"""# 637 - PPC4161 Zmem/M2mem Positive Operator Source Or Bound Row

Timestamp UTC: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Branch: `{BRANCH_ID}`

## Local Memory Operator

The local memory amplitude branch is reduced to:

`L_mem δm_mem = rho_mem`, with `L_mem := -∇_i(Z_mem ∇^i) + M2_mem`.

Multiplying by `δm_mem` and integrating on the local domain `Ω` gives:

`∫Ω Z_mem |∇δm|^2 dμ + ∫Ω M2_mem δm^2 dμ = ∫Ω rho_mem δm dμ + ∮∂Ω δm Z_mem n^i∇_iδm dΣ`.

Thus the local-vacuum plateau is derivable, not assumed, if:

1. `Z_mem_min > 0`;
2. `M2_mem_min > 0` or a zero-mode is removed;
3. `rho_mem = 0` on the same branch;
4. `q_boundary_mem = 0` or the boundary value is fixed to zero.

Under those conditions `δm_mem=0`, so `Delta_v m_mem=0`, and the 4620 memory/F2 term drops out.

If source or boundary survives:

`C_memory_F2 ≤ |kappa_memF2|/Z_Q_eff_min * Delta_v m_mem_bound`.

The next target is `{NEXT_TARGET}`: classify `rho_mem` channels, including curvature, matter trace, EM invariant, Poynting flux, and high-frequency wave stress.
"""


def append_claim_once() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4621 derives the local memory plateau/no-hair condition from a positive Zmem/M2mem operator and stages finite amplitude bound rows.",
        "current_evidence": "Generated positive-operator identity, Zmem/M2mem source rows, amplitude bounds, rho_mem source-channel audit, controls, blockers, promotion gates, decision, status, next target and validation.",
        "status": "memory_amplitude_nohair_conditional_bound_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Assuming source and boundary silence instead of deriving rho_mem=0 or sourcing finite EM/Poynting/wave channels.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No b_alpha, Maxwell, WEP, clock, R10, Newton or local-GR pass until Zmem/M2mem positivity and rho/boundary rows are same-branch parent-signed or source-backed.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, ok: bool, detail: str) -> None:
        rows.append({
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "status": "PASS" if ok else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        })

    required_sources = [row for row in tables["sources"] if not row["source_id"].endswith(("630_coupling", "627_geometry"))]
    add(
        "VAL4621_00_sources_exist_and_needles_found",
        all(row["path_exists"] and row["needle_found"] for row in required_sources),
        "all required cited paths/needles found",
    )
    csv_paths = [
        SOURCE_REGISTER,
        IDENTITY_CSV,
        SOURCE_ROW_CSV,
        BOUND_CSV,
        CHANNEL_CSV,
        CONTROL_CSV,
        BLOCKERS_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    parsed = {path.name: len(read_csv(path)) for path in csv_paths if path.exists()}
    add("VAL4621_01_csv_parse", len(parsed) == len(csv_paths) and all(count > 0 for count in parsed.values()), ";".join(f"{k}:{v}" for k, v in parsed.items()))
    add("VAL4621_02_energy_identity", any(row["identity_id"] == "MPI4621_1_energy_identity" for row in tables["identity"]), "energy identity row present")
    add("VAL4621_03_nohair_theorem", any(row["identity_id"] == "MPI4621_2_nohair_zero" for row in tables["identity"]), "conditional no-hair row present")
    add("VAL4621_04_source_channels", len(tables["channels"]) >= 5 and any("Poynting" in row["channel_id"] for row in tables["channels"]), "curvature/matter/EM/Poynting/wave channels present")
    add("VAL4621_05_source_rows_nonclaim", not any_claim_true(tables["source_values"]), "source rows remain nonclaim")
    add("VAL4621_06_all_rows_nonclaim", not any(any_claim_true(rows) for rows in tables.values()), "no generated row promotes a claim")
    add("VAL4621_07_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4621_08_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4621_09_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4621_10_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4621_11_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4621_12_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4621_13_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4621_14_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4621_OVERALL", all(row["status"] == "PASS" for row in rows), "4621 positive-operator amplitude checkpoint")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "identity": identity_rows(now),
        "source_values": source_value_rows(now),
        "bounds": bound_rows(now),
        "channels": channel_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(IDENTITY_CSV, tables["identity"])
    write_csv(SOURCE_ROW_CSV, tables["source_values"])
    write_csv(BOUND_CSV, tables["bounds"])
    write_csv(CHANNEL_CSV, tables["channels"])
    write_csv(CONTROL_CSV, tables["controls"])
    write_csv(BLOCKERS_CSV, tables["blockers"])
    write_csv(PROMOTION_CSV, tables["promotion"])
    write_csv(DECISION_CSV, tables["decision"])
    write_csv(STATUS_CSV, tables["status"])
    write_csv(NEXT_CSV, tables["next"])
    write_text(DOC_PATH, build_doc(now, tables))
    write_text(FORMAL_PATH, build_formal(now))
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## PPC4161 Local Addendum - Zmem/M2mem Positive Operator Source Or Bound Row

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

4621 turns the local memory plateau into a derived conditional theorem. For `L_mem δm_mem = rho_mem`, positivity of `Z_mem` and `M2_mem` plus zero source and zero boundary flux forces `Delta_v m_mem=0`. If any source survives, the finite route is `||δm||_H1 ≤ CΩ (||rho_mem||_H-1+||q_boundary_mem||_H-1/2)/min(Z_mem_min,M2_mem_min)`, feeding `C_memory_F2 ≤ |kappa_memF2|/Z_Q_eff_min * Delta_v m_mem_bound`. EM invariant, Poynting flux, and high-frequency wave stress are now explicit source-channel rows.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Zmem/M2mem Positive Operator Source Or Bound Row

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The packet no longer treats local memory silence as a plateau axiom. It is allowed only by same-branch positive operator, zero source, and zero boundary flux. Next target: `{NEXT_TARGET}`.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4621 validation failed: {failed}")
    print(f"4621 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
