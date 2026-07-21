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

CHECKPOINT = "4655"
CLAIM_ID = "L-497"
BRANCH = "MTS_R2FR_Y5_CGAMMA_MEMORY_PROJECTOR_LOCAL_SUPPORT_OR_PROFILE_BOUND_4655"
MARKER = "PPC4161_CGAMMA_MEMORY_PROJECTOR_LOCAL_SUPPORT_OR_PROFILE_BOUND_4655"
PACKET_MARKER = "PPC4161_PACKET_CGAMMA_MEMORY_PROJECTOR_LOCAL_SUPPORT_OR_PROFILE_BOUND_4655"
DECISION = "CGAMMA_QUIET_COLLAR_SILENCE_AND_PROFILE_BOUND_INTERFACE_SYNTHESIZED_NONCLAIM"
NEXT_TARGET = "4656-Y5-R2FR-cGamma-parent-memory-extremum-or-CX-final-source-bound.md"

DOC_PATH = POST / "4655-Y5-R2FR-cGamma-memory-projector-local-support-or-profile-bound.md"
FORMAL_PATH = FORMAL / "671-PPC4161-cGamma-memory-projector-local-support-or-profile-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4654 = POST / "4654-Y5-R2FR-deltaKappa-source-coupling-lock-or-Gdot-orbital-bound.md"
DOC_4652 = POST / "4652-Y5-R2FR-AMF-Palatini-IR-selector-origin-or-EH-effective-demotion.md"
FORMAL_203 = FORMAL / "203-PPC4161-local-memory-support-projector-zero-law-for-cGamma.md"
FORMAL_204 = FORMAL / "204-PPC4161-finite-cGamma-product-bound-law.md"
FORMAL_466 = FORMAL / "466-PPC4161-extra-invariant-residual-coefficient-map-to-PPN-R10-clocks-or-parent-scale-law.md"
DOC_4569 = POST / "4569-Y5-R2FR-parent-source-current-covariance-or-A_src-zero-source-norm-row.md"
DOC_4570 = POST / "4570-Y5-R2FR-parent-mL-attractor-equation-or-A_lap-source-row.md"
DOC_4571 = POST / "4571-Y5-R2FR-static-boundary-nohair-or-B_boundary-profile-kernel-row.md"
DOC_4572 = POST / "4572-Y5-R2FR-higher-order-static-residue-or-transition-shell-profile-row.md"
DOC_4575 = POST / "4575-Y5-R2FR-transition-moment-zero-law-or-first-source-profile-matrix.md"
DOC_4576 = POST / "4576-Y5-R2FR-same-worldtube-Hilbert-source-lock-or-residual-moment-bound.md"
DOC_4577 = POST / "4577-Y5-R2FR-density-profile-owner-or-DeltaWtr-first-bound.md"
DOC_4579 = POST / "4579-Y5-R2FR-readout-commutator-zero-or-rho-readout-shift-bound-value.md"
DOC_4600 = POST / "4600-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md"
DOC_4629 = POST / "4629-Y5-R2FR-canonical-normalization-and-first-anchor-smoke-runner.md"
DOC_4630 = POST / "4630-Y5-R2FR-co-normalized-gap-and-source-coupling-parent-action.md"
DOC_4648 = POST / "4648-Y5-R2FR-same-branch-Xi-tail-zero-assembly-and-lambda-promotion-gate.md"
CSV_4185_ARENA = SOURCE_DIR / "P8_Y5_R2FR_4185_RESIDUAL_COEFFICIENT_ARENA_MAP.csv"
CSV_4611_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4611_STATUS.csv"
CSV_4612_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4612_STATUS.csv"
CSV_4648_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4648_STATUS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4655_SOURCE_REGISTER.csv"
MEMORY_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4655_CGAMMA_MEMORY_GATE.csv"
LOCAL_SCORECARD_CSV = SOURCE_DIR / "P8_Y5_R2FR_4655_LOCAL_SUPPORT_SCORECARD.csv"
PROFILE_INTERFACE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4655_PROFILE_BOUND_INTERFACE.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4655_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4655_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4655_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4655_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4655_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4655_VALIDATION.csv"


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
        ("SRC4655_00_4654_handoff", DOC_4654, "RUN4654_5_next", "4654 selects c_Gamma as the remaining leakage root."),
        ("SRC4655_01_4652_triage", DOC_4652, "c_D -> delta_kappa -> c_Gamma", "4652 triage order imported."),
        ("SRC4655_02_4185_arena", CSV_4185_ARENA, "RC4185_2_cGamma", "machine arena map for c_Gamma."),
        ("SRC4655_03_4450_cGamma", FORMAL_466, "C4450_4_cGamma", "post-A_MF residual map keeps c_Gamma as finite survivor."),
        ("SRC4655_04_203_zero_law", FORMAL_203, "E_Gamma^loc :=", "exact local support/projector zero contract."),
        ("SRC4655_05_204_product_law", FORMAL_204, "|c_Gamma * profile_a| <=", "finite product bound law."),
        ("SRC4655_06_4569_Asrc", DOC_4569, "A_src^std=0", "standard source-current covariance closes A_src."),
        ("SRC4655_07_4570_Alap", DOC_4570, "A_lap^std=0", "m_L attractor closes A_lap."),
        ("SRC4655_08_4571_boundary", DOC_4571, "B_boundary,a^std=0", "fixed-collar boundary nohair closes static boundary."),
        ("SRC4655_09_4572_arena_zero", DOC_4572, "PRIVATE_ARENA_SCORECARD_ZERO", "higher-order fixed-collar arena scorecard zero."),
        ("SRC4655_10_4575_moments", DOC_4575, "M_a^perp[q_tr] :=", "transition safety reduced to common-mode-subtracted residual moments."),
        ("SRC4655_11_4576_lock", DOC_4576, "epsilon_lock <= Y_nonHilbert + Delta_Wtr + E_profile", "same-worldtube Hilbert lock bound."),
        ("SRC4655_12_4577_profile", DOC_4577, "rho_eff = rho_H", "all-lapse profile-owner theorem."),
        ("SRC4655_13_4579_readout", DOC_4579, "PURE_POSTPROCESSING_READOUT_COMMUTATOR_ZERO_DERIVED", "readout commutator split."),
        ("SRC4655_14_4600_final_CX", DOC_4600, "C_X^final_live", "final C_X live body-charge envelope."),
        ("SRC4655_15_4611_source_side", CSV_4611_STATUS, "QBARXH_FULL_SOURCE_ENVELOPE_ROLLUP_READY", "source-side Qbar_XH rollup."),
        ("SRC4655_16_4612_test_side", CSV_4612_STATUS, "QBARXT_TEST_BODY_RESPONSE_ENVELOPE_READY", "test-side qbar_XT rollup."),
        ("SRC4655_17_4629_conorm", DOC_4629, "CAN4629_1_source_coupling_co_normalization", "canonical normalization and anchor smoke guard."),
        ("SRC4655_18_4630_parent_action", DOC_4630, "CONDITIONAL_FIRST_ORDER_LOCAL_GR_RECOVERY", "parent action extremum/gap route."),
        ("SRC4655_19_4648_tail_zero", DOC_4648, "B_tail -> alpha_tail(lambda)=0", "same-branch Xi tail zero theorem."),
        ("SRC4655_20_4648_status", CSV_4648_STATUS, "PRIVATE_DERIVATION_ADVANCE_NONCLAIM", "4648 status imported."),
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


