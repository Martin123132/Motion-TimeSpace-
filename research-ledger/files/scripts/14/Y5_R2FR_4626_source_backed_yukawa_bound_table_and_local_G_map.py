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

CHECKPOINT = "4626"
CLAIM_ID = "L-468"
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_BACKED_YUKAWA_LOCAL_G_MAP_4626"
MARKER = "PPC4161_SOURCE_BACKED_YUKAWA_BOUND_TABLE_AND_LOCAL_G_MAP_4626"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_BACKED_YUKAWA_LOCAL_G_MAP_4626"
DECISION = "SOURCE_BACKED_ANCHORS_READY_FULL_CURVES_AND_MTS_NUMERIC_ROWS_STILL_BLOCK_LOCAL_GR_CLAIM"
NEXT_TARGET = "4627-Y5-R2FR-betaT-Qeff-first-numeric-row-or-exact-zero.md"

DOC_PATH = POST / "4626-Y5-R2FR-source-backed-yukawa-bound-table-and-local-G-map.md"
FORMAL_PATH = FORMAL / "642-PPC4161-source-backed-yukawa-bound-table-and-local-G-map.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4626_SOURCE_REGISTER.csv"
BOUND_ANCHOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4626_SOURCE_BACKED_BOUND_ANCHORS.csv"
LOCAL_MAP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4626_LOCAL_G_BOUND_MAP_ROWS.csv"
MTS_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4626_MTS_YUKAWA_INPUT_REQUIREMENTS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4626_BOUND_RUNNER_DRYRUN_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4626_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4626_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4626_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4626_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4626_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4626_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4626_VALIDATION.csv"

CSV_4625_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4625_NEXT_TARGET.csv"
CSV_4625_CHARGE = SOURCE_DIR / "P8_Y5_R2FR_4625_TRACE_CHARGE_DERIVATION_ROWS.csv"
CSV_4625_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4625_QMEM_ZERO_ROUTES.csv"
CSV_4625_SCREEN = SOURCE_DIR / "P8_Y5_R2FR_4625_SCREENING_OR_MASS_GAP_ROWS.csv"
CSV_4625_YUKAWA = SOURCE_DIR / "P8_Y5_R2FR_4625_YUKAWA_BOUND_MAPPING_ROWS.csv"
CSV_4625_ARENA = SOURCE_DIR / "P8_Y5_R2FR_4625_LOCAL_ARENA_BOUND_ROWS_NONCLAIM.csv"
CSV_4625_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4625_VALIDATION.csv"

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
    local_specs = [
        ("SRC4626_00_4625_next", CSV_4625_NEXT, "4626-Y5-R2FR-source-backed-yukawa-bound-table-and-local-G-map.md", "4625 selected source-backed Yukawa/local-G map."),
        ("SRC4626_01_4625_charge", CSV_4625_CHARGE, "QDER4625_0_gauss_law", "4625 Q_mem charge law."),
        ("SRC4626_02_4625_zero", CSV_4625_ZERO, "QZ4625_0_parent_decoupling", "4625 exact zero route."),
        ("SRC4626_03_4625_screen", CSV_4625_SCREEN, "SCR4625_0_large_gap", "4625 screening/gap row."),
        ("SRC4626_04_4625_yukawa", CSV_4625_YUKAWA, "YB4625_0_alpha_yukawa_map", "4625 Yukawa alpha map."),
        ("SRC4626_05_4625_arena", CSV_4625_ARENA, "ARENA4625_0_R10_short_range", "4625 local arena row."),
        ("SRC4626_06_4625_validation", CSV_4625_VALIDATION, "VAL4625_OVERALL", "4625 validation."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in local_specs:
        text = read_text(path)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "source_kind": "local",
            "path": str(path),
            "path_exists": path.exists(),
            "needle": needle,
            "needle_found": needle in text,
            "line": line_of(path, needle),
            "source_url": "",
            "web_evidence": "",
            "role": role,
            "valid_for_claim": False,
            "timestamp_utc": now,
        })
    web_specs = [
        (
            "WEB4626_0_EOTWASH_2020",
            "https://arxiv.org/abs/2002.11761",
            "arXiv lines 21-23: torsion balance separations 52 um to 3.0 mm; gravitational-strength Yukawa ranges <38.6 um at 95 percent confidence.",
            "R10 short-range inverse-square/Yukawa alpha=1 threshold anchor.",
        ),
        (
            "WEB4626_1_MICROSCOPE_2022",
            "https://arxiv.org/abs/2209.15487",
            "arXiv lines 20-23: MICROSCOPE tests WEP to 1e-15 and reports eta(Ti,Pt)=(-1.5 +/-2.3 stat +/-1.5 syst)e-15 at 1 sigma.",
            "WEP/Eotvos composition anchor.",
        ),
        (
            "WEB4626_2_CASSINI_2003",
            "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "PubMed/search abstract reports gamma = 1 + (2.1 +/- 2.3)e-5.",
            "Solar-system PPN gamma/local-G consistency anchor.",
        ),
    ]
    for source_id, url, evidence, role in web_specs:
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "source_kind": "web_primary_or_indexed",
            "path": "",
            "path_exists": True,
            "needle": "",
            "needle_found": True,
            "line": "",
            "source_url": url,
            "web_evidence": evidence,
            "role": role,
            "valid_for_claim": False,
            "timestamp_utc": now,
        })
    return rows


