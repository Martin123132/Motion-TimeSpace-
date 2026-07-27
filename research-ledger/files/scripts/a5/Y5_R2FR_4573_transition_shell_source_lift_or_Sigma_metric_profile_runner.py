from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4573"
CLAIM_ID = "L-415"
BRANCH_ID = "MTS_R2FR_Y5_TRANSITION_SOURCE_LIFT_SIGMA_METRIC_PROFILE_RUNNER_4573"
MARKER = "PPC4161_TRANSITION_SOURCE_LIFT_OR_SIGMA_METRIC_PROFILE_RUNNER_4573"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_SOURCE_LIFT_SIGMA_METRIC_PROFILE_RUNNER_4573"
DECISION = "GENERIC_SIGMA_METRIC_ZERO_NOT_DERIVED_SOURCE_LIFT_CONTRACT_AND_PROFILE_RUNNER_WRITTEN_NONCLAIM"
NEXT_TARGET = "4574-Y5-R2FR-P_metric-loc-zero-theorem-or-transition-profile-source-pack.md"

FORMAL_PATH = FORMAL / "589-PPC4161-transition-shell-source-lift-or-Sigma-metric-profile-runner.md"
DOC_PATH = POST / "4573-Y5-R2FR-transition-shell-source-lift-or-Sigma_metric-profile-runner.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4572_FORMAL = FORMAL / "588-PPC4161-higher-order-static-residue-or-transition-shell-profile-row.md"
DOC_4572_POST = POST / "4572-Y5-R2FR-higher-order-static-residue-or-transition-shell-profile-row.md"
EQ_REGISTER = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
CSV_4572_TRANSITION = SOURCE_DIR / "P8_Y5_R2FR_4572_TRANSITION_SHELL_PROFILE_ROWS.csv"
CSV_4572_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4572_NEXT_TARGET.csv"
CSV_4283_INPUTS = SOURCE_DIR / "P8_Y5_R2FR_4283_SHELL_PROFILE_RUNNER_INPUTS.csv"
CSV_4283_RESULTS = SOURCE_DIR / "P8_Y5_R2FR_4283_SHELL_PROFILE_RUNNER_RESULTS.csv"
CSV_4283_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4283_STATUS.csv"
CSV_4283_SCOPE = SOURCE_DIR / "P8_Y5_R2FR_4283_NOFLUX_SELECTOR_SCOPE.csv"
CSV_4283_FIREWALL = SOURCE_DIR / "P8_Y5_R2FR_4283_CLAIM_FIREWALL.csv"
CSV_4292_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4292_TRANSITION_MEMBERSHIP_AUDIT.csv"
CSV_4295_VERDICT = SOURCE_DIR / "P8_Y5_R2FR_4295_PARENT_SIGNATURE_VERDICT.csv"
CSV_4295_PLEAK = SOURCE_DIR / "P8_Y5_R2FR_4295_PLEAK_DECOMPOSITION.csv"
CSV_4560_GAPS = SOURCE_DIR / "P8_Y5_R2FR_4560_PARENT_SIGNATURE_GAP_MAP.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4573_SOURCE_REGISTER.csv"
ZERO_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4573_SOURCE_LIFT_ZERO_CONTRACT.csv"
BRANCH_VERDICT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4573_SIGMA_METRIC_BRANCH_VERDICT.csv"
PROFILE_ROWS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4573_SIGMA_METRIC_PROFILE_RUNNER_ROWS.csv"
DRYRUN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4573_SIGMA_METRIC_PROFILE_DRYRUN.csv"
INPUT_QUEUE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4573_TRANSITION_PROFILE_INPUT_QUEUE.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4573_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4573_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4573_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4573_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4573_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


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
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
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
        lines.append(
            "| "
            + " | ".join(
                str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
                for header in headers
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def append_once(path: Path, marker: str, block: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + block.strip() + "\n")


def source_rows() -> list[dict[str, Any]]:
    source_specs = [
        ("SRC4573_00_4572_formal", "4572 formal source-lift blocker", DOC_4572_FORMAL, "Sigma_metric[q_tr] = MISSING_SOURCE_LIFT"),
        ("SRC4573_01_4572_post", "4572 post checkpoint blocker", DOC_4572_POST, "q_tr_shell_norm = MISSING_REAL_PROFILE"),
        ("SRC4573_02_4572_transition_csv", "4572 transition shell profile row", CSV_4572_TRANSITION, "TS4572_metric_source_lift"),
        ("SRC4573_03_4572_next", "4572 selected target", CSV_4572_NEXT, "transition-shell-source-lift"),
        ("SRC4573_04_4283_inputs", "4283 runner input rows", CSV_4283_INPUTS, "IN4283_1"),
        ("SRC4573_05_4283_results", "4283 runner dryrun controls", CSV_4283_RESULTS, "RUN4283_live"),
        ("SRC4573_06_4283_status", "4283 runner status", CSV_4283_STATUS, "STATUS4283_0"),
        ("SRC4573_07_4283_scope", "4283 no-flux scope", CSV_4283_SCOPE, "NF4283_1_shell_scope_fail"),
        ("SRC4573_08_4283_firewall", "4283 shell firewalls", CSV_4283_FIREWALL, "FW4283_0"),
        ("SRC4573_09_redteam_explicit", "red-team source-lift explicit blocker", RED_TEAM, "the source-lift problem is now explicit"),
        ("SRC4573_10_redteam_doubled", "red-team doubled action blocker", RED_TEAM, "no doubled action currently derives Sigma_metric[q_tr]=0"),
        ("SRC4573_11_eq_pmetric_zero", "equation register P_metric zero route", EQ_REGISTER, "P_metric,loc q_tr^nu = 0"),
        ("SRC4573_12_eq_threshold", "equation register local threshold", EQ_REGISTER, "P_metric,loc <= 4.212667126774669e-17"),
        ("SRC4573_13_4292_membership", "4292 transition membership audit", CSV_4292_AUDIT, "MA4292_0_parent_source_action"),
        ("SRC4573_14_4295_raw_kernel", "4295 raw transition kernel verdict", CSV_4295_VERDICT, "VERDICT4295_1_raw_transition_kernel"),
        ("SRC4573_15_4295_pleak", "4295 P_leak decomposition", CSV_4295_PLEAK, "PLEAK4295_0"),
        ("SRC4573_16_4560_parent_gaps", "4560 parent signature boundary/no-flux gap", CSV_4560_GAPS, "PS4560_4_boundary_sector_no_flux"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, label, path, needle in source_specs:
        source_text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "label": label,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needle": needle,
                "needle_found": bool_text(needle in source_text),
                "role": "source-lift zero proof audit and Sigma_metric profile runner",
                "valid_for_claim": "False",
            }
        )
    return rows


def zero_contract_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "contract_id": "ZC4573_0_define_source_lift",
            "route": "definition",
            "condition": "Sigma_metric[q_tr] := (2/sqrt(-g_obs)) delta S_tr[q_tr,g_obs]/delta g_obs",
            "would_imply": "The transition current becomes a metric source, a metric-null source, or a bounded metric residual instead of a free notation.",
            "corpus_status": "DEFINITION_ADDED_NOT_A_ZERO_THEOREM",
            "failure_mode": "q_tr is still a vector/current until S_tr or an equivalent tensor source lift is parent-owned.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "contract_id": "ZC4573_1_topological_boundary_exact",
            "route": "boundary/topological exact block",
            "condition": "S_tr = integral dB[q_tr] or a metric-independent topological density, with zero local collar pullback and fixed boundary Hamiltonian charge",
            "would_imply": "delta_g S_tr|W_loc = 0, so P_metric,loc Sigma_metric[q_tr] = 0",
            "corpus_status": "SIGNED_ONLY_FOR_SUPPORT_SEPARATED_COLLARS",
            "failure_mode": "4283 blocks applying the no-flux/topological language to collars intersecting transition support.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "contract_id": "ZC4573_2_projector_orthogonality",
            "route": "metric projector nullity",
            "condition": "P_metric,loc q_tr = 0 and delta_g P_metric,loc = 0 on the local collar",
            "would_imply": "q_metric,loc=0 and therefore no local transition metric source in PPN/R10/clock/orbital channels",
            "corpus_status": "QUARANTINE_CONDITION_NOT_PARENT_THEOREM",
            "failure_mode": "Equation-register and red-team rows treat P_metric,loc=0 as a required theorem or closure, not a derived fact.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "contract_id": "ZC4573_3_same_worldtube_hilbert_absorption",
            "route": "Hilbert monopole absorption",
            "condition": "q_tr is in the same observed-metric Hilbert source action before readout, is counted once, and has only a static l=0 monopole absorbed into M_H^dress",
            "would_imply": "No extra local residual beyond the calibrated Hilbert mass charge; non-EH monopole, multipoles, time drift and range hair vanish",
            "corpus_status": "CONDITIONAL_SELECTOR_UNSIGNED_FOR_RAW_TRANSITION",
            "failure_mode": "4292/4295 leave same-worldtube action membership and raw transition kernel membership unsigned.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "contract_id": "ZC4573_4_support_separated_collar",
            "route": "private compact support separation",
            "condition": "supp(q_tr) cap W_loc = empty, side/interface pullbacks vanish, and boundary Hamiltonian charge is fixed/routed",
            "would_imply": "P_loc Sigma_metric[q_tr]=0 in the private compact collar branch",
            "corpus_status": "DERIVED_ONLY_IN_RESTRICTED_PRIVATE_COLLAR",
            "failure_mode": "Does not solve generic Solar transition shells where W_loc intersects transition support.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "contract_id": "ZC4573_5_doubled_owner_or_solder",
            "route": "doubled/open-system owner connection or solder map",
            "condition": "Hidden metric dependence from nabla, trace lifts, connection contractions and solder maps cancels or is independent of g_loc",
            "would_imply": "Sigma_metric[q_tr]=0 by a parent Ward/owner-current identity",
            "corpus_status": "TESTED_AND_NOT_DERIVED_IN_74_TO_77_RED_TEAM_CHAIN",
            "failure_mode": "The solder/tetrad/connection map reintroduces g_loc or breaks covariance without a further theorem.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def branch_verdict_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "branch_id": "BV4573_0_private_support_separated",
            "domain": "fixed compact non-radiative local collar away from transition support",
            "source_lift_status": "QUIET_BY_SUPPORT_SEPARATION",
            "verdict": "LOCAL_PRIVATE_ZERO_BRANCH_RETAINED",
            "reason": "This is the 4281/4283 no-flux scope and is consistent with 4572 higher-order static residue zero.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "branch_id": "BV4573_1_raw_transition_shell",
            "domain": "generic Solar/local transition shell intersecting metric readout collar",
            "source_lift_status": "NOT_DERIVED",
            "verdict": "GENERIC_SIGMA_METRIC_ZERO_NOT_DERIVED",
            "reason": "No parent action block, same-worldtube Hilbert signature, projector theorem, or metric-null Ward identity currently sets Sigma_metric[q_tr]=0.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "branch_id": "BV4573_2_conditional_hilbert_monopole",
            "domain": "same-worldtube Hilbert l=0 transition membership before charge readout",
            "source_lift_status": "CONDITIONAL_UNSIGNED",
            "verdict": "PROMISING_BUT_NOT_PARENT_SIGNED",
            "reason": "Would convert the shell into calibrated mass charge, but 4292/4295 keep action membership and raw kernel membership unsigned.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "branch_id": "BV4573_3_profile_bound_route",
            "domain": "source-backed transition profile rows",
            "source_lift_status": "RUNNER_SCHEMA_READY_VALUES_MISSING",
            "verdict": "PROFILE_RUNNER_REQUIRED",
            "reason": "If zero theorem fails, the next honest route is to source P_metric,loc q_tr, Sigma_metric response, boundary response, K_perp and transport/B-gradient rows.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def profile_runner_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "profile_id": "PR4573_0_source_lift_zero",
            "quantity": "Sigma_metric[q_tr]",
            "profile_formula": "Sigma_metric[q_tr] := (2/sqrt(-g_obs)) delta S_tr[q_tr,g_obs]/delta g_obs",
            "profile_value": "MISSING_PARENT_ACTION_OR_SOURCE_LIFT",
            "pass_requirement": "Sigma_metric[q_tr]=0 by one parent-signed ZC4573 route, or bounded below local arena thresholds",
            "units": "metric stress/source response",
            "status": "SOURCE_LIFT_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "profile_id": "PR4573_1_pmetric_qtr",
            "quantity": "P_metric,loc q_tr",
            "profile_formula": "epsilon_Pmetric := ||P_metric,loc q_tr||/(||q_tr||+epsilon)",
            "profile_value": "MISSING_REAL_PROFILE_OR_PROJECTOR_THEOREM",
            "pass_requirement": "epsilon_Pmetric = 0 by theorem or epsilon_Pmetric <= 4.212667126774669e-17",
            "units": "dimensionless local metric leakage",
            "status": "PROFILE_OR_THEOREM_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "profile_id": "PR4573_2_qtr_shell_norm",
            "quantity": "q_tr_shell_norm",
            "profile_formula": "||q_tr|| normalized to local source budget",
            "profile_value": "MISSING_REAL_PROFILE",
            "pass_requirement": "q_tr_shell_norm <= 4.3819265819966744e-17",
            "units": "dimensionless threshold normalization",
            "status": "PROFILE_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "profile_id": "PR4573_3_sigma_metric_response",
            "quantity": "Sigma_metric_shell_response",
            "profile_formula": "epsilon_metric_tr := ||P_metric,loc Sigma_metric[q_tr]||/M_H_ref",
            "profile_value": "MISSING_REAL_PROFILE",
            "pass_requirement": "epsilon_metric_tr <= 4.212667126774669e-17",
            "units": "dimensionless local response",
            "status": "PROFILE_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "profile_id": "PR4573_4_boundary_response",
            "quantity": "boundary_response",
            "profile_formula": "epsilon_boundary := ||P_metric,loc boundary/domain-wall response||/M_H_ref",
            "profile_value": "MISSING_REAL_PROFILE",
            "pass_requirement": "epsilon_boundary <= 4.212667126774669e-17",
            "units": "dimensionless local response",
            "status": "PROFILE_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "profile_id": "PR4573_5_transport_Bgrad",
            "quantity": "R_transport_to_local_plus_R_Bgrad_to_local",
            "profile_formula": "|R_transport_to_local|+|R_Bgrad_to_local|",
            "profile_value": "MISSING_REAL_PROFILE",
            "pass_requirement": "0.1678939074330212*(mu_Xi T_res)/|c_Gamma|",
            "units": "AJ private units",
            "status": "PROFILE_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "profile_id": "PR4573_6_Kperp",
            "quantity": "K_perp_boundary_guard",
            "profile_formula": "||P_metric,loc K_perp_boundary|| or parent K_perp=0 theorem",
            "profile_value": "MISSING_REAL_PROFILE_OR_ZERO_THEOREM",
            "pass_requirement": "source-backed Kperp bound",
            "units": "PPN/tensor response",
            "status": "BOUND_OR_THEOREM_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def dryrun_rows(now: str) -> list[dict[str, Any]]:
    controls = [
        ("LIVE4573_missing", "Sigma_metric_shell_response", "MISSING_REAL_PROFILE", "4.212667126774669e-17"),
        ("CTRL4573_pass_sigma", "Sigma_metric_shell_response", "1.0e-18", "4.212667126774669e-17"),
        ("CTRL4573_fail_sigma", "Sigma_metric_shell_response", "1.0e-10", "4.212667126774669e-17"),
        ("CTRL4573_pass_qtr", "q_tr_shell_norm", "1.0e-18", "4.3819265819966744e-17"),
        ("CTRL4573_fail_qtr", "q_tr_shell_norm", "1.0e-10", "4.3819265819966744e-17"),
    ]
    rows: list[dict[str, Any]] = []
    for control_id, quantity, value, threshold in controls:
        try:
            numeric_value = float(value)
            numeric_threshold = float(threshold)
            verdict = "CONTROL_PASS_NONCLAIM" if numeric_value <= numeric_threshold else "CONTROL_FAIL_NONCLAIM"
        except ValueError:
            verdict = "BLOCKED_PENDING_REAL_PROFILE_INPUTS"
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH_ID,
                "generated_utc": now,
                "control_id": control_id,
                "quantity": quantity,
                "profile_value": value,
                "threshold": threshold,
                "verdict": verdict,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def input_queue_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "input_id": "IQ4573_0_parent_action",
            "needed_object": "S_tr[q_tr,g_obs] or equivalent tensor source lift",
            "minimum_content": "metric variables, connection/coframe dependence, boundary terms, support domain and variation rule",
            "acceptance_test": "delta S_tr/delta g_obs is computable and either zero by theorem or returns sourced Sigma_metric rows",
            "status": "MISSING_PARENT_INPUT",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "input_id": "IQ4573_1_projector_theorem",
            "needed_object": "P_metric,loc theorem",
            "minimum_content": "parent-defined projector algebra, normalization, covariance, and proof that P_metric,loc q_tr=0 or is below threshold",
            "acceptance_test": "P_metric,loc is not an imposed quarantine coefficient and survives variation/readout order",
            "status": "MISSING_PARENT_THEOREM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "input_id": "IQ4573_2_shell_profile",
            "needed_object": "real transition profile q_tr(r,t) and metric response kernel",
            "minimum_content": "normalization, units, local collar support, boundary response, K_perp row and arena projection map",
            "acceptance_test": "all PR4573 rows have positive numeric sourced values or parent zero theorems",
            "status": "MISSING_REAL_PROFILE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "input_id": "IQ4573_3_hilbert_membership",
            "needed_object": "same-worldtube Hilbert membership certificate for q_tr",
            "minimum_content": "same observed metric source action, support inside W_H before readout, once-only counting, l=0 static monopole and zero non-EH hair",
            "acceptance_test": "4292/4295 unsigned membership rows flip to parent-signed without calibration circularity",
            "status": "MISSING_PARENT_SIGNATURE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def promotion_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4573_0_zero_theorem_gate",
            "gate": "At least one ZC4573 zero route is parent-signed for the raw transition shell.",
            "status": "FAIL",
            "reason": "No generic raw-shell source-lift zero theorem is currently derived.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4573_1_profile_gate",
            "gate": "All PR4573 live rows are numeric, sourced and below threshold.",
            "status": "FAIL",
            "reason": "Live rows still contain MISSING_PARENT_ACTION_OR_SOURCE_LIFT, MISSING_REAL_PROFILE or MISSING_REAL_PROFILE_OR_ZERO_THEOREM.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "gate_id": "PG4573_2_nonclaim_firewall",
            "gate": "No local-GR/PPN/R10/clock/orbital claim fires from private compact branch while transition shell is unresolved.",
            "status": "PASS",
            "reason": "4573 explicitly separates support-separated private collar zero from generic transition-shell source-lift.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "source_lift_zero_derived": "False",
            "private_support_separated_zero_retained": "True",
            "profile_runner_schema_ready": "True",
            "live_profile_values_missing": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "next_target": NEXT_TARGET,
        }
    ]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "decision": DECISION,
            "status_id": "STATUS4573_0",
            "status": "GENERIC_SOURCE_LIFT_ZERO_NOT_DERIVED_PROFILE_RUNNER_READY",
            "summary": "4573 converts Sigma_metric[q_tr] from a prose blocker into an exact source-lift contract plus live profile runner rows. The private support-separated collar remains quiet, but raw/generic transition shells remain nonclaim until P_metric,loc zero or profile rows are sourced.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH_ID,
            "generated_utc": now,
            "next_target": NEXT_TARGET,
            "reason": "The source-lift audit says the decisive fork is now P_metric,loc: prove P_metric,loc q_tr=0 from the parent projector algebra, or source real transition-profile rows for the runner.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def doc_body(
    now: str,
    sources: list[dict[str, Any]],
    contracts: list[dict[str, Any]],
    verdicts: list[dict[str, Any]],
    profile_rows: list[dict[str, Any]],
    dryruns: list[dict[str, Any]],
    input_queue: list[dict[str, Any]],
    promotions: list[dict[str, Any]],
) -> str:
    return f"""# 4573 — Transition-shell source lift or Sigma_metric profile runner

Marker: `{MARKER}`  
Generated: `{now}`  
Decision: `{DECISION}`

## Short verdict

The generic transition-shell zero is **not** derived.  The useful progress is sharper:

```text
Sigma_metric[q_tr] := (2/sqrt(-g_obs)) delta S_tr[q_tr,g_obs] / delta g_obs
```

The transition problem is now an exact metric-variation contract, not a vibe.  The only currently clean zero is still the support-separated private collar.  The raw/generic transition shell must either satisfy a parent-owned source-lift zero theorem or supply real profile rows.

## Exact zero conditions

The local transition branch is safe only if one of these routes is parent-signed:

```text
1. Boundary/topological exact block:
   delta_g S_tr|W_loc = 0.

2. Projector nullity:
   P_metric,loc q_tr = 0 and delta_g P_metric,loc = 0.

3. Hilbert monopole absorption:
   q_tr is in the same observed-metric Hilbert source before charge readout,
   counted once, static l=0, and has no non-EH/range/time/species hair.

4. Support-separated collar:
   supp(q_tr) cap W_loc = empty with zero side/interface pullback.
```

Current corpus status: route 4 is valid only in the private support-separated collar.  Routes 1-3 are still unsigned for the raw transition shell.

## Source-lift contract rows

{markdown_table(contracts)}

## Branch verdict

{markdown_table(verdicts)}

## Profile runner rows

These are the rows a future real shell profile or parent source action must fill.

{markdown_table(profile_rows)}

## Dry-run controls

The runner control rows prove the threshold logic behaves correctly without pretending the live shell is solved.

{markdown_table(dryruns)}

## Required inputs

{markdown_table(input_queue)}

## Promotion gates

{markdown_table(promotions)}

## Source register

{markdown_table(sources)}

## Next target

`{NEXT_TARGET}`

Reason: prove `P_metric,loc q_tr=0` from the parent projector algebra, or move directly to source-backed transition profile acquisition.
"""