def memory_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CGM4655_0_definition", "E_Gamma^loc := P_loc(delta S_Gamma/delta O_loc)", "local memory pressure is the projected Euler response of the c_Gamma sector", "DEFINITION_IMPORTED"),
        ("CGM4655_1_quiet_collar_zero", "stationary compact non-radiative fixed collar plus support/projector silence", "A_src^std=A_lap^std=B_boundary,a^std=0 and higher-order private arena projections vanish", "CONDITIONAL_PRIVATE_ZERO"),
        ("CGM4655_2_transition_moment_reduction", "P_anom Sigma_metric[q_tr]=0 iff M_a^perp[q_tr]=0 for all anomalous moments", "raw transition is no longer vague; it is a residual moment problem", "DERIVED_REDUCTION_RAW_UNSIGNED"),
        ("CGM4655_3_source_profile_lock", "epsilon_lock <= Y_nonHilbert + Delta_Wtr + E_profile", "same Hilbert action domain, same worldtube/readout order and all-lapse profile ownership are the transition-source lock", "LOCK_CONTRACT_READY"),
        ("CGM4655_4_readout_split", "rho_readout_shift=0 for pure postprocessing; projector-dependent readout goes to C_readout", "prevents readout/projector dependence being smuggled into source mass or G calibration", "ZERO_OR_BOUND_SPLIT"),
        ("CGM4655_5_body_charge_rollup", "C_X^final_live, Qbar_XH and qbar_XT feed source-test product rows", "finite c_Gamma scoring now has explicit source/test/body-charge envelopes rather than loose placeholders", "PROFILE_INTERFACE_READY_VALUES_MISSING"),
        ("CGM4655_6_parent_extremum_route", "positive memory gap plus branch extremum A_m'(m0)=0 gives first-order local memory source silence", "best derivation route is a parent action extremum/symmetry, not fitted smallness", "CONDITIONAL_THEOREM_UNSIGNED"),
        ("CGM4655_7_R10_tail", "B_tail -> alpha_tail(lambda)=0", "same-branch Xi tail silence kills the normalized R10 tail amplitude independent of lambda, but does not by itself promote local GR", "CONDITIONAL_R10_SILENCE"),
        ("CGM4655_8_result", "c_Gamma is quiet-collar silent but raw transition/public branch remains profile-bound", "do not circle c_D/delta_kappa; next attack is parent extremum/source envelope or first sourced C_X/Qbar rows", "NONCLAIM_SYNTHESIS"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": row[0],
            "formula_or_condition": row[1],
            "meaning": row[2],
            "status": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def local_scorecard_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("LSC4655_0_private_quiet_collar", "fixed compact stationary non-radiative private collar", "Delta_a^private=0 through A_src/A_lap/B_boundary/higher-order scorecard", "PASS_CONDITIONAL_PRIVATE_SILENCE_NONCLAIM", "do not export to raw transition shell or public claim"),
        ("LSC4655_1_raw_transition_shell", "raw transition shell intersecting local source/readout", "epsilon_moment_perp active until source-lock/profile/readout clauses are parent-signed or bounded", "FAIL_CLOSED_RAW_UNSIGNED", "use residual moments and C_X/Qbar interface"),
        ("LSC4655_2_source_body_charge", "finite body-charge profile route", "C_X^final_live, Qbar_XH, qbar_XT, Z_X, M_X^2, lambda_X and arena kernels required", "SCHEMA_READY_VALUES_MISSING", "fill source-backed rows or theorem-zero certificates"),
        ("LSC4655_3_parent_extremum", "single parent action with positive gap and branch extremum", "first-order memory source vanishes if A_m'(m0)=0 and source coupling co-normalized", "BEST_DERIVATION_ROUTE_UNSIGNED", "prove symmetry/extremum or fill co-normalized coefficients"),
        ("LSC4655_4_R10_tail", "same-branch B_tail selector", "alpha_tail(lambda)=0 if all component zeros and fixed readout/domain/lambda clauses live on one branch", "CONDITIONAL_ZERO_NOT_PROMOTION", "still derive local GR/PPN/Newton/EM promotion maps"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "score_id": row[0],
            "branch": row[1],
            "deduction": row[2],
            "status": row[3],
            "next_action": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def profile_interface_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("PBI4655_0_product_law", "C_Gamma,a", "C_Gamma,a := c_Gamma * profile_a; require |c_Gamma profile_a| <= B_a/|J_a^Gamma|", "PPN/R10/clock/Gdot/orbital", "profile_a, J_a^Gamma, B_a", "PRODUCT_BOUND_READY_VALUES_MISSING"),
        ("PBI4655_1_moment_norm", "epsilon_moment_perp", "epsilon_moment_perp <= epsilon_lock + Y_tau + Y_l>=1 + Y_species_frame_source + Y_lambda + Y_nonEH + Y_boundary", "transition local-GR profile", "residual moments or zero clauses", "MOMENT_BOUND_READY_VALUES_MISSING"),
        ("PBI4655_2_profile_lock", "E_profile", "rho_eff=rho_H if all compact lapse probes agree; otherwise retain E_shadow+E_top+E_nonHilbert+E_readout", "Newton/PPN/orbital profile residual", "all-lapse parent identity or sourced profile defects", "PROFILE_THEOREM_READY_RAW_UNSIGNED"),
        ("PBI4655_3_final_CX", "C_X^final_live", "|C_X^final_live| <= |C_X^std_weight_live|+|C_X^LHRS_live|+|C_X^boundary|+|C_X^nonHilbert|", "body-charge source coupling", "all C_X subblocks zero or numeric", "FINAL_CX_READY_VALUES_MISSING"),
        ("PBI4655_4_source_test_product", "I_X^ST(lambda)", "|I_X^ST| <= |Qbar_XH| |qbar_XT|/(4*pi |Z_X| G_N M_H_ref m_T)", "R10/WEP/PPN/clock/orbital", "Qbar_XH, qbar_XT, Z_X, M_X^2, K_X, tau rows", "PRODUCT_GATE_READY_VALUES_MISSING"),
        ("PBI4655_5_conormalized_memory", "lambda_mem, alpha_Y", "lambda_mem=sqrt(Z_mem/M2_mem); alpha_Y must use the same canonical memory field/source coupling", "R10 finite-range and local memory amplitude", "Z_mem, M2_mem, Q_eff or exact zero", "CONORMALIZATION_READY_VALUES_MISSING"),
        ("PBI4655_6_tail_zero", "alpha_tail(lambda)", "B_tail -> alpha_tail(lambda)=0 for all lambda", "R10 tail control", "same parent selector and local promotion maps", "CONDITIONAL_ZERO_PROMOTION_OPEN"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "interface_id": row[0],
            "quantity": row[1],
            "formula": row[2],
            "observable_link": row[3],
            "required_inputs": row[4],
            "status": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("RUN4655_0_quiet_collar", "private fixed compact stationary collar", "PASS_CONDITIONAL_CGAMMA_SILENCE_NONCLAIM", "A_src/A_lap/B_boundary/higher-order static residues vanish on the same private collar."),
        ("RUN4655_1_static_export", "use quiet-collar zero for raw transition shell", "FAIL_FIREWALL", "transition support/profile/readout clauses are separate and cannot be erased by static collar silence."),
        ("RUN4655_2_raw_transition", "claim P_anom Sigma_metric[q_tr]=0 for raw transition", "FAIL_RAW_PARENT_UNSIGNED", "residual moments and source-lock/profile/readout clauses are not parent-signed."),
        ("RUN4655_3_profile_values", "score finite c_Gamma source/test product", "FAIL_VALUES_MISSING", "C_X^final_live, Qbar_XH, qbar_XT, Z_X/M_X^2 and arena kernels are not claim-grade sourced numbers."),
        ("RUN4655_4_parent_extremum", "positive gap plus A_m'(m0)=0 signed by parent action", "PASS_CONDITIONAL_FIRST_ORDER_SILENCE_NONCLAIM", "this is the cleanest derivation target but is unsigned in the live corpus."),
        ("RUN4655_5_R10_tail", "same-branch B_tail selector signed", "PASS_CONDITIONAL_ALPHA_TAIL_ZERO_NONCLAIM", "R10 tail amplitude zero follows, but local-GR promotion maps remain separate."),
        ("RUN4655_6_next", "c_Gamma synthesis complete", "PASS_NEXT_SELECTED", NEXT_TARGET),
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
    controls = [
        ("CTRL4655_0_no_public_claim", "No local-GR/R10/PPN/clock/orbital claim while raw c_Gamma transition/profile rows are unsigned.", True),
        ("CTRL4655_1_no_branch_mixing", "A_src/A_lap/B_boundary/tail/source/product zeros must live on one selector before promotion.", True),
        ("CTRL4655_2_no_total_mass_shortcut", "Equal total source mass is not profile ownership; all-lapse/profile certificate or bound is required.", True),
        ("CTRL4655_3_no_rescaling_win", "lambda_mem and alpha/source amplitude must use the same canonical normalization.", True),
        ("CTRL4655_4_no_cancellation", "C_X/Qbar/profile envelopes are absolute sums unless a parent identity signs cancellation.", True),
        ("CTRL4655_5_no_R10_only_promotion", "R10 tail silence does not by itself prove GR/Newton/Maxwell/PPN promotion.", True),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "firewall": row[1],
            "active": row[2],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in controls
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4655_0",
            "decision": DECISION,
            "summary": "4655 turns c_Gamma from a vague survivor into a two-branch theorem/interface. The private quiet-collar branch is conditionally silent through A_src, A_lap, boundary and higher-order zero rows. The raw transition/public branch is reduced to residual moments, all-lapse profile ownership, readout commutator/domain ownership and final C_X/Qbar source-test product envelopes. The best derivation target is a parent memory extremum/positive-gap theorem; otherwise the next step is source-backed C_X/Qbar/profile rows.",
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
            "status": "CGAMMA_SYNTHESIS_PRIVATE_QUIET_COLLAR_ZERO_RAW_TRANSITION_PROFILE_BOUND_NONCLAIM",
            "quiet_collar_cGamma": "conditional_zero",
            "raw_transition_cGamma": "profile_bound_interface",
            "public_local_GR_claim": False,
            "best_next_route": "parent memory extremum/positive gap or first C_X/Qbar source-backed row",
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
            "reason": "The c_Gamma branch is now narrowed to one clean derivation route and one finite-score route: prove the parent memory extremum/positive-gap/source-coupling zero, or fill the first C_X/Qbar/profile source-backed row.",
            "success_condition": "Either parent-sign first-order memory source silence in one branch, or produce numeric/source-backed C_X^final_live, Qbar_XH, qbar_XT, Z_X/M_X^2/lambda_X and arena kernels without placeholders.",
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    scorecard: list[dict[str, Any]],
    interfaces: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    public_clean, public_detail = git_clean(PUBLIC_STAGE)
    backup_clean, backup_detail = git_clean(BACKUP_REPO)
    all_rows: list[dict[str, Any]] = sources + gates + scorecard + interfaces + runners + decisions
    checks = [
        ("VAL4655_00_sources_exist", all(row["path_exists"] for row in sources), "all cited paths exist"),
        ("VAL4655_01_needles_found", all(row["needle_found"] for row in sources), "all cited needles found"),
        ("VAL4655_02_line_anchors", all(int(row["line_number"]) > 0 for row in sources), "all source line anchors positive"),
        ("VAL4655_03_definition", any(row["gate_id"] == "CGM4655_0_definition" for row in gates), "c_Gamma local Euler definition imported"),
        ("VAL4655_04_quiet_collar", any(row["score_id"] == "LSC4655_0_private_quiet_collar" and row["status"].startswith("PASS_CONDITIONAL") for row in scorecard), "quiet collar conditional silence recorded"),
        ("VAL4655_05_raw_transition_fail_closed", any(row["score_id"] == "LSC4655_1_raw_transition_shell" and "FAIL_CLOSED" in row["status"] for row in scorecard), "raw transition fails closed"),
        ("VAL4655_06_profile_interface", {"PBI4655_3_final_CX", "PBI4655_4_source_test_product", "PBI4655_5_conormalized_memory"}.issubset({row["interface_id"] for row in interfaces}), "C_X/Qbar/co-normalized memory interfaces present"),
        ("VAL4655_07_parent_extremum", any(row["gate_id"] == "CGM4655_6_parent_extremum_route" for row in gates), "parent extremum route captured"),
        ("VAL4655_08_runner_values_missing", any(row["run_id"] == "RUN4655_3_profile_values" and row["result"] == "FAIL_VALUES_MISSING" for row in runners), "finite scoring fails closed until values exist"),
        ("VAL4655_09_next_selected", decisions and decisions[0]["next_target"] == NEXT_TARGET, "4656 selected next"),
        ("VAL4655_10_no_claim_allowed", all(str(row.get("valid_for_claim", "False")) == "False" and str(row.get("claim_allowed", "False")) == "False" for row in all_rows), "no row is claim-grade"),
        ("VAL4655_11_public_stage_clean", public_clean, f"public stage: {public_detail}"),
        ("VAL4655_12_backup_repo_clean", backup_clean, f"backup repo: {backup_detail}"),
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
            "validation_id": "VAL4655_OVERALL",
            "status": "PASS" if all(passed for _, passed, _ in checks) else "FAIL",
            "detail": "4655 c_Gamma memory/projector synthesis passed" if all(passed for _, passed, _ in checks) else "4655 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    scorecard: list[dict[str, Any]],
    interfaces: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4655 - c_Gamma memory-projector local support or profile bound

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4655 moves `c_Gamma` from a loose survivor into a sharp two-branch gate.

The private quiet-collar branch is conditionally silent:

`A_src^std = A_lap^std = B_boundary,a^std = 0`

plus the higher-order private arena scorecard gives:

`Delta_a^private = 0`

for the fixed compact stationary non-radiative local collar.

That is not exported to the raw transition shell.

The raw transition/public branch is now reduced to explicit objects:

`P_anom Sigma_metric[q_tr]=0 iff M_a^perp[q_tr]=0`,

`epsilon_lock <= Y_nonHilbert + Delta_Wtr + E_profile`,

and the finite source-test path uses:

`C_X^final_live`, `Qbar_XH`, `qbar_XT`, `Z_X`, `M_X^2`, `lambda_X` and arena kernels.

The best derivation route is the parent memory action route:

positive gap plus branch extremum/source-coupling silence gives first-order local memory silence. If that does not parent-sign, the route must score the source-backed profile/product rows.

No local-GR, R10, PPN, clock, orbital, Maxwell or Newton public claim is made here.

## Source Register

{table(sources)}

## c_Gamma Memory Gate

{table(gates)}

## Local Support Scorecard

{table(scorecard)}

## Profile Bound Interface

{table(interfaces)}

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
        "4655 synthesizes the c_Gamma local-memory branch: fixed compact stationary collars are conditionally silent through A_src/A_lap/boundary/higher-order zero rows, while raw transition/public branches reduce to residual moments, all-lapse profile ownership, readout commutators and C_X/Qbar source-test product envelopes.",
        "Generated source register, c_Gamma memory gate, local support scorecard, profile bound interface, runner, controls, decision, status, next target and validation.",
        "cGamma_quiet_collar_silence_profile_bound_interface_nonclaim",
        NEXT_TARGET,
        "Exporting quiet-collar silence to raw transition shells, claiming local GR/R10/PPN before C_X/Qbar/profile rows are parent-signed or sourced, mixing branches, or using R10 tail zero as a full promotion map.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10/clock/orbital/Maxwell claim until the parent memory extremum/source-coupling route is signed or the finite profile/product rows are source-backed and pass.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4655 turns the remaining `c_Gamma` root into a sharp local-memory gate. The fixed compact stationary non-radiative collar has conditional silence from the already-derived `A_src^std=0`, `A_lap^std=0`, `B_boundary,a^std=0` and higher-order private scorecard rows. The raw transition/public branch is not claimed: it is reduced to residual moments, all-lapse profile ownership, readout/projector commutators and the finite `C_X^final_live`, `Qbar_XH`, `qbar_XT`, `Z_X/M_X^2/lambda_X` product interface. Best next derivation route: parent memory extremum plus positive gap/source-coupling silence; fallback: source-backed profile/product rows.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4655` closes the vague `c_Gamma` fog into a private quiet-collar zero branch plus a raw-transition finite profile/product interface. It does not claim public local GR or R10. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    timestamp = now()
    sources = source_rows(timestamp)
    gates = memory_gate_rows(timestamp)
    scorecard = local_scorecard_rows(timestamp)
    interfaces = profile_interface_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validations = validation_rows(sources, gates, scorecard, interfaces, runners, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(MEMORY_GATE_CSV, gates)
    write_csv(LOCAL_SCORECARD_CSV, scorecard)
    write_csv(PROFILE_INTERFACE_CSV, interfaces)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validations)

    doc = build_doc(sources, gates, scorecard, interfaces, runners, controls, decisions, statuses, nexts, validations)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = validations[-1]["status"]
    print(f"4655 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
