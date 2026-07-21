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

CHECKPOINT = "4669"
CLAIM_ID = "L-511"
BRANCH = "MTS_R2FR_Y5_BMEM_JMEM_QBOUNDARY_ZM_SOURCE_NORMALIZATION_GATE_4669"
MARKER = "PPC4161_BMEM_JMEM_QBOUNDARY_ZM_SOURCE_NORMALIZATION_GATE_4669"
PACKET_MARKER = "PPC4161_PACKET_BMEM_JMEM_QBOUNDARY_ZM_SOURCE_NORMALIZATION_GATE_4669"
DECISION = "BJQ_ZM_ZERO_ROUTE_ATTEMPTED_NOT_PARENT_SIGNED_FIRST_BODY_CHARGE_ROW_CONTRACT_LOCKED_NONCLAIM"
NEXT_TARGET = "4670-Y5-R2FR-Zmem-M2mem-positive-parent-Hessian-or-Bmem-first-component-source-row.md"

DOC_PATH = POST / "4669-Y5-R2FR-Bmem-Jmem-Qboundary-ZM-source-normalization-zero-or-first-body-charge-row.md"
FORMAL_PATH = FORMAL / "685-PPC4161-Bmem-Jmem-Qboundary-ZM-source-normalization-gate.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

DOC_4668 = POST / "4668-Y5-R2FR-Cmem-final-zero-to-body-charge-source-charge-gate.md"
FORMAL_684 = FORMAL / "684-PPC4161-Cmem-final-zero-to-body-charge-source-charge-gate.md"
CSV_4668_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4668_NEXT_TARGET.csv"
CSV_4668_RESIDUAL = SOURCE_DIR / "P8_Y5_R2FR_4668_REDUCED_BODY_CHARGE_RESIDUAL_VECTOR.csv"
CSV_4668_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4668_STATUS.csv"
CSV_4668_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4668_VALIDATION.csv"