def bound_anchor_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "anchor_id": "BA4626_0_R10_EOTWASH_ALPHA1",
            "arena": "R10_short_range_inverse_square",
            "observable": "Yukawa alpha(lambda)",
            "lambda_value_m": 3.86e-5,
            "alpha_bound": 1.0,
            "bound_type": "threshold_anchor_alpha_equals_1",
            "confidence": "95_percent",
            "source_url": "https://arxiv.org/abs/2002.11761",
            "source_evidence": "gravitational-strength Yukawa interactions limited to ranges below 38.6 um; separations 52 um to 3.0 mm",
            "full_curve": False,
            "anchor_only": True,
            "usable_for_smoke": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "anchor_id": "BA4626_1_WEP_MICROSCOPE_TiPt",
            "arena": "WEP_Eotvos",
            "observable": "eta_TiPt",
            "lambda_value_m": "",
            "alpha_bound": "",
            "eta_bound_conservative_2sigma": 5.5e-15,
            "bound_type": "derived_2sigma_from_stat_syst_1sigma",
            "confidence": "approx_2sigma_internal_gate",
            "source_url": "https://arxiv.org/abs/2209.15487",
            "source_evidence": "eta(Ti,Pt)=(-1.5 +/- 2.3 stat +/- 1.5 syst)e-15 at 1 sigma; internal 2sigma gate uses 2*sqrt(2.3^2+1.5^2)e-15",
            "full_curve": False,
            "anchor_only": True,
            "usable_for_smoke": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "anchor_id": "BA4626_2_PPN_CASSINI_GAMMA",
            "arena": "solar_system_PPN",
            "observable": "gamma_minus_one",
            "lambda_value_m": "",
            "alpha_bound": "",
            "gamma_minus_one_bound_conservative_2sigma": 6.7e-5,
            "bound_type": "derived_abs_mean_plus_2sigma",
            "confidence": "approx_2sigma_internal_gate",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "source_evidence": "gamma=1+(2.1 +/-2.3)e-5; internal conservative gate uses (abs(2.1)+2*2.3)e-5",
            "full_curve": False,
            "anchor_only": True,
            "usable_for_smoke": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def local_map_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "map_id": "LGM4626_0_R10_alpha",
            "from_mts": "alpha_Y_AB(lambda_mem) ~= alpha_A Q_eff_source/(4*pi Z_mem G M_source)",
            "to_observable": "Yukawa alpha(lambda)",
            "comparison": "require alpha_Y(lambda_mem) <= alpha_bound(lambda_mem)",
            "available_anchor": "BA4626_0_R10_EOTWASH_ALPHA1",
            "claim_status": "ANCHOR_ONLY_FULL_CURVE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "map_id": "LGM4626_1_WEP_eta",
            "from_mts": "eta_AB(lambda) ~= (alpha_A-alpha_B) Q_eff_source exp(-r/lambda)(1+r/lambda)/(4*pi Z_mem g r^2)",
            "to_observable": "Eotvos eta_AB",
            "comparison": "require |eta_AB| <= eta_bound for the relevant composition/source geometry",
            "available_anchor": "BA4626_1_WEP_MICROSCOPE_TiPt",
            "claim_status": "COMPOSITION_AND_GEOMETRY_MAP_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "map_id": "LGM4626_2_orbital_newton",
            "from_mts": "delta_a/a_N ~= alpha_Y exp(-r/lambda_mem)(1+r/lambda_mem)",
            "to_observable": "inverse-square/orbital residual",
            "comparison": "require residual below scale-dependent orbital/local-G bound",
            "available_anchor": "none_yet",
            "claim_status": "SOURCE_BACKED_ORBITAL_BOUND_CURVE_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "map_id": "LGM4626_3_PPN_gamma",
            "from_mts": "metric slip projection c_gamma(lambda)*alpha_Y(lambda)",
            "to_observable": "gamma_minus_one",
            "comparison": "require |gamma-1| <= Cassini-style gamma bound after deriving projection c_gamma",
            "available_anchor": "BA4626_2_PPN_CASSINI_GAMMA",
            "claim_status": "PPN_PROJECTION_COEFFICIENT_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def mts_input_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "input_id": "MIN4626_0_lambda_mem",
            "symbol": "lambda_mem",
            "definition": "sqrt(Z_mem/M2_mem)",
            "needed_for": "all Yukawa/local-G comparisons",
            "current_status": "MISSING_ZMEM_M2MEM_NUMERIC_OR_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "MIN4626_1_Qeff",
            "symbol": "Q_eff_source",
            "definition": "S_scr Q_mem or exact zero",
            "needed_for": "alpha_Y and WEP residuals",
            "current_status": "MISSING_QMEM_ZERO_SCREENING_OR_VALUE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "MIN4626_2_alpha_A",
            "symbol": "alpha_A, alpha_B",
            "definition": "test-body memory sensitivities",
            "needed_for": "WEP and universal Yukawa force mapping",
            "current_status": "MISSING_UNIVERSAL_OR_COMPOSITION_DEPENDENT_SENSITIVITY",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "input_id": "MIN4626_3_bound_curves",
            "symbol": "alpha_bound(lambda), eta_bound(lambda), orbital_bound(lambda)",
            "definition": "source-backed full curves or safe interpolation tables",
            "needed_for": "claim-grade local-G/PPN/Newtonian comparison",
            "current_status": "ANCHORS_ONLY_FULL_CURVES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def runner_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "runner_id": "RUN4626_0_anchor_smoke",
            "input_case": "lambda_mem=38.6e-6 m; alpha_Y numeric supplied",
            "acceptance": "if alpha_Y<=1 at this anchor, R10 anchor smoke passes only at anchor point",
            "failure_mode": "does not prove full curve or other lambda values",
            "ready_to_execute": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "runner_id": "RUN4626_1_missing_mts_inputs",
            "input_case": "current MTS rows with Q_eff/lambda/alpha_A missing",
            "acceptance": "must fail closed with MISSING_MTS_NUMERIC_INPUT",
            "failure_mode": "any pass without Q_eff/lambda/sensitivity is invalid",
            "ready_to_execute": True,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "runner_id": "RUN4626_2_full_claim",
            "input_case": "full source-backed curves plus MTS numeric rows",
            "acceptance": "all relevant arenas pass across the claimed lambda/profile domain",
            "failure_mode": "blocked until full curves or defensible anchors for the claimed domain exist",
            "ready_to_execute": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "control_id": "CTL4626_0_no_anchor_overclaim", "rule": "A single alpha=1 threshold anchor is not a full alpha(lambda) curve.", "violation_blocks_claim": True, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTL4626_1_no_mts_missing_pass", "rule": "No bound runner can pass without lambda_mem, Q_eff, Z_mem and sensitivity rows.", "violation_blocks_claim": True, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTL4626_2_ppn_projection_needed", "rule": "Cassini gamma bounds cannot be applied to MTS until a metric-slip projection coefficient is derived.", "violation_blocks_claim": True, "timestamp_utc": now},
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4626_0_MTS_numeric", "blocks": "any local-G empirical pass", "missing": "lambda_mem, Q_eff_source, alpha_A/B, Z_mem", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4626_1_full_curves", "blocks": "claim-grade R10/WEP/orbital comparison", "missing": "source-backed alpha(lambda), eta(lambda), orbital/local-G bound curves or domain-safe anchors", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4626_2_projection", "blocks": "PPN gamma use", "missing": "MTS metric-slip projection coefficient c_gamma(lambda)", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4626_0_anchor_smoke", "promotion_condition": "MTS provides numeric lambda/Qeff/alpha at anchor and passes the anchor inequality.", "current_result": "blocked_missing_mts_numeric", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4626_1_full_curve", "promotion_condition": "Full source-backed curves and MTS profile domain pass with no extrapolation overclaim.", "current_result": "blocked_missing_full_curves", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4626_2_exact_zero", "promotion_condition": "Q_eff=0 or beta_T=0 parent theorem makes empirical Yukawa comparison unnecessary for that branch.", "current_result": "blocked_parent_zero_unsigned", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "decision_id": "DEC4626_0", "decision": DECISION, "meaning": "Real source-backed anchors now exist for R10 alpha=1, MICROSCOPE WEP and Cassini gamma, but the branch remains nonclaim because MTS numeric inputs and full bound curves are missing.", "status": "NONCLAIM_PRIVATE_EMPIRICAL_INTERFACE_STAGE", "best_route": "derive beta_T/Q_eff exact zero or first numeric row before spending effort on full curves", "next_target": NEXT_TARGET, "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now}
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "status": "PRIVATE_NONCLAIM_EMPIRICAL_INTERFACE_ADVANCE", "summary": "Source-backed anchor table and local-G map written; no claim because anchors are not full curves and MTS numeric rows are missing.", "valid_for_claim": False, "claim_allowed": False, "next_target": NEXT_TARGET, "timestamp_utc": now}
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "branch_id": BRANCH_ID, "timestamp_utc": now, "next_target": NEXT_TARGET, "reason": "The empirical map is ready to accept numbers; the next bottleneck is beta_T/Q_eff/lambda_mem ownership or first numeric smoke row.", "derive_first": "try beta_T=0, Q_eff=0 or parent screening theorem", "fallback": "stage first numeric nonclaim MTS smoke row and run anchor comparisons", "valid_for_claim": False}
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return "\n".join([
        "# 4626 - Source-Backed Yukawa Bound Table And Local-G Map",
        "",
        f"Timestamp UTC: `{now}`",
        f"Branch: `{BRANCH_ID}`",
        f"Marker: `{MARKER}`",
        f"Decision: `{DECISION}`",
        "",
        "## Result",
        "",
        "4626 adds real source-backed bound anchors, but refuses to promote them into a full local-GR claim. The R10 row is an alpha=1 threshold anchor, not a digitized alpha(lambda) curve.",
        "",
        "Main source-backed anchor:",
        "",
        "`lambda = 38.6e-6 m`, `alpha_bound = 1` from the Eot-Wash 2020 short-range inverse-square result.",
        "",
        "Local-G map:",
        "",
        "`alpha_Y_AB(lambda_mem) ~= alpha_A Q_eff_source/(4*pi Z_mem G M_source)` must be compared to `alpha_bound(lambda_mem)`.",
        "",
        "Current verdict: empirical interface is ready for smoke tests, but claim-grade comparison is blocked by missing MTS numeric rows and missing full bound curves.",
        "",
        "## Sources",
        markdown_table(tables["sources"]),
        "",
        "## Source-Backed Bound Anchors",
        markdown_table(tables["anchors"]),
        "",
        "## Local-G Bound Map Rows",
        markdown_table(tables["local_map"]),
        "",
        "## MTS Yukawa Input Requirements",
        markdown_table(tables["mts_inputs"]),
        "",
        "## Bound Runner Dry-Run Rows",
        markdown_table(tables["runner"]),
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
        "All rows remain `valid_for_claim=false`. Anchors can be used for smoke discipline only; full claims require full curves or a parent exact-zero route.",
    ]).strip() + "\n"


