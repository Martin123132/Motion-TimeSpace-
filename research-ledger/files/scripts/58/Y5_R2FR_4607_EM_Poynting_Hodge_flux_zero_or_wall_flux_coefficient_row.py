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

CHECKPOINT = "4607"
CLAIM_ID = "L-449"
BRANCH_ID = "MTS_R2FR_Y5_EM_POYNTING_HODGE_FLUX_GATE_4607"
MARKER = "PPC4161_EM_POYNTING_HODGE_FLUX_ZERO_OR_WALL_FLUX_COEFFICIENT_ROW_4607"
PACKET_MARKER = "PPC4161_PACKET_EM_POYNTING_HODGE_FLUX_GATE_4607"
DECISION = "EM_POYNTING_SAME_HODGE_NO_FLUX_OR_WALL_COEFFICIENT_SCHEMA_READY_NONCLAIM"
NEXT_TARGET = "4608-Y5-R2FR-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md"

DOC_PATH = POST / "4607-Y5-R2FR-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md"
FORMAL_PATH = FORMAL / "623-PPC4161-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4607_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4607_EM_POYNTING_HODGE_FLUX_THEOREM.csv"
HODGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4607_HODGE_OWNER_ROWS.csv"
FLUX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4607_POYNTING_FLUX_ROWS.csv"
EM_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4607_EM_BULK_BOUND_UPDATE_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4607_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4607_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4607_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4607_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4607_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4607_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4607_VALIDATION.csv"

