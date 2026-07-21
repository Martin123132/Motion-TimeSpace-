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

CHECKPOINT = "4625"
CLAIM_ID = "L-467"
BRANCH_ID = "MTS_R2FR_Y5_TRACE_CHARGE_ZERO_SCREENING_YUKAWA_4625"
MARKER = "PPC4161_TRACE_CHARGE_ZERO_SCREENING_OR_YUKAWA_BOUND_ROW_4625"
PACKET_MARKER = "PPC4161_PACKET_TRACE_CHARGE_ZERO_SCREENING_YUKAWA_4625"
DECISION = "QMEM_REDUCED_TO_PARENT_TRACE_CHARGE_SCREENING_OR_EMPIRICAL_YUKAWA_BOUND_NONCLAIM"
NEXT_TARGET = "4626-Y5-R2FR-source-backed-yukawa-bound-table-and-local-G-map.md"

DOC_PATH = POST / "4625-Y5-R2FR-trace-charge-zero-screening-or-yukawa-bound-row.md"
FORMAL_PATH = FORMAL / "641-PPC4161-trace-charge-zero-screening-or-yukawa-bound-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4625_SOURCE_REGISTER.csv"
CHARGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4625_TRACE_CHARGE_DERIVATION_ROWS.csv"
ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4625_QMEM_ZERO_ROUTES.csv"
SCREENING_CSV = SOURCE_DIR / "P8_Y5_R2FR_4625_SCREENING_OR_MASS_GAP_ROWS.csv"
YUKAWA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4625_YUKAWA_BOUND_MAPPING_ROWS.csv"
ARENA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4625_LOCAL_ARENA_BOUND_ROWS_NONCLAIM.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4625_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4625_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4625_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4625_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4625_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4625_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4625_VALIDATION.csv"

CSV_4624_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4624_NEXT_TARGET.csv"
CSV_4624_EXTERIOR = SOURCE_DIR / "P8_Y5_R2FR_4624_TRACE_EXTERIOR_THEOREM_ROWS.csv"
CSV_4624_YUKAWA = SOURCE_DIR / "P8_Y5_R2FR_4624_TRACE_YUKAWA_PROFILE_ROWS.csv"
CSV_4624_WEP = SOURCE_DIR / "P8_Y5_R2FR_4624_WEP_RESIDUAL_VECTOR_ROWS.csv"
CSV_4624_GATES = SOURCE_DIR / "P8_Y5_R2FR_4624_LOCAL_GR_GATES.csv"
CSV_4624_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4624_VALIDATION.csv"
CSV_4623_BETA = SOURCE_DIR / "P8_Y5_R2FR_4623_BETA_OWNERSHIP_MATRIX.csv"
CSV_4623_TRACE = SOURCE_DIR / "P8_Y5_R2FR_4623_TRACE_BRANCH_ROWS.csv"
CSV_4621_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4621_ZMEM_M2MEM_SOURCE_ROWS_NONCLAIM.csv"
CSV_4621_IDENTITY = SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_POSITIVE_OPERATOR_IDENTITY.csv"

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
        ("SRC4625_00_4624_next", CSV_4624_NEXT, "4625-Y5-R2FR-trace-charge-zero-screening-or-yukawa-bound-row.md", "4624 selected Q_mem/screening/Yukawa target."),
        ("SRC4625_01_4624_boundary", CSV_4624_EXTERIOR, "EXT4624_1_boundary_charge_warning", "4624 boundary charge warning."),
        ("SRC4625_02_4624_exact_gate", CSV_4624_EXTERIOR, "EXT4624_2_exact_zero_gate", "4624 exact zero gate."),
        ("SRC4625_03_4624_yukawa", CSV_4624_YUKAWA, "YUK4624_0_spherical_exterior", "4624 Yukawa profile."),
        ("SRC4625_04_4624_trace_charge", CSV_4624_YUKAWA, "YUK4624_1_trace_charge", "4624 trace charge row."),
        ("SRC4625_05_4624_wep", CSV_4624_WEP, "WEP4624_1_species_dependent_trace", "4624 WEP residual row."),
        ("SRC4625_06_4624_gate", CSV_4624_GATES, "GATE4624_1_yukawa_bound", "4624 Yukawa bound gate."),
        ("SRC4625_07_4624_validation", CSV_4624_VALIDATION, "VAL4624_OVERALL", "4624 validation."),
        ("SRC4625_08_4623_betaT", CSV_4623_BETA, "BOWN4623_1_beta_T", "4623 beta_T owner row."),
        ("SRC4625_09_4623_trace", CSV_4623_TRACE, "TR4623_0_minimal_trace_branch", "4623 trace branch row."),
        ("SRC4625_10_4621_Zmem", CSV_4621_SOURCE, "ZMR4621_0_Zmem_min", "4621 Zmem lower row."),
        ("SRC4625_11_4621_M2mem", CSV_4621_SOURCE, "ZMR4621_1_M2mem_min", "4621 M2mem lower row."),
        ("SRC4625_12_4621_nohair", CSV_4621_IDENTITY, "MPI4621_2_nohair_zero", "4621 nohair theorem."),
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


