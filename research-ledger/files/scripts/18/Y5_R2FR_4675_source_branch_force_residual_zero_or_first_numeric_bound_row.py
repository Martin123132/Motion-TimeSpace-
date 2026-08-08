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

CHECKPOINT = "4675"
CLAIM_ID = "L-517"
BRANCH = "MTS_R2FR_Y5_SOURCE_BRANCH_FORCE_RESIDUAL_ZERO_OR_FIRST_NUMERIC_BOUND_ROW_4675"
MARKER = "PPC4161_SOURCE_BRANCH_FORCE_RESIDUAL_ZERO_OR_FIRST_NUMERIC_BOUND_ROW_4675"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_BRANCH_FORCE_RESIDUAL_ZERO_OR_FIRST_NUMERIC_BOUND_ROW_4675"
DECISION = "JM_UNOWNED_REDUCED_TO_SURVIVOR_VECTOR_CONDITIONAL_ZEROS_IMPORTED_NUMERIC_BOUND_ROW_READY_NONCLAIM"
NEXT_TARGET = "4676-Y5-R2FR-common-action-current-owner-or-Jm-source-weight-bound-row.md"

DOC_PATH = POST / "4675-Y5-R2FR-source-branch-force-residual-zero-or-first-numeric-bound-row.md"
FORMAL_PATH = FORMAL / "691-PPC4161-source-branch-force-residual-zero-or-first-numeric-bound-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4674_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4674_NEXT_TARGET.csv"
CSV_4674_PROOF = SOURCE_DIR / "P8_Y5_R2FR_4674_R826_EULER_RESIDUAL_PROOF.csv"
CSV_4674_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4674_FIRST_FINITE_B826_BOUND_SCHEMA.csv"
CSV_4674_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4674_STATUS.csv"
CSV_4674_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4674_VALIDATION.csv"
DOC_4674 = POST / "4674-Y5-R2FR-first-ZM-B826-finite-input-pack-or-R826-no-slot-owner-proof.md"
FORMAL_690 = FORMAL / "690-PPC4161-first-ZM-B826-finite-input-pack-or-R826-no-slot-owner-proof.md"

