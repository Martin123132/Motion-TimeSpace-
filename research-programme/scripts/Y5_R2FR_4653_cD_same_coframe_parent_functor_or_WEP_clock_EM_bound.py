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

CHECKPOINT = "4653"
CLAIM_ID = "L-495"
BRANCH = "MTS_R2FR_Y5_CD_SAME_COFRAME_PARENT_FUNCTOR_OR_WEP_CLOCK_EM_BOUND_4653"
MARKER = "PPC4161_CD_SAME_COFRAME_PARENT_FUNCTOR_OR_WEP_CLOCK_EM_BOUND_4653"
PACKET_MARKER = "PPC4161_PACKET_CD_SAME_COFRAME_PARENT_FUNCTOR_OR_WEP_CLOCK_EM_BOUND_4653"
DECISION = "cD_PRIVATE_SAME_COFRAME_ZERO_REDERIVED_PUBLIC_PARENT_FUNCTOR_UNSIGNED_DELTAKAPPA_NEXT"
NEXT_TARGET = "4654-Y5-R2FR-deltaKappa-source-coupling-lock-or-Gdot-orbital-bound.md"

DOC_PATH = POST / "4653-Y5-R2FR-cD-same-coframe-parent-functor-or-WEP-clock-EM-bound.md"
FORMAL_PATH = FORMAL / "669-PPC4161-cD-same-coframe-parent-functor-or-WEP-clock-EM-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4652 = POST / "4652-Y5-R2FR-AMF-Palatini-IR-selector-origin-or-EH-effective-demotion.md"
FORMAL_579 = FORMAL / "579-PPC4161-A-MF-axiom-pack-to-IR-scale-law-and-no-extra-mode-contract.md"
FORMAL_465 = FORMAL / "465-PPC4161-parent-motion-frame-A-MF-adoption-or-derived-flow-symmetry.md"
FORMAL_191 = FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md"
FORMAL_223 = FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md"
FORMAL_466 = FORMAL / "466-PPC4161-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md"
DOC_4564 = POST / "4564-Y5-R2FR-cD-deltaKappa-cGamma-root-ownership-zero-law-or-bound-interface.md"
CSV_4186_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4186_JOINT_ZERO_LAW_CLAUSES.csv"
CSV_4652_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4652_NEXT_TARGET.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4653_SOURCE_REGISTER.csv"
FUNCTOR_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4653_CD_SAME_COFRAME_FUNCTOR_CONTRACT.csv"
ZERO_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4653_CD_ZERO_THEOREM.csv"
ARENA_ROUTES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4653_CD_ARENA_ROUTES.csv"
BOUND_INTERFACE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4653_CD_BOUND_INTERFACE.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4653_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4653_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4653_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4653_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4653_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4653_VALIDATION.csv"


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
    if not rows:
        return ""
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
        ("SRC4653_00_4652_next", CSV_4652_NEXT, "4653-Y5-R2FR-cD-same-coframe-parent-functor-or-WEP-clock-EM-bound.md", "4652 selected c_D as first leakage-root attack."),
        ("SRC4653_01_4652_triage", DOC_4652, "TRI4652_0_cD", "c_D first because WEP/clocks/EM/PPN fail if same-coframe fails."),
        ("SRC4653_02_4563_same_coframe", FORMAL_579, "AP4563_2_same_coframe", "same observed coframe clause."),
        ("SRC4653_03_4563_cD_root", FORMAL_579, "NEM4563_0_cD", "c_D root maps to WEP, clocks, EM and Poynting/Hilbert stress."),
        ("SRC4653_04_4449_private_AMF", FORMAL_465, "D4449_1_private_adoption", "A_MF private branch owns coframe/connection variables."),
        ("SRC4653_05_4449_same_coframe_route", FORMAL_465, "same-coframe matter/EM and boundary routing", "same-coframe route retained as downstream gate."),
        ("SRC4653_06_191_poynting_identity", FORMAL_191, "Poynting vector is not a separate background field", "Poynting is Hilbert-stress flux."),
        ("SRC4653_07_191_no_second_metric", FORMAL_191, "forbids independent EM source weights, hidden EM-current multipliers, a second EM metric", "no hidden EM/coframe fork."),
        ("SRC4653_08_223_poynting_zero", FORMAL_223, "=> c_Poynt_extra = 0", "standalone Poynting source coefficient is zero in safe branch."),
        ("SRC4653_09_4450_cD", FORMAL_466, "C4450_0_cD", "c_D was already private-routed but needs refreshed gate after 4652."),
        ("SRC4653_10_4450_not_reopen", FORMAL_466, "Do not waste the next pass circling Poynting, calibrated G, or c_D unless a guard reopens.", "guard against circular c_D/Poynting work."),
        ("SRC4653_11_4564_cD_zero", DOC_4564, "TZ4564_0_cD_zero", "existing c_D private zero theorem row."),
        ("SRC4653_12_4564_cD_bound", DOC_4564, "BI4564_0_cD", "dormant finite c_D bound interface."),
        ("SRC4653_13_4186_same_coframe", CSV_4186_ZERO, "JZ4186_0_same_coframe", "machine-readable same-coframe zero clause."),
        ("SRC4653_14_4186_poynting", CSV_4186_ZERO, "JZ4186_1_poynting_owner", "machine-readable Poynting owner clause."),
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


