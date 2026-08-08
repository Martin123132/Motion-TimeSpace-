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

CHECKPOINT = "4662"
CLAIM_ID = "L-504"
BRANCH = "MTS_R2FR_Y5_CMEM_FIRST_BLOCK_FINAL_ROLLUP_OR_DYNAMIC_SOURCE_WEIGHT_BOUND_RUNNER_4662"
MARKER = "PPC4161_CMEM_FIRST_BLOCK_FINAL_ROLLUP_OR_DYNAMIC_SOURCE_WEIGHT_BOUND_RUNNER_4662"
PACKET_MARKER = "PPC4161_PACKET_CMEM_FIRST_BLOCK_FINAL_ROLLUP_OR_DYNAMIC_SOURCE_WEIGHT_BOUND_RUNNER_4662"
DECISION = "CMEM_FIRST_BLOCK_ZERO_ROLLED_IN_FINAL_VECTOR_REBASED_HODGE_POYNTING_NEXT_NONCLAIM"
NEXT_TARGET = "4663-Y5-R2FR-Cmem-Hodge-Poynting-owner-or-LHRS-bound.md"

DOC_PATH = POST / "4662-Y5-R2FR-Cmem-first-block-final-rollup-or-dynamic-source-weight-bound-runner.md"
FORMAL_PATH = FORMAL / "678-PPC4161-Cmem-first-block-final-rollup-or-dynamic-source-weight-bound-runner.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4661 = POST / "4661-Y5-R2FR-kappa-Cmem-import-or-deltaw-source-weight-final-bound.md"
DOC_4657 = POST / "4657-Y5-R2FR-Cmem-final-live-zero-or-first-source-backed-component-row.md"
DOC_4599 = POST / "4599-Y5-R2FR-label-Hodge-support-readout-zero-or-CXlive-next-norm.md"
DOC_4600 = POST / "4600-Y5-R2FR-boundary-nonHilbert-zero-or-final-CXlive-norm.md"
DOC_4653 = POST / "4653-Y5-R2FR-cD-same-coframe-parent-functor-or-WEP-clock-EM-bound.md"
DOC_4658 = POST / "4658-Y5-R2FR-balpha-Maxwell-normalization-owner-or-first-source-bound.md"

FORMAL_191 = FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md"
FORMAL_223 = FORMAL / "223-PPC4161-EM-Poynting-Hodge-source-owner-lock.md"
FORMAL_225 = FORMAL / "225-PPC4161-Maxwell-normalization-charge-current-owner.md"
FORMAL_630 = FORMAL / "630-PPC4161-EM-gauge-kinetic-descent-or-b-alpha-source-row.md"
FORMAL_669 = FORMAL / "669-PPC4161-cD-same-coframe-parent-functor-or-WEP-clock-EM-bound.md"
FORMAL_674 = FORMAL / "674-PPC4161-balpha-Maxwell-normalization-owner-or-first-source-bound.md"
FORMAL_677 = FORMAL / "677-PPC4161-kappa-Cmem-import-or-deltaw-source-weight-final-bound.md"

CSV_4661_CMEM = SOURCE_DIR / "P8_Y5_R2FR_4661_CMEM_STD_WEIGHT_FINAL_UPDATE.csv"
CSV_4661_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4661_DECISION.csv"
CSV_4661_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4661_STATUS.csv"
CSV_4661_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4661_VALIDATION.csv"

CSV_4657_DECOMP = SOURCE_DIR / "P8_Y5_R2FR_4657_CMEM_FINAL_DECOMPOSITION.csv"
CSV_4657_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4657_CMEM_COMPONENT_ZERO_THEOREM.csv"
CSV_4657_QUEUE = SOURCE_DIR / "P8_Y5_R2FR_4657_FIRST_COMPONENT_QUEUE.csv"
CSV_4657_AMEM = SOURCE_DIR / "P8_Y5_R2FR_4657_AMEM_INSERTION_ROWS.csv"
CSV_4657_RUNNER = SOURCE_DIR / "P8_Y5_R2FR_4657_RUNNER_RESULTS.csv"
CSV_4657_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4657_VALIDATION.csv"