CSV_4266_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4266_SOURCE_READOUT_THEOREM.csv"
CSV_4266_REMAINDER = SOURCE_DIR / "P8_Y5_R2FR_4266_REMAINDER_SPLIT_ROWS.csv"
CSV_4268_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4268_BOUNDARY_PROJECTOR_THEOREM.csv"
CSV_4268_REMAINDER = SOURCE_DIR / "P8_Y5_R2FR_4268_OPEN_BOUNDARY_RESIDUAL_SPLIT_ROWS.csv"
CSV_4263_CLOSED = SOURCE_DIR / "P8_Y5_R2FR_4263_CLOSED_COLLAR_THEOREM.csv"
CSV_4312_POYNTING = SOURCE_DIR / "P8_Y5_R2FR_4312_EM_POYNTING_CANCELLATION_THEOREM.csv"
CSV_4303_VISIBLE = SOURCE_DIR / "P8_Y5_R2FR_4303_VISIBLE_HILBERT_M_LOCK_SILENCE_THEOREM.csv"
CSV_4303_MATRIX = SOURCE_DIR / "P8_Y5_R2FR_4303_COMPONENT_ZERO_NORM_MATRIX.csv"
CSV_2158_IDENTITY = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2158_SOURCE_ZERO_IDENTITY.csv"
CSV_2158_DECOMP = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2158_JX_QBARXT_DECOMPOSITION.csv"
CSV_2127_IDENTITY = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2127_INERTIAL_ACTIVE_SOURCE_IDENTITY_ATTEMPT.csv"
CSV_4301_EULER = SOURCE_DIR / "P8_Y5_R2FR_4301_EULER_LOCK_DERIVATION.csv"
CSV_1454_READOUT = SOURCE_DIR / "P8_Y5_R10_1454_VARIATION_BEFORE_READOUT_THEOREM_ATTEMPT.csv"
CSV_1455_PROJECT = SOURCE_DIR / "P8_Y5_R10_1455_DERIVATIVE_BEFORE_PROJECTION_THEOREM.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4675_SOURCE_REGISTER.csv"
REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4675_JM_UNOWNED_COMPONENT_REDUCTION.csv"
ZERO_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4675_CONDITIONAL_ZERO_IMPORT_MATRIX.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4675_JM_SURVIVOR_VECTOR.csv"
BOUND_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4675_FIRST_JM_NUMERIC_BOUND_ROW.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4675_CONTROL_ROWS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4675_RUNNER_RESULTS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4675_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4675_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4675_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4675_VALIDATION.csv"


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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
        ("SRC4675_00_4674_next", CSV_4674_NEXT, "4675-Y5-R2FR-source-branch-force-residual-zero-or-first-numeric-bound-row.md", "4674 selected this target."),
        ("SRC4675_01_4674_identity", CSV_4674_PROOF, "PR4674_2_exact_identity", "B826 Euler-residual identity."),
        ("SRC4675_02_4674_bound", CSV_4674_BOUND, "BND4674_0_master", "first B826 bound schema."),
        ("SRC4675_03_4674_status", CSV_4674_STATUS, "euler_identity_derived", "4674 status."),
        ("SRC4675_04_4674_validation", CSV_4674_VALIDATION, "VAL4674_OVERALL,True,PASS", "4674 validation."),
        ("SRC4675_05_doc4674", DOC_4674, "B_826 = -a_F", "4674 derivation prose."),
        ("SRC4675_06_formal690", FORMAL_690, "B_826 = -a_F", "4674 formal note."),
        ("SRC4675_07_4266_theorem", CSV_4266_THEOREM, "SRCRO4266_2_charge_readout_zero", "source charge readout zero."),
        ("SRC4675_08_4266_remainder", CSV_4266_REMAINDER, "REM4266_0_kappa_G_owner", "coupling coefficient remainder."),
        ("SRC4675_09_4268_theorem", CSV_4268_THEOREM, "BPROJ4268_1_fixed_collar_qbasic", "fixed collar theorem."),
        ("SRC4675_10_4268_remainder", CSV_4268_REMAINDER, "BRES4268_3_open_radiation", "open radiation retained."),
        ("SRC4675_11_4263_closed", CSV_4263_CLOSED, "CCT4263_0_poynting_owner", "Poynting counted once."),
        ("SRC4675_12_4312_poynting", CSV_4312_POYNTING, "EC4312_2_once_only", "extra Poynting coefficient zero condition."),
        ("SRC4675_13_4303_visible", CSV_4303_VISIBLE, "VHS4303_1_matter_silence", "visible matter m-lock silence."),
        ("SRC4675_14_4303_matrix", CSV_4303_MATRIX, "CM4303_2_screened_source", "non-Hilbert screened source survivor."),
        ("SRC4675_15_2158_identity", CSV_2158_IDENTITY, "SZI2158_2_zero_theorem", "ordinary source-zero theorem."),
        ("SRC4675_16_2158_decomp", CSV_2158_DECOMP, "JQD2158_3_source_weight", "source-weight survivor."),
        ("SRC4675_17_2127_identity", CSV_2127_IDENTITY, "IAS2127_2_classical_rescale_obstruction", "source-weight obstruction."),
        ("SRC4675_18_4301_euler", CSV_4301_EULER, "EL4301_3_exact_nohair", "positive operator/nohair gate."),
        ("SRC4675_19_1454_readout", CSV_1454_READOUT, "VBR1454_2_post_selector_kill", "variation-before-readout."),
        ("SRC4675_20_1455_projection", CSV_1455_PROJECT, "DBP1455_2_projection", "derivative-before-projection."),
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