def spine_block(now: str) -> str:
    return f"""## PPC4161 4573 transition source lift / Sigma_metric runner

Marker: `{MARKER}`  
Generated: `{now}`

4573 does not claim the generic transition-shell zero.  It defines the required metric source lift
`Sigma_metric[q_tr] := (2/sqrt(-g_obs)) delta S_tr[q_tr,g_obs]/delta g_obs`
and proves the exact contract a future parent action must satisfy.  The support-separated compact collar remains quiet, but the raw/generic transition shell is still blocked unless one of four routes is parent-signed: topological/boundary exactness, `P_metric,loc q_tr=0` with variation-safe projector, same-worldtube Hilbert monopole absorption, or support separation.  A live profile runner schema now requires `epsilon_metric_tr <= 4.212667126774669e-17` or a zero theorem.

Decision: `{DECISION}`.  Next target: `{NEXT_TARGET}`.
"""


def packet_block(now: str) -> str:
    return f"""## 4573 packet update — transition source lift

Marker: `{PACKET_MARKER}`  
Generated: `{now}`

The private local packet remains internally quiet only on the fixed compact support-separated branch.  Transition shells are not folded into the packet as local-GR evidence.  `Sigma_metric[q_tr]` is now the required metric-source object, and the live transition rows stay nonclaim until `P_metric,loc q_tr=0` is parent-derived or source-backed profile values pass the runner thresholds.
"""