def charge_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "charge_id": "QDER4625_0_gauss_law",
            "statement": "For the trace branch, the exterior scalar charge is the flux of the memory operator through a surface enclosing the body.",
            "derivation": "Integrate L_mem delta_m = rho_mem over the body-plus-boundary matching region. The exterior Yukawa integration constant is fixed by the interior source and boundary flux.",
            "formula": "Q_mem = surface_int Z_mem n.grad(delta_m) dA = int_body rho_mem dV - int_body M2_mem delta_m dV plus matching terms",
            "result": "QMEM_IS_NOT_FREE_BUT_NOT_AUTOMATICALLY_ZERO",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "charge_id": "QDER4625_1_trace_source",
            "statement": "In the weak unscreened trace branch, the first source estimate is Q_mem approximately int_body beta_T T_obs dV.",
            "derivation": "4623 ties visible matter sourcing to the trace owner beta_T. In a weak linear branch the body charge is the volume integral of that trace source up to gap/screening and frame terms.",
            "formula": "Q_mem ~= beta_T int_body T_obs dV for constant beta_T, before screening and binding-energy corrections",
            "result": "TRACE_CHARGE_FIRST_ESTIMATE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "charge_id": "QDER4625_2_compact_object_screened_charge",
            "statement": "With a nonlinear parent potential or environment-dependent gap, the effective charge is Q_eff = S_scr Q_mem with 0 <= S_scr <= 1.",
            "derivation": "Screening can suppress the exterior integration constant, but only if it follows from the parent potential/kinetic operator rather than being appended after the fact.",
            "formula": "Q_eff = S_scr(beta_T,Z_mem,M2_mem,V_parent,environment) * Q_mem",
            "result": "SCREENING_FACTOR_TEMPLATE_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def zero_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_id": "QZ4625_0_parent_decoupling",
            "route": "beta_T=0 parent trace decoupling",
            "condition": "memory does not enter matter masses/metric scale and beta_R frame-equivalent owner is also absent",
            "result": "Q_mem=0 in trace branch",
            "status": "EXACT_IF_PARENT_SIGNED_NOT_CURRENTLY_SIGNED",
            "risk": "also removes the trace branch mechanism, so local/cosmology coupling must come from another owned sector",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "zero_id": "QZ4625_1_scalar_neutral_body",
            "route": "zero net scalar charge",
            "condition": "int_body beta_T T_obs dV plus binding/frame terms cancels exactly",
            "result": "Q_mem=0 for a specified body/source class",
            "status": "POSSIBLE_BUT_BODY_DEPENDENT_NOT_PARENT_GENERAL",
            "risk": "composition dependence makes this dangerous for WEP unless cancellation is universal",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "zero_id": "QZ4625_2_boundary_condition",
            "route": "parent boundary/no-flux condition",
            "condition": "the selected local domain has parent-owned delta_m=0 or Z_mem n.grad(delta_m)=0 and no interior charge leakage",
            "result": "exterior integration constant vanishes",
            "status": "EXACT_IF_BOUNDARY_OWNED_NOT_CLOSURE",
            "risk": "cannot be imposed merely to recover GR; must be a consequence of quotient/local matching",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "zero_id": "QZ4625_3_symmetry_odd_memory",
            "route": "selection symmetry forbids linear trace charge",
            "condition": "m_mem is odd under a parent symmetry while trace matter is even, so beta_T=partial_m ln A_m|branch=0",
            "result": "linear Q_mem=0, with quadratic source still needing a bound",
            "status": "SYMMETRY_ROUTE_OPEN_UNSIGNED",
            "risk": "quadratic or environmental terms may survive",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def screening_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "screen_id": "SCR4625_0_large_gap",
            "mechanism": "large positive M2_mem",
            "derived_effect": "lambda_mem=sqrt(Z_mem/M2_mem) is short, so exterior profile is exponentially suppressed",
            "needed_parent_input": "Z_mem_min and M2_mem_min values or lower bounds from parent Hessian",
            "claim_status": "BOUND_ROUTE_NOT_CLOSED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "screen_id": "SCR4625_1_environmental_screening",
            "mechanism": "density-dependent effective mass or thin-shell suppression",
            "derived_effect": "Q_eff=S_scr Q_mem with S_scr much less than one in dense bodies",
            "needed_parent_input": "nonlinear V_parent(m), coupling beta_T, branch stability, no composition leakage",
            "claim_status": "PARENT_SCREENING_LAW_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "screen_id": "SCR4625_2_universal_absorption",
            "mechanism": "universal trace coupling absorbed into calibrated G over a limited range",
            "derived_effect": "composition-independent scalar correction can look like a Yukawa shift in Newtonian G",
            "needed_parent_input": "universal beta_T and empirical inverse-square/orbital residual bounds",
            "claim_status": "EMPIRICAL_BOUND_ROUTE_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def yukawa_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "map_id": "YB4625_0_alpha_yukawa_map",
            "quantity": "alpha_Y_AB(lambda_mem)",
            "formula": "alpha_Y_AB ~= alpha_A Q_eff_source / (4*pi Z_mem G M_source)",
            "meaning": "maps MTS trace charge to a standard Yukawa-strength parameter for test body A around source body",
            "needed_inputs": "alpha_A, Q_eff_source, Z_mem, M_source, lambda_mem",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "map_id": "YB4625_1_wep_eta_map",
            "quantity": "eta_AB(lambda_mem)",
            "formula": "eta_AB ~= (alpha_A-alpha_B) Q_eff_source exp(-r/lambda_mem)(1+r/lambda_mem)/(4*pi Z_mem g r^2)",
            "meaning": "maps species/composition dependence to Eotvos/WEP residuals",
            "needed_inputs": "alpha_A-alpha_B, Q_eff_source, Z_mem, r, g, lambda_mem",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "map_id": "YB4625_2_newtonian_orbital_map",
            "quantity": "delta_a/a_N",
            "formula": "delta_a/a_N ~= alpha_Y exp(-r/lambda_mem)(1+r/lambda_mem)",
            "meaning": "maps universal scalar force to inverse-square, orbital, lunar/planetary and PPN-style residuals",
            "needed_inputs": "alpha_Y(lambda), orbital scale r, empirical bound curve",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def arena_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "arena_id": "ARENA4625_0_R10_short_range",
            "arena": "R10/short-range inverse-square",
            "uses": "alpha_Y(lambda_mem) bound at sub-mm to meter scales",
            "status": "NEEDS_SOURCE_BACKED_BOUND_CURVE_AND_QEFF",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "arena_id": "ARENA4625_1_WEP_Eotvos",
            "arena": "WEP/Eotvos composition tests",
            "uses": "eta_AB(lambda_mem) bound for composition-dependent alpha_A-alpha_B",
            "status": "NEEDS_COMPOSITION_SENSITIVITY_ROWS",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "arena_id": "ARENA4625_2_orbital_PPN",
            "arena": "orbital/PPN/Newtonian residuals",
            "uses": "universal Yukawa acceleration correction at planetary/lunar/local scales",
            "status": "NEEDS_SCALE_DEPENDENT_BOUND_SOURCE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "control_id": "CTL4625_0_no_charge_magic", "rule": "Do not set Q_mem=0 without parent decoupling, symmetry, boundary theorem, or explicit charge cancellation proof.", "violation_blocks_claim": True, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTL4625_1_screening_not_closure", "rule": "Screening must come from parent potential/gap/branch stability, not an empirical patch.", "violation_blocks_claim": True, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTL4625_2_bound_by_arena", "rule": "If Q_eff survives, map it to at least R10, WEP and orbital/Newtonian residual arenas before any local-GR claim.", "violation_blocks_claim": True, "timestamp_utc": now},
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4625_0_betaT", "blocks": "Q_mem value", "missing": "beta_T derivation/value and universality/species-dependence", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4625_1_Qeff", "blocks": "Yukawa bound mapping", "missing": "Q_eff or parent exact-zero/screening theorem", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4625_2_bound_curves", "blocks": "empirical local-GR recovery claim", "missing": "source-backed alpha_Y(lambda) and eta_AB(lambda) bound curves by arena", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4625_0_exact_charge_zero", "promotion_condition": "Parent proves beta_T=0, exact scalar neutrality, or no-flux/Dirichlet matching without closure.", "current_result": "blocked", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4625_1_screened_charge", "promotion_condition": "Parent derives S_scr and M2_mem/Z_mem so Q_eff and lambda_mem are source-backed.", "current_result": "blocked", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4625_2_empirical_bound", "promotion_condition": "Surviving Q_eff maps below sourced R10/WEP/orbital bound curves.", "current_result": "blocked", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "decision_id": "DEC4625_0", "decision": DECISION, "meaning": "Q_mem is now an owned trace-charge quantity with exact-zero, screening, and empirical-bound routes. No route is claim-ready until parent beta_T/Q_eff or real bound curves exist.", "status": "NONCLAIM_PRIVATE_DERIVATION_STAGE", "best_route": "try parent exact-zero or symmetry first; fallback to source-backed Yukawa/WEP bound table", "next_target": NEXT_TARGET, "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now}
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "status": "PRIVATE_NONCLAIM_DERIVATION_ADVANCE", "summary": "Trace charge Q_mem reduced to parent beta_T volume charge, screening factor or Yukawa/WEP bound mapping.", "valid_for_claim": False, "claim_allowed": False, "next_target": NEXT_TARGET, "timestamp_utc": now}
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "timestamp_utc": now, "next_target": NEXT_TARGET, "reason": "The symbolic bound map is ready; next needs source-backed bound curves/local-G map or a parent exact-zero proof.", "derive_first": "attempt beta_T exact-zero/symmetry/no-flux theorem", "fallback": "build sourced alpha_Y(lambda), eta(lambda), orbital bound table", "valid_for_claim": False}
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return "\n".join([
        "# 4625 - Trace Charge Zero, Screening, Or Yukawa Bound Row",
        "",
        f"Timestamp UTC: `{now}`",
        f"Branch: `{BRANCH_ID}`",
        f"Marker: `{MARKER}`",
        f"Decision: `{DECISION}`",
        "",
        "## Result",
        "",
        "4625 turns the exterior trace-charge problem into an owned equation instead of a vibe. The body charge is not free, but it is also not automatically zero.",
        "",
        "Core relation:",
        "",
        "`Q_mem = surface_int Z_mem n.grad(delta_m) dA = int_body rho_mem dV - int_body M2_mem delta_m dV + matching_terms`.",
        "",
        "Weak trace estimate:",
        "",
        "`Q_mem ~= beta_T int_body T_obs dV`, before screening, binding-energy and frame corrections.",
        "",
        "If charge survives, the standard Yukawa map is:",
        "",
        "`alpha_Y_AB(lambda_mem) ~= alpha_A Q_eff_source/(4*pi Z_mem G M_source)`.",
        "",
        "So local GR is reachable by one of three routes: exact `Q_mem=0`, parent-derived screening/large gap, or empirical Yukawa/WEP/orbital bounds.",
        "",
        "## Sources",
        markdown_table(tables["sources"]),
        "",
        "## Trace Charge Derivation Rows",
        markdown_table(tables["charge"]),
        "",
        "## Q_mem Zero Routes",
        markdown_table(tables["zero"]),
        "",
        "## Screening Or Mass Gap Rows",
        markdown_table(tables["screening"]),
        "",
        "## Yukawa Bound Mapping Rows",
        markdown_table(tables["yukawa"]),
        "",
        "## Local Arena Bound Rows",
        markdown_table(tables["arenas"]),
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
        "All rows remain `valid_for_claim=false`. This is the local-GR scalar-charge gate, not a pass.",
    ]).strip() + "\n"