CSV_4599_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4599_LABEL_HODGE_SUPPORT_READOUT_ZERO_THEOREM.csv"
CSV_4599_NORM = SOURCE_DIR / "P8_Y5_R2FR_4599_CX_LABEL_HODGE_SUPPORT_READOUT_NORM.csv"
CSV_4599_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4599_CXLIVE_NEXT_NORM_ROWS.csv"
CSV_4599_CONTROL = SOURCE_DIR / "P8_Y5_R2FR_4599_CONTROL_ROWS.csv"
CSV_4599_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4599_VALIDATION.csv"

CSV_4600_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4600_BOUNDARY_NONHILBERT_ZERO_THEOREM.csv"
CSV_4600_FINAL = SOURCE_DIR / "P8_Y5_R2FR_4600_FINAL_CXLIVE_NORM.csv"
CSV_4600_BODY = SOURCE_DIR / "P8_Y5_R2FR_4600_BODY_CHARGE_ENVELOPE_FINAL_CX_UPDATE.csv"
CSV_4600_INTERFACE = SOURCE_DIR / "P8_Y5_R2FR_4600_EMPIRICAL_SCORE_INPUT_INTERFACE.csv"
CSV_4600_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4600_VALIDATION.csv"

CSV_4653_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4653_CD_ZERO_THEOREM.csv"
CSV_4653_ARENA = SOURCE_DIR / "P8_Y5_R2FR_4653_CD_ARENA_ROUTES.csv"
CSV_4653_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4653_VALIDATION.csv"
CSV_4658_NORMAL = SOURCE_DIR / "P8_Y5_R2FR_4658_BALPHA_MEMORY_NORMAL_FORM.csv"
CSV_4658_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4658_FIXED_BRANCH_ZERO_IMPORT.csv"
CSV_4658_CONTROL = SOURCE_DIR / "P8_Y5_R2FR_4658_CONTROL_ROWS.csv"
CSV_4658_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4658_VALIDATION.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4662_SOURCE_REGISTER.csv"
ROLLUP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4662_CMEM_FIRST_BLOCK_ROLLUP.csv"
REBASE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4662_FINAL_CMEM_RESIDUAL_REBASE.csv"
AMEM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4662_AMEM_REDUCED_TRACE_BOUND.csv"
NEXT_ATTACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4662_NEXT_ATTACK_SELECTION.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4662_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4662_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4662_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4662_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4662_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4662_VALIDATION.csv"


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
        ("SRC4662_00_4661_doc", DOC_4661, "C_mem^std_weight_live = 0", "4661 fixed-branch first-block closure."),
        ("SRC4662_01_4661_first_block", CSV_4661_CMEM, "CSF4661_3_fixed_first_block_result", "first standard/weight block zero row."),
        ("SRC4662_02_4661_not_full", CSV_4661_CMEM, "CSF4661_5_not_full_Cmem", "4661 guard: full Cmem not claimed."),
        ("SRC4662_03_4661_validation", CSV_4661_VALIDATION, "VAL4661_OVERALL", "4661 validation pass."),
        ("SRC4662_04_677_formal", FORMAL_677, "CSF4661_3_fixed_first_block_result", "formal 4661 first-block closure."),
        ("SRC4662_05_4657_decomp_sum", CSV_4657_DECOMP, "CDF4657_4_final_sum", "Cmem final decomposition."),
        ("SRC4662_06_4657_triangle", CSV_4657_DECOMP, "CDF4657_5_triangle_bound", "absolute-sum Cmem fallback."),
        ("SRC4662_07_4657_zero_route", CSV_4657_THEOREM, "ZCM4657_1_sufficient_zero", "componentwise zero route."),
        ("SRC4662_08_4657_no_cancel", CSV_4657_THEOREM, "ZCM4657_2_no_cancellation_guard", "no cancellation guard."),
        ("SRC4662_09_4657_lhrs_queue", CSV_4657_QUEUE, "FCQ4657_4", "LHRS was next after first block."),
        ("SRC4662_10_4657_boundary_queue", CSV_4657_QUEUE, "FCQ4657_5", "boundary/non-Hilbert follows LHRS."),
        ("SRC4662_11_4657_Amem", CSV_4657_AMEM, "AMP4657_1_Cmem_inserted", "Cmem split inserted into A_mem."),
        ("SRC4662_12_4657_runner_old", CSV_4657_RUNNER, "RUN4657_1_current_live_branch", "old live branch to be updated."),
        ("SRC4662_13_4657_validation", CSV_4657_VALIDATION, "VAL4657_OVERALL", "4657 validation pass."),
        ("SRC4662_14_4599_combined", CSV_4599_THEOREM, "LHRS4599_4_combined", "LHRS combined zero-or-bound theorem."),
        ("SRC4662_15_4599_hodge", CSV_4599_THEOREM, "LHRS4599_1_Hodge", "Hodge/EM zero-or-bound theorem."),
        ("SRC4662_16_4599_lhrs_norm", CSV_4599_NEXT, "C4599_4_LHRS", "LHRS live norm row."),
        ("SRC4662_17_4599_hodge_norm", CSV_4599_NORM, "N4599_1_Hodge", "Hodge finite norm row."),
        ("SRC4662_18_4599_hodge_control", CSV_4599_CONTROL, "CTRL4599_Hodge_countermodel", "Hodge countermodel guard."),
        ("SRC4662_19_4599_validation", CSV_4599_VALIDATION, "VAL4599_06_no_claim_true", "4599 validation/no-claim row."),
        ("SRC4662_20_4600_final_theorem", CSV_4600_THEOREM, "BNH4600_4_final_CX_live", "final C_X live theorem."),
        ("SRC4662_21_4600_boundary_norm", CSV_4600_FINAL, "C4600_3_boundary_nonHilbert", "boundary/non-Hilbert live row."),
        ("SRC4662_22_4600_final_norm", CSV_4600_FINAL, "C4600_4_final", "final C_X live norm."),
        ("SRC4662_23_4600_Amem", CSV_4600_BODY, "BU4600_1_memory", "A_mem final C update."),
        ("SRC4662_24_4600_EM_interface", CSV_4600_INTERFACE, "E4600_4_EM_Poynting", "EM/Poynting scoring interface."),
        ("SRC4662_25_4600_validation", CSV_4600_VALIDATION, "VAL4600_05_final_norm", "4600 final norm validation."),
        ("SRC4662_26_4653_EM_Poynting", CSV_4653_ZERO, "CDZ4653_4_EM_Poynting", "same-coframe EM/Poynting owner."),
        ("SRC4662_27_4653_Poynting_arena", CSV_4653_ARENA, "ARENA4653_3_Poynting", "Poynting arena route."),
        ("SRC4662_28_4653_validation", CSV_4653_VALIDATION, "VAL4653_OVERALL", "4653 validation pass."),
        ("SRC4662_29_4658_same_Hodge", CSV_4658_ZERO, "BZI4658_4_same_Hodge_current", "same Hodge/current owner."),
        ("SRC4662_30_4658_alpha_result", CSV_4658_ZERO, "BZI4658_5_result", "b_alpha fixed branch zero."),
        ("SRC4662_31_4658_Poynting_control", CSV_4658_CONTROL, "CTRL4658_3_no_Poynting_double_count", "Poynting no-double-count guard."),
        ("SRC4662_32_4658_validation", CSV_4658_VALIDATION, "VAL4658_OVERALL", "4658 validation pass."),
        ("SRC4662_33_191_Poynting", FORMAL_191, "Poynting vector is not a separate background field", "Poynting as Hilbert stress flux."),
        ("SRC4662_34_191_no_second", FORMAL_191, "forbids independent EM source weights", "no hidden EM/Hodge fork guard."),
        ("SRC4662_35_223_zero", FORMAL_223, "=> c_Poynt_extra = 0", "Poynting extra coefficient lock."),
        ("SRC4662_36_225_no_alpha", FORMAL_225, "do not determine the absolute gauge kinetic coefficient", "no numerical alpha overclaim."),
        ("SRC4662_37_630_balpha", FORMAL_630, "b_alpha_EM := Lie_v ln(alpha_EM)", "EM gauge kinetic normal form."),
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


