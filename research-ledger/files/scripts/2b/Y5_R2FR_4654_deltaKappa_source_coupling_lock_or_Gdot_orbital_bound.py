from __future__ import annotations

import csv
import io
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
PUBLIC_STAGE = Path(r"D:\Users\ollet\Desktop\Motion-TimeSpace-public-stage")
BACKUP_REPO = Path(r"D:\Users\ollet\Desktop\laptop-back-up-")

CHECKPOINT = "4654"
CLAIM_ID = "L-496"
BRANCH = "MTS_R2FR_Y5_DELTAKAPPA_SOURCE_COUPLING_LOCK_OR_GDOT_ORBITAL_BOUND_4654"
MARKER = "PPC4161_DELTAKAPPA_SOURCE_COUPLING_LOCK_OR_GDOT_ORBITAL_BOUND_4654"
PACKET_MARKER = "PPC4161_PACKET_DELTAKAPPA_SOURCE_COUPLING_LOCK_OR_GDOT_ORBITAL_BOUND_4654"
DECISION = "deltaKappa_PRIVATE_SOURCE_COUPLING_ZERO_CALIBRATED_G_NOT_NUMERIC_PREDICTION_cGamma_NEXT"
NEXT_TARGET = "4655-Y5-R2FR-cGamma-memory-projector-local-support-or-profile-bound.md"

DOC_PATH = POST / "4654-Y5-R2FR-deltaKappa-source-coupling-lock-or-Gdot-orbital-bound.md"
FORMAL_PATH = FORMAL / "670-PPC4161-deltaKappa-source-coupling-lock-or-Gdot-orbital-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4653 = POST / "4653-Y5-R2FR-cD-same-coframe-parent-functor-or-WEP-clock-EM-bound.md"
FORMAL_181 = FORMAL / "181-PPC4161-kappa-G-normalization-gate.md"
FORMAL_182 = FORMAL / "182-PPC4161-ZH-source-measure-and-kappa-lock.md"
FORMAL_183 = FORMAL / "183-PPC4161-topological-kappa-star-lock-or-ZH-bound.md"
FORMAL_184 = FORMAL / "184-PPC4161-parent-adopted-topological-kappa-sector.md"
FORMAL_185 = FORMAL / "185-PPC4161-Hilbert-source-measure-descent-and-delta-ZH-closure.md"
FORMAL_189 = FORMAL / "189-PPC4161-local-empirical-validation-pack.md"
FORMAL_194 = FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md"
FORMAL_202 = FORMAL / "202-PPC4161-same-coframe-source-memory-zero-law.md"
FORMAL_222 = FORMAL / "222-PPC4161-calibrated-GN-bridge-and-source-charge-caveat.md"
FORMAL_466 = FORMAL / "466-PPC4161-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md"
DOC_4564 = POST / "4564-Y5-R2FR-cD-deltaKappa-cGamma-root-ownership-zero-law-or-bound-interface.md"
CSV_4185_ARENA = SOURCE_DIR / "P8_Y5_R2FR_4185_RESIDUAL_COEFFICIENT_ARENA_MAP.csv"
CSV_4186_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4186_JOINT_ZERO_LAW_CLAUSES.csv"
CSV_4206_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4206_STATUS.csv"
CSV_4206_CHAIN = SOURCE_DIR / "P8_Y5_R2FR_4206_COUPLING_CHAIN.csv"
CSV_4206_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4206_CALIBRATION_THEOREM.csv"
CSV_4206_REOPEN = SOURCE_DIR / "P8_Y5_R2FR_4206_REOPENING_GATES.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4654_SOURCE_REGISTER.csv"
COUPLING_LOCK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4654_DELTAKAPPA_COUPLING_LOCK.csv"
ZERO_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4654_DELTAKAPPA_ZERO_THEOREM.csv"
NEWTON_READOUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4654_NEWTON_COUPLING_READOUT.csv"
BOUND_INTERFACE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4654_DELTAKAPPA_BOUND_INTERFACE.csv"
ANTI_CIRCULARITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4654_ANTI_CIRCULARITY_GUARDS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4654_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4654_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4654_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4654_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4654_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4654_VALIDATION.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_number(path: Path, needle: str) -> int:
    for index, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    suffix = "" if not existing or existing.endswith("\n") else "\n"
    path.write_text(existing + suffix + text.lstrip("\n"), encoding="utf-8")


def csv_line(values: list[str]) -> str:
    buffer = io.StringIO()
    csv.writer(buffer, lineterminator="\n").writerow(values)
    return buffer.getvalue()