def build_formal(now: str) -> str:
    return f"""# 642 - PPC4161 Source-Backed Yukawa Bound Table And Local-G Map

Timestamp UTC: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Branch: `{BRANCH_ID}`

## Empirical Interface

The MTS trace-charge branch maps to a standard Yukawa strength by:

`alpha_Y_AB(lambda_mem) ~= alpha_A Q_eff_source/(4*pi Z_mem G M_source)`.

The source-backed R10 anchor used here is:

`lambda = 38.6e-6 m`, `alpha_bound = 1`, 95 percent threshold anchor from Lee et al. 2020 / Eot-Wash.

This is anchor-only. It is not a full `alpha_bound(lambda)` curve.

WEP and PPN source anchors are recorded for interface discipline:

- MICROSCOPE 2022: internal conservative 2-sigma eta gate `5.5e-15` from the published Ti/Pt result.
- Cassini 2003: internal conservative 2-sigma `|gamma-1|` gate `6.7e-5` from the reported gamma result.

Next target: `{NEXT_TARGET}`.
"""


def append_claim_once() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4626 adds source-backed R10/WEP/PPN anchor rows and maps MTS trace charge to alpha_Y, eta and local-G residual comparisons.",
        "current_evidence": "Generated source register, source-backed anchors, local-G map, MTS input requirements, runner dry-run rows, controls, blockers, promotion gates, decision, status, next target and validation.",
        "status": "source_backed_anchor_table_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Using anchor-only bounds or missing MTS inputs as if they were a full empirical pass.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local-GR/Newton/WEP/PPN pass until MTS numeric rows and source-backed bound curves or exact-zero theorem close.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, ok: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "status": "PASS" if ok else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False})

    local_sources = [row for row in tables["sources"] if row["source_kind"] == "local"]
    web_sources = [row for row in tables["sources"] if row["source_kind"] == "web_primary_or_indexed"]
    add("VAL4626_00_local_sources_exist_and_needles_found", all(row["path_exists"] and row["needle_found"] for row in local_sources), "all local cited paths/needles found")
    add("VAL4626_01_web_sources_recorded", len(web_sources) == 3 and all(row["source_url"] and row["web_evidence"] for row in web_sources), "web source anchors recorded")
    csv_paths = [SOURCE_REGISTER, BOUND_ANCHOR_CSV, LOCAL_MAP_CSV, MTS_INPUT_CSV, RUNNER_CSV, CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    parsed = {path.name: len(read_csv(path)) for path in csv_paths if path.exists()}
    add("VAL4626_02_csv_parse", len(parsed) == len(csv_paths) and all(count > 0 for count in parsed.values()), ";".join(f"{name}:{count}" for name, count in parsed.items()))
    r10 = [row for row in tables["anchors"] if row["anchor_id"] == "BA4626_0_R10_EOTWASH_ALPHA1"]
    add("VAL4626_03_r10_anchor_positive", bool(r10) and float(r10[0]["lambda_value_m"]) > 0 and float(r10[0]["alpha_bound"]) > 0, "positive R10 lambda/alpha anchor")
    add("VAL4626_04_wep_anchor", any(row["anchor_id"] == "BA4626_1_WEP_MICROSCOPE_TiPt" for row in tables["anchors"]), "MICROSCOPE WEP anchor present")
    add("VAL4626_05_local_map", len(tables["local_map"]) >= 4 and any(row["map_id"] == "LGM4626_0_R10_alpha" for row in tables["local_map"]), "local-G map rows present")
    add("VAL4626_06_missing_inputs_fail_closed", any(row["input_id"] == "MIN4626_1_Qeff" for row in tables["mts_inputs"]), "MTS missing-input row present")
    add("VAL4626_07_all_rows_nonclaim", not any(any_claim_true(rows) for rows in tables.values()), "no generated row promotes a claim")
    add("VAL4626_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4626_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4626_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4626_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4626_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4626_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4626_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4626_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4626_OVERALL", all(row["status"] == "PASS" for row in rows), "4626 source-backed anchor/local-G map checkpoint")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "anchors": bound_anchor_rows(now),
        "local_map": local_map_rows(now),
        "mts_inputs": mts_input_rows(now),
        "runner": runner_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": promotion_rows(now),
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(BOUND_ANCHOR_CSV, tables["anchors"])
    write_csv(LOCAL_MAP_CSV, tables["local_map"])
    write_csv(MTS_INPUT_CSV, tables["mts_inputs"])
    write_csv(RUNNER_CSV, tables["runner"])
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
## PPC4161 Local Addendum - Source-Backed Yukawa Bound Table And Local-G Map

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

4626 adds source-backed empirical anchors for the trace-charge/local-G interface. The R10 anchor is `lambda=38.6e-6 m`, `alpha_bound=1`, source-backed to Eot-Wash 2020, but explicitly anchor-only. MICROSCOPE and Cassini anchors are recorded as WEP/PPN guardrails. MTS still needs `lambda_mem`, `Q_eff`, sensitivities and/or an exact-zero theorem before any empirical pass.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Source-Backed Yukawa Bound Table And Local-G Map

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The packet now has a source-backed anchor table and local-G comparison map. Next target: `{NEXT_TARGET}`.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4626 validation failed: {failed}")
    print(f"4626 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