def append_claim() -> None:
    existing = read_text(CLAIMS_PATH)
    if CLAIM_ID in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_parent_signature",
        "claim": "4573 converts the transition-shell source-lift blocker into an exact Sigma_metric[q_tr] metric-variation contract and a live profile runner, while finding that the generic raw-shell zero is not derived.",
        "current_evidence": "Generated source register, source-lift zero contract rows, branch verdict rows, Sigma_metric profile runner rows, dry-run controls, required input queue, promotion gates, status and validation CSVs.",
        "status": DECISION.lower(),
        "next_test": NEXT_TARGET,
        "key_risk": "Treating support-separated private collar quietness, imposed P_metric,loc quarantine, or dry-run controls as a raw transition-shell local-GR proof.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Raw/generic transition shells still need a parent projector theorem, same-worldtube Hilbert source signature, or real source-backed profile rows.",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        writer.writerow(row)


def validation_rows(
    outputs: list[Path],
    sources: list[dict[str, Any]],
    profile_rows: list[dict[str, Any]],
    dryruns: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH_ID,
                "check_id": check_id,
                "check": check,
                "passed": bool_text(passed),
                "detail": detail,
            }
        )

    for path in outputs:
        add(f"VAL4573_exists_{path.name}", "output path exists", path.exists(), str(path))
        if path.suffix == ".csv" and path.exists():
            rows = read_csv(path)
            add(f"VAL4573_csv_parse_{path.name}", "CSV parses with at least one row", len(rows) > 0, f"rows={len(rows)}")

    add(
        "VAL4573_sources_exist",
        "all cited sources exist",
        all(row["exists"] == "True" for row in sources),
        "source register existence check",
    )
    add(
        "VAL4573_needles_found",
        "all cited source needles found",
        all(row["needle_found"] == "True" for row in sources),
        "source register needle check",
    )
    add(
        "VAL4573_nonclaim_profiles",
        "all profile rows remain nonclaim",
        all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in profile_rows),
        "profile rows firewalled",
    )
    add(
        "VAL4573_live_missing_blocks",
        "live rows remain blocked when source/profile inputs are missing",
        any("MISSING" in row["profile_value"] for row in profile_rows),
        "live profile rows contain explicit missing tokens",
    )
    add(
        "VAL4573_control_pass",
        "dry-run pass controls pass",
        any(row["control_id"] == "CTRL4573_pass_sigma" and row["verdict"] == "CONTROL_PASS_NONCLAIM" for row in dryruns),
        "Sigma pass control",
    )
    add(
        "VAL4573_control_fail",
        "dry-run fail controls fail",
        any(row["control_id"] == "CTRL4573_fail_sigma" and row["verdict"] == "CONTROL_FAIL_NONCLAIM" for row in dryruns),
        "Sigma fail control",
    )
    add(
        "VAL4573_decision_token",
        "decision token recorded",
        DECISION in read_text(DECISION_CSV) and DECISION in read_text(DOC_PATH),
        DECISION,
    )
    add(
        "VAL4573_next_target",
        "next target recorded",
        NEXT_TARGET in read_text(NEXT_CSV) and NEXT_TARGET in read_text(DOC_PATH),
        NEXT_TARGET,
    )
    add(
        "VAL4573_claim_register",
        "claim register updated",
        CLAIM_ID in read_text(CLAIMS_PATH),
        CLAIM_ID,
    )
    add(
        "VAL4573_spine_packet",
        "spine and packet markers present",
        MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH),
        f"{MARKER}; {PACKET_MARKER}",
    )
    return checks


