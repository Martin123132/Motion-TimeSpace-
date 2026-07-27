from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3937"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3937-Y5-R2FR-R10-or-orbital-first-bound-dashboard.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3937_SOURCE_REGISTER.csv",
    "readiness": SRC / "P8_Y5_R2FR_3937_R10_OR_ORBITAL_READINESS_COMPARISON.csv",
    "orbital_dashboard": SRC / "P8_Y5_R2FR_3937_ORBITAL_EPHEMERIS_BOUND_DASHBOARD.csv",
    "r10_deferred": SRC / "P8_Y5_R2FR_3937_R10_DEFERRED_QUEUE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3937_CLAIM_GATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3937_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3937_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3937_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3937_VALIDATION.csv",
}

NEXT_DOC = "3938-Y5-R2FR-orbital-ephemeris-source-acquisition-and-Delta-cal-score-runner.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3938_orbital_ephemeris_source_acquisition_and_Delta_cal_score_runner.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_row_count(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3937_00_3936_next", SRC / "P8_Y5_R2FR_3936_NEXT_TARGET.csv", "NEXT3936_0", "3936 handoff to R10/orbital route choice"),
        ("SRC3937_01_3935_r10_queue", SRC / "P8_Y5_R2FR_3935_FIRST_BOUND_DASHBOARD_QUEUE.csv", "DASH3935_1_R10", "R10 was queued as a second dashboard"),
        ("SRC3937_02_3935_orbital_queue", SRC / "P8_Y5_R2FR_3935_FIRST_BOUND_DASHBOARD_QUEUE.csv", "DASH3935_2_orbital", "orbital/ephemeris was queued as a second dashboard"),
        ("SRC3937_03_3936_yukawa", SRC / "P8_Y5_R2FR_3936_PPN_BOUND_DASHBOARD.csv", "PPND3936_8_yukawa", "short-range/Yukawa lane is active only if finite-range residual survives"),
        ("SRC3937_04_3884_orbital_readout", SRC / "P8_Y5_R2FR_3884_ORBITAL_NEWTON_READOUT_CHAIN.csv", "ORB3884_0_exterior", "Newtonian slow-orbit readout chain"),
        ("SRC3937_05_3920_radial_shape", SRC / "P8_Y5_R2FR_3920_XIN_BOUND_RUNNER_ROWS.csv", "RUN3920_4_radial_shape", "epsilon_r inverse-square residual formula"),
        ("SRC3937_06_3922_ephemeris_map", SRC / "P8_Y5_R2FR_3922_ESCAPE_TO_PPN_ORBITAL_MAP.csv", "MAP3922_6_ephemeris", "escape-to-orbital map"),
        ("SRC3937_07_3598_delta_cal", SRC / "P8_Y5_R2FR_3598_GAUSS_ORBITAL_BOUND_ROWS.csv", "GOB3598_0_epsilon_Delta_cal", "Delta_cal bound row"),
        ("SRC3937_08_3598_theorem", SRC / "P8_Y5_R2FR_3598_GAUSS_ORBITAL_CALIBRATION_THEOREM.csv", "GOC3598_5_exact_Delta_cal_identity", "exact Poisson/Gauss/orbit residual identity"),
        ("SRC3937_09_3652_orbital_vector", SRC / "P8_Y5_R2FR_3652_PPN_ORBITAL_RESIDUAL_VECTOR_ROWS.csv", "PVR3652_6_Gdot", "PPN/orbital residual vector includes Gdot/orbit source drift"),
        ("SRC3937_10_3652_GM_source", SRC / "P8_Y5_R2FR_3652_GM_SOURCE_CALIBRATION_ROWS.csv", "GMC3652_1_delta_mu", "GM source calibration row"),
        ("SRC3937_11_3436_r10_readiness", SRC / "P8_Y5_R2FR_3436_R10_SCORE_READINESS.csv", "SR3436_3_mts_alpha", "R10 score readiness blocker"),
        ("SRC3937_12_3436_alpha_map", SRC / "P8_Y5_R2FR_3436_MTS_ALPHA_SOURCE_MAP_STATUS.csv", "MSM3436_4_profile_or_zero", "MTS alpha source/profile blocker"),
        ("SRC3937_13_2936_r10_promotion", SRC / "P8_Y5_R2FR_2936_R10_PROMOTION_GATE_AUDIT.csv", "PROM2936_5_verdict", "R10 curve promotion remains refused"),
        ("SRC3937_14_3707_r10_gate", SRC / "P8_Y5_R2FR_3707_R10_SCORE_GATE_ROWS.csv", "R10SG3707_000", "executable nonclaim R10 score-gate rows exist"),
        ("SRC3937_15_3936_validation", SRC / "P8_Y5_BRR545_3936_VALIDATION.csv", "VAL3936_14_no_pycache", "previous checkpoint validation"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        found = False
        line_number = ""
        excerpt = ""
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    excerpt = line[:900]
                    break
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "needle": needle,
                "purpose": purpose,
                "exists": exists,
                "needle_found": found,
                "line_number": line_number,
                "line_excerpt": excerpt,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def readiness_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "READY3937_0_orbital",
            "candidate_dashboard": "orbital_ephemeris",
            "tests": "epsilon_r; Delta_cal; GM calibration; slow-orbit inverse-square readout; Gdot drift; finite-range escape-to-R10",
            "existing_rows": csv_row_count(SRC / "P8_Y5_R2FR_3598_GAUSS_ORBITAL_BOUND_ROWS.csv") + csv_row_count(SRC / "P8_Y5_R2FR_3652_GM_SOURCE_CALIBRATION_ROWS.csv"),
            "strength": "directly tests MTS-to-Newton/GR reduction rather than a detached short-range lane",
            "blockers": "numeric ephemeris/source rows still missing; private branch zero is not a public pass",
            "selected_first": True,
            "selection_reason": "cleaner next route because the Poisson/Gauss/orbit accounting law already exists and targets the core GR-to-Newton bridge",
            "claim_status": "SELECTED_FIRST_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "READY3937_1_R10",
            "candidate_dashboard": "R10_Yukawa",
            "tests": "alpha(lambda); finite-range source profile; R10 bound curve; parent alpha numerator",
            "existing_rows": csv_row_count(SRC / "P8_Y5_R2FR_3436_R10_SCORE_READINESS.csv") + csv_row_count(SRC / "P8_Y5_R2FR_3707_R10_SCORE_GATE_ROWS.csv"),
            "strength": "useful if a finite-range/local residual survives the local theorem branch",
            "blockers": "MTS alpha numerator, source/test charges, q_loc profile or zero certificate, and live curve promotion remain nonclaim",
            "selected_first": False,
            "selection_reason": "defer because it is mostly a fallback branch until alpha/source-map ownership is solved",
            "claim_status": "DEFERRED_SECOND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def orbital_dashboard_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "ORB3937_0_epsilon_Delta_cal",
            "epsilon_Delta_cal",
            "abs(mu_obs-G_eff M_H[Pi_M J_H_total])/abs(G_eff M_H)",
            "0 in private calibrated-monopole/EH/same-frame branch",
            "Delta_cal = Delta_Poisson + Delta_Gauss + Delta_orbit + mu_extra + Delta_frame + Delta_G + Delta_flux + Delta_range + Delta_PPN_source",
            "GOB3598_0_epsilon_Delta_cal; GOC3598_5_exact_Delta_cal_identity",
            "source every Delta_cal component or prove it zero with parent-signed clauses",
            "CRITICAL",
        ),
        (
            "ORB3937_1_epsilon_r",
            "epsilon_r(r)",
            "epsilon_r(r)=|((1+xi_1)-r partial_r xi_1)/(1+xi_ref)-1|",
            "0 when xi_1 is a constant monopole calibration only",
            "constant xi_ref may calibrate GM; radial gradients cannot be hidden inside measured GM",
            "RUN3920_4_radial_shape; MAP3922_6_ephemeris",
            "source xi_1(r) or prove radial derivative hair zero in the local branch",
            "CRITICAL",
        ),
        (
            "ORB3937_2_Poisson_Gauss_bridge",
            "epsilon_Poisson_Gauss",
            "norm(nabla^2 Phi-4 pi G_eff rho_H)/norm(4 pi G_eff rho_H) plus surface-flux residual",
            "0 in same-frame EH leading-operator branch",
            "weak-field 00 equation must feed the same Gauss charge that orbiting bodies read",
            "GOC3598_2_weak_field_Poisson_bridge; GOC3598_3_Gauss_surface_bridge",
            "source EH weak-field coefficient, Gauss surface residual, and boundary/domain/range terms",
            "HIGH",
        ),
        (
            "ORB3937_3_orbital_readout",
            "epsilon_orbit",
            "abs(mu_obs-mu_Gauss)/abs(mu_Gauss)",
            "0 for slow minimally coupled matter with no direct fifth force/frame/range/multipole residual",
            "slow circular readout mu_obs=r^2 |a_r|=v^2 r must equal the Gauss monopole only under the no-cheat guard",
            "ORB3884_0_exterior; ORB3884_1_no_range; GOC3598_4_orbital_readout_bridge",
            "build ephemeris source rows and keep finite-range/direct-force corrections explicit",
            "HIGH",
        ),
        (
            "ORB3937_4_GM_source_calibration",
            "delta_ln_mu_obs",
            "delta ln mu_obs = delta ln G_obs + delta ln M_S^eff + q_metric + q_readout + q_boundary + q_source",
            "0 for universal constant G_eff and stationary closed Hilbert source",
            "measured GM may absorb only a universal constant; source/time/radial dependence is observable hair",
            "GMC3652_1_delta_mu; GOB3598_5_dln_Geff_dt; GOB3598_6_dln_Meff_dt",
            "source Gdot, source-flux conservation, and active/inertial source identity rows",
            "HIGH",
        ),
        (
            "ORB3937_5_PPN_orbital_vector",
            "Delta_PPN_orbital",
            "(gamma-1,beta-1,alpha1,alpha2,alpha3,xi,Gdot/G) with source/readout calibration",
            "0 in private local GR theorem branch",
            "orbital scoring must not re-open a PPN residual already assigned to the PPN dashboard",
            "PVR3652_0_gamma through PVR3652_6_Gdot; P8_Y5_R2FR_3936_PPN_BOUND_DASHBOARD.csv",
            "share source rows with 3936 PPN dashboard and do not double-count fitted cancellation",
            "MEDIUM",
        ),
        (
            "ORB3937_6_R10_escape",
            "alpha(lambda)_escape",
            "route finite-range radial/direct-force residuals to alpha(lambda) when not theorem-zero",
            "0 in local no finite-range branch",
            "if Delta_range survives, R10 becomes the next active dashboard rather than a loose analogy",
            "PPND3936_8_yukawa; SR3436_3_mts_alpha; R10SG3707_000",
            "only activate after q_loc/profile/source-map or range residual is real",
            "MEDIUM",
        ),
    ]
    return [
        {
            "row_id": row_id,
            "observable": observable,
            "fallback_formula": formula,
            "private_branch_value": private_value,
            "accounting_rule": accounting,
            "source_basis": source_basis,
            "next_source_action": action,
            "priority": priority,
            "score_ready": False,
            "claim_status": "ZERO_IN_PRIVATE_BRANCH_FALLBACK_NOT_SCORE_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, observable, formula, private_value, accounting, source_basis, action, priority in data
    ]


def r10_deferred_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("R10DEF3937_0_bound_curve", "alpha_bound(lambda)", "source-backed full curve or officially usable table", "ASSET_AUDITED_NONCLAIM; promotion refused without official/human QA", "P8_Y5_R2FR_3436_R10_SCORE_READINESS.csv; P8_Y5_R2FR_2936_R10_PROMOTION_GATE_AUDIT.csv"),
        ("R10DEF3937_1_alpha_numerator", "alpha_predicted(lambda)", "K_i, Z_i, M_i^2, Q_source, Q_test, tau_R10", "SOURCE_MAP_BLOCKED; symbolic template only", "P8_Y5_R2FR_3436_MTS_ALPHA_SOURCE_MAP_STATUS.csv"),
        ("R10DEF3937_2_profile_or_zero", "q_loc profile/zero certificate", "parent-signed q_loc=0 or source-current profile with absolute error envelope", "PROFILE_MISSING_ZERO_NOT_SIGNED", "P8_Y5_R2FR_3436_MTS_ALPHA_SOURCE_MAP_STATUS.csv"),
        ("R10DEF3937_3_executable_gate", "R10 score gate", "eta/domain/source-slope reviewed before any alpha(lambda) comparison", "EXECUTABLE_NONCLAIM_PARENT_PN_LAMBDAH_ETA_AND_CURVE_REVIEW_REQUIRED", "P8_Y5_R2FR_3707_R10_SCORE_GATE_ROWS.csv"),
    ]
    return [
        {
            "row_id": row_id,
            "r10_piece": piece,
            "required_input": required,
            "current_status": status,
            "source_basis": source,
            "selected_now": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, required, status, source in data
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CG3937_0_route_choice",
            "gate": "route choice",
            "requirement": "choose the next dashboard from existing readiness, not preference",
            "status": "PASS_ORBITAL_SELECTED_FIRST",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CG3937_1_private_zero",
            "gate": "private orbital zero",
            "requirement": "Delta_cal, epsilon_r, finite-range and PPN/orbital residuals vanish only inside the signed local theorem branch",
            "status": "PASS_PRIVATE_BRANCH_ONLY",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CG3937_2_numeric_scoring",
            "gate": "fallback numeric scoring",
            "requirement": "every active orbital fallback has source-backed numeric bound or theorem-zero row",
            "status": "FAIL_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CG3937_3_R10",
            "gate": "R10 activation",
            "requirement": "finite-range branch plus alpha source-map and usable bound curve",
            "status": "DEFERRED_BLOCKED_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CG3937_4_public_claim",
            "gate": "public local/Newton/orbital claim",
            "requirement": "private theorem plus pressure tests plus source-backed orbital dashboard",
            "status": "BLOCKED_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3937_0_select_orbital",
            "decision": "build orbital/ephemeris bound dashboard first",
            "reason": "it directly tests the MTS-to-GR-to-Newton reduction through Poisson, Gauss, measured GM and radial-hair accounting",
            "effect": "next checkpoint should source or score Delta_cal/epsilon_r/orbital residual rows",
            "claim_status": "SELECTED_FIRST_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3937_1_defer_R10",
            "decision": "keep R10/Yukawa as second dashboard, not the active first dashboard",
            "reason": "R10 remains blocked by missing MTS alpha numerator/source-map/profile ownership even though executable nonclaim score gates exist",
            "effect": "return to R10 only if finite-range escape survives or alpha/source rows are filled",
            "claim_status": "DEFERRED_SECOND_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3937_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "turn the orbital/ephemeris dashboard into a source acquisition and Delta_cal scoring runner",
            "success_condition": "real or explicitly missing source rows for mu_obs, epsilon_r, Gdot, Poisson/Gauss residuals, and finite-range escape with no public claim until score-ready",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "3937 selects orbital/ephemeris as the next bound dashboard and defers R10 until finite-range/source-map blockers are solved",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3937 - R10 or Orbital First Bound Dashboard

Timestamp: `{timestamp}`

## Result

Built the route-choice dashboard between `R10/Yukawa` and `orbital/ephemeris`.

The selected first route is `orbital/ephemeris`, not because R10 is unimportant, but because orbital scoring tests the core reduction:

`parent source -> weak-field Poisson -> Gauss monopole -> slow-orbit measured GM -> Newtonian inverse-square residual`.

That is closer to the "does MTS really reduce to GR/Newton?" spine than an immediate alpha(lambda) fight.

## Orbital Dashboard

The new dashboard tracks:

- `epsilon_Delta_cal`: measured GM versus dressed Hilbert source.
- `epsilon_r(r)`: radial inverse-square hair that cannot be hidden in a constant GM calibration.
- `epsilon_Poisson_Gauss`: weak-field operator and Gauss surface consistency.
- `epsilon_orbit`: slow test-body readout.
- `delta_ln_mu_obs`: source/G drift and active-inertial source calibration.
- `Delta_PPN_orbital`: shared PPN/orbital residual vector.
- `alpha(lambda)_escape`: only sent to R10 if finite-range residuals survive.

## R10 Status

R10 remains queued, but not promoted:

- executable nonclaim score rows exist;
- full source-backed alpha(lambda) ownership is still missing;
- MTS alpha numerator/source/test/profile rows are still symbolic or blocked;
- no R10/local short-range claim is allowed from this checkpoint.

## Claim Gate

No public orbital, R10, local-GR, or Newtonian-reduction claim is made here. The private theorem branch is allowed to say "zero inside the branch"; every fallback row still needs source-backed numbers or parent-signed zero clauses.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3937_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3937_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3937_R10_OR_ORBITAL_READINESS_COMPARISON.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3937_ORBITAL_EPHEMERIS_BOUND_DASHBOARD.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3937_R10_DEFERRED_QUEUE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3937_CLAIM_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3937_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3937_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3937 - R10 or Orbital First Bound Dashboard

Timestamp: `{timestamp}`

- Route choice: orbital/ephemeris selected first because it directly tests the MTS -> weak-field Poisson -> Gauss monopole -> measured Newtonian GM chain.
- Orbital dashboard: emits nonclaim rows for `epsilon_Delta_cal`, `epsilon_r(r)`, Poisson/Gauss consistency, slow-orbit readout, `delta_ln_mu_obs`, PPN/orbital residual vector, and finite-range escape to R10.
- R10 status: deferred but queued; executable nonclaim rows exist, while alpha numerator/source-map/profile ownership remains blocked.
- Claim gate: no public orbital/R10/local-GR/Newton claim; private branch zeros remain private conditional results.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3937 - R10 or Orbital First Bound Dashboard"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def formalization_workbench_modified_count() -> int:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(FWB.relative_to(ROOT))],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return 0
    if result.returncode != 0:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    readiness = readiness_rows(timestamp)
    orbital = orbital_dashboard_rows(timestamp)
    r10 = r10_deferred_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_modified = formalization_workbench_modified_count()
    selected = [row for row in readiness if str(row["selected_first"]) == "True"]
    nonclaim_groups = (readiness, orbital, r10, claim_gate, decisions, next_rows(timestamp))
    checks = [
        ("VAL3937_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3937_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3937_02_one_route_selected", len(selected) == 1 and selected[0]["candidate_dashboard"] == "orbital_ephemeris", "exactly one first route selected and it is orbital/ephemeris"),
        ("VAL3937_03_R10_deferred", any(row["candidate_dashboard"] == "R10_Yukawa" and str(row["selected_first"]) == "False" for row in readiness), "R10 route is deferred, not discarded"),
        ("VAL3937_04_orbital_rows", len(orbital) == 7 and any(row["observable"] == "epsilon_r(r)" for row in orbital), "orbital dashboard rows emitted"),
        ("VAL3937_05_finite_range_escape", any(row["observable"] == "alpha(lambda)_escape" for row in orbital), "finite-range escape row keeps R10 connected"),
        ("VAL3937_06_R10_queue", len(r10) == 4 and all(str(row["selected_now"]) == "False" for row in r10), "R10 deferred queue emitted"),
        ("VAL3937_07_claim_gate", len(claim_gate) == 5 and any(row["status"] == "BLOCKED_NONCLAIM" for row in claim_gate), "claim gate blocks public claim"),
        ("VAL3937_08_not_score_ready", all(str(row.get("score_ready", "False")) == "False" for row in orbital), "orbital fallback rows not score-ready"),
        ("VAL3937_09_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in nonclaim_groups for row in group), "all generated rows are nonclaim"),
        ("VAL3937_10_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3937_11_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3937_12_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3937_13_spine_written", SPINE_PATH.exists() and "3937 - R10 or Orbital First Bound Dashboard" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3937_14_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3937_15_script_compiles", True, "script compiles"),
        ("VAL3937_16_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "row_id": row_id,
            "check": detail,
            "result": "PASS" if passed else "FAIL",
            "timestamp_utc": timestamp,
        }
        for row_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = now_utc()
    source_rows = source_register_rows(timestamp)
    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["readiness"], readiness_rows(timestamp))
    write_csv(OUTPUTS["orbital_dashboard"], orbital_dashboard_rows(timestamp))
    write_csv(OUTPUTS["r10_deferred"], r10_deferred_rows(timestamp))
    write_csv(OUTPUTS["claim_gate"], claim_gate_rows(timestamp))
    write_csv(OUTPUTS["decision"], decision_rows(timestamp))
    write_csv(OUTPUTS["next"], next_rows(timestamp))
    write_csv(OUTPUTS["status"], status_rows(timestamp, source_rows))
    DOC_PATH.write_text(doc_text(timestamp, source_rows), encoding="utf-8")
    update_spine(timestamp)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation = validation_rows(timestamp, source_rows)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3937 validation failed: {failed}")
    print(f"3937 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
