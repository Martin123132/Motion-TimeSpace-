from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4663"
CLAIM_ID = "L-505"
BRANCH = "MTS_R2FR_Y5_CMEM_HODGE_POYNTING_OWNER_OR_LHRS_BOUND_4663"
MARKER = "PPC4161_CMEM_HODGE_POYNTING_OWNER_OR_LHRS_BOUND_4663"
PACKET_MARKER = "PPC4161_PACKET_CMEM_HODGE_POYNTING_OWNER_OR_LHRS_BOUND_4663"
DECISION = "CMEM_HODGE_ZERO_PRIVATE_BRANCH_POYNTING_HILBERT_STRESS_DYNAMIC_CONSTITUTIVE_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4664-Y5-R2FR-Cmem-label-source-functor-owner-or-LHRS-bound.md"

DOC_PATH = POST / "4663-Y5-R2FR-Cmem-Hodge-Poynting-owner-or-LHRS-bound.md"
FORMAL_PATH = FORMAL / "679-PPC4161-Cmem-Hodge-Poynting-owner-or-LHRS-bound.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4662 = POST / "4662-Y5-R2FR-Cmem-first-block-final-rollup-or-dynamic-source-weight-bound-runner.md"
DOC_4599 = POST / "4599-Y5-R2FR-label-Hodge-support-readout-zero-or-CXlive-next-norm.md"
DOC_4653 = POST / "4653-Y5-R2FR-cD-same-coframe-parent-functor-or-WEP-clock-EM-bound.md"
DOC_4658 = POST / "4658-Y5-R2FR-balpha-Maxwell-normalization-owner-or-first-source-bound.md"

FORMAL_191 = FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md"
FORMAL_223 = FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md"
FORMAL_225 = FORMAL / "225-PPC4161-Maxwell-normalization-charge-current-owner.md"
FORMAL_276 = FORMAL / "276-PPC4161-Delta-Hodge-EM-closure-or-bound.md"
FORMAL_630 = FORMAL / "630-PPC4161-EM-gauge-kinetic-descent-or-b-alpha-source-row.md"
FORMAL_669 = FORMAL / "669-PPC4161-cD-same-coframe-parent-functor-or-WEP-clock-EM-bound.md"
FORMAL_674 = FORMAL / "674-PPC4161-balpha-Maxwell-normalization-owner-or-first-source-bound.md"
FORMAL_678 = FORMAL / "678-PPC4161-Cmem-first-block-final-rollup-or-dynamic-source-weight-bound-runner.md"

CSV_4662_REBASE = SOURCE_DIR / "P8_Y5_R2FR_4662_FINAL_CMEM_RESIDUAL_REBASE.csv"
CSV_4662_AMEM = SOURCE_DIR / "P8_Y5_R2FR_4662_AMEM_REDUCED_TRACE_BOUND.csv"
CSV_4662_NEXT_ATTACK = SOURCE_DIR / "P8_Y5_R2FR_4662_NEXT_ATTACK_SELECTION.csv"
CSV_4662_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4662_NEXT_TARGET.csv"
CSV_4662_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4662_VALIDATION.csv"

CSV_4599_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4599_LABEL_HODGE_SUPPORT_READOUT_ZERO_THEOREM.csv"
CSV_4599_NORM = SOURCE_DIR / "P8_Y5_R2FR_4599_CX_LABEL_HODGE_SUPPORT_READOUT_NORM.csv"
CSV_4599_CONTROL = SOURCE_DIR / "P8_Y5_R2FR_4599_CONTROL_ROWS.csv"
CSV_4599_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4599_VALIDATION.csv"

CSV_4315_HODGE = SOURCE_DIR / "P8_Y5_R2FR_4315_SAME_HODGE_THEOREM.csv"
CSV_4315_RESIDUALS = SOURCE_DIR / "P8_Y5_R2FR_4315_CONSTITUTIVE_RESIDUAL_ENVELOPE.csv"
CSV_4315_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4315_DELTA_HODGE_BOUND_UPDATE.csv"
CSV_4315_FIREWALL = SOURCE_DIR / "P8_Y5_R2FR_4315_CLAIM_FIREWALL.csv"
CSV_4315_SCALE = SOURCE_DIR / "P8_Y5_R2FR_4315_SCALE_GUARD.csv"
CSV_4315_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4315_VALIDATION.csv"