CSV_4514_BMEM = SOURCE_DIR / "P8_Y5_R2FR_4514_BMEM_EFFECTIVE_COMPONENT_VECTOR.csv"
CSV_4514_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4514_BODY_CHARGE_INSERTION_BOUND.csv"
CSV_4515_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4515_CMEM_JMEM_COUPLING_VECTOR.csv"
CSV_4515_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4515_SOURCE_FUNCTOR_DESCENT_THEOREM.csv"
CSV_4515_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4515_SOURCE_COUPLING_BOUND.csv"
CSV_4516_DEBT = SOURCE_DIR / "P8_Y5_R2FR_4516_REMAINING_SOURCE_DEBT.csv"
CSV_4596_JMEM = SOURCE_DIR / "P8_Y5_R2FR_4596_JMEM_JH_REDUCED_RESIDUAL_VECTOR.csv"
CSV_4596_COEFF = SOURCE_DIR / "P8_Y5_R2FR_4596_FIRST_BODY_CHARGE_COEFFICIENT_ROWS.csv"
CSV_4595_MEM = SOURCE_DIR / "P8_Y5_R2FR_4595_MEMORY_BODY_CHARGE_BOUND.csv"
CSV_4601_SCORE = SOURCE_DIR / "P8_Y5_R2FR_4601_BODY_CHARGE_SCORE_VECTOR.csv"
CSV_4621_IDENTITY = SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_POSITIVE_OPERATOR_IDENTITY.csv"
CSV_4621_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4621_MEMORY_AMPLITUDE_BOUND_ROWS.csv"
CSV_4621_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4621_ZMEM_M2MEM_SOURCE_ROWS_NONCLAIM.csv"
CSV_4622_DECOMP = SOURCE_DIR / "P8_Y5_R2FR_4622_RHOMEM_CHANNEL_DECOMPOSITION.csv"
CSV_4622_POYNTING = SOURCE_DIR / "P8_Y5_R2FR_4622_EM_POYNTING_ZERO_AND_BOUND_RULES.csv"
CSV_4628_HESSIAN = SOURCE_DIR / "P8_Y5_R2FR_4628_PARENT_HESSIAN_ROWS.csv"
CSV_4628_GAP = SOURCE_DIR / "P8_Y5_R2FR_4628_LAMBDA_MEM_GAP_ROWS.csv"
CSV_4628_NUM = SOURCE_DIR / "P8_Y5_R2FR_4628_ZMEM_M2MEM_FIRST_NUMERIC_TEMPLATE_NONCLAIM.csv"
CSV_4012_CHARGE = SOURCE_DIR / "P8_Y5_R2FR_4012_PIM_HTAU_CHARGE_LOCK_THEOREM.csv"
CSV_4012_FINITE = SOURCE_DIR / "P8_Y5_R2FR_4012_CHARGE_GLUE_FINITE_ROWS.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4669_SOURCE_REGISTER.csv"
ZERO_ATTEMPT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4669_BJQ_ZM_ZERO_ATTEMPT_MATRIX.csv"
FIRST_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4669_FIRST_BODY_CHARGE_SOURCE_ROW_CONTRACT.csv"
RESIDUAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4669_REMAINING_SOURCE_NORMALIZATION_VECTOR.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4669_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4669_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4669_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4669_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4669_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4669_VALIDATION.csv"


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
        ("SRC4669_00_4668_next", CSV_4668_NEXT, "4669-Y5-R2FR-Bmem-Jmem-Qboundary-ZM-source-normalization-zero-or-first-body-charge-row.md", "4668 selected B/J/Q/ZM."),
        ("SRC4669_01_4668_residual", CSV_4668_RESIDUAL, "RES4668_7_source_row_contract", "4668 source row contract."),
        ("SRC4669_02_4668_status", CSV_4668_STATUS, "REDUCED_TO_BMEM_JMEM_QBOUNDARY_ZM_GATE", "4668 status."),
        ("SRC4669_03_4668_validation", CSV_4668_VALIDATION, "VAL4668_OVERALL", "4668 validation."),
        ("SRC4669_04_doc4668", DOC_4668, "B_mem_eff / J_mem_live / Q_boundary_mem / Z_mem,M2_mem", "4668 prose target."),
        ("SRC4669_05_formal684", FORMAL_684, "rho_mem = B_mem_eff R_obs + J_mem_live", "formal 4668 reduction."),
        ("SRC4669_06_4514_Bmem_combined", CSV_4514_BMEM, "BMV4514_6_combined", "B_mem_eff component vector."),
        ("SRC4669_07_4514_Y5", CSV_4514_BMEM, "BMV4514_2_Y5_trace", "B_Y5 tail."),
        ("SRC4669_08_4514_bound", CSV_4514_BOUND, "BCB4514_4_nohair", "body-charge nohair criterion."),
        ("SRC4669_09_4515_common", CSV_4515_THEOREM, "SFT4515_1_single_source_functor_zero", "source functor common zero theorem."),
        ("SRC4669_10_4515_B", CSV_4515_THEOREM, "SFT4515_2_Y5_measured_GM", "Y5 source-normalization zero contract."),
        ("SRC4669_11_4515_Poynting", CSV_4515_THEOREM, "SFT4515_4_EM_Poynting_guard", "Jmem Poynting guard."),
        ("SRC4669_12_4515_vector_total", CSV_4515_VECTOR, "SCV4515_4_total_density_source", "rho_mem source vector."),
        ("SRC4669_13_4515_Qboundary", CSV_4515_VECTOR, "SCV4515_3_Qboundary_mem", "Q_boundary zero route."),
        ("SRC4669_14_4515_bound", CSV_4515_BOUND, "SB4515_3_nohair", "source-coupling nohair criterion."),
        ("SRC4669_15_4516_debt_boundary", CSV_4516_DEBT, "RSD4516_5_boundary", "remaining boundary debt."),
        ("SRC4669_16_4596_J_total", CSV_4596_JMEM, "J4596_5_live_total", "Jmem live vector."),
        ("SRC4669_17_4596_J_nonHilbert", CSV_4596_JMEM, "J4596_2_nonHilbert", "Jmem non-Hilbert survivor."),
        ("SRC4669_18_4596_coeff", CSV_4596_COEFF, "CO4596_6_Qboundary", "first coefficient rows."),
        ("SRC4669_19_4595_amplitude", CSV_4595_MEM, "MEM4595_2_amplitude", "memory amplitude bound."),
        ("SRC4669_20_4601_Z", CSV_4601_SCORE, "BCV4601_00", "Z_mem score row."),
        ("SRC4669_21_4601_B", CSV_4601_SCORE, "BCV4601_03", "B_mem_eff score row."),
        ("SRC4669_22_4601_J", CSV_4601_SCORE, "BCV4601_05", "J_mem score row."),
        ("SRC4669_23_4601_Q", CSV_4601_SCORE, "BCV4601_06", "Q_boundary score row."),
        ("SRC4669_24_4621_nohair", CSV_4621_IDENTITY, "MPI4621_2_nohair_zero", "positive operator nohair theorem."),
        ("SRC4669_25_4621_bound", CSV_4621_BOUND, "AMB4621_1_finite_H1", "finite H1 bound."),
        ("SRC4669_26_4621_Zsource", CSV_4621_SOURCE, "ZMR4621_0_Zmem_min", "Zmem source row."),
        ("SRC4669_27_4621_Msource", CSV_4621_SOURCE, "ZMR4621_1_M2mem_min", "M2mem source row."),
        ("SRC4669_28_4622_decomp", CSV_4622_DECOMP, "RDEC4622_5_hidden", "rho_mem hidden source decomposition."),
        ("SRC4669_29_4622_poynting", CSV_4622_POYNTING, "EMP4622_1_poynting_volume_to_boundary", "Poynting finite/zero rule."),
        ("SRC4669_30_4628_hessian", CSV_4628_HESSIAN, "HES4628_1_parent_hessian_definitions", "parent Hessian definitions."),
        ("SRC4669_31_4628_gap", CSV_4628_GAP, "GAP4628_0_exact_positive_gap", "positive gap criterion."),
        ("SRC4669_32_4628_numeric", CSV_4628_NUM, "LNUM4628_0_Zmem", "first numeric Z/M template."),
        ("SRC4669_33_4012_charge", CSV_4012_CHARGE, "CHG4012_6_charge_glue_finite_vector", "charge glue finite vector."),
        ("SRC4669_34_4012_finite", CSV_4012_FINITE, "CGLUE4012_0_master", "charge glue master residual."),
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