def build_formal(now: str) -> str:
    return f"""# 641 - PPC4161 Trace Charge Zero, Screening, Or Yukawa Bound Row

Timestamp UTC: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Branch: `{BRANCH_ID}`

## Trace Charge Gate

The exterior integration constant is an owned trace charge:

`Q_mem = surface_int Z_mem n.grad(delta_m) dA = int_body rho_mem dV - int_body M2_mem delta_m dV + matching_terms`.

In the weak trace branch:

`Q_mem ~= beta_T int_body T_obs dV`.

If screening exists:

`Q_eff = S_scr Q_mem`, with `0 <= S_scr <= 1`.

If charge survives, map to a standard Yukawa strength:

`alpha_Y_AB(lambda_mem) ~= alpha_A Q_eff_source/(4*pi Z_mem G M_source)`.

Next target: `{NEXT_TARGET}`.
"""


def append_claim_once() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4625 reduces trace exterior scalar charge to parent beta_T charge, screening, or a Yukawa/WEP bound map.",
        "current_evidence": "Generated trace charge derivation rows, zero routes, screening rows, Yukawa maps, arena rows, controls, blockers, promotion gates, decision, status, next target and validation.",
        "status": "trace_charge_screening_yukawa_bound_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating Q_mem or screening as adjustable closure rather than deriving or source-backing it.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/WEP/Newtonian pass until Q_mem=0, Q_eff screening, or sourced alpha_Y/eta/orbital bounds close.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, ok: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False})

    add("VAL4625_00_sources_exist_and_needles_found", all(row["path_exists"] and row["needle_found"] for row in tables["sources"]), "all cited paths/needles found")
    csv_paths = [SOURCE_REGISTER, CHARGE_CSV, ZERO_CSV, SCREENING_CSV, YUKAWA_CSV, ARENA_CSV, CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    parsed = {path.name: len(read_csv(path)) for path in csv_paths if path.exists()}
    add("VAL4625_01_csv_parse", len(parsed) == len(csv_paths) and all(count > 0 for count in parsed.values()), ";".join(f"{name}:{count}" for name, count in parsed.items()))
    add("VAL4625_02_charge_derivation", any(row["charge_id"] == "QDER4625_0_gauss_law" for row in tables["charge"]), "Q_mem Gauss law row present")
    add("VAL4625_03_zero_routes", len(tables["zero"]) >= 4, "Q_mem zero routes present")
    add("VAL4625_04_yukawa_map", any(row["map_id"] == "YB4625_0_alpha_yukawa_map" for row in tables["yukawa"]), "Yukawa alpha map present")
    add("VAL4625_05_arenas", len(tables["arenas"]) >= 3, "R10/WEP/orbital arenas present")
    add("VAL4625_06_all_rows_nonclaim", not any(any_claim_true(rows) for rows in tables.values()), "no generated row promotes a claim")
    add("VAL4625_07_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4625_08_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4625_09_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4625_10_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4625_11_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4625_12_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4625_13_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4625_14_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4625_OVERALL", all(row["status"] == "PASS" for row in rows), "4625 trace charge/screening/Yukawa checkpoint")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "charge": charge_rows(now),
        "zero": zero_rows(now),
        "screening": screening_rows(now),
        "yukawa": yukawa_rows(now),
        "arenas": arena_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": promotion_rows(now),
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(CHARGE_CSV, tables["charge"])
    write_csv(ZERO_CSV, tables["zero"])
    write_csv(SCREENING_CSV, tables["screening"])
    write_csv(YUKAWA_CSV, tables["yukawa"])
    write_csv(ARENA_CSV, tables["arenas"])
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
## PPC4161 Local Addendum - Trace Charge Zero, Screening, Or Yukawa Bound Row

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

4625 reduces the exterior scalar charge to an owned quantity: `Q_mem = surface_int Z_mem n.grad(delta_m)dA = int_body rho_mem dV - int_body M2_mem delta_m dV + matching_terms`. In the weak trace branch `Q_mem ~= beta_T int_body T_obs dV`. Local GR now needs exact charge zero, parent-derived screening/large gap, or a source-backed Yukawa/WEP/orbital bound map.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Trace Charge Zero, Screening, Or Yukawa Bound Row

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The packet now routes trace-branch local-GR recovery through `Q_mem=0`, `Q_eff=S_scr Q_mem`, or empirical Yukawa/WEP/orbital bounds. Next target: `{NEXT_TARGET}`.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4625 validation failed: {failed}")
    print(f"4625 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