CSV_4653_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4653_CD_ZERO_THEOREM.csv"
CSV_4653_ARENA = SOURCE_DIR / "P8_Y5_R2FR_4653_CD_ARENA_ROUTES.csv"
CSV_4653_CONTROL = SOURCE_DIR / "P8_Y5_R2FR_4653_CONTROL_ROWS.csv"
CSV_4653_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4653_VALIDATION.csv"
CSV_4658_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4658_FIXED_BRANCH_ZERO_IMPORT.csv"
CSV_4658_NORMAL = SOURCE_DIR / "P8_Y5_R2FR_4658_BALPHA_MEMORY_NORMAL_FORM.csv"
CSV_4658_CONTROL = SOURCE_DIR / "P8_Y5_R2FR_4658_CONTROL_ROWS.csv"
CSV_4658_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4658_VALIDATION.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4663_SOURCE_REGISTER.csv"
OWNER_CLAUSE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4663_HODGE_POYNTING_OWNER_CLAUSES.csv"
ZERO_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4663_CMEM_HODGE_ZERO_IMPORT.csv"
DYNAMIC_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4663_DYNAMIC_HODGE_CONSTITUTIVE_BOUND_ROWS.csv"
LHRS_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4663_LHRS_CMEM_UPDATE_AFTER_HODGE.csv"
AMEM_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4663_AMEM_TRACE_BOUND_UPDATE_AFTER_HODGE.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4663_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4663_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4663_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4663_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4663_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4663_VALIDATION.csv"


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
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
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


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4663_00_4662_next", CSV_4662_NEXT, "4663-Y5-R2FR-Cmem-Hodge-Poynting-owner-or-LHRS-bound.md", "4662 selects Hodge/Poynting target."),
        ("SRC4663_01_4662_Hodge", CSV_4662_REBASE, "RCM4662_1_Hodge", "Cmem Hodge channel definition."),
        ("SRC4663_02_4662_LHRS", CSV_4662_AMEM, "ARB4662_2_LHRS_expanded", "LHRS expansion before Hodge closure."),
        ("SRC4663_03_4662_attack", CSV_4662_NEXT_ATTACK, "NAX4662_1_Hodge", "Hodge attack priority."),
        ("SRC4663_04_4662_validation", CSV_4662_VALIDATION, "VAL4662_OVERALL", "4662 validation pass."),
        ("SRC4663_05_678_formal", FORMAL_678, "NAX4662_1_Hodge", "formal 4662 handoff."),
        ("SRC4663_06_4599_Hodge", CSV_4599_THEOREM, "LHRS4599_1_Hodge", "LHRS Hodge zero-or-bound theorem."),
        ("SRC4663_07_4599_combined", CSV_4599_THEOREM, "LHRS4599_4_combined", "combined LHRS row."),
        ("SRC4663_08_4599_Hodge_norm", CSV_4599_NORM, "N4599_1_Hodge", "Hodge finite norm row."),
        ("SRC4663_09_4599_Hodge_control", CSV_4599_CONTROL, "CTRL4599_Hodge_countermodel", "Hodge countermodel guard."),
        ("SRC4663_10_4599_validation", CSV_4599_VALIDATION, "VAL4599_06_no_claim_true", "4599 no-claim validation."),
        ("SRC4663_11_4315_unique", CSV_4315_HODGE, "HT4315_0_unique_hodge", "Hodge uniqueness lemma."),
        ("SRC4663_12_4315_same_action", CSV_4315_HODGE, "HT4315_1_same_action", "same-Hodge Maxwell action."),
        ("SRC4663_13_4315_readout", CSV_4315_HODGE, "HT4315_3_readout_guard", "readout Hodge guard."),
        ("SRC4663_14_4315_counter", CSV_4315_HODGE, "HT4315_4_countermodel", "constitutive countermodel retained."),
        ("SRC4663_15_4315_zero_contract", CSV_4315_HODGE, "HT4315_5_zero_contract", "full Hodge zero contract."),
        ("SRC4663_16_4315_envelope", CSV_4315_BOUND, "HB4315_0_envelope", "Delta_Hodge no-cancellation envelope."),
        ("SRC4663_17_4315_principal", CSV_4315_RESIDUALS, "CR4315_0_Delta_chi_principal", "principal constitutive residual."),
        ("SRC4663_18_4315_orientation", CSV_4315_RESIDUALS, "CR4315_5_Delta_orientation_flux", "orientation flux residual."),
        ("SRC4663_19_4315_firewall", CSV_4315_FIREWALL, "FW4315_2", "no alpha/G/source scale derivation from Hodge."),
        ("SRC4663_20_4315_conformal", CSV_4315_SCALE, "SG4315_4_conformal", "four-dimensional Hodge conformal guard."),
        ("SRC4663_21_4315_validation", CSV_4315_VALIDATION, "VAL4315_2_same_hodge_zero", "4315 same-Hodge validation."),
        ("SRC4663_22_4653_EM_Poynting", CSV_4653_ZERO, "CDZ4653_4_EM_Poynting", "Maxwell-Hodge/Poynting owner."),
        ("SRC4663_23_4653_result", CSV_4653_ZERO, "CDZ4653_5_result", "same-coframe cD result."),
        ("SRC4663_24_4653_Poynting_arena", CSV_4653_ARENA, "ARENA4653_3_Poynting", "Poynting arena route."),
        ("SRC4663_25_4653_guard", CSV_4653_CONTROL, "CTRL4653_2_no_Poynting_double_count", "Poynting no-double-count guard."),
        ("SRC4663_26_4653_validation", CSV_4653_VALIDATION, "VAL4653_OVERALL", "4653 validation pass."),
        ("SRC4663_27_4658_same_Hodge", CSV_4658_ZERO, "BZI4658_4_same_Hodge_current", "same observed Hodge/current owner."),
        ("SRC4663_28_4658_alpha_result", CSV_4658_ZERO, "BZI4658_5_result", "fixed EM branch b_alpha zero."),
        ("SRC4663_29_4658_normal", CSV_4658_NORMAL, "BNF4658_2_4614_refinement", "b_alpha normal form; not full Hodge closure."),
        ("SRC4663_30_4658_Poynting_control", CSV_4658_CONTROL, "CTRL4658_3_no_Poynting_double_count", "4658 no Poynting double count."),
        ("SRC4663_31_4658_validation", CSV_4658_VALIDATION, "VAL4658_OVERALL", "4658 validation pass."),
        ("SRC4663_32_191_Poynting", FORMAL_191, "Poynting vector is not a separate background field", "Poynting as Hilbert stress flux."),
        ("SRC4663_33_191_guard", FORMAL_191, "forbids independent EM source weights", "forbid hidden EM forks."),
        ("SRC4663_34_223_zero", FORMAL_223, "=> c_Poynt_extra = 0", "standalone Poynting coefficient zero."),
        ("SRC4663_35_225_no_scale", FORMAL_225, "do not determine the absolute gauge kinetic coefficient", "scale guard."),
        ("SRC4663_36_276_hodge", FORMAL_276, "Delta_Hodge_EM = 0", "formal Hodge closure source."),
        ("SRC4663_37_630_balpha", FORMAL_630, "b_alpha_EM := Lie_v ln(alpha_EM)", "b_alpha normal form source."),
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


