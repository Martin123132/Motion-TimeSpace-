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

CHECKPOINT = "4622"
CLAIM_ID = "L-464"
BRANCH_ID = "MTS_R2FR_Y5_RHOMEM_SOURCE_CHANNELS_4622"
MARKER = "PPC4161_RHOMEM_SOURCE_CHANNEL_ZERO_OR_EM_POYNTING_BOUND_4622"
PACKET_MARKER = "PPC4161_PACKET_RHOMEM_SOURCE_CHANNELS_4622"
DECISION = "RHOMEM_CHANNEL_DECOMPOSITION_DERIVED_EM_POYNTING_AS_BOUNDARY_OR_FINITE_SOURCE_NONCLAIM"
NEXT_TARGET = "4623-Y5-R2FR-parent-coupling-selection-rule-for-rho-mem.md"

DOC_PATH = POST / "4622-Y5-R2FR-rho-mem-source-channel-zero-or-EM-Poynting-bound.md"
FORMAL_PATH = FORMAL / "638-PPC4161-rho-mem-source-channel-zero-or-EM-Poynting-bound.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4622_SOURCE_REGISTER.csv"
DECOMPOSITION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4622_RHOMEM_CHANNEL_DECOMPOSITION.csv"
EM_POYNTING_CSV = SOURCE_DIR / "P8_Y5_R2FR_4622_EM_POYNTING_ZERO_AND_BOUND_RULES.csv"
LOCAL_TEST_CSV = SOURCE_DIR / "P8_Y5_R2FR_4622_LOCAL_VACUUM_BRANCH_TESTS.csv"
COUPLING_CSV = SOURCE_DIR / "P8_Y5_R2FR_4622_COUPLING_COEFFICIENT_ROWS_NONCLAIM.csv"
BOUND_FEED_CSV = SOURCE_DIR / "P8_Y5_R2FR_4622_BOUND_FEED_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4622_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4622_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4622_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4622_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4622_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4622_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4622_VALIDATION.csv"

CSV_4621_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4621_NEXT_TARGET.csv"
CSV_4621_CHANNEL = SOURCE_DIR / "P8_Y5_R2FR_4621_RHOMEM_SOURCE_CHANNEL_AUDIT.csv"
CSV_4621_IDENTITY = SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_POSITIVE_OPERATOR_IDENTITY.csv"
CSV_4621_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4621_ZMEM_M2MEM_SOURCE_ROWS_NONCLAIM.csv"
CSV_4621_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_AMPLITUDE_BOUND_ROWS.csv"
CSV_4621_CONTROL = SOURCE_DIR / "P8_Y5_R2FR_4621_CONTROL_ROWS.csv"
CSV_4621_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4621_VALIDATION.csv"

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
        ("SRC4622_00_4621_next", CSV_4621_NEXT, "4622-Y5-R2FR-rho-mem-source-channel-zero-or-EM-Poynting-bound.md", "4621 selected rho_mem source-channel target."),
        ("SRC4622_01_4621_poynting", CSV_4621_CHANNEL, "RHO4621_3_Poynting_flux", "4621 Poynting channel."),
        ("SRC4622_02_4621_em", CSV_4621_CHANNEL, "RHO4621_2_EM_invariant", "4621 EM invariant channel."),
        ("SRC4622_03_4621_wave", CSV_4621_CHANNEL, "RHO4621_4_high_frequency_waves", "4621 high-frequency wave channel."),
        ("SRC4622_04_4621_nohair", CSV_4621_IDENTITY, "MPI4621_2_nohair_zero", "4621 no-hair theorem."),
        ("SRC4622_05_4621_bound", CSV_4621_IDENTITY, "MPI4621_3_finite_amplitude_bound", "4621 finite amplitude theorem."),
        ("SRC4622_06_4621_rho", CSV_4621_SOURCE, "ZMR4621_2_rhomem_norm", "4621 rho source row."),
        ("SRC4622_07_4621_boundary", CSV_4621_SOURCE, "ZMR4621_3_boundary_flux", "4621 boundary row."),
        ("SRC4622_08_4621_amp_bound", CSV_4621_BOUND, "AMB4621_1_finite_H1", "4621 H1 bound."),
        ("SRC4622_09_4621_control", CSV_4621_CONTROL, "CTL4621_1_no_Poynting_silence", "4621 no-Poynting-silence control."),
        ("SRC4622_10_4621_validation", CSV_4621_VALIDATION, "VAL4621_OVERALL", "4621 validation."),
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