def main() -> None:
    now = utc_now()
    sources = source_rows()
    contracts = zero_contract_rows(now)
    verdicts = branch_verdict_rows(now)
    profile_rows = profile_runner_rows(now)
    dryruns = dryrun_rows(now)
    input_queue = input_queue_rows(now)
    promotions = promotion_rows(now)
    decisions = decision_rows(now)
    statuses = status_rows(now)
    next_targets = next_rows(now)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_CONTRACT_CSV, contracts)
    write_csv(BRANCH_VERDICT_CSV, verdicts)
    write_csv(PROFILE_ROWS_CSV, profile_rows)
    write_csv(DRYRUN_CSV, dryruns)
    write_csv(INPUT_QUEUE_CSV, input_queue)
    write_csv(PROMOTION_CSV, promotions)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_targets)
    write_csv(STATUS_CSV, statuses)

    body = doc_body(now, sources, contracts, verdicts, profile_rows, dryruns, input_queue, promotions)
    DOC_PATH.write_text(body, encoding="utf-8", newline="\n")
    FORMAL_PATH.write_text(body, encoding="utf-8", newline="\n")

    append_once(SPINE_PATH, MARKER, spine_block(now))
    append_once(PACKET_PATH, PACKET_MARKER, packet_block(now))
    append_claim()

    outputs = [
        SOURCE_REGISTER,
        ZERO_CONTRACT_CSV,
        BRANCH_VERDICT_CSV,
        PROFILE_ROWS_CSV,
        DRYRUN_CSV,
        INPUT_QUEUE_CSV,
        PROMOTION_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    validations = validation_rows(outputs, sources, profile_rows, dryruns)
    write_csv(VALIDATION_PATH, validations)

    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"{CHECKPOINT} complete: {DECISION}")
    print(f"wrote: {DOC_PATH}")
    print(f"validation: {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