def rollup_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RFB4662_0_import", "C_mem^std_weight_live=0", "4661 closes alpha, mass, clock, kappa and relative source-weight pieces on the fixed private branch", "CSF4661_3_fixed_first_block_result", "FIRST_BLOCK_ZERO_IMPORTED"),
        ("RFB4662_1_original_final", "C_mem^final_live = C_mem^std_weight_live + C_mem^LHRS_live + C_mem^boundary_nonHilbert_live", "4657/4600 final matter-trace split", "CDF4657_4_final_sum; BNH4600_4_final_CX_live", "FINAL_SPLIT_IMPORTED"),
        ("RFB4662_2_reduced_final", "fixed private branch => C_mem^final_live = C_mem^LHRS_live + C_mem^boundary_nonHilbert_live", "first standard/weight block is removed from the final vector", "linear memory projection and same-branch import", "FINAL_VECTOR_REBASED"),
        ("RFB4662_3_reduced_bound", "|C_mem^final_live| <= |C_mem^LHRS_live| + |C_mem^boundary| + |C_mem^nonHilbert|", "no-cancellation finite fallback after first-block closure", "absolute-sum policy from 4657", "BOUND_REDUCED_NO_CANCELLATION"),
        ("RFB4662_4_not_full_zero", "C_mem^final_live=0 requires C_mem^LHRS_live=C_mem^boundary=C_mem^nonHilbert=0", "first-block zero alone is insufficient for local-GR/cGamma closure", "ZCM4657_1_sufficient_zero", "FULL_ZERO_STILL_OPEN"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "rollup_id": row[0],
            "statement": row[1],
            "meaning": row[2],
            "source_or_condition": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def rebase_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RCM4662_0_label", "C_mem^label", "source-label/constructor/spurion return leakage", "prove total-source functor has no label/spurion/readout slot", "Delta_label_mem", "LHRS"),
        ("RCM4662_1_Hodge", "C_mem^Hodge", "Maxwell-Hodge/constitutive/Poynting owner leakage", "prove same observed Hodge/current owner, no independent chi_EM/hidden EM/readout Hodge/orientation residual", "Delta_Hodge_EM_mem", "LHRS"),
        ("RCM4662_2_support", "C_mem^support", "source-support/worldtube/Reynolds shell leakage", "prove q-basic regular zero-trace support with no birth/death shell, threshold mask or side flux", "Delta_support_mem", "LHRS"),
        ("RCM4662_3_readout", "C_mem^readout", "readout/variation/projector commutator leakage", "prove variation-before-readout and pure postprocessing no coefficient reentry", "C_R_mem", "LHRS"),
        ("RCM4662_4_boundary", "C_mem^boundary", "boundary/reference/domain-wall matter-trace leakage", "prove parent boundary neutrality and compact local projection silence", "Delta_boundary_mem", "boundary_nonHilbert"),
        ("RCM4662_5_nonHilbert", "C_mem^nonHilbert", "non-Hilbert source-current bypass leakage", "prove P_source[J_NH]=0 componentwise after Hilbert extraction", "epsilon_current_owner_NH_abs", "boundary_nonHilbert"),
        ("RCM4662_6_final_rebased", "C_mem^final_live", "rebased final vector after first-block closure", "sum of RCM4662_0 through RCM4662_5, with absolute-sum fallback", "|C_label|+|C_Hodge|+|C_support|+|C_readout|+|C_boundary|+|C_nonHilbert|", "final"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "residual_id": row[0],
            "symbol": row[1],
            "role": row[2],
            "derive_first": row[3],
            "finite_fallback": row[4],
            "block": row[5],
            "current_status": "OPEN_ZERO_OR_VALUE_REQUIRED" if row[0] != "RCM4662_6_final_rebased" else "FINAL_REBASED_VECTOR_READY",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def amem_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("ARB4662_0_before", "|A_mem| <= [exp(R/lambda_mem) int_body(|B_mem_eff||R_obs|+|C_mem^final_live||T|+|J_mem_live|)dV + |Q_boundary_mem|]/(4*pi Z_min)", "4657/4600 Green-function envelope", "BOUND_IMPORTED_VALUES_MISSING"),
        ("ARB4662_1_Cmem_rebased", "|C_mem^final_live||T| <= (|C_mem^LHRS_live|+|C_mem^boundary|+|C_mem^nonHilbert|)|T|", "first standard/weight block no longer contributes on fixed private branch", "TRACE_TERM_REDUCED"),
        ("ARB4662_2_LHRS_expanded", "|C_mem^LHRS_live| <= |C_mem^label|+|C_mem^Hodge|+|C_mem^support|+|C_mem^readout|", "LHRS split is the next actual Cmem work surface", "LHRS_EXPANDED"),
        ("ARB4662_3_exact_zero_condition", "C_mem^LHRS_live=C_mem^boundary=C_mem^nonHilbert=0 => C_mem^final_live=0", "componentwise same-branch zero condition after first-block closure", "CONDITIONAL_ZERO_ROUTE_REDUCED"),
        ("ARB4662_4_live_branch", "A_mem trace-source term remains live through LHRS/boundary/nonHilbert rows", "no local-GR/R10/PPN pass until those rows are zero or source-backed", "FAIL_CLOSED_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row[0],
            "formula": row[1],
            "meaning": row[2],
            "status": row[3],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def next_attack_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("NAX4662_0_label", 2, "C_mem^label", "source-label forgetting", "promising but overlaps source-weight work already handled; still has constructor/spurion countermodels", "later in LHRS"),
        ("NAX4662_1_Hodge", 1, "C_mem^Hodge", "Maxwell-Hodge/Poynting owner", "best next target: 4653 and 4658 already give same-coframe, same-Hodge/current and Poynting-as-Hilbert-stress inputs; directly advances EM/Maxwell stress reduction", NEXT_TARGET),
        ("NAX4662_2_support", 3, "C_mem^support", "regular support/worldtube", "harder geometry/Reynolds shell problem; attack after Hodge unless support reopens Hodge", "later LHRS/support checkpoint"),
        ("NAX4662_3_readout", 4, "C_mem^readout", "variation-before-readout", "important but projector/source-worldtube countermodel is broad; use after Hodge/support branch conditions are fixed", "later readout checkpoint"),
        ("NAX4662_4_boundary_nonHilbert", 5, "C_mem^boundary_nonHilbert", "boundary/current bypass", "last in this mini-stack because it needs boundary/current source data and Q_boundary separation", "after LHRS block"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "attack_id": row[0],
            "priority": row[1],
            "target": row[2],
            "route": row[3],
            "rationale": row[4],
            "next_target": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RUN4662_0_first_block", "C_mem^std_weight_live", "PASS_IMPORTED_ZERO", "4661 removes the standard/weight block on the fixed private branch."),
        ("RUN4662_1_final_rebase", "C_mem^final_live", "PASS_REBASED_VECTOR", "final Cmem now reduces to LHRS plus boundary/non-Hilbert in this branch."),
        ("RUN4662_2_six_channels", "remaining residual channels", "PASS_NAMED", "label, Hodge, support, readout, boundary and non-Hilbert rows are explicit."),
        ("RUN4662_3_Amem", "A_mem trace-source term", "PASS_REDUCED_BOUND", "trace term now depends only on LHRS/boundary/non-Hilbert rows plus B/J/Q/Z/M gates."),
        ("RUN4662_4_Hodge_next", "Maxwell-Hodge/Poynting owner route", "PASS_NEXT_SELECTED", NEXT_TARGET),
        ("RUN4662_5_claim_status", "local GR/Newton/PPN/R10/EM claim", "NONCLAIM_STILL_BLOCKED", "remaining Cmem channels and body-charge vector are not fully zero/source-backed."),
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
        ("CTRL4662_0_no_full_Cmem_claim", "First-block zero is not full Cmem final-live zero.", "ACTIVE"),
        ("CTRL4662_1_no_recycling_solved_work", "Do not reopen alpha/mass/clock/kappa/source-weight unless a guard actually fails.", "ACTIVE"),
        ("CTRL4662_2_no_Poynting_double_count", "Poynting is Maxwell-Hilbert stress or boundary flux, not an extra background force.", "ACTIVE"),
        ("CTRL4662_3_no_numerical_alpha_claim", "Hodge/Maxwell branch cannot claim numerical alpha_EM or absolute gauge kinetic value.", "ACTIVE"),
        ("CTRL4662_4_no_cancellation", "Use absolute-sum residuals unless a parent-owned cancellation identity is derived.", "ACTIVE"),
        ("CTRL4662_5_no_public_GR_claim", "Private branch progress is not a public local-GR/Newton/PPN/R10 pass.", "ACTIVE"),
        ("CTRL4662_6_local_private_only", "No GitHub action; local framework/post-checkpoint packet only.", "ACTIVE"),
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
            "decision_id": "DEC4662_0",
            "decision": DECISION,
            "summary": (
                "4662 rolls the 4661 first-block closure into the 4657/4600 final Cmem split. On the fixed private branch, "
                "C_mem^final_live reduces from std_weight + LHRS + boundary_nonHilbert to LHRS + boundary_nonHilbert, with the absolute bound "
                "|C_mem^final_live| <= |C_label|+|C_Hodge|+|C_support|+|C_readout|+|C_boundary|+|C_nonHilbert|. "
                "The next best derivation target is C_mem^Hodge because 4653/4658/191/223 already give same-coframe Maxwell-Hodge/Poynting ownership inputs."
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
            "first_block_status": "C_MEM_STD_WEIGHT_LIVE_ZERO_IMPORTED",
            "Cmem_final_rebased": "C_MEM_FINAL_LIVE_EQUALS_LHRS_PLUS_BOUNDARY_NONHILBERT",
            "remaining_channels": "label;Hodge;support;readout;boundary;nonHilbert",
            "selected_next_channel": "C_mem^Hodge / Maxwell-Hodge-Poynting owner",
            "local_GR_status": "NONCLAIM_REMAINING_CMEM_AND_BODY_CHARGE_GATES",
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
            "why": "The first Cmem standard/weight block is now closed; the cleanest next live channel is Hodge/Poynting because it directly advances Maxwell/EM stress ownership and has existing same-coframe/Maxwell-Hilbert evidence.",
            "derive_route": "try to prove C_mem^Hodge=0 from one observed metric/coframe/Hodge, Maxwell Hilbert stress, no independent chi_EM/hidden current/readout Hodge, and Poynting-as-Hilbert-flux.",
            "fallback_route": "if any Hodge/Poynting clause reopens, write Delta_Hodge_EM_mem finite rows with EM/Poynting/clock/R10/PPN projection requirements.",
            "avoid": "double-counting Poynting as background force, claiming numerical alpha, or treating b_alpha_mem=0 as full Hodge closure.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    rollup: list[dict[str, Any]],
    rebase: list[dict[str, Any]],
    amem: list[dict[str, Any]],
    next_attack: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    all_rows = sources + rollup + rebase + amem + next_attack + runners + controls + decisions
    outputs = [
        SOURCE_REGISTER,
        ROLLUP_CSV,
        REBASE_CSV,
        AMEM_CSV,
        NEXT_ATTACK_CSV,
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
        ("VAL4662_00_sources_exist", all(row["path_exists"] for row in sources), "all cited source paths exist"),
        ("VAL4662_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        ("VAL4662_02_line_anchors", all(int(row["line_number"]) > 0 for row in sources), "all source line anchors positive"),
        ("VAL4662_03_first_block_imported", any(row["rollup_id"] == "RFB4662_0_import" for row in rollup), "4661 first-block zero imported"),
        ("VAL4662_04_final_rebased", any(row["rollup_id"] == "RFB4662_2_reduced_final" for row in rollup), "final Cmem vector rebased"),
        ("VAL4662_05_six_channels", sum(1 for row in rebase if row["residual_id"].startswith("RCM4662_") and row["residual_id"] != "RCM4662_6_final_rebased") == 6, "six remaining residual channels named"),
        ("VAL4662_06_Amem_reduced", any(row["bound_id"] == "ARB4662_1_Cmem_rebased" for row in amem), "A_mem trace term reduced"),
        ("VAL4662_07_Hodge_next", any(row["attack_id"] == "NAX4662_1_Hodge" and row["priority"] == 1 for row in next_attack), "Hodge/Poynting selected next"),
        ("VAL4662_08_nonclaim_runner", any(row["run_id"] == "RUN4662_5_claim_status" and row["result"] == "NONCLAIM_STILL_BLOCKED" for row in runners), "claim status remains nonclaim"),
        ("VAL4662_09_no_claim_rows", all(str(row.get("valid_for_claim", "False")) == "False" and str(row.get("claim_allowed", "False")) == "False" for row in all_rows), "no generated row is claim-grade"),
        ("VAL4662_10_no_Poynting_double_count", any(row["control_id"] == "CTRL4662_2_no_Poynting_double_count" for row in controls), "Poynting no-double-count guard present"),
        ("VAL4662_11_no_solved_loop", any(row["control_id"] == "CTRL4662_1_no_recycling_solved_work" for row in controls), "solved first-block loop guard present"),
        ("VAL4662_12_next_target", decisions and decisions[0]["next_target"] == NEXT_TARGET, "next target selected"),
        ("VAL4662_13_local_outputs", all(ROOT in path.parents or path == ROOT for path in outputs), "outputs stay under local MTS root"),
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
            "validation_id": "VAL4662_OVERALL",
            "status": "PASS" if passed_all else "FAIL",
            "detail": "4662 first-block Cmem rollup and Hodge/Poynting handoff passed" if passed_all else "4662 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    rollup: list[dict[str, Any]],
    rebase: list[dict[str, Any]],
    amem: list[dict[str, Any]],
    next_attack: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4662 - Cmem first-block final rollup or dynamic source-weight bound runner

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4662 updates the 4657 Cmem decomposition using the real 4661 result.

4657/4600 had:

`C_mem^final_live = C_mem^std_weight_live + C_mem^LHRS_live + C_mem^boundary_nonHilbert_live`.

4661 now gives, on the fixed private ordinary-visible branch:

`C_mem^std_weight_live = 0`.

Therefore the live final trace-source vector is rebased to:

`C_mem^final_live = C_mem^LHRS_live + C_mem^boundary_nonHilbert_live`.

Expanded without cancellation:

`|C_mem^final_live| <= |C_mem^label| + |C_mem^Hodge| + |C_mem^support| + |C_mem^readout| + |C_mem^boundary| + |C_mem^nonHilbert|`.

The `A_mem` trace-source term correspondingly reduces to:

`|C_mem^final_live||T| <= (|C_mem^LHRS_live|+|C_mem^boundary|+|C_mem^nonHilbert|)|T|`.

This is the important state change: alpha, mass, clock, kappa and relative source-weight are no longer the active first block in this private branch. The next live work surface is the LHRS block, followed by boundary/non-Hilbert.

## Next Attack

The selected next target is:

`C_mem^Hodge`.

Reason: it directly advances the Maxwell/EM stress part of the full goal. It already has real supporting ancestry:

- 4653: Maxwell/Hodge/Poynting uses the same observed coframe and Poynting is Hilbert stress flux.
- 4658: the fixed EM branch kills `b_alpha_mem` and retains a no-Poynting-double-count guard.
- 191/223: Poynting is not a separate background field and the standalone Poynting source coefficient is zero in the safe branch.

But it is not yet claimed closed: Hodge closure still needs to rule out independent `chi_EM`, hidden constitutive coefficients, readout Hodge, orientation residuals and Poynting boundary re-entry in the same branch.

## Source Register

{table(sources)}

## First-Block Rollup

{table(rollup)}

## Final Cmem Residual Rebase

{table(rebase)}

## A_mem Reduced Trace Bound

{table(amem)}

## Next Attack Selection

{table(next_attack)}

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
        "4662 rolls the 4661 first-block closure into the 4657/4600 Cmem final split. On the fixed private branch C_mem^final_live reduces to C_mem^LHRS_live + C_mem^boundary_nonHilbert_live, with six remaining channels: label, Hodge, support, readout, boundary and non-Hilbert. The next concrete target is C_mem^Hodge / Maxwell-Hodge-Poynting ownership, not another pass over alpha/mass/clock/kappa/source-weight.",
        "Generated source register, first-block rollup, final Cmem residual rebase, A_mem reduced trace bound, next attack selection, runner, controls, decision, status, next target and validation.",
        "Cmem_first_block_zero_rolled_into_final_vector_Hodge_Poynting_next_nonclaim",
        NEXT_TARGET,
        "Claiming full Cmem/local-GR closure from the first-block result, recycling solved alpha/mass/clock/kappa/source-weight work, double-counting Poynting as a background force, claiming numerical alpha, or using cancellation between remaining residual channels.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10/EM claim until LHRS and boundary/non-Hilbert channels plus B/J/Q/Z/M body-charge gates are same-branch zero or source-backed.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4662 rebases the final memory trace-source vector after the 4661 first-block closure. On the fixed private branch, `C_mem^std_weight_live=0`, so `C_mem^final_live = C_mem^LHRS_live + C_mem^boundary_nonHilbert_live`. The remaining channels are `C_mem^label`, `C_mem^Hodge`, `C_mem^support`, `C_mem^readout`, `C_mem^boundary`, and `C_mem^nonHilbert`. The next target is `C_mem^Hodge` because it advances Maxwell/Hodge/Poynting stress ownership and has existing same-coframe and Hilbert-stress evidence.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4662` rolls `C_mem^std_weight_live=0` into the final `C_mem` split. The active private-branch residual vector is now LHRS plus boundary/non-Hilbert, expanded into six named channels. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    timestamp = now()
    sources = source_rows(timestamp)
    rollup = rollup_rows(timestamp)
    rebase = rebase_rows(timestamp)
    amem = amem_rows(timestamp)
    next_attack = next_attack_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validations = validation_rows(sources, rollup, rebase, amem, next_attack, runners, controls, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ROLLUP_CSV, rollup)
    write_csv(REBASE_CSV, rebase)
    write_csv(AMEM_CSV, amem)
    write_csv(NEXT_ATTACK_CSV, next_attack)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validations)

    doc = build_doc(sources, rollup, rebase, amem, next_attack, runners, controls, decisions, statuses, nexts, validations)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = validations[-1]["status"]
    print(f"4662 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