def decomposition_rows(now: str) -> list[dict[str, Any]]:
    channels = [
        ("RDEC4622_0_curvature", "beta_R R_obs", "local curvature scalar source", "R_obs=0 in exact Ricci-flat exterior, or beta_R=0 by parent selection", "source beta_R and local Ricci scalar norm"),
        ("RDEC4622_1_matter_trace", "beta_T T_obs", "matter trace source", "T_obs=0 in exterior vacuum, or beta_T=0/screened branch", "source beta_T and body trace profile"),
        ("RDEC4622_2_em_invariant", "beta_F F_Q^2 + beta_G F_Q starF_Q", "local EM scalar invariant source", "beta_F=beta_G=0, or null radiation has F^2=F starF=0", "source beta_F,beta_G and local field invariant norms"),
        ("RDEC4622_3_poynting", "beta_S div S_EM", "EM energy-flux/Poynting source", "stationary source-free region gives div S=0; otherwise convert to boundary/absorption term", "source beta_S and boundary/absorption flux"),
        ("RDEC4622_4_wave_stress", "beta_gw rho_gw_eff", "high-frequency gravitational/relic-wave stress source", "beta_gw=0 or wave envelope absent/projected out", "source beta_gw and averaged wave energy density"),
        ("RDEC4622_5_hidden", "J_hidden", "hidden or quotient leakage source", "no-Hom/typed-domain exclusion of hidden memory source", "source hidden current norm or prove projection zero"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "channel_id": channel_id,
            "rho_piece": rho_piece,
            "interpretation": interpretation,
            "zero_route": zero_route,
            "finite_route": finite_route,
            "current_status": "MISSING_PARENT_COUPLING_SELECTION_OR_SOURCE_NORM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
        for channel_id, rho_piece, interpretation, zero_route, finite_route in channels
    ]


def em_poynting_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "rule_id": "EMP4622_0_null_wave_scalar_zero",
            "object": "source-free null EM radiation",
            "derivation": "For a null EM wave, F_Q^2=2(B^2-E^2/c^2)=0 and F_Q starF_Q is proportional to E·B=0, so scalar invariant memory sources vanish if rho_mem only sees those invariants.",
            "zero_condition": "rho_mem EM part uses only F^2 and F starF and the field is null/radiative on the branch",
            "bound_condition": "near-field/static/non-null EM requires finite invariant norms instead",
            "result": "EXACT_CONDITIONAL_EM_SCALAR_ZERO",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "rule_id": "EMP4622_1_poynting_volume_to_boundary",
            "object": "Poynting vector S_EM",
            "derivation": "Poynting theorem gives div S_EM = -partial_t u_EM - J·E. In a stationary source-free volume this is zero; in general it becomes absorption/storage or boundary flux, not an unconstrained local source.",
            "zero_condition": "partial_t u_EM=0, J·E=0, and net boundary flux is zero on the chosen local domain",
            "bound_condition": "||div S||_H-1 bounded by time-varying EM energy storage, Joule/absorption power, or |S·n| boundary flux",
            "result": "POYNTING_IS_BOUNDARY_OR_FINITE_SOURCE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "rule_id": "EMP4622_2_static_EM_not_zero",
            "object": "electrostatic/magnetostatic local fields",
            "derivation": "Static fields can have nonzero F_Q^2 even when div S_EM=0, so the EM scalar-invariant channel is not killed by Poynting silence.",
            "zero_condition": "beta_F=beta_G=0 or typed-domain/no-Hom exclusion",
            "bound_condition": "finite local E^2, B^2 and E·B norms with parent beta coefficients",
            "result": "STATIC_EM_REQUIRES_COUPLING_RULE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "rule_id": "EMP4622_3_wave_stress_not_free",
            "object": "high-frequency gravitational/relic-wave stress",
            "derivation": "Averaged high-frequency waves behave like a positive stress envelope. If memory couples to that envelope, zero requires beta_gw=0 or absence/projection of the envelope; otherwise it is a finite source norm.",
            "zero_condition": "beta_gw=0, no local wave bath, or parent projection removes rho_gw_eff",
            "bound_condition": "finite rho_gw_eff envelope and beta_gw value",
            "result": "WAVE_CHANNEL_REDUCED_TO_COUPLING_OR_BOUND",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def local_test_rows(now: str) -> list[dict[str, Any]]:
    tests = [
        ("LVT4622_0_exterior_vacuum", "outside compact neutral body", "T_obs=0, R_obs≈0 under GR limit, no local currents", "EM/wave/background flux channels still need zero or bounds"),
        ("LVT4622_1_inside_matter", "inside material body", "T_obs generally nonzero and static EM fields can be nonzero", "requires beta_T/beta_F rules or finite body-profile source"),
        ("LVT4622_2_source_free_light", "freely propagating light/radiation", "F^2=F starF=0 and div S=0 for ideal null stationary beam segment", "boundary flux and wave packet time-dependence still need domain rule"),
        ("LVT4622_3_laboratory_fields", "lab EM fields/clocks/R10", "static/non-null EM invariants and material traces may be measurable", "good arena for bounds, bad arena for pretending source silence"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "test_id": test_id,
            "branch": branch,
            "what_zeroes": what_zeroes,
            "what_remains": what_remains,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        }
        for test_id, branch, what_zeroes, what_remains in tests
    ]


def coupling_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("COUP4622_0_beta_R", "beta_R", "curvature coupling to memory source", "MISSING_PARENT_SELECTION_OR_VALUE", "dimension depends on memory normalization"),
        ("COUP4622_1_beta_T", "beta_T", "matter-trace coupling to memory source", "MISSING_PARENT_SELECTION_OR_VALUE", "memory-source per stress trace"),
        ("COUP4622_2_beta_F", "beta_F", "EM invariant F_Q^2 coupling to memory source", "MISSING_PARENT_SELECTION_OR_VALUE", "memory-source per EM invariant"),
        ("COUP4622_3_beta_G", "beta_G", "pseudoscalar EM invariant F_Q starF_Q coupling", "MISSING_PARITY_OR_SELECTION_RULE", "memory-source per EM pseudoscalar"),
        ("COUP4622_4_beta_S", "beta_S", "Poynting/divergence or flux coupling", "MISSING_BOUNDARY_COUPLING_RULE", "memory-source per energy-flux divergence"),
        ("COUP4622_5_beta_gw", "beta_gw", "high-frequency wave stress coupling", "MISSING_PARENT_SELECTION_OR_VALUE", "memory-source per wave energy density"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "value": value,
            "units": units,
            "source_required": "parent action/source functional, quotient typing, or calibrated matching row",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
        for row_id, symbol, definition, value, units in specs
    ]


def bound_feed_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "feed_id": "BF4622_0_rho_norm",
            "quantity": "||rho_mem||_H-1",
            "formula": "≤ Σ |beta_i| ||source_i||_H-1 + ||J_hidden||_H-1",
            "feeds": "4621 finite amplitude bound",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "feed_id": "BF4622_1_boundary_flux",
            "quantity": "||q_boundary_mem||_H-1/2",
            "formula": "includes beta_S ||S_EM·n|| plus any memory matching flux at ∂Ω",
            "feeds": "4621 boundary term",
            "status": "BOUNDARY_RULE_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "feed_id": "BF4622_2_nohair_gate",
            "quantity": "Delta_v m_mem",
            "formula": "Delta_v m_mem=0 only if every rho channel and q_boundary channel is zero on the same branch",
            "feeds": "local PPN/R10/clock residual suppression",
            "status": "EXACT_GATE_NOT_CLOSED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "control_id": "CTL4622_0_no_source_silence", "rule": "Every rho_mem term must be zero by typing/symmetry/field equation or carried as a finite bound.", "violation_blocks_claim": True, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTL4622_1_static_EM_warning", "rule": "Poynting silence does not kill static EM scalar invariants.", "violation_blocks_claim": True, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTL4622_2_same_domain", "rule": "Volume source and boundary flux must be evaluated on the same local domain used in the 4621 operator.", "violation_blocks_claim": True, "timestamp_utc": now},
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4622_0_couplings", "blocks": "rho_mem zero or finite value", "missing": "beta_R,beta_T,beta_F,beta_G,beta_S,beta_gw parent selection/value rows", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4622_1_domain_profiles", "blocks": "finite amplitude scoring", "missing": "R,T,F^2,FstarF,divS/radiative flux,wave envelope norms on selected local domain", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "BLK4622_2_hidden_current", "blocks": "no-hair proof", "missing": "J_hidden no-Hom/projection-zero proof or finite norm", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": now},
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4622_0_exact_source_zero", "promotion_condition": "All beta/source channels are parent-zero or field-equation zero, and boundary flux is zero on the same domain.", "current_result": "blocked", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4622_1_finite_source_bound", "promotion_condition": "All surviving beta/source channels and boundary fluxes have source-backed numerical/norm rows.", "current_result": "blocked", "valid_for_claim": False, "claim_allowed": False, "timestamp_utc": now},
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4622_0",
            "decision": DECISION,
            "meaning": "rho_mem is now decomposed; EM/Poynting/wave ideas are kept but disciplined as scalar invariants, conservation-law boundary terms, or finite source norms.",
            "status": "NONCLAIM_PRIVATE_DERIVATION_STAGE",
            "best_route": "derive parent selection rules for beta coefficients; do not infer them from phenomenology",
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
            "summary": "rho_mem source channels decomposed; Poynting vector route is boundary/finite-source controlled; next is parent coupling selection.",
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
            "reason": "The source-channel structure is clear; the live theory question is which beta couplings are parent-allowed.",
            "derive_first": "selection rule for beta_R,beta_T,beta_F,beta_G,beta_S,beta_gw",
            "fallback": "finite source-backed coupling rows and local profile norms",
            "valid_for_claim": False,
        }
    ]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return "\n".join([
        "# 4622 - rho_mem Source Channel Zero Or EM/Poynting Bound",
        "",
        f"Timestamp UTC: `{now}`",
        f"Branch: `{BRANCH_ID}`",
        f"Marker: `{MARKER}`",
        f"Decision: `{DECISION}`",
        "",
        "## Result",
        "",
        "4622 attacks the coupling/source fork directly. The local memory source is decomposed as:",
        "",
        "`rho_mem = beta_R R_obs + beta_T T_obs + beta_F F_Q^2 + beta_G F_Q starF_Q + beta_S div S_EM + beta_gw rho_gw_eff + J_hidden`.",
        "",
        "This is not a claim. It is the bookkeeping needed to stop source terms being smuggled in or silently dropped.",
        "",
        "Key result: the Poynting vector is not ignored. By Poynting's theorem, `div S_EM = -partial_t u_EM - J·E`, so in a stationary source-free volume it vanishes, while in real domains it becomes absorption/storage or boundary flux. Static EM fields can still have nonzero `F_Q^2`, so Poynting silence alone does **not** kill EM memory sourcing.",
        "",
        "## Sources",
        markdown_table(tables["sources"]),
        "",
        "## rho_mem Channel Decomposition",
        markdown_table(tables["decomposition"]),
        "",
        "## EM/Poynting Rules",
        markdown_table(tables["em_poynting"]),
        "",
        "## Local Vacuum Branch Tests",
        markdown_table(tables["local_tests"]),
        "",
        "## Coupling Coefficient Rows",
        markdown_table(tables["couplings"]),
        "",
        "## Bound Feed Rows",
        markdown_table(tables["bound_feed"]),
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
        "All rows remain `valid_for_claim=false`. No local-GR, PPN, clock, R10, or Maxwell claim is allowed until the beta couplings are parent-selected or source-backed.",
    ]).strip() + "\n"