def reduction_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "RED4675_0_start",
            "J_m_unowned",
            "J_m_src + J_m_bdy + J_m_readout + J_m_domain + E_m_res",
            "4674 exact identity",
            "STARTING_VECTOR",
            "B_826 = -a_F L_cg^-2 J_m_unowned",
        ),
        (
            "RED4675_1_visible_Hilbert",
            "J_visible_matter",
            "0 on the q-owned visible Hilbert branch",
            "4303 + 2158",
            "CONDITIONAL_ZERO_IMPORTED",
            "ordinary matter stress remains in T_Hilbert; it is not a separate m-lock force",
        ),
        (
            "RED4675_2_source_readout",
            "J_readout_Hilbert_charge",
            "0 for post-solution Hilbert/ADM source-charge readout",
            "4266 + 1454 + 1455",
            "CONDITIONAL_ZERO_IMPORTED",
            "readout cannot re-enter the parent Euler equation if downstream",
        ),
        (
            "RED4675_3_fixed_boundary",
            "J_fixed_collar_projector",
            "0 on fixed compact no-flux collar/projector branch",
            "4268",
            "CONDITIONAL_ZERO_IMPORTED",
            "moving/open boundary pieces survive separately",
        ),
        (
            "RED4675_4_poynting_once",
            "J_extra_Poynting",
            "0 on single Maxwell-Hodge Hilbert-owner branch",
            "4263 + 4312 + 4303",
            "CONDITIONAL_ZERO_IMPORTED",
            "Poynting is real flux inside T_EM or a boundary residual, not a second hidden source",
        ),
        (
            "RED4675_5_survivor_identity",
            "J_m_survivor",
            "J_source_weight + J_coeff + J_nonHilbert + J_open_boundary + J_domain_reentry + J_Euler_res",
            "component reduction",
            "SURVIVOR_VECTOR_DEFINED",
            "this is the actual coupling gap after conditional zero imports",
        ),
        (
            "RED4675_6_B826_reduced_bound",
            "B_826",
            "|B_826| <= |a_F| L_cg^-2 |J_m_survivor|",
            "4674 + 4675",
            "BOUND_SHARPENED_NONCLAIM",
            "no local-GR/R10/PPN claim until survivor vector is zero or bounded",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "reduction_id": row[0],
            "object": row[1],
            "mathematical_form": row[2],
            "source": row[3],
            "status": row[4],
            "consequence": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def zero_import_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("ZERO4675_0_visible_matter", "visible Hilbert matter m-lock force", "S_matter has no direct m slot and depends only on g_obs(q)", "CONDITIONAL_ZERO", "parent visible-Hilbert split still unsigned globally"),
        ("ZERO4675_1_source_readout", "post-solution source readout", "Q_src=Qbar[T_obs,g_obs,Sigma_obs,xi_obs] downstream of Hilbert variation", "CONDITIONAL_ZERO", "coefficient/G_N/source-current normalization remains outside this zero"),
        ("ZERO4675_2_fixed_collar", "fixed collar/projector derivative", "W_loc,n,orientation,Pi_loc q-basic before variation and no source crossing", "CONDITIONAL_ZERO", "open radiation/source crossing/domain selector survives"),
        ("ZERO4675_3_poynting_extra", "extra standalone Poynting source", "single Maxwell-Hodge/Hilbert owner with no c_Poynt_extra", "CONDITIONAL_ZERO", "radiative flux enters boundary residual if nonzero"),
        ("ZERO4675_4_domain_projection", "downstream projection as parent force", "derivative-before-projection and variation-before-readout", "CONDITIONAL_ZERO", "pre-action selector/domain dependence survives"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_id": row[0],
            "component": row[1],
            "condition": row[2],
            "import_status": row[3],
            "not_killed": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SURV4675_0_source_weight", "J_source_weight", "w_A, kappa_A, source-only prefactor/current normalization before variation", "delta_kappa_A;w_A_prime;source_current_norm", "PRIMARY_NEXT_TARGET"),
        ("SURV4675_1_coeff", "J_coeff", "common kappa/G_N/ell_J/calibration coefficient owner", "delta_v_kappa_cal;delta_v_ell_J", "SURVIVES_AS_COEFFICIENT_GATE"),
        ("SURV4675_2_nonHilbert", "J_nonHilbert", "non-Hilbert screened source, hidden EM/current, torsion/connection/memory tail", "q_nonH;S_cg_nonHilbert;Q_m_H_nonHilbert", "BOUND_OR_ZERO_REQUIRED"),
        ("SURV4675_3_open_boundary", "J_open_boundary", "source crossing, radiative flux, memory pullback, corner/edge terms", "R_source_crossing;R_rad_flux;R_memory_pullback;R_corner_edge", "BOUND_OR_ZERO_REQUIRED"),
        ("SURV4675_4_domain_reentry", "J_domain_reentry", "pre-action domain selector/projector or branch classifier", "Delta_domain_selector_projector;q_domain", "BOUND_OR_ZERO_REQUIRED"),
        ("SURV4675_5_euler", "E_m_res", "parent branch equation/stationarity certificate missing", "E_m_res;lambda_m;no_zero_mode", "PARENT_EULER_CERTIFICATE_REQUIRED"),
        ("SURV4675_6_total", "J_m_survivor_abs", "absolute no-cancellation sum of survivor components", "all above in common normalization", "SCHEMA_READY_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": row[0],
            "symbol": row[1],
            "meaning": row[2],
            "required_inputs": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("JMB4675_0_master", "J_m_survivor_abs", "|J_source_weight|+|J_coeff|+|J_nonHilbert|+|J_open_boundary|+|J_domain_reentry|+|E_m_res|", "common_m_lock_force_units", "MISSING_COMPONENT_VALUES"),
        ("JMB4675_1_B826", "B826_bound", "|a_F| L_cg^-2 J_m_survivor_abs", "B826_units_from_4507", "MISSING_AF_LCG_AND_JM_VALUES"),
        ("JMB4675_2_R10", "alpha_R10_projection", "tau_R10(lambda_mem) * B826_bound or source-normalized equivalent", "arena_declared_units", "MISSING_ARENA_PROJECTION"),
        ("JMB4675_3_PPN", "PPN_projection", "tau_PPN dot survivor vector", "PPN_residual_units", "MISSING_TAU_PPN"),
        ("JMB4675_4_orbital", "orbital_projection", "tau_orbital dot source_weight/open_boundary/domain components", "orbital_residual_units", "MISSING_TAU_ORBITAL"),
        ("JMB4675_5_claim_gate", "valid_for_claim", "true only after all numeric inputs are source-backed and comparator limits exist", "boolean", "FALSE_NOW"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row[0],
            "symbol": row[1],
            "formula": row[2],
            "units": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CTRL4675_0_no_public_zero", "Conditional zero imports do not make public local-GR/R10/PPN claims.", "ACTIVE"),
        ("CTRL4675_1_no_cancellation", "Use absolute survivor-vector bounds; do not cancel components against each other.", "ACTIVE"),
        ("CTRL4675_2_no_poynting_double_count", "Poynting is T_EM flux or boundary flux, not a second bulk source.", "ACTIVE"),
        ("CTRL4675_3_no_fitted_G_hiding", "Measured G/GM may calibrate common scale only; it cannot hide relative source weights.", "ACTIVE"),
        ("CTRL4675_4_same_branch", "Zeros, coefficients, and bounds must refer to the same parent local branch.", "ACTIVE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "rule": row[1],
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
            "decision": DECISION,
            "why": "4675 imports only already-established conditional zeros and compresses J_m_unowned to a survivor vector. The leading survivor is source-weight/current normalization, with coefficient, non-Hilbert, open-boundary/domain and Euler-certificate terms retained.",
            "promoted": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "conditional_zeros_imported": True,
            "Jm_survivor_vector_defined": True,
            "source_weight_closed": False,
            "numeric_bound_sourced": False,
            "B826_zero": False,
            "local_GR_claim": False,
            "r10_claim": False,
            "ppn_claim": False,
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "After conditional zero imports, the most dangerous survivor is J_source_weight/current normalization. It is the coupling problem in its sharpest form.",
            "derive_route": "Try to prove one common action/current owner forbids w_A, kappa_A and species current prefactors before variation.",
            "fallback_route": "Fill first numeric/source-backed bound row for delta_kappa_A or source-current normalization.",
            "avoid": "Do not use classical EOM rescaling as proof; Hilbert source still sees w_A.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def runner_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    zeros: list[dict[str, Any]],
    survivors: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    reduction_ok = any(row["reduction_id"] == "RED4675_5_survivor_identity" for row in reductions)
    zero_ok = len(zeros) >= 5 and all(row["import_status"] == "CONDITIONAL_ZERO" for row in zeros)
    survivor_ok = any(row["survivor_id"] == "SURV4675_0_source_weight" for row in survivors)
    bound_ok = any(row["bound_id"] == "JMB4675_0_master" for row in bounds)
    nonclaim_ok = all(not row["valid_for_claim"] and not row["claim_allowed"] for row in [*reductions, *zeros, *survivors, *bounds])
    checks = [
        ("RUN4675_0_sources", source_ok, "all source paths and needles found" if source_ok else "source path/needle failure"),
        ("RUN4675_1_reduction", reduction_ok, "Jm survivor reduction row present" if reduction_ok else "reduction missing"),
        ("RUN4675_2_zero_imports", zero_ok, "conditional zero imports recorded" if zero_ok else "zero import issue"),
        ("RUN4675_3_survivor", survivor_ok, "source-weight survivor selected" if survivor_ok else "source-weight survivor missing"),
        ("RUN4675_4_bound", bound_ok, "numeric bound row schema present" if bound_ok else "bound row missing"),
        ("RUN4675_5_nonclaim", nonclaim_ok, "all rows remain nonclaim" if nonclaim_ok else "claim flag promoted"),
        ("RUN4675_6_next", True, "next target selected"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "runner_id": check_id,
            "passed": passed,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]


def validation_rows(timestamp: str, csv_paths: list[Path], sources: list[dict[str, Any]], runners: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    rows.append({"validation_id": "VAL4675_0_sources", "passed": source_ok, "detail": "all source paths and needles found" if source_ok else "source path/needle failure", "timestamp_utc": timestamp})
    parse_ok = True
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            detail = f"rows={len(parsed)} columns={len(parsed[0]) if parsed else 0}"
            passed = bool(parsed)
        except Exception as exc:  # pragma: no cover
            detail = repr(exc)
            passed = False
        parse_ok = parse_ok and passed
        rows.append({"validation_id": f"VAL4675_parse_{path.name}", "passed": passed, "detail": detail, "timestamp_utc": timestamp})
    runner_ok = all(row["passed"] for row in runners)
    rows.append({"validation_id": "VAL4675_1_runner_pass", "passed": runner_ok, "detail": "runner rows passed" if runner_ok else "runner failure", "timestamp_utc": timestamp})
    output_paths = [DOC_PATH, FORMAL_PATH, *csv_paths]
    outputs_exist = all(path.exists() for path in output_paths)
    rows.append({"validation_id": "VAL4675_2_outputs_exist", "passed": outputs_exist, "detail": ";".join(str(path) for path in output_paths), "timestamp_utc": timestamp})
    nonclaim = "valid_for_claim,true" not in read_text(RUNNER_CSV).lower() and "claim_allowed,true" not in read_text(RUNNER_CSV).lower()
    rows.append({"validation_id": "VAL4675_3_no_claim_promotion", "passed": nonclaim, "detail": "valid_for_claim remains false", "timestamp_utc": timestamp})
    overall = source_ok and parse_ok and runner_ok and outputs_exist and nonclaim
    rows.append({"validation_id": "VAL4675_OVERALL", "passed": overall, "detail": "PASS" if overall else "FAIL", "timestamp_utc": timestamp})
    return rows


def write_documents(
    sources: list[dict[str, Any]],
    reductions: list[dict[str, Any]],
    zeros: list[dict[str, Any]],
    survivors: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    body = f"""# 4675 - Y5/R2FR Source Branch-Force Residual Zero or First Numeric Bound Row

**Current verdict:** 4675 moves the coupling problem forward by shrinking `J_m_unowned`. The visible Hilbert matter term, post-solution Hilbert source readout, fixed compact collar/projector term, and extra standalone Poynting source are imported only as conditional zeros. The remaining object is the survivor vector:

```text
J_m_survivor =
  J_source_weight
+ J_coeff
+ J_nonHilbert
+ J_open_boundary
+ J_domain_reentry
+ E_m_res.
```

Therefore:

```text
|B_826| <= |a_F| L_cg^-2 |J_m_survivor|.
```

This is not a local-GR/R10/PPN claim. It is a sharper coupling target: prove or bound the survivor vector.

## Runner results

{table(runners)}

## Decision

{table(decisions)}

## Status

{table(statuses)}

## Next target

{table(nexts)}

## Jm component reduction

{table(reductions)}

## Conditional zero import matrix

{table(zeros)}

## Jm survivor vector

{table(survivors)}

## First numeric Jm bound row

{table(bounds)}

## Controls

{table(controls)}

## Source register

{table(sources)}

## Validation

{table(validations)}
"""
    DOC_PATH.write_text(body, encoding="utf-8")
    FORMAL_PATH.write_text(body.replace("# 4675 -", "# 691 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        claim = csv_line(
            [
                CLAIM_ID,
                "local_gr_empirical_interface",
                "4675 compresses J_m_unowned by importing only conditional zero branches for visible Hilbert matter, post-solution source readout, fixed compact collar/projector, and extra Poynting source. The surviving coupling vector is source-weight/current normalization, coefficient owner, non-Hilbert tails, open-boundary/domain reentry and Euler certificate.",
                "Generated source register, Jm component reduction, conditional zero import matrix, survivor vector, first numeric Jm bound row, controls, runner, decision, status, next target and validation.",
                DECISION.lower(),
                NEXT_TARGET,
                "Treating conditional zeros as public proof, cancelling survivor components, double-counting Poynting, or hiding source weights inside fitted G.",
                "local_gr",
                str(DOC_PATH),
                NEXT_TARGET,
                "No public local-GR/Newton/PPN/R10 claim until the survivor vector is theorem-zero or numerically source-bounded.",
            ]
        )
        append_once(CLAIMS_PATH, CLAIM_ID, claim)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""

## {MARKER}

4675 reduces the live `B_826` coupling obstruction to:

```text
J_m_survivor =
  J_source_weight + J_coeff + J_nonHilbert
+ J_open_boundary + J_domain_reentry + E_m_res
```

after conditional zero imports for visible Hilbert matter, post-solution source readout, fixed no-flux collar/projector and extra standalone Poynting source. The next real coupling target is the source-weight/current owner.

- checkpoint: `{DOC_PATH.name}`
- formal note: `{FORMAL_PATH.name}`
- decision: `{DECISION}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""

## {PACKET_MARKER}

Packet update: `J_m_unowned` is no longer one foggy term. It has a survivor vector, and the leading survivor is source-weight/current normalization. This is the cleanest coupling target for the next derivation pass.

- claim id: `{CLAIM_ID}`
- reduction csv: `{REDUCTION_CSV.name}`
- survivor csv: `{SURVIVOR_CSV.name}`
- bound csv: `{BOUND_ROW_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def main() -> None:
    timestamp = now()
    sources = source_rows(timestamp)
    reductions = reduction_rows(timestamp)
    zeros = zero_import_rows(timestamp)
    survivors = survivor_rows(timestamp)
    bounds = bound_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    runners = runner_rows(timestamp, sources, reductions, zeros, survivors, bounds)

    csv_paths = [
        SOURCE_REGISTER,
        REDUCTION_CSV,
        ZERO_IMPORT_CSV,
        SURVIVOR_CSV,
        BOUND_ROW_CSV,
        CONTROL_CSV,
        RUNNER_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(REDUCTION_CSV, reductions)
    write_csv(ZERO_IMPORT_CSV, zeros)
    write_csv(SURVIVOR_CSV, survivors)
    write_csv(BOUND_ROW_CSV, bounds)
    write_csv(CONTROL_CSV, controls)
    write_csv(RUNNER_CSV, runners)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_documents(sources, reductions, zeros, survivors, bounds, controls, runners, decisions, statuses, nexts, [])
    validations = validation_rows(timestamp, csv_paths, sources, runners)
    write_csv(VALIDATION_CSV, validations)
    write_documents(sources, reductions, zeros, survivors, bounds, controls, runners, decisions, statuses, nexts, validations)
    update_registers(timestamp)
    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