DOC_4606 = POST / "4606-Y5-R2FR-Qbulk-Hilbert-EM-Poynting-source-current-zero-or-first-coefficient-row.md"
FORMAL_622 = FORMAL / "622-PPC4161-Qbulk-Hilbert-EM-Poynting-source-current-zero-or-first-coefficient-row.md"
CSV_4606_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4606_NEXT_TARGET.csv"
CSV_4606_EM = SOURCE_DIR / "P8_Y5_R2FR_4606_QBULK_EM_POYNTING_ROWS.csv"
CSV_4606_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4606_QBULK_SOURCE_CURRENT_THEOREM.csv"
CSV_4587_POYNTING = SOURCE_DIR / "P8_Y5_R2FR_4587_POYNTING_OWNER_LOCK.csv"
CSV_4587_RESIDUAL = SOURCE_DIR / "P8_Y5_R2FR_4587_DENSITY_POYNTING_RESIDUAL_VECTOR.csv"
CSV_4013_ONCE = SOURCE_DIR / "P8_Y5_R2FR_4013_MAXWELL_POYNTING_ONCE_ONLY_THEOREM.csv"
CSV_4014_HODGE = SOURCE_DIR / "P8_Y5_R2FR_4014_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv"
CSV_4014_FINITE = SOURCE_DIR / "P8_Y5_R2FR_4014_HODGE_F2_CURRENT_FINITE_ROWS.csv"
CSV_4038_NOFLUX = SOURCE_DIR / "P8_Y5_R2FR_4038_POYNTING_NO_FLUX_THEOREM.csv"
CSV_4315_HODGE = SOURCE_DIR / "P8_Y5_R2FR_4315_SAME_HODGE_THEOREM.csv"
CSV_4315_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4315_DELTA_HODGE_BOUND_UPDATE.csv"
CSV_3946_FLUX = SOURCE_DIR / "P8_Y5_R2FR_3946_POYNTING_AND_WALL_FLUX_BOUND_LAW.csv"
CSV_3994_FLUX = SOURCE_DIR / "P8_Y5_R2FR_3994_POYNTING_FLUX_ZERO_OR_BOUND_ROWS.csv"
CSV_4520_FLOW = SOURCE_DIR / "P8_Y5_R2FR_4520_POYNTING_HILBERT_FLOW_GATE.csv"
CSV_4516_GUARD = SOURCE_DIR / "P8_Y5_R2FR_4516_EM_POYNTING_STATIONARY_WORLDTUBE_GUARD.csv"

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


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for number, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return number
    return 0


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
        lines.append("| " + " | ".join(str(row.get(key, "")).replace("\n", " ").replace("|", "\\|") for key in headers) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    write_text(path, text.rstrip() + "\n\n" + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--short"], capture_output=True, text=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def append_claim_once() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = list(rows[0].keys()) if rows else [
        "claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk", "sector", "evidence", "next_action", "risk"
    ]
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4607 isolates the Maxwell/Poynting fork: same observed Hodge and once-only Maxwell stress make Poynting part of the Hilbert source, while nonstationary wall flux, Hodge mismatch, extra Poynting source, or nonminimal EM coupling are retained as explicit nonclaim coefficients.",
        "current_evidence": "Generated EM/Poynting Hodge/flux theorem rows, Hodge owner rows, Poynting wall-flux rows, EM bulk bound update rows, controls, blockers and validation.",
        "status": "EM_Poynting_Hodge_flux_zero_or_wall_coefficient_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Treating gauge covariance or a Poynting slogan as a same-Hodge/no-flux theorem; or erasing radiative/open-system wall flux from the source-current numerator.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No R10, PPN, clock, orbital or local-GR claim until EM/Poynting, retained, edge/shadow, denominator/projector, qbar_XT and arena kernels are zero or source-backed.",
    }
    rows.append({key: row.get(key, "") for key in fieldnames})
    write_csv(CLAIMS_PATH, rows)


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4607_00_4606_doc", DOC_4606, "4607-Y5-R2FR-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md", "4606 selected 4607."),
        ("SRC4607_01_622_formal", FORMAL_622, "|Q_bulk_EM/Poynting|", "formal EM bulk bound."),
        ("SRC4607_02_4606_next", CSV_4606_NEXT, "4607-Y5-R2FR-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md", "machine next target."),
        ("SRC4607_03_4606_em_rows", CSV_4606_EM, "EM4606_2_wall_flux", "wall-flux row handoff."),
        ("SRC4607_04_4606_theorem", CSV_4606_THEOREM, "QBH4606_3_EM_Poynting_zero_or_flux", "EM zero/flux theorem handoff."),
        ("SRC4607_05_4587_public", CSV_4587_POYNTING, "POY4587_0_public_Maxwell_Hodge", "public Maxwell-Hodge row."),
        ("SRC4607_06_4587_once", CSV_4587_POYNTING, "POY4587_1_once_only", "once-only Poynting row."),
        ("SRC4607_07_4587_flux", CSV_4587_POYNTING, "POY4587_2_flux_boundary", "flux boundary row."),
        ("SRC4607_08_4587_Hodge", CSV_4587_RESIDUAL, "DRV4587_3_E_Hodge_EM", "Hodge residual component."),
        ("SRC4607_09_4587_Poynting", CSV_4587_RESIDUAL, "DRV4587_4_E_Poynting_boundary", "Poynting residual component."),
        ("SRC4607_10_4587_nonminimal", CSV_4587_RESIDUAL, "DRV4587_5_E_nonminimal_EM", "nonminimal EM component."),
        ("SRC4607_11_4013_once", CSV_4013_ONCE, "MPE4013_4_once_only_rule", "Maxwell once-only theorem."),
        ("SRC4607_12_4013_flux", CSV_4013_ONCE, "MPE4013_3_Poynting_flux_placement", "Poynting flux placement."),
        ("SRC4607_13_4014_Hodge", CSV_4014_HODGE, "OHN4014_0_observed_Hodge_lock", "observed Hodge owner theorem."),
        ("SRC4607_14_4014_guard", CSV_4014_HODGE, "OHN4014_5_conformal_scale_guard", "Hodge/conformal overclaim guard."),
        ("SRC4607_15_4014_finite", CSV_4014_FINITE, "EMOWN4014_1_Delta_Hodge_EM", "finite Hodge owner vector."),
        ("SRC4607_16_4038_no_flux", CSV_4038_NOFLUX, "PNT4038_1_exterior_collar", "stationary exterior no-flux theorem."),
        ("SRC4607_17_4038_guard", CSV_4038_NOFLUX, "PNT4038_3_no_global_zero_guard", "local not global no-flux guard."),
        ("SRC4607_18_4315_same", CSV_4315_HODGE, "HT4315_1_same_action", "same-Hodge Maxwell action."),
        ("SRC4607_19_4315_counter", CSV_4315_HODGE, "HT4315_4_countermodel", "constitutive countermodel."),
        ("SRC4607_20_4315_bound", CSV_4315_BOUND, "HB4315_0_envelope", "Delta_Hodge bound envelope."),
        ("SRC4607_21_3994_zero", CSV_3994_FLUX, "PY3994_0_stationary_zero", "stationary Poynting zero row."),
        ("SRC4607_22_3994_bound", CSV_3994_FLUX, "PY3994_2_flux_bound", "finite Poynting flux bound row."),
        ("SRC4607_23_3946_wall", CSV_3946_FLUX, "FLX3946_1_Poynting", "wall Poynting flux coefficient."),
        ("SRC4607_24_4520_flow", CSV_4520_FLOW, "Poynting", "Poynting Hilbert flow gate."),
        ("SRC4607_25_4516_guard", CSV_4516_GUARD, "Poynting", "stationary worldtube guard."),
        ("SRC4607_26_claim_448", CLAIMS_PATH, "L-448", "claim-register handoff from 4606."),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": bool(line),
                "line_number": line,
                "role": role,
                "generated_utc": now,
                "valid_for_claim": False,
            }
        )
    return rows


def theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "EMF4607_0_once_only",
            "statement": "On the public observed-Hodge Maxwell branch, Poynting is a component of Hilbert EM stress and is counted once.",
            "formula": "S_EM=-(4 mu0)^-1 int F wedge *_obs F; T_EM=delta S_EM/delta g_obs; S_Poynting^i=-T_EM^i_nu tau^nu",
            "consequence": "c_Poynt_extra=0 in the single source functional branch.",
            "status": "ONCE_ONLY_THEOREM_DERIVED_CONDITIONAL",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "EMF4607_1_same_Hodge",
            "statement": "Same-Hodge ownership zeros Delta_Hodge_EM only when the Maxwell action uses *_obs[e_obs(q)] with no independent constitutive tensor/readout Hodge.",
            "formula": "S_Maxwell=-(4 mu0)^-1 int F wedge *_obs[e_obs(q)] F => Delta_Hodge_EM=0",
            "consequence": "Gauge invariance alone is insufficient; constitutive countermodels remain unless object language excludes them.",
            "status": "SAME_HODGE_ZERO_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "EMF4607_2_no_wall_flux",
            "statement": "The direct Poynting wall coefficient is zero only in a stationary isolated local collar with no incoming/background radiation and no current crossing the collar.",
            "formula": "Phi_wall_Poynting=int_boundary T_EM(tau,n) dSigma dt=0",
            "consequence": "Open/radiative/nonstationary systems retain a finite wall-flux coefficient.",
            "status": "LOCAL_NO_FLUX_THEOREM_CONDITIONAL_NOT_GLOBAL",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "EMF4607_3_finite_EM_bound",
            "statement": "If same-Hodge or no-flux is unsigned, EM/Poynting feeds Q_bulk through a no-cancellation envelope.",
            "formula": "|Q_bulk_EM/Poynting| <= W_lambda_max(M_ref|Delta_Hodge_EM| + |c_Poynt_extra Phi_wall| + |Phi_wall_Poynting| + M_ref|epsilon_nonminimal_EM|)",
            "consequence": "The Poynting branch is either theorem-silent or sourceable; it is not a closure axiom.",
            "status": "BOUND_FORMULA_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def hodge_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "HG4607_0_same_Hodge_zero",
            "quantity": "Delta_Hodge_EM_zero",
            "zero_condition": "fixed e_obs, g_obs, orientation and S_EM=-(4mu0)^-1 int F wedge *_obs F with no independent chi_EM",
            "bound_formula": "Delta_Hodge_EM=0",
            "current_status": "CONDITIONAL_ZERO_NOT_GLOBAL",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "HG4607_1_Hodge_envelope",
            "quantity": "Delta_Hodge_EM_abs",
            "zero_condition": "all constitutive residuals zero in the same parent-visible branch",
            "bound_formula": "||Delta_Hodge_EM|| <= ||Delta_chi_principal|| + ||Delta_chi_skewon|| + L||dtheta_EM|| + |C_Hodge_hidden| + |C_Hodge_readout| + |Delta_orientation_flux|",
            "current_status": "BOUND_DERIVED_VALUES_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "HG4607_2_conformal_guard",
            "quantity": "Delta_conformal_scale_guard",
            "zero_condition": "clock/source/impedance/alpha normalization also fixed, not merely EM cone/Hodge on two-forms",
            "bound_formula": "retain scale/source normalization rows if only conformal cone agreement is proved",
            "current_status": "ANTI_OVERCLAIM_GUARD_ACTIVE",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def flux_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "FX4607_0_stationary_zero",
            "quantity": "Phi_wall_Poynting_zero",
            "zero_condition": "stationary isolated source collar, time_avg(dU_EM/dt)=0, time_avg(int J.E dV)=0, no external radiation/current crossing wall",
            "bound_formula": "Phi_wall_Poynting=0",
            "current_status": "CONDITIONAL_LOCAL_ZERO_NOT_GLOBAL",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "FX4607_1_wall_flux_bound",
            "quantity": "Phi_wall_Poynting_abs",
            "zero_condition": "not zeroed on open/radiative/nonstationary source collars",
            "bound_formula": "|Phi_wall_Poynting| <= |dU_EM/dt| + |int_W J.E dV| + |Phi_incoming| + |Phi_apparatus|",
            "current_status": "FINITE_FLUX_BOUND_TEMPLATE_VALUE_MISSING",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "FX4607_2_closed_domain_wall",
            "quantity": "epsilon_Poynting_flux",
            "zero_condition": "closed stationary wall or finite measured/modelled wall-flux bound",
            "bound_formula": "epsilon_Poynting_flux=|int_wall S_EM dot dA dt|/E_pos",
            "current_status": "MISSING_POYNTING_FLUX_BOUND",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def em_bound_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EB4607_0_zero_route",
            "quantity": "Q_bulk_EM/Poynting",
            "formula": "Delta_Hodge_EM=0, c_Poynt_extra=0, Phi_wall_Poynting=0, epsilon_nonminimal_EM=0 => Q_bulk_EM/Poynting=0",
            "current_status": "CONDITIONAL_ZERO_ROUTE_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "EB4607_1_bound_route",
            "quantity": "Q_bulk_EM_Poynting_abs",
            "formula": "|Q_bulk_EM/Poynting| <= W_lambda_max(M_ref|Delta_Hodge_EM| + |c_Poynt_extra Phi_wall| + |Phi_wall_Poynting| + M_ref|epsilon_nonminimal_EM|)",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4607_0_once_only", "control": "Do not add Poynting as an extra source after Maxwell stress has already been varied into T_EM.", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4607_1_same_Hodge_not_gauge", "control": "Gauge covariance alone does not prove same-Hodge; independent chi_EM or readout Hodge remains a coefficient.", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4607_2_local_not_global", "control": "Stationary no-flux is a local collar theorem, not a cosmology/global EM erasure.", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4607_3_no_claim_from_schema", "control": "Hodge/flux coefficient schemas do not imply local-GR, R10, PPN, clock or orbital success.", "status": "ACTIVE", "valid_for_claim": False, "generated_utc": now},
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "blocker_id": "MIS4607_0_Hodge", "missing_object": "parent-signed same-Hodge/visible Maxwell action branch or numeric Delta_Hodge_EM envelope", "why_it_matters": "without it EM constitutive mismatch can source Q_bulk", "best_next_action": "prove same-Hodge zero or fill Delta_Hodge components", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "MIS4607_1_wall_flux", "missing_object": "stationary no-wall-flux proof or Phi_wall_Poynting bound", "why_it_matters": "open EM flux is the live Poynting source-current channel", "best_next_action": "fill wall flux coefficient or prove local stationary collar", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "MIS4607_2_nonminimal", "missing_object": "no-extra-F2/nonminimal EM source coupling zero or bound", "why_it_matters": "nonminimal EM couplings survive even if ordinary Poynting is once-only", "best_next_action": "route through retained/source current rows", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "MIS4607_3_downstream", "missing_object": "retained bulk, edge, shadow, denominator/projector, qbar_XT and arena kernels", "why_it_matters": "EM/Poynting closure alone is not a local-GR claim", "best_next_action": NEXT_TARGET, "valid_for_claim": False, "generated_utc": now},
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4607_0_Hodge", "promotion_requirement": "same-Hodge branch signed or Delta_Hodge_EM components source-backed", "current_status": "FAIL_HODGE_VALUES_MISSING", "source_count": len(sources), "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4607_1_flux", "promotion_requirement": "Phi_wall_Poynting zero or finite wall-flux coefficient sourced", "current_status": "FAIL_WALL_FLUX_VALUE_MISSING", "source_count": len(sources), "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4607_2_EM_total", "promotion_requirement": "all EM/Poynting coefficients zero or bounded in same branch", "current_status": "FAIL_EM_TOTAL_VALUES_MISSING", "source_count": len(sources), "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4607_3_empirical", "promotion_requirement": "EM row joins all other source/test/arena gates for empirical claim", "current_status": "FAIL_DOWNSTREAM_INPUTS_MISSING", "source_count": len(sources), "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [{"checkpoint": CHECKPOINT, "branch": BRANCH_ID, "decision": DECISION, "reason": "The Maxwell/Poynting fork is now exact: same-Hodge plus local no-wall-flux gives silence; otherwise Hodge and wall-flux coefficients remain explicit.", "claim": "no R10/PPN/local-GR pass", "next_target": NEXT_TARGET, "generated_utc": now, "valid_for_claim": False}]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [{"checkpoint": CHECKPOINT, "branch": BRANCH_ID, "status": DECISION, "what_moved": "Poynting is now a testable local collar coefficient when no-flux is not signed, while same-Hodge prevents double counting.", "what_did_not_move": "No numeric EM wall flux, R10 alpha, PPN residual or local-GR pass is claimed.", "generated_utc": now, "valid_for_claim": False}]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [{"checkpoint": CHECKPOINT, "branch": BRANCH_ID, "generated_utc": now, "next_target": NEXT_TARGET, "reason": "After EM/Poynting is isolated, the next live bulk numerator is retained source current: J_direct, J_mem, marker/readout tails.", "derive_first": "prove retained/direct/memory/readout source-current silence in the same parent branch", "fallback": "fill Jdirect_abs, Jmem_abs, Jmarker_abs and Jreadout_abs as nonclaim source rows", "valid_for_claim": False}]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4607 - Y5 R2FR EM/Poynting Hodge Flux Zero Or Wall-Flux Coefficient Row