def build_formal(now: str) -> str:
    return f"""# 638 - PPC4161 rho_mem Source Channel Zero Or EM/Poynting Bound

Timestamp UTC: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Branch: `{BRANCH_ID}`

## Source Decomposition

`rho_mem = beta_R R_obs + beta_T T_obs + beta_F F_Q^2 + beta_G F_Q starF_Q + beta_S div S_EM + beta_gw rho_gw_eff + J_hidden`.

Poynting theorem gives:

`div S_EM = -partial_t u_EM - J·E`.

Therefore Poynting-vector sourcing is zero only in a stationary source-free volume with zero relevant boundary flux. Otherwise it is a finite source/boundary term for the 4621 memory amplitude bound.

Null EM radiation can kill scalar invariant channels because `F_Q^2=0` and `F_Q starF_Q=0`, but static/non-null local fields do not. High-frequency waves reduce to a coupling coefficient and an averaged stress envelope.

Next target: `{NEXT_TARGET}`.
"""


def append_claim_once() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4622 decomposes rho_mem source channels and derives the EM/Poynting route as zero only by source-free stationarity/boundary silence or finite source bounds.",
        "current_evidence": "Generated channel decomposition, EM/Poynting rules, local branch tests, coupling coefficient rows, bound feeds, controls, blockers, promotion gates, decision, status, next target and validation.",
        "status": "rho_mem_channel_decomposition_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating Poynting silence as equivalent to all EM source silence; static EM invariants can survive.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No local suppression claim until parent coupling selection or finite source-backed beta/profile rows exist.",
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

    add("VAL4622_00_sources_exist_and_needles_found", all(row["path_exists"] and row["needle_found"] for row in tables["sources"]), "all cited paths/needles found")
    csv_paths = [SOURCE_REGISTER, DECOMPOSITION_CSV, EM_POYNTING_CSV, LOCAL_TEST_CSV, COUPLING_CSV, BOUND_FEED_CSV, CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    parsed = {path.name: len(read_csv(path)) for path in csv_paths if path.exists()}
    add("VAL4622_01_csv_parse", len(parsed) == len(csv_paths) and all(count > 0 for count in parsed.values()), ";".join(f"{name}:{count}" for name, count in parsed.items()))
    add("VAL4622_02_poynting_rule", any(row["rule_id"] == "EMP4622_1_poynting_volume_to_boundary" for row in tables["em_poynting"]), "Poynting boundary/finite source rule present")
    add("VAL4622_03_static_em_warning", any(row["rule_id"] == "EMP4622_2_static_EM_not_zero" for row in tables["em_poynting"]), "static EM warning present")
    add("VAL4622_04_coupling_rows", len(tables["couplings"]) >= 6 and any(row["symbol"] == "beta_S" for row in tables["couplings"]), "beta coupling rows present")
    add("VAL4622_05_all_rows_nonclaim", not any(any_claim_true(rows) for rows in tables.values()), "no generated row promotes a claim")
    add("VAL4622_06_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4622_07_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4622_08_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4622_09_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4622_10_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4622_11_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4622_12_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4622_13_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4622_OVERALL", all(row["status"] == "PASS" for row in rows), "4622 rho_mem source-channel checkpoint")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "decomposition": decomposition_rows(now),
        "em_poynting": em_poynting_rows(now),
        "local_tests": local_test_rows(now),
        "couplings": coupling_rows(now),
        "bound_feed": bound_feed_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": promotion_rows(now),
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(DECOMPOSITION_CSV, tables["decomposition"])
    write_csv(EM_POYNTING_CSV, tables["em_poynting"])
    write_csv(LOCAL_TEST_CSV, tables["local_tests"])
    write_csv(COUPLING_CSV, tables["couplings"])
    write_csv(BOUND_FEED_CSV, tables["bound_feed"])
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
## PPC4161 Local Addendum - rho_mem Source Channel Zero Or EM/Poynting Bound

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

4622 decomposes `rho_mem` into curvature, matter trace, EM scalar invariants, Poynting flux/divergence, wave stress and hidden-current terms. The Poynting route is disciplined by `div S_EM=-partial_t u_EM-J·E`: zero only in stationary source-free domains with zero boundary flux, otherwise a finite boundary/source norm. Static EM invariants can survive even when Poynting divergence is silent.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - rho_mem Source Channel Zero Or EM/Poynting Bound

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The packet now routes local memory sourcing through explicit beta couplings and local profile norms. Next target: `{NEXT_TARGET}`.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4622 validation failed: {failed}")
    print(f"4622 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