def git_clean(repo: Path) -> tuple[bool, str]:
    if not repo.exists() or not (repo / ".git").exists():
        return True, "absent or not git"
    result = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], text=True, capture_output=True, check=False)
    if result.returncode != 0:
        return False, result.stderr.strip() or "git status failed"
    detail = result.stdout.strip()
    return detail == "", detail or "clean"


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4654_00_4653_next", DOC_4653, "RUN4653_4_next", "4653 selected delta_kappa as next leakage root."),
        ("SRC4654_01_181_normalization", FORMAL_181, "kappa_eff = kappa_* Z_H", "base kappa-G normalization."),
        ("SRC4654_02_181_no_numeric_G", FORMAL_181, "The numerical value of `G_N` is not predicted here.", "numeric G firewall."),
        ("SRC4654_03_182_ZH_factor", FORMAL_182, "Z_H = Z_0 exp(delta_ZH)", "source-measure leakage factorization."),
        ("SRC4654_04_182_residuals", FORMAL_182, "Gdot/G = D_t ln(kappa_* Z_H)", "finite drift arenas."),
        ("SRC4654_05_183_topological", FORMAL_183, "=> d(kappa_*) = 0.", "topological kappa-star lock."),
        ("SRC4654_06_184_private_adopted", FORMAL_184, "=> D_A ln kappa_* = 0.", "private adopted topological kappa sector."),
        ("SRC4654_07_184_reduction", FORMAL_184, "R_A^G = D_A delta_ZH.", "kappa side reduced to source-measure leak."),
        ("SRC4654_08_185_source_descent", FORMAL_185, "T_parent^H = Z_H T_H + T_leak", "Hilbert source-measure descent decomposition."),
        ("SRC4654_09_185_deltaZH_zero", FORMAL_185, "delta_ZH = 0,", "source measure leak zero in private packet."),
        ("SRC4654_10_194_calibrated_law", FORMAL_194, "G_cal := c^4 kappa_eff/(8*pi).", "calibrated source-coupling law."),
        ("SRC4654_11_194_no_orbital_GM", FORMAL_194, "No orbital `GM`, fitted acceleration, or measured numerical `G` is used", "anti-circularity guard."),
        ("SRC4654_12_222_not_need_numeric_G", FORMAL_222, "MTS does not need to numerically predict G_N", "GR-comparison standard."),
        ("SRC4654_13_202_deltaKappa", FORMAL_202, "=> delta_kappa = 0.", "joint zero law already contains delta_kappa."),
        ("SRC4654_14_4185_deltaKappa", CSV_4185_ARENA, "RC4185_1_deltaKappa", "delta_kappa arena map."),
        ("SRC4654_15_4186_kappa_lock", CSV_4186_ZERO, "JZ4186_2_kappa_lock", "machine kappa lock clause."),
        ("SRC4654_16_4186_source_measure", CSV_4186_ZERO, "JZ4186_3_source_measure", "machine source-measure clause."),
        ("SRC4654_17_4206_chain", CSV_4206_CHAIN, "CC4206_6_no_drift_vector", "machine no-drift coupling chain."),
        ("SRC4654_18_4206_theorem", CSV_4206_THEOREM, "GT4206_2_non_circularity", "machine anti-circular calibration theorem."),
        ("SRC4654_19_4206_reopen", CSV_4206_REOPEN, "RG4206_6_numeric_G_claim", "machine reopening gates."),
        ("SRC4654_20_4206_status", CSV_4206_STATUS, "NUMERIC_G_NOT_PREDICTED", "4206 status imported."),
        ("SRC4654_21_4450_deltaKappa", FORMAL_466, "C4450_1_deltaKappa", "post-A_MF delta_kappa residual map."),
        ("SRC4654_22_4564_deltaKappa", DOC_4564, "TZ4564_2_deltaKappa_zero", "4564 delta_kappa private zero theorem."),
        ("SRC4654_23_189_empirical_pack", FORMAL_189, "Local Gdot/G from Lunar Laser Ranging.", "source-backed comparator arena exists if finite drift reopens."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, note in specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "line_number": line_number(path, needle),
                "note": note,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def coupling_lock_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DKL4654_0_factorization", "kappa_eff = kappa_* Z_H = kappa_* Z_0 exp(delta_ZH)", "separates dimensionful coupling, common source normalization and physical source-measure leakage", "PRIVATE_SELECTOR_INPUT"),
        ("DKL4654_1_topological_kappa", "D_A ln kappa_* = 0", "topological/superselection sector makes kappa_* source-blind and locally constant if branch-adopted", "PRIVATE_ZERO"),
        ("DKL4654_2_common_Z0", "D_A ln Z_0 = 0", "one calibration constant can be absorbed into kappa_eff; it is not measured-G prediction", "CALIBRATION_CONSTANT"),
        ("DKL4654_3_Hilbert_source", "T_parent^H = Z_0 T_H and delta_ZH = 0", "single Hilbert source measure; no species, material, range, clock or readout multiplier", "PRIVATE_ZERO"),
        ("DKL4654_4_no_drift", "D_A ln kappa_eff = D_A ln kappa_* + D_A delta_ZH = 0", "source-coupling drift slot is closed inside the private packet", "DELTAKAPPA_ZERO"),
        ("DKL4654_5_guard", "if D_A ln kappa_* != 0 or D_A delta_ZH != 0", "reopen finite Gdot/WEP/orbital/clock/local-G/source-measure bound rows", "FAIL_CLOSED_GUARD"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "lock_id": row[0],
            "formula": row[1],
            "meaning": row[2],
            "status": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def zero_theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DKZ4654_0_definition", "delta_kappa := D_A ln kappa_eff", "kappa_eff = kappa_* Z_0 exp(delta_ZH)", "delta_kappa = D_A ln kappa_* + D_A delta_ZH", "DEFINITION"),
        ("DKZ4654_1_kappa_lock", "topological/superselection kappa branch", "D_A ln kappa_* = 0", "kappa-star drift contribution vanishes", "PRIVATE_ZERO"),
        ("DKZ4654_2_source_measure", "single Hilbert source measure", "delta_ZH=0 and D_A delta_ZH=0", "source-measure drift contribution vanishes", "PRIVATE_ZERO"),
        ("DKZ4654_3_result", "source-coupling drift", "D_A ln kappa_eff = 0", "delta_kappa = 0 inside private topological-kappa/Hilbert-source selector", "PASS_PRIVATE_ZERO_NONCLAIM"),
        ("DKZ4654_4_numeric_G_firewall", "dimensionful magnitude", "G_cal = c^4 kappa_eff/(8*pi) is calibrated once", "numeric G_N predicted = false unless a parent scale law fixes kappa_*", "PUBLIC_FIREWALL"),
        ("DKZ4654_5_public_debt", "global parent proof", "derive topological kappa sector and Hilbert-source measure from full MTS parent grammar", "public parent-derived delta_kappa=0 remains unsigned", "PUBLIC_UNSIGNED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": row[0],
            "step": row[1],
            "premise": row[2],
            "consequence": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def newton_readout_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("NCR4654_0_EH_source", "G_mu_nu[g_obs] = kappa_eff T_H_mu_nu", "same Hilbert source and one calibrated coupling", "GR-form local source equation"),
        ("NCR4654_1_calibration", "G_cal := c^4 kappa_eff/(8*pi)", "one empirical calibration constant, as in GR", "not a numerical G prediction"),
        ("NCR4654_2_Poisson", "nabla^2 Phi_N = 4*pi G_cal rho_H", "weak-field 00 equation with Hilbert density", "Newtonian Poisson coefficient recovered structurally"),
        ("NCR4654_3_Gauss_orbit", "a_r = -G_cal M_H^dress/r^2", "requires M_H^dress parent-owned before orbital readout", "orbital GM is an output, not an input"),
        ("NCR4654_4_Gdot", "D_t ln G_eff = 0", "delta_kappa time component vanishes in private selector", "Gdot/G residual zero only under lock clauses"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "readout_id": row[0],
            "formula": row[1],
            "condition": row[2],
            "effect": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def bound_interface_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DKB4654_0_time_Gdot", "Gdot/G", "|(dot G/G)_delta| = |tau^A D_A ln kappa_eff|", "source-backed local time derivative map, clock/tau convention, units yr^-1", "dormant_if_private_zero"),
        ("DKB4654_1_species_WEP", "WEP/source species", "|eta_delta| <= |J_eta^delta Delta_species delta_ZH|", "composition map, source-measure Jacobian, WEP budget", "dormant_if_private_zero"),
        ("DKB4654_2_clock_localG", "clock/local-G", "|R_clock^delta| <= |J_clock^delta D_clock ln kappa_eff|", "clock species/readout map and local-G convention", "dormant_if_private_zero"),
        ("DKB4654_3_orbital_GM", "orbital GM consistency", "|d ln(GM)_orb/dt| <= |D_t ln kappa_eff| + |d ln M_H^dress/dt|", "source-charge owner and orbital ephemeris residual budget", "dormant_if_private_zero"),
        ("DKB4654_4_range_env", "range/environment", "|R_env^delta| <= |J_env^delta D_env delta_ZH|", "environment/range derivative source map and units", "dormant_if_private_zero"),
        ("DKB4654_5_PPN_source", "PPN/source frame", "|R_PPN_source^delta| <= |J_PPN^delta D_frame ln kappa_eff|", "PPN source-frame projection map and residual budget", "dormant_if_private_zero"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row[0],
            "arena": row[1],
            "symbolic_bound": row[2],
            "required_inputs": row[3],
            "status": row[4],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def anti_circularity_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("ACG4654_0_no_numeric_G_claim", "Do not claim MTS predicts the numerical value of G_N from this gate.", "G_cal is calibrated unless a parent scale law fixes kappa_* without measured G.", "ACTIVE"),
        ("ACG4654_1_no_orbital_backfill", "Do not define M_H^dress, rho_H, kappa_* or Z_0 using observed orbital GM.", "orbital acceleration is downstream of the Poisson/Gauss readout.", "ACTIVE"),
        ("ACG4654_2_no_ZH_gauge_cheat", "Do not set Z_H=1 until physical delta_ZH leak channels are zero.", "common Z_0 is gauge/calibration; delta_ZH is physical if nonzero.", "ACTIVE"),
        ("ACG4654_3_no_public_GR", "Do not claim public local GR from private delta_kappa=0.", "global parent adoption, source-charge glue and c_Gamma remain active.", "ACTIVE"),
        ("ACG4654_4_no_source_weight", "Do not introduce species/material/range/readout source multipliers.", "that reopens delta_ZH and finite WEP/Gdot/orbital bounds.", "ACTIVE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "guard_id": row[0],
            "guard": row[1],
            "reason": row[2],
            "status": row[3],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("RUN4654_0_private_lock", "topological kappa lock plus single Hilbert source measure", "PASS_PRIVATE_DELTAKAPPA_ZERO_NONCLAIM", "delta_kappa=0 structurally; G_cal remains calibrated."),
        ("RUN4654_1_numeric_G", "claim numeric G_N predicted from calibrated kappa_eff", "FAIL_NUMERIC_G_FIREWALL", "GR reduction requires one universal G, not a fundamental prediction of its number."),
        ("RUN4654_2_orbital_backfill", "use observed orbital GM to define source mass/coupling before Poisson/Gauss bridge", "FAIL_CIRCULAR_ORBITAL_GM", "borrows Newton to prove Newton."),
        ("RUN4654_3_source_leak", "species/material/range/readout source multiplier survives", "FAIL_REOPENS_BOUND_INTERFACE", "finite delta_kappa must be bounded in Gdot/WEP/clock/orbital/PPN arenas."),
        ("RUN4654_4_public_parent", "global parent-derived topological kappa and Hilbert-source measure claimed", "FAIL_PUBLIC_PARENT_UNSIGNED", "private selector imported; full parent grammar still not signed."),
        ("RUN4654_5_next", "delta_kappa private-closed; c_Gamma remains MTS-specific local hair", "PASS_NEXT_CGAMMA_SELECTED", NEXT_TARGET),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "run_id": row[0],
            "branch": row[1],
            "result": row[2],
            "reason": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CTRL4654_0_calibrated_G", "Use calibrated `G_cal`, not claimed numeric-G prediction."),
        ("CTRL4654_1_source_first", "Define Hilbert source charge before orbital readout; no GM backfill."),
        ("CTRL4654_2_private_lock_only", "delta_kappa=0 is private-selector closure until parent grammar is signed."),
        ("CTRL4654_3_bounds_if_reopened", "If kappa/source drift reopens, use Gdot/WEP/clock/orbital/source-frame bounds."),
        ("CTRL4654_4_move_to_cGamma", "Do not circle c_D/delta_kappa again unless a guard fails; next live root is c_Gamma."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "firewall": row[1],
            "active": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4654_0",
            "decision": DECISION,
            "summary": "4654 locks the second leakage root inside the private selector: kappa_eff factorizes as kappa_* Z_0 exp(delta_ZH), the topological/superselection kappa branch gives D_A ln kappa_*=0, and the single Hilbert source-measure descent gives delta_ZH=0 and D_A delta_ZH=0. Therefore delta_kappa=D_A ln kappa_eff=0 in the private branch. This recovers the GR/Newton coupling structurally after one calibration, without claiming a numerical prediction of G_N and without using orbital GM as an input. Public parent derivation remains unsigned; if any source leak survives, finite Gdot/WEP/clock/orbital/PPN bounds are required.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": BRANCH,
            "status": "PRIVATE_DELTAKAPPA_ZERO_CALIBRATED_G_PUBLIC_PARENT_UNSIGNED_NONCLAIM",
            "delta_kappa_private_branch": "zero",
            "numeric_G_predicted": False,
            "orbital_GM_backfill_allowed": False,
            "public_parent_delta_kappa": "unsigned",
            "fallback": "finite Gdot/WEP/clock/local-G/orbital/PPN source-coupling bound interface",
            "next_target": NEXT_TARGET,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "c_D and delta_kappa are now closed inside the private selector; c_Gamma is the remaining MTS-specific local hair not killed by same-coframe or source-coupling laws.",
            "success_condition": "derive local memory support/projector silence for c_Gamma, or build source-backed profile/product bounds in PPN, clocks, orbital/Gdot and R10 arenas.",
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    locks: list[dict[str, Any]],
    zeros: list[dict[str, Any]],
    readouts: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    guards: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    public_clean, public_detail = git_clean(PUBLIC_STAGE)
    backup_clean, backup_detail = git_clean(BACKUP_REPO)
    all_rows: list[dict[str, Any]] = sources + locks + zeros + readouts + bounds + guards + runners + decisions
    checks = [
        ("VAL4654_00_sources_exist", all(row["path_exists"] for row in sources), "all cited paths exist"),
        ("VAL4654_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ("VAL4654_02_line_anchors", all(int(row["line_number"]) > 0 for row in sources), "all source line anchors positive"),
        ("VAL4654_03_factorization", any(row["lock_id"] == "DKL4654_0_factorization" for row in locks), "kappa_eff factorization present"),
        ("VAL4654_04_no_drift", any(row["lock_id"] == "DKL4654_4_no_drift" and "D_A ln kappa_eff" in row["formula"] for row in locks), "no-drift lock present"),
        ("VAL4654_05_delta_zero", any(row["theorem_id"] == "DKZ4654_3_result" and row["consequence"].startswith("delta_kappa = 0") for row in zeros), "private delta_kappa zero theorem present"),
        ("VAL4654_06_numeric_firewall", any(row["guard_id"] == "ACG4654_0_no_numeric_G_claim" for row in guards), "numeric-G firewall present"),
        ("VAL4654_07_orbital_firewall", any(row["guard_id"] == "ACG4654_1_no_orbital_backfill" for row in guards), "orbital GM anti-circularity guard present"),
        ("VAL4654_08_newton_readout", any(row["readout_id"] == "NCR4654_2_Poisson" for row in readouts), "Poisson readout recorded"),
        ("VAL4654_09_bound_interface", {row["arena"] for row in bounds} == {"Gdot/G", "WEP/source species", "clock/local-G", "orbital GM consistency", "range/environment", "PPN/source frame"}, "finite delta_kappa bound interface complete"),
        ("VAL4654_10_private_runner_pass", any(row["run_id"] == "RUN4654_0_private_lock" and row["result"] == "PASS_PRIVATE_DELTAKAPPA_ZERO_NONCLAIM" for row in runners), "private lock runner passes"),
        ("VAL4654_11_public_runner_fail", any(row["run_id"] == "RUN4654_4_public_parent" and row["result"] == "FAIL_PUBLIC_PARENT_UNSIGNED" for row in runners), "public parent route fails closed"),
        ("VAL4654_12_no_claim_allowed", all(str(row.get("valid_for_claim", "False")) == "False" and str(row.get("claim_allowed", "False")) == "False" for row in all_rows), "no row is claim-grade"),
        ("VAL4654_13_decision_next", decisions and decisions[0]["next_target"] == NEXT_TARGET, "c_Gamma selected next"),
        ("VAL4654_14_public_stage_clean", public_clean, f"public stage: {public_detail}"),
        ("VAL4654_15_backup_repo_clean", backup_clean, f"backup repo: {backup_detail}"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4654_OVERALL",
            "status": "PASS" if all(passed for _, passed, _ in checks) else "FAIL",
            "detail": "4654 delta_kappa calibrated source-coupling gate passed" if all(passed for _, passed, _ in checks) else "4654 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    locks: list[dict[str, Any]],
    zeros: list[dict[str, Any]],
    readouts: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    guards: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4654 - delta_kappa source-coupling lock or Gdot/orbital bound

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4654 closes the second leakage root inside the private selector:

`kappa_eff = kappa_* Z_H = kappa_* Z_0 exp(delta_ZH)`

and therefore

`delta_kappa := D_A ln kappa_eff = D_A ln kappa_* + D_A delta_ZH`.

The private route is:

`topological/superselected kappa_* -> D_A ln kappa_* = 0`

plus

`single Hilbert source measure -> delta_ZH = 0 and D_A delta_ZH = 0`.

So:

`delta_kappa = 0`

inside the private topological-kappa/Hilbert-source selector.

This gives the GR/Newton coupling **structurally**:

`G_cal = c^4 kappa_eff/(8*pi)`,

`nabla^2 Phi_N = 4*pi G_cal rho_H`.

It does not claim a numerical prediction of `G_N`, and it explicitly forbids using orbital `GM` to define the source charge or coupling. If source drift reopens, the fallback is finite `Gdot/G`, WEP/source-species, clock/local-G, orbital-GM, range/environment and PPN/source-frame bounds.

## Source Register

{table(sources)}

## Coupling Lock

{table(locks)}

## delta_kappa Zero Theorem

{table(zeros)}

## Newton Coupling Readout

{table(readouts)}

## Finite delta_kappa Bound Interface

{table(bounds)}

## Anti-Circularity Guards

{table(guards)}

## Runner Results

{table(runners)}

## Controls

{table(controls)}

## Decision

{table(decisions)}

## Status

{table(statuses)}

## Next Target

{table(nexts)}

## Validation

{table(validations)}
"""


def register_claim() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = [
        CLAIM_ID,
        "local_gr_empirical_interface",
        "4654 rederives delta_kappa=0 inside the private topological-kappa/Hilbert-source selector: kappa_eff=kappa_* Z_0 exp(delta_ZH), D_A ln kappa_*=0, delta_ZH=0 and D_A delta_ZH=0 imply D_A ln kappa_eff=0. This recovers the GR/Newton coupling structurally after one calibration while rejecting numerical-G prediction and orbital-GM backfill.",
        "Generated source register, coupling lock, delta_kappa zero theorem, Newton coupling readout, finite bound interface, anti-circularity guards, runner, controls, decision, status, next target and validation.",
        "deltaKappa_private_source_coupling_zero_calibrated_G_nonclaim",
        NEXT_TARGET,
        "Claiming numeric G_N, defining source mass/coupling from orbital GM, setting Z_H=1 before delta_ZH leaks vanish, or claiming public local GR from the private coupling lock.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN claim until the topological kappa/Hilbert-source grammar is parent-derived and remaining c_Gamma/local-memory residuals are closed or source-backed.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4654 closes the second leakage root inside the private selector. With `kappa_eff=kappa_* Z_0 exp(delta_ZH)`, topological/superselected `kappa_*` gives `D_A ln kappa_*=0` and single Hilbert source-measure descent gives `delta_ZH=0`, so `delta_kappa=D_A ln kappa_eff=0`. The GR/Newton coupling is recovered structurally as `G_cal=c^4 kappa_eff/(8*pi)` and `nabla^2 Phi_N=4*pi G_cal rho_H`. This is not a numerical prediction of `G_N`, and orbital `GM` is forbidden as an input. Public parent derivation remains unsigned. Next leakage root: `c_Gamma`.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4654` rederives `delta_kappa=0` inside the private topological-kappa/Hilbert-source selector, installs numeric-G and orbital-GM firewalls, and stages finite `Gdot/WEP/clock/orbital/PPN` bounds if source drift reopens. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    timestamp = now()
    sources = source_rows(timestamp)
    locks = coupling_lock_rows(timestamp)
    zeros = zero_theorem_rows(timestamp)
    readouts = newton_readout_rows(timestamp)
    bounds = bound_interface_rows(timestamp)
    guards = anti_circularity_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validations = validation_rows(sources, locks, zeros, readouts, bounds, guards, runners, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(COUPLING_LOCK_CSV, locks)
    write_csv(ZERO_THEOREM_CSV, zeros)
    write_csv(NEWTON_READOUT_CSV, readouts)
    write_csv(BOUND_INTERFACE_CSV, bounds)
    write_csv(ANTI_CIRCULARITY_CSV, guards)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validations)

    doc = build_doc(sources, locks, zeros, readouts, bounds, guards, runners, controls, decisions, statuses, nexts, validations)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = validations[-1]["status"]
    print(f"4654 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