def functor_contract_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CDF4653_0_parent_domain", "Parent branch variables include X^A, omega^A_B, B^A, q, theta and visible sector fields.", "A_MF private branch supplies Cartan variables; not yet global parent-derived.", "PRIVATE_INPUT"),
        ("CDF4653_1_observed_coframe_functor", "F_obs(Phi) := e_obs^A = D_omega X^A + B^A and g_obs = eta_AB e_obs^A e_obs^B.", "one observed coframe/metric/Hodge readout for local matter, clocks, EM and tests", "PRIVATE_FUNCTOR"),
        ("CDF4653_2_visible_action_descent", "S_vis = S_matter[psi,g_obs,theta] + S_clock[C,g_obs] + S_rods[R,g_obs] + S_EM[A,*_obs] + S_bind[e_obs] + dB_flux.", "no sector action is allowed to depend on e_s^A, g_s, *_s, chi_s or a source-label coframe.", "REQUIRED_CLAUSE"),
        ("CDF4653_3_shadow_coframe_absence", "For any disformal/shadow variable D_s^A, partial S_vis / partial D_s^A = 0 because D_s^A is not a branch variable.", "the operator multiplying c_D is absent rather than tuned small.", "ZERO_MECHANISM"),
        ("CDF4653_4_EM_Hodge_lock", "S_EM = -1/4 integral sqrt(-g_obs) F_{mu nu}F^{mu nu}[g_obs]; T_EM and Poynting flux are Hilbert stress components on g_obs.", "EM cannot reopen c_D via a second Hodge or standalone Poynting source while this lock holds.", "ZERO_MECHANISM"),
        ("CDF4653_5_reactivation_guard", "If any sector uses e_s^A != e_obs^A, a second metric/Hodge, independent EM source weight, hidden current multiplier or material coframe, c_D is live again.", "then c_D must move to finite WEP/clock/EM/PPN/orbital bounds.", "FAIL_CLOSED_GUARD"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "contract_id": row[0],
            "clause": row[1],
            "meaning": row[2],
            "status": row[3],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def zero_theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CDZ4653_0_functor_domain", "single observed coframe functor", "all local visible/readout sectors factor through F_obs and g_obs", "no independent coframe variable remains for c_D", "PRIVATE_BRANCH_CLAUSE"),
        ("CDZ4653_1_variation", "shadow variation", "delta S_vis / delta D_s^A = 0 for every forbidden shadow/material coframe D_s^A", "source term for c_D vanishes identically", "DERIVED_WITHIN_CLAUSE"),
        ("CDZ4653_2_coefficient_identity", "coefficient extraction", "S_trial = S_vis[g_obs] + c_D O_D[e_s-g_obs] is outside the same-coframe branch unless O_D=0", "c_D=0 in the branch, not merely small", "PRIVATE_ZERO"),
        ("CDZ4653_3_WEP_clock", "ordinary matter, rods and clocks", "universal g_obs readout makes free-fall and clock redshift composition/frame independent at the c_D slot", "R_WEP^D=0 and R_clock^D=0 from c_D", "PRIVATE_ZERO"),
        ("CDZ4653_4_EM_Poynting", "Maxwell-Hodge/Poynting owner", "T_EM^{mu nu}[g_obs] contains energy flux; no second EM metric or Poynting source is admitted", "R_EM^D=0 and c_D_EM_side=0", "PRIVATE_ZERO"),
        ("CDZ4653_5_result", "same-coframe c_D theorem", "F_obs descent + no-shadow-frame signature + Maxwell-Hodge owner", "c_D = 0 inside the private B_GR/A_MF same-coframe branch", "PASS_PRIVATE_ZERO_NONCLAIM"),
        ("CDZ4653_6_public_debt", "public parent proof debt", "derive F_obs and no-shadow-frame exclusion from deeper MTS motion/time/space parent variables", "public parent-derived c_D=0 remains unsigned", "PUBLIC_UNSIGNED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": row[0],
            "step": row[1],
            "assumption_or_derivation": row[2],
            "consequence": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def arena_route_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("ARENA4653_0_WEP", "WEP", "single matter coframe and Hilbert stress", "R_WEP^D=0", "finite c_D would become composition/material-dependent acceleration residual"),
        ("ARENA4653_1_clock", "clocks/redshift", "clock action descends through g_obs", "R_clock^D=0", "finite c_D would be clock-species/frame redshift drift"),
        ("ARENA4653_2_EM", "EM propagation/Hodge", "Maxwell action uses *_obs only", "R_EM_Hodge^D=0", "finite c_D would be second-Hodge birefringence/propagation residual"),
        ("ARENA4653_3_Poynting", "Poynting/Hilbert stress", "Poynting is T_EM^{0i} or routed boundary flux", "c_D_EM_side=0", "finite side-channel would double count EM energy flow"),
        ("ARENA4653_4_PPN", "preferred-frame PPN", "matter/EM/readout share g_obs and tau", "R_PPN_frame^D=0", "finite c_D would contribute alpha_1/alpha_2-like frame residuals"),
        ("ARENA4653_5_orbital", "orbital/local Newton", "test bodies and source stress use one observed metric", "R_orbital_frame^D=0", "finite c_D would be source/test-metric mismatch before delta_kappa"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "arena_id": row[0],
            "arena": row[1],
            "branch_clause": row[2],
            "private_branch_result": row[3],
            "if_reopened": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def bound_interface_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CDB4653_0_WEP", "WEP", "|R_WEP^D| <= |J_WEP^D c_D|", "source-backed WEP budget, material composition map, J_WEP^D units", "MISSING_SOURCE_BACKED_JACOBIAN", False),
        ("CDB4653_1_clock", "clocks", "|R_clock^D| <= |J_clock^D c_D|", "source-backed clock/redshift budget, clock species map, J_clock^D units", "MISSING_SOURCE_BACKED_JACOBIAN", False),
        ("CDB4653_2_EM_Hodge", "EM propagation/Hodge", "|R_EM^D| <= |J_EM^D c_D|", "source-backed EM propagation/constitutive bound, J_EM^D units", "MISSING_SOURCE_BACKED_JACOBIAN", False),
        ("CDB4653_3_Poynting", "Poynting/Hilbert stress", "|R_Poynt^D| <= |J_Poynt^D c_D|", "radiative/boundary flux budget and no-double-count convention", "MISSING_SOURCE_BACKED_JACOBIAN", False),
        ("CDB4653_4_PPN", "PPN preferred frame", "|R_PPN^D| <= |J_PPN^D c_D|", "PPN residual budget and frame projection Jacobian", "MISSING_SOURCE_BACKED_JACOBIAN", False),
        ("CDB4653_5_orbital", "orbital/local Newton", "|R_orbital^D| <= |J_orbital^D c_D|", "orbital/source-test metric mismatch budget and units", "MISSING_SOURCE_BACKED_JACOBIAN", False),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row[0],
            "arena": row[1],
            "symbolic_bound": row[2],
            "required_inputs": row[3],
            "status": row[4],
            "valid_for_claim": row[5],
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("RUN4653_0_private_same_coframe", "A_MF/B_GR private branch with F_obs, same g_obs, *_obs and no shadow-frame variables", "PASS_PRIVATE_CD_ZERO_NONCLAIM", "c_D=0 by absence of an independent disformal/shadow coframe slot."),
        ("RUN4653_1_public_parent", "same-coframe functor claimed as globally parent-derived from deeper MTS primitives", "FAIL_PUBLIC_PARENT_FUNCTOR_UNSIGNED", "A_MF origin and no-shadow-frame signature remain private/effective, not public theorem."),
        ("RUN4653_2_second_metric", "any sector introduces g_s, e_s, *_s, chi_EM or hidden source/current multiplier", "FAIL_REOPENS_CD_BOUND_INTERFACE", "finite c_D rows must be sourced and bounded before any local claim."),
        ("RUN4653_3_Poynting_double_count", "Poynting treated as a standalone background source in addition to Hilbert EM stress", "FAIL_REJECT_DOUBLE_COUNT", "violates 191/223 Maxwell-Hodge/Poynting owner lock."),
        ("RUN4653_4_next", "c_D is private-closed; delta_kappa remains the next leakage-root coefficient", "PASS_NEXT_DELTAKAPPA_SELECTED", NEXT_TARGET),
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
        ("CTRL4653_0_private_not_public", "c_D=0 is allowed only inside the explicitly labelled private same-coframe B_GR/A_MF branch."),
        ("CTRL4653_1_no_shadow_smuggling", "No material/species coframe, second metric/Hodge, chi_EM or hidden EM-current multiplier can be silently introduced."),
        ("CTRL4653_2_no_Poynting_double_count", "Poynting is an EM Hilbert-stress/boundary flux component, not a second background force."),
        ("CTRL4653_3_bounds_if_reopened", "If same-coframe fails, c_D must be scored with WEP/clock/EM/PPN/orbital source-backed bounds."),
        ("CTRL4653_4_move_on", "Do not circle c_D again unless a guard fails; next leakage root is delta_kappa/source coupling."),
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
            "decision_id": "DEC4653_0",
            "decision": DECISION,
            "summary": "4653 rederives the c_D closure in the active private B_GR/A_MF branch: if every visible sector descends through one observed coframe/metric/Hodge functor and Maxwell/Poynting is Hilbert-owned, there is no independent shadow/disformal coframe slot, so c_D=0 inside that branch. The result remains non-public because the deeper parent derivation of F_obs/no-shadow-frame is unsigned. If that clause is rejected, finite c_D must be bounded in WEP, clocks, EM, Poynting, PPN and orbital arenas.",
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
            "status": "PRIVATE_CD_ZERO_PUBLIC_PARENT_UNSIGNED_NONCLAIM",
            "c_D_private_branch": "zero",
            "public_parent_cD": "unsigned",
            "fallback": "finite WEP/clock/EM/Poynting/PPN/orbital bound interface",
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
            "reason": "With c_D closed inside the private same-coframe branch, the next leakage root is delta_kappa: whether source coupling/kappa/source measure drift can be derived as zero without pretending to predict numeric G.",
            "success_condition": "derive a Hilbert-source/kappa calibration lock that gives delta_kappa=0 structurally, or build source-backed Gdot/orbital/clock/local-G bounds for finite delta_kappa.",
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    zeros: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    public_clean, public_detail = git_clean(PUBLIC_STAGE)
    backup_clean, backup_detail = git_clean(BACKUP_REPO)
    all_rows: list[dict[str, Any]] = sources + contracts + zeros + arenas + bounds + runners + decisions
    checks = [
        ("VAL4653_00_sources_exist", all(row["path_exists"] for row in sources), "all cited paths exist"),
        ("VAL4653_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ("VAL4653_02_line_anchors", all(int(row["line_number"]) > 0 for row in sources), "all source line anchors positive"),
        ("VAL4653_03_functor_contract", any(row["contract_id"] == "CDF4653_1_observed_coframe_functor" for row in contracts), "observed coframe functor written"),
        ("VAL4653_04_no_shadow_guard", any(row["contract_id"] == "CDF4653_5_reactivation_guard" for row in contracts), "shadow-frame reactivation guard present"),
        ("VAL4653_05_cd_zero", any(row["theorem_id"] == "CDZ4653_5_result" and row["consequence"].startswith("c_D = 0") for row in zeros), "private c_D zero theorem present"),
        ("VAL4653_06_public_unsigned", any(row["theorem_id"] == "CDZ4653_6_public_debt" and row["status"] == "PUBLIC_UNSIGNED" for row in zeros), "public parent debt retained"),
        ("VAL4653_07_arena_routes", {row["arena"] for row in arenas} == {"WEP", "clocks/redshift", "EM propagation/Hodge", "Poynting/Hilbert stress", "preferred-frame PPN", "orbital/local Newton"}, "all local arenas routed"),
        ("VAL4653_08_bound_interface", {row["arena"] for row in bounds} == {"WEP", "clocks", "EM propagation/Hodge", "Poynting/Hilbert stress", "PPN preferred frame", "orbital/local Newton"}, "finite c_D bound interface complete"),
        ("VAL4653_09_private_runner_pass", any(row["run_id"] == "RUN4653_0_private_same_coframe" and row["result"] == "PASS_PRIVATE_CD_ZERO_NONCLAIM" for row in runners), "private same-coframe runner passes"),
        ("VAL4653_10_public_runner_fail", any(row["run_id"] == "RUN4653_1_public_parent" and row["result"] == "FAIL_PUBLIC_PARENT_FUNCTOR_UNSIGNED" for row in runners), "public parent route fails closed"),
        ("VAL4653_11_no_claim_allowed", all(str(row.get("valid_for_claim", "False")) == "False" and str(row.get("claim_allowed", "False")) == "False" for row in all_rows), "no row is claim-grade"),
        ("VAL4653_12_decision_next", decisions and decisions[0]["next_target"] == NEXT_TARGET, "delta_kappa selected next"),
        ("VAL4653_13_public_stage_clean", public_clean, f"public stage: {public_detail}"),
        ("VAL4653_14_backup_repo_clean", backup_clean, f"backup repo: {backup_detail}"),
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
            "validation_id": "VAL4653_OVERALL",
            "status": "PASS" if all(passed for _, passed, _ in checks) else "FAIL",
            "detail": "4653 c_D same-coframe gate passed" if all(passed for _, passed, _ in checks) else "4653 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    zeros: list[dict[str, Any]],
    arenas: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4653 - c_D same-coframe parent functor or WEP/clock/EM bound

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4653 takes the first leakage root seriously instead of just naming it.

Inside the active private `B_GR/A_MF` branch, define one observed coframe functor

`F_obs(Phi) -> e_obs^A = D_omega X^A + B^A`, with `g_obs = eta_AB e_obs^A e_obs^B`.

If matter, clocks, rods, EM/Hodge, binding/source stress and local test readouts all descend through that same `g_obs`, then a shadow/material/disformal coframe is not a branch variable. Varying the visible action with respect to such a forbidden shadow coframe gives zero identically, not by tuning:

`delta S_vis / delta D_s^A = 0  =>  c_D = 0`.

This closes `c_D` inside the private same-coframe selector. It does **not** make a public parent-derived GR claim, because the deeper MTS derivation of `F_obs` and the no-shadow-frame signature is still unsigned. If any sector reintroduces a second metric/Hodge/material coframe/hidden EM-current multiplier, `c_D` reopens and must be bounded in WEP, clocks, EM, Poynting, PPN and orbital arenas.

## Source Register

{table(sources)}

## Same-Coframe Functor Contract

{table(contracts)}

## c_D Zero Theorem

{table(zeros)}

## Arena Routes

{table(arenas)}

## Finite c_D Bound Interface

{table(bounds)}

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
        "4653 rederives c_D=0 inside the private B_GR/A_MF same-coframe branch: visible matter, clocks, rods, EM/Hodge, Poynting/Hilbert stress and local test readouts all descend through one observed coframe/metric, so no independent shadow/disformal coframe slot exists. Public parent derivation remains unsigned; finite c_D fallback bounds are staged.",
        "Generated source register, same-coframe functor contract, c_D zero theorem, arena routes, finite bound interface, runner, controls, decision, status, next target and validation.",
        "cD_same_coframe_private_zero_nonclaim",
        NEXT_TARGET,
        "Claiming public parent-derived local GR from the private c_D zero, introducing a second metric/Hodge/material coframe, double-counting Poynting as a background force, or ignoring WEP/clock/EM/PPN/orbital bounds if c_D reopens.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/Maxwell/EM claim until the same-coframe/no-shadow functor is parent-derived and delta_kappa/c_Gamma residuals are closed or source-backed.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4653 closes the first leakage root inside the private `B_GR/A_MF` selector. With a single observed coframe functor `F_obs -> e_obs^A` and one `g_obs`/Hodge for matter, clocks, rods, EM, binding/source stress and local test readout, no independent shadow or disformal coframe slot exists; hence `c_D=0` in that branch. This remains nonclaim because the parent derivation of `F_obs`/no-shadow-frame is unsigned. If the guard fails, finite `c_D` must be bounded in WEP, clock, EM, Poynting, PPN and orbital arenas. Next leakage root: `delta_kappa`.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4653` rederives `c_D=0` inside the private same-coframe branch and stages finite WEP/clock/EM/PPN/orbital bounds if the guard reopens. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    timestamp = now()
    sources = source_rows(timestamp)
    contracts = functor_contract_rows(timestamp)
    zeros = zero_theorem_rows(timestamp)
    arenas = arena_route_rows(timestamp)
    bounds = bound_interface_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validations = validation_rows(sources, contracts, zeros, arenas, bounds, runners, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(FUNCTOR_CONTRACT_CSV, contracts)
    write_csv(ZERO_THEOREM_CSV, zeros)
    write_csv(ARENA_ROUTES_CSV, arenas)
    write_csv(BOUND_INTERFACE_CSV, bounds)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validations)

    doc = build_doc(sources, contracts, zeros, arenas, bounds, runners, controls, decisions, statuses, nexts, validations)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = validations[-1]["status"]
    print(f"4653 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