Generated: `{now}`

Marker: `{MARKER}`
Branch: `{BRANCH_ID}`
Claim register row: `{CLAIM_ID}`
Previous target: `{DOC_4606}`

## Result

4607 makes the Maxwell/Poynting fork explicit:

```text
S_EM=-(4 mu0)^-1 int F wedge *_obs F
T_EM = delta S_EM/delta g_obs
S_Poynting^i = -T_EM^i_nu tau^nu
```

So, on the public observed-Hodge branch, Poynting is already inside the Hilbert EM stress. It is not added twice.

The exact local zero route is:

```text
Delta_Hodge_EM = 0
c_Poynt_extra = 0
Phi_wall_Poynting = 0
epsilon_nonminimal_EM = 0
    => Q_bulk_EM/Poynting = 0.
```

If the stationary/no-flux collar is not signed, the wall-flux row is live:

```text
Phi_wall_Poynting = int_boundary T_EM(tau,n_boundary) dSigma dt,
|Phi_wall_Poynting| <= |dU_EM/dt| + |int_W J.E dV| + |Phi_incoming| + |Phi_apparatus|.
```

The nonclaim bound remains:

```text
|Q_bulk_EM/Poynting| <= W_lambda_max(
    M_ref|Delta_Hodge_EM|
    + |c_Poynt_extra Phi_wall|
    + |Phi_wall_Poynting|
    + M_ref|epsilon_nonminimal_EM|
).
```