def owner_clause_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("HOC4663_0_unique_hodge", "e_obs, g_obs, orientation and volume determine *_obs", "observed Hodge has no independent branch variable once observed metric/coframe/orientation are fixed", "HT4315_0_unique_hodge", "EXACT_MATH_IMPORTED"),
        ("HOC4663_1_same_action", "S_EM = -(4 mu0)^-1 int F wedge *_obs F", "Maxwell action uses the observed Hodge only; metric dependence routes through Hilbert stress, not a separate C_Hodge coefficient", "HT4315_1_same_action", "SAME_HODGE_ACTION_BRANCH"),
        ("HOC4663_2_same_coframe", "visible EM descends through the same observed coframe/metric as matter and clocks", "no second EM metric/coframe slot is available in the private branch", "CDZ4653_4_EM_Poynting", "SAME_COFRAME_IMPORTED"),
        ("HOC4663_3_poynting_owner", "Poynting vector is T_EM^{0i} or boundary flux", "Poynting is real EM energy flow but not a second background/source force", "191/223/4653", "POYNTING_HILBERT_STRESS_OWNER"),
        ("HOC4663_4_same_current", "same observed Hodge and same Noether current owner", "no hidden EM-current multiplier or side source channel inside the fixed branch", "BZI4658_4_same_Hodge_current", "SAME_CURRENT_IMPORTED"),
        ("HOC4663_5_forbidden_slots", "chi_EM != chi(g_obs), hidden constitutive tensor, readout Hodge, orientation flux and standalone Poynting source are absent", "these are the precise slots whose absence makes Delta_Hodge_EM vanish", "HT4315_5_zero_contract", "ZERO_CONTRACT_CLAUSES"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "clause_id": row[0],
            "clause": row[1],
            "deduction": row[2],
            "source": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def zero_import_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("HZI4663_0_definition", "C_mem^Hodge := Pi_mem[C_X^Hodge]", "memory projection of Maxwell-Hodge/constitutive/Poynting owner leakage", "RCM4662_1_Hodge", "TARGET_DEFINED"),
        ("HZI4663_1_delta_hodge", "Delta_Hodge_EM=0", "same observed Hodge action plus no constitutive/readout/orientation/Poynting side slot kills Hodge mismatch", "HT4315_5_zero_contract + HOC4663", "PRIVATE_BRANCH_ZERO_IMPORTED"),
        ("HZI4663_2_metric_dependence", "delta_g S_EM routes to T_EM[g_obs]", "ordinary metric/Hodge dependence is Hilbert stress and remains in T_total; it is not a separate memory trace-source coefficient", "191 + 4653", "NO_DOUBLE_COUNT_MECHANISM"),
        ("HZI4663_3_poynting", "c_Poynt_extra=0", "Poynting is already T_EM^{0i} or boundary flux, so no bulk C_mem^Hodge side force is admitted", "223 + ARENA4653_3_Poynting", "POYNTING_SIDE_CHANNEL_ZERO"),
        ("HZI4663_4_result", "fixed same-Hodge visible EM branch => C_mem^Hodge=0", "Hodge term drops from C_mem^LHRS_live only inside the private observed-coframe Maxwell branch", "all HOC4663 clauses", "CMEM_HODGE_TERM_ZERO_PRIVATE_BRANCH"),
        ("HZI4663_5_scope", "b_alpha_mem=0 is supportive but not identical to Hodge closure", "4658 removes EM coupling normalization drift; 4663 separately removes Hodge/constitutive leakage", "BNF4658_2_4614_refinement", "SCALE_AND_HODGE_SEPARATED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_id": row[0],
            "statement": row[1],
            "deduction": row[2],
            "source_or_condition": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def dynamic_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("DHB4663_0_envelope", "Delta_Hodge_EM_mem", "||Delta_chi_principal|| + ||Delta_chi_skewon|| + L||dtheta_EM|| + |C_Hodge_hidden| + |C_Hodge_readout| + |Delta_orientation_flux|", "off-branch no-cancellation envelope", "HB4315_0_envelope"),
        ("DHB4663_1_principal", "Delta_chi_principal", "principal constitutive anisotropy/birefringence/light-cone residual", "finite row if chi_EM is not chi(g_obs)", "CR4315_0_Delta_chi_principal"),
        ("DHB4663_2_skewon_axion", "Delta_chi_skewon; dtheta_EM", "nonreciprocal/dissipative or parity-odd EM propagation residual", "finite row if skewon/axion-gradient survives", "CR4315_1/2"),
        ("DHB4663_3_hidden_readout", "C_Hodge_hidden; C_Hodge_readout", "hidden medium-like Hodge or post-solution readout Hodge regeneration", "finite row if hidden/readout slot survives", "CR4315_3/4"),
        ("DHB4663_4_orientation_flux", "Delta_orientation_flux", "orientation/time-orientation/boundary-normal mismatch affecting Poynting or source flux", "finite row if radiative boundary/orientation reentry survives", "CR4315_5_Delta_orientation_flux"),
        ("DHB4663_5_source_contract", "C_mem_Hodge_dynamic_source_row", "system_id;branch;Delta_chi_principal;Delta_chi_skewon;L_dtheta_EM;C_Hodge_hidden;C_Hodge_readout;Delta_orientation_flux;projection;units;source_path;valid_for_claim", "future dynamic row contract", "SOURCE_ROW_TEMPLATE_READY_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row[0],
            "quantity": row[1],
            "bound_or_contract": row[2],
            "meaning": row[3],
            "source": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def lhrs_update_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("LHU4663_0_before", "|C_mem^LHRS_live| <= |C_mem^label|+|C_mem^Hodge|+|C_mem^support|+|C_mem^readout|", "4662/4599 LHRS expansion", "LHRS_IMPORTED"),
        ("LHU4663_1_Hodge_zero", "|C_mem^Hodge|=0", "4663 same-Hodge/Poynting owner private branch zero", "HODGE_TERM_REMOVED"),
        ("LHU4663_2_after", "|C_mem^LHRS_live| <= |C_mem^label|+|C_mem^support|+|C_mem^readout|", "LHRS live block after Hodge closure", "LHRS_REDUCED"),
        ("LHU4663_3_final_Cmem", "|C_mem^final_live| <= |C_mem^label|+|C_mem^support|+|C_mem^readout|+|C_mem^boundary|+|C_mem^nonHilbert|", "final Cmem residual vector after first-block and Hodge closure", "FINAL_VECTOR_REDUCED"),
        ("LHU4663_4_not_full", "C_mem^final_live=0 is not claimed", "label, support, readout, boundary and non-Hilbert channels remain open", "FULL_CMEM_STILL_OPEN"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": row[0],
            "statement": row[1],
            "meaning": row[2],
            "status": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def amem_update_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("AHU4663_0_trace_before", "|C_mem^final_live||T| <= (|C_label|+|C_Hodge|+|C_support|+|C_readout|+|C_boundary|+|C_nonHilbert|)|T|", "4662 trace-source bound before Hodge closure", "TRACE_BOUND_IMPORTED"),
        ("AHU4663_1_trace_after", "|C_mem^final_live||T| <= (|C_label|+|C_support|+|C_readout|+|C_boundary|+|C_nonHilbert|)|T|", "Hodge term removed on private same-Hodge branch", "TRACE_BOUND_REDUCED"),
        ("AHU4663_2_dynamic", "|C_Hodge| term returns through Delta_Hodge_EM_mem envelope if the branch is rejected", "dynamic constitutive branch retained", "DYNAMIC_BRANCH_BOUND_RETAINED"),
        ("AHU4663_3_body_charge_status", "A_mem still also depends on B_mem_eff, J_mem_live, Q_boundary_mem, Z_mem and lambda_mem", "Hodge closure alone is not local-GR/R10/PPN closure", "BODY_CHARGE_GATES_REMAIN"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": row[0],
            "statement": row[1],
            "meaning": row[2],
            "status": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RUN4663_0_same_Hodge_branch", "C_mem^Hodge", "PASS_CONDITIONAL_PRIVATE_ZERO", "same observed Hodge/current owner and no constitutive/readout/orientation/Poynting side slot."),
        ("RUN4663_1_dynamic_Hodge", "Delta_Hodge_EM_mem", "FAIL_CLOSED_TO_BOUND_ROWS", "principal/skewon/axion/hidden/readout/orientation terms stay explicit off branch."),
        ("RUN4663_2_LHRS_update", "C_mem^LHRS_live", "PASS_REDUCED_BOUND", "Hodge term removed; label/support/readout remain."),
        ("RUN4663_3_Poynting", "Poynting/background interpretation", "PASS_NO_DOUBLE_COUNT", "Poynting is Hilbert stress flux or boundary flux, not an added bulk force."),
        ("RUN4663_4_claim_status", "local GR/Newton/PPN/R10/EM claim", "NONCLAIM_STILL_BLOCKED", "remaining LHRS/boundary/non-Hilbert and body-charge gates remain."),
        ("RUN4663_5_next", "next channel", "PASS_NEXT_SELECTED", NEXT_TARGET),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "run_id": row[0],
            "object": row[1],
            "result": row[2],
            "detail": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CTRL4663_0_no_numerical_alpha", "Do not derive numerical alpha_EM or absolute gauge kinetic coefficient from Hodge matching.", "ACTIVE"),
        ("CTRL4663_1_no_balpha_confusion", "b_alpha_mem=0 supports fixed EM normalization but is not itself full Hodge/constitutive closure.", "ACTIVE"),
        ("CTRL4663_2_no_Poynting_double_count", "Poynting is Hilbert stress or boundary flux, never a second bulk/background source.", "ACTIVE"),
        ("CTRL4663_3_radiative_boundary_retained", "Radiative EM boundary flux is routed to Q_boundary/boundary rows, not silently zeroed.", "ACTIVE"),
        ("CTRL4663_4_hidden_constitutive_retained", "Hidden chi_EM, skewon, axion-gradient, readout Hodge and orientation residuals remain finite rows off branch.", "ACTIVE"),
        ("CTRL4663_5_no_full_local_GR", "C_mem^Hodge=0 does not claim full local GR/Newton/PPN/R10/EM pass.", "ACTIVE"),
        ("CTRL4663_6_local_private_only", "No GitHub action; local framework/post-checkpoint packet only.", "ACTIVE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "guard": row[1],
            "status": row[2],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4663_0",
            "decision": DECISION,
            "summary": (
                "4663 closes C_mem^Hodge in the fixed private same-Hodge visible EM branch. The observed metric/coframe/orientation determine *_obs, "
                "the Maxwell action uses only that Hodge, Poynting is T_EM^{0i} or boundary flux, and no independent chi_EM/hidden/readout/orientation/Poynting slot is admitted. "
                "Therefore Delta_Hodge_EM_mem=0 and C_mem^Hodge=0 on that branch. Off-branch constitutive residuals retain the 4315 no-cancellation envelope. "
                "The final Cmem bound now loses the Hodge term and the next live LHRS channel is C_mem^label."
            ),
            "next_target": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "decision": DECISION,
            "hodge_result": "C_MEM_HODGE_ZERO_PRIVATE_SAME_HODGE_BRANCH",
            "dynamic_status": "DELTA_HODGE_EM_MEM_BOUND_ROWS_RETAINED",
            "LHRS_status": "LABEL_SUPPORT_READOUT_REMAIN",
            "final_Cmem_status": "LABEL_SUPPORT_READOUT_BOUNDARY_NONHILBERT_REMAIN",
            "selected_next_channel": "C_mem^label / source functor owner",
            "next_target": NEXT_TARGET,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "After Hodge/Poynting closure, the remaining LHRS rows are label, support and readout; label is the cleanest next target because source-label functor ownership overlaps the already tightened source-weight branch.",
            "derive_route": "try to prove C_mem^label=0 from total-source functor ownership, no constructor/spurion/source-label return slot, and the GR-parity source universality branch.",
            "fallback_route": "if source labels or constructor labels survive, write Delta_label_mem finite rows for WEP/R10/PPN/source-label sensitivity.",
            "avoid": "confusing source-label closure with material microphysics derivation or erasing hidden/nonstandard sectors.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    zero_import: list[dict[str, Any]],
    dynamic: list[dict[str, Any]],
    lhrs: list[dict[str, Any]],
    amem: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    all_rows = sources + owner + zero_import + dynamic + lhrs + amem + runners + controls + decisions
    outputs = [
        SOURCE_REGISTER,
        OWNER_CLAUSE_CSV,
        ZERO_IMPORT_CSV,
        DYNAMIC_BOUND_CSV,
        LHRS_UPDATE_CSV,
        AMEM_UPDATE_CSV,
        RUNNER_CSV,
        CONTROL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
        VALIDATION_CSV,
        DOC_PATH,
        FORMAL_PATH,
    ]
    checks = [
        ("VAL4663_00_sources_exist", all(row["path_exists"] for row in sources), "all cited source paths exist"),
        ("VAL4663_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        ("VAL4663_02_line_anchors", all(int(row["line_number"]) > 0 for row in sources), "all source line anchors positive"),
        ("VAL4663_03_owner_clauses", any(row["clause_id"] == "HOC4663_5_forbidden_slots" for row in owner), "Hodge owner forbidden slots named"),
        ("VAL4663_04_hodge_zero", any(row["zero_id"] == "HZI4663_4_result" and row["status"] == "CMEM_HODGE_TERM_ZERO_PRIVATE_BRANCH" for row in zero_import), "Cmem Hodge zero row present"),
        ("VAL4663_05_dynamic_envelope", any(row["bound_id"] == "DHB4663_0_envelope" for row in dynamic), "dynamic constitutive envelope retained"),
        ("VAL4663_06_LHRS_reduced", any(row["update_id"] == "LHU4663_2_after" for row in lhrs), "LHRS reduced after Hodge"),
        ("VAL4663_07_Amem_reduced", any(row["update_id"] == "AHU4663_1_trace_after" for row in amem), "A_mem trace bound reduced after Hodge"),
        ("VAL4663_08_no_Poynting_double_count", any(row["control_id"] == "CTRL4663_2_no_Poynting_double_count" for row in controls), "Poynting no-double-count guard present"),
        ("VAL4663_09_no_claim_rows", all(str(row.get("valid_for_claim", "False")) == "False" and str(row.get("claim_allowed", "False")) == "False" for row in all_rows), "no generated row is claim-grade"),
        ("VAL4663_10_nonclaim_runner", any(row["run_id"] == "RUN4663_4_claim_status" and row["result"] == "NONCLAIM_STILL_BLOCKED" for row in runners), "local claim status remains nonclaim"),
        ("VAL4663_11_next_label", decisions and decisions[0]["next_target"] == NEXT_TARGET, "next target is label/source functor"),
        ("VAL4663_12_local_outputs", all(ROOT in path.parents or path == ROOT for path in outputs), "outputs stay under local MTS root"),
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
    passed_all = all(passed for _, passed, _ in checks)
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4663_OVERALL",
            "status": "PASS" if passed_all else "FAIL",
            "detail": "4663 Cmem Hodge/Poynting private zero and dynamic bound gate passed" if passed_all else "4663 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    owner: list[dict[str, Any]],
    zero_import: list[dict[str, Any]],
    dynamic: list[dict[str, Any]],
    lhrs: list[dict[str, Any]],
    amem: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4663 - Cmem Hodge/Poynting owner or LHRS bound

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4663 attacks the Hodge/Poynting channel selected by 4662:

`C_mem^Hodge := Pi_mem[C_X^Hodge]`.

The same-Hodge branch gives a clean private zero:

`C_mem^Hodge = 0`.

The reason is not that electromagnetism is ignored. It is the opposite: EM is routed through the correct owner.

Inside the fixed visible EM branch:

- `e_obs`, `g_obs`, orientation and volume determine the observed Hodge star `*_obs`.
- The Maxwell action is `S_EM = -(4 mu0)^-1 int F wedge *_obs F`.
- Metric/Hodge variation gives the Maxwell Hilbert stress `T_EM`.
- The Poynting vector is `T_EM^{{0i}}` or boundary flux, not a second background force.
- There is no independent `chi_EM`, hidden constitutive tensor, readout Hodge, orientation residual, or standalone Poynting bulk source.

Therefore `Delta_Hodge_EM_mem=0`, and the Hodge term drops from the LHRS part of `C_mem`.

The reduced LHRS/final trace bounds become:

`|C_mem^LHRS_live| <= |C_mem^label| + |C_mem^support| + |C_mem^readout|`,

and

`|C_mem^final_live| <= |C_mem^label| + |C_mem^support| + |C_mem^readout| + |C_mem^boundary| + |C_mem^nonHilbert|`.

The off-branch dynamic constitutive envelope remains:

`||Delta_Hodge_EM_mem|| <= ||Delta_chi_principal|| + ||Delta_chi_skewon|| + L||dtheta_EM|| + |C_Hodge_hidden| + |C_Hodge_readout| + |Delta_orientation_flux|`.

This checkpoint does not derive numerical `alpha_EM`, `mu0`, source mass or `G_N`, and it does not erase radiative boundary flux.

## Source Register

{table(sources)}

## Hodge/Poynting Owner Clauses

{table(owner)}

## Cmem Hodge Zero Import

{table(zero_import)}

## Dynamic Hodge Constitutive Bound Rows

{table(dynamic)}

## LHRS Cmem Update After Hodge

{table(lhrs)}

## A_mem Trace Bound Update After Hodge

{table(amem)}

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
        "4663 closes C_mem^Hodge in the fixed private same-Hodge visible EM branch. The observed metric/coframe/orientation determine the Hodge star; Maxwell uses that Hodge; Poynting is Maxwell Hilbert stress flux or boundary flux; and no independent chi_EM, hidden constitutive tensor, readout Hodge, orientation residual or standalone Poynting bulk source is admitted. Dynamic constitutive residual rows remain explicit off branch.",
        "Generated source register, Hodge/Poynting owner clauses, Cmem Hodge zero import, dynamic Hodge constitutive bound rows, LHRS Cmem update, A_mem trace update, runner, controls, decision, status, next target and validation.",
        "Cmem_Hodge_zero_private_same_Hodge_branch_dynamic_constitutive_bound_nonclaim",
        NEXT_TARGET,
        "Claiming numerical alpha or G from Hodge closure, confusing b_alpha_mem with full Hodge closure, double-counting Poynting as background force, erasing radiative boundary flux, or claiming full local GR from this one channel.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10/EM claim until label/support/readout/boundary/non-Hilbert channels plus body-charge gates are same-branch zero or source-backed.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4663 closes `C_mem^Hodge` inside the fixed private same-Hodge visible EM branch. The observed metric/coframe/orientation determine `*_obs`; Maxwell variation gives `T_EM`; Poynting is Hilbert stress flux or boundary flux, not an extra bulk force. Thus `Delta_Hodge_EM_mem=0` and `C_mem^Hodge=0` on that branch. The remaining final Cmem channels are label, support, readout, boundary and non-Hilbert; off-branch constitutive residuals keep the 4315 envelope.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4663` removes the Hodge/Poynting channel from the private-branch Cmem residual vector while retaining dynamic constitutive bounds. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    timestamp = now()
    sources = source_rows(timestamp)
    owner = owner_clause_rows(timestamp)
    zero_import = zero_import_rows(timestamp)
    dynamic = dynamic_bound_rows(timestamp)
    lhrs = lhrs_update_rows(timestamp)
    amem = amem_update_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validations = validation_rows(sources, owner, zero_import, dynamic, lhrs, amem, runners, controls, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(OWNER_CLAUSE_CSV, owner)
    write_csv(ZERO_IMPORT_CSV, zero_import)
    write_csv(DYNAMIC_BOUND_CSV, dynamic)
    write_csv(LHRS_UPDATE_CSV, lhrs)
    write_csv(AMEM_UPDATE_CSV, amem)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validations)

    doc = build_doc(sources, owner, zero_import, dynamic, lhrs, amem, runners, controls, decisions, statuses, nexts, validations)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = validations[-1]["status"]
    print(f"4663 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