def zero_attempt_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("ZAT4669_0_ZM", "Z_mem,M2_mem", "Z_mem_min>0 and M2_mem_min>0 from the same parent quadratic Hessian", "4621;4628", "CONDITIONAL_POSITIVE_OPERATOR_THEOREM_VALUES_MISSING"),
        ("ZAT4669_1_B826", "B_826", "branch extremum/source-root signs R_m=0 with X_B fixed and m_L parent-owned", "4514 BMV4514_0", "CONDITIONAL_ZERO_UNSIGNED"),
        ("ZAT4669_2_BWeyl", "B_Weyl_vec", "all Weyl/metric-response vector components zero in the same branch", "4514 BMV4514_1", "VECTOR_STAGED_NONCLAIM"),
        ("ZAT4669_3_BY5", "B_Y5_trace", "single q-basic Hilbert-current source functor with q-basic Pi_M and no source-normalization hair", "4515 SFT4515_1;SFT4515_2", "CONDITIONAL_ZERO_NOT_PARENT_SIGNED"),
        ("ZAT4669_4_BY6", "B_Y6_trace", "extra stress is topological/invisible/EH-owned metric response/exchange-even", "4515 SFT4515_3", "CONDITIONAL_ZERO_NOT_PARENT_SIGNED"),
        ("ZAT4669_5_Bboundary_readout", "B_src_boundary+B_src_readout", "source-functional boundary/reference and readout/calibration shifts have no linear memory response", "4514 BMV4514_4;BMV4514_5", "CONDITIONAL_ZERO_NOT_PARENT_SIGNED"),
        ("ZAT4669_6_Bmem_eff", "B_mem_eff", "all B components ZAT4669_1..5 vanish componentwise with no cancellation", "4514 BMV4514_6", "ZERO_ATTEMPT_FAILS_CURRENT_PARENT_SIGNATURE"),
        ("ZAT4669_7_JEM", "J_mem^EM_open", "same Hodge/current owner plus stationary no-radiative/no-Poynting-flux collar", "4515 SFT4515_4;4596 J4596_1", "CONDITIONAL_ZERO_UNSIGNED"),
        ("ZAT4669_8_JnonHilbert", "J_mem^nonHilbert", "no retained non-Hilbert source current, not merely C_mem non-Hilbert silence", "4515 SCV4515_1;4596 J4596_2", "LIVE_CURRENT_NOT_CLOSED_BY_4667"),
        ("ZAT4669_9_Jdyn", "J_mem^dyn_exchange", "stationary exchange closure and same tau/source clock lock", "4596 J4596_3", "CONDITIONAL_ZERO_UNSIGNED"),
        ("ZAT4669_10_Jboundary_readout", "J_mem^boundary_readout", "boundary/readout source-reference neutrality theorem", "4596 J4596_4", "CONDITIONAL_ZERO_UNSIGNED"),
        ("ZAT4669_11_Jmem_live", "J_mem_live", "JEM, JnonHilbert, Jdyn and Jboundary_readout vanish componentwise", "4596 J4596_5", "ZERO_ATTEMPT_FAILS_CURRENT_PARENT_SIGNATURE"),
        ("ZAT4669_12_Qboundary", "Q_boundary_mem", "fixed no-flux/topological boundary class with no linked source-normalization boundary charge", "4515 SCV4515_3;4596 CO4596_6", "ZERO_ATTEMPT_FAILS_CURRENT_PARENT_SIGNATURE"),
        ("ZAT4669_13_total", "A_mem exact zero", "Z/M positive and B_mem_eff=J_mem_live=Q_boundary_mem=0 in the same branch", "4514;4515;4621;4668", "NOT_PROMOTED_FIRST_ROW_REQUIRED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "attempt_id": row[0],
            "component": row[1],
            "zero_condition": row[2],
            "source_basis": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def first_row_contract(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("FBC4669_0_system", "system_id", "named source/body/local arena", "nonempty identifier and source path", "required"),
        ("FBC4669_1_operator", "Z_mem,M2_mem,lambda_mem", "positive same-branch operator normalization and range", "finite positive Z_mem and M2_mem or parent-signed constraint elimination", "required"),
        ("FBC4669_2_B", "B_mem_eff", "curvature/source-normalization source vector", "componentwise theorem-zero or finite values for B826,BWeyl,BY5,BY6,Bboundary,Breadout", "required"),
        ("FBC4669_3_profiles", "R_obs,T_obs,body_profile", "body/source profiles and units", "finite profiles or theorem-zero domain", "required"),
        ("FBC4669_4_J", "J_mem_live", "EM/Poynting, non-Hilbert, dynamic exchange and boundary-readout current", "componentwise theorem-zero or finite flux/current norms", "required"),
        ("FBC4669_5_Q", "Q_boundary_mem", "Green-function boundary charge", "zero flux/topological class or finite boundary integral", "required"),
        ("FBC4669_6_source_charge", "Pi_M/H_tau/M_H_ref", "same-source charge normalizer", "positive same-frame M_H_ref and charge-glue gate", "required"),
        ("FBC4669_7_guard", "no_cancellation_guard", "absolute sum policy", "ABS_SUM_NO_CANCELLATION; no fitted G/GM source definition", "required"),
        ("FBC4669_8_claim", "valid_for_claim", "claim admission switch", "true only when all required fields are numeric/source-backed or parent-signed zero", "false_now"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "field_id": row[0],
            "field": row[1],
            "meaning": row[2],
            "claim_grade_requirement": row[3],
            "status": row[4],
            "example_value": "MISSING_NOT_ALLOWED_FOR_CLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def residual_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RSN4669_0_master", "epsilon_BJQZM", "|B_mem_eff|_profile+|J_mem_live|_profile+|Q_boundary_mem|/(4*pi|Z_mem|)+epsilon_ZM+epsilon_charge_4012", "reduced body/source charge obstruction after 4669", "finite rows required"),
        ("RSN4669_1_Bmem", "B_mem_eff", "abs(B826)+abs(BWeyl)+abs(BY5)+abs(BY6)+abs(Bsrc_boundary)+abs(Bsrc_readout)", "no cancellation between B components", "first target family"),
        ("RSN4669_2_Jmem", "J_mem_live", "abs(J_EM_open)+abs(J_nonHilbert)+abs(J_dyn_exchange)+abs(J_boundary_readout)", "J current channels remain distinct", "first target family"),
        ("RSN4669_3_Qboundary", "Q_boundary_mem", "abs(Green boundary charge)", "separate from C_mem^boundary already closed", "first target family"),
        ("RSN4669_4_ZM", "epsilon_ZM", "blocked if Z_mem<=0, M2_mem<=0, lambda_mem undefined, or parent Hessian missing", "operator positivity/range gate", "first target family"),
        ("RSN4669_5_charge_glue", "epsilon_charge_4012", "same-charge finite vector from 4012", "source normalization to Newton/Poisson still requires this", "open gate"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "residual_id": row[0],
            "quantity": row[1],
            "formula": row[2],
            "meaning": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("RUN4669_0_attempt_zero", "B/J/Q/ZM exact zero", "FAIL_CLOSED", "zero route is identified but not parent-signed for all components in the same branch."),
        ("RUN4669_1_ZM", "positive Z/M", "CONDITIONAL_THEOREM_VALUES_MISSING", "operator identity/nohair theorem exists, but parent Hessian values or constraint elimination are missing."),
        ("RUN4669_2_Bmem", "B_mem_eff", "FAIL_CLOSED_TO_COMPONENT_ROWS", "B826/BWeyl/Y5/Y6/source-boundary/source-readout zeros are not all signed."),
        ("RUN4669_3_Jmem", "J_mem_live", "FAIL_CLOSED_TO_CURRENT_ROWS", "Poynting, retained non-Hilbert current, dynamic exchange and boundary-readout currents are not all killed."),
        ("RUN4669_4_Qboundary", "Q_boundary_mem", "FAIL_CLOSED_TO_BOUNDARY_ROW", "Green-function boundary charge is not the same as the closed C_mem boundary bookkeeping term."),
        ("RUN4669_5_claim_status", "local GR/Newton/PPN/R10 claim", "NONCLAIM_STILL_BLOCKED", "body-charge zero and same-source normalization remain incomplete."),
        ("RUN4669_6_next", "next channel", "PASS_NEXT_SELECTED", NEXT_TARGET),
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
        ("CTRL4669_0_no_promotion", "Do not promote B/J/Q/ZM zero unless every component is parent-signed in the same branch.", "ACTIVE"),
        ("CTRL4669_1_no_cancellation", "No cancellation between B, J, Q and Z/M components; absolute sums only.", "ACTIVE"),
        ("CTRL4669_2_no_Cmem_reopen", "Do not reopen solved Cmem channels to hide unresolved body-charge components.", "ACTIVE"),
        ("CTRL4669_3_no_Poynting_erasure", "Poynting/radiative flux is a Hilbert-owned no-flux theorem or finite current row.", "ACTIVE"),
        ("CTRL4669_4_no_boundary_confusion", "Q_boundary_mem is a Green-function boundary charge separate from C_mem^boundary.", "ACTIVE"),
        ("CTRL4669_5_no_fitted_G", "No fitted G/GM/orbital calibration may define the source-normalization row.", "ACTIVE"),
        ("CTRL4669_6_local_private_only", "No GitHub action; local framework/post-checkpoint packet only.", "ACTIVE"),
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
            "decision_id": "DEC4669_0",
            "decision": DECISION,
            "summary": (
                "4669 tries the exact-zero route for the remaining reduced body-charge/source-normalization gate. "
                "The route is mathematically clean: positive same-branch Z_mem/M2_mem plus B_mem_eff=0, J_mem_live=0 and Q_boundary_mem=0 would make A_mem=0 after 4668. "
                "Current evidence does not parent-sign that package. B_mem_eff still contains B826, BWeyl, Y5/Y6 and source-boundary/readout tails; J_mem_live still contains EM/Poynting, non-Hilbert, dynamic and boundary-readout currents; Q_boundary_mem is a separate Green-function boundary charge; and Z/M still needs parent Hessian values or constraint elimination. "
                "The pass condition is therefore refused and the first body-charge source-row contract is locked."
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
            "zero_attempt_status": "BJQ_ZM_ZERO_ROUTE_IDENTIFIED_NOT_PARENT_SIGNED",
            "first_row_status": "FIRST_BODY_CHARGE_SOURCE_ROW_CONTRACT_LOCKED",
            "body_charge_status": "A_MEM_ZERO_NOT_CLAIMED",
            "source_charge_status": "PI_M_HTAU_MHREF_CHARGE_GLUE_STILL_OPEN",
            "local_GR_status": "NONCLAIM_STILL_BLOCKED",
            "selected_next_channel": "Z_mem/M2_mem parent Hessian or first B_mem component",
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
            "why": "4669 shows the exact zero route is not parent-signed; the first useful hard input is the positive Z/M Hessian or the first B_mem_eff component row.",
            "derive_route": "try to parent-sign Z_mem>0 and M2_mem>0 from the quadratic memory Hessian; in parallel test whether B826/BWeyl/Y5/Y6/source-boundary/readout tails can be zeroed by the existing branch signatures.",
            "fallback_route": "if the Hessian or B component zero fails, write the first source-backed numeric/theorem-zero row with units and source paths, still nonclaim.",
            "avoid": "claiming A_mem zero from a conditional route, treating R10 anchor smoke as parent Z/M, or deleting Poynting/non-Hilbert currents by naming them Cmem.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    zero_attempt: list[dict[str, Any]],
    first_row: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    all_rows = sources + zero_attempt + first_row + residuals + runners + controls + decisions
    outputs = [
        SOURCE_REGISTER,
        ZERO_ATTEMPT_CSV,
        FIRST_ROW_CSV,
        RESIDUAL_CSV,
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
        ("VAL4669_00_sources_exist", all(row["path_exists"] for row in sources), "all cited source paths exist"),
        ("VAL4669_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        ("VAL4669_02_line_anchors", all(int(row["line_number"]) > 0 for row in sources), "all source line anchors positive"),
        ("VAL4669_03_total_attempt", any(row["attempt_id"] == "ZAT4669_13_total" for row in zero_attempt), "total BJQ/ZM zero attempt present"),
        ("VAL4669_04_zero_refused", any(row["attempt_id"] == "ZAT4669_13_total" and row["status"] == "NOT_PROMOTED_FIRST_ROW_REQUIRED" for row in zero_attempt), "zero route is refused rather than promoted"),
        ("VAL4669_05_first_row_contract", any(row["field_id"] == "FBC4669_8_claim" for row in first_row), "first body-charge source-row contract present"),
        ("VAL4669_06_residual_master", any(row["residual_id"] == "RSN4669_0_master" for row in residuals), "remaining residual master present"),
        ("VAL4669_07_nonclaim_runner", any(row["run_id"] == "RUN4669_5_claim_status" and row["result"] == "NONCLAIM_STILL_BLOCKED" for row in runners), "local claim remains blocked"),
        ("VAL4669_08_no_promotion_control", any(row["control_id"] == "CTRL4669_0_no_promotion" for row in controls), "no-promotion control present"),
        ("VAL4669_09_no_claim_rows", all(str(row.get("valid_for_claim", "False")) == "False" and str(row.get("claim_allowed", "False")) == "False" for row in all_rows), "no generated row is claim-grade"),
        ("VAL4669_10_next_ZM_Bmem", decisions and decisions[0]["next_target"] == NEXT_TARGET, "next target is Z/M or Bmem first component"),
        ("VAL4669_11_local_outputs", all(ROOT in path.parents or path == ROOT for path in outputs), "outputs stay under local MTS root"),
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
            "validation_id": "VAL4669_OVERALL",
            "status": "PASS" if passed_all else "FAIL",
            "detail": "4669 BJQ/ZM zero attempt and first source-row contract gate passed" if passed_all else "4669 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    zero_attempt: list[dict[str, Any]],
    first_row: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4669 - Bmem/Jmem/Qboundary/ZM source-normalization zero or first body-charge row

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4669 attacks the reduced body-charge gate left by 4668:

`rho_mem = B_mem_eff R_obs + J_mem_live`,

with Green boundary charge `Q_boundary_mem` and operator denominator/range `Z_mem,M2_mem,lambda_mem`.

The exact zero route is:

`Z_mem>0`, `M2_mem>0`, `B_mem_eff=0`, `J_mem_live=0`, `Q_boundary_mem=0`

all in the same branch.

That route would imply:

`A_mem=0`.

But it is not parent-signed by the current corpus. The result is therefore deliberately fail-closed:

`A_mem=0` is not claimed.

The useful forward product is the exact first body-charge row contract. Any future pass must fill or parent-sign `Z_mem`, `M2_mem`, `lambda_mem`, the component vector for `B_mem_eff`, the component vector for `J_mem_live`, `Q_boundary_mem`, the same-source `Pi_M/H_tau/M_H_ref` gate, units, source paths, and an absolute no-cancellation guard.

## Source Register

{table(sources)}

## BJQ/ZM Zero Attempt Matrix

{table(zero_attempt)}

## First Body-Charge Source Row Contract

{table(first_row)}

## Remaining Source-Normalization Vector

{table(residuals)}

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
        "4669 attempts the exact zero route for the reduced B_mem_eff/J_mem_live/Q_boundary_mem/Z_mem,M2_mem source-normalization gate. The route is clean but not parent-signed: A_mem=0 would require positive same-branch Z/M and componentwise B=J=Q=0, while current evidence leaves B826/BWeyl/Y5/Y6/source-boundary/readout tails, EM/Poynting/non-Hilbert/dynamic/boundary-readout currents, Green boundary charge, and parent Hessian values open. The checkpoint refuses promotion and locks the first body-charge source-row contract.",
        "Generated source register, BJQ/ZM zero attempt matrix, first body-charge source-row contract, residual vector, runner, controls, decision, status, next target and validation.",
        "BJQ_ZM_zero_route_attempted_not_parent_signed_first_body_charge_row_contract_nonclaim",
        NEXT_TARGET,
        "Promoting conditional BJQ/ZM zero, using cancellation, reopening Cmem to hide body-charge pieces, erasing Poynting/non-Hilbert currents, confusing Q_boundary_mem with C_mem boundary, or using fitted G/GM/R10 anchor smoke as parent Z/M.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/R10 claim until a positive parent Z/M Hessian or constraint route and the B/J/Q components are same-branch derived or source-backed.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4669 tries to close the reduced body-charge/source-normalization gate left by 4668. The exact zero route is componentwise and same-branch: positive `Z_mem,M2_mem`, `B_mem_eff=0`, `J_mem_live=0`, and `Q_boundary_mem=0`. Current evidence does not parent-sign the package, so `A_mem=0` is refused. The first body-charge source-row contract is now explicit; next work should either parent-sign positive `Z/M` or fill the first `B_mem_eff` component row.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4669` refuses a fake BJQ/ZM zero pass and locks the first body-charge source-row contract. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    timestamp = now()
    sources = source_rows(timestamp)
    zero_attempt = zero_attempt_rows(timestamp)
    first_row = first_row_contract(timestamp)
    residuals = residual_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validations = validation_rows(sources, zero_attempt, first_row, residuals, runners, controls, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_ATTEMPT_CSV, zero_attempt)
    write_csv(FIRST_ROW_CSV, first_row)
    write_csv(RESIDUAL_CSV, residuals)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validations)

    doc = build_doc(sources, zero_attempt, first_row, residuals, runners, controls, decisions, statuses, nexts, validations)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = validations[-1]["status"]
    print(f"4669 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