## Private Decision

`{DECISION}`

No R10, PPN, clock, orbital, EM, Newton or local-GR pass is claimed. The immediate best target is `{NEXT_TARGET}`.

## Source Register

{markdown_table(tables["sources"])}

## EM/Poynting Hodge-Flux Theorem

{markdown_table(tables["theorem"])}

## Hodge Owner Rows

{markdown_table(tables["hodge"])}

## Poynting Flux Rows

{markdown_table(tables["flux"])}

## EM Bulk Bound Update Rows

{markdown_table(tables["em_bound"])}

## Claim Blockers

{markdown_table(tables["blockers"])}

## Controls

{markdown_table(tables["controls"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Decision

{markdown_table(tables["decision"])}

## Status

{markdown_table(tables["status"])}

## Next Target

{markdown_table(tables["next"])}
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 623 - EM/Poynting Hodge Flux Zero Or Wall-Flux Coefficient Row

Generated: `{now}`

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`
Claim register: `{CLAIM_ID}`

## Formal Statement

On the public observed-Hodge branch:

```text
S_EM=-(4 mu0)^-1 int F wedge *_obs F,
T_EM=delta S_EM/delta g_obs,
S_Poynting^i=-T_EM^i_nu tau^nu.
```

Thus Poynting is counted once inside Hilbert EM stress.

The zero route is:

```text
Delta_Hodge_EM=c_Poynt_extra=Phi_wall_Poynting=epsilon_nonminimal_EM=0
=> Q_bulk_EM/Poynting=0.
```

The bound route is:

```text
|Q_bulk_EM/Poynting| <= W_lambda_max(M_ref|Delta_Hodge_EM|+|c_Poynt_extra Phi_wall|+|Phi_wall_Poynting|+M_ref|epsilon_nonminimal_EM|).
```

Private nonclaim. The next target is `{NEXT_TARGET}`.
"""


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False})

    add("VAL4607_00_sources_exist", all(row["path_exists"] for row in tables["sources"]), "all cited source paths exist")
    missing_needles = [row["source_id"] for row in tables["sources"] if not row["needle_found"]]
    add("VAL4607_01_needles_found", not missing_needles, "missing needles: " + ",".join(missing_needles) if missing_needles else "all cited source needles found")
    csv_paths = [SOURCE_REGISTER, THEOREM_CSV, HODGE_CSV, FLUX_CSV, EM_BOUND_CSV, CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    details = []
    csv_ok = True
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4607_02_csv_parse", csv_ok, ";".join(details))
    theorem_text = "\n".join(str(row) for row in tables["theorem"])
    hodge_text = "\n".join(str(row) for row in tables["hodge"])
    flux_text = "\n".join(str(row) for row in tables["flux"])
    bound_text = "\n".join(str(row) for row in tables["em_bound"])
    add("VAL4607_03_once_only", "c_Poynt_extra=0" in theorem_text and "T_EM" in theorem_text, "once-only theorem present")
    add("VAL4607_04_hodge_rows", "Delta_Hodge_EM" in hodge_text and "ANTI_OVERCLAIM_GUARD_ACTIVE" in hodge_text, "Hodge rows present")
    add("VAL4607_05_flux_rows", "Phi_wall_Poynting" in flux_text and "FINITE_FLUX_BOUND_TEMPLATE_VALUE_MISSING" in flux_text, "flux rows present")
    add("VAL4607_06_bound_update", "Q_bulk_EM/Poynting" in bound_text and "epsilon_nonminimal_EM" in bound_text, "EM bound update present")
    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "empirical_pass_claimed", "score_ready", "numeric_value_present"} and value is True:
                    all_false = False
    add("VAL4607_07_no_claim_true", all_false, "no generated table promotes a claim")
    add("VAL4607_08_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4607_09_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4607_10_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4607_11_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4607_12_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4607_13_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4607_14_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4607_15_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4607_OVERALL", all(row["status"] == "PASS" for row in rows), "4607 EM/Poynting Hodge-flux gate")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "theorem": theorem_rows(now),
        "hodge": hodge_rows(now),
        "flux": flux_rows(now),
        "em_bound": em_bound_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(THEOREM_CSV, tables["theorem"])
    write_csv(HODGE_CSV, tables["hodge"])
    write_csv(FLUX_CSV, tables["flux"])
    write_csv(EM_BOUND_CSV, tables["em_bound"])
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
## PPC4161 Local Addendum - EM/Poynting Hodge-Flux Gate

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The Maxwell/Poynting branch is now split into same-Hodge ownership, once-only Hilbert stress, local no-wall-flux, and finite wall-flux/nonminimal coefficients. Poynting is either inside `T_EM` or a declared boundary/source residual; it is not a hidden extra source.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - EM/Poynting Hodge-Flux Gate

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private packet now treats `Phi_wall_Poynting` as the live coefficient when stationary same-Hodge no-flux is not signed. The next bulk route is retained/direct source current.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4607 validation failed: {failed}")
    print(f"4607 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
